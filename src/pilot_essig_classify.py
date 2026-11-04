"""Pilot (Essig IFC, exp1): classical ML on hand-crafted features, leave-one-donor-out.

Tasks
  T1  +SEA vs -SEA (superantigen activation), binary, ROC AUC
  T2  4 conditions (+SEA, -SEA, Isotype, Teplizumab), balanced accuracy / macro F1
  T3  dead vs live, label from Live-Dead channel (Otsu threshold on log intensity),
      predicted from BRIGHTFIELD features only (label-free viability)
Feature sets: BF (brightfield only, label-free) vs ALL (all 8 channels).

Usage: python -m src.pilot_essig_classify [--csv results/pilot-essig/features.csv]
"""
from __future__ import annotations

import argparse
import json
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from skimage.filters import threshold_otsu
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42


def models():
    return {
        "LogReg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=0.1)),
        "RF": RandomForestClassifier(n_estimators=300, min_samples_leaf=3, n_jobs=-1, random_state=SEED,
                                     class_weight="balanced"),
    }


def lodo(X: pd.DataFrame, y: np.ndarray, donors: np.ndarray, binary: bool, n_perm: int = 0) -> dict:
    """Leave-one-donor-out; returns per-model mean metric, per-fold metrics, and RF permutation importance."""
    out = {}
    for name, mdl in models().items():
        folds, imps = [], []
        for d in np.unique(donors):
            tr, te = donors != d, donors == d
            mdl.fit(X[tr], y[tr])
            if binary:
                s = roc_auc_score(y[te], mdl.predict_proba(X[te])[:, 1])
                folds.append({"test_donor": d, "auc": round(float(s), 3)})
            else:
                p = mdl.predict(X[te])
                folds.append({"test_donor": d, "bal_acc": round(float(balanced_accuracy_score(y[te], p)), 3),
                              "f1_macro": round(float(f1_score(y[te], p, average="macro")), 3)})
            if name == "RF":
                sub = np.where(te)[0][:2000]
                pi = permutation_importance(mdl, X.iloc[sub], y[sub], n_repeats=5, random_state=SEED, n_jobs=-1,
                                            scoring="roc_auc" if binary else "balanced_accuracy")
                imps.append(pi.importances_mean)
        key = "auc" if binary else "bal_acc"
        res = {"mean_" + key: round(float(np.mean([f[key] for f in folds])), 3), "folds": folds}
        if not binary:
            res["mean_f1_macro"] = round(float(np.mean([f["f1_macro"] for f in folds])), 3)
        if name == "LogReg" and n_perm:
            rng = np.random.default_rng(SEED)
            null = []
            for _ in range(n_perm):
                yp = y.copy()
                for d in np.unique(donors):  # shuffle within donor
                    idx = np.where(donors == d)[0]
                    yp[idx] = rng.permutation(yp[idx])
                ss = []
                for d in np.unique(donors):
                    tr, te = donors != d, donors == d
                    mdl.fit(X[tr], yp[tr])
                    ss.append(roc_auc_score(yp[te], mdl.predict_proba(X[te])[:, 1]) if binary
                              else balanced_accuracy_score(yp[te], mdl.predict(X[te])))
                null.append(np.mean(ss))
            res["perm_p"] = round(float((1 + np.sum(np.array(null) >= res["mean_" + key])) / (1 + n_perm)), 3)
            res["perm_null_mean"] = round(float(np.mean(null)), 3)
        if imps:
            imp = pd.Series(np.mean(imps, axis=0), index=X.columns).sort_values(ascending=False)
            res["top_features"] = {k: round(float(v), 4) for k, v in imp.head(10).items()}
        out[name] = res
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="results/pilot-essig/features.csv")
    ap.add_argument("--n-perm", type=int, default=20)
    a = ap.parse_args()
    df = pd.read_csv(a.csv)
    meta = ["file", "donor", "condition", "expert_label"]
    feats = [c for c in df.columns if c not in meta]
    bf = [c for c in feats if c.startswith("BF_") or c in ("img_h", "img_w")]
    sets = {"BF": bf, "ALL": feats}
    donors = df["donor"].to_numpy()
    res = {"n_cells": int(len(df)), "n_features": {k: len(v) for k, v in sets.items()},
           "cells_per_group": df.groupby(["donor", "condition"]).size().astype(int).to_dict().__repr__(),
           "versions": {p: version(p) for p in ["scikit-learn", "numpy", "scikit-image", "pandas"]}}

    # T1: +SEA vs -SEA
    m = df["condition"].isin(["+SEA", "-SEA"]).to_numpy()
    y1 = (df.loc[m, "condition"] == "+SEA").astype(int).to_numpy()
    res["T1_SEA"] = {s: lodo(df.loc[m, c].reset_index(drop=True), y1, donors[m], True, a.n_perm) for s, c in sets.items()}
    print("T1 done", flush=True)

    # T2: 4 conditions
    y2 = df["condition"].astype("category").cat.codes.to_numpy()
    res["T2_4cond"] = {s: lodo(df[c], y2, donors, False) for s, c in sets.items()}
    res["T2_classes"] = list(df["condition"].astype("category").cat.categories)
    print("T2 done", flush=True)

    # T3: dead vs live from brightfield only; label = Otsu on log Live-Dead mean intensity (bg-subtracted)
    ld = np.log1p(np.clip(df["Live-Dead_mean"].to_numpy(), 0, None))
    thr = float(threshold_otsu(ld))
    y3 = (ld > thr).astype(int)
    res["T3_dead_from_BF"] = {
        "label_rule": f"dead = log1p(Live-Dead_mean) > Otsu threshold {thr:.3f}",
        "dead_fraction_per_condition": df.assign(dead=y3).groupby(["donor", "condition"])["dead"].mean().round(3)
        .to_dict().__repr__(),
        "dead_fraction_total": round(float(y3.mean()), 3),
        "BF": lodo(df[bf], y3, donors, True, a.n_perm),
    }
    print("T3 done", flush=True)

    out = Path(a.csv).with_name("metrics_classify.json")
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
