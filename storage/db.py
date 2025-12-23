import sqlite3
from config.settings import DB_PATH, DATA_DIR

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_meta (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        version TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_run TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
