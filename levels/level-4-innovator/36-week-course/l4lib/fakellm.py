"""fakellm.py - STAND-IN, NOT A MODEL.  A scripted "LLM" with the shape of a chat API.

Used in weeks 23-36:
  * Weeks 23-24  prompt harness (frozen set, versioned prompts, constant baseline, BudgetGuard);
                 W24 re-earns the real in-context effects on a model the student TRAINS, not on this.
  * Weeks 25-26  (via rag.py) the extractive generator plugs in as this client's policy.
  * Weeks 28-29  token / cost accounting shared with toyagent.py.
  * Weeks 30-33  the frozen suite, cost tables, retry and fault drills.
  * Weeks 34-36  capstone cost-and-latency budget.

What it is
----------
``FakeClient`` exposes the surface the modules use::

    client = FakeClient(seed=0)
    r = client.messages.create(model="fake-small", max_tokens=200, system="...",
                               messages=[{"role": "user", "content": "..."}])
    r.content[0].text, r.stop_reason, r.usage.input_tokens, r.usage.output_tokens

It is NOT a language model. The "answer" is a plain Python function of features of the prompt,
written out in this file, so a student can read every rule. Its competence is a DOCUMENTED function
(see ``competence``):

    p_correct = clamp(BASE + W_RULES*has_rules + W_EXAMPLE*min(n_examples, 3)
                           + W_SCHEMA*has_schema - error_rate, 0, 1)

Each field of an answer is independently wrong with probability ``1 - p_correct``, decided by a
seeded hash of (seed, prompt text, field name). Same prompt + same seed -> same answer, always.
Rates measured against this client are properties of this file, not of any real model. We model the
mechanism (prompt features change results; tokens cost money; calls fail), not the rate.

Honesty labels
--------------
Every client and every response carries the label ``"stand-in, not a model"``: in ``repr(client)``,
in ``repr(response)``, in ``response.metadata["label"]`` and in ``client.usage_log``. The label is
deliberately NOT put inside ``content[0].text`` because that would corrupt the parsers being taught.

Tokens and money
----------------
Tokens are counted locally: ``tinytok.count`` if that module exists, else ``ceil(words * 1.3)``.
Dollar amounts use ``PRICE_TABLE``, which is ILLUSTRATIVE (round numbers, not any vendor's bill).

Prefix cache
------------
If the start of this prompt (system + messages, compared word by word) matches a previous prompt,
those tokens are reported as ``usage.cache_read_input_tokens`` (billed at ``CACHE_READ_FACTOR`` of
the input price) and are NOT included in ``usage.input_tokens``. Total prompt size is
``input_tokens + cache_read_input_tokens``.

Faults
------
``fail_on={3: RateLimit}`` raises on the 3rd call (1-based). ``forbid_temperature=True`` makes a
``temperature=`` argument raise ``BadRequest``, simulating ONE vendor's rule (a labelled simulation,
not a universal fact).
"""
import hashlib
import json
import math
import re

LABEL = "stand-in, not a model"

# dollars per MILLION tokens: (input, output).  ILLUSTRATIVE, not a real price list.
PRICE_TABLE = {
    "fake-small": (1.00, 5.00),
    "fake-large": (3.00, 15.00),
}
CACHE_READ_FACTOR = 0.1

# competence constants (see `competence`)
BASE, W_RULES, W_EXAMPLE, W_SCHEMA = 0.55, 0.15, 0.08, 0.05


# ---------------------------------------------------------------- tokens
def count_tokens(text):
    """Local token count: tinytok if available, else ceil(words * 1.3). Never a download."""
    if not text:
        return 0
    try:
        try:
            from . import tinytok
        except ImportError:  # run as a plain script from inside l4lib
            import tinytok
        return int(tinytok.count(text))
    except Exception:
        return math.ceil(len(text.split()) * 1.3)


def cost_usd(model, input_tokens, output_tokens, cache_read_tokens=0):
    """Illustrative dollars for one call under PRICE_TABLE."""
    p_in, p_out = PRICE_TABLE.get(model, PRICE_TABLE["fake-small"])
    return (input_tokens * p_in + cache_read_tokens * p_in * CACHE_READ_FACTOR
            + output_tokens * p_out) / 1e6


# ---------------------------------------------------------------- errors
class FakeAPIError(Exception):
    """Base class for injected faults. Carries status_code like a real HTTP error would."""
    status_code = 500


class RateLimit(FakeAPIError):
    status_code = 429


class BadRequest(FakeAPIError):
    status_code = 400


# ---------------------------------------------------------------- response
class _Block:
    def __init__(self, text):
        self.type = "text"
        self.text = text

    def __repr__(self):
        return f"TextBlock({self.text!r})"


class Usage:
    def __init__(self, input_tokens, output_tokens, cache_read):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_read_input_tokens = cache_read

    def __repr__(self):
        return (f"Usage(input_tokens={self.input_tokens}, output_tokens={self.output_tokens}, "
                f"cache_read_input_tokens={self.cache_read_input_tokens})")


class Response:
    def __init__(self, text, stop_reason, usage, model, stop_sequence=None, call_index=0):
        self.content = [_Block(text)]
        self.stop_reason = stop_reason
        self.stop_sequence = stop_sequence
        self.usage = usage
        self.model = model
        self.cost = cost_usd(model, usage.input_tokens, usage.output_tokens,
                             usage.cache_read_input_tokens)
        self.metadata = {"label": LABEL, "standin": True, "call_index": call_index,
                         "price_table": "illustrative"}

    @property
    def text(self):
        return self.content[0].text

    def __repr__(self):
        return (f"<Response [{LABEL}] stop={self.stop_reason} {self.usage} "
                f"cost=${self.cost:.6f}>")


# ---------------------------------------------------------------- features
def flatten(messages):
    """Join message contents (str or list of {'text': ...} blocks) into one string."""
    out = []
    for m in messages:
        c = m["content"]
        out.append(c if isinstance(c, str) else " ".join(
            b.get("text", "") if isinstance(b, dict) else getattr(b, "text", "") for b in c))
    return "\n".join(out)


def features(system, user):
    """The prompt features the policy is allowed to look at. Nothing else influences the answer."""
    return {
        "has_rules": bool(re.search(r"\brules?:", system, re.I)),
        "n_examples": len(re.findall(r"<example>", system + "\n" + user)),
        "has_schema": bool(re.search(r"\bschema\b|\bjson\b", system, re.I)),
        "has_source": "<source" in user,
        "says_not_in_source": bool(re.search(r"NOT[ _]IN[ _](SOURCES?|NOTES)", system)),
        "n_words": len((system + " " + user).split()),
    }


def competence(feats, error_rate=0.0):
    """P(a field is right). Documented, linear, clamped. Read it; it is the whole 'skill'."""
    p = (BASE + W_RULES * feats["has_rules"] + W_EXAMPLE * min(feats["n_examples"], 3)
         + W_SCHEMA * feats["has_schema"] - error_rate)
    return max(0.0, min(1.0, p))


def _u(seed, *parts):
    """Deterministic uniform [0,1) from (seed, parts) - sha256, never Python's salted hash()."""
    h = hashlib.sha256(("|".join(map(str, (seed,) + parts))).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


# ---------------------------------------------------------------- default policy
_CATS = ["billing", "shipping", "technical", "account", "other"]


def _true_ticket(text):
    low = text.lower()
    oid = re.search(r"\b([A-Z]-\d{2,6})\b", text)
    if re.search(r"charg|billed|card|twice|payment", low):
        cat = "billing"
    elif re.search(r"package|deliver|never (?:showed|arrived)|arrived|shipping", low):
        cat = "shipping"
    elif re.search(r"crash|bug|error|\bapp\b|android", low):
        cat = "technical"
    elif re.search(r"log in|password|account|email", low):
        cat = "account"
    else:
        cat = "other"
    refund = bool(re.search(r"refund|money back|give it back", low))
    if re.search(r"urgent|now|twice|3 times|smashed|never showed|days", low) or refund:
        urg = 3
    elif cat == "other" or "no rush" in low or "quick q" in low:
        urg = 1
    else:
        urg = 2
    return {"category": cat, "urgency": urg, "order_id": oid.group(1) if oid else None,
            "refund_requested": refund}


def _corrupt(field, value):
    """The specific wrong value a field takes when the dice say 'wrong' (deterministic)."""
    if field == "category":
        return _CATS[(_CATS.index(value) + 1) % len(_CATS)]
    if field == "urgency":
        return 1 if value != 1 else 2
    if field == "order_id":
        return None if value else "X-000"
    return not value


def ticket_policy(system, user, feats, seed, p):
    msgs = re.findall(r"<message>\n?(.*?)\n?</message>", user, re.S)
    text = msgs[-1] if msgs else user
    rec = _true_ticket(text)
    for f in list(rec):
        if _u(seed, text, f) >= p:
            rec[f] = _corrupt(f, rec[f])
    body = json.dumps(rec)
    if feats["has_rules"] or feats["has_schema"]:
        return body
    return "Sure! Here is the extracted record:\n```json\n" + body + "\n```"


def default_policy(system, user, feats, seed, p):
    """Routes on prompt features: ticket extraction, grounded answer, or a one-sentence echo."""
    if feats["has_source"]:
        try:
            from . import rag
        except ImportError:
            import rag
        return rag.extractive_answer_from_prompt(user)
    if "<message>" in user or "Extract" in user:
        return ticket_policy(system, user, feats, seed, p)
    return re.split(r"(?<=[.!?])\s+", user.strip())[0] if user.strip() else ""


# ---------------------------------------------------------------- client
class _Messages:
    def __init__(self, owner):
        self._o = owner

    def create(self, model="fake-small", max_tokens=1024, system="", messages=(),
               stop_sequences=None, temperature=None, **kw):
        return self._o._create(model, max_tokens, system, list(messages), stop_sequences,
                               temperature, kw)

    def count_tokens(self, model="fake-small", system="", messages=(), **kw):
        n = count_tokens(str(system)) + count_tokens(flatten(list(messages)))
        return type("TokenCount", (), {"input_tokens": n})()


class FakeClient:
    """Scripted stand-in with the ``messages.create`` surface. See module docstring.

    policy(system, user, feats, seed, p_correct) -> str   replaces default_policy.
    error_rate   extra probability subtracted from p_correct (0.0 - 1.0).
    fail_on      {call_number: exception class or instance}, 1-based.
    """

    def __init__(self, policy=None, seed=0, error_rate=0.0, fail_on=None,
                 forbid_temperature=False, prefix_cache=True, min_cache_words=5):
        self.policy = policy or default_policy
        self.seed = seed
        self.error_rate = error_rate
        self.fail_on = dict(fail_on or {})
        self.forbid_temperature = forbid_temperature
        self.prefix_cache = prefix_cache
        self.min_cache_words = min_cache_words
        self.calls = 0
        self.usage_log = []
        self._seen = []
        self.messages = _Messages(self)

    def __repr__(self):
        return f"<FakeClient [{LABEL}] seed={self.seed} calls={self.calls}>"

    # -- bookkeeping ----------------------------------------------------
    def total_tokens(self):
        return (sum(u["input_tokens"] + u["cache_read"] for u in self.usage_log),
                sum(u["output_tokens"] for u in self.usage_log))

    def total_cost(self):
        return sum(u["cost"] for u in self.usage_log)

    # -- the call -------------------------------------------------------
    def _create(self, model, max_tokens, system, messages, stop_sequences, temperature, kw):
        self.calls += 1
        n = self.calls
        if n in self.fail_on:
            e = self.fail_on[n]
            raise e(f"injected fault on call {n} ({LABEL})") if isinstance(e, type) else e
        if not messages:
            raise BadRequest("messages must be non-empty")
        if any(m.get("role") not in ("user", "assistant") for m in messages):
            raise BadRequest("role must be 'user' or 'assistant'")
        if not isinstance(max_tokens, int) or max_tokens < 1:
            raise BadRequest("max_tokens must be a positive integer")
        if temperature is not None and self.forbid_temperature:
            raise BadRequest("temperature not accepted (simulating ONE vendor's rule, "
                             f"{LABEL})")
        system = system if isinstance(system, str) else flatten([{"content": system}])
        user = flatten(messages)
        feats = features(system, user)
        p = competence(feats, self.error_rate)
        text = self.policy(system, user, feats, self.seed, p)

        prompt_words = (system + "\n" + user).split()
        cache_words = self._cache_match(prompt_words) if self.prefix_cache else 0
        cache_read = math.ceil(cache_words * 1.3) if cache_words >= self.min_cache_words else 0
        total_in = count_tokens(system) + count_tokens(user)
        cache_read = min(cache_read, total_in)
        self._seen.append(prompt_words)

        stop_reason, hit = "end_turn", None
        for s in (stop_sequences or []):
            i = text.find(s)
            if i != -1 and (hit is None or i < text.find(hit)):
                hit = s
        if hit is not None:
            text, stop_reason = text[:text.find(hit)], "stop_sequence"
        out_tok = count_tokens(text)
        if out_tok > max_tokens:
            words = text.split()
            text = " ".join(words[:max(0, int(max_tokens / 1.3))])
            out_tok, stop_reason, hit = max_tokens, "max_tokens", None

        usage = Usage(total_in - cache_read, out_tok, cache_read)
        resp = Response(text, stop_reason, usage, model, stop_sequence=hit, call_index=n)
        self.usage_log.append({"call": n, "label": LABEL, "model": model,
                               "input_tokens": usage.input_tokens, "cache_read": cache_read,
                               "output_tokens": out_tok, "cost": resp.cost})
        return resp

    def _cache_match(self, words):
        best = 0
        for prev in self._seen:
            k = 0
            for a, b in zip(prev, words):
                if a != b:
                    break
                k += 1
            best = max(best, k)
        return best
