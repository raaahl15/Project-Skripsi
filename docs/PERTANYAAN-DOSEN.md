# Pertanyaan yang Mungkin Diajukan Dosen / Penguji

> Kerangka dibuat agent berdasarkan topik. **Jawaban diisi sendiri oleh pengguna** dengan pemahaman sendiri,
> dan setiap angka harus merujuk ke file di `results/`.

## A. Latar belakang & masalah
1. Mengapa klasifikasi kondisi sel CD4 penting? Apa masalah dari analisis manual/konvensional?
   - Jawaban:
2. Apa kelebihan imaging flow cytometry dibanding flow cytometry konvensional atau mikroskop biasa?
   - Jawaban:
3. Apa beda fisis/biologis antara sel sehat, terinfeksi, dan lisis? Ciri apa yang terlihat di citra?
   - Jawaban:
4. Di mana sisi "instrumentasi" dan "sistem optika" dalam penelitian ini?
   - Jawaban:

## B. Data
5. Dari mana dataset berasal? Bagaimana label (sehat/terinfeksi/lisis) ditentukan, dan siapa yang melabeli?
   - Jawaban:
6. Berapa jumlah sampel per kelas? Apakah tidak seimbang, dan bagaimana menanganinya?
   - Jawaban:
7. Kanal apa saja yang dipakai (brightfield, darkfield/side scatter, fluoresens)? Mengapa kanal tersebut?
   - Jawaban:
8. Bagaimana data dibagi (train/validation/test)? Apakah ada kebocoran data, mis. sel dari sampel/donor yang sama muncul di train dan test?
   - Jawaban:
9. Praproses apa yang dilakukan (normalisasi, resize, augmentasi), dan apa alasannya?
   - Jawaban:

## C. Fitur & model
10. Fitur morfometri/bio-optik apa yang diekstraksi? Bagaimana cara menghitungnya?
    - Jawaban:
11. Mengapa memilih model ini? Apa baseline pembandingnya?
    - Jawaban:
12. Bagaimana hyperparameter dipilih? Apakah dicari pada data validasi, bukan data test?
    - Jawaban:
13. Bagaimana mencegah overfitting?
    - Jawaban:

## D. Evaluasi
14. Mengapa memakai metrik ini? Mengapa accuracy saja tidak cukup (terutama jika kelas tidak seimbang)?
    - Jawaban:
15. Kelas mana yang paling sering tertukar (confusion matrix), dan mengapa secara fisis/biologis?
    - Jawaban:
16. Apakah hasilnya stabil (beberapa seed / cross-validation)?
    - Jawaban:

## E. Explainable AI
17. Bagaimana cara kerja Grad-CAM? Mengapa dipilih dibanding metode XAI lain?
    - Jawaban:
18. Apakah area yang disorot Grad-CAM sesuai dengan ciri fisis sel (membran, inti/Lamin B1)? Bagaimana membuktikannya?
    - Jawaban:

## F. Keterbatasan & kontribusi
19. Apa keterbatasan utama penelitian ini?
    - Jawaban:
20. Apakah model bisa digeneralisasi ke instrumen/laboratorium lain?
    - Jawaban:
21. Apa kontribusi utama penelitian ini?
    - Jawaban:
