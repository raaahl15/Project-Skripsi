"""Essig IFC (exp1, expert labels): live T cell vs Dead_Cell from brightfield - extra validation for B6.

1. Permutation test : labels shuffled WITHIN each donor, leave-one-donor-out LogReg (C=1), 200 permutations.
2. Bootstrap CI     : 95% CI of the AUC on each held-out donor (cells resampled, 1000x), LogReg C=1 and RF.
3. Robustness       : (a) BF mask eroded 1 px / dilated 1-2 px, (b) OWN brightfield mask (gradient magnitude + Otsu,
                      no dataset mask), (c) feature groups removed (shape / intensity / texture / gradient).
                      Each variant: WO-14 protocol (LogReg/RF/SVM, inner 3-fold GridSearch), leave-one-donor-out.
4. Visual check     : gallery of live / dead / misclassified cells (BF + mask contour); expert label vs the
                      Live-Dead stain channel (AUC of the stain intensity alone).

Usage: python -I src/b6_essig_validation.py --zip C:/Users/.../exp1.zip
"""
import argparse
import io
import json
import sys
import time
import warnings
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage.filters import threshold_otsu
from skimage.measure import label as cc_label
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.pilot_essig_features import intensity_feats, shape_feats, texture_feats
from src.wo14_kfold_heidata import models, run

SEED = 42
OUT = Path("results/b6")
LIVE, DEAD = ["T_cell", "T_cell_with_signaling"], ["Dead_Cell"]
GROUPS = {"shape": ["n_obj", "area", "perimeter", "eccentricity", "solidity", "circularity", "major_axis", "minor_axis"],
          "intensity": ["mean", "std", "max", "sum", "p90", "rim_inner_ratio"],
          "texture": ["glcm_contrast", "glcm_homogeneity", "glcm_energy", "glcm_correlation"],
          "gradient": ["gradient_rms"]}


def own_mask(bf):
    g = ndi.gaussian_gradient_magnitude(bf.astype(np.float32), 1.0)
    m = ndi.binary_fill_holes(ndi.binary_closing(g > threshold_otsu(g), iterations=2))
    lab = cc_label(m)
    if lab.max() == 0:
        return m
    return lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)


def bf_features(img, mask, m0):
    bf = img[..., 0].astype(np.float32)
    union = (mask > 0).any(-1)
    bg = float(np.median(bf[~union])) if (~union).any() else 0.0
    f = {}
    f.update(shape_feats(m0, "BF")); f.update(intensity_feats(bf, m0, bg, "BF")); f.update(texture_feats(bf, m0, "BF"))
    gy, gx = np.gradient(bf)
    f["BF_gradient_rms"] = float(np.sqrt((gx[m0] ** 2 + gy[m0] ** 2).mean())) if m0.any() else 0.0
    return f


def recompute(zip_path, files):
    variants = {"erode1": lambda m: ndi.binary_erosion(m, iterations=1), "dilate1": lambda m: ndi.binary_dilation(m, iterations=1),
                "dilate2": lambda m: ndi.binary_dilation(m, iterations=2)}
    rows = {k: [] for k in list(variants) + ["own_mask"]}
    imgs = {}
    z = zipfile.ZipFile(zip_path); t0 = time.time()
    for i, n in enumerate(files):
        with z.open(n) as fh, h5py.File(io.BytesIO(fh.read()), "r") as h:
            img, mask = h["image"][()], h["mask"][()]
        m0 = mask[..., 0] > 0
        for k, fn in variants.items():
            rows[k].append(bf_features(img, mask, fn(m0)))
        om = own_mask(img[..., 0])
        rows["own_mask"].append({**bf_features(img, mask, om), "own_vs_dataset_iou": float((om & m0).sum() / max((om | m0).sum(), 1))})
        imgs[n] = (img[..., 0], m0, img[..., 7] if img.shape[-1] > 7 else None)
        if i % 200 == 0:
            print(f"recompute {i}/{len(files)} {time.time()-t0:.0f}s", flush=True)
    return {k: pd.DataFrame(v) for k, v in rows.items()}, imgs


def lodo_eval(X, y, donors):
    splits = list(LeaveOneGroupOut().split(X, y, donors))
    out = {}
    for mname, (model, grid) in models().items():
        r = run(model, grid, X, y, splits)
        out[mname] = {"auc_mean": r["roc_auc"]["mean"], "fold_auc": [f["roc_auc"] for f in r["folds"]],
                      "bacc_mean": r["balanced_accuracy"]["mean"]}
    return out


def main():
    warnings.filterwarnings("ignore")
    ap = argparse.ArgumentParser(); ap.add_argument("--zip", required=True); a = ap.parse_args()
    df = pd.read_csv("results/pilot-essig/features_labeled.csv")
    df = df[df.expert_label.isin(LIVE + DEAD)].reset_index(drop=True)
    y = df.expert_label.isin(DEAD).astype(int).to_numpy(); donors = df.donor.to_numpy()
    bf = [c for c in df.columns if c.startswith("BF_")]
    X = df[bf].to_numpy(float)
    rng = np.random.default_rng(SEED)
    res = {"n": {"live": int((y == 0).sum()), "dead": int(y.sum())}, "features": bf}
    splits = list(LeaveOneGroupOut().split(X, y, donors))
    lr = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=2000))  # noqa: E731

    # 1. permutation (within donor)
    def lodo_auc(yy):
        s = np.zeros(len(yy))
        for tr, te in splits:
            s[te] = lr().fit(X[tr], yy[tr]).predict_proba(X[te])[:, 1]
        return np.mean([roc_auc_score(yy[te], s[te]) for _, te in splits])
    a_obs = lodo_auc(y)
    perm = []
    for _ in range(200):
        yp = y.copy()
        for dn in np.unique(donors):
            idx = np.where(donors == dn)[0]; yp[idx] = rng.permutation(yp[idx])
        perm.append(lodo_auc(yp))
    res["permutation"] = {"logreg_C1_lodo_auc": round(float(a_obs), 3), "null_mean": round(float(np.mean(perm)), 3),
                          "null_max": round(float(np.max(perm)), 3), "n_perm": 200,
                          "p": round(float((1 + np.sum(np.array(perm) >= a_obs)) / 201), 4)}
    print("permutation", res["permutation"], flush=True)

    # 2. bootstrap CI per held-out donor
    res["bootstrap_ci95"] = {}
    for mname, mk in {"logreg_C1": lr, "rf": lambda: RandomForestClassifier(300, random_state=SEED, n_jobs=-1)}.items():
        for tr, te in splits:
            dn = donors[te][0]
            s = mk().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]; yt = y[te]
            boots = []
            for _ in range(1000):
                i = rng.integers(0, len(te), len(te))
                if len(np.unique(yt[i])) == 2:
                    boots.append(roc_auc_score(yt[i], s[i]))
            res["bootstrap_ci95"][f"{mname}_test_{dn}"] = {"auc": round(float(roc_auc_score(yt, s)), 3),
                                                          "ci95": np.percentile(boots, [2.5, 97.5]).round(3).tolist()}
            if mname == "logreg_C1":
                df.loc[te, "score_lodo"] = s
    print("bootstrap", res["bootstrap_ci95"], flush=True)

    # 3c. feature groups removed (original features)
    rob = []
    base = lodo_eval(X, y, donors); rob.append({"variant": "baseline (mask dataset, semua fitur BF)", **flat(base)})
    for gname, keys in GROUPS.items():
        keep = [c for c in bf if c.replace("BF_", "") not in keys]
        rob.append({"variant": f"tanpa fitur {gname}", "n_feat": len(keep), **flat(lodo_eval(df[keep].to_numpy(float), y, donors))})
        only = [c for c in bf if c.replace("BF_", "") in keys]
        rob.append({"variant": f"hanya fitur {gname}", "n_feat": len(only), **flat(lodo_eval(df[only].to_numpy(float), y, donors))})
        print(rob[-2]["variant"], rob[-2]["logreg"], rob[-1]["variant"], rob[-1]["logreg"], flush=True)

    # 3a/b. recomputed features with altered / own masks
    rec, imgs = recompute(a.zip, df.file.tolist())
    for k, d in rec.items():
        r = {"variant": f"mask {k}", **flat(lodo_eval(d[bf].to_numpy(float), y, donors))}
        if k == "own_mask":
            r["median_iou_vs_dataset_mask"] = round(float(d.own_vs_dataset_iou.median()), 3)
        rob.append(r); print(r, flush=True)
    pd.DataFrame(rob).to_csv(OUT / "B_robustness.csv", index=False)
    res["robustness"] = rob

    # 4. stain sanity + gallery
    ld = [c for c in df.columns if c.startswith("Live-Dead_")]
    res["live_dead_stain_auc_vs_expert"] = {c: round(float(roc_auc_score(y, df[c])), 3) for c in ["Live-Dead_mean", "Live-Dead_max", "Live-Dead_sum"] if c in ld}
    gallery(df, y, imgs)
    (OUT / "B_validation.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ["permutation", "bootstrap_ci95", "live_dead_stain_auc_vs_expert"]}, indent=1))


def flat(r):
    return {m: v["auc_mean"] for m, v in r.items()} | {f"{m}_folds": v["fold_auc"] for m, v in r.items()} | \
           {"bacc_range": [min(v["bacc_mean"] for v in r.values()), max(v["bacc_mean"] for v in r.values())]}


def gallery(df, y, imgs, n=8, seed=SEED):
    rng = np.random.default_rng(seed)
    pred = (df.score_lodo >= 0.5).astype(int).to_numpy()
    groups = {"Hidup (benar)": np.where((y == 0) & (pred == 0))[0], "Mati (benar)": np.where((y == 1) & (pred == 1))[0],
              "Hidup, diprediksi mati": np.where((y == 0) & (pred == 1))[0], "Mati, diprediksi hidup": np.where((y == 1) & (pred == 0))[0]}
    fig, ax = plt.subplots(len(groups), n, figsize=(n * 1.6, len(groups) * 1.9))
    for r, (title, idx) in enumerate(groups.items()):
        pick = rng.choice(idx, min(n, len(idx)), replace=False) if len(idx) else []
        for c in range(n):
            ax[r, c].axis("off")
            if c < len(pick):
                bf, m, _ = imgs[df.file.iat[pick[c]]]
                ax[r, c].imshow(bf, cmap="gray"); ax[r, c].contour(m, levels=[0.5], colors="lime", linewidths=0.6)
                ax[r, c].set_title(f"{df.donor.iat[pick[c]][-1]} p={df.score_lodo.iat[pick[c]]:.2f}", fontsize=7)
        ax[r, 0].text(-0.15, 0.5, f"{title}\n(n={len(idx)})", transform=ax[r, 0].transAxes, ha="right", va="center", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / "B_gallery_live_dead.png", dpi=110, bbox_inches="tight")


if __name__ == "__main__":
    main()
