"""scorer.py — exact match after normalisation, plus per-category breakdown."""
import re
from collections import defaultdict
from evalset import EVAL, LABELS

SYNONYMS = {                       # map plausible phrasings onto canonical labels
    "tech": "technical", "technical support": "technical", "support": "technical",
    "return": "refund", "returns": "refund", "refunds": "refund",
    "payment": "billing", "payments": "billing", "invoice": "billing",
    "greetings": "greeting", "hello": "greeting", "smalltalk": "greeting",
    "other": "out_of_scope", "off-topic": "out_of_scope", "none": "out_of_scope",
    "out of scope": "out_of_scope", "unrelated": "out_of_scope",
}


def normalise(pred):
    p = re.sub(r"[^a-z_ ]", "", str(pred).strip().lower()).strip()
    p = SYNONYMS.get(p, p)
    return p if p in LABELS else "UNPARSEABLE"


def score(preds, name="system"):
    """preds: list of 30 raw predictions, aligned with EVAL."""
    assert len(preds) == len(EVAL), "prediction count must match the frozen eval set"
    per = defaultdict(lambda: [0, 0])              # category -> [correct, total]
    wrong = []
    for (text, gold), raw in zip(EVAL, preds):
        p = normalise(raw)
        ok = (p == gold)
        per[gold][1] += 1
        per[gold][0] += int(ok)
        if not ok:
            wrong.append((text, gold, p))
    total_ok = sum(c for c, _ in per.values())
    return {"name": name, "overall": total_ok / len(EVAL),
            "correct": total_ok, "n": len(EVAL),
            "per_category": {k: (c, t, c / t) for k, (c, t) in per.items()},
            "wrong": wrong}


def report(res):
    print(f"\n=== {res['name']} ===  overall {res['correct']}/{res['n']} "
          f"= {res['overall']:.3f}")
    for cat in LABELS:
        c, t, a = res["per_category"][cat]
        bar = "█" * round(a * 20)
        print(f"  {cat:14s} {c}/{t}  {a:.3f}  {bar}")
    for text, gold, pred in res["wrong"]:
        print(f"    ✗ {text[:48]:50s} gold={gold:13s} pred={pred}")

