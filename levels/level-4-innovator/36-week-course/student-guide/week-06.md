# Week 6 — Norms, Residuals, and the Gradient Highway

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Next ➡ Week 7](week-07.md) · [Workbook](../workbook/week-06.md)

---

> ### This week in one sentence
> **A deep stack of plain layers can sit at the coin-flip loss for ever because the error cannot get back to its first layer; a residual connection `x + f(x)` gives the error a road, a norm layer keeps the numbers calm, and the two kinds of norm are not interchangeable, because batch norm leans on the other examples in the batch and layer norm does not.**
>
> **By the end of this chapter you will be able to:**
> - **Compute layer norm by hand** on one row of four numbers, and say which direction batch norm averages in instead
> - **Explain why batch norm breaks at batch size 2** and layer norm does not
> - **Use the slope of a sum:** if `f` has slope 0.3 at some point, say what `x + f(x)` has there, after *seeing* it with a tiny nudge
> - **Read a depth table** of first-block gradient length against number of blocks, for plain and residual stacks
> - **Use `clip_grad_norm_`** after `backward()` and before `step()`, and say what it returns
> - **Say what was not shown** this week, as clearly as what was
>
> **New maths:** **the slope of a sum.** You will find it by nudging a number, before it has a formula.
>
> **New syntax:** `nn.LayerNorm(d)` · `nn.BatchNorm1d(d)` · `nn.Identity()` · `torch.nn.utils.clip_grad_norm_`
>
> **Reading time:** about 45 minutes. **Homework:** about 60–75 minutes.

> **📌 About the code blocks.**
> - Each block is its own file. The ones that say `from lab6 import *` need the `lab6.py` you build in Step 2, in the same folder. If you paste a block on its own and get `NameError` or `ModuleNotFoundError: No module named 'lab6'`, that is why; nothing is broken.
> - The blocks marked **DELIBERATE ERROR** are broken on purpose.
> - Every output shown was printed by a real run on a CPU, one thread, with a seed set (torch 2.2.1, numpy 1.26.4). Your numbers should match to every digit shown, except that file paths inside an error message will be your own. For a loss or accuracy that differs in the last digit, compare to two significant figures.
> - Every network and training run this week is **real**. The small grids of numbers in `slope.py`, `norm_hand.py` and `batch_dep.py` are **made up on purpose** so you can check the arithmetic by hand.
> - Nothing this week needs the internet, and nothing is a language model.
>
> **Before you start:** `l4lib` must be importable. From inside the `36-week-course` folder, once per terminal: `export PYTHONPATH="$PWD"`, then `mkdir -p w06 && cd w06`. If you see `ModuleNotFoundError: No module named 'l4lib'`, that is the fix.

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 6 is highlighted with a pointer above it, weeks 1 to 5 are outlined solid, and every later tile has a dashed outline](../figures/fig-w06-0-where-this-fits.svg)
*Figure 6.0 — Where this fits: week 6 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## 🪝 Start Here

Since Week 1 you have trained the same small network: four blocks, 16,962 parameters. It never needed help to train. This week the question changes from *"how do I train it better?"* to *"how do I make a deep network trainable at all?"*

First, one experiment you will run in Step 4. The same network, the same spirals, 10 epochs, seed 0. The only things changed are the **kind of norm layer** inside it (none, batch, layer) and the **batch size** (how many examples are shown per step, Week 4). Here is the table with the top rows filled in and the bottom rows hidden:

```text
validation accuracy after 10 epochs (seed 0)
batch size     none   batch norm   layer norm
        64     98.3%      96.9%       97.8%
        16     96.9%      98.6%       98.3%
         4         ?          ?            ?
         2         ?          ?            ?
```

Before you read further, write in your Bug Log:

1. At batch sizes 64 and 16 all three columns score about 97–98%. What do you predict happens as the batch size shrinks to 4 and then 2, for each column? Three guesses, one per column.
2. A coin that always says "class 0" gets **46.9%** on the validation set (that is the share of class 0). If you saw 46.9% in the table, what would it mean?
3. Which of the two norm layers do you think would be bothered by a **small batch**? Why might that be? Even a silly reason is fine.

You will come back to your guesses in Step 4.

---

## 🧠 The Big Idea

This section explains why deep plain stacks fail to learn, and the three devices that fix it. You need it before the code, because every experiment below tests one of these ideas.

### 1. The problem: the error has a long way to go

To learn, the *last* layer's error has to be passed backwards, layer by layer, to the *first*. At each layer it is multiplied by that layer's **slope** (how much the layer's output moves when its input is nudged).

If each slope is smaller than 1, the error shrinks at every step on the way back and the first layer hears almost nothing. That is called a **vanishing gradient**.

A network in that state does not learn; it sits at the coin-flip loss (0.693, which is `ln 2`, from Week 1) for the whole run.

The fixes this week are two cheap devices and one emergency tool:

| Device | What it does | In one line |
|---|---|---|
| **Norm layer** | Re-centres and re-scales the numbers inside the network | *No layer is ever handed numbers in a strange range.* |
| **Residual connection** | Hands on `x + f(x)` instead of just `f(x)` | *The error has a road back.* |
| **Gradient clipping** | Shortens a gradient that is too long | *Insurance, not a speed-up.* |

### 2. 🔢 The maths, worked on numbers first

This part teaches one new idea (the slope of a sum) and the arithmetic of layer norm. Each is done on real numbers before it gets a name. Use a calculator or pencil.

**A. A slope is a nudge and a division** (you did this in Level 3). To find how steeply `y` rises at `x = 2`: work out `y` at `x = 2`, work it out again at `x = 2.001`, divide the **change** by `0.001`. No formula needed.

**B. Try it on a sum.** Let `f(x) = 0.05 × x × x`, "a block that does only a little". At `x = 2`:

```text
f(2)     = 0.05 × 4        = 0.2
f(2.001) = 0.05 × 4.004001 = 0.20020005
change in f = 0.00020005   → slope of f = 0.00020005 / 0.001 = 0.2
```

Now the **sum**, `y = x + f(x)`. `y(2) = 2.2`. `y(2.001) = 2.001 + 0.20020005 = 2.20120005`. The change is `0.00120005`, and divided by `0.001` that is **1.2**.

Look at where the 1.2 came from. The `x` part moved by exactly `0.001`, so its slope is **1**. The `f` part moved by 0.0002, so its slope is **0.2**. The slopes of the pieces *add up*: `1 + 0.2 = 1.2`. In words: **the slope of a sum is the sum of the slopes, and the slope of `x` by itself is 1.** That is the whole new idea. Write that sentence in your Bug Log in your own words.

**C. Slopes multiply along a chain.** Four plain blocks, each with a slope (at this point) of `0.3, 0.2, 0.4, 0.1`. The error going backwards is multiplied by each in turn. **Do it by hand now:**

```text
0.3 × 0.2 = 0.06      × 0.4 = ?      × 0.1 = ?
```

Now give each block a road. Each block's slope is now `1 +` its old slope, so `1.3, 1.2, 1.4, 1.1`. Multiply those four in turn the same way. Compare the two answers. You will check them against the computer in Step 1.

**D. Layer norm, on one row.** Take the row `2, 4, 6, 8`.

```text
mean:                    (2 + 4 + 6 + 8) / 4 = 5
distances from the mean: -3, -1, 1, 3
square them:             9, 1, 1, 9      average: 20 / 4 = 5      square root: 2.236   ← the row's "spread"
divide each distance by the spread:   -1.342, -0.447, 0.447, 1.342
```

The row now has mean 0 and spread 1. That is **layer norm: each row, using its own mean and spread.** (The spread divides by 4, the number of entries. Do not worry about 3.) **Batch norm does the same arithmetic down a column** instead: across the examples, one feature at a time.

**E. Why two examples are a disaster for the column version.** Take two numbers, `a` and `b`. Their mean is `(a + b)/2`. Their distances from it are `+(a − b)/2` and `−(a − b)/2`. Their spread is `|a − b|/2`. Divide each distance by the spread and you get exactly **`+1` and `−1`**, for *any* `a` and `b` that differ. Try it with `a = 3, b = 11` and then `a = 100, b = 101` on paper. Keep that result in mind for Step 4.

**F. A length: the 3-4-5 triangle** (Week 2). The gradient `[3, 4]` has length `sqrt(9 + 16) = 5`. To *clip* it to a maximum length of 1, scale both entries by `1/5`, giving `[0.6, 0.8]`: same direction, shorter arrow. If it was already shorter than the maximum, nothing changes.

![Two stacks of four blocks with a horizontal bar beside each for the error's running product: the plain stack shrinks to a hairline at 0.0024, the residual stack grows to 2.4024](../figures/fig-w06-1-residual-road-four-blocks.svg)
*Figure 6.1 — With a road each block's slope is 1 plus its old slope, so the error's running product stays near or above 1 instead of shrinking to 0.0024.*

### 3. The four new lines of syntax

Each entry below names the call, what it does, and the one rule that trips people up.

**`nn.LayerNorm(d)`.** A layer that normalises **each example by itself**: for every row of `d` numbers, it subtracts that row's mean, divides by that row's spread, then multiplies by a learned **scale** (`weight`, starts at 1) and adds a learned **shift** (`bias`, starts at 0). So the network *can* undo the normalising if that turns out to help.

That is `2 × d` parameters: `LayerNorm(64)` has 128. The `d` must equal the size of the **last** dimension of what you feed in. It behaves identically in `train()` and `eval()`.

**`nn.BatchNorm1d(d)`.** The same arithmetic, but **down each column**: for each of the `d` features it uses the mean and spread of that feature *across the examples in the batch*. Same 128 parameters for `d = 64`, **plus stored numbers that are not parameters**: a *running mean* and a *running variance* per feature.

In `train()` mode it uses the batch's own statistics and updates the stored ones a little (10% of the way towards the batch each time). In `eval()` mode it uses the stored ones. In `train()` mode it needs more than one example.

**`nn.Identity()`.** A layer that hands back exactly what it was given. No parameters. You have seen `Identity()` in the printout of the Week 1 network: it is the "no norm" placeholder. Having a layer that does nothing lets a model say `self.norm = Identity()` and keep the same shape of code whether or not there is a norm.

**`torch.nn.utils.clip_grad_norm_(parameters, max_norm)`.** One call that does three things, in this order:

- (1) Measures the length of the *whole* gradient (all the knobs together, as one long arrow: Week 2's `.norm()`).
- (2) If that length is more than `max_norm`, multiplies every gradient by `max_norm / length`.
- (3) **Returns the length it measured, before shrinking.**

The trailing underscore means "changes things in place". Where you put it matters: **after `loss.backward()`** (before it there is no gradient to clip) and **before `opt.step()`** (after it, the update has already been made). The `gnorm` column that `run(...)` has been printing since Week 2 is this function with `max_norm=inf`, which measures and never clips.

### 4. Reading, not writing: the block

You will not write the class that holds these layers (classes arrive in Week 23). You will *read* the two lines of `l4lib/spirals.py` that are the whole idea. They are shown as text, not for you to type:

```text
h = self.drop(self.act(self.fc(self.norm(x))))     # norm, then the linear layer, then GELU, then dropout
return x + h if self.residual else h                # the road: x + h, or just h
```

`h` is what the block *adds*. With the road switched on the block hands back `x + h`. Off, it hands back `h`, and `x` is lost. The norm goes **first** in the block. You switch things on with `make_model(depth=..., norm="layer", residual=True)`. (When you print a block, the layers appear in the order they were *created*, not the order they *run*.)

---

## 💻 Try It Yourself

In this section you check the maths on the computer, build `lab6.py`, run the small-batch experiment, break four things on purpose, and read the depth tables. Do the steps in order.

### Step 1 — the maths, on the computer

Type each of these as its own file and run it. Each takes under two seconds, and each shows one idea from The Big Idea in numbers.

**The slope of a sum.** Check your hand arithmetic from Part C.

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

Look at the last two lines and compare them with your pencil answers from Part C. Four numbers, no powers: that is the entire reason a road helps. (Multiplying the *same* number many times is a bigger topic, and it is Week 10's.)

**Layer norm by hand, then by machine.** This file does Part D with numpy, then asks `nn.LayerNorm` for the same thing.

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

Row 1 is the one you did on paper. Look at row 3: `1, 2, 3, 50` has one huge feature, and afterwards the three small ones sit together near `−0.6` while the big one is at `+1.731`. The by-hand and `nn.LayerNorm` answers differ by about `1e-06`: that is a tiny constant (`eps = 1e-05`) that stops a division by zero when a row has no spread at all. The scale and shift start at 1 and 0, so the output is *exactly* the by-hand answer until training moves them.

**Does an example's answer depend on who else is in the batch?**

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

Read the first four lines: it is the *same* example `a` every time. Compare it with Part E. (The `-0.998` in the last block is because those two inputs, `0.1` and `0.2`, are so close together that the tiny `eps` stops being negligible.)

**Batch norm's stored numbers.** This file feeds three batches to a batch norm layer and watches its stored numbers move. In it, the `torch.randn` line draws a column of seeded, bell-shaped random numbers, then stretches them to a spread of five and shifts them to centre on ten.

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

The stored mean starts at 0 and the stored variance at 1 (arbitrary starting values), then each batch moves them 10% of the way towards the data (mean 10, variance 25). After three batches they are still far away, so in `eval()` mode a 10.0 comes out as `2.753`, not near 0. Stored numbers need many batches to settle. The `try`/`except` is just a safe way to print an error message instead of stopping; you meet the same message as a deliberate error in Step 4.

**`Identity` does nothing, on purpose.** This file shows that `nn.Identity()` returns its input unchanged, then adds a small block's output to it by hand. The `nn.init.normal_` line overwrites the layer's weights with random numbers centred on zero, with the last argument as their typical size.

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

Look at the last two lines: `f(x)` is what a hand-made block "adds"; `x + f(x)` is what the road hands on.

**Clipping on two numbers.** Run just the first half of this file for now. The whole file takes about 9 seconds because of the training runs at the bottom; you will read those in Step 5.

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

This block needs `lab6.py` from Step 2, so do Step 2 first if you want to run it. The first four lines are the 3-4-5 triangle from Part F. The bottom block is the real thing, which you will read in Step 5.

### Step 2 — build `lab6.py`

This step builds the file that everything else this week imports. It is short, and only the second function is new. Type it in two pieces.

**Piece 1: the imports and the data.**

```python
# lab6.py
import torch
import torch.nn as nn
from l4lib.spirals import get_data, make_model, run

torch.set_num_threads(1)

Xtr, ytr, Xva, yva = get_data()          # the Week 1 spirals: 840 train, 360 validation
lossf = nn.CrossEntropyLoss()
```

`make_model` builds the network from Week 1, `get_data` gives the spirals, `run` is the training harness. All three are in `l4lib`; you import them, you never copy them.

**Piece 2: `first_block_grad`.** Add this to the bottom of the same file.

```python
def first_block_grad(depth, *, residual=False, norm="none", seed=0):
    """Length of the gradient on the FIRST block's weights, for one untrained network."""
    torch.manual_seed(seed)
    model = make_model(depth=depth, residual=residual, norm=norm)
    loss = lossf(model(Xtr[:64]), ytr[:64])
    loss.backward()
    return model.blocks[0].fc.weight.grad.norm().item()
```

Read it line by line:

- `def first_block_grad(depth, *, residual=False, norm="none", seed=0)`: the `*` is the Week 1 "keyword only" rule, so the arguments cannot be mixed up.
- `torch.manual_seed(seed)` then `make_model(...)`: a fresh, **untrained** network at this depth.
- `lossf(model(Xtr[:64]), ytr[:64])`: one batch of 64 examples, one loss.
- `loss.backward()`: pass the error backwards through every block. Every weight now has a `.grad`.
- `model.blocks[0].fc.weight.grad.norm()`: the **first** block, the one *furthest from the loss*. How long is its gradient arrow? (`.norm()` is Week 2.)

This measures an **untrained** network, one batch. It says how well the error *could* reach block 1 at the start. It does not say what happens by epoch 30; Step 5 checks that.

Now check the build with a file that prints the data shapes, the parameter counts and one printed block:

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

Look at the parameter counts, then answer these in your Bug Log (the numbers are on your screen):

- The norm networks have 512 more parameters than the plain one (`17,474 − 16,962`). Where do 512 come from? (Hint: how many norm layers, and how many scales and shifts in each?)
- Batch norm and layer norm have the *same* count. What does that tell you about where they differ?
- The road adds no parameters. Why not?

### Step 3 — predict, then probe

This step is a prediction game on `first_block_grad`. Open a Python prompt in the folder (`python3`) and type `from lab6 import *`. Then **before each call, write your guess** for the answer (is it big, middling or tiny?), and then run it:

```python
first_block_grad(2)
first_block_grad(8)
```

Plain at depth 2 gives `7.01e-02`, and at depth 8 gives `3.23e-05`. (Read `3.23e-05` as *3.23 times ten to the minus five*: five zeros come before the 3. `e-05` means "a hundred-thousandth".) Now guess depth 16, then depth 32, and write the guesses down. Then run:

```python
first_block_grad(16)
first_block_grad(32)
first_block_grad(32, residual=True)
```

Look at the third call for longer than the others.

### Step 4 — the hook table, and four deliberate errors

**The hook.** Run this to fill in the hidden rows of the Start Here table. It takes about 8 seconds; read your Bug Log guesses while it runs.

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

Look at the bottom row and compare it with your three guesses. Then link it to Part E: what does a column-wise norm do to a batch of two? The batch-size-4 row is one seed and 10 epochs, the noisiest cell in the table, so build your argument on the batch-size-2 row, and do not build a rule on the 63.3%.

**Two deliberate errors.** Both are broken on purpose. Read the **last line** of each error and say what it is asking for *before* you fix anything.

```python
# err1.py
# DELIBERATE ERROR 1: batch norm in train mode cannot normalise a batch of ONE example
import torch
import torch.nn as nn

bn = nn.BatchNorm1d(4)
one_example = torch.tensor([[2.0, 4.0, 6.0, 8.0]])     # shape (1, 4): a batch of one
print(bn(one_example))
```

```text
Traceback (most recent call last):
  File "err1.py", line 8, in <module>
    print(bn(one_example))
  ... frames inside torch (elided) ...
ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 4])
```

```python
# err2.py
# DELIBERATE ERROR 2: LayerNorm(d) must be told the size of the LAST dimension
import torch
import torch.nn as nn

ln = nn.LayerNorm(8)
x = torch.randn(3, 4)                                   # 3 examples, 4 features each
print(ln(x))
```

```text
Traceback (most recent call last):
  File "err2.py", line 8, in <module>
    print(ln(x))
  ... frames inside torch (elided) ...
RuntimeError: Given normalized_shape=[8], expected input with shape [*, 8], but got input of size[3, 4]
```

Fix each.

- Error 1: write down *three different ways* to make the program run, and say which you would choose for a model that answers one question at a time.
- Error 2: the message prints the shape it wanted and the shape it got; say what `[*, 8]` means and what the rule for LayerNorm's number is.

Two more deliberate errors, in the same style:

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

For error 4, note **which line** failed and compare it with the line that caused the problem. How far apart are they? Which layer was the `None`?

**One more thing to print, no error involved.** If you call `clip_grad_norm_` and keep what it returns, you can print it. Run the 3-4-5 part of `clip_demo.py` again and look at what the call gave back. A clip that returns exactly `0.0` on a real network is telling you something about where you put it. Which of the two placements (before `backward()`, or after) would return `0.0`, and why?

### Step 5 — read the depth tables

This step shows how long the error is when it reaches the first block, then checks whether that predicts who can train. Both programs are quick; run `probe.py` first.

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

Look down the columns and compare each with your guesses. Is it only seed 0? This file repeats the plain and residual cases over five seeds.

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

That table is the *gradient* the first block receives at the start. It is a prediction. The real question is whether the network **trains**. This one takes about 25 seconds, so start it and read ahead:

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

![Left, a log-scale chart of first-block gradient length against depth, plain falling to 1e-18 and residual rising to 300; right, grouped accuracy bars where the plain bars at depths 16 and 32 sit at the 46.9 percent coin line](../figures/fig-w06-2-depth-gradient-vs-accuracy.svg)
*Figure 6.2 — The first-block gradient at the start predicts which plain stacks never train; the road keeps every depth at about 99%.*

Now go back to `clip_demo.py` from Step 1 and run the whole file. Its second half is a real experiment on clipping: with plain SGD (Week 2) on 16 residual blocks at a high learning rate, and with AdamW (Week 3) on 32 blocks. (In the SGD rows without clipping, the loss became `nan`, which means "the number blew up", not "learning slowly".)

---

## 🎲 Your Turn — The Depth Table

This section turns the depth tables into a prediction, two tables and a three-sentence report. It is the week's main deliverable.

You will fill the page 6.4 table in the workbook. Four stacks by four depths, two numbers per cell: the first-block gradient length at the start (`probe.py`) and the validation accuracy after training (`depth_train.py`). Use two pen colours.

**Part 1 — predict (about 3 minutes).** *Before* looking at the numbers above again (cover them if you scrolled), guess for every cell of the gradient table: "big (over 1)", "middling (0.01 to 1)" or "tiny (under 0.01)". Write your sixteen guesses down.

**Part 2 — fill the gradient table (about 8 minutes).** Run `probe.py` and copy the sixteen numbers in scientific notation. Then run `probe_seeds.py`. For the plain column and for the residual column, say whether the *size* of the number is the same from seed to seed. Which column would you describe with "about 3e-18 every time", and which with "somewhere between 20 and 300"?

**Part 3 — fill the accuracy table (about 7 minutes).** Run `depth_train.py` and fill the second table. Then answer:

- Which cells are the coin (46.9%)?
- Which of those did the gradient table warn you about, and which did it not?
- Pair the two tables for each column. Which columns agree with each other and which do not?

**Part 4 — the report (about 5 minutes).** One paragraph, three sentences, in the Bug Log:

```text
In the plain column, the gradient was ___ and the accuracy was ___.
In the residual column, the gradient was ___ and the accuracy was ___.
One thing I measured and cannot explain: ___.
```

A thing you measured and cannot explain is a good result. Put it in the "later" column of your Bug Log.

**Easier version.** Only plain and residual, depths 2 and 32, and only the gradient (no training). Two sentences.

**Harder version.** Run `first_block_grad` for plain at depths 2, 4, 8, 12 and 16 and find where the collapse begins. Or run a 64-block residual stack for 30 epochs and see whether it trains. **That has not been run for this course, so whatever you find is yours; no one has the answer.** Use three seeds and say how many you used.

---

## 🔑 Wrap Up

This section checks that you can state the week's ideas in your own words, and lists what the week did not show.

Answer these before you close the laptop:

1. Batch norm tidies each ___ using the batch; layer norm tidies each ___ using the example alone. Fill in the blanks.
2. In your own words, why does a batch of two make batch norm useless? (Use Part E.)
3. `x + f(x)` has slope ___ plus the slope of `f`. What does that mean for the error travelling backwards?
4. What number did you see for the plain 32-block network's first-block gradient, and what accuracy did it get?
5. What does `clip_grad_norm_` return, and where does it go in the training loop?
6. Which of today's four layers had weights, which had stored running numbers, and which had neither? (`LayerNorm`, `BatchNorm1d`, `Identity`, and last week's `Dropout`.)
7. What do you want to know about this next? Put it in your Parking Lot.

Then write this sentence in your Bug Log, in your own handwriting:

> **"A toy result shows a mechanism, not a rate. I say how many seeds I ran, and I do not turn a table of three seeds into a law."**

Things you may read elsewhere that are **not** shown by anything you measured this week; write them in the "later" column:

- That a residual connection keeps the gradient "near 1". The residual column above did **not** stay near 1; at 32 blocks it was 20 to 300. What survives is the weaker claim that the road keeps it from *vanishing*.
- That layer norm on its own fixes deep networks. The table above is the evidence you need to say whether that is true here.
- **Why** layer norm alone failed in the table. Nobody measured it.
- That clipping makes training better. You saw one case where it saved a run and one where it did not.
- Anything about a large language model. A spiral classifier tells you nothing about what a 96-block transformer needs.

---

## 📝 Vocabulary

The words below are new or reused this week.

| Word | Meaning |
|---|---|
| **normalise** | Subtract the mean and divide by the spread so the numbers have mean 0 and spread 1. |
| **layer norm** | Normalise each example by itself, across its own features (each row). |
| **batch norm** | Normalise each feature across the examples in the batch (each column). |
| **running statistics** | The mean and variance batch norm stores while training, used in `eval()` mode. Not parameters. |
| **train mode / eval mode** | `model.train()` and `model.eval()`. Dropout and batch norm behave differently in the two; layer norm does not. |
| **residual / skip connection** | Handing on `x + f(x)` instead of `f(x)`. |
| **gradient highway** | The road that a skip connection gives the error on its way back to the first layer. |
| **vanishing gradient** | The error shrinks at every layer on the way back and the first layer hears almost nothing. |
| **gradient length** | The length of the gradient as one long arrow (`.norm()`). |
| **gradient clipping** | Shrinking the gradient to a maximum length if it is longer. Done after `backward()`, before `step()`. |
| **slope of a sum** | The slope of `x + f(x)` is the slope of `x` (which is 1) plus the slope of `f`. |

---

## 🏠 Homework

Homework turns your own runs into a plot and a short written claim.

Workbook Week 6, pages 6.1 to 6.5 (about 60 to 75 minutes). Everything you write down must come from **your own run, printed on your own screen, with a seed set**, not from this chapter.

1. **Finish your own `lab6.py`** and the four checks (`checks.py`, `probe.py`, `depth_train.py`, `clip_demo.py`) so every one runs from a fresh terminal.
2. **Plot gradient length against depth.** For depths `[2, 8, 16, 32]`, compute the first-block gradient length for a plain stack and a residual stack using **five seeds** (`range(5)`) and take the **median** (the middle one of five) of each cell. Plot both lines on one figure with a **log** vertical axis (`plt.yscale("log")`), using matplotlib as in Level 2, and save it as a PNG. Run it with `MPLBACKEND=Agg` if your screen cannot open windows. Print the medians as well as plotting them.
3. **Three sentences.** (1) What the plain line does, and by roughly how many powers of ten across the whole range. (2) What the residual line does, and one reason not to say it "stays near 1". (3) One thing the plot does **not** show.
4. **Optional extension.** Run `run(..., depth=32, residual=True, clip=1.0)` against `clip=None` at the default AdamW learning rate, three seeds, and report whether clipping helped. Nobody has measured this for the course; the result is yours.

**The one line to write in your Bug Log tonight:** *"Two examples are not enough to tell what is normal. One example always is."*

---

## 🔮 Next Week

Week 7 is the first project week: **The Symptom-Check-Action Playbook**. You will sweep several of the knobs from Weeks 1 to 6 (depth is now one more of them) over a small grid, three seeds each, and hand in a one-page playbook that maps each symptom on a loss curve to one cheap check and one action. It uses one new Python tool, `itertools.product`.

**Before then:** keep `lab6.py` exactly as it is. Bring one sentence: *which of this week's symptoms (stuck at 0.693, or a number turning into `nan`) would you check first, and what would you print to check it?*

---

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Next ➡ Week 7](week-07.md) · [Workbook](../workbook/week-06.md)
