# WORK ORDER — Tracker Pengerjaan Skripsi
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**
Judul (Simaster, ditetapkan bimbingan 4): *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry
Menggunakan Machine Learning*
Terakhir diperbarui: **2026-11-03**

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
| Bimbingan formal tercatat | **4** (2 Sep, 4 Sep, 9 Sep, 23 Sep) · target rubrik CPMK 2 "Sangat Baik": **> 8** |
| Jeda sejak bimbingan terakhir | 6 minggu (23 Sep → 3 Nov) — panduan: min. 1× per 2 minggu |
| Ujian (perkiraan) | Periode akhir semester ±minggu 15–16 (pertengahan–akhir Des 2026); tanggal & tenggat daftar: **[ISI NANTI]** |
| Status WO | ✅ 4 · 🔄 7 · ⏳ 1 · ➖ 1 (total 13) |

## Daftar Work Order

| ID | Dari | Arahan / tugas | Status | Eksekusi & bukti | Catatan |
|---|---|---|---|---|---|
| WO-01 | B1 · 2 Sep | Cari dataset | ✅ | heiDATA ditemukan & dibawa ke B2 (4 Sep). Penelusuran ulang 3 Nov: 7 dataset dinilai → `docs/DATASET-KANDIDAT.md` | Dilanjutkan oleh WO-09 |
| WO-02 | B1 · 2 Sep | Susun gambaran Bab 1 | 🔄 | Belum dikerjakan s.d. 3 Nov; draf gambaran (alur latar belakang, perumusan masalah, tujuan, manfaat) dibuat 3 Nov → `docs/materi/WO-02-gambaran-bab1.md` | Menunggu keputusan dataset/judul B5; sitasi latar belakang belum ada |
| WO-03 | B2 · 4 Sep | Rumuskan perbedaan skripsi dengan Teknik Biomedis & Teknologi Informasi | 🔄 | Belum dikerjakan s.d. 3 Nov; draf 1 halaman (jawaban singkat + tabel perbandingan) dibuat 3 Nov → `docs/materi/WO-03-posisi-teknik-fisika.md` | Mahasiswa mempelajari & menyampaikan dengan kata-kata sendiri |
| WO-04 | B2 · 4 Sep | Pelajari metode deep learning | ➖ | Digantikan keputusan B4 (deep learning → machine learning) | Materi ML dipelajari lewat WO-08 |
| WO-05 | B2 · 4 Sep | Pelajari struktur sel, sel T CD4, biologi HIV | 🔄 | Belum dikerjakan s.d. 3 Nov; materi ringkas (struktur sel & lamina inti, sel T CD4, HIV-1 & siklus replikasi, SAMHD1/Vpx, ciri sel normal/terinfeksi/mati, dasar optika fluoresens/IFC, 5 latihan soal) dibuat 3 Nov → `docs/materi/WO-05-biologi-sel-cd4-hiv.md` | Mahasiswa mempelajari; pernyataan umum perlu sitasi buku teks untuk Bab 2 |
| WO-06 | B3 · 9 Sep | Ganti judul sesuai saran pembimbing | ✅ | Judul baru dibawa ke B4; ditetapkan & disetujui di Simaster | Digantikan judul final B4 |
| WO-07 | B3 · 9 Sep | **Ekstraksi fitur**: karakteristik fisik/bio-optik pembeda sel **normal, terinfeksi, mati** | 🔄 | Pilot heiDATA (3 Nov): segmentasi inti Lamin B1 (209 sel) + fitur morfometri inti, intensitas & rasio tepi/inti Lamin B1, jumlah kapsid HIV di dalam/sekitar inti; peringkat fitur dengan SHAP → `results/pilot-heidata/` | Kelas **"mati" belum ada** di heiDATA; CyTOF Luo punya apoptosis tetapi bukan fitur optik |
| WO-08 | B4 · 23 Sep | Cari **metode** machine learning yang tepat | 🔄 | Pilot: Logistic Regression & Random Forest (heiDATA), HistGradientBoosting (CyTOF); validasi *leave-one-figure/donor-out* + uji permutasi → `results/pilot-heidata/metrics_classify.json`, `results/pilot-luo/metrics_classify.json` | Berikutnya: bandingkan SVM, seleksi fitur; tetapkan metode di B5 |
| WO-09 | B4 · 23 Sep | **Fiksasi dataset** | 🔄 | Tidak ada dataset IFC publik sel CD4 terinfeksi HIV. Kandidat: heiDATA (citra mikroskopi, HIV, Lamin B1), CyTOF Luo (HIV, sehat/terinfeksi/apoptosis, tanpa citra), IFC Essig (citra IFC, tanpa HIV) → `docs/DATASET-KANDIDAT.md`, `docs/bimbingan/bahan-bimbingan-5.md` | **Keputusan diminta di B5** (berdampak ke judul) |
| WO-10 | B4 · 23 Sep | Tentukan **fitur yang diekstrak** | 🔄 | Daftar fitur awal di `src/data/heidata_cells.py` (11 fitur morfometri/intensitas + 2 fitur kapsid) | Usulan tambahan: tekstur (GLCM), fitur multi-kanal, fitur 3D z-stack |
| WO-11 | Inisiatif | Sistem kerja skripsi (repo GitHub, Google Drive, naskah Google Docs + LaTeX template kampus, backup) | ✅ | `README.md`, `MASTER-SKRIPSI-SETUP.md`, `thesis/` (PDF 21 hlm ter-*compile*) | — |
| WO-12 | Inisiatif | Permintaan citra tambahan ke pemilik dataset heiDATA (Heidelberg) | ⏳ | Draf email: `docs/korespondensi/permintaan-data-heidata.md` | Menunggu persetujuan pembimbing (B5) |
| WO-13 | Inisiatif | Ringkasan Panduan Skripsi TF 2026 | ✅ | `docs/PANDUAN-KAMPUS.md` | — |

## Eksekusi sejak bimbingan terakhir (B4 · 23 Sep → 3 Nov) — untuk disampaikan di B5
1. **Dataset (WO-09):** penelusuran repositori publik (BBBC, BioStudies, Dryad, FlowRepository, heiDATA) → tidak ada citra IFC sel CD4
   terinfeksi HIV; 3 kandidat diperiksa langsung dan diuji coba (pilot).
2. **Ekstraksi fitur (WO-07, WO-10):** 209 sel heiDATA disegmentasi otomatis; 13 fitur fisik/bio-optik per sel diekstrak.
3. **Metode ML (WO-08):** klasifikasi +Vpx vs −Vpx dengan fitur Lamin B1 + kapsid HIV → AUC 0,65 (p = 0,01, signifikan tetapi sedang);
   fitur paling berpengaruh: panjang sumbu mayor inti & kapsid di sekitar inti. Data CyTOF: prediksi sel HIV+ pada donor baru AUC 0,85–0,91.
4. **Temuan keterbatasan:** heiDATA hanya 14 bidang pandang (1 per kondisi) → efek *batch* kuat; tidak ada kelas sel mati.
5. **Tugas bimbingan 1–2 yang tertunda (WO-02, WO-03, WO-05):** baru dikerjakan menjelang B5 — draf gambaran Bab 1, posisi
   keilmuan Teknik Fisika vs Teknik Biomedis/TI, dan materi biologi sel/CD4/HIV (`docs/materi/`).
6. **Administrasi:** sistem kerja, naskah template kampus, ringkasan panduan, draf email permintaan data.
Rincian angka: `docs/bimbingan/bahan-bimbingan-5.md`.

## Keputusan yang dibutuhkan di bimbingan berikutnya (B5)
1. Dataset final (WO-09) dan dampaknya ke judul (fast-track Simaster?).
2. Definisi kelas: normal / terinfeksi / mati tidak tersedia utuh dalam satu dataset citra — kelas apa yang dipakai?
3. Persetujuan mengirim email permintaan data ke Heidelberg (WO-12).
4. Jadwal bimbingan rutin hingga ujian (min. 1×/2 minggu; idealnya mingguan) & target periode ujian.
5. Status pembimbing pendamping & NIP pembimbing (halaman pengesahan).
