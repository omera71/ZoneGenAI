# Checklist Git Line Endings (Windows + GitHub)
# 1. Buat file .gitattributes di root repo
Isi standar:
-- Default semua file teks gunakan LF
* text=auto eol=lf

-- Source code
*.py    text eol=lf
*.ipynb text eol=lf
*.json  text eol=lf
*.yml   text eol=lf
*.yaml  text eol=lf
*.md    text eol=lf

-- Windows scripts
*.bat   text eol=crlf
*.cmd   text eol=crlf
*.ps1   text eol=crlf

-- Binary files
*.png   binary
*.jpg   binary
*.jpeg  binary
*.gif   binary
*.zip   binary
*.exe   binary
*.dll   binary



# 2. Set konfigurasi Git global
Jalankan sekali saja di Command Prompt/Git Bash:
git config --global core.autocrlf true


👉 Artinya:
- Saat commit → CRLF otomatis dikonversi ke LF (sesuai aturan repo).
- Saat checkout di Windows → LF otomatis dikonversi ke CRLF di working copy.

# 3. Normalisasi file (sekali per repo)
Kalau repo sudah ada file lama:
git rm --cached -r .
git add .
git commit -m "Normalize line endings via .gitattributes"
git push origin main



# 4. Workflow harian
- Commit & push seperti biasa (git add ., git commit, git push).
- Git akan otomatis jaga line endings sesuai aturan.
- Tidak perlu khawatir lagi soal CRLF vs LF.
