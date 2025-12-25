import imaplib
import email
from email.header import decode_header


class OutlookEmailReader:
    def __init__(self, username, app_password):
        self.host = "outlook.office365.com"
        self.username = username
        self.password = app_password
        self.conn = None

    def connect(self):
        self.conn = imaplib.IMAP4_SSL(self.host)
        self.conn.login(self.username, self.password)
        self.conn.select("INBOX")

    def fetch_recent_headers(self, limit=5):
        status, messages = self.conn.search(None, "ALL")
        if status != "OK":
            return []

        email_ids = messages[0].split()[-limit:]
        headers = []

        for eid in email_ids:
            status, msg_data = self.conn.fetch(eid, "(BODY.PEEK[HEADER])")
            if status != "OK":
                continue

            msg = email.message_from_bytes(msg_data[0][1])

            subject, encoding = decode_header(msg.get("Subject", ""))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            headers.append({
                "from": msg.get("From"),
                "subject": subject,
                "date": msg.get("Date")
            })

        return headers

    def disconnect(self):
        if self.conn:
            self.conn.logout()
