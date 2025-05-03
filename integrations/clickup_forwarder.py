import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

def forward_to_clickup(email_data):
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_TOKEN,
        "Content-Type": "application/json"
    }

    lead_score = email_data.get("lead_score", 0)

    if lead_score >= 9:
        priority = 1
        due_date = int((datetime.now() + timedelta(days=1)).timestamp() * 1000)
    elif lead_score >= 7:
        priority = 2
        due_date = int((datetime.now() + timedelta(days=3)).timestamp() * 1000)
    elif lead_score >= 5:
        priority = 3
        due_date = int((datetime.now() + timedelta(days=7)).timestamp() * 1000)
    else:
        return False

    payload = {
        "name": f"Lead: {email_data['sender']}",
        "description": f"""
        Subject: {email_data['subject']}
        Body: {email_data['body'][:500]}...

        Phone Numbers: {', '.join([p['number'] for p in email_data.get('phone_numbers', [])])}
        WhatsApp: {', '.join(email_data.get('whatsapp_numbers', []))}
        Social Links: {', '.join(email_data.get('social_links', []))}

        Score: {lead_score}
        """,
        "status": "New",
        "priority": priority,
        "due_date": due_date,
        "tags": ["ai_lead", "auto-import"],
        "custom_fields": [
            {"id": "lead_source", "value": "Email AI Agent"},
            {"id": "lead_score", "value": str(lead_score)},
            {"id": "contact_email", "value": email_data["sender"]}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("✅ Sent to ClickUp")
        return True
    else:
        print(f"❌ Failed to send to ClickUp: {response.status_code} - {response.text}")
        return False