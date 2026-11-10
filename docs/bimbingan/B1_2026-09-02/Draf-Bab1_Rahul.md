---
title: "Draf Gambaran Bab 1 — Pendahuluan"
subtitle: "Klasifikasi Kondisi Sel CD4 pada Infeksi HIV Berdasarkan Citra Imaging Flow Cytometry Menggunakan Machine Learning"
---

**Mahasiswa:** Rahul Ghulam Hidayatulloh (23/519760/TK/57266) · **Pembimbing:** Nopriadi, S.T., M.Sc. · **Tanggal:** 10 November 2026

> Draf berupa poin-poin alur argumen, belum naskah final. Struktur mengikuti template skripsi DTNTF (Latar Belakang, Perumusan
> Masalah, Tujuan, Manfaat). Bagian bertanda [ISI NANTI] dilengkapi setelah dataset dan rumusan judul ditetapkan; setiap klaim
> fakta/angka akan diberi sitasi terverifikasi saat ditulis menjadi naskah.

## 1.1 Latar Belakang — alur argumen
1. **Masalah kesehatan**: HIV masih menjadi masalah kesehatan global; ciri utama infeksi adalah **penurunan (deplesi) sel T CD4**.
   [data epidemiologi terbaru: ISI NANTI + sitasi WHO/UNAIDS/Kemenkes]
2. **Sel T CD4 sebagai target**: HIV memakai CD4 sebagai reseptor; sel yang terpapar dapat terinfeksi, gagal terinfeksi
   (infeksi abortif), atau mati → **kondisi sel beragam** dan memengaruhi perjalanan penyakit.
3. **Cara analisis saat ini**: flow cytometry konvensional mengukur intensitas penanda tanpa citra; mikroskopi memberi citra
   tetapi analisis kondisi sel sering **manual/kurasi visual** (contoh: penentuan lokasi kapsid secara manual di Fiji pada
   Ananth et al. 2024) → lambat dan subjektif.
4. **Peluang bio-optik**: pencitraan fluoresens multi-kanal (dan IFC) merekam informasi **fisik/bio-optik** sel — bentuk inti,
   distribusi intensitas, tekstur, lokasi sinyal virus — yang dapat dikuantifikasi.
5. **Pendekatan**: **ekstraksi fitur** bermakna fisis + ***machine learning*** memungkinkan klasifikasi kondisi sel secara objektif
   **dan** mengetahui fitur apa yang membedakan kondisi tersebut (berbeda dengan *deep learning* yang sulit ditafsirkan).
6. **Celah penelitian**: [ISI NANTI setelah tinjauan pustaka — mis. belum banyak kajian kuantitatif fitur bio-optik inti
   (Lamin B1) dan lokasi kapsid untuk membedakan kondisi sel T CD4 terpapar HIV] → **harus dibuktikan dengan Bab 2**.

## 1.2 Perumusan Masalah (template: akar masalah + pendekatan, termasuk batasan)
- **Akar masalah**: penentuan kondisi sel T CD4 pada infeksi HIV dari citra masih bergantung pada pengamatan manual, dan
  belum diketahui secara kuantitatif karakteristik bio-optik mana yang paling membedakan kondisi sel.
- **Pendekatan**: segmentasi sel/inti dari citra fluoresens → ekstraksi fitur morfometri, intensitas, tekstur, dan lokasi sinyal virus
  → klasifikasi dengan *machine learning* → analisis kepentingan fitur.
- **Batasan** (draf): data sekunder publik [dataset final: ISI NANTI]; kondisi sel sesuai label yang tersedia
  [+Vpx/−Vpx/Mock atau sehat/terinfeksi/apoptosis — ISI NANTI]; tanpa akuisisi citra baru; *machine learning* klasik.

## 1.3 Tujuan (draf)
1. Mengekstraksi fitur fisik/bio-optik sel T CD4 dari citra fluoresens [IFC/mikroskopi — sesuai keputusan B5].
2. Membangun dan memvalidasi model *machine learning* untuk mengklasifikasikan kondisi sel T CD4 pada infeksi HIV.
3. Mengidentifikasi fitur yang paling membedakan kondisi sel dan menafsirkannya secara fisis/biologis.

## 1.4 Manfaat (draf)
- **Keilmuan**: pemahaman kuantitatif ciri bio-optik sel T CD4 terpapar HIV; contoh penerapan instrumentasi cerdas & sistem optika
  pada analisis sel.
- **Praktis**: dasar pengembangan analisis citra sel yang lebih objektif dan otomatis untuk riset HIV/diagnostik.
