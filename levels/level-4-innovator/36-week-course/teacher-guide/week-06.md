# Week 6 — Norms, Residuals, and the Gradient Highway

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Week 7 ➡](week-07.md) · [Student Guide](../student-guide/week-06.md) · [Workbook](../workbook/week-06.md)

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 6 is highlighted with a pointer above it, weeks 1 to 5 are outlined solid, and every later tile has a dashed outline](../figures/fig-w06-0-where-this-fits.svg)
*Figure 6.0 — Where this fits: week 6 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## 📋 At a Glance

This table is the week on one screen: timing, the big idea, the new vocabulary and syntax, and what to have ready.

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the first week where the question changes from *"how do I train better?"* to *"how do I make a deep network trainable at all?"* |
| **Big idea** | A deep stack of plain layers can sit at the coin-flip loss for ever, because the gradient that should reach its first layer has shrunk to nothing on the way back. Two cheap devices fix that. A **norm** layer re-centres and re-scales the numbers so no layer sees a strange range; a **residual** connection, `x + f(x)`, gives the gradient a road of slope exactly 1 to walk back down. And the two norms are not interchangeable: **batch norm leans on the other examples in the batch** and fails at batch size 2; **layer norm looks only at one example** and does not. |
| **New vocabulary** | normalise · batch norm · layer norm · running statistics · train mode vs eval mode (again) · residual / skip connection · gradient highway · vanishing gradient · gradient length · gradient clipping |
| **New maths** | **Slope of a sum** — nudge `x` in `x + f(x)` and watch the answer move by *1 plus whatever `f` does*. Met numerically, with a tiny step, **before** the words `1 + f'(x)` are ever written. See 🔢 below. |
| **New syntax** | `nn.LayerNorm(d)` · `nn.BatchNorm1d(d)` · `nn.Identity()` · `torch.nn.utils.clip_grad_norm_` — four, the ladder maximum |
| **Dataset** | The Week 1 spirals, unchanged: `get_data()` gives 840 training and 360 validation points (2 features, 2 classes). Nothing is downloaded. |
| **Materials** | Paper · a calculator · printed workbook pages 6.1–6.5 · the Bug Log · three coloured pens (for the three columns of the depth table) |
| **Tech needed** | Laptop with Python 3, numpy, torch, matplotlib (homework only). `l4lib/` importable (Prep step 1). **No new install. No network.** |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime** | `small_batch.py` about 8 seconds · `depth_train.py` about 25 seconds · `clip_demo.py` about 9 seconds · everything else under 2 seconds each |

> **⚠️ Watch out:** this week has **three results that contradict the reference module or the folk story**, all measured here and all in the Answer Key. (1) A *plain* 12-block network trains fine; the collapse starts between 8 and 16 blocks. (2) A residual stack with **no norm** does not keep the gradient "near 1"; at 32 blocks it *grows* to 20–300. (3) **Layer norm alone** keeps the gradient healthy at 16 and 32 blocks and the network still never learns (46.9%). Do not tell the student the textbook version. Tell them what the table says.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compute layer norm by hand** on one row of four numbers (subtract the row's mean, divide by the row's spread) and say which direction batch norm averages in instead (down a column, across examples).
2. **Say why batch norm fails at batch size 2** — the answer for one example depends on who else is in the batch, and with two examples every feature collapses to `-1` and `+1` — and why layer norm does not.
3. **Use the slope of a sum** — given that `f` has slope `0.3` at some point, say that `x + f(x)` has slope `1.3` there — and *see it first* by nudging `x` by `0.001`.
4. **Read the depth table**: first-block gradient length against depth for plain and residual stacks, and say what the plain column does (it collapses by a factor of about a thousand every few blocks) and what the residual column does instead.
5. **Use `clip_grad_norm_` correctly** — after `backward()` and before `step()` — and say what it returns (the length *before* clipping).
6. **Say what was NOT shown**: that the residual stack grows without a norm, that layer norm alone did not rescue depth, and why *no single table settles "which device is best"*.

Observable evidence: the filled depth table (workbook page 6.4); the sentence *"batch norm needs more than one example and gets very noisy with two; layer norm looks at one example only"*; and the sentence *"x + f(x) has slope 1 plus the slope of f, so the road stays open while the slope of f stays above -1"*.

---

## 🧑‍🏫 What YOU Need to Know First

Read this section once, slowly. It is about twelve minutes. There is no calculus (the "slope" is a nudge and a division) and no statistics beyond the mean and spread you already teach.

### 1. Why this week exists

Weeks 1–5 changed *how* the same small network (four blocks, 16,962 parameters) is trained. That network never needed help to train. This week it gets **deeper**, and it stops working. The three layers the student has seen in every printout since Week 1 — `Identity()` (which has sat there doing nothing), and the two that replace it, `LayerNorm` and `BatchNorm1d` — and the `+` of a skip connection are the cures. Later weeks depend on all of it: **every transformer block in Weeks 14–17 is written `x = x + attention(norm(x))`**, Week 11's gate is "the highway of Week 6 in a loop", and Week 10 asks what happens when you multiply the same number forty times.

The problem, in one picture. A network is a chain of layers. To learn, the *last* layer's error has to be passed backwards, layer by layer, to the *first*. At each layer it is multiplied by that layer's slope. If each slope is smaller than 1, the product shrinks at every step and the first layer hears nothing. That is a **vanishing gradient**, and it is why a 32-block plain network is stuck at the coin-flip loss (0.693, `ln 2`, Week 1) for the whole run.

> **🧑‍🏫 If you remember one sentence from this section:** *a residual connection turns "multiply the slopes" into "multiply (1 + each slope)", and (1 + a small non-negative number) does not shrink to nothing; a norm layer makes sure nobody downstream gets handed numbers in a strange range; and the only reason there are two kinds of norm is that one of them needs more than one example.*

### 2. 🧭 REAL vs STAND-IN — what everything this week is

| Thing on the screen | Real model or stand-in? |
|---|---|
| Every network and every training run (`run(...)`, `first_block_grad(...)`) | **Real.** The Week 1 network (stem, `depth` blocks, head; 16,962 parameters at depth 4) built by `make_model`, trained for real on a CPU, one thread, seeded. |
| `nn.LayerNorm`, `nn.BatchNorm1d`, `nn.Identity`, `clip_grad_norm_` | **Real PyTorch.** Nothing is simulated. |
| The 3 × 4 grid on the board (`norm_hand.py`), the pairs of numbers in `batch_dep.py`, the four slopes in `slope.py` | **Made-up numbers, on purpose**, so the arithmetic can be done by hand. They are not from a run. |
| The "gradient length on block 1, before any training" | **Real, but of an untrained network.** It is the gradient of one batch of 64 at random weights. It says how well the error *could* reach block 1 at the start; it does not say what happens by epoch 30. `depth_train.py` is the check that does. |
| Any LLM, transformer, or API | **None this week.** Nothing here is a stand-in because nothing here is a language model. |

**What you must NOT claim.** Each of these is tempting after this week, and each is false or unmeasured on what the student sees.

1. **"Residual connections keep the gradient near 1."** The reference module says `(1 + f₁')(1 + f₂')… stays near 1`. That is true only if every `f'` is small. Measured: without a norm, the first-block gradient at 32 blocks is **3.00e+02, 2.02e+01, 6.23e+01, 7.47e+01, 2.63e+01** over five seeds. It does not vanish and it does not stay near 1: it *explodes*. The claim that survives: *a residual road keeps the gradient from vanishing; a norm layer keeps it from growing too much.*
2. **"A plain deep network stalls because its gradient vanishes — at depth 12."** The ledger (re-run of the module's own answer key) found a 12-block plain network trains to 98.9%. Here: plain trains fine at 2 and 8 blocks and is stuck at 46.9% at 16 and 32. The collapse is real; **the cliff is between 8 and 16**, not at 12.
3. **"Layer norm fixes deep networks."** Layer norm alone gives a healthy first-block gradient at 16 and 32 blocks (2.01e+00 and 7.90e+00) and **the network still scores 46.9% — the coin**. We measured that. We did not find out why. Say so (see Question 6). The pair, layer norm *with* a residual road, scored 97.6% and 98.8%.
4. **"Layer norm makes a model robust to a shift in the inputs."** The ledger tested exactly this (workbook-style 2 × 2: matched vs shifted validation data, +1.5 on every feature). Layer norm on shifted data: **48.3%**, no better than batch norm's **46.7%**. The shift enters before any norm layer; normalising afterwards cannot undo it: the shift reaches the hidden features unevenly, so the data fall outside the region the network learned. This is *not* run in class; quote it from the ledger (`_ledger/out/m01_02_answerkey.txt`, Practice 6B) only if asked.
5. **"Gradient clipping makes training better."** It is **insurance**. With plain SGD on 16 residual blocks at a high learning rate it is the difference between `nan` and 98.9% (three seeds each, below). With AdamW at 32 blocks it did **not** help — it made things worse at lr 0.03 (94.7%, 81.9%, 96.7% against 97.8%, 99.2%, 98.9%). One possible reason, which this run did not test, is that Adam already rescales gradients (Week 3).
6. **Anything about a language model.** A spiral classifier tells you nothing about what a 96-block transformer needs. Say: *"a toy result shows a mechanism, not a rate."*

> **Honest framing to say aloud, in your own words:** *"Here is a small network that gets deeper. Without help it stops learning; with a residual road it keeps learning; with norm layers the numbers stay sensible. I'm showing you the mechanism with three seeds, not a recipe."*

### 3. 🔢 THE MATHS YOU NEED, TAUGHT TO YOU FIRST

The new idea this week is the **slope of a sum**. You also need layer norm's arithmetic and one length. Each is worked on real numbers **before** it has a name.

**A. A slope is a nudge and a division (revision — Level 3, Week 12).** To find how steeply `y` rises at `x = 2`: compute `y` at `x = 2`, compute it again at `x = 2.001`, divide the *change* by `0.001`. No formula needed.

**B. Try it on a sum.** Let `f(x) = 0.05 × x × x`, "a block that does only a little". At `x = 2`:

```text
f(2)     = 0.05 × 4        = 0.2
f(2.001) = 0.05 × 4.004001 = 0.20020005
change in f = 0.00020005   → slope of f = 0.00020005 / 0.001 = 0.2
```

Now the **sum**, `y = x + f(x)`: `y(2) = 2.2`, `y(2.001) = 2.001 + 0.20020005 = 2.20120005`. The change is `0.00120005`; divided by `0.001` that is **1.2**. The `x` part moved by exactly `0.001` (slope **1**) and `f` moved by 0.0002 (slope **0.2**). Slopes of the pieces *add*: `1 + 0.2 = 1.2`. `slope.py` prints `0.2`, `1.0`, `1.2` (it rounds). **Do not write `1 + f'(x)` anywhere today.** Say it in words: *"the slope of a sum is the sum of the slopes, and the slope of `x` by itself is 1."* The symbol comes after the student has said it themselves.

**C. Slopes multiply along a chain (revision — Level 3, Week 18).** Four plain blocks, each with a slope at this point of `0.3, 0.2, 0.4, 0.1`. The error going backwards is multiplied by each in turn: `0.3 × 0.2 = 0.06`, `× 0.4 = 0.024`, `× 0.1 =` **0.0024**. With residual roads the four slopes are `1.3, 1.2, 1.4, 1.1`: `1.3 × 1.2 = 1.56`, `× 1.4 = 2.184`, `× 1.1 =` **2.4024**. Do that by hand on the board: it takes ninety seconds and it *is* the lesson. **Four numbers only.** "Multiply the same number many times" is *compounding*, which is Week 10's idea; today there are four different numbers and no powers.

**D. Layer norm, on one row.** Take the row `2, 4, 6, 8`. Mean: `(2+4+6+8) / 4 = 5`. Distances from the mean: `−3, −1, 1, 3`. Square them: `9, 1, 1, 9`; average: `20 / 4 = 5`; square root: `2.236`. That is the row's spread. Divide each distance by it: `−1.342, −0.447, 0.447, 1.342`. The row now has mean 0 and spread 1. That is **layer norm: each row, by its own mean and spread.** (The spread divides by 4, not 3. Do not mention `n − 1`.) Batch norm does the *same arithmetic down a column* — across the examples, one feature at a time.

**E. Why two examples are a disaster for the column version.** Two numbers `a` and `b`: mean `(a + b)/2`, distances `±(a − b)/2`, spread `|a − b|/2`. Divide: **`−1` and `+1`, for *any* `a` and `b`** (as long as they differ). So with a batch of 2, every feature of every example is normalised to `±1`; the only thing left is *which of the two was bigger*. `batch_dep.py` shows it: two completely different pairs of examples give the same `[−1, −1, 1, 1]` / `[1, 1, −1, −1]`.

**F. A length — the 3-4-5 triangle (Week 2).** The gradient `[3, 4]` has length `sqrt(9 + 16) = 5`. Clipping to a maximum length of 1 scales *both* entries by `1/5`: `[0.6, 0.8]`. It keeps the direction and shortens the arrow. If the length is already under the maximum, nothing happens. The function **returns the length it measured before clipping** — here `5.0`.

### 4. Every new line of this week's code, explained to someone who has never seen it

**`nn.LayerNorm(d)`** — a layer that normalises *each example by itself*: for every row of `d` numbers it subtracts that row's mean and divides by that row's spread, then multiplies by a learned scale (`gamma`, starts at 1) and adds a learned shift (`beta`, starts at 0) — so the network *can* undo the normalising if it wants to. That is `2 × d` parameters: `LayerNorm(64)` has **128**. The `d` must equal the size of the **last** dimension of what is fed in (deliberate error 2). It has no running statistics and behaves identically in `train()` and `eval()`.

**`nn.BatchNorm1d(d)`** — the same arithmetic but **down each column**: for each of the `d` features, it uses the mean and spread of that feature across the examples in the batch. Same 128 parameters for `d = 64`, **plus stored numbers that are not parameters**: a *running mean* and a *running variance* per feature (and a counter) — `BatchNorm1d(64)` holds 129 such stored numbers. In `train()` mode it uses the batch's own statistics and *updates* the running ones (slowly: each batch moves them 10% of the way). In `eval()` mode it uses the stored running ones. In `train()` mode it **refuses a batch of one** — `ValueError: Expected more than 1 value per channel when training` — because one number has no spread (deliberate error 1). In `eval()` mode a batch of one is fine. `mode_demo.py` shows both, *and* a trap: after only 3 batches the running mean is still `2.718`, so a 10.0 comes out as `2.753`, not 0. Running statistics need many batches to settle.

**`nn.Identity()`** — a layer that returns its input untouched; no parameters. The student has seen `Identity()` in the printout of Week 1's network (it is the "no norm" placeholder). Why have a layer that does nothing? So a model can say `self.norm = Identity()` and keep the same shape of code whether or not there is a norm. Its other job is the skip path. Deliberate error 4 is the student writing `None` instead.

**`torch.nn.utils.clip_grad_norm_(parameters, max_norm)`** — one call that (1) measures the length of the whole gradient (all the knobs together, as one long arrow, as in Week 2's `.norm()`), (2) if it is longer than `max_norm`, multiplies every gradient by `max_norm / length`, and (3) **returns the length it measured**, before shrinking. The trailing underscore means "changes things in place" (the student has met that in `zero_grad`, `w -= ...`). Placement is everything: after `loss.backward()` (there is nothing to clip before it) and before `opt.step()` (after it, the update has already been made). `silent.py` measures what each wrong placement does. You have already seen it at work: `run(...)`'s `gnorm` column is this function with `max_norm=inf`, which measures and never clips (Week 2 called it "a Week 6 tool").

**Reading, not writing: the block.** The student does *not* write the class that holds these layers (classes are Week 23). They *read* the one line of `l4lib/spirals.py` that is the whole idea, and you should too:

```python
h = self.drop(self.act(self.fc(self.norm(x))))     # norm, then the linear layer, then GELU, then dropout
return x + h if self.residual else h                # the road: x + h, or just h
```

Say: *"`h` is what the block adds. With the road switched on the block hands back `x + h`. Off, it hands back `h`, and `x` is lost."* The norm goes **first** (this is called "pre-norm" and is what transformers do). The student switches things on with `make_model(depth=..., norm="layer", residual=True)`.

### 5. The lab protocol, in plain words

Everything the student runs this week is **one new helper, `first_block_grad`**, plus the harness `run(...)` from Week 1 (which already has `depth=`, `norm=`, `residual=`, `batch_size=` and `clip=` arguments). **One switch per run** — the Week 1 rule. There are three measurements:

- **Small batch table** (`small_batch.py`): validation accuracy for `norm` in none/batch/layer at batch sizes 64, 16, 4, 2. This is the hook.
- **Gradient table** (`probe.py`): how long the gradient on block 1's weights is, *before any training*, for four stack types at depth 2, 8, 16, 32. One batch of 64, seed 0, `loss.backward()`, then `.grad.norm()` — the length from Week 2. Cheap (under a second), and **the table the lesson is built around**.
- **Trained table** (`depth_train.py`): does each stack actually *train*? 30 epochs, three seeds, mean validation accuracy. 46.9% is the always-guess-one-class answer (class balance of the validation set); anything near it means "did not learn".

Three details to be ready for:

- **"Gradient length" is of the first block's `fc.weight` only**, not the whole network. It is the part of the network *furthest from the loss*, so it is the one that hears the error last.
- **`run(...)`'s `gnorm` is the whole-network length at the last step of each epoch.** Different quantity; do not mix them.
- **Seeds.** `first_block_grad(..., seed=0)` fixes the starting weights. `probe_seeds.py` repeats for five seeds; the *size* of the plain column's collapse is the same for every seed (all about `1e-18` at 32 blocks), the residual column's size varies by an order of magnitude (20 to 300). **Say the word "seeds" when you quote a number.**

### 6. The three misconceptions you will actually meet

1. **"A residual connection is just a trick for very deep networks."** It is also why *shallow* networks train faster, and the reason any transformer block can be skipped by the network if it has nothing useful to add (`f(x) ≈ 0` gives `x + 0 = x`, which is much easier to learn than reproducing the identity through three layers). Keep it to one sentence.
2. **"Normalising throws information away."** It throws away *the row's mean and spread* — and the learned `gamma` and `beta` let the network put them back. Ask: *"if the mean were important, could the network use `beta` for that?"* Yes.
3. **"Batch norm is better because it did better on the module's table (0.019 vs 0.064)."** True on that table: batch norm has the better validation loss on this fixed-length, large-batch toy (the reference module and the ledger agree). It is the *dependence on other examples* that makes transformers avoid it (variable-length sequences, batches of one at generation). The honest comparison is on *what each needs*, not on one score.

### 7. How deep to go, and where to stop

Go as far as: *"each row by its own numbers vs each column by the batch's; a batch of two collapses the column version; `x + f(x)` has slope `1 + slope of f` so the gradient has a road; the plain stack's first block hears almost nothing at 16 blocks; clipping is a length cap, used as insurance."* Stop before: *why* layer norm alone fails at 16 blocks (not measured), initialisation schemes (Kaiming/Xavier — "not yet"), the formal chain rule, RMSNorm (one sentence: *"layer norm without the subtracting step; big models use it"*), group norm, weight norm, and "internal covariate shift" (a popular story that is disputed; do not teach it). If the student asks about any, the answer is *"good question, not measured yet, write it in the Bug Log's 'later' column."*

### 8. 🧭 Where this fits (text version — the figure pass comes later)

```text
 TERM 1 — THE TEN KNOBS
 W1  learning rate, one at a time            ✔ done
 W2  momentum  (running average)             ✔ done
 W3  Adam / AdamW  (per-knob step size)      ✔ done
 W4  schedule + batch size                   ✔ done
 W5  four ways to stop memorising            ✔ done
 W6  norms, residuals, clipping              ◀ you are here   (can a DEEP network learn at all?)
 W7  the sweep (all knobs, one grid)         next: depth becomes one more row in the grid
 W8  a cell that remembers (RNN)             ... and W11: the highway of today, in a loop
```

Two minutes at the end of the lesson: ask *"which of today's four layers had weights, which had stored running numbers, and which had neither?"* (`LayerNorm`: weights only. `BatchNorm1d`: weights **and** stored running numbers. `Identity`: neither. `Dropout`, from Week 5: neither.) That is last week's closing question, answered.

---

## 🧰 Prep Checklist

Use this section the night before to get every script running and every number checked before the student sees it.

### 25 minutes the night before

**1. (3 min) Make `l4lib` importable and check versions.** `l4lib/` sits inside `36-week-course/`. Python only finds it if that folder is on the path. Make a folder for this week's files and work in it.

```bash
# from inside the 36-week-course folder, once per terminal:
export PYTHONPATH="$PWD"
mkdir -p w06 && cd w06            # every script below lives here
python3 -c "import torch, numpy; print(torch.__version__, numpy.__version__)"
```

You want a torch version and a numpy version. The numbers in this guide were produced with torch 2.2.1 and numpy 1.26.4 on a CPU, one thread. A different torch build may differ in the last digit of a loss; see "If a number does not match" below.

**2. (3 min) Create `lab6.py` and run its checks.** Everything else this week imports `lab6.py`. It is the only file the student builds in the Live-Code segment (and it is eleven lines).

```python
# lab6.py
import torch
import torch.nn as nn
from l4lib.spirals import get_data, make_model, run

torch.set_num_threads(1)

Xtr, ytr, Xva, yva = get_data()          # the Week 1 spirals: 840 train, 360 validation
lossf = nn.CrossEntropyLoss()

def first_block_grad(depth, *, residual=False, norm="none", seed=0):
    """Length of the gradient on the FIRST block's weights, for one untrained network."""
    torch.manual_seed(seed)
    model = make_model(depth=depth, residual=residual, norm=norm)
    loss = lossf(model(Xtr[:64]), ytr[:64])
    loss.backward()
    return model.blocks[0].fc.weight.grad.norm().item()
```

```python
# checks.py
from lab6 import *
import numpy as np
print(Xtr.shape, ytr.shape, Xva.shape, yva.shape)
for name, kw in [("plain", {}), ("batch norm", {"norm": "batch"}), ("layer norm", {"norm": "layer"}),
                 ("residual", {"residual": True}), ("depth 32", {"depth": 32})]:
    m = make_model(**kw)
    print(f"{name:<11} parameters: {sum(p.numel() for p in m.parameters()):>6}   blocks: {len(m.blocks)}")
print(make_model(depth=2, norm="layer", residual=True).blocks[0])
print(torch.__version__, np.__version__)
```

```text
torch.Size([840, 2]) torch.Size([840]) torch.Size([360, 2]) torch.Size([360])
plain       parameters:  16962   blocks: 4
batch norm  parameters:  17474   blocks: 4
layer norm  parameters:  17474   blocks: 4
residual    parameters:  16962   blocks: 4
depth 32    parameters: 133442   blocks: 32
Block(
  (fc): Linear(in_features=64, out_features=64, bias=True)
  (act): GELU(approximate='none')
  (drop): Dropout(p=0.0, inplace=False)
  (norm): LayerNorm((64,), eps=1e-05, elementwise_affine=True)
)
2.2.1 1.26.4
```

Read it aloud: 840 training and 360 validation points; the plain network has **16,962** parameters; the norm networks have **17,474**, which is `16,962 + 512` (four norm layers, each with 64 scales and 64 shifts, `4 × 128 = 512`); the same count for batch norm and layer norm, because the difference between them is the *direction of the arithmetic*, not the number of weights; the road adds no parameters (`x + h` is just an addition); depth 32 has 133,442 parameters. The printed block shows where the norm sits in the block: it is registered last but runs **first**. (The order of the lines in a printout is the order the layers were *created*, not the order they *run*. Do not let the student read it as the running order.)

**3. (3 min) Run the slope of a sum.** Pure Python; no torch.

```python
# slope.py  -- the slope of a sum, with nothing but a tiny nudge
def f(x):
    return 0.05 * x * x            # a block that does only a little

def slope(fn, x, h=0.001):
    return (fn(x + h) - fn(x)) / h

def plus_f(x):
    return x + f(x)                # the residual block: input PLUS what the block adds

x = 2.0
print("slope of f      at x=2:", round(slope(f, x), 3))
print("slope of x      at x=2:", round(slope(lambda t: t, x), 3))
print("slope of x + f  at x=2:", round(slope(plus_f, x), 3))

print()
print("a stack of four blocks, slope of each one on its own:")
slopes = [0.3, 0.2, 0.4, 0.1]
plain = 1.0
for s in slopes:
    plain = plain * s
print("  plain stack, slopes multiply:     ", round(plain, 4))
roads = 1.0
for s in slopes:
    roads = roads * (1 + s)
print("  residual stack, (1 + slope) each: ", round(roads, 4))
```

```text
slope of f      at x=2: 0.2
slope of x      at x=2: 1.0
slope of x + f  at x=2: 1.2

a stack of four blocks, slope of each one on its own:
  plain stack, slopes multiply:      0.0024
  residual stack, (1 + slope) each:  2.4024
```

The first three lines are the nudge (step `0.001`). The last four are the by-hand multiplication of Concept Part C: `0.3 × 0.2 × 0.4 × 0.1 = 0.0024` and `1.3 × 1.2 × 1.4 × 1.1 = 2.4024`. **Hand-check both before class.**

**4. (3 min) Run layer norm by hand.**

```python
# norm_hand.py  -- layer norm by hand, then check against nn.LayerNorm
import numpy as np
import torch
import torch.nn as nn

x = np.array([[ 2.0, 4.0,  6.0, 8.0],      # example 1
              [10.0, 0.0, 10.0, 0.0],      # example 2
              [ 1.0, 2.0,  3.0, 50.0]])    # example 3  (one huge feature)

mean = x.mean(axis=1, keepdims=True)       # one mean PER EXAMPLE (across its own 4 features)
spread = x.std(axis=1, keepdims=True)      # one spread per example
by_hand = (x - mean) / spread
print("per-example means: ", mean.ravel())
print("per-example spread:", spread.ravel().round(3))
print("by hand:")
print(by_hand.round(3))

ln = nn.LayerNorm(4)
out = ln(torch.tensor(x, dtype=torch.float32))
print("nn.LayerNorm(4):")
print(out.detach().numpy().round(3))                # .detach(): hand numpy the numbers without PyTorch's training bookkeeping. Copy it; Week 22 explains it
print("biggest difference from by-hand:", float(np.abs(out.detach().numpy() - by_hand).max()))
print("learned scale (gamma) and shift (beta):", ln.weight.data.tolist(), ln.bias.data.tolist())
print("each row now has mean", out.mean(dim=1).detach().numpy().round(4), "and spread", out.detach().numpy().std(axis=1).round(3))
```

```text
per-example means:  [ 5.  5. 14.]
per-example spread: [ 2.236  5.    20.797]
by hand:
[[-1.342 -0.447  0.447  1.342]
 [ 1.    -1.     1.    -1.   ]
 [-0.625 -0.577 -0.529  1.731]]
nn.LayerNorm(4):
[[-1.342 -0.447  0.447  1.342]
 [ 1.    -1.     1.    -1.   ]
 [-0.625 -0.577 -0.529  1.731]]
biggest difference from by-hand: 1.267762080869872e-06
learned scale (gamma) and shift (beta): [1.0, 1.0, 1.0, 1.0] [0.0, 0.0, 0.0, 0.0]
each row now has mean [0. 0. 0.] and spread [1. 1. 1.]
```

Read: the three rows have means `5, 5, 14` and spreads `2.236, 5.0, 20.797`. Row 1 is the worked example in Concept Part D. **Row 3 is the instructive one**: `1, 2, 3, 50` has one huge feature, and after layer norm the three small features sit together at about `−0.6` and the big one at `+1.731`. By-hand and `nn.LayerNorm` agree to `1.3e-06` (that gap is the tiny `eps = 1e-05` that stops a division by zero when a row has no spread). The learned scale and shift start at 1 and 0, so the output is *exactly* the by-hand answer until training moves them.

**5. (3 min) Run the batch-dependence demo.** This is the heart of the first half.

```python
# batch_dep.py  -- does an example's answer depend on who else is in the batch?
import torch
import torch.nn as nn

torch.manual_seed(0)
a = torch.tensor([[2.0, 4.0, 6.0, 8.0]])           # our example
others1 = torch.tensor([[1.0, 1.0, 1.0, 1.0], [3.0, 2.0, 1.0, 0.0]])
others2 = torch.tensor([[9.0, 9.0, 0.0, 0.0], [5.0, 7.0, 5.0, 7.0]])
batch1 = torch.cat([a, others1])                    # a with one pair of neighbours
batch2 = torch.cat([a, others2])                    # a with a different pair

bn = nn.BatchNorm1d(4)                              # train mode is the default
ln = nn.LayerNorm(4)
print("example a, batch norm, neighbours 1:", bn(batch1)[0].detach().numpy().round(3))
print("example a, batch norm, neighbours 2:", bn(batch2)[0].detach().numpy().round(3))
print("example a, layer norm, neighbours 1:", ln(batch1)[0].detach().numpy().round(3))
print("example a, layer norm, neighbours 2:", ln(batch2)[0].detach().numpy().round(3))

print()
print("a batch of TWO, batch norm, two completely different pairs:")
pair1 = torch.tensor([[1.0, 5.0, 2.0, 9.0], [2.0, 6.0, 1.0, 3.0]])
pair2 = torch.tensor([[100.0, 0.1, 7.0, 4.0], [101.0, 0.2, 3.0, -50.0]])
print(bn(pair1).detach().numpy().round(3))
print(bn(pair2).detach().numpy().round(3))
```

```text
example a, batch norm, neighbours 1: [0.    1.336 1.414 1.405]
example a, batch norm, neighbours 2: [-1.162 -1.298  0.889  0.843]
example a, layer norm, neighbours 1: [-1.342 -0.447  0.447  1.342]
example a, layer norm, neighbours 2: [-1.342 -0.447  0.447  1.342]

a batch of TWO, batch norm, two completely different pairs:
[[-1. -1.  1.  1.]
 [ 1.  1. -1. -1.]]
[[-1.    -0.998  1.     1.   ]
 [ 1.     0.998 -1.    -1.   ]]
```

Read: the *same* example `a = [2, 4, 6, 8]` gives `[0, 1.336, 1.414, 1.405]` with one pair of neighbours and `[−1.162, −1.298, 0.889, 0.843]` with another: **batch norm's answer for `a` depends on who else is in the batch.** Layer norm gives `[−1.342, −0.447, 0.447, 1.342]` both times. The bottom two matrices: two *completely different* pairs of examples give the same `±1` pattern (the second pair has `−0.998` in one place only because those two inputs, `0.1` and `0.2`, are so close that the `eps` stops being negligible).

**6. (3 min) Run the running-statistics demo.** Includes a real error message.

```python
# mode_demo.py  -- batch norm keeps running statistics for eval mode
import torch
import torch.nn as nn

torch.manual_seed(0)
bn = nn.BatchNorm1d(1)
print("before any data: running mean", round(bn.running_mean.item(), 3), " running var", round(bn.running_var.item(), 3))
for step in range(3):
    batch = torch.randn(64, 1) * 5 + 10               # feature with mean 10, spread 5
    bn(batch)
    print(f"after batch {step + 1}:    running mean {bn.running_mean.item():.3f}  running var {bn.running_var.item():.3f}")

one = torch.tensor([[10.0]])
bn.eval()
print("eval mode, ONE example of 10.0 ->", round(bn(one).item(), 3), "(uses the stored numbers, so a batch of 1 is fine)")
bn.train()
try:
    bn(one)
except ValueError as e:
    print("train mode, ONE example ->", type(e).__name__ + ":", e)
```

```text
before any data: running mean 0.0  running var 1.0
after batch 1:    running mean 1.046  running var 3.659
after batch 2:    running mean 1.948  running var 6.008
after batch 3:    running mean 2.718  running var 6.997
eval mode, ONE example of 10.0 -> 2.753 (uses the stored numbers, so a batch of 1 is fine)
train mode, ONE example -> ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 1])
```

Read: the running mean starts at 0 and the running variance at 1 (arbitrary start values), and after each batch moves 10% of the way towards the batch's numbers (the data have mean 10 and variance 25). After three batches they are `2.718` and `6.997`, still far away. So in `eval()` mode a 10.0 comes out as `2.753`, not near 0: **the stored numbers have not settled yet**. That is the *real* train/eval gap of batch norm. The last line is the message the student will meet in deliberate error 1.

**7. (2 min) Run the `Identity` demo.**

```python
# identity_demo.py  -- nn.Identity does nothing, on purpose
import torch
import torch.nn as nn

x = torch.tensor([[1.0, -2.0, 3.0]])
skip = nn.Identity()
print("Identity gives back the same numbers:", skip(x).tolist(), "  same object?", skip(x) is x)
print("it has parameters?", len(list(skip.parameters())))

torch.manual_seed(0)
block = nn.Linear(3, 3)
nn.init.normal_(block.weight, 0, 0.1)
fx = block(x)
print("f(x)     :", [round(v, 3) for v in fx[0].tolist()])
print("x + f(x) :", [round(v, 3) for v in (skip(x) + fx)[0].tolist()])
```

```text
Identity gives back the same numbers: [[1.0, -2.0, 3.0]]   same object? True
it has parameters? 0
f(x)     : [-0.19, -0.041, -0.741]
x + f(x) : [0.81, -2.041, 2.259]
```

`Identity` returns *the same object* and holds no parameters. The two lines at the bottom are a hand-made block: `f(x)` is what the block "adds", `x + f(x)` is what the road hands on.

**8. (1 min) Run the hook, `small_batch.py`.** This is minute 1 of the lesson. It takes about 8 seconds: start it, *then* start talking.

```python
# small_batch.py  -- the same network, three kinds of norm, four batch sizes
from lab6 import *

print("validation accuracy after 10 epochs (seed 0)")
print("batch size     none   batch norm   layer norm")
for bs in (64, 16, 4, 2):
    row = []
    for norm in ("none", "batch", "layer"):
        h = run(f"{norm}", norm=norm, batch_size=bs, epochs=10, verbose=False)
        row.append(h["acc"][-1] * 100)
    print(f"{bs:>10}   {row[0]:6.1f}%   {row[1]:7.1f}%   {row[2]:8.1f}%")
```

```text
validation accuracy after 10 epochs (seed 0)
batch size     none   batch norm   layer norm
        64     98.3%      96.9%       97.8%
        16     96.9%      98.6%       98.3%
         4     96.4%      63.3%       98.3%
         2     97.8%      46.9%       97.2%
```

Read: with no norm the network scores 96.4–98.3% at every batch size. **Batch norm: 96.9%, 98.6% at batch sizes 64 and 16, then 63.3% at batch size 4 and 46.9% — the coin — at batch size 2.** Layer norm stays at 97–98% throughout. The "46.9%" is the share of the validation set that is class 0: a network that always answers class 0 gets it. The ledger's 30-epoch version of the batch-2 row says the same: batch norm train loss 0.688, val loss 0.677, accuracy 56.4%; layer norm accuracy 98.6%. The size of the failure depends on how many epochs (ledger 30, here 10); **the direction does not**. *(Note: the "batch 4" row, 63.3%, is one seed and 10 epochs; do not build a rule on it.)*

**9. (2 min) Run the gradient table.** The heart of the second half.

```python
# probe.py  -- length of the gradient on block 1, before any training
from lab6 import *

print("depth   plain          residual       layer norm     layer norm + residual")
for depth in (2, 8, 16, 32):
    cells = []
    for kw in ({}, {"residual": True}, {"norm": "layer"}, {"norm": "layer", "residual": True}):
        cells.append(first_block_grad(depth, seed=0, **kw))
    print(f"{depth:>5}   " + "   ".join(f"{c:>12.2e}" for c in cells))
```

```text
depth   plain          residual       layer norm     layer norm + residual
    2       7.01e-02       4.26e-01       2.46e-01       5.40e-01
    8       3.23e-05       1.27e+00       5.29e-01       1.42e+00
   16       1.21e-09       2.61e+00       2.01e+00       1.37e+00
   32       1.27e-18       3.00e+02       7.90e+00       3.58e+00
```

Read down the **plain** column: `7.01e-02`, `3.23e-05`, `1.21e-09`, `1.27e-18`. Between depth 2 and 8 the gradient on block 1 fell by a factor of about **2,000**; between 8 and 16 by about **27,000**; by 32 it is `1e-18`. (Do not call that "exponential" this week; Week 10 does the arithmetic. Say: *"it shrinks by a big factor every few blocks."*) The **residual** column: `4.26e-01`, `1.27e+00`, `2.61e+00`, `3.00e+02` — *no* vanishing, but a climb. The **layer norm** column stays between `2e-01` and `8` — healthy, mildly growing. **Layer norm + residual**: `5e-01` to `3.6` — the calmest.

**10. (2 min) Five seeds of the two extremes.** Is that just seed 0?

```python
# probe_seeds.py  -- is that one seed a fluke? Plain vs residual, five seeds.
from lab6 import *

for depth in (8, 32):
    for residual in (False, True):
        vals = [first_block_grad(depth, residual=residual, seed=s) for s in range(5)]
        print(f"depth {depth:>2}  residual={str(residual):<5}  " + "  ".join(f"{v:9.2e}" for v in vals))
```

```text
depth  8  residual=False   3.23e-05   4.28e-05   3.79e-05   3.66e-05   4.40e-05
depth  8  residual=True    1.27e+00   3.06e-01   3.10e-01   9.63e-01   5.37e-01
depth 32  residual=False   1.27e-18   3.20e-18   2.29e-18   3.34e-18   3.61e-18
depth 32  residual=True    3.00e+02   2.02e+01   6.23e+01   7.47e+01   2.63e+01
```

The plain column is `~4e-05` at 8 blocks and `~3e-18` at 32 for **every** seed; the residual column varies by a factor of 4 to 15 from seed to seed (and is `20` to `300` at 32 blocks). So *the collapse is the same every time; the growth is not*. That is the honest reason this guide says "seeds" over and over.

**11. (3 min) Run the trained table.** About 25 seconds. This is the check that matters.

```python
# depth_train.py  -- does the gradient length decide who can train? 30 epochs, three seeds.
from lab6 import *

configs = [("plain", {}), ("residual", {"residual": True}),
           ("layer norm", {"norm": "layer"}), ("layer norm + residual", {"norm": "layer", "residual": True})]
print("mean validation accuracy over seeds 0-2, 30 epochs")
print(f"{'depth':>5}  " + "  ".join(f"{n:>21}" for n, _ in configs))
for depth in (2, 8, 16, 32):
    cells = []
    for name, kw in configs:
        accs = [run(name, depth=depth, epochs=30, seed=s, verbose=False, **kw)["acc"][-1] for s in range(3)]
        cells.append(100 * sum(accs) / len(accs))
    print(f"{depth:>5}  " + "  ".join(f"{c:>20.1f}%" for c in cells))
```

```text
mean validation accuracy over seeds 0-2, 30 epochs
depth                  plain               residual             layer norm  layer norm + residual
    2                  99.2%                  99.2%                  98.9%                  98.9%
    8                  99.1%                  99.2%                  98.7%                  98.6%
   16                  46.9%                  99.0%                  46.9%                  97.6%
   32                  46.9%                  99.3%                  46.9%                  98.8%
```

Read it in three columns of meaning. **Plain**: 99.2%, 99.1%, **46.9%, 46.9%** — it trains to 8 blocks and never leaves the coin from 16. **Residual**: 99.2%, 99.2%, 99.0%, 99.3% — it trains at every depth. **Layer norm alone**: 98.9%, 98.7%, **46.9%, 46.9%** — the same collapse as plain, *although its first-block gradient was healthy* (`probe.py`: 2.01 and 7.90). **Layer norm + residual**: 98.9%, 98.6%, 97.6%, 98.8%. The pairing with the gradient table is the interesting part: **gradient size predicts the plain stack's failure, but is not the whole story** — the layer-norm-only stack has the gradient and still fails.

**12. (2 min, optional) Do different inputs still look different?** A quick look at *why* the plain stack is stuck.

```python
# spread.py  -- do different inputs still look different after 16 blocks? (untrained network)
from lab6 import *

print("average spread ACROSS the 840 examples of the last block's 64 outputs")
for name, kw in [("plain", {}), ("residual", {"residual": True}),
                 ("layer norm", {"norm": "layer"}), ("layer norm + residual", {"norm": "layer", "residual": True})]:
    row = []
    for depth in (2, 16):
        torch.manual_seed(0)
        model = make_model(depth=depth, **kw)
        with torch.no_grad():
            h = model.blocks(model.stem(Xtr))
        row.append(h.std(dim=0).mean().item())
    print(f"  {name:<22} depth 2: {row[0]:.4f}   depth 16: {row[1]:.4f}")
```

```text
average spread ACROSS the 840 examples of the last block's 64 outputs
  plain                  depth 2: 0.0559   depth 16: 0.0000
  residual               depth 2: 0.5840   depth 16: 4.4045
  layer norm             depth 2: 0.2346   depth 16: 0.2666
  layer norm + residual  depth 2: 0.6330   depth 16: 1.1201
```

At 16 blocks the plain stack's last block outputs are **almost identical for every input** (spread `0.0000`, below 5e-5 across 840 examples): the network has stopped telling inputs apart, so the gradient has nothing to work with at the start. That is the plain stack's problem. Layer norm alone does *not* have it (`0.2666`), so something else is wrong there, and **we did not find out what**. Do not guess aloud; say "not measured".

**13. (3 min) Run the clipping demo.** About 9 seconds.

```python
# clip_demo.py  -- clip_grad_norm_ on two numbers, then on a real run
from lab6 import *

w = torch.tensor([3.0, 4.0], requires_grad=True)
(w * torch.tensor([3.0, 4.0])).sum().backward()      # gradient is exactly [3, 4]
print("gradient before:", w.grad.tolist(), " its length:", w.grad.norm().item())
before = torch.nn.utils.clip_grad_norm_([w], max_norm=1.0)
print("clip_grad_norm_ RETURNED:", before.item(), "(the length BEFORE clipping)")
print("gradient after: ", [round(v, 3) for v in w.grad.tolist()], " its length:", round(w.grad.norm().item(), 3))
w.grad = torch.tensor([0.3, 0.4])
before = torch.nn.utils.clip_grad_norm_([w], max_norm=1.0)
print("a small gradient [0.3, 0.4] is left alone:", [round(v, 3) for v in w.grad.tolist()], " returned", round(before.item(), 3))

print()
print("SGD, 16 residual blocks, lr 0.3, 30 epochs (validation accuracy)")
for clip in (None, 1.0):
    accs = [run("x", depth=16, residual=True, optimizer="sgd", lr=0.3, clip=clip,
                epochs=30, seed=s, verbose=False)["acc"][-1] * 100 for s in range(3)]
    print(f"  clip={str(clip):<4}  seeds 0-2: " + "  ".join(f"{a:5.1f}%" for a in accs))
print("AdamW, 32 residual blocks, lr 0.03, 30 epochs")
for clip in (None, 1.0):
    accs = [run("x", depth=32, residual=True, lr=0.03, clip=clip,
                epochs=30, seed=s, verbose=False)["acc"][-1] * 100 for s in range(3)]
    print(f"  clip={str(clip):<4}  seeds 0-2: " + "  ".join(f"{a:5.1f}%" for a in accs))
```

```text
gradient before: [3.0, 4.0]  its length: 5.0
clip_grad_norm_ RETURNED: 5.0 (the length BEFORE clipping)
gradient after:  [0.6, 0.8]  its length: 1.0
a small gradient [0.3, 0.4] is left alone: [0.3, 0.4]  returned 0.5

SGD, 16 residual blocks, lr 0.3, 30 epochs (validation accuracy)
  clip=None  seeds 0-2:  46.9%   46.9%   46.9%
  clip=1.0   seeds 0-2:  98.9%   98.9%   98.3%
AdamW, 32 residual blocks, lr 0.03, 30 epochs
  clip=None  seeds 0-2:  97.8%   99.2%   98.9%
  clip=1.0   seeds 0-2:  94.7%   81.9%   96.7%
```

Read: the 3-4-5 triangle (`[3, 4]` has length 5; clip to 1 gives `[0.6, 0.8]`; the call **returned 5.0**); a small gradient is left alone (returned 0.5). Then the real one: **SGD, 16 residual blocks, lr 0.3: without clipping, 46.9% on all three seeds (the run went to `nan` — check with `run(..., verbose=True)`); with `clip=1.0`, 98.9%, 98.9%, 98.3%.** And the honest counter-example: **AdamW at 32 blocks, lr 0.03, clipping made it worse** (94.7%, 81.9%, 96.7% against 97.8%, 99.2%, 98.9%). Clipping is insurance, not a performance feature. *(In the 46.9% rows the loss is `nan`; that is "the number blew up", not "slow learning".)*

**14. (3 min) Print the four deliberate errors** — Prep step only. Run each once, so nothing about them surprises you. Their messages are in the Debugging Clinic.

```bash
for f in err1 err2 err3 err4; do echo "=== $f"; python3 $f.py 2>&1 | tail -1; done
```

(You need `err1.py` … `err4.py` from the Live-Code and Clinic sections, below. Create them before running this.)

### Two more scripts to have run

```bash
python3 silent.py     # the three silent mistakes, about 1 second
python3 key.py        # every number in the answer key, under 1 second
MPLBACKEND=Agg python3 homework.py    # the homework reference, about 1 second
```

Their outputs are reproduced in the Debugging Clinic, the Answer Key and the Homework section.

### 5 minutes on the day

1. `cd` to `w06`; `export PYTHONPATH=...` again if this is a new terminal.
2. `python3 checks.py` — the parameter counts (16,962 / 17,474 / 133,442) should match.
3. Write the three board headings (Hook) and the 3 × 4 grid for layer norm (Concept) before the student arrives.
4. Have `small_batch.py` ready to run but **not run**.
5. Print workbook pages 6.1–6.5.

### If a number does not match this guide

| What differs | Why | What to do |
|---|---|---|
| Last digit of a gradient or loss | torch build, BLAS library | Fine. Compare to **two significant figures**. |
| Plain depth-32 gradient is `1e-17` or `1e-19` not `1e-18` | Different float rounding at tiny values | Fine. The point is "about a billion billion times smaller". |
| `small_batch` rows differ by a point or two | Thread count: did you call `torch.set_num_threads(1)`? `lab6.py` does. | Fix the thread count; rerun. The **order** (batch norm worst at batch 2) must hold. |
| Batch norm at batch size 4 is very different from 63.3% | One seed, 10 epochs: it is the noisiest cell | Ignore it; use the batch-size-2 row. |
| `depth_train` plain is *not* stuck at 16 | Wrong depth passed, or `lab6.py` edited | Check `run(..., depth=depth)`; print `len(make_model(depth=16).blocks)`. |

### Fallback if the laptops fail

Everything in the Hook, the Concept and the Their-Turn segments can be done from the printed tables in this guide (Prep steps 8, 9 and 11). Print them. The student fills workbook page 6.4 by reading the **gradient table** and the **trained table** instead of running them, and writes one sentence each. The live-coding and the two deliberate errors are the only parts lost.

---

## ⏱️ The Lesson, Minute by Minute

This section is the whole lesson plan: a timing table first, then each segment in order with what to say, ask, expect and watch for.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Same Network, Two Kinds of Norm | 8 | 8 | Run `small_batch.py`. At batch size 2, batch norm scores 46.9% (the coin) and layer norm 97.2%. "What does a norm layer need that the other doesn't?" |
| 🧠 Concept & Maths — Rows, Columns, and a Road | 15 | 23 | Layer norm by hand on `2, 4, 6, 8`; why two examples give `±1`; the slope of a sum by nudging; four slopes multiplied, plain vs road |
| 💻 Live-Code Together — `lab6.py`, the depth probe, and two mistakes | 17 | 40 | Type `first_block_grad`; predict then run depth 2, 8, 16, 32; break `BatchNorm1d` and `LayerNorm` on purpose |
| 🎲 Their Turn — The Depth Table | 23 | 63 | Fill gradient length and trained accuracy for four stack types at four depths; find the three surprises |
| 🔑 Wrap & Assign | 7 | 70 | Clipping in one minute; the five sentences; homework |

---

### 🪝 Hook — The Same Network, Two Kinds of Norm (8 minutes)

**Do this:** Write on the board:

```text
the Week 1 spirals · same network · AdamW lr 0.003 · 10 epochs · seed 0
three versions: no norm | batch norm | layer norm
four batch sizes: 64, 16, 4, 2
```

> **Say this:** "For five weeks the network was never in trouble. Today I'm going to change two things that sound harmless. One: I'll put a *norm* layer in front of every block — I'll tell you what that is in a minute; for now it's a layer that tidies the numbers. Two: I'll shrink the batch. There are two kinds of norm layer. Write down which one you think will break first, if either."

Let them write a guess. **Do this:** Start `small_batch.py` (about 8 seconds) and keep talking: *"Each cell is the accuracy on 360 points the network never trained on. 46.9% is what you get by always answering the same class."*

**Output they should see** (Prep step 8):

```text
validation accuracy after 10 epochs (seed 0)
batch size     none   batch norm   layer norm
        64     98.3%      96.9%       97.8%
        16     96.9%      98.6%       98.3%
         4     96.4%      63.3%       98.3%
         2     97.8%      46.9%       97.2%
```

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What does the no-norm column do as the batch shrinks?" | Almost nothing: 96–98% every time. | If they say "it goes down a bit": agree (98.3 to 97.8 is 0.5 points; that is seed noise, Week 5). |
| "Which norm breaks, and when?" | **Batch norm**, and at batch size 2 it scores 46.9%: the coin, the same score as always guessing one class. | If they say "both": point at the layer-norm column. |
| "At batch size 64 and 16 batch norm was fine. What changed at 2?" | Only the batch size. Same network, same data, same everything. | If they guess "it needs more epochs": the Week 1 rule is one change at a time. We changed one thing. |
| "Layer norm never cared. What do you think it looks at that batch norm doesn't?" | **Anything other than the one example in front of it.** Accept guesses; don't confirm yet. | If they say "layer norm is just better": ask them to hold that thought until the table at the end. |
| "If I handed you the batch-norm-at-2 model, would you be happy?" | No: 46.9% is the always-guess-one-class score. It learned nothing. | — |

> **Say this:** "Same network, one change, from fine to useless. The only difference between the two columns is *which numbers the norm layer looks at while it tidies*. The next fifteen minutes are what that sentence means."

**Do not** define batch norm or layer norm yet. Write the new words on the board: **batch norm** and **layer norm**, with space below each.

---

### 🧠 Concept & Maths — Rows, Columns, and a Road (15 minutes)

**Do this (5 minutes): layer norm by hand.** Draw a 3 × 4 grid on the board (3 examples, 4 features each), using the numbers from `norm_hand.py`:

```text
                feature 1   feature 2   feature 3   feature 4
   example 1        2           4           6           8
   example 2       10           0          10           0
   example 3        1           2           3          50
```

> **Say this:** "Each row is one example: four numbers describing one point. Layer norm treats *each row on its own*. Take row 1. What's the average of 2, 4, 6, 8?" (5.) "How far is each number from 5?" (−3, −1, 1, 3.) "Square those, average them, square-root the result: that's how spread out the row is." (`9, 1, 1, 9` → 5 → 2.236.) "Divide each distance by 2.236."

Let the student compute `−1.342, −0.447, 0.447, 1.342`. **Ask:** *"What are the new mean and spread?"* (0 and 1 — they can verify: the distances now sum to zero, the squares average to 1.)

> **Say this:** "That's layer norm: each row, by its own average and spread. Now **batch norm** does the same sum, but **down a column** — feature 1 across the three examples: 2, 10, 1."

Draw the arrows: a horizontal arrow through row 1 (layer norm) and a vertical arrow down column 1 (batch norm). **Ask:** *"What does the answer for example 1 depend on, in each case?"* (Layer norm: its own four numbers. Batch norm: its own numbers **and** the other examples in the batch.) Write: **batch norm needs the neighbours.**

**Do this (3 minutes): why a pair is a disaster.** Write two numbers, `a` and `b`, on the board, with `a = 3, b = 9`. **Ask:** *"Batch norm, for this one feature, on this pair. Average?"* (6.) *"Distances from the average?"* (−3 and +3.) *"Spread?"* (3.) *"Divide?"* (−1 and +1.) Now change them: `a = 100, b = 101`. Distances `−0.5, +0.5`, spread `0.5`, divide: **−1 and +1** again.

> **Say this:** "Whatever the two numbers are — 3 and 9, 100 and 101 — after batch norm, one is −1 and the other is +1. Two examples can't tell it anything except *which one is bigger*. That's the collapse you saw in the hook. And one example has no spread at all."

If the student asks "how many examples do you need?": *"More, so the average is steady; 64 was fine. We saw 16 fine and 4 shaky."* That's the table; don't generalise beyond it.

**Do this (4 minutes): the slope of a sum.** Write on the board: `f(x) = 0.05 × x × x`. **Say:** *"This is what one block might do: a little change. I'm going to find how fast it changes at `x = 2` the way you did in Level 3: nudge and divide."* Have the student compute (calculator): `f(2) = 0.2`, `f(2.001) = 0.20020005`; the change is `0.00020005`; divide by `0.001`: **0.2**.

> **Say this:** "Now a different function: `y = x + f(x)`. The input *plus* what the block does. Nudge it the same way. `y(2)`?" (2.2.) "`y(2.001)`?" (2.20120005.) "The change?" (0.00120005.) "Divide by 0.001?" (**1.2**.)

**Ask:** *"Where did 1.2 come from, if f's slope was 0.2?"* (`1 + 0.2`.) *"Where did the 1 come from?"* (From the `x` itself: nudge `x` by 0.001 and the `x` part moves by exactly 0.001.) Write the student's sentence on the board: **the slope of a sum is the sum of the slopes — and the slope of `x` by itself is 1.**

**Do this (3 minutes): a chain of four.** Write four plain blocks with slopes `0.3, 0.2, 0.4, 0.1`. **Say:** *"The error comes back through them one at a time and each one multiplies it by its slope. Multiply: how much of the error reaches the front?"* (`0.0024`: about a quarter of one percent.) Then: *"Same four blocks, but each now hands back `x + f(x)`, so each slope is 1 plus what it was. Multiply `1.3 × 1.2 × 1.4 × 1.1`."* (`2.4024`.) *"Which of those two would you like to be the first block, listening for the error?"*

> **Say this:** "The `+` makes a road. The error can walk straight down it — slope 1 — whatever the block in the middle does. That's a **residual connection**. And it's the reason the network in the hook's no-norm column didn't need any help, but a 32-block one will."

**Do not** write `1 + f'(x)` or say "derivative". **Do not** multiply the same number many times (Week 10). **Do not** say "vanishing gradient" until the table in Their Turn has shown it; the word arrives *after* the thing.

![Two stacks of four blocks with a horizontal bar beside each for the error's running product: the plain stack shrinks to a hairline at 0.0024, the residual stack grows to 2.4024](../figures/fig-w06-1-residual-road-four-blocks.svg)
*Figure 6.1 — With a road each block's slope is 1 plus its old slope, so the error's running product stays near or above 1 instead of shrinking to 0.0024.*

---

### 💻 Live-Code Together — `lab6.py`, the depth probe, and two mistakes (17 minutes)

**Do this:** Have the student type `lab6.py` (Prep step 2) in pieces, saying aloud what each piece is. *Only the second function is new.*

**Piece 1 — the imports and the data (3 minutes).** The first nine lines, ending at `lossf = nn.CrossEntropyLoss()`. Say: *"`make_model` builds the network from Week 1. `get_data` gives the spirals. `run` is the training harness."* Run `checks.py` and read the parameter counts: *"The network with a norm has 512 more numbers: a scale and a shift for each of 64 features in each of 4 blocks."*

**Piece 2 — `first_block_grad` (6 minutes).** Type the function. Say each line:

- *"`def first_block_grad(depth, *, residual=False, norm="none", seed=0)` — the star is the Week 1 'keyword only' rule: I can't mix up the arguments."*
- *"`torch.manual_seed(seed)` and `make_model(...)` — a fresh untrained network at this depth. Nothing has been trained."*
- *"`lossf(model(Xtr[:64]), ytr[:64])` — one batch of 64, one loss."*
- *"`loss.backward()` — pass the error backwards through every block. Now every weight has a `.grad`."*
- *"`model.blocks[0].fc.weight.grad.norm()` — the **first** block, the one furthest from the loss: how long is its gradient arrow?"* (`.norm()` is Week 2.)

**Predict, then run (4 minutes).** **Do this:** run `first_block_grad(2)`, then `first_block_grad(8)` in the Python prompt, and **before each one** ask for a guess. Plain at depth 2 gives `7.01e-02`, at 8 gives `3.23e-05`.

> **Ask this:** "Depth 2 gives 0.07. Depth 8 gives 0.00003. What will 16 give? 32?" Accept guesses on paper. Then run `first_block_grad(16)` and `first_block_grad(32)`: `1.21e-09` and `1.27e-18`. *"A billion-billionth. The first block of a 32-block plain network hears nothing at all."*

Then run `first_block_grad(32, residual=True)` and read it: `3.00e+02` (see Prep step 9). **Ask:** *"What does the road do?"* (The gradient is not tiny.) *"Is it near 1?"* **No — it's 300.** Leave that hanging; Their Turn picks it up.

**Mistake 1 — deliberate (2 minutes).** Say: *"Before we run the full tables, I'm going to show you the error the batch norm gives when you ask it for a batch of one. This is on purpose."* Type `err1.py`:

```python
# err1.py
# DELIBERATE ERROR 1: batch norm in train mode cannot normalise a batch of ONE example
import torch
import torch.nn as nn

bn = nn.BatchNorm1d(4)
one_example = torch.tensor([[2.0, 4.0, 6.0, 8.0]])     # shape (1, 4): a batch of one
print(bn(one_example))
```

**Predict:** *"What will it say?"* Run it. **The real error (file path shortened, torch's own lines elided):**

```text
Traceback (most recent call last):
  File "err1.py", line 8, in <module>
    print(bn(one_example))
  ... frames inside torch (elided) ...
ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 4])
```

> **Say this:** "Read the last line. **Expected more than 1 value per channel when training.** A *channel* is one feature; 'value' is one example's number. Batch norm needs at least two examples to compute a spread, and it tells you so in plain English. The fix: a batch of two or more; *or* `eval()` mode; *or* use layer norm. Which of those would you choose for a model that answers one question at a time?" (Layer norm, or `eval()` with settled running statistics. *This is why transformers use layer norm.*)

**Mistake 2 — deliberate (2 minutes).** Type `err2.py`:

```python
# err2.py
# DELIBERATE ERROR 2: LayerNorm(d) must be told the size of the LAST dimension, here 4 not 8
import torch
import torch.nn as nn

ln = nn.LayerNorm(8)
x = torch.randn(3, 4)                                   # 3 examples, 4 features each
print(ln(x))
```

**Predict:** *"What's wrong with the 8?"* Run it:

```text
Traceback (most recent call last):
  File "err2.py", line 8, in <module>
    print(ln(x))
  ... frames inside torch (elided) ...
RuntimeError: Given normalized_shape=[8], expected input with shape [*, 8], but got input of size[3, 4]
```

> **Say this:** "The norm layer is told how many features it's tidying. I said 8, the data has 4 per row. The message prints the shape it wanted — `[*, 8]` means *anything, then 8* — and the shape it got — `[3, 4]`. That's a Level 3 shape mismatch wearing a new name. **Layer norm's number is always the size of the last dimension.**"

---

### 🎲 Their Turn — The Depth Table (23 minutes)

The full activity is under **🎲 The Activity, In Full** below. The shape: the student fills a 4 × 4 table of *first-block gradient length* (from `probe.py`, a second to run), then a 4 × 4 table of *validation accuracy after training* (from `depth_train.py`, 25 seconds) in a different colour, and then reads three surprises off the pair.

**Part 1 — Predict (3 minutes).** Before anything is run, the student fills the *gradient-length* table with guesses: for each of four stacks at four depths, "bigger than 1, between 0.01 and 1, or tiny". Accept anything; the guesses get compared.

**Part 2 — Run and fill (8 minutes).** Run `probe.py`; they copy the sixteen numbers to page 6.4 in scientific notation (read `3.23e-05` as *"3.23 times ten to the minus five — five zeros before the 3"*). Run `probe_seeds.py` and note the five-seed spread of the plain and residual columns.

**Part 3 — Does it train? (7 minutes).** Run `depth_train.py` (25 seconds; keep talking). They fill the second table. **Ask:** *"Which rows match the gradient table, and which rows don't?"*

**Part 4 — The three surprises (5 minutes).** On the board:

1. **Plain: tiny gradient and 46.9% from 16 blocks.** The first block hears nothing. *Vanishing gradient* — now it has a name.
2. **Residual alone: gradient 20–300 at 32 blocks, and it still trains (99.3%).** The road is *wide enough that the error arrives*. It is not "near 1": it grows, and training copes with it here. (Do not say it will always cope.)
3. **Layer norm alone: healthy gradient, and 46.9% anyway.** *A healthy gradient on the first block is necessary-looking but not sufficient.* We did not find out why. **That is a perfectly good thing to write in the Bug Log's "later" column.**

> **Say this (at the end):** "Fixing the gradient, which the road does, trains the network. Tidying the numbers, which a norm layer does, keeps them calm. The calmest gradient at 32 blocks (`3.58` against `300`) came from the pair, norm and road together; the highest accuracy came from the road alone (99.3% against 98.8%). Both facts are from three seeds. Do not turn either into a law."

![Left, a log-scale chart of first-block gradient length against depth, plain falling to 1e-18 and residual rising to 300; right, grouped accuracy bars where the plain bars at depths 16 and 32 sit at the 46.9 percent coin line](../figures/fig-w06-2-depth-gradient-vs-accuracy.svg)
*Figure 6.2 — The first-block gradient at the start predicts which plain stacks never train; the road keeps every depth at about 99%.*

---

### 🔑 Wrap & Assign (7 minutes)

**Do this (1 minute): clipping.** Run the first half of `clip_demo.py` (the 3-4-5 triangle) or just do it on the board: *"gradient `[3, 4]`; longest I'll allow is 1; the arrow shrinks to `[0.6, 0.8]`. The call tells you how long it was: 5."* Say: *"Clipping is a safety net for the day a run produces a huge gradient. It goes **after** `backward()` and **before** `step()`."* Show the SGD result from Prep step 13: **no clip: 46.9% on all three seeds (the loss became `nan`); clip at 1: 98.9%, 98.9%, 98.3%.** *"And with Adam, in this one setting (lr 0.03, 32 blocks, three seeds), it did not help; a possible reason is that Adam already rescales gradients, but we did not test that. Insurance, not a speed-up."*

**Do this (3 minutes): five sentences.** Ask the student to say, in their own words, each of these (and write them in the Bug Log):

1. Batch norm tidies each *column* using the batch; layer norm tidies each *row* using the example alone.
2. With two examples batch norm turns every feature into `−1` and `+1`, so it learns nothing.
3. `x + f(x)` has slope `1 +` the slope of `f`: the error has a road that stays open while the slope of `f` stays above -1.
4. In a plain stack the first block's gradient fell to `1e-18` at 32 blocks and the network never left 46.9%.
5. We did not find out why layer norm alone failed at 16 blocks.

**Do this (3 minutes): homework.** Hand out workbook pages 6.1–6.5 and say the build: finish the gradient-versus-depth plot (reference script in the Homework section), **five seeds, median** per cell.

---

## 🐞 The Debugging Clinic

Every message below was produced by running a broken version of this week's actual code (torch 2.2.1, numpy 1.26.4). Torch's own frames are elided with `...` and file paths are shortened; the last line and the line from the student's file are what they should read.

> **🧑‍🏫 If a student asks:** the rule from Week 1 stands. **Read the last line, then find the `File` line with your own filename in it.** Today's loud errors are `ValueError` (right type, wrong range: one example), `RuntimeError` (two shapes that do not agree), and `TypeError` (a missing or non-callable thing). Today's **silent** mistakes are the dangerous ones, and there are six.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 4])` | "Batch norm can't take a spread of one number." | A batch of one in train mode (the last batch of a loop; a single test point). | Batch of ≥ 2, **or** `model.eval()`, **or** layer norm. (Deliberate error 1.) |
| `RuntimeError: Given normalized_shape=[8], expected input with shape [*, 8], but got input of size[3, 4]` | "The norm layer was built for 8 features; the data has 4." | `nn.LayerNorm(8)` for 4-feature rows. | `nn.LayerNorm(4)` — the size of the **last** dimension. (Deliberate error 2.) |
| `TypeError: clip_grad_norm_() missing 1 required positional argument: 'max_norm'` | "I need to know how long is too long." | `clip_grad_norm_(model.parameters())` with no limit. | `clip_grad_norm_(model.parameters(), max_norm=1.0)`. (Deliberate error 3.) |
| `TypeError: 'NoneType' object is not callable` | "A layer in the chain is `None`; you can't call it." | "No norm" written as `None` inside `nn.Sequential`. Note the message arrives when the network is *used*, not when it is built. | `nn.Identity()`. (Deliberate error 4.) |
| **No error.** The "clipped" run is exactly as bad as the unclipped one. | Clipping was called before `backward()`: no gradient existed yet. | Clip placed above `loss.backward()`. Silent mistake 1: it **returned 0.0**. | After `backward()`, before `step()`. |
| **No error.** The same model's loss is 2.0 in one place and 0.014 in another. | The model is in `train()` mode: batch norm used a batch of four. | Forgot `model.eval()` before measuring. Silent mistake 2. | `model.eval()` then `torch.no_grad()`. |
| **No error.** A huge loss on the batch after the update (3741). | `clip_grad_norm_` was called after `opt.step()`: the damage was done. | Clip placed below the step. Silent mistake 3. | Between `backward()` and `step()`. |
| **No error.** The plain 32-block network sits at 0.693 for the whole run. | A vanishing gradient, not a bug. | Depth without a road. | `residual=True` (and a norm). Not a code fix; a design fix. |
| **No error.** Batch norm gives 46.9% at batch size 2 and 98% at 64. | Not a bug. See the Hook. | — | Layer norm, or a bigger batch. |
| **No error.** Different numbers on every run. | The generator or the torch seed was not set. | `torch.manual_seed` forgotten. | `torch.manual_seed(seed)` before `make_model`. |

The four loud ones, in order, are the deliberate-error blocks: 1 and 2 in the Live-Code segment, and these two:

```python
# err3.py
# DELIBERATE ERROR 3: clip_grad_norm_ needs to be told how long is too long
import torch
from lab6 import make_model

model = make_model()
torch.nn.utils.clip_grad_norm_(model.parameters())
```

```text
Traceback (most recent call last):
  File "err3.py", line 7, in <module>
    torch.nn.utils.clip_grad_norm_(model.parameters())
TypeError: clip_grad_norm_() missing 1 required positional argument: 'max_norm'
```

> **Say this:** "Python tells you the *name* of the missing piece: `max_norm`. This is the shortest kind of error to read: it names what it wants."

```python
# err4.py
# DELIBERATE ERROR 4: "no norm" written as None instead of nn.Identity()
import torch
import torch.nn as nn

norm = None
net = nn.Sequential(norm, nn.Linear(4, 4))      # building it does not complain...
print(net(torch.randn(2, 4)))                   # ...using it does
```

```text
Traceback (most recent call last):
  File "err4.py", line 8, in <module>
    print(net(torch.randn(2, 4)))                   # ...using it does
  ... frames inside torch (elided) ...
TypeError: 'NoneType' object is not callable
```

> **Say this:** "Look at *where* it fails. Building the network was fine — Python only checks that you gave it things. It fails when you *use* it: `'NoneType' object is not callable` means 'the thing I was about to call as a function is `None`'. Which layer is it? The first one. `nn.Identity()` is the layer that means 'do nothing'."

### The three silent mistakes, measured

The other three silent mistakes in the table (the plain 32-block network sitting at 0.693, batch norm at batch size 2, and an unseeded run) are Hook, Their-Turn and Week 1 material respectively. Here are the three about clipping and modes, run with seeds. Each runs without an error and gives a believable number.

```python
# silent.py  -- three SILENT mistakes: each runs, each gives a believable number
from lab6 import *

# 1. clip BEFORE backward: there is no gradient yet, so there is nothing to clip
torch.manual_seed(0)
model = make_model(depth=16, residual=True)
loss = lossf(model(Xtr[:64]), ytr[:64])
early = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
loss.backward()
late = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
print("1. clip before backward returned", early.item(), "; after backward returned", round(late.item(), 2))

# 2. validation with batch norm still in train mode
torch.manual_seed(0)
bnm = make_model(norm="batch")
opt = torch.optim.AdamW(bnm.parameters(), lr=3e-3)
for step in range(200):
    idx = torch.randint(0, 840, (64,))
    loss = lossf(bnm(Xtr[idx]), ytr[idx]); opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
with torch.no_grad():
    bnm.train()
    a = lossf(bnm(Xva[:4]), yva[:4]).item(), lossf(bnm(Xva[4:8]), yva[4:8]).item()
    bnm.eval()
    b = lossf(bnm(Xva[:4]), yva[:4]).item(), lossf(bnm(Xva[4:8]), yva[4:8]).item()
print("2. same trained model, same 4 points:  train-mode loss", round(a[0], 3), "(batch of 4)  eval-mode loss", round(b[0], 3))

# 3. clip AFTER opt.step: the update already used the big gradient
torch.manual_seed(0)
m1 = make_model(depth=16, residual=True); m2 = make_model(depth=16, residual=True)
m2.load_state_dict(m1.state_dict())
o1 = torch.optim.SGD(m1.parameters(), lr=0.3); o2 = torch.optim.SGD(m2.parameters(), lr=0.3)
for m, o, when in ((m1, o1, "before step"), (m2, o2, "after step ")):
    lossf(m(Xtr[:64]), ytr[:64]).backward()
    if when == "before step":
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
    o.step()
    if when == "after step ":
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
    print("3. clip", when, "-> loss on next batch:", round(lossf(m(Xtr[64:128]), ytr[64:128]).item(), 3))
```

```text
1. clip before backward returned 0.0 ; after backward returned 42.8
2. same trained model, same 4 points:  train-mode loss 2.002 (batch of 4)  eval-mode loss 0.014
3. clip before step -> loss on next batch: 10.546
3. clip after step  -> loss on next batch: 3741.048
```

- **1.** `clip_grad_norm_` before `backward()` **returned `0.0`**; after it, the same network's gradient measured `42.8`. No error, because "clip nothing" is a perfectly valid thing to do. **Tell-tale sign: the returned length is exactly `0.0`.** This is why the function *returns* the length; print it once.
- **2.** The same trained batch-norm model, on the same four validation points: **loss 2.002 in train mode, 0.014 in eval mode**. In train mode batch norm normalised using only those four examples. The model did not get worse; the measuring instrument changed. (The Week 5 silent mistake 2, now with batch norm instead of dropout.)
- **3.** Clipping after the step: the update had already used the raw gradient, so the loss on the next batch was **3741**; clipping before the step: **10.5** (still large, because lr 0.3 on a deep network is aggressive, but survivable beside 3741).

### How to teach debugging without giving the answer

Ask **"What does the last line say?"**, then **"Which of your lines does it point at?"**, then **"What did you give it, and what did it want?"** For the silent mistakes ask **"What is the one number I could print that would tell me this is wrong?"** (the returned length; the loss in `eval()` mode.) Resist saying the fix.

---

## 🎲 The Activity, In Full

This section gives the full depth-table activity and the numbers the student's table should be compared against.

### The Depth Table

The student fills one table with **two** numbers per cell (colours if you can): the length of the first block's gradient at the start, and the accuracy after 30 epochs. Four stacks × four depths. The rows to fill are on workbook page 6.4; the numbers to compare are:

| Depth | Plain | Residual | Layer norm | Layer norm + residual |
|:--:|---|---|---|---|
| 2 | 7.01e-02 / 99.2% | 4.26e-01 / 99.2% | 2.46e-01 / 98.9% | 5.40e-01 / 98.9% |
| 8 | 3.23e-05 / 99.1% | 1.27e+00 / 99.2% | 5.29e-01 / 98.7% | 1.42e+00 / 98.6% |
| 16 | 1.21e-09 / **46.9%** | 2.61e+00 / 99.0% | 2.01e+00 / **46.9%** | 1.37e+00 / 97.6% |
| 32 | 1.27e-18 / **46.9%** | 3.00e+02 / 99.3% | 7.90e+00 / **46.9%** | 3.58e+00 / 98.8% |

*(Gradient: seed 0, one batch, untrained. Accuracy: mean of seeds 0–2. These are the two outputs in Prep steps 9 and 11, side by side.)*

### Part 1 — Predict (3 minutes)

Guess, for each cell of the gradient table, "big (over 1)", "middling (0.01 to 1)" or "tiny (under 0.01)". Common guesses: "all of them get smaller with depth" (the plain column does; the residual column does not).

### Part 2 — Fill the gradient table (8 minutes)

Run `probe.py`. Read three cells aloud together: plain at 32 (`1.27e-18`), residual at 32 (`3.00e+02`), layer norm + residual at 32 (`3.58e+00`). **Ask:** *"Which one would you like on the first block?"* (Most students say the one near 1 — the third.) Then run `probe_seeds.py` and compare: the first cell is the same every time; the second jumps around.

### Part 3 — Fill the accuracy table (7 minutes)

Run `depth_train.py`. Ask: *"Which cells are the coin?"* Four: plain and layer-norm-only at depths 16 and 32. *"Which of those did the gradient table warn us about?"* Two (the plain ones). *"Which did it not warn us about?"* The layer-norm ones. **This is the pair-reading skill of the week.**

### Part 4 — The report (5 minutes)

One paragraph in the Bug Log, three sentences: **what the plain column did in each table; what the residual column did in each table; the one thing we measured and could not explain.**

### Variation — easier

Skip layer norm alone and layer norm + residual. Just plain and residual, depths 2 and 32, with `first_block_grad` only (no training). Two sentences.

### Variation — harder

Add the optional `spread.py` (Prep step 12) and have the student find the depth at which the plain stack's last-block spread goes to zero (try 2, 4, 8, 12, 16). Or ask: *"Does the residual stack at 64 blocks still train?"* — **we have not run that; whatever they find is theirs, and you must not 'know' the answer.**

---

## ❓ Questions Students Ask This Week

Use this section when a student asks something the plan does not cover; each answer stays within what was measured.

**"Why does the norm go *before* the linear layer, not after?"** In the blocks the student runs, norm comes first ("pre-norm"), which is what GPT-style transformers do. The original 2017 transformer put it after ("post-norm"). Pre-norm is easier to train deep. We did not run post-norm here; if the student wants to, it is a good Bug Log "later".

**"What is `gamma` and `beta`?"** A learned scale and shift per feature, starting at 1 and 0. They let the network undo the normalising if it wants. `norm_hand.py` prints them: `[1.0, 1.0, 1.0, 1.0] [0.0, 0.0, 0.0, 0.0]`.

**"Why does batch norm have 'running' numbers?"** At test time there may be one example (or the batch is whatever the user sent), so it cannot use the batch's own statistics. It uses a long-run average collected during training. `mode_demo.py` shows them settling slowly: 1.046, 1.948, 2.718, … towards 10.

**"Is batch norm bad?"** No. On this toy it did *best* on validation loss in the module's table (0.019 against 0.064 for layer norm); it is standard in image networks. It is a poor fit when batches are small or variable, which is why transformers use layer norm.

**"Why does layer norm alone fail at 16 blocks if the gradient is fine?"** **We measured that it does; we did not find out why.** The plain stack's *outputs* lose all difference between inputs (spread 0.0000, `spread.py`); layer norm alone does not (0.2666). Something else is wrong. Say "I don't know; write it down."

**"Why does the residual network's gradient *grow*?"** Each road adds its slope to 1 and the product of those climbs. `3.00e+02` at 32 blocks. A norm layer in front of each block reduces it to `3.58`. Do not derive; point at the two numbers.

**"What does `Identity` do? Why have it?"** Nothing; so the code for "no norm" has the same shape as the code for "a norm". It was in the Week 1 printout all along.

**"Why 1.0 for clipping?"** It is the near-universal default for language-model training (the module says so). An untrained 16-block residual network's gradient has length `42.8` (`silent.py`), so a limit of 1.0 shrinks it a lot. It is a convention, not a derived number. Do not say "optimal".

**"Does clipping change the direction?"** No. Every entry is multiplied by the same number; only the length changes.

**"Can I use both norms together?"** You can; it is rare and untested here.

**"Which is best — residual, norm or both?"** At 32 blocks on this toy: residual alone trains (99.3%), layer norm + residual trains (98.8%), the other two do not. The gradient with both is the calmest (3.58 against 300). Three seeds; not a law.

**"Why does my table differ from the guide's by a little?"** Seed, torch version, thread count. See the checklist. Never copy the guide's number.

**"Does this work for language models?"** Every transformer block you will build in Weeks 14–17 uses `x + f(norm(x))`. Today is why.

---

## ⚠️ Where This Lesson Goes Wrong

These are the seven most likely ways the lesson drifts from what was measured. Check them against your own delivery.

1. **The teacher says "residuals keep the gradient near 1".** Measured: up to 300. Say "keeps it from vanishing".
2. **The layer-norm-alone cell is explained.** It isn't understood. The temptation is to invent a story ("layer norm loses information"). Resist; say "not measured".
3. **Batch size 4 is over-read.** 63.3% is one seed, 10 epochs. It tells you "somewhere between 16 and 2"; no more.
4. **`first_block_grad` is mistaken for the training result.** It is the gradient of an *untrained* network, one batch. The trained table is the check. Insist the student fills both.
5. **The student writes `1 + f'(x)` before saying it in words.** The sentence first: "the slope of a sum is the sum of the slopes".
6. **The class is read from the printout.** The printout lists `fc, act, drop, norm`, which looks like the running order; it is not. The block runs norm first.
7. **Clipping is taught as an optimisation.** It is insurance. The Adam counter-example (clipping made lr 0.03 worse) is in the Prep step 13 for exactly this reason.

---

## 🧭 Differentiation

### If the student is struggling

- Drop the batch-size-4 row, the layer-norm-alone column and the clipping demo. Keep: the layer-norm-by-hand on `2, 4, 6, 8`; the pair collapse; the slope of a sum with one nudge; the plain-vs-residual two-column table at depths 2 and 32.
- If "scientific notation" is the stumbling block: replace `3.23e-05` by "0.0000323" and say "four zeros".
- Do the four-slope multiplication on a calculator, twice, aloud.
- Give the sentence frame: *"Plain: gradient goes ___; residual: gradient goes ___; so the road ___."*

### If the student is flying

- Run `spread.py` at depths 4, 8, 12 and find where the plain stack's outputs stop varying; ask *why that would stop learning*.
- Ask for the layer-norm-alone mystery as a project: *form one hypothesis, design one measurement, run it.* (Possible: print the loss of the layer-norm stack for the first 10 steps; print its last-block spread at each depth; try a smaller learning rate. **None of these has been run for this guide.**)
- Ask them to find the batch size between 16 and 4 at which batch norm starts to fail (three seeds each).
- Ask: *"What does `x + f(x)` do to the gradient if `f` has slope −1?"* (Slope 0 — the road closes. A subtle point; a good one.)

### If the student won't engage today

Do the hook table only, then the residual-vs-plain pair at depth 32. Ask for one sentence: *"The plain network can't learn at 32 blocks because ___."* Do the rest next time as a ten-minute opener.

---

## ✅ Assessing Understanding

Three checks, all oral or on paper, none requiring a computer. Do them at the end of the lesson.

**Check 1 — rows and columns (2 minutes).** Write `4, 6, 8, 10` on the board. *"Layer norm, by hand."* → mean 7, distances `−3, −1, 1, 3`, spread 2.236, answer `−1.342, −0.447, 0.447, 1.342` (the same as `2, 4, 6, 8`: adding the same number to every entry changes nothing). *"Now a batch of just two examples and batch norm: what does each feature become?"* → `−1` and `+1`.

**Check 2 — the road (2 minutes).** *"A block has slope 0.3 at some point. What is the slope of `x + block(x)` there?"* → **1.3**. *"Three blocks with slopes 0.5, 0.5, 0.2: plain stack and road stack?"* → **0.05** and **2.7**. Follow-up: *"Which one hears the error?"*

**Check 3 — the table (2 minutes).** *"A friend says: 'layer norm fixes deep networks, I measured the gradient and it was healthy.' What would you ask?"* → *did it train?* (Layer norm alone had a healthy gradient and 46.9%.) Bonus: *how many seeds; depth 16 or 32?*

### Mastery scale for this week

| Level | What you see |
|---|---|
| **Secure** | Does layer norm by hand; explains the pair collapse; says "slope of a sum is the sum of the slopes" unprompted and computes 1.3; reads the gradient and trained tables **together** and names the cell the gradient did not predict; places clipping after `backward()` and before `step()`. |
| **Nearly there** | Table right; explains layer norm vs batch norm when prompted; says "residuals keep the gradient at 1"; or reads only one of the two tables. |
| **Not yet** | Cannot say what a norm layer looks at; treats the gradient table as the whole answer; cannot say why a batch of one is a problem. Re-teach the hook and the by-hand grid next week (a five-minute opener) and re-ask Check 1. |

---

## 📤 Homework to Assign

~60–75 minutes. Workbook pages 6.1–6.6 (6.3 and 6.4 are paper-and-calculator pages, 6.5 is the error-reading page), plus the build below.

**The build.** The student plots the first-block gradient length against depth (2, 8, 16, 32) for plain and residual stacks, on a log vertical axis, using **five seeds and the median** of each cell. They finish `lab6.py` first. Teacher reference:

```python
# homework.py  -- first-block gradient length against depth, five seeds, with and without the road
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lab6 import *

depths = [2, 8, 16, 32]
for residual, label in ((False, "plain"), (True, "residual")):
    mids = []
    for d in depths:
        vals = sorted(first_block_grad(d, residual=residual, seed=s) for s in range(5))
        mids.append(vals[2])                      # the middle of five = the median
    print(f"{label:<9} median over 5 seeds:", "  ".join(f"d={d}: {m:.2e}" for d, m in zip(depths, mids)))
    plt.plot(depths, mids, marker="o", label=label)
plt.yscale("log"); plt.xlabel("number of blocks"); plt.ylabel("gradient length on block 1 (log scale)")
plt.legend(); plt.savefig("w06_gradient_vs_depth.png", dpi=100)
print("saved w06_gradient_vs_depth.png")
```

```text
plain     median over 5 seeds: d=2: 6.66e-02  d=8: 3.79e-05  d=16: 1.46e-09  d=32: 3.20e-18
residual  median over 5 seeds: d=2: 3.06e-01  d=8: 5.37e-01  d=16: 2.61e+00  d=32: 6.23e+01
saved w06_gradient_vs_depth.png
```

(The picture is saved as `w06_gradient_vs_depth.png`; the plain line falls from `7e-02` to `3e-18` and the residual line climbs from `0.3` to `62`.) Written, three sentences: **(1)** what the plain line does and by roughly how many powers of ten across the whole range; **(2)** what the residual line does and one reason not to say it "stays near 1"; **(3)** one thing the plot does not show (it does not show *training*: the untrained gradient is a prediction, `depth_train.py` is the test).

**Optional extension.** Use `run(..., depth=32, residual=True, clip=1.0)` against `clip=None` at the default AdamW lr 0.003, three seeds, and report whether clipping helped. *(Nothing has been recorded for this at lr 0.003; let the student's own three seeds speak.)*

---

## 🔑 Answer Key

This section holds the answers to every workbook page, page by page. Keep it away from the student.

### Page 6.1 — Match the word to the thing

| Word | Match |
|---|---|
| layer norm | normalise each example (each row) by its own mean and spread |
| batch norm | normalise each feature (each column) by the mean and spread across the batch |
| running statistics | stored averages batch norm uses in `eval()` mode, updated slowly in `train()` mode |
| residual connection | a block hands back `x + f(x)` instead of `f(x)` |
| vanishing gradient | the error reaching the first layers is tiny because every layer multiplied it by something under 1 |
| `nn.Identity()` | a layer that returns its input and has no parameters |
| gradient clipping | if the gradient's length is over a limit, shrink it to the limit (same direction) |

Parameter counts (from `key.py`): **`LayerNorm(64)` 128 parameters, no stored numbers; `BatchNorm1d(64)` 128 parameters and 129 stored numbers; `Identity` 0.**

Block-parts figure (workbook Figure W6.3): 1 norm (layer norm), 2 linear layer, 3 GELU, 4 dropout, 5 the road (`x` carried past the boxes), 6 the add `x + h`, 7 `h`. With the road off the block returns just `h`.

### Page 6.2 — Predict the output

```python
# key.py  -- every number in the answer key, computed
import numpy as np
import torch
import torch.nn as nn

def by_hand(row):
    row = np.array(row, dtype=float)
    return ((row - row.mean()) / row.std()).round(3).tolist()

print("6.3a layer norm of [0, 0, 6, 6]:", by_hand([0, 0, 6, 6]))
print("6.3b layer norm of [1, 3, 5, 7]:", by_hand([1, 3, 5, 7]), "  and of [2, 4, 6, 8]:", by_hand([2, 4, 6, 8]))
print("6.3c layer norm of [5, 5, 5, 5]:", nn.LayerNorm(4)(torch.tensor([5.0, 5.0, 5.0, 5.0])).tolist(), "(spread 0, so only epsilon saves the division)")
pair = torch.tensor([[1.0, 5.0], [3.0, 9.0]])
print("6.3d batch norm on a pair of examples:", nn.BatchNorm1d(2)(pair).detach().numpy().round(3).tolist())

for slopes in ([0.3], [0.5, 0.5, 0.2]):
    plain, roads = 1.0, 1.0
    for s in slopes:
        plain = plain * s
        roads = roads * (1 + s)
    print(f"6.4 slopes {slopes}: plain {plain:.4f}  residual {roads:.4f}")

w = torch.tensor([1.0, 1.0], requires_grad=True)
(6 * w[0] + 8 * w[1]).backward()
r = torch.nn.utils.clip_grad_norm_([w], max_norm=5.0)
print("6.2c gradient [6, 8], max_norm 5: returned", round(r.item(), 1), " gradient now", [round(v, 2) for v in w.grad.tolist()])
w.grad = torch.tensor([1.0, 2.0])
r = torch.nn.utils.clip_grad_norm_([w], max_norm=5.0)
print("6.2d gradient [1, 2], max_norm 5: returned", round(r.item(), 3), " gradient now", w.grad.tolist())

ln, bn = nn.LayerNorm(64), nn.BatchNorm1d(64)
print("6.1 LayerNorm(64): parameters", sum(p.numel() for p in ln.parameters()), " stored buffers", sum(b.numel() for b in ln.buffers()))
print("    BatchNorm1d(64): parameters", sum(p.numel() for p in bn.parameters()), " stored buffers", sum(b.numel() for b in bn.buffers()))
bn_eval = nn.BatchNorm1d(4).eval()
print("6.2b BatchNorm1d(4) in eval mode on one row [2, 4, 6, 8]:", [round(v, 3) for v in bn_eval(torch.tensor([[2.0, 4.0, 6.0, 8.0]]))[0].tolist()])
print("    Identity: parameters", sum(p.numel() for p in nn.Identity().parameters()))
```

```text
6.3a layer norm of [0, 0, 6, 6]: [-1.0, -1.0, 1.0, 1.0]
6.3b layer norm of [1, 3, 5, 7]: [-1.342, -0.447, 0.447, 1.342]   and of [2, 4, 6, 8]: [-1.342, -0.447, 0.447, 1.342]
6.3c layer norm of [5, 5, 5, 5]: [0.0, 0.0, 0.0, 0.0] (spread 0, so only epsilon saves the division)
6.3d batch norm on a pair of examples: [[-1.0, -1.0], [1.0, 1.0]]
6.4 slopes [0.3]: plain 0.3000  residual 1.3000
6.4 slopes [0.5, 0.5, 0.2]: plain 0.0500  residual 2.7000
6.2c gradient [6, 8], max_norm 5: returned 10.0  gradient now [3.0, 4.0]
6.2d gradient [1, 2], max_norm 5: returned 2.236  gradient now [1.0, 2.0]
6.1 LayerNorm(64): parameters 128  stored buffers 0
    BatchNorm1d(64): parameters 128  stored buffers 129
6.2b BatchNorm1d(4) in eval mode on one row [2, 4, 6, 8]: [2.0, 4.0, 6.0, 8.0]
    Identity: parameters 0
```

The workbook's six questions, in its order:

- **P1.** `nn.BatchNorm1d(4)` in train mode on **one** row raises `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 4])`.
- **P2.** The same layer after `bn.eval()`: no error; very nearly the input, `[2.0, 4.0, 6.0, 8.0]` (stored mean 0, variance 1).
- **P3.** `nn.LayerNorm(4)` on `[5, 5, 5, 5]`: every distance 0, spread 0, `eps` stops the division by zero, output `[0.0, 0.0, 0.0, 0.0]`.
- **P4.** Gradient `[6, 8]`, `max_norm=5`: length `sqrt(100)` = 10, prints `10.0`, gradient becomes `[3.0, 4.0]` (new length 5).
- **P5.** Gradient `[1, 2]`: length `sqrt(5)` = 2.236, not over 5, gradient unchanged, prints `2.236`.
- **P6.** `nn.Identity()`; 0 numbers.

### Page 6.3 — Normalise by hand

- **Worked example.** `[4, 8]` gives `[−1, 1]`.
- **(a)** `[0, 0, 6, 6]` → mean 3, distances `−3, −3, 3, 3`, spread 3 → **`[−1, −1, 1, 1]`**.
- **(b)** `[1, 3, 5, 7]` → mean 4, distances `−3, −1, 1, 3`, spread `sqrt(5)` = 2.236 → **`[−1.342, −0.447, 0.447, 1.342]`**, the same as `[2, 4, 6, 8]`: adding the same number to every entry leaves the answer unchanged.
- **(c)** `[20, 40, 60, 80]` gives the same `[−1.342, −0.447, 0.447, 1.342]`: every distance and the spread both grow ten times.
- **(d)** `[5, 5, 5, 5]` → distances 0, spread 0; `0 / 0` is undefined; torch prints **`[0, 0, 0, 0]`** (epsilon keeps the division legal). Accept "undefined" with a note that torch returns zeros.
- **(e)** Batch norm on the pair `[1, 5]` and `[3, 9]`: feature 1 has mean 2, distances `−1, 1`, spread 1; feature 2 has mean 7, distances `−2, 2`, spread 2; both give `−1, 1`, so **A = [−1, −1], B = [1, 1]**. The second pair, A = `[10, 0]` and B = `[20, 4]`, gives the same **A = [−1, −1], B = [1, 1]**: the collapse. Layer norm for A needs only A, so A's answer does not depend on who else is in the batch.

### Page 6.4 — The slope of a sum, and the depth table

**(a)** For `f(x) = 0.1x²` at `x = 3`: change 0.0006001, slope about **0.6**; `x` has slope **1.0**; `x + f(x)` goes from 3.9 to 3.9016001, slope about **1.6**. Pattern: the slope of a sum is the sum of the slopes (1 plus whatever `f` does). For `f = −0.5x` the slope of `f` is −0.5 and of `x + f` is **0.5**; the road is still open (positive, but shrunk).

**(b)** Slopes `0.5, 0.5, 0.2`: plain **0.05**, residual **2.7**; ten blocks of slope 0.5: plain **0.000977**, residual **57.665**; five blocks of slope 0: plain **0**, residual **1**. Plain shrinks to nothing, the residual does not shrink (here it grows) and reaches block 1. The warning sentence: each block gives `1 + slope`, and a number over 1 multiplied again and again grows; the road keeps the signal from vanishing, it does not keep it near 1. Method accepted: nudge by `0.001` and divide. **Full credit** for "the road adds 1 to each slope, so the product cannot shrink to nothing".

**(c)** `7.01e-02` = 0.0701; `3.23e-05` = 0.0000323; 0.0000000012 = `1.2e-09`; `3.00e+02` = 300. `7.01e-02` is bigger, by about 16 powers of ten.

**(d)** The depth table is the one printed in 🎲 The Activity, In Full. Accept any gradient within a factor of two of the printed one *at the student's own seed*, and accuracies within about two points. **Four** coin cells (46.9%): plain and layer-norm-only at depths 16 and 32; the gradient warned about the two plain ones and did not warn about the two layer-norm-only ones. **The three required observations:** (i) the plain column collapses (`7e-02` to `1e-18`) and is stuck at 46.9% from 16 blocks; (ii) the residual column's gradient *grows* (to about `3e+02` at 32 blocks, seed 0) and trains at every depth; (iii) layer norm alone has a healthy gradient and does **not** train at 16 or 32 blocks, unexplained. Five seeds, residual, 32 blocks: **3.00e+02, 2.02e+01, 6.23e+01, 7.47e+01, 2.63e+01**; not near each other, so one seed is not enough to quote this cell. The 64-block question is unanswered: nobody has run it.

### Page 6.5 — Read the message

| Message | What it means | Fix |
|---|---|---|
| `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 4])` | Batch norm in train mode got one example. | Batch of ≥ 2; or `model.eval()`; or layer norm. |
| `RuntimeError: Given normalized_shape=[8], expected input with shape [*, 8], but got input of size[3, 4]` | The norm layer was built for 8 features and the data has 4. | `nn.LayerNorm(4)`. |
| `TypeError: clip_grad_norm_() missing 1 required positional argument: 'max_norm'` | The limit was not given. | Add `max_norm=1.0`. |
| `TypeError: 'NoneType' object is not callable` | A layer in the chain is `None`. | `nn.Identity()`. |

**Marking note for the batch-norm question:** a student who writes "batch norm has no running average" is *half* right; the running statistics exist and are what `eval()` uses. Give the mark for any of the three fixes with the right reason, not for "use a bigger batch" without the reason (this is the same standard Assessment 1's Bug C3 uses).

**F1.** `nn.LayerNorm(8)` on data of shape `[3, 4]` fails: give `LayerNorm` the size of the last dimension, here 4. **F2.** Building `nn.Sequential(None, nn.Linear(4, 4))` does not complain; calling the network does (`TypeError: 'NoneType' object is not callable`); use `nn.Identity()`.

**S1.** The clip ran before `backward()`, so there was no gradient: it printed `length returned: 0.0` (after `backward()` the same net measures **1.323**). The tell-tale is the returned length of exactly 0.0; fix by clipping after `loss.backward()`. **S2.** Forgot `model.eval()` (and `torch.no_grad()`): in train mode batch norm used only four examples (loss 2.002 in train mode, 0.014 in eval mode). **S3.** Order: `zero_grad` (1), `backward` (2), `clip_grad_norm_` (3), `opt.step()` (4); clipping after the step is too late (loss on the next batch 3741 against 10.5; see Silent mistake 3).

### Page 6.6 and Self-Check

Bug Log: any real entries with the last line copied and the fix working. Sentence: "A deep plain stack that sits at 0.693 is not necessarily **broken**, it may be **a vanishing gradient**." The silent bugs are S1 (the number 0.0), S2 (the loss in `eval()` mode) and S3 (the loss on the next batch). Self-Check: 1 row, column; 2 `ValueError`, returns a result, running statistics; 3 1, the slope of `f`; 4 under, multiplied; 5 no, at 32 blocks the gradient grew to 20 to 300 over five seeds; 6 before the clip, after `backward()` and before `opt.step()`; 7 layer norm alone at depth 16 or 32 (gradient 2.01 or 7.90, accuracy 46.9%).

### Mastery check — the table in one sentence

*"A deep plain network's first block hears almost nothing, so it never leaves the coin; a residual road lets the error arrive (sometimes too loudly); a norm layer keeps the numbers calm; batch norm needs the neighbours, layer norm doesn't; and layer norm alone did not rescue depth here, for a reason we did not find."*

---

## 🔮 Next Week Preview

This section says what next week does with today's results, so you can close the lesson with a bridge.

**Week 7 — Project: The Symptom-Check-Action Playbook.** No new idea; one new tool (`itertools.product`, every combination of several lists) and a table the student must be able to defend. The student runs a sweep of 75 runs on the spirals (about 30 seconds at the default 60 epochs), prints the mean and the spread over three seeds for each knob, and turns what Weeks 1-6 taught into a playbook: each **symptom** in a loss curve gets **one cheap check** and **one action**, and every line is backed by a number they printed themselves. Nothing this week is a stand-in; it is real PyTorch on the CPU. The thing to carry in from today: a difference between two runs only counts if it is bigger than the spread between seeds.

---

## 📝 Notes for the next author

This section is for whoever revises the guide: where numbers came from, what the guide contradicts, and what was not run.

- **Numbers that came from the ledger, not from this guide's own scripts:** the 30-epoch batch-2 row (train 0.688, val 0.677, 56.4%) and the layer-norm shift result (48.3% vs batch norm 46.7%). Both are in `_ledger/out/m01_02_answerkey.txt`, Practice 6.
- **The module's claims this week contradicts:** "plain depth 12 stalls" (it trains: 98.9%); "`(1+f1')(1+f2')…` stays near 1" (it grows, 20 to 300 at 32 blocks without a norm); "layer norm adapts to a shift" (it does not, 48.3%). None of these is repeated in this guide.
- **Not run, so not claimed:** residual stacks deeper than 32; post-norm; layer norm alone with other learning rates; what is wrong with layer norm alone at 16 blocks.
- **Week 7** adds `depth` to its sweep and says it has not been run for its guide; the numbers in this guide are the only ones that exist for depth. Week 9 Assessment 1 checks a batch of one (Bug C3), the length `clip_grad_norm_` returns (B6) and the slope of a sum (A16): all three are taught here with the same wording.
- **Week 11** reuses this week's road as a gate: the gate near 1 is `x + f(x)` with a multiplier.
