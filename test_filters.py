from mail.mock_reader import MockEmailReader
from mail.filters import is_relevant_email

reader = MockEmailReader()
reader.connect()

emails = reader.fetch_recent_headers(limit=5)

for e in emails:
    relevant, signals = is_relevant_email(e)
    print("-" * 50)
    print("SUBJECT:", e["subject"])
    print("RELEVANT:", relevant)
    print("SIGNALS:", signals)

reader.disconnect()
