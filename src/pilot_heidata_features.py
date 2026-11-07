"""Pilot (feasibility) step 1: segment nuclei in every heiDATA field and extract per-cell features.

Usage:
    python src/pilot_heidata_features.py --root data/raw/heidata-MUXYRY --out results/pilot-heidata --seg classical
Outputs: cells.csv (one row per nucleus), labels/<field>.npy, overlays/<field>.png, summary.txt
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

from src.data.heidata import FIELDS, field_id, load_stack, max_projection
from src.data.heidata_cells import (cell_features, detect_puncta, segment_nuclei_cellpose,
                                    segment_nuclei_classical, shared_scale)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/raw/heidata-MUXYRY")
    ap.add_argument("--out", default="results/pilot-heidata")
    ap.add_argument("--seg", choices=["classical", "cellpose"], default="classical")
    args = ap.parse_args()

    out = Path(args.out)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    (out / "overlays").mkdir(parents=True, exist_ok=True)
    cp_model = None
    if args.seg == "cellpose":
        from cellpose import models
        cp_model = models.CellposeModel(gpu=False)

    # CA puncta: one intensity scale per figure (experiment), shared by all its fields, so that a Mock field
    # without capsids is not stretched to full range (QC 7 Nov 2026, src/check_ca_channel.py).
    ca_mips = {}
    for f in FIELDS:
        if "ca" in f.channels:
            ca_mips[field_id(f)] = max_projection(load_stack(Path(args.root), f), f.channels["ca"])
    ca_scale = {fig: shared_scale([ca_mips[field_id(f)] for f in FIELDS if f.figure == fig and "ca" in f.channels])
                for fig in {f.figure for f in FIELDS if "ca" in f.channels}}

    rows, summary = [], []
    for f in FIELDS:
        fid = field_id(f)
        stack = load_stack(Path(args.root), f)
        lam = max_projection(stack, f.channels["lamin"])
        lab = (segment_nuclei_cellpose(lam, cp_model) if args.seg == "cellpose"
               else segment_nuclei_classical(lam))
        np.save(out / "labels" / f"{fid}.npy", lab)

        extra = {k: max_projection(stack, f.channels[k]) for k in ("gfp",) if k in f.channels}
        puncta = {}
        if "ca" in f.channels:
            puncta["ca"] = detect_puncta(ca_mips[fid], scale=ca_scale[f.figure])
        feats = cell_features(lab, lam, extra, puncta)
        for r in feats:
            r.update(field=fid, figure=f.figure, condition=f.condition, treatment=f.treatment)
        rows += feats
        summary.append(f"{fid:16s} cells={len(feats):3d}  channels={sorted(f.channels)}")

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(lam, cmap="gray", vmax=np.percentile(lam, 99.5))
        ax.contour(lab > 0, levels=[0.5], colors="yellow", linewidths=0.6)
        if "ca" in puncta and len(puncta["ca"]):
            ax.plot(puncta["ca"][:, 1], puncta["ca"][:, 0], ".", color="magenta", ms=1.5)
        ax.set_title(f"{fid} ({args.seg}): {len(feats)} nuclei", fontsize=9)
        ax.axis("off")
        fig.savefig(out / "overlays" / f"{fid}.png", dpi=110, bbox_inches="tight")
        plt.close(fig)

    df = pd.DataFrame(rows)
    df.to_csv(out / "cells.csv", index=False)
    by_cond = df.groupby("condition").size().to_dict()
    summary.append(f"TOTAL cells={len(df)}  per condition={by_cond}  segmentation={args.seg}")
    (out / "summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
