# Workbook — Week 27: Review and Assessment 3

**Name:** ________________________________  **Date:** ______________

[⬅ Week 26](week-26.md) · [📖 Read the chapter first](../student-guide/week-27.md) · [Course Home](../README.md) · [Next ➡](week-28.md)

---

> **Rules for this workbook.** Today's paper has no new material, so this workbook has none either. It is for **two moments**: the night **before** the paper (Pages 27.1 and 27.2 are practice on numbers that are **not** the paper's) and the days **after** it (Pages 27.3 and 27.4 are your marking, your grid and your chunk-size homework). Then a Break-It page and a Bug Log. **Write your answer by hand first, then run.** A guess written after the run is not a guess.
>
> **Real numbers.** Every number printed below came from a real run of the code shown (no randomness is used anywhere, so your numbers should match). By-hand numbers are plain arithmetic. Numbers marked **PRACTICE** are invented for this workbook, so they are **not** your marks, **not** the paper's numbers and **not** the class's results.
>
> **Stand-ins.** If a page mentions Week 23's scripted client or Week 26's sentence-copier, each is a **stand-in, not a model**: nothing scored against one says anything about a real model. No real model is run in this workbook.
>
> **Files you need.** Pages 27.1 to 27.3 and 27.5 need only Python (27.1 uses `numpy`). Page 27.4 needs `l4lib/` (import it, never copy it): run it from the folder that contains `l4lib/`. Nothing needs the internet.
>
> **Calculator.** `ln`, `log` (base 10) and a power key. Round only the answer.

---

## ✅ Warm-Up (5 min, before anything else)

`a = [3, 0, 4]` and `b = [0, 4, 3]`. Write the dot product, the two lengths, and the cosine of the angle between them.

dot = ______ · length of a = ______ · length of b = ______ · cosine = ______

Then run:

```python
# warm27.py - Warm-Up check. PRACTICE numbers.
import math
a = [3, 0, 4]
b = [0, 4, 3]
dot = sum(x * y for x, y in zip(a, b))
la = math.sqrt(sum(x * x for x in a))
lb = math.sqrt(sum(y * y for y in b))
print("dot:", dot, " lengths:", la, lb, " cosine:", round(dot / (la * lb), 2))
```

```text
dot: 12  lengths: 5.0 5.0  cosine: 0.48
```

---

## 🧮 Page 27.1 — The By-Hand Ideas, Fresh Numbers (25 min · pen, calculator, then one check)

These are the kinds of questions the paper asks, on numbers it does not use. **Do all of it before you run anything.**

**Part 1 — Cosine (6 min).** `q = [1, 2, 2]`. Three cards: `A = [2, 4, 4]`, `B = [2, 1, 0]`, `C = [-1, -2, -2]`.

| Card | q · card | length of card | cos(q, card) |
|:--:|:--:|:--:|:--:|
| A | | | |
| B | | | |
| C | | | |

(The length of `q` is 3.) **i.** Which card is nearest in direction to `q`? ________ **ii.** Card `A` is longer than `q`. Why does that not matter to a cosine? ____________________________________________________________

**Part 2 — KL and the pair loss (9 min).** `p = [0.7, 0.2, 0.1]`, `r = [0.4, 0.4, 0.2]`. KL of `p` from `r` is the sum of `p × ln(p / r)`.

| place | p | r | p × ln(p / r) | r × ln(r / p) |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 0.7 | 0.4 | | |
| 2 | 0.2 | 0.4 | | |
| 3 | 0.1 | 0.2 | | |
| **sum** | | | | |

**iii.** Is KL of `p` from `r` the same as KL of `r` from `p`? ________ **iv.** What is KL of `p` from `p`, and why, before you compute it? ____________________________________________________________

The pair loss is `-ln(sigmoid(gap))`, where `gap` is the winner's score minus the loser's. Without a calculator, put these three in order, smallest loss first: gap `+3`, gap `0`, gap `-3`. ________ Then fill in gap `0` with a calculator: ________ (hint: `ln 2`).

**Part 3 — Tokens, a slope, `6ND` (6 min).**

**v.** 1,800 bytes become 900 tokens; after more merges, 600 tokens. Bytes per token before: ______ after: ______
**vi.** Models of `N = 10,000`, `100,000`, `1,000,000` knobs score losses `6.4`, `2.0`, `0.8`. Slope between the first and last point (`log10` both sides): ______ Predicted loss at `N = 10,000,000`: ______ Measurement or prediction? ______
**vii.** `C ≈ 6ND` for `N = 500,000` and `D = 40,000,000`: ______

**Part 4 — A floor and a top k (4 min).** A prompt gets 21 of 32 fields right; the constant answer gets 17 of 32. Prompt: ______% · constant: ______% · gap: ______ fields. Scores `[0.42, 0.05, 0.31, 0.77, 0.29]`: the ids of the best three, best first: ______ (ids start at 0).

**Now run the check:**

```python
# check271.py - Page 27.1: every hand answer, computed.  PRACTICE numbers.
import math
import numpy as np

def cosine(x, y):
    return sum(a * b for a, b in zip(x, y)) / (math.sqrt(sum(a * a for a in x)) * math.sqrt(sum(b * b for b in y)))

q = [1, 2, 2]
cards = [("A", [2, 4, 4]), ("B", [2, 1, 0]), ("C", [-1, -2, -2])]
for name, card in cards:
    print("cos(q, card", name + "):", round(cosine(q, card), 3))

def kl(p, r):
    return sum(x * math.log(x / y) for x, y in zip(p, r))

p = [0.7, 0.2, 0.1]
r = [0.4, 0.4, 0.2]
print("KL terms p from r:", [round(x * math.log(x / y), 4) for x, y in zip(p, r)], " sum", round(kl(p, r), 4))
print("KL terms r from p:", [round(y * math.log(y / x), 4) for x, y in zip(p, r)], " sum", round(kl(r, p), 4))
print("KL p from p:", kl(p, p))
for gap in (3.0, 0.0, -3.0):
    print("pair loss at gap", gap, ":", round(-math.log(1 / (1 + math.exp(-gap))), 4))
print("bytes per token:", 1800 / 900, 1800 / 600)
slope = (math.log10(0.8) - math.log10(6.4)) / (math.log10(1e6) - math.log10(1e4))
print("slope:", round(slope, 3), " loss at 1e7:", round(0.8 * 10 ** slope, 3))
print("C = 6ND:", f"{6 * 5e5 * 4e7:.1e}")
fields, right, floor = 32, 21, 17
print("score", round(right / fields * 100, 1), "floor", round(floor / fields * 100, 1), "gap", right - floor, "fields")
scores = np.array([0.42, 0.05, 0.31, 0.77, 0.29])
print("top 3 ids:", np.argsort(-scores)[:3].tolist())
```

```text
cos(q, card A): 1.0
cos(q, card B): 0.596
cos(q, card C): -1.0
KL terms p from r: [0.3917, -0.1386, -0.0693]  sum 0.1838
KL terms r from p: [-0.2238, 0.2773, 0.1386]  sum 0.192
KL p from p: 0.0
pair loss at gap 3.0 : 0.0486
pair loss at gap 0.0 : 0.6931
pair loss at gap -3.0 : 3.0486
bytes per token: 2.0 3.0
slope: -0.452  loss at 1e7: 0.283
C = 6ND: 1.2e+14
score 65.6 floor 53.1 gap 4 fields
top 3 ids: [3, 0, 2]
```

**viii.** One of your answers will not match the printed one. Which, and what did you do differently? ____________________________________________________________

---

## 📊 Page 27.2 — Reading a Table Honestly (20 min · pen only, then a tiny check)

Section E of the paper gives you real tables and asks what you would *not* say. Practise on a **PRACTICE** table (invented, not the paper's, not yours). A small model was trained with one part deleted, twice with different seeds.

| Model | Train loss | Validation loss | Validation, repeated with seed 1 |
|---|:--:|:--:|:--:|
| full | 1.90 | 2.00 | 1.95 |
| no mask | 0.10 | 0.12 | 0.15 |
| no positions | 1.80 | 2.10 | 2.08 |
| no norm | 1.40 | 1.70 | 1.72 |

**A.** Work out each gap (validation minus train). full ______ no mask ______ no positions ______ no norm ______

**B.** One row cannot be ranked by its validation loss. Which, and why? ____________________________________________________________

**C.** A classmate says *"no norm has the lowest loss of the ones that can be ranked, so norm is useless."* Give two reasons, from the table, to be careful. (1) ____________________________________________________________ (2) ____________________________________________________________

**D.** A **PRACTICE** recall table: ten questions in **your own wording** score `0.90 / 1.00 / 1.00` at k = 1, 3, 5. The same ten facts in **a stranger's words** score `0.30 / 0.60 / 0.70`. Which row would you quote for how the search will do for someone else, and why? ____________________________________________________________

**E.** Write the one question you would ask before trusting any recall number: ____________________________________________________________

**F.** With ten questions, how big is one question? With eight? ______ ______ A difference of `0.10` is how many questions? ______ Run the check:

```python
# check272.py - Page 27.2: the gaps in the PRACTICE table, and what one question is worth.
rows = [("full", 1.90, 2.00, 1.95), ("no mask", 0.10, 0.12, 0.15), ("no positions", 1.80, 2.10, 2.08), ("no norm", 1.40, 1.70, 1.72)]
for name, train, val, val2 in rows:
    print(f"{name:13s} gap {val - train:.2f}   seed change {abs(val - val2):.2f}")
print("one question of 10 is worth", 1 / 10, " of 8 is worth", 1 / 8)
```

```text
full          gap 0.10   seed change 0.05
no mask       gap 0.02   seed change 0.03
no positions  gap 0.30   seed change 0.02
no norm       gap 0.30   seed change 0.02
one question of 10 is worth 0.1  of 8 is worth 0.125
```

**G.** In two sentences: why is "no mask has the lowest loss" a reason to worry rather than celebrate? ____________________________________________________________

---

## 📋 Page 27.3 — Mark Your Own Paper, Fill the Grid (after the paper · 30 min · pen in the *other colour*, then one check)

Mark your paper against the printed marking sheet (the one your teacher gave you). For Sections D and E, mark the **working** and not only the answer. Then fill the grid with **your own** marks.

| Week | What it covers | Marks available | Marks earned | % | Redo if marks ≤ | Circle? |
|:--:|---|:--:|:--:|:--:|:--:|:--:|
| 19 | Ablations; the mask leak; heads | 10 | | | 6 | |
| 20 | BPE: bytes, merges, bytes per token | 6 | | | 3 | |
| 21 | The log-log line; `6ND` | 8 | | | 4 | |
| 22 | Masked loss; pair loss; KL; the leash | 13 | | | 7 | |
| 23 | The harness: floor, frozen set, guard | 8 | | | 4 | |
| 24 | Examples in the prompt; the logit mask | 4 | | | 2 | |
| 25 | Cosine; recall | 12 | | | 7 | |
| 26 | RAG: top k, citations, chunk size | 14 | | | 8 | |
| | **Total** | **75** | | | | |

("Redo if marks ≤" is 60% of the week's marks, rounded down. Weeks 20 and 24 are worth only 6 and 4 marks, so a flag there is one or two questions: ask yourself the question out loud before you call it a weakness.)

**Circle at most two weeks.** Pick the lowest percentage; on a tie, the priority is **Week 23, then Week 26, then Week 22**, because Weeks 28 and 29 lean on them. For each circled week write the day and time of the redo: ______________________

Here is a check for your grid. The marks in it are **PRACTICE**; **replace the `earned` list with your own eight numbers** (in the order of the table):

```python
# check273.py - Page 27.3: percentages and redo flags from your marks.  PRACTICE marks (not yours).
weeks = [19, 20, 21, 22, 23, 24, 25, 26]
available = [10, 6, 8, 13, 8, 4, 12, 14]
earned = [8, 2, 5, 6, 7, 3, 10, 9]            # PRACTICE: replace with your own eight numbers
print("total available:", sum(available), " earned:", sum(earned))
for wk, av, got in zip(weeks, available, earned):
    line = int(av * 0.6)
    flag = "REDO?" if got <= line else ""
    print(f"week {wk}: {got:2d}/{av:2d} = {got / av * 100:3.0f}%  line {line}  {flag}")
```

```text
total available: 75  earned: 50
week 19:  8/10 =  80%  line 6  
week 20:  2/ 6 =  33%  line 3  REDO?
week 21:  5/ 8 =  62%  line 4  
week 22:  6/13 =  46%  line 7  REDO?
week 23:  7/ 8 =  88%  line 4  
week 24:  3/ 4 =  75%  line 2  
week 25: 10/12 =  83%  line 7  
week 26:  9/14 =  64%  line 8
```

**A.** With the **PRACTICE** marks, which weeks are flagged, and which two would you circle? ____________________________________________________________

**B.** Your own result: lowest week ______ (____%) · my two circled weeks ______ and ______ · the redo page for each: ______________________

**C.** The answer I was most surprised to get wrong was ____________________, because I thought ____________________.

---

## ✂️ Page 27.4 — Three New Cuts: Predict First (after the paper · 25 min · pen, then computer)

Week 26 cut the 688-word notebook into chunks of 30, 60, 120 and 250 words. Your homework is three cuts it did not use: **20, 45 and 90 words**, with overlaps of **5, 10 and 20**. The computer job itself (`sweep.py`) is in the student guide; this page is for the thinking around it.

**Part 1 — Counting windows by hand (8 min).** A window starts every `size - overlap` words and the last window is the first one that reaches the end of the text. For a text of **100** words, size 30, overlap 10 (step 20), the starts are 0, 20, 40, 60, 80: **5** windows. Now for the notebook (688 words), estimate the number of windows for each cut. (Hint: the step, then the first start that is at least `688 - size`.)

| size | overlap | step | windows (your count) | words stored ≈ windows × size | times the notebook (÷ 688) |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 20 | 5 | | | | |
| 45 | 10 | | | | |
| 90 | 20 | | | | |

Check the counts (the stored words are a little less than windows × size, because the last window is short):

```python
# check274.py - Page 27.4: window counts for the three new cuts (needs l4lib/ next to this file).
from l4lib import rag

total_words = len(rag.NOTEBOOK.split())
print("notebook words:", total_words)
for size, over in [(20, 5), (45, 10), (90, 20)]:
    cs = rag.chunk_fixed(rag.NOTEBOOK, size, over)
    stored = sum(len(c.split()) for c in cs)
    print(f"size {size}, overlap {over}: step {size - over}, windows {len(cs)}, words stored {stored}, times the notebook {stored / total_words:.2f}, k=3 sends at most {3 * size} words")
```

```text
notebook words: 688
size 20, overlap 5: step 15, windows 46, words stored 913, times the notebook 1.33, k=3 sends at most 60 words
size 45, overlap 10: step 35, windows 20, words stored 878, times the notebook 1.28, k=3 sends at most 135 words
size 90, overlap 20: step 70, windows 10, words stored 868, times the notebook 1.26, k=3 sends at most 270 words
```

**Part 2 — Predict, before you run `sweep.py` (5 min).** Circle one in each row.

| My prediction | |
|---|---|
| As the window grows from 20 to 90, recall@1 goes | **up / down / stays about the same** |
| As the window grows, the share of the notebook sent at k = 3 goes | **up / down / stays about the same** |
| The window that sends the smallest share of the notebook is | 20 / 45 / 90 |

**Part 3 — The run (7 min).** Run `sweep.py` from the student guide in the same session as Week 26's `load.py` and `questions.py`. **Your rows are yours to read; they are not printed here.** Copy them:

| cut | n | r@1 | r@3 | r@5 | % of notebook at k = 3 |
|---|:--:|:--:|:--:|:--:|:--:|
| 20 / 5 | | | | | |
| 45 / 10 | | | | | |
| 90 / 20 | | | | | |

**Part 4 — Two sentences (5 min).** (1) What my table shows: ____________________________________________________________
(2) What ten questions **cannot** tell me (hint: how big is one question? who wrote them?): ____________________________________________________________

---

## 🐞 Page 27.5 — Break It on Purpose (three bugs · 25 min)

Each block is **deliberately broken**. For each: (i) predict what it prints, (ii) run it, (iii) say what it means, (iv) write the fix and the check you would run next time. One is **loud** and two are **SILENT**.

### 27.5-A (SILENT) — the roles swapped in KL

```python
# DELIBERATE BUG 27.5-A (SILENT): the roles in KL are swapped inside the loop; it runs, prints a sensible number, and is wrong.
import math

def kl_wrong(p, r):
    return sum(y * math.log(y / x) for x, y in zip(p, r))

p = [0.7, 0.2, 0.1]
r = [0.4, 0.4, 0.2]
print("KL(p from r), wrong:", round(kl_wrong(p, r), 4))
print("KL(p from p), wrong:", round(kl_wrong(p, p), 4))
```

```text
KL(p from r), wrong: 0.192
KL(p from p), wrong: 0.0
```

(i) ______________ (ii) ______________ (iii) ______________ (iv) ______________
(v) The `KL(p from p)` check printed `0.0`. Does that catch this bug? Why not? ____________________________________________________________

### 27.5-B (loud) — bytes per token on nothing

```python
# DELIBERATE BUG 27.5-B (loud): bytes per token on an empty text.
def bytes_per_token(text, tokens):
    return len(text.encode("utf-8")) / len(tokens)

print(bytes_per_token("hello world", ["hello", " world"]))
print(bytes_per_token("", []))
```

```text
5.5

    print(bytes_per_token("", []))
  File "/private/tmp/wb27/b2.py", line 3, in bytes_per_token
    return len(text.encode("utf-8")) / len(tokens)
ZeroDivisionError: division by zero
```

(i) ______________ (ii) ______________ (iii) ______________ (iv) ______________

### 27.5-C (SILENT) — two kinds of logarithm

```python
# DELIBERATE BUG 27.5-C (SILENT): natural log for the loss but log10 for N.
import math

sizes = [1e4, 1e5, 1e6]
losses = [6.4, 2.0, 0.8]
good = (math.log10(losses[2]) - math.log10(losses[0])) / (math.log10(sizes[2]) - math.log10(sizes[0]))
bad = (math.log(losses[2]) - math.log(losses[0])) / (math.log10(sizes[2]) - math.log10(sizes[0]))
print("slope, same log both sides:", round(good, 3))
print("slope, mixed logs:", round(bad, 3))
print("prediction at 1e7 with the mixed slope:", round(losses[2] * 10 ** bad, 3))
print("prediction at 1e7 with the right slope:", round(losses[2] * 10 ** good, 3))
```

```text
slope, same log both sides: -0.452
slope, mixed logs: -1.04
prediction at 1e7 with the mixed slope: 0.073
prediction at 1e7 with the right slope: 0.283
```

(i) ______________ (ii) ______________ (iii) ______________ (iv) ______________

---

## 📓 Page 27.6 — The Bug Log

Add **at least two** entries (one must be SILENT). One of them should be the answer you were most surprised to get wrong on the paper.

| # | File / page | What I saw | What it meant | The fix | How I would catch it next time |
|:--:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

---

## 🧠 Self-Check (from memory, no notes)

1. What does one BPE merge do, and what happens to bytes per token as merges are learned? ____________________________________________________________
2. Losses `9, 3, 1` at steps of ×10 lie on a line. Is a prediction from it a measurement? ____________________________________________________________
3. A masked loss is higher than an unmasked one. Is the model worse? ____________________________________________________________
4. Why does the guard stop one call late? ____________________________________________________________
5. A mask forces valid JSON. What can still be wrong? ____________________________________________________________
6. Why does a long vector beat a close one on a plain dot product, and what fixes it? ____________________________________________________________
7. Recall is 1.00. What is your first question? And a valid citation proves what? ____________________________________________________________
8. Which two weeks did I circle, and when is each redo? ____________________________________________________________

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up

dot = `12`; lengths `5` and `5`; cosine = `12 / 25` = `0.48`.

### Page 27.1

| Card | q · card | length | cos |
|:--:|:--:|:--:|:--:|
| A | 18 | 6 | `18 / 18` = **1.000** |
| B | 4 | `√5` = 2.236 | `4 / (3 × 2.236)` = **0.596** |
| C | -9 | 3 | `-9 / 9` = **-1.000** |

i. **A**. ii. It points the same way as `q` and twice the length; the lengths are divided out, so only direction counts (a cosine of 1.000). (Card C points exactly the opposite way.)

| place | p × ln(p / r) | r × ln(r / p) |
|:--:|:--:|:--:|
| 1 | `0.3917` | `-0.2238` |
| 2 | `-0.1386` | `0.2773` |
| 3 | `-0.0693` | `0.1386` |
| **sum** | **0.1838** | **0.1920** |

iii. **No**, `0.1838` against `0.1920`: close, but not equal, so we always say "from which". iv. `0`: nothing has moved, every `p/p` is `1` and `ln 1 = 0`. Pair losses, smallest first: gap `+3` (`0.0486`), gap `0` (`0.6931`, which is `ln 2`), gap `-3` (`3.0486`): the winner being ahead is cheap, behind is expensive.

v. `2.0`, then `3.0`. vi. Slope `log10(0.8/6.4) / 2` = `-0.9031 / 2` = **-0.452**. Prediction at 10,000,000: `0.8 × 10^(-0.452)` = **0.283**. A **prediction** (train that model to turn it into a measurement). vii. `6 × 500,000 × 40,000,000` = **1.2e+14** (`1.2 × 10^14`). Part 4: `21/32` = **65.6%**, `17/32` = **53.1%**, gap **4 fields**; top three ids **[3, 0, 2]**. viii. Accept any honest answer. The commonest slips: dividing by the wrong length in B, writing `log` of a loss on the wrong side of the division, and listing the right ids in the wrong order.

### Page 27.2

A. full `0.10`, no mask `0.02`, no positions `0.30`, no norm `0.30`. B. **No mask**: it can read the answer (the mask is what stops the model from seeing the next letter it is asked to guess), so its tiny loss is a leak, not a good model. C. Two of: (1) one small model and two seeds, so the gap between seeds (`0.05`, `0.03`, `0.02`, `0.02`) is a reminder that each number has wobble; (2) the no-norm gap (`0.30`) is as big as the no-positions gap, so its validation loss is further from its train loss than the full model's (`0.10`); (3) a switch-off test on the parts would say more than a loss; (4) one word about "useless" is a claim about every model, from one. Accept any two reasons that use the table. D. The **stranger's** row (`0.30 / 0.60 / 0.70`): the first row is an upper bound, because the questions were written from the notes and so contain the notes' words. E. *"Who wrote the questions?"* (accept: how many were there, and were they written independently of the notes). F. `0.10`; `0.125`; **one** question. The check prints the gaps and these values. G. Any version of: the mask stops the model from peeking at the answer; without it the model reads the answer it is asked to predict, so a tiny loss means it is cheating, not that it is good.

### Page 27.3

A. With the **PRACTICE** marks: flagged **Week 20** (2 of 6) and **Week 22** (6 of 13). Lowest percentages: Week 20 (33%), Week 22 (46%). Circle **both**. (Week 20 is thin, 6 marks: ask the spoken check first.) B, C. Your own. Full marks for C: a real answer with a reason (a wrong answer you believed is the most useful entry you can make).

### Page 27.4

| size | overlap | step | windows | words stored | times the notebook |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 20 | 5 | 15 | 46 | 913 | 1.33 |
| 45 | 10 | 35 | 20 | 878 | 1.28 |
| 90 | 20 | 70 | 10 | 868 | 1.26 |

Your hand count can be off by one (`+/- 1`); the method is `688 / step`, rounded up where the last window still reaches the end. The check prints the real counts above. The fixed cost of overlap is small here: every cut stores only about 1.3 times the notebook. **Part 2:** no fixed answer (the point is to commit first); the arithmetic says the share of the notebook sent at k = 3 **must** go up with the window, because the most it can send is `3 × size` words (`60`, `135`, `270`). **Part 3:** your own table. **Part 4:** full marks for (1) a sentence that names what your rows show (both recall and the share sent), and (2) a sentence that says one question is `0.10`, the ten questions were written by someone who knew the notes, and a small difference is noise, not a finding.

### Page 27.5

**A.** (i) Something near `0.19` that looks fine. (ii) `KL(p from r), wrong: 0.192` and `KL(p from p), wrong: 0.0`. (iii) The loop uses `y * log(y / x)` (the terms of KL of `r` from `p`) instead of `x * log(x / y)`. It returns `0.192` where the right value is `0.1838`. (iv) Use `x * math.log(x / y)` as the Page 27.1 table does; check the function against a hand-worked value, not only against a case where the answer is known to be zero. (v) **No.** KL of a table from itself is `0` whichever way round the terms go, so the test passes on broken code; it is a check that cannot fail.

**B.** (i) `5.5`, then an error. (ii) `ZeroDivisionError: division by zero`. (iii) An empty text has no tokens, and dividing by `len(tokens) = 0` is the error. (iv) Decide what an empty text should mean (return `0.0`, or refuse with your own message) and test the empty case on purpose; a loud bug is a good bug.

**C.** (i) Two slopes that look plausible. (ii) `-0.452` (same log on both sides) and `-1.04` (mixed); the predictions are `0.283` and `0.073`. (iii) The natural log (`ln`) of the loss divided by a `log10` change in `N` gives a slope that is wrong by a constant factor (`ln 10` = `2.303`), and `10 ** slope` then wrongly undoes it: a silent, plausible-looking prediction. (iv) Use the same logarithm on both sides, and check the slope against a two-point hand calculation (`-0.9031 / 2`).

### Page 27.6 and Self-Check

Bug Log: any two true entries, one SILENT, naming a check that would have caught it (a hand-worked value; a case that can fail; the same logarithm on both sides).

1. It joins the most common neighbouring pair into one token; bytes per token **rises**. 2. **No**: it is a prediction; train the model to measure. 3. **No**: it is a different set of guesses (the masked loss skips the easy ones), not a worse model. 4. The guard checks the bill **after** each call, so the call that crosses the limit has already happened. 5. The **values** (shape, not sense). 6. Length raises a plain dot product; divide the length out (normalise once). 7. *"Who wrote the questions?"*; a valid citation proves only that the writer named a note it was handed. 8. Your own, with a day and time attached.
