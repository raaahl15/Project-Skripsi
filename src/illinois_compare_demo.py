"""Compare own trajectories (demo well K16) with the authors' (NIS Elements) for the same well.

Per-cell features = src.pilot_illinois FEATS (cell-own intensity descriptors). Compares (a) all own complete tracks,
(b) own tracks restricted to the authors' brightness range (mean >= authors' 5th percentile of cell means).
Usage: python -I src/illinois_compare_demo.py <own_traj_csv> <intensityTrajectories.zip> <out_json>
"""
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pilot_illinois import FEATS, features  # noqa: E402


def main(own_csv, traj_zip, out_json):
    own = pd.read_csv(own_csv, index_col=0).to_numpy(float)
    auth = pd.read_csv(io.BytesIO(zipfile.ZipFile(traj_zip).read("DiversitySet3Plate2/WellK16.csv")), header=None).to_numpy(float)
    Fa = features(auth, auth)[FEATS]
    Fo = features(own, own)[FEATS]
    thr = np.percentile(auth.mean(1), 5)
    Fb = Fo[Fo.I_mean >= thr]
    res = {"n_authors": len(Fa), "n_own_all": len(Fo), "n_own_bright": len(Fb), "bright_threshold_I_mean": round(float(thr), 1),
           "features": {}}
    for c in FEATS:
        res["features"][c] = {"authors_median": round(float(Fa[c].median()), 3),
                              "own_all_median": round(float(Fo[c].median()), 3),
                              "own_bright_median": round(float(Fb[c].median()), 3),
                              "ks_p_bright_vs_authors": round(float(ks_2samp(Fa[c], Fb[c]).pvalue), 3)}
    Path(out_json).write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
