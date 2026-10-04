"""LLM-as-judge with a checkable rubric, plus kappa and a position-bias test."""
import json
import re
import scripted_api as anthropic

MODEL = "claude-sonnet-5"
client = anthropic.Anthropic()

JUDGE_SYSTEM = """You grade one-sentence customer-support acknowledgements.

Apply this rubric exactly. The reply PASSES only if ALL FOUR are true:
1. It is a single sentence of 30 words or fewer.
2. It names the correct department: greeting, refund, technical, billing,
   or explicitly declines as out of scope.
3. It makes NO promise about timing, money, or outcome (no "within 24 hours",
   no "you will be refunded").
4. It does not ask the customer for information already in their message.

Reply with JSON only: {"verdict": "pass" | "fail", "failed_rules": [1,3],
"reason": "<15 words>"}"""


def judge_one(message, reply):
    r = client.messages.create(
        model=MODEL, max_tokens=200, system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content":
                   f"<customer_message>\n{message}\n</customer_message>\n\n"
                   f"<reply_to_grade>\n{reply}\n</reply_to_grade>"}],
    )
    txt = "".join(b.text for b in r.content if b.type == "text")
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return {"verdict": "UNPARSEABLE", "failed_rules": [], "reason": txt[:60]}
    try:
        return json.loads(m.group())
    except json.JSONDecodeError:
        return {"verdict": "UNPARSEABLE", "failed_rules": [], "reason": txt[:60]}


# ------------------------------------------------------------- kappa
def cohen_kappa(both_pass, judge_pass_human_fail, judge_fail_human_pass, both_fail):
    n = both_pass + judge_pass_human_fail + judge_fail_human_pass + both_fail
    p_o = (both_pass + both_fail) / n
    jp = (both_pass + judge_pass_human_fail) / n
    hp = (both_pass + judge_fail_human_pass) / n
    p_e = jp * hp + (1 - jp) * (1 - hp)
    kappa = (p_o - p_e) / (1 - p_e)
    return {"n": n, "p_o": p_o, "p_e": p_e, "kappa": kappa,
            "judge_pass_rate": jp, "human_pass_rate": hp,
            "false_pass": judge_pass_human_fail, "false_fail": judge_fail_human_pass}


def kappa_label(k):
    for hi, name in [(0.20, "poor"), (0.40, "fair"), (0.60, "moderate"),
                     (0.80, "substantial")]:
        if k <= hi:
            return name
    return "almost perfect"


# ---------------------------------------------------- pairwise + position bias
PAIR_SYSTEM = """You compare two candidate support replies to the same message.
Pick the better one using this rubric: correct department, no promises, one
sentence, under 30 words. Reply with JSON only: {"winner": "A" | "B"}."""


def judge_pair(message, a, b):
    r = client.messages.create(
        model=MODEL, max_tokens=50, system=PAIR_SYSTEM,
        messages=[{"role": "user", "content":
                   f"<message>{message}</message>\n\n<A>{a}</A>\n\n<B>{b}</B>"}],
    )
    txt = "".join(bl.text for bl in r.content if bl.type == "text")
    m = re.search(r'"winner"\s*:\s*"([AB])"', txt)
    return m.group(1) if m else None


def position_bias_test(cases, replies_v1, replies_v2):
    """Run every comparison in both orders. Returns the honest verdict."""
    first_wins = consistent = flipped = 0
    v1_consistent = v2_consistent = 0
    for msg, r1, r2 in zip(cases, replies_v1, replies_v2):
        fwd = judge_pair(msg, r1, r2)        # A=v1, B=v2
        rev = judge_pair(msg, r2, r1)        # A=v2, B=v1
        if fwd is None or rev is None:
            continue
        first_wins += (fwd == "A") + (rev == "A")
        w_fwd = "v1" if fwd == "A" else "v2"
        w_rev = "v2" if rev == "A" else "v1"
        if w_fwd == w_rev:
            consistent += 1
            v1_consistent += (w_fwd == "v1")
            v2_consistent += (w_fwd == "v2")
        else:
            flipped += 1
    n = consistent + flipped
    return {"n": n, "first_position_win_rate": first_wins / (2 * n),
            "flip_rate": flipped / n, "consistent": consistent,
            "v1_wins_consistent": v1_consistent, "v2_wins_consistent": v2_consistent}

