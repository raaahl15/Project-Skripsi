"""Pilot (Essig exp1): extract features for every expert-labelled image (h5 key 'label').

Writes results/pilot-essig/features_labeled.csv. Used to validate the Live-Dead threshold label against the
expert 'Dead_Cell' class and to train brightfield-only live-vs-dead models on expert labels.

Usage: python -m src.pilot_essig_labeled --zip <exp1.zip>
"""
from __future__ import annotations

import argparse
import io
import time
import zipfile
from pathlib import Path

import h5py
import pandas as pd

from src.pilot_essig_features import cell_features


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--out", default="results/pilot-essig/features_labeled.csv")
    a = ap.parse_args()
    z = zipfile.ZipFile(a.zip)
    rows, t0 = [], time.time()
    for i, n in enumerate(n for n in z.namelist() if n.endswith(".h5")):
        with z.open(n) as fh, h5py.File(io.BytesIO(fh.read()), "r") as h:
            if "label" not in h:
                continue
            lab = h["label"][()]
            img, mask = h["image"][()], h["mask"][()]
        parts = n.split("/")
        row = {"file": n, "donor": parts[1], "condition": parts[2],
               "expert_label": lab.decode() if isinstance(lab, bytes) else str(lab)}
        row.update(cell_features(img, mask))
        rows.append(row)
        if len(rows) % 500 == 0:
            print(f"{len(rows)} labelled ({i} scanned), {time.time() - t0:.0f}s", flush=True)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print("saved", out, len(rows))


if __name__ == "__main__":
    main()
