# 🔎 Level 2 Capstone — Data Detective

**Level 2 · Capstone · ~10 hours · Prereqs: all nine Level 2 modules, especially [M6](module-06-pandas-tables.md) (cleaning + the cleaning log), [M7](module-07-visualizing-data.md) (five honest charts), [M8](module-08-first-model-knn.md) (X, y, the split), [M9](module-09-trees-lines-and-overfitting.md) (three models, three metrics, the train/test gap)**

[⬅ Module 9](module-09-trees-lines-and-overfitting.md) · [Level 2 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md)

---

## 🎯 What You'll Be Able To Do

By the end of this capstone:

1. **You will be able to** turn a question you actually care about into a dataset you built yourself — 100+ rows, named columns, one target column — and defend every column as something a person could really measure.
2. **You will be able to** clean a messy table in pandas and produce a **numbered cleaning log** where every single change has a reason next to it, so a stranger could redo your work and land on the same table.
3. **You will be able to** answer your question with **five labelled charts arranged in narrative order**, each with a one-sentence caption that states the finding rather than the topic.
4. **You will be able to** train three genuinely different models on **one fixed train/test split**, put them in a results table with the metric named, and say which one you would actually use and why that may not be the highest-scoring one.
5. **You will be able to** write a "what I got wrong" section that is specific, numeric, and uncomfortable — the section that turns a school project into a piece of real work.
6. **You will be able to** state, in one paragraph, whose data this is and what a wrong prediction would cost a real person.

---

## 🪝 The Brief

A local youth centre is deciding something with money attached. Maybe it's *how many snacks to order for Friday club*. Maybe it's *whether to move cricket practice earlier because kids arrive late*. Maybe it's *which of two after-school clubs to keep*.

The person deciding has no data. They have a strong opinion, three anecdotes, and a budget.

**You are going to be the one who shows up with a table.**

Not a table someone handed you. A table you built, one row at a time, about something in your own life — 100+ rows of it. Then a cleaning log, five charts, three models, and one honest sentence about how sure you are.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │                                                                    │
   │   THE FOUR THINGS THAT MAKE THIS A REAL PROJECT                    │
   │                                                                    │
   │   1.  The data is YOURS. You collected it. You know what every     │
   │       row means, because you were there when it happened.          │
   │                                                                    │
   │   2.  Every change you made to it is written down with a reason.   │
   │       Anyone can rerun your work and land in the same place.       │
   │                                                                    │
   │   3.  The score you report is measured on rows the model never     │
   │       saw. Once. You do not get to try again.                      │
   │                                                                    │
   │   4.  There is a section, in your own handwriting, titled          │
   │       "what I got wrong". And it is not empty.                     │
   │                                                                    │
   └────────────────────────────────────────────────────────────────────┘
```

### Why this matters

Every module in this level built one piece of one thing. This is the thing.

| Module | The piece it gave you | Where it shows up in the notebook |
|---|---|---|
| 1 | Variables, types, f-strings, tracebacks | Every cell. You will read a lot of tracebacks. |
| 2 | Loops and conditionals | The collection script, the depth loop |
| 3 | Functions and lists | One `report()` function used for every model |
| 4 | Dicts, list-of-dicts, CSV round trip | How your raw rows get from paper into a file |
| 5 | numpy arrays, masks, axis | `np.sqrt`, boolean filters, derived columns |
| 6 | DataFrames, cleaning, `groupby`, the log | Sections 2 and 3 of the notebook |
| 7 | Five chart types, labels, honest axes | Section 4 |
| 8 | X, y, `train_test_split`, scaling, leakage | Section 5 |
| 9 | Trees, lines, MAE/RMSE/R², the train/test gap | Sections 5 and 6 |

And here is the professional truth underneath it, the same one Level 1 told you and this level proves: **the model is about 15% of the work.** The other 85% is the question, the collection, the cleaning log, the charts, and knowing what you got wrong. Nobody teaches the 85%. You are about to build it.

---

## 🔎 Choosing Your Question

Spend real time here. Two hours of collecting the wrong data cannot be rescued by four hours of good modelling.

### The four tests a good capstone question passes

```
   TEST 1 — THE CARE TEST
   Will you still want the answer in four weeks?
        ✅ "How much of my day actually goes to homework vs screens?"
        ❌ "Something about the weather I guess."

   TEST 2 — THE 100-ROW TEST
   Can you honestly get 100+ rows in about two hours, without
   asking anyone for permission you can't get?
        ✅ 100 YouTube videos from your own watch history
        ❌ 100 classmates' exam marks

   TEST 3 — THE TARGET TEST
   Is there ONE column you'd like to predict from the others?
        ✅ minutes (a number)  ·  late / on-time (a category)
        ❌ "I just want to explore" — that's a chart project, not a model project

   TEST 4 — THE HONEST-FEATURE TEST
   Could you know every feature BEFORE the target happens?
        ✅ predicting journey time from distance, mode, weather
        ❌ predicting journey time from "what time I arrived"  ← that IS the answer
```

Test 4 is the one that sinks projects. Module 8 called it **leakage**, and it feels amazing while it's happening: your model scores 99% and you feel like a genius. Then you notice one of your features already contains the answer.

### Question shapes that work well

| Question | Target column | Features you'd collect | Rows in ~2 h | Watch out for |
|---|---|---|:--:|---|
| **How long does my journey to school take?** | `minutes` (number) | distance, mode, rain, departure hour, day | 100 (5/day × 20 days, or log a family's trips) | You need real variety in mode — 100 identical walks teach nothing |
| **How many views will a video get?** | `views` (number) | duration, upload hour, title length, has-a-face thumbnail, channel size | 120 in one sitting from a channel page | Views depend on time-since-upload. Use only videos older than 30 days. |
| **How long will I actually watch a video?** | `watch_minutes` | duration, category, time of day, who recommended it | 100 over two weeks | Be honest in the log. Rounding 3 min up to 5 is data corruption. |
| **What does a cricket innings score?** | `runs` (number) | overs faced, batting position, ground, opposition strength, first/second innings | 100 from your own scorebook or a public league table | Scorebooks have gaps. Gaps are a *finding*, not a problem — log them. |
| **How much does a shop trip cost?** | `total_rupees` | number of items, has-a-list, day of week, shopper, store | 100 receipts over a month (ask first!) | Prices drift over months. Note the date range in the data card. |
| **Will the bus be late?** | `late` (category) | scheduled time, rain, day of week, route | 100 over 5 weeks | Two classes → state the baseline (the majority-class %) |
| **How many hours did I sleep?** | `hours` (number) | bedtime, screen-off time, day of week, exercise minutes, caffeine | 100 = ~14 weeks (start early!) or one row per person per night for a family | Slow to collect. Start this in week 14 if you want it. |
| **How long does a chore take?** | `minutes` | chore type, who did it, how long since last time, helpers | 100 over three weeks | Get every family member's permission first |

> 🔑 **Strong recommendation: pick a *number* target (regression).** All three Level 2 models — kNN, decision tree, linear regression — work on numbers, and your three metrics (MAE, RMSE, R²) all apply. A category target is allowed, but linear regression can't do it, and the third-model workaround is fiddly (see the sidebar in the worked solution).

### Questions to avoid, and why

| Don't do | Why not |
|---|---|
| Anything predicting things **about people** — their marks, their mood, whether they're "good at" something | You cannot collect a fair sample of humans, the labels are opinions, and someone gets hurt. Level 1 Module 9 explained this properly; it is a hard rule here. |
| Data you took from friends **without asking**, or scraped from someone's private account | Milestone 6 asks whose data this is. If the honest answer is "not mine and they don't know", stop. |
| A dataset you **downloaded** from Kaggle | You will learn a tenth as much. The whole point is that you know what every row means because you were there. (Exception: a *public* dataset like a published league table or a government open-data CSV is fine if you collect and clean it yourself.) |
| Fewer than 100 rows | With a 20% test set, 60 rows leaves you 12 test rows. One row is 8 percentage points. You cannot conclude anything. |
| A target you can't measure consistently | If "was it a good day?" means something different on Tuesday than on Friday, your target column is noise. |
| Something needing medical, legal or safety judgement | Being wrong costs too much and you cannot test it honestly. |

> ⚠️ **The 100-row floor is not decoration.** Below 100 rows, an 80/20 split gives you under 20 test rows, and every honest thing you'd like to say ("this model is better than that one") becomes unsayable. Module 8 made you state the test-set size next to every accuracy for exactly this reason. If your idea can only get 60 rows, find a way to get 40 more — a longer window, more people logging, or a coarser row (one row per *day* instead of per *event*).

---

## 📋 Requirements

### 🟥 Must-have — without all of these, the capstone is not done

| # | Requirement | Evidence in the notebook |
|:--:|---|---|
| M1 | A **stated question** in one sentence, at the top, before any code | Section 1 |
| M2 | **100+ rows** you collected or assembled yourself, with **4+ feature columns and 1 target column** | `df.shape` printed, showing `(100+, 5+)` |
| M3 | A **raw file saved and never edited** (`data/raw.csv`), plus a separate clean one | Both files exist; the notebook reads `raw.csv` |
| M4 | A **data card**: what each column means, its units, who collected it, over what dates | A markdown cell, before the cleaning |
| M5 | A **numbered cleaning log** — every change, with a *reason* — and a printed before/after `shape` | Section 3 |
| M6 | **Five labelled charts** in narrative order, each with a title, axis labels **with units**, and a one-sentence caption stating the finding | Section 4 |
| M7 | **One `train_test_split`, created once**, with `random_state` set, used by every model | Section 5, one cell, near the top |
| M8 | A **baseline model** (`DummyRegressor` / `DummyClassifier`) scored on the same split | In the results table |
| M9 | **Three genuinely different models** trained and scored on that one split | In the results table |
| M10 | A **results table** with the metric **named in the column header**, and both a train score and a test score for every model | Section 5 |
| M11 | A **"what I got wrong"** section with at least three specific, numeric admissions | Section 6 |
| M12 | A paragraph on **whose data this is** and **what being wrong would cost a real person** | Section 7 |
| M13 | The notebook **runs top to bottom without errors** on a fresh kernel | Restart & Run All, then say so |

### 🟨 Should-have — this is what separates a good notebook from a passing one

| # | Requirement | Why it lifts the project |
|:--:|---|---|
| S1 | A **written prediction** of what you expect to find, made *before* you look at the data | Stops you from discovering whatever you already believed |
| S2 | The **five worst predictions inspected by hand** — actual, predicted, error, and a guess at why | This is the single most grown-up thing in the whole project |
| S3 | A **model-complexity curve** (train and test score vs `max_depth`) with the overfitting point marked | Module 9's headline graph, on *your* data |
| S4 | The **units stated everywhere** — "MAE = 2.7 **minutes**", never a bare number | A metric without units is a rumour |
| S5 | **Scaled vs unscaled kNN** compared, with a sentence explaining the result you actually got | Module 8's lesson, tested rather than recited |
| S6 | One `groupby` table answering a question the charts raised | Charts ask questions; `groupby` answers them |
| S7 | An explicit sentence about **how much one test row is worth** ("with 24 test rows, one row moves accuracy by 4.2 points") | Turns a number into an honest number |

### 🟩 Could-have — pick at most two, only after every Must-have is done

| # | Idea |
|:--:|---|
| C1 | **Collect a second batch later** (a different week, a different person) and test the frozen model on it. Real-world drift, measured. |
| C2 | An **engineered feature** you invented — `minutes_per_km`, `is_weekend`, `days_since_last` — with a before/after score showing whether it helped |
| C3 | A **feature-importance** readout (`tree.feature_importances_`) compared against your own guess made beforehand |
| C4 | A **residual plot** — error on the y-axis against the prediction on the x-axis — and what its shape tells you |
| C5 | **Two thresholds**: if your target is a number, also build the category version (`late = minutes > 25`) and compare which framing is more useful |
| C6 | A **one-page printed summary** for the actual person who'd make the decision, with no code on it |

> ⚠️ **The trap.** Every year somebody spends five hours making beautiful charts and twenty minutes on the split. The rubric weights honesty above polish, deliberately. Finish all thirteen Must-haves before you change a single colour.

---

## 🗺️ Milestone Plan

Seven milestones, about **10 hours**. The order is not negotiable: you cannot clean data you haven't collected, and you cannot hold out rows after training.

```
   ┌────┬──────────────────────────────────┬─────────┬────────────────────────┐
   │ #  │  MILESTONE                       │  TIME   │  YOU END UP HOLDING    │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 1  │  Lock the question, design the   │  45 min │  A filled-in plan +    │
   │    │  columns, write the data card    │         │  a written prediction  │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 2  │  Collect 100+ rows → raw.csv     │ 120 min │  data/raw.csv          │
   │    │  (and then never touch it again) │         │  (read-only, forever)  │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 3  │  Clean in pandas + the numbered  │  90 min │  data/clean.csv +      │
   │    │  cleaning log                    │         │  a log with reasons    │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 4  │  Five charts in narrative order  │ 105 min │  5 PNGs + 5 captions   │
   │    │  with captions                   │         │  that read as a story  │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 5  │  ⚠️ HARDEST: one split, four     │ 120 min │  A results table with  │
   │    │  models, one results table       │         │  the metric named      │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 6  │  "What I got wrong" + the        │  60 min │  Three numeric         │
   │    │  ethics paragraph                │         │  admissions + 1 para   │
   ├────┼──────────────────────────────────┼─────────┼────────────────────────┤
   │ 7  │  Assemble as a story, Restart &  │  60 min │  One notebook a        │
   │    │  Run All, read it out loud       │         │  stranger can follow   │
   └────┴──────────────────────────────────┴─────────┴────────────────────────┘
                                             ─────────
                                             600 min = 10 h exactly
                                             (add 60 min slack. You will need it.)
```

---

### ☐ Milestone 1 — Lock the question (45 min)

- [ ] Run all four tests (Care / 100-Row / Target / Honest-Feature) on your idea, **in writing**
- [ ] Write the question as **one sentence** with a question mark at the end
- [ ] Design the columns: name, type, units, and *how you will measure it*
- [ ] Name your **target** column and say whether it's a number or a category
- [ ] Write your **prediction** — what you expect the answer to be — and date it (Should-have S1)
- [ ] Write the **data card**

**Template — paste this into the first markdown cell of your notebook:**

```
# DATA DETECTIVE — <your title>

## The question
   ____________________________________________________________?

## My prediction, written on <date>, BEFORE collecting anything
   I expect ______________ to be the strongest driver, because ____________.
   I expect the model to be off by roughly ______ <units> on average.

## The columns
   | column        | type   | units  | how I measure it                    |
   |---------------|--------|--------|-------------------------------------|
   | ____________  | number | ______ | ___________________________________ |
   | ____________  | text   |   —    | ___________________________________ |
   | ____________  | 0/1    |   —    | ___________________________________ |
   | ____________  | number | ______ | ___________________________________ |
   | ____________  | number | ______ | ___________________________________ |  ← TARGET

## Data card
   Collected by:  ______________
   Between:       ______ and ______
   How:           ______________________________________________
   Who is in it:  ______________________________________________
   Permission:    I asked ____________ on ______ and they said yes.
   What is NOT in it: __________________________________________
```

> That prediction line matters more than it looks. Writing down what you expect *before* you look stops you from "discovering" the thing you already believed. Scientists call this **pre-registration**, and it is the cheapest honesty upgrade in existence.

---

### ☐ Milestone 2 — Collect 100+ rows (120 min)

- [ ] Decide the **unit of a row** in one sentence: "one row = one ______"
- [ ] Collect on paper or in a spreadsheet **as it happens** — not from memory a week later
- [ ] Aim for **120 rows**, so you can throw some away in cleaning and still clear 100
- [ ] Deliberately collect **variety** in every feature, not 100 near-identical rows
- [ ] Save as `data/raw.csv` and then **stop touching it**
- [ ] Print `df.shape` and `df.head()` and paste the output into the notebook

**The variety checklist — run it before you stop collecting:**

```
   □ Every category value appears at least 10 times
     (if "cycle" appears 3 times, the model learns nothing about cycling)
   □ Your numeric features actually spread out
     (if every distance is 2.0–2.3 km, distance can't explain anything)
   □ At least a few genuinely awkward rows — the day it poured,
     the one that took twice as long. Those rows earn their keep.
   □ No row where you guessed the target. Missing is better than invented.
```

**Writing the raw file — the Module 4 way:**

```python
import csv

rows = [
    {"distance_km": 1.2, "mode": "walk", "rain": 0, "depart_hour": 8, "minutes": 17.5},
    {"distance_km": 3.4, "mode": "bus",  "rain": 1, "depart_hour": 8, "minutes": 21.0},
    # ... 118 more, typed or appended by a small logging script
]

with open("data/raw.csv", "w", newline="") as f:              # newline="" avoids blank lines
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(len(rows), "rows written")
```

> ⚠️ **The one mistake you cannot undo.** Editing `raw.csv` by hand — "I'll just fix that typo in the spreadsheet" — destroys reproducibility, because the fix now exists nowhere in your code. Every repair happens in pandas, in a cell, with a log line. Make the file read-only if you have to: `chmod 444 data/raw.csv` on macOS/Linux.

---

### ☐ Milestone 3 — Clean it, and log every change (90 min)

- [ ] `df = pd.read_csv("data/raw.csv")` — always from raw
- [ ] `print(df.shape)` **before**
- [ ] Run `df.info()` and `df.describe()` and read them properly
- [ ] Find and fix: missing values · wrong dtypes · duplicate rows · inconsistent spellings · impossible values
- [ ] For **every** fix, append a numbered line to `CLEANING_LOG` with a reason
- [ ] `print(df.shape)` **after**, and print the log
- [ ] Save `data/clean.csv`

**The pattern to use — a log that lives in the code:**

```python
import pandas as pd

df = pd.read_csv("data/raw.csv")
before = df.shape
CLEANING_LOG = []                      # every entry: what I did, and WHY

def log(action, reason):
    """Record one cleaning decision so it ships with the results."""
    CLEANING_LOG.append(f"{len(CLEANING_LOG) + 1}. {action}  —  {reason}")

# --- 1. duplicates -------------------------------------------------------
dupes = df.duplicated().sum()
df = df.drop_duplicates()
log(f"Dropped {dupes} exact duplicate rows",
    "I logged 3 journeys twice on 14 Sept when my phone re-synced.")

# --- 2. inconsistent spellings ------------------------------------------
df["mode"] = df["mode"].str.strip().str.lower()
log("Lower-cased and stripped 'mode'",
    "'Walk', 'walk ' and 'walk' were three groups in value_counts(); they are one thing.")

# --- 3. a number that arrived as text -----------------------------------
df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")
log("Converted 'minutes' with to_numeric(errors='coerce')",
    "Two rows said 'about 20' — unusable as a number, so they became NaN and are handled below.")

# --- 4. impossible values -----------------------------------------------
bad = (df["minutes"] <= 0) | (df["minutes"] > 120)
log(f"Marked {bad.sum()} rows with minutes outside 0–120 as missing",
    "A 0-minute or 3-hour journey to a school 3 km away is a typo, not a journey.")
df.loc[bad, "minutes"] = pd.NA

# --- 5. missing target ---------------------------------------------------
n_missing = df["minutes"].isna().sum()
df = df.dropna(subset=["minutes"])
log(f"Dropped {n_missing} rows with no target value",
    "You cannot train on a row whose answer is unknown, and inventing one would be fabrication.")

# --- 6. missing feature --------------------------------------------------
median_dist = df["distance_km"].median()
n_filled = df["distance_km"].isna().sum()
df["distance_km"] = df["distance_km"].fillna(median_dist)
log(f"Filled {n_filled} missing distances with the median ({median_dist:.2f} km)",
    "Only 2 rows; the median is robust to my one 4.5 km outlier. Flagged as a limitation.")

after = df.shape
print(f"shape before: {before}   after: {after}")
print("\n".join(CLEANING_LOG))
df.to_csv("data/clean.csv", index=False)
```

```
shape before: (123, 5)   after: (118, 5)
1. Dropped 3 exact duplicate rows  —  I logged 3 journeys twice on 14 Sept when my phone re-synced.
2. Lower-cased and stripped 'mode'  —  'Walk', 'walk ' and 'walk' were three groups in value_counts(); they are one thing.
3. Converted 'minutes' with to_numeric(errors='coerce')  —  Two rows said 'about 20' — unusable as a number, so they became NaN and are handled below.
4. Marked 2 rows with minutes outside 0–120 as missing  —  A 0-minute or 3-hour journey to a school 3 km away is a typo, not a journey.
5. Dropped 4 rows with no target value  —  You cannot train on a row whose answer is unknown, and inventing one would be fabrication.
6. Filled 2 missing distances with the median (2.31 km)  —  Only 2 rows; the median is robust to my one 4.5 km outlier. Flagged as a limitation.
```

> 🍕 **Why the reason column is the whole point.** "Dropped 4 rows" is a fact. "Dropped 4 rows because the target was unknown and inventing it would be fabrication" is an *argument*, and arguments can be checked, disagreed with, and improved. A cleaning log without reasons is a receipt. With reasons, it's science.

---

### ☐ Milestone 4 — Five charts that tell a story (105 min)

- [ ] Chart 1 — **the shape of the target**: a histogram. What's typical? What's the spread?
- [ ] Chart 2 — **the strongest driver**: a scatter plot of the target against your best numeric feature
- [ ] Chart 3 — **the categories**: a bar chart of the target's mean per category
- [ ] Chart 4 — **the spread inside categories**: a box plot, because a bar chart hides it
- [ ] Chart 5 — **your own choice**, answering the question the first four raised
- [ ] Every chart: title stating a **finding**, axis labels **with units**, legend if 2+ series, bars starting at 0
- [ ] Every chart: a one-sentence **caption** under it
- [ ] Read the five captions in order. They must read as a paragraph.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["minutes"], bins=12, edgecolor="black")
ax.set_title("Most journeys take 10–25 minutes, but a long tail reaches 59")
ax.set_xlabel("journey time (minutes)")
ax.set_ylabel("number of journeys")
fig.savefig("figures/01_target_distribution.png", dpi=150, bbox_inches="tight")
```

> **Caption 1:** *"Journey times pile up between 10 and 25 minutes, with a thin tail out to 59 — so any model that always guesses the mean of 21.6 will be badly wrong on the long walks."*

That caption does three things at once: it says what the chart shows, it names a number, and it sets up the next chart. That's what "narrative order" means — chart 5 should feel inevitable by the time you get there.

**The five-caption test:** copy your five captions into a plain text file with nothing else. Read it aloud. If it reads as a paragraph that answers your question, your story works. If it reads as five unrelated sentences, reorder the charts.

---

### ☐ Milestone 5 — ⚠️ One split, four models, one table (120 min) — *hardest milestone*

- [ ] Build `X` (features) and `y` (target), and print both shapes
- [ ] Turn text columns into numbers with `pd.get_dummies`
- [ ] Call `train_test_split` **exactly once**, with `random_state` set, and print the two shapes
- [ ] Write **one** `report()` function and use it for every model
- [ ] Score: a **baseline**, **kNN**, a **decision tree**, and **linear regression**
- [ ] Build the results table with the metric **named** and both train and test scores
- [ ] Write which model you'd actually use, and why

Full worked solution below — see **🔍 Worked Solution: Milestone 5**. Do not skip it; this is the milestone where projects stall.

---

### ☐ Milestone 6 — What I got wrong, and who it costs (60 min)

- [ ] Look at your **five worst test predictions** by hand (Should-have S2)
- [ ] Write **three specific, numeric admissions**. Vague ones don't count.
- [ ] State the **test-set size** and what one row is worth
- [ ] Write the **whose-data-is-this** paragraph
- [ ] Write the **what-would-being-wrong-cost** paragraph

**The difference between a weak and a strong admission:**

| ❌ Weak | ✅ Strong |
|---|---|
| "My dataset was quite small." | "118 rows, 24 in the test set. One test row is worth 4.2% of the accuracy, so the 0.03 gap between my tree and my kNN is noise, not a ranking." |
| "There might be some bias." | "97 of my 118 rows are my own journeys. The model has effectively learned *my* walking speed, and my little brother walks about 30% slower — I'd expect it to under-predict his time by roughly 4 minutes per km." |
| "The model wasn't perfect." | "Linear regression's five worst errors are all walks: it says 18.0 minutes for a 0.59 km walk that really took 6.1. It has one 'minutes per km' number for every mode, but a km on foot costs 12 minutes and a km on a bus costs 3.3. A straight line cannot hold both." |
| "I chose the best model." | "I picked `max_depth=5` by looking at the test curve, which means my reported test R² of 0.922 is optimistic. An honest number needs a third split I don't have." |

**The ethics paragraph — the four questions it must answer:**

```
   1. WHOSE DATA IS THIS?
      Who appears in the rows? Did they know? Did they agree? Can they
      ask you to remove their rows, and do you know which rows are theirs?

   2. WHAT IS THE WORST WRONG ANSWER?
      Not the average error — the WORST one in your test set. Say the number.

   3. WHO PAYS FOR THAT MISTAKE?
      A person, named by role. "The kid who leaves at 8:05 and arrives late."
      Not "users". Not "the system".

   4. WOULD YOU LET SOMEONE ELSE USE THIS TO DECIDE SOMETHING?
      Answer yes or no, and say what would have to change to flip your answer.
```

---

### ☐ Milestone 7 — Make it read as a story (60 min)

- [ ] Order the notebook into the **seven sections** (layout below)
- [ ] Every code cell has a markdown cell above it saying *why* it exists
- [ ] Delete every dead cell, failed experiment, and stray `print(df)`
- [ ] **Kernel → Restart & Run All.** Fix everything that breaks.
- [ ] Add a final markdown line: *"Ran clean, top to bottom, on <date>."*
- [ ] Read the whole notebook **out loud** to a human. Mark every place they look confused.
- [ ] Fix those places. That's the last edit.

**The seven sections, in order:**

```
   1. THE QUESTION       one sentence + your dated prediction
   2. THE DATA           data card, raw load, shape, head()
   3. THE CLEANING       every change + the numbered log + before/after shape
   4. THE CHARTS         five figures, five captions, in narrative order
   5. THE MODELS         one split, four models, one results table
   6. WHAT I GOT WRONG   three numeric admissions + the worst-five table
   7. WHOSE DATA & COST  the ethics paragraph + what I'd do next
```

---

## 📁 Starter Scaffold

Make this before Milestone 2. Everything lands somewhere.

```
   data-detective/
   │
   ├── data-detective.ipynb        ← THE deliverable. One notebook, seven sections.
   │
   ├── data/
   │   ├── raw.csv                 ⛔ WRITE ONCE. Never edit. Never.
   │   └── clean.csv               ← produced by Milestone 3's code
   │
   ├── figures/
   │   ├── 01_target_distribution.png
   │   ├── 02_strongest_driver.png
   │   ├── 03_category_means.png
   │   ├── 04_category_spread.png
   │   ├── 05_my_choice.png
   │   └── 06_depth_curve.png      ← optional (Should-have S3)
   │
   ├── helpers.py                  ← your Module 3 habit: reusable functions
   │
   └── notes/
       ├── plan.md                 ← Milestone 1 template, filled in
       └── collection-diary.md     ← what went wrong while collecting. Gold dust.
```

### Starter file — `helpers.py`

```python
"""helpers.py — small reusable tools for the Data Detective capstone.

Import from the notebook with:   from helpers import log_maker, report_regression
"""

import numpy as np
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             r2_score, accuracy_score)


def log_maker():
    """Return (log_function, log_list). Every call appends a numbered entry."""
    entries = []

    def log(action, reason):
        entries.append(f"{len(entries) + 1}. {action}  —  {reason}")

    return log, entries


def report_regression(name, model, X_train, y_train, X_test, y_test, units=""):
    """Fit a model on the training split and score it on the test split.

    Returns one dict = one row of the results table. Using ONE function for
    every model is what makes the comparison fair — you cannot accidentally
    score two models differently.
    """
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return {
        "model": name,
        f"MAE ({units})": round(mean_absolute_error(y_test, pred), 2),
        f"RMSE ({units})": round(float(np.sqrt(mean_squared_error(y_test, pred))), 2),
        "test R2": round(r2_score(y_test, pred), 3),
        "train R2": round(model.score(X_train, y_train), 3),
    }


def report_classification(name, model, X_train, y_train, X_test, y_test):
    """Same idea, for a category target."""
    model.fit(X_train, y_train)
    return {
        "model": name,
        "test accuracy": round(accuracy_score(y_test, model.predict(X_test)), 3),
        "train accuracy": round(model.score(X_train, y_train), 3),
    }


def worst_n(df_test, y_true, y_pred, n=5):
    """Return the n rows the model got most wrong — the Should-have S2 table."""
    out = df_test.copy()
    out["actual"] = np.round(y_true, 1)
    out["predicted"] = np.round(y_pred, 1)
    out["error"] = np.round(y_true - y_pred, 1)
    order = out["error"].abs().sort_values(ascending=False).index
    return out.loc[order].head(n)
```

### Starter file — `notes/collection-diary.md`

```
COLLECTION DIARY — write one line every time something goes wrong

   date     what happened                             what I did about it
   ───────  ────────────────────────────────────────  ──────────────────────
   14 Sept  phone re-synced, 3 journeys logged twice   noted; will drop in cleaning
   17 Sept  forgot to log the morning trip             row missing, NOT invented
   19 Sept  measured distance on a map, not the        wrote it in the data card as
            actual route walked                        a known measurement error
```

> That diary is the least glamorous file in the project and the one that makes Milestone 6 easy. Every line in it becomes a sentence in "what I got wrong."

---

## 🔍 Worked Solution: Milestone 5

This is where projects stall, so here is a complete, runnable answer. **It runs as-is** — it generates a stand-in dataset so you're never blocked. When your own `clean.csv` is ready, delete the generator and load your file instead. Everything below it is unchanged.

### The problem, in three parts

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  PART 1 — scikit-learn only eats numbers.                            │
   │           Your "mode" column says "walk". That is text.              │
   │           → pd.get_dummies turns 1 text column into 3 number columns │
   │                                                                      │
   │  PART 2 — the split must be made ONCE, before any model exists.      │
   │           → one call, random_state set, results stored in variables  │
   │             that every model reads. Never re-split.                  │
   │                                                                      │
   │  PART 3 — the comparison must be fair.                               │
   │           → one report() function, called four times. Not four       │
   │             hand-written scoring blocks that quietly differ.         │
   └──────────────────────────────────────────────────────────────────────┘
```

### Step 1 — Get a table (swap this for your own)

```python
import numpy as np
import pandas as pd

def make_demo_journeys(n=120, seed=7):
    """A stand-in dataset so this file runs before your own data is ready.
    120 journeys to school. DELETE THIS once data/clean.csv exists."""
    rng = np.random.default_rng(seed)                    # seeded = repeatable
    mode = rng.choice(["walk", "cycle", "bus"], size=n, p=[0.40, 0.25, 0.35])
    distance = np.round(rng.uniform(0.4, 4.5, size=n), 2)
    rain = rng.choice([0, 1], size=n, p=[0.72, 0.28])
    hour = rng.choice([7, 8, 9], size=n, p=[0.25, 0.55, 0.20])

    speed = np.where(mode == "walk", 5.0,                # km/h, by mode
             np.where(mode == "cycle", 14.0, 18.0))
    minutes = distance / speed * 60                       # the physics
    minutes = minutes + np.where(mode == "bus", 6.0, 0.0) # waiting for the bus
    minutes = minutes + rain * 3.5                        # rain slows everything
    minutes = minutes + (hour == 8) * 2.5                 # the 8 a.m. crush
    minutes = minutes + rng.normal(0, 1.6, size=n)        # everything else

    return pd.DataFrame({"distance_km": distance, "mode": mode, "rain": rain,
                         "depart_hour": hour, "minutes": np.round(minutes, 1)})

df = make_demo_journeys()
# YOUR VERSION:  df = pd.read_csv("data/clean.csv")

print(df.head())
print("shape:", df.shape)
```

```
   distance_km   mode  rain  depart_hour  minutes
0         0.46  cycle     0            8      5.4
1         2.98    bus     0            8     17.2
2         3.65    bus     0            8     21.4
3         2.50   walk     0            8     30.9
4         3.38   walk     0            8     41.1
shape: (120, 5)
```

### Step 2 — Build `X` and `y`, and turn text into numbers

```python
FEATURES = ["distance_km", "mode", "rain", "depart_hour"]
TARGET   = "minutes"

# get_dummies: one text column becomes one 0/1 column per value.
# "walk" -> mode_walk=1, mode_cycle=0, mode_bus=0
X = pd.get_dummies(df[FEATURES], columns=["mode"]).astype(float)
y = df[TARGET].values

print("X shape:", X.shape, " y shape:", y.shape)
print("columns:", list(X.columns))
print(X.head(3))
```

```
X shape: (120, 6)  y shape: (120,)
columns: ['distance_km', 'rain', 'depart_hour', 'mode_bus', 'mode_cycle', 'mode_walk']
   distance_km  rain  depart_hour  mode_bus  mode_cycle  mode_walk
0         0.46   0.0          8.0       0.0         1.0        0.0
1         2.98   0.0          8.0       1.0         0.0        0.0
2         3.65   0.0          8.0       1.0         0.0        0.0
```

> **Definition — one-hot encoding:** replacing one text column that has *k* different values with *k* columns of 0s and 1s, exactly one of which is 1 per row. It's called "one-hot" because only one switch is on.

Why not just map `walk → 0, cycle → 1, bus → 2`? Because that tells the model bus is *twice* cycle and *three times* nothing, which is nonsense. One-hot says "these are three separate things", which is true. `.astype(float)` is there because pandas 2.x makes dummy columns `bool`; sklearn is happy either way, but a uniform dtype prevents surprises.

### Step 3 — Split. Once. Right now.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% held out — 24 of 120 journeys
    random_state=42,      # the same 24 every time I run this
)

print("train:", X_train.shape, " test:", X_test.shape)
print(f"One test row is worth {100 / len(y_test):.1f}% of any accuracy figure.")
```

```
train: (96, 6)  test: (24, 6)
One test row is worth 4.2% of any accuracy figure.
```

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  ⛔ FROM HERE ON, X_test AND y_test ARE RADIOACTIVE.                 │
   │                                                                      │
   │     No model calls .fit() on them. No scaler is fitted on them.      │
   │     Nothing computes a mean or a median from them. They exist to     │
   │     be scored, at the end, once.                                     │
   │                                                                      │
   │     Everything below re-uses these four variables. There is exactly  │
   │     one train_test_split call in the whole notebook, and this is it. │
   └──────────────────────────────────────────────────────────────────────┘
```

### Step 4 — One scoring function, used by everyone

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def report(name, model):
    """Fit on train, score on test, return one row of the results table."""
    model.fit(X_train, y_train)                    # learn from the 96
    pred = model.predict(X_test)                   # guess the 24
    return {
        "model": name,
        "MAE (min)":  round(mean_absolute_error(y_test, pred), 2),
        "RMSE (min)": round(float(np.sqrt(mean_squared_error(y_test, pred))), 2),
        "test R2":    round(r2_score(y_test, pred), 3),
        "train R2":   round(model.score(X_train, y_train), 3),
    }
```

Four things to notice, because each one is a mark on the rubric:

1. **The metric name is inside the column header**, with units. `MAE (min)` not `score`.
2. **Both `train R2` and `test R2`** are returned. The gap between them is the whole Module 9 story.
3. **RMSE is `np.sqrt(mean_squared_error(...))`**, not the removed `squared=False` argument.
4. The function fits *inside*, so no model can be accidentally scored before it's trained.

### Step 5 — The bake-off

```python
from sklearn.dummy import DummyRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

rows = [
    report("baseline (mean)",   DummyRegressor(strategy="mean")),
    report("kNN k=5 (scaled)",  make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=5))),
    report("kNN k=5 (raw)",     KNeighborsRegressor(n_neighbors=5)),
    report("tree depth=4",      DecisionTreeRegressor(max_depth=4, random_state=0)),
    report("tree unlimited",    DecisionTreeRegressor(random_state=0)),
    report("linear regression", LinearRegression()),
]

results = pd.DataFrame(rows).sort_values("MAE (min)")
print(results.to_string(index=False))
```

```
            model  MAE (min)  RMSE (min)  test R2  train R2
    kNN k=5 (raw)       1.83        2.56    0.954     0.969
   tree unlimited       2.72        3.40    0.919     1.000
 kNN k=5 (scaled)       2.78        3.65    0.907     0.944
     tree depth=4       2.86        3.83    0.898     0.978
linear regression       4.67        5.77    0.767     0.831
  baseline (mean)       9.41       12.07   -0.016     0.000
```

**Read that table properly. There are four findings in it, and three of them are surprising.**

**Finding 1 — the baseline gives every other number its meaning.** Always guessing 21.6 minutes is off by 9.41 minutes on average. The best model is off by 1.83. So the model buys you about **7.6 minutes of accuracy**. Without that bottom row, "MAE 1.83" is a number floating in space.

Also look at the baseline's `test R2` of **−0.016**. R² can go negative. It means "worse than guessing the mean" — and the baseline *is* guessing the mean, so it should be ~0; the small negative is just because the test set's mean differs slightly from the training set's. If any of your real models goes negative, something is badly wrong.

**Finding 2 — `tree unlimited` scores 1.000 on training data.** A perfect score. It has memorised all 96 training journeys exactly. And on the test set it drops to 0.919. That 0.081 fall is the **train/test gap** from Module 9, in your own table. Compare `tree depth=4`: 0.978 train, 0.898 test — a smaller gap from a simpler tree, which is exactly what Module 9's curve predicts.

**Finding 3 — unscaled kNN beat scaled kNN.** That contradicts Module 8, and it is not a mistake. Here's why. Module 8's rule is *"scale before a distance-based model, because a feature measured in thousands will drown a feature measured in ones."* True. But scaling also says *"every feature matters equally"* — and in this dataset that's false. `distance_km` genuinely is the most important thing, and leaving it unscaled lets it dominate the distance calculation, which happens to be correct here.

**The honest conclusion is not "scaling is wrong."** It is: *scaling is a sensible default whose effect you must measure, not assume.* You measured it. Write that sentence in your notebook — a learner who reports a result that contradicts the textbook, and explains it, is doing better work than one who quietly deletes it.

**Finding 4 — linear regression came last among the real models.** Look at *why*, because this is the best paragraph in your whole notebook. Print its coefficients:

```python
lin = LinearRegression().fit(X_train, y_train)
for name, weight in zip(X.columns, lin.coef_):
    print(f"{name:>13}  {weight:+7.3f}")
print(f"    intercept  {lin.intercept_:+7.3f}")
```

```
  distance_km   +6.632
         rain   +4.089
  depart_hour   -0.236
     mode_bus   -4.064
   mode_cycle   -7.759
    mode_walk  +11.824
    intercept   +4.432
```

In plain English: *"every extra kilometre adds 6.63 minutes; rain adds 4.09 minutes; walking adds 11.82 minutes compared to a baseline, while cycling subtracts 7.76 — so walking costs about 19.6 minutes more than cycling for the same distance."*

And there is the bug in the model's thinking. It has **one** "minutes per kilometre" number — 6.63 — that it applies to walking, cycling and the bus alike. But a kilometre on foot really costs 12 minutes, and a kilometre on a bus costs about 3.3. A straight line cannot hold two different slopes at once. The tree can, because it splits on `mode_walk` first and then asks about distance separately.

You can see it in the errors:

```python
from helpers import worst_n
worst = worst_n(df.loc[X_test.index, ["distance_km", "mode", "rain"]],
                y_test, lin.predict(X_test), n=5)
print(worst.to_string())
```

```
    distance_km  mode  rain  actual  predicted  error
65         0.59  walk     0     6.1       18.0  -11.9
89         0.61  walk     0     6.9       18.2  -11.3
62         4.00   bus     1    20.7       29.3   -8.6
10         4.29  walk     0    51.7       43.1    8.6
31         3.70  walk     0    46.6       38.7    7.9
```

Every one of the five worst errors involves a walk. Short walks are massively over-predicted (18 minutes for a 6-minute stroll), long walks under-predicted. That's the signature of a slope that's too flat for walking — and you found it by *looking at five rows*, not by reading a book.

### Step 6 — Say which one you'd use

The highest-scoring model is not automatically the one you ship. Write a short paragraph like this:

> *"kNN (raw) has the best MAE at 1.83 minutes, but I would deploy the depth-4 tree at 2.86 minutes. Three reasons. First, the difference is 1.03 minutes on a 24-row test set where one row is worth 4.2% — that gap is inside the noise. Second, the tree prints as eight if/then rules I can show my mum, and she can sanity-check them; kNN can only say 'the five most similar journeys took about this long'. Third, kNN's advantage came from leaving distance unscaled, which happened to be right for this dataset and I have no reason to think it'll stay right when I add my brother's journeys next month."*

That paragraph is worth more than every chart in the notebook.

---

### 🔀 Sidebar — if your target is a **category** instead of a number

Swap three things:

```python
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. stratify, so both splits keep the same class balance (Module 8)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 2. the baseline is "always guess the biggest class"
#    DummyClassifier(strategy="most_frequent")

# 3. the metric is accuracy, and you must print a confusion matrix
print(confusion_matrix(y_test, model.predict(X_test)))
```

**The third model problem.** Linear regression cannot output a category, and logistic regression is a Level 3 tool. So your third model is a **regression-plus-threshold**: predict the underlying *number* with `LinearRegression`, then convert. If your category is `late = minutes > 25`, then:

```python
number_model = LinearRegression().fit(X_train_minutes, y_train_minutes)
pred_late = (number_model.predict(X_test_minutes) > 25).astype(int)
```

This is a real technique, not a fudge — but say in your notebook that you did it and why.

> ⚠️ **If your classifier scores 100%, do not celebrate.** Check for leakage first. On this demo dataset, predicting `late` from the same features gives *exactly* 1.000 accuracy — because `late` is defined from `minutes`, and `minutes` is almost perfectly determined by the features. A perfect score on real data nearly always means the answer is hiding in your features.

---

## ⚠️ Common Capstone Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Editing `raw.csv` by hand to fix a typo | It's one keystroke and pandas feels like effort | Every repair goes in a cell with a log line. Otherwise nobody — including future you — can reproduce your table. Make the file read-only. |
| Splitting inside a loop, or once per model | You copy-paste a model block and the split comes along for the ride | Exactly one `train_test_split` call in the whole notebook, near the top of Section 5. Search the file for the string; if it appears twice, that's a bug. |
| Fitting `StandardScaler` before the split | It reads like a cleaning step, so it drifts up into Section 3 | Use `make_pipeline(StandardScaler(), Model())`. The pipeline re-fits the scaler on training data only, automatically. Module 8 called this leakage. |
| A feature that contains the answer | The best predictors are always the ones closest to the target | Ask of every column: *"could I know this before the target happened?"* If no, delete it. A 0.99 R² on self-collected data is a warning light, not a trophy. |
| Reporting a bare number: "MAE 2.86" | Units feel obvious to the person who collected the data | "2.86 **minutes**". Always. The rubric checks for this in every table and every caption. |
| Tuning `max_depth` on the test set and reporting that score | It's the only extra data you have | You may do it — everyone does — but you must then write "this estimate is optimistic because I chose the depth by looking at it." One sentence, full marks. |
| Charts with no captions | The chart "obviously" shows the thing | A caption states the finding in one sentence. Without it a reader invents their own conclusion, and it won't be yours. |
| A "what I got wrong" section that says "more data would help" | It's true of every project ever, so it feels safe | It's also content-free. Three *specific*, *numeric* admissions. Use the weak-vs-strong table in Milestone 6. |
| Forgetting Restart & Run All | The notebook works because of a variable you defined an hour ago and then deleted the cell for | Restart & Run All is the only test that counts. Do it twice: once at Milestone 7, once before you present. |
| Building charts before cleaning | Charts are fun and cleaning isn't | Your chart of "average time by mode" will silently average `walk`, `Walk` and `walk ` as three groups. Clean first. Always. |

---

## 📊 Grading Rubric

Score each of the eight rows 1–4. **8–14 = Beginning · 15–21 = Developing · 22–28 = Proficient · 29–32 = Exceptional.**

| Criterion | 1 · Beginning | 2 · Developing | 3 · Proficient | 4 · Exceptional |
|---|---|---|---|---|
| **1. Question & data design** | No stated question, or a topic instead of a question; columns chosen after collecting | A question is stated; 3–4 columns; the target is identifiable but not named as such | One-sentence question with a `?`; 4+ features + a named target; a data card with units and measurement method; the honest-feature test applied | A dated prediction written before collecting; every column defended as something a person could really measure; a stated unit-of-a-row; known measurement error acknowledged up front |
| **2. Data collection** | Under 60 rows, or rows invented / recalled from memory | 60–99 rows, or 100+ with almost no variety (one category value dominates) | **100+ rows** collected as they happened; every category value appears 10+ times; numeric features genuinely spread; `raw.csv` saved and untouched | 120+ rows with a collection diary logging what went wrong; deliberately awkward rows included and defended; a second batch collected later for a drift check |
| **3. Cleaning & the log** | No cleaning, or cleaning done by editing the spreadsheet | Some cleaning in pandas; a list of what was changed but not why; no before/after shape | Missing values, dtypes, duplicates and spellings all handled in code; a **numbered log with a reason per line**; before/after `shape` printed; `clean.csv` saved | Each decision names the alternatives rejected ("median not mean, because of the 4.5 km outlier"); rows dropped are counted and the loss quantified; the log alone would let a stranger reproduce the table exactly |
| **4. Charts** | Fewer than 5, or charts with no titles/labels | 5 charts, labelled, but in arbitrary order and with topic-titles ("Distance vs Time") | 5 charts, correct type for each question, titles that state a **finding**, axis labels **with units**, bars from 0, one-sentence caption each | The five captions read aloud as a single paragraph that answers the question; at least one chart exists because an earlier chart raised the question; small-*n* groups flagged in the caption |
| **5. Modelling honesty** | Scored on the training data, or split more than once, or no baseline | One split but no `random_state`; models scored with different ad-hoc code; baseline missing | **One split, `random_state` set, made once**; a baseline plus three genuinely different models; one `report()` function used for all; scaler inside a pipeline | The test set is provably untouched (a reader can verify by scanning the file); test-set size and the value of one row stated; scaled-vs-unscaled measured rather than assumed |
| **6. Results & interpretation** | A single number with no metric name or units | A results table, but only test scores, and metrics unnamed | Metric **named with units** in every header; train **and** test score for every model; the train/test gap identified and named; a stated choice of model | The chosen model is justified against the highest-scoring one on grounds other than score (interpretability, robustness, noise); a coefficient or a tree rule is translated into a plain-English sentence about the real world |
| **7. What I got wrong** | Absent, or "it could be improved" | One vague admission; no numbers | **Three specific admissions with numbers**; test-set size and one-row worth stated; the optimism from tuning on test acknowledged if it happened | The five worst predictions inspected by hand with a *mechanism* proposed for the pattern; a limitation is traced back to a specific choice in Milestone 1 or 2 |
| **8. Whose data & what it costs** | Not attempted, or "no ethical issues here" | Mentions privacy in general terms | Names who is in the data, whether they consented, the worst error in the test set as a number, and who would pay for it — by role, not "users" | Answers whether they'd let someone decide with this and what would have to change to flip the answer; identifies a group the data under-represents and predicts the direction of the error for them |

---

## 🎤 Show Your Work

### The 8-minute walkthrough

You are not presenting slides. You are scrolling one notebook, top to bottom, out loud.

```
   ┌─────────┬────────────────────────────────────────────────────────────┐
   │  0:00   │  THE QUESTION (45 s)                                       │
   │         │  Say it, then say who would care about the answer.         │
   │         │  Then read your dated prediction — including the bit       │
   │         │  you got wrong. Start with being wrong. It buys trust.     │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  0:45   │  THE DATA (60 s)                                           │
   │         │  "One row is one ______. I collected 123 of them between   │
   │         │   4 and 26 September, by ______." Show head() and shape.   │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  1:45   │  THE CLEANING (75 s)  ← nobody expects this to be good     │
   │         │  Read three log lines out loud, including the reasons.     │
   │         │  "123 rows in, 118 out. Here's every row I lost and why."  │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  3:00   │  THE CHARTS (2 min)                                        │
   │         │  Read the five captions in order, as a paragraph. Do not   │
   │         │  describe the axes; the labels do that. Say the finding.   │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  5:00   │  THE MODELS (90 s)                                         │
   │         │  Baseline first, always: "guessing the mean is off by      │
   │         │   9.4 minutes." Then the table. Name the metric and the    │
   │         │   units every single time you say a number.                │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  6:30   │  WHAT I GOT WRONG (60 s)  ← the bit that wins the room     │
   │         │  Three admissions with numbers. Show the worst-five table  │
   │         │  and explain the pattern in it.                            │
   ├─────────┼────────────────────────────────────────────────────────────┤
   │  7:30   │  WHOSE DATA, WHAT IT COSTS (30 s)                          │
   │         │  Who's in it, who'd pay for a wrong answer, and whether    │
   │         │  you'd let anyone decide anything with this yet.           │
   └─────────┴────────────────────────────────────────────────────────────┘
```

### The question bank — rehearse all seven

| They ask | The shape of a good answer |
|---|---|
| *"How do you know the model actually works?"* | I don't, fully — I know it scored MAE 2.86 minutes on 24 journeys it never saw. Guessing the mean scores 9.41. That's the comparison, and 24 rows is a small test, so one row is worth 4.2%. |
| *"Why did you pick that model?"* | Name the metric, then give a non-score reason. "The tree is 1 minute worse and I can read its eight rules out loud. On a 24-row test set, 1 minute is inside the noise." |
| *"Couldn't you just look at the average?"* | Yes — that's my baseline row, and it's off by 9.41 minutes. The model gets that to 2.86. Show the baseline row. Always have a baseline row. |
| *"Isn't 118 rows really small?"* | Yes. Here's exactly how small: 24 in the test set, one row = 4.2%, so I can't distinguish two models less than about 5 points apart. That's why I'm not claiming a winner among the top three. |
| *"What would make it better?"* | Not "more data". Be specific: "97 of 118 rows are my own journeys. Forty journeys from three other people would tell me whether it learned about journeys or about *me*." |
| *"Did you delete data that didn't fit?"* | Point at the cleaning log. Every dropped row, counted, with a reason. Say the before/after shape out loud. |
| *"Should the youth centre actually use this?"* | Answer honestly with a number attached. "Not yet. It under-predicts long walks by up to 8.6 minutes, and long walks are exactly the kids who arrive late — the ones the decision is about." |

### 🚫 The banned words

```
   magic  ·  the AI figured it out  ·  pretty accurate  ·  it's smart
   basically perfect  ·  the data speaks for itself  ·  obviously  ·  just
```

`just` is on that list on purpose — "I just dropped the weird rows" is where projects go to die. Every "just" is a decision you skipped explaining.

### 🚀 Three stretch directions

**1. The drift test (~1.5 h).**
Freeze your model. Collect **30 brand-new rows** two or three weeks later — a different week, different weather, ideally a different person. Do not retrain. Score the frozen model on the new batch and put the two numbers side by side.

Expect it to get worse. It almost always does, and the amount tells you something no cross-validation can: whether you built a model of *the world* or a model of *the fortnight you collected in*. This is the single most valuable extension here, because "the model got worse when reality moved" is the number-one way real deployed models fail, and almost nobody your age has ever measured it.

**2. Feature invention, measured (~1.5 h).**
Guess a feature that isn't in your table but could be computed from it. `minutes_per_km`. `is_weekend`. `days_since_the_last_time`. `distance × is_walking` (that's an **interaction**, and on the demo dataset it's exactly what linear regression was missing).

Write down *before* you build it whether you think it will help and by how much. Then add it, rerun the identical bake-off on the identical split, and put the before/after MAE side by side. Half your ideas will do nothing. That's the lesson — and the half that work, you invented, which is a genuinely different feeling from importing a model.

**3. Explain it to the person who'd decide (~1 h).**
Make a **one-page printout with no code on it**: the question, one chart, the headline number with its baseline and units, the one-sentence limitation, and your recommendation. Then hand it to the actual person — the coach, the club organiser, the parent — and watch them read it without you talking.

Note every place they frown, every question they ask, and every number they misread. That list is the most useful feedback in this entire capstone, because a result nobody can act on is a result that didn't happen. This is the skill that separates people who *do* data science from people who *ship* it.

---

## 🔑 Key Takeaways

- **The model is 15% of the work.** The question, the collection, the cleaning log, and the honesty are the other 85% — and they're the parts that make the 15% mean anything.
- **One split, made once, `random_state` set.** Every fair comparison in this notebook rests on that single line being true.
- **A metric without units and a baseline is a rumour.** "MAE 2.86 minutes, against a baseline of 9.41 minutes, on 24 test rows" is a fact.
- **Write down what you expect before you look.** You cannot un-see a result, and a prediction made afterwards is not a prediction.
- **A result that contradicts the textbook is a gift**, not an error — if you can explain the mechanism. Unscaled kNN winning was the most interesting line in the worked solution.
- **"What I got wrong" with three numbers in it** is the section that turns a school project into work an adult would take seriously.

---

## ✅ Final Checklist Before You Present

```
   THE QUESTION & DATA
   □ Question stated in one sentence, with a question mark
   □ Dated prediction written BEFORE collection, and reported either way
   □ 100+ rows, 4+ features, 1 named target
   □ data/raw.csv exists and has never been hand-edited
   □ Data card: columns, units, who, when, permission, what's NOT in it

   THE CLEANING
   □ Notebook reads raw.csv, not clean.csv
   □ Numbered cleaning log with a REASON on every line
   □ Before/after shape printed
   □ data/clean.csv written by code, not by hand

   THE CHARTS
   □ Five charts, five PNGs, five captions
   □ Every title states a finding, not a topic
   □ Every axis label names the quantity AND its units
   □ Bar charts start at zero
   □ The five captions read aloud as one paragraph

   THE MODELS
   □ Exactly ONE train_test_split call in the whole notebook
   □ random_state set on the split and on every tree
   □ Any scaler is inside a make_pipeline, never fitted before the split
   □ A baseline model in the results table
   □ Three genuinely different models
   □ One report() function used for all of them
   □ Metric named WITH UNITS in every column header
   □ Train score AND test score for every model
   □ Test-set size stated, and what one row is worth

   THE HONESTY
   □ Three specific, NUMERIC admissions
   □ The five worst predictions inspected, with a proposed mechanism
   □ "I tuned on the test set so this is optimistic" — if you did
   □ Whose data this is, and whether they agreed
   □ The worst error as a number, and who would pay for it, by role
   □ A yes/no on whether anyone should decide with this yet

   THE NOTEBOOK
   □ Seven sections, in order
   □ A markdown cell above every code cell saying why it exists
   □ Zero dead cells, zero stray print(df)
   □ Kernel → Restart & Run All, clean, twice
   □ Read out loud to a human, and their confusions fixed
```

---

## 🎓 You Have Finished Level 2

Look at what you can do now that you could not do twenty weeks ago.

You can open a blank file and write a program. You can take a pile of messy rows and turn them into a table you'd defend. You can make a chart that argues honestly, and spot the one that doesn't. You can train three models, put them in a table, and — the rare part — say out loud which number in that table you don't believe and why.

Twenty weeks ago you could not print "hello".

Level 3 opens the boxes you've been using. `LinearRegression()` becomes **gradient descent**, which you will write yourself and watch converge on a plot. `fit()` becomes a loop over a **loss function**. And then the same idea, stacked into layers, becomes a **neural network** — first in raw numpy so you can see every multiplication, then in PyTorch so you can make it big.

None of that will feel like magic, because you'll have built the floor it stands on.

Take the [assessment](assessment.md) if you haven't. Then:

> ### 👉 **[Level 3 — Engineer](../level-3-engineer/)**

---

[⬅ Module 9](module-09-trees-lines-and-overfitting.md) · [Level 2 Home](README.md) · [Assessment](assessment.md) · [Glossary](glossary.md) · [Level 3 ➡](../level-3-engineer/)

*You asked a question, built the data yourself, cleaned it in the open, and reported the number you didn't like. That is the job. See you in Level 3.*
