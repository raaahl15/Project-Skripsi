# Dokumentasi Pemrosesan Data & Fitur yang Diekstrak
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**
Terakhir diperbarui: **4 Nov 2026** · Terkait: WO-07 (ekstraksi fitur), WO-08 (metode ML), WO-09 (dataset), WO-10 (fitur)
> Status: **pilot / studi kelayakan** (3 Nov 2026), bukan hasil akhir skripsi.

## 1. Di mana pemrosesan dilakukan
| Aspek | Keterangan |
|---|---|
| Perangkat | **Laptop utama** (Windows 10 Pro), Intel Core i5-2500S 2,7 GHz (4 inti logis), RAM 7,9 GB, **tanpa GPU** |
| Lingkungan | Python 3.13 di `.venv` repo (numpy, scikit-image, scikit-learn, pandas, tifffile, flowio, shap, torch CPU) |
| Lokasi kode | Repo `skripsi-ml/` (GitHub `raaahl15/Project-Skripsi`): `src/`, `notebooks/` |
| Lokasi data mentah | Laptop: `data/raw/` (tidak di-commit). Cadangan zip: Google Drive `Project-Skripsi/data/raw/` |
| Lokasi hasil | Repo `results/` (angka, tabel, gambar — boleh dikutip di naskah) |
| Cloud (Colab/Kaggle) | **Belum dipakai** — semua pilot berjalan di CPU laptop |

## 2. Ringkasan per dataset
| Dataset | Data mentah (laptop) | Skrip | Keluaran | Waktu proses (perkiraan) |
|---|---|---|---|---|
| **heiDATA** (Ananth et al. 2024) — citra mikroskopi fluoresens 3D | `data/raw/heidata-MUXYRY/` (dari `dataverse_files.zip`, 736 MB) | `notebooks/00_…metadata.py`, `notebooks/01_…hitung_inti.py`, `src/pilot_heidata_features.py`, `src/pilot_heidata_classify.py` (modul `src/data/heidata.py`, `src/data/heidata_cells.py`) | `results/eksplorasi-heidata/`, `results/pilot-heidata/` (cells.csv, overlays/, labels/, metrics_classify*.json, shap_*.png) | Segmentasi + fitur: beberapa menit; klasifikasi + 100 permutasi: ±40 menit per varian |
| **CyTOF Luo** (Luo et al. 2022) — tabel mass cytometry (FCS) | `data/raw/dryad-luo-2023/` (dari zip 1,27 GB) | `src/pilot_luo_inspect.py`, `src/pilot_luo_classify.py` (modul `src/data/luo_cytof.py`) | `results/pilot-luo/` (inventory.csv, panel.csv, state_counts.csv, metrics_classify.json, shap_L1_*.png) | Beberapa menit |
| **IFC Essig** (Essig et al. 2022) — citra IFC sel tunggal | `exp1.zip` (19,58 GB) dibaca langsung dari `C:\Users\Qenuarally\Downloads\` (belum dipindah ke `data/raw/`) | `src/pilot_cnn_transfer.py` (modul `src/data/essig.py`, `src/models/cnn.py`) | `data/processed/essig_pretrain_64.npz` (24.000 citra 64×64, 242 MB) | Penyiapan citra ±6 menit; *pretraining* CNN >1 jam lalu **gagal (RAM tidak cukup)** — tidak dilanjutkan (keputusan B4: ML, bukan DL) |

## 3. heiDATA — alur pemrosesan
1. **Baca citra**: z-stack TIFF (Z × kanal × 512 × 512 px, 16-bit, **0,133 µm/px**); indeks kanal dari `README.rtf` dataset
   (Lamin B1, HIV-1 CA, HIV-1 GFP, dll.). 14 bidang pandang: +Vpx (5), −Vpx (7), Mock (2).
2. **Proyeksi intensitas maksimum** (MIP) sepanjang Z untuk tiap kanal → citra 2D.
3. **Normalisasi** persentil (1–99,8%) agar offset kamera (±1.900 hitungan) tidak berpengaruh.
4. **Segmentasi inti dari kanal Lamin B1** (`segment_nuclei_classical`): transformasi log → Gaussian (σ = 1,5 px) → ambang lokal
   (blok 151 px) dan ambang global (0,6 × Otsu) → *closing* (disk 4 px) → isi lubang (Lamin B1 berbentuk cincin) → *opening* (disk 3 px)
   → pemisahan inti yang bersentuhan (*watershed* jarak).
5. **Filter objek**: diameter setara 3–12 µm, **soliditas ≥ 0,88** (inti sel T istirahat kompak/cembung), objek terpotong tepi citra dibuang
   → **209 sel** (+Vpx 77, −Vpx 93, Mock 39). Validasi visual: `results/pilot-heidata/overlays/`.
6. **Deteksi titik kapsid HIV-1** (kanal CA; Fig 1G, 3B, 4D, S3B): *Laplacian of Gaussian* (σ 1–3 px, ambang 0,08 pada citra ternormalisasi).
7. **Ekstraksi fitur per sel** (`cell_features`) → `results/pilot-heidata/cells.csv` (1 baris = 1 sel).
8. **Klasifikasi** (`pilot_heidata_classify.py`): Logistic Regression & Random Forest; imputasi median; validasi
   *leave-one-figure-out*; 100 permutasi label; SHAP (Random Forest).

### 3.1 Fitur yang diekstrak (heiDATA)
| # | Fitur (kolom) | Kanal | Cara hitung | Satuan | Makna fisis/biologis | Dipakai di |
|---|---|---|---|---|---|---|
| 1 | `area_um2` | Lamin B1 | jumlah piksel inti × (0,133 µm)² | µm² | ukuran inti | T1a, T1b, T2 |
| 2 | `perimeter_um` | Lamin B1 | keliling kontur inti | µm | ukuran & kekasaran batas inti | T1a, T1b, T2 |
| 3 | `eq_diameter_um` | Lamin B1 | diameter lingkaran berluas sama | µm | ukuran inti | T1a, T1b, T2 |
| 4 | `major_axis_um` | Lamin B1 | sumbu mayor elips bermomen sama | µm | elongasi inti | T1a, T1b, T2 |
| 5 | `minor_axis_um` | Lamin B1 | sumbu minor elips bermomen sama | µm | lebar inti | T1a, T1b, T2 |
| 6 | `eccentricity` | Lamin B1 | eksentrisitas elips (0 = lingkaran) | — | bentuk lonjong vs bulat | T1a, T1b, T2 |
| 7 | `solidity` | Lamin B1 | luas / luas *convex hull* | — | lekukan/deformasi batas inti | T1a, T1b, T2 |
| 8 | `circularity` | Lamin B1 | 4π·luas / keliling² | — | kebulatan inti | T1a, T1b, T2 |
| 9 | `lamin_mean` | Lamin B1 | rata-rata intensitas di dalam inti | hitungan (a.u.) | jumlah/kepadatan Lamin B1 | T1a, T1b, T2 |
| 10 | `lamin_std` | Lamin B1 | simpangan baku intensitas di inti | a.u. | heterogenitas distribusi lamina | T1a, T1b, T2 |
| 11 | `lamin_rim_core_ratio` | Lamin B1 | rata-rata intensitas tepi (±0,5 µm) / bagian tengah inti | — | keutuhan "cincin" lamina | T1a, T1b, T2 |
| 12 | `ca_puncta_nucleus` | HIV-1 CA | jumlah titik kapsid di dalam batas inti | buah | kapsid yang sudah masuk inti | T1b |
| 13 | `ca_puncta_perinuclear` | HIV-1 CA | jumlah titik kapsid pada cincin 1,5 µm di luar inti | buah | kapsid di sekitar inti/sitoplasma | T1b |
| 14 | `gfp_mean` | HIV-1 GFP | rata-rata intensitas GFP di inti | a.u. | penanda infeksi produktif | dicatat, **belum dipakai** (sel GFP+ sangat sedikit) |

Fitur 1–11 tersedia untuk 209 sel; 12–13 untuk sel di Fig 1G/3B/4D/S3B; 14 untuk Fig 2A/2D/3B/4D/S3B.
Tugas: **T1a** +Vpx vs −Vpx (fitur 1–11) · **T1b** +Vpx vs −Vpx (1–13) · **T2** terpapar HIV vs Mock (1–11).

## 4. CyTOF Luo — alur pemrosesan
1. **Baca 19 file FCS** (6 donor; kultur terinfeksi & tak terinfeksi; sudah di-*gating* sel hidup oleh penulis) dengan `flowio`;
   subsampel 40.000 sel/file (seed 42); nama penanda diseragamkan antar-donor (mis. `Casp3`/`Cas3_cleaved` → `Casp3_cleaved`).
2. **Transformasi arcsinh** (kofaktor 5) — standar mass cytometry.
3. **Gating sel T CD4**: CD3 > 3 dan CD8 < 2 → 185.208 sel (CD8− dipakai karena HIV menurunkan ekspresi CD4).
4. **Label per sel**: HIV+ jika kanal HIV > 2,0 (kultur tak terinfeksi: persentil 99,9 = 1,2–1,6); apoptosis jika Casp3_cleaved > 1,894
   (persentil 99 kultur tak terinfeksi) dan HIV−.
5. **Klasifikasi** HIV+ vs HIV− pada kultur terinfeksi (103.341 sel; 7.405 HIV+): Logistic Regression & HistGradientBoosting;
   validasi *leave-one-donor-out*; SHAP.

### 4.1 Fitur yang dipakai (CyTOF) — 29 penanda permukaan (intensitas arcsinh per sel)
HLA-DR, CTLA4, CD69, CXCR3, CXCR5, CD27, CD8, CD3, CD2, CD62L, CCR6, CD29, OX40, CD28, CD127, CXCR4, CD45RA, CCR5, ICOS, CD19, CD7,
CCR4, CD45RO, CCR7, CD25, PD1, CD38, **CD4**, CD57. Varian "tanpa CD4" memakai 28 penanda.
**Tidak dipakai sebagai fitur** (agar tidak "bocor"): kanal HIV, KC57/p24, Casp3_cleaved, LiveDead, CD95, BST2, SAMHD1, IFI16.
Catatan: fitur CyTOF adalah **ekspresi protein**, bukan fitur optik/citra.

## 5. IFC Essig — alur pemrosesan (pilot CNN, dihentikan)
1. Baca `.h5` langsung dari `exp1.zip` (480.000 sel; 2 donor × 4 kondisi; 8 kanal, kanal 0 = *brightfield*).
2. Sampel 24.000 sel (3.000 per donor × kondisi); 1 kanal fluoresens acak per sel → *padding* persegi → 64 × 64 px → normalisasi.
3. *Pretraining* CNN kecil (4 kelas kondisi) → **berhenti karena RAM tidak cukup** saat evaluasi (bug sudah diperbaiki).
**Belum ada fitur bio-optik yang diekstrak dari Essig.** Bila dipakai nanti (sesuai arahan ML): fitur morfometri & intensitas per kanal
(*brightfield*, fluoresens) dengan cara serupa heiDATA.

## 6. Cara menjalankan ulang (dari root repo, di laptop)
```powershell
.\.venv\Scripts\python.exe src\pilot_heidata_features.py --seg classical
.\.venv\Scripts\python.exe src\pilot_heidata_classify.py               # tambah --norm figure untuk varian normalisasi
.\.venv\Scripts\python.exe src\pilot_luo_inspect.py
.\.venv\Scripts\python.exe src\pilot_luo_classify.py
.\.venv\Scripts\python.exe src\pilot_cnn_transfer.py --essig-zip <path ke exp1.zip>   # tidak dianjurkan di laptop 8 GB RAM
```
Semua skrip memakai *seed* tetap (42) agar hasil dapat direproduksi.
