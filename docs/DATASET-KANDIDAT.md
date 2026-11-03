# Kandidat Dataset (penelusuran 2026-11-03)

> Konteks: dataset harus dicari sendiri (tidak disediakan pembimbing/lab). Topik proposal: klasifikasi kondisi sel T CD4
> (sehat / terinfeksi HIV / lisis) dari citra *imaging flow cytometry* (IFC) multi-kanal + Grad-CAM.
> Semua data di bawah diverifikasi langsung dari halaman sumbernya; yang tidak tercantum ditulis "tidak disebutkan".

## Temuan utama
**Tidak ditemukan dataset IFC publik berisi sel CD4 terinfeksi HIV** (dengan label sehat/terinfeksi/lisis). Pencarian
literatur & repositori (BBBC, BioStudies, Dryad, Zenodo/figshare via mesin pencari) hanya menemukan dataset IFC sel T/limfosit
dengan label lain. Review terbaru IFC dalam riset HIV (Methods Protoc 2025, DOI 10.3390/mps8010014) juga tidak menyebut dataset publik.
→ Topik perlu **disesuaikan dengan data yang tersedia** atau data harus **diakuisisi di lab** (tidak realistis untuk tenggat Desember).
Panduan §1.3 mengizinkan penggantian topik lewat *fast-track approval* jika topik semester 6 tidak dapat dilanjutkan.

## Kandidat

### 1. Dryad — IFC sinaps imunologis sel T CD4 memori (paling dekat secara biologis)
- Judul: "An imaging flow cytometry dataset for profiling the immunological synapse of therapeutic antibodies"
- Sel: **sel T CD4+ memori manusia** (9 donor sehat) dikokultur dengan sel B-LCL. Instrumen: Amnis ImageStreamX Mark II, 60×.
- Kelas/kondisi: −SEA, +SEA, Teplizumab, CD19-TCB, CD20-TCB (kondisi stimulasi/aktivasi, bukan infeksi).
- Kanal: brightfield + fluoresens (CD3-BV421, HLA-DR-PE-Cy7, Phalloidin AF594, P-CD3ζ Y142-AF647); viability dye eF780.
  Gating memakai "in-focus live+ CD3+ MHCII+ cells" → kemungkinan **sel mati tidak disertakan** (README belum terbaca, 403).
- Jumlah: > 2,8 juta citra; format `.h5` (key `image`, `mask`, `label`); ukuran total **124,94 GB** (exp1 19,6 GB … exp4 42,7 GB).
- Lisensi: tidak disebutkan spesifik (footer Dryad: "licensed for reuse"). Unduhan langsung per file.
- Sitasi: Essig K., Shetab Boushehri S., Marr C. et al. (2022), Dryad, DOI 10.5061/dryad.ht76hdrk7;
  paper: Shetab Boushehri S. et al., *Nature Communications* (2023), DOI 10.1038/s41467-023-43429-2 (juga memakai *explainable ML*).
- Kecocokan: sel CD4 asli + IFC multi-kanal + ada preseden XAI; tetapi kelas = kondisi aktivasi, bukan infeksi/lisis.

### 2. BBBC048 — Siklus sel Jurkat (paling ringan, cepat dipakai)
- Judul: "Cell Cycle Jurkat Cells" (Broad Bioimage Benchmark Collection).
- Sel: **Jurkat (garis sel limfosit T)**, terfiksasi, diwarnai PI dan MPM2; ImageStream.
- Kelas: 7 fase siklus sel (G1, S, G2, profase, metafase, anafase, telofase). Jumlah per kelas tidak disebutkan.
  Paper menyebut subpopulasi **sel mati** dapat dipisahkan secara *unsupervised* (tidak ada label sel mati).
- Jumlah: 32.266 citra sel tunggal; `BBBC048v1.zip` **1,5 GB**, unduhan langsung tanpa login.
- Lisensi: CC BY-NC-SA 3.0 (penggunaan akademik non-komersial).
- Sitasi: Eulenberg P. et al., "Reconstructing cell cycle and disease progression using deep learning", *Nat Commun* 8, 463 (2017),
  DOI 10.1038/s41467-017-00623-3; + Ljosa et al., *Nat Methods* (2012), DOI 10.1038/nmeth.2083.
- Kecocokan: sel T + IFC + kecil; tetapi kelas = siklus sel.

### 3. BioStudies S-BIAD452 — Sel darah putih sehat (stain-free IFC)
- Judul: "Imaging flow cytometry dataset of healthy human white blood cells"; ImageStream-X MK II.
- Kelas: tipe sel darah putih (CD4+/CD8+ T, neutrofil, monosit, sel B, NKT, eosinofil). Tidak ada kelas sel mati.
- Kanal: brightfield, darkfield, 9 penanda fluoresens (termasuk CD4 BV605, CD3 BV421).
- Isi file: **dataframe fitur** (IDEAS, SCIP); ketersediaan citra mentah tidak disebutkan. Lisensi & ukuran: tidak disebutkan.
- Sitasi: Lippeveld M. et al., "Classification of Human White Blood Cells Using Machine Learning for Stain-Free Imaging Flow
  Cytometry", *Cytometry A* 97(3) (2020), PMID 31688997.
- Kecocokan: rendah untuk "kondisi sel"; berguna sebagai pembanding fitur morfometri.

## Opsi penyesuaian topik (diputuskan bersama Pak Nopriadi)
| Opsi | Data | Pertanyaan riset yang mungkin | Dampak ke judul |
|---|---|---|---|
| A | Dryad (CD4 memori) | Klasifikasi kondisi aktivasi sel T CD4 dari citra IFC multi-kanal + validasi Grad-CAM | "infeksi HIV" diganti/diturunkan menjadi konteks motivasi |
| B | BBBC048 (Jurkat) | Klasifikasi kondisi/fase sel limfosit T dari citra IFC + Grad-CAM | idem; data kecil, eksperimen cepat |
| C | Data lab sendiri | Sesuai proposal asli | Tidak realistis untuk tenggat Desember |

Sumber penelusuran: https://bbbc.broadinstitute.org/BBBC048 · https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrk7 ·
https://www.ebi.ac.uk/biostudies/BioImages/studies/S-BIAD452 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11858172/
