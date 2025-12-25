import re

VESSEL_REGEX = re.compile(
    r'\b(MV|MT|VESSEL)\s+([A-Z][A-Z\s]{2,30})\b'
)

TRACKING_REGEX = re.compile(
    r'\b(?:tracking|awb)?\s*[:\-]?\s*(\d{6,15})\b',
    re.IGNORECASE
)

ORDER_REGEX = re.compile(
    r'\b(?:order|po)\s*#?\s*([A-Z0-9\-]+)\b',
    re.IGNORECASE
)


def extract_info(email_header: dict):
    subject = email_header.get("subject", "")

    vessel_match = VESSEL_REGEX.search(subject)
    tracking_match = TRACKING_REGEX.search(subject)
    order_match = ORDER_REGEX.search(subject)

    return {
        "vessel_name": (
            f"{vessel_match.group(1)} {vessel_match.group(2).strip()}"
            if vessel_match else None
        ),
        "tracking_number": tracking_match.group(1) if tracking_match else None,
        "order_ref": order_match.group(1) if order_match else None
    }
