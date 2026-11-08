# Bahan Bimbingan 6 — Senin, 9 November 2026
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.** · bersama Luna

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 6 |
| Tanggal | Senin, 9 November 2026 |
| Tercatat di SIMASTER | [ ] |

## 1. Laporan Work Order dari Bimbingan 5
| WO | Tugas | Status | Ringkasan eksekusi / bukti |
|---|---|---|---|
| WO-14 | Arti fisis & rumus fitur | 🔄 draf lengkap | Rumus, satuan, arti fisis: 13 fitur heiDATA, 19 fitur *brightfield* Essig, 9 fitur deret waktu Illinois + perbandingan & latihan; beberapa pernyataan masih [perlu pustaka] → `docs/materi/WO-14-fitur-heidata.md` |
| WO-14 | Validasi k-fold (training/validation/testing) | ✅ | LogReg, RF, SVM; hiperparameter dipilih di data latih (3-fold), diuji di fold luar → `results/wo14-kfold/` |
| WO-14 | Prosedur ganti judul | ✅ | Perlu surat persetujuan dosen pembimbing; surat sudah disiapkan |
| WO-12 | Email permintaan citra ke Heidelberg | 🔄 | Sudah dikirim; balasan tidak diharapkan → rencana tidak bergantung pada data tambahan |

### Hasil k-fold heiDATA (ROC AUC; 0,5 = acak; rentang = tiga model)
| Tugas | k-fold 5 / 10 per sel | k-fold berkelompok per percobaan |
|---|---|---|
| Terpapar HIV vs Mock | 0,74–0,80 | 0,27–0,46 |
| +Vpx vs −Vpx (Lamin B1) | 0,66–0,72 | 0,52–0,58 |
| +Vpx vs −Vpx (Lamin B1 + kapsid, setelah perbaikan) | 0,66–0,79 | 0,46–0,53 |

Selisih kedua skema = **kebocoran efek *batch***: pada k-fold per sel, sel dari percobaan yang sama ada di data latih dan uji, sehingga
model mengenali percobaan, bukan kondisi sel. Dengan heiDATA saja (14 bidang pandang), hasil lintas percobaan masih setara acak.

## 2. Usulan utama: heiDATA + Essig (alternatif teruji: Illinois)
| Bagian | Data | Jenis citra | Klasifikasi | Hasil lintas kelompok (setelah validasi lengkap) |
|---|---|---|---|---|
| A | heiDATA (Ananth dkk., 2024) | Mikroskop fluoresensi (Lamin B1, kapsid HIV-1) | **Sel terpapar HIV-1 vs Mock** | Kapsid: AUC **0,91** lintas percobaan (p = 0,01; 28 variasi detektor 0,86–0,97) |
| B | Essig dkk. (Dryad 2022) | Imaging flow cytometry (brightfield) | **Sel T CD4 hidup vs mati** | AUC **0,91–0,95** pada donor baru (p = 0,005; mask sendiri 0,92–0,95) |

**Alasan memilih heiDATA + Essig (bukan Illinois) sebagai usulan utama:** paling sesuai judul Simaster (sel T CD4 primer, virus HIV-1
utuh, data citra); seluruh pipeline dari citra mentah sudah berjalan dan tervalidasi; risiko waktu paling kecil untuk tenggat Desember.
Kelemahan: heiDATA kecil (2 percobaan dengan Mock, 100 sel) → diakui sebagai keterbatasan; Essig melengkapi dengan data besar.

### Integrasi dua dataset — disatukan oleh pertanyaan, metode, dan fisika; tidak digabung dalam satu model
Alat, objek yang dicitrakan (inti vs sel utuh), kanal, resolusi, dan label berbeda → fitur tidak dapat dimasukkan ke satu tabel.
1. **Pertanyaan biologis:** kondisi sel T CD4 pada infeksi HIV-1 = (A) apakah sel terpapar/terinfeksi, (B) apakah sel masih hidup.
   Kaitan B dengan HIV lewat pustaka: berkurangnya sel T CD4 pada infeksi HIV-1 terutama terjadi melalui kematian sel (apoptosis dan
   piroptosis, termasuk sel *bystander* yang tidak terinfeksi produktif) (Doitsh dkk., 2014; Cummins & Badley, 2010).
   Data Essig sendiri tidak berisi HIV — kaitannya konteks, bukan pengukuran langsung.
2. **Satu pipeline:** citra → pra-pemrosesan → segmentasi → **ekstraksi fitur fisis** → ML klasik (LogReg, RF, SVM; GridSearch 3-fold
   di data latih) → validasi berkelompok (A per percobaan, B per donor) + uji permutasi + uji ketahanan → interpretasi fisis.
3. **Kerangka fisis — dua mekanisme kontras optik:**

   | | A: fluoresensi | B: *brightfield* |
   |---|---|---|
   | Sumber kontras | Emisi penanda fluoresen spesifik molekul | Serapan & pembiasan cahaya oleh sel (tanpa pewarna) |
   | Fitur kunci | Titik kapsid (deteksi LoG; SNR, normalisasi, saturasi) | Gradien RMS, sebaran intensitas, tekstur |
   | Sifat | Spesifik, perlu pewarnaan | *Label-free*, tidak spesifik molekul |
4. **Perbandingan temuan:** heiDATA — selisih besar k-fold per sel vs lintas percobaan (kebocoran *batch*); Essig — selisih kecil
   (sinyal nyata). Pelajaran metodologis: kapan hasil ML citra sel dapat dipercaya.

### Hasil analisis kedua dataset (7 Nov) — rincian: `results/b6/README.md`
**Bagian A — heiDATA, konsistensi efek per percobaan (tanpa ML)**
- Sel +Vpx punya inti **lebih konveks (soliditas, arah sama di 5 dari 5 percobaan, d median 0,59)** dan **lebih bulat (sirkularitas,
  4 dari 5, d 0,54)**. Arah konsisten, efek sedang, tetapi belum signifikan (uji tanda p = 0,06; sampel per percobaan kecil).
- Fitur ukuran & intensitas berubah arah antar-percobaan → sumber efek *batch*.
- **Koreksi atas hasil B5 (kontrol kualitas):** sel Mock (tanpa virus) di 1G terhitung paling banyak titik kapsid. Penyebabnya:
  setiap citra dinormalisasi ke rentangnya sendiri, sehingga derau citra Mock teregang menjadi ribuan titik palsu (8.325 titik).
  Setelah dinormalisasi dengan skala yang sama per percobaan, Mock = 0 titik. Akibatnya hasil B5 "+Vpx vs −Vpx dengan kapsid,
  AUC 0,65, p = 0,01" **menjadi AUC 0,57, p = 0,14 (tidak signifikan)**. Fitur Lamin B1/morfometri tidak terdampak.

**Bagian A2 — heiDATA, terpapar HIV-1 vs Mock dari kapsid terdeteksi optik (latih di satu percobaan, uji di percobaan lain)**
| Fitur | AUC lintas percobaan | *Balanced accuracy* |
|---|---|---|
| Kapsid HIV-1 (jumlah titik di dalam & sekitar inti) | **0,91** (p permutasi = 0,01) | **0,78–0,90** |
| Lamin B1 / bentuk inti | 0,19–0,26 | 0,36–0,48 |

- Sesuai arahan B5 (terinfeksi vs tidak). Mock: 0 titik kapsid pada semua sel; 15 dari 40 sel terpapar di S3B tanpa kapsid di inti.
- **Uji ketahanan:** 28 variasi pengaturan detektor (ambang 0,03–0,20, ukuran titik, lebar cincin, skala intensitas) → AUC tetap
  **0,86–0,97**; ambang 0,08 bukan hasil "memilih yang terbaik". Ambang rendah menangkap kapsid redup tetapi mulai memberi titik palsu
  pada Mock (kompromi sensitivitas–spesifisitas yang diatur rasio sinyal-derau). Rincian: `results/b6/README.md` Bagian A3.
- Keterbatasan: hanya 2 percobaan yang punya Mock (100 sel).

**Bagian B — Essig, sel T CD4 hidup vs mati (brightfield saja, label ahli 354 vs 348 sel)**
| Skema | LogReg | RF | SVM |
|---|---|---|---|
| k-fold 5 per sel | 0,945 | 0,961 | 0,954 |
| Leave-one-donor-out (donor baru) | 0,921 | 0,935 | 0,909 |

- Selisih kedua skema kecil → sinyal berlaku pada donor baru. Fitur utama: **gradien RMS brightfield** (ketajaman tepi/kontras refraktif),
  sebaran intensitas, dan tekstur GLCM.
- **Validasi tambahan (8 Nov):** uji permutasi p = 0,005; IK 95 % AUC donor baru 0,87–0,97; tetap 0,92–0,95 dengan **mask buatan
  sendiri** (tanpa mask dataset) dan saat mask diubah ±1–2 piksel; label ahli sesuai pewarna Live-Dead (AUC 0,99). Galeri sel hidup/mati
  & salah klasifikasi (sel ganda, terpotong, buram): `results/b6/B_gallery_live_dead.png`. Rincian: `results/b6/README.md` Bagian B2.
- **Rencana perluasan (setelah B6):** baru exp1 (donor 1–2) yang diproses. Dataset Essig berisi 4 percobaan dan 9 donor (±125 GB).
  exp2–exp4 dipakai untuk validasi pada lebih banyak donor dan **lintas percobaan** (latih exp1, uji exp2–4). Langkah pertama: cek
  apakah exp2–4 punya label ahli; bila tidak, label dari pewarna Live-Dead (di exp1 sesuai label ahli, AUC 0,99), model tetap
  *brightfield* saja. Diproses per percobaan (unduh → ekstrak fitur → simpan CSV → hapus zip) atau di Colab.

### Alternatif Bagian A: Illinois Data Bank IDB-8103861 (Lu dkk., *PNAS* 2021)
- Sel T Jurkat dengan sirkuit gen HIV minimal (reporter GFP), citra fluoresensi time-lapse 48 jam (1 bingkai / 15 menit), 384 sumur
  per plate, 1.806 senyawa. Kontrol di setiap plate: **TNF-α (aktivasi HIV)**, **tanpa perlakuan (laten)**, **alsterpaullone (penekan)**.
- Kemungkinan klasifikasi: sel HIV **teraktivasi vs laten vs ditekan** dari fitur rerata & ***noise* ekspresi** (fluktuasi stokastik
  intensitas per sel — besaran fisis-statistik), divalidasi berkelompok per sumur/plate (16–32 sumur kontrol per kelas per plate).
- Data yang realistis diunduh: lintasan intensitas (54,8 MB) & *noise* (125 MB) per sel, tabel senyawa (14,5 MB), citra demo 1 sumur
  (1,72 GB). Citra penuh 271–585 GB per plate → tidak realistis; data per frame lengkap 18,8 GB.
- Kekurangan: Jurkat (lini sel, bukan CD4 primer); reporter, bukan virus utuh; kanal kemungkinan hanya GFP; fitur untuk banyak sumur
  berasal dari ekstraksi citra oleh peneliti (NIS Elements), ekstraksi sendiri hanya dari 1 sumur demo.
- **Uji ekstraksi citra sendiri (8 Nov, sumur demo K16):** segmentasi + pelacakan sel dari citra `.nd2` mentah di laptop
  (±17 menit/sumur) → 404 lintasan sel lengkap; rata-rata sumur hampir identik dengan data penulis (**r = 0,985**), fitur relatif
  (CV, rasio akhir/awal) sebanding → **ekstraksi fitur dari citra bisa dilakukan sendiri**. Untuk klasifikasi masih perlu citra sumur
  kontrol (arsip besar → Colab). Rincian: `results/pilot-illinois/demo/README.md`.
- **Pertanyaan:** apakah data ini (berasal dari citra, tetapi diolah sebagai tabel fitur per sel) masih sesuai arahan "data citra"?
  Jika ya, Illinois dapat **menggantikan heiDATA** sebagai bagian HIV (bukan dataset ketiga).

## 3. Opsi judul
Judul Simaster saat ini: *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry Menggunakan Machine Learning*.
Semua opsi hanya mengubah sedikit judul Simaster.

| | Untuk dataset | Judul | Yang berubah | Catatan |
|---|---|---|---|---|
| **Opsi 1** | heiDATA + Essig | *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Mikroskop Fluoresensi dan Imaging Flow Cytometry Menggunakan Machine Learning* | Tambah "Mikroskop Fluoresensi dan" | Kedua alat disebut eksplisit; "kondisi sel" = terpapar HIV (A) dan hidup/mati (B) |
| **Opsi 2** | Illinois | *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Mikroskop Fluoresensi Time-Lapse Menggunakan Machine Learning* | Jenis citra diganti | Jurkat = lini sel T CD4+, bukan sel primer → dijelaskan di Bab 1/3; "kondisi" = ekspresi HIV aktif/laten/ditekan |
| **Opsi 3** | Semua opsi | *Klasifikasi Kondisi Sel T CD4 pada Infeksi HIV Berdasarkan Citra Mikroskopi Optik Menggunakan Machine Learning* | "Sel CD4" → "Sel T CD4"; jenis citra → "Mikroskopi Optik" | 14 kata; tidak perlu diganti lagi apa pun dataset yang dipilih; menonjolkan sisi optika. IFC = *flow cytometry* dengan optik mikroskop → dijelaskan di Bab 2/3 |

"CD4" dipertahankan di semua opsi karena HIV secara khusus menyerang sel T CD4 (reseptor CD4 = pintu masuk virus).

### Gambaran tujuan penelitian (untuk dataset heiDATA + Essig; Opsi 1 atau 3)
1. Mengekstraksi fitur fisis (morfometri dan intensitas/bio-optik) dari citra sel T CD4 pada dua modalitas: mikroskop fluoresensi dan IFC.
2. Membangun dan membandingkan model ML (LogReg, RF, SVM) untuk mengklasifikasikan (a) sel terpapar HIV-1 vs tidak dan (b) sel hidup vs mati.
3. Mengevaluasi model dengan validasi k-fold berkelompok untuk menghindari kebocoran efek *batch*.
4. Menafsirkan fitur yang paling berpengaruh beserta arti fisisnya.

## 4. Pertanyaan & keputusan yang diminta dari pembimbing
0. **Dataset:** setuju usulan utama heiDATA (A) + Essig (B)? Atau Bagian HIV diganti Illinois (alternatif teruji)?
1. Bolehkah data Essig (tanpa HIV, dikaitkan lewat pustaka kematian sel CD4) dipakai sebagai Bagian B?
2. Opsi judul mana yang dipilih: Opsi 1 / Opsi 2 (sesuai dataset) atau Opsi 3 (berlaku untuk semua dataset)?
3. Kelas Bagian A: usulan **terpapar HIV-1 vs Mock dari kapsid** sebagai hasil utama; +Vpx vs −Vpx (Lamin B1) cukup sebagai analisis
   konsistensi fitur (ML lintas percobaan ≈ acak). Setuju?
4. Apakah hasil k-fold berkelompok (jujur tetapi lebih rendah) boleh dilaporkan berdampingan dengan k-fold per sel sebagai temuan
   kebocoran efek *batch*?
5. Koreksi hasil B5 (AUC 0,65 → 0,57 akibat bug normalisasi kapsid): cukup dilaporkan di naskah sebagai bagian kontrol kualitas?
6. Administrasi: target periode ujian & tenggat; pembimbing pendamping & NIP; judul Bab 3.

## 5. Pustaka (sudah diperiksa keberadaannya)
- Doitsh G., dkk. (2014). Cell death by pyroptosis drives CD4 T-cell depletion in HIV-1 infection. *Nature*, 505, 509–514. DOI 10.1038/nature12940.
- Cummins N. W., & Badley A. D. (2010). Mechanisms of HIV-associated lymphocyte apoptosis: 2010. *Cell Death & Disease*. PMID 21368875.
- Ananth dkk. (2024) — heiDATA; Essig K., dkk. (2022), Dryad, DOI 10.5061/dryad.ht76hdrk7; Shetab Boushehri S., dkk. (2023),
  *Nature Communications*, DOI 10.1038/s41467-023-43429-2.
