# Pilot Illinois IDB-8103861 (8 Nov 2026)
Skrip: `src/pilot_illinois.py --cap 20` · seed 42 · laptop. Data: `intensityTrajectories.zip`, `noiseTrajectories.zip`, `plateNSClookup.xlsx`
(salinan di Drive `data/raw/`, lokal `data/raw/illinois-IDB-8103861/`). Paper: Lu dkk., *PNAS* 2021, DOI 10.1073/pnas.2012191118.

## Data
- Sel T Jurkat dengan sirkuit gen HIV minimal (reporter GFP). Lintasan intensitas per sel, 72 bingkai (15 menit, jam 1–19),
  hasil ekstraksi citra oleh peneliti (NIS Elements). 7 plate (Diversity Set 3 Plate 1–5, Plate 1 Repeat, Oncology Set).
- Hanya sumur kontrol: kolom 1 = TNF-α (aktivasi HIV), kolom 2 & 23 = tanpa perlakuan, kolom 24 = alsterpaullone (penekan).
- Maksimal 20 sel per sumur: 2.100 sel TNF (105 sumur), 4.120 tanpa perlakuan (206 sumur), 2.039 alsterpaullone (102 sumur).

## Fitur per sel (dari lintasan intensitas sel itu sendiri)
`I_mean`, `I_std`, `I_cv` (= std/mean), `I_slope` (kemiringan regresi linear per jam), `I_start`/`I_end` (rata-rata 4 bingkai
pertama/terakhir), `I_fold` (= end/start), `I_resid_std` (simpangan baku setelah tren linear dibuang), `I_ac1` (autokorelasi lag-1 residu).

**Temuan kebocoran:** lintasan *noise* dari peneliti = intensitas yang dipusatkan ganda (rata-rata sel dan rata-rata sumur per bingkai
dikurangkan; selisih maksimum 0). Fitur turunannya membawa rata-rata sumur ke setiap sel (mis. `I_slope − N_slope` = kemiringan
rata-rata sumur). Dengan semua fitur *noise*, AUC = 1,00 di semua skema → **tidak dipakai**.

## Hasil (ROC AUC rata-rata fold; protokol WO-14: GridSearch 3-fold di data latih, fold luar = testing)
| Tugas | Fitur | k-fold 5 per sel | Per sumur (5 fold) | Leave-one-plate-out (7) |
|---|---|---|---|---|
| TNF vs tanpa perlakuan | **sel saja** | 0,85–0,88 | 0,85–0,88 | **0,85–0,87** |
| Alsterpaullone vs tanpa perlakuan | **sel saja** | 0,93–0,95 | 0,93–0,95 | **0,93–0,95** |
| TNF vs tanpa perlakuan | sel + `N_std` | 0,85–0,98 | 0,86–0,98 | 0,85–0,98 |
| Alsterpaullone vs tanpa perlakuan | sel + `N_std` | 0,96–0,99 | 0,96–0,99 | 0,96–0,98 |
| TNF vs tanpa perlakuan | semua fitur *noise* (bocor) | 1,00 | 1,00 | 1,00 |

Rentang = LogReg, RF, SVM. Rincian: `summary.csv`, `metrics.json` (termasuk AUC univariat per fitur), median fitur: `feature_medians.csv`.

## Tafsiran
- Fitur sel saja: skor hampir sama di ketiga skema, termasuk plate baru → **tidak ada kebocoran efek *batch***; sinyal berlaku lintas plate.
- AUC < 1 masuk akal: tidak semua sel merespons TNF (heterogenitas ekspresi).
- Fitur univariat terkuat: TNF ↔ `I_fold` 0,82, `I_slope` 0,80, `I_cv` 0,79; alsterpaullone ↔ `I_end` (AUC 0,10, yaitu 0,90 terbalik),
  `I_fold` 0,14, `I_slope` 0,16.
- `N_std` (besar fluktuasi setelah tren sumur dibuang) menaikkan RF/SVM ke ±0,98, tetapi ikut membawa informasi rata-rata sumur
  → hanya sebagai pembanding, bukan hasil utama.
- Keterbatasan: fitur dari ekstraksi citra oleh peneliti (bukan ekstraksi sendiri); Jurkat, bukan CD4 primer; 20 sel per sumur.
