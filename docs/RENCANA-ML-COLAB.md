# Rencana Penyelesaian Machine Learning di Google Colab
Disusun 28 Nov 2026 (Claude Code / Rakai) atas permintaan pengguna. Target: ML final selesai **Senin 30 Nov 2026** (B8).
Status: **konsep, menunggu persetujuan** (keputusan di §10).

## 1. Prinsip
Semua pengolahan data dan pelatihan ML **dijalankan di Google Colab**, bukan di laptop. Laptop hanya dipakai untuk menulis kode dan
naskah (Claude Code), lalu kode dikirim ke GitHub.

| Tempat | Isi | Tidak berisi |
|---|---|---|
| **GitHub** (`raaahl15/Project-Skripsi`) | Kode `src/final/`, config `configs/final/`, notebook, **hasil kecil** (`results/final/`: CSV, JSON, PNG, README) | Data mentah, zip, model besar |
| **Google Drive** (`Project-Skripsi/`) | Data mentah (`data/raw/`), fitur per sel (`data/processed/`), model terlatih (`models/`), salinan lengkap tiap run (`results-colab/<run_id>/`) | Kode (kode hanya di GitHub) |
| **Google Colab** | Eksekusi: ekstraksi fitur, pelatihan, evaluasi, pembuatan gambar | Penyimpanan permanen (disk Colab hilang tiap sesi) |
| **Laptop** | Menulis kode/naskah, membaca hasil dari GitHub | Pengolahan data, pelatihan |

## 2. Alur kerja
```
 Claude Code (laptop)                 GitHub                       Google Colab                      Google Drive
 tulis kode + config ──push──▶  src/final, configs/final ──clone──▶  1. mount Drive  ◀──────────── data/raw/*.zip
                                                                     2. salin zip ke /content
                                                                     3. ekstraksi fitur ──────────▶ data/processed/<dataset>/
                                                                     4. latih + evaluasi
                                                                     5. hasil kecil ──commit+push──▶ GitHub results/final/<model>/
                                                                     6. hasil lengkap + model ────▶ results-colab/<run_id>/, models/<run_id>/
 baca hasil ◀──pull── GitHub
 tulis Bab IV, WO, B8
```
Pengguna membuka notebook di Colab lalu menekan **Runtime → Run all**. Claude Code tidak dapat menekan tombol Colab sendiri. Setelah run
selesai, Claude Code menarik hasilnya dari GitHub dan menuliskannya ke naskah.

## 3. Struktur folder
**Drive `Project-Skripsi/`**
```
data/raw/        dataverse_files.zip (heiDATA), exp1.zip … exp4.zip (Essig), intensityTrajectories.zip, noiseTrajectories.zip,
                 plateNSClookup.xlsx, images_demo_…K16.zip (Illinois)
data/processed/  heidata/cells.csv · essig/exp1_features.csv … exp4_features.csv · illinois/cells_controls.csv
models/<run_id>/ model_A_*.joblib, model_B_*.joblib, model_C_*.joblib
results-colab/<run_id>/  semua keluaran run + log + pip_freeze.txt + config yang dipakai
colab/           salinan notebook (pintasan untuk dibuka dari Drive/iPad)
```
**Repo**
```
notebooks/colab/final_ml_colab.ipynb   notebook final (menggantikan pilot_skripsi_colab.ipynb untuk hasil naskah)
configs/final/model_A.yaml  model_B.yaml  model_C.yaml
src/final/  features_essig.py  features_heidata.py  features_illinois.py  protocol.py  run.py  report.py
results/final/<model>/  metrics.json  summary.csv  cm.png  roc.png  importance.png  README.md
results/final/README.md  tabel ringkasan tiga model (sumber angka Bab IV)
requirements-colab.txt  versi pustaka dikunci
```

## 4. Kelas final (keputusan pengguna 28 Nov: kelas ditentukan sendiri)
Tiga model berurutan, 7 kelas, 5 keluaran akhir (sesuai WO-18):

| Model | Kelas | Dataset | Kelompok uji (anti-kebocoran) |
|---|---|---|---|
| A | hidup / mati | Essig exp1–exp4, kanal *brightfield* saja | per percobaan dan per donor |
| B | tidak terinfeksi (Mock) / terinfeksi (terpapar HIV-1) | heiDATA, fitur kapsid (+ Lamin B1 sebagai pembanding) | per percobaan (figure) |
| C | aktif (TNF-α) / laten (tanpa perlakuan) / ditekan (alsterpaullone) | Illinois, 7 plate, sumur kontrol | per plate |

## 5. Protokol evaluasi (sama untuk ketiga model)
1. **Model:** regresi logistik, *random forest*, SVM (RBF); fitur distandardisasi di dalam *pipeline* (hanya dari data latih).
2. **Nested CV:** lapisan luar *leave-one-group-out* (kelompok di §4); lapisan dalam GridSearch berkelompok 3-fold, skor *balanced accuracy*.
3. **Pembanding:** k-fold 5 per sel (tanpa kelompok) untuk menunjukkan besar kebocoran *batch*.
4. **Metrik (WO-15):** sensitivitas & spesifisitas per kelas, *balanced accuracy*, MCC, ROC AUC (makro *one-vs-rest* untuk 3 kelas),
   *confusion matrix* gabungan prediksi lapisan luar.
5. **Selang kepercayaan 95%:** *bootstrap* 1.000 kali atas prediksi lapisan luar.
6. **Uji permutasi label:** label diacak di dalam kelompok, 100 kali, model terbaik dengan parameter tetap.
   Untuk Model C (8.259 sel) dipakai regresi logistik/RF agar waktu masuk akal; dicatat di README.
7. **Kepentingan fitur:** permutasi pada data uji lapisan luar, dirata-rata antarlipatan → bahan arti fisis Bab IV.
8. Seed 42 di semua langkah; satu lingkungan Colab untuk semua angka naskah.

## 6. Pengadaan data
| Dataset | Status di Drive | Tindakan |
|---|---|---|
| heiDATA | ✅ `dataverse_files.zip` | — |
| Essig exp1 | ✅ `exp1.zip` | — |
| Essig exp2 (20 GB) | ❌ hanya di laptop | Unggah sekali dari laptop ke Drive dengan rclone (hanya pemindahan berkas, bukan pengolahan) |
| Essig exp3 (38 GB), exp4 (40 GB) | ❌ | Dryad perlu login. **Opsi 1:** token API Dryad disimpan di Colab Secrets, Colab mengunduh langsung ke Drive. **Opsi 2:** pengguna mengunduh lewat peramban lalu mengunggah ke Drive. Diuji dulu Opsi 1 |
| Illinois lintasan (7 plate) | ✅ `intensityTrajectories.zip`, `noiseTrajectories.zip`, `plateNSClookup.xlsx` | — |
| Illinois citra mentah | Hanya demo K16 (+4 sumur kontrol di laptop) | Arsip penuh 270–580 GB per plate → **tidak diolah**. Fitur Model C dari lintasan penulis; ekstraksi sendiri pada sumur kontrol yang tersedia (r = 0,985 terhadap penulis) dipakai sebagai validasi dan ditulis terus terang di Bab III |

Drive: kapasitas 5 TiB, terpakai ±174 GiB → cukup. Disk Colab gratis ±100 GB → zip Essig diolah satu per satu, fitur disimpan ke Drive
setelah setiap zip selesai (*checkpoint*).

## 7. Integrasi GitHub dari Colab
- Token baru: **fine-grained personal access token**, hanya repo `Project-Skripsi`, izin *Contents: Read and write*, masa berlaku 30 hari.
  Disimpan di **Colab Secrets** sebagai `GITHUB_TOKEN_RW` (tidak pernah ditulis di notebook/repo). Token lama *read-only* tetap untuk notebook pilot.
- Di akhir run: `git pull --rebase` → `git add results/final configs/final` → commit `Run <run_id> (Colab, commit <sha>)` → push ke `main`.
  Hanya folder hasil yang di-commit; berkas > 5 MB tidak di-commit (tetap di Drive).
- Identitas commit: nama/email pengguna di GitHub (diisi di sel konfigurasi, bukan dari agent).

## 8. Reprodusibilitas
- `run_id` = waktu UTC + 7 karakter SHA commit kode yang dijalankan.
- Tiap run menyimpan: config yang dipakai, `pip_freeze.txt`, versi Python, log lengkap, waktu eksekusi.
- `requirements-colab.txt` mengunci versi scikit-learn, numpy, pandas, scikit-image.
- Angka di naskah hanya dari `results/final/` (aturan 6 AGENTS.md).

## 9. Jadwal
| Waktu | Claude Code (Kai) | Pengguna | Colab |
|---|---|---|---|
| **Sabtu malam 28 Nov** | Tulis `src/final/`, configs, notebook, requirements; uji logika pada data kecil | Buat token GitHub *read/write* + (bila ada) token API Dryad, simpan di Colab Secrets | — |
| **Minggu pagi 29 Nov** | Unggah exp2.zip ke Drive; perbaiki bila run gagal | Jalankan notebook **Run 1**: B dan C (data sudah ada) + A dari exp1–2 | Run 1 (±1–2 jam) |
| **Minggu siang** | Analisis Run 1, tulis README hasil | Jalankan unduh + ekstraksi exp3, lalu exp4 | ekstraksi ±2 jam per percobaan |
| **Minggu malam** | Bahan Bab IV, perbarui WO-14/15/18, bahan B8 | Jalankan **Run final** (A dengan exp1–4) | Run final (±2–3 jam) |
| **Senin 30 Nov** | Rapikan | Bawa hasil ke B8 | — |

## 10. Keputusan yang dibutuhkan dari pengguna
1. Setuju 7 kelas di §4?
2. Setuju cakupan Illinois di §6 (lintasan penulis + validasi ekstraksi sendiri), karena citra mentah ratusan GB?
3. Boleh mengunggah `exp2.zip` dari laptop ke Drive (pemindahan berkas saja)?
4. Bersedia membuat token GitHub *read/write* (fine-grained, satu repo) dan, bila ada, akun/token API Dryad?

## 11. Risiko & mitigasi
| Risiko | Mitigasi |
|---|---|
| Sesi Colab terputus (idle / batas ±12 jam) | *Checkpoint* fitur per zip ke Drive; run dapat dilanjutkan tanpa mengulang ekstraksi |
| Disk Colab penuh | Satu zip per sesi, hapus dari `/content` setelah fitur tersimpan |
| RAM 12 GB | Baca zip secara *streaming* (tanpa ekstrak penuh), seperti skrip exp2 |
| Dryad menolak unduhan otomatis | Opsi 2 (unduh manual lewat peramban) |
| Uji permutasi lambat pada Model C | Model cepat + 100 permutasi, dicatat |
| Hasil berbeda dari laptop (versi pustaka) | Semua angka naskah dari satu lingkungan Colab; hasil pilot laptop hanya pembanding |
| Push GitHub bentrok dengan commit laptop | `git pull --rebase` sebelum push; Colab hanya menyentuh `results/final/` |
