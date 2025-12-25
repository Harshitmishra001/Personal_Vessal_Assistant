from datetime import datetime, timedelta

RISK_LEVELS = {
    "OK": "🟢",
    "ATTENTION": "🟡",
    "CRITICAL": "🔴"
}

RISKY_STATUSES = [
    "customs",
    "held",
    "exception"
]


def evaluate_shipment_risk(shipment, vessel=None):
    """
    Evaluate risk for a single shipment.

    shipment: row from shipments table
    vessel: row from vessels table (optional)
    """

    reasons = []
    risk = "OK"

    now = datetime.utcnow()

    # ----- Stagnation Risk -----
    if shipment["last_checked"]:
        last = datetime.fromisoformat(shipment["last_checked"])
        if now - last > timedelta(hours=24):
            risk = "ATTENTION"
            reasons.append("No tracking update in 24+ hours")

    # ----- Status Risk -----
    status = (shipment["last_status"] or "").lower()
    for kw in RISKY_STATUSES:
        if kw in status:
            risk = "ATTENTION"
            reasons.append(f"Risky status: {shipment['last_status']}")
            break

    # ----- Schedule Risk -----
    if vessel and shipment["eta"] and vessel["departure_date"]:
        eta = datetime.fromisoformat(shipment["eta"])
        departure = datetime.fromisoformat(vessel["departure_date"])
        if eta > departure:
            risk = "CRITICAL"
            reasons.append("ETA is after vessel departure")

    return {
        "risk": risk,
        "icon": RISK_LEVELS[risk],
        "reasons": reasons
    }
