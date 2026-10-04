"""STAND-IN, NOT A MODEL: anthropic-shaped shim for the capstone spine. Extractive generator over
<untrusted_data> passages formatted '[id] (similarity s)\\n text'. Same rule as m06_stub."""
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import stub_anthropic as sa
class APIStatusError(Exception): status_code = 500
def policy(system, user, kw):
    passages = re.findall(r"\[(\d+)\] \(similarity [0-9.]+\)\n(.*?)(?=\n\n\[\d+\] \(similarity|\n</untrusted_data>)", user, re.S)
    q = user.split("Question:")[-1]
    qw = {w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) > 3}
    best = (0, None, None)
    for cid, body in passages:
        for s in re.split(r"(?<=[.!?])\s+", body.replace("\n", " ")):
            ov = len(qw & set(re.findall(r"[a-z0-9]+", s.lower())))
            if ov > best[0]: best = (ov, cid, s)
    return "NOT_IN_SOURCES" if best[0] < 1 else f"{best[2]} [{best[1]}]"
def Anthropic(): return sa.StubAnthropic(policy=policy)
