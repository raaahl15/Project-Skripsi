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
