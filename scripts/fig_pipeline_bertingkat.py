"""Draw the hierarchical (cascade) classification framework figure for Bab III.

Output: thesis/figures/pipeline-bertingkat.png (300 dpi).
Text in the figure is Indonesian because it goes into the thesis.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "thesis" / "figures" / "pipeline-bertingkat.png"

plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots(figsize=(7.2, 7.4))
ax.set_xlim(0, 10)
ax.set_ylim(1.2, 12)
ax.axis("off")

SOLID = dict(edgecolor="black", facecolor="white", linewidth=1.2)
GREY = dict(edgecolor="black", facecolor="#e8e8e8", linewidth=1.2)
DASH = dict(edgecolor="black", facecolor="white", linewidth=1.0, linestyle="--")

CX, W = 3.9, 5.6          # main column centre and width
SX, SW = 8.65, 2.1        # side (output) column centre and width
H = 1.0


def box(x, y, w, h, text, style=SOLID, size=10, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.04,rounding_size=0.12", **style))
    ax.text(x, y, text, ha="center", va="center", fontsize=size,
            fontweight="bold" if bold else "normal")


def arrow(x1, y1, x2, y2, label=None, dashed=False, dx=0.12, dy=0.0, ha="left"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=1.1, color="black",
                                linestyle="--" if dashed else "-"))
    if label:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, fontsize=9,
                ha=ha, va="center", style="italic")


def side(y, text, label):
    box(SX, y, SW, 0.75, text, DASH, size=9.5)
    arrow(CX + W / 2 + 0.05, y, SX - SW / 2 - 0.05, y, label, dx=0, dy=0.2, ha="center")


ys = [9.9, 8.3, 6.7, 5.1]
box(CX, 11.3, 3.6, 0.7, "Citra sel tunggal", bold=True)
arrow(CX, 10.92, CX, ys[0] + H / 2 + 0.05)

box(CX, ys[0], W, H, "Tahap 0: pengenalan modalitas citra\n"
    "(IFC brightfield / mikroskopi fluoresensi)", GREY)
side(ys[0], "Lainnya:\ndi luar cakupan", "lainnya")

box(CX, ys[1], W, H, "Tahap 1: hidup atau mati\nModel A, data latih Essig (IFC)")
arrow(CX, ys[0] - H / 2 - 0.05, CX, ys[1] + H / 2 + 0.05)
side(ys[1], "Sel mati", "mati")

box(CX, ys[2], W, H, "Tahap 2: terinfeksi atau tidak\nModel B, data latih heiDATA (fluoresensi)")
arrow(CX, ys[1] - H / 2 - 0.05, CX, ys[2] + H / 2 + 0.05, "hidup")
side(ys[2], "Tidak\nterinfeksi", "tidak")

box(CX, ys[3], W, H, "Tahap 3: kondisi infeksi\nModel C, data latih Illinois (fluoresensi)")
arrow(CX, ys[2] - H / 2 - 0.05, CX, ys[3] + H / 2 + 0.05, "terinfeksi")

yo = 3.55
for x, t in [(CX - 2.0, "Aktif"), (CX, "Laten"), (CX + 2.0, "Ditekan")]:
    box(x, yo, 1.7, 0.65, t, DASH, size=10)
    arrow(CX + (x - CX) * 0.5, ys[3] - H / 2 - 0.05, x, yo + 0.38)

ax.text(0.5, 2.75,
        "Abu-abu: tahap pengarah berdasarkan modalitas, tidak menilai kondisi biologis.\n"
        "Garis putus: keluaran akhir. Setiap model dilatih dan diuji di dalam datasetnya sendiri;\n"
        "rantai utuh (Tahap 0 sampai 3 pada citra yang sama) belum dapat diuji karena belum ada\n"
        "dataset yang memuat semua label sekaligus.",
        fontsize=8.5, ha="left", va="top")

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
print(OUT)
