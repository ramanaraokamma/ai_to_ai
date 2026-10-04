"""Prompt Bench: a tiny, honest eval harness."""
import json
import re
import time
from dataclasses import dataclass

CATEGORIES = ["billing", "shipping", "technical", "account", "other"]
FIELDS = ["category", "urgency", "order_id", "refund_requested"]

# ---------------------------------------------------------------- test set
# FROZEN. Written before any prompt existed. Do not edit to make a score go up.
TESTS = [
    {"id": "t1", "text": "Order #A-4471 never showed up. It's been 12 days. I want my money back.",
     "gold": {"category": "shipping", "urgency": 3, "order_id": "A-4471", "refund_requested": True}},
    {"id": "t2", "text": "hi, quick q - can I change the email on my account? no rush",
     "gold": {"category": "account", "urgency": 1, "order_id": None, "refund_requested": False}},
    {"id": "t3", "text": "You charged me twice for order B-1029. Please fix.",
     "gold": {"category": "billing", "urgency": 2, "order_id": "B-1029", "refund_requested": False}},
    {"id": "t4", "text": "App crashes every time I open the settings tab on Android 14.",
     "gold": {"category": "technical", "urgency": 2, "order_id": None, "refund_requested": False}},
    {"id": "t5", "text": "URGENT!!! my card was charged 3 times, order C-77, refund NOW",
     "gold": {"category": "billing", "urgency": 3, "order_id": "C-77", "refund_requested": True}},
    {"id": "t6", "text": "Just wanted to say the new packaging is lovely. No issue here.",
     "gold": {"category": "other", "urgency": 1, "order_id": None, "refund_requested": False}},
    {"id": "t7", "text": "Package arrived smashed. Order D-3312. Send a new one or refund me.",
     "gold": {"category": "shipping", "urgency": 3, "order_id": "D-3312", "refund_requested": True}},
    {"id": "t8", "text": "I can't log in. Password reset email never arrives. Been 2 days.",
     "gold": {"category": "account", "urgency": 2, "order_id": None, "refund_requested": False}},
]

# ---------------------------------------------------------------- scoring
def score_record(pred, gold):
    """Field-level score in [0,1] plus a per-field 0/1 dict."""
    if not isinstance(pred, dict):
        return 0.0, {f: 0 for f in FIELDS}
    per = {f: int(pred.get(f, "__missing__") == gold[f]) for f in FIELDS}
    return sum(per.values()) / len(FIELDS), per


def extract_json(text):
    """Best-effort parse: grab the first {...} block. None if it fails."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


@dataclass
class CaseResult:
    id: str
    score: float
    per_field: dict
    parsed_ok: bool
    in_tok: int
    out_tok: int
    latency: float
    raw: str


def run_suite(name, call, cases=TESTS):
    """`call(text) -> (raw_text, input_tokens, output_tokens)`."""
    results = []
    for c in cases:
        t0 = time.perf_counter()
        raw, itok, otok = call(c["text"])
        lat = time.perf_counter() - t0
        pred = extract_json(raw)
        s, per = score_record(pred, c["gold"])
        results.append(CaseResult(c["id"], s, per, pred is not None, itok, otok, lat, raw))
    return name, results


def report(name, results, price_in=2.00, price_out=10.00):
    n = len(results)
    avg = sum(r.score for r in results) / n
    exact = sum(r.score == 1.0 for r in results)
    itok = sum(r.in_tok for r in results)
    otok = sum(r.out_tok for r in results)
    cost = itok / 1e6 * price_in + otok / 1e6 * price_out
    lat = sum(r.latency for r in results) / n
    fails = sum(not r.parsed_ok for r in results)
    print(f"{name:22s} field {avg * 100:5.1f}%  exact {exact:2d}/{n}  parse-fail {fails}  "
          f"tok {itok:5d}/{otok:4d}  ${cost:.4f}  {lat * 1000:6.1f} ms/case")
    return {"name": name, "field": avg, "exact": exact, "cost": cost}


def field_breakdown(name, results):
    print(f"  {name} per-field correct:",
          {f: sum(r.per_field[f] for r in results) for f in FIELDS})


# ---------------------------------------------------- offline stub "models"
def stub_dumb(text):
    return ('{"category": "other", "urgency": 1, "order_id": null, '
            '"refund_requested": false}'), 90, 30


def stub_chatty(text):
    body = ('{"category": "billing", "urgency": 2, "order_id": null, '
            '"refund_requested": false}')
    return f"Sure! Here is the extracted record:\n```json\n{body}\n```\nLet me know!", 140, 70


def stub_broken(text):
    return "category: billing, urgency: 2", 90, 20


if __name__ == "__main__":
    for nm, fn in [("v0-stub-dumb", stub_dumb),
                   ("v1-stub-chatty", stub_chatty),
                   ("v2-stub-broken", stub_broken)]:
        n, r = run_suite(nm, fn)
        report(n, r)
        field_breakdown(n, r)

