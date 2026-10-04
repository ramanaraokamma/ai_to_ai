"""Every 'no' the system can say, in one file, so they can be tested together."""
import re
from pathlib import Path

MAX_QUESTION_CHARS = 2000          # red-team #6. Checked BEFORE any API call.
SANDBOX = (Path(__file__).resolve().parent.parent / "sandbox").resolve()

INJECTION_MARKERS = [
    "ignore all previous", "ignore previous instructions", "disregard the above",
    "new instructions", "new rule", "you are now", "system:", "override",
    "exfiltrate", "print your system prompt", "reveal your instructions",
]

PII_PATTERNS = [
    (re.compile(r"\b[\w.\-+]+@[\w\-]+\.[\w.\-]+\b"), "[EMAIL REDACTED]"),
    (re.compile(r"(?<!\d)(?:\+?\d[\d\s\-().]{7,}\d)(?!\d)"), "[PHONE REDACTED]"),
]


class BudgetExceeded(Exception):
    pass


class BudgetGuard:
    """Refuse BEFORE the call that would go over. From Module 5, unchanged."""

    def __init__(self, limit_usd, price_in=2.00, price_out=10.00):
        self.limit, self.spent, self.calls = limit_usd, 0.0, 0
        self.price_in, self.price_out = price_in, price_out

    def check(self, projected_usd=0.0):
        if self.spent + projected_usd > self.limit:
            raise BudgetExceeded(
                f"${self.spent:.4f} spent over {self.calls} calls; "
                f"next call would exceed the ${self.limit:.2f} cap")

    def record(self, in_tok, out_tok):
        self.spent += in_tok / 1e6 * self.price_in + out_tok / 1e6 * self.price_out
        self.calls += 1
        return self.spent


def check_question(q: str) -> str | None:
    """Return a refusal reason, or None if the question is acceptable."""
    if not q or not q.strip():
        return "empty question"
    if len(q) > MAX_QUESTION_CHARS:
        return f"question too long ({len(q)} chars; limit {MAX_QUESTION_CHARS})"
    return None


def scan_injection(text: str) -> list[str]:
    low = text.lower()
    return [m for m in INJECTION_MARKERS if m in low]


def redact_pii(text: str) -> str:
    """Red-team #5. Runs on retrieved text BEFORE it enters the context,
    and on anything written to the trace."""
    for pattern, replacement in PII_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def wrap_untrusted(text: str) -> str:
    """Retrieved text is DATA. Tag it so the system prompt can say so."""
    return f"<untrusted_data>\n{text}\n</untrusted_data>"


def safe_sandbox_path(name: str) -> Path:
    """Resolve first, THEN compare. Resolving after the check is the bug."""
    p = (SANDBOX / name).resolve()
    if not p.is_relative_to(SANDBOX):
        raise PermissionError(f"path escapes the sandbox: {name}")
    return p

