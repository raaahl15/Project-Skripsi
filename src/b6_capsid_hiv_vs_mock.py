"""heiDATA: HIV-exposed vs Mock from optically detected HIV-1 capsid (CA) puncta, validated ACROSS experiments.

Only figures 1G and S3B contain Mock cells and a CA channel. Validation = leave-one-figure-out: train on one
experiment, test on the other (2 folds), inner 3-fold GridSearch for hyperparameters (WO-14 protocol).
CA puncta use the per-figure shared intensity scale (fixed 7 Nov 2026), which is label-free.

Feature sets:
    CA        : ca_puncta_nucleus, ca_puncta_perinuclear
    CA+Lamin  : CA + 11 nuclear morphometry / Lamin B1 features
    Lamin     : 11 Lamin B1 features only (reference)
Also: a no-training rule "infected if >= 1 CA punctum in the nucleus" and a label-permutation test.

Usage: python src/b6_capsid_hiv_vs_mock.py
"""
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold

from src.pilot_heidata_classify import CA_FEATS, LAMIN_FEATS
from src.wo14_kfold_heidata import models, run

SEED = 42
OUT = Path("results/b6")


def main():
    warnings.filterwarnings("ignore")
    df = pd.read_csv("results/pilot-heidata/cells.csv")
    d = df[df.figure.isin(["1G", "S3B"])].reset_index(drop=True)
    y = (d.condition != "Mock").astype(int).to_numpy()
    g = d.figure.to_numpy()
    res = {"tasks": {}}
    res["n"] ={f"{k[0]}_{k[1]}": int(v) for k, v in d.groupby(["figure", "condition"]).size().items()}

    # rule without training
    rule = (d.ca_puncta_nucleus >= 1).astype(int).to_numpy()
    res["rule_nucleus_puncta>=1"] = {
        fig: {"balanced_accuracy": round(balanced_accuracy_score(y[g == fig], rule[g == fig]), 3),
              "confusion[[TN,FP],[FN,TP]]": confusion_matrix(y[g == fig], rule[g == fig]).tolist()}
        for fig in ["1G", "S3B"]}
    res["per_figure_condition_ca_nucleus"] = {f"{k[0]}_{k[1]}": {"median": float(v.median()), "frac_zero": round(float((v == 0).mean()), 2)}
                                             for k, v in d.groupby(["figure", "condition"]).ca_puncta_nucleus}

    rows = []
    sets = {"CA": CA_FEATS, "CA+Lamin": CA_FEATS + LAMIN_FEATS, "Lamin": LAMIN_FEATS}
    rng = np.random.default_rng(SEED)
    for sname, feats in sets.items():
        X = d[feats].to_numpy(float)
        schemes = {"leave_one_figure_out": list(LeaveOneGroupOut().split(X, y, g)),
                   "kfold5_per_sel": list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y))}
        res["tasks"][sname] = {}
        for sch, splits in schemes.items():
            res["tasks"][sname][sch] = {}
            for mname, (model, grid) in models().items():
                r = run(model, grid, X, y, splits)
                if sch == "leave_one_figure_out" and mname == "logreg":
                    perm = []
                    for _ in range(100):
                        perm.append(run(model, {"clf__C": [1]}, X, rng.permutation(y), splits)["pooled_oof_roc_auc"])
                    r["perm_null_mean_pooled_auc"] = round(float(np.mean(perm)), 3)
                    r["perm_p_pooled"] = round(float((1 + np.sum(np.array(perm) >= r["pooled_oof_roc_auc"])) / 101), 3)
                res["tasks"][sname][sch][mname] = r
                fold_auc = [f["roc_auc"] for f in r["folds"]]
                rows.append({"features": sname, "scheme": sch, "model": mname, "auc_mean": r["roc_auc"]["mean"],
                             "fold_auc": fold_auc, "bacc_mean": r["balanced_accuracy"]["mean"],
                             "pooled_auc": r["pooled_oof_roc_auc"], "perm_p": r.get("perm_p_pooled")})
                print(sname, sch, mname, "AUC", r["roc_auc"]["mean"], fold_auc, "bAcc", r["balanced_accuracy"]["mean"],
                      "perm_p", r.get("perm_p_pooled"), flush=True)
    (OUT / "A_capsid_hiv_vs_mock.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    pd.DataFrame(rows).to_csv(OUT / "A_capsid_hiv_vs_mock_summary.csv", index=False)
    print(json.dumps({k: res[k] for k in ["n", "rule_nucleus_puncta>=1", "per_figure_condition_ca_nucleus"]}, indent=1))


if __name__ == "__main__":
    main()
