# Hasil Bimbingan 7 — 26 Nov 2026
Mahasiswa: **Rahul Ghulam Hidayatulloh** (23/519760/TK/57266) · Pembimbing: **Nopriadi, S.T., M.Sc.**

> Disusun oleh Claude Code (26 Nov) dari rekaman bimbingan (±34 menit; transkrip otomatis Whisper *medium*, kualitas sedang).
> **Kutipan di bawah adalah parafrase**, bukan kata per kata. Hal yang tidak terdengar jelas ditandai **[perlu konfirmasi]**.
> Pembimbing meminta **rekaman tidak disebarkan** (hanya untuk mahasiswa) → rekaman dan transkrip **tidak** disimpan di repo/Drive.

| Kolom | Isi |
|---|---|
| Bimbingan ke- | 7 (SIMASTER: ke-5 bila B2 diisi lebih dulu) |
| Tanggal | Kamis, 26 Nov 2026 |
| Bentuk | Tatap muka; sekaligus latihan presentasi/tanya-jawab ujian ("*drill*") |
| Tercatat di SIMASTER | [ ] |

## 1. Yang dibawa
- Slide B7 (13 slide) dan Bahan B7. Yang terbahas: **skenario kelas**, lalu pembimbing menguji alur cerita penelitian dari awal
  (latar belakang → masalah → penelitian terdahulu → metode → validasi → metrik). Bahasan per sel vs berkelompok, hasil kedua skenario,
  judul, dan format naskah **tidak dibahas**.

## 2. Pertanyaan & tanggapan pembimbing
**a. Kelas (bahasa *machine learning*).** Mahasiswa menyampaikan rencana kelas: terinfeksi vs tidak, atau terinfeksi dibagi lagi
(aktif/laten/ditekan obat). Pembimbing: dalam ML, hal pertama pada klasifikasi adalah **kelasnya**; saat ujian pasti ditanya "kelasnya ada
berapa". Dari diskusi disimpulkan **4 kondisi**: (1) tidak terinfeksi, (2) terinfeksi (aktif/"baru terinfeksi"), (3) terinfeksi laten,
(4) terinfeksi dan ditekan obat → bagi model ini **4 kelas** (model tidak "mengerti" terinfeksi atau tidak, hanya mengenal 4 kelas).
Pembimbing menilai data **cukup untuk 4 kelas**; di akhir ada ucapan yang kurang jelas ("kayaknya bukan 4 kelas…") [perlu konfirmasi].

**b. Latar belakang harus dikuasai.** Pembimbing meminta mahasiswa bercerita dari awal seperti kepada orang awam: bagaimana selama ini
dokter/peneliti menentukan sel terinfeksi atau tidak, prosedurnya (preparasi sampel, **mengapa sel diberi pewarna**: tanpa pewarna yang
tampak hanya komponen darah; dengan pewarna/reagen, keadaan sel memberi warna berbeda), apa grafik/citra yang dihasilkan (sumbu horizontal
dan vertikal artinya apa), lalu **apa masalahnya**. "Teknis itu tukang pun bisa; sarjana harus *problem solving* dan *critical thinking*."
Jawaban mahasiswa: penghitungan manual → *human error* dan lama → ditawarkan ML.

**c. Penelitian terdahulu (bagian penting).** Pembimbing: kalau ada metode sebelumnya (AI/ML/*deep learning*), jelaskan **sampai mana**
penelitian itu dan **apa kekurangannya** — "di situlah kamu masuk"; jangan tiba-tiba masuk. Bila mengklaim "lebih akurat", harus
**dibandingkan pada dataset yang sama**. Mahasiswa: baru menemukan 3 paper yang bisa diakses; sebagian berbayar → pembimbing menyarankan
mencari akses jurnal (akun UGM). Pembimbing mengingatkan bahaya terlalu bergantung pada AI: bagian yang mestinya lancar dijawab
menjadi tidak lancar.

**d. Metode dan pembagian data.** Mahasiswa: *random forest*, ±6.200 sel, setengah (3.100) untuk latih, sisanya validasi dan uji.
Pembimbing: semua metode ML membagi data **latih, validasi, uji** — harus hafal "di luar kepala". **Latih** = menentukan parameter model
matematis; **validasi** = data berbeda untuk menilai apakah latihan sudah cukup (kalau belum, latih lagi); **uji** = mengukur kinerja
akhir dengan data uji.

**e. Metrik.** Pembimbing: "kenapa akurasi, bukan presisi, *recall*, sensitivitas?" Mahasiswa menyebut akurasi, sensitivitas,
spesifisitas. Pembimbing: orang informatika cukup memakai empat metrik; mahasiswa TF harus tahu metrik-metrik itu **dan mana yang paling
cocok** untuk kasusnya → pelajari (lanjutan WO-15).

**f. Jadwal.** Mahasiswa menyebut target presentasi/ujian **Desember** (tanggal [perlu konfirmasi]); pembimbing menyinggung alternatif
jadwal berikutnya (sekitar April) [perlu konfirmasi]. Pembimbing juga menanyakan mata kuliah Perancangan (2 semester).

**g. Penutup.** "Yang saya jelaskan tadi harus bisa kamu jawab di luar kepala." Mahasiswa menyampaikan sudah bimbingan 7–8 kali, tetapi
di SIMASTER baru 5.

## 3. Keputusan
| No | Pertanyaan (Bahan B7 §0) | Keputusan |
|---|---|---|
| 1 | Skenario dataset | Tidak diputuskan eksplisit; arah kelas pembimbing (4 kondisi termasuk laten & ditekan obat) **condong ke Skenario 2 (Illinois)** + kelas tidak terinfeksi [perlu konfirmasi] |
| 2 | Kelas | **4 kelas**: tidak terinfeksi, terinfeksi (aktif), laten, ditekan obat [perlu konfirmasi ucapan akhir] |
| 3 | Per sel vs berkelompok | Tidak dibahas |
| 4 | Metrik utama | Belum diputuskan; mahasiswa harus bisa menjelaskan metrik mana yang paling cocok |
| 5–6 | Judul, format naskah | Tidak dibahas |
| 7 | Ujian | Target Desember [tanggal perlu konfirmasi] |

## 4. Penugasan baru (→ Work Order)
| WO | Tugas | Target |
|---|---|---|
| WO-16 | Kuasai **latar belakang** sebagai cerita utuh: cara identifikasi sel terinfeksi selama ini, prosedur (pewarnaan/reagen, alat, citra/grafik dan arti sumbunya), masalahnya | B8 / ujian |
| WO-17 | **Tinjauan metode terdahulu**: apa yang sudah dicapai, kekurangannya, posisi penelitian ini; perbandingan pada dataset yang sama bila mengklaim lebih baik | B8 |
| WO-18 | **Kelas 4 kondisi**: tetapkan definisi tiap kelas + sumber datanya, latih model multikelas | B8 |
| (WO-15) | Lanjutan: pahami latih/validasi/uji dan metrik "di luar kepala"; alasan metrik paling cocok | B8 |

## 5. Revisi (→ naskah)
- Bab I latar belakang: alur "praktik saat ini → masalah → penelitian terdahulu & kekurangannya → usulan" (bukan langsung ke ML).
- Bab II.1: tabel penelitian terdahulu diisi dengan hasil **dan kekurangan** tiap penelitian.
- Bab III: definisi 4 kelas; pembagian latih/validasi/uji dijelaskan sederhana.

## 6. Jadwal bimbingan berikutnya
- [ISI NANTI]

## 7. Isian SIMASTER — salin ke form
| Kolom form | Isi |
|---|---|
| Dosen Pembimbing | Nopriadi, S.T., M.Sc. |
| Tanggal | 26 November 2026 |
| Topik Bimbingan | Penentuan kelas klasifikasi dan penguasaan alur penelitian (latar belakang, penelitian terdahulu, validasi, dan metrik evaluasi) |
| Dokumen | PDF slide B7 (unduh dari https://claude.ai/artifact/36C74VKWiKGgrMGVVY4xdZ, ≤ 2 MB) |

**Catatan Bimbingan** (teks polos, satu paragraf):
```
Mahasiswa menyampaikan progres pengolahan data dan rencana skenario kelas, yaitu klasifikasi sel terinfeksi dan tidak terinfeksi atau sel terinfeksi yang dibagi lagi menurut kondisinya. Pembimbing menekankan bahwa dalam machine learning kelas harus ditentukan dengan jelas, dan dari diskusi ditetapkan empat kondisi sel, yaitu tidak terinfeksi, terinfeksi, terinfeksi laten, dan terinfeksi yang ditekan obat, sehingga model memiliki empat kelas. Pembimbing kemudian melatih mahasiswa mempresentasikan alur penelitian dari awal dan meminta mahasiswa menguasai latar belakang masalah, yaitu bagaimana selama ini sel terinfeksi diidentifikasi, prosedur pewarnaan sampel dan citra yang dihasilkan, serta masalah pada cara tersebut. Mahasiswa juga diminta mempelajari penelitian terdahulu beserta kekurangannya sebagai dasar posisi penelitian ini, dan bila mengklaim metode lebih baik harus dibandingkan pada dataset yang sama. Pada bagian metode, pembimbing menegaskan pembagian data latih, validasi, dan uji beserta fungsinya, serta meminta mahasiswa memahami metrik evaluasi seperti akurasi, presisi, recall, sensitivitas, dan spesifisitas dan menjelaskan metrik yang paling sesuai untuk kasus ini. Tindak lanjut: menguasai latar belakang dan penelitian terdahulu, menetapkan definisi empat kelas, serta mempersiapkan penjelasan metode dan metrik untuk ujian pada bulan Desember.
```

## 8. Catatan untuk mahasiswa (penting sebelum B8/ujian)
- **Latar belakang yang disampaikan perlu diluruskan.** *Flow cytometry* konvensional mengukur intensitas fluoresensi tiap sel yang
  lewat (hasilnya histogram/*dot plot*: sumbu = intensitas pewarna/penanda, atau jumlah sel), **bukan** citra mikroskop yang titiknya
  dihitung manual; pemisahan populasi (*gating*) dilakukan di perangkat lunak. Masalah "manual" yang ada pustakanya adalah **kurasi/penilaian
  visual citra mikroskopi** (mis. lokasi kapsid ditentukan manual di Fiji pada Ananth et al. 2024) dan *gating* yang subjektif. Susun
  ulang ceritanya dengan sumber (WO-16) sebelum ditanya lagi.
- **Arti kelas Illinois tidak sama dengan yang diucapkan.** Pada data Lu et al. (2021): "aktif" = ekspresi HIV dipicu TNF (bukan
  "baru terinfeksi"), "ditekan" = diberi Alp (agen pemicu latensi, **bukan ARV**), "laten" = kontrol. Semua sel Jurkat di data ini
  membawa sirkuit gen HIV → **tidak ada kelas "tidak terinfeksi"** di Illinois. Kelas tidak terinfeksi hanya ada di heiDATA (Mock; sel
  primer, mikroskop berbeda). Menggabungkan 4 kelas dari dua dataset berbeda berisiko model mengenali **asal dataset**, bukan kondisi sel
  → perlu dibahas/dikonfirmasi di B8 (alternatif: 3 kelas Illinois aktif/laten/ditekan + heiDATA terinfeksi vs tidak terpisah).
- **Pembagian data**: yang dijalankan di repo adalah validasi bersarang (k-fold dalam untuk memilih parameter, fold/plate luar untuk uji),
  bukan "setengah latih". Samakan jawaban lisan dengan yang benar-benar dikerjakan; siapkan gambar alur latih–validasi–uji.
- Metrik: siapkan jawaban 1 menit "kenapa sensitivitas–spesifisitas (dan MCC), bukan akurasi" dengan contoh kasus Lamin B1 (WO-15).
