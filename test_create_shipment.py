from storage.models import create_shipment
from storage.db import get_connection

# Find an existing order (Order 123)
conn = get_connection()
order = conn.execute(
    "SELECT * FROM orders WHERE order_ref = ?",
    ("123",)
).fetchone()
conn.close()

if not order:
    print("Order not found")
else:
    create_shipment(
        order_id=order["id"],
        courier="DHL",
        tracking_number="987654321"
    )
    print("Test shipment created for Order 123")
