from mail.mock_reader import MockEmailReader

reader = MockEmailReader()
reader.connect()

emails = reader.fetch_recent_headers(limit=3)

for e in emails:
    print(e)

reader.disconnect()
