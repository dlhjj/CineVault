
import sqlite3

DB_NAME = 'cinevault.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre TEXT,
        rating REAL,
        watched INTEGER
    )
    ''')

    conn.commit()
    conn.close()
