"""Rough nucleus count per field from the Lamin B1 channel (max projection), plus GFP/CA summary.
Exploratory only (not a thesis result): Otsu threshold + hole filling + size filter."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tifffile
from scipy import ndimage as ndi
from skimage import filters, measure, morphology, segmentation

root = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

# 0-based channel indices from README.rtf
PANELS = {
    "raw Fig 1/Fig 1G +Vpx.tif": dict(lamin=2, ca=1),
    "raw Fig 1/Fig 1G -Vpx.tif": dict(lamin=2, ca=1),
    "raw Fig 1/Fig 1G Mock.tif": dict(lamin=2, ca=1),  # README gives no channel list for Mock; assumed same as 1G
    "raw Fig 2/Fig 2A +Vpx.tif": dict(lamin=3, gfp=2),
    "raw Fig 2/Fig 2A -Vpx.tif": dict(lamin=3, gfp=2),
    "raw Fig 2/Fig 2D +Vpx.tif": dict(lamin=3, gfp=2),
    "raw Fig 2/Fig 2D -Vpx.tif": dict(lamin=3, gfp=2),
    "raw Fig 3/Fig 3B +Vpx.tif": dict(lamin=0, gfp=1, ca=3),
    "raw Fig 3/Fig 3B -Vpx.tif": dict(lamin=0, gfp=1, ca=3),
    "raw Fig 4/Fig 4D DMSO -Vpx.tif": dict(lamin=0, gfp=1, ca=3),
    "raw Fig 4/Fig 4D SMI -Vpx.tif": dict(lamin=0, gfp=1, ca=3),
    "raw Fig S3/Fig S3B +Vpx +EFV.tif": dict(lamin=0, gfp=1, ca=3),  # channel order assumed as Fig 3B/4D
    "raw Fig S3/Fig S3B -Vpx +EFV.tif": dict(lamin=0, gfp=1, ca=3),
    "raw Fig S3/Fig S3B mock.tif": dict(lamin=0, gfp=1, ca=3),
}
PX_UM = 0.133
MIN_AREA = int(np.pi * (3.0 / PX_UM / 2) ** 2)   # nucleus diameter >= 3 um
MAX_AREA = int(np.pi * (10.0 / PX_UM / 2) ** 2)  # nucleus diameter <= 10 um

total = 0
for rel, ch in PANELS.items():
    f = root / rel
    img = tifffile.imread(f)  # (Z, C, Y, X)
    lam = img[:, ch["lamin"]].max(axis=0).astype(float)
    sm = filters.gaussian(lam, sigma=2)
    mask = sm > filters.threshold_otsu(sm)
    mask = ndi.binary_fill_holes(morphology.binary_closing(mask, morphology.disk(3)))
    mask = morphology.remove_small_objects(mask, MIN_AREA)
    # split touching nuclei with distance-transform watershed
    dist = ndi.distance_transform_edt(mask)
    peaks = morphology.h_maxima(filters.gaussian(dist, 2), 3)
    markers = measure.label(peaks)
    lab = segmentation.watershed(-dist, markers, mask=mask)
    props = [p for p in measure.regionprops(lab) if MIN_AREA <= p.area <= MAX_AREA]
    border = sum(1 for p in props if min(p.bbox[:2]) == 0 or max(p.bbox[2:]) >= lam.shape[0])
    n = len(props)
    total += n
    diam = [2 * np.sqrt(p.area / np.pi) * PX_UM for p in props]
    line = f"{rel:38s} nuclei={n:3d} (touching border={border:2d}) median diam={np.median(diam) if diam else 0:.1f} um"
    if "gfp" in ch:
        g = img[:, ch["gfp"]].max(axis=0).astype(float)
        means = [g[lab == p.label].mean() for p in props]
        line += f" | GFP per-nucleus mean: min={min(means):.0f} med={np.median(means):.0f} max={max(means):.0f}"
    print(line)

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.imshow(lam, cmap="gray", vmax=np.percentile(lam, 99.5))
    ax.contour(lab > 0, levels=[0.5], colors="yellow", linewidths=0.6)
    for p in props:
        y, x = p.centroid
        ax.plot(x, y, "r+", ms=4)
    ax.set_title(f"{Path(rel).stem}: {n} nuclei", fontsize=9)
    ax.axis("off")
    fig.savefig(out_dir / (Path(rel).stem.replace(" ", "_") + ".png"), dpi=110, bbox_inches="tight")
    plt.close(fig)

print(f"TOTAL nuclei (rough): {total}")
