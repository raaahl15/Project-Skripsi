# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-28

## Posisi saat ini
- Tahap: penulisan naskah (Bab I LaTeX ada; Bab II–V draf) + eksperimen B8, pasca-Bimbingan 7
- Minggu ke-13 dari ±16 minggu semester (asumsi mulai 1 Sep 2026)
- Bimbingan formal terlaksana: **7** (2, 4, 9, 23 Sep; 6, 9, 26 Nov). Bimbingan berikutnya: **B8 Senin 30 Nov 2026**
- **Jadwal resmi** (`docs/JADWAL-UJIAN-2026.md`): draf PDF **9 Des** · hardcopy **11 Des** · ujian **21–23 Des 2026**;
  syarat **≥ 12 catatan SIMASTER dinilai pembimbing**. SIMASTER tercatat: B1, B2, B5, B6, B7; B3 + B8 masuk 30 Nov; B4 belum
  → masih perlu 4 pertemuan baru (B9–B12) sebelum 9 Des.
- Arah B7: kelas **4 kondisi** (tidak terinfeksi, aktif, laten, ditekan obat); kuasai alur ujian: latar belakang → masalah →
  penelitian terdahulu & kekurangannya → metode → latih/validasi/uji → metrik.

## Sudah selesai
- B7 (26 Nov): `docs/bimbingan/B7_2026-11-26/HASIL.md` (+ isian SIMASTER §7); WO-16, WO-17, WO-18 dibuat
- Pipeline bertingkat sebagai kerangka Bab III → `thesis/figures/pipeline-bertingkat.png` (Gambar III.2)
- Eksperimen B8 gabung vs terpisah → `results/b8/`
- Bab I LaTeX (`thesis/bab1-pendahuluan.tex`, 25 sitasi, ter-*compile*); ceklis 25 referensi Bab I + 7 PDF OA
  di Drive `papers/pdf-bab1/` (28 Nov)
- Isian SIMASTER B2, B3, B4, B7 siap di masing-masing `HASIL.md`

- **Draf Bab II** (28 Nov) di Google Docs tab Bab II: II.1 tinjauan pustaka 4 subbab + Tabel II.1 (dari WO-17), II.2 dasar
  teori 7 subbab dengan Persamaan II.1–II.15 (±3.900 kata); ditandai draf berbantuan AI, wajib ditinjau mahasiswa

- **Draf Bab III** (28 Nov) di tab Bab III: III.1 alat (Colab/Drive/GitHub) & bahan + Tabel III.1 dataset; III.2.1–III.2.6
  (alur bertingkat, praproses, fitur, definisi kelas + Tabel III.2, model, validasi bersarang per kelompok); III.3 rencana analisis
  (±2.600 kata). Gambar III.1 belum dibuat; Gambar III.2 disisipkan manual.
- **Pipeline ML final untuk Colab siap** (28 Nov): `src/final/`, `configs/final/`, `notebooks/colab/final_ml_colab.ipynb`;
  rencana `docs/RENCANA-ML-COLAB.md`. Target ML final selesai Senin 30 Nov.

## Sedang dikerjakan
- **Run ML final di Colab** (pengguna menjalankan notebook; hasil otomatis ke GitHub `results/final/` + Drive). Essig exp3/exp4 perlu
  diunduh ke Drive `data/raw/`.
- **Mahasiswa meninjau draf Bab II** (catatan cek di paragraf atas tab: 3 pustaka belum dibaca, paragraf *brightfield* belum
  berpustaka, angka 1.806 senyawa & kutipan "arbitrary threshold of 35" dicocokkan ke paper)
- **Mahasiswa membaca & memverifikasi 25 referensi Bab I** (ceklis di `docs/literatur/DAFTAR-REFERENSI.md`); yang sudah dibaca
  dipindah dari `refs-kandidat.bib` ke `refs.bib`. Angka Kemenkes (564.000 / 63% / 67% / 55%) dicocokkan sendiri ke sumbernya.
- WO-16 (latar belakang), WO-17 (metode terdahulu), WO-18 (kelas) — mahasiswa menguasai isinya; 3 paper penopang wajib dibaca sendiri
- WO-14, WO-15 (fitur & metrik) — dikuasai "di luar kepala" untuk ujian

## Berikutnya (maks. 3)
1. B8 Senin 30 Nov: bawa keputusan pipeline bertingkat, hasil `results/b8/`, dan draf Bab II; masukkan B3 & B8 (lalu B4) ke SIMASTER
2. Draf Bab III, lalu Bab IV
3. Baca/verifikasi referensi Bab I

## Blocker / pertanyaan terbuka
- Kelas 4 kondisi lintas dataset (Illinois tak punya kelas tidak terinfeksi) → risiko model mengenali dataset; konfirmasi di B8
- Jumlah pertemuan SIMASTER: perlu 12 dinilai sebelum 9 Des (setelah 30 Nov + B4 = 8)
- NIP pembimbing & pembimbing pendamping; judul Bab 3
- Repo GitHub berstatus **publik** (keputusan 8 Nov) — PDF paper tetap di luar git (`.gitignore`)
