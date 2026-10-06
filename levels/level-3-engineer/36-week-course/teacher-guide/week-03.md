# Week 3 — The Artifact Is the Deliverable

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Week 4 ➡](week-04.md) · [Student Guide](../student-guide/week-03.md) · [Workbook](../workbook/week-03.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — the first real model of the year, and it is not the point of the lesson |
| **Big idea** | What you hand over is not a score, it is a **file**: a fitted `Pipeline` on disk, plus a card saying what it is and where it breaks. |
| **New vocabulary** | pipeline · ColumnTransformer · artifact · joblib · model card · clean room test |
| **New maths** | **None.** One piece of counting, done on paper before the code runs: 5 + 5 + 7 + 3 = 20. |
| **New syntax** | `Pipeline(steps=[...])` · `ColumnTransformer([...])` · `joblib.dump(pipe, "m.joblib")` · `joblib.load("m.joblib")` |
| **Dataset** | The same numpy-generated pizza-delivery table, `make_data.py`, seed 0. **Do not edit that file.** Nothing downloads. |
| **Materials** | Two shoeboxes or two envelopes, one that fits inside the other · printed workbook pages 3.1–3.3 · the Bug Log · Week 2's baseline box, still on the wall · a printed copy of the seven model-card headings |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. `joblib` arrives with scikit-learn — nothing extra to install. No internet, ever. |
| **Prep time** | 30 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `train_pipeline.py` about **1 second** · `predict.py` about 0.7 seconds, most of which is importing scikit-learn. Nothing waits. |

> **⚠️ Watch out:** the model arrives today and it is **eight lines out of forty-five.** If the lesson becomes "we built a model", the lesson has failed. The thing they take away is a **5,002-byte file** and a page of writing. A student who leaves with an AUC and no artifact has done Level 2 again.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Assemble a `ColumnTransformer`** that applies different preparation to number columns and to word columns, **selected by name**, and say how many columns come out.
2. **Weld the preparation and the model into one `Pipeline` object**, and explain why that makes forgetting the preparation *structurally impossible* rather than merely unlikely.
3. **Save the fitted pipeline with `joblib` and reload it in a brand-new file that contains zero training code** — and prove that file is clean by counting.
4. **Write a model card under seven headings**: intended use, out-of-scope use, unit of prediction, training data, splits, metrics, known limitations.

Observable evidence: a run of `train_pipeline.py` printing `(1200, 8)` in and `(1200, 20)` out with validation AUC **0.7541**; a `delivery_pipeline.joblib` file of **5002 bytes** on disk; a `predict.py` that contains no `fit(` and no `make_data`, run from a cold start, printing **0.968 / 0.022 / 0.291**; and a `model_card.md` with seven headings filled in.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**There is no maths this week and no calculus.** There is one idea about software design, and it is the idea that separates people who write models from people who ship them. Read this section once — about twenty-five minutes, it is the longest of the term so far — and you will be able to teach it and defend it.

### 1. Why this week exists

Two weeks of writing, and today it pays. But look at what actually pays.

Here is the whole model, and it is three lines:

```python
model = LogisticRegression(max_iter=1000, random_state=0)
model.fit(prepared_training_rows, y_train)
prob = model.predict_proba(prepared_validation_rows)[:, 1]
```

Three lines, and the AUC comes out at **0.7541** against Week 2's baseline of **0.5000**. That is 0.2541 above the zero on the ruler, and it is a genuinely decent result for a first attempt.

**And now the awkward question: what do you hand to somebody?**

The score? A score is a claim. Nobody can use a claim. The code? Then they have to install the same libraries, get the same data, run the same script and hope. **The thing they need is the fitted model itself, as a file** — something that already contains the learned numbers, that loads in a fresh program on a different day, and that turns a raw order into a probability without any training happening.

> **Artifact** — the fitted thing, saved to disk as a file. Not the code that made it, and not the score it got. The file.

Everything in this week is arranged around that one word. And the reason it needs a whole lesson is that **the artifact has to contain the preparation too**, and getting that right is the difference between a system that works and a system that silently returns nonsense.

### 2. The problem: eight columns the model cannot read

Here is X, and here is why you cannot hand it straight to a model.

| Column | What is in it | Can a model add it up? |
|---|---|---|
| `distance_km` | 7.4 | yes |
| `items` | 5 | yes |
| `prep_minutes` | 22.0 | yes |
| `order_hour` | 19 | yes |
| `driver_experience_months` | 59.0, or **nothing at all** in 108 rows | not when it is nothing |
| `restaurant` | `"GreenLeaf"` | **no** |
| `day_of_week` | `"Thu"` | **no** |
| `weather` | `"rain"` | **no** |

Two separate problems, and they need two separate treatments:

- **The number columns have holes.** Week 1 counted them: 108 empty cells in `driver_experience_months`. A model cannot multiply by nothing. So each hole gets filled with the **median** of that column — the middle value — learned from the training rows.
- **The word columns are words.** A model does arithmetic. `"rain"` is not a number and cannot be made into one by voting on it. So each word column becomes **one new column per value that exists**, each holding a 0 or a 1.

And a third, quieter problem: **the number columns are on wildly different rulers.** `distance_km` runs from about 0.3 to 15; `driver_experience_months` runs 0 to 59. Left alone, the big-numbered column shouts. So all five get put on the same ruler.

Here is the honest bit, and say it to the class: **all four of those tools get taught properly later.** Filling holes is **Week 6**. Rulers are **Week 4**. Turning words into columns is **Week 4**. What logistic regression actually *does* is **Week 13**. This week they are four named parts you wire together — and wiring is the subject. You do not need to know how a fuse works to know it must be upstream of the socket.

### 3. `ColumnTransformer`: one switchboard, two routes

> **ColumnTransformer** — a switchboard. You give it a list of routes; each route is a name, a treatment, and the list of columns it applies to. It runs each route on its own columns and glues the results side by side.

![One switchboard, two routes, twenty columns out](../figures/fig-w03-1-columntransformer-two-routes.svg)
*Figure 3.1 — One switchboard, two routes, twenty columns out. 8 columns go in; the arithmetic on the right is the whole diagram.*

**Count the output columns on paper before you ever run this.** It is the one piece of arithmetic in the week and it is the thing that catches shape bugs for the next thirty-three weeks.

Route 1 — the five number columns. Fill the holes, put them on one ruler. Neither of those changes how many columns there are. **5 in, 5 out.**

Route 2 — the three word columns. Each becomes one column per value that exists in the training data:

- `restaurant` has **5** different values (Napoli, SliceHouse, CrustyBros, TandooriPizza, GreenLeaf) → 5 columns
- `day_of_week` has **7** → 7 columns
- `weather` has **3** (clear, rain, storm) → 3 columns
- **3 columns in, 5 + 7 + 3 = 15 columns out.**

Glue the routes together: **5 + 15 = 20.**

So: **8 columns in, 20 columns out.** Written the way you will write it all year: **(1200, 8) → (1200, 20).** The 1200 never changes — you are not adding or removing rows, only re-describing each one.

> **🔢 The arithmetic, slowly:** 5 numbers stay 5. Then 5 restaurants + 7 days + 3 weathers = 15. And 5 + 15 = **20**. If you print the shape and it says 20, your counting was right. If it says something else, **do not go on** — one of your three counts is wrong, and finding out now costs thirty seconds while finding out in Week 17 costs an afternoon.

And here is the sentence that makes `ColumnTransformer` worth its long name: **the columns are chosen by name, not by position.** You wrote `["distance_km", "items", ...]`. So a new order with its columns typed in a completely different order still works, and we prove it in class — the switchboard looks up names, and does not count from the left.

### 4. `Pipeline`: two objects you can drop, or one you cannot

This is the heart of the week. Slow all the way down.

You now have two things: a `prep` object that knows how to prepare a row, and a `model` object that knows how to score a prepared row. **Keeping them as two things is a trap**, and it is not a trap about being careless.

![Two objects you can drop, or one you cannot](../figures/fig-w03-2-pipeline-as-one-sealed-box.svg)
*Figure 3.2 — Two objects you can drop, or one you cannot. The right-hand picture is not more careful; it is a shape that cannot be got wrong.*

**Watch what happens with two objects.** Take one real order: GreenLeaf, 7.4 km, 5 items, 22 minutes of prep, 7 pm on a Thursday, raining, driver with 59 months' experience.

Prepared properly, the four numbers the model receives are:

| typed | 7.4 | 5.0 | 22.0 | 19.0 |
|---|---|---|---|---|
| **after preparation** | **1.793** | **0.811** | **2.008** | **0.662** |

And the model says **P(late) = 0.709.** Seventy percent. That is a sensible answer for a long, rainy, rush-hour delivery.

Now put the **raw** numbers into those four slots instead — change nothing else at all, not one other value — and the model says:

**P(late) = 1.000.**

![The same order, prepared and unprepared](../figures/fig-w03-5-forgotten-preparation.svg)
*Figure 3.3 — The same order, prepared and unprepared. 1.000 − 0.709 = 0.291 of pure damage, and not one warning was printed.*

**1.000. Absolute, total certainty.** And no error. No warning. No pink text. A number that a dashboard would print, that a dispatcher would believe, and that is wrong.

**Why it goes to 1.000, and this is worth being able to explain rather than assert:** the model learned its numbers on a world where `distance_km` sits around 0 and rarely leaves −2 to +5. You have just handed it 7.4 — not 7.4 kilometres, 7.4 *on the prepared scale*, which is off the end of anything it ever saw. And 22.0 for prep minutes, which is off the end of the end. The numbers are **4 to 30 times too big**, so the sum the model adds up is thrown far off the end of its scale — and because all four of these numbers carry a positive weight (further, more items, longer prep, later hour all push towards *late*), it is thrown towards 1.000. A number with a negative weight, such as driver experience, would be thrown the other way, towards 0.000: being huge is what makes the answer extreme, and the weights decide which extreme. (To isolate the damage, this demonstration pastes the four raw numbers into the prepared row and leaves everything else alone. Forgetting the preparation on the real table would more likely stop with an error about the words.) It is not confused. It is answering exactly the question it was asked, and the question was nonsense.

> **Pipeline** — a single object that holds several steps in a fixed order. Calling `fit` on it fits every step in order. Calling `predict_proba` on it runs every step in order. It has one name.

And here is the sentence to say twice:

> **The pipeline is not more careful than you. It is a shape that cannot be got wrong.**

With two objects, "remember to prepare first" is a thing a human has to remember, at 4pm on a Friday, six months from now, in a different file. With one object there is **no way in** — the only door into the model goes through the preparation. You cannot forget a step you cannot reach.

**And there is a second gift, which is why `Pipeline` exists at all rather than just being tidy.** Week 2's whole argument was that the validation pile must not influence the training. But the *preparation* learns things too — the median used to fill the holes, the centre of the ruler. If you prepare all 2000 rows and *then* split, those learned numbers have seen the validation and test rows.

Here is what actually changes, and it is worth running:

```text
the hole-filling value the pipeline learns
  median driver experience, 1200 TRAIN rows : 30.0
  median driver experience, all 2000 rows   : 29.0

the centre of the ruler the pipeline learns
  mean distance_km, 1200 TRAIN rows : 3.4591
  mean distance_km, all 2000 rows   : 3.5193
```

**Two different medians. Two different centres.** And the honest part, which you must say out loud: with this data the difference in AUC is about **0.0001** — far too small to notice. **That is precisely why it is dangerous.** It does not announce itself, it is invisible in the score, and on a different dataset it could be worth 0.05 or more (we have not measured one, but nothing stops it) and nobody ever finds out. `Pipeline` makes it impossible by construction: `pipe.fit(X_train, y_train)` fits the preparation on `X_train` and could not reach the other rows if it wanted to.

*(There is a proper name for this class of mistake and three named kinds of it. That is **Week 6**. Do not name it today.)*

### 5. `joblib`: the artifact crosses; the code does not

> **joblib** — a tool that writes a fitted Python object to a file and reads it back. Two lines: `joblib.dump(thing, "name.joblib")` and `thing = joblib.load("name.joblib")`.

```python
joblib.dump(pipe, "delivery_pipeline.joblib")
```

That writes **5002 bytes.** Five kilobytes. And inside those five kilobytes are: the median it will use to fill holes, the centre and width of the ruler for all five number columns, the list of every restaurant, day and weather it knows about, and the twenty-one numbers logistic regression learned. **Everything the model needs, and nothing else.**

![The artifact crosses; the training code does not](../figures/fig-w03-3-artifact-crossing-to-a-clean-process.svg)
*Figure 3.4 — The artifact crosses; the training code does not. If `predict.py` contains one `fit(`, the artifact was not the deliverable.*

> **Clean room test** — close the training file completely. Open a brand-new file that contains **no training code at all** — no `fit`, no split, no import of the data — load the artifact, and predict.

The three hand-typed orders come out at **0.968, 0.022 and 0.291**, and `predict.py` is 24 lines long and contains:

```text
occurrences of  fit(        : 0
occurrences of  make_data   : 0
occurrences of  train_test  : 0
```

**Those three zeros are the test.** Not a feeling about tidiness — a count. If `predict.py` needs to import `make_data`, then the artifact was not the deliverable, and the person you hand it to needs your data before they can use your model.

> **🧑‍🏫 If a student asks:** *"why not just save the numbers to a text file?"* You could, and people do, and it is more work than it sounds. You would have to write out the median, five means, five widths, fifteen category names in the right order, and twenty-one coefficients — and then write the code that applies them in the right order, and keep that code in step with the training code forever. `joblib` writes all of it, in the right order, in one line. **The reason to know it is a pickle-shaped file and not a magic box** is honesty about its one real weakness: see the Questions section on version mismatches. **And the second weakness, which the Questions section does not cover:** loading a pickle-shaped file can execute arbitrary code, so `joblib.load` must only ever be run on files from a source you trust. Say it in one sentence when the file first crosses to `predict.py`.

### 6. The model card: seven headings, twenty minutes

Here is the part nobody teaches and everybody needs.

A 5,002-byte file is completely silent. It does not know what it is for. It does not know what it must not be used for. It does not know that its test pile was never opened. **A number and a file with no writing beside them are a liability**, and the fix is a page of writing.

> **Model card** — a short document that travels with the artifact, under fixed headings, saying what it is for and where it breaks.

![The seven headings of a card](../figures/fig-w03-4-model-card-seven-headings.svg)
*Figure 3.5 — The seven headings of a card, with ours filled in. Seven headings, twenty minutes.*

| # | Heading | What goes under it | Ours |
|---|---|---|---|
| 1 | **Intended use** | what it is FOR, in one sentence | Flag a risky order at order time, so a dispatcher can act |
| 2 | **Out-of-scope use** | what it must NOT be used for | Not for driver pay, ratings or discipline decisions |
| 3 | **Unit of prediction** | what one row stands for | One order |
| 4 | **Training data** | how many rows, which columns, where from | 2000 rows (after 20 duplicates removed), 8 features, generated by `make_data.py`, seed 0 |
| 5 | **Splits** | the three counts, and whether test was opened | 1200 / 400 / 400, stratified. **Test pile not opened.** |
| 6 | **Metrics** | the number, the pile it came from, and the baseline | Validation ROC-AUC **0.7541** against a baseline of **0.5000** |
| 7 | **Known limitations** | where it breaks, in your own words | A restaurant the model has never seen becomes five zeros and it answers anyway, with no warning |

**Heading 2 is the one people skip and the one that matters most.** "Not for driver pay decisions" is not legal boilerplate. It is the sentence that stops somebody, in eight months, using a lateness model to decide who gets fewer shifts — a use the model was never measured for, on people who never agreed to it, from data that mostly measures distance and weather.

**Heading 7 has a real, demonstrable entry**, and you should run it before class so you can say it as a fact:

```text
SliceHouse (in the training data) P(late) = 0.291
PizzaNova  (never seen before)    P(late) = 0.308
no error, no warning, difference = 0.017
```

`PizzaNova` was never in the training data, so all five restaurant columns come out **0** — as if the order came from no restaurant at all — and the model answers **0.308** with total composure. That is not a bug we are going to fix today; `handle_unknown="ignore"` is what stops it crashing on new data, and it is the right choice. **It is a limitation, and limitations go in writing.**

### 7. Every line of this week's new code, explained to someone who has never programmed

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
```

Three new toolboxes. `pipeline` holds the welding tool, `compose` holds the switchboard, and `joblib` is the file writer. **`import joblib` on its own line, no `from`** — because we want the whole toolbox, not one tool out of it.

```python
NUMBER_COLUMNS = ["distance_km", "items", "prep_minutes",
                  "order_hour", "driver_experience_months"]
WORD_COLUMNS = ["restaurant", "day_of_week", "weather"]
```

Two lists of names, written in **CAPITALS** because that is Python's convention for *"this is a fixed setting, decided once, not something the program changes as it runs"*. Nothing happens here; these are just two lists of words. **They are also Week 1's card three, in code** — the eight features, split into two kinds.

```python
number_route = Pipeline(steps=[
    ("fill_holes", SimpleImputer(strategy="median")),
    ("same_ruler", StandardScaler()),
])
```

A `Pipeline` of two steps. **`steps=` takes a list, and each item in the list is a pair in round brackets: a name you invent, then the tool.** The name is yours — `"fill_holes"` could be `"bob"` — and its only job is to let you refer to that step later. **Order matters and it is the order they run in:** fill the holes first, then put things on one ruler, because we want the ruler measured on complete columns. (Swapping them does **not** error — `StandardScaler` skips the holes when learning the ruler and passes them through, and the imputer then fills them — but the numbers differ slightly; e.g. the Worked Example 1 column becomes -0.743 / 0.650 / -1.207 / -0.279 / 1.578 / -0.279 instead of -0.758 / 0.758 / -1.263 / -0.253 / 1.769 / -0.253.)

```python
prep = ColumnTransformer([
    ("num", number_route, NUMBER_COLUMNS),
    ("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS),
])
```

The switchboard. **Each route is a triple: a name, a treatment, and the columns it applies to.** So: route `"num"` applies `number_route` to the five number columns; route `"cat"` applies the word-splitter to the three word columns. `handle_unknown="ignore"` means *"if you meet a restaurant you have never seen, put zeros rather than crashing"* — which is heading 7 of the card.

```python
pipe = Pipeline(steps=[
    ("prep", prep),
    ("model", LogisticRegression(max_iter=1000, random_state=0)),
])
```

The weld. **One object. One name.** `max_iter=1000` is "you may take up to a thousand goes at finding your numbers" — the default of 100 is not always enough and warns you when it runs out. `random_state=0` for the same reason as always: **a number you cannot reproduce is not a result.**

```python
pipe.fit(X_train, y_train)
```

**One line, and it does everything in order.** Fill the holes using the training median. Learn the ruler from the training rows. Learn which restaurants exist. Then fit the model on the result. Every one of those learns from `X_train` and only `X_train`, and there is no way to ask it to do otherwise.

```python
print("columns out:", prep.transform(X_train).shape)
```

`prep` is still a name we can use, and after `pipe.fit` it is **fitted** — a `Pipeline` fits the objects you handed it, not copies of them. So this asks the switchboard alone: *"show me what you turn 1200 rows of 8 columns into."* Answer: `(1200, 20)`. **This is the print that checks your paper arithmetic.**

```python
joblib.dump(pipe, "delivery_pipeline.joblib")
```

Write the whole fitted object to a file called `delivery_pipeline.joblib`. **The `.joblib` ending is a convention, not a rule** — the file would work if you called it `cheese`, and nobody would thank you.

```python
pipe = joblib.load("delivery_pipeline.joblib")
```

In the new file: read it back. **What comes out is a fully fitted pipeline**, ready to predict, with no training and no data anywhere in sight.

```python
orders = pd.DataFrame([{...}, {...}, {...}])
prob = pipe.predict_proba(orders)[:, 1]
```

A `DataFrame` built from a list of dictionaries — one dictionary per order, each key a column name. **The keys have to match the eight column names exactly**, because the switchboard looks up by name. `predict_proba(...)[:, 1]` is Week 2's tool, unchanged: every row, column 1, the chance of "late".

### 8. The three misconceptions you will actually meet

**Misconception 1 — "the pipeline is just tidier."**

It is tidier, and that is the least of it. Two objects can be dropped; one cannot. And the demonstration is the number: **0.709 becomes 1.000**, with no error message of any kind. The cure is to run that demo rather than describe it, and to say the sentence: *"the right-hand picture is not more careful, it is a shape that cannot be got wrong."*

**Misconception 2 — "the artifact is the code."**

The most common version of this is a `predict.py` that imports `make_data`, splits the table, fits, and *then* predicts — and the student thinks they have done the clean room test because the file has "predict" in the name. The cure is mechanical and it is why we count: **`fit(` must appear zero times.** Counting is not pedantry; it is the only version of this check that cannot be fooled by good intentions.

**Misconception 3 — "the model card is paperwork we do at the end if there's time."**

Half of the card cannot be written at the end. Heading 5 says whether the test pile was opened — and if you write that after five weeks of poking about, you will write what you wish were true. Heading 3 (the unit of prediction) is Week 1's card one, heading 4's feature list is card three and heading 6's metric is card five; headings 1 and 2 are new. **The card is not a report; it is the contract, updated.** The cure is to point at the Week 1 index cards: three of the seven headings are already written, in their own handwriting, from two weeks ago.

### 9. How deep to go, and where to stop

**Go this far:** `ColumnTransformer` with two named routes and the columns chosen by name. The 5 + 5 + 7 + 3 = 20 count, done on paper first and then checked with `.shape`. `Pipeline` as a weld, with the 0.709-to-1.000 demonstration run live. `joblib.dump` and `joblib.load`. The clean room test, with the three counts printed. All seven card headings, filled in with our real numbers. The two medians that show why preparing early is a problem.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| What `StandardScaler` actually does — mean, standard deviation, z-scores | **Week 4.** Today: "puts them all on the same ruler". |
| What `OneHotEncoder` actually does, and ordinal encoding | **Week 4.** Today: "one column per value that exists". |
| What `SimpleImputer` actually does, `add_indicator`, and whether the median is the right choice | **Week 6.** Today: "fills the holes with the middle value from the training rows". |
| What logistic regression **is** — the S-curve, the score, the coefficients | **Weeks 13–15.** Today it is a named box that turns 20 numbers into one probability. |
| The word **leakage**, and its three named kinds | **Week 6.** You may say "the preparation saw rows it shouldn't have" as often as you like. Do not name it. |
| `pipe.set_params(...)`, swapping parts to compare them | **Week 7.** |
| `pipe.get_feature_names_out()` | **Week 5.** Today we count to 20 on paper, which is better for exactly one week. |
| Opening the test pile | **Not this term.** Heading 5 says "not opened" and it must stay true. |
| Threshold tuning — "should 0.291 count as late?" | **Week 10.** Today a probability is a probability. |

The line to keep in your head all lesson: **the deliverable is a file and a page, not a number.**

---

### 10. 🧭 The Growing Map

The student guide carries **Where This Fits** — the same picture every week with one more piece filled in.
This is the third and final week of the first tile, so today the map is about **closing** something.

![The Level 3 pipeline in Week 3: the decisions and split tile closes with the model saved as a file](../figures/fig-w03-0-where-this-fits.svg)

*Figure 3.0 — Week 3's version. Last week in the gold tile. The ↻ on stage three is the training loop, still
grey until Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask *"which box did we do today?"*** Same gold tile, third week running — *decisions and
   the split*. Then the real question: *"we finally trained a model today. Does that mean we have reached
   stage five?"* **No.** Point at the eight lines out of forty-five. The model was the cheap part; the tile
   closes because there is now a **file** and a **card**, not because something got fitted.
2. **Then hold up the `.joblib` file on screen — 5,002 bytes — and ask *"what is missing from this file?"***
   The answer is **nothing**, and that is the whole week: the scaler, the encoder, the column routing and
   the fitted model are all in there. That is why the tile can close. Ask what would be missing if they had
   saved the model without the `Pipeline`, and let them list it.
3. **Then look forward, on the map:** *"find the tile where we do this again for a neural network."*
   Stage four, first tile, Week 23. And *"find the tile where we ship one for real."* Stage five, bottom,
   Week 34. Today's habit is the one that gets reused at both.

> **🧑‍🏫 Why this is worth two minutes.** A student who thinks "we built a model" has learned the wrong
> thing from today, and the map is the cheapest correction you have: the gold tile is labelled *decisions
> and the split*, not *models*. It is still stage **one**. If the artifact is what closes stage one, then
> the artifact — not the AUC — is what they should be proud of.

**One thing to notice, so you can answer if asked.** The tile is still gold, not white, even though the
work is finished. White arrives next week, when the gold moves down to *scaling · features*. The rule on
this map is simple and worth stating once: **gold is where you are standing, white is what is behind you,
dashed is not yet.**

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Work in the Week 1 folder.** Weeks 1 to 7 live together, and this week imports Week 1's file unchanged.

```bash
cd ~/level3/term1
ls
python3 make_data.py
```

You must see `make_data.py` in the listing, and the first `order_id` must be **100955**. If it is not, stop and fix that before anything else.

- [ ] **Check `joblib` imports.** It ships with scikit-learn, so this will work — find out tonight rather than at minute forty.

```bash
python3 -c "import joblib; print(joblib.__version__)"
```

```text
1.2.0
```

*(Yours may differ. Anything 1.0 or later behaves identically for this week.)*

- [ ] **Type `train_pipeline.py` yourself and run it.** This is the file you build together in class, and it is the longest file of the term so far.

```python
"""train_pipeline.py - fit one sealed pipeline, measure it, save it. Runs once."""
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

NUMBER_COLUMNS = ["distance_km", "items", "prep_minutes",
                  "order_hour", "driver_experience_months"]
WORD_COLUMNS = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])

X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=0)
print("piles:", len(y_train), len(y_val), len(y_test))

# ROUTE 1 - the five number columns: fill the holes, then one ruler for all.
number_route = Pipeline(steps=[
    ("fill_holes", SimpleImputer(strategy="median")),
    ("same_ruler", StandardScaler()),
])

# THE SWITCHBOARD - route 1 for numbers, route 2 for words, selected by name.
prep = ColumnTransformer([
    ("num", number_route, NUMBER_COLUMNS),
    ("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS),
])

# THE SEALED BOX - preparation and model, welded, one name.
pipe = Pipeline(steps=[
    ("prep", prep),
    ("model", LogisticRegression(max_iter=1000, random_state=0)),
])

pipe.fit(X_train, y_train)

print("columns in :", X_train.shape)
print("columns out:", prep.transform(X_train).shape)
print("restaurants:", X_train["restaurant"].nunique(),
      " days:", X_train["day_of_week"].nunique(),
      " weathers:", X_train["weather"].nunique())

prob_val = pipe.predict_proba(X_val)[:, 1]
auc = roc_auc_score(y_val, prob_val)

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
base = roc_auc_score(y_val, dummy.predict_proba(X_val)[:, 1])

print(f"validation ROC-AUC  : {auc:.4f}")
print(f"baseline ROC-AUC    : {base:.4f}")
print(f"beat the baseline by: {auc - base:.4f}")

joblib.dump(pipe, "delivery_pipeline.joblib")
print("saved delivery_pipeline.joblib")
```

**Takes about 1 second.** You must see exactly this:

```text
piles: 1200 400 400
columns in : (1200, 8)
columns out: (1200, 20)
restaurants: 5  days: 7  weathers: 3
validation ROC-AUC  : 0.7541
baseline ROC-AUC    : 0.5000
beat the baseline by: 0.2541
saved delivery_pipeline.joblib
```

- [ ] **Check the size of the file you just made.** This number goes on the board.

```bash
ls -l delivery_pipeline.joblib
```

```text
-rw-r--r--  1 you  staff  5002 ... delivery_pipeline.joblib
```

**5002 bytes.** Five kilobytes, containing a whole working model. *(The number in the middle is the size in bytes; the rest of the line is dates and permissions and will look different on your machine.)*

- [ ] **Type `predict.py` and run it.** This is the clean room, and it is the homework.

```python
"""predict.py - loads the artifact and predicts. Contains no training code at all."""
import joblib
import pandas as pd

pipe = joblib.load("delivery_pipeline.joblib")

orders = pd.DataFrame([
    {"restaurant": "CrustyBros", "distance_km": 8.5, "items": 4, "prep_minutes": 22.0,
     "order_hour": 19, "day_of_week": "Fri", "weather": "storm",
     "driver_experience_months": 12.0},
    {"restaurant": "Napoli", "distance_km": 1.2, "items": 1, "prep_minutes": 8.0,
     "order_hour": 12, "day_of_week": "Tue", "weather": "clear",
     "driver_experience_months": 42.0},
    {"restaurant": "SliceHouse", "distance_km": 4.2, "items": 3, "prep_minutes": 14.0,
     "order_hour": 18, "day_of_week": "Sat", "weather": "rain",
     "driver_experience_months": 42.0},
])

prob = pipe.predict_proba(orders)[:, 1]

for i in range(len(orders)):
    row = orders.iloc[i]
    print(f"{row['restaurant']:13s} {row['distance_km']:4.1f} km  {row['weather']:6s} "
          f"{row['order_hour']:2d}:00   P(late) = {prob[i]:.3f}")
```

**Takes about 0.7 seconds**, nearly all of it importing scikit-learn.

```text
CrustyBros     8.5 km  storm  19:00   P(late) = 0.968
Napoli         1.2 km  clear  12:00   P(late) = 0.022
SliceHouse     4.2 km  rain   18:00   P(late) = 0.291
```

**Read those three and check they make sense.** Long, stormy, rush-hour from the slow restaurant: 0.968. Short, clear, lunchtime, experienced driver: 0.022. Middling: 0.291. **A model whose three answers do not tell a sensible story is a model with a bug, and this eyeball test costs five seconds.**

- [ ] **Type `clean_room_check.py` and run it.** Four lines, and it is the objective.

```python
"""clean_room_check.py - is predict.py really a clean room?"""
text = open("predict.py").read()
print("occurrences of  fit(        :", text.count("fit("))
print("occurrences of  make_data   :", text.count("make_data"))
print("occurrences of  train_test  :", text.count("train_test"))
print("lines in predict.py         :", len(text.splitlines()))
```

```text
occurrences of  fit(        : 0
occurrences of  make_data   : 0
occurrences of  train_test  : 0
lines in predict.py         : 24
```

- [ ] **Type `kept_apart.py` and run it. This is the demonstration the week rests on.** If you rehearse one thing tonight, rehearse this one, because you need to be able to say "watch" and mean it.

```python
"""kept_apart.py - the two-loose-objects version, and what it costs."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

NUMBER_COLUMNS = ["distance_km", "items", "prep_minutes",
                  "order_hour", "driver_experience_months"]
WORD_COLUMNS = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=0)

number_route = Pipeline(steps=[("fill_holes", SimpleImputer(strategy="median")),
                               ("same_ruler", StandardScaler())])
prep = ColumnTransformer([("num", number_route, NUMBER_COLUMNS),
                          ("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS)])

# TWO OBJECTS, KEPT APART. Two things to remember, in the right order.
model = LogisticRegression(max_iter=1000, random_state=0)
prep.fit(X_train)
model.fit(prep.transform(X_train), y_train)

print("validation ROC-AUC:", round(roc_auc_score(
    y_val, model.predict_proba(prep.transform(X_val))[:, 1]), 4))

one = pd.DataFrame([{
    "restaurant": "GreenLeaf", "distance_km": 7.4, "items": 5, "prep_minutes": 22.0,
    "order_hour": 19, "day_of_week": "Thu", "weather": "rain",
    "driver_experience_months": 59.0}])

ready = prep.transform(one)
print()
print("the four typed numbers, raw     :", [7.4, 5.0, 22.0, 19.0])
print("the same four, after preparation:", np.round(ready[0][:4], 3))
print()
print(f"prepared   P(late) = {model.predict_proba(ready)[0, 1]:.3f}")

# A controlled demonstration: put the four RAW numbers into the four slots the
# preparation had filled, and change nothing else at all.
unprepared = ready.copy()
unprepared[0, :4] = [7.4, 5.0, 22.0, 19.0]
print(f"unprepared P(late) = {model.predict_proba(unprepared)[0, 1]:.3f}")
print(f"damage             = {model.predict_proba(unprepared)[0, 1] - model.predict_proba(ready)[0, 1]:.3f}")
```

```text
validation ROC-AUC: 0.7541

the four typed numbers, raw     : [7.4, 5.0, 22.0, 19.0]
the same four, after preparation: [1.793 0.811 2.008 0.662]

prepared   P(late) = 0.709
unprepared P(late) = 1.000
damage             = 0.291
```

**Notice the first line: 0.7541, identical to the pipeline version.** Say this in class, because it removes any suspicion of magic: **the sealed box is not a better model, it is the same model with no way to reach it wrongly.**

- [ ] **Type `leak_demo.py` and run it.** Thirty seconds of class time, and it is the argument for why the weld matters as well as the tidiness.

```python
"""leak_demo.py - preparing before splitting: exactly which numbers change."""
from sklearn.model_selection import train_test_split
from make_data import make_deliveries

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=0)

print("the hole-filling value the pipeline learns")
print("  median driver experience, 1200 TRAIN rows :",
      X_train["driver_experience_months"].median())
print("  median driver experience, all 2000 rows   :",
      X["driver_experience_months"].median())
print()
print("the centre of the ruler the pipeline learns")
print("  mean distance_km, 1200 TRAIN rows :", round(X_train["distance_km"].mean(), 4))
print("  mean distance_km, all 2000 rows   :", round(X["distance_km"].mean(), 4))
```

```text
the hole-filling value the pipeline learns
  median driver experience, 1200 TRAIN rows : 30.0
  median driver experience, all 2000 rows   : 29.0

the centre of the ruler the pipeline learns
  mean distance_km, 1200 TRAIN rows : 3.4591
  mean distance_km, all 2000 rows   : 3.5193
```

- [ ] **Type `known_limits.py` and run it.** This is heading 7 of the card, as a fact rather than a worry.

```python
"""known_limits.py - what happens to a restaurant the model has never seen."""
import pandas as pd
import joblib

pipe = joblib.load("delivery_pipeline.joblib")

order = {"restaurant": "SliceHouse", "distance_km": 4.2, "items": 3,
         "prep_minutes": 14.0, "order_hour": 18, "day_of_week": "Sat",
         "weather": "rain", "driver_experience_months": 42.0}

known = pd.DataFrame([order])
new = pd.DataFrame([{**order, "restaurant": "PizzaNova"}])

print("SliceHouse (in the training data) P(late) =",
      round(pipe.predict_proba(known)[0, 1], 3))
print("PizzaNova  (never seen before)    P(late) =",
      round(pipe.predict_proba(new)[0, 1], 3))
print("no error, no warning, difference =",
      round(pipe.predict_proba(new)[0, 1] - pipe.predict_proba(known)[0, 1], 3))
```

```text
SliceHouse (in the training data) P(late) = 0.291
PizzaNova  (never seen before)    P(late) = 0.308
no error, no warning, difference = 0.017
```

- [ ] **Break it on purpose, twice**, so neither traceback is a surprise:
  1. Delete `"weather"` from the dictionary of an order in `predict.py`. You get a traceback ending in `ValueError: columns are missing: {'weather'}`.
  2. Put the model **first** in the outer `Pipeline`. It does not complain when you build it. It complains at `fit` with `TypeError: All intermediate steps should be transformers...`.
- [ ] **Print workbook pages 3.1–3.3, and the seven card headings on their own sheet.**
- [ ] **Find two boxes or two envelopes, one that fits inside the other.** The nesting is the whole `Pipeline` idea and it takes four seconds to show.
- [ ] **Check Week 2's baseline box is still on the wall.** Today's `0.7541` gets written directly underneath it, and the subtraction is the point.

### 5 minutes on the day

- [ ] Terminal in `~/level3/term1`. `make_data.py` present and proved with one run.
- [ ] `train_pipeline.py`, `predict.py`, `clean_room_check.py`, `kept_apart.py`, `leak_demo.py`, `known_limits.py` **deleted or renamed** — they type them.
- [ ] **`delivery_pipeline.joblib` deleted.** It has to appear in front of them.
- [ ] The two nesting boxes on the table.
- [ ] Workbook 3.1–3.3 out. **3.2's column count filled in pen before any code runs.**
- [ ] Week 2's baseline box on the wall, with space under it.

### Fallback if the laptop fails

**This week's paper version is genuinely good**, because two of the four objectives are writing and one is counting.

1. **The Hook is the two boxes.** Hold up two envelopes. *"Two things to remember, in order. What happens when you forget one?"* Then put one inside the other. *"Now how many things?"*
2. **The switchboard is arithmetic.** On paper: five number columns stay five. Restaurant has 5 values, day has 7, weather has 3 — so 5 + 7 + 3 = 15. Total 5 + 15 = **20.** That is objective 1, complete, with a pencil.
3. **The forgotten-preparation disaster works on paper too**, with the four numbers from the table above: the model expected numbers around 1.793, 0.811, 2.008, 0.662 and got 7.4, 5.0, 22.0, 19.0 — **four to thirty times too big.** *"So will the answer be more extreme or less extreme?"* More extreme — and all four numbers push towards *late*, so it goes to 1.000. (A negatively-weighted number such as driver experience would push towards 0.000.)
4. **The model card is the homework anyway.** Seven headings, on paper, filled in from the Week 1 index cards and the Week 2 box. **That is objective 4, complete**, and it is the part of this week most likely to be remembered in five years.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'joblib'` | Nearly impossible — it comes with scikit-learn. If it happens, the scikit-learn install is broken; go to the paper version and reinstall before Week 4. |
| `ModuleNotFoundError: No module named 'make_data'` | Wrong folder. `cd` and prove it with `ls`. Still the commonest error of the term. |
| `columns out` is not `(1200, 20)` | One of the three word-column counts is wrong, or a column name is misspelled in one of the two lists. **Print `X_train["restaurant"].nunique()` and friends and find which of 5, 7, 3 is wrong.** |
| The AUC is not 0.7541 | `random_state` missing somewhere, or `drop_duplicates()` missing (check the piles line says `1200 400 400`), or the two `train_test_split` calls in the wrong order. |
| The file is not 5002 bytes | A different scikit-learn version pickles slightly differently. **This is fine** — say the real number on their machine and move on. Nothing in the lesson depends on 5002 except the pleasure of it. |
| `predict.py` crashes with `columns are missing` | A key is misspelled or absent in one of the three order dictionaries. The message names the column. |
| The student wants to open the test pile | "Heading 5 of your card says *not opened*. Are you going to write it, or change it?" |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Two Things to Remember, or One | 7 | 7 | Two envelopes. Then the 0.709-to-1.000 disaster on screen. |
| 🧠 Concept — The Switchboard and the Weld | 18 | 25 | Count to 20 on paper. Nest the boxes. The two medians. |
| 💻 Live-Code Together — `train_pipeline.py` | 18 | 43 | Build it, fit it, measure it, save it. Two deliberate mistakes: one loud, one silent. |
| 🎲 Their Turn — The Clean Room Test | 20 | 63 | A brand-new `predict.py`, three orders by hand, and the count that proves it. |
| 🔑 Wrap & Assign | 7 | 70 | 0.7541 under the box. Three checks. Homework. |

---

### 🪝 Hook — Two Things to Remember, or One (7 minutes)

**Do this:** Laptops closed. Two envelopes on the table, side by side.

**Say this:**

> "Two weeks of writing and today we build a model. It's three lines and it works and it's not what today is about.
>
> Here's what today is about. Look at these two envelopes."

**Do this:** Pick up the left one. Then the right one.

> "This one is called *the preparation*. It knows how to turn a raw order — words, holes, numbers on wild different scales — into something a model can add up.
>
> This one is called *the model*. It knows how to turn that into a probability.
>
> **Two things. And they have to be used in the right order, every single time, forever, by anybody who ever touches this system.** Including you, in eight months, on a Friday afternoon, in a different file.
>
> What happens if somebody forgets the first one?"

Take answers. Most students say "it'll crash" or "you'll get an error".

> "Sometimes it does crash — the raw table has words in it, and the words stop it. But that's the hopeful answer, and the dangerous case is the one that doesn't crash: numbers that look like numbers, just on the wrong scale. Let me show you what happens then."

**Do this:** Open one laptop and run `kept_apart.py`, which you typed last night.

```text
the four typed numbers, raw     : [7.4, 5.0, 22.0, 19.0]
the same four, after preparation: [1.793 0.811 2.008 0.662]

prepared   P(late) = 0.709
unprepared P(late) = 1.000
damage             = 0.291
```

**Do this:** Silence. Let them read it.

> **Say this:** "One order. Seven point four kilometres, five items, twenty-two minutes in the kitchen, seven in the evening, raining.
>
> Prepared properly, the model receives those numbers rescaled — **1.793, 0.811, 2.008, 0.662** — and says **0.709.** Seventy percent chance of being late. Sensible.
>
> Forget the preparation, hand it the raw **7.4, 5.0, 22.0, 19.0**, and it says **1.000.**
>
> **One point zero zero zero.** Total, absolute certainty. And no error. No warning. No red text. Nothing at all.
>
> Why is it so sure? Because it learned on a world where those numbers sit around zero and rarely leave minus two to plus five. I've just handed it twenty-two. The numbers are **four to thirty times too big**, so the answer gets thrown off the end of the scale — and these four all push towards late, so it goes to 1.000. It isn't confused. It answered the question I asked, and my question was nonsense."

**Do this:** Now pick up the two envelopes, and slide one inside the other. Hold up the outer one.

> "So here's today's move. **Instead of being careful, we change the shape.**
>
> One envelope, with the other one inside it. **How many things do you have to remember now?**"

*One.*

> "One. And how do you get to the model without going through the preparation?"

*You can't.*

> "**You can't. There's no way in.** That's not being careful. Careful is a thing you can fail at. This is a shape that cannot be got wrong.
>
> That object has a name in Python: a **`Pipeline`**. And when you save it to a file, that file is what you hand somebody. Not the score. Not the code. **The file.** It's five kilobytes and it's the whole deliverable, and by the end of today you'll have made one."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Two objects, right order. What if you forget one?" | If the raw numbers reach the model (words already handled), a confident, wrong answer with no error. | "It crashes" is the expected answer — reward the instinct and then show the screen. That gap is the lesson. |
| "Why is the model so *sure* rather than just wrong?" | The numbers are far bigger than anything it trained on, so the sum it adds up is thrown off the end of the scale — and these four all push towards late, so the answer is pushed to 1.000. | If stuck: "22 instead of 2. Ten times bigger. So the push towards *late* is ten times bigger too — what does that do to the answer?" |
| "How many things to remember with one envelope inside another?" | One. | If they say two, hold up only the outer envelope: "how many am I holding?" |
| "So is the pipeline a better model?" | No — the same model, with no way to reach it wrongly. | Point at the first line of the output: 0.7541 either way. **The identical AUC is the proof.** |
| "What would you hand to the pizza company?" | The file. | "The code" is the common answer — then ask: "and do they have your data? your Python? your version of scikit-learn?" |

---

### 🧠 Concept — The Switchboard and the Weld (18 minutes)

**Say this — part 1, why eight columns are not eight numbers:**

> "Before anything else: our X has eight columns, and a model can only do arithmetic. Let's see which columns it can actually use."

**Do this:** Draw two lists on the board as you talk.

```text
   the model can add these up          the model cannot
   --------------------------          -----------------
   distance_km        7.4              restaurant   "GreenLeaf"
   items              5                day_of_week  "Thu"
   prep_minutes       22.0             weather      "rain"
   order_hour         19
   driver_exp         59.0  <- or NOTHING, in 108 rows
```

> "Five number columns, three word columns. And **two different problems.**
>
> The word columns are words. You can't multiply `"rain"` by anything. So each word column becomes **one new column per value that exists**, holding a 0 or a 1.
>
> And the number columns have holes — a hundred and eight of them, all in driver experience, which you counted in Week 1. You can't multiply by nothing either. So each hole gets filled with the middle value from the training rows.
>
> There's a third thing, quieter. Distance runs zero to fifteen. Driver experience runs zero to fifty-nine. Left alone, **the big-numbered column shouts.** So all five get put on the same ruler.
>
> Two of those three are Week 4 and one is Week 6, properly, with the maths. **Today they're named parts you wire up**, and the wiring is what I'm teaching."

**Say this — part 2, the count. This is workbook page 3.2 and it is in pen:**

> "**Page 3.2, in pen, before we touch the keyboard.**
>
> Eight columns go in. **How many come out?** Work it out on paper. You have everything you need."

Let them struggle for two minutes. Then walk it through on the board, slowly.

```text
   ROUTE 1  the 5 number columns
            fill the holes  -> still 5
            one ruler       -> still 5
                                     5 out

   ROUTE 2  the 3 word columns
            restaurant   how many different?  5   -> 5 columns
            day_of_week  how many different?  7   -> 7 columns
            weather      how many different?  3   -> 3 columns
                                     5 + 7 + 3 = 15 out

   GLUED    5 + 15 = 20

   (1200, 8)  ->  (1200, 20)
```

> **Say this:** "**Twenty.** Five plus five plus seven plus three.
>
> And notice the 1200 doesn't move. We're not adding rows or losing rows. **We're re-describing each row using more columns.**
>
> Write this down, because it's the habit that saves you all year: **count the columns on paper, then print the shape and check.** If the shape says 20, your counting was right. If it says 19 or 22, one of your three counts is wrong — and finding that out now costs thirty seconds. Finding it out in Week 17 costs an afternoon."

**Ask this:** *"Where did the 5, the 7 and the 3 come from?"*

The answer is Week 1's tool: `nunique()`. Five restaurants, seven days of the week, three kinds of weather. If nobody gets it, say: *"you already have the command that counts them — you used it to catch `order_id`."*

**Say this — part 3, the weld, and the second reason for it:**

**Do this:** Pick up the envelopes again. Nest them.

> "So: a **switchboard** that routes number columns one way and word columns the other, and glues the results together. That's one object, and it's called a `ColumnTransformer`.
>
> Then that goes inside a `Pipeline`, with the model, in that order. **One object. One name.** That's the envelope inside the envelope, and it's why forgetting the preparation stops being possible.
>
> But there's a second reason for the weld, and it's about Week 2 rather than about Friday afternoons. Watch this."

**Do this:** Run `leak_demo.py`.

```text
the hole-filling value the pipeline learns
  median driver experience, 1200 TRAIN rows : 30.0
  median driver experience, all 2000 rows   : 29.0

the centre of the ruler the pipeline learns
  mean distance_km, 1200 TRAIN rows : 3.4591
  mean distance_km, all 2000 rows   : 3.5193
```

> **Say this:** "The preparation **learns things too.** It learns the number it uses to fill the holes. It learns where the middle of the ruler goes.
>
> And look: learned from the twelve hundred training rows, the middle value is **30.** Learned from all two thousand, it's **29.** Different number. And the centre of the distance ruler is 3.4591 or 3.5193 depending on which rows you looked at.
>
> So if you prepare all two thousand rows and *then* split them, **the numbers inside your preparation have seen your validation pile and your test pile.** After everything Week 2 was about.
>
> Now the honest part, and I want you to feel how uncomfortable it is: on this data, doing it wrong changes the AUC by about **one ten-thousandth.** You would never, ever notice.
>
> **That's exactly why it's dangerous.** It doesn't announce itself, it's invisible in the score, and on somebody else's data it could be worth 0.05 or more (we haven't measured one, but nothing stops it) and nobody ever finds out. So we don't remember to avoid it. **We build a shape where it can't happen:** `pipe.fit(X_train, y_train)` fits the preparation on the training rows and could not reach the others if it wanted to."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Eight columns in. How many out?" | 20. | If wrong, ask for the three word-column counts separately. The error is always in one of 5, 7, 3. |
| "Where did 5, 7 and 3 come from?" | `nunique()` on each word column. | If stuck, remind them they used it on `order_id` in Week 1. |
| "Does the row count change?" | No. 1200 in, 1200 out. | If they say yes, ask "did we add any orders?" |
| "What does the preparation *learn*?" | The hole-filling value, and the centre and width of the ruler. | If they say "nothing, it just converts", point at 30.0 vs 29.0 on the screen. |
| "The wrong way changes AUC by 0.0001. So why care?" | Because it is invisible here and might not be elsewhere — and we cannot tell which. | If they say "so it doesn't matter", agree it does not matter *today*, then ask how they would know on the next dataset. |
| "Why not just remember to prepare first?" | Because remembering is a thing you can fail at, and the shape isn't. | If they insist they would remember: "for the next thirty-three weeks? On every file?" |

---

### 💻 Live-Code Together — `train_pipeline.py` (18 minutes)

**You never touch the keyboard.** Predictions before every run.

**Step 1 (3 min).** New file, `train_pipeline.py`. Imports, and the split copied from Week 2.

```python
"""train_pipeline.py - fit one sealed pipeline, measure it, save it. Runs once."""
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from make_data import make_deliveries

NUMBER_COLUMNS = ["distance_km", "items", "prep_minutes",
                  "order_hour", "driver_experience_months"]
WORD_COLUMNS = ["restaurant", "day_of_week", "weather"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])

X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=0)
print("piles:", len(y_train), len(y_val), len(y_test))
```

> **Say this:** "Ten imports, and that's the most you'll ever type in this course in one go. Read them as a shopping list: the welding tool, the switchboard, last week's dummy, the hole-filler, the model, the metric, the splitter, the pipeline, the two preparers.
>
> Then `import joblib` on its own line with no `from`, because we want the whole toolbox rather than one tool out of it.
>
> Then the two lists in **capitals.** Capitals in Python mean 'this is a fixed setting, decided once'. And notice what those two lists actually are: **Week 1's card three, in code.** Eight features, split into two kinds.
>
> And then the split from last week, unchanged. Last time you'll copy it."

Run it.

```text
piles: 1200 400 400
```

**Step 2 (4 min).** The two routes and the switchboard.

```python
# ROUTE 1 - the five number columns: fill the holes, then one ruler for all.
number_route = Pipeline(steps=[
    ("fill_holes", SimpleImputer(strategy="median")),
    ("same_ruler", StandardScaler()),
])

# THE SWITCHBOARD - route 1 for numbers, route 2 for words, selected by name.
prep = ColumnTransformer([
    ("num", number_route, NUMBER_COLUMNS),
    ("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS),
])
```

> **Say this:** "`Pipeline(steps=[...])` — a list, and each item in the list is a **pair in round brackets: a name you invent, then the tool.** The name is genuinely yours. `"fill_holes"` could be `"bob"`. It's a label so you can refer to that step later.
>
> And the order is the order they run in. Fill the holes **first**, then the ruler — because we want the ruler measured on complete columns. Swap those two lines and, be ready for this, you do *not* get an error — the ruler just quietly ignores the holes and the numbers come out slightly different. Silent again.
>
> Then the switchboard. Each route is a **triple: a name, a treatment, and the list of columns it applies to.** Route `num` sends `number_route` at the five number columns. Route `cat` sends the word-splitter at the three word columns.
>
> `handle_unknown="ignore"` means: **if you meet a restaurant you've never seen, put zeros instead of crashing.** Remember that setting. It comes back at the end of the lesson and it goes on the card."

**Ask before going on:** *"The columns are chosen by name. So does the order of the columns in my table matter?"*

Let them guess. The answer is no, and we prove it in the activity.

**Step 3 (3 min).** The weld, the fit, and the shape check.

```python
# THE SEALED BOX - preparation and model, welded, one name.
pipe = Pipeline(steps=[
    ("prep", prep),
    ("model", LogisticRegression(max_iter=1000, random_state=0)),
])

pipe.fit(X_train, y_train)

print("columns in :", X_train.shape)
print("columns out:", prep.transform(X_train).shape)
print("restaurants:", X_train["restaurant"].nunique(),
      " days:", X_train["day_of_week"].nunique(),
      " weathers:", X_train["weather"].nunique())
```

> **Say this:** "The weld. Preparation, then model. **One object, one name, and one order that can't be changed by accident.**
>
> Then `pipe.fit(X_train, y_train)` — **one line, and it does all of it in order.** Fill the holes using the training median. Learn the ruler from the training rows. Learn which restaurants exist. Then fit the model on the result. All of it from `X_train`, and there's no way to ask it for anything else.
>
> `max_iter=1000` is 'you may have up to a thousand goes at finding your numbers'; the default of a hundred isn't always enough and it warns you when it runs out.
>
> Now — **before we run it. Page 3.2. What number did you write in pen?**"

Get the number out loud. Then run it.

```text
columns in : (1200, 8)
columns out: (1200, 20)
restaurants: 5  days: 7  weathers: 3
```

**Do this:** Point at the three counts, then at the 20.

> **Say this:** "**Five, seven, three.** And five number columns. Five plus five plus seven plus three is twenty. **Your paper arithmetic and the computer's shape agree**, and that agreement is what you're going to check every week for the rest of the year.
>
> Twelve hundred rows in, twelve hundred rows out. Only the description got wider."

**Step 4 — ⚠️ FIRST DELIBERATE MISTAKE (2 min).** Put the model first. This one **does not complain when you build it.**

> **Say this:** "Swap the two lines in the outer pipeline. Model first, prep second."

```python
pipe = Pipeline(steps=[
    ("model", LogisticRegression(max_iter=1000, random_state=0)),
    ("prep", prep),
])
```

**Ask before running:** *"When does this complain? When we build it, or when we fit it?"*

Run it. Real output, tail end:

```text
Traceback (most recent call last):
  File "/Users/you/level3/term1/train_pipeline.py", line 46, in <module>
    pipe.fit(X_train, y_train)
  ...
  File ".../sklearn/pipeline.py", line 340, in _validate_steps
    raise TypeError(
TypeError: All intermediate steps should be transformers and implement fit and transform or be the string 'passthrough' 'LogisticRegression(max_iter=1000, random_state=0)' (type <class 'sklearn.linear_model._logistic.LogisticRegression'>) doesn't
```

> **Say this:** "Look at **which line** it points at. Not the line where I built the pipeline — the line where I **fitted** it. Building a wrong pipeline is silent; using one is not.
>
> And the message is doing real work if you slow down: *'all intermediate steps should be transformers'*. **Intermediate** means every step except the last. A transformer is a thing that changes data and passes it on. A model is a thing that ends the line — it produces answers, not data. **So a model can only ever be last.**
>
> That's a nice, honest constraint: **a pipeline is a queue with a worker at the end.**"

Fix it. **Bug Log entry now:** *saw* `TypeError: All intermediate steps should be transformers...` · *means* a model can only be the last step · *cause* prep and model in the wrong order · *fix* prep first, model last — and note that it only complained at `fit`, not at build.

**Step 5 (3 min).** Measure it, against last week's box.

```python
prob_val = pipe.predict_proba(X_val)[:, 1]
auc = roc_auc_score(y_val, prob_val)

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
base = roc_auc_score(y_val, dummy.predict_proba(X_val)[:, 1])

print(f"validation ROC-AUC  : {auc:.4f}")
print(f"baseline ROC-AUC    : {base:.4f}")
print(f"beat the baseline by: {auc - base:.4f}")
```

> **Say this before running:** "`predict_proba(X_val)[:, 1]` — last week's tool, unchanged. Every row, column one, the chance of late.
>
> And notice I'm rebuilding last week's dummy in the same script. **Never report a number without its baseline in the same printout.** If they're in two different files, sooner or later somebody quotes one without the other."

Run it.

```text
validation ROC-AUC  : 0.7541
baseline ROC-AUC    : 0.5000
beat the baseline by: 0.2541
```

**Do this:** Go to Week 2's box on the wall. Write directly underneath it:

```text
   validation ROC-AUC   0.7541
   baseline             0.5000
   ------------------------------
   above the zero       0.2541
```

> **Say this:** "**0.7541.** And here's why last week mattered: I can tell you exactly what that number is worth. It is **0.2541 above the score of learning nothing.**
>
> Without last week, 0.7541 is just a number that sounds all right. **With last week, it's a distance from a zero I can point at.** That's the whole reason we spent a lesson building two useless models."

**Step 6 (3 min).** Save it. This is the deliverable.

```python
joblib.dump(pipe, "delivery_pipeline.joblib")
print("saved delivery_pipeline.joblib")
```

Run it. Then, in the terminal:

```bash
ls -l delivery_pipeline.joblib
```

```text
-rw-r--r--  1 you  staff  5002 ... delivery_pipeline.joblib
```

> **Say this:** "**Five thousand and two bytes.** Five kilobytes. Smaller than a photograph.
>
> And inside it: the median it fills holes with, the centre and width of five rulers, the names of every restaurant, day and weather it knows about, and the twenty-one numbers logistic regression learned. **Everything the model needs, and nothing it doesn't.**
>
> That file is the deliverable. Not the score — a score is a claim, and nobody can use a claim. Not the code — then they need your data, your Python and your library versions. **The file.**"

**Step 7 — ⚠️ SECOND DELIBERATE MISTAKE (2 min).** This one is **silent**, and it is the one they will actually make at home.

> **Say this:** "New file, `predict.py`. Load the artifact and predict on one order. But — I'll dictate the order slightly wrong on purpose and we'll see if it tells us."

```python
import joblib
import pandas as pd

pipe = joblib.load("delivery_pipeline.joblib")

one = pd.DataFrame([{"restaurant": "Napoli", "distance_km": 1.2, "items": 1,
                     "prep_minutes": 8.0, "order_hour": 12, "day_of_week": "Tue",
                     "driver_experience_months": 42.0}])
print(pipe.predict_proba(one)[:, 1])
```

**Ask before running:** *"Count the keys. How many should there be?"*

Eight. There are seven — `weather` is missing. Run it.

```text
Traceback (most recent call last):
  File "/Users/you/level3/term1/predict.py", line 9, in <module>
    print(pipe.predict_proba(one)[:, 1])
  ...
  File ".../sklearn/compose/_column_transformer.py", line 1085, in transform
    raise ValueError(f"columns are missing: {diff}")
ValueError: columns are missing: {'weather'}
```

> **Say this:** "**`columns are missing: {'weather'}`.** It names the column. By name. That's what the switchboard being name-based buys you.
>
> And think about what that error just did. It stopped at the door and named the column, instead of guessing or answering anyway. (A missing *column* can't slip through as zeros — the switchboard looks it up by name and complains. The silent case is a missing *value* in a column that exists, and we'll meet that in a few minutes.)
>
> **That error is a friend.** It refused to guess. Write that in the Bug Log with the word 'protected' in it."

Fix it by adding `"weather": "clear"`.

---

### 🎲 Their Turn — The Clean Room Test (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–10:** their own `predict.py`, from scratch, in a **new file**, with three orders typed in by hand — and the three probabilities checked for whether they tell a sensible story.
- **Minutes 10–15:** `clean_room_check.py`, and the three counts that have to be zero.
- **Minutes 15–20:** the last two experiments: **columns in a different order** (works), and **a restaurant that does not exist** (works, and shouldn't be trusted) — which becomes heading 7 of their card.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the two nesting envelopes · a pen · workbook pages 3.2–3.3 · the printed sheet of seven card headings · the Bug Log.

**On the screen:** `train_pipeline.py`, working, with `delivery_pipeline.joblib` on disk.

![The artifact crosses; the training code does not](../figures/fig-w03-3-artifact-crossing-to-a-clean-process.svg)
*Figure 3.6 — What "finished" looks like: the artifact crosses the wall and the training code does not.*

**The one rule that makes this work:** *`predict.py` is a new, empty file.* Not a copy of `train_pipeline.py` with the top deleted. **New. Empty.** Copying and deleting is exactly how a `fit(` survives, and the whole exercise is about it not surviving.

### Part 1 — the clean room (10 minutes)

> **Say this:** "Close `train_pipeline.py`. Actually close it — close the tab. You are not allowed to look at it again this lesson.
>
> New file, `predict.py`, completely empty. **Two imports, one load, three orders, one print.** And you have to type the eight column names from memory or from your Week 1 card three, not from the training file.
>
> Three orders, and make them tell a story: **one that should obviously be late, one that should obviously be fine, and one you genuinely can't call.**"

Their orders will differ from ours, and that is correct and good. Ours, for reference:

| # | The order | P(late) |
|---|---|---|
| 1 | CrustyBros, 8.5 km, 4 items, 22.0 min prep, 19:00 Friday, **storm**, driver 12 months | **0.968** |
| 2 | Napoli, 1.2 km, 1 item, 8.0 min prep, 12:00 Tuesday, clear, driver 42 months | **0.022** |
| 3 | SliceHouse, 4.2 km, 3 items, 14.0 min prep, 18:00 Saturday, rain, driver 42 months | **0.291** |

```text
CrustyBros     8.5 km  storm  19:00   P(late) = 0.968
Napoli         1.2 km  clear  12:00   P(late) = 0.022
SliceHouse     4.2 km  rain   18:00   P(late) = 0.291
```

**Then the check that matters, and it takes five seconds:**

> **Say this:** "Read your three numbers. **Do they tell a sensible story?** The nasty one high, the easy one low, the middling one in the middle?"

If a student's three numbers are all similar, or the wrong way round, **that is a finding and not a failure.** Something is wrong — usually a column name that does not match, so a value quietly became zeros. Have them print `orders` and read the column names against `NUMBER_COLUMNS` and `WORD_COLUMNS`.

**Say the general rule out loud:** *"three predictions you can check by common sense is the cheapest test in this subject, and almost nobody does it."*

### Part 2 — the count (5 minutes)

> **Say this:** "Now prove it's clean. Not 'I think it's clean' — **count.**"

```python
"""clean_room_check.py - is predict.py really a clean room?"""
text = open("predict.py").read()
print("occurrences of  fit(        :", text.count("fit("))
print("occurrences of  make_data   :", text.count("make_data"))
print("occurrences of  train_test  :", text.count("train_test"))
print("lines in predict.py         :", len(text.splitlines()))
```

```text
occurrences of  fit(        : 0
occurrences of  make_data   : 0
occurrences of  train_test  : 0
lines in predict.py         : 24
```

> **Say this:** "Three zeros. **That's the test.** Not a feeling — a count.
>
> Because think about what a `fit(` in that file would mean: the person you hand this to would need your data before they could use your model. And if they had your data, they wouldn't need your model.
>
> `open("predict.py").read()` just reads the file as text, and `.count("fit(")` counts how many times a bit of text appears. **Your program is reading your other program.** It's the same tool you'd use to count how many times 'the' appears in a book."

### Part 3 — two experiments, and heading 7 (5 minutes)

**Experiment one — columns in a different order.** Take order 3 and retype the eight keys in a completely different order.

```python
scrambled = pd.DataFrame([{"weather": "rain", "day_of_week": "Sat",
                           "restaurant": "SliceHouse",
                           "driver_experience_months": 42.0, "order_hour": 18,
                           "prep_minutes": 14.0, "items": 3, "distance_km": 4.2}])
print(round(pipe.predict_proba(scrambled)[0, 1], 3), "<- columns in a totally different order")
```

```text
0.291 <- columns in a totally different order
```

> **Say this:** "**Identical.** 0.291 either way. Because the switchboard looks columns up **by name** and never counts from the left. That is worth knowing, because a spreadsheet somebody emails you will have its columns in whatever order they felt like."

**Experiment two — a restaurant that does not exist.**

```python
order = {"restaurant": "SliceHouse", "distance_km": 4.2, "items": 3,
         "prep_minutes": 14.0, "order_hour": 18, "day_of_week": "Sat",
         "weather": "rain", "driver_experience_months": 42.0}

known = pd.DataFrame([order])
new = pd.DataFrame([{**order, "restaurant": "PizzaNova"}])

print("SliceHouse (in the training data) P(late) =",
      round(pipe.predict_proba(known)[0, 1], 3))
print("PizzaNova  (never seen before)    P(late) =",
      round(pipe.predict_proba(new)[0, 1], 3))
print("no error, no warning, difference =",
      round(pipe.predict_proba(new)[0, 1] - pipe.predict_proba(known)[0, 1], 3))
```

*(`{**order, "restaurant": "PizzaNova"}` means "the same eight keys, but with that one replaced" — a copy with one change, so nothing else can differ.)*

```text
SliceHouse (in the training data) P(late) = 0.291
PizzaNova  (never seen before)    P(late) = 0.308
no error, no warning, difference = 0.017
```

> **Say this:** "`PizzaNova` was never in the training data. So all five restaurant columns come out **zero** — as if this order came from **no restaurant at all** — and the model answers 0.308 with total composure. No error. No warning.
>
> Is that a bug? **No.** That's `handle_unknown="ignore"` doing exactly what we asked, and the alternative is a system that crashes the first time a new branch opens. It's the right choice.
>
> **It's a limitation.** And limitations go in writing, under heading seven, in your own words. Write it now: *'a restaurant the model has never seen becomes five zeros, and it answers anyway.'*"

### What "finished" looks like

- `train_pipeline.py` runs and prints `(1200, 8)` in, `(1200, 20)` out, and validation AUC **0.7541**.
- `delivery_pipeline.joblib` exists on disk, about **5002 bytes**.
- `predict.py` is a **new file**, contains **no** `fit(`, no `make_data`, no `train_test`, and prints three probabilities that tell a sensible story.
- The count has been run, and all three counts are zero.
- Page 3.2 has the paper arithmetic **5 + 5 + 7 + 3 = 20** written before the code ran.
- Heading 7 of the card has a real sentence in it, in the student's own words.
- 0.7541 is written under Week 2's box, with 0.2541 as the subtraction.
- Both of today's bugs are in the Bug Log — the wrong-order `TypeError` and the `columns are missing` one.

### Variation — easier

- **Cut the two routes to one.** Drop the word columns entirely and use the five number columns only. It still needs `ColumnTransformer`, `Pipeline` and `joblib`; the count becomes 5 in, 5 out; and the AUC drops but it still beats 0.5000 by a distance. **All four objectives survive.**
- **Cut `leak_demo.py` and the two medians.** The tidiness argument and the 0.709-to-1.000 demo carry the whole idea.
- **Give them `train_pipeline.py` already typed** and have them run it, read the shapes, and then do all of Parts 1 to 3 themselves. **Everything today is in `predict.py` and the card**, not in typing the switchboard.
- **One order instead of three** in `predict.py`. One is enough to prove the artifact loads.
- **Do the card orally**, with you writing. Seven headings, one sentence each, out loud, then they copy it. **The card is objective 4 and it must not be the thing that gets cut.**

**The copy-this-exactly scaffold.** Two files. Here is the whole of `train_pipeline.py`, cut down:

```python
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from make_data import make_deliveries

NUMBER_COLUMNS = ["distance_km", "items", "prep_minutes",
                  "order_hour", "driver_experience_months"]

df = make_deliveries(n=2000, seed=0).drop_duplicates().reset_index(drop=True)
y = df["late"]
X = df.drop(columns=["late", "order_id"])
X_rest, X_test, y_rest, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, stratify=y_rest, random_state=0)

number_route = Pipeline(steps=[("fill_holes", SimpleImputer(strategy="median")),
                               ("same_ruler", StandardScaler())])
prep = ColumnTransformer([("num", number_route, NUMBER_COLUMNS)])
pipe = Pipeline(steps=[("prep", prep),
                       ("model", LogisticRegression(max_iter=1000, random_state=0))])
pipe.fit(X_train, y_train)

print("columns in :", X_train.shape)
print("columns out:", prep.transform(X_train).shape)
print("validation ROC-AUC:", round(roc_auc_score(
    y_val, pipe.predict_proba(X_val)[:, 1]), 4))
joblib.dump(pipe, "numbers_only.joblib")
print("saved numbers_only.joblib")
```

```text
columns in : (1200, 8)
columns out: (1200, 5)
validation ROC-AUC: 0.7112
saved numbers_only.joblib
```

Then three questions and nothing else: **"how many columns came out? what did it score? and is that above 0.5000?"** Five, 0.7112, yes — by 0.2112.

*(Notice this makes a lovely accidental point: throwing away the three word columns costs 0.7541 − 0.7112 = **0.0429** of AUC. Restaurant and weather were carrying real information, and the five number columns were carrying most of it. A struggling student who spots that has done better than a fast one who did not.)*

### Variation — harder

None of these need syntax from a later week.

1. **How much is each route worth?** Build three pipelines — numbers only, words only, both — and report all three AUCs against the baseline.

```python
def num_route():
    return Pipeline(steps=[("fill_holes", SimpleImputer(strategy="median")),
                           ("same_ruler", StandardScaler())])

setups = {
  "numbers only": ColumnTransformer([("num", num_route(), NUMBER_COLUMNS)]),
  "words only":   ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS)]),
  "both":         ColumnTransformer([("num", num_route(), NUMBER_COLUMNS),
                                     ("cat", OneHotEncoder(handle_unknown="ignore"), WORD_COLUMNS)]),
}
for name, prep in setups.items():
    pipe = Pipeline(steps=[("prep", prep),
                           ("model", LogisticRegression(max_iter=1000, random_state=0))])
    pipe.fit(X_train, y_train)
    auc = roc_auc_score(y_val, pipe.predict_proba(X_val)[:, 1])
    print(f"{name:13s}: {auc:.4f}   columns out {prep.transform(X_train).shape[1]}")
d = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print(f"{'baseline':13s}: {roc_auc_score(y_val, d.predict_proba(X_val)[:,1]):.4f}")
```

```text
numbers only : 0.7112   columns out 5
words only   : 0.5982   columns out 15
both         : 0.7541   columns out 20
baseline     : 0.5000
```

   Then the real question: *"0.7112 and 0.5982. Add up how far each is above 0.5 — that's 0.2112 and 0.0982, which is 0.3094. But both together is only 0.2541 above. Where did the other 0.0553 go?"* **Because AUC gains do not add up like money** — the AUC measures how well the *whole ranking* of orders is ordered, and combining two sets of clues does not add their separate gains. (In this table the weather and the distance are generated independently, so it is *not* that they "say the same thing"; do not tell the student that. Columns that genuinely overlap would shrink the combined gain further, which is what Week 5 and Week 7 return to.) *(This is Week 5 and Week 7 arriving early, and it is the best question available today.)*

2. **Predict the artifact's size before saving it.** Have them list what must be inside: 1 median × 5 columns, 1 centre and 1 width × 5 columns, 15 category names, 20 coefficients and 1 intercept. That is roughly 36 numbers and 15 words. **So why is the file 5002 bytes rather than about 500?** Because a `.joblib` file also stores *what kind of object each thing is* so it can be rebuilt — the machinery, not just the numbers. **Most of those five kilobytes is scaffolding.**

3. **Save the model without the preparation, on purpose, and hand it to a partner** with the instruction "predict on this order". Watch what they do. Either they get a shape error, or — worse and more instructive — they hand it raw numbers and get a confident answer. **The best version of this week's lesson is having it happen to you.**

4. **Write the out-of-scope section properly.** Give them three proposed uses and have them accept or refuse each in writing, with a reason: *(a)* warn a customer their order may be late; *(b)* pay drivers less when they are late; *(c)* decide which restaurants stay on the app. The interesting one is **(c)**, and the argument is that `restaurant` is one of only eight columns and the model has no idea whether CrustyBros is slow because of its kitchen or because of where it happens to be.

5. **Break the artifact and see what happens.** Open `delivery_pipeline.joblib` in a text editor, change a few characters, save, and load it. The error is ugly and the lesson is short: **a binary artifact is not a document, and it has no way to tell you it has been damaged.** Which is why real systems store a checksum beside it — and that is Week 34.

6. **What is missing from the seven headings?** Give them the list and ask what a *real* card should also have that ours does not. Excellent answers: **a date**, **a version number**, **who to contact**, and **when it should be retrained.** All four are real, and all four are Week 34's subject. A student who says "when should this be thrown away?" has had an outstanding week.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

> **🧑‍🏫 If a student asks:** the tracebacks are longer again this week — ten lines for a missing column, thirteen for a wrong-order pipeline, and forty-four for a mistyped column name — because a `Pipeline` error travels up through every layer it passed on the way in. **The rule never changes: read the last line, then find the `File` line with your own filename in it.** And this week add a second habit: **the last line usually names a column or a shape. Find that name in your own code.**

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: columns are missing: {'weather'}` | "One of the eight columns I was trained on isn't in what you gave me." | A key missing or misspelled in a hand-typed order. | Add or correct it. **It names the column — search your file for that exact word.** This error protected you from a guess: it names the column and stops, rather than answering. (The *silent* all-zeros case is a missing value, not a missing column.) |
| `FileNotFoundError: [Errno 2] No such file or directory: 'deliverypipeline.joblib'` | "There is no file with that name here." | The underscore left out, or `predict.py` run from a different folder from the `.joblib`. | Match the name exactly, and `ls` to check the file is in the folder you are standing in. |
| `TypeError: All intermediate steps should be transformers and implement fit and transform or be the string 'passthrough' 'LogisticRegression(max_iter=1000, random_state=0)' (type <class 'sklearn.linear_model._logistic.LogisticRegression'>) doesn't` | "Every step but the last has to change data and pass it on. Your model doesn't." | Prep and model in the wrong order in the outer `Pipeline`. | Prep first, model last. **A model can only ever be the last step.** Note it did not complain until `fit`. |
| `ValueError: A given column is not a column of the dataframe` | "One of the column names in your route list isn't in the table." | A typo in `NUMBER_COLUMNS` or `WORD_COLUMNS` — `item_count` instead of `items`. | Print `list(X.columns)` and compare, character by character. **Unhelpfully, this one does not tell you which name.** |
| `ValueError: Input X contains NaN. LogisticRegression does not accept missing values encoded as NaN natively...` | "There are holes in what reached me, and I can't multiply by nothing." | The hole-filler left out of the number route, or a number column not covered by any route. | Put `SimpleImputer` back, or check all five number columns are in `NUMBER_COLUMNS`. **The message runs to several sentences of advice, and the first ten words are the whole story.** |
| `ValueError: could not convert string to float: 'Napoli'` | "You asked me to do arithmetic on a word." | The word columns bypassed the encoder — often `remainder="passthrough"` instead of a proper second route. | Give the word columns their own route with `OneHotEncoder`. |
| `ValueError: Cannot use median strategy with non-numeric data: could not convert string to float: '1.2 km'` | "You asked for the middle value of a column containing writing." | Units typed into a number cell in a hand-typed order — `"1.2 km"` instead of `1.2`. | `1.2`, no quotes and no unit. **Quotes make it writing; no quotes make it a number.** |
| `ValueError: Expected 2D array, got scalar array instead: array={'restaurant': 'Napoli', ...}` | "You gave me one dictionary. I need a table." | `pipe.predict_proba(one_dict)` — the `pd.DataFrame([...])` left off. | `pd.DataFrame([one_dict])`. **The square brackets matter: a list of one row, not a bare row.** |
| `KeyError: 'preprocessing'` | "There is no step with that name." | Asking for a step by a name you did not give it. | Use the name you wrote — `"prep"`. **You invented these names; they are not standard.** |
| `ModuleNotFoundError: No module named 'make_data'` | "There is no file called `make_data.py` anywhere I looked." | Wrong folder. Still the commonest error of the term. | `cd` and prove it with `ls`. |
| **No error**, but all three probabilities are almost the same | Nothing is broken. Your three orders probably differ in ways the model does not care about. | Only `items` or `day_of_week` changed between them. | Change **distance, weather and hour** — those are what actually move the answer. |
| **No error**, but one row's answer is slightly off and the value shows as `nan` | Nothing is broken. The *column* existed, so the switchboard was satisfied — only that row's *value* was missing, and `nan` became all zeros. | A key left out of **one** hand-typed order while the others have it. `pd.DataFrame` fills the gap with `nan`. | Print `orders` and look for `NaN`. **A missing column shouts; a missing value whispers.** |
| **No error**, but a probability is 1.000 or 0.000 | Nothing is broken *as far as scikit-learn knows*. | The preparation was skipped, or a raw number reached the model. **This is the week's disaster and it never announces itself.** | Go through the sealed pipeline, never the model directly. And treat a 1.000 as an alarm: **real data almost never justifies certainty.** |

### How to teach debugging without giving the answer

The escalation ladder from [orientation §9.2](00-orientation.md). Rungs two and three, ten full seconds apart.

1. **"Hm."**
2. **"Read me the last line of the error."**
3. **"What did you expect it to do?"**

This week adds a question you will use for the rest of the year:

> **"The error named something. Find that exact name in your own file."**

Almost every message today names a column, a shape, a step or a file. Getting a student to *search their own code for the word in the message* — rather than re-reading the whole file hoping — is the single biggest speed-up available in Level 3.

And the sentence for this week:

> **"A probability of 1.000 is not a good result. It is an alarm. Check what reached the model."**

---

## ❓ Questions Students Ask This Week

**"Why can't I just save the model and prepare the data myself in the other file?"**

You can, and it works, and it is the exact bug we spent seven minutes on at the start of the lesson.

Here is the honest version of the problem: to prepare a row yourself you need the median that filled the holes, the centre and width of five rulers, and the list of fifteen categories **in the right order.** Those are all *learned* numbers — they live inside the fitted preparation. So you either save them too (which is what saving the whole pipeline does, in one line) or you recompute them, and recomputing them from a different set of rows gives you different numbers and a quietly wrong answer.

And even if you got all of it right today, you now have two files that must be changed together forever. **The first time somebody changes one and not the other, nothing crashes.** That is not a risk worth taking to avoid one line of code.

**"Is 0.7541 good?"**

It is **0.2541 above the score of learning nothing**, which is the only form of that sentence that means anything — and it is why Week 2 existed.

Is it good enough to *use*? That is a different question and it is not answerable from the number alone. It depends on what happens when the model is wrong, and there are two very different kinds of wrong here that 0.7541 does not distinguish between. **Weeks 8 to 11 are entirely about that**, and by Week 11 the student will be able to say what a mistake costs.

What we can say today: the model is definitely learning something real about the world, because 0.2541 is far too big a gap to be luck on 400 rows. Compare with Week 2's twenty coin flips, where the *best of twenty* only managed 0.0853 above zero.

**"How does five kilobytes hold a whole model?"**

Because a model is a surprisingly small number of numbers.

Count them: 5 medians, 5 centres, 5 widths, 15 category names, 20 coefficients and 1 intercept. That is about 36 numbers and 15 short words — which is maybe 500 bytes of actual information. The other 4,500 bytes are the file describing **what kind of object each piece is**, so that `joblib.load` can rebuild the same structure rather than just handing you a pile of numbers.

Worth saying, because it is the thing that scales: the file is small because **logistic regression is small.** By Week 26 the student will build a network whose artifact is a few hundred kilobytes, and by the end of Level 4 they will read about models whose artifacts are hundreds of gigabytes. **The five kilobytes is not a property of the technique; it is a property of this particular model.**

**"What if I load the artifact on a computer with a different scikit-learn version?"** *(Nobody fully agrees, and here is why.)*

**This is the real weakness of the whole approach and it is worth being straight about**, because the disagreement is genuine and it is not going to be settled.

What actually happens: sometimes it works silently, sometimes it warns you, and sometimes it fails. A `.joblib` file does not contain scikit-learn — it contains instructions for rebuilding objects *out of* scikit-learn. If the library has changed the shape of those objects, the instructions no longer fit. So an artifact is only reliably loadable by the version that wrote it.

One camp says: **that is a fatal flaw, so never ship a pickle.** Export the numbers to a plain, documented format instead, and write the prediction code yourself. Then your artifact will still load in ten years. This is a strong argument and it is what safety-critical and long-lived systems actually do.

The other camp says: **the fix is to pin the version, not to abandon the tool.** Record which scikit-learn wrote the file, ship that requirement alongside it, and you get the enormous convenience of one line in and one line out. This is also a strong argument and it is what most working teams actually do.

The two answers conflict, and they conflict in real projects. What experienced people do is decide based on how long the artifact must live: months, and pin the version; decades, and export the numbers. **And either way, they write down which they chose.** That is heading 4 of the card, and it is why "where from" is on it.

What to tell a fourteen-year-old: **"the file is not a document, so write down what made it."**

**"Why is `handle_unknown="ignore"` a good idea if it gives us that PizzaNova problem?"**

Because the alternative is worse, and comparing the two is the whole answer.

Without it, the first order from a newly-opened restaurant crashes your prediction service. In the middle of a Friday evening. For every order from that restaurant, until somebody retrains the model. **A system that stops working when the world changes slightly is not a robust system.**

With it, that order gets a slightly worse prediction and everything keeps running. That is a much better failure: **degraded rather than dead.**

But — and this is the point of heading 7 — *degraded rather than dead* is only acceptable if **somebody knows**. An undocumented degradation is just a wrong answer. A documented one is a known limitation with a plan. **The setting is right and the card is what makes it right.**

**"Do professionals actually write model cards?"**

Some do and many do not, and it is worth being honest about the state of things rather than pretending.

The idea is recent — it comes out of work published in 2019 — and it caught on fastest exactly where you would expect: where a model affects people, and where somebody eventually has to answer a question about it. Big public model releases now usually come with one. A three-person team shipping an internal dashboard usually does not.

Here is the part worth saying to a fourteen-year-old, though. **Every single project that had a bad afternoon because a model was used for something it was never measured for would have been saved by heading 2.** The card is not for the person who built the model — they know all of it. **It is for the person who finds the file in eight months.** And that person is very often you.

**"Could I put my own model in the pipeline instead of logistic regression?"**

Yes, and it is one word, and it is exactly what Week 7 is about.

Swap `LogisticRegression(...)` for `DecisionTreeClassifier(random_state=0)` and everything else stays identical — same switchboard, same split, same `joblib.dump`. That is the deepest reason `Pipeline` is worth learning: **it makes the model the smallest, most easily replaced part of the system.**

The honest caveat: some models do not need some of the preparation. A decision tree does not care about rulers at all, because it only ever asks "is this value above or below?" — so `StandardScaler` does nothing for it either way. That is not a reason to remove it; it is a reason to understand what each part is for, which is Week 4 and Week 7.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The lesson becomes "we built a model!"** | It is the first model of the year and 0.7541 feels like the point | Count the lines out loud: the model is **three lines of forty-five.** Then point at the file: *"that's the deliverable. The model is the smallest part of it."* If the artifact does not get made, the lesson did not happen. |
| **`predict.py` is a copy of `train_pipeline.py` with the top deleted** | Copying is faster than typing, and it looks like the same result | This is the failure mode of the week and it is why we **count**. Run `clean_room_check.py` and let the number be the verdict. Then insist on a genuinely new file — the point is that the eight column names came from their card, not from the training file. |
| **The 0.709-to-1.000 demo gets a shrug** | 1.000 looks like a *good* number to somebody who has only seen scores | Say the sentence that reframes it: *"a probability of 1.000 means the model thinks there is no chance whatsoever that this pizza arrives on time. Is that a thing you believe?"* **Certainty is the alarm, not the achievement.** |
| **The count comes out `(1200, 19)` or `(1200, 22)`** | One of 5, 7, 3 was miscounted, or a name is misspelled | Do not fix it for them. Have them print the three `nunique()` calls and find which of the three numbers disagrees with their pen. **The debugging is the exercise.** |
| **The model card gets treated as homework padding** | It is writing, and writing feels like the bit that does not count | Point at the Week 1 index cards. **Three of the seven headings (3, 4's feature list and 6's metric) are already written, in their handwriting, from two weeks ago.** The card is not new work; it is the contract with two more weeks of facts in it. |
| **Heading 2 gets left blank or filled with "nothing"** | It is hard to imagine misuse of your own work | Give them the driver-pay example out loud and watch the reaction. Then: *"you can see why that's wrong. Will the person who finds this file in eight months?"* |
| **Somebody proposes running on the test pile "since we've got a model now"** | It is the obvious next step and it is one line | "Heading 5 of your card says *test pile not opened*. You're about to make your own card a lie in the same lesson you wrote it." Then: *"and what would you do with the number? Nothing is allowed to change because of it."* |
| **The wrong-order `TypeError` causes real confusion** | It fires at `fit`, not where the mistake was typed, and it is long | Point at the line number *first*, before reading the message. *"It's pointing at line 46. Where did I actually make the mistake?"* Line 41, where the pipeline was built. **An error's line number is where it was noticed, not where it was caused** — and that is a lesson worth more than the fix. |
| **The `.joblib` file is a different size on their machine** | A different scikit-learn version pickles slightly differently | Say so immediately and move on. **Nothing in the lesson depends on 5002.** If you act surprised, they will spend ten minutes chasing it. |
| **All three predictions come out nearly identical** | The three orders differ in things the model barely cares about | Have them change **distance, weather and hour** together. Then the useful question: *"which columns actually moved the answer?"* That is Week 5, arriving early and welcome. |
| **The class runs out of time before the card** | The card is last and the code is absorbing | **Move the card earlier if you have to cut.** Objective 4 is the one the student will still be using in Week 36. Cut the two Part-3 experiments instead; they are lovely and they are not the objective. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the word columns. One route, five number columns, 5 in and 5 out. AUC comes out at **0.7112**, still 0.2112 above the baseline, and every one of the four objectives survives intact.

**Cut:** `leak_demo.py`, `known_limits.py`, and both Part-3 experiments.

**Cut:** typing `train_pipeline.py`. Hand it over. **Everything today that matters is in `predict.py`, the count, and the card.**

**Skip the maths-free version of the maths:** the only arithmetic is the column count, and if it is shaky do it with objects rather than numbers. Put five coins on the table for the number columns. Then five, seven and three paper scraps for the restaurants, days and weathers. **Count the whole pile.** Twenty. A student who counts twenty objects has met objective 1 completely.

**Reteach — with the two envelopes and nothing else.** This is the whole lesson:

1. *"Two envelopes. Two things to remember. What if you forget one?"* A confident wrong answer, and no error.
2. *"Put one inside the other. How many things now?"* One.
3. *"Can you reach the inner one without opening the outer one?"* No.
4. *"That's a `Pipeline`. Now — I save the outer envelope in a drawer and go home. Tomorrow, what do I need?"* Just the envelope.
5. *"So what do I hand the pizza company?"* The envelope. **The file.**
6. *"And how do they know what it's for?"* They don't. **That's why you write the card.**

A student who leaves able to hold up one envelope and say *"there's no way to reach the model without going through the preparation, and this is the thing you hand over"* has succeeded, whether or not any Python ran.

**The copy-this-exactly scaffold.** The cut-down `train_pipeline.py` is in the Variations above, with its real output. Pair it with the shortest possible clean room:

```python
"""predict_one.py - the whole clean room, in nine lines."""
import joblib
import pandas as pd

pipe = joblib.load("numbers_only.joblib")

one = pd.DataFrame([{"restaurant": "CrustyBros", "distance_km": 8.5, "items": 4,
                     "prep_minutes": 22.0, "order_hour": 19, "day_of_week": "Fri",
                     "weather": "storm", "driver_experience_months": 12.0}])
print("P(late) =", round(pipe.predict_proba(one)[0, 1], 3))
```

```text
P(late) = 0.852
```

Then three questions and nothing else: **"is there any training in that file? where did the model come from? and does that probability make sense for a long stormy rush-hour delivery?"** No; the file; yes. That is objectives 2 and 3.

*(Note the number is 0.852 rather than 0.968, because this artifact only has the five number columns and so never learned that CrustyBros is slow or that storms are slow. **If a student notices the difference, that is a gift** — the three word columns were worth 0.116 on this one order and 0.0429 of AUC on the whole validation pile.)*

### If the student is flying

None of these need syntax from a later week.

1. **How much is each route worth?** (Variation-harder 1) — numbers only 0.7112, words only 0.5982, both 0.7541, and the question of where the missing 0.0553 went. **This is the best question available today.**
2. **Predict the artifact's size before saving it** (Variation-harder 2), then explain why 36 numbers take five kilobytes.
3. **Hand a partner a model with no preparation** (Variation-harder 3) and watch the disaster happen to somebody else. Then have both of them write it in the Bug Log.
4. **Write the out-of-scope section properly** (Variation-harder 4), including the genuinely hard third case about which restaurants stay on the app.
5. **Corrupt the artifact in a text editor** (Variation-harder 5) and read the resulting mess. Then the question: *"how could a file tell you it had been damaged?"* (A checksum. Week 34.)
6. **What is missing from the seven headings?** (Variation-harder 6) — date, version, contact, retraining schedule. A student who asks *"when should this file be thrown away?"* has understood something most professionals have not.

### If the student won't engage today

**Close the laptop and get out the two envelopes.** This week rescues itself well, because the core idea is physical and the second idea is writing about something they choose.

**Start with the envelopes, in ninety seconds:**

> **"Two things to remember, in order. What happens when you forget one?"**
>
> **"Now one inside the other. How many things?"**

Then hand over the card, and let them pick the model:

> **"Forget pizza. Pick something you'd actually build. A model that guesses whether you'll like a song. Whether a team wins. Whether a video is worth clicking."**

Then the seven headings, out loud, one at a time, about *their* thing:

> **"What's it for?"**
>
> **"What must it never be used for?"** *(This one always produces something good, because everybody can see the misuse of a thing they invented.)*
>
> **"What's one row?"**
>
> **"Where would the data come from?"**
>
> **"How would you split it?"**
>
> **"What number would you report, and what's the score of learning nothing?"**
>
> **"Where does it break?"**

That is objective 4 delivered with a pen in ten minutes, on something they chose, and it is the objective most likely to still be useful in five years. The second question is the one that always gets them.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the artifact (spoken, 60 seconds)**

> "You've finished. The pizza company asks for your work. **What exactly do you hand them, and what do you not hand them?**"

*Good answer:* "The `.joblib` file — the fitted pipeline, about five kilobytes — plus the model card. Not the score on its own, because a score is a claim nobody can use. Not the training code, because then they'd need my data and my library versions too."

**What to catch:** "the code". Push once: *"they run your code. Where does the data come from?"*

**Check 2 — why one object (spoken, 90 seconds)**

> "I've got a preparation object and a model object, and I promise I'll always remember to use them in the right order. **Convince me to weld them together anyway.**"

*Good answer:* "Because forgetting doesn't always crash — with numbers only, the same order came out 0.709 prepared and 1.000 unprepared, with no error at all. And the preparation learns things from data, so with two objects you can accidentally learn them from all 2000 rows instead of the 1200 training rows. Welded, there's no way in except through the preparation."

**Full marks needs the word *no error* or *silent*.** A student who says "it's tidier" or "it's good practice" has missed the argument entirely. Push: *"what does it look like when it goes wrong?"*

**Check 3 — the column count (spoken, 45 seconds)**

> "Eight columns go into the switchboard and twenty come out. **Where do the twenty come from?**"

*Good answer:* "Five number columns stay five. Then the three word columns become one column per value — 5 restaurants, 7 days, 3 weathers, which is 15. And 5 + 15 = 20."

**What to catch:** an answer that says "it makes more columns" without the three counts. **The three counts are the understanding**; 20 is just the answer.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks the deliverable is the score or the code. Cannot say what `Pipeline` is for beyond "it's neater". Cannot account for the twenty columns. |
| **2 — Emerging** | Builds the pipeline by copying, and it runs. Saves and loads the artifact when told to. Fills in the card's headings with short answers, mostly copied from the board. |
| **3 — Secure** | Assembles the two routes and can say which columns go down each and why. **Explains that welding makes forgetting impossible rather than unlikely, and names the silent 1.000 as the evidence.** Writes a `predict.py` with no training code in it and proves it by counting. Writes all seven headings with the real numbers. **This is the target.** |
| **4 — Strong** | Counts 5 + 5 + 7 + 3 = 20 on paper before running anything. Explains that the preparation *learns* numbers, and that this is a second reason for the weld. Reads `columns are missing: {'weather'}` and goes straight to the named column. Writes a heading 7 nobody dictated. |
| **5 — Exceptional** | Notices that the separate gains of numbers-only (0.2112) and words-only (0.0982) add up to more than the combined gain (0.2541), and can say that AUC gains do not simply add. Argues that `handle_unknown="ignore"` is the right choice *and* a documented limitation, holding both at once. Asks what is missing from the seven headings — a date, a version, when to retrain — without being prompted. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, and it's one file and one page of writing.
>
> **First, page 3.4 — finish `predict.py` so it runs from a cold start.** Cold start means: close everything, open a new terminal, and run only that one file. No training. Then run the count and paste all three zeros.
>
> **Second, page 3.5, and this is what I'm marking. `model_card.md`, seven headings.** A real markdown file, in the same folder as the artifact, and every heading gets a real answer for *this* model — with the real numbers. Heading 5 has to say whether the test pile was opened. Heading 6 has to give the number **and** the pile **and** the baseline. And heading 7 has to be **in your own words** — you found a real limitation in class, so write that one.
>
> **Third, page 3.6 — break it on purpose.** Delete one required column from an order in `predict.py`. Run it. **Paste the real error message**, all of it, and then write one line: *what did that error protect you from?* One line, and 'it stopped my program' is not the answer. The answer is about what would have happened if it hadn't.
>
> And **two Bug Log entries** from today: the wrong-order `TypeError`, and the missing-column one."

**Workbook pages:** 3.1, 3.2, 3.3 in class · **3.4, 3.5, 3.6** at home.

**Expected time:** 15 min finishing and cold-starting `predict.py` · 30 min on the model card · 10 min on the deliberate break and its one line · 5 min on the Bug Log and vocabulary. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** four things, and the third is the real one. **One — does `predict.py` contain zero `fit(`?** Search the file. This is binary. **Two — does heading 6 name the pile and the baseline?** "AUC 0.7541" earns half; "validation AUC 0.7541 against a baseline of 0.5000" earns all of it. **Three — is heading 7 in their own words, about something they actually saw?** A copied "it may not generalise" earns nothing; "a restaurant it's never seen becomes five zeros and it answers anyway" earns everything, and it is the sentence that proves they were paying attention in the last five minutes. **Four — does the one-line answer on 3.6 say what the error did *instead of guessing*?** The good answer is "it named `weather` and stopped instead of answering" (not "it would have become three zeros": that happens only for a missing value, not a missing column).

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 3.1 — Match the word to the thing

| Word | Description |
|---|---|
| **pipeline** | A single object holding several steps in a fixed order. `fit` fits them all in order; `predict_proba` runs them all in order. One name. |
| **ColumnTransformer** | A switchboard. Each route is a name, a treatment, and the columns it applies to — chosen **by name**, not by position. It glues the routes' outputs side by side. |
| **artifact** | The fitted thing, saved to disk as a file. Not the code that made it, and not the score it got. |
| **joblib** | The tool that writes a fitted Python object to a file and reads it back. `joblib.dump(...)` and `joblib.load(...)`. |
| **model card** | A short document that travels with the artifact, under fixed headings, saying what it is for and where it breaks. |
| **clean room test** | Closing the training file completely and predicting from a brand-new file that contains no training code at all — proved by counting. |

*Label the printed diagram below.*

```text
    8 columns
        |
   +----+----+
   |         |
  5 numbers  3 words        <- (a) the switchboard: routes chosen BY NAME
   |         |
 fill holes  one column      <- (b) 5 in, 5 out       (c) 3 in, 15 out
 one ruler   per value
   |         |
   +----+----+
        |
   (1200, 20)                <- (d) 5 + 5 + 7 + 3 = 20
        |
     the model               <- (e) can only ever be the LAST step
        |
   P(late)
```

**3.1(f) Why can a model only be the last step of a `Pipeline`?**
Because every step except the last has to **change data and pass it on** — the word scikit-learn uses is *transformer*. A model produces answers, not data, so nothing can follow it. Getting this wrong gives `TypeError: All intermediate steps should be transformers...`, **and only at `fit`, not when you build it.**

**3.1(g) One sentence: what is the difference between the artifact and the code?**
The artifact **already contains the learned numbers**, so it works in a fresh program with no data and no training; the code only produces those numbers if you also have the data, the libraries and the time.

**3.1(h) Why does welding the two objects together prevent leakage as well as forgetfulness?**
Because `pipe.fit(X_train, y_train)` fits the preparation on the training rows and **has no way to reach the other rows.** With two loose objects you can fit the preparation on all 2000 rows by accident, and it will not complain.

### Page 3.2 — Count the columns (in pen, before running)

| # | Question | The real answer |
|---|---|---|
| (a) | How many columns go into the switchboard? | **8** |
| (b) | How many are number columns? | **5** — `distance_km`, `items`, `prep_minutes`, `order_hour`, `driver_experience_months` |
| (c) | How many are word columns? | **3** — `restaurant`, `day_of_week`, `weather` |
| (d) | How many columns does route 1 produce? | **5.** Filling holes and rescaling never change the count |
| (e) | How many different restaurants? days? weathers? | **5 · 7 · 3** |
| (f) | How many columns does route 2 produce? | **5 + 7 + 3 = 15** |
| (g) | How many columns come out altogether? | **5 + 15 = 20** |
| (h) | How many **rows** come out? | **1200.** Unchanged — no rows were added or removed |
| (i) | Write the shape before and after | **(1200, 8) → (1200, 20)** |

**3.2(j) Where did the 5, the 7 and the 3 come from, and which Week 1 tool finds them?**
They are the counts of different values in each word column, and the tool is **`nunique()`** — the same one that caught `order_id` in Week 1. Real output:

```text
restaurants: 5  days: 7  weathers: 3
```

**3.2(k) Suppose a sixth restaurant opened and appeared in the training data. What would the shape become?**
**(1200, 21).** One more restaurant means one more column out of route 2: 6 + 7 + 3 = 16, and 5 + 16 = 21. *(Full marks for also noticing that the artifact would have to be rebuilt, and that the old artifact would silently give the new restaurant five zeros — which is heading 7.)*

### Page 3.3 — Which object gets dropped?

*One order: GreenLeaf, 7.4 km, 5 items, 22.0 minutes of prep, 19:00 Thursday, rain, driver 59 months.*

| # | Question | The real answer |
|---|---|---|
| (a) | What four numbers does the model receive if the order is prepared properly? | **1.793, 0.811, 2.008, 0.662** |
| (b) | What is P(late)? | **0.709** |
| (c) | Predict, in pen: what happens if the preparation is skipped? | Most students write "an error". **With these four raw numbers pasted in, it is not an error.** (On the whole raw table, with words and holes, it would be: `could not convert string to float`.) |
| (d) | What is P(late) with the raw numbers instead? | **1.000** |
| (e) | Do the subtraction | **1.000 − 0.709 = 0.291** |
| (f) | What error message do you get? | **None at all** in this demonstration: no error, no warning. |
| (g) | Why is the model *more* sure rather than just wrong? | The raw numbers are 4 to 30 times bigger than anything it trained on, so the answer is thrown off the end of its scale; these four all have positive weights, so it goes towards 1.000 (a negatively-weighted column such as driver experience would send it towards 0.000). Not "4 to 30 times" anything — the probability is not linear in the inputs. |

**3.3(h) The two-loose-objects version and the pipeline version scored the same validation AUC. What number, and why does that matter?**
**0.7541, both.** It matters because it proves the pipeline is **not a better model** — it is the same model with no way to reach it wrongly. Real output:

```text
validation ROC-AUC: 0.7541
```

**3.3(i) In one sentence: why is "I'll remember to prepare first" not good enough?**
Because remembering is something you can fail at silently, six months later, in a different file — and the shape of a welded object is something you cannot fail at at all.

**3.3(j) A probability of 1.000 came out and nothing crashed. What should you do?**
**Treat it as an alarm and check what reached the model.** Real data almost never justifies certainty about a pizza. *(Full marks for saying "check the preparation ran".)*

### Page 3.4 — Finish `predict.py` and cold-start it

Model answer, actually run:

```python
"""predict.py - loads the artifact and predicts. Contains no training code at all."""
import joblib
import pandas as pd

pipe = joblib.load("delivery_pipeline.joblib")

orders = pd.DataFrame([
    {"restaurant": "CrustyBros", "distance_km": 8.5, "items": 4, "prep_minutes": 22.0,
     "order_hour": 19, "day_of_week": "Fri", "weather": "storm",
     "driver_experience_months": 12.0},
    {"restaurant": "Napoli", "distance_km": 1.2, "items": 1, "prep_minutes": 8.0,
     "order_hour": 12, "day_of_week": "Tue", "weather": "clear",
     "driver_experience_months": 42.0},
    {"restaurant": "SliceHouse", "distance_km": 4.2, "items": 3, "prep_minutes": 14.0,
     "order_hour": 18, "day_of_week": "Sat", "weather": "rain",
     "driver_experience_months": 42.0},
])

prob = pipe.predict_proba(orders)[:, 1]

for i in range(len(orders)):
    row = orders.iloc[i]
    print(f"{row['restaurant']:13s} {row['distance_km']:4.1f} km  {row['weather']:6s} "
          f"{row['order_hour']:2d}:00   P(late) = {prob[i]:.3f}")
```

Real output:

```text
CrustyBros     8.5 km  storm  19:00   P(late) = 0.968
Napoli         1.2 km  clear  12:00   P(late) = 0.022
SliceHouse     4.2 km  rain   18:00   P(late) = 0.291
```

And the count:

```text
occurrences of  fit(        : 0
occurrences of  make_data   : 0
occurrences of  train_test  : 0
lines in predict.py         : 24
```

**Students' three orders will differ from these, and that is correct.** Mark the *shape* of the answer: three orders, three probabilities, and a story that makes sense.

**3.4(a) Do your three probabilities tell a sensible story? Say why in one line each.**
Model answer:

> *"0.968 — 8.5 km in a storm at seven in the evening from the slowest restaurant, with a driver who's been there twelve months. Everything is against it. 0.022 — 1.2 km, one item, lunchtime, clear, experienced driver. Nothing is against it. 0.291 — middling distance, rain, six in the evening. Genuinely could go either way, and 29% is close to the base rate of 28.75%, which is the honest answer for an order with nothing remarkable about it."*

**Mark for the third one.** Anybody can explain the extremes. Noticing that the middling order lands near the **base rate of 0.2875** is the strong answer.

**3.4(b) What do the three zeros prove?**
That the artifact really is the deliverable: `predict.py` does no training, never touches the data, and never splits anything. **Anybody with the 5,002-byte file can run it.**

**3.4(c) Why does the file have to be *new*, rather than a copy of `train_pipeline.py` with the top deleted?**
Because deleting is how a `fit(` survives — and because typing the eight column names from your own card, rather than copying them, is what proves the artifact is self-contained. *(A copied file that happens to pass the count is still fine; the point is that most of them do not.)*

**3.4(d) Retype one order with its eight keys in a completely different order. What happens?**

```text
0.291 <- columns in a totally different order
```

**Identical.** The switchboard looks columns up by name and never counts from the left.

### Page 3.5 — `model_card.md`, seven headings

This is the marked page. Model answer, as a real markdown file:

> # Model card — late pizza deliveries, v1
>
> ## 1. Intended use
> Flag an order as likely to be late **at the moment it is placed**, so that a dispatcher can act — reassign a driver, warn the customer, or hold the order. One probability per order.
>
> ## 2. Out-of-scope use
> **Not for decisions about drivers.** Not pay, not shift allocation, not ratings, not discipline. The model has one column about the driver (`driver_experience_months`) and seven that are about distance, weather, time and restaurant, so it mostly measures the *situation* and not the person. **Also not for deciding which restaurants stay on the app** — `restaurant` is one of eight columns and the model cannot tell whether a restaurant is slow because of its kitchen or because of where it happens to be.
>
> ## 3. Unit of prediction
> **One row is one pizza order.** One prediction per order, made at the moment the order is placed.
>
> ## 4. Training data
> 2,000 rows, generated by `make_data.py` with `seed=0`. Originally 2,020 rows; **20 exact duplicate rows removed** before splitting. 8 features: `restaurant`, `distance_km`, `items`, `prep_minutes`, `order_hour`, `day_of_week`, `weather`, `driver_experience_months`. Two columns excluded: `late` (that is y) and `order_id` (an ID — 2,000 different values in 2,020 rows). 106 cells of `driver_experience_months` (108 before the duplicates went) were empty and are filled with the **training** median (30.0).
> Written with scikit-learn 1.7.1, pandas 1.5.3, numpy 1.26.4, joblib 1.2.0 — **the artifact is only reliably loadable by these versions.**
>
> ## 5. Splits
> **1200 train / 400 validation / 400 test**, made by two stratified cuts with `random_state=0`. All three piles are **28.75% late** (345, 115, 115 — total 575). **The test pile has not been opened.**
>
> ## 6. Metrics
> **Validation ROC-AUC 0.7541**, against a `most_frequent` baseline of **0.5000** on the same 400 rows — so **0.2541 above the score of learning nothing.** Accuracy is deliberately not the headline: the baseline scores 0.7125 accuracy while catching 0 of the 115 late orders.
>
> ## 7. Known limitations
> - **A restaurant, day or weather the model has never seen becomes all zeros, and it answers anyway with no warning.** Measured: an identical order from `SliceHouse` gives 0.291, and from an unseen `PizzaNova` gives 0.308.
> - The data is generated, not collected, so its mess is *designed* mess. Real tables contain problems nobody planned.
> - 106 driver-experience values were filled in with a single median, so any pattern in *why* they were missing has been thrown away.
> - The model has never been measured on the test pile, so **every number here is a validation number** and is mildly optimistic.
> - No date and no version number beyond "v1" — see below.

**Mark against four things:**

1. **Are the real numbers in it?** 2000, 8, 1200/400/400, 0.2875, 0.7541, 0.5000. A card with no numbers is a mood.
2. **Does heading 5 say whether the test pile was opened?** This is the honesty line and it is the whole reason the card exists.
3. **Does heading 6 name the pile *and* the baseline?** "AUC 0.7541" is half an answer.
4. **Is heading 7 in their own words and about something they actually saw?** The PizzaNova result, or the generated data, or the 108 filled holes. **Copied generalities earn nothing.**

**3.5(a) Which three headings could you have written in Week 1?**
**3 (unit of prediction, Week 1's card one), 4 (the feature list, card three) and 6 (the metric, committed on card five, though the number came later).** Headings 1 and 2 (intended use, out-of-scope use) are *new* this week — Week 1's cards do not contain them, so a student who claims them has not been checking.

**3.5(b) Name something a real model card should have that our seven headings do not.**
Any of: **a date**, **a version number**, **who to contact**, **when it should be retrained**, **who is accountable for it**, **what data it must never be run on**. All are real; all are Week 34's subject. **The best answer is "when should this file be thrown away?"**

### Page 3.6 — Break it on purpose

*Delete a required column from **all** the orders in `predict.py` and run it.*

Real output, the whole thing, with `"weather"` removed from all three orders:

```text
Traceback (most recent call last):
  File "/Users/you/level3/term1/predict.py", line 19, in <module>
    prob = pipe.predict_proba(orders)[:, 1]
  File ".../sklearn/pipeline.py", line 904, in predict_proba
    Xt = transform.transform(Xt)
  File ".../sklearn/utils/_set_output.py", line 316, in wrapped
    data_to_wrap = f(self, X, *args, **kwargs)
  File ".../sklearn/compose/_column_transformer.py", line 1085, in transform
    raise ValueError(f"columns are missing: {diff}")
ValueError: columns are missing: {'weather'}
```

*(Your paths and line number will be your own. The middle three `File` lines are inside scikit-learn.)*

> **⚠️ Watch out — and this is the best accident in the week.** If a student deletes `weather` from only **one** of the three orders, **there is no error at all.** `pd.DataFrame` builds the column anyway and fills the missing entry with `nan`, `OneHotEncoder` turns `nan` into three zeros, and the answer comes out. Real output, with `weather` removed from the Napoli order only:
>
> ```text
> CrustyBros    weather=storm  P(late) = 0.968
> Napoli        weather=nan    P(late) = 0.039
> SliceHouse    weather=rain   P(late) = 0.291
> ```
>
> **Napoli moved from 0.022 to 0.039 and nothing complained.** The column existed, so the switchboard was satisfied; only its *contents* were missing. **If this happens to a student, stop the class and show everybody** — it is the whole theme of the week arriving by accident, and it is better than anything you could have planned.

**3.6(a) One line: what did that error protect you from?**

Model answer:

> *"It stopped the program and named `weather`, instead of guessing or answering anyway. A column that is missing entirely can't slip through as zeros — it's a missing value inside a column that exists that does that."*

**Mark for "named the column", "refused to guess" or "stopped instead of answering"; a student who contrasts it with the silent missing-value case (3.6(d)) has gone further.** "It stopped my program" alone is the wrong shape of answer: the error is the *good* outcome, and the answer has to say what it did *instead of* guessing. Do not reward a claim that the column would have become three zeros: that happens only for a missing value (3.6(d)), not a missing column.

**3.6(b) Why does the error name the column?**
Because the `ColumnTransformer` selects columns **by name**, so it knows exactly which name it was looking for and could not find. *(Contrast with `ValueError: A given column is not a column of the dataframe`, which does not tell you which one — that is the same class of bug with a much worse message, and it is in the clinic.)*

**3.6(c) Now try it with a *number* column deleted instead. Same message?**
Yes, same shape, different name. Deleting `driver_experience_months` from all three orders gives:

```text
ValueError: columns are missing: {'driver_experience_months'}
```

**All eight are required, and the switchboard does not care which kind of column it is.**

**3.6(d) Delete the column from just ONE order instead of all three. What happens, and why is it worse?**
**Nothing happens** — no error, and the Napoli order's probability moves from **0.022 to 0.039**. `pd.DataFrame` still creates a `weather` column because two of the three orders have one; the missing entry becomes `nan`; and `OneHotEncoder` turns `nan` into three zeros, exactly as it does for a restaurant it has never seen. **The switchboard checks that the column *exists*, not that it has anything in it.**

It is worse because **it is silent**, and silent is this whole week's subject. *(Full marks for connecting it to the PizzaNova result: an unknown value and a missing value both become all zeros, and neither says so.)*

**3.6(e) Your two Bug Log entries for today.**

Model, two rows:

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| `TypeError: All intermediate steps should be transformers and implement fit and transform...` | Every step but the last has to change data and pass it on; a model can only be last. | Prep and model swapped in the outer `Pipeline`. | Prep first, model last. **And note: it did not complain when I built it, only when I fitted it.** |
| `ValueError: columns are missing: {'weather'}` | One of the eight columns the model was trained on wasn't in what I handed it. | A key left out of a hand-typed order. | Add it. **This error protected me — it named the column and stopped instead of guessing.** |

### Answers to every question posed in the lesson

- *"Two objects, right order. What if you forget one?"* → A confident, wrong answer, with no error at all. 0.709 becomes 1.000.
- *"Why is the model more *sure* rather than just wrong?"* → The raw numbers are 4 to 30 times bigger than anything it trained on, and all four push towards late, so the sum is thrown far up the scale (negative weights would throw it down).
- *"How many things to remember with one envelope inside another?"* → One.
- *"So is the pipeline a better model?"* → No. Identical AUC, 0.7541 either way. It is the same model with no way to reach it wrongly.
- *"What would you hand the pizza company?"* → The `.joblib` file and the card.
- *"Eight columns in. How many out?"* → 20.
- *"Where did the 5, the 7 and the 3 come from?"* → `nunique()` on each word column.
- *"Does the row count change?"* → No. 1200 in, 1200 out.
- *"What does the preparation *learn*?"* → The hole-filling median (30.0 on train, 29.0 on all 2000) and the centre and width of each ruler (mean distance 3.4591 on train, 3.5193 on all 2000).
- *"The wrong way changes AUC by 0.0001. So why care?"* → Because it is invisible here, and we cannot know it will be invisible on the next dataset.
- *"Why not just remember to prepare first?"* → Because remembering is a thing you can fail at, and a welded shape is not.
- *"The columns are chosen by name. Does the order of columns in my table matter?"* → No. The scrambled order gives the identical 0.291.
- *"When does the wrong-order pipeline complain — at build or at fit?"* → At `fit`. Building a wrong pipeline is silent.
- *"Count the keys. How many should there be?"* → Eight.
- *"What does `columns are missing: {'weather'}` protect you from?"* → From a guess: it names the missing column and stops instead of answering. (A missing *value* is the silent case; a missing *column* is not.)
- *"Is 0.7541 good?"* → It is 0.2541 above the score of learning nothing, which is the only form of the sentence that means anything.
- *"Five thousand and two bytes. What is inside?"* → 5 medians, 5 ruler centres, 5 ruler widths, 15 category names, 20 coefficients and 1 intercept — plus the machinery to rebuild the objects.
- *"Do your three probabilities tell a sensible story?"* → 0.968 for the nasty one, 0.022 for the easy one, 0.291 for the middling one — and 0.291 sits near the base rate of 0.2875.
- *"PizzaNova was never in the training data. Is that a bug?"* → No. It is `handle_unknown="ignore"` doing what we asked, and it is a limitation that belongs in writing.
- *"What do the three zeros prove?"* → That `predict.py` does no training, never touches the data and never splits anything.

---

## 🔮 Next Week Preview

Term 1 has spent three weeks on decisions, piles and shapes, and next week goes **inside one of the boxes we used today without opening.** Week 4 is called *Same Number, Different Ruler*, and it is the week `StandardScaler` and `OneHotEncoder` stop being named parts and start being arithmetic you can do by hand. It also brings the term's **first new maths**, and it is gentle: the **standard deviation**, taught as *"the typical distance of a value from the mean"*, then the **z-score**, which is just `(value − mean) ÷ sd`. Both get worked all the way through on five numbers written on paper — **2, 4, 6, 8, 100** — and that fifth number is chosen on purpose, because it is what makes the whole idea visible in about ten seconds.

The payoff is that today's mystery numbers become readable. That order came out as **1.793, 0.811, 2.008, 0.662**, and by the end of next week the student will be able to say exactly where 1.793 came from: 7.4 kilometres is 3.9 kilometres above the training mean of 3.4591, and the typical distance from that mean is 2.1983, so **3.9409 ÷ 2.1983 = 1.793** — this order is a bit under two typical distances further than usual. They will also meet `MinMaxScaler` as the other common choice, see one column become five with `OneHotEncoder`, and meet `OrdinalEncoder` and the trap it sets: giving `clear = 0, rain = 1, storm = 2` quietly tells the model that a storm is twice a rain, which is a claim nobody made.

**Prep early:** three things. **Keep `make_data.py` and `delivery_pipeline.joblib`** — next week reaches inside that artifact and reads the actual numbers out of it, which is much more satisfying than making new ones. **Keep the model card open in an editor**, because next week's Week 4 result will need heading 4 amending, and a card that gets amended is a card the student believes in. And **get a ruler and a strip of squared paper**, because the five numbers 2, 4, 6, 8, 100 get plotted by hand on two different scales side by side, and the moment where the 100 shoves everything else into one column is worth more than any amount of explaining.

---

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Week 4 ➡](week-04.md) · [Student Guide](../student-guide/week-03.md) · [Workbook](../workbook/week-03.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
