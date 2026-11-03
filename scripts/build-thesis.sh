#!/usr/bin/env bash
# Build thesis PDF with latexmk (requires TeX Live/MiKTeX with biber).
set -e
cd "$(dirname "$0")/../thesis"
latexmk -pdf -interaction=nonstopmode -outdir=build main.tex
echo "PDF: thesis/build/main.pdf"
