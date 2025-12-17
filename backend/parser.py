from mailparser import parse_from_file
from email.header import decode_header, make_header
import re


def decode_header_value(value):
    """
    Secure decoding RFC2047 Header
    """
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return str(value)


def strip_html(html: str) -> str:
    """
    minimalist HTML -> text（For search only）
    """
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.S)
    return re.sub(r"<[^>]+>", "", html)


def normalize_sender(name, addr):
    name = decode_header_value(name)

    if not addr:
        return name

    addr_upper = addr.upper()

    # Exchange IMCEAEX address
    if addr_upper.startswith("IMCEAEX-"):
        return name or "(Exchange user)"

    return f"{name} <{addr}>" if name else addr


def parse_eml(path):
    mail = parse_from_file(path)

    # -------- subject --------
    subject = decode_header_value(mail.subject)

    # -------- sender --------
    sender = ""
    if mail.from_:
        # mail.from_ = [(name, addr), ...]
        name, addr = mail.from_[0]
        sender = normalize_sender(name, addr)

    # -------- recipients --------
    recipients = ""
    if mail.to:
        recipients = ", ".join(
            decode_header_value(name) + f" <{addr}>" if name else addr
            for name, addr in mail.to
        )

    # -------- body (searchable text only) --------
    body = ""

    if mail.text_plain:
        body = "\n".join(mail.text_plain)
    elif mail.text_html:
        body = strip_html("\n".join(mail.text_html))

    body = body.strip()

    result = {
        "path": str(path),
        "subject": subject,
        "sender": sender,
        "recipients": recipients,
        "body": body,
    }

    return result
