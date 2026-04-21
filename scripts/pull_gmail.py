import imaplib
import email
import os
from bs4 import BeautifulSoup
from email.header import decode_header
from email import message_from_bytes 
from .validator import validate_or_raise
from .extractor import extract_insights
from .normalizer import normalize_insight
from .scorer import score_insight
import re



def decode_mime_words(s):
    if not s:
        return ""
    decoded = decode_header(s)
    return "".join([
        part.decode(enc or "utf-8") if isinstance(part, bytes) else part
        for part, enc in decoded
    ])


def extract_html(msg):
    """Extract HTML content from email"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                return part.get_payload(decode=True)
    else:
        if msg.get_content_type() == "text/html":
            return msg.get_payload(decode=True)
    return None


def clean_html(html):
    """Convert HTML → clean readable text"""
    soup = BeautifulSoup(html, "html.parser")

    # Remove junk elements
    for tag in soup(["script", "style", "footer", "nav", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Normalize whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()

    return text


def extract_main_link(html):
    """Try to find the most relevant link (very useful for newsletters)"""
    soup = BeautifulSoup(html, "html.parser")

    links = [a.get("href") for a in soup.find_all("a", href=True)]

    # Filter junk links
    links = [
        l for l in links
        if l and not any(x in l.lower() for x in [
            "unsubscribe", "preferences", "twitter.com/share", "linkedin.com/share"
        ])
    ]

    return links[0] if links else None


def get_body(msg):
    """Fallback to plain text if no HTML"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    return ""

from dotenv import load_dotenv

def pull_gmail(max_messages=5):
    load_dotenv()
    import os

    IMAP_HOST = "imap.gmail.com"
    USERNAME = os.getenv("EMAIL_USERNAME")
    PASSWORD = os.getenv("EMAIL_PASSWORD")

    if not USERNAME or not PASSWORD:
        raise ValueError("Missing EMAIL creds")
    
    mail = imaplib.IMAP4_SSL(IMAP_HOST)

    try:
        mail.login(USERNAME, PASSWORD)
    except Exception as e:
        raise RuntimeError(f"Gmail login failed: {e}") 
    mail.select("inbox")

    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()[-max_messages:]

    results = []

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = message_from_bytes(raw_email)

        subject = decode_mime_words(msg["subject"])
        sender = decode_mime_words(msg.get("from"))
        date = msg.get("date")

        html = extract_html(msg)

        if html:
            html = html.decode(errors="ignore")
            content = clean_html(html)
            link = extract_main_link(html)
        else:
            content = get_body(msg)
            link = None

        # Skip garbage emails
        if not content or len(content) < 200:
            continue

        insight = extract_insights(content)

        if not isinstance(insight, dict) or "insights" not in insight:
            print(f"[extractor] failed for subject: {subject}")
            continue

        try:
            validated = validate_or_raise(insight)

            normalized = normalize_insight(validated, {
                "url": link,
                "source": "gmail"
            })

            scored = score_insight(normalized)

            if not scored or "score" not in scored:
                print(f"[scorer] invalid score for {subject}")
                continue

            if scored["score"] < 0.5:
                continue
            
            results.append({
                "id": eid.decode(),
                "subject": subject,
                "from": sender,
                "date": date,
                "url": link,
                "source": "gmail",
                "insight": normalized,
                "score": scored
            })

        except ValueError as e:
            print(f"Rejected email {eid.decode()} due to validation error: {e}")
            print(f"Content snippet: {content[:300]}")
            print(f"Content snippet: {content[:300]}")

        # Mark as read
        mail.store(eid, '+FLAGS', '\\Seen')

    mail.logout()
    return results
