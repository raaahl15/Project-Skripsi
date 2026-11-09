# Materi WO-15 — Metrik evaluasi klasifikasi dan alasan pemilihannya
Disusun 9 Nov 2026 untuk arahan Bimbingan 6. Angka contoh berasal dari `results/wo15-metrics/` (jangan diketik ulang dari ingatan).
Pustaka bertanda **[perlu pustaka]** adalah kandidat yang **belum diverifikasi**; periksa dulu sebelum masuk refs.bib.

## 1. Dasar: *confusion matrix*
Kelas **positif** = kondisi yang ingin dideteksi dan tidak boleh terlewat: sel **terpapar HIV** (heiDATA), sel **mati** (Essig).

| | Diprediksi negatif | Diprediksi positif |
|---|---|---|
| **Sebenarnya negatif** | TN (*true negative*) | FP (*false positive*, alarm palsu) |
| **Sebenarnya positif** | FN (*false negative*, terlewat) | TP (*true positive*) |

N = TP + TN + FP + FN. Prevalensi π = (TP + FN)/N.

## 2. Definisi dan rumus
| Metrik | Rumus | Arti | Catatan |
|---|---|---|---|
| Akurasi | (TP + TN) / N | Proporsi semua prediksi yang benar | Menyesatkan bila kelas timpang: menebak "positif" untuk semua sel heiDATA sudah 0,81 |
| Presisi (PPV) | TP / (TP + FP) | Dari yang diprediksi positif, berapa yang benar | Bergantung pada prevalensi |
| Recall = sensitivitas (TPR) | TP / (TP + FN) | Dari semua sel positif, berapa yang tertangkap | Turun bila banyak FN |
| Spesifisitas (TNR) | TN / (TN + FP) | Dari semua sel negatif, berapa yang dikenali negatif | Turun bila banyak FP |
| NPV | TN / (TN + FN) | Dari yang diprediksi negatif, berapa yang benar | Bergantung pada prevalensi |
| *Balanced accuracy* | (Sensitivitas + Spesifisitas) / 2 | Akurasi yang tidak terpengaruh ketimpangan kelas | Tebakan acak = 0,5 |
| F1 | 2·Presisi·Recall / (Presisi + Recall) | Rata-rata harmonik presisi dan recall | **Mengabaikan TN** → buta terhadap kegagalan pada kelas negatif |
| F2 (Fβ, β = 2) | (1 + β²)·P·R / (β²·P + R) | Seperti F1, tetapi recall diberi bobot β² = 4 kali | Dipakai bila FN lebih mahal daripada FP |
| MCC | (TP·TN − FP·FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)] | Korelasi antara label dan prediksi, −1…+1 | Memakai keempat sel CM; 0 = acak [perlu pustaka: Chicco & Jurman 2020, *BMC Genomics*] |
| ROC AUC | Luas di bawah kurva TPR vs FPR untuk semua ambang | Peluang sel positif acak diberi skor lebih tinggi daripada sel negatif acak | Tidak bergantung ambang dan prevalensi; 0,5 = acak |
| PR AUC (*average precision*) | Luas di bawah kurva presisi vs recall | Kinerja pada kelas positif | Garis acak = π, jadi tidak bisa dibandingkan antar-dataset dengan π berbeda [perlu pustaka: Saito & Rehmsmeier 2015, *PLoS ONE*] |

**Ambang (threshold).** Model memberi skor; sel disebut positif bila skor ≥ ambang. Menurunkan ambang → TP dan FP naik → recall naik,
spesifisitas turun. ROC AUC merangkum semua ambang. Metrik lain (recall, spesifisitas, F1, …) hanya berlaku pada **satu ambang** yang
harus disebutkan. Ambang tidak boleh dipilih memakai data uji; di WO-15 ambang `recall90` dipilih dari data latih.

## 3. Biaya kesalahan: FN atau FP?
| Tugas | FN berarti | FP berarti | Mana lebih mahal? |
|---|---|---|---|
| A. Terpapar HIV vs Mock | Sel terinfeksi lolos dianggap sehat → jumlah sel terinfeksi **diremehkan** | Sel sehat dianggap terinfeksi → infeksi **dibesar-besarkan** | Pada analogi uji diagnostik/penapisan, **FN lebih mahal**: infeksi yang terlewat tidak ditindaklanjuti, sedangkan FP masih bisa dikonfirmasi dengan uji lanjutan [perlu pustaka: prinsip uji penapisan] |
| B. Mati vs hidup | Sel mati dihitung hidup → viabilitas dan kesehatan populasi CD4 **dilebih-lebihkan**; penurunan sel CD4 tidak terlihat | Sel hidup dihitung mati → kematian sel dibesar-besarkan | FN sedikit lebih mahal (sama arahnya dengan A), tetapi kelas seimbang sehingga kedua kesalahan relatif setara |

Catatan jujur: unit klasifikasi skripsi ini adalah **sel**, bukan pasien. "Uji kesehatan" dipakai sebagai analogi: model per sel menjadi
dasar penghitungan fraksi sel terinfeksi/mati, sehingga kesalahan sistematis (terutama FN) menggeser angka fraksi tersebut.

## 4. Usulan pemilihan metrik (keputusan mahasiswa, untuk dibawa ke B7)
1. **Metrik utama:** **sensitivitas (recall)** dan **spesifisitas**, selalu dilaporkan berpasangan pada ambang yang disebutkan.
   Alasan: keduanya langsung menjawab pertanyaan pembimbing (berapa FN, berapa FP), tidak bergantung prevalensi, dan lazim di uji diagnostik.
2. **Metrik ringkas tanpa ambang:** **ROC AUC**, untuk membandingkan model dan skema validasi (dan dengan penelitian lain).
3. **Metrik ringkas pada ambang:** ***balanced accuracy*** dan **MCC**, karena data heiDATA timpang (81 % positif).
4. **Pelengkap:** presisi, NPV, F1/F2, PR AUC, dan *confusion matrix* gabungan; **akurasi dan F1 tidak dipakai sebagai metrik utama**.
5. **Ambang:** dilaporkan dua: bawaan (p = 0,5) dan ambang yang diarahkan ke recall tinggi (dipilih dari data latih), untuk menunjukkan
   pertukaran FN ↔ FP.

## 5. Bukti dari data sendiri (`results/wo15-metrics/README.md`)
- **Mengapa bukan F1/akurasi:** Lamin B1, fold per percobaan → F1 0,72–0,77, tetapi ROC AUC 0,27–0,46, MCC negatif, spesifisitas 0
  (semua sel Mock diprediksi HIV). F1 "bagus" hanya karena kelas positif dominan.
- **Mengapa recall dan spesifisitas harus berpasangan:** kapsid HIV vs Mock → spesifisitas 1,00 (tidak ada alarm palsu), recall 0,56–0,80.
  Recall dibatasi sel HIV yang **tidak punya titik kapsid terdeteksi** (S3B: 45 % +Vpx, 30 % −Vpx). Memaksa recall 0,90 membuat
  spesifisitas jatuh ke 0. Ini batas **kepekaan deteksi optik** (sinyal kapsid redup di bawah ambang deteksi), bukan batas model.
  → Sisi Teknik Fisika: memperbaiki recall berarti memperbaiki deteksi sinyal (rasio sinyal-derau, ambang titik), bukan mengganti model.
- **Pertukaran FN ↔ FP:** Essig mati vs hidup → menggeser ambang menaikkan recall dari 0,82–0,87 menjadi 0,86–0,91, dengan spesifisitas
  turun dari 0,90–0,94 menjadi 0,80–0,88.

## 6. Latihan (siapkan jawaban lisan)
1. Hitung akurasi, recall, spesifisitas, F1, dan MCC untuk CM [[TN, FP], [FN, TP]] = [[39, 0], [16, 45]].
2. Mengapa F1 tidak berubah bila TN dinaikkan 1000 kali, sedangkan MCC berubah?
3. Model yang selalu menebak "HIV" pada heiDATA (170 HIV, 39 Mock): berapa akurasi, recall, spesifisitas, F1, *balanced accuracy*?
4. Bila prevalensi sel terinfeksi turun dari 81 % ke 10 %, metrik mana yang berubah walaupun modelnya sama?
5. Jelaskan dengan bahasa fisika mengapa recall kapsid tidak bisa naik tanpa mengorbankan spesifisitas.
