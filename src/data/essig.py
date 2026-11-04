"""Essig et al. 2022 IFC dataset (Dryad doi:10.5061/dryad.ht76hdrk7): single-cell .h5 inside expN.zip.

Layout: Experiment_1/Donor_<d>/<condition>/<...>.h5 with datasets 'image' (H, W, 8) uint16 and 'mask' (H, W, 8).
Observed (pilot, exp1): 2 donors x 4 conditions (+SEA, -SEA, Isotype, Teplizumab) x 60,000 cells.
Channel 0 = brightfield (verified visually); channels 1-7 = fluorescence.
Channel names from the authors' notebook (marrlab/scifAI-notebooks, 'Data exploration.ipynb', Ch1..Ch8 -> index 0..7;
index mapping assumed, not stated by the authors). The Dryad README itself lists no channel names.
Each image is a T cell - B-LCL conjugate (immunological synapse); expert 'label' (str) exists only for a small subset.
"""
from __future__ import annotations

import io
import random
import zipfile
from pathlib import Path

import h5py
import numpy as np
from skimage.transform import resize

CONDITIONS = ["+SEA", "-SEA", "Isotype", "Teplizumab"]
FLUO_CHANNELS = list(range(1, 8))
CHANNEL_NAMES = ["BF", "Antibody", "CD18", "F-Actin", "MHCII", "CD3", "P-CD3zeta", "Live-Dead"]


def to_square64(img: np.ndarray, size: int = 64) -> np.ndarray:
    """Pad to square with the image median, resize to size x size, percentile-normalize to [0, 1]."""
    h, w = img.shape
    s = max(h, w)
    canvas = np.full((s, s), np.median(img), dtype=np.float32)
    canvas[(s - h) // 2:(s - h) // 2 + h, (s - w) // 2:(s - w) // 2 + w] = img
    out = resize(canvas, (size, size), anti_aliasing=True, preserve_range=True)
    lo, hi = np.percentile(out, [1, 99.5])
    return np.clip((out - lo) / max(hi - lo, 1e-6), 0, 1).astype(np.float32)


def build_pretrain_set(zip_path: Path, per_group: int = 3000, seed: int = 42) -> dict:
    """Sample `per_group` cells per (donor, condition); one random fluorescence channel per cell
    (channel-agnostic morphology). Returns X (N,64,64) float32, y (condition idx), donor, channel."""
    rng = random.Random(seed)
    z = zipfile.ZipFile(zip_path)
    groups: dict[tuple, list] = {}
    for n in z.namelist():
        if n.endswith(".h5"):
            parts = n.split("/")
            groups.setdefault((parts[1], parts[2]), []).append(n)
    X, y, donors, chans = [], [], [], []
    for (donor, cond), names in sorted(groups.items()):
        for n in rng.sample(names, min(per_group, len(names))):
            with z.open(n) as fh, h5py.File(io.BytesIO(fh.read()), "r") as h:
                img = h["image"][()]
            c = rng.choice(FLUO_CHANNELS)
            X.append(to_square64(img[..., c].astype(np.float32)))
            y.append(CONDITIONS.index(cond))
            donors.append(donor)
            chans.append(c)
    return {"X": np.stack(X), "y": np.array(y), "donor": np.array(donors), "channel": np.array(chans)}
