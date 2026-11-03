# Konteks Skripsi
- Judul (ID): KLASIFIKASI KONDISI SEL CD4 PADA INFEKSI HIV BERDASARKAN CITRA IMAGING FLOW CYTOMETRY MENGGUNAKAN MACHINE LEARNING
- Judul (EN): CLASSIFICATION OF CD4 T CELL CONDITIONS IN HIV INFECTION BASED ON IMAGING FLOW CYTOMETRY IMAGES USING MACHINE LEARNING
- Status proposal: DISETUJUI di Simaster UGM (Pengajuan Tugas Akhir ke-1). Tahap berikutnya: bimbingan.
- Bidang: Instrumentasi (Implementasi Kecerdasan Buatan) & Multifisika (Implementasi Sistem Optika)
- Keywords: Sel T CD4, Infeksi HIV, Imaging Flow Cytometry, Machine Learning, Analisis Bio-Optik, Morfometri Sel, Explainable AI
- Ringkasan (dari deskripsi proposal): klasifikasi kondisi sel T CD4 (sehat, terinfeksi, lisis) dari citra imaging flow cytometry multi-kanal, memakai fitur bio-optik dan morfometri sel, dengan validasi Explainable AI (mis. Grad-CAM).
- Masalah (rumusan resmi): [ISI NANTI]
- Metode / model: [ISI NANTI] (catatan: Grad-CAM mensyaratkan model berbasis CNN)
- Dataset: [ISI NANTI] (nama, sumber, ukuran, format, lokasi di Drive). BELUM ADA.
- Metrik: [ISI NANTI]
- Dosen pembimbing: Nopriadi, S.T., M.Sc. | preferensi: mengizinkan penggunaan AI di semua tahapan (lisan, 2026-11-03; lihat aturan 15)
- Dosen pembimbing pendamping: belum ada / belum dipastikan (sementara `-` di thesis/data_skripsi.tex) — konfirmasi ke Pak Nopriadi
- Naskah: **draf di Google Docs per bab** (Drive `Project-Skripsi/naskah/`) → **final di LaTeX** (`thesis/`, memakai template resmi DTNTF: `skripsidtntf.cls` + BibTeX `skripsi.bst`; salinan asli di `thesis/template-kampus/`). Konversi per bab setelah disetujui dosen; konvensi di docs/PANDUAN-GDOCS.md
- Panduan kampus: docs/PANDUAN-KAMPUS.md (ringkasan Panduan Pelaksanaan Skripsi TF UGM 2026: aturan AI, timeline 16 minggu, bimbingan, tata tulis, ujian, penilaian)
- Deadline: akhir semester ini, sekitar Desember 2026 (tanggal pasti: [ISI NANTI])
- GitHub: https://github.com/raaahl15/Project-Skripsi (private). Folder lokal di laptop utama: `D:\rahul\Project Skripsi\skripsi-ml\`
- Google Drive: folder `Project-Skripsi/`; folder `naskah/` dibagikan ke Pak Nopriadi (nopriadi@ugm.ac.id, akses komentar)

# Aturan Kerja (berlaku untuk semua agent)
1. Awal sesi: baca docs/STATUS.md dan docs/REVISI.md.
2. Akhir sesi: update docs/STATUS.md, lalu commit.
3. Naskah: Indonesia formal akademik. Kode dan komentar: Inggris.
4. Jangan ubah data mentah. Semua eksperimen reproducible (seed tetap, config di configs/).
5. Setiap eksperimen: config disimpan di configs/, hasil di results/.
6. Angka di naskah HARUS berasal dari file di results/. Jangan mengetik angka dari ingatan.
7. Jangan mengarang sitasi. Referensi hanya boleh yang ada di refs.bib dan sudah diverifikasi pengguna.
8. Jangan commit data besar, checkpoint, atau rahasia.
9. Jika tidak yakin, tanya pengguna; jangan berasumsi.
10. Pengguna harus bisa memahami dan membela semua isi: jelaskan alasan di balik setiap keputusan teknis penting.
11. Naskah: bab yang belum dikonversi → edit di Google Docs (link di bawah). Bab yang sudah dikonversi → edit di thesis/*.tex; pastikan tidak merusak kompilasi (CI GitHub Actions membangun PDF).
12. Di Google Docs ikuti konvensi docs/PANDUAN-GDOCS.md (Heading bawaan, sitasi `[@kunci]`, persamaan `$...$`, sumber angka dari results/).
13. **Akhir setiap sesi: tambahkan entri di docs/RIWAYAT-PENGERJAAN.md** (entri terbaru di atas).
14. **Setiap perubahan sistem** (struktur, alur kerja, alat, lokasi file): perbarui MASTER-SKRIPSI-SETUP.md dan catat di bagian 10-nya.
15. **PENGGUNAAN AI — mengikat semua agent.**
    - Panduan Skripsi TF UGM 2026 §4.1 (tertulis, disahkan Kadep): AI hanya untuk penyuntingan tata bahasa & penerjemahan;
      dilarang memproduksi substansi analisis, merangkai ide penelitian, atau membuat literatur fiktif.
    - **Pembimbing (Nopriadi, S.T., M.Sc.) mengizinkan AI untuk semua tahapan** — konfirmasi LISAN, dilaporkan pengguna 2026-11-03,
      **belum tercatat tertulis** (target: dicatat di SIMASTER → Catatan bimbingan). Penguji & KaProdi tetap menilai CPMK 4 (etika ilmiah).
    - Maka agent BOLEH membantu semua tahap (kode, analisis, draf naskah), DENGAN batasan yang tetap berlaku tanpa pengecualian:
      a. **Tidak ada literatur, sitasi, data, atau angka fiktif** — sitasi hanya dari refs.bib yang diverifikasi pengguna; angka hanya dari results/.
      b. Draf teks dari AI ditandai jelas sebagai draf (mis. komentar "DRAF AI" di Docs/LaTeX) dan **wajib ditinjau, disunting,
         dan disetujui pengguna** sebelum dianggap final; pengguna harus memahami dan mampu membela setiap kalimat & baris kode di sidang.
      c. Bagian yang menyangkut ide/kontribusi penelitian (rumusan masalah, tujuan, interpretasi hasil, kesimpulan) diputuskan
         pengguna dan pembimbing; agent menyajikan opsi + alasan, bukan memutuskan.
      d. Setiap bantuan AI yang substansial dicatat di docs/RIWAYAT-PENGERJAAN.md (transparansi bila ditanya penguji).
      e. Similarity check tetap wajib sebelum daftar ujian.
16. Ikuti tata tulis kampus (docs/PANDUAN-KAMPUS.md): PUEBI, istilah asing miring, kalimat pasif tanpa "saya/penulis",
    persamaan bernomor dengan variabel & satuan SI didefinisikan, grafik bersatuan & berlegenda, intisari ≤ 200 kata/3 alinea.

# Lokasi Google Drive
- Folder utama: [Project-Skripsi](https://drive.google.com/drive/folders/1L5EdiZuWsGFqOQ64QzMGHmxBUs63yKJ6)
- Naskah (Google Docs): [naskah/](https://drive.google.com/drive/folders/1B0gIkugJe1yVZWEBZaS62jG9fA5LRTU7)
  - [Bab 1 - Pendahuluan](https://docs.google.com/document/d/1p69-U7fzbd2Ydz3FTPpsLzeso2VxKKuop7Wu87yZU_c/edit) | status: draf
  - [Bab 2 - Tinjauan Pustaka](https://docs.google.com/document/d/1LrQ97_Z0-YM3Cp55wuU83Q8QE8rf2Gl69k1UEBV1nGU/edit) | status: draf
  - [Bab 3 - Pelaksanaan Penelitian](https://docs.google.com/document/d/1PXJV-7R0AnAec47qgtHCnJPVZS0JpDIV5Gif1RwNXU8/edit) | status: draf
  - [Bab 4 - Hasil dan Pembahasan](https://docs.google.com/document/d/1ACWGzFW2NnN6pc6Vcr2viowCTIJKE5-9y7zd-ioeYVY/edit) | status: draf
  - [Bab 5 - Kesimpulan dan Saran](https://docs.google.com/document/d/1VnkG_kycJ_thdN9Uccn_WvxQHZ9RjxeLhXWjkjgbrxQ/edit) | status: draf
- Template skripsi resmi (asli, jangan diubah): [template skripsi teknik fisika 2026](https://drive.google.com/drive/folders/1B6cKBuUzV7s64e6OHGQzxSq73vBb5Vo0)
- Data: [data/](https://drive.google.com/drive/folders/1wcYNg3EGv3t-Ney1ob-lIiztwekcxFx6) (raw/, processed/)
- [models/](https://drive.google.com/drive/folders/1OSlB-5_Z0mu2WMVoLba3eFAAt44nV-DG) · [papers/](https://drive.google.com/drive/folders/19mvT-mO8oCPxfcoPliSO_SveokBSHWnB) · [backup/](https://drive.google.com/drive/folders/1pPGir4R7OWcgDM2mCi5qs9fsSlCJj5Dl) · [bimbingan/](https://drive.google.com/drive/folders/1YjipHgDX7Wvb2MeyM5nzaiJFYCCO_vSe) · [00-BOOTSTRAP/](https://drive.google.com/drive/folders/1j8f-ELyBuVCOGR1CGci8Y5r3LvNUwRiJ)

# Struktur
Lihat README.md. Dasar sistem: MASTER-SKRIPSI-SETUP.md. Data besar dan model ada di Google Drive (link di atas).
