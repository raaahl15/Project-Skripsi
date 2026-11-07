"""Analyses for Bimbingan 6 (9 Nov 2026).

Part A (heiDATA, HIV exposure): per-feature effect size computed WITHIN each figure/experiment
    (+Vpx vs -Vpx, and HIV-exposed vs Mock where a figure has Mock), then checked for sign consistency
    across experiments. No ML: answers "which physical feature changes the same way in every experiment?"
    Also a sanity check of the HIV-1 capsid (CA) puncta count per condition.

Part B (Essig IFC, live vs dead): the WO-14 protocol (LogReg/RF/SVM, inner 3-fold GridSearch = validation,
    outer folds = testing) on expert-labelled live T cells vs Dead_Cell, using brightfield features only.
    Outer schemes: k-fold 5 per cell vs leave-one-donor-out (grouped). Feature sets: brightfield with and
    without image-size features (img_h, img_w).

Usage:
    python src/b6_analyses.py
"""
import json
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.model_selection import LeaveOneGroupOut, StratifiedKFold

from src.pilot_heidata_classify import LAMIN_FEATS
from src.wo14_kfold_heidata import models, run

SEED = 42
OUT = Path("results/b6")
LIVE, DEAD = ["T_cell", "T_cell_with_signaling"], ["Dead_Cell"]


def cohen_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp if sp > 0 else np.nan


def part_a():
    df = pd.read_csv("results/pilot-heidata/cells.csv")
    comps = {"+Vpx_vs_-Vpx": ("+Vpx", "-Vpx"), "HIV_vs_Mock": (None, "Mock")}
    rows = []
    for cname, (pos, neg) in comps.items():
        for fig, d in df.groupby("figure"):
            a = d[d.condition == pos] if pos else d[d.condition != "Mock"]
            b = d[d.condition == neg]
            if len(a) < 3 or len(b) < 3:
                continue
            for f in LAMIN_FEATS:
                p = mannwhitneyu(a[f], b[f]).pvalue
                rows.append({"comparison": cname, "figure": fig, "n_pos": len(a), "n_neg": len(b), "feature": f,
                             "cohen_d": round(cohen_d(a[f], b[f]), 2), "mw_p": round(p, 4)})
    es = pd.DataFrame(rows)
    es.to_csv(OUT / "A_effect_size_per_figure.csv", index=False)

    summ = []
    for (cname, f), g in es.groupby(["comparison", "feature"]):
        d = g.cohen_d.dropna()
        sign = np.sign(d.median())
        summ.append({"comparison": cname, "feature": f, "n_figures": len(d), "median_d": round(d.median(), 2),
                     "same_sign": int((np.sign(d) == sign).sum()), "n_sig_p<0.05": int((g.mw_p < 0.05).sum()),
                     "min_d": d.min(), "max_d": d.max()})
    summ = pd.DataFrame(summ)
    summ["abs_median_d"] = summ.median_d.abs()
    summ = summ.sort_values(["comparison", "abs_median_d"], ascending=[True, False]).drop(columns="abs_median_d")
    summ.to_csv(OUT / "A_effect_size_consistency.csv", index=False)

    piv = es[es.comparison == "+Vpx_vs_-Vpx"].pivot(index="feature", columns="figure", values="cohen_d")
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(piv.values, cmap="RdBu_r", vmin=-1.5, vmax=1.5)
    ax.set_xticks(range(piv.shape[1]), piv.columns)
    ax.set_yticks(range(piv.shape[0]), piv.index)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            ax.text(j, i, f"{piv.values[i, j]:.1f}", ha="center", va="center", fontsize=7)
    ax.set_title("Cohen's d (+Vpx - -Vpx) per percobaan", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(OUT / "A_effect_size_heatmap.png", dpi=130)
    plt.close(fig)

    ca = df[df.ca_puncta_nucleus.notna()].groupby(["figure", "condition"]).agg(
        n=("ca_puncta_nucleus", "size"), ca_nucleus_median=("ca_puncta_nucleus", "median"),
        ca_perinuclear_median=("ca_puncta_perinuclear", "median")).reset_index()
    ca.to_csv(OUT / "A_capsid_sanity.csv", index=False)
    return summ, ca


def part_b():
    df = pd.read_csv("results/pilot-essig/features_labeled.csv")
    df = df[df.expert_label.isin(LIVE + DEAD)].reset_index(drop=True)
    y = df.expert_label.isin(DEAD).astype(int).to_numpy()
    donors = df.donor.to_numpy()
    bf = [c for c in df.columns if c.startswith("BF_")]
    sets = {"BF_tanpa_ukuran_citra": bf, "BF_dengan_ukuran_citra": bf + ["img_h", "img_w"]}
    res, rows = {"n_live": int((y == 0).sum()), "n_dead": int(y.sum()),
                 "per_donor": {f"{k[0]}_dead={k[1]}": int(v)
                               for k, v in df.assign(dead=y).groupby(["donor", "dead"]).size().items()},
                 "feature_sets": {k: v for k, v in sets.items()}, "results": {}}, []
    for sname, feats in sets.items():
        X = df[feats].to_numpy(float)
        schemes = {"kfold5_per_sel": list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y)),
                   "leave_one_donor_out": list(LeaveOneGroupOut().split(X, y, donors))}
        res["results"][sname] = {}
        for sch, splits in schemes.items():
            res["results"][sname][sch] = {}
            for mname, (model, grid) in models().items():
                r = run(model, grid, X, y, splits)
                res["results"][sname][sch][mname] = r
                rows.append({"feature_set": sname, "scheme": sch, "model": mname,
                             "auc_mean": r["roc_auc"]["mean"], "auc_sd": r["roc_auc"]["sd"],
                             "bacc_mean": r["balanced_accuracy"]["mean"], "f1_mean": r["f1"]["mean"]})
                print(sname, sch, mname, r["roc_auc"], flush=True)

    # univariate effect size per BF feature (dead - live), per donor, for interpretation
    eff = []
    for f in bf:
        eff.append({"feature": f, **{f"d_{dn}": round(cohen_d(df.loc[(donors == dn) & (y == 1), f],
                                                               df.loc[(donors == dn) & (y == 0), f]), 2)
                                    for dn in sorted(set(donors))}})
    eff = pd.DataFrame(eff)
    eff["abs_mean"] = eff.filter(like="d_").abs().mean(axis=1)
    eff.sort_values("abs_mean", ascending=False).to_csv(OUT / "B_effect_size_bf.csv", index=False)
    (OUT / "B_metrics.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    summ = pd.DataFrame(rows)
    summ.to_csv(OUT / "B_summary.csv", index=False)
    return summ


def main():
    warnings.filterwarnings("ignore")
    OUT.mkdir(parents=True, exist_ok=True)
    a, ca = part_a()
    print(a.to_string())
    print(ca.to_string())
    b = part_b()
    print(b.to_string())


if __name__ == "__main__":
    main()
