"""Pilot step for the CyTOF component: inventory of the Luo FCS files (events per file, marker panel).

Usage:
    python src/pilot_luo_inspect.py --root data/raw/dryad-luo-2023 --out results/pilot-luo
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import flowio
import pandas as pd

from src.data.luo_cytof import FNAME_RE, channel_table


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/raw/dryad-luo-2023")
    ap.add_argument("--out", default="results/pilot-luo")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    files = sorted(Path(args.root).rglob("*.fcs"))
    if not files:
        sys.exit(f"No FCS files under {args.root} (unzip the Dryad download there first)")
    inv = []
    for p in files:
        m = FNAME_RE.search(p.name)
        f = flowio.FlowData(str(p))
        inv.append({"file": p.name, "donor": m.group(1) if m else "?", "culture": m.group(2) if m else "?",
                    "events": f.event_count, "channels": f.channel_count})
    inv = pd.DataFrame(inv)
    inv.to_csv(out / "inventory.csv", index=False)
    # marker panel per file -> markers shared by ALL files (needed to pool donors)
    panels = {p.name: set(channel_table(p).marker) for p in files}
    common = sorted(set.intersection(*panels.values()))
    allm = sorted(set.union(*panels.values()))
    pd.DataFrame({"marker": allm, "in_all_files": [m in common for m in allm],
                  "n_files": [sum(m in s for s in panels.values()) for m in allm]}).to_csv(out / "panel.csv", index=False)
    print(inv.to_string(index=False))
    print(f"\nTotal events: {inv.events.sum():,} | files: {len(inv)}")
    print(f"\nMarkers present in ALL files ({len(common)}):", ", ".join(common))
    print(f"\nMarkers missing in some files ({len(allm) - len(common)}):", ", ".join(m for m in allm if m not in common))


if __name__ == "__main__":
    main()
