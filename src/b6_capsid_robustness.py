"""Robustness of the heiDATA HIV-exposed vs Mock result (capsid puncta) to the detector settings.

Re-detects HIV-1 CA puncta in figures 1G and S3B with varied settings, recounts puncta per nucleus (nuclear labels
from results/pilot-heidata/labels, unchanged), and re-evaluates:
    - leave-one-figure-out LogReg (C=1, standardised; train on one experiment, test on the other): AUC per fold
    - no-training rule "exposed if >= 1 nuclear punctum": balanced accuracy per figure
Varied (one at a time around the baseline, plus a threshold x max_sigma grid):
    threshold  : LoG threshold (baseline 0.08)
    max_sigma  : largest LoG scale in px (baseline 3)
    ring_um    : perinuclear ring width (baseline 1.5 um)
    high_pct   : upper percentile of the shared per-figure scale (baseline 99.95; lower = less dominated by saturation)
Baseline also gets a bootstrap 95% CI (cells resampled within each test figure, 1000x).

Usage: python src/b6_capsid_robustness.py
"""
import itertools
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from skimage import feature, morphology
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.data.heidata import FIELDS, PIXEL_SIZE_UM, field_id, load_stack, max_projection
from src.data.heidata_cells import shared_scale

ROOT = Path("data/raw/heidata-MUXYRY")
LAB = Path("results/pilot-heidata/labels")
OUT = Path("results/b6")
FIGS = ["1G", "S3B"]
BASE = {"threshold": 0.08, "max_sigma": 3, "ring_um": 1.5, "high_pct": 99.95}


def puncta(img01, threshold, max_sigma):
    b = feature.blob_log(img01, min_sigma=1, max_sigma=max_sigma, num_sigma=5, threshold=threshold)
    return b[:, :2] if len(b) else np.zeros((0, 2))


def count(lab, coords, ring_um):
    ring_px = max(1, int(round(ring_um / PIXEL_SIZE_UM)))
    rc = np.clip(np.round(coords).astype(int), 0, np.array(lab.shape) - 1) if len(coords) else np.zeros((0, 2), int)
    hit = lab[rc[:, 0], rc[:, 1]] if len(rc) else np.zeros(0, int)
    rows = []
    for lb in np.unique(lab)[1:]:
        m = lab == lb
        ring = morphology.binary_dilation(m, morphology.disk(ring_px)) & ~m & (lab == 0)
        near = ring[rc[:, 0], rc[:, 1]].sum() if len(rc) else 0
        rows.append({"label": int(lb), "nuc": int((hit == lb).sum()), "peri": int(near)})
    return rows


def evaluate(d):
    y = (d.condition != "Mock").astype(int).to_numpy(); g = d.figure.to_numpy(); X = d[["nuc", "peri"]].to_numpy(float)
    out = {}
    for test in FIGS:
        tr, te = g != test, g == test
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000)).fit(X[tr], y[tr])
        out[f"auc_test_{test}"] = round(roc_auc_score(y[te], m.predict_proba(X[te])[:, 1]), 3)
        out[f"rule_bacc_{test}"] = round(balanced_accuracy_score(y[te], (X[te, 0] >= 1).astype(int)), 3)
    out["auc_mean"] = round((out["auc_test_1G"] + out["auc_test_S3B"]) / 2, 3)
    out["mock_cells_with_puncta"] = int(((d.condition == "Mock") & (d.nuc >= 1)).sum())
    out["exposed_zero_nuc_frac"] = round(float(((d.condition != "Mock") & (d.nuc == 0)).sum() / (d.condition != "Mock").sum()), 3)
    return out


def bootstrap(d, n=1000, seed=42):
    rng = np.random.default_rng(seed)
    y = (d.condition != "Mock").astype(int).to_numpy(); g = d.figure.to_numpy(); X = d[["nuc", "peri"]].to_numpy(float)
    res = {}
    for test in FIGS:
        tr, te = np.where(g != test)[0], np.where(g == test)[0]
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000)).fit(X[tr], y[tr])
        s, yt = m.predict_proba(X[te])[:, 1], y[te]
        aucs = []
        for _ in range(n):
            i = rng.integers(0, len(te), len(te))
            if len(np.unique(yt[i])) == 2:
                aucs.append(roc_auc_score(yt[i], s[i]))
        res[f"auc_test_{test}_ci95"] = np.percentile(aucs, [2.5, 97.5]).round(3).tolist()
    return res


def main():
    warnings.filterwarnings("ignore")
    fields = [f for f in FIELDS if f.figure in FIGS and "ca" in f.channels]
    mips = {field_id(f): max_projection(load_stack(ROOT, f), f.channels["ca"]) for f in fields}
    labs = {field_id(f): np.load(LAB / f"{field_id(f)}.npy") for f in fields}

    settings = []
    for k, vals in {"threshold": [0.03, 0.04, 0.06, 0.08, 0.10, 0.12, 0.16, 0.20], "max_sigma": [2, 3, 4, 5],
                    "ring_um": [0.75, 1.5, 2.5, 3.5], "high_pct": [99.5, 99.9, 99.95, 99.99]}.items():
        settings += [{**BASE, k: v, "varied": k} for v in vals]
    settings += [{**BASE, "threshold": t, "max_sigma": s, "varied": "threshold x max_sigma"}
                 for t, s in itertools.product([0.04, 0.08, 0.12, 0.16], [2, 4])]

    rows, cache = [], {}
    for st in settings:
        scales = {fig: shared_scale([mips[field_id(f)] for f in fields if f.figure == fig], 1.0, st["high_pct"]) for fig in FIGS}
        cells = []
        for f in fields:
            fid = field_id(f); lo, hi = scales[f.figure]
            key = (fid, st["threshold"], st["max_sigma"], st["high_pct"])
            if key not in cache:
                img = np.clip((mips[fid].astype(np.float32) - lo) / max(hi - lo, 1e-6), 0, 1)
                cache[key] = puncta(img, st["threshold"], st["max_sigma"])
            for r in count(labs[fid], cache[key], st["ring_um"]):
                cells.append({**r, "field": fid, "figure": f.figure, "condition": f.condition})
        d = pd.DataFrame(cells)
        r = {**st, "n_cells": len(d), **evaluate(d)}
        if st == {**BASE, "varied": "threshold"} and not any(x.get("ci") for x in rows):
            r.update(bootstrap(d)); r["ci"] = True
        rows.append(r)
        print({k: r[k] for k in r if k not in ("ci",)}, flush=True)
    df = pd.DataFrame(rows).drop(columns="ci", errors="ignore")
    df.to_csv(OUT / "A_capsid_robustness.csv", index=False)
    summ = {"n_settings": len(df), "auc_mean_min": float(df.auc_mean.min()), "auc_mean_max": float(df.auc_mean.max()),
            "auc_mean_median": float(df.auc_mean.median()),
            "rule_bacc_S3B_range": [float(df.rule_bacc_S3B.min()), float(df.rule_bacc_S3B.max())],
            "rule_bacc_1G_range": [float(df.rule_bacc_1G.min()), float(df.rule_bacc_1G.max())],
            "mock_cells_with_puncta_max": int(df.mock_cells_with_puncta.max()),
            "baseline": rows[[i for i, x in enumerate(rows) if x.get("ci")][0]]}
    (OUT / "A_capsid_robustness.json").write_text(json.dumps(summ, indent=1, default=str), encoding="utf-8")
    print(json.dumps(summ, indent=1, default=str))


if __name__ == "__main__":
    main()
