"""QC of the HIV-1 capsid (CA) puncta feature (heiDATA).

Problem found 7 Nov 2026: Mock 1G (no virus) had the MOST CA puncta. detect_puncta() rescales every image to its own
1-99.95 percentile range before a fixed LoG threshold, so in an image without real puncta the background noise is
stretched to full range and detected as spots.

This script (1) prints raw CA-channel statistics per field and (2) recounts puncta with a scale SHARED by all fields
of the same figure (percentiles of the pooled raw pixels), so a dim Mock image stays dim.

Usage: python src/check_ca_channel.py --root data/raw/heidata-MUXYRY
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import feature

from src.data.heidata import FIELDS, field_id, load_stack, max_projection
from src.data.heidata_cells import detect_puncta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/raw/heidata-MUXYRY")
    ap.add_argument("--out", default="results/b6")
    a = ap.parse_args()
    out = Path(a.out)
    fields = [f for f in FIELDS if "ca" in f.channels]
    imgs = {field_id(f): (f, max_projection(load_stack(Path(a.root), f), f.channels["ca"]).astype(np.float32))
            for f in fields}

    rows = []
    for fig in sorted({f.figure for f, _ in imgs.values()}):
        group = {k: v for k, v in imgs.items() if v[0].figure == fig}
        pooled = np.concatenate([im.ravel() for _, im in group.values()])
        lo, hi = np.percentile(pooled, [1, 99.95])
        for fid, (f, im) in group.items():
            shared = np.clip((im - lo) / (hi - lo), 0, 1)
            n_shared = len(feature.blob_log(shared, min_sigma=1, max_sigma=3, num_sigma=5, threshold=0.08))
            rows.append({"field": fid, "figure": fig, "condition": f.condition,
                         "raw_median": float(np.median(im)), "raw_p99": float(np.percentile(im, 99)),
                         "raw_p99.95": float(np.percentile(im, 99.95)), "raw_max": float(im.max()),
                         "puncta_per_image_scale": len(detect_puncta(im)), "puncta_shared_scale": n_shared})
    df = pd.DataFrame(rows)
    df.to_csv(out / "A_capsid_channel_qc.csv", index=False)
    print(df.round(1).to_string())

    # side-by-side 1G fields, same display range (pooled percentiles)
    g = {k: v for k, v in imgs.items() if v[0].figure == "1G"}
    lo, hi = np.percentile(np.concatenate([im.ravel() for _, im in g.values()]), [1, 99.95])
    fig, axes = plt.subplots(1, len(g), figsize=(4 * len(g), 4))
    for ax, (fid, (_, im)) in zip(axes, sorted(g.items())):
        ax.imshow(im, cmap="magma", vmin=lo, vmax=hi)
        ax.set_title(f"{fid} (skala sama)", fontsize=9)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(out / "A_capsid_1G_same_scale.png", dpi=110)


if __name__ == "__main__":
    main()
