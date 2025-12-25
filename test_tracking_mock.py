from tracking.mock_dhl import MockDHLTracker

tracker = MockDHLTracker()

tracking_number = "987654321"

status = tracker.get_status(tracking_number)
eta = tracker.get_eta(tracking_number)

print("STATUS:", status)
print("ETA:", eta)

delayed = tracker.is_delayed(status["timestamp"])
print("DELAYED:", delayed)
