# Analisis untuk Bimbingan 6 (7 Nov 2026)
Skrip: `src/b6_analyses.py` · seed 42 · laptop (CPU). Log: `log.txt`.

## Bagian A — heiDATA (paparan HIV-1): konsistensi efek per percobaan
Tanpa ML. Untuk tiap fitur dan tiap percobaan (figure) dihitung Cohen's d (+Vpx − −Vpx, dan terpapar HIV − Mock) dan uji Mann–Whitney,
lalu dilihat apakah arah perubahannya sama di semua percobaan. Keluaran: `A_effect_size_per_figure.csv`, `A_effect_size_consistency.csv`,
`A_effect_size_heatmap.png`.

**+Vpx vs −Vpx (5 percobaan berisi kedua kelas: 1G, 2A, 2D, 3B, S3B)**
| Fitur | d median | Arah sama | p < 0,05 | Rentang d |
|---|---|---|---|---|
| Soliditas | 0,59 | **5 dari 5** | 0 | 0,12 – 0,70 |
| Sirkularitas | 0,54 | 4 dari 5 | 1 (3B) | −0,02 – 0,69 |
| Rasio tepi/inti Lamin B1 | 0,87 | 4 dari 5 | 2 (2D, S3B) | −1,02 – 1,98 |
| Fitur ukuran (luas, keliling, diameter) | ≈ 0 | 3 dari 5 | — | ±1,5 – 2,3 |

- Sel +Vpx cenderung punya inti **lebih konveks (soliditas ↑) dan lebih bulat (sirkularitas ↑)** di hampir semua percobaan.
  Efeknya sedang dan konsisten arahnya, tetapi per percobaan sebagian besar tidak signifikan (sampel kecil). Uji tanda 5/5: p = 0,06 (dua sisi).
- Fitur ukuran dan intensitas berubah arah antar-percobaan → inilah yang menjadi efek *batch* dan membuat ML lintas percobaan gagal.
- HIV vs Mock hanya bisa dibandingkan di 2 percobaan (1G, S3B) → terlalu sedikit untuk menyimpulkan.
- Tafsiran biologis (mengapa inti lebih bulat pada +Vpx) **belum ada pustakanya** — jangan diklaim dulu.

**Pemeriksaan kanal kapsid — kesalahan ditemukan dan diperbaiki (7 Nov)**
- Gejala: sel Mock (tanpa virus) di 1G terhitung paling banyak titik kapsid (median 124 per inti vs 10–19 pada sel terpapar).
- Penyebab: detektor menormalisasi **tiap citra ke rentangnya sendiri** (persentil 1–99,95). Citra Mock tidak punya kapsid, sehingga
  derau latarnya teregang ke rentang penuh dan terdeteksi sebagai titik. Bukti (`A_capsid_channel_qc.csv`, `src/check_ca_channel.py`):

| Bidang pandang | Persentil 99,95 mentah | Titik (skala per citra, lama) | Titik (skala bersama per percobaan, baru) |
|---|---|---|---|
| 1G +Vpx | 7.151 | 216 | 113 |
| 1G −Vpx | 12.741 | 292 | 417 |
| **1G Mock** | **2.644** | **8.325** | **0** |
| **S3B Mock** | 4.139 | 480 | **0** |

- Perbaikan: `detect_puncta(..., scale=...)` dengan skala bersama per figure; fitur dihitung ulang (`cells.csv`; versi lama disimpan sebagai
  `cells_v1_skala-per-citra.csv`). Fitur non-kapsid identik. Median kapsid di inti setelah perbaikan (`A_capsid_sanity.csv`):
  Mock = 0 di kedua percobaan; 1G +Vpx 11 / −Vpx 18; 3B +Vpx 8,5 / −Vpx 0; S3B +Vpx 3 / −Vpx 2,5.
- Keterbatasan sisa: di 3B, 4D, S3B banyak piksel jenuh (65.535), sehingga skala bersama ditentukan bidang pandang tercerah.
- **Dampak ke hasil B5:** pilot T1b (*leave-one-figure-out*, LogReg) yang dilaporkan AUC **0,65, p = 0,01** menjadi **AUC 0,57, p = 0,14
  (tidak signifikan)**; RF 0,53 (p = 0,28). Klaim "signifikan tetapi sedang" di B5 **gugur**. SHAP: sumbu mayor inti tetap teratas.
- Label "terinfeksi per sel dari kapsid" (ide 2b) belum dijalankan; bisa dipertimbangkan lagi setelah kanal kapsid diperbaiki.
Normalisasi fitur per percobaan (ide 2a) sudah diuji di pilot (`results/pilot-heidata/metrics_classify_norm-figure.json`): AUC 0,17–0,44, tidak membantu.

## Bagian A2 — heiDATA: terpapar HIV-1 vs Mock dari kapsid terdeteksi optik (8 Nov)
Skrip: `src/b6_capsid_hiv_vs_mock.py` → `A_capsid_hiv_vs_mock.json`, `A_capsid_hiv_vs_mock_summary.csv`, `log_capsid.txt`.
Hanya 1G dan S3B yang punya Mock + kanal kapsid: 1G 21 terpapar / 11 Mock; S3B 40 terpapar (+EFV) / 28 Mock (100 sel).
Validasi utama: **latih di satu percobaan, uji di percobaan lain** (2 fold), GridSearch 3-fold di data latih.

| Fitur | Lintas percobaan: AUC (fold 1G, S3B) | *Balanced accuracy* | k-fold 5 per sel (pembanding) |
|---|---|---|---|
| **Kapsid saja (2 fitur)** | **0,91 (1,00; 0,81)** — LogReg/RF/SVM sama | **0,78–0,90** | 0,88 |
| Kapsid + Lamin B1 | 0,27–0,80 | 0,51–0,60 | 0,93–0,96 |
| Lamin B1 saja | 0,19–0,26 | 0,36–0,48 | 0,60–0,81 |

- Uji permutasi (LogReg, kapsid, 100 permutasi): **p = 0,01** (batas terkecil untuk 100 permutasi).
- Aturan tanpa pelatihan "terinfeksi bila ≥ 1 titik kapsid di inti": 1G *balanced accuracy* 1,00; S3B 0,81 (0 Mock salah;
  15 dari 40 sel terpapar tanpa kapsid di inti — 45% sel +Vpx dan 30% sel −Vpx). Mock: 0 titik pada 100% sel di kedua percobaan.
- Tafsiran: kapsid HIV-1 yang terdeteksi secara optik **membedakan sel terpapar dari Mock lintas percobaan**. Menambah fitur Lamin B1
  justru menurunkan hasil lintas percobaan (efek *batch*), padahal menaikkan k-fold per sel → contoh lain kebocoran.
- Keterbatasan: 2 percobaan, 100 sel; label = kondisi paparan, bukan status infeksi per sel (sel terpapar tanpa kapsid di inti mungkin
  memang tidak terinfeksi); kapsid adalah penanda virus yang diwarnai, sehingga tugas ini relatif langsung — tantangannya ada pada deteksi
  titik dan normalisasi intensitas (lihat perbaikan 7 Nov).

## Bagian B — Essig IFC: sel T CD4 hidup vs mati (label ahli)
Protokol WO-14: LogReg, RF, SVM; GridSearch 3-fold di dalam data latih (validation), fold luar = testing.
Data: label ahli exp1 — 354 sel T hidup (T_cell, T_cell_with_signaling) vs 348 Dead_Cell, 2 donor. Fitur: brightfield saja.
Keluaran: `B_summary.csv`, `B_metrics.json`, `B_effect_size_bf.csv`.

| Fitur | Skema | LogReg | RF | SVM |
|---|---|---|---|---|
| Brightfield (tanpa ukuran citra) | k-fold 5 per sel | 0,945 | 0,961 | 0,954 |
| Brightfield (tanpa ukuran citra) | **Leave-one-donor-out** | **0,921** | **0,935** | **0,909** |
| Brightfield + ukuran citra | k-fold 5 per sel | 0,947 | 0,968 | 0,961 |
| Brightfield + ukuran citra | Leave-one-donor-out | 0,926 | 0,951 | 0,925 |

ROC AUC rata-rata fold. *Balanced accuracy* donor baru 0,86–0,88.
- Selisih per sel vs per donor kecil (≈ 0,02–0,05) → **sinyalnya nyata dan berlaku pada donor baru**, berbeda dengan heiDATA.
- Fitur paling membedakan (Cohen's d mati − hidup, konsisten di kedua donor): **gradien RMS brightfield** (d 1,5–1,8; ketajaman tepi /
  kontras refraktif), simpangan baku dan maksimum intensitas brightfield, energi GLCM (tekstur), eksentrisitas.
- Keterbatasan: hanya 2 donor berlabel ahli (2 fold berkelompok); kelas Dead_Cell dari anotator tidak dipastikan seluruhnya sel T.
