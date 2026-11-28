# WORK ORDER — Tracker Pengerjaan Skripsi
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**
Judul (Simaster, ditetapkan bimbingan 4): *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry
Menggunakan Machine Learning*
Terakhir diperbarui: **2026-11-26**

> Dokumen ini ditunjukkan saat bimbingan: (1) arahan dari setiap bimbingan, (2) status eksekusinya, (3) bukti/keluaran.
> Diperbarui setiap selesai bimbingan (tambah WO baru) dan setiap ada progres (ubah status & bukti).
> Dashboard ini merangkum semua WO; **detail tiap penugasan** ada di `docs/work-order/WO-xx.md` (1 dokumen per penugasan).
> Versi Google Docs (dashboard "00 Daftar Work Order" + dokumen WO-xx di folder Drive `bimbingan/Work Order/`): lihat `docs/DRIVE-DOCS.md`.
> Bahan & hasil tiap bimbingan: `docs/bimbingan/B<n>_<tanggal>/BAHAN.md` dan `HASIL.md`.
> Status: ✅ selesai · 🔄 berjalan · ⏳ belum dimulai · ❓ perlu konfirmasi mahasiswa · ⛔ terhambat · ➖ digantikan

## Ringkasan posisi
| Indikator | Nilai |
|---|---|
| Minggu semester (asumsi mulai 1 Sep 2026) | **Minggu ke-11 dari 16** (panduan: minggu 7–10 = pengambilan data tahap akhir) |
| Bimbingan formal tercatat | **7** (2 Sep, 4 Sep, 9 Sep, 23 Sep, 6 Nov, 9 Nov, 26 Nov) · target rubrik CPMK 2 "Sangat Baik": **> 8** |
| Jeda sejak bimbingan terakhir | B7 26 Nov 2026; bimbingan berikutnya: **[ISI NANTI]** |
| Ujian (RESMI) | Draf PDF **9 Des** · hardcopy **11 Des** · ujian **21–23 Des 2026** · syarat **≥ 12 catatan SIMASTER dinilai pembimbing** → `docs/JADWAL-UJIAN-2026.md` |
| Status WO | ✅ 4 · 🔄 13 · ⏳ 0 · ➖ 1 (total 18) |

## Daftar Work Order

| ID | Dari | Arahan / tugas | Status | Eksekusi & bukti | Catatan |
|---|---|---|---|---|---|
| WO-01 | B1 · 2 Sep | Cari dataset | ✅ | heiDATA ditemukan & dibawa ke B2 (4 Sep). Penelusuran ulang 3 Nov: 7 dataset dinilai → `docs/DATASET-KANDIDAT.md` | Dilanjutkan oleh WO-09 |
| WO-02 | B1 · 2 Sep | Susun gambaran Bab 1 | 🔄 | Draf gambaran (alur latar belakang, perumusan masalah, tujuan, manfaat) dibuat → `docs/materi/WO-02-gambaran-bab1.md` | Penyesuaian ke citra fluoresensi & sistem visual |
| WO-03 | B2 · 4 Sep | Rumuskan perbedaan skripsi dengan Teknik Biomedis & Teknologi Informasi | 🔄 | Draf 1 halaman (jawaban singkat + tabel perbandingan) dibuat → `docs/materi/WO-03-posisi-teknik-fisika.md` | Ditekankan kembali di B5: wajib kuasai aspek fisis/matematis fitur |
| WO-04 | B2 · 4 Sep | Pelajari metode deep learning | ➖ | Digantikan keputusan B4 (deep learning → machine learning) | Materi ML dipelajari lewat WO-08 |
| WO-05 | B2 · 4 Sep | Pelajari struktur sel, sel T CD4, biologi HIV | 🔄 | Materi ringkas dibuat → `docs/materi/WO-05-biologi-sel-cd4-hiv.md` | Mahasiswa mempelajari; relevan dengan interpretasi biologis/fisis |
| WO-06 | B3 · 9 Sep | Ganti judul sesuai saran pembimbing | ✅ | Judul baru dibawa ke B4; ditetapkan & disetujui di Simaster | Akan disesuaikan kembali pasca-B5 |
| WO-07 | B3 · 9 Sep | **Ekstraksi fitur**: karakteristik fisik/bio-optik pembeda sel **normal, terinfeksi, mati** | 🔄 | Pilot heiDATA: segmentasi inti Lamin B1 (209 sel) + fitur morfometri inti, intensitas & rasio tepi/inti Lamin B1, jumlah kapsid HIV di dalam/sekitar inti | B5: fokus murni citra visual; wajib dokumentasikan arti fisis & rumus matematis |
| WO-08 | B4 · 23 Sep | Cari **metode** machine learning yang tepat | 🔄 | Pilot: Logistic Regression & Random Forest (heiDATA); validasi *leave-one-figure-out* + uji permutasi | B5: wajib terapkan K-Fold Cross-Validation (5-fold / 10-fold) |
| WO-09 | B4 · 23 Sep | **Fiksasi dataset** | 🔄 | B5 (6 Nov): opsi E (tiga dataset) diajukan; pembimbing **membatasi data pada citra**, data non-citra (CyTOF) ditinggalkan → data utama heiDATA; judul boleh diganti | Masih terbuka: status Essig, kelas terinfeksi vs tidak, rumusan judul baru |
| WO-10 | B4 · 23 Sep | Tentukan **fitur yang diekstrak** | 🔄 | 11 fitur morfometri/intensitas + 2 fitur kapsid di `src/data/heidata_cells.py` | B5: wajib rumuskan definisi fisis & rumus matematisnya |
| WO-11 | Inisiatif | Sistem kerja skripsi (repo GitHub, Google Drive, naskah Google Docs + LaTeX template kampus, backup) | ✅ | `README.md`, `MASTER-SKRIPSI-SETUP.md`, `thesis/` (PDF 21 hlm ter-*compile*) | — |
| WO-12 | Inisiatif | Permintaan citra tambahan ke pemilik dataset heiDATA (Heidelberg) | 🔄 | Email sudah dikirim mahasiswa (dicatat 7 Nov); draf: `docs/korespondensi/permintaan-data-heidata.md` | Balasan tidak diharapkan → rencana tidak bergantung pada data tambahan |
| WO-13 | Inisiatif | Ringkasan Panduan Skripsi TF 2026 | ✅ | `docs/PANDUAN-KAMPUS.md` | — |
| WO-14 | B5 · 6 Nov | **Validasi k-fold + arti fisis & rumus matematis fitur citra** | 🔄 | Tabel 13 fitur → `docs/materi/WO-14-fitur-heidata.md`; k-fold → `results/wo14-kfold/`: per sel AUC 0,65–0,80, per percobaan 0,27–0,58. Dipresentasikan di B6 | B6: pembimbing menganggap evaluasi baku = per sel; isu kebocoran *batch* perlu diluruskan di B7 |
| WO-15 | B6 · 9 Nov | **Pilih metrik evaluasi + alasannya** (konteks uji kesehatan: FP vs FN) | 🔄 | 11 metrik + CM → `results/wo15-metrics/`; materi & usulan → `docs/materi/WO-15-metrik-evaluasi.md` | B7: mahasiswa harus bisa menjelaskan latih/validasi/uji dan metrik paling cocok "di luar kepala" |
| WO-16 | B7 · 26 Nov | **Kuasai latar belakang** sebagai cerita utuh: cara identifikasi sel terinfeksi selama ini, prosedur (pewarnaan, alat, citra/grafik & arti sumbu), masalahnya | 🔄 | Cerita 5 babak + jawaban 30 detik → `docs/work-order/WO-16.md`; bukti kurasi manual & "arbitrary threshold" dari PDF Ananth 2024 yang sudah dibaca | Mahasiswa perlu menghafal; 5 pustaka pendukung belum dibaca |
| WO-17 | B7 · 26 Nov | **Tinjauan metode terdahulu** + kekurangannya → posisi penelitian; banding pada dataset yang sama bila klaim lebih baik | 🔄 | 8 paper akses terbuka dibaca; tabel 3 kelompok + paragraf posisi penelitian + sikap atas klaim "lebih baik" → `docs/work-order/WO-17.md` | Celah ditopang Elfimov 2025 (IFC-HIV masih berbasis aturan) & Hennig 2017 ("highly manual and subjective"); mahasiswa wajib baca sendiri 3 paper penopang |
| WO-18 | B7 · 26 Nov | **Kelas 4 kondisi** (tidak terinfeksi, aktif, laten, ditekan obat): definisi + sumber data, model multikelas | 🔄 | Definisi 7 kelas dalam 3 model bertingkat (Gambar III.2) + sumber & jumlah sel → `docs/work-order/WO-18.md`; EFV di heiDATA S3B diperiksa lewat paper Ananth 2024 → kontrol negatif praperlakuan, bukan kelas "ditekan obat" | Illinois tidak punya kelas tidak terinfeksi (hanya heiDATA Mock) → risiko model mengenali dataset; konfirmasi di B8 |

## Hasil Bimbingan 7 (26 Nov 2026) — rincian: `docs/bimbingan/B7_2026-11-26/HASIL.md`
1. **Kelas:** 4 kondisi — tidak terinfeksi, terinfeksi (aktif), laten, ditekan obat → model 4 kelas; data dinilai cukup [ucapan akhir perlu konfirmasi] → WO-18.
2. **Latar belakang** harus dikuasai sebagai cerita (praktik saat ini → prosedur → masalah) → WO-16.
3. **Penelitian terdahulu** + kekurangannya = pintu masuk penelitian; klaim lebih baik harus dibandingkan pada dataset sama → WO-17.
4. Latih / validasi / uji dan metrik harus dijawab "di luar kepala" (lanjutan WO-15). Target ujian **Desember** [tanggal perlu konfirmasi].
5. Tidak dibahas: per sel vs berkelompok, hasil skenario, judul, format naskah. Rekaman tidak boleh disebarkan.

## Hasil Bimbingan 6 (9 Nov 2026) — rincian: `docs/bimbingan/B6_2026-11-09/HASIL.md`
1. Hanya hasil k-fold heiDATA yang dibahas. Pembimbing: klasifikasi dilakukan per sel, **evaluasi baku per sel**.
2. Alur: data dibagi training / validation (k-fold 5, untuk memutuskan parameter sudah cukup) / testing.
3. **Metrik:** jangan hanya akurasi; pilih metrik (F1, recall, dll.) dan jelaskan alasannya berdasarkan biaya FP vs FN → WO-15.
4. Perbandingan dengan penelitian lain belum ada; "yang penting bisa menjelaskan hasilmu".
5. Surat ganti judul: **belakangan saja**. Catatan bimbingan wajib ditulis di SIMASTER setiap bertemu.
6. Belum terbahas: dataset (Essig/Illinois), kelas, opsi judul, koreksi 0,65 → 0,57, ujian, pembimbing pendamping, judul Bab 3.

## Hasil Bimbingan 5 (6 Nov 2026) — rincian: `docs/bimbingan/B5_2026-11-04/HASIL.md`
1. **Data citra saja:** data non-citra (CyTOF) ditinggalkan → opsi E tidak dipakai; data utama heiDATA. Status Essig belum diputuskan.
2. **Arah kelas:** terinfeksi vs tidak terinfeksi.
3. **Identitas Teknik Fisika:** kuasai arti fisis dan rumus matematis tiap fitur (*circularity*, *solidity*, dst.).
4. **Validasi:** training / validation / testing dengan k-fold cross-validation (5 atau 10 fold).
5. **Judul:** boleh diganti; prosedur (dicek 7 Nov): surat persetujuan dosen pembimbing — surat sudah diselesaikan mahasiswa.
6. Belum terbahas: izin email Heidelberg, periode ujian, pembimbing pendamping & NIP, judul Bab 3.

## Keputusan mahasiswa (26 Nov 2026) — dijalankan sekarang, **dilaporkan** ke pembimbing di B8 (belum dikonfirmasi pembimbing)
| # | Keputusan | Dasar |
|---|---|---|
| 1 | **Satu alur metode, tiga sub-tugas; dataset tidak digabung**: heiDATA terpapar HIV-1 vs Mock · Illinois aktif (TNF) / laten / ditekan (Alp), 3 kelas · Essig hidup vs mati. Empat kondisi arahan B7 tercakup | `results/b8/README.md`: asal dataset tertebak 0,99–1,00; label diacak masih bAcc 0,44–0,45 vs peluang 0,20–0,25 |
| 2 | **Validasi**: unit klasifikasi = sel; data uji = percobaan/donor/plate yang tidak dipakai melatih; k-fold dalam data latih = validasi (pemilihan parameter); k-fold per sel dilaporkan sebagai pembanding | Kebocoran *batch* heiDATA Lamin B1 (0,79 → 0,27–0,46) |
| 3 | **Metrik**: utama sensitivitas & spesifisitas (per kelas untuk multikelas); pendukung *balanced accuracy*, MCC, ROC AUC; F1/akurasi tidak dipakai sebagai metrik utama | WO-15 (Lamin B1: F1 0,72–0,77 padahal spesifisitas 0) |
| 4 | **Judul naskah**: "Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Mikroskopi Optik Menggunakan Machine Learning" (Opsi 3). Judul resmi SIMASTER tetap lama sampai surat persetujuan ganti judul ditandatangani pembimbing | heiDATA & Illinois = mikroskopi, Essig = IFC |
| 5 | **Format naskah**: ikuti template `skripsidtntf.cls` (spasi 1,5; Bab III "Pelaksanaan Penelitian") | Template resmi DTNTF |

Masih perlu pembimbing (formal): tanda tangan surat ganti judul; tanggal ujian & tenggat pendaftaran.

### Daftar lama (dari B6)
Usulan mahasiswa: heiDATA (paparan HIV) + Essig (hidup vs mati); tiga opsi judul (Bahan B6 §3).
1. Pakai Essig sebagai pelengkap (sel mati; Essig tanpa infeksi HIV) atau heiDATA saja (atau Illinois)?
2. Kelas heiDATA untuk "terinfeksi vs tidak": usulan HIV vs Mock dari kapsid (AUC 0,91 lintas percobaan).
3. Luruskan per sel vs berkelompok: unit klasifikasi tetap sel, tetapi fold dipisah per percobaan (kebocoran *batch*).
4. Rumusan judul baru (surat persetujuan: pembimbing minta belakangan).
5. Laporkan bahwa email ke Heidelberg (WO-12) sudah dikirim; koreksi AUC B5 0,65 → 0,57.
6. Target periode ujian & tenggat; pembimbing pendamping & NIP; judul Bab 3.

## Arsip: eksekusi B4 → B5 (23 Sep → 3 Nov, disampaikan di B5)
1. **Dataset (WO-09):** penelusuran repositori publik (BBBC, BioStudies, Dryad, FlowRepository, heiDATA) → tidak ada citra IFC sel CD4
   terinfeksi HIV; 3 kandidat diperiksa langsung dan diuji coba (pilot).
2. **Ekstraksi fitur (WO-07, WO-10):** 209 sel heiDATA disegmentasi otomatis; 13 fitur fisik/bio-optik per sel diekstrak.
3. **Metode ML (WO-08):** klasifikasi +Vpx vs −Vpx dengan fitur Lamin B1 + kapsid HIV → AUC 0,65 (p = 0,01, signifikan tetapi sedang);
   fitur paling berpengaruh: panjang sumbu mayor inti & kapsid di sekitar inti.
   **Koreksi 7 Nov:** deteksi kapsid salah normalisasi (Mock terhitung ribuan titik palsu); setelah diperbaiki AUC 0,57, p = 0,14 (tidak
   signifikan) → `results/b6/README.md`. Data CyTOF: prediksi sel HIV+ pada donor baru AUC 0,85–0,91.
4. **Temuan keterbatasan:** heiDATA hanya 14 bidang pandang (1 per kondisi) → efek *batch* kuat; tidak ada kelas sel mati.
5. **Tugas bimbingan 1–2 yang tertunda (WO-02, WO-03, WO-05):** baru dikerjakan menjelang B5 — draf gambaran Bab 1, posisi
   keilmuan Teknik Fisika vs Teknik Biomedis/TI, dan materi biologi sel/CD4/HIV (`docs/materi/`).
6. **Administrasi:** sistem kerja, naskah template kampus, ringkasan panduan, draf email permintaan data.
Rincian angka: `docs/bimbingan/B5_2026-11-04/BAHAN.md`.
