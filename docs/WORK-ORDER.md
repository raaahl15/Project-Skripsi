# WORK ORDER — Tracker Pengerjaan Skripsi
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**
Judul (Simaster, ditetapkan bimbingan 4): *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry
Menggunakan Machine Learning*
Terakhir diperbarui: **2026-11-07**

> Dokumen ini ditunjukkan saat bimbingan: (1) arahan dari setiap bimbingan, (2) status eksekusinya, (3) bukti/keluaran.
> Diperbarui setiap selesai bimbingan (tambah WO baru) dan setiap ada progres (ubah status & bukti).
> Dashboard ini merangkum semua WO; **detail tiap penugasan** ada di `docs/work-order/WO-xx.md` (1 dokumen per penugasan).
> Versi Google Docs (dashboard "00 Daftar Work Order" + dokumen WO-xx di folder Drive `bimbingan/Work Order/`): lihat `docs/DRIVE-DOCS.md`.
> Bahan & hasil tiap bimbingan: `docs/bimbingan/B<n>_<tanggal>/BAHAN.md` dan `HASIL.md`.
> Status: ✅ selesai · 🔄 berjalan · ⏳ belum dimulai · ❓ perlu konfirmasi mahasiswa · ⛔ terhambat · ➖ digantikan

## Ringkasan posisi
| Indikator | Nilai |
|---|---|
| Minggu semester (asumsi mulai 1 Sep 2026) | **Minggu ke-10 dari 16** (panduan: minggu 7–10 = pengambilan data tahap akhir) |
| Bimbingan formal tercatat | **5** (2 Sep, 4 Sep, 9 Sep, 23 Sep, 6 Nov) · target rubrik CPMK 2 "Sangat Baik": **> 8** |
| Jeda sejak bimbingan terakhir | B5 6 Nov 2026; bimbingan berikutnya: **Senin, 9 Nov 2026** bersama Luna |
| Ujian (perkiraan) | Periode akhir semester ±minggu 15–16 (pertengahan–akhir Des 2026); tanggal & tenggat daftar: **[ISI NANTI]** |
| Status WO | ✅ 4 · 🔄 9 · ➖ 1 (total 14) |

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
| WO-14 | B5 · 6 Nov | **Validasi k-fold + arti fisis & rumus matematis fitur citra** | 🔄 | Tabel 13 fitur → `docs/materi/WO-14-fitur-heidata.md`; k-fold → `results/wo14-kfold/`: per sel AUC 0,65–0,80, per percobaan 0,27–0,58 | Selisih = kebocoran efek *batch*; data tambahan (WO-12) jadi kebutuhan utama |

## Hasil Bimbingan 5 (6 Nov 2026) — rincian: `docs/bimbingan/B5_2026-11-04/HASIL.md`
1. **Data citra saja:** data non-citra (CyTOF) ditinggalkan → opsi E tidak dipakai; data utama heiDATA. Status Essig belum diputuskan.
2. **Arah kelas:** terinfeksi vs tidak terinfeksi.
3. **Identitas Teknik Fisika:** kuasai arti fisis dan rumus matematis tiap fitur (*circularity*, *solidity*, dst.).
4. **Validasi:** training / validation / testing dengan k-fold cross-validation (5 atau 10 fold).
5. **Judul:** boleh diganti; prosedur (dicek 7 Nov): surat persetujuan dosen pembimbing — surat sudah diselesaikan mahasiswa.
6. Belum terbahas: izin email Heidelberg, periode ujian, pembimbing pendamping & NIP, judul Bab 3.

## Keputusan yang dibutuhkan di bimbingan berikutnya (B6) — bahan: `docs/bimbingan/B6_2026-11-09/BAHAN.md`
Usulan mahasiswa: heiDATA (paparan HIV) + Essig (hidup vs mati); dua opsi judul disiapkan.
1. Pakai Essig sebagai pelengkap (sel mati; Essig tanpa infeksi HIV) atau heiDATA saja?
2. Kelas heiDATA untuk "terinfeksi vs tidak": (+Vpx dan −Vpx) vs Mock, atau +Vpx vs −Vpx?
3. Rumusan judul baru (prosedur sudah jelas: surat persetujuan dospem).
4. Laporkan bahwa email ke Heidelberg (WO-12) sudah dikirim; balasan tidak diharapkan.
5. Target periode ujian & tenggat; pembimbing pendamping & NIP; judul Bab 3.

## Arsip: eksekusi B4 → B5 (23 Sep → 3 Nov, disampaikan di B5)
1. **Dataset (WO-09):** penelusuran repositori publik (BBBC, BioStudies, Dryad, FlowRepository, heiDATA) → tidak ada citra IFC sel CD4
   terinfeksi HIV; 3 kandidat diperiksa langsung dan diuji coba (pilot).
2. **Ekstraksi fitur (WO-07, WO-10):** 209 sel heiDATA disegmentasi otomatis; 13 fitur fisik/bio-optik per sel diekstrak.
3. **Metode ML (WO-08):** klasifikasi +Vpx vs −Vpx dengan fitur Lamin B1 + kapsid HIV → AUC 0,65 (p = 0,01, signifikan tetapi sedang);
   fitur paling berpengaruh: panjang sumbu mayor inti & kapsid di sekitar inti. Data CyTOF: prediksi sel HIV+ pada donor baru AUC 0,85–0,91.
4. **Temuan keterbatasan:** heiDATA hanya 14 bidang pandang (1 per kondisi) → efek *batch* kuat; tidak ada kelas sel mati.
5. **Tugas bimbingan 1–2 yang tertunda (WO-02, WO-03, WO-05):** baru dikerjakan menjelang B5 — draf gambaran Bab 1, posisi
   keilmuan Teknik Fisika vs Teknik Biomedis/TI, dan materi biologi sel/CD4/HIV (`docs/materi/`).
6. **Administrasi:** sistem kerja, naskah template kampus, ringkasan panduan, draf email permintaan data.
Rincian angka: `docs/bimbingan/B5_2026-11-04/BAHAN.md`.
