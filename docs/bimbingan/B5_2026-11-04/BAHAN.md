# Bahan Bimbingan 5 — Dataset, Hasil Pilot, dan Usulan Penyesuaian Topik
> Status eksekusi tugas dari bimbingan 1–4: lihat **`docs/WORK-ORDER.md`** (ditunjukkan di awal bimbingan).
> Arah penelitian mengikuti bimbingan 3–4: **ekstraksi fitur fisik/bio-optik** pembeda sel normal/terinfeksi/mati +
> **machine learning** (bukan deep learning).
Mahasiswa: Rahul Ghulam Hidayatulloh (23/519760/TK/57266) · Pembimbing: Nopriadi, S.T., M.Sc.
Judul (Simaster): Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra *Imaging Flow Cytometry* Menggunakan *Machine Learning*

## 1. Masalah: dataset sesuai judul tidak tersedia
- Dataset harus dicari sendiri. Penelusuran repositori publik (BBBC, BioStudies, Dryad, FlowRepository, heiDATA, literatur):
  **tidak ada dataset citra *imaging flow cytometry* (IFC) sel T CD4 terinfeksi HIV** dengan label sehat/terinfeksi/lisis.
- Yang tersedia terbagi tiga jenis:

| Dataset | Bentuk data | HIV? | Sel CD4 primer? | Catatan |
|---|---|---|---|---|
| **heiDATA – Ananth et al. 2024** (*Cell Reports*), CC BY 4.0 | **Citra mikroskopi fluoresens 3D** (Lamin B1, kapsid HIV-1, GFP) | ✅ +Vpx / −Vpx / Mock | ✅ sel T CD4 istirahat | Paling cocok konsep; data kecil |
| Dryad – Essig et al. 2022 | Citra IFC (ImageStream), > 2,8 juta citra | ❌ (kondisi stimulasi) | ✅ sel T CD4 memori | Cocok untuk *pretraining* |
| Dryad – Luo et al. 2023 (*Front. Immunol.* 2022) | Tabel CyTOF (FCS), tanpa citra | ✅ kultur terinfeksi vs tidak | ✅ sel tonsil | Bukan optika; tanpa citra |

Detail lengkap: `docs/DATASET-KANDIDAT.md`.

## 2. Dataset utama yang diusulkan: heiDATA (Ananth et al. 2024)
- Sel T CD4 istirahat terinfeksi HIV-1 (NLENG GFP p6mod), dengan/tanpa Vpx, dan kontrol Mock.
- Citra z-stack 31–36 irisan × 3–4 kanal × 512×512 px, 16-bit, 0,133 µm/px. **Kanal Lamin B1 ada di semua citra** (sesuai proposal).
- Kanal lain: kapsid HIV-1 (CA), reporter GFP, CPSF6/SC35, EdU.
- Keterbatasan: **14 bidang pandang** (1 per kondisi per figure paper); sel GFP+ (terinfeksi produktif) sangat sedikit; tanpa penanda kematian/lisis.

## 3. Hasil pilot (studi kelayakan, bukan hasil akhir)
- Segmentasi inti otomatis dari kanal Lamin B1 → **209 sel** (+Vpx 77, −Vpx 93, Mock 39). Contoh overlay: `results/pilot-heidata/overlays/`.
- Fitur per sel: morfometri inti (luas, keliling, eksentrisitas, soliditas, sirkularitas), intensitas & rasio tepi/inti Lamin B1,
  jumlah titik kapsid HIV di dalam inti dan di sekitar inti.
- Klasifikasi dengan validasi *leave-one-figure-out* (sel dari satu percobaan tidak pernah dipakai saat latih) + uji permutasi label:

Sumber angka: `results/pilot-heidata/metrics_classify.json` (100 permutasi, seed 42).

| Tugas | n sel | Model | *Balanced accuracy* | ROC AUC | p (permutasi) |
|---|---|---|---|---|---|
| T1a: +Vpx vs −Vpx — morfometri Lamin B1 saja | 170 | LogReg / RF | 0,544 / 0,559 | 0,544 / 0,584 | 0,248 / 0,059 |
| T1b: +Vpx vs −Vpx — Lamin B1 + titik kapsid HIV | 132 | LogReg / RF | 0,617 / 0,626 | **0,651** / 0,566 | **0,010** / 0,149 |
| T2: terpapar HIV (±Vpx) vs Mock — Lamin B1 | 209 | LogReg / RF | 0,326 / 0,379 | 0,172 / 0,084 | 1,0 / 1,0 |

Interpretasi awal:

- Morfometri inti saja hampir tidak membedakan +Vpx/−Vpx antar-percobaan (sinyal lemah).
- Menambah fitur **lokasi kapsid HIV** memberi sinyal yang **signifikan namun sedang** (AUC 0,65; p = 0,01) — sejalan dengan
  topik paper (tahap pasca-masuk HIV-1). Fitur terpenting (SHAP): panjang sumbu mayor inti dan jumlah kapsid di sekitar inti.
- T2 gagal (AUC jauh < 0,5): Mock hanya ada di 2 bidang pandang dari 2 percobaan berbeda, sehingga model mempelajari
  **perbedaan antar-percobaan (efek *batch*)**, bukan kondisi sel. → Data Mock terlalu sedikit; efek *batch* harus ditangani.
- Kesimpulan pilot: data heiDATA **layak tetapi terbatas**; jalan keluar utama = **data tambahan dari pemilik dataset** dan
  penambahan fitur bio-optik (tekstur, multi-kanal, 3D) untuk ML.

- Variasi **normalisasi fitur per percobaan** (`metrics_classify_norm-figure.json`) memperburuk semua tugas (AUC 0,17–0,44):
  normalisasi di dalam percobaan yang berisi campuran +Vpx/−Vpx ikut menghapus perbedaan antar-kondisi, apalagi dengan hanya
  6 percobaan (4D hanya −Vpx). → Efek *batch* tidak bisa "dikoreksi" secara statistik dengan data sekecil ini; yang dibutuhkan
  adalah **lebih banyak bidang pandang per kondisi**.

### 3b. Pilot komponen CyTOF (Luo et al.) — data tabel, tanpa citra
Sumber angka: `results/pilot-luo/metrics_classify.json`, `results/pilot-luo/state_counts.csv` (subsampel 40.000 sel/file, seed 42).

- 19 file FCS, 6 donor, 924.121 sel total. Kanal **HIV** ada di semua file → **status infeksi per sel**; **caspase-3 terbelah**
  (apoptosis) juga tersedia di semua file setelah nama penanda diseragamkan.
- *Gating* sel T CD4: CD3 > 3 dan CD8 < 2 (arcsinh; CD8− dipakai karena HIV menurunkan CD4) → 185.208 sel (subsampel).
- Ambang HIV+ = 2,0: kultur tak terinfeksi hanya 0–5 sel "HIV+" per donor vs 682–1.677 per donor di kultur terinfeksi.
- **Kelas per sel yang bisa dibentuk**: sehat (HIV−, Casp3−), **terinfeksi (HIV+)**, **apoptosis (Casp3+ HIV−)** — mendekati
  konsep proposal sehat/terinfeksi/lisis (kelas apoptosis kecil: 31–265 sel per donor pada kultur terinfeksi).
- Klasifikasi HIV+ vs HIV− dari penanda permukaan (kanal HIV/p24/penanda status tidak dipakai), validasi *leave-one-donor-out*:

| Varian fitur | Model | ROC AUC | PR AUC (acak = 0,072) | *Balanced accuracy* |
|---|---|---|---|---|
| Dengan CD4 | LogReg / HistGB | 0,900 / **0,915** | 0,623 / 0,702 | 0,843 / 0,852 |
| Tanpa CD4 | LogReg / HistGB | 0,833 / **0,847** | 0,394 / 0,531 | 0,780 / 0,779 |

- SHAP (HistGB, tanpa CD4): PD1, CD127, CD2, CD62L, HLA-DR, CTLA4 terpenting. Catatan: CD19 ikut muncul pada sel yang di-*gating*
  sebagai sel T → kemungkinan *doublet*/limpahan sinyal; perlu diperiksa.
- Kesimpulan: komponen CyTOF **sinyal kuat & konsisten antar-donor**, tetapi **tanpa citra** (tidak ada Grad-CAM/aspek optika).

### 3c. Komponen pretraining (Essig et al., IFC)
- `exp1.zip` (19,58 GB, ukuran cocok dengan Dryad): **480.000 citra sel tunggal** = 2 donor × 4 kondisi (+SEA, −SEA, Isotype,
  Teplizumab) × 60.000; tiap sel `.h5` berisi `image` (≈50–100 px × 8 kanal, uint16) + `mask`.
  Kanal 0 = *brightfield* (diverifikasi visual); kanal 1–7 = fluoresens (nama penanda per kanal: lihat README Dryad).
  Banyak citra berupa konjugat sel T–sel B (sinapsis imun).
- Pilot: CNN kecil di-*pretrain* pada 24.000 sel Essig (1 kanal fluoresens acak per sel), lalu di-*fine-tune* pada potongan
  sel tunggal heiDATA (Lamin B1) untuk +Vpx vs −Vpx (*leave-one-figure-out*), dibandingkan CNN dari nol, + Grad-CAM.

- Hasil: pretraining berjalan, tetapi proses berhenti saat evaluasi karena memori RAM tidak cukup (bug sudah diperbaiki).
  **Tidak dijalankan ulang** karena bimbingan 4 sudah memutuskan *machine learning*, bukan *deep learning*. Data Essig tetap
  berguna bila nanti diperlukan sebagai sumber fitur bio-optik IFC (brightfield + fluoresens) untuk pembanding.

## 4. Tiga skema penggunaan dataset
| Skema | Isi | Estimasi kerja |
|---|---|---|
| 1 | Pretraining CNN pada citra IFC Essig → *fine-tuning* pada heiDATA (+ ML klasik fitur morfometri, Grad-CAM) | ±5–6 minggu |
| 2 | Analisis citra heiDATA + analisis CyTOF Luo (ML + SHAP) | ±6–7 minggu |
| 3 | Gabungan 1 + 2 | ±8–10 minggu |

Dataset tidak bisa digabung menjadi satu set latih (modalitas & label berbeda). Pilot Skema 3 telah dijalankan untuk menilai kelayakan.

**Catatan keselarasan dengan bimbingan 4:** Skema 1 memakai CNN (*deep learning*), padahal bimbingan 4 memutuskan **machine learning**.
Karena itu inti yang diusulkan = **ekstraksi fitur + ML** (heiDATA, ditambah data CyTOF bila perlu); CNN/Grad-CAM paling jauh hanya
sebagai pembanding opsional. Pilot CNN sempat dijalankan tetapi gagal karena memori (sudah diperbaiki, tidak dijalankan ulang).

## 5. Kecocokan judul & usulan judul pengganti (draf untuk didiskusikan)
Tidak ada satu dataset yang memenuhi semua unsur judul; unsur yang paling bermasalah adalah **"citra imaging flow cytometry"**.

| Unsur judul/proposal | heiDATA | CyTOF Luo | IFC Essig |
|---|---|---|---|
| Sel (T) CD4 | ✅ | ✅ | ✅ |
| Infeksi HIV | ✅ | ✅ | ❌ |
| Citra IFC | ❌ (mikroskopi fluoresens) | ❌ (tanpa citra) | ✅ |
| Kondisi sehat/terinfeksi/lisis | ⚠️ +Vpx/−Vpx/Mock | ✅ sehat/HIV+/apoptosis per sel | ❌ |
| Lamin B1, morfometri | ✅ | ❌ | ⚠️ |
| Grad-CAM, Bidang II Sistem Optika | ✅ | ❌ (SHAP; spektrometri massa) | ✅ |

Usulan (template: judul ≤ 15 kata):

- **A — perubahan minimal, heiDATA (ekstraksi fitur + ML):** *Klasifikasi Kondisi Sel T CD4 pada Infeksi HIV-1 Berdasarkan Citra Mikroskopi
  Fluoresens Menggunakan Machine Learning* (15 kata) — EN: *Classification of CD4 T Cell Conditions in HIV-1 Infection Based on
  Fluorescence Microscopy Images Using Machine Learning*
- **B — dua sumber data (Skema 2/3):** *Klasifikasi Kondisi Sel T CD4 pada Infeksi HIV-1 Berbasis Citra Mikroskopi Fluoresens dan Mass Cytometry* (15 kata)
- **C — fokus CyTOF (sinyal pilot terkuat; tanpa citra, Bidang II perlu diganti):** *Klasifikasi Kondisi Sel T CD4 Terinfeksi HIV-1
  Berbasis Data Mass Cytometry Menggunakan Explainable Machine Learning* (15 kata)

Rekomendasi mahasiswa: **A** (perubahan minimal, bidang keilmuan tetap, Lamin B1 + fitur bio-optik + ML sesuai arahan B3–B4) dengan upaya menambah data heiDATA;
**B** bila pembimbing mengutamakan hasil kuat & konsep sehat/terinfeksi/apoptosis. Prosedur perubahan judul (*fast-track*) ditanyakan.

## 5b. Opsi tambahan (disusun 4 Nov 2026): D — Essig sebagai inti, E — satu kerangka ML untuk tiga dataset

### Opsi D — Essig (citra IFC) dengan ekstraksi fitur + machine learning
- Essig **dapat diolah dengan ML** (bukan hanya *deep learning*): tiap sel sudah memiliki **mask** dari peneliti asli, sehingga tidak
  perlu segmentasi. Pilot CNN sebelumnya gagal karena metodenya (DL + RAM laptop), bukan karena datanya.
- **Fitur per sel (8 kanal: kanal 0 *brightfield*, kanal 1–7 fluoresens):** morfometri dari mask (luas, keliling, eksentrisitas,
  soliditas, sirkularitas); intensitas per kanal (rata-rata, simpangan baku, maksimum, total); tekstur GLCM/Haralick (kontras,
  homogenitas, entropi) pada *brightfield* & fluoresens; distribusi spasial (rasio tepi/tengah sel); kolokalisasi antar-kanal (korelasi Pearson).
- **Metode:** Random Forest / gradient boosting / SVM / Logistic Regression; validasi *leave-one-donor-out* (exp1 = 2 donor;
  exp2–exp4 menambah donor); interpretasi SHAP / *permutation importance*. Sampel ±2.000–10.000 sel per kondisi (Colab/laptop).
- **Kelas:** kondisi stimulasi/aktivasi sel T CD4 (+SEA, −SEA, Isotype, Teplizumab) — **bukan infeksi HIV**.
- **Kecocokan judul:** paling dekat dengan judul Simaster (citra IFC + sel CD4 + ML); yang hilang hanya unsur infeksi HIV.
- Judul D (14 kata): *Klasifikasi Kondisi Aktivasi Sel T CD4 Berdasarkan Citra Imaging Flow Cytometry Menggunakan Machine Learning*.
- Kanal (dicek 4 Nov; README Dryad tidak memuat nama kanal, urutan diambil dari notebook penulis): 0 brightfield · 1 Antibody · 2 CD18 · 3 F-Actin ·
  4 MHCII · 5 CD3 · 6 P-CD3ζ · 7 Live-Dead. Setiap citra = konjugat sel T CD4 memori + sel B (sinapsis imunologis). Kanal Live-Dead membuka kemungkinan kelas sel mati.
- Catatan kebaruan: paper aslinya (Shetab Boushehri dkk., Nat Commun 14:7888, 2023) sudah memakai ekstraksi fitur + ML (XGBoost, F1-macro 0,92).
  Karena itu skripsi perlu sudut sendiri, misalnya tafsiran fisis/bio-optik, kelas hidup vs mati dari Live-Dead, atau fitur brightfield saja (label-free).

#### Hasil pilot D (4 Nov 2026; exp1, 2 donor, validasi *leave-one-donor-out*; `results/pilot-essig/`)
- **Label kondisi stimulasi gagal.** +SEA vs −SEA menghasilkan AUC 0,44–0,49 (acak = 0,5). Untuk 4 kondisi, *balanced accuracy* dengan brightfield
  0,25–0,27 (acak = 0,25). Dengan semua kanal naik ke 0,56–0,59, tetapi kenaikan itu didorong kanal *Antibody* (artefak pewarnaan).
  Penyebabnya, label kondisi berlaku per tabung, bukan per sel, dan hanya sebagian kecil sel yang membentuk sinapsis. → Judul D ("kondisi aktivasi") **tidak disarankan**.
- **Sel mati dikenali dari brightfield saja (tanpa pewarnaan).**
  - Pada 12.000 sel dengan label dari ambang Live-Dead: AUC 0,94 (LogReg) / 0,96 (RF).
  - **Validasi dengan label ahli** (354 sel T hidup vs 348 *Dead_Cell*): AUC **0,92 / 0,95**, uji permutasi p = 0,02.
    Label ambang Live-Dead cocok 96% dengan label ahli (kappa 0,92).
- **Fitur terpenting:** *gradient RMS* brightfield (ketajaman tepi/kontras optik sel), intensitas maksimum dan simpangan baku brightfield,
  serta ukuran citra (proksi ukuran objek). Tafsiran fisis yang mungkin: perubahan membran/struktur sel mati mengubah kontras fase/hamburan
  pada brightfield (hipotesis, perlu pustaka).
- **Usulan judul D′ (16 kata):** *Identifikasi Sel T CD4 Mati Berdasarkan Fitur Bio-Optik Citra Brightfield Imaging Flow Cytometry Menggunakan Machine Learning*.
- **Keterbatasan:**
  - Belum ada kelas terinfeksi HIV.
  - Baru 2 donor (exp2–exp4 menambah 7 donor).
  - Kebaruan terhadap paper asli ada pada fokus *label-free* brightfield + tafsiran fisis; paper asli memakai semua kanal untuk tipe sinapsis.
- **Catatan rekomendasi:** dari sisi data, D′ sekarang kandidat terkuat: efeknya besar, tervalidasi antar-donor dan dengan label ahli, serta sesuai
  "citra IFC + ML + fitur fisik". Keputusan tetap pada pembimbing.
- **Kandidat pelengkap kelas terinfeksi: FlowRepository FR-FCM-Z8VC.**
  - Isi: sel T CD4 primer diinfeksi 4 strain HIV vs mock, 6 donor, 24/48/72 jam, gate Gag p24⁺CD4⁻, 1.152 FCS (2,2 GB).
  - Flow cytometry, bukan citra. Panel live/dead dan FSC/SSC belum dicek (unduhan butuh CAPTCHA/login).
  - **Status 5 Nov 2026: ditunda** — unduhan terlalu sulit (CAPTCHA/login); tidak dipakai untuk bimbingan 5.

### Opsi E — satu pipeline ML, tiga studi, satu benang merah
Ketiga dataset **tidak dapat digabung menjadi satu model/tabel** (fitur, label, dan sel berbeda → model akan mengenali asal dataset).
Yang dapat dilakukan: **pipeline ML yang sama** (segmentasi/mask → ekstraksi fitur → klasifikasi → SHAP → tafsiran fisis)
diterapkan pada tiga studi yang saling melengkapi:

```
            SATU PIPELINE ML (dipakai di tiap dataset)
  segmentasi/mask → ekstraksi fitur → klasifikasi ML → SHAP → tafsiran fisis
        │                     │                        │
   [A] Essig (IFC)       [B] CyTOF Luo            [C] heiDATA (mikroskopi)
   fitur bio-optik       penanda protein          fitur inti (Lamin B1) &
   sel T CD4 teraktivasi pembeda sel HIV+ /       kapsid pada sel istirahat
   vs istirahat          apoptosis                terpapar HIV
        └──────────────────────┴────────────────────────┘
        Benang merah: AKTIVASI SEL T CD4 ↔ KERENTANAN TERHADAP HIV
```

- Dasar benang merah: HIV lebih mudah menginfeksi sel T CD4 teraktivasi, sel istirahat lebih sulit (antara lain karena SAMHD1;
  karena itu heiDATA memakai Vpx) — perlu disitasi dari literatur. Pilot CyTOF: penanda terpenting untuk sel HIV+ adalah PD1, HLA-DR,
  CTLA4, CD127 (aktivasi/memori).
- Pertanyaan pemersatu: *karakteristik fisik/bio-optik apa yang menandai kondisi sel T CD4 dan kaitannya dengan infeksi HIV?*
- Hasil gabungan = **perbandingan lintas studi** (mis. apakah fitur pembeda aktivasi di Essig sejalan dengan penanda aktivasi yang
  memprediksi infeksi di CyTOF) — berupa **hipotesis** yang dilaporkan apa adanya, bukan satu angka akurasi.

| Aspek | Opsi E |
|---|---|
| Arahan pembimbing (B3–B4) | ✅ ekstraksi fitur + ML di semua studi; kelas terinfeksi & mati tersedia di CyTOF |
| Kecocokan judul | Sebagian: citra IFC (Essig), HIV (CyTOF, heiDATA); judul perlu diarahkan ke "aktivasi & infeksi" |
| Beban kerja | ±6–8 minggu (pipeline sama; CyTOF & heiDATA sudah dipilot) + Bab 2 mencakup IFC, mikroskopi, CyTOF → **sangat ketat** untuk Desember |
| Risiko | Benang merah belum tentu terlihat di data; cakupan bisa dinilai terlalu lebar |

Saran: bila opsi E dipilih, tetapkan **satu studi sebagai inti** (mis. Essig karena sesuai judul IFC + ML), CyTOF sebagai penghubung
ke HIV, heiDATA sebagai pendukung singkat — cakupan akhir diputuskan pembimbing.

## 6. Keputusan yang diminta dari pembimbing
1. Setuju dataset utama heiDATA (citra mikroskopi, bukan IFC)? Perlukah perubahan judul diajukan ulang di Simaster (*fast-track*)?
2. Kelas klasifikasi: +Vpx / −Vpx / Mock (kondisi infeksi) sebagai pengganti sehat/terinfeksi/lisis — dapat diterima?
3. Opsi/skema yang dipilih: A (heiDATA), B (heiDATA + CyTOF), C (CyTOF), **D (Essig, citra IFC + ML)**, atau
   **E (satu kerangka ML untuk tiga studi; tentukan studi inti)**?
4. Perlukah menghubungi pemilik dataset heiDATA untuk meminta citra tambahan?
5. Target periode ujian (tengah/akhir semester) dan tenggat pendaftaran.
6. Pembimbing pendamping: ada atau tidak? NIP pembimbing untuk halaman pengesahan.
7. Judul Bab 3: "Metodologi Penelitian" atau "Pelaksanaan Penelitian" (template)?
