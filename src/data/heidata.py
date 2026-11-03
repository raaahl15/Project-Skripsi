"""heiDATA MUXYRY dataset (Ananth et al. 2024, CC BY 4.0): loading, channel mapping, segmentation.

Raw files: 3D fluorescence z-stacks (Z, C, Y, X), uint16, 0.133 um/px.
Channel indices (0-based) come from README.rtf shipped with the dataset.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import tifffile

PIXEL_SIZE_UM = 0.133


@dataclass(frozen=True)
class Field:
    """One microscopy field (one raw z-stack file)."""
    rel_path: str     # path relative to the dataset root
    figure: str       # paper panel, e.g. "1G"
    condition: str    # "+Vpx", "-Vpx" or "Mock"
    treatment: str    # extra treatment ("", "EFV", "DMSO", "SMI")
    channels: dict    # marker name -> channel index


_C1 = {"snap": 0, "ca": 1, "lamin": 2}                     # Fig 1G
_C2 = {"snap": 0, "cpsf6_or_sc35": 1, "gfp": 2, "lamin": 3}  # Fig 2A / 2D
_C3 = {"lamin": 0, "gfp": 1, "edu": 2, "ca": 3}             # Fig 3B / 4D / S3B

FIELDS: list[Field] = [
    Field("raw Fig 1/Fig 1G +Vpx.tif", "1G", "+Vpx", "", _C1),
    Field("raw Fig 1/Fig 1G -Vpx.tif", "1G", "-Vpx", "", _C1),
    # README lists no channels for Mock; assumed identical to the other Fig 1G files.
    Field("raw Fig 1/Fig 1G Mock.tif", "1G", "Mock", "", _C1),
    Field("raw Fig 2/Fig 2A +Vpx.tif", "2A", "+Vpx", "", _C2),
    Field("raw Fig 2/Fig 2A -Vpx.tif", "2A", "-Vpx", "", _C2),
    Field("raw Fig 2/Fig 2D +Vpx.tif", "2D", "+Vpx", "", _C2),
    Field("raw Fig 2/Fig 2D -Vpx.tif", "2D", "-Vpx", "", _C2),
    Field("raw Fig 3/Fig 3B +Vpx.tif", "3B", "+Vpx", "", _C3),
    Field("raw Fig 3/Fig 3B -Vpx.tif", "3B", "-Vpx", "", _C3),
    # README says "4D DMSO +Vpx", but the shipped files are "-Vpx" (DMSO and SMI). Using the file names.
    Field("raw Fig 4/Fig 4D DMSO -Vpx.tif", "4D", "-Vpx", "DMSO", _C3),
    Field("raw Fig 4/Fig 4D SMI -Vpx.tif", "4D", "-Vpx", "SMI", _C3),
    # Channel order for S3B not listed in README; assumed identical to 3B/4D (same 4-channel layout).
    Field("raw Fig S3/Fig S3B +Vpx +EFV.tif", "S3B", "+Vpx", "EFV", _C3),
    Field("raw Fig S3/Fig S3B -Vpx +EFV.tif", "S3B", "-Vpx", "EFV", _C3),
    Field("raw Fig S3/Fig S3B mock.tif", "S3B", "Mock", "", _C3),
]


def field_id(f: Field) -> str:
    return f"{f.figure}_{f.condition}{('_' + f.treatment) if f.treatment else ''}"


def load_stack(root: Path, f: Field) -> np.ndarray:
    """Return the raw stack as (Z, C, Y, X) uint16."""
    arr = tifffile.imread(Path(root) / f.rel_path)
    if arr.ndim != 4:
        raise ValueError(f"{f.rel_path}: expected ZCYX, got shape {arr.shape}")
    return arr


def max_projection(stack: np.ndarray, channel: int) -> np.ndarray:
    """Maximum-intensity projection over Z for one channel, as float32."""
    return stack[:, channel].max(axis=0).astype(np.float32)


def normalize(img: np.ndarray, low: float = 1.0, high: float = 99.8) -> np.ndarray:
    """Percentile normalization to [0, 1] (robust to the camera offset ~1900 counts)."""
    lo, hi = np.percentile(img, [low, high])
    return np.clip((img - lo) / max(hi - lo, 1e-6), 0, 1).astype(np.float32)
