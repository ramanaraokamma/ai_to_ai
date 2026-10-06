# Week 7 — Beat the Baseline

[⬅ Week 6](week-06.md) · [Course Home](../README.md) · [Week 8 ➡](week-08.md) · [Student Guide](../student-guide/week-07.md) · [Workbook](../workbook/week-07.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — no new ideas, one new discipline, and a tournament |
| **Big idea** | Improving a model by changing only the features is a **discipline**: one change, one measurement, one row in the table, no exceptions. |
| **New vocabulary** | feature set · ablation table · regression (a change that made it worse) · leak hunt |
| **New maths** | **None.** This week practises what they already have. Every number on the page is a subtraction of two AUCs, and they have been subtracting since Week 5. |
| **New syntax** | `pipe.set_params(prep__num__scaler=MinMaxScaler())` · `X.drop(columns=[c])` · `df.to_string(index=False)` |
| **Dataset** | The same numpy-generated pizza-delivery table from Weeks 1–6: `make_data.py`, `seed=0`, 2,020 rows. Plus one supplied file, `leaky_features.py`, which has a bug planted in it on purpose. **Nothing downloads. No internet needed.** |
| **Materials** | The printed workbook (Warm-Up, Do the Maths by Hand, Practice Set A, and the Build It page, which carries the predict-the-sign table, the ablation table, the leak hunt and the defence) · **a big sheet of paper or a whiteboard for the ablation table** (this is the lesson's centrepiece) · a red pen for striking out illegal rounds · a timer that can do six minutes · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. **No new installs this week.** `make_data.py` from Week 1 must still exist in the folder. You must place `leaky_features.py` in the folder before class — the full text is in the Prep Checklist. |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `bench.py` **under 2 seconds**. `leak_hunt.py` **under 2 seconds**. Nothing this week takes longer than a breath. If something runs for a minute, something is wrong. |

> **⚠️ Watch out:** the thing that ruins this lesson is not a technical failure. It is a student who changes three things at once, gets a better number, and cannot say which change earned it. **The table on the wall is the whole lesson.** Guard it. Any round with two changes in it gets struck out in red and re-run — and the first time you do that, do it cheerfully and immediately, because it sets the rule for the rest of the year.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Improve Week 3's validation score using only feature changes** inside the `ColumnTransformer`, with **no change to the model** — same `LogisticRegression`, same settings.
2. **Keep an ablation table with at least six rows**, in which every row records **exactly one change** and its measured delta.
3. **Find the planted leakage bug in `leaky_features.py`**, name which flavour it is, and report the score before and after the fix.
4. **State their chosen final feature set** and defend every inclusion with a number from their own table.

Observable evidence: an ablation table of at least six rows, on paper and in code, where every row names one change and carries a delta to four decimal places; a stated best validation AUC with the split named out loud; and a leak-hunt writeup naming the flavour, the fake score and the honest score.

---

## 🧑‍🏫 What YOU Need to Know First

Read this section once before class. It explains the habit being taught, the new code, the real numbers and the mistakes to expect.

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is no new mathematics this week and no new idea.** That is deliberate and it is a relief: Week 6 was heavy. This week you are teaching a *habit*. Read this section once, about fifteen minutes, and you will be ahead of the student — and much more importantly, you will know exactly which behaviour to stop the moment you see it.

### 1. What the student is actually doing today, in one paragraph

They have a working machine from Week 3: a `Pipeline` that takes the raw delivery table, fills in the missing driver-experience values, puts the number columns on the same ruler, turns the word columns into 0/1 columns, and fits a `LogisticRegression`. On the validation pile it scores **0.7541** on the metric they committed to in Week 1 (ROC AUC). Today they are going to try to make that number bigger — **without touching the model at all.** The only things they may change are the columns going in: add an invented column, remove a column, swap one scaler for another.

And the rule, which is the whole week: **one change at a time, measured, written down, and only then the next change.**

### 2. Why "one at a time" is not fussiness — it is the only way the numbers mean anything

This is the bit to have straight in your own head, because a bright student will push back on it.

Suppose you change two things at once — you add a new column *and* you swap the scaler — and the score goes up by 0.004. What have you learnt?

**Almost nothing.** There are four possible worlds, and your one number cannot tell them apart:

| World | Change A did | Change B did | Total |
|---|---|---|---|
| 1 | +0.004 | 0.000 | +0.004 |
| 2 | 0.000 | +0.004 | +0.004 |
| 3 | +0.010 | −0.006 | +0.004 |
| 4 | −0.006 | +0.010 | +0.004 |

In world 3 you have just quietly shipped a change that **loses** you 0.006 and never found out. Next month somebody removes change A for an unrelated reason and the model gets mysteriously worse.

One change per measurement makes those four worlds distinguishable. That is the entire argument, and it is the same argument as a school science experiment: **change one variable, hold everything else still.** Say it exactly that way, because the student has met it in science and will recognise it.

> **This week's one sentence:** "One change, one measurement, one row. If a row has two changes in it, throw the row away — it cannot tell you anything."

![One change, one measurement, one row](../figures/fig-w07-1-one-change-one-row.svg)
*Figure 7.1 — One change, one measurement, one row. The bottom lane is struck out because nothing on that row says which of the two changes lost the 0.0015.*

### 3. The four new words, in plain English

> **feature set** — the exact list of columns you decided to feed the model. Not "the data" — a written list, which you can read out, and which somebody else could reproduce.

> **ablation table** — the log of your experiments. One row per change: what you changed, the score you got, the difference from before, and whether you kept it. "Ablation" just means *taking something away*; the table grew out of the habit of removing one feature at a time to see what it was worth. We use it for adding as well as removing.

> **regression** — a change that made things **worse**. Nothing to do with "linear regression"; it is the ordinary software-engineering word for "it used to work better than this". Five of our seven changes today end up dropped, four of them true regressions, and that is normal and healthy.

> **leak hunt** — the deliberate audit you run on a suspiciously good score, to find out whether the model is clever or the data is poisoned.

**A warning about the word "regression".** The student has met `LinearRegression` in Level 2 and will be confused for about thirty seconds. Head it off: *"today 'a regression' means 'a change that made it worse'. Two different meanings, same word, and unfortunately both are standard. Programmers say 'that release had a regression in it' and they mean something broke."*

### 4. Every line of this week's code, explained to somebody who has never programmed

Three lines are new this week. Here they are, one at a time, with nothing assumed.

**New line 1 — swapping one part of the machine without rebuilding it.**

```python
pipe.set_params(prep__num__scaler=MinMaxScaler())
```

Read it right to left. `MinMaxScaler()` is one of the two rulers from Week 4 — the one that squashes every column into the range 0 to 1. `pipe` is the whole assembled machine. `set_params` means "change one setting inside this machine".

The strange-looking part is `prep__num__scaler`, and it is **an address, not a word.** Those are *double* underscores, two of them, twice. Read it as a path down through the machine:

```text
pipe
 └── "prep"          the ColumnTransformer that handles the columns
      └── "num"      the branch inside it that handles number columns
           └── "scaler"   the step inside THAT branch that does the scaling
```

So `prep__num__scaler` means *"the thing called `scaler`, inside the thing called `num`, inside the thing called `prep`"*. The double underscore is scikit-learn's way of writing "inside". Every one of those names was chosen by the student when they built the pipeline in Week 3 — they are not magic words, they are labels somebody typed.

**Why does this matter enough to teach?** Because the alternative is retyping the entire twelve-line pipeline just to change one scaler, and when you retype twelve lines you change something you did not mean to. `set_params` changes exactly one thing and provably leaves everything else alone. That is the whole point of the week.

> **⚠️ Watch out:** get the address wrong and you get a long, loud error. Missing out the middle bit — `prep__scaler` instead of `prep__num__scaler` — produces `ValueError: Invalid parameter 'scaler' for estimator ColumnTransformer(...)` followed by a list of the names it *would* have accepted. **That list is the answer.** It is in the Debugging Clinic and you will meet it live.

**New line 2 — throwing a column away.**

```python
X_lean = X.drop(columns=["day_of_week"])
```

`X` is the table of features. `.drop` means "give me a copy with something taken out". `columns=["day_of_week"]` says *which* — and note the **square brackets**, because it takes a *list* of column names, even when the list has one thing in it.

**It gives you a copy.** The original `X` is untouched. That matters: you can drop a column, measure, and still have the full table for the next experiment. If you write `X = X.drop(...)` you have thrown the column away permanently and your next experiment is silently running on a smaller table.

> **⚠️ Watch out:** forget the `columns=` and pandas thinks you meant a *row*, goes looking for a row labelled `"day_of_week"`, does not find one, and says `KeyError: "['day_of_week'] not found in axis"`. Also in the Clinic.

**New line 3 — printing a table so a human can read it.**

```python
print(table.round(4).to_string(index=False))
```

Three things happening left to right. `table` is a DataFrame. `.round(4)` rounds every number to four decimal places — because `0.7585749463...` is not a thing anybody can compare by eye. `.to_string(index=False)` turns the table into neat text **without the row numbers down the left**, which are pure noise on a table whose rows are already labelled `1`, `2`, `3`. And `print` puts it on the screen.

**Why four decimal places and not two?** Because our whole week's honest gain is **0.0058**. Round to two and the entire lesson reads `0.75, 0.76, 0.76, 0.75, 0.76…` and vanishes. Say this out loud in class; it is a real decision, not a formatting nicety.

### 5. The table you are going to build, with the real numbers

Here is what the run actually produces. **These are the real numbers from `bench.py`, seed 0, and you will see exactly these on your screen.**

```text
               what I changed  val_auc   delta verdict
1  baseline (Week 3 pipeline)   0.7541     NaN    keep
                 2  + is_rush   0.7586  0.0045    keep
              3  + is_weekend   0.7585 -0.0001    drop
              4  + min_per_km   0.7536 -0.0051    drop
            5  + items_per_km   0.7590  0.0003    drop
    6  scaler -> MinMaxScaler   0.7579 -0.0007    drop
           7  drop order_hour   0.7599  0.0013    keep
          8  drop day_of_week   0.7576 -0.0010    drop
```

![Eight rows, two kept](../figures/fig-w07-2-ablation-table-six-rows.svg)
*Figure 7.2 — Eight rows, two kept. Every row changes exactly one thing, so every delta is attributable.*

**Read this table slowly, because it teaches five separate things and four of them are uncomfortable.**

1. **`is_rush` earned its place.** +0.0045 for one column of 0s and 1s. `order_hour` was already in the model as a number from 10 to 23, and a straight-line model can only say "later is more late" or "later is less late" with it. The truth is a *hump* at 18:00–20:00, which a straight line cannot express and a 0/1 flag can. **That is the entire craft of feature engineering in one example**, and it is worth two minutes.

2. **`is_weekend` bought nothing.** −0.0001. That is not "slightly bad", it is **the same number**, arriving with a different amount of rounding noise. There was no weekend signal in the table to find. **Delete the feature.** A feature that buys nothing costs you maintenance, one more thing to explain, and one more thing to break.

3. **Row 7 is the surprise, and it is the best moment of the lesson.** Dropping `order_hour` — a real column, out of the actual file — makes the model **better** by 0.0013. Why? Probably because `is_rush` already carries the useful part of `order_hour`, and the raw hour column adds a straight-line story that is not true. That is a hypothesis: +0.0013 is under the 0.005 line (see point 4), so present it as the likely reason, not a proven one. **Once you have the good version of a column, the raw version can be harmful.** Nobody expects this. Let it land.

4. **Row 5 is where you must be honest.** `items_per_km` gained +0.0003. Is that real? **Almost certainly not.** The validation pile has 400 rows. Shuffle it differently and a difference that small will flip sign. We do not yet have the tool to say how big a difference has to be before it counts — that is **Week 11**, where five folds give us a `±`. Until then use a working rule and say it out loud: **on 400 validation rows, treat anything under about 0.005 as "no evidence".** Which, honestly, also puts a question mark over row 7's +0.0013 — and a student who spots that has understood more than the exercise asked for. Praise it, agree with it, and promise Week 11.

5. **The total honest gain is +0.0058.** From 0.7541 to 0.7599. Seven changes tried, two kept, five thrown away, and the reward is half a percentage point. **Say that number out loud without flinching.** Feature engineering is not magic; it is a grind of small defensible gains. It is still usually a better use of an afternoon than fiddling with the model, and the reason is the point of the week: you can *explain* every one of those 0.0058.

### 6. The planted leak, and why it is a different flavour from last week's

Last week the poisoned column was handed to them: `customer_called_support`, a column that only gets filled in *after* the delivery is late. This week the poison is **inside a feature function**, which is much more realistic and much harder to see, because feature functions look like harmless arithmetic.

Here is the crime, and it is three lines long:

```python
_FULL = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
_KEY = ["restaurant", "day_of_week", "weather", "order_hour"]
_LATE_RATE = _FULL.groupby(_KEY)["late"].mean().to_dict()
```

In English: *"take all 2,000 rows. Group them by restaurant, day, weather and hour. For each group, work out what fraction of those orders were late. Remember it in a lookup table."* Then the feature function hands each row its own group's late rate, under the entirely reasonable-sounding name `similar_orders_late_rate`.

**Why this is fatal, in one sentence a 14-year-old will get instantly:** there are 820 groups and 2,000 rows, and **360 of those groups contain exactly one order.** For those 360 rows, "the fraction of orders in this group that were late" is the fraction of *one* order that was late — which is `1.0` if that order was late and `0.0` if it was not. **The feature is the answer with a statistic's name on it.**

![Where the leak was hiding](../figures/fig-w07-3-where-the-leak-was-hiding.svg)
*Figure 7.3 — Where the leak was hiding. For a group of one, "the late rate of similar orders" is just that order's label.*

And here is the payoff, three real numbers:

| What you did | Validation AUC |
|---|---|
| With `similar_orders_late_rate`, lookup built from all 2,000 rows | **0.9240** ← the fake score |
| Same feature set, that one column removed | **0.7535** ← the honest score |
| Same idea, lookup rebuilt from the 1,200 **training** rows only | **0.6115** ← worse than nothing |

**That third row is the one to dwell on.** A student's instinct will be "fine, so compute it properly and keep it". So rebuild the lookup from the 1,200 training rows — and it scores 0.6115, which is *worse than not having the feature at all.* Be precise about why, because the obvious story is wrong: this rebuild is still naive. Every training row sits inside its own group, so for a group of one the training-time value is still that row's own label. Measured: train AUC 0.957, the feature's weight about 2.7, then validation 0.6115, because 28.5% of validation orders fall in groups never seen in training (they get the fallback 0.2875) and the rest get a rate from one or two *other* orders. The model learned to trust a column that is only trustworthy on the rows it was computed from. Computed properly (each row's value from the *other* rows only, out-of-fold, smoothed towards the overall rate) it scores about 0.758 in a quick check — barely above 0.7535 — so the column is worth little on this table even when honest. **The 0.9240 was never a measure of the feature. It was the answer.**

**The flavour is target leakage**, because the poisoned quantity was computed from the `late` column — the answer. (Preprocessing leakage would be computing a *scaler's mean* over all the rows, which is a real bug and a much milder one. Week 6 covered both; today's is squarely the first.)

**And the decisive test is not a number at all.** Ask: *at the moment a customer places an order, does this value exist?* No. Nobody knows yet whether it will be late. The lookup could only be built by a person who already had the answers. That question — **"does this value exist at the moment I need the prediction?"** — is worth more than all four statistical audits put together, and it is the sentence you want them saying by June.

![Baseline, best, and the lie](../figures/fig-w07-4-baseline-to-best-score-ladder.svg)
*Figure 7.4 — Baseline, best, and the lie. The honest afternoon's work is the small step at the bottom.*

### 7. The three misconceptions you will actually meet

**Misconception 1 — "more features is better."**
It is the single most common belief in the room and the table refutes it four times over. Rows 3, 4 and 5 all *add* a column and two of the three make it worse (row 6 swaps the ruler and does not help either). The reason is worth saying plainly: every extra column is another weight the model has to estimate from the same 1,200 training rows. Estimating more things from the same evidence means estimating each of them worse. **The best model today has no more columns than the baseline and fewer than row 2** — row 7 swaps the raw hour for its better version — and that is the most surprising line in the file.

**Misconception 2 — "a bigger number means a better model."**
This is the belief the leak hunt exists to kill. 0.9240 is a bigger number than 0.7599 and it belongs to a model that will be useless the moment it is switched on. Give them the rule as a reflex: **on this table, a sudden jump of 0.1 or more from one column means stop and audit.** It is not proof of a bug by itself (removing `distance_km` costs 0.10 honestly); Audit 4, "does it exist yet?", decides. Honest changes here arrived in units of 0.005.

**Misconception 3 — "the validation score is the truth."**
It is a measurement on 400 particular rows, taken with a particular shuffle. It has wobble in it. We do not yet have the machinery to say how much — Week 11 — but today's honest posture is: *a delta under 0.005 on 400 rows is not evidence, and I will say so in writing.* A student who writes "+0.0003, which is probably nothing" on their table has done better work than one who writes "+0.0003, kept".

### 8. How deep to go, and where to stop

**Go this far:** the one-change rule and why; the ablation table as a permanent artifact; `set_params` with its underscore address; `X.drop(columns=[...])`; `to_string(index=False)` and why four decimals; running the leak hunt and naming the flavour; and the sentence *"at the moment I need the prediction, does this value exist?"*

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| Cross-validation, `StratifiedKFold`, mean ± sd | **Week 11.** They will ask "how do I know 0.0003 isn't luck?" The honest answer is *"you can't yet, and that's Week 11's whole job."* Do not sketch it — a half-explained fold is worse than an honest "not yet". |
| Precision, recall, the confusion matrix | **Week 8, next week.** Today the score is AUC, exactly as committed to in Week 1. If somebody asks what AUC actually *is*, the Week 2 answer stands: "the chance that a randomly picked late order scores higher than a randomly picked on-time one." |
| Moving the 0.5 threshold | **Week 10.** Not today, at all. |
| `GridSearchCV`, tuning `C`, changing the model | **Not in Level 3 at all as a lesson**, and explicitly banned today. The whole point is that the model is frozen. If a student changes `LogisticRegression` to a decision tree, their table is void and they know why. |
| `SelectKBest`, automatic feature selection | Mentioned in Week 6's noise experiment; not a tool this year. Choosing by hand with a written reason is the skill. |
| Target encoding done properly (smoothing, out-of-fold) | Genuinely advanced. Today it is enough that the naive version is a leak and that the train-only rebuild (0.6115) is still naive. The careful version scores about 0.758 here, barely above no feature. |
| Opening the test pile | **Week 36.** Somebody will suggest it "just to check". No. |

The line to hold in your head all lesson: **today the student learns to write a row before they change the next thing.** That is it. If they leave with a six-row table in their own handwriting and no new Python at all, the lesson worked.

---

### 9. 🧭 The Growing Map — where Week 7 sits

The student guide carries the same figure every week with one more piece filled in. It is the only thing
in this course that shows the learner the *shape* of the year rather than this week's content. This week
it changes in two places at once, which is worth thirty seconds of pointing.

![The Level 3 pipeline in Week 7: stage two opens and its baseline and four numbers tile is this week's box](../figures/fig-w07-0-where-this-fits.svg)

*Figure 7.0 — Week 7's version. Stage one is white and solid, both tiles done. Stage two, MEASURE IT,
has gone solid because we have crossed into it, and its first tile is gold. The ↻ on stage three is
drawn grey because the training loop stays closed until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, don't explain it.** Ask *"which box did we do today?"* They point at the gold tile —
   *baseline · four numbers*. Pointing is the exercise.
2. **Then the question that belongs to this week.** Stand next to the ablation table on the wall and
   ask: *"we have six rows up there — which one is the baseline, and why does it stay at the top?"* The
   answer you want is that every other row only means anything **as a difference from it**, so it never
   gets deleted and it is still there in Week 36. If somebody says the best row should go on top, that
   is the §7 misconception surfacing, and this is a cheap and cheerful place to correct it.
3. **Point at the two tiles that just went white.** Weeks 4 to 6 are finished work now. Every single row
   in today's table is one decision from those three weeks, finally carrying a number instead of an
   opinion. Say that out loud — it is the whole reason stage one had to come before stage two.

> **🧑‍🏫 Why this is worth two minutes.** A learner who can see the map can distinguish *"I don't
> understand this week"* from *"I don't know where this week goes"* — and those two need completely
> different help from you. Without the map, both arrive at your desk as "I don't get it."

**Two things to notice, so you can answer if asked.**

- **Two threads are lit for the first time: evaluation and model.** A sharp student may object that we
  never touched the model today. That *is* the point — the model is lit because it was pinned
  deliberately still, same `LogisticRegression`, same settings, while only the features moved. Holding
  one thing fixed on purpose is a move on the model thread, and it is the move that makes the table
  readable.
- **The ↻ on stage three is still grey.** It is the training loop and it stays shut until Week 12, when
  the symbol turns black. Do not preview it. *"That's the bit that does the learning, and we take it
  apart in the spring"* is plenty.

> **⚠️ Watch out:** the map is orientation, not assessment. Never quiz them on it. If a student cannot
> remember which thread this week was, that costs nothing at all.

---

## 🧰 Prep Checklist

This section lists everything to set up before class, so nothing has to be fixed live.

### 25 minutes the night before

- [ ] **Check `make_data.py` still exists and still runs.** Everything today imports it.

```bash
cd ~/delivery && python3 make_data.py
```

You must see:

```text
(2020, 10)
 order_id restaurant  distance_km  items  prep_minutes  order_hour day_of_week weather  driver_experience_months  late
   100955     Napoli         2.78      3          15.0          12         Mon   clear                       5.0     0
   101493 CrustyBros         3.09      5          12.9          22         Mon    rain                       0.0     0
   101857 CrustyBros         2.65      2          14.2          16         Mon    rain                      33.0     0
   100215     Napoli         9.60      2           4.9          13         Tue   clear                      27.0     1
   100506 CrustyBros         2.33      5          19.6          20         Thu   clear                      35.0     0
```

**If that shape is not `(2020, 10)`, stop and fix it before anything else.** Every number in this file depends on it.

- [ ] **Create `leaky_features.py` in the same folder. This file is supplied to the student deliberately broken — do not fix it.**

```python
"""leaky_features.py  --  SUPPLIED FILE.  Do not fix it until you have measured it.

Three engineered features.  One of them is poisoned.
"""
import pandas as pd

from make_data import make_deliveries

# Build a lookup of "how often are orders like this one late?"
_FULL = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
_KEY = ["restaurant", "day_of_week", "weather", "order_hour"]
_LATE_RATE = _FULL.groupby(_KEY)["late"].mean().to_dict()


def add_features(d):
    """Add three columns to a copy of the incoming table."""
    d = d.copy()
    d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    rates = []
    for row in d[_KEY].itertuples(index=False, name=None):
        rates.append(_LATE_RATE.get(row, 0.29))
    d["similar_orders_late_rate"] = rates
    return d
```

- [ ] **Run `bench.py` yourself, all the way through.** The complete file is in the Answer Key under Build It — Finish the ablation table (`bench.py`). Create it, run it, and check you get **exactly** this:

```text
train 1200   val 400   test 400

               what I changed  val_auc   delta verdict
1  baseline (Week 3 pipeline)   0.7541     NaN    keep
                 2  + is_rush   0.7586  0.0045    keep
              3  + is_weekend   0.7585 -0.0001    drop
              4  + min_per_km   0.7536 -0.0051    drop
            5  + items_per_km   0.7590  0.0003    drop
    6  scaler -> MinMaxScaler   0.7579 -0.0007    drop
           7  drop order_hour   0.7599  0.0013    keep
          8  drop day_of_week   0.7576 -0.0010    drop

best honest val AUC : 0.7599
total honest gain   : 0.0058
```

**Expected runtime: under 2 seconds.** If your numbers differ, the cause is almost always one of three things: `make_data.py` has been edited, a `random_state` is not `0`, or `drop_duplicates()` is missing.

- [ ] **Run `leak_hunt.py` yourself.** Complete file in the Answer Key under Build It — The leak hunt (`leak_hunt.py`). Expected output:

```text
--- audit 0: the two scores ---
with similar_orders_late_rate : val AUC 0.9240
without it                      : val AUC 0.7535
jump                            : +0.1705

--- audit 1: correlation of every number column with late ---
similar_orders_late_rate    0.676
distance_km                 0.345
min_per_km                 -0.186
is_rush                     0.133
driver_experience_months   -0.123
items                       0.106
prep_minutes                0.066

--- audit 2: that one column, on its own ---
model with ONLY similar_orders_late_rate : val AUC 0.8916

--- audit 3: the biggest weights the model learned ---
num__similar_orders_late_rate    2.071
num__distance_km                 0.971
num__driver_experience_months   -0.411
cat__day_of_week_Sat            -0.269

--- audit 4: the question no number can answer ---
The lookup was built from the 'late' column of ALL 2000 rows.
360 of the 820 groups hold exactly one order, so for those rows
the 'rate' is 1.0 when that order was late and 0.0 when it was not.
VERDICT: target leakage. The feature is the answer, dressed as a statistic.
```

**Expected runtime: under 2 seconds.**

- [ ] **Break it on purpose, twice, so you have seen both live.**
  1. Change `prep__num__scaler` to `prep__scaler`. You get a `ValueError` whose final sentence lists the valid names. **Read that list.** It is scikit-learn handing you the answer.
  2. In `bench.py`, delete `"order_hour"` from the incoming frame with `X_train.drop(columns=["order_hour"])` instead of removing it from the `num` list. You get `KeyError: 'order_hour'` from **inside the feature function**, because `is_rush` is built *from* `order_hour`. This is the good mistake and Step 4 of the live-code stages it deliberately.
- [ ] **Print the whole workbook for Week 7** (sections: Warm-Up · Do the Maths by Hand · Predict the Output · Practice Set A · Practice Set B · Fix the Broken Program · Puzzle of the Week · Think Deeper · Build It · Draw It · Self-Check). The lesson itself uses only Practice Set A (A2) and the Build It page.
- [ ] **Put a big blank table on the wall.** Four columns: `what I changed`, `val AUC`, `Δ`, `keep or drop`. Ten blank rows. **This is the single most important physical object in the room today.**
- [ ] **Find the red pen.** You are going to strike out at least one round.

### 5 minutes on the day

- [ ] Editor open, terminal in the delivery folder. `make_data.py` and `leaky_features.py` both present.
- [ ] `bench.py` and `leak_hunt.py` **deleted or renamed** — they type them.
- [ ] Week 3's saved score written on the board on its own: **`0.7541 on the 400 validation rows`**. Nothing else.
- [ ] The blank ablation table on the wall, and the red pen next to it.
- [ ] Timer set to six minutes and tested.
- [ ] Bug Log out, open at a fresh page.

### Fallback if the laptops fail

**This week survives a total laptop failure better than any other week in the level**, because the discipline is the lesson and the discipline is done in pen.

1. **Hand out the printed table** from §5 above, with the `val_auc` column filled in and the `delta` and `verdict` columns **blank**. Their job: compute all seven deltas by subtraction, and write keep or drop next to each. Seven subtractions of four-decimal numbers. **That is objective 2, complete, on paper.** (Answers in the Answer Key under Workbook answers — Do the Maths by Hand, M1, and Build It — Finish the ablation table.)
2. **Then the harder question, which needs no computer at all:** *"row 7 removes a real column from the file and the score goes UP. How is that possible?"* Give them three minutes and a hint — *"look at row 2"*. **That is the deepest idea of the week and paper delivers it better than a screen**, because both rows are visible at once.
3. **The leak hunt, on paper.** Hand them the printed `leaky_features.py` and the three scores 0.9240 / 0.7535 / 0.6115. Four questions: *"which of the three features is poisoned? What was it computed from? Why does 360 groups of one matter? And at the moment an order is placed, does this value exist?"* **Objective 3, complete.**
4. **The defence.** Write out the final feature set as a list, and beside every column a number from the table that justifies it. **Objective 4, and it is a writing task, not a typing task.**
5. **The tournament, unplugged.** Run it as a prediction game: you read out a proposed change, they write down whether the delta will be positive or negative *and by how much*, then you reveal the real number from the table. Six rounds, scoreboard on the wall. It is genuinely fun and it teaches calibration, which is Week 14's ground.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'make_data'` | The terminal is in the wrong folder. `cd` into the folder that contains `make_data.py`. Nothing is broken. |
| `make_data.py` prints a shape other than `(2020, 10)` | Somebody edited it. Restore it from Week 1 or retype it from the Week 1 file. **Do not proceed with different numbers** — the whole lesson's arithmetic hangs off 2,020. |
| A student's baseline is not 0.7541 | Check three things in order: `random_state=0` in both splits, `drop_duplicates()` present, `stratify=y` present. It is almost always the first. |
| The tournament is running long | Cut rounds, never the table. Four rows written down beats eight rows shouted out. |
| Somebody changes the model | Their table is void from that row on. Say so calmly, strike the rows in red, restart from the last good row. This will happen once, to one student, and handling it without drama is the lesson. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the running order of the lesson, segment by segment.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Suspiciously Good Score | 7 | 7 | 0.9240 on the board. Admire it. Then the question. |
| 🧠 Concept — One Change, One Row | 12 | 19 | The four worlds; the three new words; the wall table gets its header |
| 💻 Live-Code Together — `bench.py` | 15 | 34 | Baseline, then two rows measured. **Two deliberate mistakes.** |
| 🎲 Their Turn — Beat The Baseline Tournament | 30 | 64 | Five six-minute rounds. The wall table fills. Red pen used at least once. |
| 🔑 Wrap & Assign | 6 | 70 | Three checks, the takeaway, homework |

> **📌 Why this is not the standard 7 / 18 / 18 / 20 / 7 shape.** Week 7 is a **lab**: there is no new maths, so the concept segment shrinks, and the tournament needs five timed rounds, so "their turn" grows. The total is still 70 minutes and the five segments are still the five segments.

---

### 🪝 Hook — The Suspiciously Good Score (7 minutes)

**Do this:** Before they arrive, write **only this** on the board, large:

```text
val AUC 0.9240
```

Nothing else. Do not write what it is or where it came from. Sit down.

**Say this:**

> "That's a validation AUC. It's from your delivery model — the same table, the same 400 validation rows, the same LogisticRegression you built in Week 3.
>
> Three weeks ago you got 0.7541 on those same 400 rows. Somebody has been busy, and now it's 0.9240.
>
> First question, and I want an honest answer, not a clever one: **how do you feel about that number?**"

Let them answer. What you are hoping for is somebody suspicious, because Week 6 happened. If nobody is suspicious, you have your hook.

> "Right. Let's put it in proportion. In a minute you are going to spend half an hour trying to improve that 0.7541. Here's what you'll get, and I'll tell you now so it doesn't disappoint you later: **0.7599.**
>
> Fifty-eight ten-thousandths. Zero point zero zero five eight. That is what a good afternoon's honest work on the features is worth."

**Do this:** Write both numbers on the board, one above the other, and the subtraction:

```text
0.7599  -  0.7541  =  +0.0058     <- an afternoon's honest work
0.9240  -  0.7599  =  +0.1641     <- whatever this was
```

**Say this:**

> "0.0058 against 0.1641. One of those is twenty-eight times the size of the other.
>
> So here's the question that runs the whole lesson: **when you see 0.9240, is the right reaction to be pleased, or to be worried?**"

**Ask this:** "What was the rule from last week?"

*Hoped-for answer:* "A suspiciously good score is a bug, not a model."

*If they say "it means the features are better":* do not correct it — ask a follow-up. *"Could a feature be twenty-eight times better than everything else we tried put together?"* The silence does the work.

*If they say nothing at all:* prompt with the noise experiment from Week 6. *"Remember the 2,000 columns of pure randomness that scored 0.75? What made that possible?"*

> "By the end of today you will have found where that 0.9240 came from, and you'll be able to name the flavour of the bug. And more importantly, you'll have a piece of paper on the wall that makes this kind of thing findable — because the reason nobody caught this in real life is almost always that nobody wrote down what they changed."

**Do this:** Stand up, point at the big blank table on the wall, and write the header row in front of them. Say the four column names out loud as you write them.

| what I changed | val AUC | Δ | keep or drop |
|---|---|---|---|

> "One row per change. And **one change per row** — that's the rule, and it's the only rule today."

---

### 🧠 Concept — One Change, One Row (12 minutes)

**Say this:**

> "You've done this in science. If you're testing whether plants grow faster in sunlight, you don't move the plant to the windowsill *and* start watering it twice as much. Because when it grows, you've learnt nothing.
>
> Same thing here. Watch."

**Do this:** On the board, draw this table and fill it in as you talk. Do not skip it — this is the argument.

> "Suppose I change two things at once. I add a new column, and I swap the scaler. My score goes up by 0.004. Here are four completely different worlds that all produce +0.004."

| World | change A did | change B did | total |
|---|---|---|---|
| 1 | +0.004 | 0.000 | +0.004 |
| 2 | 0.000 | +0.004 | +0.004 |
| 3 | +0.010 | −0.006 | +0.004 |
| 4 | −0.006 | +0.010 | +0.004 |

**Ask this:** "Which of those four worlds am I in?"

*Hoped-for answer:* "You can't tell."

> "I can't tell. And look at world three: change B is **losing** me 0.006 and I've just shipped it, because A was carrying it. Six months from now somebody deletes A for an unrelated reason and the model mysteriously gets worse, and nobody will ever find out why, because nobody wrote a row.
>
> That's the whole discipline. **One change, one measurement, one row.**"

**Do this:** Write the three new words on the board, with their one-line definitions. Say each definition out loud.

> **feature set** — the exact written list of columns you feed the model.
>
> **ablation table** — the log: what I changed, what I got, the difference, keep or drop.
>
> **a regression** — a change that made things worse.

**Say this:**

> "That last one is going to trip you up for thirty seconds, so let's get it over with. You know `LinearRegression`, the model. **This is a different meaning of the same word.** Programmers say 'that update had a regression in it' and they mean something used to be better. Nothing to do with lines.
>
> And I'll tell you now: **five of the seven changes we try today end up dropped, and four of those are true regressions.** That is not failure. That is what the table is *for*. A table where every change succeeded would mean you weren't trying anything risky."

**Ask this:** "Here's a proposal. I add a column called `is_weekend`, and while I'm in there I also change the scaler from StandardScaler to MinMaxScaler, because why not. Is that one row or two?"

*Hoped-for answer:* "Two."

*If they say one:* ask *"if the score goes up, which of the two did it?"*

> "Two rows. And here's the enforcement, so you know it's real: **if a round has two changes in it, I strike the row out in red and you re-run it.** Not as a punishment — because the row is genuinely worthless and leaving it there is worse than having no row."

**Do this:** Hand out workbook Practice Set A, item A2 ("One change or more?") and give them four minutes on it, in pen. Six described experiments; they mark each as one change or more, and rewrite the bad ones as separate rows. Walk round. **Do not help beyond re-reading the description out loud.**

**Then:** the "Predict the sign" table on the Build It page, two minutes, also in pen. Four candidate changes; they predict the *sign* of each delta before any code runs.

> "Pen, not pencil. You are going to be wrong about at least two of these and I want the evidence."

---

### 💻 Live-Code Together — `bench.py` (15 minutes)

**You never touch their keyboard.** They type; you type the same thing on the shared screen.

**Step 1 (4 min) — the baseline, and nothing else.**

New file, `bench.py`. Everything down to the first `print`.

```python
"""bench.py - one change, one measurement, one row."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, MinMaxScaler,
                                   OneHotEncoder, StandardScaler)

from make_data import make_deliveries

BASE_NUM = ["distance_km", "items", "prep_minutes", "order_hour",
            "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("train %d   val %d   test %d" % (len(X_train), len(X_val), len(X_test)))
```

**Ask before running:** "Three numbers are about to print. What are they?"

*Hoped-for answer:* 1200, 400, 400.

Run it. Real output:

```text
train 1200   val 400   test 400
```

> **Say this:** "Nothing new in any of that — it's Week 2 and Week 3, retyped. `drop_duplicates()` because the file has 20 duplicated rows in it and a duplicate that lands in both piles is a row the model has already seen. `stratify=y` so all three piles have the same late rate. `random_state=0` everywhere, so that when your number differs from mine, it's a real difference and not the shuffle.
>
> And `X_test` — 400 rows — is now going to sit there, untouched, for twenty-nine weeks. Do not look at it."

**Step 2 (5 min) — the measuring machine.**

```python
def add_features(d, rush=False, weekend=False, ratio=False, items_ratio=False,
                 inter=False):
    """Row-wise arithmetic only.  Nothing here looks across rows, so nothing can leak."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if weekend:
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    if ratio:
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    if items_ratio:
        d["items_per_km"] = d["items"] / (d["distance_km"] + 0.5)
    if inter:
        severity = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * severity
    return d


def measure(num, cat, kw, drop=(), minmax=False):
    """Fit on train, score on val.  Returns one number."""
    tr = X_train.drop(columns=list(drop))
    va = X_val.drop(columns=list(drop))
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scaler", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
    ])
    pipe = Pipeline([("derive", FunctionTransformer(add_features, kw_args=kw)),
                     ("prep", prep),
                     ("model", LogisticRegression(max_iter=2000, random_state=0))])
    if minmax:
        pipe.set_params(prep__num__scaler=MinMaxScaler())
    pipe.fit(tr, y_train)
    return roc_auc_score(y_val, pipe.predict_proba(va)[:, 1])
```

> **Say this:** "`measure` is the referee. You hand it a feature set, it hands you back one number. It is the *only* place in this file that fits a model, which means every row in your table was produced by exactly the same procedure. That is not tidiness — it's what makes the rows comparable.
>
> Look at the docstring on `add_features`: **row-wise arithmetic only.** Every line in there looks at one row and does sums with that row's own numbers. Nothing computes an average across rows. Nothing looks at `y`. That's *why* this function is safe to put in a `FunctionTransformer` — and hold that thought, because the file I'm going to hand you later breaks exactly that rule."

**Step 3 (3 min) — the first two rows. 🐞 DELIBERATE MISTAKE ONE.**

Type this, **with the mistake in it**, and do not flag it:

```python
RUSH = {"rush": True}
CHAMP = BASE_NUM + ["is_rush"]

base = measure(BASE_NUM, CAT, {})
print("baseline        : %.4f" % base)
champ = measure(CHAMP, CAT, {})           # <-- the mistake
print("+ is_rush       : %.4f" % champ)
```

Run it. Real output:

```text
baseline        : 0.7541
Traceback (most recent call last):
  ...
ValueError: A given column is not a column of the dataframe
```

**Do this:** Stop. Ask: "Read me the last line. Which column is it talking about, and did I ever make it?"

> **Say this:** "Look at the second call. I passed `CHAMP`, which *lists* `is_rush`… and I passed `{}` as the settings, which tells `add_features` to build nothing. So the column is in the list and not in the table, and `ColumnTransformer` went looking for a name that was never made. That was the loud direction."

**Do this:** Now type the quiet direction, on purpose:

```python
oops = measure(BASE_NUM, CAT, RUSH)     # is_rush BUILT, but never listed
print("+ is_rush (built, not shown): %.4f" % oops)
```

```text
+ is_rush (built, not shown): 0.7541
```

**Ask this:** "That is identical to the baseline to four decimal places. Is that possible?"

*Hoped-for answer:* "No — you added a column, something should have changed."

> **Say this:** "Something should have changed. So either `is_rush` is worth *exactly* nothing to four decimal places — which would be a remarkable coincidence — or **the change I thought I made never happened.** This time the column *was* built, but it was never in the list of columns the model is shown.
>
> **This is the most dangerous kind of bug in the whole of this term: the one that gives you a plausible number.** Write both directions in the Bug Log now, before we fix it."

**Do this:** Bug Log entry. Ninety seconds. Message: *"A given column is not a column of the dataframe"* (loud) and *"two rows scored identically to 4 dp"* (silent). Meaning: *"the list of columns and the switches that build them disagree"*. Fix: *"make the two lists agree: pass the kw_args AND the column name"*. Then fix it live:

```python
champ = measure(CHAMP, CAT, RUSH)
```

Run again:

```text
baseline        : 0.7541
+ is_rush       : 0.7586
```

> **Say this:** "0.7586. Now subtract."

**Do this:** Go to the wall. Write rows 1 and 2 in front of them, saying each cell out loud.

| what I changed | val AUC | Δ | keep or drop |
|---|---|---|---|
| 1 baseline (Week 3 pipeline) | 0.7541 | — | keep |
| 2 + is_rush | 0.7586 | +0.0045 | keep |

> "0.7586 minus 0.7541 is 0.0045. **That is the first honest row of the day and it took eleven minutes.** Get used to that ratio."

**Ask this:** "`order_hour` was already in the model. Why does a 0/1 flag beat a number that contains strictly more information?"

*Hoped-for answer:* "Because the model draws a straight line, and rush hour is a bump in the middle, not a slope."

*If they are stuck:* draw it. Hours 10 to 23 along the bottom, lateness up the side, a hump over 18–20, and one straight line trying to follow it. The picture answers the question.

**Step 4 (3 min) — 🐞 DELIBERATE MISTAKE TWO, and the good `KeyError`.**

> **Say this:** "Row 7 on my list is 'drop `order_hour`'. Let me try the obvious thing."

Type this, run it:

```python
print("drop order_hour : %.4f" % measure(CHAMP, CAT, RUSH, drop=("order_hour",)))
```

Real output, last four lines of the traceback:

```text
  File "/private/tmp/l3w789/bench.py", line 30, in add_features
    d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    ...
KeyError: 'order_hour'
```

**Ask this:** "Read me the last line. Then tell me which of our files it happened in."

*Hoped-for answer:* `KeyError: 'order_hour'`, inside `add_features`, in our own file.

> **Say this:** "So: I threw `order_hour` out of the *table*, and then `add_features` went looking for it to build `is_rush` — because **`is_rush` is made out of `order_hour`.** You can't throw away the ingredient and keep the cake.
>
> What I actually meant was: build `is_rush` from the hour, and then don't *show the model* the raw hour. Which is a different thing, and it's done by taking the name out of the number list, not out of the table."

Fix it live:

```python
LEAN = [c for c in CHAMP if c != "order_hour"]
print("drop order_hour : %.4f" % measure(LEAN, CAT, RUSH))
```

```text
drop order_hour : 0.7599
```

**Do this:** Bug Log entry, ninety seconds. Then write row 7 on the wall.

| 7 drop order_hour | 0.7599 | +0.0013 | keep |

> **Say this:** "Sit with that for a second. I **removed a real column that came out of the actual file**, and the model got better. Not by much — 0.0013 — but the right direction.
>
> Probably because row 2 already took the useful part out of `order_hour`. What was left may be a straight-line story that isn't true, with the model spending a weight on it. Mind you, 0.0013 is under our own 0.005 line, so that's a hypothesis, not a finding. **Once you've got the good version of a column, the raw version *can* cost you.**"

---

### 🎲 Their Turn — Beat The Baseline Tournament (30 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: five rounds of six minutes; one change per round; every round ends with a row written on the wall in the student's own handwriting; any round containing two changes gets struck out in red and re-run.

Your job for thirty minutes is to sit on your hands, run the timer, and enforce exactly one rule.

---

### 🔑 Wrap & Assign (6 minutes)

**Do this:** Stand at the wall table. Read the whole thing out loud, row by row, including the deltas.

**Say this:**

> "Eight rows: a baseline and seven changes. Two changes kept, five dropped, four of them regressions. Best honest score **0.7599 on the 400 validation rows** — and say it that way, with the pile named, always.
>
> Total gain, 0.0058. And every single ten-thousandth of it is on that wall with a reason next to it. If somebody asks you in six months why `is_weekend` isn't in the model, you point at row 3 and say 'minus 0.0001'."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Do this:** Hand out `leaky_features.py`, printed, and read the three scores out.

> "Homework. This file has three features in it and one of them is poisoned. With it, the model scores **0.9240**. Without it, **0.7535**. Your job is to find which one, name the flavour, and — this is the part I'm marking — say what would have to be true for that number to be real, and why it isn't.
>
> That 0.9240 on the board this morning? That was this. You've now got the tools to catch it."

---

## 🐞 The Debugging Clinic

Use this section to recognise this week's error messages and fix them without giving the answer away.

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Invalid parameter 'scaler' for estimator ColumnTransformer(...). Valid parameters are: ['force_int_remainder_cols', 'n_jobs', 'remainder', 'sparse_threshold', 'transformer_weights', 'transformers', 'verbose', 'verbose_feature_names_out'].` | "There's nothing called `scaler` at that address." | `prep__scaler` instead of `prep__num__scaler` — a level of the address missed out. | `pipe.set_params(prep__num__scaler=MinMaxScaler())`. **And read the list at the end of the message** — those are the names it *would* have taken, and `transformers` being in the list is the hint that you need to go one level deeper. |
| `KeyError: "['day_of_week'] not found in axis"` | "I looked for a **row** called `day_of_week` and there isn't one." | `X.drop("day_of_week")` — the `columns=` was left out, so pandas assumed you meant a row label. | `X.drop(columns=["day_of_week"])`. Both the `columns=` **and** the square brackets. |
| `KeyError: 'order_hour'` ending inside `add_features` | "The feature function needs a column that isn't in the table any more." | The raw column was dropped from the *frame* while a derived feature is still built from it. | Take the name out of the `num` list instead. The column stays in the table, `is_rush` still gets built, and `ColumnTransformer` simply never shows the raw hour to the model. |
| `ValueError: A given column is not a column of the dataframe` | "`ColumnTransformer` was told to use a column name that isn't there." | A derived feature is listed in `num` but never actually built — the `kw_args` that switch it on were not passed. | Pass the switches: `measure(CHAMP, CAT, RUSH)`, not `measure(CHAMP, CAT, {})`. **Check the two lists agree every time.** |
| `ValueError: columns are missing: {'weather'}` | "At predict time the table has fewer columns than at fit time." | A column was dropped from the validation frame but not the training frame, or vice versa. | Drop it in **both** places, which is what the `drop=` argument to `measure` is for. It does `tr` and `va` in the same two lines so they cannot drift apart. |
| `ValueError: y should be a 1d array, got an array of shape (400, 2) instead.` | "I wanted one number per row, you gave me two." | `roc_auc_score(y_val, pipe.predict_proba(va))` without `[:, 1]`. | `pipe.predict_proba(va)[:, 1]` — column 1 is the probability of the positive class. |
| **No error. Two rows score identically to four decimal places.** | Nothing crashed. The change you thought you made did not happen. | Usually a column that was built but never listed in `num` (the quiet half of deliberate mistake one; the other half, listed but not built, crashes). Sometimes a typo in a column name that silently produced a column nobody uses. | Print the actual column list going into the model: `print(sorted(add_features(X_train.head(2), **kw).columns))`. If your new name is not in it, it was never made. |
| **No error. A score of 0.92 or higher on this table.** | Nothing crashed. Something is leaking. | A feature computed from `late`, or a statistic computed over all the rows before splitting. | Run the leak hunt. **On this dataset, honest scores live between 0.74 and 0.77. Anything above 0.80 is a bug until proven otherwise.** |
| **No error. `to_string` printed nothing.** | You built the string and then threw it away. | `table.to_string(index=False)` with no `print()` round it. | `print(table.to_string(index=False))`. `to_string` *makes* text; `print` *shows* it. |
| **No error, but every delta is 0.0000 in the table and non-zero on screen.** | Nothing is wrong. | `.round(4)` was applied to the whole table for display, and the deltas really are that small. | Print more digits for the delta column only, or accept it: a delta that vanishes at four decimals is a delta you should not be keeping. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two that are specific to a measurement lab, and they matter more than any traceback.

13. **"Did the number change at all?"** Ask it before anything else. Two identical scores is the loudest signal in the room and the easiest to miss, because nothing goes red.

14. **"Which one thing is different between this row and the row above it?"** If they cannot answer in one sentence, the row is void and they know it without being told. This question replaces almost all correcting.

And the sentence for this week:

> **"On this table, honest lives between 0.74 and 0.77. If you're above 0.80, don't celebrate — go hunting."**

---

## 🎲 The Activity, In Full

This section gives the complete setup, rules and rounds for the tournament.

### Beat The Baseline Tournament

**What it is.** Five timed rounds. In each round the student proposes **one** change to the feature set, predicts the sign of the delta, runs it, and writes the row on the wall in their own handwriting. The table is the deliverable.

### Setup (2 minutes, done during the wrap of the previous segment)

- The big table on the wall, header written, rows 1, 2 and 7 already filled in from the live-code.
- A pen for the student. **They write on the wall, not you.** This matters more than it sounds.
- Your red pen, visible.
- Timer at six minutes.
- The ablation table on the workbook Build It page open in front of them — the paper copy of the same table, which goes home.

### The rules, read out loud before round one

> 1. **One change per round.** One. If your round has two changes in it, I strike the row out in red and you re-run it.
> 2. **Predict first.** Before you press run, write your predicted sign — `+` or `−` — in the margin. In pen.
> 3. **You may not touch the model.** `LogisticRegression(max_iter=2000, random_state=0)` is frozen all lesson. Change it and every row below is void.
> 4. **The row goes on the wall before the next round starts.** No exceptions, even if you are mid-idea.
> 5. **A regression is a result.** You do not get fewer points for a change that made it worse. You get zero points for a row nobody can interpret.

### The five rounds

**Round 1 (6 min) — `+ is_weekend`.** Everybody does this one, so that everybody has the experience of a change that buys nothing. Real answer: **0.7585, Δ −0.0001, drop.**

**Round 2 (6 min) — a ratio.** `min_per_km` = prep minutes ÷ (distance + 0.5). Real answer: **0.7536, Δ −0.0051, drop.** This one is satisfying to lose, because a ratio *feels* clever.

**Round 3 (6 min) — their own invented column.** Free choice. `items_per_km` is the common one: **0.7590, Δ +0.0003, drop** — and the discussion about whether +0.0003 is real is the best three minutes of the lesson.

**Round 4 (6 min) — swap the ruler.** `pipe.set_params(prep__num__scaler=MinMaxScaler())`. Real answer: **0.7579, Δ −0.0007, drop.** Note out loud that this is *not* a feature change at all, which is why it is only one round: it is a reminder that the ruler is a choice too.

**Round 5 (6 min) — take a real column away.** `X.drop(columns=["day_of_week"])`. Real answer: **0.7576, Δ −0.0010, drop.** So `day_of_week` is doing *something*, just not much.

### What "finished" looks like

- **Eight rows on the wall**, each with one change, a four-decimal AUC, a signed delta, and keep or drop.
- **Five of them say "drop"** (and the baseline and two changes say "keep"). If every change says keep, they were not trying anything risky, or they were rounding kindly.
- The student can put a finger on any row and say, in one sentence, what changed and what it cost.
- The best honest score is stated **with the pile named**: *"0.7599 on the 400 validation rows."*
- The workbook Build It ablation table is a copy of the wall, in their handwriting.

### Variation — easier

**Cut to three rounds and hand them the code.** Give them a working `bench.py` with rows 1 and 2 already in it, and let each round be a single edit to one line — the column list. The learning is entirely in *writing the row*, not in typing.

**And cut the prediction step if it is causing paralysis.** Prediction is the second-best part of this activity but the table is the objective.

### Variation — harder

1. **Two changes on purpose, then untangle them.** Run A alone, B alone, and A+B. Then ask: does the A+B delta equal the sum of the two separate deltas? (Not exactly — 0.0018 vs 0.0016 here, a gap too small to interpret.) The general phenomenon is *interaction* between features, it is genuinely interesting, and it is the honest reason "one at a time" is a discipline and not a proof.
2. **Find a change that helps by more than 0.005.** Give them ten minutes. **They will probably fail**, and the failure is the point (if someone succeeds, ask whether it would survive a different split — that is Week 11): the table has already told them the ceiling is about half a point. A student who reports "I tried six things and none of them cleared 0.005" has produced a real result.
3. **Beat 0.7599 with FEWER columns than row 2.** Row 7 got there with one fewer. Can they get two fewer? This pushes hard on "more is not better".
4. **Write the leak yourself.** Inside `add_features`, add `d["cheat"] = y_train` (and list `cheat` in `num`). It does **not** fail: `y_train` is a global, the index lines up at fit time, and the model is silently fitted on a column that is the label. On the validation rows the index does not match, `cheat` is NaN and gets imputed, so the validation score (0.7522 when we tried it) looks innocent while the fitted model is contaminated. `FunctionTransformer` does not *hand* your function `y`, but nothing stops a function reaching for a global. That is exactly how `leaky_features.py` works.
5. **Argue with row 5.** Write the case, in one paragraph, that `items_per_km`'s +0.0003 should be kept. Then write the case against. Whichever one is better argued wins, and the answer key has both.

---

## ❓ Questions Students Ask This Week

These are the questions most likely to come up, with suggested answers.

**"0.0058? That's it? That's the whole afternoon?"**

Yes, and you should be suspicious of anybody who tells you otherwise.

Here is the honest picture of where model improvements come from, in rough order of size: **more data** (big, expensive, slow), **a genuinely new source of information** (big, usually impossible), **better features** (small, cheap, and yours), **a different model** (small, and mostly a lottery), **tuning the model's settings** (usually tiny, and the thing beginners spend all their time on).

Feature engineering is the third one. It is small. But it is the one you can do this afternoon with no budget, and — the part that actually matters — **it is the only one where you end up understanding your problem better than you did at breakfast.** You now know that lateness has a hump at rush hour and that the day of the week barely matters. Nobody knew that this morning. That knowledge outlives the model.

**"Why can't I change the model? A decision tree would probably do better."**

It might. And the moment you change it, your table stops meaning anything.

Every row on that wall says "with this model, this feature change was worth this much". Swap the model and all eight rows are about a machine that no longer exists. You would have to re-run every one.

There is also a harder reason, and it is the professional one: **when two things can change, people quietly change both and report the good number.** Freezing the model for a whole session is a discipline that keeps you honest with yourself. Change the model on a different day, with the features frozen, and write *that* table.

**"How do I know +0.0003 isn't just luck?"**

**You don't, and that is the correct answer today.** Say it exactly like that.

Your validation pile is 400 particular rows chosen by one particular shuffle. Choose a different shuffle and you get a slightly different number. How much slightly? You cannot say yet, and you should not pretend to.

What you can do is use a working rule and write it on your table so future-you knows what past-you believed: **on 400 rows, anything under about 0.005 is not evidence.** By that rule, row 5's +0.0003 is nothing, and — awkwardly — row 7's +0.0013 is nothing either. That awkwardness is real and you are allowed to feel it. **Week 11 gives you the actual instrument**: run it five times on five different splits and report the average *and* the spread. Then "is 0.0003 luck?" becomes a question with a number for an answer.

**"If a feature makes it worse, isn't the model just bad at ignoring it?"**

Sharp question, and the answer is genuinely interesting.

A perfect model *would* ignore a useless column: it would give it a weight of zero. But the model does not know the column is useless. It only sees 1,200 training rows, and in 1,200 rows a useless column will, by pure chance, line up slightly with the answer. So the model gives it a small non-zero weight — and that weight is fitted to a coincidence in the training rows, which will not repeat in the validation rows.

So the cost of a useless feature is not that the model is stupid; it is that **the model has to spend some of its limited evidence deciding the column is useless, and it never quite finishes.** With 1,200 rows and 20 columns there is enough evidence to go round. With 1,200 rows and 2,000 columns there is not — which is exactly what Week 6's noise experiment showed you.

**"The leak got 0.9240. Couldn't we just... use it? If it works, it works."**

This is the best question of the week and you should let the student sit in it for a moment before answering, because the answer is a *demonstration*, not an argument.

It does not work. Try it. **At the moment a customer taps "order", the lookup cannot be built**, because it is built out of whether orders were late, and this one has not happened yet. So on the first real request the column has no value. Fill it with the average and the model's biggest weight is now pointing at a constant, and your 0.9240 model performs at about 0.73 (we measured 0.7298) — worse than the 0.7535 of a model that never had the column. That is not a small degradation; it is a completely different model.

And a naive train-only rebuild of it scores **0.6115** — worse than not having it — and even a careful one is barely better than nothing. **The 0.9240 was never a measure of the feature. It was only the answer.**

**"Which features should I actually keep, then? Just the two that helped?"**

That is the right instinct and here is the sharper version of it. Keep a feature if you can point at a **number** that says it earned its place. Drop it otherwise. Write both lists down.

The subtle part: **"drop" does not mean "wrong idea".** `is_weekend` was a perfectly sensible hypothesis — weekends really might be different. You tested it, the answer was no, and now you know something about pizza that you did not know before. The table is a record of things you have *learnt*, not a record of things you got wrong.

**"Is there a right answer to which features to use?"** *(Nobody fully agrees, and here is why.)*

**No, and this is one of the genuinely unsettled arguments in applied machine learning.** Being straight about it is better than pretending.

**What everybody agrees on:** a feature that leaks must go, always, no argument. And you must be able to say where every feature came from.

**Where it splits.** One camp says **keep it lean**: fewer features, every one justified by a number, because a lean model is easier to explain, cheaper to run, less likely to break when one input source goes wrong at 3am, and less prone to fitting coincidences. Our row 7 is this camp's whole argument in one line.

The other camp says **keep almost everything and let the model sort it out**: use a model with strong built-in penalties for unhelpful columns, throw in every column you have, and accept that you will not be able to explain all of it. On big datasets this camp frequently wins on score. It is how most competition-winning models are built.

**And there is a third position which is harder and probably the most honest:** the argument is unresolvable as stated, because "better" is not one thing. A lean model and a sprawling model can score identically and still be wildly different products — one you can debug at 3am and explain to a regulator, one you cannot. **Which you should prefer depends on what happens when it is wrong**, and that is not a question about data at all.

What to tell a 14-year-old, out loud: **"there's no right answer, but there is a right habit: whichever features you keep, be able to point at the number that put them there."**

---

## ⚠️ Where This Lesson Goes Wrong

This section lists the common failures and what to do the moment you see each one.

| What happens | Why | What to do right now |
|---|---|---|
| **A student changes three things, gets a good number, and is delighted** | It is genuinely faster and the number is genuinely bigger | Strike the row out in red **immediately and cheerfully**, in front of everybody, and say why in one sentence: *"which of the three did it?"* Then re-run it as three rows. **Do this the first time it happens or you will never do it.** |
| The table stays in the laptop and never reaches the wall | Typing is faster than walking across the room | The wall table is the objective, not a display of it. **No round ends until the row is written.** Enforce it as hard as you enforce one-change-at-a-time. |
| Deltas get computed to two decimals and the whole lesson vanishes | 0.75 to 0.76 looks like nothing happened | Four decimal places, on the wall, from row one. Show them: our entire gain is 0.0058. At two decimals it does not exist. |
| Nobody can say which pile a number came from | The number feels self-explanatory | Every score said out loud gets the pile: *"0.7599 on the 400 validation rows."* Ritual 3 from the orientation. Do not let a bare number past you. |
| "More features must be better" survives the whole lesson | It is the intuition everybody arrives with | Point at rows 3, 4 and 5 — three added columns, two of them worse. Then point at row 7: **the best model has one fewer column than row 2 and no more than the baseline.** Make them read row 7 aloud. |
| A tiny positive delta gets treated as a win | +0.0003 is positive, and positive feels like winning | Ask one question: *"if we reshuffled the validation rows, would that 0.0003 survive?"* Then be honest that you cannot answer it yet, and name Week 11. **Do not fake certainty.** |
| A student is crushed by five drops | Five drops out of seven changes feels like failing | Reframe before it sets in (four are true regressions, one is a tiny gain that did not clear the bar): *"you now know five things about pizza deliveries that nobody in this room knew an hour ago."* A regression is a result. Say it every time you write one. |
| The `KeyError: 'order_hour'` derails ten minutes | It is a confusing error the first time | It is deliberate mistake two and it is on the schedule. Read the last line, name the file, name the function, fix it, Bug Log, move on. **Three minutes, not ten.** |
| Somebody "fixes" `leaky_features.py` before measuring it | Fixing a bug feels like the responsible thing | Stop them warmly: *"if you fix it now you'll never know what it was worth."* The fake number is the evidence. Measure first, then fix. |
| The leak hunt turns into a hunt for the syntax error | The file looks unfamiliar | The file **runs fine.** Say so up front: *"there is nothing wrong with this file as Python. It runs. The bug is in what it means."* That single sentence saves ten minutes. |
| The tournament overruns and the wrap gets cut | Five rounds of six minutes always wants to be seven | Timer, out loud, on the wall. Cut a round rather than the wrap — the wrap is where they say the takeaway, and a takeaway they never said is a takeaway they do not have. |

---

## 🧭 Differentiation

This section shows how to adjust the lesson for a student who is struggling, flying or disengaged.

### If the student is struggling

**Cut:** `set_params` and the scaler swap entirely — that is round 4 gone. It is the least important row on the table and its address syntax is the fiddliest thing in the week.

**Cut:** the prediction-first step. Predicting the sign is valuable and it is not an objective.

**Cut:** the tournament to three rounds: `+ is_weekend`, `+ items_per_km`, `drop day_of_week`. One addition, one invention, one removal. That is enough to make the point.

**Give them `bench.py` complete**, with rows 1 and 2 already in it. All of today's learning is in *writing the row*, and none of it is in typing a `ColumnTransformer` they built four weeks ago.

**The version of the arithmetic that skips everything hard.** There is no algebra this week, so the scaffold is a subtraction table. Hand them this, filled in on the left and blank on the right:

| row | val AUC | Δ from row 2 (0.7586) |
|---|---|---|
| 3 | 0.7585 | |
| 4 | 0.7536 | |
| 5 | 0.7590 | |
| 6 | 0.7579 | |
| 7 | 0.7599 | |
| 8 | 0.7576 | |

Six subtractions. Then one question: **"circle every row where the number went up."** Two of them. **That is objective 2, delivered with a pencil.**

**The copy-this-exactly scaffold.** Four lines that change one thing and measure it. This runs, given the `measure` function from the live-code:

```python
CHAMP = BASE_NUM + ["is_rush"]
before = measure(CHAMP, CAT, {"rush": True})
after = measure(CHAMP + ["is_weekend"], CAT, {"rush": True, "weekend": True})
print("before %.4f   after %.4f   delta %+.4f" % (before, after, after - before))
```

```text
before 0.7586   after 0.7585   delta -0.0001
```

Then two questions and nothing else: **"did it go up or down? and is that one change or two?"** Down, and one. That is the whole discipline in four lines.

**One thing you must not cut:** writing the row on the wall. If the entire lesson collapses to a single act, make it *"change one thing, and write down what it did."*

### If the student is flying

None of these need syntax from a later week.

1. **Untangle two changes** (Variation-harder 1): A alone, B alone, A+B, and does the sum add up? It does not, and *interaction* is a real idea they can now name.
2. **Beat 0.7599 with fewer columns still** (Variation-harder 3). Row 7 removed one. Can they remove two and hold the score?
3. **Try to write the leak by hand** (Variation-harder 4) and discover that it does *not* crash: `FunctionTransformer` does not pass `y` in, but a function can still reach a global `y_train`, and the result is a silently contaminated model. Ask them why that is more dangerous than an error. **This is the deepest question available today.**
4. **Argue both sides of row 5** (Variation-harder 5). Two paragraphs. The answer key has both.
5. **The honest question:** *"our best is 0.7599. What is the highest score this table could possibly support, with perfect features?"* Nobody knows — and the reason is that some lateness is genuinely random (a driver got a puncture) and no feature can predict it. That ceiling has a name, **irreducible error**, and it is Week 14's ground. A student who arrives at "some of it is just luck" on their own has had an excellent week.
6. **Rebuild the leak honestly and explain 0.6115.** Why is a properly-computed version *worse than nothing*? (Because the rebuild is still naive: each training row is counted in its own group, so the model learns to trust the column on training rows and it does not transfer; with 647 groups over 1,200 rows most groups hold one or two orders.) This is a genuinely advanced insight and it is available today.

### If the student won't engage today

**Close the laptop. The wall table and a pen.**

Hand them the printed eight-row table with the AUC column filled in and everything else blank. Then three instructions, and nothing else:

> **"Fill in the Δ column. Six subtractions."**
>
> **"Circle every row where the number went up."**
>
> **"Now tell me: how many of the eight changes were worth making?"**

Two. And then the one question that usually reopens the door, because it is genuinely surprising and it does not feel like schoolwork:

> **"Row 7 throws away a real column from the actual file, and the score goes UP. How is that possible?"**

That is objectives 2 and 4 delivered with a pencil in ten minutes, and it is the half of the lesson everything from here to Week 36 sits on. The typing survives to next week, which is about metrics and starts fresh.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the one-change rule (spoken, 45 seconds)**

> "I add two new columns and swap the scaler, all in one go, and my score goes up by 0.006. **What have I learnt?**"

*Good answer:* "Nothing you can use. Any of the three changes could have done it, and one of them might be losing you score while the others carry it."

**What to catch:** "that the changes helped". Push once: *"which one?"*

**Check 2 — reading the table (spoken, 60 seconds)**

> "Row 7 is 'drop `order_hour`', and the delta is **plus** 0.0013. **We removed a real column from the file and the model got better. How?**"

*Good answer:* "Because `is_rush` already carries the useful part of `order_hour` — the rush-hour hump. What was left was a straight-line story that isn't true, and it was costing the model a weight."

**Full marks needs the connection back to row 2.** A student who says "the column was useless" has half of it; the other half is *why it was useless now and not before*. Push once: *"was it useless in row 1?"*

**Check 3 — the leak reflex (spoken, 90 seconds)**

> "Somebody hands you a delivery model and says it scores **0.94** on validation. **What do you do first, and what do you say?**"

*Good answer:* "I don't celebrate. On this table honest scores are 0.74 to 0.77, so 0.94 is a bug until proven otherwise. First I'd look at every feature and ask whether its value exists at the moment the order is placed. Then I'd check the correlations and train a model on each column alone."

**What to catch:** any version of "that's great". The reflex you are building is *suspicion proportional to the size of the jump*, and the fastest way to install it is to make them say the 0.74–0.77 range out loud.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Changes several things at once. Cannot say what produced a number. Reports scores with no pile named. Treats every positive delta as a win. |
| **2 — Emerging** | Changes one thing at a time when reminded. Fills in the table when told to. Computes deltas correctly. Does not yet distinguish a real gain from noise. |
| **3 — Secure** | Runs six or more single-change experiments unprompted and writes every row. States the best score **with the split named**. Can defend each kept feature with a number. Finds the planted leak and names the flavour. **This is the target.** |
| **4 — Strong** | Predicts the sign before running and is right more often than not. Explains row 7 by pointing at row 2. Says out loud that +0.0003 on 400 rows is not evidence. Reports the fake, the honest and the properly-computed-but-still-bad score for the leak, and explains all three. |
| **5 — Exceptional** | Notices unprompted that row 7's +0.0013 is inside the same noise band as row 5's +0.0003, and says so on the table. Explains why `FunctionTransformer` structurally cannot leak the labels. Argues that a leaner model can be the right choice even at equal score, on grounds that are not about score at all. |

---

## 📤 Homework to Assign

This section gives the wording for setting the homework.

**Say this:**

> "About an hour, and most of the marking is on the Build It page.
>
> **First, the Build It page — the ablation table. Six rows minimum**, and every row is one change with its delta to four decimal places and a keep-or-drop. Copy across the rows we did together, then add your own. **At the top of the table write your best validation AUC and the pile it came from.** Not '0.7599'. '**0.7599 on the 400 validation rows.**' And fill in the *Predict the sign* table in pen before you run anything.
>
> **Second, still on Build It — the leak hunt.** Run `leak_hunt.py` and fill in all five audits. Then answer four things: **which of the three features is poisoned**, **which flavour of leak it is**, **the fake score**, and **the honest score**. And one sentence I want in your own words: *at the moment a customer places an order, does that value exist?*
>
> **Third, the defence table on the same page — and this is the part I'm actually marking. Defend your final feature set.** Write out every column you kept, and next to each one **a number from your own table**. Then every column you dropped, with its number. If you cannot put a number next to a decision, you have not finished the experiment — go and run it.
>
> **Also, before next week:** the Warm-Up, *Do the Maths by Hand* (M1 to M4, calculator only), and *Fix the Broken Program*. The other sections — Predict the Output, Practice Sets A and B, the Puzzle, Think Deeper and Draw It — are there if you want more; tell me which ones you did."

**Workbook sections:** Practice Set A (A2) and the Build It predict-the-sign table in class · **Build It (ablation table, leak hunt, defence), Warm-Up, Do the Maths by Hand and Fix the Broken Program** at home · everything else optional.

**Expected time:** 20 min finishing the table and its deltas · 20 min on the leak hunt and its four answers · 20 min writing the defence. **About 60 minutes for the Build It page**, plus roughly 30 for the Warm-Up, M1–M4 and Fix the Broken Program if you set them.

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — does every row contain exactly one change?** Any row naming two things is a zero for that row, and say why on the page. **Two — is there a number beside every keep and every drop in the Build It defence table?** A defence that says "I kept `distance_km` because distance obviously matters" has not done the work, however true it is. **Three — does the leak answer name the flavour AND say why the fake number could never be real?** The good answer is something like *"target leakage — the column was worked out from the `late` column, and 360 groups hold one order, so for those rows the 'rate' is just that order's answer. At the moment the order is placed nobody knows if it'll be late, so the column would be empty in real life."* An answer that says "it's leakage because the score was too high" has spotted the smell and not the cause.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

**Where things are in the workbook.** The key is organised by the workbook's own sections and item labels. The older lesson-handout names ("Page 7.1" to "Page 7.6") survive only in brackets in the headings of the Build It sections and the A2 notes further down; this table maps them.

| Workbook section (item labels) | Answered in this key under |
|---|---|
| Warm-Up (W1–W5) | Workbook answers — Warm-Up |
| Do the Maths by Hand (M1–M4) | Workbook answers — Do the Maths by Hand |
| Predict the Output (P1–P4) | Workbook answers — Predict the Output |
| Practice Set A (A1–A6) | Workbook answers — Practice Set A; A2 also has the older "Page 7.1" notes below |
| Practice Set B (B1–B5) | Workbook answers — Practice Set B |
| Fix the Broken Program (Bugs 1–3) | Workbook answers — Fix the Broken Program |
| Puzzle of the Week (Parts 1–2) | Workbook answers — Puzzle of the Week |
| Think Deeper (T1–T2) | Workbook answers — Think Deeper |
| Build It: predict the sign | Build It — Predict the sign (formerly "Page 7.2") section, below |
| Build It: ablation table | Build It — class wall table and Finish the ablation table (formerly "Page 7.3", "Page 7.4") sections, below (`bench.py`) |
| Build It: leak hunt | Build It — The leak hunt (formerly "Page 7.5") section, below (`leak_hunt.py`) |
| Build It: defence table | Build It — Defend your final feature set (formerly "Page 7.6") section, below |
| Draw It · Self-Check | Workbook answers — Draw It, Self-Check |

> **🧑‍🏫 One rounding trap when marking by hand.** `bench.py` prints **−0.0051** (row 4) and **+0.0003** (row 5). A student subtracting the already-rounded table values (M1, A6, B2) gets **−0.0050** and **+0.0004**. Both are correct arithmetic on the numbers given; accept either, and do not change the keep/drop verdicts, which are the same either way. The workbook answers below use the hand-subtraction values; the Build It sections use the `bench.py` values.


### Workbook answers — Warm-Up

**W1.** **Target leakage** — a column that only exists, or only gets filled in, **because the outcome already happened** (`customer_called_support`, fake 0.9762 against honest 0.7752). **Temporal leakage** — rows shuffled across a **time** boundary, so the model trains on the future and is tested on the past (0.8139 against 0.5249). **Preprocessing leakage** — a statistic worked out over **all** the data before the split: a mean, a median, or a choice of which columns to keep (0.765 against 0.520).

**W2.** **29.5, the median of the training rows.** The fill-in number is a thing the model *learns*, so it may only be learned from the rows the model is allowed to see. 29.0 was worked out partly from the 800 rows you were about to be marked on, so a score measured against them is measured against numbers that already knew something about the answers.

**W3.** **0.7723 − 0.7752 = −0.0029.** It made the model worse, so **the column goes.** A new column earns its place or it leaves — that is the Week 5 habit surviving contact with a new tool.

**W4.** **Preprocessing leakage.** No individual column was poisoned and no time boundary was crossed. The bug was *choosing* the 20 columns while looking at every label — a decision made over all the data, before the split. With 2,000 pure-noise columns you get 2,000 chances to get lucky, and 20 of them look wonderful by accident.

**W5.** ***"At the moment I need the prediction, does this value exist?"*** If the answer is no, the feature is poison no matter how good the score looks — and no arithmetic is required to find that out.

### Workbook answers — Do the Maths by Hand

**M1.**

| row | val AUC | measured against | Δ | keep / drop |
|---|---|---|---|---|
| 2 | 0.7586 | 0.7541 | **+0.0045** | **keep** |
| 3 | 0.7585 | 0.7586 | **−0.0001** | **drop** |
| 4 | 0.7536 | 0.7586 | **−0.0050** | **drop** |
| 5 | 0.7590 | 0.7586 | **+0.0004** | **drop** |
| 6 | 0.7579 | 0.7586 | **−0.0007** | **drop** |
| 7 | 0.7599 | 0.7586 | **+0.0013** | **keep** |
| 8 | 0.7576 | 0.7586 | **−0.0010** | **drop** |

> **🔢 The maths, slowly — and this is worth two minutes of your life.** `bench.py` prints **−0.0051** for row 4 and **+0.0003** for row 5, and you just wrote **−0.0050** and **+0.0004**. **You are not wrong and neither is the computer.** Row 4's real score is `0.75356217`, and `0.75356217 − 0.75862700 = −0.00506484`, which rounds to **−0.0051**. You subtracted the numbers *after* they had been rounded to `0.7536`, so you got **−0.0050**. Same for row 5: the real delta is `+0.00033562`, but `0.7590 − 0.7586` is `+0.0004`.
>
> **The rule this teaches: round at the end, never in the middle.** A tenth of a ten-thousandth does not matter today. It matters enormously in Week 15, when thousands of tiny numbers get added up.

**M1(a).** `0.7599 − 0.7541 = **0.0058**`.

**M1(b).** **Four** of the seven deltas are negative: rows 3 (−0.0001), 4 (−0.0050), 6 (−0.0007) and 8 (−0.0010). Row 5 (+0.0004) is *positive* and still gets dropped, because it is below the keep line.

**So the honest count is: seven changes, four regressions, five drops (the four regressions plus row 5), two keeps.** An earlier wording of the chapter called the dropped rows "regressions" — and the distinction is worth having in your own words: **a regression made it worse; a drop merely failed to earn its place.** Both belong on the table.

**M2.**

| World | change A did | change B did | total |
|---|---|---|---|
| 1 | +0.004 | **0.000** | +0.004 |
| 2 | **0.000** | +0.004 | +0.004 |
| 3 | +0.010 | **−0.006** | +0.004 |
| 4 | **−0.006** | +0.010 | +0.004 |

**M2(a).** **World 3** (and world 4, which is the same story with the letters swapped). Change B costs you 0.006 and you have just shipped it, because A was carrying it.

**M2(b).** One number is one equation and you have two unknowns. Four different pairs of contributions produce the identical total, so the measurement cannot choose between them — **the information was never collected.**

**M3(a).** `0.7586 + 0.0003 + 0.0013 = **0.7602**`.

**M3(b).** `0.7604 − 0.7586 = **+0.0018**`.

**M3(c).** **Not exactly — the prediction is 0.0002 low.** But 0.0002 is far below the 0.005 line (and partly rounding: the unrounded deltas are 0.00034 and 0.00131), so this example does not prove the deltas fail to add. It shows you cannot *assume* they add: when features overlap in what they explain, their effects can **interact**, which is the honest reason "one change at a time" is a *discipline* rather than a *proof*. It gives you attributable rows; it does not give you a formula for combining them.

**M4.**

| delta *d* | *d* − mean | (*d* − mean)² |
|---|---|---|
| −0.0001 | +0.00078 | 0.00000061 |
| −0.0051 | −0.00422 | 0.00001778 |
| +0.0003 | +0.00118 | 0.00000140 |
| −0.0007 | +0.00018 | 0.00000003 |
| +0.0013 | +0.00218 | 0.00000477 |
| −0.0010 | −0.00012 | 0.00000001 |

**sum of the six deltas** = `−0.0001 − 0.0051 + 0.0003 − 0.0007 + 0.0013 − 0.0010 = **−0.0053**`

**mean** = `−0.0053 ÷ 6 = **−0.00088**` (to five places, −0.000883)

**sum of the squares** = **0.00002461**  **÷ 6** = **0.00000410**

**standard deviation** = `√0.00000410 = **0.00203**` (Python gives 0.002025)

**M4(a).** `(0.1705 − (−0.00088)) ÷ 0.00203 = 0.17138 ÷ 0.00203 = **84.4**` standard deviations. (Python, keeping every decimal place instead of the rounded ones: **84.63**.)

**M4(b).** *"An honest change on this table moves the score by about **0.002**, so a jump of 0.1705 is about **84** times bigger than anything honest, and that is why I stopped and audited it."* Any answer in the same neighbourhood is right; the point is that **the leak is not slightly unusual, it is off the end of the ruler.**

### Workbook answers — Predict the Output

**P1.**

```text
(2000, 8)
(2000, 7)
True
```

**Why not 2,020?** Because of `.drop_duplicates()`. `make_data.py` deliberately duplicates 20 rows — 1% of 2,000 — and a duplicated row that lands in two different piles is a row the model has already seen. Dropping them takes 2,020 back to **2,000**.

And **8 columns, not 10**, because `order_id` and `late` were both dropped: `order_id` is a row number, not a fact about the world, and `late` is the answer.

**Line 3 is `True` and it is the whole point of the snippet:** `.drop` hands you a **copy**. `X` is untouched, which is exactly what lets you drop a column, measure, and still have the full table ready for the next experiment.

**P2.**

```text
0.7585
0.7587
0.00039999999999995595
0.0004
```

**Two surprises, both worth having.**

**One: `0.75855` printed `0.7585` and `0.75865` printed `0.7587`.** Both end in 5, and they went opposite ways. The reason is that neither number exists exactly in binary — `0.75855` is stored as very slightly *less* than 0.75855, so it rounds down, and `0.75865` is stored as slightly *more*, so it rounds up. **You cannot predict which way a `...5` will go, so never let a decision hang on the fourth decimal place.**

**Two: `0.7590 - 0.7586` is not `0.0004`.** It is `0.00039999999999995595`. Same cause: neither number is exact, so their difference carries the error. `round(..., 4)` tidies it to `0.0004` for printing.

**What it means for a table whose gain is 0.0058:** the arithmetic is fine to about twelve decimal places, which is eight more than you are using — so it does not threaten your table. **But it does mean you round for display and never compare two numbers by `==`.**

**P3.**

```text
KeyError: "['order_hour'] not found in axis"
```

**`.drop` means rows unless you say otherwise.** With no `columns=`, pandas went looking for a **row** whose index label was `"order_hour"` and there is no such row. Note the message says *"not found in axis"* — that is pandas telling you it searched the wrong axis, which is the clue.

The fix is `X.drop(columns=["order_hour"])` — `columns=` **and** square brackets, even for a single name.

**P4.**

```text
[0, 1, 1, 1, 0]
3
[1, 0, 1]
```

**`between(18, 20)` includes both ends.** 18, 19 **and 20** are all `True`, so there are **three** rush hours, not two. That is `is_rush` in one line, and if you thought the 20 was excluded, you had just invented a different feature.

`.isin(["Sat", "Sun"])` is the same idea for words: `Sat` → 1, `Mon` → 0, `Sun` → 1. That is `is_weekend`.

**Both lines end in `.astype(int)`** because a column of `True`/`False` is not something you can scale and multiply by a weight — but `1` and `0` are.

### Workbook answers — Practice Set A

**A1.** feature set → **(iii)** · ablation table → **(i)** · regression → **(v)** · leak hunt → **(ii)** · target leakage → **(iv)**

**A2.**

| # | Verdict | If more than one, the rows it should be |
|---|---|---|
| 1 | **One change.** | — |
| 2 | **Two changes.** | Row A: + `is_rush`. Row B: + `is_weekend`, on top of A. |
| 3 | **One change.** | — |
| 4 | **Two changes.** | Row A: + `min_per_km`. Row B: − `prep_minutes`, on top of A. The reasoning is good; it is still two rows. |
| 5 | **Two changes — and one of them is illegal today.** | Row A: + `dist_x_weather`. The `max_iter` change touches the **model**, which is frozen this week. Revert it. |
| 6 | **Zero changes — and not comparable anyway.** | Nothing to record. |

**A2(a).** **Number 5.** `max_iter` is a setting on `LogisticRegression`, and this week's whole discipline is *the model is frozen, only the features move.* If you change the model, every earlier row in your table is now about a machine that no longer exists.

**A2(b).** **Number 6.** A different laptop is not a feature change. If the score differs, the cause is a different `random_state`, a different `make_data.py`, or a different library version — all of which are **bugs to investigate**, not experiments to record.

**A3.**

| # | What happens | The fix |
|---|---|---|
| a | `ValueError: Invalid parameter 'scaler' for estimator ColumnTransformer(...)`, ending in a list of valid names. The address is missing a level: `prep` holds *transformers*, and the scaler lives inside the one called `num`. | `pipe.set_params(prep__num__scaler=MinMaxScaler())` |
| b | `KeyError: "['day_of_week'] not found in axis"`. Without `columns=`, `.drop` looks for a **row**. | `X.drop(columns=["day_of_week"])` |
| c | **No error. A plausible, wrong number: 0.7541 — identical to the baseline.** `is_rush` was built and never shown to the model, because it is not in the number list. | `measure(CHAMP, CAT, RUSH)` — both lists must agree |
| d | `ValueError: A given column is not a column of the dataframe`. `CHAMP` **lists** `is_rush` and `{}` tells `add_features` to build **nothing**. | `measure(CHAMP, CAT, RUSH)` |
| e | `KeyError: 'order_hour'`, raised **inside `add_features`** in your own file: you threw away the ingredient and then asked for the cake. | Take the name out of the **number list**, not out of the table: `measure([c for c in CHAMP if c != "order_hour"], CAT, RUSH)` |
| f | **No error and nothing appears.** `to_string` *makes* text; only `print` *shows* it. | `print(table.round(4).to_string(index=False))` |
| g | **No error, and a slow disaster.** You have overwritten `X`, so the column is gone for every later experiment and every later row of your table is secretly about a smaller table. | `X_lean = X.drop(columns=["order_hour"])` — never assign back over the original |

**A3(h).** **c, f and g** produce no error at all — three of the seven, which is the real lesson of the page. The clues: **c** prints a score *identical to the baseline to four decimal places*, which is a coincidence too large to believe; **f** prints *nothing*, and a program that prints nothing has not succeeded; **g** shows up as a later row failing with `KeyError` on a column you know is in the file, or — worse — as every later score quietly shifting.

**A4.** i → **T** · ii → **S** · iii → **Q** · iv → **P** · v → **R**

`%+.4f` on `0.7536 - 0.7586` gives `-0.0050`: the `+` in the format means *always show the sign*, and the sign here is a minus.

**A5.**

**Log A — the built-but-not-listed bug.** `is_rush` was created by the derive step and never put in the `num` list, so the model never saw it. **The giveaway is the identical score:** 0.7541 twice, to four decimal places. A new column is worth *exactly* nothing only if it never arrived.

**Log B — the listed-but-not-built bug.** The same mistake from the other direction: the column is named in `num` and `add_features` was told to build nothing. **The giveaway is that the baseline printed first** — so the file is fine and it is the *second* call that is wrong.

**Log C — target leakage.** A single column moved the score by 0.1705 when every honest change all afternoon moved it by less than 0.005. **The giveaway is the size of the jump**, and audit 4 confirms it with no arithmetic: the value does not exist when the order is placed.

**Log D — measured on the wrong pile.** These are training scores, not validation scores. **The giveaway is the level, 0.786** — far above the 0.74 to 0.77 band where honest scores live on this table — **and the sign**, because on validation this change is a small loss, not a small gain.

**A5(a).** Easiest → hardest: **B, C, D, A.**

**B** is easiest: it crashes, and the message names the problem. **C** is next: nothing crashes, but the number is so far outside the honest band that it announces itself — *if* you know what the honest band is. **D** is harder: the numbers look like plausible AUCs and only the level gives it away. **A** is hardest of all, because the number is not merely plausible, it is *the number you already believed*.

What would have caught them: B — reading the last line. C — knowing the honest range, plus audit 0. D — printing which pile every score came from, on every line. A — printing both lists side by side before trusting the row.

**A6.** The deltas and verdicts are exactly M1's table: **+0.0045 keep · −0.0001 drop · −0.0050 drop · +0.0004 drop · −0.0007 drop · +0.0013 keep · −0.0010 drop** (`bench.py` prints −0.0051 and +0.0003 on rows 4 and 5, because it subtracts before rounding — see the note under M1).

**A6(a).** *"Rows 3 to 8 are each one change from row 2, so every delta on those rows is measured against **0.7586**. Only row 2 is measured against row 1's 0.7541."*

**A6(b).** **Rows 2 and 7.** Between them: `+0.0045 + 0.0013 = +0.0058` — which is exactly the total honest gain, `0.7599 − 0.7541`. **The two keeps account for the whole afternoon.**

### Workbook answers — Practice Set B

**B1.**

```python
X_lean = X_train.drop(columns=["order_hour"])

print("full %s   lean %s   original still has order_hour: %s"
      % (X_train.shape, X_lean.shape, "order_hour" in X_train.columns))
```

```text
full (1200, 8)   lean (1200, 7)   original still has order_hour: True
```

**B2.**

```python
rows = [("3  + is_weekend", 0.7585), ("4  + min_per_km", 0.7536),
        ("5  + items_per_km", 0.7590), ("6  scaler -> MinMaxScaler", 0.7579),
        ("7  drop order_hour", 0.7599), ("8  drop day_of_week", 0.7576)]


def show_deltas(rows, reference):
    print("reference: %.4f" % reference)
    for label, auc in rows:
        delta = auc - reference
        verdict = "keep" if delta > 0.0010 else "drop"
        print("%-26s %.4f  %+.4f  %s" % (label, auc, delta, verdict))


show_deltas(rows, 0.7586)
```

```text
reference: 0.7586
3  + is_weekend            0.7585  -0.0001  drop
4  + min_per_km            0.7536  -0.0050  drop
5  + items_per_km          0.7590  +0.0004  drop
6  scaler -> MinMaxScaler  0.7579  -0.0007  drop
7  drop order_hour         0.7599  +0.0013  keep
8  drop day_of_week        0.7576  -0.0010  drop
```

**The two rows that differ from `bench.py` are 4 and 5** — `−0.0050` here against `−0.0051` there, and `+0.0004` here against `+0.0003` there. **Cause: you handed the function numbers that had already been rounded to four places.** `bench.py` subtracts `0.75356217 − 0.75862700` and only rounds at the end. Both are correct arithmetic on the numbers they were given; only one of them is *the delta*. **Round at the end, never in the middle.**

**B3.**

```python
auc = measure(CHAMP + ["dist_x_weather"], CAT, {**RUSH, "inter": True})
```

Full program and its real output:

```python
from bench import CAT, CHAMP, RUSH, measure

champ = measure(CHAMP, CAT, RUSH)
auc = measure(CHAMP + ["dist_x_weather"], CAT, {**RUSH, "inter": True})
print("reference (+ is_rush)   : %.4f" % champ)
print("9  + dist_x_weather     : %.4f" % auc)
print("delta                   : %+.4f" % (auc - champ))
print("verdict                 : %s" % ("keep" if auc - champ > 0.0010 else "drop"))
```

```text
reference (+ is_rush)   : 0.7586
9  + dist_x_weather     : 0.7568
delta                   : -0.0018
verdict                 : drop
```

**Note the two lists agreeing.** `dist_x_weather` is in the number list **and** `inter=True` is in the settings. Leave either one out and you get the pair of bugs from A3 (c) and (d).

**And note the result: an "obviously clever" interaction feature lost 0.0018.** Distance times weather severity *sounds* like exactly the sort of thing that should help. It is a regression, it goes on the table as a regression, and the table is better for having it.

**B4.**

```python
print("--- audit 0: the two scores ---")
leaky_pipe, leaky_auc = fit_and_score(NUM + [SUSPECT])
_, honest_auc = fit_and_score(NUM)
print("with %s : val AUC %.4f" % (SUSPECT, leaky_auc))
print("without it                      : val AUC %.4f" % honest_auc)
print("jump                            : %+.4f" % (leaky_auc - honest_auc))
```

```text
--- audit 0: the two scores ---
with similar_orders_late_rate : val AUC 0.9240
without it                      : val AUC 0.7535
jump                            : +0.1705
```

**Two model fits and three prints, and it is the most valuable two seconds in the week.** Audit 0 does not tell you *what* is wrong — it tells you *whether to worry*, which is the only question you have at the start.

**B5.** `my_bench.py`:

```python
"""my_bench.py - two rows of my own, on top of the Week 7 champion."""
import pandas as pd

from bench import CAT, CHAMP, RUSH, measure

champ = measure(CHAMP, CAT, RUSH)
rows = [["2  + is_rush (reference)", champ, 0.0, "keep"]]

for label, num, cat, kw, drop in [
    ("9  + dist_x_weather", CHAMP + ["dist_x_weather"], CAT, {**RUSH, "inter": True}, ()),
    ("10 drop restaurant", CHAMP, [c for c in CAT if c != "restaurant"], RUSH, ("restaurant",)),
    ("11 drop weather", CHAMP, [c for c in CAT if c != "weather"], RUSH, ("weather",)),
]:
    auc = measure(num, cat, kw, drop)
    delta = auc - champ
    rows.append([label, auc, delta, "keep" if delta > 0.0010 else "drop"])

table = pd.DataFrame(rows, columns=["what I changed", "val_auc", "delta", "verdict"])
print()
print(table.round(4).to_string(index=False))
print()
print("reference : 0.7586 on the 400 validation rows")
print("best      : %.4f on the 400 validation rows" % table["val_auc"].max())
```

**Real output — and read the first thing that happens:**

```text
          what I changed  val_auc   delta verdict
2  + is_rush (reference)   0.7586  0.0000    keep
     9  + dist_x_weather   0.7568 -0.0018    drop
      10 drop restaurant   0.7465 -0.0121    drop
         11 drop weather   0.7310 -0.0276    drop

reference : 0.7586 on the 400 validation rows
best      : 0.7586 on the 400 validation rows
```

> **⚠️ Watch out:** `from bench import ...` **runs the whole of `bench.py`**, so before your own table appears you will see Week 7's eight-row table print itself again. Nothing is broken — importing a script executes it. It is also why `bench.py` is worth keeping short.

**And now read rows 10 and 11, because they are the most useful thing on this page.** Dropping `restaurant` costs **0.0121**; dropping `weather` costs **0.0276**. Those are the two biggest numbers in this little table, and they are *negative* — which means those two columns are **carrying the model**. You now have a number to write next to `weather` on your defence page instead of "untested", and it is twenty times the size of anything you invented.


### Workbook answers — Fix the Broken Program

**Bug 1 — line `row1 = measure(NUM, {})`. A wrong-columns bug.** `NUM` lists `is_rush`, and `{}` tells `add_features` to build nothing, so `ColumnTransformer` went looking for a column that was never made. It is looking for **`is_rush`**.

**The fix:** `row1 = measure(NUM, {"rush": True})` — the list and the settings must agree.

**Bug 2 — the `set_params` line. A runtime bug.** `prep__scaler` is an address with a level missing. Read the last sentence of the error: the valid parameters of a `ColumnTransformer` include **`transformers`**, which is the hint — the scaler is not a part of `prep` itself, it is inside the transformer called `num`.

**The fix:** `pipe.set_params(prep__num__scaler=MinMaxScaler())`.

**Bug 3 — the last line of `measure`. A silent logic bug.** It scores on `y_train` and `X_train`: **the model is being marked on the rows it revised from.**

Why that is always wrong: the model has already seen every one of those 1,200 rows and adjusted its weights to fit them. A score on training rows measures **memory**, not skill, and it always looks better — 0.7861 against the honest 0.7586. Worse, it moves in unpredictable directions when you add features, because a more complicated model can memorise more.

**The fix:**

```python
    return roc_auc_score(y_val, pipe.predict_proba(X_val)[:, 1])
```

**What happened to the sign:** the broken version says `MinMaxScaler` **gained** 0.0002; the truth is that it **lost** 0.0007. On the broken table you would have written **keep** in the verdict column (well, not quite — +0.0002 is below the +0.0010 line, so you would have written *drop* for the wrong reason, which is worse: a right answer with a broken instrument). Either way **the sign of the delta flipped, and the sign is the entire content of the row.**

**Ranking, easiest → hardest: 2, 1, 3.**

**Bug 2** is easiest — it crashes and the message prints the list of names it would have accepted. **Bug 1** also crashes, but the message does not say *which* column, so you have to compare two lists yourself. **Bug 3** is by far the hardest: it produces four plausible decimal numbers and a plausible delta, and nothing on the screen says which pile they came from. What would have caught it: **printing the pile beside every score.** `"val AUC 0.7586"` and `"train AUC 0.7861"` are impossible to confuse; `0.7861` on its own is not.

### Workbook answers — Puzzle of the Week

**Part 1(a).** `+40 − 20 + 100 = **+120**`.

**Part 1(b).** Every letter appears exactly twice in that sum — A in experiments 1 and 3, B in 1 and 2, C in 2 and 3 — so the total is `2 × (A + B + C)`. Therefore `A + B + C = 120 ÷ 2 = **+60**`, that is **+0.0060**.

**Part 1(c).**

```text
C = (A + B + C) − (A + B) = 60 − 40   = +20   -> +0.0020
A = (A + B + C) − (B + C) = 60 − (−20) = +80  -> +0.0080
B = (A + B + C) − (A + C) = 60 − 100  = −40   -> −0.0040
```

**Part 1(d).** `A + B = 80 − 40 = +40` ✅ · `B + C = −40 + 20 = −20` ✅ · `A + C = 80 + 20 = +100` ✅

**Part 1(e).** **B is the regression, at −0.0040.** And the notebook's owner shipped it — twice. Experiment 1 looked like a success (+40) and experiment 2 looked like a modest failure (−20), and in both of them **B was quietly costing 40 while A or C paid for it.** That is world 3 from M2, happening to a real person.

**Part 1(f).** **Three** experiments, one per change — the same number they ran. **The same amount of work — but under the stated assumption they had to solve three equations to untangle it, and every number in the notebook was muddled until they did.** One-change rows hand you A, B and C directly, with no assumption about how changes combine. That is the argument for the discipline, and notice that it cost them nothing in effort to get it wrong.

**Part 2.**

| # | strike out? | why |
|---|---|---|
| 1 | no | the baseline: zero changes, and it is the anchor for row 2 |
| 2 | no | one change |
| 3 | **STRIKE** | **two changes in one row.** +0.0002 could be `+0.0004` and `−0.0002`, or anything else |
| 4 | no | one change, and a regression — perfectly legal |
| 5 | **STRIKE** | changes the **model**, which is frozen. Not a feature experiment at all |
| 6 | no | one change |
| 7 | **STRIKE** | different machine. Not comparable, and it belongs in the Bug Log |

**Part 2(a).** **Four** usable rows: 1, 2, 4 and 6.

**Part 2(b).** `row 3a: + is_weekend` and `row 3b: + items_per_km (on top of 3a)`. Both must be measured with the same `measure` function, from the same reference, and the second one has to say what it is sitting on top of.

### Workbook answers — Think Deeper

**T1.** A good answer contains four things.

**One — what 0.0058 is actually worth.** On 400 validation rows, an AUC of 0.7599 against 0.7541 is a small, real, *defensible* improvement, and — this is the part that matters — **you can explain every ten-thousandth of it.** One row bought +0.0045 and one bought +0.0013, and both have a reason: a 0/1 flag can express a hump that a straight line cannot, and once you have the good version of a column the raw version costs you.

**Two — what you learned that the model did not.** Lateness humps over the dinner rush. Day of week barely matters. Distance, weather and restaurant are carrying most of the signal (dropping them costs 0.1038, 0.0276 and 0.0121). **That knowledge outlives this model**, and it will still be true when somebody replaces the logistic regression with something else next year.

**Three — the honest defence of the afternoon.** Yes, worth it — not because of the 0.0058 but because of the *table*. The table is what makes the next 0.0058 findable, and it is what would have caught the 0.9240.

**Four — the harder half.** Yes, there is a gain too small to report *as a gain*: on 400 rows, anything under about 0.005 has no evidence behind it. But **"no evidence" is itself worth reporting**, as a row with a number and the word "drop". A table that only records successes is a table that has thrown away most of what it learned. The dishonest move is not reporting a small number — it is reporting it *without* saying how big the wobble might be.

**T2.** A good answer says: **no, keeping row 7 is not dishonest — reporting it as certain would be.**

Row 7 gained +0.0013, which is inside the noise band you have declared, so the correct entry is something like: *"drop `order_hour`: +0.0013 on the 400 validation rows. Kept, because it also removes a column and simpler is better when the evidence is a tie. This is inside my noise band and I have not proven it."* **That sentence is worth more than the decision either way**, because it tells future-you exactly what past-you believed and how much they believed it.

What would settle it: **measure the wobble.** Score the same change on many different splits of the same data and look at the spread of the answers — if reshuffling flips the sign, there is nothing there. That is **cross-validation**, and it is Week 11. Until then the honest move is a written rule at the top of the table (*"under 0.005 = no evidence, on 400 rows"*) and a note in the "why" column on any row that leans on it.

**A full-marks extra:** notice that row 7 has a *second* reason to be kept that has nothing to do with the score — it makes the feature set **smaller**. One fewer column to explain, maintain and break. When two options tie on evidence, prefer the one with less machinery.


### Workbook answers — Draw It

A good drawing has **five** things on it, and they are on the panel in the figure: the 2,000-row table with the `late` column marked; an arrow into a box labelled with one group (`CrustyBros, Fri, clear, 16`); that box holding **exactly one order**, whose `late` is 1; the rate written out as `1 ÷ 1 = 1.0` and annotated *"its own answer"*; and the arrow coming back out into the feature column under its innocent name.

**How many boxes between `late` and the feature?** **Two** — the group, and the lookup table. And that is precisely why it is hard to spot: nobody looks two boxes upstream of a column called `similar_orders_late_rate`.

**Where is the `1.0`?** Inside the group of one, and it is "the late rate of similar orders" for a group whose only member is **this order**. So it is not a rate at all. **It is a label with a statistic's name on it.**

**The one arrow to point at:** the one going **from the `late` column into the lookup**. Everything downstream of that arrow is contaminated, and everything upstream is fine.

### Workbook answers — Self-Check

There are no right answers to a self-check, but two of those ten lines are the ones to be honest about. **"State my best score with the pile named"** — if that is not a 😀 by now, put a sticky note on your screen, because it is a mark in every week for the rest of the year. And **"defend every column I kept with a number"** — if that is a 😕, the cure is not more reading, it is running six more rows of `my_bench.py` and filling in the "why" column.


---

### Practice Set A, A2 — One change or more? (lesson handout, formerly "Page 7.1"): teacher notes

*For each experiment, say whether it is one change or more than one. If it is more, rewrite it as separate rows.*

| # | The experiment as described | Verdict | If more than one, the rows it should be |
|---|---|---|---|
| 1 | "I added `is_rush`." | **One change.** | — |
| 2 | "I added `is_rush` and `is_weekend`." | **Two changes.** | Row A: + `is_rush`. Row B: + `is_weekend` (on top of A). |
| 3 | "I swapped StandardScaler for MinMaxScaler." | **One change.** | — |
| 4 | "I added `min_per_km` and dropped `prep_minutes`, since the ratio contains it." | **Two changes.** | Row A: + `min_per_km`. Row B: − `prep_minutes` (on top of A). The reasoning is good; it is still two rows. |
| 5 | "I added `dist_x_weather` and changed `max_iter` from 2000 to 5000." | **Two changes — and one of them is illegal today.** | Row A: + `dist_x_weather`. The `max_iter` change touches the **model**, which is frozen. Revert it and note it for another session. |
| 6 | "I re-ran yesterday's experiment on my friend's laptop." | **Zero changes — and it is not comparable anyway.** | Nothing to record. If the score differs, the cause is a different `random_state` or a different `make_data.py`, not a feature. **This row belongs in the Bug Log, not the ablation table.** |

**The sentence to look for on this page:** any version of *"if two things move, the number can't tell you which one did it."*

### Build It — Predict the sign (formerly "Page 7.2")

*For each proposed change, predict whether the delta will be positive or negative. Then fill in the truth.*

| Proposed change | A common prediction | The truth | Δ |
|---|---|---|---|
| `+ is_weekend` | positive — "weekends are busier" | **0.7585** | **−0.0001** |
| `+ min_per_km` | positive — "a ratio is cleverer than two columns" | **0.7536** | **−0.0051** |
| `scaler → MinMaxScaler` | no change — "it's the same information" | **0.7579** | **−0.0007** |
| `drop order_hour` | negative — "you're throwing away real data" | **0.7599** | **+0.0013** |

**Mark for honesty, not accuracy.** Two wrong predictions out of four is the expected result and should be praised. The learning is in the *surprise*, and a student who predicted all four correctly probably wrote them after running.

**The two worth discussing:** `min_per_km` feels clever and loses 0.0051. `drop order_hour` feels destructive and gains 0.0013. Both intuitions were backwards, and that is exactly why we measure.

### Build It — The class wall table, copied (formerly "Page 7.3"; the same table as M1)

*A copy of the class table, in the student's handwriting. Marked for completeness, not for matching.*

| what I changed | val AUC | Δ | keep or drop |
|---|---|---|---|
| 1 baseline (Week 3 pipeline) | 0.7541 | — | keep |
| 2 + `is_rush` | 0.7586 | +0.0045 | keep |
| 3 + `is_weekend` | 0.7585 | −0.0001 | drop |
| 4 + `min_per_km` | 0.7536 | −0.0051 | drop |
| 5 + `items_per_km` | 0.7590 | +0.0003 | drop |
| 6 scaler → MinMaxScaler | 0.7579 | −0.0007 | drop |
| 7 drop `order_hour` | 0.7599 | +0.0013 | keep |
| 8 drop `day_of_week` | 0.7576 | −0.0010 | drop |

**Rows 3–8 are each one change from row 2**, so every delta on those rows is measured against 0.7586. Row 2's delta is measured against row 1. **A student who writes that note on their page unprompted is at level 4.**

### Build It — Finish the ablation table (formerly "Page 7.4")

**The complete runnable file. Run with `python3 bench.py`. Runtime: under 2 seconds.**

```python
"""bench.py - one change, one measurement, one row.  Week 7."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, MinMaxScaler,
                                   OneHotEncoder, StandardScaler)

from make_data import make_deliveries

BASE_NUM = ["distance_km", "items", "prep_minutes", "order_hour",
            "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)
print("train %d   val %d   test %d" % (len(X_train), len(X_val), len(X_test)))


def add_features(d, rush=False, weekend=False, ratio=False, items_ratio=False,
                 inter=False):
    """Row-wise arithmetic only.  Nothing here looks across rows, so nothing can leak."""
    d = d.copy()
    if rush:
        d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    if weekend:
        d["is_weekend"] = d["day_of_week"].isin(["Sat", "Sun"]).astype(int)
    if ratio:
        d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    if items_ratio:
        d["items_per_km"] = d["items"] / (d["distance_km"] + 0.5)
    if inter:
        severity = d["weather"].map({"clear": 0.0, "rain": 1.0, "storm": 2.0})
        d["dist_x_weather"] = d["distance_km"] * severity
    return d


def measure(num, cat, kw, drop=(), minmax=False):
    """Fit on train, score on val.  Returns one number."""
    tr = X_train.drop(columns=list(drop))
    va = X_val.drop(columns=list(drop))
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scaler", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
    ])
    pipe = Pipeline([("derive", FunctionTransformer(add_features, kw_args=kw)),
                     ("prep", prep),
                     ("model", LogisticRegression(max_iter=2000, random_state=0))])
    if minmax:
        pipe.set_params(prep__num__scaler=MinMaxScaler())
    pipe.fit(tr, y_train)
    return roc_auc_score(y_val, pipe.predict_proba(va)[:, 1])


RUSH = {"rush": True}
CHAMP = BASE_NUM + ["is_rush"]

rows = []
base = measure(BASE_NUM, CAT, {})
rows.append(["1  baseline (Week 3 pipeline)", base, np.nan, "keep"])

champ = measure(CHAMP, CAT, RUSH)
rows.append(["2  + is_rush", champ, champ - base, "keep"])

for label, num, cat, kw, drop, mm in [
    ("3  + is_weekend",            CHAMP + ["is_weekend"],   CAT, {**RUSH, "weekend": True},      (), False),
    ("4  + min_per_km",            CHAMP + ["min_per_km"],   CAT, {**RUSH, "ratio": True},        (), False),
    ("5  + items_per_km",          CHAMP + ["items_per_km"], CAT, {**RUSH, "items_ratio": True},  (), False),
    ("6  scaler -> MinMaxScaler",  CHAMP,                    CAT, RUSH,                           (), True),
    ("7  drop order_hour",         [c for c in CHAMP if c != "order_hour"], CAT, RUSH,            (), False),
    ("8  drop day_of_week",        CHAMP, [c for c in CAT if c != "day_of_week"], RUSH, ("day_of_week",), False),
]:
    auc = measure(num, cat, kw, drop, mm)
    delta = auc - champ
    rows.append([label, auc, delta, "keep" if delta > 0.0010 else "drop"])

table = pd.DataFrame(rows, columns=["what I changed", "val_auc", "delta", "verdict"])
print()
print(table.round(4).to_string(index=False))
print()
print("best honest val AUC : %.4f" % table["val_auc"].max())
print("total honest gain   : %.4f" % (table["val_auc"].max() - base))
```

**Real output:**

```text
train 1200   val 400   test 400

               what I changed  val_auc   delta verdict
1  baseline (Week 3 pipeline)   0.7541     NaN    keep
                 2  + is_rush   0.7586  0.0045    keep
              3  + is_weekend   0.7585 -0.0001    drop
              4  + min_per_km   0.7536 -0.0051    drop
            5  + items_per_km   0.7590  0.0003    drop
    6  scaler -> MinMaxScaler   0.7579 -0.0007    drop
           7  drop order_hour   0.7599  0.0013    keep
          8  drop day_of_week   0.7576 -0.0010    drop

best honest val AUC : 0.7599
total honest gain   : 0.0058
```

**The six subtractions, shown, for the paper version:**

| row | val AUC | minus 0.7586 | Δ |
|---|---|---|---|
| 3 | 0.7585 | 0.7585 − 0.7586 | **−0.0001** |
| 4 | 0.7536 | 0.7536 − 0.7586 | **−0.0051** |
| 5 | 0.7590 | 0.7590 − 0.7586 | **+0.0003** |
| 6 | 0.7579 | 0.7579 − 0.7586 | **−0.0007** |
| 7 | 0.7599 | 0.7599 − 0.7586 | **+0.0013** |
| 8 | 0.7576 | 0.7576 − 0.7586 | **−0.0010** |

And row 2: 0.7586 − 0.7541 = **+0.0045**. Total honest gain: 0.7599 − 0.7541 = **+0.0058**.

**Rows of the student's own that the workbook also lists** (from `my_bench.py`; all against 0.7586, all **drop**, so a student's own rows should land near these): 9 `+ dist_x_weather` 0.7568, **−0.0018** · 10 drop `restaurant` 0.7465, **−0.0121** · 11 drop `weather` 0.7310, **−0.0276** · 12 drop `distance_km` 0.6548, **−0.1038** · 13 drop `items` 0.7561, **−0.0025** · 14 drop `prep_minutes` 0.7562, **−0.0024**. Rows 10 to 14 are the numbers to put beside those columns on the defence table instead of "untested".

**The required headline sentence:** *"My best validation AUC is 0.7599, on the 400 validation rows."* **A page without the pile named loses a mark, every week, all year.**

### Build It — The leak hunt (formerly "Page 7.5")

**The complete runnable file. Run with `python3 leak_hunt.py`. Runtime: under 2 seconds.**

```python
"""leak_hunt.py - four audits on a suspiciously good score."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, OneHotEncoder,
                                   StandardScaler)

from leaky_features import add_features
from make_data import make_deliveries

NUM = ["distance_km", "items", "prep_minutes", "driver_experience_months",
       "is_rush", "min_per_km"]
CAT = ["restaurant", "day_of_week", "weather"]
SUSPECT = "similar_orders_late_rate"

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)


def fit_and_score(num):
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scaler", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    pipe = Pipeline([("derive", FunctionTransformer(add_features)),
                     ("prep", prep),
                     ("model", LogisticRegression(max_iter=2000, random_state=0))])
    pipe.fit(X_train, y_train)
    auc = roc_auc_score(y_val, pipe.predict_proba(X_val)[:, 1])
    return pipe, auc

print("--- audit 0: the two scores ---")
leaky_pipe, leaky_auc = fit_and_score(NUM + [SUSPECT])
_, honest_auc = fit_and_score(NUM)
print("with %s : val AUC %.4f" % (SUSPECT, leaky_auc))
print("without it                      : val AUC %.4f" % honest_auc)
print("jump                            : %+.4f" % (leaky_auc - honest_auc))

print()
print("--- audit 1: correlation of every number column with late ---")
feat = add_features(df)
cols = ["distance_km", "items", "prep_minutes", "driver_experience_months",
        "is_rush", "min_per_km", SUSPECT]
corr = feat[cols + ["late"]].corr()["late"].drop("late")
print(corr.reindex(corr.abs().sort_values(ascending=False).index).round(3).to_string())

print()
print("--- audit 2: that one column, on its own ---")
_, alone = fit_and_score([SUSPECT])
print("model with ONLY %s : val AUC %.4f" % (SUSPECT, alone))

print()
print("--- audit 3: the biggest weights the model learned ---")
names = leaky_pipe.named_steps["prep"].get_feature_names_out()
co = pd.Series(leaky_pipe.named_steps["model"].coef_[0], index=names)
print(co.reindex(co.abs().sort_values(ascending=False).index).head(4).round(3).to_string())

print()
print("--- audit 4: the question no number can answer ---")
print("The lookup was built from the 'late' column of ALL 2000 rows.")
print("360 of the 820 groups hold exactly one order, so for those rows")
print("the 'rate' is 1.0 when that order was late and 0.0 when it was not.")
print("VERDICT: target leakage. The feature is the answer, dressed as a statistic.")
```

**Real output:**

```text
--- audit 0: the two scores ---
with similar_orders_late_rate : val AUC 0.9240
without it                      : val AUC 0.7535
jump                            : +0.1705

--- audit 1: correlation of every number column with late ---
similar_orders_late_rate    0.676
distance_km                 0.345
min_per_km                 -0.186
is_rush                     0.133
driver_experience_months   -0.123
items                       0.106
prep_minutes                0.066

--- audit 2: that one column, on its own ---
model with ONLY similar_orders_late_rate : val AUC 0.8916

--- audit 3: the biggest weights the model learned ---
num__similar_orders_late_rate    2.071
num__distance_km                 0.971
num__driver_experience_months   -0.411
cat__day_of_week_Sat            -0.269

--- audit 4: the question no number can answer ---
The lookup was built from the 'late' column of ALL 2000 rows.
360 of the 820 groups hold exactly one order, so for those rows
the 'rate' is 1.0 when that order was late and 0.0 when it was not.
VERDICT: target leakage. The feature is the answer, dressed as a statistic.
```

**The four answers the page asks for:**

1. **Which feature is poisoned?** `similar_orders_late_rate`. The other two — `is_rush` and `min_per_km` — are row-wise arithmetic on columns that exist when the order is placed. They are fine. (`min_per_km` happens to be a *bad* feature — it cost 0.0051 in row 4 — but bad is not the same as poisoned.)

2. **Which flavour of leak?** **Target leakage.** The column was computed from the `late` column, which is the answer. It is *also* computed over all 2,000 rows rather than just the training rows, which is preprocessing leakage — so a student who says "both, and target leakage is the fatal half" is more right than the answer key and should be told so.

3. **The fake score:** **0.9240** validation AUC. **The honest score:** **0.7535** validation AUC, the same feature set with the poisoned column removed. **The jump: +0.1705.**

4. **Does the value exist at the moment the order is placed?** **No.** The lookup is built out of which past orders were late, and it hands each row *its own group's* rate. For the 360 groups containing exactly one order, that rate is that order's own answer. At the moment the customer taps "order", nobody knows whether it will be late, so nobody could compute this column. In production it would be empty.

**The four independent alarms, each louder than the last, for marking the reasoning:**

1. One column moved the score by **0.1705**. Every honest change we made all lesson moved it by less than 0.005. That is a factor of thirty-four.
2. Its correlation with `late` is **0.676**, while the best honest feature manages **0.345**.
3. **That column alone scores 0.8916** — better than every honest feature put together (0.7535).
4. Its weight is **2.071**, more than twice the next one (0.971).

**And the bonus number, for anyone who says "so compute it properly and keep it":** rebuild the identical lookup from the 1,200 training rows only, and validation AUC is **0.6115** — *worse than the 0.7535 you get without the feature at all.* The complete file:

```python
"""leak_fix.py - the same idea, computed from the training rows only."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, OneHotEncoder,
                                   StandardScaler)

from make_data import make_deliveries

KEY = ["restaurant", "day_of_week", "weather", "order_hour"]
NUM = ["distance_km", "items", "prep_minutes", "driver_experience_months",
       "is_rush", "min_per_km"]
CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_test, y_tmp, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(
    X_tmp, y_tmp, test_size=0.25, random_state=0, stratify=y_tmp)

# the lookup, built from the 1200 TRAINING rows and nothing else
train_tbl = X_train.copy()
train_tbl["late"] = y_train
LOOKUP = train_tbl.groupby(KEY)["late"].mean().to_dict()
PRIOR = float(y_train.mean())
print("groups seen in training:", len(LOOKUP), " fallback rate: %.4f" % PRIOR)


def add_features(d):
    d = d.copy()
    d["is_rush"] = d["order_hour"].between(18, 20).astype(int)
    d["min_per_km"] = d["prep_minutes"] / (d["distance_km"] + 0.5)
    rates = []
    for row in d[KEY].itertuples(index=False, name=None):
        rates.append(LOOKUP.get(row, PRIOR))
    d["similar_orders_late_rate"] = rates
    return d


def fit_and_score(num):
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scaler", StandardScaler())]), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    pipe = Pipeline([("derive", FunctionTransformer(add_features)),
                     ("prep", prep),
                     ("model", LogisticRegression(max_iter=2000, random_state=0))])
    pipe.fit(X_train, y_train)
    return roc_auc_score(y_val, pipe.predict_proba(X_val)[:, 1])


print("train-only lookup, with the feature : val AUC %.4f" % fit_and_score(NUM + ["similar_orders_late_rate"]))
print("train-only lookup, without it      : val AUC %.4f" % fit_and_score(NUM))
```

```text
groups seen in training: 647  fallback rate: 0.2875
train-only lookup, with the feature : val AUC 0.6115
train-only lookup, without it      : val AUC 0.7535
```

**Why 0.6115 and not something respectable?** The rebuild is still naive: each training row is counted inside its own group (647 groups over 1,200 rows, so most hold one or two orders), so on training rows the column is partly the row's own label. Measured: train AUC 0.957, weight about 2.7, validation 0.6115, with 28.5% of validation orders in groups never seen in training. Out-of-fold and smoothed, the same idea scores about 0.758, barely above 0.7535. **The 0.9240 was never a measure of the feature.**

### Build It — Defend your final feature set (formerly "Page 7.6")

*Every kept column with the number that justifies it; every dropped column with the number that condemns it.*

**A full-marks answer.** The exact columns will vary; the **shape** must be this, with a number on every line.

**Kept — the final feature set (val AUC 0.7599 on the 400 validation rows):**

| Column | Where it came from | The number that justifies it |
|---|---|---|
| `distance_km` | the raw file | Highest honest correlation with `late`, **0.345**, the largest honest weight, **0.971**, and dropping it costs **0.1038** (row 12). |
| `items` | the raw file | In the baseline that scored 0.7541. Dropping it costs **0.0025** (row 13, if the student ran it). **If they did not run it, an honest answer says "untested" rather than inventing a reason.** |
| `prep_minutes` | the raw file | Dropping it costs **0.0024** (row 14). Untested individually if the student did not run it. |
| `driver_experience_months` | the raw file, with a median imputer | Correlation **−0.123**, and the third-largest weight, **−0.411**. |
| `is_rush` | invented, from `order_hour` | **Row 2: +0.0045.** The largest single gain of the day. |
| `restaurant` | the raw file, one-hot | Dropping it costs **0.0121** (row 10). |
| `weather` | the raw file, one-hot | Dropping it costs **0.0276** (row 11), the biggest honest number after `distance_km`. |

**Dropped, with the number:**

| Column | Why it went | The number |
|---|---|---|
| `order_hour` (raw) | `is_rush` already carries the useful part | **Row 7: +0.0013 when removed.** |
| `day_of_week` | one-hot, and it barely earns its three columns | **Row 8: −0.0010 when removed**, so it *is* worth a little — kept in the final set on that basis, and a student who keeps it and cites −0.0010 is **right**. |
| `is_weekend` | never made it in | **Row 3: −0.0001.** No signal. |
| `min_per_km` | a ratio that looked clever | **Row 4: −0.0051.** The worst change of the day. |
| `items_per_km` | possible, but not proven | **Row 5: +0.0003**, which is inside the noise on 400 rows. |
| `dist_x_weather` | an interaction that sounded clever | **Row 9: −0.0018.** |
| `similar_orders_late_rate` | **target leakage** | Fake **0.9240**, honest **0.7535**, naively rebuilt from training rows **0.6115**. |
| `order_id` | it is a row number, not a fact about the world | Never a candidate. Naming it anyway is a **level-4 answer**. |

**Marking notes.** Three specific things:

- **A line with no number is not a defence.** "Distance obviously matters" is true and worth zero marks. "Correlation 0.345, weight 0.971" is a defence.
- **"Untested" is an acceptable and honest entry** and is *better* than an invented number. Reward it.
- **The best answers disagree with this key.** Row 8 says removing `day_of_week` costs 0.0010 — inside the noise band. A student who keeps it *and* one who drops it can both be right, provided they cite the number and say which side of 0.005 they think it falls on.

### Answers to every question posed in the lesson

**Hook — "how do you feel about 0.9240?"** Suspicious. On this table honest scores sit between 0.74 and 0.77, and a single feature that moves the score by 0.17 has moved it thirty-four times more than any honest change all lesson. **A jump that big is a bug, not a discovery.**

**Hook — "what was the rule from last week?"** A suspiciously good score is not good news. Week 6 planted the same lesson with `customer_called_support`.

**Concept — "which of the four worlds am I in?"** You cannot tell. All four produce +0.004 and one of them is hiding a change that costs you 0.006.

**Concept — "`is_weekend` plus a scaler swap: one row or two?"** Two. If the score moves, nothing on a single row says which change moved it.

**Live-code step 1 — "what three numbers will print?"** 1200, 400, 400. From 2,000 rows after `drop_duplicates()`: 20% test is 400, then 25% of the remaining 1,600 is 400 validation, leaving 1,200 train.

**Live-code step 3 — "two identical scores: is that possible?"** No. Adding a column and getting the identical number to four decimal places means the change never reached the model: here, the column was built but never listed in `num`. **A plausible number is more dangerous than a crash.**

**Live-code step 3 — "why did the first call crash and the second not?"** The first call listed `is_rush` in `num` but never built it, so `ColumnTransformer` was asked for a column that does not exist and raised `ValueError: A given column is not a column of the dataframe`. The second built `is_rush` but never listed it, so nothing asked for it and nothing complained. **This is the most dangerous bug class of the term precisely because one direction shouts and the other stays silent.**

**Live-code step 3 — "why does a 0/1 flag beat a number containing more information?"** Because `LogisticRegression` fits a straight line in each input. With `order_hour` as a number it can only say "later is worse" or "later is better". The truth is a hump over 18:00–20:00. A 0/1 flag can express a hump; a straight line cannot. **The flag has less information and more of the right shape.**

**Live-code step 4 — "read me the last line, and which file?"** `KeyError: 'order_hour'`, raised inside `add_features` in the student's own `bench.py`. The column was removed from the table while a derived feature still needed it as an ingredient.

**Wrap / Check 1 — "two columns and a scaler, +0.006: what have I learnt?"** Nothing usable. See the four worlds.

**Wrap / Check 2 — "removed a real column, score went up: how?"** `is_rush` probably extracted the useful part of `order_hour`; the leftover raw hour may contribute a straight-line story that is not true. At +0.0013 that is a hypothesis under our own 0.005 line, not a finding. Once you have the good version of a column, the raw version can cost you.

**Wrap / Check 3 — "somebody's model scores 0.94: what do you do?"** Do not celebrate. Ask of every feature: *does this value exist at the moment I need the prediction?* Then run the four audits: score with and without, correlation with the target, that column alone, and the weight sizes.

**Variation-harder 1 — "does the A+B delta equal the sum of the two deltas?"** No. Take A = `+ items_per_km` (+0.0003) and B = `drop order_hour` (+0.0013). Run separately from the champion 0.7586 you get 0.7590 and 0.7599. Run together you get **0.7604**, a delta of +0.0018 against a sum of +0.0016. That 0.0002 gap is far under the 0.005 line (and partly rounding), so this example does not demonstrate anything; it shows you cannot *assume* the effects add. When features overlap in what they explain their effects can interact, which is the honest reason "one at a time" is a *discipline* rather than a *proof*.

**Variation-harder 4 — "can `add_features` cheat by using `y`?"** It is not *given* `y`: `FunctionTransformer` only hands your function the feature table. But nothing stops it reading a global such as `y_train` (we tried `d["cheat"] = y_train`: it runs, fits a model that leans on the label, and scores 0.7522 on validation because the mismatched index turns `cheat` into NaN there). So the design makes the leak harder to write by accident, not impossible — and that is exactly how `leaky_features.py` smuggles it in at import time, outside the function, from a fresh copy of the whole table. **A student who finds that it does not crash has understood something most working practitioners have not.**

**Variation-harder 5 — argue both sides of row 5.**
*For keeping `items_per_km`:* the delta is positive, it is a cheap row-wise calculation with no leakage risk, it is easy to explain ("how many items per kilometre the driver is carrying"), and 0.7590 is genuinely the second-best honest score on the table.
*Against:* +0.0003 is a fifteenth of the smallest gain we were prepared to call real, it is measured on 400 rows with no estimate of the wobble, and every column you keep is a weight fitted from the same 1,200 rows and one more thing to maintain and explain. **The against case is stronger**, and the deciding sentence is: *"if reshuffling the validation rows would flip the sign, it is not evidence."*

---

## 🔮 Next Week Preview

Next week the number changes. All term the student has reported one figure — AUC — and next week they meet the reason that is not enough: **accuracy can be 98.6% on a model that has never once said yes.** They will build that model on purpose, admire its score, and then split thirty predictions into four piles — caught, false alarm, miss, correctly left alone — and discover that those four counts say something accuracy cannot: *what kind of wrong you are.* There is no new maths, only four counts and two fractions, both computed on paper before any code runs.

**To prep early:** you need **forty index cards or forty slips of paper** for the activity, and four labels for the piles. Cut them the night before; cutting paper in class costs five minutes you will want. Nothing new to install. And if you have a printer, print the Week 8 confusion-matrix figure large and put it on the wall next to this week's ablation table — the two artifacts sit side by side for the rest of the term, and Week 9 uses both.
