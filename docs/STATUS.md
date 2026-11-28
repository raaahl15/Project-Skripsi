# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-28

## Posisi saat ini
- Tahap: penulisan naskah (Bab I LaTeX ada; Bab II–V draf) + eksperimen B8, pasca-Bimbingan 7
- Minggu ke-13 dari ±16 minggu semester (asumsi mulai 1 Sep 2026)
- Bimbingan formal terlaksana: **7** (2, 4, 9, 23 Sep; 6, 9, 26 Nov). Bimbingan berikutnya (B8): **[ISI NANTI]**
- **Jadwal resmi** (`docs/JADWAL-UJIAN-2026.md`): draf PDF **9 Des** · hardcopy **11 Des** · ujian **21–23 Des 2026**;
  syarat **≥ 12 catatan SIMASTER dinilai pembimbing** → masih perlu ±5 pertemuan baru (B8–B12) sebelum 9 Des.
- Arah B7: kelas **4 kondisi** (tidak terinfeksi, aktif, laten, ditekan obat); kuasai alur ujian: latar belakang → masalah →
  penelitian terdahulu & kekurangannya → metode → latih/validasi/uji → metrik.

## Sudah selesai
- B7 (26 Nov): `docs/bimbingan/B7_2026-11-26/HASIL.md` (+ isian SIMASTER §7); WO-16, WO-17, WO-18 dibuat
- Pipeline bertingkat sebagai kerangka Bab III → `thesis/figures/pipeline-bertingkat.png` (Gambar III.2)
- Eksperimen B8 gabung vs terpisah → `results/b8/`
- Bab I LaTeX (`thesis/bab1-pendahuluan.tex`, 25 sitasi, ter-*compile*); ceklis 25 referensi Bab I + 7 PDF OA
  di Drive `papers/pdf-bab1/` (28 Nov)
- Isian SIMASTER B2, B3, B4, B7 siap di masing-masing `HASIL.md`

## Sedang dikerjakan
- **Mahasiswa membaca & memverifikasi 25 referensi Bab I** (ceklis di `docs/literatur/DAFTAR-REFERENSI.md`); yang sudah dibaca
  dipindah dari `refs-kandidat.bib` ke `refs.bib`. Angka Kemenkes (564.000 / 63% / 67% / 55%) dicocokkan sendiri ke sumbernya.
- WO-16 (latar belakang), WO-17 (metode terdahulu), WO-18 (kelas) — mahasiswa menguasai isinya; 3 paper penopang wajib dibaca sendiri
- WO-14, WO-15 (fitur & metrik) — dikuasai "di luar kepala" untuk ujian

## Berikutnya (maks. 3)
1. Jadwalkan B8 dan bawa keputusan pipeline bertingkat + hasil `results/b8/`; masukkan isian B2/B3/B4/B7 ke SIMASTER
2. Draf Bab II (tabel WO-17 → II.1), lalu Bab III–IV
3. Baca/verifikasi referensi Bab I

## Blocker / pertanyaan terbuka
- Kelas 4 kondisi lintas dataset (Illinois tak punya kelas tidak terinfeksi) → risiko model mengenali dataset; konfirmasi di B8
- Jumlah pertemuan SIMASTER: perlu 12 dinilai sebelum 9 Des
- NIP pembimbing & pembimbing pendamping; judul Bab 3
- Repo GitHub berstatus **publik** (keputusan 8 Nov) — PDF paper tetap di luar git (`.gitignore`)
