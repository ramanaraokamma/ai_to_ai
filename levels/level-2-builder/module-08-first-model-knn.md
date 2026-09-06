# Module 8 — Your First Real Model: k-Nearest Neighbors and the Train/Test Rule

**Level 2 · Module 8 · ~4 hours · Prereqs: Modules 1–7 (Python, functions, numpy arrays and broadcasting, pandas DataFrames, matplotlib charts)**

[⬅ Previous](module-07-visualizing-data.md) · [Level 2 Home](README.md) · [Next ➡](module-09-trees-lines-and-overfitting.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** take a messy real-world question and structure it as a **feature matrix `X`** and a **label vector `y`** with the right shapes.
2. **You will be able to** compute the Euclidean distance between two rows of features by hand, with arithmetic you can show on paper.
3. **You will be able to** run the full `fit` → `predict` → `score` cycle with scikit-learn and report an honest test accuracy.
4. **You will be able to** explain — with a worked numeric example where the answer actually flips — why features must be scaled before a distance-based model.
5. **You will be able to** split data with `train_test_split`, say what `random_state` and `stratify` do, and explain why scoring a model on its own training data is meaningless.

---

## 🪝 The Hook

You move to a new school and sit down in the canteen. You don't know anybody. You want to guess which club the person opposite you is in.

You don't run a statistical analysis. You look at the four people sitting nearest to them. Three of the four are wearing chess-club badges. You guess: chess.

That's it. **That's the entire algorithm you are about to build**, and it is a real machine learning model that real people use in production. It has a name — *k-nearest neighbors* — and once you can write six lines of scikit-learn you can point it at wines, handwriting, cancer scans, or songs.

Here's the part that separates a model that works from a model that only *looks* like it works. Suppose you build it, then test it by asking it to classify the exact same people it learned from. It gets 100%. Of course it does — for each person, the nearest neighbour is *themselves*. A model that has memorised the answer key scores perfectly and knows nothing.

The whole discipline of machine learning hangs on one rule that fixes this. **Hide some of your data before you start, and never let the model see it until the very end.** That rule is worth more than every algorithm in this book.

---

## 🧠 The Concept

### 0. Getting scikit-learn

```bash
pip install scikit-learn
```

The import name is `sklearn`, not `scikit-learn`. Yes, that's annoying.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

print(np.__version__)
```

Everything in this module runs on scikit-learn 1.0 or newer.

---

### 1. The ML mindset: X, y, fit, predict, score

Every supervised machine learning problem in existence, from a spam filter to a self-driving car, gets squeezed into the same two objects.

> **Feature matrix `X`** — a table of numbers. One **row per example**, one **column per measurement**. Shape `(n_samples, n_features)`.
>
> **Label vector `y`** — the answer for each row. One value per row. Shape `(n_samples,)`.

🍕 **Analogy.** `X` is a stack of index cards, one per fruit, each card listing weight and bumpiness. `y` is the answer written on the back of each card: apple or orange. **Learning** is flipping through the stack. **Predicting** is being handed a card with a blank back.

The critical rule: **`X` and `y` line up row by row.** `X[7]` describes the same example that `y[7]` labels. If you sort one and not the other, everything silently breaks and your accuracy quietly collapses.

```
        X  (features)                    y  (labels)
   ┌──────────┬───────────┐            ┌──────────┐
 0 │  150 g   │   2 bumpy │            │  apple   │  ← row 0 of X is labelled by row 0 of y
 1 │  170 g   │   3 bumpy │            │  apple   │
 2 │  140 g   │   1 bumpy │            │  apple   │
 3 │  160 g   │   8 bumpy │            │  orange  │
 4 │  180 g   │   9 bumpy │            │  orange  │
 5 │  155 g   │   7 bumpy │            │  orange  │
   └──────────┴───────────┘            └──────────┘
    shape (6, 2)                        shape (6,)
```

Notice `y` has shape `(6,)` — a **1-D array with 6 elements**, not `(6, 1)`. That trailing comma matters; sklearn expects 1-D labels and will warn you if you hand it a column.

Every sklearn model then speaks exactly three verbs:

| Verb | What it does | Code |
|---|---|---|
| **fit** | Learn from `X` and `y` | `model.fit(X_train, y_train)` |
| **predict** | Guess labels for new rows of `X` | `model.predict(X_new)` |
| **score** | Fraction of predictions that were right | `model.score(X_test, y_test)` |

That's the whole API. Swap `KNeighborsClassifier` for any of the two hundred models in sklearn and those three lines don't change. Learn them once, use them forever.

🔍 **Tiny example.**

```python
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

X = np.array([[150, 2], [170, 3], [140, 1], [160, 8], [180, 9], [155, 7]])
y = np.array(["apple", "apple", "apple", "orange", "orange", "orange"])

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)                         # learn
print(model.predict([[175, 2]]))        # guess -> ['orange']  (we'll see why)
```

Note the **double brackets** in `predict([[175, 2]])`. `predict` always wants a *table* of rows, even when the table has exactly one row. Single brackets give you a 1-D array and an error that reads `Expected 2D array, got 1D array instead`.

---

### 2. k-nearest neighbors and majority vote

> **k-nearest neighbors (kNN)** — to label a new example, find the `k` training examples closest to it and take a vote.

That's genuinely all of it. There is no equation to solve, no weights to learn. **kNN doesn't "train" at all** — `fit` just memorises the training table. All the work happens at predict time, when it measures distances to every stored row.

🍕 **Analogy.** You've just moved to a new city and want to know if a street is safe to walk at night. You don't build a model of urban criminology. You ask the five nearest neighbours and go with the majority.

**What `k` does.** `k` is the size of the committee you ask.

| `k` | Behaviour | Failure mode |
|---|---|---|
| 1 | Copy the single closest example | One weird neighbour ruins the answer. Very jumpy. |
| 5–15 | Small committee, sensible | usually the sweet spot |
| = number of training rows | Everyone votes, so it always predicts the most common class | Ignores the input completely |

🔍 **Tiny example with real numbers.** Six training fruits, sorted by distance from a new fruit:

```
distance   label
  5.10     apple      ← closest
  6.40     orange
 10.44     orange
 15.13     apple
 15.81     orange
 25.18     apple
```

- **k = 1** → nearest is apple → predict **apple**
- **k = 3** → apple, orange, orange → 1 vs 2 → predict **orange**
- **k = 5** → apple, orange, orange, apple, orange → 2 vs 3 → predict **orange**

Same data, three different answers. `k` is not a detail — it *is* the model.

⚠️ **Use an odd `k` for two classes.** With `k = 4` you can get a 2–2 tie, and the tie-break is arbitrary. With three or more classes, ties can still happen; sklearn breaks them by picking the class that comes first in sorted order, which is not a principle, just a rule.

---

### 3. Euclidean distance between feature rows

"Closest" needs a definition. The everyday one works fine.

> **Euclidean distance** — straight-line distance. For two rows with features (x₁, x₂, …) and (z₁, z₂, …):
>
> distance = √[ (x₁ − z₁)² + (x₂ − z₂)² + … ]

🍕 **Analogy.** Walk 3 metres east and 4 metres north. How far are you from where you started? Not 7 — you went diagonally. √(3² + 4²) = √25 = **5**. That's Pythagoras, and it's exactly the formula above with two features.

```
        ↑
      4 │      ● you are here
        │     ╱│
        │  5 ╱ │ 4
        │   ╱  │
      0 │  ●───┘
        └──────────→
        0   3
        √(3² + 4²) = √25 = 5
```

With 13 features instead of 2 the picture stops being drawable, but the arithmetic is identical: subtract, square, add up, square-root. **A row of features is a point in as many dimensions as you have columns.**

🔍 **Tiny worked example.** Row A = (150 g, 2 bumpy). Row B = (175 g, 2 bumpy).

```
differences:  150 − 175 = −25      2 − 2 = 0
squares:      (−25)² = 625         0² = 0
sum:          625 + 0 = 625
square root:  √625 = 25.0
```

Distance = **25.0**.

In numpy, without a single loop (Module 5 skills):

```python
import numpy as np
a = np.array([150.0, 2.0])
b = np.array([175.0, 2.0])
print(np.sqrt(((a - b) ** 2).sum()))     # 25.0
```

And for a whole table at once, using broadcasting:

```python
X = np.array([[150, 2], [170, 3], [140, 1], [160, 8], [180, 9], [155, 7]], dtype=float)
new = np.array([175.0, 2.0])
d = np.sqrt(((X - new) ** 2).sum(axis=1))   # axis=1 -> sum across columns, per row
print(np.round(d, 3))
```

```
[25.     5.099 35.014 16.155  8.602 20.616]
```

Six distances, no loop. `X - new` broadcasts the single row against all six rows; `axis=1` collapses each row to one number.

---

### 4. train_test_split, random_state, and stratify

Here is the most important idea in this entire level.

🍕 **Analogy.** Your teacher gives you 100 practice questions with answers. You study them until you can recite every one. Then the exam is… those exact 100 questions. You score 100%. Did you learn maths, or did you learn the answer sheet? Nobody can tell — including you.

That's what happens when you score a model on the data it learned from.

> **Training set** — the rows the model is allowed to learn from.
> **Test set** — rows you lock in a drawer and only look at once, at the very end, to estimate how the model will do on data it has never seen.

```
   all 178 wines
   ┌────────────────────────────────────────────────┐
   │                                                │
   └────────────────────────────────────────────────┘
                       │  shuffle, then cut at 80%
                       ▼
   ┌───────────────────────────────────┬────────────┐
   │   X_train, y_train  (142 rows)    │  X_test    │
   │   the model sees these            │  y_test    │
   │                                   │  (36 rows) │
   └───────────────────────────────────┴────────────┘
        fit() uses ONLY the left side       LOCKED
                                        until the end
```

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% goes to test; 0.2 and 0.25 are the usual choices
    random_state=42,      # fixes the shuffle so you get the same split every run
    stratify=y,           # keep the class proportions the same in both halves
)
```

**Why `random_state`?** Without it, every run reshuffles and you get a different accuracy. You'd never know whether your "improvement" was a real improvement or a lucky shuffle. Setting it to any fixed integer (42 is traditional, 0 and 1 are equally fine) makes your result **reproducible**: someone else running your file gets your exact number.

> **Reproducible** — running the same code again gives the same answer, so differences you see are caused by your changes and nothing else.

**Why `stratify=y`?** Without it, the shuffle can hand you a lopsided test set. Wine has 59 / 71 / 48 examples of its three classes. Here's what a plain random split with `random_state=0` gives:

| Split | class 0 | class 1 | class 2 |
|---|---|---|---|
| Whole dataset (proportions) | 33% | 40% | 27% |
| Test set, **no** stratify | 14 (39%) | 16 (44%) | **6 (17%)** |
| Test set, **with** stratify | 12 (33%) | 14 (39%) | 10 (28%) |

Without stratify, class 2 gets only 6 test examples. Your estimate of how well the model handles class 2 is now based on six wines. **`stratify=y` costs one keyword and removes a whole category of bad luck.** Use it for every classification problem.

⚠️ **The rule you must never break:** the test set is looked at **once**. If you try 25 values of `k`, look at the test score each time, and pick the best — you have used the test set to make a decision, and it is no longer a clean estimate. (The professional fix is a third *validation* set, or cross-validation. For Level 2, just be honest that a `k` chosen this way is a little optimistic, and say so out loud.)

---

### 5. accuracy_score, feature scaling, and choosing k

**Accuracy.**

> **Accuracy** — the fraction of predictions that were correct: (number right) ÷ (total).

```python
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, model.predict(X_test)))    # e.g. 0.9722
```

`model.score(X_test, y_test)` computes exactly the same thing for classifiers. 0.9722 means 35 of 36 test wines were classified correctly.

⚠️ **Accuracy has a trap.** If 99% of emails are not spam, a model that says "not spam" every single time scores 99%. Always ask: *what would the laziest possible model score?* That number is your **baseline**, and beating it is the actual bar. (Module 9 introduces better metrics for when accuracy misleads.)

**Feature scaling — the big one.**

kNN measures distance. Distance adds up squared differences. **A column measured in big numbers contributes big squared differences and therefore drowns out every other column.** This isn't a subtle statistical concern; it will silently wreck your model.

🍕 **Analogy.** You're comparing two people by height in *millimetres* and age in *years*. Person A is 1700 mm and 12 years. Person B is 1750 mm and 40 years. Distance = √(50² + 28²) = √(2500 + 784) = √3284 = 57.3. The 50 mm height difference (2500) contributes three times more than the 28-year age gap (784). Change height to metres and the answer flips completely. **Your model's opinion should not depend on whether you wrote millimetres or metres.**

Look at the real wine dataset:

| Feature | min | max | std |
|---|---|---|---|
| `hue` | 0.48 | 1.71 | 0.23 |
| `nonflavanoid_phenols` | 0.13 | 0.66 | 0.12 |
| `magnesium` | 70 | 162 | 14.28 |
| **`proline`** | **278** | **1680** | **314.91** |

Two wines can differ by 400 in `proline` and by 0.5 in `hue`. Squared: 160,000 versus 0.25. `proline` is **640,000 times** more influential. The other twelve features may as well not exist.

> **Standardization** — rescale every column so it has mean 0 and standard deviation 1, using `z = (value − mean) ÷ std`. Every column then speaks the same language: "how many standard deviations from typical".

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)                       # learn mean and std FROM TRAINING DATA ONLY
X_train_s = scaler.transform(X_train)
X_test_s = scaler.transform(X_test)       # apply the TRAINING mean/std to test data
```

⚠️ **Fit the scaler on the training set only.** If you compute the mean over all the data including the test rows, information from the test set has leaked into your preprocessing. It's a small leak, but the habit is what protects you when the leak isn't small.

The clean way to make that mistake impossible is a **pipeline**:

> **Pipeline** — a chain of steps glued into a single object, so `fit` runs every step in order on the training data and `predict` applies the same fitted steps to new data.

```python
from sklearn.pipeline import make_pipeline
model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
model.fit(X_train, y_train)               # scaler fit on train only, automatically
print(model.score(X_test, y_test))
```

One line, leak-proof. Use pipelines from now on.

**Choosing k.** Try a range, plot the test accuracy, and pick a `k` in a **flat, high region** rather than at a lonely spike. A lonely spike is usually luck; a plateau is usually real. Prefer a larger `k` within the plateau, because larger `k` is less sensitive to noise. Then say out loud, in writing, that you chose it by looking at the test set.

---

## 🔍 Worked Example

We're going to classify one fruit by hand, twice — once with raw features and once with scaled features — and the answer will **flip**. Then we'll confirm every number with sklearn.

### The setup

Six training fruits:

| # | weight (g) | bumpiness (1–10) | label |
|---|---|---|---|
| 1 | 150 | 2 | apple |
| 2 | 170 | 3 | apple |
| 3 | 140 | 1 | apple |
| 4 | 160 | 8 | orange |
| 5 | 180 | 9 | orange |
| 6 | 155 | 7 | orange |

**New fruit to classify: weight 175 g, bumpiness 2.** A big, very smooth fruit. Use `k = 3`.

Look at the table with your eyes first. All three apples have bumpiness 1–3; all three oranges have bumpiness 7–9. Our fruit has bumpiness **2**. It should obviously be an apple. Hold that thought.

### Round 1 — raw features

Distance from (175, 2) to each training fruit.

**Fruit 1 — (150, 2):**
```
weight diff:  150 − 175 = −25   →  (−25)² = 625
bumpy  diff:    2 −   2 =   0   →     0²  =   0
sum = 625 + 0 = 625
√625 = 25.000
```

**Fruit 2 — (170, 3):**
```
weight diff:  170 − 175 = −5    →  (−5)²  =  25
bumpy  diff:    3 −   2 =  1    →    1²   =   1
sum = 25 + 1 = 26
√26 = 5.099
```

**Fruit 3 — (140, 1):**
```
weight diff:  140 − 175 = −35   →  (−35)² = 1225
bumpy  diff:    1 −   2 =  −1   →   (−1)² =    1
sum = 1225 + 1 = 1226
√1226 = 35.014
```

**Fruit 4 — (160, 8):**
```
weight diff:  160 − 175 = −15   →  (−15)² = 225
bumpy  diff:    8 −   2 =   6   →    6²   =  36
sum = 225 + 36 = 261
√261 = 16.155
```

**Fruit 5 — (180, 9):**
```
weight diff:  180 − 175 =  5    →    5²   = 25
bumpy  diff:    9 −   2 =  7    →    7²   = 49
sum = 25 + 49 = 74
√74 = 8.602
```

**Fruit 6 — (155, 7):**
```
weight diff:  155 − 175 = −20   →  (−20)² = 400
bumpy  diff:    7 −   2 =   5   →    5²   =  25
sum = 400 + 25 = 425
√425 = 20.616
```

**Sorted, nearest first:**

| Rank | Fruit | Distance | Label |
|---|---|---|---|
| 1 | #2 | 5.099 | apple |
| 2 | #5 | 8.602 | **orange** |
| 3 | #4 | 16.155 | **orange** |
| 4 | #1 | 25.000 | apple |
| 5 | #6 | 20.616 | orange |
| 6 | #3 | 35.014 | apple |

*(Note ranks 4 and 5: 20.616 < 25.000, so #6 is actually 4th and #1 is 5th. Only the top 3 matter here.)*

**k = 3 vote:** apple, orange, orange → **2 oranges beat 1 apple → predict ORANGE.**

**That is wrong**, and you can see why in the arithmetic. Look at fruit #5: its bumpiness differs from our fruit by 7 — a huge gap on a 1–10 scale, contributing 49. But its weight differs by only 5, contributing 25. Meanwhile fruit #1 has *identical* bumpiness (contributing 0) but a 25 g weight gap contributing 625. **Weight, measured in grams, is running the whole show. Bumpiness is background noise.**

### Round 2 — standardized features

Rescale both columns so each has mean 0 and standard deviation 1.

**Weight column: 150, 170, 140, 160, 180, 155.**

```
mean = (150 + 170 + 140 + 160 + 180 + 155) ÷ 6 = 955 ÷ 6 = 159.1667

deviations:  150 − 159.1667 = −9.1667      squared:   84.03
             170 − 159.1667 =  10.8333                117.36
             140 − 159.1667 = −19.1667                367.36
             160 − 159.1667 =   0.8333                  0.69
             180 − 159.1667 =  20.8333                434.03
             155 − 159.1667 =  −4.1667                 17.36
                                          sum       = 1020.83
variance = 1020.83 ÷ 6 = 170.139
std      = √170.139 = 13.0437
```

**Bumpiness column: 2, 3, 1, 8, 9, 7.**

```
mean = (2 + 3 + 1 + 8 + 9 + 7) ÷ 6 = 30 ÷ 6 = 5.0

deviations:  −3, −2, −4, 3, 4, 2
squared:      9,  4, 16, 9, 16, 4      sum = 58
variance = 58 ÷ 6 = 9.6667
std      = √9.6667 = 3.1091
```

Now apply z = (value − mean) ÷ std to every cell:

| # | weight z | bumpy z | label |
|---|---|---|---|
| 1 | (150−159.167)/13.0437 = **−0.7028** | (2−5)/3.1091 = **−0.9649** | apple |
| 2 | (170−159.167)/13.0437 = **0.8305** | (3−5)/3.1091 = **−0.6433** | apple |
| 3 | (140−159.167)/13.0437 = **−1.4694** | (1−5)/3.1091 = **−1.2865** | apple |
| 4 | (160−159.167)/13.0437 = **0.0639** | (8−5)/3.1091 = **0.9649** | orange |
| 5 | (180−159.167)/13.0437 = **1.5972** | (9−5)/3.1091 = **1.2865** | orange |
| 6 | (155−159.167)/13.0437 = **−0.3194** | (7−5)/3.1091 = **0.6433** | orange |

**The new fruit (175, 2)** gets the *same* transformation, using the *training* mean and std:

```
weight z = (175 − 159.1667) ÷ 13.0437 = 15.8333 ÷ 13.0437 =  1.2139
bumpy  z = (  2 −   5.0   ) ÷  3.1091 = −3      ÷  3.1091 = −0.9649
```

New fruit in scaled space: **(1.2139, −0.9649)**.

Now the distances again.

**Fruit 1 — (−0.7028, −0.9649):**
```
w diff: −0.7028 − 1.2139 = −1.9167  → 3.6737
b diff: −0.9649 − (−0.9649) = 0     → 0.0000
sum = 3.6737   √3.6737 = 1.9166
```

**Fruit 2 — (0.8305, −0.6433):**
```
w diff: 0.8305 − 1.2139 = −0.3834   → 0.1470
b diff: −0.6433 − (−0.9649) = 0.3216 → 0.1034
sum = 0.2504   √0.2504 = 0.5004
```

**Fruit 3 — (−1.4694, −1.2865):**
```
w diff: −1.4694 − 1.2139 = −2.6833  → 7.2001
b diff: −1.2865 + 0.9649 = −0.3216  → 0.1034
sum = 7.3035   √7.3035 = 2.7025
```

**Fruit 4 — (0.0639, 0.9649):**
```
w diff: 0.0639 − 1.2139 = −1.1500   → 1.3225
b diff: 0.9649 + 0.9649 =  1.9298   → 3.7241
sum = 5.0466   √5.0466 = 2.2465
```

**Fruit 5 — (1.5972, 1.2865):**
```
w diff: 1.5972 − 1.2139 = 0.3833    → 0.1469
b diff: 1.2865 + 0.9649 = 2.2514    → 5.0688
sum = 5.2157   √5.2157 = 2.2838
```

**Fruit 6 — (−0.3194, 0.6433):**
```
w diff: −0.3194 − 1.2139 = −1.5333  → 2.3510
b diff:  0.6433 + 0.9649 =  1.6082  → 2.5863
sum = 4.9373   √4.9373 = 2.2220
```

**Sorted, nearest first:**

| Rank | Fruit | Scaled distance | Label |
|---|---|---|---|
| 1 | #2 | 0.5004 | **apple** |
| 2 | #1 | 1.9166 | **apple** |
| 3 | #6 | 2.2220 | orange |
| 4 | #4 | 2.2465 | orange |
| 5 | #5 | 2.2838 | orange |
| 6 | #3 | 2.7025 | apple |

**k = 3 vote:** apple, apple, orange → **2 apples beat 1 orange → predict APPLE.** ✅

**The answer flipped.** Not because we changed a single measurement, but because we stopped letting the choice of units decide which feature mattered.

### Confirm every number with code

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

X = np.array([[150, 2], [170, 3], [140, 1],
              [160, 8], [180, 9], [155, 7]], dtype=float)
y = np.array(["apple", "apple", "apple", "orange", "orange", "orange"])
new = np.array([[175.0, 2.0]])

# ---- raw ---------------------------------------------------------------
d_raw = np.sqrt(((X - new) ** 2).sum(axis=1))
print("raw distances   :", np.round(d_raw, 3))
print("nearest (1-based):", np.argsort(d_raw) + 1)
print("raw prediction  :", KNeighborsClassifier(3).fit(X, y).predict(new))

# ---- scaled ------------------------------------------------------------
scaler = StandardScaler().fit(X)               # learns mean and std from X
print("means:", scaler.mean_, " stds:", np.round(scaler.scale_, 4))

Xs, news = scaler.transform(X), scaler.transform(new)
print("scaled X:\n", np.round(Xs, 4))
print("scaled new:", np.round(news, 4))

d_scaled = np.sqrt(((Xs - news) ** 2).sum(axis=1))
print("scaled distances:", np.round(d_scaled, 4))
print("nearest (1-based):", np.argsort(d_scaled) + 1)
print("scaled prediction:", KNeighborsClassifier(3).fit(Xs, y).predict(news))
```

Output:

```
raw distances   : [25.     5.099 35.014 16.155  8.602 20.616]
nearest (1-based): [2 5 4 6 1 3]
raw prediction  : ['orange']
means: [159.16666667   5.        ]  stds: [13.0437  3.1091]
scaled X:
 [[-0.7028 -0.9649]
 [ 0.8305 -0.6433]
 [-1.4694 -1.2865]
 [ 0.0639  0.9649]
 [ 1.5972  1.2865]
 [-0.3194  0.6433]]
scaled new: [[ 1.2139 -0.9649]]
scaled distances: [1.9166 0.5004 2.7025 2.2465 2.2838 2.222 ]
nearest (1-based): [2 1 6 4 5 3]
scaled prediction: ['apple']
```

Every single number matches the hand arithmetic. Compare the two `nearest` orderings: `[2 5 4 6 1 3]` versus `[2 1 6 4 5 3]`. Scaling didn't just tweak the numbers — **it completely reordered who counts as a neighbour.**

---

## 💻 Hands-On

Now the real thing: 178 Italian wines, 13 chemical measurements each, three grape varieties to tell apart.

### Step 1 — Look at the data before you model it

```python
# wine_explore.py
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine

wine = load_wine()                 # a "Bunch": dict-like object bundled with sklearn

print("X shape:", wine.data.shape)         # (178, 13)
print("y shape:", wine.target.shape)       # (178,)
print("classes:", wine.target_names)       # ['class_0' 'class_1' 'class_2']
print("counts :", np.bincount(wine.target))  # how many of each class

print("\nfeatures:")
for i, name in enumerate(wine.feature_names):
    print(f"  {i:2d}  {name}")

# Put it in a DataFrame so Module 6/7 skills work on it.
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df["target"] = wine.target
print("\nscale of each feature:")
print(df[wine.feature_names].agg(["min", "max", "mean", "std"]).T.round(2))
```

Output (trimmed):

```
X shape: (178, 13)
y shape: (178,)
classes: ['class_0' 'class_1' 'class_2']
counts : [59 71 48]

features:
   0  alcohol
   1  malic_acid
   ...
  12  proline

scale of each feature:
                                 min      max    mean     std
alcohol                        11.03    14.83   13.00    0.81
malic_acid                      0.74     5.80    2.34    1.12
ash                             1.36     3.23    2.37    0.27
alcalinity_of_ash              10.60    30.00   19.49    3.34
magnesium                      70.00   162.00   99.74   14.28
total_phenols                   0.98     3.88    2.30    0.63
flavanoids                      0.34     5.08    2.03    1.00
nonflavanoid_phenols            0.13     0.66    0.36    0.12
proanthocyanins                 0.41     3.58    1.59    0.57
color_intensity                 1.28    13.00    5.06    2.32
hue                             0.48     1.71    0.96    0.23
od280/od315_of_diluted_wines    1.27     4.00    2.61    0.71
proline                       278.00  1680.00  746.89  314.91
```

**Stop and read that table.** `proline` has a standard deviation of 314.91. `nonflavanoid_phenols` has 0.12. That's a ratio of about **2,600 to 1**. Before you write another line, you already know scaling is going to matter enormously here.

### Step 2 — The dishonest baseline: score on the training data

Let's do the wrong thing on purpose, so you recognise it when you see it in the wild.

```python
# wine_dishonest.py
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier

X, y = load_wine(return_X_y=True)

model = KNeighborsClassifier(n_neighbors=1)
model.fit(X, y)                        # learn from everything
print("accuracy:", model.score(X, y))  # test on everything
```

```
accuracy: 1.0
```

**100%. Perfect. Ship it.**

No. With `k = 1`, the nearest neighbour of every training row is *itself*, at distance 0. The model has memorised the table and we asked it to recite the table. This number is worth exactly nothing, and versions of it appear in real press releases every month.

### Step 3 — Split honestly

```python
# wine_split.py
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

X, y = load_wine(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("train:", X_train.shape, "test:", X_test.shape)
print("train class counts:", np.bincount(y_train))
print("test  class counts:", np.bincount(y_test))
```

```
train: (142, 13) test: (36, 13)
train class counts: [47 57 38]
test  class counts: [12 14 10]
```

142 + 36 = 178. ✅ And the test class proportions (12/14/10) mirror the full dataset (59/71/48) — that's `stratify` doing its job.

### Step 4 — kNN without scaling

```python
# wine_unscaled.py
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
print("train accuracy:", round(knn.score(X_train, y_train), 4))
print("test  accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\nconfusion matrix (rows = truth, cols = prediction):")
print(confusion_matrix(y_test, y_pred))
```

```
train accuracy: 0.7817
test  accuracy: 0.8056

confusion matrix (rows = truth, cols = prediction):
[[12  0  0]
 [ 0 10  4]
 [ 0  3  7]]
```

> **Confusion matrix** — a grid where row *i*, column *j* counts examples whose true class was *i* and whose predicted class was *j*. The diagonal is "got it right"; everything off the diagonal is a specific kind of mistake.

Read it: all 12 class-0 wines were correct. But 4 class-1 wines were called class 2, and 3 class-2 wines were called class 1. **The model cannot tell classes 1 and 2 apart.** That's much more useful than the single number 0.8056 — it tells you *where* to look.

### Step 5 — kNN with scaling, via a pipeline

```python
# wine_scaled.py
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# The pipeline: scale, then classify. fit() does both, in order, on train only.
model = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5),
)
model.fit(X_train, y_train)

print("train accuracy:", round(model.score(X_train, y_train), 4))
print("test  accuracy:", round(model.score(X_test, y_test), 4))
print("\nconfusion matrix:")
print(confusion_matrix(y_test, model.predict(X_test)))
```

```
train accuracy: 0.9789
test  accuracy: 0.9722

confusion matrix:
[[12  0  0]
 [ 0 13  1]
 [ 0  0 10]]
```

**0.8056 → 0.9722.** Test accuracy jumped by 16.7 percentage points. The error count fell from 7 wrong out of 36 to **1 wrong out of 36**. We changed no data, added no features, and tuned nothing. We just stopped letting `proline` shout over the other twelve measurements.

Put the comparison in a table you can show someone:

| Model | Train accuracy | Test accuracy | Test errors (of 36) |
|---|---|---|---|
| kNN k=5, **raw features** | 0.7817 | 0.8056 | 7 |
| kNN k=5, **standardized** | 0.9789 | **0.9722** | **1** |

### Step 6 — Sweep k and plot it

```python
# wine_choose_k.py
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

ks = list(range(1, 26))
scaled_scores = []
raw_scores = []

for k in ks:
    scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(k))
    scaled.fit(X_train, y_train)
    scaled_scores.append(scaled.score(X_test, y_test))

    raw = KNeighborsClassifier(k)
    raw.fit(X_train, y_train)
    raw_scores.append(raw.score(X_test, y_test))

for k, s, r in zip(ks, scaled_scores, raw_scores):
    print(f"k={k:2d}   scaled={s:.4f}   raw={r:.4f}")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ks, scaled_scores, marker="o", linewidth=2,
        color="#1f77b4", label="standardized features")
ax.plot(ks, raw_scores, marker="s", linewidth=2,
        color="#d62728", label="raw features")

ax.set_title("Scaling is worth ~17 accuracy points on the wine dataset")
ax.set_xlabel("k (number of neighbours voting)")
ax.set_ylabel("Test accuracy (fraction of 36 wines correct)")
ax.set_ylim(0, 1.05)                    # honest axis, from zero
ax.set_xticks(ks)
ax.grid(alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig("wine_accuracy_vs_k.png", dpi=150)
plt.show()
```

Output (first and last few lines):

```
k= 1   scaled=0.9722   raw=0.7778
k= 2   scaled=0.9444   raw=0.7500
k= 3   scaled=0.9722   raw=0.7500
k= 4   scaled=0.9444   raw=0.7222
k= 5   scaled=0.9722   raw=0.8056
k= 6   scaled=0.9722   raw=0.7500
k= 7   scaled=1.0000   raw=0.7222
k= 8   scaled=1.0000   raw=0.7500
k= 9   scaled=1.0000   raw=0.8056
k=10   scaled=1.0000   raw=0.8333
...
k=24   scaled=1.0000   raw=0.7500
k=25   scaled=1.0000   raw=0.7500
```

Two things to say out loud about that plot:

1. **The blue line sits above the red line at every single k.** Scaling isn't a tweak; on this dataset it is the difference between a usable model and a broken one.
2. **`scaled = 1.0000` from k = 7 onwards is not "perfect".** It means the model got all 36 test wines right. With only 36 test examples, the finest distinction accuracy can measure is 1/36 = 2.8%. A model scoring 100% on 36 examples and a model scoring 100% on 36,000 examples are not remotely the same claim. **Always report the size of your test set next to your accuracy.**

### Step 7 — What happens when k gets absurd

```python
# wine_big_k.py
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

for k in [1, 5, 142]:                 # 142 = every single training row votes
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(k))
    m.fit(X_train, y_train)
    print(f"k={k:3d}   train={m.score(X_train, y_train):.4f}"
          f"   test={m.score(X_test, y_test):.4f}")
```

```
k=  1   train=1.0000   test=0.9722
k=  5   train=0.9789   test=0.9722
k=142   train=0.4014   test=0.3889
```

Three completely different personalities:

- **k = 1** memorises. Train accuracy is *always* exactly 1.0, because every point is its own nearest neighbour. The train score is meaningless; only the test score tells you anything.
- **k = 5** learns. Train and test are close together, and both are high. That's what health looks like.
- **k = 142** gives up. Every training row votes on every prediction, so the answer is always the most common class (class 1, 57 of 142 = 0.4014). The model ignores its input entirely.

Module 9 gives these two failure directions their proper names.

---

## ✍️ Practice

### 1. [Warm-up] Build X and y with the right shapes

Using `students.py` from Module 7 (the cleaned 38-row table), build a feature matrix from `age`, `hours` and `score`, and a label vector from `club`. Print both shapes, the first three rows of `X`, and the first three labels. Then print the number of examples of each club using `np.unique(y, return_counts=True)`.

Finally, write a one-sentence answer: why is `name` a bad feature?

**Done looks like:** `X.shape` is `(38, 3)`, `y.shape` is `(38,)`, the counts are art 12, chess 14, music 12, and your sentence says that a name is unique to one row so a model can only memorise it — it carries no information that transfers to a new student.

### 2. [Warm-up] Distance by hand, then by numpy

Two wines, using just three features (`alcohol`, `hue`, `proline`):

```
Wine A: alcohol 13.20, hue 1.05, proline  1050
Wine B: alcohol 12.80, hue 0.85, proline   630
```

Compute the Euclidean distance by hand, showing every squared term. Then compute it in numpy. Then standardize both wines using mean `[13.00, 0.96, 746.89]` and std `[0.81, 0.23, 314.91]` and compute the distance again. Explain in two sentences which feature dominated before and after.

**Done looks like:** raw distance ≈ 420.0002, scaled distance ≈ 1.6670, and your explanation notes that `proline` contributed 176,400 of the 176,400.2 raw squared total (99.9999%) but only about 1.78 of the 2.78 scaled total (64%).

### 3. [Build] The full cycle on iris

Load `load_iris`, split 80/20 with `random_state=42` and `stratify=y`, and train a `KNeighborsClassifier` with `k=5`, once with raw features and once inside a `StandardScaler` pipeline. Print both test accuracies and the confusion matrix of the better one. Then print `iris.target_names` and translate one off-diagonal cell of the matrix into a plain English sentence.

**Done looks like:** the raw model scores 1.0000 and the scaled one scores 0.9333 — **scaling made it worse**, and your write-up explains why (all four iris features are already in centimetres on similar ranges, so there was no imbalance to fix, and standardizing threw away the genuinely useful fact that petal measurements vary more than sepal ones).

### 4. [Build] Find the flip yourself

Here is a tiny dataset predicting whether a second-hand phone is `"good"` or `"risky"`:

```python
import numpy as np
X = np.array([
    [ 6000,  5],   # price in rupees, battery health score 1-10
    [ 9000,  7],
    [12000,  9],
    [ 5000,  2],
    [ 8000,  3],
    [11000,  4],
], dtype=float)
y = np.array(["risky", "good", "good", "risky", "risky", "risky"])
```

Write a loop that tries every price in `range(5000, 12001, 500)` paired with battery health `8`, and finds the first query point where the raw-feature kNN (k=3) and the scaled kNN (k=3) **disagree**. Print the point, both predictions, and both sorted distance lists.

**Done looks like:** the first disagreement is at price 7000 with battery 8 — raw predicts `risky`, scaled predicts `good` — and you can point at the two distance lists and name the training rows that swapped rank.

### 5. [Stretch] Does `random_state` change the story?

On the wine dataset with a `StandardScaler` + `KNeighborsClassifier(5)` pipeline, loop over `random_state` values 0 through 19 (keeping `test_size=0.2, stratify=y`), collect the 20 test accuracies, and print the minimum, maximum, mean, and standard deviation. Draw a histogram of the 20 accuracies with a labelled title.

Then write three sentences on what this means for someone who reports a single number like "97.2% accuracy".

**Done looks like:** you observe a spread of several percentage points across splits (0.9167 to 1.0000, mean 0.9653, std 0.0213), you notice the mean is *below* the `random_state=42` number you reported earlier, and your paragraph says that a single split's accuracy has real uncertainty attached and should be reported with the test-set size and ideally the spread across splits.

### 6. [Stretch] The leakage habit

Two versions of the same wine experiment:

- **Version A (leaky):** run `StandardScaler().fit_transform(X)` on the *whole* dataset, then split, then fit `KNeighborsClassifier(5)`.
- **Version B (clean):** split first, then use a `make_pipeline(StandardScaler(), KNeighborsClassifier(5))`.

Report both test accuracies. Then print `scaler_all.mean_ - scaler_train.mean_` and `scaler_all.scale_ / scaler_train.scale_` to show, numerically, that the two scalers learned different parameters.

Write a paragraph answering: if the accuracies come out the same, was the leak harmless?

**Done looks like:** both accuracies are 0.9722 on this split, the `proline` mean differs by about 7.41 and some scale ratios differ by up to 5%, and your paragraph argues that identical accuracy here is *luck*, not proof of safety — the leak means the reported score is no longer a clean estimate of unseen-data performance, and you cannot tell in advance whether a given leak will matter.

---

## 🤔 Think Deeper

### 1. kNN keeps every training example forever. What does that mean for privacy?

*How to reason about it:* a decision tree throws the data away and keeps only rules; kNN keeps the actual rows. Imagine your model was trained on medical records and you ship the trained model to a hospital. What exactly did you ship? Now think about a person who could query the model repeatedly with carefully chosen inputs — could they work backwards to reconstruct individual training rows? Consider what "the model has memorised a real person" means for a right to be forgotten, and whether deleting somebody from your database is enough if their row is baked into a model you already released.

### 2. You chose `k` by looking at the test accuracy for 25 different values. Is your reported accuracy still honest?

*How to reason about it:* count how many decisions the test set influenced. If you tried 25 values and reported the best, then the test set helped you *choose*, which is a kind of learning. Think about a student who takes 25 practice exams, picks the one they scored highest on, and reports that score as their ability. Then consider the standard fix — a third split, or cross-validation — and ask what it costs: with 178 wines, carving out a validation set leaves even less to train on. Where's the honest line for a small dataset, and what sentence should appear next to your number?

### 3. The wine model can't tell class 1 from class 2. Whose problem is that?

*How to reason about it:* the confusion matrix showed all the errors concentrated in two classes. Suppose this were a medical test instead of wine, where class 0 is "healthy", class 1 is "mild condition" and class 2 is "serious condition". A model with 97% overall accuracy that makes *every one of its mistakes* on the serious cases is far more dangerous than one with 90% accuracy spread evenly. Think about how you'd change what you report so this is impossible to hide, and then ask who decides which errors are acceptable — the person who builds the model, or the person the error lands on.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead` | You called `predict([175, 2])` with single brackets | `predict([[175, 2]])` — always a table of rows |
| Accuracy is 1.0 and you're delighted | You scored the model on its training data | Score on `X_test, y_test`, which the model never saw |
| Accuracy changes every time you run the file | No `random_state` in `train_test_split` | Pass `random_state=42` (or any fixed integer) |
| A distance model gives nonsense predictions | One feature is in the thousands and drowns the rest | `make_pipeline(StandardScaler(), YourModel())` |
| `X` and `y` have mismatched lengths | You filtered one and not the other | Filter the DataFrame, *then* pull out `X` and `y` |
| You scaled with `fit_transform(X)` before splitting | It felt tidier to preprocess everything at once | Split first; use a pipeline so the scaler only ever sees train |
| Test set has almost none of one class | Plain random split on imbalanced classes | `stratify=y` |
| `k` is even and predictions look arbitrary | Ties in the vote | Use an odd `k` for two classes |
| kNN is unbearably slow on a big dataset | `fit` is instant but `predict` measures distance to every stored row | Reduce features, subsample, or switch to a tree-based model |
| You report 100% accuracy without the test size | The number sounds better alone | Report "36/36 test examples" next to it, always |
| `y` has shape `(n, 1)` and sklearn warns | You sliced a DataFrame with double brackets | Use `df["club"].values` (single brackets) for the label |
| Model predicts one class for everything | `k` is too large, or the classes are very imbalanced | Shrink `k`; check `np.bincount(y_train)` |

---

## 🛠️ Mini-Project — Classifier Lab

### Goal

Run a complete, honest classification experiment on a built-in sklearn dataset: split it, train kNN with and without scaling, sweep `k` from 1 to 25, plot the result, and choose a `k` with a written reason.

### Choose your dataset

Any of these ship with sklearn — no downloads, no files:

| Dataset | Rows | Features | Classes | Note |
|---|---|---|---|---|
| `load_wine()` | 178 | 13 | 3 | wildly different feature scales — scaling matters hugely |
| `load_breast_cancer()` | 569 | 30 | 2 | bigger, medical, and a great ethics discussion |
| `load_digits()` | 1797 | 64 | 10 | handwritten digits as 8×8 pixel grids; you can `imshow` them |
| `load_iris()` | 150 | 4 | 3 | small and tidy; scaling barely helps |

Pick one that is **not** wine, so the numbers are yours.

### Starter steps

**Step 1 — Describe the data before touching a model (20 min).**

```python
from sklearn.datasets import load_breast_cancer
import numpy as np
import pandas as pd

data = load_breast_cancer()
X, y = data.data, data.target

print("shape        :", X.shape)
print("classes      :", data.target_names)
print("class counts :", np.bincount(y))
print("baseline (always predict the biggest class):",
      np.bincount(y).max() / len(y))

df = pd.DataFrame(X, columns=data.feature_names)
print(df.agg(["min", "max", "std"]).T.round(3))
```

Write down the **baseline** number. Any accuracy you report later must be compared to it, or it means nothing.

**Step 2 — Split, once, and never touch the test set again until Step 5 (10 min).**

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape, np.bincount(y_test))
```

**Step 3 — Two models, one table (30 min).** Train `KNeighborsClassifier(5)` raw and inside a `StandardScaler` pipeline. Build a comparison table with these exact columns:

| Model | Train acc | Test acc | Test errors | Errors / test size |
|---|---|---|---|---|
| kNN k=5 raw | | | | |
| kNN k=5 scaled | | | | |

**Step 4 — The accuracy-vs-k plot (40 min).** Loop `k` from 1 to 25 for both the raw and the scaled model. Plot two lines on one figure. Every Module 7 rule applies: title stating the finding, both axis labels with units, `set_ylim(0, 1.05)`, legend, `savefig`.

**Step 5 — Choose a k and defend it in writing (20 min).** Three to five sentences that must include:

- the `k` you chose and its test accuracy
- the size of the test set
- why you preferred a plateau over a spike
- the sentence "I chose this k by looking at test scores, which makes this estimate slightly optimistic."

### Success criteria checklist

- [ ] A saved accuracy-vs-k PNG with two labelled lines and a y-axis from 0
- [ ] A scaled-vs-unscaled comparison table with train *and* test accuracy
- [ ] The baseline accuracy stated, and your model compared to it
- [ ] The test-set size stated next to every accuracy number
- [ ] A confusion matrix printed for your best model
- [ ] A stated chosen `k` with a written reason of at least three sentences
- [ ] The honesty sentence about having peeked at the test set
- [ ] Everything reproducible: `random_state` set, file runs top to bottom without errors

### Level it up

**Add a third line: training accuracy.** Plot train and test accuracy against `k` on the same axes. At `k = 1` the train line will be pinned at exactly 1.0 while the test line sits lower — the gap between those two lines has a name, and Module 9 is entirely about it. Predict, before you plot it, what happens to the gap as `k` grows. Then check whether you were right.

---

## 🔑 Key Takeaways

- **Every supervised problem is `X` and `y`**: one row per example, one column per feature, labels lined up row for row. Three verbs — `fit`, `predict`, `score` — work for every model in sklearn.
- **kNN doesn't learn a rule; it remembers examples** and takes a vote among the `k` closest ones. `k = 1` copies; `k = n` ignores the input; the sweet spot is in between.
- **Distance is Pythagoras in as many dimensions as you have columns.** Subtract, square, add, square-root.
- **Scaling is not optional for distance models.** In this module it changed a hand-worked prediction from *orange* to *apple* and moved wine test accuracy from 0.8056 to 0.9722.
- **A score on training data is not a score.** Split before you model, use `random_state` so it's reproducible and `stratify=y` so it's balanced, and open the test set once.
- **Always report the test-set size with the accuracy.** "100%" on 36 examples and "100%" on 36,000 are different claims wearing the same clothes.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **feature** | One measurement you make about each example | A wine's `proline` value |
| **feature matrix (`X`)** | The table of features: one row per example | Shape `(178, 13)` for wine |
| **label vector (`y`)** | The right answer for each row | Shape `(178,)`, values 0/1/2 |
| **classification** | Predicting which *category* something belongs to | Apple or orange; wine class 0, 1 or 2 |
| **fit** | Show the model the training data so it can learn | `model.fit(X_train, y_train)` |
| **predict** | Ask the model to guess labels for new rows | `model.predict([[175, 2]])` |
| **k-nearest neighbors** | Guess by asking the `k` closest examples to vote | 3 neighbours: apple, apple, orange → apple |
| **Euclidean distance** | Straight-line distance; Pythagoras in many dimensions | √(3² + 4²) = 5 |
| **training set** | The rows the model is allowed to learn from | 142 of the 178 wines |
| **test set** | Rows locked away, used once, to check honestly | The other 36 wines |
| **`random_state`** | A fixed number that makes the random shuffle repeatable | `random_state=42` |
| **stratify** | Keep each class's share the same in train and test | 12/14/10 instead of 14/16/6 |
| **accuracy** | Fraction of predictions that were right | 35 ÷ 36 = 0.9722 |
| **baseline** | What the laziest possible model would score | Always guess the biggest class |
| **confusion matrix** | A grid showing exactly which classes got mixed up | 4 class-1 wines called class 2 |
| **standardization** | Rescale a column to mean 0, std 1 | z = (value − mean) ÷ std |
| **pipeline** | Preprocessing + model glued into one object | `make_pipeline(StandardScaler(), KNeighborsClassifier(5))` |
| **leakage** | Test-set information sneaking into training | Fitting the scaler on all the data before splitting |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Build X and y with the right shapes

```python
import numpy as np
from students import build_students          # from Module 7

df = build_students()

# Features: three numeric columns. Double brackets give a DataFrame,
# .values turns it into a numpy array of shape (n_rows, n_cols).
X = df[["age", "hours", "score"]].values

# Label: ONE column. Single brackets give a Series -> shape (n_rows,).
y = df["club"].values

print("X.shape:", X.shape)          # (38, 3)
print("y.shape:", y.shape)          # (38,)
print("first three rows of X:\n", X[:3])
print("first three labels   :", y[:3])

labels, counts = np.unique(y, return_counts=True)
print("class counts:", dict(zip(labels, counts)))
```

Output:

```
X.shape: (38, 3)
y.shape: (38,)
first three rows of X:
 [[13.   3.5 72. ]
 [14.   5.  90. ]
 [13.   2.  55. ]]
first three labels   : ['chess' 'music' 'chess']
class counts: {'art': 12, 'chess': 14, 'music': 12}
```

**Why `name` is a bad feature:** every name appears in exactly one row, so it is a perfect ID rather than a measurement — a model can only memorise "Aarav Shah → chess", which tells it nothing at all about a new student called Priya Rao. Features must describe *properties that other examples can share*.

(Also worth noticing: `X` came out as `float64` even though `age` and `score` are integers, because numpy needs one dtype for the whole array and `hours` contains 3.5. That's fine — sklearn wants floats anyway.)

---

### 2. [Warm-up] Distance by hand, then by numpy

**Raw distance, by hand.**

```
alcohol:  13.20 − 12.80 =      0.40   →  0.40²   =        0.16
hue    :   1.05 −  0.85 =      0.20   →  0.20²   =        0.04
proline: 1050   − 630   =    420      →  420²    =  176400
                                  sum =            176400.20
                            √176400.20 =            420.0002
```

Distance = **420.0002**.

**In numpy.**

```python
import numpy as np

A = np.array([13.20, 1.05, 1050.0])
B = np.array([12.80, 0.85,  630.0])

sq = (A - B) ** 2
print("squared terms:", sq)                 # [1.60e-01 4.00e-02 1.764e+05]
print("raw distance :", np.sqrt(sq.sum()))  # 420.00023809...
```

**Standardized.**

```python
mean = np.array([13.00, 0.96, 746.89])
std  = np.array([ 0.81, 0.23, 314.91])

As = (A - mean) / std
Bs = (B - mean) / std
print("A scaled:", np.round(As, 4))    # [ 0.2469  0.3913  0.9625]
print("B scaled:", np.round(Bs, 4))    # [-0.2469 -0.4783 -0.3712]

sq_s = (As - Bs) ** 2
print("squared terms:", np.round(sq_s, 4))       # [0.2439 0.7561 1.7788]
print("sum:", round(sq_s.sum(), 4))              # 2.7788
print("scaled distance:", np.sqrt(sq_s.sum()))   # 1.6669742103799619
```

Working the scaled squares by hand to check — note that the *difference* of two z-scores is just the raw difference divided by the std, so you can skip standardizing each wine separately:
- alcohol: 0.40 ÷ 0.81 = 0.4938 → 0.4938² = **0.2439**
- hue: 0.20 ÷ 0.23 = 0.8696 → 0.8696² = **0.7561**
- proline: 420 ÷ 314.91 = 1.3337 → 1.3337² = **1.7788**
- sum = **2.7788**, √2.7788 = **1.6670** — exactly what the code printed. ✅

**The two sentences:** Before scaling, `proline` contributed 176,400 out of a total 176,400.20 — that's **99.9999%** of the distance, so the model was effectively using one feature and ignoring the other two entirely. After scaling, `proline` contributes 1.7788 out of 2.7788 (**64%**), `hue` 0.7561 (**27%**), and `alcohol` 0.2439 (**9%**) — still not equal, but now every feature has a real say, and the share reflects how *unusual* each difference is rather than which unit someone happened to write it in.

---

### 3. [Build] The full cycle on iris

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("train/test:", X_train.shape, X_test.shape)
print("test class counts:", np.bincount(y_test))

raw = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
scaled = make_pipeline(StandardScaler(),
                       KNeighborsClassifier(n_neighbors=5)).fit(X_train, y_train)

print("raw    test accuracy:", round(raw.score(X_test, y_test), 4))
print("scaled test accuracy:", round(scaled.score(X_test, y_test), 4))

print("\ntarget names:", iris.target_names)
print("confusion matrix for the BETTER model (raw):")
print(confusion_matrix(y_test, raw.predict(X_test)))
print("\nconfusion matrix for the scaled model:")
print(confusion_matrix(y_test, scaled.predict(X_test)))
```

Output:

```
train/test: (120, 4) (30, 4)
test class counts: [10 10 10]
raw    test accuracy: 1.0
scaled test accuracy: 0.9333

target names: ['setosa' 'versicolor' 'virginica']
confusion matrix for the BETTER model (raw):
[[10  0  0]
 [ 0 10  0]
 [ 0  0 10]]

confusion matrix for the scaled model:
[[10  0  0]
 [ 0 10  0]
 [ 0  2  8]]
```

**Reading an off-diagonal cell:** in the scaled model's matrix, row 2 (`virginica`), column 1 (`versicolor`) holds the value **2**. In plain English: *"Two flowers that were really virginica were predicted to be versicolor."*

**The surprise, explained.** Scaling made iris **worse** (1.0000 → 0.9333). This is not a bug and it is worth sitting with:

- All four iris features are measured in **centimetres**, and their ranges are already comparable (sepal length 4.3–7.9, petal width 0.1–2.5). There was no unit imbalance to fix.
- Standardization forces every column to std = 1. But in the raw data, petal length and petal width naturally vary *more* than the sepal measurements — and that extra variation is genuinely informative, because petals are what separate the species. Standardizing deliberately erased a real signal.
- On wine, where `proline` outweighed `hue` by 2,600× purely because of units, scaling fixed a catastrophe. On iris there was no catastrophe.

**The rule that survives both cases:** scale when your features live on wildly different scales or in different units. Don't scale reflexively — check, and report both numbers when it's close.

Also note: 30 test flowers means each single flower is worth 3.3 percentage points. The gap between 1.0000 and 0.9333 is **two flowers**. Don't build a philosophy on two flowers.

---

### 4. [Build] Find the flip yourself

```python
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

X = np.array([
    [ 6000,  5],
    [ 9000,  7],
    [12000,  9],
    [ 5000,  2],
    [ 8000,  3],
    [11000,  4],
], dtype=float)
y = np.array(["risky", "good", "good", "risky", "risky", "risky"])

scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

raw_model = KNeighborsClassifier(n_neighbors=3).fit(X, y)
scaled_model = KNeighborsClassifier(n_neighbors=3).fit(Xs, y)

found = False
for price in range(5000, 12001, 500):
    q = np.array([[float(price), 8.0]])     # query: this price, battery health 8
    qs = scaler.transform(q)                # same transform the scaled model saw

    p_raw = raw_model.predict(q)[0]
    p_scaled = scaled_model.predict(qs)[0]

    if p_raw != p_scaled and not found:
        found = True
        d_raw = np.sqrt(((X - q) ** 2).sum(axis=1))
        d_scaled = np.sqrt(((Xs - qs) ** 2).sum(axis=1))
        print(f"FIRST DISAGREEMENT at price={price}, battery=8")
        print(f"  raw prediction    : {p_raw}")
        print(f"  scaled prediction : {p_scaled}")
        print(f"  raw distances     : {np.round(d_raw, 3)}")
        print(f"  raw rank (0-based): {np.argsort(d_raw)}")
        print(f"  scaled distances  : {np.round(d_scaled, 3)}")
        print(f"  scaled rank       : {np.argsort(d_scaled)}")
        print()

    flag = "<-- DISAGREE" if p_raw != p_scaled else ""
    print(f"price={price:6d}  raw={p_raw:6s}  scaled={p_scaled:6s} {flag}")
```

Output:

```
FIRST DISAGREEMENT at price=7000, battery=8
  raw prediction    : risky
  scaled prediction : good
  raw distances     : [1000.004 2000.    5000.    2000.009 1000.012 4000.002]
  raw rank (0-based): [0 4 1 3 5 2]
  scaled distances  : [1.322 0.904 2.044 2.644 2.138 2.32 ]
  scaled rank       : [1 0 2 4 5 3]

price=  5000  raw=risky   scaled=risky  
price=  5500  raw=risky   scaled=risky  
price=  6000  raw=risky   scaled=risky  
price=  6500  raw=risky   scaled=risky  
price=  7000  raw=risky   scaled=good   <-- DISAGREE
price=  7500  raw=risky   scaled=good   <-- DISAGREE
price=  8000  raw=risky   scaled=good   <-- DISAGREE
price=  8500  raw=risky   scaled=good   <-- DISAGREE
price=  9000  raw=risky   scaled=good   <-- DISAGREE
price=  9500  raw=risky   scaled=good   <-- DISAGREE
price= 10000  raw=good    scaled=good   
price= 10500  raw=good    scaled=good   
price= 11000  raw=good    scaled=good   
price= 11500  raw=good    scaled=good   
price= 12000  raw=good    scaled=good   
```

**Reading the flip at price = 7000, battery = 8.**

The raw top three are ranks `[0, 4, 1]`:

| Rank | Row | Phone | Raw distance | Label |
|---|---|---|---|---|
| 1 | 0 | (6000, 5) | 1000.004 | risky |
| 2 | 4 | (8000, 3) | 1000.012 | **risky** |
| 3 | 1 | (9000, 7) | 2000.000 | good |

Vote: 2 risky, 1 good → **risky**.

The scaled top three are ranks `[1, 0, 2]`:

| Rank | Row | Phone | Scaled distance | Label |
|---|---|---|---|---|
| 1 | 1 | (9000, 7) | 0.904 | **good** |
| 2 | 0 | (6000, 5) | 1.322 | risky |
| 3 | 2 | (12000, 9) | 2.044 | **good** |

Vote: 2 good, 1 risky → **good**.

**Which rows swapped rank, and why.**

- **Row 4, phone (8000, 3):** raw rank **2**, scaled rank **4**. Its price is only ₹1,000 from the query, contributing 1,000,000 to the raw squared sum, while its battery health of 3 versus our 8 — a gap of 5 points on a 1–10 scale, which is the difference between a healthy phone and a dying one — contributes a laughable 25. Raw kNN essentially cannot see the battery column at all.
- **Row 2, phone (12000, 9):** raw rank **6, dead last**, scaled rank **3**. It's ₹5,000 away in price, which annihilates it in raw space, but its battery health of 9 is the closest match in the whole table to our query's 8.

Once both columns are standardized, "₹1,000 of price" and "1 point of battery health" are compared as *how unusual each gap is* rather than *how big the number looks*, and the two rows trade places.

**The transferable lesson:** the raw model decided a phone's fate almost entirely on price and treated battery health 3 and battery health 8 as nearly the same thing. On a real second-hand marketplace that model would happily recommend dying phones because they happened to be priced right — and the bug would be invisible in the accuracy number, because it is a bug in what the model is *paying attention to*, not in how often it is right on this particular tiny table.

---

### 5. [Stretch] Does `random_state` change the story?

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_wine(return_X_y=True)

scores = []
for rs in range(20):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=rs, stratify=y
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(5))
    model.fit(X_train, y_train)
    s = model.score(X_test, y_test)
    scores.append(s)
    print(f"random_state={rs:2d}  test accuracy = {s:.4f}")

scores = np.array(scores)
print(f"\nmin  = {scores.min():.4f}")
print(f"max  = {scores.max():.4f}")
print(f"mean = {scores.mean():.4f}")
print(f"std  = {scores.std():.4f}")
print(f"range = {scores.max() - scores.min():.4f}")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(scores, bins=np.arange(0.90, 1.02, 0.01),
        color="#4c72b0", edgecolor="white")
ax.axvline(scores.mean(), color="#d62728", linestyle="--", linewidth=2,
           label=f"mean = {scores.mean():.4f}")
ax.set_title("The 'same' model scores differently on 20 different splits")
ax.set_xlabel("Test accuracy (36 wines per test set)")
ax.set_ylabel("Number of splits (out of 20)")
ax.legend()
fig.tight_layout()
fig.savefig("random_state_spread.png", dpi=150)
plt.show()
```

Output:

```
random_state= 0  test accuracy = 0.9444
random_state= 1  test accuracy = 0.9722
random_state= 2  test accuracy = 0.9722
random_state= 3  test accuracy = 0.9722
random_state= 4  test accuracy = 0.9722
random_state= 5  test accuracy = 0.9722
random_state= 6  test accuracy = 0.9167
random_state= 7  test accuracy = 1.0000
random_state= 8  test accuracy = 0.9722
random_state= 9  test accuracy = 1.0000
random_state=10  test accuracy = 0.9444
random_state=11  test accuracy = 0.9444
random_state=12  test accuracy = 0.9722
random_state=13  test accuracy = 0.9722
random_state=14  test accuracy = 0.9444
random_state=15  test accuracy = 1.0000
random_state=16  test accuracy = 0.9722
random_state=17  test accuracy = 0.9722
random_state=18  test accuracy = 0.9444
random_state=19  test accuracy = 0.9444

min  = 0.9167
max  = 1.0000
mean = 0.9653
std  = 0.0213
range = 0.0833
```

Worth noticing: the `random_state=42` value we reported all through the Hands-On (0.9722) is *above* the 20-split mean of 0.9653. Not dishonestly so — but it is on the lucky side, and we had no way of knowing that from one split.

**The three sentences:** Across 20 different but equally valid splits of the same data with the same model, test accuracy ranged from 0.9167 to 1.0000 — a spread of 8.3 percentage points, which is three whole wines out of 36. A person who reports "97.2% accuracy" from a single `random_state` is reporting one draw from that distribution and may well have drawn a lucky one; the honest version is "96.5% ± 2.1% across 20 splits, 36 wines in each test set." The smaller your test set, the wider this spread gets — with 36 test examples the finest difference measurable is 2.8 percentage points, so any two models within 3 points of each other are, on this evidence, indistinguishable.

---

### 6. [Stretch] The leakage habit

```python
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_wine(return_X_y=True)

# ---- Version A: LEAKY -------------------------------------------------
# The scaler sees every row, including the ones we're about to call "unseen".
scaler_all = StandardScaler().fit(X)
X_all_scaled = scaler_all.transform(X)
Xa_tr, Xa_te, ya_tr, ya_te = train_test_split(
    X_all_scaled, y, test_size=0.2, random_state=42, stratify=y
)
leaky = KNeighborsClassifier(5).fit(Xa_tr, ya_tr)
print("Version A (leaky) test accuracy:", round(leaky.score(Xa_te, ya_te), 4))

# ---- Version B: CLEAN -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
clean = make_pipeline(StandardScaler(), KNeighborsClassifier(5))
clean.fit(X_train, y_train)
print("Version B (clean) test accuracy:", round(clean.score(X_test, y_test), 4))

# ---- Show the two scalers learned different things --------------------
scaler_train = StandardScaler().fit(X_train)
names = load_wine().feature_names

print("\nfeature                        mean difference   scale ratio")
for n, md, sr in zip(names,
                     scaler_all.mean_ - scaler_train.mean_,
                     scaler_all.scale_ / scaler_train.scale_):
    print(f"{n:30s} {md:14.4f}   {sr:11.4f}")
```

Output:

```
Version A (leaky) test accuracy: 0.9722
Version B (clean) test accuracy: 0.9722

feature                        mean difference   scale ratio
alcohol                                0.0290        1.0123
malic_acid                            -0.0040        1.0151
ash                                    0.0020        1.0230
alcalinity_of_ash                     -0.1300        0.9885
magnesium                              0.1080        0.9568
total_phenols                          0.0210        1.0078
flavanoids                             0.0440        1.0500
nonflavanoid_phenols                   0.0020        1.0447
proanthocyanins                       -0.0090        0.9879
color_intensity                        0.0680        0.9936
hue                                    0.0080        1.0092
od280/od315_of_diluted_wines           0.0050        1.0302
proline                                7.4140        1.0452
```

**If the accuracies come out the same, was the leak harmless?**

No — it was *lucky*, which is a different thing. The two scalers demonstrably learned different parameters: the `proline` mean differs by 7.41, and several scale factors differ by 4–5%. Version A used the mean and standard deviation of the test wines to decide how to transform the training wines, so a tiny amount of information about the "unseen" data was baked into the model before it ever saw a label. On this split the effect happened to be too small to move any of the 36 predictions, but you could only discover that *after* running both — which means you can never rely on it in advance.

There are two deeper reasons the habit matters more than this particular number. First, the size of a leak scales with how aggressive the preprocessing is: standardization is mild, but things like fitting a feature selector, an imputer, or a resampling step on the full dataset can move accuracy by many points. Second, the whole purpose of a test set is to answer the question *"what will happen on data that genuinely did not exist when I built this?"* Once test rows have touched any part of the build, the answer you get is no longer an answer to that question, however close to correct it happens to be. A pipeline costs one line and makes the mistake structurally impossible, which is why professionals use one every time rather than deciding case by case whether this particular leak is small enough to tolerate.

</details>

---

[⬅ Previous](module-07-visualizing-data.md) · [Level 2 Home](README.md) · [Next ➡](module-09-trees-lines-and-overfitting.md)
