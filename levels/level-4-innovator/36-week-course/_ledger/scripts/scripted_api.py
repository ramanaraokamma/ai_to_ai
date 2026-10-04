"""STAND-IN, NOT A MODEL.  `anthropic`-shaped shim whose 'model' is a deterministic scripted policy.
Replaces `import anthropic` in agent.py. It returns real-shaped content blocks (text / tool_use with ids),
stop_reason 'tool_use' or 'end_turn', and usage = ceil(words*1.3) over system + tool specs + every message
(the whole conversation is re-counted each turn, so the k^2 input growth shape is real but the token
values are the stand-in's, not Claude's tokenizer).
A policy is  policy(messages) -> (text, [(tool_name, args_dict), ...])   ; empty tool list = finish.
Switch policies with scripted_api.POLICY = fn.   GullibleModel-style behaviour is one such policy."""
import json, math, re

class RateLimitError(Exception): pass
class APIStatusError(Exception): status_code = 500

POLICY = None
_ids = iter(range(1, 10**6))

class Blk:
    def __init__(self, **kw): self.__dict__.update(kw)

def _ser(x):
    if isinstance(x, str): return x
    if isinstance(x, list): return " ".join(_ser(i) for i in x)
    if isinstance(x, dict): return " ".join(_ser(v) for v in x.values())
    if hasattr(x, "__dict__"): return _ser(x.__dict__)
    return str(x)

def _ntok(s): return math.ceil(len(s.split()) * 1.3)

class _U:
    def __init__(s, i, o): s.input_tokens, s.output_tokens = i, o
class _R:
    def __init__(s, content, stop, i, o): s.content, s.stop_reason, s.usage = content, stop, _U(i, o)

class _Msgs:
    def create(self, model=None, max_tokens=1024, system="", messages=(), tools=None, **kw):
        n_in = _ntok(system) + _ntok(_ser(tools or [])) + _ntok(_ser(list(messages)))
        text, calls = POLICY(list(messages), tools=tools)
        content = []
        if text: content.append(Blk(type="text", text=text))
        for name, args in calls:
            content.append(Blk(type="tool_use", id=f"toolu_{next(_ids):03d}", name=name, input=args))
        n_out = _ntok(text) + sum(_ntok(json.dumps(a)) + 4 for _, a in calls)
        return _R(content, "tool_use" if calls else "end_turn", n_in, n_out)

class Anthropic:
    def __init__(self): self.messages = _Msgs()

# ---- helpers for policies --------------------------------------------------
def tool_results(messages):
    """All tool_result strings so far, in order (ids stripped)."""
    out = []
    for m in messages:
        if m["role"] == "user" and isinstance(m["content"], list):
            out += [r["content"] for r in m["content"]]
    return out

def n_assistant(messages): return sum(m["role"] == "assistant" for m in messages)
