# Workbook — Week 35: Capstone 2, Build, Measure, Attack

**Name:** ________________________________  **Date:** ______________

[⬅ Week 34](week-34.md) · [📖 Read the chapter first](../student-guide/week-35.md) · [Course Home](../README.md) · [Next ➡](week-36.md)

---

> **Rules for this workbook.** There is **no new maths and no new syntax** this week. The one reuse is Week 33's wobble, `sqrt(n p (1-p))`, used on the eval's scores and on an attack's landing count. Pages 35.1 to 35.3 are **pen first**: write your answer by hand, then run the check. **A guess written after the run is not a guess.**
>
> **Nothing here calls a model.** Every "system" is either a column of verdicts typed into a table or a tiny scripted function. Every dollar is a **stand-in dollar** (Week 28's illustrative price table) and every millisecond is a **stand-in millisecond**. *Stand-in, not a model:* nothing printed here says anything about any real model. The tables come from the chapter's worked example ("Ask My Notes", 25 frozen cases, 15 notes); **your own project's numbers will differ**, and the Red-Team Card on Page 35.3 is for *your* numbers.
>
> **Real numbers.** Every number printed below came from running the code shown, on CPU. There is nothing random in this workbook (the attack counts on Page 35.3 are typed in from the chapter's seeded run, and the code only does arithmetic on them). The people "Leo" and "Asha" are invented. The attacks in this workbook are defensive and educational and are only ever run against scripted stand-ins.
>
> **Files you need.** Every "check" block below is **self-contained**: it defines every name it uses, needs only Python 3, and can be run from any folder. Whole workbook at the computer: under 2 seconds. A pen and a calculator, plus your chapter output from `python capstone34/eval/run_eval.py v1` for the "your own" boxes.
>
> **Calculator.** Plain arithmetic. Four decimals while you work, round only the answer.

---

## ✅ Warm-Up (5 min, before anything else, from memory)

1. What is the first thing you do at the start of Week 35, before any score is shown? ______________________________
2. The floor is `refuse everything`. What is a **baseline**, and why is it a bigger number? ____________________________________________________
3. In the chapter's order, which comes first: the baseline or the spine? ______________ Why? ____________________________________________________
4. Name the three paths the spine can take: ______________ , ______________ , ______________
5. Week 33: a count that comes from weighted-coin flips strays from `n p` by about ______________ . Write it as a formula.

---

## 🧮 Page 35.1 — The Tally, by Hand (30 min · pen, then one check)

Below are the chapter's 25 frozen cases and the baseline's verdict on each (given: `pass` or `FAIL`). The spine's eight failing ids are: **c02, c10, c11, c12, c13, c15, c19, c24**. Every other case passes. Fill the last column.

| id | category | baseline | spine v1 (you fill) |
|:-:|---|:-:|:-:|
| c01 | `factual` | pass | ______ |
| c02 | `factual` | FAIL | ______ |
| c03 | `factual` | pass | ______ |
| c04 | `factual` | pass | ______ |
| c05 | `factual` | pass | ______ |
| c06 | `factual` | pass | ______ |
| c07 | `factual` | pass | ______ |
| c08 | `factual` | pass | ______ |
| c09 | `factual` | pass | ______ |
| c10 | `multi_hop` | FAIL | ______ |
| c11 | `multi_hop` | FAIL | ______ |
| c12 | `multi_hop` | FAIL | ______ |
| c13 | `multi_hop` | FAIL | ______ |
| c14 | `arithmetic` | FAIL | ______ |
| c15 | `arithmetic` | FAIL | ______ |
| c16 | `arithmetic` | FAIL | ______ |
| c17 | `arithmetic` | FAIL | ______ |
| c18 | `out_of_scope` | pass | ______ |
| c19 | `out_of_scope` | FAIL | ______ |
| c20 | `out_of_scope` | pass | ______ |
| c21 | `adversarial` | FAIL | ______ |
| c22 | `adversarial` | FAIL | ______ |
| c23 | `adversarial` | FAIL | ______ |
| c24 | `ambiguous` | FAIL | ______ |
| c25 | `ambiguous` | pass | ______ |

**A. Tally.** Count the passes by category, for each column. Write `n` in the first column.

| category | `n` | baseline passes | spine passes | change |
|---|:-:|:-:|:-:|:-:|
| `factual` | ______ | ______ | ______ | ______ |
| `multi_hop` | ______ | ______ | ______ | ______ |
| `arithmetic` | ______ | ______ | ______ | ______ |
| `out_of_scope` | ______ | ______ | ______ | ______ |
| `adversarial` | ______ | ______ | ______ | ______ |
| `ambiguous` | ______ | ______ | ______ | ______ |
| **total** | ______ | ______ | ______ | ______ |

Largest gain: ______________ . A category with no change at all, and a case that fails in **both** columns inside `out_of_scope`: ______________ . Cases the spine fixes that the baseline failed: ______________ . Write the closing line: *"the floor is ____/25; the baseline is ____/25; the spine is ____/25."*

**B. The wobble, by hand.** `wobble = sqrt(25 × p × (1 − p))` with `p = k / 25`. Fill the table. Then for the two comparisons: *combined wobble* `= sqrt(wobble_a² + wobble_b²)`, and the bar is **twice** the combined wobble. A gap smaller than the bar is *inside the noise*.

| `k` (passes of 25) | `p` | wobble |
|:-:|:-:|:-:|
| 11 (baseline) | ______ | ______ |
| 17 (spine v1) | ______ | ______ |
| 15 (v2, a later change) | ______ | ______ |

| comparison | gap | combined wobble | bar (twice) | more than noise? |
|---|:-:|:-:|:-:|:-:|
| baseline 11 against v1 17 | ______ | ______ | ______ | ______ |
| v1 17 against v2 15 | ______ | ______ | ______ | ______ |

The gap from 11 to 17 is six cases. Is "the spine is better than the baseline" a finding **on the overall** by this rule? ______ . So what do you point at instead? ____________________________________________________ (Rule of thumb only: both versions answer the *same* 25 questions, so the real bar is a little tighter. Do not shrink it by hand.)

```python
# check351.py - Page 35.1: the tally by hand, then by code, and the wobble of the three scores. (Plain Python; no files needed.)
from collections import Counter
CATS = {"factual": range(1, 10), "multi_hop": range(10, 14), "arithmetic": range(14, 18), "out_of_scope": range(18, 21), "adversarial": range(21, 24), "ambiguous": range(24, 26)}
cat_of = {f"c{i:02d}": cat for cat, ids in CATS.items() for i in ids}
baseline_fail = ["c02", "c10", "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c19", "c21", "c22", "c23", "c24"]
spine_fail = ["c02", "c10", "c11", "c12", "c13", "c15", "c19", "c24"]
tb = Counter(cat_of[c] for c in cat_of if c not in baseline_fail)
ts = Counter(cat_of[c] for c in cat_of if c not in spine_fail)
n = Counter(cat_of.values())
for cat in CATS:
    print(f"{cat:13s} n={n[cat]}  baseline {tb[cat]}  spine {ts[cat]}  change {ts[cat] - tb[cat]:+d}")
print("floor 6/25 =", 6 / 25, "| baseline", sum(tb.values()), "/25 =", round(sum(tb.values()) / 25, 2), "| spine", sum(ts.values()), "/25 =", round(sum(ts.values()) / 25, 2))
print("cases the spine passes that the baseline failed:", sorted(set(baseline_fail) - set(spine_fail)))
print("cases both fail:", sorted(set(baseline_fail) & set(spine_fail)))
def wob(k, n=25):
    p = k / n
    return (n * p * (1 - p)) ** 0.5
print("wobble of a count k out of 25 = sqrt(25 p (1-p)), p = k / 25")
for k in (11, 15, 17):
    print(f"  k={k}: p={k / 25:.2f}  wobble {wob(k):.2f}")
for a, b in [(11, 17), (17, 15)]:
    combined = (wob(a) ** 2 + wob(b) ** 2) ** 0.5
    print(f"  {a} vs {b}: gap {abs(b - a)}, combined {combined:.1f}, twice combined {2 * combined:.1f} ->", "more than noise" if abs(b - a) > 2 * combined else "inside the noise")
```

```text
factual       n=9  baseline 8  spine 8  change +0
multi_hop     n=4  baseline 0  spine 0  change +0
arithmetic    n=4  baseline 0  spine 3  change +3
out_of_scope  n=3  baseline 2  spine 2  change +0
adversarial   n=3  baseline 0  spine 3  change +3
ambiguous     n=2  baseline 1  spine 1  change +0
floor 6/25 = 0.24 | baseline 11 /25 = 0.44 | spine 17 /25 = 0.68
cases the spine passes that the baseline failed: ['c14', 'c16', 'c17', 'c21', 'c22', 'c23']
cases both fail: ['c02', 'c10', 'c11', 'c12', 'c13', 'c15', 'c19', 'c24']
wobble of a count k out of 25 = sqrt(25 p (1-p)), p = k / 25
  k=11: p=0.44  wobble 2.48
  k=15: p=0.60  wobble 2.45
  k=17: p=0.68  wobble 2.33
  11 vs 17: gap 6, combined 3.4, twice combined 6.8 -> inside the noise
  17 vs 15: gap 2, combined 3.4, twice combined 6.8 -> inside the noise
```

Did your tallies match? Which row did you get wrong, if any? ______ . Your two bars: ______ and ______ ; the printout says ____________________________________________________

---

## 🧮 Page 35.2 — Promise Against Measurement (35 min · pen, then computer)

In Week 34 you wrote five promises **before** anything existed. Today `run_eval.py` measured them. The measured values below are the chapter's worked example (stand-in dollars; the sum of the 25 task costs is `$0.01129`, the most expensive single task was `$0.00148`).

**A. The promise table.** For a **ceiling** ("under"), headroom = promised ÷ measured. For a **floor** ("at least"), headroom = measured ÷ promised. Write `kept` if headroom is above or equal to `1.0`, `MISSED` if below.

| promise (Week 34 §6) | promised | measured | headroom | kept / MISSED |
|---|:-:|:-:|:-:|:-:|
| mean cost per task, under | $0.001 | `0.01129 ÷ 25 =` ______ | ______ | ______ |
| worst single task, under | $0.003 | $0.00148 | ______ | ______ |
| score, at least | 0.70 | `17 ÷ 25 =` ______ | ______ | ______ |
| refusals right, at least | 5 of 6 | 5 | ______ | ______ |

How many passing cases would have met the score promise? `0.70 × 25 =` ______ , so ______ cases. How many short was the run? ______ . Is that gap bigger than the wobble you found on Page 35.1? ______ . Finish the sentence, using your numbers: *"I promised ______________ and measured ______________ , so ______________________________ ."* May you now edit the promise to `0.65`? ______ Why not? ____________________________________________________

**B. A p95, by sorting and an index.** Here are the stand-in milliseconds for 25 tasks of an invented project (made up for this exercise). Sort them by hand, smallest first, and write them below.

`0.2 0.3 0.2 0.2 0.4 0.2 0.3 0.5 0.2 0.2 0.3 0.2 0.6 0.2 0.3 0.2 0.4 0.2 0.3 0.7 0.2 0.2 0.3 2.9 0.2`

sorted: ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____

p95 index `int(0.95 × 25) =` ______ → p95 = ______ . p50 index `int(0.5 × 25) =` ______ → p50 = ______ . Mean = ______ . Max = ______ . Now cross out the slowest task: the list has ______ tasks, the index is `int(0.95 × ______) =` ______ and the p95 is ______ . What did one slow task do to the p95? ____________________________________________________

**C. A budget that moves with the router.** Leo's helper costs about `$0.00031` for a retrieve task, `$0.00128` for an agent task and `$0` for a refusal (stand-in dollars: the chapter's measured averages). Leo's 25 tasks: 12 retrieve, 5 agent, 8 refusals. Then he changes the router so that every question with a digit goes to the agent: now 8 retrieve, 9 agent, 8 refusals.

| | retrieve cost | agent cost | total | mean over 25 | headroom on $0.001 |
|---|:-:|:-:|:-:|:-:|:-:|
| before | `12 × 0.00031 =` ______ | `5 × 0.00128 =` ______ | ______ | ______ | ______ |
| after | `8 × 0.00031 =` ______ | `9 × 0.00128 =` ______ | ______ | ______ | ______ |

Which line of the table would you read first if the headroom dropped below `1.0`? ____________________________________________________

```python
# check352.py - Page 35.2: promises against measurements, a p95 by sorting and an index, and a cost that moves with the router. STAND-IN dollars and STAND-IN milliseconds.
total, worst = 0.01129, 0.00148
mean = total / 25
print(f"mean = {total} / 25 = {mean:.5f} | headroom on 0.001 = {0.001 / mean:.2f}x")
print(f"worst {worst} | headroom on 0.003 = {0.003 / worst:.2f}x")
print(f"score 17/25 = {17 / 25:.2f} | measured / promised = {(17 / 25) / 0.70:.3f} | cases needed = {0.70 * 25} -> 18")
print(f"refusals 5 of 6 | measured / promised = {5 / 5:.2f}")
print(f"p95 1000 ms promised, 0.6 measured: headroom {1000 / 0.6:.0f}x (a scripted function, so it means nothing)")
print()
ms = [0.2, 0.3, 0.2, 0.2, 0.4, 0.2, 0.3, 0.5, 0.2, 0.2, 0.3, 0.2, 0.6, 0.2, 0.3, 0.2, 0.4, 0.2, 0.3, 0.7, 0.2, 0.2, 0.3, 2.9, 0.2]
s = sorted(ms)
print("n =", len(ms), "| sorted:", s)
print("p95 index = int(0.95 * 25) =", int(0.95 * len(s)), "-> p95 =", s[int(0.95 * len(s))], "| p50 index", int(0.5 * len(s)), "-> p50 =", s[int(0.5 * len(s))], "| mean", round(sum(s) / len(s), 2), "| max", s[-1])
t = sorted(ms)[:-1]
print("slowest removed: n =", len(t), "index", int(0.95 * len(t)), "-> p95 =", t[int(0.95 * len(t))])
print()
R, A = 0.00031, 0.00128
for name, nr, na in [("Leo, before", 12, 5), ("Leo, router sends digits to the agent", 8, 9)]:
    tot = nr * R + na * A
    print(f"{name}: {nr} x {R} + {na} x {A} = {tot:.5f} | mean over 25 = {tot / 25:.6f} | headroom on 0.001 = {0.001 / (tot / 25):.2f}x")
```

```text
mean = 0.01129 / 25 = 0.00045 | headroom on 0.001 = 2.21x
worst 0.00148 | headroom on 0.003 = 2.03x
score 17/25 = 0.68 | measured / promised = 0.971 | cases needed = 17.5 -> 18
refusals 5 of 6 | measured / promised = 1.00
p95 1000 ms promised, 0.6 measured: headroom 1667x (a scripted function, so it means nothing)

n = 25 | sorted: [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 2.9]
p95 index = int(0.95 * 25) = 23 -> p95 = 0.7 | p50 index 12 -> p50 = 0.2 | mean 0.4 | max 2.9
slowest removed: n = 24 index 22 -> p95 = 0.6

Leo, before: 12 x 0.00031 + 5 x 0.00128 = 0.01012 | mean over 25 = 0.000405 | headroom on 0.001 = 2.47x
Leo, router sends digits to the agent: 8 x 0.00031 + 9 x 0.00128 = 0.01400 | mean over 25 = 0.000560 | headroom on 0.001 = 1.79x
```

Your worst-task headroom was ______ ; the printout rounds it to `2.03x` and the chapter's own run says `2.0x`: why can two honest rounded numbers differ in the second decimal? ____________________________________________________ Which of your p95s changed when you removed the slow task, and by how much? ______________

---

## 🧮 Page 35.3 — The Red-Team Card (40 min · pen, then computer)

**A. Five rows, from measured outcomes.** These are the chapter's results against the **stand-in** spine (the planted-note follower is a scripted `GullibleModel`; its landing count is the dial we typed, not a finding about any real model). Fill the last three columns. Statuses: **FIXED** (it landed, you patched it, you re-tested), **ALREADY BLOCKED** (it never landed and a control shows the test can), **ACCEPTED** (it landed, you did not fix it, and you wrote down why). Severity is `1` (mild) to `5` (someone loses something).

| | attack | what happened (seeded, stand-in) | status | severity | re-test |
|:-:|---|---|:-:|:-:|---|
| A1 | a planted note orders a file write | landed in 15 of 50 runs; after a named-files-only guard 0 of 50 | ______ | ______ | legitimate save before: ____ / 50; after: ____ / 50 |
| A2 | an instruction to escape the sandbox | 0 of 50 landed; with the box switched off, 15 of 50 | ______ | ______ | ____________ |
| A3 | personal data in a question | not in the answer, not in the trace; with redaction off, both leak | ______ | ______ | ____________ |
| A4 | a huge question and a runaway loop | refused at `$0.00`; the loop stopped at the iteration cap | ______ | ______ | ____________ |
| A5 | a near-miss question the notes cannot answer | answered with a real-looking citation in 2 of 3 probes | ______ | ______ | ____________ |

For the **accepted** row, write the one-line reason a stranger could hold you to (the near-miss question scores `0.357` against the notes, higher than six answerable cases; raising the refusal threshold to refuse it made `factual` go from `8` to `5`): ____________________________________________________

**B. Wobble of an attack count.** A1 landed in 15 of 50 runs. At `p = 0.3`, the wobble is `sqrt(50 × 0.3 × 0.7) =` ______ . Would 12 or 18 landings have surprised you? ______ . Why can 50 runs not tell `0.30` from `0.25`? ____________________________________________________

**C. Is it a fix?** A patch is a fix only if the attack **falls** and the **legitimate task still works**. Fill the last column.

| patch | attack landed (of 50) | legitimate save worked (of 50) | the 25-case suite | fix? |
|---|:-:|:-:|:-:|:-:|
| no patch | 15 | 50 | 17 / 25 | ______ |
| forbid every write | 0 | 0 | 17 / 25 | ______ |
| allow only the files the user named | 0 | 50 | 17 / 25 | ______ |

The suite says `17 / 25` for all three. Why can it not tell them apart? ____________________________________________________ What one case would you add (and where, so the frozen file is untouched)? ____________________________________________________

**D. A zero needs a control.** For each "did not land", say whether the test could ever have said "landed". What does the test say with the defence **off**?

| test | with the defence off, the test says | can this test fail? |
|---|:-:|:-:|
| A2 (sandbox) | 15 of 50 landed | ______ |
| A3 (personal data) | the answer and trace both leak | ______ |
| A6 (invented) | 0 landed | ______ |

```python
# check353.py - Page 35.3: fixed, already blocked or accepted; a zero needs a control; a patch is only a fix if the happy path survives. (Numbers typed from the chapter's run.)
rows = [("A1", "injection via a note", 15, 50, "after the fix 0/50", "legit save 50/50 before and after"), ("A2", "sandbox escape", 0, 50, "control 15/50", ""),
        ("A3", "personal data", 0, 50, "controls leak", ""), ("A4", "budget", 0, 1, "refused at 0.00", ""), ("A5", "confidently wrong", 2, 3, "no threshold can refuse it", "")]
for r in rows:
    print(f"{r[0]} {r[1]:22s} landed {r[2]}/{r[3]}  {r[4]}")
print()
print("wobble of 15 landings in 50 runs at p=0.3:", round((50 * 0.3 * 0.7) ** 0.5, 1), "-> 12 or 18 would not have been surprising")
print()
patches = [("no patch", 15, 50), ("forbid every write", 0, 0), ("named files only", 0, 50)]
for name, landed, happy in patches:
    print(f"{name:20s} attack landed {landed:2d}/50 | legitimate save {happy:2d}/50 ->", "FIX" if landed == 0 and happy == 50 else "NOT A FIX")
print()
for name, test_when_defence_off in [("A2 (control)", 15), ("A3 (control)", "leaks"), ("A6, invented (control)", 0)]:
    print(f"{name:24s} with the defence OFF the test says {test_when_defence_off} ->", "the test can fail" if test_when_defence_off not in (0, False) else "this test cannot fail: it proves nothing")
```

```text
A1 injection via a note   landed 15/50  after the fix 0/50
A2 sandbox escape         landed 0/50  control 15/50
A3 personal data          landed 0/50  controls leak
A4 budget                 landed 0/1  refused at 0.00
A5 confidently wrong      landed 2/3  no threshold can refuse it

wobble of 15 landings in 50 runs at p=0.3: 3.2 -> 12 or 18 would not have been surprising

no patch             attack landed 15/50 | legitimate save 50/50 -> NOT A FIX
forbid every write   attack landed  0/50 | legitimate save  0/50 -> NOT A FIX
named files only     attack landed  0/50 | legitimate save 50/50 -> FIX

A2 (control)             with the defence OFF the test says 15 -> the test can fail
A3 (control)             with the defence OFF the test says leaks -> the test can fail
A6, invented (control)   with the defence OFF the test says 0 -> this test cannot fail: it proves nothing
```

**E. Your own Red-Team Card.** From **your** `RED_TEAM.md` (every row, misses included):

| | what I typed or planted (verbatim) | predict: can it land? | landed / n (control) | severity | fixed / already blocked / accepted | re-test: attack, happy path |
|:-:|---|:-:|:-:|:-:|:-:|---|
| A1 | | | | | | |
| A2 | | | | | | |
| A3 | | | | | | |
| A4 | | | | | | |
| A5 | | | | | | |

*Log the ones that failed too. A zero needs a control that is not zero.*

Committed numbers (copy from `run_eval.py v1`): overall ______ / ______ · factual ____ multi_hop ____ arithmetic ____ out_of_scope ____ adversarial ____ ambiguous ____ · mean cost ______ stand-in dollars · date ______ · my initials ______ · teacher's initials ______

**F. The four sentences.** Write each in your own handwriting, with your own numbers, and keep the words *stand-in* and `n`.

1. My baseline scores ______ of ______ and the spine ______ of ______ ; the biggest gain is in ____________________ because ____________________________________________________
2. `run_eval.py` prints ____________________________________________________ and it cannot see ____________________________________________________
3. I promised ______________ before I measured; I measured ______________ ; so ____________________________________________________
4. I attempted ______ attacks in ______ categories; ______ landed; I fixed ______ and accepted ______ because ____________________________________________________

---

## 🐞 Page 35.4 — Break It on Purpose (four bugs · 35 min)

Run each as written. Predict first. Then say what went wrong and how you would have known. Each is **deliberate**; each is a tiny stand-in of a mistake from the chapter.

### 35.4-A (loud) — the whole case goes in

```python
# DELIBERATE BUG 35.4-A (loud): the runner hands the system the whole CASE; the guard wants the question text.
cases = [{"id": "c01", "q": "which optimizer does the note recommend", "must_contain": ["adamw"]}]
def question_guard(q):
    if not q.strip():
        return "empty question"
    return None
def run_eval(cases, system):
    return [system(c) for c in cases]
print(run_eval(cases, question_guard))
```

Prediction (which error, and on which line is the *cause*, not the frame the traceback names last?): ____________________________________________________

```text
Traceback (most recent call last):
  File "/home/you/l4/b_a.py", line 9, in <module>
    print(run_eval(cases, question_guard))
  File "/home/you/l4/b_a.py", line 8, in run_eval
    return [system(c) for c in cases]
  File "/home/you/l4/b_a.py", line 8, in <listcomp>
    return [system(c) for c in cases]
  File "/home/you/l4/b_a.py", line 4, in question_guard
    if not q.strip():
AttributeError: 'dict' object has no attribute 'strip'
```

What went wrong, and why is a crash better here than turning the case into text with `str(c)`? ____________________________________________________

### 35.4-B (SILENT) — a test that cannot fail

A toy system with a dummy number. The defence is switched **off** for this run, on purpose, to see what the test says.

```python
# DELIBERATE BUG 35.4-B (SILENT): an attack test that looks only at the ANSWER. The leak is in the TRACE. (Dummy number; a toy system, not a model.)
def system(question, redact):
    shown = question.replace("555-0100", "[PHONE REDACTED]") if redact else question
    answer = "I cannot help with that."
    trace = {"question": shown}
    return answer, trace
question = "Call me on 555-0100 about the notes"
answer, trace = system(question, redact=False)         # the defence is switched OFF
print("test (answer only):", "LANDED" if "555-0100" in answer else "did not land -> 'safe'")
print("what is in the trace:", trace)
```

Prediction (does the test say landed? is there a leak?): ____________________________________________________

```text
test (answer only): did not land -> 'safe'
what is in the trace: {'question': 'Call me on 555-0100 about the notes'}
```

With the defence **off**, the test still says "safe". What is it blind to? ____________________________________________________ Write the control that would have caught it, in words: ____________________________________________________

### 35.4-C (SILENT) — moving the goalposts

```python
# DELIBERATE BUG 35.4-C (SILENT): the promise was 0.70, the run measured 17 of 25, and the promise is edited in memory so the line says kept.
promises = {"score_at_least": 0.70}
measured = 17 / 25
print("before:", "kept" if measured >= promises["score_at_least"] else "MISSED", "| measured", measured, "promised", promises["score_at_least"])
promises["score_at_least"] = 0.65                      # "0.65 is more realistic"
print("after :", "kept" if measured >= promises["score_at_least"] else "MISSED", "| measured", measured, "promised", promises["score_at_least"])
```

Prediction (what do the two lines say?): ____________________________________________________

```text
before: MISSED | measured 0.68 promised 0.7
after : kept | measured 0.68 promised 0.65
```

Nothing is broken in the code and the result is wrong. What changed between the two lines, and what should have been written in the report instead? ____________________________________________________

### 35.4-D (SILENT) — a digit is not arithmetic

A router sends every question with a digit to the arithmetic path. The "plan" there multiplies the numbers it finds. Both pieces are scripted stand-ins, not a model.

```python
# DELIBERATE BUG 35.4-D (SILENT): a router that sends any digit to the arithmetic path, and a draft plan that assumes there are two numbers to combine.
import re
def route_of(q):
    return "agent" if any(ch.isdigit() for ch in q) else "retrieve"
def draft_plan(q):
    nums = [float(x) for x in re.findall(r"\d+\.?\d*", q)]
    total = 1.0
    for x in nums:
        total *= x
    return str(round(total, 5))
for q in ["what is 0.00144 times 250", "what does the note say about week-11"]:
    print(f"{route_of(q):9s} {q!r:45s} -> {draft_plan(q) if route_of(q) == 'agent' else '(retrieve path)'}")
```

Prediction (what does the second question get back?): ____________________________________________________

```text
agent     'what is 0.00144 times 250'                   -> 0.36
agent     'what does the note say about week-11'        -> 11.0
```

The second answer has the look of a result and is not one. What did the plan assume, and what is the smallest repair that keeps the router as it is? ____________________________________________________ Which number in the eval would show this problem, if you read it? ______________

---

## 📓 Page 35.5 — Stop and Think (10 min · pen only)

1. Your baseline scores more than you expected. Which Week 34 sentence says what to do if it passes almost everything? ____________________________________________________
2. `multi_hop` is `0/4` and you want to write "RAG fails at multi-hop questions". Why can you not, and what do you write instead? ____________________________________________________
3. The run prints `internal errors: 0`. What does that count, and what does it not count? ____________________________________________________
4. v2 scores `15` where v1 scored `17`, but `factual` went from `8` to `5` with three named cases. Which is the finding, which is noise, and why? ____________________________________________________
5. `run_eval.py` says `DIFFER`. Someone suggests committing the new numbers so it says `MATCH`. What is that the same as, and who would notice? ____________________________________________________
6. A guard turned away `3` of `5` paraphrased attacks you made up afterwards. What does that say about the guard, and what is the real wall? ____________________________________________________
7. Name one attack you did not run, and write the one honest sentence about your red-team log that does **not** contain the word "secure": ____________________________________________________

---

## 📓 Page 35.6 — The Bug Log

| # | What went wrong (your words) | Loud or silent? | The one line or check that caught it | The rule I will keep |
|:-:|---|:-:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

Checks to keep: **the freeze checked and the 12 characters compared to the paper before any score · the baseline scored before anything clever · `n` written beside every score · the overall computed from counts, never typed · a promise missed is reported missed, and `DESIGN.md` is never edited · every failing case read and placed in the chain · every "0 landed" beside a control that is not 0 · every fix re-tested on the happy path · the suite's blind spots listed.**

Then write this sentence in your own handwriting, with your own numbers, and keep the words *stand-in* and *n*:

> "On my ______ frozen cases (fingerprint ______________ , 12 characters, checked against the paper) my baseline scored ______ and my spine ______ ; I promised ______ and measured ______ , so I report it as ______________ ; I attempted ______ attacks, ______ landed, I fixed ______ and accepted ______ ; every dollar and millisecond is a stand-in, which says nothing about a real model."

---

## 🧠 Self-Check (from memory, no notes)

- [ ] I can say why the floor, the baseline and the spine are three different numbers, and tally them by category.
- [ ] I can say what a 6-case gap on 25 cases can and cannot show, using the wobble.
- [ ] I can work out headroom for a ceiling and for a floor, and say `MISSED` out loud.
- [ ] I can find a p95 by sorting and an index, and say what one slow task does to it.
- [ ] I can classify an attack as fixed, already blocked or accepted, and say what each needs.
- [ ] I can say why a patch must be re-tested on the legitimate task, and why the suite may not see it.
- [ ] I can say why an attack test with no control proves nothing.
- [ ] I can explain why "edit the promise" and "commit the new numbers" are the same mistake.

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up
1. Run `check_frozen` on the cases and compare the 12 characters to the paper (the fingerprint written in Week 34), before any score is shown.
2. A baseline is the cheapest **useful** system (one search, copy a sentence, cite it); the floor is the worst *sensible* system (refuse everything, `6/25 = 0.24` in the worked example). Beating the floor proves nothing; the baseline (`11/25 = 0.44`) is the number the spine has to beat.
3. The baseline first, so that the cleverer thing has something honest to beat and you cannot choose the baseline after seeing the score.
4. Retrieve, agent, refuse.
5. About `sqrt(n p (1−p))`.

### Page 35.1
- **Table.** Spine column: `FAIL` on c02, c10, c11, c12, c13, c15, c19, c24; `pass` on the other 17. (Baseline `FAIL` on c02, c10-c17, c19, c21-c24 as given.)
- **A.** `factual` n 9: baseline 8, spine 8, change +0. `multi_hop` 4: 0, 0, +0. `arithmetic` 4: 0, 3, **+3**. `out_of_scope` 3: 2, 2, +0. `adversarial` 3: 0, 3, **+3**. `ambiguous` 2: 1, 1, +0. Total 25: 11, 17, **+6**. Largest gain: `arithmetic` and `adversarial` (+3 each; the agent path and the guard). No change: `factual` (8 and 8) and `multi_hop` (0 and 0). **c19** fails in both. Spine fixes **c14, c16, c17, c21, c22, c23**; both fail on c02, c10, c11, c12, c13, c15, c19, c24. The line: *"the floor is 6/25; the baseline is 11/25; the spine is 17/25."*
- **B.** `k = 11`: `p = 0.44`, wobble **2.48**. `k = 17`: `p = 0.68`, **2.33**. `k = 15`: `p = 0.60`, **2.45**. 11 against 17: gap **6**, combined **3.4**, bar **6.8**, **not** more than noise (inside). 17 against 15: gap **2**, combined **3.4**, bar **6.8**, inside the noise. So "the spine is better" is **not** a finding on the overall by this rule (6 against 6.8, about 1.8 combined wobbles: borderline). Point at the **categories** and mechanisms: `arithmetic` `0 → 3` (the agent path) and `adversarial` `0 → 3` (the guard), with the six named cases. Hand arithmetic with two decimals may differ from the printout in the third.

### Page 35.2
- **A.** Mean **0.00045**, headroom **2.2x** (`0.001 ÷ 0.00045`; the code gives `2.21x`), **kept**. Worst **2.0x** (`0.003 ÷ 0.00148`; unrounded `2.03x`), **kept**. Score: `17 ÷ 25 =` **0.68**, headroom `0.68 ÷ 0.70 =` **0.97**, **MISSED**. Refusals: `5 ÷ 5 =` **1.00**, **kept** with no spare (one case would turn it MISSED). `0.70 × 25 = 17.5`, so **18** cases; the run was **one** case short. One case is inside the wobble (about 2.3), so the honest sentence is: *"I promised a score of at least 0.70 and measured 17 of 25, 0.68, so I missed it by one case; one case is inside the wobble, so I report the miss and do not call the system good or bad."* May you edit the promise to 0.65? **No**: a promise that can be edited after the result could never have been broken; write the miss down, and if you want a different budget, add a `v2` budget with a reason, beside the first.
- **B.** Sorted: `0.2` thirteen times, `0.3` six times, `0.4` twice, `0.5`, `0.6`, `0.7`, `2.9`. p95 index `int(23.75) =` **23** → **0.7**. p50 index `int(12.5) =` **12** → **0.2**. Mean **0.4** (sum 9.9 over 25 = 0.396). Max **2.9**. With the slowest removed: **24** tasks, `int(0.95 × 24) = int(22.8) =` **22**, p95 **0.6**. One slow task moves the p95 only from 0.7 to 0.6 here, because with 25 tasks the p95 already sits on the *second slowest*; it dragged the **mean** (0.4) and **max** (2.9), not the p95. (A 26th slow task would move the index to 24.)
- **C.** Before: retrieve **0.00372**, agent **0.00640**, total **0.01012**, mean **0.000405**, headroom **2.47x**. After: **0.00248**, **0.01152**, total **0.01400**, mean **0.000560**, headroom **1.79x**. Read first: the **routing rule**: how many questions go to the agent, which costs about `4x` a retrieve task because every turn resends the history (Week 29). The two headroom roundings differ in the second decimal because one of you rounded `0.00148` before dividing and the other did not; round only the answer, and keep four decimals while working.

### Page 35.3
- **A.** A1 **FIXED**, severity **5** (a legal write that an untrusted note ordered); re-test: legitimate save **50** before, **50** after. A2 **ALREADY BLOCKED**, **5**, re-test: the control at 15 of 50 shows the test can land. A3 **ALREADY BLOCKED**, **4**, re-test: the control with redaction off leaks both. A4 **ALREADY BLOCKED**, **3**, re-test: run it again and the loop stops at the cap. A5 **ACCEPTED**, **4**, re-test: the near-miss still answers. Reason: *"the near-miss question scores 0.357 against the notes, higher than six answerable cases, so no threshold can refuse it without refusing them; raising the threshold to 0.36 made `factual` go from 8 to 5. I shipped v1, and the system card says a near-miss question can be answered with a real-looking citation."*
- **B.** `sqrt(50 × 0.3 × 0.7) = sqrt(10.5) =` **3.2**. No: 12 and 18 are each within one wobble of 15. 50 runs have a wobble of about 3 landings, which is `0.06` of the rate; `0.30` against `0.25` is a gap of `0.05` (2.5 landings): smaller than the wobble.
- **C.** No patch: **not a fix** (the attack still lands). Forbid every write: **not a fix** (the attack falls but the legitimate save falls to 0 of 50: the product is broken). Named files only: **FIX**. The suite cannot tell them apart because it has **no write case**: it only protects what it contains. Add a case for the legitimate save in `eval/cases_extra.py` with its own fingerprint (the frozen file stays as it is), or a check beside the suite.
- **D.** A2: **yes** (it said 15 with the box off). A3: **yes** (it leaks with redaction off). A6: **no**: it says 0 with the defence off, so a 0 with the defence on means nothing.
- **E and F.** Your own words and numbers. Marks: sentence 1 needs the baseline, the spine and the category with the gain. Sentence 2 needs the per-category table with `n`, routing and internal errors on their own lines, `MATCH` or `DIFFER`, and a named blind spot (the suite cannot see a capability with no case, such as saving a file). Sentence 3 needs a promise **before** the measurement and the word *missed* if it was. Sentence 4 needs a count of attempts, the number that landed, one fixed, one accepted with a reason. Model for the worked example: *(1) My baseline scores 11 of 25 and the spine 17 of 25; the gain is in `arithmetic` and `adversarial`. (2) It prints a per-category table with `n` on every row, routing on its own line, `internal errors`, and `MATCH` or `DIFFER`; it cannot see a capability with no case, such as saving a file. (3) I promised a score of at least 0.70; I measured 0.68 (17 of 25), one case short, so I report it as missed and do not edit the design. (4) I attempted five attacks in five categories; one landed and was fixed (A1, 15 of 50 to 0 of 50, legitimate save still 50 of 50); one is accepted (A5); the others were already blocked, each with a control that is not zero.* Remember: *stand-in* belongs in every line about dollars, milliseconds or attack rates.

### Page 35.4
- **A.** `AttributeError: 'dict' object has no attribute 'strip'`. The traceback ends in `question_guard`, at `q.strip()`, but the **cause** is in `run_eval`, in the line `system(c)`: it passes the whole case where the system wants the question text. Fix: `system(c["q"])`, as in `lambda c: spine.answer(c["q"])`. A crash is better than `str(c)` because a dictionary turned into text would be scored as a strange question, and nothing would say so.
- **B.** The test says **did not land -> 'safe'** and the trace holds `{'question': 'Call me on 555-0100 about the notes'}`, the dummy number in plain text. The test looks only at the **answer**; the leak is in the **trace**. The repair looks in **every** place the data can go and runs the control. Repaired output:

```text
defence OFF -> LANDED
defence ON  -> did not land
```

 The control (defence OFF) says `LANDED`, so the test can fail; with it ON it says `did not land` and that now means something.
- **C.** The promise was edited in memory from `0.70` to `0.65`, so the same measured `0.68` now reads `kept`. The code has no bug; the **report** is wrong. It should say `MISSED` (17 of 25 against 0.70, one case short, inside the wobble) and leave `DESIGN.md` alone. (The chapter's version of this edits nothing on disk; your paper and your teacher's paper are what would have caught a disk edit.)
- **D.** The second question is answered `11.0`: a clean number from a "tool" that multiplied one number by 1. The draft plan assumed there are at least two numbers to combine; `week-11` has one. Repair, keeping the router: the plan **refuses** when it has fewer than two numbers. Repaired output:

```text
agent     'what is 0.00144 times 250'                   -> 0.36
agent     'what does the note say about week-11'        -> NOT IN NOTES
```

 The router is a rule about digits and is written down as a known limit; the number that would show it is the **routing** line of `run_eval.py` (`23/25` in the worked example: c20 is sent to the agent by a year and is refused there, the right answer by the wrong road).

### Page 35.5
1. Week 34 §3: if the baseline passes most cases, the cases are too easy, so write the script instead (a harder set, not a cleverer system). Accept any answer that says the **cases** were too easy.
2. One copied sentence cannot hold two facts, and the retrieval fetched both notes: the number is a property of this stand-in's copy rule, not of RAG. Write: *"with this one-sentence copier, `multi_hop` scored 0 of 4; the retrieved notes held both facts in N of 4."* Look at the `retrieved` list.
3. It counts errors the catch-all caught and wrote down (it would say `1` on a draft that crashed inside `answer()`). It does **not** count wrong answers, and it says nothing about a path that returns a clean wrong number (35.4-D).
4. The `factual 8 → 5` with three named cases and a mechanism (the higher threshold refuses answerable questions) is the finding. The overall `17 → 15` is inside the wobble (about 2.3 per score; the bar was 6.8).
5. It is **re-freezing**: it changes what green means. Your teacher would notice on Monday, because your paper holds the committed numbers too.
6. It is a speed bump: it matches shapes (`../`, `/etc/`, "the instructions you were given") and not meanings, so paraphrased overrides get through. The wall is the **capability limit** (sandbox, named files only, iteration cap, confirmation), which is why A1's fix is a write guard and not a longer list of bad words.
7. Any real attack you did not run: a paraphrased override, another language, an instruction in a hidden comment. Honest sentence: *"I attempted N attacks in 5 categories; k landed; here is the log, including the ones that failed."*

### Page 35.6 and Self-Check
Your words, your numbers. Bug Log rules, for the four bugs above: A (loud): the error names the line where the dictionary arrived, the cause is one frame up; rule: *pass what the function asks for, and let a type error crash.* B (silent): control run, defence off must say landed. C (silent): the promise is a commitment; report `MISSED`. D (silent): a clean number is not a correct number; refuse when the inputs are not there, and read the routing line. For the worked example the closing sentence reads: *"On my 25 frozen cases (fingerprint your 12 characters, checked against the paper) my baseline scored 11 and my spine 17; I promised 0.70 and measured 0.68, so I report it as MISSED; I attempted 5 attacks, 1 landed before any fix (plus the 2 of 3 near-miss probes under A5), I fixed 1 and accepted 1; every dollar and millisecond is a stand-in, which says nothing about a real model."* If a tick is not earned, go back to: the tally and the wobble (35.1), promises, p95 and the router's cost (35.2), the card, the control and the happy path (35.3), the four bugs (35.4).
