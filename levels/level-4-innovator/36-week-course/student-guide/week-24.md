# Week 24 — Examples, Scratchpads, and Schemas: Learned in Context

[⬅ Week 23](week-23.md) · [Course Home](../README.md) · [Week 25 ➡](week-25.md) · [Workbook](../workbook/week-24.md)

---

> ### This week in one sentence
> **A small transformer that you train yourself can learn to use the examples in its prompt, and to show its working before its answer, but the best it can score is a line you can compute by hand, one seed is one roll of the dice, and a schema that forces the shape of a reply never forces it to make sense.**
>
> **By the end of this chapter you will be able to:**
> - **Compute the best possible score before training anything**: `(n + 1) / 6` when `n` of 6 pairs are shown (`0.167` for none, `0.667` for three, `1.000` for six)
> - **Train a model to use examples in its prompt** and plot its accuracy against that line (ours scores `0.176` with no examples and `0.638` with three)
> - **Compare a model that answers at once with one that writes its working first**, on the same size and the same number of steps (exact match `0.000` against `1.000`), and say why one seed is not enough to believe either
> - **Write a mask with `torch.where`** that lets a model type only characters a grammar allows, and measure what it fixes (every reply parses: `100` of `100`) and what it cannot (`26` of `100` fully right on names it never saw)
>
> **New maths:** **none.** One habit of arithmetic: work out the best possible score first, then look at yours.
>
> **New syntax:** `random.Random(seed)` · `hashlib.sha256` · `torch.where(condition, a, b)`
>
> **New words:** in-context learning · zero-shot / few-shot · best possible score (ceiling) · scratchpad · schema · logit · logit mask · prefix · cache key
>
> **Reading time:** about 45 minutes. **In class:** about 70 minutes (about four minutes of it is a model training while you talk). **Homework (the workbook):** about 60-75 minutes.

> **📌 About the code blocks.** Nine files this week, each a whole file with its name in the first line. Type them into **one folder**. **That folder must contain two things from earlier weeks:** `l4lib/` (the shared kit) and **your own `tinygpt.py` from Week 17, unchanged**. Only the sizes differ today: width 64, 2 blocks, instead of Week 17's bigger model. Run them in this order: `constructs.py` and `cachekey.py` stand alone; `incontext_run.py` imports `icl.py`; `scratchpad_run.py` imports `addlib.py`; `jsonmask_run.py` imports `jsonlib.py`, which imports `grammar.py`. **`grammar.py` is given to you to read; you do not have to type it.** Every output shown was printed by a real run on a CPU, one thread, with the seeds shown. Nothing needs the internet. Training is the same every time on one machine, so **your numbers should match ours**; on another machine the last digit or two can differ, and the seconds will. If your `47d6a3db7a1a` fingerprint below matches and a number at the top of a curve differs, that is not a bug: see "one seed is one roll" in the box after the first table.
>
> **⚠️ One stand-in, and only one.** Last week the "model" was a script. **This week there is no script in any measured number**: the three models are real neural networks of about a hundred thousand knobs each, trained from scratch by you in a couple of minutes. The only stand-in is one line in `cachekey.py`, where `FakeClient` (labelled **stand-in, not a model**) counts tokens for a ten-second demonstration. **Being real does not make these models about ChatGPT.** What you measure is what three tiny models do on three made-up jobs.

---

![Map of the 36 weeks with Week 24, Examples, Scratchpads, and Schemas: Learned in Context, highlighted in Term 3](../figures/fig-w24-0-where-this-fits.svg)
*Figure 24.0 — Week 24 is the sixth lesson of Term 3: what changes when only the prompt changes.*

## 🪝 Start Here

Last week a scorer learned to love examples, and the reason was that we wrote it to. The table could never answer the question *"do examples in a prompt actually help a model?"* Today you answer it on a model you trained.

To answer it you need three things: **a model**, **a job where examples could matter**, and **a way to say how good is good enough**. The job is a card game.

```text
examples:   b 3     e 0     a 4
question:   e ?                       answer 0   (it is on the page)
question:   c ?                       answer ?   (it is NOT on the page; the unused digits are 1, 2, 5)
```

There are six letters, `a` to `f`, and six digits, `0` to `5`, each digit used once. A **secret code** pairs them in a random order, and **a fresh code is made for every prompt**. I show you some pairs, then ask about one letter. You have never seen this code before.

Before you touch a laptop, write four guesses on a card.

1. If I show **0** pairs and ask about one letter, what is the **best possible** accuracy? Not what you hope for: the best anyone could do.
2. The same for **1** pair shown.
3. The same for **3** pairs shown.
4. The same for **all 6** shown.

Keep the card. We come back to it at the end.

---

## 🧠 The Big Idea

This section defines the four ideas the labs use: in-context learning, the ceiling, the scratchpad, and the schema with its mask.

### In-context learning

In Week 22 you changed a model's knobs: that is training. Today the knobs are **frozen** and all that changes is the text you put in front of the model. When a model uses what is on the page to answer, that is **in-context learning**. A prompt with no worked examples is **zero-shot**; with a few, **few-shot**. A "shot" is one worked example.

There is small print, and it is the honest frame of the whole week: **a model can only do this if its training taught it to.** Ours will train on thousands of different random codes and then be tested on prompts it has never seen: a fresh code, a fresh choice of shown pairs and a fresh key each time. (There are only 720 possible codes, so it has very likely met every code during training; what it cannot have met is this exact prompt.) Last week's lookup task (Week 19) was easier: the key was always on the page. Today it may or may not be.

### The ceiling

How well can *anyone* do? Take three pairs shown, one letter asked.

- **Half the time** (3 times in 6) the asked letter is one of the three shown. The answer is on the page, so a good player is right every time.
- **The other half** the letter was not shown. The three digits already used are ruled out, because each digit appears once, so the answer is one of the three left: a guess, right one time in three.

Add them: `3/6 x 1 + 3/6 x 1/3 = 0.500 + 0.167 = 0.667`. For `n` pairs shown the same argument gives one line:

```text
best possible  =  n/6 x 1  +  (6 - n)/6 x 1/(6 - n)  =  (n + 1) / 6
```

That is `0.167, 0.333, 0.500, 0.667, 0.833, 1.000, 1.000` for `n = 0` to `6`. **Nothing a model does can beat this line**, however big it is. A score above it means noise or a leak. How much noise? With 500 test prompts, a score wobbles by about two to four points either way, so `0.686` at `n = 3` is not "above the ceiling".

Call this line the **ceiling** (or the **best possible score**). You met the idea in Week 23 as a number for one dataset; today you compute it from the rules of the task, before training anything.

### A scratchpad

Can you add `48,391 + 76,254` in your head and say only the answer? On paper you write the working: column by column, right to left, with a carry. A **scratchpad** is working written out *before* the answer. We will train two models of the same size for the same number of steps: one must write the six-digit answer at once, the other writes the working first.

### A schema and a mask

Suppose you need a reply as JSON. You can ask nicely, or you can make it *impossible to type a wrong character*. A **schema** is the shape a reply must have. A **logit** is a model's score for a next character before the softmax turns scores into chances (you have called these "scores" since Week 13). A **logit mask** sets the score of every forbidden character to minus infinity, so its chance becomes exactly `0`. Forcing the model to obey a schema this way is **constrained decoding**. What does that fix, and what can it not? Hold the question; it is the last lab.

---

## 💻 The Code

This section builds the week's experiments in order, one file at a time, with the output each one printed on our machine.

### 1. The three new constructs

Three pieces of syntax, each on a toy small enough to read. Before you run `constructs.py`, write a prediction next to each of (a), (b), (c).

**(a) `random.Random(seed)`: your own private dice.** Python's `random` module has one shared dice that nobody seeded, so two runs give different numbers. `random.Random(7)` builds **a dice of your own**. Two of them with the same seed roll the same numbers, and neither disturbs torch's dice. You can say it as *"a dice with my name on it"*. Today's design uses it so that **the test prompts and the training prompts never share dice**: the test set comes out the same on every run.

**(b) `hashlib.sha256`: a fingerprint.** You met `hashlib.md5` in Week 21 to catch duplicates. `sha256` is the same idea with a longer fingerprint (64 hex characters; we keep 12). Same text, same fingerprint; one letter changed, one that looks completely different.

**(c) `torch.where(condition, a, b)`: choose, place by place.** Where `condition` is `True` take the number from `a`, where it is `False` take it from `b`. It is Week 15's causal mask, `masked_fill(mask == 0, -inf)`, with the choice written out.

**Predict first:** (a) two dice both made with `Random(7)`: the same five rolls or different? Do a hundred rolls of a private dice move torch's own `manual_seed(0)` sequence? (b) change one letter: how much of the fingerprint changes? (c) what is the softmax of `[2, 1, -inf, -inf]`?

**`constructs.py`**

```python
# constructs.py - Week 24: the three new constructs, each on a toy small enough to read.
import hashlib
import random
import torch

# (a) random.Random(seed): a private dice. Two of them with the same seed roll the same numbers,
#     and neither touches torch's seed or anybody else's dice.
dice = random.Random(7)
print("roll five      :", [dice.randint(1, 6) for _ in range(5)])
twin = random.Random(7)
print("twin, same five:", [twin.randint(1, 6) for _ in range(5)])
torch.manual_seed(0)
expected = torch.rand(2)                                           # torch's own two numbers, with nothing in between
torch.manual_seed(0)
first = torch.rand(1)
_ = [random.Random(7).randint(1, 6) for _ in range(100)]          # a hundred rolls of a private dice ...
second = torch.rand(1)
print("torch unmoved  :", first.item() == expected[0].item() and second.item() == expected[1].item())   # ... did not disturb torch
letters = list("abcdef")
random.Random(3).shuffle(letters)                                  # shuffle changes the list IN PLACE
print("shuffled       :", letters)
print("choice, sample :", random.Random(3).choice("abcdef"), random.Random(3).sample("abcdef", 2))

# (b) hashlib.sha256: text in, a fixed-length fingerprint out. Same text, same fingerprint; one letter changed, a different one.
def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

print("fingerprint 1  :", fingerprint("a3b1c0d2"))
print("same text      :", fingerprint("a3b1c0d2"))
print("one letter off :", fingerprint("a3b1c0d3"))
print("length of full :", len(hashlib.sha256(b"x").hexdigest()), "hex characters; we keep 12")

# (c) torch.where(condition, a, b): for every place, take a where the condition is True, b where it is False.
scores = torch.tensor([2.0, 1.0, 0.5, 3.0])
allowed = torch.tensor([True, True, False, False])
print("plain softmax  :", [round(p, 3) for p in torch.softmax(scores, dim=0).tolist()])
masked = torch.where(allowed, scores, torch.tensor(float("-inf")))
print("masked scores  :", masked.tolist())
print("masked softmax :", [round(p, 3) for p in torch.softmax(masked, dim=0).tolist()])
print("same as Wk 15  :", torch.equal(masked, scores.masked_fill(allowed == False, float("-inf"))))
```

```text
roll five      : [3, 2, 4, 6, 1]
twin, same five: [3, 2, 4, 6, 1]
torch unmoved  : True
shuffled       : ['a', 'c', 'd', 'f', 'e', 'b']
choice, sample : b ['b', 'e']
fingerprint 1  : 4dd9459a127c
same text      : 4dd9459a127c
one letter off : 377bc58b5592
length of full : 64 hex characters; we keep 12
plain softmax  : [0.232, 0.085, 0.052, 0.631]
masked scores  : [2.0, 1.0, -inf, -inf]
masked softmax : [0.731, 0.269, 0.0, 0.0]
same as Wk 15  : True
```

Read the second line again: the twin dice give the same five rolls. Read `torch unmoved`: a hundred rolls of a private dice did not disturb torch. `shuffled` shows the list **after** `shuffle` changed it: `shuffle` works **in place** and gives back nothing. The fingerprint of the changed text looks nothing like the first (only one of the 12 characters happens to match, by luck): it is not "close". And `-inf` is a score so low that `exp` of it is zero, so the last two chances are exactly `0.0`.

### 2. The codes: `icl.py`

Type this file whole. It prints nothing. Most of it is Weeks 1-17 again; here is what is new.

- `new_table(rng)` makes a fresh secret code. `rng.shuffle(vals)` changes the list in place; `dict(zip(KEYS, vals))` pairs the six letters with the shuffled digits.
- `stream(rng)` is **training text**: 12 pairs about one secret code. Keys repeat, so a value can be guessed once its key has been seen. That is what teaches the model to read the page.
- `make_prompt(rng, n)` shows `n` different pairs (`rng.sample(KEYS, n)`), then asks one key. It returns the prompt, the right answer, and whether the asked key was shown.
- The **test set** uses `random.Random(1000 + n)`: one private dice per `n`, 500 prompts each, the same every run, and different from everything training will roll. Its `sha256` fingerprint lets you check that your test set is the same as ours.
- In `train_model`, `guess = logits[:, 0::2]` and `truth = x[:, 1::2]`: the places that hold a **key** predict the character after them, a **value**. That is Week 12's shift by one, done with a step of two. Keys are never scored: a key is random.
- `float("nan")` means "not a number". It is printed where there was nothing to average.

**`icl.py`**

```python
# icl.py - Week 24: everything for the in-context experiment. It prints nothing; other files import it.
import hashlib
import math
import random
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT                       # YOUR Week 17 file, unchanged

torch.set_num_threads(1)

KEYS, VALS = "abcdef", "012345"                   # six keys, six values
CHARS = KEYS + VALS
stoi = {c: i for i, c in enumerate(CHARS)}
K = len(KEYS)
PAIRS = 12                                        # a training stream is 12 pairs: 24 characters


def new_table(rng):
    vals = list(VALS)
    rng.shuffle(vals)                             # a fresh secret code for every prompt
    return dict(zip(KEYS, vals))


def stream(rng):
    """Training text: 12 pairs about ONE secret table. Keys repeat, so a value is guessable once its key has been seen."""
    table = new_table(rng)
    return "".join(k + table[k] for k in [rng.choice(KEYS) for _ in range(PAIRS)])


def make_prompt(rng, n):
    """n different example pairs, then one query key. Returns (prompt, right answer, was the query key shown?)."""
    table = new_table(rng)
    shown = rng.sample(KEYS, n)
    query = rng.choice(KEYS)
    return "".join(k + table[k] for k in shown) + query, table[query], query in shown


TEST = {}
for n in range(K + 1):
    rng = random.Random(1000 + n)                 # one private dice per n: the test never shares dice with training
    TEST[n] = [make_prompt(rng, n) for _ in range(500)]
TEST_FINGERPRINT = hashlib.sha256(repr(TEST).encode("utf-8")).hexdigest()[:12]


def train_model(seed, steps, batch=64, log_every=0, lr=2e-3):
    torch.manual_seed(seed)
    rng = random.Random(seed)                     # the training dice: different from every test dice
    model = TinyGPT(len(CHARS), 64, 4, 2, 2 * PAIRS)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1, (s + 1) / 200) * 0.5 * (1 + math.cos(math.pi * s / steps)))
    for step in range(steps):
        x = torch.tensor([[stoi[c] for c in stream(rng)] for _ in range(batch)])       # (64, 24)
        logits, _ = model(x)
        guess = logits[:, 0::2]                   # the places that hold a KEY predict the character after it: a value
        truth = x[:, 1::2]
        loss = F.cross_entropy(guess.reshape(-1, len(CHARS)), truth.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if log_every and (step % log_every == 0 or step == steps - 1):
            print(f"  step {step:5d}  loss {loss.item():.3f}")
    return model


@torch.no_grad()
def evaluate(model, n):
    """Accuracy on the frozen prompts with n examples: (all, query was shown, query was not shown)."""
    cases = TEST[n]
    x = torch.tensor([[stoi[c] for c in p] for p, a, shown in cases])
    logits, _ = model(x)
    said = logits[:, -1].argmax(dim=-1)
    right = [int(said[i]) == stoi[a] for i, (p, a, shown) in enumerate(cases)]
    on_shown = [r for r, (p, a, shown) in zip(right, cases) if shown]
    on_unseen = [r for r, (p, a, shown) in zip(right, cases) if not shown]
    def mean(v):
        return sum(v) / len(v) if v else float("nan")
    return mean(right), mean(on_shown), mean(on_unseen)


def ceiling(n):
    """Best any player could do: copy when the key was shown, guess among the K - n unused values otherwise."""
    return 1.0 if n >= K else (n + 1) / K
```

### 3. Train it and plot it: `incontext_run.py`

**Write the `(n + 1) / 6` column on your card before you run this.** Then run it. It trains for about 100 seconds (8,000 steps, one CPU thread), so do the next section while you wait.

**`incontext_run.py`**

```python
# incontext_run.py - Week 24: train, then measure accuracy with 0 ... 6 examples in the prompt. (CPU, one thread.)
import time
import matplotlib.pyplot as plt
from icl import TEST, TEST_FINGERPRINT, train_model, evaluate, ceiling, K

print("frozen test set fingerprint:", TEST_FINGERPRINT, "  prompts per n:", len(TEST[0]))
t0 = time.time()
model = train_model(seed=0, steps=8000, log_every=1000)
print(f"trained in {time.time() - t0:.0f} s")

print(" n  all   ceiling  key-shown  key-unseen")
alls = []
for n in range(K + 1):
    a, s, u = evaluate(model, n)
    alls.append(a)
    print(f"{n:2d}  {a:.3f}  {ceiling(n):.3f}    {s:.3f}      {u:.3f}")

plt.plot(range(K + 1), [ceiling(n) for n in range(K + 1)], "k--", label="best possible")
plt.plot(range(K + 1), alls, "o-", label="your model")
plt.xlabel("examples in the prompt")
plt.ylabel("accuracy")
plt.legend()
plt.savefig("in_context.png")
print("saved in_context.png")
```

```text
frozen test set fingerprint: 47d6a3db7a1a   prompts per n: 500
  step     0  loss 2.550
  step  1000  loss 1.209
  step  2000  loss 0.812
  step  3000  loss 0.728
  step  4000  loss 0.688
  step  5000  loss 0.658
  step  6000  loss 0.656
  step  7000  loss 0.624
  step  7999  loss 0.614
trained in 99 s
 n  all   ceiling  key-shown  key-unseen
 0  0.176  0.167    nan      0.176
 1  0.312  0.333    1.000      0.181
 2  0.480  0.500    1.000      0.240
 3  0.638  0.667    1.000      0.252
 4  0.666  0.833    0.788      0.474
 5  0.828  1.000    0.854      0.699
 6  0.998  1.000    0.998      nan
saved in_context.png
```

It also writes `in_context.png`: the dashed line is the ceiling, the dots are your model. The "trained in" seconds are from our machine; yours will differ. The fingerprint must match: `47d6a3db7a1a`. If it differs, your test set differs and your numbers are about a different test.

`nan` in two places is correct: at `n = 0` no key is ever shown, and at `n = 6` every key is, so there was nothing to average.

Read the table in four moves.

1. **`n = 0`: `0.176` against `0.167`.** The code is new and nothing is on the page, so there is nothing to know. A prompt with no examples is a coin toss here, however good the model.
2. **`n = 1, 2, 3`: within `0.03` of the ceiling, and `1.000` when the key was shown.** Every remaining error is on a key that was never shown. There the model scores `0.181`, `0.240` and `0.252` against guess-the-unused-digit ceilings of `0.200`, `0.250` and `0.333`: at or below a pure guess, so it has only partly learned to rule out the digits already on the page.
3. **`n = 4, 5`: below the ceiling.** The `key-shown` column says why: it is only `0.788` and `0.854`. On this run the model copies unreliably when more pairs crowd the page. **We did not investigate why.** Do not invent a story.
4. **`n = 6`: `0.998`.**

> **🎲 One seed is one roll.** Everything above is seed 0. We also trained the same recipe on five seeds. At `n = 0` to `3` they agree (`0.146` to `0.182` at zero, `0.630` to `0.676` at three). At six examples the five seeds scored `0.998, 0.998, 0.998, 0.686, 0.956`: one of them had simply not finished learning to copy. The top of the curve is where seeds disagree. The workbook has you run more seeds.

![A line chart of accuracy against 0 to 6 worked examples: a dashed ceiling climbing from 0.167 to 1.000 and a solid model line that follows it but falls short at 4 and 5 examples](../figures/fig-w24-1-in-context-vs-ceiling.svg)
*Figure 24.1 — Accuracy can only follow the ceiling (n + 1) ÷ 6; the model tracks it up to n = 3 and falls short at n = 4 and 5.*

### 4. The start of the prompt as a name: `cachekey.py`

The examples are the **start** (the **prefix**) of every prompt. If two prompts begin with the same text, a service could file the work it did on that start under a fingerprint of the start, a **cache key**, and not repeat it. **Say it out loud before you press enter: this is a stand-in, not a model.** `FakeClient` does not read the prompt; it only counts tokens, by counting the leading words two prompts share.

**`cachekey.py`**

```python
# cachekey.py - Week 24: the examples are a PREFIX. A fingerprint of the prefix is the name a service could file its work under.
# STAND-IN, NOT A MODEL: FakeClient only counts tokens; it does not read the prompt.
import hashlib
from l4lib.fakellm import FakeClient


def cache_key(prefix):
    return hashlib.sha256(prefix.encode("utf-8")).hexdigest()[:12]


examples = "a3 b1 c0 d2 e5 f4 "
print("prompt 1 prefix key:", cache_key(examples))
print("prompt 2 prefix key:", cache_key(examples), " <- same examples, same key")
print("one example edited :", cache_key("a3 b1 c0 d2 e5 f5 "))

client = FakeClient(seed=0)
for query in ("query: c", "query: f"):
    r = client.messages.create(model="fake-small", max_tokens=20, system="",
                               messages=[{"role": "user", "content": examples + query}])
    u = r.usage
    print(f"{query}: fresh input tokens {u.input_tokens}, read from cache {u.cache_read_input_tokens}")
print(client)
```

```text
prompt 1 prefix key: 65e96215c33b
prompt 2 prefix key: 65e96215c33b  <- same examples, same key
one example edited : 129dbb6d18a0
query: c: fresh input tokens 11, read from cache 0
query: f: fresh input tokens 1, read from cache 10
<FakeClient [stand-in, not a model] seed=0 calls=2>
```

Same examples, same key; change one example, a different key. The second query reports `10` read from cache and `1` fresh. It counted the shared leading words, including the word `query:`. **This shows a name for a prefix, not how any real service bills.**

### 5. Addition, two ways: `addlib.py` and `scratchpad_run.py`

**Predict first.** Two models, same size, same 3,000 steps. The *direct* model gets `00042+00917=` and must write the six-digit answer at once. The *working* model first writes, column by column from the right, the two digits it is looking at, the digit it writes and the carry; then the answer. Guess the exact-match score of each, out of 1, and write it down.

Here is one sum written both ways (your `scratchpad_run.py` prints it):

```text
direct : 04211+00009=004220.
pad    : 04211+00009=19011020202040400000#004220.
```

Read the working as five columns of four characters, right to left: `1901` (the digits `1` and `9`, write `0`, carry `1`), `1020` (`1` and `0`, plus the carry `1`: write `2`, carry `0`), `2020`, `4040`, `0000`. Then `#`, then the answer, which is the digits written, read right to left after the last carry: `004220`.

What is new in `addlib.py`, nothing more than habits from earlier weeks:

- `f"{a:05d}"` means "five digits, padded with zeros" (Week 23 used `:5.1f`).
- `HELD_OUT = {p: True for p in TEST}` is a dictionary used as a "have I seen this?" list; `(a, b) in HELD_OUT` asks it. Training **skips** any sum that is in the test set, so the test sums are ones the model has never been trained on.
- The question is given, not scored: the targets start after the `=`.
- `mean` inside `evaluate` and `solve`'s loop use `torch.cat(..., dim=1)` and `argmax(dim=-1, keepdim=True)`; `keepdim=True` keeps the answer as a column so it can be glued on.

**`addlib.py`**

```python
# addlib.py - Week 24: five-digit addition written two ways, and a trainer for each. It prints nothing; other files import it.
import math
import random
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT

torch.set_num_threads(1)

ND = 5                                               # digits per number
CHARS = "0123456789+=#."
stoi = {c: i for i, c in enumerate(CHARS)}
itos = {i: c for c, i in stoi.items()}


def question(a, b):
    return f"{a:05d}+{b:05d}="                                  # 00042+00917=  (:05d = five digits, padded with zeros)


def working(a, b, mode="pad"):
    """The scratchpad, one column at a time, right to left. mode "pad": copy the two digits, then write (digit, carry): 7521.
    mode "pad_short" (the mistake in the clinic): skip the copy and write only (digit, carry): 21."""
    da, db = f"{a:05d}", f"{b:05d}"
    carry, out = 0, ""
    for i in range(ND - 1, -1, -1):
        total = int(da[i]) + int(db[i]) + carry
        out += (da[i] + db[i] if mode == "pad" else "") + str(total % 10) + str(total // 10)
        carry = total // 10
    return out


def answer(a, b):
    return f"{a + b:06d}"                                           # six characters: 000959


def full_text(a, b, mode):
    if mode != "direct":
        return question(a, b) + working(a, b, mode) + "#" + answer(a, b) + "."
    return question(a, b) + answer(a, b) + "."


def make_test(count=500):
    rng = random.Random(2024)
    pairs = {}                                       # a dict, used as a set: have we got this pair already?
    while len(pairs) < count:
        pairs[(rng.randrange(10 ** ND), rng.randrange(10 ** ND))] = True
    return list(pairs)


TEST = make_test()
HELD_OUT = {p: True for p in TEST}


def train_adder(mode, seed, steps, batch=64, log_every=0, lr=2e-3):
    torch.manual_seed(seed)
    rng = random.Random(seed)
    length = len(full_text(0, 0, mode))
    start = len(question(0, 0))
    model = TinyGPT(len(CHARS), 64, 4, 2, length)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1, (s + 1) / 200) * 0.5 * (1 + math.cos(math.pi * s / steps)))
    for step in range(steps):
        rows = []
        while len(rows) < batch:
            a, b = rng.randrange(10 ** ND), rng.randrange(10 ** ND)
            if (a, b) in HELD_OUT:
                continue                              # never train on a test sum
            rows.append([stoi[c] for c in full_text(a, b, mode)])
        x = torch.tensor(rows)
        logits, _ = model(x)
        guess = logits[:, start - 1:-1]              # places that come BEFORE the working/answer predict it
        truth = x[:, start:]                         # the question itself is given, so it is not scored
        loss = F.cross_entropy(guess.reshape(-1, len(CHARS)), truth.reshape(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if log_every and (step % log_every == 0 or step == steps - 1):
            print(f"  [{mode}] step {step:5d}  loss {loss.item():.3f}")
    return model


@torch.no_grad()
def solve(model, a, b, mode):
    """Greedy: at every step write the single most likely next character."""
    length = len(full_text(a, b, mode))
    idx = torch.tensor([[stoi[c] for c in question(a, b)]])
    while idx.shape[1] < length:
        logits, _ = model(idx)
        idx = torch.cat([idx, logits[:, -1].argmax(dim=-1, keepdim=True)], dim=1)
    return "".join(itos[i] for i in idx[0].tolist())


def read_answer(text, mode):
    tail = text.split("#")[-1] if mode != "direct" else text[len(question(0, 0)):]
    return tail.rstrip(".")


def score(model, mode):
    """(exact-match accuracy, accuracy of each of the six answer characters)."""
    exact, per_place = 0, [0] * (ND + 1)
    for a, b in TEST:
        got = read_answer(solve(model, a, b, mode), mode)
        want = answer(a, b)
        exact += got == want
        for i in range(ND + 1):
            per_place[i] += i < len(got) and got[i] == want[i]
    return exact / len(TEST), [p / len(TEST) for p in per_place]
```

**`scratchpad_run.py`** (about 90 seconds in total on our machine)

```python
# scratchpad_run.py - Week 24: the same sums, the same model size, the same number of steps: answer straight away, or show the working first.
import time
from addlib import TEST, question, working, answer, full_text, train_adder, solve, score

print("one sum, both ways:")
print("  direct :", full_text(4211, 9, "direct"))
print("  pad    :", full_text(4211, 9, "pad"))
print("held-out sums:", len(TEST))

for mode in ("direct", "pad"):
    t0 = time.time()
    model = train_adder(mode, seed=0, steps=3000, log_every=1000)
    secs = time.time() - t0
    exact, per_place = score(model, mode)
    print(f"{mode:6s}: exact {exact:.3f}   per answer character {[round(p, 2) for p in per_place]}   ({secs:.0f} s)")
    a, b = TEST[0]
    print(f"        {a} + {b} = {a + b};  the model wrote: {solve(model, a, b, mode)}")
```

```text
one sum, both ways:
  direct : 04211+00009=004220.
  pad    : 04211+00009=19011020202040400000#004220.
held-out sums: 500
  [direct] step     0  loss 2.666
  [direct] step  1000  loss 1.353
  [direct] step  2000  loss 1.119
  [direct] step  2999  loss 1.060
direct: exact 0.000   per answer character [1.0, 0.98, 0.82, 0.11, 0.11, 0.13]   (31 s)
        61615 + 23816 = 85431;  the model wrote: 61615+23816=085791.
  [pad] step     0  loss 2.669
  [pad] step  1000  loss 0.000
  [pad] step  2000  loss 0.000
  [pad] step  2999  loss 0.000
pad   : exact 1.000   per answer character [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]   (60 s)
        61615 + 23816 = 85431;  the model wrote: 61615+23816=56111130684113506280#085431.
```

Read the `direct` row. The first two answer characters are near-perfect, the third is mostly right (`0.82`), and the last three are at `0.11`, `0.11`, `0.13`. A pure guess at one digit is `0.10`, so **the last three characters are at chance**. The `pad` row is `1.000` everywhere. Notice the model's working for the held-out sum: it wrote `56111130684113506280#085431`, a working of its own, and then the right answer.

Now the warning, before you believe anything. That was seed 0. We also ran five seeds of each:

| mode | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 |
|---|:--:|:--:|:--:|:--:|:--:|
| direct | 0.000 | 0.038 | 0.052 | 0.082 | 0.000 |
| with working (copy the two digits, then write digit and carry) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| compact working (write only digit and carry) | 1.000 | **0.090** | 0.974 | 1.000 | **0.000** |

Two small prints, both measured:

- **Direct is "not learned yet", not "impossible".** Trained for four times the steps (12,000), the direct model scored exact match `0.994`. On this task, with this model, the working bought **speed and reliability**: direct also got there with four times the steps (one seed, one task). We did not test whether that holds for harder tasks.
- **The design of the working matters.** A leaner working that skips the "copy the two digits" step worked on only three seeds of five. On the failing seeds it writes a wrong working and then copies it faithfully into the answer. A faithful answer to a wrong working is still wrong.

### 6. The grammar: `grammar.py` (read it, do not type it)

Which characters may come next in `{"name":"mia","age":14,"adult":false}.`? `grammar.py` answers that one question with a lookup, not a model. A **pattern** is a list of pieces, each piece `(allowed characters, fewest, most)`. `lit('{"name":"')` is one allowed character per place; `(LETTERS, 1, 8)` is one to eight letters; `(NONZERO, 1, 1), (DIGITS, 1, 1)` is a two-digit number that does **not** start with `0`, because JSON forbids `02`. `allowed_after(text)` returns every character that may legally come next.

**`grammar.py`** (given)

```python
# grammar.py - Week 24 (GIVEN: read it, do not type it). Which characters may come next in
#   {"name":"mia","age":14,"adult":false}.
# A pattern is a list of pieces (allowed characters, fewest, most). The function walks every pattern at once.
LETTERS = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
NONZERO = "123456789"                        # JSON does not allow a number like 02, so the first digit is never 0


def lit(s):
    return [(c, 1, 1) for c in s]            # a piece that allows exactly one character, once


HEAD = lit('{"name":"') + [(LETTERS, 1, 8)] + lit('","age":') + [(NONZERO, 1, 1), (DIGITS, 1, 1)] + lit(',"adult":')
PATTERNS = [HEAD + lit("true}."), HEAD + lit("false}.")]


def spots_after(pattern, text):
    """Every (piece, characters used in it) the text could have reached. Empty list = the text already broke the pattern."""
    spots = [(0, 0)]
    for ch in text:
        new = []
        for piece, used in spots:
            while piece < len(pattern):
                chars, lo, hi = pattern[piece]
                if ch in chars and used < hi and (piece, used + 1) not in new:
                    new.append((piece, used + 1))          # the character belongs to this piece
                if used >= lo:
                    piece, used = piece + 1, 0             # this piece is full enough: try the next one
                else:
                    break
        spots = new
    return spots


def allowed_after(text):
    """A string holding every character that may legally come next."""
    out = ""
    for pattern in PATTERNS:
        for piece, used in spots_after(pattern, text):
            while piece < len(pattern):
                chars, lo, hi = pattern[piece]
                if used < hi:
                    out += chars
                if used >= lo:
                    piece, used = piece + 1, 0
                else:
                    break
    return out
```

Check it with a few prefixes. This is a sanity check, not a lesson file.

**`check_grammar.py`**

```python
# check_grammar.py - Week 24: what the grammar allows after a few prefixes. Not a lesson file; your sanity check.
from grammar import allowed_after

for text in ['', '{"name":"mi', '{"name":"mia"', '{"name":"mia","age":0', '{"name":"mia","age":1', '{"name":"mia","age":14,"adult":', '{"name":"mia","age":14,"adult":tr', '{"name":"mia","age":14,"adult":true}.']:
    print(repr(text[-14:]).ljust(18), repr("".join(sorted(set(allowed_after(text))))))
```

```text
''                 '{'
'{"name":"mi'      '"abcdefghijklmnopqrstuvwxyz'
'{"name":"mia"'    ','
':"mia","age":0'   ''
':"mia","age":1'   '0123456789'
'e":14,"adult":'   'ft'
':14,"adult":tr'   'u'
'"adult":true}.'   ''
```

The second line is the 26 letters plus the closing quote (the quote sorts first). After `"age":0` nothing is allowed: the first digit of an age is never `0`. After the final `.` nothing is allowed either, which is how the decoder knows the reply is complete.

### 7. The mask: `jsonlib.py` and `jsonmask_run.py`

The third model turns `mia 14>` into `{"name":"mia","age":14,"adult":false}.`. It writes one character at a time by rolling dice weighted by its scores. What could go wrong? A missing quote, a letter where a digit belongs, `02`.

`jsonlib.py` is Week 17's `generate` with a stop and one new idea. In `decode`, when `mask=True`, four lines do the work:

```text
ok = allowed_after(reply)                                   # which characters may come next?
allow = torch.tensor([c in ok for c in CHARS])              # True / False for every character the model knows
last = torch.where(allow, last, torch.tensor(float("-inf")))   # forbidden characters get -inf
# ... then the usual softmax and multinomial
```

**The mask is applied before the dice are rolled, so the model can never choose a forbidden character, and it has no idea it was stopped.** The model's knobs do not move. Also new: `@torch.no_grad()` above a function (you met it in Week 17's `generate`; copy the line), `ignore_index=-100` with `masked_fill` (Week 12), and `json.loads` with `json.JSONDecodeError` (Week 23): a reply "parses" if `json.loads` does not raise. The model trains on 200 of the 231 typed names from Weeks 8-13; **31 names are held back** and never seen in training.

**`jsonlib.py`**

```python
# jsonlib.py - Week 24: teach a TinyGPT to turn "mia 14>" into {"name":"mia","age":14,"adult":false}. and decode it with or without a mask.
import json
import math
import random
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT
from l4lib.names import NAMES
from grammar import allowed_after

torch.set_num_threads(1)

CHARS = "".join(sorted(set("abcdefghijklmnopqrstuvwxyz0123456789 >{}\":,.")))
stoi = {c: i for i, c in enumerate(CHARS)}
TRAIN_NAMES, NEW_NAMES = NAMES[:200], NAMES[200:]          # 31 names the model never sees in training
T = 56


def prompt_of(name, age):
    return f"{name} {age}>"


def target_of(name, age):
    adult = "true" if age >= 18 else "false"
    return '{"name":"' + name + '","age":' + str(age) + ',"adult":' + adult + "}."


def train_json(seed, steps, batch=64, log_every=0):
    torch.manual_seed(seed)
    rng = random.Random(seed)
    model = TinyGPT(len(CHARS), 64, 4, 2, T)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1, (s + 1) / 100) * 0.5 * (1 + math.cos(math.pi * s / steps)))
    for step in range(steps):
        x = torch.zeros(batch, T, dtype=torch.long)
        scored = torch.zeros(batch, T, dtype=torch.bool)
        for b in range(batch):
            name, age = rng.choice(TRAIN_NAMES), rng.randint(10, 40)
            p = prompt_of(name, age)
            text = p + target_of(name, age)
            x[b, :len(text)] = torch.tensor([stoi[c] for c in text])
            scored[b, len(p):len(text)] = True                 # score only the JSON, not the prompt and not the padding
        logits, _ = model(x)
        truth = x[:, 1:].masked_fill(scored[:, 1:] == False, -100)
        loss = F.cross_entropy(logits[:, :-1].reshape(-1, len(CHARS)), truth.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if log_every and (step % log_every == 0 or step == steps - 1):
            print(f"  step {step:5d}  loss {loss.item():.3f}")
    return model


@torch.no_grad()
def decode(model, prompt, mask, gen):
    """Sample one reply, one character at a time. With mask=True, characters the grammar forbids get -inf before the softmax."""
    idx = torch.tensor([[stoi[c] for c in prompt]])
    reply = ""
    while len(prompt) + len(reply) < T:
        logits, _ = model(idx)
        last = logits[0, -1]
        if mask:
            ok = allowed_after(reply)
            if ok == "":
                break                                            # the grammar says the reply is complete
            allow = torch.tensor([c in ok for c in CHARS])
            last = torch.where(allow, last, torch.tensor(float("-inf")))
        nxt = torch.multinomial(F.softmax(last, dim=-1), 1, generator=gen).item()
        reply += CHARS[nxt]
        idx = torch.cat([idx, torch.tensor([[nxt]])], dim=1)
        if CHARS[nxt] == ".":
            break
    return reply


def judge(reply, name, age):
    """Returns (parses as JSON?, has the three keys?, the wrong fields)."""
    try:
        record = json.loads(reply.rstrip("."))
    except json.JSONDecodeError:
        return False, False, []
    if type(record) is not dict or sorted(record) != ["adult", "age", "name"]:
        return True, False, []
    wrong = []
    if record["name"] != name:
        wrong.append("name")
    if record["age"] != age:
        wrong.append("age")
    if record["adult"] != (age >= 18):
        wrong.append("adult")
    return True, True, wrong
```

`jsonmask_run.py` trains for 800 steps (about 25 seconds), then asks 100 questions four ways: names it has seen or not, decoding free or masked. The same 100 questions and the same dice are used for every row.

**`jsonmask_run.py`**

```python
# jsonmask_run.py - Week 24: free sampling vs a grammar mask. The mask can fix the SHAPE. Can it fix the CONTENT?
import random
import time
import torch
from jsonlib import train_json, decode, judge, prompt_of, TRAIN_NAMES, NEW_NAMES

t0 = time.time()
model = train_json(seed=0, steps=800, log_every=200)
print(f"trained in {time.time() - t0:.0f} s")

print("names     decoding  parses  right-shape  all-fields-right")
examples = []
for label, names in (("seen", TRAIN_NAMES), ("new ", NEW_NAMES)):
    for mask in (False, True):
        gen = torch.Generator().manual_seed(5)          # the same dice for every row
        rng = random.Random(77)                         # the same 100 questions for every row
        parses = shaped = right = 0
        for _ in range(100):
            name, age = rng.choice(names), rng.randint(10, 40)
            reply = decode(model, prompt_of(name, age), mask, gen)
            ok_parse, ok_shape, wrong = judge(reply, name, age)
            parses += ok_parse
            shaped += ok_shape
            right += ok_shape and wrong == []
            if mask and ok_shape and wrong and len(examples) < 4 and label == "new ":
                examples.append((prompt_of(name, age), reply, wrong))
        print(f"{label}      {'mask' if mask else 'free':4s}      {parses:3d}     {shaped:3d}          {right:3d}")

print("valid JSON, right shape, still wrong (mask on, names the model never saw):")
for p, reply, wrong in examples:
    print(f"  {p:12s} -> {reply:42s} wrong: {wrong}")
```

```text
  step     0  loss 3.771
  step   200  loss 0.121
  step   400  loss 0.007
  step   600  loss 0.005
  step   799  loss 0.005
trained in 24 s
names     decoding  parses  right-shape  all-fields-right
seen      free       90      87           79
seen      mask      100     100           95
new       free       85      85           25
new       mask      100     100           26
valid JSON, right shape, still wrong (mask on, names the model never saw):
  bex 16>      -> {"name":"umele","age":40,"adult":true}.    wrong: ['name', 'age', 'adult']
  zora 16>     -> {"name":"ukor","age":16,"adult":false}.    wrong: ['name']
  zaid 19>     -> {"name":"usai","age":16,"adult":true}.     wrong: ['name', 'age']
  gero 40>     -> {"name":"gera","age":40,"adult":true}.     wrong: ['name']
```

Read it as a 2 x 2.

- **Parses.** Free sampling gives `90` and `85` of 100. The mask gives `100` and `100`. The mask wins, as it was built to.
- **Fully right, names seen in training.** `79` free, `95` masked. The mask lifted it by 16; we did not look at which replies account for the other 6.
- **Fully right, names never seen.** `25` free, `26` masked. **The mask does almost nothing for content.**
- **The four wrong replies** are all well-formed JSON with the right shape: `zora` became `ukor`. One possible reason, which this run did not test, is that the model has memorised 200 names and does not copy an unfamiliar one letter by letter. That would be a generalisation failure (Week 5), not a formatting failure, and the mask cannot see it.

We also ran the mask over three training seeds. Masked always parsed `100`. On new names "fully right" was `26`, `44`, `45` masked against `25`, `36`, `46` free: the same picture.

![Two panels of paired bars out of 100 prompts: for seen names parses 90 free and 100 masked, all fields right 79 and 95; for new names parses 85 and 100, all fields right 25 and 26](../figures/fig-w24-2-mask-shape-not-content.svg)
*Figure 24.2 — The grammar mask fixes the shape (parses go to 100) but not the content on names the model never saw (25 to 26).*

---

## 🎲 Your Turn

This section is for playing the card game by hand, so you have a feel for the ceiling before you compare it with the model.

### The Secret Code Game

Play this **before** any code, with a partner, as the Keeper and the Player. You need 12 index cards: letters `a` to `f` and digits `0` to `5`.

1. The Keeper shuffles the six digit cards face down and lays them under the six letter cards. Nobody has seen the code; it is new every round.
2. The Keeper flips `n` digit cards (choose which letters at random; do not help). The Player sees the shown pairs.
3. The Keeper draws one letter at random. The Player says a digit. The Keeper flips the card. Write right or wrong on the sheet.
4. Play **sixteen rounds**: four each at `n` = 0, 1, 3, 6.

Before the rounds, write beside each block what you expect out of 4 (`4 x (n + 1)/6`): `0.67`, `1.33`, `2.67`, `4`. After sixteen rounds you got, say, 6 and the formula says about 8.7. Were you bad, or unlucky? **Sixteen rounds cannot tell.** That is the model's test set in miniature: the model gets 500 prompts at each `n`, and even a perfect player's score wobbles by about two to four points. What do you need to tell the difference?

Then turn to your prediction card and fill in a row for each file you ran:

| n | best possible `(n+1)/6` | your model | gap |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 3 | | | |
| 6 | | | |

---

## 🔬 Break It On Purpose

This section is for meeting one error on purpose so you can read it when it happens by accident.

**DELIBERATE.** The mask needs a `True`/`False` condition. What happens if you build it from `1` and `0`? Write down what you expect before you run it.

**`bad_where.py`**

```python
# DELIBERATE: the condition is a list of 1s and 0s, not a tensor of True/False.
import torch

scores = torch.tensor([2.0, 1.0, 0.5, 3.0])
allowed = torch.tensor([1, 1, 0, 0])
print(torch.where(allowed, scores, torch.tensor(float("-inf"))))
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad_where.py", line 6, in <module>
    print(torch.where(allowed, scores, torch.tensor(float("-inf"))))
RuntimeError: where expected condition to be a boolean tensor, but got a tensor with dtype Long
```

The error names the kind of thing `where` wanted: a **boolean** tensor. In `decode`, `[c in ok for c in CHARS]` already builds `True`/`False`, which is why the real code works. Fix the file in one short step and run it again (hint: a comparison with `== 1` turns numbers into `True`/`False`). Write in your Bug Log what the fixed line printed.

---

## 🧭 What was shown, and what was not

This section lists what this week's runs measured and what they did not, so you can state the limits of your own results.

**Shown:**
- A ceiling of `(n + 1) / 6`, computed by hand from the rules, and a small transformer that follows it from `0.176` (no examples) to `0.638` (three examples, ceiling `0.667`), with `1.000` whenever the asked key was shown at one to three examples.
- The copying is **not reliable**: `0.788` at four examples on seed 0, and `0.686` to `0.998` at six examples across five seeds.
- Direct five-digit addition at 3,000 steps: exact match `0.000` (and `0.000` to `0.082` across five seeds); with working, `1.000` on all five; a leaner working, `1.000, 0.090, 0.974, 1.000, 0.000`; direct at 12,000 steps, `0.994`.
- A mask that made `100` of `100` replies parse (against `85` to `90` free) and left `26` of `100` fully right on names the model had never seen.

**Not shown:**
- That examples help **large language models**. Our model was trained on thousands of random codes, exactly the family it was tested on. A model trained on text and only then shown a code is a harder experiment that was not run.
- That the model **understands addition**. It learned a column-by-column procedure for five-digit numbers and was not tested on anything else.
- That a scratchpad is **how real systems reason**. Ours is a format the model was shown in training.
- That a direct model **cannot** add. It had not learned in 3,000 steps.
- That the dip at `n = 4, 5` has an explanation. We have none.
- That the cache demo shows **how a real service bills**. It shows a stand-in counting shared leading words.
- That a bigger or more complicated grammar would be safer. The mask is exactly as safe as the grammar is correct, and a grammar you wrote is only as good as what you remembered to write (JSON forbids `02`; a grammar that forgets it lets `02` through).
- That `100` of `100` valid JSON means the model works.

---

## 🔑 Wrap Up

This section is for checking yourself against the week's questions before you write the three sentences.

1. Turn to your prediction card. What did you guess for the best possible score at 0, 1, 3 and 6 shown pairs? What is the formula?
2. Why can a model never beat `(n + 1) / 6`? What are the two things a score above it could mean?
3. Six numbers: `0.167`, `0.638`, `0.000`, `1.000`, `100` and `26`. What was each?
4. Direct addition scored `0.000`. Why is "the model cannot add" the wrong conclusion?
5. The mask made every reply valid. Is the model better? Where exactly are the `74` wrong replies hiding?
6. Which of today's results would change if you used a different seed? Which would not?
7. What did we **not** do today?

Then write these three sentences in your Bug Log in your own handwriting:

> **"A key that was never shown is a guess, so the best possible score is a line nobody can beat."**
> **"One seed is one roll of the dice; the compact scratchpad has a seed where it scores 0.000."**
> **"A mask fixes the shape of a reply and never its sense."**

**A look ahead.** The prompts we have built so far are just text we write. Next week we turn text into geometry: numbers where similar things sit near each other. That is what will let a search decide what goes into a prompt.

---

## 📤 Homework

This section says what to do at home and points to the workbook.

Complete workbook pages 24.1 to 24.6. Write your **predictions before you run anything**: a guess written after the run is not a guess. Every number you write must have come from your own calculator or your own run.

**Optional (fast students).** The dip at `n = 4, 5` is unexplained. Week 19's attention pictures are the obvious tool. Can you find out whether the model is looking at the right place when it fails to copy a key that was shown? Write down what you expect first, and say in your log what the picture does and does not show.

---

## 🐞 A mistake to know by name

This section names one mistake so you can recognise it.

A fingerprint is not a secret code. You cannot run it backwards and you do not need to: it is a short name for a text. Two different texts can in principle share one, but with 12 characters of `sha256` you will never meet it in this course. The mistake worth knowing is the one in **Break It On Purpose**: giving `torch.where` numbers where it wants `True`/`False`. It is loud, which is the kind you want.

---

## 📖 Words from this week

This section is a reference for the words and syntax introduced this week.

| Word | Meaning |
|---|---|
| **in-context learning** | a model using the examples in its prompt to answer, with its knobs frozen |
| **zero-shot / few-shot** | a prompt with no worked examples / with a few; a "shot" is one worked example |
| **best possible score (ceiling)** | the highest score anyone could get on a task, computed from its rules; here `(n + 1) / 6` |
| **scratchpad** | working written out before the answer |
| **schema** | the shape a reply must have |
| **logit** | a model's score for a next character before the softmax |
| **logit mask / constrained decoding** | setting the score of forbidden characters to minus infinity so only legal ones can be chosen |
| **prefix** | the start of a prompt |
| **cache key** | a fingerprint of a prefix, used to name work already done on it |
| **stand-in** | a scripted imitation of a model, labelled "stand-in, not a model" |
| **`random.Random(seed)`** | your own private dice; the same seed gives the same rolls and does not disturb anyone else's dice |
| **`hashlib.sha256`** | a fingerprint of text (64 hex characters; we keep 12) |
| **`torch.where(cond, a, b)`** | choose from `a` where `cond` is `True`, from `b` where it is `False` |

---

[⬅ Week 23](week-23.md) · [Course Home](../README.md) · [Week 25 ➡](week-25.md) · [Workbook](../workbook/week-24.md)
