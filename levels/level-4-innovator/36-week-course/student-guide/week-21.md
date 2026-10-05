# Week 21 — Pretraining and the Scaling Arithmetic

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Workbook](../workbook/week-21.md)

---

> ### This week in one sentence
> **You train four TinyGPTs that differ only in width, draw one straight line through their four losses on log-log paper, write down in ink what that line says about a fifth and bigger model, train the fifth to check, and then measure two things that matter at real scale: how many operations a training run costs, and how many of the lines in your text are exact copies.**
>
> **By the end of this chapter you will be able to:**
> - **Say what pretraining is:** the same next-character loss as Week 17, at a scale where the data and the budget are the hard parts
> - **Turn a power law into a straight line** by taking the `log10` of both columns, and read the slope as "what ten times the knobs does to the loss"
> - **Fit that line** to four trained models with `np.polyfit`, and **write a prediction before the check**
> - **Report a miss as a signed number** (`+15.8%`), not as a verdict, and say which explanations the course tested and which it did not
> - **Time your own computer** with a matrix multiply, and estimate the cost of a run with `C = 6ND`
> - **Fingerprint lines of text** with `hashlib.md5`, count exact duplicates, and find lines that leaked from the training text into the validation text
>
> **New maths:** **one idea**: the **log-log straight line**. A power law becomes a straight line when both axes are logged, and the slope is the exponent. You meet it on three numbers before it gets its name. **New syntax:** **three**: `np.polyfit(x, y, 1)`, `np.log10`, and `hashlib.md5`. **One small mirror rides along:** `.hexdigest()`, the way you ask `md5` for its 32 characters.
>
> **Reading time:** about 30 minutes. **In class:** 70 minutes (two runs of about 90 seconds each sit inside it). **Homework:** about 60 to 75 minutes (workbook pages 21.1 to 21.6).

> **📌 About the code blocks.** Every file has its name in its first line. Type them into **one folder, next to your `l4lib/` folder and your own Week 17 `tinygpt.py`**, and run them from that folder. Two files are **given** (`textpool.py`, `trainer.py`): you read them, you do not type them. Every output shown was printed by a real run on a CPU, with one thread, Python 3.10.10, torch 2.2.1, numpy 1.26.4. **Everything is seeded** (`torch.manual_seed` inside `train_one`; the validation windows are fixed, not drawn at random), so **your losses, knob counts and duplicate counts should match to every printed digit. Only the timings in brackets, like `(12 s)`, and the speeds in `flops.py` change from computer to computer and from minute to minute.** If you have a different Python version, the text pool is a little different and every loss moves a little; the shapes should not. There is **no scripted backend and no stand-in** anywhere this week: the five models are real, trained on your computer today. Nothing is downloaded and nothing needs the internet. Two runs take about a minute and a half each (`sweep.py` and `check.py`); **close other programs before you run them**, because the timings and the speeds are disturbed by other work.

---

## 🪝 Start Here

Here is a guess to make before any computer is switched on. Write it on a card and keep it.

> A model with **14,549 knobs** scores a loss of **2.28** on some text. You train another with **10 times as many knobs** (about 145,000), on the same text, for the same number of steps. Its loss is:
> **(a)** 0.228 (ten times smaller) **(b)** about 1.7 **(c)** 2.28, no change.

Do not look ahead. Pick a letter. Then a second, harder guess: *how sure are you?* Write a number from 1 (a pure guess) to 5 (certain).

Everything you have built since Week 14 is the real thing at toy size. Today's job has a name: **pretraining**. You train on a lot of text with no questions and no answers, only *"what comes next?"*. The loss is the **Week 17 loss**: how surprised the model is by the true next character, averaged. Nothing about the loss is new.

What changes with scale is that two things stop being ideas and become **engineering problems**:

1. **The data.** Is it clean? Is some of it copied? Did the test text leak into the training text?
2. **The budget.** How many operations does the run need, and how long will *your* machine take?

And there is a third thing, which is the lesson today is built around: **a straight line through a few points is a true description of those points. Whether it is also a prediction is something you have to check.**

---

## 🧠 The Big Idea

### 1. A power law, with no name yet

Take `y = 100 / x`. Try three values of `x`:

| `x` | `y` |
|--:|--:|
| 10 | 10 |
| 100 | 1 |
| 1,000 | 0.1 |

Every time `x` is multiplied by 10, `y` is multiplied by 0.1: **the same fraction every time**. Drawn on ordinary axes that is a curve that bends. Now take the **`log10`** of each number. (`log10` asks "how many factors of ten?": `log10(1000)` is 3, `log10(1)` is 0, `log10(0.1)` is -1.) Run this:

```python
# powerlaw.py - Week 21: a power law, with no name yet. y = 100 / x, then the logs of both columns.
import numpy as np

x = np.array([10, 100, 1000])
y = 100 / x
print("x        ", x)
print("y        ", y)
print("log10(x) ", np.log10(x))
print("log10(y) ", np.log10(y))

slope, intercept = np.polyfit(np.log10(x), np.log10(y), 1)
print("slope", round(slope, 3), " intercept", round(intercept, 3))
print("undo the log with 10 **:", 10 ** np.log10(1000), " and 10 ** intercept =", round(10 ** intercept, 3))
```

```text
x         [  10  100 1000]
y         [10.   1.   0.1]
log10(x)  [1. 2. 3.]
log10(y)  [ 1.  0. -1.]
slope -1.0  intercept 2.0
undo the log with 10 **: 1000.0  and 10 ** intercept = 100.0
```

Look at the last two rows. `log10(x)` goes 1, 2, 3 and `log10(y)` goes 1, 0, -1: each step right by 1 goes **down by 1**. That is a **straight line with slope -1**. `np.polyfit` finds it for you, and `10 ** intercept` turns the intercept back into the 100 in `y = 100 / x`.

**This is the whole idea.** A curve like `y = 100 / x` is called a **power law**, and *a power law becomes a straight line once both axes are logged. The slope of the line is the exponent.* A ruler can only extend a straight line, so this is what lets you draw a prediction.

### 2. What a slope means: a ratio, not a percentage

If a line on log-log paper has slope `s`, then **multiplying `x` by 10 multiplies `y` by `10 ** s`**. For `y = 100 / x`, `s = -1` and `10 ** -1 = 0.1`, which is exactly what you saw. Say the result **as a ratio**, because the ratio is the thing that stays the same. A slope of -0.126 does *not* mean "lose 0.126" and it does *not* mean "lose 12.6%". You will compute what it does in a few minutes.

### 3. Two rules of thumb you will use today

- **`C = 6ND`.** `N` is the number of knobs, `D` is the number of characters the run reads, and `C` is the number of operations (additions and multiplications of ordinary numbers) in the whole run. A forward pass costs about `2` operations per knob per character (a multiply and an add), the backward pass about twice that, so about `6` altogether. This is a **rule of thumb from Module 4, used here as arithmetic**. You will test it against a stopwatch.
- **Operations per second** (written **FLOP/s**, "floating-point operations per second"; just say "operations a second"). Multiplying two `n` by `n` tables takes about `2 x n x n x n` operations. Time one and divide: that is how fast *your computer* is.

### 4. The new syntax

Three new constructs, and one small mirror.

| Construct | What it does | Example |
|---|---|---|
| `np.log10(x)` | the base-10 logarithm of a number, or of every number in an array. Undo it with `10 ** y`. | `np.log10(1000)` is `3.0` |
| `np.polyfit(x, y, 1)` | the best straight line through the points `(x, y)`; the `1` means "a line". It **returns two numbers, the slope first and the intercept second.** "Best" means the smallest total squared miss (you met squared errors in Level 2): think of a ruler that uses all the points at once. | `slope, intercept = np.polyfit(x, y, 1)` |
| `hashlib.md5(b)` | a **fingerprint**: any bytes go in, 32 letters-and-digits come out. The same text always gives the same 32; different texts give different ones. You must `import hashlib`, and you must hand it **bytes**, which is why you meet `.encode("utf-8")` from Week 20 again. | `hashlib.md5("hi".encode("utf-8"))` |
| `.hexdigest()` *(mirror)* | what you call on the thing `md5` returns, to get the 32 characters as a string. Say it as one phrase: "md5 of the bytes, as hex digits". | `hashlib.md5(b).hexdigest()` |

Everything else in today's files you have already met: `zip`, list comprehensions, `set`, `Counter` (Week 20), `open(...).read()`, f-strings with format specs, `lambda` and `LambdaLR` (Week 4), `clip_grad_norm_` (Week 6), `time.perf_counter` (Week 17), `torch.manual_seed`, `a @ b`, `.strip()` and `.split("\n")` (Level 2), and `10 ** x`.

### 5. A fingerprint, in one look

```python
# hash_demo.py - Week 21: the first look at a fingerprint. Same text, same 32 characters. One letter changed, all different.
import hashlib

for text in ("the river ran past the town", "the river ran past the town", "the river ran past the towN"):
    print(hashlib.md5(text.encode("utf-8")).hexdigest(), "<-", text)
```

```text
29316ac3af62c94eaf8bd9267f2b3576 <- the river ran past the town
29316ac3af62c94eaf8bd9267f2b3576 <- the river ran past the town
d9d1ed4bcca4b4b8494ca96a2e355f88 <- the river ran past the towN
```

The first two lines are identical, so their fingerprints are identical. The third line differs in **one letter** (a capital `N`), and its fingerprint is completely different. That is the whole mechanism: **two lines are the same, exactly as written, if and only if their fingerprints are the same**, and comparing 32 characters is quicker than comparing whole lines. `md5` is used here only to find exact copies. It is **not** a security tool, and nothing today relies on it being hard to forge.

---

## 🏗️ Build It

### 6. `textpool.py` and `trainer.py` (given, you do not type them)

Last week your tokenizer read 6,972 characters. Today's text pool is **14 times bigger**, and it was already on your computer: it is every `.py` file sitting directly in Python's own library folder. Nothing downloads. `textpool.py` reads them all, cuts the **first 90%** off as training text and keeps the **last 10%** (different files) as the validation text, and gives you `get_batch()` and `val_loss(model)`. You are told only what the file-listing lines do (they list the files in a folder); the rest is Week 17. The important fact is in `val_loss`: **every model is scored on the same 640 validation windows**. Without that, differences between widths would include luck about which windows were drawn.

```python
# textpool.py - Week 21 (GIVEN to the student, not typed): a text pool 14 times bigger than Week 20's, and one fixed validation score.
import os
import torch

folder = os.path.dirname(os.__file__)                                   # where Python keeps its own source files
names = sorted(f for f in os.listdir(folder) if f.endswith(".py"))      # every .py file directly in that folder, in order
pool = "".join(open(os.path.join(folder, f), encoding="utf-8", errors="replace").read() for f in names)

chars = sorted(set(pool))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in pool])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]                               # the last tenth of the files is the validation text
T, B = 64, 32                                                           # places per window, windows per batch


def get_batch():
    starts = torch.randint(len(train_data) - T, (B,))
    x = torch.stack([train_data[s:s + T] for s in starts])
    y = torch.stack([train_data[s + 1:s + T + 1] for s in starts])
    return x, y


@torch.no_grad()
def val_loss(model):
    """The SAME 640 validation windows for every model (spread evenly over the validation text), averaged."""
    total = 0.0
    for i in range(20):
        starts = (torch.arange(32) + 32 * i) * 700
        x = torch.stack([val_data[s:s + T] for s in starts])
        y = torch.stack([val_data[s + 1:s + T + 1] for s in starts])
        _, loss = model(x, y)
        total += loss.item()
    return total / 20
```

`trainer.py` is your Week 17 `train.py` turned into a function. Read it for two minutes: every line is from Week 17 (the warm-up-and-cosine schedule is Week 4, the clipping Week 6). Two things are different. **It builds `TinyGPT(V, d, 2, 2, T)`: two heads and two blocks for every model, so width is the only thing that changes.** And it **returns** three numbers: `(knobs, validation loss, seconds)`. It needs your own Week 17 `tinygpt.py` in the same folder, defining `TinyGPT(V, d, H, L, T)` as you wrote it. It prints nothing.

```python
# trainer.py - Week 21: train ONE TinyGPT of a given width for a given number of steps; return (knobs, validation loss, seconds).
import math
import time
import torch
from tinygpt import TinyGPT
from textpool import V, T, get_batch, val_loss


def train_one(d, steps=1500, seed=0, lr=3e-3, warmup=100):
    torch.manual_seed(seed)
    model = TinyGPT(V, d, 2, 2, T)                                       # 2 heads, 2 blocks; only the width d changes
    knobs = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / warmup if s < warmup
                                              else 0.5 * (1 + math.cos(math.pi * (s - warmup) / (steps - warmup))))
    t0 = time.perf_counter()
    for step in range(steps):
        x, y = get_batch()
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
    seconds = time.perf_counter() - t0
    return knobs, val_loss(model), seconds


def knob_count(d, blocks=2):
    """Week 16's hand count for a TinyGPT of width d (vocabulary V, T places, `blocks` blocks)."""
    return V * d + T * d + blocks * (12 * d * d + 10 * d) + 2 * d + (d * V + V)
```

### 7. How much text does one run read?

```python
# pool_facts.py - Week 21: how big is the pool, and how much of it will one training run actually read?
from textpool import names, pool, V, train_data, val_data, T, B

STEPS = 1500
print("files:", len(names), "  characters:", len(pool), "  distinct characters (vocab):", V)
print("train:", len(train_data), "  validation:", len(val_data))
tokens_seen = STEPS * B * T
print("one run of", STEPS, "steps reads", tokens_seen, "characters =", round(tokens_seen / len(train_data), 2), "passes over the training text")
print("Week 17, for comparison: 1500 steps read", 1500 * 32 * 64, "characters of a 6,274-character training text =", round(1500 * 32 * 64 / 6274), "passes")
```

```text
files: 170   characters: 4644415   distinct characters (vocab): 213
train: 4179973   validation: 464442
one run of 1500 steps reads 3072000 characters = 0.73 passes over the training text
Week 17, for comparison: 1500 steps read 3072000 characters of a 6,274-character training text = 490 passes
```

**0.73 passes**: in one run, the model does not even read the training text once on average. In Week 17 it read its text 490 times. That is why the validation loss is honest today: the model is **not memorising**.

### 8. The sweep: four widths, everything else the same

`sweep.py` trains widths 16, 32, 64 and 128, each for exactly **1,500 steps of 32 windows of 64 characters = 3,072,000 characters**, seed 0, and saves the result to a file. Saving matters: the slow part (about 90 seconds) is done **once**, and you can redo the fitting as often as you like. Start it now, then do the card in the next section while it runs.

```python
# sweep.py - Week 21: train four widths with everything else the same, and save (width, knobs, validation loss, seconds) to sweep.csv.
from trainer import train_one

WIDTHS = [16, 32, 64, 128]
rows = []
for d in WIDTHS:
    knobs, loss, seconds = train_one(d)
    rows.append((d, knobs, loss, seconds))
    print(f"width {d:3d}  knobs {knobs:7d}  validation loss {loss:.4f}  ({seconds:.0f} s)")

with open("sweep.csv", "w") as f:
    for d, knobs, loss, seconds in rows:
        f.write(f"{d},{knobs},{loss},{seconds}\n")
print("saved sweep.csv")
```

```text
width  16  knobs   14549  validation loss 2.2760  (12 s)
width  32  knobs   41173  validation loss 2.0878  (15 s)
width  64  knobs  131285  validation loss 1.7127  (21 s)
width 128  knobs  458965  validation loss 1.4991  (36 s)
saved sweep.csv
```

The file it wrote (`sweep.csv`) has four rows, `width,knobs,loss,seconds`; the losses are the same every run, and the seconds are not. **Knobs** is how many numbers the model has (14,549 to 458,965); the loss is *validation* loss in nats per character on text the model never trained on. These losses are not comparable with Week 17's: different text, different vocabulary (213 distinct characters now, not 28).

### 9. The Draw the Line card (with a ruler, before the next file)

Copy this onto a card or a page. **Fill it from your own `sweep.py` output.**

```text
Four models, same text, same number of steps. Fill in from YOUR sweep.py output:

   width   knobs      log10(knobs)   loss    log10(loss)
    16     14,549        4.16        ____       ____
    32     41,173        4.61        ____       ____
    64    131,285        5.12        ____       ____
   128    458,965        5.66        ____       ____

   1. Plot the four points on a grid (x = log10 of knobs, y = log10 of loss).
      Suggested grid: x from 4.0 to 6.4 in steps of 0.2; y from 0.10 to 0.40 in steps of 0.05.
   2. Lay the ruler so it passes as close as you can to all four. Draw the line.
      Extend it to the right as far as x = 6.23 (that is width 256: log10(1,704,149)).
   3. Pick two points on YOUR line, far apart. Slope = rise / run = ______
   4. Read y on your line at x = 6.23:  y = ______    Loss = 10 ** y = ______
   5. WRITE IT IN INK:  "My line says width 256 scores ______."   (Do not change this later.)
   6. Ten times the knobs multiplies the loss by  10 ** slope = ______ .   Twice the knobs: 2 ** slope = ______ .
   7. AFTER check.py:  measured ______   my line was off by ______ %  (too hopeful / too gloomy)
```

Use a calculator for the `log10` columns (the `log10` button) or wait for `fit.py`, which prints them. **Box 5 is the point of the card.** A prediction written after you have seen the answer is not a prediction. Once it is in ink, you do not touch it.

### 10. `fit.py`: the same line, by the computer

```python
# fit.py - Week 21: a power law is a straight line on log-log paper. Fit it to the four widths, then PREDICT the width-256 model.
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from trainer import knob_count

rows = [line.split(",") for line in open("sweep.csv").read().split("\n") if line]
N = np.array([float(r[1]) for r in rows])                # knobs
L = np.array([float(r[2]) for r in rows])                # validation loss

x, y = np.log10(N), np.log10(L)
print("   knobs    log10(knobs)   loss    log10(loss)")
for i in range(len(N)):
    print(f"{N[i]:8.0f}   {x[i]:.4f}      {L[i]:.4f}   {y[i]:.4f}")

slope, intercept = np.polyfit(x, y, 1)                   # the best straight line through the four points
a = 10 ** intercept
print(f"\nline: log10(loss) = {slope:.4f} * log10(knobs) + {intercept:.4f}")
print(f"same thing as a law: loss = {a:.3f} * knobs^({slope:.4f})")
print(f"so 10 times the knobs multiplies the loss by {10 ** slope:.3f}, and 2 times the knobs by {2 ** slope:.3f}")

fitted = 10 ** (slope * x + intercept)
for i in range(len(N)):
    print(f"  knobs {N[i]:7.0f}: measured {L[i]:.4f}  line says {fitted[i]:.4f}  off by {100 * (L[i] / fitted[i] - 1):+.1f}%")

N_big = knob_count(256)
predicted = 10 ** (slope * np.log10(N_big) + intercept)
print(f"\nPREDICTION for width 256 ({N_big} knobs, {N_big / N[-1]:.1f} times the biggest so far): validation loss {predicted:.4f}")

fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
grid = np.linspace(x.min(), np.log10(N_big), 50)
left.plot(N, L, "o-")
left.plot(N_big, predicted, "*", markersize=14, label="prediction (width 256)")
left.set_xlabel("knobs")
left.set_ylabel("validation loss")
left.set_title("ordinary axes: a curve")
left.legend()
right.plot(x, y, "o")
right.plot(grid, slope * grid + intercept, "--", label=f"line, slope {slope:.3f}")
right.plot(np.log10(N_big), np.log10(predicted), "*", markersize=14)
right.set_xlabel("log10(knobs)")
right.set_ylabel("log10(validation loss)")
right.set_title("both axes logged: a line")
right.legend()
fig.savefig("scaling.png")
print("saved scaling.png")
```

```text
   knobs    log10(knobs)   loss    log10(loss)
   14549   4.1628      2.2760   0.3572
   41173   4.6146      2.0878   0.3197
  131285   5.1182      1.7127   0.2337
  458965   5.6618      1.4991   0.1758

line: log10(loss) = -0.1262 * log10(knobs) + 0.8886
same thing as a law: loss = 7.737 * knobs^(-0.1262)
so 10 times the knobs multiplies the loss by 0.748, and 2 times the knobs by 0.916
  knobs   14549: measured 2.2760  line says 2.3082  off by -1.4%
  knobs   41173: measured 2.0878  line says 2.0242  off by +3.1%
  knobs  131285: measured 1.7127  line says 1.7487  off by -2.1%
  knobs  458965: measured 1.4991  line says 1.4932  off by +0.4%

PREDICTION for width 256 (1704149 knobs, 3.7 times the biggest so far): validation loss 1.2654
saved scaling.png
```

Read it in four bites.

1. The two middle columns are the logs. Compare them with your card.
2. `slope, intercept = np.polyfit(x, y, 1)`: the **slope comes first**. The line is `log10(loss) = -0.1262 x log10(knobs) + 0.8886`. Turned back into a power law with `10 ** intercept`, it is `loss = 7.737 x knobs^-0.1262`.
3. **Ten times the knobs multiplies the loss by 0.748**, and doubling multiplies it by 0.916. Go back to the guess on your first card: 2.28 times 0.748 is about 1.70, so **(b)**. Not "ten times smaller", and not "no change". Compare your ruler slope with -0.1262: they should agree to within a couple of hundredths.
4. The line against the four points: **-1.4%, +3.1%, -2.1%, +0.4%**. Every point is within about 3% of the line. Remember that the **+3.1%** is the biggest, because we will come back to it.

The last line is the **PREDICTION** for width 256: **1.2654**. Compare it with the number in ink on your card (yours will be 1.25 to 1.30 if your ruler was careful). `fit.py` also saved `scaling.png`: open it. The left plot is the curve on ordinary axes; the right plot is the line with both axes logged.

### 11. `check.py`: train the fifth model and compare

This trains a width-256 model (1,704,149 knobs, 3.7 times the biggest so far) and will take about a minute and a half. **Your prediction must already be written in ink.** The file repeats three lines of `fit.py` so that it runs on its own.

```python
# check.py - Week 21: train the width-256 model and compare it with what the line PREDICTED. (About 2 minutes.)
import numpy as np
from trainer import train_one, knob_count

rows = [line.split(",") for line in open("sweep.csv").read().split("\n") if line]
N = np.array([float(r[1]) for r in rows])
L = np.array([float(r[2]) for r in rows])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
predicted = 10 ** (slope * np.log10(knob_count(256)) + intercept)

knobs, measured, seconds = train_one(256)
print(f"width 256: knobs {knobs}  validation loss {measured:.4f}  ({seconds:.0f} s)")
print(f"line predicted {predicted:.4f}   measured {measured:.4f}   the line was too hopeful by {100 * (measured / predicted - 1):.1f}%")

with open("check.csv", "w") as f:
    f.write(f"256,{knobs},{measured},{seconds}\n")

print("\ncharacters read per knob (3,072,000 characters in every run):")
for n_i, l_i in zip(list(N) + [knobs], list(L) + [measured]):
    print(f"  knobs {n_i:8.0f}: {3072000 / n_i:6.1f} characters per knob   loss {l_i:.4f}")

N5 = np.array(list(N) + [knobs])
L5 = np.array(list(L) + [measured])
slope5, intercept5 = np.polyfit(np.log10(N5), np.log10(L5), 1)
print(f"\nslope with four points {slope:.4f}, with five points {slope5:.4f}")
```

```text
width 256: knobs 1704149  validation loss 1.4656  (87 s)
line predicted 1.2654   measured 1.4656   the line was too hopeful by 15.8%

characters read per knob (3,072,000 characters in every run):
  knobs    14549:  211.1 characters per knob   loss 2.2760
  knobs    41173:   74.6 characters per knob   loss 2.0878
  knobs   131285:   23.4 characters per knob   loss 1.7127
  knobs   458965:    6.7 characters per knob   loss 1.4991
  knobs  1704149:    1.8 characters per knob   loss 1.4656

slope with four points -0.1262, with five points -0.1008
```

Fill box 7 of your card. The model scored **1.4656** and the line said **1.2654**: the model is **15.8% worse than the line said**. Say that as a number with a sign, not as a verdict. Look at the table below it: at the top, each knob has **1.8 characters** to learn from; at the bottom, **211**. And look at the last line: with the fifth point included the slope is **-0.1008**. The line got flatter.

**Why did the line miss?** We do not know. Here is what *can* be said, and it is deliberately short.

---

## 🔬 What the miss does and does not show

The course author ran three extra checks that you do **not** run, each against the same five widths. They are reported here so you know which explanations have been ruled out. (The author's runs are real; they simply take 8 to 11 minutes each.)

- **Is it luck?** Three seeds. The miss was **+15.8%, +15.5% and +17.4%**. It is not luck. But the width-32 model moved by 0.051 in loss between seeds, which is about 2.5% of its value, so your "+3.1%" at width 32 is **the size of seed noise**: the line fits the four points *to within the noise*, and no better.
- **Is it only the learning rate?** Four rates (1e-3, 2e-3, 3e-3, 5e-3) for widths 128 and 256. The best width-256 loss was **1.4564**, still far above the prediction of 1.2654. So it is **not only the learning rate**. A footnote on tuning: the best rate was *not* the same for both widths, so using one rate for every width, as you did, is a limitation.
- **Is it that the biggest model is starved of text?** Twice the characters (3,000 steps) lowered every model's loss by about the same amount, and the width-256 miss was **+17.3%**, the same as before. Twice the text did not close the gap. The test that would settle it needs about 34 million characters per run, and the pool has 4.2 million for training. **So that explanation is not supported by a doubling, and it was not tested properly.**

**The honest sentence is:** *"The line was true of these four models and not of the fifth. It is not luck, not only the learning rate, and not fixed by twice the text. I have not shown the cause."* Two things this does **not** let you say: *"scaling laws are wrong"* (we did not test any published law, which are fitted on runs millions of times larger with settings that were tuned) and *"bigger is not better"* (we trained five small models, one depth, one text, one learning rate, one seed per point, 1,500 steps). What it **does** show is how a line through few points behaves when you push it, and that **the budget has two numbers, knobs and data, not one**.

---

## 🎲 Your Turn

### The Fingerprint card (about 4 minutes, pencil and paper, no computer)

```text
Eight lines of text. Line 1 is:   the baker opened her door

   1  the baker opened her door
   2  the baker opened her door
   3  the Baker opened her door
   4  the baker opened her door␣          (one space at the end)
   5  the baker opened the door
   6  ␣␣the baker opened her door         (two spaces at the start)
   7  the␣␣baker opened her door          (two spaces in the middle)
   8  THE BAKER OPENED HER DOOR

   A. Tick the lines that md5 will call "the same as line 1", exactly as written.    ______
   B. Tick the lines that will match after .strip() is applied to both lines.       ______
   C. Which lines would a human call "the same thing" but md5 never will?            ______
```

Fill A, B and C **before** you run anything. Then type `card.py` and check yourself.

```python
# card.py - Week 21: the Fingerprint card. Which of these eight lines does md5 call 'the same as line 1'?
import hashlib

card = ["the baker opened her door", "the baker opened her door", "the Baker opened her door", "the baker opened her door ",
        "the baker opened the door", "  the baker opened her door", "the  baker opened her door", "THE BAKER OPENED HER DOOR"]


def fingerprint(line):
    return hashlib.md5(line.encode("utf-8")).hexdigest()


for k, line in enumerate(card, 1):
    raw = fingerprint(line) == fingerprint(card[0])
    stripped = fingerprint(line.strip()) == fingerprint(card[0].strip())
    print(f"line {k}: same as line 1?  raw: {raw}  after .strip(): {stripped}  |{line}|")
```

```text
line 1: same as line 1?  raw: True  after .strip(): True  |the baker opened her door|
line 2: same as line 1?  raw: True  after .strip(): True  |the baker opened her door|
line 3: same as line 1?  raw: False  after .strip(): False  |the Baker opened her door|
line 4: same as line 1?  raw: False  after .strip(): True  |the baker opened her door |
line 5: same as line 1?  raw: False  after .strip(): False  |the baker opened the door|
line 6: same as line 1?  raw: False  after .strip(): True  |  the baker opened her door|
line 7: same as line 1?  raw: False  after .strip(): False  |the  baker opened her door|
line 8: same as line 1?  raw: False  after .strip(): False  |THE BAKER OPENED HER DOOR|
```

How many did you get right? What would you do to a line before fingerprinting it to catch line 7? And line 3? (Real pipelines do some of that, up to a point. We do not.)

### The speed of your computer and the price of a run

`flops.py` reads `sweep.csv` and `check.csv`, so run it after `check.py`. **The speeds in its first table will be different on your computer, and different again if you run it twice.** On the author's laptop the best speed was about 1.5 to 1.6 trillion operations a second when nothing else was running, and 0.5 to 0.9 when something was. Give your own speed to the nearest half, not the nearest digit.

```python
# flops.py - Week 21: how fast is THIS computer, and does C = 6 * N * D predict how long training took?
import time
import torch

torch.set_num_threads(1)                                  # the same single thread every training run used

print("matrix multiply speed on one thread (2*n*n*n operations per multiply):")
rate = {}
for n in (32, 128, 512, 1024):
    a, b = torch.randn(n, n), torch.randn(n, n)
    a @ b                                                 # one throw-away multiply to warm up
    best = 1e9
    for trial in range(5):                                # five timings; keep the fastest (the least disturbed)
        t0 = time.perf_counter()
        for _ in range(20):
            a @ b
        best = min(best, (time.perf_counter() - t0) / 20)
    secs = best
    rate[n] = 2 * n ** 3 / secs
    print(f"  {n:5d} x {n:<5d}  {secs * 1000:8.3f} ms per multiply  {rate[n] / 1e9:6.1f} billion operations per second")

RATE = max(rate.values())                                 # the fastest figure we saw: our best-case 'peak'
D = 1500 * 32 * 64                                        # characters read in one training run
print(f"\nbest-case rate used below: {RATE / 1e9:.0f} billion operations per second")
print(f"characters per run D = {D}")

rows = [line.split(",") for line in open("sweep.csv").read().split("\n") if line]
rows.append(open("check.csv").read().strip().split(","))
print("\n width      N = knobs      C = 6*N*D    predicted s   measured s   measured / predicted")
for r in rows:
    N, seconds = int(r[1]), float(r[3])
    C = 6 * N * D
    predicted = C / RATE
    print(f"{r[0]:>6} {N:14,d} {C:14.3e} {predicted:12.1f} {seconds:12.1f} {seconds / predicted:14.1f}")

print("\nthe worked example from Module 4 (hypothetical, arithmetic only): N = 7e9 knobs, D = 1.4e12 tokens")
C = 6 * 7e9 * 1.4e12
seconds = C / RATE
print(f"  C = {C:.2e} operations;  on this laptop, one thread: {seconds:.2e} s = {seconds / 86400 / 365:,.0f} years")
```

```text
matrix multiply speed on one thread (2*n*n*n operations per multiply):
     32 x 32        0.001 ms per multiply    77.7 billion operations per second
    128 x 128       0.004 ms per multiply   933.4 billion operations per second
    512 x 512       0.167 ms per multiply  1610.6 billion operations per second
   1024 x 1024      1.360 ms per multiply  1579.4 billion operations per second

best-case rate used below: 1611 billion operations per second
characters per run D = 3072000

 width      N = knobs      C = 6*N*D    predicted s   measured s   measured / predicted
    16         14,549      2.682e+11          0.2         12.1           72.9
    32         41,173      7.589e+11          0.5         15.1           32.0
    64        131,285      2.420e+12          1.5         20.8           13.8
   128        458,965      8.460e+12          5.3         35.6            6.8
   256      1,704,149      3.141e+13         19.5         87.4            4.5

the worked example from Module 4 (hypothetical, arithmetic only): N = 7e9 knobs, D = 1.4e12 tokens
  C = 5.88e+22 operations;  on this laptop, one thread: 3.65e+10 s = 1,158 years
```

Read it in three bites.

1. **The speed depends on the size of the multiply.** Tiny tables (32 by 32) are slow, 78 billion a second here; big ones (512 by 512) are fast, 1,611 billion. Your models' own tables are small.
2. **`6ND` counts operations; it does not count time.** The last column is *measured seconds divided by predicted seconds*. It is **bigger than 1 for every model, and about 73 for the smallest and 4.5 for the largest**: the bigger the model, the closer the arithmetic gets. Reasons we **believe** (and did not separate): small tables run far below the best-case speed; softmax, layer norm, GELU, the optimizer and Python's own bookkeeping are not multiplies; and `6ND` ignores the attention table. **We did not take the seconds apart**, so those are candidates, not findings.
3. **The hypothetical.** Module 4's example is a model with 7 billion knobs reading 1.4 trillion tokens: `6 x 7e9 x 1.4e12 = 5.88e22` operations. At your laptop's best speed that is over a thousand years (1,158 here). That is arithmetic, not a plan: that model would not even fit in your computer's memory.

Also: **characters per knob** is `D / N`. Your width-16 model had 211; your width-256 model had 1.8. Module 4 quotes a published rule of thumb of about **20 tokens per parameter** for training "compute-optimally". **That is quoted, not reproduced**: our units are characters, not tokens, and our models are not tuned. Compare the *idea*, not the number.

### Fingerprinting the whole pool

`dedup.py` uses fingerprints on four million characters of text. It keeps only lines with **25 or more** characters (after `.strip()`), because `}` and `pass` and blank lines repeat innocently. It counts the lines whose fingerprint has been seen before, and then asks how many **validation** lines also appear in the **training** text (a leak: the model has, in a sense, seen part of its own test).

```python
# dedup.py - Week 21: an exact-duplicate detector made from a fingerprint. hashlib.md5 turns any text into 32 hex characters.
import hashlib
from collections import Counter
from textpool import pool

for text in ("the river ran past the town", "the river ran past the town", "the river ran past the towN"):
    print(hashlib.md5(text.encode("utf-8")).hexdigest(), "<-", text)


def fingerprint(line):
    return hashlib.md5(line.encode("utf-8")).hexdigest()


n_cut = int(0.9 * len(pool))                              # the same 90/10 cut as textpool.py (characters, not files)
train_text, val_text = pool[:n_cut], pool[n_cut:]


def long_lines(text):
    lines = [ln.strip() for ln in text.split("\n")]
    return [ln for ln in lines if len(ln) >= 25]          # ignore blank and very short lines: '}' and 'pass' repeat innocently


train_lines, val_lines = long_lines(train_text), long_lines(val_text)
counts = Counter(fingerprint(ln) for ln in train_lines)
print("\ntraining lines (25+ characters):", len(train_lines), "  distinct fingerprints:", len(counts))
print(f"exact repeats a dedup pass would delete: {len(train_lines) - len(counts)} lines = {100 * (len(train_lines) - len(counts)) / len(train_lines):.1f}% of the lines")

first_seen = {}
for ln in train_lines:
    if fingerprint(ln) not in first_seen:
        first_seen[fingerprint(ln)] = ln
print("\nthe five most repeated lines:")
for digest, times in counts.most_common(5):
    print(f"  {times:4d} times: {first_seen[digest][:70]}")

train_prints = set(counts)                                # a set remembers which fingerprints exist
leaked = [ln for ln in val_lines if fingerprint(ln) in train_prints]
print(f"\nvalidation lines (25+ characters): {len(val_lines)}   also found in the training text: {len(leaked)} = {100 * len(leaked) / len(val_lines):.1f}%")

a = "    return self._append(key, value, True)"
b = "    return self._append(key, value, True) "          # the same line with one trailing space
c = "    return self._append(key, val, True)"             # the same line with one variable renamed
print("\nsame line, trailing space:  fingerprints match?", fingerprint(a) == fingerprint(b))
print("  ... after .strip() on both:  fingerprints match?", fingerprint(a.strip()) == fingerprint(b.strip()))
print("same line, variable renamed:  fingerprints match?", fingerprint(a.strip()) == fingerprint(c.strip()))
```

```text
29316ac3af62c94eaf8bd9267f2b3576 <- the river ran past the town
29316ac3af62c94eaf8bd9267f2b3576 <- the river ran past the town
d9d1ed4bcca4b4b8494ca96a2e355f88 <- the river ran past the towN

training lines (25+ characters): 55978   distinct fingerprints: 50155
exact repeats a dedup pass would delete: 5823 lines = 10.4% of the lines

the five most repeated lines:
    57 times: raise NotImplementedError
    56 times: a = _convert_other(a, raiseit=True)
    35 times: if __name__ == '__main__':
    22 times: return context._raise_error(InvalidOperation,
    20 times: Traceback (most recent call last):

validation lines (25+ characters): 6343   also found in the training text: 327 = 5.2%

same line, trailing space:  fingerprints match? False
  ... after .strip() on both:  fingerprints match? True
same line, variable renamed:  fingerprints match? False
```

Read it in three bites.

1. **10.4% of the training lines** (5,823 of 55,978) are exact repeats. The most repeated is `raise NotImplementedError` (57 times). **This is Python source, where boilerplate repeats; it is not a measurement of a web crawl.** Module 4 says deduplication "often removes 50 to 70%" of a crawl: quoted, not reproduced.
2. **327 of 6,343 validation lines (5.2%)** also appear word for word in the training text. That is a small, real leak between the two files. We did **not** remove those lines and did **not** measure what they do to the validation loss.
3. **The last three lines are the limit of the tool.** A trailing space defeats the fingerprint until you `.strip()` both lines; a renamed variable defeats it **always**. Near-duplicates need a different tool. Module 4 names one (MinHash); **we did not build or run it.**

---

## 🧭 What was shown, and what was not

**Shown:**
- Four TinyGPTs differing only in width (14,549 to 458,965 knobs) lie on a straight line on log-log paper: **slope -0.1262**, so ten times the knobs multiplies the loss by **0.748**. Every point is within 3.1% of it.
- The line predicted **1.2654** for a 1.7-million-knob model and the model scored **1.4656**, **15.8% worse**.
- Not luck (three seeds, 15.5 to 17.4%), not only the learning rate (four rates), not fixed by twice the text (+17.3%). Those three runs are the author's, not yours.
- `6ND` predicts a run time 4.5 to about 73 times too short on this computer.
- **10.4%** of the training lines are exact repeats and **5.2%** of the validation lines also sit in the training text.
- An exact fingerprint misses a trailing space until you strip it, and always misses a renamed variable.

**Not shown:**
- **Why the line missed.** We ruled some things out. We did not find the cause. We never gave width 256 the 34 million characters that would test the "starved of text" idea.
- That **scaling laws are wrong**, or that **bigger is not better**. We did not test a published law and we did not test a bigger budget.
- That the **slope** means anything outside five tiny models, one depth, one text, one learning rate, one seed each (for you), 1,500 steps.
- **Where `6ND`'s missing time goes.** We listed reasons and did not test them.
- **What duplicates or leaks do to a loss.** We counted them. We did not train with and without them.
- Anything about **GPUs**. The speed is one laptop, one thread, one moment.
- That **pretraining at scale** works like this. The biggest run read 3 million characters in about 90 seconds. A sentence like "this is how it works at scale" is a quotation, not a result.
- That **near-duplicates** are rare. We showed one that fooled the tool and counted none.

---

## 🔑 Wrap Up

1. Go back to the guess on your first card, and to your confidence number. What did you get right? What surprised you?
2. A power law, `y = 100 / x`, becomes a straight line when both axes are logged. What does the slope of that line mean?
3. Your line has slope -0.1262. By what number does ten times the knobs multiply the loss? Why is "it takes 12.6% off" wrong?
4. The line was drawn through four points and used to predict a fifth. What happened, and which three explanations were ruled out?
5. `6ND` says a run should take 5 seconds and it took 36. Give two reasons, and say which you tested.
6. What can an exact fingerprint find, and what can it not?

Then write this sentence in your Bug Log in your own handwriting:

> **"A straight line through four points describes the four; it only predicts the fifth if nothing else is limiting it, and I have to check."**

**A look ahead.** Next week the model is already pretrained, and the question is how to turn a good continuer of text into something that follows instructions. The same loss family returns.

---

## 📤 Homework

Complete workbook pages 21.1 to 21.6. Write your **predictions before you run anything**: a guess written after the run is not a guess. **Every number you write must have been printed by your own run in the last 24 hours.** The seed is the default in `train_one` (0); if you change it, say so.

**Optional.** Run `train_one(16, seed=1)` and `train_one(32, seed=1)` from a short file of your own (12 and 15 seconds). How far does each loss move from its seed-0 value? Is that bigger or smaller than the width-32 point's distance from the line (+3.1%)? Write one sentence on what that says about "every point is within 3% of the line".

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **pretraining** | training on a lot of text with only "what comes next?" as the job, before any other training |
| **power law** | `y = a x^b`: multiply `x` by a fixed amount and `y` is multiplied by a fixed amount |
| **log-log** | both axes logged; a power law is a straight line there |
| **slope (log-log)** | the exponent; `10 ** slope` is what ten times `x` does to `y` |
| **extrapolate** | to extend a line beyond the points it was drawn through |
| **`C = 6ND`** | operations in a run ≈ 6 x knobs x characters read (Module 4's rule of thumb) |
| **FLOP / FLOP/s** | one operation on an ordinary number / operations per second |
| **deduplicate** | remove exact repeats from the text |
| **fingerprint (hash)** | 32 characters computed from a text; the same text always gives the same ones |
| **contamination (leak)** | test text that also appears in the training text |
| **`np.log10`** | base-10 logarithm; undone by `10 ** y` |
| **`np.polyfit(x, y, 1)`** | the best straight line; returns the slope first, then the intercept |
| **`hashlib.md5`** | the fingerprint recipe; takes bytes, so use `.encode("utf-8")` first |
| **`.hexdigest()`** | the 32 characters, as a string |

---

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Workbook](../workbook/week-21.md)
