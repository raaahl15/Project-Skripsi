# Run Google Colab — 20261103-2339 (UTC) = 4 Nov 2026 06:39 WIB
Notebook: `notebooks/colab/pilot_skripsi_colab.ipynb` (Run all; Essig nonaktif). Sumber asli: Drive `Project-Skripsi/results-colab/20261103-2339/`.
Arsip ini **tidak** menggantikan `results/pilot-heidata/` dan `results/pilot-luo/` (hasil laptop yang dikutip di Bahan Bimbingan 5).
Catatan: `pilot-heidata/metrics_classify_norm-figure.json` di folder Drive berasal dari repo (tidak dijalankan ulang di Colab), sehingga tidak diarsipkan di sini.

## Perbandingan dengan run laptop (3 Nov 2026)
| Bagian | Hasil |
|---|---|
| Segmentasi + ekstraksi fitur heiDATA (`cells.csv`, 209 sel, per kondisi sama) | **Identik** (selisih maks. 7,1×10⁻¹⁵) |
| CyTOF Luo (`metrics_classify.json`, 61 angka) | **Identik** |
| heiDATA Logistic Regression (semua tugas) | **Identik** (T1b AUC 0,651; p = 0,010) |
| heiDATA Random Forest | **Sedikit berbeda** (20 dari 42 angka; mis. T1b balanced accuracy 0,626 → 0,577; T1a AUC 0,584 → 0,570; T2 AUC 0,084 → 0,090); kesimpulan tidak berubah |

Dugaan penyebab perbedaan RF: versi pustaka berbeda (laptop: scikit-learn 1.9.1, numpy 2.5.4, scikit-image 0.26.0, shap 0.54.1;
versi Colab tidak tercatat) dan paralelisme `n_jobs=-1`.
**Tindak lanjut:** catat versi pustaka di setiap keluaran, kunci versi (`pip freeze`) untuk run final, dan ambil semua angka naskah dari
satu lingkungan yang sama.
