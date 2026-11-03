#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
$PY -m venv .venv
if [ -f .venv/bin/activate ]; then source .venv/bin/activate; else source .venv/Scripts/activate; fi
pip install -r requirements.txt
mkdir -p data results
[ -f .env ] || cp .env.example .env
echo "Selesai. Ambil data: rclone copy gdrive:Skripsi-ML/data ./data"
