# pii.py — find and mask personally identifiable information.
# Pure standard library. No API key, no network, no cost.
import re
from collections import Counter

# Order matters. The longest, most specific patterns run FIRST, so a 16-digit
# card number is never chopped into a 10-digit "phone number" by a later rule.
PATTERNS = [
    ("CARD",    re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")),
    ("AADHAAR", re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b")),
    ("EMAIL",   re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    # (?<!\d) and (?!\d) stop this matching 10 digits inside a longer number.
    ("PHONE",   re.compile(r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)")),
    ("IPV4",    re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]


def redact(text):
    """Return (masked_text, Counter of what was found)."""
    found = Counter()                       # how many of each type we replaced

    def make_replacer(tag):
        def _replace(match):                # called once per match
            found[tag] += 1                 # number them so [EMAIL_1] != [EMAIL_2]
            return f"[{tag}_{found[tag]}]"
        return _replace

    out = text
    for tag, pattern in PATTERNS:           # apply every rule in order
        out = pattern.sub(make_replacer(tag), out)
    return out, found


# --------------------------------------------------------------- demo
NOTE = """# Week 7 — shipping notes

Called the vendor on +91 98765 43210, no answer. Emailed
priya.sharma@example.com instead. Backup contact 9123456789.
Test card 4111 1111 1111 1111 (sandbox only).
Server was at 192.168.1.44.
Met Ramana at the third house past the temple on Nehru Road.
"""

clean, counts = redact(NOTE)
print(clean)
print("found:", dict(counts))

# Append to pii.py — a recall test you can actually quote a number from.
CASES = [
    ("priya.sharma@example.com", "EMAIL",   True),
    ("+91 98765 43210",          "PHONE",   True),
    ("9123456789",               "PHONE",   True),
    ("4111 1111 1111 1111",      "CARD",    True),
    ("1234 5678 9012",           "AADHAAR", True),
    ("192.168.1.44",             "IPV4",    True),
    ("Ramana Kamma",             "NAME",    True),      # regex cannot do this
    ("third house past the temple, Nehru Road", "ADDRESS", True),
]

caught = 0
print(f"{'input':<42} {'type':<9} caught?")
print("-" * 60)
for raw, kind, _is_pii in CASES:
    masked, hits = redact(raw)
    ok = bool(hits)
    caught += ok
    print(f"{raw:<42} {kind:<9} {'YES' if ok else 'no'}")

print("-" * 60)
print(f"recall = {caught}/{len(CASES)} = {caught / len(CASES):.2f}")

