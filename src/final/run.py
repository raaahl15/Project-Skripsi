"""Run one final model end to end: load features -> nested evaluation -> permutation test -> figures -> README.

Usage (Colab, from the repo root):
    python -m src.final.run --config configs/final/model_B.yaml --data-root /content/drive/MyDrive/Project-Skripsi \
        --out results/final/model_B --models-dir /content/drive/MyDrive/Project-Skripsi/models/<run_id>
Options: --quick (tiny subsample, few permutations/bootstraps; code check only, results not for the thesis)
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import yaml
from sklearn.metrics import roc_curve

from src.final.data import LOADERS, feature_list
from src.final.protocol import build_models, evaluate, outer_splits, permutation_test, stratified_subsample


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short=7", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def strip_private(r: dict) -> dict:
    return {k: v for k, v in r.items() if not k.startswith("_")}


def fmt(v, ci=None):
    if v is None:
        return "–"
    s = f"{v:.3f}".replace(".", ",")
    if ci:
        s += f" [{ci[0]:.2f}–{ci[1]:.2f}]".replace(".", ",")
    return s


def plot_cm(cm, classes, title, path):
    cm = np.array(cm)
    norm = cm / cm.sum(1, keepdims=True).clip(min=1)
    fig, ax = plt.subplots(figsize=(1.3 * len(classes) + 1.8, 1.2 * len(classes) + 1.4))
    ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
    for (i, j), v in np.ndenumerate(cm):
        ax.text(j, i, f"{v}\n({norm[i, j]:.0%})", ha="center", va="center", fontsize=9,
                color="white" if norm[i, j] > 0.5 else "black")
    ax.set_xticks(range(len(classes)), classes, fontsize=8)
    ax.set_yticks(range(len(classes)), classes, fontsize=8)
    ax.set_xlabel("Kelas prediksi"); ax.set_ylabel("Kelas sebenarnya"); ax.set_title(title, fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_roc(results, classes, title, path):
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    K = len(classes)
    for name, r in results.items():
        y, P = r["_y"], r["_P"]
        if K == 2:
            fpr, tpr, _ = roc_curve(y, P[:, 1])
            ax.plot(fpr, tpr, label=f"{name} (AUC {fmt(r['pooled']['roc_auc'])})")
    if K > 2:
        best = max(results, key=lambda m: results[m]["pooled"]["mcc"] or -1)
        y, P = results[best]["_y"], results[best]["_P"]
        for c in range(K):
            fpr, tpr, _ = roc_curve((y == c).astype(int), P[:, c])
            ax.plot(fpr, tpr, label=f"{classes[c]} vs lainnya ({best})")
    ax.plot([0, 1], [0, 1], "--", color="gray", lw=0.8)
    ax.set_xlabel("Laju positif palsu (1 − spesifisitas)"); ax.set_ylabel("Laju positif benar (sensitivitas)")
    ax.set_title(title, fontsize=9); ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_importance(imp, title, path, top=15):
    items = sorted(imp.items(), key=lambda kv: kv[1]["mean"], reverse=True)[:top][::-1]
    fig, ax = plt.subplots(figsize=(5.2, 0.32 * len(items) + 1.2))
    ax.barh([k for k, _ in items], [v["mean"] for _, v in items], xerr=[v["sd"] or 0 for _, v in items],
            color="#4C72B0", ecolor="gray", capsize=2)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xlabel("Penurunan balanced accuracy saat fitur diacak"); ax.set_title(title, fontsize=9)
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def main():
    warnings.filterwarnings("ignore")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--models-dir", default=None)
    ap.add_argument("--run-id", default=time.strftime("%Y%m%d-%H%M", time.gmtime()))
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    t_start = time.time()
    cfg = yaml.safe_load(Path(a.config).read_text(encoding="utf-8"))
    seed, classes = cfg["seed"], cfg["classes"]
    K = len(classes)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    logf = open(out / "log.txt", "w", encoding="utf-8")

    def log(msg):
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()

    df, y, data_info = LOADERS[cfg["dataset"]](Path(a.data_root), cfg)
    if a.quick:
        keep = stratified_subsample(np.arange(len(y)), y, 600, seed)
        df, y = df.iloc[keep].reset_index(drop=True), y[keep]
    n_boot = 50 if a.quick else cfg.get("bootstrap", 1000)
    perm_cfg = dict(cfg.get("permutation", {}))
    if a.quick:
        perm_cfg["n"] = min(5, perm_cfg.get("n", 100))
    log(f"== {cfg['title']} | n={len(y)} | per kelas={dict(zip(classes, np.bincount(y, minlength=K).tolist()))}")
    models = build_models(seed)
    models = {m: models[m] for m in cfg.get("models", list(models))}
    schemes = dict(cfg["group_schemes"])
    if cfg.get("compare_kfold"):
        schemes[f"kfold{cfg['compare_kfold']}_per_sel"] = None
    main_fs, main_scheme = cfg["main_feature_set"], cfg["main_scheme"]

    results, rows = {}, []
    for fs_name, spec in cfg["feature_sets"].items():
        feats = feature_list(df, spec)
        X = df[feats].to_numpy(float)
        for sc_name, gcol in schemes.items():
            groups = df[gcol].astype(str).to_numpy() if gcol else None
            splits = outer_splits(X, y, groups, "group" if gcol else sc_name.split("_")[0], seed)
            is_main = fs_name == main_fs and sc_name == main_scheme
            for mname, (model, grid) in models.items():
                log(f"-- {fs_name} | {sc_name} ({len(splits)} lipatan) | {mname}")
                r = evaluate(mname, model, grid, X, y, groups, splits, K, seed=seed,
                             svm_max_train=cfg.get("svm_max_train"), n_boot=n_boot if is_main else 0,
                             importance=cfg.get("importance") if is_main else None, feature_names=feats, log=log)
                results[(fs_name, sc_name, mname)] = r
                p, ms = r["pooled"], r["per_fold_mean_sd"]
                rows.append({"feature_set": fs_name, "scheme": sc_name, "n_folds": r["n_folds"], "model": mname,
                             "balanced_accuracy_pooled": p["balanced_accuracy"], "mcc_pooled": p["mcc"],
                             "roc_auc_pooled": p["roc_auc"], "sensitivity_pooled": p.get("sensitivity"),
                             "specificity_pooled": p.get("specificity"),
                             "balanced_accuracy_fold_mean": ms["balanced_accuracy"]["mean"],
                             "balanced_accuracy_fold_sd": ms["balanced_accuracy"]["sd"],
                             "roc_auc_fold_mean": ms["roc_auc"]["mean"], "roc_auc_fold_sd": ms["roc_auc"]["sd"],
                             "ci95_balanced_accuracy": r["ci95_pooled"].get("balanced_accuracy"),
                             "ci95_mcc": r["ci95_pooled"].get("mcc"), "ci95_roc_auc": r["ci95_pooled"].get("roc_auc"),
                             "sensitivity_per_class": p["sensitivity_per_class"],
                             "specificity_per_class": p["specificity_per_class"], "cm_pooled": p["cm"],
                             "seconds": r["seconds"]})
                log(f"   pooled bAcc={p['balanced_accuracy']} MCC={p['mcc']} AUC={p['roc_auc']} ({r['seconds']} s)")

    main_res = {m: results[(main_fs, main_scheme, m)] for m in models}
    best = max(main_res, key=lambda m: (main_res[m]["pooled"]["mcc"] or -1, main_res[m]["pooled"]["roc_auc"] or 0))
    log(f"== model terbaik (skema utama, MCC gabungan): {best}")

    # label-permutation test on the main scheme
    feats = feature_list(df, cfg["feature_sets"][main_fs])
    X = df[feats].to_numpy(float)
    groups = df[cfg["group_schemes"][main_scheme]].astype(str).to_numpy()
    splits = outer_splits(X, y, groups, "group", seed)
    perm_model = best if perm_cfg.get("model", "best") == "best" else perm_cfg["model"]
    perm = None
    if perm_cfg.get("n"):
        log(f"-- uji permutasi label ({perm_model}, {perm_cfg['n']} kali)")
        perm = permutation_test(models[perm_model][0], main_res[perm_model]["most_common_params"], X, y, groups, splits,
                                n_perm=perm_cfg["n"], seed=seed, svm_max_train=cfg.get("svm_max_train"),
                                is_svm=perm_model == "svm", log=log)
        perm["model"] = perm_model
        log(f"   p = {perm['p_value']} (teramati {perm['observed_balanced_accuracy']}, nol rata-rata {perm['null_mean']})")

    # figures
    title = cfg["title"]
    plot_cm(main_res[best]["pooled"]["cm"], classes, f"{title}\n{main_scheme}, {best} (gabungan lipatan uji)",
            out / "confusion_matrix.png")
    plot_roc(main_res, classes, f"{title}\nROC, {main_scheme}", out / "roc.png")
    if "importance" in main_res[best]:
        plot_importance(main_res[best]["importance"], f"{title}\nKepentingan fitur ({best}, {main_scheme})",
                        out / "importance.png")
        pd.DataFrame([{"feature": k, **v} for k, v in main_res[best]["importance"].items()]) \
            .sort_values("mean", ascending=False).to_csv(out / "importance.csv", index=False)

    # out-of-fold predictions of the best main model (small table, kept with the results)
    r = main_res[best]
    oof = pd.DataFrame({"row": r["_tested"], "y_true": r["_y"], "y_pred": r["_pred"]})
    for c in range(K):
        oof[f"p_{classes[c]}"] = np.round(r["_P"][:, c], 4)
    oof["group"] = groups[r["_tested"]]
    oof.to_csv(out / "oof_predictions_best.csv", index=False)

    # final model on all data (saved to Drive, not to git)
    if a.models_dir and not a.quick:
        import joblib
        md = Path(a.models_dir); md.mkdir(parents=True, exist_ok=True)
        est = models[best][0].set_params(**main_res[best]["most_common_params"])
        idx = stratified_subsample(np.arange(len(y)), y, cfg.get("svm_max_train"), seed) if best == "svm" \
            else np.arange(len(y))
        path = md / "model_{}_{}.joblib".format(cfg["model"], best)
        joblib.dump({"model": est.fit(X[idx], y[idx]), "features": feats, "classes": classes, "config": cfg}, path)
        log(f"   model akhir disimpan: {path}")

    summary = pd.DataFrame(rows)
    summary.to_csv(out / "summary.csv", index=False)
    full = {"config": cfg, "data_info": data_info, "n": int(len(y)),
            "class_counts": dict(zip(classes, np.bincount(y, minlength=K).tolist())), "best_model": best,
            "permutation_test": perm,
            "results": {" | ".join(k): strip_private(v) for k, v in results.items()}}
    (out / "metrics.json").write_text(json.dumps(full, indent=1, default=str), encoding="utf-8")
    info = {"run_id": a.run_id, "git_commit": git_sha(), "quick": a.quick, "python": platform.python_version(),
            "sklearn": sklearn.__version__, "numpy": np.__version__, "pandas": pd.__version__,
            "minutes": round((time.time() - t_start) / 60, 1), "config_file": a.config}
    (out / "run_info.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    write_readme(out, cfg, full, summary, info, best)
    log(f"== selesai dalam {info['minutes']} menit -> {out}")


def write_readme(out, cfg, full, summary, info, best):
    classes, K = cfg["classes"], len(cfg["classes"])
    L = [f"# {cfg['title']}", "",
         f"Run `{info['run_id']}` · commit `{info['git_commit']}` · Python {info['python']} · scikit-learn {info['sklearn']}"
         f" · {info['minutes']} menit" + (" · **QUICK (uji kode, bukan hasil naskah)**" if info["quick"] else ""), "",
         f"Config: `{info['config_file']}`. Dibuat otomatis oleh `src/final/run.py`; angka di tabel ini boleh dikutip di naskah.", "",
         "## Data", f"- Jumlah sel: **{full['n']}** · per kelas: " +
         ", ".join(f"{c} {n}" for c, n in full["class_counts"].items()),
         f"- Rincian: `{json.dumps(full['data_info'], ensure_ascii=False)[:600]}`", "",
         f"## Hasil utama: {cfg['main_feature_set']} · {cfg['main_scheme']}",
         "Gabungan semua lipatan uji (kelompok yang tidak dipakai melatih); kurung siku = selang kepercayaan 95% *bootstrap*.", ""]
    hdr = "| Model | Balanced accuracy | MCC | ROC AUC |" + (" Sensitivitas | Spesifisitas |" if K == 2 else "")
    L += [hdr, "|" + "---|" * (hdr.count("|") - 1)]
    m = summary[(summary.feature_set == cfg["main_feature_set"]) & (summary.scheme == cfg["main_scheme"])]
    for _, r in m.iterrows():
        line = (f"| {r.model}{' (terbaik)' if r.model == best else ''} | {fmt(r.balanced_accuracy_pooled, r.ci95_balanced_accuracy)}"
                f" | {fmt(r.mcc_pooled, r.ci95_mcc)} | {fmt(r.roc_auc_pooled, r.ci95_roc_auc)} |")
        if K == 2:
            line += f" {fmt(r.sensitivity_pooled)} | {fmt(r.specificity_pooled)} |"
        L.append(line)
    br = m[m.model == best].iloc[0]
    L += ["", f"Per kelas ({best}): " + "; ".join(
        f"{c}: sensitivitas {fmt(s)}, spesifisitas {fmt(p)}"
        for c, s, p in zip(classes, br.sensitivity_per_class, br.specificity_per_class)), ""]
    pt = full.get("permutation_test")
    if pt:
        L += [f"**Uji permutasi label** ({pt['model']}, {pt['n_perm']} kali, label diacak di dalam kelompok): balanced accuracy "
              f"teramati {fmt(pt['observed_balanced_accuracy'])}, rata-rata nol {fmt(pt['null_mean'])}, **p = {pt['p_value']}**.", ""]
    L += ["## Semua skema dan set fitur", "| Set fitur | Skema | Lipatan | Model | bAcc gabungan | MCC | ROC AUC | bAcc per lipatan (rerata ± sd) |",
          "|---|---|---|---|---|---|---|---|"]
    for _, r in summary.iterrows():
        sd = f" ± {fmt(r.balanced_accuracy_fold_sd)}" if pd.notna(r.balanced_accuracy_fold_sd) else ""
        L.append(f"| {r.feature_set} | {r.scheme} | {r.n_folds} | {r.model} | {fmt(r.balanced_accuracy_pooled)} | "
                 f"{fmt(r.mcc_pooled)} | {fmt(r.roc_auc_pooled)} | {fmt(r.balanced_accuracy_fold_mean)}{sd} |")
    L += ["", "Selisih antara skema per kelompok dan *k-fold* per sel menunjukkan besar kebocoran efek *batch*.", "",
          "## Berkas", "- `confusion_matrix.png`, `roc.png`, `importance.png` / `importance.csv`",
          "- `summary.csv` (semua baris), `metrics.json` (lengkap, termasuk per lipatan), `oof_predictions_best.csv`, `log.txt`",
          "", "## Catatan protokol"]
    L += [f"- {n}" for n in cfg.get("notes", [])]
    L += ["- Lapisan dalam: GridSearchCV (skor balanced accuracy), berkelompok bila data latih memuat ≥ 3 kelompok.",
          "- Prediksi kelas = argmax peluang; SVM dilatih ulang dengan `probability=True` setelah pencarian parameter.",
          f"- Seed {cfg['seed']}."]
    (out / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
