"""Overlay of own segmentation (frames 0, 76, 191) for visual QC. Usage: python -I src/illinois_overlay_demo.py <nd2> <out_dir>"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nd2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from illinois_extract_demo import segment  # noqa: E402


def main(nd2_path, out):
    f = nd2.ND2File(nd2_path); a = f.to_dask()
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    for i, t in enumerate([0, 76, 191]):
        im = a[t].compute(); p, _, _ = segment(im, 5)
        y0, x0, s = 800, 800, 400
        lo, hi = np.percentile(im, [1, 99.8])
        ax[i].imshow(im[y0:y0 + s, x0:x0 + s], cmap="gray", vmin=lo, vmax=hi)
        q = p[(p.y > y0) & (p.y < y0 + s) & (p.x > x0) & (p.x < x0 + s)]
        ax[i].scatter(q.x - x0, q.y - y0, s=q.area / 2, facecolors="none", edgecolors="lime", linewidths=0.8)
        ax[i].set_title(f"frame {t}: {len(p)} objects in full field"); ax[i].axis("off")
    f.close()
    plt.tight_layout(); plt.savefig(Path(out) / "demo_K16_segmentation_overlay.png", dpi=80)


if __name__ == "__main__":
    main(*sys.argv[1:3])
