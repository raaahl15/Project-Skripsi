# Bahan Bimbingan 7 — [tanggal: ISI NANTI]
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**

> Disusun 25 Nov 2026 (berbantuan AI, wajib ditinjau mahasiswa). Folder diganti nama menjadi `B7_<tanggal>` setelah jadwal pasti.
> Prinsip B7: **keputusan yang dibutuhkan ditaruh di awal** (B6 hanya sempat membahas k-fold heiDATA).
> Slide (13, gaya UGM seperti B5–B6): https://claude.ai/artifact/36C74VKWiKGgrMGVVY4xdZ · sumber di slides/project/.

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 7 (SIMASTER: ke-4 setelah persetujuan judul [cek penomoran]) |
| Tanggal | [ISI NANTI] |
| Tercatat di SIMASTER | [ ] |

## 0. Keputusan yang diminta (urut prioritas)
| # | Pertanyaan | Usulan mahasiswa | Dasar |
|---|---|---|---|
| 1 | **Dataset**: Skenario 1 (heiDATA + Essig), Skenario 2 (Illinois + Essig), atau keduanya? | Keduanya sudah dikerjakan; bila harus memilih satu, Skenario 1 (paling sesuai judul: sel T CD4 primer + virus HIV-1 utuh) | §2 |
| 2 | **Kelas**: (Sk1) terpapar HIV-1 vs Mock; (Sk2) ekspresi HIV aktif / laten / ditekan; (Essig) hidup vs mati — diterima? | Ya; kelas Sk2 menggeser arti "terinfeksi vs tidak" menjadi "keadaan ekspresi HIV" | §2 |
| 3 | **Evaluasi**: unit klasifikasi tetap sel, tetapi lipatan dipisah per percobaan/donor/plate — setuju dilaporkan berdampingan dengan k-fold per sel? | Ya (selisih keduanya = kebocoran efek *batch*) | §3 |
| 4 | **Metrik utama** (WO-15): sensitivitas + spesifisitas, didukung ROC AUC, *balanced accuracy*, MCC | Setuju? | §1 |
| 5 | **Judul**: Opsi 1 (heiDATA + Essig) atau Opsi 3 "… Citra Mikroskopi Optik …" (berlaku semua skenario) | Opsi 3 | Bahan B6 §3 |
| 6 | **Format naskah**: spasi 1,5 (opsi `satusetengahspasi` di template) atau 2? Judul Bab 3 "Pelaksanaan Penelitian" (template) atau "Metodologi Penelitian" (panduan)? | Ikuti template | §4 |
| 7 | **Administrasi**: tanggal ujian & tenggat pendaftaran; pembimbing pendamping & NIP | — | — |

Laporan singkat (tidak perlu keputusan): koreksi hasil B5 (AUC 0,65 → 0,57, bug normalisasi kapsid); email ke Heidelberg sudah dikirim
(tidak ada balasan).

## 1. Laporan Work Order dari Bimbingan 6
| WO | Tugas | Status | Ringkasan eksekusi / bukti |
|---|---|---|---|
| WO-15 | Pilih metrik evaluasi + alasan (FP vs FN) | ✅ draf | 11 metrik + *confusion matrix* untuk semua tugas → `results/wo15-metrics/`; materi & usulan → `docs/materi/WO-15-metrik-evaluasi.md` |
| WO-14 | Arti fisis & rumus fitur | 🔄 | Tabel rumus 13 + 19 + 9 fitur; pustaka pendukung sudah dicari (DAFTAR-REFERENSI) |
| — | Catatan B6 di SIMASTER | ✅ | Dicatat pengguna |

**Temuan WO-15 (alasan memilih metrik):** pada fitur Lamin B1 (kelas timpang 170 : 39), F1 0,72–0,77 tampak "baik" padahal ROC AUC
0,27–0,46, MCC negatif, dan spesifisitas 0 (semua Mock diprediksi HIV). Sensitivitas–spesifisitas dan MCC langsung memperlihatkan
kegagalan ini → dipilih sebagai metrik utama/pendukung; F1 dan akurasi tidak.

## 2. Dua skenario dataset (rincian: `docs/materi/SKENARIO-DATASET-B7.md`)
| | Skenario 1: heiDATA + Essig | Skenario 2: Illinois + Essig |
|---|---|---|
| Bagian HIV: sel | Sel T CD4 primer, virus HIV-1 utuh | Jurkat (lini sel T CD4+), sirkuit gen HIV dengan reporter GFP |
| Kelas | Terpapar HIV-1 vs Mock | Ekspresi aktif (TNF) vs laten; ditekan (Alp) vs laten |
| Data | 100 sel, 2 percobaan | ±6.200 sel, 7 plate (fitur penulis) + citra sendiri Plate 2 |
| Hasil lintas kelompok | Kapsid: AUC 0,91, spesifisitas 1,00, recall 0,80, MCC 0,81 | Aktif vs laten: AUC 0,87, MCC 0,56; ditekan vs laten: AUC 0,95, MCC 0,75 |
| Kebocoran *batch* | Ada (fitur Lamin B1: per sel 0,79 → per percobaan 0,27–0,46) | Tidak ada (selisih ≤ 0,01) |
| Bagian Essig (hidup vs mati) | Latih exp1 → uji exp2: AUC 0,98–1,00; 4 donor (LODO): 0,95–0,96 | sama |

**Progres setelah keputusan mengerjakan kedua skenario (25 Nov):**
- Illinois — **ekstraksi citra sendiri** pada 4 sumur kontrol Plate 2 (A23 laten, A24 Alp, B01 TNF, B02 laten) dari potongan arsip
  `.zip.003` (10 GB, bukan seluruh plate 356 GB): **1.185 sel**. Model dilatih dengan fitur penulis dari 6 plate lain lalu diuji pada fitur
  ekstraksi sendiri Plate 2 (plate baru + ekstraksi baru): aktif vs laten AUC 0,86–0,89, ditekan vs laten 0,90–0,92; AUC per fitur
  sendiri vs penulis berkorelasi 0,97. Keterbatasan: 1 sumur per kelas positif (`results/skenario-b7/illinois-own/README.md`).
- Essig — **percobaan 2** (480.001 citra sel, donor 3–4; label ahli hidup 137 / mati 79): model *brightfield* dilatih di exp1, diuji di
  exp2 (percobaan + donor baru): **AUC 0,98–1,00**, recall 0,94–0,98, spesifisitas 0,97–0,99, MCC 0,91–0,96; leave-one-donor-out
  (4 donor) AUC 0,95–0,96 (`results/essig-exps/README.md`).

## 3. Pelurusan: per sel vs berkelompok (dari B6)
Pembimbing di B6: "klasifikasi per sel, evaluasi baku per sel". Usulan pelurusan: **unit yang diklasifikasikan tetap sel**; yang dipisah
per kelompok hanya **pembagian lipatan** (sel dari satu percobaan/donor/plate tidak boleh sekaligus ada di data latih dan uji).
Alasan: sel dari bidang pandang/percobaan yang sama berbagi kondisi pengambilan citra (pewarnaan, fokus, intensitas laser), sehingga
model bisa mengenali percobaan, bukan kondisi sel. Bukti: heiDATA Lamin B1 AUC 0,79 (per sel) → 0,27–0,46 (per percobaan, tiga model); sebaliknya
Illinois dan Essig hampir sama di kedua skema (sinyal nyata). Gambar: `results/b7/split_schemes.png` (A: skema pembagian; B: ROC AUC kedua skema untuk 5 tugas, model terbaik; skrip `src/b7_figures.py`).

## 4. Naskah
- Google Docs naskah digabung: **1 dokumen, 6 tab** (Bab I–V + Skripsi Final), format mengikuti `skripsidtntf.cls`
  (A4, Times New Roman 12, margin template, BAB tengah tebal, penomoran I.1.).
- **Bab I**: draf lengkap (latar belakang, perumusan masalah + batasan, tujuan, manfaat) dengan sitasi; masih: data HIV Indonesia, celah penelitian.
- **Bab II**: kerangka 7 subbab dasar teori + tinjauan pustaka (Grad-CAM dihapus karena tidak lagi *deep learning*).
- **Bab III**: kerangka alat & bahan, tata laksana (segmentasi, fitur, model, validasi), rencana analisis.
- **Pustaka**: 63 kandidat, DOI terverifikasi (Crossref/DataCite), sedang dibaca → `docs/literatur/DAFTAR-REFERENSI.md`.
- Perkiraan panjang: ±80–120 halaman (spasi 1,5).

## 5. Rencana sampai ujian [disesuaikan dengan tanggal ujian]
| Minggu | Target |
|---|---|
| 26 Nov – 2 Des | B7; hasil final kedua skenario (Essig exp2–4, Illinois sumur kontrol); Bab I direvisi |
| 3 – 9 Des | Bab II dan III menjadi naskah; Bab IV (hasil) mulai |
| 10 – 16 Des | Bab IV pembahasan, Bab V, intisari/*abstract*; konversi LaTeX; revisi pembimbing |
| 17 Des – … | Pendaftaran & ujian [ISI NANTI] |

## 6. Isian SIMASTER (draf sebelum bimbingan) — **DIGANTIKAN** oleh `HASIL.md` §7 (berdasarkan rekaman B7)
> Satu paragraf (permintaan pengguna 26 Nov): isi = yang dipaparkan mahasiswa dari bahan ini; tidak memuat arahan pembimbing
> karena belum ada catatan hasil B7. Nomor di SIMASTER mengikuti urutan pengisian
> (B5 = 1, B6 = 2, B1 = 3, B2 = 4 → B7 = 5).

| Kolom form | Isi |
|---|---|
| Dosen Pembimbing | Nopriadi, S.T., M.Sc. |
| Tanggal | [tanggal pertemuan B7] |
| Topik Bimbingan | Pemilihan metrik evaluasi, validasi per sel vs berkelompok, dan penetapan skenario dataset |
| Dokumen | PDF slide B7 — unduh dari artifact slide (menu unduh → PDF), pastikan ≤ 2 MB; simpan di folder B7 |

**Catatan Bimbingan** (teks polos):
```
Mahasiswa melaporkan hasil WO-15 tentang pemilihan metrik evaluasi: sebelas metrik beserta confusion matrix dihitung untuk semua tugas klasifikasi, dan diusulkan sensitivitas serta spesifisitas sebagai metrik utama dengan ROC AUC, balanced accuracy, dan MCC sebagai pendukung, karena pada data dengan kelas timpang (fitur Lamin B1, 170:39) nilai F1 0,72-0,77 tampak baik padahal spesifisitasnya 0 dan MCC negatif. Mahasiswa juga menjelaskan bahwa unit klasifikasi tetap per sel, tetapi pembagian data latih dan uji perlu dipisah per percobaan, donor, atau plate agar tidak terjadi kebocoran efek batch; pada heiDATA fitur Lamin B1 AUC turun dari 0,79 (per sel) menjadi 0,27-0,46 (per percobaan), sedangkan pada dataset Illinois dan Essig hasil kedua skema hampir sama. Selanjutnya dipaparkan dua skenario dataset, yaitu Skenario 1 (heiDATA + Essig) dengan fitur kapsid HIV-1 vs Mock mencapai AUC 0,91 dan MCC 0,81 lintas percobaan, serta Skenario 2 (Illinois + Essig) dengan ekspresi HIV aktif vs laten AUC 0,87 dan ditekan vs laten AUC 0,95, yang juga diuji pada 1.185 sel hasil ekstraksi citra sendiri (AUC 0,86-0,92); klasifikasi hidup vs mati pada data Essig yang dilatih pada percobaan 1 dan diuji pada percobaan 2 dengan donor baru mencapai AUC 0,98-1,00. Mahasiswa juga melaporkan progres naskah (Bab I draf, Bab II dan III kerangka, 63 pustaka terverifikasi), usulan judul, dan rencana pengerjaan sampai ujian. Tindak lanjutnya adalah menetapkan skenario dataset yang digunakan, menyelesaikan hasil akhir, dan menulis Bab II dan III menjadi naskah.
```
