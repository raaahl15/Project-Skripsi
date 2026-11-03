# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-03

## Posisi saat ini
- Tahap: proposal (disetujui di Simaster), menuju bimbingan awal & pengumpulan data
- Minggu ke- [ISI NANTI] dari ±16 minggu semester (tanggal mulai semester: [ISI NANTI])

## Sudah selesai
- Proposal TA ke-1 disetujui di Simaster UGM (pembimbing: Nopriadi, S.T., M.Sc.)
- Repo skripsi + sistem kerja (Langkah 0) disiapkan; GitHub `raaahl15/Project-Skripsi` (private)
- Struktur Google Drive `Project-Skripsi/` + 5 Google Docs bab; folder `naskah/` dibagikan ke Pak Nopriadi (Commenter)
- Environment Python (.venv, Python 3.13, torch CPU); rclone + backup otomatis ke Drive
- Panduan Skripsi TF 2026 dirangkum (docs/PANDUAN-KAMPUS.md); template LaTeX resmi dipasang di `thesis/`;
  kerangka Google Docs & LaTeX disesuaikan dengan struktur bab template

## Sedang dikerjakan
- Menyiapkan bimbingan pertama

## Berikutnya (maks. 3)
1. **Bimbingan pertama** (catat di SIMASTER → Catatan bimbingan). Agenda: sumber dataset; rumusan masalah; model & metrik;
   judul Bab 3 ("Metodologi" vs "Pelaksanaan Penelitian"); batas penggunaan AI untuk kode program;
   target periode ujian (tengah/akhir semester) & tenggat pendaftaran; jadwal bimbingan rutin (min. 1×/2 minggu, target > 8×)
2. Pastikan dataset tersedia (nama, format, jumlah sel per kelas), simpan di Drive `Project-Skripsi/data/raw/`
3. Isi `thesis/data_skripsi.tex` (nama lengkap, NIM, NIP pembimbing) dan cek PDF hasil GitHub Actions

## Blocker / pertanyaan terbuka
- **Dataset belum ada** (blocker paling kritis; semua eksperimen bergantung padanya)
- Rumusan masalah, model, dan metrik belum ditentukan
- **Risiko waktu:** target ujian akhir semester (sekitar Desember 2026). Syarat daftar ujian: draf 100% + persetujuan
  pembimbing + catatan bimbingan SIMASTER lengkap + bukti lulus similarity check. Tenggat pendaftaran: [ISI NANTI]
- Kompilasi template LaTeX belum terverifikasi (menunggu hasil GitHub Actions)
- Tidak ada GPU lokal (torch versi CPU) → training berat di Colab/Kaggle
