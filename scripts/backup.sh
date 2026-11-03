#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
F=~/skripsi-backup-$(date +%F).bundle
git bundle create "$F" --all
if command -v rclone >/dev/null 2>&1; then
  rclone copy "$F" gdrive:Project-Skripsi/backup/
  echo "Backup terkirim ke Drive: $F"
else
  echo "rclone tidak ada. Upload manual $F ke Drive Project-Skripsi/backup/"
fi
