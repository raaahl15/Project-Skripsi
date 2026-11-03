# Setup di Laptop Baru / Laptop Lain

## 1. Install software
- [ ] **Git**: https://git-scm.com (di Windows sekaligus mendapat Git Bash)
- [ ] **Python 3.11 atau 3.12**: https://www.python.org/downloads/ (Windows: centang *Add python.exe to PATH*)
- [ ] **Node.js LTS**: https://nodejs.org (dibutuhkan Claude Code)
- [ ] **Antigravity** (editor)
- [ ] **Claude Code**: `npm install -g @anthropic-ai/claude-code`
- [ ] **LaTeX**: MiKTeX (Windows) atau TeX Live (Linux/macOS), pastikan `latexmk` dan `biber` tersedia.
      Opsional: cukup andalkan GitHub Actions untuk compile PDF.
- [ ] **rclone** (untuk data dari Drive): https://rclone.org/downloads/, lalu `rclone config` dengan remote bernama `gdrive`

## 2. Login akun
- GitHub (pakai `gh auth login` atau Git Credential Manager), Google, Claude.

## 3. Ambil repo & siapkan environment
```bash
git clone https://github.com/raaahl15/Project-Skripsi.git skripsi-ml
cd skripsi-ml
bash scripts/setup.sh                                          # Linux/macOS/Git Bash
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1     # Windows
```
> Jangan clone ke dalam folder yang disinkronkan Google Drive.

## 4. Ambil data dari Drive
```bash
rclone copy gdrive:Project-Skripsi/data ./data
```
Tanpa rclone: unduh manual dari Drive ke folder `data/`.

## 5. Mulai bekerja
- Buka folder di Antigravity, atau jalankan `claude` di terminal.
- Baca `docs/STATUS.md` terlebih dahulu.

---

## Khusus: memakai laptop/komputer TEMAN (sementara)

Utamakan cara **tanpa menyimpan kredensial**:
1. **Paling aman:** pakai browser saja, yaitu `github.dev` (tekan `.` di repo) atau claude.ai/code. Gunakan jendela private/incognito.
2. Jika harus clone dan menjalankan kode:
   - Gunakan akun/profil Windows terpisah kalau memungkinkan.
   - Login GitHub via browser (Git Credential Manager); **jangan** simpan token di file.
   - Jangan isi `.env` dengan API key di laptop teman.
3. **Setelah selesai** (wajib):
   - Commit & push semua pekerjaan.
   - Logout dari GitHub, Google, dan Claude di browser.
   - Hapus kredensial Git: Windows, buka *Credential Manager* lalu *Windows Credentials* dan hapus entri `git:https://github.com`.
   - Logout Claude Code: `claude` lalu `/logout`.
   - Hapus folder repo dan folder `data/` jika tidak diperlukan lagi.
