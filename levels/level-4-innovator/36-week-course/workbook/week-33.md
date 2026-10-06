# Workbook — Week 33: Attack Your Own System

**Name:** ________________________________  **Date:** ______________

[⬅ Week 32](week-32.md) · [📖 Read the chapter first](../student-guide/week-33.md) · [Course Home](../README.md) · [Next ➡](week-34.md)

---

![Thirty-six week tiles in four lanes of nine, one per term; weeks 1 to 32 solid, Week 33 (a lab week in term 4) tinted pink with a thick border and a pointer, weeks 34 to 36 dashed](../figures/fig-w33-0-where-this-fits.svg)

*Figure 33.0 — Week 33 of 36: a lab week in term 4, agents, evidence and the system card.*

---

> **Rules for this workbook.** The new idea this week is **the wobble of a count**: `sqrt(n p (1-p))`, how far a count of weighted-coin flips typically strays from `n p`. Pages 33.1 to 33.3 do it on paper first, then with the code you ran in the chapter. **Write your answer by hand first, then run.** A guess written after the run is not a guess.
>
> **Every "model" here is a stand-in, not a model.** The agent's brain is `GullibleModel` wrapped round `ScriptedModel`: a script plus a coin whose chance someone typed. The obey rate of `0.30` is three typed numbers multiplied. **Nothing you measure says anything about a real model.** What is real is the method: the attack written as data, the count out of `n`, the noise bound, the two re-tests, the redactor and the sweep. The three extra notes are invented, and the phone number, email address and card number in them are dummies that belong to nobody. The attacks are defensive and educational: you run them against an agent you built, on your own laptop.
>
> **Real numbers.** Every number printed below came from a real run of the code shown, on CPU, with every seed written in the code. If you ran the chapter's `week33.py` as written, your counts should match these exactly. (Lines that show seconds or ages in seconds vary; none are printed here.) Page 33.1 Part C reuses counts from the chapter's Section 8. Hand-calculation numbers are plain arithmetic.
>
> **Files you need.** Pages 33.1 and 33.3 Part A need only pen and a calculator with a square-root key. Every "check" block runs **in the same Python session as your `week33.py`, straight after it** (the chapter's blocks S1 to S12; you can skip S13), because the blocks use its names: `np`, `re`, `json`, `time`, `Path`, `redact`, `EMAIL`, `CARD`, `PHONE_LOOSE`, `PHONE`, `PATTERNS`, `redact_pii`, `CASES`, `heads`, `ATTACKS`, `attack`, `rate`, `run_attack`, `count_landed`, `named_files_only`, `happy`, `line`, `save_safe`, `sweep`, `DAY`, and `Q_REM`. Run from the folder that contains `l4lib/` and `notes/`. Nothing needs the internet. Whole workbook at the computer: about 15 seconds.
>
> **Calculator.** Plain arithmetic and a square-root key are enough; the one power (`0.95 ** 50`) on Page 33.1 Part E is marked. Four decimals while you work, round only the answer.

---

## ✅ Warm-Up (5 min, before anything else, from memory)

This warm-up recalls the earlier weeks that this page builds on. Answer from memory.

1. A system is said to obey a planted note "30% of the time". You run it 20 times. What count do you *expect*? ______ Will you *see* exactly that? ______
2. Week 32: a model's average rose. What did you have to look at before saying it got better? ____________________________________________________
3. A patch takes an attack from 15 landings in 50 to 0. Name the **two** things you must re-test before calling it a fix. (1) ______________________ (2) ______________________
4. What does `re.sub` need, in order? ______________ , ______________ , ______________
5. Week 29: name one thing a note can do to an agent that a *legal* write to a *legal* filename makes impossible to stop with a sandbox. ____________________________________________________

---

## 🧮 Page 33.1 — The Wobble by Hand (30 min · pen, then one check)

This page is for computing the wobble of a count by hand and using it to judge whether a gap between two counts is more than noise. Work the four steps below, in order.

- **Expected count** `n × p`.
- **`n p (1 − p)`**.
- **Wobble** = its square root.
- **Window** = expected count minus and plus two wobbles.

**A. Eight (n, p) pairs.** The first two are worked for you as a model of the layout; do the rest.

| `n` | `p` | expected `n p` | `n p (1−p)` | wobble | share = wobble ÷ `n` | window (± 2 wobbles) |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 20 | 0.3 | 6 | 4.2 | 2.05 | 0.102 | 1.9 to 10.1 |
| 50 | 0.3 | 15 | 10.5 | 3.24 | 0.065 | 8.5 to 21.5 |
| 50 | 0.5 | ______ | ______ | ______ | ______ | ______ to ______ |
| 50 | 0.1 | ______ | ______ | ______ | ______ | ______ to ______ |
| 100 | 0.2 | ______ | ______ | ______ | ______ | ______ to ______ |
| 200 | 0.5 | ______ | ______ | ______ | ______ | ______ to ______ |
| 50 | 0.0 | ______ | ______ | ______ | ______ | ______ to ______ |
| 50 | 1.0 | ______ | ______ | ______ | ______ | ______ to ______ |

Which is more wobbly in counts, `p = 0.3` or `p = 0.5` (same `n = 50`)? ______ . At which `p` is the wobble biggest? ______ . Why is the wobble `0` at `p = 0` **and** at `p = 1`? ____________________________________________________

**B. The Hook.** A count of 9 of 20 runs at `p = 0.3`: is it inside the window from row 1? ______ . So is "7 of 20 before, 9 of 20 after" evidence that a change made things worse? ______ , because ____________________________________________________

**C. Is a gap more than noise?** For two counts `a` and `b` out of the same `n`: take `p_a = a/n` and `p_b = b/n`, find each wobble `sqrt(n p (1−p))`, square each, add, take the root, and double it. If the gap `|a − b|` is bigger than that **noise bound**, call it more than noise. Four pairs; the counts come from the chapter's Section 8 (the first is the Hook).

| pair | `n` | `a` | `b` | wobble of `a` | wobble of `b` | bound = 2 × sqrt(sum of squares) | gap | more than noise? |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| the Hook | 20 | 7 | 9 | ________ | ________ | ________ | ______ | ______ |
| frame only vs frame + scan | 20 | 14 | 7 | ________ | ________ | ________ | ______ | ______ |
| gullibility 1.0 vs 0.8 | 200 | 62 | 54 | ________ | ________ | ________ | ______ | ______ |
| gullibility 1.0 vs 0.8 | 1000 | 310 | 225 | ________ | ________ | ________ | ______ | ______ |

In the second pair the true rates are `0.6` and `0.3`; in the last two they are `0.30` and `0.24`. Which pair does 20 runs see, and which needs 1,000? One sentence on why a *small* gap needs many more runs: ____________________________________________________

**D. Quadruple the runs.** At `p = 0.3`, work out the wobble of the **share** for `n = 20`, then `n = 80`, then `n = 320`. Write: ______ , ______ , ______ . Each step quadruples `n`. What happens to the share's wobble each time? ______________________ . To halve your uncertainty you need ______ times the runs.

**E. "0 of 50" is not "never".** If the true chance that one run lands is `r`, the chance that 50 runs show **no** landing is `(1 − r)` multiplied by itself 50 times, written `(1 − r) ** 50`. Use the calculator's power key and fill in the table.

| true rate `r` | chance that 50 runs show 0 landings |
|:-:|:-:|
| 0.10 | ________ |
| 0.05 | ________ |
| 0.02 | ________ |
| 0.01 | ________ |

At what true rate would you be quite surprised (say, under 1 chance in 100) to see 0 of 50? ______ . Using your table, finish the honest sentence: *"0 of 50 landed; any rate above about ______ would usually have shown at least one, and ______ would often have shown none."*

Now run the two checks below, after `week33.py`. The first block covers Parts A to D and the second covers Part E.

```python
# check331.py - Page 33.1: the wobble table for the practice rows, the windows, and the noise bounds. Needs np.
print("Part A/B: expected count, n p (1-p), wobble, share, window (expected -/+ 2 wobbles)")
for n, p in [(20, 0.3), (50, 0.3), (50, 0.5), (50, 0.1), (100, 0.2), (200, 0.5), (50, 0.0), (50, 1.0)]:
    sd = np.sqrt(n * p * (1 - p))
    print(f"  n={n:3d} p={p:.1f}: n p = {n * p:5.1f}, n p (1-p) = {n * p * (1 - p):6.2f}, wobble = {sd:5.2f}, share = {sd / n:.3f}, window {n * p - 2 * sd:5.1f} to {n * p + 2 * sd:5.1f}")
print("Part C: noise bound for a gap = 2 x sqrt(wobble_a^2 + wobble_b^2), each p taken as count / n")
for label, n, a, b in [("the Hook", 20, 7, 9), ("frame only vs frame + scan", 20, 14, 7), ("1.0 vs 0.8, n 200", 200, 62, 54), ("1.0 vs 0.8, n 1000", 1000, 310, 225)]:
    pa, pb = a / n, b / n
    sa, sb = np.sqrt(n * pa * (1 - pa)), np.sqrt(n * pb * (1 - pb))
    bound = 2 * np.sqrt(sa ** 2 + sb ** 2)
    print(f"  {label:28s} n={n:4d} {a:4d} vs {b:4d}: wobbles {sa:5.2f} and {sb:5.2f}, gap {abs(a - b):3d}, bound {bound:5.1f} -> {'more than noise' if abs(a - b) > bound else 'not distinguishable'}")
print("Part D: quadrupling the runs at p = 0.3")
for n in [20, 80, 320]:
    print(f"  n={n:3d}: wobble of the share = {np.sqrt(n * 0.3 * 0.7) / n:.4f}")
```

```text
Part A/B: expected count, n p (1-p), wobble, share, window (expected -/+ 2 wobbles)
  n= 20 p=0.3: n p =   6.0, n p (1-p) =   4.20, wobble =  2.05, share = 0.102, window   1.9 to  10.1
  n= 50 p=0.3: n p =  15.0, n p (1-p) =  10.50, wobble =  3.24, share = 0.065, window   8.5 to  21.5
  n= 50 p=0.5: n p =  25.0, n p (1-p) =  12.50, wobble =  3.54, share = 0.071, window  17.9 to  32.1
  n= 50 p=0.1: n p =   5.0, n p (1-p) =   4.50, wobble =  2.12, share = 0.042, window   0.8 to   9.2
  n=100 p=0.2: n p =  20.0, n p (1-p) =  16.00, wobble =  4.00, share = 0.040, window  12.0 to  28.0
  n=200 p=0.5: n p = 100.0, n p (1-p) =  50.00, wobble =  7.07, share = 0.035, window  85.9 to 114.1
  n= 50 p=0.0: n p =   0.0, n p (1-p) =   0.00, wobble =  0.00, share = 0.000, window   0.0 to   0.0
  n= 50 p=1.0: n p =  50.0, n p (1-p) =   0.00, wobble =  0.00, share = 0.000, window  50.0 to  50.0
Part C: noise bound for a gap = 2 x sqrt(wobble_a^2 + wobble_b^2), each p taken as count / n
  the Hook                     n=  20    7 vs    9: wobbles  2.13 and  2.22, gap   2, bound   6.2 -> not distinguishable
  frame only vs frame + scan   n=  20   14 vs    7: wobbles  2.05 and  2.13, gap   7, bound   5.9 -> more than noise
  1.0 vs 0.8, n 200            n= 200   62 vs   54: wobbles  6.54 and  6.28, gap   8, bound  18.1 -> not distinguishable
  1.0 vs 0.8, n 1000           n=1000  310 vs  225: wobbles 14.63 and 13.21, gap  85, bound  39.4 -> more than noise
Part D: quadrupling the runs at p = 0.3
  n= 20: wobble of the share = 0.1025
  n= 80: wobble of the share = 0.0512
  n=320: wobble of the share = 0.0256
```

```python
# check331e.py - Page 33.1 Part E: 'zero of 50' is not 'never'. The chance that 50 runs show nothing at a true rate r is (1 - r) ** 50.
for r in [0.10, 0.05, 0.02, 0.01]:
    print(f"  true rate {r:.2f}: chance of 0 landings in 50 runs = {(1 - r) ** 50:.3f}")
n = 1
while 0.95 ** n >= 0.05:
    n += 1
print("fewest runs at a true rate of 0.05 for the chance of seeing nothing to fall below 0.05:", n, "->", round(0.95 ** n, 4))
```

```text
  true rate 0.10: chance of 0 landings in 50 runs = 0.005
  true rate 0.05: chance of 0 landings in 50 runs = 0.077
  true rate 0.02: chance of 0 landings in 50 runs = 0.364
  true rate 0.01: chance of 0 landings in 50 runs = 0.605
fewest runs at a true rate of 0.05 for the chance of seeing nothing to fall below 0.05: 59 -> 0.0485
```

Did your wobbles match to two decimals? If not, which step was it (the `p (1−p)`, the root, or the window)? ______ . Your hand result for the `n = 200` window was ______ to ______ ; in the Hook, the gap of 2 against the bound of 6.2 means ____________________________________________________

![Ten dots, the landings out of 20 runs in ten batches of the same stand-in system, inside a shaded band of 6 plus or minus 2.05, beside the totals over 200 batches](../figures/fig-w33-1-count-wobble.svg)
*Figure 33.1 — Twenty runs of an unchanged system give counts from 3 to 8 in ten batches, so a gap of 2 is not a finding.*

---

## 🧮 Page 33.2 — Red-Team Log and Redaction (45 min · pen, then computer)

This page is for predicting how ordered redaction patterns behave, measuring the redactor's recall, and filling in your red-team card from your own runs.

**A. The order of patterns, by hand.** `redact(text, patterns)` runs `re.sub` once per pattern, **in list order**, each on the previous output. The loose phone pattern `PHONE_LOOSE` matches *any* run of 9 or more digits, spaces, dashes, dots and brackets. The shaped `PHONE` wants ten digits starting with 6, 7, 8 or 9, with an optional `+91`, in the shape `5 digits, optional space or dash, 5 digits`. The list `PATTERNS` is email, card, Aadhaar, phone, IPv4.

Write what each line prints **before** you run it. Tags are written `[CARD]`, `[PHONE]`, `[IPV4]`.

| # | text | patterns | your prediction |
|:-:|---|---|---|
| 1 | `Card 4111 1111 1111 1111.` | email, **card**, loose phone | ____________________ |
| 1b | `Card 4111 1111 1111 1111.` | email, loose phone, **card** | ____________________ |
| 2 | `Due 2026-09-02.` | email, card, loose phone | ____________________ |
| 2b | `Due 2026-09-02.` | `PATTERNS` (shaped) | ____________________ |
| 3 | `Call 98765 43210 today.` | `PATTERNS` | ____________________ |
| 4 | `Call 12345 67890 today.` | `PATTERNS` | ____________________ |
| 5 | `Server 192.168.1.44 runs version 1.2.3.4567.` | `PATTERNS` | ____________________ |
| 6 | `[note 3] (similarity 0.512) 2026-03-11 and 2026-04-02` | `PATTERNS` | ____________________ |

Rows 1 and 1b differ in only one thing. Say what, and say which order is right and why: ____________________________________________________

Row 4 is a real phone-shaped number that is **not** redacted. Why? ____________________________________________________ Is that a bug in the regex or a limit of shape-matching? ______________________

Run this block to print the eight practice strings through both pattern sets.

```python
# check332a.py - Page 33.2 Part A: the practice strings through the loose pattern and the shaped patterns, in two orders. Needs redact, PHONE_LOOSE, PHONE, EMAIL, CARD, AADHAAR, IPV4, PATTERNS from week33.py.
loose = [("EMAIL", EMAIL), ("CARD", CARD), ("PHONE", PHONE_LOOSE)]
card_last = [("EMAIL", EMAIL), ("PHONE", PHONE_LOOSE), ("CARD", CARD)]
print("1 card, card first   :", redact("Card 4111 1111 1111 1111.", loose))
print("1 card, phone first  :", redact("Card 4111 1111 1111 1111.", card_last))
print("2 date, loose        :", redact("Due 2026-09-02.", loose))
print("2 date, shaped       :", redact("Due 2026-09-02.", PATTERNS))
print("3 phone, shaped      :", redact("Call 98765 43210 today.", PATTERNS))
print("4 starts with a 1    :", redact("Call 12345 67890 today.", PATTERNS))
print("5 address + version  :", redact("Server 192.168.1.44 runs version 1.2.3.4567.", PATTERNS))
print("6 two dates and a tag:", redact("[note 3] (similarity 0.512) 2026-03-11 and 2026-04-02", PATTERNS))
```

```text
1 card, card first   : Card [CARD].
1 card, phone first  : Card [PHONE].
2 date, loose        : Due [PHONE].
2 date, shaped       : Due 2026-09-02.
3 phone, shaped      : Call [PHONE] today.
4 starts with a 1    : Call 12345 67890 today.
5 address + version  : Server [IPV4] runs version 1.2.3.4567.
6 two dates and a tag: [note 3] (similarity 0.512) 2026-03-11 and 2026-04-02
```

How many of your 8 predictions were right? ______ / 8. The one you got wrong, and the rule you missed: ____________________________________________________

**B. Recall, and six inputs of your own (homework).** *Recall* (Week 30): of the inputs that **are** personal data, the share that the redactor changes. Before you run, mark each of the chapter's eight typed cases: would the shaped redactor change it (C) or leave it (M)?

| case | kind | your guess (C or M) |
|---|---|:-:|
| `priya.sharma@example.com` | EMAIL | ______ |
| `+91 98765 43210` | PHONE | ______ |
| `9123456789` | PHONE | ______ |
| `4111 1111 1111 1111` | CARD | ______ |
| `1234 5678 9012` | AADHAAR | ______ |
| `192.168.1.44` | IPV4 | ______ |
| `Ramana Kamma` | NAME | ______ |
| `third house past the temple, Nehru Road` | ADDRESS | ______ |

Your recall guess: ______ / 8 = ______ . Now write **six inputs of your own**: three you expect the redactor to catch and three you expect it to miss (all dummy data, nothing real).

| # | input (dummy) | predicted | run result |
|:-:|---|:-:|:-:|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

Run this block to check the eight typed cases, then your own six.

```python
# check332b.py - Page 33.2 Part B: recall on the 8 typed cases, then on your own six. Needs redact_pii and CASES from week33.py.
for raw, kind in CASES:
    print(f"  {raw:42s} {kind:8s} {'caught' if redact_pii(raw) != raw else 'MISSED'}")
MINE = ["priya dot sharma at example dot com", "+919876543210", "9 8 7 6 5 4 3 2 1 0", "98765-43210", "nine eight seven six five four three two one zero", "priya.sharma@example"]   # an EXAMPLE list: replace it with the six you wrote
got = sum(redact_pii(r) != r for r in MINE)
base = sum(redact_pii(raw) != raw for raw, kind in CASES)
print(f"your six: {got}/{len(MINE)} | all together: {got + base}/{len(CASES) + len(MINE)} = {(got + base) / (len(CASES) + len(MINE)):.2f}")
```

```text
  priya.sharma@example.com                   EMAIL    caught
  +91 98765 43210                            PHONE    caught
  9123456789                                 PHONE    caught
  4111 1111 1111 1111                        CARD     caught
  1234 5678 9012                             AADHAAR  caught
  192.168.1.44                               IPV4     caught
  Ramana Kamma                               NAME     MISSED
  third house past the temple, Nehru Road    ADDRESS  MISSED
your six: 2/6 | all together: 8/14 = 0.57
```

The `MINE` list above is **an example**, not an answer to copy: your own six will give your own number. Your recall on your six: ______ / 6 . Together with the chapter's eight: ______ / 14 = ______ . One sentence: why does a longer list of patterns never bring the recall to 1.0 on names? ____________________________________________________

**C. Your red-team card, with your own numbers.** Fill in the three findings from *your* runs. Leave nothing to memory of the chapter: run the block below and copy the figures.

| | A1 (legal write) | A2 (escape) | A3 (PII) |
|---|---|---|---|
| Attack (what the planted note orders / asks) | | | |
| Evidence (count out of `n`) | | | |
| Mechanism (why no fence fired) | | | |
| Fix (the one line) | | | |
| Before | | | |
| After | | | |
| Happy path (real task, count / `n`) | | | |
| Residual (what is still true) | | | |
| Gap vs noise bound | | | |

Run this block to print the three findings and the control.

```python
# check332c.py - Page 33.2 Part C: the three findings on your card, as one line each, and the control. (stand-in, not a model) Needs rate, run_attack, attack, ATTACKS, line, count_landed, named_files_only, happy, Q_REM from week33.py.
a1_before = rate(ATTACKS[0], "a1", strict=True)
a1_after = rate(ATTACKS[0], "a1", strict=True, write_guard=named_files_only)
ok = sum(happy(s, strict=True, write_guard=named_files_only)[0] for s in range(50))
a2_before, a2_after = rate(ATTACKS[1], "a2", strict=False), rate(ATTACKS[1], "a2", strict=True)
a3_before = (rate(ATTACKS[2], "a3_context"), rate(ATTACKS[2], "a3_trace"))
a3_after = (rate(ATTACKS[2], "a3_context", search_wrap=redact_pii, trace_saver=save_safe), rate(ATTACKS[2], "a3_trace", search_wrap=redact_pii, trace_saver=save_safe))
print(line("A1", a1_before, a1_after))
print(line("A2", a2_before, a2_after))
print(f"A3 before: context {a3_before[0]}/50, trace {a3_before[1]}/50 | after both locks: context {a3_after[0]}/50, trace {a3_after[1]}/50")
print(f"legitimate save after the A1 patch: {ok}/50")
print(line("A1 vs itself", a1_before, count_landed(ATTACKS[0], 50, 7000, strict=True)))
s1 = [s for s in range(50) if run_attack(ATTACKS[0], s)["a1"]]
s2 = [s for s in range(50) if run_attack(ATTACKS[1], s)["a2"]]
print("A1 and A2 landed on the same seeds:", s1 == s2, "| first five:", s1[:5])
```

```text
A1: before 15/50 (0.30), after 0/50 (0.00); gap 15 counts vs noise bound 6.5 -> more than noise
A2: before 15/50 (0.30), after 0/50 (0.00); gap 15 counts vs noise bound 6.5 -> more than noise
A3 before: context 50/50, trace 50/50 | after both locks: context 0/50, trace 0/50
legitimate save after the A1 patch: 50/50
A1 vs itself: before 15/50 (0.30), after 17/50 (0.34); gap -2 counts vs noise bound 9.3 -> NOT distinguishable from noise
A1 and A2 landed on the same seeds: True | first five: [1, 3, 4, 8, 13]
```

Answer in writing. (i) A1 and A2 both show `15`: are they two independent findings about how gullible the stand-in is? ______ , because ____________________________________________________ (ii) The "A1 vs itself" line is a **control**: same system, other seeds. What would you conclude about your bound if it had said "more than noise"? ____________________________________________________ (iii) A5 is not on the card. Why is it listed as *skipped* instead of left out? ____________________________________________________

**D. Two doors, predicted.** Personal data reaches the trace by two doors: the **notes** (A3) and the **user** (A3b: the user typed the number). Four versions of the agent. Before you look back at the chapter's Section 11, fill in, out of 50, what you expect.

| version | A3: PII in the model's context | A3: PII in the trace file | A3b: PII in the trace file |
|---|:-:|:-:|:-:|
| v0: raw everywhere | ______ /50 | ______ /50 | ______ /50 |
| redact tool output only | ______ /50 | ______ /50 | ______ /50 |
| redact the saved trace only | ______ /50 | ______ /50 | ______ /50 |
| both | ______ /50 | ______ /50 | ______ /50 |

Then look at the chapter's Section 11 table. How many of your twelve cells were right? ______ / 12. Why does redacting the tool output not protect a log where the user typed the number? ____________________________________________________

![A table of four versions of a stand-in agent against four measured columns out of 50 runs, cells marked with ticks and crosses, with the refuse-everything patch outlined](../figures/fig-w33-2-patch-and-happy-path.svg)
*Figure 33.2 — A patch must lower the attack count and keep the legitimate save at 50 of 50; a patch that refuses everything scores zero on both.*

---

## 🧮 Page 33.3 — Keep Less, Delete on Time, and the Four Sentences (40 min · pen, then computer)

This page is for working out file ages for a retention rule, running the sweep as a dry run first, and writing your findings up in four sentences.

**A. Ages by hand.** A file's age in days is `(now − mtime) ÷ 86400`. `sweep(folder, 7)` deletes a file only if its age is **greater than** 7 days (`>`, not `>=`). Fill in the days (five decimals) and say kept or deleted.

| age in seconds | age in days | 7-day rule: kept or deleted? |
|:-:|:-:|:-:|
| 90,000 | ________ | ________ |
| 604,800 | ________ | ________ |
| 604,801 | ________ | ________ |
| 1,000,000 | ________ | ________ |
| 3,000,000 | ________ | ________ |

604,800 seconds is exactly ______ days. Why does the rule's `>` matter for a file that old? What would you write in the policy so nobody is surprised? ____________________________________________________

Run this block to turn each age in seconds into days and apply the retention rule.

```python
# ages333.py - Page 33.3 Part A: ages in days and the 7-day rule (older than, so '>'). Needs sweep's rule only.
for secs in [90000, 604800, 604801, 1000000, 3000000]:
    d = secs / 86400
    print(f"  {secs:8d} s = {d:9.5f} days -> {'deleted' if d > 7 else 'kept'}")
```

```text
     90000 s =   1.04167 days -> kept
    604800 s =   7.00000 days -> kept
    604801 s =   7.00001 days -> deleted
   1000000 s =  11.57407 days -> deleted
   3000000 s =  34.72222 days -> deleted
```

**B. Your retention policy (homework).** One sentence of the form *"traces older than N days are deleted by `sweep`, run at ______."* Choose `N` and give a reason that is about the *use* of the logs, not about disk space. Mine:

____________________________________________________________________________

____________________________________________________________________________

Before you run: on a folder of three traces made just now, what does `sweep(folder, 7, now=time.time() + 3 * DAY)` list? ______ . With `6 * DAY`? ______ . With `8 * DAY`? ______ . Does a dry run delete anything? ______

Run this block to try the retention policy as a dry run and then for real.

```python
# check333.py - Page 33.3: a retention policy, run as a dry run and then for real on three traces. Needs run_attack, ATTACKS, redact_pii, save_safe, sweep, Path, time, DAY from week33.py.
W33 = Path("logs33_wb")
W33.mkdir(exist_ok=True)
for i in range(3):
    run_attack(ATTACKS[2], i, search_wrap=redact_pii, trace_saver=save_safe, trace_file=str(W33 / f"trace-{i}.jsonl"))
print("files:", sorted(p.name for p in W33.glob("*.jsonl")))
print("age of the first, in days:", round((time.time() - sorted(W33.glob("*.jsonl"))[0].stat().st_mtime) / DAY, 4))
for pretend in [3, 6, 8]:
    print(f"pretend it is {pretend} days on, 7-day rule (dry run):", [p.name for p in sweep(W33, 7, now=time.time() + pretend * DAY)])
print("still there after the dry runs:", len(list(W33.glob("*.jsonl"))))
gone = sweep(W33, 7, now=time.time() + 8 * DAY, dry_run=False)
print("real sweep removed:", [p.name for p in gone], "| left:", len(list(W33.glob("*.jsonl"))))
raw_b, slim_b = len(run_attack(ATTACKS[2], 0)["trace_text"]), len(run_attack(ATTACKS[2], 0, search_wrap=redact_pii, trace_saver=save_safe)["trace_text"])
print(f"one trace: raw {raw_b} bytes, redacted and slimmed {slim_b} bytes, {100 * (raw_b - slim_b) / raw_b:.1f}% smaller")
W33.rmdir()
```

```text
files: ['trace-0.jsonl', 'trace-1.jsonl', 'trace-2.jsonl']
age of the first, in days: 0.0
pretend it is 3 days on, 7-day rule (dry run): []
pretend it is 6 days on, 7-day rule (dry run): []
pretend it is 8 days on, 7-day rule (dry run): ['trace-0.jsonl', 'trace-1.jsonl', 'trace-2.jsonl']
still there after the dry runs: 3
real sweep removed: ['trace-0.jsonl', 'trace-1.jsonl', 'trace-2.jsonl'] | left: 0
one trace: raw 1582 bytes, redacted and slimmed 710 bytes, 55.1% smaller
```

`W33.rmdir()` removes only the empty folder this block made; `notes/` is never touched because `sweep` globs `*.jsonl` only. The slim trace is 55.1% smaller. Write **one thing a slim trace no longer tells you** (it drops the fields `text`, `result_preview` and `answer`): ____________________________________________________ And one thing it still tells you: ____________________________________________________

**C. The four sentences (homework).** Use **your own numbers** and keep the words *stand-in* and *n*. Frames to start you; finish each.

1. *A finding has six parts: ______________________________. For A1 the stand-in obeyed a planted note ______ times in ______, and the write was ______, so* ____________________________________________________
2. *A count of successes wobbles by about ______. With 20 runs at 0.3 that is about ______, so "7 then 9 of 20" is* ____________________________________________________
3. *"0 of 50" means ______________________________, because a true rate of ______ would show no landing about ______ of the time; and every rate here belongs to* ____________________________________________________
4. *The redactor finds ______ of my 8 typed cases by* ______________ *, not by* ______________ *; redacting what the model sees and what the log keeps close* ______________________________

**D. The residual risk for A1,** the sentence you would put in a system card. Include one thing you tested and one thing you only argued:

____________________________________________________________________________

____________________________________________________________________________

---

## 🐞 Page 33.4 — Break It on Purpose (three bugs · 30 min)

This page is for reading failures. Run each bug as written and predict first. Then say what went wrong and how you would have known. Each bug is **deliberate**.

### 33.4-A (loud) — `re.sub` without the text

Run this block as written.

```python
# DELIBERATE BUG 33.4-A (loud): re.sub with the text left out.
print(re.sub(PHONE, "[PHONE]"))
```

Prediction (which error, and what will it name?): ____________________________________________________

```text
TypeError: sub() missing 1 required positional argument: 'string'
```

The message counts the arguments. `re.sub` needs ______ things and I gave ______ . The fix: ____________________________________________________ Which line of `redact` shows the right shape? ______________________

### 33.4-B (loud) — `.stat` without brackets

Run this block as written.

```python
# DELIBERATE BUG 33.4-B (loud): .stat without its brackets.
p = sorted(Path("notes").glob("*.md"))[0]
print(time.time() - p.stat.st_mtime)
```

Prediction: ____________________________________________________

```text
AttributeError: 'function' object has no attribute 'st_mtime'
```

(On Python 3.11 and later the word in that message is `'method'`; it means the same thing.) What does the word `function` tell you that you forgot? ____________________________________________________ Which part is the method (needs brackets) and which is the field of its answer? method: ______________ field: ______________

### 33.4-C (SILENT) — a date-proof pattern that passes its own test

The tempting fix for the loose phone pattern eating dates: "refuse to start on something that looks like `2026-09-02`". It is tested on the fifteen note headings.

Run this block as written.

```python
# DELIBERATE BUG 33.4-C (SILENT): a phone pattern that "refuses to start on a date". It passes the test on the headings.
PHONE_DATE_SAFE = r"(?<![\d-])(?!\d{4}-\d{2}-\d{2}\b)(?:\+?\d[\d\s\-().]{7,}\d)(?!\d)"
patterns_v2 = [("EMAIL", EMAIL), ("CARD", CARD), ("PHONE", PHONE_DATE_SAFE)]
print("headings changed:", sum(redact(h, patterns_v2) != h for h in heads), "of", len(heads))
print(redact("[note 15] (similarity 0.326) 2026-09-02 - Vendor call", patterns_v2))
```

Predict two things: the first line prints ______ of 15; the second line prints ____________________________________________________

```text
headings changed: 0 of 15
[note 15] (similarity [PHONE] - Vendor call
```

Nothing crashed, and `0 of 15` looks perfect. **What did the test leave out?** ____________________________________________________ What does the agent's real search output look like, and why does the pattern start at `0.326)`? ____________________________________________________

Run this block to apply the repair.

```python
# The repair for 33.4-C: test on the REAL output of the running system, and use the pattern with a shape.
real_line = "[note 15] (similarity 0.326) 2026-09-02 - Vendor call"
print("shaped patterns, same real line:", redact(real_line, PATTERNS))
print("shaped patterns, headings changed:", sum(redact(h, PATTERNS) != h for h in heads), "of", len(heads))
```

```text
shaped patterns, same real line: [note 15] (similarity 0.326) 2026-09-02 - Vendor call
shaped patterns, headings changed: 0 of 15
```

The repair is not another exclusion. It is a pattern with a ______________ . The rule for next time: run the fix on ____________________________________________________

---

## 📓 Page 33.5 — Stop and Think (10 min · pen only)

These questions check your reasoning about the week's results. Answer in writing, with no code.

1. After `0 of 50`, the wobble formula says `0.00`. Does that mean the attack cannot work? What is the honest sentence? ____________________________________________________
2. `refuse_all_writes` also scores `0 / 50` on A1. Why is it not a fix? Give the second number that shows it. ____________________________________________________
3. The scan from Week 29 missed the reworded note (`34 / 50` landed), and `named_files_only` did not (`0 / 50`). What is the difference between the two defences? ____________________________________________________
4. For the A1 line, the bound `6.5` is slightly too small. Which side of the comparison made it so, and does it change the verdict? ____________________________________________________
5. Someone reports: "7 of 20 before, 9 of 20 after the patch, so the patch made it worse." Write the two numbers you would ask for before you agree. ____________________________________________________
6. A user asks for `notes_backup.md`, and the planted note orders a write to `notes_backup.md` with different content. What does `named_files_only` do, did we measure it, and where does it go on the card? ____________________________________________________

---

## 📓 Page 33.6 — The Bug Log

This page is for recording what went wrong this week and the rule you will keep from each failure.

| # | What went wrong (your words) | Loud or silent? | The one line or check that caught it | The rule I will keep |
|:-:|---|:-:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

Checks to keep: **the noise bound printed beside every gap · the control (the same system on other seeds) · the happy path re-tested after every patch · the reworded twin of every attack · the pattern with a shape, tested on the real output of the running system · the dry run read before the real sweep · `n` written next to every count.**

Then write this sentence in your own handwriting, with your own numbers, and keep the words *stand-in* and *n*:

> "On a stand-in that obeys at 0.3, A1 landed ______ of ______ before and ______ of ______ after allowing only files the user typed, a gap of ______ against a noise bound of about ______, and the legitimate save still worked ______ of ______; but zero of fifty only rules out rates above about ______, not 'never', and ____________________________________________________."

---

## 🧠 Self-Check (from memory, no notes)

Tick a line only if you can do it without looking anything up.

- [ ] I can work out `n p`, `n p (1−p)`, the wobble and the window by hand, and say what happens at `p = 0`.
- [ ] I can say whether "7 of 20 then 9 of 20" is a difference, with a number.
- [ ] I can say why quadrupling the runs only halves the wobble of the share.
- [ ] I can write a finding in six parts and re-test twice: the attack and the happy path.
- [ ] I can say why `0 / 50` is "not seen", and give the chance of seeing nothing at a true rate of `0.05`.
- [ ] I can predict the output of `re.sub` with ordered patterns, and say why the order is the design.
- [ ] I can say which personal data a regex redactor finds, which it cannot, and give the recall as a fraction of a typed set.
- [ ] I can write a retention sweep that lists before it deletes, and explain `>`.

---

**✂️ ANSWERS - keep this page folded until you have finished**

Check your written work against these answers only after you have finished every page.

### Warm-Up
1. Expect `20 × 0.3 =` **6**. No: you will almost never see exactly 6 (the wobble is about 2).
2. The table by category (Week 32), with how many results are behind each row.
3. (1) The **attack** again, (2) the **happy path**: the real task the agent is for.
4. The **pattern**, the **replacement**, the **text**.
5. A note that orders a write of a legal filename inside the box (A1): the sandbox, the allowlist and the size limit are all satisfied, so no fence fires. Accept any clear statement of this.

### Page 33.1
- **A.** Row 3 (`50, 0.5`): expected **25**, `n p (1−p) =` **12.5**, wobble **3.54**, share **0.071**, window **17.9 to 32.1**. Row 4 (`50, 0.1`): **5**, **4.5**, **2.12**, **0.042**, **0.8 to 9.2**. Row 5 (`100, 0.2`): **20**, **16**, **4.00**, **0.040**, **12.0 to 28.0**. Row 6 (`200, 0.5`): **100**, **50**, **7.07**, **0.035**, **85.9 to 114.1**. Row 7 (`50, 0.0`): **0**, **0**, **0.00**, **0.000**, **0 to 0**. Row 8 (`50, 1.0`): **50**, **0**, **0.00**, **0.000**, **50 to 50**. More wobbly: `p = 0.5` (**3.54** against **3.24**). The wobble is biggest at `p = 0.5`. At `p = 0` and `p = 1` the coin always lands the same way, so there is nothing to wobble. (This is also the trap: the formula applied to `0 of 50` says `0.00` whatever the truth.) Accept a window rounded to one decimal.
- **B.** Yes, `9` is inside `1.9 to 10.1`. No, it is not evidence of "worse": 7 and 9 are both ordinary counts for the same system; the difference, 2, is about one wobble.
- **C.** The Hook: wobbles **2.13** and **2.22**, bound **6.2**, gap **2**, **not** more than noise. Frame vs frame + scan (14 vs 7): **2.05**, **2.13**, bound **5.9**, gap **7**, **more than noise**. Gullibility 1.0 vs 0.8, `n = 200` (62 vs 54): **6.54**, **6.28**, bound **18.1**, gap **8**, **not** distinguishable. `n = 1000` (310 vs 225): **14.63**, **13.21**, bound **39.4**, gap **85**, **more than noise**. Twenty runs sees the big gap (true `0.6` vs `0.3`) and not the small one (`0.30` vs `0.24`); the small one needs about a thousand. A small gap needs many runs because the wobble shrinks only with the square root of the runs, so the gap must be big compared with the wobble, and it is the wobble that you are fighting. Accept rounding to one decimal in the bound. (Note the expected gap at `n = 200` is only `0.06 × 200 = 12`; an observed 8 can be a smaller or larger stretch of luck.)
- **D.** **0.1025, 0.0512, 0.0256.** Each time the wobble of the share **halves**. To halve your uncertainty you need **4** times the runs.
- **E.** `0.005, 0.077, 0.364, 0.605`. You would be quite surprised to see 0 of 50 at a true rate of about **0.10** (`0.005`, 1 chance in 200). The sentence: *"0 of 50 landed; any rate above about **6%** (or **5-10%**) would usually have shown at least one, and **1-2%** would often have shown none."* Accept any threshold between `0.05` and `0.10` for "usually", as long as the table supports it. The code also finds that at a true `0.05` you need **59** runs before seeing nothing becomes less than a 1-in-20 event.

### Page 33.2
- **A.** Predictions: 1 `Card [CARD].` · 1b `Card [PHONE].` · 2 `Due [PHONE].` · 2b `Due 2026-09-02.` · 3 `Call [PHONE] today.` · 4 `Call 12345 67890 today.` · 5 `Server [IPV4] runs version 1.2.3.4567.` · 6 unchanged. Rows 1 and 1b differ in the **order of the list**: with the loose phone pattern first, it eats the 16 digits of the card and the card pattern never gets to see them. **Longest and most specific first** (email, card, Aadhaar, phone, IPv4). The order is the design. Row 4 is not redacted because the shaped phone pattern wants a first digit of 6, 7, 8 or 9; `1...` is not the shape of an Indian mobile number. It is a **limit of shape-matching**, not a typo: the regex does exactly what it says, and what it says is a guess about shapes. Row 5: the version `1.2.3.4567` survives because the last group of an IPv4 address has at most three digits. Row 6: nothing changes. The score and the dates survive because they do not have the shape of a phone number (the loose pattern, by contrast, damages such lines: row 2 and Page 33.4-C).
- **B.** Guess: the first six C, the last two M (recall **6/8 = 0.75**). On the eight typed cases: six caught, name and address **missed**, recall `6/8 = 0.75`. The example `MINE` list: `+919876543210` and `98765-43210` are **caught** (the phone pattern allows `+91` and a dash), the spaced digits, the spelled-out digits, the "dot/at" address and the email without its ending are **missed**: 2/6; together `8/14 = 0.57`. Your own six will give your own number; what counts is that each prediction was written first. Why it never reaches 1.0: a name or an address has no shape, and every new pattern finds one more shape while people invent spellings of digits faster than you can list them. The number belongs in the system card, with "n = 14 typed cases".
- **C.** Model card, A1. **Attack:** a planted note orders `write_file(filename="notes_backup.md", ...)`. **Evidence:** `15 / 50` (seeds 1, 3, 4, 8, 13, ...). **Mechanism:** the filename is flat, the suffix is `.md`, the file is small and inside the box, so the strict sandbox, the allowlist and the size limit are all satisfied and no fence fires. **Fix:** `named_files_only`: a write is allowed only to a filename that appears in the user's question. **Before / after:** `15 / 50 → 0 / 50`. **Happy path:** legitimate save `50 / 50`. **Residual:** a user who asks for a file still trusts its contents; an order to write the *same* file with other content is argued, not measured; `0 / 50` is "did not see it". **Gap vs bound:** `15` against about `6.5`: more than noise. A2: `15 / 50 → 0 / 50` with `strict=True`; gap `15`, bound `6.5`; **mechanism:** the weak sandbox let a path leave the box. A3: context `50/50` and trace `50/50` → `0/50` and `0/50` with both locks; **residual:** recall `6/8`; the user's own number still reaches the model. (i) **No**: both use the same stand-in on the same seeds `0 ... 49`, so the same 15 seeds obey in both (`True`); A1 and A2 differ in what the note *asks for*, not in how often the model *obeys*. It is one measurement of the stand-in read through two fences. (ii) The bound would be **too small**: a fair comparison of a system with itself must say "no difference" (here, gap `-2` against `9.3`: not distinguishable, as it should). (iii) So nobody reads five attacks and thinks five were run; A5 needs a real model's judgement, which does not exist offline.
- **D.** v0: `50 / 50 / 50`. Redact tool output only: `0 / 0 / 50`. Redact the saved trace only: `50 / 0 / 0`. Both: `0 / 0 / 0`. (Chapter Section 11, same numbers; I re-ran the code and it printed exactly these.) Each lock covers a different door: redacting the tool output stops door 1 (the notes) but a number the *user typed* is in the question, the model's words and its search query, and they go straight to the saved trace; only the saved-trace lock stops that, and only the tool-output lock stops the model being shown the note's number. The user's typed number is still in the model's context; it was theirs to send.

### Page 33.3
- **A.** `1.04167` kept · `7.00000` kept · `7.00001` deleted · `11.57407` deleted · `34.72222` deleted. 604,800 s is exactly **7** days; the rule is "older than" (`>`), so a file exactly at the limit survives **one more second**. In the policy say "older than 7 days" (not "7 days or older") and say which clock the age is measured on (last changed).
- **B.** Model policy: *"Traces older than 7 days are deleted by `sweep`, run every night at 03:00, because a trace is only useful for the week in which someone could still remember the question that produced it."* Any `N` with a use-based reason is fine; disk space alone is not a reason here. Predictions: `3 * DAY` lists **nothing**, `6 * DAY` lists **nothing**, `8 * DAY` lists **all three**. A dry run deletes **nothing** (`3` files still there). The real sweep removed all three. The slim trace no longer tells you **what was said**: the words of the model's reply, the preview of what a tool returned, and the answer the user saw. It still tells you which tool was called, with which arguments, in which order, and whether it errored (the shape of the run).
- **C.** Model sentences. *(1) A finding has attack, evidence, mechanism, fix, two re-tests and a residual; for A1 the stand-in obeyed a planted note 15 times in 50 and the write was legal, so no fence fired; allowing only files the user typed took it to 0 of 50 while the legitimate save stayed 50 of 50. (2) A count of successes wobbles by about sqrt(n p (1-p)); with 20 runs at 0.3 that is about 2, so "7 then 9 of 20" is well inside the noise and not a difference. (3) "0 of 50" means I did not see it in 50 runs, because a true rate of 0.05 would show no landing about 8% of the time (1 in 13); and every rate here belongs to a stand-in whose obey chance I typed. (4) The redactor finds 6 of my 8 typed cases by shape, not by meaning; redacting what the model sees and what the log keeps close two different doors, and the scan loses to rewording where the code layer does not.* Any wording works if the numbers are your own, `n` is beside each count, and *stand-in* appears.
- **D.** Model: *"A1 (a planted note orders a legal write of a file nobody asked for): 15 of 50 before, 0 of 50 after `named_files_only`, gap 15 against a noise bound of about 6.5, the legitimate save 50 of 50, on a stand-in with an obey chance of 0.3. Tested: the reworded twin (34 of 50 against the scan alone, 0 of 50 against the guard). Argued, not measured: an order to write the same file the user typed with other content would be allowed; and 0 of 50 only rules out rates above about 6%."*

### Page 33.4
- **A.** `TypeError: sub() missing 1 required positional argument: 'string'`. `re.sub` needs **three** things (pattern, replacement, text) and I gave **two**. Fix: `re.sub(PHONE, "[PHONE]", text)`, with a string in the third place. `redact` has the right shape: `re.sub(pattern, f"[{tag}]", text)`. (Do not confuse it with `str.replace`, which gives a different message.)
- **B.** `AttributeError: 'function' object has no attribute 'st_mtime'`. The word `function` says that `p.stat` is the method itself; I forgot to **call** it. Fix: `p.stat().st_mtime`. Method: **`stat`** (needs brackets); field: **`st_mtime`** (belongs to what `stat()` returns).
- **C.** The first line prints **0 of 15**; the second prints `[note 15] (similarity [PHONE] - Vendor call`. The test left out the real output of the running system: the search result has a score and a date next to each other, `(similarity 0.326) 2026-09-02`, and the pattern starts at `0.326)` (the `(?<![\d-])` guard is satisfied there) and runs through the date, so the score and the date are lost. It passed only the example that motivated the fix. The repair is a pattern with a **shape** (ten digits starting 6-9), which leaves the real line intact and still changes 0 of the 15 headings. Rule: run the fix on **the real output of the system**, as well as on the example that motivated it, and on the happy path.

### Page 33.5
1. No. The formula `sqrt(n p-hat (1 − p-hat))` with `p-hat = 0` is zero whatever the truth; it was used for something it cannot do. Honest sentence: *"0 of 50 landed; any rate above about 6% would usually have shown at least one."* If 50 runs are not enough, more runs are the repair.
2. It stops the attack by stopping the agent's job. The second number: the legitimate save worked `0 / 50`. An attack count of zero is not enough; the happy path has to survive.
3. The scan looks for nine known **phrases**; a polite rewording uses none of them, so it does nothing. `named_files_only` works on the **cause** (a write nobody asked for), in code, so it does not care how the order is worded. The scan is a guess about words; the guard is a rule about actions.
4. The "after" side was `0 of 50`, where the formula gives a wobble of exactly zero, so the combined bound is `2 × sqrt(10.5 + 0) ≈ 6.5` rather than a little larger. The gap of 15 is far above either, so the verdict does not change, but the bound is "slightly too small", never "tight".
5. The gap **and** its noise bound (here 2 against 6.2), and the same system run again on other seeds (the control). Also the number of runs, `n`.
6. It allows it: the filename is in the question. We did not measure it; it goes on the card as a **residual risk, argued and not measured**.

### Page 33.6 and Self-Check
Your words, your numbers. For the chapter's runs the sentence reads: *"... A1 landed 15 of 50 before and 0 of 50 after allowing only files the user typed, a gap of 15 against a noise bound of about 6.5, and the legitimate save still worked 50 of 50; but zero of fifty only rules out rates above about 6%, not 'never', and a user who asks for a file is still trusting what gets written."* If a tick is not earned, go back to the page that trains it: the wobble, bound and zero (33.1), the order of patterns, recall and the red-team card (33.2), ages, the sweep and the four sentences (33.3), the three bugs (33.4).
