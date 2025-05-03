# sender.py - Sends automated replies using Gmail SMTP

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config_loader import load_env_vars
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load email credentials from .env
try:
    EMAIL_USER = load_env_vars("EMAIL_USER")
    EMAIL_PASSWORD = load_env_vars("EMAIL_PASSWORD")
except ValueError as e:
    logger.error(f"⚠️ Missing environment variable: {e}")
    raise SystemExit("Please check your .env file — missing required credentials")


def send_email(subject, recipient, body):
    """
    Sends an email to the specified recipient.

    Args:
        subject (str): Subject line of the email.
        recipient (str): Email address to send to.
        body (str): Content of the email.

    Returns:
        bool: True if email was sent successfully, False otherwise.
    """
    # Skip noreply or no-reply addresses
    if "noreply" in recipient.lower() or "no-reply" in recipient.lower():
        logger.warning(f"🚫 Skipping noreply address: {recipient}")
        return False

    try:
        # Create message container
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = subject

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail's SMTP server
        logger.info(f"📧 Connecting to SMTP server...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        # Send email
        server.sendmail(EMAIL_USER, recipient, msg.as_string())
        logger.info(f"✅ Reply sent to {recipient}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to send reply: {e}")
        return False

    finally:
        try:
            server.quit()
        except:
            pass


def generate_auto_reply_template(name="Sender"):
    """
    Generates a standardized auto-reply email with contact info.

    Args:
        name (str): Name of the sender (optional).

    Returns:
        str: The formatted auto-reply message.
    """
    return f"""
Thank you for your message.

This is an automated response from the Email AI Agent.

For more information about this project or to view the source code, please visit:
🔗 https://github.com/jan6088177/AiemailAgent

For direct support or inquiries, feel free to reach out via:

📧 Email: khan6088177@gmail.com  
📱 WhatsApp: +92 343 6088177

Best regards,  
KHAN
""".strip()


# For testing only
if __name__ == "__main__":
    test_body = generate_auto_reply_template(name="John Doe")
    print(test_body)