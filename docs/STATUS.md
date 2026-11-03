# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-04

## Posisi saat ini
- Tahap: proposal (disetujui di Simaster), menuju bimbingan awal & pengumpulan data
- Minggu ke-10 dari ±16 minggu semester (asumsi mulai 1 Sep 2026; bimbingan 1 = 2 Sep)
- Bimbingan formal: 4 (2, 4, 9, 23 Sep); bimbingan 5 = 4 Nov 2026. Tracker: docs/WORK-ORDER.md (+ docs/work-order/WO-xx.md, docs/bimbingan/B<n>_*/)
- Arah dari pembimbing: ekstraksi fitur fisik/bio-optik (normal/terinfeksi/mati) + machine learning (bukan deep learning)

## Sudah selesai
- Proposal TA ke-1 disetujui di Simaster UGM (pembimbing: Nopriadi, S.T., M.Sc.)
- Repo skripsi + sistem kerja (Langkah 0) disiapkan; GitHub `raaahl15/Project-Skripsi` (private)
- Struktur Google Drive `Project-Skripsi/` + 5 Google Docs bab; folder `naskah/` dibagikan ke Pak Nopriadi (Commenter)
- Environment Python (.venv, Python 3.13, torch CPU); rclone + backup otomatis ke Drive
- Panduan Skripsi TF 2026 dirangkum (docs/PANDUAN-KAMPUS.md); template LaTeX resmi dipasang di `thesis/`;
  kerangka Google Docs & LaTeX disesuaikan dengan struktur bab template

## Sedang dikerjakan
- Persiapan bimbingan 5 (4 Nov 2026): Bahan Bimbingan 5, Work Order, Materi Persiapan (WO-02/03/05)

## Berikutnya (maks. 3)
1. **Putuskan dataset & desain bersama Pak Nopriadi** — kandidat utama heiDATA (Ananth 2024: citra mikroskopi HIV + Lamin B1,
   ±250–350 sel, label +Vpx/−Vpx/Mock); sekaligus minta citra tambahan ke pemilik dataset. Detail: docs/DATASET-KANDIDAT.md
2. **Jadwal mundur dari tanggal ujian**: tentukan periode ujian & tenggat pendaftaran → Gantt mingguan
3. Lanjutkan ekstraksi fitur + ML (WO-07/08/10) pada dataset yang diputuskan; isi Hasil Bimbingan 5 & WO baru

## Hasil konfirmasi pembimbing (2026-11-03)
- Penggunaan AI: diizinkan untuk semua tahapan (lisan) → aturan 15 AGENTS.md diperbarui (dengan batasan: tanpa literatur/data fiktif, draf AI wajib ditinjau pengguna)
- Pembimbing pendamping: belum dipastikan (dicatat; sementara `-`)
- Belum dibahas / masih terbuka: sumber dataset, rumusan masalah, model & metrik, judul Bab 3, periode ujian

## Blocker / pertanyaan terbuka
- **Dataset belum ada** (blocker paling kritis). Hasil penelusuran: tidak ada dataset publik yang cocok persis dengan kelas
  sehat/terinfeksi/lisis → perlu keputusan penyesuaian topik (mungkin lewat *fast-track approval*, panduan §1.3)
- NIP pembimbing & pembimbing pendamping: belum diisi/dipastikan
- Rumusan masalah, model, dan metrik belum ditentukan
- **Risiko waktu:** target ujian akhir semester (sekitar Desember 2026). Syarat daftar ujian: draf 100% + persetujuan
  pembimbing + catatan bimbingan SIMASTER lengkap + bukti lulus similarity check. Tenggat pendaftaran: [ISI NANTI]
- Kompilasi template LaTeX: **berhasil secara lokal** (MiKTeX, 21 halaman, 0 error); hasil CI setelah push perlu dicek di tab Actions
- Tidak ada GPU lokal (torch versi CPU) → training berat di Colab/Kaggle
