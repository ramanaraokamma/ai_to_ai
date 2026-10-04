# Week 10 — Forty Multiplications: Why Memory Fades

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Workbook](../workbook/week-10.md)

---

> ### This week in one sentence
> **Learning a recurrent cell sends an error backwards through the loop, and at every step back it is multiplied by that step's slope; forty slopes below 1 multiply to almost nothing, forty above 1 to an enormous number, and clipping can only cure the second.**
>
> **By the end of this chapter you will be able to:**
> - **Compound by hand**: work out `r ** k` on a calculator for `r` below and above 1, and say *before* you press the key whether the answer will be tiny, near 1, or large
> - **Explain why an error vanishes or explodes** on its way back through a loop, in one sentence
> - **Measure it**: print the size of the gradient at position 1 for sequence lengths 10, 20, 40 and 80 and four settings of the recurrent weights, and read each row of the table in one sentence
> - **Force an explosion** with one update of the knobs, with and without `clip_grad_norm_`, and read the weight size before and after
> - **Say what clipping does not do**
>
> **New maths:** **compounding**: a number multiplied by itself `T` times, `r ** T`. You will do it on a calculator before you do it on the computer.
>
> **New syntax:** `h.retain_grad()` · `torch.stack` · `torch.randn(T, ...)`
>
> **Reading time:** about 30 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60-70 minutes.

> **📌 About the code blocks.** Type the seven blocks below into **one file, `week10.py`**, one under the other with no gap, and run the file after adding each block. Later blocks use names defined by earlier ones. The output printed under each block is what **that block** prints. Every output shown was printed by a real run on a CPU, with the seeds shown. The by-hand numbers match to every digit. The tiny and huge numbers (like `2.06e-10`) can differ in their second digit on a different PyTorch version; their sizes, and the shape of every table, will not. Blocks marked **DELIBERATE** are written on purpose to behave in a way you must notice. Nothing this week needs the internet, and nothing imports `l4lib`. There is no language model and no stand-in anywhere. The cell is a **real** PyTorch loop with **untrained** weights (seeded random numbers), and the inputs are seeded random numbers too. The only "training" all week is **one** update of the knobs, in the last block.

---

## 🪝 Start Here

Forty people stand in a line. The first whispers a message to the second. Each person is a little forgetful: each passes on **95%** of what they heard and loses 5%.

How much of the original message reaches the fortieth person?

**Before you touch a calculator**, write a guess on a card, with a number: half? a third? nine tenths? Keep the card.

Now press `1`, then `x 0.95`, forty times. Say the number out loud after 5, 10, 20 and 40 presses. Compare it with your card.

Then the other way. Everyone *adds* a little: each passes on **105%** of what they heard. Guess first, then press.

Words to keep in mind:

- A **position** is a place in a sequence. Position 1 is the first word; position 41 is the forty-first.
- A **gradient** is how much the final number cares about a value. You have met **vanishing gradients** and **clipping** in Week 6.

---

## 🧠 The Big Idea

### 1. Compounding: the same multiplication, again and again

If each step keeps 95%, you do not lose 5% in total. You lose 5% of **what is left**, forty times. That is **compounding**: a number multiplied by itself `T` times is `r ** T`.

Type block 1 into `week10.py`. It prints the same multiplication for three rates. Before you run it, guess one cell: what is `0.9526 ** 10`?

**Block 1**

```python
# compound.py - Week 10: a number multiplied by itself k times. No torch.
for rate in [0.9526, 0.95, 1.05]:
    print(f"rate {rate}")
    for k in [1, 2, 5, 10, 20, 40]:
        print(f"   {rate} ** {k:2d} = {rate ** k:.4g}")

# How many multiplications until it is below one half? (above double, for 1.05)
for rate in [0.9526, 0.95]:
    value, k = 1.0, 0
    while value > 0.5:
        value = value * rate
        k = k + 1
    print(f"{rate}: first below 0.5 after {k} multiplications ({value:.4f})")
value, k = 1.0, 0
while value < 2.0:
    value = value * 1.05
    k = k + 1
print(f"1.05: first above 2 after {k} multiplications ({value:.4f})")
```

```text
rate 0.9526
   0.9526 **  1 = 0.9526
   0.9526 **  2 = 0.9074
   0.9526 **  5 = 0.7844
   0.9526 ** 10 = 0.6153
   0.9526 ** 20 = 0.3786
   0.9526 ** 40 = 0.1434
rate 0.95
   0.95 **  1 = 0.95
   0.95 **  2 = 0.9025
   0.95 **  5 = 0.7738
   0.95 ** 10 = 0.5987
   0.95 ** 20 = 0.3585
   0.95 ** 40 = 0.1285
rate 1.05
   1.05 **  1 = 1.05
   1.05 **  2 = 1.103
   1.05 **  5 = 1.276
   1.05 ** 10 = 1.629
   1.05 ** 20 = 2.653
   1.05 ** 40 = 7.04
0.9526: first below 0.5 after 15 multiplications (0.4827)
0.95: first below 0.5 after 14 multiplications (0.4877)
1.05: first above 2 after 15 multiplications (2.0789)
```


The two `while` loops write `value = value * rate` out in full, on purpose, so you can **see** the multiplication that `**` hides.

Read the **shape**, not the table:

- A number a *little* under 1 loses about 5% a step, and after forty steps you have about *one-eighth*.
- A number a *little* over 1 gains about 5% a step, and after forty steps you have *seven times*.
- At about 5% a step, it halves (or doubles) in **about 14 or 15 steps**. "About": that is a rule of thumb, not a formula.

Neither direction is "about the same". **Below 1: tiny. Above 1: huge. The only rate that stays put is exactly 1.** If your card said "about 80%", you have just seen why the next hour matters.

### 2. Where the multiplication hides in a loop

In Week 8 you unrolled a cell: four boxes, each one's note fed to the next, with arrows going **right**. Learning works backwards. The last note has to ask: *"how much did note 1 matter to me?"* That is a slope, like the ones in Week 6: **slopes multiply along a chain**. An unrolled loop *is* a chain, with the same layer repeated. Pushing the error back along it has a name: **backpropagation through time** ("time" just means the steps of the sentence).

So the question is: how big is the slope of **one** step? The cell from Week 8 is

> new note = `tanh(W_xh x + W_hh x old note)`

Ask: *how far does the new note move if I nudge the old one?* You know how to find out (Level 3): nudge by a tiny step, divide. For this cell the answer has a shortcut: **`W_hh x (1 - new note squared)`**. You will not derive it. You will **check** it by nudging.

Block 2 takes Week 8's own four notes (`0.7616, 0.3634, 0.1797, 0.0896`, with `W_hh = 0.5`) and prints the slope into each later note.

**Block 2**

```python
# slopes.py - Week 10: Week 8's cell (W_xh = 1.0, W_hh = 0.5, no bias), and the slope from one note to the next.
import math
import torch
import torch.nn as nn
torch.set_num_threads(1)

W_hh = 0.5
notes = [0.7616, 0.3634, 0.1797, 0.0896]          # the four notes of Week 8, hand.py
slopes = []
for h in notes[1:]:                                # the slope INTO each later note
    s = W_hh * (1 - h * h)                         # shortcut: tanh's slope is 1 - note squared
    slopes.append(s)
    print(f"slope into note {h}: {s:.4f}")
print("note 1 -> note 4 is three multiplications:", round(slopes[0] * slopes[1] * slopes[2], 4))

# Check one slope the Level-3 way: nudge the old note, see how far the new note moves.
old, nudge = 0.7616, 0.001
new_a = math.tanh(0.5 * old)                      # x = 0 at step 2, so only the old note feeds in
new_b = math.tanh(0.5 * (old + nudge))
print("by nudging:", round((new_b - new_a) / nudge, 4), "  by the shortcut:", round(W_hh * (1 - new_a ** 2), 4))
```

```text
slope into note 0.3634: 0.4340
slope into note 0.1797: 0.4839
slope into note 0.0896: 0.4960
note 1 -> note 4 is three multiplications: 0.1041
by nudging: 0.4339   by the shortcut: 0.434
```


Three steps back, about a tenth of the signal is left (`0.4340 x 0.4839 x 0.4960`). Forty steps back, at a typical slope of `0.5`? Press `0.5 ^ 40` on your calculator. (It is `9.1e-13`: a millionth of a millionth.)

The nudge check at the bottom agrees with the shortcut to rounding (`0.4339` against `0.4340`). Two ways to the same number: that is why we trust the shortcut.

### 3. The parked cell: a loop where every slope is the same

Real slopes change from step to step. To see the theory cleanly, we **cheat on purpose** and build a one-number cell whose note sits still at `0.2177`. Its slope is then `1 - 0.2177 ** 2 = 0.9526` at **every** step. If the theory is right, the gradient at position 1 of a chain of 41 notes should be `0.9526` multiplied forty times. Predict it, then run block 3.

This block has the first new construct. **`h.retain_grad()`**: `h` was made from other things, so it is an *in-between* value. PyTorch normally throws away the gradient of in-between values to save memory, keeping only the knobs'. This line says: **keep this one**. After `backward()`, `h.grad` is how much the final number cares about that note. It goes *before* `backward()`.

**Block 3**

```python
# parked.py - Week 10: a one-number cell with W_hh = 1.0 whose note is PARKED at 0.2177, so every slope is the same.
w = torch.tensor(1.0, requires_grad=True)        # the recurrent weight, tracked so a gradient can flow

def run_parked(T):
    h = torch.tensor(0.2177)
    notes = []
    for t in range(T):
        h = torch.tanh(w * h + 0.0035)           # x = 0 every step; 0.0035 keeps the note parked
        h.retain_grad()                          # keep the gradient of this in-between value
        notes.append(h)
    notes[-1].backward()                         # slopes of the LAST note with respect to every earlier note
    return notes

notes = run_parked(41)
print("the note, positions 1, 2, 41:", [round(notes[i].item(), 4) for i in (0, 1, 40)])
print("slope of one step: 1 - 0.2177**2 =", round(1 - 0.2177 ** 2, 4))
for p in [41, 40, 39, 31, 21, 11, 1]:
    print(f"position {p:2d}: gradient {notes[p - 1].grad.item():.4f}   0.9526 ** {41 - p:2d} = {0.9526 ** (41 - p):.4f}")
```

```text
the note, positions 1, 2, 41: [0.2177, 0.2176, 0.217]
slope of one step: 1 - 0.2177**2 = 0.9526
position 41: gradient 1.0000   0.9526 **  0 = 1.0000
position 40: gradient 0.9529   0.9526 **  1 = 0.9526
position 39: gradient 0.9080   0.9526 **  2 = 0.9074
position 31: gradient 0.6173   0.9526 ** 10 = 0.6153
position 21: gradient 0.3809   0.9526 ** 20 = 0.3786
position 11: gradient 0.2348   0.9526 ** 30 = 0.2330
position  1: gradient 0.1447   0.9526 ** 40 = 0.1434
```


The measured `0.1447` and the theory's `0.1434` agree to two places. The rest is the note drifting from `0.2177` to `0.217` by position 41, and the slope drifting with it. This cell is **designed**: it is not what a trained cell looks like. It teaches the arithmetic.

### 4. The real probe: a 16-number cell

Now the real thing: a cell with 16 numbers in its note, written out as a loop (your own `unroll`, built from Week 8's `loop.py`). Its weights come from a seeded `nn.RNN(4, 16)`, used only as a source of random weights, and they are **untrained**. The **scale** is a knob we turn: `scale = 1` is PyTorch's own starting weights; `2`, `4`, `8` multiply the recurrent weights by that number. Nothing in a model forces a scale; this is an experiment.

Two more new constructs appear here:

- **`torch.stack(list_of_tensors)`** joins a list into one new tensor with a **new first axis**: a pile of sheets. Forty sheets of 16 numbers become one pile of shape `(40, 16)`. It takes **one list**, with square brackets. (`torch.cat`, from Level 3, joins along an axis that already exists; `stack` makes a new one.)
- **`torch.randn(T, 4)`** gives seeded, bell-shaped random numbers in a grid of the shape you name: here `T` inputs of 4 numbers each. `torch.randn(5)` would be five single numbers, which is not the same thing. **Say the shape aloud before you press Enter.**

The "loss" is a toy: add up the 16 numbers of the **last** note. Its gradient at the last position is always length `4.0` (16 ones; `sqrt(16) = 4`), which is a *check*, not a result.

**Block 4**

```python
# probe.py - Week 10: a 16-number cell, built from Week 8's loop, and a probe of its gradients.
def make_cell(scale=1.0, seed=0, D=4, H=16):
    torch.manual_seed(seed)
    rnn = nn.RNN(D, H)                           # used only as a seeded source of random weights
    rnn.weight_hh_l0.data = rnn.weight_hh_l0.data * scale
    return rnn

def unroll(rnn, x):
    W_ih, W_hh = rnn.weight_ih_l0, rnn.weight_hh_l0
    b = rnn.bias_ih_l0 + rnn.bias_hh_l0
    h = torch.zeros(W_hh.shape[0])
    hs = []
    for t in range(len(x)):
        h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
        h.retain_grad()
        hs.append(h)
    return hs

def probe(T, scale=1.0, seed=0):
    rnn = make_cell(scale, seed)
    x = torch.randn(T, 4)                        # T random inputs, 4 features each, seeded by make_cell
    hs = unroll(rnn, x)
    states = torch.stack(hs)                     # one tensor, shape (T, 16)
    states[-1].sum().backward()                  # the "loss": add up the 16 numbers of the LAST note
    grads = torch.stack([h.grad for h in hs])    # shape (T, 16): how much the loss cares about each position
    return [row.norm().item() for row in grads]

x = torch.randn(5, 4)
print("randn(5, 4) shape:", tuple(x.shape), "  stacked states for T = 5:", tuple(torch.stack(unroll(make_cell(), x)).shape))
g = probe(40)
print("T = 40, scale 1: gradient at position 40 =", round(g[39], 4), "(16 ones, length 4)")
for p in [40, 30, 20, 10, 1]:
    print(f"   position {p:2d}: {g[p - 1]:.2e}")
```

```text
randn(5, 4) shape: (5, 4)   stacked states for T = 5: (5, 16)
T = 40, scale 1: gradient at position 40 = 4.0 (16 ones, length 4)
   position 40: 4.00e+00
   position 30: 5.39e-03
   position 20: 1.09e-05
   position 10: 2.24e-08
   position  1: 2.06e-10
```


Read the five lines. Position 40 is `4.0`. Position 30 is five thousandths. Position 1 is `2e-10`. That is ten orders of magnitude lost across forty steps, with no cheating this time. **Vanishing or exploding?**

---

## 🎲 Your Turn

### The Forty-Multiplications Grid

Now vary the length and the scale. On **workbook page 10.4**, the grid has rows for scale `1, 2, 4, 8` and columns for `T = 10, 20, 40, 80`.

**Before you run anything**, put one letter in each of the 16 cells, in your first pen colour:

- **V** (vanishing): below `0.001`
- **L** (level): between `0.001` and `10`
- **E** (exploding): above `10`

Nobody will tell you whether you are right. Then run block 5 and copy each measured number **in full, exponent included** (`9.15e-03` is `0.00915`; a dropped exponent changes the answer by a factor of a hundred or more).

**Block 5**

```python
# grid.py - Week 10: the whole experiment. Gradient at position 1, for four lengths and four recurrent-weight scales.
print("gradient at position 1 (the last position's is always 4.0)")
print("scale |       T=10       T=20       T=40       T=80")
for scale in [1, 2, 4, 8]:
    row = [probe(T, scale)[0] for T in [10, 20, 40, 80]]
    print(f"  x{scale}  |" + "".join(f"  {v:9.2e}" for v in row))
```

```text
gradient at position 1 (the last position's is always 4.0)
scale |       T=10       T=20       T=40       T=80
  x1  |   9.15e-03   1.01e-05   2.06e-10   4.69e-21
  x2  |   5.63e-01   1.66e-02   2.25e-03   2.93e-06
  x4  |   1.08e+01   1.14e+01   2.09e+01   3.36e+03
  x8  |   3.49e+01   2.55e+02   4.38e+03   6.92e+07
```


Colour in which predictions were right. The score is not the point; the **pattern of the misses** is. Some predictions will "miss" only because of our cut-offs, which are ours, not nature's. Read the **trend** down each row and write one sentence per row on page 10.4:

- scale 1: the number falls by orders of magnitude, in every row;
- scale 2: it falls, more slowly;
- scale 4: roughly level up to `T = 40`, then it climbs;
- scale 8: it climbs every time, to `7e+07`.

**No row stays near `4`**, the value at the last position. There is no comfortable middle: that is the point of the week.

### Is it just one seed?

Block 6 repeats `T = 40` for five different seeds, at scale 1 and at scale 8.

**Block 6**

```python
# seeds.py - Week 10: is that one seed's luck? T = 40, five seeds, scale 1 and scale 8.
for scale in [1, 8]:
    vals = [probe(40, scale, seed)[0] for seed in range(5)]
    print(f"scale {scale}: position-1 gradient over seeds 0-4:", [f"{v:.1e}" for v in vals])
```

```text
scale 1: position-1 gradient over seeds 0-4: ['2.1e-10', '8.4e-11', '9.8e-10', '4.7e-09', '1.9e-14']
scale 8: position-1 gradient over seeds 0-4: ['4.4e+03', '8.8e+04', '9.7e+05', '5.5e-07', '1.1e+05']
```


At scale 1, all five are tiny, spread over five orders of magnitude. At scale 8, four are huge and **one has vanished**. So "above scale 1 means exploding" is not a law. Which seed broke the rule? What would you print to find out why?

### Force an explosion

Seeing a huge signal is one thing. What happens if we **act** on one? Block 7 does one update of the knobs (`lr = 0.1`) at scale 1 and at scale 8, with and without `clip_grad_norm_` (you met clipping in Week 6). **Read the column headings before you run it**, and predict: at scale 8, what happens to the size of the weight matrix after one update, with and without clipping?

Words for the columns:

- *grad size* is the length of the recurrent knobs' gradient, before and after clipping;
- *weight size* is the length of the recurrent weight matrix, before and after the update;
- *pinned* means a note whose size is above `0.99`: it is stuck on the flat part of `tanh` (the "capped by `tanh`" of Week 8, in numbers).

**Block 7**

```python
# explode.py - Week 10: one update of the knobs, with and without clipping. T = 40, learning rate 0.1.
def update(scale, clip, lr=0.1, T=40, seed=0):
    rnn = make_cell(scale, seed)
    x = torch.randn(T, 4)
    before = torch.stack(unroll(rnn, x))
    before[-1].sum().backward()
    size = rnn.weight_hh_l0.grad.norm().item()          # the gradient of the recurrent knobs, before any clipping
    if clip:
        nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
    size_after = rnn.weight_hh_l0.grad.norm().item()
    w_before = rnn.weight_hh_l0.norm().item()
    torch.optim.SGD(rnn.parameters(), lr=lr).step()
    w_after = rnn.weight_hh_l0.norm().item()
    after = torch.stack(unroll(rnn, x))
    pinned_before = (before.abs() > 0.99).float().mean().item()
    pinned_after = (after.abs() > 0.99).float().mean().item()
    return size, size_after, w_before, w_after, pinned_before, pinned_after

print("scale  run    | grad size -> after clip | weight size before -> after | notes pinned at +-1 before -> after")
for scale in [1, 8]:
    for clip in [False, True]:
        a, b, c, d, e, f = update(scale, clip)
        label = "clipped" if clip else "plain  "
        print(f"  x{scale}  {label} | {a:9.2e} -> {b:9.2e}      | {c:6.2f} -> {d:9.2f}         | {e:.3f} -> {f:.3f}")
```

```text
scale  run    | grad size -> after clip | weight size before -> after | notes pinned at +-1 before -> after
  x1  plain   |  7.22e+00 ->  7.22e+00      |   2.23 ->      2.40         | 0.000 -> 0.000
  x1  clipped |  7.22e+00 ->  5.14e-01      |   2.23 ->      2.24         | 0.000 -> 0.000
  x8  plain   |  8.55e+04 ->  8.55e+04      |  17.87 ->   8548.25         | 0.484 -> 0.997
  x8  clipped |  8.55e+04 ->  8.78e-01      |  17.87 ->     17.87         | 0.484 -> 0.494
```


Read the two scale-8 rows aloud. The weights went from `17.87` to **`8548.25`**: one update multiplied their size by almost 500. And the notes pinned at plus or minus 1 went from about half to nearly all. With clipping, the weights stayed at `17.87`.

Now the half students miss. Look at the **clipped** row. The weights were not wrecked, but about half the notes were already pinned **before** the update, and still are. Clipping did not make that cell healthy. And at scale 1, the gradient was a healthy `7.22`, which clipping (at `max_norm = 1.0`) shrank to `0.514`: it also throttled a gradient that was fine.

**A seatbelt, not an engine.**

Finally, the question that makes the activity. Our table says the signal from position 1 is `2e-10` at scale 1. Clipping multiplies everything by one number. **Can clipping ever bring that `2e-10` back?** Write "no" and the reason, on page 10.5.

---

## 🔬 Break It On Purpose

Two blocks, both **DELIBERATE**. Predict what each will do before you run it.

**1. `torch.stack` with two arguments.** Run this in a scratch file:

```python
# DELIBERATE: torch.stack wants ONE list of tensors, not the tensors one after another.
import torch
a = torch.tensor([1.0, 2.0])
b = torch.tensor([3.0, 4.0])
both = torch.stack(a, b)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 5, in <module>
    both = torch.stack(a, b)
TypeError: stack(): argument 'tensors' (position 1) must be tuple of Tensors, not Tensor
```

Read the last line, slowly. What did `stack` want in position 1, and what did it get? Fix the file, and write the fix in your Bug Log.

**2. Clipping at the wrong moment (no error at all).** Add this **below** block 4 in a scratch copy of `week10.py` (it needs `make_cell` and `unroll`):

```python
# DELIBERATE (SILENT): clip_grad_norm_ called BEFORE backward(). No error.
rnn = make_cell(8.0)
x = torch.randn(40, 4)
states = torch.stack(unroll(rnn, x))
size = nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
print("clip_grad_norm_ returned:", size.item())
states[-1].sum().backward()
print("recurrent gradient size after the 'clip':", f"{rnn.weight_hh_l0.grad.norm().item():.3e}")
```

```text
clip_grad_norm_ returned: 0.0
recurrent gradient size after the 'clip': 8.548e+04
```

Nothing crashed. So was the gradient clipped? Compare the two printed numbers with what block 7 told you about this cell. What order should the three lines `backward()`, `clip_grad_norm_`, `step()` run in, and what should the first printed number have been?

---

## 🔑 Wrap Up

1. Say from memory, in your own words: (1) what compounding is, (2) why a loop makes it matter, (3) what clipping does and does not do.
2. "It's only 5% per step, so it only loses 5%." What is wrong with that, and what did you press to see it?
3. The signal from position 1 was `2e-10` at scale 1. Does that mean a *trained* recurrent net cannot remember the first word? (Think about what you measured: an untrained cell, random inputs, one toy score. Write what you can claim and what you cannot.)

**What we did not do.** We measured a random cell at the *start*. We did not train it. We did not show that a trained cell cannot remember. And none of this is a result about language models. Next week is the first answer, **gates**: a memory that *adds* instead of multiplies, and we measure the same table again. Week 12 trains one properly.

Then write this sentence in your Bug Log in your own handwriting:

> **"Forty small multiplications are not a small change, and clipping is a seatbelt, not an engine."**

---

## 📤 Homework

Complete workbook pages 10.1 to 10.7 in order, and **write predictions before running anything**. Every number in your write-up must have been printed by your own run in the last 24 hours (or your own calculator), with the seed stated.

**Optional.** Scale 3 lies between 2 and 4. Run `probe(T, 3.0)` for several `T` in `week10.py`. Does the gradient at position 1 level off, or wander? Write what you saw before you explain it.

---

## 📖 What carries into next week

Next week asks: can a note **add** instead of multiply? Bring the grid from page 10.4. You will measure it again.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **compounding** | multiplying a number by itself `T` times; `r ** T` |
| **position** | a place in a sequence; position 1 is the first |
| **backpropagation through time** | sending the error backwards through the unrolled loop, one slope per step |
| **exploding gradient** | the opposite of vanishing: slopes above 1 multiply to a huge number |
| **vanishing gradient** | (from Week 6) slopes below 1 multiply to almost nothing |
| **clipping** | (from Week 6) rescaling a gradient that is too big; it cannot bring back one that has vanished |
| **pinned** | a note stuck near plus or minus 1, on the flat part of `tanh` |

---

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Workbook](../workbook/week-10.md)
