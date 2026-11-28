---
title: "Draf Gambaran Bab 2 — Tinjauan Pustaka dan Dasar Teori"
subtitle: "Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry Menggunakan Machine Learning"
---

**Mahasiswa:** Rahul Ghulam Hidayatulloh (23/519760/TK/57266) · **Pembimbing:** Nopriadi, S.T., M.Sc. · **Tanggal:** 26 November 2026

> Draf berupa kerangka poin isi dan pustaka per subbab, belum naskah final. Struktur mengikuti template skripsi DTNTF
> (II.1 Tinjauan Pustaka, II.2 Dasar Teori). Bagian bertanda [Sk1] khusus Skenario 1 (heiDATA + Essig) dan [Sk2] khusus
> Skenario 2 (Illinois + Essig); dipilih setelah dataset ditetapkan. Pustaka sudah diverifikasi DOI-nya dan akan dibaca
> sebelum tiap poin ditulis menjadi paragraf. Bagian bertanda [perlu pustaka] belum memiliki rujukan.

## II.1 Tinjauan Pustaka — penelitian terdahulu
Isi: penelitian yang relevan, hasil, dan keterbatasannya, lalu posisi penelitian ini. Ditutup dengan tabel ringkasan
penelitian terdahulu (peneliti, data, metode, hasil, keterbatasan).

1. **Fitur citra + *machine learning* pada *imaging flow cytometry* (IFC)**: analisis siklus sel tanpa pewarna dari kanal
   *brightfield*/*darkfield* (Blasi et al., 2016); alur terbuka fitur CellProfiler + ML (Hennig et al., 2017); klasifikasi sel
   darah putih dengan validasi per subjek (Lippeveld et al., 2020); pemantauan leukemia (Doan et al., 2020).
2. **Pembanding *deep learning***: *deep learning* pada citra IFC (Eulenberg et al., 2017); tinjauan *image-based profiling*
   (Caicedo et al., 2017; Chandrasekaran et al., 2021).
3. **Pencitraan dalam riset HIV**: tinjauan IFC pada riset HIV (Elfimov et al., 2025); klasifikasi morfologi virion HIV-1 pada
   citra TEM dengan *deep learning* (Rey et al., 2021); kuantifikasi sel target HIV di jaringan (Shao et al., 2024).
4. **Penelitian sumber data**: tahap pasca-masuk HIV-1 pada sel T CD4 istirahat (Ananth et al., 2024) [Sk1]; skrining
   fluktuasi ekspresi gen HIV untuk agen pemicu latensi (Lu et al., 2021) [Sk2]; profil sinaps imunologis sel T dengan IFC
   dan *explainable* ML (Shetab Boushehri et al., 2023).
5. **Keandalan evaluasi**: kebocoran data membuat hasil ML terlalu optimistis (Kapoor & Narayanan, 2023).
6. **Celah dan posisi penelitian**: klasifikasi kondisi sel T CD4 pada infeksi HIV dengan fitur fisis yang dapat ditafsirkan
   dan validasi berkelompok — [dipastikan setelah pustaka di atas dibaca].

## II.2 Dasar Teori
### II.2.1 Sel T CD4 dan Infeksi HIV
- Peran sel T CD4 dalam sistem imun dan perjalanan infeksi HIV hingga AIDS (Deeks et al., 2015).
- Struktur virion HIV-1 dan siklus replikasi: masuk melalui reseptor CD4 dan koreseptor, kapsid, transkripsi balik, integrasi
  (Engelman & Cherepanov, 2012); bentuk dan ukuran kapsid (Briggs et al., 2006).
- Kondisi sel setelah terpapar: infeksi produktif, laten, dan reservoir (Siliciano & Greene, 2011; Finzi et al., 1997);
  ekspresi gen HIV stokastik dari promotor LTR dan umpan balik Tat (Weinberger et al., 2005) [Sk2].
- Kematian sel T CD4: apoptosis dan piroptosis, termasuk sel *bystander* (Doitsh et al., 2014; Cummins & Badley, 2010);
  ciri morfologi sel mati (Elmore, 2007; Kroemer et al., 2009).
- Inti sel dan lamina inti (Lamin B1) sebagai penanda struktur inti (Dechat et al., 2008) [Sk1].

### II.2.2 Pembentukan Citra Optik Sel
- Fluoresensi: eksitasi, emisi, fluorofor dan penanda spesifik molekul; mikroskop *widefield* dan konfokal
  (Lichtman & Conchello, 2005; Pawley, 2006).
- Batas resolusi optik dan *point spread function*: d = 0,61 λ / NA; objek lebih kecil dari batas resolusi (kapsid) tampak
  sebagai titik PSF (Born & Wolf, 1999; Pawley, 2006).
- Kuantifikasi intensitas fluoresensi: derau, latar, saturasi, normalisasi (Waters, 2009).
- Citra *brightfield*: kontras dari serapan dan pembiasan cahaya oleh sel tanpa pewarna [perlu pustaka].
- Prinsip IFC (ImageStream): kanal *brightfield*, *darkfield*, dan fluoresensi untuk tiap sel (Basiji et al., 2007;
  Barteneva et al., 2012; Doan et al., 2018).
- Mikroskopi fluoresensi *time-lapse* dan reporter GFP untuk mengukur ekspresi gen dari waktu ke waktu (Lu et al., 2021) [Sk2].

### II.2.3 Segmentasi Citra Sel
- Tinjauan metode segmentasi sel (Meijering, 2012).
- Pengambangan Otsu (varians antarkelas) (Otsu, 1979) dan *watershed* untuk memisahkan sel bersentuhan (Vincent & Soille, 1991).
- Deteksi titik dengan *Laplacian of Gaussian* dan pemilihan skala (Lindeberg, 1998); pengaruh rasio sinyal-derau terhadap
  deteksi (Smal et al., 2010) [Sk1].
- Pelacakan sel antarbingkai pada citra *time-lapse* (Jaqaman et al., 2008) [Sk2].

### II.2.4 Fitur Fisis Citra Sel
- Morfometri: luas, keliling, sirkularitas 4πA/P², soliditas A/A<sub>hull</sub>, eksentrisitas, sumbu mayor dan minor
  (Pincus & Theriot, 2007).
- Intensitas: rerata, simpangan baku, intensitas terintegrasi, rasio intensitas tepi terhadap tengah inti (Waters, 2009).
- Tekstur: matriks ko-okurensi aras keabuan (GLCM) — kontras, homogenitas, energi, korelasi (Haralick et al., 1973);
  gradien RMS citra *brightfield* sebagai ukuran ketajaman tepi [perlu pustaka].
- Sinyal virus: jumlah titik kapsid di dalam dan di sekitar inti [Sk1]; fitur deret waktu intensitas GFP: koefisien variasi,
  kemiringan, rasio akhir/awal, autokorelasi (Weinberger et al., 2005) [Sk2].
- Perangkat ekstraksi fitur citra sel (Carpenter et al., 2006; van der Walt et al., 2014).

### II.2.5 *Machine Learning* untuk Klasifikasi
- Pembelajaran terawasi, standardisasi fitur, bias dan varians (Hastie et al., 2009; James et al., 2013).
- Regresi logistik (Hastie et al., 2009), *random forest* (Breiman, 2001), dan *support vector machine* (Cortes & Vapnik, 1995):
  prinsip, rumus, dan hiperparameter.
- Kepentingan fitur dengan permutasi untuk menafsirkan model (Altmann et al., 2010).

### II.2.6 Validasi Model
- Validasi silang *k-fold*; pemilihan hiperparameter di dalam data latih (*nested cross-validation*) (Varma & Simon, 2006;
  James et al., 2013).
- Validasi silang berkelompok untuk data berstruktur (per percobaan, donor, atau *plate*) (Roberts et al., 2017); efek *batch*
  (Leek et al., 2010); kebocoran data (Kapoor & Narayanan, 2023).
- Uji permutasi untuk signifikansi (Altmann et al., 2010) dan selang kepercayaan dengan *bootstrap* (Efron & Tibshirani, 1993).

### II.2.7 Metrik Evaluasi
- Matriks konfusi; sensitivitas dan spesifisitas pada konteks uji diagnostik, biaya *false negative* dan *false positive*
  (Altman & Bland, 1994).
- Kurva ROC dan AUC (Fawcett, 2006); kurva *precision-recall* pada kelas timpang (Saito & Rehmsmeier, 2015).
- Koefisien korelasi Matthews (MCC) dibandingkan F1 dan akurasi (Chicco & Jurman, 2020); *balanced accuracy*
  (Brodersen et al., 2010).

## Catatan
- Subbab "*Explainable AI* (Grad-CAM)" pada kerangka awal dihapus karena penelitian tidak lagi memakai *deep learning*;
  IFC digabung ke II.2.2.
- Template menyarankan pustaka maksimal 20 tahun; pustaka lebih tua (Otsu, Haralick, Cortes & Vapnik, dll.) hanya untuk asal-usul
  metode klasik.
- Masih terbuka: 2 [perlu pustaka] (optika *brightfield*, gradien RMS), pemilihan [Sk1]/[Sk2] setelah dataset ditetapkan, dan
  tabel penelitian terdahulu.
