# Module 1 — The Supervised Pipeline, End to End

**Level 3 · Module 1 · ~5 hours · Prereqs: Level 2 complete (Python, pandas, a first scikit-learn model), comfort with functions, lists, and dictionaries.**

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 3 Home](README.md) · [Next ➡](module-02-feature-engineering.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to turn a vague real-world question ("are our deliveries bad?") into a supervised learning problem with a defined **X**, a defined **y**, a unit of prediction, and one success metric you commit to before training.
2. You will be able to run a **data audit** that catches ID columns, duplicate rows, missing values, and class imbalance *before* they wreck your model.
3. You will be able to split data three ways — train, validation, test — and state out loud what each split is legally allowed to be used for.
4. You will be able to build a **baseline**, beat it, and explain why a model that cannot beat the baseline should be deleted.
5. You will be able to assemble a scikit-learn `Pipeline`, save it with `joblib`, reload it in a brand-new Python process that contains zero training code, and predict on new rows.
6. You will be able to write a **model card** — a short document that tells the next human what this artifact is, what it was measured on, and where it breaks.

---

## 🪝 The Hook

A pizza chain hires you. The manager says: *"Our deliveries are bad. Can AI fix it?"*

That sentence contains no machine learning problem. It contains a mood.

Here is what actually happened at a real company that skipped this module. A team spent six weeks building a delivery-time model. It scored 94% accuracy. Everyone clapped. Then someone asked what the 6% looked like, and it turned out the model had learned to read a column called `refund_issued` — which is only filled in *after* the delivery is late. The model was 94% accurate at predicting the past. In production it was useless, because at the moment you need the prediction, that column is empty.

Six weeks. One column. The fancy algorithm was never the problem.

This module is the assembly line that makes that mistake structurally hard to commit. Fitting the model is about eight lines of code and it comes near the end. Everything before it is engineering.

---

## 🧠 The Concept

### 1. Problem framing: what is a row, what is the answer, and what counts as winning?

**Supervised learning** — teaching a model by showing it examples where you already know the right answer.

You have seen this in Level 2. What you have probably *not* done is the part that comes before: deciding what a single example even is.

Three questions, always in this order.

**Question 1 — what is the unit of prediction?** One row of your table = one thing you will make one prediction about. This is a decision, not a fact about the data.

For the pizza chain, "our deliveries are bad" could mean:

| Unit of prediction | One row is... | Prediction you'd make |
|---|---|---|
| One order | a single delivery | will *this* order be late? |
| One restaurant-day | Napoli on Tuesday | how many late orders today? |
| One driver-month | Ravi in March | will this driver quit? |
| One customer | a person | will they order again? |

All four are legitimate. All four need completely different tables. Pick one and write it down. We pick **one order**.

**Question 2 — what exactly is y?** The **target** — the column holding the answer you want the model to produce.

"Late" is not a definition. *These* are definitions:

- `late = 1` if actual delivery time > promised delivery time
- `late = 1` if actual delivery time > promised time + 5 minutes (a grace period)
- `late = 1` if the customer complained

They give different datasets and different models. We pick: **`late = 1` if the order arrived after the promised time**, a plain binary 0/1 column.

> **Target (y):** the single column you are trying to predict. Everything else the model is allowed to see is **X**, the features.

**Question 3 — what is the metric, and when do you pick it?** Before training. Always before. If you pick the metric after you see the scores, you will pick the metric that flatters you. That is not evaluation, that is marketing.

🍕 **Analogy.** Framing is deciding the rules of a cricket match *before* the toss. If you decide after the innings that "actually, wides don't count," you have not won a match — you have edited the scoreboard.

🔢 **Tiny concrete example.** Out of 2,000 orders, 576 were late (28.8%). If you predict "never late" for everybody you are right 71.2% of the time. So any metric where 71.2% sounds impressive is a bad metric. We will use **ROC-AUC** as our headline number and report accuracy alongside it, and Module 3 will explain exactly why. For now: AUC of 0.5 means "coin flip," AUC of 1.0 means perfect ranking, and the "never late" strategy scores exactly 0.5.

---

### 2. The data audit: five minutes that save six weeks

Before any model, you interrogate the table. Every audit answers the same five questions.

**(a) Shape and dtypes.** How many rows, how many columns, and is each column the type you expected? A `distance_km` column that arrives as `object` instead of `float64` means somebody typed `"3.4 km"` into a cell somewhere.

**(b) Missing values.** Which columns have `NaN`, and how many? A column that is 60% missing is usually a column to drop, not to impute.

**(c) Duplicate rows.** Exact duplicates are almost always a data-pipeline bug — the same order exported twice. If a duplicated row lands in train *and* in test, your model gets to memorize the answer and then be tested on it. Free marks. Fake marks.

**(d) Class balance.** What fraction of rows are `y = 1`? This single number tells you what your baseline is and warns you if accuracy is going to lie to you.

**(e) Suspicious columns.** Two kinds:

- **ID-like columns.** A column with a unique value in almost every row (`order_id`, `email`, `uuid`). It carries no generalizable signal, but a flexible model will happily memorize it.
- **Too-good columns.** A column that correlates almost perfectly with the target. This is the pizza-chain disaster. Module 2 gives this a name — **data leakage** — and teaches you how to hunt it. In Module 1 your job is only to *notice* and get suspicious.

🍕 **Analogy.** An audit is checking your ingredients before you cook, not after the guests arrive. Two eggs are cracked, the milk smells wrong, and you have somehow got 14 onions. Better to know now.

🔢 **Tiny concrete example.** Our delivery table loads as 2,020 rows. `df.duplicated().sum()` returns **20**. So 20 rows are exact copies. Real dataset size: 2,000. Had we not checked, roughly 4 of those copies would have landed in the test set with their twin in training.

---

### 3. Three-way split: train, validation, test

You already know train/test. Level 3 adds a third box, and the reason is subtle and important.

```
              ALL DATA (2000 rows)
                     |
        +------------+------------+
        |                         |
   80% "temp" (1600)         20% TEST (400)
        |                         |
   +----+-----+                   |
   |          |                   |
 75%        25%                   |
TRAIN (1200) VAL (400)            |
   |          |                   |
   v          v                   v
 fit the   pick between      opened ONCE,
 model     your choices      at the very end
```

> **Train set:** the model learns its parameters here. Fit happens only on train.
> **Validation set:** you look at this repeatedly to choose between options — which features, which model, which threshold. Every look "uses up" a little of it.
> **Test set:** untouched until you are completely finished. You open it exactly once, report the number, and stop.

**Why three?** Because *choosing* is also a form of learning. Suppose you try 40 different feature ideas and keep whichever scores best on your test set. You have now fitted your *decisions* to that test set. Its score is no longer an honest estimate of new data — it is the best of 40 lottery tickets. The validation set exists to absorb that damage, so the test set stays clean.

🍕 **Analogy.** Train = the homework you practise on. Validation = the mock exam you take five times, adjusting your study plan after each. Test = the actual board exam, sealed until exam day. If you take the board exam five times and report your best score, you have not measured your ability. You have measured your persistence.

🔢 **Tiny concrete example.** 2,000 rows. `test_size=0.20` peels off **400** test rows, leaving 1,600. Then `test_size=0.25` on those 1,600 peels off **400** validation rows, leaving **1,200** train. Final split: 1200 / 400 / 400. And because we pass `stratify=y`, the late-rate stays at ~0.287 in all three — not 0.31 in one and 0.24 in another.

⚠️ One more rule: **split before you look**. Not before you `head()` — looking at five rows is fine — but before you compute any statistic you will later use to make a modelling decision. If you compute the median of `driver_experience_months` over the whole table and use it to fill missing values, you have quietly told the training process something about the test rows.

---

### 4. Baselines: the number your model has to beat to exist

A **baseline** is the dumbest possible predictor. It is not a strawman — it is your zero point. A score without a baseline is a number without units.

Three baselines you should know:

| Baseline | What it does | Use when |
|---|---|---|
| **Majority class** | always predicts whichever label is most common | classification |
| **Stratified / random** | guesses randomly, matching the class proportions | classification, sanity check |
| **Predict the mean** | always outputs the average of `y` | regression |

`scikit-learn` gives you all of these in one object:

```python
from sklearn.dummy import DummyClassifier
DummyClassifier(strategy="most_frequent")   # majority class
DummyClassifier(strategy="stratified")      # random, matching proportions
DummyClassifier(strategy="prior")           # majority class for .predict, class rates for .predict_proba
```

For regression there is `DummyRegressor(strategy="mean")`.

🍕 **Analogy.** A weather app that says "no rain" every day in Chennai in January is right about 95% of the time. It is also worth exactly nothing. The baseline is the "no rain" app. Your model has to be better than the app that isn't trying.

🔢 **Tiny concrete example.** On our validation set:

| Baseline | accuracy | ROC-AUC |
|---|---|---|
| most_frequent | 0.7125 | 0.5000 |
| stratified | 0.5850 | 0.4909 |
| prior | 0.7125 | 0.5000 |

Notice the split personality: majority-class gets **71% accuracy** — which sounds respectable if you don't know better — and an AUC of exactly **0.500**, which is the number for "learned nothing." Two metrics, two completely different stories about the same useless model. That is why you fix your metric first.

---

### 5. The Pipeline, the artifact, and the card

Here is the mistake almost everyone makes once:

```python
# THE BAD WAY — do not do this
scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)
model = LogisticRegression().fit(X_train_s, y_train)
# ... two weeks later, in a different file ...
model.predict(new_rows)      # 💥 forgot to scale. Garbage predictions, no error message.
```

Nothing crashes. The model happily consumes unscaled numbers and returns confident nonsense.

> **Pipeline:** a single scikit-learn object that chains preprocessing steps and a model together, so that `fit` fits everything in order and `predict` applies everything in order. One object. Impossible to forget a step.

```python
pipe = Pipeline([
    ("pre",   some_preprocessor),
    ("model", LogisticRegression()),
])
pipe.fit(X_train, y_train)     # fits preprocessor, then model
pipe.predict(new_rows)         # transforms, then predicts. Always.
```

A `Pipeline` also fixes the leakage problem for free: when you call `pipe.fit(X_train, y_train)`, the scaler's mean and standard deviation are computed from **training rows only**. When you later call `pipe.predict(X_val)`, it *transforms* validation rows using the training statistics. It never re-fits. That is exactly the correct behaviour and you get it without thinking about it.

For mixed data — numbers *and* text categories — you need a **ColumnTransformer**:

> **ColumnTransformer:** applies different preprocessing to different columns and glues the results side by side. Numbers get scaled; categories get one-hot encoded; everything comes out as one numeric matrix.

Then you save it:

> **Artifact:** the saved file that *is* your trained model. Weights plus preprocessing plus column order, all in one `.joblib` file. If it isn't saved, you don't have a model — you have a script that had a model once.

```python
import joblib
joblib.dump(pipe, "late_pipeline_v1.joblib")     # save
pipe = joblib.load("late_pipeline_v1.joblib")    # load, in any process
```

And finally you write the card:

> **Model card:** a short markdown document shipped next to the artifact, describing intended use, training data, metrics, and known limitations. It is the label on the medicine bottle.

The card is not paperwork. It is the thing that stops someone six months from now taking your Chennai delivery model, pointing it at Mumbai data, getting bad predictions, and blaming you.

🍕 **Analogy.** The artifact is the packaged frozen pizza. The model card is the box: ingredients, cooking instructions, allergy warnings, best-before date. Shipping a pizza with no box is how people get hurt.

🔢 **Tiny concrete example.** Our saved pipeline is about 4 KB. Loaded in a fresh process with no `sklearn.model_selection` import anywhere, it takes a 3-row DataFrame of raw values (`"CrustyBros"`, `7.4`, `"storm"`, ...) and returns `P(late) = 0.975, 0.017, 0.279`. No scaling code in that file. No encoder. The artifact carries it all.

---

## 🔍 Worked Example

Let's frame, audit, split, baseline, and evaluate **by hand** on a 12-row toy table before touching real code. Numbers small enough to check with a pencil.

**The table.** Twelve deliveries. Columns: `order_id`, `distance_km`, `weather`, `late`.

| order_id | distance_km | weather | late |
|---|---|---|---|
| 1 | 1.0 | clear | 0 |
| 2 | 2.0 | clear | 0 |
| 3 | 8.0 | storm | 1 |
| 4 | 1.5 | clear | 0 |
| 5 | 6.0 | rain  | 1 |
| 6 | 2.5 | clear | 0 |
| 7 | 7.0 | storm | 1 |
| 8 | 3.0 | rain  | 0 |
| 9 | 1.0 | clear | 0 |
| 10 | 2.0 | clear | 0 |
| 11 | 9.0 | storm | 1 |
| 12 | 2.0 | clear | 0 |

**Step 1 — Frame.**
- Unit of prediction: one order.
- y = `late` (binary).
- X = `distance_km`, `weather`. (`order_id` is excluded — see step 2.)
- Metric: accuracy, for this toy. (Real project: AUC.)

**Step 2 — Audit.**
- Shape: 12 rows × 4 columns.
- Missing: none.
- Duplicates: rows 2 and 10 and 12 all read `2.0 / clear / 0` — but they have different `order_id`s, so `df.duplicated()` on the full table finds **0** duplicates. On the feature columns only, it finds 2. Lesson: *duplicate* depends on which columns you check.
- Unique-per-row check: `order_id` has 12 unique values in 12 rows → 12/12 = 1.00 > 0.95 → **ID column, drop it**.
- Class balance: 4 late out of 12 = **0.333**.

**Step 3 — Split.** With 12 rows a three-way split is silly, but let's do it to see the arithmetic. `test_size=0.25` → 3 test rows, 9 remain. `test_size=1/3` on those 9 → 3 validation rows, 6 train rows. Say the split lands like this:

- Train (6): orders 1, 3, 5, 6, 9, 11 → late = 0,1,1,0,0,1 → 3 late out of 6.
- Val (3): orders 2, 7, 8 → late = 0,1,0 → 1 late out of 3.
- Test (3): orders 4, 10, 12 → late = 0,0,0 → 0 late out of 3.

Look at that test set: **zero** positives. With 3 rows, stratification cannot save you. This is the visible, honest reason why tiny datasets give unreliable scores — a lesson Module 3 turns into cross-validation.

**Step 4 — Baseline.** Majority class in *train* is `late = 0` (3 vs 3 — a tie; scikit-learn breaks ties by choosing the smaller label, so `0`). Predict 0 for everything.

- On validation: predictions `0, 0, 0`; truth `0, 1, 0`. Correct on 2 of 3 → accuracy **0.667**.

**Step 5 — A real (tiny) model.** Rule: predict late if `distance_km > 4.0`.

- Val order 2: distance 2.0 → predict 0. Truth 0. ✅
- Val order 7: distance 7.0 → predict 1. Truth 1. ✅
- Val order 8: distance 3.0 → predict 0. Truth 0. ✅

Accuracy **3/3 = 1.000**.

**Step 6 — Compare.** Model 1.000 vs baseline 0.667. Improvement: +0.333. The model beats the baseline, so it earns the right to exist.

**Step 7 — Be honest about it.** Three validation rows. If one had flipped, accuracy drops to 0.667 and the model looks exactly as good as doing nothing. A three-row validation set can only produce four possible scores: 0, 0.333, 0.667, 1.000. You cannot detect a 5% improvement with an instrument whose finest gradation is 33%.

This is the whole discipline of Level 3 in one worked example: get a number, then immediately ask how much you should trust it.

---

## 💻 Hands-On

Three files. Type them, run them in order.

```
project/
├── make_data.py        # generates the table (stands in for a real database export)
├── train_pipeline.py   # audit → split → baseline → fit → evaluate → save → card
└── predict.py          # loads the artifact and predicts. NO training code.
```

Install what you need:

```bash
pip install "numpy>=1.26" "pandas>=2.0" "scikit-learn>=1.4" joblib matplotlib
```

### File 1 — `make_data.py`

This stands in for "SELECT * FROM orders". Everything is generated from a fixed seed so your numbers match the ones printed below exactly.

```python
"""Generates the 'was this pizza delivery late?' table used in Modules 1-3."""
import numpy as np
import pandas as pd

RESTAURANTS = ["Napoli", "SliceHouse", "CrustyBros", "TandooriPizza", "GreenLeaf"]
WEATHER = ["clear", "rain", "storm"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def make_deliveries(n=2000, seed=0, add_leak=False):
    rng = np.random.default_rng(seed)

    distance_km = np.round(rng.gamma(shape=2.0, scale=1.6, size=n) + 0.3, 2)
    items = rng.integers(1, 7, size=n)
    prep_minutes = np.round(rng.normal(14, 4, size=n).clip(4, 40), 1)
    hour = rng.choice(np.arange(10, 24), size=n,
                      p=np.array([2, 3, 6, 8, 5, 3, 3, 4, 7, 9, 8, 5, 3, 2]) / 68)
    day = rng.choice(DAYS, size=n)
    restaurant = rng.choice(RESTAURANTS, size=n, p=[.28, .24, .20, .16, .12])
    weather = rng.choice(WEATHER, size=n, p=[.70, .24, .06])
    driver_exp = rng.integers(0, 60, size=n).astype(float)

    # The hidden "truth" the model will have to rediscover from data alone.
    rest_effect = pd.Series(restaurant).map(
        {"Napoli": -0.3, "SliceHouse": 0.0, "CrustyBros": 0.6,
         "TandooriPizza": 0.2, "GreenLeaf": -0.1}).to_numpy()
    weather_effect = pd.Series(weather).map(
        {"clear": 0.0, "rain": 0.8, "storm": 1.7}).to_numpy()
    rush = ((hour >= 18) & (hour <= 20)).astype(float)

    score = (-3.9
             + 0.42 * distance_km
             + 0.16 * items
             + 0.055 * prep_minutes
             + 0.9 * rush
             + rest_effect
             + weather_effect
             - 0.022 * driver_exp
             + rng.normal(0, 0.35, size=n))
    p_late = 1 / (1 + np.exp(-score))          # squash score into a probability
    late = (rng.random(n) < p_late).astype(int)

    df = pd.DataFrame({
        "order_id": np.arange(100000, 100000 + n),
        "restaurant": restaurant,
        "distance_km": distance_km,
        "items": items,
        "prep_minutes": prep_minutes,
        "order_hour": hour,
        "day_of_week": day,
        "weather": weather,
        "driver_experience_months": driver_exp,
        "late": late,
    })

    if add_leak:
        # A poisoned column, used in Module 2. Ignore it for now.
        called = np.where(df["late"] == 1, rng.random(n) < 0.85, rng.random(n) < 0.03)
        df["customer_called_support"] = called.astype(int)

    # Realistic mess: ~6% missing driver experience, ~1% duplicated rows.
    miss = rng.random(n) < 0.06
    df.loc[miss, "driver_experience_months"] = np.nan
    dup_idx = rng.choice(n, size=max(1, n // 100), replace=False)
    df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)

    return df.sample(frac=1.0, random_state=seed).reset_index(drop=True)


if __name__ == "__main__":
    d = make_deliveries()
    print(d.shape)
    print(d.head().to_string(index=False))
```

Run it:

```bash
python make_data.py
```

```
(2020, 10)
 order_id restaurant  distance_km  items  prep_minutes  order_hour day_of_week weather  driver_experience_months  late
   100955     Napoli         2.78      3          15.0          12         Mon   clear                       5.0     0
   101493 CrustyBros         3.09      5          12.9          22         Mon    rain                       0.0     0
   101857 CrustyBros         2.65      2          14.2          16         Mon    rain                      33.0     0
   100215     Napoli         9.60      2           4.9          13         Tue   clear                      27.0     1
   100506 CrustyBros         2.33      5          19.6          20         Thu   clear                      35.0     0
```

2,020 rows for a 2,000-row dataset — the duplicates are already visible in the shape.

### File 2 — `train_pipeline.py`

```python
"""Raw table -> audit -> split -> baseline -> Pipeline -> metrics -> artifact -> card."""
from datetime import date

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

RANDOM_STATE = 42
TARGET = "late"


def rule(title):
    print("\n" + "=" * 62)
    print(title)
    print("=" * 62)


# ---------------------------------------------------------------- 1. LOAD
df = make_deliveries(n=2000, seed=0)

# ---------------------------------------------------------------- 2. AUDIT
rule("DATA AUDIT")
print("shape:", df.shape)
print("\ndtypes:\n" + df.dtypes.to_string())
print("\nmissing per column:\n" + df.isna().sum().to_string())
print("\nexact duplicate rows:", int(df.duplicated().sum()))
print("\nclass balance:\n" + df[TARGET].value_counts(normalize=True).round(4).to_string())

for col in df.columns:
    if df[col].nunique() / len(df) > 0.95:            # near-unique => ID-like
        print(f"\n!! '{col}' is unique in >95% of rows -> looks like an ID. Drop it.")

df = df.drop_duplicates().reset_index(drop=True)
print("\nshape after dropping exact duplicates:", df.shape)

# ---------------------------------------------------------------- 3. SPLIT
y = df[TARGET]
X = df.drop(columns=[TARGET, "order_id"])             # never feed the model an ID

X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=RANDOM_STATE, stratify=y_temp)

rule("THREE-WAY SPLIT")
print(f"train {X_train.shape[0]}   val {X_val.shape[0]}   test {X_test.shape[0]}")
print("late rate  ->  train %.3f   val %.3f   test %.3f"
      % (y_train.mean(), y_val.mean(), y_test.mean()))
print("TEST SET IS NOW SEALED. Not opened again in this script.")

# ---------------------------------------------------------------- 4. BASELINES
rule("BASELINES (validation set)")
for strategy in ["most_frequent", "stratified", "prior"]:
    dummy = DummyClassifier(strategy=strategy, random_state=RANDOM_STATE)
    dummy.fit(X_train, y_train)
    acc = accuracy_score(y_val, dummy.predict(X_val))
    auc = roc_auc_score(y_val, dummy.predict_proba(X_val)[:, 1])
    print(f"{strategy:>14s}   accuracy={acc:.4f}   roc_auc={auc:.4f}")

baseline_acc = accuracy_score(
    y_val, DummyClassifier(strategy="most_frequent").fit(X_train, y_train).predict(X_val))

# ---------------------------------------------------------------- 5. PIPELINE
NUM_COLS = ["distance_km", "items", "prep_minutes",
            "order_hour", "driver_experience_months"]
CAT_COLS = ["restaurant", "day_of_week", "weather"]

numeric_branch = Pipeline([
    ("impute", SimpleImputer(strategy="median")),     # median learned from TRAIN only
    ("scale", StandardScaler()),
])

preprocess = ColumnTransformer([
    ("num", numeric_branch, NUM_COLS),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_COLS),
])

pipe = Pipeline([
    ("pre", preprocess),
    ("model", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
])
pipe.fit(X_train, y_train)

# ---------------------------------------------------------------- 6. EVALUATE
val_prob = pipe.predict_proba(X_val)[:, 1]
val_pred = pipe.predict(X_val)
val_acc = accuracy_score(y_val, val_pred)
val_auc = roc_auc_score(y_val, val_prob)

rule("PIPELINE v1 (validation set)")
print(f"accuracy = {val_acc:.4f}     (baseline {baseline_acc:.4f},"
      f" lift {val_acc - baseline_acc:+.4f})")
print(f"roc_auc  = {val_auc:.4f}     (baseline 0.5000,"
      f" lift {val_auc - 0.5:+.4f})")

feature_names = pipe.named_steps["pre"].get_feature_names_out()
coefs = pd.Series(pipe.named_steps["model"].coef_[0], index=feature_names)
print("\ntop 8 coefficients by magnitude:")
print(coefs.reindex(coefs.abs().sort_values(ascending=False).index).head(8).round(3).to_string())

# ---------------------------------------------------------------- 7. SAVE
joblib.dump(pipe, "late_pipeline_v1.joblib")
print("\nsaved -> late_pipeline_v1.joblib")

# ---------------------------------------------------------------- 8. MODEL CARD
card = f"""# Model Card — Late Delivery Predictor v1

**Version:** 1.0  **Date:** {date.today().isoformat()}  **Artifact:** `late_pipeline_v1.joblib`

## Intended use
Predicts the probability that a single pizza order will arrive after its promised
time, at the moment the order is placed. Intended for dispatch triage: flag risky
orders so a human can call the customer early.

## Out-of-scope use
- Not for driver performance reviews or pay decisions.
- Not valid for a different city, a different chain, or a different promise policy.
- Not a delivery-time estimate. It outputs a probability, not minutes.

## Unit of prediction
One order.

## Training data
{len(df)} de-duplicated synthetic orders. Features available at order time only:
{', '.join(NUM_COLS + CAT_COLS)}. `order_id` dropped as an identifier.
Missing `driver_experience_months` (~6% of rows) imputed with the TRAIN median.

## Splits
train {len(X_train)} / validation {len(X_val)} / test {len(X_test)}, stratified on the target.
Test set not opened during development of v1.

## Metrics (validation set)
| metric | model | baseline (most_frequent) |
|---|---|---|
| accuracy | {val_acc:.4f} | {baseline_acc:.4f} |
| ROC-AUC | {val_auc:.4f} | 0.5000 |

## Known limitations
- Trained on synthetic data; real traffic, strikes, and festivals are absent.
- One-hot encoding uses `handle_unknown="ignore"`: a brand-new restaurant becomes an
  all-zero vector and the model falls back on the numeric features only.
- No calibration check has been done — *calibration* means asking whether a
  predicted 0.7 really comes true about 70% of the time (Module 3 measures it) —
  so the probabilities may be over- or under-confident even when the ranking is good.
- Class balance is ~29% positive. Accuracy alone is a misleading headline here.

## Contact
Owner: you. Retrain trigger: monthly, or whenever the promise policy changes.
"""
with open("model_card.md", "w") as fh:
    fh.write(card)
print("wrote -> model_card.md")
```

Run it:

```bash
python train_pipeline.py
```

Expected output (abridged, but the numbers are exact):

```
==============================================================
DATA AUDIT
==============================================================
shape: (2020, 10)

missing per column:
order_id                      0
restaurant                    0
distance_km                   0
items                         0
prep_minutes                  0
order_hour                    0
day_of_week                   0
weather                       0
driver_experience_months    108
late                          0

exact duplicate rows: 20

class balance:
0    0.7119
1    0.2881

!! 'order_id' is unique in >95% of rows -> looks like an ID. Drop it.

shape after dropping exact duplicates: (2000, 10)

==============================================================
THREE-WAY SPLIT
==============================================================
train 1200   val 400   test 400
late rate  ->  train 0.287   val 0.287   test 0.287
TEST SET IS NOW SEALED. Not opened again in this script.

==============================================================
BASELINES (validation set)
==============================================================
 most_frequent   accuracy=0.7125   roc_auc=0.5000
    stratified   accuracy=0.5850   roc_auc=0.4909
         prior   accuracy=0.7125   roc_auc=0.5000

==============================================================
PIPELINE v1 (validation set)
==============================================================
accuracy = 0.7600     (baseline 0.7125, lift +0.0475)
roc_auc  = 0.7752     (baseline 0.5000, lift +0.2752)

top 8 coefficients by magnitude:
num__distance_km                 0.925
cat__weather_storm               0.742
cat__weather_clear              -0.650
cat__restaurant_CrustyBros       0.616
cat__day_of_week_Mon             0.470
cat__restaurant_Napoli          -0.458
num__driver_experience_months   -0.387
num__items                       0.297

saved -> late_pipeline_v1.joblib
wrote -> model_card.md
```

Read those coefficients. Longer distance → more late (+0.925). Storm → more late (+0.742). Clear → less late (−0.650). Experienced drivers → less late (−0.387). The model rediscovered the physics of pizza delivery from 1,200 rows, and it agrees with common sense. That agreement is itself a test: a model whose signs are backwards is telling you something is wrong with your data.

Also note the honest headline: accuracy went from 0.7125 to 0.7600. That is a **4.75 point** gain, not a miracle. The AUC gain from 0.500 to 0.775 is the more impressive number, and it is the one we committed to up front.

### File 3 — `predict.py`

The whole point of the artifact. Notice what is *not* imported: no `train_test_split`, no `DummyClassifier`, no `make_data`.

```python
"""Loads the saved artifact and scores new orders. Contains no training code."""
import joblib
import pandas as pd

pipe = joblib.load("late_pipeline_v1.joblib")

new_orders = pd.DataFrame([
    {"restaurant": "CrustyBros", "distance_km": 7.4, "items": 5, "prep_minutes": 22.0,
     "order_hour": 19, "day_of_week": "Fri", "weather": "storm",
     "driver_experience_months": 2.0},
    {"restaurant": "Napoli", "distance_km": 1.1, "items": 1, "prep_minutes": 9.5,
     "order_hour": 14, "day_of_week": "Tue", "weather": "clear",
     "driver_experience_months": 48.0},
    {"restaurant": "GreenLeaf", "distance_km": 3.2, "items": 3, "prep_minutes": 16.0,
     "order_hour": 20, "day_of_week": "Sat", "weather": "rain",
     "driver_experience_months": None},          # missing on purpose: imputer handles it
])

proba = pipe.predict_proba(new_orders)[:, 1]
for i, p in enumerate(proba):
    verdict = "LATE" if p >= 0.5 else "on time"
    print(f"order {i}:  P(late) = {p:.3f}   ->  {verdict}")
```

```bash
python predict.py
```

```
order 0:  P(late) = 0.975   ->  LATE
order 1:  P(late) = 0.017   ->  on time
order 2:  P(late) = 0.279   ->  on time
```

Order 0: long distance, storm, rush hour, rookie driver, the slow restaurant. 97.5%. Order 1: short, clear, quiet afternoon, veteran driver, the fast restaurant. 1.7%. Order 2 sits in the middle at 27.9% — and its `driver_experience_months` was `None`, silently filled with the training median by the imputer inside the artifact.

That is a shipped model. Three files, one artifact, one card.

---

## ✍️ Practice

### [Warm-up] 1 — Frame three questions
For each vague request below, write down: the unit of prediction, the exact definition of `y`, three features that would be available *at prediction time*, one feature that would **not** be available at prediction time, and the metric you'd commit to.

(a) "Can we tell which students need help?"
(b) "Which YouTube videos should we recommend?"
(c) "Is this text message spam?"

**Done looks like:** a table with 5 filled cells per request, and your "not available at prediction time" column contains something genuinely tempting.

### [Warm-up] 2 — Audit by hand
Load the delivery table and answer, with the code you used:
(a) How many rows have `distance_km > 10`?
(b) What is the late rate for `weather == "storm"` versus `weather == "clear"`?
(c) Which restaurant has the highest late rate, and how many orders does it have?
(d) After `drop_duplicates()`, is any column still unique in more than 95% of rows?

**Done looks like:** four numbers, each with the one-line pandas expression that produced it.

### [Build] 3 — Break the split on purpose
Modify `train_pipeline.py` to remove `stratify=y` from **both** splits and change `random_state` to `7`. Print the late rate in train, val, and test. Then loop `random_state` over `0..29` without stratification and record the widest gap between the highest and lowest late rate across the three splits. Repeat with stratification on.

**Done looks like:** two numbers (max gap without stratify, max gap with stratify) and one sentence saying which you would ship and why.

### [Build] 4 — A better baseline
`DummyClassifier` is deliberately dumb. Write a **rule-based baseline**: predict late if `distance_km > 5.0` OR `weather == "storm"`. Score it on validation (accuracy and AUC — for AUC, use the rule's 0/1 output as the score). Compare against both the dummy and the fitted pipeline.

**Done looks like:** a three-row comparison table, plus one sentence on whether the trained model earns its complexity over a rule a manager could apply in their head.

### [Stretch] 5 — Regression version
Change the problem: instead of predicting *whether* an order is late, predict *how many minutes* it takes. Add a `delivery_minutes` column to `make_data.py` computed as `8 + 3.1*distance_km + 0.7*prep_minutes + 6*rush + noise` (use `rng.normal(0, 4, n)` for the noise), and build a regression pipeline with `Ridge`. Baseline with `DummyRegressor(strategy="mean")`. Report MAE and R² for both.

**Done looks like:** a table of MAE and R² for baseline vs model, and one sentence explaining what an MAE of *X* minutes means to the pizza manager in plain language.

### [Stretch] 6 — Artifact integrity test
Write `test_artifact.py` that: (1) loads `late_pipeline_v1.joblib`; (2) asserts it is a `Pipeline` with exactly the step names `["pre", "model"]`; (3) asserts predicting on a DataFrame with the columns in a *shuffled order* gives the same answer as the original order; (4) asserts that predicting on a DataFrame that is missing a required column raises an error rather than returning silently wrong numbers. Print `ALL CHECKS PASSED`.

**Done looks like:** a script that exits cleanly, plus a note on which of those four checks you think is most likely to catch a real production bug.

---

## 🤔 Think Deeper

**1. Who decides what "late" means?**
Suppose the chain redefines the promise from 30 minutes to 45 minutes. Overnight, your `late` rate collapses and your model's accuracy "improves." Nothing about deliveries changed — only a definition.
*How to reason about it:* Ask who benefits from each definition. Trace what happens to the model's outputs, to driver bonuses, and to the customer, under each. Then ask: should the target definition live in your code, or in a config file that the business owns and versions?

**2. Is it fair to use `driver_experience_months` as a feature?**
It predicts lateness well (coefficient −0.387). But if dispatch starts routing easy orders to experienced drivers because the model says rookies are risky, rookies never gain experience, and the model's prediction becomes true because the model made it true.
*How to reason about it:* Look for the feedback loop. Draw the arrow from prediction → action → future data → next model. Ask which features are things the person *is* versus things the person *did*, and which of those the person can change.

**3. What does the test set protect you from, really?**
You are allowed to open the test set once. But nothing physically stops you from opening it, feeling disappointed, tweaking, and opening it again. No error is raised. No log is written.
*How to reason about it:* Think about what makes a rule enforceable versus merely stated. What would a team have to build — file permissions, a held-out server, a submission system like a Kaggle leaderboard — to make "once" actually mean once? What is the cost of that machinery, and at what team size does it become worth paying?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Feeding `order_id` (or any ID) to the model | It's a column in the table and you did `X = df.drop(columns=["late"])` without thinking | Audit for near-unique columns; explicitly list the features you *want* rather than dropping the ones you don't |
| Fitting the scaler on all data, then splitting | Scaling feels like "cleaning," which feels like it happens before modelling | Split first. Put every transform inside a `Pipeline` so `fit` only ever sees train |
| Reporting accuracy on an imbalanced target | Accuracy is the default and 71% sounds fine | State the majority-class rate in the same breath; use AUC or the Module 3 metrics |
| Checking the test set "just to see" | Curiosity, plus no error message when you do it | Load the test set only in a separate final script; keep it out of your training file entirely |
| No baseline at all | The model produced a number, and the number was above 0.5, so it must be working | `DummyClassifier` is three lines. Run it every single time, first |
| Saving only the model, not the pipeline | `joblib.dump(model, ...)` looks complete | Always dump the whole `Pipeline` object so preprocessing travels with the weights |
| Forgetting `handle_unknown="ignore"` in `OneHotEncoder` | Works fine in training, crashes in production on a new category | Set it explicitly and write the fallback behaviour into the model card |
| `drop_duplicates()` after splitting | You found the duplicates late | De-duplicate immediately after loading, before any split |

---

## 🛠️ Mini-Project — Pipeline v1

**Goal.** Produce a complete, shippable supervised-learning deliverable: one training script that goes raw table → audit → three-way split → baseline → fitted Pipeline → validation metrics → saved `.joblib` → generated `model_card.md`, and one inference script that loads the artifact in a clean process and predicts on new rows.

**Time:** 60–90 minutes if you type the Hands-On code; longer if you extend it.

### Starter steps

1. Create a folder `pipeline_v1/` and put `make_data.py` in it.
2. Write `train_pipeline.py` section by section. After each section, run the script and read the output before writing the next one. Do not write all 150 lines then hit run.
3. **Audit first.** Do not write a single modelling line until your audit prints shape, dtypes, missing counts, duplicate count, class balance, and an ID warning.
4. **Split second.** Print the three sizes and the three class rates. Print the sentence `TEST SET IS NOW SEALED.` and mean it.
5. **Baseline third.** All three dummy strategies. Write the majority-class accuracy on a sticky note.
6. **Then** the `ColumnTransformer` + `LogisticRegression` pipeline. Fit on train. Evaluate on validation only.
7. Dump the artifact. Generate the model card with an f-string so the metrics in the card can never drift from the metrics in the run.
8. Open a **new terminal**, `cd` into the folder, and run `predict.py`. If it works, you have shipped something.

### Success criteria checklist

- [ ] `train_pipeline.py` prints an audit block before anything else runs.
- [ ] The audit explicitly flags `order_id` as ID-like and the script drops it.
- [ ] Duplicates are removed and the before/after shapes are printed.
- [ ] Three splits are printed with sizes **1200 / 400 / 400** and late rates within 0.005 of each other.
- [ ] At least two baselines are scored on validation.
- [ ] The fitted pipeline beats the majority-class baseline on your chosen metric, and the lift is printed as a signed number.
- [ ] `late_pipeline_v1.joblib` exists on disk.
- [ ] `model_card.md` exists and its metric numbers were generated by the script, not typed by you.
- [ ] `predict.py` contains **no** import from `sklearn.model_selection`, no `.fit(` call, and no import of `make_data`.
- [ ] `predict.py` runs in a fresh terminal and prints three probabilities.
- [ ] The word `y_test` appears **zero times** in `train_pipeline.py` after the split line.

### Level it up

Add a `--version` flag to `train_pipeline.py` using `argparse`, so running `python train_pipeline.py --version 2` writes `late_pipeline_v2.joblib` and `model_card_v2.md`, and appends one row to a `runs.csv` log containing: timestamp, version, train/val/test sizes, baseline accuracy, model accuracy, model AUC, and the git commit hash if you're in a repo (`subprocess.run(["git","rev-parse","--short","HEAD"], capture_output=True, text=True).stdout.strip()`). You now have experiment tracking, which is a thing companies pay money for.

---

## 🔑 Key Takeaways

- **Framing is the job.** Unit of prediction, exact target definition, and the metric — decided and written down *before* any model is fitted. A vague request is not a problem statement.
- **Audit before you model.** Shape, dtypes, missing, duplicates, class balance, suspicious columns. Five minutes here has saved entire projects.
- **Three splits, three jobs.** Train fits, validation chooses, test judges once. Choosing is a kind of fitting, which is why validation exists.
- **A score without a baseline is not a result.** 76% accuracy means nothing until you know the dumb answer scores 71%.
- **Ship the `Pipeline`, not the model.** Preprocessing that lives outside the artifact will eventually be forgotten, and it will fail silently.
- **The model card is part of the deliverable.** Intended use, data, metrics, limitations. Generate the numbers programmatically so they can never go stale.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Supervised learning** | Learning from examples where you already know the right answer | 2,000 past orders, each labelled late or on time |
| **Target (y)** | The one column you're trying to predict | `late` (0 or 1) |
| **Features (X)** | Everything the model is allowed to look at | distance, weather, restaurant, hour |
| **Unit of prediction** | What one row of your table stands for | one pizza order |
| **Data audit** | Checking the table for problems before you model | "20 duplicate rows, 108 missing values" |
| **ID column** | A column with a different value in nearly every row | `order_id` — carries no real signal |
| **Class balance** | The fraction of rows in each class | 28.8% late, 71.2% on time |
| **Train / validation / test** | Practice set / mock exam / final exam | 1200 / 400 / 400 rows |
| **Stratified split** | A split that keeps the class proportions equal in every part | 28.7% late in all three splits |
| **Baseline** | The dumbest possible predictor, used as a zero point | "always say on time" → 71.25% accurate |
| **DummyClassifier** | scikit-learn's built-in baseline maker | `DummyClassifier(strategy="most_frequent")` |
| **Pipeline** | One object that chains preprocessing and a model together | scale → one-hot → logistic regression |
| **ColumnTransformer** | Applies different preprocessing to different columns | scale the numbers, one-hot the categories |
| **Imputation** | Filling in missing values with a sensible guess | missing driver experience → train median, 29 |
| **Artifact** | The saved file that *is* your trained model | `late_pipeline_v1.joblib` |
| **joblib** | The library that saves and loads scikit-learn objects | `joblib.dump(pipe, "m.joblib")` |
| **Model card** | The label on the bottle: use, data, metrics, limits | `model_card.md` |
| **ROC-AUC** | How well the model *ranks* positives above negatives; 0.5 = coin flip | 0.7752 |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Frame three questions

**(a) "Can we tell which students need help?"**

| Field | Answer |
|---|---|
| Unit of prediction | one student, per term |
| y | `needs_help = 1` if the student's end-of-term grade is below 40% |
| Features available at prediction time (start of term) | attendance % from last term, last term's grade, number of homework submissions in weeks 1–3 |
| **Not** available at prediction time | this term's final exam score — it *is* the answer |
| Metric | recall (you would rather offer help to a student who didn't need it than miss one who did) |

Note the trap: "number of times the student came to tutoring this term" sounds like a great feature, but if tutoring is assigned *because* a teacher already noticed the student struggling, you are predicting the teacher, not the student.

**(b) "Which YouTube videos should we recommend?"**

| Field | Answer |
|---|---|
| Unit of prediction | one (user, video) pair |
| y | `clicked = 1` if the user clicked this video within 24 hours of it being shown |
| Features at prediction time | video length, video topic tag, the user's watch-time in that topic last month, hour of day |
| **Not** available | total watch time on this video by this user — that only exists after the click |
| Metric | precision at 10 (of the top 10 videos we show, how many get clicked) |

**(c) "Is this text message spam?"**

| Field | Answer |
|---|---|
| Unit of prediction | one message |
| y | `spam = 1` if the user reported it as spam or the carrier blocklist flagged the sender |
| Features at prediction time | message length, count of digits, count of URLs, whether the sender is in contacts |
| **Not** available | "user deleted without reading" — that happens after delivery |
| Metric | precision (a false positive means a real message from your bank vanishes — very expensive) |

### 2 — Audit by hand

```python
import pandas as pd
from make_data import make_deliveries

df = make_deliveries(n=2000, seed=0)

# (a) long deliveries
print("distance > 10 km:", int((df["distance_km"] > 10).sum()))

# (b) late rate by weather
print(df.groupby("weather")["late"].agg(["mean", "size"]).round(4))

# (c) worst restaurant
by_rest = df.groupby("restaurant")["late"].agg(["mean", "size"]).sort_values("mean", ascending=False)
print(by_rest.round(4))

# (d) ID check after de-duplication
dd = df.drop_duplicates()
for c in dd.columns:
    ratio = dd[c].nunique() / len(dd)
    if ratio > 0.95:
        print(f"{c}: {ratio:.3f} unique -> ID-like")
```

Expected shape of the answers:

- (a) A small count — long deliveries are rare because `distance_km` comes from a gamma distribution with mean ≈ 3.5.
- (b) Storm has a much higher late rate than clear. This is the `weather_effect` of +1.7 versus 0.0 showing through, and it is why `weather` earned a big coefficient.
- (c) `CrustyBros` — it was built with `rest_effect = +0.6`, the worst of the five. It has ~390 orders, which is enough to trust the estimate. If the worst restaurant had only 12 orders you should not trust the ranking.
- (d) Only `order_id`. After de-duplication it is 2000/2000 = 1.000 unique.

The point of (c) is the second half of the question. A rate without a sample size is not evidence.

### 3 — Break the split on purpose

```python
import numpy as np
from sklearn.model_selection import train_test_split
from make_data import make_deliveries

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])


def gap(seed, stratify):
    s1 = y if stratify else None
    X_tmp, X_te, y_tmp, y_te = train_test_split(
        X, y, test_size=0.20, random_state=seed, stratify=s1)
    s2 = y_tmp if stratify else None
    X_tr, X_va, y_tr, y_va = train_test_split(
        X_tmp, y_tmp, test_size=0.25, random_state=seed, stratify=s2)
    rates = [y_tr.mean(), y_va.mean(), y_te.mean()]
    return max(rates) - min(rates)


for stratify in [False, True]:
    gaps = [gap(s, stratify) for s in range(30)]
    label = "WITH stratify" if stratify else "WITHOUT stratify"
    print(f"{label:>16s}: max gap {max(gaps):.4f}   mean gap {np.mean(gaps):.4f}")
```

Typical result: without stratification the worst gap across 30 seeds is roughly **0.05–0.07** (so one split might be 25% late while another is 32%); with stratification the gap is around **0.002–0.005**, which is just integer rounding — you cannot put 0.287 × 400 = 114.8 rows in a set.

**Which would you ship?** Stratified, always, for classification. Not because it makes your score higher — it doesn't reliably — but because it removes a source of noise you gain nothing from. If your validation score moves 2 points when you change `random_state`, you cannot tell whether a 1-point feature improvement is real. Stratification makes the measuring instrument steadier.

### 4 — A better baseline

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from make_data import make_deliveries

RS = 42
df = make_deliveries(2000, 0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=.2, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

rows = []

# 1. dummy
d = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
rows.append(("dummy: always on-time",
             accuracy_score(y_va, d.predict(X_va)),
             roc_auc_score(y_va, d.predict_proba(X_va)[:, 1])))

# 2. hand rule
rule_pred = ((X_va["distance_km"] > 5.0) | (X_va["weather"] == "storm")).astype(int)
rows.append(("rule: dist>5 OR storm",
             accuracy_score(y_va, rule_pred),
             roc_auc_score(y_va, rule_pred)))

# 3. fitted pipeline
NUM = ["distance_km", "items", "prep_minutes", "order_hour", "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]
pipe = Pipeline([
    ("pre", ColumnTransformer([
        ("num", Pipeline([("i", SimpleImputer(strategy="median")),
                          ("s", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])),
    ("m", LogisticRegression(max_iter=1000, random_state=RS)),
]).fit(X_tr, y_tr)
prob = pipe.predict_proba(X_va)[:, 1]
rows.append(("logistic pipeline",
             accuracy_score(y_va, (prob >= .5).astype(int)),
             roc_auc_score(y_va, prob)))

print(pd.DataFrame(rows, columns=["approach", "accuracy", "roc_auc"]).round(4).to_string(index=False))
```

You will find the hand rule scores clearly above the dummy on AUC (it captures real signal — distance and storm are the two biggest true effects) but its accuracy may land close to, or even below, the dummy's 0.7125, because the rule flags a lot of orders that turn out fine.

**Does the model earn its complexity?** Yes, on AUC: ~0.775 versus roughly 0.62–0.66 for the rule. The rule is a hard 0/1 with no notion of *how* risky an order is, so it cannot rank, cannot be threshold-tuned, and cannot combine four weak signals. But it is worth saying out loud: if the rule had scored 0.77, you should ship the rule. It needs no artifact, no retraining, and no model card. The correct answer to "should we use ML here?" is sometimes no.

### 5 — Regression version

Add to `make_deliveries`, just before the `df = pd.DataFrame(...)` line:

```python
    delivery_minutes = np.round(
        8 + 3.1 * distance_km + 0.7 * prep_minutes + 6 * rush + rng.normal(0, 4, size=n), 1
    ).clip(5, None)
```

and add `"delivery_minutes": delivery_minutes,` to the DataFrame dict.

```python
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

y = df["delivery_minutes"]
X = df.drop(columns=["delivery_minutes", "late", "order_id"])   # drop 'late': it leaks!
X_tmp, X_te, y_tmp, y_te = train_test_split(X, y, test_size=.2, random_state=42)
X_tr, X_va, y_tr, y_va = train_test_split(X_tmp, y_tmp, test_size=.25, random_state=42)

pre = ColumnTransformer([
    ("num", Pipeline([("i", SimpleImputer(strategy="median")), ("s", StandardScaler())]), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])

results = []
for name, est in [("baseline: predict the mean", DummyRegressor(strategy="mean")),
                  ("ridge pipeline", Ridge(alpha=1.0))]:
    m = Pipeline([("pre", pre), ("m", est)]).fit(X_tr, y_tr)
    p = m.predict(X_va)
    results.append((name, mean_absolute_error(y_va, p), r2_score(y_va, p)))

print(pd.DataFrame(results, columns=["model", "MAE (min)", "R2"]).round(3).to_string(index=False))
```

Expect the mean baseline to have MAE around 6–8 minutes and R² of approximately 0.0 (R² of the mean predictor is 0 by definition on the data it was fit on, and slightly negative on held-out data). Ridge should land near MAE ≈ 3.2 minutes and R² ≈ 0.8, because `delivery_minutes` was built as an almost-linear function of the features plus noise with standard deviation 4.

**Note the trap in the code above:** `late` must be dropped from X. `late` is derived from the same underlying process and is only known after delivery. Leaving it in is leakage — the exact bug from The Hook. Module 2 formalises this.

**Plain-language MAE.** "On average our estimate is off by about 3.2 minutes in either direction." That is a sentence a pizza manager can act on: if you promise a 30-minute window you are fine; if you promise a 3-minute arrival window you are not.

### 6 — Artifact integrity test

```python
"""test_artifact.py — checks the saved model behaves like a shippable artifact."""
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

pipe = joblib.load("late_pipeline_v1.joblib")

# Check 1: it is a Pipeline with the expected steps
assert isinstance(pipe, Pipeline), "artifact is not a Pipeline"
assert [name for name, _ in pipe.steps] == ["pre", "model"], \
    f"unexpected steps: {[n for n, _ in pipe.steps]}"
print("check 1 OK: Pipeline with steps ['pre', 'model']")

row = {"restaurant": "Napoli", "distance_km": 4.0, "items": 3, "prep_minutes": 15.0,
       "order_hour": 19, "day_of_week": "Fri", "weather": "rain",
       "driver_experience_months": 12.0}

# Check 2: column order must not matter (ColumnTransformer selects by NAME)
a = pd.DataFrame([row])
b = a[list(reversed(a.columns))]
pa = pipe.predict_proba(a)[0, 1]
pb = pipe.predict_proba(b)[0, 1]
assert abs(pa - pb) < 1e-12, f"column order changed the prediction: {pa} vs {pb}"
print(f"check 2 OK: shuffled column order gives identical P(late) = {pa:.6f}")

# Check 3: a missing required column must raise, not silently mispredict
missing = a.drop(columns=["weather"])
try:
    pipe.predict(missing)
except (KeyError, ValueError) as exc:
    print(f"check 3 OK: missing column raised {type(exc).__name__}")
else:
    raise AssertionError("missing column did NOT raise — artifact is unsafe")

# Check 4: an unseen category must not crash (handle_unknown='ignore')
unseen = a.copy()
unseen.loc[0, "restaurant"] = "BrandNewPizzaCo"
p_unseen = pipe.predict_proba(unseen)[0, 1]
print(f"check 4 OK: unseen restaurant handled, P(late) = {p_unseen:.6f}")

print("ALL CHECKS PASSED")
```

**Which check catches the most real bugs?** Check 3. Check 2 passes because `ColumnTransformer` selects columns by name, so it is really a *documentation* test — it proves a property you were relying on. Check 3 tests the failure mode that actually costs money: an upstream system quietly stops sending a field, and you want a loud crash and a page at 3 a.m., not six months of subtly wrong predictions that nobody notices. Loud failure beats silent wrongness, every time.

</details>

---

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 3 Home](README.md) · [Next ➡](module-02-feature-engineering.md)
