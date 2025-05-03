# integrations/slack_notifier.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_alert(data):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not set!")
        return False

    message = {
        "text": f"*New high-quality lead*: {data['sender']} | Score: {data['score']}"
    }

    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("✅ Sent to Slack")
        return True
    else:
        print(f"❌ Failed to send to Slack: {response.text}")
        return False