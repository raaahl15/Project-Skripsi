"""Luo et al. 2022/2023 CyTOF dataset (Dryad doi:10.7272/Q6SX6BFR): FCS loading and preprocessing.

Files: <Donor>_<Infected k | Uninfected>_CD8Normed_Singlets.fcs ("Normalized Singlets HLAC cells", README).
Culture label from the file name (HIV-infected vs uninfected culture); per-cell infection from the 'HIV' channel.
Marker names differ between donors (e.g. 'Casp3' / 'Cas3_cleaved'), so they are harmonized with ALIASES.
"""
from __future__ import annotations

import re
from pathlib import Path

import flowio
import numpy as np
import pandas as pd

FNAME_RE = re.compile(r"(Donor\d+)_(Infected\d+|Uninfected)_", re.I)
COFACTOR = 5.0  # standard arcsinh cofactor for mass cytometry

# lower-case raw marker name -> harmonized name
ALIASES = {
    "casp3": "Casp3_cleaved", "cas3_cleaved": "Casp3_cleaved", "caspase3": "Casp3_cleaved",
    "cd95fasl": "CD95", "pd-1": "PD1", "pd1": "PD1", "kc57": "KC57_p24",
    "live_dead": "LiveDead", "livedead": "LiveDead", "cisplatin": "LiveDead",
    "samhd1_abcam": "SAMHD1",
}
NON_MARKERS = {"Time", "Event_length", "DNA1", "DNA2", "bead", "bead_2", "bead_3", "background", "BCKG190Di",
               "190BCKG", "EQ", "empty", "BAR", "Ba", "Xe", "I", "131Xe", "138Ba", "140Ce", "142Ce", "176Lu",
               "195Pt", "208Pb", "Cis_2", "Cis_3"}


def _marker(pns: str, pnn: str) -> str:
    """'164Dy_CD95fasL' -> 'CD95' (harmonized); falls back to $PnN when $PnS is empty."""
    raw = (pns.split("_", 1)[1] if "_" in pns else pns) if pns else pnn
    return ALIASES.get(raw.lower(), raw)


def channel_table(fcs_path: Path) -> pd.DataFrame:
    """Channel index, $PnN (e.g. 'Dy164Di'), $PnS (e.g. '164Dy_CD95fasL') and harmonized marker name."""
    f = flowio.FlowData(str(fcs_path))
    rows = []
    for key in sorted(f.channels, key=int):  # flowio uses 1-based string keys, not guaranteed ordered
        ch = f.channels[key]
        pnn, pns = ch.get("PnN", ""), ch.get("PnS", "")
        rows.append({"idx": int(key) - 1, "pnn": pnn, "pns": pns, "marker": _marker(pns, pnn)})
    return pd.DataFrame(rows)


def load_fcs(fcs_path: Path) -> pd.DataFrame:
    """Event matrix with columns named by harmonized marker name (first occurrence kept)."""
    f = flowio.FlowData(str(fcs_path))
    data = np.reshape(np.array(f.events, dtype=np.float32), (-1, f.channel_count))
    ct = channel_table(fcs_path)
    df = pd.DataFrame(data[:, ct.idx.to_numpy()], columns=ct.marker.tolist())
    return df.loc[:, ~df.columns.duplicated()]


def load_all(root: Path, max_events_per_file: int | None = None, seed: int = 42) -> pd.DataFrame:
    """All FCS files (optionally subsampled per file) with donor / culture columns added."""
    frames = []
    for p in sorted(Path(root).rglob("*.fcs")):
        m = FNAME_RE.search(p.name)
        if not m:
            continue
        df = load_fcs(p)
        if max_events_per_file and len(df) > max_events_per_file:
            df = df.sample(max_events_per_file, random_state=seed)
        df["donor"] = m.group(1)
        df["culture"] = m.group(2)
        df["infected_culture"] = int(m.group(2).lower().startswith("infected"))
        df["file"] = p.name
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"No FCS files found under {root}")
    return pd.concat(frames, ignore_index=True)


def arcsinh(df: pd.DataFrame, cols: list[str], cofactor: float = COFACTOR) -> pd.DataFrame:
    out = df.copy()
    out[cols] = np.arcsinh(out[cols] / cofactor)
    return out
