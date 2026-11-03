"""Inspect README.rtf and TIFF metadata of the heiDATA MUXYRY dataset (read-only)."""
import re
import sys
from pathlib import Path

import numpy as np
import tifffile

root = Path(sys.argv[1])

readme = root / "README.rtf"
if readme.exists():
    raw = readme.read_text(errors="replace")
    text = re.sub(r"\\par[d]?", "\n", raw)
    text = re.sub(r"\{\\\*[^{}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", text)
    text = re.sub(r"[{}]", "", text)
    print("===== README =====")
    print("\n".join(l.strip() for l in text.splitlines() if l.strip()))
    print()

print("===== TIFF =====")
for f in sorted(root.rglob("*.tif")):
    rel = f.relative_to(root)
    try:
        with tifffile.TiffFile(f) as t:
            s = t.series[0]
            ij = t.imagej_metadata or {}
            page = t.pages[0]
            xres = page.tags.get("XResolution")
            unit = page.tags.get("ResolutionUnit")
            px = ""
            if xres and xres.value and xres.value[0]:
                px = f"{xres.value[1] / xres.value[0]:.4g} {ij.get('unit', unit.value if unit else '')}/px"
            arr = s.asarray()
            print(f"{str(rel):45s} shape={s.shape} axes={s.axes} dtype={s.dtype} pages={len(t.pages)} "
                  f"px={px} ch={ij.get('channels')} sl={ij.get('slices')} fr={ij.get('frames')} "
                  f"min={arr.min()} max={arr.max()}")
    except Exception as e:  # noqa: BLE001
        print(f"{str(rel):45s} ERROR {e}")
