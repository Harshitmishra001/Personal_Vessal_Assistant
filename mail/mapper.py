from storage.db import get_connection


def find_vessel_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM vessels WHERE name = ? AND active = 1",
        (name,)
    ).fetchone()
    conn.close()
    return row


def find_order_by_ref(order_ref):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM orders WHERE order_ref = ?",
        (order_ref,)
    ).fetchone()
    conn.close()
    return row


def dry_run_map(extracted: dict):
    """
    Decide what DB actions WOULD happen.
    No DB writes allowed.
    """

    actions = []

    vessel_name = extracted.get("vessel_name")
    order_ref = extracted.get("order_ref")
    tracking = extracted.get("tracking_number")

    vessel = None
    order = None

    if vessel_name:
        vessel = find_vessel_by_name(vessel_name)
        if vessel:
            actions.append(f"FOUND vessel '{vessel_name}'")
        else:
            actions.append(f"WOULD CREATE vessel '{vessel_name}'")

    if order_ref:
        order = find_order_by_ref(order_ref)
        if order:
            actions.append(f"FOUND order '{order_ref}'")
        else:
            actions.append(f"WOULD CREATE order '{order_ref}'")

    if tracking:
        if order:
            actions.append(f"WOULD CREATE shipment with tracking '{tracking}'")
        else:
            actions.append(
                f"HOLD tracking '{tracking}' (no order linked yet)"
            )

    return actions

from datetime import datetime
from storage.models import (
    create_vessel,
    create_order,
    create_shipment,
    log_event
)


def apply_mapping(extracted: dict):
    """
    Apply mapping decisions to the database.
    This ENABLES DB writes.
    """

    actions = []

    vessel_name = extracted.get("vessel_name")
    order_ref = extracted.get("order_ref")
    tracking = extracted.get("tracking_number")

    vessel = None
    order = None

    # ----- VESSEL -----
    if vessel_name:
        vessel = find_vessel_by_name(vessel_name)
        if vessel:
            actions.append(f"FOUND vessel '{vessel_name}'")
        else:
            create_vessel(name=vessel_name)
            log_event("vessel", vessel_name, "CREATED")
            actions.append(f"CREATED vessel '{vessel_name}'")
            vessel = find_vessel_by_name(vessel_name)

    # ----- ORDER -----
    if order_ref:
        order = find_order_by_ref(order_ref)
        if order:
            actions.append(f"FOUND order '{order_ref}'")
        else:
            vessel_id = vessel["id"] if vessel else None
            create_order(
                vessel_id=vessel_id,
                supplier=None,
                item_summary=None,
                order_ref=order_ref
            )
            log_event("order", order_ref, "CREATED")
            actions.append(f"CREATED order '{order_ref}'")
            order = find_order_by_ref(order_ref)

    # ----- SHIPMENT -----
    if tracking:
        if order:
            create_shipment(
                order_id=order["id"],
                courier=None,
                tracking_number=tracking
            )
            log_event("shipment", tracking, "CREATED")
            actions.append(f"CREATED shipment '{tracking}'")
        else:
            actions.append(
                f"SKIPPED shipment '{tracking}' (no linked order)"
            )

    return actions
