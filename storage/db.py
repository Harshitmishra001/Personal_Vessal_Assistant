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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vessels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        departure_date TEXT,
        notes TEXT,
        created_at TEXT NOT NULL,
        active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vessel_id INTEGER NOT NULL,
        supplier TEXT,
        item_summary TEXT,
        order_ref TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (vessel_id) REFERENCES vessels(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        courier TEXT,
        tracking_number TEXT,
        last_status TEXT,
        last_location TEXT,
        eta TEXT,
        delivered INTEGER DEFAULT 0,
        last_checked TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
