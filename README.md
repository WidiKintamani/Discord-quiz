# 🎮 Discord Quiz Bot (Slash Command + Button UI)

Bot Discord kuis dengan tema **anime**, memiliki **UI tombol A/B/C/D persis seperti tampilan Discord**, dan menggunakan **slash command modern** (`/kuis`, `/leaderboard`, `/reset`). Dibangun dengan Python dan `discord.py`.

---

## ✨ Fitur

- 📚 20 Soal kuis bertema anime (editable lewat `quiz_data.json`)
- 🔘 UI tombol pilihan A–D (Discord button interface)
- ⏱️ Timer otomatis per soal (20 detik)
- ✅ Evaluasi jawaban + skor per soal
- 🏆 Leaderboard real-time
- 🧼 Fitur reset leaderboard (khusus admin)
- ⚙️ Token disimpan aman di `.env`

---

## 📂 Struktur Project

discord_quiz_bot/
├── bot.py              # Main logic bot  
├── db.py               # Database handling (SQLite)  
├── quiz_data.json      # Soal kuis (tema anime)  
├── .env                # Token bot (jangan upload!)  
├── .gitignore  
├── requirements.txt    # Python dependencies  
└── README.md           # Dokumentasi ini

INSTALASI:

python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate.bat      # Windows

pip install -r requirements.txt

