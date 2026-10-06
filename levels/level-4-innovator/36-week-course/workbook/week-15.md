# Workbook — Week 15: Scale, Mask, and Many Heads

**Name:** ________________________________  **Date:** ______________

[⬅ Week 14](week-14.md) · [📖 Read the chapter first](../student-guide/week-15.md) · [Course Home](../README.md) · [Next ➡](week-16.md)

---

> **Rules for this workbook.** Pages 15.1 to 15.5 are the week's homework (about 60 minutes: one pen pass, one page of softmax arithmetic, and about 10 minutes at the computer). Page 15.6 (break it on purpose) and page 15.7 (the Bug Log) are the extra pages that make the week stick; do them in the same sitting if you can.
>
> **Pen first, then run.** Write your answer **before** you open the check file. The numbers in the worked examples and in the answers came from real CPU runs (numpy 1.26 and PyTorch 2.2, one thread; every random draw is seeded). By-hand numbers are plain arithmetic and will match. On another CPU or build the **last digit** of a torch number can move, and the third decimal of a number measured from random draws can move; the **pattern** will not.
>
> **There is no model this week, and no stand-in.** Nothing is trained. The three word vectors and the tables are **invented by us** so they are easy to multiply; the words are only labels on rows. The tables with heads on page 15.5 are **random and untrained**. A weight on these pages says what the arithmetic did, never what a language model pays attention to.
>
> **Nothing new to install, no internet.** Check files `check151.py` to `check155.py` stand alone. Two pages (15.3 and 15.4) are typed at the bottom of your own `dials.py`, after `hw.py`. Carry **four decimals** in the weights, and round only the answer to **three**. After every weight row **add the row**.
>
> **Only this week's tools are used:** `masked_fill(mask, float("-inf"))`, `torch.tril` and `.view(B, T, H, dh).transpose(1, 2)`, plus last week's attention and the idea that **variances add**.

![Map of the 36 weeks in four term lanes with week 15, Scale, Mask, and Many Heads, highlighted in term 2 and weeks 1 to 14 solid behind it](../figures/fig-w15-0-where-this-fits.svg)
*Figure 15.0 — Where this week fits: week 15 of 36, in term 2 (memory, then attention).*

---

## ✅ Warm-Up (5 min, before anything else)

**W1.** Why do we divide the scores by `sqrt(d)` before the softmax? Finish the sentence: *wide scores make the softmax ...* ___________________________________________

**W2.** Two independent wobbles have spreads 3 and 4. The spread of their sum is ______ (not 7). Because it is the ____________ that add.

**W3.** To hide the future we put ____________ in the scores, and we do it **before / after** (circle one) the softmax, because `exp(` ______ `)` is 0 but `exp(0)` is ______ .

**W4.** A sentence of 6 words, read with the mask on, gives ______ lessons ("read these words, predict the next one").

**W5.** For `B = 1, T = 3, d = 4, H = 2`: `dh = ` ______ ; after `.view(B, T, H, dh)` the shape is ( ____ , ____ , ____ , ____ ); after `.transpose(1, 2)` it is ( ____ , ____ , ____ , ____ ).

---

## 🎲 Page 15.1 — Pen Pass 2, and the River Shouted (25 min)

**Part A. A guess, before any arithmetic (2 min).** The river question from last week gave three scores `0.1, 2.0, 0.3` on the values `10, 50, 30`, and the soft answer was `42.77`. Shout the question ten times louder: the scores become `1, 20, 3`. **My guess for the answer** (circle one): **still about 42 / about 50 / something else: ______ .** Why? ___________________________________________

**Part B. Pen Pass 2 on your class sheet, once more.** Use a fresh copy. The scores and the values come from your Week 14 sheet. Width `d = 2`, so `sqrt(2) = 1.4142` and `1 / sqrt(2) = 0.7071`. Use `exp(0) = 1.0000`, `exp(0.7071) = 2.0281`, `exp(1.4142) = 4.1132`.

```text
   scores   the [1, 0, 1]      values   V(the) = [0, 1]
            cat [0, 1, 1]               V(cat) = [1, 0]
            sat [1, 1, 2]               V(sat) = [1, 1]

STEP A  DIVIDE.  Every score divided by 1.4142 (or times 0.7071), four places.
                  key:  the      cat      sat
        the      [ ____   ____   ____ ]
        cat      [ ____   ____   ____ ]
        sat      [ ____   ____   ____ ]

STEP B  HIDE THE FUTURE.  Write  X  through every score ABOVE the diagonal.

STEP C  SHARE.  Per ROW: exp of each score that is LEFT, the row total, each exp / total.
        row the:  exps __          total ______   weights ______ ______ ______   add to ______
        row cat:  exps __ __       total ______   weights ______ ______ ______   add to ______
        row sat:  exps __ __ __    total ______   weights ______ ______ ______   add to ______

STEP D  BLEND.   output row = (w1) V(the) + (w2) V(cat) + (w3) V(sat)
        the ->  [ ______ , ______ ]
        cat ->  [ ______ , ______ ]
        sat ->  [ ______ , ______ ]                 (four places)
```

Every weight row adds to 1? ____ Every number above the diagonal in the weights is 0? ____

Why is the weight of `the` on itself **exactly** 1? ___________________________________________

Which row moved most from last week's output (`cat`: `[0.845, 0.578]`), and which dial moved it? ___________________________________________

**Part C. A two-token pass on numbers that are not from class (10 min).** Two tokens: `a = [1, 0]`, `b = [0, 1]`. `Wq` and `Wk` are both `[[1, 0], [0, 1]]`; `Wv = [[2, 0], [0, 4]]` (it doubles the first number and quadruples the second). Both dials on, `d = 2`. Use `exp(0) = 1.0000`, `exp(0.7071) = 2.0281`.

| Step | Your working |
|---|---|
| `Q`, `K` (rows `a`, `b`) | |
| `V` (rows `a`, `b`) | |
| Raw scores (2 by 2) | |
| Divided by 1.4142 | |
| After the mask (cross out the future) | |
| Weights, row `a` | |
| Weights, row `b` (exps, total, shares) | |
| Output row `a` | |
| Output row `b` (**three** places) | |

**Check it.** Save as `check151.py` and run it.

```python
# check151.py - Week 15 workbook page 15.1 Part C: a two-token pass with BOTH dials, on practice numbers.
import torch
import torch.nn.functional as F

X  = torch.tensor([[1.0, 0.0],
                   [0.0, 1.0]])                 # a, b
Wq = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
Wk = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
Wv = torch.tensor([[2.0, 0.0], [0.0, 4.0]])
Q, K, V = X @ Wq, X @ Wk, X @ Wv
d = 2
mask = torch.tril(torch.ones(2, 2))

scores = (Q @ K.transpose(-2, -1)) / d ** 0.5
print("scaled scores =", [[round(x, 4) for x in r] for r in scores.tolist()])
weights = F.softmax(scores.masked_fill(mask == 0, float("-inf")), dim=-1)
print("weights =", [[round(x, 4) for x in r] for r in weights.tolist()])
print("row sums =", [round(x, 4) for x in weights.sum(dim=-1).tolist()])
print("output =", [[round(x, 4) for x in r] for r in (weights @ V).tolist()])
```

My output row `b` by pen: ____________ ; by the machine: ____________ . Difference: ____________ (under `0.001` is fine).

Output row `a` is `[2, 0]`, the first row of `V`, with no blending at all. Why? ___________________________________________

---

## 📉 Page 15.2 — Variances Add, and a Softmax Before and After (15 min)

**Part A. Spreads of sums.** (Square each spread, add, take the square root.)

1. Spreads 5 and 12 are added. Variances: ______ and ______ ; added: ______ ; spread of the sum: ______ . (Not 17.)
2. Spreads 6 and 8: spread of the sum ______ .
3. A dot product has `d` terms, each with variance 1, all independent. Its variance is ______ and its spread is ______ . For `d = 36` the spread is ______ ; the divide that brings it back to 1 is `/` ______ . For `d = 100`: spread ______ , divide by ______ .

**Part B. The softmax, raw and divided (homework task 1).** Three scores `4, -2, 2` come from a dot product of width 16. Use `exp(4) = 54.598`, `exp(-2) = 0.135`, `exp(2) = 7.389`, and, for the divided row, `exp(1) = 2.7183`, `exp(-0.5) = 0.6065`, `exp(0.5) = 1.6487`.

```text
RAW        scores   4      -2      2
           exps     ______  ______  ______      total ______
           weights  ______  ______  ______      add to ______

DIVIDED    sqrt(16) = ____.   scores  ______  ______  ______
           exps     ______  ______  ______      total ______
           weights  ______  ______  ______      add to ______
```

Biggest weight divided by smallest: raw ______ to 1; divided ______ to 1.

Which row is still a **soft** lookup, and how can you tell without computing the answer? ___________________________________________

**Part C. Measure it, then try a new row.** Save as `check152.py` and run it. It needs numpy only.

```python
# check152.py - Week 15 workbook page 15.2: variances add, spreads measured, and a softmax before and after the divide. Numpy only.
import numpy as np

def softmax(s):
    e = np.exp(s)
    return e / e.sum()

# ---- spreads of sums: variances add ----
print("spreads 5 and 12 -> spread of the sum:", round((5 ** 2 + 12 ** 2) ** 0.5, 2))
print("spreads 6 and 8  -> spread of the sum:", round((6 ** 2 + 8 ** 2) ** 0.5, 2))

# ---- three new widths, measured (seeded) ----
rng = np.random.default_rng(0)
print("\nwidth d | spread of q.k (raw) | spread after dividing by sqrt(d)")
for d in [9, 36, 100]:
    q = rng.normal(0, 1, size=(10000, d))
    k = rng.normal(0, 1, size=(10000, d))
    dots = (q * k).sum(axis=1)
    print(f"{d:>7} | {dots.std():5.2f} | {(dots / d ** 0.5).std():5.2f}")

# ---- one row of three scores from a 36-wide dot product ----
s = np.array([6.0, 0.0, -6.0])
print("\nraw    [6, 0, -6]  ->", np.round(softmax(s), 4).tolist())
print("scaled [1, 0, -1]  ->", np.round(softmax(s / 36 ** 0.5), 4).tolist())
print("biggest / smallest, raw:", round(float(np.exp(12)), 1), " scaled:", round(float(np.exp(2)), 2))
```

| Width `d` | My prediction of the raw spread | Real raw spread | Real spread after the divide |
|:--:|:--:|:--:|:--:|
| 9 | | | |
| 36 | | | |
| 100 | | | |

The weights for the raw row `[6, 0, -6]`: ______ , ______ , ______ . Scaled: ______ , ______ , ______ . Which one would you trust to learn from, and why? ___________________________________________

![Left, bars of weights from raw scores 8, minus 2, 1 where one bar takes 0.999044, beside bars from the same scores divided by 8 that are 0.587, 0.168 and 0.245; right, bars of spread by width](../figures/fig-w15-1-why-divide.svg)
*Figure 15.1 — Dividing by the square root of the width keeps the softmax soft at every width.*

---

## 🔍 Page 15.3 — The Four Settings, and the Mask Built by Hand (20 min)

**Part A. The four settings.** Run your own `dials.py` (the one from class). Copy the three output rows of each setting, to three places. *Predict first*: which of the four settings will have the row `the` equal to `[0, 1]`? ____________

| Divide | Hide the future | Row `the` | Row `cat` | Row `sat` |
|:--:|:--:|---|---|---|
| no | no | | | |
| yes | no | | | |
| no | yes | | | |
| **yes** | **yes** | | | |

1. Which line of the table is last week's pass? ____________ Which is the module's? ____________
2. The leak test prints one `True`/`False` row without the mask and one with it. Write them: without ____________ ; with ____________ . Which word can still change the **last** row? ____________ Why can it not change the first? ___________________________________________
3. The page's two wrong masks, from `dials.py`: the row sums with the mask applied **after** the softmax are ______ , ______ , ______ ; filling the future with `0` gives the row `the` the weights ______ , ______ , ______ , so the first word is still listening to the ______ .

**Part B. A four-word mask, and two rows by hand.** *Pen first.* Write the table that `torch.tril(torch.ones(4, 4))` makes, and then the True/False table that `mask == 0` makes (True means hidden).

```text
   mask (1 = may read)                mask == 0  (True = hidden)
   [ __ __ __ __ ]                    [ ____ ____ ____ ____ ]
   [ __ __ __ __ ]                    [ ____ ____ ____ ____ ]
   [ __ __ __ __ ]                    [ ____ ____ ____ ____ ]
   [ __ __ __ __ ]                    [ ____ ____ ____ ____ ]
```

The invented scores (already divided) are:

```text
   row 1   [1, 2, 0, 3]
   row 2   [0, 1, 2, 1]
   row 3   [2, 0, 1, 0]
   row 4   [1, 1, 1, 1]
```

Cross out the future, then do the softmax of row 2 and of row 3 by hand. Use `exp(0) = 1`, `exp(1) = 2.7183`, `exp(2) = 7.3891`.

```text
row 2 left:  [ ____ , ____ ]   exps ______ ______   total ______   weights ______ ______ ______ ______
row 3 left:  [ ____ , ____ , ____ ]   exps ______ ______ ______   total ______   weights ______ ______ ______ ______
```

Row 1 has one score left, so its weights are ______ . Row 4 has four equal scores left, so its weights are ______ each.

**Check it.** Save as `check153.py` and run it.

```python
# check153.py - Week 15 workbook page 15.3: a 4-word mask, built and used. Four words, so every table is 4 x 4.
import torch
import torch.nn.functional as F

mask = torch.tril(torch.ones(4, 4))
print("mask =")
print(mask)
print("mask == 0 (True = hidden) =")
print(mask == 0)

scores = torch.tensor([[1.0, 2.0, 0.0, 3.0],
                       [0.0, 1.0, 2.0, 1.0],
                       [2.0, 0.0, 1.0, 0.0],
                       [1.0, 1.0, 1.0, 1.0]])          # INVENTED scores, already divided
hidden = scores.masked_fill(mask == 0, float("-inf"))
print("\nmasked scores =")
print(hidden)
weights = F.softmax(hidden, dim=-1)
for r in weights.tolist():
    print([round(p, 4) for p in r])
print("row sums:", [round(x, 4) for x in weights.sum(dim=-1).tolist()])
```

Did every row add to 1? ____ Which numbers in row 1 of `scores` (`2`, `0`, `3`) mattered to the answer? ____________ Why? ___________________________________________

**Part C. Break the mask (from the chapter).** This file is **deliberately** broken. Do not run it first.

```python
# DELIBERATE: masked_fill given the table of 1s and 0s instead of True and False.
import torch

scores = torch.ones(3, 3)
mask = torch.tril(torch.ones(3, 3))
print(scores.masked_fill(mask, float("-inf")))
```

My prediction (error or quiet wrong numbers?): ____________ . The fixed last line: ___________________________________________ . In my fixed mask the cells that are **True** are: ___________________________________________

![A 3 by 3 mask of ones and zeros, the attention weights with the later words struck out, and a small table showing that changing the last word moves only the last row once the mask is on](../figures/fig-w15-2-hide-the-future.svg)
*Figure 15.2 — The causal mask hides later words before the softmax, so earlier answers cannot change.*

---

## 🔀 Page 15.4 — A Second Pass With Both Dials (15 min)

**Prediction first (homework task 2).** Same `X`, `Wk` and `Wv` as the class, but the question table is now `Wq = [[0, 0], [1, 0]]`. Last week, with this table, the row `the` came out as `[0.333, 0.333, 0.333]`. **This week, with the mask on, the row `the` of the weights becomes:** ____________ **because** ___________________________________________

```text
Q  = X times Wq        the [ __ , __ ]   cat [ __ , __ ]   sat [ __ , __ ]
K  = X (Wk is the identity)               V = X times Wv:   the [0, 1]  cat [1, 0]  sat [1, 1]

raw scores   (row i of Q dot row j of K)
        key:  the  cat  sat
  the        [ __   __   __ ]
  cat        [ __   __   __ ]
  sat        [ __   __   __ ]

STEP A  divide by 1.4142 (four places)
  the        [ ______ ______ ______ ]
  cat        [ ______ ______ ______ ]
  sat        [ ______ ______ ______ ]

STEP B  cross out the future (the upper triangle)

STEP C  share, row by row (exp(0) = 1.0000, exp(0.7071) = 2.0281)
  row the:  exps ______              total ______   weights ______ ______ ______
  row cat:  exps ______ ______       total ______   weights ______ ______ ______
  row sat:  exps ______ ______ ______ total ______   weights ______ ______ ______    add to ______

STEP D  blend (three places)
  the ->  [ ______ , ______ ]
  cat ->  [ ______ , ______ ]
  sat ->  [ ______ , ______ ]
```

Was my prediction right? ____ If not, what did I forget? ___________________________________________

**The computer check.** Type `hw.py` from the chapter at the **bottom** of `dials.py`, and run the whole file. Copy the lines:

```text
H2 weights (both dials):   row the ____________   row cat ____________   row sat ____________
H2 output:                 row the ____________   row cat ____________   row sat ____________
```

Biggest gap between my pen output and the machine's: ____________ . (Over `0.001`? Find out which is wrong before you go on.)

**Extension (5 min).** *Predict first.* Same question table. If you turn the **divide off** and leave the mask on, the row `cat` of the weights is ____________ ; if you turn the **mask off** and leave the divide on, the row `the` of the weights is ____________ . Now type this below the `hw.py` lines in `dials.py`.

```python
# ext154.py - Week 15 workbook page 15.4 extension. (Type at the bottom of dials.py, after hw.py.)
d = 2                                              # hw.py's last block set d = 12; put the real width back
w, out = attend_dials(False, True)                 # still the page 15.4 question table. Divide OFF, hide the future ON
print("hide only, weights =")
rows(w)
print("hide only, output =")
rows(out)
w, out = attend_dials(True, False)                 # divide ON, hide the future OFF
print("divide only, weights =")
rows(w)
```

Real lines: hide only, row `cat` of the weights ____________ ; divide only, row `the` of the weights ____________ .

The first line of the extension is `d = 2`. In one sentence, what would have happened to `attend_dials` if I had left it out? ___________________________________________

---

## 🧩 Page 15.5 — The Shapes of Heads, and the Computer Check (10 min)

**Part A. Homework task 3, by hand.** For 2 sentences of 5 words, width 12 and 3 heads (`B = 2, T = 5, d = 12, H = 3`):

| Question | My answer |
|---|---|
| `dh = d // H` | |
| Shape after `.view(B, T, H, dh)` | |
| Shape after `.transpose(1, 2)` | |
| Shape of the score table `q @ k.transpose(-2, -1)` | |
| Knobs in the three tables (`3 x d x d`) | |
| The divide is by the root of ______ , which is | |

Does `H` appear in the knob count? ____ Why not? ___________________________________________

`hw.py` printed `H3 per-head tensor:` ____________ and `scores:` ____________ . Do they match my table? ____

**Part B. The same questions on new numbers.** For `B = 3, T = 4, d = 20, H = 5` write your answers, *then* run the file.

| Question | My answer | The file said |
|---|---|---|
| `dh` | | |
| Shape after `.view(B, T, H, dh)` | | |
| Shape after `.transpose(1, 2)` | | |
| Shape of the score table | | |
| Knobs in the three tables | | |
| The divide | | |

```python
# check155.py - Week 15 workbook page 15.5: the shapes of heads on NEW numbers. Random, seed 0, nothing trained.
import torch

B, T, d, H = 3, 4, 20, 5
dh = d // H
torch.manual_seed(0)
x = torch.randn(B, T, d)
cut = x.view(B, T, H, dh)
heads = cut.transpose(1, 2)
print("dh =", dh)
print("after view(B,T,H,dh):", tuple(cut.shape))
print("after transpose(1,2):", tuple(heads.shape))
print("score table:", tuple((heads @ heads.transpose(-2, -1)).shape))
print("knobs in three d x d tables:", 3 * d * d)
print("divide by sqrt(dh) =", round(dh ** 0.5, 3), " not sqrt(d) =", round(d ** 0.5, 3))
```

**Extension (for the fast student).** *Predict first.* With `d = 8` and `H = 6`, what is `dh`, and does `view` work? ____________ This file is **deliberately** broken; run it and copy the last line.

```python
# DELIBERATE: width 8 cut into 6 heads. 8 does not divide by 6.
import torch

B, T, d, H = 1, 3, 8, 6
dh = d // H
print("dh =", dh, "  H x dh =", H * dh, "  d =", d)
x = torch.zeros(B, T, d)
print(x.view(B, T, H, dh).shape)
```

Last line: ___________________________________________ . The habit that would catch this before the run: check that `H x dh = ` ______ . What happens to `dh` and to the knob count if `d = 12` and `H = 6`? ___________________________________________

---

## 🐞 Page 15.6 — Break It on Purpose (25 min)

This page is for practising how to find a bug by predicting before you run.

**Each program below is deliberately broken.** Do **not** run it first. For each, write **(i)** what the bug is, **(ii)** what you think happens when it runs (an error, or quietly wrong numbers), **(iii)** the fixed line, and **(iv)** a *check* that would have caught it. *Then* run it. Bugs A to D and F use scores that are **already divided**.

```python
# DELIBERATE BUG 15.6-A: the future "hidden" with 0 instead of -inf. (Scores are already divided.)
import torch
import torch.nn.functional as F

scores = torch.tensor([[1.0, 0.0, 2.0],
                       [0.0, 1.0, 0.0],
                       [1.0, 1.0, 1.0]])
mask = torch.tril(torch.ones(3, 3))
hidden = scores.masked_fill(mask == 0, 0.0)
weights = F.softmax(hidden, dim=-1)
for r in weights.tolist():
    print([round(p, 4) for p in r])
print("row sums:", [round(x, 4) for x in weights.sum(dim=-1).tolist()])
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________ The row sums are all 1. Why does that check not catch it? ___________________

```python
# DELIBERATE BUG 15.6-B: the mask applied AFTER the softmax.
import torch
import torch.nn.functional as F

scores = torch.tensor([[1.0, 0.0, 2.0],
                       [0.0, 1.0, 0.0],
                       [1.0, 1.0, 1.0]])
mask = torch.tril(torch.ones(3, 3))
weights = F.softmax(scores, dim=-1) * mask
for r in weights.tolist():
    print([round(p, 4) for p in r])
print("row sums:", [round(x, 4) for x in weights.sum(dim=-1).tolist()])
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________

```python
# DELIBERATE BUG 15.6-C: the mask the wrong way round.
import torch
import torch.nn.functional as F

scores = torch.tensor([[1.0, 0.0, 2.0],
                       [0.0, 1.0, 0.0],
                       [1.0, 1.0, 1.0]])
mask = torch.tril(torch.ones(3, 3))
hidden = scores.masked_fill(mask == 1, float("-inf"))
print(hidden)
print(F.softmax(hidden, dim=-1))
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________ What does a `nan` in a weight row tell you? ___________________

```python
# DELIBERATE BUG 15.6-D: view(B, H, T, dh) where view(B, T, H, dh) then transpose(1, 2) was needed.
import torch

B, T, d, H = 1, 2, 4, 2
dh = d // H
x = torch.tensor([[[1.0, 2.0, 3.0, 4.0],
                   [10.0, 20.0, 30.0, 40.0]]])           # 2 words, 4 numbers each
good = x.view(B, T, H, dh).transpose(1, 2)
bad = x.view(B, H, T, dh)
print("good:", tuple(good.shape), " bad:", tuple(bad.shape))
print("head 0, good:", good[0, 0].tolist())
print("head 0, bad: ", bad[0, 0].tolist())
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________ Why can a shape check not catch this one? ___________________

```python
# DELIBERATE BUG 15.6-E (loud): a mask made for 3 words, used on a sentence of 6.
import torch

mask = torch.tril(torch.ones(3, 3))
scores = torch.zeros(1, 2, 6, 6)                         # (B, H, T, T) with T = 6
print(scores.masked_fill(mask == 0, float("-inf")).shape)
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________ Where do the numbers `3` and `6` in the message come from? ___________________

```python
# DELIBERATE BUG 15.6-F: divided by d, not by the square root of d. Width 16, eight labels, seeded.
import numpy as np

rng = np.random.default_rng(0)
d = 16
q = rng.normal(0, 1, size=(2000, 8, d))
k = rng.normal(0, 1, size=(2000, 8, d))
s = (q * k).sum(axis=2)
sc = s / d
w = np.exp(sc) / np.exp(sc).sum(axis=1).reshape(-1, 1)
print("spread of the scores:", round(sc.std(), 3))
print("average biggest weight:", round(w.max(axis=1).mean(), 3))
```

(i) ___________________ (ii) ___________________ (iii) ___________________ (iv) ___________________ Eight equal weights would have a biggest weight of ______ . How close is the printed one?

**After you have written all six predictions, run them.** Save each as its own file (`bad_a.py` ... `bad_f.py`) and copy the **last line** (for A and B copy the first three rows; for C and D copy every line that prints numbers; for F copy both lines).

| Bug | Real output | Did my prediction match? |
|:--:|---|:--:|
| A | | |
| B | | |
| C | | |
| D | | |
| E | | |
| F | | |

---

## 📓 Page 15.7 — The Bug Log

This page is for recording what went wrong this week and how you found it.

**Entry 1: the one row that would not add to 1.** Which row, which page, and what was wrong with it? (If none, write the first number that was wrong on any page, and how you found it.) ___________________________________________

**Entry 2: two right answers.** On page 15.1 the `sat` output can come out `0.7517` or `0.7518`, and on page 15.1 Part C the row `b` can come out `0.6604` or `0.6605`. In your own words, why are both correct? ___________________________________________

**Entry 3: the silent ones.** Bugs A, B, C, D and F ran **without an error**. For each, write the property that must be true and which the bug broke.

| Bug | The property that must be true | What the output showed instead |
|:--:|---|---|
| A | | |
| B | | |
| C | | |
| D | | |
| F | | |

**Entry 4: a bug I mispredicted** (skip if you got all six).

| What I predicted | What actually happened | The sentence that would have told me |
|---|---|---|
| | | |

**Entry 5: the rule I will follow next week.** One sentence (a habit, not a fact): ___________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (do this last, from memory)

Seven things, no scrolling up. Tick only if you could do it **now**.

- ☐ Show that a softmax over wide scores freezes, and say what lookup it has turned into.
- ☐ Say what "variances add" means with spreads 3 and 4, and why a dot product of `d` terms has spread `sqrt(d)`.
- ☐ Do one attention pass by hand with both dials, and add every weight row.
- ☐ Write the mask in torch (`torch.tril`, then `masked_fill`) and say why `-inf`, and why before the softmax.
- ☐ Say why a masked pass gives `T - 1` lessons, and what test shows the future is hidden.
- ☐ Cut a width into heads with `.view(B, T, H, dh).transpose(1, 2)` and name every shape on the way.
- ☐ Say what this week did **not** do (nothing was trained, nothing glued back, no layers stacked).

**Ticks:** ______ / 7 . **The one I could not tick, and when I will redo it:** ___________________________________________

**Next week.** Week 16 is **Where Am I? Positions and the Transformer Block** (a transformer is a model built from blocks that each contain attention; you build one by Week 17). Attention as it stands cannot tell the order of the words, so you will add a **place** to every word. You will also glue the heads back together and count the knobs in a whole block. **Bring your `dials.py` and `heads.py`.**

---

## ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact to the places stated. The last digit of a torch number can differ on another CPU or PyTorch build, and the digits of numbers measured from random draws can move in the third decimal. **Mark the method, the row sums and the zeros above the diagonal, not the last digit.**

### Warm-Up

**W1.** ... **freeze onto one word** (the biggest weight goes to nearly 1 and the rest to nearly 0), so the soft lookup becomes a hard one. **W2.** **5**; the **variances** add (`9 + 16 = 25`). **W3.** `-inf`; **before**; `exp(-inf)` is **0**, but `exp(0)` is **1**. **W4.** **5** lessons (`T - 1`). **W5.** `dh = 2`; `(1, 3, 2, 2)`; `(1, 2, 3, 2)`.

### Page 15.1

**Part A.** The answer is **50.0**. The weights for `1, 20, 3` are `0, 1, 0` (to six places), so the soft lookup has turned into the hard one of Week 14. Any reason that says "one score towers over the others, so the softmax puts everything on it" is right.

**Part B (the class example).**

| | |
|---|---|
| Scaled scores (step A; step B crosses out the upper triangle) | the `[0.7071, X, X]`, cat `[0.0000, 0.7071, X]`, sat `[0.7071, 0.7071, 1.4142]` |
| Exps of the scores that are left | the `[2.0281]` (total 2.0281) · cat `[1.0000, 2.0281]` (total **3.0281**) · sat `[2.0281, 2.0281, 4.1132]` (total **8.1694**) |
| Weights, four places | the `[1.0000, 0, 0]`, cat `[0.3302, 0.6698, 0]`, sat `[0.2483, 0.2483, 0.5035]` |
| Output, four places | the `[0.0000, 1.0000]`, cat `[0.6698, 0.3302]`, sat `[0.7517, 0.7517]` |
| Output, three places | the `[0.000, 1.000]`, cat `[0.670, 0.330]`, sat `[0.752, 0.752]` |

Every weight row adds to 1 and everything above the diagonal is 0. `the` has only one score left, and a softmax of one number is 1. Carrying **three** places in the weights gives `sat` `0.751` (that row of weights adds to `0.999`), and adding the rounded four-place weights `0.2483 + 0.5035` gives `0.7518`: accept all three. The row that moved most is `cat` (or `the`: `[0.578, 0.845]` became `[0, 1]`); hiding the future did it, because `sat` was removed from what `cat` can read. Accept any sentence that names a row, a number and a dial.

**Part C (two tokens).**

| Step | Answer |
|---|---|
| `Q`, `K` | both are `X`: `a [1, 0]`, `b [0, 1]` |
| `V` | `a [2, 0]`, `b [0, 4]` |
| Raw scores | `[[1, 0], [0, 1]]` |
| Divided | `[[0.7071, 0.0000], [0.0000, 0.7071]]` |
| After the mask | row `a` `[0.7071, X]`; row `b` `[0.0000, 0.7071]` |
| Weights, row `a` | `[1.0000, 0]` |
| Weights, row `b` | exps `1.0000, 2.0281`, total `3.0281`, weights `[0.3302, 0.6698]` |
| Output row `a` | `[2.0000, 0.0000]` |
| Output row `b` | `[0.660, 2.679]` |

The machine printed:

```text
scaled scores = [[0.7071, 0.0], [0.0, 0.7071]]
weights = [[1.0, 0.0], [0.3302, 0.6698]]
row sums = [1.0, 1.0]
output = [[2.0, 0.0], [0.6605, 2.679]]
```

By pen with the rounded weights `0.3302 x 2 = 0.6604`; the machine kept every digit and printed `0.6605`. The difference is rounding, not a mistake. Row `a` is `[2, 0]` because the mask leaves `a` only itself to read, so its weight on itself is 1, and 1 times the first row of `V` is that row.

### Page 15.2

**Part A.** 1. Variances `25` and `144`; added `169`; spread **13**. 2. Variances `36` and `64`; added `100`; spread **10**. 3. Variance **`d`**; spread **`sqrt(d)`**. For `d = 36`: spread **6**, divide by **6**. For `d = 100`: spread **10**, divide by **10**.

**Part B.**

```text
RAW        scores   4        -2       2
           exps     54.598   0.135    7.389       total 62.122 (62.123 with more digits)
           weights  0.8789   0.0022   0.1189      add to 1.0000

DIVIDED    sqrt(16) = 4.   scores   1       -0.5     0.5
           exps     2.7183   0.6065   1.6487        total 4.9735
           weights  0.5465   0.1220   0.3315        add to 1.0000
```

Biggest to smallest: raw **403 to 1**; divided **4.5 to 1** (`exp(6) = 403.4` and `exp(1.5) = 4.48`; by pen from the weights `0.8789 / 0.0022` gives `399.5`, which is off only because `0.0022` is rounded, so accept any answer near 400). The **divided** row is still soft: the three weights are all of a useful size, and no weight is below `0.1`. The raw row has put `0.88` on one word and `0.002` on another.

**Part C.** The machine printed:

```text
spreads 5 and 12 -> spread of the sum: 13.0
spreads 6 and 8  -> spread of the sum: 10.0

width d | spread of q.k (raw) | spread after dividing by sqrt(d)
      9 |  3.03 |  1.01
     36 |  5.99 |  1.00
    100 | 10.00 |  1.00

raw    [6, 0, -6]  -> [0.9975, 0.0025, 0.0]
scaled [1, 0, -1]  -> [0.6652, 0.2447, 0.09]
biggest / smallest, raw: 162754.8  scaled: 7.39
```

The predicted raw spreads are `3, 6, 10` (the square roots of `9, 36, 100`). The raw row `[6, 0, -6]` freezes onto the first word (`0.9975`) and the third gets about `0.000006`, which prints as `0.0`; the scaled row is `0.6652, 0.2447, 0.0900`. Trust the scaled one: every word still has a share, so a small change in a score can still change the answer, and so something can be learned from it.

### Page 15.3

**Part A (from `dials.py`).** Prediction: the two settings with the mask on (**hide the future = yes**), because only the mask removes the other words from row `the`.

| Divide | Hide the future | Row `the` | Row `cat` | Row `sat` |
|:--:|:--:|---|---|---|
| no | no | `[0.578, 0.845]` | `[0.845, 0.578]` | `[0.788, 0.788]` |
| yes | no | `[0.599, 0.802]` | `[0.802, 0.599]` | `[0.752, 0.752]` |
| no | yes | `[0.000, 1.000]` | `[0.731, 0.269]` | `[0.788, 0.788]` |
| **yes** | **yes** | `[0.000, 1.000]` | `[0.670, 0.330]` | `[0.752, 0.752]` |

1. Last week's pass is the **no / no** line; the module's is the **yes / yes** line. 2. Without the mask `[True, True, True]`; with it `[False, False, True]`. Only the **last** word can change the last row (its own row reads it); the first row can read only the first word, which did not change. 3. After the softmax the row sums are `0.4011, 0.5989, 1.0`; filling with `0` gives `0.5035, 0.2483, 0.2483`, so the first word is still listening to the **later words** (`exp(0) = 1`, which is an ordinary weight, not "nothing").

**Part B.** The mask: rows `[1, 0, 0, 0]`, `[1, 1, 0, 0]`, `[1, 1, 1, 0]`, `[1, 1, 1, 1]`. `mask == 0`: the upper triangle is `True`, everything else `False` (row 1 `[False, True, True, True]`, row 2 `[False, False, True, True]`, row 3 `[False, False, False, True]`, row 4 all `False`). Row 2 left `[0, 1]`: exps `1.0000, 2.7183`, total `3.7183`, weights `[0.2689, 0.7311, 0, 0]`. Row 3 left `[2, 0, 1]`: exps `7.3891, 1.0000, 2.7183`, total `11.1074`, weights `[0.6652, 0.0900, 0.2447, 0]`. Row 1 weights `[1, 0, 0, 0]`; row 4 weights `0.25` each. The machine printed:

```text
mask =
tensor([[1., 0., 0., 0.],
        [1., 1., 0., 0.],
        [1., 1., 1., 0.],
        [1., 1., 1., 1.]])
mask == 0 (True = hidden) =
tensor([[False,  True,  True,  True],
        [False, False,  True,  True],
        [False, False, False,  True],
        [False, False, False, False]])

masked scores =
tensor([[1., -inf, -inf, -inf],
        [0., 1., -inf, -inf],
        [2., 0., 1., -inf],
        [1., 1., 1., 1.]])
[1.0, 0.0, 0.0, 0.0]
[0.2689, 0.7311, 0.0, 0.0]
[0.6652, 0.09, 0.2447, 0.0]
[0.25, 0.25, 0.25, 0.25]
row sums: [1.0, 1.0, 1.0, 1.0]
```

Every row adds to 1. In row 1 of `scores`, only the first number, `1`, mattered: the others (`2`, `0`, `3`) are in the future and were replaced by `-inf` before the softmax, so even the large `3` has no effect.

**Part C.** The prediction is an **error** (the mask is floats). The error is `RuntimeError: masked_fill_ only supports boolean masks, but got mask with dtype float`. The fix is `print(scores.masked_fill(mask == 0, float("-inf")))`. The True cells are the **upper triangle**, above the diagonal: `(row 1, column 2)`, `(row 1, column 3)` and `(row 2, column 3)` for 3 words, the future.

### Page 15.4

Prediction: `[1, 0, 0]`, because the mask leaves the row `the` only itself, and a softmax of one number is 1. (Last week, with no mask, its question was all zeros so every score was 0 and it averaged the three words.)

| | |
|---|---|
| `Q` | the `[0, 0]`, cat `[1, 0]`, sat `[1, 0]` |
| Raw scores | the `[0, 0, 0]`, cat `[1, 0, 1]`, sat `[1, 0, 1]` |
| Step A (divided) | the `[0.0000, 0.0000, 0.0000]`, cat `[0.7071, 0.0000, 0.7071]`, sat `[0.7071, 0.0000, 0.7071]` |
| Step C | row the exps `1.0000` (total 1.0000); row cat left `[0.7071, 0.0000]` exps `2.0281, 1.0000` (total **3.0281**); row sat exps `2.0281, 1.0000, 2.0281` (total **5.0562**) |
| Weights | the `[1, 0, 0]`, cat `[0.6698, 0.3302, 0]`, sat `[0.4011, 0.1978, 0.4011]` |
| Output (three places) | the `[0.000, 1.000]`, cat `[0.330, 0.670]`, sat `[0.599, 0.802]` |

The machine printed (from `hw.py`):

```text
H2 weights (both dials):
[1.0, 0.0, 0.0]
[0.6698, 0.3302, 0.0]
[0.4011, 0.1978, 0.4011]
H2 output:
[0.0, 1.0]
[0.3302, 0.6698]
[0.5989, 0.8022]
```

Gaps between pen (three places) and machine should be under `0.001`. The extension prediction: with the divide off and the mask on, the row `cat` is `[0.7311, 0.2689, 0]` (scores `1, 0` give `e / (e + 1)`); with the mask off and the divide on, the row `the` is `[0.3333, 0.3333, 0.3333]` (all scores 0). The machine printed:

```text
hide only, weights =
[1.0, 0.0, 0.0]
[0.7311, 0.2689, 0.0]
[0.4223, 0.1554, 0.4223]
hide only, output =
[0.0, 1.0]
[0.2689, 0.7311]
[0.5777, 0.8446]
divide only, weights =
[0.3333, 0.3333, 0.3333]
[0.4011, 0.1978, 0.4011]
[0.4011, 0.1978, 0.4011]
```

Without `d = 2`, `d` would still be `12` (hw.py's shape block set it), so `attend_dials` would divide by `sqrt(12)` instead of `sqrt(2)`, and print the wrong weights **with no error**. For the page 15.4 table that gives row `cat` `[0.5717, 0.4283, 0]` and row `sat` `[0.3637, 0.2725, 0.3637]`, instead of `[0.6698, 0.3302, 0]` and `[0.4011, 0.1978, 0.4011]`.

### Page 15.5

**Part A.** `dh = 12 // 3 =` **4**; after `.view(B, T, H, dh)`: **(2, 5, 3, 4)**; after `.transpose(1, 2)`: **(2, 3, 5, 4)**; score table: **(2, 3, 5, 5)**; knobs `3 x 12 x 12 =` **432**; the divide is by the root of **`dh`**, `sqrt(4) = 2.0` (not `sqrt(12) = 3.464`). `H` does not appear in the knob count: each table is still `d x d`; the heads are only slices of its output. `hw.py` printed `H3 per-head tensor: (2, 3, 5, 4)  scores: (2, 3, 5, 5)`.

**Part B.** The machine printed:

```text
dh = 4
after view(B,T,H,dh): (3, 4, 5, 4)
after transpose(1,2): (3, 5, 4, 4)
score table: (3, 5, 4, 4)
knobs in three d x d tables: 1200
divide by sqrt(dh) = 2.0  not sqrt(d) = 4.472
```

So `dh = 20 // 5 = 4`; `(3, 4, 5, 4)`; `(3, 5, 4, 4)`; `(3, 5, 4, 4)` for the score table; `3 x 20 x 20 = 1200`; the divide is `2.0`.

**Extension.** With `d = 8`, `H = 6`: `8 // 6 = 1`, and `view` fails. The machine printed:

```text
dh = 1   H x dh = 6   d = 8
```

then the traceback ended with

```text
RuntimeError: shape '[1, 3, 6, 1]' is invalid for input of size 24
```

(There are 24 numbers, and `1 x 3 x 6 x 1` is only 18.) The habit: check that `H x dh = d` (here `6` is not `8`). With `d = 12` and `H = 6`, `dh = 2` and the knob count is unchanged at `432`.

### Page 15.6

**15.6-A (silent).** (i) The future was filled with `0`, but `exp(0) = 1` is an ordinary weight: a score of 0 is "average", not "nothing". Use `float("-inf")`. (ii) It runs; the future is still heard. The printed output:

```text
[0.5761, 0.2119, 0.2119]
[0.2119, 0.5761, 0.2119]
[0.3333, 0.3333, 0.3333]
row sums: [1.0, 1.0, 1.0]
```

(iii) `hidden = scores.masked_fill(mask == 0, float("-inf"))`. With the fix, the weights are `[1, 0, 0]`, `[0.2689, 0.7311, 0]` and `[0.3333, 0.3333, 0.3333]`. (iv) Check that everything above the diagonal of the weights is **exactly 0**. The row sums are 1 because the softmax always makes them so; they say nothing about **where** the weight went.

**15.6-B (silent).** (i) The softmax came first and the mask was multiplied in afterwards, so the zeroed weights are not shared back out. (ii) It runs; the zeros are in the right places, but the rows no longer add to 1. The printed output:

```text
[0.2447, 0.0, 0.0]
[0.2119, 0.5761, 0.0]
[0.3333, 0.3333, 0.3333]
row sums: [0.2447, 0.7881, 1.0]
```

(iii) Mask the **scores**, then softmax: `F.softmax(scores.masked_fill(mask == 0, float("-inf")), dim=-1)`. (iv) `weights.sum(dim=-1)` must be all ones.

**15.6-C (silent, prints `nan`).** (i) `mask == 1` is True on the **allowed** cells, so this hides the past and keeps the future. (ii) It runs; the last row has nothing left to attend to. The printed output:

```text
tensor([[-inf, 0., 2.],
        [-inf, -inf, 0.],
        [-inf, -inf, -inf]])
tensor([[0.0000, 0.1192, 0.8808],
        [0.0000, 0.0000, 1.0000],
        [   nan,    nan,    nan]])
```

(iii) `mask == 0`. (iv) Print the hidden scores and look at the **upper** triangle: it must be the `-inf` one; or check that no weight is `nan`. A `nan` in a weight row tells you that a row had **nothing** to attend to (a softmax of nothing is `0 / 0`), and a `nan` spreads to everything it touches. Notice that rows 1 and 2 look like legal weights.

**15.6-D (silent).** (i) `view(B, H, T, dh)` cuts the data in the order it is stored, so one "word" of a head is made of pieces of different words. The right way is `view(B, T, H, dh)` (cut each word), then `.transpose(1, 2)`. (ii) It runs, and both shapes are `(1, 2, 2, 2)`. The printed output:

```text
good: (1, 2, 2, 2)  bad: (1, 2, 2, 2)
head 0, good: [[1.0, 2.0], [10.0, 20.0]]
head 0, bad:  [[1.0, 2.0], [3.0, 4.0]]
```

(iii) `bad = x.view(B, T, H, dh).transpose(1, 2)`. (iv) Print head 0 of a table you can read: it must hold the **first two numbers of every word** (`[1, 2]` and `[10, 20]`). A shape check cannot catch it because both versions have the same shape; only the order of the numbers inside differs.

**15.6-E (loud).** (i) The mask was built for 3 words and the scores are `6 x 6`. (ii) An error. The printed output (last lines):

```text
Traceback (most recent call last):
  File "/private/tmp/wb15/bad_e.py", line 6, in <module>
    print(scores.masked_fill(mask == 0, float("-inf")).shape)
RuntimeError: The size of tensor a (3) must match the size of tensor b (6) at non-singleton dimension 3
```

(The path on your machine will differ.) (iii) Build the mask from `T`: `mask = torch.tril(torch.ones(T, T))` with `T = 6`. (iv) Print `mask.shape` and `scores.shape[-2:]`; they must be equal. The `3` is the mask's size and the `6` is the last axis of the scores (dimension 3, counting from 0).

**15.6-F (silent).** (i) The divide is by `d = 16`; it should be by `sqrt(d) = 4`. The spread of a sum of `d` terms is `sqrt(d)`, not `d`. (ii) It runs; the scores are squashed too flat. The printed output:

```text
spread of the scores: 0.252
average biggest weight: 0.176
```

(iii) `sc = s / d ** 0.5`. With the fix the same file prints a spread of `1.007` and an average biggest weight of `0.371`. (iv) The spread of the scores (`sc.std()`) must be near **1** after the divide; and the biggest weight in a row of 8 should be about `0.37`, nowhere near `0.125`. Eight equal weights would have `0.125`, and `0.176` is nearly that: the lookup has gone **flat** (Bug 15.6-F), where forgetting the divide entirely makes it **freeze**.

### Page 15.7 and Self-Check

Your own words. A good **Entry 2** says: the weights are rounded to four places before the blend (`0.3302` instead of `0.330197...`), so the pen number and the machine's can differ in the last place, and neither is a mistake. A good **Entry 3** uses the property for each: A, the future gets exactly 0 (upper triangle of the weights); B, every row adds to 1; C, no `nan`, and the upper triangle is what gets hidden; D, head 0 holds the first numbers of **each** word; F, the scores have a spread near 1 after the divide. A good **Entry 5** is short and about a habit ("print the upper triangle of the weights", "check `H x dh = d` before I `view`", "after any mask, add the row").

**Self-Check:** if you could tick fewer than five, redo pages 15.1 and 15.3 first. Week 16 builds on this exact pass (with a mask and with heads) and will not stop to redo it.
