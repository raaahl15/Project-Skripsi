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
| WO-14 | Arti fisis & rumus fitur | 🔄 | Tabel 13 fitur (definisi, rumus, satuan, arti fisis) → `docs/materi/WO-14-fitur-heidata.md` |
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

## 2. Usulan: dua dataset citra, HIV tetap menjadi konteks
| Bagian | Data | Jenis citra | Klasifikasi | Hasil awal |
|---|---|---|---|---|
| A | heiDATA (Ananth dkk., 2024) | Mikroskop fluoresensi (Lamin B1, kapsid HIV-1) | Sel terpapar HIV-1 vs tidak / ±Vpx | Lihat tabel di atas (lintas percobaan ≈ acak) |
| B | Essig dkk. (Dryad 2022) | Imaging flow cytometry (brightfield) | Sel T CD4 hidup vs mati | Protokol WO-14: AUC 0,91–0,94 pada donor baru |

- Metode keduanya sama: segmentasi → **ekstraksi fitur fisis** (morfometri, intensitas, tekstur) → ML (LogReg, RF, SVM) → k-fold
  berkelompok (per percobaan / per donor) → interpretasi fitur.
- Kedua dataset **tidak digabung dalam satu model** (alat, kanal, dan kondisi sel berbeda); yang disatukan adalah metode dan pertanyaannya.
- **Kaitan Essig dengan HIV:** data Essig tidak berisi HIV. Kaitannya lewat pustaka — berkurangnya sel T CD4 pada infeksi HIV-1 terutama
  terjadi melalui kematian sel (apoptosis dan piroptosis, termasuk pada sel *bystander* yang tidak terinfeksi produktif)
  (Doitsh dkk., 2014; Cummins & Badley, 2010). Kemampuan mengenali sel mati dari citra karena itu relevan untuk konteks infeksi HIV.

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
- Keterbatasan: hanya 2 percobaan yang punya Mock (100 sel).

**Bagian B — Essig, sel T CD4 hidup vs mati (brightfield saja, label ahli 354 vs 348 sel)**
| Skema | LogReg | RF | SVM |
|---|---|---|---|
| k-fold 5 per sel | 0,945 | 0,961 | 0,954 |
| Leave-one-donor-out (donor baru) | 0,921 | 0,935 | 0,909 |

- Selisih kedua skema kecil → sinyal berlaku pada donor baru. Fitur utama: **gradien RMS brightfield** (ketajaman tepi/kontras refraktif),
  sebaran intensitas, dan tekstur GLCM.

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
| | Judul | Kelebihan | Catatan |
|---|---|---|---|
| **Opsi 1** | *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Mikroskop Fluoresensi dan Imaging Flow Cytometry Menggunakan Machine Learning* | Perubahan minimal dari judul Simaster (hanya menambah "Mikroskop Fluoresensi dan") → prosedur paling mudah | "Kondisi sel" = terpapar HIV (A) dan hidup/mati (B) |
| **Opsi 2** | *Ekstraksi Fitur Morfometri dan Bio-Optik Citra Sel T CD4 untuk Klasifikasi Paparan HIV-1 dan Viabilitas Sel Menggunakan Machine Learning* | Paling jelas menggambarkan isi dan menonjolkan sisi Teknik Fisika (ekstraksi fitur fisis) | Perubahan judul lebih besar |

Judul Simaster saat ini: *Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry Menggunakan Machine Learning*.

### Gambaran tujuan penelitian (berlaku untuk kedua opsi)
1. Mengekstraksi fitur fisis (morfometri dan intensitas/bio-optik) dari citra sel T CD4 pada dua modalitas: mikroskop fluoresensi dan IFC.
2. Membangun dan membandingkan model ML (LogReg, RF, SVM) untuk mengklasifikasikan (a) sel terpapar HIV-1 vs tidak dan (b) sel hidup vs mati.
3. Mengevaluasi model dengan validasi k-fold berkelompok untuk menghindari kebocoran efek *batch*.
4. Menafsirkan fitur yang paling berpengaruh beserta arti fisisnya.

## 4. Pertanyaan & keputusan yang diminta dari pembimbing
0. Bagian HIV: tetap heiDATA, atau diganti data Illinois (lihat alternatif di atas)?
1. Bolehkah data Essig dipakai sebagai Bagian B (hidup vs mati), mengingat data dari Heidelberg kemungkinan tidak didapat?
2. Opsi judul mana yang dipilih: Opsi 1 atau Opsi 2?
3. Kelas Bagian A: (+Vpx dan −Vpx) vs Mock, atau +Vpx vs −Vpx? (Mock hanya ada di 2 dari 6 percobaan.)
4. Apakah hasil k-fold berkelompok (yang jujur tetapi rendah) boleh dilaporkan sebagai temuan, berdampingan dengan k-fold per sel?
5. Untuk Bagian A, apakah analisis konsistensi fitur per percobaan (soliditas/sirkularitas) boleh menjadi hasil utama, mengingat ML lintas percobaan belum berhasil?
6. Administrasi: target periode ujian & tenggat; pembimbing pendamping & NIP; judul Bab 3.

## 5. Pustaka (sudah diperiksa keberadaannya)
- Doitsh G., dkk. (2014). Cell death by pyroptosis drives CD4 T-cell depletion in HIV-1 infection. *Nature*, 505, 509–514. DOI 10.1038/nature12940.
- Cummins N. W., & Badley A. D. (2010). Mechanisms of HIV-associated lymphocyte apoptosis: 2010. *Cell Death & Disease*. PMID 21368875.
- Ananth dkk. (2024) — heiDATA; Essig K., dkk. (2022), Dryad, DOI 10.5061/dryad.ht76hdrk7; Shetab Boushehri S., dkk. (2023),
  *Nature Communications*, DOI 10.1038/s41467-023-43429-2.
