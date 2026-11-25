"""Essig: live vs dead T cells from BRIGHTFIELD features across experiments (exp1 + exp2..exp4).

Labels per experiment:
    expert : h5 'label' (T_cell / T_cell_with_signaling = live, Dead_Cell = dead) when present
    stain  : Live-Dead channel, log1p(Live-Dead_mean) > Otsu threshold computed on that experiment's random sample
             (exp1: expert vs stain agreement was AUC 0.99). Used only for experiments without enough expert labels;
             agreement with expert labels is reported wherever both exist.
Features: the 19 BF_* features only (the Live-Dead channel defines the label and is never a model input).

Evaluation (same protocol and metrics as WO-15: src/wo15_metrics.evaluate; LogReg / RF / SVM; inner 3-fold GridSearch):
    A. train exp1 -> test each other experiment (new experiment AND new donors)
    B. leave-one-experiment-out over all experiments
    C. leave-one-donor-out over all donors
Output: results/essig-exps/cross_exp_summary.csv, cross_exp_metrics.json, label_agreement.json, combined_labeled.csv

Usage: python -I src/essig_cross_exp.py [--min-expert 100]
"""
import argparse
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from skimage.filters import threshold_otsu
from sklearn.metrics import cohen_kappa_score, roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut

from src.wo14_kfold_heidata import models
from src.wo15_metrics import METRICS, evaluate

LIVE, DEAD = ["T_cell", "T_cell_with_signaling"], ["Dead_Cell"]
OUT = Path("results/essig-exps")


def stain_score(df):
    return np.log1p(np.clip(df["Live-Dead_mean"].to_numpy(float), 0, None))


def load(min_expert, out):
    frames, agree = [], {}
    e1 = pd.read_csv("results/pilot-essig/features_labeled.csv").assign(exp="exp1")
    e1_all = pd.read_csv("results/pilot-essig/features.csv").assign(exp="exp1")  # random sample (stain threshold)
    sources = {"exp1": (e1, e1_all)}
    for f in sorted(out.glob("exp*_features.csv")):
        d = pd.read_csv(f, keep_default_na=False)
        sources[d.exp.iat[0]] = (d[d.expert_label != ""], d[d.in_random_sample.astype(str) == "True"])
    for exp, (lab, rnd) in sources.items():
        thr = float(threshold_otsu(stain_score(rnd))) if len(rnd) else np.nan
        ex = lab[lab.expert_label.isin(LIVE + DEAD)].copy()
        info = {"n_expert_live": int(ex.expert_label.isin(LIVE).sum()), "n_expert_dead": int(ex.expert_label.isin(DEAD).sum()),
                "stain_threshold_log1p": round(thr, 3)}
        if len(ex) and ex.expert_label.isin(DEAD).any() and ex.expert_label.isin(LIVE).any():
            ye, s = ex.expert_label.isin(DEAD).astype(int), stain_score(ex)
            info.update(stain_auc_vs_expert=round(roc_auc_score(ye, s), 3),
                        stain_kappa_vs_expert=round(cohen_kappa_score(ye, (s > thr).astype(int)), 3))
        if len(ex) >= min_expert:
            ex["y"], ex["label_source"] = ex.expert_label.isin(DEAD).astype(int), "expert"
            frames.append(ex)
        else:
            st = rnd.copy(); st["y"], st["label_source"] = (stain_score(st) > thr).astype(int), "stain"
            frames.append(st)
        agree[exp] = {**info, "label_source": frames[-1].label_source.iat[0], "n_used": int(len(frames[-1])),
                      "n_dead_used": int(frames[-1].y.sum())}
    df = pd.concat(frames, ignore_index=True)
    df["donor_id"] = df.exp + "/" + df.donor.astype(str)
    return df, agree


def main():
    warnings.filterwarnings("ignore")
    ap = argparse.ArgumentParser(); ap.add_argument("--min-expert", type=int, default=100)
    ap.add_argument("--out-dir", default=str(OUT)); a = ap.parse_args()
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    df, agree = load(a.min_expert, out)
    (out / "label_agreement.json").write_text(json.dumps(agree, indent=1), encoding="utf-8")
    print(json.dumps(agree, indent=1))
    bf = sorted(c for c in df.columns if c.startswith("BF_"))
    df[["file", "exp", "donor_id", "label_source", "y"] + bf].to_csv(out / "combined_labeled.csv", index=False)
    X, y = df[bf].to_numpy(float), df.y.to_numpy()
    exps, donors = df.exp.to_numpy(), df.donor_id.to_numpy()
    schemes = {}
    tr1 = np.where(exps == "exp1")[0]
    for e in sorted(set(exps) - {"exp1"}):
        schemes[f"A_train-exp1_test-{e}"] = [(tr1, np.where(exps == e)[0])]
    if len(set(exps)) > 1:
        schemes["B_leave-one-experiment-out"] = list(LeaveOneGroupOut().split(X, y, exps))
    schemes["C_leave-one-donor-out"] = list(LeaveOneGroupOut().split(X, y, donors))
    rows, full = [], {"labels": agree, "n": int(len(y)), "features": bf, "schemes": {}}
    for sname, sp in schemes.items():
        full["schemes"][sname] = {}
        for mname, (model, grid) in models().items():
            r = evaluate(model, grid, X, y, sp, 0.90)
            full["schemes"][sname][mname] = r
            for op, rr in r.items():
                row = {"scheme": f"{sname} ({len(sp)} fold)", "model": mname, "threshold": op}
                row.update({m: rr["per_fold_mean_sd"][m]["mean"] for m in METRICS})
                row["cm_pooled[[TN,FP],[FN,TP]]"] = rr["pooled"]["cm"]
                rows.append(row)
            d = r["default"]["per_fold_mean_sd"]
            print(f"{sname:32s} {mname:6s} AUC={d['roc_auc']['mean']} rec={d['recall']['mean']} spec={d['specificity']['mean']} "
                  f"MCC={d['mcc']['mean']}", flush=True)
    pd.DataFrame(rows).to_csv(out / "cross_exp_summary.csv", index=False)
    (out / "cross_exp_metrics.json").write_text(json.dumps(full, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
