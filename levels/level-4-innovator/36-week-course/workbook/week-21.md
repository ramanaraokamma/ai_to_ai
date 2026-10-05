# Workbook — Week 21: Pretraining and the Scaling Arithmetic

**Name:** ________________________________  **Date:** ______________

[⬅ Week 20](week-20.md) · [📖 Read the chapter first](../student-guide/week-21.md) · [Course Home](../README.md) · [Next ➡](week-22.md)

---

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed in the last 24 hours.** The digits in the worked examples and in the answers came from real CPU runs (Python 3.10, torch 2.2.1, numpy 1.26.4, one thread, no GPU). **Everything that trains a model is seeded** (seed 0 unless a page says otherwise), so your losses, knob counts and duplicate counts should match mine **to every printed digit** if you have the same Python version. **Only seconds and operations-a-second differ** from computer to computer and from minute to minute. By-hand numbers are plain arithmetic.
>
> **Predict first, then run.** On pages 21.2, 21.3, 21.4 and 21.5 you write your guess, or your line, *before* you run anything. A wrong guess is useful. A guess written after the run is not a guess. **Once a prediction is in ink, you do not change it.**
>
> **Two kinds of page.** Pages **21.1 to 21.5 each have a PRACTICE part** (small, on numbers or lines I ran for you, so you can check your reading) **and a YOURS part** (what your own class files print). The practice numbers are not your results and must not be pasted into your report. Page 21.6 is about **your** results only.
>
> **Everything is real. There is no stand-in and no scripted backend anywhere in this workbook.** The models are your own `TinyGPT` from Week 17, trained on your CPU on text that is already on your computer. **No model was trained at scale, and nothing here says what any shipped model does.** The "7-billion-knob" lines are **arithmetic on numbers Module 4 assumed**, not something anyone measured.
>
> **Keep your class files.** You need `textpool.py`, `trainer.py`, `pool_facts.py`, `sweep.py` (and its `sweep.csv`), `fit.py`, `check.py` (and its `check.csv`), `flops.py`, `dedup.py` and `card.py` from class, and your own Week 17 `tinygpt.py`. The practice pages add **four** small files you type yourself (`check211.py`, `check212.py`, `check214.py`, `check215.py`, all in the answers section, for checking only), and page 21.7 has four deliberate bugs. Run everything from the folder that contains `l4lib/`. The slow runs are `sweep.py` (about 90 seconds), `check.py` (about 90 seconds) and `check212.py` (about 1 minute); **close other programs first**, because the timings are disturbed by other work. Nothing downloads anything.
>
> Use a **calculator** (with a `log10` button) and carry **four decimals for logs** and **two decimals** elsewhere unless a page says otherwise.

---

## ✅ Warm-Up (5 min)

Five quick questions about **Weeks 16 to 20**.

**W1.** A tokenizer starts from the 256 bytes and learns 300 merges. Its vocabulary has ____________ tokens. (Week 20)

**W2.** Can "bytes per token" ever be below 1? ____________ Why? ________________________________

**W3.** Without a calculator: `log10(1000)` = ______  `log10(1)` = ______  `log10(0.01)` = ______  `10 ** -1` = ______

**W4.** Week 17's TinyGPT trained for 1,500 steps on a training text of 6,274 characters, and so read it about ______ times over. (Look it up in your Week 17 notes if you must.) Today's text pool is 4,179,973 characters long; one run reads it about ______ of a time.

**W5.** Week 19's rule for a fair ablation: change ______ thing, and keep the ______ , the ______ and the ______ the same.

---

## 📈 Page 21.1 — The Straight-Line Trick (15 min, pen first)

A **power law** is a curve like `y = 100 / x`. Drawn on ordinary axes it bends. The trick of the day is that once you take the `log10` of **both** columns, it is a straight line. Nothing is run until Part B.

**Predict first.** For `y = 100 / x`, every time `x` is multiplied by 10, `y` is multiplied by ____________ .

### Part A — PRACTICE (three power laws, pencil only)

**A1. `y = 100 / x`.** Fill in both tables.

| `x` | `y = 100 / x` | `log10(x)` | `log10(y)` |
|--:|--:|--:|--:|
| 10 | ______ | ______ | ______ |
| 100 | ______ | ______ | ______ |
| 1,000 | ______ | ______ | ______ |

Each step of 1 to the right in `log10(x)` moves `log10(y)` by ______ . So the slope is ______ .

**A2. `y = 1 / x^2`** (that is `1` divided by `x` times `x`).

| `x` | `y` | `log10(x)` | `log10(y)` |
|--:|--:|--:|--:|
| 1 | ______ | ______ | ______ |
| 10 | ______ | ______ | ______ |
| 100 | ______ | ______ | ______ |

Slope: ______

**A3. `y = 1000 / x^3`.** Do it *without* a table first: from A1 and A2, guess the slope: ______ . Then check with a table at `x` = 1, 10, 100. `y` = ______ , ______ , ______ . `log10(y)` = ______ , ______ , ______ . Slope: ______ .

**A4.** Complete the sentence from your three results: *"When both axes are logged, a power law is a ______ line, and the slope is the ______ ."*

**A5. From a slope to a ratio.** If a line on log-log paper has slope `s`, then **multiplying `x` by 10 multiplies `y` by `10 ** s`** and multiplying `x` by 2 multiplies `y` by `2 ** s`. Fill in (calculator; three decimals):

| slope `s` | `10 ** s` | `2 ** s` |
|--:|--:|--:|
| -1 | ______ | ______ |
| -2 | ______ | ______ |
| -0.5 | ______ | ______ |
| -0.3 | ______ | ______ |

**A6.** A line has slope **-0.3**. A student says "so ten times the data loses 30%." Say in one sentence why that is wrong. ________________________________________________

### Part B — YOURS (`powerlaw.py` from the chapter)

Run it. Copy what it printed.

| Quantity | My run printed |
|---|:--:|
| `log10(y)` column | ________________ |
| slope / intercept | ________ / ________ |
| `10 ** intercept` | ________ |

**B1.** Does `10 ** intercept` give back a number you can see in `y = 100 / x`? Which? ________

**B2.** Why does a ruler need the *logged* picture to draw a prediction? ________________________________________________

---

## 🔮 Page 21.2 — Your Sweep and Your Line (25 min)

Four TinyGPTs that differ **only in width**: 16, 32, 64, 128. Same text, same 1,500 steps, same seed. The number of knobs is the number Week 16's hand formula gives.

**Predict before you run `sweep.py`.** (Look back at the Start Here guess in the chapter.)

| Guess | My number |
|---|:--:|
| Loss of the width-16 model (14,549 knobs) | ________ |
| Loss of the width-128 model (458,965 knobs) | ________ |
| Will the four losses fall in a straight line on **ordinary** axes? (yes / no) | ________ |

### Part A — PRACTICE (a SHORT sweep, 300 steps, that is not yours)

I trained the same four widths for only **300 steps** instead of 1,500 (a quick version of `sweep.py`; file `check212.py` in the answers). Here is what it printed, with the logs added:

| Width | Knobs | Loss | `log10(knobs)` | `log10(loss)` |
|--:|--:|:--:|:--:|:--:|
| 16 | 14,549 | 2.7459 | 4.1628 | ________ |
| 32 | 41,173 | 2.5256 | 4.6146 | ________ |
| 64 | 131,285 | 2.3303 | 5.1182 | ________ |
| 128 | 458,965 | 2.1188 | 5.6618 | 0.3261 |

**A1.** Fill the blank `log10(loss)` cells (four decimals).

**A2. The ruler slope, by hand, from the first and last point.**
`slope = (log10(loss) at 128 - log10(loss) at 16) / (log10(knobs) at 128 - log10(knobs) at 16)` = (________ - ________) / (________ - ________) = ________

**A3.** Ten times the knobs multiplies the loss by `10 ** slope` = ________ . Twice the knobs: `2 ** slope` = ________ .

**A4. The prediction, by hand.** Width 256 has 1,704,149 knobs, and `log10(1,704,149)` = 6.2315. Start at the last point and keep going along the ruler line:
`y at 256 = 0.3261 + slope x (6.2315 - 5.6618)` = ________ , so the loss is `10 ** y` = ________ .
Write it as: *"My line says the width-256 model scores ________ ."*

**A5. Characters per knob.** Each 300-step run reads `300 x 32 x 64 = 614,400` characters. For width 16 that is `614,400 / 14,549` = ________ characters per knob. For width 128: `614,400 / 458,965` = ________ . For width 256: ________ .

### Part B — YOURS (`sweep.py` and `fit.py` from class, and the Draw the Line card)

Run `sweep.py`, then `fit.py`. Copy their output.

| Width | Knobs | Loss | `log10(knobs)` | `log10(loss)` | Characters per knob (`3,072,000 /` knobs) |
|--:|--:|:--:|:--:|:--:|:--:|
| 16 | ________ | ________ | ________ | ________ | ________ |
| 32 | ________ | ________ | ________ | ________ | ________ |
| 64 | ________ | ________ | ________ | ________ | ________ |
| 128 | ________ | ________ | ________ | ________ | ________ |

**B1. Plot and draw, before `fit.py`.** Mark the four points on the grid (`x` = `log10(knobs)`, `y` = `log10(loss)`; each `.` is one grid crossing). Lay a ruler so it passes as close as you can to all four, draw the line, and extend it right to `x = 6.23`.

```text
   y
 0.40 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.35 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.30 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.25 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.20 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.15 .  .  .  .  .  .  .  .  .  .  .  .  .
 0.10 .  .  .  .  .  .  .  .  .  .  .  .  .
      4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4 5.6 5.8 6.0 6.2 6.4   x
```

**B2.** Two points far apart on **your** line: (____ , ____) and (____ , ____). Slope = rise / run = ________ (it should be between about -0.10 and -0.14).

**B3.** Read `y` on your line at `x = 6.23`: `y` = ________ . Loss = `10 ** y` = ________ .

**B4. In ink.** Write it with a pen, and do not change it later:

> **"My line says the width-256 model scores ________ ."**

**B5.** Ten times the knobs multiplies the loss by `10 ** slope` = ________ . Twice the knobs: ________ .

**B6. The computer's line.** From `fit.py`: slope ________ , intercept ________ , `loss = ________ x knobs^(________)`.
Ten times the knobs multiplies the loss by ________ ; twice the knobs by ________ .
Prediction for width 256: ________ . Is it close to your ink number? By how much? ________

**B7.** `fit.py` printed how far the line is from each of the four points. Fill in: ________ % , ________ % , ________ % , ________ % . Which point is the line furthest from? ________

---

## ⚖️ Page 21.3 — Predict, Then Check (25 min)

Now train the fifth model. Your prediction is already in ink on page 21.2.

### Part A — PRACTICE (misses, by hand and on the short sweep)

**A1. A signed miss.** `miss = 100 x (measured / predicted - 1)`. Give the sign and the size, and say **too hopeful** (the model did worse than the line said) or **too gloomy**.

| Predicted | Measured | Miss (%) | Too hopeful or too gloomy? |
|:--:|:--:|:--:|:--:|
| 1.90 | 2.09 | ________ | ________ |
| 1.50 | 1.35 | ________ | ________ |

**A2.** On the short sweep from page 21.2, I trained the width-256 model for 300 steps as well. It scored **2.0093**. Using your hand prediction from 21.2 A4 (or the computer's: **1.9215**), the miss is ________ % . (Three decimals of division; one decimal in the answer.)

**A3.** The short sweep's miss and the real sweep's miss (you will see yours in Part B) are **different experiments**. The short sweep also had a different slope: about -0.075 against the real sweep's -0.126. Give **one** reason that could explain why 300 steps gave a flatter line, and say whether anyone *tested* it today. Reason: ________________________________ Tested? ________

**A4. What a reasonable reader says.** Which of these would you accept from a student who has one miss? Tick one. ☐ "Scaling laws are wrong." ☐ "The line fitted four models and missed the fifth by X%; I do not yet know why." ☐ "The model is bad." ☐ "I will change my prediction to the measured number so it looks right."

### Part B — YOURS (`check.py`, about 90 seconds)

Run `check.py`. Copy the output.

| Quantity | My run printed |
|---|:--:|
| width 256 knobs | ________ |
| measured validation loss | ________ |
| line predicted | ________ |
| the line was too hopeful by | ________ % |
| slope with four points / five points | ________ / ________ |

**B1. On the Draw the Line card, box 7.** Your ink number: ________ . Measured: ________ . Signed miss of **your hand line**: ________ % ( too hopeful / too gloomy ).

**B2. Characters per knob.** Fill from `check.py`: 211 / ________ / ________ / ________ / ________ . What changed for the biggest model? ________________________________

**B3. Candidate reasons.** You have one miss. Here are five explanations. For each, write **what it would predict** if it were the cause, and whether the course **tested** it (yes / no). You do not need the answer key to write what it would predict.

| Candidate | What it would predict | Tested in class? |
|---|---|:--:|
| Luck of the seed | ______________________________ | ____ |
| The learning rate was wrong for width 256 | ______________________________ | ____ |
| Too little text for so many knobs | ______________________________ | ____ |
| The law is not a straight line past the four points | ______________________________ | ____ |
| Depth, context length or batch size matter | ______________________________ | ____ |

**B4. Your three sentences.** Say (1) what the line predicted and what happened, with both numbers; (2) one reason you can rule out and why; (3) one you cannot rule out and why.

(1) ________________________________________________________________

(2) ________________________________________________________________

(3) ________________________________________________________________

**B5. Optional (homework).** Run `train_one(16, seed=1)` and `train_one(32, seed=1)` from a short file of your own. Loss at width 16, seed 1: ________ (seed 0: ________ ). Width 32, seed 1: ________ (seed 0: ________ ). The difference at width 32 is ________ . The line's distance from the width-32 point was ________ in loss. What does that say about "every point is within 3% of the line"? ________________________________

---

## ⏱️ Page 21.4 — Your Computer's Speed and the Price of a Run (25 min)

`C = 6ND`: operations in a run is about 6 x knobs x characters read. It is a **rule of thumb from Module 4**, and today you test it with a stopwatch.

**Predict before you run `flops.py`.** How many operations a second do you think your computer can do, one thread, best case? Write a guess as a power of ten: ____________ a second. For width 128, do you think `C = 6ND` will predict the time to within a factor of 2? (yes / no) ______

### Part A — PRACTICE (`C = 6ND` on paper, then in Python)

Every run in class reads `D = 1500 x 32 x 64` characters. **A1.** `D` = ________________ .

**A2.** A model with **50,000 knobs**, same `D`: `C = 6 x 50,000 x D` = ________ operations. On a machine that does `1 x 10^12` operations a second, the predicted time is `C / 10^12` = ________ seconds.

**A3. Week 17.** Your Week 17 TinyGPT has 807,196 knobs. Same `D`: `C` = ________ . At `1.6 x 10^12` a second: ________ seconds. In Week 17 it took about 80 seconds. The ratio `measured / predicted` = ________ .

**A4. Reading a ratio.** A table says: width 16, predicted 0.2 s, measured 10.0 s; width 128, predicted 5.4 s, measured 40.0 s (these seconds are made up for practice). Ratios: ________ and ________ . Is the measured time **faster** or **slower** than predicted? ________ Which model is further from its prediction? ________ Give **two** reasons the stopwatch would be slower than `6ND`, and say whether they were **tested**:

1. ________________________________ Tested? ____
2. ________________________________ Tested? ____

**A5. A model nobody here trained** (Module 4's assumption, arithmetic only): `N` = 7 x 10^9 knobs, `D` = 1.4 x 10^12 tokens. `C = 6ND` = ________ . How many years at `1 x 10^12` operations a second (one year is 31,536,000 seconds)? ________ . At `1.6 x 10^12`? ________ . Module 4 *assumed* an accelerator doing `4 x 10^14` a second: ________ years. Which of these three rates was measured on a computer you have touched? ________

### Part B — YOURS (`flops.py`, after `sweep.py` and `check.py`)

Run `flops.py`. Copy what it printed (the rates change every run, so note the time of day):

| Multiply size | Billion operations per second |
|--:|:--:|
| 32 x 32 | ________ |
| 128 x 128 | ________ |
| 512 x 512 | ________ |
| 1024 x 1024 | ________ |

Best-case rate used below: ________ billion a second = ________ x 10^12 .

| Width | Knobs | `C = 6ND` | Predicted s | Measured s | Measured / predicted |
|--:|--:|:--:|:--:|:--:|:--:|
| 16 | ________ | ________ | ________ | ________ | ________ |
| 32 | ________ | ________ | ________ | ________ | ________ |
| 64 | ________ | ________ | ________ | ________ | ________ |
| 128 | ________ | ________ | ________ | ________ | ________ |
| 256 | ________ | ________ | ________ | ________ | ________ |

**B1.** Check one row by hand. Width ______: `6 x ______ x 3,072,000` = ________ . Divided by your rate ________ = ________ s. Does it match the printed row? ________

**B2.** Down the ratio column, does the gap grow or shrink as the model gets bigger? ________ Two reasons from A4 that could explain it (you have not tested them): ________________________________

**B3.** The printed line for the 7-billion-knob model on **your** laptop says ________ years. Would you train it on this computer? One sentence, using a number: ________________________________

---

## 🧬 Page 21.5 — Fingerprints (20 min)

`hashlib.md5` turns any bytes into 32 characters. The same bytes always give the same 32; a different byte gives a different 32. That makes it a cheap test for "**exactly the same line**".

**Predict before you run `dedup.py`.** Out of the training lines of 25 or more characters, I think ________ % are exact repeats of an earlier line. And out of the validation lines, I think ________ % also appear in the training text.

### Part A — PRACTICE (eight lines, then thirteen)

**A1. The practice card.** Line 1 is `open the red door slowly`.

```text
   1  open the red door slowly
   2  Open the red door slowly
   3  open the red door slowly
   4  open the red door slowly␣␣        (two spaces at the end)
   5  open the red door quickly
   6  open the␣␣red door slowly         (two spaces in the middle)
   7  ␣␣␣open the red door slowly       (three spaces at the start)
   8  open the red door slowly.         (a full stop at the end)
```

Tick, before you run anything:

- **A.** Lines md5 calls "the same as line 1", exactly as written: ________
- **B.** Lines that match after `.strip()` is applied to both: ________
- **C.** Lines a human would call "the same thing" that md5 still never matches, **even after `.strip()`**: ________

**A2. Thirteen lines.** This is a tiny "code file". Count by eye.

```text
    1  import os
    2  raise NotImplementedError
    3  x = compute_total(items, tax)
    4  raise NotImplementedError
    5  return None
    6  x = compute_total(items, tax)
    7  x = compute_total(items, tax)
    8  pass
    9  y = compute_total(items, tax)
   10  if value is None: return default
   11  pass
   12  raise NotImplementedError␣          (one space at the end)
   13  return None
```

- Counting **all 13 lines exactly as written**, how many are distinct? ________
- Now `.strip()` every line and keep only lines of **12 or more characters**. How many lines are left? ________ How many are distinct? ________ How many are repeats? ________ As a share of the lines left: ________ %
- Count the repeats without the length filter (13 lines, after `.strip()`): distinct ________ , so ________ repeats = ________ % of 13. Which lines made the share change? ________________
- Now call the **first six** of the kept lines "training" and the **last two** "validation". How many validation lines also appear in training? ________ (This is a **leak**.)

**A3.** Line 9 differs from line 3 by **one letter**. Does md5 catch it as a near-duplicate? ________ Say why in one sentence. ________________________________

### Part B — YOURS (`card.py` and `dedup.py`)

**B1. The chapter's Fingerprint card** (`the baker opened her door` and seven variants). Run `card.py` and copy: lines that match line 1 raw: ________ ; after `.strip()`: ________ .

**B2. Run `dedup.py`.** Copy:

| Quantity | My run printed |
|---|:--:|
| training lines of 25+ characters | ________ |
| distinct fingerprints | ________ |
| repeats (lines - distinct) | ________ |
| share of lines that are repeats | ________ % |
| validation lines of 25+ characters | ________ |
| of those also in the training text | ________ |
| share | ________ % |

**B3.** The most repeated line and how many times: ________________________________ . Is that an innocent repeat or a copied page? Why? ________________________________

**B4.** The last three lines of `dedup.py`'s output: trailing space, matches? ______ ; after `.strip()`? ______ ; variable renamed? ______ .

**B5.** Finish the sentence: *"md5 finds lines that are ______________ the same; it cannot see a line that is the same except for ______________ or ______________ , so near-duplicates ______________ ."*

**B6.** A leak of some percent means the validation loss might be **flattering** the model. Which test would tell you how much? You do not have to run it. ________________________________ Did the course run it? ________

---

## 🧾 Page 21.6 — What Was and Was Not Measured (15 min)

Use **only** your own numbers from 21.2 to 21.5.

**Measured** (list at least **four**, each with its number):

1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________

**Not measured** (list at least **four**; "we did not test ..."):

1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________

**The report paragraph.** Write 4 to 6 sentences for a reader who was not in class: what you built, what the line predicted and what happened, what the cost arithmetic says about your computer, what the fingerprints found. **Rule:** no sentence about "big models" or "AI" in general.

________________________________________________________________

________________________________________________________________

________________________________________________________________

________________________________________________________________

**Confidence.** On a scale of 1 to 5, how far do you trust "the loss falls as a straight line on log-log paper" as a statement about **your five models**? ____ About **models in general**? ____ Say in a few words why they differ. ________________________________

---

## 🐞 Page 21.7 — Break It on Purpose (25 min)

Four files below are **deliberately** wrong, and three of the four do **not** print an error. For each: **read, predict what it prints, run, compare**, then fix. Run them from the folder with your class files (`sweep.csv`, `textpool.py`). Your numbers in bug C will differ in their digits because they depend on your seconds; the pattern will not.

### Bug A (SILENT): the line is fitted to the raw numbers

```python
# DELIBERATE BUG 21.7-A (SILENT): the line is fitted to the raw knobs and losses, not to their logs. It runs and it is a line.
import numpy as np
from trainer import knob_count

rows = [line.split(",") for line in open("sweep.csv").read().split("\n") if line]
N = np.array([float(r[1]) for r in rows])
L = np.array([float(r[2]) for r in rows])

slope, intercept = np.polyfit(N, L, 1)                       # <- should be np.polyfit(np.log10(N), np.log10(L), 1)
for size in (456000, 1704149, 3000000):
    print(f"{size:9d} knobs: the line says a validation loss of {slope * size + intercept:.3f}")
```

**A.1** Predict: will this crash? ______ Will the lines it prints look sensible? ______

**A.2** Run it. Copy the three lines: ________________________________________________

**A.3** What is impossible about one of them? ________________________________ Why did the error not stop the program? ________________________________

**A.4** Fix it (one line) and say what you must also change on the way out, when you turn the answer back into a loss: ________________________________________________

### Bug B (loud): a fingerprint of text

```python
# DELIBERATE BUG 21.7-B (loud): md5 is handed text, not bytes.
import hashlib

card = ["open the red door slowly", "open the red door slowly"]
prints = [hashlib.md5(line).hexdigest() for line in card]    # <- md5 only takes bytes
print(prints[0] == prints[1])
```

**B.1** Run it. Last line of the error: ________________________________________________

**B.2** Which week taught you the fix? ______ The fix: ________________________________

### Bug C (SILENT): `D` is the number of steps

```python
# DELIBERATE BUG 21.7-C (SILENT): D is taken to be the number of STEPS, not the number of characters read.
rows = [line.split(",") for line in open("sweep.csv").read().split("\n") if line]
RATE = 1.5e12                                                # a rate like the one flops.py printed
D = 1500                                                     # <- should be 1500 * 32 * 64
for r in rows[:4]:
    N, seconds = int(r[1]), float(r[3])
    predicted = 6 * N * D / RATE
    print(f"width {r[0]:>3}: predicted {predicted:.5f} s   measured {seconds:.1f} s   measured / predicted {seconds / predicted:,.0f}")
```

**C.1** Predict: how many steps does the loop say the model took, and how many characters did it read? Steps ______ , characters per step ______ , so `D` should be ______ .

**C.2** Run it. The last column is: ________ , ________ , ________ , ________ . How many digits is that? ______ Is a ratio that big believable? ________

**C.3** Fix it and copy the new ratio for width 16: ________

### Bug D (SILENT): repeats counted over every line

```python
# DELIBERATE BUG 21.7-D (SILENT): "exact repeats" counted over EVERY line, including blank lines and '}' and 'pass'.
import hashlib
from textpool import pool

n_cut = int(0.9 * len(pool))
lines = [ln.strip() for ln in pool[:n_cut].split("\n")]      # <- no  if len(ln) >= 25  filter
prints = set(hashlib.md5(ln.encode("utf-8")).hexdigest() for ln in lines)
print("lines:", len(lines), "  distinct:", len(prints))
print(f"'exact repeats': {100 * (len(lines) - len(prints)) / len(lines):.1f}% of the lines")
print("blank lines:", sum(1 for ln in lines if ln == ""), "  lines under 25 characters (blanks included):", sum(1 for ln in lines if len(ln) < 25))
```

**D.1** Predict the share of "exact repeats" (circle): under 5% / around 10% / over 30%. ________

**D.2** Run it and copy: lines ________ , distinct ________ , share ________ % . Blank lines ________ ; lines under 25 characters ________ .

**D.3** Is `pass` a copied page? ________ Which line of the file hides that the honest answer is 10.4%? ________________________________

**D.4** Fix it (one line) and run it. Copy the share: ________ %

**Debugging habit (write it out).** *When a number looks very good or very bad for no reason, I check ________ before I believe it.* ________________________________

---

## 📓 Page 21.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Add a row for every real error you hit this week, not only the deliberate ones.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more; three of this week's four deliberate bugs were silent): write the one I made, or nearly made. ________________________________________________

**The habit for silent mistakes.** Fill in the blanks: *when a fitted line gives a loss below ______ I check whether I fitted to the ______ of the numbers or to the numbers themselves*; *when a ratio has five or six digits I check what I used for ______* ; *when a share is far bigger than I expected I check what I ______ out before I counted*.

Write this sentence in your own handwriting:

> **"A line through four points describes those four points; whether it predicts a fifth, I have to check."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **In one sentence: what is pretraining, and which loss does it use?**

________________________________________________________________

2. **`y = 1 / x^2`. What are its slope on log-log paper and what does ten times `x` do to `y`?**

________________________________________________________________

3. **Your sweep gave a slope of about -0.126. In words, what does ten times the knobs do to the loss? Why is "it loses 12.6%" wrong?**

________________________________________________________________

4. **The line predicted one number and the fifth model scored another. Report the miss as a signed number, name one explanation the course ruled out and one it could not.**

________________________________________________________________

5. **Write `C = 6ND` and say what each letter is. For which model did you compute it this week, and did the stopwatch agree?**

________________________________________________________________

6. **What can md5 find in a training text, and what can it not? Give a line that slips through.**

________________________________________________________________

7. **Name one thing today's results do not tell you about any real language model.**

________________________________________________________________

Tick what you can do without looking: ☐ take `log10` of a power law and read the slope ☐ turn a slope into "ten times the knobs multiplies the loss by ..." ☐ write a prediction in ink and report a signed miss ☐ estimate the time of a run with `6ND` ☐ fingerprint a line and say what it misses ☐ spot a silent bug by checking a number against common sense

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Numbers below came from real runs (`/tmp` scratch folder, Python 3.10, torch 2.2.1, numpy 1.26.4, one thread, seed 0). The check files are for checking your reading; the practice numbers are not your results. Where a number is a **time** (seconds, operations a second, or a ratio made from them) yours will differ by 10 to 15% or more from mine; losses, knob counts and duplicate counts should match to every digit.

### Warm-Up

W1: **556** (256 + 300). W2: **No**: every token is at least one byte, so bytes per token cannot be below 1. W3: **3, 0, -2, 0.1**. W4: about **490** times (1,500 x 32 x 64 = 3,072,000 characters read, over 6,274); today **0.73** of a pass (3,072,000 over 4,179,973; `pool_facts.py` prints it). W5: **one** thing; keep the **seed**, the **steps** and the **data** the same (and score on the same batches). Accept these in any order.

### Page 21.1

Predict: multiplied by **0.1**.

Check file (`check211.py`); its printed output is below.

```python
# check211.py - Week 21 workbook page 21.1: logs of two power laws, and what a slope does. PRACTICE numbers.
import numpy as np

print("y = 100 / x")
for x in (10, 100, 1000):
    y = 100 / x
    print(f"  x {x:5d}  y {y:7.4f}  log10(x) {np.log10(x):5.2f}  log10(y) {np.log10(y):5.2f}")
print("y = 1 / x^2")
for x in (1, 10, 100):
    y = 1 / x ** 2
    print(f"  x {x:5d}  y {y:7.4f}  log10(x) {np.log10(x):5.2f}  log10(y) {np.log10(y):5.2f}")
print("y = 1000 / x^3  (page 21.1 part A, question A4)")
for x in (1, 10, 100):
    y = 1000 / x ** 3
    print(f"  x {x:5d}  y {y:9.6f}  log10(x) {np.log10(x):5.2f}  log10(y) {np.log10(y):5.2f}")
sl, ic = np.polyfit(np.log10([1, 10, 100]), np.log10([1000, 1, 0.001]), 1)
print(f"  slope {sl:.2f}  intercept {ic:.2f}")
print("what ten times x does to y, for a slope s:")
for s in (-1, -2, -0.5, -0.126, -0.3):
    print(f"  slope {s:6.3f}: 10 ** s = {10 ** s:.3f}   2 ** s = {2 ** s:.3f}")
```

```text
y = 100 / x
  x    10  y 10.0000  log10(x)  1.00  log10(y)  1.00
  x   100  y  1.0000  log10(x)  2.00  log10(y)  0.00
  x  1000  y  0.1000  log10(x)  3.00  log10(y) -1.00
y = 1 / x^2
  x     1  y  1.0000  log10(x)  0.00  log10(y)  0.00
  x    10  y  0.0100  log10(x)  1.00  log10(y) -2.00
  x   100  y  0.0001  log10(x)  2.00  log10(y) -4.00
y = 1000 / x^3  (page 21.1 part A, question A4)
  x     1  y 1000.000000  log10(x)  0.00  log10(y)  3.00
  x    10  y  1.000000  log10(x)  1.00  log10(y)  0.00
  x   100  y  0.001000  log10(x)  2.00  log10(y) -3.00
  slope -3.00  intercept 3.00
what ten times x does to y, for a slope s:
  slope -1.000: 10 ** s = 0.100   2 ** s = 0.500
  slope -2.000: 10 ** s = 0.010   2 ** s = 0.250
  slope -0.500: 10 ** s = 0.316   2 ** s = 0.707
  slope -0.126: 10 ** s = 0.748   2 ** s = 0.916
  slope -0.300: 10 ** s = 0.501   2 ** s = 0.812
```

**A1.** `y` = 10, 1, 0.1; `log10(x)` = 1, 2, 3; `log10(y)` = 1, 0, -1. Each step right by 1 moves `log10(y)` by **-1**; slope **-1**. **A2.** `y` = 1, 0.01, 0.0001; `log10(x)` = 0, 1, 2; `log10(y)` = 0, -2, -4; slope **-2**. **A3.** Guess **-3**; table: `y` = 1000, 1, 0.001; `log10(y)` = 3, 0, -3; slope **-3**. **A4.** *"straight", "exponent"*: a power law is a straight line on log-log axes and the slope is the exponent. **A5.** -1: 0.100 and 0.500; -2: 0.010 and 0.250; -0.5: 0.316 and 0.707; -0.3: 0.501 and 0.812. **A6.** A slope is not a percentage; ten times the data multiplies the loss by `10 ** -0.3` = **0.501**, so it about halves it (loses about 50%), not 30%.

**B.** Your run (`powerlaw.py`): `log10(y)` = `[ 1.  0. -1.]`; slope **-1.0**, intercept **2.0**; `10 ** intercept` = **100.0**. B1: yes, the **100** in `y = 100 / x`. B2: a ruler can only extend a straight line; the logged picture is straight, so the line can be extended to where no point was measured (the risk of doing so is page 21.3).

### Page 21.2

Predict: no single right answer. For reference: losses were 2.2760 and 1.4991; on ordinary axes the four points **curve** (bending), not a straight line. Accept any guess written in ink before the run.

Practice check file (`check212.py`, about 1 minute); its printed output is below.

```python
# check212.py - Week 21 workbook pages 21.2 and 21.3: a SHORT sweep (300 steps instead of 1,500) so you can see the same idea on numbers that are not yours. PRACTICE numbers. (About 1 minute.)
import numpy as np
from trainer import train_one, knob_count

N, L = [], []
for d in (16, 32, 64, 128):
    knobs, loss, seconds = train_one(d, steps=300)
    N.append(knobs)
    L.append(loss)
    print(f"width {d:3d}  knobs {knobs:7d}  validation loss {loss:.4f}  log10(knobs) {np.log10(knobs):.4f}  log10(loss) {np.log10(loss):.4f}")

x, y = np.log10(N), np.log10(L)
slope, intercept = np.polyfit(x, y, 1)
print(f"\nslope {slope:.4f}  intercept {intercept:.4f}")
print(f"ruler from the first and last point: slope {(y[3] - y[0]) / (x[3] - x[0]):.4f}")
big = knob_count(256)
predicted = 10 ** (slope * np.log10(big) + intercept)
print(f"10 times the knobs multiplies the loss by {10 ** slope:.3f}; twice the knobs by {2 ** slope:.3f}")
print(f"PREDICTION for width 256 ({big} knobs): {predicted:.4f}")

knobs, measured, seconds = train_one(256, steps=300)
print(f"width 256 measured {measured:.4f};  miss {100 * (measured / predicted - 1):+.1f}%")
print(f"characters read per knob (300 x 32 x 64 = {300 * 32 * 64}): " + ", ".join([f"{300 * 32 * 64 / n:.1f}" for n in N + [knobs]]))
```

```text
width  16  knobs   14549  validation loss 2.7459  log10(knobs) 4.1628  log10(loss) 0.4387
width  32  knobs   41173  validation loss 2.5256  log10(knobs) 4.6146  log10(loss) 0.4024
width  64  knobs  131285  validation loss 2.3303  log10(knobs) 5.1182  log10(loss) 0.3674
width 128  knobs  458965  validation loss 2.1188  log10(knobs) 5.6618  log10(loss) 0.3261

slope -0.0745  intercept 0.7479
ruler from the first and last point: slope -0.0751
10 times the knobs multiplies the loss by 0.842; twice the knobs by 0.950
PREDICTION for width 256 (1704149 knobs): 1.9215
width 256 measured 2.0093;  miss +4.6%
characters read per knob (300 x 32 x 64 = 614400): 42.2, 14.9, 4.7, 1.3, 0.4
```

**A1.** `log10(loss)` = **0.4387, 0.4024, 0.3674** (0.3261 given). **A2.** (0.3261 - 0.4387) / (5.6618 - 4.1628) = -0.1126 / 1.4990 = **-0.0751** (the computer's best line: -0.0745). **A3.** `10 ** -0.0751` = **0.841** (the computer's slope gives **0.842**); `2 ** -0.0751` = **0.949** (computer: **0.950**). **A4.** `0.3261 + (-0.0751)(0.5697)` = 0.3261 - 0.0428 = **0.2833**; `10 ** 0.2833` = **1.92** (the computer's prediction: **1.9215**). **A5.** 42.2; 1.3; `614,400 / 1,704,149` = **0.4**.

**B.** Reference (seed 0; your losses should match to every digit, and so should knobs):

| Width | Knobs | Loss | `log10(knobs)` | `log10(loss)` | Characters per knob |
|--:|--:|:--:|:--:|:--:|:--:|
| 16 | 14,549 | 2.2760 | 4.1628 | 0.3572 | 211.1 |
| 32 | 41,173 | 2.0878 | 4.6146 | 0.3197 | 74.6 |
| 64 | 131,285 | 1.7127 | 5.1182 | 0.2337 | 23.4 |
| 128 | 458,965 | 1.4991 | 5.6618 | 0.1758 | 6.7 |

`fit.py` prints the same table and then: `np.polyfit` slope **-0.1262**, intercept **0.8886**, `loss = 7.737 x knobs^(-0.1262)`; ten times the knobs multiplies the loss by **0.748**, twice the knobs by **0.916**; the line is off by **-1.4%, +3.1%, -2.1%, +0.4%** (furthest from the 32 or the 64 point); prediction for width 256 (1,704,149 knobs): **1.2654**. **By hand** with a ruler your slope is likely between -0.11 and -0.13 and your prediction between about 1.25 and 1.30 (a ruler through the first and last point gives slope -0.121 and 1.279). **Accept any prediction written in ink before 21.3.** B1: the furthest point is the 32 or the 64.

### Page 21.3

**A1.** 2.09 / 1.90 - 1 = **+10.0%**, too hopeful (the model did worse than the line said); 1.35 / 1.50 - 1 = **-10.0%**, too gloomy. **A2.** 2.0093 / 1.9215 - 1 = **+4.6%** (with the hand prediction 1.92 it is +4.7%; a difference in the last digit is fine). **A3.** One reason, any of: with only 300 steps every model is far from trained, so the losses are all high and flatter in size (the bigger model has not had time to use its extra knobs); the characters per knob are different (page 21.2 A5). **Tested? No**: nobody varied the number of steps to test this; what was measured is that the slope is -0.075 against -0.126. **A4.** The second: *"The line fitted four models and missed the fifth by X%; I do not yet know why."* The others are not accepted ("scaling laws are wrong" and "the model is bad" are verdicts, not measurements; changing a prediction after the fact defeats the point).

**B.** `check.py` prints (your knobs and losses should match):

```text
width 256: knobs 1704149  validation loss 1.4656  (87 s)
line predicted 1.2654   measured 1.4656   the line was too hopeful by 15.8%
```

Characters per knob **211 / 75 / 23 / 6.7 / 1.8**; slope with four points **-0.1262**, with five points **-0.1008** (flatter). B1: your own hand line is off by a different signed number; it should be **positive** (too hopeful) if your ink number is 1.25 to 1.30: for 1.279 the miss is +14.6%. B2: the biggest model got **1.8** characters per knob against **211** for the smallest.

B3, with what the course measured:

| Candidate | Would predict | What was measured |
|---|---|---|
| Luck of the seed | the miss changes sign or size with another seed | **Ruled out**: three seeds gave +15.8%, +15.5%, +17.4% |
| Learning rate wrong for width 256 | a better rate closes the gap | **Ruled out**: rates 1e-3, 2e-3, 3e-3, 5e-3 gave 1.5035, 1.4564, 1.4656, 1.4976; the best, 1.4564, is far above 1.2654 |
| Too little text for so many knobs (1.8 characters per knob) | twice the characters helps the big model more than the small ones | **Not supported by a doubling**: 3,000 steps helped width 256 by 0.127 and width 128 by 0.123; the miss stayed +17.3%. A 20-per-knob diet for width 256 (about 34 million characters) was **not** tried |
| The law is not straight past the four points | a fifth point flattens the slope | **Consistent**: slope -0.126 to -0.101 |
| Depth, context length, batch size | changing them changes the curve | **Not tested** |

(Those numbers come from the teacher's longer runs; you did not run them, and your "Tested in class?" column should say so.) B4 model: *"The line fitted the four models, predicted 1.265 for the fifth, and the fifth scored 1.466, 16% worse. It is not luck (three seeds) and not just the learning rate. The biggest model got 1.8 characters per knob against 211 for the smallest, which is my best guess, but twice the text did not close the gap and I cannot test it with enough text here."* B5: `train_one(16, seed=1)` = **2.2848** (seed 0: 2.2760); `train_one(32, seed=1)` = **2.0507** (seed 0: 2.0878, a difference of 0.037). The line's distance from the width-32 point is +3.1%, 0.064 in loss, about the size of the three-seed spread there (0.051): the line fits **to within the noise** at the small sizes.

### Page 21.4

Predict: no single right answer; a laptop's one-thread best case is around 10^12.

Check file (`check214.py`); its printed output is below.

```python
# check214.py - Week 21 workbook page 21.4: C = 6 * N * D by hand, then by Python. PRACTICE numbers.
D = 1500 * 32 * 64
print("D =", D)
for N, rate, label in ((50000, 1e12, "a 50,000-knob model on a 1-trillion-a-second machine"),
                       (807196, 1.6e12, "Week 17's TinyGPT at 1.6 trillion a second"),
                       (2000000, 5e11, "a 2-million-knob model at half a trillion a second")):
    C = 6 * N * D
    print(f"{label}: C = {C:.3e}  predicted {C / rate:.1f} s")
print()
print("a table that was timed (made-up seconds, to practise reading the ratio):")
for width, N, predicted, measured in ((16, 14549, 0.2, 10.0), (128, 458965, 5.4, 40.0)):
    print(f"  width {width}: measured / predicted = {measured / predicted:.1f}")
N7, D7 = 7e9, 1.4e12
print(f"\n7e9 knobs, 1.4e12 tokens: C = {6 * N7 * D7:.2e}")
for rate in (1e12, 1.6e12, 4e14):
    sec = 6 * N7 * D7 / rate
    print(f"  at {rate:.1e} a second: {sec:.2e} s = {sec / 86400:,.0f} days = {sec / 31536000:,.1f} years")
```

```text
D = 3072000
a 50,000-knob model on a 1-trillion-a-second machine: C = 9.216e+11  predicted 0.9 s
Week 17's TinyGPT at 1.6 trillion a second: C = 1.488e+13  predicted 9.3 s
a 2-million-knob model at half a trillion a second: C = 3.686e+13  predicted 73.7 s

a table that was timed (made-up seconds, to practise reading the ratio):
  width 16: measured / predicted = 50.0
  width 128: measured / predicted = 7.4

7e9 knobs, 1.4e12 tokens: C = 5.88e+22
  at 1.0e+12 a second: 5.88e+10 s = 680,556 days = 1,864.5 years
  at 1.6e+12 a second: 3.68e+10 s = 425,347 days = 1,165.3 years
  at 4.0e+14 a second: 1.47e+08 s = 1,701 days = 4.7 years
```

**A1.** 1500 x 32 x 64 = **3,072,000**. **A2.** `6 x 50,000 x 3,072,000` = **9.216 x 10^11**; at 10^12 a second: **0.9** s. **A3.** `6 x 807,196 x 3,072,000` = **1.488 x 10^13**; at 1.6 x 10^12: **9.3** s; measured 80 s; ratio 80 / 9.3 = **about 8.6**. **A4.** 10.0 / 0.2 = **50.0**; 40.0 / 5.4 = **7.4**. **Slower** than predicted; the width-16 model is further off. Two reasons (any two): small tables run well below the best rate (a 32 x 32 multiply does 60 to 90 billion a second against about 1,500 billion for 512 x 512); the softmax, layer norm, GELU, the optimizer and Python bookkeeping are not counted in `6ND`; `6ND` ignores the attention table. **None was tested.** **A5.** `C` = **5.88 x 10^22**; at 10^12: **1,864.5** years; at 1.6 x 10^12: **1,165.3** years; at 4 x 10^14: **4.7** years (1,701 days). Only a laptop's rate was ever measured; 4 x 10^14 is **quoted from Module 4, not measured**.

**B.** Reference (quiet laptop, one of several runs; the seconds and rates move by 10 to 15% from run to run):

```text
matrix multiply speed on one thread (2*n*n*n operations per multiply):
     32 x 32        0.001 ms per multiply    76.9 billion operations per second
    128 x 128       0.005 ms per multiply   911.4 billion operations per second
    512 x 512       0.177 ms per multiply  1513.4 billion operations per second
   1024 x 1024      1.496 ms per multiply  1435.1 billion operations per second

best-case rate used below: 1513 billion operations per second
characters per run D = 3072000

 width      N = knobs      C = 6*N*D    predicted s   measured s   measured / predicted
    16         14,549      2.682e+11          0.2         12.1           68.2
    32         41,173      7.589e+11          0.5         14.4           28.8
    64        131,285      2.420e+12          1.6         20.7           13.0
   128        458,965      8.460e+12          5.6         36.8            6.6
   256      1,704,149      3.141e+13         20.8         86.7            4.2

the worked example from Module 4 (hypothetical, arithmetic only): N = 7e9 knobs, D = 1.4e12 tokens
  C = 5.88e+22 operations;  on this laptop, one thread: 3.89e+10 s = 1,232 years
```

The ratio runs from about 68 at width 16 down to about 4 at width 256. B1: for width 128, `6 x 458,965 x 3,072,000` = 8.460 x 10^12; at 1.513 x 10^12 that is 5.6 s (5.4 s at 1.553 x 10^12); yours uses your own rate. B2: the gap **shrinks** as the model grows (bigger tables run closer to the best speed, and a larger share of the work is the big multiplies: believed, not tested). B3: a sentence with a number, for example *"at my rate the 7-billion-knob example would take about 1,200 years, so no"* (1,165 to 1,232 years for the rates seen).

### Page 21.5

Predict: no single right answer; the measured values are below.

Check file (`check215.py`); its printed output is below.

```python
# check215.py - Week 21 workbook page 21.5: a tiny dedup, by hand and then by md5. PRACTICE numbers.
import hashlib

def fingerprint(line):
    return hashlib.md5(line.encode("utf-8")).hexdigest()

card = ["open the red door slowly", "Open the red door slowly", "open the red door slowly", "open the red door slowly  ",
        "open the red door quickly", "open the  red door slowly", "   open the red door slowly", "open the red door slowly."]
for k, line in enumerate(card, 1):
    raw = fingerprint(line) == fingerprint(card[0])
    stripped = fingerprint(line.strip()) == fingerprint(card[0].strip())
    print(f"line {k}: raw {raw}  after .strip() {stripped} |{line}|")

log = ["import os", "raise NotImplementedError", "x = compute_total(items, tax)", "raise NotImplementedError",
       "return None", "x = compute_total(items, tax)", "x = compute_total(items, tax)", "pass",
       "y = compute_total(items, tax)", "if value is None: return default", "pass", "raise NotImplementedError ", "return None"]
print("\nall lines:", len(log), " distinct:", len(set([fingerprint(l) for l in log])))
long = [l.strip() for l in log if len(l.strip()) >= 12]
print("lines of 12+ characters:", len(long), " distinct:", len(set([fingerprint(l) for l in long])), " repeats:", len(long) - len(set([fingerprint(l) for l in long])))
train = long[:6]
val = long[6:]
tp = set([fingerprint(l) for l in train])
print("train", train)
print("val", val)
print("leaked:", [l for l in val if fingerprint(l) in tp])
```

```text
line 1: raw True  after .strip() True |open the red door slowly|
line 2: raw False  after .strip() False |Open the red door slowly|
line 3: raw True  after .strip() True |open the red door slowly|
line 4: raw False  after .strip() True |open the red door slowly  |
line 5: raw False  after .strip() False |open the red door quickly|
line 6: raw False  after .strip() False |open the  red door slowly|
line 7: raw False  after .strip() True |   open the red door slowly|
line 8: raw False  after .strip() False |open the red door slowly.|

all lines: 13  distinct: 8
lines of 12+ characters: 8  distinct: 4  repeats: 4
train ['raise NotImplementedError', 'x = compute_total(items, tax)', 'raise NotImplementedError', 'x = compute_total(items, tax)', 'x = compute_total(items, tax)', 'y = compute_total(items, tax)']
val ['if value is None: return default', 'raise NotImplementedError']
leaked: ['raise NotImplementedError']
```

**A1.** **A** = lines 1 and 3; **B** = lines 1, 3, 4, 7; **C** = lines 2 (a capital), 6 (a doubled space) and possibly 8 (a full stop) and 5 (a different word, so a different sentence; accept a reasoned yes or no). **A2.** Distinct as written: **8**. After `.strip()` and the 12-character filter: **8** lines left, **4** distinct, **4** repeats = **50.0%**. Without the length filter (13 stripped lines): distinct are `import os`, `raise NotImplementedError`, `x = compute_total(items, tax)`, `return None`, `pass`, `y = compute_total(items, tax)`, `if value is None: return default` = **7**, so **6** repeats = **46.2%**, and short lines like `pass` and `return None` repeat innocently (the first count, as written, has 8 distinct because of the trailing space in line 12). Leak: **1** (`raise NotImplementedError`). **A3.** **No**: one letter changed means a completely different fingerprint, so md5 only finds **exact** copies.

**B1.** Chapter card: raw lines 1 and 2; after `.strip()` lines 1, 2, 4, 6. **B2.** Reference (your values should match exactly):

```text
training lines (25+ characters): 55978   distinct fingerprints: 50155
exact repeats a dedup pass would delete: 5823 lines = 10.4% of the lines
...
validation lines (25+ characters): 6343   also found in the training text: 327 = 5.2%
```

**B3.** Most repeated: `raise NotImplementedError`, 57 times (then `a = _convert_other(a, raiseit=True)`, 56; `if __name__ == '__main__':`, 35). It is an **innocent** repeat (a line that many files legitimately contain), not a copied page. **B4.** `False` , `True` , `False`. **B5.** *"md5 finds lines that are **exactly** the same; it cannot see a line that is the same except for **a space** or **a renamed variable**, so near-duplicates **slip through**."* **B6.** Remove the 327 leaked lines from the validation text and score the model again (not run). **No**: the course did not run it; the effect of the 5.2% overlap on the loss is **not measured**.

### Page 21.6

Any four **measured**, each with a number: the losses of five widths; the slope -0.126 (and -0.101 with five points); the miss 15.8% (15.5 to 17.4% over three seeds); the learning-rate rows; the 3,000-step rows; the operations a second of one laptop; `6ND` against seconds; 10.4% repeats; 5.2% leak. Any four **not measured**: the cause of the miss; a 20-per-knob diet for width 256; any other depth, context or batch size; a learning rate tuned per width; a GPU; what the repeats or the leak do to the loss; near-duplicates; any real pretraining; any named model. **Not accepted:** any sentence about "big models" or "AI" in general. The confidence question has no single answer: a good one gives a higher number for the five models than for models in general.

### Page 21.7

**Bug A.** Printed:

```text
   456000 knobs: the line says a validation loss of 1.445
  1704149 knobs: the line says a validation loss of -0.460
  3000000 knobs: the line says a validation loss of -2.437
```

A.1: it does not crash; the first line looks sensible (1.445 for 456,000 knobs, close to the real 1.4991). A.3: a **negative loss** (-0.460, -2.437) is impossible for a loss of this kind; it runs because `np.polyfit` will fit a line to any numbers, and a straight line on **raw** numbers keeps falling forever. A.4: `np.polyfit(np.log10(N), np.log10(L), 1)`; and on the way out, undo the log with `10 ** (slope * np.log10(size) + intercept)`.

**Bug B.** Printed:

```text
Traceback (most recent call last):
  File "/private/tmp/w21wb/bugB.py", line 5, in <module>
    prints = [hashlib.md5(line).hexdigest() for line in card]    # <- md5 only takes bytes
  File "/private/tmp/w21wb/bugB.py", line 5, in <listcomp>
    prints = [hashlib.md5(line).hexdigest() for line in card]    # <- md5 only takes bytes
TypeError: Strings must be encoded before hashing
```

B.2: Week **20** (`.encode("utf-8")`). Fix: `hashlib.md5(line.encode("utf-8")).hexdigest()`.

**Bug C.** Printed (your digits differ with your seconds; the size does not):

```text
width  16: predicted 0.00009 s   measured 12.1 s   measured / predicted 138,436
width  32: predicted 0.00025 s   measured 14.4 s   measured / predicted 58,411
width  64: predicted 0.00079 s   measured 20.7 s   measured / predicted 26,321
width 128: predicted 0.00275 s   measured 36.8 s   measured / predicted 13,346
```

C.1: 1,500 steps; each step reads 32 x 64 = **2,048** characters; `D` = **3,072,000**. C.2: five or six digits; **not believable**, because the predicted time is thousands of times too small (`D` is 2,048 times too small). C.3: with `D = 1500 * 32 * 64` the width-16 ratio is about **68** (yours differs a little).

**Bug D.** Printed:

```text
lines: 117376   distinct: 72940
'exact repeats': 37.9% of the lines
blank lines: 17695   lines under 25 characters (blanks included): 61398
```

D.1: the honest answer is around 10%; this bug says **37.9%** (over 30%). D.3: **No**: `pass` and `}` repeat innocently; 17,695 blank lines and 61,398 lines under 25 characters are what inflate it; the honest 10.4% is the line that filters with `len(ln) >= 25`. D.4: add `if len(ln) >= 25` to the comprehension (the 10.4% comes from `dedup.py`'s count over the same 90% of the text).

Habit blank: *when a number looks very good or very bad for no reason, I check **what it was computed from** before I believe it.*

### Page 21.8 and Self-Check

The Bug Log has no single right answer. The blanks: *when a fitted line gives a loss below **zero** I check whether I fitted to the **logs** of the numbers or to the numbers themselves*; *when a ratio has five or six digits I check what I used for **`D`***; *when a share is far bigger than I expected I check what I **filtered** out before I counted*. Self-Check model answers: (1) training on a lot of text with only "what comes next?" as the job; the same per-character next-token loss as Week 17; (2) slope **-2**; ten times `x` multiplies `y` by **0.01**; (3) the loss is multiplied by **0.748** (2.28 becomes about 1.70); a slope is an exponent on a ratio, not a percentage; (4) *"+15.8%, too hopeful"*; ruled out: luck of the seed (three seeds) or the learning rate; not ruled out: too little text per knob (1.8 against 211 characters per knob), depth/context/batch size, the curve not being straight; (5) `C = 6ND`: `C` operations in the run, `N` knobs, `D` characters read; the stopwatch said the run was **slower** than predicted, by a ratio that fell from about 68 to about 4 as the model grew; (6) md5 finds **exact** repeated lines (10.4% of the 25+ character lines) and leaks (5.2%); it misses a line differing by a space before `.strip()`, a capital, or a renamed variable; (7) any of: no model was trained at scale; one text pool and one seed per width (three seeds for the miss only); no GPU; no other depth; the effect of the repeats or the leak on the loss was not measured; nothing was said about any named model.

---

## 🔮 Next Week Preview

**Week 22 — After Pretraining: SFT, Reward Model, DPO.** A pretrained model is a good continuer of text and a poor assistant. You will fine-tune on prompt-and-answer pairs but hide the prompt from the loss, teach a tiny reward model from preferences and find a feature it can be fooled by, and run DPO at two values of a setting called `beta`. The one new maths idea is **KL divergence**, "how far did the leash let you move". It is the same loss family as today, applied after pretraining. Keep from this week: the habit of writing a prediction before a check, the knowledge that a loss is per character on a particular text, and the warning that a toy result shows a mechanism, not a rate.
