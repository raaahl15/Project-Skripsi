"""Feature extraction entry points for the final run (Colab). Essig and heiDATA reuse the tested pilot extractors:
    Essig   : python -I src/essig_exp_features.py --zip <expN.zip> --exp expN --out-dir <Drive>/data/processed/essig
    heiDATA : python -I src/pilot_heidata_features.py --root <heidata dir> --out <Drive>/data/processed/heidata
Illinois (this module): ALL cells of the control wells of all plates (the pilots capped 20 cells per well).

Usage: python -m src.final.features illinois --root <dir with intensityTrajectories.zip, noiseTrajectories.zip> \
           --out <Drive>/data/processed/illinois/cells_controls_all.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np


def illinois(root: Path, out: Path) -> None:
    from src.pilot_illinois import load
    df = load(root, cap=None).replace([np.inf, -np.inf], np.nan)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    summ = {"cells": int(len(df)), "wells": int(df.well.nunique()), "plates": sorted(df.plate.unique().tolist()),
            "per_condition": df.condition.value_counts().to_dict()}
    out.with_suffix(".summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", choices=["illinois"])
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    illinois(Path(a.root), Path(a.out))


if __name__ == "__main__":
    main()
