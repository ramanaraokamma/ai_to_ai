# Workbook — Week 30: Evaluating LLM Systems: The Frozen Suite and the Judge

**Name:** ________________________________  **Date:** ______________

[⬅ Week 29](week-29.md) · [📖 Read the chapter first](../student-guide/week-30.md) · [Course Home](../README.md) · [Next ➡](week-31.md)

---

> **Rules for this workbook.** The one new piece of maths is **Cohen's kappa**: `κ = (p_o − p_e) / (1 − p_e)`, agreement with the agreement-by-luck taken out. The pen-and-paper work is *word sets and Jaccard, applying keyword rules in order, a kappa grid, and reading two letters per pair*. Then the computer confirms. **Write your answer by hand first, then run.** A guess written after the run is not a guess.
>
> **Real numbers.** Every number printed below came from a real run of the code shown, on a CPU, in about a second. Everything that looks random is **seeded**, so your counts should match. By-hand numbers are plain arithmetic.
>
> **There is no language model here.** The keyword rules are a list a person typed. The replies are built from fixed templates by Python. The rubric is a short function. The sealed judge in `mystery.py` and the `longer_judge` on Page 30.3 are each a **stand-in, not a model**: they read a rubric score or a word count, not language, and the habit in `mystery.py` is a number (`BIAS = 0.5`) somebody typed. **Nothing measured against a stand-in says anything about how often a real judge model shows a position habit.** What transfers is the *method*: write the test first, take luck out of agreement, ask twice in both orders.
>
> **Files you need.** Run every code block in the **same Python session** as your `eval_suite.py` from the chapter, straight after it, because the blocks use its names: `EVAL`, `fingerprint`, `words`, `jaccard`, `rules_predict`, `pairs`, `rubric`, `judge_pair`, `random`, `cohen_kappa_score`, `np`, `H` and `J`. Run it from the folder that holds your eight files (`evalset.py` and the rest) and import them; never retype them. Nothing needs the internet. Nothing here writes a file. **Do not open `mystery.py` to find the answers to Page 30.3**; the point is to find the number by asking.
>
> **Calculator.** Plain arithmetic is enough. Round to three places.

---

## ✅ Warm-Up (5 min, before anything else, from memory)

1. Why is the eval set written and fingerprinted *before* any system is built? What does the fingerprint do, and what can it not do? ____________________________________________________________
2. The trained classifier scored 21 of 30 and the free rules scored 25 of 30. Is something wrong with the code? What does this tell you about the order of work? ____________________________________________________________
3. Two raters agree 90 percent of the time. Name the one other thing you must find out before you call that good. ____________________________________________________________
4. What is a "stand-in, not a model"? Why can't the flip rate of `mystery.py` tell you about a real judge? ____________________________________________________________

---

## 🎲 Page 30.1 — Overlap, and a Second Set (homework · 20 min · pen first)

A ticket becomes a **set** of words: lower case, letters and digits only, each word once (`"don't"` becomes `don` and `t`). `Jaccard = (words in both) / (words in either)`.

**Part 1 (pen, no computer).** Fill in the counts and the fraction for each pair.

| | Ticket X | Ticket Y | In both | In either | Jaccard |
|:--:|---|---|:--:|:--:|:--:|
| 1 | `put the money back on my card` | `cancel order 7781 and put the money back on my card` | | | |
| 2 | `the export button does nothing` | `clicking save does absolutely nothing` | | | |
| 3 | `don't charge me twice` | `did you charge me twice?` | | | |
| 4 | `???` | `!!!` | | | |

(a) Pair 4 has no words at all. What does the formula try to do, and what does the `if (A | B)` in `jaccard` do about it? ____________________________________________________________

(b) The scan removes a training ticket whose Jaccard against an eval ticket is **at least** the threshold. Suppose pairs 1 to 3 are (training, eval) pairs. Threshold `0.60` removes pair(s): ______ Threshold `0.40` removes pair(s): ______

(c) At `0.40`, one of the removals is a different question. Which pair, and why do its words overlap so much? ____________________________________________________________

**Check it (computer).**

```python
# jaccard_check.py - Page 30.1 Part 1: check your hand sets. The last pair has no letters at all.
pairs_j = [
    ("put the money back on my card", "cancel order 7781 and put the money back on my card"),
    ("the export button does nothing", "clicking save does absolutely nothing"),
    ("don't charge me twice", "did you charge me twice?"),
    ("???", "!!!"),
]
for a, b in pairs_j:
    A, B = words(a), words(b)
    print(f"in both {len(A & B)} | in either {len(A | B)} | Jaccard {jaccard(a, b):.3f}   {a!r}")
```

Real output:

```text
in both 7 | in either 11 | Jaccard 0.636   'put the money back on my card'
in both 2 | in either 8 | Jaccard 0.250   'the export button does nothing'
in both 3 | in either 7 | Jaccard 0.429   "don't charge me twice"
in both 0 | in either 0 | Jaccard 0.000   '???'
```

**Part 2 (pen, then computer): a second set.** The free rules were written by the course author who had already seen the 30 frozen tickets. Here are ten **new** tickets, two per category, written for this workbook. **Predict with your pen first.** Apply the rules **in this order**, and stop at the first one that fires: greeting keys (`hi`, `hiya`, `hello`, `hey`, `morning`, `afternoon`, `evening`), then refund keys (`refund`, `return`, `send them back`, `send it back`, `money back`, `reimburs`, `postage`), then billing keys (`invoice`, `plan`, `paying`, `charge`, `card`, `billing`, `subscription`, `twice`), then technical keys (`error`, `crash`, `blank`, `csv`, `loading`, `sync`, `closes`, `rendering`, `nothing`, `inbox`), otherwise `out_of_scope`. A key counts if it appears **anywhere inside** the lower-cased ticket.

| # | Ticket | Gold | Which key fires first? | Your predicted label | Right? |
|:--:|---|---|---|---|:--:|
| 1 | `hi there, anybody about?` | greeting | | | |
| 2 | `evening all` | greeting | | | |
| 3 | `the lamp arrived broken, I want my money back` | refund | | | |
| 4 | `please take this kettle back, it leaks` | refund | | | |
| 5 | `the page is stuck loading forever` | technical | | | |
| 6 | `nothing shows after I tap the icon` | technical | | | |
| 7 | `why was I charged twice for one order?` | billing | | | |
| 8 | `can I change my plan next month?` | billing | | | |
| 9 | `what is the tallest building in Dubai?` | out_of_scope | | | |
| 10 | `which film should I watch tonight?` | out_of_scope | | | |

Your predicted score: ______ / 10. The frozen eval gave `25/30 = 0.833`. Will the second set score higher, lower or the same? ______

```python
# second_set.py - Page 30.1 Part 2: ten NEW tickets, two per category, written for this workbook. The free rules have never seen them.
SECOND_W = [
    ("hi there, anybody about?",                    "greeting"),
    ("evening all",                                 "greeting"),
    ("the lamp arrived broken, I want my money back", "refund"),
    ("please take this kettle back, it leaks",      "refund"),
    ("the page is stuck loading forever",           "technical"),
    ("nothing shows after I tap the icon",          "technical"),
    ("why was I charged twice for one order?",      "billing"),
    ("can I change my plan next month?",            "billing"),
    ("what is the tallest building in Dubai?",      "out_of_scope"),
    ("which film should I watch tonight?",          "out_of_scope"),
]
print("fingerprint of the second set:", fingerprint(SECOND_W))
for t, y in SECOND_W:
    print(f"{rules_predict(t):13s} {y:13s} {'ok' if rules_predict(t) == y else 'MISS'}   {t}")
hits = sum(rules_predict(t) == y for t, y in SECOND_W)
print(f"free rules on the second set: {hits}/10 = {hits / 10:.1f}   (on the frozen eval: 25/30 = 0.833)")
print("highest Jaccard of any second-set ticket against the frozen eval:",
      round(max(jaccard(t, e) for t, _ in SECOND_W for e, _ in EVAL), 3))
```

Real output:

```text
fingerprint of the second set: 9b0b514bf50bc702ae94cb4f034f0760
greeting      greeting      ok   hi there, anybody about?
greeting      greeting      ok   evening all
refund        refund        ok   the lamp arrived broken, I want my money back
greeting      refund        MISS   please take this kettle back, it leaks
technical     technical     ok   the page is stuck loading forever
greeting      technical     MISS   nothing shows after I tap the icon
billing       billing       ok   why was I charged twice for one order?
billing       billing       ok   can I change my plan next month?
out_of_scope  out_of_scope  ok   what is the tallest building in Dubai?
greeting      out_of_scope  MISS   which film should I watch tonight?
free rules on the second set: 7/10 = 0.7   (on the frozen eval: 25/30 = 0.833)
highest Jaccard of any second-set ticket against the frozen eval: 0.25
```

(i) Three tickets were sent to `greeting` wrongly. Which single key did it, and inside which three words? ____________________________________________________________

(ii) The second set scores `0.7`, the frozen eval `0.833`. Is that gap proof that the frozen score was flattered? One ticket is worth how many points on ten? ______ What would you need before you put a number on the gap? ____________________________________________________________

(iii) Highest Jaccard `0.25`. Could any of these ten have been in the training data by copy? What could the scan **not** tell you about them? ____________________________________________________________

**Part 3 (your own set).** Write **ten** tickets of your own, two per category, in your own words and **without looking at the rules**. Put them in a new file `second_set.py` (do **not** touch `evalset.py`), print their `fingerprint(...)`, score the rules, and run the highest-Jaccard line against the frozen eval. Report: hits ______ / 10 · fingerprint (first 8 characters) ____________ · highest Jaccard ______. Which of your tickets did the rules get wrong, and which key or missing key was it? ____________________________________________________________

---

## 📏 Page 30.2 — Kappa by Hand on a Fresh Twenty (homework · 25 min · pen first)

Two programs rate the **old bot's** replies to tickets **11 to 30** (this week's class sheet used tickets 1 to 20). Rater **H** passes a reply only if its rubric score is **3**. Rater **J** passes it if the score is **2 or 3**. Here are the real rubric scores:

| Ticket | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Score | 3 | 1 | 3 | 2 | 1 | 2 | 3 | 1 | 3 | 2 | 1 | 2 | 3 | 1 | 3 | 2 | 1 | 2 | 3 | 1 |
| H (1 pass, 0 fail) | | | | | | | | | | | | | | | | | | | | |
| J (1 pass, 0 fail) | | | | | | | | | | | | | | | | | | | | |

**Part 1 (pen).**

(a) Tally:

| | H pass | H fail |
|---|:--:|:--:|
| **J pass** | | |
| **J fail** | | |

(b) `p_o = (both pass + both fail) / 20 =` ______
(c) J passes ___ of 20 = ______ · H passes ___ of 20 = ______
(d) `p_e = (J pass rate × H pass rate) + (J fail rate × H fail rate) = (____ × ____) + (____ × ____) =` ______
(e) `κ = (p_o − p_e) / (1 − p_e) = (____ − ____) / (1 − ____) =` ______
(f) Look at the two off-diagonal cells. Which way does J lean? ______ Is that the same way as in the class sheet? ______

**Part 2 (pen, then computer): a grid you build.** A different pair of raters gives this tally on 20 replies:

| | H pass | H fail |
|---|:--:|:--:|
| **J pass** | 9 | 3 |
| **J fail** | 2 | 6 |

Work out `p_o`, J's and H's pass rates, `p_e` and `κ` by hand: `p_o =` ______ · J passes ______ · H passes ______ · `p_e =` ______ · `κ =` ______

Now rebuild the two lists from the tally. The first nine entries are "both pass"; before you look, write what the next blocks must be:

```python
# grid_to_lists.py - Page 30.2 Part 2: a grid of counts turned back into two lists of 20, then the library.
H3 = [1] * 9 + [0] * 3 + [1] * 2 + [0] * 6
J3 = [1] * 9 + [1] * 3 + [0] * 2 + [0] * 6
print("lengths:", len(H3), len(J3), "| agreement:", sum(h == j for h, j in zip(H3, J3)) / 20)
print("library kappa:", round(cohen_kappa_score(H3, J3), 4))
```

Real output:

```text
lengths: 20 20 | agreement: 0.75
library kappa: 0.4898
```

(i) In the lists, the second block is `[0] * 3` for H and `[1] * 3` for J. Which cell of the tally is that, and why does it have those two values? ____________________________________________________________

(ii) Check Part 1 by running the block below, then compare with your `κ`.

```python
# kappa_window.py - Page 30.2 Part 1 check: the old bot's replies to tickets 11-30 (not 1-20), rated by the same two programs.
items2 = [(text, label, r1) for text, label, r1, r2 in pairs[10:30]]
print("scores, tickets 11-30:", [rubric(r, l) for _, l, r in items2])
H2w = [1 if rubric(r, l) == 3 else 0 for _, l, r in items2]
J2w = [1 if rubric(r, l) >= 2 else 0 for _, l, r in items2]
print("H:", H2w)
print("J:", J2w)
bp = sum(h == 1 and j == 1 for h, j in zip(H2w, J2w))
jh = sum(h == 0 and j == 1 for h, j in zip(H2w, J2w))
hj = sum(h == 1 and j == 0 for h, j in zip(H2w, J2w))
bf = sum(h == 0 and j == 0 for h, j in zip(H2w, J2w))
print("both pass", bp, "| J pass, H fail", jh, "| J fail, H pass", hj, "| both fail", bf)
print("library kappa:", round(cohen_kappa_score(H2w, J2w), 4))
```

Real output:

```text
scores, tickets 11-30: [3, 1, 3, 2, 1, 2, 3, 1, 3, 2, 1, 2, 3, 1, 3, 2, 1, 2, 3, 1]
H: [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
J: [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0]
both pass 7 | J pass, H fail 6 | J fail, H pass 0 | both fail 7
library kappa: 0.4495
```

**Part 3 (predict, then run): a judge that never fails anything.** The **new** bot's replies to tickets 1 to 20 score 2, 3, 3, 3, 2, 2 over and over (the pattern repeats every six tickets). H and J are the same two programs.

(a) Before you run: how many of the 20 will J pass? ______ How many will H pass? ______ Raw agreement will be ______ and `κ` will be ______ (use `p_e = J pass rate × H pass rate + J fail rate × H fail rate`).

```python
# v2_raters.py - Page 30.2 Part 3: the SAME two raters on the NEW bot's replies to tickets 1-20.
items_v2 = [(text, label, r2) for text, label, r1, r2 in pairs[:20]]
Hv = [1 if rubric(r, l) == 3 else 0 for _, l, r in items_v2]
Jv = [1 if rubric(r, l) >= 2 else 0 for _, l, r in items_v2]
print("scores:", [rubric(r, l) for _, l, r in items_v2])
print("H passes", sum(Hv), "of 20 | J passes", sum(Jv), "of 20")
print("raw agreement:", sum(h == j for h, j in zip(Hv, Jv)) / 20)
print("library kappa:", cohen_kappa_score(Hv, Jv))
```

Real output:

```text
scores: [2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3]
H passes 10 of 20 | J passes 20 of 20
raw agreement: 0.5
library kappa: 0.0
```

(b) Raw agreement is `0.5`. Is J doing any work on this set? Why does J's pass rate make `p_e` equal `p_o`? ____________________________________________________________

(c) The library prints `0.0`, not `nan`. When *would* it return `nan`? (Hint: `p_e` would be 1 and you would divide by `1 − p_e`.) ____________________________________________________________

---

## 🔁 Page 30.3 — Flips and a Weak Habit (homework · 25 min · pen first)

**Part 1 (pen, no computer).** The sealed judge is asked each question **twice**. Column A: v1 shown first. Column B: v2 shown first. The judge answers `A` (the reply shown first) or `B` (the reply shown second). This is the real output of the stand-in judge, seed 0, pairs **21 to 30** (this week's class sheet used pairs 11 to 20).

| Pair | Ticket | A: said | B: said | Winner in A | Winner in B | Same? |
|:--:|---|:--:|:--:|:--:|:--:|:--:|
| 21 | took the money twice on the 3rd | A | A | | | |
| 22 | swap me onto the yearly plan | B | A | | | |
| 23 | need a proper tax invoice | A | B | | | |
| 24 | what am I paying per month | A | A | | | |
| 25 | card expired, where do I put | A | B | | | |
| 26 | what's a good recipe for dosa? | B | A | | | |
| 27 | how tall is Mount Kilimanjaro? | A | A | | | |
| 28 | write my sister a birthday | B | A | | | |
| 29 | explain quantum entanglement | A | B | | | |
| 30 | should I buy bitcoin? | B | A | | | |

(a) In column A, `A` means v1 won and `B` means v2 won. In column B, `A` means **v2** won (it was shown first) and `B` means v1 won. Fill the two winner columns and `yes/no`.
(b) Flips (same = no): ______ of 10. Estimate of the bias = flips / 10 = ______
(c) How many of the 20 answers are `A`? ______ A judge with no habit says `A` about ______ times in 20.
(d) If you had run only column A, how many of the ten would say v1 wins? ______ If only column B, how many would say v1 wins? ______

Check your table with this (it prints the letters first, then the winners and the rubric):

```python
# sheet_21_30.py - Page 30.3 Part 1: the sealed judge, seed 0, pairs 21-30. It prints the two letters, then the winners behind them.
rng = random.Random(0)
rows = []
for i, (text, label, r1, r2) in enumerate(pairs):
    f = judge_pair(label, r1, r2, rng)
    r = judge_pair(label, r2, r1, rng)
    rows.append((i, text, f, r))
print("pair  ticket                           v1 first  v2 first")
for i, text, f, r in rows[20:30]:
    print(f"{i + 1:3d}   {text[:30]:30s}   {f}         {r}")
flips = first = 0
for i, text, f, r in rows[20:30]:
    label, r1, r2 = pairs[i][1], pairs[i][2], pairs[i][3]
    wf = "v1" if f == "A" else "v2"
    wr = "v2" if r == "A" else "v1"
    flips += wf != wr
    first += (f == "A") + (r == "A")
    rub = "v1" if rubric(r1, label) > rubric(r2, label) else "v2"
    print(f"{i + 1:3d}  {wf}  {wr}  {'same' if wf == wr else 'FLIP'}   rubric {rub}")
print("flips:", flips, "of 10 | 'A' answers:", first, "of 20")
```

Real output:

```text
pair  ticket                           v1 first  v2 first
 21   took the money twice on the 3r   A         A
 22   swap me onto the yearly plan     B         A
 23   need a proper tax invoice for    A         B
 24   what am I paying per month rig   A         A
 25   card expired, where do I put t   A         B
 26   what's a good recipe for dosa?   B         A
 27   how tall is Mount Kilimanjaro?   A         A
 28   write my sister a birthday mes   B         A
 29   explain quantum entanglement     A         B
 30   should I buy bitcoin?            B         A
 21  v1  v2  FLIP   rubric v2
 22  v2  v2  same   rubric v2
 23  v1  v1  same   rubric v1
 24  v1  v2  FLIP   rubric v2
 25  v1  v1  same   rubric v1
 26  v2  v2  same   rubric v2
 27  v1  v2  FLIP   rubric v2
 28  v2  v2  same   rubric v2
 29  v1  v1  same   rubric v1
 30  v2  v2  same   rubric v2
flips: 3 of 10 | 'A' answers: 13 of 20
```

(e) On the pairs that did **not** flip, how many times does the judge's winner agree with the rubric? ______ of ______. On the pairs that did flip, could the judge have been right in both orders? ______
(f) Ten pairs gave an estimate of ______; the 30-pair run of the chapter gave `0.267`; the planted number is `0.5`. One sentence: what does that spread say about one small test? ____________________________________________________________

**Part 2 (pen, then computer): how small a habit can thirty pairs see?** For the stand-in, the chance that a pair flips is the planted `bias`, and the chance the judge says `A` to any one question is `0.5 + bias/2`.

(a) Fill in for 60 answers (30 pairs, 2 orders) and 30 pairs:

| planted `bias` | expected `A` answers of 60 (`60 × (0.5 + bias/2)`) | expected flips of 30 (`30 × bias`) |
|:--:|:--:|:--:|
| 0.10 | | |
| 0.30 | | |
| 0.80 | | |

(b) Predict, for `bias = 0.10` and 20 seeds: the smallest flip rate will be about ______ and the largest about ______. Will any seed say "no bias at all"? ______

```python
# weak_bias.py - Page 30.3 Part 2: twenty seeds at each planted bias. One generator per TEST, a new seed per test. STAND-IN JUDGE, NOT A MODEL.
def flip_rate(bias, seed):
    rng = random.Random(seed)
    flips = 0
    for text, label, r1, r2 in pairs:
        fwd = judge_pair(label, r1, r2, rng, bias=bias)
        rev = judge_pair(label, r2, r1, rng, bias=bias)
        w_fwd = "v1" if fwd == "A" else "v2"
        w_rev = "v2" if rev == "A" else "v1"
        flips += w_fwd != w_rev
    return flips / len(pairs)

for b in (0.10, 0.25, 0.30, 0.80):
    ests = [flip_rate(b, s) for s in range(20)]
    print(f"planted {b:.2f}: smallest {min(ests):.2f}  largest {max(ests):.2f}  average {np.mean(ests):.3f}")
```

Real output:

```text
planted 0.10: smallest 0.03  largest 0.23  average 0.110
planted 0.25: smallest 0.13  largest 0.37  average 0.247
planted 0.30: smallest 0.13  largest 0.43  average 0.290
planted 0.80: smallest 0.63  largest 0.90  average 0.792
```

(i) The averages sit close to the planted numbers; single seeds do not. For `0.10`, could you call the habit "found" from one run of thirty pairs? What about `0.80`? ____________________________________________________________
(ii) The `0.10` run has a smallest value of `0.03`. Which is the smaller mistake: calling that "no bias", or calling the `0.10` run's `0.23` a bias of about a quarter? ____________________________________________________________
(iii) Can thirty pairs tell `0.10` from `0.25` on one run? What would you change to make the test steadier? ____________________________________________________________

**Part 3 (predict, then run): a judge the swap test cannot catch.** A different stand-in picks the **longer** reply (more words) every time, whichever is shown first. Nothing in it uses a random number.

(a) Predict: its flip rate on the 30 pairs will be ______. Its first-position win rate will be about ______. Will it agree with the rubric?

```python
# longer_judge.py - Page 30.3 Part 3: a second stand-in whose flaw is "the longer reply wins". STAND-IN, NOT A MODEL.
def longer_judge(label, a, b, rng):
    return "A" if len(a.split()) >= len(b.split()) else "B"

flips = agree = ties = 0
for text, label, r1, r2 in pairs:
    fwd = longer_judge(label, r1, r2, None)
    rev = longer_judge(label, r2, r1, None)
    w_fwd = "v1" if fwd == "A" else "v2"
    w_rev = "v2" if rev == "A" else "v1"
    flips += w_fwd != w_rev
    ties += len(r1.split()) == len(r2.split())
    rub = "v1" if rubric(r1, label) > rubric(r2, label) else "v2"
    agree += w_fwd == rub
print("flips:", flips, "of 30 | pairs of equal length:", ties, "| agrees with the rubric:", agree, "of 30")
```

Real output:

```text
flips: 0 of 30 | pairs of equal length: 0 | agrees with the rubric: 5 of 30
```

(b) Zero flips. Does that mean the judge is good? ______ How many of 30 does it get right against the rubric? ______ Which check (from Page 30.2) would have caught it? ____________________________________________________________
(c) Finish with three sentences: what the swap test shows, what it cannot show, and what today says about a real judge. ____________________________________________________________

---

## 🐞 Page 30.4 — Break It on Purpose (three bugs · 15 min, in class or at home)

Each block below is **DELIBERATELY wrong**. Predict, run, then write what it meant and the fix. Run them in the same session as the chapter, so `H` and `J` are the ones from the chapter's Block P6.

### 30.4-A (SILENT) — luck forgets one term

```python
# break_a.py - DELIBERATE BUG 30.4-A (SILENT): luck forgets the fail-fail term.
j_rate = sum(J) / 20
h_rate = sum(H) / 20
p_o = sum(h == j for h, j in zip(H, J)) / 20
p_e_wrong = j_rate * h_rate
print(f"p_o {p_o:.2f}  p_e {p_e_wrong:.3f}  kappa {(p_o - p_e_wrong) / (1 - p_e_wrong):.3f}   library: {cohen_kappa_score(H, J):.3f}")
p_e = j_rate * h_rate + (1 - j_rate) * (1 - h_rate)
print(f"fixed: p_e {p_e:.3f}  kappa {(p_o - p_e) / (1 - p_e):.3f}")
```

(i) The correct `p_e` for these raters is `0.44`. Will the wrong one be higher or lower? Will `κ` come out higher or lower? ______

(ii) Run it. Did the code raise an error? ______ What are the two kappas? ______ and ______ What is the only thing that revealed the mistake? ____________________________________________________________

(iii) Write the fix: ____________________________________________________________

### 30.4-B (SILENT) — reading the swapped answer the wrong way round

```python
# break_b.py - DELIBERATE BUG 30.4-B (SILENT): in the swapped order, "A" is v2, but the winner is read as v1.
rng = random.Random(0)
flips_wrong = 0
flips_right = 0
for text, label, r1, r2 in pairs:
    fwd = judge_pair(label, r1, r2, rng)
    rev = judge_pair(label, r2, r1, rng)
    w_fwd = "v1" if fwd == "A" else "v2"
    w_rev_wrong = "v1" if rev == "A" else "v2"       # the bug
    w_rev = "v2" if rev == "A" else "v1"
    flips_wrong += w_fwd != w_rev_wrong
    flips_right += w_fwd != w_rev
print("flips with the bug:", flips_wrong, "of 30 | flips, fixed:", flips_right, "of 30")
```

(i) The chapter's run of this seed found 8 flips in 30, so 22 consistent pairs. Predict the buggy count: ______ (Hint: when the bug is present, a consistent pair looks like what?)

(ii) Run it. The buggy estimate of the planted bias is ______ (true value `0.5`). Would a reader who trusts this number be badly wrong, or only a bit? ____________________________________________________________

(iii) Explain in words why "A" in the second question means v2. Write the fix. ____________________________________________________________

### 30.4-C (loud) — "in either" written as a plus

```python
# break_c.py - DELIBERATE BUG 30.4-C (loud): "in either" written as a plus.
a, b = "what am I paying per month right now?", "what am I paying each month right now?"
A, B = words(a), words(b)
try:
    print(len(A & B) / len(A + B))
except TypeError as e:
    print("ERR", type(e).__name__ + ":", e)
print(len(A & B) / len(A | B))
```

(i) Which operator is "the words in both"? ______ Which is "the words in either"? ______

(ii) Run it. What does the message say about `+` and about the two types? ____________________________________________________________ What is the Jaccard once it is fixed? ______

(iii) If `A` and `B` had been **lists**, `A + B` would have worked and divided by the wrong number. What would it count that a set does not? ____________________________________________________________

---

## 📓 Page 30.5 — The Bug Log

Add **at least two** entries, one of them SILENT. Then copy this sentence in your own handwriting on the last line of the page:

> **"The eval was written first and fingerprinted, the free rules beat my model, my scan cannot see a paraphrase, kappa takes luck out of agreement, and the pairwise judge changes its mind when I swap the order, so I do not trust a single-order verdict. The judge is a stand-in, so its habit says nothing about a real model."**

| # | File / page | What I saw | What it meant | The fix | How I would catch it next time |
|:--:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## 🧠 Self-Check (from memory, no notes)

1. What does a fingerprint of the eval set do when a ticket is edited? What does it not do? ____________________________________________________________
2. Why is a trained model compared with the free rules and not only with the floor? ____________________________________________________________
3. The scan removed two tickets and missed five paraphrases. Why can word overlap not see a paraphrase? ____________________________________________________________
4. Write `κ` in words: what is the top, what is the bottom? ____________________________________________________________
5. A rater says "pass" to everything on a set where most things pass. What are its raw agreement and its kappa? ____________________________________________________________
6. Why does a 0.4-kappa summary hide something that the two off-diagonal cells show? ____________________________________________________________
7. Why is "v1 wins" from one single-order run not a verdict? ____________________________________________________________
8. A judge never flips when the order is swapped. Can you conclude it is good? ____________________________________________________________
9. What does the flip rate of the sealed judge tell you about a real judge model? ____________________________________________________________

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up

1. An eval written after the system is written to flatter it. The fingerprint is a short code computed from the 30 cases at freeze time; after any edit, even one character, the assert fails and the edit is loud. It **cannot stop** an edit; it only makes one visible.
2. **Nothing is wrong.** `21/30` against `25/30` is the measured result. The order of work is: write the eval first, score the cheap baselines, and only then decide the fancier system earned its complexity.
3. **Against what?** Luck can give 90 percent (a rater that never looks, on a set where 18 of 20 pass). Find the agreement expected by chance, or compute kappa.
4. A script imitating a model, not a model. Its flip rate is a property of a number typed into the file (`BIAS = 0.5`); it was never a language model, so it says nothing about how often a real judge model behaves any way at all.

### Page 30.1

**Part 1.** Row 1: in both `put, the, money, back, on, my, card` (7), in either those seven plus `cancel, order, 7781, and` (11): `7/11 = 0.636`. Row 2: in both `does, nothing` (2); in either `the, export, button, does, nothing, clicking, save, absolutely` (8): `2/8 = 0.250`. Row 3: `don't` becomes `don` and `t`. In both `charge, me, twice` (3); in either `don, t, charge, me, twice, did, you` (7): `3/7 = 0.429`. Row 4: no words, `0/0`.

(a) The formula divides by zero (`0 / 0`), a `ZeroDivisionError`. `if (A | B)` is false for an empty set, so the function returns `0.0` instead.
(b) At `0.60`: pair 1 only (`0.636`). At `0.40`: pairs 1 and 3 (`0.429`; pair 2 at `0.250` stays).
(c) Pair 3: `don't charge me twice` and `did you charge me twice?` ask different things (do not charge me; did you charge me), but they share `charge`, `me`, `twice`, which are most of the content words in such short tickets. Short tickets overlap a lot by accident.

```text
in both 7 | in either 11 | Jaccard 0.636   'put the money back on my card'
in both 2 | in either 8 | Jaccard 0.250   'the export button does nothing'
in both 3 | in either 7 | Jaccard 0.429   "don't charge me twice"
in both 0 | in either 0 | Jaccard 0.000   '???'
```

**Part 2.** The first key that fires, ticket by ticket (greeting is checked first, and a key counts if it appears *anywhere inside* the ticket):

| # | Key fires | Label | Right? |
|:--:|---|---|:--:|
| 1 | `hi` | greeting | yes |
| 2 | `evening` | greeting | yes |
| 3 | `money back` | refund | yes |
| 4 | `hi` (inside `this`) | greeting | **no** |
| 5 | `loading` | technical | yes |
| 6 | `hi` (inside `nothing`) | greeting | **no** |
| 7 | `charge` (inside `charged`) | billing | yes |
| 8 | `plan` | billing | yes |
| 9 | none | out_of_scope | yes |
| 10 | `hi` (inside `which`) | greeting | **no** |

Score `7/10 = 0.7`, lower than `0.833`.

(i) The key `hi`, hiding inside **`this`** (ticket 4), **`nothing`** (6) and **`which`** (10). It is a substring test, so the greeting key fires on any word that contains those two letters, and greeting is checked first.
(ii) **No, it is a hint, not a proof.** One ticket is `0.1` on ten tickets, so the gap of `0.133` is about one and a third tickets. You would need many more tickets, written by several people, before putting a number on the gap. The honest reading is: the frozen score was probably a bit flattered (the author wrote the rules after seeing the eval), but ten tickets cannot size it.
(iii) No: `0.25` is far under any sensible threshold, so none is a copy of a frozen ticket. The scan compares words, not meaning, so it would not see a ticket that is a reworded copy of a frozen one.

**Part 3.** Any honest numbers. Common misses are `hi` inside a longer word and a ticket with no key. If your hits are all 10, read your tickets: did you write them while looking at the keys?

```text
(your own output: a fingerprint, hits/10, the highest Jaccard)
```

### Page 30.2

**Part 1.** H passes on tickets `11, 13, 17, 19, 23, 25, 29` (score 3); J passes on every ticket **except** `12, 15, 18, 21, 24, 27, 30` (score 1).
(a) `J pass / H pass 7`, `J pass / H fail 6`, `J fail / H pass 0`, `J fail / H fail 7`.
(b) `p_o = (7 + 7) / 20 = 0.70`.
(c) J passes `13` of 20 (`0.65`); H passes `7` of 20 (`0.35`).
(d) `p_e = (0.65 × 0.35) + (0.35 × 0.65) = 0.2275 + 0.2275 = 0.455`.
(e) `κ = (0.70 − 0.455) / (1 − 0.455) = 0.245 / 0.545 = 0.4495` (to three places `0.450`; matches the library's `0.4495`).
(f) J is **lenient**: it passes `6` replies H fails and never fails one H passes. Yes, the same way as in class (there, `7` and `0`).

**Part 2.** `p_o = (9 + 6) / 20 = 0.75`; J passes `12` of 20 (`0.60`); H passes `11` of 20 (`0.55`); `p_e = 0.60 × 0.55 + 0.40 × 0.45 = 0.33 + 0.18 = 0.51`; `κ = (0.75 − 0.51) / (1 − 0.51) = 0.24 / 0.49 = 0.4898`.
(i) The cell "J pass, H fail" (3 replies): H says `0` and J says `1` on each. The next block, `[1] * 2` for H and `[0] * 2` for J, is the opposite cell, "J fail, H pass" (2 replies).
(ii) The first check prints `0.4495` and matches Part 1.

**Part 3.** (a) J passes `20` of 20 (every score is 2 or 3); H passes `10` of 20 (the score-3 tickets). Raw agreement `10/20 = 0.5`. `p_e = 1.0 × 0.5 + 0.0 × 0.5 = 0.5`, so `κ = (0.5 − 0.5) / (1 − 0.5) = 0`.
(b) **No.** J says "pass" without looking; the only agreement it can get is H's pass rate, and that is exactly the agreement luck gives, so `p_o = p_e` and `κ = 0`. Raw `0.5` looks like "sometimes right", while the real skill is zero.
(c) When **both** raters say one thing only and the same thing (for instance two lists of all 1s). Then `p_e = 1` and the denominator is `0`. The library warns and returns `nan`.

### Page 30.3

**Part 1.** (a) Winners in A / in B / same?: `21`: v1 / v2 / **no** · `22`: v2 / v2 / yes · `23`: v1 / v1 / yes · `24`: v1 / v2 / **no** · `25`: v1 / v1 / yes · `26`: v2 / v2 / yes · `27`: v1 / v2 / **no** · `28`: v2 / v2 / yes · `29`: v1 / v1 / yes · `30`: v2 / v2 / yes.
(b) `3` of 10; estimate `0.30`.
(c) `13` of 20 answers are `A`: column A has `A` on pairs 21, 23, 24, 25, 27, 29 (`6`); column B has `A` on pairs 21, 22, 24, 26, 27, 28, 30 (`7`). A judge with no habit says `A` about `10` times.
(d) Column A alone: v1 wins in `6` of the ten (21, 23, 24, 25, 27, 29); column B alone: v1 wins in `3` (23, 25, 29).
(e) All `7` non-flipping pairs agree with the rubric (`22, 23, 25, 26, 28, 29, 30`). On a flipped pair the judge changed its mind on the same two replies, so it cannot have been right in both orders.
(f) `0.30` from ten pairs; `0.267` from thirty; planted `0.5`. Any sentence that says a small test is one draw and can land well away from the truth; use more pairs or repeat with fresh draws.

**Part 2.** (a) `bias 0.10`: expected `A` answers `60 × 0.55 = 33`, expected flips `3`. `0.30`: `60 × 0.65 = 39`, flips `9`. `0.80`: `60 × 0.90 = 54`, flips `24`.
(b) Roughly: smallest 0.0 to 0.1, largest 0.2 to 0.3 (the real run: `0.03` and `0.23`). No seed says "no bias at all": with a real habit of `0.10`, the real smallest flip rate is `0.03`, not `0`.
(i) **No for `0.10`**: one run can land on `0.03` or on `0.23`, so it is close to the truth only by luck of the draw. For `0.80`, yes: every seed is at least `0.63`, far from "no habit". A big habit is found on one run, a small one is only seen on average.
(ii) Calling `0.03` "no bias" is the worse mistake, because a habit is there (an honest judge gives exactly `0.00`, as the control in the lesson showed). Calling `0.23` a quarter overstates the size but still gets the direction right.
(iii) **No**: the ranges of `0.10` (`0.03` to `0.23`) and `0.25` (`0.13` to `0.37`) overlap, so one run cannot tell them apart. Ask many more pairs (the same 30 tickets asked many times with fresh draws), which cuts the spread to about a third.

**Part 3.** (a) Flip rate `0`: the longer reply is the longer reply in both orders, so the winner never changes. First-position win rate `0.5` (half the time the longer reply is shown first). It will **not** agree with the rubric except by accident.
(b) **No.** It gets `5` of 30 right against the rubric, because in these pairs the longer reply is usually the one with the promise or the filler, which the rubric penalises. **Agreement with trusted labels** (kappa against the rubric) would have caught it; the swap test cannot see a flaw that is the same in both orders.
(c) Model answer: *Swapping the order finds a position habit, because an honest judge gives the same winner both ways. It cannot find a judge that is consistently wrong, like one that always prefers the longer reply. Today measured a number typed into a stand-in and says nothing about real judges; the thing to take away is the method (freeze a test, swap the order, count the flips, and check against labels you trust).*

### Page 30.4

**A (SILENT).** (i) Lower; `κ` higher. (ii) **No error.** `p_e 0.245`, `κ 0.536` against the library's `0.375`: `0.536` is too high because the luck of agreeing on "fail" was dropped. The only thing that revealed it was comparing with `cohen_kappa_score`. (iii) Add the fail-fail term: `p_e = j_rate * h_rate + (1 - j_rate) * (1 - h_rate)`.

```text
p_o 0.65  p_e 0.245  kappa 0.536   library: 0.375
fixed: p_e 0.440  kappa 0.375
```

**B (SILENT).** (i) `22`: with the bug, every pair that is really **consistent** looks like a flip, and every real flip looks consistent; `30 − 8 = 22`. (ii) `22` of 30, so an estimate of `0.733` against the true `0.5`. The buggy count is always `30` minus the real flips, so a weak habit (few real flips) would read as a strong one. (iii) In the swapped question the reply shown first is **v2**, so `A` means v2 won and `B` means v1 won: `w_rev = "v2" if rev == "A" else "v1"`.

```text
flips with the bug: 22 of 30 | flips, fixed: 8 of 30
```

**C (loud).** (i) `&` is in both; `|` is in either. (ii) `TypeError: unsupported operand type(s) for +: 'set' and 'set'`: sets do not add. Fixed: `7/9 = 0.778`. (iii) A list keeps repeats and adds the two lists end to end, so `len(A + B)` counts every word twice when it appears in both, which gives `len(A) + len(B)`; a set counts a shared word once.

```text
ERR TypeError: unsupported operand type(s) for +: 'set' and 'set'
0.7777777777777778
```

### Page 30.5 and Self-Check

**Bug Log.** Any two honest entries. Model answers: *30.4-A: "kappa 0.536 looks fine" / luck was computed with only one of its two terms / add the fail-fail term / always print the library value beside my hand value.* *30.4-B: "22 flips" / a flip and a consistent pair swapped places because "A" means a different reply in the second order / `w_rev = "v2" if rev == "A" else "v1"` / check the answer against a control judge with `bias=0.0` that must give 0 flips.*

1. It makes the edit loud: the assert on the fingerprint fails. It does not prevent the edit or say which ticket changed.
2. The floor is too easy to beat. A cheap, free system that ignores language is the real test of whether the extra work earned its cost.
3. The scan compares the words two tickets share. A paraphrase shares almost none (highest Jaccard `0.200` for the five), so it has nothing to find.
4. Top: how often they actually agree minus how often luck would make them agree. Bottom: `1` minus how often luck would make them agree. It is the share of the possible improvement over luck that they achieved.
5. Raw agreement is the human's pass rate (for example `0.90`), and `κ = 0`.
6. A single number does not say which way the raters differ. In the grid on Page 30.2 J never fails what H passes but passes a number of replies H fails: J leans lenient.
7. The order of the two replies is pulling the answer toward whichever is shown first; one run is one draw. The consistent-pairs verdict uses both orders.
8. **No.** It only shows there is no position habit. A judge that is consistently wrong in both orders passes the swap test, as `longer_judge` did (`0` flips, `5` of 30 right).
9. **Nothing.** It is a property of the number `0.5` typed into `mystery.py`. What transfers is the test: swap the order and count the flips.
