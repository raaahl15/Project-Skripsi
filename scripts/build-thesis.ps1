# Build thesis PDF with latexmk (requires MiKTeX/TeX Live with biber).
#   powershell -ExecutionPolicy Bypass -File scripts\build-thesis.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\thesis")

if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw "latexmk not found. Install MiKTeX (https://miktex.org) or rely on GitHub Actions to build the PDF."
}
latexmk -pdf -interaction=nonstopmode -outdir=build main.tex
Write-Host "PDF: thesis\build\main.pdf"
