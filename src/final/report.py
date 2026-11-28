"""Combine the per-model results into results/final/README.md (source of the Bab IV numbers).

Usage: python -m src.final.report --dir results/final
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def f(v):
    return "–" if v is None else f"{v:.3f}".replace(".", ",")


def ci(c):
    return "" if not c else f" [{c[0]:.2f}–{c[1]:.2f}]".replace(".", ",")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="results/final"); a = ap.parse_args()
    root = Path(a.dir)
    L = ["# Hasil final machine learning (tiga model bertingkat)", "",
         "Dibuat otomatis oleh `src/final/report.py` dari `results/final/model_*/metrics.json`. Semua angka berasal dari data uji",
         "kelompok yang tidak dipakai melatih (skema utama tiap model). Rincian, gambar, dan protokol: README tiap model.", "",
         "| Model | Kelas | Data (sel) | Skema uji | Model terbaik | Balanced accuracy [CI 95%] | MCC [CI 95%] | ROC AUC [CI 95%] | Uji permutasi p | Run |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for d in sorted(root.glob("model_*")):
        mf, rf = d / "metrics.json", d / "run_info.json"
        if not mf.exists():
            continue
        m, info = json.loads(mf.read_text(encoding="utf-8")), json.loads(rf.read_text(encoding="utf-8"))
        cfg, best = m["config"], m["best_model"]
        r = m["results"][f"{cfg['main_feature_set']} | {cfg['main_scheme']} | {best}"]
        p, c = r["pooled"], r["ci95_pooled"]
        pt = m.get("permutation_test") or {}
        L.append(f"| {cfg['model']} | {' / '.join(cfg['classes'])} | {m['n']} | {cfg['main_scheme']} ({r['n_folds']} lipatan) | "
                 f"{best} | {f(p['balanced_accuracy'])}{ci(c.get('balanced_accuracy'))} | {f(p['mcc'])}{ci(c.get('mcc'))} | "
                 f"{f(p['roc_auc'])}{ci(c.get('roc_auc'))} | {pt.get('p_value', '–')} | `{info['run_id']}`"
                 f"{' QUICK' if info.get('quick') else ''} |")
    L += ["", "Keluaran akhir kerangka bertingkat: mati, tidak terinfeksi, aktif, laten, ditekan (Gambar III.2). Tiap model dilatih",
          "dan diuji pada datasetnya sendiri; rantai utuh tidak dapat diuji karena tidak ada dataset yang memuat semua label."]
    (root / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
