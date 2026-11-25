# Panduan Menulis di Google Docs → LaTeX

Draf naskah ditulis di **satu Google Doc dengan 6 tab** (`Drive/Project-Skripsi/naskah/`, "Naskah Skripsi - Rahul Ghulam
Hidayatulloh"; sejak 25 Nov 2026): tab Bab I–V untuk draf per bab, dan tab **Skripsi Final** berisi urutan lengkap naskah
(halaman muka → Bab I–V → Daftar Pustaka → Lampiran) yang diisi dengan bab yang sudah disetujui. Setiap bab dikonversi ke LaTeX
(`thesis/`) **setelah bab itu disetujui dosen**. Jangan menunggu semua bab selesai: konversi di akhir menumpuk
pekerjaan tepat menjelang deadline.

## Format (mengikuti `thesis/skripsidtntf.cls`, opsi `tugasakhir,satusetengahspasi`)
| Unsur | Pengaturan di Google Docs | Asal di template |
|---|---|---|
| Kertas | A4 | `a4paper` |
| Margin | kiri 4,0 cm · kanan 2,7 cm · atas 4,26 cm · bawah 3,44 cm | 1 in + `oddsidemargin` 1,46 cm; `textwidth` 14,3 cm; `topmargin`/`headsep`; `textheight` 22 cm |
| Huruf | Times New Roman 12 pt | `times`, `12pt` |
| Spasi baris | 1,5 | `satusetengahspasi` (lihat catatan) |
| Paragraf | rata kiri-kanan, inden baris pertama 1,27 cm (36 pt), jarak antarparagraf 8 pt | `parindent` 3em, `parskip` 8pt |
| Judul bab (Heading 1) | "BAB I" baris baru "PENDAHULUAN", tengah, tebal, 14 pt | `\@makechapterhead` (`\large\bfseries`, huruf kapital) |
| Subbab (Heading 2/3) | "I.1. Judul" / "I.1.1. Judul", rata kiri, tebal, 12 pt | `\thesection` = I.1., `\thesubsection` = I.1.1. |
| Nomor halaman | **belum dipasang** — Sisipkan → Nomor halaman, kanan atas (halaman pertama bab: tengah bawah) | `myheadings`; `chapterheading` |

Catatan: class memuat opsi bawaan `duaspasi` dan opsi `satusetengahspasi` tidak mematikannya, sehingga PDF LaTeX saat ini
ter-*compile* dengan `\doublespacing`. Docs memakai 1,5 sesuai opsi yang dipilih di `main.tex`; pastikan ke pembimbing/panduan.
Nomor subbab diketik manual (Docs tidak punya penomoran I.1.); saat konversi ke LaTeX nomor dihapus karena dibuat otomatis.

## Konvensi wajib (supaya konversi mulus)

| Elemen | Tulis di Docs sebagai | Alasan |
|---|---|---|
| Judul bab/subbab | Gaya **Heading 1 / 2 / 3** (menu Format → Gaya paragraf), bukan teks tebal biasa; ikuti struktur bab template kampus | Pandoc mengubahnya jadi `\chapter`, `\section`, `\subsection` |
| Sitasi | `[@kunci]`, mis. `[@smith2020]`; beberapa: `[@smith2020; @lee2021]` | Kunci harus ada di `thesis/refs.bib` dan sudah diverifikasi. Saat konversi menjadi `\cite{kunci}` (gaya `skripsi.bst`). Jangan ketik "(Smith, 2020)" bebas |
| Persamaan | Notasi LaTeX di antara `$$...$$` (persamaan bernomor) + definisikan semua variabel dan satuan SI di paragraf bawahnya | Panduan kampus §4.3: persamaan rata tengah, bernomor di kanan |
| Istilah asing | *Miring* (Ctrl+I), mis. *machine learning*, *imaging flow cytometry* | Panduan kampus §4.3 (PUEBI) |
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
2. Unduh: buka tab bab itu, **File → Download → Microsoft Word (.docx)** (unduhan dapat memuat semua tab; ambil bagian bab
   yang dimaksud), simpan sementara di luar repo. Alternatif: Claude membaca tab langsung lewat konektor Google Docs (`tabId` di AGENTS.md).
3. Konversi:
   ```bash
   pandoc "Bab 3 - Pelaksanaan Penelitian.docx" -o thesis/bab3-pelaksanaan-penelitian.tex --top-level-division=chapter
   ```
4. Rapikan: sitasi `[@kunci]` → `\cite{kunci}` (set `\adapustakatrue` di `main.tex` begitu ada sitasi pertama),
   gambar → `\includegraphics` dari `results/`/`thesis/figures/`, rujukan silang → `\label`/`\ref`, persamaan → `equation`
   bernomor, istilah asing → `\textit{}`; ikuti contoh format di `thesis/template-kampus/Bab4.tex`.
5. Compile (`scripts/build-thesis.ps1` atau GitHub Actions), cek PDF, lalu commit.
6. Tandai di `docs/STATUS.md` dan `docs/RIWAYAT-PENGERJAAN.md` bahwa bab tersebut sudah dikonversi.
   Setelah dikonversi, **sumber kebenaran bab itu pindah ke LaTeX**; revisi berikutnya dilakukan di `.tex`.

Langkah 3–5 bisa didelegasikan ke Claude Code ("konversi Bab 3 dari Google Docs ke LaTeX sesuai PANDUAN-GDOCS.md").
