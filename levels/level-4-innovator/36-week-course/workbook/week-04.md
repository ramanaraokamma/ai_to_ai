# Workbook — Week 4: Schedules and Batch Size

**Name:** ________________________________  **Date:** ______________

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [📖 Read the chapter first](../student-guide/week-04.md) · [Next ➡ Week 5](week-05.md)

---

> **Rules for this workbook.** Every number you write in a report must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the Answers were produced by real runs on one CPU thread (`torch.set_num_threads(1)`). If your third decimal differs, that is fine. If the *shape* differs, tell your teacher.
>
> Run everything from inside `36-week-course/` so that `from l4lib.spirals import run` works. **Import `l4lib`. Never copy it.**
>
> **This week has no new maths.** You need only: a straight-line ramp, a cosine value off a calculator, and `//` (how many whole ones fit). **Pages 4.1 to 4.3 are paper and calculator only. No code.**
>
> **The sentence of the week:** *"What did I hold fixed?"* Say it out loud before you write any conclusion.

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 4 is highlighted with a pointer above it, weeks 1 to 3 are outlined solid, and every later tile has a dashed outline](../figures/fig-w04-0-where-this-fits.svg)
*Figure W4.0 — Where this fits: week 4 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## ✅ Warm-Up (5 min)

Five from **last week** and earlier. No looking back.

**W1.** In `w -= lr * grad`, which name is the step size? ____________

**W2.** Week 1 said a model guessing between two classes has a loss of about 0.693. In one word or symbol, where does that number come from? ____________

**W3.** A model scores 0.99 on rows it trained on and 0.61 on rows it never saw. One word for that: ____________

**W4.** Why do we run **several seeds** instead of one?

________________________________________________________________

**W5.** The dataset has 1,200 points: 840 train and 360 validation. Which of the two does a batch come from?

________________________________________________________________

---

## 📖 Page 4.1 — Match the Word to the Thing

Draw a line, or write the letter.

| Word | Letter | | Meaning |
|---|:--:|---|---|
| learning-rate schedule | ____ | **A** | A function with no name, written in one line. |
| multiplier | ____ | **B** | A smooth fall from one to zero: slow, fast, slow. |
| warmup | ____ | **C** | A rule that sets the learning rate for each step. |
| cosine decay | ____ | **D** | Two things changed at once, so you cannot say which caused the result. |
| `lambda` | ____ | **E** | A number between 0 and 1 that the peak is multiplied by. |
| steps per epoch | ____ | **F** | A short ramp at the start, from small up to the peak. |
| confound | ____ | **G** | `840 // batch`. |
| scheduler | ____ | **H** | An object attached to an optimizer that sets the rate for each step. |

**Two in your own words.** A **batch** is: ______________________________________________

A **confound** is: _____________________________________________________________

---

## 🔮 Page 4.2 — Predict the Output

Write your prediction **in pen, before** you run anything. Then run it and write what happened beside it.

**P1.**

```python
print((lambda x: x + 3)(4))
print((lambda a, b: a * b)(3, 5))
```

My prediction: ______________________ Real: ______________________

**P2.** Starting rate 0.1. The multiplier halves every step.

```python
import torch
import torch.nn as nn
w = nn.Parameter(torch.zeros(1))
opt = torch.optim.SGD([w], lr=0.1)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 ** s)
print(sched.get_last_lr())
opt.step(); sched.step()
print(sched.get_last_lr())
opt.step(); sched.step()
print(sched.get_last_lr())
```

Three lines, with brackets: ______________ ______________ ______________

**P3.** How many steps does one epoch take, and how many points are left out each epoch?

`840 // 150` = ______ steps, used `5 * 150 = ` ______ points, left out ______.

`840 // 1000` = ______. (What does that mean for training?) _______________________

**P4.** A loop calls `opt.step()` **40 times** and never calls `sched.step()`. The scheduler has a cosine rule and a starting `lr=0.02`. What does `opt.param_groups[0]["lr"]` print?

My prediction: ______________ Real: ______________

**P5.** The cosine runs on for **75 steps** when `T = 50`, with no `min`. Peak 0.02. Rate at steps 0, 25, 50, 75:

My prediction: ______ ______ ______ ______

Real: ______ ______ ______ ______

What word describes what the rate did after step 50? ______________

---

## 🔢 Page 4.3 — The Schedule, by Hand

**Calculator and graph paper. No code until the last box.**

Peak rate = **0.02**. Total steps `T` = **50**. Warmup `W` = **5** steps.

The rules (copy them onto the margin of your graph paper):

- **Cosine only:** multiplier = `0.5 * (1 + cos(pi * s / T))`
- **Warmup + cosine:**
  - if `s < W`: multiplier = `(s + 1) / W`
  - otherwise: progress = `(s - W) / (T - W)`, multiplier = `0.5 * (1 + cos(pi * progress))`
- **Rate** = `0.02 * multiplier`

> Put your calculator in **radians** mode. `pi` is 3.14159. If `cos(pi)` does not give `-1`, you are in degrees.

**M1 — Three checkpoints, no calculator needed.** Fill in the cosine-only rule.

| Where | `s / T` | angle `pi * s / T` | cosine | multiplier | rate |
|---|:--:|:--:|:--:|:--:|:--:|
| Start | 0 | 0 | | | |
| Halfway | 0.5 | | | | |
| End | 1 | | | | |

**M2 — Fill the table.** Four decimals on the multiplier, five on the rate.

| Step | Cosine multiplier | Cosine rate | Warm+cos multiplier | Warm+cos rate |
|:--:|:--:|:--:|:--:|:--:|
| 0 | | | | |
| 2 | | | | |
| 4 | | | | |
| 5 | | | | |
| 10 | | | | |
| 20 | | | | |
| 25 | | | | |
| 40 | | | | |
| 50 | | | | |

**M3 — One cell, fully shown.** Warm+cos at step **20**. Write every line.

progress = (20 - ___) / (___ - ___) = ______

angle = pi * ______ = ______

cosine = ______

multiplier = 0.5 * (1 + ______) = ______

rate = 0.02 * ______ = ______

**M4 — The "+ 1".** The ramp uses `(s + 1) / W`, not `s / W`. What rate would step 0 get without the `+ 1`? ______ What would that first step do to the weights? ___________________________

**M5 — Plot it.** On graph paper: step on the bottom (0 to 50), rate up the side (0 to 0.02). Plot both columns, two colours. Then write **two things you notice**:

1. ______________________________________________________________

2. ______________________________________________________________

**M6 — Where is the cosine falling fastest?** (Look at your table.) Around step ______. A straight line from 0.02 at step 0 to 0 at step 50 would be at ______ at step 10. The cosine is at ______. So the cosine starts (slower / faster) than a straight line.

**M7 — The verification box (now you may use code).** Write a 12-line script that builds `LambdaLR` with your warm+cos rule, and prints `get_last_lr()[0]` for steps 0, 1, 2, 3. Paste what it printed:

______________________________________________________________

Then answer: step 0 prints ______ but your table says step 0 uses ______. **Who is right?** _________________________________________________

![Line chart of learning rate against step: a dashed cosine-only curve falling from 0.003 to zero, a solid warm-up-then-cosine curve that climbs over 50 steps first, and a table of printed rates beside it](../figures/fig-w04-1-warmup-then-cosine-rate.svg)
*Figure W4.1 — The rate is the peak times a multiplier: warm-up ramps it up over 50 steps and cosine brings it down to zero.*

---

## 🔢 Page 4.4 — Counting Steps

Paper and calculator first. **Use `//`**: two slashes mean "how many whole ones fit". The harness drops the short last batch and reshuffles every epoch.

| Batch | Steps per epoch (`840 // batch`) | Points used | Points left out | Steps in 30 epochs |
|:--:|:--:|:--:|:--:|:--:|
| 24 | | | | |
| 70 | | | | |
| 150 | | | | |
| 400 | | | | |
| 420 | | | | |
| 1000 | | | | |

**C1.** Which batches in the table use **every** point? ______________ What do they have in common with 840? _________________________________

**C2.** You want **at least 1,000 steps** with batch 64. Steps per epoch: ______. Epochs needed (round **up**): ______. Steps you actually get: ______.

**C3.** Batch 8 versus batch 512, both for 60 epochs. How many times as many steps does batch 8 take? Show the division: ______________ (If you wrote 64, you divided the batch sizes. Try again from the steps-per-epoch column.)

**C4.** You want batch 120 to take about 360 steps. Epochs: ______ . Steps you get: ______ .

**C5.** Batch 420 for 60 epochs, versus batch 420 for 180 epochs. Which is "same epochs as batch 24", and which is "same steps as batch 24 at 10 epochs"? _________________________________________________

---

## 🎲 Page 4.5 — Two Experiments and a Report

You will run a grid like the class one but with **different batch sizes**, so you cannot copy the class table. Save it as `w4_grid.py`.

```python
import torch
torch.set_num_threads(1)
import numpy as np
from l4lib.spirals import run

N_TRAIN = 840
print("workbook grid: validation loss, mean of seeds 0-2")
for bs in [24, 120, 420]:
    per = N_TRAIN // bs
    same_epochs = [run("x", batch_size=bs, seed=s, verbose=False)["val"][-1] for s in range(3)]
    ep = 360 // per
    same_steps = [run("x", batch_size=bs, epochs=ep, seed=s, verbose=False)["val"][-1] for s in range(3)]
    print(f"bs {bs:>3}  60 epochs = {per * 60:>4} steps: {np.mean(same_epochs):.3f}   "
          f"{ep:>3} epochs = {per * ep:>3} steps: {np.mean(same_steps):.3f}")
```

**Before you run it, write a prediction** (better / worse / same, for batch 420 compared with batch 24, in each column):

Column 1 (60 epochs each): ______________ Column 2 (about 360 steps each): ______________

**Your run** (about 10 seconds):

| Batch | 60 epochs: steps | 60 epochs: val loss | Epochs for ~360 steps | Steps | val loss |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 24 | | | | | |
| 120 | | | | | |
| 420 | | | | | |

**R1. Fill in the template** (use words from this page, not "bigger batch is better"):

```
Column 1 held ________ fixed.  It also changed ________.
Column 2 held ________ fixed.  It also changed ________.
```

**R2.** On ______ points, with ______ seeds, I held ______ fixed. The result was ______ (mean of the seeds). That could also be because ______ changed at the same time.

______________________________________________________________

______________________________________________________________

**R3. One thing I can honestly conclude:** ______________________________________________________________

**One thing I cannot conclude:** ______________________________________________________________

**R4.** Someone says: *"Bigger batches are worse, because the gradient is less noisy."* Which column of your table would support that sentence? What else changed in that column? What would you need to see?

______________________________________________________________

______________________________________________________________

**R5 (optional).** Run the same grid with seeds `range(5, 8)`. Did the **ordering** of the rows stay the same? Did the **digits**?

______________________________________________________________

![Two panels of bars: on the left the number of optimizer steps for five batch sizes at 60 epochs, on a log scale, with mean validation loss beside each; on the right the validation and training loss of four batch sizes given the same 780 steps](../figures/fig-w04-2-batch-size-hold-what-fixed.svg)
*Figure W4.2 — Changing the batch size changes the number of steps, so ask what each experiment held fixed.*

---

## 🔟 Page 4.6 — Hook Table: Read It

This is the table from the hook (five seeds, peak `lr = 0.03`, final accuracy in percent).

```text
constant        46.9  50.6  53.1  98.1  97.2   mean  69.2
warmup only     99.2  67.5  76.4  98.1  86.7   mean  85.6
cosine only     98.9  98.9  98.9  98.9  98.9   mean  98.9
warmup+cosine   99.2  98.9  98.9  98.9  98.9   mean  98.9
```

**H1.** Out of 5 seeds, how many reach more than 90% with `constant`? ______ With `cosine only`? ______

**H2.** What does 46.9% mean? _____________________________________________

**H3.** Which row would you have guessed was best *before* you saw it? ______________ Was that the best? ______

**H4.** The gentle rate (`lr = 0.003`), mean final validation loss over 5 seeds: constant **0.039** (lowest 0.030, highest 0.050); cosine only **0.035** (lowest 0.032, highest 0.040). Is the gap between those two means **bigger or smaller** than the gap between the lowest and highest seed inside the `constant` row? ______

**H5.** In two sentences: what did a schedule do at the too-big rate, and what did it do at the gentle one?

______________________________________________________________

______________________________________________________________

---

## 🐞 Page 4.7 — Fix the Broken Programs

Each is **deliberately broken**. Read the **last line** of the message first.

**D1 — DELIBERATE ERROR**

```python
import torch
import torch.nn as nn
w = nn.Parameter(torch.zeros(1))
opt = torch.optim.SGD([w], lr=0.02)
sched = torch.optim.lr_scheduler.LambdaLR(opt, 0.5)
```

Last line of the message: ______________________________________________

Is `0.5` a number or a function? ______ Fix: ______________________________

**D2 — DELIBERATE ERROR**

```python
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)
print(f"lr {sched.get_last_lr():.4f}")
```

Last line: ______________________________________________

Print `sched.get_last_lr()` by itself first. It shows: ______________ Fix: ______________________________

**D3 — NO ERROR, but wrong.** A student wants the cosine to fall from 0.02 to 0. They write:

```python
import numpy as np
w = nn.Parameter(torch.zeros(1))
opt = torch.optim.SGD([w], lr=0.02)
sched = torch.optim.lr_scheduler.LambdaLR(
    opt, lambda s: 0.02 * 0.5 * (1 + np.cos(np.pi * s / 50)))
print(sched.get_last_lr())
```

It prints `[0.0004]`. What should it print? ______ Why is it 50 times too small? ______________________________________ Fix: ______________________________

**D4 — NO ERROR, but wrong.** The loop is:

```python
for step in range(40):
    opt.step()
print(opt.param_groups[0]["lr"])
```

with the cosine from P4. The rate printed is `0.02` after 40 steps, when it should be near 0.0004. What is missing? ______________________________

**D5 — NO ERROR, but wrong.** The rate at steps 0, 25, 50, 75 prints `0.02, 0.01, 0.0, 0.01`. What went wrong at step 75? ______________________ Write the line that fixes it: ______________________________________________

**D6 — a `lambda` that cannot be a `lambda`.** You want a warmup: `if s < 5: ...`. Can a `lambda` hold an `if`/`for` line? ______ What do you write instead? ______________________________

**D7 — the guard.** `lambda s: s / warm` with `warm = 0` raises `ZeroDivisionError: division by zero` **when the scheduler is built**. Why so early? ______________________________ One-line fix: ______________________________

---

## 📓 Page 4.8 — The Bug Log

Copy the **last line** of every error or surprise you meet this week, not the whole traceback.

| # | Last line (copied) | What it meant | The fix | Caught by (message / print / nobody) |
|:-:|---|---|---|:-:|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Your sentence for this week:** *"A scheduler without a printout is a ______."* Complete it from memory: ______________________________

**Which bug was silent (no error, wrong answer)?** How would you have found it? ______________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. The learning rate at step `s` is `peak × ________(s)`. Cosine goes from ______ to ______.
2. Which runs first in a training step: `opt.step()` or `sched.step()`? ______________ What does `get_last_lr()` show right after `sched.step()`? _________________________
3. Why is `get_last_lr()[0]` written with `[0]`? ______________________________
4. Batch size 64: steps per epoch = ______. Batch 512: ______. Why is "same epochs" not a fair comparison? ______________________________
5. Why is "same steps" not a fair comparison either? ______________________________
6. What would you need to see to claim "bigger batches are worse"? ______________________________

**How sure am I?** (circle one per line)

| I can write a `lambda` | 1 2 3 4 5 |
|---|---|
| I can get a learning rate by hand | 1 2 3 4 5 |
| I can count steps from a batch size | 1 2 3 4 5 |
| I can say what I held fixed | 1 2 3 4 5 |

---

# ✂️ ANSWERS — keep this page folded until you have finished

### Warm-Up

- **W1.** `lr`.
- **W2.** `ln 2`, the loss of guessing between two classes (`-ln(0.5)`).
- **W3.** Overfitting (or "memorising"). Either is fine this week; Week 5 names it.
- **W4.** One seed is one lucky or unlucky starting point. Several seeds show the spread, so you can tell a real gap from noise.
- **W5.** The train set (840 points). Validation (360) is only for scoring.

### Page 4.1

Order: schedule **C**, multiplier **E**, warmup **F**, cosine decay **B**, `lambda` **A**, steps per epoch **G**, confound **D**, scheduler **H**.

A batch: the handful of training examples whose gradients are averaged for one step (a poll of the training set). A confound: two things changed at once, so you cannot say which one caused the result.

### Page 4.2

Real output (run, CPU):

- **P1.** `7` and `15`.
- **P2.** `[0.1]`, `[0.05]`, `[0.025]`. Each step halves the rate, and the list has one entry.
- **P3.** `840 // 150` = **5** steps; used 750; left out **90** (a different 90 each epoch). `840 // 1000` = **0**: not even one full batch fits, so no step is ever taken.
- **P4.** `0.02`. No error. The clock never moved. (`sched.get_last_lr()` would say `[0.02]` too.)
- **P5.** `0.02, 0.01, 0.0, 0.01`. The rate **climbed back up**: the cosine is periodic, so after `T` it rises again.

### Page 4.3

**M1.**

| Where | `s/T` | angle | cosine | multiplier | rate |
|---|:--:|:--:|:--:|:--:|:--:|
| Start | 0 | 0 | 1 | 1 | 0.02 |
| Halfway | 0.5 | pi/2 (1.5708) | 0 | 0.5 | 0.01 |
| End | 1 | pi (3.1416) | -1 | 0 | 0 |

**M2.** (Checked against `LambdaLR` in code.)

| Step | Cos mult | Cos rate | Warm+cos mult | Warm+cos rate |
|:--:|:--:|:--:|:--:|:--:|
| 0 | 1.0000 | 0.02000 | 0.2000 | 0.00400 |
| 2 | 0.9961 | 0.01992 | 0.6000 | 0.01200 |
| 4 | 0.9843 | 0.01969 | 1.0000 | 0.02000 |
| 5 | 0.9755 | 0.01951 | 1.0000 | 0.02000 |
| 10 | 0.9045 | 0.01809 | 0.9698 | 0.01940 |
| 20 | 0.6545 | 0.01309 | 0.7500 | 0.01500 |
| 25 | 0.5000 | 0.01000 | 0.5868 | 0.01174 |
| 40 | 0.0955 | 0.00191 | 0.1170 | 0.00234 |
| 50 | 0.0000 | 0.00000 | 0.0000 | 0.00000 |

Marking: allow the 3rd decimal on the multiplier and the 5th decimal place on the rate. A student who gets `0.0000` at step 0 of the ramp forgot the `+ 1`.

**M3.** progress = (20 - 5) / (50 - 5) = 15/45 = **0.3333**; angle = pi × 0.3333 = **1.0472**; cosine = **0.5**; multiplier = 0.5 × (1 + 0.5) = **0.75**; rate = 0.02 × 0.75 = **0.015**.

**M4.** `0 / 5 = 0`, so a rate of **0**. A zero rate does nothing, so the first step is wasted.

**M5.** Any honest two. Good ones: "the two curves are almost the same after the ramp"; "warm+cos is lower in the middle, because its cosine started 5 steps later and so falls over a shorter distance (45 steps), ending in the same place"; "both hit 0 at step 50"; "the warm+cos is a straight line up for 5 steps". (Check: at step 25 warm+cos is 0.01174, higher than cos at 0.01000.)

**M6.** Around step **25** (the middle, between about steps 20 and 30). A straight line is at **0.016** at step 10; the cosine is at **0.01809**. The cosine starts **slower** than a straight line.

**M7.** The script prints `0.004, 0.008, 0.012, 0.016` for steps 0 to 3 (real run: `[(0, 0.004), (1, 0.008), (2, 0.012), (3, 0.016)]`). The first value printed is **right after construction**, before any `sched.step()`, so it is step 0's rate, 0.004, which agrees with the table. If a student prints *after* `sched.step()`, they see the **next** step's rate (after the first `opt.step(); sched.step()` the value is 0.008). Both are right; `get_last_lr()` shows the rate the **next** step will use. Real run, after four `opt.step(); sched.step()` pairs: `[0.02]`.

### Page 4.4

| Batch | Steps/epoch | Used | Left out | Steps in 30 epochs |
|:--:|:--:|:--:|:--:|:--:|
| 24 | 35 | 840 | 0 | 1050 |
| 70 | 12 | 840 | 0 | 360 |
| 150 | 5 | 750 | 90 | 150 |
| 400 | 2 | 800 | 40 | 60 |
| 420 | 2 | 840 | 0 | 60 |
| 1000 | 0 | 0 | 840 | 0 |

(Real output of `840 // bs` in Python.)

- **C1.** 24, 70, 420: they are **divisors of 840**, so a whole number of batches fits.
- **C2.** `840 // 64` = 13 steps per epoch. 1,000 ÷ 13 = 76.9, so **77** epochs. 77 × 13 = **1,001** steps. (76 epochs gives 988, which is not enough.)
- **C3.** Batch 8: 105 steps per epoch, 6,300 in 60 epochs. Batch 512: 1 step per epoch, 60 in 60 epochs. 6,300 ÷ 60 = **105**. (Not 64.)
- **C4.** `840 // 120` = 7 steps per epoch. 360 ÷ 7 = 51.4; **51** epochs gives **357** steps (52 gives 364). Either is fine if the steps are checked.
- **C5.** Batch 420 at 60 epochs is "same epochs" (120 steps, against 2,100 for batch 24). Batch 420 at 180 epochs is "same steps": 360 steps, against 350 for batch 24 at 10 epochs. The point: **same epochs is not same steps**.

### Page 4.5

Reference run (seeds 0 to 2, mean validation loss; run on CPU with one thread):

```text
workbook grid: validation loss, mean of seeds 0-2
bs  24  60 epochs = 2100 steps: 0.052    10 epochs = 350 steps: 0.056
bs 120  60 epochs =  420 steps: 0.053    51 epochs = 357 steps: 0.039
bs 420  60 epochs =  120 steps: 0.036   180 epochs = 360 steps: 0.068
```

- **Predictions:** any honest guess is full marks if written before the run. Do not mark a student wrong for a third-decimal difference.
- **R1.** Column 1 held **epochs** fixed; it also changed **steps** (2,100 against 120). Column 2 held **steps** fixed (about 360); it also changed **epochs, the number of times the same 840 points are revisited** (10 against 180).
- **R2 model:** *"On 840 training points, with 3 seeds, I held steps fixed at about 360. The result was val 0.056, 0.039 and 0.068 for batches 24, 120 and 420. That could also be because batch 420 ran 180 epochs, so it saw the same points 180 times, while batch 24 ran only 10."*
- **R3.** Can: "at the same number of steps, batch 420 (0.068) was worse than batch 120 (0.039) on these 3 seeds." Cannot: that bigger batches are worse in general. Also, in column 1 batch 420 (0.036) is the **best** row, with only 120 steps. **The two columns point in opposite directions**, which is the whole lesson: neither experiment is neutral.
- **R4.** Column 2 supports it, but "less noisy" is not what the table tests: epochs changed from 10 to 180. You would need the same steps **and** the same epochs (hard to do together), several more seeds, and still worse.
- **R5.** Different seeds give the same ordering if the gap is large and different digits always. If the ordering flips, the gap was inside the noise.

A worked example from the class table, for comparison (do not copy it): five-seed means at 60 epochs are 0.046, 0.039, 0.039, 0.039, 0.053 for batches 8, 32, 64, 128, 512; at 780 steps, batches 128 and 256 give 0.073 against 0.034 and 0.039 for batches 32 and 64.

### Page 4.6

- **H1.** Two (98.1, 97.2); five.
- **H2.** The "always answer the same class" score, since 46.9% of the validation set is one class and 53.1% the other. Nothing learned. (The Week 1 `ln 2` coin in another costume.)
- **H3.** Honest answers vary. The best (tied) rows are `cosine only` and `warmup+cosine`, both 98.9; `warmup only` was **not** the safe one.
- **H4.** **Smaller.** The gap between the means is 0.004 (0.039 against 0.035); inside the `constant` row the seeds span 0.020 (0.030 to 0.050).
- **H5.** At the too-big rate the falling rate rescued every seed, while warmup alone did not. At the gentle rate none of the schedules differed more than the seeds did. So a schedule can rescue a bad rate; it does not make a good rate better, on this problem.

### Page 4.7

- **D1.** `TypeError: 'float' object is not callable`. A number. Fix: `lambda s: 0.5`.
- **D2.** `TypeError: unsupported format string passed to list.__format__`. It shows `[0.02]` (a list of one number). Fix: `sched.get_last_lr()[0]`.
- **D3.** `[0.02]`. The lambda returned a **rate** (`0.02 * ...`), and `LambdaLR` multiplied by the starting `lr=0.02` again: 0.02 × 0.02 = 0.0004. `LambdaLR` wants a **multiplier**. Fix: drop the `0.02 *`.
- **D4.** `sched.step()` after `opt.step()`. (The scheduler is attached but its clock never moves.) Print the rate once.
- **D5.** The loop ran past `T = 50` and the cosine is periodic. Fix: clamp the progress, `min(1.0, s / T)`, inside the cosine.
- **D6.** No. A `lambda` holds one expression. Write a `def` with the `if`.
- **D7.** `LambdaLR` calls your function once at construction (for step 0). Fix: `(s + 1) / max(1, warm)` or `if warm > 0 and s < warm`.

### Page 4.8 and Self-Check

Bug Log: any real entries are fine if the **last line** (not the whole traceback) was copied and the fix works. The silent bugs (D3, D4, D5) show nothing on their own; a printout of the rate at step 0, the middle and the end catches all three (too small, constant, back up).

1. `multiplier`; from 1 to 0.
2. `opt.step()` first, then `sched.step()`. The rate the **next** step will use.
3. It returns a **list**, one entry per parameter group; we have one group.
4. 13; 1. Same epochs gives big batches far fewer steps (780 steps at batch 64 against 60 at batch 512, 13 times as many).
5. At equal steps, big batches run many more epochs and so revisit the same 840 points, which can memorise them (train loss near 0.000).
6. The same steps, the same epochs, more than one seed, and still worse.

---

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [📖 Chapter](../student-guide/week-04.md) · [Next ➡ Week 5](week-05.md)
