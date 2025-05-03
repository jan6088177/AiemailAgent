# llm_processor/processor.py

import os
import logging
import requests
import yaml
from typing import Optional, Dict, Any

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logging.warning("⚠️ python-dotenv not found — install it to use .env files")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load prompts from YAML
try:
    with open("llm_processor/prompts.yaml", "r") as f:
        PROMPTS = yaml.safe_load(f)
    logger.info("📄 Prompts loaded successfully")
except FileNotFoundError:
    logger.error("❌ Prompts file not found. Please check: llm_processor/prompts.yaml")
    PROMPTS = {}
except Exception as e:
    logger.exception(f"❌ Failed to load prompts: {e}")
    PROMPTS = {}

# Get API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    logger.warning("⚠️ OPENROUTER_API_KEY is missing — LLM features may fail.")

def call_mistral(prompt: str) -> str:
    """
    Calls Mistral or another LLM via OpenRouter.
    Returns response text or empty string on failure.
    """
    if not OPENROUTER_API_KEY:
        logger.error("🔑 OPENROUTER_API_KEY not set — skipping LLM call.")
        return ""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        logger.info("🧠 Sending request to LLM...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10  # Set timeout for network errors
        )

        if response.status_code != 200:
            logger.error(f"🔴 LLM API returned status code: {response.status_code}")
            logger.debug(response.text)
            return ""

        data = response.json()

        if "choices" not in data:
            logger.warning("⚠️ Unexpected LLM response structure:")
            logger.debug(data)
            return ""

        content = data["choices"][0]["message"]["content"]
        logger.info("🟢 Successfully received LLM response.")
        return content.strip()

    except requests.exceptions.RequestException as e:
        logger.error(f"🌐 Network error during LLM call: {e}")
        return ""
    except KeyError as e:
        logger.error(f"🚫 Missing expected field in LLM response: {e}")
        return ""
    except Exception as e:
        logger.exception("💥 Unexpected error in LLM call:")
        return ""


def classify_email(body: str) -> str:
    """
    Classifies an email into categories like Sales Inquiry, Spam, etc.
    Returns 'Other' if classification fails.
    """
    prompt_data = PROMPTS.get("classification", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Classification prompt not found in YAML.")
        return "Other"

    full_prompt = prompt.format(body=body[:1000])  # Limit input size
    result = call_mistral(full_prompt).lower()

    valid_categories = {
        "sales inquiry": ["sales", "inquiry"],
        "marketing / newsletter": ["marketing", "newsletter"],
        "management request": ["management"],
        "internal communication": ["internal"],
        "support request": ["support"],
        "hr / recruitment": ["hr", "recruit"],
        "spam / fraudulent": ["spam", "phishing", "fraudulent"],
        "other": []
    }

    for cat, keywords in valid_categories.items():
        if any(kw in result for kw in keywords):
            return cat.title()

    return "Other"


def generate_reply(body: str) -> str:
    """
    Generates a reply using the LLM.
    Returns empty string if generation fails.
    """
    prompt_data = PROMPTS.get("auto_reply", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Auto-reply prompt not found in YAML.")
        return ""

    full_prompt = prompt.format(body=body[:1000])
    reply_text = call_mistral(full_prompt)

    if not reply_text:
        logger.warning("💬 Empty reply generated — no content returned.")
        return ""

    return reply_text.strip()


def get_lead_score(body: str) -> int:
    """
    Uses LLM to rate lead score from 1 to 10.
    Returns 5 if unable to determine.
    """
    prompt_data = PROMPTS.get("lead_score", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Lead scoring prompt not found in YAML.")
        return 5

    full_prompt = prompt.format(body=body[:1000])
    result = call_mistral(full_prompt)

    try:
        score = int(result.strip())
        if 1 <= score <= 10:
            return score
        else:
            logger.warning("⚠️ Invalid score range returned:", result)
            return 5
    except ValueError:
        logger.warning("🔢 Could not parse score — defaulting to 5")
        return 5


def extract_info(body: str) -> Dict[str, Any]:
    """
    Extracts personal/business info (name, phone, company, etc.)
    Returns empty dict if extraction fails.
    """
    prompt_data = PROMPTS.get("extraction", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Info extraction prompt not found in YAML.")
        return {}

    full_prompt = prompt.format(body=body[:1000])
    extracted = call_mistral(full_prompt)

    try:
        info = yaml.safe_load(extracted)
        logger.info("📄 Extracted structured info:", info)
        return info
    except Exception as e:
        logger.error(f"❌ Failed to parse extracted info: {e}")
        return {}


def is_spam(body: str) -> bool:
    """
    Uses LLM to detect spam or phishing attempts.
    Returns True if spam-like.
    """
    prompt_data = PROMPTS.get("spam_detection", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Spam detection prompt not found in YAML.")
        return False

    full_prompt = prompt.format(body=body[:1000])
    result = call_mistral(full_prompt).lower()

    return any(keyword in result for keyword in ["spam", "phishing", "fraud"])


def analyze_tone(body: str) -> str:
    """
    Analyzes tone of email — polite, urgent, neutral, etc.
    """
    prompt_data = PROMPTS.get("tone_analysis", {})
    prompt = prompt_data.get("prompt", "")

    if not prompt:
        logger.warning("🟡 Tone analysis prompt not found in YAML.")
        return "Unknown"

    full_prompt = prompt.format(body=body[:1000])
    result = call_mistral(full_prompt).strip().capitalize()
    return result