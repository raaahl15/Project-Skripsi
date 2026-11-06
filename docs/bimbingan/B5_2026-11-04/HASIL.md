# Hasil Bimbingan 5 — 6 Nov 2026
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**

> Dicatat berdasarkan rekaman bimbingan langsung (tatap muka) pada 6 November 2026.
> Bahan persiapan bimbingan sebelumnya: `docs/bimbingan/B5_2026-11-04/BAHAN.md` & `docs/WORK-ORDER.md`.

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 5 |
| Tanggal | 6 Nov 2026 (jadwal semula 4 Nov) |
| Bentuk | Tatap Muka (ruang kerja pembimbing) |
| Tercatat di SIMASTER | [ ] Segera diinput ke catatan bimbingan SIMASTER |

---

## 1. Yang dibawa
- Progres olah data awal (pilot model machine learning) yang dijalankan di **Google Colab Pro** (akun UGM).
- Pembahasan 3 kandidat dataset:
  1. Citra mikroskopi fluoresensi (heiDATA - Ananth et al. 2024): ada infeksi HIV (+Vpx / −Vpx / Mock), berwujud citra 3D fluoresensi, jumlah donor terbatas.
  2. Data flow cytometry tabel (CyTOF Luo et al.): banyak penanda/fitur CD protein, ada label HIV, tetapi **tanpa citra**.
  3. Citra flow cytometry (IFC Essig et al.): berwujud citra sel tunggal IFC, tetapi **tanpa kondisi infeksi HIV**.
- Hasil akurasi awal pilot klasifikasi citra fluoresensi (±65% / 0,65).
- Bahan Bimbingan 5 (`BAHAN.md`), Work Order (`WORK-ORDER.md` WO-01 s.d. WO-13), dan draf usulan judul.

---

## 2. Pertanyaan & tanggapan pembimbing

### a. Batasan Data: Fokus ke Citra Visual (Tinggalkan Non-Citra)
- Pembimbing menanyakan kembali inti tujuan riset: yaitu **klasifikasi kondisi sel CD4 apakah terinfeksi HIV atau tidak**.
- Terhadap temuan bahwa data flow cytometry tidak memiliki citra sedangkan citra mikroskopi fluoresensi memiliki visual, pembimbing memberi arahan tegas:
  > *"Gimana kalau dibatasi citra saja datanya? Supaya kamu ketika presentasi nggak bingung... Ini kan instrumentasi sistem visual, jadi pakai visual. Tinggalkan aja yang bukan citra itu."*
- **Alasan keilmuan Teknik Fisika:** Ruang lingkup riset berada di bawah bidang keahlian **Instrumentasi & Sistem Optika / Visual**. Jika menggunakan data tabular tanpa visual, aspek fisis dan instrumentasinya tidak tampak, sehingga sulit dipertanggungjawabkan saat ujian pendadaran dan kehilangan ciri khas Teknik Fisika.

### b. Aspek Fisis & Rumus Matematis Fitur (Ciri Khas Teknik Fisika vs Informatika)
- Pembimbing mengamati visualisasi deteksi/segmentasi sel (titik-titik penanda dan kontur sel) serta daftar fitur yang diekstrak.
- Pembimbing menegaskan bahwa sebagai mahasiswa Teknik Fisika, mahasiswa **wajib memahami makna fisis dan formulasi matematis** dari setiap fitur yang diekstrak:
  > *"Kamu bagian Teknik Fisika, mesti tahu fisiknya... Kalau gini mesti Teknik Informatika. Kamu mesti tahu circularity itu apa, rumus matematikanya seperti apa... solidity itu apa, rumus matematikanya gimana."*
- Mahasiswa diminta tidak memperlakukan machine learning sebagai *black-box*, melainkan harus menguasai definisi fisis dan dasar matematis setiap parameter morfometri/bio-optik yang dimasukkan ke model.

### c. Metodologi Validasi Machine Learning (Training, Validation, Testing)
- Saat mahasiswa menunjukkan akurasi awal sekitar 65% (0,65), pembimbing menanyakan apakah sudah dilakukan validasi.
- Pembimbing mengedukasi mahasiswa mengenai prosedur evaluasi model ML yang baku:
  1. **Training set:** Digunakan untuk melatih model dan mencari bobot/parameter optimal.
  2. **Validation set:** Digunakan untuk memastikan bobot/parameter sudah cukup belajar (tuning/evaluasi konvergensi).
  3. **Testing set:** Digunakan untuk menguji seberapa baik model saat menghadapi data baru (*unseen data*).
- Pembimbing menginstruksikan mahasiswa untuk mengimplementasikan **K-Fold Cross-Validation** (misalnya 5-fold atau 10-fold cross validation) untuk membuktikan kestabilan model.

### d. Infrastruktur Komputasi & Saran untuk Rekan Bimbingan
- Mahasiswa menjelaskan bahwa proses komputasi awal di laptop lambat, sehingga dialihkan ke **Google Colab Pro** (fasilitas gratis 1 tahun akun UGM) dan berjalan jauh lebih cepat.
- Pembimbing meminta mahasiswa untuk memberitahukan solusi Google Colab gratisan UGM ini kepada **Luna** (rekan bimbingan satu dosen) yang laptopnya juga terkendala saat pemrosesan.

### e. Penyesuaian Judul di SIMASTER
- Mahasiswa menanyakan konsekuensi pergantian jenis citra (dari *imaging flow cytometry* ke *citra mikroskopi fluoresensi*) terhadap judul resmi yang telah disetujui di SIMASTER.
- Pembimbing menyampaikan bahwa **pergantian judul tidak menjadi masalah**:
  > *"Pergantian judul sepertinya nggak begitu masalah. Nanti coba tanya pengajaran gimana caranya, atau nanti belakangan pas ujian/pendadaran kalau datanya memang tidak ada yang flow cytometry visual."*

---

## 3. Keputusan Pembimbing

| No | Poin Masalah / Pertanyaan | Keputusan Pembimbing |
|---|---|---|
| 1 | **Pemilihan Dataset** | **Fokus penuh pada dataset citra (mikroskopi fluoresens heiDATA).** Tinggalkan data tabular tanpa citra (CyTOF Luo). Batasi hanya pada data visual. |
| 2 | **Perubahan Judul SIMASTER** | **Disetujui untuk diganti.** Judul disesuaikan dari *imaging flow cytometry* menjadi citra mikroskopi fluoresens. Tanyakan prosedur ke bagian akademik/pengajaran fakultas atau proses menjelang ujian. |
| 3 | **Fitur Morfometri / Bio-optik** | **Wajib menyusun dasar fisis & rumus matematis** dari setiap fitur (mis. *circularity*, *solidity*, rasio intensitas, dsb.) sebagai landasan ilmiah Teknik Fisika. |
| 4 | **Metodologi Evaluasi ML** | Terapkan pembagian baku: **Training, Validation, Testing**, dan gunakan metode **K-Fold Cross-Validation** (5-fold / 10-fold). |
| 5 | **Penggunaan Komputasi** | Lanjutkan eksperimen di **Google Colab Pro** (akun UGM) untuk percepatan iterasi training. Bagikan info akses ke Luna. |

---

## 4. Penugasan Baru (→ Work Order)

| WO | Tugas | Rincian / Keluaran | Target |
|---|---|---|---|
| **WO-14** | **Implementasi K-Fold Cross-Validation & Dokumentasi Matematis/Fisis Fitur** | 1. Implementasikan 5-fold & 10-fold cross-validation pada pipeline ML citra fluoresens heiDATA.<br>2. Susun dokumen referensi rumus matematis & arti fisis seluruh fitur morfometri inti (*circularity*, *solidity*, dll.).<br>3. Tanyakan prosedur penyesuaian judul TA ke bagian Pengajaran/SIA Departemen. | **Senin, 9 Nov 2026** (siap diperlihatkan saat bimbingan bersama Luna) |

---

## 5. Revisi Dokumen & Naskah (→ docs/REVISI.md)
1. **Fokus Ruang Lingkup:** Hapus opsi gabungan data non-citra (CyTOF) dari draf naskah/proposal; arahkan Bab 1 & Bab 3 murni ke citra mikroskopi fluoresensi dan instrumentasi sistem visual.
2. **Bab 3 (Metodologi):**
   - Masukkan subbab khusus rumus matematis fitur morfometri dan bio-optik.
   - Masukkan diagram alur pemisahan data: Training, Validation (K-Fold CV), dan Testing.

---

## 6. Jadwal Bimbingan Berikutnya
- **Hari/Tanggal:** **Senin, 9 November 2026**
- **Agenda:** Mengevaluasi hasil K-Fold Cross-Validation dan perkembangan model ML bersama pembimbing (sekalian bimbingan bersama Luna).
