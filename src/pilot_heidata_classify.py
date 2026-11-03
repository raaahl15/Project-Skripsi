"""Pilot (feasibility) step 2: classify cell condition from per-cell features (heiDATA).

Validation: leave-one-FIGURE-out (all cells of one experiment/figure held out), so the model is always
tested on an experiment it never saw. Pooled out-of-fold predictions -> balanced accuracy and ROC AUC.
A label-permutation test (same CV) estimates how likely the score is under "no signal".

Usage:
    python src/pilot_heidata_classify.py --cells results/pilot-heidata/cells.csv --out results/pilot-heidata
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
LAMIN_FEATS = ["area_um2", "perimeter_um", "eq_diameter_um", "major_axis_um", "minor_axis_um",
               "eccentricity", "solidity", "circularity", "lamin_mean", "lamin_std", "lamin_rim_core_ratio"]
CA_FEATS = ["ca_puncta_nucleus", "ca_puncta_perinuclear"]

TASKS = {
    # name: (row filter, positive class rule, feature list, description)
    "T1a_vpx_lamin": (lambda d: d.condition.isin(["+Vpx", "-Vpx"]), lambda d: d.condition == "+Vpx",
                      LAMIN_FEATS, "+Vpx vs -Vpx, Lamin B1 morphometry only (all figures)"),
    "T1b_vpx_lamin_ca": (lambda d: d.condition.isin(["+Vpx", "-Vpx"]) & d.ca_puncta_nucleus.notna(),
                         lambda d: d.condition == "+Vpx", LAMIN_FEATS + CA_FEATS,
                         "+Vpx vs -Vpx, Lamin B1 + HIV-1 CA puncta (figures with CA channel)"),
    "T2_infected_vs_mock": (lambda d: d.index == d.index, lambda d: d.condition != "Mock",
                            LAMIN_FEATS, "HIV-exposed (+/-Vpx) vs Mock, Lamin B1 morphometry only"),
}
MODELS = {
    "logreg": make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                            LogisticRegression(class_weight="balanced", max_iter=2000)),
    "rf": make_pipeline(SimpleImputer(strategy="median"),
                        RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                               min_samples_leaf=3, random_state=SEED, n_jobs=-1)),
}


def oof_predict(model, X, y, groups):
    proba = np.zeros(len(y))
    for tr, te in LeaveOneGroupOut().split(X, y, groups):
        m = clone(model).fit(X[tr], y[tr])
        proba[te] = m.predict_proba(X[te])[:, 1]
    return proba


def evaluate(model, X, y, groups, n_perm, rng):
    proba = oof_predict(model, X, y, groups)
    pred = (proba >= 0.5).astype(int)
    bacc = balanced_accuracy_score(y, pred)
    auc = roc_auc_score(y, proba)
    perm = []
    for _ in range(n_perm):
        yp = rng.permutation(y)
        perm.append(roc_auc_score(yp, oof_predict(model, X, yp, groups)))
    p = (1 + np.sum(np.array(perm) >= auc)) / (1 + n_perm)
    return {"balanced_accuracy": round(bacc, 3), "roc_auc": round(auc, 3),
            "perm_auc_mean": round(float(np.mean(perm)), 3), "perm_p_value": round(float(p), 3),
            "confusion_matrix[[TN,FP],[FN,TP]]": confusion_matrix(y, pred).tolist()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default="results/pilot-heidata/cells.csv")
    ap.add_argument("--out", default="results/pilot-heidata")
    ap.add_argument("--n-perm", type=int, default=100)
    ap.add_argument("--norm", choices=["none", "figure"], default="none",
                    help="'figure': robust-standardize every feature within each figure/experiment "
                         "(label-free; removes per-experiment staining/imaging offsets = batch effect)")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    df = pd.read_csv(args.cells)
    out = Path(args.out)
    suffix = "" if args.norm == "none" else f"_norm-{args.norm}"
    if args.norm == "figure":
        feats_all = [c for c in LAMIN_FEATS + CA_FEATS if c in df.columns]
        def _robust_z(s):
            iqr = s.quantile(0.75) - s.quantile(0.25)
            return (s - s.median()) / (iqr if iqr > 0 else 1.0)
        df[feats_all] = df.groupby("figure")[feats_all].transform(_robust_z)

    results = {}
    for tname, (rows, pos, feats, desc) in TASKS.items():
        d = df[rows(df)].copy()
        X, y, g = d[feats].to_numpy(float), pos(d).astype(int).to_numpy(), d.figure.to_numpy()
        res = {"description": desc, "n_cells": int(len(d)), "n_positive": int(y.sum()),
               "figures(groups)": sorted(set(g)), "models": {}}
        for mname, model in MODELS.items():
            res["models"][mname] = evaluate(model, X, y, g, args.n_perm, rng)
        results[tname] = res
        print(f"{tname}: n={len(d)} pos={y.sum()} | " + " | ".join(
            f"{m}: bAcc={r['balanced_accuracy']} AUC={r['roc_auc']} (perm p={r['perm_p_value']})"
            for m, r in res["models"].items()))

        # SHAP explanation of the RF fitted on all rows of this task (descriptive, not a test result)
        try:
            import shap
            rf = clone(MODELS["rf"]).fit(X, y)
            Xi = rf[0].transform(X)
            sv = shap.TreeExplainer(rf[-1]).shap_values(Xi)
            sv = sv[1] if isinstance(sv, list) else (sv[..., 1] if sv.ndim == 3 else sv)
            imp = pd.Series(np.abs(sv).mean(axis=0), index=feats).sort_values()
            fig, ax = plt.subplots(figsize=(5, 0.3 * len(feats) + 1))
            imp.plot.barh(ax=ax, color="#4C72B0")
            ax.set_xlabel("mean |SHAP value| (impact on P(positive))")
            ax.set_title(desc, fontsize=8)
            fig.savefig(out / f"shap_{tname}{suffix}.png", dpi=120, bbox_inches="tight")
            plt.close(fig)
            res["shap_mean_abs_top5"] = {k: round(float(v), 4) for k, v in imp[::-1].head(5).items()}
        except Exception as e:  # noqa: BLE001
            res["shap_error"] = str(e)

    (out / f"metrics_classify{suffix}.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
