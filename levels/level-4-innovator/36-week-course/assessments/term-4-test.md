# 📝 Term 4 Test — Weeks 28–36: Fences, Judges, Patches and Honest Numbers

[⬅ Course home](../README.md) · [⬅ Term 3 test](term-3-test.md) · [Assessments home](README.md) · Term 4 of 4 · covers Weeks 28–36

---

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │   AI ACADEMY · LEVEL 4 INNOVATOR                                     │
   │   TERM 4 TEST — Fences, Judges, Patches and Honest Numbers           │
   │   Covers Weeks 28–36. Nothing earlier is new on this test.           │
   │                                                                      │
   │   PART 1 · THE PAPER           75 minutes      75 marks              │
   │   PART 2 · THE DEMO            15 minutes      15 marks              │
   │                                                                      │
   │   Section A   20 multiple choice          1 mark each     20 marks   │
   │   Section B    8 "what does this print"   2 marks each    16 marks   │
   │   Section C    4 "find the bug"           3 marks each    12 marks   │
   │   Section D    3 "do the arithmetic"      5 marks each    15 marks   │
   │   Section E    1 question on 3 real tables (4 + 4 + 4)    12 marks   │
   │                                                                      │
   │   PART 1:  ⛔ NO COMPUTER.   ✅ A CALCULATOR WITH A SQUARE-ROOT KEY. │
   │   PART 2:  ✅ A COMPUTER AND YOUR OWN WEEK 28–36 FILES. NO NETWORK.  │
   │                                                                      │
   │   SUGGESTED TIME   A 15 · B 15 · C 10 · D 20 · E 15 minutes          │
   │                                                                      │
   │   INSTRUCTIONS FOR THE PAPER                                         │
   │   · Pencil. Answer every question. "Did not get it" is allowed and   │
   │     costs nothing extra; a blank tells nobody anything.              │
   │   · Section A: circle ONE letter. If you guessed, write "not sure".  │
   │   · Section B: write EVERY line the program prints, in order,        │
   │     exactly as Python prints it (quotes, trailing zeros, brackets).  │
   │   · Section C: say (i) what is wrong, (ii) what happens when it      │
   │     runs, (iii) the fixed line.                                      │
   │   · Section D: show every line of working. Carry FOUR decimal        │
   │     places and round only at the end.                                │
   │   · Section E: use the numbers in the tables. Quote them.            │
   │                                                                      │
   │   WHAT IS ALLOWED ON THE PAPER                                       │
   │   ✅  Pencil, pen, eraser, ruler, a calculator                       │
   │   ✅  Rough paper. Working earns marks                               │
   │   ❌  A computer, a phone, your notes, your .py files                │
   │   ❌  A search engine, a chatbot, another person                     │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘
```

> **🧑‍🏫 Teacher, read this box once before you hand anything out.**
>
> **What this file is.** Week 36 already holds Assessment 4 (the final paper, in that week's teacher guide).
> **This is a second paper of the same shape, with every question and every number different.** Use it as
> the Term 4 re-sit, as practice, or as a second look after the remediation fortnight. It does **not**
> replace Assessment 4, and it does not test the capstone: the capstone is marked from the card, the
> numbers and the demo. **Report the paper and the demo separately.** Nothing is built on Term 4, so this
> one is a look-back.
>
> **You do not need to know Python, probability or machine learning to run or mark this.** The answer key
> at the bottom gives every answer, every line of working, and the *real printed output* of every code
> block. Compare, do not work out.
>
> **What "real" means here.** Every code block in this file, on the paper and in the key, was run from a
> scratch folder on a CPU, one thread (`torch.set_num_threads(1)` where torch is used), Python 3.10.10,
> torch 2.2.1, numpy 1.26.4, scikit-learn 1.7.1, with the seeds shown, and the output pasted in
> unedited (a traceback has its file path shortened). The code came from the course's own files: the
> `l4lib/` kit (`toyagent`, `fakellm`, `rag`), Week 28's calculator and fences, Week 29's cost curve,
> Week 30's kappa, Week 31's `LoRALinear`, Week 32's reliability functions, Week 33's attack harness
> (`run_attack`, `named_files_only`, `line`) and Week 34's `fingerprint`. **The three tables in Section E
> are printed numbers: print them, do not regenerate them on the day.** Tables 1 and 2 come from the
> scripted agent and depend only on the `notes/` folder of Week 26 (15 notes, the planted 16th in Week
> 33's worlds); Table 3 is 40 **invented** results made with `numpy` seed 7.
>
> **Everything scripted on this test is a stand-in, not a model.** The gullible agent in Table 1, the
> scripted plans in Table 2 and in the demo, and the 40 results in Table 3 are **stand-ins**. The
> probabilities in them (the `0.30` dial, the token counts, the dollar prices) are numbers somebody typed.
> Nothing scored on them says anything about how a real model behaves, and the paper says so every time.
> No network, no API and no pretrained weights are used anywhere.
>
> **Run the paper first, then the demo, on different days if you can** (as Week 36 does for its own two
> sittings). Say out loud, before you start: *"Everything on this test is something you have already
> done with your own hands. It is an X-ray, not a grade. If a question looks strange, read it twice,
> write what you do know, and move on."* Then say nothing until the timer goes. Do not explain any answer
> afterwards; the section at the end of this file says what to do with the pattern.

---

# 📄 PART 1 — THE PAPER

**Name: ____________________   Date: ______________   Time allowed: 75 minutes   Total: 75 marks**

---

# 🅰️ Section A — Multiple Choice

*20 questions · 1 mark each · circle ONE letter · the week each question comes from is in brackets*

---

**A1.** [W28] Why is a calculator built from `ast.parse` and a short list of allowed operators safer than one built on `eval`?

- (a) It runs faster, so it cannot be left waiting
- (b) The set of things the text can make happen is exactly the set you wrote in the list; with `eval` the text decides
- (c) `ast` checks that the sums come out right
- (d) `eval` cannot do sums with brackets

---

**A2.** [W28] A model asks for `write_file("run.sh", "hi")`. A human says yes. The sandbox is strict and `write_file` is on the list of tools. What stops the request?

- (a) The turn cap
- (b) The allowlist of tool names
- (c) The sandbox's check on the file ending (`.sh` is not one of `.md`, `.txt`, `.json`)
- (d) The timeout

---

**A3.** [W28] A run ends with `stop=end_turn`, and the only tool result in its trace reads `Error: the human declined this action.` The best reading is:

- (a) The task worked, because the run ended normally
- (b) The confirmation fence did nothing, because the run did not stop with an error
- (c) The run crashed
- (d) The fence worked: the model was handed an error, "read" it, and finished. The stop reason is not the name of the fence; the `Error:` text is

---

**A4.** [W29] Framing search results as data and scanning them for known phrases lowered how often the stand-in obeyed a planted order, but never to zero. The strict sandbox gave `0` landings every time. The difference is that the sandbox:

- (a) never asks the model: it decides from the path alone, whatever the model was persuaded of
- (b) is random, so it sometimes lets things through
- (c) reads the planted note more carefully
- (d) only works on legal filenames

---

**A5.** [W29] The re-sent history of a 10-step task adds up to `1 + 2 + ... + 10 = 55` units, and of a 20-step task to `1 + 2 + ... + 20 = 210` units. Twice the steps costs the history part about:

- (a) 2 times as much
- (b) 3.8 times as much
- (c) 20 times as much
- (d) the same, because each step is the same size

---

**A6.** [W29] A straight line drawn through the costs of 3, 6 and 9 steps predicts the cost of 24 steps far too low. The reason is:

- (a) The straight line was fitted on too few decimal places
- (b) Dollars cannot be fitted with a line
- (c) The kit's price table changes at 24 steps
- (d) Each step re-sends everything so far, so the cost per step grows; the true shape bends upward

---

**A7.** [W29] Why does a trace write one JSON object per line (JSONL)?

- (a) It makes the file smaller than any other format
- (b) It encrypts the trace
- (c) You can add an event at a time, read it back a line at a time and total it; a crash loses at most the last line
- (d) `json.dumps` cannot write more than one line

---

**A8.** [W30] Two ticket replies have the word sets `{the, river, ran, fast}` and `{river, ran, fast, slow}`. Their Jaccard overlap (words in both divided by words in either) is:

- (a) `0.5`
- (b) `0.6`
- (c) `0.75`
- (d) `1.0`

---

**A9.** [W30] Two raters agree on 19 of 20 tickets, and Cohen's kappa is `0.0`. The most likely reason is:

- (a) One of them says "pass" to every ticket and 19 of the 20 really pass, so agreement that good is what luck alone would give
- (b) They disagreed on the one ticket that mattered
- (c) Kappa cannot be computed when agreement is high
- (d) The library has a bug

---

**A10.** [W30] A pairwise judge is asked each question twice, with the two replies swapped. On 30 of 100 pairs it changes its verdict when they swap. This shows:

- (a) The judge is right 70 percent of the time
- (b) The two replies in those 30 pairs are equally good
- (c) The judge has learned to read
- (d) The verdict depends partly on *where* a reply is listed and not only on the reply

---

**A11.** [W31] A frozen `128 x 128` projection gets a LoRA patch of rank `r = 8`. The patch has `r x in + out x r` numbers. That is:

- (a) `1,024`
- (b) `128`
- (c) `2,048`
- (d) `16,384`

---

**A12.** [W31] In `LoRALinear`, `B` starts at zeros and `A` at small random numbers. At step 0 the patched layer gives the same answer as the base layer because:

- (a) `A` is small
- (b) `B` is zero, so the patch `x @ A.T @ B.T` adds exactly nothing
- (c) `requires_grad_(False)` turns the patch off
- (d) `copy.deepcopy` copies the output

---

**A13.** [W31] `base.requires_grad_(False)` on a layer:

- (a) Keeps its numbers in every forward pass but stops them from being trained
- (b) Deletes its numbers
- (c) Makes the layer skip its forward pass
- (d) Is the same as setting its learning rate to one

---

**A14.** [W32] In one bucket the system said about `0.90` and was right `0.60` of the time. The gap is `0.30`, and this bucket is:

- (a) Under-confident
- (b) Well calibrated
- (c) Impossible, because a system cannot be wrong when it says `0.90`
- (d) Over-confident: it said more than it delivered

---

**A15.** [W32] A system answers binary questions and says `0.5` every single time. Whatever the results, its Brier score is:

- (a) `0.0`
- (b) `0.5`
- (c) `0.25`
- (d) The same as its accuracy

---

**A16.** [W33] An attack that lands with chance `0.2` is run `100` times. The count of landings wobbles by about:

- (a) `0.2`
- (b) `4`
- (c) `16`
- (d) `20`

---

**A17.** [W33] A patched agent shows `0` landings in `20` runs. If the attack still worked `1` time in `20` (`0.05`), the chance that 20 runs would show zero landings is about:

- (a) `0.36`, about one time in three
- (b) `0.01`
- (c) `0.95`
- (d) Zero: it would always show at least one

---

**A18.** [W34] A frozen eval set is checked with `check_frozen`, which compares a fingerprint with the one in `FROZEN.txt`. Someone who edited a case could also edit `FROZEN.txt`. What protects the freeze?

- (a) A longer hash
- (b) Sorting the keys in `json.dumps`
- (c) The first 12 characters of the fingerprint written somewhere that cannot be quietly edited, on paper or in an earlier commit
- (d) Nothing can

---

**A19.** [W35] Your eval cases each carry a `route` field saying where a good system should send the question. The reason is:

- (a) `route` makes the answers shorter
- (b) The router is only decoration
- (c) It lets the guard skip the question
- (d) The router is a rule and a rule can be wrong, so the eval can score the routing separately from the answers

---

**A20.** [W36] A system card may quote a number only if it carries an `n` and comes from the logs. Which row of a "measured numbers" table breaks the rule?

- (a) `refund | 3 of 4`
- (b) `billing | 0.50`
- (c) `all | 17 of 25`
- (d) `latency | 12 ms (stand-in)`

---

# 🅱️ Section B — What Does This Print?

*8 questions · 2 marks each · write EVERY line the program prints, exactly. Each snippet is separate and imports what it needs. `toyagent` is the kit's agent file in `l4lib/`. Scripted parts are **stand-ins, not models**.*

---

**B1.** [W28] `toyagent.calculate` is the kit's whitelist calculator. It returns its answer as text, or raises an error. Six lines are printed.

```py
from l4lib import toyagent
for text in ["3 * 4 + 2", "2 ** 3 ** 2", "'ab' * 2", "7 / 2", "max(1, 2)", "5 -"]:
    try:
        print(toyagent.calculate(text))
    except Exception as e:
        print(type(e).__name__)
```

---

**B2.** [W28] A scripted plan (**stand-in, not a model**) asks for three tool calls and would then say `fine`. The loop is allowed `3` turns. Three lines are printed. (`is_error` is `True` for a call that came back as an error.)

```py
from l4lib import toyagent
specs = toyagent.tool_specs()
reg = toyagent.ToolRegistry()
reg.register("calculate", toyagent.calculate, timeout=2.0)
plan = toyagent.ScriptedModel([("", [("calculate", {"expression": "6 * 7"})]),
                               ("", [("delete_all", {})]),
                               ("", [("calculate", {})]),
                               ("fine", [])])
r = toyagent.run_agent("q", reg, specs, plan, max_iterations=3)
print(r["stop"], r["iterations"])
print([(c["tool"], c["is_error"]) for c in r["tool_calls"]])
print(r["label"])
```

---

**B3.** [W29] Four lines are printed. (`json.dumps(..., sort_keys=True)` writes the keys in alphabetical order; `false` is how JSON writes `False`.)

```py
import json
events = [{"event": "model_turn", "iteration": 1, "in_tok": 200, "out_tok": 12},
          {"event": "tool_call", "tool": "calculate", "is_error": False},
          {"event": "model_turn", "iteration": 2, "in_tok": 230, "out_tok": 9}]
line = json.dumps(events[1], sort_keys=True)
print(line)
back = json.loads(line)
print(back["is_error"], type(back["is_error"]).__name__)
print(sum(e.get("in_tok", 0) for e in events))
k = 12
print(k * (k + 1) // 2)
```

---

**B4.** [W30] Four lines are printed. Do the kappa by hand first: the library will agree with you. `sorted` puts a list of words in alphabetical order.

```py
from sklearn.metrics import cohen_kappa_score
H = [1, 1, 1, 1, 0, 0, 0, 0]
J = [1, 1, 1, 0, 0, 0, 0, 1]
print(sum(h == j for h, j in zip(H, J)) / len(H))
print(round(cohen_kappa_score(H, J), 3))
a = {"refund", "money", "back", "please"}
b = {"refund", "money", "returned"}
print(sorted(a & b), len(a | b))
print(round(len(a & b) / len(a | b), 2))
```

---

**B5.** [W31] Four lines are printed. (`nn.Linear(10, 6)` has a weight grid of `6 x 10` and a bias of `6`.)

```py
import torch
from torch import nn
col = torch.tensor([[1.], [0.], [3.]])
row = torch.tensor([[2., -1.]])
g = col @ row
print(g.tolist())
print(g.numel(), col.numel() + row.numel())
lin = nn.Linear(10, 6)
lin.requires_grad_(False)
A = nn.Parameter(torch.zeros(2, 10))
B = nn.Parameter(torch.zeros(6, 2))
print(sum(p.numel() for p in [lin.weight, lin.bias, A, B] if p.requires_grad))
print(sum(p.numel() for p in lin.parameters()))
```

---

**B6.** [W32] Four lines are printed. (`np.digitize(x, [0.6, 0.8])` gives `0` below `0.6`, `1` from `0.6` up to `0.8`, and `2` from `0.8` up. The Brier score is the mean of the squared gaps.)

```py
import numpy as np
from sklearn.metrics import brier_score_loss
conf = np.array([0.95, 0.85, 0.80, 0.65, 0.55, 0.60])
right = np.array([1, 0, 1, 1, 0, 0])
bucket = np.digitize(conf, [0.6, 0.8])
print(bucket.tolist())
print(np.bincount(bucket, minlength=3).tolist())
print(round(brier_score_loss(right, conf), 4))
sure = conf >= 0.8
print(int(sure.sum()), round(float(right[sure].mean()), 3))
```

---

**B7.** [W33] Four lines are printed. (`re.sub(pattern, "[TAG]", text)` replaces every match with `[TAG]`. `NUMBERY` matches any run of ten or more characters made of digits and spaces that starts and ends with a digit. `\b(?:\d{4}[ -]?){3}\d{4}\b` is a sixteen-digit card number.)

```py
import re
import numpy as np
EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
CARD = r"\b(?:\d{4}[ -]?){3}\d{4}\b"
NUMBERY = r"\d[\d ]{8,}\d"

def redact(text, patterns):
    for tag, pattern in patterns:
        text = re.sub(pattern, f"[{tag}]", text)
    return text

text = "Mail a@b.org, card 4111 1111 1111 1111, call 98765 43210."
print(redact(text, [("EMAIL", EMAIL), ("CARD", CARD), ("NUM", NUMBERY)]))
print(redact(text, [("EMAIL", EMAIL), ("NUM", NUMBERY), ("CARD", CARD)]))
print(redact("No secrets here.", [("EMAIL", EMAIL), ("CARD", CARD)]))
print(round(float(np.sqrt(80 * 0.25 * 0.75)), 2))
```

---

**B8.** [W34] Two lines are printed. (`hashlib.sha256(...).hexdigest()` is 64 characters long. The three `==` tests compare whole fingerprints.)

```py
import hashlib, json

def fp(cases):
    return hashlib.sha256(json.dumps(cases, sort_keys=True).encode("utf-8")).hexdigest()

a = [{"q": "cancel it", "gold": "billing"}, {"q": "it crashes", "gold": "technical"}]
b = [{"gold": "billing", "q": "cancel it"}, {"gold": "technical", "q": "it crashes"}]
c = [{"q": "cancel it", "gold": "billing"}, {"q": "it crashes", "gold": "refund"}]
d = [a[1], a[0]]
print(fp(a) == fp(b), fp(a) == fp(c), fp(a) == fp(d))
print(len(fp(a)), len(fp(a)[:12]))
```

---

# 🅲 Section C — Find and Fix the Bug

*4 questions · 3 marks each · for each: **(i)** what is wrong · **(ii)** what happens when it runs (an error, with what its last line means in plain words, or a silent wrong result) · **(iii)** the fixed line. The programs are **deliberately** broken.*

---

**C1.** [W28] The programmer wants `inside` to say `False` for the second name. Two lines are printed.

```py
# DELIBERATE: this program has a bug. Find it.
from pathlib import Path
ROOT = Path("sandbox").resolve()
ROOT.mkdir(exist_ok=True)

def inside(root, filename):
    return str(root / filename).startswith(str(root))

print(inside(ROOT, "plan.md"))
print(inside(ROOT, "../secrets.md"))
```

The program prints:

```text
True
True
```

---

**C2.** [W31] The programmer has built a LoRA patch beside a frozen layer (`x @ A.T @ B.T`) and expects both `A` and `B` to receive a gradient after one backward pass. The program is a stand-in for a real fine-tune: nothing in it is a trained model.

```py
# DELIBERATE: this program has a bug. Find it.
import torch
from torch import nn
torch.manual_seed(0)
base = nn.Linear(4, 3)
base.requires_grad_(False)
A = nn.Parameter(torch.zeros(2, 4))
B = nn.Parameter(torch.zeros(3, 2))
x = torch.randn(5, 4)
out = base(x) + x @ A.T @ B.T
loss = out.pow(2).mean()
loss.backward()
print(float(A.grad.abs().sum()), float(B.grad.abs().sum()))
```

The program prints:

```text
0.0 0.0
```

---

**C3.** [W32] The programmer wants the Brier score of four results. Python also prints a long traceback; only its last line is shown.

```py
# DELIBERATE: this program has a bug. Find it.
import numpy as np
from sklearn.metrics import brier_score_loss
conf = np.array([0.9, 0.8, 0.6, 0.55])
right = np.array([1, 0, 1, 0])
print(round(brier_score_loss(conf, right), 4))
```

The last line of the traceback:

```text
ValueError: The type of the target inferred from y_true is continuous but should be binary according to the shape of y_prob.
```

---

**C4.** [W33] The programmer wants to run a stand-in attack with a true rate of `0.3` fifty times, each run with its own seed, and count the landings. About `15` are expected.

```py
# DELIBERATE: this program has a bug. Find it.
import random
hits = 0
for run in range(50):
    rng = random.Random(0)
    if rng.random() < 0.3:
        hits += 1
print(hits, "of 50")
```

The program prints:

```text
0 of 50
```

---

# 🅳 Section D — Do the Arithmetic

*3 questions · 5 marks each · a calculator is expected · show every line of working · carry FOUR decimal places and round only at the end. The numbers are invented for this paper; the arithmetic is real.*

---

**D1.** [W29] **The bill for a long task.** A scripted agent (stand-in, not a model) sends `n0 = 200` tokens on its first turn and the conversation grows by `g = 30` tokens at every step. It makes `k` tool calls and then a closing answer, so it has `k + 1` model turns. The input tokens over the whole run are

```text
   total in  =  n0 x (k + 1)  +  g x (1 + 2 + ... + k)        and   1 + 2 + ... + k = k (k + 1) / 2
```

Each tool turn writes `10` tokens and the closing answer writes `2`. The price is `1.00` dollar per million tokens in and `5.00` per million out.

**(a)** For `k = 8`: write the flat part `n0 x (k + 1)`, the history part `g x (1 + ... + 8)`, and the total input. *(1)*
**(b)** Write the total output tokens, and the bill for `k = 8` in millionths of a dollar and in dollars. *(1)*
**(c)** Do (a) and (b) again for `k = 16`. *(1)*
**(d)** By what number is the history part multiplied when the steps double? By what number is the whole bill multiplied? *(1)*
**(e)** What share of the input tokens at `k = 16` is re-sent history? Say in one sentence what this means for a long task. *(1)*

---

**D2.** [W30] **Two raters.** Rater A (strict) and rater B (lenient) each mark the same 20 tickets *pass* or *fail*:

```text
                      B pass    B fail
       A pass           9          1
       A fail           5          5
```

**(a)** How many tickets do they agree on, and what is the raw agreement `p_o`? *(1)*
**(b)** How often does A say pass, and how often does B? *(1)*
**(c)** Work out `p_e`, the chance agreement: `(A pass rate) x (B pass rate) + (A fail rate) x (B fail rate)`. *(1)*
**(d)** Work out kappa `= (p_o - p_e) / (1 - p_e)`. In which direction does B differ from A? *(1)*
**(e)** A third "judge" says *pass* to all 20 tickets. The human passes 19 of the 20. Write `p_o`, `p_e` and kappa, and say what the result shows about raw agreement. *(1)*

---

**D3.** [W32] **Said against delivered.** A stand-in system (invented results, not from any model) gave ten answers. Each row is how sure it said it was, and whether it was right (`1`) or wrong (`0`):

```text
   said   0.9  0.9  0.9  0.8  0.8  0.6  0.6  0.5  0.5  0.5
   right   1    1    0    1    0    1    0    1    0    0
```

**(a)** Work out the Brier score: the gap for each result (said minus right), square it, add the ten, divide by ten. *(1)*
**(b)** The accuracy is `0.5`. What Brier score would a system get that said `0.5` every time? Did the system beat it? *(1)*
**(c)** Split the results into "said 0.8 or more" (5 results) and "said less than 0.8" (5 results). For each group write `n`, the mean of what it said, and the share it got right. *(1)*
**(d)** Work out the ECE: the average of `|said - right|` over the groups, each group weighted by its share of the ten. *(1)*
**(e)** The system now answers only when it said `0.8` or more. Write how many it answers, its accuracy on those, and how many right answers it gave up. *(1)*

---

# 🅴 Section E — Reading Real Tables

*1 question with three parts · 12 marks · the numbers are real (the scripts and seeds are in the key) · quote them. Every agent and every "model" in Tables 1 and 2 is a scripted **stand-in, not a model**; Table 3 is **invented**.*

**Table 1 (Week 33 harness, new seeds).** The Week 33 attacks on four versions of the agent, each run **50** times on seeds `2000` to `2049`. **A1** is a planted note that orders a write to a **legal** filename. **A2** is a planted note that orders a write **outside** the box. "Legit save" is the real task (save a summary to `reminders.md`) run in the A1 world: how many of 50 saved the file. The gullible agent is a scripted stand-in whose obey chance is a dial somebody typed.

```text
version of the agent                A1      A2 | legit save
v0: weak sandbox, no guard       14/50   14/50 |      50/50
patch 1: strict sandbox          14/50    0/50 |      50/50
patch 2: + named files only       0/50    0/50 |      50/50
BAD patch: no writes at all       0/50    0/50 |       0/50

A1 patch 2: 14/50 -> 0/50; gap 14 vs noise bound 6.3 -> more than noise
A1 vs itself (seeds 9000-9049): 14/50 -> 16/50; gap -2 vs noise bound 9.2 -> NOT distinguishable from noise
```

(`sqrt(50 x 0.28 x 0.72) = 3.17`.)

**E(a)** *(4 marks, 1 each)*
**(i)** Which patch fixed A2, and what did it do to A1? Quote the numbers, and say in a sentence why.
**(ii)** The "BAD patch" has the best attack numbers in the table. Say why it must not ship, quoting one number.
**(iii)** The last line compares the system with **itself** on other seeds and gets `14` against `16`. What is that line *for*, and what does it say about reading `14/50 -> 0/50`?
**(iv)** Write the one honest sentence for the `0/50` of patch 2, and name one thing the table has **not** tried.

**Table 2 (Week 29 cost curve).** The scripted agent that calls the calculator `k` times and then answers (stand-in, not a model; the tokens are the kit's own count and the dollars are illustrative). The input tokens of the first turns were `223, 255, 288, 320`. The formula `n0 x (k + 1) + grow x k (k + 1) / 2` was fitted from the first three rows (`n0 = 223`, `grow = 32.444` tokens per step) and then used to predict the last two rows, which were then really run. A straight line was also drawn through the first three rows' dollars.

```text
k= 3: total in  1086 | total out  32 | spend $0.001246
k= 6: total in  2242 | total out  62 | spend $0.002552
k= 9: total in  3690 | total out  92 | spend $0.004150
k=15: total in  7464 | total out 152 | spend $0.008224
k=24: total in 15319 | total out 242 | spend $0.016529

k=15: curve predicts in    7461 $0.008221 | straight line $0.007005 | measured in 7464 $0.008224
k=24: curve predicts in   15308 $0.016518 | straight line $0.011361 | measured in 15319 $0.016529
k=24 over k=6: measured 6.48 times the dollars for 4 times the steps
```

**E(b)** *(4 marks, 1 each)*
**(i)** Check the curve's prediction for `k = 15` by hand: `223 x 16 + 32.444 x 15 x 16 / 2`. How close is it to the measured `7464`?
**(ii)** By what percentage is the straight line's `k = 24` prediction below the measured `$0.016529`? (`0.011361 / 0.016529` first.) Say why a straight line is the wrong shape.
**(iii)** Four times the steps (`6` to `24`) cost `6.48` times the dollars. Explain in a sentence why it is not `4`.
**(iv)** The curve predicted to within a few tokens. Give **two** reasons that does not promise a real agent's bill will be predicted so well.

**Table 3 (Week 32 tools, invented results).** Forty results **invented for this test** (`numpy` seed 7); nothing here comes from a model. Each result has a category, how sure the system said it was, and whether it was right. The stand-in system was built to be a little over-confident in some categories.

```text
40 results; accuracy 0.65 average stated 0.753
0.00-0.59  n= 5 stated 0.560 actual 0.400
0.60-0.69  n=11 stated 0.650 actual 0.545
0.70-0.79  n= 9 stated 0.757 actual 0.667
0.80-0.89  n= 8 stated 0.847 actual 0.625
0.90-1.00  n= 7 stated 0.940 actual 1.000
ECE 0.1240  Brier 0.2036  flat-0.650 Brier 0.2275
t=0.00 answered 40 coverage 1.000 accuracy 0.650 wrong-but-answered 14
t=0.70 answered 24 coverage 0.600 accuracy 0.750 wrong-but-answered 6
t=0.80 answered 15 coverage 0.375 accuracy 0.800 wrong-but-answered 3
t=0.90 answered  7 coverage 0.175 accuracy 1.000 wrong-but-answered 0
category     n before answered after
greeting    10  0.800        6  1.000
refund      10  0.900        4  0.750
technical   10  0.500        3  0.333
billing     10  0.400        2  1.000
```

**E(c)** *(4 marks, 1 each)*
**(i)** Which bucket has the biggest gap between stated and actual, and which bucket is the only one that was **under**-confident? Quote the numbers. What does "ECE 0.1240" **not** mean about how often the system is wrong?
**(ii)** The system's Brier score (`0.2036`) is lower than the flat system's (`0.2275`). Does that prove the confidence numbers are useful? Say what else you would want, in one sentence.
**(iii)** At `t = 0.80`, the accuracy rose from `0.650` to `0.800`. Work out how many right answers were given up (the total right is `0.65 x 40`; the answered ones that were right are `15 - 3`), and say what else was paid.
**(iv)** Which **two** categories fell while the average rose? For each, say how many results its "after" rests on. Then say which "rise" in the category table you would **not** believe, and why.

---

# 💻 PART 2 — THE DEMO

**15 minutes · 15 marks · a computer, your own Week 28–36 files, and the `l4lib` folder. No network, no chatbot.**
*Teacher: sit beside the student. The marks are for what you **watch** and **hear**, so keep the checklist in the marking scheme next to you.*

Open a terminal in the folder that contains `l4lib/` and your `notes/`. Each demo is a new file. **Say your prediction out loud before you run anything.** A prediction you make after seeing the output does not count. Say "stand-in, not a model" out loud each time a scripted part is on the screen.

**Demo 1 — "Four requests, and the bill" · 5 marks · Weeks 28 and 29**
Write `demo1.py`. **(i)** Build a `Sandbox`, a `ToolRegistry` with `calculate` and `write_file` (confirmation required, `auto_approve=True`) and send four scripted `write_file` requests through `toyagent.run_agent`: `run.sh`, `../x.md`, a `big.md` of 25,000 letters, and `plan.md`. For each print the stop reason, whether the call was an error and the first 52 characters of the result. Then print the files in the box and how many attempts were logged. Say which fence stopped each one **before** you run. **(ii)** Write `steps(k)` (the calculator called `k` times, then an answer; `max_tool_errors=99`, `budget_usd=10`), run `k = 6` and `k = 12`, take `n0` and `grow` from the `k = 12` run, and print the predicted and measured total input for both, and the spend. **(iii)** Print how many times the dollars the doubled run cost, and the history share of the `k = 12` input. Say in one sentence why "twice the steps" is not "twice the bill".

**Demo 2 — "Kappa, the patch, the reliability" · 5 marks · Weeks 30, 31 and 32**
Write `demo2.py`. **(i)** From the grid of **D2**, build the two rating lists and print the raw agreement and `cohen_kappa_score`; then print both again for the always-pass judge of **D2(e)**. These must match your paper. **(ii)** Type your `LoRALinear` (freeze the base, `A` small random, `B` zeros) around a `64 x 64` `nn.Linear` with `r = 4` and `torch.manual_seed(0)`. Print whether step 0 equals the base, how many patch numbers there are and their share of the layer, then do one backward pass and print whether a gradient reaches `A`, `B` and the base weight. **Predict the three answers first.** **(iii)** With the ten results of **D3**, print the two-group table with `np.digitize` and `np.bincount`, the ECE, the Brier score and the flat Brier score, and the result of answering only at `0.8` or more. Say out loud which of your paper's numbers it confirms.

**Demo 3 — "Attack, redact, freeze" · 5 marks · Weeks 33 to 36**
Write `demo3.py`. **(i)** With your Week 33 harness, run A1 on seeds `3000` to `3049` with the strict sandbox, with and without `named_files_only`, and on seeds `8000` to `8049` without it. Print the two `line(...)` reports (before against after, and before against itself). Say the honest sentence for the `0`. **(ii)** With your five-pattern `redact_pii` (email, card, Aadhaar, phone, in that order), redact five new strings (an email, a phone, a card, an Aadhaar number, and a name with an address) and print each result and the recall. Print how many of your 15 notes it changes. **(iii)** Build five dictionaries as cases, print the first 12 characters of their `fingerprint`, change **one** gold label in a copy, print the new 12, and show that `check_frozen` style refusal (an `assert`) fires. Say out loud why the 12 characters belong on paper.

*End of Part 2.*

---

# 📊 MARKING SCHEME

**Paper: 75 marks. Demo: 15 marks. Report them separately.** The paper is "can you read code, arithmetic and tables without a machine", the demo is "can you prove it on a machine, in front of someone". A student who is strong on one and weak on the other has told you something that one sum would hide. **Neither is the capstone.**

> **Mark Section A first.** It is fast, and the pattern of wrong answers tells you where to look in the rest.
> Below each answer in the key is a sentence on why the wrong options were tempting.

## Section A — 20 marks

| Q | Ans | Week | | Q | Ans | Week |
|:--:|:--:|:--:|---|:--:|:--:|:--:|
| A1 | **b** | W28 | | A11 | **c** | W31 |
| A2 | **c** | W28 | | A12 | **b** | W31 |
| A3 | **d** | W28 | | A13 | **a** | W31 |
| A4 | **a** | W29 | | A14 | **d** | W32 |
| A5 | **b** | W29 | | A15 | **c** | W32 |
| A6 | **d** | W29 | | A16 | **b** | W33 |
| A7 | **c** | W29 | | A17 | **a** | W33 |
| A8 | **b** | W30 | | A18 | **c** | W34 |
| A9 | **a** | W30 | | A19 | **d** | W35 |
| A10 | **d** | W30 | | A20 | **b** | W36 |

No half marks. Two letters circled scores 0. A guess marked "not sure" that is right still scores 1; count the "not sure" ones separately, because a student who is right and knows they are unsure needs a different conversation from one who is wrong and sure.

## Section B — 16 marks

Two marks each: **1** for the first half of the lines exactly right, **1** for the rest. Quotes, `True`/`False`, trailing zeros and list brackets count. Carry forward: a wrong first line that is used correctly later loses only once.

| Q | Lines (first mark / second mark) | Common slip |
|:--:|---|---|
| B1 | lines 1–3 / lines 4–6 | writing `512` as `2 ** 9` or `64`; `'ab' * 2` as `abab` (the whitelist refuses a string); `5 -` as `ValueError` (it is a `SyntaxError`: the text is not an expression) |
| B2 | line 1 / lines 2–3 | `end_turn` instead of `max_iterations`; a `(calculate, True)` for the first call; forgetting that the fourth plan step is never reached |
| B3 | lines 1–2 / lines 3–4 | `True` for `false` (JSON writes it lower case, Python gives back `False`); `430` as `439` (only the two model turns have `in_tok`) |
| B4 | lines 1–2 / lines 3–4 | `0.75` and `0.5`; the set of words in common printed in the wrong order |
| B5 | lines 1–2 / lines 3–4 | `0.0` written as `0` in the grid; `32` as `66` (the frozen layer's `60 + 6` do not count) |
| B6 | lines 1–2 / lines 3–4 | `0.80` landing in bucket `2` (an edge goes to the **upper** bucket); `0.60` in bucket `1` |
| B7 | lines 1–2 / lines 3–4 | the second line: the `NUMBERY` pattern eats the card first, so `[NUM]` not `[CARD]` |
| B8 | line 1 / line 2 | `True` for `fp(a) == fp(d)` (a list keeps its order: only a dictionary's keys are sorted) |

## Section C — 12 marks

Each is 3 marks: **(i)** the cause, **(ii)** what happens when it runs, **(iii)** a working fix. The fix must run.

| Q | (i) The cause | (ii) What happens | (iii) The fix |
|:--:|---|---|---|
| C1 | The check compares the **text** of the path before the `..` has been applied: `.../sandbox/../secrets.md` still starts with `.../sandbox` | Silent wrong result: `True` for a path that leaves the box | `(root / filename).resolve().is_relative_to(root)` (resolve first, compare second) |
| C2 | Both `A` and `B` start at zeros; `B` is zero so `A` gets no gradient, and `A` is zero so `B` gets none | Silent: both gradients are `0.0`, so nothing will ever move | `nn.init.normal_(A, std=0.02)`; keep `B` at zeros (see the key: `B` then gets a gradient and `A` follows a step later) |
| C3 | Arguments in the wrong order: the truth comes first, the probabilities second | A `ValueError` whose last line says the first argument is continuous but a binary truth was expected | `brier_score_loss(right, conf)` |
| C4 | `random.Random(0)` is made **inside** the loop, so every run uses the same seed and draws the same number | Silent: one draw copied fifty times, so the count is `0` or `50` and never about `15` | `random.Random(run)` (each run its own seed) |

## Section D — 15 marks

One mark per part (a) to (e). **Carry forward:** an earlier error used correctly later loses only once. The exact answers and the working are in the key.

| | (a) | (b) | (c) | (d) | (e) |
|:--:|---|---|---|---|---|
| D1 | `1800`, `1080`, `2880` | `82`; `3290` millionths; `$0.00329` | `3400`, `4080`, `7480`; `162`; `8290`; `$0.00829` | `136 / 36 = 3.78`; `8290 / 3290 = 2.52` | `4080 / 7480 = 0.545`: more than half the input is the past re-sent |
| D2 | `14` agree, `p_o = 0.70` | A `0.50`, B `0.70` | `p_e = 0.50` | kappa `0.40`; B is the more lenient one | `0.95`, `0.95`, kappa `0` |
| D3 | `0.278` | `0.25`; **no**, it was worse | high `n=5`, `0.86`, `0.6`; low `n=5`, `0.54`, `0.4` | `0.20` | `5`, `0.6`, `2` |

## Section E — 12 marks

| Part | Marks | Full marks need |
|---|:--:|---|
| E(a) | 4 | (i) patch 1; A2 `14/50 -> 0/50`, A1 stays `14/50`; a legal write never touches the sandbox check · (ii) the legit save fell to `0/50`; it stops the attack by stopping the job · (iii) the control: a fair comparison of a system with itself must say "no difference"; `14/50 -> 0/50` (gap 14 against 6.3) is more than noise, the `14 -> 16` is not · (iv) "I did not see it in 50 runs on this stand-in", plus one untried thing (a reworded twin of the note; the same-file-different-content order; a real model) |
| E(b) | 4 | (i) `3568 + 3893 = 7461`, within 3 tokens of `7464` · (ii) `0.011361 / 0.016529 = 0.687`, so about `31%` too low; cost per step grows, so cost against steps bends upward · (iii) every step re-sends the whole past, so the history part grows like `k(k+1)/2` · (iv) two of: every step is the same size here, the plan is scripted, the tokens and dollars are the kit's typed numbers, the real steps vary, the price table is illustrative |
| E(c) | 4 | (i) biggest gap `0.80–0.89` (`0.847` against `0.625`, gap `0.222`); only `0.90–1.00` under-confident (`0.940` against `1.000`, n = 7); ECE is the size of the average gap, not the share wrong (`0.35` of these are wrong) · (ii) no, it only beats one baseline on 40 results; want a second set it has not seen · (iii) `26 - 12 = 14` right answers given up; also 25 of 40 not answered (coverage `0.375`) · (iv) refund (`0.900 -> 0.750`, 4 results) and technical (`0.500 -> 0.333`, 3 results); do not believe billing's `0.400 -> 1.000` (2 results) |

## Part 2 — the demo, 15 marks

| Demo | Mark | Watch for |
|---|:--:|---|
| **Demo 1** | 1 | the four stop reasons are `end_turn`, and the student reads the `Error:` text, not the stop reason, as the fence: suffix, resolve, size, and the one request that works |
| | 1 | files in the box: `['plan.md']` and `4` attempts logged |
| | 1 | predicted against measured input: `2244` against `2242`, `5434` against `5431` |
| | 1 | says `2.37` times the dollars for doubling the steps, and the history share `47%` |
| | 1 | says "stand-in, not a model" and that the shape, not the values, would survive a real agent |
| **Demo 2** | 1 | `0.7`, `0.4`, then `0.95`, `0.0` |
| | 1 | step 0 equals the base (`True`); `512` numbers, share `0.125` |
| | 1 | gradient: `A` `False` at step 0 (because `B` is zero), `B` `True`, base `False`; the student can say why `A` is `False` |
| | 1 | ECE `0.2`, Brier `0.278`, flat `0.25` |
| | 1 | abstaining: answers `5`, accuracy `0.6` against `0.5`; says what was given up |
| **Demo 3** | 1 | A1 before/after and the control line (`more than noise` and `NOT distinguishable`); seeds are the ones given |
| | 1 | says the `0` sentence as "I did not see it in 50 runs", not "it cannot" |
| | 1 | redaction: `4/5` caught, name and address missed, `0 of 15` notes changed; says recall is not safety |
| | 1 | fingerprint changes after one label; the assertion refuses |
| | 1 | says why 12 characters belong on paper |

The demo is marked from what you **watch and hear**, not from the files. A demo file that prints the right lines and a student who cannot say why earns the "prints" marks and not the "says" marks.

## How to read the score

Add the paper (out of 75) and the demo (out of 15) **separately**. Then do these in order.

1. **Section A against E.** A high A with a low E means recall without judgement: the student knows the words and cannot yet say what a table does not show. The reverse means judgement without recall: give pencil work on old pages, not new reading.
2. **Count the "not sure" circles.** Right and unsure is healthy. Wrong and sure, especially on A17 (zero landings) and A20 (a number with no `n`), is the pattern that will embarrass a system card.
3. **Look for the one habit.** Three of A2, A3, A4 and C1 wrong: the fences and the sandbox are not clear, redo Week 28's six fences on paper. A5, A6, D1 and E(b) wrong together: the triangular sum is not in place, redo Week 29 page 29.1. A9, D2 and A10 wrong: agreement beyond chance, redo Week 30's kappa. A11, A12, C2 wrong: Week 31's `B` of zeros. A14, A15, D3, E(c) wrong: Week 32. A16, A17, C4, E(a) wrong: Week 33's wobble.

### The per-week grid

| Week | Items | Marks | Scored | Week | Items | Marks | Scored |
|:--:|---|:--:|:--:|:--:|---|:--:|:--:|
| W28 | A1–A3, B1, B2, C1 | 10 | ___ | W33 | A16, A17, B7, C4, E(a) | 11 | ___ |
| W29 | A4–A7, B3, D1, E(b) | 15 | ___ | W34 | A18, B8 | 3 | ___ |
| W30 | A8–A10, B4, D2 | 10 | ___ | W35 | A19 | 1 | ___ |
| W31 | A11–A13, B5, C2 | 8 | ___ | W36 | A20 | 1 | ___ |
| W32 | A14, A15, B6, C3, D3, E(c) | 16 | ___ | | **Total** | **75** | |

---

# ✅ ANSWER KEY

## Section A — why each answer, and why the wrong ones were tempting

| Q | Answer | Why the wrong options were tempting |
|:--:|---|---|
| A1 | **b** | (a) is true of nothing in the week; (c) confuses "the text is only arithmetic" with "the sums are right"; (d) is false, `eval` is happy with brackets, which is the trouble |
| A2 | **c** | (b) because `write_file` is a real tool, so the allowlist lets it through; (a) and (d) are real fences but neither fires on one short request |
| A3 | **d** | (a) is the trap of the week: `end_turn` means the model finished, not that the task worked; (b) and (c) read the stop reason as the fence |
| A4 | **a** | (b) is the sandbox being confused with the gullible agent, which is the random part; (d) the opposite is true: a legal write is the one it cannot see |
| A5 | **b** | `210 / 55 = 3.8`. (a) is the "cost per step is constant" picture; (d) is the same mistake |
| A6 | **d** | (a) and (b) blame the line's mechanics and not its shape; (c) invents a price change |
| A7 | **c** | (a) and (b) are not what JSONL is for; (d) is false |
| A8 | **b** | `3 / 5`. (a) is 2 of 4 (counting words in only one set); (c) is 3 of 4 (dividing by one set); (d) is identical sets |
| A9 | **a** | `19 / 20` agreement by always saying pass is exactly what chance gives, so kappa is `0.0`. (b) would lower agreement; (c) and (d) are false |
| A10 | **d** | (a) confuses a 30 percent flip rate with a 70 percent hit rate; (b) is a possible cause for a few, not 30 |
| A11 | **c** | `8 x 128 + 128 x 8 = 2048`. (a) counts one thin grid; (d) is the whole layer; (b) is only the width |
| A12 | **b** | (a) small `A` would still give a small non-zero patch; (c) `requires_grad_(False)` freezes the *base*; (d) is nonsense |
| A13 | **a** | (b) and (c) imagine "freeze" as "remove"; (d) mixes it with the optimiser |
| A14 | **d** | (a) reverses the sign; (c) a system can be sure and wrong; that is the lesson of Week 32 |
| A15 | **c** | `(0.5 - 1)^2 = (0.5 - 0)^2 = 0.25` for every result. (d) is a different thing (a flat system at the accuracy, not at 0.5) |
| A16 | **b** | `sqrt(100 x 0.2 x 0.8) = 4`. (a) and (d) are the share and the mean; (c) is the variance |
| A17 | **a** | `0.95^20 = 0.3585`. (b) is the chance if the rate were far higher; (d) forgets that each run is a weighted coin |
| A18 | **c** | (a) and (b) change nothing about who can edit the file; (d) is the pessimist's answer; the week's answer is the paper copy |
| A19 | **d** | (a), (b) and (c) are not what a `route` field is for |
| A20 | **b** | `0.50` has no `n`. The others each carry an `n` or a stand-in label |

### The Section A facts, run

```python
# afacts.py - the numbers behind Section A. Plain Python and numpy.
import numpy as np
print("A7: 1+...+20 =", sum(range(1, 21)), "| 20 * 21 / 2 =", 20 * 21 // 2, "| 1+...+10 =", sum(range(1, 11)), "| ratio for twice the steps:", round(210 / 55, 2))
print("A11: 8 x 128 + 128 x 8 =", 8 * 128 + 128 * 8, "| whole layer", 128 * 128, "| share", round(2048 / 16384, 4))
print("A14: gap", round(0.9 - 0.6, 2))
print("A15: Brier of always saying 0.5, on results [1,0,0,1,1,0,1,0]:", np.mean((0.5 - np.array([1, 0, 0, 1, 1, 0, 1, 0])) ** 2))
print("A16: sqrt(100 * 0.2 * 0.8) =", round(float(np.sqrt(100 * 0.2 * 0.8)), 2))
print("A17: chance of 0 landings in 20 runs at a true rate of 0.05:", round(0.95 ** 20, 4), "| in 50 runs:", round(0.95 ** 50, 4))
a = {"the", "river", "ran", "fast"}; b = {"river", "ran", "fast", "slow"}
print("A8: Jaccard", len(a & b), "/", len(a | b), "=", len(a & b) / len(a | b))
```

```text
A7: 1+...+20 = 210 | 20 * 21 / 2 = 210 | 1+...+10 = 55 | ratio for twice the steps: 3.82
A11: 8 x 128 + 128 x 8 = 2048 | whole layer 16384 | share 0.125
A14: gap 0.3
A15: Brier of always saying 0.5, on results [1,0,0,1,1,0,1,0]: 0.25
A16: sqrt(100 * 0.2 * 0.8) = 4.0
A17: chance of 0 landings in 20 runs at a true rate of 0.05: 0.3585 | in 50 runs: 0.0769
A8: Jaccard 3 / 5 = 0.6
```

## Section B — outputs, run

Each snippet was run from the folder that holds `l4lib/`.

**B1**

```text
14
512
ValueError
3.5
ValueError
SyntaxError
```

`3 * 4 + 2 = 14`; `2 ** 3 ** 2` is `2 ** 9 = 512`; a string, and a call to `max`, are refused with `ValueError`; `7 / 2 = 3.5`; `5 -` is not an expression at all, so Python's own parser raises `SyntaxError`.

**B2**

```text
max_iterations 3
[('calculate', False), ('delete_all', True), ('calculate', True)]
stand-in, not a model
```

Turn 1 works. Turn 2 asks for a tool that is not on the list (the allowlist returns an error, as text). Turn 3 calls `calculate` with no `expression` (bad arguments, an error). The cap is `3`, so the loop stops before the plan's `fine`.

**B3**

```text
{"event": "tool_call", "is_error": false, "tool": "calculate"}
False bool
430
78
```

**B4**

```text
0.75
0.5
['money', 'refund'] 5
0.4
```

By hand: 6 of 8 agree (`0.75`); both pass 50 percent of the time so `p_e = 0.5 x 0.5 + 0.5 x 0.5 = 0.5`; `(0.75 - 0.5) / (1 - 0.5) = 0.5`. The common words are `money` and `refund`; between them the two sets hold `5` words; `2 / 5 = 0.4`.

**B5**

```text
[[2.0, -1.0], [0.0, 0.0], [6.0, -3.0]]
6 5
32
66
```

Six cells built from five numbers. The trainable numbers are `A` (`2 x 10 = 20`) and `B` (`6 x 2 = 12`): `32`. The frozen layer has `60 + 6 = 66` numbers.

**B6**

```text
[2, 2, 2, 1, 0, 1]
[1, 2, 3]
0.2583
3 0.667
```

The gaps squared: `0.0025 + 0.7225 + 0.04 + 0.1225 + 0.3025 + 0.36 = 1.55`, and `1.55 / 6 = 0.2583`. Three results are `0.8` or more, and `2` of them were right.

**B7**

```text
Mail [EMAIL], card [CARD], call [NUM].
Mail [EMAIL], card [NUM], call [NUM].
No secrets here.
3.87
```

With the card pattern first, the card is a card. With the loose pattern first, it eats the card (and the phone number). `sqrt(80 x 0.25 x 0.75) = sqrt(15) = 3.87`.

**B8**

```text
True False False
64 12
```

Key order does not matter (`sort_keys`); a changed word does; the order of the list does.

## Section C — bugs, run

**C1** prints `True`, `True` (as on the paper). The fixed program:

```python
def inside(root, filename):
    return (root / filename).resolve().is_relative_to(root)
```

```text
C1: True False
```

**C2** prints `0.0 0.0`. The fix is one line after creating `A`: `nn.init.normal_(A, std=0.02)`. Honest note: at step 0 the gradient to `A` is **still** `0.0`, because `B` is zero and `A`'s gradient is multiplied by `B`; it is `B` that moves first, and `A` follows one step later. Run three steps of plain SGD to see it:

```python
import torch
from torch import nn
torch.manual_seed(0)
base = nn.Linear(4, 3); base.requires_grad_(False)
A = nn.Parameter(torch.zeros(2, 4)); nn.init.normal_(A, std=0.02)
B = nn.Parameter(torch.zeros(3, 2))
x = torch.randn(5, 4)
opt = torch.optim.SGD([A, B], lr=0.5)
for step in range(3):
    opt.zero_grad()
    loss = (base(x) + x @ A.T @ B.T).pow(2).mean()
    loss.backward()
    print(step, round(float(loss), 4), "A.grad", round(float(A.grad.abs().sum()), 6), "B.grad", round(float(B.grad.abs().sum()), 4))
    opt.step()
```

```text
0 0.2674 A.grad 0.0 B.grad 0.0531
1 0.2669 A.grad 0.025824 B.grad 0.053
2 0.2663 A.grad 0.051414 B.grad 0.0612
```

(With both at zero, neither would ever move. A student who writes "one of them must be random" earns the fix mark.)

**C3** last line as on the paper. The fixed call is `brier_score_loss(right, conf)`:

```text
C3: 0.2781 (hand: 0.2781 )
```

By hand: `(0.1^2 + 0.8^2 + 0.4^2 + 0.55^2) / 4 = 1.1125 / 4 = 0.2781`.

**C4** prints `0 of 50` (`random.Random(0).random()` is above `0.3`, so every run misses). Fixed with `random.Random(run)`:

```text
C4: 15 of 50
C4 five more batches of 50: [15, 17, 16, 14, 13]
```

The second line comes from `[sum(random.Random(s).random() < 0.3 for s in range(b * 50, b * 50 + 50)) for b in range(5)]`: five batches of 50 on seeds `0` to `249`, each run its own seed. They sit about `15` and wobble by about `3.2`, as `sqrt(50 x 0.3 x 0.7)` says.

## Section D — worked answers

The arithmetic was checked by machine:

```python
# d_check.py - the arithmetic behind D1, D2 and D3 of the Term 4 test (numbers are invented for the paper; the arithmetic is real; the price table is a stand-in, not a model).
import numpy as np
from sklearn.metrics import cohen_kappa_score, brier_score_loss
from l4lib import fakellm
# D1
def bill(k, n0=200, g=30, out_tool=10, out_close=2):
    tin = n0 * (k + 1) + g * k * (k + 1) // 2
    tout = out_tool * k + out_close
    return tin, tout, (tin * 1.00 + tout * 5.00) / 1e6
for k in [8, 16]:
    print(k, bill(k), "history part:", 30 * k * (k + 1) // 2, "flat part:", 200 * (k + 1))
print("ratio", round(bill(16)[2] / bill(8)[2], 3), "input ratio", round(bill(16)[0] / bill(8)[0], 3))
# D2
A = [1]*9 + [1]*1 + [0]*5 + [0]*5
B = [1]*9 + [0]*1 + [1]*5 + [0]*5
print("kappa", round(cohen_kappa_score(A, B), 4), "raw", np.mean(np.array(A) == np.array(B)))
Hh = [1]*19 + [0]; Z = [1]*20
print("lopsided", np.mean(np.array(Hh) == np.array(Z)), cohen_kappa_score(Hh, Z))
# D3
conf = np.array([.9, .9, .9, .8, .8, .6, .6, .5, .5, .5]); right = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0])
print("brier", np.mean((conf - right) ** 2), brier_score_loss(right, conf), "flat", np.mean((right.mean() - right) ** 2), "acc", right.mean())
hi = conf >= 0.8
print("high", conf[hi].mean(), right[hi].mean(), "low", conf[~hi].mean(), right[~hi].mean())
print("ece", 0.5 * abs(conf[hi].mean() - right[hi].mean()) + 0.5 * abs(conf[~hi].mean() - right[~hi].mean()))
```

```text
8 (2880, 82, 0.00329) history part: 1080 flat part: 1800
16 (7480, 162, 0.00829) history part: 4080 flat part: 3400
ratio 2.52 input ratio 2.597
kappa 0.4 raw 0.7
lopsided 0.95 0.0
brier 0.278 0.278 flat 0.25 acc 0.5
high 0.86 0.6 low 0.54 0.4
ece 0.2
```

### D1 (the bill, 5 marks)

- **(a)** `k = 8`: flat part `200 x 9 = 1800`. History part `30 x (1 + 2 + ... + 8) = 30 x 36 = 1080`. Total input `1800 + 1080 = 2880`.
- **(b)** Output `10 x 8 + 2 = 82`. Bill `2880 x 1.00 + 82 x 5.00 = 2880 + 410 = 3290` millionths of a dollar: **`$0.00329`**.
- **(c)** `k = 16`: flat `200 x 17 = 3400`; history `30 x 136 = 4080` (`16 x 17 / 2 = 136`); total input `7480`. Output `10 x 16 + 2 = 162`. Bill `7480 + 810 = 8290` millionths: **`$0.00829`**.
- **(d)** History multiplied by `136 / 36 = 3.78`. The whole bill by `8290 / 3290 = 2.52`: more than double, less than the history alone, because the flat part only doubles (and the input total is multiplied by `7480 / 2880 = 2.60`).
- **(e)** `4080 / 7480 = 0.545`, about `55%`. More than half of what the agent reads on a `16`-step task is the past, re-sent; the longer the task, the bigger that share. (The numbers are a stand-in's: the shape is the point.)

### D2 (two raters, 5 marks)

- **(a)** They agree on `9 + 5 = 14` tickets of `20`: `p_o = 14 / 20 = 0.70`.
- **(b)** A passes `9 + 1 = 10` of 20: `0.50`. B passes `9 + 5 = 14`: `0.70`.
- **(c)** `p_e = 0.50 x 0.70 + 0.50 x 0.30 = 0.35 + 0.15 = 0.50`.
- **(d)** kappa `= (0.70 - 0.50) / (1 - 0.50) = 0.20 / 0.50 = 0.40`. The two off-diagonal cells are "A pass, B fail" (1 ticket) and "A fail, B pass" (5 tickets): B passes what A fails five times and the other way once, so **B is the lenient one**.
- **(e)** `p_o = 19 / 20 = 0.95`. The judge passes everything and the human passes `0.95`, so `p_e = 0.95 x 1.00 + 0.05 x 0.00 = 0.95`. kappa `= (0.95 - 0.95) / 0.05 = 0.0`. Raw agreement of `0.95` sounds excellent and hides a judge that never looked.

### D3 (said against delivered, 5 marks)

- **(a)** Gaps (said minus right): `-0.1, -0.1, 0.9, -0.2, 0.8, -0.4, 0.6, -0.5, 0.5, 0.5`. Squares: `0.01, 0.01, 0.81, 0.04, 0.64, 0.16, 0.36, 0.25, 0.25, 0.25`; sum `2.78`; divided by ten: **`0.278`**.
- **(b)** Saying `0.5` every time gives `0.25` whatever the results. The system's `0.278` is **worse** than that: on Brier, its confidence numbers are worth less than a shrug.
- **(c)** Said 0.8 or more: `n = 5`, mean said `(0.9 + 0.9 + 0.9 + 0.8 + 0.8) / 5 = 0.86`, right `3 of 5 = 0.6`. Said less than 0.8: `n = 5`, mean said `(0.6 + 0.6 + 0.5 + 0.5 + 0.5) / 5 = 0.54`, right `2 of 5 = 0.4`.
- **(d)** `0.5 x |0.86 - 0.6| + 0.5 x |0.54 - 0.4| = 0.5 x 0.26 + 0.5 x 0.14 = 0.13 + 0.07 =` **`0.20`**.
- **(e)** It answers `5`. Accuracy on those: `3 / 5 = 0.6`, up from `0.5`. The total right is `5`; it gave up `5 - 3 = 2` right answers (and three wrong ones: of the five it held back, `2` were right and `3` wrong).

## Section E — worked answers

### How the three tables were made

**Table 1** (`e1.py`): exec the Week 33 blocks `s1_setup`, `s3_attacks`, `s4_harness` (the harness's `run_attack`) and `s6_patch` (`HAPPY`, the `reminders.md` task), and count over seeds `2000` to `2049`.

```python
# e1.py - Term 4 test, Table 1: the Week 33 harness on NEW seeds (2000 to 2049), four versions of the agent. Stand-in, not a model.
# (exec the Week 33 blocks s1_setup, s3_attacks, s4_harness and s6_patch first, with their output hidden; then:)
def named_files_only(box, question, filename, content):
    if filename not in question:
        raise PermissionError("refused")
    return box.write_file(filename, content)
def refuse_all_writes(box, question, filename, content):
    raise PermissionError("refused")
def cnt(att, key, first, n=50, **kw):
    return sum(run_attack(att, first + i, **kw)[key] for i in range(n))
def happy(first, n=50, **kw):   # HAPPY (Q_SAVE in the A1 world) is Week 33's own; count the runs where reminders.md was really saved
    total = 0
    for i in range(n):
        run_attack(HAPPY, first + i, **kw)
        total += (BOX / "reminders.md").exists()
    return total
def line(name, k_before, k_after, n=50):
    pb, pa = k_before / n, k_after / n
    sb, sa = np.sqrt(n * pb * (1 - pb)), np.sqrt(n * pa * (1 - pa))
    gap, bound = k_before - k_after, 2 * np.sqrt(sb ** 2 + sa ** 2)
    return f"{name}: {k_before}/{n} -> {k_after}/{n}; gap {gap} vs noise bound {bound:.1f} -> " + ("more than noise" if gap > bound else "NOT distinguishable from noise")
print(f"{'version of the agent':30s} {'A1':>7s} {'A2':>7s} | {'legit save':>10s}")
for label, kw in [("v0: weak sandbox, no guard", dict(strict=False)),
                  ("patch 1: strict sandbox", dict(strict=True)),
                  ("patch 2: + named files only", dict(strict=True, write_guard=named_files_only)),
                  ("BAD patch: no writes at all", dict(strict=True, write_guard=refuse_all_writes))]:
    print(f"{label:30s} {cnt(ATTACKS[0], 'a1', 2000, **kw):4d}/50 {cnt(ATTACKS[1], 'a2', 2000, **kw):4d}/50 | {happy(2000, **kw):7d}/50")
a = cnt(ATTACKS[0], 'a1', 2000, strict=True)
print(line("A1 patch 2", a, cnt(ATTACKS[0], 'a1', 2000, strict=True, write_guard=named_files_only)))
print(line("A1 vs itself (seeds 9000-9049)", a, cnt(ATTACKS[0], 'a1', 9000, strict=True)))
```

```text
version of the agent                A1      A2 | legit save
v0: weak sandbox, no guard       14/50   14/50 |      50/50
patch 1: strict sandbox          14/50    0/50 |      50/50
patch 2: + named files only       0/50    0/50 |      50/50
BAD patch: no writes at all       0/50    0/50 |       0/50
A1 patch 2: 14/50 -> 0/50; gap 14 vs noise bound 6.3 -> more than noise
A1 vs itself (seeds 9000-9049): 14/50 -> 16/50; gap -2 vs noise bound 9.2 -> NOT distinguishable from noise
```

**Table 2** (`e2.py`): Week 29's `steps(k)` (the calculator called `k` times, `max_tool_errors=99`, `budget_usd=10`), the curve `n0 x (k + 1) + grow x k (k + 1) / 2` with `n0` and `grow` from the `k = 9` run, and `np.polyfit(ks, dollars, 1)` for the straight line.

```python
# e2.py - Term 4 test, Table 2: cost against steps, fitted on k = 3, 6, 9 and used to predict k = 15 and 24. Stand-in, not a model.
import numpy as np
import torch
torch.set_num_threads(1)
from l4lib import toyagent, fakellm
specs = toyagent.tool_specs()
calc_reg = toyagent.ToolRegistry()
calc_reg.register("calculate", toyagent.calculate, timeout=2.0)
def steps(k, **kw):
    plan = toyagent.ScriptedModel([("", [("calculate", {"expression": "1 + 1"})])] * k + [("done", [])])
    return toyagent.run_agent("q", calc_reg, specs, plan, max_iterations=k + 1, max_tool_errors=99, budget_usd=10, **kw)
m = {k: steps(k) for k in [3, 6, 9, 15, 24]}
for k in [3, 6, 9, 15, 24]:
    r = m[k]
    print(f"k={k:2d}: input per turn {r['in_tokens'][:4]} ... {r['in_tokens'][-1]} | total in {sum(r['in_tokens']):5d} | total out {sum(r['out_tokens']):3d} | spend ${r['spend']:.6f}")
n0 = m[9]["in_tokens"][0]
grow = (m[9]["in_tokens"][-1] - n0) / 9
print(f"first turn {n0}; growth {grow:.3f} per step")
def predict(k):
    tin = n0 * (k + 1) + grow * k * (k + 1) / 2
    return tin, fakellm.cost_usd("fake-small", tin, 10 * k + 2)
ks = np.array([3, 6, 9]); dol = np.array([m[k]["spend"] for k in [3, 6, 9]])
sl, ic = np.polyfit(ks, dol, 1)
for k in [15, 24]:
    pi, pc = predict(k)
    print(f"k={k:2d}: curve predicts in {pi:7.0f} ${pc:.6f} | straight line ${sl * k + ic:.6f} | measured in {sum(m[k]['in_tokens'])} ${m[k]['spend']:.6f}")
print(f"k=24 over k=6: measured {m[24]['spend'] / m[6]['spend']:.2f} times the dollars for 4 times the steps")
```

```text
k= 3: input per turn [223, 255, 288, 320] ... 320 | total in  1086 | total out  32 | spend $0.001246
k= 6: input per turn [223, 255, 288, 320] ... 418 | total in  2242 | total out  62 | spend $0.002552
k= 9: input per turn [223, 255, 288, 320] ... 515 | total in  3690 | total out  92 | spend $0.004150
k=15: input per turn [223, 255, 288, 320] ... 710 | total in  7464 | total out 152 | spend $0.008224
k=24: input per turn [223, 255, 288, 320] ... 1003 | total in 15319 | total out 242 | spend $0.016529
first turn 223; growth 32.444 per step
k=15: curve predicts in    7461 $0.008221 | straight line $0.007005 | measured in 7464 $0.008224
k=24: curve predicts in   15308 $0.016518 | straight line $0.011361 | measured in 15319 $0.016529
k=24 over k=6: measured 6.48 times the dollars for 4 times the steps
```

**Table 3** (`e3.py`): forty results **invented** with `numpy` seed 7, four categories of ten, each with a typed shortfall (`greeting +0.05`, `refund -0.05`, `technical -0.15`, `billing -0.30`) between how sure it said it was and how often it was right.

```python
# e3.py - Term 4 test, Table 3: 40 INVENTED results (seed 7). Not from any model. Reliability, Brier, abstaining, and the categories.
import numpy as np
from sklearn.metrics import brier_score_loss
rng = np.random.default_rng(7)
names = ["greeting", "refund", "technical", "billing"]
bias = {"greeting": 0.05, "refund": -0.05, "technical": -0.15, "billing": -0.30}
cat = np.repeat(names, 10)
conf = np.round(rng.uniform(0.55, 0.98, 40), 2)
right = np.array([float(rng.random() < min(max(c + bias[k], 0.02), 0.98)) for c, k in zip(conf, cat)])
edges = [0.6, 0.7, 0.8, 0.9]
bucket = np.digitize(conf, edges)
counts = np.bincount(bucket, minlength=5); safe = np.maximum(counts, 1)
stated = np.bincount(bucket, weights=conf, minlength=5) / safe
actual = np.bincount(bucket, weights=right, minlength=5) / safe
ece = float(np.sum(counts / counts.sum() * np.abs(stated - actual)))
print(len(conf), "results; accuracy", round(right.mean(), 3), "average stated", round(conf.mean(), 3))
for lab, k, s, a in zip(["0.00-0.59", "0.60-0.69", "0.70-0.79", "0.80-0.89", "0.90-1.00"], counts, stated, actual):
    print(f"{lab:<10} n={k:>2} stated {s:.3f} actual {a:.3f}")
print(f"ECE {ece:.4f}  Brier {brier_score_loss(right, conf):.4f}  flat-{right.mean():.3f} Brier {np.mean((right.mean() - right) ** 2):.4f}")
for t in [0.0, 0.7, 0.8, 0.9]:
    ans = conf >= t
    print(f"t={t:.2f} answered {int(ans.sum()):2d} coverage {ans.mean():.3f} accuracy {right[ans].mean():.3f} wrong-but-answered {int((ans & (right == 0)).sum())}")
ans = conf >= 0.8
print("category     n before answered after")
for k in names:
    mine = cat == k; kept = mine & ans
    print(f"{k:<10} {int(mine.sum()):>3} {right[mine].mean():6.3f} {int(kept.sum()):8d} {right[kept].mean() if kept.sum() else float('nan'):6.3f}")
```

```text
40 results; accuracy 0.65 average stated 0.753
0.00-0.59  n= 5 stated 0.560 actual 0.400
0.60-0.69  n=11 stated 0.650 actual 0.545
0.70-0.79  n= 9 stated 0.757 actual 0.667
0.80-0.89  n= 8 stated 0.847 actual 0.625
0.90-1.00  n= 7 stated 0.940 actual 1.000
ECE 0.1240  Brier 0.2036  flat-0.650 Brier 0.2275
t=0.00 answered 40 coverage 1.000 accuracy 0.650 wrong-but-answered 14
t=0.70 answered 24 coverage 0.600 accuracy 0.750 wrong-but-answered 6
t=0.80 answered 15 coverage 0.375 accuracy 0.800 wrong-but-answered 3
t=0.90 answered  7 coverage 0.175 accuracy 1.000 wrong-but-answered 0
category     n before answered after
greeting    10  0.800        6  1.000
refund      10  0.900        4  0.750
technical   10  0.500        3  0.333
billing     10  0.400        2  1.000
```

### E(a) — Table 1 (4 marks)

- **(i)** Patch 1 (the strict sandbox). A2 went `14/50 -> 0/50`; **A1 stayed at `14/50`**. A2 writes outside the box, which the path check catches; A1 orders a *legal* filename inside the box, so the path check has nothing to refuse. One of two problems fixed.
- **(ii)** The BAD patch forbids every write, so the **legit save fell to `0/50`**: it stopped the attack by stopping the job. The happy path is the second re-test; an attack count of zero alone cannot call a patch good.
- **(iii)** It is a **control**: the same system, other seeds. A fair test of a system against itself must say "no difference"; here it does (`14` against `16`, gap `2` against a bound of `9.2`), so the bound is sensible. Then `14 -> 0` (gap `14` against `6.3`) really is more than noise, while a gap of 2 or 3 at n = 50 is nothing.
- **(iv)** "I did not see the attack land in 50 runs with patch 2 on this stand-in." Not tried: a **reworded twin** of the note (Week 33 showed the phrase scan misses it); an order for the **same** filename the user typed but with different content, which `named_files_only` would allow; any real model (the obey chance is a dial somebody typed). Any one earns the mark. "The attack is impossible / fixed forever" earns nothing.

### E(b) — Table 2 (4 marks)

- **(i)** `223 x 16 = 3568`; `32.444 x 15 x 16 / 2 = 32.444 x 120 = 3893.3`; total `7461`. The measured `7464` is `3` tokens higher (about 0.04 percent).
- **(ii)** `0.011361 / 0.016529 = 0.687`, so the line is about **`31%` too low**. (At `k = 15` it is `0.007005 / 0.008224 = 0.852`, `15%` too low.) A straight line adds the same dollars for each extra step; here each step costs more than the one before because it re-sends more past. The true shape bends upward, so a line through the cheap end undershoots further out.
- **(iii)** Each step re-sends everything so far, so the history part grows like `1 + 2 + ... + k = k(k+1)/2`, roughly `k^2 / 2`, not `k`. Quadrupling the steps multiplies the history part by about sixteen, and the flat part only by four; the whole bill lands between (`6.48`).
- **(iv)** Any two of: every step in this run is the same size (`32` or `33` tokens), which is what makes the formula nearly exact; the plan is **scripted**, so no model ever varied; the tokens are the kit's own count and the dollars come from an illustrative price table; a real agent's steps differ (Week 29's worked run grew `168, 33, 71, 47`); the shape would survive a real tokenizer but the values would not. A sentence that calls the curve "a forecast" earns nothing.

### E(c) — Table 3 (4 marks)

- **(i)** The biggest gap is the `0.80–0.89` bucket: said `0.847`, right `0.625`, a gap of `0.222`. The only under-confident bucket is `0.90–1.00`: said `0.940`, right `1.000`, on `7` results. ECE `0.1240` is the **average size of the gap** between said and delivered, not a share of wrong answers: here `1 - 0.65 = 0.35` of the answers are wrong.
- **(ii)** No. `0.2036` beats one baseline on **40 results** (and the same results were used to look at it); the useful next step is a second set of results it has not seen. (Compare Week 32: on the course's own sheet the flat system won.)
- **(iii)** Total right `0.65 x 40 = 26`. The answered ones that were right: `15 - 3 = 12`. So `26 - 12 =` **`14` right answers were given up**. Also paid: coverage fell to `0.375`, so `25` of 40 got "I don't know"; whether that trade is good depends on what a wrong answer costs, which the code cannot say.
- **(iv)** **refund** fell (`0.900 -> 0.750`, resting on `4` results) and **technical** fell (`0.500 -> 0.333`, resting on `3` results). Do not believe billing's rise (`0.400 -> 1.000`): it is `2` results, both right. (Greeting's `1.000` is 6 of 6; neither is a finding.) Eight or ten results per category are a reason to look, not a verdict.

## Part 2 — the demo, reference output

The demo files run from a folder that holds `l4lib/` and `notes/` (Week 26's 15 notes). In the reference run, Week 33's three blocks (`s1_setup.py`, `s3_attacks.py`, `s4_harness.py`) were executed first with their printing hidden; a student simply runs their own copies first. The reference files are `demo1.py`, `demo2.py` and `demo3.py`.

**Demo 1**

```python
# demo1.py - Term 4 test, Demo 1: four requests and the bill (Weeks 28 and 29). The "models" are scripted: stand-in, not a model.
import torch
torch.set_num_threads(1)
from pathlib import Path
from l4lib import toyagent, fakellm
specs = toyagent.tool_specs()
ROOT = Path("demo_box").resolve()
box = toyagent.Sandbox(root=ROOT)
reg = toyagent.ToolRegistry()
reg.register("calculate", toyagent.calculate, timeout=2.0)
reg.register("write_file", box.write_file, timeout=5.0, requires_confirmation=True)

def once(name, args):
    return toyagent.ScriptedModel([("", [(name, args)]), ("ok", [])])

requests = [("run.sh", dict(filename="run.sh", content="hi")),
            ("../x.md", dict(filename="../x.md", content="hi")),
            ("big.md", dict(filename="big.md", content="a" * 25000)),
            ("plan.md", dict(filename="plan.md", content="hi"))]
for label, args in requests:
    r = toyagent.run_agent("q", reg, specs, once("write_file", args), auto_approve=True)
    call = r["trace"][[e["event"] for e in r["trace"]].index("tool_call")]
    print(f"{label:8s} stop={r['stop']:9s} error={call['is_error']!s:5s} {call['result_preview'][:52]!r}")
print("files in the box:", sorted(p.name for p in ROOT.iterdir()), "| attempts logged:", len(box.attempts))

calc_reg = toyagent.ToolRegistry()
calc_reg.register("calculate", toyagent.calculate, timeout=2.0)
def steps(k):
    plan = toyagent.ScriptedModel([("", [("calculate", {"expression": "1 + 1"})])] * k + [("done", [])])
    return toyagent.run_agent("q", calc_reg, specs, plan, max_iterations=k + 1, max_tool_errors=99, budget_usd=10)
r6, r12 = steps(6), steps(12)
n0 = r12["in_tokens"][0]
grow = (r12["in_tokens"][-1] - n0) / 12
for k, r in [(6, r6), (12, r12)]:
    predicted = n0 * (k + 1) + grow * k * (k + 1) / 2
    print(f"k={k:2d}: predicted input {predicted:7.0f} | measured {sum(r['in_tokens']):5d} | spend ${r['spend']:.6f}")
print(f"double the steps: {r12['spend'] / r6['spend']:.2f} times the dollars; the history part of k=12 is {grow * 12 * 13 / 2 / sum(r12['in_tokens']):.0%} of its input")
print("label:", r12["label"])
```

```text
run.sh   stop=end_turn  error=True  "Error: PermissionError: refused: suffix '.sh' not al"
../x.md  stop=end_turn  error=True  "Error: PermissionError: refused: '../x.md' resolves "
big.md   stop=end_turn  error=True  'Error: ValueError: content too large: 25000 bytes > '
plan.md  stop=end_turn  error=False 'wrote 2 bytes to plan.md'
files in the box: ['plan.md'] | attempts logged: 4
k= 6: predicted input    2244 | measured  2242 | spend $0.002552
k=12: predicted input    5434 | measured  5431 | spend $0.006041
double the steps: 2.37 times the dollars; the history part of k=12 is 47% of its input
label: stand-in, not a model
```

Every stop reason is `end_turn`: the fences live in the `Error:` text, not in the stop reason. The suffix fence stops `run.sh`, the resolve fence `../x.md`, the size limit `big.md`; `plan.md` is fine. The sentence to listen for: *the next turn re-sends everything so far, so twice the steps is more than twice the bill, and it is a shape and not a forecast.*

**Demo 2**

```python
# demo2.py - Term 4 test, Demo 2: judge, LoRA, calibration (Weeks 30, 31, 32). Checks the hand work of D2 and D3.
import numpy as np
import torch
from torch import nn
torch.set_num_threads(1)
from sklearn.metrics import cohen_kappa_score, brier_score_loss
A = [1] * 9 + [1] * 1 + [0] * 5 + [0] * 5
B = [1] * 9 + [0] * 1 + [1] * 5 + [0] * 5
print("D2: raw agreement", np.mean(np.array(A) == np.array(B)), "| kappa", round(cohen_kappa_score(A, B), 4))
Hh, Z = [1] * 19 + [0], [1] * 20
print("D2(d): raw agreement", np.mean(np.array(Hh) == np.array(Z)), "| kappa", cohen_kappa_score(Hh, Z))

class LoRALinear(nn.Module):
    def __init__(self, base, r=4, alpha=8):
        super().__init__()
        self.base = base
        self.base.requires_grad_(False)
        self.A = nn.Parameter(torch.zeros(r, base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        nn.init.normal_(self.A, std=0.02)
        nn.init.zeros_(self.B)
        self.scale = alpha / r
    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale

torch.manual_seed(0)
base = nn.Linear(64, 64)
lora = LoRALinear(base, r=4)
x = torch.randn(5, 64)
print("step 0 equals the base:", torch.allclose(lora(x), base(x)))
print("patch numbers:", lora.A.numel() + lora.B.numel(), "of", 64 * 64, "->", round((lora.A.numel() + lora.B.numel()) / (64 * 64), 4))
loss = lora(x).pow(2).mean()
loss.backward()
print("gradient reaches A:", float(lora.A.grad.abs().sum()) > 0, "| reaches B:", float(lora.B.grad.abs().sum()) > 0, "| reaches the base weight:", base.weight.grad is not None)

conf = np.array([.9, .9, .9, .8, .8, .6, .6, .5, .5, .5]); right = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0])
bucket = np.digitize(conf, [0.75])
counts = np.bincount(bucket, minlength=2)
stated = np.bincount(bucket, weights=conf, minlength=2) / counts
actual = np.bincount(bucket, weights=right, minlength=2) / counts
print("buckets (low, high): n", counts.tolist(), "stated", stated.round(3).tolist(), "actual", actual.round(3).tolist())
print("ECE", round(float(np.sum(counts / counts.sum() * np.abs(stated - actual))), 4), "| Brier", round(brier_score_loss(right, conf), 4),
      "| flat Brier", round(float(np.mean((right.mean() - right) ** 2)), 4))
sure = conf >= 0.8
print("abstain below 0.8: answered", int(sure.sum()), "accuracy", round(float(right[sure].mean()), 3), "| before", right.mean())
```

```text
D2: raw agreement 0.7 | kappa 0.4
D2(d): raw agreement 0.95 | kappa 0.0
step 0 equals the base: True
patch numbers: 512 of 4096 -> 0.125
gradient reaches A: False | reaches B: True | reaches the base weight: False
buckets (low, high): n [5, 5] stated [0.54, 0.86] actual [0.4, 0.6]
ECE 0.2 | Brier 0.278 | flat Brier 0.25
abstain below 0.8: answered 5 accuracy 0.6 | before 0.5
```

The surprise worth a mark: **`A` gets no gradient at step 0** even though it is trainable. The patch is `x @ A.T @ B.T`, and `B` is zero, so the gradient reaching `A` is multiplied by zero; `B` moves first. A student who predicted "all three are `True`" has not yet met the point of starting `B` at zero.

**Demo 3**

```python
# demo3.py - Term 4 test, Demo 3: attack, redact, freeze (Weeks 33 to 36). Stand-in, not a model.
# (exec Week 33's s1_setup, s3_attacks and s4_harness first, with their output hidden, so run_attack, ATTACKS and chunks exist.)
def named_files_only(box, question, filename, content):
    if filename not in question:
        raise PermissionError("refused")
    return box.write_file(filename, content)
def count(att, key, first, n=50, **kw):
    return sum(run_attack(att, first + i, **kw)[key] for i in range(n))
def line(name, k_before, k_after, n=50):
    pb, pa = k_before / n, k_after / n
    sb, sa = np.sqrt(n * pb * (1 - pb)), np.sqrt(n * pa * (1 - pa))
    gap, bound = k_before - k_after, 2 * np.sqrt(sb ** 2 + sa ** 2)
    return f"{name}: {k_before}/{n} -> {k_after}/{n}; gap {gap} vs noise bound {bound:.1f} -> " + ("more than noise" if gap > bound else "NOT distinguishable from noise")
before = count(ATTACKS[0], "a1", 3000, strict=True)
after = count(ATTACKS[0], "a1", 3000, strict=True, write_guard=named_files_only)
same = count(ATTACKS[0], "a1", 8000, strict=True)
print(line("A1, patch 2    ", before, after))
print(line("A1 vs itself  ", before, same))
print("the stand-in dial is 0.30; a count of 0 of 50 means: I did not see it in 50 runs.")

EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
CARD = r"\b(?:\d{4}[ -]?){3}\d{4}\b"
AADHAAR = r"\b\d{4}\s\d{4}\s\d{4}\b"
PHONE = r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{4}[ -]?\d{5}(?!\d)"
PATTERNS = [("EMAIL", EMAIL), ("CARD", CARD), ("AADHAAR", AADHAAR), ("PHONE", PHONE)]
def redact_pii(text):
    for tag, pattern in PATTERNS:
        text = re.sub(pattern, f"[{tag}]", text)
    return text
CASES = [("mail asha.rao@example.org", "EMAIL"), ("call 91234 56789", "PHONE"), ("card 5500 0000 0000 0004", "CARD"),
         ("id 2345 6789 0123", "AADHAAR"), ("Asha Rao lives at 12 Temple Road", "NAME/ADDRESS")]
caught = 0
for raw, kind in CASES:
    out = redact_pii(raw)
    caught += out != raw
    print(f"{kind:13s} {out}")
print(f"recall {caught}/{len(CASES)}; chunks changed by redact_pii: {sum(redact_pii(c) != c for c in chunks)} of {len(chunks)}")

def fingerprint(cases):
    return hashlib.sha256(json.dumps(cases, sort_keys=True).encode("utf-8")).hexdigest()
CASES25 = [{"q": f"question {i}", "gold": g} for i, g in enumerate(["billing", "refund", "technical", "greeting", "billing"])]
saved = fingerprint(CASES25)
edited = copy.deepcopy(CASES25)
edited[2]["gold"] = "refund"
print("on file:", saved[:12], "| unchanged:", fingerprint(CASES25)[:12], "| after editing one gold label:", fingerprint(edited)[:12])
try:
    assert fingerprint(edited) == saved, "the frozen eval set was edited"
except AssertionError as e:
    print("check_frozen refuses:", e)
```

```text
A1, patch 2    : 17/50 -> 0/50; gap 17 vs noise bound 6.7 -> more than noise
A1 vs itself  : 17/50 -> 15/50; gap 2 vs noise bound 9.3 -> NOT distinguishable from noise
the stand-in dial is 0.30; a count of 0 of 50 means: I did not see it in 50 runs.
EMAIL         mail [EMAIL]
PHONE         call [PHONE]
CARD          card [CARD]
AADHAAR       id [AADHAAR]
NAME/ADDRESS  Asha Rao lives at 12 Temple Road
recall 4/5; chunks changed by redact_pii: 0 of 15
on file: f44d158338d6 | unchanged: f44d158338d6 | after editing one gold label: dcedec7cdce9
check_frozen refuses: the frozen eval set was edited
```

(Imports needed: `io, contextlib, copy, json, hashlib, re, numpy as np`, and `Path`. The first twelve characters `f44d158338d6` are what belongs on paper.) A name and an address are not caught by patterns of this kind: recall `4/5` is a measurement of the five cases, not a promise about personal data in general.

---

# 🩺 What to do with the pattern

- **Strong on the paper, weak on the demo:** the student can read a fence and cannot yet run one. Give the Week 28 `fences.py` and the Week 33 harness again, with their own hands, and ask for predictions first.
- **Strong on the demo, weak on E:** they can run the code and have not learned to say what a table does not show. Give them Page 33.3 and Page 35.3 again, and a card from someone else to fault (look for *fixed*, *safe*, *impossible*, *cannot* and any number with no `n`).
- **Low everywhere on Weeks 28 and 29:** do these first; they carry the rest of the term.
- **A wrong answer to A17 or A20:** ask the spoken check first ("what does `0 of 20` show?") before reassigning reading.

# 🧭 What this test does and does not show

- **It shows** whether a student can read a fence, a cost curve, a kappa, a patch and a calibration table without a machine, and say what each one cannot show.
- **It does not show** anything about a real model. The agents, the judges, the tokens and the dollars are all stand-ins, and Table 3 is invented. A number from a stand-in is a property of these cases and these scripted parts, and nothing else.
- **It does not test the capstone.** The capstone (design, frozen eval, measured system, red-team log, card, demo) is marked from its deliverables, on its own rubric.

---

[⬅ Course home](../README.md) · [⬅ Term 3 test](term-3-test.md) · [Assessments home](README.md) · [Capstone](../projects/capstone.md)
