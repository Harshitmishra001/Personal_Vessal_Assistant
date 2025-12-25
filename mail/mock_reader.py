from datetime import datetime

class MockEmailReader:
    """
    Offline test reader.
    Simulates Outlook email headers.
    """

    def connect(self):
        print("[MOCK] Connected to mock inbox")

    def fetch_recent_headers(self, limit=5):
        return [
            {
                "from": "supplier@vendor.com",
                "subject": "Shipment Confirmation – Order 123 – MV SEA STAR",
                "date": datetime.utcnow().isoformat()
            },
            {
                "from": "ops@company.com",
                "subject": "Urgent: Spare Parts Required for MV OCEAN QUEEN",
                "date": datetime.utcnow().isoformat()
            },
            {
                "from": "dhl@dhl.com",
                "subject": "DHL Tracking Update: 987654321",
                "date": datetime.utcnow().isoformat()
            }
        ][:limit]

    def disconnect(self):
        print("[MOCK] Disconnected")
