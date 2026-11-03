# Panduan Menulis di Google Docs → LaTeX

Draf naskah ditulis di Google Docs (`Drive/Project-Skripsi/naskah/`, satu dokumen per bab), lalu dikonversi ke LaTeX
(`thesis/`) **per bab setelah bab itu disetujui dosen**. Jangan menunggu semua bab selesai: konversi di akhir menumpuk
pekerjaan tepat menjelang deadline.

## Konvensi wajib (supaya konversi mulus)

| Elemen | Tulis di Docs sebagai | Alasan |
|---|---|---|
| Judul bab/subbab | Gaya **Heading 1 / 2 / 3** (menu Format → Gaya paragraf), bukan teks tebal biasa | Pandoc mengubahnya jadi `\chapter`, `\section`, `\subsection` |
| Sitasi | `[@kunci]`, mis. `[@smith2020]`; beberapa: `[@smith2020; @lee2021]` | Kunci harus ada di `thesis/refs.bib` dan sudah diverifikasi. Jangan ketik "(Smith, 2020)" bebas |
| Persamaan | Notasi LaTeX di antara `$...$`, mis. `$F_1 = \frac{2PR}{P+R}$` | Langsung terbawa ke LaTeX tanpa diketik ulang |
| Gambar | Sisipkan gambar + baris di bawahnya: `Sumber: results/<run_id>/<file>.png` | File asli diambil dari repo saat konversi (resolusi penuh) |
| Angka hasil | Tulis angkanya + sumber, mis. `0,912 (results/exp01/metrics.json)` | Aturan: angka di naskah HARUS berasal dari `results/` |
| Tabel | Tabel Docs sederhana (tanpa sel gabungan) | Sel gabungan sering rusak saat konversi |
| Rujukan silang | Teks biasa "Gambar 3.1", "Tabel 4.2" | Diubah ke `\ref{}` saat konversi |
| Catatan untuk diri sendiri | Fitur **Komentar** Docs, bukan teks berwarna di badan naskah | Komentar tidak ikut terkonversi |

## Revisi dari dosen
- Minta dosen memberi **komentar** atau memakai mode **Menyarankan** (Suggesting).
- Setelah bimbingan: catat tiap poin revisi di `docs/REVISI.md` (kolom Bagian: mis. "Bab 3 §3.4").
- Claude (laptop, web, atau app dengan konektor Google Docs) bisa membaca komentar dan mengedit dokumen bab.

## Konversi satu bab ke LaTeX
1. Pastikan bab sudah disetujui dan semua komentar selesai.
2. Unduh: **File → Download → Microsoft Word (.docx)**, simpan sementara di luar repo.
3. Konversi:
   ```bash
   pandoc "Bab 3 - Metodologi Penelitian.docx" -o thesis/bab3-metodologi.tex --top-level-division=chapter
   ```
4. Rapikan: sitasi `[@kunci]` → `\textcite{}`/`\parencite{}`, gambar → `\includegraphics` dari `results/`/`thesis/figures/`,
   rujukan silang → `\label`/`\ref`, sesuaikan dengan template kampus.
5. Compile (`scripts/build-thesis.ps1` atau GitHub Actions), cek PDF, lalu commit.
6. Tandai di `docs/STATUS.md` dan `docs/RIWAYAT-PENGERJAAN.md` bahwa bab tersebut sudah dikonversi.
   Setelah dikonversi, **sumber kebenaran bab itu pindah ke LaTeX**; revisi berikutnya dilakukan di `.tex`.

Langkah 3–5 bisa didelegasikan ke Claude Code ("konversi Bab 3 dari Google Docs ke LaTeX sesuai PANDUAN-GDOCS.md").
