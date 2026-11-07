"""Inspect the Illinois demo well (nd2 time-lapse, GFP) and the authors' trajectory CSV for the same well.

Usage: python -I src/illinois_inspect_nd2.py <nd2> <intensityTrajectories.zip> <out_dir>
"""
import io
import sys
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nd2
import numpy as np
import pandas as pd


def main(nd2_path, traj_zip, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    f = nd2.ND2File(nd2_path)
    a = f.to_dask()
    frames = {t: a[t].compute() for t in [0, 4, 76, 191]}
    f.close()
    fig, ax = plt.subplots(2, 4, figsize=(16, 8))
    for i, (t, im) in enumerate(frames.items()):
        lo, hi = np.percentile(im, [1, 99.8])
        ax[0, i].imshow(im[::4, ::4], cmap="gray", vmin=lo, vmax=hi); ax[0, i].set_title(f"frame {t} ({t*0.25:.1f} h) full")
        ax[1, i].imshow(im[900:1156, 900:1156], cmap="gray", vmin=lo, vmax=hi); ax[1, i].set_title("crop 256 px")
        print(f"frame {t}: min {im.min()} p1 {lo:.0f} median {np.median(im):.0f} p99.8 {hi:.0f} max {im.max()}")
    for x in ax.ravel():
        x.axis("off")
    plt.tight_layout(); plt.savefig(out / "demo_K16_frames.png", dpi=80)
    I = pd.read_csv(io.BytesIO(zipfile.ZipFile(traj_zip).read("DiversitySet3Plate2/WellK16.csv")), header=None).to_numpy(float)
    print("authors K16:", I.shape, "nan frac", np.isnan(I).mean().round(3), "median", np.nanmedian(I).round(1),
          "p5/p95", np.nanpercentile(I, [5, 95]).round(1))
    print("authors first row:", np.round(I[0, :8], 1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
