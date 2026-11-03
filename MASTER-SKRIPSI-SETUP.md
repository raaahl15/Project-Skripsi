# MASTER SETUP: Sistem Pengerjaan Skripsi ML

> File ini adalah **dasar sistem** proyek skripsi: spesifikasi awal (Langkah 0) + keputusan sistem yang berlaku saat ini.
> Lokasi: root repo `skripsi-ml/` (dipindah ke dalam repo pada 2026-11-03 agar ter-versi dan terbaca dari iPad/cloud).
> **Wajib diperbarui** oleh agent setiap kali ada perubahan sistem (struktur, alur kerja, alat, lokasi file). Catat perubahannya di bagian 10.
> Langkah 0 sudah dijalankan pada 2026-11-03. Riwayat pengerjaan per sesi ada di `docs/RIWAYAT-PENGERJAAN.md`.

---

## Data Proposal Resmi (Simaster UGM - Disetujui)

> **Sumber:** Portal Akademik Simaster UGM (`simaster.ugm.ac.id/akademik/mhs_proposal/`)  
> **Status:** **DISETUJUI** (Pengajuan Tugas Akhir Ke 1)  
> *Pesan Portal:* "Tahap selanjutnya silahkan saudara melakukan bimbingan dengan melakukan pengisian ke catatan bimbingan."

| Field / Parameter | Keterangan |
| :--- | :--- |
| **Topik** | Ekstraksi Fitur & Klasifikasi Citra Sel CD4+ |
| **Judul (ID)** | **KLASIFIKASI KONDISI SEL CD4 PADA INFEKSI HIV BERDASARKAN CITRA IMAGING FLOW CYTOMETRY MENGGUNAKAN MACHINE LEARNING** |
| **Judul (EN)** | **CLASSIFICATION OF CD4 T CELL CONDITIONS IN HIV INFECTION BASED ON IMAGING FLOW CYTOMETRY IMAGES USING MACHINE LEARNING** |
| **Bidang I** | Instrumentasi - Implementasi Kecerdasan Buatan |
| **Bidang II** | Multifisika - Implementasi Sistem Optika |
| **Dosen Pembimbing** | Nopriadi, S.T., M.Sc. |
| **Keywords** | Sel T CD4, Infeksi HIV, Imaging Flow Cytometry, Machine Learning, Analisis Bio-Optik, Morfometri Sel, Explainable AI |

### Deskripsi Penelitian:
> "Penelitian ini bertujuan untuk mengembangkan sistem otomasi klasifikasi status kondisi sel limfosit T CD4 pada infeksi HIV menggunakan pendekatan machine learning berbasis data citra imaging flow cytometry. Sel T CD4 memegang peranan krusial dalam sistem imun adaptif dan merupakan target utama replikasi virus HIV, di mana progresivitas infeksi memicu perubahan fisik, kerusakan integritas membran inti (Lamin B1), hingga kematian sel (apoptosis). Melalui integrasi bidang instrumentasi cerdas dan sistem optika, penelitian ini mengekstraksi fitur bio-optik multi-kanal serta parameter morfometri sel untuk mengidentifikasi kondisi sel sehat, terinfeksi, dan lisis. Model pembelajaran mesin dilatih untuk mengenali pola kompleks tersebut, dilengkapi dengan metode Explainable AI (XAI) seperti Grad-CAM guna memvalidasi korelasi fisis antara representasi fitur visual dengan keputusan prediksi model. Penelitian ini diharapkan dapat berkontribusi pada pengembangan instrumentasi diagnostik medis yang presisi, objektif, dan terotomasi."

### Hasil Wawancara Langkah 0 (2026-11-03)

| # | Pertanyaan | Jawaban |
|---|---|---|
| 1 | Judul | Lihat tabel di atas |
| 2 | Rumusan masalah | [ISI NANTI] |
| 3 | Jenis & lokasi data | Citra imaging flow cytometry (multi-kanal); dataset **belum ada** |
| 4 | Metode/model | Belum ditentukan (Grad-CAM di proposal → kemungkinan CNN) |
| 5 | Metrik | Belum ditentukan |
| 6 | Dosen & preferensi | Nopriadi, S.T., M.Sc.; preferensi belum diketahui |
| 7 | OS | Laptop utama Windows 10; belum ada laptop cadangan (sementara pinjam laptop teman) |
| 8 | Format naskah | **Draf di Google Docs** (per bab), dikonversi ke **LaTeX** setelah bab disetujui |
| 9 | Template kampus | Ada, format LaTeX (belum dimasukkan ke repo) |
| 10 | GitHub | Akun `raaahl15`; repo belum dibuat |
| 11 | GPU | Belum disiapkan → rencana Colab/Kaggle |
| 12 | Deadline | Akhir semester, sekitar Desember 2026 |

---

## 0. Cara Agent Bekerja (WAJIB DIBACA DULU)

1. **Jangan langsung membuat file.** Mulai dengan bagian 1 (wawancara singkat). Tanyakan semua pertanyaan sekaligus, tunggu jawaban pengguna.
2. Setelah jawaban lengkap, tampilkan **rencana** (daftar file dan folder yang akan dibuat), minta konfirmasi, baru eksekusi.
3. **Jangan mengarang** judul, dataset, dosen, atau referensi. Jika data belum ada, isi placeholder `[ISI NANTI]`.
4. **Jangan menyimpan rahasia** (API key, token, password) di file mana pun.
5. Jangan menjalankan `git push` atau membuat repo GitHub tanpa persetujuan eksplisit pengguna.
6. Bahasa komunikasi dengan pengguna: Indonesia. Bahasa kode dan komentar kode: Inggris.
7. Setelah selesai, buat ringkasan: file apa yang dibuat, apa yang masih harus dilakukan manual oleh pengguna.
8. **Setiap sesi pengerjaan:** tambahkan entri di `docs/RIWAYAT-PENGERJAAN.md` (tanggal, yang dikerjakan, keputusan, file/Drive yang berubah, langkah berikutnya).
9. **Setiap perubahan sistem:** perbarui file MASTER ini dan catat di bagian 10.

---

## 1. Wawancara Awal (tanyakan sekaligus)

1. Judul skripsi atau kandidat topik ML
2. Rumusan masalah (1-2 kalimat; boleh "belum tahu")
3. Jenis data (time series sensor, citra, teks, tabular) dan lokasinya saat ini
4. Metode atau model yang direncanakan (boleh "belum tahu")
5. Metrik evaluasi yang direncanakan
6. Nama dosen pembimbing dan preferensinya (jika ada)
7. OS laptop utama dan laptop cadangan (Windows / macOS / Linux)
8. Naskah ditulis dengan **Markdown (+Pandoc)** atau **LaTeX**
9. Template naskah kampus: ada atau tidak (jika ada, minta file/format-nya)
10. Username GitHub, dan apakah repo sudah dibuat
11. Kebutuhan GPU: ada atau tidak (untuk menentukan Colab/Kaggle)
12. Deadline penting (seminar proposal, sidang, dll.)

---

## 2. Prinsip Arsitektur

- **GitHub (private)** = sumber kebenaran: kode, naskah, konteks agent, hasil kecil.
- **Google Drive** = gudang: dataset, checkpoint model, PDF paper, backup, bootstrap kit.
- **Google Docs** (`Drive/Skripsi-ML/naskah/`) = **draf naskah** per bab, tempat revisi dan komentar dosen. Konvensi: `docs/PANDUAN-GDOCS.md`.
- **LaTeX** (`thesis/` di repo) = **naskah final**, hasil konversi bab yang sudah disetujui, memakai template kampus.
- **Repo git TIDAK boleh berada di folder Drive yang tersinkron** (risiko `.git` korup).
- **Antigravity + Claude Code** = kerja berat di laptop.
- **Claude app (HP/iPad)** = kerja ringan, bimbingan, delegasi ke Claude Code.
- **Colab/Kaggle** = training GPU; hasil di-commit ke repo, checkpoint ke Drive.

---

## 3. Struktur Repo yang Harus Dibuat

```
skripsi-ml/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── docs/
│   ├── STATUS.md
│   ├── REVISI.md
│   ├── PERTANYAAN-DOSEN.md
│   ├── bimbingan/
│   │   └── TEMPLATE.md
│   └── literatur/
│       └── TEMPLATE.md
├── thesis/
│   ├── bab1-pendahuluan.md
│   ├── bab2-tinjauan-pustaka.md
│   ├── bab3-metodologi.md
│   ├── bab4-hasil-pembahasan.md
│   ├── bab5-penutup.md
│   └── refs.bib
├── src/
│   ├── data/
│   ├── models/
│   ├── train.py
│   └── evaluate.py
├── configs/
│   └── baseline.yaml
├── notebooks/
├── results/
├── data/            # kosong, di-gitignore (isi .gitkeep saja)
└── scripts/
    ├── setup.sh
    ├── setup.ps1
    ├── backup.sh
    └── build-thesis.sh
```

Jika pengguna memilih LaTeX, ganti isi `thesis/` dengan `main.tex` + file bab `.tex` + `refs.bib`, dan ganti `build-thesis.sh` dengan perintah `latexmk`.

**Struktur aktual (setelah Langkah 0, LaTeX dipilih)** — tambahan terhadap struktur di atas:
- `MASTER-SKRIPSI-SETUP.md` (file ini), `.gitattributes`
- `docs/RIWAYAT-PENGERJAAN.md`, `docs/PANDUAN-GDOCS.md`, `docs/SETUP-LAPTOP-BARU.md`
- `thesis/main.tex`, `thesis/bab1-pendahuluan.tex` … `bab5-penutup.tex`, `thesis/refs.bib`, `thesis/figures/`, `thesis/template-kampus/`
- `scripts/backup.ps1`, `scripts/build-thesis.ps1` (padanan Windows)
- `.github/workflows/build-thesis.yml` (compile PDF otomatis saat push ke `thesis/`)

---

## 4. Template Isi File

### 4.1 `AGENTS.md`

```markdown
# Konteks Skripsi
- Judul: [dari wawancara]
- Masalah: [dari wawancara]
- Metode: [dari wawancara]
- Dataset: [nama, ukuran, lokasi di Drive]
- Metrik: [dari wawancara]
- Dosen pembimbing: [nama] | preferensi: [catatan]
- Deadline: [dari wawancara]

# Aturan Kerja (berlaku untuk semua agent)
1. Awal sesi: baca docs/STATUS.md dan docs/REVISI.md.
2. Akhir sesi: update docs/STATUS.md, lalu commit.
3. Naskah: Indonesia formal akademik. Kode dan komentar: Inggris.
4. Jangan ubah data mentah. Semua eksperimen reproducible (seed tetap, config di configs/).
5. Setiap eksperimen: config disimpan di configs/, hasil di results/.
6. Angka di naskah HARUS berasal dari file di results/. Jangan mengetik angka dari ingatan.
7. Jangan mengarang sitasi. Referensi hanya boleh yang ada di refs.bib dan sudah diverifikasi pengguna.
8. Jangan commit data besar, checkpoint, atau rahasia.
9. Jika tidak yakin, tanya pengguna; jangan berasumsi.
10. Pengguna harus bisa memahami dan membela semua isi: jelaskan alasan di balik setiap keputusan teknis penting.

# Struktur
Lihat README.md. Data besar dan model ada di Google Drive (lokasi dicatat di bagian Dataset).
```

### 4.2 `CLAUDE.md`

```markdown
Baca dan patuhi AGENTS.md di root repo ini sebelum melakukan apa pun.
```

### 4.3 `docs/STATUS.md`

```markdown
# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: YYYY-MM-DD

## Posisi saat ini
- Tahap: [proposal / data / baseline / eksperimen / penulisan / revisi]

## Sudah selesai
-

## Sedang dikerjakan
-

## Berikutnya (maks. 3)
1.

## Blocker / pertanyaan terbuka
-
```

### 4.4 `docs/REVISI.md`

```markdown
# DAFTAR REVISI
Status: todo | doing | done

| # | Tanggal | Dari | Revisi | Bagian | Status |
|---|---------|------|--------|--------|--------|
| 1 |         |      |        |        | todo   |
```

### 4.5 `docs/bimbingan/TEMPLATE.md`

```markdown
# Bimbingan YYYY-MM-DD
## Yang dibawa
-
## Pertanyaan dosen & jawaban
-
## Revisi (pindahkan ke REVISI.md)
-
## Arahan berikutnya & jadwal
-
```

### 4.6 `docs/literatur/TEMPLATE.md`

```markdown
# [Judul paper]
- Penulis / tahun / venue:
- DOI / URL:
- Masalah:
- Metode:
- Dataset & metrik:
- Hasil utama:
- Keterbatasan:
- Relevansi ke skripsiku:
- Status verifikasi: [ ] sudah dibuka & dibaca langsung oleh pengguna
```

### 4.7 `docs/PERTANYAAN-DOSEN.md`

Daftar pertanyaan yang mungkin diajukan (alasan pemilihan model, hyperparameter, split data, metrik, baseline, keterbatasan). Agent mengisi kerangka berdasarkan topik; pengguna melengkapi jawaban dengan pemahamannya sendiri.

### 4.8 `.gitignore` (minimal)

```
data/*
!data/.gitkeep
models/
*.pt
*.pth
*.ckpt
*.h5
.env
.venv/
__pycache__/
.ipynb_checkpoints/
*.bundle
.DS_Store
```

### 4.9 `scripts/setup.sh`

```bash
#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data results
echo "Selesai. Ambil data: rclone copy gdrive:Skripsi-ML/data ./data"
```

`scripts/setup.ps1` adalah padanannya untuk Windows PowerShell (`python -m venv .venv`, aktivasi, `pip install -r requirements.txt`).

### 4.10 `scripts/backup.sh`

```bash
#!/usr/bin/env bash
set -e
F=~/skripsi-backup-$(date +%F).bundle
git bundle create "$F" --all
rclone copy "$F" gdrive:Skripsi-ML/backup/
```

### 4.11 `scripts/build-thesis.sh` (Markdown + Pandoc)

```bash
#!/usr/bin/env bash
pandoc thesis/bab*.md -o skripsi.docx --citeproc --bibliography=thesis/refs.bib
```

---

## 5. Struktur Google Drive

Agent tidak mengakses Drive kecuali ada konektor aktif dan pengguna menyetujui.
**Status:** sudah dibuat oleh agent lewat konektor Google Drive pada 2026-11-03 (atas persetujuan pengguna).

```
Drive/Skripsi-ML/
├── 00-BOOTSTRAP/  (salinan setup.sh, setup.ps1, requirements.txt, SETUP-LAPTOP-BARU.md)
├── naskah/        (Google Docs: Bab 1 … Bab 5 — draf naskah)
├── data/raw/  data/processed/
├── models/
├── papers/
├── backup/
└── bimbingan/
```

Link folder & dokumen tercatat di `AGENTS.md` (bagian "Lokasi Google Drive").

Agent juga membuat file `docs/SETUP-LAPTOP-BARU.md` berisi langkah: install Git, Python, Node.js, Antigravity, Claude Code; login akun; `git clone`; `bash scripts/setup.sh`; `rclone copy` data dari Drive; buka di Antigravity atau jalankan `claude`.

---

## 6. Alur Kerja yang Harus Didokumentasikan di README.md

| Situasi | Cara |
|---|---|
| Laptop utama | Antigravity + Claude Code, commit dan push rutin |
| Laptop lain | Clone repo, bootstrap kit dari Drive, rclone data |
| Hanya HP/iPad | `github.dev` untuk edit, Claude app untuk tanya jawab dan delegasi |
| Bimbingan | Naskah terbuka di iPad, tanya Claude via Project, catat ke REVISI.md |
| Menulis & revisi naskah | Google Docs per bab (bisa dari HP/iPad; Claude bisa membaca/mengedit lewat konektor Google Docs) |
| Bab disetujui dosen | Konversi bab itu ke LaTeX (`thesis/`), lihat `docs/PANDUAN-GDOCS.md` |
| Training berat | Colab/Kaggle, mount Drive, commit metrik ke repo |
| GitHub bermasalah | Clone dari `.bundle` di Drive |

Ritme: awal sesi baca STATUS; akhir sesi update STATUS + commit + push; H-1 bimbingan update PDF di Project; setelah bimbingan isi catatan dan REVISI; mingguan jalankan backup.

---

## 7. Peringatan Keamanan

- Jangan login di komputer umum tanpa logout tuntas; untuk komputer umum pakai `github.dev`/Codespaces lalu hapus sesi.
- Rahasia hanya di password manager. Pastikan `.env` ada di `.gitignore`.
- Aktifkan 2FA di GitHub, Google, dan Claude.
- Cek aturan kampus dan dosen soal penggunaan AI dalam skripsi.

---

## 8. Langkah Setelah Agent Selesai (untuk Pengguna)

1. Review semua file yang dibuat; lengkapi placeholder `[ISI NANTI]`.
2. Buat repo private di GitHub, lalu `git remote add origin ...` dan push.
3. Buat struktur folder di Drive; salin bootstrap kit.
4. Aktifkan konektor Google Drive di aplikasi Claude.
5. Buat **Claude Project** untuk skripsi; upload `AGENTS.md`, `STATUS.md`, `REVISI.md`, dan PDF naskah terbaru.
6. Tes dari iPad: buka `github.dev`, edit satu file, commit.
7. Tes laptop lain: clone, jalankan `setup.sh`.

---

## 9. Kriteria Selesai (Definition of Done)

- [ ] Semua file di bagian 3 ada dan berisi template yang benar
- [ ] `AGENTS.md` terisi sesuai wawancara
- [ ] Skrip setup dan backup dapat dijalankan
- [ ] Tidak ada rahasia atau data besar di repo
- [ ] Agent memberi ringkasan + daftar tugas manual untuk pengguna

---

## 10. Log Perubahan Sistem

| Tanggal | Perubahan | Alasan |
|---|---|---|
| 2026-11-03 | Langkah 0 dijalankan: repo `skripsi-ml/` dibuat (LaTeX), commit awal lokal | Setup awal |
| 2026-11-03 | Ditambah GitHub Actions compile PDF, skrip `.ps1` untuk Windows, `.gitattributes` | Revisi dari iPad tetap menghasilkan PDF; laptop utama Windows |
| 2026-11-03 | Naskah: draf di **Google Docs** per bab, LaTeX untuk versi final (konversi per bab setelah disetujui) | Permintaan pengguna: revisi lebih mudah |
| 2026-11-03 | Struktur Drive `Skripsi-ML/` + folder `naskah/` + 5 Google Docs bab dibuat oleh agent | Permintaan pengguna |
| 2026-11-03 | Ditambah `docs/RIWAYAT-PENGERJAAN.md`; aturan wajib update riwayat & MASTER tiap sesi | Permintaan pengguna |
| 2026-11-03 | File MASTER dipindah dari `D:\rahul\Project Skripsi\` ke root repo | Agar ter-versi git dan bisa diperbarui dari iPad/cloud |
