import json
from datetime import datetime
import pandas as pd

def save_processed_email(data):
    data["timestamp"] = datetime.now().isoformat()
    with open("processed_emails.json", "a") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

def export_to_csv(filename="leads_export.csv"):
    df = pd.read_json("processed_emails.json", lines=True)
    df.to_csv(filename, index=False)
    print(f"✅ Exported {len(df)} leads to {filename}")