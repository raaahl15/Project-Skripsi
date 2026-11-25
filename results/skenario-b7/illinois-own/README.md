# Illinois Plate 2 — fitur dari ekstraksi citra sendiri (25 Nov 2026)
Citra: potongan arsip `images_DiversitySet3Plate2.zip.003` (10 GiB) → 4 sumur kontrol utuh (dibaca dengan `src/illinois_zip_parts.py`).
Segmentasi + pelacakan sendiri (k = 5), bingkai 4–75 (jam 1–19), lintasan lengkap saja → 9 fitur per sel (`results/illinois-own/*.csv`).

| Sumur | Kelas | Sel (lintasan lengkap) | Waktu proses |
|---|---|---|---|
| A23 | tanpa perlakuan (laten) | 264 | 402 s |
| A24 | alsterpaullone (ditekan) | 334 | 645 s |
| B01 | TNF-α (aktif) | 300 | 464 s |
| B02 | tanpa perlakuan (laten) | 287 | 528 s |

Analisis: `python -I src/illinois_own_analysis.py` → `summary.csv`, `univariate_auc.csv`, `report.json`.

## Hasil (ambang bawaan; rentang = LogReg / RF / SVM)
| Tugas | k-fold 5 per sel (fitur sendiri, 9 fitur) | Transfer: latih fitur **penulis** 6 plate lain → uji fitur **sendiri** Plate 2 (5 fitur bebas skala) |
|---|---|---|
| Aktif (TNF) vs laten | AUC 0,91–0,92 · bal. acc 0,81–0,82 · MCC 0,63 | AUC **0,86–0,89** · recall 0,67–0,78 · spesifisitas 0,84–0,91 · MCC 0,56–0,61 |
| Ditekan (Alp) vs laten | AUC 0,99–1,00 · MCC 0,94–0,96 | AUC **0,90–0,92** · recall 0,84–0,89 · spesifisitas 0,81–0,85 · MCC 0,67–0,69 |

- **Kesesuaian dengan data penulis** (sumur yang sama, AUC univariat per fitur): korelasi 0,97 untuk kedua tugas; arah efek sama
  9/9 fitur (Alp) dan 7/9 (TNF; dua yang berbeda adalah fitur di sekitar 0,5: `I_start` 0,48 vs 0,52, `I_resid_std` 0,61 vs 0,48).
  Fitur terkuat sama: `I_fold`, `I_slope`, `I_end` (TNF menaikkan GFP), `I_mean`/`I_end` turun pada Alp.
- **Transfer** = plate baru **dan** cara ekstraksi baru sekaligus; hasilnya setara dengan uji plate baru pada fitur penulis
  (AUC 0,87 / 0,95), sehingga ekstraksi sendiri dapat dipakai untuk Skenario 2.
- **Keterbatasan:** hanya 1 sumur per kelas positif → validasi berkelompok per sumur tidak mungkin; k-fold per sel di sini batas atas
  (sel satu sumur berbagi kondisi). Bukti lintas kelompok = skema transfer. Menambah sumur: bagian `.005` (blok B23–C02) dan `.007`.
- Fitur bebas skala dipakai untuk transfer karena intensitas absolut ekstraksi sendiri lebih rendah daripada penulis (ROI/latar berbeda).
