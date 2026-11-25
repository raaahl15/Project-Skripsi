"""Illinois IDB-8103861: read well images from PARTS of a split zip (images_<plate>.zip.001 ... .0NN, 10 GB each).

The archive is one zip split into raw 10 GB byte pieces, so a single middle piece cannot be opened as a zip (its central
directory is in the last piece). This tool scans the piece(s) for zip LOCAL FILE HEADERS and recovers every member whose
data lies completely inside the given consecutive piece(s).

    list    : print every member found (name, well, compressed size, complete?) -> decide which pieces to download next
    process : for control wells only (column 1 = TNF, 2/23 = untreated, 24 = alsterpaullone) extract the .nd2 to a temp
              file, segment + track every frame (src/illinois_extract_demo.py: segment, track; k = 5), keep tracks complete
              over frames 4-75 (hours 1-19, the authors' window), compute the 9 per-cell features of src/pilot_illinois.py
              from OWN trajectories, write results/illinois-own/<plate>_<well>.csv, delete the temp .nd2.
              Wells already processed are skipped (rerun-safe). ~17 min per well on the laptop.

Usage:
    python -I src/illinois_zip_parts.py list    D:/.../images_DiversitySet3Plate2.zip.003 [more consecutive parts]
    python -I src/illinois_zip_parts.py process D:/.../images_DiversitySet3Plate2.zip.003 --plate DiversitySet3Plate2
"""
import argparse
import json
import re
import struct
import sys
import tempfile
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SIG = b"PK\x03\x04"
WELL_RE = re.compile(r"Well([A-P])(\d{1,2})_Seq(\d+)\.nd2$", re.I)
CONTROL = {1: "TNF", 2: "untreated", 23: "untreated", 24: "Alp"}
WIN_START, WIN_LEN = 4, 72  # frames 4-75 = hours 1-19 (best match to the authors' trajectories on the demo well)


class Parts:
    """Consecutive split-zip pieces read as one byte stream."""
    def __init__(self, paths):
        self.paths = [Path(p) for p in paths]
        self.sizes = [p.stat().st_size for p in self.paths]
        self.size = sum(self.sizes)
        self.fh = [open(p, "rb") for p in self.paths]

    def read(self, off, n):
        out = bytearray()
        for f, s in zip(self.fh, self.sizes):
            if off >= s:
                off -= s; continue
            f.seek(off); chunk = f.read(min(n - len(out), s - off)); out += chunk; off = 0
            if len(out) >= n:
                break
        return bytes(out)


def parse_header(p, off):
    h = p.read(off, 30)
    if len(h) < 30 or h[:4] != SIG:
        return None
    _, ver, flags, method, _, _, crc, csize, usize, nlen, xlen = struct.unpack("<4sHHHHHIIIHH", h)
    if method not in (0, 8) or not (0 < nlen < 400) or ver > 63:
        return None
    raw = p.read(off + 30, nlen + xlen)
    try:
        name = raw[:nlen].decode("utf-8")
    except UnicodeDecodeError:
        name = raw[:nlen].decode("cp437")
    if not name.isprintable() or not re.search(r"(\.\w{2,4}|/)$", name):
        return None
    extra = raw[nlen:]
    if csize == 0xFFFFFFFF or usize == 0xFFFFFFFF:  # zip64 extra field 0x0001: usize, csize (only the 0xFFFFFFFF ones)
        i = 0
        while i + 4 <= len(extra):
            hid, hl = struct.unpack("<HH", extra[i:i + 4]); body = extra[i + 4:i + 4 + hl]; j = 0
            if hid == 1:
                if usize == 0xFFFFFFFF and j + 8 <= len(body):
                    usize = struct.unpack("<Q", body[j:j + 8])[0]; j += 8
                if csize == 0xFFFFFFFF and j + 8 <= len(body):
                    csize = struct.unpack("<Q", body[j:j + 8])[0]
            i += 4 + hl
    known = not (flags & 8) and csize not in (0, 0xFFFFFFFF)
    data = off + 30 + nlen + xlen
    return {"name": name, "method": method, "csize": csize if known else None, "usize": usize if known else None,
            "header": off, "data": data}


def scan(p, chunk=64 << 20):
    entries, off = [], 0
    while off < p.size:
        buf = p.read(off, chunk + 3)
        i = buf.find(SIG)
        if i < 0:
            off += chunk; continue
        e = parse_header(p, off + i)
        if e is None:
            off += i + 1; continue
        e["complete"] = (e["data"] + e["csize"] <= p.size) if e["csize"] is not None else None
        entries.append(e)
        off = e["data"] + e["csize"] if e["csize"] is not None else e["data"]
    return entries


def extract(p, e, dest, chunk=16 << 20):
    """Decompress member e to dest; returns True if the whole member was inside the parts."""
    off, end = e["data"], (e["data"] + e["csize"]) if e["csize"] is not None else p.size
    d = zlib.decompressobj(-15) if e["method"] == 8 else None
    with open(dest, "wb") as out:
        while off < end:
            buf = p.read(off, min(chunk, end - off)); off += len(buf)
            if d is None:
                out.write(buf)
            else:
                out.write(d.decompress(buf))
                if d.eof:
                    return True
    return d is None and e["csize"] is not None and off >= end


def well_of(name):
    m = WELL_RE.search(name)
    return (m.group(1).upper(), int(m.group(2)), int(m.group(3))) if m else None


def cmd_list(p, a):
    ents = scan(p)
    for e in ents:
        w = well_of(e["name"])
        tag = f"{w[0]}{w[1]:02d} seq{w[2]:04d} {CONTROL.get(w[1], 'compound')}" if w else ""
        cs = f"{e['csize'] / 1e9:6.2f} GB" if e["csize"] is not None else "   ? GB"
        print(f"{'OK ' if e['complete'] else ('?  ' if e['complete'] is None else 'cut')} {cs}  {tag:28s} {e['name']}")
    wells = [well_of(e["name"]) for e in ents if well_of(e["name"])]
    if wells:
        print(f"\n{len(wells)} well files, seq {min(w[2] for w in wells)}-{max(w[2] for w in wells)}; "
              f"control wells: {[f'{w[0]}{w[1]:02d}' for w in wells if w[1] in CONTROL]}")


def cmd_process(p, a):
    import nd2
    import numpy as np
    import pandas as pd
    from src.illinois_extract_demo import segment, track
    from src.pilot_illinois import FEATS, features
    out_dir = Path(a.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(a.tmp_dir or tempfile.gettempdir()); tmp_dir.mkdir(parents=True, exist_ok=True)
    for e in scan(p):
        w = well_of(e["name"])
        if not w or (w[1] not in CONTROL and f"{w[0]}{w[1]:02d}" not in a.wells):
            continue
        well = f"{w[0]}{w[1]:02d}"; dest_csv = out_dir / f"{a.plate}_{well}.csv"
        if dest_csv.exists():
            print("skip (done)", well); continue
        nd2_path = tmp_dir / f"{a.plate}_{well}.nd2"; t0 = time.time()
        if not extract(p, e, nd2_path):
            print(f"skip {well}: member not complete in these parts"); nd2_path.unlink(missing_ok=True); continue
        try:
            f = nd2.ND2File(nd2_path); arr = f.to_dask()
            frames = [segment(arr[t].compute(), a.k)[0].reset_index(drop=True)
                      for t in range(WIN_START, min(WIN_START + WIN_LEN, arr.shape[0]))]
            f.close()
        finally:
            nd2_path.unlink(missing_ok=True)
        obj = track(frames)
        cnt = obj.groupby("track").frame.nunique()
        full = cnt[cnt == len(frames)].index
        piv = obj[obj.track.isin(full)].pivot_table(index="track", columns="frame", values="I_raw_mean")
        I = piv.to_numpy(float)
        feat = features(I, I)[FEATS] if len(I) else pd.DataFrame(columns=FEATS)
        feat.insert(0, "track", piv.index.to_numpy()); feat.insert(0, "condition", CONTROL.get(w[1], "compound"))
        feat.insert(0, "well", f"{a.plate}/{well}"); feat.insert(0, "plate", a.plate)
        feat.to_csv(dest_csv, index=False)
        print(f"{well} ({CONTROL.get(w[1], 'compound')}): {len(I)} complete tracks, {time.time() - t0:.0f}s", flush=True)
        log = out_dir / "process_log.jsonl"
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"plate": a.plate, "well": well, "seq": w[2], "n_tracks": int(len(I)), "k": a.k,
                                 "seconds": round(time.time() - t0)}) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "process"]); ap.add_argument("parts", nargs="+")
    ap.add_argument("--plate", default="DiversitySet3Plate2"); ap.add_argument("--k", type=float, default=5)
    ap.add_argument("--out-dir", default="results/illinois-own"); ap.add_argument("--wells", nargs="*", default=[], help="extra non-control wells, e.g. K16 (testing)"); ap.add_argument("--tmp-dir", default="data/raw/illinois-IDB-8103861/_tmp")
    a = ap.parse_args()
    p = Parts(a.parts)
    {"list": cmd_list, "process": cmd_process}[a.cmd](p, a)


if __name__ == "__main__":
    main()
