import re

# keywords grouped by intent
COURIER_KEYWORDS = [
    "dhl", "tracking", "shipment", "awb", "dispatch"
]

SUPPLY_KEYWORDS = [
    "order", "spare", "supply", "required", "parts"
]

VESSEL_KEYWORDS = [
    "mv ", "mt ", "vessel", "ship"
]


def is_relevant_email(email_header: dict):
    """
    Decide whether an email is relevant to vessel logistics.

    Returns:
        (bool, list[str]) → (is_relevant, matched_signals)
    """

    subject = (email_header.get("subject") or "").lower()
    sender = (email_header.get("from") or "").lower()

    matched = []

    def match_keywords(keywords, source, label):
        for kw in keywords:
            if kw in source:
                matched.append(label)
                return True
        return False

    match_keywords(COURIER_KEYWORDS, subject + sender, "COURIER")
    match_keywords(SUPPLY_KEYWORDS, subject, "SUPPLY")
    match_keywords(VESSEL_KEYWORDS, subject, "VESSEL")

    return (len(matched) > 0), matched
