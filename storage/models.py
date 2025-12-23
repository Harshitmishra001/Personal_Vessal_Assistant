from datetime import datetime
from storage.db import get_connection
from config.settings import APP_VERSION

def initialize_app_meta():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM app_meta WHERE id = 1")
    row = cursor.fetchone()

    now = datetime.utcnow().isoformat()

    if row is None:
        cursor.execute("""
        INSERT INTO app_meta (id, version, created_at, last_run)
        VALUES (1, ?, ?, ?)
        """, (APP_VERSION, now, now))
        print(f"[PVA] First run recorded at {now}")
    else:
        cursor.execute("""
        UPDATE app_meta
        SET last_run = ?, version = ?
        WHERE id = 1
        """, (now, APP_VERSION))
        print(f"[PVA] last_run updated from {row['last_run']} → {now}")

    conn.commit()
    conn.close()
