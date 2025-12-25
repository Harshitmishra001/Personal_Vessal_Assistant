from storage.models import get_shipments_pending, get_vessel_by_id
from risk.evaluator import evaluate_shipment_risk

shipments = get_shipments_pending()

for s in shipments:
    vessel = None
    if s["order_id"]:
        # get vessel via order
        from storage.db import get_connection
        conn = get_connection()
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ?",
            (s["order_id"],)
        ).fetchone()
        conn.close()

        if order:
            vessel = get_vessel_by_id(order["vessel_id"])

    risk = evaluate_shipment_risk(s, vessel)

    print("-" * 50)
    print("Tracking:", s["tracking_number"])
    print("Risk:", risk["icon"], risk["risk"])
    for r in risk["reasons"]:
        print("•", r)
