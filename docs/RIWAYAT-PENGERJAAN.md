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
