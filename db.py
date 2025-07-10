import sqlite3

def init_db():
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def update_score(user_id, username, delta):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO scores (user_id, username, score) VALUES (?, ?, 0)", (user_id, username))
    c.execute("UPDATE scores SET score = score + ? WHERE user_id = ?", (delta, user_id))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return results

def reset_leaderboard():
    conn = sqlite3.connect("quiz.db")
    c = conn.cursor()
    c.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
