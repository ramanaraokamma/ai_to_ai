"""STAND-IN, NOT A MODEL. Extractive RAG 'generator' for module 06/07/09 ledgers.
Rule: among the <source id=N> blocks in the user turn, take the sentence with the largest word
overlap (words >3 chars) with the question; answer = that sentence + ' [N]'. No overlap>=1 -> 'NOT IN NOTES'.
Honours fault switches: cite_wrong_id, no_citation, ignore_sources (returns a fixed uncited sentence)."""
import re, stub_anthropic as sa

FAULT = {"cite_wrong_id": False, "no_citation": False, "ignore_sources": False}

def rag_policy(system, user, kw):
    srcs = re.findall(r'<source id="(\d+)"[^>]*>\n(.*?)\n</source>', user, re.S)
    q = user.split("Question:")[-1]
    if FAULT["ignore_sources"]: return "The answer is probably 42."
    if not srcs: return "NOT IN NOTES"
    qw = {w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) > 3}
    best = (0, None, None)
    for sid, body in srcs:
        for s in re.split(r"(?<=[.!?])\s+", body.replace("\n", " ")):
            ov = len(qw & set(re.findall(r"[a-z0-9]+", s.lower())))
            if ov > best[0]: best = (ov, sid, s)
    if best[0] < 1: return "NOT IN NOTES"
    sid = "99" if FAULT["cite_wrong_id"] else best[1]
    return best[2] if FAULT["no_citation"] else f"{best[2]} [{sid}]"

def client(): return sa.StubAnthropic(policy=rag_policy)
