from mail.outlook_reader import OutlookEmailReader

reader = OutlookEmailReader(
    username="HIS_EMAIL@domain.com",
    app_password="APP_PASSWORD_HERE"
)

reader.connect()
emails = reader.fetch_recent_headers(limit=3)

for e in emails:
    print(e)

reader.disconnect()
