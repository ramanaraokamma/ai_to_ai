# Week 15 — Scale, Mask, and Many Heads

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Workbook](../workbook/week-15.md)

---

> ### This week in one sentence
> **Last week's attention works on three tiny words. Today we make three repairs so it can work on real sentences: a divide, so big scores do not freeze the softmax; a mask, so a word cannot read the word it is about to predict; and heads, so one word can share its attention in more than one way.**
>
> **By the end of this chapter you will be able to:**
> - **Show** that a softmax over very wide scores stops being soft
> - **Say what "variances add" means** and use it to explain why we divide by the square root of the width
> - **Do one attention pass by hand with both repairs** and land on `[0.6698, 0.3302]`
> - **Write the mask in torch** with `torch.tril` and `masked_fill`, before the softmax, and check it worked
> - **Say why `-inf` and not `0`**, and why before the softmax and not after
> - **Say why one masked pass over a sentence gives many lessons at once**
> - **Cut a width into heads** with `.view(B, T, H, dh).transpose(1, 2)` and say every shape on the way
>
> **New maths:** **variances add.** Two independent wobbles of spread 3 and 4 make a wobble of spread **5**, not 7. Measured today with a seeded generator; not proved.
>
> **New syntax:** `scores.masked_fill(mask, float("-inf"))` · `torch.tril` · `.view(B, T, H, dh).transpose(1, 2)`
>
> **New words:** scale · saturate · mask · causal mask · label leakage · head · head width (`dh`)
>
> **Reading time:** about 30 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60 minutes: one pen pass, one page of softmax arithmetic, and about 10 minutes at the computer.

> **📌 About the code blocks.** Each block is a file, with its name in the first line. Keep them in **one folder**. `scale.py`, `heads.py` and the two files marked **DELIBERATE** stand alone. **`dials.py` is typed in one go, and `hw.py` is typed at the bottom of it** (it uses the names `dials.py` makes). Every output shown was printed by a real run on a CPU with one thread and the seeds shown. The numbers that come from random draws are seeded; on a different NumPy or PyTorch build the *pattern* is the same and the third decimal can move. Nothing this week needs the internet, and **nothing is trained**: there is no model today. The three words and three tables are **invented by us**, the same ones as Week 14. The tables in `heads.py` are random and untrained; they are there to show shapes and checks, not to show what a trained model does.

![Map of the 36 weeks in four term lanes with week 15, Scale, Mask, and Many Heads, highlighted in term 2 and weeks 1 to 14 solid behind it](../figures/fig-w15-0-where-this-fits.svg)
*Figure 15.0 — Where this week fits: week 15 of 36, in term 2 (memory, then attention).*

---

## 🪝 Start Here

Last week's river question, with the scores `0.1, 2.0, 0.3` and the values `10, 50, 30`, gave weights `0.112, 0.751, 0.137` and a soft answer of `42.77`.

Now **shout the question ten times louder**: the scores become `1, 20, 3`. Before you run anything, write your guess on workbook page 15.1: *what will the answer be now: still about 42, or something else?*

Then keep the question in your head while you read: *real scores are not 0, 1, 2. Where do real scores come from, and how big are they?*

---

## 🧠 The Big Idea

### 1. The new maths: variances add

You already know **spread** (standard deviation, Level 3) and **variance** (the spread squared). The new fact is how spreads combine when you **add** two things that have nothing to do with each other. Such things are called **independent**.

| Thing | Spread | Variance (spread x spread) |
|---|:--:|:--:|
| `a`, a wobble | 3 | 9 |
| `b`, another, unrelated wobble | 4 | 16 |
| `a + b` | **5** (not 7) | **25** = 9 + 16 |

In one sentence: **to add independent wobbles, add their variances, then take the square root.** Spreads do not add; their squares do. (A 3-4-5 triangle is the same picture.)

Now a **score** is a dot product: `q . k = q1 k1 + q2 k2 + ... + qd kd`, a sum of `d` products. Suppose the numbers in `q` and `k` are random with spread 1 and have nothing to do with each other. Then each product has a variance of about 1 (we will measure this, not prove it). Add `d` of them and the variances add:

| Width `d` | Variance of `q . k` | Spread | After dividing by `sqrt(d)` |
|:--:|:--:|:--:|:--:|
| 4 | about 4 | about **2** | 1 |
| 16 | about 16 | about **4** | 1 |
| 64 | about 64 | about **8** | 1 |

**The longer the list, the wider the dot product.** Dividing a list of numbers by 8 divides its spread by 8 (you did exactly this with z-scores in Level 3), so dividing by `sqrt(d)` turns a spread of `sqrt(d)` into a spread of 1, at every width. That is the whole idea. We call this divide the **scale**.

### 2. Measure it: `scale.py`

Type this. Before you run it, write down what you think the spread of `a + b` will be.

```python
# scale.py - Week 15: why big dot products need a divide. numpy only. Everything is seeded.
import numpy as np

rng = np.random.default_rng(0)

# ---- 0. Two independent wobbles added together: spreads 3 and 4 ----
a = rng.normal(0, 3, size=100000)
b = rng.normal(0, 4, size=100000)
print("spread of a:", round(a.std(), 2), " spread of b:", round(b.std(), 2), " spread of a + b:", round((a + b).std(), 2))
print("variance of a:", round(a.var(), 1), " of b:", round(b.var(), 1), " of a + b:", round((a + b).var(), 1), "  (9 + 16 = 25)")

# ---- 1. The Week 14 river, with the question shouted ten times louder ----
values = np.array([10.0, 50.0, 30.0])
def nice(w, places):
    """A row of weights as plain decimals (no 4.5e-05 style)."""
    return "  ".join([f"{x:.{places}f}" for x in w])

def softmax(s):
    e = np.exp(s)
    return e / e.sum()

calm = np.array([0.1, 2.0, 0.3])
loud = calm * 10
print("calm weights:", nice(softmax(calm), 3), " answer:", round((softmax(calm) * values).sum(), 2))
print("loud weights:", nice(softmax(loud), 6), " answer:", round((softmax(loud) * values).sum(), 2))

# ---- 2. The module's example: three raw scores from a 64-wide dot product ----
raw = np.array([8.0, -2.0, 1.0])
print("raw    [8, -2, 1]        ->", nice(softmax(raw), 6))
print("scaled [1, -0.25, 0.125] ->", nice(softmax(raw / 8), 3), "  (8 is the square root of 64)")

# ---- 3. Measure how wide the dot products are, at three widths ----
print("\nwidth d | spread of q.k (raw) | spread after dividing by sqrt(d)")
for d in [4, 16, 64]:
    q = rng.normal(0, 1, size=(10000, d))      # 10,000 random questions, d numbers each
    k = rng.normal(0, 1, size=(10000, d))      # 10,000 random labels
    dots = (q * k).sum(axis=1)                 # 10,000 dot products
    print(f"{d:>7} | variance {dots.var():6.2f}  spread {dots.std():5.2f} | spread {(dots / d ** 0.5).std():5.2f}")

# ---- 4. What that does to a softmax: the biggest weight in a row of 8 scores ----
print("\nwidth d | average biggest weight: raw | divided by sqrt(d)")
for d in [4, 16, 64]:
    q = rng.normal(0, 1, size=(2000, 8, d))    # 2,000 rows; each row is 1 question against 8 labels
    k = rng.normal(0, 1, size=(2000, 8, d))
    s = (q * k).sum(axis=2)                    # (2000, 8): 8 scores per row
    raw_w = np.exp(s) / np.exp(s).sum(axis=1).reshape(-1, 1)
    sc = s / d ** 0.5
    sc_w = np.exp(sc) / np.exp(sc).sum(axis=1).reshape(-1, 1)
    print(f"{d:>7} | {raw_w.max(axis=1).mean():.3f} | {sc_w.max(axis=1).mean():.3f}")
print("(a row of 8 equal weights would have a biggest weight of", 1 / 8, ")")
```

Output of a real run (seeded):

```text
spread of a: 3.0  spread of b: 4.01  spread of a + b: 5.01
variance of a: 9.0  of b: 16.1  of a + b: 25.1   (9 + 16 = 25)
calm weights: 0.112  0.751  0.137  answer: 42.77
loud weights: 0.000000  1.000000  0.000000  answer: 50.0
raw    [8, -2, 1]        -> 0.999044  0.000045  0.000911
scaled [1, -0.25, 0.125] -> 0.587  0.168  0.245   (8 is the square root of 64)

width d | spread of q.k (raw) | spread after dividing by sqrt(d)
      4 | variance   4.03  spread  2.01 | spread  1.00
     16 | variance  16.04  spread  4.00 | spread  1.00
     64 | variance  62.58  spread  7.91 | spread  0.99

width d | average biggest weight: raw | divided by sqrt(d)
      4 | 0.573 | 0.372
     16 | 0.763 | 0.363
     64 | 0.880 | 0.365
(a row of 8 equal weights would have a biggest weight of 0.125 )
```

Read the output in order:

- **Spread of `a + b` is about 5**, and the variances give `9 + 16 = 25`. Variances add.
- **Calm versus loud.** The loud question gives weights `0.000000  1.000000  0.000000` and the answer `50.0`. The soft lookup has **frozen into the hard lookup** of Week 14. When a softmax puts nearly all its weight on one entry we say it has **saturated**.
- **The 64-wide example.** Raw scores `8, -2, 1` give `0.999044` on the first and almost nothing on the others. Divided by 8 (the square root of 64) they become `1, -0.25, 0.125`, and the weights are `0.587  0.168  0.245`: everyone still counts. The biggest weight is about 22,000 times the smallest before the divide, and about 3.5 times after.
- **The table.** The spread of `q . k` goes 2, 4, 8 (the 64 row prints `7.91`; it is a random measurement). After the divide it is 1 at every width.
- **The last table.** For a row of 8 scores, a perfectly equal share would give a biggest weight of `0.125`. Raw scores at width 64 give `0.880`: nearly one winner. Divided scores stay near `0.365` at every width.

**Honest limit.** The argument needs the numbers to be independent. In a *trained* model they are not exactly random and not exactly independent, so "the spread is exactly `sqrt(d)`" is true for random tables at the start and only roughly true later. The fair claim is: *the divide gives every width the same calm start.*

![Left, bars of weights from raw scores 8, minus 2, 1 where one bar takes 0.999044, beside bars from the same scores divided by 8 that are 0.587, 0.168 and 0.245; right, bars of spread by width](../figures/fig-w15-1-why-divide.svg)
*Figure 15.1 — Dividing by the square root of the width keeps the softmax soft at every width.*

### 3. Dial 2: hide the future

A model that learns to predict the next word reads a sentence and must guess each word from the words before it. If word 3 is allowed to *read* word 4 while predicting it, it will simply copy it. That is **label leakage**: the answer is leaking into the question.

The rule is: **word `i` may read word `j` only when `j` is at or before `i`.** A table that says who may read whom has a 1 where reading is allowed. Row `i` is word `i` asking; column `j` is the word being read:

```text
            reads:  word 1   word 2   word 3
   word 1             1        0        0
   word 2             1        1        0
   word 3             1        1        1
```

This lower-triangle table is called the **causal mask** (the order of cause and effect only runs forwards). How do we make a softmax ignore the cells marked 0? We cannot just delete them. Instead we set their **scores** to minus infinity, **before** the softmax. Since `exp(-inf)` is exactly 0, those cells get a weight of exactly 0, and the rest share out the total so the row still adds to 1.

Two wrong ways, which you will see fail by printing:

- Set the hidden scores to `0`. But `exp(0) = 1`: a score of 0 is not "nothing", it is an ordinary weight.
- Zero the **weights** after the softmax. Then the rows no longer add to 1.

### 4. Three new pieces of syntax

Each snippet below is complete and runs on its own.

```python
import torch
import torch.nn.functional as F

# (a) torch.tril: keep the lower triangle (diagonal included), zero the rest
print(torch.tril(torch.ones(3, 3)))
print(torch.tril(torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])))

# (b) masked_fill(mask, value): wherever mask is True, put value. The mask must be True/False.
scores = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
allowed = torch.tril(torch.ones(3, 3))
print(allowed == 0)                                     # True where the future is
print(scores.masked_fill(allowed == 0, float("-inf")))
print(F.softmax(scores.masked_fill(allowed == 0, float("-inf")), dim=-1))

# (c) view + transpose: cut the width into heads
x = torch.zeros(2, 5, 12)                               # 2 sentences, 5 words, width 12
cut = x.view(2, 5, 3, 4)                                # 3 heads of width 4
print(tuple(cut.shape), "->", tuple(cut.transpose(1, 2).shape))
print("3 heads x 4 =", 3 * 4, "= the width 12")
```

Output of the snippet above:

```text
tensor([[1., 0., 0.],
        [1., 1., 0.],
        [1., 1., 1.]])
tensor([[1., 0., 0.],
        [4., 5., 0.],
        [7., 8., 9.]])
tensor([[False,  True,  True],
        [False, False,  True],
        [False, False, False]])
tensor([[1., -inf, -inf],
        [4., 5., -inf],
        [7., 8., 9.]])
tensor([[1.0000, 0.0000, 0.0000],
        [0.2689, 0.7311, 0.0000],
        [0.0900, 0.2447, 0.6652]])
(2, 5, 3, 4) -> (2, 3, 5, 4)
3 heads x 4 = 12 = the width 12
```

**(a) `torch.tril`: the lower triangle.** Read as: *"keep the numbers on and below the diagonal; set the rest to 0."* `torch.tril(torch.ones(3, 3))` is exactly the table of 1s above: row `i` has a 1 for every word that word `i` may read. It works on any table, as the second print shows.

**(b) `scores.masked_fill(mask, float("-inf"))`: write a value where a condition holds.** Read as: *"wherever `mask` is True, put `-inf` instead."* Three things to be exact about:

1. **The mask must be True/False.** `torch.tril(torch.ones(...))` is a table of `1.` and `0.`, so make the True/False table with a comparison: `allowed == 0` is **True where the future is**. Print it; it is the upper triangle.
2. **`float("-inf")`** is minus infinity: a value smaller than every number.
3. **The order is: scores, divide, `masked_fill`, `F.softmax`.**

The first word has a single allowed entry, so its row is `[1, 0, 0]` whatever the scores say: the first word can only look at itself.

**(c) `.view(B, T, H, dh).transpose(1, 2)`: cut the width into heads.** Read as: *"each word has `d` numbers; cut them into `H` pieces of `dh = d // H` numbers; then bring the piece-axis forward so that each piece is a little attention problem of its own."* A **head** is one of those pieces with its own question, label and value tables. `dh` is the **head width**. The shapes, step by step:

```text
   (B, T, d)   ->  view(B, T, H, dh)  ->  (B, T, H, dh)  ->  transpose(1, 2)  ->  (B, H, T, dh)
   B = sentences in the batch, T = words per sentence, d = numbers per word, H = heads, dh = d // H
```

After that, `q @ k.transpose(-2, -1)` has shape `(B, H, T, T)`: a `T` by `T` table of scores for every head in every sentence. `transpose(1, 2)` swaps axes 1 and 2 by number, because here the head axis must come *forward*. `.view` gives the **same numbers in the same order** in a new shape; it never moves data, so the *order* of the four axes matters.

---

## 🎲 Your Turn: Pen Pass 2

**No laptop for this part.** You need a pen, a calculator and your Week 14 pen sheet. This is the same three-word pass, now with **both dials on**. The exps are given so that the calculator does not eat the lesson. **Carry four decimal places in the weights. Round only the answer.**

```text
PEN PASS 2 - the same three words as Week 14, now with BOTH dials.

   From your Week 14 sheet:     scores   the [1, 0, 1]        values   V(the) = [0, 1]
                                         cat [0, 1, 1]                 V(cat) = [1, 0]
                                         sat [1, 1, 2]                 V(sat) = [1, 1]

   The width is d = 2.  sqrt(2) = 1.4142,  1 / sqrt(2) = 0.7071.
   exp(0) = 1.0000     exp(0.7071) = 2.0281     exp(1.4142) = 4.1132

STEP A  DIVIDE.  Divide every score by 1.4142 (or multiply by 0.7071). Write each to four places.
                  key:  the      cat      sat
        the      [ ____   ____   ____ ]
        cat      [ ____   ____   ____ ]
        sat      [ ____   ____   ____ ]

STEP B  HIDE THE FUTURE.  Row i may read only words 1..i. Write  X  through every score ABOVE the diagonal.
        (The crossed-out scores are -inf: they get weight exactly 0, so do not use them again.)

STEP C  SHARE.  For each ROW, exp of each score that is LEFT, the row total, each exp / total.
        row the:  exps __          total __     weights __ __ __     (they must add to 1)
        row cat:  exps __ __       total __     weights __ __ __
        row sat:  exps __ __ __    total __     weights __ __ __

STEP D  BLEND.   output row = (weight 1) x V(the) + (weight 2) x V(cat) + (weight 3) x V(sat)
        the ->  [ ____ , ____ ]
        cat ->  [ ____ , ____ ]
        sat ->  [ ____ , ____ ]                 (four places)

CHECK   Did every weight row add to 1?  __     Is every number above the diagonal in the weights 0?  __
COMPARE Put your Week 14 output for cat and sat beside this one.
WRITE   Which number moved most, and which dial (divide or hide the future) moved it?
```

After step C, stop and add each weight row. If a row does not add to 1, find out why before you go on. Keep your sheet: the computer will check it next.

---

## 💻 The Two Dials in Torch: `dials.py`

Type all of this into one file. `attend_dials(scale, hide)` is Week 14's pass with the two repairs as switches, so you can see all four settings side by side. Read your own pen numbers aloud before you run it.

```python
# dials.py - Week 15: the two dials (divide, hide the future) on the Week 14 pass.
# Same three words and tables as Week 14: INVENTED, nothing learned, nothing a language model.
import torch
import torch.nn.functional as F

torch.set_num_threads(1)

X  = torch.tensor([[1.0, 0.0],
                   [0.0, 1.0],
                   [1.0, 1.0]])           # the, cat, sat
Wq = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
Wk = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
Wv = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
Q, K, V = X @ Wq, X @ Wk, X @ Wv
d = 2

# ---- the mask: a lower-triangle table of 1s. Row i has 1s for the words that word i may read. ----
mask = torch.tril(torch.ones(3, 3))
print("mask =")
print(mask)

def rows(t, places=4):
    """Print a tensor as rounded plain numbers, one row per line."""
    for r in t.tolist():
        print([round(x, places) for x in r])

def attend_dials(scale, hide):
    """The Week 14 pass with the two dials as switches. Returns (weights, output)."""
    scores = Q @ K.transpose(-2, -1)
    if scale:
        scores = scores / d ** 0.5               # dial 1: divide by the square root of the width
    if hide:
        scores = scores.masked_fill(mask == 0, float("-inf"))     # dial 2: hide the future, BEFORE the softmax
    weights = F.softmax(scores, dim=-1)
    return weights, weights @ V

# ---- the four settings of the two dials ----
for scale, hide in [(False, False), (True, False), (False, True), (True, True)]:
    w, out = attend_dials(scale, hide)
    print("\ndivide =", scale, "  hide the future =", hide, "  -> output")
    rows(out)

w, out = attend_dials(True, True)
print("\nboth dials: weights")
rows(w)
print("row sums:", w.sum(dim=-1).tolist())
print("the module's answer for cat is [0.6698, 0.3302]; ours:", [round(x, 4) for x in out[1].tolist()])

# ---- what the masked scores look like just before the softmax ----
scores = (Q @ K.transpose(-2, -1)) / d ** 0.5
print("\nscores after the divide, after the mask:")
print(scores.masked_fill(mask == 0, float("-inf")))

# ---- the test that the future is really hidden: change the LAST word, do earlier answers move? ----
X2 = torch.tensor([[1.0, 0.0],
                   [0.0, 1.0],
                   [5.0, -3.0]])                  # the same first two words, a very different third word
def answer_for(x, hide):
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    s = q @ k.transpose(-2, -1) / d ** 0.5
    if hide:
        s = s.masked_fill(mask == 0, float("-inf"))
    return F.softmax(s, dim=-1) @ v
print("\nchange the LAST word; does each row of the output move? (True = moved)")
print("  without the mask:", [(answer_for(X, False)[i] - answer_for(X2, False)[i]).abs().max().item() > 1e-6 for i in range(3)])
print("  with the mask:   ", [(answer_for(X, True)[i] - answer_for(X2, True)[i]).abs().max().item() > 1e-6 for i in range(3)])

# ---- why -inf and not 0 ----
zero_filled = (Q @ K.transpose(-2, -1) / d ** 0.5).masked_fill(mask == 0, 0.0)
print("\nhidden with 0 instead of -inf: weights =")
rows(F.softmax(zero_filled, dim=-1))
late = F.softmax((Q @ K.transpose(-2, -1) / d ** 0.5), dim=-1) * mask      # mask applied AFTER the softmax
print("mask applied after the softmax: weights =")
rows(late)
print("row sums:", [round(x, 4) for x in late.sum(dim=-1).tolist()])

# ---- one sentence, T training signals ----
words = ["the", "baker", "made", "bread", "daily"]
print("\nwith the mask, ONE pass gives", len(words) - 1, "lessons:")
for i in range(len(words) - 1):
    print(f"  reads {words[:i + 1]}  ->  must predict '{words[i + 1]}'")
```

Output of a real run:

```text
mask =
tensor([[1., 0., 0.],
        [1., 1., 0.],
        [1., 1., 1.]])

divide = False   hide the future = False   -> output
[0.5777, 0.8446]
[0.8446, 0.5777]
[0.7881, 0.7881]

divide = True   hide the future = False   -> output
[0.5989, 0.8022]
[0.8022, 0.5989]
[0.7517, 0.7517]

divide = False   hide the future = True   -> output
[0.0, 1.0]
[0.7311, 0.2689]
[0.7881, 0.7881]

divide = True   hide the future = True   -> output
[0.0, 1.0]
[0.6698, 0.3302]
[0.7517, 0.7517]

both dials: weights
[1.0, 0.0, 0.0]
[0.3302, 0.6698, 0.0]
[0.2483, 0.2483, 0.5035]
row sums: [1.0, 1.0, 1.0]
the module's answer for cat is [0.6698, 0.3302]; ours: [0.6698, 0.3302]

scores after the divide, after the mask:
tensor([[0.7071,   -inf,   -inf],
        [0.0000, 0.7071,   -inf],
        [0.7071, 0.7071, 1.4142]])

change the LAST word; does each row of the output move? (True = moved)
  without the mask: [True, True, True]
  with the mask:    [False, False, True]

hidden with 0 instead of -inf: weights =
[0.5035, 0.2483, 0.2483]
[0.2483, 0.5035, 0.2483]
[0.2483, 0.2483, 0.5035]
mask applied after the softmax: weights =
[0.4011, 0.0, 0.0]
[0.1978, 0.4011, 0.0]
[0.2483, 0.2483, 0.5035]
row sums: [0.4011, 0.5989, 1.0]

with the mask, ONE pass gives 4 lessons:
  reads ['the']  ->  must predict 'baker'
  reads ['the', 'baker']  ->  must predict 'made'
  reads ['the', 'baker', 'made']  ->  must predict 'bread'
  reads ['the', 'baker', 'made', 'bread']  ->  must predict 'daily'
```

Compare with your pen sheet. With both dials on, the `cat` row of the output should match the module's `[0.6698, 0.3302]`, and the `sat` row `[0.7517, 0.7517]` (if you added the rounded weights `0.2483 + 0.5035` by hand you got `0.7518`; that is rounding, not a mistake).

What the printout shows:

- **The divide** flattens the scores. The `sat` row of the output changed from `[0.7881, 0.7881]` to `[0.7517, 0.7517]` because the scores `1, 1, 2` became `0.71, 0.71, 1.41`.
- **The mask** changed the `the` row from `[0.5777, 0.8446]` to `[0.0, 1.0]`: it can only read itself.
- **The proof that the future is hidden.** We changed only the **last** word. Without the mask, all three rows moved. With the mask, the first two rows did not move at all (`False`). Changing word 3 cannot change what words 1 and 2 hear.
- **`0` instead of `-inf`** left weights in the hidden cells. **The mask after the softmax** left rows that add to `0.4011` and `0.5989`, not 1.
- **One sentence, many lessons.** With the mask, a five-word sentence gives four separate training questions in a single pass: each prefix must predict the next word. Without a mask there would be no honest question to ask.

![A 3 by 3 mask of ones and zeros, the attention weights with the later words struck out, and a small table showing that changing the last word moves only the last row once the mask is on](../figures/fig-w15-2-hide-the-future.svg)
*Figure 15.2 — The causal mask hides later words before the softmax, so earlier answers cannot change.*

---

## 🔬 Break the Mask

This section shows the error you get when `masked_fill` receives the wrong kind of mask, so you can read it.

**DELIBERATE:** this file is written to fail. It is a separate file.

```python
# DELIBERATE: masked_fill given the table of 1s and 0s instead of True and False.
import torch

scores = torch.ones(3, 3)
mask = torch.tril(torch.ones(3, 3))
print(scores.masked_fill(mask, float("-inf")))
```

Output of a real run:

```text
Traceback (most recent call last):
  File "/home/you/l4/bad5.py", line 6, in <module>
    print(scores.masked_fill(mask, float("-inf")))
RuntimeError: masked_fill_ only supports boolean masks, but got mask with dtype float
```

Read the last line: `masked_fill` wants a table of True and False (a **boolean** table), and `torch.tril(torch.ones(...))` is a table of floats. On workbook page 15.3, write the fix, and say which cells of your fixed mask are True.

---

## ✂️ Many Heads: `heads.py`

Type this. The first part cuts a table you can read; the rest uses random, **untrained** tables (seed 0) to check shapes and independence.

```python
# heads.py - Week 15: cutting the width into heads with view + transpose. Random tables, seed 0: NOT trained.
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)

# ---- 1. The reshape, on numbers you can read: 1 sentence, 3 words, width 4, 2 heads ----
B, T, d, H = 1, 3, 4, 2
dh = d // H                                        # the width of ONE head: 4 // 2 = 2
x = torch.tensor([[[1.0, 2.0, 3.0, 4.0],
                   [5.0, 6.0, 7.0, 8.0],
                   [9.0, 10.0, 11.0, 12.0]]])      # (B, T, d) = (1, 3, 4)
print("x:", tuple(x.shape), " dh =", dh)
cut = x.view(B, T, H, dh)                          # cut each word's 4 numbers into H pieces of dh
print("after view(B,T,H,dh):", tuple(cut.shape))
heads = cut.transpose(1, 2)                        # bring the head axis forward
print("after transpose(1,2):", tuple(heads.shape), " = (B, H, T, dh)")
print("head 0 sees the FIRST two numbers of every word:")
print(heads[0, 0])
print("head 1 sees the LAST two numbers of every word:")
print(heads[0, 1])

# ---- 2. Full attention with heads: random tables, batch of 2 sentences ----
torch.manual_seed(0)
B, T, d, H = 2, 5, 8, 2
dh = d // H
lin_q = nn.Linear(d, d, bias=False)
lin_k = nn.Linear(d, d, bias=False)
lin_v = nn.Linear(d, d, bias=False)
x = torch.randn(B, T, d)                           # 2 sentences, 5 words, 8 numbers each
mask = torch.tril(torch.ones(T, T))

def split(t):
    """(B, T, d) -> (B, H, T, dh): H heads, each with its own slice of the width."""
    return t.view(B, T, H, dh).transpose(1, 2)

q, k, v = split(lin_q(x)), split(lin_k(x)), split(lin_v(x))
scores = q @ k.transpose(-2, -1) / dh ** 0.5       # (B, H, T, T): divide by the root of ONE head's width
scores = scores.masked_fill(mask == 0, float("-inf"))
weights = F.softmax(scores, dim=-1)
out = weights @ v                                  # (B, H, T, dh)
print("\nq:", tuple(q.shape), " scores:", tuple(scores.shape), " out:", tuple(out.shape))
print("every row adds to 1:", bool((weights.sum(dim=-1) - 1).abs().max() < 1e-6))
print("nothing above the diagonal:", bool((weights * (1 - mask)).abs().max() == 0))
print("number of knobs in the three tables:", 3 * d * d, "(no H in that number)")

# ---- 3. Are the heads really independent? Recompute head 1 alone from a slice of the width ----
h = 1
q1 = lin_q(x)[:, :, h * dh:(h + 1) * dh]           # just head 1's slice of the width: (B, T, dh)
k1 = lin_k(x)[:, :, h * dh:(h + 1) * dh]
v1 = lin_v(x)[:, :, h * dh:(h + 1) * dh]
s1 = (q1 @ k1.transpose(-2, -1) / dh ** 0.5).masked_fill(mask == 0, float("-inf"))
alone = F.softmax(s1, dim=-1) @ v1
print("\nhead 1 alone equals head 1 of the batched version:", bool((alone - out[:, h]).abs().max() < 1e-6))

# ---- 4. Two heads, two different ways of sharing attention (last word of sentence 0) ----
print("\nlast word, sentence 0: how head 0 and head 1 share attention over the 5 words")
print("  head 0:", [round(p, 3) for p in weights[0, 0, 4].tolist()])
print("  head 1:", [round(p, 3) for p in weights[0, 1, 4].tolist()])
```

Output of a real run:

```text
x: (1, 3, 4)  dh = 2
after view(B,T,H,dh): (1, 3, 2, 2)
after transpose(1,2): (1, 2, 3, 2)  = (B, H, T, dh)
head 0 sees the FIRST two numbers of every word:
tensor([[ 1.,  2.],
        [ 5.,  6.],
        [ 9., 10.]])
head 1 sees the LAST two numbers of every word:
tensor([[ 3.,  4.],
        [ 7.,  8.],
        [11., 12.]])

q: (2, 2, 5, 4)  scores: (2, 2, 5, 5)  out: (2, 2, 5, 4)
every row adds to 1: True
nothing above the diagonal: True
number of knobs in the three tables: 192 (no H in that number)

head 1 alone equals head 1 of the batched version: True

last word, sentence 0: how head 0 and head 1 share attention over the 5 words
  head 0: [0.212, 0.208, 0.18, 0.194, 0.206]
  head 1: [0.203, 0.217, 0.228, 0.149, 0.202]
```

Read it in order:

- Head 0 sees the **first** two numbers of every word; head 1 sees the **last** two. Nothing moved: `view` only re-labelled the axes.
- The scores are `(B, H, T, T)`. Note that we divide by `dh ** 0.5`, the square root of **one head's** width, because each score is a dot product of `dh` numbers.
- The number of knobs in the three tables is `3 * d * d = 192`. **There is no `H` in that number.** Heads give the *same* knobs, cut up, not more of them.
- `head 1 alone equals head 1 of the batched version: True`: the heads really are separate attention problems.
- The two lines at the end show two heads sharing their attention in two slightly different ways. Do not read meaning into them. The tables are random, so the weights are nearly equal everywhere (0.15 to 0.23). They say only that heads are **free to differ**, not that trained heads attend to different things. Week 19 measures a trained model and reports what it finds.

---

## 🔑 Wrap Up

This section collects what you built today and what you did not.

Three repairs you made today:

1. **The divide.** A dot product of `d` independent terms has spread `sqrt(d)`, so we divide by `sqrt(d)` to give every width a spread of 1 and keep the softmax soft.
2. **The mask.** Hide the future with `-inf` **before** the softmax. Then check two things: every weight row adds to 1, and everything above the diagonal is exactly 0.
3. **Heads.** `.view(B, T, H, dh).transpose(1, 2)` cuts the width into `H` pieces of `dh`. The knob count has no `H`.

What you did **not** do, on purpose:

- **Nothing was learned.** The tables are invented or random. Week 17 trains our own small model.
- **A mask does not make a model safe or honest.** It stops one leak: a word reading its own answer.
- **Two heads do not necessarily look at two different things.** With random tables they look at nearly the same amount everywhere.
- **The words still have no order.** Shuffle the rows and each word gets the same answer (with no mask). Week 16 fixes that.

**A look ahead.** Next week: adding a position to each word, and wrapping attention and a small network into one block that can be stacked.

---

## 📤 Homework

This section is the work to do before next week, with the computer check at the end.

Complete workbook pages 15.1 to 15.5 (about 60 minutes):

1. **A softmax by hand, before and after the divide (15.2).** Scores `4, -2, 2` come from a dot product of width 16. Work out the three weights raw, and divided by `sqrt(16) = 4`, then the ratio of the biggest weight to the smallest in each. Say in a sentence which one is still soft.
2. **A second pen pass with both dials (15.4).** Same `X`, `Wk` and `Wv`, but the question table is `Wq = [[0, 0], [1, 0]]`. **Before** calculating, predict what the row `the` becomes and why.
3. **The shapes of heads, and the computer check (15.5).** For 2 sentences of 5 words, width 12 and 3 heads: write `dh`, the shape after `.view(B, T, H, dh)`, the shape after `.transpose(1, 2)`, the shape of the score table, and the number of knobs in the three tables. Then check your work with the file below.

When you have finished the pen work, type this at the **bottom** of `dials.py`. It changes `Wq`, so it must come after the lines above. It prints the weights and output for task 2, the two softmaxes of task 1, and the shapes of task 3. If your pen answer and the computer differ by more than `0.001`, find out which is wrong before you move on.

```python
# hw.py - Week 15 homework check. Typed at the BOTTOM of dials.py (it re-assigns Wq, Q and calls attend_dials).
Wq = torch.tensor([[0.0, 0.0], [1.0, 0.0]])        # the Week 14 H2 question table
Q = X @ Wq
w, out = attend_dials(True, True)
print("H2 weights (both dials):")
rows(w)
print("H2 output:")
rows(out)

# H1: three scores from a 16-wide dot product, before and after the divide
s = torch.tensor([4.0, -2.0, 2.0])
print("\nH1 raw:    ", [round(p, 4) for p in F.softmax(s, dim=-1).tolist()])
print("H1 divided:", [round(p, 4) for p in F.softmax(s / 16 ** 0.5, dim=-1).tolist()])

# H3: shapes for 2 sentences, 5 words, width 12, 3 heads
B, T, d, H = 2, 5, 12, 3
torch.manual_seed(0)
t = torch.randn(B, T, d).view(B, T, H, d // H).transpose(1, 2)
print("\nH3 per-head tensor:", tuple(t.shape), " scores:", tuple((t @ t.transpose(-2, -1)).shape))
```

---

## 📖 Words from this week

The words and syntax introduced this week, for reference.

| Word | Meaning |
|---|---|
| **independent** | two things with nothing to do with each other |
| **variances add** | for independent wobbles, the variance of the sum is the sum of the variances; the spread is the square root |
| **scale** | the divide by `sqrt(d)` applied to scores before the softmax |
| **saturate** | a softmax puts nearly all its weight on one entry |
| **mask** | a table saying which cells to hide |
| **causal mask** | the lower-triangle mask: a word may read itself and earlier words only |
| **label leakage** | the answer being visible to the thing that must predict it |
| **head** | one slice of the width with its own question, label and value tables |
| **`dh`** | the width of one head, `d // H` |
| **`torch.tril`** | keep the lower triangle, zero the rest |
| **`masked_fill(mask, v)`** | where the True/False mask is True, put `v` |
| **`.view(B,T,H,dh).transpose(1,2)`** | cut the width into heads and bring the head axis forward |

---

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Workbook](../workbook/week-15.md)
