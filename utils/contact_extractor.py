import phonenumbers
from phonenumbers.phonenumberutil import number_type
from urllib.parse import urlparse
import re

def extract_phone_numbers(text):
    results = []
    for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        num_str = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        results.append({
            "number": num_str,
            "valid": phonenumbers.is_valid_number(match.number),
            "country_code": match.number.country_code,
            "location": "",
            "type": number_type(match.number)
        })
    return results

def extract_whatsapp_numbers(phone_results):
    return [p for p in phone_results if p["valid"] and p["number"].startswith("+")]