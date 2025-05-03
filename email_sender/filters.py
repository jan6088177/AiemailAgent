def should_auto_reply(category, sender, body):
    if "noreply" in sender.lower() or "no-reply" in sender.lower():
        return False
    if category in ["Marketing / Newsletter", "Spam / Fraudulent"]:
        return False
    if "unsubscribe" in body.lower() or "click here" in body.lower():
        return False
    return True