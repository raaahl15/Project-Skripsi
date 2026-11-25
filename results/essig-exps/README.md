# Essig — hidup vs mati dari citra *brightfield* lintas percobaan (25 Nov 2026)
Ekstraksi: `src/essig_exp_features.py --zip exp2.zip --exp exp2` (59 menit; 480.001 file sel dipindai; semua sel berlabel ahli +
400 sel acak per donor × kondisi). Evaluasi: `src/essig_cross_exp.py` (protokol & metrik WO-15; hanya 19 fitur `BF_*`).

| Percobaan | Donor | Label ahli hidup / mati | Sumber label | Kesesuaian pewarna Live-Dead vs label ahli |
|---|---|---|---|---|
| exp1 | 1, 2 | 354 / 348 | ahli | AUC 0,994, kappa 0,92 |
| exp2 | 3, 4 | 137 / 79 | ahli | AUC 1,000, kappa 1,00 |

## Hasil (ambang bawaan; rentang = LogReg / RF / SVM)
| Skema | ROC AUC | Recall (sel mati) | Spesifisitas | MCC |
|---|---|---|---|---|
| **Latih exp1 → uji exp2** (percobaan baru + donor baru) | **0,98–1,00** | 0,94–0,98 | 0,97–0,99 | 0,91–0,96 |
| Leave-one-experiment-out (2 lipatan) | 0,95–0,96 | 0,89–0,91 | 0,92–0,95 | 0,81–0,85 |
| Leave-one-donor-out (4 donor) | 0,95–0,96 | 0,86–0,89 | 0,92–0,93 | 0,79–0,82 |

- Model *brightfield* yang dilatih pada exp1 tetap bekerja pada percobaan lain dengan donor lain → sinyal hidup/mati bukan efek *batch*.
- Catatan: kesepakatan pewarna vs label ahli di exp2 sempurna (kappa 1,00) → label ahli kemungkinan dibantu kanal Live-Dead.
  Model hanya memakai *brightfield*, jadi tidak ada kebocoran dari kanal pewarna ke fitur.
- exp2 berisi 216 sel berlabel hidup/mati → selang kepercayaan lebih lebar daripada exp1. exp3 dan exp4 (38–40 GB) belum diproses.

Berkas: `exp2_features.csv`, `exp2_summary.json`, `label_agreement.json`, `combined_labeled.csv`, `cross_exp_summary.csv`, `cross_exp_metrics.json`.
