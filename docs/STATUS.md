# STATUS (update di akhir setiap sesi)
Terakhir diperbarui: 2026-11-06

## Posisi saat ini
- Tahap: Pengolahan Data & Eksperimen Model ML (Pasca-Bimbingan 5)
- Minggu ke-10 dari ±16 minggu semester (asumsi mulai 1 Sep 2026; bimbingan 1 = 2 Sep)
- Bimbingan formal terlaksana: **5** (2, 4, 9, 23 Sep; 6 Nov). Bimbingan berikutnya: **Senin, 9 Nov 2026** (bersama Luna)
- Arah dari pembimbing (B5): **Fokus murni ke citra visual** (mikroskopi fluoresens heiDATA), tinggalkan data non-citra. Pahami dasar fisis & rumus matematis fitur morfometri (identitas Teknik Fisika). Terapkan evaluasi baku: Training, Validation (K-Fold CV), Testing.

## Sudah selesai
- Bimbingan 5 terlaksana (6 Nov 2026) tatap muka: keputusan dataset citra visual disepakati & perubahan judul disetujui
- Hasil Bimbingan 5 (`docs/bimbingan/B5_2026-11-04/HASIL.md`) dan penugasan baru WO-14 (`docs/work-order/WO-14.md`) didokumentasikan
- Proposal TA ke-1 disetujui di Simaster UGM (pembimbing: Nopriadi, S.T., M.Sc.)
- Repo skripsi + sistem kerja (Langkah 0) disiapkan; GitHub `raaahl15/Project-Skripsi` (private)
- Struktur Google Drive `Project-Skripsi/` + 5 Google Docs bab; folder `naskah/` dibagikan ke Pak Nopriadi (Commenter)
- Environment Python (.venv, Python 3.13); Google Colab Pro UGM aktif untuk pelatihan ML
- Panduan Skripsi TF 2026 dirangkum (docs/PANDUAN-KAMPUS.md); template LaTeX resmi dipasang di `thesis/`

## Sedang dikerjakan
- **WO-14:** Implementasi K-Fold Cross-Validation (5-fold / 10-fold) pada pipeline ML citra heiDATA
- **WO-14:** Dokumentasi formularium matematis dan tafsiran fisis seluruh fitur morfometri inti (*circularity*, *solidity*, dll.)
- Koordinasi ke bagian Pengajaran/Akademik mengenai mekanisme administratif pergantian judul SIMASTER

## Berikutnya (maks. 3)
1. **Selesaikan evaluasi K-Fold CV & tabel fitur fisis:** Siapkan bahan untuk bimbingan berikutnya pada **Senin, 9 Nov 2026**
2. **Input catatan bimbingan 5 ke SIMASTER:** Masukkan ringkasan B5 agar log bimbingan resmi kampus terisi
3. **Penyusunan draf Bab 3 (Metodologi):** Masukkan alur pemisahan data (Training, Validation K-Fold, Testing) dan rumus matematis fitur

## Hasil konfirmasi & keputusan Bimbingan 5 (2026-11-06)
- **Dataset:** Fokus ke citra visual mikroskopi fluoresens (heiDATA - Ananth et al. 2024). Data tabel non-citra (CyTOF) ditinggalkan.
- **Identitas Keilmuan:** Wajib memahami dan menyajikan rumus matematis serta arti fisis setiap fitur (mis. *circularity*, *solidity*), bukan sekadar black-box ML.
- **Validasi ML:** Wajib menerapkan pembagian Training, Validation, Testing dengan K-Fold Cross-Validation.
- **Judul SIMASTER:** Pergantian judul dari *imaging flow cytometry* ke citra mikroskopi fluoresensi disetujui pembimbing.
- **Rekan Bimbingan:** Bagikan info Google Colab Pro UGM ke Luna.

## Blocker / pertanyaan terbuka
- Prosedur teknis pergantian judul di SIMASTER (apakah form fast-track atau saat pendaftaran ujian) perlu dikonfirmasi ke pengajaran
- NIP pembimbing & pembimbing pendamping: belum diisi/dipastikan
- **Risiko waktu:** Target ujian akhir semester (Desember 2026). Perlu percepatan penulisan draf Bab 1–3 seiring eksperimen ML selesai
- Akses GPU: Menggunakan Google Colab Pro UGM (sudah terbukti cepat dan stabil)
