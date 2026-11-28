"""Download open-access full texts from Europe PMC and save as plain text."""
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

PAPERS = {
    "elfimov2025ifchiv": "PMC11858172",
    "blasi2016labelfree": "PMC4729834",
    "shetab2023scifai": "PMC10689847",
    "lu2021latency": "PMC7980449",
    "rey2021temnet": "PMC8554174",
    "shao2024hivtarget": "PMC10806185",
    "hennig2017ifcml": "PMC5231320",
    "doan2020leukemia": "PMC7213640",
    "eulenberg2017deep": "PMC5587733",
}

for key, pmcid in PAPERS.items():
    dest = OUT / f"{key}.txt"
    if dest.exists():
        print("skip", key)
        continue
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "research-reading-script/1.0"})
        with urllib.request.urlopen(req, timeout=90) as r:
            xml = r.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        print("FAIL", key, exc)
        continue
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    dest.write_text(text, encoding="utf-8")
    print("ok", key, len(text))
