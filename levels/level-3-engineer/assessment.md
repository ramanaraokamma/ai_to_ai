# 📝 Level 3 Assessment — Prove You Can Engineer It

**Level 3 · Assessment · ~2.5 hours · Prereqs: all nine Level 3 modules**

[⬅ Module 9](module-09-classic-nlp.md) · [Level 3 Home](README.md) · [Capstone ➡](capstone.md) · [Glossary](glossary.md)

---

## 🎯 What This Is For

This is not a test you can fail. It is a **map of your holes**, and holes are far cheaper to find here than three days into the capstone with a service that returns the wrong answer and no log to tell you why.

Level 3's bugs are **silent**. Almost nothing in this assessment raises an exception. That is the whole point: a Level 2 bug crashes, a Level 3 bug prints `0.994` and smiles at you. So most items here ask the same underlying question — *is this number trustworthy?*

Three parts, 70 points, about two and a half hours:

| Part | Items | Points each | Total | What it checks |
|---|:--:|:--:|:--:|---|
| **A — Multiple choice** | 20 | 1 | 20 | Do you know what the code actually does? |
| **B — Short answer** | 8 | 3 | 24 | Can you explain *why*, in words, to a person? |
| **C — Debug** | 4 | 6.5 | 26 | Can you find the silent bug and fix it? |
| | | | **70** | |

### How to sit it

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  RULES OF ENGAGEMENT                                             │
   ├──────────────────────────────────────────────────────────────────┤
   │  ✅  Paper, pen, and a calculator for the arithmetic.            │
   │  ✅  The glossary, if a word blanks on you.                      │
   │  ❌  No running the code. Predict the output in your head        │
   │      first — reading code for silent bugs IS the skill being     │
   │      tested, and a runtime doesn't help you when nothing         │
   │      raises.                                                     │
   │  ❌  No peeking at the answer key until you have written         │
   │      something for EVERY item, including the guesses. A wrong    │
   │      written answer teaches you more than a blank one.           │
   │                                                                  │
   │  Afterwards: actually run the four debug programs, broken        │
   │  and then fixed. Watching the number move is half the point.     │
   └──────────────────────────────────────────────────────────────────┘
```

Every item is tagged with the module it comes from, like `[M6]`, so a wrong answer tells you exactly which file to reopen.

---

# Part A — Multiple Choice (20 × 1 point)

Pick **one** answer per question.

---

**Q1. `[M1]`** Your pizza-delivery table has 2,000 orders, of which **28.8% are late**. You run:

```python
from sklearn.dummy import DummyClassifier
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(dummy.score(X_val, y_val))
```

Roughly what does it print, and what does that number mean?

- **A.** About `0.288` — the dummy always predicts "late"
- **B.** About `0.500` — a dummy is always a coin flip
- **C.** About `0.712` — the floor your real model has to beat
- **D.** About `0.000` — a dummy has learned nothing, so it scores nothing

---

**Q2. `[M1]`** You split 2,000 rows into 1,200 train / 400 validation / 400 test. Which statement is correct?

- **A.** Train fits the weights; validation picks the model, features and threshold; test is opened exactly once, at the end, and never tuned against
- **B.** Train fits the weights; test picks the model; validation is a spare set in case the test set is unlucky
- **C.** Train and validation are both used to fit weights; test measures overfitting during training
- **D.** All three are interchangeable as long as the split is stratified

---

**Q3. `[M2]`** A numeric column has **mean 5** and **standard deviation 2** on the training set. After `StandardScaler`, what does the raw value `9` become?

- **A.** `0.8`
- **B.** `1.8`
- **C.** `2.0`
- **D.** `4.0`

---

**Q4. `[M2]`** Your delivery-lateness model jumps from AUC 0.78 to AUC 0.978 when you add the column `customer_called_support`. What is this, and what should you do?

- **A.** A great feature — customer behaviour is genuinely predictive, so keep it
- **B.** **Target leakage** — the call mostly happens *because* the order was already late, so the column is empty at prediction time. Drop it
- **C.** **Preprocessing leakage** — fix it by moving the scaler inside the `Pipeline`
- **D.** **Temporal leakage** — fix it by splitting on the timestamp instead of randomly

---

**Q5. `[M3]`** A fraud model produces this confusion matrix, with rows = actual and columns = predicted:

```
                 PREDICTED
              legit     fraud
ACTUAL legit │  5941  │     2   │
       fraud │    53  │     4   │
```

What is the **recall** for fraud?

- **A.** `0.667`
- **B.** `0.070`
- **C.** `0.127`
- **D.** `0.9997`

---

**Q6. `[M3]`** You lower the decision threshold from `0.5` to `0.2`. What happens?

- **A.** Recall goes up (or stays equal); precision usually goes down
- **B.** Precision goes up; recall goes down
- **C.** Both go up — that's why threshold tuning is worth doing
- **D.** Nothing changes; the threshold only affects `predict_proba`, not the metrics

---

**Q7. `[M3]`** On a dataset that is **0.95% positive**, your model gets **average precision = 0.19**. Is that good?

- **A.** No — anything under 0.5 is worse than random
- **B.** No — AP is on the same scale as accuracy, so 0.19 means it's wrong 81% of the time
- **C.** Yes — AP's no-skill baseline is the positive rate, `0.0095`, so 0.19 is about 20× baseline
- **D.** You can't tell — AP has no baseline

---

**Q8. `[M4]`** Your logistic-regression training loss drops for two epochs and then sits at exactly **0.6931** for the next 5,000. What does that number tell you?

- **A.** The model has converged to the optimum
- **B.** `0.6931` is `ln 2` — the model is outputting `0.5` for every single row and has learned nothing
- **C.** The loss function is misconfigured; log loss can never be below 1
- **D.** The data is perfectly separable, so the loss has bottomed out

---

**Q9. `[M4]`** You start at `w = 0`, learning rate `lr = 1.0`, and compute `∂L/∂w = −0.5`. After one gradient-descent step, `w` is:

- **A.** `−0.5`
- **B.** `+0.5`
- **C.** `0.0`
- **D.** `−1.0`

---

**Q10. `[M5]`** You build `Linear(2, 16) → Linear(16, 1)` and forget the activation between them. What have you built?

- **A.** A network that raises a shape error
- **B.** A 2-layer network that is slightly weaker than one with ReLU
- **C.** Something exactly equivalent to a single linear layer — no curved decision boundary is possible
- **D.** A network that trains fine but is slower

---

**Q11. `[M5]`** You initialize every weight in your MLP to `0.0`. What happens on `make_moons`?

- **A.** It trains normally — zeros are a neutral starting point
- **B.** Every hidden unit computes the same thing and receives the same gradient forever, so the network never breaks symmetry and the loss parks at `0.6931`
- **C.** NumPy raises a `ZeroDivisionError` in the backward pass
- **D.** It converges faster because there is nothing random to undo

---

**Q12. `[M6]`** You write a PyTorch training loop but forget `optimizer.zero_grad()`. What do you see?

- **A.** `RuntimeError: Trying to backward through the graph a second time`
- **B.** Nothing raises. Gradients accumulate across every batch, the effective step gets bigger and bigger, and accuracy ends up far worse than it should be
- **C.** The weights never change at all, so the loss is flat
- **D.** Only the first batch of each epoch trains; the rest are ignored

---

**Q13. `[M6]`** Your `predict.py` gives a **different class** each time you run it on the same saved image. The most likely cause is:

- **A.** `torch.load` is non-deterministic
- **B.** You forgot to set a random seed before loading
- **C.** You forgot `model.eval()`, so `Dropout` is still randomly zeroing units at inference time
- **D.** The `.pt` file is corrupt

---

**Q14. `[M7]`** A `32×32` input goes into `nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1)`. What is the spatial size of the output?

- **A.** `32 × 32`
- **B.** `16 × 16`
- **C.** `15 × 15`
- **D.** `30 × 30`

---

**Q15. `[M7]`** You build one `transforms.Compose` with `RandomHorizontalFlip` and `RandomCrop` in it and use it for the training set *and* the test set. What is wrong?

- **A.** Nothing — more augmentation is always better
- **B.** Your test number now measures accuracy on randomly mangled images, so it is noisy, pessimistic, and not comparable to anyone else's — the test transform must be deterministic
- **C.** It will crash, because augmentation requires labels
- **D.** It leaks the test set into training

---

**Q16. `[M8]`** You want to choose `k` for k-means, so you run `k = 2…10` and pick the `k` with the **lowest inertia**. What's wrong?

- **A.** Nothing — inertia is exactly the quantity k-means minimises
- **B.** Inertia falls monotonically as `k` rises, so this always picks the largest `k` you tried; you want the **bend**, cross-checked with silhouette
- **C.** Inertia is only defined for `k = 2`
- **D.** Inertia rises with `k`, so you should pick the highest one

---

**Q17. `[M8]`** You run PCA on raw wine data where `proline` ranges 278–1680 and `hue` ranges 0.48–1.71, without standardizing. What happens?

- **A.** PC1 is essentially the `proline` axis, because PCA maximises variance and `proline` has by far the largest raw variance
- **B.** Nothing — PCA standardizes internally
- **C.** PCA raises an error on unscaled input
- **D.** PC1 becomes the average of all features equally weighted

---

**Q18. `[M9]`** In a 4-document corpus, sklearn's smoothed IDF is `ln((1 + n) / (1 + df)) + 1`. Which word gets the **largest** IDF weight?

- **A.** The word appearing in all 4 documents
- **B.** The word appearing in 3 documents
- **C.** The word appearing in 1 document
- **D.** The word with the highest raw count in any single document

---

**Q19. `[M9]`** Under plain bag-of-words with unigrams, which pair produces **identical** feature vectors?

- **A.** `"the pizza was great"` and `"the pizza was cold"`
- **B.** `"the dog bit the man"` and `"the man bit the dog"`
- **C.** `"great pizza"` and `"pizza"`
- **D.** `"good"` and `"not good"`

---

**Q20. `[M9]` `[M2]`** A classmate writes:

```python
Xtr = vec.fit_transform(X_train)
Xte = vec.fit_transform(X_test)
```

What is the consequence?

- **A.** Harmless — it's the same vectorizer object, so nothing changes
- **B.** The vectorizer relearns its vocabulary and IDF from the test set, so column 47 means a different word in `Xte` than it did in `Xtr` — the reported score is meaningless, and it will often raise a feature-count error instead
- **C.** It only affects speed
- **D.** It makes the test score artificially *low*, so it is a safe, conservative mistake

---

<br>

---

# Part B — Short Answer (8 × 3 points)

Two to five sentences each unless it says otherwise. Numbers earn marks; vibes do not.

---

**S1. `[M1]`** Explain why a model that cannot beat its baseline is worthless, using the pizza-lateness numbers (28.8% late). Then state the two things you must always print *next to* an accuracy figure.

---

**S2. `[M2]`** Name the **three** kinds of leakage taught in this level. For each, give a one-line concrete example, and say **which direction** it moves the score you report versus the score you'd actually get in production.

---

**S3. `[M3]`** A missed fraud costs **500** units; a false alarm costs **10**. Explain, with the arithmetic written out, how you choose a decision threshold — and why "the F1-optimal threshold" is the wrong answer here.

---

**S4. `[M4]`** Explain why squared error is the wrong loss for classification and log loss is right. Include the cost of predicting `0.05` when the truth is `1`, and say what that cost would have been under squared error.

---

**S5. `[M5]`** Explain backpropagation to someone who knows the chain rule but has never seen a neural network, in one paragraph. Then say what a **gradient check** is, what number counts as passing, and why you would ever bother when PyTorch exists.

---

**S6. `[M6]`** Autograd computes your gradients for you. State precisely **what job it removed** from you and **what job it did not**. Name one bug that autograd will happily compute perfect gradients for.

---

**S7. `[M8]`** You cluster a dataset, get `k = 3`, silhouette `0.28`, and a beautiful 2-D PCA plot where `PC1 + PC2 = 55%` of the variance. Write the honest three-sentence summary you would put under that plot. Say what "no ground truth" costs you here.

---

**S8. `[M9]`** Explain in plain words why IDF boosts rare words, using `and` (idf 1.916) and `pizza` (idf 1.223) from the four-review corpus. Then name one review your TF-IDF classifier gets wrong *because word order was thrown away*, and say why adding bigrams is only a partial fix.

---

<br>

---

# Part C — Debug (4 × 6.5 points)

Every one of these **runs**. Not one of them raises the error you'd want it to. Find the problems, rank them worst-first, and write the fix.

---

**D1. `[M1]` `[M2]` `[M3]`** — *The 0.994 that means nothing*

This trains a fraud detector on a table where 0.95% of rows are fraud.

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("transactions.csv")
# columns: amount, hour, merchant_type, country,
#          chargeback_filed, is_fraud

y = df["is_fraud"]                                          # line 13
X = df.drop(columns=["is_fraud"])                           # line 14

num = ["amount", "hour", "chargeback_filed"]                # line 16
cat = ["merchant_type", "country"]                          # line 17

X[num] = StandardScaler().fit_transform(X[num])             # line 19

X_train, X_test, y_train, y_test = train_test_split(        # line 21
    X, y, test_size=0.2, random_state=0)                    # line 22

pre = ColumnTransformer([
    ("c", OneHotEncoder(), cat),                            # line 25
], remainder="passthrough")

pipe = Pipeline([("pre", pre), ("clf", LogisticRegression())])
pipe.fit(X_train, y_train)

print("accuracy:", pipe.score(X_test, y_test))              # line 31
# accuracy: 0.9942

joblib.dump(pipe.named_steps["clf"], "fraud_v1.joblib")     # line 34
```

It prints `0.9942` and saves a file. There are **five** separate problems. Find them all and rank them worst-first.

---

**D2. `[M4]` `[M5]`** — *The descent that climbs*

Hand-rolled logistic regression on the four-student dataset from Module 4. You know the right answer: after one step from `w = 0` with `lr = 1.0`, `w` should be `+0.5` and the loss should fall from `0.693147` to `0.653920`.

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

X = np.array([[1.0], [2.0], [3.0], [4.0]])     # 4 rows, 1 feature
y = np.array([0, 0, 1, 1])                     # line 7

w = np.zeros((1, 1))
b = 0.0
lr = 1.0

for epoch in range(200):
    z = X @ w + b                              # line 14  -> shape (4, 1)
    p = sigmoid(z)

    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))   # line 18

    dz = (p - y) / len(y)                      # line 20
    dw = X.T @ dz                              # line 21
    db = dz.sum()

    w += lr * dw                               # line 24
    b += lr * db                               # line 25

    if epoch % 50 == 0:
        print(epoch, round(float(loss), 6))
```

It runs, prints numbers, and the loss goes **up**. There are **three** bugs. Find all three, say which is worst and why, and write the corrected loop.

---

**D3. `[M6]`** — *The loop that won't learn*

```python
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

X = torch.randn(600, 20)
y = (X[:, 0] + X[:, 1] > 0).long()

train_dl = DataLoader(TensorDataset(X[:500], y[:500]),
                      batch_size=32, shuffle=True)
val_dl   = DataLoader(TensorDataset(X[500:], y[500:]), batch_size=32)

model = nn.Sequential(
    nn.Linear(20, 64), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(64, 2), nn.Softmax(dim=1),        # line 15
)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(20):
    for xb, yb in train_dl:
        out = model(xb)                         # line 22
        loss = loss_fn(out, yb)
        loss.backward()
        opt.step()                              # line 25

    correct = 0
    for xb, yb in val_dl:                       # line 28
        correct += (model(xb).argmax(1) == yb).sum().item()
    print(epoch, correct / 100)
```

The task is separable by a straight line, so this should reach ~99%. It reaches about 60% and wobbles. There are **four** problems. Find them, and write the corrected loop.

---

**D4. `[M9]` `[M3]`** — *The sentiment model that scored 1.00*

The corpus is 400 reviews, 360 positive and 40 negative.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0)          # line 7

vec = TfidfVectorizer(stop_words="english")                 # line 9
Xtr = vec.fit_transform(X_train)                            # line 10
Xte = vec.fit_transform(X_test)                             # line 11

clf = LogisticRegression().fit(Xtr, y_train)
print("accuracy:", accuracy_score(y_test, clf.predict(Xte)))  # line 14
```

On the day it worked it printed `accuracy: 0.91`, and the author declared victory. There are **four** problems. Find them, rank them, and write the fixed version.

---

<br>

---

# ✅ Answer Key

<details>
<summary><b>Click to reveal answers — but only after you have written something for every item</b></summary>

<br>

## Part A — Multiple Choice

---

### Q1 `[M1]` — **C. About `0.712`**

`strategy="most_frequent"` finds the majority class in the training labels (**on time**, 71.2%) and predicts it for every row, forever. On a stratified validation set that scores about `0.712`.

That number is the **floor**. It is what "no model at all" is worth. If your fancy pipeline scores 0.70, it is *worse than a constant* and you should delete it.

| Why the others are wrong | |
|---|---|
| **A** `0.288` | That would be a dummy always predicting the *minority* class — `strategy="constant", constant=1`. |
| **B** `0.500` | 0.5 is the coin-flip accuracy on a **balanced** binary problem. This problem isn't balanced, so the constant predictor does much better than a coin. |
| **D** `0.000` | A dummy has learned nothing but still scores — that's the whole uncomfortable point. Being right by accident is still being right, which is exactly why accuracy alone is a bad metric here. |

---

### Q2 `[M1]` — **A. Train fits weights; validation picks model/features/threshold; test is opened exactly once**

The three splits are practice papers, a mock exam, and the sealed final. Every time you look at a set and change something because of what you saw, that set stops being an honest estimate of unseen performance. The validation set is *designed* to be burned that way. The test set gets exactly one look, at the very end, and you report whatever it says.

| Why the others are wrong | |
|---|---|
| **B** | Backwards. If test picks the model, test is now a validation set and you have no honest final number left. |
| **C** | Fitting weights on validation destroys its only job. And "measuring overfitting during training" is precisely what validation is for. |
| **D** | Stratification balances *classes* across splits. It does nothing about which split you're allowed to peek at. |

---

### Q3 `[M2]` — **C. `2.0`**

Standardization is `z = (x − mean) / std` = `(9 − 5) / 2` = `4 / 2` = **2.0**. The value 9 sits two standard deviations above the training mean.

Note the two words that carry all the weight: **training** mean and **training** std. `StandardScaler` learns them in `fit()` on the training rows only, and reuses them unchanged in `transform()` on validation and test.

| Why the others are wrong | |
|---|---|
| **A** `0.8` | That's min-max-ish thinking, or `9/(5+2·...)`. There's no division by a range here. |
| **B** `1.8` | `9/5` — you divided by the mean instead of subtracting it. |
| **D** `4.0` | You subtracted the mean and forgot to divide by the std. That's **centering**, not standardizing. |

---

### Q4 `[M2]` — **B. Target leakage — drop it**

The test is the **availability question**: *at the exact moment I need this prediction, is this value filled in?* A support call about a late delivery happens **after** the delivery is late. At prediction time (order placed, driver not dispatched), the column is empty or zero for everyone. The model has learned to read the answer off the back of the card.

The tell is the size of the jump. 0.78 → 0.978 from one column is not a feature, it is a confession. Treat any large unexplained jump as a leak until you have proven otherwise.

| Why the others are wrong | |
|---|---|
| **A** | It *is* genuinely correlated. That's not the issue — availability is. A perfectly correlated feature that doesn't exist yet is worth zero. |
| **C** | Preprocessing leakage is statistics (means, medians, vocabularies) computed before the split. Nothing here is about a transform. |
| **D** | Temporal leakage is training on the future and testing on the past. This bug survives any split strategy you choose. |

---

### Q5 `[M3]` — **B. `0.070`**

Read the numbers off the matrix: `TN = 5941`, `FP = 2`, `FN = 53`, `TP = 4`.

```
Recall = TP / (TP + FN) = 4 / (4 + 53) = 4 / 57 = 0.0702
```

Recall reads **across the actual-positive row**: of the 57 real frauds, you caught 4. That is a catastrophe hiding behind an accuracy of `(5941 + 4) / 6000 = 0.9908`.

| Why the others are wrong | |
|---|---|
| **A** `0.667` | That's **precision**: `TP / (TP + FP) = 4 / 6`. Precision reads down the *predicted-positive column*. This is the single most common mix-up in the level. |
| **C** `0.127` | That's **F1**: `2 · (0.667 · 0.070) / (0.667 + 0.070)`. |
| **D** `0.9997` | That's **specificity**: `TN / (TN + FP) = 5941 / 5943`. It looks wonderful and tells you nothing, because almost everything is negative. |

---

### Q6 `[M3]` — **A. Recall up (or equal); precision usually down**

Lowering the threshold flags more rows as positive. More flags means you catch more of the real positives (**recall can only rise or stay flat**) but you also sweep in more junk, so precision usually falls.

"Usually" is doing real work in that sentence. Precision is **not monotonic** — in Module 3's worked sweep it went 1.000, 1.000, 0.667, 0.750, 0.800, 0.667, 0.714. It ticks up whenever the next item down the ranking happens to be a true positive.

| Why the others are wrong | |
|---|---|
| **B** | That's what *raising* the threshold does. |
| **C** | If moving one dial improved both, there would be no trade-off and no reason for a PR curve to exist. |
| **D** | The threshold is exactly how `predict_proba` output becomes a hard label. Every count in the confusion matrix depends on it. |

---

### Q7 `[M3]` — **C. Yes — AP's baseline is the positive rate, 0.0095**

A **no-skill** model on a 0.95%-positive dataset has average precision ≈ 0.0095, because if you flag rows at random, 0.95% of your flags are right no matter how many you flag. So AP = 0.19 is roughly **20× baseline** — genuinely useful.

This is the trap of importing ROC intuition into PR space. **ROC-AUC's** baseline is 0.5 regardless of balance. **AP's** baseline is the positive rate. Always print the positive rate next to an AP.

| Why the others are wrong | |
|---|---|
| **A** | Applying ROC's 0.5 baseline to AP. Different curve, different baseline. |
| **B** | AP is not an error rate and is not on accuracy's scale. It is the area under precision-vs-recall. |
| **D** | It has a very clear baseline. That baseline just isn't a constant. |

---

### Q8 `[M4]` — **B. `0.6931` is `ln 2` — the model outputs 0.5 for everything**

If `p = 0.5` for every row, then each row's log loss is `−ln(0.5) = 0.693147`, whatever the label. So a flat `0.6931` is the signature of a model that has learned exactly nothing.

The diagnostic checklist from Module 4: print `w` and `b` (are they still zeros?), print `X.mean()` and `X.std()` per column (did the scaler actually run, or is `X` all zeros?), and check the learning rate isn't so small that nothing has moved.

| Why the others are wrong | |
|---|---|
| **A** | Converged to `ln 2` means converged to ignorance. A logistic loss on separable-ish data goes well below 0.69. |
| **C** | Log loss is unbounded above and its floor is 0. Values like 0.21 or 0.05 are routine. |
| **D** | Perfect separability drives log loss *toward zero* (and the weights toward infinity). It is the opposite symptom. |

---

### Q9 `[M4]` — **B. `+0.5`**

The update rule is `w ← w − lr · ∂L/∂w`:

```
w = 0 − 1.0 × (−0.5) = 0 + 0.5 = +0.5
```

The gradient points **uphill**. You subtract it to go downhill. When the gradient is negative, subtracting it moves `w` *up* — which is right, because the loss decreases in that direction. This is exactly Module 4's iteration 0 → 1.

| Why the others are wrong | |
|---|---|
| **A** `−0.5` | You wrote `w += lr * grad`. This is *the* sign error, and its symptom is a loss that rises even at a tiny learning rate. |
| **C** `0.0` | Only if the gradient were 0 — which happens to `b` in that worked example, but not to `w`. |
| **D** `−1.0` | Sign error plus a doubled step. |

---

### Q10 `[M5]` — **C. Equivalent to a single linear layer**

`(x W₁ + b₁) W₂ + b₂ = x (W₁W₂) + (b₁W₂ + b₂)`. The product `W₁W₂` is just another matrix. You have spent 33 extra parameters to rebuild logistic regression, and no amount of training will produce a curved boundary.

The activation is not decoration. **The non-linearity is the entire reason depth buys you anything.**

| Why the others are wrong | |
|---|---|
| **A** | Shapes are perfectly fine: `(n,2) @ (2,16) @ (16,1)` composes cleanly. It runs, which is why this bug is silent. |
| **B** | Not "slightly weaker" — *exactly* as expressive as one linear layer. If your MLP scores precisely what logistic regression scored, check for this first. |
| **D** | It's marginally *slower* than one layer and no better. Worst of both. |

---

### Q11 `[M5]` — **B. Symmetry never breaks; loss parks at 0.6931**

Every hidden unit starts identical, so on the forward pass every unit computes the same value, and on the backward pass every unit receives the same gradient. They stay identical forever. Sixteen units behave as one. With ReLU it's worse: `z = 0` everywhere means the gradient through the hidden layer is zero-or-arbitrary and `W1` barely moves at all.

The fix is **He initialization**: `rng.normal(0, sqrt(2 / n_in), (n_in, n_hidden))`. Random init isn't sloppiness — it is **symmetry breaking**, and it's load-bearing.

| Why the others are wrong | |
|---|---|
| **A** | Zeros are neutral in the sense of being unbiased, and useless in the sense of being indistinguishable. Biases *can* start at zero; weights cannot. |
| **C** | Nothing divides by anything. No exception is raised — the loss simply refuses to move. |
| **D** | It converges to nothing, immediately, and stays there. |

---

### Q12 `[M6]` — **B. Nothing raises; gradients accumulate**

PyTorch **accumulates** into `.grad` by design (it's what lets you sum gradients across several backward passes on purpose). If you never clear it, batch 40's gradient is the sum of batches 1–40, your effective step size grows without limit, and training turns into noise. Module 6 measures the damage: about 36 accuracy points on FashionMNIST.

`optimizer.zero_grad()` is the **first line of the inner loop**, always. Memorise the four-line liturgy: `zero_grad → forward/loss → backward → step`.

| Why the others are wrong | |
|---|---|
| **A** | That error comes from calling `.backward()` twice on the *same* loss tensor without `retain_graph`. Different bug. |
| **C** | The weights change plenty — far too much. "Flat loss, no movement" is the `lr = 0` or dead-network symptom. |
| **D** | Every batch trains. They just all train with a corrupted, ever-growing gradient. |

---

### Q13 `[M6]` — **C. You forgot `model.eval()`**

`Dropout` is active in training mode and randomly zeroes 20–30% of units on every forward pass. In training that's a regulariser. At inference it's a random number generator attached to your predictions. `model.eval()` switches dropout off (and freezes any batch-norm statistics). Call it **immediately after `load_state_dict`**, before any prediction, and wrap inference in `with torch.no_grad():`.

| Why the others are wrong | |
|---|---|
| **A** | `torch.load` is deterministic — it reads a file. |
| **B** | Seeding would *hide* the symptom by making the randomness repeatable. The randomness shouldn't exist at all. |
| **D** | A corrupt file raises on load; it doesn't quietly return different classes. |

---

### Q14 `[M7]` — **B. `16 × 16`**

```
out = floor((n + 2p − k) / s) + 1
    = floor((32 + 2 − 3) / 2) + 1
    = floor(31 / 2) + 1
    = floor(15.5) + 1
    = 15 + 1
    = 16
```

Learn the two combinations you'll use constantly: `k=3, s=1, p=1` **preserves** size, and `k=2, s=2` pooling **halves** it. Everything else, compute on paper before you run — that's how you avoid `mat1 and mat2 shapes cannot be multiplied`.

| Why the others are wrong | |
|---|---|
| **A** `32` | That's `s=1, p=1`. Stride 2 halves the map. |
| **C** `15` | You did the floor and forgot the `+ 1`. Classic off-by-one. |
| **D** `30` | That's `s=1, p=0`. You dropped both the padding and the stride. |

---

### Q15 `[M7]` — **B. The test number is noisy, pessimistic and not comparable**

Augmentation is **free extra training data**: a mirrored cat is still a cat, so showing the model flipped and cropped copies teaches invariance. But evaluation must be a fixed, repeatable measurement. If you randomly crop the test images, you're grading the model on a harder, randomly different exam every run — the number moves when nothing about the model moved.

Keep **two transform objects**: `train_tf` with randomness, `eval_tf` with resize/normalize only, and never let them cross. It is the same discipline as fit-on-train-only from Module 2, wearing a different hat.

| Why the others are wrong | |
|---|---|
| **A** | "More is better" is true for training and false for measurement. |
| **C** | Torchvision transforms act on images and never see the label. No crash. |
| **D** | Nothing flows from test to train here. The damage is to the *measurement*, not the training. |

---

### Q16 `[M8]` — **B. Inertia falls monotonically, so this always picks the largest `k`**

Inertia (within-cluster sum of squares) can only go down as you add centroids, all the way to zero at `k = n`, where every point is its own cluster. Minimising it is therefore a non-question with a useless answer.

What you actually do: look for the **elbow** — where the curve stops dropping steeply — and cross-check with **silhouette**, which *can* have an interior maximum because it penalises clusters that overlap. Then apply domain sense. And if the curve is a smooth arc with no bend, say so out loud; on real data that happens constantly.

| Why the others are wrong | |
|---|---|
| **A** | k-means minimises inertia *for a fixed k*. Comparing inertia *across* different k is a different question with a degenerate answer. |
| **C** | Inertia is defined for every `k ≥ 1`. |
| **D** | It falls, not rises. |

---

### Q17 `[M8]` — **A. PC1 becomes essentially the `proline` axis**

PCA looks for the direction of **greatest variance**, and variance is measured in the squared units of the raw column. `proline` spans ~1,400 units; `hue` spans ~1.2. In squared units that's a factor of about a million. PC1 will be almost pure `proline`, and your "principal component" is a statement about your measurement units, not your data.

Standardize first — unless every feature is already in the same natural unit *and* you deliberately want the scale to matter.

| Why the others are wrong | |
|---|---|
| **B** | `sklearn.decomposition.PCA` centres the data but does **not** scale it. That's why `make_pipeline(StandardScaler(), PCA())` is the standard idiom. |
| **C** | No error. It cheerfully returns a component you'll misinterpret. |
| **D** | Equal weighting would only happen if all features had equal variance — which is exactly what standardizing gives you. |

---

### Q18 `[M9]` — **C. The word appearing in 1 document**

With `n = 4`:

```
df = 1  →  ln(5/2) + 1 = 0.9163 + 1 = 1.9163   ← largest
df = 2  →  ln(5/3) + 1 = 0.5108 + 1 = 1.5108
df = 3  →  ln(5/4) + 1 = 0.2231 + 1 = 1.2231
df = 4  →  ln(5/5) + 1 = 0      + 1 = 1.0000   ← smallest
```

IDF is a **rarity bonus**. A word in every document distinguishes nothing, so it gets the smallest weight; a word in one document is a fingerprint for that document, so it gets the largest.

| Why the others are wrong | |
|---|---|
| **A** | That's the *minimum* — with smoothing it bottoms out at exactly 1.0, not 0. |
| **B** | Middling `df`, middling idf. |
| **D** | That's **term frequency**, the other half of TF-IDF. IDF depends only on *how many documents* contain the word, never on how often. |

---

### Q19 `[M9]` — **B. `"the dog bit the man"` and `"the man bit the dog"`**

Both contain `the`×2, `dog`×1, `bit`×1, `man`×1. Identical counts, identical vector, cosine similarity 1.0 — and opposite meanings. That is the defining limitation of bag-of-words, and it's why Level 4's sequence models exist.

| Why the others are wrong | |
|---|---|
| **A** | `great` vs `cold` differ, so the vectors differ. |
| **C** | Different lengths and different counts; `"great pizza"` has a `great` the other lacks. |
| **D** | `"not good"` has an extra token. Under *unigrams* the vectors differ by one dimension — but note the classifier still often gets it wrong, because `not` on its own is a weak, near-neutral feature. Word order isn't destroyed here; it's *ignored*. |

---

### Q20 `[M9]` `[M2]` — **B. It relearns the vocabulary and IDF from test; the score is meaningless**

`fit_transform` on test does two bad things at once.

1. **Leakage.** The vocabulary and IDF table are now built from data you were supposed to be blind to.
2. **Worse: the columns stop meaning the same thing.** `Xtr` column 47 might be `delicious`; `Xte` column 47 might be `delivery`. The trained coefficients are indexed by position, so you're multiplying the wrong weights by the wrong words. Usually the two vocabularies differ in size and sklearn raises `X has 812 features, but LogisticRegression is expecting 1043 features as input` — and you should be grateful, because when the sizes happen to match, it silently returns nonsense.

The rule: `fit_transform` on train, `transform` only on test. Put the vectorizer in a `Pipeline` and it becomes impossible to get wrong.

| Why the others are wrong | |
|---|---|
| **A** | Same object, refitted — `fit` *discards* the previous vocabulary. Reusing the object is what makes it look innocent. |
| **C** | It's a correctness bug, not a performance one. |
| **D** | Leakage inflates scores far more often than it deflates them, and the column-misalignment bug is unpredictable in either direction. "Safe conservative mistake" is not a category that exists here. |

---

<br>

## Part B — Short Answer

Three points each: **1** for the core idea, **1** for the numbers/specifics, **1** for the "so what."

---

### S1 `[M1]` — the baseline

**Model answer.** The pizza data is 28.8% late, so a model that says "on time" every single time — no features, no training, no thought — is right 71.2% of the time. If my pipeline reports 70% accuracy, it has spent an hour of compute to be *worse than a constant string*. A score is not a fact until it is a **comparison**; 0.71 alone is a boast, 0.71 against a 0.712 baseline is a verdict.

The two things that must always be printed next to an accuracy figure:

1. **The baseline** (majority-class rate, or `DummyClassifier`'s score on the same split).
2. **The size and class balance of the set it was measured on** — 0.87 on 40 rows with 3 positives is one lucky afternoon, not a result.

*(Credit also for: the metric name and its units; a spread from cross-validation rather than one number.)*

---

### S2 `[M2]` — the three leakages

| Leakage | One-line example | Direction |
|---|---|---|
| **Target leakage** | `customer_called_support`, `chargeback_filed`, `refund_issued` — a column that only gets filled in *because* the outcome already happened | Reported score is **far too high** (0.978 vs a real 0.78). Production performance collapses on day one because the column is empty. |
| **Temporal leakage** | Random-splitting time-ordered orders, so the model trains on December and tests on November | Reported score is **too high** (0.79 random-split vs 0.56 time-split). You've measured interpolation and will deploy extrapolation. |
| **Preprocessing leakage** | `StandardScaler().fit_transform(X)` before `train_test_split`, or `SimpleImputer` learning its median from all rows, or a `TfidfVectorizer` fitted on train+test | Reported score is **too high** — usually mildly, sometimes absurdly. Module 2 gets 83% accuracy on *pure noise* with an aggressive version of it. |

**The one-line summary that earns the third mark:** all three are the same crime — the model was allowed to see something at training time that it will not have at prediction time — and two of the three are prevented for free by putting every transform inside a `Pipeline` and splitting first.

---

### S3 `[M3]` — the cost-based threshold

**Model answer.** I don't pick the threshold by eye. I sweep it and minimise **expected cost**:

```
Cost(t) = 500 × FN(t) + 10 × FP(t)
```

For every candidate threshold in the sorted list of predicted probabilities, I compute the confusion matrix on the **validation** set and evaluate that expression. Worked example from the module: at one threshold, `FN = 18` and `FP = 542`:

```
Cost = 500 × 18  +  10 × 542
     = 9,000     +  5,420
     = 14,420
```

I pick the `t` with the smallest total, then report the final metrics on the untouched **test** set at that frozen threshold. The threshold is a number I can defend with arithmetic, and it goes in the model card.

**Why F1 is wrong here.** F1 is the harmonic mean of precision and recall, which silently assumes a false positive and a false negative matter *equally*. Here a miss costs **50× more** than a false alarm. Optimising F1 would pick a much higher threshold than the cost arithmetic does, and every fraud it lets through is worth 50 wasted phone calls. When you know the costs, use the costs; F1 is the metric for when you don't.

---

### S4 `[M4]` — log loss vs squared error

**Model answer.** Squared error is wrong for classification for two reasons. First, it barely punishes confident wrongness: predicting `0.05` when the truth is `1` costs `(1 − 0.05)² = 0.9025` — less than 1, and not much worse than the `0.25` you'd get for shrugging and saying 0.5. Second, when you push a sigmoid output through squared error the resulting loss surface is **non-convex**, so gradient descent can get stuck in a local dip.

Log loss punishes confidence properly. Predicting `0.05` when the truth is `1` costs:

```
−ln(0.05) = 2.9957
```

That's **3.3× worse** than squared error's 0.9025, and as the prediction approaches 0 the cost goes to infinity. Log loss measures *surprise*, so a model that is sure and wrong pays enormously — which is exactly the behaviour you want from something that will be trusted.

And a bonus: log loss over a sigmoid is convex, and its gradient collapses to the beautiful `(p − y) · x`, one bowl with one bottom.

---

### S5 `[M5]` — backprop and the gradient check

**Model answer.** A network is a chain of functions: inputs go through a weighted sum, a squash, another weighted sum, another squash, and finally into a loss. To improve a weight buried in the first layer, I need to know how much the final loss changes when I nudge it — and the chain rule says that's just the product of the local slopes along every step of the path from that weight to the loss. Backpropagation computes the forward pass once, then walks *backwards*, carrying the accumulated slope with it, so every weight in the whole network gets its gradient in a single sweep instead of one expensive pass per weight. It is bookkeeping, not new mathematics.

A **gradient check** verifies that bookkeeping numerically. Nudge one weight by `ε = 1e-6` in each direction, recompute the loss both times, and estimate the slope as `(L₊ − L₋) / (2ε)`. Compare with your analytic gradient using **relative error** `|a − b| / (|a| + |b|)`. Below `1e-6` is a pass (Module 5 gets `3.7e-08`); anything around `1e-3` or `0.5` is a bug — a missing `keepdims=True` on a bias sum, or a forgotten `/n`.

**Why bother when PyTorch exists?** Because the check is how you *know* you understand the calculus rather than trusting a library, and because the same technique catches a wrong custom loss or a hand-written layer in PyTorch too. Autograd differentiates whatever you wrote — including the wrong thing.

---

### S6 `[M6]` — what autograd removed, and what it didn't

**Model answer.**

**What it removed:** deriving and hand-coding the backward pass. You no longer write `dZ1 = (dA1 * (Z1 > 0))`, you no longer have to remember `keepdims=True` on the bias sums, and you no longer have to divide by `n` in three places. PyTorch records every operation into a computation graph as you run the forward pass, and `loss.backward()` walks it in reverse applying the chain rule.

**What it did not remove:** deciding *what to differentiate*. Autograd computes a perfectly correct gradient of whatever loss you actually wrote, on whatever tensors you actually fed it. It has no opinion about whether that was the right loss, the right shapes, or the right data.

**A bug autograd computes perfect gradients for:** ending the model with `nn.Softmax(dim=1)` and then using `nn.CrossEntropyLoss`, which applies log-softmax internally. The squash is applied twice. Nothing raises, the gradients are exactly right *for that wrong objective*, and your accuracy quietly caps out low. *(Equally good answers: forgetting `zero_grad()`; a target-leaking feature; `y` shaped `(n,)` broadcasting against `(n,1)`; scaling fitted on the full dataset.)*

---

### S7 `[M8]` — the honest caption

**Model answer.** Something close to:

> "k-means with k = 3 on the standardized features gives a silhouette of **0.28**, which is *real but overlapping* structure — the groups exist, but many points sit near a boundary and would move under a different random seed. The plot shows the first two principal components, which together capture only **55%** of the total variance, so two points that look adjacent here may be far apart in the 45% of the spread that isn't drawn. Cluster 3 is the weakest: it has the lowest mean silhouette and its profile differs from Cluster 1 on only two features."

**What "no ground truth" costs you:** there is no test set and no accuracy, because there is no right answer to be graded against. Nothing can tell you whether these groups are *real* or just an artefact of `k`, the scaling, and the seed. So the burden of proof moves onto you: multiple lines of evidence (elbow *and* silhouette), a stability check with a different seed, a profile table showing each cluster differs on features a human can name — and an honest sentence about which cluster you trust least. Reporting weak structure as weak is a finding, not a failure.

---

### S8 `[M9]` — IDF, and what bag-of-words loses

**Model answer.** IDF asks "how many documents contain this word?" and rewards the answer *few*. In the four-review corpus, `and` appears in one review, so `idf = ln(5/2) + 1 = 1.916`; `pizza` appears in three, so `idf = ln(5/4) + 1 = 1.223`. A word sitting in nearly every document can't help you tell those documents apart, so it gets shrunk toward 1.0; a word appearing in one is a fingerprint, so it gets boosted. Multiply by term frequency and you get a score that is high only for words that are *both* frequent here *and* rare elsewhere — which is a decent working definition of "what this document is about."

**A review it gets wrong:** `"the service was not good and the pizza was not fresh"`. Under unigrams the model sees `good` and `fresh` — two strongly positive features — plus `not` twice, which is weak and near-neutral because it appears in positive and negative reviews alike. It predicts positive. The identical failure runs the other way: `"not bad at all, honestly great"` gets read off `bad`.

**Why bigrams are only a partial fix:** a bigram is a feature only if that exact pair appeared in the *training* corpus. `ngram_range=(1,2)` will help with `not good` if `not good` was in the training data; it does nothing for `not fresh`, `not worth it`, or `never coming back` unless those were there too. It also multiplies the vocabulary several-fold, which makes rare-feature overfitting worse. The real fix is training examples that contain negation — and, in Level 4, a model that reads the sentence in order.

---

<br>

## Part C — Debug

---

### D1 `[M1]` `[M2]` `[M3]` — the 0.994 that means nothing

**Five problems, worst first.**

**1. Target leakage: `chargeback_filed` is in the features (line 16).** A chargeback is filed *after* a fraudulent transaction is discovered. At scoring time — the instant the card is swiped — this column is empty for everyone. This single column is doing most of the work, and it will do none of it in production. **Worst, because the model is fundamentally not the model you think you have.**

**2. Preprocessing leakage: the scaler is fitted before the split (line 19).** `StandardScaler().fit_transform(X[num])` learns means and standard deviations from **all 6,000 rows**, including the 1,200 that become the test set. The reported score is optimistic and the scaler cannot travel with the model — it wasn't saved at all.

**3. Accuracy on a 0.95%-positive problem (line 31).** `0.9942` looks superb and is essentially the majority-class rate (`0.9905`). The model could be catching 3 frauds out of 57 and still print this. There is no baseline, no confusion matrix, no precision/recall, no AUC, and no threshold decision.

**4. `OneHotEncoder()` without `handle_unknown="ignore"` (line 25).** Works in training, raises `Found unknown categories` the first time a new merchant type or country arrives in production.

**5. Only the classifier is saved (line 34).** `pipe.named_steps["clf"]` is the bare `LogisticRegression`. Reloading it gives you a model that expects one-hot-encoded, scaled input and has no idea how to produce it. **Always dump the whole fitted `Pipeline`.** *(Also: no `random_state` on the split is not in the count but is worth a mention, and there's no three-way split — the "test" set is being used as a validation set.)*

**Fixed version:**

```python
import pandas as pd, joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_auc_score, average_precision_score)

df = pd.read_csv("transactions.csv").drop_duplicates()

y = df["is_fraud"]
# fix 1: name the features you WANT. chargeback_filed does not exist
#        at prediction time, so it is not a feature.
num = ["amount", "hour"]
cat = ["merchant_type", "country"]
X = df[num + cat]

# fix 2 + 6: split FIRST, three ways, stratified, seeded.
X_tr, X_tmp, y_tr, y_tmp = train_test_split(
    X, y, test_size=0.40, stratify=y, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(
    X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=0)

pre = ColumnTransformer([
    ("num", StandardScaler(), num),                       # fitted on train only,
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat), # fix 4
])                                                        # because it lives here

pipe = Pipeline([("pre", pre),
                 ("clf", LogisticRegression(max_iter=1000,
                                            class_weight="balanced"))])
pipe.fit(X_tr, y_tr)

# fix 3: baseline first, then metrics that survive imbalance.
dummy = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
print("baseline accuracy:", round(dummy.score(X_val, y_val), 4))
print("positive rate    :", round(y_val.mean(), 4))

proba = pipe.predict_proba(X_val)[:, 1]
print("ROC-AUC          :", round(roc_auc_score(y_val, proba), 4))
print("avg precision    :", round(average_precision_score(y_val, proba), 4))
tn, fp, fn, tp = confusion_matrix(y_val, proba >= 0.5).ravel()
print(f"tn={tn} fp={fp} fn={fn} tp={tp}")
print(classification_report(y_val, proba >= 0.5, digits=3))

# fix 5: the WHOLE pipeline is the artifact.
joblib.dump(pipe, "fraud_v1.joblib")
```

---

### D2 `[M4]` `[M5]` — the descent that climbs

**Three bugs.**

**Bug 1 (worst) — the shape mismatch, line 7 / 20.** `y` has shape `(4,)`; `p` has shape `(4, 1)`. NumPy broadcasts `p - y` into a **`(4, 4)`** matrix, and raises nothing. Every number downstream is garbage: `loss` averages 16 nonsense terms, `dw` becomes `(1,4)`, and `w += lr * dw` silently reshapes `w` from `(1,1)` to `(1,4)`.

*Why this is worse than the sign error:* the sign error produces a wrong answer you can **see** (the loss rises). The shape error produces numbers that are wrong in a way that no plot will tell you about — and it happily survives being "fixed" in other places. Silent beats loud.

Fix: `y = y.reshape(-1, 1)`, then assert it: `assert p.shape == y.shape`.

**Bug 2 — the sign, lines 24–25.** The gradient points **uphill**. `w += lr * dw` walks up the hill. Fix: `w -= lr * dw` and `b -= lr * db`. The tell you already had: with the worked example you *know* `w` should be `+0.5` after step one, and this prints `−0.5`.

**Bug 3 — no clipping before `log`, line 18.** Once the weights grow, `sigmoid` saturates to exactly `1.0` or `0.0` in float64, `np.log(0)` returns `-inf` with a `RuntimeWarning`, and the loss becomes `nan`. Fix: clip `p` into `[1e-12, 1 − 1e-12]` before taking any logarithm.

**Corrected loop:**

```python
import numpy as np

def sigmoid(z):
    # branching form: never overflows exp() for large |z|
    out = np.empty_like(z, dtype=float)
    pos, neg = z >= 0, z < 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[neg])
    out[neg] = ez / (1.0 + ez)
    return out

X = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([0, 0, 1, 1]).reshape(-1, 1)      # fix 1: (4, 1), not (4,)

w = np.zeros((1, 1))
b = 0.0
lr = 1.0
n = len(y)

for epoch in range(200):
    z = X @ w + b
    p = sigmoid(z)
    assert p.shape == y.shape                  # fix 1, enforced

    pc = np.clip(p, 1e-12, 1 - 1e-12)          # fix 3
    loss = -np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc))

    dz = (p - y) / n                           # shape (4, 1) ✓
    dw = X.T @ dz                              # shape (1, 1) ✓
    db = dz.sum()

    w -= lr * dw                               # fix 2: subtract
    b -= lr * db

    if epoch % 50 == 0:
        print(epoch, round(float(loss), 6), "w =", round(float(w), 6))
```

**Expected output** (matches the module's hand-computed trace at epoch 0 → 1):

```
0 0.693147 w = 0.5
50 0.196... w = 1.4...
100 0.152... w = 1.7...
150 0.132... w = 1.9...
```

Epoch 0 prints the loss *before* the step, `0.693147` — `ln 2`, exactly as computed by hand — and `w` becomes `+0.5`. Recomputing the loss after that step gives `0.653920`. Both match the paper trace, which is how you know the code is right.

---

### D3 `[M6]` — the loop that won't learn

**Four problems.**

**1. No `optimizer.zero_grad()` (worst).** Gradients accumulate across all 16 batches of every epoch, so the effective step balloons and training becomes noise. This alone explains most of the missing 39 accuracy points.

**2. `nn.Softmax(dim=1)` as the last layer *with* `nn.CrossEntropyLoss` (line 15).** `CrossEntropyLoss` expects **raw logits** — it applies log-softmax internally. Softmaxing first means the squash happens twice, which flattens the gradients and caps accuracy. End the model with a bare `nn.Linear`.

**3. No `model.eval()` / `model.train()` around the validation loop (line 28).** `Dropout(0.3)` is still active during evaluation, so 30% of the units are randomly zeroed while you're measuring. Your validation number is noisy and too low.

**4. No `torch.no_grad()` in the validation loop.** PyTorch builds a computation graph for every validation batch and immediately throws it away. Wasteful in memory and time, and it's how you eventually meet an out-of-memory error on a big model.

*(Bonus, half a mark: `correct / 100` hard-codes the validation size. Use `len(val_dl.dataset)`.)*

**Corrected loop:**

```python
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)
X = torch.randn(600, 20)
y = (X[:, 0] + X[:, 1] > 0).long()

train_dl = DataLoader(TensorDataset(X[:500], y[:500]),
                      batch_size=32, shuffle=True)
val_ds = TensorDataset(X[500:], y[500:])
val_dl = DataLoader(val_ds, batch_size=32)

model = nn.Sequential(
    nn.Linear(20, 64), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(64, 2),                       # fix 2: bare Linear. No Softmax.
)
loss_fn = nn.CrossEntropyLoss()             # applies log-softmax itself
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

@torch.no_grad()                            # fix 4
def evaluate(dl):
    model.eval()                            # fix 3: dropout OFF
    correct = 0
    for xb, yb in dl:
        correct += (model(xb).argmax(1) == yb).sum().item()
    return correct / len(dl.dataset)        # bonus fix

for epoch in range(20):
    model.train()                           # fix 3: dropout back ON
    for xb, yb in train_dl:
        opt.zero_grad()                     # fix 1: FIRST line of the loop
        out = model(xb)
        loss = loss_fn(out, yb)
        loss.backward()
        opt.step()
    print(f"epoch {epoch:2d}  val acc {evaluate(val_dl):.3f}")
```

**Expected output:** accuracy climbing past `0.95` within a handful of epochs and settling around `0.98–1.00`, because the task really is linearly separable.

---

### D4 `[M9]` `[M3]` — the sentiment model that scored 1.00

**Four problems, worst first.**

**1. `vec.fit_transform(X_test)` on line 11.** Two disasters in one call. The vectorizer relearns its vocabulary and IDF from the test set (leakage), *and* the column indices no longer line up with the columns the classifier was trained on — coefficient 47 now multiplies a different word. Usually the vocabularies differ in size and `predict` raises a feature-count error; when they happen to match, it silently returns nonsense. **Worst, because the reported number measures nothing at all.** Fix: `Xte = vec.transform(X_test)`, or better, put the vectorizer in a `Pipeline` so it cannot happen.

**2. `stop_words="english"` on line 9.** sklearn's English stopword list contains `not`, `no`, `never`, `nothing`, `against`, `cannot`. On a **sentiment** task those are the load-bearing words. `"the pizza was not good"` becomes `['pizza', 'good']` — the model is now looking at a positive review. Fix: drop `stop_words` entirely, or pass a custom list with the negators removed.

**3. Accuracy on a 90%-positive corpus (line 14).** Always predicting "positive" scores `0.90`. The reported `0.91` is one point above doing nothing. Fix: print the baseline and the positive rate, then the confusion matrix and per-class precision/recall — Module 3 does not stop applying just because the data is text.

**4. No baseline, no cross-validation, and a 100-row test set.** With 100 test reviews of which ~10 are negative, a single accuracy figure has an enormous margin of error — one review flipping moves it a full point, and the negative class is decided by ten examples. Fix: `StratifiedKFold` cross-validation reporting mean ± std, and `class_weight="balanced"`.

**Fixed version:**

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, stratify=labels, random_state=0)  # fix 4: stratify

# fix 1 + 2: one Pipeline. The vectorizer can now only ever be fitted on
# training folds, and the negation words stay in the vocabulary.
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True,
                              ngram_range=(1, 2),      # give negation a chance
                              min_df=2,
                              stop_words=None)),       # fix 2: KEEP "not"
    ("clf", LogisticRegression(max_iter=1000,
                               class_weight="balanced")),  # fix 4
])

# fix 3: baseline before anything else.
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("baseline accuracy:", round(dummy.score(X_test, y_test), 3))
print("positive rate    :", round(np.mean(y_train), 3))

# fix 4: a score with a spread, on the training data only.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
print(f"5-fold ROC-AUC   : {scores.mean():.3f} ± {scores.std():.3f}")

pipe.fit(X_train, y_train)
pred = pipe.predict(X_test)

# fix 3: the numbers that survive imbalance.
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, digits=3,
                            target_names=["negative", "positive"]))

# sanity check that fix 2 worked:
vocab = pipe.named_steps["tfidf"].get_feature_names_out()
print("'not' in vocabulary      :", "not" in vocab)
print("'not good' in vocabulary :", "not good" in vocab)
```

The last two lines are the habit worth keeping: **print your vocabulary before you trust your model.** If `not` isn't in there, nothing else you measure about a sentiment classifier means anything.

</details>

---

## 📊 Score Yourself

| Part | Your score | Out of |
|---|:--:|:--:|
| A — Multiple choice | ____ | 20 |
| B — Short answer | ____ | 24 |
| C — Debug | ____ | 26 |
| **Total** | **____** | **70** |

| Band | Score | What it means | What to do |
|---|:--:|---|---|
| 🔴 **Rebuild** | 0–34 | You can follow the modules but you can't yet run the machinery yourself | Redo the mini-projects for the modules your wrong answers cluster in, **from a blank file**. Do not start the capstone — it assumes a working artifact you already trust. |
| 🟠 **Patch** | 35–48 | Real competence with two or three specific holes | Use the module tags. Reread only those modules, redo their practice, re-sit those items. Then start the capstone. |
| 🟡 **Ready** | 49–60 | You can ship it | Start the capstone. Keep the glossary open. Reread whichever module your wrong answers clustered in while the capstone runs. |
| 🟢 **Fluent** | 61–70 | You could teach this level | Start the capstone and take one of its stretch directions. Then go and find someone else's notebook and audit it — you now have the eyes for it. |

**Two diagnostics that matter more than the total.**

1. **Count wrong answers by module tag.** Four wrong in one module is a real gap. Four spread across eight modules is a tired afternoon.
2. **Look at Part C alone.** If you scored well on A and B but under 13 on C, you understand the concepts and cannot yet *see* them in code. That is the most common Level 3 profile, and the only fix is reading broken code: take your own mini-projects, deliberately plant one bug in each, leave them a week, and hunt them down.

---

## ✅ Self-Assessment Checklist

Tick honestly. "I could do it with the module open" is **not** a tick — the standard is *from a blank file, with only the glossary and the library docs*.

### Outcome 1 — Build a complete supervised pipeline to a saved artifact

- [ ] Given a vague sentence from a non-technical person, I can write down the **unit of prediction**, the target `y`, the candidate features `X`, and the metric — before touching code
- [ ] I audit every new table for shape, dtypes, duplicates, missing values, class balance, and near-unique ID columns
- [ ] I split **three ways**, stratified, with a `random_state`, and I can say out loud what each split is allowed to be used for
- [ ] I run a `DummyClassifier` baseline **first**, every time, and print it next to every score I report
- [ ] I can assemble a `Pipeline`, `joblib.dump` it, and load it in a genuinely fresh process that contains **zero training code**
- [ ] I have written a model card with intended use, data description, metrics, and named limitations

### Outcome 2 — Engineer features, and detect leakage

- [ ] I can compute a z-score and a min-max scaling by hand and say when each is appropriate
- [ ] I one-hot unordered categories and ordinal-encode only orderings I can state out loud without wincing
- [ ] I check `nunique()` before one-hot encoding anything, and I always set `handle_unknown="ignore"`
- [ ] I can derive features from dates, ratios, bins and interactions, and I keep an **ablation table** proving which ones paid
- [ ] I can name all three leakage types and give a concrete example of each
- [ ] Every transform I write lives inside a `ColumnTransformer` / `Pipeline`, so `fit` can only ever see training rows
- [ ] When a score jumps suspiciously, my first reaction is to audit for a leak, not to celebrate

### Outcome 3 — Metrics, thresholds, and the cost of errors

- [ ] I can build a confusion matrix by hand and compute precision, recall, specificity and F1 from it
- [ ] I unpack with `tn, fp, fn, tp = confusion_matrix(y, p).ravel()` instead of indexing from memory
- [ ] I can state, in the language of the actual application, what a false positive and a false negative *are* and which costs more
- [ ] I can sweep a threshold, plot the precision/recall trade-off, and pick a threshold by **expected cost arithmetic**
- [ ] I know ROC-AUC's baseline is 0.5 and average precision's baseline is the positive rate
- [ ] I report cross-validated **mean ± std**, not a single lucky number, and I use `StratifiedKFold` on rare classes

### Outcome 4 — Gradient descent, derived and implemented

- [ ] I can compute `σ(z)` by hand and convert a raw score to a probability
- [ ] I can compute log loss for a handful of predictions on a calculator, and I know `ln 2 = 0.6931` on sight
- [ ] I can state `w ← w − lr · ∂L/∂w` and run three iterations on paper without looking it up
- [ ] I can explain why the gradient points uphill and what happens if you add instead of subtract
- [ ] I have implemented logistic regression in NumPy and matched sklearn's weights (with `penalty=None`)
- [ ] I have plotted a loss curve that diverges at too high a learning rate and crawls at too low a one, and I can recognise both shapes instantly

### Outcome 5 — Neural networks from scratch, then in PyTorch

- [ ] I can compute a neuron's output by hand from weights, inputs, bias and activation
- [ ] I can trace a full forward pass through a 2-layer network with real numbers
- [ ] I can derive the backward pass with the chain rule and write it in five lines of NumPy
- [ ] My gradient check agrees with my analytic gradients to better than `1e-6`, and I know what a `0.5` relative error on a bias means
- [ ] I can explain why He initialization exists and what happens if you start at zeros
- [ ] I can write the canonical PyTorch loop — `zero_grad, forward, loss, backward, step` — from a blank file
- [ ] I can build a `Dataset`/`DataLoader`, save a `state_dict`, and write a `predict.py` with `model.eval()` and `torch.no_grad()` in the right places

### Outcome 6 — CNNs on images

- [ ] I can explain why flattening an image into a dense layer throws away structure
- [ ] I can compute `out = floor((n + 2p − k)/s) + 1` on paper for any conv or pool, before running anything
- [ ] I can build and train a CNN in PyTorch and visualize its first-layer filters
- [ ] I keep `train_tf` and `eval_tf` as separate objects and never let augmentation touch an evaluation set
- [ ] I have measured what augmentation bought me and what transfer learning bought me, as separate rows in a results table
- [ ] I read a 10-class confusion matrix and can name the top confusion pair and give a mechanism for it

### Outcome 7 — Unsupervised learning and text

- [ ] I can run two iterations of k-means by hand on a tiny 2-D dataset
- [ ] I always `StandardScaler` before k-means and before PCA, and I can say why
- [ ] I justify `k` with elbow **and** silhouette evidence, and I say so when the elbow doesn't exist
- [ ] I can explain a principal component as a new axis along the biggest spread, and I always print the explained-variance ratio beside a 2-D plot
- [ ] I can tokenize, build a bag-of-words matrix by hand, and compute a TF-IDF weight on a calculator
- [ ] I can compute cosine similarity between two document vectors and interpret the number
- [ ] I can name what bag-of-words loses, demonstrate it with a real example, and say what an embedding is

### The cross-cutting habits

- [ ] I never report a score without a **baseline**, a **spread**, and the **size** of the set it came from
- [ ] I print `.shape` after operations I'm not 100% sure about
- [ ] When something breaks, I change **one** thing at a time and write down what happened
- [ ] I do the arithmetic on paper first and use the code to check *me*, not the other way round
- [ ] I can name at least one subgroup my model works worse for, because I measured it

---

## 🚪 You're Ready for Level 4 When…

Level 4 builds transformers, trains language models, and wires up agents. It will not slow down for a missing Level 3 skill — and the specific thing it assumes is that **you already know how to tell whether a model is working**. Here is the honest gate.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │  THE LEVEL 4 GATE — all seven, or go back                          │
   ├────────────────────────────────────────────────────────────────────┤
   │                                                                    │
   │  1.  You scored 49+ on this assessment (70%), with no single       │
   │      module accounting for 4+ of your wrong answers, and at        │
   │      least 13/26 on Part C.                                        │
   │                                                                    │
   │  2.  You have FINISHED the capstone. Not started — finished:       │
   │      an artifact that loads in a fresh process, a predict.py,      │
   │      a running HTTP service, a log file with latencies in it,      │
   │      a model card with subgroup metrics, and a monitoring plan     │
   │      naming one number.                                            │
   │                                                                    │
   │  3.  You can write the PyTorch training loop from a blank file     │
   │      in under three minutes, from memory, and it runs.             │
   │                                                                    │
   │  4.  You can derive backpropagation for a 2-layer MLP on paper     │
   │      without notes, and say what each of the five lines does.      │
   │                                                                    │
   │  5.  Shown any model score, your first three questions are:        │
   │      what's the baseline, what's the class balance, and was        │
   │      anything fitted before the split.                             │
   │                                                                    │
   │  6.  You can explain a matrix multiply's shapes out loud —         │
   │      (n, d) @ (d, h) -> (n, h) — and predict the output shape      │
   │      of any layer you write before you run it.                     │
   │                                                                    │
   │  7.  You can explain what an embedding is and why cosine           │
   │      similarity is the right way to compare two of them.           │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘
```

### If you're missing one

| Missing | The cheapest fix |
|---|---|
| **Gate 1** (score) | Reread the module your wrong answers cluster in, redo its six practice exercises, re-sit those items. Half a day per module. |
| **Gate 2** (capstone) | There is no shortcut. Level 4 Module 8 fine-tunes and *evaluates* an LLM, and the entire notion of "evaluate" you'll use there is the one the capstone forces you to build. |
| **Gate 3** (the loop) | Ten days of one five-minute drill: blank file, `nn.Sequential`, `DataLoader` over `torch.randn`, train it, print the loss falling. It is a typing-fluency problem, and typing fluency only comes from typing. |
| **Gate 4** (backprop) | Redo [Module 5](module-05-neural-networks-from-scratch.md)'s worked example with **different numbers** you make up, and gradient-check your own answer. If the check passes, you own it. |
| **Gate 5** (the three questions) | Reread [Module 1](module-01-the-supervised-pipeline.md) §4 and [Module 3](module-03-evaluation-metrics.md) §1. Then go and audit a public notebook on the internet and write down the three questions its author didn't ask. |
| **Gate 6** (shapes) | Print `.shape` after every tensor operation for a week. Add `assert x.shape == (n, h)` to your own code. This habit is worth more in Level 4 than in this one — attention is nothing but a shape argument. |
| **Gate 7** (embeddings) | Redo [Module 9](module-09-classic-nlp.md) Part G. Level 4's RAG module is built directly on top of it. |

### What Level 4 does with all of this

```
   YOUR LEVEL 3 SKILL             ─►   WHAT LEVEL 4 TURNS IT INTO
   ────────────────────────────        ────────────────────────────────────
   the PyTorch training loop      ─►   training a small transformer,
                                       same five lines, bigger model
   backprop by hand               ─►   why gradients vanish over long
                                       sequences, and what fixed it
   bag-of-words losing word order ─►   RNNs, then attention: models that
                                       read the sentence in order
   TF-IDF vectors + cosine        ─►   dense embeddings, vector search,
                                       and retrieval-augmented generation
   the confusion matrix           ─►   LLM evaluation: rubrics, judges,
                                       and why "it sounded good" isn't a metric
   threshold tuned to a cost      ─►   deciding when an agent should
                                       refuse, escalate, or ask a human
   the model card                 ─►   system cards, red-teaming, and
                                       documented failure modes at scale
   your saved artifact + service  ─►   an agent that calls tools, with
                                       your logging habits already in place
```

Every arrow points from something you can already do to something you're about to understand. Nothing in Level 4 is magic. You built the floor it stands on.

---

> ### 👉 Next: **[The Level 3 Capstone — Ship It](capstone.md)**
>
> Then: **[Level 4 — Innovator](../level-4-innovator/)**

---

[⬅ Module 9](module-09-classic-nlp.md) · [Level 3 Home](README.md) · [Capstone](capstone.md) · [Glossary](glossary.md) · [Level 4 ➡](../level-4-innovator/)

*A model that cannot beat its baseline is worthless. A score without a baseline is not a score. And a number you cannot reproduce in a fresh process was never a result.*
