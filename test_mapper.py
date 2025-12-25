from mail.mock_reader import MockEmailReader
from mail.filters import is_relevant_email
from mail.extractor import extract_info
from mail.mapper import dry_run_map

reader = MockEmailReader()
reader.connect()

emails = reader.fetch_recent_headers(limit=5)

for e in emails:
    relevant, _ = is_relevant_email(e)
    if not relevant:
        continue

    extracted = extract_info(e)
    actions = dry_run_map(extracted)

    print("-" * 50)
    print("SUBJECT:", e["subject"])
    for a in actions:
        print("→", a)

reader.disconnect()
