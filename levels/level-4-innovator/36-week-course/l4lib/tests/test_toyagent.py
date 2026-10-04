"""Plain-assert tests for l4lib/toyagent.py.  Run:  python3 tests/test_toyagent.py  (from l4lib/)."""
import os, sys, json, time, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from l4lib import rag, toyagent as ta, fakellm
from l4lib.toyagent import (ScriptedModel, GullibleModel, FlakyBackend, FlakyModel, Sandbox,
                            ToolRegistry, run_agent, calculate, worked_plan, reminder_plan)


def clean_index():
    ch = rag.notebook_chunks()
    return rag.VectorIndex(ch, rag.TfidfEmbedder()), rag.notebook_titles(ch)


def poisoned_index():
    ch = rag.poisoned_notebook_chunks()
    return rag.VectorIndex(ch, rag.TfidfEmbedder()), rag.notebook_titles(ch)


def registry(sb, poisoned=False):
    ix, titles = poisoned_index() if poisoned else clean_index()
    return ta.build_registry(sb, ix, titles)


# ---------------------------------------------------------------- fences, NO model involved
def test_calculator_fence():
    assert calculate("0.00144 * 250") == "0.36"
    for bad, msg in (("__import__('os').system('ls')", "Call"), ("2 ** 10 ** 10", "exponent"),
                     ("'a' * 3", "numeric"), ("1 +", None)):
        try:
            calculate(bad); assert False, bad
        except (ValueError, SyntaxError) as e:
            assert msg is None or msg in str(e)


def test_fence_sandbox():
    sb = Sandbox()
    assert sb.write_file("a.md", "hi").startswith("wrote 2 bytes")
    for name in ("../escape.md", "/etc/passwd", "run.sh"):
        try:
            sb.write_file(name, "x"); assert False, name
        except PermissionError:
            pass
    try:
        sb.write_file("sub/a.md", "x"); assert False
    except ValueError as e:
        assert "does not exist" in str(e)
    try:
        sb.write_file("big.md", "x" * 20001); assert False
    except ValueError:
        pass
    assert sb.escaped() == [] and [a[2] for a in sb.attempts].count(True) == 1


def test_weak_sandbox_lets_dotdot_through_and_records_it():
    outer = tempfile.mkdtemp(prefix="l4_outer_")
    sb = Sandbox(os.path.join(outer, "box"), strict=False)
    sb.write_file("../leak.txt", "oops")
    assert os.path.exists(os.path.join(outer, "leak.txt")) and len(sb.escaped()) == 1


def test_fence_allowlist_timeout_confirmation_iterations_budget_with_no_model():
    sb = Sandbox()
    reg = ToolRegistry()
    reg.register("calculate", calculate, timeout=1.0)
    reg.register("slow", lambda: time.sleep(0.4) or "done", timeout=0.05)
    reg.register("write_file", sb.write_file, requires_confirmation=True)
    spec = ta.tool_specs()

    def once(name, args):                       # a plan is just data: no model is consulted
        return ScriptedModel([("", [(name, args)]), ("ok", [])])

    r = run_agent("q", reg, spec, once("delete_everything", {}))
    assert "no tool named" in r["trace"][2]["result_preview"]                     # fence 5
    r = run_agent("q", reg, spec, once("slow", {}))
    assert "timed out" in r["trace"][2]["result_preview"]                         # fence 4
    r = run_agent("q", reg, spec, once("write_file", {"filename": "h.md", "content": "x"}),
                  confirm=lambda n, a: False)
    assert "declined" in r["trace"][2]["result_preview"] and not sb.attempts      # fence 6
    r = run_agent("q", reg, spec, once("write_file", {"filename": "h.md", "content": "x"}),
                  confirm=lambda n, a: True)
    assert sb.attempts[-1][2] is True
    forever = ScriptedModel([("", [("calculate", {"expression": "1+1"})])] * 50)
    r = run_agent("q", reg, spec, forever, max_iterations=3)
    assert r["stop"] == "max_iterations" and r["iterations"] == 3                 # fence 1
    r = run_agent("q", reg, spec, forever, max_iterations=50, budget_usd=0.0004)
    assert r["stop"] == "budget_exhausted" and r["spend"] >= 0.0004               # fence 2
    r = run_agent("q", reg, spec, once("write_file", {"filename": "../x.md", "content": "y"}),
                  auto_approve=True)
    assert "PermissionError" in r["trace"][2]["result_preview"]                   # fence 3


def test_stdin_eof_means_decline():
    sb = Sandbox()
    reg = registry(sb)
    plan = ScriptedModel([("", [("write_file", {"filename": "a.md", "content": "x"})]), ("ok", [])])
    old = sys.stdin
    sys.stdin = open(os.devnull)
    try:
        r = run_agent("q", reg, ta.tool_specs(), plan)
    finally:
        sys.stdin = old
    assert "declined" in r["trace"][2]["result_preview"]


def test_too_many_tool_errors_takes_tool_away():
    reg = ToolRegistry()
    reg.register("calculate", calculate)
    m = ScriptedModel([("", [("calculate", {"expression": "nope"})])] * 10)
    r = run_agent("q", reg, ta.tool_specs(), m, max_iterations=10)
    assert r["stop"] == "too_many_tool_errors" and r["iterations"] == 3


# ---------------------------------------------------------------- the worked five-turn run
def test_worked_plan_five_turns():
    sb = Sandbox()
    r = run_agent("cost of 250 calls?", registry(sb), ta.tool_specs(), ScriptedModel(worked_plan()),
                  auto_approve=True)
    assert r["stop"] == "end_turn" and r["iterations"] == 5 and r["label"] == fakellm.LABEL
    tools = [(c["tool"], c["is_error"]) for c in r["tool_calls"]]
    assert tools == [("search_notes", False), ("calculate", False), ("write_file", True), ("write_file", False)]
    assert r["trace"][0]["label"] == "stand-in, not a model"
    assert (sb.root / "extraction-250.md").exists()
    assert "0.36" in r["answer"] and r["spend"] > 0
    calc = [e for e in r["trace"] if e["event"] == "tool_call"][1]
    assert calc["args"]["expression"] == "0.00144 * 250"


def test_input_tokens_grow_and_triangular_sum():
    r = run_agent("q", registry(Sandbox()), ta.tool_specs(), ScriptedModel(worked_plan()), auto_approve=True)
    ins = r["in_tokens"]
    assert all(b > a for a, b in zip(ins, ins[1:])) and len(ins) == 5
    # a constant-size step repeated: history is re-sent every turn, so per-turn input grows by a
    # constant (first differences ~equal) and the TOTAL grows like k^2 once the fixed prompt is removed
    reg = ToolRegistry(); reg.register("calculate", calculate)
    def run(k):
        m = ScriptedModel([("", [("calculate", {"expression": "1+1"})])] * k + [("done", [])])
        return run_agent("q", reg, ta.tool_specs(), m, max_iterations=k + 1, max_tool_errors=99)["in_tokens"]
    i = run(8)
    d = [b - a for a, b in zip(i, i[1:])]
    assert max(d) - min(d) <= 2 and min(d) > 20
    growth = lambda k: sum(x - run(k)[0] for x in run(k))             # total minus the fixed first-turn prompt
    assert 3.0 < growth(10) / growth(5) < 4.6                          # k(k+1)/2: 55/15 = 3.7


def test_trace_jsonl_roundtrip_and_determinism():
    path = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    a = run_agent("q", registry(Sandbox()), ta.tool_specs(), ScriptedModel(worked_plan()),
                  auto_approve=True, trace_path=path)
    rows = [json.loads(l) for l in open(path)]
    assert [r["seq"] for r in rows] == list(range(1, len(rows) + 1)) and rows[-1]["event"] == "finish"
    b = run_agent("q", registry(Sandbox()), ta.tool_specs(), ScriptedModel(worked_plan()), auto_approve=True)
    assert a["in_tokens"] == b["in_tokens"] and a["answer"] == b["answer"]


# ---------------------------------------------------------------- flaky things
def test_flaky_backend():
    f = FlakyBackend(lambda x: x * 2, fail_on={2})
    assert f(1) == 2
    try:
        f(1); assert False
    except ConnectionError as e:
        assert "stand-in" in str(e)
    assert f(3) == 6 and f.calls == 3
    g1 = [FlakyBackend(lambda: 1, fail_rate=0.5, seed=7) for _ in range(2)]
    def pattern(x):
        out = []
        for _ in range(20):
            try: x(); out.append(0)
            except ConnectionError: out.append(1)
        return out
    assert pattern(g1[0]) == pattern(g1[1]) and 0 < sum(pattern(FlakyBackend(lambda: 1, fail_rate=0.5, seed=1))) < 20
    t0 = time.perf_counter(); FlakyBackend(lambda: 1, latency=0.05)(); assert time.perf_counter() - t0 >= 0.05


def test_flaky_tool_inside_agent_is_an_error_result_not_a_crash():
    reg = ToolRegistry(); reg.register("calculate", FlakyBackend(calculate, fail_on={1}))
    m = ScriptedModel([("", [("calculate", {"expression": "1+1"})]), ("", [("calculate", {"expression": "1+1"})]), ("ok", [])])
    r = run_agent("q", reg, ta.tool_specs(), m)
    assert [c["is_error"] for c in r["tool_calls"]] == [True, False] and r["stop"] == "end_turn"


def test_rate_limit_retry_and_giveup():
    reg = ToolRegistry(); reg.register("calculate", calculate)
    m = FlakyModel(ScriptedModel([("", [("calculate", {"expression": "2+2"})]), ("4", [])]), fail_on={1})
    r = run_agent("q", reg, ta.tool_specs(), m)
    assert r["stop"] == "end_turn" and any(e["event"] == "api_retry" for e in r["trace"])
    m = FlakyModel(ScriptedModel([("4", [])]), fail_on={1, 2, 3, 4, 5, 6})
    r = run_agent("q", reg, ta.tool_specs(), m, retry_limit=1)
    assert r["stop"] == "api_error_429"


# ---------------------------------------------------------------- injection (W26 / W29 / W33)
def inject_run(seed, gullibility=1.0, frame=True, flag=True, strict=True, auto=True):
    assert auto, 'tests never block on stdin'
    outer = tempfile.mkdtemp(prefix="l4_inj_")
    sb = Sandbox(os.path.join(outer, "a", "box"), strict=strict)     # "../../exfil.txt" lands in outer/
    model = GullibleModel(ScriptedModel(reminder_plan()), gullibility=gullibility, seed=seed)
    r = run_agent("What reminders did I write to myself?", registry(sb, poisoned=True),
                  ta.tool_specs(), model, auto_approve=auto, frame_results=frame, flag_injections=flag)
    return r, sb, outer


def test_find_imperative_grammar():
    assert ta.find_imperative('x call write_file(filename="a.md", content="hi there") y') == \
        ("write_file", {"filename": "a.md", "content": "hi there"})
    assert ta.find_imperative("the file was written") is None
    assert ta.find_imperative(rag.NOTEBOOK) is None                      # no false alarms on the clean notes


def test_honest_model_ignores_poison():
    r = run_agent("reminders?", registry(Sandbox(), poisoned=True), ta.tool_specs(),
                  ScriptedModel(reminder_plan()), auto_approve=True)
    assert r["obeyed"] == [] and [c["tool"] for c in r["tool_calls"]] == ["search_notes"]
    assert r["trace"][2]["injection_flags"] != []                        # the detector saw it


def test_capability_layer_holds_when_model_is_fully_fooled():
    r, sb, outer = inject_run(0, gullibility=1.0, frame=False, flag=False)
    assert r["obeyed"] and r["obeyed"][0][0] == "write_file"             # model WAS fooled
    wf = [c for c in r["tool_calls"] if c["tool"] == "write_file"]
    assert len(wf) == 1 and wf[0]["is_error"] is True
    assert not os.path.exists(os.path.join(outer, "exfil.txt")) and sb.escaped() == []


def test_weak_sandbox_lets_the_injection_land():
    r, sb, outer = inject_run(0, gullibility=1.0, frame=False, flag=False, strict=False)
    assert len(sb.escaped()) == 1 and os.path.exists(os.path.join(outer, "exfil.txt"))
    assert sb.attempts and sb.attempts[0][2] is True


def test_confirmation_is_a_capability_layer_too():
    # auto_approve False and stdin not a human (declines on EOF) -> nothing written even with a weak sandbox
    old = sys.stdin; sys.stdin = open(os.devnull)
    try:
        model = GullibleModel(ScriptedModel(reminder_plan()), gullibility=1.0, seed=0)
        sb2 = Sandbox(strict=False)
        r = run_agent("reminders?", registry(sb2, poisoned=True), ta.tool_specs(), model, frame_results=False, flag_injections=False)
    finally:
        sys.stdin = old
    assert r["obeyed"] and sb2.attempts == []


def test_gullibility_dial_and_discounts_are_seeded_rates():
    def frac(n=100, **kw):
        return sum(bool(inject_run(s, **kw)[0]["obeyed"]) for s in range(n)) / n
    assert frac(gullibility=0.0) == 0.0 and frac(gullibility=1.0, frame=False, flag=False) == 1.0
    bare = frac(gullibility=0.5, frame=False, flag=False)
    both = frac(gullibility=0.5, frame=True, flag=True)        # 0.5 * 0.6 * 0.5 = 0.15
    assert 0.35 < bare < 0.65 and both < bare and both < 0.3
    assert frac(gullibility=0.5, frame=False, flag=False) == bare       # same seeds, same answer


def test_models_label_themselves():
    for m in (ScriptedModel([]), GullibleModel(ScriptedModel([]))):
        assert "stand-in, not a model" in repr(m)
    assert ta.ModelTurn().standin == "stand-in, not a model"


if __name__ == "__main__":
    n = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); n += 1; print("ok", name)
    print(f"{n} tests passed")
