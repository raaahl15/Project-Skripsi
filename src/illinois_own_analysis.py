"""Illinois Plate 2: classification from OUR OWN image extraction (results/illinois-own/, src/illinois_zip_parts.py).

Only one well per positive class (B01 TNF, A24 Alp; untreated A23 + B02), so grouped-by-well folds are impossible.
    1. k-fold 5 per cell on own features (WO-15 protocol/metrics)          -> within-plate, optimistic upper bound
    2. own vs authors' features for the SAME wells: univariate ROC AUC per feature (direction & size)
    3. transfer: train on the AUTHORS' features of the 6 other plates (cap 20 cells/well), test on OUR cells of Plate 2;
       scale-free features only (I_cv, I_fold, I_ac1, I_resid_std/I_mean, I_slope/I_mean) because our absolute intensity
       is lower than the authors' (different ROI/background, see results/pilot-illinois/demo/README.md)
Output: results/skenario-b7/illinois-own/{summary.csv, univariate_auc.csv, report.json}
Usage: python -I src/illinois_own_analysis.py
"""
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from src.pilot_illinois import FEATS, load as load_authors
from src.wo14_kfold_heidata import models
from src.wo15_metrics import METRICS, evaluate

OUT = Path("results/skenario-b7/illinois-own"); SEED = 42
TASKS = {"TNF_vs_untreated": ("TNF", "untreated"), "Alp_vs_untreated": ("Alp", "untreated")}


def scale_free(df):
    return pd.DataFrame({"I_cv": df.I_cv, "I_fold": df.I_fold, "I_ac1": df.I_ac1,
                         "resid_rel": df.I_resid_std / df.I_mean, "slope_rel": df.I_slope / df.I_mean})


def main():
    warnings.filterwarnings("ignore"); OUT.mkdir(parents=True, exist_ok=True)
    own = pd.concat([pd.read_csv(f) for f in sorted(Path("results/illinois-own").glob("*.csv"))], ignore_index=True)
    auth = load_authors(Path("data/raw/illinois-IDB-8103861"), 20)
    plate2 = own.plate.iat[0]
    auth_same = auth[auth.well.isin(own.well.unique())]
    auth_other = auth[auth.plate != plate2]
    rows, uni, rep = [], [], {"n_own": own.groupby(["well", "condition"]).size().reset_index().values.tolist(),
                              "n_authors_same_wells": auth_same.groupby("well").size().to_dict(), "plate": plate2}
    for tname, (pos, neg) in TASKS.items():
        o = own[own.condition.isin([pos, neg])].reset_index(drop=True)
        y = o.condition.eq(pos).astype(int).to_numpy()
        # 1. k-fold per cell, own features
        sp = list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(o, y))
        # 3. transfer authors(other plates) -> own(plate 2), scale-free features
        a = auth_other[auth_other.condition.isin([pos, neg])].reset_index(drop=True)
        ya = a.condition.eq(pos).astype(int).to_numpy()
        Xt = pd.concat([scale_free(a), scale_free(o)], ignore_index=True).to_numpy(float)
        yt = np.concatenate([ya, y]); tr, te = np.arange(len(a)), np.arange(len(a), len(a) + len(o))
        for sname, X, yy, splits in (("kfold5 per sel (fitur sendiri, 9 fitur)", o[FEATS].to_numpy(float), y, sp),
                                     ("transfer penulis 6 plate -> sendiri Plate 2 (5 fitur bebas skala)", Xt, yt, [(tr, te)])):
            for mname, (model, grid) in models().items():
                r = evaluate(model, grid, X, yy, splits, 0.90)["default"]
                row = {"task": tname, "scheme": sname, "model": mname}
                row.update({m: r["per_fold_mean_sd"][m]["mean"] for m in METRICS}); row["cm_pooled"] = r["pooled"]["cm"]
                rows.append(row)
                print(f"{tname:17s} {sname[:40]:40s} {mname:6s} AUC={row['roc_auc']} rec={row['recall']} spec={row['specificity']} MCC={row['mcc']}", flush=True)
        # 2. univariate AUC, own vs authors, same wells
        s = auth_same[auth_same.condition.isin([pos, neg])]
        ys = s.condition.eq(pos).astype(int)
        for f in FEATS:
            uni.append({"task": tname, "feature": f, "auc_own": round(roc_auc_score(y, o[f]), 3),
                        "auc_authors_same_wells": round(roc_auc_score(ys, s[f]), 3) if ys.nunique() == 2 else None,
                        "median_own_pos": round(float(o[f][y == 1].median()), 3), "median_own_neg": round(float(o[f][y == 0].median()), 3)})
    pd.DataFrame(rows).to_csv(OUT / "summary.csv", index=False)
    u = pd.DataFrame(uni); u.to_csv(OUT / "univariate_auc.csv", index=False)
    v = u.dropna()
    rep["univariate_direction_agreement"] = {t: f"{int(((g.auc_own - .5) * (g.auc_authors_same_wells - .5) > 0).sum())}/{len(g)}"
                                             for t, g in v.groupby("task")}
    rep["univariate_corr_own_vs_authors"] = {t: round(float(np.corrcoef(g.auc_own, g.auc_authors_same_wells)[0, 1]), 3)
                                             for t, g in v.groupby("task")}
    (OUT / "report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(u.to_string(index=False)); print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
