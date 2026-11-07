"""Pilot: Illinois Data Bank IDB-8103861 (Lu et al., PNAS 2021) - Jurkat T cells with a minimal HIV gene circuit (GFP reporter).

Input (read straight from the zip archives, nothing unpacked):
    intensityTrajectories.zip / noiseTrajectories.zip : <Plate>/Well<XNN>.csv, one row per cell, 72 columns = 15-min frames
                                                         (hours 1-19), values from the authors' NIS Elements image analysis.
Control wells on every plate (README): column 1 = TNF-alpha (activates HIV LTR), columns 2 and 23 = untreated,
column 24 = alsterpaullone (Alp, suppresses). Compound wells (3-22) are not used here.

Per-cell features (physical/statistical descriptors of the expression time series):
    I_mean, I_std, I_cv (=std/mean), I_slope (per hour, linear fit), I_start / I_end (mean of first / last 4 frames),
    I_fold (=end/start), I_resid_std (std after linear detrending), I_ac1 (lag-1 autocorrelation of the residual),
    N_mean (authors' noise trajectory mean), N_rel (=N_mean / I_mean), N_slope.

Tasks: TNF vs untreated (activation), Alp vs untreated (suppression).
Validation (WO-14 protocol, models from src.wo14_kfold_heidata): outer k-fold 5 per cell vs grouped per WELL (5 folds)
vs leave-one-PLATE-out; inner 3-fold GridSearch. Cells are capped per well to keep the laptop run short.

Usage: python src/pilot_illinois.py --root data/raw/illinois-IDB-8103861 --cap 20
"""
import argparse
import io
import json
import re
import sys
import warnings
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut, StratifiedGroupKFold, StratifiedKFold

from src.wo14_kfold_heidata import models, run

SEED = 42
FRAME_H = 0.25
CONTROL = {1: "TNF", 2: "untreated", 23: "untreated", 24: "Alp"}
FEATS_ALL = ["I_mean", "I_std", "I_cv", "I_slope", "I_start", "I_end", "I_fold", "I_resid_std", "I_ac1",
             "N_mean", "N_rel", "N_slope", "N_std"]
# The authors' noise trajectory is the DOUBLE-CENTRED intensity (cell mean and the well-mean of every frame subtracted;
# checked 8 Nov 2026: max |N - doublecentred(I)| = 0). N features therefore carry the WELL-average trajectory
# (e.g. I_slope - N_slope = well-mean slope) -> well-level information leaks into a "per-cell" feature.
# Main feature set = cell-own intensity descriptors only; N_std kept as a separate, flagged variant.
FEATS = ["I_mean", "I_std", "I_cv", "I_slope", "I_start", "I_end", "I_fold", "I_resid_std", "I_ac1"]
FEATS_N = FEATS + ["N_std"]


def features(I: np.ndarray, N: np.ndarray) -> pd.DataFrame:
    t = np.arange(I.shape[1]) * FRAME_H
    mean = np.nanmean(I, 1)
    slope, icpt = np.polyfit(t, np.nan_to_num(I.T, nan=np.nanmean(I)), 1)
    resid = I - (slope[:, None] * t + icpt[:, None])
    r0, r1 = resid[:, :-1], resid[:, 1:]
    ac1 = np.nansum((r0 - np.nanmean(r0, 1, keepdims=True)) * (r1 - np.nanmean(r1, 1, keepdims=True)), 1) / \
        (np.nanstd(r0, 1) * np.nanstd(r1, 1) * r0.shape[1] + 1e-9)
    start, end = np.nanmean(I[:, :4], 1), np.nanmean(I[:, -4:], 1)
    nslope = np.polyfit(t, np.nan_to_num(N.T, nan=np.nanmean(N)), 1)[0]
    return pd.DataFrame({
        "I_mean": mean, "I_std": np.nanstd(I, 1), "I_cv": np.nanstd(I, 1) / mean, "I_slope": slope,
        "I_start": start, "I_end": end, "I_fold": end / start, "I_resid_std": np.nanstd(resid, 1), "I_ac1": ac1,
        "N_mean": np.nanmean(N, 1), "N_rel": np.nanmean(N, 1) / mean, "N_slope": nslope, "N_std": np.nanstd(N, 1)})


def load(root: Path, cap: int) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    zi, zn = zipfile.ZipFile(root / "intensityTrajectories.zip"), zipfile.ZipFile(root / "noiseTrajectories.zip")
    noise_names = set(zn.namelist())
    rows = []
    for name in zi.namelist():
        m = re.match(r"(.+)/Well([A-P])(\d\d)\.csv$", name)
        if not m or int(m.group(3)) not in CONTROL or name not in noise_names:
            continue
        I = pd.read_csv(io.BytesIO(zi.read(name)), header=None).to_numpy(float)
        N = pd.read_csv(io.BytesIO(zn.read(name)), header=None).to_numpy(float)
        if I.shape != N.shape or len(I) == 0:
            continue
        idx = rng.permutation(len(I))[:cap]
        f = features(I[idx], N[idx])
        f["plate"], f["well"] = m.group(1), f"{m.group(1)}/{m.group(2)}{m.group(3)}"
        f["column"], f["condition"] = int(m.group(3)), CONTROL[int(m.group(3))]
        f["n_cells_in_well"] = len(I)
        rows.append(f)
    return pd.concat(rows, ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/raw/illinois-IDB-8103861")
    ap.add_argument("--out", default="results/pilot-illinois")
    ap.add_argument("--cap", type=int, default=20, help="max cells per well")
    a = ap.parse_args()
    warnings.filterwarnings("ignore")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    df = load(Path(a.root), a.cap)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.to_csv(out / "cells_controls.csv", index=False)
    wells = df.drop_duplicates("well")
    info = {"cells_used": df.groupby("condition").size().to_dict(),
            "wells": wells.groupby("condition").size().to_dict(),
            "median_cells_per_well": wells.groupby("condition").n_cells_in_well.median().to_dict(),
            "plates": sorted(df.plate.unique()), "cap_per_well": a.cap}
    print(json.dumps(info, indent=1))
    desc = df.groupby("condition")[FEATS_ALL].median().T.round(3)
    desc.to_csv(out / "feature_medians.csv")
    print(desc.to_string())

    from sklearn.metrics import roc_auc_score
    uni = {}
    for pos in ["TNF", "Alp"]:
        s = df[df.condition.isin([pos, "untreated"])]
        uni[f"{pos}_vs_untreated"] = {f: round(roc_auc_score(s.condition == pos, s[f].fillna(0)), 3) for f in FEATS_ALL}
    info["univariate_auc"] = uni

    res, rows = {"info": info, "tasks": {}}, []
    jobs = [("TNF_vs_untreated", "TNF", "untreated", "sel", FEATS), ("Alp_vs_untreated", "Alp", "untreated", "sel", FEATS),
            ("TNF_vs_untreated", "TNF", "untreated", "sel+N_std", FEATS_N),
            ("Alp_vs_untreated", "Alp", "untreated", "sel+N_std", FEATS_N),
            ("TNF_vs_untreated", "TNF", "untreated", "BOCOR_semua_N", FEATS_ALL)]
    for task0, pos, neg, fset, feats in jobs:
        task = f"{task0}|{fset}"
        d = df[df.condition.isin([pos, neg])].reset_index(drop=True)
        X, y = d[feats].to_numpy(float), (d.condition == pos).astype(int).to_numpy()
        schemes = {
            "kfold5_per_sel": list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y)),
            "group5_per_sumur": list(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(X, y, d.well)),
            "leave_one_plate_out": list(LeaveOneGroupOut().split(X, y, d.plate)),
        }
        res["tasks"][task] = {}
        for sch, splits in schemes.items():
            res["tasks"][task][sch] = {}
            for mname, (model, grid) in models().items():
                r = run(model, grid, X, y, splits)
                res["tasks"][task][sch][mname] = r
                rows.append({"task": task, "scheme": sch, "model": mname, "auc_mean": r["roc_auc"]["mean"],
                             "auc_sd": r["roc_auc"]["sd"], "bacc_mean": r["balanced_accuracy"]["mean"],
                             "f1_mean": r["f1"]["mean"]})
                print(task, sch, mname, r["roc_auc"], flush=True)
    (out / "metrics.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    pd.DataFrame(rows).to_csv(out / "summary.csv", index=False)


if __name__ == "__main__":
    main()
