"""Draw the research flow diagram (Gambar III.1) for Bab III.

Output: thesis/figures/alur-penelitian.png (300 dpi). Same visual style as scripts/fig_pipeline_bertingkat.py.
Text in the figure is Indonesian because it goes into the thesis.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "thesis" / "figures" / "alur-penelitian.png"

plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots(figsize=(7.4, 10.2))
ax.set_xlim(0, 10)
ax.set_ylim(-0.4, 14.2)
ax.axis("off")

SOLID = dict(edgecolor="black", facecolor="white", linewidth=1.2)
GREY = dict(edgecolor="black", facecolor="#e8e8e8", linewidth=1.2)
NOTE = dict(edgecolor="#555555", facecolor="white", linewidth=0.9, linestyle="--")

CX, W, H = 3.3, 4.4, 0.95      # main column
NX, NW = 8.0, 3.6              # note column


def box(x, y, w, h, text, style=SOLID, size=10, bold=False, round_=0.12):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle=f"round,pad=0.04,rounding_size={round_}", **style))
    ax.text(x, y, text, ha="center", va="center", fontsize=size, fontweight="bold" if bold else "normal",
            linespacing=1.25)


def arrow(x1, y1, x2, y2, dashed=False, label=None, lx=0.0, ly=0.0, rad=0.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color="black", linestyle="--" if dashed else "-",
                                connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=8.5, style="italic", ha="center", va="center")


steps = [
    ("Studi pustaka", "Penelitian terdahulu dan celah\npenelitian (Bab II.1)"),
    ("Pemilihan dataset citra publik", "heiDATA, Essig, Illinois\n(Tabel III.1)"),
    ("Praproses dan segmentasi citra", "Proyeksi z, segmentasi inti,\ndeteksi titik kapsid, mask sel"),
    ("Ekstraksi fitur fisis per sel", "Bentuk, intensitas, tekstur,\nsinyal virus, deret waktu GFP"),
    ("Penetapan kelas kondisi sel", "Model A, B, C: 7 kelas\n(Tabel III.2, Gambar III.2)"),
    ("Pelatihan dan validasi model", "Regresi logistik, RF, SVM;\nvalidasi bersarang per kelompok"),
    ("Evaluasi dan tafsiran fisis", "Sensitivitas, spesifisitas, MCC,\nROC AUC, kepentingan fitur"),
    ("Penulisan dan kesimpulan", "Bab IV dan Bab V"),
]

y_top, gap = 12.35, 1.42
ys = [y_top - i * gap for i in range(len(steps))]
ys[-1] -= 0.6                  # room for the computing-environment label under the Colab band

# start / end terminals
box(CX, 13.6, 2.2, 0.6, "Mulai", GREY, bold=True, round_=0.3)
arrow(CX, 13.28, CX, ys[0] + H / 2 + 0.05)
for i, (title, note) in enumerate(steps):
    box(CX, ys[i], W, H, f"{i + 1}. {title}", size=10.5)
    box(NX, ys[i], NW, H * 0.92, note, NOTE, size=8.8)
    ax.plot([CX + W / 2 + 0.06, NX - NW / 2 - 0.06], [ys[i], ys[i]], color="#777777", lw=0.8, ls=":")
    if i < len(steps) - 1:
        arrow(CX, ys[i] - H / 2 - 0.05, CX, ys[i + 1] + H / 2 + 0.05)
y_end = ys[-1] - 1.25
arrow(CX, ys[-1] - H / 2 - 0.05, CX, y_end + 0.33)
box(CX, y_end, 2.2, 0.6, "Selesai", GREY, bold=True, round_=0.3)

# feedback loop: evaluation -> preprocessing (quality control / robustness checks)
xl = CX - W / 2 - 0.55
ax.plot([CX - W / 2 - 0.05, xl], [ys[6], ys[6]], color="black", lw=1.0, ls="--")
ax.plot([xl, xl], [ys[6], ys[2]], color="black", lw=1.0, ls="--")
arrow(xl, ys[2], CX - W / 2 - 0.05, ys[2], dashed=True)
ax.text(xl - 0.18, (ys[2] + ys[6]) / 2, "pemeriksaan kualitas dan uji ketahanan", rotation=90, fontsize=8.5,
        style="italic", ha="center", va="center")

# computing environment band
ax.text(CX, ys[2] + gap / 2 + 0.02, "", fontsize=1)
ax.add_patch(FancyBboxPatch((CX - W / 2 - 0.15, ys[6] - H / 2 - 0.18), W + 0.3,
                            (ys[2] + H / 2 + 0.18) - (ys[6] - H / 2 - 0.18),
                            boxstyle="round,pad=0.02,rounding_size=0.15", edgecolor="#999999",
                            facecolor="none", linewidth=0.8, linestyle=(0, (2, 2))))
ax.text(CX + 0.25, ys[6] - H / 2 - 0.26, "Langkah 3–7 dijalankan di Google Colab;\ndata di Google Drive, kode dan hasil di GitHub",
        fontsize=8, ha="left", va="top", color="#444444")

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
print(OUT)
