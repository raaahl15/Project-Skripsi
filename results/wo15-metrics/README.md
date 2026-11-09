# WO-15 — Metrik evaluasi lengkap (9 Nov 2026)
Skrip: `src/wo15_metrics.py` · config: `configs/wo15_metrics.yaml` · keluaran: `metrics_full.json`, `summary_metrics.csv`,
`confusion_matrices.png`.

**Protokol** = WO-14: fold luar = *testing*; di dalam data latih GridSearch 3-fold = *validation* (pilih hiperparameter, skor ROC AUC).
Model LogReg / RF / SVM (`class_weight="balanced"`). Kelas positif = kondisi yang **tidak boleh terlewat**: sel terpapar HIV (heiDATA),
sel mati (Essig). FN = sel positif yang lolos (dikira negatif), FP = alarm palsu.
- `default`: ambang bawaan model (p = 0,5 / skor SVM = 0).
- `recall90`: ambang dipilih **di data latih** (skor *out-of-fold* validasi dalam) agar recall ≥ 0,90, lalu diterapkan ke fold uji.
- Skema `group` = fold dipisah per percobaan (heiDATA: per figure) / per donor (Essig). `kfold5` = fold acak per sel.
- Angka = rata-rata antar-fold. Spesifisitas/NPV hanya dihitung pada fold yang memuat kelas negatif.

## Ringkasan (ambang bawaan; model dengan MCC tertinggi per baris)
| Tugas | Skema | Model | Akurasi | Bal. acc | Presisi | Recall | Spesifisitas | F1 | MCC | ROC AUC | CM gabungan [[TN,FP],[FN,TP]] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A HIV vs Mock, kapsid (n = 100; 61/39) | per percobaan | RF | 0,883 | 0,900 | 1,000 | 0,800 | 1,000 | 0,875 | 0,809 | 0,906 | [[39, 0], [16, 45]] |
| A HIV vs Mock, kapsid | k-fold 5 per sel | RF | 0,850 | 0,876 | 1,000 | 0,751 | 1,000 | 0,850 | 0,746 | 0,876 | [[39, 0], [15, 46]] |
| A HIV vs Mock, Lamin B1 (n = 209; 170/39) | per percobaan | RF | 0,627 | 0,482 | 0,859 | 0,758 | 0,000 | 0,759 | −0,090 | 0,274 | [[0, 39], [46, 124]] |
| A HIV vs Mock, Lamin B1 | k-fold 5 per sel | SVM | 0,732 | 0,721 | 0,918 | 0,741 | 0,700 | 0,818 | 0,360 | 0,788 | [[27, 12], [44, 126]] |
| B mati vs hidup, BF (n = 702; 348/354) | per donor | RF | 0,875 | 0,873 | 0,910 | 0,845 | 0,902 | 0,871 | 0,758 | 0,935 | [[329, 25], [62, 286]] |
| B mati vs hidup, BF | k-fold 5 per sel | RF | 0,897 | 0,897 | 0,918 | 0,874 | 0,921 | 0,893 | 0,799 | 0,961 | [[326, 28], [44, 304]] |

Semua model dan kedua ambang: `summary_metrics.csv`.

## Temuan
1. **F1 / akurasi menyesatkan bila kelas timpang.** Lamin B1 per percobaan: F1 0,72–0,77 tampak "bagus", padahal ROC AUC 0,27–0,46,
   MCC negatif, dan **spesifisitas 0** (semua sel Mock diprediksi HIV). F1 tinggi hanya karena 81 % sel adalah kelas positif.
   MCC, *balanced accuracy*, dan pasangan recall–spesifisitas langsung memperlihatkan kegagalan ini.
2. **Kapsid: spesifisitas sempurna, recall terbatas.** Tidak ada sel Mock yang diprediksi HIV (FP = 0), tetapi 15–35 dari 61 sel HIV
   terlewat. Penyebabnya fisis: di S3B, **45 % sel +Vpx dan 30 % sel −Vpx tidak punya titik kapsid terdeteksi** (1G: 0 %), sama dengan Mock.
   Batas atas recall tanpa salah alarm ≈ 46/61 = 0,75. Menaikkan recall ke 0,90 berarti menyebut sel tanpa titik kapsid sebagai
   terinfeksi, sehingga spesifisitas runtuh (RF `recall90`: recall 1,0, spesifisitas 0). Batas ini ditentukan oleh **kepekaan deteksi
   optik** (titik kapsid redup di bawah ambang), bukan oleh pilihan model.
3. **Essig seimbang (348/354)**, jadi akurasi ≈ *balanced accuracy*. Ambang `recall90` menaikkan recall sel mati dari 0,82–0,87 menjadi
   0,86–0,91, dengan spesifisitas turun dari 0,90–0,94 menjadi 0,80–0,88: contoh nyata pertukaran FN ↔ FP.
4. Pada kapsid, ketiga model punya ROC AUC identik (0,906 / 0,876): fitur hanya dua hitungan titik dan ketiga model sama-sama monoton
   terhadapnya, sehingga urutan sel sama. Perbedaan model baru muncul setelah ambang dipilih (recall 0,56–0,80).
5. Ambang `recall90` tidak stabil bila skor banyak yang seri (hitungan kapsid = 0): satu langkah ambang memindahkan puluhan sel sekaligus.
