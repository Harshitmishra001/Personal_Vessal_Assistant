from datetime import datetime, timedelta
import random

class MockDHLTracker:
    """
    Offline mock for DHL tracking.
    Simulates realistic shipment behavior.
    """

    STATUSES = [
        "Shipment picked up",
        "In transit",
        "Arrived at facility",
        "Customs clearance in progress",
        "Out for delivery",
        "Delivered"
    ]

    def get_status(self, tracking_number: str):
        status = random.choice(self.STATUSES[:-1])
        return {
            "tracking_number": tracking_number,
            "courier": "DHL",
            "status": status,
            "location": "Transit Hub",
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_eta(self, tracking_number: str):
        eta = datetime.utcnow() + timedelta(days=random.randint(1, 5))
        return eta.isoformat()

    def is_delayed(self, last_update_time: str, threshold_hours=24):
        last = datetime.fromisoformat(last_update_time)
        delta = datetime.utcnow() - last
        return delta.total_seconds() > threshold_hours * 3600
