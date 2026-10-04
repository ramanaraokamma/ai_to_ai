"""STAND-IN, NOT A MODEL.  Local stub replacing `anthropic.Anthropic()` for the ledger.

What it does (nothing here is learned behaviour; every rule is written below):
  * messages.create(model, max_tokens, system, messages, **kw) -> object with
      .content[0].text / .type, .stop_reason, .usage.input_tokens/.output_tokens
  * messages.count_tokens(...) -> .input_tokens
  * Token counts = ceil(len(text.split()) * 1.3)   (the plan's tinytok fallback). NOT Claude's tokenizer.
  * Policy: a keyword/regex ticket extractor.  Its 'competence' depends on prompt features only:
      - system contains 'Rules:'           -> lowercase vocabulary (else capitalised free text + chatter)
      - '<example>' anywhere in the prompt -> urgency uses a 'money/blocked' heuristic (else constant 2)
      - output_config.format present       -> raw JSON only
      - thinking present                   -> output tokens x4 (no quality change: nothing is invented)
      - 'NOT IN SOURCE' in system + <source> in user -> extractive sentence-overlap answer or NOT IN SOURCE
      - otherwise a generic one-sentence echo of the first sentence (truncated by max_tokens)
  * Other modules add their own policies by passing `policy=` to StubAnthropic.
Rates measured against it are properties of this stub, not of Claude.
"""
import json, math, re, hashlib


class _Blk:
    def __init__(self, text): self.type = "text"; self.text = text

class _Usage:
    def __init__(self, i, o): self.input_tokens = i; self.output_tokens = o
    cache_read_input_tokens = 0

class _Resp:
    def __init__(self, text, stop, i, o):
        self.content = [_Blk(text)]; self.stop_reason = stop; self.usage = _Usage(i, o)

class _Count:
    def __init__(self, n): self.input_tokens = n

class BadRequestError(Exception):
    message = "bad request (stub)"
class RateLimitError(Exception): pass


def ntok(s):
    return math.ceil(len(s.split()) * 1.3) if s else 0

def _flat(messages):
    out = []
    for m in messages:
        c = m["content"]
        out.append(c if isinstance(c, str) else " ".join(b.get("text", "") for b in c))
    return "\n".join(out)


def ticket_policy(system, user, kw):
    t = user
    ms = re.findall(r"<message>\n?(.*?)\n?</message>", user, re.S)
    if ms: t = ms[-1]
    elif "Extract category" in user: t = user.split("message as JSON:", 1)[-1]
    low = t.lower()
    oid = re.search(r"\b([A-Z]-\d{2,6})\b", t)
    oid = oid.group(1) if oid else None
    if re.search(r"charg|billed|card|twice|payment", low): cat = "billing"
    elif re.search(r"package|deliver|order .*never|showed up|arrived|shipping", low): cat = "shipping"
    elif re.search(r"crash|bug|error|app |android", low): cat = "technical"
    elif re.search(r"log in|password|account|email", low): cat = "account"
    else: cat = "other"
    refund = bool(re.search(r"refund|money back|give it back", low))
    if "<example>" in user:
        if re.search(r"urgent|now|twice|3 times|smashed|never showed|days", low) or refund: urg = 3
        elif cat == "other" or "no rush" in low or "quick q" in low: urg = 1
        else: urg = 2
    else:
        urg = 2
    rec = {"category": cat, "urgency": urg, "order_id": oid, "refund_requested": refund}
    if "Rules:" not in system:
        rec["category"] = cat.capitalize() + " issue"
    body = json.dumps(rec)
    if kw.get("output_config", {}).get("format") or "Rules:" in system:
        return body
    return "Sure! Here is the extracted record:\n```json\n" + body + "\n```"


def grounded_policy(system, user, kw):
    src = re.search(r"<source>\n(.*?)\n</source>", user, re.S)
    q = user.split("</source>")[-1].strip() if src else user
    if not src:
        return "I am not able to say."       # ungrounded stand-in: a fixed non-answer
    sents = re.split(r"(?<=[.!?])\s+", src.group(1).replace("\n", " "))
    qw = {w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) > 3}
    best = max(sents, key=lambda s: len(qw & set(re.findall(r"[a-z0-9]+", s.lower()))))
    ov = len(qw & set(re.findall(r"[a-z0-9]+", best.lower())))
    return best if ov >= 2 else "NOT IN SOURCE"


def default_policy(system, user, kw):
    if "NOT IN SOURCE" in system: return grounded_policy(system, user, kw)
    if "<message>" in user or "Extract category" in user: return ticket_policy(system, user, kw)
    if "<source>" in user: return grounded_policy(system, user, kw)
    return re.split(r"(?<=[.!?])\s+", user.strip())[0]


class _Messages:
    def __init__(self, owner): self.o = owner
    def create(self, model=None, max_tokens=1024, system="", messages=(), **kw):
        if "temperature" in kw:
            raise BadRequestError("temperature not accepted (stub mirrors module claim)")
        user = _flat(messages)
        text = self.o.policy(system if isinstance(system, str) else str(system), user, kw)
        o = ntok(text) * (4 if kw.get("thinking") else 1)
        i = ntok(system if isinstance(system, str) else str(system)) + ntok(user)
        stop = "end_turn"
        if ntok(text) > max_tokens:
            words = text.split(); text = " ".join(words[: int(max_tokens / 1.3)]); o = max_tokens; stop = "max_tokens"
        self.o.calls += 1
        return _Resp(text, stop, i, o)
    def count_tokens(self, model=None, system="", messages=(), **kw):
        return _Count(ntok(system) + ntok(_flat(messages)))


class StubAnthropic:
    def __init__(self, policy=default_policy):
        self.policy = policy; self.calls = 0; self.messages = _Messages(self)

# mimic `import anthropic; anthropic.Anthropic()`
Anthropic = StubAnthropic
