# 📝 Level 2 Assessment — Prove You Can Build It

**Level 2 · Assessment · ~2 hours · Prereqs: all nine Level 2 modules**

[⬅ Module 9](module-09-trees-lines-and-overfitting.md) · [Level 2 Home](README.md) · [Capstone ➡](capstone.md) · [Glossary](glossary.md)

---

## 🎯 What This Is For

This is not a test you can fail. It is a **map of your holes**, and holes are much cheaper to find now than in the middle of the capstone.

Three parts, 60 points, about two hours:

| Part | Items | Points each | Total | What it checks |
|---|:--:|:--:|:--:|---|
| **A — Multiple choice** | 20 | 1 | 20 | Do you know what the code does? |
| **B — Short answer** | 8 | 3 | 24 | Can you explain *why*, in words? |
| **C — Debug** | 4 | 4 | 16 | Can you find and fix a real bug? |
| | | | **60** | |

### How to sit it

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  RULES OF ENGAGEMENT                                             │
   ├──────────────────────────────────────────────────────────────────┤
   │  ✅  Paper and pen for working out.                              │
   │  ✅  The glossary, if a word blanks on you.                      │
   │  ❌  No running the code. Predict the output in your head        │
   │      first — that's the actual skill being tested.               │
   │  ❌  No peeking at the answer key until you have written         │
   │      something for EVERY item, including the ones you're         │
   │      guessing at. A wrong written answer teaches you more        │
   │      than a blank.                                               │
   │                                                                  │
   │  Afterwards: run the debug problems. Watching your fix work      │
   │  is half the point.                                              │
   └──────────────────────────────────────────────────────────────────┘
```

Every item is tagged with the module it comes from, like `[M6]`, so a wrong answer tells you exactly which file to reread.

---

# Part A — Multiple Choice (20 × 1 point)

Pick **one** answer per question.

---

**Q1. `[M1]`** What does this print?

```python
print(type(7 / 2))
```

- **A.** `<class 'int'>`
- **B.** `<class 'float'>`
- **C.** `<class 'str'>`
- **D.** `3.5`

---

**Q2. `[M1]`** Exactly one of these lines runs without raising an error. Which?

- **A.** `age = "12";  print(age + 1)`
- **B.** `age = "12";  print(int(age) + 1)`
- **C.** `age = "twelve";  print(int(age) + 1)`
- **D.** `age = 12;  print(age + "1")`

---

**Q3. `[M2]`** How many numbers does `range(1, 10, 2)` produce?

- **A.** 4
- **B.** 5
- **C.** 9
- **D.** 10

---

**Q4. `[M2]`** What is `grade` after this runs?

```python
mark = 92

if mark >= 35:
    grade = "Pass"
elif mark >= 90:
    grade = "Distinction"
else:
    grade = "Fail"
```

- **A.** `"Distinction"`
- **B.** `"Pass"`
- **C.** `"Fail"`
- **D.** Python raises an error because two conditions are true

---

**Q5. `[M3]`** What does this print?

```python
def double(n):
    print(n * 2)

result = double(5)
print(result)
```

- **A.** `10` then `10`
- **B.** `10` then `None`
- **C.** `None` then `10`
- **D.** A `TypeError`

---

**Q6. `[M3]`** Given `scores = [10, 20, 30, 40, 50]`, what is `scores[1:4]`?

- **A.** `[10, 20, 30]`
- **B.** `[20, 30, 40]`
- **C.** `[20, 30, 40, 50]`
- **D.** `[10, 20, 30, 40]`

---

**Q7. `[M4]`** `player = {"name": "Anu", "runs": 40}`. Which expression gives you `0` instead of crashing, when there is no `"wickets"` key?

- **A.** `player["wickets"]`
- **B.** `player.get("wickets")`
- **C.** `player.get("wickets", 0)`
- **D.** `player.wickets`

---

**Q8. `[M4]`** You write the record `{"title": "Blue Lights", "plays": 120}` to a CSV with `csv.DictWriter`, then read it back with `csv.DictReader`. What is `row["plays"]`?

- **A.** `120` — an `int`
- **B.** `'120'` — a `str`
- **C.** `120.0` — a `float`
- **D.** `None`, because numbers can't be stored in CSV

---

**Q9. `[M5]`** What does this print?

```python
import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])
b = np.array([10, 20, 30])
print(a + b)
```

- **A.** An error — the shapes `(2, 3)` and `(3,)` don't match
- **B.** `[[11 22 33]` / ` [14 25 36]]`
- **C.** `[[11 12 13]` / ` [24 25 26]]`
- **D.** `[[11 22 33]]`

---

**Q10. `[M5]`** `scores` is a numpy array of shape `(10, 5)` — 10 students down the rows, 5 tests across the columns. Which gives you **each student's average**?

- **A.** `scores.mean(axis=0)`
- **B.** `scores.mean(axis=1)`
- **C.** `scores.mean()`
- **D.** `scores.mean(axis=2)`

---

**Q11. `[M5]`** What does this print?

```python
import numpy as np

temps = np.array([28, 33, 30, 35, 27])
print(temps[temps > 30])
```

- **A.** `[False  True False  True False]`
- **B.** `[33 35]`
- **C.** `[1 3]`
- **D.** `[28 30 27]`

---

**Q12. `[M6]`** A DataFrame `df` has the index `["a", "b", "c"]`. Which statement is **true**?

- **A.** `df.loc["b"]` and `df.iloc[1]` return the same row
- **B.** `df.loc["b"]` raises an error, because `loc` only takes numbers
- **C.** `df.iloc[1]` raises an error, because the index is text
- **D.** `df.loc[1]` returns the second row

---

**Q13. `[M6]`** `df.info()` shows that your `score` column has dtype `object` even though every value looks like a number. What is the most likely cause?

- **A.** The column has too many rows for pandas to store as numbers
- **B.** At least one value is text — something like `"12"`, `"unknown"` or `"78 "`
- **C.** pandas always uses `object` for numeric columns
- **D.** The column contains negative numbers

---

**Q14. `[M6]`** What does `df.groupby("house")["score"].mean()` return?

- **A.** A DataFrame with all the original columns, sorted by house
- **B.** One mean score per house
- **C.** The overall mean score across the whole table
- **D.** The number of students in each house

---

**Q15. `[M7]`** You want to answer: *"How are my 120 journey times spread out — what's typical, and is there a long tail?"* Which chart?

- **A.** Line chart
- **B.** Bar chart
- **C.** Histogram
- **D.** Scatter plot

---

**Q16. `[M7]`** A bar chart of three house scores (72.4, 71.9, 65.1) is drawn with `ax.set_ylim(64, 73)`. What does this do?

- **A.** Makes the chart more accurate, by zooming in on the real range
- **B.** Exaggerates the differences — Green's bar looks nearly empty next to the others
- **C.** Nothing; the bar heights are set by the data, not the axis
- **D.** It is required, because all the values are above 60

---

**Q17. `[M8]`** Why must features usually be scaled before a k-nearest-neighbors model?

- **A.** Because scikit-learn refuses to fit on unscaled numbers
- **B.** Because a feature with a large numeric range dominates the distance calculation, so small-range features are effectively ignored
- **C.** Because scaling makes training run faster
- **D.** Because scaling removes outliers from the data

---

**Q18. `[M8]`** Which of these is **leakage**?

- **A.** Calling `train_test_split` first, then fitting the scaler on `X_train` only
- **B.** Calling `scaler.fit_transform(X)` on all the data, and *then* splitting
- **C.** Wrapping the scaler and the model in `make_pipeline(...)` and fitting on `X_train`
- **D.** Setting `random_state=42` on the split

---

**Q19. `[M9]`** A decision tree scores **R² = 1.000** on the training data and **R² = 0.71** on the test data. This is:

- **A.** Underfitting — the model is too simple
- **B.** Overfitting — the model has memorised the training rows
- **C.** A good model; 1.000 means it learned perfectly
- **D.** Leakage — the test set must have got into training

---

**Q20. `[M9]`** Two regression models have the **same MAE of 4.0 minutes**. Model A has RMSE 4.2; Model B has RMSE 9.5. What does that tell you?

- **A.** Model B is more accurate on average
- **B.** Model B makes a few very large errors, while Model A's errors are all about the same size
- **C.** Model A is overfitting and Model B is not
- **D.** Nothing — RMSE and MAE always agree, so one of them was computed wrong

---

# Part B — Short Answer (8 × 3 points)

Two to four sentences each. Marks are for **precision and numbers**, not length.

---

**S1. `[M3]`** Explain the difference between `print` and `return` inside a function. Then say why a function that only prints cannot be used inside another calculation.

---

**S2. `[M9]`** Your model reports **MAE = 2.86**. Write the single sentence you would say to an adult who has never heard of machine learning. Your sentence must include the units and a comparison to a baseline.

---

**S3. `[M6]`** What is a **cleaning log**? Explain why the *reason* attached to each entry matters more than the *action*, and give one example line.

---

**S4. `[M5]`** Explain **broadcasting** using a numeric example with real numbers. Then give one pair of shapes that will **not** broadcast, and say why.

---

**S5. `[M8]`** Explain **leakage** using a specific example involving `StandardScaler`. Say what leakage does to the score you report, and in which direction.

---

**S6. `[M7]`** You are shown a bar chart of exam pass rates where the y-axis starts at 92%. Name the trick, and describe two specific steps you would take to repair the chart.

---

**S7. `[M9]`** Describe what happens to the **training score** and the **test score** as you increase a decision tree's `max_depth` from 1 to 15. Say what the widening gap between the two lines is measuring, and what you would do at the point where the test score peaks.

---

**S8. `[M6]` `[M8]`** You collected 118 rows and used `test_size=0.2`. Your kNN classifier scores **0.917** accuracy and your decision tree scores **0.875**. Can you say kNN is the better model? Answer with a number in it.

---

# Part C — Debug (4 × 4 points)

For each: **(a)** say what's wrong, **(b)** predict what the broken code actually prints, **(c)** write the fixed code, **(d)** say what the fixed code prints.

---

**D1. `[M2]` `[M3]`** — *The average that isn't*

This should print the average of the five scores.

```python
scores = [45, 0, 112, 67, 89]

total = 0
for i in range(1, len(scores)):
    total = scores[i]

print("Average:", total / len(scores))
```

It prints something, and the something is wrong. There are **two** bugs.

---

**D2. `[M6]`** — *The top scorer who isn't*

This should find the highest score and the average score.

```python
import pandas as pd

df = pd.DataFrame({
    "name":  ["Aarav", "Bela", "Chen", "Divya"],
    "score": ["90", "85", "78", "100"],
})

print("Top score:", df["score"].max())
print("Average:  ", df["score"].mean())
print(df.sort_values("score", ascending=False))
```

All three lines produce a wrong or nonsensical answer, and **none of them raise an error** on pandas 1.x. Find the single root cause.

---

**D3. `[M8]` `[M9]`** — *The score that lies*

This is supposed to train a kNN regressor and report how well it does.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

scaler = StandardScaler()                                   # line 5
X_scaled = scaler.fit_transform(X)                          # line 6

X_train, X_test, y_train, y_test = train_test_split(        # line 8
    X_scaled, y, test_size=0.2)                             # line 9

knn = KNeighborsRegressor(n_neighbors=5)                    # line 11
knn.fit(X_train, y_train)                                   # line 12

print("R2:", knn.score(X_train, y_train))                   # line 14
```

It runs, prints a lovely number, and that number should not be believed. There are **three** separate problems. Find all three and rank them worst-first.

---

**D4. `[M7]`** — *The chart that argues dishonestly*

This is meant to show mean scores by house so a reader can compare them.

```python
import matplotlib.pyplot as plt

houses = ["Red", "Blue", "Green"]
means  = [72.4, 71.9, 65.1]

plt.bar(houses, means)
plt.ylim(64, 73)
plt.title("Chart")
plt.savefig("houses.png")
```

It runs and produces a picture. List **four** things wrong with it, then rewrite it properly.

---

<br>

---

# ✅ Answer Key

<details>
<summary><b>Click to reveal answers — but only after you've written something for every item</b></summary>

<br>

## Part A — Multiple Choice

### Q1 `[M1]` — **B. `<class 'float'>`**

In Python 3 the `/` operator is **true division** and *always* returns a `float`, even when the division comes out even: `6 / 2` is `3.0`, not `3`.

| Why the others are wrong | |
|---|---|
| **A** `int` | You get an `int` from `//` (floor division): `7 // 2` → `3`. |
| **C** `str` | Nothing here is text. No quotes anywhere. |
| **D** `3.5` | That's the *value*. `type()` reports the *category* of the value, so the printed thing is `<class 'float'>`. Reading the question carefully is the test here. |

---

### Q2 `[M1]` — **B. `age = "12"; print(int(age) + 1)`** → prints `13`

`int("12")` converts the text `"12"` into the number `12`, and `12 + 1` is fine.

| Why the others are wrong | |
|---|---|
| **A** | `TypeError: can only concatenate str (not "int") to str`. Python will not guess whether you meant `"12" + "1"` (glue) or `12 + 1` (add), so it refuses. |
| **C** | `ValueError: invalid literal for int() with base 10: 'twelve'`. Right *kind* of operation, impossible *value* — that's the difference between a `TypeError` and a `ValueError`, and it's worth learning cold. |
| **D** | `TypeError: unsupported operand type(s) for +: 'int' and 'str'`. Same refusal, opposite order. |

---

### Q3 `[M2]` — **B. 5**

`range(start, stop, step)` begins at `start`, adds `step` each time, and **stops before `stop`**: `1, 3, 5, 7, 9`. Count them: five.

| Why the others are wrong | |
|---|---|
| **A** 4 | The classic off-by-one — forgetting that 9 is included because 9 < 10. |
| **C** 9 | That's `range(1, 10)` with the default step of 1. |
| **D** 10 | That's `range(10)`, which is `0…9`. |

---

### Q4 `[M2]` — **B. `"Pass"`**

An `if / elif / else` chain checks conditions **top to bottom and stops at the first true one**. `92 >= 35` is true, so `grade = "Pass"` runs and the `elif` is never even looked at.

This is the **order-matters trap**. The fix is to put the *narrowest* condition first:

```python
if mark >= 90:
    grade = "Distinction"
elif mark >= 35:
    grade = "Pass"
else:
    grade = "Fail"
```

| Why the others are wrong | |
|---|---|
| **A** `"Distinction"` | What you *meant*, not what you *wrote*. Python is literal. |
| **C** `"Fail"` | `else` only runs when every condition above it is false. |
| **D** error | Two true conditions is perfectly legal — Python just takes the first. That's exactly why this bug is so quiet and so common. |

---

### Q5 `[M3]` — **B. `10` then `None`**

`double(5)` prints `10` as a side effect. But it has **no `return` statement**, so it hands back Python's word for "no value at all": `None`. That lands in `result`, and the second `print` shows `None`.

| Why the others are wrong | |
|---|---|
| **A** `10`, `10` | This would need `return n * 2` instead of (or as well as) the print. |
| **C** `None`, `10` | The order is wrong: the function's print happens when the function is called, which is first. |
| **D** `TypeError` | Nothing illegal happened. That's the danger — the code runs perfectly and gives you a useless answer. |

> **The rule:** functions that compute should `return`. Functions that display should `print`. Mixing them is how you end up with `None` in your results table.

---

### Q6 `[M3]` — **B. `[20, 30, 40]`**

A slice `list[start:stop]` includes `start` and **excludes** `stop`. Positions 1, 2, 3 → values 20, 30, 40. A useful shortcut: the length of a slice is `stop − start` = 4 − 1 = 3 items.

| Why the others are wrong | |
|---|---|
| **A** | That's `scores[0:3]`. Indexing starts at **0**, so position 1 is the *second* item. |
| **C** | This includes position 4, which is what `scores[1:5]` would give. `stop` is excluded. |
| **D** | That's `scores[:4]`. |

---

### Q7 `[M4]` — **C. `player.get("wickets", 0)`**

`.get(key, fallback)` is polite asking: if the key isn't there, hand back the fallback instead of crashing.

| Why the others are wrong | |
|---|---|
| **A** | Square brackets on a missing key raise `KeyError: 'wickets'`. |
| **B** | `.get()` with no fallback returns `None`, not `0`. And `None + 5` is a `TypeError` waiting to happen three lines later. |
| **D** | Dot access doesn't work on dictionaries: `AttributeError: 'dict' object has no attribute 'wickets'`. (It *does* work on some other objects, which is why people try it.) |

---

### Q8 `[M4]` — **B. `'120'` — a `str`**

A CSV file is **plain text**. There is nowhere in the file to record that `120` was a number. `csv.DictReader` hands everything back as a string, and `'120' + 1` is a `TypeError`.

The fix is to convert on load, using a written-down schema:

```python
SCHEMA = {"plays": int, "minutes": float}

for row in reader:
    for key, converter in SCHEMA.items():
        row[key] = converter(row[key])
```

| Why the others are wrong | |
|---|---|
| **A** | This is the assumption that breaks the round-trip check. `loaded == songs` comes back `False` and you spend twenty minutes confused. |
| **C** | `float` isn't guessed either. Nothing is guessed. |
| **D** | Numbers store fine — as their text spelling. It's the *type* that's lost, not the value. |

---

### Q9 `[M5]` — **B. `[[11 22 33]` / ` [14 25 36]]`**

**Broadcasting.** Compare shapes right-to-left: `(2, 3)` and `(3,)`. The last dimensions match (3 and 3), and the missing dimension is stretched. So `b` is treated as if it were `[[10,20,30],[10,20,30]]`, and the addition happens position by position.

```
   [[1 2 3]      [10 20 30]      [[11 22 33]
    [4 5 6]]  +  [10 20 30]  =    [14 25 36]]
                  ▲ b, stretched down to 2 rows
```

| Why the others are wrong | |
|---|---|
| **A** | Shapes don't have to match exactly — that's the whole point of broadcasting. |
| **C** | This adds `[10, 20]`-style *down* the rows. To do that you need `b` reshaped to `(2, 1)`. |
| **D** | Broadcasting never shrinks the result; the output shape is `(2, 3)`. |

---

### Q10 `[M5]` — **B. `scores.mean(axis=1)`**

The rule that stops the confusion: **`axis` names the direction you collapse.** `axis=1` is the column direction, so you collapse all 5 columns and are left with 10 numbers — one per student. Shape `(10, 5)` → `(10,)`.

| Why the others are wrong | |
|---|---|
| **A** `axis=0` | Collapses down the rows → 5 numbers, one per **test**. Correct answer to a different question. |
| **C** no axis | Collapses everything → one number, the overall mean. |
| **D** `axis=2` | `AxisError` — a 2-D array only has axes 0 and 1. |

> Memory hook: *"axis=0 squashes rows and leaves you a row; axis=1 squashes columns and leaves you a column."*

---

### Q11 `[M5]` — **B. `[33 35]`**

Two steps happen. First `temps > 30` builds a **boolean mask**: `[False True False True False]`. Then `temps[mask]` keeps only the positions where the mask is `True`.

| Why the others are wrong | |
|---|---|
| **A** | That's the mask itself — what `print(temps > 30)` would show. It's the intermediate step, not the result. |
| **C** | Those are the *positions*, which is what `np.where(temps > 30)` gives. |
| **D** | That's the opposite selection, `temps[temps <= 30]`. |

---

### Q12 `[M6]` — **A. `df.loc["b"]` and `df.iloc[1]` return the same row**

`.loc` selects by **label**; `.iloc` selects by **position**, counting from 0. Here `"b"` is the label of the row at position 1, so both land on the same row. They agree *by coincidence of this index*, not by rule — which is exactly why mixing them up is dangerous.

| Why the others are wrong | |
|---|---|
| **B** | `.loc` takes whatever the index labels are — text, dates, anything. |
| **C** | `.iloc` ignores labels completely; it counts. |
| **D** | `df.loc[1]` raises `KeyError: 1`, because there is no row *labelled* `1`. This is the single most common `loc`/`iloc` bug: it only shows up once you set a non-default index, which is usually well after you wrote the line. |

---

### Q13 `[M6]` — **B. At least one value is text**

A pandas column has **one** dtype for all its values. If 39 rows hold real numbers and one row holds `"unknown"`, `"12 "` (note the trailing space) or an empty string, pandas can't use `int64` — so it falls back to `object`, which means "text, or a mixed mess".

The diagnosis and the fix:

```python
df["score"] = pd.to_numeric(df["score"], errors="coerce")   # bad values -> NaN
print(df["score"].isna().sum(), "values could not be converted")
```

| Why the others are wrong | |
|---|---|
| **A** | Row count has nothing to do with dtype. |
| **C** | pandas uses `int64` / `float64` happily when it can. Seeing `object` on a numeric column is always a signal. |
| **D** | Negatives are perfectly ordinary numbers. |

---

### Q14 `[M6]` — **B. One mean score per house**

`groupby` is *split → apply → combine*: split the rows into groups by house, take the mean of `score` in each, stick the answers back together. The result is a **Series** indexed by house name.

```
house
Blue     75.5
Green    83.0
Red      63.5
Name: score, dtype: float64
```

| Why the others are wrong | |
|---|---|
| **A** | That's `df.sort_values("house")` — no aggregation happened. |
| **C** | That's `df["score"].mean()` with no grouping. |
| **D** | That's `df["house"].value_counts()`, or `.groupby("house")["score"].count()`. |

> ⚠️ The hidden danger the module made you look for: that clean three-row output says nothing about whether Green has 40 students or 2. Always print the counts alongside the means. `agg(n=("score","count"), avg=("score","mean"))`.

---

### Q15 `[M7]` — **C. Histogram**

The question has one number column and asks about its **shape** — typical value, spread, tail. That's the definition of a distribution, and a histogram is the chart that shows one.

| Why the others are wrong | |
|---|---|
| **A** line | Lines are for a value moving **over time**. Journeys have no natural time order here. |
| **B** bar | Bars **compare categories**. "Journey time" isn't a category. |
| **D** scatter | Scatter shows the **relationship between two** numbers. This question only has one. |

---

### Q16 `[M7]` — **B. Exaggerates the differences**

This is the **truncated y-axis**, the most common visual lie there is. The real gap between Red (72.4) and Green (65.1) is 7.3 points out of ~72 — about 10%. With the axis starting at 64, Red's bar is 8.4 units tall and Green's is 1.1, so Green *looks* about 87% smaller. The exaggeration factor is roughly 8×.

| Why the others are wrong | |
|---|---|
| **A** | Zooming is fine for a **line** chart of a slow-moving quantity, where you label the axis clearly. It is never fine for **bars**, because a bar's whole meaning is that its *area* represents the value. |
| **C** | The bar heights on screen absolutely do change — that's the trick. |
| **D** | Nothing requires it. Bars start at 0. That's the rule. |

**The repair:** `ax.set_ylim(0, 100)`, plus a caption stating the real gap in points.

---

### Q17 `[M8]` — **B. A large-range feature dominates the distance**

kNN's only idea is "which rows are closest?", and closeness is Euclidean distance — squares of the differences, added up. If `proline` runs 200–1700 and `hue` runs 0.5–1.7, then a typical `proline` difference is ~500 and a typical `hue` difference is ~0.4. Squared, that's 250,000 versus 0.16. The `hue` column might as well not exist.

`StandardScaler` rewrites every column as `z = (value − mean) ÷ std`, so all columns arrive at the distance calculation with the same-sized units.

| Why the others are wrong | |
|---|---|
| **A** | sklearn will happily fit unscaled data. It just gives you a worse model, silently. |
| **C** | Speed barely changes. Accuracy changes a lot. |
| **D** | Scaling *moves* outliers; it doesn't remove them. A z-score of 4.2 is still a z-score of 4.2. |

> Worth remembering from the capstone: scaling is a strong **default**, not a law. On a dataset where one feature genuinely deserves to dominate, unscaled can win. Measure it; don't assume it.

---

### Q18 `[M8]` — **B. `scaler.fit_transform(X)` on all the data, then split**

`fit` on the scaler computes the **mean and standard deviation of every column**. If you compute those from all the rows, the training data now carries information about the test rows — their values helped decide the centring. Your test score is no longer an honest estimate of performance on unseen data. It comes out too high.

| Why the others are wrong | |
|---|---|
| **A** | This is the correct order. Split first, fit on train only, `transform` the test set with the training statistics. |
| **C** | A pipeline does exactly A for you, automatically, and can't forget. This is the recommended way. |
| **D** | `random_state` makes the split *repeatable*, which is the opposite of a problem. |

---

### Q19 `[M9]` — **B. Overfitting**

A perfect training score with a much lower test score is the definition. The tree has grown deep enough to make a leaf for (almost) every training row — it has memorised the answer key rather than learned a rule. The **train/test gap** here is 1.000 − 0.71 = **0.29**.

| Why the others are wrong | |
|---|---|
| **A** underfitting | The opposite: bad on *both*. A depth-1 tree scoring 0.42 train / 0.22 test is underfitting. |
| **C** | 1.000 on training data is a warning light, never a result. Any model with enough freedom can hit it. |
| **D** leakage | Leakage usually makes the **test** score suspiciously high, not low. Here the test score is the believable one. |

**The fix:** turn the complexity dial down — set `max_depth` to the value where the *test* curve peaks.

---

### Q20 `[M9]` — **B. Model B makes a few very large errors**

MAE averages the **sizes** of the errors. RMSE squares them first, which punishes big misses far harder, then square-roots at the end. RMSE is always ≥ MAE, and the *gap between them* is a measure of how uneven your errors are.

A worked case with the same MAE of 1.0:

| Errors | MAE | RMSE |
|---|:--:|:--:|
| `1, 1, 1, 1` | 1.0 | `√((1+1+1+1)/4)` = **1.00** |
| `0, 0, 0, 4` | 1.0 | `√((0+0+0+16)/4)` = **2.00** |

Same average miss; wildly different behaviour. Model B is the second row: mostly fine, occasionally catastrophic. Which matters depends on your problem — a bus that's usually on time but occasionally 40 minutes late is worse than one that's always 5 minutes late, even though the MAE could be identical.

| Why the others are wrong | |
|---|---|
| **A** | "On average" is precisely what MAE measures, and they're tied at 4.0. |
| **C** | Neither metric says anything about training scores, which is where overfitting lives. |
| **D** | They're different formulas and routinely disagree; RMSE ≥ MAE always, with equality only when every error is the same size. |

---

## Part B — Short Answer

Award yourself **3** for a full answer, **2** for correct but missing a number or an example, **1** for a partly-right idea, **0** for blank or wrong.

---

### S1 `[M3]` — print vs return

**Full answer:** `print` sends text to the screen for a human to read; `return` hands a **value** back to the code that called the function. A function with no `return` gives back `None`. So `total = show_mean(scores)` puts `None` into `total` if `show_mean` only prints — and `None * 2` raises a `TypeError`. You cannot chain, store, test, or do arithmetic with something that was printed, because printing produces no value; it only produces pixels.

**Full marks needs:** the word `None`, and a concrete example of the downstream breakage.

---

### S2 `[M9]` — explaining MAE

**Full answer (a model sentence):** *"On the 24 journeys the model had never seen, its guesses were off by about **2.86 minutes** on average — compared with **9.41 minutes** if you just always guessed the overall average time."*

**Full marks needs three things:**

| Ingredient | Why it's required |
|---|---|
| The **units** ("minutes") | A bare "2.86" is meaningless. Is that good? Nobody can tell. |
| The **baseline** ("9.41 if you just guessed the mean") | A number with nothing to compare it to is a boast, not a measurement. |
| **Unseen data** ("had never seen") | Otherwise you may be quoting a memorised score. |

Bonus if you also state the test-set size. Zero marks for "it's 97% accurate" — MAE is not a percentage and accuracy is not a regression metric.

---

### S3 `[M6]` — the cleaning log

**Full answer:** A cleaning log is a numbered list of every change you made to the raw data, each with a reason. It ships alongside the results. The *action* alone ("dropped 4 rows") is just a receipt — it tells a reader what happened but gives them nothing to agree or disagree with. The *reason* turns it into an argument that can be checked, challenged and improved: someone can read it and say "I'd have filled those instead, and here's why."

**Example line:**

> `5. Dropped 4 rows with a missing target — you cannot train on a row whose answer is unknown, and inventing one would be fabrication.`

**Full marks needs:** a real example line with a real reason, and the point that reasons are *checkable* while actions are not.

---

### S4 `[M5]` — broadcasting

**Full answer:** Broadcasting is numpy stretching a smaller array so it fits a bigger one, without copying any memory. Compare shapes **right to left**; dimensions must either match or be 1.

```
   scores.shape = (3, 4)        bonus.shape = (4,)
   [[80 60 90 70]               [0 5 0 10]
    [45 75 55 65]        +      stretched to all 3 rows
    [90 88 92 79]]

   row 1 becomes  80+0=80,  60+5=65,  90+0=90,  70+10=80
```

**A pair that will not broadcast:** `(3, 4)` and `(3,)`. Right-to-left, 4 vs 3 — neither matches nor is 1, so numpy raises `ValueError: operands could not be broadcast together`. To add one value per *row* you must reshape to `(3, 1)`.

**Full marks needs:** actual arithmetic on real numbers, plus a failing pair with the reason.

---

### S5 `[M8]` — leakage

**Full answer:** Leakage is when information from the test set reaches the model during training, so your reported score is better than the model's real ability.

**Specific example:** you call `scaler.fit_transform(X)` on all 120 rows and *then* split. `fit` computed each column's mean and standard deviation using all 120 rows — including the 24 test rows. Those 24 rows have now influenced how the training data was rescaled. The test set is no longer unseen.

**Direction:** it makes the reported score **too high** (optimistically biased). The model looks better in your notebook than it will ever be in the world, which is the most expensive kind of wrong.

**The fix:** `make_pipeline(StandardScaler(), KNeighborsRegressor(5))`, fitted after the split. The pipeline fits the scaler on the training fold only and uses those same statistics to transform the test fold.

**Full marks needs:** the direction of the bias (too high) and a concrete fix.

---

### S6 `[M7]` — the truncated axis

**Full answer:** The trick is a **truncated y-axis** — starting the axis at 92% instead of 0, so a tiny real difference fills the whole picture. If the bars are 94%, 96% and 98%, the real spread is 4 percentage points, but on a 92–100 axis the tallest bar is *three times* the height of the shortest.

**Two repairs:**

1. `ax.set_ylim(0, 100)` — bars must start at zero, always, because a bar's meaning is carried by its height from the baseline.
2. Add a caption stating the real difference in its own units: *"Pass rates differ by 4 percentage points (94% to 98%)."* If the small difference genuinely matters, say so in words rather than faking it with geometry.

A good third: if you truly need the zoom, switch to a **dot plot** or a line chart with the axis break clearly marked and labelled.

---

### S7 `[M9]` — the complexity curve

**Full answer:** As `max_depth` rises from 1 to 15:

- The **training score rises, always**, and eventually reaches 1.000. A deeper tree can carve the training rows into ever-finer boxes until each leaf holds a handful of rows — or one.
- The **test score rises, peaks, then falls or flattens**. Early on, extra depth buys real structure. After the peak, extra depth is only fitting the noise in *these particular* training rows, which doesn't transfer.

The **widening gap** between the two lines measures how much of the model's performance is memorisation rather than learning.

**At the peak:** stop. Set `max_depth` to that value and refit. Then add the honesty sentence: *"I chose this depth by looking at the test curve, so my reported test score is slightly optimistic."*

**Full marks needs:** "training score can only go up", the peak-then-fall shape, and the gap-as-memorisation reading.

---

### S8 `[M6]` `[M8]` — is kNN better?

**Full answer: no, you cannot say that.** With 118 rows and `test_size=0.2`, the test set holds **24 rows** (118 × 0.2 = 23.6, and sklearn rounds the test set up). One row is therefore worth 1 ÷ 24 = **4.2 percentage points** of accuracy.

Now do the arithmetic on the two scores. 0.917 × 24 = **22 rows correct**. 0.875 × 24 = **21 rows correct**. The entire difference between your two models is **one single test journey.** Change `random_state` and that one row moves, and the ranking very likely flips.

What you *can* honestly say: both models are far above the baseline, they are indistinguishable at this sample size, so choose between them on other grounds — interpretability, speed, robustness — and say so out loud.

**Full marks needs:** the test-set size (24), the value of one row (4.2 points), and the conclusion that a one-row gap is not a ranking.

---

## Part C — Debug

---

### D1 `[M2]` `[M3]` — the average that isn't

**(a) The two bugs**

| # | Line | Bug | Why it happens |
|:--:|---|---|---|
| 1 | `for i in range(1, len(scores))` | Starts at **1**, so `scores[0]` (the 45) is never visited, and it stops at index 4 correctly but only covers 4 of 5 items | People count from 1 in real life; Python indexes from 0 |
| 2 | `total = scores[i]` | Plain assignment **replaces** `total` each pass instead of adding to it | `=` and `+=` look almost identical at speed |

Bug 2 is the fatal one: after the loop, `total` is simply `scores[4]`, i.e. `89`. Bug 1 is invisible because of bug 2 — fix only bug 2 and you'd still get the wrong answer.

**(b) What the broken code prints**

```
Average: 17.8
```

(`89 / 5` = 17.8.)

**(c) The fix**

```python
scores = [45, 0, 112, 67, 89]

total = 0
for score in scores:          # loop over the VALUES — no index, no off-by-one
    total += score            # += accumulates instead of replacing

print("Average:", total / len(scores))
```

Two habits worth stealing here: loop over the items rather than over indices when you don't need the position, and use `+=` for anything called `total`.

**(d) What the fixed code prints**

```
Average: 62.6
```

Hand-check it: 45 + 0 + 112 + 67 + 89 = 313, and 313 ÷ 5 = 62.6. ✅

*(One-line version, once you trust it: `print("Average:", sum(scores) / len(scores))`. Write the loop first, though — Module 3's point is that you should be able to build the tool before you use the built-in.)*

---

### D2 `[M6]` — the top scorer who isn't

**(a) The root cause**

The `score` column is **text, not numbers**. Quotes around `"90"`, `"85"`, `"78"`, `"100"` make the dtype `object`. Every operation then does the *string* version of what you meant:

- `.max()` compares strings **alphabetically**, character by character. `'9'` comes after `'1'`, so `"90"` beats `"100"` — because it compares `'9'` vs `'1'` and stops there.
- `.mean()` on object dtype (pandas 1.x) **glues the strings together** — `"90"+"85"+"78"+"100"` = `"908578100"` — and then divides that by 4.
- `.sort_values()` sorts alphabetically too, so `"100"` sinks to the bottom.

The one-line diagnosis you should always run first:

```python
print(df.dtypes)
```
```
name     object
score    object          ← this is the bug
dtype: object
```

**(b) What the broken code prints**

```
Top score: 90
Average:   227144525.0
    name score
0  Aarav    90
1   Bela    85
2   Chen    78
3  Divya   100
```

`227144525.0` is `908578100 / 4`. Note that `Divya`, the actual top scorer with 100, is sorted **last**.

> **Version note:** on pandas 2.x the `.mean()` line raises `TypeError` instead of returning nonsense. The silent-wrong-answer version is the more dangerous one, which is why it's the version shown.

**(c) The fix**

```python
import pandas as pd

df = pd.DataFrame({
    "name":  ["Aarav", "Bela", "Chen", "Divya"],
    "score": ["90", "85", "78", "100"],
})

# Convert once, as early as possible. errors="coerce" turns anything
# unconvertible (like "tbd") into NaN instead of crashing the whole script.
df["score"] = pd.to_numeric(df["score"], errors="coerce")

print(df.dtypes)                      # verify BEFORE trusting any number
print("Top score:", df["score"].max())
print("Average:  ", df["score"].mean())
print(df.sort_values("score", ascending=False).to_string(index=False))
```

**(d) What the fixed code prints**

```
name     object
score     int64
dtype: object
Top score: 100
Average:   88.25
 name  score
Divya    100
Aarav     90
 Bela     85
 Chen     78
```

Hand-check: (90 + 85 + 78 + 100) ÷ 4 = 353 ÷ 4 = 88.25. ✅

**The habit this teaches:** run `df.info()` or `df.dtypes` immediately after every `read_csv`, before you compute anything. Module 4 warned you that CSV gives everything back as text; this is that warning arriving with real consequences.

---

### D3 `[M8]` `[M9]` — the score that lies

**(a) Three problems, worst first**

| Rank | Line | Problem | Effect |
|:--:|:--:|---|---|
| 🥇 **1** | 14 | **Scored on the training data.** `knn.score(X_train, y_train)` measures how well the model does on rows it learned from. That is not a result; it is a memory test. | The reported number is meaningless. This is the worst bug because it invalidates the entire output. |
| 🥈 **2** | 6 | **Leakage.** `scaler.fit_transform(X)` runs before the split, so the column means and standard deviations were computed using the test rows too. | Even when you fix bug 1, the test score is inflated. |
| 🥉 **3** | 9 | **No `random_state`.** Every run produces a different split and a different score. | Not reproducible. You cannot compare two models, or your result today with your result tomorrow. |

**(b) What the broken code prints**

Something like `R2: 0.946` — high, stable-looking, and completely untrustworthy. Note that it *looks* fine, which is the point: none of these three bugs raises an error. Broken evaluation code is silent, and that is why it is the most dangerous kind.

**(c) The fix**

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# 1. SPLIT FIRST. Nothing has touched the data yet.
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,          # fix 3: the same split every run
)

# 2. The scaler lives INSIDE the pipeline, so it is fitted on the
#    training fold only and cannot see the test rows.  (fix 2)
model = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(n_neighbors=5),
)
model.fit(X_train, y_train)

# 3. Report BOTH. The gap between them is the story.   (fix 1)
print(f"train R2: {model.score(X_train, y_train):.3f}")
print(f"test  R2: {model.score(X_test,  y_test):.3f}")
print(f"test rows: {len(y_test)}  ·  one row is worth {100/len(y_test):.1f}%")
```

**(d) What the fixed code prints** (on the capstone's demo journey data)

```
train R2: 0.944
test  R2: 0.907
test rows: 24  ·  one row is worth 4.2%
```

The honest number, 0.907, is **lower** than the broken one — and that is the normal, healthy direction. If your score goes *up* after you fix an evaluation bug, look again; something else is wrong.

> **The rule of thumb:** if a scoring line mentions `_train` on the right-hand side and you're calling it a result, stop. Report both, always, and treat the gap as data.

---

### D4 `[M7]` — the chart that argues dishonestly

**(a) Four things wrong**

| # | Problem | Why it matters |
|:--:|---|---|
| 1 | **`plt.ylim(64, 73)` truncates the y-axis** | Green's real score is 65.1 out of ~72 — about 10% below Red. On this axis its bar is 1.1 units tall against Red's 8.4, so it *looks* 87% smaller. Roughly an 8× exaggeration. |
| 2 | **No axis labels** | A reader has no idea whether the numbers are marks out of 100, percentages, or points. Units are not optional. |
| 3 | **The title is a topic, not a finding** | `"Chart"` tells nobody anything. A title should state the takeaway. |
| 4 | **No caption, and no `n` per house** | Green might be 40 students or 2. A mean over 2 students is not a fact about a house. |

Two more worth spotting for extra credit: `savefig` without `bbox_inches="tight"` will clip long labels, and using the `plt.` interface instead of `fig, ax` makes the figure hard to reuse or place in a grid.

**(b) What the broken code produces**

A PNG in which Blue and Red look roughly level and Green looks like a stump — visually implying Green scored close to nothing, when it actually scored 65.1 out of ~72.

**(c) The fix**

```python
import matplotlib.pyplot as plt

houses = ["Red", "Blue", "Green"]
means  = [72.4, 71.9, 65.1]
counts = [14, 13, 11]                       # never plot a mean without its n

fig, ax = plt.subplots(figsize=(6, 4))      # explicit figure and axes
bars = ax.bar(houses, means, color=["#c0392b", "#2980b9", "#27ae60"])

ax.set_ylim(0, 100)                         # FIX 1: bars start at zero
ax.set_title("Green averages 7.3 points below Red — the houses are close")   # FIX 3
ax.set_xlabel("house")                      # FIX 2
ax.set_ylabel("mean end-of-term score (points out of 100)")   # FIX 2, with units

# print the value and the group size on each bar
for bar, mean, n in zip(bars, means, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, mean + 1.5,
            f"{mean:.1f}\n(n={n})", ha="center", fontsize=9)   # FIX 4

fig.savefig("houses.png", dpi=150, bbox_inches="tight")
```

**(d) What the fixed chart shows**

Three bars of almost the same height — because that is the truth. The gap between Red (72.4) and Green (65.1) is **7.3 points out of 100**, visible but modest.

**Caption to go under it:**

> *"Red and Blue are effectively tied (72.4 and 71.9); Green sits 7.3 points lower. With 11–14 students per house, a gap this size is worth noticing but not worth acting on yet."*

**The lesson:** the dishonest chart and the honest chart are drawn from **identical data**. Nothing was faked. The lie lived entirely in `set_ylim`. That's why Module 7 spends so long on axes — the most effective visual lies never touch the numbers.

</details>

---

## 📊 Score Yourself

| Part | Your score | Out of |
|---|:--:|:--:|
| A — Multiple choice | ____ | 20 |
| B — Short answer | ____ | 24 |
| C — Debug | ____ | 16 |
| **Total** | **____** | **60** |

| Band | Score | What it means | What to do |
|---|:--:|---|---|
| 🔴 **Rebuild** | 0–29 | The vocabulary is there but the mechanics aren't yet | Redo the mini-projects for M1–M4 from a blank file, without looking. Then re-sit. Do **not** start the capstone. |
| 🟠 **Patch** | 30–41 | Solid in places, with two or three real gaps | Use the module tags on the items you missed. Reread just those modules and redo their practice sets. Re-sit the items you got wrong. |
| 🟡 **Ready** | 42–52 | You can build the capstone | Start it. Keep the glossary open. Reread the one module your wrong answers clustered in. |
| 🟢 **Fluent** | 53–60 | You could teach Modules 1–7 | Start the capstone and take one of its stretch directions. |

**One diagnostic that matters more than the total:** count your wrong answers **by module tag**. Four wrong in one module is a real gap. Four wrong spread across eight modules is just a tired afternoon.

---

## ✅ Self-Assessment Checklist

Tick honestly. "I could do it with the module open" is **not** a tick — the standard is *from a blank file, with only the glossary*.

### Outcome 1 — Write a Python program from a blank file

- [ ] I can write, save and run a `.py` file from the terminal **and** from my editor
- [ ] I can name the type of any value and convert between `str`, `int`, `float` and `bool`
- [ ] I can read a traceback, find the line number, name the error type, and fix it myself
- [ ] I can write an `if/elif/else` chain where the order is correct and every case is handled exactly once
- [ ] I can write a `for` loop with an accumulator, and a `while` loop that definitely terminates
- [ ] I can define a function with parameters, a default value, and a `return` — and explain why `return` isn't `print`
- [ ] I can index, slice, append to, sort and loop over a list, and write a list comprehension
- [ ] I can build a dictionary, get a value safely with `.get()`, and build a list-of-dicts dataset
- [ ] I can write that dataset to CSV and read it back, converting types on the way in

### Outcome 2 — Clean and interrogate a table with pandas

- [ ] I can build a DataFrame and read `head`, `info`, `describe` and `shape` without guessing
- [ ] I can select with `loc` and `iloc` and say which one is by label and which by position
- [ ] I can filter rows with a boolean condition and add a computed column
- [ ] I can find missing values, fix wrong dtypes, drop duplicates, and standardise messy category spellings
- [ ] I write a **numbered cleaning log with a reason per line**, every time, without being asked
- [ ] I can answer a grouped question with `groupby` + `agg` — and I always print the group sizes too

### Outcome 3 — Array maths without loops

- [ ] I can create arrays and read `shape`, `dtype` and `ndim`
- [ ] I can predict whether two shapes will broadcast, and say what the result's shape will be
- [ ] I can aggregate along `axis=0` vs `axis=1` and say which one I need without trial and error
- [ ] I can select data with a boolean mask instead of a loop with an `if` inside

### Outcome 4 — Five labelled charts, and spotting the liars

- [ ] Given a question, I can name the right chart type and say why
- [ ] Every chart I make has a title stating a **finding**, axis labels **with units**, and a legend when needed
- [ ] I can read a distribution off a histogram and a relationship off a scatter plot
- [ ] I can spot a truncated axis or a cherry-picked range, name the trick, and repair it
- [ ] I say "correlation is not causation" **and** can name a plausible confounder for a given pair

### Outcome 5 — Train models with a proper split

- [ ] I can turn a table into `X` and `y` and print both shapes
- [ ] I can compute the Euclidean distance between two feature rows **by hand** on paper
- [ ] I call `train_test_split` **exactly once**, with `random_state` set
- [ ] I put any scaler inside a `make_pipeline` and can explain what leakage would otherwise do
- [ ] I can fit and score kNN, a decision tree, and linear regression on the same split
- [ ] I read a tree's splits out loud as plain-English rules
- [ ] I state the slope and intercept of a linear regression **in the units of the problem**

### Outcome 6 — Measure honestly, and demonstrate overfitting

- [ ] I never report a score without a **baseline** next to it
- [ ] I never report a metric without its **units** and the **test-set size**
- [ ] I can say what MAE, RMSE and R² each mean, and when I'd prefer one over another
- [ ] I always report a **train score and a test score**, and read the gap as data
- [ ] I have produced my own complexity curve where train rises and test falls
- [ ] I can point at a depth on that curve and say "here is where it starts memorising"

---

## 🚪 You're Ready for Level 3 When…

Level 3 will not slow down for missing Level 2 skills. Here is the honest gate.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │  THE LEVEL 3 GATE — all six, or go back                            │
   ├────────────────────────────────────────────────────────────────────┤
   │                                                                    │
   │  1.  You scored 42+ on this assessment (70%), with no single       │
   │      module accounting for 4+ of your wrong answers.               │
   │                                                                    │
   │  2.  You have FINISHED the capstone. Not started — finished,       │
   │      with a cleaning log, five charts, three models on one         │
   │      split, and a "what I got wrong" section with numbers in it.   │
   │                                                                    │
   │  3.  You can open a blank file and write a working function with   │
   │      a loop and a conditional inside it, from memory, in under     │
   │      five minutes. No copying.                                     │
   │                                                                    │
   │  4.  Given a shape mismatch error from numpy, you can say what     │
   │      the two shapes were and how to fix it — without running it.   │
   │                                                                    │
   │  5.  You can explain leakage to someone who has never heard the    │
   │      word, using StandardScaler as the example, in under a         │
   │      minute, and say which direction it moves your score.          │
   │                                                                    │
   │  6.  You can draw the overfitting graph on a napkin — both lines,  │
   │      labelled axes — and say what the gap between them means.      │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘
```

### If you're missing one

| Missing | The cheapest fix |
|---|---|
| **Gate 1** (score) | Reread the module your wrong answers cluster in, redo its six practice exercises, re-sit those items. Half a day. |
| **Gate 2** (capstone) | There is no shortcut. Level 3 Module 1 builds a reusable pipeline and assumes you have already suffered through one end-to-end project by hand. |
| **Gate 3** (blank-file fluency) | Ten days of one 15-minute exercise: write `fizzbuzz`, a temperature converter, a list-max function, a word counter — each from nothing. This is a typing-fluency problem, and typing fluency only comes from typing. |
| **Gate 4** (shapes) | Redo [Module 5](module-05-numpy-arrays.md)'s practice, and add a habit: print `.shape` after **every** array operation for a week. |
| **Gate 5** (leakage) | Reread [Module 8](module-08-first-model-knn.md) section 5 and explain it out loud to a person. If they ask a question you can't answer, you found the hole. |
| **Gate 6** (the graph) | Rerun [Module 9](module-09-trees-lines-and-overfitting.md)'s depth curve on a different dataset (`load_diabetes()` needs no download) and draw the result by hand before you plot it. |

### What Level 3 does with all of this

```
   YOUR LEVEL 2 SKILL          ─►   WHAT LEVEL 3 TURNS IT INTO
   ─────────────────────────        ────────────────────────────────────
   LinearRegression().fit()    ─►   gradient descent you write yourself,
                                    plotted converging step by step
   "the model has a loss"      ─►   a loss function you differentiate
   X of shape (n, d)           ─►   the design matrix, and matrix maths
   a derived column            ─►   feature engineering, with leakage rules
   the train/test gap          ─►   regularization and cross-validation
   three models in a table     ─►   one reusable pipeline object
   a tree of if/then rules     ─►   layers of neurons doing the same job
                                    with numbers instead of questions
```

Every arrow points from something you can already do to something you're about to understand. That is what a good curriculum feels like from the inside.

---

> ### 👉 Next: **[The Level 2 Capstone — Data Detective](capstone.md)**
>
> Then: **[Level 3 — Engineer](../level-3-engineer/)**

---

[⬅ Module 9](module-09-trees-lines-and-overfitting.md) · [Level 2 Home](README.md) · [Capstone](capstone.md) · [Glossary](glossary.md) · [Level 3 ➡](../level-3-engineer/)
