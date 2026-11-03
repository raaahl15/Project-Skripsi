# Build thesis PDF on Windows (MiKTeX/TeX Live) -> thesis\build\main.pdf
#   powershell -ExecutionPolicy Bypass -File scripts\build-thesis.ps1
# Runs the same sequence latexmk uses in CI (pdflatex, bibtex, makeindex for nomencl, pdflatex x2)
# without needing Perl (MiKTeX's latexmk requires Perl).
# Not "Stop": in Windows PowerShell 5.1 native tools writing to stderr (makeindex banner,
# MiKTeX update notice) would abort the script. Failures are detected via $LASTEXITCODE + throw.
$ErrorActionPreference = "Continue"
Set-Location (Join-Path $PSScriptRoot "..\thesis")

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw "pdflatex not found. Install MiKTeX (winget install -e --id MiKTeX.MiKTeX --scope user) or rely on GitHub Actions."
}
New-Item -ItemType Directory -Force build | Out-Null
$opts = @('-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-output-directory=build', 'main.tex')

function Invoke-PdfLatex {
    pdflatex @opts 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Select-String -Path build\main.log -Pattern '^!|\.tex:\d+:' -Context 0, 6 | Select-Object -First 3 | ForEach-Object { $_.ToString() }
        throw "pdflatex failed - see thesis\build\main.log"
    }
}

Invoke-PdfLatex
if (Select-String -Path build\main.aux -Pattern '\\bibdata' -Quiet) {
    bibtex build/main 2>&1 | Out-Null  # finds refs.bib and skripsi.bst in thesis\
    if ($LASTEXITCODE -ne 0) { Get-Content build\main.blg -Tail 20; throw "bibtex failed - see thesis\build\main.blg" }
}
if (Test-Path build\main.nlo) {
    makeindex build/main.nlo -s nomencl.ist -o build/main.nls 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "makeindex failed - see thesis\build\main.ilg" }
}
Invoke-PdfLatex
Invoke-PdfLatex

$pages = ([regex]::Match((Get-Content build\main.log -Raw), '\(\s*(\d+)\s+pages')).Groups[1].Value
Write-Host "PDF: thesis\build\main.pdf ($pages halaman)"
