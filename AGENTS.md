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
- Dosen pembimbing: Nopriadi, S.T., M.Sc. | preferensi: [ISI NANTI]
- Naskah: LaTeX (template kampus ada, diletakkan di thesis/template-kampus/)
- Deadline: akhir semester ini, sekitar Desember 2026 (tanggal pasti: [ISI NANTI])
- GitHub: https://github.com/raaahl15 (repo: [ISI NANTI])

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
11. Naskah LaTeX ada di thesis/ (main.tex + bab*.tex). Setelah mengedit naskah, pastikan tidak merusak kompilasi (CI GitHub Actions akan membangun PDF).

# Struktur
Lihat README.md. Data besar dan model ada di Google Drive (lokasi dicatat di bagian Dataset).
