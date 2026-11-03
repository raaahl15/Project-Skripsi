# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-03

## Posisi saat ini
- Tahap: proposal (disetujui di Simaster), menuju bimbingan awal & pengumpulan data

## Sudah selesai
- Proposal TA ke-1 disetujui di Simaster UGM (pembimbing: Nopriadi, S.T., M.Sc.)
- Repo skripsi + sistem kerja (Langkah 0) disiapkan
- Struktur Google Drive `Project-Skripsi/` + 5 Google Docs bab (kerangka) dibuat; draf naskah ditulis di Docs, final di LaTeX
- Folder `naskah/` dibagikan ke Pak Nopriadi (akses komentar)
- Repo di-push ke GitHub `raaahl15/Project-Skripsi` (private)
- Environment Python (.venv, Python 3.13, torch CPU) siap di laptop utama

## Sedang dikerjakan
- Menyiapkan bimbingan pertama

## Berikutnya (maks. 3)
1. Bimbingan pertama: tanyakan sumber dataset imaging flow cytometry, rumusan masalah, dan ekspektasi metode/metrik
2. Pastikan dataset tersedia (nama, format, jumlah sel per kelas), simpan di Drive `Project-Skripsi/data/raw/`
3. Masukkan template LaTeX kampus ke `thesis/template-kampus/`; upload backup `.bundle` ke Drive `backup/`

## Blocker / pertanyaan terbuka
- **Dataset belum ada** (blocker paling kritis; semua eksperimen bergantung padanya)
- Rumusan masalah, model, dan metrik belum ditentukan
- **Risiko waktu:** target selesai akhir semester (sekitar Desember 2026), tinggal sekitar 1–2 bulan. Tanggal pasti seminar/sidang: [ISI NANTI]
- Distribusi LaTeX belum terpasang di laptop utama (opsional; PDF bisa dibuat oleh GitHub Actions)
- Tidak ada GPU lokal (torch versi CPU) → training berat di Colab/Kaggle
