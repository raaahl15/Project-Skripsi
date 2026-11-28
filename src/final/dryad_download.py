"""Download Essig experiment zips from Dryad (doi:10.5061/dryad.ht76hdrk7) straight into Google Drive (Colab).

Dryad file downloads need an API account: create one at https://datadryad.org (log in -> "My account" -> API),
then store the client id/secret in Colab Secrets as DRYAD_CLIENT_ID / DRYAD_CLIENT_SECRET.
Not yet tested end-to-end (28 Nov 2026); if it fails, download in the browser and upload the zip to Drive data/raw/.

Usage: python -m src.final.dryad_download --files exp3.zip exp4.zip --dest /content/drive/MyDrive/Project-Skripsi/data/raw
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.parse
from pathlib import Path

import requests

BASE = "https://datadryad.org"
DOI = "doi:10.5061/dryad.ht76hdrk7"


def token(cid, secret):
    r = requests.post(f"{BASE}/oauth/token", data={"grant_type": "client_credentials", "client_id": cid,
                                                   "client_secret": secret}, timeout=60)
    r.raise_for_status()
    return r.json()["access_token"]


def list_files(session):
    ds = urllib.parse.quote(DOI, safe="")
    v = session.get(f"{BASE}/api/v2/datasets/{ds}/versions", timeout=60); v.raise_for_status()
    versions = v.json()["_embedded"]["stash:versions"]
    files_href = versions[-1]["_links"]["stash:files"]["href"]
    out, url = {}, BASE + files_href
    while url:
        r = session.get(url, timeout=60); r.raise_for_status(); j = r.json()
        for f in j["_embedded"]["stash:files"]:
            out[f["path"]] = (BASE + f["_links"]["stash:download"]["href"], f.get("size"))
        nxt = j.get("_links", {}).get("next")
        url = BASE + nxt["href"] if nxt else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--dest", required=True)
    a = ap.parse_args()
    cid, secret = os.environ.get("DRYAD_CLIENT_ID"), os.environ.get("DRYAD_CLIENT_SECRET")
    s = requests.Session()
    if cid and secret:
        s.headers["Authorization"] = f"Bearer {token(cid, secret)}"
    files = list_files(s)
    print("files in dataset:", {k: v[1] for k, v in files.items()})
    dest = Path(a.dest); dest.mkdir(parents=True, exist_ok=True)
    for name in a.files:
        if name not in files:
            sys.exit(f"{name} not found in the Dryad file list")
        url, size = files[name]
        target = dest / name
        if target.exists() and size and target.stat().st_size == size:
            print(f"{name}: already complete in Drive"); continue
        part = target.with_suffix(target.suffix + ".part")
        done = part.stat().st_size if part.exists() else 0
        hdr = {"Range": f"bytes={done}-"} if done else {}
        with s.get(url, headers=hdr, stream=True, timeout=120, allow_redirects=True) as r:
            r.raise_for_status()
            mode = "ab" if done and r.status_code == 206 else "wb"
            with open(part, mode) as fh:
                for i, chunk in enumerate(r.iter_content(chunk_size=8 << 20)):
                    fh.write(chunk)
                    if i % 128 == 0:
                        print(f"  {name}: {part.stat().st_size / 2**30:.1f} GiB", flush=True)
        part.rename(target)
        print(f"{name}: done ({target.stat().st_size / 2**30:.1f} GiB)")


if __name__ == "__main__":
    main()
