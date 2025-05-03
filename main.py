# main.py - Email AI Agent Orchestrator

import logging
from datetime import datetime
from email_fetcher.fetcher import fetch_emails
from llm_processor.processor import classify_email, generate_reply, get_lead_score
from email_sender.sender import send_email
from email_sender.filters import should_auto_reply
from utils.contact_extractor import extract_phone_numbers, extract_whatsapp_numbers
from utils.url_utils import extract_social_media_links
from utils.database import save_processed_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_emails():
    logger.info("🚀 Starting Email AI Agent")

    for email_data in fetch_emails():
        body = email_data["body"]
        sender = email_data["sender"]

        # 🧠 Classification
        category = classify_email(body)

        # 📞 Contact Info Extraction
        phone_numbers = extract_phone_numbers(body)
        whatsapp_numbers = extract_whatsapp_numbers(phone_numbers)
        social_links = extract_social_media_links(body)

        # ⚖️ Lead Scoring
        lead_score = get_lead_score(body)

        # 🛑 Filter out unwanted emails
        if not should_auto_reply(category, sender, body):
            logger.info(f"🚫 Skipping {category} from {sender}")
            continue

        # 💬 Generate and send reply
        reply_text = generate_reply(body)
        send_email(
            subject=f"Re: {email_data['subject']}",
            recipient=sender,
            body=reply_text
        )

        # 📤 Save to DB
        save_processed_email({
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "subject": email_data["subject"],
            "body": body,
            "category": category,
            "lead_score": lead_score,
            "phone_numbers": phone_numbers,
            "whatsapp_numbers": whatsapp_numbers,
            "social_links": social_links,
            "reply_sent": bool(reply_text),
            "reply_text": reply_text
        })


if __name__ == "__main__":
    process_emails()