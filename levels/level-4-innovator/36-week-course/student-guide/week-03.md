# Week 3 — Adam: Every Knob Gets Its Own Step Size

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Next ➡ Week 4](week-04.md) · [Workbook](../workbook/week-03.md)

---

> ### This week in one sentence
> **Divide each knob's step by the typical size of that knob's own gradient, and every knob moves about `lr` per step, whatever the scale of its gradient.**
>
> **By the end of this chapter you will be able to:**
> - **Compute a root-mean-square by hand** on `[3, -4]` and on `[300, -400]`, and say what it measures
> - **Fill a three-optimizer table** (SGD, momentum, Adam) for four steps on paper, then match all three against `torch.optim`
> - **Show that Adam's first step is `lr`** for a gradient of 1 and for a gradient of 1000
> - **Say what AdamW changes** about weight decay
> - **Say the "divide" sentence** about what Adam divides by, and why
>
> **New maths:** **one idea: root-mean-square.** *Square every number, average the squares, take the square root.* You meet it on `[3, -4]` on paper before any code. It comes with one tiny number, **epsilon**.
>
> **New syntax:** `torch.optim.Adam` · `torch.optim.AdamW` · `weight_decay=` · `torch.sqrt`
>
> **Reading time:** about 35 minutes. **Homework:** about 60-75 minutes.

> **📌 About the code blocks.** Each block carries on from the one above it, so each `import` is typed once, in the first block that needs it. If you paste a block on its own and get `NameError`, that is why; nothing is broken. Blocks marked **DELIBERATE MISTAKE** are broken (or quietly wrong) on purpose. Every output shown was printed by a real run on a CPU with a seed set, using one thread. The small by-hand blocks match to every digit shown. The spirals runs should match within 0.005 on a loss and 0.5 points on an accuracy. Open your terminal in the `36-week-course/` folder (the one that contains `l4lib/`) and keep everything in one file, `week03.py`. Keep `week02.py` too.

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 3 is highlighted with a pointer above it, weeks 1 and 2 are outlined solid, and every later tile has a dashed outline](../figures/fig-w03-0-where-this-fits.svg)
*Figure 3.0 — Where this fits: week 3 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## 🪝 Start Here

This section shows two surprising results that the rest of the chapter explains.

Last week you turned the `optimizer` knob from `"sgd"` to `"momentum"`. Today there is a third word for the same knob.

Same data. Same starting weights. Same learning rate, `0.003`. Two runs. Only one word differs.

**Before you look at the next block, write one number in your Bug Log: your guess for the final training loss of the second run.** Remember what a coin scores.

Here are the two runs (you will type this code later; for now just read the output):

```text
sgd lr=0.003                 train 0.693  val 0.694  acc  46.9%
adam lr=0.003                train 0.007  val 0.037  acc  98.9%
```

The first is a coin. The second is 98.9% correct. **One word changed:** `optimizer="sgd"` became `optimizer="adam"`.

Now a second surprise. Here is the new rule at `0.03`, which was last week's winner for momentum:

```text
adam lr=0.03                 train 0.658  val 0.684  acc  46.9%
```

A coin again. So the new rule has a learning rate that **means something different**.

**What does `"adam"` do to the size of the step?** Write your guess in the Bug Log. Any guess is fair (faster, remembers, smarter, bigger step). By the end of this chapter you will have built the answer yourself, on paper, with two numbers first, and then watched PyTorch agree with your paper.

---

## 🧠 The Big Idea

This section explains what Adam divides by, and introduces the one new maths idea you need to see why.

### 1. Week 2 fixed the direction. Today fixes the size.

Momentum gave the step a memory of its *direction*. It did not touch the step's *size*. The size is still:

```text
lr x (something proportional to the gradient)
```

So a knob whose gradient is 1000 times bigger moves 1000 times further. Two things follow:

- **One learning rate has to suit every knob at once,** even though different knobs get very different gradients.
- **The right learning rate depends on the scale of the gradient,** which depends on the loss, the width and the depth. That is why Week 1's winning rates and Week 2's winning rates were different numbers.

**Adam** is *the rule where each knob's step is divided by the typical size of that knob's own recent gradients.* Divide by the typical size, and the scale cancels out. That is the whole week. To do it you need a way to measure a "typical size".

### 2. The one new maths idea: root-mean-square

The **root-mean-square (RMS)** of a list is *the typical size of its numbers, ignoring sign.* Three steps, in this order (the order is the name read backwards):

```text
1. square every number            (so the signs vanish: -4 becomes 16)
2. take the mean of the squares
3. take the square root of that   (so we are back in the original units)
```

**Do this on paper first, with a calculator.** Two gradients from two knobs: `3` and `-4`.

```text
1. square each number          3 -> 9      -4 -> 16
2. average the squares         (9 + 16) / 2 = 12.5
3. take the square root        sqrt(12.5) = 3.5355
```

Check 3.5355 on your calculator. Then answer two questions in your Bug Log:

- *Why square first?* (What does `-4` become?)
- *Is 3.5355 a sensible "typical size" for a 3 and a 4?*

Now the key move. **The knobs got bigger: `300` and `-400`.** Work out the RMS of that list on paper. Then divide each number by its own RMS: `300 / RMS` and `-400 / RMS`. Compare with `3 / 3.5355` and `-4 / 3.5355`.

Now the same thing in code. This first block of your file imports `torch`, fixes the thread count and prints the versions:

```python
import torch
torch.set_num_threads(1)
print("threads:", torch.get_num_threads(), " torch", torch.__version__)
```
```text
threads: 1  torch 2.2.1
```

If your torch version prints differently, the by-hand numbers below will still match.

Before you run the next block, write down what you expect the `plain mean` line to say. The block does RMS on the same list one step at a time (`.mean()` averages a tensor, `.item()` turns a one-number tensor into a plain number):

```python
g = torch.tensor([3.0, -4.0])
print("plain mean      :", g.mean().item())
print("squares         :", (g ** 2).tolist())
print("mean of squares :", (g ** 2).mean().item())
print("root of that    :", round(torch.sqrt((g ** 2).mean()).item(), 4))
```
```text
plain mean      : -0.5
squares         : [9.0, 16.0]
mean of squares : 12.5
root of that    : 3.5355
```

Look at each line and notice three things:

- **The plain mean is `-0.5`.** A list with a 3 and a -4 in it has, by the plain mean, a "typical size" of nearly nothing: the signs cancelled. That is why we square first.
- **`3.5355` sits between 3 and 4,** where a typical size for a 3 and a 4 should sit. It is a little closer to the bigger one, because squaring makes big numbers count for more.
- **You have met a cousin before.** Week 2's `.norm()` of `[6, 8]` was `sqrt(36 + 64) = 10`. RMS does the same squares and the same square root but **divides by how many numbers** first.

Now the same list, a hundred and a thousand times bigger. The loop divides each list by its own RMS:

```python
for scale in [1, 100, 1000]:
    g = torch.tensor([3.0, -4.0]) * scale
    rms = torch.sqrt((g ** 2).mean())
    print(f"list {g.tolist()}  rms {rms.item():.4f}  list / rms {[round(x, 4) for x in (g / rms).tolist()]}")
```
```text
list [3.0, -4.0]  rms 3.5355  list / rms [0.8485, -1.1314]
list [300.0, -400.0]  rms 353.5534  list / rms [0.8485, -1.1314]
list [3000.0, -4000.0]  rms 3535.5339  list / rms [0.8485, -1.1314]
```

The RMS grows exactly as the list grows (3.5355, 353.5534, 3535.5339). **The list divided by its RMS does not change at all:** `0.8485, -1.1314`, three times. That last column is the week's whole trick: *divide by the typical size and the scale disappears.* Compare with what you got on paper for `300` and `-400`.

![Three rows, each a pair of gradients, an arrow to its typical size, and an arrow to the same result 0.8485 and minus 1.1314, whatever the scale of the pair](../figures/fig-w03-1-divide-by-typical-size.svg)
*Figure 3.1 — Dividing by the typical size cancels the scale, so a thousand-times-bigger knob looks the same.*

**Standard deviation?** If you remember it from Level 3, it is a close cousin. Standard deviation measures the spread around the average. RMS measures the size around zero. We only use RMS this week.

**Epsilon.** What if every number in the list is zero? Then the RMS is 0, and dividing by 0 gives something that is not a number. The fix is to add a tiny number to the thing you divide by. It is called **epsilon**, written `eps`. In Adam it is `0.00000001`, which you can also write `1e-8`. It is there so you never divide by zero, and it should be too small to change any normal answer. You will see exactly where it stops being too small, at the end of Step 5.

### 3. From the RMS to Adam

Adam keeps **two running averages per knob**. Both are exponential moving averages, which you know from Week 2. In the formulas, `g` is the gradient, `m` and `s` are the averages, and `x` means multiply:

```text
m = 0.9   x old m + 0.1   x g        the average of the gradient          (direction: Week 2)
s = 0.999 x old s + 0.001 x g*g      the average of the gradient SQUARED  (size)
```

`m` is Week 2 exactly. `s` is the same trick on the *squares*: that is the first two steps of RMS. With `0.999` instead of `0.9` its memory is much longer. Then the step:

```text
step = lr x m / (sqrt(s) + eps)
```

`sqrt(s)` is the third step of RMS. So **Adam's step is `lr` times the average gradient, divided by the running RMS of the gradient.** A knob whose gradients are huge has a huge `sqrt(s)`, which cancels its huge `m`. A knob whose gradients are tiny has a tiny `sqrt(s)`, which also cancels. Either way, when the gradient is steady, the ratio is about 1 and the step is about `lr` (smaller when the gradient is noisy and the average washes out).

**The snag you already met.** Last week the average of ten, ten, ten, ten, ten started at 1.0 instead of 10, because it started at zero. Adam has the same snag twice. The fix is to divide by **how much has arrived**: after `t` steps that share is `1 - 0.9^t`. Try it on last week's numbers. The loop keeps the start-at-zero average and divides it by the arrived share:

```python
avg = 0.0
for t in range(1, 6):
    avg = 0.9 * avg + 0.1 * 10
    arrived = 1 - 0.9 ** t
    print(f"step {t}: average {avg:.4f}   arrived {arrived:.4f}   average / arrived {avg / arrived:.4f}")
```
```text
step 1: average 1.0000   arrived 0.1000   average / arrived 10.0000
step 2: average 1.9000   arrived 0.1900   average / arrived 10.0000
step 3: average 2.7100   arrived 0.2710   average / arrived 10.0000
step 4: average 3.4390   arrived 0.3439   average / arrived 10.0000
step 5: average 4.0951   arrived 0.4095   average / arrived 10.0000
```

The droop is gone: the last column reads ten every time. The name for this fix is **bias correction**. You only need the name once. After this we call it "divide by what has arrived". For `m` the arrived share is `1 - 0.9^t`; for `s` it is `1 - 0.999^t`.

**Do the first step on paper.** Function `f(w) = w * w` starting at `w = 1.0`, learning rate `0.1`. The gradient is `2w = 2.0`. After the fix, `m` is `2.0` and `s` is `4.0`, so `sqrt(s)` is `2.0`. The ratio is `1.0`. The step is `0.1 x 1.0 = 0.1`, so `w` lands on `0.9`. Now: **if the gradient had been 2000, what would the step have been?** Write your answer before reading on.

### 4. AdamW and the quiet bug

**Weight decay** is *shrinking every weight a little on every step*, to discourage the model from leaning on any one large weight. In code it is one keyword, `weight_decay=`. (Whether decay is worth using is Week 5's question. Today it is a keyword and a bug.)

With plain SGD the rule is simple: each step, every weight also loses `lr x weight_decay x weight`, so big weights lose more in absolute terms and every weight loses the same *share*.

**Adam** does its decay the old way: it adds the decay to the gradient, and then the whole thing goes through the division by the RMS. **AdamW** applies the decay to the weight directly, outside the division. You will see what that does to two weights in Step 6.

### 5. The four new constructs

Each construct is named below with what it takes and what it does.

**`torch.optim.Adam(params, lr=...)`** has the same shape as `SGD` from Week 2: a list of things to adjust, and a learning rate. It keeps two numbers per weight, your `m` and `s`. The two shares (`0.9` and `0.999`) and `eps=1e-8` are built-in defaults. **There are dials for them, and we leave them alone.**

**`torch.optim.AdamW(params, lr=..., weight_decay=...)`** is Adam with the decay done outside the division. The arguments are the same. Note that the default `weight_decay` on `AdamW` is `0.01`, not zero.

**`weight_decay=`** is the strength of the shrinking. It exists on `SGD`, `Adam` and `AdamW` with the same name.

**`torch.sqrt(x)`** is the square root of every element of a **tensor**. It needs a tensor, not a bare number.

---

## 💻 Try It Yourself

### Step 1 — the by-hand table

Here is Adam by hand, four steps on `f(w) = w * w` from `w = 1.0` with `lr = 0.1`. Type it in two halves: the three lines that update `g`, `m` and `s`, then the three that fix and step. (The square root is `** 0.5` here because this is your own hand arithmetic on plain numbers; `torch.sqrt` is for tensors.)

```python
w, m, s, lr, eps = 1.0, 0.0, 0.0, 0.1, 1e-8
print("step      g         m          s      m/arrived  s/arrived  rms-root    step      w")
for t in range(1, 5):
    g = 2 * w
    m = 0.9 * m + 0.1 * g
    s = 0.999 * s + 0.001 * g * g
    m_fix = m / (1 - 0.9 ** t)
    s_fix = s / (1 - 0.999 ** t)
    root = s_fix ** 0.5
    step = lr * m_fix / (root + eps)
    w = w - step
    print(f"{t:>4} {g:>8.4f} {m:>10.6f} {s:>10.7f} {m_fix:>10.4f} {s_fix:>10.4f} {root:>9.4f} {step:>9.5f} {w:>8.4f}")
```
```text
step      g         m          s      m/arrived  s/arrived  rms-root    step      w
   1   2.0000   0.200000  0.0040000     2.0000     4.0000    2.0000   0.10000   0.9000
   2   1.8000   0.360000  0.0072360     1.8947     3.6198    1.9026   0.09959   0.8004
   3   1.6008   0.484082  0.0097914     1.7863     3.2671    1.8075   0.09883   0.7016
   4   1.4032   0.575991  0.0117505     1.6749     2.9420    1.7152   0.09765   0.6039
```

Look at row 1 and walk it with your finger: `m = 0.2`, `s = 0.004`; divide by the arrived shares (0.1 and 0.001) to get 2.0 and 4.0; the root of 4.0 is 2.0; the ratio is 1.0; the step is `0.10000`; `w` is `0.9000`. Then **find the row where the step is smaller than `lr`.** Why do you think it is smaller there? Compare the gradient `g` with the `rms-root` in that row.

Now put Adam next to the two columns you have from Week 2. This block runs SGD, momentum and Adam side by side on the same function:

```python
w_sgd = 1.0
w_mom, v = 1.0, 0.0
print("step |    SGD   | momentum |   Adam")
w_adam, m, s = 1.0, 0.0, 0.0
for t in range(1, 5):
    w_sgd = w_sgd - 0.1 * (2 * w_sgd)
    v = 0.9 * v + 2 * w_mom
    w_mom = w_mom - 0.1 * v
    g = 2 * w_adam
    m = 0.9 * m + 0.1 * g
    s = 0.999 * s + 0.001 * g * g
    w_adam = w_adam - 0.1 * (m / (1 - 0.9 ** t)) / ((s / (1 - 0.999 ** t)) ** 0.5 + 1e-8)
    print(f"{t:>4} | {w_sgd:>8.4f} | {w_mom:>8.4f} | {w_adam:>8.4f}")
```
```text
step |    SGD   | momentum |   Adam
   1 |   0.8000 |   0.8000 |   0.9000
   2 |   0.6400 |   0.4600 |   0.8004
   3 |   0.5120 |   0.0620 |   0.7016
   4 |   0.4096 |  -0.3086 |   0.6039
```

**Read this table honestly: on this toy, Adam is the slowest** (0.6039 after four steps, against SGD's 0.4096). Its step is a fixed 0.1 from the start, and the gradient here is a gentle one. Look instead at how the step *sizes* behave: SGD's shrink (0.200, 0.160, 0.128, 0.102), momentum's swing (0.200, 0.340, 0.398, 0.371), Adam's stay put (0.1000, 0.0996, 0.0988, 0.0977). This toy has *one* knob. Adam is for when there are thousands and their gradients differ. Steps 5 and 6 show that.

### Step 2 — the same thing in PyTorch

Three optimizers, one small helper. The helper wraps the lines you already know (clear, backward, step, record) so you do not write them three times.

```python
def trace(w, opt, steps=4):
    out = []
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        (w * w).sum().backward()
        opt.step()
        out.append(round(w.item(), 4))
    return out

w = torch.tensor([1.0], requires_grad=True)
print("SGD     ", trace(w, torch.optim.SGD([w], lr=0.1)))
w = torch.tensor([1.0], requires_grad=True)
print("momentum", trace(w, torch.optim.SGD([w], lr=0.1, momentum=0.9)))
w = torch.tensor([1.0], requires_grad=True)
print("Adam    ", trace(w, torch.optim.Adam([w], lr=0.1)))
```
```text
SGD      [0.8, 0.64, 0.512, 0.4096]
momentum [0.8, 0.46, 0.062, -0.3086]
Adam     [0.9, 0.8004, 0.7016, 0.6039]
```

Look at each line and compare it with its column of the table above. They match to four decimals. You did them on paper; PyTorch agrees.

### Step 3 — what Adam keeps inside

Adam creates its two averages the first time it steps, so this block runs three steps and then prints what Adam stored:

```python
w = torch.tensor([1.0], requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
trace(w, opt, steps=3)
print("after 3 steps, Adam's memory for w:")
print("  exp_avg    (my m):", round(opt.state[w]["exp_avg"].item(), 5))
print("  exp_avg_sq (my s):", round(opt.state[w]["exp_avg_sq"].item(), 7))
print("  step count       :", int(opt.state[w]["step"].item()))
```
```text
after 3 steps, Adam's memory for w:
  exp_avg    (my m): 0.48408
  exp_avg_sq (my s): 0.0097914
  step count       : 3
```

PyTorch calls them `exp_avg` and `exp_avg_sq`. **Find row 3 of your Step 1 output:** `m` is `0.484082` and `s` is `0.0097914`. They are your numbers. `opt.state[w]` is a dictionary keyed by the weight, like the `"momentum_buffer"` you looked at last week. (`int(... .item())` is only there because the step count is stored as a float and would otherwise print `3.0`.)

### Step 4 — the scale test

Two knobs. Knob one has gradient 1. Knob two has gradient 1000. Learning rate `0.1`.

**Before you run this, write four numbers:** how far does each knob move on the first step under SGD, and under Adam?

```python
for name in ["SGD ", "Adam"]:
    w = torch.tensor([0.0, 0.0], requires_grad=True)
    if name == "SGD ":
        opt = torch.optim.SGD([w], lr=0.1)
    else:
        opt = torch.optim.Adam([w], lr=0.1)
    loss = (torch.tensor([1.0, 1000.0]) * w).sum()
    loss.backward()
    opt.step()
    print(name, "gradients", w.grad.tolist(), "   first step moved", [round(-x, 4) for x in w.tolist()])
```
```text
SGD  gradients [1.0, 1000.0]    first step moved [0.1, 100.0]
Adam gradients [1.0, 1000.0]    first step moved [0.1, 0.1]
```

Look at the last two numbers on the Adam line. **The knob with the thousand-times-bigger gradient moves the same distance.** That is Adam.

![Horizontal bars on a log axis of how far two knobs move on the first step: SGD moves 0.1 and 100.0, Adam moves 0.1 and 0.1](../figures/fig-w03-2-scale-test-sgd-vs-adam.svg)
*Figure 3.2 — Adam divides each knob's step by its own gradient size, so both knobs move the same distance.*

### Step 5 — epsilon, where it starts to matter

What if a gradient is tiny? This block prints Adam's first step for smaller and smaller gradients:

```python
print("   gradient     first step (lr = 0.1)")
for c in [1000.0, 1.0, 0.001, 1e-6, 1e-8, 1e-9]:
    w = torch.tensor([0.0], requires_grad=True)
    opt = torch.optim.Adam([w], lr=0.1)
    (c * w).sum().backward()
    opt.step()
    print(f"{c:>12g}     {-w.item():.6f}")
```
```text
   gradient     first step (lr = 0.1)
        1000     0.100000
           1     0.100000
       0.001     0.099999
       1e-06     0.099010
       1e-08     0.050000
       1e-09     0.009091
```

For every gradient down to `0.001`, the first step is `lr` to five decimals. It only stops being `lr` when the gradient is as small as epsilon itself. Read the `1e-08` row: the step is **half** of `lr`. Why half? The gradient and epsilon are equal, so the division is `g / (g + g)`. That is what epsilon is for, and what it costs. Whether real runs ever have gradients that small was **not measured** in this course, so do not guess.

### Step 6 — weight decay, and the bug

First, what decay should look like. Here the loss does not depend on `w` at all (`w * 0`), so the gradient is zero and only the decay acts:

```python
for name in ["no decay", "weight_decay=0.1"]:
    w = torch.tensor([1.0, 100.0], requires_grad=True)
    if name == "no decay":
        opt = torch.optim.SGD([w], lr=0.1)
    else:
        opt = torch.optim.SGD([w], lr=0.1, weight_decay=0.1)
    for _ in range(10):
        opt.zero_grad(set_to_none=True)
        (w * 0).sum().backward()
        opt.step()
    print(f"{name:<18} after 10 steps:", [round(x, 4) for x in w.tolist()])
```
```text
no decay           after 10 steps: [1.0, 100.0]
weight_decay=0.1   after 10 steps: [0.9044, 90.4382]
```

Both weights lose the same **share** per step (`1 - 0.1 x 0.1 = 0.99`, ten times, leaves 0.9044 of each). The 100 lost more in absolute terms than the 1. That is what decay should do.

Now the same setup with `Adam` and `AdamW`: same keyword, same number. **Read the first weight before you read anything else.**

```python
for name in ["Adam ", "AdamW"]:
    w = torch.tensor([1.0, 100.0], requires_grad=True)
    if name == "Adam ":
        opt = torch.optim.Adam([w], lr=0.1, weight_decay=0.1)
    else:
        opt = torch.optim.AdamW([w], lr=0.1, weight_decay=0.1)
    for _ in range(10):
        opt.zero_grad(set_to_none=True)
        (w * 0).sum().backward()
        opt.step()
    print(f"{name} weight_decay=0.1  after 10 steps:", [round(x, 4) for x in w.tolist()])
```
```text
Adam  weight_decay=0.1  after 10 steps: [0.0762, 99.0003]
AdamW weight_decay=0.1  after 10 steps: [0.9044, 90.4382]
```

Compare the two lines. Under **Adam** the small weight is nearly destroyed (1.0 to 0.0762) and the big one barely moves (100 to 99.0003). Every weight is pushed by about `lr` per step: the division by the RMS has turned "decay in proportion to the weight" into "decay by a fixed amount". Under **AdamW** the two weights lose the same *share* (0.9044 and 90.4382, exactly the SGD numbers). That is the whole difference, and the only reason AdamW exists.

**This is the cleanest version of the mechanism, on two weights with no loss at all. It is not a measurement of a real network's weights.**

### Step 7 — the spirals

The Week 1 harness takes `optimizer="sgd"`, `"momentum"`, `"adam"` or `"adamw"`. Same data, same seed, same starting weights. Only the rule and the rate change. The harness is imported, never copied. This block runs all four rules at the same small rate:

```python
from l4lib.spirals import run
for opt_name in ["sgd", "momentum", "adam", "adamw"]:
    run(f"{opt_name} lr=0.003", lr=0.003, optimizer=opt_name)
```
```text
sgd lr=0.003                 train 0.693  val 0.694  acc  46.9%
momentum lr=0.003            train 0.690  val 0.690  acc  56.7%
adam lr=0.003                train 0.007  val 0.037  acc  98.9%
adamw lr=0.003               train 0.007  val 0.037  acc  98.9%
```

```python
for opt_name in ["sgd", "momentum", "adam", "adamw"]:
    run(f"{opt_name} lr=0.03", lr=0.03, optimizer=opt_name)
```
```text
sgd lr=0.03                  train 0.690  val 0.690  acc  52.8%
momentum lr=0.03             train 0.018  val 0.034  acc  98.6%
adam lr=0.03                 train 0.658  val 0.684  acc  46.9%
adamw lr=0.03                train 0.658  val 0.684  acc  46.9%
```

Here are the two runs in a table (final train loss / validation accuracy):

| `lr` | SGD | Momentum | Adam |
|:--:|:--:|:--:|:--:|
| 0.003 | 0.693 / 46.9% | 0.690 / 56.7% | **0.007 / 98.9%** |
| 0.03 | 0.690 / 52.8% | **0.018 / 98.6%** | 0.658 / 46.9% |

Each rule has its own good learning rate. This block runs each rule at its own:

```python
for opt_name, lr in [("sgd", 0.3), ("momentum", 0.03), ("adam", 0.003), ("adamw", 0.003)]:
    run(f"{opt_name} lr={lr}", lr=lr, optimizer=opt_name)
```
```text
sgd lr=0.3                   train 0.016  val 0.041  acc  98.9%
momentum lr=0.03             train 0.018  val 0.034  acc  98.6%
adam lr=0.003                train 0.007  val 0.037  acc  98.9%
adamw lr=0.003               train 0.007  val 0.037  acc  98.9%
```

**All three end in about the same place.** The good rates are a factor of 10 apart, and 100 from end to end (0.3, 0.03, 0.003). Adam has the lowest train loss, but the validation losses are 0.041, 0.034 and 0.037. Read them before you decide which rule is best, and remember this is one seed.

What Adam buys shows up in a sweep of rates. This block runs Adam at seven learning rates:

```python
for lr in [0.0001, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3]:
    run(f"adam lr={lr}", lr=lr, optimizer="adam")
```
```text
adam lr=0.0001               train 0.077  val 0.063  acc  98.1%
adam lr=0.001                train 0.018  val 0.026  acc  99.4%
adam lr=0.003                train 0.007  val 0.037  acc  98.9%
adam lr=0.01                 train 0.013  val 0.059  acc  99.2%
adam lr=0.03                 train 0.658  val 0.684  acc  46.9%
adam lr=0.1                  train 0.693  val 0.702  acc  46.9%
adam lr=0.3                  train 0.701  val 0.723  acc  46.9%
```

Four rates in a row, from `0.0001` to `0.01` (a factor of 100), all give 98.1% or better. Last week SGD had one good rate out of the six you tried. But Adam still has a learning rate that must be chosen: `0.03` and above fail. It has a *wider* good range and *a different one*. One seed, one dataset: Week 7's three seeds are where we ask whether a gap is real.

Finally, weight decay on the spirals, with the two rules side by side. Compare each `adam` line with the `adamw` line under it:

```python
run("adam  wd=0", lr=0.003, optimizer="adam")
run("adamw wd=0", lr=0.003, optimizer="adamw")
run("adam  wd=0.1", lr=0.003, optimizer="adam", weight_decay=0.1)
run("adamw wd=0.1", lr=0.003, optimizer="adamw", weight_decay=0.1)
run("adam  wd=0.01", lr=0.003, optimizer="adam", weight_decay=0.01)
run("adamw wd=0.01", lr=0.003, optimizer="adamw", weight_decay=0.01)
```
```text
adam  wd=0                   train 0.007  val 0.037  acc  98.9%
adamw wd=0                   train 0.007  val 0.037  acc  98.9%
adam  wd=0.1                 train 0.693  val 0.694  acc  46.9%
adamw wd=0.1                 train 0.011  val 0.077  acc  98.9%
adam  wd=0.01                train 0.693  val 0.695  acc  46.9%
adamw wd=0.01                train 0.009  val 0.051  acc  98.9%
```

With no decay the two rules give the **identical** line: it is the same optimizer until decay is switched on. With any decay, `Adam` finishes at a coin and `AdamW` finishes near its no-decay number. The habit to take away: *if you want weight decay with an adaptive optimizer, use `AdamW`.* Also notice that `adamw wd=0.1` has a *worse* validation loss than `wd=0` (0.077 against 0.037), so decay is not free. Whether it helps a model is Week 5's question.

### Step 8 — two deliberate mistakes

Save each of these as its own file and run it. Both are broken on purpose. Read the output, then write the last line in your Bug Log.

The first is a missing step in the RMS recipe:

```python
# DELIBERATE MISTAKE 1: forgetting to square before averaging
import torch
g = torch.tensor([3.0, -4.0])
print("mean          :", g.mean().item())
print("sqrt of mean  :", torch.sqrt(g.mean()).item())
print("what it should be:", torch.sqrt((g ** 2).mean()).item())
```
```text
mean          : -0.5
sqrt of mean  : nan
what it should be: 3.535533905029297
```

Nothing crashed. `nan` means "not a number". Compare the recipe in section 2 with the code: which of the three RMS steps is missing, and what does the square root do to a negative number?

The second also runs without any error, and that is the problem. It does one Adam step by hand and one in PyTorch:

```python
# DELIBERATE MISTAKE 2: Adam by hand, step 1, compared with torch
import torch
torch.set_num_threads(1)
w_hand, m, s = 1.0, 0.0, 0.0
w = torch.tensor([1.0], requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
(w * w).sum().backward()
opt.step()
g = 2 * w_hand
m = 0.9 * m + 0.1 * g
s = 0.999 * s + 0.001 * g * g
w_hand = w_hand - 0.1 * m / (s ** 0.5 + 1e-8)
print("my hand step 1 :", round(w_hand, 4))
print("torch step 1   :", round(w.item(), 4))
```
```text
my hand step 1 : 0.6838
torch step 1   : 0.9
```

The two numbers should agree and do not. Your hand result for step 1 in Step 1 was `0.9000`. Find the lines that this loop is missing compared with the Step 1 table. (When a hand calculation and PyTorch disagree, suspect your hand number first.)

---

## 🎲 Your Turn — fill the table

This section is the paper task that checks you can produce Adam's numbers yourself. Use the blank three-optimizer table on workbook page 3.1 (four rows, three columns). Do these in order.

1. **Fill the Adam column for four steps on paper** (`f(w) = w * w`, `w = 1.0`, `lr = 0.1`). Copy the SGD and momentum columns from last week. Use the Step 1 column headings as a guide and a calculator. Accept a match within 0.0001.
2. **Run `torch.optim.Adam` on it** (Step 2) and tick each cell that matches.
3. **Show that Adam's first step is `lr` for a gradient of 1 and for a gradient of 1000,** with code (Step 4, or your own version). Then write one sentence saying why.
4. **Place two new cards** beside your A-F cards and the two from Week 2: where do "adam lr=0.003" and "adam lr=0.03" go? Where exactly a coin sits among the A-F shapes was not plotted this week, so if you are not sure, say so.

---

## 🔑 Wrap Up

These are the sentences to keep from this chapter. Say this sentence aloud, then write it in your Bug Log in your own handwriting:

> **"Adam divides each knob's step by the typical size of that knob's own gradient, so every knob moves about `lr` per step, whatever its gradient's scale."**

Then add this underneath:

> **"That makes the learning rate mean the same thing for every knob, but on a different scale from SGD's: 0.003 for Adam where SGD needed 0.3. And when you want weight decay with Adam, use AdamW, because Adam's version gets divided away."**

And one short line: *"RMS: square, mean, root. Adam's first step is `lr` for any gradient. AdamW for decay."*

---

## 📝 Vocabulary

Every new word from this chapter, in one place.

| Word | Meaning |
|---|---|
| **root-mean-square (RMS)** | Square every number, average the squares, take the root: the typical size of a list, ignoring sign |
| **epsilon** (`eps`) | A tiny number added to what you divide by so you never divide by zero; `1e-8` in Adam |
| **per-knob step size** | Each weight's step is scaled by its own gradient's typical size, not by one shared rule |
| **Adam** | Momentum's average of the gradient, divided by the running RMS of the gradient |
| **bias correction** | Dividing a start-at-zero average by how much of it has arrived; "divide by what has arrived" |
| **weight decay** | Shrinking every weight a little each step |
| **AdamW** | Adam with weight decay applied to the weight directly, outside the division |

---

## 🏠 Homework

Workbook Week 3 (about 60-75 minutes). Everything you write down must come from **your own run, printed on your own screen, with a seed set, in the last 24 hours**, not from this chapter.

1. **The three-optimizer table.** Four steps each of SGD, momentum and Adam on `f(w) = w * w`, `w = 1.0`, `lr = 0.1`. Then check against `torch.optim`.
2. **The first step.** Gradient 1 and gradient 1000, SGD and Adam. Four numbers, one sentence.
3. **RMS on your own list.** Pick three numbers that are not 3 and -4. Work out the RMS by hand, then in code. Then multiply the list by 100 and show that list / RMS has not changed.
4. **Adam's rate.** Run Adam at four rates of your choice and write "good" or "coin" against each, from your own screen.
5. **Break it on purpose.** Pick one of the two mistakes from Step 8. Reproduce it, paste the last line into your Bug Log, then fix it.
6. **AdamW.** Run Adam and AdamW with `weight_decay=0.1` on the two-weight test from Step 6 and say in one sentence which weight each one hurt.
7. **Self-check.** In one sentence: what does Adam divide by, and why does that make every knob move about the same distance?

**The one line to write in your Bug Log tonight:** *"Adam = Week 2's average, divided by the running RMS of the gradient; first step is lr; its lr is on a smaller scale than SGD's; decay goes with AdamW."*

---

## 🔮 Next Week

This section says what comes next and what to keep. Adam fixed the **size** problem per knob. It did not ask whether the step should be `lr` for the *whole run*. Next week: the right step size changes during a run (start small, then shrink), and the batch you average over changes both the noise in the gradient and how many steps you get. There is no new maths idea. The new syntax is a function written in one line.

**Before then:** keep `week03.py` exactly as it is. Next week re-runs its Adam line. Keep your cards.

---

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Next ➡ Week 4](week-04.md) · [Workbook](../workbook/week-03.md)
