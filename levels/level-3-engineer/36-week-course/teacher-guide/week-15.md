# Week 15 — Rolling Downhill: Descent From Scratch

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Student Guide](../student-guide/week-15.md) · [Workbook](../workbook/week-15.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — the week the student writes `fit()` |
| **Big idea** | Training is a **loop**: get the slope for every knob, step every knob a little way **against** its slope, repeat. That loop is what `fit()` was doing all along. |
| **New vocabulary** | gradient · epoch · step / iteration · divergence · convergence criterion · batch / mini-batch / stochastic |
| **New maths** | **The gradient: one slope per knob, collected in a list** — and the update `w ← w − lr × slope` applied to all of them at once, **worked for three rounds on paper before any code.** |
| **New syntax** | `(X * w).sum(axis=1)` · `w -= lr * grad` · `ax.set_yscale("log")` |
| **Dataset** | `make_classification(n_samples=400, n_features=2, n_informative=2, n_redundant=0, random_state=0)` — 400 rows, generated offline instantly. Plus **four hand-typed delivery rows** for the paper work. |
| **Materials** | Printed workbook pages 15.1–15.8 · **the four-round update table blown up on the board before the lesson** · a calculator per pair · the Bug Log · `0.6931` still on the wall from last week |
| **Tech needed** | Laptop with Python 3, numpy, matplotlib, scikit-learn. **Nothing to install, nothing to download.** matplotlib writes to a file — no window ever opens. |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `three_rounds.py` **instant**. `descent.py` — 1,500 epochs across three learning rates — **under 2 seconds.** `match.py`, 20,000 epochs, **about 1 second.** `curves.py` including both plots, **about 1 second.** **Nothing in this lab takes longer than you can hold your breath.** |

> **⚠️ Watch out:** the whole lab rests on **three rounds of arithmetic done on paper before anybody opens an editor.** If the class types the loop first, the loop is a spell — twenty-five lines that produce a number, with no way to tell a right number from a wrong one. If they do three rounds by hand first, then every line of code has a hand-computed number sitting beside it, and the loop is a *transcription*. **Paper first. Non-negotiable.**

---

## 🎯 Lesson Objectives

By the end of the lab the student can:

1. **Implement logistic regression trained by their own numpy gradient descent** in about 25 lines, with no framework anywhere near the training loop.
2. **Apply `w ← w − lr × slope` to three weights at once**, and show three rounds of every intermediate number on paper.
3. **Plot three learning rates on one loss curve** and match each to its name: **too small**, **converged**, **diverged**.
4. **Match their own final weights against scikit-learn's to three decimal places**, and say what it means that they agree.

Observable evidence: a completed four-round table on workbook page 15.2 with every `z`, `p`, error, slope and update shown; a `descent.png` with a log-scale left panel carrying three named curves; a printed side-by-side weight comparison; and a diagnosis of four supplied loss curves with a one-line fix for each.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

There is exactly one new mathematical idea this week and it is **"one slope per knob, in a list"**. Everything else is Week 12's slope, Week 13's sigmoid and Week 14's loss, arranged in a loop. Twenty-five minutes with this section is enough; if you only have twelve, read §3, §4 and §5.

### 1. Where we are: three weeks arriving at once

This is the week the term has been building towards, and it is worth saying so out loud in class.

| Week | What it gave us | Where it lands today |
|---|---|---|
| **12** | how to measure how steep a curve is at one point, by nudging | **the slope** |
| **13** | how to turn a raw score into a probability with the sigmoid | **the forward pass** |
| **14** | how to price a set of probabilities with log loss | **the number we roll downhill on** |

Put them in a loop and you have `fit()`. **Not a simplified version of `fit()` — the actual algorithm**, which is why the final weights are going to match scikit-learn's.

### 2. What the loop is, in five lines of English

Before any arithmetic, here is the whole algorithm. Read it out loud; it is genuinely this short.

```
1. start with every weight at zero
2. work out the probability for every row            (Week 13)
3. work out the loss                                 (Week 14)
4. work out, for each weight, which way is downhill  (Week 12)
5. step each weight a little way downhill.  go to 2
```

Steps 2 and 3 the student has already built. Step 5 is one line of code. **Step 4 is the only genuinely new thing**, and it turns out to be almost embarrassingly easy — which is the surprise of the week.

### 3. The gradient: one slope per knob

Week 12 measured the slope of a curve that had **one** input. Nudge `w`, see what happens to the loss, divide. Fine.

But our model has **three** knobs: `w1`, `w2` and the bias `b`. So "which way is downhill" is not one number. It is **three** numbers — one per knob.

> **gradient** — the collection of all the slopes, one per knob, kept in a list. `[−0.375, +0.125, 0.000]` is a gradient. It answers "if I nudge this knob, which way does the loss go?" once for every knob.

🍕 **The analogy, and it carries the week.** You are standing on a foggy hillside and you cannot see the valley. But you can feel the ground under your feet. Step your left foot ten centimetres north: it goes **down** three centimetres. Step ten centimetres east: it goes **up** one centimetre. So north is downhill and east is uphill. **You do not need a map of the hill; you only need the ground right under you** — and you need it in every direction you could step. The gradient is that: one measurement per direction.

**Now the formula, and this is the surprise.** For logistic regression with log loss, the slope for weight `j` turns out to be:

```
slope for weight j  =  the average of (prediction − truth) × (feature j)
```

**That is it. Error times feature, averaged.** No exponentials. No logarithms. No sigmoid derivative. Nothing left over.

> **🔢 The maths, slowly:** this is startling and you should let the class be startled by it. Last week's loss was full of logarithms; the week before, the model was full of exponentials. When you work out the slope of one composed with the other, **the messy parts cancel exactly.** What survives is `prediction − truth`, multiplied by whichever feature fed that weight, averaged over the rows. **This cancellation is the real reason sigmoid and log loss are always paired** — somebody noticed, a hundred years ago, that these two particular functions were built for each other. You do not need to show the cancellation and neither does the student. **You do need to say that it happened, and that it is why.**

**And the slope for the bias?** The bias is not multiplied by any feature — it is added to every row unchanged. So it is the same formula with the feature set to 1:

```
slope for the bias  =  the average of (prediction − truth)
```

**Read the formula as blame, because that is what it is.**

- Model said `0.9`, truth was `1` → error is `−0.1`. Small error, small push.
- Model said `0.9`, truth was `0` → error is `+0.9`. **Big error, big push.**
- And that push is multiplied by the feature, so **rows where the feature was large get corrected the most.** A row with 8 orders in the oven has more say about `w1` than a row with 1.

![One slope per knob](../figures/fig-w15-1-gradient-one-slope-per-knob.svg)
*Figure 15.1 — One slope per knob. Four rows, three knobs, three slopes, and the sum for `w1` written out in full.*

### 4. The update rule, and the minus sign that is the whole algorithm

> **the update rule** — `w ← w − lr × (that knob's slope)`, done to every knob, then repeat.

> **learning rate (`lr`)** — how big a step to take. A small positive number, usually between 0.001 and 1.

**The minus sign is the entire idea and you should point at it.** The slope tells you which way is **uphill**. You want to go **down**. So you step the opposite way. That is the whole algorithm; everything else is bookkeeping.

Work one update out loud. Suppose `w1 = 0.000000` and its slope is `−0.375000`, with `lr = 1.0`:

```
w1 ← 0.000000 − 1.0 × (−0.375000)
   = 0.000000 + 0.375000
   = 0.375000
```

**The slope was negative, so the weight went up.** Correct: a negative slope means "the loss goes down as this weight goes up", so up is where you want to go. Say that sentence twice; a sign confusion here breaks everything downstream.

🍕 **Back on the hillside.** The gradient tells you which way is up. You turn a hundred and eighty degrees and take one step. **The learning rate is your stride length.** Baby steps and you are out there all night. Giant leaps and you bound clean across the valley and up the far slope, and then back, and then across again, for ever.

### 5. The three rounds, in full, with every number

**This is the arithmetic you will do on the board, and you should do it once tonight so you can do it without looking.** Four delivery rows. `x1` = orders in the oven, `x2` = riders free. `y = 1` means the order was late.

| Row | `x1` (in the oven) | `x2` (riders free) | `y` (late?) |
|:--:|:--:|:--:|:--:|
| 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 2 | 1 | 1 |
| 4 | 3 | 1 | 1 |

Start at `w1 = 0`, `w2 = 0`, `b = 0`, with `lr = 1.0`.

**Round 0.**

Every weight is zero, so every `z` is zero, so every `p` is exactly `0.5` — Week 13's third property, doing real work.

```
loss = −ln(0.5) averaged over four rows = 0.693147        ← last week's number, on the wall
```

Errors, `p − y`:

```
row 1:  0.5 − 0 = +0.5
row 2:  0.5 − 0 = +0.5
row 3:  0.5 − 1 = −0.5
row 4:  0.5 − 1 = −0.5
```

Slopes. **Error times feature, averaged:**

```
slope w1 = (+0.5×1  +0.5×1  −0.5×2  −0.5×3) ÷ 4
         = (0.5 + 0.5 − 1.0 − 1.5) ÷ 4  =  −1.5 ÷ 4  =  −0.375000

slope w2 = (+0.5×1  +0.5×2  −0.5×1  −0.5×1) ÷ 4
         = (0.5 + 1.0 − 0.5 − 0.5) ÷ 4  =  +0.5 ÷ 4  =  +0.125000

slope b  = (+0.5 +0.5 −0.5 −0.5) ÷ 4    =   0.0 ÷ 4  =   0.000000
```

Updates, all three at once:

```
w1 ← 0.000000 − 1.0 × (−0.375000) = +0.375000
w2 ← 0.000000 − 1.0 × (+0.125000) = −0.125000
b  ← 0.000000 − 1.0 × ( 0.000000) =  0.000000
```

**Notice the bias did not move, and it is worth a sentence.** Its slope was exactly zero because two rows were late and two were not, and every prediction was 0.5, so the errors cancelled perfectly. **The bias only moves when the average prediction is off from the average label.** Round 1 will move it.

**Round 1.** `w1 = 0.375`, `w2 = −0.125`, `b = 0`.

```
z: row1 = 0.375×1 − 0.125×1 = 0.250      p = 0.562177
   row2 = 0.375×1 − 0.125×2 = 0.125      p = 0.531209
   row3 = 0.375×2 − 0.125×1 = 0.625      p = 0.651355
   row4 = 0.375×3 − 0.125×1 = 1.000      p = 0.731059

loss = 0.581375         ← down from 0.693147

errors: +0.562177, +0.531209, −0.348645, −0.268941

slope w1 = −0.102682     slope w2 = +0.251752     slope b = +0.118950

w1 ← 0.375000 − 1.0 × (−0.102682) = 0.477682
w2 ← −0.125000 − 1.0 × (+0.251752) = −0.376752
b  ← 0.000000 − 1.0 × (+0.118950) = −0.118950
```

**Round 2.** `w1 = 0.477682`, `w2 = −0.376752`, `b = −0.118950`.

```
z: −0.018020, −0.394772, +0.459662, +0.937344
p:  0.495495,  0.402569,  0.612934,  0.718563

loss = 0.504824         ← down again

errors: +0.495495, +0.402569, −0.387066, −0.281437

slope w1 = −0.180095     slope w2 = +0.158033     slope b = +0.057390

w1 ← 0.477682 − 1.0 × (−0.180095) = 0.657777
w2 ← −0.376752 − 1.0 × (+0.158033) = −0.534785
b  ← −0.118950 − 1.0 × (+0.057390) = −0.176340
```

**And the loss after that third step is `0.448421`.**

```
0.693147  →  0.581375  →  0.504824  →  0.448421
```

**Down every single round.** That column of four numbers is the proof that the algorithm works, and it is the thing to put on the board.

![Three rounds of the same line](../figures/fig-w15-4-update-rule-arithmetic-three-rounds.svg)
*Figure 15.2 — Three rounds of the same line. The same subtraction, three knobs, three times over.*

**One more thing to notice, because a student will:** `w2` is going **more and more negative** — 0, then −0.125, then −0.377, then −0.535. That is the model discovering that **more riders free means less likely to be late.** A negative weight is not a bug; it is the model disagreeing with a feature, and it is one of the nicest things you can read off a trained linear model.

### 6. Every line of `descent.py`, explained to somebody who has never programmed

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
```

The numbers library, then three tools from scikit-learn: one to generate a dataset offline, one to cut it into a training pile and a test pile, one to put both feature columns on the same ruler. **All three are from Weeks 1 to 4 and none of them will go anywhere near the training loop.**

```python
np.random.seed(0)
```

Fixes the dice so your numbers match the ones printed in this guide.

```python
X, y = make_classification(n_samples=400, n_features=2, n_informative=2,
                           n_redundant=0, random_state=0)
```

Generates 400 rows with 2 useful features and a yes/no label. `n_redundant=0` is **required**, not optional: the default is 2, and 2 informative plus 2 redundant is more than 2 total, so leaving it out is an error. (It is in the Clinic.)

```python
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
```

Deals 300 rows into the training pile and 100 into the test pile, keeping the class mix the same in both. Week 2's material, unchanged.

```python
scaler = StandardScaler().fit(X_tr)
X_tr = scaler.transform(X_tr)
X_te = scaler.transform(X_te)
```

Puts both columns on the same ruler — Week 4. **`fit` on the training pile only, then `transform` both.** And this is not cosmetic today: §8 explains why gradient descent falls apart without it.

```python
def squash(z):
    e = np.exp(np.where(z >= 0, -z, z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))
```

**Last week's sigmoid, unchanged**, in its two-branch form so it never overflows.

```python
def train(X, y, lr, n_epochs):
    w = np.array([0.0, 0.0])
    b = 0.0
    history = []
```

The function that does the training. Three things get set up: the two weights, both starting at zero; the bias, starting at zero; and an empty list to record the loss at every step so we can plot it afterwards.

> **⚠️ Watch out:** `np.array([0.0, 0.0])` with the decimal points is **essential**. `np.array([0, 0])` makes a whole-number list, and later `w -= lr * grad` tries to put a decimal back into it and fails with a message about casting. This is deliberate mistake one and it is in the Clinic.

```python
    for epoch in range(n_epochs):
```

> **epoch** — one complete pass over all the training data. Today one epoch is also one weight update, because we use every row to compute one gradient and then step once.

> **step**, or **iteration** — one weight update. Today epochs and steps are the same thing. §9 explains when they stop being.

```python
        p = squash((X * w).sum(axis=1) + b)
```

**This is the forward pass, and it is one of this week's three new pieces of syntax.**

`X` is a grid, 300 rows by 2 columns. `w` is a list of 2. `X * w` multiplies **every row** by `w`, item by item — so row 5 becomes `[x1 × w1, x2 × w2]`. Then `.sum(axis=1)` adds up **along each row**, giving one number per row.

**`axis=1` means "squash the columns, keep the rows".** That is the single most confusing thing in numpy and it is worth thirty seconds: `axis=0` goes down the columns and gives you one number per column; `axis=1` goes across the rows and gives you one number per row. **Get it wrong and you get one number instead of three hundred**, and the error appears three lines later. In the Clinic.

Then `+ b` adds the bias to all 300, and `squash` turns all 300 into probabilities.

```python
        p = np.clip(p, 1e-12, 1 - 1e-12)
```

**Last week's guard.** Without it, one probability of exactly 0 or 1 produces a `nan` that poisons the whole loss.

```python
        history.append(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
```

**Last week's log loss**, appended to the record. Nothing new.

```python
        err = p - y
```

The errors, all 300 at once. **This one short line is the entire gradient**, in the sense that everything else is just multiplying it by a feature.

```python
        grad = np.array([np.mean(err * X[:, 0]), np.mean(err * X[:, 1])])
```

The two slopes, in a list. `X[:, 0]` is "every row, column 0" — the first feature for all 300 rows. `err * X[:, 0]` multiplies error by feature row by row, and `np.mean` averages. **That is "error times feature, averaged", typed out.** Then the same for column 1, and both go into a list of two — **which is the gradient.**

```python
        w -= lr * grad
        b -= lr * np.mean(err)
```

**These two lines are the algorithm.** `w -= lr * grad` is shorthand for `w = w - lr * grad`, and because `w` and `grad` are both lists of two, numpy does **both** subtractions at once. The bias gets the same treatment with the feature set to 1, so there is nothing to multiply by.

`w -= lr * grad` is the second of this week's new pieces of syntax, and it is the one to write on the board.

```python
    return w, b, history
```

Hands back the trained weights, the trained bias, and the record of every loss.

```python
    downhill = bool(np.all(np.diff(h) <= 1e-12))
```

`np.diff` gives the gaps between consecutive losses. If every gap is zero or negative, the loss never went up. **`np.all` says "was that true for all of them?"** This one line is how you decide whether a learning rate was safe, and **it is a measurement rather than a glance at a picture** — which matters, because a curve that rises by 0.0001 in the middle looks flat to the eye.

```python
ax.set_yscale("log")
```

**The third new piece of syntax.** Without it, the `lr = 800` curve — which reaches 12.1 — squashes the other two curves into an unreadable smear along the bottom. A log scale gives every *ratio* the same amount of space, so 0.34 to 0.69 takes as much room as 6 to 12. **This is the only way to get all three learning rates onto one honest picture**, and it is why the syntax appears this week and not another.

### 7. What you will actually see on the screen

**This is the real output of `descent.py`. You will see exactly this.**

```text
X_tr shape: (300, 2)   X_te shape: (100, 2)

      lr   epoch 0 epoch 100     final     worst downhill?
   0.005    0.6931    0.6375    0.5098    0.6931      True
   0.500    0.6931    0.3438    0.3416    0.6931      True
 800.000    0.6931    2.7628    7.8482   12.1169     False

lr = 0.5, 2000 epochs
   my w = [-0.6221  3.0924]   my b = 0.2271
   final training loss = 0.3416
   test accuracy       = 0.8200
```

**Read that table like a doctor reads a chart, and get the class to do it before you tell them anything.**

| | What happened | Name | The fix |
|---|---|---|---|
| **`lr = 0.005`** | Nothing is broken. It is just slow — still falling at epoch 500, ending at 0.5098, nowhere near the bottom. | **too small** | Turn it up, or run far more epochs. |
| **`lr = 0.5`** | Flat by epoch 100 and stayed. `downhill? True` — it went down every single epoch. | **converged** | Nothing. Extra epochs cost time and buy nothing. |
| **`lr = 800`** | Shot from 0.69 to 12.1 and thrashed for the rest of the run. `downhill? False`. Ended **eleven times worse than it started.** | **diverged** | Divide by 10 until the curve is monotone. |

**Notice the first column: every single run starts at 0.6931.** That is last week's number, and it is on the wall. All three runs begin with a model that knows nothing, because every weight starts at zero, so every `z` is zero, so every probability is exactly 0.5. **Point at the wall while you say it.**

> **The diagnostic rule to memorise, and it is exact rather than approximate:** for full-batch gradient descent on this loss, **with a good learning rate the loss goes down every single epoch. Not "mostly". Every one.** If the curve wiggles upward, your learning rate is too big. Full stop. (Mini-batch curves *do* wiggle, harmlessly, for a different reason — §9.)

![Three learning rates, three fates](../figures/fig-w15-2-three-learning-rates-three-loss-curves.svg)
*Figure 15.3 — Three learning rates, three fates. A log vertical scale, because 0.34 and 12.1 will not share a linear axis.*

**And the match against scikit-learn**, which is the fourth objective and the emotional high point of the term:

```text
                      weight 1    weight 2        bias
mine (20000 epochs)   -0.622142    3.092423    0.227114
sklearn, default      -0.621309    3.089931    0.226750
sklearn, tol=1e-8     -0.622142    3.092423    0.227114

biggest gap vs default   : 0.002492
biggest gap vs tol=1e-8  : 0.000000
```

**Read those three rows carefully, because there is a genuine subtlety and it is a gift.**

Against scikit-learn's **default** settings we agree to about `0.0025` — three decimal places, which is what objective 4 asks for. But that is not the interesting line.

Against scikit-learn with `tol=1e-8` we agree to **all six printed decimal places, exactly.**

**So the remaining 0.0025 was not our error. It was scikit-learn stopping early.** Its default `tol=1e-4` means "stop when the improvement gets small", and it stopped a little before the bottom. Tighten the tolerance and it walks the rest of the way and lands exactly where we did.

> **🧑‍🏫 If a student asks** "so is sklearn wrong?": no, and this is worth answering properly. **Stopping early is deliberate and usually correct** — the last 0.0025 of a weight makes no difference to any prediction (both versions score 0.8200 on the test set) and chasing it costs time. What scikit-learn is doing is trading a meaningless amount of precision for speed, on purpose. **The interesting thing is that we can now *tell*, and we can turn it off.**

**Two things you must say about the match, and say them plainly.**

1. **This is not luck.** The loss for logistic regression is **convex** — one bowl, one bottom, no traps. So there is exactly one right answer, and any correct method must find it. Twenty-five lines of numpy and a professionally engineered optimiser both got there because there was only one place to get to.
2. **`fit()` is not magic; it is this loop.** The only differences at industrial scale are more features, more rows, and somebody else's C code doing the arithmetic faster.

### 8. Why scaling suddenly matters, in one number

Week 4 taught `StandardScaler` as a tidiness measure. **This week it becomes load-bearing**, and it is worth thirty seconds because it is the first time the student can see *why*.

If one feature runs 0 to 1 and another runs 0 to 100,000, the loss surface is a long thin canyon rather than a bowl. Any learning rate small enough to be stable in the steep direction is hopelessly slow in the shallow one, so training crawls — or the steep direction diverges while the shallow one has barely moved.

**You do not need to demonstrate this today** and the lab does not have room. But if a student asks why the scaler is there, the honest answer is: *"because without it there is no single learning rate that works for both features, and you would have to pick one and lose."*

### 9. Batch, mini-batch and stochastic: name them, do not build them

Everything today used **all 300 rows** to compute one gradient, then took one step. That is one flavour of three.

> **batch (full-batch) gradient descent** — use every training row for one gradient, then step. **One step per epoch.**
>
> **stochastic gradient descent (SGD)** — use **one** row, step, next row. **300 steps per epoch.**
>
> **mini-batch gradient descent** — use a chunk of 32 or 64 rows, step, next chunk. **About 10 steps per epoch here.**

🍕 **The analogy.** You are salting a huge pot of curry. **Full batch:** blend the whole pot, taste one spoonful of the blend, add salt once. Perfectly informed, and you have to blend the whole pot every time. **Stochastic:** taste one grain of rice, add a pinch, taste the next grain. Fast and noisy — one weird grain sends you the wrong way, but over hundreds it averages out. **Mini-batch:** taste a small bowl. Almost as informed as the whole pot, almost as fast as one grain. **Everybody uses mini-batch.**

**Name all three today and build none of them.** The reason to name them is one specific misconception: mini-batch looks like magic if you compare by *epochs*, because an epoch of mini-batch is ten weight updates and an epoch of full batch is one. **Compare by weight updates or by wall-clock time, never by epochs.** Week 23 builds mini-batching properly with a `DataLoader`.

> **convergence criterion** — the rule that tells you to stop. Three common ones: a fixed number of epochs (simple, wasteful); stop when the loss stops changing by more than some tiny amount (**this is scikit-learn's `tol`**, and §7 just showed it in action); or stop when the validation loss stops improving (the one that matters for real models, and it arrives in Week 22).

### 10. The three misconceptions you will actually meet

**Misconception 1 — "the minus sign is arbitrary."** It is the algorithm. The gradient points **uphill**; the loss is a thing you want **small**; so you step the other way. The test is cheap and you should give it to them: **write `w += lr * grad` instead and watch the loss climb — 0.6931, 0.7600, 0.8444, 0.9499, 1.0792.** It is deliberate mistake two.

**Misconception 2 — "a bigger learning rate learns faster."** Up to a point, and then it is catastrophic rather than merely slower. Compare `lr = 0.5` ending at **0.3416** with `lr = 800` ending at **7.8482** — eleven times worse than knowing nothing. **The relationship is not "bigger is faster"; it is "bigger is faster until it is broken", and the cliff is sudden.**

**Misconception 3 — "we matched sklearn, so we have written sklearn."** We have written the training loop for **one model** on a **convex** loss. Weeks 16 to 19 build a network whose loss is **not** convex, and then there is no single right answer and this loop can land in different places on different runs. **Today's exactness is a property of today's problem**, and it is worth flagging so that Week 19's inexactness does not feel like a failure.

### 11. How deep to go, and where to stop

**Go this far:** three rounds by hand with every intermediate number; the loop typed and run; three learning rates named from their curves; the sklearn match printed side by side; the boundary plotted at four epochs.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **Anything with more than one layer** | **Weeks 16 to 19.** Today's model draws a straight line and cannot do better. Say so — the 0.8200 test accuracy is the evidence, and it is the reason the next four weeks exist. |
| **Building mini-batching** | Named today, built in **Week 23** with `DataLoader`. Do not write a batching loop; it doubles the code and teaches nothing new this week. |
| **`torch`, autograd, `loss.backward()`** | **Week 20.** The whole point of today is that they did the slopes themselves. |
| Momentum, Adam, learning-rate schedules | Adam appears in **Week 26**. Momentum is a stretch note only. |
| Regularisation, `penalty`, `C` | Mention `penalty=None` because the comparison needs it, and say in one line what it turns off. No more. |
| The actual derivation of `(p − y) × x` | **Never in this course.** Say that the messy parts cancel, say that is why sigmoid and log loss are paired, and move on. |
| Non-convex losses and local minima | Week 19, where they meet one. Today just plant the word **convex**: one bowl, one bottom. |

The line to hold all lab: **today you write the thing you have been importing.**

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Do the three rounds on paper yourself, with a calculator.** Not read them — **do them.** It takes about eight minutes and it is the single highest-value thing in this checklist, because you will be doing round 0 live on the board with the class calling out numbers. The four rows are `[1,1]→0`, `[1,2]→0`, `[2,1]→1`, `[3,1]→1`, starting at all zeros with `lr = 1.0`. **You should get `−0.375`, `+0.125`, `0.000` for the three slopes and a loss of `0.693147`.**
- [ ] **Blow up the four-round table on the board before the lesson**, empty, with these column headings: `round | w1 | w2 | b | loss | slope w1 | slope w2 | slope b`. Four blank rows. **You will fill it in with the class and it becomes the reference for the whole lab.**
- [ ] **Type and run `three_rounds.py` yourself.** The complete file:

```python
"""three_rounds.py - the four-order table, three rounds, every number printed."""
import numpy as np

X = np.array([[1.0, 1.0],
              [1.0, 2.0],
              [2.0, 1.0],
              [3.0, 1.0]])
y = np.array([0.0, 0.0, 1.0, 1.0])

w = np.array([0.0, 0.0])
b = 0.0
lr = 1.0

for it in range(4):
    z = (X * w).sum(axis=1) + b
    p = 1.0 / (1.0 + np.exp(-z))
    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    err = p - y
    g1 = np.mean(err * X[:, 0])
    g2 = np.mean(err * X[:, 1])
    gb = np.mean(err)
    print("round %d" % it)
    print("   w = [%.6f, %.6f]   b = %.6f   loss = %.6f" % (w[0], w[1], b, loss))
    print("   z   =", np.round(z, 6))
    print("   p   =", np.round(p, 6))
    print("   err =", np.round(err, 6))
    print("   grad = [%.6f, %.6f]   grad_b = %.6f" % (g1, g2, gb))
    grad = np.array([g1, g2])
    w = w - lr * grad
    b = b - lr * gb
    print("   after the step:  w = [%.6f, %.6f]   b = %.6f" % (w[0], w[1], b))
```

Run `python3 three_rounds.py`. You must see **exactly** this. **Runtime: instant.**

```text
round 0
   w = [0.000000, 0.000000]   b = 0.000000   loss = 0.693147
   z   = [0. 0. 0. 0.]
   p   = [0.5 0.5 0.5 0.5]
   err = [ 0.5  0.5 -0.5 -0.5]
   grad = [-0.375000, 0.125000]   grad_b = 0.000000
   after the step:  w = [0.375000, -0.125000]   b = 0.000000
round 1
   w = [0.375000, -0.125000]   b = 0.000000   loss = 0.581375
   z   = [0.25  0.125 0.625 1.   ]
   p   = [0.562177 0.531209 0.651355 0.731059]
   err = [ 0.562177  0.531209 -0.348645 -0.268941]
   grad = [-0.102682, 0.251752]   grad_b = 0.118950
   after the step:  w = [0.477682, -0.376752]   b = -0.118950
round 2
   w = [0.477682, -0.376752]   b = -0.118950   loss = 0.504824
   z   = [-0.01802  -0.394772  0.459662  0.937344]
   p   = [0.495495 0.402569 0.612934 0.718563]
   err = [ 0.495495  0.402569 -0.387066 -0.281437]
   grad = [-0.180095, 0.158033]   grad_b = 0.057390
   after the step:  w = [0.657777, -0.534785]   b = -0.176340
round 3
   w = [0.657777, -0.534785]   b = -0.176340   loss = 0.448421
   z   = [-0.053348 -0.588133  0.604429  1.262206]
   p   = [0.486666 0.357063 0.646669 0.779406]
   err = [ 0.486666  0.357063 -0.353331 -0.220594]
   grad = [-0.131179, 0.156717]   grad_b = 0.067451
   after the step:  w = [0.788956, -0.691502]   b = -0.243791
```

**Check your paper answers against that printout, row by row, before you go to bed.** That is exactly the experience the class will have, and having had it yourself is what lets you run the lab.

- [ ] **Type and run `descent.py`.** The complete file is in the Answer Key, page 15.4. **Runtime under 2 seconds** for all 1,500 epochs. You must get `0.5098 / 0.3416 / 7.8482` in the final column and `True / True / False` in the last.
- [ ] **Run `match.py`** (Answer Key, page 15.6). **Runtime about 1 second** for 20,000 epochs. You must get `biggest gap vs tol=1e-8 : 0.000000`.
- [ ] **Run `curves.py`** (Answer Key, page 15.5) and **open `descent.png`.** **Runtime about 1 second.** Look at both panels: the left has three curves on a log scale with the red one thrashing above the dashed `ln 2` line; the right has four straight lines sweeping from a badly wrong angle into place.
- [ ] **Break it on purpose, twice**, so both deliberate mistakes are muscle memory:
  1. Write `w = np.array([0, 0])` without the decimal points. Real message: `numpy.core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'subtract' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'`.
  2. Write `w += lr * grad` instead of `w -= lr * grad`. **No error.** The loss climbs: `0.693147, 0.759960, 0.844350, 0.949854, 1.079249`.
- [ ] **Print workbook pages 15.1–15.8.**
- [ ] **Check `0.6931` is still on the wall from last week.** You will point at it inside the first four minutes.

### 5 minutes on the day

- [ ] Editor open, terminal ready. **`descent.py` deleted or renamed** — they type it.
- [ ] The empty four-round table on the board, large.
- [ ] **`w ← w − lr × slope` written on the board on its own, in the biggest letters you can manage.** Draw a box round the minus sign.
- [ ] One calculator per pair.
- [ ] `0.6931` visible.
- [ ] Bug Log out.
- [ ] Week 13's S-curve still on the wall — you point at it once, in round 0, when every `p` comes out at exactly 0.5.

### Fallback if the laptops fail

**The first half of this lab is paper anyway.** What you lose is the three learning rates and the sklearn match, and both survive as printouts.

1. **Round 0 on the board works untouched.** That is the core of the lab.
2. **Rounds 1 and 2 in pairs, on calculators.** Give each pair one row of the forward pass and pool the four `p` values on the board, then do the three slopes together. **That is objective 2, complete, on paper.** Budget 20 minutes rather than 12.
3. **Hand out the `descent.py` printout** — the three-learning-rate table — and have them name each row before you say anything. **Objective 3, delivered with a highlighter.** The three names are on the sheet in a jumbled order and they match them up.
4. **Hand out the `match.py` printout** and ask one question: *"which two of these three rows are identical, and what does that tell you?"* **Objective 4, in ninety seconds.**
5. **Draw the diverging curve on the board** rather than plotting it. Two axes, a dashed line at 0.6931, one curve that dives to 0.34 and stays, one that sags gently to 0.51, one that leaps to 12 and thrashes. **Then the question: "which one would you ship?"**

| If this fails | Do this instead |
|---|---|
| `_UFuncOutputCastingError: Cannot cast ufunc 'subtract' output from dtype('float64') to dtype('int64')` | `np.array([0, 0])` needs decimal points: `np.array([0.0, 0.0])`. **This is deliberate mistake one and it is on the schedule.** |
| `ValueError: operands could not be broadcast together with shapes (300,2) (3,)` | `w` has three numbers and `X` has two columns. `print(X.shape, w.shape)` and count. |
| The loss climbs steadily from 0.6931 with a sensible learning rate | `w += lr * grad`. **The gradient points uphill; you must subtract.** Deliberate mistake two. |
| `RuntimeWarning: overflow encountered in exp`, then every loss is `nan` | They used the naive one-line sigmoid and the learning rate is large enough to send `z` to the hundreds. **Use the two-branch `squash` from Week 13.** |
| Every loss is `nan` from epoch 1 with a normal learning rate | The `np.clip` line is missing and a probability hit exactly 0 or 1. **Week 14's guard.** |
| The loss is parked at exactly `0.6931` and will not move | Either `lr` is so small nothing has happened, or the two update lines are missing, or `grad` is all zeros. **Print `w` after ten epochs.** Last week's diagnostic, arriving for real. |
| `ValueError: 'logarithmic' is not a valid value for scale` | It is spelled `ax.set_yscale("log")`. The message helpfully lists every legal value. |
| The three curves are an unreadable smear along the bottom | `set_yscale("log")` is missing. **Without it the `lr = 800` curve at 12.1 flattens everything else against the axis.** |
| Their weights are nowhere near sklearn's | `penalty=None` is missing from the `LogisticRegression(...)` call. By default scikit-learn handicaps the model on purpose, and it will not match an unhandicapped one. |
| Their weights are close but not exact | **Expected, and it is a gift.** Add `tol=1e-8` to sklearn's call and watch them become identical. The gap was sklearn stopping early. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — What Happened in That One Second | 7 | 7 | `fit()` on the board, and five lines of English |
| 🧠 Concept & Maths — Round 0, By Hand, Together | 18 | 25 | Three slopes and three updates, on the board, with the class |
| 💻 Live-Code Together — `descent.py` | 18 | 43 | Twenty-five lines, **two deliberate mistakes**, three learning rates |
| 🎲 Their Turn — Descent From Scratch | 20 | 63 | Their own loop, the sklearn match, the moving boundary |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — What Happened in That One Second (7 minutes)

**Do this:** Nothing on the screen. On the board, write one line:

```
model.fit(X_train, y_train)
```

**Say this:**

> "You have typed that line, at a guess, sixty times since Level 2. Every single time, the same thing happened: about a second of silence, and then an object came back that could predict.
>
> **What happened in that second?**"

**Do this:** Take answers. You will get "it learned", "it found the pattern", "it trained". Write them up without comment. Then:

> "Every one of those is a name for the thing, not a description of it. So let me tell you exactly what happened, and it is going to take five lines."

**Do this:** Write these five lines on the board, slowly, numbering them.

```
1. start with every weight at zero
2. work out the probability for every row
3. work out the loss
4. work out, for each weight, which way is downhill
5. step each weight a little way downhill.  go to 2
```

**Ask this:** "Which of those five can you already do?"

**Do this:** Let them work it out. This is the moment of the hook and it is worth waiting for.

- **Line 2** — Week 13. The sigmoid. They can do it on a calculator.
- **Line 3** — Week 14. Log loss. They can do it on a calculator.
- **Line 4** — Week 12. The slope. They measured slopes by nudging.
- **Line 5** — subtraction.

> **Say this:** "Four out of five. **You have been building this for a month without being told what it was for.**
>
> And the one that is left, line 4, is the only new thing today. Here is what makes it a good day: **it turns out to be easier than the other four.**
>
> So today is a lab, and by the end of it you will have written this" — point at `model.fit` — "in about twenty-five lines of numpy, with scikit-learn nowhere near it. And then we are going to check your answer against scikit-learn's, and **your weights are going to match theirs to six decimal places.**"

**Do this:** Point at `0.6931` on the wall.

**Ask this:** "One prediction before we start. Line 1 says every weight starts at zero. So what is the loss on the very first step, before anything has been learned?"

*Hoped-for answer:* 0.6931.

*If they hesitate:* walk it. *"All weights zero, so every raw score is zero, so every probability is..."* — exactly 0.5 — *"and the loss of a model that says 0.5 to everything is..."* — 0.6931. **"So every training run today starts on that number on the wall. All three of them. Watch for it."**

---

### 🧠 Concept & Maths — Round 0, By Hand, Together (18 minutes)

**Do this (4 min) — the gradient, as three numbers.**

> **Say this:** "Week 12 you measured the slope of a curve with **one** input. Nudge it, see what happens, divide.
>
> Today the model has **three** knobs: `w1`, `w2`, and the bias. So 'which way is downhill' is not one number. It is three."

**Do this:** Write on the board:

```
gradient = [ slope for w1 ,  slope for w2 ,  slope for b ]
```

> **Say this:** "That list has a name. **The gradient.** It is one slope per knob, kept together.
>
> Foggy hillside. You cannot see the valley. But you can feel the ground under your feet. Step your left foot ten centimetres north — it goes **down** three centimetres. Step ten centimetres east — it goes **up** one. So north is downhill and east is uphill. **You do not need a map. You need the ground under your feet, in every direction you could step.**
>
> And now the formula, and I want you to be suspicious of how short it is."

**Do this:** Write it, large:

```
slope for a weight  =  average of  (prediction − truth) × (that feature)
slope for the bias  =  average of  (prediction − truth)
```

**Ask this:** "Where are the logarithms? Last week's loss was made of logarithms. Where are the exponentials?"

*Hoped-for answer:* confusion, which is correct.

> **Say this:** "They cancelled. **All of them.** When you work out the slope of last week's loss applied to the week before's sigmoid, the exponentials and the logarithms cancel exactly, and what is left is `prediction minus truth` times the feature.
>
> That is not a coincidence and it is not luck. Somebody noticed, a very long time ago, that **those two particular functions were built for each other**, and that is why they are always used together. I am not going to prove it to you and you do not need it. **What you need is the sentence: error times feature, averaged.**
>
> Say it back to me."

**Do this (14 min) — round 0, on the board, with the class doing every number.** Reveal the four rows.

```
        x1 (oven)   x2 (riders free)   y (late?)
row 1       1              1               0
row 2       1              2               0
row 3       2              1               1
row 4       3              1               1
```

**Say this:** "Four orders. Orders in the oven, riders standing about doing nothing, and whether it turned up late. Start every weight at zero. Stride length one."

**Ask this:** "All three knobs are zero. What is `z` for row 1?"

*Zero.* **"For row 4?"** *Also zero — everything is multiplied by zero.*

**Ask this:** "So what is `p` for all four rows?"

*Exactly 0.5.* **Point at Week 13's S-curve on the wall.** *"Third property. Sigmoid of zero is exactly a half, no rounding."*

**Do this:** Fill the first row of the board table: `w1 = 0, w2 = 0, b = 0, loss = 0.693147`. **Point at 0.6931 on the wall.** "Predicted it in the hook."

**Ask this:** "Errors. `prediction minus truth`, four of them. Go."

```
row 1:  0.5 − 0 = +0.5
row 2:  0.5 − 0 = +0.5
row 3:  0.5 − 1 = −0.5
row 4:  0.5 − 1 = −0.5
```

**Do this:** Now the slope for `w1`, out loud, one term at a time, with the class supplying each product. **Write every term.**

```
slope w1 = ( +0.5×1  +0.5×1  −0.5×2  −0.5×3 ) ÷ 4
         = ( 0.5 + 0.5 − 1.0 − 1.5 ) ÷ 4
         = −1.5 ÷ 4
         = −0.375000
```

**Ask this:** "Why did rows 3 and 4 come out negative?"

*Because those two were late and the model said 0.5, so the error is negative.*

**Ask this:** "And why is row 4's contribution the biggest of the four?"

*Because its feature is 3, the largest.* **This is the important one.**

> **Say this:** "**The rows with the biggest features get the biggest say in that weight.** That is not a bug either — it is a blame rule, and it is fair. If a weight is attached to a feature that was large on that row, that weight is more responsible for the answer on that row."

**Do this:** Now `w2` and `b`, faster, class doing them.

```
slope w2 = ( +0.5×1  +0.5×2  −0.5×1  −0.5×1 ) ÷ 4 = +0.5 ÷ 4 = +0.125000
slope b  = ( +0.5  +0.5  −0.5  −0.5 ) ÷ 4         =  0.0 ÷ 4 =  0.000000
```

**Ask this:** "The bias slope is **exactly** zero. Why?"

*Hoped-for answer:* two rows late and two on time, and every prediction was 0.5, so the errors cancel.

> **Say this:** "Perfectly balanced. **The bias only moves when the average prediction is off from the average label**, and right now it is dead on. That will not last."

**Do this:** Now the update. Point at `w ← w − lr × slope` in giant letters, and at the box around the minus sign.

> **Say this:** "The slope points **uphill**. The loss is a thing we want **small**. So we go the other way. **That is the entire algorithm.** Everything else today is bookkeeping."

```
w1 ← 0.000000 − 1.0 × (−0.375000) = 0.000000 + 0.375000 = +0.375000
w2 ← 0.000000 − 1.0 × (+0.125000)                       = −0.125000
b  ← 0.000000 − 1.0 × ( 0.000000)                       =  0.000000
```

**Ask this:** "`w1`'s slope was **negative** and `w1` went **up**. Is that right?"

*Hoped-for answer:* yes — a negative slope means the loss falls as the weight rises, so up is downhill.

*If they say it looks wrong:* **do not correct with the rule.** Ask instead: *"a negative slope means the loss goes ______ as the weight goes up?"* Down. *"And we want the loss to go?"* Down. *"So?"*

**Do this:** Fill in the second row of the board table. Then run one more round with the class, **fast**, giving them the four `p` values rather than making them compute four sigmoids:

```
round 1:  p = 0.562177, 0.531209, 0.651355, 0.731059     loss = 0.581375
          slopes = −0.102682, +0.251752, +0.118950
          w1 = 0.477682   w2 = −0.376752   b = −0.118950
```

**Ask this:** "Loss went from 0.693147 to 0.581375. And the bias has moved off zero. Why now and not before?"

*Because the predictions are no longer all 0.5, so the errors no longer cancel.*

> **Say this:** "One more thing to notice, and it is my favourite thing on this board. Look at `w2`. Zero, then minus 0.125, then minus 0.377. **It is going more and more negative.**
>
> `w2` is 'riders standing about with nothing to do'. The model is working out — from four rows and two rounds of arithmetic — that **more riders free means less likely to be late.** Nobody told it that. It found it in the errors.
>
> A negative weight is not a mistake. **It is the model disagreeing with a feature, out loud, in a number you can read.**"

---

### 💻 Live-Code Together — `descent.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — the data, and the forward pass in one line.**

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(0)

X, y = make_classification(n_samples=400, n_features=2, n_informative=2,
                           n_redundant=0, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
scaler = StandardScaler().fit(X_tr)
X_tr = scaler.transform(X_tr)
X_te = scaler.transform(X_te)
print("X_tr shape:", X_tr.shape, "  X_te shape:", X_te.shape)
```

```text
X_tr shape: (300, 2)   X_te shape: (100, 2)
```

> **Say this:** "Everything on that screen is Weeks 1 to 4. Generate, split, scale, and **fit the scaler on the training pile only.** Nothing new. And notice: **this is the last time scikit-learn appears until we check our answer.** It does not go anywhere near the loop."

Now the forward pass:

```python
w = np.array([0.0, 0.0])
b = 0.0
z = (X_tr * w).sum(axis=1) + b
print("z shape:", z.shape, "  first five:", z[:5])
```

```text
z shape: (300,)   first five: [0. 0. 0. 0. 0.]
```

> **Say this:** "`X_tr * w` multiplies **every row** by the weights, item by item. Then `.sum(axis=1)` adds up **along each row.**
>
> `axis=1` is the thing to remember, and it is the most confusing word in numpy. **`axis=0` goes down the columns and gives you one number per column. `axis=1` goes across the rows and gives you one number per row.** We want one raw score per row, so it is 1.
>
> And look at the shape: **three hundred.** One score per order. All zeros, because every weight is zero — which is why the first loss is going to be..."

*0.6931.* Point at the wall.

**Step 2 (5 min) — 🐞 DELIBERATE MISTAKE ONE: whole numbers.**

Type the loop, but with `w = np.array([0, 0])` — no decimal points:

```python
w = np.array([0, 0])
b = 0.0
for epoch in range(500):
    p = np.clip(squash((X_tr * w).sum(axis=1) + b), 1e-12, 1 - 1e-12)
    err = p - y_tr
    grad = np.array([np.mean(err * X_tr[:, 0]), np.mean(err * X_tr[:, 1])])
    w -= 0.5 * grad
    b -= 0.5 * np.mean(err)
```

Real output:

```text
Traceback (most recent call last):
  File "descent.py", line 25, in <module>
    w -= 0.5 * grad
numpy.core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'subtract' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```

(Your line number will be whatever line `w -= ...` sits on in your file. The message text is identical.)

**Do this:** Say nothing for five seconds. Then read the last line aloud, slowly, and translate it word by word.

**Ask this:** "`int64` and `float64`. Which is which, and which one is my `w`?"

*`int64` is whole numbers, `float64` is decimals. `w` is the int64 one.*

> **Say this:** "**`np.array([0, 0])` — no decimal points — makes a box that only holds whole numbers.** Then I asked it to store `−0.1875` and it refused. It did not round it silently and it did not throw the decimals away; **it stopped.**
>
> And notice how good that error is. It named both types, it named the operation, and it pointed at the exact line. **Long error messages are usually the helpful kind.** The short ones are worse.
>
> The fix is two characters."

```python
w = np.array([0.0, 0.0])
```

**Bug Log, ninety seconds**, with the words *"a weight must be a decimal, because a step of `−lr × slope` almost never is."*

**Step 3 (4 min) — 🐞 DELIBERATE MISTAKE TWO: the wrong sign.**

Change `w -= 0.5 * grad` to `w += 0.5 * grad` and print the first five losses.

Real output:

```text
epoch 0  loss = 0.693147
epoch 1  loss = 0.759960
epoch 2  loss = 0.844350
epoch 3  loss = 0.949854
epoch 4  loss = 1.079249
```

**Ask this:** "Any error message? And what is happening?"

*No error at all, and the loss is going up.*

> **Say this:** "**No crash. It is running perfectly.** It is running perfectly in the wrong direction.
>
> Look at the board." — point at `w ← w − lr × slope` and the boxed minus — "**The gradient points uphill.** With a plus sign I am walking up the hill as fast as I can, deliberately, five hundred times.
>
> And here is why this is worth four minutes: **the only thing that catches it is knowing the loss should go down.** No message will tell you. There is no test that fires. **You have to know what the number is supposed to do.**
>
> Which gives you a rule for the rest of your career: **print the loss every epoch, and look at it.** If it is going up, either your sign is wrong or your stride is too long, and those are the only two options."

Fix it. **Bug Log** — this one goes in as a **"no error message, loss goes up"** entry.

**Step 4 (5 min) — three learning rates, and the log scale.**

Wrap the loop in a function and run it three times:

```python
print("%8s %9s %9s %9s %9s %9s" % ("lr", "epoch 0", "epoch 100", "final",
                                   "worst", "downhill?"))
for lr in (0.005, 0.5, 800.0):
    w, b, h = train(X_tr, y_tr, lr, 500)
    h = np.array(h)
    downhill = bool(np.all(np.diff(h) <= 1e-12))
    print("%8.3f %9.4f %9.4f %9.4f %9.4f %9s"
          % (lr, h[0], h[100], h[-1], h.max(), str(downhill)))
```

```text
      lr   epoch 0 epoch 100     final     worst downhill?
   0.005    0.6931    0.6375    0.5098    0.6931      True
   0.500    0.6931    0.3438    0.3416    0.6931      True
 800.000    0.6931    2.7628    7.8482   12.1169     False
```

**Ask this:** "Read the first column. What do all three have in common?"

*They all start at 0.6931.* **Point at the wall one more time.**

**Ask this:** "Now name each row. One word each. I will give you the three words: **too small**, **converged**, **diverged**. Which is which, and how do you know?"

*Hoped-for answers, and push for the evidence not just the label:*

- `0.005` → **too small.** Evidence: still falling at epoch 500, and its final loss (0.5098) is far above 0.3416. **Nothing is broken; it just did not finish.**
- `0.5` → **converged.** Evidence: flat by epoch 100, and `downhill? True` — it went down every single epoch out of five hundred.
- `800` → **diverged.** Evidence: `downhill? False`, worst loss 12.1169, and it ended at 7.8482, which is **eleven times worse than knowing nothing.**

> **Say this:** "And one rule to memorise, because it is exact rather than a guideline. **For this kind of training, with a good learning rate, the loss goes down every single epoch. Not mostly. Every one.** If it wiggles up, your learning rate is too big. That is what the `downhill?` column measures, and it measures it — you do not squint at a picture."

**Do this:** Plot all three, and **deliberately forget the log scale first.**

```python
for lr in (0.005, 0.5, 800.0):
    _, _, h = train(X_tr, y_tr, lr, 500)
    ax.plot(h, label="lr = %g" % lr)
plt.savefig("descent.png")
```

**Ask this:** "The `lr = 800` curve reaches 12. The other two live between 0.34 and 0.69. What is this picture going to look like?"

*Two flat lines squashed against the bottom.*

```python
ax.set_yscale("log")
```

> **Say this:** "One line. **A log scale gives every *ratio* the same amount of room**, so the gap from 0.34 to 0.69 gets as much space as the gap from 6 to 12. Now all three fit on one honest picture."

---

### 🎲 Their Turn — Descent From Scratch (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: type the twenty-five-line loop; get three learning rates onto one log-scale plot; match sklearn's weights side by side; then plot the boundary at four epochs and watch it swing into place.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the board with the four-round table filled in and `w ← w − lr × slope` in giant letters. Write four things underneath:

```
gradient      one slope per knob, in a list:  [−0.375, +0.125, 0.000]
each slope    average of (prediction − truth) × (that feature)
the update    w ← w − lr × slope,  for every knob, at the same time
epoch         one pass over the data.  Today, one pass = one step
```

**Say this:**

> "Four things. That is the week, and it is the whole of `fit()`.
>
> **The gradient** is one slope per knob, kept in a list. Three knobs, three numbers. Not one number — that is the mental shift.
>
> **Each slope** is `error times feature, averaged`. And I want to say the strange thing about that once more: last week's loss was made of logarithms and the week before's model was made of exponentials, and **when you work out the slope, they cancel.** What is left is a subtraction and a multiplication. That cancellation is why those two functions are always used together, and it is a hundred years old.
>
> **The update** is one line with a minus sign in it. The gradient points uphill; you want to go down; so you subtract. Every knob, at the same time.
>
> **An epoch** is one pass over the data. Today one pass is one step, and there are two other ways to arrange that, called mini-batch and stochastic, and you will build one in Week 23."

**Do this:** Point at the sklearn match on the screen.

> "And then this. **Your twenty-five lines and scikit-learn's optimiser agree to six decimal places.**
>
> That is not luck, and it is worth knowing why. This loss is **convex** — one bowl, one bottom, no traps anywhere. So there is exactly **one** right answer, and any method that works at all has to find it. You wrote a correct method. It found the answer. **`fit()` is not magic. It is this loop, in somebody else's C code.**
>
> And do not skip past the middle row. At sklearn's default settings we disagreed by 0.0025 — **and that gap was theirs, not ours.** Their default rule is 'stop when the improvement gets small', and they stopped a bit before the bottom, on purpose, because the last 0.0025 of a weight changes no prediction at all. Both versions score 0.8200. **The interesting thing is that you can now tell, and you can turn it off.**"

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One number on that screen should annoy you. **Test accuracy: 0.8200.**
>
> You wrote a correct training loop. It converged. It matched a professional library exactly. And it gets **eighty-two per cent.** Almost one order in five, wrong.
>
> That is not a bug in your loop, and it is not a learning rate you could have picked better. **It is the model.** Look at the right-hand panel of your plot: your boundary is a **straight line**, and it is a straight line because the model predicts 'late' when `z ≥ 0`, and that is the equation of a straight line. There is no choice of `w1`, `w2` and `b` that bends it.
>
> And the data is not straight. Look at it. Two clumps of triangles with circles wrapped round them.
>
> So next week we start again, and we build a model that can bend. It is made out of **several** of these things stacked on top of each other — and every single one of them is trained by the loop you wrote today."

**Do this:** Hand out the homework. Read the third part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `numpy.core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'subtract' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'` | "You asked me to put a decimal into a box that only holds whole numbers, and I will not do that silently." | `w = np.array([0, 0])` with no decimal points. | `w = np.array([0.0, 0.0])`. **A weight must be a decimal, because `−lr × slope` almost never is.** |
| `ValueError: operands could not be broadcast together with shapes (300,2) (3,)` | "You have three weights and two feature columns." | `w = np.array([0.0, 0.0, 0.0])` — the bias counted as a third weight by mistake. The bias is separate; it is not in `w`. | Two weights, and `b` on its own. `print(X.shape, w.shape)` and count. |
| `ValueError: operands could not be broadcast together with shapes (300,) (100,)` | "You gave me 300 predictions and 100 truths." | `p - y_te` instead of `p - y_tr` inside the training loop. | Train against `y_tr`. **`print(len(p), len(y))` is the cheapest check in the file.** |
| `ValueError: operands could not be broadcast together with shapes (2,) (2,300) (2,)` | "Your gradient is a 2-by-300 grid, not a list of 2." | `np.mean` forgotten: `np.array([err * X[:, 0], err * X[:, 1]])` keeps all 300 products instead of averaging them. | `np.array([np.mean(err * X[:, 0]), np.mean(err * X[:, 1])])`. **A gradient has one number per knob, always.** |
| `ValueError: Number of informative, redundant and repeated features must sum to less than the number of total features` | "You asked for 2 features and also 2 informative plus 2 redundant ones." | `n_redundant=0` left off `make_classification`. The default is **2**, not 0. | Add `n_redundant=0`. **Read the message as arithmetic: 2 + 2 > 2.** |
| `ValueError: 'logarithmic' is not a valid value for scale; supported values are 'linear', 'log', 'symlog', 'asinh', 'logit', 'function', 'functionlog'` | "That is not a scale I know, and here is the complete list." | `ax.set_yscale("logarithmic")`. | `ax.set_yscale("log")`. **When a message lists the legal values, read the list.** |
| `RuntimeWarning: overflow encountered in exp` then every loss becomes `nan` | "The raw scores got so big that `e^(−z)` could not be stored." | The naive one-line sigmoid plus a large learning rate — `lr = 800` sends `z` into the hundreds within one epoch. | Use Week 13's two-branch `squash`. **Then the run survives and you get to *see* divergence instead of just `nan`.** |
| `RuntimeWarning: divide by zero encountered in log` then `nan` | "Some probability was exactly 0 or exactly 1 and `ln(0)` is minus infinity." | The `np.clip` line is missing. | `p = np.clip(p, 1e-12, 1 - 1e-12)`. **Week 14's guard, needed for real.** |
| **No error. The loss climbs smoothly from 0.6931 with a sensible learning rate.** | Nothing crashed. You are walking uphill on purpose, five hundred times. | `w += lr * grad` instead of `w -= lr * grad`. | Subtract. **The gradient points uphill.** Diagnostic: `0.693147, 0.759960, 0.844350, 0.949854` climbing steadily is this bug and nothing else. |
| **No error. The loss is parked at exactly 0.6931 for all 500 epochs.** | Nothing crashed. The model is predicting 0.5 for everything and has never moved. | The two update lines are missing, or `lr` is so tiny nothing changed, or `grad` is all zeros. | `print(w, b)` after ten epochs. **All zeros means nothing is updating.** Last week's diagnostic, arriving for real. |
| **No error. `z` has shape `()` instead of `(300,)` and everything downstream is one number.** | Nothing crashed until much later. | `.sum()` instead of `.sum(axis=1)`. Without the axis it adds up **every** number in the grid and gives you one. | `.sum(axis=1)`. **`axis=1` keeps the rows.** |
| **No error. Your weights are nowhere near sklearn's.** | Nothing crashed and both models work. | `penalty=None` missing from `LogisticRegression(...)`. By default scikit-learn handicaps the model to stop it overfitting, and a handicapped model has smaller weights. | `LogisticRegression(penalty=None, max_iter=5000)`. |
| **No error. Your weights are close to sklearn's but not identical.** | Nothing is wrong. **This one is a gift.** | sklearn's default `tol=1e-4` stopped it a little short of the bottom. | Add `tol=1e-8` and watch the gap become `0.000000`. **The 0.0025 was theirs, not yours.** |
| **No error, no output. The plot file is empty or the run "hangs".** | Nothing crashed. | Every loss is `nan`, and matplotlib draws nothing for `nan` on a log axis. | Print `h[0]`, `h[1]`, `h[2]`. **A `nan` at epoch 1 means overflow or a missing clip; the plot is a symptom, not the bug.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and they are the three questions that will resolve most training bugs the student will ever have.

17. **"Print the loss every epoch and look at it."** Not the final loss — every one. The shape of that column tells you which of four things is happening: falling and flattening (fine), falling slowly and still falling (too small), wobbling (too big), climbing (sign error or far too big). **You cannot diagnose training from one number.**

18. **"Is it going down every epoch? Measure it, do not look at it."** `np.all(np.diff(h) <= 1e-12)` prints `True` or `False`. A curve that rises by 0.0001 in the middle of five hundred epochs looks perfectly flat and is not. **A measurement beats a glance.**

19. **"What is `w` after ten epochs?"** If it is still `[0.0, 0.0]`, nothing is updating, and the whole rest of the file is irrelevant. **Ten epochs is enough; you do not need to wait for five hundred.**

And the sentence for this week:

> **"Every training run starts at 0.6931. If it is not falling by epoch 10, print `w`. If it is climbing, check the minus sign. If it is wobbling, divide the learning rate by ten."**

---

## 🎲 The Activity, In Full

### Descent From Scratch

**The goal.** Every student ends the lab with a working gradient-descent logistic regression they typed themselves, a plot naming three learning rates, and a printed side-by-side comparison against scikit-learn where the weights agree.

**Setup (2 minutes)**

- The four-round table is on the board, filled in, from the concept segment. **It stays up for the whole lab** — it is the reference every student checks their loop against.
- `w ← w − lr × slope` in giant letters with a box round the minus sign.
- `0.6931` on the wall.
- Workbook pages 15.3 to 15.6 out.
- **The Week 13 `squash` function should be copied in, not retyped.** There is no learning left in typing the sigmoid a fourth time.

**Part 1 — the loop, and one hard checkpoint (8 minutes)**

They type the `train` function. About fifteen lines.

**The checkpoint, and do not let anybody past it:** run the loop for **four** epochs only, on the **four hand-typed rows** from the board, with `lr = 1.0`, and print the loss each round. **They must get:**

```
0.693147
0.581375
0.504824
0.448421
```

> **⚠️ Watch out:** this is the most important ninety seconds of the lab. A student whose loop prints those four numbers has a correct implementation and can trust everything that follows. A student who skips this and runs straight at 400 rows has a program that prints *a* number, with no way at all to know whether it is right. **Check every screen for those four numbers before anybody scales up.**

**What goes wrong here, and what to say:**

| Their four numbers | What it is | Ask this |
|---|---|---|
| `0.693147` then rising | sign error | "Which way does the gradient point?" |
| `0.693147` four times | nothing is updating | "What is `w` after the first round?" |
| All `nan` | missing clip, or the naive sigmoid | "Print `p`. Is anything exactly 0 or 1?" |
| A crash on `w -= ...` | `np.array([0, 0])` | "Read the last line of the error. Which two types?" |
| Right first, then drifting | they used `lr = 0.5`, not `1.0` | "What stride did the board use?" |

**Part 2 — three learning rates on one plot (5 minutes)**

Switch to the 400-row dataset. Run 500 epochs at `0.005`, `0.5` and `800`. Print the table, then plot all three with `ax.set_yscale("log")` and a dashed line at `ln 2`.

**Then, on page 15.5, they write the three names next to the three learning rates and one line of evidence for each.** Not the label alone — **the evidence.**

**Part 3 — the sklearn match (4 minutes)**

Train 20,000 epochs at `lr = 0.5` — it takes about a second — then fit `LogisticRegression(penalty=None, max_iter=5000)` on the identical arrays and print both sets of numbers, aligned in columns.

Then the twist, which they should discover rather than be told: **add `tol=1e-8` to the sklearn call and re-run.** The gap goes to `0.000000`.

**Ask this, when the room has it:** "The gap was 0.0025 and now it is zero. **Whose 0.0025 was it?**"

*scikit-learn's.* It stopped early, on purpose.

**Part 4 — the boundary walking into place (3 minutes)**

Plot the 300 training rows — circles for on time, triangles for late — and overlay the boundary at epochs 0, 50, 150 and 300, **starting deliberately from a bad place**, `w = [2.0, −2.0]` and `b = 1.0`.

The line is `x2 = −(w1 × x1 + b) ÷ w2`, which comes straight from `z = 0`. Give them that line; deriving it is not today's job.

```
epoch   0   w = [ 2.0000, −2.0000]   b =  1.0000   loss = 2.0454
epoch  50   w = [−0.2798,  2.1091]   b =  0.0902   loss = 0.3590
epoch 150   w = [−0.5478,  2.8694]   b =  0.1883   loss = 0.3423
epoch 300   w = [−0.6110,  3.0587]   b =  0.2211   loss = 0.3416
```

![The line walking into place](../figures/fig-w15-3-boundary-moving-over-epochs.svg)
*Figure 15.4 — The line walking into place. Four snapshots, and the loss beside each one.*

**Ask this at the finished plot:** "The line at epoch 0 is badly wrong and by epoch 50 it is basically right. So why did we bother running another 250 epochs?"

*Because the loss was still falling — 0.3590 to 0.3416 — even though the picture barely changes.* **A picture is not a measurement.**

**What "finished" looks like**

- The four-epoch checkpoint printing `0.693147 / 0.581375 / 0.504824 / 0.448421`.
- A three-row table with `True / True / False` in the `downhill?` column.
- `descent.png` with a **log** y-axis, three labelled curves, and a dashed `ln 2` line.
- Three names written next to three learning rates, **each with a line of evidence.**
- A weight comparison printed in aligned columns, with `biggest gap vs tol=1e-8 : 0.000000`.
- Four boundary lines on a scatter, with the loss beside each.

**Variation — easier**

**Cut part 4 entirely.** The moving boundary is the prettiest thing in the lab and the least load-bearing.

**Cut the 400-row dataset.** Do everything on the four hand-typed rows: run 200 epochs at `lr = 0.1`, `1.0` and `50` and name the three curves. The names still come out right, the loop is identical, and objectives 1, 2 and 3 are all met on data they can check by hand.

**Give them the loop with three lines blanked out.** These three, and nothing else:

```python
        err = p - ________
        grad = np.array([np.mean(err * X[:, 0]), np.mean(______ * X[:, 1])])
        w -= lr * ________
```

**Those three blanks are the entire week.** Everything else in the file is Weeks 1 to 14.

**The version of the maths that skips the algebra.** No formula and no letters. **A four-column table they fill in for one knob:**

| | prediction | truth | error | × feature |
|:--:|:--:|:--:|:--:|:--:|
| row 1 | 0.5 | 0 | +0.5 | +0.5 × 1 = +0.5 |
| row 2 | 0.5 | 0 | +0.5 | +0.5 × 1 = +0.5 |
| row 3 | 0.5 | 1 | −0.5 | −0.5 × 2 = −1.0 |
| row 4 | 0.5 | 1 | −0.5 | −0.5 × 3 = −1.5 |
| | | | **add up** | **−1.5** |
| | | | **÷ 4** | **−0.375** |

**Then one subtraction:** `0 − 1.0 × (−0.375) = +0.375`. **That is objective 2 for one knob**, done with a table and a subtraction, and a student who can fill it in twice has met the week's new maths.

**Variation — harder**

None of these need syntax from a later week.

1. **Find the largest learning rate that still goes downhill every epoch.** Sweep `lr` over `1, 3, 8, 10, 12, 15, 20, 30` and print `np.all(np.diff(h) <= 1e-12)` for each. **The answer is between 12 and 15**: `lr = 12` is monotone and ends at `0.3416`; `lr = 15` is not monotone and ends at `0.3591`, wobbling between `0.3557` and `0.3591` for ever. **Then the punchline: `lr = 12` reaches the bottom in about 8 epochs, and `lr = 0.5` needs about 100.** **Twenty-four times the stride bought about twelve times the speed, and it was still perfectly safe.**
2. **Confirm the slope by nudging**, which is Week 12 arriving to check Week 15. Compute the loss at `w1`, then at `w1 + 0.0001` and `w1 − 0.0001`, and do `(up − down) ÷ 0.0002`. It should match the gradient formula's answer to about six decimal places. **This is the single most valuable technique in the next five weeks and it is called a gradient check.** Week 18 makes it compulsory.
3. **Read the trained model as English.** Given `w = [−0.6221, 3.0924]` and `b = 0.2271`: write two sentences a delivery manager could act on. Then the harder question: **is feature 2 really five times as important as feature 1?** (Here the answer is close to yes, *because* the scaler put both columns on the same ruler. Without the scaler the comparison would be meaningless — Week 4 doing real work.)
4. **Ask why 0.82.** Plot the data and look at it. Then answer: the boundary is a straight line because `z = 0` is the equation of a straight line, and the data is not separable by one. **Estimate how many rows a straight line can never get right**, and compare to the 18 it actually misses out of 100.
5. **Momentum, as a stretch.** Instead of `w ← w − lr × g`, keep a running velocity: `v ← 0.9 × v + 0.1 × g`, then `w ← w − lr × v`. Re-run all three learning rates. **You should find momentum helps enormously at small `lr` and makes the large one worse**, which is a genuinely surprising result worth two sentences of explanation. (It arrives officially as `torch.optim.SGD(..., momentum=0.9)` in Week 21.)

---

## ❓ Questions Students Ask This Week

**"How does it know it is going the right way? It cannot see the bottom."**

It cannot, and that is the point of the foggy-hillside picture. **It never knows where the bottom is. It only knows which way is down, right where it is standing.**

That works because of a property this particular loss has: it is **convex**, one bowl with one bottom and no side dips. On a bowl, "keep going downhill" always gets you to the bottom eventually, however long it takes.

And it stops working in Week 19, when the model has layers and the loss stops being a bowl. Then "keep going downhill" can land you in a shallow dip that is not the bottom, and there is genuinely nothing the algorithm can do about it. **Everyone lives with that.** Today's exactness is a property of today's problem, not of gradient descent.

**"Why does the slope formula have no logarithms in it? Last week's loss was full of them."**

Because they cancelled, exactly, and it is one of the most satisfying accidents in the subject.

When you work out the slope of log loss applied to a sigmoid, an ugly term appears from the logarithm and an equally ugly term appears from the sigmoid, and **they are reciprocals of each other**, so they multiply to 1 and vanish. What survives is `prediction − truth`.

That is not luck; it is why these two functions are always used together. Somebody in the 1940s noticed that sigmoid and log loss were built for each other, and every classifier since has used the pair. **If you paired sigmoid with squared error instead, nothing would cancel, and the mess you would be left with is exactly why that pairing trains so badly.**

**"How do I choose the learning rate for a new problem?"**

Honestly: **you try some, and you look at the loss curve.** There is no formula, and anybody who gives you one is selling something.

The practical recipe, and it is what professionals do: **start at 0.1. Run 20 epochs. If the loss goes up, divide by 10. If it goes down but barely, multiply by 3. Repeat.** Two minutes gets you within a factor of three of the best value, and a factor of three does not matter.

What you should absolutely do is what you did today: **run three or four values and look at the curves side by side.** The three shapes are so distinctive that once you have seen them you can diagnose a run at a glance for the rest of your life.

**"We matched scikit-learn exactly. So does scikit-learn use this loop?"**

Not this exact one, and the difference is interesting.

`LogisticRegression`'s default method is called **L-BFGS**, and it is cleverer: it builds up a picture of the *shape* of the bowl as it goes, and uses it to take much better steps than "downhill by a fixed stride". It gets there in dozens of steps rather than thousands.

**But it is solving the same problem and finding the same answer**, which is exactly what you proved today. That is why the match is meaningful: two completely different methods, one right answer, because the loss is convex.

Neural networks do **not** use L-BFGS — they use variants of the loop you wrote today, because the clever methods need too much memory when there are millions of weights. **So the twenty-five lines you wrote are much closer to how a real neural network trains than scikit-learn's optimiser is.**

**"Why start the weights at zero? Could I start somewhere else?"**

You could, and for this model it makes no difference at all — the bowl has one bottom, so you get there from anywhere. You proved it in part 4 of the activity: starting from `w = [2.0, −2.0]` with a loss of 2.0454, it still landed on 0.3416.

**For a neural network it matters enormously and you must not start at zero.** If every weight in a layer starts identical, every unit in that layer computes the same thing and receives the same gradient, so they stay identical forever — you have a hundred units doing the work of one. This is called the symmetry problem and Week 19 hits it head-on. **Today zero is fine and simple; from Week 19 it is a bug.**

**"Is there a best learning rate, or is it different every time? And could a computer just work it out?"**

**Nobody fully agrees, and this is a live argument worth knowing about.**

For a convex bowl you can prove things: there is a largest stable learning rate, it depends on how curved the bowl is, and you can compute it if you can measure the curvature. You found today that on this problem it sits between 12 and 15. That is real mathematics and it works.

For a neural network almost none of it survives. The loss is not a bowl, the curvature changes as you move, and the best learning rate at epoch 1 is usually far too big at epoch 100 — which is why real training uses a **schedule** that turns the rate down as it goes.

And here is the disagreement. There is a serious research effort building optimisers that need **no** learning rate at all — they measure the landscape and set their own stride. Some of them work impressively well on benchmarks. And yet **almost every large model in the world is still trained with a hand-picked learning rate and a hand-picked schedule**, because the automatic methods are less predictable when things go wrong, and at the scale where a training run costs real money, predictability beats elegance.

So: the theory says it should be automatable, a decade of engineering has mostly declined to automate it, and both sides have good reasons. **You are allowed to find that unsatisfying.**

**"What is `epoch` for, if today one epoch is one step?"**

Today they are the same and the word looks redundant. It stops being redundant the moment you stop using all the rows at once.

If you have 300 rows and you use 32 at a time, one **epoch** — one pass over the data — is about ten **steps**. So a run of "100 epochs" is 1,000 weight updates.

**And this is where people get fooled.** If you compare full-batch and mini-batch by epochs, mini-batch looks like magic — it got much further in "the same number of epochs". It did ten times as many updates. **Always compare by weight updates or by wall-clock time.** You will build the mini-batch version in Week 23.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The class types the loop before doing round 0 on paper** | It is a lab and the laptops are open | **Close the laptops.** A loop with no hand-computed number beside it is a spell, and a student who cannot tell a right answer from a wrong one has not learned to train anything. **Round 0 on the board first, every time.** |
| **The four-epoch checkpoint gets skipped** | It looks like a formality and the real dataset is more exciting | It is the only place in the lab where correctness is *checkable*. **Walk the room and look for `0.693147 / 0.581375 / 0.504824 / 0.448421` on every screen** before anybody scales up. Ninety seconds, and it saves the second half of the lab. |
| Somebody's loss climbs and they conclude gradient descent does not work | The sign error produces no error message | Point at the boxed minus sign, ask *"which way does the gradient point?"*, and let them fix it themselves. **Then put it in the Bug Log**, because they will do it again in Week 19 with four gradients instead of three. |
| The `lr = 800` run fills the screen with `nan` and warnings | They used the naive one-line sigmoid instead of Week 13's | Use `squash`. **This matters more than it looks:** with the safe sigmoid, `lr = 800` produces a beautiful visible divergence to 12.1. With the naive one it produces `nan` and there is nothing to see. |
| The plot comes out as two flat lines and a spike | `set_yscale("log")` missing | It is one line and it is one of the week's three new pieces of syntax. **Ask first: "the red curve reaches 12 and the others live near 0.4 — what shape will a linear axis make?"** |
| The lesson runs out of time in part 3 | Four parts is a lot for twenty minutes | **Cut part 4, the moving boundary.** It is the prettiest thing in the lab and the least important. **Never cut part 3** — the sklearn match is objective 4 and the emotional point of the term. |
| Students conclude 82% is a failure of their code | It is a natural inference and it is wrong | **Name it before they ask.** The boundary is a straight line because `z = 0` is a straight line, and the data is not separable by one. **This is the argument for the next four weeks and it should feel like a cliffhanger, not a disappointment.** |
| The `tol=1e-8` discovery gets explained instead of discovered | It is quicker to tell them | Let them run it. **The moment `0.002492` becomes `0.000000` is worth more than any sentence you could say about tolerances**, and the follow-up question — *"whose 0.0025 was it?"* — only works if they were surprised. |
| Mini-batch gets built because somebody asks | It is a reasonable request and you know how | **Say the analogy, name the three flavours, build none of them.** It doubles the code and teaches nothing this week. Week 23 builds it with a `DataLoader` and it belongs there. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** part 4, the moving boundary, entirely.

**Cut:** the 400-row dataset. Everything on the four hand-typed rows, at `lr = 0.1`, `1.0` and `50` for 200 epochs. **The three curve shapes still appear and objectives 1, 2 and 3 are still met** — on data they can check line by line against the board.

**Cut:** the `tol=1e-8` subtlety. Match at sklearn's defaults, note that the weights agree to about two decimal places, and stop.

**Give them the loop with exactly three blanks**, and nothing else:

```python
        err = p - ________
        grad = np.array([np.mean(err * X[:, 0]), np.mean(______ * X[:, 1])])
        w -= lr * ________
```

**Those three blanks are the whole week.** Everything else in that file is material from Weeks 1 to 14.

**The version of the maths that skips the algebra.** Fill in a table for one knob. No letters, no formula:

| | prediction | truth | error = pred − truth | error × feature |
|:--:|:--:|:--:|:--:|:--:|
| row 1 | 0.5 | 0 | +0.5 | `+0.5 × 1 = +0.5` |
| row 2 | 0.5 | 0 | +0.5 | `+0.5 × 1 = +0.5` |
| row 3 | 0.5 | 1 | −0.5 | `−0.5 × 2 = −1.0` |
| row 4 | 0.5 | 1 | −0.5 | `−0.5 × 3 = −1.5` |
| | | | **add up** | **−1.5** |
| | | | **divide by 4** | **−0.375** |

Then one subtraction, on a card:

```
new weight  =  old weight  −  stride × slope
            =  0           −  1.0    × (−0.375)
            =  +0.375
```

**A student who can fill in that table twice — once for `w1`, once for `w2` — has done objective 2.** The word "gradient" can wait; what they need is that it is *a list of these*.

**The copy-this-exactly scaffold.** Twelve lines, runs alone, and it prints the four numbers from the board:

```python
import numpy as np

X = np.array([[1.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 1.0]])
y = np.array([0.0, 0.0, 1.0, 1.0])
w = np.array([0.0, 0.0])
b = 0.0

for round_number in range(4):
    p = 1.0 / (1.0 + np.exp(-((X * w).sum(axis=1) + b)))
    print("round", round_number, " loss =",
          round(float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))), 6))
    err = p - y
    w -= 1.0 * np.array([np.mean(err * X[:, 0]), np.mean(err * X[:, 1])])
    b -= 1.0 * np.mean(err)
```

```text
round 0  loss = 0.693147
round 1  loss = 0.581375
round 2  loss = 0.504824
round 3  loss = 0.448421
```

Then two questions: **"find those four numbers on the board"** — they are all there — and **"which line takes the step?"**

**One thing you must not cut:** the four-number checkpoint. If the whole lab collapses to one thing, make it *"my loop printed the same four numbers we worked out with a pencil."*

### If the student is flying

None of these need syntax from a later week.

1. **The largest safe learning rate** (harder variation 1). Sweep and measure with `np.all(np.diff(h) <= 1e-12)`. **The boundary is between 12 and 15** — `lr = 12` is monotone and lands on `0.3416`; `lr = 15` is not, and oscillates between `0.3557` and `0.3591` for ever. **And the punchline is the good bit: `lr = 12` gets to the bottom in about 8 epochs where `lr = 0.5` takes 100.** They have just discovered why anybody bothers tuning a learning rate.
2. **The gradient check** (harder variation 2). Nudge `w1` by `0.0001` each way and divide by `0.0002`. It agrees with the formula to about six decimals. **This is the most valuable technique of the next five weeks** — Week 18 makes it compulsory — and discovering it a lesson early is a real advantage.
3. **Read the model as English** (harder variation 3), including the honest caveat that comparing weights only works because Week 4's scaler put both columns on the same ruler.
4. **Explain the 0.82** (harder variation 4). Plot the data, look at it, and argue about how many of the 100 test rows a single straight line could never get. **Then keep their number and check it against Week 19's network.**
5. **Momentum** (harder variation 5), including the surprising part: it helps at small learning rates and makes large ones worse. Two sentences of explanation is a strong answer.
6. **The honest challenge:** *"make the loss go down without ever computing a gradient."* They can — pick a random direction, try a small step, keep it if the loss went down, otherwise try again. It works, and **it is unbelievably slow**, and measuring how much slower is the best possible argument for why anybody computes derivatives at all.

### If the student won't engage today

**Close the laptop. One sheet of paper, one calculator, and a game.**

Draw a valley on the paper — a big U — and put a dot on the left-hand slope.

> **"You're standing here. Thick fog. You want to get to the bottom and you can't see it. What can you actually do?"**

Let them get to "feel which way is downhill". Then:

> **"Right. So: downhill from here is which way?"**

Left or right — they will point. Then hand them the number:

> **"The slope here is minus 0.375. Negative slope means the ground drops as you go right. So you go right. How far?"**

Whatever they say, that is the learning rate, and it is the right answer to have an opinion about.

> **"You said one step. Fine. New position: `0 − 1 × (−0.375) = 0.375`. You've moved."**

Then do it once more with a slope of `−0.103`:

> **"`0.375 − 1 × (−0.103) = 0.478`. Notice something? The slope got smaller. What does that tell you about where you are?"**

Closer to the bottom — the ground is flattening out. **That is the whole algorithm and they just ran two rounds of it.**

Then, if they will take one more:

> **"Last one. What if your step was eight hundred instead of one?"**

`0 − 800 × (−0.375) = 300`. Point at where 300 is on the paper: **off the page, up the far side of the valley, higher than where they started.**

> **"That's called divergence, and it's why the size of the step is the most important number you'll ever pick."**

That is **objectives 2 and 3 delivered with a drawing of a valley**, in about ten minutes. The typing survives; next week uses all of it again.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — one slope, by hand (written, 2 minutes)**

> "Two rows. Row 1: feature is **2**, truth is **1**, the model said **0.6**. Row 2: feature is **4**, truth is **0**, the model said **0.3**. **Give me the slope for that weight**, and show the working."

*Good answer:*

```
errors:  0.6 − 1 = −0.4        0.3 − 0 = +0.3
× feature: −0.4 × 2 = −0.8     +0.3 × 4 = +1.2
add:  −0.8 + 1.2 = +0.4
÷ 2:  +0.2
```

**What to catch:** `truth − prediction` instead of `prediction − truth`. It gives `−0.2`, and then the update goes the wrong way. Ask back: *"which order did the board use?"*

**Check 2 — the update, and the sign (spoken, 60 seconds)**

> "A weight is currently **0.8**. Its slope is **+0.25**. The learning rate is **0.1**. What is the new weight, and **why did it go down?**"

*Good answer:* "`0.8 − 0.1 × 0.25 = 0.8 − 0.025 = 0.775`. It went down because the slope is positive, which means the loss *increases* as the weight increases — so to make the loss smaller you make the weight smaller."

**Full marks needs the reason, not just the arithmetic.** A student who gets 0.775 and cannot say why is at level 2.

**Check 3 — diagnose from a column of numbers (spoken, 90 seconds)**

> "Three training runs, and I will read you the losses at epoch 0, 100 and 500. **Name each one and give me the fix.**
> **Run A:** 0.6931, 0.6375, 0.5098.
> **Run B:** 0.6931, 0.3438, 0.3416.
> **Run C:** 0.6931, 2.7628, 7.8482."

*Good answer:* "A is **too small** — it is still falling at 500 and nowhere near B's final loss, so turn the learning rate up or run more epochs. B is **converged** — flat by 100, and extra epochs buy nothing. C has **diverged** — it went above the starting point and ended eleven times worse than knowing nothing, so divide the learning rate by 10 until the curve goes down every epoch."

**What to catch:** calling A "broken". **Nothing is broken about A** — it is a correct run that has not finished. That distinction is the difference between level 3 and level 4.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot compute one slope from a table of errors and features. Cannot say which way the update goes. Types the loop and cannot tell whether its output is right. |
| **2 — Emerging** | Computes one slope with the table scaffold. Applies the update when given the numbers. Gets the loop running from a partly-filled file and reaches the four checkpoint numbers with help. |
| **3 — Secure** | Does three rounds on paper unaided, all three knobs, every intermediate number. Types the loop and hits `0.693147 / 0.581375 / 0.504824 / 0.448421`. Names the three learning rates from their curves with evidence. Prints the sklearn comparison. **This is the target.** |
| **4 — Strong** | Explains why the loss should fall every epoch and measures it rather than eyeballing it. Distinguishes "too small" from "broken". Diagnoses a climbing loss as a sign error without prompting. Explains what `penalty=None` turns off, and why `tol` mattered. |
| **5 — Exceptional** | Finds the largest monotone learning rate by measurement and notices it is twenty times the "safe" default. Confirms a gradient by nudging, unprompted. Explains that the exact sklearn match is a consequence of convexity and predicts that it will stop happening once the model has layers. Argues that the 0.82 is a limitation of a straight boundary, and can say where the 18 misses come from. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, three parts, and the third is short and is the one I am marking hardest.
>
> **First, page 15.2 — finish the four-round table.** You did rounds 0 and 1 in class. Do rounds 2 and 3 at home, by hand, on the four rows from the board. **Every intermediate number:** all four `z` values, all four `p` values, all four errors, three slopes, three updates. Then check the whole thing against `three_rounds.py` and **put a tick or a cross beside every single number.** I want to see crosses. A page of forty ticks with no working is a page I do not believe.
>
> **Second, page 15.6 — match scikit-learn, printed side by side.** Your weights and theirs, in aligned columns, plus the biggest gap. Then do it again with `tol=1e-8` in sklearn's call and print both comparisons. **One sentence: whose 0.0025 was it, and how do you know?**
>
> **Third, page 15.7 — diagnose four loss curves.** I give you four tables of numbers. For each one: **the name** — too small, too big, converged, or diverged — **the evidence you used**, and **the fix, in one line.** Four names, four pieces of evidence, four fixes.
>
> And the evidence is the part I am marking. **'It looks wrong' is not evidence. 'It rises between epoch 100 and 101' is.**"

**Workbook pages:** 15.1, 15.3, 15.4 and 15.5 in class · **15.2, 15.6 and 15.7** at home · **15.8** stretch, for anyone who wants to find the largest safe learning rate by measurement.

**Expected time:** 25 min on rounds 2 and 3 with the check · 15 min on the sklearn match · 20 min on the four diagnoses. **About an hour.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — are all the intermediate numbers on page 15.2, with ticks and crosses?** Three slopes and three updates per round is the minimum; a page with only the final weights has skipped the objective. Watch for the bias in round 0: its slope must be **exactly** 0.000000, and a student who writes 0.0001 has an arithmetic slip worth finding. **Two — does the sentence about `tol` say whose gap it was?** The answer is scikit-learn's, and the evidence is that tightening *their* tolerance closed it while our loop never changed. A student who writes *"we were slightly less accurate"* has it backwards. **Three — is the evidence in part three actually evidence?** For the "too big" curve the evidence is that consecutive epochs alternate — `0.3557, 0.3591, 0.3557, 0.3591` — which you can only see by looking at consecutive rows rather than every fiftieth. **A student who spots that has learned the most useful debugging habit in the whole term**, and it is worth saying so in the margin.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 15.1 — Warm-up: which way does the weight move?

*For each row, say whether the weight goes up or down, and give the new value. `lr = 0.1` throughout.*

| # | Weight now | Its slope | Up or down? | New weight |
|:--:|:--:|:--:|---|:--:|
| 1 | `0.80` | `+0.25` | **down** — positive slope means the loss grows as the weight grows | `0.80 − 0.1 × 0.25 = 0.775` |
| 2 | `0.80` | `−0.25` | **up** — negative slope means the loss shrinks as the weight grows | `0.80 − 0.1 × (−0.25) = 0.825` |
| 3 | `0.00` | `−0.375` | **up** | `0.00 − 0.1 × (−0.375) = 0.0375` |
| 4 | `−0.50` | `+1.20` | **down** | `−0.50 − 0.1 × 1.20 = −0.62` |
| 5 | `2.00` | `0.00` | **neither** | `2.00 − 0.1 × 0 = 2.00` — a zero slope means flat ground; nothing to do |

**The question on the page:** *"Row 5's slope is zero. Is that good or bad?"*

**It is what the bottom looks like** — at the lowest point of a bowl the ground is level, so the slope is zero and the weight stops moving. **But it is also what a stuck model looks like**, and today you saw one: in round 0 the bias's slope was exactly zero and the bias did not move, even though it was nowhere near its final value. **A zero slope means "no reason to move *right now*", not "we have arrived".**

### Page 15.2 — The four-round table (rounds 0–1 in class, 2–3 at home)

`X = [[1,1], [1,2], [2,1], [3,1]]`, `y = [0, 0, 1, 1]`, start at all zeros, `lr = 1.0`.

**Round 0**

```
w = [0.000000, 0.000000]   b = 0.000000

z   = [0, 0, 0, 0]                      (everything is multiplied by zero)
p   = [0.5, 0.5, 0.5, 0.5]              (sigmoid(0) is exactly a half)
loss = −ln(0.5) averaged = 0.693147

err = [+0.5, +0.5, −0.5, −0.5]

slope w1 = (0.5×1 + 0.5×1 − 0.5×2 − 0.5×3) ÷ 4 = (0.5+0.5−1.0−1.5) ÷ 4 = −1.5 ÷ 4 = −0.375000
slope w2 = (0.5×1 + 0.5×2 − 0.5×1 − 0.5×1) ÷ 4 = (0.5+1.0−0.5−0.5) ÷ 4 = +0.5 ÷ 4 = +0.125000
slope b  = (0.5 + 0.5 − 0.5 − 0.5) ÷ 4         = 0.0 ÷ 4                          =  0.000000

w1 ← 0.000000 − 1.0 × (−0.375000) = +0.375000
w2 ← 0.000000 − 1.0 × (+0.125000) = −0.125000
b  ← 0.000000 − 1.0 × ( 0.000000) =  0.000000
```

**Round 1**

```
w = [0.375000, -0.125000]   b = 0.000000

z   = [0.250000, 0.125000, 0.625000, 1.000000]
p   = [0.562177, 0.531209, 0.651355, 0.731059]
loss = 0.581375

err = [+0.562177, +0.531209, −0.348645, −0.268941]

slope w1 = −0.102682     slope w2 = +0.251752     slope b = +0.118950

w1 ← 0.375000 − 1.0 × (−0.102682) = 0.477682
w2 ← −0.125000 − 1.0 × (+0.251752) = −0.376752
b  ← 0.000000 − 1.0 × (+0.118950) = −0.118950
```

**Round 2**

```
w = [0.477682, -0.376752]   b = -0.118950

z   = [-0.018020, -0.394772, 0.459662, 0.937344]
p   = [ 0.495495,  0.402569, 0.612934, 0.718563]
loss = 0.504824

err = [+0.495495, +0.402569, −0.387066, −0.281437]

slope w1 = −0.180095     slope w2 = +0.158033     slope b = +0.057390

w1 ← 0.477682 − 1.0 × (−0.180095) = 0.657777
w2 ← −0.376752 − 1.0 × (+0.158033) = −0.534785
b  ← −0.118950 − 1.0 × (+0.057390) = −0.176340
```

**Round 3**

```
w = [0.657777, -0.534785]   b = -0.176340

z   = [-0.053348, -0.588133, 0.604429, 1.262206]
p   = [ 0.486666,  0.357063, 0.646669, 0.779406]
loss = 0.448421

err = [+0.486666, +0.357063, −0.353331, −0.220594]

slope w1 = −0.131179     slope w2 = +0.156717     slope b = +0.067451

w1 ← 0.657777 − 1.0 × (−0.131179) = 0.788956
w2 ← −0.534785 − 1.0 × (+0.156717) = −0.691502
b  ← −0.176340 − 1.0 × (+0.067451) = −0.243791
```

**The loss column, which is the point of the page:**

```
0.693147  →  0.581375  →  0.504824  →  0.448421
```

**Down every single round.**

**The three questions on the page:**

**(a) Why was the bias's slope exactly zero in round 0 and not afterwards?**

Because in round 0 every prediction was 0.5 and two rows were late while two were not, so the four errors were `+0.5, +0.5, −0.5, −0.5` and they cancelled exactly. From round 1 onwards the predictions differ from each other, so the errors no longer cancel. **The bias only moves when the average prediction is off from the average label.**

**(b) `w2` goes 0 → −0.125 → −0.377 → −0.535 → −0.692. What is the model learning?**

`w2` is "riders free". It is becoming more and more negative, which means **the model has worked out that more riders standing free makes an order *less* likely to be late.** A negative weight is the model disagreeing with a feature, and it is one of the most readable things about a linear model.

**(c) Between rounds 0 and 1 the loss fell by 0.1118. Between 2 and 3 it fell by 0.0564. Why is the improvement shrinking?**

Because the slopes are shrinking as the weights get closer to the bottom of the bowl — `slope w1` went from `−0.375` to `−0.103` to `−0.180` to `−0.131`. **Flatter ground means smaller steps means smaller improvements.** That is what approaching a minimum looks like, and it is why `lr = 0.5` was flat by epoch 100 rather than stopping dead at some particular epoch.

The check, and its real output — the complete file is in the Prep Checklist, and its full output is printed there.

### Page 15.3 — Predict the output

*Write what each block prints before you run it.*

**P1**

```python
import numpy as np
X = np.array([[1.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 1.0]])
w = np.array([0.5, -0.25])
print(X * w)
print((X * w).sum(axis=1))
```

```text
[[ 0.5  -0.25]
 [ 0.5  -0.5 ]
 [ 1.   -0.25]
 [ 1.5  -0.25]]
[0.25 0.   0.75 1.25]
```

**`X * w` keeps the grid shape** — every row multiplied item by item. `.sum(axis=1)` collapses each row to one number. Four rows in, four numbers out.

**P2 — the trap**

```python
import numpy as np
X = np.array([[1.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 1.0]])
w = np.array([0.5, -0.25])
print((X * w).sum())
print(np.shape((X * w).sum()))
```

```text
2.25
()
```

**`.sum()` with no axis adds up everything** and gives one number, with shape `()` — no rows at all. **This is the bug that hides for three lines and then explodes.** `axis=1` keeps the rows.

**P3**

```python
import numpy as np
X = np.array([[1.0, 1.0], [1.0, 2.0], [2.0, 1.0], [3.0, 1.0]])
print(X[:, 0])
print(X[:, 1])
```

```text
[1. 1. 2. 3.]
[1. 2. 1. 1.]
```

`X[:, 0]` is "every row, column 0". These two are the two feature columns, and they are what the errors get multiplied by.

**P4**

```python
import numpy as np
h = [0.6931, 0.5814, 0.5048, 0.4484]
print(np.diff(h))
print(np.all(np.diff(h) <= 0))
```

```text
[-0.1117 -0.0766 -0.0564]
True
```

**`np.diff` gives the gaps.** All three are negative, so the loss fell every round, so `np.all(... <= 0)` is `True`. **That is the whole `downhill?` test in one line.**

**P5 — the hard one**

```python
import numpy as np
w = np.array([0, 0])
w -= 0.5 * np.array([0.1, 0.2])
```

```text
Traceback (most recent call last):
  File "p5.py", line 3, in <module>
    w -= 0.5 * np.array([0.1, 0.2])
numpy.core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'subtract' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```

**`np.array([0, 0])` has no decimal points**, so numpy made a whole-number box and then refused to store `−0.05` in it. **Two characters fix it:** `np.array([0.0, 0.0])`.

### Page 15.4 — `descent.py` (done in class)

The complete file:

```python
"""descent.py - logistic regression trained by our own gradient descent."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(0)

X, y = make_classification(n_samples=400, n_features=2, n_informative=2,
                           n_redundant=0, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
scaler = StandardScaler().fit(X_tr)
X_tr = scaler.transform(X_tr)
X_te = scaler.transform(X_te)


def squash(z):
    e = np.exp(np.where(z >= 0, -z, z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))


def train(X, y, lr, n_epochs):
    w = np.array([0.0, 0.0])
    b = 0.0
    history = []
    for epoch in range(n_epochs):
        p = squash((X * w).sum(axis=1) + b)
        p = np.clip(p, 1e-12, 1 - 1e-12)
        history.append(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
        err = p - y
        grad = np.array([np.mean(err * X[:, 0]), np.mean(err * X[:, 1])])
        w -= lr * grad
        b -= lr * np.mean(err)
    return w, b, history


print("X_tr shape:", X_tr.shape, "  X_te shape:", X_te.shape)
print()
print("%8s %9s %9s %9s %9s %9s" % ("lr", "epoch 0", "epoch 100", "final",
                                   "worst", "downhill?"))
for lr in (0.005, 0.5, 800.0):
    w, b, h = train(X_tr, y_tr, lr, 500)
    h = np.array(h)
    downhill = bool(np.all(np.diff(h) <= 1e-12))
    print("%8.3f %9.4f %9.4f %9.4f %9.4f %9s"
          % (lr, h[0], h[100], h[-1], h.max(), str(downhill)))

w, b, h = train(X_tr, y_tr, 0.5, 2000)
pred = (squash((X_te * w).sum(axis=1) + b) >= 0.5).astype(int)
print()
print("lr = 0.5, 2000 epochs")
print("   my w =", np.round(w, 4), "  my b =", round(b, 4))
print("   final training loss = %.4f" % h[-1])
print("   test accuracy       = %.4f" % float((pred == y_te).mean()))
```

Real output. **Runtime under 2 seconds for all 3,500 epochs.**

```text
X_tr shape: (300, 2)   X_te shape: (100, 2)

      lr   epoch 0 epoch 100     final     worst downhill?
   0.005    0.6931    0.6375    0.5098    0.6931      True
   0.500    0.6931    0.3438    0.3416    0.6931      True
 800.000    0.6931    2.7628    7.8482   12.1169     False

lr = 0.5, 2000 epochs
   my w = [-0.6221  3.0924]   my b = 0.2271
   final training loss = 0.3416
   test accuracy       = 0.8200
```

**Count the lines in `train`: thirteen, including the `def` and the `return`. Add the three-line `squash` and you have sixteen.** That is the whole of `fit()`. The other thirty-odd lines of the file are generating data, splitting it, scaling it and printing tables — all Weeks 1 to 4.

### Page 15.5 — Name the three learning rates (done in class)

| `lr` | Final loss | Worst loss | Downhill every epoch? | **Name** | Evidence | Fix |
|:--:|:--:|:--:|:--:|---|---|---|
| `0.005` | 0.5098 | 0.6931 | `True` | **too small** | Still falling at epoch 500 and its final loss is 0.17 above what `lr = 0.5` reached. **Nothing is broken; it did not finish.** | Turn the learning rate up, or run many more epochs. |
| `0.5` | 0.3416 | 0.6931 | `True` | **converged** | Flat from about epoch 100 (0.3438 → 0.3416 over 400 epochs) and monotone throughout. | Nothing. Extra epochs cost time and buy nothing. |
| `800` | 7.8482 | **12.1169** | `False` | **diverged** | Went **above** its starting point, peaked at 12.1169, and ended eleven times worse than a model that knows nothing. | Divide by 10 until the curve is monotone, then use the largest value that still is. |

**The three questions on the page:**

**(a) Why does every run start at exactly 0.6931?**

Every weight starts at zero, so every raw score is zero, so every probability is exactly 0.5, so every row's loss is `−ln(0.5) = 0.693147`. **Week 14's number, arriving in every training run there will ever be.**

**(b) `lr = 0.005` and `lr = 0.5` both show `True` in the downhill column. Are they equally good?**

No. **Monotone means safe, not finished.** `lr = 0.005` never went up, and it also never arrived: 0.5098 against 0.3416. **`downhill? True` is a safety check, not a success check** — you need the final loss as well.

**(c) `lr = 800`'s worst loss is 12.1169. What does a loss of 12 mean?**

It means the model is confidently, catastrophically wrong on many rows. `−ln(p) = 12` means `p = e^(−12) = 0.0000061` — a six-millionths chance given to something that happened. **A loss of 12 is not "a bit worse than 0.69"; it is a model that has become an anti-predictor**, and if you thresholded it at 0.5 you would do better by flipping every answer.

**And the plot that goes with this page.** The complete `curves.py`:

```python
"""curves.py - three learning rates on one log-scale plot, and the boundary moving."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(0)

X, y = make_classification(n_samples=400, n_features=2, n_informative=2,
                           n_redundant=0, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
scaler = StandardScaler().fit(X_tr)
X_tr = scaler.transform(X_tr)


def squash(z):
    e = np.exp(np.where(z >= 0, -z, z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))


def train(X, y, lr, n_epochs, w0, b0):
    w = np.array(w0)
    b = b0
    history = []
    snapshots = []
    for epoch in range(n_epochs):
        p = np.clip(squash((X * w).sum(axis=1) + b), 1e-12, 1 - 1e-12)
        loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        history.append(loss)
        if epoch in (0, 50, 150, 300):
            snapshots.append((epoch, w.copy(), b, loss))
        err = p - y
        w -= lr * np.array([np.mean(err * X[:, 0]), np.mean(err * X[:, 1])])
        b -= lr * np.mean(err)
    return w, b, history, snapshots


fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.5))

for lr in (0.005, 0.5, 800.0):
    _, _, h, _ = train(X_tr, y_tr, lr, 500, [0.0, 0.0], 0.0)
    left.plot(h, label="lr = %g" % lr)
left.axhline(np.log(2), color="grey", linestyle="--", linewidth=1,
             label="ln 2 = 0.6931")
left.set_yscale("log")
left.set_xlabel("epoch")
left.set_ylabel("training log loss (log scale)")
left.set_title("Three learning rates")
left.legend(fontsize=8)

_, _, _, snaps = train(X_tr, y_tr, 0.5, 301, [2.0, -2.0], 1.0)
right.scatter(X_tr[y_tr == 0, 0], X_tr[y_tr == 0, 1], s=12, marker="o",
              label="on time")
right.scatter(X_tr[y_tr == 1, 0], X_tr[y_tr == 1, 1], s=12, marker="^",
              label="late")
xs = np.linspace(-3.0, 3.0, 50)
print("epoch       w1        w2         b      loss")
for epoch, ww, bb, ll in snaps:
    print("%5d %9.4f %9.4f %9.4f %9.4f" % (epoch, ww[0], ww[1], bb, ll))
    right.plot(xs, -(ww[0] * xs + bb) / ww[1], linewidth=1.3,
               label="epoch %d" % epoch)
right.set_ylim(-3.2, 2.7)
right.set_xlim(-3.0, 3.2)
right.set_xlabel("feature 1 (standardised)")
right.set_ylabel("feature 2 (standardised)")
right.set_title("The boundary walking into place")
right.legend(fontsize=7)

plt.tight_layout()
plt.savefig("descent.png", dpi=120)
print("wrote descent.png")
```

Real output. **Runtime about 1.4 seconds, including both panels.**

```text
epoch       w1        w2         b      loss
    0    2.0000   -2.0000    1.0000    2.0454
   50   -0.2798    2.1091    0.0902    0.3590
  150   -0.5478    2.8694    0.1883    0.3423
  300   -0.6110    3.0587    0.2211    0.3416
wrote descent.png
```

**What you should see in `descent.png`.** Left panel: three curves on a **log** vertical axis. The orange `lr = 0.5` curve dives almost vertically and flattens just under 0.35. The blue `lr = 0.005` curve sags gently and is still sagging at epoch 500. The green `lr = 800` curve leaps straight over the dashed `ln 2` line in one epoch and then thrashes between about 2 and 12 for the remaining 499. Right panel: the epoch-0 line cuts steeply across the data at completely the wrong angle, and the other three lie almost on top of each other, nearly flat, with circles below and triangles above.

> **⚠️ Watch out:** `matplotlib.use("Agg")` **must come before** `import matplotlib.pyplot`. It tells matplotlib to draw into a file rather than trying to open a window, which is what you want on a machine with no display and what stops the program appearing to hang.

### Page 15.6 — Match scikit-learn (homework)

The complete file:

```python
"""match.py - my 25 lines against scikit-learn's."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

np.random.seed(0)

X, y = make_classification(n_samples=400, n_features=2, n_informative=2,
                           n_redundant=0, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
scaler = StandardScaler().fit(X_tr)
X_tr, X_te = scaler.transform(X_tr), scaler.transform(X_te)


def squash(z):
    e = np.exp(np.where(z >= 0, -z, z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))


w = np.array([0.0, 0.0])
b = 0.0
lr = 0.5
for epoch in range(20000):
    p = np.clip(squash((X_tr * w).sum(axis=1) + b), 1e-12, 1 - 1e-12)
    err = p - y_tr
    w -= lr * np.array([np.mean(err * X_tr[:, 0]), np.mean(err * X_tr[:, 1])])
    b -= lr * np.mean(err)

loose = LogisticRegression(penalty=None, max_iter=5000).fit(X_tr, y_tr)
tight = LogisticRegression(penalty=None, max_iter=5000, tol=1e-8).fit(X_tr, y_tr)

print("                      weight 1    weight 2        bias")
print("mine (20000 epochs) %11.6f %11.6f %11.6f" % (w[0], w[1], b))
print("sklearn, default    %11.6f %11.6f %11.6f"
      % (loose.coef_[0][0], loose.coef_[0][1], float(loose.intercept_[0])))
print("sklearn, tol=1e-8   %11.6f %11.6f %11.6f"
      % (tight.coef_[0][0], tight.coef_[0][1], float(tight.intercept_[0])))
print()
print("biggest gap vs default   : %.6f" % float(np.max(np.abs(w - loose.coef_[0]))))
print("biggest gap vs tol=1e-8  : %.6f" % float(np.max(np.abs(w - tight.coef_[0]))))
```

(`np.abs` strips the minus sign off every number in a list, so `np.max(np.abs(...))` is "the biggest disagreement, ignoring which way round it was". It is the only place it appears today.)

Real output. **Runtime about 1 second for 20,000 epochs.**

```text
                      weight 1    weight 2        bias
mine (20000 epochs)   -0.622142    3.092423    0.227114
sklearn, default      -0.621309    3.089931    0.226750
sklearn, tol=1e-8     -0.622142    3.092423    0.227114

biggest gap vs default   : 0.002492
biggest gap vs tol=1e-8  : 0.000000
```

**The four questions on the page:**

**(a) Whose 0.0025 was it, and how do you know?**

**scikit-learn's.** The evidence is that our loop never changed between the two comparisons — the only thing that changed was scikit-learn's stopping rule. Tightening `tol` from `1e-4` to `1e-8` moved *their* answer onto ours, to all six printed decimal places. **If the gap had been our error, tightening their tolerance would have made it worse, not zero.**

**(b) Why does `penalty=None` matter?**

By default `LogisticRegression` applies **L2 regularisation** — it deliberately handicaps the model by adding a penalty for large weights, so it cannot overfit by leaning hard on one feature. That shrinks the weights towards zero, so a regularised model will never match an unregularised one. **We are comparing training loops, so both sides must be unhandicapped.**

**(c) Is it a problem that scikit-learn stops early?**

No, and this is the honest answer. Both versions score **exactly 0.8200** on the test set, so the last 0.0025 of a weight changed no prediction at all. **Stopping early trades an amount of precision that does not matter for time that does.** The valuable thing is not that they agree — it is that you can now *tell* they disagree, and turn it off.

**(d) We wrote 25 lines and matched a professional library. Does that mean our loop is as good as theirs?**

**No, and this is worth being precise about.** We matched the *answer*, not the *method*. Ours took 20,000 steps; scikit-learn's L-BFGS took a few dozen, because it builds up a picture of the shape of the bowl as it goes and uses it to take much better steps.

We matched because **the loss is convex** — one bowl, one bottom — so there is exactly one right answer and any correct method must find it. **What we proved is that our method is correct, not that it is efficient.**

And the interesting footnote: neural networks do not use L-BFGS, because it needs too much memory when there are millions of weights. **They use variants of the loop you just wrote.** So these 25 lines are closer to how a real network trains than scikit-learn's optimiser is.

### Page 15.7 — Diagnose four loss curves (homework)

*Four training runs, all on the same data. Name each, give your evidence, and give the fix in one line.*

Here are the four tables as the student sees them. **Note the two extra columns of consecutive epochs — they are there on purpose.**

| Curve | ep 0 | ep 1 | ep 2 | ep 3 | ep 100 | ep 101 | ep 102 | ep 103 | ep 250 | ep 499 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **A** | 0.6931 | 0.6925 | 0.6919 | 0.6913 | 0.6375 | 0.6370 | 0.6365 | 0.6360 | 0.5757 | 0.5098 |
| **B** | 0.6931 | 0.6342 | 0.5889 | 0.5537 | 0.3438 | 0.3438 | 0.3437 | 0.3437 | 0.3417 | 0.3416 |
| **C** | 0.6931 | 0.4485 | 0.3684 | 0.3571 | 0.3557 | 0.3591 | 0.3557 | 0.3591 | 0.3557 | 0.3591 |
| **D** | 0.6931 | 3.5719 | 3.3446 | 3.5101 | 2.7628 | 3.1164 | 8.8994 | 6.4570 | 7.1064 | 7.8482 |

**Curve A — too small.** *(This was `lr = 0.005`.)*

**Evidence:** it falls at every single epoch and never rises, so nothing is unstable. But the drop per epoch is tiny — `0.0006` between epoch 0 and 1 — and at epoch 499 it is still falling and still 0.17 above what curve B reached. **A correct run that has not finished.**

**Fix:** turn the learning rate up — multiply by 10 and check it is still monotone — or run far more epochs.

**Curve B — converged.** *(This was `lr = 0.5`.)*

**Evidence:** falls fast, monotone throughout, and essentially flat from epoch 100 onwards: it improves by `0.0022` over the last 400 epochs. The consecutive columns confirm there is no wobble — `0.3438, 0.3438, 0.3437, 0.3437`.

**Fix:** none. Stop earlier if you want the time back.

**Curve C — too big.** *(This was `lr = 15`.)*

**Evidence, and this is the discriminating one:** it looks converged if you only read epochs 0, 100, 250 and 499 — it sits at about 0.356 the whole way. But **read the consecutive columns**: `0.3557, 0.3591, 0.3557, 0.3591`. It is **alternating**, for ever, between two values either side of the bottom. It never lands. And its final loss (0.3591) is worse than curve B's (0.3416).

**Fix:** divide the learning rate by 2 or 3. **You lose almost nothing** — this run got most of the way down in three epochs — but you gain the last 0.0175.

**Curve D — diverged.** *(This was `lr = 800`.)*

**Evidence:** it went **above its starting point immediately** — 0.6931 to 3.5719 in one epoch — never came back below 2, spiked to 8.8994 at epoch 102, and ended at 7.8482, which is **eleven times worse than a model that knows nothing.** The steps are so long that it leaps across the valley and up the far side every time.

**Fix:** divide the learning rate by 10 repeatedly until the curve is monotone, then use the largest value that still is.

**The two questions on the page:**

**(a) Which two curves would you have called "converged" if you had only been given epochs 0, 100, 250 and 499?**

**B and C.** At those four epochs C reads `0.6931, 0.3557, 0.3557, 0.3591` and looks flat and settled. **Only the consecutive rows expose the alternation.** This is the whole reason the `downhill?` measurement exists: `np.all(np.diff(h) <= 1e-12)` returns `False` for C and `True` for B, and no amount of squinting at a plot would have told you.

**(b) Curve D's loss at epoch 1 is 3.5719. What did the weights do in that one epoch?**

They took a step 800 times the gradient. The gradient at the start is `[−0.0051, −0.3545]` on this data, so `w2` alone leapt from `0` to `800 × 0.3545 = 283.6`. **Raw scores in the hundreds make probabilities of essentially 0 or 1**, so every row that the model got wrong contributed an enormous surprise. **A single step turned a know-nothing model into a confidently wrong one.**

### Page 15.8 — The largest safe learning rate (stretch)

*Sweep the learning rate and find the biggest one whose loss still falls every single epoch.*

```python
for lr in (1.0, 3.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0):
    _, _, h = train(X_tr, y_tr, lr, 500)
    h = np.array(h)
    print("lr=%-5g  worst %.4f  final %.4f  downhill %s"
          % (lr, h.max(), h[-1], bool(np.all(np.diff(h) <= 1e-12))))
```

Real output:

```text
lr=1      worst 0.6931  final 0.3416  downhill True
lr=3      worst 0.6931  final 0.3416  downhill True
lr=8      worst 0.6931  final 0.3416  downhill True
lr=10     worst 0.6931  final 0.3416  downhill True
lr=12     worst 0.6931  final 0.3416  downhill True
lr=15     worst 0.6931  final 0.3591  downhill False
lr=20     worst 0.6931  final 0.5115  downhill False
lr=30     worst 1.5311  final 0.8175  downhill False
```

**The largest safe learning rate on this problem is between 12 and 15.**

**The three questions on the page:**

**(a) How many epochs does `lr = 12` need to reach 0.3416, and how many does `lr = 0.5` need?**

`lr = 12` is essentially there by **epoch 8** (its first eight losses are `0.6931, 0.4018, 0.3495, 0.3456, 0.3439, 0.3429, 0.3423, 0.3420`). `lr = 0.5` needs about **100**. **Twenty-four times the stride bought about twelve times the speed, and it was still perfectly safe.**

**(b) So why would anybody use `lr = 0.5`?**

Because on a problem where you do not already know the answer, **you cannot tell 12 from 15 without trying**, and 15 costs you a permanently worse final loss. `0.5` is slow and unmistakably safe. **On a training run that costs an hour you tune; on one that costs a second you do not bother.**

**(c) `lr = 30` has a worst loss of 1.5311, above its starting point. `lr = 20` has a worst loss of 0.6931. Is `lr = 20` therefore safe?**

**No, and this is the trap in the question.** `lr = 20` never went above its *starting* value, so "worst loss" looks innocent — but `downhill` is `False`, which means it rose *somewhere*, and its final loss of 0.5115 is far worse than 0.3416. **"Worst loss ≤ starting loss" is a much weaker test than "went down every epoch".** Use the strong one.

### Answers to every question posed in the lesson

**Hook — "What happened in that second?"**
Five lines: start every weight at zero; compute a probability per row (Week 13); compute the loss (Week 14); work out which way is downhill for each weight (Week 12); step each weight a little way downhill; repeat.

**Hook — "Which of those five can you already do?"**
Four of the five. Only step 4 — one slope per knob — is new.

**Hook — "What is the loss on the very first step?"**
`0.6931`. All weights zero → all raw scores zero → all probabilities exactly 0.5 → `−ln(0.5) = 0.693147`.

**Concept — "Where are the logarithms? Where are the exponentials?"**
They cancel exactly when you work out the slope of log loss applied to a sigmoid. What is left is `prediction − truth`, times the feature, averaged. **That cancellation is why sigmoid and log loss are always used together.**

**Concept — "All three knobs are zero. What is `z` for row 1? For row 4?"**
Zero for both — every feature is multiplied by a weight of zero.

**Concept — "So what is `p` for all four rows?"**
Exactly 0.5. Week 13's third property.

**Concept — "Why did rows 3 and 4 come out negative?"**
Those two rows were late (`y = 1`) and the model said 0.5, so `p − y = −0.5`.

**Concept — "Why is row 4's contribution the biggest?"**
Its feature is 3, the largest of the four. **Rows with big features get the biggest say in that weight** — it is a fair blame rule.

**Concept — "The bias slope is exactly zero. Why?"**
Two rows late and two on time, and every prediction 0.5, so the four errors were `+0.5, +0.5, −0.5, −0.5` and cancelled exactly. The bias only moves when the average prediction is off from the average label.

**Concept — "`w1`'s slope was negative and `w1` went up. Is that right?"**
Yes. A negative slope means the loss falls as the weight rises, so up *is* downhill. `0 − 1.0 × (−0.375) = +0.375`.

**Concept — "The bias has moved off zero in round 1. Why now?"**
Because the four predictions are no longer identical, so the errors no longer cancel.

**Live-code — "`int64` and `float64`. Which is which, and which is my `w`?"**
`int64` is whole numbers, `float64` is decimals. `w = np.array([0, 0])` made an `int64` array, and numpy refused to store `−0.1875` in it rather than silently rounding.

**Live-code — "Any error message? What is happening?" (`w += lr * grad`)**
No error at all. The loss climbs — `0.693147, 0.759960, 0.844350, 0.949854, 1.079249` — because the gradient points uphill and we are following it deliberately.

**Live-code — "Read the first column. What do all three have in common?"**
All three start at `0.6931`, because all three start with every weight at zero.

**Live-code — "Name each row."**
`0.005` is **too small** (still falling at 500, final 0.5098). `0.5` is **converged** (flat by 100, `downhill? True`). `800` is **diverged** (`downhill? False`, worst 12.1169, ended eleven times worse than knowing nothing).

**Live-code — "The `lr = 800` curve reaches 12 and the others live near 0.4. What will this picture look like?"**
Two flat lines squashed against the bottom of the axes and one spike. A log scale gives every ratio the same room and fixes it.

**Activity — "The gap was 0.0025 and now it is zero. Whose 0.0025 was it?"**
scikit-learn's. Its default `tol=1e-4` stopped it a little short of the bottom, on purpose. Our loop never changed.

**Activity — "The line is basically right by epoch 50. Why run another 250 epochs?"**
Because the loss was still falling — 0.3590 to 0.3416 — even though the picture barely moves. **A picture is not a measurement.**

---

## 🔮 Next Week Preview

Next week the model stops being a single line. The student meets **one neuron by hand** — which turns out to be exactly what they built today, three things they can already do: multiply each input by a weight, add them up with a bias, then squash. What is new is that the squash no longer has to be the sigmoid, and that you are allowed to have **more than one** of them. The maths is **the shape of a grid of numbers** — rows × columns, written `(3, 2)` — counted off a real printout and established as the first thing you print whenever anything is confusing. Six neuron outputs get computed by hand for ReLU, sigmoid and tanh, eighteen numbers in all, and all eighteen get checked in numpy.

**To prep early:** two things, and the first matters most. **One:** leave today's `w ← w − lr × slope` on the board and do not rub it out for the rest of the term — every model from here to Week 36 is trained by that line, and pointing at it in Week 26 while a convolutional network trains is worth ten minutes of explanation. **Two:** print today's test accuracy, `0.8200`, and pin it somewhere visible. **That number is the whole argument for the next four weeks**, and in Week 19 the class will beat it with a boundary that curves. Nothing new to install.
