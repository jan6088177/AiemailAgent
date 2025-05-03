import imaplib
import email
from email.header import decode_header
from utils.config_loader import load_env_vars
import logging

logger = logging.getLogger(__name__)

def fetch_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        EMAIL_USER = load_env_vars("EMAIL_USER")
        EMAIL_PASSWORD = load_env_vars("EMAIL_PASSWORD")

        logger.info(f"🔐 Logging in as {EMAIL_USER}...")
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("inbox")

        _, data = mail.search(None, "UNSEEN")
        if data[0]:
            logger.info("📬 Found unread emails. Processing...")

        for num in data[0].split():
            _, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    yield {
                        "id": num,
                        "sender": msg["From"],
                        "subject": decode_header(msg["Subject"])[0][0],
                        "body": extract_body(msg)
                    }

        mail.logout()
    except Exception as e:
        logger.error(f"⚠️ Error fetching emails: {e}")


def extract_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode()
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode()
    return body.strip()