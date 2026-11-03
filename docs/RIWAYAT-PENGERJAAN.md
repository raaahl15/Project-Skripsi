# Riwayat Pengerjaan

> Log setiap sesi pengerjaan (oleh pengguna maupun agent). **Wajib ditambah di akhir setiap sesi.**
> Entri terbaru di paling atas. Perubahan *sistem* juga dicatat di `MASTER-SKRIPSI-SETUP.md` bagian 10.
>
> Format entri:
> ```
> ## YYYY-MM-DD — judul singkat sesi
> **Oleh:** pengguna / Claude Code (laptop) / Claude Code (web) / Claude app
> **Dikerjakan:** ...
> **Keputusan:** ...
> **File/Drive berubah:** ...
> **Berikutnya:** ...
> ```

---

## 2026-11-04 — Opsi D & E untuk bimbingan 5
**Oleh:** Claude Code atas permintaan pengguna (pengguna berangkat kuliah; diminta langsung dikerjakan)

**Dikerjakan:**
- Bahan Bimbingan 5 §5b (repo + Google Doc, sisipan terverifikasi): **opsi D** — Essig diolah dengan ekstraksi fitur + ML
  (mask tersedia, fitur morfometri/intensitas/tekstur/spasial/kolokalisasi, RF/GB/SVM/LogReg, leave-one-donor-out, SHAP;
  judul D 14 kata) dan **opsi E** — satu pipeline ML untuk tiga studi (Essig, CyTOF, heiDATA) dengan benang merah
  aktivasi ↔ kerentanan HIV (hipotesis), konsekuensi & risiko.
- Pertanyaan keputusan no. 3 (Bahan & Hasil Bimbingan 5) diperbarui ke opsi A–E; log WO-09.

---

## 2026-11-04 — Run Colab pertama berhasil + uji reproduksibilitas
**Oleh:** pengguna (Colab) + Claude Code (perbandingan)

**Dikerjakan:**
- Pengguna membuat token GitHub baru (Contents: Read-only) dan menjalankan notebook Colab sampai selesai → hasil di Drive
  `results-colab/20261103-2339/`.
- Perbandingan dengan run laptop: fitur heiDATA & CyTOF identik; Logistic Regression identik (T1b AUC 0,651, p = 0,010);
  Random Forest sedikit berbeda (kesimpulan sama). Diarsipkan di `results/colab-runs/20261103-2339/` (+ README perbandingan).

**Tindak lanjut:** kunci versi pustaka & catat versi di keluaran sebelum run final; angka naskah dari satu lingkungan.

---

## 2026-11-04 — Notebook Google Colab
**Oleh:** Claude Code (laptop utama) atas permintaan pengguna

**Dikerjakan:**
- `notebooks/colab/pilot_skripsi_colab.ipynb` (20 sel, tervalidasi nbformat) + salinan di Drive `Project-Skripsi/colab/`:
  mount Drive → clone repo privat (token di Colab Secrets) → ekstrak data heiDATA & Luo → jalankan pipeline → simpan ke `results-colab/`.
  Bagian Essig opsional & nonaktif (`RUN_ESSIG_CNN = False`).
- `docs/PEMROSESAN-DATA.md` §7, `docs/DRIVE-DOCS.md`, MASTER diperbarui.

**Belum diuji di Colab** (perlu token GitHub dari pengguna). `exp1.zip` Essig belum ada di Drive.

**Essig di Drive (4 Nov):** unggahan browser dihentikan pengguna; `exp1.zip` diunggah via rclone (±28 menit, ±11 MiB/s) ke
`Project-Skripsi/data/raw/exp1.zip`; ukuran sama (19.581.330.572 B), MD5 `60289a8ada11216a7e11558577a857e6`.

**Insiden keamanan (4 Nov):** run pertama di Colab gagal di sel clone (exit 128) dan pesan error menampilkan token GitHub karena
token disisipkan di URL clone (kesalahan kode notebook). Pengguna diminta *revoke* token & membuat token baru (Contents: Read-only,
hanya repo Project-Skripsi). Notebook diperbaiki: token hanya dikirim sebagai header HTTP satu perintah, keluaran/galat disensor,
prompt interaktif dimatikan; diuji dengan token palsu (tidak bocor). Notebook di Drive ditimpa (ID tetap, tanpa output).

---

## 2026-11-04 — Dokumentasi pemrosesan data & fitur
**Oleh:** Claude Code (laptop utama) atas permintaan pengguna

**Dikerjakan:**
- `docs/PEMROSESAN-DATA.md` (+ Google Doc "Dokumentasi Pemrosesan Data dan Fitur" di Drive `bimbingan/`): lokasi pemrosesan
  (laptop utama, i5-2500S 4 inti, RAM 7,9 GB, tanpa GPU; belum memakai Colab/Kaggle), lokasi data mentah/hasil, skrip, alur
  langkah & parameter per dataset, tabel 14 fitur heiDATA (kanal, rumus, satuan, makna fisis, tugas), 29 penanda CyTOF, status Essig.
- WO-07 & WO-10 (repo + Google Docs) dan Bahan Bimbingan 5 diberi rujukan ke dokumen tersebut.

---

## 2026-11-04 — Struktur dokumen bimbingan: Bahan & Hasil per bimbingan, 1 dokumen per Work Order
**Oleh:** Claude Code (laptop utama) atas permintaan pengguna

**Dikerjakan:**
- Repo: `docs/bimbingan/B1…B5_<tanggal>/` (BAHAN.md + HASIL.md); notulensi lama → HASIL.md B1–B4; Bahan B1–B4 disusun ulang
  dari laporan mahasiswa (hanya hal yang tercatat); Hasil B5 berupa template keputusan; `docs/work-order/WO-01…13.md` + template;
  template Bahan/Hasil/WO.
- Drive `bimbingan/`: 25 Google Docs baru (via rclone, konversi HTML) di folder `00 Template`, `B1…B5`, `Work Order`; 3 dokumen lama
  dipindah (link tetap): Bahan Bimbingan 5 & Materi → `B5 - 2026-11-04`, Work Order Skripsi → `Work Order/00 Daftar Work Order`.
- Peta ID dokumen: `docs/DRIVE-DOCS.md`; aturan 17 AGENTS.md diperbarui.

**Catatan:** folder uji `bimbingan/_uji` (dokumen "Uji Konversi") masih ada — dapat dihapus pengguna.

---

## 2026-11-03 — Google Docs bimbingan + draf tugas tertunda WO-02/03/05
**Oleh:** Claude Code (laptop utama) bersama pengguna

**Dikerjakan:**
- Google Docs di Drive `bimbingan/`: Work Order Skripsi, Bahan Bimbingan 5, Materi Persiapan Bimbingan 5.
- Pengguna: WO-02, WO-03, WO-05 belum dikerjakan → draf dibuat dengan bantuan AI di `docs/materi/` (gambaran Bab 1, posisi
  Teknik Fisika vs Teknik Biomedis/TI, materi biologi sel/CD4/HIV + optika). Status WO → 🔄; mahasiswa wajib mempelajari.
- Perbaikan hitungan status di Work Order (✅ 4 · 🔄 7 · ⏳ 1 · ➖ 1).

**Catatan:** materi biologi berisi pengetahuan umum yang masih perlu sitasi buku teks; hanya Ananth 2024 & Luo 2022 yang terverifikasi.

---

## 2026-11-03 — Pilot Skema 3, riwayat bimbingan 1–4, Work Order
**Oleh:** Claude Code (laptop utama) bersama pengguna

**Dikerjakan:**
- Pilot Skema 3: heiDATA (segmentasi klasik 209 sel, 13 fitur, LogReg/RF *leave-one-figure-out*, uji permutasi, SHAP; variasi
  normalisasi per percobaan memperburuk hasil); CyTOF Luo (gating sel T CD4, ambang HIV+, kelas sehat/HIV+/apoptosis, HistGB
  *leave-one-donor-out* AUC 0,85–0,91, SHAP); Essig exp1 (480.000 sel, 8 kanal, ch0 brightfield) → pilot CNN gagal karena RAM
  (diperbaiki, tidak dijalankan ulang). Cellpose dihentikan (terlalu lambat di CPU).
- Draf email permintaan data ke Heidelberg (kontak: O. T. Fackler, dari Europe PMC).
- Usulan judul pengganti + tabel kecocokan judul vs dataset.
- **Riwayat bimbingan 1–4 dicatat** (`docs/bimbingan/2026-09-02/04/09/23.md`) dan **Work Order** dibuat (`docs/WORK-ORDER.md`).
  Bahan bimbingan diganti nama menjadi `bahan-bimbingan-5.md`.

**Temuan penting:** bimbingan 3–4 menetapkan arah **ekstraksi fitur + machine learning (bukan deep learning)** → Skema 1 (CNN)
dan judul berbasis *transfer learning* tidak dipakai; aturan 17–18 ditambahkan di AGENTS.md.

---

## 2026-11-03 — Penilaian dataset temuan pengguna + pemeriksaan heiDATA
**Oleh:** Claude Code (laptop utama) bersama pengguna

**Dikerjakan:**
- Menilai 4 dataset temuan pengguna (detail di `docs/DATASET-KANDIDAT.md`): Dryad Luo 2023 (CyTOF HIV, tanpa citra),
  FlowRepository Corneau (CyTOF donor sehat/HIV, tanpa citra & paper), ACTG388 (data klinis, tidak cocok),
  heiDATA Ananth 2024 (citra mikroskopi HIV + Lamin B1 di sel T CD4 istirahat, CC BY 4.0).
- Pengguna mengunggah heiDATA (`dataverse_files.zip`, 771 MB) ke Drive; diunduh via rclone, diekstrak ke `data/raw/heidata-MUXYRY/`.
- Pemeriksaan metadata TIFF + README dan hitung inti otomatis kasar (skrip di `notebooks/`, keluaran di `results/eksplorasi-heidata/`):
  z-stack 3–4 kanal 0,133 µm/px; 14 bidang pandang (1 per kondisi per figure); 178 inti terdeteksi (perkiraan nyata ±250–350);
  sel GFP+ sangat sedikit; tidak ada penanda kematian.

**Kesimpulan:** heiDATA paling cocok secara konsep tetapi kecil → perlu keputusan desain/judul bersama pembimbing; opsi menambah data via pemilik dataset.

---

## 2026-11-03 — Data diri, aturan AI final, penelusuran dataset
**Oleh:** Claude Code (laptop utama) bersama pengguna

**Dikerjakan:**
- Pengguna: ikuti arahan Pak Nopriadi soal AI (boleh semua tahapan) → aturan 15 AGENTS.md disederhanakan.
- Nama & NIM diisi di `thesis/data_skripsi.tex` (Rahul Ghulam Hidayatulloh, 23/519760/TK/57266; tahun masuk 2023 dari NIM); build lokal OK.
- Dataset harus dicari sendiri → penelusuran web; hasil di `docs/DATASET-KANDIDAT.md`:
  tidak ada dataset IFC publik sel CD4 terinfeksi HIV; kandidat terdekat Dryad (sel T CD4 memori, kondisi aktivasi, 125 GB),
  BBBC048 (Jurkat, siklus sel, 1,5 GB), S-BIAD452 (tipe sel darah putih, terutama fitur).

**Keputusan tertunda:** pilihan dataset & penyesuaian judul/topik — dibahas dengan pembimbing.

---

## 2026-11-03 — Konfirmasi pembimbing: izin AI & pembimbing pendamping
**Oleh:** Claude Code (laptop utama) berdasarkan laporan pengguna

**Dikerjakan:**
- Pengguna melaporkan: Pak Nopriadi **mengizinkan penggunaan AI untuk semua tahapan** (lisan); pembimbing pendamping **dicatat dulu** (belum dipastikan).
- AGENTS.md aturan 15 diperbarui: AI boleh membantu semua tahap dengan batasan tetap (tanpa literatur/data/angka fiktif,
  draf AI ditandai & wajib ditinjau pengguna, keputusan ide/kontribusi oleh pengguna & pembimbing, bantuan substansial dicatat di riwayat).
- Catatan bimbingan dibuat: `docs/bimbingan/2026-11-03.md`.

**Catatan risiko:** izin lisan berbeda dari panduan tertulis §4.1 → disarankan dicatat di SIMASTER sebagai bukti.

---

## 2026-11-03 — Perbaikan kompilasi template LaTeX + build lokal
**Oleh:** Claude Code (laptop utama, Windows) bersama pengguna

**Dikerjakan:**
- CI (GitHub Actions) gagal 2× pada class resmi `skripsidtntf.cls`:
  1. `\uline` tak terdefinisi (halaman pengesahan) → `\usepackage[normalem]{ulem}` di `thesis/packages.tex`.
  2. `\@pembimbingpendamping` tak terdefinisi saat `\end{intisari}`; class juga memakai `\@nippembimbingpendamping`
     di `\halamantugas` tanpa definisi → setter + default ditambah di `packages.tex` (pola sama dengan pembimbing utama);
     `data_skripsi.tex`: `\pembimbingpendamping{-}`, `\nippembimbingpendamping{-}` (Simaster: hanya 1 pembimbing).
  Pengecekan seluruh class: tidak ada makro metadata lain yang dipakai tanpa definisi.
- CI diperbaiki: error LaTeX/BibTeX/makeindex tampil sebagai *annotation*, log diunggah saat gagal, `actions/checkout@v5`.
- MiKTeX 25.12 dipasang (winget, scope user, auto-install paket aktif) → kompilasi lokal **berhasil: 21 halaman,
  0 error, 0 undefined control sequence**; teks halaman intisari/abstract diverifikasi ("Pembimbing Pendamping : -").
- `scripts/build-thesis.ps1` ditulis ulang: tanpa latexmk/Perl (pdflatex → bibtex bila ada pustaka → makeindex → pdflatex ×2),
  diuji dari build bersih.

**Catatan:** 4 *overfull hbox* kecil di halaman muka bawaan template (tidak fatal). Peringatan babel `bahasa` deprecated berasal dari class resmi.
Tampilan visual PDF belum diperiksa (renderer PDF tidak tersedia); pengguna diminta membuka `thesis\build\main.pdf`.

---

## 2026-11-03 — Panduan kampus + template LaTeX resmi
**Oleh:** Claude Code (laptop utama, Windows) bersama pengguna

**Dikerjakan:**
- Pengguna memberikan *Panduan Pelaksanaan Skripsi TF UGM 2026* (PDF) dan mengunggah folder template LaTeX resmi ke Drive
  (`Project-Skripsi/template skripsi teknik fisika 2026`).
- Template diunduh via rclone ke `thesis/template-kampus/` (salinan asli). `thesis/` dibangun ulang dari template:
  `skripsidtntf.cls`, BibTeX `skripsi.bst`, halaman muka, data skripsi, lampiran, `latexmkrc` (nomencl).
  Bug di template asli (`\nipkajur{` tanpa kurung tutup) diperbaiki di versi kita.
- Struktur bab disesuaikan dengan template: Bab 1 (Latar Belakang, Perumusan Masalah, Tujuan, Manfaat),
  Bab 2 Tinjauan Pustaka, Bab 3 **Pelaksanaan Penelitian** (Alat & Bahan, Tata Laksana, Rencana Analisis Hasil),
  Bab 4 Hasil dan Pembahasan, Bab 5 **Kesimpulan dan Saran** — di LaTeX dan di 5 Google Docs (link tetap; judul dokumen diganti).
- Ringkasan panduan: `docs/PANDUAN-KAMPUS.md`. **Aturan AI §4.1** dimasukkan sebagai aturan mengikat di `AGENTS.md`.

**Keputusan:**
- Ikuti nama bab dari template LaTeX resmi; judul Bab 3 dikonfirmasi ke dosen (panduan menyebut "Metodologi Penelitian").
- Agent tidak menulis substansi naskah; hanya penyuntingan bahasa, terjemahan, format, kode/infrastruktur (kode menunggu konfirmasi dosen).
- Daftar pustaka dimatikan (`\adapustakafalse`) sampai ada sitasi pertama, karena BibTeX gagal pada bibliografi kosong.

**Belum terverifikasi:** kompilasi template di GitHub Actions (LaTeX tidak terpasang di laptop).

**Berikutnya:** lihat `docs/STATUS.md` (bimbingan pertama, dataset, isi data_skripsi.tex).

---

## 2026-11-03 — rclone + backup otomatis ke Drive
**Oleh:** Claude Code (laptop utama, Windows) bersama pengguna

**Dikerjakan:**
- Pengguna menjalankan GitHub Actions (build PDF) dan meng-upload bundle backup manual ke Drive.
- Memasang rclone v1.75.2 (winget) dan mengonfigurasi remote `gdrive` (login Google oleh pengguna; token tersimpan di `%APPDATA%\rclone\rclone.conf`, di luar repo).
- `scripts/backup.ps1` diuji: bundle terkirim otomatis ke `Project-Skripsi/backup/`.
- Bootstrap kit (`setup.sh`, `setup.ps1`, `requirements.txt`, `SETUP-LAPTOP-BARU.md`) disalin ke `Project-Skripsi/00-BOOTSTRAP/`.

**Catatan:** rclone memperingatkan bahwa client_id bawaan untuk Google Drive akan dihentikan selama 2026. Jika backup tiba-tiba gagal, buat client_id sendiri (https://rclone.org/drive/#making-your-own-client-id).

**Berikutnya:**
1. Bimbingan pertama (dataset, rumusan masalah, model, metrik, tanggal seminar/sidang).
2. Pengguna mencari template LaTeX kampus → masukkan ke `thesis/template-kampus/`.

---

## 2026-11-03 — GitHub, berbagi naskah ke dosen, environment Python
**Oleh:** Claude Code (laptop utama, Windows) bersama pengguna

**Dikerjakan:**
- Pengguna membuat repo private `raaahl15/Project-Skripsi`; repo lokal di-push ke sana.
- Pengguna mengganti nama folder Drive `Skripsi-ML` → `Project-Skripsi`; semua rujukan di repo (termasuk path rclone di skrip) diperbarui.
- Folder Drive `naskah/` dibagikan ke Pak Nopriadi (nopriadi@ugm.ac.id) dengan akses Commenter (lihat + komentar).
- Ternyata Python 3.13 sudah terpasang dan ada di PATH (sesi VS Code sebelumnya memakai PATH lama). `setup.ps1` berhasil: `.venv` + semua library (torch 2.15 CPU, torchvision, scikit-learn, scikit-image, opencv, jupyter, dll.).
- Uji cepat: semua import OK; `src/train.py` berjalan sampai `NotImplementedError` yang memang disengaja (data/model belum ada).
- Bundle backup diperbarui; upload ke Drive lewat konektor tidak praktis (file biner) → pengguna upload manual.

**Keputusan:**
- Pakai Python 3.13 yang sudah ada (tidak memasang 3.12).
- Folder lokal tetap bernama `skripsi-ml/` walau repo GitHub bernama `Project-Skripsi`.

**Berikutnya:**
1. Bimbingan pertama (dataset, rumusan masalah, model, metrik, tanggal seminar/sidang).
2. Masukkan template LaTeX kampus ke `thesis/template-kampus/`.
3. Upload `C:\Users\Qenuarally\skripsi-backup-2026-11-03.bundle` ke Drive `Project-Skripsi/backup/`; pertimbangkan memasang rclone.

---

## 2026-11-03 — Langkah 0: setup sistem skripsi + Google Drive
**Oleh:** Claude Code (laptop utama, Windows) bersama pengguna

**Dikerjakan:**
- Wawancara awal Langkah 0 (jawaban dicatat di `MASTER-SKRIPSI-SETUP.md`).
- Membuat repo `skripsi-ml/` (AGENTS, README, docs, thesis LaTeX, src, configs, scripts, CI) + `git init` + commit awal lokal.
- Menguji `scripts/backup.ps1` → bundle `C:\Users\Qenuarally\skripsi-backup-2026-11-03.bundle` valid (belum di-upload ke Drive).
- Membuat struktur Google Drive `Skripsi-ML/` (00-BOOTSTRAP, naskah, data/raw, data/processed, models, papers, backup, bimbingan).
- Membuat 5 Google Docs bab (kerangka subbab, isi `[ISI NANTI]`) di `Skripsi-ML/naskah/`.
- Menambah `docs/PANDUAN-GDOCS.md` dan file riwayat ini; memindahkan `MASTER-SKRIPSI-SETUP.md` ke dalam repo.

**Keputusan:**
- Repo di `D:\rahul\Project Skripsi\skripsi-ml\` (bukan folder sinkron Drive).
- Draf naskah di Google Docs per bab; LaTeX (template kampus) untuk versi final, konversi per bab setelah disetujui dosen.
- GitHub Actions compile PDF agar revisi dari iPad tetap menghasilkan PDF.

**Belum bisa diuji:** `setup.ps1` (Python belum terpasang), `build-thesis.ps1` (LaTeX belum terpasang), CI (repo belum di-push).

**Berikutnya:**
1. Bimbingan pertama: dataset, rumusan masalah, model, metrik, tanggal seminar/sidang.
2. Buat repo private GitHub `raaahl15/skripsi-ml` lalu push.
3. Pasang Python 3.12; masukkan template LaTeX kampus ke `thesis/template-kampus/`.
