"""Own image feature extraction from the Illinois demo well (IDB-8103861, DiversitySet3 Plate2 Well K16).

nd2: 192 frames x 2044 x 2048, one GFP channel, 0.646 um/px, 15 min/frame (48 h).
Pipeline per frame:
    1. background = Gaussian blur (sigma 40 px) of a 1/8-downsampled frame, upsampled -> removes vignetting
    2. signal = Gaussian(sigma 1.5) - background; threshold = k * robust noise sigma (MAD) of the signal
    3. connected components, holes filled, area 40-1200 px, touching cells split by distance-transform watershed
    4. per object: centroid, area, perimeter-free shape (eccentricity, solidity), raw mean intensity,
       background-subtracted mean and integrated intensity
Tracking: frame-to-frame nearest-neighbour linking (mutual nearest, max 6 px), tracks kept if complete over a window.
Comparison with the authors' trajectories (72 frames, NIS Elements) for the same well.

Usage: python -I src/illinois_extract_demo.py <nd2> <intensityTrajectories.zip> <out_dir> [--k 5]
"""
import argparse
import io
import json
import time
import zipfile
from pathlib import Path

import nd2
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from skimage.feature import peak_local_max
from skimage.measure import regionprops_table
from skimage.segmentation import watershed
from skimage.transform import resize

FRAME_H = 0.25


def segment(im: np.ndarray, k: float):
    im = im.astype(np.float32)
    small = im[::8, ::8]
    bg = resize(ndi.gaussian_filter(small, 5), im.shape, order=1, preserve_range=True)  # sigma 5 at 1/8 = 40 px
    sig = ndi.gaussian_filter(im, 1.5) - bg
    noise = 1.4826 * np.median(np.abs(sig - np.median(sig)))
    mask = ndi.binary_fill_holes(sig > k * noise)
    mask = ndi.binary_opening(mask, iterations=1)
    dist = ndi.distance_transform_edt(mask)
    lab0, _ = ndi.label(mask)
    peaks = peak_local_max(dist, min_distance=6, labels=lab0, exclude_border=False)
    markers = np.zeros_like(lab0); markers[tuple(peaks.T)] = np.arange(1, len(peaks) + 1)
    lab = watershed(-dist, markers, mask=mask)
    p = pd.DataFrame(regionprops_table(lab, intensity_image=np.dstack([im, im - bg]),
                                       properties=("label", "centroid", "area", "eccentricity", "solidity",
                                                   "intensity_mean")))
    p = p.rename(columns={"centroid-0": "y", "centroid-1": "x", "intensity_mean-0": "I_raw_mean",
                          "intensity_mean-1": "I_bgsub_mean"})
    p = p[(p.area >= 40) & (p.area <= 1200)].copy()
    p["I_bgsub_int"] = p.I_bgsub_mean * p.area
    return p, float(noise), float(np.median(bg))


def track(frames: list, max_d=6.0):
    """Mutual-nearest-neighbour linking; returns DataFrame with track_id."""
    tid = np.arange(len(frames[0])); nxt = len(frames[0])
    frames[0]["track"] = tid
    for t in range(1, len(frames)):
        a, b = frames[t - 1], frames[t]
        b["track"] = -1
        if len(a) and len(b):
            ta, tb = cKDTree(a[["y", "x"]]), cKDTree(b[["y", "x"]])
            dab, iab = tb.query(a[["y", "x"]]); dba, iba = ta.query(b[["y", "x"]])
            tr = b["track"].to_numpy().copy()
            for i, (d, j) in enumerate(zip(dab, iab)):
                if d <= max_d and iba[j] == i:
                    tr[j] = a["track"].iat[i]
            b["track"] = tr
        new = b["track"] < 0
        b.loc[new, "track"] = np.arange(nxt, nxt + new.sum()); nxt += int(new.sum())
    return pd.concat([f.assign(frame=t) for t, f in enumerate(frames)], ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nd2"); ap.add_argument("traj_zip"); ap.add_argument("out"); ap.add_argument("--k", type=float, default=5)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cache = out / f"objects_k{a.k:g}_untracked.csv.gz"
    n_frames = 192
    if cache.exists():
        allp = pd.read_csv(cache)
        frames = [allp[allp.frame == t].drop(columns="frame").reset_index(drop=True) for t in range(n_frames)]
    else:
        f = nd2.ND2File(a.nd2); arr = f.to_dask(); n_frames = arr.shape[0]
        frames, qc = [], []
        t0 = time.time()
        for t in range(n_frames):
            p, noise, bgmed = segment(arr[t].compute(), a.k)
            frames.append(p.reset_index(drop=True)); qc.append({"frame": t, "n_obj": len(p), "noise": noise, "bg_median": bgmed})
            if t % 24 == 0:
                print(f"frame {t}: {len(p)} objects, noise {noise:.1f}, {time.time()-t0:.0f}s", flush=True)
        f.close()
        pd.concat([fr.assign(frame=t) for t, fr in enumerate(frames)]).to_csv(cache, index=False)
        pd.DataFrame(qc).to_csv(out / f"frame_qc_k{a.k:g}.csv", index=False)
    qc = [{"n_obj": len(fr)} for fr in frames]
    obj = track(frames)
    obj.to_csv(out / f"objects_k{a.k:g}_tracked.csv.gz", index=False)

    # complete tracks over the authors' window (72 frames; window start chosen by best match of well-mean shape below)
    I_auth = pd.read_csv(io.BytesIO(zipfile.ZipFile(a.traj_zip).read("DiversitySet3Plate2/WellK16.csv")), header=None).to_numpy(float)
    L = I_auth.shape[1]
    summ = {"authors": {"n_cells": int(I_auth.shape[0]), "median": float(np.median(I_auth)),
                        "p5_p95": np.percentile(I_auth, [5, 95]).round(1).tolist()},
            "objects_per_frame_median": float(pd.DataFrame(qc).n_obj.median()), "windows": {}}
    auth_mean = I_auth.mean(0)
    best = None
    for s in range(0, n_frames - L + 1, 4):
        w = obj[(obj.frame >= s) & (obj.frame < s + L)]
        cnt = w.groupby("track").frame.nunique()
        full = cnt[cnt == L].index
        if len(full) < 5:
            continue
        piv = w[w.track.isin(full)].pivot_table(index="track", columns="frame", values="I_raw_mean")
        r = float(np.corrcoef(piv.mean(0).to_numpy(), auth_mean)[0, 1])
        summ["windows"][s] = {"n_full_tracks": int(len(full)), "median_raw": round(float(np.median(piv.to_numpy())), 1),
                              "r_wellmean_vs_authors": round(r, 3)}
        if best is None or r > best[1]:
            best = (s, r, piv)
    s, r, piv = best
    summ["best_window_start_frame"] = int(s)
    piv.to_csv(out / f"own_trajectories_k{a.k:g}_I_raw_window{s}.csv")
    (out / f"extract_summary_k{a.k:g}.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summ.items() if k != "windows"}, indent=1))
    print("best window", s, "r", round(r, 3), "n full", piv.shape[0])
    for k_, v in list(summ["windows"].items())[:8]:
        print(k_, v)


if __name__ == "__main__":
    main()
