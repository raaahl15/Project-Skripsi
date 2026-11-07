# WO-14 — Validasi k-fold heiDATA (7 Nov 2026)
Skrip: `src/wo14_kfold_heidata.py` · scikit-learn 1.9.1 · seed 42 · laptop (CPU).
Keluaran: `metrics_kfold.json` (per fold, termasuk hiperparameter terpilih), `summary_kfold.csv`, `kfold_auc.png`.

## Desain
- **Training / validation / testing:** tiap fold luar = data uji (testing). Di dalam data latih, `GridSearchCV` dengan 3-fold (validation)
  memilih hiperparameter; model terbaik lalu diuji pada fold luar yang tidak pernah dipakai melatih atau memilih.
- **Model:** Logistic Regression, Random Forest, SVM (RBF); semua `class_weight="balanced"`.
- **Skema fold luar:** k-fold 5 dan 10 per sel (`StratifiedKFold`, sesuai arahan B5) vs k-fold berkelompok per figure/percobaan
  (`StratifiedGroupKFold`; satu percobaan seluruhnya di latih atau seluruhnya di uji).

## Hasil (ROC AUC rata-rata antar-fold; 0,5 = acak)
| Tugas | n sel | k-fold 5 (per sel) | k-fold 10 (per sel) | Berkelompok per figure |
|---|---|---|---|---|
| T2 terpapar HIV vs Mock (Lamin B1) | 209 | 0,74–0,79 | 0,75–0,80 | 0,27–0,46 (2 fold berisi Mock) |
| T1a +Vpx vs −Vpx (Lamin B1) | 170 | 0,66–0,72 | 0,67–0,72 | 0,52–0,58 |
| T1b +Vpx vs −Vpx (Lamin B1 + kapsid) | 132 | 0,66–0,77 | 0,69–0,79 | 0,46–0,53 |

T1b dihitung ulang 7 Nov setelah perbaikan deteksi kapsid (skala bersama per percobaan; lihat `results/b6/README.md`).
T2 dan T1a tidak memakai fitur kapsid sehingga tidak berubah.

Rentang = tiga model. Rincian simpangan baku, *balanced accuracy*, dan F1 ada di `summary_kfold.csv`.

## Tafsiran
- K-fold per sel memberi AUC 0,65–0,80, tetapi **turun ke sekitar acak (0,45–0,58) atau di bawahnya** saat percobaan dipisah.
  Selisih ini adalah **kebocoran efek *batch***: dengan k-fold per sel, model mengenali dari percobaan mana sebuah sel berasal
  (intensitas, setelan mikroskop), bukan kondisi selnya.
- T2 (arah B5: terinfeksi vs tidak) paling terdampak: Mock hanya ada di 2 dari 6 percobaan, sehingga label Mock hampir identik dengan
  "berasal dari percobaan 1G atau S3B". AUC berkelompok < 0,5 berarti model justru belajar perbedaan antar-percobaan.
- Kesimpulan: angka k-fold per sel **tidak boleh dilaporkan sendirian**. Dengan data heiDATA saat ini (14 bidang pandang), belum ada bukti
  fitur citra yang memisahkan kondisi sel lintas percobaan. Penambahan bidang pandang per kondisi (WO-12, permintaan data ke Heidelberg)
  menjadi kebutuhan utama, bukan pilihan.
- Catatan metode: validasi dalam (pemilihan hiperparameter) memakai 3-fold per sel di semua skema; ini hanya memengaruhi pilihan
  hiperparameter, bukan data uji.
