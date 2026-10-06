# Week 14 — Attention by Hand

[⬅ Week 13](week-13.md) · [Course Home](../README.md) · [Week 15 ➡](week-15.md) · [Workbook](../workbook/week-14.md)

---

> ### This week in one sentence
> **Attention is a soft dictionary lookup: compare a question with every label, turn the scores into weights that add up to 1, and hand back the weighted average of what each entry says. Today you do one small pass with a pen, then in numpy, then in torch, and show that all three agree.**
>
> **By the end of this chapter you will be able to:**
> - **Compute a weighted average by hand** and say why the weights must add to 1
> - **Say the difference** between a hard lookup (one winner) and a soft lookup (everyone counts, in proportion)
> - **Do the four steps of one attention pass** on three words: make, score, share, blend
> - **Type the same pass** in numpy and in torch with `nn.Linear(d, d, bias=False)`, `k.transpose(-2, -1)` and `unsqueeze`
> - **Show that pen, numpy and torch agree** to within rounding
> - **Explain why a word gets a question *and* a label** (two different tables)
>
> **New maths:** the **weighted average**: a mean where some values count more. The weights are never negative and add to 1.
>
> **New syntax:** `k.transpose(-2, -1)` · `nn.Linear(d, d, bias=False)` · `tensor.unsqueeze(dim)`
>
> **New words:** token · query · key · value · score · weight · weighted average · hard lookup / soft lookup · attention
>
> **Reading time:** about 30 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60 minutes, almost all of it pen and calculator; the computer is used for about 10 minutes of checking.

> **📌 About the code blocks.** Each block is a file, with its name in the first line. Keep them in **one folder**. `lookup.py` stands alone. **`attention.py` is typed in pieces, one after another, into the same file**, so that later pieces can use the names made by earlier ones; the chapter says when a block goes "at the bottom of `attention.py`". Every output shown was printed by a real run on a CPU. Different PyTorch build: the last digit of the tiny gap in `numpy vs torch` can differ (anything below `1e-05` is fine). Blocks marked **DELIBERATE** are written on purpose to fail. Nothing this week needs the internet, and **nothing is trained**: there is no model today. The three word vectors and the three tables are **invented by us** so that they are easy to multiply. They are not learned, and the words `the`, `cat`, `sat` are only labels on rows.

![Map of the 36 weeks in four term lanes with week 14, Attention by Hand, highlighted in term 2 and weeks 1 to 13 solid behind it](../figures/fig-w14-0-where-this-fits.svg)
*Figure 14.0 — Where this week fits: week 14 of 36, in term 2 (memory, then attention).*

---

## 🪝 Start Here

This section gives you the idea of a soft lookup with a tiny example, before any code.

Imagine three people, each holding one secret number:

| Person | Their number |
|---|:--:|
| bread | 10 |
| river | 50 |
| rope | 30 |

You ask: *"Who knows about the river?"* Each person has a label for what they know, and we measure how well each label matches your question: **bread 0.1 · river 2.0 · rope 0.3**.

- **Hard lookup:** you may listen to only one person, the best match. That is `river`, so the answer is **50**. Everyone else is silenced.
- **Soft lookup:** bread and rope matched a little too. Why throw their answers away? Let **everyone** answer, at a volume that matches how well they matched.

For the volumes we need numbers that add up to 1. Where have you seen scores turned into shares that add to 1? Last week: **softmax**.

Before you read on, write your guess on workbook page 14.1: *will the soft answer be bigger than 50, equal to 50, or smaller?*

---

## 🧠 The Big Idea

This section defines the weighted average, shows it in code, and lays out the four steps of one attention pass.

### 1. The new maths: the weighted average

You know the ordinary **mean**: add up, divide by how many. A **weighted average** lets some values count more. Each value gets a **weight**. Two rules for the weights: none is negative, and they **add up to 1**. Then multiply each value by its own weight and add.

Values `10, 50, 30` with weights `0.7, 0.2, 0.1`:

```text
   0.7 x 10  +  0.2 x 50  +  0.1 x 30   =   7 + 10 + 3   =   20
```

Two facts worth keeping:

- Because the weights are not negative and add to 1, the answer always lands **between the smallest and the biggest value** (20 is between 10 and 50).
- Equal weights (`1/3, 1/3, 1/3`) give the plain mean. A **hard** lookup is the special case where one weight is 1 and the rest are 0.

### 2. The soft lookup in code: `lookup.py`

Type this. Before you run it, write down what you think the hard lookup prints and roughly what the soft one prints.

```python
# lookup.py - Week 14: a dictionary lookup, hard and then soft. Numpy only.
import numpy as np

names  = ["bread", "river", "rope"]
scores = np.array([0.1, 2.0, 0.3])        # how well each label matches the question (invented)
values = np.array([10.0, 50.0, 30.0])     # what each one could tell you (invented)

# HARD lookup: find the best match, hear only that one.
best = scores.argmax()
print("hard lookup:", names[best], "->", values[best])

# SOFT lookup, step 1: scores -> weights (the softmax you wrote in Week 13).
e = np.exp(scores)
weights = e / e.sum()
print("weights:", np.round(weights, 3), " add up to", round(weights.sum(), 3))

# SOFT lookup, step 2: the weighted average = each value times its weight, added up.
soft = (weights * values).sum()
print("soft lookup:", round(soft, 2))

# A weighted average with weights you choose yourself.
w = np.array([0.7, 0.2, 0.1])
print("weights [0.7, 0.2, 0.1]:", (w * values).sum())

# Equal weights give the ordinary mean.
equal = np.array([1/3, 1/3, 1/3])
print("equal weights:", round((equal * values).sum(), 2), " ordinary mean:", values.mean())
```

```text
hard lookup: river -> 50.0
weights: [0.112 0.751 0.137]  add up to 1.0
soft lookup: 42.77
weights [0.7, 0.2, 0.1]: 20.0
equal weights: 30.0  ordinary mean: 30.0
```

The soft answer, 42.77, is mostly the river's answer with a trace of the other two. If you did it on a calculator with the weights rounded to three places you got `1.12 + 37.55 + 4.11 = 42.78`. The computer kept every digit, so it says 42.77. That one hundredth is **rounding**, not a mistake.

Why bother with the soft version? Because every one of those numbers can be nudged a little, so a machine could *learn* to make the answer better. A hard "pick one" cannot be nudged. That is why models use soft lookups. (Learning comes in Week 17. Today there is none.)

![A table of bread, river and rope with scores, weight bars 0.112, 0.751 and 0.137, values 10, 50 and 30, and the soft answer 42.77 beside the hard answer 50.0](../figures/fig-w14-1-soft-lookup.svg)
*Figure 14.1 — A soft lookup is a weighted average: mostly the best match, with a trace of the others.*

### 3. Where the question, the label and the answer come from

In the people example someone handed us the scores. In a sentence, the words themselves must produce them. A **token** is one piece of text the model reads; today a token is one word. Each word is a row of numbers, and it is turned into three things by multiplying by three tables:

```text
   a word, as 2 numbers:  x = [1, 0]
        x times Wq  ->  q   "what am I looking for?"      the QUESTION  (query)
        x times Wk  ->  k   "what do I offer?"             the KEY       (a label)
        x times Wv  ->  v   "what do I actually say?"      the VALUE
```

### 4. The four steps

```text
   1. make     Q = X Wq      K = X Wk      V = X Wv                (each word's row times a table)
   2. score    scores = Q K^T                                       (every question against every key)
   3. share    weights = softmax of each ROW of scores              (each row adds to 1)
   4. blend    output = weights V                                   (weighted average of the values)
```

- **Step 2** is nine dot products for three words. The **score** of word *i*'s question against word *j*'s key is the dot product of row *i* of `Q` with row *j* of `K`: multiply matching numbers and add (Level 3).
- **Step 3** is the Week 13 softmax, applied to **each row separately**. One row is one word deciding how to share its attention, so it must add to 1.
- **Step 4**: each word's answer is a weighted average of all three values, using its own row of weights.

---

## 🎲 Your Turn: The Pen Pass

This section is for doing one full attention pass by hand, so that every later number has a pen answer to be checked against.

**No laptop for this part.** You need a pen and a calculator. The three words and the three tables are:

```text
   the  = [1, 0]        Wq = identity         Wk = identity         Wv = swap the two numbers
   cat  = [0, 1]             [[1, 0],              [[1, 0],              [[0, 1],
   sat  = [1, 1]              [0, 1]]               [0, 1]]               [1, 0]]
```

Fill in workbook page 14.2 as you go:

1. **Make.** Multiply each word's row by each table. (Hint: the identity table changes nothing, and `Wv` swaps the two numbers.) Write `Q`, `K`, `V`.
2. **Score.** Write the nine dot products as a 3 by 3 table.
3. **Share.** For each **row**, raise `e` to each score, add the three results, and divide each by that row total. **Carry four decimal places in the weights.** Check that each row adds to 1 (or very nearly).
4. **Blend.** For each word, multiply each row of `V` by that word's weight for it, and add. Round the *answer* to three places.

Then turn the sheet over and write one sentence: **which word did `sat` give the biggest weight to, and what number says so?**

Keep your sheet. In a moment the computer will check it.

> **⚠️ Watch out:** If a row of your weights does not add to 1, stop and look at that row before you go on. One slip in an exponent spoils every number after it. If you rounded the weights to only three places, a row may add to `0.999`; your answer may then differ from the computer's in the third decimal. That is fine. Four places avoids it.

---

## 💻 The Same Pass in Numpy: `attention.py`, Part 1

Each line below is one step of your pen pass. Before you run it, read your own pen numbers for the scores and the weights aloud.

```python
# attention.py - Week 14. One pass of attention on three tokens, three ways: numpy, torch, and the pen.
# The three tokens are "the", "cat", "sat". Their 2-number vectors and the three tables are INVENTED to be easy.
# Nothing here is learned and nothing is a language model.
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)

# ======================== PART 1: numpy, one line per step of the pen version ========================
X  = np.array([[1.0, 0.0],
               [0.0, 1.0],
               [1.0, 1.0]])               # one row per token
Wq = np.array([[1.0, 0.0],
               [0.0, 1.0]])               # question table
Wk = np.array([[1.0, 0.0],
               [0.0, 1.0]])               # label table
Wv = np.array([[0.0, 1.0],
               [1.0, 0.0]])               # what-I-say table (swaps the two numbers)

Q = X @ Wq                                # step 1: every token makes a question...
K = X @ Wk                                # ...a label...
V = X @ Wv                                # ...and a value
print("Q =\n", Q)
print("K =\n", K)
print("V =\n", V)

scores = Q @ K.T                          # step 2: every question against every label (nine dot products)
print("scores =\n", scores)

e = np.exp(scores)                        # step 3: softmax, row by row
weights = e / e.sum(axis=1).reshape(3, 1)
print("weights =\n", np.round(weights, 3))
print("row sums:", weights.sum(axis=1))

out = weights @ V                         # step 4: blend the values
print("output =\n", np.round(out, 3))
```

```text
Q =
 [[1. 0.]
 [0. 1.]
 [1. 1.]]
K =
 [[1. 0.]
 [0. 1.]
 [1. 1.]]
V =
 [[0. 1.]
 [1. 0.]
 [1. 1.]]
scores =
 [[1. 0. 1.]
 [0. 1. 1.]
 [1. 1. 2.]]
weights =
 [[0.422 0.155 0.422]
 [0.155 0.422 0.422]
 [0.212 0.212 0.576]]
row sums: [1. 1. 1.]
output =
 [[0.578 0.845]
 [0.845 0.578]
 [0.788 0.788]]
```

Compare with your pen sheet, row by row. If a row is off, check its row sum first.

One line needs explaining: `e.sum(axis=1)` is **three totals, one per row**. `.reshape(3, 1)` stands them on end so that each row is divided by **its own** total. (Dividing by `e.sum()` would use one grand total for everything, which is a different and wrong recipe.)

Note that `Q` and `K` came out equal. That is only because `Wq` and `Wk` are both the identity table here. It is not a rule of attention. The last section of today shows why.

![Three small grids joined by arrows: scores for the, cat and sat, then rows of weights that each add to 1 with the largest ringed, then the output rows](../figures/fig-w14-2-one-pass-three-words.svg)
*Figure 14.2 — One pass of attention on three words: scores, then weights that add to 1 in every row, then the blended output.*

---

## 🔥 The Same Pass in Torch: `attention.py`, Part 2

This section repeats the same pass in torch. Type the block below at the **bottom** of `attention.py`. Three new pieces of syntax appear, explained first.

**(a) `nn.Linear(d, d, bias=False)`.** You have built `nn.Linear` layers: a layer multiplies by a table and then adds a **bias**. `bias=False` leaves out the adding, so the layer is *a table and nothing else*, exactly like `X @ Wq` on paper. The table is kept in `lin.weight`. Watch out: `nn.Linear` stores its table **the other way round** (it computes `x @ W.T`), so to make a layer that does `x @ table` we hand it the table **turned on its side**. That is the `.transpose(0, 1)` in `linear_from`.

Today's tables (identity and swap) happen to be their own flips, so forgetting this would not show up today. It will matter when the tables are not like that, so build the habit now.

**(b) `k.transpose(-2, -1)`: swap the last two axes.** The score table is `q @ k.transpose(-2, -1)`. `q` has shape `(3, 2)`: three questions, two numbers each. To dot every question with every key we need the keys as `(2, 3)`. The pair `-2, -1` names "the last two axes", so the same words work for one sentence `(3, 2)` and for a stack of sentences `(2, 3, 2)`, leaving the stack axis alone.

**(c) `tensor.unsqueeze(dim)`: add a length-1 axis.** `w.unsqueeze(0)` puts the new axis at the front, `w.unsqueeze(-1)` at the end. We use it twice: to make a **batch of one sentence** `(3, 2)` into `(1, 3, 2)`, and to stand a row of weights on end so it multiplies the values. PyTorch stretches a length-1 axis to fit, so `(3, 1) * (3, 2)` multiplies each row of values by its own weight. Then `.sum(dim=0)` adds the rows.

```python
# ======================== PART 2: the same pass in torch ========================
xt = torch.tensor(X.tolist())             # the same three rows, now a torch tensor
d = 2


def linear_from(table):
    """A layer that is ONLY a table (no bias). nn.Linear stores its table the other way round, so we transpose."""
    lin = nn.Linear(d, d, bias=False)
    lin.weight.data = torch.tensor(table).transpose(0, 1)
    return lin


lin_q = linear_from(Wq.tolist())
lin_k = linear_from(Wk.tolist())
lin_v = linear_from(Wv.tolist())


def weights_of(x):
    """x is (T, d) or (B, T, d). The weights: one row per token, each row adds to 1."""
    q, k = lin_q(x), lin_k(x)
    scores = q @ k.transpose(-2, -1)      # swap the LAST TWO axes, whatever comes before them
    return F.softmax(scores, dim=-1)


def attend(x):
    """One pass of attention: weights, then blend the values."""
    return weights_of(x) @ lin_v(x)


def show(t):
    """Print a tensor as plain numbers rounded to 3 places."""
    print(np.round(t.tolist(), 3))


w_t = weights_of(xt)
out_t = attend(xt)
print("torch weights =")
show(w_t)
print("torch output =")
show(out_t)

# ---- unsqueeze: add an axis of length 1 ----
print("xt shape:", tuple(xt.shape))
batch = xt.unsqueeze(0)                   # a batch of ONE sentence: (1, 3, 2)
print("batch shape:", tuple(batch.shape))
print("batch answer shape:", tuple(attend(batch).shape))
print("same answer as the single pass:", (attend(batch)[0] - out_t).abs().max().item() == 0.0)

# two sentences at once: the second is the first with "the" and "sat" swapped
xt2 = torch.tensor([[1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])
both = torch.cat([xt.unsqueeze(0), xt2.unsqueeze(0)], dim=0)
print("two sentences:", tuple(both.shape), "->", tuple(attend(both).shape))

# ---- the blend written out: the weights of ONE token, stood on end, times the values ----
w3 = w_t[2]                               # the weights of "sat"
v_t = lin_v(xt)
blend = (w3.unsqueeze(-1) * v_t).sum(dim=0)     # (3,1) * (3,2) -> (3,2), then add the three rows
print("w3 shape:", tuple(w3.shape), " w3.unsqueeze(-1) shape:", tuple(w3.unsqueeze(-1).shape))
print("blend of the three value rows:", np.round(blend.tolist(), 3), " equals row 3 of the output:",
      (blend - out_t[2]).abs().max().item() < 1e-6)
```

```text
torch weights =
[[0.422 0.155 0.422]
 [0.155 0.422 0.422]
 [0.212 0.212 0.576]]
torch output =
[[0.578 0.845]
 [0.845 0.578]
 [0.788 0.788]]
xt shape: (3, 2)
batch shape: (1, 3, 2)
batch answer shape: (1, 3, 2)
same answer as the single pass: True
two sentences: (2, 3, 2) -> (2, 3, 2)
w3 shape: (3,)  w3.unsqueeze(-1) shape: (3, 1)
blend of the three value rows: [0.788 0.788]  equals row 3 of the output: True
```

Before running, predict the shape after `xt.unsqueeze(0)`. The last block is step 4 for the single word `sat`, done with a pen's logic: each value row times its own weight, then added. Say in your own words why `w3.unsqueeze(-1)` has shape `(3, 1)`.

---

## ✅ Do the Three Agree? `attention.py`, Part 3

This section compares the pen, numpy and torch answers in code.

At the bottom of `attention.py`, type the `hand` table **from your own pen sheet** (three decimals). The numbers below are what a careful pen pass gives; replace them with yours.

```python
# ======================== PART 3: do the three agree? ========================
hand = np.array([[0.578, 0.845],
                 [0.845, 0.578],
                 [0.788, 0.788]])         # typed in from the pen, three decimals
out_from_torch = np.array(out_t.tolist())
print("numpy vs torch, biggest gap:", np.abs(out - out_from_torch).max())
print("pen vs numpy, biggest gap:  ", round(np.abs(hand - out).max(), 4))
print("all three agree to 0.002:", np.abs(hand - out).max() < 0.002 and np.abs(out - out_from_torch).max() < 0.002)
```

```text
numpy vs torch, biggest gap: 4.222880078952329e-08
pen vs numpy, biggest gap:   0.0004
all three agree to 0.002: True
```

Three ways: a pen, numpy, torch. One answer. Agreement is **to rounding**, not exact: numpy keeps 64 bits per number, torch keeps 32, so they differ around the eighth decimal. A gap that is *not* tiny means a bug, not rounding.

---

## 🔬 Why a Question *and* a Label? `twotables.py`

This section is for seeing what changes when questions and labels come from two different tables, and for one general check on the weights.

In our example `Wq` and `Wk` are the same table. What do you expect about "`cat` asks about `sat`" compared with "`sat` asks about `cat`"? Write a guess, then type this at the bottom of `attention.py`.

```python
# twotables.py - Week 14: why a token gets a question AND a label. Needs attention.py run first (uses its names).
# With the SAME table for questions and labels, "cat asks about sat" equals "sat asks about cat".
# With DIFFERENT tables, it need not.
print("same table for both (attention.py):")
print(scores)                              # scores[1][2] and scores[2][1] are the same number

Wq2 = np.array([[0.0, 0.0],
                [1.0, 0.0]])               # a question built from the SECOND number of a token, put in the first slot
scores2 = (X @ Wq2) @ (X @ Wk).T
print("question table changed:")
print(scores2)
print("cat asks about sat:", scores2[1][2], "  sat asks about cat:", scores2[2][1])   # cat is row 1, sat is row 2

e2 = np.exp(scores2)
weights2 = e2 / e2.sum(axis=1).reshape(3, 1)
print("weights =\n", np.round(weights2, 3))
print("the's weights are all equal:", np.round(weights2[0], 3), "-> its answer is the plain mean of the values:",
      np.round(weights2[0] @ V, 3), np.round(V.mean(axis=0), 3))
print("first table is symmetric (score[i][j] equals score[j][i]):", bool((scores == scores.T).all()))
```

```text
same table for both (attention.py):
[[1. 0. 1.]
 [0. 1. 1.]
 [1. 1. 2.]]
question table changed:
[[0. 0. 0.]
 [1. 0. 1.]
 [1. 0. 1.]]
cat asks about sat: 1.0   sat asks about cat: 0.0
weights =
 [[0.333 0.333 0.333]
 [0.422 0.155 0.422]
 [0.422 0.155 0.422]]
the's weights are all equal: [0.333 0.333 0.333] -> its answer is the plain mean of the values: [0.667 0.667] [0.667 0.667]
first table is symmetric (score[i][j] equals score[j][i]): True
```

With one table, the score table is a mirror image of itself. With two tables, **what I look for and what I offer can be different**. (Picture a verb that looks for its subject while advertising itself as a verb.) Also look at `the`: its question is all zeros, so every score is 0, every weight is 0.333, and its answer is just the **plain mean** of the values. Attention with no preference is the ordinary average.

Last check: do the row sums stay at 1 even when the tables are random and nothing makes sense? Type this at the bottom too.

```python
# anyweights.py - Week 14: whatever the three tables hold, the weights always add to 1 (random tables, seed 0).
torch.manual_seed(0)
x4 = torch.randn(5, 4)                     # 5 tokens, 4 numbers each (random, invented)
r_q = nn.Linear(4, 4, bias=False)          # two random tables, nothing learned
r_k = nn.Linear(4, 4, bias=False)

w5 = F.softmax(r_q(x4) @ r_k(x4).transpose(-2, -1), dim=-1)
print("weights shape:", tuple(w5.shape))
print("row sums:", np.round(w5.sum(dim=-1).tolist(), 4))
print("every weight is between 0 and 1:", bool((w5 >= 0).all()) and bool((w5 <= 1).all()))
```

```text
weights shape: (5, 5)
row sums: [1. 1. 1. 1. 1.]
every weight is between 0 and 1: True
```

Each row is a softmax, so it adds to 1 and is never negative, **whatever the tables hold**. That is the only general claim today makes.

---

## 🛠️ Break It On Purpose

This section is for reading one shape error and fixing it.

What if you forget to turn the keys on their side? **DELIBERATE:** this file is written to fail. It is a separate file, not part of `attention.py`.

```python
# DELIBERATE: the labels were not turned on their side.
import torch

q = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])    # 3 questions, 2 numbers each
k = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])    # 3 labels, 2 numbers each
scores = q @ k
print(scores)
```

```text
Traceback (most recent call last):
  File "bad.py", line 6, in <module>
    scores = q @ k
RuntimeError: mat1 and mat2 shapes cannot be multiplied (3x2 and 3x2)
```

Read the last line. Two tables of shape `3x2` cannot be multiplied: the inner numbers (2 and 3) do not match. We need `(3, 2) @ (2, 3)`. On page 14.5, write the fix, and say what shape the answer will have and what each of its entries means.

---

## 🔑 Wrap Up

Three things you built today:

1. **A soft lookup is a weighted average:** weights that are never negative and add to 1.
2. **Four steps:** make (Q, K, V), score, share (softmax per row), blend.
3. **Three routes, one answer:** pen, numpy and torch agree to rounding.

What you did **not** do, on purpose:

- **Nothing was learned.** The tables are invented. Week 17 is where they are learned.
- **The weights do not say what matters.** They are a softmax of dot products of invented numbers. Never say "the model paid attention to the important word" about today's numbers.
- **This is not yet the pass a real language model runs (you will build a GPT, a text-writing model made of attention, in Week 17).** It has no divide and no "no peeking at the future". Next week adds both.
- **The words have no order yet.** Shuffle the rows and each word gets the same answer. Week 16 fixes that.

**A look ahead.** Next week two things break: what happens when the scores are big, and what stops a word from reading the future.

---

## 📤 Homework

Complete workbook pages 14.1 to 14.5 (about 60 minutes):

1. **The weighted-average sheet (14.1).** Several sets of values and weights. Say which sets are real weighted averages and why.
2. **The pen pass (14.2)**, which you did in class, and then **a second pass by hand with the question table changed**, as in `twotables.py`.
3. **The three-way check (14.4):** put your second pen answer into code and make the computer agree. If they do not, find out which of the two is wrong before you move on.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **token** | one piece of text the model reads; today, one word |
| **query** (question) | what a token is looking for: its row times `Wq` |
| **key** (label) | what a token offers so others can match it: its row times `Wk` |
| **value** | what a token actually says if listened to: its row times `Wv` |
| **score** | how well one token's query matches another's key (a dot product) |
| **weight** | a score turned into a share by softmax; never negative, each row adds to 1 |
| **weighted average** | a mean where some values count more; the weights add to 1 |
| **hard lookup** | listen to the best match only; one weight is 1, the rest 0 |
| **soft lookup** | listen to everyone, in proportion to their weight |
| **attention** | ask every token a question, share the attention out by softmax, take the weighted average of the values |
| **`k.transpose(-2, -1)`** | swap the last two axes |
| **`nn.Linear(d, d, bias=False)`** | a layer that is only a multiply by a table |
| **`unsqueeze(dim)`** | add a length-1 axis at that position |

---

[⬅ Week 13](week-13.md) · [Course Home](../README.md) · [Week 15 ➡](week-15.md) · [Workbook](../workbook/week-14.md)
