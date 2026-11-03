# WO-03 — Perbedaan Skripsi Ini dengan Teknik Biomedis dan Teknologi Informasi
> Draf disusun dengan bantuan AI (2026-11-03) untuk dipelajari & disesuaikan mahasiswa. Arahan asal: bimbingan 2 (4 Sep 2026).

## Jawaban singkat (±30 detik, untuk disampaikan lisan)
Skripsi ini memandang sel sebagai **objek optik** dan citra sel sebagai **hasil pengukuran instrumen optik**. Yang diteliti adalah
**besaran fisis/bio-optik apa** (ukuran, bentuk, distribusi intensitas fluoresensi, tekstur, lokasi sinyal) yang membedakan sel CD4
normal, terinfeksi, dan mati, serta bagaimana besaran itu diekstraksi dan dianalisis secara kuantitatif. *Machine learning* dipakai
sebagai alat untuk menguji dan memeringkat fitur fisis tersebut — bukan tujuan akhir. Itulah ciri Teknik Fisika: penerapan prinsip
fisika (optika, pengukuran, pengolahan sinyal/citra) untuk menyelesaikan masalah rekayasa — sesuai bidang di Simaster:
**Instrumentasi (Implementasi Kecerdasan Buatan)** dan **Multifisika (Implementasi Sistem Optika)**.

## Perbandingan
| Aspek | **Teknik Fisika (skripsi ini)** | Teknik Biomedis | Teknologi Informasi / Ilmu Komputer |
|---|---|---|---|
| Pertanyaan utama | Karakteristik fisik/bio-optik apa yang membedakan kondisi sel, dan bagaimana mengukurnya? | Bagaimana membuat alat/metode yang berguna secara klinis bagi pasien? | Algoritma/arsitektur apa yang memberi kinerja (akurasi, kecepatan) terbaik? |
| Cara memandang citra | Hasil pengukuran sistem optik: fluoresensi (eksitasi–emisi), resolusi, *noise*, *z-stack*, kanal spektral | Data diagnostik untuk keputusan klinis | Data masukan untuk model |
| Fokus analisis | **Ekstraksi fitur bermakna fisis** (morfometri, intensitas, tekstur, lokalisasi) + interpretasi fisis | Validasi klinis, keamanan, regulasi, fisiologi | Rekayasa model, optimasi, skala komputasi |
| Peran *machine learning* | Alat untuk menguji & memeringkat fitur (mis. *feature importance*/SHAP) | Komponen sistem diagnosis | Inti kontribusi |
| Ukuran keberhasilan | Fitur pembeda yang dapat dijelaskan secara fisis/biologis + kinerja yang tervalidasi jujur | Manfaat klinis, akurasi diagnostik pada pasien | Metrik kinerja model |
| Kaitan CPMK | CPMK 3: penerapan matematika, sains (optika), dan rekayasa | — | — |

## Contoh konkret di skripsi ini
- **Lamin B1** (kanal fluoresens 405 nm) → batas selubung inti → fitur morfometri inti (luas, sirkularitas, sumbu mayor/minor)
  dan rasio intensitas tepi/tengah inti.
- **Kapsid HIV-1 (CA)** → titik fluoresens kecil (mendekati batas resolusi optik) → jumlah dan lokasi titik relatif terhadap batas inti.
- Interpretasi fisis: perubahan bentuk inti/lamina dan lokasi kapsid sebagai penanda kondisi sel; keterbatasan pengukuran
  (resolusi, *z-stack*, efek *batch* antar-percobaan) dibahas sebagai bagian analisis instrumen.

## Kemungkinan pertanyaan lanjutan dari pembimbing/penguji
1. "Kalau fokusnya fitur, kenapa perlu *machine learning*?" → untuk menguji apakah gabungan fitur benar-benar membedakan kondisi
   pada data baru (validasi) dan memeringkat kontribusi tiap fitur secara objektif.
2. "Apa unsur optikanya?" → pembentukan citra fluoresens (eksitasi/emisi, fluorofor per kanal), resolusi & *z-stack*, ekstraksi
   besaran dari distribusi intensitas.
3. "Bedanya dengan *deep learning*?" → *deep learning* belajar fitur sendiri yang sulit ditafsirkan; skripsi ini menekankan fitur
   yang terdefinisi dan bermakna fisis (arahan bimbingan 3).
