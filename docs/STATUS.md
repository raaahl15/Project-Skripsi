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
1. **Putuskan dataset & penyesuaian topik bersama Pak Nopriadi** — tidak ada dataset IFC publik sel CD4 terinfeksi HIV;
   kandidat & opsi di docs/DATASET-KANDIDAT.md (A: Dryad CD4 memori, B: BBBC048 Jurkat)
2. **Jadwal mundur dari tanggal ujian**: tentukan periode ujian & tenggat pendaftaran → Gantt mingguan
3. Siapkan pipeline kode (loader IFC, baseline CNN, evaluasi, Grad-CAM) — bisa dimulai dengan BBBC048 (1,5 GB)

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
