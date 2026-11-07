# WO-14 — Definisi, Rumus, dan Arti Fisis 13 Fitur Citra heiDATA
> Bahan belajar dan draf subbab Bab 3. Disusun dengan bantuan AI (Claude Code, 7 Nov 2026) dari kode `src/data/heidata_cells.py`;
> wajib dipelajari dan dapat dijelaskan sendiri oleh mahasiswa. Pernyataan biologis yang belum bersitasi ditandai **[perlu pustaka]**.

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

## 4. Latihan (jawab tanpa melihat tabel)
1. Mengapa sirkularitas lingkaran = 1? Turunkan dari A = πr² dan P = 2πr.
2. Sebuah inti berbentuk elips dengan a = 10 µm dan b = 6 µm. Hitung eksentrisitasnya.
3. Apa beda soliditas dan sirkularitas? Beri contoh bentuk yang soliditasnya tinggi tetapi sirkularitasnya rendah.
4. Mengapa rasio tepi/inti Lamin B1 bernilai < 1 pada citra MIP padahal Lamin B1 ada di tepi inti?
5. Mengapa intensitas rata-rata kurang bisa diandalkan untuk dibandingkan antar-percobaan dibanding fitur bentuk?

Kunci singkat: (1) 4π·πr² / (2πr)² = 1. (2) e = √(1 − 36/100) = 0,8. (3) Soliditas mengukur kecembungan; sirkularitas mengukur kemiripan dengan
lingkaran. Elips panjang yang mulus: S ≈ 1, C rendah. (4) Proyeksi permukaan atas/bawah cangkang menambah sinyal di tengah. (5) Intensitas
bergantung pada setelan pencitraan yang bisa berbeda antar-percobaan; bentuk tidak.
