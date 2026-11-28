"""Bahan B8 (arahan B7: kelas kondisi sel) — dua analisis:

1. ILLINOIS 3 KELAS (laten / aktif-TNF / ditekan-Alp) dalam SATU dataset, fitur lintasan GFP per sel (9 fitur, sama dengan
   skenario B7). Validasi: leave-one-PLATE-out (7 plate = data uji baru) dan k-fold 5 per sel; GridSearch dalam (3-fold,
   skor balanced accuracy) = validasi; LogReg / RF / SVM (class_weight="balanced", dari wo14_kfold_heidata.models()).
   Metrik multikelas: akurasi, balanced accuracy, F1 makro, MCC, ROC AUC makro one-vs-rest, sensitivitas & spesifisitas per kelas.

2. UJI GABUNGAN (mengapa dataset TIDAK digabung jadi satu model): tiap kelas hanya ada di satu dataset, jadi kelas = asal data.
   A. heiDATA + Illinois, 5 kelas (Mock, HIV | laten, aktif, ditekan); fitur bersama = rerata, simpangan baku, CV intensitas
      kanal fluoresensi utama (heiDATA: Lamin B1; Illinois: GFP) — satu-satunya fitur yang ada di keduanya.
   B. heiDATA + Essig, 4 kelas (Mock, HIV | hidup, mati); fitur bersama = 7 fitur bentuk + rerata & simpangan baku intensitas
      (heiDATA: inti/Lamin B1; Essig: sel/brightfield).
   Dengan RF k-fold 5 per sel (cara orang yang "asal menggabung") dilaporkan:
     - akurasi menebak ASAL DATASET dari fitur yang sama,
     - balanced accuracy model gabungan dan proporsi salah tebak lintas dataset,
     - KONTROL: label diacak DI DALAM tiap dataset (informasi kondisi sel dihapus, asal dataset tetap) -> bila balanced accuracy
       masih jauh di atas peluang (1/K), angka model gabungan sebagian besar berasal dari perbedaan dataset, bukan kondisi sel.

Output: results/b8/{illinois_3kelas_summary.csv, illinois_3kelas_cm.png, gabungan_summary.csv, gabungan_cm.png, report.json}
Usage: .venv/Scripts/python -I src/b8_gabung_vs_terpisah.py
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
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, matthews_corrcoef,
                             roc_auc_score)
from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut, StratifiedKFold, cross_val_predict

from src.pilot_illinois import FEATS as I_FEATS
from src.wo14_kfold_heidata import models

SEED = 42
OUT = Path("results/b8")
I_CLASSES = ["untreated", "TNF", "Alp"]
I_NAMES = ["Laten", "Aktif (TNF)", "Ditekan (Alp)"]


def proba(est, X):
    if hasattr(est, "predict_proba"):
        return est.predict_proba(X)
    d = est.decision_function(X)
    e = np.exp(d - d.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


def multiclass_metrics(y, pred, p, k):
    cm = confusion_matrix(y, pred, labels=list(range(k)))
    sens = [cm[i, i] / cm[i].sum() if cm[i].sum() else np.nan for i in range(k)]
    spec = []
    for i in range(k):
        tn = cm.sum() - cm[i].sum() - cm[:, i].sum() + cm[i, i]
        fp = cm[:, i].sum() - cm[i, i]
        spec.append(tn / (tn + fp) if (tn + fp) else np.nan)
    try:
        auc = roc_auc_score(y, p, multi_class="ovr", average="macro", labels=list(range(k)))
    except ValueError:
        auc = np.nan
    return {"accuracy": accuracy_score(y, pred), "balanced_accuracy": balanced_accuracy_score(y, pred),
            "f1_macro": f1_score(y, pred, average="macro"), "mcc": matthews_corrcoef(y, pred), "roc_auc_ovr": auc,
            **{f"sens_{i}": s for i, s in enumerate(sens)}, **{f"spec_{i}": s for i, s in enumerate(spec)}, "cm": cm}


def run_multiclass(model, grid, X, y, splits, k):
    inner = StratifiedKFold(3, shuffle=True, random_state=SEED)
    folds, pred_all, y_all = [], [], []
    for tr, te in splits:
        best = GridSearchCV(model, grid, scoring="balanced_accuracy", cv=inner).fit(X[tr], y[tr]).best_estimator_
        p = proba(best, X[te])
        pred = best.predict(X[te])
        folds.append(multiclass_metrics(y[te], pred, p, k))
        pred_all.append(pred); y_all.append(y[te])
    keys = [m for m in folds[0] if m != "cm"]
    agg = {m: float(np.nanmean([f[m] for f in folds])) for m in keys}
    agg.update({f"{m}_sd": float(np.nanstd([f[m] for f in folds], ddof=1)) for m in ["balanced_accuracy", "roc_auc_ovr", "mcc"]})
    agg["cm"] = confusion_matrix(np.concatenate(y_all), np.concatenate(pred_all), labels=list(range(k)))
    return agg


def illinois_3class():
    df = pd.read_csv("results/pilot-illinois/cells_controls.csv").replace([np.inf, -np.inf], np.nan)
    df = df[df.condition.isin(I_CLASSES)].reset_index(drop=True)
    X = df[I_FEATS].to_numpy(float)
    y = df.condition.map({c: i for i, c in enumerate(I_CLASSES)}).to_numpy()
    g = df.plate.to_numpy()
    schemes = {"per plate (LOPO, 7 fold)": list(LeaveOneGroupOut().split(X, y, g)),
               "k-fold 5 per sel": list(StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y))}
    rows, cms = [], {}
    for sname, sp in schemes.items():
        for mname, (model, grid) in models().items():
            r = run_multiclass(model, grid, X, y, sp, 3)
            cms[(sname, mname)] = r.pop("cm")
            rows.append({"skema": sname, "model": mname, **{k: round(v, 3) for k, v in r.items()}})
            print(f"[3 kelas] {sname:26s} {mname:6s} bAcc={r['balanced_accuracy']:.3f} AUC={r['roc_auc_ovr']:.3f} "
                  f"MCC={r['mcc']:.3f}", flush=True)
    summ = pd.DataFrame(rows).rename(columns={f"sens_{i}": f"sens_{n}" for i, n in enumerate(I_NAMES)} |
                                     {f"spec_{i}": f"spec_{n}" for i, n in enumerate(I_NAMES)})
    summ.to_csv(OUT / "illinois_3kelas_summary.csv", index=False)
    best = {s: max((r for r in rows if r["skema"] == s), key=lambda r: r["mcc"]) for s in schemes}
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, (s, r) in zip(axes, best.items()):
        cm = cms[(s, r["model"])]
        cmn = cm / cm.sum(1, keepdims=True)
        ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
        for (i, j), v in np.ndenumerate(cm):
            ax.text(j, i, f"{v}\n({cmn[i, j]:.2f})", ha="center", va="center", fontsize=8,
                    color="white" if cmn[i, j] > 0.5 else "black")
        ax.set_xticks(range(3), I_NAMES, fontsize=7); ax.set_yticks(range(3), I_NAMES, fontsize=7)
        ax.set_xlabel("Prediksi"); ax.set_ylabel("Sebenarnya")
        ax.set_title(f"Illinois 3 kelas — {s}\n{r['model']}, bAcc {r['balanced_accuracy']:.2f}, MCC {r['mcc']:.2f}", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "illinois_3kelas_cm.png", dpi=140); plt.close(fig)
    return {"n": int(len(y)), "per_kelas": df.condition.value_counts().to_dict(), "best": best}


def merged_sets(rng):
    h = pd.read_csv("results/pilot-heidata/cells.csv")
    h["kelas"] = np.where(h.condition == "Mock", "heiDATA: Mock", "heiDATA: HIV")
    # A. heiDATA + Illinois: intensity statistics of the main fluorescence channel
    hA = pd.DataFrame({"mean": h.lamin_mean, "std": h.lamin_std, "cv": h.lamin_std / h.lamin_mean,
                       "kelas": h.kelas, "dataset": "heiDATA"})
    il = pd.read_csv("results/pilot-illinois/cells_controls.csv")
    il = il.groupby("condition").sample(n=200, random_state=SEED)  # every class has > 200 cells
    iA = pd.DataFrame({"mean": il.I_mean, "std": il.I_std, "cv": il.I_cv,
                       "kelas": "Illinois: " + il.condition.map(dict(zip(I_CLASSES, I_NAMES))), "dataset": "Illinois"})
    A = pd.concat([hA, iA], ignore_index=True)
    # B. heiDATA + Essig: shape + intensity of the segmented object
    shape_h = {"area": "area_um2", "perimeter": "perimeter_um", "major": "major_axis_um", "minor": "minor_axis_um",
               "eccentricity": "eccentricity", "solidity": "solidity", "circularity": "circularity",
               "mean": "lamin_mean", "std": "lamin_std"}
    hB = pd.DataFrame({k: h[v] for k, v in shape_h.items()}); hB["kelas"], hB["dataset"] = h.kelas, "heiDATA"
    e = pd.read_csv("results/pilot-essig/features_labeled.csv")
    e = e[e.expert_label.isin(["T_cell", "T_cell_with_signaling", "Dead_Cell"])].copy()
    e["kelas"] = np.where(e.expert_label == "Dead_Cell", "Essig: mati", "Essig: hidup")
    e = e.groupby("kelas").sample(n=200, random_state=SEED)  # hidup 354, mati 348
    shape_e = {"area": "BF_area", "perimeter": "BF_perimeter", "major": "BF_major_axis", "minor": "BF_minor_axis",
               "eccentricity": "BF_eccentricity", "solidity": "BF_solidity", "circularity": "BF_circularity",
               "mean": "BF_mean", "std": "BF_std"}
    eB = pd.DataFrame({k: e[v].to_numpy() for k, v in shape_e.items()}); eB["kelas"], eB["dataset"] = e.kelas.to_numpy(), "Essig"
    B = pd.concat([hB, eB], ignore_index=True)
    return {"A_heiDATA+Illinois (5 kelas, 3 fitur intensitas)": A, "B_heiDATA+Essig (4 kelas, 9 fitur bentuk+intensitas)": B}


def rf_oof(X, y):
    rf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=-1)
    return cross_val_predict(rf, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=SEED))


def merge_demo():
    rng = np.random.default_rng(SEED)
    rows, cms = [], {}
    for name, d in merged_sets(rng).items():
        d = d.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
        feats = [c for c in d.columns if c not in ("kelas", "dataset")]
        X = d[feats].to_numpy(float)
        classes = sorted(d.kelas.unique())
        y = d.kelas.map({c: i for i, c in enumerate(classes)}).to_numpy()
        ds = d.dataset.to_numpy()
        ds_pred = rf_oof(X, ds)
        pred = rf_oof(X, y)
        pred_ds = np.array([c.split(":")[0] for c in np.array(classes)[pred]])
        # control: shuffle class labels WITHIN each dataset (cell-condition information removed, dataset kept)
        ys = y.copy()
        for s in np.unique(ds):
            idx = np.where(ds == s)[0]
            ys[idx] = rng.permutation(y[idx])
        pred_s = rf_oof(X, ys)
        within = {}
        for s in np.unique(ds):
            m = ds == s
            within[s] = round(balanced_accuracy_score(y[m], pred[m]), 3)
        row = {"gabungan": name, "n": int(len(y)), "n_kelas": len(classes), "fitur": ", ".join(feats),
               "akurasi_tebak_dataset": round(accuracy_score(ds, ds_pred), 3),
               "bAcc_model_gabungan": round(balanced_accuracy_score(y, pred), 3),
               "salah_lintas_dataset": int((pred_ds != ds).sum()),
               "bAcc_label_diacak_dalam_dataset": round(balanced_accuracy_score(ys, pred_s), 3),
               "peluang_1/K": round(1 / len(classes), 3),
               "bAcc_dalam_tiap_dataset": within}
        rows.append(row)
        cms[name] = (classes, confusion_matrix(y, pred), confusion_matrix(ys, pred_s))
        print(f"[gabung] {name}: tebak dataset {row['akurasi_tebak_dataset']}, bAcc {row['bAcc_model_gabungan']}, "
              f"label diacak {row['bAcc_label_diacak_dalam_dataset']} (peluang {row['peluang_1/K']}), "
              f"salah lintas dataset {row['salah_lintas_dataset']}", flush=True)
    pd.DataFrame(rows).to_csv(OUT / "gabungan_summary.csv", index=False)
    fig, axes = plt.subplots(2, 2, figsize=(11, 9.5))
    for r, (name, (classes, cm, cm_s)) in enumerate(cms.items()):
        for c, (m, t) in enumerate([(cm, "label asli"), (cm_s, "label DIACAK di dalam tiap dataset")]):
            ax = axes[r, c]
            mn = m / m.sum(1, keepdims=True)
            ax.imshow(mn, cmap="Blues", vmin=0, vmax=1)
            for (i, j), v in np.ndenumerate(m):
                ax.text(j, i, str(v), ha="center", va="center", fontsize=8, color="white" if mn[i, j] > 0.5 else "black")
            ax.set_xticks(range(len(classes)), classes, fontsize=6, rotation=30, ha="right")
            ax.set_yticks(range(len(classes)), classes, fontsize=6)
            ax.set_title(f"{name.split(' (')[0]} — {t}\nbAcc {balanced_accuracy_score(*_yp(m)):.2f}", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "gabungan_cm.png", dpi=140); plt.close(fig)
    return rows


def _yp(cm):
    y, p = [], []
    for (i, j), v in np.ndenumerate(cm):
        y += [i] * v; p += [j] * v
    return y, p


def main():
    warnings.filterwarnings("ignore")
    OUT.mkdir(parents=True, exist_ok=True)
    rep_path = OUT / "report.json"
    rep = json.loads(rep_path.read_text(encoding="utf-8")) if rep_path.exists() else {}
    if "--merge-only" not in sys.argv:
        rep["illinois_3kelas"] = illinois_3class()
    rep["gabungan"] = merge_demo()
    (OUT / "report.json").write_text(json.dumps(rep, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
