# Bahan B8 — Illinois 3 kelas & uji gabungan dataset (26 Nov 2026)
Skrip: `src/b8_gabung_vs_terpisah.py` (`--merge-only` = hanya bagian 2). Arahan B7: kelas kondisi sel (WO-18).

## 1. Illinois 3 kelas (laten / aktif-TNF / ditekan-Alp), satu dataset
8.259 sel (laten 4.120, aktif 2.100, ditekan 2.039), 7 plate, 9 fitur lintasan GFP. Validasi dalam (GridSearch 3-fold, skor balanced
accuracy) untuk memilih parameter; uji = plate yang tidak dipakai melatih (LOPO) atau k-fold 5 per sel.

| Skema | Model | Balanced acc | ROC AUC (makro OvR) | MCC | Sens. laten / aktif / ditekan | Spes. laten / aktif / ditekan |
|---|---|---|---|---|---|---|
| per plate (LOPO) | SVM | **0,78** | 0,90 | **0,63** | 0,67 / 0,82 / 0,86 | 0,85 / 0,84 / 0,93 |
| per plate (LOPO) | RF | 0,78 | **0,91** | 0,63 | 0,70 / 0,79 / 0,84 | 0,82 / 0,85 / 0,94 |
| per plate (LOPO) | LogReg | 0,74 | 0,88 | 0,55 | 0,58 / 0,75 / 0,88 | 0,83 / 0,84 / 0,88 |
| k-fold 5 per sel | RF | 0,79 | 0,92 | 0,64 | 0,71 / 0,80 / 0,85 | 0,83 / 0,86 / 0,94 |

- Peluang acak balanced accuracy = 0,33. Selisih per plate vs per sel ≤ 0,01 → tidak ada kebocoran *batch* (sama dengan hasil biner B7).
- Aktif dan ditekan hampir tidak pernah tertukar (9–23 sel); kesalahan utama adalah sel **laten** yang tertebak aktif (23%) atau ditekan
  (10%). Masuk akal: sebagian sel yang diberi TNF/Alp tidak merespons (heterogenitas ekspresi), sehingga mirip sel laten.
- Gambar: `illinois_3kelas_cm.png`; tabel lengkap: `illinois_3kelas_summary.csv`.

## 2. Uji gabungan: mengapa dataset tidak digabung jadi satu model
RF, k-fold 5 per sel, fitur yang ada di kedua dataset.

| Gabungan | Kelas | Akurasi menebak **asal dataset** | bAcc model gabungan | Salah tebak lintas dataset | bAcc saat label **diacak** di dalam tiap dataset | Peluang (1/K) |
|---|---|---|---|---|---|---|
| A. heiDATA + Illinois (rerata, SD, CV intensitas) | 5 | **0,99** | 0,55 | 9 dari 809 | **0,44** | 0,20 |
| B. heiDATA + Essig (7 bentuk + 2 intensitas) | 4 | **1,00** | 0,76 | 0 dari 609 | **0,45** | 0,25 |

- Asal dataset dapat ditebak hampir sempurna dari fitur yang sama (perbedaan alat, pewarna, satuan, jenis sel).
- *Confusion matrix* model gabungan berbentuk blok: kesalahan hanya terjadi **di dalam** dataset, hampir tidak pernah lintas dataset.
- **Kontrol penting:** saat label kondisi diacak di dalam tiap dataset (informasi kondisi sel dihapus), balanced accuracy tetap 0,44–0,45,
  jauh di atas peluang 0,20–0,25. Angka itu murni hasil mengenali asal dataset. Jadi sebagian besar "kinerja" model gabungan bukan
  kemampuan membedakan kondisi sel. Kemampuan yang sebenarnya hanya bisa diukur di dalam tiap dataset.
- Catatan: fitur heiDATA di sini memakai Lamin B1 (bukan kapsid) karena hanya itu yang ada padanannya; karena itu heiDATA HIV vs Mock lemah.
- Gambar: `gabungan_cm.png` (kiri label asli, kanan label diacak); tabel: `gabungan_summary.csv`.

## Kesimpulan untuk naskah/B8
Tiga sub-tugas dalam satu alur metode: heiDATA (terinfeksi vs Mock), Illinois 3 kelas (aktif/laten/ditekan; bAcc 0,78, MCC 0,63 pada
plate baru), Essig (hidup vs mati). Menggabungkan dataset membuat model belajar asal data (bukti: kontrol label diacak).
