"""WO-15: full evaluation metrics + confusion matrices for the existing classification tasks (arahan Bimbingan 6).

Same protocol as WO-14 (src/wo14_kfold_heidata.py): outer folds = testing, inner StratifiedKFold(3) GridSearchCV on the
training part = validation (hyperparameter choice, scoring ROC AUC). Models: LogReg, RF, SVM (class_weight="balanced").

Positive class (label 1) = the condition we must NOT miss:
    heiDATA  : HIV-exposed cell (+Vpx or -Vpx)   vs  Mock
    Essig    : dead cell                         vs  live T cell
So FN = a positive cell called negative (missed infection / missed dead cell), FP = a false alarm.

Metrics per outer fold (mean +- sd over folds) and on the pooled out-of-fold predictions:
    accuracy, balanced accuracy, precision (PPV), recall (= sensitivity, TPR), specificity (TNR), NPV, F1, F2,
    MCC, ROC AUC, PR AUC (average precision), confusion matrix [[TN, FP], [FN, TP]].
Class predictions use each model's default threshold (LogReg/RF: p = 0.5; SVM: decision = 0).
Operating points: inside every outer fold the threshold reaching recall >= 0.90 on the TRAINING out-of-fold scores
(inner 3-fold) is chosen and applied to the test fold -> "recall90" rows (no threshold tuned on test data).

Usage: python -I src/wo15_metrics.py            (config: configs/wo15_metrics.yaml)
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
import yaml
from sklearn.base import clone
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, fbeta_score, matthews_corrcoef, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import (GridSearchCV, LeaveOneGroupOut, StratifiedGroupKFold, StratifiedKFold,
                                     cross_val_predict)

from src.pilot_heidata_classify import CA_FEATS, LAMIN_FEATS
from src.wo14_kfold_heidata import models

CFG = yaml.safe_load(Path("configs/wo15_metrics.yaml").read_text(encoding="utf-8"))
SEED = CFG["seed"]
OUT = Path(CFG["out"])
METRICS = ["accuracy", "balanced_accuracy", "precision", "recall", "specificity", "npv", "f1", "f2", "mcc",
           "roc_auc", "pr_auc"]


def scores(est, X):
    return est.decision_function(X) if hasattr(est, "decision_function") else est.predict_proba(X)[:, 1]


def default_threshold(est):
    return 0.0 if hasattr(est, "decision_function") else 0.5


def metric_set(y, pred, s):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    both = len(set(y)) == 2
    sd = lambda a, b: round(float(a / (a + b)), 3) if (a + b) else None  # noqa: E731
    return {"accuracy": round(accuracy_score(y, pred), 3),
            "balanced_accuracy": round(balanced_accuracy_score(y, pred), 3) if both else None,
            "precision": round(precision_score(y, pred, zero_division=0), 3) if (tp + fp) else None,
            "recall": sd(tp, fn), "specificity": sd(tn, fp), "npv": sd(tn, fn),
            "f1": round(f1_score(y, pred, zero_division=0), 3), "f2": round(fbeta_score(y, pred, beta=2, zero_division=0), 3),
            "mcc": round(matthews_corrcoef(y, pred), 3) if both else None,
            "roc_auc": round(roc_auc_score(y, s), 3) if both else None,
            "pr_auc": round(average_precision_score(y, s), 3) if both else None,
            "cm": [[int(tn), int(fp)], [int(fn), int(tp)]]}


def threshold_for_recall(y, s, target):
    """Highest threshold whose recall on (y, s) is >= target."""
    pos = np.sort(s[y == 1])[::-1]
    if len(pos) == 0:
        return np.inf
    k = int(np.ceil(target * len(pos))) - 1
    return float(pos[max(k, 0)])


def evaluate(model, grid, X, y, splits, recall_target):
    inner = StratifiedKFold(CFG["inner_k"], shuffle=True, random_state=SEED)
    folds = {"default": [], "recall90": []}
    pooled = {k: {"y": [], "pred": []} for k in folds}
    oof_rank = np.full(len(y), np.nan)
    for tr, te in splits:
        search = GridSearchCV(model, grid, scoring="roc_auc", cv=inner, error_score=np.nan).fit(X[tr], y[tr])
        best = search.best_estimator_
        s_te = scores(best, X[te])
        # threshold for recall target, chosen on inner out-of-fold scores of the training part only
        s_tr = cross_val_predict(clone(best), X[tr], y[tr], cv=inner,
                                 method="decision_function" if hasattr(best, "decision_function") else "predict_proba")
        s_tr = s_tr if s_tr.ndim == 1 else s_tr[:, 1]
        thr = {"default": default_threshold(best), "recall90": threshold_for_recall(y[tr], s_tr, recall_target)}
        for k, t in thr.items():
            pred = (s_te >= t).astype(int)
            m = metric_set(y[te], pred, s_te)
            m.update({"n_test": int(len(te)), "threshold": round(t, 4), "best_params": search.best_params_})
            folds[k].append(m)
            pooled[k]["y"].append(y[te]); pooled[k]["pred"].append(pred)
        # rank-normalised scores so pooled ROC AUC is not distorted by fold-specific score scales
        oof_rank[te] = pd.Series(s_te).rank(pct=True).to_numpy()
    out = {}
    for k in folds:
        agg = {}
        for mname in METRICS:
            v = [f[mname] for f in folds[k] if f[mname] is not None]
            agg[mname] = {"mean": round(float(np.mean(v)), 3) if v else None,
                          "sd": round(float(np.std(v, ddof=1)), 3) if len(v) > 1 else None, "n_folds": len(v)}
        yy, pp = np.concatenate(pooled[k]["y"]), np.concatenate(pooled[k]["pred"])
        out[k] = {"per_fold_mean_sd": agg, "pooled": metric_set(yy, pp, oof_rank), "folds": folds[k]}
    return out


def load_task(name, spec):
    if spec["dataset"] == "heidata":
        df = pd.read_csv("results/pilot-heidata/cells.csv")
        if spec.get("figures"):
            df = df[df.figure.isin(spec["figures"])]
        if spec.get("conditions"):
            df = df[df.condition.isin(spec["conditions"])]
        feats = {"CA": CA_FEATS, "Lamin": LAMIN_FEATS, "CA+Lamin": CA_FEATS + LAMIN_FEATS}[spec["features"]]
        df = df.dropna(subset=CA_FEATS) if "CA" in spec["features"] else df
        df = df.reset_index(drop=True)
        y = df.condition.isin(spec["positive"]).astype(int).to_numpy()
        return df[feats].to_numpy(float), y, df.figure.to_numpy()
    df = pd.read_csv("results/pilot-essig/features_labeled.csv")
    live, dead = ["T_cell", "T_cell_with_signaling"], ["Dead_Cell"]
    df = df[df.expert_label.isin(live + dead)].reset_index(drop=True)
    bf = [c for c in df.columns if c.startswith("BF_")]
    return df[bf].to_numpy(float), df.expert_label.isin(dead).astype(int).to_numpy(), df.donor.to_numpy()


def splits_for(scheme, X, y, g):
    if scheme == "group":
        return list(LeaveOneGroupOut().split(X, y, g)) if len(set(g)) <= 5 else \
            list(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(X, y, g))
    return list(StratifiedKFold(int(scheme.replace("kfold", "")), shuffle=True, random_state=SEED).split(X, y))


def main():
    warnings.filterwarnings("ignore")
    OUT.mkdir(parents=True, exist_ok=True)
    res, rows = {"config": CFG}, []
    for tname, spec in CFG["tasks"].items():
        X, y, g = load_task(tname, spec)
        res[tname] = {"description": spec["description"], "n": int(len(y)), "n_positive": int(y.sum()),
                      "groups": sorted(set(map(str, g))), "schemes": {}}
        for scheme in spec["schemes"]:
            sp = splits_for(scheme, X, y, g)
            res[tname]["schemes"][scheme] = {}
            for mname, (model, grid) in models().items():
                r = evaluate(model, grid, X, y, sp, CFG["recall_target"])
                res[tname]["schemes"][scheme][mname] = r
                for op, rr in r.items():
                    row = {"task": tname, "scheme": f"{scheme} ({len(sp)} fold)", "model": mname, "threshold": op}
                    row.update({m: rr["per_fold_mean_sd"][m]["mean"] for m in METRICS})
                    row.update({f"{m}_sd": rr["per_fold_mean_sd"][m]["sd"] for m in ["recall", "specificity", "f1", "roc_auc"]})
                    row["cm_pooled[[TN,FP],[FN,TP]]"] = rr["pooled"]["cm"]
                    rows.append(row)
                d = r["default"]["per_fold_mean_sd"]
                print(f"{tname:22s} {scheme:7s} {mname:6s} AUC={d['roc_auc']['mean']} rec={d['recall']['mean']} "
                      f"spec={d['specificity']['mean']} F1={d['f1']['mean']} cm={r['default']['pooled']['cm']}", flush=True)
    (OUT / "metrics_full.json").write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    summary = pd.DataFrame(rows)
    summary.to_csv(OUT / "summary_metrics.csv", index=False)
    plot_cms(res)


def plot_cms(res):
    """Pooled confusion matrices (default threshold) for the best-MCC model of each task x scheme (AUC can tie)."""
    cells = [(t, s, r) for t in CFG["tasks"] for s, r in res[t]["schemes"].items()]
    fig, axes = plt.subplots(1, len(cells), figsize=(3.1 * len(cells), 3.4))
    for ax, (t, s, r) in zip(np.atleast_1d(axes), cells):
        mname = max(r, key=lambda m: (r[m]["default"]["per_fold_mean_sd"]["mcc"]["mean"] or -1,
                                      r[m]["default"]["per_fold_mean_sd"]["roc_auc"]["mean"] or 0))
        cm = np.array(r[mname]["default"]["pooled"]["cm"])
        ax.imshow(cm, cmap="Blues")
        for (i, j), v in np.ndenumerate(cm):
            ax.text(j, i, str(v), ha="center", va="center", fontsize=11,
                    color="white" if v > cm.max() / 2 else "black")
        neg, pos = CFG["tasks"][t]["labels"]
        ax.set_xticks([0, 1], [neg, pos], fontsize=7); ax.set_yticks([0, 1], [neg, pos], fontsize=7)
        ax.set_xlabel("Prediksi", fontsize=8); ax.set_ylabel("Sebenarnya", fontsize=8)
        ax.set_title(f"{t}\n{s}, {mname}", fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "confusion_matrices.png", dpi=130)


if __name__ == "__main__":
    main()
