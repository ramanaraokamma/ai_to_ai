# Workbook — Week 23: Prompting as Engineering: The Harness

**Name:** ________________________________  **Date:** ______________

[⬅ Week 22](week-22.md) · [📖 Read the chapter first](../student-guide/week-23.md) · [Course Home](../README.md) · [Next ➡](week-24.md)

---

![Map of the 36 weeks with Week 23, Prompting as Engineering: The Harness, highlighted in Term 3](../figures/fig-w23-0-where-this-fits.svg)
*Figure 23.0 — Week 23 is the fifth lesson of Term 3: asking a model is tested like code.*

> **Rules for this workbook.** Six pages, a "Break It" page and a Bug Log. **Write your prediction or your hand answer first, then run.** A guess written after the run is not a guess. Every number you write in the write-up (page 23.6) must have been printed by **your own** run in the last 24 hours, with the seed stated.
>
> **The "model" today is a stand-in, not a model.** `FakeClient` is a short Python script. It has the *shape* of a chat API and it does not read English. The harness around it (the frozen set, the scorer, the parser, the guard) is real; **nothing the stand-in scores says anything about how a real model behaves.** Wherever you write the word "model" for the thing that was scored, check that you did not mean "stand-in".
>
> **Real numbers.** Every printed number below came from a real CPU run of plain Python with the seeds shown. Nothing today uses `torch`, and every number comes from plain Python and a seeded hash, so **your numbers should match exactly**. Numbers marked **PRACTICE** are invented for this workbook so they are not the class numbers.
>
> **Files you need.** Your own `bench.py`, `guard.py` and `versions.py` from class, in one folder that also contains `l4lib/`. Each practice script below says which of them it needs. Name the practice scripts as shown (`p1.py`, `p2.py`, ...) so they do not overwrite your class files.
>
> **Calculator.** A phone is fine, airplane mode on. Keep every digit, and round only the answer.

---

## ✅ Warm-Up (5 min, before anything else)

Five short questions that use ideas from earlier weeks and this week's setup. Answer from memory, before you open any file.

**W1.** The best constant answer right on 14 of 32 fields scores `14 / 32` = ____________ (write it as a percentage with one decimal).

**W2.** Circle one. A prompt scores `50.0%` and the floor is `43.8%`. The prompt is: **half right** / **two fields above a rock**.

**W3.** A call uses 400 tokens in and 60 out. The price is $1.00 per million in and $5.00 per million out. Cost in dollars: `400 x 1.00 / 1,000,000 + 60 x 5.00 / 1,000,000` = ____________ + ____________ = ____________

**W4.** Circle one. A budget guard that adds up the cost **after** each call will stop the run: **before** / **after** the call that crosses the limit.

**W5.** In one sentence, what is `re.S` for? _____________________________________________

---

## 🧊 Page 23.1 — Freeze (needs `bench.py` · 20 min)

This page is for comparing your blind labels with the frozen gold, recording the fingerprint, and practising what a change to a frozen set looks like.

**A. Your blind labels.** You labelled the eight messages before you looked at `bench.py`. Copy your labels here (from your paper sheet), then, **after** reading `TESTS` in `bench.py`, mark each box **✓** (you and the gold agree) or **✗**.

| id | your `category` | your `urgency` | your `order_id` | your `refund_requested` |
|:--:|---|:--:|---|:--:|
| t1 | | | | |
| t2 | | | | |
| t3 | | | | |
| t4 | | | | |
| t5 | | | | |
| t6 | | | | |
| t7 | | | | |
| t8 | | | | |

Boxes where you and the gold disagree: `category` ____ · `urgency` ____ · `order_id` ____ · `refund_requested` ____ · in all ____ of 32.

Which field had the most disagreements? ____________ Why do you think so? _____________________________________________

**B. The fingerprint.** Run `python3 bench.py`. Write the fingerprint: ______________________. Now open `log.txt` (make it if you have not) and write the fingerprint and the date into it **before you do anything else**. Done? ☐

**C. A fingerprint on a tiny set (predict first).** Type this as `p1.py`. It uses only `hashlib`, which you have met.

```python
# p1.py - Workbook 23.1 (PRACTICE set): a fingerprint changes when one label changes.
import hashlib

MINI = [
    {"id": "p1", "text": "where is my parcel?? ordered K-1 a week ago", "gold": {"urgency": 2, "refund_requested": False}},
    {"id": "p2", "text": "thanks, all good now", "gold": {"urgency": 1, "refund_requested": False}},
    {"id": "p3", "text": "wrong item sent, order K-2, give me my money back", "gold": {"urgency": 2, "refund_requested": True}},
]


def fingerprint(cases):
    return hashlib.md5(repr(cases).encode("utf-8")).hexdigest()[:10]


before = fingerprint(MINI)
MINI[1]["gold"]["urgency"] = 2          # one digit of one label
after = fingerprint(MINI)
MINI[1]["gold"]["urgency"] = 1          # put it back
restored = fingerprint(MINI)
print("before  :", before)
print("after   :", after)
print("restored:", restored)
print("before == after    ?", before == after)
print("before == restored ?", before == restored)
```

I predict (circle): `before == after` is **True / False**. `before == restored` is **True / False**.

Run it. Copy the two `==` lines: ________________________________ / ________________________________

What does "restored" tell you about how a fingerprint could catch a change that somebody later *undid*? _____________________________________________

**D. The run that refuses to start (DELIBERATE).** This one is broken on purpose. Type it as `p1b.py` beside `bench.py`. It "fixes" t3's urgency gold to `3` **after** seeing that every prompt says `3`.

```python
# DELIBERATE: editing a gold label after the set was frozen.
from bench import TESTS, run_suite

TESTS[2]["gold"]["urgency"] = 3
run_suite("v3", lambda text: ("{}", 0, 0, 0.0), cases=TESTS)
```

Write the **last line** of the error: _____________________________________________

Which function in `bench.py` raised it? ____________________

Is the gold for t3's urgency really wrong? (Nobody knows: the message is polite but money is at risk.) Write the **honest** way to change a gold label, in four short steps (the first is "write the rule down"):

1. ______________________________ 2. ______________________________

3. ______________________________ 4. ______________________________

---

## 🪨 Page 23.2 — Floor (needs `bench.py` · 25 min)

The **floor** is the score of a constant answer that ignores the message. Any prompt has to beat it before it has learned anything.

**A. Count by hand (do not run yet).** Use the gold labels in `bench.py`. For each field, find the **most common** gold value and count how many of the 8 cases have it. Write the counts for **every** value, then circle the biggest.

| Field | Each value and how many of 8 | Best constant | Right out of 8 |
|---|---|---|:--:|
| `category` | billing ___ shipping ___ technical ___ account ___ other ___ | | |
| `urgency` | 1 ___ 2 ___ 3 ___ | | |
| `order_id` | `None` ___ (the others once each) | | |
| `refund_requested` | True ___ False ___ | | |

Total right: ____ + ____ + ____ + ____ = ____ out of `8 x 4` = ____ field decisions.

Floor as a percentage, one decimal: ____ / ____ = ____________

Two fields have a **tie** for best. Which? ____________ and ____________ . So the number of different constants that reach the top score is `3 x 2` = ____ (all with `order_id` = `None`, `refund_requested` = `False`).

**B. Run it and compare.** Run `python3 bench.py` and copy: `constants tried:` ____ , the best score ____ , the worst score ____ . Then run `s1.py`, which prints the first eight of the sorted 30:

```python
# s1.py - Workbook 23.2: the first eight constants, best first.
from bench import constant_baseline
rows = constant_baseline()
for s, rec in rows[:8]:
    print(f"{s * 100:5.1f}%", rec["category"], rec["urgency"], rec["refund_requested"])
```

How many of the eight printed rows show the top score? ____ Does that match your tie count from part A? Yes / No

**C. What does `50%` mean?** A prompt scores `50.0%` on these eight cases.

- Fields right: `0.50 x 32` = ____ .
- Fields right for the rock: ____ .
- Fields the prompt is above the rock: ____ (about ____ percentage points).
- Complete the sentence: "`50%` is not 'half right'. It means ______________________________________________ ."

**D. Why is the floor not zero?** One sentence about how the gold labels are spread (think of `order_id` and `refund_requested`): _____________________________________________

**E. A floor on a new set (PRACTICE).** A different frozen set has six cases and three fields. Here is its gold:

| case | `urgency` | `order_id` | `refund_requested` |
|:--:|:--:|:--:|:--:|
| p1 | 1 | `None` | True |
| p2 | 2 | `None` | False |
| p3 | 2 | `"K-1"` | False |
| p4 | 3 | `None` | False |
| p5 | 2 | `"K-2"` | True |
| p6 | 1 | `None` | False |

Best constant per field and how many of 6 it gets: `urgency` ____ , ____ of 6 · `order_id` ____ , ____ of 6 · `refund_requested` ____ , ____ of 6.

Field decisions right: ____ of `6 x 3` = ____ . Floor: ____________ %

How many constants would you have to try, if the constant `order_id` is always `None`, `urgency` can be 1, 2 or 3, and `refund_requested` can be True or False? ____ `x` ____ = ____

Now check by machine. Type `p2.py` (plain loops and a dict; it counts, you read):

```python
# p2.py - Workbook 23.2 (PRACTICE): count each value, to check your hand count.
GOLD = [
    {"urgency": 1, "order_id": None,  "refund_requested": True},
    {"urgency": 2, "order_id": None,  "refund_requested": False},
    {"urgency": 2, "order_id": "K-1", "refund_requested": False},
    {"urgency": 3, "order_id": None,  "refund_requested": False},
    {"urgency": 2, "order_id": "K-2", "refund_requested": True},
    {"urgency": 1, "order_id": None,  "refund_requested": False},
]
for field in ["urgency", "order_id", "refund_requested"]:
    tally = {}
    for g in GOLD:
        tally[g[field]] = tally.get(g[field], 0) + 1
    print(field, tally)
```

Copy the three printed lines: _______________________________________________

Did your hand counts match? Yes / No. If not, which field, and what did you miscount? ____________________

---

## 📋 Page 23.3 — Versions (needs `bench.py`, `guard.py`, `versions.py`, `l4lib/` · 25 min)

> **STAND-IN, NOT A MODEL.** Every score on this page is a script's. The point of the page is to read a table, not to learn which prompt a real model likes.

This page is for predicting, then reading, the table of three prompt versions, and for pricing each run by hand.

**A. Predict first (from the stand-in's one documented line, in the student guide).** The stand-in gets a field right with chance `p`. It uses `p = 0.55` for v1, `0.75` for v2 and `0.99` for v3. Only `30` of the 32 fields can ever match it (you will see why in part D).

- v1 should get about `0.55 x 30` = ____ fields right. In percent of 32: ____ %
- v3 should get about `0.99 x 30` = ____ fields right (round to a whole field). In percent of 32: ____ %
- Which column would you expect to cost more, v1 or v3? ____ Why? ____________________

**B. Run and fill the table.** Run `python3 versions.py`. Copy the **first three rows** (seed 0, cache off).

| Version | Field score | Exact | Parse-fail | Tokens in | Tokens out | Cost |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| v1-zero-shot | | | | | | |
| v2-rules | | | | | | |
| v3-few-shot | | | | | | |

Per-field correct (out of 8):

| Version | `category` | `urgency` | `order_id` | `refund_requested` |
|---|:--:|:--:|:--:|:--:|
| v1 | | | | |
| v2 | | | | |
| v3 | | | | |

**C. Three questions.**

1. How many fields is v1 above the rock? ____ (its fields right minus the floor's 14).
2. In v3, which single field is the bottleneck? ____________
3. Every version is below `100%`. The best any version got is ____ % . Write `30 / 32` as a percentage: ____ % . Does it match?

**D. Find the two fields nobody can get.** Type `s2.py`. It runs v3 again (seed 0) and prints every field it got wrong, with what the stand-in said and what the gold says.

```python
# s2.py - Workbook 23.3: which fields does v3 get wrong, and what did each side say?
from l4lib.fakellm import FakeClient
from bench import TESTS, run_suite, extract_json
from versions import PROMPTS, make_caller

_, res3 = run_suite("v3", make_caller(FakeClient(seed=0, prefix_cache=False), PROMPTS[2]))
for r, c in zip(res3, TESTS):
    for f in r.per_field:
        if r.per_field[f] == 0:
            print(r.id, f, "| stand-in said:", extract_json(r.raw)[f], "| gold says:", c["gold"][f])
```

Copy the printed lines: _______________________________________________

Look at the two messages (t3 and t8) in `TESTS`. Who is right about the urgency, the stand-in's rules or our gold? Circle: **the stand-in** / **our gold** / **neither: the specification does not decide it**

When **every** version fails the same case, what should you suspect first, the prompt or the test? ____________

**E. Dollars by hand.** Prices: $1.00 per million tokens in, $5.00 per million tokens out. Use your table.

| Version | `tokens in x 1.00 / 1,000,000` | `tokens out x 5.00 / 1,000,000` | Sum |
|---|:--:|:--:|:--:|
| v3 | | | |
| v2 | | | |
| v1 | | | |

Does the sum, rounded to four decimals, match the Cost column? v3 ____ v2 ____ v1 ____ (if v1 is off in the last digit, write the sum in full and see the answers)

About how many times more does v3 cost than v1? `cost(v3) / cost(v1)` = ____ ( one decimal )

> **Do not write** "v3 is the best prompt, so examples help." The stand-in **gives** v3 the higher chance by its own line. The table shows the harness reporting what the script does.

---

## 🎲 Page 23.4 — Noise (needs `bench.py`, `versions.py` · 25 min)

One run is one roll of a die. The stand-in's `seed` is which roll.

**A. The six seeds.** Run `python3 versions.py` again and copy the block "one seed is one draw" (field score in percent, seeds 0 to 5).

| Prompt | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | Mean | Min | Max |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| v1 | | | | | | | | | |
| v2 | | | | | | | | | |
| v3 | | | | | | | | | |

(Work out the Mean by hand: add the six, divide by 6, one decimal.)

**B. Read it.**

1. On how many of the six seeds is v1 **below** the `43.8%` floor? ____ On how many is it **exactly on** it? ____
2. Is v1 "better than the rock"? Circle: **yes, always** / **not reliably** / **no, never**. The number that shows it: ____________
3. The lowest v2 is ____ . The highest v1 is ____ . Is the gap between them bigger than the spread of either? Yes / No. So is v2 better than v1 on these six seeds? ____
4. v3 is the same on every seed. Does that mean it has no noise? ____________ (Hint: `p = 0.99` and 30 fields give almost no room for a wrong one, but some.)

**C. Which of these can you believe? (PRACTICE)** Here are five invented scores for each of two made-up prompts (seeds 0 to 4), in percent.

```python
A = [61.0, 48.0, 55.0, 66.0, 50.0]        # PRACTICE: prompt A (invented)
B = [72.0, 69.0, 75.0, 70.0, 79.0]        # PRACTICE: prompt B (invented)
```

By hand: mean of A = ____ , min ____ , max ____ . Mean of B = ____ , min ____ , max ____ .

Is B better than A, with an honest reason that uses the range? _____________________________________________

If somebody showed you **only** seed 0 (A = `61.0`, B = `72.0`), what would they have hidden? ____________________

**D. The regression report by hand (PRACTICE).** Three cases, four fields each. `1` means right, `0` means wrong.

| case | old: category, urgency, order_id, refund | new: category, urgency, order_id, refund |
|:--:|:--:|:--:|
| p1 | 1 1 0 0 | 1 0 1 1 |
| p2 | 1 1 1 1 | 1 1 1 1 |
| p3 | 0 1 1 0 | 1 0 1 1 |

- Old field score: fields right ____ of 12 = ____ %. New field score: ____ of 12 = ____ %.
- Did the score go up? ____
- List every `(case, field)` that was right in `old` and is wrong in `new`: _____________________________________________

Now check by machine. Type `p3.py` (needs `bench.py` and `versions.py`):

```python
# p3.py - Workbook 23.4 (PRACTICE): invented scores, and a made-up regression report.
from bench import CaseResult
from versions import regressions

A = [61.0, 48.0, 55.0, 66.0, 50.0]        # PRACTICE: prompt A over seeds 0-4 (invented)
B = [72.0, 69.0, 75.0, 70.0, 79.0]        # PRACTICE: prompt B over seeds 0-4 (invented)
for name, row in [("A", A), ("B", B)]:
    print(f"{name}: mean {sum(row) / len(row):.1f}  min {min(row):.1f}  max {max(row):.1f}")


def mk(case_id, c, u, o, r):
    return CaseResult(case_id, (c + u + o + r) / 4, {"category": c, "urgency": u, "order_id": o, "refund_requested": r},
                      True, 0, 0, 0.0, "")


old = [mk("p1", 1, 1, 0, 0), mk("p2", 1, 1, 1, 1), mk("p3", 0, 1, 1, 0)]
new = [mk("p1", 1, 0, 1, 1), mk("p2", 1, 1, 1, 1), mk("p3", 1, 0, 1, 1)]
print("old field score: %.1f%%" % (100 * sum(r.score for r in old) / 3))
print("new field score: %.1f%%" % (100 * sum(r.score for r in new) / 3))
print("lost:", regressions(old, new))
```

Copy the output: _______________________________________________

**E. The real regression report.** In the `versions.py` output, the block "regression report" has two lines. Copy the second one: _______________________________________________

The score **rose**. Name the two fields that were right before and wrong after: ____________ and ____________ . Why would somebody who looked only at the score have missed them? _____________________________________________

---

## 💸 Page 23.5 — Guard (needs `guard.py`, `versions.py` · 25 min)

This page is for working through the budget guard by hand, then checking your work against a run.

**A. By hand.** The guard adds each call's cost **after** the call, and raises `BudgetExceeded` the moment `spent` is **more than** the limit.

1. Every call costs `$0.0014`, limit `$0.01`. Fill in `spent` after each call until it crosses:

| call | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| spent | | | | | | | | |

The alarm goes off on call ____ . Spent at that moment: $________ . Over the limit by: $________ .

2. A call of 400 tokens in and 60 out costs (page W3) $________ . With a limit of `$0.01`, after how many calls is `spent` **still under** the limit? ____ On which call does it cross? ____ (Divide `0.01` by the cost first, then be careful: *more than*, not *equal to*.)

3. Why did the guard not stop you **before** the call that crossed the line? _____________________________________________

**B. A guard fed uneven costs (PRACTICE).** Predict, then run. Limit `$0.02`. Costs for calls 1 to 5, in dollars (invented): `0.004, 0.006, 0.005, 0.007, 0.003`.

| after call | 1 | 2 | 3 | 4 | 5 |
|---|:--:|:--:|:--:|:--:|:--:|
| predicted spent | | | | | |

I predict it stops at call ____ having spent $________ .

Type this script and run it beside `guard.py`.

```python
# p4.py - Workbook 23.5 (PRACTICE): a guard fed costs that are NOT all equal.
from guard import BudgetGuard, BudgetExceeded

costs = [0.004, 0.006, 0.005, 0.007, 0.003]      # PRACTICE: dollars for calls 1 to 5 (invented)
g = BudgetGuard(limit_usd=0.02)
for i in range(len(costs)):
    try:
        g.record(costs[i])
        print(f"after call {i + 1}: spent ${g.spent:.4f}")
    except BudgetExceeded as e:
        print(f"stopped at call {i + 1}: {e}")
        break
print(g.summary())
```

Copy the last two printed lines: _______________________________________________

Was call 5 ever made? ____ (Look at the loop: what does `break` do?)

**C. The guard on the whole run.** Open `versions.py` output, block "a budget guard on the whole run" (limit `$0.004`, seed 0). Copy the `STOPPED:` line and the last line:

`STOPPED:` ______________________________________________

Last line (the stand-in's own meter): ______________________________________________

Overspend: `spent - limit` = $________ . Which single call pushed it over, and is the overspend bigger or smaller than that call's cost? _____________

The guard and the stand-in's meter agree. Who is right? Circle: **the guard** / **the meter** / **both, they count the same 19 calls**

**D. Explain the exception in your own words.** `BudgetExceeded` is a class with nothing inside. Write what each of these does:

- `class BudgetExceeded(Exception): pass` : _____________________________________
- `raise BudgetExceeded("...")` : _____________________________________
- `except BudgetExceeded as e:` : _____________________________________
- Why is `except Exception:` dangerous in a loop that has a guard? _____________________________________

**E. (Fast students, optional.)** Price the run **before** making a call. If your teacher gave you a pre-flight script that prices the 24 calls before making any, write its two lines here: `calls made so far:` ____ , ceiling: $________ . Why is the ceiling higher than the real bill of `$0.0059`? _____________________________________________

---

## ✍️ Page 23.6 — Write-Up: What a Harness Showed and What It Did Not (20 min)

One page. Every number must be one your own run printed, with its seed.

**The numbers (fill from your runs, seed stated):**

| Thing | Number | Seed / where it came from |
|---|:--:|---|
| Frozen-set fingerprint | | |
| Floor (best constant) | | |
| v1 field score | | |
| v3 field score | | |
| Ceiling (the best score any version could reach: `30 / 32`) | | |
| Guard trip call on the whole run | | |

**1. What the harness showed.** Use the words "floor" and "spread". Finish: "A score only means something against ______________________ and against ______________________ ."

_______________________________________________________________________________

_______________________________________________________________________________

**2. What the stand-in cannot tell us.** One sentence that starts "The stand-in is not a model, so" ___________________________________________

_______________________________________________________________________________

**3. The four constructs, in your own words.** Run `constructs.py` once more and copy its six output lines on scrap paper. Then explain each in one or two sentences, with an example of your own.

- `@dataclass` : _____________________________________________________________

- a class with `__init__` and `self` : _____________________________________________________________

- `try` / `except` with your own exception, and `raise` : _____________________________________________________________

- `re.search(..., re.S)` : _____________________________________________________________

**4. Checklist.** ☐ every number printed by my own run ☐ every seed stated ☐ the word "stand-in" used wherever the thing scored was the script ☐ I did not write that examples help a real model ☐ I did not write that `93.8%` means "94% accurate"

---

## 🐞 Page 23.7 — Break It on Purpose (three bugs · 25 min)

**Each program is deliberately broken.** Do **not** run it first. For each, write **(i)** what the bug is, **(ii)** what you think the output says, **(iii)** the fixed line. *Then* run it (beside `bench.py` and `guard.py`).

**The reading method.** If there is an error, read the **last line**. If there is no error, ask what should be *true* of the output and check it: did the alarm reach the top? Does a reply that looks right score `1.0`?

**Bug 23.7-A. (SILENT)** A loop of 12 calls at `$0.0014`, limit `$0.01`. Predict both printed lines: how many calls "finished", and what the guard's summary says.

```python
# DELIBERATE BUG 23.7-A (SILENT): a catch-all except around the record call swallows the alarm.
from guard import BudgetGuard

guard = BudgetGuard(limit_usd=0.01)
done = 0
for i in range(12):
    try:
        guard.record(0.0014)
        done += 1
    except Exception:
        pass
print("calls that finished:", done)
print(guard.summary())
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 23.7-B. (SILENT)** The reply is well-formed JSON for t5. The programmer expects a perfect score. Predict `parsed`, `score` and which field is `0`.

```python
# DELIBERATE BUG 23.7-B (SILENT): the reply is well-formed JSON, but urgency came back as the TEXT "3".
from bench import TESTS, extract_json, score_record

reply = '{"category": "billing", "urgency": "3", "order_id": "C-77", "refund_requested": true}'
gold = TESTS[4]["gold"]
pred = extract_json(reply)
score, per = score_record(pred, gold)
print("parsed:", pred is not None)
print("gold  :", gold)
print("score :", score)
print("per   :", per)
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________ (hint: the fix goes in the *prompt* or in a conversion step, **not** in the gold.)

**Bug 23.7-C. (LOUD)** A guard class with one missing word. Read the **last line** of the error and say which line of the file is really at fault.

```python
# DELIBERATE BUG 23.7-C (loud): record is missing self.
class BudgetGuard:
    def __init__(self, limit_usd):
        self.limit = limit_usd
        self.spent = 0.0

    def record(cost):                       # <- forgot "self"
        self.spent += cost
        return self.spent


g = BudgetGuard(0.01)
g.record(0.0014)
```

(i) The bug: ___________________ (ii) I predict the last line says: ___________________ (iii) Fix: ___________________

**Which one would you catch without a table?** A and B ran with **no error**. For each, write the one thing you would print or check to catch it: A: ____________ B: ____________

---

## 📓 Page 23.8 — The Bug Log

Every entry needs a line from a **real** run of yours this week.

**Entry 1: a prediction I got wrong.** *"I predicted ______________, and the run printed ______________, because ____________________."*

_______________________________________________________________________________

**Entry 2: the one I was most tempted to believe.** The sentence *"v3 is the best prompt, so examples help"* is tempting. Write the two numbers from your own runs that stop you (the stand-in's `p` for v3, and the v1 spread over six seeds) and a sentence of your own.

Number 1: ____________ Number 2: ____________

_______________________________________________________________________________

**Entry 3: a slip, not a gap.** A digit or a count you lost that you knew how to get (a tie counted twice, `14` written as `14 of 8`, the guard's call number off by one). What was it, and what is the one habit that would have saved it?

Slip: ____________________ Habit: ___________________________________________

**Entry 4: the silent ones.** Name the check you will use after each of these: a `score` of `0.0` with no error → ____________ . A guard that never seems to stop → ____________ . A gold label you are tempted to edit → ____________ .

**Entry 5: the honest limits.** One thing today's stand-in *cannot* tell you about a real model, in your own words:

_______________________________________________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (from memory, no notes)

Six questions to answer last, without looking back at the pages.

1. The floor is the score of ____________________ . For our set it is ____ of 32, which prints as ____ %.
2. Freeze the set **before / after** (circle) you write the prompt, because ___________________________ .
3. `re.search(r"\{.*\}", reply)` on a reply spread over three lines gives ____ ; with `re.S` it gives ____________ .
4. `self.spent = 0.0` and `spent = 0.0` inside `__init__` differ because ___________________________ .
5. The guard stops the run one call late because ___________________________ .
6. One sentence: a stand-in showed me ________________ but not ________________ .

---

## ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact. Where you carried fewer decimals, anything within `0.1` of a percentage is fine. These answers are for the pages in **this workbook**. Everything measured against the stand-in is a script's, not a model's.

### Warm-Up

**W1.** `14 / 32 = 0.4375`, which prints as **43.8%**. **W2.** **two fields above a rock** (16 fields against 14). **W3.** `0.0004 + 0.0003 =` **$0.0007**. **W4.** **after**: the cost is known only once the call has happened. **W5.** It lets `.` match a line break too, so `\{.*\}` can run across several lines.

### Page 23.1

**A.** Your own labels, so your counts are yours. Fields people most often disagree on: `urgency`. Two cases where a reasonable person differs from the gold are t3 and t8. (Other disagreements, for example t4's urgency, depend on you.) The total is out of `8 x 4 = 32`.

**B.** The fingerprint is **`0f25042fb4`**. If yours differs, you changed a letter of a label or a message when you typed `TESTS`.

**C.** `before == after` is **False**; `before == restored` is **True**. Printed:

```text
before  : 1905113039
after   : 2d3cbf131c
restored: 1905113039
before == after    ? False
before == restored ? True
```

A fingerprint tells you whether the set is the **same as when it was frozen**, not whether somebody touched it: an edit that was later undone leaves no trace. That is fine; the set is then the frozen set again.

**D.** Last line: `AssertionError: the test set changed since it was frozen`, raised by **`check_frozen`** (called from `run_suite`). The honest way to change a gold label: (1) write the rule first (for example "a double charge is always urgent, 3"); (2) write the change and the date in `log.txt`; (3) change the gold and make a **new** frozen set with a **new** fingerprint; (4) rerun **every** version, because the old scores were against the old set.

### Page 23.2

**A.** `category`: billing 2, shipping 2, technical 1, account 2, other 1 (three-way tie at **2**). `urgency`: 1 is 2, 2 is 3, 3 is 3 (tie at **3**, between `2` and `3`). `order_id`: `None` 4. `refund_requested`: True 3, False 5 (best **False**, 5). Total: **2 + 3 + 4 + 5 = 14** out of `8 x 4 =` **32**. `14 / 32 =` **43.8%** (0.4375). Ties: `category` and `urgency`. Constants at the top: `3 x 2 =` **6**.

**B.** `constants tried: 30`, best `43.8%`, worst `31.2%`. `s1.py` prints:

```text
 43.8% billing 2 False
 43.8% billing 3 False
 43.8% shipping 2 False
 43.8% shipping 3 False
 43.8% account 2 False
 43.8% account 3 False
 40.6% billing 1 False
 40.6% shipping 1 False
```

**Six** rows show the top score, matching `3 x 2`.

**C.** `0.50 x 32 =` **16** fields. The rock: **14**. Above the rock: **2** fields (about **6.2** percentage points). "`50%` is not 'half right'. It means **it is two fields above a rock that ignores the message**."

**D.** The gold is unevenly spread: `None` is right for `order_id` in half of the cases and `False` is right for `refund_requested` in five of eight, so a constant gets those for free.

**E.** `urgency`: **2**, 3 of 6 · `order_id`: **None**, 4 of 6 · `refund_requested`: **False**, 4 of 6. `3 + 4 + 4 =` **11** of `6 x 3 =` **18**, so **61.1%** (0.6111). Constants: `3 x 2 =` **6** (only one of them, `urgency` 2 with `False`, reaches the top). `p2.py` prints:

```text
urgency {1: 2, 2: 3, 3: 1}
order_id {None: 4, 'K-1': 1, 'K-2': 1}
refund_requested {True: 2, False: 4}
```

### Page 23.3

**A.** v1: `0.55 x 30 = 16.5`, so about **16 or 17** fields, about **51.6%** (`16.5 / 32`); it actually got 16 (`50.0%`). v3: `0.99 x 30 = 29.7`, so about **30** fields, `30 / 32 =` **93.8%**. v3 should cost more (the prompt has the rules and three examples, so there are far more tokens in).

**B.** (Stand-in, seed 0, cache off.)

| Version | Field score | Exact | Parse-fail | Tokens in | Tokens out | Cost |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| v1-zero-shot | `50.0%` | `0/8` | `0` | `310` | `168` | `$0.0011` |
| v2-rules | `68.8%` | `2/8` | `0` | `1566` | `88` | `$0.0020` |
| v3-few-shot | `93.8%` | `6/8` | `0` | `2262` | `88` | `$0.0027` |

| Version | `category` | `urgency` | `order_id` | `refund_requested` |
|---|:--:|:--:|:--:|:--:|
| v1 | 6 | 3 | 4 | 3 |
| v2 | 6 | 5 | 7 | 4 |
| v3 | 8 | 6 | 8 | 8 |

Totals, if you want them: `4138` tokens in, `344` out, `$0.0059`.

**C.** 1. v1 is `16 - 14 =` **2** fields above the rock. 2. The bottleneck in v3 is **`urgency`** (6 of 8). 3. The best any version got is **93.8%**, and `30 / 32 = 0.9375 =` **93.8%**. It matches: 30 of the 32 fields are the most any version can reach.

**D.** `s2.py` prints:

```text
t3 urgency | stand-in said: 3 | gold says: 2
t8 urgency | stand-in said: 3 | gold says: 2
```

The right answer is **neither: the specification does not decide it** (a double charge, politely put; a locked-out user for two days). When every version fails the same case, suspect **the test** first. It is a specification bug, not a prompt bug.

**E.** v3: `2262 x 1.00 / 1,000,000 = 0.002262`; `88 x 5.00 / 1,000,000 = 0.00044`; sum `0.002702` which rounds to **$0.0027**. v2: `0.001566 + 0.00044 = 0.002006` so **$0.0020**. v1: `0.00031 + 0.00084 = 0.00115`, which is exactly on a rounding line: the program prints **$0.0011**, and a calculator that rounds half up writes `0.0012`. Either is fine if you wrote the full sum. `cost(v3) / cost(v1)` = `0.0027 / 0.0011 =` about **2.5**.

### Page 23.4

**A.** Field score, percent (stand-in, seeds 0 to 5):

| Prompt | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | Mean | Min | Max |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| v1 | 50.0 | 43.8 | 46.9 | 59.4 | 40.6 | 31.2 | **45.3** | 31.2 | 59.4 |
| v2 | 68.8 | 87.5 | 71.9 | 68.8 | 81.2 | 75.0 | **75.5** | 68.8 | 87.5 |
| v3 | 93.8 | 93.8 | 93.8 | 93.8 | 93.8 | 93.8 | **93.8** | 93.8 | 93.8 |

(Means: `(50.0+43.8+46.9+59.4+40.6+31.2)/6 = 271.9/6 = 45.3`; v2 `453.2/6 = 75.5`; v3 `93.8`.)

**B.** 1. **Two** seeds below (`40.6` and `31.2`); **one** exactly on it (`43.8`, seed 1). 2. **Not reliably**; its range `31.2` to `59.4` straddles `43.8`. 3. Lowest v2 `68.8`, highest v1 `59.4`: the gap is bigger than the range, so **yes**, v2 is better than v1 on these six seeds. 4. It has a little noise too (about a 1 in 4 chance of at least one wrong field in a run), but none happened in six.

**C.** A: mean `56.0`, min `48.0`, max `66.0`. B: mean `73.0`, min `69.0`, max `79.0`. B is better: B's lowest (`69.0`) is above A's highest (`66.0`), so the gap is bigger than the spread of either. Seed 0 alone (`61.0` vs `72.0`) would have hidden that A ranged from `48.0` to `66.0`, that is, how big the spread is.

**D.** Old: p1 `1 1 0 0` (2), p2 (4), p3 `0 1 1 0` (2), so `2 + 4 + 2 = 8` of 12 = **66.7%**. New: p1 is `1 0 1 1` (3), p2 is 4, p3 is `1 0 1 1` (3), so `3 + 4 + 3 = 10` of 12 = **83.3%**. The score went **up**. Lost: p1 `urgency` (was 1, now 0) and p3 `urgency` (was 1, now 0). (Gains at p1 `order_id`, p1 `refund`, p3 `category`, p3 `refund`, p3 `order_id` are not regressions.) `p3.py` prints:

```text
A: mean 56.0  min 48.0  max 66.0
B: mean 73.0  min 69.0  max 79.0
old field score: 66.7%
new field score: 83.3%
lost: [('p1', 'urgency'), ('p3', 'urgency')]
```

**E.** The second line: `v2, model seed 0 -> seed 1: now 87.5%, lost [('t1', 'category'), ('t5', 'order_id')]`. Lost: **t1.category** and **t5.order_id**. The score alone said "better" (68.8% to 87.5%); the report counts what used to be right.

### Page 23.5

**A.** 1. Spent after each call: `0.0014, 0.0028, 0.0042, 0.0056, 0.0070, 0.0084, 0.0098, 0.0112`. After 7 it is `0.0098`, still **under** `0.01`; the alarm goes off on call **8**, spent **$0.0112**, over by **$0.0012**. (`guard.py` prints `stopped at call 8: spent $0.0112 over 8 calls, limit $0.0100`.) 2. **$0.0007**. `0.01 / 0.0007 = 14.29`, so after **14** calls it is `$0.0098`, still under; call **15** crosses (`$0.0105`). 3. The cost is known only **after** the call; `record` runs after the call has happened and been paid for.

**B.** Predicted spent: `0.0040, 0.0100, 0.0150, 0.0220` (call 5 not reached). Stops at call **4**, spent **$0.0220**. Printed:

```text
after call 1: spent $0.0040
after call 2: spent $0.0100
after call 3: spent $0.0150
stopped at call 4: spent $0.0220 over 4 calls, limit $0.0200
4 calls, $0.0220 spent, $-0.0020 of $0.0200 left
```

Call 5 was **never made**: `break` ends the loop as soon as the alarm is caught. Call 4 was made and paid for.

**C.** `STOPPED: spent $0.0042 over 19 calls, limit $0.0040` and `the stand-in's own meter says $0.0042 over 19 calls`. Overspend: `$0.0002` (exactly `$0.00017`), which is **part of** the cost of **call 19**, the one that crossed (that call cost `$0.000334`; `$0.0038` had been spent before it). **Both, they count the same 19 calls.**

**D.** `class BudgetExceeded(Exception): pass` makes a **new kind of error with your own name** (`pass` means nothing more inside). `raise BudgetExceeded("...")` **throws** one, with a message. `except BudgetExceeded as e:` catches **only that kind** and puts the message in `e`. `except Exception:` catches **every** kind of error, including your own alarm, so the loop carries on past a budget that is already blown (Bug 23.7-A).

**E.** `calls made so far: 0` and `pre-flight ceiling for 24 calls: $0.0161`. It is higher than the real `$0.0059` because it assumes 100 output tokens per call and the stand-in's replies are 11 tokens (v2, v3) to 21 (v1).

### Page 23.6

Full marks: your own numbers with seeds (fingerprint `0f25042fb4`, floor `43.8%`, v1 `50.0%` and v3 `93.8%` at seed 0, ceiling `93.8%`, guard trip call `19` on the whole run with limit `$0.004`). "A score only means something against **the floor (the rock)** and against **the spread (the noise)**." One honest sentence about the stand-in (for example "The stand-in is not a model, so I cannot say whether examples help a real one"). Constructs: `@dataclass` makes a labelled record and writes `__init__` for you; a class with `__init__` makes an object that **remembers** (`self` is the object being built, `self.spent` is something this object remembers); `try`/`except` with your own class catches only that kind, and `except Exception` would also catch your alarm; `re.S` lets `.` cross line breaks. Deduct for any number your own run did not print, and for "model" where "stand-in" is meant. `constructs.py` prints:

```text
(a) Point(x=3.0, y=4.0) | p.x = 3.0 | equal to a twin? True
(b) c.n = 16 | a second, separate object: 0
(c) 3 is fine
(c) caught TooBig: 9 is over the limit 5
(d) without re.S: None
(d) with re.S   : '{\n  "urgency": 2,\n  "order_id": null\n}'
```

### Page 23.7

**A. (SILENT)** (i) `except Exception:` catches `BudgetExceeded`, so the loop never stops; the alarm fires on every call from the 8th and is thrown away. (ii)

```text
calls that finished: 7
12 calls, $0.0168 spent, $-0.0068 of $0.0100 left
```

Seven calls finished, but 12 were made and paid for: `$0.0168` against a `$0.01` limit. (iii) Catch only what you expect (`except json.JSONDecodeError:` or your own specific class), or move the `try` so that `BudgetExceeded` is not inside it and goes up to a place that stops the loop. Check: compare `done` with `guard.calls`; they should be equal.

**B. (SILENT)** (i) The reply is valid JSON but `urgency` is the text `"3"`, and `"3" == 3` is `False` in Python, so the box scores `0`. (ii)

```text
parsed: True
gold  : {'category': 'billing', 'urgency': 3, 'order_id': 'C-77', 'refund_requested': True}
score : 0.75
per   : {'category': 1, 'urgency': 0, 'order_id': 1, 'refund_requested': 1}
```

(iii) Not the gold. Either say in the prompt that `urgency` is an **integer** (your `RULES` already do), or convert the parsed value (`int(pred["urgency"])`) in a step you add and freeze. The check that catches it: print `per` for a reply that looks right, and print `type(pred["urgency"])`.

**C. (LOUD)** (i) `def record(cost):` has no `self`, so Python passes the object as the first argument and `cost` receives it. The real fault is the `def` line. (ii) The last line:

```text
TypeError: BudgetGuard.record() takes 1 positional argument but 2 were given
```

(The exact wording can differ a little between Python versions.) (iii) `def record(self, cost):`.

**Catching A and B without a table:** A: print `done` next to `guard.calls` (or `guard.summary()`), and check that `spent` is not over `limit` at the end. B: print `per` (the per-field 0/1) for one reply you can see is right, and print the `type(...)` of the field that scored `0`.

### Page 23.8 and Self-Check

**Bug Log Entry 2** should name: `p = 0.99` for v3 (the ordering was built in by the stand-in's one line) and v1's spread `31.2` to `59.4` over six seeds (two seeds below the floor); plus an honest sentence. **Self-Check:** 1. a constant answer that ignores the message; `14`; `43.8`. 2. **before**, because otherwise you fit the test to the prompt (the same way last week's judge learned the pairs we wrote). 3. `None`; the whole `{ ... }` block. 4. `self.spent` is stored **on the object** and survives after `__init__` ends; a plain `spent` is a local name that vanishes when `__init__` finishes. 5. the cost is known only after the call, and `record` runs after it. 6. Any honest sentence; the usual answer: the stand-in showed me how the harness works (floor, spread, ceiling, guard) but not how a real model behaves.
