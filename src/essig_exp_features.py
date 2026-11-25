"""Essig IFC (Dryad 10.5061/dryad.ht76hdrk7): feature extraction for one experiment zip (exp2 / exp3 / exp4).

Reads the .h5 files straight from the zip (nothing unpacked). For every cell file:
    - expert-labelled cells (h5 key 'label')            -> always kept (features computed)
    - unlabelled cells                                   -> random sample of --per-group per (donor, condition), seed 42
Features: src.pilot_essig_features.cell_features (all channels; the models use only BF_*; 'Live-Dead_mean' is kept to build
a stain-derived live/dead label when an experiment has no expert labels, see src/essig_cross_exp.py).

Checkpointing: rows are appended to <out>.partial.csv every --flush cells; a rerun skips files already done.
Disk: the zip is NOT deleted; remove it yourself after the CSV is complete (summary printed at the end).

Usage: python -I src/essig_exp_features.py --zip D:/.../exp2.zip --exp exp2
       (output: results/essig-exps/<exp>_features.csv + <exp>_summary.json)
"""
import argparse
import io
import json
import random
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import h5py
import pandas as pd

from src.pilot_essig_features import cell_features


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--exp", required=True, help="experiment name, e.g. exp2")
    ap.add_argument("--per-group", type=int, default=400, help="unlabelled cells sampled per (donor, condition)")
    ap.add_argument("--out-dir", default="results/essig-exps")
    ap.add_argument("--flush", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--limit", type=int, default=0, help="debug: stop after N files scanned")
    a = ap.parse_args()

    out_dir = Path(a.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    out, partial = out_dir / f"{a.exp}_features.csv", out_dir / f"{a.exp}_features.partial.csv"
    done = set(pd.read_csv(partial, usecols=["file"]).file) if partial.exists() else set()

    z = zipfile.ZipFile(a.zip)
    names = sorted(n for n in z.namelist() if n.endswith(".h5"))
    groups = {}
    for n in names:
        p = n.split("/")
        groups.setdefault((p[1], p[2]), []).append(n)
    rng = random.Random(a.seed)
    sampled = {n for g in sorted(groups) for n in rng.sample(groups[g], min(a.per_group, len(groups[g])))}
    print(f"{a.exp}: {len(names)} cell files, {len(groups)} donor x condition groups, {len(sampled)} sampled; "
          f"{len(done)} already done", flush=True)

    buf, n_lab, labels, t0 = [], 0, Counter(), time.time()
    for i, n in enumerate(names):
        if a.limit and i >= a.limit:
            break
        if n in done:
            continue
        with z.open(n) as fh, h5py.File(io.BytesIO(fh.read()), "r") as h:
            lab = h["label"][()] if "label" in h else None
            if lab is None and n not in sampled:
                continue
            img, mask = h["image"][()], h["mask"][()]
        lab = (lab.decode() if isinstance(lab, bytes) else str(lab)) if lab is not None else ""
        p = n.split("/")
        row = {"file": n, "exp": a.exp, "donor": p[1], "condition": p[2], "expert_label": lab,
               "in_random_sample": n in sampled}
        row.update(cell_features(img, mask))
        buf.append(row)
        if lab:
            n_lab += 1; labels[lab] += 1
        if len(buf) >= a.flush:
            pd.DataFrame(buf).to_csv(partial, mode="a", header=not partial.exists(), index=False); buf = []
        if i % 5000 == 0:
            print(f"  scanned {i}/{len(names)}, labelled {n_lab}, {time.time() - t0:.0f}s", flush=True)
    if buf:
        pd.DataFrame(buf).to_csv(partial, mode="a", header=not partial.exists(), index=False)

    df = pd.read_csv(partial).drop_duplicates("file")
    df.to_csv(out, index=False)
    summ = {"exp": a.exp, "zip": str(a.zip), "n_cell_files": len(names), "rows": len(df),
            "donors": sorted(df.donor.unique().tolist()), "conditions": sorted(df.condition.unique().tolist()),
            "expert_labels": df.expert_label.fillna("").replace("", "(none)").value_counts().to_dict(),
            "per_donor": df.groupby("donor").size().to_dict(), "minutes": round((time.time() - t0) / 60, 1)}
    (out_dir / f"{a.exp}_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    if not a.limit:
        partial.unlink()
    print(json.dumps(summ, indent=1))
    print(f"selesai -> {out}. Zip boleh dihapus setelah CSV dicek.")


if __name__ == "__main__":
    main()
