"""Sync repo Markdown -> Google Docs in Drive `Project-Skripsi/bimbingan/` (same document, same ID, same link).

How: Markdown -> HTML (python-markdown, tables), then
    rclone copyto <file.html> "gdrive:Project-Skripsi/bimbingan/<folder>/<Doc title>.html" \
        --drive-import-formats html --drive-export-formats html
With the html export format an existing Google Doc is listed as "<title>.html", so rclone UPDATES it in place
(files.update -> ID unchanged; tested 8 Nov 2026 on _uji/Uji Konversi). A title that does not exist yet is created
as a new Google Doc -> record its ID in docs/DRIVE-DOCS.md.

Usage: python scripts/sync_gdocs.py [--only <md path> ...] [--dry-run]
Edit SYNC below when a document is added (keep it in line with docs/DRIVE-DOCS.md).
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

REMOTE = "gdrive:Project-Skripsi/bimbingan"
SYNC = [  # (repo markdown, Drive folder, Google Doc title)
    ("docs/PEMROSESAN-DATA.md", "", "Dokumentasi Pemrosesan Data dan Fitur"),
    ("docs/WORK-ORDER.md", "Work Order", "00 Daftar Work Order"),
    ("docs/work-order/WO-09.md", "Work Order", "WO-09 Fiksasi dataset"),
    ("docs/work-order/WO-12.md", "Work Order", "WO-12 Permintaan data tambahan heiDATA"),
    ("docs/work-order/WO-14.md", "Work Order", "WO-14 Validasi k-fold dan arti fisis fitur"),
    ("docs/bimbingan/B5_2026-11-04/BAHAN.md", "B5 - 2026-11-04", "Bahan Bimbingan 5"),
    ("docs/bimbingan/B5_2026-11-04/HASIL.md", "B5 - 2026-11-04", "Hasil Bimbingan 5"),
    ("docs/bimbingan/B6_2026-11-09/BAHAN.md", "B6 - 2026-11-09", "Bahan Bimbingan 6"),
    ("docs/materi/WO-14-fitur-heidata.md", "B6 - 2026-11-09", "Materi WO-14 Fitur heiDATA"),
    ("docs/bimbingan/B6_2026-11-09/HASIL.md", "B6 - 2026-11-09", "Hasil Bimbingan 6"),
    ("docs/work-order/WO-15.md", "Work Order", "WO-15 Pemilihan metrik evaluasi"),
    ("docs/materi/WO-15-metrik-evaluasi.md", "B6 - 2026-11-09", "Materi WO-15 Metrik Evaluasi"),
]
CSS = ("body{font-family:Arial,sans-serif;font-size:11pt;line-height:1.4}table{border-collapse:collapse}"
       "th,td{border:1px solid #9FB3CF;padding:4px 6px;vertical-align:top}th{background:#E6F0FA}"
       "code{font-family:Consolas,monospace}")


def to_html(md_path: Path) -> str:
    body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=["tables", "sane_lists", "fenced_code"])
    return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", nargs="*"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    items = [s for s in SYNC if not a.only or s[0] in a.only]
    with tempfile.TemporaryDirectory() as tmp:
        for md, folder, title in items:
            h = Path(tmp) / f"{abs(hash(md))}.html"
            h.write_text(to_html(Path(md)), encoding="utf-8")
            dest = f"{REMOTE}/{folder + '/' if folder else ''}{title}.html"
            print(f"{md} -> {dest}", flush=True)
            if a.dry_run:
                continue
            r = subprocess.run(["rclone", "copyto", str(h), dest, "--drive-import-formats", "html",
                                "--drive-export-formats", "html", "--drive-allow-import-name-change", "-q"], capture_output=True, text=True)
            if r.returncode:
                print("  GAGAL:", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.returncode, file=sys.stderr)


if __name__ == "__main__":
    main()
