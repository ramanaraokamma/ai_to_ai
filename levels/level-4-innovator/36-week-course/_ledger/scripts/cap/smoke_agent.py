import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, os.path.join(HERE, "src")); sys.path.insert(0, os.path.join(HERE, ".."))
from spine import answer, NEEDS_MATH
from guards import redact_pii
Q = "how many merges did the BPE tokenizer learn, and what is the total?"
print("NEEDS_MATH matches module's own example question 2?", bool(NEEDS_MATH.search("if I go from batch 32 to batch 128, what LR keeps things equal?")))
print("NEEDS_MATH matches:", bool(NEEDS_MATH.search(Q)))
try:
    a = answer(Q, verbose=True); print(a.route, a.refused, a.text[:100])
except Exception as e:
    print("!! EXCEPTION ESCAPED answer():", type(e).__name__, e)
print("redact_pii('## 2026-01-14 — Optimizer bake-off') ->", redact_pii("## 2026-01-14 — Optimizer bake-off"))
print("redact_pii('version 1.2.3.4567 on 2026-09-06 at 12:30') ->", redact_pii("version 1.2.3.4567 on 2026-09-06 at 12:30"))
print("redact_pii('call +91 98765 43210 or a@b.co') ->", redact_pii("call +91 98765 43210 or a@b.co"))
