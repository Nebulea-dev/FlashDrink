import sqlite3

conn = sqlite3.connect('payment_system.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    balance REAL DEFAULT 0
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id TEXT UNIQUE NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
conn.commit()
conn.close()
