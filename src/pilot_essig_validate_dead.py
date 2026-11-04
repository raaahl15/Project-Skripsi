"""Pilot (Essig exp1): validate 'dead from brightfield' on expert labels.

(a) Agreement of the Live-Dead Otsu label (threshold from pilot_essig_classify) with expert Dead_Cell
    vs expert live T cells (T_cell + T_cell_with_signaling).
(b) Brightfield-only, leave-one-donor-out: expert live T cell vs expert Dead_Cell.
    Also ALL-channels for reference.

Usage: python -m src.pilot_essig_validate_dead [--thr 3.006]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

from src.pilot_essig_classify import lodo

LIVE = ["T_cell", "T_cell_with_signaling"]
DEAD = ["Dead_Cell"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="results/pilot-essig/features_labeled.csv")
    ap.add_argument("--thr", type=float, default=3.006)
    ap.add_argument("--n-perm", type=int, default=50)
    a = ap.parse_args()
    df = pd.read_csv(a.csv)
    df = df[df["expert_label"].isin(LIVE + DEAD)].reset_index(drop=True)
    y = df["expert_label"].isin(DEAD).astype(int).to_numpy()
    meta = ["file", "donor", "condition", "expert_label"]
    feats = [c for c in df.columns if c not in meta]
    bf = [c for c in feats if c.startswith("BF_") or c in ("img_h", "img_w")]
    otsu = (np.log1p(np.clip(df["Live-Dead_mean"].to_numpy(), 0, None)) > a.thr).astype(int)
    cm = confusion_matrix(y, otsu)
    res = {
        "n": {"live_T": int((y == 0).sum()), "dead": int(y.sum())},
        "per_donor": df.assign(dead=y).groupby(["donor", "dead"]).size().astype(int).to_dict().__repr__(),
        "otsu_vs_expert": {"confusion[expert][otsu]": cm.tolist(),
                            "agreement": round(float((otsu == y).mean()), 3),
                            "cohen_kappa": round(float(cohen_kappa_score(y, otsu)), 3)},
        "BF_only": lodo(df[bf], y, df["donor"].to_numpy(), True, a.n_perm),
        "ALL": lodo(df[feats], y, df["donor"].to_numpy(), True, 0),
    }
    out = Path(a.csv).with_name("metrics_dead_expert.json")
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
