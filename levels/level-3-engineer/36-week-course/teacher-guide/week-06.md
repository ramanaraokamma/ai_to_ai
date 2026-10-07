# Week 6 — The Answer Was in the Features

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Week 7 ➡](week-07.md) · [Student Guide](../student-guide/week-06.md) · [Workbook](../workbook/week-06.md)

---

## 📋 At a Glance

This table is the week on one page: what is taught, how long it takes, and what you need.

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the week good news becomes suspicious |
| **Big idea** | A suspiciously perfect score is almost never a great model — it is information leaking in that will not exist when you actually have to predict. |
| **New vocabulary** | imputation · missing indicator · data leakage · target leakage · temporal leakage · preprocessing leakage |
| **New maths** | **None new.** Today re-uses the median from Level 2 and the subtraction of two scores from Week 5. One median is worked out by hand on 1,140 numbers by counting to the middle. |
| **New syntax** | `SimpleImputer(strategy="median")` · `add_indicator=True` · `pipe.named_steps["prep"]` |
| **Dataset** | The Week 1 pizza-delivery table (`make_data.py`, seed 0) with one poisoned column joined onto it by a supplied file, `support_calls.py` · a 3,000-row drifting table generated inline with numpy (seed 0) · a 200×2,000 table of **pure noise** (seed 0). **Nothing downloads.** |
| **Materials** | The printed Week 6 workbook (`workbook/week-06.md`, printed **without** the Answers section at its end) · plain paper for the Crime Scene notes · printed copies of `mystery.py`'s output (one each) · **a whiteboard divided into three columns headed `target` / `temporal` / `preprocessing`** · a red pen · a timer that can do twelve minutes · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. **No new installs.** `make_data.py` from Week 1 must still be in the folder, unchanged. You must place `support_calls.py` and `noise_leak.py` in the folder before class — full text in the Prep Checklist. |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | Every script this week runs in **about one second**. `fill_blanks.py` 0.8 s · `leak_hunt.py` 0.9 s · `temporal.py` 0.8 s · `noise_leak.py` 0.8 s · `deploy.py` 0.9 s. If anything runs for a minute, something else is wrong. |

> **⚠️ Watch out:** this is the first week where **the student is asked to distrust a good number**, and that is genuinely hard. Four weeks of the course have trained them to want a bigger score. Today a bigger score is the crime scene. Do not soften it and do not rush the twelve silent minutes of the Crime Scene activity — the discovery has to be theirs or the lesson does not take.

> **📌 One honest note about the syntax ladder.** Two constructs appear this week that are **not** on the Week 6 ladder — `SelectKBest` and `cross_val_score`. They live inside `noise_leak.py`, which is a **supplied file the student reads, runs, and changes by one line.** Nothing this week asks them to write either one, and nothing in the homework depends on understanding them. `cross_val_score` gets taught properly in **Week 11**. If a student asks what it is, the one-line answer is in the Questions section and that is all they need today.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Impute missing values with a statistic learned from the training rows only**, and add an indicator column marking where the blank was.
2. **Name the three flavours of leakage** — target, temporal, preprocessing — and give the tell for each.
3. **Produce a 76.5% accuracy score on data that is literally random noise**, and explain in their own words how it happened.
4. **Fix all three leaks and report the honest number beside the fake one** for each.

Observable evidence: `fill_blanks.py` printing `29.5` as the number the imputer learned and `29.0` as the number it was *not* allowed to learn; a filled-in three-column table naming each flavour, its fake score and its honest score; and `noise_leak.py` printing `0.765` for the leaky route and `0.520` for the honest one.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is no new mathematics this week.** There are two new ideas, and the second one is the most important idea in the whole of Term 1. Read this section once — about twenty-five minutes — and you will be comfortably ahead.

### 1. The one-sentence version, and the story behind it

> **This week's one sentence:** "When a score goes up a lot, the first question is not *how did I do that* — it is *what did I accidentally tell it?*"

Here is the story, and it is worth telling in the Hook exactly as written.

A hospital builds a model to predict which patients will need intensive care. It scores brilliantly — much better than the doctors. Everybody is delighted. Then somebody looks at which column the model is leaning on hardest, and it is a column recording **which ward the patient was moved to**. Patients who were moved to the intensive-care ward needed intensive care. The model had not learnt medicine. It had learnt to read the answer off a form that is only filled in *after* the decision has already been made.

That failure has a name.

> **data leakage** — when a column contains information that would not be available at the moment you actually have to make the prediction.

**And here is the property that makes leakage so dangerous: it almost always makes your score go up.** (The honest version is in the Questions section: contrived cases exist. Tell students "almost always".) A bug that makes your score go *down* gets fixed on Tuesday afternoon, because somebody is annoyed. A bug that makes your score go *up* gets a celebration, a slide in a presentation, and six months in production being wrong.

So this week the rule changes. **Good news gets audited harder than bad news.**

![Three ways to be handed the answer](../figures/fig-w06-1-three-flavours-of-leakage.svg)
*Figure 6.1 — Three ways to be handed the answer. Three different bugs, three different tells, and all three push the number in the same flattering direction.*

### 2. First, the small job: filling in the 106 blanks

Before the leakage, there is a piece of unfinished business from Week 1. The `driver_experience_months` column has holes in it — **106 of them**, out of 2,000 rows. Nothing has been done about that for five weeks, because `SimpleImputer` was quietly doing it inside the pipeline. Today you look at what it actually did.

> **imputation** — filling a blank with a number worked out from the rows you are allowed to look at.

You have three options and only one of them is good.

| Option | What it does | Why not |
|---|---|---|
| Delete the rows with blanks | 2,000 rows becomes 1,894 | You threw away 106 rows of evidence to fix one column. And if blanks are commoner among new drivers, you have just deleted the new drivers. |
| Fill with **0** | "This driver has zero months of experience" | That is a **lie the model will believe.** Zero is not "unknown", it is "brand new", and it is the worst possible guess. |
| Fill with the **median** of the training rows | "Assume they are a typical driver until told otherwise" | ✅ This one. It is a guess, but it is the least wrong guess and it does not invent an extreme. |

**Why the median rather than the mean?** Because the median cannot be dragged by one silly value. The student proved this to themselves in Week 4 on the list `2, 4, 6, 8, 100`: the mean is 24, the median is 6, and 6 is the honest description of that list. Same reasoning here.

> **🔢 The maths, slowly:** the median is *the middle number when you line them all up*. In the 1,200 training rows, 60 are blank, so **1,140 have a value.** 1,140 is an even number, so there is no single middle one — the two middle ones are number **570** and number **571** in the sorted line. Number 570 is **29**. Number 571 is **30**. Halfway between them is **(29 + 30) ÷ 2 = 29.5**. That is where `29.5` comes from, and you can say every step of that out loud without a calculator.

Now the part that matters, and it is Week 2's rule wearing a new hat. **Which rows is the imputer allowed to look at when it works out that number?**

- Median of **all 2,000 rows** (1,894 with values): the two middle ones are both 29, so **29.0**.
- Median of **the 1,200 training rows** (1,140 with values): **29.5**.

They are different numbers. And if you use 29.0, then the number you wrote into the training data was **partly worked out from the 800 rows you were about to be marked on.** That is a leak. It is a very small leak, and this week you will measure exactly how small — but it is the same shape of mistake as the huge ones.

![Which rows the fill-in number is allowed to see](../figures/fig-w06-2-imputation-learned-from-train-only.svg)
*Figure 6.2 — Which rows the fill-in number is allowed to see. Same 106 blanks, same median, two different answers — 29.0 and 29.5 — depending only on when you cut.*

**And the bonus column.** Sometimes *being blank is itself a fact about the row.* If the paperwork is worse for brand-new drivers, then "this field is empty" is a clue, and filling in 29.5 destroys it. So you keep the clue:

> **missing indicator** — an extra 0/1 column that records "the original value here was blank", kept alongside the filled-in value.

`add_indicator=True` builds it for you. In our table it is a **hypothesis, not a gift** — and Week 5 taught the student exactly what to do with a hypothesis. Ablate it:

```text
add_indicator=False cols= 20  accuracy=0.7600  roc_auc=0.7752
add_indicator=True  cols= 21  accuracy=0.7550  roc_auc=0.7723
```

0.7723 − 0.7752 = **−0.0029**. The indicator made the model **worse**, so it goes. Say this out loud, because it is the Week 5 habit surviving contact with a new tool: *a new column earns its place or it leaves, and this one did not earn it.*

Why not? Because in our table the blanks were scattered at random — `make_data.py` chose them with a coin flip, and you can read the line that did it. There is no hidden story about rookie drivers to find. The 60 blank training rows do look less late (0.15 against 0.2947), but 60 rows is nine late deliveries; that gap is noise wearing a costume.

### 3. Flavour 1 — target leakage, the loud one

> **target leakage** — a column that only exists, or only gets filled in, *because* the outcome already happened.

Our poisoned column is `customer_called_support`: **did this customer ring up to complain?** It arrives from another database, joined on by `support_calls.py`, and it looks exactly like a normal column. It is not. A customer rings up to complain *after* the pizza turns up late. At the moment you need the prediction — the moment the order is placed — that column is empty for every row, for ever.

Here is what it does to the score:

```text
with customer_called_support     accuracy=0.9700  roc_auc=0.9762
without it                       accuracy=0.7600  roc_auc=0.7752
the jump one column bought       +0.2011
```

**+0.2011 of AUC from one column.** Week 5's two surviving inventions (`is_rush`, `min_per_km`) bought +0.0091 between them. That ratio — twenty-two to one — *is* the alarm. Real features arrive in units of 0.005. A single column worth 0.2 is not a discovery.

Four audits catch it, each louder than the last, and then a fifth thing that is not an audit at all.

![Four alarms, and the one no computer can ring](../figures/fig-w06-5-four-audits-that-caught-it.svg)
*Figure 6.3 — Four alarms, and the one no computer can ring. The first four are arithmetic. The fifth is a question about the world, and it is the one that actually settles it.*

**Audit 1 — correlation with the answer.** `customer_called_support` scores **0.942**. The best honest column, `distance_km`, scores **0.345**. That is 0.942 ÷ 0.345 = **2.73 times bigger.** Nothing honest in a real table correlates 0.94 with the thing you are trying to predict; if it did, nobody would need a model.

**Audit 2 — count it against the answer.**

```text
late                        0    1
customer_called_support           
0                        1413   35
1                          12  540
```

Read the bottom row: **552 orders had a support call, and 540 of them were late.** 12 + 540 = 552, and 540 ÷ 552 = **0.9783**. The table is nearly diagonal. The column is almost a copy of the answer.

**Audit 3 — how well does the column do on its own?** Rank the validation rows by that one column's raw values alone (no model at all) and measure the AUC of that ranking: AUC **0.9556**. `distance_km` alone gets **0.6800**; `prep_minutes` alone gets **0.5739**. One column reaching 0.9556 by itself is not a feature, it is a label with a different name on it.

**Audit 4 — which knob is the model turning?**

```text
num__customer_called_support    3.482
num__distance_km                0.804
```

3.482 ÷ 0.804 = **4.33 times bigger** than the next thing. The model has stopped modelling and started reading.

**And then the fifth thing, which is not a statistic:**

> **🧑‍🏫 Ask this, and keep asking it all year:** *"At the moment I need the prediction, does this value exist?"*

For `customer_called_support` the answer is no, and that single question is worth more than all four audits together. It needs no data, no code and no maths. It is the sentence you want the student saying in June.

**Want to make it visceral? Show what the leaky model does on the day it is switched on.** Its column is 0 for every new order, because nobody has rung up yet:

```text
--- in the lab, where the column is filled in ---
accuracy 0.9700   recall 0.9217   roc_auc 0.9762

--- in production, where nobody has rung up yet, so it is always 0 ---
accuracy 0.7175   recall 0.0174   roc_auc 0.7924
late orders in these 400 rows: 115    late orders it flagged: 2
```

**In the lab it catches 92% of the late deliveries. In production it catches 2 out of 115.** That is what the 0.9762 was worth.

### 4. Flavour 2 — temporal leakage, the sneaky one

> **temporal leakage** — shuffling rows across a time boundary, so the model trains on the future and is tested on the past.

`train_test_split` shuffles. That is normally a good thing — Week 2 spent a whole lesson on why. But if your rows have a *time* in them and you will use the model *forward in time*, shuffling puts next month's rows into the training pile, and the model gets to see the future.

To make this visible we generate a small world where the rules **drift**. Thirty weeks, 100 orders a week, two features. Feature `x1` starts out mattering enormously and slowly stops mattering:

```text
how much x1 matters, week by week:
  week  0 : 2.0
  week 15 : 0.05
  week 29 : -1.77
```

That is `2.0 − 0.13 × week`, and you can check any row of it on paper: 2.0 − 0.13 × 15 = 2.0 − 1.95 = 0.05. ✅

Now split the same 3,000 rows two ways.

```text
rows in the random split : 2250 train, 750 test
rows in the time split   : 2200 train, 800 test

RANDOM split AUC  0.8139   <- what you would report
TIME   split AUC  0.5249   <- what production will give you
the gap           0.2890
```

**0.2890 of AUC, produced by nothing except where you cut.** Nothing else changed — same rows, same features, same model. The random split reports a good model. The time split reports roughly a coin flip (0.5249, one seed), and the time split is the one that matches how the thing will actually be used: trained on the past, run on the future. *(Mechanism, stated carefully: the model has no week column, so it cannot literally use the future. The random split averages the drift across all 30 weeks and so flatters it; the time-split model learns an `x1` rule from weeks 0–21 that has reversed by weeks 22–29. Say "drift that a random split hides" if a student pushes on "trained on the future".)*

![Trained on the future, tested on the past](../figures/fig-w06-4-temporal-leak-training-on-the-future.svg)
*Figure 6.4 — Trained on the future, tested on the past. The random split's train and test rows are interleaved through all 30 weeks, so the drift is averaged into the model and hidden from the score.*

**The tell:** *do the rows have a date, an order number, or anything else that says when they happened?* If yes, and if you will deploy forward in time, split by time.

**The honest caveat you should say out loud:** the delivery table does **not** drift — `make_data.py` uses the same rule for row 1 and row 2000 — so a random split is genuinely fine there. This flavour needed its own little dataset, and that is not a cheat; it is the only way to show a bug that our main table cannot have. Real tables usually can.

### 5. Flavour 3 — preprocessing leakage, the quiet one

> **preprocessing leakage** — any statistic worked out over all the data before the split: a scaler's mean, an imputer's median, a feature selector's ranking.

This is the one that sounds harmless. Surely a median is just a median? So here are two demonstrations, and the contrast between them is the lesson.

**Demonstration A — on our delivery table, it is worth nothing measurable.**

```text
median used by the wrong version : 29.0
WRONG - filled in before splitting           roc_auc=0.7751
RIGHT - imputer inside the Pipeline          roc_auc=0.7752
difference                                   -0.0000
```

One ten-thousandth, in the wrong direction. **You could never find this bug by looking at your score.** That is exactly why it survives in real code for years.

**Demonstration B — the same bug, at full strength, on data with nothing in it at all.**

Generate 200 rows and 2,000 columns of pure random noise, and a label that is a coin flip. There is **no relationship between X and y**, by construction — we built both of them out of a random number generator and never let them meet. Any honest method must score about 50%.

Then commit the bug: **pick the 20 columns that look most related to the answer, using all 200 rows and all 200 labels**, and only then measure.

```text
WRONG - 20 columns chosen while looking at every label
  five scores: [0.875 0.75  0.8   0.725 0.675]
  their total: 3.825   divided by 5: 0.765

RIGHT - the choosing is inside the Pipeline
  five scores: [0.425 0.475 0.6   0.425 0.675]
  their total: 2.600   divided by 5: 0.520   <- the truth
```

**76.5% accuracy on data containing no information whatsoever.**

Here is why, and it is the most important paragraph in the file. 2,000 columns of noise means **2,000 chances for a column to line up with the coin flip by luck.** Some of them will, beautifully — that is what 2,000 tries buys you. Choosing the best 20 *while looking at every label* hands the model a cheat sheet for the very rows it is about to be marked on. **Nothing about the model was wrong. The leak was upstream of it.**

![Three-quarters right, on data with nothing in it](../figures/fig-w06-3-noise-table-scoring-seventy-five.svg)
*Figure 6.5 — Three-quarters right, on data with nothing in it. 0.765 − 0.520 = 0.245 of pure invention, and there was nothing in the table to find.*

**And the structural fix is the reason `Pipeline` exists at all.** Everything inside a `Pipeline` is fitted on exactly the rows handed to `.fit()` and nothing else. Move the selection inside the pipeline — one line moved — and the bug becomes *unwriteable*. That is the deepest point of Term 1: you do not defend against this class of bug by being careful. You defend against it by using a structure in which it cannot be expressed.

### 6. Every line of this week's code, explained to someone who has never programmed

**`SimpleImputer(strategy="median")`**

```python
SimpleImputer(strategy="median")
```

`SimpleImputer` is a small machine with two buttons. When you `fit` it on some rows, it looks at each column and works out one number for it — with `strategy="median"`, the middle value — and remembers it. When you `transform` a table, it writes that remembered number into every blank. `strategy=` is where you choose which number: `"median"`, `"mean"`, or `"most_frequent"` for word columns.

The remembered numbers live in `.statistics_`, one per column, in the order you gave the columns:

```python
print(imp.statistics_)
```

```text
[ 2.91  4.   14.   18.   29.5 ]
```

Read it off against the column list: distance 2.91 km, items 4, prep 14.0 minutes, hour 18, experience 29.5 months. **The trailing underscore in `statistics_` is a scikit-learn convention meaning "I learnt this from data".** Anything with a trailing underscore did not exist before `.fit` was called — which is why asking for it too early raises an error, and that error is in the Debugging Clinic.

**`add_indicator=True`**

```python
SimpleImputer(strategy="median", add_indicator=True)
```

One extra instruction, one extra column. The imputer still fills the blanks — and it also appends a 0/1 column recording where they were. On four rows with one blank:

```text
in                        out
exp    dist               exp   dist  wasblank
10.0    1.0               10.0   1.0     0
20.0    2.0               20.0   2.0     0
 NaN    3.0               20.0   3.0     1
40.0    4.0               40.0   4.0     0
```

Two columns in, **three** columns out. Note where the new column went: **on the end**, after all the original ones, not next to the column it describes. That surprises people, and it matters when you are counting columns.

**`pipe.named_steps["prep"]`**

```python
prep = pipe.named_steps["prep"]
```

A `Pipeline` is a list of named stages. `named_steps` is the way in — you hand it the name you gave a stage and it hands you back the actual fitted object, so you can interrogate it. **The name has to match exactly**; `"pre"` when you wrote `"prep"` gives `KeyError: 'pre'`.

And then one warning that saves ten minutes. `named_steps["prep"]` is a `ColumnTransformer`, not an imputer — it is the thing that *contains* the imputer. So it has no `.statistics_` of its own. To reach the imputer you go one more step in:

```python
prep = pipe.named_steps["prep"]
print("its branches:", list(prep.named_transformers_.keys()))
imp = prep.named_transformers_["num"].named_steps["impute"]
print("what the imputer learned:", imp.statistics_)
```

```text
its branches: ['num', 'cat']
what the imputer learned: [ 2.91  4.   14.   18.   29.5 ]
```

Read that chain out loud as an address: *the pipeline's `prep` stage, its `num` branch, that branch's `impute` step, and what it learned.* It is long, and it is just a path through a nest of boxes.

**The crosstab, which is the audit you will use most**

```python
print(pd.crosstab(df["customer_called_support"], df["late"]))
```

`crosstab` counts how many rows fall into each combination. Two 0/1 columns give four counts in a 2×2 grid. If the two big numbers sit on one diagonal and the other two are tiny, **the two columns are nearly the same column** — and if one of them is the answer, you have found your leak. It is one line and it is the fastest audit there is.

### 7. The three misconceptions you will actually meet

**"But the score really did go up — surely that's good?"** This is the belief the whole lesson exists to break, and arguing about it in the abstract never works. Run `deploy.py`. In the lab, recall 0.9217. In production, recall 0.0174 — **two late deliveries caught out of 115.** The score went up and the model got worse. Let the numbers do it.

**"A median is just a median — how can it leak?"** Two answers, in this order. First, the small one: 29.0 and 29.5 are different numbers, and 29.0 was partly worked out from rows you were about to be marked on. Second, the big one: the noise table, where the "statistic worked out too early" was *which columns to keep* and it bought 24.5 percentage points of pure fiction. **Same bug, two sizes.**

**"Leakage means somebody cheated."** No, and this matters for the tone of the whole week. Nobody in the hospital story cheated. Somebody joined a table, and the join was correct, and the column was real, and the whole thing was reasonable at every step. **Leakage is a design accident, not dishonesty** — which is exactly why you need audits that run whether or not you suspect anything.

### 8. How deep to go, and where to stop

| Do not teach today | Where it lives |
|---|---|
| `cross_val_score`, `StratifiedKFold`, mean ± sd | **Week 11.** It appears inside the supplied `noise_leak.py` as a black box. If asked: "it splits the rows into five piles and scores five times instead of once, because 40 rows is not enough to trust. Week 11." |
| `SelectKBest` as a *tool* for choosing features | Nowhere in Level 3 as a tool. It appears today **only** as the thing that committed the crime. Choosing columns by hand with a written reason is the skill; Week 7 does exactly that. |
| `TimeSeriesSplit` | Name it in one sentence as "the thing you use instead of a random split when rows have dates". Do not demonstrate it. |
| Target encoding done properly (out-of-fold, smoothing) | Not this year. **Week 7's planted bug is the naive version**, so do not spoil it. |
| KNN or iterative imputation | Not this year. Median is enough and it is honest. |
| Precision, recall and the confusion matrix as *concepts* | **Week 8, next week.** `deploy.py` prints a recall today; call it "the fraction of the late ones it caught" and move on. Do not define it properly — you would be doing next week's lesson badly. |
| Opening the test pile | **Week 36.** Somebody will suggest it to "check whether the leak is really there". No. |
| Whether a 400-row validation number is trustworthy at all | **Week 11.** A strong student will notice that −0.0029 for the indicator is smaller than the wobble. They are right. Say "Week 11" and mean it. |

The line to hold in your head all lesson: **today the student learns that a number can be a lie, and learns four ways to catch it.** If they leave able to ask *"at the moment I need the prediction, does this value exist?"*, the lesson worked, even if everything else slipped.

---

### 9. 🧭 The Growing Map

The student guide carries **Where This Fits** — the same picture every week with one more piece filled in.
This is the last week of stage one, so today the map is doing a bigger job than usual: it closes a stage.

![The Level 3 pipeline in Week 6: the scaling and features tile closes on the three kinds of leakage](../figures/fig-w06-0-where-this-fits.svg)

*Figure 6.0 — Week 6's version. Both tiles of stage one are accounted for and the stage closes here. The ↻
on stage three is the training loop, still grey until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask *"which box did we do today?"*** — *scaling · features*, third week in it. Then the
   question this lesson has earned: *"we found the leak in a column. Which box did the leak actually get
   **into** the project through?"* Trace it with a finger: `customer_called_support` was a **column
   decision**, made in stage one, and it produced `0.9762` in stage two. **The bug and the symptom are in
   different boxes.** That is why leakage is hard to find and why it belongs at the end of stage one.
2. **Then close the stage out loud.** *"Count the boxes we have finished. Six weeks, two tiles, one stage —
   and not one of them was about choosing a model."* Ask what stage one was actually about. You want some
   version of **"deciding what the data is, honestly."** Then point at stage two and say next week the gold
   moves for the first time since September.
3. **Then the three forward pointers, ten seconds each:** Week 11's five folds, each of which has to stay
   honest on its own; Week 27, where the validation images must not be augmented; Week 35, where leakage
   shows up in production as a score that quietly decays. All three are dashed boxes on the map today. The
   point is that this week is not a topic they are finishing, it is a check they now run forever.

> **🧑‍🏫 Why this is worth two minutes.** Six weeks without a serious model is the hardest stretch of the
> year to justify, and today is the day it justifies itself: `+0.2011` from one dishonest column against
> `+0.0091` from two honest ones. The map is what turns that into a structural claim rather than a war
> story — the whole of stage one exists because stages two to five inherit whatever it got wrong.

**If a student asks whether the whole stage goes white next week:** yes. Both tiles solid, and the gold
moves to *baseline · four numbers*. Worth flagging today, because a stage changing state is the clearest
signal of progress the picture ever gives, and they should be looking for it.

---

## 🧰 Prep Checklist

This section lists everything to prepare before the lesson, and holds the complete runnable files.

### 25 minutes the night before

**1. (1 min) Check the folder.**

```bash
ls make_data.py
python3 -c "import sklearn; print(sklearn.__version__)"
```

`make_data.py` must be the **unchanged** Week 1 file. Prove it:

```bash
python3 make_data.py
```

```text
shape: (2020, 10)
 order_id restaurant  distance_km  items  prep_minutes  order_hour day_of_week weather  driver_experience_months  late
   100955     Napoli         2.78      3          15.0          12         Mon   clear                       5.0     0
   101493 CrustyBros         3.09      5          12.9          22         Mon    rain                       0.0     0
   101857 CrustyBros         2.65      2          14.2          16         Mon    rain                      33.0     0
   100215     Napoli         9.60      2           4.9          13         Tue   clear                      27.0     1
   100506 CrustyBros         2.33      5          19.6          20         Thu   clear                      35.0     0
```

**If the first `order_id` is not 100955, stop.** Every number in this file depends on that table.

**2. (2 min) Create `support_calls.py`. This is a supplied file. Do not show its contents to the student before the Crime Scene is over — it gives the answer away in three lines.**

```python
"""support_calls.py - joins the customer-service call log onto the delivery table.

SUPPLIED FILE. It stands in for a real join against another database:
somewhere there is a table of complaint calls, and somebody matched it
to the delivery rows by order_id. A fixed seed keeps the log the same
every time you run it.
"""
import numpy as np


def attach_support_calls(df):
    """Add customer_called_support: 1 if this customer rang up to complain."""
    rng = np.random.default_rng(3)
    u = rng.random(len(df))
    called = np.where(df["late"].to_numpy() == 1, u < 0.94, u < 0.01)
    return df.assign(customer_called_support=called.astype(int))
```

**3. (5 min) Create and run `fill_blanks.py`.** Complete file in the **🔑 Answer Key**, under **📁 The teacher scripts** (`fill_blanks.py`). Run it and check you get exactly this:

```text
--- where the holes are ---
blanks in the whole table : 106
blanks in the 1200 train  : 60
blanks in the  400 val    : 25
blanks in the  400 test   : 21

--- two candidate fill-in numbers ---
median of the WHOLE table : 29.0
median of the TRAIN rows  : 29.5

--- what the imputer actually learned ---
statistics_ : [ 2.91  4.   14.   18.   29.5 ]

--- is being blank itself a signal? ---
late rate, rows with a value : 0.2947
late rate, rows that are blank: 0.15

--- with the indicator column, and without ---
add_indicator=False cols= 20  accuracy=0.7600  roc_auc=0.7752
add_indicator=True  cols= 21  accuracy=0.7550  roc_auc=0.7723

the new column is called: num__missingindicator_driver_experience_months
its weight: -0.1609
```

**Runtime: about 0.8 seconds.** 60 + 25 + 21 = 106. ✅

**4. (5 min) Create and run `mystery.py` and `leak_hunt.py`.** Both complete in the Answer Key: `mystery.py` under **🕵️ The Crime Scene**, `leak_hunt.py` under **📁 The teacher scripts**. `mystery.py` is what the student is handed at the start of the Crime Scene — **print one copy of its output per student and nothing else.**

```text
columns going into the model: 21
validation accuracy : 0.9700
validation roc_auc  : 0.9762
Week 5's best honest score was 0.7843.  Congratulations?
```

**5. (4 min) Create and run `temporal.py`.** Complete file in the Answer Key, under **📁 The teacher scripts** (`temporal.py`). Expected:

```text
RANDOM split AUC  0.8139   <- what you would report
TIME   split AUC  0.5249   <- what production will give you
the gap           0.2890
```

**6. (4 min) Create and run `noise_leak.py`.** Complete file in the Answer Key, under **📁 The teacher scripts** (`noise_leak.py`). It contains **both halves** — the leaky route and the fixed route — so one run prints both numbers, and you must get `0.765` and then `0.520`. The homework asks the student to comment out the wrong half and prove the right half on its own, which is why the file is built this way.

**7. (4 min) Print and set up.**

- The Week 6 workbook, printed **without its Answers section** (sections: Warm-Up, Do the Maths by Hand, Predict the Output, Practice Set A and B, Fix the Broken Program, Puzzle of the Week, Think Deeper, Build It, Draw It, Self-Check).
- Plain paper, one sheet each, for the Crime Scene notes — the workbook has no page for them.
- **One printed copy of `mystery.py`'s output per student.** Nothing else printed for the Crime Scene — no code, no hints.
- The whiteboard divided into **three columns**, headed `target`, `temporal`, `preprocessing`, each with three empty rows underneath labelled *what it is · fake score · honest score*. Leave it empty and visible.
- A timer. The Crime Scene is **twelve minutes** and it needs to be twelve.
- Figures 6.1 and 6.3 printed, **face down.** They are the answers.

### 5 minutes on the day

- Terminal open in the project folder. `mystery.py`, `leak_hunt.py`, `temporal.py`, `noise_leak.py`, `deploy.py` all present and all already run once, so the output is in the scrollback if a laptop dies.
- The empty three-column table on the board.
- On a corner of the board, from last week and left up all lesson: `Week 5's best honest score: 0.7843`.

### Fallback if the laptops fail

| If this fails | Do this instead |
|---|---|
| No Python at all | **The Crime Scene works entirely on paper**, and it is the heart of the lesson. Hand out the printed `mystery.py` output and the printed column list (21 columns, one of them `customer_called_support`) and run the full twelve minutes. Then read out the four audits from Figure 6.3 one at a time. You lose nothing that matters. |
| `make_data.py` missing or edited | Every delivery number in the file is wrong and you cannot fix it in five minutes. Switch to the printed outputs above and **find the file before Week 7**, which is built entirely on it. |
| The noise experiment will not run | Read the two lines of output from the board: `0.765` and `0.520`. Then ask the question that carries the whole idea: *"there is nothing in that table. Where did 76.5% come from?"* The discussion is worth more than the run. |
| A student's numbers differ from the book | Almost always one of three things: `make_data.py` edited, a missing `drop_duplicates()`, or `random_state` not 42. Check in that order. |

---

## ⏱️ The Lesson, Minute by Minute

Use this section to run the class: the timing table first, then each segment in order.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Model That Read the Answer | 7 | 7 | The hospital story, and 0.9762 on the board |
| 🧠 Concept — Filling Blanks, Then Three Flavours | 18 | 25 | 29.0 against 29.5; then target, temporal, preprocessing |
| 💻 Live-Code Together — Four Audits | 18 | 43 | Two deliberate mistakes: one shouts, one is silent and worth nothing |
| 🎲 Their Turn — The 0.9762 Crime Scene | 20 | 63 | Twelve silent minutes, no hints; then the noise table together |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — The Model That Read the Answer (7 minutes)

**Do this:** Write nothing but this on the board.

```text
Week 5's best honest score:   0.7843
This week's model:            0.9762
```

Say nothing for a moment. Let them react — they will be pleased.

> **Say this:** "A hospital built a model to predict which patients would end up needing intensive care. It scored brilliantly. Better than the doctors. Everybody was delighted, and somebody made a slide about it.
>
> Then one person asked a boring question: **which column is the model leaning on hardest?** And the answer was a column recording which ward the patient had been moved to. Patients who were moved to the intensive-care ward needed intensive care.
>
> The model had not learnt medicine. It had learnt to read a form that only gets filled in **after** the decision has already been made."

Pause properly here.

> "That has a name. It is called **data leakage** — a column that contains information you would not actually have at the moment you need the prediction.
>
> And here is the thing I want you to take away before we do anything else. **Leakage almost always makes your score go up.** Almost always. Which means it is nearly the only kind of bug that gets applauded. A bug that makes your number worse gets fixed on Tuesday because somebody is annoyed about it. A bug that makes your number better gets a presentation and six months in production being wrong.
>
> So from today the rule changes. **Good news gets audited harder than bad news.**"

**Do this:** Point at the 0.9762.

> **Say this:** "That is a real number, from a real model, fitted on your delivery table this morning. Nineteen points better than everything you did last week put together.
>
> In about half an hour I am going to hand you that model and twelve minutes, and you are going to tell me what is wrong with it. I am not going to help."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "The hospital model was 'wrong'. But it *was* right about who needed intensive care. So what exactly was wrong with it?" | It could only be right after the answer was already known, so it was useless for deciding anything. | If they say "the data was bad", push: "the column was completely accurate. Every value was true. So what's the problem?" (*When* it becomes true.) |
| "Give me a column that could exist in our delivery table and would be a leak." | `refund_issued`, `actual_delivery_time`, `driver_arrived_at`, `customer_complained`. | Anything after-the-fact earns a tick. If they name a legitimate column, ask when its value gets filled in. Week 1 already had this conversation once — remind them. |
| "Why is a bug that makes the score go up more dangerous than one that makes it go down?" | Because nobody looks for it. | If they don't get there, say it yourself. It is the sentence of the week. |
| "How suspicious should 0.9762 make you, on a scale of nought to ten?" | **Ten.** | If they say "it depends", that is a *better* answer — agree, then ask what it depends on. (How much one column jumped. Real features move 0.005.) |

---

### 🧠 Concept — Filling Blanks, Then Three Flavours (18 minutes)

**Part 1 (6 min) — the 106 blanks, and the two medians.**

> **Say this:** "Small piece of unfinished business first. Since Week 1, your `driver_experience_months` column has had holes in it. **106 of them, out of 2,000 rows.** You have never done anything about it, because a machine has been quietly patching them for you inside the pipeline. Today we look at what it actually put there.
>
> Three choices. **One:** delete those 106 rows. What's wrong with that?"

*You lose 106 rows of evidence.*

> "Yes — and something worse. What if the paperwork is worse for brand-new drivers? Then you've just deleted all the new drivers, and your model has never met one.
>
> **Two:** write in 0. What's wrong with that?"

*Zero means "no experience", not "we don't know".*

> "Exactly. Zero is a **lie the model will believe.**
>
> **Three:** write in the middle value of the column — the **median**. It's still a guess, but it's the least wrong guess and it doesn't invent an extreme. That's the one we use, and it has a name: **imputation**."

**Do this:** On the board:

```text
1140 training rows have a value.  1140 is even.
the two middle ones are number 570 and number 571:

        570th = 29        571st = 30

        (29 + 30) / 2  =  29.5
```

> **Say this:** "That's it. That's the whole calculation. And now the only question that matters, and you already know the answer because it's Week 2's rule wearing a hat: **which rows is that machine allowed to look at?**"

**Ask this:** "The median of all 2,000 rows is 29.0. The median of the 1,200 training rows is 29.5. Which one may I use, and why?"

*29.5 — because 29.0 was partly worked out from the validation and test rows.*

> **Say this:** "Right. And notice how small that is. Twenty-nine against twenty-nine and a half. Hold onto how small it feels, because in about twenty minutes I am going to show you the exact same mistake being worth twenty-four percentage points."

**Part 2 (12 min) — the three flavours.**

**Do this:** Fill in the three column headings on the board out loud as you name them: `target`, `temporal`, `preprocessing`.

> **Say this:** "There are three ways to get handed the answer, and every single one of them makes your score go up.
>
> **Flavour one: target leakage.** A column that only exists *because* the outcome already happened. The hospital's ward column. And, as it happens, one of the twenty-one columns in the model I'm about to hand you.
>
> **Flavour two: temporal leakage.** This one is sneakier because the bug is not in a column at all — it is in how you cut. `train_test_split` shuffles the rows, which has been a good thing for four weeks. But if your rows happened at *times*, and you're going to use the model on *next month*, then shuffling puts next month into the training pile. **You trained on the future.**"

**Do this:** Draw two strips of thirty blocks on the board. In the first, scribble train/test marks all the way along, interleaved. In the second, mark the first twenty-two blocks train and the last eight test.

> **Say this:** "Same rows. Same model. Same features. Two ways to cut. Here's what happens in a world where the rules slowly change — where something that used to matter a lot gradually stops mattering.
>
> Random split: **0.8139.** Time split: **0.5249.** Subtract."

*0.2890.*

> "Nearly three tenths of AUC, produced by nothing but where you put the scissors. And the one on the right is the true one, because that's how the model will actually be used: trained on the past, run on the future.
>
> The tell is a question: **do my rows have a date on them?** If yes, and if I'll deploy forwards in time, I split by time.
>
> One honest note — your delivery table doesn't drift. `make_data.py` uses the same rule for row 1 and row 2000, so a random split is genuinely fine there. I had to build a separate little world to show you this one. Real tables usually do drift.
>
> **Flavour three: preprocessing leakage.** Any number worked out *before* you cut. A median. An average. A choice of which columns to keep. **This is the 29.0 you rejected five minutes ago**, and on your delivery table it is worth — let's see it later — essentially nothing. Which is precisely what makes it dangerous: you can never catch it by looking at your score."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which of the three is a bug in a *column*, and which are bugs in *how you cut*?" | Target is a column. Temporal and preprocessing are both about the cut. | If they get it backwards, walk it through once more with the three headings on the board. This distinction is the spine of the week. |
| "0.8139 and 0.5249. Which of those is the lie?" | 0.8139. | If they say 0.5249 "because it's worse", press: "which of the two matches how we'll actually use it?" |
| "Why is 'the median of all the rows' a leak if the median is only one number?" | Because that number was partly computed from rows you were about to be marked on. | If they say "it's basically the same number anyway", agree — and promise them a case where it is worth 24 points. Do not resolve it yet. |
| "Name the tell for each flavour." | *Is it filled in yet? · Do the rows have a date? · Was it fitted before the cut?* | Write all three on the board and leave them up. They go on the student's Build It page (the three-repairs table and its tells). |
| "Could a leak ever make your score go *down*?" | **This one is genuinely open.** | Take the discussion. The honest answer is in the Questions section: contrived cases exist, but if you find one in the wild you almost certainly have a different bug. Do not fake certainty. |

---

### 💻 Live-Code Together — Four Audits (18 minutes)

**You never touch the keyboard.** Predictions before every run.

**Step 1 (3 min).** New file, `fill_blanks.py`. Type only the top — the counting part.

```python
"""fill_blanks.py - filling in the 106 holes, and marking where they were."""
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from make_data import make_deliveries

RS = 42
NUM = ["distance_km", "items", "prep_minutes", "order_hour",
       "driver_experience_months"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

print("blanks in the whole table :", int(X["driver_experience_months"].isna().sum()))
print("blanks in the 1200 train  :", int(X_tr["driver_experience_months"].isna().sum()))
print("median of the WHOLE table :", X["driver_experience_months"].median())
print("median of the TRAIN rows  :", X_tr["driver_experience_months"].median())
```

**Ask before running:** "106 blanks altogether. Roughly how many land in the 1,200 training rows?"

*About 60 — 1,200 is 60% of 2,000.*

Run it. Real output:

```text
blanks in the whole table : 106
blanks in the 1200 train  : 60
median of the WHOLE table : 29.0
median of the TRAIN rows  : 29.5
```

> **Say this:** "Sixty. Good arithmetic. And there are your two candidate numbers — 29.0 and 29.5 — and you already know which one you're allowed."

**Step 2 — ⚠️ FIRST DELIBERATE MISTAKE (3 min).** The loud one.

> **Say this:** "Let's skip the imputer entirely. Hand the raw columns straight to the model — it's a computer, it can cope with a blank."

```python
from sklearn.linear_model import LogisticRegression
LogisticRegression(max_iter=2000).fit(X_tr[NUM], y_tr)
```

Run it. Real output (last three lines):

```text
    raise ValueError(msg_err)
ValueError: Input X contains NaN.
LogisticRegression does not accept missing values encoded as NaN natively. For supervised learning, you might want to consider sklearn.ensemble.HistGradientBoostingClassifier and Regressor which accept missing values encoded as NaNs natively. Alternatively, it is possible to preprocess the data, for instance by using an imputer transformer in a pipeline or drop samples with missing values. See https://scikit-learn.org/stable/modules/impute.html You can find a list of all estimators that handle NaN values at the following page: https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values
```

> **Say this:** "`Input X contains NaN.` **NaN** is how a computer writes 'not a number' — it is what a blank looks like from the inside.
>
> And read the rest of that message, because it is unusually generous: *'it is possible to preprocess the data, for instance by using an imputer transformer in a pipeline.'* The error message contains the fix. That happens more often than people expect, and most people never read far enough to find out."

**Step 3 (4 min).** Now the imputer, the indicator, and the ablation.

```python
imp = SimpleImputer(strategy="median")
imp.fit(X_tr[NUM])
print("statistics_ :", imp.statistics_)
```

```text
statistics_ : [ 2.91  4.   14.   18.   29.5 ]
```

> **Say this:** "Five numbers, one per column, in the order I listed them. Distance 2.91. Items 4. Prep 14.0. Hour 18. Experience **29.5** — the training median, and nothing else. **The trailing underscore on `statistics_` means 'I learnt this from data'.** Anything in scikit-learn with an underscore on the end did not exist before you called `.fit`."

Then the indicator, and the ablation from Week 5:

```text
add_indicator=False cols= 20  accuracy=0.7600  roc_auc=0.7752
add_indicator=True  cols= 21  accuracy=0.7550  roc_auc=0.7723
```

**Ask:** "Subtract."

*0.7723 − 0.7752 = −0.0029.*

> **Say this:** "**Worse.** So it goes. Same rule as last week: a column earns its place or it leaves, and a shiny new tool does not get an exemption. Why didn't it pay? Because `make_data.py` chose the blanks with a coin flip — you can read the line. There is no story about rookie drivers hiding in there to find."

**Step 4 — ⚠️ SECOND DELIBERATE MISTAKE (4 min).** The silent one, and it is the more important of the two.

> **Say this:** "Now let's be helpful and tidy. Fill the blanks in properly at the top of the script, before we split, so the data is clean before anything touches it. That's how you'd do it by hand."

```python
pre_filled = df.copy()
pre_filled["driver_experience_months"] = \
    pre_filled["driver_experience_months"].fillna(
        pre_filled["driver_experience_months"].median())
```

**Ask before running:** "What breaks?"

Most will say nothing.

Run the full comparison. Real output:

```text
median used by the wrong version : 29.0
WRONG - filled in before splitting           roc_auc=0.7751
RIGHT - imputer inside the Pipeline          roc_auc=0.7752
difference                                   -0.0000
```

**Do this:** Let it sit.

> **Say this:** "**No error. No warning. And the score is the same to three decimal places.**
>
> So it's fine, yes? No. It is a leak — the 29.0 was partly worked out from the 800 rows you were going to be marked on — and it happens to be worth almost nothing on this table. **Which is the worst possible combination.** A bug that shouts is a good day. A bug that changes your score by minus nought-point-nought-nought-nought-nought is a bug that lives in your code for three years.
>
> You cannot catch this one by looking at your score. You catch it by looking at *where the statistic was computed*. And in twenty minutes I am going to show you the identical mistake being worth twenty-four points."

**Step 5 (4 min).** The four audits. Run `leak_hunt.py` — do not type it, it is long and it is in the Answer Key.

**Ask before running:** "Which column do you think is the problem, out of the twenty-one?"

Take guesses. Write them down.

Real output:

```text
--- the two scores ---
with customer_called_support     accuracy=0.9700  roc_auc=0.9762
without it                       accuracy=0.7600  roc_auc=0.7752
the jump one column bought       +0.2011

--- audit 1: how strongly does each number move with late? ---
customer_called_support     0.942
distance_km                 0.345
driver_experience_months   -0.123
items                       0.106
prep_minutes                0.066
order_hour                  0.064

--- audit 2: the suspect, counted against the answer ---
late                        0    1
customer_called_support           
0                        1413   35
1                          12  540

--- audit 3: how well does each column do ON ITS OWN? ---
  customer_called_support    AUC 0.9556
  distance_km                AUC 0.6800
  prep_minutes               AUC 0.5739

--- audit 4: which knob is the model actually turning? ---
num__customer_called_support    3.482
num__distance_km                0.804
cat__restaurant_GreenLeaf      -0.744
cat__weather_clear             -0.679
```

> **Say this, one audit at a time — do not read it all at once:**
>
> "**The jump: +0.2011 from one column.** Last week your two surviving inventions bought 0.0091 between them. This is twenty-two times that, from one column. **That ratio is the alarm.**
>
> **Audit one, correlation: 0.942 against 0.345.** Two point seven times the best honest column. Nothing real correlates 0.94 with the thing you're trying to predict — if it did, nobody would need a model.
>
> **Audit two, the crosstab. Read me the bottom row.** *(12 and 540.)* So 552 orders had a support call and 540 of them were late. 540 over 552 is 0.9783. **The column is nearly a photocopy of the answer.**
>
> **Audit three, on its own: 0.9556.** One single column, no help from anything else, gets 0.9556. `distance_km` on its own gets 0.6800. That is not a feature.
>
> **Audit four, the weights: 3.482 against 0.804.** Four and a third times the next one. The model has stopped modelling and started reading."

**Do this:** Then close the laptop lid halfway and ask the question that matters.

> **Say this:** "Now forget every one of those numbers. **At the moment a customer places an order, has that customer already rung up to complain about a delivery that hasn't arrived yet?**"

*No.*

> "No. That question needed no data, no code and no maths, and it is worth more than all four audits together. **Learn that sentence: at the moment I need the prediction, does this value exist?** I want to hear you say it in June."

---

### 🎲 Their Turn — The 0.9762 Crime Scene (20 minutes)

Full instructions in the next section. In brief: twelve silent minutes with the printed score, the column list and a laptop, and **no hints at all**; then eight minutes reproducing 76.5%-on-pure-noise together and sitting with it.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Turn Figures 6.1 and 6.3 face-up beside the completed three-column table.

> **Say this:** "Five things.
>
> **One.** Blanks get filled with a number learned from **the training rows only**. 29.5, not 29.0. And you may add a 0/1 column marking where the blank was — but it is a hypothesis like any other, and ours lost by 0.0029, so it went.
>
> **Two.** Three flavours, three tells. **Target:** is the value filled in yet? **Temporal:** do the rows have a date? **Preprocessing:** was the statistic worked out before the cut?
>
> **Three.** All three make the score go **up**. That is the whole reason today exists. From now on, when your number jumps, your first feeling is suspicion, not pride.
>
> **Four.** Four audits, cheap and quick: correlation with the answer, the crosstab, one column on its own, and the size of the weight. Run them on good news.
>
> **Five, and this is the one I want.** There is a question no computer can answer for you: **at the moment I need the prediction, does this value exist?** The support-call model scored 0.9762 in the lab and caught **two** late deliveries out of 115 in production. One sentence would have saved it."

Run the three checks from **✅ Assessing Understanding**, then assign the homework.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Input X contains NaN.` followed by a long paragraph about `HistGradientBoostingClassifier` | "One of your numbers is a blank and I cannot multiply by a blank." | The model is being fitted on `driver_experience_months` with no imputer in front of it. | Put `SimpleImputer(strategy="median")` in the numeric branch of the `ColumnTransformer`. **The fix is written in the error message itself** — read to the end of it. |
| `ValueError: Cannot use median strategy with non-numeric data:` `could not convert string to float: 'clear'` | "You asked me for the middle number of a list of words." | A word column — `weather`, `restaurant` — went down the numeric branch. | Send it down the categorical branch. If you really need to impute a word column, `strategy="most_frequent"`. |
| `AttributeError: 'SimpleImputer' object has no attribute 'statistics_'` | "I have not looked at any data yet, so I have not learnt anything." | `imp.statistics_` before `imp.fit(...)`. | Fit first. **The trailing underscore means "learnt from data"** — nothing with an underscore on the end exists before `.fit`. |
| `AttributeError: 'ColumnTransformer' object has no attribute 'statistics_'` | "You are asking the box, not the thing inside the box." | `pipe.named_steps["prep"].statistics_`. The `prep` stage is a `ColumnTransformer`; the imputer lives inside its `num` branch. | Go one level deeper: `pipe.named_steps["prep"].named_transformers_["num"].named_steps["impute"].statistics_`. |
| `KeyError: 'pre'` | "There is no stage with that name." | `pipe.named_steps["pre"]` when the stage was named `"prep"`. | Use the exact name from the `Pipeline` list. `print(pipe.named_steps.keys())` shows all of them. |
| `ValueError: columns are missing: {'customer_called_support'}` | "The table you just gave me is missing a column I was fitted with." | The pipeline was fitted with the leaky column, and now a real row has arrived without it. | **This error IS the lesson.** It is the pipeline telling you the column cannot exist at prediction time. Drop it from the feature list and refit. |
| `ValueError: Found unknown categories ['PopUpPizza'] in column 0 during transform` | "A new restaurant turned up and I was never told it could." | `OneHotEncoder()` without `handle_unknown="ignore"`. | `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` — Week 4's habit, and it will bite again all year. |
| `ValueError: X has 2000 features, but LogisticRegression is expecting 70 features as input.` | "You trained me on a narrow table and handed me a wide one." | The selector was run on the training rows but not on the test rows: `m.predict(X_te)` instead of `m.predict(sel.transform(X_te))`. | Put the selector **inside** a `Pipeline` so it can never be forgotten. This bug is the reason `Pipeline` exists. |
| `UserWarning: Skipping features without any observed values: ['b']. At least one non-missing value is needed for imputation with strategy='median'.` | "That column is blank all the way down, so there is no middle number to find." | A column with 100% missing values. | Drop the column. It contains nothing. Note that this is a **warning**, not an error — your script carried on and silently gave you fewer columns than you thought. |
| `UserWarning: k=70 is greater than n_features=50. All the features will be returned.` | "You asked for 70 columns out of 50." | `SelectKBest(k=70)` on a 50-column table. | Not fatal — you got all 50. But you also got no selection at all, which is probably not what you meant. |
| **No error**, and the score barely changes | Nothing is wrong as far as Python is concerned. | A statistic computed before the split. Our version cost **−0.0000** of AUC. | Look at *where* the statistic was computed, not at the score. **You cannot detect this one by measurement.** Move it inside the `Pipeline`. |
| **No error**, and the score is wonderful | Nothing is wrong as far as Python is concerned. | A leak. | Run the four audits. Then ask whether the value exists at prediction time. |

### How to teach debugging without giving the answer

The moves from Weeks 1–5 all stand. This week adds three, and the last one is the most valuable thing in the file.

- **"Read to the end of the message."** This week's first error contains its own fix in the last sentence. Most students stop at the red word. Make finishing the paragraph a habit now.
- **"Print the crosstab."** When a score looks too good, `pd.crosstab(suspect, target)` is one line and settles it in four seconds. Ask for it before you ask anything else.
- **"When does that value get filled in?"** Not "is that column allowed" — that invites a guess. Ask *when*, and the student has to think about the world instead of the code, which is where the answer is.

And the sentence for this week:

> **"An error that shouts is a good day. A score that shouts is a bad one."**

---

## 🎲 The Activity, In Full

This section gives the full set-up and running order of the week's activity.

### The 0.9762 Crime Scene

**Setup (1 minute).** Every student gets:

- one printed copy of `mystery.py`'s output — **the four lines and nothing else**;
- one printed list of the 21 column names going into the model;
- a laptop with the delivery folder on it;
- a sheet of plain paper to write the investigation on (the workbook has no page for the Crime Scene; the student lists each check and its result, including dead ends).

The whiteboard still says `Week 5's best honest score: 0.7843`. Set the timer for twelve minutes.

**Do NOT hand out `support_calls.py`.** Three lines of it give the whole thing away.

---

### Part 1 — Twelve silent minutes, no hints (12 minutes)

**The instruction, given once and then not repeated:**

> **"This model scores 0.9762 on the validation pile. Last week your best honest score was 0.7843. Something is wrong with it. You have twelve minutes and I am not going to help you. Write down what you tried, including the things that led nowhere."**

**Rules to state up front:**

- You may run anything you like. You may not open `support_calls.py`.
- **Write down every check you run, including the failures.** The sheet is the deliverable, not the answer.
- No talking for the first eight minutes. Pairs allowed for the last four.

**What you do during the twelve minutes:** walk about, read over shoulders, and say **nothing evaluative.** Not "good", not "warm", not "hmm". If somebody has done nothing for four minutes, one neutral prompt only:

> *"You have twenty-one columns. Which one would you bet on, and how would you check?"*

**The routes they actually take, and what to do:**

| What they do | What to say |
|---|---|
| Print the column list and spot the name `customer_called_support` | **This is the fastest correct route and it deserves full credit.** "Good. Now prove it with a number." |
| Correlate every column with `late` | "That's audit one. What did you get?" (0.942.) Then: "Is that a lot? Compared to what?" |
| Crosstab the suspect against `late` | "That's the fastest audit there is. Read me the bottom row." |
| Fit the model twice, with and without | "That's an ablation — same tool as last week. What's the delta?" (+0.2011.) |
| Look at the coefficients | "Which one is biggest, and by how many times?" (3.482 against 0.804.) |
| Blame the model, or `max_iter`, or the scaler | Do not correct. Ask: *"is a model allowed to be this good on data this messy?"* |
| Go quiet and stare at the printout | Leave them. Staring at a column list is a legitimate investigative technique and it works. |
| Try to open `support_calls.py` | "Not that one. Everything else is fair game." |

---

### Part 2 — Twenty seconds each, out loud (3 minutes)

Round the room. Each student says **one sentence**: what they checked and what it told them. Write each finding in the `target` column of the board table.

Then the two numbers go in: **fake 0.9762, honest 0.7752.**

Then run `deploy.py` and let the room go quiet:

```text
--- in the lab, where the column is filled in ---
accuracy 0.9700   recall 0.9217   roc_auc 0.9762

--- in production, where nobody has rung up yet, so it is always 0 ---
accuracy 0.7175   recall 0.0174   roc_auc 0.7924
late orders in these 400 rows: 115    late orders it flagged: 2
```

> **Say this:** "In the lab it caught 92% of the late deliveries. On the day it was switched on, it caught **two out of 115.**"

---

### Part 3 — 76.5% on nothing at all (5 minutes)

Everybody runs `noise_leak.py` together, at the same time.

**Before running, say this and mean it:**

> "This table is 200 rows and 2,000 columns of pure random noise, and a label that is a coin flip. I made both of them out of a random number generator and I never let them meet. **There is nothing in there. There cannot be anything in there.** So what score should an honest method get?"

*50%.*

Run it. Real output:

```text
X shape: (200, 2000)
y: 98 ones and 102 zeros
There is no relationship between X and y. There cannot be one.

WRONG - 20 columns chosen while looking at every label
  five scores: [0.875 0.75  0.8   0.725 0.675]
  their total: 3.825   divided by 5: 0.765

RIGHT - the choosing is inside the Pipeline
  five scores: [0.425 0.475 0.6   0.425 0.675]
  their total: 2.600   divided by 5: 0.520   <- the truth
```

**Do this: say nothing for thirty seconds.** Let them look at 0.765.

> **Say this:** "Seventy-six and a half per cent, on a table with nothing in it.
>
> Two thousand columns of noise is **two thousand chances for a column to line up with a coin flip by luck.** Some of them will, beautifully. And when you pick the best twenty *while looking at every single label*, you have handed the model a cheat sheet for the exact rows it is about to be marked on.
>
> Nothing about the model was wrong. **The leak was upstream of it.**
>
> And now the important half: look at what fixes it. One line moved. The choosing goes **inside** the `Pipeline`, so it only ever sees training rows. Not 'be more careful'. **Move the line, and the bug becomes impossible to write.** That is what a `Pipeline` is actually for, and it took you six weeks to find out."

**What "finished" looks like:** the three-column board table full — nine cells, each flavour with its tell, its fake score and its honest score. Every student's investigation sheet carries at least three checks they ran, including the ones that went nowhere.

---

### Variation — easier

**Cut the twelve minutes to six, and hand over the column list with a narrower brief:** *"one of these twenty-one columns is the problem. Find it, and prove it with one number."* Naming `customer_called_support` from the name alone and confirming it with a crosstab is objectives 2 and 4 complete.

**Better still, for a student who freezes on open-ended work:** give them the answer at the start and make them the **prosecutor** instead of the detective. *"It's `customer_called_support`. Your job is to prove it four different ways."* Running four audits on a known culprit teaches the audits better than hunting does, and it removes the part they find impossible.

### Variation — harder

1. **Invent the leak.** Add a column to the delivery table that leaks, get it past all four statistical audits, and then defeat it with the "does it exist yet" question. (A good attempt: `driver_shift_overtime_minutes` = `25 × late + noise`. It looks like an honest operational number and it correlates about 0.7.)
2. **Break the noise experiment on purpose.** Change 2,000 columns to 50. Does 76.5% survive? (No — fewer columns, fewer lucky coincidences.) Then: how many columns do you need before the fake score gets interesting? Plot it.
3. **Find the temporal leak in the delivery table.** `order_id` counts upwards, so it is a clock. Split on `order_id` instead of at random and compare. **The finding is that nothing happens**, and the explanation is worth more than a result: `make_data.py` uses the same rule for row 1 and row 2000, so there is no drift to leak.
4. **Prove the −0.0029 verdict on the missing indicator is honest.** Re-run with `RS = 0, 1, 2`. Does the indicator lose every time? If it wins once, what does that tell you about a 400-row validation number? (Week 11.)
5. **The hardest question in the week, in writing:** *"Which of the three flavours would be hardest to spot at your first job, and why?"* There is a defensible answer and it is not the loud one. See the marking note in the Answer Key.

---

## ❓ Questions Students Ask This Week

These are the questions students raise this week, each with a suggested reply.

**"If the column is real and the value is true, how is using it cheating?"**

**It is not cheating and nobody lied.** Every value in `customer_called_support` is accurate. The problem is not truth, it is **timing**.

Line up the two moments. The moment you need the prediction: a customer has just clicked *order*. The moment the column gets a value: the pizza has already arrived late and the customer has already rung up. Those moments are an hour apart, and the model is being trained as though they were the same moment.

So the useful phrasing is not "is this column allowed?" — it is **"when does this value appear?"** That question has a factual answer and it settles every case.

**"Couldn't we keep it and just use it for the orders where somebody has called?"**

This is a genuinely good idea and it is worth taking seriously for a minute, because the reasoning kills it cleanly.

By the time somebody has called to complain, **you no longer need a prediction.** You know. The whole point of the model is to warn the kitchen *before* the delivery is late, so a feature that only exists afterwards can never be used for the thing the model is for. It is a very expensive `if` statement that reads the answer.

**"What if a leaky feature is the only thing that works? Do I just ship a bad model?"**

You ship the honest one and you say what it is worth. 0.7752 that works is worth infinitely more than 0.9762 that does not, and you now have `deploy.py` to prove it: recall 0.9217 in the lab, **0.0174** in production.

And then there is a real engineering answer underneath. If the leaky column is genuinely predictive, ask **what it is a proxy for.** People ring up when a delivery is late; deliveries are late when the route is long or the weather is bad. So the honest columns are distance and weather, and you already have them. **A leak is often a shadow cast by something legitimate**, and chasing the shadow back to the object is how real features get found.

**"How would I catch this at a real job, where nobody tells me there's a bug?"**

You would not catch it by being clever. You would catch it with a habit, and there are four:

1. Print the column list before you fit anything, and read every name out loud.
2. Correlate every numeric column with the target, every time, and look at the top of the list.
3. For any suspicious score, fit without the suspect and compare.
4. **For every column, write one sentence saying when its value appears.** That sentence goes in the model card from Week 3, and it is why the model card has a data-provenance heading.

Habit four is the one that actually works, and it is the one nobody does.

**"Is a median really a leak? It's one number out of 2,000 rows."**

Yes, and the interesting part is *how much* of a leak, because the answer is "it depends entirely on what the statistic is".

A single median over 2,000 rows carries almost nothing about any individual row — which is why the delivery table's version cost −0.0000. But *which 20 of 2,000 columns to keep* is a statistic with enormous capacity to memorise, and it bought 24.5 percentage points of fiction. **Same bug, two sizes, and you cannot tell in advance which size you have.**

Which is why the rule is structural rather than judgemental: everything that learns from data goes inside the `Pipeline`. Then you never have to decide.

**"Can leakage ever make your score go *down*?"**

**Nobody fully agrees on this one, and it is worth telling the student that.**

The textbook answer is no: leakage means extra information, and extra information about the answer pushes the score up. That is right almost all of the time and it is why "score jumped, be suspicious" is a good rule.

The honest answer is that contrived cases exist. A leaky column can be *differently* leaky in the training rows than in the validation rows and confuse the model. A leaky column can crowd out an honest one and cost you more than it gives — Week 5's `dist_x_weather` was a mild version of exactly that shape.

The practical position: **if you find a leak that made things worse, you almost certainly have a second bug as well.** Do not spend the afternoon on the theory; go and look for the other bug. And do not pretend to the student that the boundary is crisp, because it is not.

**"Our delivery table doesn't have dates. Does temporal leakage matter to us?"**

Not for this table, and it is worth being straight about that. `make_data.py` uses the same rule for row 1 and row 2000, so there is no drift and a random split is genuinely honest.

But almost everything you will ever be handed at work *does* have a timestamp, and the world *does* drift — prices, fashions, opening hours, what people order, what counts as "late". The habit to install now is a question you ask of every new table: **do these rows have a time in them, and will I be deploying forwards?** If both answers are yes, cut by time.

**"What is `cross_val_score`? It's in the noise file."**

One sentence: it splits the rows into five piles, trains five times, and gives you five scores instead of one — because a single score on 40 rows is not worth much. That is genuinely all you need today.

**Week 11 is entirely about it**, including the part that matters: five scores let you say how much your one number wobbles, which is the tool you have been missing every time you have squinted at a difference of 0.0018. Do not go further today; a half-explained fold is worse than an honest "next month".

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| Somebody blurts out "it's the support-call column" in minute two | The name is a giveaway and bright students read column lists fast. | Have this planned. Say warmly: *"Right. Now prove it four different ways, and don't tell anyone else."* Give them a blank investigation sheet as a prosecution brief. **Do not let the room hear it** — eleven other people still have ten minutes of real work to do. |
| You help during the twelve minutes | Watching a student flounder is genuinely uncomfortable and you will want to nudge. | **Sit on your hands.** The discovery has to be theirs; a leak found for you is a fact, a leak found by you is a habit. One neutral prompt maximum, and only after four minutes of nothing. |
| The class decides the lesson is "don't use bad columns" | It is the easiest available summary and it is nearly useless. | Push back with the hospital ward column: it was a real column, correctly recorded, joined correctly. **The lesson is about timing, not badness.** Make them say the word "when". |
| Nobody believes the noise result | It is genuinely unbelievable. Disbelief is the correct first reaction. | **Feed it.** Open the file together and read the two lines that make the data: `rng.normal` for X, `rng.integers` for y, drawn separately, never compared. Then have somebody change the seed and watch 76.5% become some other equally impossible number. Belief has to be earned here. |
| The preprocessing flavour lands as "unimportant" because −0.0000 | You showed them a version that cost nothing. Reasonable inference. | **This is why the noise experiment comes after it and not before.** Do them in that order, and say the link out loud: *"same bug, two sizes."* If you are short of time, cut the delivery-table version and keep the noise one. |
| It becomes a lecture about how ML is untrustworthy | Three leaks in a row is genuinely dispiriting, and cynicism is a comfortable place to stop. | Finish on the fix, always. All three have a repair, and two of the three are *structural* — put it in the `Pipeline` and it cannot happen. **The subject is not untrustworthy. Sloppy pipelines are.** |
| Time runs out and the noise experiment is skipped | The Crime Scene is compelling and expands to fill any space. | The noise experiment is objective 3 and it is the most memorable ninety seconds of Term 1. **Cut the four audits down to two** (crosstab and the ablation) and protect it. If you truly have four minutes left, run it and skip the wrap. |
| A student's `mystery.py` prints a different score | `make_data.py` edited, `drop_duplicates()` missing, or `random_state` not 42. | Check in that order. **Do not let them investigate a different number** — every audit value in this file is tied to 0.9762. |

---

## 🧭 Differentiation

This section adjusts the lesson for a student who is struggling, flying, or not engaging.

### If the student is struggling

**Cut, in this order:** the temporal flavour (keep the two numbers 0.8139 and 0.5249 as a story, drop the script); then the missing-indicator ablation (keep the imputation, drop the indicator); then the four audits shrink to two — the crosstab and the with/without comparison.

**The version that skips the investigation.** Make them the prosecutor rather than the detective. Tell them the answer immediately and give them this ladder:

> 1. "Print the crosstab of `customer_called_support` against `late`. Read me the bottom row." → 12 and 540
> 2. "How many orders had a call?" → 12 + 540 = **552**
> 3. "What fraction of those were late?" → 540 ÷ 552 = **0.9783**
> 4. "Fit the model without that column. What's the AUC?" → **0.7752**
> 5. "And with it?" → **0.9762**
> 6. "Subtract." → **+0.2011**
> 7. "At the moment the order is placed, has the customer rung up yet?" → **No.**

**Those seven steps are objectives 2 and 4 in twelve minutes**, they require inventing nothing, and step 7 is the whole year's lesson.

**The version of the maths that skips the counting.** The median of 1,140 numbers is unpleasant to think about. Do it on five instead, on paper:

```text
five drivers:   4   12   29   30   55        median = 29  (the middle one)
four drivers:        12   29   30   55     median = (29 + 30) / 2 = 29.5
```

*"Now imagine 1,140 instead of four. Same idea: line them up, take the middle. When there are two middles, split the difference."* That is all the arithmetic they need.

**The copy-this-exactly scaffold.** Give the leak report as a fill-in-the-blanks form, because the *writing* is the marked part and a blank page is the obstacle:

```text
THE LEAK I FOUND:  ______________________________

which flavour:  target  /  temporal  /  preprocessing   (circle one)

the fake score:     0.______
the honest score:   0.______
the difference:     0.______  -  0.______  =  ____________

how I spotted it: _______________________________________

at the moment I need the prediction, does this value exist?   YES / NO
```

Three of those, filled in, is objective 4.

### If the student is flying

None of these needs syntax from a later week.

1. **Variation-harder 1 — invent a leak that passes all four audits.** The best exercise in the week. `driver_shift_overtime_minutes = 25 × late + noise` looks like an ordinary operational number, gets past a casual glance, and dies instantly to the timing question.
2. **Variation-harder 2 — how many noise columns do you need?** Run the noise experiment at 50, 200, 500 and 2,000 columns and plot the fake score. **The shape of that curve is the whole idea of overfitting-by-selection**, discovered rather than told.
3. **Variation-harder 3 — hunt for a temporal leak in the delivery table using `order_id` as a clock.** The finding is *no gap*, and explaining why is better than finding one.
4. **Variation-harder 4 — re-run the indicator ablation at three different splits.** −0.0029 is smaller than the wobble of a 400-row measurement, and a student who says so out loud has arrived at Week 11 five weeks early. Write it on a card and pin it up.
5. **Audit the whole table properly.** Correlate all five numeric columns with `late`, sort by size, and write one sentence per column saying when its value appears. That sentence set **is** the model card's data-provenance section from Week 3, finally filled in for real.
6. **The honest question:** *"`support_calls.py` did a correct join of a real table. Nobody made a mistake. So whose job was it to catch this?"* There is no clean answer, and that is the point — write theirs down and keep it for Week 34's model card.

### If the student won't engage today

**Close the laptop. One sheet of paper.**

Write these five column names on it and nothing else:

```text
distance_km
weather
prep_minutes
refund_issued
customer_called_support
```

Then one instruction, repeated for each row:

> **"A customer has just clicked ORDER. Right now, this second. Is there a value in this box — yes or no?"**

Work down the list. Yes, yes, yes, no, no.

Then: *"The last two are the ones that would make your model look brilliant. Why?"*

**That is objective 2 delivered in eight minutes with a pencil**, and it is the half of the week that Weeks 7, 34 and 36 all sit on. The four audits can wait a day; the picture of two empty boxes at the bottom of the list cannot be un-seen.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the three flavours and their tells, spoken (60 seconds)**

> "Name the three flavours of leakage, and for each one give me the question you would ask to catch it."

*Good answer:* "**Target** — a column that only exists because the answer happened; ask *is it filled in yet?* **Temporal** — shuffling rows so you train on the future; ask *do the rows have a date?* **Preprocessing** — a statistic worked out before the split; ask *was it fitted before the cut?*"

**What to catch:** three names with no tells. The names are worth little. Push: *"how would you actually notice it?"*

**Check 2 — the imputer's number, spoken (45 seconds)**

> "The median of all 2,000 rows is 29.0. The median of the 1,200 training rows is 29.5. Which one goes into the blanks, and what exactly is wrong with the other?"

*Good answer:* "29.5. The 29.0 was partly worked out from the validation and test rows, so a number that touched the rows I'm marked on would end up written into my training data."

**Full marks needs the *reason*, not just the choice.** "29.5 because it's the train one" is a level-2 answer; push: *"and what's wrong with 29.0?"*

**Check 3 — the noise result, written, two sentences (90 seconds)**

> "A table of 200 rows and 2,000 columns of pure random noise, with a coin-flip label. A model scored 76.5%. **Write me two sentences: how, and what one line fixes it.**"

*Good answer:* "The twenty columns were chosen by looking at all 200 labels, so out of 2,000 columns some lined up with the coin flip by luck and the model was handed a cheat sheet for the exact rows it was tested on. Moving the selection inside the `Pipeline` fixes it, because then it only ever sees the training rows and the score falls to 0.520."

**What to catch:** "the model overfitted." That is not it — the model was innocent. Push: *"the model never saw 2,000 columns. Who chose the twenty?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks a higher score is always better. Cannot say what a blank gets filled with. Reads "leakage" as "somebody cheated". |
| **2 — Emerging** | Names imputation and uses `SimpleImputer` when shown. Recognises that 0.9762 is suspicious but cannot say which column or why. Names one flavour of leakage. |
| **3 — Secure** | Fills blanks with the **training** median and can say why 29.0 is wrong. Names all three flavours with their tells. Finds the poisoned column and proves it with at least one number. Reports the fake and honest scores side by side. **This is the target.** |
| **4 — Strong** | Runs the four audits unprompted on any suspiciously good score. Explains the noise result in terms of 2,000 chances to get lucky, and names the one-line fix. Treats the missing indicator as a hypothesis and deletes it over −0.0029. |
| **5 — Exceptional** | Asks *"when does this value appear?"* before running any audit at all. Notices that the preprocessing leak on the delivery table cost −0.0000 and argues that this makes it **more** dangerous, not less. Points out that −0.0029 is smaller than the wobble of a 400-row measurement and names cross-validation as the thing that would settle it. Can explain that the fix for two of the three flavours is structural — put it in the `Pipeline` and the bug becomes unwriteable. |

---

## 📤 Homework to Assign

This section says what to assign at the end of class and how to introduce it.

**Say this:**

> "About an hour, and the part I'm marking is **Build It** at the back of the workbook. Everything else in the workbook is practice that leads up to it — do it first if you want the numbers to come easily.
>
> **Build It, the imputation.** Fill in the 106 blanks properly, with a median learned from the training rows only, and print `statistics_` to prove which number it learned. Write down the number you were *not* allowed. Then add the missing indicator, ablate it exactly the way you learned last week, and write the delta to four decimal places. **If it loses, delete it and write down the number** — a new tool does not get an exemption.
>
> **Build It, the three repairs — this is the marked one.** One row per flavour. Each row needs: the flavour's name, one sentence on what the bug was, **the fake number and the honest number side by side**, and the subtraction written out. Target, temporal, preprocessing. Three rows, six numbers, three subtractions.
>
> **Build It, the noise experiment.** Run `noise_leak.py` and paste the whole output — both halves, all ten fold scores. Then run it a second time with the leaky half commented out, to prove to yourself that the honest half stands on its own. Then the two paragraphs in your own words: **how can a table with nothing in it score 76.5%**, and **which of the three flavours would be hardest to spot at a real job, and why?** And two entries in the Bug Log, one loud and one silent.
>
> That last question has no single right answer and I will mark you on the reason, not the choice."

**Workbook sections:** in class — **Predict the Output** (P1–P4, in pen, before running anything) and, if time allows, **Practice Set A, A1** (match the words) · at home — **Build It** (marked), then the rest of the workbook over the week: **Warm-Up**, **Do the Maths by Hand**, **Practice Set A and B**, **Fix the Broken Program**, **Puzzle of the Week**, **Think Deeper**, **Draw It**, **Self-Check**. The Crime Scene is done in class on plain paper and is not in the workbook. *(The whole workbook is more than an hour of work; the hour below is the marked Build It only, and the other sections are for the student to work through before Week 7, checking against the workbook's own Answers section.)*

**Expected time (Build It):** 15 min on the imputation and the indicator ablation · 20 min on the three repairs and their six numbers · 15 min running the noise experiment and reading it · 10 min writing the two paragraphs. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** four things. **One — are there two numbers on every row of the three-repairs table?** A repair with only the honest number is not a repair, it is a claim. The fake number is the evidence that there was something to fix. **Two — is the subtraction written out?** Same rule as Week 5: the number is the deliverable, not the decision. **Three — does the noise paragraph blame the *selection* rather than the *model*?** "The model overfitted" is the commonest wrong answer and it misses the whole point; the model never saw 2,000 columns. **Four — the hardest-to-spot answer.** A student who picks **preprocessing** and argues that a leak worth −0.0000 can never be found by measurement has produced the best answer in the class. A student who picks **temporal** and argues that it needs no bad column at all, just a shuffle, is equally right. A student who picks **target** because "it's the biggest" has missed the question — the loud one is the easy one.

---

## 🔑 Answer Key

Organised in the **same order as the student workbook** (`workbook/week-06.md`), using its own section names and item labels (W1, M1, P1, A1, B1 …), with every question restated so you can mark from this page alone. Every workbook section has an entry. The values are the ones in the workbook's own *Answers* section; the numeric ones were re-run or recomputed while this key was being aligned. The complete teacher scripts (`mystery.py`, `fill_blanks.py`, `leak_hunt.py`, `deploy.py`, `temporal.py`, `silent.py`, `noise_leak.py`) are at the end of the key, under **🕵️ The Crime Scene** and **📁 The teacher scripts**. **All code below was run; all output is real.**

> **📌 The workbook has no numbered pages.** Earlier drafts of this guide called its sections "Page 6.1 … 6.6". Those labels never existed in the workbook. Use the section names below. The workbook also has **no blank investigation sheet** for the Crime Scene — the student records their checks on plain paper (see **🕵️ The Crime Scene**, below).

### ✅ Warm-Up (five from last week)

| # | Question | Answer |
|---|---|---|
| **W1** | Name the four shapes of invented column, with a one-word example of each. | **FLAG** (`is_rush`) · **BIN** (`hour_band`) · **RATIO** (`min_per_km`) · **INTERACTION** (`dist_x_weather`). |
| **W2** | `pd.cut(..., bins=[10, 14, 17, 20, 23], ...)` on hours that start at 10. No error. What went wrong, how many rows? | `pd.cut` reads `(10, 14]` as "bigger than 10, up to and including 14", and **hour 10 is not bigger than 10.** All **47** orders placed at 10:00 fell out of the bins and became `NaN` — no error, no warning. Fix: start the first edge below the minimum (`bins=[9, ...]`) and `print(int(s.isna().sum()))` every time. |
| **W3** | Round `+0.0018` and `−0.0014` to two decimal places. Why a disaster? | `0.00` and `0.00`. One means keep and one means delete; rounding erases the answer, and the sign matters more than the size. |
| **W4** | A new feature's delta is **exactly** `0.0000`. What does that almost always mean, and what is the one line? | The model **never saw the feature** — it was created but not added to the `ColumnTransformer`'s list, so it was silently dropped. The line: `print(pipe.named_steps["prep"].get_feature_names_out())`, then count. |
| **W5** | `d["prep_minutes"] / (d["distance_km"] + 0.5)`: what is `+ 0.5` for, and what error without it? | A **guard** against dividing by zero. Without it a `distance_km` of 0 gives `inf`, then `ValueError: Input X contains infinity or a value too large for dtype('float64')`. Pick a constant and write down that you picked it. |

**Marking tip:** W3 and W4 are the two that catch people. A student who writes "0.00 and 0.00, so they're the same" has got the numbers right and missed the point — ask them which one you would keep.

### 🔢 Do the Maths by Hand

No new maths this week: the median, three subtractions, two divisions, and the fold-score averages. Calculator only.

**M1 — the median, by counting to the middle.** Eight pupils, sleep hours `5.0, 6.0, blank, 7.0, 9.0 | blank, 12.0, 10.0` (first five rows are train, last three validation).

```text
values present in train, lined up:  5.0  6.0  7.0  9.0

that is 4 numbers. 4 is even, so there is no single middle one.
the two middles are number 2 and number 3, which are 6.0 and 7.0
( 6.0 + 7.0 ) ÷ 2 = 6.5

values present in the whole table:  5.0  6.0  7.0  9.0  10.0  12.0
that is 6 numbers, so the two middles are number 3 and number 4, which are 7.0 and 9.0
( 7.0 + 9.0 ) ÷ 2 = 8.0
```

- **M1(a)** Which two pupils caused the difference, and which pile? **Gus (12.0) and Hana (10.0)**, both in the **validation** pile. Using 8.0 would write into Cleo's row a number partly computed from two pupils you are about to be marked on.
- **M1(b)** Cleo → **6.5**, Fay → **6.5**. Same number because **the imputer does not re-learn on new rows — it applies the number it already remembers.** `.fit` on train, `.transform` on everything.
- **M1(c)** Train mean: 27.0 ÷ 4 = **6.75**. Whole-table mean: 49.0 ÷ 6 = **8.1667**. Both moved; the medians by 1.5, the means by 1.4167. Put a 100 in instead of the 12 and the mean runs away while the median barely moves — that is why the median.
- **M1(d)** 1140 is even, so the two middles are number **570** and number **571**; (29 + 30) ÷ 2 = **29.5**. Whole table: (29 + 29) ÷ 2 = **29.0**. The two candidates are **29.0 and 29.5**; the student is allowed **29.5**.

**M2 — three subtractions.**

```text
target        : 0.9762 − 0.7752 = 0.2010
temporal      : 0.8139 − 0.5249 = 0.2890
preprocessing : 0.765  − 0.520  = 0.245
```

- **M2(a)** 0.2011 ÷ 0.0091 = **22.1**. Twenty-two times as much from one column, in four seconds, as two honest features bought in a whole lesson. That ratio is the alarm.
- **M2(b)** The rule: **round the printed result, never the inputs.** 0.976231884 − 0.775163997 = 0.2010678…, which rounds to **0.2011**; subtracting the two rounded numbers gives 0.2010. It changes no verdict, but say so when it happens instead of quietly writing a different number from the machine's. *(This is why the key gives the target gap as 0.2010 in the hand subtraction and 0.2011 everywhere the machine printed it. Accept either from the student if they say why.)*
- **M2(c)** All three make the score go **up**, which is why leakage is nearly the only kind of bug that gets applauded. A bug that makes your number worse gets fixed on Tuesday; one that makes it better gets a presentation and six months in production being wrong.

**M3 — two divisions that convict a column.**

```text
12 + 540 = 552 orders had a support call
540 ÷ 552 = 0.9783

1413 + 35 + 12 + 540 = 2000
1413 + 540 = 1953
1953 ÷ 2000 = 0.9765
```

- **M3(a)** Hospital: 11 + 187 = **198** biopsies booked; 187 ÷ 198 = **0.9444** malignant.
- **M3(b)** The two big numbers sit on **one diagonal** and the other two are tiny — what "this column is nearly a photocopy of the answer" looks like.
- **M3(c)** 0.942 ÷ 0.345 = **2.73** · 3.482 ÷ 0.804 = **4.33**. **The crosstab needs the fewest keystrokes** — one line, four seconds, no model.

**M4 — five fold scores, twice.**

```text
WRONG: 0.875 + 0.750 + 0.800 + 0.725 + 0.675 = 3.825    3.825 ÷ 5 = 0.765
RIGHT: 0.425 + 0.475 + 0.600 + 0.425 + 0.675 = 2.600    2.600 ÷ 5 = 0.520

0.765 − 0.520 = 0.245 of pure invention
```

- **M4(a)** An honest method should give about **0.500**; it gave **0.520**, twenty thousandths off on 40 rows a fold — the size of wobble to expect. 0.520 is what "nothing there" looks like.
- **M4(b)** **0.675** appears in both. It means **nothing** — a coincidence between two lists of five noisy numbers.
- **M4(c)** Drift: week 0 → 2.0 − 0 = **2.0** · week 15 → 2.0 − 1.95 = **0.05** · week 29 → 2.0 − 3.77 = **−1.77**. It has **reversed**: a model trained on a shuffled mixture of all thirty weeks has no way to express a knob whose true value changed sign.

**Marking tip:** the commonest slip is M1 Step 2 — counting the whole table as 8 numbers (blanks included) and taking the 4th and 5th. There are 6 present values. A second slip is answering M1(b) "Fay gets 8.0" — that is the leak itself.

### 🔎 Predict the Output

**P1 — asking before it has looked.** The first snippet (`print(imp.statistics_)` on an unfitted imputer) **stops with an error**:

```text
Traceback (most recent call last):
  File "/private/tmp/w56/p6/p1a.py", line 7, in <module>
    print(imp.statistics_)
AttributeError: 'SimpleImputer' object has no attribute 'statistics_'
```

With `imp.fit(col)` added:

```text
statistics_: [6.5]
filled     : [5.  6.  6.5 7.  9. ]
if mean    : [6.75]
```

Present values 5, 6, 7, 9 → median **6.5**, mean **6.75**. **The trailing underscore means "I learnt this from data."** The `AttributeError` is the library saying "I have not looked at any data yet"; nothing in scikit-learn ending in `_` exists before `.fit`, so an `AttributeError` on such a name has exactly one cause.

**P2 — shapes.** Blanks: `sleep` 1, `screen` 1, total **2**.

```text
in shape     : (5, 2)
plain out    : (5, 2)
flagged out  : (5, 4)
[[5.  2.  0.  0. ]
 [6.  4.  0.  1. ]
 [6.5 4.  1.  0. ]
 [7.  4.  0.  0. ]
 [9.  8.  0.  0. ]]
```

It is `(5, 4)` and not `(5, 3)` because there is **one indicator column per column that had a blank**, and both columns had one. The **indicators go on the end**, not beside the column they describe: columns 0–1 are the filled `sleep` and `screen`, column 2 flags `sleep` blanks (the 1 in row 3), column 3 flags `screen` blanks (the 1 in row 2). On the delivery table this is why 20 becomes 21 rather than the indicator appearing beside `driver_experience_months`.

**P3 — the same column, two piles.**

```text
values present in train : [5.0, 6.0, 7.0, 9.0]
values present in all   : [5.0, 6.0, 7.0, 9.0, 10.0, 12.0]
train-only median : 6.5
whole-table median: 8.0
train-only mean   : 6.75
whole-table mean  : 8.1667
```

*Is silent dropping right here?* For **computing a statistic, yes** — you cannot include a blank in a median. It would be wrong to report "the median of 8 pupils" when you used 6. **Dropping blanks to compute a number is fine; dropping blanks to make a problem go away is not; the difference is whether you print the count.** Gaps: medians **1.5**, means **1.4167**. The mean is more affected by Gus's 12 in principle (every value drags it), but here both move by almost the same amount because 10 and 12 both sit above the old middle. With a 100 instead of the 12 the mean would jump to 22.8 and the median would not move.

**P4 — read a crosstab you have never seen.**

```text
late   : 0  0  1  1  0  1  0  1  1  0
called : 0  0  0  1  1  1  0  1  1  0
              ^     ^
            index 2  index 4
```

```text
late    0  1
called      
0       4  1
1       1  4
orders with a call : 5
of those, late     : 4
agreement count    : 8 out of 10
the column on its own, AUC: 0.8
```

`called[2] = 0` created the **`called 0 / late 1`** cell (a late order nobody rang about); `called[4] = 1` created the **`called 1 / late 0`** cell (somebody rang about an order that was not late). Those two cells are all that stops the column being a perfect photocopy; on the real table they hold 35 and 12 out of 2,000.

**The scoreboard ("___ / 18")** is self-reported and not marked; there is no answer to give. **Marking tip for P1:** a student who ticks "it prints a number" has not yet absorbed that `_` means fitted. Do not tell them — have them run it.

### ✍️ Practice Set A — Read It

**A1 — match the word to the thing.** imputation → **ii** · missing indicator → **v** · data leakage → **vii** · target leakage → **vi** · temporal leakage → **iii** · preprocessing leakage → **i** · NaN → **iv**.

| Word | Letter | Description |
|---|---|---|
| **imputation** | ii | Filling a blank with a number worked out from the rows you are allowed to look at. |
| **missing indicator** | v | An extra 0/1 column recording that the original value was blank. |
| **data leakage** | vii | Information that will not be available at the moment you have to predict. |
| **target leakage** | vi | A column that only gets filled in because the outcome already happened. |
| **temporal leakage** | iii | Shuffling rows across a time boundary, so the model trains on the future. |
| **preprocessing leakage** | i | A statistic worked out over all the data before the split. |
| **NaN** | iv | How a computer writes "not a number". |

**A2 — trace the shapes.**

```text
df.shape                                        (2000, 11)
X.shape                                         (2000, 9)
X_tr.shape                                      (1200, 9)
X_tr[NUM].shape                                 (1200, 5)
imp.statistics_.shape                           (5,)
imp.transform(X_tr[NUM]).shape                  (1200, 5)
with add_indicator=True, statistics_.shape      (5,)
with add_indicator=True, transform shape        (1200, 6)
len(get_feature_names_out()), plain             20
len(get_feature_names_out()), add_indicator     21
len(get_feature_names_out()), + leaky column    21
```

`df` has 11 columns because the support-call column was joined on; `X` has 9 because `late` and `order_id` came off.

- **A2(a)** The two 21s: with `add_indicator=True` the 21st column is **`num__missingindicator_driver_experience_months`** (a 0/1 blank flag — honest); with the leaky column the 21st is **`num__customer_called_support`** (a sixth real numeric column — a disaster). Same count, so print the **names**, not just the number.
- **A2(b)** `statistics_` holds **one fill-in number per column**; the indicator is a *record of where the filling happened*, not a fill-in number. Five columns still means five statistics, while the output gains a sixth column.

**A3 — spot the bug.**

| # | What happens | The fix |
|---|---|---|
| a | `ValueError: Input X contains NaN.` plus a long paragraph; the model cannot multiply by a blank | `SimpleImputer(strategy="median")` in the numeric branch. The fix is written inside the message |
| b | `ValueError: Cannot use median strategy with non-numeric data: could not convert string to float: 'clear'` | send word columns down the categorical branch, or `strategy="most_frequent"` |
| c | `AttributeError: 'ColumnTransformer' object has no attribute 'statistics_'` — you asked the box, not the thing inside it | `...named_transformers_["num"].named_steps["impute"].statistics_` |
| d | `KeyError: 'pre'` | use the exact stage name; `print(pipe.named_steps.keys())` lists them |
| e | **No error.** Blanks filled with the **whole-table** median, 29.0, partly computed from the 800 rows you are marked on. Worth **−0.0000** here | let the imputer inside the `Pipeline` do it, fitted on train rows only → **29.5** |
| f | **No error.** The 20 columns were chosen while looking at every label, so cross-validation is scoring a cheat sheet. **0.765 on pure noise** | put the `SelectKBest` **inside** the `Pipeline` → **0.520** |

- **A3(g)** **e** and **f** give no traceback. **e is more dangerous**: f is worth +0.245 and anyone who checks against "what should an honest method score?" finds it; e is worth −0.0000, so no measurement will reveal it — only reading *where* the statistic was computed.
- **A3(h)** Flavour: **preprocessing leakage.** e: **0.7751 against 0.7752** (gap −0.0000, from `silent.py`). f: **0.765 against 0.520** (gap +0.245). Same bug, one thousand times the consequence; the strength depends on how many chances the leak had to find a lucky coincidence.

**A4 — match the code to the output.** i → **S** (106) · ii → **R** (`[ 2.91  4.   14.   18.   29.5 ]`) · iii → **T** (21) · iv → **P** (0.9556) · v → **Q** (`[1413   35   12  540]`).

- **A4(a)** One column reaching 0.9556 on its own is not a feature — it is a label with a different name on it. If any honest column moved that closely with the thing you are predicting, nobody would need a model. Compare `distance_km` alone: 0.6800.
- **A4(b)** The one this week cares about is **29.5** (the fifth, `driver_experience_months`). The number you are **not** allowed is **29.0**, the whole-table median, because 800 of the rows behind it are rows you are about to be marked on.

**A5 — four audit reports, four verdicts.**

| Report | Verdict | Why |
|---|---|---|
| 1 — `customer_called_support` | **TARGET LEAKAGE — drop it.** | Fastest convincing audit: **the crosstab** — one line, no model, 540 of 552 is unmistakable. The 0.942 is just as damning; accept either if the student says *why*. |
| 2 — `distance_km` | **KEEP — it is honest.** | A big gap is not evidence of leakage. The address is known the moment the order is placed, and it is nowhere near a photocopy: over 5 km is late 0.5521 of the time, so **45% of long trips arrive on time**. A leaked column does not leave 45% of its rows disagreeing. |
| 3 — `order_hour` | **KEEP — the Week 5 lesson in audit clothing.** | `0.064` and `0.5358` both look for a steady one-way trend; the effect of the hour is a **hump** (0.374 at 18:00, 0.196 at 22:00). Neither sees a hump; the two-group rates do (0.3682 against 0.2424). A low correlation can mean you are measuring the wrong way. |
| 4 — `biopsy_booked` | **TARGET LEAKAGE — drop it.** | A biopsy gets booked *because* somebody read the scan and was worried. |

- **A5(a)** The question: **"At the moment I need the prediction, does this value exist?"** `distance_km` → **yes** (the address exists the instant somebody clicks ORDER). `biopsy_booked` → **no** (only after a radiologist has read the scan). It needs no data, no code and no maths.
- **A5(b)** Keeping one number can hide a catastrophe: AUC fell 0.15 and looked survivable; recall fell from 87.5% to 6.25% (60 women with malignant tumours told they were fine). A leaky column can look respectable in one metric while ruinous in another — which is why next week is about four numbers instead of one.

**A6 — fill in the three flavours** (Figure W6.1, the blank diagram).

```text
TARGET         tell: "is it filled in yet?"            0.9762 / 0.7752  gap 0.2011
TEMPORAL       tell: "do the rows have a date?"        0.8139 / 0.5249  gap 0.2890
PREPROCESSING  tell: "was it fitted before the cut?"   0.765  / 0.520   gap 0.245

the question no computer can answer:
  "At the moment I need the prediction, does this value exist?"
  For customer_called_support the answer is No.
```

- **A6(a)** Self-marked ("which boxes did you get wrong?"); check against the block above.
- **A6(b)** **Temporal and preprocessing** are bugs in **how you cut**; target is a bug **in a column**. The two cutting bugs have a *structural* fix (everything that learns from data goes inside the `Pipeline`; split by time when rows have a time); the column bug needs a human to ask a question about the world.

### ✍️ Practice Set B — Write It

**B1 — count the holes, find the two numbers.** Expected output:

```text
blanks: whole 106  train 60  val 25  test 21
they add up to: 106
median of the WHOLE table: 29.0
median of the TRAIN rows : 29.5
the one I am allowed     : 29.5
```

60 + 25 + 21 = 106 ✅. Roughly 60% of the blanks landed in the pile that is 60% of the rows, as a random split should do. Done looks like two different medians on screen at once. (`fill_blanks.py` under **📁 The teacher scripts** prints all of this.)

**B2 — walk the address into a fitted pipeline.**

```python
prep = pipe.named_steps["prep"]
print("stage names   :", list(pipe.named_steps.keys()))
print("branch names  :", list(prep.named_transformers_.keys()))
imp = prep.named_transformers_["num"].named_steps["impute"]
print("statistics_   :", imp.statistics_)
print("the one I care about:", imp.statistics_[4])
```

```text
stage names   : ['prep', 'model']
branch names  : ['num', 'cat']
statistics_   : [ 2.91  4.   14.   18.   29.5 ]
the one I care about: 29.5
```

**B2(a)** `prep` is a **`ColumnTransformer`** — the box that *contains* the imputer — so it has no `statistics_` of its own. Read the address aloud: the pipeline's `prep` stage, its `num` branch, that branch's `impute` step, and what it learned.

**B3 — the fastest audit there is.**

```text
late                        0    1
customer_called_support           
0                        1413   35
1                          12  540
calls: 552  of those late: 540
540 / 552 = 0.9783
the column agrees with the answer 1953 times out of 2000
```

**B3(a)** A crosstab of a continuous column against the answer would have hundreds of rows. Cut it into two or three groups and compare the rates: `df.groupby(df["distance_km"] > 5)["late"].agg(["size", "mean"])` gives 0.2167 against 0.5521. Same audit, one extra step.

**B4 — ablate the missing indicator.**

```text
add_indicator=False cols= 20  accuracy=0.7600  roc_auc=0.7752
add_indicator=True  cols= 21  accuracy=0.7550  roc_auc=0.7723
0.7723 - 0.7752 = -0.0029
the new column is called: num__missingindicator_driver_experience_months
its weight: -0.1609
```

Worse, so it goes: a new tool does not get an exemption. Honest caveat: −0.0029 on 400 validation rows is inside the wobble of a 400-row measurement, so retest with cross-validation in Week 11. **B4(a)** 60 × 0.15 = **9** late deliveries. The whole "enormous" 0.1447 gap is made of nine events, and `make_data.py` chose the blanks with a coin flip, so there is no rookie-driver story to find — the gap is noise wearing a costume.

**B5 — `noise_shrink.py`.** A whole program the student writes (about 20 lines):

```python
"""noise_shrink.py - fewer columns, fewer lucky coincidences."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

cv = StratifiedKFold(5, shuffle=True, random_state=0)
print("columns   fake    honest   invented")
for ncols in [2000, 500, 200, 50]:
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, ncols))
    y = rng.integers(0, 2, size=200)
    X20 = SelectKBest(f_classif, k=20).fit_transform(X, y)
    wrong = cross_val_score(LogisticRegression(max_iter=1000), X20, y, cv=cv).mean()
    pipe = Pipeline([("select", SelectKBest(f_classif, k=20)),
                     ("model", LogisticRegression(max_iter=1000))])
    right = cross_val_score(pipe, X, y, cv=cv).mean()
    print(f"{ncols:>7d}   {wrong:.3f}   {right:.3f}    {wrong - right:+.3f}")
```

```text
columns   fake    honest   invented
   2000   0.765   0.520    +0.245
    500   0.735   0.505    +0.230
    200   0.700   0.540    +0.160
     50   0.635   0.615    +0.020
```

Runtime about 1 second. Check: the `StratifiedKFold` is created **once outside the loop**, and `invented` shrinks all the way down.

- **B5(a)** More columns means more **chances** for a column of noise to line up with the coin flip by luck, so the best 20 of 2,000 look far more convincing than the best 20 of 50 — none of which has anything to do with the data meaning anything.
- **B5(b)** **No, the bug is not gone at 50 columns** — the code is exactly as wrong. The honest score there is **0.615**, so the invented part is only **+0.020**. The bug has not changed; its consequence has. A leak's danger depends on how many chances it had. *(Honest caveat from the workbook: this is one seed, and the 0.615 is itself a lucky draw on noise whose true answer is 0.5. Averaged over 20 seeds the 50-column leak is worth about +0.085 and the 2,000-column leak about +0.28. The slide from large to small is real; the exact size of the last row is not.)*

### 🐞 Fix the Broken Program

`broken06.py` has **three** bugs: one runtime, one attribute, one silent logic.

> **Line numbers.** Counting the listing exactly as printed in the workbook (docstring = line 1), the three offending lines are **28** (`("num", StandardScaler(), NUM)`), **37** (the `statistics_` print) and **14** (the `NUM = [...]` list, with `"customer_called_support"` on line 15). The workbook's *Answers* now say the same (28 and 37). The printed tracebacks say line 34 and line 40 because they were pasted from the file the author ran, which had a few extra lines; **accept 28/34 and 37/40**, and mark the *kind* of bug and the fix, not the line number.

**Bug 1 — a runtime bug.** No imputer in the numeric branch, and `driver_experience_months` has holes. Error: `ValueError: Input X contains NaN.` The seven words that are the fix: **"by using an imputer transformer in a pipeline"**. The error message contains the answer; most people stop at the red word. Fix:

```python
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), NUM),
```

Blanks in the column: **106**; in the training pile: **60**.

**Bug 2 — an attribute bug.** `AttributeError: 'ColumnTransformer' object has no attribute 'statistics_'`. The first four words name the type: `prep` is a **`ColumnTransformer`**, the box that *contains* the imputer. Fix:

```python
pipe.named_steps["prep"].named_transformers_["num"].named_steps["impute"].statistics_
```

**Bug 3 — a silent logic bug:** `customer_called_support` is in `NUM`. It runs, prints a lovely score, and is **target leakage.** The three tells in the three-line output:

1. **`columns going into the model: 21`** — should be 20 (five numeric plus fifteen one-hot). There is a sixth numeric column in there.
2. **`roc_auc : 0.9762`** — nineteen points above last week's best honest 0.7843, when last week's two surviving honest features bought +0.0091 between them. When one change moves the score by more than about 0.05, stop and audit.
3. **`statistics_` has SIX numbers, the sixth is `0.`** — one per numeric column, so six numbers means six numeric columns; a median of 0 says most rows have no call, which is what a column that only fills in after a failure looks like.

The question that settles it: *"At the moment I need the prediction — the moment a customer clicks ORDER — has that customer already rung up to complain about a delivery that has not arrived yet?"* **No.** The fix: remove **`"customer_called_support"`** from **`NUM`**. After all three fixes:

```text
columns going into the model: 20
validation roc_auc : 0.7752
the fill-in number it learned: [ 2.91  4.   14.   18.   29.5 ]
```

**Ranking, easiest to hardest: bug 1, bug 2, bug 3.** Bug 1 stopped the program and the fix was inside the message ("an error that shouts is a good day"). Bug 2 also stopped the program and named the wrong object type. Bug 3 printed three tidy lines and a wonderful score; nothing would ever have stopped the student handing it in, and shipped, it would have caught **2 late deliveries out of 115**. **The sentence:** a bug that makes your number worse gets fixed on Tuesday afternoon because somebody is annoyed; a bug that makes it better gets a presentation and six months in production being wrong — which is why good news gets audited harder than bad news.

### 🧩 Puzzle of the Week — The Timing Detective

| # | Column | Exists at prediction time? | When does it appear? |
|---|---|---|---|
| 1 | `driver_experience_months` | **yes** | a fact about the driver, already true before the order exists |
| 2 | `customer_called_support` | **no** | about an hour later, and **only if the delivery was late** |
| 3 | `ward_moved_to` | **no** | after a doctor has already decided the patient needs intensive care |
| 4 | `mock_exam_mark` | **yes**, if the mock happened before you predict | in the spring term, weeks before the summer exam |
| 5 | `summer_revision_hours` | **arguable** | during the revision period, which may be after you wanted the prediction |
| 6 | `total_repaid_so_far` | **no**, as written | grows for the whole life of the loan, including after the default |

- **Part 1(a)** **Number 5.** You would need to be told **when you are making the prediction**. In April, after revision is over, it is a legal column; in September, when you want to offer help early, it does not exist yet — and how much revision they will do is partly a consequence of what you are predicting. The question is not "is this column allowed?" but "is it allowed at the moment I predict?"
- **Part 1(b)** It is **temporal**: the value is measured at a point in time that may be **after** your prediction moment. Nothing about the column is dishonest; the bug is in **when** you read it.
- **Part 1(c)** **`total_repaid_so_far_as_at_the_moment_of_prediction`** — a snapshot frozen at the decision date, stored with the date you read it, not a running total that keeps updating. Any column that keeps changing after the outcome is a leak in waiting.

**Part 2 — work backwards.**

```text
target        : 0.9762 − 0.2011 = 0.7751     (the printed honest number is 0.7752)
temporal      : 0.8139 − 0.2890 = 0.5249
preprocessing : 0.520  + 0.245  = 0.765
```

The target one comes out 0.7751 rather than 0.7752 — the rounding lesson again; working backwards from rounded numbers recovers the answer to about ±0.0001. Accept 0.7751 or 0.7752 if the student says why.

- **Part 2(a)** **The temporal one, 0.5249.** 0.5000 is what a model that knows nothing scores — a coin flip. The time split is reporting a model no better than guessing, because the rule it learned from the past has reversed.
- **Part 2(b)** The threshold is about **0.05**; +0.06 is above it, so **audit**. Real features arrive in units of 0.005. Four audits and one question take under ten minutes; being wrong in production for eight months does not.
- **Part 2(c)** **There is no clean answer, and that is the point.** Somebody joined two correct tables, another built a model on the result, a third approved it. Every step was reasonable, so there is no individual to blame and therefore none who will spontaneously fix it — which is why you need audits that run whether or not anyone suspects anything, and a model card naming every column and when it is filled in. **Leakage is a design accident, not dishonesty.** (The student keeps this answer for Week 34.)

### 🤔 Think Deeper

Marked on the reasoning, not a single right answer. A full-marks answer contains these moves.

**T1 — the −0.0000 bug against the +0.245 bug.**

- **The −0.0000 one is more dangerous**, which is counter-intuitive. The +0.245 bug announces itself: anybody who asks "what should an honest method score on a table with nothing in it?" finds it in a minute. The −0.0000 bug cannot be found by **any** measurement; you find it only by reading where the statistic was computed.
- **It will not stay worth −0.0000.** The same line was worth +0.245 on 2,000 columns, and `noise_shrink.py` shows the consequence sliding from +0.245 to +0.020 on that seed (about +0.28 to +0.09 averaged over 20 seeds) purely on how many chances the leak had. A loaded gun pointing at the floor.
- **The fix is structural, not moral.** "Be more careful" fails under deadlines, new colleagues and 200-line files. Putting everything that learns from data inside the `Pipeline` means the bug cannot be expressed.
- **Is carefulness ever right?** Yes — for "does this value exist at prediction time?", because no structure can answer it; that question is about the world. Structure for the bugs a computer can see, discipline for the ones only a person can.

**T2 — nobody made a mistake, so whose job?**

- The mistake was that **nobody's job description included the question** "when does this column get its value?"; a question that belongs to nobody gets asked by nobody.
- **A checklist** anyone can run: (1) print every column name and write when each gets filled in — before, at, or after the prediction; (2) any "after" column is deleted, no argument; (3) for every 0/1 column print the crosstab against the answer — if two cells hold nearly everything, stop; (4) if the score is more than about 0.05 better than the previous honest model, stop and run step 1 again; (5) do the rows have a date? Then also split by time and report both numbers.
- **Can you make people follow "good news gets audited harder"?** Not by asking — good news is when people are least motivated to look. It has to be **built into the tools**: the script that reports the score also prints the four audits and the column timing table every time, with no flag to switch it off.

### 🛠️ Build It — Three Repairs, Six Numbers, One Noise Table

**This is the marked section** — the three things handed in are the imputation with `statistics_` printed, the three repairs with fake and honest numbers side by side, and the two paragraphs. Step-checklist answers:

| Step | What a correct entry has |
|---|---|
| 1 | First `order_id` is **100955** (`make_data.py` unchanged). |
| 2 | Blank counts **whole 106 · train 60 · val 25 · test 21**, adding to **106**. |
| 3 | `statistics_` printed with **29.5** in it; the number not allowed is **29.0**. |
| 4 | Indicator ablated; delta written with its sign: **−0.0029**. |
| 5–7 | Repairs 1–3: two numbers, the subtraction, and the one-sentence tell (below). |
| 8 | `noise_leak.py` run once, all ten fold scores pasted, both totals (3.825, 2.600) and both means (0.765, 0.520). |
| 9 | `noise_leak.py` run again with the leaky half removed, with two sentences on what was expected. |
| 10 | Two Bug Log entries, one loud and one silent (below). |

**The imputation** (a worked model answer):

```text
blanks: whole 106  train 60  val 25  test 21      add up to 106 ✅

statistics_ : [ 2.91  4.   14.   18.   29.5 ]

the number I am allowed  : 29.5   (the median of the 1,140 training values present)
the number I am NOT       : 29.0   (the median of all 1,894 values present)
where the difference came from: the 800 validation-and-test rows, which I am
   about to be marked on and am therefore not allowed to learn anything from.
```

**The arithmetic the student must be able to reproduce:**

- 60 + 25 + 21 = **106.** Every blank is accounted for.
- **The median, by hand.** 1,200 train rows − 60 blanks = **1,140 with a value.** 1,140 ÷ 2 = 570, so the two middles are number 570 (**29**) and number 571 (**30**). (29 + 30) ÷ 2 = **29.5.**
- **The whole-table median.** 2,000 − 106 = **1,894 with a value.** Both middles are 29, so the median is **29.0** — the number the imputer is *not* allowed to learn.
- **The indicator ablation.** 0.7723 − 0.7752 = **−0.0029.** Delete it.
- **Column count.** 5 numeric + 15 one-hot = 20 without the indicator; 21 with it.

| | cols | accuracy | roc_auc |
|---|---|---|---|
| `add_indicator=False` | 20 | 0.7600 | 0.7752 |
| `add_indicator=True` | 21 | 0.7550 | 0.7723 |

```text
the subtraction: 0.7723 − 0.7752 = −0.0029     verdict DELETE
```

*Why didn't it pay?* The lateness rates were 0.15 (blank) against 0.2947 (present), a gap of 0.1447, but with 60 blank training rows the 0.15 is made of **nine** late deliveries, and `make_data.py` chooses the blanks with a coin flip. The column's fitted weight (−0.1609) is the model dutifully learning from nine events.

**The deletion note that earns full marks:**

> **Feature:** the missing indicator on `driver_experience_months`.
> **What I thought it would do:** if the paperwork is worse for brand-new drivers, then "this field is blank" is itself a clue about who the driver was.
> **AUC without it:** 0.7752 · **AUC with it:** 0.7723 · **the delta:** 0.7723 − 0.7752 = **−0.0029**
> **Why I am deleting it:** it made the model worse. The blanks in this table were chosen at random by `make_data.py` — you can read the line that does it — so there is no story about rookie drivers hiding in there. The 60 blank training rows do look less late (0.15 against 0.2947), but that is nine late deliveries out of sixty and it is noise.
> **Honest caveat:** −0.0029 on 400 validation rows is inside the wobble. Retest with cross-validation in Week 11.

**The three repairs:**

| Flavour | What the bug was | Fake score | Honest score | The subtraction |
|---|---|---|---|---|
| **target** | `customer_called_support` is only filled in after the delivery has already arrived late — a bug in a **column** | **0.9762** | **0.7752** | 0.9762 − 0.7752 = **0.2011** |
| **temporal** | 3,000 rows across 30 weeks, split at random, so next month's rows were in the training pile — a bug in **how you cut** | **0.8139** | **0.5249** | 0.8139 − 0.5249 = **0.2890** |
| **preprocessing** | 20 of 2,000 columns chosen while looking at every label — a bug in **how you cut** | **0.765** | **0.520** | 0.765 − 0.520 = **0.245** |

The tells, as one-sentence answers: **target** — *"Is it filled in yet?"* A customer rings up after the pizza is late; at the moment of ORDER the column is empty for every row. **Timing question, one sentence:** at the moment somebody clicks ORDER, no customer has rung up. **temporal** — *"Do the rows have a date, and will I deploy forward in time?"* If both, split by time; the random split reports a working model, the time split reports roughly a coin flip, and **the time split is the one that matches how the thing will be used.** **preprocessing** — *"Was the statistic fitted before the cut?"* A median, a mean, a ranking, a choice of columns; you cannot detect it from the score, only from where the statistic was computed. (`leak_hunt.py`, `temporal.py`, `silent.py` and `deploy.py` under **📁 The teacher scripts** produce every number in this table.)

**The noise experiment, run 1:**

```text
WRONG five scores: 0.875  0.750  0.800  0.725  0.675
       total 3.825  ÷ 5 = 0.765

RIGHT five scores: 0.425  0.475  0.600  0.425  0.675
       total 2.600  ÷ 5 = 0.520

the invented score: 0.765 − 0.520 = 0.245
98 + 102 = 200 ✅  the label really is a coin flip
```

**Run 2 — the leaky half removed.** Expected and seen: only the honest half prints, with **exactly the same five scores and the same 0.520**, because removing the leaky *report* does not change the honest number — the two halves never interacted.

```text
RIGHT - the choosing is inside the Pipeline
  five scores: [0.425 0.475 0.6   0.425 0.675]
  their total: 2.600   divided by 5: 0.520   <- the truth
```

If the honest number *does* change, something else is wrong — most likely the generator was re-seeded in between, or the `cross_val_score` call was moved. A correct measurement should not care what else is in the file.

**Paragraph 1 — "How can a table with nothing in it score 76.5%?" The answer that earns full marks:**

> There are 2,000 columns, so there are 2,000 chances for a column of noise to line up with the coin flip by luck. Some of them do, very well — that is what 2,000 tries buys you, and it has nothing to do with the data meaning anything. When the best 20 are chosen *while looking at all 200 labels*, the model is handed the columns that happen to match the exact rows it is about to be marked on. **The model did nothing wrong; the choosing did.** Moving the selection inside the `Pipeline` means it only ever sees the training rows of each fold, and the score falls to 0.520 — which is what "nothing there" looks like.

**What does not earn full marks:** "the model overfitted." The model never saw 2,000 columns. Push the student to name **who chose the twenty**.

**Paragraph 2 — "Which flavour would be hardest to spot at a real job?" Three defensible answers:**

| Choice | The argument | Verdict |
|---|---|---|
| **preprocessing** | It produces **no error and no measurable score change** — ours cost −0.0000. You cannot find by measurement a bug that does not move the measurement. You can only find it by reading where the statistic was computed. | **The strongest answer.** |
| **temporal** | It needs no bad column at all. Every column is honest, every value is true, and the bug is a single call to `train_test_split` that looks exactly like the right thing to do. | **Equally strong.** |
| **target** | Real tables have hundreds of columns, most of them undocumented, and nobody knows when each one gets filled in. | Defensible **only** with the "hundreds of undocumented columns" reasoning. "Because it's the biggest" misses the question — the loud one is the easy one. |

A model student paragraph: *"Preprocessing, because it is the only one you cannot find by measuring. On my delivery table it was worth −0.0000 — the wrong version scored 0.7751 and the right one 0.7752 — so no experiment I could run would ever reveal it. Target leakage announces itself with a suspiciously good score, and temporal leakage shows up the moment you also report a time split. Preprocessing leakage shows up as nothing at all, until the day somebody runs the same code on a table with 2,000 columns and it is suddenly worth 0.245."*

**Optional extension — the temporal hunt on the student's own table.** Real numbers:

```text
RANDOM split AUC : 0.7462
TIME   split AUC : 0.8018      (cut at order_id 101499, 1500 train / 500 test)
the gap          : −0.0556
```

The finding is that **nothing bad happens — the time split is actually higher.** That is strong evidence of no drift (a drifting world would make the time split *worse*). `make_data.py` uses the same rule for row 1 and row 2000, so there is nothing to leak, and the ±0.05 is the noise of two different 500-row test piles. A negative result explained is worth more than a positive one guessed. *(Not re-run while aligning this key; the figures are the workbook's.)*

**The Bug Log — two entries, one loud and one silent:**

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| `ValueError: Input X contains NaN.` plus a long paragraph | the model cannot multiply by a blank | no imputer in the numeric branch | `SimpleImputer(strategy="median")`. The fix was inside the message |
| `roc_auc : 0.9762`, `21` columns, and a `statistics_` array with **six** numbers. **No error at all** | a column that will not exist at prediction time is in my feature list | `customer_called_support` in `NUM` | drop the column. **Run the four audits on good news, not just on bad news** |

### 🎨 Draw It

- **Panel 1 — the prediction moment comes FIRST.** Somebody clicks ORDER and you need the prediction that instant. `customer_called_support` gets its value **about an hour later**, and **only if the delivery was late** and the customer is annoyed enough to ring — two separate later events, which the model is trained on as though they were the click. The real gap is about an hour.
- **Panel 2 — the two recalls are 0.9217 in the lab and 0.0174 in production.** The counts: **115** late orders in the 400 validation rows, **2** flagged. (`deploy.py` prints these.)
- **Redrawn for `driver_experience_months`,** the two moments collapse: the value's moment moves to **before** the prediction, because the driver's tenure is already true when the order arrives. A good drawing makes the arrow for `driver_experience_months` come in from the *left* of the prediction, and the arrow for `customer_called_support` from the *right*. That is the whole difference between an honest column and a leaked one, and it is a fact about time, not statistics.

### 📊 Self-Check

The student rates themselves; there is no answer key, but every row should be 😀 by the end of Build It. Four rows deserve an honest conversation:

- *"explain why 29.5 is allowed and 29.0 is not"* — full marks names the 800 rows: "29.0 was partly computed from the validation and test rows, which I am about to be marked on." "Because you should only use training data" is the rule without the reason.
- *"ablate it like any other column"* — did they actually write `0.7723 − 0.7752 = −0.0029` down, or just remember that it "didn't help"? The number is the deliverable.
- *"ask the one question no computer can answer, unprompted"* — the word that matters is **unprompted.** If they only ask it when a workbook tells them to, mark it 🙂 and put it on a sticky note.
- *"say why a leak worth −0.0000 is more dangerous"* — full answer: "because no measurement can ever reveal it, and its size depends on the data rather than the code." The row about the list `2, 4, 6, 8, 100` (median 6, mean 24) tests the median-not-mean reasoning.

### 🕵️ The Crime Scene (class activity — no workbook page)

The Crime Scene is the 20-minute class activity. **It has no page in the workbook**; students record their checks on plain paper. Nothing from it is handed in or marked on a form, so there is no workbook item to cross-reference.

There is no single right route. **Marked on the number of checks recorded, including the ones that led nowhere.** A full sheet has at least three checks with their results, and a verdict naming the column and the flavour. Routes that earn full marks:

| Check | What it gives | Verdict it supports |
|---|---|---|
| Read the 21 column names | spots `customer_called_support` | suspicion only — must be confirmed with a number |
| `df[NUM + ["late"]].corr()["late"]` | 0.942 against 0.345 next | audit 1 ✅ |
| `pd.crosstab(suspect, df["late"])` | 12 / 540 on the bottom row | audit 2 ✅ |
| fit with and without the column | 0.9762 against 0.7752 | the ablation ✅ |
| look at the coefficients | 3.482 against 0.804 | audit 4 ✅ |
| ask when the value appears | after the delivery is late | **the verdict** ✅ |

**Dead ends that should be written down and earn credit:** blaming `max_iter`; blaming the scaler; suspecting `order_hour`; checking for duplicate rows (there are none after `drop_duplicates()`); checking whether the split was stratified (it was). **A sheet with three dead ends and one hit is a better sheet than one with a lucky guess.**

**The complete `mystery.py`**, as handed out. Save it beside `make_data.py` and `support_calls.py`.

```python
"""mystery.py - somebody's model. It scores this. Find out why."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries
from support_calls import attach_support_calls

RS = 42
NUM = ["distance_km", "items", "prep_minutes", "order_hour",
       "driver_experience_months", "customer_called_support"]
CAT = ["restaurant", "day_of_week", "weather"]

df = attach_support_calls(
    make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True))
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

pre = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
pipe = Pipeline([("prep", pre),
                 ("model", LogisticRegression(max_iter=2000, random_state=RS))])
pipe.fit(X_tr, y_tr)
prob = pipe.predict_proba(X_va)[:, 1]

print("columns going into the model:",
      len(pipe.named_steps["prep"].get_feature_names_out()))
print(f"validation accuracy : {accuracy_score(y_va, (prob >= .5).astype(int)):.4f}")
print(f"validation roc_auc  : {roc_auc_score(y_va, prob):.4f}")
print("Week 5's best honest score was 0.7843.  Congratulations?")
```

```text
columns going into the model: 21
validation accuracy : 0.9700
validation roc_auc  : 0.9762
Week 5's best honest score was 0.7843.  Congratulations?
```

**Runtime: about 0.9 seconds.**

### 📁 The teacher scripts

The complete files you create before class (see the Prep Checklist), with their real output. `mystery.py` is above, under the Crime Scene. The numbers in the workbook sections above all come from these files.

#### `fill_blanks.py` — the imputation (workbook B1, B2, B4 and Build It)

**The complete, runnable file.** Save as `fill_blanks.py` beside `make_data.py`.

```python
"""fill_blanks.py - filling in the 106 holes, and marking where they were."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

RS = 42
NUM = ["distance_km", "items", "prep_minutes", "order_hour",
       "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

print("--- where the holes are ---")
print("blanks in the whole table :", int(X["driver_experience_months"].isna().sum()))
print("blanks in the 1200 train  :", int(X_tr["driver_experience_months"].isna().sum()))
print("blanks in the  400 val    :", int(X_va["driver_experience_months"].isna().sum()))
print("blanks in the  400 test   :", int(X_te["driver_experience_months"].isna().sum()))

print("\n--- two candidate fill-in numbers ---")
print("median of the WHOLE table :", X["driver_experience_months"].median())
print("median of the TRAIN rows  :", X_tr["driver_experience_months"].median())

print("\n--- what the imputer actually learned ---")
imp = SimpleImputer(strategy="median")
imp.fit(X_tr[NUM])
print("statistics_ :", imp.statistics_)

print("\n--- is being blank itself a signal? ---")
blank = X_tr["driver_experience_months"].isna()
print("late rate, rows with a value :", round(y_tr[~blank].mean(), 4))
print("late rate, rows that are blank:", round(y_tr[blank].mean(), 4))


def build(indicator):
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median",
                                                   add_indicator=indicator)),
                          ("scale", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
    return Pipeline([("prep", pre),
                     ("model", LogisticRegression(max_iter=2000, random_state=RS))])


print("\n--- with the indicator column, and without ---")
for indicator in (False, True):
    pipe = build(indicator).fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_va)[:, 1]
    n_cols = len(pipe.named_steps["prep"].get_feature_names_out())
    print(f"add_indicator={str(indicator):<5s} cols={n_cols:>3d}"
          f"  accuracy={accuracy_score(y_va, (prob >= .5).astype(int)):.4f}"
          f"  roc_auc={roc_auc_score(y_va, prob):.4f}")

pipe = build(True).fit(X_tr, y_tr)
names = pipe.named_steps["prep"].get_feature_names_out()
print("\nthe new column is called:", names[5])
co = pd.Series(pipe.named_steps["model"].coef_[0], index=names)
print("its weight:", round(co[names[5]], 4))
```

```bash
python3 fill_blanks.py
```

Real output:

```text
--- where the holes are ---
blanks in the whole table : 106
blanks in the 1200 train  : 60
blanks in the  400 val    : 25
blanks in the  400 test   : 21

--- two candidate fill-in numbers ---
median of the WHOLE table : 29.0
median of the TRAIN rows  : 29.5

--- what the imputer actually learned ---
statistics_ : [ 2.91  4.   14.   18.   29.5 ]

--- is being blank itself a signal? ---
late rate, rows with a value : 0.2947
late rate, rows that are blank: 0.15

--- with the indicator column, and without ---
add_indicator=False cols= 20  accuracy=0.7600  roc_auc=0.7752
add_indicator=True  cols= 21  accuracy=0.7550  roc_auc=0.7723

the new column is called: num__missingindicator_driver_experience_months
its weight: -0.1609
```

**Runtime: about 0.8 seconds.**

#### `leak_hunt.py`, `deploy.py`, `temporal.py`, `silent.py` — the three repairs (workbook Build It, A3, A5, Fix the Broken Program, Draw It)

**The complete `leak_hunt.py`.** Save it beside `make_data.py` and `support_calls.py`.

```python
"""leak_hunt.py - a suspiciously perfect model, and the four audits that catch it."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries
from support_calls import attach_support_calls

RS = 42
CAT = ["restaurant", "day_of_week", "weather"]
GOOD = ["distance_km", "items", "prep_minutes", "order_hour",
        "driver_experience_months"]
POISONED = GOOD + ["customer_called_support"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
df = attach_support_calls(df)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)


def fit_and_score(num_cols, label):
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
    pipe = Pipeline([("prep", pre),
                     ("model", LogisticRegression(max_iter=2000, random_state=RS))])
    pipe.fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_va)[:, 1]
    acc = accuracy_score(y_va, (prob >= .5).astype(int))
    auc = roc_auc_score(y_va, prob)
    print(f"{label:<32s} accuracy={acc:.4f}  roc_auc={auc:.4f}")
    return pipe, auc


print("--- the two scores ---")
bad_pipe, bad_auc = fit_and_score(POISONED, "with customer_called_support")
good_pipe, good_auc = fit_and_score(GOOD, "without it")
print(f"{'the jump one column bought':<32s} {bad_auc - good_auc:+.4f}")

print("\n--- audit 1: how strongly does each number move with late? ---")
corr = df[POISONED + ["late"]].corr()["late"].drop("late")
print(corr.reindex(corr.abs().sort_values(ascending=False).index).round(3).to_string())

print("\n--- audit 2: the suspect, counted against the answer ---")
print(pd.crosstab(df["customer_called_support"], df["late"]).to_string())

print("\n--- audit 3: how well does each column do ON ITS OWN? ---")
for col in ["customer_called_support", "distance_km", "prep_minutes"]:
    print(f"  {col:<26s} AUC {roc_auc_score(y_va, X_va[col]):.4f}")

print("\n--- audit 4: which knob is the model actually turning? ---")
names = bad_pipe.named_steps["prep"].get_feature_names_out()
co = pd.Series(bad_pipe.named_steps["model"].coef_[0], index=names)
print(co.reindex(co.abs().sort_values(ascending=False).index).head(4).round(3).to_string())

print("\n--- the question no statistic can answer ---")
print("At the moment the order is PLACED, has the customer already rung up")
print("to complain about a delivery that has not arrived yet?   No.")
print("VERDICT: target leakage. Drop the column.")
```

Real output:

```text
--- the two scores ---
with customer_called_support     accuracy=0.9700  roc_auc=0.9762
without it                       accuracy=0.7600  roc_auc=0.7752
the jump one column bought       +0.2011

--- audit 1: how strongly does each number move with late? ---
customer_called_support     0.942
distance_km                 0.345
driver_experience_months   -0.123
items                       0.106
prep_minutes                0.066
order_hour                  0.064

--- audit 2: the suspect, counted against the answer ---
late                        0    1
customer_called_support           
0                        1413   35
1                          12  540

--- audit 3: how well does each column do ON ITS OWN? ---
  customer_called_support    AUC 0.9556
  distance_km                AUC 0.6800
  prep_minutes               AUC 0.5739

--- audit 4: which knob is the model actually turning? ---
num__customer_called_support    3.482
num__distance_km                0.804
cat__restaurant_GreenLeaf      -0.744
cat__weather_clear             -0.679

--- the question no statistic can answer ---
At the moment the order is PLACED, has the customer already rung up
to complain about a delivery that has not arrived yet?   No.
VERDICT: target leakage. Drop the column.
```

**Runtime: about 0.9 seconds.**

**The audit arithmetic, spelled out:**

- 0.942 ÷ 0.345 = **2.73 times** the best honest column.
- Crosstab bottom row: 12 + 540 = **552 calls**, and 540 ÷ 552 = **0.9783** of them were late.
- One column alone: **0.9556** against `distance_km`'s **0.6800**.
- Weights: 3.482 ÷ 0.804 = **4.33 times** the next one.
- The jump: 0.9762 − 0.7752 = **+0.2011**, against Week 5's two surviving honest features earning +0.0091 between them — **twenty-two times as much from one column.**

**And the demonstration that settles the argument.** `deploy.py`:

```python
"""deploy.py - what the leaky model actually does on the day it is switched on."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries
from support_calls import attach_support_calls

RS = 42
CAT = ["restaurant", "day_of_week", "weather"]
NUM = ["distance_km", "items", "prep_minutes", "order_hour",
       "driver_experience_months", "customer_called_support"]

df = attach_support_calls(
    make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True))
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_tmp, X_te, y_tmp, y_te = train_test_split(
    X, y, test_size=.20, random_state=RS, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(
    X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)

pre = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
pipe = Pipeline([("prep", pre),
                 ("model", LogisticRegression(max_iter=2000, random_state=RS))])
pipe.fit(X_tr, y_tr)

print("--- in the lab, where the column is filled in ---")
prob = pipe.predict_proba(X_va)[:, 1]
pred = (prob >= .5).astype(int)
print(f"accuracy {accuracy_score(y_va, pred):.4f}   recall {recall_score(y_va, pred):.4f}"
      f"   roc_auc {roc_auc_score(y_va, prob):.4f}")

print("\n--- in production, where nobody has rung up yet, so it is always 0 ---")
real = X_va.copy()
real["customer_called_support"] = 0
prob2 = pipe.predict_proba(real)[:, 1]
pred2 = (prob2 >= .5).astype(int)
print(f"accuracy {accuracy_score(y_va, pred2):.4f}   recall {recall_score(y_va, pred2):.4f}"
      f"   roc_auc {roc_auc_score(y_va, prob2):.4f}")
print("late orders in these 400 rows:", int(y_va.sum()),
      "   late orders it flagged:", int(((pred2 == 1) & (y_va == 1)).sum()))
```

```text
--- in the lab, where the column is filled in ---
accuracy 0.9700   recall 0.9217   roc_auc 0.9762

--- in production, where nobody has rung up yet, so it is always 0 ---
accuracy 0.7175   recall 0.0174   roc_auc 0.7924
late orders in these 400 rows: 115    late orders it flagged: 2
```

**Runtime: about 0.9 seconds.** `recall` here means, for today, "the fraction of the late ones it caught" — it gets a proper name and a proper lesson next week.

**The complete `temporal.py`.**

```python
"""temporal.py - the same data, two ways to split, two different truths."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
n = 3000
week = np.repeat(np.arange(30), n // 30)      # 30 weeks, 100 orders a week
x1 = rng.normal(size=n)
x2 = rng.normal(size=n)
w1 = 2.0 - 0.13 * week                        # the world drifts: x1 matters less
y = ((w1 * x1 + 0.8 * x2 + rng.normal(0, .5, n)) > 0).astype(int)
df = pd.DataFrame({"week": week, "x1": x1, "x2": x2, "y": y})
F = ["x1", "x2"]

print("how much x1 matters, week by week:")
print("  week  0 :", round(2.0 - 0.13 * 0, 3))
print("  week 15 :", round(2.0 - 0.13 * 15, 3))
print("  week 29 :", round(2.0 - 0.13 * 29, 3))


def model():
    return Pipeline([("scale", StandardScaler()),
                     ("model", LogisticRegression(max_iter=2000))])


X_tr, X_te, y_tr, y_te = train_test_split(
    df[F], df["y"], test_size=.25, random_state=0, stratify=df["y"])
m = model().fit(X_tr, y_tr)
random_auc = roc_auc_score(y_te, m.predict_proba(X_te)[:, 1])

tr = df[df["week"] < 22]
te = df[df["week"] >= 22]
m2 = model().fit(tr[F], tr["y"])
time_auc = roc_auc_score(te["y"], m2.predict_proba(te[F])[:, 1])

print()
print("rows in the random split :", len(X_tr), "train,", len(X_te), "test")
print("rows in the time split   :", len(tr), "train,", len(te), "test")
print()
print(f"RANDOM split AUC  {random_auc:.4f}   <- what you would report")
print(f"TIME   split AUC  {time_auc:.4f}   <- what production will give you")
print(f"the gap           {random_auc - time_auc:.4f}")
```

Real output:

```text
how much x1 matters, week by week:
  week  0 : 2.0
  week 15 : 0.05
  week 29 : -1.77

rows in the random split : 2250 train, 750 test
rows in the time split   : 2200 train, 800 test

RANDOM split AUC  0.8139   <- what you would report
TIME   split AUC  0.5249   <- what production will give you
the gap           0.2890
```

**Runtime: about 0.8 seconds.**

**The drift arithmetic, checkable on paper:** 2.0 − 0.13 × 0 = **2.0** · 2.0 − 0.13 × 15 = 2.0 − 1.95 = **0.05** · 2.0 − 0.13 × 29 = 2.0 − 3.77 = **−1.77.** By week 29 the feature has not merely stopped mattering, it has **reversed**, and a model trained on the shuffled mixture has no way to express that.

**And the silent one, `silent.py`:**

```python
"""silent.py - the leak that produces no error and almost no evidence."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

RS = 42
NUM = ["distance_km", "items", "prep_minutes", "order_hour",
       "driver_experience_months"]
CAT = ["restaurant", "day_of_week", "weather"]
raw = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)


def score(df, label):
    y = df["late"]
    X = df.drop(columns=["late", "order_id"])
    X_tmp, X_te, y_tmp, y_te = train_test_split(
        X, y, test_size=.20, random_state=RS, stratify=y)
    X_tr, X_va, y_tr, y_va = train_test_split(
        X_tmp, y_tmp, test_size=.25, random_state=RS, stratify=y_tmp)
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT)])
    pipe = Pipeline([("prep", pre),
                     ("model", LogisticRegression(max_iter=2000, random_state=RS))])
    pipe.fit(X_tr, y_tr)
    auc = roc_auc_score(y_va, pipe.predict_proba(X_va)[:, 1])
    print(f"{label:<44s} roc_auc={auc:.4f}")
    return auc


# WRONG: fill the blanks with the median of the WHOLE table, before splitting
pre_filled = raw.copy()
whole_median = pre_filled["driver_experience_months"].median()
pre_filled["driver_experience_months"] = \
    pre_filled["driver_experience_months"].fillna(whole_median)
print("median used by the wrong version :", whole_median)
bad = score(pre_filled, "WRONG - filled in before splitting")

# RIGHT: the imputer lives inside the Pipeline and is fitted on train rows only
good = score(raw, "RIGHT - imputer inside the Pipeline")
print(f"{'difference':<44s} {bad - good:+.4f}")
```

```text
median used by the wrong version : 29.0
WRONG - filled in before splitting           roc_auc=0.7751
RIGHT - imputer inside the Pipeline          roc_auc=0.7752
difference                                   -0.0000
```

**Runtime: about 1.3 seconds.** Note what this proves: **the leak is real and the score cannot see it.** Which is the argument for the structural fix rather than a watchful eye.
#### `noise_leak.py` — the noise experiment (workbook Build It, M4, B5)

**The complete supplied file.** Save as `noise_leak.py`.

```python
"""noise_leak.py - three-quarters right, on data with nothing in it.

SUPPLIED FILE. You will change exactly one thing in it.
"""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

rng = np.random.default_rng(0)
X = rng.normal(size=(200, 2000))     # 200 rows, 2000 columns of pure noise
y = rng.integers(0, 2, size=200)     # a coin flip. Nothing to do with X at all.

print("X shape:", X.shape)
print("y:", int(y.sum()), "ones and", int((y == 0).sum()), "zeros")
print("There is no relationship between X and y. There cannot be one.")

cv = StratifiedKFold(5, shuffle=True, random_state=0)

# WRONG: choose the 20 best-looking columns using ALL 200 rows and ALL 200 labels
X20 = SelectKBest(f_classif, k=20).fit_transform(X, y)
wrong = cross_val_score(LogisticRegression(max_iter=1000), X20, y, cv=cv)

# RIGHT: the choosing lives inside the Pipeline, so it re-runs on training rows only
pipe = Pipeline([("select", SelectKBest(f_classif, k=20)),
                 ("model", LogisticRegression(max_iter=1000))])
right = cross_val_score(pipe, X, y, cv=cv)

print()
print("WRONG - 20 columns chosen while looking at every label")
print("  five scores:", np.round(wrong, 3))
print(f"  their total: {wrong.sum():.3f}   divided by 5: {wrong.mean():.3f}")
print()
print("RIGHT - the choosing is inside the Pipeline")
print("  five scores:", np.round(right, 3))
print(f"  their total: {right.sum():.3f}   divided by 5: {right.mean():.3f}   <- the truth")
```

Real output:

```text
X shape: (200, 2000)
y: 98 ones and 102 zeros
There is no relationship between X and y. There cannot be one.

WRONG - 20 columns chosen while looking at every label
  five scores: [0.875 0.75  0.8   0.725 0.675]
  their total: 3.825   divided by 5: 0.765

RIGHT - the choosing is inside the Pipeline
  five scores: [0.425 0.475 0.6   0.425 0.675]
  their total: 2.600   divided by 5: 0.520   <- the truth
```

**Runtime: about 0.8 seconds.**

### Every question posed in the lesson

- *"The hospital model was right about who needed intensive care. What was wrong with it?"* → It could only be right after the answer was already known.
- *"Name a column in our table that would be a leak."* → `refund_issued`, `actual_delivery_time`, `driver_arrived_at`, `customer_called_support`.
- *"Why is a bug that raises your score worse than one that lowers it?"* → Because nobody goes looking for it.
- *"106 blanks. How many land in the 1,200 train rows?"* → **60.** 60 + 25 + 21 = 106.
- *"1,140 values. What's the median?"* → 570th is 29, 571st is 30, so **(29 + 30) ÷ 2 = 29.5.**
- *"29.0 or 29.5 — which may I use?"* → **29.5.** 29.0 was partly computed from the 800 rows you are marked on.
- *"Subtract the indicator ablation."* → 0.7723 − 0.7752 = **−0.0029.** Delete it.
- *"0.8139 and 0.5249. Subtract."* → **0.2890**, produced by nothing but where you cut.
- *"Which of those two is the lie?"* → **0.8139.**
- *"Name the tell for each flavour."* → Is it filled in yet? · Do the rows have a date? · Was it fitted before the cut?
- *"What breaks if I fill the blanks before splitting?"* → **Nothing visible.** No error, and −0.0000 of AUC. Which is what makes it dangerous.
- *"Which column is the problem, out of the 21?"* → `customer_called_support`.
- *"Read me the bottom row of the crosstab."* → 12 and 540. 552 calls, 540 late, 540 ÷ 552 = 0.9783.
- *"At the moment the order is placed, has the customer rung up?"* → **No.** That question beats all four audits.
- *"There is nothing in that noise table. What should an honest method score?"* → **50%.** It gets 52.0%.
- *"So where did 76.5% come from?"* → 2,000 columns is 2,000 chances to match a coin flip by luck, and the best 20 were chosen while looking at every label.
- *"What one line fixes it?"* → Move the selection **inside** the `Pipeline`.

---

## 🔮 Next Week Preview

Next week is a **lab**, and after three heavy weeks that is deliberate: no new ideas, one new discipline, and a tournament. The student takes Week 3's pipeline — validation AUC **0.7541** on the split Week 7 uses — and tries to beat it using **only** feature changes. The model is frozen. Same `LogisticRegression`, same settings, no exceptions; a student who swaps in a decision tree has voided their table and will know why. The whole lesson lives on a big sheet of paper on the wall: **one change, one measurement, one row.** Any round with two changes in it gets struck out in red and re-run, and the first time you do that you should do it cheerfully and immediately, because it sets the rule for the rest of the year.

Eight rounds, and the results are not what anybody expects. `is_rush` earns +0.0045. `is_weekend` buys −0.0001, again. `min_per_km` — which *won* its place in Week 5 on a different split — **loses** by 0.0051 here, which is a lesson in itself about how much a 400-row measurement wobbles. And the best row in the whole table is round 7, which **removes** a real column out of the original file: dropping `order_hour` makes the model better by 0.0013, because `is_rush` already carries the useful part and the raw hour adds a straight-line story that is not true. **The winning model has fewer columns than the baseline.** Total honest gain for an afternoon's work: **+0.0058.** Say that number without flinching.

And then the second half, which is this week's lesson wearing a disguise. This week the poisoned column was handed to them with a suspicious name on it. Next week the poison is **inside a feature function**, which is far more realistic and far harder to see, because feature functions look like harmless arithmetic. Three lines at the top of a supplied file build a lookup of "how often are orders like this one late?" from all 2,000 rows — and 360 of the 820 groups contain exactly one order, so for those rows the feature *is* the label with a statistic's name on it. It reports **0.9240**. Remove it and you get 0.7535. Compute it honestly, from the training rows only, and it scores **0.6115** — worse than not having it at all. That third number is the one to dwell on, and this week's closing question is what kills it in one line: *at the moment I need the prediction, does this value exist?*

**Prep early:** three things. **Keep `make_data.py`, `support_calls.py` and every script from this week** — Week 7 imports the first and the contrast with the second is the whole point of its leak hunt. **Type `leaky_features.py` into the folder yourself before class and run it once**, because you want to have found that bug unhurried before you watch somebody else look for it. And **get a big sheet of paper and a red pen**: the ablation table goes on the wall, it stays there for the rest of Term 1, and the red pen is for striking out any round that changed two things at once.

---

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Week 7 ➡](week-07.md) · [Student Guide](../student-guide/week-06.md) · [Workbook](../workbook/week-06.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
