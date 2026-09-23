# Week 5 — Columns You Invent Yourself

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Week 6 ➡](week-06.md) · [Student Guide](../student-guide/week-05.md) · [Workbook](../workbook/week-05.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the week the score finally moves, and the week you learn to delete your own work |
| **Big idea** | The biggest score jumps usually come from a column that was not in the file — a ratio, a bin, or two columns multiplied together. |
| **New vocabulary** | feature engineering · binning · ratio feature · interaction feature · ablation · delta |
| **New maths** | **None new.** Today practises the mean, the subtraction and the division from Week 4, plus one honest reading of a fourth decimal place. |
| **New syntax** | `FunctionTransformer(add_features)` · `pd.cut(s, bins=[...], labels=[...])` · `df.assign(new=...)` · `pipe.get_feature_names_out()` |
| **Dataset** | The numpy-generated pizza-delivery table from Week 1 (`make_data.py`, seed 0) |
| **Materials** | Graph paper or plain paper for the Invention Round · a whiteboard with room for a **six-row table** · printed workbook pages 5.1–5.6 · the Bug Log · **a timer** |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. `make_data.py` from Week 1 in the same folder. Nothing new to install. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `look.py` about **1 second**. `ablation.py` fits six pipelines and finishes in about **1 second** — say so before you run it, because six models sounds slow and is not. |

> **⚠️ Watch out:** the emotional content of this lesson is **deleting a column you were proud of**, and it is harder than the code. Two of the four features invented today buy nothing. Plan for that moment: do not soften it, do not skip it, and do not let the student delete it silently. The deletion goes in the table **with the number that justified it**. That habit is what this week is really teaching.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Derive four new features from an existing table** — one ratio, one bin, one interaction and one flag.
2. **Wrap their own feature function so it lives inside the `Pipeline`** and re-runs automatically on every new row.
3. **Run an ablation** — build with the feature, build without it, compare — and read the delta to four decimal places.
4. **Delete a feature they invented** because the ablation says it bought nothing, and write down the number that justified the deletion.

Observable evidence: `ablation.py` printing a six-row table with a ΔAUC column to four decimal places; four new columns visible in `pipe.get_feature_names_out()`; and two written deletion notes, each naming a feature and the number that killed it.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is no new maths this week and nothing to install.** What there is instead is one genuinely new *idea* — that a column can be invented — and one genuinely new *discipline*, which is measuring whether the invention was worth anything. Read this section once, about twenty minutes, and you will be well ahead.

### 1. The one-sentence version, and the story behind it

> **This week's one sentence:** "The columns in the file are whatever somebody happened to write down. They are almost never the shape the answer lives in — so you build better ones and then you measure whether they helped."

Here is the story that makes it land, and it is worth telling in the Hook exactly as written.

Two teams get the same 2,000 rows of pizza-delivery data and the same 24 hours.

**Team A** downloads a big fancy tree-based library, spends the night running hundreds of configurations on a rented computer, and reports a validation score of **0.781**.

**Team B** uses the same plain `LogisticRegression` the student already has. They spend the whole day *looking at the data*. They notice that lateness spikes hard between 18:00 and 20:00, so they add one column: `is_rush`. They notice that distance hurts more in a storm than on a clear day, so they add `distance × weather severity`. Two columns, four lines of code. They report **0.785**.

Team B wins, and every weight in their model can be explained to the pizza manager in one sentence.

**That is the whole argument for this week**, and it is not a fairy tale — it is roughly what happens in real projects. A day spent looking at data usually beats a day spent turning knobs.

But say the honest half too, because the numbers today are small: **we go from 0.7752 to 0.7843. That is one point.** Feature engineering is not magic. It is a grind of small, defensible gains, and it is still normally the better use of a day.

### 2. The four shapes of invented column

There are only four shapes worth knowing, and today's four features are one of each.

> **feature engineering** — building new columns out of the ones you already have, so the pattern becomes something a simple model can see.

**(a) The FLAG.** A yes-or-no column that answers one question about the row.

```python
d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
```

`between(18, 20)` gives `True` or `False`; `.astype(int)` turns those into 1 and 0, because a model multiplies and cannot multiply by `True`.

**(b) The BIN.** Cutting a number into ranges and treating each range as a category.

> **binning** — chopping a continuous column into ranges and treating each range as a category.

Why on earth would you throw away detail like that? Because `order_hour` is a **number that does not behave like a number**. Look at the real lateness rate by hour:

| hour | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | **18** | **19** | **20** | 21 | 22 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| late rate | .213 | .231 | .261 | .249 | .202 | .218 | .256 | .280 | **.374** | **.375** | **.355** | .237 | .196 | .309 |

That is a **hump**, not a slope. A model given raw `order_hour` and one weight has to draw one straight line through that shape, and the best straight line through a hump is nearly flat — which is exactly what happened: `order_hour`'s weight in the fitted model is **−0.121**, effectively nothing. The information was there and the model could not reach it.

Cut the hours into ranges and it can:

```
morning   (hours 10-14)   684 orders   late 0.2383
afternoon (hours 15-17)   286 orders   late 0.2552
rush      (hours 18-20)   717 orders   late 0.3682
night     (hours 21-23)   313 orders   late 0.2396
```

684 + 286 + 717 + 313 = 2000. ✅

![The hump a straight line cannot see](../figures/fig-w05-2-binning-hours-into-rush.svg)
*Figure 5.1 — The hump a straight line cannot see. 0.3682 − 0.2424 = 0.1258: a twelve-and-a-half-point gap that one yes-or-no column can hold and one weight on `order_hour` cannot.*

**(c) The RATIO.** Two columns often only matter in relation to each other.

> **ratio feature** — one column divided by another.

```python
d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
```

**Why the `+ 0.5`?** Because `distance_km` could in principle be zero, and dividing by zero gives `inf`, and `inf` makes `LogisticRegression` raise an error. The `+ 0.5` is a guard. Any small constant does; pick one and write down that you did.

And read what the column *means*, because that is the interesting bit. `prep_minutes` on its own is a weak column. `distance_km` on its own is the strongest column in the table. But *minutes of prep per kilometre* asks a different question entirely: **is the kitchen the bottleneck, or the road?**

```
12 minutes of prep on a 2 km run:   12 ÷ 2.5 = 4.80
12 minutes of prep on a 9 km run:   12 ÷ 9.5 = 1.26
```

Same prep time. Completely different situation. Neither original column could say that.

**(d) The INTERACTION.** Two features whose *combination* matters more than either alone.

> **interaction feature** — a new column built by combining two others, usually by multiplying, so the model can express "A matters more when B is true".

This is the one that needs the most care, so here is the evidence first. Real lateness rates from our table, split by distance and weather:

| | clear | rain | storm |
|---|---|---|---|
| **under 5 km** | 0.1765 (1105 orders) | 0.2927 (386) | 0.3908 (87) |
| **over 5 km** | 0.5034 (294) | 0.5914 (93) | 0.8571 (35) |

Now compute what a long trip *costs* you, in each kind of weather:

```
in the clear:   0.5034 − 0.1765 = 0.3269
in a storm:     0.8571 − 0.3908 = 0.4663

0.4663 ÷ 0.3269 = 1.43
```

**Distance is 1.43 times as costly in a storm as in the clear.** Now — a model with a weight on `distance` and a separate weight on `storm` can only **add** those two effects. Adding cannot say "worse together". Multiplying can:

```python
severity = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
d["dist_x_weather"] = d["distance_km"] * severity
```

```
a 6 km trip, clear:  6 × 0 = 0
a 6 km trip, rain:   6 × 1 = 6
a 6 km trip, storm:  6 × 2 = 12
```

The model now has a knob for "long trip **and** bad weather" that is separate from either one.

![When distance costs more, and how much more](../figures/fig-w05-3-interaction-distance-times-storm.svg)
*Figure 5.2 — When distance costs more, and how much more. Six cells, 2000 orders. The bottom-right corner is where the two problems meet, and 0.4663 against 0.3269 is the size of the meeting.*

🍕 **The analogy for the whole section.** Raw features are ingredients as they arrive: a whole onion, an unopened tin, a block of cheese. Feature engineering is the chopping, grating and mixing. The oven is the same either way — but nobody ever made a good pizza by throwing an unpeeled onion on top.

And here are all four shapes at once, worked out for one real row:

![The columns that were not in the file](../figures/fig-w05-1-raw-columns-to-invented-columns.svg)
*Figure 5.3 — The columns that were not in the file, worked out for one order: distance 2.78 km, prep 15.0 minutes, hour 12, weather clear. Every one is arithmetic on that row alone, which is why none of them can leak.*

### 3. The discipline: ablation, and why it is the deliverable

> **ablation** — measuring a feature's worth by building the model **with** it and **without** it, changing nothing else, and comparing on the validation set.
>
> **delta** — the difference between two scores. Written to four decimal places, because the differences are small.

**Every derived feature is a hypothesis, not a gift.** You thought of it; that is not evidence. The ablation table is the referee.

Here is the table you and the student will produce, and it teaches four separate lessons:

```
              variant  cols  accuracy  roc_auc  d_auc
  A  raw columns only    20    0.7600   0.7752 0.0000
       B  A + is_rush    21    0.7725   0.7825 0.0074
     C  A + hour_band    24    0.7675   0.7815 0.0063
    D  B + min_per_km    22    0.7675   0.7843 0.0091
E  D + dist_x_weather    23    0.7725   0.7829 0.0077
    F  E + is_weekend    24    0.7725   0.7828 0.0076
```

**Lesson 1 — `is_rush` earned its place.** +0.0074 AUC for one binary column. That is the 18:00–20:00 hump that raw `order_hour` could not express.

**Lesson 2 — the crude flag beat the clever bin.** Row C is the four-band `pd.cut` version. It costs **three extra columns** and delivers **less** (+0.0063 against +0.0074). Take that seriously: the fancier tool lost. The reason is that the real effect in this data is a hard rectangular step at 18:00, and `is_rush` is exactly that shape, while four bands spend two of their columns describing a difference between morning and afternoon that barely exists (0.2383 against 0.2552).

**Lesson 3 — two of the four inventions bought nothing, and one of them made things worse.** Read the deltas **against the row above**, not against A:

```
D − B  =  0.7843 − 0.7825  =  +0.0018    keep min_per_km
E − D  =  0.7829 − 0.7843  =  −0.0014    dist_x_weather made it WORSE
F − E  =  0.7828 − 0.7829  =  −0.0001    is_weekend bought nothing at all
```

`dist_x_weather` is the feature with the best *story* in this whole lesson — you can see the amplification in the crosstab, 0.4663 against 0.3269, it is real — **and it still lost 0.0014 of AUC.** Sit with that. The story was right and the column was not worth its place, because the one-hot weather columns and the distance column, between them, were already carrying most of it, and the new column is one more weight to estimate from the same 1,200 rows.

And `is_weekend` is the one that hurts to delete, because it sounds so obviously right. Here is why it is not:

```
weekend  556 orders   late 0.2752
weekday 1444 orders   late 0.2922
```

Weekends are **slightly less** late than weekdays. There was no signal to find. Delete it — and keep the row in the table, so future-you knows it was tested.

**Lesson 4 — your metric decides the winner, and you chose it in Week 1.** On AUC, **D wins** with 0.7843. On accuracy, **B, E and F tie** at 0.7725 and D is *worse* at 0.7675. If you had not fixed the metric in advance you would now be quietly picking whichever column made you look best. You fixed AUC. **Ship D.**

![The ablation table decides, not you](../figures/fig-w05-4-ablation-table-with-deltas.svg)
*Figure 5.4 — The ablation table decides, not you. Two inventions kept, two deleted, and the subtraction that justified each deletion printed beside it.*

### 4. Every line of this week's code, explained to someone who has never programmed

**The feature function.** This is the only genuinely new *structure* this week.

```python
def add_features(d, rush=False, band=False, ratio=False, inter=False, weekend=False):
    """One row in, the same row plus new columns out."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    ...
    return d
```

`def` means "I am defining a new instruction and here is its name". `add_features` is the name. Inside the round brackets are the things you hand it: `d`, the table, and then five **switches**, each set to `False` unless you say otherwise. So `add_features(X, rush=True)` adds only `is_rush`, and `add_features(X)` adds nothing at all. **That is what makes an ablation possible in one function** rather than six copies of a file.

`d = d.copy()` makes a private copy of the table before touching it, so the original is untouched. Skip this line and you slowly corrupt your own data across runs, silently. It is one line and it is not optional.

`d["is_rush"] = ...` creates a new column called `is_rush`. `return d` hands the table back.

**`pd.cut` — the bin.**

```python
d["hour_band"] = pd.cut(d["order_hour"],
                        bins=[9, 14, 17, 20, 23],
                        labels=["morning", "afternoon", "rush", "night"])
```

`bins` is a list of **edges**, and there is always one more edge than there are labels: five edges, four ranges, four labels. Get that count wrong and pandas says so out loud (it is in the Debugging Clinic).

The edges are read as **"bigger than the left, up to and including the right"**. So `(9, 14]` catches hours 10, 11, 12, 13 and 14. **This is where people get bitten:** if you had written `bins=[10, 14, ...]`, hour 10 would be *excluded* — it is not bigger than 10 — and all 47 orders placed at 10:00 would silently become blanks. No error. Start your first edge *below* your smallest value.

**`df.assign` — build a column without touching the original.**

```python
d2 = df.assign(min_per_km=df["prep_minutes"] / (df["distance_km"] + 0.5))
```

`assign` hands you back a **new** table with the extra column on it, and leaves `df` exactly as it was. It is the polite version of `df["new"] = ...`, and it is what you want while you are exploring, because you can try five ideas without ever damaging the table you started from.

**`FunctionTransformer` — putting your function inside the pipeline.**

```python
pipe = Pipeline([
    ("derive", FunctionTransformer(add_features, kw_args={"rush": True})),
    ("prep",   preprocess),
    ("model",  LogisticRegression(max_iter=2000, random_state=42)),
])
```

`FunctionTransformer` is a wrapper. It takes your plain function and dresses it up so that a `Pipeline` will accept it — a `Pipeline` only talks to things that have a `.fit` and a `.transform`, and your function has neither. `kw_args={"rush": True}` is how you set the switches through the wrapper.

**Why this matters more than it looks.** Stage 2 now happens *inside the saved object*. When a real order arrives next Tuesday, the pipeline computes `is_rush` for it automatically. Write `d["is_rush"] = ...` outside the pipeline instead and your saved artifact has no idea the column ever existed — it will be handed a row without it and fail, or worse, be handed a row where somebody computed it slightly differently.

![Where the invented columns have to live](../figures/fig-w05-5-derive-inside-the-pipeline.svg)
*Figure 5.5 — Where the invented columns have to live. 7 numeric columns + 15 one-hot columns = 22 going into the model, and stage 2 re-runs for ever because it is inside the object you saved.*

**And the safety property, which is the reason `FunctionTransformer` is allowed here at all:** `add_features` looks at **one row at a time**. It never computes an average, a total, or anything else that needs to see other rows. So there is nothing in it that could carry information between the train pile and the test pile. If you ever write a "feature function" that computes a column mean, **it is no longer safe and it does not belong in a `FunctionTransformer`** — it belongs in the `prep` stage where it will be fitted on train rows only. That distinction is Week 6's whole subject.

**`get_feature_names_out` — what the columns are actually called now.**

```python
print(pipe.named_steps["prep"].get_feature_names_out())
```

After all that imputing, scaling and one-hot encoding, the thing going into the model is a wide block of numbers with no names on it. `get_feature_names_out()` gives you the names back, in order:

```
num__distance_km, num__items, num__prep_minutes, num__order_hour,
num__driver_experience_months, num__is_rush, num__min_per_km,
cat__restaurant_CrustyBros, ... cat__weather_storm
```

Twenty-two of them, prefixed by which branch they came from. **You need this to read the model's weights**, and you will use it every week from here to the end of the year.

### 5. The three misconceptions you will actually meet

**"More columns must be better — the model has more to work with."** Row F has the most columns (24) and is worse than row D (22). Every extra column is another weight to estimate from the same 1,200 rows, and a weight estimated from not-quite-enough data is a noisy weight that costs you. Say the number: **F has four more columns than D and scores 0.0015 lower.**

**"The delta is only 0.0018, that's basically nothing."** This is the Week 4 rounding habit coming back. Four decimal places is the unit of this work. 0.0018 is small; **−0.0014 is a different sign**, and telling those two apart is the entire skill. Write the deltas out in full every time, never rounded to two places.

**"If the feature makes sense, keep it even though the number says no."** This is the one that costs professionals real money, and the reason it is so persuasive is that the story usually *is* right — the amplification in `dist_x_weather` is genuinely in the data. The reply is not "your story is wrong". It is: *"the column has to earn its place, and this one didn't. Keep the row in the table so we know we tried."*

### 6. How deep to go, and where to stop

| Do not teach today | Where it lives |
|---|---|
| Cyclical hour encoding (`sin`, `cos`) | Not this year as a required idea. If a strong student asks, the honest answer is in the Questions section: it makes a smooth hump, and our effect is a hard step, so `is_rush` wins here. |
| Date parts (`dt.dayofweek`, `days_since_signup`) | Mention in one sentence — our table already has `day_of_week` as a column. Real timestamps are Week 34's problem. |
| `PolynomialFeatures` (generate every product automatically) | Nowhere in Level 3. Mention only to say why not: it generates hundreds of columns and you cannot ablate hundreds of columns honestly. |
| Cross-validation and error bars on the delta | **Week 11.** This is the honest weakness of today's table and a strong student will spot it. Say "Week 11" and mean it — see the Questions section. |
| Target encoding | Not this year. Leakage minefield, and Week 6 has enough. |
| Feature selection (`SelectKBest`) | **Week 6**, and it appears there as a *cautionary tale*, not a tool. |
| Automated search over all subsets of features | Mention as a trap in the "flying" path. 2⁶ = 64 pipelines and the winner of 64 on 400 validation rows is very likely the luckiest, not the best. |
| Why `distance_km` gets a weight of 1.128 and `items` almost nothing | Week 13, when logistic regression gets opened up. |

---

## 🧰 Prep Checklist

### 20 minutes the night before

**1. (1 min) Check the folder.**

```bash
ls make_data.py
python3 -c "import sklearn; print(sklearn.__version__)"
```

**2. (7 min) Run the looking-first script.** Create `look.py`:

```python
"""look.py - fifteen minutes of looking, before any code."""
import pandas as pd
from make_data import make_deliveries

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)

print("--- lateness by hour of the day ---")
by_hour = df.groupby("order_hour")["late"].agg(["size", "mean"]).round(4)
by_hour.columns = ["orders", "late_rate"]
print(by_hour.to_string())

print("\n--- the same hours, cut into four bands with pd.cut ---")
band = pd.cut(df["order_hour"], bins=[9, 14, 17, 20, 23],
              labels=["morning", "afternoon", "rush", "night"])
print(df.groupby(band, observed=True)["late"].agg(["size", "mean"]).round(4).to_string())

print("\n--- the two-bucket version: is_rush ---")
rush = df["order_hour"].between(18, 20).astype(int)
print(df.groupby(rush)["late"].agg(["size", "mean"]).round(4).to_string())

print("\n--- weekend vs weekday ---")
wk = df["day_of_week"].isin(["Sat", "Sun"])
print(df.groupby(wk)["late"].agg(["size", "mean"]).round(4).to_string())

print("\n--- df.assign builds a column without touching the original ---")
d2 = df.assign(min_per_km=df["prep_minutes"] / (df["distance_km"] + 0.5))
print(d2[["prep_minutes", "distance_km", "min_per_km"]].head(5).round(4).to_string(index=False))
print("original still has", df.shape[1], "columns; the new table has", d2.shape[1])

print("\n--- distance x weather: the rates, then the counts ---")
far = df["distance_km"] > 5
print(pd.crosstab([far], df["weather"], values=df["late"], aggfunc="mean").round(4).to_string())
print(pd.crosstab([far], df["weather"]).to_string())
```

```bash
python3 look.py
```

Real output — this is what you must get:

```text
--- lateness by hour of the day ---
            orders  late_rate
order_hour                   
10              47     0.2128
11              91     0.2308
12             180     0.2611
13             237     0.2489
14             129     0.2016
15              78     0.2179
16              90     0.2556
17             118     0.2797
18             214     0.3738
19             275     0.3745
20             228     0.3553
21             148     0.2365
22              97     0.1959
23              68     0.3088

--- the same hours, cut into four bands with pd.cut ---
            size    mean
order_hour              
morning      684  0.2383
afternoon    286  0.2552
rush         717  0.3682
night        313  0.2396

--- the two-bucket version: is_rush ---
            size    mean
order_hour              
0           1283  0.2424
1            717  0.3682

--- weekend vs weekday ---
             size    mean
day_of_week              
False        1444  0.2922
True          556  0.2752

--- df.assign builds a column without touching the original ---
 prep_minutes  distance_km  min_per_km
         15.0         2.78      4.5732
         12.9         3.09      3.5933
         14.2         2.65      4.5079
          4.9         9.60      0.4851
         19.6         2.33      6.9258
original still has 10 columns; the new table has 11

--- distance x weather: the rates, then the counts ---
weather       clear    rain   storm
distance_km                        
False        0.1765  0.2927  0.3908
True         0.5034  0.5914  0.8571
weather      clear  rain  storm
distance_km                    
False         1105   386     87
True           294    93     35
```

**Runtime: about 1 second.**

**3. (8 min) Run the ablation.** Create `ablation.py` — the complete file is in the **🔑 Answer Key** under Page 5.5, and you should run it tonight and keep the output open in a second window during the lesson. It fits six pipelines in about **one second**.

The one number you must check: **row A is accuracy 0.7600, AUC 0.7752.** Those are Week 1's numbers exactly. If row A does not reproduce them, your split has drifted and every delta in the table is meaningless. Fix that before anything else.

**4. (4 min) Print and set up.**

- Workbook pages **5.1–5.6**.
- **A six-row table drawn on the whiteboard, empty**, with the column headings already written: `variant · cols · accuracy · AUC · ΔAUC · verdict`. Leaving it visibly empty at the start of the lesson does real work.
- Enough paper for the Invention Round — one sheet each, plus spares.
- A timer. The Invention Round is **eight silent minutes** and it needs to actually be eight.
- Figure 5.4 printed, **face down**. It is the answer.

### 5 minutes on the day

- Terminal open in the project folder, `look.py` already run once so the output is in the scrollback.
- The empty six-row table on the board.
- Write the two team scores on a corner of the board and leave them: `Team A: 0.781` and `Team B: 0.785`.

### Fallback if the laptops fail

| If this fails | Do this instead |
|---|---|
| No Python at all | **The whole first half works on paper.** The lateness-by-hour table, the weekend table and the distance-by-weather crosstab are all printed above — read them out and have the student compute the gaps. The Invention Round needs no computer. You lose only the ablation table, and you can hand them the printed one and have them fill in the ΔAUC column *by subtraction*, which is most of objective 3. |
| `make_data.py` missing | Use the printed tables above. Find the file before Week 6, which cannot be done on paper. |
| The ablation is slow | It is not. If it takes more than ten seconds something else is wrong — check you are not fitting on all 2,000 rows instead of the 1,200 train rows. |
| A student's row A does not match 0.7600 / 0.7752 | They dropped duplicates in a different order, or used a different `random_state`. Give them the two `train_test_split` lines verbatim from the Answer Key. **Do not let them continue with a broken row A** — every delta in the table is measured from it. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Two Teams, One Point Apart | 7 | 7 | 0.781 against 0.785, and who you'd rather be |
| 🧠 Concept — The Four Shapes, From the Data | 18 | 25 | Look at the real tables; four features invented from evidence |
| 💻 Live-Code Together — `add_features` and the ablation | 18 | 43 | Two deliberate mistakes: one loud, one silent and worse |
| 🎲 Their Turn — The Invention Round | 20 | 63 | Eight silent minutes, four votes, deltas on the board |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Two Teams, One Point Apart (7 minutes)

**Do this:** On the board, nothing but two numbers:

```
Team A:  0.781
Team B:  0.785
```

> **Say this:** "Two teams. Same 2,000 rows of delivery data — your table. Same 24 hours.
>
> **Team A** downloaded the most powerful model library they could find. Hundreds of settings, run overnight on a rented computer. Cost them about forty pounds in cloud time. They report 0.781.
>
> **Team B** used the same plain logistic regression you have been using for four weeks. Same settings. They didn't tune anything. They spent the whole day *looking at the data*. They noticed two things, added two columns, four lines of code, and they report 0.785.
>
> Team B won."

Pause.

> "Now — 0.785 against 0.781 is four thousandths. It's nothing. So I am not going to tell you Team B won because their score is higher, because that difference could be luck and by Week 11 you'll know how to check.
>
> Here is why Team B actually won. **Team B can explain their model.** They can walk into the pizza place and say 'orders between six and eight in the evening are late 37% of the time instead of 24%, and long trips in storms are much worse than long trips or storms on their own.' Team A can say 'the computer found it'.
>
> And Team B could do it again tomorrow, on a different problem, without renting a computer."

**Do this:** Now write on the board, big:

```
is_rush          = 1 if the order was placed between 18:00 and 20:00
dist_x_weather   = distance × how bad the weather is
```

> **Say this:** "Those are Team B's two columns. **Neither of them is in the file.** Nobody logged 'is_rush'. Somebody logged the hour, and Team B built the rest.
>
> That's today. You are going to invent columns that don't exist. And then — and this is the harder half — you are going to **measure whether each one was worth anything, and delete the ones that weren't.** Including the ones you liked."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Where did `is_rush` come from? Somebody had to notice something." | They looked at how lateness changes with the hour. | If they say "they guessed", push: "how would you check a guess like that before writing any model code?" (Group by the hour and look.) |
| "The table has `order_hour` in it already. Why isn't that enough?" | Don't resolve this yet — it is the next segment. | Take any answer. "Hold that" is a fine response. Write their guesses in a corner. |
| "Which team would you rather be?" | Team B, and for the explaining reason more than the score. | If they say Team A because it's more impressive, agree that it *sounds* more impressive, and ask what happens when the pizza manager asks why the model said 80%. |
| "How many days of work is 0.004 of score worth?" | **This is a real, open question.** | There is no right answer and you should say so. It depends what the score is for. Get them to notice that the question exists — most people never ask it. |

---

### 🧠 Concept — The Four Shapes, From the Data (18 minutes)

**Do this:** Put the lateness-by-hour table on the screen from `look.py`'s scrollback. Do not explain it. Just show it.

> **Say this — part 1, the hump:** "Fourteen hours. Read me the biggest three."

*18, 19, 20 — about 0.374.*

> "And the smallest?"

*22, at 0.196. And 14, at 0.202.*

> "So lateness goes down a bit in the afternoon, jumps hard at six in the evening, stays high for three hours, and drops again at nine. **That is a hump. It is not a slope.**
>
> Now here is the thing I want you to feel. Your model has **one weight** for `order_hour`. One number, multiplied by the hour. So whatever it does, it has to be a straight line: bigger hour, bigger effect, or bigger hour, smaller effect. It has no way of saying 'up in the middle'.
>
> **What's the best straight line through a hump?**"

*A flat one.*

> "Almost flat. And that is exactly what happened — in the fitted model, `order_hour`'s weight is **minus 0.121**, which next to `distance_km`'s **1.128** is nothing. The information was sitting right there in the table and the model could not reach it."

**Do this:** Draw the two-bucket table on the board:

```
             orders   late rate
not rush      1283     0.2424
rush (18-20)   717     0.3682
```

**Ask this:** "Subtract."

*0.1258.*

> **Say this:** "Twelve and a half points, in one yes-or-no column. That is shape number one, and it has two names depending on how you build it. If you cut a number into ranges you call it **binning**. If you cut it into exactly two ranges you usually just call it a **flag**."

**Do this:** Write the four shapes on the board as a list, leaving room under each. You will fill them in as you go.

```
1. FLAG          a yes-or-no question about the row
2. BIN           a number chopped into ranges
3. RATIO         one column divided by another
4. INTERACTION   two columns multiplied
```

> **Say this — part 2, the ratio:** "Shape three. `prep_minutes` on its own is a weak column. `distance_km` on its own is the strongest column in the table. Divide one by the other and you get something neither of them can say.
>
> Twelve minutes of prep on a two-kilometre run. Twelve divided by two and a half — I'll explain the extra half in a second — is **4.80**.
>
> Twelve minutes of prep on a nine-kilometre run. Twelve divided by nine and a half is **1.26**.
>
> Same prep time. What's different?"

*The first one is mostly kitchen; the second is mostly road.*

> "Exactly. **Is the kitchen the bottleneck, or is the road?** Neither original column asks that.
>
> And the extra half: `distance_km` could be zero, and dividing by zero gives you infinity, and infinity makes the model crash. So we add a small guard. Any small number does. **Write down that you did it**, because six months later you will wonder where the 0.5 came from."

**Do this:** Put the distance-by-weather crosstab on the screen. Both halves — rates and counts.

> **Say this — part 3, the interaction:** "Six cells. Under five kilometres and over five kilometres, against clear, rain and storm. Read me the top-left and the bottom-left."

*0.1765 and 0.5034.*

> "So going from a short trip to a long trip, on a clear day, costs you... subtract."

*0.3269.*

> "Now the same thing in a storm. Top-right and bottom-right."

*0.3908 and 0.8571. That's 0.4663.*

> "**0.4663 against 0.3269.** So a long trip is about one and a half times as costly when it's storming. Distance and weather don't just both matter — they **make each other worse**.
>
> And a model that has a weight for distance and a weight for storm can only **add them together**. Adding cannot say 'worse together'. So we build a column that multiplies."

**Do this:** Write the severity map and the three products on the board:

```
clear = 0    rain = 1    storm = 2

6 km, clear:   6 × 0 =  0
6 km, rain:    6 × 1 =  6
6 km, storm:   6 × 2 = 12
```

> **Say this — part 4, the referee:** "Four shapes. Four features. And now the important half of the lesson, which is the bit nobody enjoys.
>
> **Every one of those is a guess.** A good guess, built out of evidence I just showed you — but still a guess. The only way to find out whether a column was worth anything is to build the model twice: once with it, once without, **change nothing else**, and look at the difference on the validation pile.
>
> That has a name. It's called an **ablation** — it means removing something to see what it was doing. And the difference is called a **delta**. We write deltas to four decimal places, because they are small.
>
> Here is the promise I am making you, and it is going to be uncomfortable. **Two of these four features are going to buy nothing at all, and one of them is going to make the model worse.** And when that happens, we are going to delete it and write down the number that killed it."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What does it mean if I add a feature and the score goes *down*?" | The extra column cost more than it gave — one more weight to estimate from the same rows. | If they say "the feature is wrong", not quite — it might be genuinely real and still not worth its place. Keep that distinction alive; row E is exactly this. |
| "In an ablation, how many things do I change at once?" | One. | This is the whole method. If they say "a few", ask how they would know which one did it. |
| "Why four decimal places?" | Because the differences live in the fourth one. | If they say "to be accurate", push: "0.7843 and 0.7829 — round those to two places." Both 0.78. One is better and one is worse and you just erased the difference. |
| "Which of my four features do you think will win?" | **Take bets and write them on the board.** | There is no wrong answer here. Writing predictions down is what makes the result land in fifteen minutes. |
| "How would you check whether `is_weekend` is worth building, before building it?" | Group by weekend and compare the two lateness rates. | This is the best question in the segment. If they get it, run it live — 0.2752 against 0.2922 — and let them predict the delta. |

---

### 💻 Live-Code Together — `add_features` and the ablation (18 minutes)

**You never touch the keyboard.** Predictions before every run.

**Step 1 (4 min).** New file, `features.py`. Just the function and a look at what it makes.

```python
"""features.py - four invented columns, one row at a time."""
import pandas as pd
from make_data import make_deliveries

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)


def add_features(d, rush=False, band=False, ratio=False, inter=False, weekend=False):
    """One row in, the same row plus new columns out."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if band:
        d["hour_band"] = pd.cut(d["order_hour"],
                                bins=[9, 14, 17, 20, 23],
                                labels=["morning", "afternoon", "rush", "night"])
    if ratio:
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    if inter:
        sev = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * sev
    if weekend:
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    return d


out = add_features(df.head(5), rush=True, band=True, ratio=True, inter=True)
print(out[["order_hour", "is_rush", "hour_band", "prep_minutes",
           "distance_km", "min_per_km", "weather", "dist_x_weather"]].round(4).to_string(index=False))
print("\ncolumns before:", df.shape[1], " after:", out.shape[1])
```

**Ask before running:** "Row one is hour 12, prep 15.0, distance 2.78, weather clear. Give me all four new values."

*is_rush 0. hour_band morning. min_per_km 15.0 ÷ 3.28 = 4.5732. dist_x_weather 2.78 × 0 = 0.*

Run it. Real output:

```text
 order_hour  is_rush hour_band  prep_minutes  distance_km  min_per_km weather  dist_x_weather
         12        0   morning          15.0         2.78      4.5732   clear            0.00
         22        0     night          12.9         3.09      3.5933    rain            3.09
         16        0 afternoon          14.2         2.65      4.5079    rain            2.65
         13        0   morning           4.9         9.60      0.4851   clear            0.00
         20        1      rush          19.6         2.33      6.9258   clear            0.00

columns before: 10  after: 14
```

> **Say this:** "Four for four. And look at row five — hour 20, `is_rush` is 1, `hour_band` is `rush`. **Those two columns are saying the same thing in two different ways**, and in about eight minutes the ablation is going to tell us which way is better. My money is on the simple one and I'll tell you why afterwards.
>
> Ten columns in, fourteen out. And notice `d = d.copy()` at the top — without it, this function would quietly add columns to your original table every time you called it, and by the fourth call your ablation would be comparing nonsense. One line."

**Step 2 — ⚠️ FIRST DELIBERATE MISTAKE (3 min).** The loud one.

> **Say this:** "I want to try three bands instead of four. Change the labels to `["morning", "afternoon", "rush"]` and leave the bins alone."

```python
d["hour_band"] = pd.cut(d["order_hour"],
                        bins=[9, 14, 17, 20, 23],
                        labels=["morning", "afternoon", "rush"])
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "features.py", line 27, in <module>
    out = add_features(df.head(5), rush=True, band=True, ratio=True, inter=True)
  File "features.py", line 14, in add_features
    d["hour_band"] = pd.cut(d["order_hour"],
  File ".../pandas/core/reshape/tile.py", line 293, in cut
    fac, bins = _bins_to_cuts(
  File ".../pandas/core/reshape/tile.py", line 454, in _bins_to_cuts
    raise ValueError(
ValueError: Bin labels must be one fewer than the number of bin edges
```

> **Say this:** "`Bin labels must be one fewer than the number of bin edges.` Count the edges: 9, 14, 17, 20, 23. **Five.** Count the labels. **Three.** It wanted four.
>
> Why one fewer? Because the edges are *fences* and the labels name the *fields between them*. Five fence posts make four fields. Draw it if it helps — it is a thing people get wrong for years.
>
> Good error, by the way. It caught the problem immediately and told you the rule. Put the fourth label back."

**Step 3 — ⚠️ SECOND DELIBERATE MISTAKE (4 min).** The silent one, and it is much more important than the first.

> **Say this:** "Now a change that looks tidier. Our hours start at 10, so having the first bin edge at 9 looks sloppy. Change it to 10."

```python
d["hour_band"] = pd.cut(d["order_hour"],
                        bins=[10, 14, 17, 20, 23],
                        labels=["morning", "afternoon", "rush", "night"])
```

**Ask before running:** "Will that break?"

Most will say no.

Run it. Real output:

```text
 order_hour  is_rush hour_band  prep_minutes  distance_km  min_per_km weather  dist_x_weather
         12        0   morning          15.0         2.78      4.5732   clear            0.00
         22        0     night          12.9         3.09      3.5933    rain            3.09
         16        0 afternoon          14.2         2.65      4.5079    rain            2.65
         13        0   morning           4.9         9.60      0.4851   clear            0.00
         20        1      rush          19.6         2.33      6.9258   clear            0.00

columns before: 10  after: 14
```

> **Say this:** "**No error. Identical output.** So it's fine, yes?
>
> Add one line and check the whole table instead of five rows."

```python
band = add_features(df, band=True)["hour_band"]
print("blank hour_band values:", int(band.isna().sum()), "out of", len(band))
```

Run it. Real output:

```text
blank hour_band values: 47 out of 2000
```

**Do this:** Let the silence sit. Then:

> **Say this:** "**Forty-seven blanks.** Where did they come from?
>
> `pd.cut` reads its ranges as *'bigger than the left edge, up to and including the right edge'*. So `(10, 14]` means bigger than 10. And hour 10 **is not bigger than 10.** Every one of the 47 orders placed at ten in the morning fell out of the bottom of your bins and became a blank.
>
> No error. No warning. Just 47 rows quietly missing a value in a column you invented, which will then get filled in with something by the imputer next week and nobody will ever know.
>
> **This is the shape of bug that actually costs people money**, and the reason is right there: the first one shouted at you and this one did not. Put the edge back to 9 — always start your first edge *below* your smallest value — and check the blanks again."

```python
band = add_features(df, band=True)["hour_band"]
print("blank hour_band values:", int(band.isna().sum()), "out of", len(band))
```

```text
blank hour_band values: 0 out of 2000
```

**Step 4 (5 min).** Now the ablation. Do not type the whole file — it is long and it is in the Answer Key. Type the **evaluate** function's pipeline and the plan, and run the finished file.

> **Say this:** "The ablation script does one thing six times. Look at the middle of it."

```python
    pipe = Pipeline([
        ("derive", FunctionTransformer(add_features, kw_args=kw)),
        ("prep", pre),
        ("model", LogisticRegression(max_iter=2000, random_state=RS)),
    ])
```

> "Three stages. Stage one is **your function**, wrapped up so the pipeline will accept it — a pipeline only talks to things with a `.fit` and a `.transform`, and your plain function has neither, so `FunctionTransformer` dresses it up. `kw_args=kw` is how the switches get set.
>
> Stage two is last week's imputing, scaling and one-hot encoding. Stage three is the model.
>
> And **stage one is now inside the saved object.** When a real order arrives next Tuesday, this pipeline works out its `is_rush` for itself. If you had written `df["is_rush"] = ...` outside the pipeline, your artifact would have no idea that column was ever supposed to exist."

**Ask before running:** "Six models. How long?"

Most will guess a minute or more.

Run `ablation.py`. Real output:

```text
              variant  cols  accuracy  roc_auc  d_auc
  A  raw columns only    20    0.7600   0.7752 0.0000
       B  A + is_rush    21    0.7725   0.7825 0.0074
     C  A + hour_band    24    0.7675   0.7815 0.0063
    D  B + min_per_km    22    0.7675   0.7843 0.0091
E  D + dist_x_weather    23    0.7725   0.7829 0.0077
    F  E + is_weekend    24    0.7725   0.7828 0.0076
```

> **Say this:** "About a second. Six models. Get used to that — most of machine learning on data this size is fast, and the slow part is you thinking.
>
> Row A: 0.7752. **That is exactly Week 1's number**, and it has to be, because row A is Week 1's model. If it weren't, every delta below it would be meaningless.
>
> Now read it with me, and read the deltas **against the row above**, not against A."

**Do this:** Fill in the whiteboard table as they read. Write each subtraction out.

```
B − A  =  0.7825 − 0.7752  =  +0.0074     is_rush        KEEP
C − A  =  0.7815 − 0.7752  =  +0.0063     hour_band      drop, B is better with 3 fewer columns
D − B  =  0.7843 − 0.7825  =  +0.0018     min_per_km     KEEP
E − D  =  0.7829 − 0.7843  =  −0.0014     dist_x_weather DELETE
F − E  =  0.7828 − 0.7829  =  −0.0001     is_weekend     DELETE
```

> **Say this:** "Four things, and the third one is going to annoy you.
>
> **One.** `is_rush` earned it. One column, +0.0074.
>
> **Two.** The fancy four-band version **lost to the crude two-bucket one**, and it cost three extra columns to lose. Why? Because the real effect is a hard rectangular step at six in the evening, and `is_rush` is exactly that shape. The four bands spend two of their columns describing a difference between morning and afternoon — 0.2383 against 0.2552 — that is barely there.
>
> **Three, and this is the annoying one.** `dist_x_weather` **made the model worse.** Minus 0.0014. And that feature had the best story in the lesson — you saw the amplification yourself, 0.4663 against 0.3269. It's real. It is genuinely in the data. **And it still wasn't worth its place**, because the distance column and the three weather columns were already carrying most of it between them, and the new one is one more weight to guess from the same 1,200 rows.
>
> **Four.** Look at the accuracy column instead of AUC. On accuracy, D is the *worst* of B through F. If we hadn't decided in Week 1 that AUC was our number, we'd now be quietly choosing whichever column made us look best. We decided. **Ship D.**"

---

### 🎲 Their Turn — The Invention Round (20 minutes)

Full instructions in the next section. In brief: eight silent minutes with a pen inventing five columns that could exist but do not; then a vote for four; then build and ablate them live with everybody watching the deltas appear.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Turn Figure 5.4 face-up next to the whiteboard table.

> **Say this:** "Five things.
>
> **One.** Four shapes: a flag, a bin, a ratio, an interaction. Nearly every invented column you will ever build is one of those four.
>
> **Two.** Build them out of **evidence**, not out of vibes. `is_rush` came from looking at fourteen hourly lateness rates. `dist_x_weather` came from a six-cell crosstab.
>
> **Three.** They go **inside the pipeline**, wrapped in a `FunctionTransformer`, so they re-run for ever on every new row.
>
> **Four.** Every one is a guess until the ablation says otherwise. **One change per row. Four decimal places. Read the delta against the row above.**
>
> **Five, and this is the one I care about.** Two of today's four features are getting deleted, and one of them had a better story than the two that survived. **Deleting your own idea because the number says so is the job.** And the deleted row stays in the table with the number that killed it — so that in six months, when somebody suggests multiplying distance by weather, you can say 'tried it, minus 0.0014' instead of arguing about it for an afternoon."

Run the three checks from **✅ Assessing Understanding**, then assign the homework.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Bin labels must be one fewer than the number of bin edges` | "Your fence posts and your fields don't match." | `pd.cut(..., bins=[9,14,17,20,23], labels=["a","b","c"])` — five edges make four ranges, so you need four labels. | Count the edges, subtract one, that is how many labels. Five edges, four labels. |
| **No error**, but some rows of the binned column are blank | Nothing is wrong as far as pandas is concerned — values outside every bin become `NaN`, silently. | The first bin edge is **at or above** the smallest value. `bins=[10, ...]` drops every row where the hour is exactly 10 — 47 of them in our table. | Start the first edge *below* your minimum: `bins=[9, ...]`. Then check: `print(int(s.isna().sum()))`. **Do this check every single time you cut.** |
| `ValueError: Input X contains infinity or a value too large for dtype('float64').` | "One of your numbers is infinite." | A ratio feature divided by zero: `d["prep_minutes"] / d["distance_km"]` where a distance is 0. | Add a guard to the bottom: `/ (d["distance_km"] + 0.5)`. Write down which constant you chose. |
| `InvalidParameterError: The 'func' parameter of FunctionTransformer must be a callable or None. Got    order_hour  is_rush ...  instead.` | "You handed me a table where I wanted an instruction." | `FunctionTransformer(add_features(d, rush=True))` — the brackets **called** the function and passed its answer in. | Pass the function itself, unbracketed, and put the switches in `kw_args`: `FunctionTransformer(add_features, kw_args={"rush": True})`. |
| `NotFittedError: This ColumnTransformer instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.` | "I have not seen any data, so I do not know what the output columns are called." | `get_feature_names_out()` before `.fit`. | Fit first. The column names depend on the data — how many restaurants there were, for instance — so they cannot exist before fitting. |
| `ValueError: columns are missing: {'min_per_km'}` | "The table you just gave me is missing a column I was fitted with." | The feature was built with `df["min_per_km"] = ...` **outside** the pipeline. The pipeline learned to expect it, and a fresh row does not have it. | Move the arithmetic inside `add_features` and wrap it in a `FunctionTransformer`. **This is the error that proves why stage 1 has to be inside the pipeline.** |
| `ValueError: could not convert string to float: 'morning'` | "You asked me to do arithmetic on a word." | `hour_band` is a *category*, not a number, and it went down the numeric branch of the `ColumnTransformer`. | Send it down the categorical branch so it gets one-hot encoded. A binned column is a category, however numeric the thing it came from was. |
| `KeyError: 'pre'` | "There is no stage with that name." | `pipe.named_steps["pre"]` when the stage was named `"prep"`. | Use the exact name from the `Pipeline` list. `print(pipe.named_steps.keys())` shows you all of them. |
| **No error**, and every row of the ablation table is identical | Nothing is wrong — the switch never got through. | The new column was built but never added to the `ColumnTransformer`'s column list, so it was silently dropped. Columns you do not list are discarded by default. | Print `pipe.named_steps["prep"].get_feature_names_out()` and count. **If your new column is not in that list, the model never saw it.** |
| **No error**, and the ΔAUC column is all zeros to two decimal places | Nothing is wrong. You rounded. | `.round(2)` instead of `.round(4)`. | Four decimal places, always, in this work. `0.7843` and `0.7829` are both `0.78` and one is better and one is worse. |

### How to teach debugging without giving the answer

The moves from Weeks 1–4 all stand. This week adds the one that matters most for the rest of the year:

- **"Print `get_feature_names_out()` and count."** Almost every "my feature didn't do anything" bug is the feature not reaching the model at all. It is one line, it takes four seconds, and it turns a mystery into a fact. Ask for it before you ask anything else.

And a second, which is about the silent bugs specifically:

- **"Did you check the whole table, or just the first five rows?"** `head()` showed nothing wrong with the broken bins. 2,000 rows showed 47 blanks. **A bug that hides in row 6 is still a bug.**

And the sentence for this week:

> **"An error that shouts is a good day. The bugs that cost money are the ones that print a perfectly normal-looking table."**

---

## 🎲 The Activity, In Full

### The Invention Round

**Setup (1 minute).** Everybody gets a sheet of paper and a pen. The `look.py` output stays on the screen — the hourly table, the weekend table, the crosstab. **The whiteboard's six-row table stays visible.** Set the timer for eight minutes.

---

### Part 1 — Eight silent minutes (8 minutes)

**The instruction, given once and then not repeated:**

> **"Write down five columns that could exist in this table but don't. Not five ideas about the data — five columns, with a name and how you'd compute it. Eight minutes. No talking, no laptops."**

**Rules to state up front:**

- It must be computable **from one row**, using only columns already in the table. `driver_name` is not allowed; there is no such column.
- It must have a name you would actually type: `items_per_km`, not "something about items and distance".
- **Five is the target and five is hard.** Three good ones is a fine outcome. Do not lower the number in advance; let them push.

**What you do during the eight minutes:** circulate, read over shoulders, say nothing evaluative. If somebody is stuck after three minutes, point at one of the three tables on the screen and say only *"what question does that table make you want to ask?"*

**Ideas they will produce, and what to do with each:**

| Their idea | What it is | Say this |
|---|---|---|
| `items_per_km` | ratio | "Good — that's the same shape as `min_per_km`. Put it on the list." |
| `is_late_night` (after 22:00) | flag | "Good. And the hourly table will tell you whether it's worth building before you build it." |
| `prep_x_items` | interaction | "Good. What's the story? Why would those two make each other worse?" |
| `distance_bucket` (short / medium / long) | bin | "Good. What edges? And check your blanks." |
| `is_busy_restaurant` (CrustyBros) | flag | "That is already in your one-hot columns. **What would the ablation say?**" (Nothing. Good, cheap lesson.) |
| `driver_experience_squared` | neither | "Interesting — what would that let the model say that it can't say now?" (That the effect flattens off. Real, and hard to justify without more evidence.) |
| Anything using the answer, e.g. `was_it_late_last_time` | **leakage** | Do not shut it down. Write it on the board with a star. **"Hold that one — it's next week's whole lesson."** |

---

### Part 2 — Vote for four (3 minutes)

Collect every idea on the board. Group the duplicates. Then vote: **each student gets four ticks and may not spend two on one idea.** Take the top four.

**One condition you enforce quietly:** the winning four should cover at least three of the four shapes. If all four are flags, add a ratio yourself and say why: *"I want to test one of each so we learn something about the shapes, not just about this table."*

---

### Part 3 — Build and ablate, live (8 minutes)

Add the four winners to `add_features` as four new switches. **The student types; you dictate nothing they cannot work out.**

Then add four rows to the plan list and run it. Fill in the whiteboard table as the numbers land.

> **Say this before running:** "Before we look — everybody predict. Which of these four is going to be biggest, and is any of them going to be negative? Write your prediction on your paper."

Run it. Fill in the table. Read out each subtraction against the row above.

**What "finished" looks like:** the whiteboard's six-row table full, **with a KEEP or a DELETE against every row and the subtraction written out beside it**. At least one DELETE. Every student's paper carries their prediction, right or wrong, next to the real delta.

---

### Variation — easier

**Cut the Invention Round to three minutes and two columns**, and give them a starting point: *"one column about the hour, one column that divides something by something."* Then ablate only two features instead of four, so the table has four rows.

**Better still, for a student who struggles with the open-ended part:** give them the four features already named, and have them do the **evidence** work instead — group by each one and compute the two lateness rates *before* any model is fitted. Predicting which feature will win from the gaps alone is a genuinely valuable exercise, and it hits objectives 1 and 3 without asking them to invent from nothing.

### Variation — harder

1. **Predict the delta before running, to two decimal places of the delta itself.** Write the predictions on the board first. Nobody gets close, and *that* is the lesson: you cannot tell from the story how much a feature is worth. Only the table can.
2. **Build `items_per_km` and ablate it against `min_per_km`.** Two ratios from the same denominator. Do they help *together*, or does the second one add nothing once the first is in? (Try it. This is a real question about redundancy.)
3. **Row C, properly investigated.** Try `hour_band` with **two** bands (rush / not rush) and with **seven** bands. Where is the sweet spot, and is it just `is_rush` again? A student who works out that the two-band version *is* `is_rush` with three more characters of typing has understood binning.
4. **The honest weakness.** *"Every number in this table came from one 400-row validation pile. If I re-split with a different `random_state`, will D still win?"* Have them change `RS` from 42 to 0, 1 and 2 and re-run the whole table. **If a different variant wins each time, the search found noise.** This is the most valuable exercise in the week and it is exactly why Week 11 exists. Do not resolve it — write the finding on a card and pin it up for Week 11.
5. **Read the weights.** Print `get_feature_names_out()` alongside the fitted model's coefficients and find `is_rush` (0.436) and `min_per_km` (0.239) among them. Then ask why `order_hour` is only −0.121 and `distance_km` is 1.128.

---

## ❓ Questions Students Ask This Week

**"Isn't inventing `is_rush` just cheating? I looked at the answer and then built a column that matches it."**

**This is the sharpest question of the week and it deserves a real answer, because it is half right.**

You looked at the *training* rows to decide that 18:00–20:00 matters. That is allowed, and it is what training rows are for. You then measured the feature on the *validation* rows, which you did not look at. So the measurement is honest.

Where it becomes cheating is if you keep going: try 40 different hour ranges, keep whichever one scores best on validation, and report that score. Then you have fitted your *choices* to the validation pile, and the number you report is too high. That is the same trap the three-way split exists to contain, and it is the reason we look at 400 validation rows *once* per feature and not fifty times.

The honest version of the rule: **look at the training rows all you like. Every time you look at the validation rows, spend a decision.** You have a limited number of decisions before the validation score stops meaning anything, and nobody can tell you exactly how many.

**"Why did the four-band version lose to the two-bucket one? Four is more information."**

Four bands *is* more information and it still lost, and the reason is worth understanding because it generalises.

Look at the four rates: morning 0.2383, afternoon 0.2552, rush 0.3682, night 0.2396. Three of those four are within 0.017 of each other. The only real distinction in the data is **rush against everything else**. So `hour_band` spends three columns describing one real difference and two imaginary ones — and each imaginary one is a weight the model has to estimate from the same 1,200 rows, which it estimates badly, which costs score.

**The general rule:** a feature's cost is a column, and its benefit is whatever real distinction it captures. Four columns capturing one distinction is a bad trade.

**"`dist_x_weather` is obviously real — you showed me the numbers. Why should I delete it?"**

Because "real" and "worth a column" are different tests, and this is the most important distinction in the week.

The amplification is real: 0.4663 against 0.3269. But the model already has `distance_km` and three one-hot weather columns, and between them they can already produce most of that pattern. The new column adds a little that they cannot — and costs one more weight estimated from 1,200 rows. On this data the cost won, by 0.0014.

**What you should be uncomfortable about is not the deletion, it is the size of the number.** 0.0014 on 400 validation rows is well inside the range where a different split might flip the sign. So the intellectually honest write-up is: *"deleted, ΔAUC −0.0014, which is small enough that I would retest it with cross-validation before being sure."* Cross-validation is Week 11, and this is precisely why it is coming.

**"Could I just build fifty features and let the model sort it out?"**

You can, and people do, and here is exactly what goes wrong.

Every column is one more weight the model has to estimate from the same 1,200 rows. Add enough columns and the weights become noise — the model fits accidents in the training data rather than patterns, and your validation score falls. Our own table shows it in miniature: row F has the most columns of any row and is not the best.

There is a second cost that is less obvious and matters more at work: **fifty features is fifty things that can break.** Each one is code somebody has to maintain, and each one has a hidden assumption in it. `is_rush` assumes rush hour is 18:00–20:00. If the city's rush hour shifts, that column silently goes stale, and nobody notices because it never raises an error.

**"So is `is_rush` part of the features or part of the model? I wrote the 18-to-20 by hand."**

**Nobody fully agrees on this, and it is a real question rather than a puzzle with an answer.**

Push it far enough and the boundary dissolves. If you write forty hand-crafted rules and the "model" just adds them up, where does your knowledge live — in your code, or in the fitted weights?

The useful way to reason about it is to ask **what updates automatically when you retrain, and what requires a human to notice and edit a file.** The weights update. The `18, 20` does not. So `is_rush` is a piece of *your* knowledge, hard-coded, sitting in a pipeline that otherwise learns for itself — and that means it can go stale in a way the weights cannot.

Some people call this a feature and some call it a model component. What matters is that you know which parts of your system a retrain can fix and which parts it cannot. Write the hard-coded ones in the model card.

**"Why does `pd.cut` use those weird brackets — `(9, 14]`?"**

They are standard mathematical notation for "which end is included". A round bracket means **excluded**; a square bracket means **included**. So `(9, 14]` is *"bigger than 9, up to and including 14"*.

It matters because it decides where the boundary values go, and boundary values are exactly where the bugs are. Hour 14 lands in `morning`, not `afternoon`. If you want it the other way, `pd.cut(..., right=False)` flips every bracket, which is a bigger change than it sounds and worth avoiding unless you need it.

**"What about the sine-and-cosine trick for hours? I read about it."**

Good find, and it is a real technique. The problem it solves is that 23:00 and 00:00 are one hour apart in life and 23 units apart as numbers, so a model given the raw hour thinks midnight is as far from 11pm as it is from 11am. Feeding it `sin(2π × hour ÷ 24)` and `cos(2π × hour ÷ 24)` puts the hours on a circle instead, so 23 and 0 land next to each other.

**On this data it loses to `is_rush`, and the reason is instructive.** Sine and cosine at one cycle per day can only make **one smooth hump** across 24 hours. Our real effect is not a smooth hump — it is a hard rectangular step: high from 18:00 to 20:00, ordinary either side. `is_rush` is exactly that shape; sine and cosine are a smooth approximation to a sharp edge.

Cyclical encoding is the better tool when the effect genuinely *is* smooth and periodic — temperature by month, traffic in a city with a gentle profile. Here the truth is a step, so the step wins. **Which is the whole lesson of the week: the right feature is the one shaped like the truth, and the only way to find out is the ablation.**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The Invention Round becomes a discussion instead of eight silent minutes | Ideas are more fun out loud, and the first person to speak sets everyone else's direction. | **Enforce the silence and the timer.** The whole value is that each student generates independently. If it becomes a conversation, you get one person's four ideas instead of everyone's five. |
| All four invented features are flags | Flags are the easiest to think of, so they crowd out the other three shapes. | State the condition before the vote: *"I want at least three of the four shapes represented."* If the vote does not deliver it, add one yourself and say why out loud. |
| The student refuses to delete `dist_x_weather` | The story is genuinely good and they built it themselves. Sunk cost is real at fourteen and at forty. | **Do not win the argument by authority.** Ask: "what number would change your mind?" Then point at −0.0014. Then concede the honest half: it is a small number and Week 11 might overturn it. Write "retest in Week 11" next to the deletion. That is a professional outcome, not a compromise. |
| ΔAUC gets rounded to two decimal places and every row looks the same | Two decimals is what school maths rounds to, so it is a reflex. | Catch it the first time. Write `0.7843` and `0.7829` on the board, then write `0.78` and `0.78` underneath. Ask which one is better. **The rounding destroyed the answer.** |
| Row A does not reproduce 0.7600 / 0.7752 and the lesson continues anyway | It is only the baseline, so it feels safe to skip. | **Stop.** Every delta is measured from row A. If A is wrong, the whole table is fiction. Hand them the two `train_test_split` lines from the Answer Key verbatim and get A right before anything else. |
| A feature is built but the ablation shows no change at all, and nobody notices why | The new column was never added to the `ColumnTransformer`'s list, so it was silently dropped. Unlisted columns are discarded by default. | `print(pipe.named_steps["prep"].get_feature_names_out())` and count. This will happen at least once during the live build; treat it as a scheduled event rather than a surprise. |
| The `pd.cut` blank-values bug goes unnoticed because `head()` looked fine | Five rows is the habit, and five rows was genuinely fine. | Make `print(int(s.isna().sum()))` a reflex after every `pd.cut`, out loud, every time, for the rest of the year. |
| The lesson runs out of time in the Invention Round and the ablation never happens | The Round is the fun part and it expands to fill whatever you give it. | The ablation is the objective; the Round is the way in. If you are at minute 58 with no deltas on the board, stop the Round mid-sentence and ablate **two** features instead of four. Two deltas on the board beats four features nobody measured. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut, in this order:** row C (`hour_band` and all of `pd.cut`) — the flag delivers the binning idea on its own; then the interaction, keeping the crosstab as a *reading* exercise rather than a column to build; then the Invention Round drops from five columns to two.

**The version that skips the invention.** Give them the four features, already named and already coded. Their job is the **evidence and the arithmetic**, which is where the learning actually is:

> 1. "Group by `is_rush` and write the two lateness rates." → 0.2424 and 0.3682
> 2. "Subtract them." → 0.1258
> 3. "Group by weekend and write the two rates." → 0.2922 and 0.2752
> 4. "Subtract them." → −0.0170
> 5. "One of those gaps is seven times the other. Which feature do you think will win, and which will buy nothing?"
> 6. "Now run the ablation and see if you were right." → +0.0074 and −0.0001

**That sequence is objectives 3 and 4 in fifteen minutes**, it requires inventing nothing, and predicting the outcome correctly from two subtractions is a genuinely strong piece of reasoning.

**The copy-this-exactly scaffold.** Give them the deletion note as a fill-in-the-blanks form, because the *writing* is the marked part and a blank page is the obstacle:

```
FEATURE I AM DELETING:  ______________________

what I thought it would do:  ______________________________________

AUC without it:  0.______
AUC with it:     0.______
the delta:       0.______  −  0.______  =  ______________

so it bought:    ______________

I am deleting it because: ______________________________________
```

Two of those, filled in, is objective 4.

### If the student is flying

None of these needs syntax from a later week.

1. **Variation-harder 4 — re-split with `RS = 0, 1, 2` and see whether D still wins.** This is the best available exercise. If a different variant wins each time, the search found noise. Do not resolve it; label it "Week 11" and pin it up.
2. **Variation-harder 2 — two ratios sharing a denominator.** Does `items_per_km` add anything once `min_per_km` is in? A real question about redundancy, answerable with one extra row.
3. **The sine-and-cosine hour**, built and ablated against `is_rush`. Then the *explanation* of why the smooth version loses: one cycle per day can only make one smooth hump, and the truth is a rectangle.
4. **Read the weights.** `get_feature_names_out()` beside the fitted coefficients: `distance_km` 1.128, `weather_storm` 0.732, `is_rush` 0.436, `min_per_km` 0.239, `order_hour` −0.121. **Then the question: why is `order_hour` almost zero when the hourly table has a clear hump in it?** A student who answers that has understood binning completely.
5. **Count the possible ablations.** Six candidate features means 2⁶ = 64 possible pipelines. If you fitted all 64 and kept the best on 400 validation rows, what would you actually have found? (The luckiest, not the best.) Then estimate how much of the winner's margin is real.
6. **The honest question:** `is_rush` hard-codes 18 to 20. Write down three ways that column could silently go wrong in a year, and which of them a retrain would fix. (None of them. That is the point.)

### If the student won't engage today

**Close the laptop. One printed table and a pen.**

Put the hourly lateness table in front of them — fourteen rows, printed. Nothing else.

Then three instructions:

> **"Draw me a bar for each hour. Tallest bar is the hour with the most late deliveries."**
>
> **"Circle the three tallest bars."**
>
> **"Now: if I gave you one yes-or-no question to ask about an order, and you wanted to know if it was going to be late — what question would you ask?"**

Whatever they say, follow with: *"so what would you call that column?"*

That is objective 1, delivered in ten minutes with a pencil, and it is the half of the week Weeks 6 and 7 sit on. Drawing the hump by hand and then inventing the flag that catches it is the whole idea, and it does not need a computer. The ablation can wait a day; the picture of three tall bars in the middle of a flat row cannot be un-seen.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the four shapes, spoken (45 seconds)**

> "Name me a **ratio**, a **bin**, an **interaction** and a **flag** you could build from the delivery table. One each, with a name."

*Good answer:* "Ratio: `min_per_km`, prep minutes divided by distance. Bin: `hour_band`, the hours cut into morning, afternoon, rush and night. Interaction: `dist_x_weather`, distance times weather severity. Flag: `is_rush`, 1 if the hour is 18, 19 or 20."

**What to catch:** a "bin" that is really a flag, or an "interaction" that is really a ratio. Push once: *"which two columns went into that, and did you divide them or multiply them?"*

**Check 2 — reading a delta, spoken (60 seconds)**

> "Row D scores AUC 0.7843. Row E is row D plus one more column and scores 0.7829. **What do I do, and what do I write down?**"

*Good answer:* "Delete the new column. 0.7829 minus 0.7843 is minus 0.0014, so it made the model worse. I write the feature name, the delta, and 'deleted' in the table — and I keep the row so nobody tries it again."

**Full marks needs the subtraction done and the row kept.** A student who says "delete it" without producing −0.0014 is a level-3 answer; push: *"what's the number that justified it?"*

**Check 3 — where the feature lives, written, one sentence (90 seconds)**

> "You build `min_per_km` with `df["min_per_km"] = ...` at the top of your script, outside the pipeline. Everything trains fine and the score is good. **Write me one sentence on what goes wrong later, and when.**"

*Good answer:* "It goes wrong the first time the saved pipeline is handed a fresh row, because that row hasn't got a `min_per_km` column and nothing inside the pipeline knows how to build one — you get `ValueError: columns are missing: {'min_per_km'}` at prediction time, not at training time."

**What to catch:** "nothing goes wrong, the score was fine." That is exactly the trap. Push: *"the score was fine today. What happens on Tuesday when one new order arrives?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot name a column that is not already in the table. Reads "feature engineering" as "changing the model". Cannot say what an ablation compares. |
| **2 — Emerging** | Builds a flag and a ratio when the shape is given. Runs the ablation script and reads the AUC column. Reports deltas to two decimal places, so several rows look identical. |
| **3 — Secure** | Invents four features unaided, one of each shape, **from evidence they looked up first**. Runs the ablation with one change per row. Reads deltas to four places against the row above. **Deletes a feature and writes the number that justified it.** This is the target. |
| **4 — Strong** | Predicts which features will pay from the group-by gaps *before* fitting anything. Explains why the four-band bin lost to the two-bucket flag. Checks `get_feature_names_out()` unprompted when a delta is suspiciously zero. Checks `isna().sum()` after every `pd.cut`. |
| **5 — Exceptional** | Argues that `dist_x_weather`'s −0.0014 is small enough to need retesting, and names cross-validation as the thing that would settle it. Notices that AUC and accuracy disagree about the winner and points at the Week 1 metric commitment as the tie-breaker. Says that `is_rush` hard-codes 18-to-20 and that a retrain cannot fix it if the city's rush hour moves. Asks whether looking at the hourly table before building the feature was allowed, and answers their own question correctly. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour. Three pages, and page 5.6 is the one I'm marking.
>
> **Page 5.4 — build four derived features.** One ratio, one bin, one interaction, one flag. **They may not be the four we built in class.** Use the tables from `look.py` to find your evidence first — I want a sentence for each one saying which numbers made you think of it. And two rules: put every one of them inside `add_features`, and after any `pd.cut`, print `isna().sum()` and write down the answer. If it isn't zero, fix your first bin edge.
>
> **Page 5.5 — the ablation table.** One row per feature. **One change per row, no exceptions** — if you add two features in one row you have learned nothing about either. Every row gets: the variant letter, the number of columns, the accuracy, the AUC, and the ΔAUC **to four decimal places**. Row A must reproduce 0.7600 and 0.7752 exactly. If it doesn't, stop and fix that before you do anything else, because every other number on the page is measured from it.
>
> **Page 5.6 — and this is the marked one. Delete the ones that bought nothing, in writing.** For each deletion: the feature's name, what you thought it would do, the two AUC numbers, **the subtraction written out**, and one sentence saying why you are deleting it.
>
> And I want at least one deletion. If all four of your features paid off, either you got lucky or something is wrong with your table — so in that case, delete the *weakest* one anyway and write down what it bought. A feature that buys +0.0002 is a column somebody has to maintain for ever in exchange for nothing."

**Workbook pages:** 5.1, 5.2, 5.3 in class · **5.4, 5.5, 5.6** at home.

**Expected time:** 20 min building the four features and checking the blanks · 15 min getting row A to match and running the table · 15 min writing the deletion notes · 10 min on the evidence sentences. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** four things. **One — does row A reproduce 0.7600 / 0.7752?** If not, nothing else on the page can be trusted and that is the first thing to say. **Two — is it one change per row?** A row that adds two features at once is the commonest failure and it invalidates both. **Three — are the deltas to four decimal places, and are they computed against the row above rather than always against A?** Both are acceptable as long as they say which; a page that mixes the two silently is the real problem. **Four — and this is the objective — does each deletion note contain an actual subtraction?** "I deleted `is_weekend` because it didn't help" is not the answer. "0.7828 − 0.7829 = −0.0001, so I deleted it" is. **The number is the deliverable, not the decision.**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone. **All code below was run; all output is real.**

### Page 5.1 — Match the word to the thing

| Word | Description |
|---|---|
| **feature engineering** | Building new columns out of the ones you already have, so the pattern becomes something a simple model can see. |
| **binning** | Chopping a continuous column into ranges and treating each range as a category. |
| **ratio feature** | One column divided by another, with a small guard on the bottom so you never divide by zero. |
| **interaction feature** | Two columns multiplied, so the model can say "A matters more when B is true". |
| **ablation** | Build the model with the feature, build it without, change nothing else, compare on the validation pile. |
| **delta** | The difference between two scores. Written to four decimal places, because that is where the difference lives. |

### Page 5.2 — Predict the output (answered in pen, in class)

**(a)** `pd.cut(pd.Series([10, 14, 17, 18, 20, 23]), bins=[9,14,17,20,23], labels=["morning","afternoon","rush","night"])`. What comes out?

```text
0      morning
1      morning
2    afternoon
3         rush
4         rush
5        night
```

Hour 14 goes to `morning` and hour 17 goes to `afternoon`, because `(9, 14]` **includes** its right-hand edge.

**(b)** Same call, but `bins=[10,14,17,20,23]`. What changes?

```text
0          NaN
1      morning
...
```

Hour 10 becomes blank, because it is not *bigger than* 10. On the full 2,000-row table that is **47 blanks**, with no error and no warning.

**(c)** `d2 = df.assign(min_per_km=df["prep_minutes"] / (df["distance_km"] + 0.5))`. How many columns has `df` got afterwards?

**Ten** — unchanged. `assign` hands back a *new* table (`d2`, with eleven) and leaves `df` alone.

**(d)** Row one is prep 15.0, distance 2.78. What is `min_per_km`?

15.0 ÷ (2.78 + 0.5) = 15.0 ÷ 3.28 = **4.5732**.

**(e)** Same row, weather `clear`. What is `dist_x_weather`?

2.78 × 0 = **0.00**.

**(f)** Row five is hour 20. What are `is_rush` and `hour_band`?

`is_rush` is **1** (20 is between 18 and 20 inclusive). `hour_band` is **rush** (20 is in `(17, 20]`).

### Page 5.3 — The Invention Round sheet (in class)

There is no single right answer. **Marked on shape, not on cleverness.** A full sheet has five entries, each with a **name you could type** and a **one-line recipe from columns that exist**. Examples that earn full marks:

| name | recipe | shape |
|---|---|---|
| `items_per_km` | `items ÷ (distance_km + 0.5)` | ratio |
| `is_late_night` | 1 if `order_hour ≥ 22` | flag |
| `distance_band` | `pd.cut(distance_km, bins=[0, 2, 5, 15], labels=["short","medium","long"])` | bin |
| `prep_x_items` | `prep_minutes × items` | interaction |
| `is_busy_restaurant` | 1 if `restaurant == "CrustyBros"` | flag (**already in the one-hot columns** — good, cheap lesson) |

**Not acceptable, and worth naming out loud:** anything using a column that does not exist (`driver_name`), anything that needs to see other rows (`this_restaurant's_average_lateness` — that is a cross-row statistic and it belongs nowhere near a `FunctionTransformer`), and anything using the answer (`was_late_last_time`). **That last one is next week's whole lesson** and a student who proposes it should get credit, not correction.

### Page 5.4 — Build four derived features

The four from the lesson, in the complete function:

```python
def add_features(d, rush=False, band=False, ratio=False, inter=False, weekend=False):
    """One row in, the same row plus new columns out. Nothing crosses between rows."""
    d = d.copy()
    if rush:                                     # the FLAG
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if band:                                     # the BIN
        d["hour_band"] = pd.cut(d["order_hour"],
                                bins=[9, 14, 17, 20, 23],
                                labels=["morning", "afternoon", "rush", "night"])
    if ratio:                                    # the RATIO
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    if inter:                                    # the INTERACTION
        sev = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * sev
    if weekend:                                  # a second FLAG
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    return d
```

**The evidence sentence for each one**, which is the marked half:

- `is_rush` — "Hours 18, 19 and 20 are late 0.3738, 0.3745 and 0.3553 of the time; every other hour is between 0.196 and 0.309."
- `hour_band` — "Same evidence, but I wanted to check whether morning, afternoon and night differ from each other too." (They barely do: 0.2383, 0.2552, 0.2396.)
- `min_per_km` — "12 minutes of prep on 2 km is 4.80 and on 9 km is 1.26; the same prep time means two completely different situations."
- `dist_x_weather` — "A long trip costs 0.5034 − 0.1765 = 0.3269 in the clear but 0.8571 − 0.3908 = 0.4663 in a storm, so distance and weather make each other worse."

**The blank check after `pd.cut`, which must be shown:**

```python
band = add_features(df, band=True)["hour_band"]
print("blank hour_band values:", int(band.isna().sum()), "out of", len(band))
```

```text
blank hour_band values: 0 out of 2000
```

With `bins=[10, ...]` instead:

```text
blank hour_band values: 47 out of 2000
```

### Page 5.5 — The ablation table

**The complete, runnable file.** Save as `ablation.py` beside `make_data.py`.

```python
"""ablation.py - does each invented column actually pay?"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from make_data import make_deliveries

RS = 42
BASE_NUM = ["distance_km", "items", "prep_minutes", "order_hour",
            "driver_experience_months"]
BASE_CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)


def add_features(d, rush=False, band=False, ratio=False, inter=False, weekend=False):
    """One row in, the same row plus new columns out. Nothing crosses between rows."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if band:
        d["hour_band"] = pd.cut(d["order_hour"],
                                bins=[9, 14, 17, 20, 23],
                                labels=["morning", "afternoon", "rush", "night"])
    if ratio:
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    if inter:
        sev = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * sev
    if weekend:
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    return d


def evaluate(label, **kw):
    made = add_features(X_tr.head(3), **kw)
    new = [c for c in made.columns if c not in X_tr.columns]
    num = BASE_NUM + [c for c in new if made[c].dtype.name != "category"]
    cat = BASE_CAT + [c for c in new if made[c].dtype.name == "category"]
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat),
    ])
    pipe = Pipeline([
        ("derive", FunctionTransformer(add_features, kw_args=kw)),
        ("prep", pre),
        ("model", LogisticRegression(max_iter=2000, random_state=RS)),
    ])
    pipe.fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_va)[:, 1]
    return {"variant": label,
            "cols": pipe.named_steps["prep"].get_feature_names_out().shape[0],
            "accuracy": accuracy_score(y_va, (prob >= .5).astype(int)),
            "roc_auc": roc_auc_score(y_va, prob)}, pipe


PLAN = [("A  raw columns only", {}),
        ("B  A + is_rush", dict(rush=True)),
        ("C  A + hour_band", dict(band=True)),
        ("D  B + min_per_km", dict(rush=True, ratio=True)),
        ("E  D + dist_x_weather", dict(rush=True, ratio=True, inter=True)),
        ("F  E + is_weekend", dict(rush=True, ratio=True, inter=True, weekend=True))]

rows, pipes = [], {}
for label, kw in PLAN:
    r, p = evaluate(label, **kw)
    rows.append(r)
    pipes[label] = p

tbl = pd.DataFrame(rows)
tbl["d_auc"] = tbl["roc_auc"] - tbl.loc[0, "roc_auc"]
print(tbl.round(4).to_string(index=False))

print("\n--- what the winner's columns are called ---")
names = pipes["D  B + min_per_km"].named_steps["prep"].get_feature_names_out()
print(len(names), "columns:")
print(", ".join(names))
```

```bash
python3 ablation.py
```

Real output:

```text
              variant  cols  accuracy  roc_auc  d_auc
  A  raw columns only    20    0.7600   0.7752 0.0000
       B  A + is_rush    21    0.7725   0.7825 0.0074
     C  A + hour_band    24    0.7675   0.7815 0.0063
    D  B + min_per_km    22    0.7675   0.7843 0.0091
E  D + dist_x_weather    23    0.7725   0.7829 0.0077
    F  E + is_weekend    24    0.7725   0.7828 0.0076

--- what the winner's columns are called ---
22 columns:
num__distance_km, num__items, num__prep_minutes, num__order_hour, num__driver_experience_months, num__is_rush, num__min_per_km, cat__restaurant_CrustyBros, cat__restaurant_GreenLeaf, cat__restaurant_Napoli, cat__restaurant_SliceHouse, cat__restaurant_TandooriPizza, cat__day_of_week_Fri, cat__day_of_week_Mon, cat__day_of_week_Sat, cat__day_of_week_Sun, cat__day_of_week_Thu, cat__day_of_week_Tue, cat__day_of_week_Wed, cat__weather_clear, cat__weather_rain, cat__weather_storm
```

**Runtime: about 1 second for all six fits.**

**The column-count arithmetic, which the student should be able to reproduce:** variant D has 5 base numeric + `is_rush` + `min_per_km` = **7 numeric**, and 5 restaurants + 7 weekdays + 3 weathers = **15 one-hot**. 7 + 15 = **22**. ✅

**The deltas against the row above:**

| step | arithmetic | verdict |
|---|---|---|
| B − A | 0.7825 − 0.7752 = **+0.0074** | keep `is_rush` |
| C − A | 0.7815 − 0.7752 = **+0.0063** | drop `hour_band` — B beats it with three fewer columns |
| D − B | 0.7843 − 0.7825 = **+0.0018** | keep `min_per_km` |
| E − D | 0.7829 − 0.7843 = **−0.0014** | delete `dist_x_weather` |
| F − E | 0.7828 − 0.7829 = **−0.0001** | delete `is_weekend` |

### Page 5.6 — The deletion notes

**Deletion 1.**

> **Feature:** `dist_x_weather` — `distance_km × weather severity`, with clear 0, rain 1, storm 2.
>
> **What I thought it would do:** let the model say that a long trip is much worse in a storm than in the clear. The evidence for that is real: a long trip costs 0.5034 − 0.1765 = 0.3269 in the clear and 0.8571 − 0.3908 = 0.4663 in a storm, which is 1.43 times as much.
>
> **AUC without it (row D):** 0.7843
> **AUC with it (row E):** 0.7829
> **The delta:** 0.7829 − 0.7843 = **−0.0014**
>
> **Why I am deleting it:** it made the model worse. The distance column and the three one-hot weather columns were already carrying most of that pattern between them, and the new column is one more weight to estimate from the same 1,200 rows. The story was right and the column still was not worth its place.
>
> **Honest caveat:** −0.0014 measured on 400 validation rows is small enough that a different split might flip the sign. Retest with cross-validation in Week 11 before calling it settled.

**Deletion 2.**

> **Feature:** `is_weekend` — 1 if the day is Saturday or Sunday.
>
> **What I thought it would do:** weekends are busier, so more deliveries should be late.
>
> **AUC without it (row E):** 0.7829
> **AUC with it (row F):** 0.7828
> **The delta:** 0.7828 − 0.7829 = **−0.0001**
>
> **Why I am deleting it:** there was nothing to find. Weekends are late 0.2752 of the time and weekdays 0.2922 — weekends are very slightly *better*, and the gap of −0.0170 is a fifth of the rush-hour gap of 0.1258. A column that buys nothing still has to be maintained for ever, so it costs more than nothing.

**What earns full marks:** the subtraction written out, both AUC numbers present, and a reason that refers to a number. **What does not:** "it didn't help", "the delta was tiny", or any note without an arithmetic line in it.

> **🧑‍🏫 Marking note on the caveat.** A student who adds the Week 11 caveat to deletion 1 unprompted has produced a level-5 answer. It is not required, and you should point it out to the class if anyone does it, because "this number is too small to be sure about" is a professional habit and almost nobody arrives with it.

### Every question posed in the lesson

- *"Where did `is_rush` come from?"* → Somebody grouped by the hour and looked at fourteen lateness rates.
- *"Read me the biggest three hours."* → 18, 19, 20 — 0.3738, 0.3745, 0.3553.
- *"What's the best straight line through a hump?"* → An almost flat one. `order_hour`'s fitted weight is −0.121 against `distance_km`'s 1.128.
- *"Subtract the two rush rates."* → 0.3682 − 0.2424 = **0.1258**.
- *"12 minutes on 2 km, and 12 minutes on 9 km."* → 12 ÷ 2.5 = **4.80** and 12 ÷ 9.5 = **1.26**. Same prep, kitchen versus road.
- *"Why the + 0.5?"* → A distance of zero would give infinity, and `LogisticRegression` raises `ValueError: Input X contains infinity`.
- *"What does a long trip cost in the clear, and in a storm?"* → 0.3269 and 0.4663, and 0.4663 ÷ 0.3269 = **1.43**.
- *"A 6 km trip in each kind of weather."* → 6 × 0 = 0, 6 × 1 = 6, 6 × 2 = 12.
- *"How many things do you change per ablation row?"* → **One.**
- *"Why four decimal places?"* → Because 0.7843 and 0.7829 both round to 0.78, and one is better and one is worse.
- *"Row one is hour 12, prep 15.0, distance 2.78, clear. Give me all four new values."* → 0, `morning`, 4.5732, 0.0.
- *"Count the bin edges and the labels."* → Five edges, four ranges, four labels.
- *"Will changing the first edge to 10 break?"* → No error, identical `head()` — and **47 silent blanks** in the full 2,000 rows.
- *"Six models. How long?"* → About one second.
- *"Why did the four-band bin lose to the two-bucket flag?"* → Three of the four bands are within 0.017 of each other; it spent three columns describing one real difference.
- *"Why should I delete a feature whose story is right?"* → Because "real" and "worth a column" are different tests. −0.0014.
- *"Which metric decides?"* → AUC, because that was committed to in Week 1. On accuracy, D is the worst of B–F.

---

## 🔮 Next Week Preview

Next week the score goes **up**, a long way, and that is the problem. Week 6 opens with a model scoring **0.978** on the delivery data — a fifth of a point better than anything in this week's ablation table — and twelve minutes for the student to find out why, with no hints. The answer is a column called `customer_called_support`, which is only ever filled in *after* a delivery has already arrived late. It is not a model. It is a very expensive `if` statement that reads the answer.

That is one of the **three flavours of leakage**, and all three make the score go up, which is why good news needs auditing harder than bad news. **Target leakage** is the column that only exists because the outcome happened. **Temporal leakage** is shuffling rows across a time boundary so you train on the future — a random split reports 0.8139 and the honest time-based split reports 0.5249, a gap of 0.2890 produced by nothing but where you cut. And **preprocessing leakage** is the quiet one: any statistic worked out before the split. Week 6 makes the student produce **76.5% accuracy on a table of pure random noise**, 200 rows by 2,000 columns with a coin-flip label and zero signal in it by construction — and then fix it with one change and watch it fall to 52.0%.

The week also finally fills in the 106 blanks in `driver_experience_months` — properly, with a median learned from the 1,200 training rows only (29.5, not the whole table's 29.0) — plus a bonus 0/1 column marking where the blank was, in case *being missing* is itself a signal.

**Prep early:** three things. **Keep `ablation.py` and `look.py`** — Week 6 runs the same pipeline with one poisoned column added and the contrast only lands if the honest numbers are already familiar. **Read the deletion notes from tonight's homework before the lesson**, because a student who cannot yet delete a feature over −0.0014 will find it very hard to delete one over +0.1926, which is what next week asks. And **regenerate the data with `add_leak=True` tonight and look at the poisoned column yourself** — you want to have found the leak once, unhurried, before you watch somebody else look for it for twelve minutes.

---

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Week 6 ➡](week-06.md) · [Student Guide](../student-guide/week-05.md) · [Workbook](../workbook/week-05.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
