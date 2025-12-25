from datetime import datetime
from storage.db import get_connection

# ---------- VESSELS ----------
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

def create_vessel(name, departure_date=None, notes=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO vessels (name, departure_date, notes, created_at)
    VALUES (?, ?, ?, ?)
    """, (name, departure_date, notes, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()


def list_active_vessels():
    conn = get_connection()
    cursor = conn.cursor()
    vessels = cursor.execute(
        "SELECT * FROM vessels WHERE active = 1"
    ).fetchall()
    conn.close()
    return vessels


# ---------- ORDERS ----------

def create_order(vessel_id, supplier, item_summary, order_ref, status="CREATED"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders (vessel_id, supplier, item_summary, order_ref, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (vessel_id, supplier, item_summary, order_ref, status, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()


# ---------- SHIPMENTS ----------

def create_shipment(order_id, courier, tracking_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO shipments (order_id, courier, tracking_number, delivered)
    VALUES (?, ?, ?, 0)
    """, (order_id, courier, tracking_number))

    conn.commit()
    conn.close()


# ---------- EVENTS ----------

def log_event(entity_type, entity_id, event_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events (entity_type, entity_id, event_type, created_at)
    VALUES (?, ?, ?, ?)
    """, (entity_type, entity_id, event_type, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

def get_shipments_pending():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("""
        SELECT * FROM shipments
        WHERE delivered = 0
    """).fetchall()
    conn.close()
    return rows


def update_shipment_status(
    shipment_id,
    status,
    location,
    eta,
    delivered=False
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE shipments
        SET last_status = ?,
            last_location = ?,
            eta = ?,
            delivered = ?,
            last_checked = ?
        WHERE id = ?
    """, (
        status,
        location,
        eta,
        1 if delivered else 0,
        __import__("datetime").datetime.utcnow().isoformat(),
        shipment_id
    ))

    conn.commit()
    conn.close()

def get_vessel_by_id(vessel_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM vessels WHERE id = ?",
        (vessel_id,)
    ).fetchone()
    conn.close()
    return row
