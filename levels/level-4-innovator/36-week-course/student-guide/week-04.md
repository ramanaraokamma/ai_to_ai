# Week 4 — Schedules and Batch Size

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [Next ➡ Week 5](week-05.md) · [Workbook](../workbook/week-04.md)

---

> ### This week in one sentence
> **The right step size changes during a run, and the batch size quietly changes how many steps you get, so every comparison needs the sentence "what did I hold fixed?"**
>
> **By the end of this chapter you will be able to:**
> - **Compute a learning rate for any step by hand** from `peak × multiplier(step)`
> - **Write a `lambda`** and hand it to `LambdaLR`, then read the rate back with `get_last_lr()`
> - **Say in which order** `opt.step()` and `sched.step()` go, and what `get_last_lr()` reports right after
> - **Work out how many optimizer steps a run takes** from the batch size, using `840 // batch`
> - **Report a result with its sample size** ("mean of five seeds") and name the quantity you held fixed
>
> **New maths:** **none.** You use a straight-line ramp, a few cosine values from a calculator, and whole-number division with a remainder.
>
> **New syntax:** `lambda step: ...` · `torch.optim.lr_scheduler.LambdaLR` · `scheduler.step()` · `scheduler.get_last_lr()`
>
> **Reading time:** about 35 minutes. **Homework:** about 60–75 minutes.

> **📌 About the code blocks.** Each block carries on from the one above it within the same file, so each `import` is typed once, in the first block that needs it. If you paste a block on its own and get `NameError`, that is why; nothing is broken. The blocks marked **DELIBERATE ERROR** are broken on purpose. Every output shown was printed by a real run on a CPU with a seed set. Your numbers should match to every digit shown, except that the file paths inside an error message will be your own. Every training run this week is a **real** network trained for real; the schedule traces use a dummy one-number "model" that only watches the clock, and the text says so where it happens. Nothing this week needs the internet.
>
> **Before you start:** `l4lib` must be importable. From inside the `36-week-course` folder, once per terminal: `export PYTHONPATH="$PWD"`. If you see `ModuleNotFoundError: No module named 'l4lib'`, that is the fix.

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 4 is highlighted with a pointer above it, weeks 1 to 3 are outlined solid, and every later tile has a dashed outline](../figures/fig-w04-0-where-this-fits.svg)
*Figure 4.0 — Where this fits: week 4 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## 🪝 Start Here

In Week 1 you found that a learning rate of 0.03 was too big for the spirals. Here is the same network, the same data and the same optimizer (AdamW), run five times with five different seeds at that too-big rate. The only thing that differs between rows is **how the learning rate changes during the run**. The numbers are final accuracy on the 360 validation points, in percent.

```text
AdamW, lr=0.03 (ten times the Week 1 default), final validation accuracy %, seeds 0-4
constant        46.9  50.6  53.1  98.1  97.2   mean  69.2
warmup only     99.2  67.5  76.4  98.1  86.7   mean  85.6
cosine only     98.9  98.9  98.9  98.9  98.9   mean  98.9
warmup+cosine   99.2  98.9  98.9  98.9  98.9   mean  98.9
```

Before you read any further, write in your Bug Log:

1. In the `constant` row, what do `46.9`, `50.6` and `53.1` have in common? (Hint: the validation set is 46.9% one class and 53.1% the other. What does a model that ignores the data score? These runs ended there, but see Question 2 before you decide they never learned anything.)
2. How many of the five seeds are still above 90% at the END of the run with a constant rate? How many with `cosine only`? (Run `hook.py` below and print the best accuracy any epoch reached, `max(h["acc"])`. Does "ended at 46.9%" mean "never learned"?)
3. Which row would you have picked as "the best" before seeing the numbers? Does the table agree with you?
4. Is this a result about every network and every problem? What is it a result about?

You will write the code that produced the last two rows today. First you need to know what a "falling rate" is as a rule you can compute. Then comes a second knob, the **batch size**, where the trap is less obvious.

---

## 🧠 The Big Idea

### 1. The rate is a rule over time

Until now the learning rate was one number that never moved. Today it is two things multiplied together:

```text
lr(step) = peak × multiplier(step)
```

- The **peak** is the biggest rate you ever use (for example 0.003).
- The **multiplier** is a number between 0 and 1 that depends on which step you are on.
- A **learning-rate schedule** is the rule that gives the multiplier.

Try it on paper. If the peak is 0.003 and the multiplier is 0.5, the rate is 0.0015. Now do peak 0.01 with multiplier 0.1, and peak 0.003 with multiplier 0.

### 2. Warmup is a straight ramp

**Warmup** means starting with a small rate and climbing to the peak over the first few steps. Say you want ten warmup steps. The multiplier at step 0 is 0.1, at step 1 it is 0.2, and it reaches 1 at step 9.

Write the rule that gives the multiplier from the step number `s` and the warmup length `W`. Try it before reading on. (The next paragraph tells you what the course uses, so cover it up for a minute.)

The course uses `(s + 1) / W`. Why `s + 1` and not `s`? Work out what the rate would be at step 0 with plain `s / W`, and what a step at that rate would do.

Fill in this table for peak 0.01 and `W = 10`:

```text
step  multiplier   rate (peak 0.01)
  0
  4
  9
```

After step `W` the ramp is over.

### 3. Cosine decay, as three checkpoints

After warmup we want the rate to come down: slowly at first, fastest in the middle, slowly again at the end. There is a curve from maths class that does exactly that. You do not need to know where it comes from. You need one sentence: **the cosine of an angle starts at 1, drifts down through 0, and ends at −1, smoothly, as the angle goes from 0 to half a turn.**

The decay multiplier is

```text
multiplier(s) = 0.5 * (1 + cos( pi * s / T ))
```

where `T` is the total number of steps. Read it as three checkpoints:

| Where in the run | `s / T` | angle `pi * s / T` | cosine of it | multiplier `0.5 * (1 + cos)` |
|---|:--:|---|:--:|:--:|
| Start | 0 | 0 | 1 | `0.5 * 2 = 1` (the full rate) |
| Halfway | 0.5 | a quarter turn | 0 | `0.5 * 1 = 0.5` |
| End | 1 | half a turn | −1 | `0.5 * 0 = 0` |

Now use a calculator (your phone is fine; set it to **radians**) with `T = 100` and fill in the two missing rows:

```text
step   straight line down   cosine
  0         1.00            1.0000
 25         0.75            ______
 50         0.50            0.5000
 75         0.25            ______
100         0.00            0.0000
```

Where does the cosine lose the most between two neighbouring rows? Why might you want the rate to fall slowly at the start of a run?

By the end the rate is nearly zero. That is on purpose. By then the model has mostly settled, and a tiny step polishes instead of bouncing.

![Line chart of learning rate against step: a dashed cosine-only curve falling from 0.003 to zero, a solid warm-up-then-cosine curve that climbs over 50 steps first, and a table of printed rates beside it](../figures/fig-w04-1-warmup-then-cosine-rate.svg)
*Figure 4.1 — The rate is the peak times a multiplier: warm-up ramps it up over 50 steps and cosine brings it down to zero.*

### 4. The batch

A **batch** is the handful of training examples whose gradients are averaged to make one step. You have used `batch_size=64` since Week 1 without being told it was a choice.

Why average at all? One example's gradient is a rough guess at "which way is downhill for everybody". An average of 64 is a better guess than an average of 8. **A batch is a poll of the training set.** You can feel this with a coin: flip it 8 times and write down the fraction of heads, then flip it 64 times and do the same. Which answer sits closer to 0.5?

Here is a measurement from the untrained network, taken over 200 random batches at each size: how far a single batch's gradient lands from the gradient of all 840 training points.

| Batch size | Average distance from the full-data gradient |
|:--:|:--:|
| 8 | 0.196 |
| 32 | 0.104 |
| 128 | 0.050 |
| 512 | 0.018 |

(The code that produced this uses a tool you have not met yet, so you only get the table. The reason it has this shape comes in Week 15.) Each time the batch gets four times bigger, the distance about halves, until 512, which is already most of the 840 points.

Now the trap, and it is arithmetic. Your training set has 840 points. The harness drops the last short batch and reshuffles every epoch. So:

```text
steps per epoch = 840 // batch
steps in a run  = steps per epoch × epochs
```

**`//` is whole-number division.** Two slashes means "how many whole ones fit". `840 // 64` is `13`, because 13 batches of 64 use 832 points and 8 are left over. The 8 left-overs are thrown away (and are different points each epoch).

So batch 64 gives 13 steps per epoch and batch 512 gives **one**. Hold that thought until the experiments.

### 5. The four new lines of syntax

**`lambda`.** A function with no name, written on one line. This:

```python
def mult(s):
    return 0.5 * (1 + np.cos(np.pi * s / T))
```

and this:

```python
mult = lambda s: 0.5 * (1 + np.cos(np.pi * s / T))
```

mean the same thing. Read `lambda s:` as "the function that takes `s` and gives back...". The part before the colon goes in; the part after comes out. A `lambda` can hold **one expression only**, with no `if` and no `for`. (That is why warmup, which needs an `if`, is written with `def` below.) Why bother? Because the tool below wants a function as an argument, and for a one-liner that is the shortest way to hand one over.

Check yourself: what does `lambda x: x + 1` give back for 4? What does `lambda x: 2 * x` give back for 4?

**`torch.optim.lr_scheduler.LambdaLR(opt, mult)`.** Attaches to an optimizer. It remembers the starting `lr`. Every time you call `.step()` on it, it sets `lr = starting_lr × mult(steps so far)`. It wants `mult` to return a **multiplier**, and it wants `mult` to be a **function**.

**`scheduler.step()`.** Advances the clock by one. It does **not** touch any weights; that is `opt.step()`'s job. The pair, in order, every training step:

```python
opt.step()      # move the weights, using the lr as it is right now
sched.step()    # then move the clock, so the next step gets the next lr
```

**`scheduler.get_last_lr()`.** Reads the current learning rate back **as a list**, one entry per group of parameters. You have one group, so you get something like `[0.003]`, and `sched.get_last_lr()[0]` is the number. Read the next sentence twice: **right after `sched.step()` it shows the rate the next step will use**, not the one the step you just finished used.

---

## 💻 Try It Yourself — the schedules

### Step 1 — the two multipliers and a table

Make a file `schedules.py`. Type this first part and run it. Then compare it with your hand table from the Big Idea.

```python
import numpy as np
import torch
import torch.nn as nn

PEAK = 0.003
T = 1000
WARM = 50

def cosine_mult(s):
    return 0.5 * (1 + np.cos(np.pi * s / T))

def warm_cosine_mult(s):
    if s < WARM:
        return (s + 1) / WARM
    prog = (s - WARM) / (T - WARM)
    return 0.5 * (1 + np.cos(np.pi * min(1.0, prog)))

print("step   cosine    warm+cosine")
for s in [0, 10, 49, 50, 250, 500, 750, 1000]:
    print(f"{s:>4}   {PEAK * cosine_mult(s):.5f}   {PEAK * warm_cosine_mult(s):.5f}")

```

Output:

```text
step   cosine    warm+cosine
   0   0.00300   0.00006
  10   0.00300   0.00066
  49   0.00298   0.00300
  50   0.00298   0.00300
 250   0.00256   0.00268
 500   0.00150   0.00162
 750   0.00044   0.00048
1000   0.00000   0.00000
```

Look at the row for step 500 in the `cosine` column, and the row for step 0 in `warm+cosine`. Which checkpoints from section 3 and which ramp rung from section 2 are they? Then find the row where the two columns differ most. Why does `warm+cosine` read `0.00268` at step 250 while `cosine` reads `0.00256`?

### Step 2 — a picture made of `#`, and the `LambdaLR` check

Add this to the same file and run it again:

```python
print()
for s in range(0, 1001, 100):
    bar = "#" * int(40 * warm_cosine_mult(s))
    print(f"{s:>4} {bar}")


def trace(mult):
    w = nn.Parameter(torch.zeros(1))
    opt = torch.optim.SGD([w], lr=PEAK)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, mult)
    seen = []
    for s in range(T + 1):
        seen.append(sched.get_last_lr()[0])
        opt.step()
        sched.step()
    return np.array(seen)

print()
for name, mult in [("cosine", cosine_mult), ("warm+cosine", warm_cosine_mult)]:
    by_hand = np.array([PEAK * mult(s) for s in range(T + 1)])
    print(f"{name:<12} biggest gap vs LambdaLR: {np.abs(trace(mult) - by_hand).max():.1e}")
```

The new output is the staircase of `#` and the two gap lines:

```text
   0 
 100 #######################################
 200 #####################################
 300 #################################
 400 ############################
 500 #####################
 600 ###############
 700 #########
 800 ####
 900 #
1000 

cosine       biggest gap vs LambdaLR: 0.0e+00
warm+cosine  biggest gap vs LambdaLR: 0.0e+00
```

`trace` does not train anything. It makes one dummy number, hands it to an optimizer only so the scheduler has something to watch, and runs the clock 1,000 times writing down the rate it reads. **The gap is zero because `LambdaLR` does the same multiplication you did.** The thing being checked is that the clock lines up: step 0 gets the multiplier of step 0.

### Step 3 — the scheduler inside a real training loop

Now a real network. Make `minitrain.py`. The loop is yours from Level 3, so the new lines are the `LambdaLR` line, `opt.step()` followed by `sched.step()`, and the print. One line in it, the one that picks 64 random rows, uses a tool (`torch.randperm`) you meet properly in Week 5; just copy it.

```python
import torch
import torch.nn as nn
import numpy as np
from l4lib.spirals import get_data, make_model

torch.set_num_threads(1)
Xtr, ytr, Xva, yva = get_data()
torch.manual_seed(0)
model = make_model()
opt = torch.optim.AdamW(model.parameters(), lr=0.003)
lossf = nn.CrossEntropyLoss()

TOTAL, WARM = 120, 12
def mult(s):
    if s < WARM:
        return (s + 1) / WARM
    prog = (s - WARM) / (TOTAL - WARM)
    return 0.5 * (1 + np.cos(np.pi * min(1.0, prog)))

sched = torch.optim.lr_scheduler.LambdaLR(opt, mult)
g = torch.Generator().manual_seed(0)
for step in range(TOTAL):
    idx = torch.randperm(len(Xtr), generator=g)[:64]
    loss = lossf(model(Xtr[idx]), ytr[idx])
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    sched.step()
    if step % 20 == 0 or step == TOTAL - 1:
        print(f"step {step:>3}  lr {sched.get_last_lr()[0]:.6f}  loss {loss.item():.3f}")
```

Output:

```text
step   0  lr 0.000500  loss 0.692
step  20  lr 0.002949  loss 0.598
step  40  lr 0.002497  loss 0.381
step  60  lr 0.001717  loss 0.092
step  80  lr 0.000866  loss 0.065
step 100  lr 0.000223  loss 0.066
step 119  lr 0.000000  loss 0.095
```

Three questions for your Bug Log:

1. The first line says `lr 0.000500`. The ramp rule says step 0 used `0.003 × 1/12 = 0.00025`. Who is right? (Use the sentence about `get_last_lr()` from section 5.)
2. Find the line where the loss stops improving much. What was the rate then?
3. Why is the first loss 0.692? Think back to Week 1.

### Step 4 — two more deliberate errors

Type each of these on its own and read the message from the **last line** upwards.

```python
# DELIBERATE ERROR 1: a number, not a function
import torch
import torch.nn as nn
w = nn.Parameter(torch.zeros(1))
opt = torch.optim.SGD([w], lr=0.003)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda=0.5)
```

```text
Traceback (most recent call last):
  File "week4_mistakes.py", line 6, in <module>
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda=0.5)
  ...
  File ".../torch/optim/lr_scheduler.py", line 274, in <listcomp>
    return [base_lr * lmbda(self.last_epoch)
TypeError: 'float' object is not callable
```

(Several frames inside torch are left out, and their line numbers and paths depend on your torch version.) What does "not callable" say about what you handed over? Why does it crash on this line, before any training step? Then write the one-line fix.

```python
# DELIBERATE ERROR 2: get_last_lr() is a list
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)
print(sched.get_last_lr())
print(f"lr {sched.get_last_lr():.4f}")
```

```text
[0.003]
Traceback (most recent call last):
  File "week4_mistakes.py", line 3, in <module>
    print(f"lr {sched.get_last_lr():.4f}")
TypeError: unsupported format string passed to list.__format__
```

Look at the first printed line, then fix the second.

---

## 🎲 Your Turn — steps per epoch, and two experiments

### Part 1 — count the steps (paper and calculator only)

Fill in the two right-hand columns:

```text
batch   steps per epoch (840 // batch)   steps in 60 epochs
  8
 64
 128
 512
```

If batch 8 and batch 512 are each trained for 60 epochs, how many times as many times does batch 8 move the weights? Both have seen every point 60 times. Is that a fair comparison? In what sense, and in what sense not?

### Part 2 — predict, then run

Write down your prediction: at 60 epochs, is batch 512 better than, worse than, or the same as batch 64 on validation loss?

Then make `batches.py`. It takes about 30 seconds, so start it and move on to the workbook while it runs.

```python
import torch
torch.set_num_threads(1)
import numpy as np
from l4lib.spirals import run

N_TRAIN = 840
print("batch  steps/epoch  steps in 60 epochs")
for bs in [8, 32, 64, 128, 256, 512]:
    per = N_TRAIN // bs
    print(f"{bs:>5}  {per:>11}  {per * 60:>18}")

print()
print("A) same 60 epochs: validation loss, seeds 0-4")
for bs in [8, 32, 64, 128, 512]:
    v = [run("x", batch_size=bs, seed=s, verbose=False)["val"][-1] for s in range(5)]
    print(f"bs {bs:>3} steps {N_TRAIN // bs * 60:>5}  " + " ".join(f"{x:.3f}" for x in v) + f"   mean {np.mean(v):.3f}")

print()
print("B) same 780 steps: validation loss, seeds 0-4")
for bs in [32, 64, 128, 256]:
    ep = 780 // (N_TRAIN // bs)
    hs = [run("x", batch_size=bs, epochs=ep, seed=s, verbose=False) for s in range(5)]
    v = [h["val"][-1] for h in hs]
    tr = np.mean([h["train"][-1] for h in hs])
    print(f"bs {bs:>3} epochs {ep:>3}  " + " ".join(f"{x:.3f}" for x in v) + f"   mean val {np.mean(v):.3f}  mean train {tr:.3f}")
```

The first table is the step count you just did by hand:

```text
batch  steps/epoch  steps in 60 epochs
    8          105                6300
   32           26                1560
   64           13                 780
  128            6                 360
  256            3                 180
  512            1                  60
```

**Experiment A** keeps the epochs the same:

```text
A) same 60 epochs: validation loss, seeds 0-4
bs   8 steps  6300  0.027 0.024 0.066 0.070 0.040   mean 0.046
bs  32 steps  1560  0.043 0.034 0.038 0.027 0.050   mean 0.039
bs  64 steps   780  0.037 0.050 0.030 0.042 0.039   mean 0.039
bs 128 steps   360  0.049 0.034 0.035 0.029 0.052   mean 0.039
bs 512 steps    60  0.079 0.050 0.051 0.025 0.061   mean 0.053
```

**Experiment B** picks the epochs so every batch gets the same 780 steps:

```text
B) same 780 steps: validation loss, seeds 0-4
bs  32 epochs  30  0.045 0.031 0.037 0.030 0.028   mean val 0.034  mean train 0.029
bs  64 epochs  60  0.037 0.050 0.030 0.042 0.039   mean val 0.039  mean train 0.006
bs 128 epochs 130  0.048 0.055 0.060 0.056 0.148   mean val 0.073  mean train 0.005
bs 256 epochs 260  0.075 0.072 0.067 0.073 0.076   mean val 0.073  mean train 0.000
```

Each number is validation loss (lower is better) for one seed, seeds 0 to 4 left to right. "mean" is the mean of those five seeds.

Read them like this:

1. In A, which row has the worst mean? Look at its `steps` column before you write a story about why.
2. In A, look at the five seeds in the `bs 512` row. What is the best single number in the whole experiment, and which row has it? What does that say about reading one seed?
3. In B, which batches are worse? Look at the `mean train` column for `bs 256`. What is it, and what does it tell you about what that model did with 840 points?
4. In B, batch 256 ran for 260 epochs and batch 32 for 30. What did B change that A did not?
5. In B, one seed of `bs 128` is 0.148 and the other four are 0.048 to 0.060. How does one seed like that change a mean of five?

![Two panels of bars: on the left the number of optimizer steps for five batch sizes at 60 epochs, on a log scale, with mean validation loss beside each; on the right the validation and training loss of four batch sizes given the same 780 steps](../figures/fig-w04-2-batch-size-hold-what-fixed.svg)
*Figure 4.2 — Changing the batch size changes the number of steps, so ask what each experiment held fixed.*

### Part 3 — "what did I hold fixed?"

Copy this into your Bug Log and fill it in:

```text
Experiment A held ______ fixed.  It also changed ______.
Experiment B held ______ fixed.  It also changed ______.
```

Then write **one honest conclusion sentence** about batch size on this problem. A sentence that says only "bigger batch is worse" is not finished: it needs the word "because" and one of the two things that changed along with the batch.

A **confound** is two things that changed at once, so you cannot say which one caused the result. Level 3 taught you to change one thing at a time; here you cannot, because turning the batch knob drags another one with it.

### Part 4 — the gentle rate

First make the file that produced the table in Start Here. Save this as `hook.py` and run it (under 15 seconds). It must print those same four rows; if a number differs, stop and find out why before you go on:

```python
import torch
torch.set_num_threads(1)
import numpy as np
from l4lib.spirals import run

variants = [
    ("constant",      dict()),
    ("warmup only",   dict(warmup_frac=0.05)),
    ("cosine only",   dict(schedule="cosine")),
    ("warmup+cosine", dict(schedule="cosine", warmup_frac=0.05)),
]
print("AdamW, lr=0.03 (ten times the Week 1 default), final validation accuracy %, seeds 0-4")
for name, kw in variants:
    accs = []
    for seed in range(5):
        h = run("x", lr=0.03, seed=seed, verbose=False, **kw)
        accs.append(h["acc"][-1] * 100)
    row = " ".join(f"{a:5.1f}" for a in accs)
    print(f"{name:<14} {row}   mean {np.mean(accs):5.1f}")
```

Now add this to the end of `hook.py` and run it:

```python
print()
print("Same four schedules at the Week 1 default lr=0.003: mean final validation loss, seeds 0-4")
for name, kw in variants:
    vals = [run("x", lr=0.003, seed=seed, verbose=False, **kw)["val"][-1] for seed in range(5)]
    print(f"{name:<14} {np.mean(vals):.3f}  (lowest {min(vals):.3f}, highest {max(vals):.3f})")
```

```text
Same four schedules at the Week 1 default lr=0.003: mean final validation loss, seeds 0-4
constant       0.039  (lowest 0.030, highest 0.050)
warmup only    0.043  (lowest 0.031, highest 0.057)
cosine only    0.035  (lowest 0.032, highest 0.040)
warmup+cosine  0.037  (lowest 0.029, highest 0.045)
```

Compare the gaps between rows with the gap between "lowest" and "highest" inside a row. Then put this beside the Start Here table and say, in two sentences, what a schedule did at the too-big rate and what it did at the gentle one.

---

## 🔑 Wrap Up

Answer these before you close the laptop:

1. What is the learning rate at step `s`, in terms of the peak and a multiplier? What does `LambdaLR` do with your function?
2. In what order do `opt.step()` and `sched.step()` go, and what does `get_last_lr()` show right after `sched.step()`?
3. How many steps does a 60-epoch run take with batch 128?
4. What would you need to see before you claimed "bigger batches are worse"? (Count the things you have varied so far and the things you have not.)
5. What do you want to know about this next? Put it in your Parking Lot.

Then write this sentence in your Bug Log, in your own handwriting:

> **"A toy result shows a mechanism, not a rate. Always say which quantity I held fixed, and how many seeds."**

Two claims you will read elsewhere are **not** shown by anything you measured this week: that warmup prevents training from blowing up, and that small batches always generalise better. Warmup's real home is the transformer in Weeks 14–19. Write both in the "later" column of your Bug Log.

---

## 📝 Vocabulary

| Word | Meaning |
|---|---|
| **learning-rate schedule** | A rule that says how the learning rate changes over a run. |
| **multiplier** | A number between 0 and 1 that the peak rate is multiplied by at each step. |
| **warmup** | A short ramp at the start where the rate climbs from small to the peak. |
| **cosine decay** | A smooth fall of the rate to zero: slow, then fast, then slow. |
| **scheduler** | An object attached to an optimizer that sets the rate for each step from your rule. |
| **`lambda`** | A function with no name, written on one line. |
| **batch** | The handful of training examples averaged to make one step. |
| **steps per epoch** | `840 // batch` on this dataset. |
| **confound** | Two things that changed at once, so you cannot say which one caused the result. |

---

## 🏠 Homework

Workbook Week 4, pages 4.1 to 4.5 (about 60 to 75 minutes). Everything you write down must come from **your own run, printed on your own screen, with a seed set, in the last 24 hours**, not from this chapter.

1. **Plot the two schedules.** Write `plot_schedules.py` using numpy and matplotlib: cosine and warmup-plus-cosine, `PEAK = 0.003`, `T = 1000`, `WARM = 50`, on one picture, saved as `w4_schedules.png`. Print the peak of the warmup-plus-cosine curve and the step where it occurs.
2. **Check it against the scheduler.** Copy `trace()` from `schedules.py` and compare your curve with `LambdaLR`'s. You are done when the printed gap is `0.0e+00`.
3. **The batch-size grid.** For batch sizes `[16, 64, 256]` and seeds 0, 1 and 2, run the harness twice per batch size: once at 60 epochs, and once with the epochs chosen so every batch gets about 780 steps. Print the mean validation loss for each. Use `780 // (840 // bs)` for the epochs.
4. **Three sentences.** Using your grid: (1) what you held fixed in each column, (2) what each column also changed, (3) one thing you can honestly conclude and one thing you cannot.

**The one line to write in your Bug Log tonight:** *"Same epochs is not same steps, and same steps is not same repeats."*

---

## 🔮 Next Week

Look at the `mean train` column of Experiment B again: a training loss of `0.000` sitting beside a validation loss several times larger. Week 5 gives that a name and tests four cures on a much smaller set of points. It adds four new pieces of syntax, one of which is the `randperm` you copied today.

**Before then:** keep `schedules.py`, `minitrain.py`, `hook.py` and `batches.py` exactly as they are. Bring one sentence: *what is the difference between a model that has learned and a model that has memorised, and how would I tell from two numbers?*

---

[⬅ Week 3](week-03.md) · [Course Home](../README.md) · [Next ➡ Week 5](week-05.md) · [Workbook](../workbook/week-04.md)
