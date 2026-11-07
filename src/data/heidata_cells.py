"""Nucleus segmentation (Lamin B1) and per-cell feature extraction for the heiDATA fields."""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi
from skimage import feature, filters, measure, morphology, segmentation

from .heidata import PIXEL_SIZE_UM, normalize

MIN_DIAM_UM, MAX_DIAM_UM = 3.0, 12.0
_MIN_AREA = int(np.pi * (MIN_DIAM_UM / PIXEL_SIZE_UM / 2) ** 2)
_MAX_AREA = int(np.pi * (MAX_DIAM_UM / PIXEL_SIZE_UM / 2) ** 2)


def segment_nuclei_classical(lamin_mip: np.ndarray) -> np.ndarray:
    """Label image of nuclei from a Lamin B1 max projection.

    Lamin B1 stains the nuclear rim; dim/out-of-focus nuclei are recovered by working on a
    log-compressed image with a local threshold, then holes (nucleus interior) are filled and
    touching nuclei are split with a distance-transform watershed.
    """
    img = normalize(lamin_mip)
    img = filters.gaussian(np.log1p(20 * img), sigma=1.5)
    local = filters.threshold_local(img, block_size=151, offset=-0.01)
    mask = (img > local) & (img > filters.threshold_otsu(img) * 0.6)
    mask = morphology.binary_closing(mask, morphology.disk(4))
    mask = ndi.binary_fill_holes(mask)
    mask = morphology.binary_opening(mask, morphology.disk(3))
    mask = morphology.remove_small_objects(mask, _MIN_AREA)
    dist = ndi.distance_transform_edt(mask)
    markers = measure.label(morphology.h_maxima(filters.gaussian(dist, 2), 3))
    lab = segmentation.watershed(-dist, markers, mask=mask)
    return _filter_labels(lab)


def segment_nuclei_cellpose(lamin_mip: np.ndarray, model=None) -> np.ndarray:
    """Label image of nuclei using Cellpose (cpsam, CPU)."""
    from cellpose import models  # heavy import, only when used
    model = model or models.CellposeModel(gpu=False)
    masks, _, _ = model.eval(normalize(lamin_mip), diameter=None)
    return _filter_labels(masks.astype(np.int32))


MIN_SOLIDITY = 0.88  # resting T-cell nuclei are compact and convex; irregular blobs are background/debris


def _filter_labels(lab: np.ndarray) -> np.ndarray:
    """Drop objects outside the plausible nucleus size, irregular (non-convex) objects,
    and objects cut by the image border."""
    out = np.zeros_like(lab)
    h, w = lab.shape
    k = 1
    for p in measure.regionprops(lab):
        r0, c0, r1, c1 = p.bbox
        if not (_MIN_AREA <= p.area <= _MAX_AREA) or p.solidity < MIN_SOLIDITY:
            continue
        if r0 == 0 or c0 == 0 or r1 >= h or c1 >= w:
            continue
        out[lab == p.label] = k
        k += 1
    return out


def detect_puncta(ch_mip: np.ndarray, threshold: float = 0.08,
                  scale: tuple[float, float] | None = None) -> np.ndarray:
    """Spot (puncta) coordinates (row, col) with a Laplacian-of-Gaussian detector.

    scale: (low, high) raw intensities mapped to 0..1. Pass a range SHARED by all fields of one experiment
    (see shared_scale). Without it the image is rescaled to its own 1-99.95 percentiles, which turns the
    background noise of a puncta-free image (Mock) into thousands of false spots (QC 7 Nov 2026).
    """
    if scale is None:
        img = normalize(ch_mip, 1, 99.95)
    else:
        lo, hi = scale
        img = np.clip((ch_mip.astype(np.float32) - lo) / max(hi - lo, 1e-6), 0, 1)
    blobs = feature.blob_log(img, min_sigma=1, max_sigma=3, num_sigma=5, threshold=threshold)
    return blobs[:, :2] if len(blobs) else np.zeros((0, 2))


def shared_scale(images: list[np.ndarray], low: float = 1.0, high: float = 99.95) -> tuple[float, float]:
    """Percentile range of the pooled pixels of several images (one experiment/figure)."""
    pooled = np.concatenate([im.ravel() for im in images])
    lo, hi = np.percentile(pooled, [low, high])
    return float(lo), float(hi)


def cell_features(lab: np.ndarray, lamin_mip: np.ndarray, extra: dict[str, np.ndarray] | None = None,
                  puncta: dict[str, np.ndarray] | None = None, ring_um: float = 1.5) -> list[dict]:
    """Per-nucleus morphometric + intensity features.

    extra:  other channel max projections (e.g. {"gfp": img}) -> mean intensity in nucleus.
    puncta: spot coordinates per channel (e.g. {"ca": coords}) -> counts inside nucleus and in a
            perinuclear ring of width ring_um (proxy for the cytoplasm of these small resting cells).
    """
    extra = extra or {}
    puncta = puncta or {}
    ring_px = max(1, int(round(ring_um / PIXEL_SIZE_UM)))
    rows = []
    for p in measure.regionprops(lab, intensity_image=lamin_mip):
        m = lab == p.label
        rim = m & ~morphology.binary_erosion(m, morphology.disk(4))   # ~0.5 um rim
        core = morphology.binary_erosion(m, morphology.disk(8))
        ring = morphology.binary_dilation(m, morphology.disk(ring_px)) & ~m & (lab == 0)
        lam_rim = lamin_mip[rim].mean() if rim.any() else np.nan
        lam_core = lamin_mip[core].mean() if core.any() else np.nan
        r = {
            "label": p.label,
            "area_um2": p.area * PIXEL_SIZE_UM ** 2,
            "perimeter_um": p.perimeter * PIXEL_SIZE_UM,
            "eq_diameter_um": p.equivalent_diameter_area * PIXEL_SIZE_UM,
            "major_axis_um": p.axis_major_length * PIXEL_SIZE_UM,
            "minor_axis_um": p.axis_minor_length * PIXEL_SIZE_UM,
            "eccentricity": p.eccentricity,
            "solidity": p.solidity,
            "circularity": 4 * np.pi * p.area / max(p.perimeter, 1) ** 2,
            "lamin_mean": p.intensity_mean,
            "lamin_std": float(lamin_mip[m].std()),
            "lamin_rim_core_ratio": lam_rim / lam_core if lam_core and not np.isnan(lam_core) else np.nan,
        }
        for name, img in extra.items():
            r[f"{name}_mean"] = float(img[m].mean())
        for name, coords in puncta.items():
            if len(coords):
                rc = np.clip(np.round(coords).astype(int), 0, np.array(lab.shape) - 1)
                inside = m[rc[:, 0], rc[:, 1]]
                near = ring[rc[:, 0], rc[:, 1]]
                r[f"{name}_puncta_nucleus"] = int(inside.sum())
                r[f"{name}_puncta_perinuclear"] = int(near.sum())
            else:
                r[f"{name}_puncta_nucleus"] = 0
                r[f"{name}_puncta_perinuclear"] = 0
        rows.append(r)
    return rows
