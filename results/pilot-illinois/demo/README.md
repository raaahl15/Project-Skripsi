# Illinois IDB-8103861 — ekstraksi citra sendiri dari sumur demo (8 Nov 2026)
Data: `images_demo_DiversitySet3Plate2_WellK16.zip` (1,08 GB zip → `.nd2` 1,62 GB + `.dat`), disalin dari Drive ke
`data/raw/illinois-IDB-8103861/demo/` (tidak di-commit). Sumur K16 = sumur **senyawa** (kolom 16), bukan kontrol.

## Isi citra
- 192 bingkai × 2044 × 2048 piksel, uint16, **satu kanal GFP** (widefield, emisi 530 nm), 0,646 µm/piksel, 48 jam (15 menit/bingkai).
- Sel Jurkat tampak sebagai bulatan GFP ±15–20 piksel (±10–13 µm); latar mengalami *vignetting* (gelap di tepi). `demo_K16_frames.png`.

## Pipeline (`src/illinois_extract_demo.py`)
1. Latar = Gaussian σ 40 piksel (dihitung pada citra 1/8 lalu diperbesar) → koreksi *vignetting*.
2. Sinyal = Gaussian σ 1,5 − latar; ambang = k × σ derau robust (MAD); k = 5 (utama) dan k = 3 (menangkap sel redup).
3. Komponen terhubung, isi lubang, luas 40–1200 piksel, pemisahan sel bersentuhan dengan *watershed* jarak.
4. Per objek: pusat, luas, eksentrisitas, soliditas, intensitas rerata mentah, rerata & integral setelah dikurangi latar.
5. Pelacakan antar-bingkai: tetangga terdekat timbal-balik, maks. 6 piksel. Lintasan "lengkap" = ada di semua 72 bingkai jendela.
Waktu: ±17 menit per k untuk 192 bingkai (laptop, CPU). Overlay: `demo_K16_segmentation_overlay.png`.

## Perbandingan dengan data penulis (NIS Elements; `DiversitySet3Plate2/WellK16.csv`, 59 sel × 72 bingkai)
| | k = 5 | k = 3 |
|---|---|---|
| Objek per bingkai (median) | 981 | 1.134 |
| Lintasan lengkap 72 bingkai | 404 | 528 |
| Jendela paling cocok | bingkai 4–75 (jam 1–19, sesuai README penulis) | sama |
| Korelasi rata-rata sumur vs penulis | **r = 0,985** | 0,982 |

Fitur per sel (`compare_k5.json`, `compare_k3.json`; sel kita dibatasi ke rentang kecerahan penulis, n = 120 untuk k = 5):
| Fitur | Penulis | Kita | Uji KS |
|---|---|---|---|
| CV intensitas | 0,068 | 0,084 | p = 0,28 (tidak beda) |
| Rasio akhir/awal | 1,15 | 1,24 | p = 0,09 |
| Simpangan baku | 69 | 76 | p = 0,06 |
| Autokorelasi lag-1 | 0,78 | 0,68 | p = 0,01 |
| Rerata intensitas | 1.008 | 878 | p < 0,001 (kita lebih rendah) |
| Simpangan residu | 45 | 27 | p < 0,001 (kita lebih rendah) |

## Kesimpulan
- **Ekstraksi citra sendiri berhasil dan bisa berjalan di laptop** untuk 1 sumur. Dinamika waktu rata-rata sumur hampir identik dengan
  penulis (r 0,98), dan fitur relatif (CV, rasio akhir/awal) sebanding.
- Perbedaan: (1) penulis hanya menyertakan 59 sel (lebih terang; kriteria seleksi tidak dijelaskan di README); kita 404–528.
  (2) Intensitas absolut kita lebih rendah, kemungkinan mask kita mencakup tepi sel yang redup dan latar dikurangi berbeda.
  (3) Simpangan residu penulis lebih besar → definisi intensitas/ROI berbeda. Belum bisa dipastikan tanpa metode NIS mereka.
- Sel redup (kemungkinan laten, GFP rendah) sebagian terlewat pada k = 5 (lihat overlay) → k = 3 lebih sesuai bila sel laten penting.
- Keterbatasan: K16 adalah sumur senyawa → belum bisa dipakai untuk klasifikasi (perlu sumur kontrol kolom 1/2/23/24,
  yang hanya ada di file citra penuh 271–585 GB per plate atau di arsip per frame 18,8 GB → tahap 2, Colab).
