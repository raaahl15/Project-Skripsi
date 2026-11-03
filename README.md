# Skripsi: Klasifikasi Kondisi Sel CD4 pada Infeksi HIV (Imaging Flow Cytometry + ML)

Repo kerja skripsi. Konteks lengkap dan aturan kerja agent: [AGENTS.md](AGENTS.md).
Posisi pekerjaan terkini: [docs/STATUS.md](docs/STATUS.md). Daftar revisi: [docs/REVISI.md](docs/REVISI.md).
Riwayat sesi: [docs/RIWAYAT-PENGERJAAN.md](docs/RIWAYAT-PENGERJAAN.md). **Tracker bimbingan: [docs/WORK-ORDER.md](docs/WORK-ORDER.md)**. Dasar sistem: [MASTER-SKRIPSI-SETUP.md](MASTER-SKRIPSI-SETUP.md).

**Naskah:** draf ditulis di **Google Docs** per bab ([folder naskah](https://drive.google.com/drive/folders/1B0gIkugJe1yVZWEBZaS62jG9fA5LRTU7)),
lalu dikonversi ke **LaTeX** (`thesis/`) per bab setelah disetujui dosen. Konvensi & cara konversi: [docs/PANDUAN-GDOCS.md](docs/PANDUAN-GDOCS.md).

- Pemilik: [raaahl15](https://github.com/raaahl15)
- Repo GitHub (private): [raaahl15/Project-Skripsi](https://github.com/raaahl15/Project-Skripsi)
- Google Drive: [Project-Skripsi](https://drive.google.com/drive/folders/1L5EdiZuWsGFqOQ64QzMGHmxBUs63yKJ6)

## Arsitektur

| Tempat | Isi |
|---|---|
| **GitHub (private)** | Sumber kebenaran: kode, naskah LaTeX, konteks agent, hasil kecil (metrik, gambar) |
| **Google Drive** `Project-Skripsi/` | Gudang: dataset, checkpoint model, PDF paper, backup `.bundle`, bootstrap kit |
| **Laptop** (Antigravity + Claude Code) | Kerja berat: koding, eksperimen, penulisan |
| **HP/iPad** (Claude app, claude.ai/code, github.dev) | Kerja ringan, revisi, bimbingan |
| **Colab/Kaggle** | Training GPU; metrik di-commit ke repo, checkpoint ke Drive |

> Repo git **tidak boleh** berada di folder yang disinkronkan Google Drive (risiko `.git` korup).

## Struktur folder

```
AGENTS.md / CLAUDE.md   konteks + aturan untuk agent AI
docs/                   STATUS, REVISI, catatan bimbingan, catatan literatur
thesis/                 naskah LaTeX (main.tex, bab1-5, refs.bib, template-kampus/)
src/                    kode Python (data, models, train.py, evaluate.py)
configs/                config eksperimen (YAML)
notebooks/              eksplorasi
results/                metrik & gambar kecil hasil eksperimen (di-commit)
data/                   dataset lokal (TIDAK di-commit; ambil dari Drive)
scripts/                setup, backup, build naskah
.github/workflows/      CI: compile LaTeX jadi PDF otomatis
```

## Alur kerja

| Situasi | Cara |
|---|---|
| Laptop utama | Antigravity + Claude Code, commit dan push rutin |
| Laptop lain / laptop teman | Clone repo, bootstrap kit dari Drive, rclone data. Lihat [docs/SETUP-LAPTOP-BARU.md](docs/SETUP-LAPTOP-BARU.md) |
| Hanya HP/iPad | Lihat bagian **Revisi dari HP/iPad** di bawah |
| Bimbingan | Naskah terbuka di iPad (Google Docs/PDF), tanya Claude via Project, catat ke `docs/bimbingan/` dan `docs/REVISI.md` |
| Menulis & revisi naskah | Google Docs per bab, bisa dari mana saja; dosen memberi komentar/saran langsung di Docs |
| Bab disetujui | Konversi ke LaTeX sesuai [PANDUAN-GDOCS.md](docs/PANDUAN-GDOCS.md) |
| Training berat | Colab/Kaggle, mount Drive, commit metrik ke `results/` |
| GitHub bermasalah | Clone dari `.bundle` di `Drive/Project-Skripsi/backup/` |

### Revisi dari HP/iPad (tanpa laptop)

0. **Google Docs (app/browser)**: untuk bab yang masih draf, revisi langsung di dokumen bab. Claude app dengan konektor Google Docs juga bisa membaca komentar dan mengeditnya.
1. **claude.ai/code (Claude Code di web)**: pilih repo ini, lalu beri perintah, mis. *"Kerjakan revisi #3 di docs/REVISI.md pada thesis/bab3-pelaksanaan-penelitian.tex"*. Ingat aturan AI kampus: Claude hanya boleh menyunting bahasa/format, bukan menulis substansi. Claude mengedit, commit, dan push dari cloud.
2. **github.dev**: buka repo di browser, tekan `.` untuk editor, lalu edit `.tex` dan commit. Cocok untuk perubahan kecil.
3. **Claude app (Project)**: diskusi dan menyusun kalimat; hasilnya dimasukkan lewat cara 1 atau 2.

Setelah push, **GitHub Actions** meng-compile LaTeX otomatis. PDF diunduh dari tab **Actions**, pilih run terbaru, lalu buka **Artifacts** dan unduh `skripsi-pdf`.

### Ritme

- **Awal sesi:** baca `docs/STATUS.md`.
- **Akhir sesi:** update `docs/STATUS.md` dan tambah entri di `docs/RIWAYAT-PENGERJAAN.md`, lalu commit dan push. Jika sistem berubah, update juga `MASTER-SKRIPSI-SETUP.md`.
- **H-1 bimbingan:** unduh PDF terbaru, lalu upload ke Claude Project.
- **Setelah bimbingan:** isi `docs/bimbingan/YYYY-MM-DD.md` dan pindahkan revisi ke `docs/REVISI.md`.
- **Mingguan:** jalankan backup (`scripts/backup.ps1` atau `scripts/backup.sh`).

## Perintah penting

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
powershell -ExecutionPolicy Bypass -File scripts\build-thesis.ps1
powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
```

```bash
# Linux/macOS/Git Bash/Colab
bash scripts/setup.sh
bash scripts/build-thesis.sh
bash scripts/backup.sh
```

## Keamanan

- Jangan login di komputer umum/teman tanpa logout tuntas; untuk komputer umum pakai `github.dev`/Codespaces lalu hapus sesi.
- Rahasia (API key, token) hanya di password manager atau `.env` lokal. `.env` sudah di-`.gitignore`; jangan pernah commit.
- Aktifkan 2FA di GitHub, Google, dan Claude.
- Cek aturan kampus (UGM/departemen) dan dosen pembimbing soal penggunaan AI dalam skripsi.
