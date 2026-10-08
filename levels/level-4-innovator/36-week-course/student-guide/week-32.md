# Week 32 — The Proxy Is Not the Goal: Calibration and Abstention

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Workbook](../workbook/week-32.md)

---

![Thirty-six week tiles in four lanes of nine, one per term; weeks 1 to 31 solid, Week 32 (a teach week in term 4) tinted pink with a thick border and a pointer, weeks 33 to 36 dashed](../figures/fig-w32-0-where-this-fits.svg)

*Figure 32.0 — Week 32 of 36: a teach week in term 4, agents, evidence and the system card.*

---

> ### This week in one sentence
> **The score you push up (accuracy) is a stand-in for what you wanted (a system you can trust when it sounds sure), so measure how far "I'm 90% sure" is from "right 90% of the time", let the system say "I don't know", and still read the result by category.**
>
> **By the end of this chapter you will be able to:**
> - **Say what a proxy is**, and name the proxy and the real goal in this week's data
> - **Compute a Brier score and an ECE by hand** on ten results, then by code on forty, and check the code against `brier_score_loss`
> - **Build a reliability table**: for each bucket of stated confidence, how sure the system said it was and how often it was right
> - **Add an abstain threshold** and read the trade: fewer questions answered, better accuracy on the ones that were
> - **Find a category that fell while the average rose**, and say it in *results*
> - **Say why "pick the threshold with the best accuracy" is the wrong rule**
>
> **New maths:** **the calibration gap**: how far a stated probability is from how often it came true.
>
> **New syntax:** `np.digitize` · `np.bincount` (with `minlength=` and `weights=`) · `brier_score_loss`
>
> **Reading time:** about 25 minutes. **In class:** 70 minutes. **Homework:** about 55 minutes (workbook pages 32.1 to 32.3).

> **📌 About the code blocks.** Put the blocks in **one file**, `week32.py`, in the order they appear, or paste them into one Python session. Later blocks use names made by earlier ones. You need numpy, scikit-learn and matplotlib, which you already have. **Nothing in this week is random**: you type the 40 results yourself, so every number you print should match the ones shown here exactly. If one differs, you have a typo in the sheet; check `accuracy 0.575` first. Nothing needs the internet, and every block runs in about a second.

> **⚠️ The 40 results are invented.** Your teacher wrote them to have a shape worth measuring. They are **not the output of any model.** They stand in for the log of a support-ticket classifier that reports its top label and how sure it is. **Nothing measured on them says anything about a real model.** What you take away is a *method*: the table, the threshold, the per-category check.

---

## 🪝 Start Here

A forecaster says "80% chance of rain" on a hundred different mornings. It rained on 55 of them. Is the forecaster wrong?

On any one morning you cannot say. Over the hundred, the forecaster said more than they delivered. Now suppose I only tell you how many mornings they got *right*. Could you tell whether they were honest about how sure they were? No. **Right answers** and **honest about being sure** are two different numbers, and today you measure the second one.

Before any code, write three guesses on a card.

1. A system is right on 23 of 40 questions. When it says "I'm 93% sure", how often do you think it is right: about 93%, a bit less, or a lot less?
2. If it may say "I don't know" below some level of sureness, will its accuracy on the questions it *does* answer go up, down, or stay the same?
3. If overall accuracy goes up when it starts refusing, can one category have gone *down*?

Keep the card. We come back to it at the end.

---

## 🧠 The Big Idea

This section defines the words the rest of the week uses: proxy, result, calibrated, abstaining, coverage.

**A proxy.** You cannot measure "I can trust this when it sounds sure" directly. You measure what you can: *how often the answer was right*. That number is a **proxy**: a stand-in for the thing you want. A proxy is useful until you start chasing it.

**A result** is a pair: how sure the system said it was, `p` (a number from 0 to 1, called its **confidence**), and what happened, `y` (1 if it was right, 0 if wrong).

**Calibrated** means: of the results where it said about 0.8, about 8 in 10 were right. The stated number matches the hit rate.

A system that says 0.8 and is right 5 times in 10 is **overconfident**. "Calibrated" does not mean "right": a system that says 0.6 and is right 6 times in 10 is calibrated, and wrong 4 times in 10.

**Abstaining** means answering only when `p` is at or above a **threshold** `t`, and otherwise saying "I don't know". Two words measure it:

- **Coverage:** the share of questions it answered.
- **Accuracy of the answered:** the share of *those* that were right.

Raise `t` and coverage falls. If the confidence means anything, accuracy of the answered rises. Nothing is free: a question it declines is a question it does not answer, right or wrong.

---

## 🔢 The maths: the calibration gap

This section gives you the week's one new maths idea, in three steps. You will do steps (b) and (c) with a pencil on ten results before the computer touches them.

**(a) The gap.** For one result the gap is `p - y`. A right answer said at 0.97 has gap `0.97 - 1 = -0.03`. A wrong answer said at 0.96 has gap `0.96 - 0 = 0.96`.

**(b) Brier score: square each gap, then average.** The cost of one result is `(p - y)²`.

- Right at 0.97 costs `(0.97 - 1)² = 0.0009`.
- Wrong at 0.96 costs `(0.96 - 0)² = 0.9216`.

**Being sure and wrong costs about a thousand times more than being sure and right.** The Brier score is the mean of these costs, over all results. Lower is better. Saying `0.5` on everything costs `0.25` whatever happens, so `0.25` is the score of a system that has no idea.

**(c) ECE (expected calibration error): bucket first, then compare.** Sort the results into **buckets** by `p`. In each bucket write down

- **stated:** the mean `p`,
- **actual:** the share with `y = 1`,
- **gap:** the size of the difference (ignore the sign).

Then average the gaps **with each bucket weighted by how many results it holds**:

```text
ECE = (n_1/N) x gap_1  +  (n_2/N) x gap_2  +  ...
```

A bucket of 10 counts more than a bucket of 6. Two buckets is enough for the pencil: "sure" (`p` at least 0.8) and "unsure" (below 0.8).

---

## 1. The three new pieces of syntax

This section names the three new tools before you use them: two numpy functions and one sklearn function.

**`np.digitize(values, edges)`** says which bucket each value falls in, numbered from **0**. With four edges there are **five** buckets: bucket 0 is "below the first edge", bucket 4 is "at or above the last edge". A value exactly on an edge goes to the **upper** bucket. The edges must be in increasing order.

**`np.bincount(bucket_numbers, minlength=5)`** counts how many times each whole number 0, 1, 2, ... appears. `minlength=5` makes the answer five long even if the top buckets are empty. You can use it a second way, with `weights=`: `np.bincount(bucket, weights=conf, minlength=5)` **adds up** the weights per bucket instead of counting. Counting is adding ones; `weights` lets you add something else. Divide those sums by the counts and you have the mean per bucket.

**`brier_score_loss(y_true, y_prob)`** from `sklearn.metrics` is the Brier score, with the **truth first** and the probabilities second. You compute Brier yourself first; the function is for checking.

Everything else today is old: boolean masks, `.mean()`, `zip`, f-strings with width and precision, `np.full`, `np.arange`, and `matplotlib`.

---

## 2. The sheet: type the 40 results

This section builds the data every later block uses. Type the block below by hand; it is the only long typing of the week. Each row is `(category, how sure it said it was, was it right: 1 or 0)`, eight rows for each of Week 30's five categories.

```python
# p0_results.py - Week 32 block P0: the 40 typed results. A HANDED-OUT SHEET, typed by the student.
# INVENTED FOR THE LESSON: these 40 rows were written by the teacher to have a shape worth measuring.
# They are not the output of any model. They stand in for the log of a support-ticket classifier
# that reports its top label and how sure it is. Nothing measured on them says anything about a real model.
# Each row: (category, how sure it said it was, was it right: 1 or 0). Eight rows per category.
import numpy as np

RESULTS = [
    ("greeting", 0.97, 1), ("greeting", 0.95, 1), ("greeting", 0.92, 1), ("greeting", 0.88, 1),
    ("greeting", 0.91, 1), ("greeting", 0.85, 1), ("greeting", 0.62, 0), ("greeting", 0.55, 1),
    ("refund", 0.93, 1), ("refund", 0.89, 1), ("refund", 0.84, 1), ("refund", 0.78, 1),
    ("refund", 0.72, 0), ("refund", 0.66, 1), ("refund", 0.58, 0), ("refund", 0.52, 0),
    ("technical", 0.81, 1), ("technical", 0.76, 1), ("technical", 0.74, 0), ("technical", 0.68, 1),
    ("technical", 0.63, 0), ("technical", 0.59, 1), ("technical", 0.55, 0), ("technical", 0.51, 0),
    ("billing", 0.96, 0), ("billing", 0.94, 1), ("billing", 0.92, 0), ("billing", 0.90, 0),
    ("billing", 0.87, 1), ("billing", 0.83, 0), ("billing", 0.64, 1), ("billing", 0.57, 1),
    ("out_of_scope", 0.91, 1), ("out_of_scope", 0.86, 0), ("out_of_scope", 0.79, 1), ("out_of_scope", 0.73, 0),
    ("out_of_scope", 0.69, 0), ("out_of_scope", 0.61, 1), ("out_of_scope", 0.56, 0), ("out_of_scope", 0.53, 0),
]

cat = np.array([row[0] for row in RESULTS])
conf = np.array([row[1] for row in RESULTS])
right = np.array([row[2] for row in RESULTS], dtype=float)

print(len(RESULTS), "results")
print({name: int((cat == name).sum()) for name in ["greeting", "refund", "technical", "billing", "out_of_scope"]})
print(f"accuracy {right.mean():.3f}   average stated confidence {conf.mean():.3f}")
```

```text
40 results
{'greeting': 8, 'refund': 8, 'technical': 8, 'billing': 8, 'out_of_scope': 8}
accuracy 0.575   average stated confidence 0.754
```

Read the last line. The system is right 57.5% of the time and claims 75.4% on average. That is a gap before we have built anything. Is accuracy alone enough to tell you that? No, and that is the proxy problem.

---

## 3. Ten results, by hand

This section sets up your pencil work on a small sample. Take every fourth row of the sheet, starting at the first: `RESULTS[0::4]`. That is ten rows.

Run this block to print them so you can copy them onto paper:

```python
# p0b_card.py - Week 32 block P0b: the ten rows for your pencil work (every 4th row, starting at the first).
for i, (name, p, y) in enumerate(RESULTS[0::4]):
    print(f"{i + 1:>2}  {name:<13} said {p:.2f}   right {y}")
```

```text
 1  greeting      said 0.97   right 1
 2  greeting      said 0.91   right 1
 3  refund        said 0.93   right 1
 4  refund        said 0.72   right 0
 5  technical     said 0.81   right 1
 6  technical     said 0.63   right 0
 7  billing       said 0.96   right 0
 8  billing       said 0.87   right 1
 9  out_of_scope  said 0.91   right 1
10  out_of_scope  said 0.69   right 0
```

Now do **pages 32.1 and 32.2 of the workbook** with a pencil, before you read on:

- **Brier:** for each of the ten rows write `(p - y)` and `(p - y)²`. Two decimals is enough. Add the ten squares and divide by ten. Circle the most expensive row and write one sentence about why it costs so much.
- **ECE, two buckets:** split the ten into *sure* (`p` at least 0.8) and *unsure* (below 0.8). For each group write the count, the mean `p` and the share right. Then `ECE = (n_sure/10) x gap_sure + (n_unsure/10) x gap_unsure`.

When you have both numbers on paper, the code in Sections 5 and 6 will compute the same two quantities for all forty. In **Your Turn** you will have it compute them for your ten rows as well, so you can check your arithmetic.

---

## 4. `digitize` and `bincount` on toys

This section tries the two new helpers on numbers small enough to check by eye, before they touch the 40 results.

**Predict the output before you run it.** In particular: which bucket does exactly `0.60` go to?

```python
# p1_digitize.py - Week 32 block P1: the two new helpers on tiny inputs, before they touch the 40 results.
edges = [0.6, 0.7, 0.8, 0.9]            # four edges make five buckets: below 0.6, 0.6-0.7, 0.7-0.8, 0.8-0.9, 0.9 and up
print(np.digitize([0.55, 0.60, 0.65, 0.95, 0.90], edges))     # which bucket each number falls in
print(np.bincount([0, 1, 1, 4, 4, 4], minlength=5))           # how many landed in each bucket
```

```text
[0 1 1 4 4]
[1 2 0 0 3]
```

Read it. `0.55` is below the first edge, so bucket 0. `0.60` sits exactly on an edge and goes to the **upper** bucket, 1. `0.90` likewise goes to bucket 4. In the second line, bucket 0 appeared once, bucket 1 twice, buckets 2 and 3 never, bucket 4 three times. That is why `minlength=5` matters: it keeps the empty buckets in the answer, so the result is always five long.

---

## 5. The reliability table and ECE

This section builds the week's main instrument. The **reliability table** has one row per bucket: how many results landed in it, how sure the system *said* it was (stated), and how often it was *right* (actual).

The picture below shows the order of the work: sort by what the system said, compare what it said with what it delivered inside each bucket, and only then weight and add.

![The 40 results sorted by stated confidence into five buckets of 9, 7, 6, 8 and 10 results, a zoom on the top bucket with a dashed bar for what it said, 0.931, beside a solid bar for what it delivered, 0.700, and three boxes in order: sort, compare, weight and add](../figures/fig-w32-4-sort-compare-weight.svg)
*Figure 32.3 — ECE sorts first, compares second and weights third; here the average gap is 0.1788, which is not the share it gets wrong.*

You write two functions, then print the table. Read the functions line by line and ask of each line, "what is this array right now, and how long is it?"

```python
# p2_reliability.py - Week 32 block P2: the reliability table (stated vs actual, per bucket) and ECE.
def reliability(conf, right, edges):
    bucket = np.digitize(conf, edges)                              # 0..len(edges): one number per result
    n_b = len(edges) + 1
    counts = np.bincount(bucket, minlength=n_b)                    # results per bucket
    safe = np.maximum(counts, 1)                                   # an empty bucket must not divide by zero
    stated = np.bincount(bucket, weights=conf, minlength=n_b) / safe     # mean stated confidence per bucket
    actual = np.bincount(bucket, weights=right, minlength=n_b) / safe    # share actually right per bucket
    return counts, stated, actual


def ece_of(counts, stated, actual):
    return float(np.sum(counts / counts.sum() * np.abs(stated - actual)))     # big buckets count for more


labels = ["0.00-0.59", "0.60-0.69", "0.70-0.79", "0.80-0.89", "0.90-1.00"]
counts, stated, actual = reliability(conf, right, edges)
print(f"{'bucket':<10} {'n':>3} {'stated':>7} {'actual':>7} {'gap':>7}")
for lab, k, s, a in zip(labels, counts, stated, actual):
    print(f"{lab:<10} {k:>3} {s:>7.3f} {a:>7.3f} {a - s:>+7.3f}")
print(f"ECE = {ece_of(counts, stated, actual):.4f}")
```

```text
bucket       n  stated  actual     gap
0.00-0.59    9   0.551   0.333  -0.218
0.60-0.69    7   0.647   0.571  -0.076
0.70-0.79    6   0.753   0.500  -0.253
0.80-0.89    8   0.854   0.750  -0.104
0.90-1.00   10   0.931   0.700  -0.231
ECE = 0.1788
```

Read the table **row by row before you read the ECE.** Which bucket is worst? Which way does every gap point? Every gap is negative: in every bucket the system *said* more than it *delivered*. Say the top row as a sentence: *"When it said about 0.93, it was right 70% of the time."*

Two cautions about the ECE number:

- **ECE 0.18 does not mean "wrong 18% of the time".** It is the average size of the gap between said and delivered. This system is wrong 42.5% of the time.
- **The buckets are a choice.** With fewer than ten results in a bucket, the gaps are noisy. ECE is one way to score calibration, not the only one.

![Five pairs of bars, stated confidence against actual accuracy, one pair per confidence bucket of 40 invented results, with each gap printed and the ECE 0.1788 in a callout](../figures/fig-w32-1-reliability-gaps.svg)
*Figure 32.1 — In every bucket the system said more than it delivered; ECE is the average size of that gap, weighted by bucket.*

---

## 6. Brier, and a baseline to beat

This section scores all forty results with Brier, two ways: your own numpy line, and sklearn's. It then adds two **baselines**: systems that ignore the question and say the same number every time.

```python
# p3_brier.py - Week 32 block P3: the Brier score, by hand-in-numpy and by sklearn, and two baselines to beat.
from sklearn.metrics import brier_score_loss

brier = float(np.mean((conf - right) ** 2))                        # mean of squared gaps
print(f"Brier, numpy:   {brier:.4f}")
print(f"Brier, sklearn: {brier_score_loss(right, conf):.4f}")      # argument order: the truth first, then the probabilities

flat = np.full(len(right), right.mean())                           # a system that says the same thing every time: its accuracy
print(f"Brier of always saying {right.mean():.3f}: {np.mean((flat - right) ** 2):.4f}")
print(f"Brier of always saying 0.5:   {np.mean((0.5 - right) ** 2):.4f}")
```

```text
Brier, numpy:   0.2499
Brier, sklearn: 0.2499
Brier of always saying 0.575: 0.2444
Brier of always saying 0.5:   0.2500
```

Your numpy line and sklearn agree, which is the check. Now the surprise: a system that says `0.575` every single time scores `0.2444`, which is *better* than ours at `0.2499`. On Brier alone, our confidence numbers are worth no more than the overall hit rate. **A score needs a comparison**, as Week 30's `0.833` did.

So is the confidence worthless? Not quite, and the next section shows why. The flat system has a perfect ECE (it says exactly how often it is right) and yet it cannot tell a sure question from an unsure one. Perfect calibration and usefulness are different things.

---

## 7. "I don't know"

This section lets the system decline to answer. Add a threshold: answer only when `conf >= t`. For each `t`, the block prints how many were answered, the coverage, the accuracy of the answered, and how many were wrong but answered anyway.

```python
# p4_abstain.py - Week 32 block P4: abstention. Answer only when conf >= t; otherwise say "I don't know".
print(f"{'t':>5} {'answered':>8} {'coverage':>8} {'accuracy of answered':>21} {'wrong but answered':>19}")
for t in [0.0, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95]:
    answered = conf >= t
    k = int(answered.sum())
    acc = right[answered].mean() if k > 0 else float("nan")
    print(f"{t:>5.2f} {k:>8} {answered.mean():>8.3f} {acc:>21.3f} {int((answered & (right == 0)).sum()):>19}")
```

```text
    t answered coverage  accuracy of answered  wrong but answered
 0.00       40    1.000                 0.575                  17
 0.50       40    1.000                 0.575                  17
 0.60       31    0.775                 0.645                  11
 0.70       24    0.600                 0.667                   8
 0.80       18    0.450                 0.722                   5
 0.85       15    0.375                 0.733                   4
 0.90       10    0.250                 0.700                   3
 0.95        3    0.075                 0.667                   1
```

Read it in results. At `t = 0.8` the system answers 18 of 40 and gets 13 right. The other 22 get "I don't know". Of those 22, ten would have been right. **Abstaining is not free**: it bought fewer wrong answers (17 down to 5) by giving up right ones. Whether that is a good trade depends on what a wrong answer costs and what a human's time costs. The code cannot say.

Notice too that the accuracy column does **not** rise forever: `0.722`, `0.733`, `0.700`, `0.667`. With fewer answers left, a few sure-and-wrong ones weigh more, and the sure-and-wrong ones are the highest-confidence ones.

The threshold `0.8` was chosen because it is round and it shows the effect. We looked at the same 40 results to choose it. A threshold for a *real* system is chosen on one set of results and judged on a **second** set it has not seen, as in Week 30's frozen eval. We have no second set, so treat `0.8` as an illustration.

![A line chart of coverage against accuracy of the answered for 40 invented results, with the threshold 0.8 point ringed and a panel counting answered, right, wrong and abstained](../figures/fig-w32-2-abstain-trade.svg)
*Figure 32.2 — Raising the threshold removes wrong answers by also removing right ones; the curve cannot say where to stop.*

---

## 8. Did every category get better?

This section repeats the abstaining experiment one category at a time.

**Predict first.** At `0.8` overall accuracy rose from `0.575` to `0.722`. Will every category rise? Write your guess, then run the block.

```python
# p5_category.py - Week 32 block P5: the per-category table before and after abstaining at 0.8. Find what fell.
t = 0.8
answered = conf >= t
print(f"threshold {t}: overall accuracy {right.mean():.3f} -> {right[answered].mean():.3f}  "
      f"(answered {int(answered.sum())} of {len(conf)})")
print(f"{'category':<13} {'n':>2} {'before':>7} {'answered':>8} {'after':>7} {'change':>8}")
for name in ["greeting", "refund", "technical", "billing", "out_of_scope"]:
    mine = cat == name
    kept = mine & answered
    before = right[mine].mean()
    after = right[kept].mean() if kept.sum() > 0 else float("nan")
    flag = "   <-- FELL while the average rose" if after < before else ""
    print(f"{name:<13} {int(mine.sum()):>2} {before:>7.3f} {int(kept.sum()):>8} {after:>7.3f} {after - before:>+8.3f}{flag}")
```

```text
threshold 0.8: overall accuracy 0.575 -> 0.722  (answered 18 of 40)
category       n  before answered   after   change
greeting       8   0.875        6   1.000   +0.125
refund         8   0.625        3   1.000   +0.375
technical      8   0.500        1   1.000   +0.500
billing        8   0.500        6   0.333   -0.167   <-- FELL while the average rose
out_of_scope   8   0.375        2   0.500   +0.125
```

Week 31's habit again: the average rose and one row fell. Say billing in results: `4 of 8` right before, `2 of 6` of the answered right after. Look at the billing rows in your sheet. Of its six answers at 0.8 or above (0.96, 0.94, 0.92, 0.90, 0.87, 0.83), only the 0.94 and the 0.87 were right, and its two answers that were *right* at `0.64` and `0.57` were the *unsure* ones, which the threshold threw away. Abstaining discarded its hits and kept its misses.

Also look at the `answered` column. `technical` has **1** answered result, so its `1.000` is one result. Rows built on one, two or three results are not something to read.

And one caution the other way. **Eight rows is a reason to look, not a verdict.** With this few results, billing's fall could be chance. The table tells you where to look; it does not tell you billing is "the weak category".

Here is the same table drawn: before and after for each category, with the number of answers behind each row.

![Five rows of paired bars, a dashed bar for the share right before and a solid bar for the share of the answered that are right after, with the counts printed: billing falls from 4 of 8 to 2 of 6 and is outlined with a cross, and the rows with 3, 1 and 2 answers are marked few](../figures/fig-w32-5-category-before-after.svg)
*Figure 32.4 — The average rose while billing fell, and three of the five rows rest on three or fewer answers.*

---

## 9. The curve

This section plots every threshold at once, so you see the whole trade instead of a few rows: one point per threshold, coverage across, accuracy of the answered up.

```python
# p6_curve.py - Week 32 block P6: the coverage-vs-accuracy curve. One point per threshold.
import matplotlib
matplotlib.use("Agg")                                   # draw to a file, not a window
import matplotlib.pyplot as plt

cov, acc = [], []
for t in np.round(np.arange(0.50, 0.981, 0.01), 2):
    answered = conf >= t
    if answered.sum() >= 1:
        cov.append(answered.mean())
        acc.append(right[answered].mean())

print(f"{len(cov)} points; first (coverage, accuracy) = ({cov[0]:.3f}, {acc[0]:.3f}); last = ({cov[-1]:.3f}, {acc[-1]:.3f})")
fig, ax = plt.subplots()
ax.plot(cov, acc, marker="o")
ax.set_xlabel("coverage (share of questions answered)")
ax.set_ylabel("accuracy of the answered ones")
ax.set_title("Coverage vs accuracy (40 invented results)")
fig.savefig("curve.png")
print("saved curve.png")
```

```text
48 points; first (coverage, accuracy) = (1.000, 0.575); last = (0.025, 1.000)
saved curve.png
```

Open `curve.png`. Put a finger on `t = 0.8`: the point `(0.450, 0.722)`. Now the last point: `(0.025, 1.000)`. That is **one question answered, and it was right**: a perfect score for a system that answers almost nothing. The curve does not tell you where to stop. You decide that in words (how many questions must it answer?) and then read off the threshold.

---

## 🎲 Your Turn

This section is for checking your own arithmetic and trying one repair.

**Check your pencil work.** Run this block on the ten rows you did by hand in Section 3. Your Brier and your two-bucket ECE should agree with it to two or three decimals. If they do not, find which row you added wrongly.

```python
# y1_ten.py - Week 32 block Y1: your Pages 32.1 and 32.2, checked by machine, on the ten rows RESULTS[0::4].
ten = RESULTS[0::4]
p10 = np.array([row[1] for row in ten])
y10 = np.array([row[2] for row in ten], dtype=float)
print("Brier on the ten:", round(float(np.mean((p10 - y10) ** 2)), 4))
c10, s10, a10 = reliability(p10, y10, [0.8])            # one edge makes two buckets: below 0.8 and 0.8 and up
print("counts (unsure, sure):", c10, "  ECE on the ten, two buckets:", round(ece_of(c10, s10, a10), 4))
```

Then answer, in writing:

1. Which single row made the biggest difference to your Brier? Give its cost and its share of your total.
2. Swap cards with a neighbour, or take `RESULTS[1::4]`, `RESULTS[2::4]` and `RESULTS[3::4]` yourself. You now have four sets of ten from the same sheet. Do they give the same ECE? Which one is "the right one"?
3. Change the `edges` to `[0.8]` (two buckets) and then to ten edges of your own choosing, and run the Section 5 table again. Does ECE change? What does that say about the number?
4. A system that says its own accuracy (`0.575`) every time has a perfect ECE. Why is it still no use for deciding which answers to trust?

**Cap what it says.** This repair does not allow "make the model better". Run the block below to cap the stated confidence at 0.85, so the system can no longer claim more than it has earned, and recompute:

```python
# y2_cap.py - Week 32 block Y2: cap what the system may SAY at 0.85. No answer changes; only the stated number.
capped = np.minimum(conf, 0.85)
c2, s2, a2 = reliability(capped, right, edges)
print("accuracy unchanged:", right.mean())
print(f"ECE before {ece_of(counts, stated, actual):.4f}   after capping at 0.85: {ece_of(c2, s2, a2):.4f}")
print(f"Brier before {brier:.4f}   after: {np.mean((capped - right) ** 2):.4f}")
```

Run it and compare. ECE and Brier both improve while **not one answer has changed**. Write one sentence on the difference between "the system stopped overclaiming" and "the system got better". (Accuracy is `0.575` either way.)

---

## 🔬 Break It On Purpose

This section runs one deliberately flawed rule that fails without any error message.

**DELIBERATE, and silent.** A tempting rule: "pick the threshold with the best accuracy". The run does not crash and prints a lovely number. Add this to the end of `week32.py`, predict what it will pick, then run it.

```python
# DELIBERATE BUG D5 (SILENT): "pick the threshold with the best accuracy". The score being chased is not the goal.
best = None
for t in np.round(np.arange(0.50, 0.981, 0.01), 2):
    answered = conf >= t
    if answered.sum() >= 1:
        acc = right[answered].mean()
        if best is None or acc > best[1]:
            best = (round(float(t), 2), float(acc), int(answered.sum()))
print(f"best threshold {best[0]}: accuracy of answered {best[1]:.3f} on {best[2]} of 40 answers")
```

```text
best threshold 0.97: accuracy of answered 1.000 on 1 of 40 answers
```

Nothing failed. The rule found a perfect `1.000`, and it does it by answering **one question in forty**. The proxy (accuracy of the answered) was maximised and the goal (a system you can rely on) was thrown away. That is the title of this week.

The check is to always print the **number answered** next to the accuracy. The repair is not a cleverer maximum. Decide in words first, *"it must answer at least half the questions"* (coverage at least `0.5`), and only then look for a threshold.

> *When a number becomes the target, it stops being a good number.*

---

## 🧭 What was shown, and what was not

This section separates what the week's numbers support from what they do not.

**Shown:**

- Accuracy `0.575` against an average stated confidence of `0.754`: the proxy and the claim come apart.
- A reliability table in which the system said more than it delivered in **every** bucket (ECE `0.1788`).
- Brier `0.2499`, checked against sklearn, and a flat system that beats it (`0.2444`) while being useless for choosing.
- Abstaining at `0.8`: `18` of `40` answered, accuracy of the answered `0.575` to `0.722`, and ten right answers given up.
- A category that fell while the average rose: billing, `4 of 8` to `2 of 6`.
- A fix that changes what the system *says* and not what it *gets right*: capping.

**Not shown:**

- **Any real model.** No model exists in this lesson. The 40 rows are invented.
- **That the system is "overconfident" in general.** That is a property of this sheet, not of classifiers.
- **That billing is a weak category.** It is eight rows.
- **A threshold chosen honestly.** `0.8` was chosen by looking at the same results it is judged on.
- **Error bars.** We said "ten results is noisy" and showed four sets of ten disagreeing. How much a count wobbles is next week's question.
- **Other ways of fixing confidence** after the fact. We capped; we did not build the rest.

---

## 🔑 Wrap Up

Use these questions to check the week against the card you wrote at the start.

1. Turn to your card. When the system said about 0.93, how often was it right?
2. Brier 0.2499 against a flat 0.2444: is our confidence worthless? Say what is true in both directions.
3. At `t = 0.8` accuracy went from `0.575` to `0.722`. What did the system give up to get it, in results?
4. Overall accuracy rose and billing fell. Say in one sentence how both can be true.
5. Why is "pick the threshold with the best accuracy" the wrong rule, and what do you print next to the accuracy to catch it?

Then write this sentence on Page 32.3, with your own numbers in it, and keep the word *invented*:

> **"On these invented 40 results the system was more sure than right in every bucket (ECE 0.179); abstaining below 0.8 lifted accuracy of the answered from 0.575 to 0.722 but answered only 18 of 40; and billing went the other way, 4 of 8 to 2 of 6, which on eight rows is a reason to look, not a verdict."**

**A look ahead.** Next week attacks the system, and its first question is the honest answer to "no error bars": *how much does a count wobble?* Bring one sentence: *"If I ran the same test on a different 40 tickets, how different would my number be?"*

---

## 📤 Homework

Complete workbook pages 32.1 to 32.3 (about 55 minutes: 30 of pen and paper, 25 at the computer). Write your **predictions before you run anything.** Every number you write must come from your own arithmetic or your own run.

1. **Another ten by hand (pages 32.1 and 32.2).** Take every fourth row **starting at the second row** (`RESULTS[1::4]`). Do Brier and the two-bucket ECE with a pencil, then check with code. One sentence on why your ECE is not the same as the first ten's.
2. **Two more thresholds (page 32.3).** Print the per-category table at `t = 0.7` and `t = 0.9`. Report overall before and after, the **number answered**, and every category that fell. Say which rows have two results or fewer and should not be read.
3. **The sentences (page 32.3).** Write the four sentences. Then write **one change** you would make to a system like this where "make the model better" is **not allowed**.

**Optional (fast students).** Build a 20-result log from your own Week 26 assistant (how sure its retrieval was, and whether the answer was right). Report `n` next to every number, and say what you could not conclude.

---

## 📖 Words from this week

The new vocabulary, in the order it appeared.

| Word | Meaning |
|---|---|
| **proxy** | a number you can measure that stands in for the thing you actually want |
| **confidence** | how sure the system says it is, a number from 0 to 1 |
| **calibrated** | when it says about 0.8, about 8 in 10 are right |
| **overconfident** | it says more than it delivers |
| **bucket** | a range of confidence; results are sorted into buckets |
| **reliability table** | per bucket: how many, how sure it said, how often it was right |
| **Brier score** | the mean of `(p - y)²` over all results; lower is better |
| **ECE** | expected calibration error: the size of the said-versus-delivered gap per bucket, averaged with big buckets counting more |
| **abstain** | decline to answer; say "I don't know" |
| **threshold** | the confidence below which the system abstains |
| **coverage** | the share of questions the system answered |
| **accuracy of the answered** | the share of the answered questions that were right |
| **stand-in** | a toy imitating something real; measures nothing about the real one |

---

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Workbook](../workbook/week-32.md)
