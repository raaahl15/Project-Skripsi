"""WO-14: k-fold cross-validation for the heiDATA per-cell features (arahan Bimbingan 5).

Data split per outer fold:
    training   -> model fitting; inside it an inner 3-fold CV (= validation) picks the hyperparameters
    testing    -> the outer held-out fold, never seen during fitting or tuning

Two outer schemes are compared:
    kfold5 / kfold10  StratifiedKFold on CELLS (as asked in B5). Cells of the same field/experiment can end up in
                      both training and testing, so the score can include batch (experiment) recognition.
    group             StratifiedGroupKFold on FIGURES (experiments): an experiment is either fully in training or
                      fully in testing. This measures generalization to a new experiment.
The gap between the two schemes estimates how much of the cell-level score is batch leakage.

Usage:
    python src/wo14_kfold_heidata.py --cells results/pilot-heidata/cells.csv --out results/wo14-kfold
"""
import argparse
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.pilot_heidata_classify import CA_FEATS, LAMIN_FEATS

SEED = 42
TASKS = {
    "T2_hiv_vs_mock": (lambda d: d.index == d.index, lambda d: d.condition != "Mock", LAMIN_FEATS,
                       "Terpapar HIV (+/-Vpx) vs Mock - Lamin B1 (arah B5: terinfeksi vs tidak)"),
    "T1a_vpx_lamin": (lambda d: d.condition.isin(["+Vpx", "-Vpx"]), lambda d: d.condition == "+Vpx",
                      LAMIN_FEATS, "+Vpx vs -Vpx - Lamin B1"),
    "T1b_vpx_lamin_ca": (lambda d: d.condition.isin(["+Vpx", "-Vpx"]) & d.ca_puncta_nucleus.notna(),
                         lambda d: d.condition == "+Vpx", LAMIN_FEATS + CA_FEATS,
                         "+Vpx vs -Vpx - Lamin B1 + kapsid HIV-1"),
}


def models():
    imp = ("imp", SimpleImputer(strategy="median"))
    return {
        "logreg": (Pipeline([imp, ("sc", StandardScaler()),
                             ("clf", LogisticRegression(class_weight="balanced", max_iter=5000))]),
                   {"clf__C": [0.01, 0.1, 1, 10]}),
        "rf": (Pipeline([imp, ("clf", RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                                             random_state=SEED, n_jobs=-1))]),
               {"clf__max_depth": [None, 5], "clf__min_samples_leaf": [1, 3, 5]}),
        "svm": (Pipeline([imp, ("sc", StandardScaler()), ("clf", SVC(kernel="rbf", class_weight="balanced"))]),
                {"clf__C": [0.1, 1, 10], "clf__gamma": ["scale", 0.01, 0.1]}),
    }


def outer_splits(scheme, X, y, groups):
    if scheme == "group":
        n = min(5, len(set(groups)))
        return list(StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=SEED).split(X, y, groups)), n
    k = int(scheme.replace("kfold", ""))
    return list(StratifiedKFold(n_splits=k, shuffle=True, random_state=SEED).split(X, y)), k


def run(model, grid, X, y, splits):
    folds, oof = [], np.full(len(y), np.nan)
    for tr, te in splits:
        search = GridSearchCV(model, grid, scoring="roc_auc",
                              cv=StratifiedKFold(3, shuffle=True, random_state=SEED), error_score=np.nan)
        search.fit(X[tr], y[tr])
        score = search.decision_function(X[te]) if hasattr(search, "decision_function") else \
            search.predict_proba(X[te])[:, 1]
        pred = search.predict(X[te])
        oof[te] = score
        both = len(set(y[te])) == 2
        folds.append({"n_test": int(len(te)), "n_test_pos": int(y[te].sum()),
                      "roc_auc": round(roc_auc_score(y[te], score), 3) if both else None,
                      "balanced_accuracy": round(balanced_accuracy_score(y[te], pred), 3) if both else None,
                      "f1": round(f1_score(y[te], pred, zero_division=0), 3),
                      "best_params": search.best_params_})
    def ms(key):
        v = [f[key] for f in folds if f[key] is not None]
        return {"mean": round(float(np.mean(v)), 3), "sd": round(float(np.std(v, ddof=1)), 3) if len(v) > 1 else None,
                "n_folds_scored": len(v)} if v else None
    return {"roc_auc": ms("roc_auc"), "balanced_accuracy": ms("balanced_accuracy"), "f1": ms("f1"),
            "pooled_oof_roc_auc": round(roc_auc_score(y, oof), 3), "folds": folds}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default="results/pilot-heidata/cells.csv")
    ap.add_argument("--out", default="results/wo14-kfold")
    args = ap.parse_args()
    warnings.filterwarnings("ignore")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.cells)

    results = {"sklearn": sklearn.__version__, "seed": SEED,
               "inner_validation": "GridSearchCV, StratifiedKFold(3) inside each outer training set",
               "tasks": {}}
    rows = []
    for tname, (rsel, pos, feats, desc) in TASKS.items():
        d = df[rsel(df)]
        X, y, g = d[feats].to_numpy(float), pos(d).astype(int).to_numpy(), d.figure.to_numpy()
        tres = {"description": desc, "n_cells": int(len(d)), "n_positive": int(y.sum()),
                "figures": sorted(set(g)), "schemes": {}}
        for scheme in ["kfold5", "kfold10", "group"]:
            splits, k = outer_splits(scheme, X, y, g)
            tres["schemes"][scheme] = {"k": k, "models": {}}
            for mname, (model, grid) in models().items():
                r = run(model, grid, X, y, splits)
                tres["schemes"][scheme]["models"][mname] = r
                auc = r["roc_auc"]
                rows.append({"task": tname, "scheme": f"{scheme} (k={k})", "model": mname,
                             "auc_mean": auc and auc["mean"], "auc_sd": auc and auc["sd"],
                             "bacc_mean": r["balanced_accuracy"] and r["balanced_accuracy"]["mean"],
                             "f1_mean": r["f1"] and r["f1"]["mean"],
                             "pooled_oof_auc": r["pooled_oof_roc_auc"]})
                print(f"{tname:18s} {scheme:8s} {mname:6s} AUC={auc} pooled={r['pooled_oof_roc_auc']}")
        results["tasks"][tname] = tres

    (out / "metrics_kfold.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    summary = pd.DataFrame(rows)
    summary.to_csv(out / "summary_kfold.csv", index=False)

    fig, axes = plt.subplots(1, len(TASKS), figsize=(5 * len(TASKS), 4), sharey=True)
    for ax, tname in zip(axes, TASKS):
        s = summary[summary.task == tname].pivot(index="model", columns="scheme", values="auc_mean")
        s.plot.bar(ax=ax, rot=0)
        ax.axhline(0.5, color="grey", ls="--", lw=1)
        ax.set_title(tname, fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_ylabel("ROC AUC (rata-rata fold)")
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "kfold_auc.png", dpi=130)


if __name__ == "__main__":
    main()
