# Template Kampus (salinan asli — jangan diedit)

Salinan utuh folder Drive "template skripsi teknik fisika 2026" (template LaTeX resmi DTNTF FT UGM,
sumber: ugm.id/TemplateSkripsiSTF), diunduh 2026-11-03.

Naskah kita di `thesis/` dibangun dari template ini:
- `skripsidtntf.cls`, `skripsi.bst`, `logoUGM.png` disalin ke `thesis/`.
- `main.tex` = adaptasi `skripsi.tex`; `muka_skripsi.tex`, `data_skripsi.tex` (diisi data skripsi kita;
  bug kurung kurawal `\nipkajur{` yang tidak tertutup di template asli sudah diperbaiki di versi kita).
- File bab mengikuti judul & subbab `Bab1.tex`–`Bab5.tex`.
- `Bab4.tex` dan `app1.tex` di sini berguna sebagai **contoh format** persamaan, gambar, tabel, sitasi,
  dan format daftar pustaka (`pustaka.bib`).

Folder ini dikecualikan dari build (tidak di-`\input` oleh `thesis/main.tex`).
