# Hasil Bimbingan 6 — 9 Nov 2026
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**

> Disusun oleh Claude Code (9 Nov) dari rekaman bimbingan (±9 menit; transkrip otomatis Whisper *medium*, kualitas sedang).
> **Kutipan di bawah adalah parafrase**, bukan kata per kata. Hal yang tidak terdengar jelas ditandai **[perlu konfirmasi]**.
> Transkrip tidak disimpan di repo karena repo publik dan rekaman memuat percakapan mahasiswa lain.

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 6 (SIMASTER: bimbingan ke-2 setelah persetujuan judul) |
| Tanggal | Senin, 9 Nov 2026 |
| Bentuk | Tatap muka, bergiliran dengan mahasiswa bimbingan lain |
| Tercatat di SIMASTER | [ ] belum |

## 1. Yang dibawa
- Slide Bimbingan 6 (13 slide) + PDF `Bimbingan6_Skripsi_Rahul.pdf`; Bahan B6 (`BAHAN.md`).
- Yang dipresentasikan dan dibahas hanya **hasil k-fold heiDATA (WO-14)**. Usulan dataset heiDATA + Essig, opsi judul, dan pertanyaan §4 BAHAN
  **tidak dibahas**.

## 2. Pertanyaan & tanggapan pembimbing
**a. K-fold per sel vs berkelompok.** Mahasiswa menjelaskan: diuji per sel hasilnya bagus, diuji berkelompok (per percobaan) di bawah 0,5.
Pembimbing: pendeteksian dilakukan **satu per satu sel** (sel ini terinfeksi atau tidak), bukan berkelompok, **jadi yang baku adalah per sel**.
→ Lihat §8: unit klasifikasi memang sel, tetapi pembagian data latih/uji tetap perlu dipisah per percobaan agar tidak bocor. Belum sempat diluruskan.

**b. Jumlah fitur.** Pembimbing menanyakan jumlah fitur per sel. Mahasiswa menjawab **17** [perlu konfirmasi]. *Koreksi:* heiDATA memakai
**13 fitur** (8 morfometri inti, 3 intensitas Lamin B1, 2 kapsid); Essig 19 fitur *brightfield*. Lamin B1 = penanda struktur/bentuk inti,
kapsid = penanda paparan HIV.

**c. Alur training / validation / testing.** Pembimbing menjelaskan ulang: data dibagi tiga (training, validation, testing). Pada data validasi
dilakukan *k-fold cross-validation* (baku 5): data dibagi lima, empat untuk latih, satu untuk uji, bergiliran, "seolah-olah punya lima data".
Hasil *cross-validation* dipakai untuk memutuskan apakah pelatihan sudah cukup / parameter sudah bagus; **setelah itu baru testing**.
Mahasiswa menyatakan prosesnya sudah seperti itu (validasi dalam untuk memilih hiperparameter, fold luar sebagai uji).

**d. Hasil.** Pembimbing menanyakan hasil testing. Mahasiswa: tertinggi **0,8**; disebut juga 0,6 dan 0,72 — Lamin B1 saja vs Lamin B1 + kapsid.
*Catatan:* angka ini adalah **ROC AUC k-fold per sel** (`results/wo14-kfold/`: HIV vs Mock Lamin B1 0,74–0,80; +Vpx vs −Vpx 0,66–0,79),
bukan akurasi/persen. Pemetaan angka ke tugas yang disebut lisan [perlu konfirmasi].

**e. Perbandingan dengan penelitian lain.** Pembimbing menanyakan hasil peneliti lain; mahasiswa: perbandingan belum selesai.
Pembimbing: "sudah lumayan; **yang penting kamu bisa menjelaskan hasilmu**."

**f. Metrik evaluasi (arahan utama).** Hasil tidak cukup akurasi; ada beberapa metrik (F-score, recall, dll.). Mahasiswa harus **memilih metrik
yang perlu dipakai dan menjelaskan alasannya**: karena ini untuk uji kesehatan, pertimbangkan mana yang lebih penting dihindari —
**false positive atau false negative**. Tujuannya agar pekerjaan tidak "seperti orang informatika" yang hanya mengolah lalu melaporkan hasil.
→ **WO-15**.

**g. Judul.** Mahasiswa menanyakan surat persetujuan ganti judul (minta tanda tangan pembimbing). Pembimbing: **nanti belakangan saja**.

**h. SIMASTER.** Pembimbing memeriksa catatan bimbingan di SIMASTER: baru tercatat satu kali dan belum disetujui. Mahasiswa menjelaskan
bahwa sebelum pengajuan judul sudah bimbingan empat kali dan dicatat mulai dari setelah persetujuan judul; pembimbing menerima.
Pembimbing: kalau bertemu, **tulis di SIMASTER** — bagi pembimbing tidak berpengaruh, tetapi mahasiswa punya syarat jumlah bimbingan minimal.

## 3. Keputusan
| No | Pertanyaan (Bahan B6 §4) | Keputusan |
|---|---|---|
| 0–1 | Dataset heiDATA + Essig / Illinois | Tidak dibahas |
| 2 | Opsi judul | Tidak dibahas; surat persetujuan ganti judul **ditunda** ("belakangan saja") |
| 3 | Kelas Bagian A (HIV vs Mock dari kapsid) | Tidak dibahas |
| 4 | K-fold berkelompok dilaporkan berdampingan | Pembimbing: evaluasi baku **per sel** (lihat §2a dan §8) |
| 5 | Koreksi AUC B5 0,65 → 0,57 | Tidak dibahas |
| 6 | Ujian & tenggat; pembimbing pendamping; judul Bab 3 | Tidak dibahas |
| — | Metrik evaluasi | Pilih metrik + alasan berdasarkan konteks medis (FP vs FN) → WO-15 |

## 4. Penugasan baru (→ Work Order)
| WO | Tugas | Target |
|---|---|---|
| WO-15 | Tentukan metrik evaluasi (akurasi, presisi, recall/sensitivitas, spesifisitas, F1, AUC) dan alasan pemilihannya untuk konteks uji kesehatan (biaya FP vs FN) | Bimbingan 7 |

## 5. Revisi (→ naskah)
- Bab 3 (Rencana Analisis Hasil): subbab metrik evaluasi — definisi, rumus dari *confusion matrix*, dan alasan metrik utama.
- Bab 3: alur training / validation (k-fold 5) / testing seperti dijelaskan pembimbing.

## 6. Jadwal bimbingan berikutnya
- [ISI NANTI] — bawa hasil WO-15.

## 7. Isian SIMASTER (bimbingan ke-2 setelah persetujuan judul) — salin ke form
| Kolom form | Isi |
|---|---|
| Dosen Pembimbing | Nopriadi, S.T., M.Sc. |
| Tanggal | 9 November 2026 |
| Topik Bimbingan | Hasil validasi k-fold cross-validation fitur citra heiDATA dan pemilihan metrik evaluasi |
| Dokumen | `docs/bimbingan/B6_2026-11-09/Bimbingan6_Skripsi_Rahul.pdf` (1,96 MB, di bawah batas 2 MB) |

**Catatan Bimbingan** (teks polos):
```
1. Mahasiswa memaparkan hasil k-fold cross-validation (5 dan 10 fold) untuk klasifikasi sel CD4 dari citra heiDATA dengan fitur Lamin B1 dan kapsid HIV-1: pengujian per sel menghasilkan ROC AUC 0,65-0,80, sedangkan pengujian berkelompok per percobaan turun mendekati acak.
2. Pembimbing menegaskan bahwa klasifikasi dilakukan per sel, serta menjelaskan alur pembagian data training, validation (k-fold cross-validation 5 fold untuk menentukan parameter) dan testing.
3. Pembimbing meminta hasil tidak hanya dilaporkan dengan akurasi, tetapi dengan beberapa metrik (precision, recall, F-score, dll.), dan mahasiswa memilih metrik yang paling sesuai beserta alasannya untuk konteks uji kesehatan (mempertimbangkan false positive dan false negative).
4. Hasil perlu dapat dijelaskan dan dibandingkan dengan penelitian sebelumnya.
5. Surat persetujuan penggantian judul ditandatangani belakangan.
Tindak lanjut: menentukan metrik evaluasi dan alasan pemilihannya (WO-15).
```

## 8. Catatan untuk mahasiswa
- **Catat B6 di SIMASTER** (bimbingan ke-2 setelah persetujuan judul) agar bisa disetujui pembimbing.
- **Per sel vs berkelompok (penting, perlu diluruskan di B7):** pembimbing benar bahwa *unit* klasifikasi adalah sel. Namun pada k-fold per sel,
  sel dari bidang pandang/percobaan yang sama masuk ke data latih dan uji sekaligus, sehingga model bisa mengenali "asal percobaan", bukan
  kondisi sel (efek *batch*). Usul penjelasan: *tetap klasifikasi per sel*, tetapi **pembagian fold per percobaan**; laporkan keduanya.
  Siapkan satu gambar sederhana untuk menjelaskannya.
- Luruskan jumlah fitur: 13 (heiDATA), bukan 17; dan bahwa 0,8 adalah AUC, bukan akurasi.
- Pertanyaan yang belum terbahas (dataset, kelas, opsi judul, koreksi 0,65 → 0,57, ujian, pembimbing pendamping, judul Bab 3) dibawa lagi ke B7.
  Sebaiknya diletakkan di awal presentasi supaya sempat dibahas.
