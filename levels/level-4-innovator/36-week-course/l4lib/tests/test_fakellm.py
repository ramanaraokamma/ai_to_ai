"""Plain-assert tests for l4lib/fakellm.py.  Run:  python3 tests/test_fakellm.py  (from l4lib/)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from l4lib import fakellm
from l4lib.fakellm import FakeClient, RateLimit, BadRequest, LABEL

TICKET_SYS = "Extract fields as JSON. Rules: category is one of billing, shipping, technical, account, other."
MSG = "<message>\nI was charged twice for order A-1234, give me my money back\n</message>"


def ask(c, system=TICKET_SYS, user=MSG, **kw):
    return c.messages.create(model="fake-small", max_tokens=kw.pop("max_tokens", 200), system=system,
                             messages=[{"role": "user", "content": user}], **kw)


def test_label_everywhere():
    c = FakeClient()
    assert LABEL == "stand-in, not a model"
    assert LABEL in repr(c)
    r = ask(c)
    assert LABEL in repr(r) and r.metadata["label"] == LABEL and r.metadata["standin"] is True
    assert c.usage_log[0]["label"] == LABEL
    assert LABEL not in r.content[0].text          # must not corrupt parsers


def test_shape_and_determinism():
    r1, r2 = ask(FakeClient(seed=3)), ask(FakeClient(seed=3))
    assert r1.content[0].text == r2.content[0].text
    assert r1.stop_reason == "end_turn" and r1.usage.input_tokens > 0 and r1.usage.output_tokens > 0
    import json
    rec = json.loads(r1.content[0].text)
    assert set(rec) == {"category", "urgency", "order_id", "refund_requested"}


def test_competence_is_documented_function():
    f = fakellm.features(TICKET_SYS, MSG)
    assert f["has_rules"] and f["n_examples"] == 0
    assert abs(fakellm.competence(f) - (0.55 + 0.15 + 0.05)) < 1e-12      # BASE + rules + schema(json)
    f2 = fakellm.features("x", "<example> <example> <example> <example> hi")
    assert abs(fakellm.competence(f2) - (0.55 + 0.08 * 3)) < 1e-12        # examples capped at 3
    assert fakellm.competence(f, error_rate=5.0) == 0.0


def test_error_rate_lowers_accuracy_measurably():
    import json
    def acc(er):
        ok = 0
        for s in range(60):
            c = FakeClient(seed=s, error_rate=er)
            rec = json.loads(ask(c).content[0].text)
            ok += rec["category"] == "billing"
        return ok / 60
    assert acc(0.0) > acc(0.6)
    assert acc(-1.0) == 1.0


def test_rules_change_format():
    chatty = ask(FakeClient(), system="You extract tickets.").content[0].text
    plain = ask(FakeClient()).content[0].text
    assert chatty.startswith("Sure!") and plain.startswith("{")


def test_max_tokens_truncates():
    c = FakeClient()
    r = ask(c, system="", user="one two three four five six seven eight nine ten eleven twelve. Next.",
            max_tokens=3)
    assert r.stop_reason == "max_tokens" and r.usage.output_tokens == 3
    assert len(r.content[0].text.split()) <= 3


def test_stop_sequences():
    c = FakeClient()
    r = ask(c, system="", user="alpha beta STOP gamma delta.", stop_sequences=["STOP"])
    assert r.stop_reason == "stop_sequence" and r.stop_sequence == "STOP"
    assert "STOP" not in r.content[0].text and r.content[0].text.startswith("alpha beta")


def test_prefix_cache_accounting():
    c = FakeClient()
    long_sys = " ".join(f"w{i}" for i in range(100))
    a = ask(c, system=long_sys, user="first question here please")
    b = ask(c, system=long_sys, user="second different question")
    assert a.usage.cache_read_input_tokens == 0
    assert b.usage.cache_read_input_tokens >= 100
    total_a = a.usage.input_tokens + a.usage.cache_read_input_tokens
    total_b = b.usage.input_tokens + b.usage.cache_read_input_tokens
    assert abs(total_a - total_b) <= 3
    assert b.cost < fakellm.cost_usd("fake-small", total_b, b.usage.output_tokens)
    off = FakeClient(prefix_cache=False)
    ask(off, system=long_sys); assert ask(off, system=long_sys).usage.cache_read_input_tokens == 0


def test_faults():
    c = FakeClient(fail_on={2: RateLimit, 3: BadRequest})
    ask(c)
    for exc, code in ((RateLimit, 429), (BadRequest, 400)):
        try:
            ask(c)
            assert False, "should have raised"
        except exc as e:
            assert e.status_code == code and LABEL in str(e)
    ask(c)                                                   # call 4 fine again
    assert c.calls == 4
    v = FakeClient(forbid_temperature=True)
    try:
        ask(v, temperature=0.5); assert False
    except BadRequest as e:
        assert "ONE vendor" in str(e)
    ask(FakeClient(), temperature=0.5)                       # accepted when not simulating that vendor


def test_bad_requests():
    c = FakeClient()
    for kw in ({"max_tokens": 0}, {"messages": []}):
        args = dict(model="m", max_tokens=5, system="", messages=[{"role": "user", "content": "hi"}])
        args.update(kw)
        try:
            c.messages.create(**args); assert False
        except BadRequest:
            pass


def test_totals_and_cost_table():
    c = FakeClient()
    ask(c); ask(c)
    tin, tout = c.total_tokens()
    assert tin > 0 and tout > 0 and c.total_cost() > 0
    # 1M in + 1M out at the fake-small illustrative prices
    assert fakellm.cost_usd("fake-small", 1_000_000, 1_000_000) == 6.0
    assert fakellm.count_tokens("") == 0 and fakellm.count_tokens("a b c d e f g h i j") == 13
    assert c.messages.count_tokens(system="a b", messages=[{"role": "user", "content": "c d"}]).input_tokens == 6


def test_custom_policy_receives_features():
    seen = {}
    def pol(system, user, feats, seed, p):
        seen.update(feats=feats, p=p); return "ok"
    r = FakeClient(policy=pol).messages.create(model="fake-small", max_tokens=5, system="Rules: x",
                                               messages=[{"role": "user", "content": "<example> q"}])
    assert r.content[0].text == "ok" and seen["feats"]["has_rules"] and seen["feats"]["n_examples"] == 1


if __name__ == "__main__":
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); n += 1; print("ok", name)
    print(f"{n} tests passed")
