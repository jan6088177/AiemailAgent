# 📨 Email AI Agent

An automated email classifier, responder, and lead scorer using **Mistral AI** via OpenRouter.

This project allows you to:
- 🧠 Classify incoming emails into categories
- 🤖 Generate auto-replies using LLMs
- ⚖️ Score leads based on content
- 📊 View processed emails in a Streamlit dashboard

---

## 🚀 Getting Started

To run this agent locally:

### 1. Clone the repo

```bash
git clone https://github.com/jan6088177/AiemailAgent.git
cd AiemailAgent
```

### 2. Set up virtual environment (optional but recommended)

```bash
python -m venv aiemail
.\aiemail\Scripts\activate   # On Windows
# or source aiemail/bin/activate on Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure these packages are installed:
- `streamlit`
- `pandas`
- `requests`
- `pyyaml`
- `python-dotenv`
- `imaplib2`
- `phonenumbers`
- `tldextract`
- `urlextract`
- `matplotlib` (for dashboard)
- `clickupapi` (optional, if re-enabling ClickUp integration)

### 4. Configure your `.env` file

Create a `.env` file with your credentials:

```
EMAIL_USER=khan6088177@gmail.com
EMAIL_PASSWORD=your_app_password_here
OPENROUTER_API_KEY=your_openrouter_key_here
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
ADMIN_EMAIL=admin@example.com
```

> ⚠️ Never commit real credentials — add `.env` to `.gitignore`.

---

## 📦 Features

- ✉️ Auto-classifies emails: Sales, Support, Spam, etc.
- 📞 Extracts phone numbers and WhatsApp info
- 🔗 Detects social media links
- 📈 Lead scoring system using Mistral AI
- 📊 Interactive dashboard with export capability

---

## 🧪 Run the Agent

```bash
python main.py
```

This will fetch unread emails from your inbox and process them.

---

## 📊 View Dashboard

Open another terminal (or tab) and run:

```bash
streamlit run dashboard/dashboard.py
```

You'll see a live view of all processed emails.

---

## 🛡️ Commercial License

This software is protected by copyright and is not open source.  
Unauthorized redistribution or commercial use is prohibited.

A copy of the license can be found in the `LICENSE` file.

If you'd like a customized version for your business or team, please [contact me](mailto:khan6088177@gmail.com).

---

## 🧰 Requirements

Ensure you have:
- Python ≥ 3.9
- Git
- A Gmail account with IMAP enabled
- An API key from [OpenRouter.ai](https://openrouter.ai)

---

## 📋 Sample `.env` File

```env
EMAIL_USER=khan6088177@gmail.com
EMAIL_PASSWORD=your_app_password_here
OPENROUTER_API_KEY=your_openrouter_api_key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
ADMIN_EMAIL=admin@example.com
```

> ⚠️ Don't commit your real `.env` file.

---

## 📁 Folder Structure

```
AiemailAgent/
│
├── LICENSE
├── README.md
├── main.py
├── .env.example
├── pyrightconfig.json
├── .cspell.json
├── requirements.txt
│
├── email_fetcher/
│   ├── fetcher.py
│   └── parser.py
│
├── llm_processor/
│   ├── processor.py
│   └── prompts.yaml
│
├── email_sender/
│   ├── sender.py
│   └── filters.py
│
├── utils/
│   ├── database.py
│   ├── contact_extractor.py
│   └── url_utils.py
│
└── dashboard/
    └── dashboard.py
```

---

## 📌 Contributing

Contributions are welcome! If you’d like to improve the agent or help fix issues, feel free to submit pull requests.

---

## 📬 Want a Customized Version?

I'm happy to provide:
- White-label versions
- Integration with your CRM
- Login/authentication
- Hosting and deployment support

📧 Contact: khan6088177@gmail.com  
🔗 Project Source: [GitHub Repo](https://github.com/jan6088177/AiemailAgent)

---

## 📜 License

See [LICENSE](LICENSE) file for full terms.  
Commercial use requires written permission from the owner.

© 2025 KHAN

---

Would you like me to:
- Add badges for GitHub Actions or License?
- Deploy the dashboard online using Streamlit Community Cloud?
- Package it as a ZIP for demos or clients?
- Schedule runs via Windows Task Scheduler?

Let me know — I’ll walk you through it live!

I'm ready to help you finish this now. Just say what you'd like next.
