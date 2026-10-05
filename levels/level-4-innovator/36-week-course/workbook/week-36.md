# Workbook — Week 36: Capstone 3, Demo, System Card, Final Assessment

**Name:** ________________________________  **Date:** ______________

[⬅ Week 35](week-35.md) · [📖 Read the chapter first](../student-guide/week-36.md) · [Course Home](../README.md) · *There is no Week 37: this is the last page of Level 4.*

---

> **Rules for this workbook.** There is **no new maths and no new syntax** this week. Pages 36.3 and 36.4 reuse four old pieces of arithmetic (the triangular sum, Cohen's kappa, the calibration gap, the wobble) with **fresh practice numbers**, so that they are warm for the paper and not memorised. Pages 36.1 to 36.4 are **pen first**: write your answer by hand, then run the check. **A guess written after the run is not a guess.**
>
> **Nothing here calls a model.** Every "system" is either a table of counts typed in or a tiny scripted function, and every one is labelled. *Stand-in, not a model:* nothing printed here says anything about any real model. Every dollar is a **stand-in dollar** and every millisecond a **stand-in millisecond**. The 25-case numbers on Page 36.1 are the chapter's worked example ("Ask My Notes"); the 20-case system on Page 36.4 and everything on Page 36.5 is **invented practice material**. **Your own card is built from your own logs**, not from these pages.
>
> **Real numbers.** Every number printed below came from running the code shown, on CPU. Nothing is random in this workbook. The attacks and failures mentioned are defensive and educational and are only ever run against scripted stand-ins.
>
> **This workbook is not the paper.** The paper (Sitting 2) is a different set of questions. Do these pages first; do not look for the paper's questions here.
>
> **Files you need.** Every "check" block is **self-contained**: it defines every name it uses, needs only Python 3 and can be run from any folder. Whole workbook at the computer: under 1 second. A pen and a calculator with a square-root key. The pages marked *your own* use your ledger, your run-sheet and your card.
>
> **Calculator.** Plain arithmetic. Four decimals while you work, round only the answer.

---

## ✅ Warm-Up (5 min, before anything else, from memory)

1. A claim, in this course, has two things written beside it or it is "a mood". Which two? ______________ and ______________
2. Name the ten parts of the card, or as many as you can: ____________________________________________________
3. Which section is the one that "gets read", and what does it have to name? ____________________________________________________
4. What does the demo have to show *on purpose* that a sales pitch would hide? ______________
5. The wobble of a count: `sqrt(____ × ____ × ____)`. Write the formula with its three letters.

---

## 🧮 Page 36.1 — The Claim Ledger (35 min · pen, then one check)

**The ledger rule.** One line per claim: **the sentence · the number · the `n` · the command that printed it.** A claim with no command does not go in the card. A rate with no count is not a claim.

**A. Judge the draft.** Below are eight sentences from a draft card for the worked example (25 frozen cases). For each, tick what is **present**, then choose a verdict: `IN` (goes in as written), `FIX` (goes in after a repair: write the repair) or `OUT` (cannot be repaired into a claim).

| # | draft sentence | number? | `n`? | command? | verdict | the repair, in your words |
|:-:|---|:-:|:-:|:-:|:-:|---|
| 1 | "The spine is about 68% accurate." | | | | | |
| 2 | "`multi_hop` passed 0 of 4 (`run_eval.py v1.1`), with this stand-in's one-sentence copier." | | | | | |
| 3 | "RAG fails at multi-hop questions." | | | | | |
| 4 | "Latency: p95 0.6 ms, very fast." | | | | | |
| 5 | "Attack A1 landed 15 of 50 before the named-files guard and 0 of 50 after (seeds 0-49)." | | | | | |
| 6 | "The system is secure." | | | | | |
| 7 | "`factual`: 0.89." | | | | | |
| 8 | "We scored 0.72 against a promise of 0.70 (kept)." *(A real rounding defect in `c15` was repaired after the score of 17 of 25 had been seen.)* | | | | | |

Sentence 5 is closer to a claim than the others. What is still missing before a stranger can believe the **0**? ____________________________________________________

**B. Your own ledger.** Fill in at least eight lines **from your own logs** (overall, baseline, floor, each category, routing, the cost line, each attack, each promise). *No line may leave a column empty.*

| claim (sentence) | number | `n` | the command that printed it |
|---|---|:-:|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

Which claim would you least like a stranger to check? ______________ Check that one first. Did it hold? ______

**C. A rate hides its `n`.** On 9 cases, `8 of 9` is `0.89`. On 900 cases, `800 of 900` is also `0.89`. By hand: (i) one more failure on the 9 cases moves the rate from ______ to ______ ; (ii) one more failure on the 900 cases moves it from `0.889` to about ______ ; (iii) `wobble = sqrt(n × p × (1 − p))` for `8 of 9`: ______ cases; for `800 of 900`: ______ cases. Which of the two rows says more, and what does the card write so that a reader can tell? ____________________________________________________

```python
# check361.py - Page 36.1: a rate hides its n; the wobble of 8 of 9 against 800 of 900; one more failure on 9 cases. (Plain Python; no files needed.)
def wob(k, n):
    p = k / n
    return (n * p * (1 - p)) ** 0.5
for k, n in [(8, 9), (800, 900)]:
    print(f"{k} of {n}: rate {k / n:.2f}  wobble of the count {wob(k, n):.2f} cases  = {wob(k, n) / n:.3f} of the rate")
print("one more failure on 9 cases:", f"{8 / 9:.2f} -> {7 / 9:.2f}")
print("one more failure on 900 cases:", f"{800 / 900:.3f} -> {799 / 900:.3f}")
print("17 of 25 =", 17 / 25, "| 18 of 25 =", 18 / 25, "| the promise was 0.70 and 0.70 * 25 =", 0.70 * 25)
```

```text
8 of 9: rate 0.89  wobble of the count 0.94 cases  = 0.105 of the rate
800 of 900: rate 0.89  wobble of the count 9.43 cases  = 0.010 of the rate
one more failure on 9 cases: 0.89 -> 0.78
one more failure on 900 cases: 0.889 -> 0.888
17 of 25 = 0.68 | 18 of 25 = 0.72 | the promise was 0.70 and 0.70 * 25 = 17.5
```

The last line: how many cases did the system need to pass to keep a promise of `0.70`? ______ . So by how many cases was `17` short? ______

---

## 🧮 Page 36.2 — The Run-Sheet (25 min · pen, then one check)

The demo is **five minutes by the clock**: `30 + 60 + 60 + 60 + 60 + 30` seconds. Fill the clock column by adding, **before** you run the check. Then fill the last two columns **for your own project**.

| segment | seconds | clock starts at | what I say (one sentence) | what I run |
|---|:-:|:-:|---|---|
| 1. Say it | 30 | ______ | | |
| 2. It works | 60 | ______ | | |
| 3. The number (worst row first) | 60 | ______ | | |
| 4. It fails, on purpose | 60 | ______ | | |
| 5. I attacked it | 60 | ______ | | |
| 6. Who should not rely on it (read the card's last section aloud) | 30 | ______ | | |
| **total** | ______ | | | |

Three boxes, in your own words:

- **The question that works:** ____________________________________________________
- **The question that fails on purpose, and its mechanism in one sentence:** ____________________________________________________
- **The sentence I read from section 10:** ____________________________________________________

```python
# check362.py - Page 36.2: the run-sheet's clock column from the seconds, and a sheet that does not add to 300. (Plain Python; no files needed.)
def clock(seconds):
    t, out = 0, []
    for s in seconds:
        out.append(f"{t // 60}:{t % 60:02d}")
        t += s
    return out, t
for name, secs in [("fixed sheet", [30, 60, 60, 60, 60, 30]), ("a draft sheet", [30, 60, 60, 60, 90, 30])]:
    starts, total = clock(secs)
    print(f"{name}: starts {starts}  total {total} s = {total // 60}:{total % 60:02d}", "-> five minutes" if total == 300 else "-> NOT five minutes")
```

```text
fixed sheet: starts ['0:00', '0:30', '1:30', '2:30', '3:30', '4:30']  total 300 s = 5:00 -> five minutes
a draft sheet: starts ['0:00', '0:30', '1:30', '2:30', '3:30', '5:00']  total 330 s = 5:30 -> NOT five minutes
```

Did your clock column match the first line? ______ In the draft sheet, which segment ran long, and what does the demo have to drop first, **the failure or something else**? ____________________________________________________ Why? ____________________________________________________

Rehearsal, timed, on your own machine: run 1 took ______ : ______ ; did you say the words *stand-in, not a model* aloud once? ______ ; did the cold start (a new terminal, `python capstone34/ask.py "..."`) work the first time? ______

---

## 🧮 Page 36.3 — Four Old Sums, Fresh Numbers (45 min · pen, then computer)

These are **practice numbers**, not the paper's. Work each by hand. Show the steps.

**A. The bill for a long task (Week 29).** An agent adds **200 tokens** to its history at every step and **re-sends the whole history** at every step. It runs **8 steps**.
(i) Tokens sent in step 8: ______ (ii) Total over the 8 steps `= 200 × k(k+1)/2`: ______ (iii) At **$0.002 per 1,000 tokens** (stand-in dollars): $______ (iv) The task is doubled to **16 steps**. The total is ______ ; the bill is ______ times the first bill (to two decimals). Doubled? ______

**B. Two raters (Week 30).** A and B each mark the same 20 tickets *pass* or *fail*:

```text
                 B says pass   B says fail
A says pass         10             2
A says fail          3             5
```

(i) `p_o` (agreement): ______ (ii) Share of *pass* from A: ______ from B: ______ (iii) `p_e = (A pass × B pass) + (A fail × B fail)`: ______ (iv) `kappa = (p_o − p_e) / (1 − p_e)`: ______ (three decimals) (v) Is the agreement mostly luck, or mostly more than luck? ______

**C. Said against delivered (Week 32).** A system's 20 results fall into three buckets:

```text
bucket        results   right   confidence it stated
"said 0.9"       8        6          0.9
"said 0.7"       6        4          0.7
"said 0.5"       6        3          0.5
```

(i) Actual accuracy of each bucket: ______ , ______ , ______ (ii) Gap `|actual − said|` of each: ______ , ______ , ______ (iii) Size-weighted average of the gaps (weights 8, 6, 6 out of 20): ______ (iv) The bucket that is most over-confident, and by how much: ______________

**D. The wobble (Week 33).** `14 of 20` and `11 of 20`.
(i) wobble of 14: ______ (ii) wobble of 11: ______ (iii) combined `= sqrt(w₁² + w₂²)`: ______ (iv) bar (twice the combined): ______ (v) the gap is 3 cases: more than noise? ______

```python
# check363.py - Page 36.3: four pieces of hand arithmetic from earlier weeks, then by code. (Plain Python; the numbers are invented practice numbers, different from the paper's.)
t, k = 200, 8
total = t * (k * (k + 1) // 2)
print("A. tokens in step", k, "=", t * k, "| total =", total)
print("   cost at $0.002 per 1,000 tokens = $" + f"{total / 1000 * 0.002:.4f}")
total2 = t * (16 * 17 // 2)
print("   16 steps: total", total2, "| multiple of the 8-step bill:", round(total2 / total, 2))
# B. kappa on a 2 x 2 table of 20 tickets
both_pass, a_only, b_only, both_fail = 10, 2, 3, 5
n = both_pass + a_only + b_only + both_fail
po = (both_pass + both_fail) / n
a_pass, b_pass = (both_pass + a_only) / n, (both_pass + b_only) / n
pe = a_pass * b_pass + (1 - a_pass) * (1 - b_pass)
print(f"B. p_o {po:.2f}  A says pass {a_pass:.2f}  B says pass {b_pass:.2f}  p_e {pe:.4f}  kappa {(po - pe) / (1 - pe):.3f}")
# C. calibration gap over three buckets: (said, results, right)
buckets = [(0.9, 8, 6), (0.7, 6, 4), (0.5, 6, 3)]
size = sum(r for s, r, c in buckets)
for s, r, c in buckets:
    print(f"C. said {s}: actual {c}/{r} = {c / r:.3f}  gap {abs(c / r - s):.3f}  ({'over-confident' if c / r < s else 'not over-confident'})")
print("   weighted gap:", round(sum(r * abs(c / r - s) for s, r, c in buckets) / size, 3))
# D. wobble of 14 of 20 against 11 of 20
def wob(k, n=20):
    p = k / n
    return (n * p * (1 - p)) ** 0.5
w1, w2 = wob(14), wob(11)
comb = (w1 ** 2 + w2 ** 2) ** 0.5
print(f"D. wobble 14: {w1:.2f}  wobble 11: {w2:.2f}  combined {comb:.2f}  twice {2 * comb:.2f}  gap 3 ->", "more than noise" if 3 > 2 * comb else "inside the noise")
```

```text
A. tokens in step 8 = 1600 | total = 7200
   cost at $0.002 per 1,000 tokens = $0.0144
   16 steps: total 27200 | multiple of the 8-step bill: 3.78
B. p_o 0.75  A says pass 0.60  B says pass 0.65  p_e 0.5300  kappa 0.468
C. said 0.9: actual 6/8 = 0.750  gap 0.150  (over-confident)
C. said 0.7: actual 4/6 = 0.667  gap 0.033  (over-confident)
C. said 0.5: actual 3/6 = 0.500  gap 0.000  (not over-confident)
   weighted gap: 0.07
D. wobble 14: 2.05  wobble 11: 2.22  combined 3.02  twice 6.05  gap 3 -> inside the noise
```

Which of your sums disagreed with the printout? ______ . Which **step** went wrong (not which number)? ____________________________________________________

---

## 🧮 Page 36.4 — Reading Two Versions (30 min · pen, then one check)

An **invented** toy system with 20 cases and two versions, `v1` and `v3` (stand-in, not a model; the counts are typed in, the arithmetic is real). The team wrote a promise **before** measuring: *score at least 0.75*.

```text
category     n   v1   v3
lookup       8    7    6
sums         6    3    5
refusals     4    2    4
tricky       2    1    1
OVERALL     20   13   16
```

A teammate says: *"v3 scored 16 against 13. That is three more. v3 kept the promise, v1 did not. Ship v3. The lookup drop of one is noise."*

**A. Fill in by hand.** The wobble of `13 of 20`: ______ ; of `16 of 20`: ______ ; combined: ______ ; bar (twice): ______ ; the gap is ______ , so the overall is ______________ (more than noise / inside the noise).

**B. The promise.** `0.75 × 20 =` ______ cases. `v1` passed ______ : short by ______ cases, so the verdict is ______________ . `v3` passed ______ : headroom of ______ case(s), so the verdict is ______________ and the margin is ______________ (thin / comfortable).

**C. By category.** The table says `lookup` went **down** by ______ and `sums` and `refusals` went **up** by ______ and ______ . For each of the three, circle what the table alone **can** support and what it **cannot** (it cannot say *which cases flipped* or *why*):
 - `lookup 7 → 6 of 8`: a finding / a hint / noise? ______________
 - `sums 3 → 5 of 6`: a finding / a hint / noise? ______________
 - `refusals 2 → 4 of 4`: a finding / a hint / noise? ______________

What would you need to be shown, in addition to this table, to turn a hint into a finding? ____________________________________________________

**D. The reply (at most six sentences).** Write the reply to your teammate. It must say whether `13 → 16` is a finding by itself, what happened to the promise, what the table cannot tell you, and *two sentences the card must contain*:

____________________________________________________
____________________________________________________
____________________________________________________
____________________________________________________

```python
# check364.py - Page 36.4: two versions of an INVENTED toy system on 20 invented cases (stand-in, not a model). The arithmetic is real; the table is typed.
cats = {"lookup": (8, 7, 6), "sums": (6, 3, 5), "refusals": (4, 2, 4), "tricky": (2, 1, 1)}
print(f"{'category':9s} {'n':>2s} {'v1':>3s} {'v3':>3s}")
for c, (n, a, b) in cats.items():
    print(f"{c:9s} {n:2d} {a:3d} {b:3d}")
n = sum(v[0] for v in cats.values()); a = sum(v[1] for v in cats.values()); b = sum(v[2] for v in cats.values())
print(f"{'OVERALL':9s} {n:2d} {a:3d} {b:3d}")
def wob(k, n):
    p = k / n
    return (n * p * (1 - p)) ** 0.5
comb = (wob(a, n) ** 2 + wob(b, n) ** 2) ** 0.5
print(f"wobble v1 {wob(a, n):.2f}  v3 {wob(b, n):.2f}  combined {comb:.2f}  twice {2 * comb:.2f}  gap {b - a} ->", "more than noise" if b - a > 2 * comb else "inside the noise")
print("promise: score at least 0.75 ->", f"v1 {a} of {n} = {a / n:.2f}", "MISSED" if a / n < 0.75 else "kept", "| v3", f"{b} of {n} = {b / n:.2f}", "MISSED" if b / n < 0.75 else "kept")
print("0.75 * 20 =", 0.75 * 20, "cases")
print("average of the four category rates for v3:", round(sum(v[2] / v[0] for v in cats.values()) / 4, 3), "| the overall:", b / n)
```

```text
category   n  v1  v3
lookup     8   7   6
sums       6   3   5
refusals   4   2   4
tricky     2   1   1
OVERALL   20  13  16
wobble v1 2.13  v3 1.79  combined 2.78  twice 5.57  gap 3 -> inside the noise
promise: score at least 0.75 -> v1 13 of 20 = 0.65 MISSED | v3 16 of 20 = 0.80 kept
0.75 * 20 = 15.0 cases
average of the four category rates for v3: 0.771 | the overall: 0.8
```

The last line: which of the two numbers, `0.771` or `0.8`, belongs in the card as the overall, and why? ______________ ____________________________________________________

---

## 🐞 Page 36.5 — Break It on Purpose (four bugs · 35 min)

Run each as written. Predict first. Then say what went wrong and how you would have known. Each is **deliberate**. Every system here is a toy or a stand-in, not a model.

### 36.5-A (loud) — the demo command with no question

```python
# DELIBERATE BUG 36.5-A (loud): a one-question command-line tool run with no question. (Stand-in: it only repeats the question back; it is not a model.)
import argparse
parser = argparse.ArgumentParser(prog="ask.py")
parser.add_argument("question")
args = parser.parse_args([])                  # the demo command, typed with nothing after it
print("you asked:", args.question)
```

Prediction (is there a traceback? what is the last line?): ____________________________________________________

```text
usage: ask.py [-h] question
ask.py: error: the following arguments are required: question
```

It is loud and it is short, and it is easy to skip over. When in the week would you meet it for the **first** time if you did not practise, and what one habit moves it earlier? ____________________________________________________

### 36.5-B (SILENT) — the score that moved after it was seen

```python
# DELIBERATE BUG 36.5-B (SILENT): the card's score line after a real defect was fixed AFTER the score was seen. (What-if arithmetic on typed counts; a toy, not a model.)
promise, n = 0.70, 25
first_run = 17                                  # what the frozen cases measured
fixed_after_seeing = first_run + 1              # one rounding defect repaired; one more case now passes
for label, passed in [("card line, version A (first run)", first_run), ("card line, version B", fixed_after_seeing)]:
    print(f"{label}: {passed} of {n} = {passed / n:.2f} against a promise of {promise:.2f} ->", "kept" if passed / n >= promise else "MISSED")
```

Prediction (which line would a card print if it kept **only** the second number?): ____________________________________________________

```text
card line, version A (first run): 17 of 25 = 0.68 against a promise of 0.70 -> MISSED
card line, version B: 18 of 25 = 0.72 against a promise of 0.70 -> kept
```

Nothing is wrong with the arithmetic, and a reader of version B is misled. Who? ______________ Write the line the card should hold instead (both numbers, the verdict on the promise, and the three words that say when the fix happened): ____________________________________________________

### 36.5-C (SILENT) — a retention rule nobody runs

```python
# DELIBERATE BUG 36.5-C (SILENT): the card says "traces older than 7 days are deleted". The function exists. Who calls it? (Invented file names and ages; no real files.)
traces = {"mon_trace.jsonl": 2, "old_trace.jsonl": 40}          # name -> age in days
def sweep(files, days):
    return {name: age for name, age in files.items() if age <= days}
print("card says: older than 7 days are deleted")
print("the traces on disk today:", sorted(traces))
print("what sweep() WOULD keep, if somebody ran it:", sorted(sweep(traces, 7)))
```

Prediction (is the 40-day-old file still there? what does the card claim?): ____________________________________________________

```text
card says: older than 7 days are deleted
the traces on disk today: ['mon_trace.jsonl', 'old_trace.jsonl']
what sweep() WOULD keep, if somebody ran it: ['mon_trace.jsonl']
```

The function is correct and the sentence is false. What would have to exist for the sentence to be true without any extra words, and does it exist in your system? ______ So write the sentence that **is** true: ____________________________________________________

### 36.5-D (SILENT) — the quote that wishes

```python
# DELIBERATE BUG 36.5-D (SILENT): a quoted wrong output rewritten to what the author wishes it had said. (STAND-IN, NOT A MODEL: ask() is a lookup table of canned sentences.)
def ask(q):
    canned = {"what dropout rate did the gru use": "Dropout 0.1 changed almost nothing. [2]"}
    return canned.get(q.lower().strip("?"), "NOT IN NOTES")
card_quote = ("What dropout rate did the GRU use?", "I could not find this in the notes.")      # typed by the author, never re-asked
q, said = card_quote
print("the card quotes:", said)
print("the system says:", ask(q))
print("quote still true:", said == ask(q))
```

Prediction (what does the last line say?): ____________________________________________________

```text
the card quotes: I could not find this in the notes.
the system says: Dropout 0.1 changed almost nothing. [2]
quote still true: False
```

The quote is evidence of a failure, and the author replaced the evidence with a wish. What one habit makes this impossible, and what does it cost? ____________________________________________________

---

## 📓 Page 36.6 — Stop and Think (15 min · pen only)

1. A stranger asks "how accurate is it?" and your log says `17 of 25`. Write the one sentence you give them, with an `n`, a stand-in label and the wobble in words. ____________________________________________________
2. Your section 10 says "May occasionally be inaccurate, so users should verify important information." Name **four** things it is missing. ____________________________________________________
3. A friend says the demo should show your three best questions. What does `demo.py` do about that, and why does the demo have to contain a failure? ____________________________________________________
4. Section 7's heading says *a plan; none of it has happened*. What does a stage that was never run have, and what does it not have? ____________________________________________________
5. `check_card` prints `[]` on your card. What has that proved, and what has it not proved? What does the proof need? ____________________________________________________
6. You score `48 of 75` on the paper. What does that say about your capstone? Which two weeks do you circle first, and which weeks do you never circle on the strength of one question? ____________________________________________________
7. On Sunday night you have a good idea for a better retriever. Where does it go, and what does it **not** become? ____________________________________________________
8. In the one-line test someone points at a wrong answer: was it retrieval, generation, the prompt, the tokenizer, or a person over-trusting it? Name the **evidence** you would show for each (a file, a number or a quoted line), and say which of the five your capstone cannot have. ____________________________________________________

---

## 📓 Page 36.7 — The Bug Log

| # | What went wrong (your words) | Loud or silent? | The one line or check that caught it | The rule I will keep |
|:-:|---|:-:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

Checks to keep: **a number with its `n`, never a rate alone · the claim ledger filled from the logs, one command per line · a missed promise said as missed, and a fix after seeing the score quoted with both numbers · every dollar and millisecond called stand-in · a quote re-asked, never retyped · a rule in the card that something actually runs, or the words "by hand" · the demo's failure chosen first · the honest section naming a person, an input, an output and a number.**

Then write this in your own handwriting, with your own numbers, and keep the words *stand-in* and *n*:

> "On my ______ frozen cases my system passed ______ ; the baseline passed ______ ; I promised ______ and measured ______ , so I report it as ______________ ; the wobble is about ______ cases. The case I would least like checked is ______________ . ______________ should not rely on it for ______________ , because on the input `____________` it said `____________` . Every dollar and millisecond is a stand-in, which says nothing about a real model."

**After the paper.** The two weeks I circled on the per-week grid: ______________ and ______________ . The pages of this book I will redo first: ______________ .

---

## 🧠 Self-Check (from memory, no notes)

- [ ] I can fill a claim ledger and say why a claim with no command, or a rate with no `n`, stays out of the card.
- [ ] I can say, from the printout, why `0.89` on 9 cases and `0.89` on 900 are different claims.
- [ ] I can fill a five-minute run-sheet that adds to 300 seconds and keeps one failure in it.
- [ ] I can do the triangular sum, a kappa on a 2 × 2 table, a calibration gap and a wobble by hand.
- [ ] I can say when a gap is "inside the noise" and why a category with a named mechanism can still be a finding.
- [ ] I can say what `check_card` finds and what it cannot, and what the proof needs.
- [ ] I can say why a retention rule needs someone to run it, and why a quote must be re-asked and never retyped.
- [ ] I can say, in one sentence with a number and an `n`, who should not rely on my system.

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up
1. A **number** and an **`n`** (the number of cases behind it); and, in the ledger, the command that printed it.
2. Intended use · out of scope · measured numbers · failure modes · guardrails and red-team results · retention · staged release · incident response · contact · what it fails at, and who should not rely on it.
3. Section 10, the honest section. It names a **person**, a **real input**, the **real wrong output** and a **number with an `n`**.
4. A **failure**, live, with its mechanism in one sentence.
5. `sqrt(n × p × (1 − p))`.

### Page 36.1
- **A.** 1: has a rate, no `n`, no command, and "accurate" claims more than 25 stand-in cases can say. **FIX** → "17 of 25 on the frozen cases (`run_eval.py v1.1`), a stand-in's score". 2: number, `n` and command are there and the stand-in is named. **IN**. 3: a general claim about RAG from one copy rule on four cases: **OUT** (the claim is about *this copier*; sentence 2 is the repair). 4: no command that will print the same on another laptop, no *stand-in* label, and "fast" means nothing about a real model: **FIX** → "p95 in stand-in milliseconds, which changes on every run and says nothing about a real model" (or drop it and quote the stand-in dollars, which repeat). 5: number, `n`, command: **FIX/IN**; still missing is the **control**: the legitimate save `50 of 50` before and after, so that "0" cannot mean "the guard broke everything". 6: no number, no `n`, no command, and the word is banned: **OUT**. 7: a rate with no `n`: **FIX** → "8 of 9". 8: **FIX**: it quotes only the second number. Write both: `17 of 25` (promise `0.70`, **MISSED**, one case short) and `18 of 25` after a repaired rounding defect, *fixed after seeing the score*.
  Missing before the 0 is believable: the **control** (the legitimate save still works, 50 of 50 after).
- **B.** Your own words and numbers. Marks: every line has all four columns; every `n` is a count of cases, not a rate; every command is one you can run again. The claim you would least like checked is usually the missed promise or the weakest category.
- **C.** (i) `0.89` to **0.78**. (ii) `0.889` to about **0.888**. (iii) `8 of 9`: **0.94** cases; `800 of 900`: **9.43** cases (`0.105` against `0.010` of the rate). The 900-case row says far more: one failure barely moves it, and its rate is known to a hundredth. The card writes `8 of 9` and `800 of 900`, so the `n` travels with the number. The last line: `0.70 × 25 = 17.5`, so **18** cases were needed; `17` was **one** case short.

### Page 36.2
Clock column: `0:00, 0:30, 1:30, 2:30, 3:30, 4:30`; total **300** (5:00). In the draft sheet segment 5 (*I attacked it*) was given 90 seconds and the total is **330** (5:30). Drop time from the *talking* (trim segment 5 back to 60 or shorten another), **never the failure**: a demo that cannot show a failure is not finished. The boxes and the rehearsal are your own. Marks: the failure has a mechanism in one sentence (*the copier took the wrong sentence*, *the near-miss scored above answerable questions*, *the note was not among the three fetched*); the worst row is read first; *stand-in, not a model* is said once aloud; the cold start was run once before being watched.

### Page 36.3
- **A.** (i) `200 × 8 =` **1,600**. (ii) `200 × (8 × 9 / 2) = 200 × 36 =` **7,200**. (iii) `7,200 ÷ 1,000 × 0.002 =` **$0.0144**. (iv) `200 × (16 × 17 / 2) = 200 × 136 =` **27,200**; `27,200 ÷ 7,200 =` **3.78** times. **Not doubled**: history is re-sent every step, so doubling the steps costs about four times.
- **B.** (i) `(10 + 5) / 20 =` **0.75**. (ii) A: `(10 + 2) / 20 =` **0.60**; B: `(10 + 3) / 20 =` **0.65**. (iii) `0.60 × 0.65 + 0.40 × 0.35 = 0.39 + 0.14 =` **0.53**. (iv) `(0.75 − 0.53) / (1 − 0.53) = 0.22 / 0.47 =` **0.468**. (v) A little under half-way from luck to perfect agreement: more than luck, well short of agreement. (Accept "moderate"; the point is that `0.75` agreement looks better than it is because `0.53` was expected by luck alone.)
- **C.** (i) `6/8 =` **0.750**; `4/6 =` **0.667**; `3/6 =` **0.500**. (ii) **0.150**, **0.033**, **0.000**. (iii) `(8 × 0.15 + 6 × 0.0333 + 6 × 0) / 20 = 1.4 / 20 =` **0.07**. (iv) the **"said 0.9"** bucket, over-confident by **0.15** (it said `0.9` and delivered `0.75`).
- **D.** (i) `sqrt(20 × 0.70 × 0.30) =` **2.05**. (ii) `p = 0.55`, `sqrt(20 × 0.55 × 0.45) =` **2.22**. (iii) `sqrt(2.05² + 2.22²) =` **3.02**. (iv) **6.05**. (v) gap `3` is smaller than `6.05`: **inside the noise**.

Which step went wrong (typical): in A the *total* (forgetting the `/ 2`, or using `k²`); in B the `p_e` (forgetting the *fail × fail* half); in C the weights (using `3` buckets instead of `20` results); in D the square root of the *sum* (adding wobbles instead of squares).

### Page 36.4
- **A.** wobble of 13: `p = 0.65`, **2.13**; of 16: `p = 0.80`, **1.79**; combined **2.78**; bar **5.57**; gap **3**: **inside the noise**.
- **B.** `0.75 × 20 = 15` cases. `v1` passed **13**: short by **2** cases: **MISSED**. `v3` passed **16**: headroom **1** case: **kept**, the margin **thin** (one case, and the wobble is about 2).
- **C.** `lookup` went **down by 1** (7 to 6 of 8); `sums` **up by 2** (3 to 5 of 6) and `refusals` **up by 2** (2 to 4 of 4). Each is **a hint, not yet a finding**, by the table alone: one case of eight is inside the noise; two cases of six or of four are too few to rule out luck, and the table does not say *which* cases flipped or *why*. To turn a hint into a finding you need the **named cases** that flipped in each direction and a **mechanism** that explains them (for example, "v3 added a calculator path, so the sums that were failing now pass; its refusal rule is eager, which would also cost a lookup question"). The mechanism, checked against the named case, is what makes a category a finding even when the overall is inside the noise.
- **D.** Your words; marks for: "`13 → 16` is inside the noise (gap 3, bar about 5.6), so it is not a finding by itself"; "`v1` missed `0.75` by two cases; `v3` kept it by one, a thin margin, and the promise was written before the measurement and is not edited"; "the tables cannot say which cases flipped, why, or how a real model would behave: these are 20 invented cases and a stand-in"; two card sentences, e.g. "v3 scored 16 of 20 against a promise of 0.75 (a margin of one case)" and "Someone who needs a refusal on every out-of-scope question should not rely on it: it refused 4 of 4 on 4 cases, and one lookup question that used to pass now fails." Ship decision: either answer earns the mark if it names a reason and the thinness of the margin ("ship v3 with the named lookup failure in section 4" is a good one).
- **Last line.** **`0.8`**: the overall is made by **adding counts** (`16 of 20`), never by averaging rates. `0.771` weights a 2-case category as heavily as an 8-case one and is not a score anything measured.

### Page 36.5
- **A.** There is **no traceback**: `argparse` prints the usage line and `error: the following arguments are required: question`, and exits. You would first meet it **at the start of the demo, in front of someone**. The habit: a **cold start** in a new terminal, once, before you are watched (and the run-sheet's segment 2 contains the command, with its question).
- **B.** Version B alone says `0.72 ... kept`. **Whoever reads the promise table** is misled: the promise looks kept. The card holds: *"17 of 25 = 0.68 against a promise of 0.70: MISSED, one case short. A rounding defect in c15 was repaired after seeing the score, giving 18 of 25 = 0.72: fixed after seeing the score."* Both numbers, the verdict on the **original** promise, and the three words *fixed after seeing the score*. A defect may be repaired; the first measurement is never deleted.
- **C.** The 40-day-old file **is** still there; the card claims it is deleted. For the sentence to be true with no extra words, **something has to call `sweep`**, on a schedule. In this system nothing does (say so about your own). The true sentence: *"Traces older than 7 days are deleted by hand when somebody runs `sweep()`; nothing runs it on a schedule."* A rule in the card that no program runs is a wish.
- **D.** `quote still true: False`: the card describes a system that does not exist. The habit: **re-ask every quoted question, and paste the answer; never retype a quote**. It costs one re-run each time the system changes (and that is the point: the card is regenerated from the system, not remembered). If the output is not the one you wish it were, that is the finding.

### Page 36.6
1. *"On my 25 frozen cases, with these stand-ins, 17 passed; a different 25 questions would move that by about 2 or 3 cases; every cost and time is a stand-in."* Marks for the `n`, the word *stand-in* and the wobble in words.
2. No **person** named; no **real input**; no **real wrong output**; no **number with an `n`**. (Also acceptable: nothing a stranger could act on.)
3. `demo.py` carries an `assert` that **refuses to finish** unless at least one failing case is shown. A demo of three best cases is a sales pitch; the failure is what the audience can trust the rest by. The fix is to **choose the failure first** and write its mechanism in one sentence.
4. It has a **plan**: stages, a gate for each, a stop condition. It has **no result**: nothing was observed. Writing a number for a stage that was not run would be a quote that wishes (36.5-D).
5. It proved that the card has the ten headings, no number outside the logs and the design, no table row without an `n` beside a count, no unlabelled time, no banned phrase, a `MISSED` where needed and a named person. It has **not** proved any sentence is true, nor that an `n` is the right `n`. The proof is `quotes_hold` (the quotes re-asked) **plus you reading every number against the log**.
6. **Nothing** about the capstone: the paper tests Term 4's ideas; the capstone is marked from the card, the numbers and the demo. Circle the two weeks with the **lowest** `marks / available`, preferring Weeks 28 and 29 (they carry the most marks and their ideas are used again later). **Never circle Weeks 26 or 34 on one question**: one question is not a pattern.
7. It goes in section 8 of the card as **what I would add to the eval next**. It does **not** become a version 2 this week, and you do not tune `tau`, `k` or the generator to reach `0.70`.
8. **Retrieval**: the list of fetched notes (was the note with the fact among them?). **Generation**: the right note fetched and the copy rule took the wrong sentence (the sentence, quoted). **The prompt / the gate**: a score such as `0.357` against the threshold. **A person over-trusting it**: the card's section 10 and the sentence you said to your named user. **The tokenizer**: a token count or split that changed the text: **none in this capstone**, which is itself a fact.

### Page 36.7 and Self-Check
Your words, your numbers. Bug Log rules for the four bugs above: A (loud): run the cold start before you are watched. B (SILENT): a real fix after seeing the score is quoted with both numbers and the words *fixed after seeing the score*; the promise is never edited. C (SILENT): a rule in the card is true only if something runs it; otherwise write *by hand*. D (SILENT): re-ask the quote and paste what the system says; never retype it. Marks for the closing sentence: the `n`, the baseline, the promise **and** the measurement with the word `MISSED` or `kept`, a named person, a real input and a real output, and the words *stand-in*.

**After the paper.** The two weeks and the pages to redo are yours. Nothing on the grid is a grade; it is where to look if you ever build on this.

