"""A rules baseline (free) and a prompted-Claude baseline (the real incumbent)."""
import time
import scripted_api as anthropic
from evalset import EVAL, LABELS
from scorer import score, report

# ------------------------------------------------------------ rules baseline
RULES = [
    ("greeting", ["hi", "hiya", "hello", "hey", "morning", "afternoon", "evening"]),
    ("refund",   ["refund", "return", "send them back", "send it back", "money back",
                  "reimburs", "postage"]),
    ("billing",  ["invoice", "plan", "paying", "charge", "card", "billing",
                  "subscription", "twice"]),
    ("technical", ["error", "crash", "blank", "csv", "loading", "sync", "closes",
                   "rendering", "nothing", "inbox"]),
]


def rules_predict(text):
    low = text.lower()
    for label, keys in RULES:
        if any(k in low for k in keys):
            return label
    return "out_of_scope"


# ------------------------------------------------- prompted-Claude baseline
MODEL = "claude-sonnet-5"
PRICE_IN, PRICE_OUT = 2.00 / 1e6, 10.00 / 1e6
client = anthropic.Anthropic()

SYSTEM = """You route customer support messages for an online shop.

Reply with EXACTLY ONE of these labels and nothing else:
greeting | refund | technical | billing | out_of_scope

Definitions:
- greeting: pure hello/small talk with no request yet
- refund: returning goods, getting money back for an order, return postage or windows
- technical: the product or app is not working correctly
- billing: subscriptions, invoices, plans, cards, prices, duplicate charges
- out_of_scope: anything not about this shop or its product

Output the label only. No punctuation, no explanation."""


def claude_predict_all(texts):
    preds, in_tok, out_tok = [], 0, 0
    t0 = time.time()
    for t in texts:
        r = client.messages.create(
            model=MODEL, max_tokens=8, system=SYSTEM,
            messages=[{"role": "user", "content": f"Message: {t}"}],
        )
        preds.append("".join(b.text for b in r.content if b.type == "text").strip())
        in_tok += r.usage.input_tokens
        out_tok += r.usage.output_tokens
    dt = time.time() - t0
    cost = in_tok * PRICE_IN + out_tok * PRICE_OUT
    print(f"prompted: {in_tok} in + {out_tok} out tok, ${cost:.5f} total, "
          f"${cost / len(texts) * 1000:.3f} per 1k calls, {dt / len(texts) * 1000:.0f} ms/call")
    return preds


if __name__ == "__main__":
    texts = [t for t, _ in EVAL]
    report(score([rules_predict(t) for t in texts], "rules baseline"))
    report(score(claude_predict_all(texts), "prompted claude-sonnet-5"))

