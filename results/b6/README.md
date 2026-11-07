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

**Pemeriksaan kanal kapsid (`A_capsid_sanity.csv`) — temuan penting**
| Percobaan | Kondisi | Median titik kapsid di inti |
|---|---|---|
| 1G | +Vpx / −Vpx / **Mock** | 19 / 10,5 / **124** |
| S3B | +Vpx / −Vpx / Mock | 2,5 / 3,5 / 6 |

Sel Mock (tidak diberi virus) seharusnya hampir tanpa kapsid, tetapi di 1G justru paling banyak. Artinya detektor titik (LoG) menghitung
derau/latar, atau kanal Mock 1G berbeda. **Fitur kapsid belum dapat dipercaya** → hasil pilot T1b dan SHAP "kapsid di sekitar inti"
perlu diperiksa ulang (lihat overlay citra), dan label "terinfeksi per sel dari kapsid" (ide 2b) **tidak dijalankan**.
Normalisasi fitur per percobaan (ide 2a) sudah diuji di pilot (`results/pilot-heidata/metrics_classify_norm-figure.json`): AUC 0,17–0,44, tidak membantu.

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
