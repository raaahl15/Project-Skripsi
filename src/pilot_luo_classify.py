"""Pilot (feasibility) for the CyTOF component (Luo et al.): per-cell HIV infection & apoptosis in tonsil CD4 T cells.

Gating (arcsinh, cofactor 5):  CD4 T cells = CD3 > 3 and CD8 < 2   (CD8- instead of CD4+ because HIV down-regulates CD4)
Per-cell states (thresholds from the uninfected cultures, see README of results):
    HIV+        : HIV > 2.0      (uninfected cultures: 99.9th percentile 1.2-1.6 for every donor)
    apoptotic   : Casp3_cleaved > its 99th percentile in uninfected cultures, and HIV-
Task L1: HIV+ vs HIV- CD4 T cells in infected cultures, from surface markers only (HIV/p24 and state markers excluded).
         Variant "noCD4" also drops CD4 (its down-regulation is a direct consequence of infection).
Validation: leave-one-DONOR-out. Metrics: ROC AUC, average precision (PR AUC), balanced accuracy.

Usage:
    python src/pilot_luo_classify.py --root data/raw/dryad-luo-2023 --out results/pilot-luo
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
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.data.luo_cytof import NON_MARKERS, arcsinh, load_all

SEED = 42
HIV_POS = 2.0
STATE_MARKERS = {"HIV", "KC57_p24", "Casp3_cleaved", "LiveDead", "CD95", "BST2", "SAMHD1", "SAMHD1_P", "IFI16"}
MODELS = {
    "logreg": make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=3000)),
    "hgb": HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08, class_weight="balanced",
                                          random_state=SEED),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/raw/dryad-luo-2023")
    ap.add_argument("--out", default="results/pilot-luo")
    ap.add_argument("--max-events", type=int, default=40000, help="subsample per FCS file (speed)")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = load_all(Path(args.root), max_events_per_file=args.max_events, seed=SEED)
    meta = ["donor", "culture", "infected_culture", "file"]
    marker_cols = [c for c in df.columns if c not in meta and c not in NON_MARKERS]
    common = [c for c in marker_cols if df[c].notna().all()]
    df = arcsinh(df, common)

    cd4t = df[(df.CD3 > 3) & (df.CD8 < 2)].copy()
    unf = cd4t[cd4t.infected_culture == 0]
    casp_thr = float(unf["Casp3_cleaved"].quantile(0.99))
    cd4t["hiv_pos"] = (cd4t.HIV > HIV_POS).astype(int)
    cd4t["apoptotic"] = ((cd4t.Casp3_cleaved > casp_thr) & (cd4t.hiv_pos == 0)).astype(int)

    # --- descriptive counts per donor/culture (feasibility of a healthy / infected / apoptotic scheme)
    counts = (cd4t.assign(state=np.select([cd4t.hiv_pos == 1, cd4t.apoptotic == 1], ["infected_HIV+", "apoptotic_Casp3+"],
                                          "other_HIV-Casp3-"))
              .groupby(["donor", "infected_culture", "state"]).size().unstack(fill_value=0))
    counts.to_csv(out / "state_counts.csv")
    print(f"CD4 T cells (CD3>3, CD8<2): {len(cd4t):,} | Casp3 threshold (99th pct uninfected) = {casp_thr:.2f}")
    print(counts.to_string())

    # --- L1 classification: HIV+ vs HIV- within infected cultures
    inf = cd4t[cd4t.infected_culture == 1]
    feats_all = [c for c in common if c not in STATE_MARKERS]
    variants = {"withCD4": feats_all, "noCD4": [c for c in feats_all if c != "CD4"]}
    results = {"n_cd4t_cells_subsampled": int(len(cd4t)), "hiv_pos_threshold": HIV_POS,
               "casp3_threshold": round(casp_thr, 3), "n_infected_culture_cells": int(len(inf)),
               "n_hiv_pos": int(inf.hiv_pos.sum()), "features": variants, "tasks": {}}
    y, g = inf.hiv_pos.to_numpy(), inf.donor.to_numpy()
    for vname, feats in variants.items():
        X = inf[feats].to_numpy(np.float32)
        for mname, model in MODELS.items():
            proba = np.zeros(len(y))
            per_donor = {}
            for tr, te in LeaveOneGroupOut().split(X, y, g):
                m = clone(model).fit(X[tr], y[tr])
                proba[te] = m.predict_proba(X[te])[:, 1]
                if y[te].min() != y[te].max():
                    per_donor[str(g[te][0])] = round(roc_auc_score(y[te], proba[te]), 3)
            r = {"roc_auc": round(roc_auc_score(y, proba), 3),
                 "pr_auc": round(average_precision_score(y, proba), 3),
                 "pr_auc_chance": round(float(y.mean()), 4),
                 "balanced_accuracy": round(balanced_accuracy_score(y, proba >= 0.5), 3),
                 "roc_auc_per_held_out_donor": per_donor}
            results["tasks"][f"L1_{vname}_{mname}"] = r
            print(f"L1 {vname:8s} {mname:6s} AUC={r['roc_auc']} PR-AUC={r['pr_auc']} (chance {r['pr_auc_chance']}) "
                  f"bAcc={r['balanced_accuracy']} per-donor AUC={per_donor}")

        # SHAP (descriptive) on the gradient-boosting model fitted on all infected-culture cells
        try:
            import shap
            m = clone(MODELS["hgb"]).fit(X, y)
            idx = np.random.default_rng(SEED).choice(len(X), size=min(3000, len(X)), replace=False)
            sv = shap.TreeExplainer(m).shap_values(X[idx])
            sv = sv[1] if isinstance(sv, list) else sv
            imp = pd.Series(np.abs(sv).mean(axis=0), index=feats).sort_values()
            fig, ax = plt.subplots(figsize=(5, 0.25 * len(feats) + 1))
            imp.plot.barh(ax=ax, color="#C44E52")
            ax.set_xlabel("mean |SHAP value| (log-odds of HIV+)")
            ax.set_title(f"HIV+ vs HIV- CD4 T cells ({vname})", fontsize=9)
            fig.savefig(out / f"shap_L1_{vname}.png", dpi=120, bbox_inches="tight")
            plt.close(fig)
            results[f"shap_top8_{vname}"] = {k: round(float(v), 4) for k, v in imp[::-1].head(8).items()}
        except Exception as e:  # noqa: BLE001
            results[f"shap_error_{vname}"] = str(e)

    (out / "metrics_classify.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
