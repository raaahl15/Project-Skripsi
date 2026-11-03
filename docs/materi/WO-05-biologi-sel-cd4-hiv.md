# WO-05 — Materi Dasar: Struktur Sel, Sel T CD4, dan Biologi HIV
> Draf disusun dengan bantuan AI (2026-11-03) untuk dipelajari mahasiswa. Arahan asal: bimbingan 2 (4 Sep 2026).
> **Pernyataan biologi umum di bawah perlu disitasi dari buku teks/review saat masuk Bab 2** (mis. buku biologi sel & imunologi
> yang dipakai di kampus). Hanya paper bertanda ✔ yang sudah diverifikasi keberadaannya.

## 1. Struktur sel (eukariot) yang relevan
- **Membran plasma**: lapisan ganda fosfolipid dengan protein reseptor (termasuk **CD4**, CCR5/CXCR4).
- **Sitoplasma & sitoskeleton**: filamen aktin (dapat diwarnai *phalloidin*), mikrotubulus.
- **Inti (nukleus)**: berisi DNA/kromatin. Dibungkus **selubung inti** (dua membran) yang memiliki **kompleks pori inti (NPC)**
  sebagai jalur keluar-masuk molekul besar.
- **Lamina inti**: jaring protein di sisi dalam selubung inti (lamin A/C, **B1**, B2) yang memberi bentuk & kekakuan inti.
  → **Lamin B1** dipakai di dataset sebagai penanda batas inti; pada citra tampak sebagai **cincin** di tepi inti.
- Saat **apoptosis**, lamina inti didegradasi dan kromatin memadat/terfragmentasi → bentuk & tekstur inti berubah
  (relevan untuk kelas "mati").

## 2. Limfosit T dan sel T CD4
- Limfosit T berkembang di timus; mengenali antigen melalui **reseptor sel T (TCR)** bersama kompleks **CD3**.
- **Sel T CD4 (T helper)**: mengenali antigen yang disajikan molekul MHC kelas II; mengoordinasikan respons imun
  (mengaktifkan sel B, sel T CD8, makrofag). **Sel T CD8**: sitotoksik (MHC kelas I).
- **CD4** = glikoprotein permukaan; selain fungsi imun, CD4 adalah **reseptor utama HIV**.
- **Sel T istirahat (*resting*)** vs **teraktivasi**: sel istirahat kecil, inti relatif besar, metabolisme rendah, kadar dNTP rendah →
  kurang permisif terhadap infeksi HIV. Sebagian besar sel T CD4 di darah dalam keadaan istirahat.

## 3. HIV-1
- **Retrovirus** (genus *Lentivirus*); virion berdiameter ±100–150 nm.
- **Selubung**: glikoprotein **gp120** (berikatan dengan CD4) dan **gp41** (fusi membran).
- **Kapsid (CA, protein p24)** berbentuk kerucut, berisi 2 salinan genom **RNA**, enzim ***reverse transcriptase* (RT)** dan
  **integrase**.
- Protein aksesori HIV-1: Vif, Vpr, Vpu, Nef (Nef antara lain menurunkan ekspresi CD4 di permukaan sel terinfeksi).
- **Vpx** **bukan** milik HIV-1, melainkan HIV-2/SIV; dalam eksperimen dipakai untuk mendegradasi **SAMHD1** (lihat §5).

## 4. Siklus replikasi HIV-1 (ringkas)
1. **Perlekatan**: gp120 ↔ CD4, lalu koreseptor **CCR5** atau **CXCR4**.
2. **Fusi** membran (gp41) → kapsid masuk sitoplasma.
3. ***Reverse transcription***: RNA → DNA, berlangsung di dalam/terkait kapsid.
4. **Transport ke inti & impor inti** melalui pori inti; kapsid berinteraksi dengan faktor inang seperti **CPSF6**.
5. **Integrasi** DNA virus ke kromosom inang oleh integrase → **provirus**.
6. **Transkripsi & translasi** → protein virus (pada virus reporter, mis. **GFP**, menandai sel yang terinfeksi produktif).
7. **Perakitan, pelepasan (*budding*), pematangan** virion baru.

## 5. Mengapa sel T CD4 istirahat sulit terinfeksi (konteks dataset heiDATA)
- Protein inang **SAMHD1** menurunkan kadar dNTP → *reverse transcription* terhambat.
- **Vpx** mendegradasi SAMHD1 → *reverse transcription* dapat berlanjut. Karena itu dataset memakai kondisi **+Vpx / −Vpx**.
- ✔ Ananth S. et al. (2024), *Cell Reports* 43(3):113941, DOI 10.1016/j.celrep.2024.113941: pada sel T CD4 istirahat, kapsid HIV-1
  yang berisi kompleks RT/PIC dapat diimpor ke inti, merekrut CPSF6, dan berpindah ke *nuclear speckles*; *reverse transcription*
  tetap tidak tuntas, dan pembatasan oleh aktivitas dNTPase SAMHD1 disimpulkan sebagai hambatan utama sebelum integrasi
  (ringkasan dari abstrak — baca paper aslinya).

## 6. Kondisi sel: normal, terinfeksi, mati — dan ciri yang mungkin terukur secara optik
| Kondisi | Penanda biologis | Ciri bio-optik yang mungkin terukur |
|---|---|---|
| Normal | Tidak ada sinyal virus | Inti bulat, lamina utuh, tanpa titik kapsid/GFP |
| Terinfeksi / terpapar | Kapsid (CA/p24), GFP reporter, CD4 turun | Titik kapsid di sitoplasma/inti, sinyal GFP, perubahan distribusi intensitas |
| Mati (apoptosis) | Caspase-3 aktif, *live/dead dye* | Penyusutan sel & inti, kromatin padat/terfragmentasi, lamina terdegradasi, perubahan tekstur |

- Deplesi sel T CD4 pada infeksi HIV terjadi melalui beberapa jalur kematian (apoptosis, piroptosis, efek sitopatik langsung);
  ✔ Luo X. et al. (2022), *Frontiers in Immunology*, DOI 10.3389/fimmu.2022.883420 meneliti kerentanan subset sel T CD4 jaringan
  terhadap infeksi dan kematian (CyTOF + scRNA-seq).

## 7. Dasar optika pencitraan
- **Fluoresensi**: fluorofor menyerap cahaya eksitasi lalu memancarkan cahaya dengan panjang gelombang lebih panjang (*Stokes shift*).
  Nama kanal di dataset (mis. Lamin B1.**405**, CA.**568**, SiR.**647**) menunjukkan panjang gelombang/fluorofor tiap penanda.
- **Resolusi lateral** mikroskop optik dibatasi difraksi, kira-kira ≈ λ/(2·NA) (±200–300 nm untuk cahaya tampak) → titik kapsid
  (±100 nm) tampak sebagai titik kabur seukuran batas resolusi.
- ***Z-stack***: serangkaian citra pada kedalaman fokus berbeda → informasi 3D; proyeksi intensitas maksimum menggabungkannya ke 2D.
- **Imaging flow cytometry (IFC)**: sel mengalir satu per satu dan dicitrakan multi-kanal (brightfield, darkfield/*side scatter*,
  fluoresens) dengan laju ribuan sel per detik — throughput tinggi, resolusi lebih rendah daripada mikroskop konfokal.

## 8. Latihan pertanyaan (jawab dengan kata-kata sendiri)
1. Mengapa HIV menyerang sel T CD4, dan apa akibatnya bagi sistem imun?
2. Apa fungsi Lamin B1 dan mengapa dipakai sebagai penanda di citra?
3. Apa itu Vpx/SAMHD1 dan mengapa dataset memakai kondisi +Vpx/−Vpx?
4. Ciri fisik apa yang berubah ketika sel mengalami apoptosis?
5. Apa beda citra mikroskop fluoresens dan citra *imaging flow cytometry*?
