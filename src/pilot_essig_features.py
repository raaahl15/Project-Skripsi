"""Pilot (Essig IFC, exp1): hand-crafted per-cell features from image + per-channel masks.

Samples N cells per (donor, condition) straight from exp1.zip (no unpacking), extracts interpretable
features per channel and writes results/pilot-essig/features.csv.

Usage: python -m src.pilot_essig_features --zip <exp1.zip> --per-group 1500
"""
from __future__ import annotations

import argparse
import io
import random
import time
import zipfile
from itertools import combinations
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import label, regionprops
from scipy import ndimage as ndi

from src.data.essig import CHANNEL_NAMES

COLOC = [3, 4, 5, 6]  # F-Actin, MHCII, CD3, P-CD3zeta


def shape_feats(m: np.ndarray, p: str) -> dict:
    """Morphometry of the largest object in a binary mask; also number of objects."""
    lab = label(m)
    if lab.max() == 0:
        return {f"{p}_n_obj": 0, f"{p}_area": 0.0, f"{p}_perimeter": 0.0, f"{p}_eccentricity": 0.0,
                f"{p}_solidity": 0.0, f"{p}_circularity": 0.0, f"{p}_major_axis": 0.0, f"{p}_minor_axis": 0.0}
    r = max(regionprops(lab), key=lambda x: x.area)
    per = r.perimeter if r.perimeter > 0 else 1.0
    return {f"{p}_n_obj": int(lab.max()), f"{p}_area": float(m.sum()), f"{p}_perimeter": float(r.perimeter),
            f"{p}_eccentricity": float(r.eccentricity), f"{p}_solidity": float(r.solidity),
            f"{p}_circularity": float(4 * np.pi * r.area / per ** 2), f"{p}_major_axis": float(r.axis_major_length),
            f"{p}_minor_axis": float(r.axis_minor_length)}


def intensity_feats(img: np.ndarray, m: np.ndarray, bg: float, p: str) -> dict:
    v = img[m] - bg if m.any() else np.array([0.0])
    out = {f"{p}_mean": float(v.mean()), f"{p}_std": float(v.std()), f"{p}_max": float(v.max()),
           f"{p}_sum": float(v.sum()), f"{p}_p90": float(np.percentile(v, 90))}
    # radial distribution: mean intensity in outer rim (2 px) vs inner region
    if m.sum() > 20:
        inner = ndi.binary_erosion(m, iterations=2)
        rim = m & ~inner
        out[f"{p}_rim_inner_ratio"] = float((img[rim].mean() - bg) / (abs(img[inner].mean() - bg) + 1e-6)) if inner.any() else 0.0
    else:
        out[f"{p}_rim_inner_ratio"] = 0.0
    return out


def texture_feats(img: np.ndarray, m: np.ndarray, p: str) -> dict:
    """GLCM (Haralick) texture inside the mask bounding box, 32 grey levels."""
    keys = ["contrast", "homogeneity", "energy", "correlation"]
    if m.sum() < 20:
        return {f"{p}_glcm_{k}": 0.0 for k in keys}
    ys, xs = np.where(m)
    crop = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)
    lo, hi = np.percentile(crop, [1, 99])
    q = np.clip((crop - lo) / max(hi - lo, 1e-6) * 31, 0, 31).astype(np.uint8)
    g = graycomatrix(q, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=32, symmetric=True, normed=True)
    return {f"{p}_glcm_{k}": float(np.nan_to_num(graycoprops(g, k).mean())) for k in keys}


def cell_features(img: np.ndarray, mask: np.ndarray) -> dict:
    img = img.astype(np.float32)
    mask = mask > 0
    union = mask.any(axis=-1)
    f = {"img_h": img.shape[0], "img_w": img.shape[1]}
    for c, name in enumerate(CHANNEL_NAMES):
        m = mask[..., c]
        bg = float(np.median(img[..., c][~union])) if (~union).any() else 0.0
        f.update(shape_feats(m, name))
        f.update(intensity_feats(img[..., c], m, bg, name))
        f.update(texture_feats(img[..., c], m, name))
    # brightfield: gradient RMS (edge sharpness / refractive contrast) inside BF mask
    bf = img[..., 0]
    gy, gx = np.gradient(bf)
    m0 = mask[..., 0]
    f["BF_gradient_rms"] = float(np.sqrt((gx[m0] ** 2 + gy[m0] ** 2).mean())) if m0.any() else 0.0
    # colocalisation (Pearson) between fluorescence channels inside the union mask
    for a, b in combinations(COLOC, 2):
        va, vb = img[..., a][union], img[..., b][union]
        r = np.corrcoef(va, vb)[0, 1] if va.size > 2 and va.std() > 0 and vb.std() > 0 else 0.0
        f[f"pearson_{CHANNEL_NAMES[a]}_{CHANNEL_NAMES[b]}"] = float(r)
    return f


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--per-group", type=int, default=1500)
    ap.add_argument("--out", default="results/pilot-essig/features.csv")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    z = zipfile.ZipFile(a.zip)
    groups: dict[tuple, list] = {}
    for n in z.namelist():
        if n.endswith(".h5"):
            parts = n.split("/")
            groups.setdefault((parts[1], parts[2]), []).append(n)
    rows, t0 = [], time.time()
    for (donor, cond), names in sorted(groups.items()):
        for n in rng.sample(sorted(names), min(a.per_group, len(names))):
            with z.open(n) as fh, h5py.File(io.BytesIO(fh.read()), "r") as h:
                img, mask = h["image"][()], h["mask"][()]
                lab = h["label"][()] if "label" in h else b""
            row = {"file": n, "donor": donor, "condition": cond,
                   "expert_label": lab.decode() if isinstance(lab, bytes) else str(lab)}
            row.update(cell_features(img, mask))
            rows.append(row)
        print(f"{donor} {cond}: {len(rows)} cells, {time.time() - t0:.0f}s", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print("saved", out, len(rows), "rows")


if __name__ == "__main__":
    main()
