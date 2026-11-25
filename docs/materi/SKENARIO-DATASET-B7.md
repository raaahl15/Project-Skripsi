# Dua Skenario Dataset untuk Bimbingan 7
*Disusun 25 Nov 2026 (draf berbantuan AI, wajib ditinjau mahasiswa). Semua angka berasal dari analisis di repo ini;
pustaka yang ditandai [perlu pustaka] belum diverifikasi.*

Kedua skenario memakai **Essig (sel T CD4 hidup vs mati)** sebagai Bagian B. Perbedaannya ada di **Bagian A (bagian HIV)**:
- **Skenario 1 — heiDATA + Essig:** sel T CD4 primer yang terpapar virus HIV-1 utuh vs Mock.
- **Skenario 2 — Illinois + Essig:** sel Jurkat dengan sirkuit gen HIV (reporter GFP), ekspresi HIV aktif / laten / ditekan.

Kedua bagian **tidak digabung dalam satu model**. Alat, objek, kanal, dan label berbeda, sehingga fitur tidak bisa dimasukkan ke satu
tabel. Penyatunya adalah pertanyaan ("kondisi sel T CD4 pada infeksi HIV"), pipeline yang sama (citra → segmentasi → fitur fisis →
ML klasik → validasi berkelompok → metrik WO-15), dan kerangka fisika kontras optik.

## 1. Perbandingan ringkas
| | **Skenario 1: heiDATA + Essig** | **Skenario 2: Illinois + Essig** |
|---|---|---|
| Bagian A: data | Ananth dkk. 2024 (heiDATA), mikroskop fluoresens 3D | Lu dkk. 2021 (*PNAS*), mikroskop fluoresens *time-lapse* 48 jam |
| Bagian A: sel | Sel T CD4 **primer** istirahat | **Jurkat** (lini sel T CD4+, bukan sel primer) |
| Bagian A: HIV | **Virus HIV-1 utuh** (kapsid terlihat) | Sirkuit gen HIV minimal (promotor LTR + reporter GFP), bukan virus |
| Bagian A: kelas | Terpapar HIV-1 vs Mock | Ekspresi HIV aktif (TNF-α) vs laten; ditekan (alsterpaullone) vs laten |
| Bagian A: ukuran data | **100 sel, 2 percobaan** yang memuat Mock (209 sel untuk Lamin B1) | ±8.000 sel kontrol (dibatasi 20/sumur), 413 sumur, **7 plate** |
| Bagian A: fitur | Bentuk & intensitas inti (Lamin B1), jumlah titik kapsid | Dinamika intensitas GFP per sel: rerata, kemiringan, CV, rasio akhir/awal, autokorelasi |
| Bagian A: ekstraksi citra | **Sendiri, dari citra mentah** (semua sel) | Fitur dari ekstraksi peneliti (NIS Elements); ekstraksi sendiri baru teruji di 1 sumur demo (r = 0,985 vs penulis) |
| Bagian A: hasil lintas kelompok | Kapsid: AUC 0,91, spesifisitas 1,00, recall 0,80, MCC 0,81 | Aktif vs laten: AUC 0,87, recall 0,83, spesifisitas 0,76, MCC 0,56; ditekan vs laten: AUC 0,95, MCC 0,75 |
| Bagian A: kebocoran *batch* | Ada pada fitur Lamin B1 (k-fold 0,79 → per percobaan 0,27) | Tidak ada (selisih ≤ 0,01) |
| Bagian A: risiko utama | Data sangat kecil → hasil rapuh, mudah dipertanyakan | Bukan sel primer & bukan virus; perlu ekstraksi citra sumur kontrol (arsip besar → Colab) |
| Bagian B | Essig: hidup vs mati, AUC 0,91–0,94 pada donor baru | sama |
| Kecocokan judul Simaster | Tinggi (sel T CD4 primer + HIV-1 utuh) | Sedang (perlu penjelasan Jurkat & reporter di Bab 1/3) |
| Sisa pekerjaan sampai naskah | Kecil: pipeline sudah lengkap | Sedang–besar: ekstraksi citra sumur kontrol bila disyaratkan "dari citra sendiri" |

## 2. Skenario 1 — heiDATA + Essig
**Judul (Opsi 1 B6):** *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Mikroskop Fluoresensi dan Imaging Flow Cytometry
Menggunakan Machine Learning* (atau Opsi 3 "Citra Mikroskopi Optik").

**Rumusan masalah**
1. Fitur fisis apa dari citra fluoresensi yang membedakan sel T CD4 terpapar HIV-1 dari sel tanpa paparan (Mock)?
2. Fitur fisis apa dari citra *brightfield* IFC yang membedakan sel T CD4 hidup dan mati?
3. Seberapa baik model ML klasik (LogReg, RF, SVM) mengklasifikasikan kedua kondisi tersebut bila diuji pada percobaan/donor yang tidak
   ikut dilatih?

**Kerangka fisika:** A = kontras **fluoresensi** (emisi penanda spesifik molekul; deteksi titik kapsid ditentukan rasio sinyal-derau);
B = kontras **brightfield** *label-free* (serapan dan pembiasan cahaya; membran sel mati kehilangan kontras refraktif → gradien RMS turun).

### 2.1 Hasil (metrik WO-15, ambang bawaan, model dengan MCC tertinggi)
| Bagian | Skema validasi | Model | Bal. acc | Recall (sensitivitas) | Spesifisitas | MCC | ROC AUC |
|---|---|---|---|---|---|---|---|
| A HIV vs Mock (kapsid, n = 100) | per percobaan (2) | RF | 0,900 | 0,800 | 1,000 | 0,809 | 0,906 |
| A HIV vs Mock (kapsid) | k-fold 5 per sel | RF | 0,876 | 0,751 | 1,000 | 0,746 | 0,876 |
| A HIV vs Mock (Lamin B1, n = 209) | per percobaan | RF | 0,482 | 0,758 | 0,000 | −0,090 | 0,274 |
| B mati vs hidup (BF, n = 702) | per donor (2) | RF | 0,873 | 0,845 | 0,902 | 0,758 | 0,935 |
| B mati vs hidup (BF) | k-fold 5 per sel | RF | 0,897 | 0,874 | 0,921 | 0,799 | 0,961 |

Sumber: `results/wo15-metrics/`. Uji ketahanan kapsid (28 pengaturan detektor): AUC 0,86–0,97. Essig: permutasi p = 0,005.

### 2.2 Kekuatan dan kelemahan
- ➕ Paling sesuai judul: sel T CD4 primer, virus HIV-1 utuh, semua fitur diekstrak sendiri dari citra mentah.
- ➕ Pipeline dan validasi sudah lengkap; sisa waktu bisa dipakai untuk menulis naskah.
- ➖ heiDATA hanya 2 percobaan dengan Mock (100 sel) → interval kepercayaan lebar; hasil "kapsid membedakan HIV vs Mock" sebagian
  bersifat trivial (Mock memang tanpa virus). Nilai ilmiahnya ada pada **batas deteksi optik** (recall maksimal ±0,75 tanpa salah
  alarm karena kapsid redup di bawah ambang).
- ➖ Fitur bentuk inti (Lamin B1) gagal lintas percobaan → dilaporkan sebagai temuan efek *batch*, bukan hasil utama.

### 2.3 Sisa pekerjaan
1. (Opsional) Essig exp2–4 untuk validasi lintas percobaan dan lebih banyak donor (±125 GB, per percobaan atau Colab).
2. Gambar/tabel final dan penulisan Bab 3–4.

## 3. Skenario 2 — Illinois + Essig
**Judul (usulan):** *Klasifikasi Kondisi Sel T CD4 pada Infeksi HIV Berdasarkan Citra Mikroskopi Optik Menggunakan Machine Learning*
(Opsi 3; Opsi 2 B6 hanya menyebut *time-lapse*, tidak mencakup IFC Essig).

**Rumusan masalah**
1. Fitur dinamika fluoresensi per sel apa (rerata, laju perubahan, fluktuasi/*noise* ekspresi) yang membedakan keadaan ekspresi HIV
   aktif, laten, dan ditekan pada sel T?
2. Fitur fisis apa dari citra *brightfield* IFC yang membedakan sel T CD4 hidup dan mati?
3. Seberapa baik model ML klasik mengklasifikasikan kondisi tersebut bila diuji pada plate/donor yang tidak ikut dilatih?

**Kerangka fisika:** A = **fluoresensi GFP sebagai fungsi waktu** (intensitas ∝ jumlah protein reporter; fluktuasi = *noise* ekspresi
gen stokastik, besaran fisis-statistik); B = kontras brightfield *label-free* (sama dengan Skenario 1). Kedua bagian sama-sama optik
dan *bio-optik*; A menekankan analisis deret waktu dan statistik sinyal, B analisis citra statis.

### 3.1 Kaitan dengan HIV
Kelas Illinois tidak berarti "terinfeksi vs tidak": semua sel membawa sirkuit HIV. Yang diklasifikasikan adalah **keadaan ekspresi**
HIV: laten (reservoir), teraktivasi (TNF-α, analog strategi *shock-and-kill*), atau ditekan (*block-and-lock*) [perlu pustaka].
Ini relevan klinis (reservoir laten = alasan HIV belum bisa disembuhkan) tetapi **menggeser arah B5 ("terinfeksi vs tidak")**,
sehingga perlu persetujuan pembimbing.

### 3.2 Hasil sebelumnya (pilot 8 Nov, ROC AUC, LogReg/RF/SVM)
| Tugas | k-fold 5 per sel | Per sumur | Leave-one-plate-out |
|---|---|---|---|
| TNF vs tanpa perlakuan | 0,85–0,88 | 0,85–0,88 | 0,85–0,87 |
| Alsterpaullone vs tanpa perlakuan | 0,93–0,95 | 0,93–0,95 | 0,93–0,95 |

Skor hampir sama di semua skema → tidak ada kebocoran efek *batch*. Lintasan *noise* bawaan penulis bocor (AUC 1,00) dan tidak dipakai.

### 3.3 Hasil dengan metrik WO-15 (25 Nov)
Protokol sama dengan WO-15 (GridSearch 3-fold di data latih, fold luar = uji). Kelas positif = kondisi yang berubah dari laten.
n = 6.220 sel (TNF 2.100 vs laten 4.120) dan 6.159 sel (Alp 2.039 vs laten 4.120). Model dengan MCC tertinggi per baris.

| Tugas | Skema | Ambang | Model | Bal. acc | Recall | Spesifisitas | MCC | ROC AUC |
|---|---|---|---|---|---|---|---|---|
| Aktif (TNF) vs laten | plate baru (7) | bawaan | SVM | 0,795 | 0,827 | 0,762 | 0,563 | 0,874 |
| Aktif (TNF) vs laten | plate baru (7) | recall ≥ 0,90 | SVM | 0,787 | 0,895 | 0,679 | 0,544 | 0,874 |
| Aktif (TNF) vs laten | k-fold 5 per sel | bawaan | SVM | 0,804 | 0,844 | 0,765 | 0,579 | 0,882 |
| Ditekan (Alp) vs laten | plate baru (7) | bawaan | RF | 0,876 | 0,840 | 0,912 | 0,750 | 0,950 |
| Ditekan (Alp) vs laten | plate baru (7) | recall ≥ 0,90 | SVM | 0,877 | 0,900 | 0,853 | 0,726 | 0,950 |
| Ditekan (Alp) vs laten | k-fold 5 per sel | bawaan | RF | 0,885 | 0,850 | 0,920 | 0,768 | 0,951 |

Semua model: `results/skenario-b7/illinois-metrics/summary_metrics.csv`; CM: `confusion_matrices.png`.

**Temuan:**
1. Plate baru vs k-fold per sel berselisih ≤ 0,01 di semua metrik → **tidak ada kebocoran *batch***. Bandingkan heiDATA Lamin B1
   (k-fold 0,79 → per percobaan 0,27).
2. Ambang recall ≥ 0,90 yang dipilih di data latih **tercapai di data uji** (0,89–0,90), dengan spesifisitas turun ±0,08–0,10:
   pertukaran FN ↔ FP yang stabil karena data besar. Pada heiDATA kapsid ambang ini runtuh (spesifisitas 0) karena banyak skor seri.
3. Aktif vs laten lebih sulit (MCC ±0,56) daripada ditekan vs laten (±0,75): tidak semua sel merespons TNF (heterogenitas ekspresi),
   sedangkan penekanan menurunkan GFP hampir di semua sel.
4. LogReg selalu terendah (AUC 0,85 / 0,93) → hubungan fitur–kelas sedikit nonlinear; RF dan SVM setara.

### 3.4 Kekuatan dan kelemahan
- ➕ Data jauh lebih besar dan validasi plate baru kuat; hasil stabil tanpa kebocoran.
- ➕ Sisi fisika jelas (dinamika & *noise* intensitas fluoresensi).
- ➖ Jurkat (lini sel leukemia T), bukan sel T CD4 primer; reporter GFP, bukan virus utuh → harus dijelaskan di Bab 1/3.
- ➖ Fitur di §3.2–3.3 dihitung dari lintasan hasil ekstraksi **peneliti**, bukan citra sendiri. Ekstraksi sendiri baru teruji pada
  1 sumur demo (senyawa, bukan kontrol). Untuk "dari citra sendiri", perlu citra sumur kontrol dari arsip citra plate (271–585 GB per plate,
  bagian 10 GB; cukup 2–3 bagian, lihat §4b). Arsip `SingleCellData` 18,8 GB hanya tabel per bingkai dari NIS Elements, bukan citra.
- ➖ Kelas berubah dari "terinfeksi vs tidak" (arahan B5).

### 3.5 Sisa pekerjaan
1. Unduh 2–3 bagian arsip citra satu plate yang memuat sumur kontrol → ekstraksi citra dengan `src/illinois_extract_demo.py`.
2. Ulangi klasifikasi dengan fitur ekstraksi sendiri; bandingkan dengan fitur penulis.
3. Gambar/tabel final dan penulisan Bab 3–4 (termasuk penjelasan Jurkat & sirkuit gen).

## 4. Rekomendasi
Dengan sisa ±3 minggu sebelum periode ujian (perkiraan pertengahan–akhir Desember), **Skenario 1 (heiDATA + Essig)** paling aman:
semua fitur sudah diekstrak sendiri, pipeline lengkap, dan paling sesuai judul serta arahan B5. Skenario 2 lebih kuat secara statistik,
tetapi menambah ekstraksi citra besar dan mengubah definisi kelas. Bila pembimbing menilai heiDATA terlalu kecil, Skenario 2 bisa
dipakai **dengan syarat** fitur dari ekstraksi penulis diterima (atau ekstraksi sendiri cukup pada sebagian plate).

## 4b. Keputusan mahasiswa (25 Nov): kedua skenario dikerjakan
Rencana kerja (data harus diunduh pengguna lewat browser: Dryad meminta login untuk unduhan (HTTP 401), Illinois Data Bank menolak akses
otomatis (HTTP 403)).

| # | Pekerjaan | Untuk | Data | Status |
|---|---|---|---|---|
| 1 | Essig exp2 (20,2 GB): cek label ahli/Live-Dead → fitur BF → uji lintas percobaan (latih exp1, uji exp2) | Kedua skenario | `exp2.zip` | ⏳ menunggu unduhan |
| 2 | Essig exp3 (38,2 GB) & exp4 (39,8 GB), satu per satu, zip dihapus setelah fitur disimpan | Kedua skenario | `exp3.zip`, `exp4.zip` | ⏳ |
| 3 | Illinois: ekstraksi citra sendiri pada sumur kontrol (`src/illinois_extract_demo.py`) | Skenario 2 | 2–3 bagian arsip citra satu plate (±10 GB/bagian) | ⏳ perlu daftar file bagian arsip |
| 4 | Illinois: klasifikasi dengan fitur ekstraksi sendiri, dibandingkan dengan fitur penulis | Skenario 2 | hasil #3 | ⏳ |

**Dasar pemilihan bagian arsip Illinois (hipotesis, perlu dicek):** file demo `WellK16_Seq0255.nd2` cocok dengan urutan akuisisi per baris
`Seq = indeks_baris × 24 + (kolom − 1)` (K = baris ke-10 dari 0 → 10 × 24 + 15 = 255). Bila benar, sumur 23–24 baris *r* dan 1–2 baris *r*+1
berurutan, sehingga **setiap blok 4 sumur berurutan berisi ketiga kelas** (tanpa perlakuan, Alp, TNF, tanpa perlakuan). Dua–tiga bagian
arsip yang memuat blok seperti ini (±12 sumur, ±400 sel per sumur, ±17 menit ekstraksi per sumur) cukup untuk klasifikasi per sumur.
Risiko: bila arsip berupa *split zip*, satu bagian tidak bisa dibuka biasa → perlu membaca *local header* per file.

**Pilihan bagian (25 Nov, dari daftar file Data Bank):** Plate 2 (`images_DiversitySet3Plate2.zip.001–.036`, 355,6 GB → ±0,93 GB per sumur,
±10,8 sumur per bagian; plate yang sama dengan sumur demo K16). Perkiraan posisi blok kontrol bila sumur tersimpan berurutan A01, A02, …:
blok A23–B02 ±20,4–24,1 GB → **`.003`**; blok B23–C02 ±42,6–46,3 GB → **`.005`**; blok C23–D02 ±64,8–68,5 GB → `.007` (cadangan).
Unduh `.003` dulu → isi dipindai (nama sumur per *local header*) → perkiraan dikoreksi sebelum mengunduh `.005`/`.007`.

**Perintah setelah unduhan selesai** (unduh ke D:, bukan C:; C: sempat penuh 25 Nov):
```
# Essig (per percobaan; ±beberapa jam, bisa dilanjutkan bila terputus)
.venv\Scripts\python.exe -I src\essig_exp_features.py --zip data\raw\dryad-essig-2022\exp2.zip --exp exp2
.venv\Scripts\python.exe -I src\essig_cross_exp.py          # latih exp1 -> uji exp2..; LOEO; LODO; metrik WO-15
# Illinois
.venv\Scripts\python.exe -I src\illinois_zip_parts.py list    data\raw\illinois-IDB-8103861\images_DiversitySet3Plate2.zip.003
.venv\Scripts\python.exe -I src\illinois_zip_parts.py process data\raw\illinois-IDB-8103861\images_DiversitySet3Plate2.zip.003
.venv\Scripts\python.exe -I src\wo15_metrics.py --config configs\illinois_own_metrics.yaml
```
Diuji 25 Nov: Essig dengan zip tiruan (struktur h5 sama); pembaca potongan zip dengan zip tiruan yang dipotong 3 (MD5 cocok) dan
zip demo asli; `process` pada sumur demo K16.

## 5. Pertanyaan untuk pembimbing (B7)
1. Skenario mana yang dipilih: 1 (heiDATA + Essig) atau 2 (Illinois + Essig)?
2. Bolehkah Essig (tanpa HIV, dikaitkan lewat pustaka kematian sel CD4 pada infeksi HIV) menjadi Bagian B?
3. Bila Skenario 2: apakah kelas "ekspresi HIV aktif/laten/ditekan" diterima sebagai pengganti "terinfeksi vs tidak"? Apakah fitur dari
   ekstraksi citra peneliti boleh dipakai, atau wajib ekstraksi sendiri?
4. Judul: Opsi 1 (Skenario 1) atau Opsi 3 (berlaku untuk keduanya)?
