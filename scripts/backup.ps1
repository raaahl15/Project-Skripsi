# Weekly backup: git bundle -> Google Drive (via rclone if available).
#   powershell -ExecutionPolicy Bypass -File scripts\backup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$F = Join-Path $HOME ("skripsi-backup-{0}.bundle" -f (Get-Date -Format "yyyy-MM-dd"))
git bundle create $F --all
if ($LASTEXITCODE -ne 0) { throw "git bundle failed." }

if (Get-Command rclone -ErrorAction SilentlyContinue) {
    rclone copy $F gdrive:Project-Skripsi/backup/
    Write-Host "Backup terkirim ke Drive: $F"
} else {
    Write-Host "rclone tidak ada. Upload manual $F ke Drive Project-Skripsi/backup/"
}
