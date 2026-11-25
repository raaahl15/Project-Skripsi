"""B7 figure: k-fold per cell vs grouped folds - schematic (A) and ROC AUC of both schemes for every task (B).

Numbers come from results/wo15-metrics/summary_metrics.csv and results/skenario-b7/illinois-metrics/summary_metrics.csv
(default threshold; per scheme the BEST of LogReg / RF / SVM by mean ROC AUC over the outer folds).
Usage: python -I src/b7_figures.py  ->  results/b7/split_schemes.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path("results/b7"); OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE = "#2a78d6", "#eb6834"          # validated categorical slots 1-2 (dataviz reference palette)
INK, INK2, GRID, LIGHT = "#0b0b0b", "#52514e", "#e6e5e1", "#d9d8d3"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2})

TASKS = [  # (label, csv, task id)
    ("heiDATA\nHIV vs Mock\n(Lamin B1)", "results/wo15-metrics/summary_metrics.csv", "A_lamin_hiv_vs_mock"),
    ("heiDATA\nHIV vs Mock\n(kapsid)", "results/wo15-metrics/summary_metrics.csv", "A_capsid_hiv_vs_mock"),
    ("Essig\nmati vs hidup", "results/wo15-metrics/summary_metrics.csv", "B_essig_dead_vs_live"),
    ("Illinois\naktif vs laten", "results/skenario-b7/illinois-metrics/summary_metrics.csv", "I_tnf_vs_untreated"),
    ("Illinois\nditekan vs laten", "results/skenario-b7/illinois-metrics/summary_metrics.csv", "I_alp_vs_untreated"),
]


def best_auc(csv, task, scheme_prefix):
    d = pd.read_csv(csv)
    d = d[(d.task == task) & (d.threshold == "default") & d.scheme.str.startswith(scheme_prefix)]
    return float(d.roc_auc.max())


def schematic(ax):
    rng = np.random.default_rng(3)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.4); ax.axis("off")
    for row, (title, y0) in enumerate([("k-fold per sel", 3.5), ("berkelompok (per percobaan)", 0.3)]):
        ax.text(0, y0 + 2.55, title, fontsize=10, color=INK, fontweight="bold")
        for e in range(3):
            x0 = 0.1 + e * 3.3
            ax.add_patch(plt.Rectangle((x0, y0), 3.0, 2.2, fill=False, ec=INK2, lw=0.8))
            ax.text(x0 + 1.5, y0 - 0.25, f"percobaan {e + 1}", ha="center", va="top", fontsize=8, color=INK2)
            pts = rng.uniform([x0 + 0.3, y0 + 0.3], [x0 + 2.7, y0 + 1.9], (14, 2))
            test = (rng.random(14) < 0.25) if row == 0 else np.full(14, e == 2)
            ax.scatter(pts[~test, 0], pts[~test, 1], s=22, c=LIGHT, ec=INK2, lw=0.5)
            ax.scatter(pts[test, 0], pts[test, 1], s=26, c=BLUE if row == 0 else ORANGE, ec="white", lw=0.8)
    ax.text(0, -0.75, "titik berwarna = sel uji, abu-abu = sel latih. Per sel: sel uji dan latih berasal dari percobaan yang sama\n"
            "(kondisi pencitraan sama, bisa dikenali model). Berkelompok: model diuji pada percobaan yang belum pernah dilihat.",
            fontsize=7.5, color=INK2, va="top")


def bars(ax):
    x = np.arange(len(TASKS)); w = 0.36
    per_cell = [best_auc(c, t, "kfold5") for _, c, t in TASKS]
    grouped = [best_auc(c, t, "group") for _, c, t in TASKS]
    ax.axhline(0.5, color=INK2, lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax.text(-0.62, 0.515, "acak (0,5)", fontsize=7.5, color=INK2, ha="left")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
    for vals, off, col, lab in ((per_cell, -w / 2 - 0.01, BLUE, "k-fold 5 per sel"), (grouped, w / 2 + 0.01, ORANGE, "berkelompok")):
        b = ax.bar(x + off, vals, w, color=col, label=lab, zorder=2)
        for rect, v in zip(b, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 0.015, f"{v:.2f}".replace(".", ","), ha="center", fontsize=7.5, color=INK)
    ax.set_xticks(x, [t[0] for t in TASKS], fontsize=7.8)
    ax.set_ylim(0, 1.08); ax.set_ylabel("ROC AUC (model terbaik)")
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=8, ncol=2, bbox_to_anchor=(0, 1.08))
    ax.set_title("Hanya heiDATA (Lamin B1) yang turun drastis bila diuji pada percobaan baru", fontsize=9.5, color=INK, loc="left", pad=18)
    return per_cell, grouped


fig = plt.figure(figsize=(11, 4.6), facecolor="#fcfcfb")
a = fig.add_axes([0.02, 0.18, 0.36, 0.74]); b = fig.add_axes([0.45, 0.2, 0.53, 0.66])
schematic(a); pc, gr = bars(b)
fig.text(0.02, 0.97, "A. Dua cara membagi data uji", fontsize=10.5, fontweight="bold", color=INK, va="top")
fig.text(0.45, 0.97, "B. ROC AUC kedua skema", fontsize=10.5, fontweight="bold", color=INK, va="top")
fig.savefig(OUT / "split_schemes.png", dpi=170)
pd.DataFrame({"task": [t[2] for t in TASKS], "auc_kfold5_per_sel": pc, "auc_berkelompok": gr}).to_csv(OUT / "split_schemes.csv", index=False)
print(pd.read_csv(OUT / "split_schemes.csv"))
