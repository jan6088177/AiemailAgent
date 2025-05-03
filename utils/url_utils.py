from urllib.parse import urlparse
import re

SOCIAL_MEDIA_DOMAINS = {
    "linkedin.com", "twitter.com", "x.com", "facebook.com",
    "instagram.com", "github.com", "youtube.com", "medium.com"
}

def extract_urls(text):
    return re.findall(r'https?://[^\s]+', text)

def is_social_media_url(url):
    domain = urlparse(url).netloc.replace("www.", "")
    return domain in SOCIAL_MEDIA_DOMAINS

def extract_social_media_links(text):
    urls = extract_urls(text)
    return [url for url in urls if is_social_media_url(url)]