# 📓 Level 2 Glossary — Every Word, Alphabetized

**Level 2 · Reference · Prereqs: none — use this any time a word stops making sense**

[Level 2 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 1 Glossary](../level-1-explorer/glossary.md)

---

## How to use this page

Every technical term introduced anywhere in Level 2 is here — **217 of them** — with a plain-English definition and the actual example from the course. The **Module** column tells you where to go for the full explanation:

| Tag | Where |
|---|---|
| `M1`–`M9` | That module file, e.g. [`module-05-numpy-arrays.md`](module-05-numpy-arrays.md) |
| `SET` | The setup section of the [level README](README.md) |
| `CAP` | The [capstone](capstone.md) |

**Jump to a letter:**
[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x) · [Y](#y) · [Z](#z)

> ⚠️ **A word on `code font`.** Terms written like `this` are things you literally type. Terms written like *this* are ideas. If you can't type it, it's an idea; if you can, it's a spelling.

---

## A

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Accumulator** | A variable you keep adding to as a loop runs, so it ends up holding the total | `total += score` inside the grade calculator loop | M2 |
| **Accuracy** | The fraction of predictions that were right | 35 correct out of 36 test wines = 0.9722 | M8 |
| **`agg()`** | Compute several statistics per group at once | `agg(n=("name","count"), avg=("score","mean"))` | M6 |
| **Aggregate** | Squash many numbers into one | `sum`, `mean`, `min`, `max`, `std` | M5 |
| **`and`** | True only when both sides are true | `age >= 13 and is_fit` | M2 |
| **`append()`** | Add one item to the end of a list | `scores.append(50)` | M3 |
| **`arange()`** | Build an array counting from start to stop, taking a **step** you choose | `np.arange(0, 10, 2)` → `[0 2 4 6 8]` | M5 |
| **`argmax()` / `argmin()`** | The **position** of the biggest / smallest value, not the value itself | `np.array([9,3,7]).argmin()` → `1` | M5 |
| **Argument** | The real value you hand over when you call a function | `greet("Anu")` — `"Anu"` is the argument | M3 |
| **Array (`ndarray`)** | A grid of numbers, all the same type, stored side by side in memory so maths on them is fast | `np.array([[1,2],[3,4]])` | M5 |
| **`assert`** | A line that claims something must be true and crashes if it isn't — a test you write inline | `assert mean([2,4]) == 3.0` | M3 |
| **Assignment** | Putting a value into a name, with `=` | `total = pizzas * price` | M1 |
| **`astype()`** | Change a whole column's type | `df["age"].astype(int)` | M6 |
| **Augmented assignment** | `+=`, `-=`, `*=` — update a variable from its own current value | `count += 1` | M2 |
| **Axes** | One drawing box inside a figure, with its own x-axis, y-axis and title | The left panel of your lie-and-fix pair | M7 |
| **Axis** | A direction through an array: `0` goes down the rows, `1` goes across the columns | `scores.mean(axis=1)` → one average per student | M5 |

---

## B

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Bar chart** | One rectangle per category; taller means bigger. Must start at zero. | Mean score for Blue, Red and Green | M7 |
| **Baseline** | The score of the laziest possible model — what you must beat before your model means anything | Always guessing the mean gives MAE 9.41 minutes | M8, M9 |
| **Bin** | One of the ranges a histogram counts into | The `[70, 80)` bin holds 8 students | M7 |
| **Block** | Lines that belong together, marked by matching indentation | The indented lines under an `if` | M2 |
| **`bool` (boolean)** | A value that is exactly `True` or `False`, nothing else | `is_captain = False` | M1, M2 |
| **Boolean filtering** | Keeping only the DataFrame rows where a condition is `True` | `df[df["score"] > 80]` | M6 |
| **Boolean mask** | A `True`/`False` array used to pick elements out of another array | `temps[temps > 30]` → `[33 35]` | M5 |
| **Box plot** | A five-number summary drawn as a box with whiskers — shows spread, not just the middle | Score spread for art, chess and music | M7 |
| **`break`** | Leave the whole loop immediately | Stop searching at the first match | M2 |
| **Broadcasting** | numpy stretching a smaller array to fit a bigger one, so shapes that don't match can still do maths together | `scores + [0, 5, 0, 10]` adds a per-test bonus to every row | M5 |

---

## C

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Caption** | One sentence under a chart saying what it *means*, not what it shows | "Blue and Red are tied; Green is 7 points lower." | M7 |
| **Cast** | See **Type conversion** | `int("12")` → `12` | M1 |
| **Chained comparison** | Writing a range the way maths does | `60 <= mark < 75` | M2 |
| **Cherry-picking** | Showing only the slice of data that supports your point | Weeks 8–10 of a 12-week rise | M7 |
| **Classification** | Predicting which **category** something belongs to, from a fixed list | Wine class 0, 1 or 2; spam or not spam | M8, M9 |
| **Cleaning log** | A numbered written record of every change you made to the data, **with a reason for each** | "5. Dropped 4 rows with no target — you can't train on a row whose answer is unknown." | M6, CAP |
| **Coefficient** | The slope belonging to one particular feature in a linear model | `−0.377` for `age_years` | M9 |
| **Comment** | A note for humans that Python ignores, starting with `#` | `# convert to minutes` | M1 |
| **Comparison operator** | A symbol that asks a yes/no question about two values: `==`, `!=`, `<`, `<=`, `>`, `>=` | `age >= 13` | M2 |
| **Complexity dial** | The setting that controls how flexible a model is allowed to be | `max_depth` for a tree; `k` for kNN | M9 |
| **Concatenation** | Joining two strings end to end with `+` | `"pi" + "zza"` → `"pizza"` | M1 |
| **Condition** | The boolean expression an `if` or `while` checks | `mark >= 35` | M2 |
| **Confounder** | A hidden third thing that causes both of the things you measured | Hot weather causes both ice-cream sales and swimming | M7 |
| **Confusion matrix** | A grid showing exactly which classes got mixed up with which | 4 class-1 wines predicted as class 2 | M8 |
| **`continue`** | Skip the rest of this pass through the loop and go to the next one | Ignore a bad input row and carry on | M2 |
| **Correlation (`r`)** | A number from −1 to +1 for how strongly two things move together. **Not** causation. | `r = 0.93` for study hours vs score | M7 |
| **Counter** | An accumulator that counts how many times something happened | `passes += 1` | M2 |
| **Counting dictionary** | The `counts[v] = counts.get(v, 0) + 1` pattern for tallying values | Builds `{'pop': 3, 'rock': 2, 'folk': 1}` | M4 |
| **CSV** | Comma-Separated Values: a plain-text table — a header line, then one line per row | `title,artist,genre` then `Blue Lights,Nova,pop` | M4 |
| **`csv.DictReader`** | Reads CSV lines back as dictionaries — **every value comes back as text** | `{'plays': '120'}`, not `{'plays': 120}` | M4 |
| **`csv.DictWriter`** | Writes a list of dictionaries out as CSV lines | `writer.writerows(songs)` | M4 |

---

## D

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Data card** | A written page saying what the data is, how much, who collected it, when, with whose permission, and what is **not** in it | The capstone's Milestone 1 template | CAP |
| **DataFrame** | A table with named columns and labelled rows — a spreadsheet you can program | `pd.DataFrame({"name": [...], "score": [...]})` | M6 |
| **Decision tree** | A flowchart of yes/no questions that the model wrote for itself | "petal width ≤ 0.8? → setosa" | M9 |
| **Default value** | A value a parameter takes when the caller doesn't supply one | `def f(price, tax=18):` | M3 |
| **Define vs call** | Writing the recipe vs actually cooking it | `def greet():` vs `greet()` | M3 |
| **Depth** | How many questions deep a decision tree is allowed to go | `max_depth=5` gave 30 leaves | M9 |
| **Derived column** | A new column computed from existing ones | `df["revenue"] = df["price"] * df["n"]` | M6 |
| **`describe()`** | Count, mean, min, quartiles and max for every numeric column | Skips text columns entirely | M6 |
| **Dictionary (`dict`)** | A box of labelled slots — you get things out by **name**, not by counting | `{"name": "Ishaan", "runs": 103}` | M4 |
| **Distribution** | The whole shape of a pile of values — where they cluster, how wide, how many peaks | "Wide, flat, no single peak, 42 to 97" | M7 |
| **Docstring** | A short string at the top of a function explaining what it does | `"""Return the mean of a list of numbers."""` | M3 |
| **Dot product** | Multiply two vectors position by position, then add it all up | `[1,2,3] @ [4,5,6]` → `32` | M5 |
| **Drift** | A model getting worse over time because the world moved on from the data it learned on | Scoring a frozen model on 30 rows collected three weeks later | CAP |
| **`drop_duplicates()`** | Remove identical rows, keeping the first by default | Removed 3 rows logged twice by a phone re-sync | M6 |
| **`dropna()`** | Delete rows that have missing values | `df.dropna(subset=["score"])` | M6 |
| **`dtype`** | The one data type shared by every element of an array, or every value in a column | `int64`, `float64`, `object`, `bool` | M5, M6 |
| **`DummyRegressor` / `DummyClassifier`** | Deliberately stupid models that give you your baseline | `DummyRegressor(strategy="mean")` | M9 |

---

## E

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Elementwise** | Doing an operation position by position, independently | `[1,2] * [3,4]` → `[3,8]` | M5 |
| **`enumerate()`** | Loop that hands you the position **and** the item together | `for i, s in enumerate(scores):` | M3 |
| **Euclidean distance** | Straight-line distance: square the differences, add them, take the square root | `√(3² + 4²) = 5` | M5, M8 |
| **`export_text()`** | Print a decision tree's splits as readable indented text | Turns the tree into if/then rules you can read aloud | M9 |
| **Extrapolation** | Predicting outside the range of data you actually have | 20 study hours → a predicted score of 158.9 | M9 |

---

## F

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **f-string** | A string with an `f` in front, where `{}` gets filled in with values | `f"Score: {runs}"` | M1 |
| **Feature** | One measurement you make about each example — one column of `X` | A wine's `proline` value | M8 |
| **Feature engineering** | Inventing a new, more useful feature out of the ones you already have | `minutes_per_km`, `is_weekend`, `days_since_last` | CAP |
| **`feature_importances_`** | A tree's own report of which features it leaned on most | Compare it against your guess made beforehand | M9 |
| **Feature matrix (`X`)** | The table of features: one row per example, one column per measurement | Shape `(178, 13)` for the wine dataset | M8 |
| **Figure** | The whole picture that gets saved to a file; it can hold several axes | An 8×4.5-inch PNG holding your line chart | M7 |
| **`fillna()`** | Replace missing values with something | `df["age"].fillna(13)` | M6 |
| **Filter** | Keep only the rows that pass a test | `filter_by(songs, "genre", "pop")` → 3 rows | M4 |
| **`fit`** | Show a model the training data so it can learn from it | `model.fit(X_train, y_train)` | M8 |
| **Flag** | A boolean variable used to remember that something happened | `won = True` | M2 |
| **`float`** | A number with a decimal point | `3.2`; and `7 / 2` is always a float | M1 |
| **Floor division (`//`)** | Division that throws the fraction away | `7 // 2` → `3` | M1 |
| **`for` loop** | Repeat once per item, a known number of times | `for i in range(10):` | M2 |
| **Format spec** | The bit after `:` inside f-string braces that controls how a number looks | `{x:.2f}`, `{n:,}`, `{p:.1%}` | M1 |
| **Function** | A named block of code you can run whenever you want, by writing its name and `()` | `print("hi")`, `def mean(numbers):` | M1, M3 |

---

## G

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`.get()`** | Polite asking on a dictionary — returns a fallback instead of crashing | `player.get("age", 0)` → `0` | M4 |
| **`get_dummies()`** | Turn one text column into one 0/1 column per value — see **One-hot encoding** | `mode` becomes `mode_walk`, `mode_cycle`, `mode_bus` | CAP |
| **Gini impurity** | How mixed a group is; `0` means all one class | 4 fails + 6 passes → 0.48 | M9 |
| **Global variable** | A variable created outside every function — readable inside, but don't assign to it there | A constant like `TAX_RATE = 18` | M3 |
| **Group and count** | Sort rows into buckets by one column and count each bucket | `group_count(songs, "genre")` | M4 |
| **`groupby()`** | Split rows into groups, calculate something for each, recombine the answers | `df.groupby("house")["score"].mean()` | M6 |

---

## H

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`head()`** | Show the first few rows of a DataFrame | `df.head(3)` | M6 |
| **Histogram** | Chops one number column into ranges and counts how many land in each — shows a distribution | 38 scores into six bins of width 10 | M7 |

---

## I

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`if` / `elif` / `else`** | Choose exactly one path out of several. Checked top to bottom; **the first true one wins.** | The grade chain — put the narrowest condition first | M2 |
| **`iloc`** | Select from a DataFrame by **position**, counting from 0 | `df.iloc[3, 0]` | M6 |
| **`import`** | Bring another file's or library's functions into this one | `import stats`, `import numpy as np` | M3 |
| **Indentation** | The spaces at the start of a line. In Python this is real syntax, not decoration. | 4 spaces per level. Never mix tabs and spaces. | M2 |
| **Index (list)** | A value's position in a list, counting from **0** | `scores[0]` is the first item | M3 |
| **Index (DataFrame)** | The row labels down the left-hand side of a table | `0, 1, 2` by default, or `"s10", "s20"` | M6 |
| **Infinite loop** | A loop whose condition never becomes false, so it never stops | Forgetting `i += 1` inside a `while`. Press Ctrl-C. | M2 |
| **`info()`** | Column list with dtypes and non-null counts — the fastest way to spot missing values | Run it immediately after every `read_csv` | M6 |
| **`input()`** | Pause and read a line the user types. **Always returns text.** | `age = int(input("Age? "))` | M1 |
| **`int` (integer)** | A whole number, no decimal point | `47` | M1 |
| **Interaction** | When two features only make sense together — the effect of one depends on the other | A kilometre costs 12 minutes walking but 3.3 by bus | CAP |
| **Intercept** | What a line predicts when every feature is 0 | 44.9 points at zero study hours | M9 |
| **Interpreter** | The program that reads your Python file and does what it says | `python3 hello.py` starts it on your file | M1 |
| **`isna()`** | `True` wherever a value is missing | `df.isna().sum()` counts holes per column | M6 |
| **`.items()`** | Hands you the key and the value together on each turn of a dictionary loop | `for k, v in d.items():` | M4 |

---

## K

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`k`** | In kNN, how many neighbours get a vote. Small `k` = jumpy; large `k` = blurry. | The accuracy-vs-`k` plot for k = 1…25 | M8 |
| **k-nearest neighbors (kNN)** | Guess a new example's answer by asking the `k` most similar known examples | 3 neighbours: apple, apple, orange → apple | M8 |
| **Key** | The label on a dictionary slot | `"runs"` | M4 |
| **`KeyError`** | Python saying "there is no slot with that label" | `player["age"]` when there's no `age` key | M4 |

---

## L

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Label vector (`y`)** | The right answer for each row, in the same order as `X` | Shape `(178,)`, values 0/1/2 | M8 |
| **Leaf** | The end of a branch in a decision tree, where the answer lives | `value: [33.91]` | M9 |
| **Leakage** | Information from the test set sneaking into training, so your reported score is **too high** | Fitting `StandardScaler` on all the data *before* splitting | M8 |
| **Legend** | The little key naming each line or series on a chart | Needed on any chart with more than one series | M7 |
| **`len()`** | How many items are in a list, string or DataFrame column | `len(scores)` → `20` | M3 |
| **Line chart** | Dots joined in time order, so you can follow a path | Library visits across 12 weeks | M7 |
| **Linear regression** | Fitting the best straight line through the dots, then reading predictions off it | `score = 5.7 × hours + 44.9` | M9 |
| **`linspace()`** | Puts a **count** of evenly spaced points between two ends | `np.linspace(0, 1, 5)` | M5 |
| **List** | An ordered collection of values held in one variable | `[45, 0, 112]` | M3 |
| **List comprehension** | A one-line way to build a new list from an old one | `[s * 2 for s in scores if s > 50]` | M3 |
| **List of dicts** | Many records in a list — your first real dataset, a table you can loop over | 30 songs, 5 keys each | M4 |
| **`loc`** | Select from a DataFrame by **name** (index label, column name) | `df.loc[3, "name"]` | M6 |
| **Local variable** | A variable created inside a function; it disappears when the function ends | Invisible from outside | M3 |
| **Loop** | A block of code that repeats | `for`, `while` | M2 |

---

## M

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **MAE** (mean absolute error) | The average **size** of your mistakes, in the target's own units | "Off by 2.18 lakh on average" | M9 |
| **matplotlib** | The Python library for drawing charts | `import matplotlib.pyplot as plt` | M7 |
| **Mean** | The ordinary average: add everything, divide by how many | 313 ÷ 5 = 62.6 | M3 |
| **Median** | The middle value once everything is sorted — not dragged around by outliers | Median of 200, 250, 250, 300, 12000 is 250 | M3, M7 |
| **Method** | A function attached to a value, called with a dot | `text.strip()`, `scores.append(5)` | M2 |
| **Min–max normalization** | Squash numbers so the smallest becomes 0 and the largest becomes 1 | `(x − min) / (max − min)` | M5 |
| **Modulo (`%`)** | The remainder left after division | `7 % 2` → `1` | M1 |
| **Module** | A `.py` file you can `import` for the tools inside it | `import stats` — your own file from M3 | M2, M3 |
| **Mutable** | Able to be changed after it's created | Lists are mutable; strings are not | M3 |

---

## N

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`NaN`** | Pandas's marker for a missing value. **Not** zero, not an empty string. | What `to_numeric(errors="coerce")` leaves behind | M6 |
| **`NameError`** | "I've never heard of that name" — nearly always a typo | Using `totl` when you defined `total` | M1 |
| **`ndim`** | How many dimensions an array has: 1 = a row, 2 = a table | `scores.ndim` → `2` | M5 |
| **Negative index** | Counting backwards from the end of a list | `scores[-1]` is the last item | M3 |
| **Nested data** | A container inside a container — it takes two lookups to reach the value | `artists["Nova"]["country"]` | M4 |
| **Nested loop** | A loop inside another loop | Printing a multiplication grid | M2 |
| **`None`** | Python's word for "no value at all" | What a function without a `return` hands back | M3 |
| **`not`** | Flips `True` to `False` and back | `not injured` | M2 |
| **numpy** | The Python library for fast arrays and array maths | `import numpy as np` | M5 |

---

## O

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`object` dtype** | Pandas for "text — or a mixed mess". Seeing it on a number column always means trouble. | One `"unknown"` among 39 numbers forces the whole column to `object` | M6 |
| **Off-by-one bug** | A loop that runs exactly one time too many or too few | `range(1, 10)` when you meant 1 to 10 | M2 |
| **One-hot encoding** | Replacing one text column that has *k* values with *k* columns of 0s and 1s, exactly one of which is on | `"walk"` → `mode_walk=1, mode_cycle=0, mode_bus=0` | CAP |
| **`or`** | True when at least one side is true | `day == "sat" or day == "sun"` | M2 |
| **Outlier** | A value sitting far away from all the others | ₹900 among nine kids getting ₹20–₹40 | M3, M7 |
| **Overfitting** | Too complex: the model memorised the training rows instead of learning a rule. Great train score, poor test score. | Depth-14 tree, R² 1.000 train / 0.716 test | M9 |

---

## P

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **pandas** | The Python library for named, cleanable tables | `import pandas as pd` | M6 |
| **Parameter** | The placeholder name in a function's definition | `def greet(name):` — `name` is the parameter | M3 |
| **PATH** | The list of folders your terminal searches for programs. If Python isn't on it, `python` isn't found. | Tick "Add python.exe to PATH" in the Windows installer | SET |
| **`pd.cut()`** | Slice a number column into named bands | `low` / `mid` / `high` | M6 |
| **pip** | The tool that downloads and installs Python libraries | `pip install numpy pandas matplotlib scikit-learn` | SET |
| **Pipeline** | Preprocessing and a model glued into one object, so the preprocessing can't leak | `make_pipeline(StandardScaler(), KNeighborsClassifier(5))` | M8 |
| **`pop()`** | Remove an item from a list and hand it back (the last one by default) | `scores.pop()` | M3 |
| **Pre-registration** | Writing down what you expect to find **before** you look, so you can't move the goalposts | The dated prediction in capstone Milestone 1 | CAP |
| **`predict`** | Ask a trained model to guess the labels for new rows | `model.predict([[175, 2]])` | M8 |
| **`print()`** | Show something on the screen. Produces no value — see **`return`**. | `print(f"Total: {total}")` | M1 |

---

## R

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **R²** (r-squared) | The fraction of the variation your model explains. 1 is perfect, 0 is no better than guessing the mean, **negative is worse than that**. | 0.935 for the housing model; −0.016 for the baseline | M9 |
| **`random_state`** | A fixed number that makes a "random" shuffle repeatable | `train_test_split(..., random_state=42)` | M8 |
| **`range()`** | Generates a run of numbers. **Stops before the end value.** | `range(1, 11)` → 1 to 10 | M2 |
| **Record** | One dictionary describing one thing — one row of a table | `{"title": "Ghost Town", "artist": "Nova", ...}` | M4 |
| **Regression** | Predicting a **number** on a sliding scale, rather than a category | A house price of 36.45 lakh; a journey of 17.5 minutes | M9 |
| **REPL / interactive shell** | The `>>>` prompt where you type one line of Python and see the answer immediately | `python3`, then `2 + 2` → `4` | M1 |
| **Residual** | Actual minus predicted, for one single row | 74 − 73.4 = +0.6 | M9 |
| **Restart & Run All** | Wiping the notebook's memory and running every cell top to bottom. The only test that counts. | Capstone Milestone 7 | CAP |
| **`return`** | Send a value back to whoever called the function | `return n * 2` | M3 |
| **RMSE** (root mean squared error) | Like MAE, but it punishes a few big misses much harder | Errors `0,0,0,4` give MAE 1.0 but RMSE 2.0 | M9 |
| **Round trip** | Save it, load it back, and check it's identical | `loaded == songs` → `True` | M4 |

---

## S

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`savefig()`** | Write a chart to an image file. Works even when no window can open. | `fig.savefig("chart.png", dpi=150, bbox_inches="tight")` | M7 |
| **Scatter plot** | One dot per row, placed at (x, y). The shape of the cloud is the answer. | Study hours vs score, 38 dots | M7 |
| **Schema** | A written-down statement of which columns exist and what type each one is | `{"plays": int, "minutes": float}` | M4 |
| **scikit-learn (`sklearn`)** | The Python library of models, splits, metrics and built-in datasets | `from sklearn.neighbors import KNeighborsClassifier` | M8 |
| **Scope** | The part of a program where a name exists at all | A local variable dies when its function ends | M3 |
| **`score`** | Ask a trained model how well it does on some data. Returns accuracy for classifiers, R² for regressors. | `model.score(X_test, y_test)` | M8 |
| **Seed** | A starting number that makes "random" repeatable | `np.random.default_rng(42)` | M5 |
| **Series** | One column of a DataFrame, with its row labels attached | `df["score"]` | M6 |
| **`shape`** | How many rows and columns — an array or table's dimensions | `(3, 4)` = 3 rows, 4 columns | M5, M6 |
| **Side effect** | A change a function makes to something outside itself | `.sort()` quietly reordering the list you passed in | M3 |
| **`size`** | The total number of elements in an array | Shape `(3,4)` → `size` 12 | M5 |
| **Slice** | A new list made from part of another. The **stop** position is excluded. | `scores[1:4]` → items at positions 1, 2, 3 | M3 |
| **Slope** | How much the prediction changes per 1 unit of a feature | +2.994 lakh per extra bedroom | M9 |
| **`sort_values()`** | Reorder DataFrame rows by a column | `df.sort_values("score", ascending=False)` | M6 |
| **`sorted()` vs `.sort()`** | `sorted(s)` hands back a **new** sorted list; `s.sort()` rearranges `s` in place and returns `None` | The `None` from `.sort()` catches everybody once | M3 |
| **Split (tree)** | One yes/no question inside a decision tree | `km_to_school <= 1.65` | M9 |
| **Standardization** | Rescale a column so its mean is 0 and its standard deviation is 1 | `z = (value − mean) ÷ std` | M5, M8 |
| **`StandardScaler`** | The scikit-learn object that does standardization. **Fit it on training data only.** | Put it inside a `make_pipeline` | M8 |
| **`str` (string)** | Text, always inside quotes | `"Bengaluru"` | M1 |
| **`.str` accessor** | Apply text methods to a whole pandas column at once | `df["house"].str.strip().str.lower()` | M6 |
| **`stratify`** | Keep each class's share the same in both the train and test splits | 12/14/10 instead of an unlucky 14/16/6 | M8 |
| **`SyntaxError`** | "That isn't valid Python" — usually a missing bracket, quote or colon | `print("hi"` | M1 |

---

## T

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Target** | The one column you are trying to predict — the thing that becomes `y` | `minutes` in the journey dataset | M8, CAP |
| **Test set** | Rows locked away and used **once**, at the end, to check the model honestly | The 36 wines the model never saw | M8 |
| **`to_numeric(errors="coerce")`** | Turn a text column into numbers; anything unconvertible becomes `NaN` instead of crashing | Fixes `"12"` and flags `"tbd"` | M6 |
| **Traceback** | The report Python prints when it gives up, saying where and why | `NameError: name 'nme' is not defined` | M1 |
| **Train/test gap** | Training score minus test score. How much of your performance is memorisation. | 0.284 at depth 14 | M9 |
| **`train_test_split()`** | Randomly divide your rows into a training set and a test set. **Call it exactly once.** | `train_test_split(X, y, test_size=0.2, random_state=42)` | M8 |
| **Training set** | The rows the model is allowed to learn from | 142 of the 178 wines | M8 |
| **Truncated axis** | An axis that doesn't start at zero, so small gaps look enormous | Starting y at 65 makes a 9-point gap look like 74% | M7 |
| **Type** | The category of a value, which decides what you're allowed to do with it | `int`, `float`, `str`, `bool` | M1 |
| **Type conversion (cast)** | Deliberately turning one type into another | `int("12")` → `12` | M1 |
| **`TypeError`** | "Those kinds of things don't go together" | `"5" + 5` | M1 |

---

## U

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Underfitting** | Too simple: the model is bad on the training data **and** the test data | Depth-1 tree, R² 0.371 train / 0.282 test | M9 |
| **Unit of a row** | The one-sentence answer to "what does one row of my table represent?" | "One row = one journey to school" | CAP |

---

## V

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Value** | What's stored in a dictionary slot | `103` in `{"runs": 103}` | M4 |
| **`value_counts()`** | Count how often each value appears in a column — Module 4's `group_count`, built in | `df["house"].value_counts()` | M6 |
| **`ValueError`** | "Right kind of thing, but I can't use that particular value" | `int("twelve")` | M1 |
| **Variable** | A label attached to a value so you can reuse it | `score = 47` | M1 |
| **Vector** | One row of numbers describing one thing | `[80, 60, 90, 70]` = one student's four marks | M5 |
| **Vectorized** | Doing the maths on the whole array at once, with no loop written by you | `celsius * 9/5 + 32` on 1,000 temperatures | M5 |
| **Virtual environment (venv)** | A private box of Python libraries belonging to one project, so you can't break anything else | `python3 -m venv .venv`, then `source .venv/bin/activate` | SET |

---

## W

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`while` loop** | Repeat for as long as a condition stays true | `while lives > 0:` | M2 |

---

## X

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`X`** | The conventional name for the feature matrix — see **Feature matrix** | Capital `X` because it's a table; lowercase `y` because it's one column | M8 |

---

## Y

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`y`** | The conventional name for the label vector — see **Label vector** | `y = df["minutes"].values` | M8 |

---

## Z

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`zip()`** | Loop over two lists side by side | `for day, temp in zip(days, temps):` | M3 |
| **z-score** | How many standard deviations a value sits from the mean | `(x − mean) / std`; a z of 4.2 is far out | M5 |

---

## 🧩 The Confusion Pairs

These are the pairs that get mixed up most. If you only reread one part of this page, make it this table.

| These two | The difference | How to remember |
|---|---|---|
| `=` and `==` | `=` **puts** a value into a name. `==` **asks** whether two things are the same. | One equals sign does something; two ask something. |
| `print` and `return` | `print` makes pixels. `return` makes a value you can use. | If you can't do maths with it, it was printed. |
| `.loc` and `.iloc` | `.loc` uses **labels**. `.iloc` uses **positions**, from 0. | The `i` stands for *integer position*. |
| `axis=0` and `axis=1` | `axis` names the direction you **collapse**. `0` squashes rows and leaves you a row; `1` squashes columns and leaves you a column. | Point your finger along the axis you're deleting. |
| `sorted(s)` and `s.sort()` | `sorted` hands back a new list. `.sort()` rearranges in place and returns `None`. | If you write `s = s.sort()` you have just deleted your list. |
| List and array | A list can hold anything and is slow at maths. An array holds one type and is fast. | Lists are a drawer; arrays are a grid. |
| `NaN` and `0` | `NaN` means "we don't know". `0` is a real measurement. | Filling `NaN` with `0` invents data. |
| Training set and test set | The model learns from one and is graded on the other. | Homework vs the sealed exam paper. |
| Train score and test score | Both are always reported. The **gap** between them is the interesting bit. | A high train score alone tells you nothing. |
| Underfitting and overfitting | Underfit is bad at *both*. Overfit is great at train, bad at test. | Too simple vs too clingy. |
| MAE and RMSE | MAE averages error sizes. RMSE punishes big misses harder. | RMSE − MAE tells you how uneven your errors are. |
| Classification and regression | Category out vs number out. | Which bin? vs how many minutes? |
| Correlation and causation | Moving together vs one making the other happen. | Ask: what third thing could cause both? |
| Accuracy and baseline | A score means nothing until you know what guessing would give. | "82%" against a 25% baseline is a fact. "82%" alone is a boast. |
| `str` and `int` from a CSV | Everything read from a CSV is text until you convert it. | `'90' > '100'` is `True`, alphabetically. |
| Fitting the scaler before vs after the split | Before = leakage = an inflated score. After (or inside a pipeline) = honest. | The scaler must never have met the test rows. |

---

## 📈 What's Coming in Level 3

These words are **not** in this level. If you meet one in the wild, that's fine — it's a preview, not a gap.

| Term | One-line preview | Where |
|---|---|---|
| **Gradient descent** | Rolling downhill on a loss surface, one small step at a time — what `LinearRegression().fit()` was quietly doing | L3 M4 |
| **Loss function** | A single number saying how wrong the model currently is; training means making it smaller | L3 M4 |
| **Cross-validation** | Doing the train/test split five times so one unlucky split can't fool you | L3 M3 |
| **Regularization** | Deliberately handicapping a model so it can't overfit | L3 M4 |
| **Logistic regression** | Linear regression bent into a classifier | L3 M4 |
| **Precision / recall / F1** | What you use instead of accuracy when the classes are lopsided | L3 M3 |
| **Neural network** | Many tiny linear models stacked in layers, each feeding the next | L3 M5 |
| **Backpropagation** | How a network works out which of its thousands of numbers to nudge | L3 M5 |
| **PyTorch** | The library that does the calculus for you so you can build big models | L3 M6 |
| **CNN** | A network that looks at small patches of an image at a time | L3 M7 |
| **k-means / PCA** | Finding structure in data that has **no** labels at all | L3 M8 |

---

[Level 2 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Module 1](module-01-python-from-zero.md) · [Level 3 ➡](../level-3-engineer/)

*If a word isn't here, it wasn't taught in this level — and you're allowed to not know it yet.*
