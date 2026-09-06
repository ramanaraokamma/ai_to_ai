# Module 6 — Pandas: Loading, Cleaning, and Interrogating a Table

**Level 2 · Module 6 · ~4 hours · Prereqs: Modules 1–5 (functions, lists, dictionaries, list-of-dicts datasets, CSV files, numpy arrays, axes, boolean masks)**

[⬅ Previous](module-05-numpy-arrays.md) · [Level 2 Home](README.md) · [Next ➡](module-07-visualizing-data.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** build a DataFrame, inspect it with `head`, `info`, `describe`, and `shape`, and select rows and columns with `loc` and `iloc`.
2. **You will be able to** filter rows with boolean conditions and create new computed columns.
3. **You will be able to** find and repair missing values, wrong dtypes, duplicate rows, and inconsistent category spellings.
4. **You will be able to** write a **cleaning log** — a numbered list of every change you made and *why* — and explain why the log matters as much as the clean data.
5. **You will be able to** answer a question about groups using `groupby` with an aggregation, and spot when a group is too small to say anything about.

---

## 🪝 The Hook

In Module 4 you built a dataset as a list of dictionaries and asked it questions with `filter_by` and `group_count`. It worked. It was also about fifteen lines of your own code per question, and every one of those lines was yours to get wrong.

In Module 5 you got numpy, which is brilliant at arithmetic and completely blind to names. `scores.mean(axis=0)` gives you four numbers. Which test was which? You kept a separate array of names and hoped the order never changed.

**Pandas is the missing piece: a table where the columns have names and the arithmetic is still vectorized.**

```python
df.groupby("house")["score"].mean()
```

One line. That's the Module 4 group-and-count *and* the Module 5 axis-mean, with the names still attached. Every question you asked with fifteen lines becomes one.

Here's the part nobody tells you at the start: **you will spend far more time cleaning the table than asking it questions.** Real data arrives with missing ages, numbers typed as text, the same house spelled four ways, and the same person entered twice. This module is mostly about that, because the honest work is there.

---

## 🧠 The Concept

### 0. Getting pandas

```bash
pip install pandas
```

```python
import pandas as pd
import numpy as np

print(pd.__version__)     # e.g. 1.5.3 or 2.x — both fine for this module
```

`pd` and `np` are the universal nicknames. Use them.

> 📌 **Version note:** pandas 2.x prints `value_counts()` results with a slightly different header (`Name: count` instead of `Name: house`). The *numbers* in this module are identical on both. If your header line differs from the book, you're fine.

---

### 1. Series and DataFrame, and the index

#### The plain-language explanation

Pandas has exactly two containers you need to know.

> **Definition — Series:** one column. A row of values with a *label* attached to each one, plus a name for the column itself. Think: a numpy array that remembers what its rows are called.

> **Definition — DataFrame:** a whole table. A collection of Series that all share the same row labels.

> **Definition — index:** the row labels down the left-hand side. By default it's `0, 1, 2, …`, but it can be dates, names, sensor IDs — anything.

#### 🍕 The analogy

A numpy 2-D array is a grid of numbers drawn on graph paper: you find things by counting squares. A DataFrame is the same grid printed as a proper spreadsheet — column headers along the top, row labels down the side. Same numbers, but now you can say "the *score* column for *Divya*" instead of "row 3, column 4."

#### 🔍 Tiny concrete example

Build one from a dictionary of lists. **Keys become column names; each list becomes a column.**

```python
import pandas as pd

students = pd.DataFrame({
    "name":    ["Aarav", "Bela", "Chen", "Divya", "Emeka"],
    "grade":   [7, 8, 7, 8, 7],
    "house":   ["Red", "Blue", "Red", "Green", "Blue"],
    "score":   [72, 90, 55, 83, 61],
    "minutes": [30, 55, 20, 45, 35],
})
print(students)
```

```
    name  grade  house  score  minutes
0  Aarav      7    Red     72       30
1   Bela      8   Blue     90       55
2   Chen      7    Red     55       20
3  Divya      8  Green     83       45
4  Emeka      7   Blue     61       35
```

That leftmost column `0 1 2 3 4` is the **index**. It is not a data column — it's the row's name.

```
              ┌── column names (like the keys of Module 4's dicts)
              ▼
       ┌───────┬───────┬───────┬───────┬─────────┐
       │ name  │ grade │ house │ score │ minutes │
   ┌───┼───────┼───────┼───────┼───────┼─────────┤
 0 │   │ Aarav │   7   │  Red  │  72   │   30    │  ← one row = one student
 1 │   │ Bela  │   8   │ Blue  │  90   │   55    │
 2 │   │ Chen  │   7   │  Red  │  55   │   20    │
 3 │   │ Divya │   8   │ Green │  83   │   45    │
 4 │   │ Emeka │   7   │ Blue  │  61   │   35    │
   └─┬─┴───────┴───────┴───────┴───────┴─────────┘
     │        │
   INDEX      └─ each column is a SERIES with its own dtype
```

Compare the three shapes you now know:

| Module | Shape | One row is | Columns have names? | Vectorized maths? |
|---|---|---|---|---|
| 4 | list of dicts | a `dict` | ✅ yes (the keys) | ❌ no, you loop |
| 5 | numpy 2-D array | a row of numbers | ❌ no, just positions | ✅ yes |
| 6 | **DataFrame** | a labelled row | ✅ **yes** | ✅ **yes** |

#### The four inspection commands you run on every new table

```python
print(students.head())        # first 5 rows — .head(3) for three
print(students.shape)         # (5, 5)  -> (rows, columns)
print(students.dtypes)        # the type of each column
print(students.describe())    # count/mean/std/min/quartiles/max for NUMERIC columns
```

```
(5, 5)

name       object
grade       int64
house      object
score       int64
minutes     int64
dtype: object

          grade      score    minutes
count  5.000000   5.000000   5.000000
mean   7.400000  72.200000  37.000000
std    0.547723  14.618481  13.509256
min    7.000000  55.000000  20.000000
25%    7.000000  61.000000  30.000000
50%    7.000000  72.000000  35.000000
75%    8.000000  83.000000  45.000000
max    8.000000  90.000000  55.000000
```

> **Definition — `object` dtype:** pandas's label for "a column of Python objects", which in practice almost always means **text**. Seeing `object` on a column you *expected* to be numeric is your loudest warning sign.

`info()` combines several of these and adds the one number that matters most when cleaning:

```python
students.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column   Non-Null Count  Dtype 
---  ------   --------------  ----- 
 0   name     5 non-null      object
 1   grade    5 non-null      int64 
 2   house    5 non-null      object
 3   score    5 non-null      int64 
 4   minutes  5 non-null      int64 
dtypes: int64(3), object(2)
```

**`5 non-null` out of 5 entries** means nothing is missing. When that number is smaller than the entry count, you have holes.

---

### 2. Selection: columns, `loc` vs `iloc`, and boolean filtering

#### The plain-language explanation

Three ways to get at data, and they answer three different questions.

#### 🍕 The analogy

Picking a column is *"give me everyone's maths mark."* `loc` is *"give me the row for the student called Divya."* `iloc` is *"give me the fourth row down, whoever that is."* Boolean filtering is *"give me everyone who scored over 80."*

#### 🔍 One column → a Series

```python
print(students["score"])
```

```
0    72
1    90
2    55
3    83
4    61
Name: score, dtype: int64
```

Note the index came along for the ride, and the Series knows its own name. A Series behaves like a numpy array with names:

```python
print(students["score"].mean())    # 72.2
print(students["score"].max())     # 90
print(students["score"] * 2)       # vectorized, just like numpy
```

#### 🔍 Several columns → a DataFrame (double brackets!)

```python
print(students[["name", "score"]])
```

```
    name  score
0  Aarav     72
1   Bela     90
2   Chen     55
3  Divya     83
4  Emeka     61
```

> ⚠️ `students["name", "score"]` (single brackets) fails. The outer bracket means "select", the inner bracket is **a list of column names**. Two brackets, always, for more than one column.

#### 🔍 `loc` vs `iloc`

> **Definition — `.loc[]`:** select by **label** — the index value and the column name.

> **Definition — `.iloc[]`:** select by **integer position** — counting from 0, exactly like a Python list.

With the default index they look identical, which is why people confuse them:

```python
print(students.loc[2])          # the row LABELLED 2
print(students.iloc[2])         # the row at POSITION 2
```

Both give Chen. But the moment your index isn't `0,1,2,…` they part company:

```python
sensors = pd.DataFrame(
    {"temp": [21.5, 23.0, 19.8, 25.2, 22.1],
     "humid": [55, 60, 48, 71, 58]},
    index=["s10", "s20", "s30", "s40", "s50"],      # a custom index
)

print(sensors.loc["s30"])       # temp 19.8 — found by NAME
print(sensors.iloc[2])          # temp 19.8 — found by COUNTING
print(sensors.iloc[0])          # temp 21.5 — the first row
# print(sensors.loc[0])         # 💥 KeyError: there is no row labelled 0
```

And slicing behaves differently in a way that catches everyone once:

```python
print(sensors.loc["s20":"s40"])    # 3 rows — s20, s30, s40. END INCLUDED.
print(sensors.iloc[1:3])           # 2 rows — s20, s30. END EXCLUDED, like a list.
```

| | `.loc` | `.iloc` |
|---|---|---|
| selects by | label | position |
| slice end | **included** | **excluded** |
| `df.loc[2, "name"]` | row labelled 2, column "name" | — |
| `df.iloc[2, 0]` | — | row 3, column 1 |

**Rule of thumb:** use `.loc` almost always, because names survive sorting and filtering while positions do not. Reach for `.iloc` when you genuinely mean "the first row" or "the last three rows".

#### 🔍 Boolean filtering — your Module 5 masks, with names

```python
print(students["score"] > 70)
```

```
0     True
1     True
2    False
3     True
4    False
Name: score, dtype: bool
```

That's a **boolean Series** — exactly the boolean mask from Module 5. Use it to select rows:

```python
print(students.loc[students["score"] > 70])
```

```
    name  grade  house  score  minutes
0  Aarav      7    Red     72       30
1   Bela      8   Blue     90       55
3  Divya      8  Green     83       45
```

Look at the index: `0, 1, 3`. Row 2 is gone and the surviving rows **kept their original labels**. That's the index doing its job — you can always trace a filtered row back to where it came from.

Combine conditions with `&`, `|`, `~` and parentheses — same rules as numpy:

```python
print(students[(students["grade"] == 7) & (students["score"] > 60)])
```

```
    name  grade house  score  minutes
0  Aarav      7   Red     72       30
4  Emeka      7  Blue     61       35
```

⚠️ Same two traps as Module 5, and they bite harder here because the error messages are longer:
- Parenthesise **every** comparison.
- Never `and` / `or` / `not` on a Series — use `&` / `|` / `~`.

---

### 3. Cleaning: `isna`, `fillna`, `dropna`, `astype`, `drop_duplicates`, and `.str` methods

#### The plain-language explanation

Four things go wrong in almost every real table. Learn to spot each one and to repair it *on purpose*.

| Problem | How you spot it | Typical repair |
|---|---|---|
| **Missing values** | `df.isna().sum()` shows a non-zero count | `fillna(...)` or `dropna(...)` |
| **Wrong dtype** | `df.dtypes` says `object` for a number column | `pd.to_numeric(..., errors="coerce")`, then `astype` |
| **Duplicate rows** | `df.duplicated().sum()` is non-zero | `drop_duplicates()` |
| **Inconsistent text** | `df["col"].value_counts()` shows `Red`, `red`, `RED` | `.str.strip().str.lower().str.capitalize()` |

#### 🍕 The analogy

Cleaning data is tidying someone else's kitchen before you cook. Some jars have no labels (missing values). Some labels say "sugar" on a jar of salt (wrong dtype). There are three identical tubs of paprika (duplicates). And the same spice is filed under "chilli", "Chilli", and "CHILLI " with a trailing space (inconsistent text). You can't cook until you sort it out — and you should leave a note saying what you moved, or the next cook will be baffled.

#### 🔍 Our messy table

```python
import pandas as pd

raw = pd.DataFrame({
    "name":  ["Aarav", "Bela", "Chen", "Divya", "Emeka", "Bela", "Farah", "Gita"],
    "age":   [13, 14, None, 13, None, 14, 12, 13],
    "house": ["red", "Red", "BLUE", "blue ", "Green", "Red", "green", "Blue"],
    "score": ["72", "90", "55", "83", "61", "90", "78", "tbd"],
    "club":  ["chess", "music", "chess", "art", "music", "music", "chess", "art"],
})
print(raw)
print(raw.dtypes)
```

```
    name   age  house score   club
0  Aarav  13.0    red    72  chess
1   Bela  14.0    Red    90  music
2   Chen   NaN   BLUE    55  chess
3  Divya  13.0  blue     83    art
4  Emeka   NaN  Green    61  music
5   Bela  14.0    Red    90  music
6  Farah  12.0  green    78  chess
7   Gita  13.0   Blue   tbd    art

name      object
age      float64
house     object
score     object      ← ⚠ should be a number
club      object
```

#### 🔍 Missing values

> **Definition — `NaN`:** "Not a Number" — pandas's marker for a missing value. It is *not* zero, and it is *not* an empty string. `NaN` is contagious: `NaN + 5` is `NaN`.

```python
print(raw.isna().sum())
```

```
name     0
age      2
house    0
score    0
club     0
```

Two missing ages. Notice `score` shows **zero** missing — because `"tbd"` is a perfectly good string. Missingness can hide inside a text column, which is why you check dtypes *and* nulls.

Two repairs, and choosing between them is a judgement call:

```python
# Option A: fill with a stand-in
df["age"] = df["age"].fillna(df["age"].median())

# Option B: throw the row away
df = df.dropna(subset=["age"])
```

| | Fill | Drop |
|---|---|---|
| Keeps every row | ✅ | ❌ loses data |
| Invents facts | ⚠️ yes | ✅ no |
| Good when | the value is unimportant or predictable | the value is the point of the analysis |

**Median vs mean for filling:** the median is safer, because one wildly wrong value (an age typed as 130) drags the mean around and leaves the median alone. That's the Module 3 mean-vs-median argument, doing real work.

⚠️ **Filling is never neutral.** If you fill 3 missing ages with 13, you have created three students who are 13 as far as every later calculation is concerned. That's why the cleaning log exists.

#### 🔍 Wrong dtype

```python
df["score"] = pd.to_numeric(df["score"], errors="coerce")
```

> **Definition — `errors="coerce"`:** convert what you can, and turn anything unconvertible into `NaN` instead of crashing.

`"tbd"` becomes `NaN`. Now the column is `float64` and the missing value is *visible* — which is the whole point. Then you decide what to do with it:

```python
print(df["score"].isna().sum())            # 1
df = df.dropna(subset=["score"])           # you cannot invent a test score
df["score"] = df["score"].astype(int)      # now safe to make it a clean int
```

> ⚠️ A column with any `NaN` in it **cannot** be `int` — that's why it becomes `float64` first. Deal with the `NaN`, then `astype(int)`.

#### 🔍 Duplicate rows

```python
print(raw.duplicated().sum())              # 1
print(raw[raw.duplicated(keep=False)])     # show BOTH copies, not just the second
```

```
   name   age house score   club
1  Bela  14.0   Red    90  music
5  Bela  14.0   Red    90  music
```

```python
df = df.drop_duplicates().reset_index(drop=True)
```

> **Definition — `reset_index(drop=True)`:** renumber the rows 0, 1, 2, … after removing some, and throw the old numbering away. Without `drop=True` the old index becomes a new column, which is almost never what you want.

**Always look at the duplicates before deleting them.** Two students genuinely called Bela with the same score would be a coincidence; the same row entered twice is a data-entry slip. Only you can tell, and `keep=False` shows you both so you can decide.

#### 🔍 Inconsistent text — the `.str` accessor

```python
print(raw["house"].value_counts())
```

```
Red      2
red      1
BLUE     1
blue     1
Green    1
green    1
Blue     1
```

Seven "different" houses. There are three.

> **Definition — `.str` accessor:** the doorway to text methods on a whole column at once. `df["col"].str.lower()` is `lower()` applied to every value, vectorized.

```python
df["house"] = df["house"].str.strip().str.lower().str.capitalize()
print(df["house"].value_counts())
```

```
Blue     3
Red      2
Green    2
```

Read the chain left to right:
- `.str.strip()` removes leading/trailing spaces → `"blue "` becomes `"blue"`
- `.str.lower()` → everything lowercase, so `"BLUE"`, `"Blue"`, `"blue"` all become `"blue"`
- `.str.capitalize()` → first letter up → `"Blue"`

⚠️ `.strip()` first. If you lowercase before stripping you still have `"blue "` ≠ `"blue"`, and the trailing space is invisible when you print it. Whitespace bugs are the ones that make you doubt your own eyes.

---

### 4. Derived columns, `sort_values`, and `value_counts`

#### The plain-language explanation

A **derived column** is a new column computed from existing ones. Because columns are vectorized, you write the formula once.

#### 🍕 The analogy

The spreadsheet you built in Level 1 had a formula column: `=C2/D2`, dragged down the whole sheet. Pandas is the same idea without the dragging — and without the risk that row 47 got missed.

#### 🔍 Tiny concrete example

```python
students["per_min"] = students["score"] / students["minutes"]
print(students.round(3))
```

```
    name  grade  house  score  minutes  per_min
0  Aarav      7    Red     72       30    2.400
1   Bela      8   Blue     90       55    1.636
2   Chen      7    Red     55       20    2.750
3  Divya      8  Green     83       45    1.844
4  Emeka      7   Blue     61       35    1.743
```

Hand-check row 0: 72 / 30 = **2.4** ✔. Row 2: 55 / 20 = **2.75** ✔.

Notice the story flip: Chen has the *lowest* score (55) and the *highest* score-per-minute (2.75). A derived column can completely change what the table says — which is exactly why you should choose it deliberately rather than reporting the first number you see.

**Sorting:**

```python
print(students.sort_values("score", ascending=False))
```

```
    name  grade  house  score  minutes   per_min
1   Bela      8   Blue     90       55  1.636364
3  Divya      8  Green     83       45  1.844444
0  Aarav      7    Red     72       30  2.400000
4  Emeka      7   Blue     61       35  1.742857
2   Chen      7    Red     55       20  2.750000
```

The index is now out of order — `1, 3, 0, 4, 2` — because sorting moved rows and each row **kept its label**. That's a feature. Add `.reset_index(drop=True)` if you want fresh 0,1,2 numbering.

**Counting categories:**

```python
print(students["house"].value_counts())
```

```
Red      2
Blue     2
Green    1
```

That is Module 4's `group_count` in one method call, already sorted biggest first.

**Binning a number into categories:**

```python
students["band"] = pd.cut(students["score"],
                          bins=[0, 60, 80, 100],
                          labels=["low", "mid", "high"])
```

> **Definition — `pd.cut`:** slices a numeric column into named ranges. `bins=[0, 60, 80, 100]` makes three buckets: (0, 60], (60, 80], (80, 100].

Note the brackets: `(0, 60]` means "above 0, up to **and including** 60". A score of exactly 60 is `low`, and 61 is `mid`. Boundary rules like this must be a decision, not an accident.

---

### 5. `groupby` + `agg`, and the cleaning log

#### The plain-language explanation

> **Definition — `groupby`:** split the table into groups by the value in one column, do a calculation on each group, and stack the answers back into a small result table. Split → apply → combine.

#### 🍕 The analogy

You have a stack of exam papers. You sort them into piles by house — that's the *split*. You add up each pile and divide by its size — that's the *apply*. You write the three averages on one sheet — that's the *combine*. `groupby` does all three.

#### 🔍 Tiny concrete example

```python
print(students.groupby("house")["score"].mean())
```

```
house
Blue     75.5
Green    83.0
Red      63.5
Name: score, dtype: float64
```

Hand-check Blue: Bela 90 and Emeka 61 → (90 + 61) / 2 = 151 / 2 = **75.5** ✔
Hand-check Red: Aarav 72 and Chen 55 → 127 / 2 = **63.5** ✔

```
 SPLIT                       APPLY                COMBINE
 ┌────────────────┐
 │ Red:   72, 55  │ ──▶ mean = 63.5 ─┐
 ├────────────────┤                  │        house   score
 │ Blue:  90, 61  │ ──▶ mean = 75.5 ─┼──▶     Blue     75.5
 ├────────────────┤                  │        Green    83.0
 │ Green: 83      │ ──▶ mean = 83.0 ─┘        Red      63.5
 └────────────────┘
```

#### 🔍 Several statistics at once with `agg`

Reporting a mean without a group size is how people mislead themselves. `agg` lets you demand both:

```python
print(students.groupby("grade").agg(
    n=("name", "count"),
    avg=("score", "mean"),
    best=("score", "max"),
))
```

```
       n        avg  best
grade                    
7      3  62.666667    72
8      2  86.500000    90
```

The pattern is `new_column_name=("existing_column", "function")`. Available functions include `"count"`, `"sum"`, `"mean"`, `"median"`, `"min"`, `"max"`, `"std"`, `"nunique"`.

Group by two columns for a cross-tab:

```python
print(students.groupby(["house", "grade"]).size())
```

⚠️ `groupby` only shows combinations that **actually occur**. If no Grade 8 student is in Red, that pair simply won't appear — it is not shown as zero. Read a `groupby` result knowing it's a list of what exists, not a complete grid.

#### 🔍 The cleaning log — the honesty habit

> **Definition — cleaning log:** a written, numbered record of every change you made to the raw data and the reason for each one.

Here is why it isn't optional. When you print `Green: 83.0`, three completely different things could be behind it:

- Green really averages 83.
- Green averages 83 *because you filled two missing scores with the class average*.
- Green averages 83 *because you dropped the one Green student who failed, as their row had a missing age*.

The number looks identical in all three cases. Only the log tells them apart.

A good log entry has three parts: **what you did**, **how many rows it touched**, and **why**.

```
CLEANING LOG
  1. Dropped 1 exact duplicate row — 'Bela' appeared twice with identical
     values; keeping both would double-count her score in every average.
  2. Standardised 'house' from 7 spellings to 3 (strip + lower + capitalize)
     — 'red', 'Red' and 'RED' are one house, and value_counts proved it.
  3. Converted 'score' with to_numeric(errors='coerce') — the column was
     object dtype because one entry was the text 'tbd'.
  4. Dropped 1 row where score was NaN (Gita, 'tbd') — a test score cannot
     be guessed, and this analysis is entirely about scores.
  5. Filled 2 missing ages with the median (13) — median resists outliers.
     WARNING: those 2 ages are now guesses, not measurements.
```

Entry 5 is the important one. It admits a limitation *in the same document as the result*. That habit is the difference between a report and a claim.

---

## 🔍 Worked Example

**The question:** *Clean the messy 8-row table, then report the average score per house — and say honestly how much the cleaning changed the answer.*

We'll do every step with the shape and the numbers shown.

### Step 0 — the raw table

```
    name   age  house score   club
0  Aarav  13.0    red    72  chess
1   Bela  14.0    Red    90  music
2   Chen   NaN   BLUE    55  chess
3  Divya  13.0  blue     83    art
4  Emeka   NaN  Green    61  music
5   Bela  14.0    Red    90  music      ← duplicate of row 1
6  Farah  12.0  green    78  chess
7   Gita  13.0   Blue   tbd    art      ← score is text
```

`shape = (8, 5)`. Dtypes: `age` is `float64` (because of the `None`s), `score` is `object` (because of `"tbd"`).

The three diagnostics, run before touching anything:

```python
print(raw.isna().sum())          # age: 2, everything else: 0
print(raw.duplicated().sum())    # 1
print(raw["house"].value_counts())   # 7 distinct spellings
```

### Step 1 — drop the duplicate

```python
df = raw.drop_duplicates().reset_index(drop=True)
```

`(8, 5)` → **`(7, 5)`**. Row 5 goes; row 1 stays (`drop_duplicates` keeps the first by default).

### Step 2 — standardise `house`

```python
df["house"] = df["house"].str.strip().str.lower().str.capitalize()
```

Trace each value:

| before | after `.strip()` | after `.lower()` | after `.capitalize()` |
|---|---|---|---|
| `"red"` | `"red"` | `"red"` | `"Red"` |
| `"Red"` | `"Red"` | `"red"` | `"Red"` |
| `"BLUE"` | `"BLUE"` | `"blue"` | `"Blue"` |
| `"blue "` | `"blue"` | `"blue"` | `"Blue"` |
| `"Green"` | `"Green"` | `"green"` | `"Green"` |
| `"green"` | `"green"` | `"green"` | `"Green"` |
| `"Blue"` | `"Blue"` | `"blue"` | `"Blue"` |

Seven spellings → three houses: `Blue 3, Red 2, Green 2`. Total 7 ✔ (equals the row count — always check.)

### Step 3 — convert `score` to numbers

```python
df["score"] = pd.to_numeric(df["score"], errors="coerce")
```

```
0    72.0
1    90.0
2    55.0
3    83.0
4    61.0
5    78.0
6     NaN      ← "tbd" became NaN, and now it's VISIBLE
Name: score, dtype: float64
```

The column is `float64`, not `int64`, because it contains a `NaN`. That's forced, not a choice.

### Step 4 — fill the missing ages

```python
med = df["age"].median()      # 13.0
df["age"] = df["age"].fillna(med).astype(int)
```

Known ages after de-duplication: 13, 14, 13, 12, 13 (five values; Chen and Emeka are missing). Sorted: 12, 13, 13, 13, 14. Middle value = **13**. So Chen and Emeka both become 13.

Compare with the mean: (13 + 14 + 13 + 12 + 13) / 5 = 65 / 5 = 13.0 as well — they agree here, which they usually won't.

### Step 5 — drop the row with no score

```python
df = df.dropna(subset=["score"]).reset_index(drop=True)
df["score"] = df["score"].astype(int)
```

`(7, 5)` → **`(6, 5)`**. Gita goes. She had a valid age and house, but no score, and the question is about scores.

⚠️ This is a real decision with a real cost: Gita was in Blue, so Blue's average is now computed from two students instead of three. The log has to say so.

### Step 6 — the clean table

```
    name  age  house  score   club
0  Aarav   13    Red     72  chess
1   Bela   14    Red     90  music
2   Chen   13   Blue     55  chess
3  Divya   13   Blue     83    art
4  Emeka   13  Green     61  music
5  Farah   12  Green     78  chess

name     object
age       int64
house    object
score     int64
club     object
```

Shape journey: **(8, 5) → (7, 5) → (6, 5)**. Two rows lost, and you can name both.

### Step 7 — answer the question

```python
print(df.groupby("house")["score"].mean().round(2))
```

```
house
Blue     69.0
Green    69.5
Red      81.0
```

Hand-check every one:

```
Red   : Aarav 72 + Bela 90 = 162,  162 / 2 = 81.0   ✔
Blue  : Chen 55 + Divya 83 = 138,  138 / 2 = 69.0   ✔
Green : Emeka 61 + Farah 78 = 139, 139 / 2 = 69.5   ✔
```

Cross-check: 2 + 2 + 2 = 6 = `len(df)` ✔

And with `agg` so the group sizes are visible:

```python
print(df.groupby("club").agg(
    n=("name", "count"),
    avg_score=("score", "mean"),
    avg_age=("age", "mean"),
).round(2))
```

```
       n  avg_score  avg_age
club                        
art    1      83.00    13.00
chess  3      68.33    12.67
music  2      75.50    13.50
```

### Step 8 — the honest paragraph

> **Result:** Red averages 81.0, Green 69.5, Blue 69.0.
>
> **But:** every house average rests on exactly **two** students. Blue would have had three, but Gita's score was `"tbd"` and was dropped — and if her eventual score were 90, Blue would jump to 76.0 and the ranking would change. Two of the six ages are filled-in guesses (the median, 13), which affects the club table's `avg_age` but not the score averages. A 6-row table cannot support a sentence like "Red is the strongest house". It can support "in this sample of six, the two Red students scored highest", which is a much smaller and much truer claim.

That paragraph is the deliverable. The numbers were the easy part.

---

## 💻 Hands-On

Create `module06/` and write `clean_club.py`. This runs the whole pipeline on a 14-row table: look, select, clean, derive, group.

```python
"""clean_club.py — inspect, clean, and interrogate a messy school-club table."""

import pandas as pd
import numpy as np

raw = pd.DataFrame({
    "name":  ["Aarav", "Bela", "Chen", "Divya", "Emeka", "Farah", "Gita",
              "Hugo", "Ivy", "Jai", "Bela", "Kira", "Liam", "Maya"],
    "age":   [13, 14, None, 13, None, 12, 13, "14", 12, 13, 14, None, 12, 13],
    "house": ["red", "Red", "BLUE", "blue ", "Green", "green", " Blue",
              "RED", "Blue", "green", "Red", "Red", "blue", "GREEN"],
    "club":  ["chess", "music", "chess", "art", "music", "chess", "art",
              "music", "chess", "art", "music", "chess", "music", "art"],
    "hours": [3.5, 5.0, 2.0, 4.5, 3.0, 6.0, 1.5, 0.5, 4.0, 2.5, 5.0, 3.0, 5.5, 2.0],
    "score": [72, 90, 55, 83, 61, 95, 78, 45, 88, 67, 90, 74, 81, 59],
})

# ============================================================ 1. FIRST LOOK
print("=" * 62); print("1. FIRST LOOK"); print("=" * 62)
print(raw.head())                                  # first 5 rows
print("\nshape:", raw.shape)                       # (14, 6)
print("\ndtypes:\n", raw.dtypes)                   # age is 'object' -> suspicious
print("\nmissing per column:\n", raw.isna().sum()) # 3 missing ages
print("\nexact duplicate rows:", raw.duplicated().sum())
print("\nhouse spellings:", raw["house"].nunique())
print(raw["house"].value_counts())
print("\ndescribe (numeric only):\n", raw.describe())

# ============================================================= 2. SELECTION
print("\n" + "=" * 62); print("2. SELECTION"); print("=" * 62)
print("one column (a Series):\n", raw["score"].head(3))
print("two columns (a DataFrame):\n", raw[["name", "score"]].head(3))
print("loc[3] (label 3):\n", raw.loc[3])
print("iloc[3] (position 3):\n", raw.iloc[3])
print("loc[3, 'name'] ->", raw.loc[3, "name"])
print("iloc[0:3, 0:3]:\n", raw.iloc[0:3, 0:3])     # end EXCLUDED
print("score > 80:\n", raw.loc[raw["score"] > 80, ["name", "score"]])
print("chess AND score>80:\n",
      raw.loc[(raw["club"] == "chess") & (raw["score"] > 80),
              ["name", "club", "score"]])

# ============================================================== 3. CLEANING
print("\n" + "=" * 62); print("3. CLEANING"); print("=" * 62)
log = []                                           # the cleaning log lives here
df = raw.copy()                                    # NEVER clean in place on raw
print("BEFORE shape:", df.shape)

n = len(df)
df = df.drop_duplicates().reset_index(drop=True)
log.append(f"Dropped {n - len(df)} exact duplicate row(s) — same person entered "
           f"twice; keeping both would double their vote in every average.")

before_houses = df["house"].nunique()
df["house"] = df["house"].str.strip().str.lower().str.capitalize()
log.append(f"Standardised 'house' from {before_houses} spellings to "
           f"{df['house'].nunique()} (strip + lower + capitalize) — "
           f"'red' and 'RED' are the same house.")

df["age"] = pd.to_numeric(df["age"], errors="coerce")
log.append("Converted 'age' to numeric with errors='coerce' — it was object "
           "dtype because one age was typed as the text '14'.")

med = df["age"].median()
nmiss = int(df["age"].isna().sum())
df["age"] = df["age"].fillna(med).astype(int)
log.append(f"Filled {nmiss} missing age(s) with the median ({med:.0f}) and cast "
           f"to int — median resists outliers, and ages here are whole numbers. "
           f"NOTE: these {nmiss} rows are now guesses.")

print("AFTER shape:", df.shape)
print(df.dtypes)
print("\nCLEANING LOG")
for i, entry in enumerate(log, 1):
    print(f"  {i}. {entry}")

# ============================== 4. DERIVED COLUMNS, SORTING, COUNTING
print("\n" + "=" * 62); print("4. DERIVED COLUMNS, SORTING, COUNTING")
print("=" * 62)
df["points_per_hour"] = (df["score"] / df["hours"]).round(2)
df["band"] = pd.cut(df["score"], bins=[0, 60, 80, 100],
                    labels=["low", "mid", "high"])
print(df.head())
print("\ntop 5 by score:\n",
      df.sort_values("score", ascending=False)
        .head(5)[["name", "house", "club", "score"]].to_string(index=False))
print("\nband counts:\n", df["band"].value_counts())
print("\nclub counts:\n", df["club"].value_counts())

# =============================================================== 5. GROUPBY
print("\n" + "=" * 62); print("5. GROUPBY"); print("=" * 62)
print("mean score per house:\n", df.groupby("house")["score"].mean().round(2))
print("\nmulti-stat per club:\n", df.groupby("club").agg(
    n=("name", "count"),
    avg_score=("score", "mean"),
    best_score=("score", "max"),
    avg_hours=("hours", "mean"),
).round(2))
print("\nhouse x club counts:\n", df.groupby(["house", "club"]).size())
print("\ncheck: group sizes total", df.groupby("house").size().sum(),
      "== rows", len(df))
```

### Expected output

```
==============================================================
1. FIRST LOOK
==============================================================
    name   age  house   club  hours  score
0  Aarav    13    red  chess    3.5     72
1   Bela    14    Red  music    5.0     90
2   Chen  None   BLUE  chess    2.0     55
3  Divya    13  blue     art    4.5     83
4  Emeka  None  Green  music    3.0     61

shape: (14, 6)

dtypes:
 name      object
age       object
house     object
club      object
hours    float64
score      int64
dtype: object

missing per column:
 name     0
age      3
house    0
club     0
hours    0
score    0
dtype: int64

exact duplicate rows: 1

house spellings: 11
Red      3
green    2
red      1
BLUE     1
blue     1
Green    1
 Blue    1
RED      1
Blue     1
blue     1
GREEN    1
Name: house, dtype: int64

describe (numeric only):
            hours      score
count  14.000000  14.000000
mean    3.428571  74.142857
std     1.639150  15.047909
min     0.500000  45.000000
25%     2.125000  62.500000
50%     3.250000  76.000000
75%     4.875000  86.750000
max     6.000000  95.000000

==============================================================
2. SELECTION
==============================================================
one column (a Series):
 0    72
1    90
2    55
Name: score, dtype: int64
two columns (a DataFrame):
     name  score
0  Aarav     72
1   Bela     90
2   Chen     55
loc[3] (label 3):
 name     Divya
age         13
house    blue 
club       art
hours      4.5
score       83
Name: 3, dtype: object
iloc[3] (position 3):
 name     Divya
age         13
house    blue 
club       art
hours      4.5
score       83
Name: 3, dtype: object
loc[3, 'name'] -> Divya
iloc[0:3, 0:3]:
     name   age house
0  Aarav    13   red
1   Bela    14   Red
2   Chen  None  BLUE
score > 80:
      name  score
1    Bela     90
3   Divya     83
5   Farah     95
8     Ivy     88
10   Bela     90
12   Liam     81
chess AND score>80:
     name   club  score
5  Farah  chess     95
8    Ivy  chess     88

==============================================================
3. CLEANING
==============================================================
BEFORE shape: (14, 6)
AFTER shape: (13, 6)
name      object
age        int64
house     object
club      object
hours    float64
score      int64
dtype: object

CLEANING LOG
  1. Dropped 1 exact duplicate row(s) — same person entered twice; keeping both would double their vote in every average.
  2. Standardised 'house' from 11 spellings to 3 (strip + lower + capitalize) — 'red' and 'RED' are the same house.
  3. Converted 'age' to numeric with errors='coerce' — it was object dtype because one age was typed as the text '14'.
  4. Filled 3 missing age(s) with the median (13) and cast to int — median resists outliers, and ages here are whole numbers. NOTE: these 3 rows are now guesses.

==============================================================
4. DERIVED COLUMNS, SORTING, COUNTING
==============================================================
    name  age  house   club  hours  score  points_per_hour  band
0  Aarav   13    Red  chess    3.5     72            20.57   mid
1   Bela   14    Red  music    5.0     90            18.00  high
2   Chen   13   Blue  chess    2.0     55            27.50   low
3  Divya   13   Blue    art    4.5     83            18.44  high
4  Emeka   13  Green  music    3.0     61            20.33   mid

top 5 by score:
  name house  club  score
Farah Green chess     95
 Bela   Red music     90
  Ivy  Blue chess     88
Divya  Blue   art     83
 Liam  Blue music     81

band counts:
 mid     5
high    5
low     3
Name: band, dtype: int64

club counts:
 chess    5
music    4
art      4
Name: club, dtype: int64

==============================================================
5. GROUPBY
==============================================================
mean score per house:
 house
Blue     77.00
Green    70.50
Red      70.25
Name: score, dtype: float64

multi-stat per club:
        n  avg_score  best_score  avg_hours
club                                      
art    4      71.75          83       2.62
chess  5      76.80          95       3.70
music  4      69.25          90       3.50

house x club counts:
 house  club 
Blue   art      2
       chess    2
       music    1
Green  art      2
       chess    1
       music    1
Red    chess    2
       music    2
dtype: int64

check: group sizes total 13 == rows 13
```

### Five things to notice

1. **`age` printed as `object` dtype, even though most values were plain integers.** One text `"14"` was enough to poison the whole column. That's the single most common real-world data bug, and it's why you print `dtypes` before anything else.
2. **`raw.describe()` skipped `age` entirely.** `describe()` only reports numeric columns. A column silently missing from `describe()` is a hint that its dtype is wrong.
3. **`score > 80` returned index `10` — a duplicate Bela.** We filtered before cleaning, deliberately, to show that dirty data gives dirty answers with total confidence. Clean first, then ask.
4. **`house x club` shows no `Red / art` row.** Not zero — *absent*. `groupby` lists what exists.
5. **`band` counts tie at 5 and 5.** Tie order can differ between pandas versions; the counts won't.

---

## ✍️ Practice

Work in `module06/`. Start every file with `import pandas as pd`.

### 1. [Warm-up] Build and inspect

Build this DataFrame and print `head()`, `shape`, `dtypes`, and `describe()`.

```python
snacks = pd.DataFrame({
    "item":  ["samosa", "idli", "vada pav", "dosa", "poha", "upma"],
    "price": [15, 30, 20, 60, 25, 25],
    "sold":  [120, 85, 200, 45, 60, 30],
    "veg":   [True, True, True, True, True, True],
})
```

Then answer in a comment: which columns appear in `describe()` and which don't, and why?

**Done looks like:** shape `(6, 4)`, `describe()` shows only `price` and `sold`, and your comment explains that `item` is `object` and `veg` is `bool`, so neither is treated as a measurement.

### 2. [Warm-up] `loc` vs `iloc` with a custom index

Build this and demonstrate the difference four ways:

```python
sensors = pd.DataFrame(
    {"temp": [21.5, 23.0, 19.8, 25.2, 22.1],
     "humid": [55, 60, 48, 71, 58]},
    index=["s10", "s20", "s30", "s40", "s50"],
)
```

Print `sensors.loc["s30"]`, `sensors.iloc[2]`, `sensors.loc["s20":"s40"]`, and `sensors.iloc[1:3]`. Then trigger the `KeyError` from `sensors.loc[0]` inside a `try`/`except` and print a message explaining what went wrong.

**Done looks like:** the two slices return **3 rows and 2 rows** respectively, and you can state in one sentence why.

### 3. [Build] Derived column and a ranking

Using `snacks` from Exercise 1: add a `revenue` column (`price × sold`), print the top 3 items by revenue, and separately print all items priced at 25 or under with their revenue. Finish by printing the total revenue.

**Done looks like:** top 3 are vada pav (4000), dosa (2700), idli (2550); the cheap list has 4 items; total revenue is 13300. Check vada pav by hand.

### 4. [Build] Clean a broken cricket table

```python
broken = pd.DataFrame({
    "player": ["Ana", "Ben", "Cy", "Dee", "Ana", "Eve", "Fay"],
    "team":   ["reds", " Reds", "BLUES", "blues", "reds", "Blues", "REDS"],
    "runs":   ["45", "30", None, "78", "45", "12", "60"],
    "overs":  [4.0, 3.5, 4.0, None, 4.0, 2.0, 4.0],
})
```

Clean it: drop duplicates, standardise `team`, convert `runs` to numeric, decide what to do with the missing `runs` and the missing `overs`, and fix the dtypes. Print the before shape, the after shape, and a numbered cleaning log with a **reason** on every line. Finish with mean runs per team.

**Done looks like:** shape goes `(7, 4)` → `(6, 4)` → `(5, 4)`, `team` has exactly 2 values, `runs` is `int64`, and both teams average 45.0 runs. Your log explains why you dropped the missing run total rather than filling it.

### 5. [Stretch] The small-group trap

Use the cleaned 13-row `df` from the Hands-On. Group by **both** `house` and `club` with `agg`, producing `n` (count) and `avg` (mean score). Sort by `avg` descending and print the top 3. Then write a short paragraph: which combination looks best, how many students it's based on, and whether you'd put that number in a school newsletter.

**Done looks like:** the top row is `Green / chess` with `avg = 95.0` and `n = 1`, and your paragraph names the problem out loud.

### 6. [Stretch] Three ways to handle a hole

Take the Hands-On table after de-duplication and text-cleaning but **before** the age fill, so `age` still has 3 `NaN`s. Produce the "average score by age" table three ways: drop the rows, fill with the median, fill with the mean. Print all three, then choose one and defend it in three sentences.

**Done looks like:** all three tables printed with counts; you have noticed that the mean fill (12.9) **invents an age group that does not exist**; and your defence names a specific number that changed.

---

## 🤔 Think Deeper

### 1. You filled 3 missing ages with the median. Whose ages were missing?

*How to reason about it:* the median fill is only fair if the missing values are missing *at random*. Ask what could make a value missing on purpose. If the form asked for a birth date and the students who left it blank were the ones repeating a year, then the missing ages are systematically *higher* than the median — and your fill has quietly pulled the whole distribution younger. Look at the other columns for those rows and see whether they look like a random handful or a pattern. Then decide: is a column with a known bias worse than a column with fewer rows?

### 2. `groupby("house")` prints a clean table of three numbers. What has it hidden?

*How to reason about it:* run `df.groupby("house")["score"].agg(["count", "mean", "min", "max", "std"])` and compare. A mean of 70.5 could be two students on 70 and 71, or one on 45 and one on 96. Ask what decision the number will be used for, then ask whether the spread would change that decision. Then think about who benefits from the summary being clean: a summary that hides variation is often *more persuasive*, and that should make you suspicious rather than pleased.

### 3. The cleaning log lives in your code. Should it travel with the results?

*How to reason about it:* imagine your table is shared as a screenshot in a group chat and then quoted in a school assembly. At which step did the caveats fall off? Consider three options — log in a comment, log printed above every result, log written into a companion file that's saved alongside the CSV — and think about which one survives a screenshot. Then consider the opposite risk: nobody reads a log with 40 entries, so a log that's too long is the same as no log. What's the shortest log that still tells the truth?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `KeyError` from `df["name", "score"]` | You need a **list** of column names inside the brackets | `df[["name", "score"]]` — double brackets |
| A whole numeric column shows as `object` dtype | One value was typed as text (`"14"`, `"tbd"`, `"1,200"`) and poisons the column | `pd.to_numeric(df["col"], errors="coerce")`, then handle the resulting `NaN`s |
| `ValueError: Cannot convert non-finite values (NA or inf) to integer` | You called `.astype(int)` on a column that still has `NaN` | Deal with the `NaN`s first (`fillna` or `dropna`), *then* `astype(int)` |
| `ValueError: The truth value of a Series is ambiguous` | You used `and` / `or` / `if` on a whole Series | Use `&`, `\|`, `~`, and parenthesise each comparison |
| `SettingWithCopyWarning` after filtering | You modified a slice of a DataFrame instead of the DataFrame itself | Make an explicit copy: `sub = df[df["x"] > 5].copy()` before assigning to it |
| `df.dropna()` deleted almost everything | With no arguments it drops any row with a `NaN` in **any** column | Target it: `df.dropna(subset=["score"])` |
| `value_counts()` shows `Red`, `red`, `RED ` as three categories | Case and stray whitespace | `.str.strip().str.lower().str.capitalize()` — strip **first** |
| `.loc["a":"c"]` returned one more row than you expected | `.loc` slices include the end label; `.iloc` excludes it | Know which you're using; prefer `.loc` with explicit labels |
| Filtered rows have a gappy index (0, 1, 3, 7) and later `.iloc` gives the wrong row | Filtering keeps original labels; `.iloc` counts positions | `.reset_index(drop=True)` after filtering, or use `.loc` |
| A group average looks amazing and is based on 1 row | `groupby` reports every group, however tiny | Always `agg` a `count` alongside the mean, and set a minimum group size *before* looking |
| You cleaned `raw` in place and can't get back to the original | No copy was made | `df = raw.copy()` at the top, always |

---

## 🛠️ Mini-Project — Mess Detective

### Goal

Take a deliberately broken **40-row** table, clean it properly, write a real cleaning log, and answer **six** questions with `groupby`.

### The data — type this in

```python
import pandas as pd

rows = [
    ("Aarav Shah",   "13",  "red",    "chess",  "3.5",  72),
    ("Bela Roy",      14,   "Red",    "music",  "5.0",  90),
    ("Chen Wu",      None,  "BLUE",   "chess",  "2.0",  55),
    ("Divya Nair",    13,   "blue ",  "art",    "4.5",  83),
    ("Emeka Obi",    None,  "Green",  "music",  "3.0",  61),
    ("Farah Aziz",    12,   "green",  "chess",  "6.0",  95),
    ("Gita Menon",    13,   " Blue",  "art",    "1.5",  78),
    ("Hugo Silva",    14,   "RED",    "music",  "0.5",  45),
    ("Ivy Chen",      12,   "Blue",   "chess",  "4.0",  88),
    ("Jai Kapoor",   "13",  "green",  "art",    "2.5",  67),
    ("Kira Das",      14,   "Red",    "chess",  "3.0",  74),
    ("Liam Byrne",   None,  "blue",   "music",  "5.5",  81),
    ("Maya Iyer",     12,   "Green",  "art",    "2.0",  59),
    ("Noor Khan",     13,   "red",    "chess",  "4.0",  86),
    ("Omar Haddad",   14,   "Blue",   "music",  "1.0",  52),
    ("Priya Rao",     12,   "GREEN",  "art",    "3.5",  70),
    ("Quinn Reid",    13,   "Red",    "chess",  "2.5",  64),
    ("Rhea Bose",    None,  "blue",   "music",  "4.5",  92),
    ("Sami Aden",     14,   "Green",  "art",    "0.5",  48),
    ("Tara Joshi",   "12",  "Red",    "chess",  "5.0",  97),
    ("Uma Pillai",    13,   "Blue",   "music",  "3.0",  76),
    ("Viraj Sen",     14,   "green ", "art",    "2.0",  63),
    ("Wren Adeyemi",  12,   "Red",    "chess",  "3.5",  80),
    ("Xu Lin",        13,   "BLUE",   "music",  "1.5",  57),
    ("Yara Fadel",   None,  "Green",  "art",    "4.0",  85),
    ("Zane Cooper",   14,   "red",    "chess",  "2.5",  69),
    ("Anika Verma",   12,   "Blue",   "music",  "5.0",  93),
    ("Bruno Costa",   13,   "green",  "art",    "1.0",  50),
    ("Cleo Marks",    14,   "Red",    "chess",  "3.0",  73),
    ("Dev Anand",     12,   "blue",   "music",  "4.5",  89),
    ("Elif Demir",    13,   "Green",  "art",    "2.0",  66),
    ("Finn Walsh",   None,  "RED",    "chess",  "3.5",  79),
    ("Greta Hahn",    14,   "Blue",   "music",  "0.5",  42),
    ("Hana Sato",     12,   "green",  "art",    "5.5",  91),
    ("Bela Roy",      14,   "Red",    "music",  "5.0",  90),
    ("Ismail Toure",  13,   "Red",    "chess",  "2.0",  62),
    ("Jia Park",      12,   "blue",   "music",  "4.0",  84),
    ("Farah Aziz",    12,   "green",  "chess",  "6.0",  95),
    ("Kofi Mensah",   14,   "Green",  "art",    "1.5",  54),
    ("Lena Fischer",  13,   "BLUE",   "chess",  "3.0",  71),
]

raw = pd.DataFrame(rows, columns=["name", "age", "house", "club", "hours", "score"])
```

### The four planted problems

1. Six missing ages (`None`)
2. Three ages typed as text (`"13"` for Aarav, `"13"` for Jai, `"12"` for Tara) — three is plenty to make the whole column `object`
3. Two exact duplicate rows
4. Twelve different spellings of three houses (case + stray spaces)

Plus one that isn't a mistake but needs handling: `hours` is stored as text too.

### Starter steps

**Step 1 — diagnose before you touch anything (20 min).** Print, in this order:

```python
print(raw.shape)                       # (40, 6)
print(raw.dtypes)                      # note which are 'object'
print(raw.isna().sum())                # 6 missing ages
print(raw.duplicated().sum())          # 2
print(raw["house"].nunique())          # 12
print(raw["house"].value_counts())
print(raw["club"].value_counts())
print(raw.describe())
```

Write down what you found *before* fixing anything. You can't log a fix you didn't notice.

**Step 2 — clean, appending to a log as you go (45 min).** Copy first (`df = raw.copy()`). Suggested order — and the order matters, because de-duplicating first means you don't clean rows you're about to delete:

1. `drop_duplicates().reset_index(drop=True)`
2. standardise `house` with `.str.strip().str.lower().str.capitalize()`
3. standardise `club` with `.str.strip().str.lower()`
4. `pd.to_numeric(df["age"], errors="coerce")`
5. fill the missing ages with the **median**, then `.astype(int)`
6. `df["hours"] = df["hours"].astype(float)`

Every step appends a string to `log` saying **what**, **how many rows**, and **why**.

**Step 3 — answer six questions with `groupby` (40 min).**

1. How many students in each house?
2. What is the average score in each club?
3. Per house: count, average score, average hours, best score — in one `agg`.
4. What is the average score at each age?
5. How many students in each house-and-club combination?
6. Add a `points_per_hour` column (`score / hours`) and print the top 5.

**Step 4 — the honest paragraph (15 min).** Pick the answer you find most interesting and write four sentences: what it says, how many rows it's based on, one way your cleaning could have caused it, and what data you'd need to be sure.

### Cross-check values (yours must match)

| Check | Value |
|---|---|
| Raw shape | `(40, 6)` |
| Raw `age` dtype | `object` |
| Missing ages (raw) | `6` |
| Exact duplicates | `2` |
| Distinct house spellings (raw) | `12` |
| Shape after `drop_duplicates` | `(38, 6)` |
| Distinct houses after cleaning | `3` — Blue, Green, Red |
| Age median used for filling | `13.0` |
| Final shape | `(38, 6)` |
| Q1 students per house | Blue 14, Red 12, Green 12 (sums to 38 ✔) |
| Q2 avg score per club | art 67.83, chess 76.07, music 71.83 |
| Q3 avg score per house | Blue 74.36, Green 67.42, Red 74.25 |
| Q4 avg score by age | 12 → 84.60, 13 → 71.39, 14 → 61.00 |
| Q5 combinations that exist | 8 of the 9 possible — there is **no** Red/art |
| Q6 top points_per_hour | Sami Aden, 96.0 (48 ÷ 0.5) |
| Overall mean score | `72.13` |

### The trap hidden in Q4 — you must find this

Before you fill the missing ages, the average score for the 12 students with a *known* age of 13 is **69.33**. After you fill six missing ages with the median (13), the age-13 group has 18 students and its average becomes **71.39**.

**Your fill changed the answer to Q4 by 2 points, and Q4 is a question about age.** That is not a bug — it is what filling means. Your log must say so, and your honest paragraph should mention it. The general rule this teaches: *never fill a column with a guess and then make that column the subject of your analysis.*

### Success criteria checklist

- [ ] Before/after shape printed: `(40, 6)` → `(38, 6)`
- [ ] All four planted problems found and named before any fix
- [ ] A numbered cleaning log with at least 6 entries, **each with a reason**
- [ ] Final `dtypes`: `age` is `int64`, `hours` is `float64`, `score` is `int64`
- [ ] `df["house"].nunique() == 3` and `df["club"].nunique() == 3`
- [ ] All six questions answered, matching the cross-check table
- [ ] One answer verified **by hand** — write the arithmetic in a comment
- [ ] A printed cross-check: group sizes sum to `len(df)`
- [ ] The Q4 fill-effect noted in the log and the paragraph
- [ ] A `# WHOSE DATA IS THIS?` comment: these are named children with scores attached — who should be allowed to see this file, and what would you delete before sharing it?

### 🚀 Level it up

Write a reusable function:

```python
def clean_report(raw, text_cols, numeric_cols, fill_strategy="median"):
    """Clean a DataFrame and return (clean_df, log_list)."""
```

It should de-duplicate, standardise every column named in `text_cols`, coerce every column in `numeric_cols`, fill according to `fill_strategy` (`"median"`, `"mean"`, or `"drop"`), and build the log automatically. Then run your 40-row table through all three strategies and print how the answer to Q4 changes across them, in one comparison table.

That function is the beginning of a real data-cleaning toolkit — and you'll want it for the Level 2 capstone.

---

## 🔑 Key Takeaways

- A **DataFrame** is a table where columns have names and dtypes, and rows have index labels. It's Module 4's list-of-dicts with Module 5's vectorized speed.
- Run four commands on every new table before anything else: `head()`, `shape`, `dtypes`, `isna().sum()`. A numeric column showing `object` dtype is your loudest alarm.
- `.loc` selects by **label** and includes the end of a slice; `.iloc` selects by **position** and excludes it. Prefer `.loc`.
- Boolean filtering is Module 5's mask with names attached: `df[(df["a"] > 1) & (df["b"] == "x")]` — parentheses on every comparison, `&` never `and`.
- The four standard messes are **missing values, wrong dtypes, duplicate rows, and inconsistent text**, and each has a standard repair: `fillna`/`dropna`, `to_numeric`+`astype`, `drop_duplicates`, `.str.strip().str.lower()`.
- **Every cleaning decision changes an answer.** Filling ages with the median moved the age-13 average by 2 points in a table you cleaned yourself.
- `groupby(col)[value].agg(...)` is split-apply-combine, and you should **always** aggregate a `count` alongside the mean so you can see when a group is too small to talk about.
- The **cleaning log** is part of the result, not a note to yourself. A number without its log is a claim without evidence.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| DataFrame | A table with named columns and labelled rows | `pd.DataFrame({"a": [1,2]})` |
| Series | One column of a DataFrame, with its labels | `df["score"]` |
| index | The row labels down the left side | `0, 1, 2` or `"s10", "s20"` |
| dtype | The type of a whole column | `int64`, `float64`, `object`, `bool` |
| `object` dtype | Pandas for "text (or a mixed mess)" | a number column showing `object` = trouble |
| `head()` | Show the first few rows | `df.head(3)` |
| `info()` | Column list with dtypes and non-null counts | spots missing values fast |
| `describe()` | Count/mean/min/quartiles/max for numeric columns | skips text columns |
| `.loc[]` | Select by **name** (index label, column name) | `df.loc[3, "name"]` |
| `.iloc[]` | Select by **position**, counting from 0 | `df.iloc[3, 0]` |
| boolean filtering | Keep rows where a condition is True | `df[df["score"] > 80]` |
| `NaN` | Pandas's marker for a missing value | not 0, not `""` |
| `isna()` | True where a value is missing | `df.isna().sum()` |
| `fillna()` | Replace missing values with something | `df["age"].fillna(13)` |
| `dropna()` | Delete rows that have missing values | `df.dropna(subset=["score"])` |
| `astype()` | Change a column's type | `df["age"].astype(int)` |
| `to_numeric(errors="coerce")` | Turn text into numbers; unconvertible → `NaN` | fixes `"12"` and flags `"tbd"` |
| `drop_duplicates()` | Remove identical rows | keeps the first by default |
| `.str` accessor | Text methods applied to a whole column | `df["h"].str.lower()` |
| derived column | A new column computed from others | `df["rev"] = df["p"] * df["n"]` |
| `sort_values()` | Reorder rows by a column | `df.sort_values("score", ascending=False)` |
| `value_counts()` | Count how often each value appears | Module 4's `group_count`, built in |
| `pd.cut()` | Slice numbers into named bands | `low` / `mid` / `high` |
| `groupby()` | Split into groups, calculate, recombine | `df.groupby("house")["score"].mean()` |
| `agg()` | Several statistics per group at once | `agg(n=("name","count"), avg=("score","mean"))` |
| cleaning log | A written record of every change and its reason | ships with the results |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Build and inspect

```python
import pandas as pd

snacks = pd.DataFrame({
    "item":  ["samosa", "idli", "vada pav", "dosa", "poha", "upma"],
    "price": [15, 30, 20, 60, 25, 25],
    "sold":  [120, 85, 200, 45, 60, 30],
    "veg":   [True, True, True, True, True, True],
})

print(snacks.head())
print("shape:", snacks.shape)
print(snacks.dtypes)
print(snacks.describe())

# describe() shows only 'price' and 'sold'.
# 'item' is object dtype (text) -- a mean of "samosa" is meaningless.
# 'veg'  is bool dtype -- pandas could average it (it'd give 1.0) but by default
#        treats it as a category, not a measurement. And every value is True,
#        so the column carries no information at all: it can't distinguish any
#        two rows. In a real project you'd drop it.
```

Output:

```
       item  price  sold   veg
0    samosa     15   120  True
1      idli     30    85  True
2  vada pav     20   200  True
3      dosa     60    45  True
4      poha     25    60  True
shape: (6, 4)
item     object
price     int64
sold      int64
veg        bool
dtype: object
           price        sold
count   6.000000    6.000000
mean   29.166667   90.000000
std    15.942605   62.529993
min    15.000000   30.000000
25%    21.250000   48.750000
50%    25.000000   72.500000
75%    28.750000  111.250000
max    60.000000  200.000000
```

**Read the `describe()` critically:** mean price is 29.17 but the median (the `50%` row) is 25. The mean is dragged up by the dosa at 60. That is the Module 3 mean-vs-median lesson visible in one glance — and it's why `describe()` gives you both.

---

### 2. [Warm-up] `loc` vs `iloc` with a custom index

```python
import pandas as pd

sensors = pd.DataFrame(
    {"temp": [21.5, 23.0, 19.8, 25.2, 22.1],
     "humid": [55, 60, 48, 71, 58]},
    index=["s10", "s20", "s30", "s40", "s50"],
)
print(sensors)

print("\nloc['s30'] -- by NAME:\n", sensors.loc["s30"])
print("\niloc[2] -- by POSITION:\n", sensors.iloc[2])

print("\nloc['s20':'s40'] -- 3 rows, END INCLUDED:\n", sensors.loc["s20":"s40"])
print("\niloc[1:3] -- 2 rows, END EXCLUDED:\n", sensors.iloc[1:3])

try:
    sensors.loc[0]
except KeyError as e:
    print("\nKeyError caught:", e)
    print("Explanation: .loc looks for an index LABEL equal to 0. This "
          "DataFrame's labels are the strings 's10'...'s50', so there is no "
          "row named 0. To get the first row by position, use .iloc[0].")
```

Output (abridged):

```
     temp  humid
s10  21.5     55
s20  23.0     60
s30  19.8     48
s40  25.2     71
s50  22.1     58

loc['s30'] -- by NAME:
 temp     19.8
humid    48.0
Name: s30, dtype: float64

iloc[2] -- by POSITION:
 temp     19.8
humid    48.0
Name: s30, dtype: float64

loc['s20':'s40'] -- 3 rows, END INCLUDED:
      temp  humid
s20  23.0     60
s30  19.8     48
s40  25.2     71

iloc[1:3] -- 2 rows, END EXCLUDED:
      temp  humid
s20  23.0     60
s30  19.8     48
```

**Why the slice lengths differ:** `iloc` copies Python's list rule — `[1:3]` means positions 1 and 2, stopping *before* 3. `loc` slices by label, and pandas can't know what comes "just before" the label `"s40"`, so it includes it. The rule is worth memorising because a silent off-by-one row is invisible in a big table.

**Also worth noticing:** the single-row results have dtype `float64` for both `temp` and `humid`, even though `humid` is `int64` in the DataFrame. Pulling one row across mixed columns forces everything to a common type — here, float. That's why you should slice columns, not rows, when you care about dtypes.

---

### 3. [Build] Derived column and a ranking

```python
snacks["revenue"] = snacks["price"] * snacks["sold"]     # vectorized, all 6 at once

print("top 3 by revenue:")
print(snacks.sort_values("revenue", ascending=False)
            .head(3)[["item", "price", "sold", "revenue"]]
            .to_string(index=False))

print("\npriced 25 or under:")
print(snacks.loc[snacks["price"] <= 25, ["item", "price", "revenue"]]
            .to_string(index=False))

print("\ntotal revenue:", snacks["revenue"].sum())
```

Output:

```
top 3 by revenue:
    item  price  sold  revenue
vada pav     20   200     4000
    dosa     60    45     2700
    idli     30    85     2550

priced 25 or under:
    item  price  revenue
  samosa     15     1800
vada pav     20     4000
    poha     25     1500
    upma     25      750

total revenue: 13300
```

**Hand check — vada pav:** 20 × 200 = **4000** ✔
**Hand check — total:** 1800 + 2550 + 4000 + 2700 + 1500 + 750 = 13300 ✔

**The interesting bit:** the dosa is by far the most expensive item (60) and sells the least (45), yet it's second in revenue. The vada pav is nearly the cheapest and wins outright on volume. Sorting by `price` and sorting by `revenue` give almost opposite answers, and a derived column is what let you see it. Choosing which column to rank by *is* the analysis.

⚠️ `snacks["price"] <= 25` includes both 25s. If you'd meant "under 25" you'd write `< 25` and get two items instead of four — a 50% change in the answer from one character.

---

### 4. [Build] Clean a broken cricket table

```python
import pandas as pd

broken = pd.DataFrame({
    "player": ["Ana", "Ben", "Cy", "Dee", "Ana", "Eve", "Fay"],
    "team":   ["reds", " Reds", "BLUES", "blues", "reds", "Blues", "REDS"],
    "runs":   ["45", "30", None, "78", "45", "12", "60"],
    "overs":  [4.0, 3.5, 4.0, None, 4.0, 2.0, 4.0],
})

print("BEFORE shape:", broken.shape)          # (7, 4)
print(broken.dtypes)                          # runs is object
print("missing:\n", broken.isna().sum())      # runs 1, overs 1
print("duplicates:", broken.duplicated().sum())   # 1

log = []
d = broken.copy()

n = len(d)
d = d.drop_duplicates().reset_index(drop=True)
log.append(f"Dropped {n - len(d)} exact duplicate row — 'Ana' appears twice "
           f"with identical team, runs and overs; a second identical row is a "
           f"data-entry slip, not a second innings.")

before = d["team"].nunique()
d["team"] = d["team"].str.strip().str.lower().str.capitalize()
log.append(f"Standardised 'team' from {before} spellings to {d['team'].nunique()} "
           f"(strip + lower + capitalize) — ' Reds', 'reds' and 'REDS' are one team, "
           f"and the leading space in ' Reds' was invisible when printed.")

d["runs"] = pd.to_numeric(d["runs"], errors="coerce")
log.append("Converted 'runs' with to_numeric(errors='coerce') — the column was "
           "object dtype because one value was None.")

n = len(d)
d = d.dropna(subset=["runs"]).reset_index(drop=True)
log.append(f"Dropped {n - len(d)} row with a missing 'runs' value (Cy) — runs "
           f"scored is the whole subject of this analysis, so a guessed value "
           f"would be inventing the answer. Dropping loses one row; filling "
           f"would corrupt every team average.")

d["runs"] = d["runs"].astype(int)
log.append("Cast 'runs' to int — no NaNs remain and runs are whole numbers.")

med = d["overs"].median()
nmiss = int(d["overs"].isna().sum())
d["overs"] = d["overs"].fillna(med)
log.append(f"Filled {nmiss} missing 'overs' with the median ({med}) — overs "
           f"bowled is background context here, not the subject, and every other "
           f"player bowled between 2 and 4, so the median is a safe stand-in. "
           f"NOTE: Dee's overs figure is now a guess.")

print("\nAFTER shape:", d.shape)              # (5, 4)
print(d)
print(d.dtypes)

print("\nCLEANING LOG")
for i, entry in enumerate(log, 1):
    print(f"  {i}. {entry}")

print("\nmean runs per team:")
print(d.groupby("team")["runs"].mean())
print("\ngroup sizes:", d.groupby("team").size().to_dict(),
      "-> total", d.groupby("team").size().sum(), "== rows", len(d))
```

Output (key parts):

```
BEFORE shape: (7, 4)
AFTER shape: (5, 4)
  player   team  runs  overs
0    Ana   Reds    45   4.00
1    Ben   Reds    30   3.50
2    Dee  Blues    78   3.75
3    Eve  Blues    12   2.00
4    Fay   Reds    60   4.00

player     object
team       object
runs        int64
overs     float64

mean runs per team:
team
Blues    45.0
Reds     45.0

group sizes: {'Blues': 2, 'Reds': 3} -> total 5 == rows 5
```

**Shape journey:** `(7, 4)` → `(6, 4)` after de-duplication → `(5, 4)` after dropping Cy.

**Hand check — Reds:** 45 + 30 + 60 = 135, and 135 / 3 = **45.0** ✔
**Hand check — Blues:** 78 + 12 = 90, and 90 / 2 = **45.0** ✔

**The overs median is 3.75, not 4.0.** After dropping Cy the remaining overs are 4.0, 3.5, NaN, 2.0, 4.0 — four known values: 2.0, 3.5, 4.0, 4.0. With an even count the median is the average of the middle two: (3.5 + 4.0) / 2 = **3.75** ✔. Notice the median depends on which rows you already dropped, so **the order of your cleaning steps changes the numbers you fill with.** Write the order down.

**Why drop `runs` but fill `overs`:** runs is what the analysis is *about* — guessing it would be manufacturing the result. Overs is context; a wrong-by-half-an-over value won't change any conclusion. That asymmetry is the actual skill here, not the syntax.

**And the punchline:** both teams average exactly 45.0. Identical means, totally different stories — Reds are 45/30/60 (tight), Blues are 78/12 (one brilliant innings and one collapse). A mean with no spread beside it hid that completely. Add `.agg(["count", "mean", "min", "max"])` and it reappears.

---

### 5. [Stretch] The small-group trap

```python
combo = (df.groupby(["house", "club"])
           .agg(n=("name", "count"), avg=("score", "mean"))
           .round(2))
print(combo.to_string())
print("\ntop 3 by average:")
print(combo.sort_values("avg", ascending=False).head(3).to_string())
```

Output:

```
             n   avg
house club          
Blue  art    2  80.5
      chess  2  71.5
      music  1  81.0
Green art    2  63.0
      chess  1  95.0
      music  1  61.0
Red   chess  2  73.0
      music  2  67.5

top 3 by average:
             n   avg
house club          
Green chess  1  95.0
Blue  music  1  81.0
      art    2  80.5
```

**The paragraph:**

> The best-performing combination looks like **Green chess, averaging 95.0** — comfortably ahead of everything else. It is based on **one student**. That isn't an average; it is Farah's score with a mean sign in front of it. The second place, Blue music at 81.0, is also a single student (Liam). The first row in this table based on more than one person is Blue art at 80.5, from two students.
>
> I would not put "Green chess averages 95" in a newsletter. It reads as a statement about a group and a club programme, when it is a statement about one child — who is also now identifiable to anyone who knows which Green student plays chess. Two harms in one line: it's statistically empty, and it's a privacy leak dressed as a statistic.
>
> The fix is a rule set **in advance**: report no group with fewer than 5 members, and always print `n` next to every mean. Deciding the threshold after seeing the results lets you pick whichever threshold flatters the story you already wanted.

**Note the mechanic that made this visible:** `agg(n=("name", "count"), ...)`. If you had written `df.groupby(["house","club"])["score"].mean()` you would have got 95.0 with no `n` beside it, and nothing on screen would have warned you. That's the whole argument for always aggregating a count.

---

### 6. [Stretch] Three ways to handle a hole

```python
import pandas as pd

# start from the Hands-On table, de-duplicated and text-cleaned,
# but with age still holding NaNs
work = raw.drop_duplicates().reset_index(drop=True)
work["house"] = work["house"].str.strip().str.lower().str.capitalize()
work["age"] = pd.to_numeric(work["age"], errors="coerce")

print("rows:", len(work), " missing ages:", int(work["age"].isna().sum()))
print("mean age:", round(work["age"].mean(), 2), " median age:", work["age"].median())

strategies = {
    "A) DROP the rows":   work.dropna(subset=["age"]),
    "B) FILL with median": work.assign(age=work["age"].fillna(work["age"].median())),
    "C) FILL with mean":   work.assign(age=work["age"].fillna(work["age"].mean())),
}

for label, table in strategies.items():
    print("\n" + label, f"  (rows = {len(table)})")
    print(table.groupby("age")["score"].agg(["count", "mean"]).round(2).to_string())
```

Output:

```
rows: 13  missing ages: 3
mean age: 12.9  median age: 13.0

A) DROP the rows   (rows = 10)
      count  mean
age              
12.0      3  88.0
13.0      5  71.8
14.0      2  67.5

B) FILL with median   (rows = 13)
      count   mean
age               
12.0      3  88.00
13.0      8  68.62
14.0      2  67.50

C) FILL with mean   (rows = 13)
      count   mean
age               
12.0      3  88.00
12.9      3  63.33
13.0      5  71.80
14.0      2  67.50
```

**Three completely different tables from the same data.** Look at what each one did:

| Strategy | Rows kept | Age-13 average | What it broke |
|---|---|---|---|
| A) Drop | 10 of 13 | **71.80** | Threw away 3 students, 23% of the table |
| B) Fill median | 13 | **68.62** | Moved age-13's average by 3.18 points |
| C) Fill mean | 13 | 71.80 (unchanged) | **Invented an age group: 12.9** |

**Strategy C is the disqualifying one.** No student is 12.9 years old. The mean fill created a fourth row in the age table that corresponds to no real category, and it happens to have the lowest average of all (63.33) purely because those three particular students scored 55, 61 and 74. Anyone reading that table would assume "12.9" is a real age band. Mean-filling is fine for a continuous measurement like height or temperature; it is wrong for a value that only comes in whole steps, because it produces categories that cannot exist.

**My choice, defended in three sentences:**

> I would use **A, drop the rows**, but only for questions that are *about* age. The three missing ages are 23% of a 13-row table, which hurts — but strategy B silently moved the age-13 average from 71.80 to 68.62, a 3.18-point shift that is entirely an artefact of my own fill, in the one column the question is asking about. For questions that are *not* about age — average score by house, say — I would keep strategy B, because there I want all 13 rows and the age column is only along for the ride.

That last sentence is the real lesson: **the right way to handle a missing value depends on the question you're about to ask.** There is no single "cleaned" version of a dataset. There is a version cleaned *for a purpose*, and the log is where you say which purpose.

</details>

---

[⬅ Previous](module-05-numpy-arrays.md) · [Level 2 Home](README.md) · [Next ➡](module-07-visualizing-data.md)
