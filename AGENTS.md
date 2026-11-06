# Konteks Skripsi
- Judul (ID): KLASIFIKASI KONDISI SEL CD4 PADA INFEKSI HIV BERDASARKAN CITRA IMAGING FLOW CYTOMETRY MENGGUNAKAN MACHINE LEARNING
- Judul (EN): CLASSIFICATION OF CD4 T CELL CONDITIONS IN HIV INFECTION BASED ON IMAGING FLOW CYTOMETRY IMAGES USING MACHINE LEARNING
- Status proposal: DISETUJUI di Simaster UGM (Pengajuan Tugas Akhir ke-1). Tahap berikutnya: bimbingan.
- Bidang: Instrumentasi (Implementasi Kecerdasan Buatan) & Multifisika (Implementasi Sistem Optika)
- Keywords: Sel T CD4, Infeksi HIV, Imaging Flow Cytometry, Machine Learning, Analisis Bio-Optik, Morfometri Sel, Explainable AI
- Ringkasan (dari deskripsi proposal): klasifikasi kondisi sel T CD4 (sehat, terinfeksi, lisis) dari citra imaging flow cytometry multi-kanal, memakai fitur bio-optik dan morfometri sel, dengan validasi Explainable AI (mis. Grad-CAM).
- Masalah (rumusan resmi): Klasifikasi status kondisi sel T CD4 pada infeksi HIV berbasis citra visual (fitur bio-optik dan morfometri inti).
- Metode / model: Ekstraksi fitur fisik/bio-optik (luas, keliling, circularity, solidity, intensitas Lamin B1, sebaran kapsid HIV) + Machine Learning klasik (LogReg, Random Forest, SVM) dengan validasi baku: **Training, Validation, Testing (K-Fold Cross-Validation 5-fold/10-fold)**. Wajib menguasai formulasi matematis & arti fisis setiap fitur.
- Dataset: **heiDATA (Ananth et al. 2024)** — Citra mikroskopi fluoresensi 3D sel T CD4 terpapar HIV-1 (Lamin B1 + kapsid HIV, kondisi +Vpx / −Vpx / Mock). Diputuskan di B5 (6 Nov 2026); data non-citra (CyTOF) ditinggalkan.
- Judul SIMASTER: Sedang dalam proses koordinasi penyesuaian dari *imaging flow cytometry* ke citra mikroskopi fluoresensi (disetujui pembimbing di B5).
- Metrik: Accuracy, Balanced Accuracy, Precision, Recall, F1-Score, ROC-AUC (dengan K-Fold Cross-Validation).
- Mahasiswa: Rahul Ghulam Hidayatulloh — NIM 23/519760/TK/57266
- Dosen pembimbing: Nopriadi, S.T., M.Sc. | preferensi: mengizinkan penggunaan AI di semua tahapan (lihat aturan 15)
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
17. **Dokumen bimbingan & Work Order (struktur sejak 4 Nov 2026):**
    - Setiap bimbingan ke-n punya folder `docs/bimbingan/B<n>_<YYYY-MM-DD>/` berisi **BAHAN.md** (disiapkan sebelum bimbingan:
      laporan WO, yang dibawa, pertanyaan) dan **HASIL.md** (notulensi sesudah bimbingan: tanggapan, keputusan, penugasan baru).
      Template: `docs/bimbingan/TEMPLATE-BAHAN.md`, `TEMPLATE-HASIL.md`.
    - **1 penugasan = 1 dokumen** `docs/work-order/WO-<nn>.md` (template `TEMPLATE-WO.md`): sumber, status, arahan, definisi selesai,
      langkah, log eksekusi, kendala, tanggapan pembimbing. `docs/WORK-ORDER.md` = dashboard ringkas semua WO.
    - Setiap dokumen di atas punya kembaran Google Doc di Drive `Project-Skripsi/bimbingan/` (per folder B<n>, `Work Order/`,
      `00 Template/`). Peta ID: **docs/DRIVE-DOCS.md**. Perbarui Google Doc yang sama (jangan buat file baru).
    - Setelah bimbingan: isi HASIL, buat WO baru, perbarui dashboard & Google Docs. Sebelum bimbingan: buat BAHAN dari laporan WO.
    Sumber utama = file di repo; versi Google Docs (Drive `bimbingan/`) disalin ulang dari repo menjelang setiap bimbingan:
    [Work Order Skripsi](https://docs.google.com/document/d/1g44jOiptFFLlyWT23MJbjdQCIzIcuGF7E2Ov2e4Ltsc/edit) ·
    [Bahan Bimbingan 5](https://docs.google.com/document/d/1pO0eVly4ouybx3KnTrH25khN3zutY_9NTK0XP3wEyyU/edit) ·
    [Materi Persiapan B5 (WO-02/03/05)](https://docs.google.com/document/d/1LJr7OYx56ouTIlyGJgfq5LuLz1JYFqk0Ku3RCMIINkE/edit)
18. **Arah penelitian dari pembimbing (B3 9 Sep, B4 23 Sep):** fokus = **ekstraksi fitur fisik/bio-optik** yang membedakan sel
    normal / terinfeksi / mati, lalu klasifikasi dengan **machine learning (bukan deep learning)**. Jangan menjadikan CNN/deep learning
    sebagai metode utama tanpa persetujuan pembimbing.
15. **Penggunaan AI:** mengikuti arahan pembimbing (Nopriadi, S.T., M.Sc.) — AI **boleh dipakai untuk semua tahapan**
    (kode, analisis, penulisan naskah). Keputusan pengguna (2026-11-03): ikuti arahan pembimbing.
    Aturan 6 dan 7 tetap berlaku (angka hanya dari results/, sitasi hanya dari refs.bib yang terverifikasi — tidak ada
    referensi/data fiktif). Pengguna tetap harus memahami isi karena akan diuji di sidang.
16. Ikuti tata tulis kampus (docs/PANDUAN-KAMPUS.md): PUEBI, istilah asing miring, kalimat pasif tanpa "saya/penulis",
    persamaan bernomor dengan variabel & satuan SI didefinisikan, grafik bersatuan & berlegenda, intisari ≤ 200 kata/3 alinea.
19. **Cek koneksi iPad ↔ laptop (sejak 4 Nov 2026).** Bila pengguna bertanya apakah sesi ini terhubung ke komputer/laptop,
    **jangan menjawab dari ingatan**. Jalankan pengecekan ini lalu laporkan hasilnya apa adanya:
    `$env:COMPUTERNAME`, folder kerja, `Test-Path data\raw\heidata-MUXYRY`, `git log -1`, `git status -sb`.
    - **Terhubung ke laptop** bila host = `DESKTOP-2I1K2HA`, folder = `D:\rahul\Project Skripsi\skripsi-ml`, dan data mentah ada.
    - Bila perintah PowerShell/Windows tidak ada, host berbeda, atau `data/raw` kosong, ini **sesi cloud** (claude.ai/code).
      Katakan terus terang bahwa sesi ini tidak bisa mengolah data mentah, lalu sarankan Remote Control (`/remote-control` di laptop).

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
