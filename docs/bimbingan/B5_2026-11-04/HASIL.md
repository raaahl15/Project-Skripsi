# Hasil Bimbingan 5 — 6 Nov 2026
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**

> Disusun dari rekaman bimbingan (±11 menit). Transkrip otomatis berkualitas sedang: **kutipan di bawah adalah parafrase**, bukan kata per kata.
> Hal yang tidak terdengar jelas ditandai **[perlu konfirmasi]**.
> Disusun awal oleh Antigravity (6 Nov), diperiksa ulang terhadap rekaman dan diperbaiki oleh Claude Code (7 Nov).

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 5 |
| Tanggal | 6 Nov 2026 (folder bernama 2026-11-04 = rencana semula) |
| Bentuk | Tatap muka |
| Tercatat di SIMASTER | [x] 8 Nov 2026 — sebagai bimbingan ke-1 setelah persetujuan judul (form "Bimbingan Tugas Akhir Ke 2"); dokumen: `Bimbingan5_Skripsi_Rahul.pdf` |

## 1. Yang dibawa
- Slide Bimbingan 5 (PDF 12 halaman, Drive `bimbingan/B5 - 2026-11-04/`), dengan usulan **opsi E** (tiga dataset: heiDATA, CyTOF Luo, Essig).
- Hasil pilot: heiDATA (citra mikroskopi fluoresens, AUC 0,65), CyTOF Luo (tanpa citra, AUC 0,85–0,91), Essig (citra IFC tanpa infeksi).
- Work Order WO-01 s.d. WO-13 dan Bahan Bimbingan 5.

## 2. Pertanyaan & tanggapan pembimbing
**a. Tujuan dan data.** Pembimbing menegaskan tujuan: mengklasifikasi sel CD4 **terinfeksi atau tidak**, sehingga dibutuhkan data sel terinfeksi
dan tidak terinfeksi. Pembimbing menanyakan alasan memakai tiga dataset dan cara memperlakukan data yang berbentuk citra dan yang tidak.

**b. Batasi pada data citra.** Pembimbing mengusulkan data **dibatasi pada citra saja** dan data yang bukan citra **ditinggalkan**, supaya fokus
dan tidak membingungkan saat presentasi, karena topiknya instrumentasi/sistem visual. → **Opsi E tidak dipakai; CyTOF Luo keluar.**
Essig (citra IFC, tanpa infeksi) tidak dibahas secara eksplisit.

**c. Arti fisis dan rumus fitur.** Pembimbing menanyakan arti fitur pada hasil (mis. *circularity*). Mahasiswa baru bisa menjelaskan sebagai
"bentuk", belum rumusnya. Arahan: pelajari tiap fitur, apa itu *circularity*, *solidity*, dan seterusnya, **beserta rumus matematisnya**,
karena Teknik Fisika harus memahami sisi fisisnya; tanpa itu pekerjaannya sama saja dengan teknik informatika.

**d. Penanda pada citra.** Pembimbing menanyakan arti tanda merah/kontur pada citra dan siapa yang menandai titik-titiknya. Mahasiswa menjawab
"machine learning". *Koreksi:* kontur inti dan titik kapsid dibuat oleh **segmentasi klasik** (ambang intensitas + operasi morfologi), bukan ML.

**e. Akurasi dan validasi.** Mahasiswa menyebut hasil sekitar 0,65 ("65 persen") dan bahwa validasi belum dilakukan. Pembimbing menjelaskan
pembagian data menjadi **training** (mencari bobot/parameter), **validation** (memastikan bobot sudah cukup), dan **testing** (menguji seberapa
baik model), serta meminta **k-fold cross-validation** (mis. 5-fold atau 10-fold).
*Koreksi:* 0,65 adalah **ROC AUC**, bukan akurasi (*balanced accuracy* = 0,617). Pilot **sudah** memakai validasi *leave-one-figure-out* +
uji permutasi, yaitu bentuk *cross-validation* berkelompok. Perlu diluruskan di bimbingan berikutnya.

**f. Komputasi.** Mahasiswa menjelaskan komputasi dipindah dari laptop ke Google Colab (Pro gratis setahun lewat akun UGM). Pembimbing
menyinggung Luna (rekan satu pembimbing) yang laptopnya tidak kuat → info Colab UGM sudah dibagikan ke Luna (dikonfirmasi mahasiswa, 7 Nov).

**g. Judul.** Mahasiswa menjelaskan bahwa citra *imaging flow cytometry* untuk infeksi HIV tidak tersedia. Pembimbing: **pergantian judul
sepertinya tidak masalah**. Prosedur (ajukan ulang di Simaster / tanya bagian pengajaran / saat ujian) **tidak terdengar jelas [perlu konfirmasi]**.

## 3. Keputusan
| No | Pertanyaan (Bahan B5 §6) | Keputusan |
|---|---|---|
| 1 | Dataset final & judul | **Data citra saja**; data non-citra (CyTOF) ditinggalkan. Data utama: heiDATA. Status Essig: belum diputuskan. Judul boleh diganti; prosedur [perlu konfirmasi] |
| 2 | Kelas klasifikasi | Arah: **terinfeksi vs tidak terinfeksi**. Pemetaan ke kelas heiDATA (+Vpx / −Vpx / Mock) belum ditetapkan |
| 3 | Opsi A–E | **Opsi E ditolak secara implisit** (karena ada data non-citra). Yang tersisa sesuai arahan: A (heiDATA), dengan atau tanpa Essig |
| 4 | Izin email ke pemilik heiDATA (WO-12) | Tidak dibahas |
| 5 | Target periode ujian & tenggat | Tidak dibahas |
| 6 | Pembimbing pendamping & NIP | Tidak dibahas |
| 7 | Judul Bab 3 | Tidak dibahas |

## 4. Penugasan baru (→ Work Order)
| WO | Tugas | Target |
|---|---|---|
| WO-14 | Validasi k-fold (training/validation/testing) + tabel arti fisis dan rumus matematis tiap fitur | Bimbingan berikutnya |

## 5. Revisi (→ naskah)
- Bab 1 dan 3 diarahkan ke klasifikasi berbasis citra (mikroskopi fluoresens); bagian CyTOF dan opsi tiga dataset dihapus dari rencana.
- Bab 3: subbab definisi dan rumus fitur; alur pembagian data training/validation/testing dan k-fold.

## 6. Jadwal bimbingan berikutnya
- Senin, 9 Nov 2026, bersama Luna, untuk melihat hasil k-fold (dikonfirmasi mahasiswa, 7 Nov).

## 7. Catatan untuk mahasiswa
- Luruskan tiga jawaban di bimbingan berikutnya: (1) validasi pilot sudah ada (*leave-one-figure-out*), (2) 0,65 adalah AUC, (3) penanda citra
  berasal dari segmentasi klasik, bukan ML.
- Bawa kembali empat pertanyaan yang belum terbahas (no. 4–7 di atas).
