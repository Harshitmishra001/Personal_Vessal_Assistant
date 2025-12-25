from tracking.mock_dhl import MockDHLTracker
from storage.models import (
    get_shipments_pending,
    update_shipment_status,
    log_event
)

def sync_shipments():
    tracker = MockDHLTracker()
    shipments = get_shipments_pending()

    if not shipments:
        print("[TRACKING] No pending shipments")
        return

    for s in shipments:
        tracking_number = s["tracking_number"]

        status_data = tracker.get_status(tracking_number)
        eta = tracker.get_eta(tracking_number)

        delivered = status_data["status"].lower() == "delivered"

        update_shipment_status(
            shipment_id=s["id"],
            status=status_data["status"],
            location=status_data["location"],
            eta=eta,
            delivered=delivered
        )

        log_event(
            entity_type="shipment",
            entity_id=s["id"],
            event_type="UPDATED"
        )

        print(
            f"[TRACKING] Updated {tracking_number} → "
            f"{status_data['status']}"
        )
