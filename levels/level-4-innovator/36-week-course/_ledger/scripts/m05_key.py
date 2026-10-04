import stub_anthropic as anthropic
from m05_prompts import *
from bench import *
from m05_caller import make_caller, SCHEMA, client, MODEL
import sys; sys.argv=['x']

PARA = ("The school library opened a new reading room with thirty chairs and eight "
        "tables. Students borrow books every morning and return them before evening. "
        "Attendance in the room has doubled since it opened in March.")


def probe(max_tokens):
    r = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system="Summarize in one sentence. No preamble.",
        messages=[{"role": "user", "content": PARA}],
    )
    cost = r.usage.input_tokens / 1e6 * 2.00 + r.usage.output_tokens / 1e6 * 10.00
    print(f"max_tokens={max_tokens}")
    print(f"  text        : {''.join(b.text for b in r.content if b.type == 'text')!r}")
    print(f"  stop_reason : {r.stop_reason}")
    print(f"  input_tokens: {r.usage.input_tokens}")
    print(f"  output_tokens: {r.usage.output_tokens}")
    print(f"  cost        : ${cost:.6f}")


probe(1024)
probe(20)

print('=== ex2 constant baseline')
from itertools import product
from bench import TESTS, FIELDS, CATEGORIES, score_record

best, best_score = None, -1.0
for cat, urg, refund in product(CATEGORIES, [1, 2, 3], [True, False]):
    rec = {"category": cat, "urgency": urg,
           "order_id": None, "refund_requested": refund}
    s = sum(score_record(rec, c["gold"])[0] for c in TESTS) / len(TESTS)
    if s > best_score:
        best, best_score = rec, s

print("best constant record:", best)
print(f"field score: {best_score * 100:.1f}%")

# how many field decisions is that?
print(f"= {round(best_score * len(TESTS) * len(FIELDS))} of {len(TESTS) * len(FIELDS)} fields")

print('=== ex3 v5')
URGENCY_RUBRIC = """
Urgency is decided by IMPACT, not by tone. Ignore capitals and exclamation marks.
  3 — the customer's money is currently wrong (charged twice, charged after
      cancelling, refund overdue), OR they are fully blocked from using the
      product, OR a delivery is more than 7 days late.
  2 — something is broken or wrong but the customer can still function, or is
      waiting on a normal-speed reply.
  1 — a question, a compliment, or a request with no deadline.
When two levels both fit, choose the LOWER one.
"""

PROMPTS["v5-urgency-rubric"] = {
    "system": SYSTEM_BASE + "\n" + RULES + "\n" + URGENCY_RUBRIC,
    "template": EXAMPLES + "\n<message>\n{{TEXT}}\n</message>",
    "schema": True,
    "notes": "v4 + impact-not-tone urgency rubric with a lower-of-two tiebreak",
}

guard = BudgetGuard(limit_usd=0.20)
rows = []
for v in ["v4-few-shot-schema", "v5-urgency-rubric"]:
    name, results = run_suite(v, make_caller(v, guard))
    rows.append(report(name, results))
    field_breakdown(name, results)

print('=== ex4 parsers')
def stub_nested(text):
    return ('{"result": {"category": "billing", "urgency": 2, "order_id": null, '
            '"refund_requested": false}, "confidence": 0.9}'), 90, 40


def stub_extra_key(text):
    return ('{"category": "billing", "urgency": 2, "order_id": null, '
            '"refund_requested": false, "sentiment": "angry"}'), 90, 40


def stub_truncated(text):
    return '{"category": "billing", "urgency": 2, "order_i', 90, 15


def stub_double(text):
    return ('{"category": "billing", "urgency": 2, "order_id": null, "refund_requested": false}\n'
            '{"category": "shipping", "urgency": 1, "order_id": null, "refund_requested": false}'), 90, 70


for nm, fn in [("nested", stub_nested), ("extra-key", stub_extra_key),
               ("truncated", stub_truncated), ("double", stub_double)]:
    n, r = run_suite(nm, fn)
    report(n, r)

def extract_json_v2(text, wanted=("category", "urgency", "order_id", "refund_requested")):
    """Scan for balanced {...} blocks; return the first that has the wanted keys."""
    candidates, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                candidates.append(text[start:i + 1])
                start = None
    for blob in candidates:
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if all(k in obj for k in wanted):
            return obj
        # one level of nesting: look inside dict-valued fields
        for v in obj.values():
            if isinstance(v, dict) and all(k in v for k in wanted):
                return v
    return None

print('=== extract_json_v2 checks')
print(extract_json_v2('{"result": {"category": "billing", "urgency": 2, "order_id": null, "refund_requested": false}, "confidence": 0.9}'))
print(extract_json_v2('{"category": "billing", "urgency": 2, "order_id": null, "refund_requested": false}\n{"category": "shipping"}'))
print(extract_json_v2('{"category": "billing", "urgency": 2, "order_id": null, "refund_requested": false}\n{"category": "shipping"}'))
print(extract_json_v2('{"category": "billing", "urgency": 2, "order_i'))
print('=== ex5 grounding')
DOC = """Millford has three bus routes. Route 1 runs from the station to the hospital
every 20 minutes between 6am and 9pm. Route 2 runs from the station to Millford Beach
every 45 minutes, but only on Saturdays and Sundays. Route 3 is a school service that
runs twice each weekday morning. A single fare on any route costs 2.40. Children under
five travel free. The last Route 1 bus leaves the hospital at 9.15pm. Route 2 does not
run in January or February. Bus passes can be bought at the station kiosk, which opens
at 5.30am on weekdays. Route 3 does not accept bus passes."""

QUESTIONS = [
    ("How often does Route 1 run?", "every 20 minutes"),                 # answerable
    ("What does a single fare cost?", "2.40"),                           # answerable
    ("Which route does not accept bus passes?", "route 3"),              # answerable
    ("When does Route 2 not run?", "january"),                           # answerable
    ("How many buses does Millford own?", "NOT IN SOURCE"),              # unanswerable
    ("Who is the mayor of Millford?", "NOT IN SOURCE"),                  # unanswerable
]

UNGROUNDED = "Answer the question in one short sentence."
GROUNDED = (
    "Answer using ONLY the text inside <source>. "
    "If the source does not contain the answer, reply with exactly: NOT IN SOURCE"
)


def ask(system, q, with_doc):
    content = f"<source>\n{DOC}\n</source>\n\n{q}" if with_doc else q
    r = client.messages.create(model=MODEL, max_tokens=150, system=system,
                               messages=[{"role": "user", "content": content}])
    return "".join(b.text for b in r.content if b.type == "text").strip()


for label, system, with_doc in [("ungrounded", UNGROUNDED, False),
                                ("grounded", GROUNDED, True)]:
    correct = refused = wrong = 0
    print(f"\n--- {label} ---")
    for q, gold in QUESTIONS:
        a = ask(system, q, with_doc)
        if gold == "NOT IN SOURCE":
            if "NOT IN SOURCE" in a.upper():
                refused += 1; verdict = "✅ refused"
            else:
                wrong += 1; verdict = "❌ INVENTED"
        else:
            if gold.lower() in a.lower():
                correct += 1; verdict = "✅ correct"
            else:
                wrong += 1; verdict = "❌ wrong"
        print(f"  {verdict:12s} {q}\n               -> {a[:90]}")
    print(f"  correct {correct}  correctly-refused {refused}  wrong {wrong}")

