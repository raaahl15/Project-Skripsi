# WO-14 — Definisi, Rumus, dan Arti Fisis Fitur Citra (heiDATA, Essig, Illinois)
> Bahan belajar dan draf subbab Bab 3. Disusun dengan bantuan AI (Claude Code, 7–8 Nov 2026) dari kode `src/data/heidata_cells.py`,
> `src/pilot_essig_features.py`, `src/pilot_illinois.py`, dan `src/illinois_extract_demo.py`; wajib dipelajari dan dapat dijelaskan
> sendiri oleh mahasiswa. Pernyataan biologis/fisis yang belum bersitasi ditandai **[perlu pustaka]**.
>
> Isi: Bagian 1–4 = heiDATA (fluoresens, 13 fitur) · Bagian 5 = Essig (*brightfield*, 19 fitur) · Bagian 6 = Illinois (deret waktu GFP,
> 9 fitur) · Bagian 7 = perbandingan ketiganya.

## 1. Dari citra ke fitur
1. **Citra:** z-stack mikroskopi fluoresens, 31–36 irisan, ukuran piksel Δ = 0,133 µm.
2. **Proyeksi intensitas maksimum (MIP):** tiap kanal diringkas menjadi satu citra 2D, I(x, y) = maks_z I(x, y, z).
   Konsekuensi: semua fitur adalah fitur **2D dari proyeksi**, bukan fitur 3D.
3. **Segmentasi inti (klasik, bukan *machine learning*)** dari kanal Lamin B1: penghalusan Gauss, ambang lokal + Otsu, operasi morfologi
   (*closing*, *fill holes*, *opening*), lalu *watershed* pada transformasi jarak untuk memisahkan inti yang bersentuhan. Objek dengan diameter
   di luar 3–12 µm, soliditas < 0,88, atau terpotong tepi citra dibuang. Hasilnya: mask biner M tiap inti.
4. **Deteksi titik kapsid HIV-1** pada kanal CA: detektor *Laplacian of Gaussian* (σ = 1–3 piksel). Titik terang berukuran kira-kira PSF
   mikroskop terdeteksi sebagai satu kapsid/klaster. Sebelum deteksi, intensitas dinormalisasi dengan **skala yang sama untuk semua
   bidang pandang satu percobaan** (bukan per citra), agar derau citra Mock tidak teregang menjadi titik palsu (perbaikan 7 Nov 2026).

Notasi: N = jumlah piksel dalam mask M; A = luas; P = keliling; I(x, y) = intensitas MIP (satuan a.u., hitungan detektor 16-bit).

## 2. Tabel fitur
| No | Fitur (nama di kode) | Rumus | Satuan | Arti fisis |
|---|---|---|---|---|
| 1 | Luas (`area_um2`) | A = N · Δ² | µm² | Ukuran penampang inti pada bidang proyeksi |
| 2 | Keliling (`perimeter_um`) | P = panjang batas mask (estimasi diskrit scikit-image) · Δ | µm | Panjang kontur inti; naik bila tepi berlekuk |
| 3 | Diameter ekuivalen (`eq_diameter_um`) | d = √(4A/π) | µm | Diameter lingkaran yang luasnya sama dengan inti |
| 4 | Sumbu mayor (`major_axis_um`) | a = 4√λ₁ · Δ | µm | Panjang elips dengan momen inersia kedua yang sama dengan inti |
| 5 | Sumbu minor (`minor_axis_um`) | b = 4√λ₂ · Δ | µm | Lebar elips tersebut |
| 6 | Eksentrisitas (`eccentricity`) | e = √(1 − λ₂/λ₁) = √(1 − b²/a²) | – (0–1) | 0 = bulat, mendekati 1 = memanjang |
| 7 | Soliditas (`solidity`) | S = A / A_convex | – (0–1) | 1 = cembung penuh; turun bila inti berlekuk/berlobus |
| 8 | Sirkularitas (`circularity`) | C = 4πA / P² | – (≤ 1 untuk kontur ideal) | 1 = lingkaran sempurna; turun bila memanjang atau tepinya kasar |
| 9 | Intensitas rata-rata Lamin B1 (`lamin_mean`) | Ī = (1/N) Σ I(x, y) | a.u. | Rata-rata sinyal fluoresens lamina inti pada proyeksi |
| 10 | Simpangan baku Lamin B1 (`lamin_std`) | σ = √[(1/N) Σ (I − Ī)²] | a.u. | Ketidakseragaman sinyal: lipatan, pengumpulan lokal |
| 11 | Rasio tepi/inti Lamin B1 (`lamin_rim_core_ratio`) | R = Ī_tepi / Ī_tengah | – | Sebaran Lamin B1 di tepi vs bagian tengah proyeksi |
| 12 | Kapsid di dalam inti (`ca_puncta_nucleus`) | n_in = jumlah titik CA dengan koordinat ∈ M | buah | Kapsid HIV-1 yang terproyeksi di area inti |
| 13 | Kapsid di sekitar inti (`ca_puncta_perinuclear`) | n_peri = jumlah titik CA di cincin selebar 1,5 µm di luar M | buah | Kapsid di dekat selubung inti (sitoplasma sel T istirahat yang tipis) |

Keterangan rumus:
- **λ₁ ≥ λ₂** adalah nilai eigen matriks kovarians posisi piksel dalam mask (momen pusat orde dua dibagi N):
  μ₂₀ = (1/N) Σ (x − x̄)², μ₀₂ = (1/N) Σ (y − ȳ)², μ₁₁ = (1/N) Σ (x − x̄)(y − ȳ); matriks [[μ₂₀, μ₁₁], [μ₁₁, μ₀₂]].
  Untuk elips padat dengan setengah sumbu p, nilai eigennya p²/4, sehingga panjang sumbu penuh = 2p = 4√λ.
- **A_convex** = luas *convex hull*, poligon cembung terkecil yang memuat seluruh mask (bayangkan karet gelang yang melingkari inti).
- **Tepi** = mask dikurangi hasil erosinya dengan cakram berjari-jari 4 piksel (lapisan ±0,53 µm).
  **Tengah** = mask yang dierosi dengan cakram berjari-jari 8 piksel (lebih dari ±1,06 µm dari tepi).
- Sirkularitas dihitung dari P diskrit; untuk objek kecil, estimasi keliling berbasis piksel bisa sedikit bias sehingga C dapat melewati 1.

## 3. Arti fisis lebih dalam (bahan penjelasan lisan)
- **Fluoresens:** dalam rezim linear (tanpa saturasi detektor dan *photobleaching* berat), intensitas sebanding dengan jumlah fluorofor ×
  intensitas eksitasi × efisiensi deteksi. Karena itu Ī dan σ sensitif terhadap **kondisi pencitraan** (daya laser, gain, waktu paparan) yang
  bisa berbeda antar-percobaan → salah satu sumber efek *batch*.
- **Lamin B1** membentuk lamina inti, lapisan protein tipis di bawah selubung inti [perlu pustaka]. Pada irisan tunggal, inti tampak sebagai
  cincin terang. Pada **MIP**, permukaan atas dan bawah cangkang ikut terproyeksi ke bagian tengah, sehingga R pada data ini < 1 (±0,7–0,8).
  Jadi R adalah sifat proyeksi cangkang 3D, bukan rasio irisan tengah.
- **Bentuk inti (fitur 1–8):** perubahan bentuk inti (pembengkakan, pemanjangan, lekukan) mengubah A, a, b, e, S, dan C. Kaitan perubahan bentuk
  dengan tahap pasca-masuk HIV-1 adalah **hipotesis [perlu pustaka]**, bukan fakta yang sudah ditunjukkan data ini.
- **Batas optik:** resolusi lateral mikroskop konfokal ±0,2–0,3 µm (≈ 0,61λ/NA) [perlu pustaka spesifikasi mikroskop]; ukuran piksel 0,133 µm
  mendekati syarat sampling Nyquist (piksel ≤ setengah resolusi). Detail tepi di bawah ±2 piksel tidak bermakna fisis, sehingga P, S, dan C memiliki ketidakpastian dari batas ini.
- **Kapsid HIV-1** (berbentuk kerucut, panjang ±100–120 nm [perlu pustaka]) jauh lebih kecil dari resolusi optik, sehingga satu titik terang = gambar PSF dari satu kapsid atau klaster.
  Jumlah titik adalah **batas bawah** jumlah kapsid.
- **Ketergantungan pada setelan detektor (uji ketahanan 8 Nov, `results/b6/README.md` A3):** n_in dan n_peri bergantung pada ambang LoG
  (diuji 0,03–0,20), σ maksimum (2–5 piksel), lebar cincin (0,75–3,5 µm), dan persentil normalisasi (99,5–99,99). Pada 28 pengaturan, AUC
  lintas percobaan tetap 0,86–0,97. Ambang rendah → lebih banyak titik redup tertangkap (sensitif) tetapi derau Mock ikut terhitung
  (kurang spesifik); kompromi ini ditentukan oleh rasio sinyal-derau (SNR) titik kapsid.

## 4. Latihan (jawab tanpa melihat tabel)
1. Mengapa sirkularitas lingkaran = 1? Turunkan dari A = πr² dan P = 2πr.
2. Sebuah inti berbentuk elips dengan a = 10 µm dan b = 6 µm. Hitung eksentrisitasnya.
3. Apa beda soliditas dan sirkularitas? Beri contoh bentuk yang soliditasnya tinggi tetapi sirkularitasnya rendah.
4. Mengapa rasio tepi/inti Lamin B1 bernilai < 1 pada citra MIP padahal Lamin B1 ada di tepi inti?
5. Mengapa intensitas rata-rata kurang bisa diandalkan untuk dibandingkan antar-percobaan dibanding fitur bentuk?

Kunci singkat: (1) 4π·πr² / (2πr)² = 1. (2) e = √(1 − 36/100) = 0,8. (3) Soliditas mengukur kecembungan; sirkularitas mengukur kemiripan dengan
lingkaran. Elips panjang yang mulus: S ≈ 1, C rendah. (4) Proyeksi permukaan atas/bawah cangkang menambah sinyal di tengah. (5) Intensitas
bergantung pada setelan pencitraan yang bisa berbeda antar-percobaan; bentuk tidak.

## 5. Essig — 19 fitur citra *brightfield* (sel hidup vs mati)
### 5.1 Dari citra ke fitur
1. **Citra:** *imaging flow cytometry* (IFC); tiap sel satu citra kecil berkanal banyak (BF, Antibody, CD18, F-Actin, MHCII, CD3, P-CD3ζ,
   Live-Dead; urutan kanal = asumsi dari indeks, README Dryad tidak menyebutnya). **Model hanya memakai kanal BF (kanal 0).** Ukuran piksel
   belum dicatat → satuan fitur dalam **piksel** [perlu pustaka: spesifikasi alat dari paper Essig].
2. **Mask:** mask BF dari dataset (M). Uji ketahanan: mask sendiri = magnitudo gradien Gauss (σ = 1) → ambang Otsu → *closing* → isi
   lubang → objek terbesar. Hasil klasifikasi setara (AUC 0,92–0,95), jadi pipeline tidak bergantung pada mask dataset.
3. **Latar:** b = median intensitas BF di luar gabungan semua mask; nilai sel ditulis v = I − b.

### 5.2 Tabel fitur
| No | Fitur (`BF_…`) | Rumus | Satuan | Arti fisis |
|---|---|---|---|---|
| 1 | `n_obj` | jumlah komponen terhubung dalam M | buah | 1 = sel utuh; > 1 = mask terpecah (sel terfragmentasi atau segmentasi gagal) |
| 2 | `area` | A = N (semua piksel M) | px² | Ukuran penampang sel |
| 3–8 | `perimeter`, `major_axis`, `minor_axis`, `eccentricity`, `solidity`, `circularity` | sama dengan fitur heiDATA no. 2, 4–8, dihitung pada **objek terbesar** | px / – | Bentuk sel; sel hidup dalam suspensi cenderung bulat |
| 9 | `mean` | v̄ = (1/N) Σ v | a.u. | Kecerahan rata-rata sel relatif terhadap latar |
| 10 | `std` | σ_v = √[(1/N) Σ (v − v̄)²] | a.u. | Ketidakseragaman kecerahan di dalam sel: granula, struktur internal |
| 11 | `max` | maks v | a.u. | Titik paling terang (mis. pusat "lensa" sel hidup atau granula pembias) |
| 12 | `sum` | Σ v | a.u.·px² | Total selisih kecerahan terhadap latar (gabungan ukuran dan kecerahan) |
| 13 | `p90` | persentil ke-90 dari v | a.u. | Seperti `max` tetapi tahan terhadap satu piksel ekstrem |
| 14 | `rim_inner_ratio` | (Ī_tepi − b) / \|Ī_dalam − b\| ; dalam = M dierosi 2×, tepi = M − dalam (lapisan ±2 px) | – | Kontras tepi vs bagian dalam sel: halo/garis tepi membran |
| 15 | `glcm_contrast` | Σᵢⱼ P(i, j)·(i − j)² | – | Besar beda tingkat keabuan antar-piksel bertetangga: tekstur kasar → tinggi |
| 16 | `glcm_homogeneity` | Σᵢⱼ P(i, j) / [1 + (i − j)²] | – (0–1) | Kemiripan piksel bertetangga: tekstur halus → tinggi |
| 17 | `glcm_energy` | √[Σᵢⱼ P(i, j)²] | – (0–1) | Keteraturan: sedikit pola tingkat keabuan yang dominan → tinggi |
| 18 | `glcm_correlation` | Σᵢⱼ (i − μᵢ)(j − μⱼ) P(i, j) / (σᵢ σⱼ) | – (−1–1) | Ketergantungan linear antar-piksel bertetangga: struktur besar yang mulus → tinggi |
| 19 | `gradient_rms` | G = √{(1/N) Σ_M [(∂I/∂x)² + (∂I/∂y)²]} (beda pusat) | a.u./px | Ketajaman tepi dan banyaknya perubahan kecerahan di dalam sel |

Keterangan:
- **GLCM** (*gray-level co-occurrence matrix*, Haralick): kotak pembatas sel dikuantisasi ke 32 tingkat (antara persentil 1 dan 99),
  P(i, j) = peluang piksel bernilai i bertetangga (jarak 1 piksel) dengan piksel bernilai j; dihitung pada arah 0°, 45°, 90°, 135°,
  simetris, dinormalisasi, lalu dirata-ratakan antar-arah. μ dan σ = rerata dan simpangan baku marjinal P. Kotak pembatas ikut memuat
  sedikit latar di sekitar sel → tekstur juga mencerminkan kontras tepi sel terhadap latar.
- Fitur bentuk 3–8 memakai objek terbesar, sedangkan `area` memakai semua piksel M; keduanya sama bila n_obj = 1.

### 5.3 Arti fisis *brightfield* (bahan penjelasan lisan)
- **Sumber kontras:** cahaya transmisi melewati sel. Sel tanpa pewarna hampir transparan, sehingga serapan (hukum Beer–Lambert) kecil;
  kontras terutama berasal dari **beda indeks bias** sel terhadap medium yang menggeser fase cahaya, lalu tampak sebagai beda intensitas
  karena pembiasan dan sedikit *defocus* [perlu pustaka: optika mikroskop *brightfield*/kontras fase].
- **Sel hidup:** membran utuh dan bentuk bulat bekerja seperti lensa kecil → pusat terang dan halo tepi yang halus (galeri
  `results/b6/B_gallery_live_dead.png`).
- **Sel mati:** membran rusak, isi sel menggumpal atau terfragmentasi [perlu pustaka: morfologi sel apoptosis/nekrosis] → banyak
  lompatan indeks bias kecil di dalam sel → gradien lokal lebih besar dan tekstur lebih kasar. Data mendukung ini: `gradient_rms` adalah
  fitur paling membedakan (Cohen's d mati − hidup 1,5–1,8 di kedua donor), diikuti `std`, `max`, dan `glcm_energy`.
- **Mengapa intensitas lebih kuat dari bentuk:** hanya fitur bentuk → AUC 0,75–0,79, hanya fitur intensitas → 0,91–0,92. Perubahan
  struktur internal (optik) lebih jelas daripada perubahan garis luar.
- **Peran latar b:** pengurangan latar menghapus beda **offset** kecerahan antar-citra/donor, tetapi tidak menghapus beda **gain**
  (perkalian). Itu sebabnya validasi *leave-one-donor-out* tetap perlu.
- **Label:** label ahli "mati" sesuai dengan pewarna Live-Dead (AUC 0,99), tetapi pewarna tidak dipakai sebagai fitur: model hanya
  melihat *brightfield* (*label-free*).

## 6. Illinois — 9 fitur deret waktu intensitas GFP (respons sirkuit gen HIV)
### 6.1 Dari citra ke fitur
1. **Citra:** mikroskop *widefield* fluoresens, satu kanal GFP (emisi 530 nm), 0,646 µm/piksel, satu bingkai tiap 15 menit. Sel Jurkat
   membawa sirkuit gen HIV minimal dengan reporter GFP (Lu dkk., *PNAS* 2021).
2. **Lintasan intensitas** I(t_k) per sel, 72 bingkai (jam 1–19), t_k = 0,25·k jam. Pada pilot klasifikasi lintasan ini **dibuat oleh
   penulis** (NIS Elements). Ekstraksi sendiri (sumur demo, `src/illinois_extract_demo.py`): koreksi *vignetting* (latar Gauss σ 40 px),
   ambang k × σ derau robust (MAD, σ ≈ 1,4826 × median |s − median s|), *watershed*, pelacakan tetangga terdekat timbal-balik (≤ 6 px);
   rata-rata sumur cocok dengan penulis (r = 0,985).
3. **Kelas** pada Illinois = **perlakuan** (TNF-α mengaktifkan, tanpa perlakuan, alsterpaullone menekan), bukan normal/terinfeksi/mati.

### 6.2 Tabel fitur (T = 72 bingkai)
| No | Fitur | Rumus | Satuan | Arti fisis |
|---|---|---|---|---|
| 1 | `I_mean` | Ī = (1/T) Σₖ I(t_k) | a.u. | Tingkat ekspresi GFP rata-rata selama pengamatan |
| 2 | `I_std` | σ_I = √[(1/T) Σₖ (I_k − Ī)²] | a.u. | Besar perubahan intensitas total (tren + fluktuasi) |
| 3 | `I_cv` | CV = σ_I / Ī | – | Variabilitas relatif; tidak bergantung pada skala kecerahan |
| 4 | `I_slope` | β₁ dari regresi kuadrat terkecil I_k ≈ β₀ + β₁ t_k | a.u./jam | Laju bersih perubahan GFP (produksi − degradasi/pengenceran) |
| 5 | `I_start` | rata-rata 4 bingkai pertama (1 jam) | a.u. | Tingkat awal |
| 6 | `I_end` | rata-rata 4 bingkai terakhir | a.u. | Tingkat akhir |
| 7 | `I_fold` | I_end / I_start | – | Kelipatan perubahan: > 1 naik (aktivasi), < 1 turun (penekanan) |
| 8 | `I_resid_std` | σ_r, dengan r_k = I_k − (β₀ + β₁ t_k) | a.u. | Fluktuasi di sekitar tren (derau ekspresi + derau pengukuran) |
| 9 | `I_ac1` | ρ₁ = Σₖ (r_k − r̄)(r_{k+1} − r̄′) / [(T − 1) σ_r σ_r′] | – (−1–1) | Seberapa "lambat" fluktuasinya: ρ₁ tinggi = fluktuasi bertahan beberapa bingkai |

Keterangan: r̄, σ_r dihitung pada r₁…r_{T−1}; r̄′, σ_r′ pada r₂…r_T. Fitur `N_*` dari lintasan *noise* penulis **tidak dipakai** karena
membawa rata-rata sumur ke tiap sel (kebocoran, `results/pilot-illinois/README.md`).

### 6.3 Arti fisis (bahan penjelasan lisan)
- **Intensitas GFP** sebanding dengan jumlah molekul GFP di sel (rezim linear, tanpa saturasi), jadi I(t) adalah **proksi ekspresi
  gen** dari promotor HIV (LTR) [perlu pustaka]. Pada *widefield*, cahaya dari luar bidang fokus ikut terukur, jadi I adalah ukuran
  relatif, bukan jumlah molekul absolut.
- **Model laju sederhana:** dG/dt = α − γG (α = laju produksi, γ = laju degradasi + pengenceran karena pembelahan) [perlu pustaka].
  `I_slope` ≈ α − γG: positif bila produksi meningkat (TNF), negatif/mendatar bila ditekan (alsterpaullone). *Photobleaching* juga
  menurunkan intensitas dan dapat menambah kemiringan negatif [perlu pustaka].
- **Derau ekspresi:** produksi mRNA/protein terjadi dalam semburan (*transcriptional bursting*), sehingga sel identik pun berfluktuasi
  [perlu pustaka; topik utama paper Lu dkk.]. `I_cv` dan `I_resid_std` mengukur besar fluktuasi, `I_ac1` mengukur lamanya: derau
  pengukuran (acak tiap bingkai) memberi ρ₁ ≈ 0, sedangkan fluktuasi biologis yang bertahan > 15 menit memberi ρ₁ > 0.
- **Fitur terkuat** (AUC univariat): TNF ↔ `I_fold` 0,82, `I_slope` 0,80, `I_cv` 0,79; alsterpaullone ↔ `I_end` (AUC 0,10 = 0,90 terbalik).
  Jadi yang membedakan perlakuan adalah **dinamika waktu**, bukan bentuk sel.

## 7. Perbandingan tiga sumber fitur
| | heiDATA | Essig | Illinois |
|---|---|---|---|
| Teknik citra | Konfokal fluoresens, z-stack → MIP | IFC *brightfield* (tanpa pewarna) | *Widefield* fluoresens GFP, *time-lapse* |
| Sumber kontras | Fluorofor terikat Lamin B1 & kapsid CA | Beda indeks bias (fase) + serapan kecil | Reporter GFP hasil ekspresi gen HIV |
| Jenis fitur | Bentuk inti, intensitas, hitungan titik | Bentuk, intensitas, tekstur GLCM, gradien | Statistik deret waktu |
| Jumlah fitur | 13 | 19 | 9 |
| Kelas | Mock vs terinfeksi | Hidup vs mati | Perlakuan (aktivasi / tanpa / penekanan) |
| Fitur kunci | Titik kapsid di inti (lintas percobaan AUC 0,86–0,97) | `gradient_rms`, sebaran intensitas BF (donor baru AUC 0,91–0,95) | `I_fold`, `I_slope`, `I_end` (plate baru AUC 0,85–0,95) |
| Risiko utama | Efek *batch* intensitas; hanya 2 figur berkapsid | 2 donor berlabel; satuan piksel | Jurkat, bukan CD4 primer; fitur pilot dari penulis |

Kaitan fisis lintas dataset: fitur **bentuk** (rumus sama di heiDATA dan Essig) relatif tahan terhadap setelan alat, sedangkan fitur
**intensitas** selalu bergantung pada setelan alat (daya, gain, paparan) → setiap hasil harus diuji lintas percobaan/donor/plate.

## 8. Latihan tambahan (Essig & Illinois)
6. Citra dengan intensitas seragam penuh: berapa nilai `glcm_contrast`, `glcm_homogeneity`, dan `glcm_energy`?
7. Mengapa `gradient_rms` sel mati lebih tinggi daripada sel hidup? Jelaskan dari sisi indeks bias.
8. Pengurangan latar b menghapus beda offset antar-citra. Beda apa yang tidak terhapus, dan apa konsekuensinya bagi validasi?
9. Sebuah sel Illinois: I_start = 1.000, I_end = 1.500. Hitung `I_fold`. Bila kenaikannya linear, dan pusat jendela awal dan akhir
   berjarak 17 jam, berapa kira-kira `I_slope`?
10. Mengapa derau pengukuran murni memberi `I_ac1` ≈ 0?
11. Mengapa `I_cv` lebih adil daripada `I_std` untuk membandingkan sel yang terang dan redup?

Kunci singkat: (6) Hanya satu tingkat keabuan → P(i, i) = 1: contrast 0, homogeneity 1, energy 1. (7) Isi sel yang rusak/bergranula
memiliki banyak batas indeks bias kecil → banyak perubahan intensitas tajam → |∇I| besar. (8) Beda **gain** (perkalian), mis. kecerahan
lampu/sensitivitas detektor → perlu validasi lintas donor/percobaan. (9) Fold = 1,5; slope ≈ 500 / 17 ≈ 29 a.u./jam. (10) Derau
pengukuran tidak berkorelasi antar-bingkai, jadi r_k dan r_{k+1} saling bebas. (11) CV tak berdimensi: bila semua intensitas dikali
konstanta c, σ dan Ī sama-sama dikali c sehingga CV tetap.
