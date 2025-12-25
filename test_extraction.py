from mail.mock_reader import MockEmailReader
from mail.filters import is_relevant_email
from mail.extractor import extract_info

reader = MockEmailReader()
reader.connect()

emails = reader.fetch_recent_headers(limit=5)

for e in emails:
    relevant, signals = is_relevant_email(e)
    if not relevant:
        continue

    extracted = extract_info(e)

    print("-" * 50)
    print("SUBJECT:", e["subject"])
    print("EXTRACTED:", extracted)

reader.disconnect()
