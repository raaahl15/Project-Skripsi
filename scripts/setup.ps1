# Windows PowerShell setup. Run from anywhere:
#   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "Python not found. Install Python 3.11/3.12 from python.org (tick 'Add to PATH')." }
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

New-Item -ItemType Directory -Force -Path data, results | Out-Null
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Selesai. Ambil data: rclone copy gdrive:Project-Skripsi/data ./data"
