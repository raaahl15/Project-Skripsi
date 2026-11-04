# Kandidat Dataset (penelusuran 2026-11-03)

> Konteks: dataset harus dicari sendiri (tidak disediakan pembimbing/lab). Topik proposal: klasifikasi kondisi sel T CD4
> (sehat / terinfeksi HIV / lisis) dari citra *imaging flow cytometry* (IFC) multi-kanal + Grad-CAM.
> Semua data di bawah diverifikasi langsung dari halaman sumbernya; yang tidak tercantum ditulis "tidak disebutkan".

## Temuan utama
**Tidak ditemukan dataset IFC publik berisi sel CD4 terinfeksi HIV** (dengan label sehat/terinfeksi/lisis). Pencarian
literatur & repositori (BBBC, BioStudies, Dryad, Zenodo/figshare via mesin pencari) hanya menemukan dataset IFC sel T/limfosit
dengan label lain. Review terbaru IFC dalam riset HIV (Methods Protoc 2025, DOI 10.3390/mps8010014) juga tidak menyebut dataset publik.
→ Topik perlu **disesuaikan dengan data yang tersedia** atau data harus **diakuisisi di lab** (tidak realistis untuk tenggat Desember).
Panduan §1.3 mengizinkan penggantian topik lewat *fast-track approval* jika topik semester 6 tidak dapat dilanjutkan.

## Kandidat

### 1. Dryad — IFC sinaps imunologis sel T CD4 memori (paling dekat secara biologis)
- Judul: "An imaging flow cytometry dataset for profiling the immunological synapse of therapeutic antibodies"
- Sel: **sel T CD4+ memori manusia** (9 donor sehat) dikokultur dengan sel B-LCL. Instrumen: Amnis ImageStreamX Mark II, 60×.
- Kelas/kondisi: −SEA, +SEA, Teplizumab, CD19-TCB, CD20-TCB (kondisi stimulasi/aktivasi, bukan infeksi).
- Kanal: brightfield + fluoresens (CD3-BV421, HLA-DR-PE-Cy7, Phalloidin AF594, P-CD3ζ Y142-AF647); viability dye eF780.
  Gating memakai "in-focus live+ CD3+ MHCII+ cells" → kemungkinan **sel mati tidak disertakan**.
- **Diperiksa 4 Nov 2026.** README Dryad sudah dibaca (salinan: `docs/dataset/essig-dryad-README.md`), tetapi tidak memuat nama kanal.
  - **Urutan 8 kanal** (sumber: notebook penulis `scifAI-notebooks`, `Data exploration.ipynb`): 0 BF · 1 Antibody · 2 CD18 · 3 F-Actin · 4 MHCII ·
    5 CD3 · 6 P-CD3ζ · 7 Live-Dead. Kanal 0 = BF sudah dicek visual. Pemetaan Ch1–8 ke indeks 0–7 masih asumsi.
  - Setiap citra adalah **konjugat sel T–B (sinapsis imunologis)**: sel T CD4 memori + sel B-LCL (EBV-transformed, bukan Raji). SEA = superantigen
    *Staphylococcal enterotoxin A*. Mask tersedia per kanal (biner).
  - **Label ahli** (`label`, str) hanya ada pada sebagian kecil citra. Di paper ada 5.221 citra beranotasi, dengan 9 kelas: single B-LCL, single T cell
    dengan/tanpa sinyal, synapse dengan/tanpa sinyal, multi-synapse, dll. Jumlah per kelas di exp1: lihat `results/eksplorasi-essig/label_counts_exp1.json`.
  - **Paper sudah melakukan ekstraksi fitur + ML** dan memakai paket scifAI (LogReg, LDA, SVM, RF, XGBoost). Yang terbaik XGBoost dengan
    F1-macro 0,92 ± 0,01, memakai fitur morfologi, intensitas/tekstur, kolokalisasi, dan sinaptik. → Skripsi dengan data ini perlu
    sudut pandang sendiri, misalnya fokus fisis/bio-optik, kanal Live-Dead untuk kelas sel mati, atau fitur brightfield saja (*label-free*).
- Jumlah: > 2,8 juta citra; format `.h5` (key `image`, `mask`, `label`); ukuran total **124,94 GB** (exp1 19,6 GB … exp4 42,7 GB).
- Lisensi: tidak disebutkan spesifik (footer Dryad: "licensed for reuse"). Unduhan langsung per file.
- Sitasi: Essig K., Shetab Boushehri S., Marr C. et al. (2022), Dryad, DOI 10.5061/dryad.ht76hdrk7;
  paper: Shetab Boushehri S. et al., *Nature Communications* (2023), DOI 10.1038/s41467-023-43429-2 (juga memakai *explainable ML*).
- Kecocokan: sel CD4 asli + IFC multi-kanal + ada preseden XAI; tetapi kelas = kondisi aktivasi, bukan infeksi/lisis.

- **Pilot ML (4 Nov 2026, `results/pilot-essig/`):**
  - Label kondisi (+SEA/−SEA/…) per sel **gagal** (AUC sekitar 0,5).
  - **Sel mati dari brightfield saja**: AUC 0,92–0,96 dengan *leave-one-donor-out*, tervalidasi dengan label ahli
    (354 T hidup vs 348 Dead_Cell, p = 0,02). Fitur teratas: gradient RMS brightfield.
  - Label ahli exp1: 2.641 dari 480.000 citra (0,55%), termasuk 348 Dead_Cell.

### 1b. FlowRepository FR-FCM-Z8VC — infeksi HIV pada sel T CD4 primer (flow cytometry spektral)
- Judul: "Analyzing NK cell ligand expression after HIV infection in human primary CD4 T cells".
  Peneliti: Ruoxi Pi; PI: Catherine Blish (Stanford). Eksperimen 2024-09-30 s.d. 2024-11-22. MIFlowCyt 97%. Belum ada manuskrip.
- Desain: 6 donor (RP51–RP58); strain HIV CH106, THRO, Q23-17, NL4-3, Mock, dan Freshly-isolated; 24/48/72 jam pascainfeksi.
  Satu tabung = satu ligan NK atau isotipe. Workspace FlowJo memakai gate **Gag p24⁺ CD4⁻**, jadi label terinfeksi per sel tersedia.
- Ukuran: 1.152 FCS (`_Unmixed.fcs`), 2,2 GB. Unduhan lewat http://flowrepository.org/experiments/9196/download_ziped_files
  (perlu CAPTCHA; unduhan per file perlu login).
- **Belum dicek:** pewarna live/dead dan FSC/SSC di panel.
- Kecocokan: kelas normal vs terinfeksi ✅ (mati: belum pasti); bukan citra.

### 2. BBBC048 — Siklus sel Jurkat (paling ringan, cepat dipakai)
- Judul: "Cell Cycle Jurkat Cells" (Broad Bioimage Benchmark Collection).
- Sel: **Jurkat (garis sel limfosit T)**, terfiksasi, diwarnai PI dan MPM2; ImageStream.
- Kelas: 7 fase siklus sel (G1, S, G2, profase, metafase, anafase, telofase). Jumlah per kelas tidak disebutkan.
  Paper menyebut subpopulasi **sel mati** dapat dipisahkan secara *unsupervised* (tidak ada label sel mati).
- Jumlah: 32.266 citra sel tunggal; `BBBC048v1.zip` **1,5 GB**, unduhan langsung tanpa login.
- Lisensi: CC BY-NC-SA 3.0 (penggunaan akademik non-komersial).
- Sitasi: Eulenberg P. et al., "Reconstructing cell cycle and disease progression using deep learning", *Nat Commun* 8, 463 (2017),
  DOI 10.1038/s41467-017-00623-3; + Ljosa et al., *Nat Methods* (2012), DOI 10.1038/nmeth.2083.
- Kecocokan: sel T + IFC + kecil; tetapi kelas = siklus sel.

### 3. BioStudies S-BIAD452 — Sel darah putih sehat (stain-free IFC)
- Judul: "Imaging flow cytometry dataset of healthy human white blood cells"; ImageStream-X MK II.
- Kelas: tipe sel darah putih (CD4+/CD8+ T, neutrofil, monosit, sel B, NKT, eosinofil). Tidak ada kelas sel mati.
- Kanal: brightfield, darkfield, 9 penanda fluoresens (termasuk CD4 BV605, CD3 BV421).
- Isi file: **dataframe fitur** (IDEAS, SCIP); ketersediaan citra mentah tidak disebutkan. Lisensi & ukuran: tidak disebutkan.
- Sitasi: Lippeveld M. et al., "Classification of Human White Blood Cells Using Machine Learning for Stain-Free Imaging Flow
  Cytometry", *Cytometry A* 97(3) (2020), PMID 31688997.
- Kecocokan: rendah untuk "kondisi sel"; berguna sebagai pembanding fitur morfometri.

## Kandidat temuan pengguna (dinilai 2026-11-03)

### 4. heiDATA doi:10.11588/DATA/MUXYRY — HIV-1 di sel T CD4 istirahat (Lamin B1) ⭐ paling relevan dengan proposal
- Metadata DataCite: "Spatial resolution of HIV-1 post-entry steps in resting CD4 T cells [data]", Ananth, Swetha, 2024, heiDATA.
  Deskripsi, lisensi, ukuran, format: **tidak diisi di metadata**; halaman heiDATA memblokir akses otomatis (bot-check) → perlu dibuka di browser.
- Paper terkait: *Cell Reports* (2024), "Spatial resolution of HIV-1 post-entry steps in resting CD4 T cells"
  (https://www.cell.com/cell-reports/fulltext/S2211-1247(24)00269-9). Paper memakai **Lamin B1** sebagai penanda selubung inti;
  citra dianalisis di Fiji (titik kapsid HIV di dalam/luar batas inti dikurasi manual) → data kemungkinan besar **citra mikroskopi**, bukan IFC.
- Kecocokan: sel T CD4 primer + HIV + Lamin B1 + citra optik (cocok dengan bidang sistem optika, CNN, Grad-CAM).
  Belum pasti: isi file, ukuran, label sel (terinfeksi/tidak), ada tidaknya kontrol tak terinfeksi, sel mati/lisis.
- **Dari halaman heiDATA (screenshot pengguna, 2026-11-03):** lisensi **CC BY 4.0**; **40 file**; dikelompokkan per figure paper
  (contoh tag "raw Fig 1/"); contoh file: `README.rtf` (2,8 KB), `Fig 1G +Vpx.tif` (46,5 MB), `Fig 1G -Vpx.tif` (46,5 MB),
  `Fig 1G +Vpx cropped.tif` / `Fig 1G -Vpx cropped.tif` (1,2 MB), `Fig 1G Mask.tif`. Deskripsi & publikasi terkait belum diisi pemilik.
  Thumbnail: citra mikroskopi fluoresens satu bidang pandang (titik-titik hijau).
- Implikasi: label tingkat kondisi **+Vpx / −Vpx** (kemungkinan permisif vs tidak permisif infeksi pada sel istirahat — perlu dicek
  di README/paper); jumlah bidang pandang per kondisi kemungkinan sedikit → sel tunggal harus disegmentasi dari citra besar,
  dan pembagian train/test harus per citra (bukan per sel) untuk menghindari kebocoran data.
- **Hasil pemeriksaan isi (2026-11-03)** — zip `dataverse_files.zip` (771 MB) di Drive `Project-Skripsi/data/raw/`;
  diekstrak lokal ke `data/raw/heidata-MUXYRY/`. Skrip: `notebooks/00_…metadata.py`, `notebooks/01_…hitung_inti.py`;
  keluaran: `results/eksplorasi-heidata/`.
  - Citra utama: **mikroskopi fluoresens 3D**, z-stack 31–36 irisan × 3–4 kanal × 512×512 px, 16-bit, **0,133 µm/px**
    (bidang pandang ≈ 68×68 µm). Fig S1 & S2A = *western blot* (tidak dipakai); Fig S2B = 2 kanal 8-bit, 0,36 µm/px.
  - Kanal (README): Fig 1G = SNAP-SiR, HIV-1 CA, **Lamin B1**; Fig 2A/2D = SNAP-SiR, CPSF6/SC35, HIV-1 GFP, Lamin B1;
    Fig 3B/4D = Lamin B1, HIV-1 GFP, EdU, HIV-1 CA. Virus: HIV-1 NLENG GFP p6mod. Lamin B1 ada di semua citra utama.
  - Bidang pandang yang dapat dipakai (masing-masing **1 citra**): +Vpx ×5 (1G, 2A, 2D, 3B, S3B+EFV), −Vpx ×7
    (1G, 2A, 2D, 3B, 4D DMSO, 4D SMI, S3B+EFV), Mock ×2 (1G, S3B). Catatan: README menyebut "Fig 4D DMSO +Vpx",
    tetapi file yang ada "4D DMSO -Vpx" dan "4D SMI -Vpx".
  - Hitung inti otomatis kasar (Lamin B1, proyeksi maksimum): **178 inti** dari 14 bidang (2–27 per bidang, diameter
    median 6–8 µm); inspeksi visual menunjukkan inti redup/di luar fokus terlewat → perkiraan nyata **±250–350 sel**.
  - Sinyal **HIV-1 GFP per inti hampir semua setara latar** (hanya ±1–2 inti lebih terang) → sel terinfeksi produktif sangat sedikit.
  - **Tidak ada penanda kematian/lisis.**
- **Kesimpulan kelayakan:** sangat cocok secara konsep (sel T CD4 primer, HIV, Lamin B1, citra optik, CC BY 4.0), tetapi
  **jumlah sel kecil** dan **1 citra per kondisi** → risiko model hanya mengenali citra/batch, bukan kondisi sel.
  Label yang realistis: **kondisi infeksi +Vpx / −Vpx / Mock** (bukan sehat/terinfeksi/lisis per sel).
  Pendekatan yang layak: ekstraksi fitur morfometri inti (Lamin B1) + fitur kapsid (CA) per sel → ML klasik dengan validasi
  *leave-one-field-out*; CNN kecil/transfer learning + Grad-CAM sebagai pembanding, dengan keterbatasan dinyatakan jujur.
  Peluang memperbesar data: minta citra tambahan ke pemilik dataset (tombol "Contact Owner" di heiDATA).

### 5. Dryad doi:10.7272/Q6SX6BFR — Subset sel T CD4 jaringan: kerentanan terhadap infeksi HIV & kematian
- Luo X. (2023), Dryad; paper: Luo X. et al., *Frontiers in Immunology* (2022), DOI 10.3389/fimmu.2022.883420.
- Data: **mass cytometry (CyTOF) berformat FCS** + scRNA-seq (CSV) — **bukan citra**. Sel limfoid tonsil manusia (sel T CD4 primer), 6 donor.
- Label: kondisi kultur di nama file (`..._Infected1_...fcs` vs `..._Uninfected_...fcs`); sudah di-*gating* sel hidup (live singlets);
  penanda per kanal ada di dalam file FCS (belum dicek). Ukuran total 1,33 GB; unduhan langsung.
- Kecocokan: HIV + CD4 + ML tabular + XAI (mis. SHAP), tetapi **tidak ada citra** → Grad-CAM & aspek "sistem optika"/IFC hilang.

### 6. FlowRepository FR-FCM-ZZSZ — CD4+ CyTOF-2 HIV (dari screenshot pengguna, 2026-11-03)
- Experiment name: "CD4+ CyTOF-2 HIV"; primary researcher/PI: Aurélien Corneau; experiment dates 2015-12-17 – 2016-02-04;
  diunggah Jun 2016, diperbarui Aug 2016. MIFlowCyt score 18,00%. Manuscripts: tidak dicantumkan. Keywords/organisasi: None.
- Purpose: "Comprehensive mass cytometry analysis of activation, cell cycle and immune check points expression in peripheral
  blood CD4 T cells in healthy and HIV-infected individuals".
- Data: **semua file FCS (mass cytometry)** — bukan citra. Label tingkat **donor**: sehat vs terinfeksi HIV (bukan per sel).
- Catatan: situs menampilkan pemberitahuan masalah kapasitas yang memengaruhi unggah & unduh; sertifikat SSL kedaluwarsa.
- Kecocokan: HIV + sel T CD4 + ML tabular (+ SHAP); tanpa citra → tanpa Grad-CAM/aspek optika. Tidak ada paper terkait untuk disitasi.

### 7. ACTG388 (UTHealth) — tidak cocok
- Data **klinis longitudinal jumlah CD4** pasien HIV (tabel teks), bukan data sel tunggal/citra.

## Peta ringkas (per 2026-11-03)
| Data | Citra? | HIV? | Sel CD4 primer? | Status |
|---|---|---|---|---|
| 4. heiDATA Ananth 2024 | ✅ mikroskopi fluoresens 3D | ✅ (±Vpx, mock) | ✅ istirahat | Diperiksa: cocok konsep, **data kecil (±250–350 sel, 14 citra)** |
| 5. Dryad Luo 2023 | ❌ CyTOF + scRNA | ✅ infected/uninfected | ✅ tonsil | Cadangan non-citra |
| 6. FlowRepository Corneau | ❌ CyTOF | ✅ donor sehat/HIV | ✅ darah tepi | Cadangan non-citra (tanpa paper) |
| 1. Dryad Essig 2022 | ✅ IFC | ❌ (aktivasi) | ✅ memori | Cadangan citra IFC |
| 2. BBBC048 | ✅ IFC | ❌ (siklus sel) | ❌ Jurkat | Prototipe pipeline |

## Skema kombinasi dataset (dicatat 2026-11-03)
Dataset **tidak bisa digabung menjadi satu set latih**: modalitas berbeda (citra mikroskopi 3D vs citra IFC vs tabel CyTOF)
dan label berbeda → model akan mengenali *asal dataset*, bukan kondisi sel. Kombinasi yang masuk akal = peran berbeda:

| Skema | Isi | Kelebihan | Risiko |
|---|---|---|---|
| **1. Pretraining + fine-tuning** | CNN dilatih awal pada citra sel T CD4 IFC **Essig (Dryad 2022)**, di-*fine-tune* pada **heiDATA** | Mengatasi data heiDATA yang kecil; ada eksperimen ablasi (dengan vs tanpa pretraining) | Beda domain (IFC vs konfokal; Essig tanpa Lamin B1); unduhan ±20 GB/eksperimen |
| **2. Dua analisis, satu benang merah** | A: citra **heiDATA** (morfometri Lamin B1 + kapsid HIV, ±Vpx, Grad-CAM); B: CyTOF **Luo (Dryad 2023)** (CD4 terinfeksi vs tidak, ML + SHAP) | Mencakup konsep proposal lebih lengkap (citra/Lamin B1 + terinfeksi vs sehat) | Beban ±2×; Luo sudah di-*gating* sel hidup (tanpa kelas lisis); CyTOF bukan optika |
| **3. Gabungan 1 + 2** | Pretraining Essig → heiDATA + CyTOF Luo | Paling lengkap | Estimasi ±8–10 minggu kerja vs ±6 minggu tersedia (s.d. Desember); risiko bertumpuk; kedalaman CPMK 3 bisa turun |

- Rekomendasi awal: heiDATA utama + Skema 1; Luo sebagai pustaka terkait/perluasan. Bergantung pada tanggal ujian.
- **Keputusan pengguna (2026-11-03): jalankan Skema 3 sebagai *pilot* sebelum bimbingan minggu ini**, lalu putuskan
  skema final bersama Pak Nopriadi berdasarkan hasil pilot. Hasil pilot = studi kelayakan, bukan hasil akhir skripsi.

## Opsi penyesuaian topik (diputuskan bersama Pak Nopriadi)
| Opsi | Data | Pertanyaan riset yang mungkin | Dampak ke judul |
|---|---|---|---|
| A | Dryad (CD4 memori) | Klasifikasi kondisi aktivasi sel T CD4 dari citra IFC multi-kanal + validasi Grad-CAM | "infeksi HIV" diganti/diturunkan menjadi konteks motivasi |
| B | BBBC048 (Jurkat) | Klasifikasi kondisi/fase sel limfosit T dari citra IFC + Grad-CAM | idem; data kecil, eksperimen cepat |
| C | Data lab sendiri | Sesuai proposal asli | Tidak realistis untuk tenggat Desember |

Sumber penelusuran: https://bbbc.broadinstitute.org/BBBC048 · https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrk7 ·
https://www.ebi.ac.uk/biostudies/BioImages/studies/S-BIAD452 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11858172/
