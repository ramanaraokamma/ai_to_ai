```
   █████╗ ██╗    ██████╗  █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗
  ██╔══██╗██║   ██╔════╝ ██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝
  ███████║██║   ██║      ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝
  ██╔══██║██║   ██║      ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝
  ██║  ██║██║   ╚██████╗ ██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║
  ╚═╝  ╚═╝╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │        L E V E L   3   ·   E N G I N E E R                        │
  │        ────────────────────────────────────────                  │
  │        T H E   3 6 - W E E K   C O U R S E                        │
  │                                                                  │
  │        One class a week. 60–75 minutes. The box gets opened.      │
  │        A teacher who knows no AI, no Python and no calculus       │
  │        can teach it — the maths is taught to YOU first.           │
  │                                                                  │
  │        model.fit(X, y)  ─────►  loss.backward()                   │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

# ⚙️ Level 3 Engineer — The 36-Week Course

### *One school year. One class a week. From "sklearn found the answer" to a neural network the student built out of arithmetic they did on paper first — and then shipped.*

**Learner:** one 9th grader, age ~14, fresh out of Levels 1 and 2 · **Teacher:** any adult — **no AI, no Python, no calculus required**
**Coding:** every single week · **Maths:** starts at algebra and `y = mx + c`; ends at gradients, matrix shapes and backpropagation
**Rhythm:** 36 weeks × one 60–75 minute class + ~60–75 min of workbook homework

[⬅ Back to Level 3 modules](../README.md) · [**Start here: How To Use This Course**](HOW-TO-USE.md) · [**Teacher Orientation**](teacher-guide/00-orientation.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md) · [Figure style guide](figures/STYLE.md)

---

## 🪝 What This Is

Level 2 ended with a student who could write this:

```python
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
print(accuracy_score(y_test, model.predict(X_test)))
```

…and defend every part of it. That is a real achievement and it is also a door they have not opened.
Because `model.fit(X_train, y_train)` is **one line hiding five decisions somebody made for them**, and
underneath those five decisions is a loop doing arithmetic that nobody has shown them yet.

This year opens the box. By June the student will have:

- written the loop themselves, in numpy, with no framework
- measured a slope with a ruler and two subtractions before anybody said the word *derivative*
- worked out backpropagation as *"how much did each knob contribute to the error"*, with real numbers,
  and then watched PyTorch produce the identical number to eight decimal places
- and shipped the result as a file a stranger can load.

The nine Level 3 modules next door are excellent and they are **not a course**. They are a book for a
motivated reader with six free hours and nobody waiting on them. This folder turns that book into a
**school year** — 36 sittings, each small enough to actually happen on a Tuesday evening.

The single design constraint that shaped every page:

> **The teacher opens the week's file 20 minutes before class, and that is all the preparation they get.
> They do not know Python. They do not know AI. They have never done calculus. They must be able to
> teach a confident, correct 70-minute lesson from that one file — including the maths.**

That is a harder promise than Level 2's, because this level contains derivatives, matrix shapes and
backpropagation. So the teacher file for every week that carries new maths **teaches the adult that
maths from scratch, numerically, before asking them to teach it.** Section 1 of the
[orientation](teacher-guide/00-orientation.md) is a complete twelve-page maths course for an adult who
has never met calculus, and every idea in it is worked on real numbers that were actually computed.

Five things are true of every week in this folder:

1. **Every code block was actually run before it was pasted**, with a seed set, and every output shown
   is the real output. If a number appears in a fenced `text` block, a machine printed it.
2. **Every new mathematical idea is computed numerically before it is named.** A derivative is *"how
   steep is this hill right here"*, measured with a tiny step, drawn as a slope on a curve, and only
   *then* called a derivative. There are no proofs, no limits, and no symbolic rule appears before the
   same number has been obtained by nudging and dividing.
3. **At most ONE new mathematical idea per week**, and 21 of the 36 weeks have none at all. The
   [maths ladder](#-the-maths-ladder) below is the enforcement mechanism.
4. **Every week shows at least one real error message**, copied from a real failed run, explained line
   by line, then fixed. Shape mismatches, `Long` vs `Float`, a forgotten `zero_grad()`, a NaN loss.
   Errors are curriculum here, not accidents.
5. **Nothing downloads.** See [Offline by design](#-offline-by-design). Every dataset either ships
   inside scikit-learn or is generated in the code, in front of the student.

### What the student walks out with in June

- A **`Pipeline` artifact** they saved with `joblib` and reloaded in a clean process with zero training
  code in it — plus the `model_card.md` that says where it breaks
- An **ablation table** proving, feature by feature, which of their own inventions actually helped
- Three **caught leakage bugs**, each with the fake score and the honest score side by side
- A **threshold chosen by arithmetic** against a written price list for the two kinds of mistake
- **Logistic regression trained by their own gradient descent loop**, matching sklearn's weights to
  three decimal places
- 🧠 **NumPy Brain** — a 2-layer neural network in pure numpy, no framework, that learns a curved
  boundary, with a numerical gradient check agreeing to `1e-6`
- The same network **rebuilt in PyTorch and proved identical**, then scaled up to a CNN that reads
  handwritten digits at ~95% test accuracy in about nine seconds on a laptop CPU
- **Clusters they named themselves** and defended from a feature-means table, with a PCA map
- 💬 A **sentiment classifier** whose fifteen most-trusted words they can read out loud, and one review
  it gets wrong *because bag-of-words threw the word order away*
- 🚢 A **shipped model**: a CLI, a local service that survives four malformed requests, a prediction
  log with latency, subgroup metrics, and a monitoring plan
- And the reflex that matters most: **a number you cannot reproduce is not a result.**

---

## 👤 Who This Is For

| | |
|---|---|
| **The learner** | One 9th grader, around 14. **Has finished Levels 1 and 2.** Writes Python confidently — variables, if/else, loops, functions, lists, dicts, numpy, pandas, matplotlib — and has trained kNN, a decision tree and a linear regression with scikit-learn, and seen an overfitting curve. **Has never seen calculus, linear algebra notation, or the inside of a neural network.** Maths available: algebra, negative numbers, fractions, graphs, a little trigonometry. |
| **The teacher** | You. **You are not expected to know AI. You are not expected to know Python. You are not expected to know calculus, and you will not need to learn it.** Read [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) once — it contains a twelve-page maths course for adults built entirely out of arithmetic, a Python-and-PyTorch mini-course, the 14 errors this level actually produces, and an offline install guide — and you are ready for all 36 weeks. |
| **The setting** | A kitchen table, a classroom, a library corner. **One laptop you are allowed to install software on**, with about 4 GB free. No GPU. No internet during lessons. |
| **Group size** | Written for one learner. Every activity has a "if you have 2–6 students" note in the teacher file. Above 8, pair them at one keyboard each and add 10 minutes to every activity. |

### What Levels 1 and 2 gave them — and why Week 1 should feel like a door opening

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │  THEY ALREADY DO THIS            ─►  THIS YEAR THEY SEE WHAT'S UNDER IT    │
   ├────────────────────────────────────────────────────────────────────────────┤
   │  train_test_split(0.2)           ─►  train / val / test, and why        w2 │
   │                                      choosing is a kind of fitting         │
   │  "don't fit the scaler first"    ─►  three named kinds of leakage,      w6 │
   │                                      each one caught with a number         │
   │  accuracy_score(y, pred)         ─►  the four cells, precision,         w8 │
   │                                      recall, F1, ROC-AUC, cost            │
   │  model.fit(X, y)                 ─►  a loss you can differentiate     w12 │
   │                                      and a loop you write yourself    w15 │
   │  LinearRegression().coef_        ─►  w ← w − lr × slope, plotted       w15 │
   │  a decision tree's if/then       ─►  layers of neurons doing the       w16 │
   │  rules                               same job with arithmetic         w19 │
   │  y = mx + c, slope by rise/run   ─►  the slope of a CURVE, at a       w12 │
   │                                      single point, measured                │
   │  arr.shape from numpy            ─►  shapes that must match, and      w17 │
   │                                      the error when they don't             │
   │  "the model overfit"             ─►  dropout, augmentation, early     w22 │
   │                                      stopping, a train/val curve      w27 │
   │  make_pipeline(Scaler, Model)    ─►  the artifact you save, version,   w3 │
   │                                      log, document and ship           w34 │
   └────────────────────────────────────────────────────────────────────────────┘
```

**Every item in the right-hand column is the inside of something they already drive.** Say that out
loud in Week 1. It is the difference between a year that feels like a promotion and a year that feels
like being handed somebody else's maths homework.

> **💡 Try this:** In Week 1, before you open Python, write `model.fit(X_train, y_train)` on a sheet of
> paper and ask them to list everything that line *does not tell you*. Keep the sheet. In Week 15 they
> will have written the loop that line was hiding, and in Week 20 PyTorch will do it for them again —
> and they will know exactly what it is doing.

---

## 📚 The Three Books

Each week exists in three files. They are different objects with different jobs. Using the wrong one
is the most common way this course goes wrong.

```
   ┌─────────────────────────┬──────────────────────────┬──────────────────────────┐
   │  📕 TEACHER GUIDE       │  📗 STUDENT GUIDE        │  📘 WORKBOOK             │
   │  teacher-guide/week-NN  │  student-guide/week-NN   │  workbook/week-NN.md     │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  WHO READS IT           │                          │                          │
   │  The adult, alone,      │  The student, at the     │  The student, alone,     │
   │  before class           │  keyboard, during and    │  after class             │
   │                         │  after class             │                          │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  WHAT'S IN IT           │                          │                          │
   │  · The 20-minute prep   │  · The hook              │  · 6–10 exercises        │
   │  · 🔢 "THE MATHS YOU    │  · The concept, written  │  · Predict-the-output    │
   │    NEED, TAUGHT TO YOU  │    for a 14-year-old     │    before you run it     │
   │    FIRST" — numerically,│  · 🔢 the maths, slowly, │  · Do-it-by-hand-first   │
   │    on real numbers, no  │    numbers before names  │    arithmetic, then the  │
   │    calculus assumed     │  · Every code block      │    code that checks it   │
   │  · Minute-by-minute     │    complete and runnable │  · The week's build      │
   │    lesson script        │  · The real output in a  │  · A self-check          │
   │  · The EXACT code to    │    separate block        │  · Full answer key at    │
   │    type, and its real   │  · 🐞 this week's error, │    the bottom, sealed    │
   │    output               │    read and fixed        │    behind a "don't look   │
   │  · 🐞 the planted bug   │  · Figures               │    yet" line — every     │
   │    and how to stage it  │  · Vocabulary            │    answer worked in full │
   │  · What students get    │  · Key takeaways         │  · Bug Log page          │
   │    wrong, and the fix   │  · What to do if stuck   │                          │
   │  · Answers to every     │                          │                          │
   │    question they'll ask │                          │                          │
   │  · Marking guidance     │                          │                          │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  WHEN                   │                          │                          │
   │  20 min before class    │  In class + re-read      │  Between classes,        │
   │                         │  during homework         │  ~60–75 min              │
   └─────────────────────────┴──────────────────────────┴──────────────────────────┘
```

**The rules:**

1. **The student never opens the teacher guide.** It contains the answers, the planted bug, and the
   "what they'll get wrong" notes.
2. **The teacher does not skip the teacher guide**, even on weeks that look easy — and *especially* not
   on the fifteen weeks that carry new maths. The section called **🧑‍🏫 The Maths You Need, Taught To You
   First** is written for an adult who has never done calculus, and it works the whole thing on real
   numbers. That section is where your confidence comes from. Read it with a pen.
3. **The workbook answer key is at the bottom of the workbook**, not hidden elsewhere. The student is
   trusted with it and told, in writing, to struggle for fifteen minutes first.
4. **Nobody pastes code.** Not the student, not you. This costs about 15 extra minutes a week and is
   the highest-return 15 minutes in the level.
5. **Every hand calculation gets checked by code, and every code result gets checked by hand at least
   once.** That two-way check is the actual method of this level. It is how you find out that you were
   wrong, and it is the only reason the maths stops being frightening.

### And two folders that are not weekly

| Folder | What is in it | When you open it |
|---|---|---|
| 📝 [**`assessments/`**](assessments/README.md) | Four papers, one per term. 75 minutes, 75 marks, **no computer**. Twenty multiple choice, eight "what does this print / what is this number", four "find and fix the bug", three "do the arithmetic", one extended question. Every paper carries its own marking scheme and a full answer key with real output | After weeks 9, 18 and 27, and in week 36 — plus [`assessments/README.md`](assessments/README.md) for the marking rules and the per-week remediation table |
| 🛠️ [**`projects/`**](projects/project-ideas.md) | [Fifty project ideas](projects/project-ideas.md) that all work offline · [one worked example](projects/worked-example-project.md) taken all the way through by a real student, tracebacks included · [the two-week Ship It capstone](projects/capstone.md) with the scaffold, the seven milestones, the rubric and the demo run-sheet | Any time from week 11 for a project; weeks 34–36 for the capstone |

---

## 🗓️ The Four Terms

Nine weeks each. Each term answers one question, and the student should be able to answer it out loud
at the end — while showing you a file that runs and a number they can reproduce.

```
   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 1  ·  WEEKS 1–9  ·  BUILD IT HONESTLY                               ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  How do you turn a messy table into a model somebody       ║
   ║                 else can load and use — without lying to yourself         ║
   ║                 about the score?                                          ║
   ║                                                                           ║
   ║  Ends with: a saved .joblib artifact plus a model card, an ablation        ║
   ║  table that deleted three of their own ideas for buying nothing, three     ║
   ║  caught leakage bugs, and a metrics report that has stopped saying         ║
   ║  "accuracy" as if it were one thing.                                      ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 2  ·  WEEKS 10–18  ·  INSIDE THE BOX                                ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  What is the machine actually DOING when it learns —       ║
   ║                 and can I do it myself, with a pen and twenty-five        ║
   ║                 lines of numpy?                                           ║
   ║                                                                           ║
   ║  Ends with: 📉 their own gradient descent loop matching sklearn's          ║
   ║  weights to 3 dp, a slope measured with a ruler before it was called a    ║
   ║  derivative, and all four gradient arrays of a neural network computed     ║
   ║  BY HAND and gradient-checked to 1e-6.                                    ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 3  ·  WEEKS 19–27  ·  REAL NETWORKS, REAL FRAMEWORK                 ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  Once you have built a brain by hand, how do you hand      ║
   ║                 the boring part to PyTorch — and teach it to see?         ║
   ║                                                                           ║
   ║  Ends with: 🧠 NumPy Brain, then the same brain in PyTorch proved          ║
   ║  identical, then 👁️ a CNN reading handwritten digits at ~95% with its      ║
   ║  learned first-layer filters rendered as pictures, and honest offline      ║
   ║  transfer learning: freeze the digits 0–4 backbone, retrain on 5–9.        ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 4  ·  WEEKS 28–36  ·  NO LABELS, WORDS, AND SHIP IT                 ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  What can you learn with no answer key, how do you turn    ║
   ║                 words into numbers, and how do you hand the finished      ║
   ║                 thing to a stranger?                                      ║
   ║                                                                           ║
   ║  Ends with: 🗺️ clusters they named and defended from a feature-means       ║
   ║  table, 💬 a sentiment engine whose fifteen most-trusted words they can    ║
   ║  read out loud, and 🚢 a shipped model with a CLI, a service, a log with   ║
   ║  latency, subgroup metrics and a monitoring plan. This is the term the     ║
   ║  whole level was built to earn.                                           ║
   ╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 All 36 Weeks

**Type key:** 🟦 teach · 🟩 lab · 🟨 project · 🟪 review · 🟥 assessment · 🎪 capstone

| Week | Term | Title | Big idea | New maths | New syntax | Type | Homework |
|:--:|:--:|---|---|---|---|:--:|---|
| 1 | 1 | The One Line That Hid Five Decisions | `model.fit(X, y)` was one line hiding five decisions somebody had to make — and this year you make them yourself, on purpose, in writing. | *(none)* | `np.random.default_rng(0)` · `df.duplicated().sum()` · `df["c"].nunique()` · `df["y"].value_counts(normalize=True)` · `X.drop(columns=[c])` · `df.to_string(index=False)` | 🟦 teach | Write the prediction contract for the delivery table: unit of prediction, X named column by column, y, the one metric you commit to, and the four audit numbers — then name the column that must never be a feature |
| 2 | 1 | Practice, Mock Exam, Final Exam | Two piles was training wheels. Real work needs three — one to learn from, one to choose with, and one you open exactly once. | *(none)* | `train_test_split` twice → three piles · `DummyClassifier(strategy="most_frequent")` · `model.predict_proba(X)[:, 1]` · `roc_auc_score(y_val, prob)` | 🟦 teach | Split the table three ways with `stratify`, prove the class balance matches in all three to 3 dp, build both dummy baselines, and write the number your model must beat |
| 3 | 1 | The Artifact Is the Deliverable | What you hand over is not a score, it is a file: a fitted `Pipeline` on disk, plus a card saying what it is and where it breaks. | *(none)* | `Pipeline(steps=[...])` · `ColumnTransformer([...])` · `joblib.dump(pipe, p)` · `joblib.load(p)` | 🟩 lab | Finish `predict.py` — a clean process with zero training code — plus `model_card.md` under seven headings; then delete a required column from the input and paste the real error |
| 4 | 1 | Same Number, Different Ruler | A model compares columns by size, so a column measured in thousands shouts over a column measured in units — until you put them on the same ruler. | **standard deviation** (typical distance from the mean), then the **z-score** `(x − mean) ÷ sd` — both by hand on five numbers | `MinMaxScaler()` · `scaler.mean_` / `scaler.scale_` · `OneHotEncoder(handle_unknown="ignore")` · `OrdinalEncoder(categories=[...])` · `prep.get_feature_names_out()` | 🟦 teach | Ten scaling drills by hand with the sklearn check beside each; then the ordinal-encoding trap — encode weather 0/1/2 and write two sentences on what the model now wrongly believes |
| 5 | 1 | Columns You Invent Yourself | The biggest score jumps usually come from a column that was not in the file — a ratio, a bin, or two columns multiplied together. | *(none)* | `FunctionTransformer(add_features)` · `pd.cut(s, bins=[...], labels=[...])` · `df.assign(new=...)` · `pipe.named_steps["prep"]` · `np.where(cond, a, b)` | 🟦 teach | Build four derived features, run the ablation table (with / without, ΔAUC to 4 dp), and delete the ones that bought nothing — in writing, with the number |
| 6 | 1 | The Answer Was in the Features | A suspiciously perfect score is almost never a great model — it is information leaking in that will not exist when you actually have to predict. | *(none)* | `SimpleImputer(strategy="median")` · `add_indicator=True` · `imp.statistics_` | 🟦 teach | Three leakage repairs, each with the fake number and the honest number; plus the 2,000-column pure-noise experiment run twice — leaky (0.75) then honest |
| 7 | 1 | Beat the Baseline | Improving a model by changing only the features is a discipline: one change, one measurement, one row in the table, no exceptions. | *(none)* | `pipe.set_params(prep__num__scaler=...)` · `pipe.get_params().keys()` | 🟩 lab | Finish the ablation table (six rows minimum), state your best validation AUC, and hunt the planted leak in the supplied `leaky_features.py` |
| 8 | 1 | Four Numbers That Tell You What Kind of Wrong | Accuracy hides *which* mistakes you made. Four counts — caught, false alarm, miss, correctly left alone — tell you what kind of wrong you are. | *(none)* | `make_classification(weights=[0.99, 0.01])` · `confusion_matrix(y, pred).ravel()` · `precision_score` / `recall_score` · `classification_report(y, pred)` | 🟦 teach | Build the 2×2 by hand from 30 given predictions, compute precision, recall and specificity, then describe one false positive and one false negative in the language of the actual application |
| 9 | 1 | **Term 1 Checkpoint — One Number Is Never Enough** | Precision and recall pull against each other, so one score that respects both must punish a lopsided pair. That is what F1 does. | **the harmonic mean** `2·p·r ÷ (p + r)` — and why it drags a lopsided pair towards the smaller number | `f1_score(y, pred)` · `precision_recall_fscore_support(y, pred)` | 🟪 review | Term 1 reflection sheet + the full metrics report for your Week 7 model: 2×2, precision, recall, F1, and a paragraph on which error your application should fear more |
| 10 | 2 | The Threshold Dial, and the Curve It Draws | 0.5 is not a law, it is a default. Turning the dial trades misses for false alarms, and the curve it traces is the model's whole personality. | **steepness of a curve between two points** — rise over run, from two real points on an ROC curve | `(prob >= t).astype(int)` · `roc_curve(y, prob)` · `precision_recall_curve(y, prob)` · `average_precision_score(y, prob)` | 🟦 teach | Sweep nine thresholds into a table of precision, recall and false-alarm count; plot both curves and mark the three thresholds you would defend out loud |
| 11 | 2 | Fraud Bench: What Does a Mistake Cost? | You cannot pick a threshold without a price list. Write down what a miss costs and what a false alarm costs, and the arithmetic picks the threshold for you. | **area under a curve** — added up as trapezoid strips, by hand, on a five-point curve | `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` · `cross_val_score(..., scoring="roc_auc")` · `np.trapz(tpr, fpr)` · `scores.mean()` / `scores.std()` | 🟩 lab | Finish Fraud Bench: the cost table for nine thresholds with the winner circled, 5-fold AUC as mean ± sd, and one sentence saying what the ± is for |
| 12 | 2 | How Steep Is the Hill Right Here? | In Level 2 sklearn found the best slope for a line and never said how. It tried a value, asked "which way is downhill", and stepped. You can measure "downhill" with two subtractions. | **the slope of a curve at ONE point**, measured by nudging: `(f(w+h) − f(w−h)) ÷ 2h` — and only then called a **derivative** | `np.linspace(a, b, n)` · `np.argmin(arr)` · `ax.annotate("...", xy=(x, y))` | 🟦 teach | Numeric slopes of three functions at three points (nine answers) with the shortcut rule beside each; then six steps of `w ← w − 0.3 × slope` on `(w − 4)²`, tabulated by hand |
| 13 | 2 | From a Score to a Chance | A weighted sum can be any number at all. A probability has to sit between 0 and 1. The sigmoid is the squasher that gets you from one to the other. | **the exponential `e^(−z)`** — evaluated for z = −2, 0, 1.4, 3, then drawn as the S-curve; then **`ln` as the undo button for `e`**, because going backwards from a chance to a score needs it (`z = ln(odds)`) | `np.exp(x)` · `np.log(x)` | 🟦 teach | Eight sigmoid conversions by hand to 4 dp, four backwards (probability → z via log-odds), and the overflow experiment: `σ(−1000)` naively, then with the two-branch fix |
| 14 | 2 | Measuring How Wrong You Are | Squared error rates a confident disaster only 2.7× worse than a near-miss. Log loss rates it 4.3× worse and keeps going — which is why classifiers use it. | **the natural logarithm `ln`** as a surprise meter: `−ln(p)` for p = 0.9, 0.5, 0.1, 0.02 | `np.clip(p, 1e-12, 1 - 1e-12)` · `log_loss(y, prob)` · `-np.mean(...)` | 🟦 teach | Log loss for six predictions by hand with the squared error beside each; then explain in three sentences why 0.6931 is the loss of a model that answers 0.5 to everything |
| 15 | 2 | Rolling Downhill: Descent From Scratch | Training is a loop: get the slope for every knob, step every knob a little way against its slope, repeat. That loop is what `fit()` was doing all along. | **the gradient** — one slope per knob, listed together, and `w ← w − lr × slope` applied to all of them at once | `(X * w).sum(axis=1)` · `w -= lr * grad` · `ax.set_yscale("log")` | 🟩 lab | Finish Descent From Scratch, match sklearn's weights to 3 dp, and diagnose four supplied loss curves by name: too small, too big, converged, diverged |
| 16 | 2 | One Neuron, By Hand | A neuron is three things you already do: multiply each input by a weight, add them up with a bias, then squash. Stacking them is only interesting *because* of the squash. | **the shape of a grid of numbers** — rows × columns, written `(3, 2)`, and why the shape is the first thing you print | `np.maximum(0, z)` · `np.tanh(z)` · `arr.reshape(r, c)` · `arr.T` · `make_moons(n_samples=400, noise=0.25, random_state=0)` | 🟦 teach | Compute six neuron outputs by hand for ReLU, sigmoid and tanh — eighteen numbers — and check all eighteen in numpy; then state the shape of eight arrays *before* running anything |
| 17 | 2 | A Layer Is a Grid Times a Grid | A whole layer for a whole batch is one operation — a grid times a grid — and it only works when the inner numbers of the two shapes match. | **multiplying two grids**: `(3,2) @ (2,4) → (3,4)`, inner numbers must match — computed cell by cell on real 3×2 numbers | `A @ B` · `arr.sum(axis=1, keepdims=True)` · `np.allclose(a, b)` | 🟦 teach | Full forward pass for a (4,2) batch through 2→3→1 by hand with every intermediate grid written out, then in numpy; plus five deliberate shape mismatches with the real error pasted for each |
| 18 | 2 | **Term 2 Checkpoint — How Much Did Each Knob Contribute?** | Backpropagation is blame assignment. Slopes multiply along a path, so you can work out how much each of a hundred knobs contributed to the error in one sweep backwards. | **slopes multiply along a chain**: if nudging w moves z 3× and nudging z moves L 14×, then w moves L 42× — measured both ways and shown to agree | `A.T @ dZ` · `(z > 0).astype(float)` | 🟪 review | Term 2 reflection sheet; compute all four gradient arrays for a 2→2→1 network by hand, then gradient-check every one to a relative error below `1e-6` and paste the numbers |
| 19 | 3 | NumPy Brain | Forty lines of numpy, no framework, and a boundary that actually curves. You have now built the thing everybody else imports. | *(none)* | `np.meshgrid(xx, yy)` · `np.c_[a.ravel(), b.ravel()]` · `ax.contourf(...)` · `np.abs(a - b).max()` | 🟨 project | Finish NumPy Brain to >90% test accuracy with the gradient check passing; the boundary plotted at epochs 0, 50 and 500; and a count of dead ReLUs in the `lr = 20` run |
| 20 | 3 | A Machine That Does the Slopes For You | A tensor is a numpy array that remembers what was done to it — so it can hand you back every slope you spent last week computing by hand. | *(none)* | `torch.tensor([...], requires_grad=True)` · `loss.backward()` · `w.grad` · `t.item()` | 🟦 teach | Ten autograd exercises with your hand answer beside each; then the `.item()` experiment — build a list of 200 losses the wrong way, watch memory grow, fix it in one character |
| 21 | 3 | The Five-Line Loop | Every training run in every framework is the same five lines in the same order — and each one has a specific failure if you drop it. | *(none)* | `torch.optim.SGD([w], lr=0.1)` · `optimizer.zero_grad()` · `optimizer.step()` · `with torch.no_grad():` | 🟦 teach | Fit `y = 8x + 12` from six points with the five-line loop; then delete each line in turn and record what happened in a five-row table — including the one that gives no error at all |
| 22 | 3 | Layers, Losses, and Watching It Overfit | `nn.Linear` is the grid multiply plus the bias you wrote by hand, and the losses with "WithLogits" in the name do the squash for you, safely. | *(none)* | `nn.Linear(n_in, n_out)` · `nn.ReLU()` · `nn.Sequential(...)` · `nn.BCEWithLogitsLoss()` · `sum(p.numel() for p in model.parameters())` · `torch.from_numpy(a).float()` · `torch.optim.Adam(model.parameters(), lr=1e-3)` · `model.eval()` / `model.train()` | 🟦 teach | Rebuild Week 19's architecture in `nn.Sequential` and prove the parameter shapes are identical; then the train/val loss plot with the epoch where validation stopped improving marked |
| 23 | 3 | Same Brain, Real Framework | A model you cannot reload in a fresh process is not finished. Weights go in a file, the architecture goes in a module both scripts import, and `predict.py` has no training code. | *(none)* | `class Net(nn.Module)` + `super().__init__()` + `forward` · `TensorDataset` + `DataLoader(..., shuffle=True)` · `torch.save(model.state_dict(), p)` + `load_state_dict` | 🟩 lab | Finish the digits MLP and its `predict.py`; count the optimizer steps in one epoch three different ways and make the arithmetic agree; then the `model.eval()` experiment — same input, five predictions, before and after |
| 24 | 3 | Why Flattening a Picture Throws Away the Picture | Flattening tells the model that the pixel above and a pixel across the room are equally related. A convolution is a small grid of weights that slides — and it keeps the neighbourhood. | *(none)* | `t.unsqueeze(0)` · `nn.Conv2d(1, 4, kernel_size=3)` · `conv.weight.data = ...` · `conv.bias.data = torch.zeros(1)` | 🟦 teach | Build four images in numpy, apply three hand-written kernels, save the twelve feature maps as one figure with a sentence per kernel; plus the parameter-count comparison, dense vs conv, with both numbers |
| 25 | 3 | Work Out the Size Before You Run It | Every conv and pool layer changes height and width by a rule you can do on paper — and if you cannot do it on paper, the shape error will find you. | **the output-size rule** `(n + 2p − k) ÷ s + 1`, rounded down — checked by counting window positions on an 8×8 grid by hand | `nn.Conv2d(..., stride=2, padding=1)` · `nn.MaxPool2d(2)` · `nn.Flatten()` · `t.view(t.size(0), -1)` | 🟦 teach | Twelve output-size calculations by hand with the printed shape beside each; then deliberately mis-size the `Linear` after `Flatten` and paste the real error, naming both numbers in it |
| 26 | 3 | A Network That Reads Digits | Once shapes stop being a mystery, a CNN is a short stack — conv, squash, pool, repeat, flatten, classify — and its first-layer filters are pictures you can look at. | *(none)* | `nn.CrossEntropyLoss()` · `logits.argmax(dim=1)` · `torch.softmax(scores, dim=1)` · `time.perf_counter()` | 🟦 teach | Train the CNN, report train and test accuracy, save the filter grid, and compare it against the Week 23 dense MLP in a four-row table: parameters, seconds, train accuracy, test accuracy |
| 27 | 3 | **Term 3 Checkpoint — See It** | You can buy accuracy two ways without collecting a single new image: make more training pictures out of the ones you have, and reuse a network that already learned to see. | *(none)* | `np.roll(img, shift, axis=0)` · `p.requires_grad = False` · `ConfusionMatrixDisplay.from_predictions(...)` · `torch.cat([...])` | 🟪 review | Term 3 reflection sheet + the See It results table (plain, augmented, frozen-transfer, fine-tuned) and a written diagnosis of the worst confusion pair with a *physical* reason |
| 28 | 4 | Sorting With No Answer Key | Two steps, repeated: give every point to its nearest centre, then move every centre to the middle of what it got. That is the whole algorithm. | **sigma notation `Σ`** as shorthand for "add up all of these", written out in full beside the symbol every single time — introduced on inertia over six points | `KMeans(n_clusters=3, n_init=10, random_state=0)` · `km.cluster_centers_` · `km.inertia_` · `km.labels_` | 🟦 teach | Two iterations by hand on eight given points with all sixteen squared distances shown; then the scaling experiment on `load_wine` — cluster unscaled and scaled, and explain in two sentences why one column took over |
| 29 | 4 | A New Pair of Axes | PCA does not delete columns. It draws a new axis along the direction the data is most spread out, and measures everything against that instead. | **variance** as the average squared distance from the mean — and "the direction of biggest spread" found by trying angles and keeping the widest | `PCA(n_components=2)` · `pca.explained_variance_ratio_` · `pca.components_` · `pca.inverse_transform(Z)` | 🟦 teach | PCA on `load_wine`: explained variance for all thirteen components as a table, the 2-D projection plot, the top three loadings of PC1 with a human name for the axis, and the reconstruction error at 2 vs 6 components |
| 30 | 4 | Cluster Cartography | A cluster is not a result until it has a human name backed by a feature-means table — and two independent pieces of evidence for how many clusters there are. | *(none)* | `silhouette_score(X, labels)` · `silhouette_samples(X, labels)` · `adjusted_rand_score(a, b)` · `km.transform(X)` | 🟩 lab | Finish Cluster Cartography — elbow plot, silhouette plot, PCA scatter coloured by cluster, feature-means table, three defended names — then add cluster ID + two PCs as features to a supervised model and report whether it helped, with the number |
| 31 | 4 | Words Into Columns | A model only eats numbers, so a review becomes a row of word counts — and the moment you do that, word order is gone. | *(none)* | `re.findall(r"\b\w\w+\b", text)` · `text.lower()` · `CountVectorizer()` · `vec.get_feature_names_out()` · `X.toarray()` · `np.argsort(counts)` | 🟦 teach | Tokenize six sentences by hand and by regex and list every disagreement; build the count matrix for five reviews by hand; then find one normalization choice that would be *wrong* for your corpus and say why |
| 32 | 4 | Rare Words Matter More | "the" appears everywhere and tells you nothing. TF-IDF multiplies how often a word appears by how rare it is, then measures documents by the angle between them. | **cosine similarity** — the dot product of two lists divided by both their lengths, worked by hand on two 3-number vectors, and what 0.726 means as an angle | `TfidfVectorizer(...)` · `cosine_similarity(A, B)` · `normalize(v)` · `np.degrees(np.arccos(c))` | 🟦 teach | Compute four TF-IDF weights by hand matching sklearn to 4 dp, and three cosine similarities by hand; then show with one example pair that raw counts rank the wrong document first and cosine fixes it |
| 33 | 4 | Sentiment Engine | A TF-IDF classifier will tell you the fifteen words it learned to trust — and the review it gets wrong will be the one where word order was the whole meaning. | *(none)* | `TfidfVectorizer(ngram_range=(1, 2))` · `make_pipeline(vec, clf)` · `clf.coef_[0]` (Level 2, used hard here) · `DummyClassifier` on text | 🟩 lab | Finish Sentiment Engine: per-class precision and recall, top fifteen positive and negative words, a PCA plot of the reviews, a unigram-vs-bigram table, and a post-mortem of one wrong prediction that names word order as the cause |
| 34 | 4 | Ship It, Part 1: The Contract and the Artifact | A model somebody else can use starts with a written contract: what one prediction is about, what goes in, what comes out, and what this must never be used for. | *(none)* | `argparse.ArgumentParser()` · `json.dump` / `json.load` · `Path(...).mkdir(parents=True, exist_ok=True)` · `sys.path.insert(0, ...)` | 🎪 capstone | Capstone milestones 1–3: the contract, the frozen artifact with a version file, a `predict.py` CLI that runs from a cold start with zero training code, and three passing golden tests |
| 35 | 4 | Ship It, Part 2: The Service, the Log, and the Card | The interesting part of shipping is what happens *after* the prediction: it gets logged with its inputs and its latency, and somebody can read that log and tell you what is going wrong. | *(none)* | `http.server.BaseHTTPRequestHandler` · `HTTPServer(("127.0.0.1", 8000), H)` · `logging.basicConfig(filename=...)` · `np.percentile(latencies, 95)` | 🎪 capstone | Capstone milestones 4–7: a local service that survives all four malformed requests, 100+ log lines, p95 latency, a subgroup metrics table, the full model card, and the one-page monitoring plan |
| 36 | 4 | Showcase Day and the Final Paper | You can hand a stranger a model, a card that says where it breaks, and a log that proves it ran — and you can defend every number in it. | *(none)* | *(none — the year is the syntax)* | 🟥 assessment | No new homework — complete the Level 4 gate self-check and write the letter to yourself about what you want to build next |

---

## 📆 Year at a Glance

```
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 1 · BUILD IT HONESTLY          "A model they can use — honestly?"      │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │  W1  │  W2  │  W3  │  W4  │  W5  │  W6  │  W7  │  W8  │  W9  │             │
   │ 🟦   │ 🟦   │ 🟩📦 │ 🟦🔢 │ 🟦   │ 🟦🔑 │ 🟩   │ 🟦   │ 🟪🔢 │             │
   │ five │train │PIPE- │ z-   │ new  │ LEAK-│BEAT  │ TP FP│ ✦CHK │             │
   │decis-│ val  │LINE  │score │ cols │ AGE  │ THE  │ FN TN│POINT │             │
   │ ions │ test │ v1   │ 1-hot│ablat.│ 0.978│BASEL.│ prec │  F1  │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │  ──── module 1 ────   ───────── module 2 ─────────   ── module 3 starts ──   │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 2 · INSIDE THE BOX             "What is it DOING when it learns?"      │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W10  │ W11  │ W12  │ W13  │ W14  │ W15  │ W16  │ W17  │ W18  │             │
   │ 🟦🔢 │ 🟩🔢 │ 🟦📐 │ 🟦🔢 │ 🟦🔢 │ 🟩⚡ │ 🟦🔢 │ 🟦🔢 │ 🟪🔑 │             │
   │thres-│FRAUD │SLOPE │ sig- │ log  │DESC- │ one  │  A@B │ ✦CHK │             │
   │ hold │BENCH │ at a │ moid │ loss │ ENT  │neuron│shapes│POINT │             │
   │ ROC  │ cost │POINT │ e^-z │  ln  │ w-=  │shape │ must │BACK- │             │
   │ dial │ k-CV │ =2w? │log-od│ vs SE│lr*g  │ ReLU │match │ PROP │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │  ─ module 3 ends ─   ────────── module 4 ──────────   ─ module 5 starts ──   │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 3 · REAL NETWORKS, REAL FRAMEWORK   "Hand the boring part over?"       │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W19  │ W20  │ W21  │ W22  │ W23  │ W24  │ W25  │ W26  │ W27  │             │
   │ 🟨🧠 │ 🟦⚡ │ 🟦   │ 🟦   │ 🟩📦 │ 🟦   │ 🟦🔢 │ 🟦👁️ │ 🟪   │             │
   │NUMPY │auto- │ FIVE │ nn.  │ SAME │conv- │strid │ CNN  │ ✦CHK │             │
   │BRAIN │ grad │ LINE │Linear│BRAIN │olve  │ pad  │reads │POINT │             │
   │moons │.back │ LOOP │Sequen│ +    │ by   │ size │digit │SEE IT│             │
   │gradck│ ward │zero_g│drop  │DIGITS│ hand │ rule │95.3% │aug/TL│             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │ ─m5 ends─   ───────── module 6 ─────────   ────────── module 7 ──────────    │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 4 · NO LABELS, WORDS, AND SHIP IT   "Hand it to a stranger?"           │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W28  │ W29  │ W30  │ W31  │ W32  │ W33  │ W34  │ W35  │ W36  │             │
   │ 🟦🔢 │ 🟦🔢 │ 🟩🗺️ │ 🟦   │ 🟦🔢 │ 🟩💬 │ 🎪   │ 🎪   │ 🟥🎓 │             │
   │k-mean│ PCA  │CLUST-│tokens│TF-IDF│SENTI-│SHIP  │SHIP  │SHOW- │             │
   │assign│ new  │ ER   │ bag- │cosine│MENT  │ IT   │ IT   │CASE  │             │
   │ move │ axes │CARTO-│  of- │n-gram│ENGINE│ p1   │ p2   │  +   │             │
   │  Σ   │varian│GRAPHY│ words│ angle│ traps│contr.│serve │PAPER │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │ ────── module 8 ──────   ────── module 9 ──────   ─ CAPSTONE ─  ─ FINAL ─    │
   └─────────────────────────────────────────────────────────────────────────────┘

   LEGEND
   🟦 teach — new idea, worked example, everyone types
   🟩 lab   — hands-on build, end to end, it runs by the end of class
   🟨 proj  — a program gets finished and handed in
   🟪 review— term checkpoint: consolidation + drills + one new idea
   🟥 test  — the final assessment
   🎪 capstone
   🔢 a week that carries ONE new mathematical idea (15 of 36 weeks)
   📐 THE week the derivative arrives — measured with a ruler, named afterwards
   ⚡ the two "it works and I built it" weeks (w15 own descent, w20 autograd matches)
   🔑 the two most important lessons in the level (w6 leakage, w18 backprop)
   📦 the two weeks a model becomes a FILE somebody else can load
   🧠 the week the neural network exists with no framework under it
   👁️ the week a network reads handwriting
   ✦  term checkpoint week
```

> **⚠️ Watch out — the two structural warnings for this year.**
>
> **1. Do not skip or rush Week 12.** Everything from Week 15 to Week 27 stands on the idea that you
> can measure how steep a curve is at one point by nudging and dividing. A student who leaves Week 12
> without having done that arithmetic *with their own pencil* will experience the rest of the year as
> memorising incantations. If Week 12 needs two weeks, take two weeks and compress Week 5 instead.
>
> **2. Do not teach Weeks 18 and 20 in the same week.** Week 18 is four gradient arrays computed by
> hand — genuinely hard, genuinely tiring, and the proudest moment of the year. Week 20 is PyTorch
> producing all four of them in one line. That gap needs the pride to sit in it for seven days, or the
> lesson becomes *"so that was pointless then"*. It was not pointless. It is the only reason
> `loss.backward()` will ever mean anything.

---

## 🪜 The Maths Ladder

**This is the most important table in this file.** Every mathematical idea in Level 3, in the week it
first appears. At most one per week, and 21 of the 36 weeks add none.

Use it two ways:
- **"Have we met derivatives yet?"** → search the table, read the week number. Five seconds.
- **A student uses an idea you don't recognise** → find it here. If its week is *after* this week, they
  got it from somewhere else, and the honest move is: *"Nice — where did you find that? We meet it
  properly in week 12. Can you explain it to me?"*

### Already theirs, from Levels 1 and 2 — assumed, never re-taught

| Idea | Plain meaning |
|---|---|
| Fractions, percentages, negative numbers | — |
| Mean and median | Add up and divide · the middle value of a sorted list |
| `y = mx + c` | A straight line: `m` is how steep, `c` is where it crosses |
| Slope of a **straight** line | Rise over run — how far up divided by how far along |
| Reading a labelled graph | Which axis is which, and what one dot means |
| Accuracy = correct ÷ total | — |
| A little trigonometry | Angles, and that sin and cos exist |

### New in Level 3, in order

| Week | The idea | What it means, in one plain line |
|:--:|---|---|
| 4 | **Standard deviation** | The typical distance of a value from the mean of its column |
| 4 | **z-score** | How many typical distances above or below the mean one value sits |
| 9 | **Harmonic mean** | An average that gets dragged down towards the smaller of the two numbers |
| 10 | **Steepness between two points** | Rise over run, but now on a *curve*: how much it climbed, divided by how far along you went |
| 11 | **Area under a curve** | Chop the space underneath into trapezoid strips and add them up |
| **12** | **Slope at a single point → the DERIVATIVE** | Nudge the input by a hair, see how far the output moved, divide. That number is which way is downhill and how steeply |
| 13 | **The exponential `e^(−z)`** | A number that shrinks fast as `z` grows. The ingredient inside the sigmoid squasher |
| 14 | **The natural logarithm `ln`** | A surprise meter: `−ln(0.9)` is 0.105 (barely surprised), `−ln(0.02)` is 3.912 (astonished) |
| 15 | **The gradient** | One slope per knob, listed together. Step every knob the opposite way and the error goes down |
| 16 | **The shape of a grid of numbers** | Rows × columns, written `(3, 2)`. The first thing you print, every time |
| 17 | **Multiplying two grids** | Rows of the left meet columns of the right. `(3,2) @ (2,4) → (3,4)`. The inner two numbers must match or nothing happens |
| 18 | **Slopes multiply along a chain** | If nudging `w` moves `z` 3× and nudging `z` moves `L` 14×, then nudging `w` moves `L` 42×. This is all backpropagation is |
| 25 | **The output-size rule** | `(n + 2p − k) ÷ s + 1`, rounded down. How big a picture is after a layer has slid over it |
| 28 | **Sigma notation `Σ`** | Shorthand for "add up all of these". Always written out in full beside the symbol in this course |
| 29 | **Variance** | The average squared distance from the mean. How spread out a column is |
| 32 | **Cosine similarity** | The angle between two rows of numbers, ignoring how long either row is. 1.0 means same direction |

### Deliberately NOT in this level — so you can say "not yet" with confidence

Limits · continuity · epsilon-delta anything · proofs of any kind · symbolic differentiation as a
skill (the shortcut rules appear only to *check* a number you already measured) · the chain rule as
symbol manipulation · integrals and antiderivatives (Week 11's area is trapezoid strips and stays
that way) · matrix inverses · determinants · eigenvectors and eigenvalues as algebra (Week 29's PCA
is *"try angles, keep the widest"*, and that is honest and enough) · vector notation with arrows or
bold · summation index gymnastics · big-O.

> **🧑‍🏫 If a student asks** *"is this real calculus?"* — Yes. The number you measured in Week 12 by
> nudging is exactly the number a calculus class computes with rules, and Week 12 proves it on three
> functions. What a calculus class adds is speed and generality. What you did is the meaning. People
> who have only the rules routinely cannot answer "so which way is downhill?" — and you can.

---

## 🪜 The Syntax Ladder

Every Python, numpy, pandas, matplotlib, scikit-learn and PyTorch construct in Level 3, in the week
it first appears. **Nothing is ever used before the week it appears here.** Maximum four per week.

Everything from the [Level 2 syntax ladder](../../level-2-builder/36-week-course/README.md#-the-syntax-ladder)
is assumed and never re-taught: `print`, variables, f-strings, `if`/`elif`/`else`, `for`, `while`,
`def`/`return`, lists, dicts, list comprehensions, `import`, `numpy` arrays and axes, boolean masks,
`pandas` DataFrames, `loc`/`iloc`, `groupby`, `matplotlib` `fig, ax`, `train_test_split`,
`StandardScaler`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `LinearRegression`,
`accuracy_score`, `confusion_matrix`, `mean_absolute_error`, `r2_score`, `load_iris`, `load_wine`,
`load_diabetes`.

| Week | New construct | What it does in one line |
|:--:|---|---|
| 1 | `np.random.default_rng(0)` | A random-number generator with a fixed seed, so your table is the same every run |
| 1 | `df.duplicated().sum()` | How many rows are exact copies of an earlier row |
| 1 | `df["col"].nunique()` | How many different values a column has. Nearly as many as rows = an ID column |
| 1 | `df["y"].value_counts(normalize=True)` | The fraction of rows in each class |
| 2 | `train_test_split` called **twice** | Three piles instead of two: train, validation, test |
| 2 | `DummyClassifier(strategy="most_frequent")` | The dumbest possible model. The number you must beat |
| 2 | `model.predict_proba(X)[:, 1]` | The model's probability for class 1, not just its yes/no answer |
| 2 | `roc_auc_score(y, prob)` | How well the model *ranks* positives above negatives. 0.5 is a coin flip |
| 3 | `Pipeline(steps=[...])` | Preprocessing and model welded into one object that can only be fitted together |
| 3 | `ColumnTransformer([...])` | Different preprocessing for different columns, selected **by name** |
| 3 | `joblib.dump(pipe, "m.joblib")` | Write the fitted model to a file |
| 3 | `joblib.load("m.joblib")` | Read it back in a completely separate program |
| 4 | `MinMaxScaler()` | Squash a column into the range 0 to 1 |
| 4 | `scaler.mean_` / `scaler.scale_` | The two numbers the scaler learned from the training rows |
| 4 | `OneHotEncoder(handle_unknown="ignore")` | One yes/no column per category; an unseen category becomes all zeros instead of a crash |
| 4 | `OrdinalEncoder(categories=[...])` | Categories become 0, 1, 2 — only safe when they really are a ladder |
| 5 | `FunctionTransformer(add_features)` | Wraps your own function so it can live inside a Pipeline |
| 5 | `pd.cut(s, bins=[...], labels=[...])` | Chop a number column into named ranges |
| 5 | `df.assign(new=...)` | Return a copy of the table with one more column, without touching the original |
| 5 | `pipe.get_feature_names_out()` | The real names of the columns your pipeline produced |
| 6 | `SimpleImputer(strategy="median")` | Fill in blanks with a number learned from the training rows only |
| 6 | `add_indicator=True` | Also add a 0/1 column saying "this one was blank" |
| 6 | `pipe.named_steps["prep"]` | Reach inside a fitted Pipeline and look at one step |
| 7 | `pipe.set_params(a__b__c=...)` | Change one setting deep inside a Pipeline without rebuilding it |
| 7 | `X.drop(columns=[c])` | The same table with one column removed. The core move of an ablation |
| 7 | `df.to_string(index=False)` | Print a whole DataFrame without the row numbers |
| 8 | `make_classification(weights=[0.99, 0.01])` | Generate a table where one class is 1% of the rows |
| 8 | `confusion_matrix(y, pred).ravel()` | The four counts as four separate numbers: TN, FP, FN, TP |
| 8 | `precision_score` / `recall_score` | The two fractions, computed for you |
| 8 | `classification_report(y, pred)` | Precision, recall and F1 for every class, in one printout |
| 9 | `f1_score(y, pred)` | The harmonic mean of precision and recall |
| 9 | `precision_recall_fscore_support(y, pred)` | All four numbers at once, per class, as arrays |
| 10 | `(prob >= t).astype(int)` | Turn probabilities into yes/no at **your** threshold, not 0.5 |
| 10 | `roc_curve(y, prob)` | False positive rate, true positive rate and the thresholds that produced them |
| 10 | `precision_recall_curve(y, prob)` | The other curve — the one to trust when positives are rare |
| 10 | `average_precision_score(y, prob)` | The area under the precision-recall curve |
| 11 | `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` | Five held-out chunks, each keeping the class proportions |
| 11 | `cross_val_score(pipe, X, y, cv=skf, scoring="roc_auc")` | Five scores instead of one lucky one |
| 11 | `np.trapz(y, x)` | Area under a curve, by trapezoid strips |
| 11 | `scores.mean()` / `scores.std()` | The average and the wobble. Always report both |
| 12 | `np.linspace(a, b, n)` | `n` evenly spaced numbers from `a` to `b`. How you draw a curve |
| 12 | `np.argmin(arr)` | The *position* of the smallest value, not the value |
| 12 | `ax.annotate("text", xy=(x, y))` | Write a label at an exact point on a chart |
| 13 | `np.exp(x)` | `e` to the power of `x`, for a whole array at once |
| 13 | `np.where(cond, a, b)` | Elementwise if/else across an array |
| 14 | `np.log(x)` | The natural logarithm, `ln`, for a whole array |
| 14 | `np.clip(p, 1e-12, 1 - 1e-12)` | Nudge values away from exactly 0 and exactly 1, so `ln` never blows up |
| 14 | `log_loss(y, prob)` | sklearn's log loss, to check the one you computed by hand |
| 15 | `(X * w).sum(axis=1)` | A weighted sum for every row at once — the long way, before `@` exists |
| 15 | `w -= lr * grad` | The update rule, in code. The single most important line of the year |
| 15 | `ax.set_yscale("log")` | Squash a y-axis so a loss falling from 800 to 0.4 is readable |
| 16 | `np.maximum(0, z)` | ReLU: keep positives, flatten negatives to zero |
| 16 | `np.tanh(z)` | The other S-curve, running from −1 to +1 |
| 16 | `arr.reshape(r, c)` | The same numbers, arranged in a different grid |
| 16 | `arr.T` | Flip a grid on its diagonal: `(3, 2)` becomes `(2, 3)` |
| 17 | `A @ B` | Matrix multiply. A whole layer for a whole batch, in one symbol |
| 17 | `arr.sum(axis=1, keepdims=True)` | Sum across each row but keep the result 2-D, so it still broadcasts |
| 17 | `np.allclose(a, b)` | "Are these two arrays the same to within floating-point noise?" |
| 18 | `A.T @ dZ` | The backward-pass shape. Transpose, then multiply |
| 18 | `(z > 0).astype(float)` | ReLU's own slope: 1 where it fired, 0 where it did not |
| 19 | `make_moons(n_samples=400, noise=0.25, random_state=0)` | Two interleaving crescents. Not separable by a straight line, on purpose |
| 19 | `np.meshgrid(xx, yy)` | Every point on a grid, so you can colour a whole plane |
| 19 | `np.c_[a.ravel(), b.ravel()]` | Glue two flattened grids into a two-column table of points |
| 19 | `ax.contourf(XX, YY, Z)` | Fill a plane with colour by value. How a decision boundary gets drawn |
| 20 | `torch.tensor([...], requires_grad=True)` | A number PyTorch will track, so it can tell you its slope later |
| 20 | `loss.backward()` | Walk the recording backwards and fill in every slope |
| 20 | `w.grad` | Where the slope PyTorch computed actually lands |
| 20 | `t.item()` | Pull a plain Python number out of a one-value tensor. Forget this and you leak memory |
| 21 | `torch.optim.SGD([w], lr=0.1)` | The object that owns your knobs and knows how to nudge them |
| 21 | `optimizer.zero_grad()` | Wipe last round's slopes. Skip it and they silently pile up |
| 21 | `optimizer.step()` | Apply `w -= lr * grad` to every knob at once |
| 21 | `with torch.no_grad():` | "Don't record any of this" — for measuring, not learning |
| 22 | `nn.Linear(n_in, n_out)` | One layer: a weight grid plus a bias, already initialised |
| 22 | `nn.ReLU()` | The Week 16 squash, as a layer you can stack |
| 22 | `nn.Sequential(...)` | Layers in a straight line, run top to bottom |
| 22 | `nn.BCEWithLogitsLoss()` | Log loss for yes/no answers, applying the sigmoid itself, safely |
| 23 | `class Net(nn.Module)` + `super().__init__()` + `forward(self, x)` | Your own network as a named object, so both scripts can import the same shape |
| 23 | `TensorDataset(X, y)` + `DataLoader(ds, batch_size=32, shuffle=True)` | Turn tensors into shuffled batches you loop over |
| 23 | `model.eval()` / `model.train()` | Switch between measuring behaviour and learning behaviour |
| 23 | `torch.save(model.state_dict(), p)` + `model.load_state_dict(torch.load(p))` | Weights out to a file, and back into a rebuilt architecture |
| 24 | `torch.from_numpy(a).float()` | Turn a numpy array into a float tensor. The dtype fix, in advance |
| 24 | `t.unsqueeze(0)` | Add a size-1 dimension at the front, because Conv2d insists on a batch |
| 24 | `nn.Conv2d(1, 4, kernel_size=3)` | Four sliding 3×3 filters over a one-channel image |
| 24 | `conv.weight.data = ...` | Force your own hand-written kernel into a layer, so you can check its output |
| 25 | `nn.Conv2d(..., stride=2, padding=1)` | Jump two pixels at a time · add a ring of zeros so the window reaches the edges |
| 25 | `nn.MaxPool2d(2)` | Keep only the biggest value in each 2×2 square. No weights to learn |
| 25 | `nn.Flatten()` | Turn `(n, 8, 4, 4)` into `(n, 128)` so a Linear layer can take it |
| 25 | `t.view(t.size(0), -1)` | The same flatten, done by hand, with `-1` meaning "work it out" |
| 26 | `nn.CrossEntropyLoss()` | Log loss for many classes, applying softmax itself |
| 26 | `logits.argmax(dim=1)` | Which of the ten scores was highest, per row |
| 26 | `torch.optim.Adam(model.parameters(), lr=1e-3)` | An optimizer that adapts the step size per knob |
| 26 | `sum(p.numel() for p in model.parameters())` | Count every learnable number in the model |
| 27 | `np.roll(img, shift, axis=0)` | Shift an image by a pixel or two — augmentation with no download |
| 27 | `p.requires_grad = False` | Freeze a layer. Transfer learning's one essential move |
| 27 | `ConfusionMatrixDisplay.from_predictions(y, pred)` | The ten-class confusion matrix, drawn |
| 27 | `torch.cat([a, b])` | Stack tensors end to end — your original images plus the shifted copies |
| 28 | `KMeans(n_clusters=3, n_init=10, random_state=0)` | Find three groups with no labels, ten times, keep the best |
| 28 | `km.cluster_centers_` | The three centre points it settled on |
| 28 | `km.inertia_` | Total squared distance from every point to its own centre. Smaller is tighter |
| 28 | `km.labels_` | Which group each row ended up in |
| 29 | `PCA(n_components=2)` | Two new axes, chosen along the data's biggest spreads |
| 29 | `pca.explained_variance_ratio_` | What share of the total spread each new axis captured |
| 29 | `pca.components_` | How much each original column contributed to each new axis |
| 29 | `pca.inverse_transform(Z)` | Rebuild the original columns from the few you kept, so you can measure what you lost |
| 30 | `silhouette_score(X, labels)` | −1 to +1: how much closer points are to their own cluster than the next one |
| 30 | `silhouette_samples(X, labels)` | The same, per point, so you can see which points are badly placed |
| 30 | `adjusted_rand_score(a, b)` | Do two different groupings agree? 1.0 = identical, 0.0 = chance |
| 30 | `km.transform(X)` | Distance from every row to every centre — three brand-new features |
| 31 | `re.findall(r"\b\w\w+\b", text)` | Chop a string into words of two letters or more |
| 31 | `text.lower()` | Make everything lower case, so `GREAT` and `great` match |
| 31 | `CountVectorizer()` | Turn a list of documents into a table of word counts |
| 31 | `vec.get_feature_names_out()` | The vocabulary, in the column order the matrix uses |
| 32 | `TfidfVectorizer()` | Counts, weighted by rarity, then row-normalised |
| 32 | `cosine_similarity(A, B)` | The angle between every pair of rows |
| 32 | `X.toarray()` | Turn a sparse matrix into a normal one so you can read it |
| 32 | `normalize(v)` | Scale a row so its length is exactly 1 |
| 33 | `TfidfVectorizer(ngram_range=(1, 2))` | Single words *and* pairs of words, so `not good` can be one feature |
| 33 | `make_pipeline(vec, clf)` | Vectorizer and classifier welded together, so the vocabulary can only come from training rows |
| 33 | `clf.coef_[0]` | The weight the classifier learned for every word |
| 33 | `np.argsort(coefs)[:15]` | The fifteen positions of the smallest values — the fifteen most negative words |
| 34 | `argparse.ArgumentParser()` | Read arguments off the command line, so your model has a real CLI |
| 34 | `json.dump` / `json.load` | Write and read structured data as text |
| 34 | `time.perf_counter()` | A high-resolution stopwatch. How latency gets measured |
| 34 | `Path(...).mkdir(parents=True, exist_ok=True)` | Create the folders your artifact lives in, safely |
| 35 | `http.server.BaseHTTPRequestHandler` | Answer an HTTP request with standard library only |
| 35 | `HTTPServer(("127.0.0.1", 8000), Handler)` | Listen on your own machine, and only your own machine |
| 35 | `logging.basicConfig(filename=...)` | Send every prediction to a file you can read afterwards |
| 35 | `np.percentile(latencies, 95)` | The p95: the time 95% of requests came in under |

### Used ahead of the ladder

The ladder above is the *teaching* schedule: the week a construct is explained and drilled. An audit
(2026-10-03) found these constructs appearing in a student-guide code block **before** that week. Most are
explained where they first appear, as a one-line "what the new line does" rather than a lesson, which is
why the four-a-week cap was not broken; check the rest before teaching that week. Treat the week below as the **first sighting**, the ladder week
as the **lesson**.

| Construct | First sighting | Ladder week |
|---|:--:|:--:|
| `.to_string(` | 1 | 7 |
| `OneHotEncoder` | 3 | 4 |
| `SimpleImputer` | 3 | 6 |
| `.reshape(` | 4 | 16 |
| `get_feature_names_out` | 4 | 5 |
| `coef_` | 5 | 33 |
| `named_steps` | 5 | 6 |
| `np.where(` | 5 | 13 |
| `StratifiedKFold` | 6 | 11 |
| `cross_val_score` | 6 | 11 |
| `recall_score` | 6 | 8 |
| `np.log(` | 13 | 14 |
| `.eval()` | 22 | 23 |
| `.numel(` | 22 | 26 |
| `from_numpy` | 22 | 24 |
| `optim.Adam` | 22 | 26 |
| `perf_counter` | 26 | 34 |
| `.toarray(` | 31 | 32 |
| `np.argsort` | 31 | 33 |

**Deliberately NOT in this level** — so you can say "not yet" with confidence: `torchvision` and any
pretrained-weights download · `nn.BatchNorm2d` · `nn.LSTM` / `nn.GRU` · `nn.Transformer` and attention
· `torch.nn.functional` as a style · custom `autograd.Function` · `GridSearchCV` and
`RandomizedSearchCV` · `Optuna` · GPU code beyond naming `.to(device)` once · `flask` / `fastapi`
(Week 35 uses the standard library on purpose, so nothing installs) · `seaborn` · `plotly` ·
`transformers` · `gensim` · `nltk` / `spacy` (Week 31 tokenizes with `re`, which is more honest) ·
type hints · `async` · decorators · `dataclasses` · `pytest`. Most of those are Level 4. None of them
is needed to do everything in this course.

---

## 🔌 Offline by Design

**Read this before Week 1.** It is the single biggest practical difference between this course and
every deep-learning tutorial on the internet.

> **Every dataset in all 36 weeks either ships inside scikit-learn or is generated by numpy in front
> of the student. Nothing downloads. Ever. Not in Week 1, not in Week 26, not in the capstone.**

This is not a compromise. It is better teaching, for three reasons: a lesson cannot be killed by a
proxy, a firewall or a flaky café connection; the student can *see exactly what went in*, because
they wrote the code that made it; and a 1,797-image dataset that trains a CNN to ~95% in nine seconds
lets you run the experiment four times in one class, which a 50,000-image download does not.

### The datasets, all 36 weeks

| Weeks | Dataset | Where it comes from |
|:--:|---|---|
| 1–7 | 2,020-row pizza-delivery table (`make_data.py`) | **Generated by numpy**, seed 0, in front of the student — including the 6% missing values, the 1% duplicate rows and the poisoned leakage column |
| 8–11 | 1%-positive fraud-shaped table | `sklearn.datasets.make_classification(weights=[0.99, 0.01], random_state=0)` |
| 12 | 10 points, hours studied vs marks | Typed out, then generated with numpy, seed 0 |
| 13–15 | Two-feature classification table | `make_classification(n_features=2, n_informative=2, random_state=0)` |
| 16–18 | Hand-typed 3-input rows, and 3×2 / 2×4 grids | Typed by hand so every number is checkable on paper |
| 19–23 | Two interleaving crescents, then handwritten digits | `make_moons(random_state=0)` · **`load_digits()`** — 1,797 images, 8×8, ships in scikit-learn |
| 24–25 | 6×6 and 8×8 images: bars, edges, crosses, noise | **Written inline with numpy.** You can see exactly what the kernel is sliding over |
| 26–27 | Handwritten digits, plus shifted copies of them | `load_digits()` · augmentation with `np.roll` |
| 28–30 | 6 hand-typed points, then 178 wines | Typed by hand · `load_wine()` · `make_blobs(random_state=0)` |
| 31–33 | 4 reviews on the board, then 80 typed reviews + 12 negation traps | **Typed out by the student.** Their own words, their own labels |
| 34–36 | Whichever artifact they chose to ship | Their own Week 26 digits CNN or their own Week 33 sentiment engine |

Also available offline and used in exercises: `load_iris`, `load_breast_cancer`,
`make_regression`, `load_diabetes`.

### 🚫 What this course never does

- **Never imports `torchvision`.** It is not installed and it is not needed. The image dataset of this
  level is `load_digits()`.
- **Never uses MNIST, FashionMNIST, CIFAR-10, `fetch_openml`, `fetch_20newsgroups`,** or any
  download-on-first-use dataset as the spine of a lesson. Not one exercise, activity or answer depends
  on a download.
- **Never needs a pretrained model.** Week 27 does real transfer learning offline: train the conv
  stack on digits 0–4, freeze it, retrain only the head on 5–9, report both numbers.
- **Never needs a GPU.** Every training run in this course is under about 30 seconds on a laptop CPU,
  and the expected runtime is stated in the text.

> **💡 When you have internet:** the reference module for CNNs uses CIFAR-10 and a pretrained
> `resnet18`, which are excellent and which you may explore any time you are on an unblocked network:
> `pip install torchvision` and then `torchvision.datasets.CIFAR10(root="./data", download=True)`.
> Weeks 24–27 each carry exactly one clearly-marked callout like this one. **It is always optional.
> No exercise, activity or answer key in this course depends on it,** and a student who never once has
> internet finishes the level having missed nothing that is assessed.

### The install: one line, once, in Week 0

```bash
pip install "numpy>=1.26" "pandas>=2.0" "matplotlib>=3.7" "scikit-learn>=1.4" "torch>=2.1"
```

That is the whole stack. Four libraries plus PyTorch. `joblib` arrives automatically as a
scikit-learn dependency, which is why Week 3 can use it without a fifth install. **Nothing else is
ever installed for the rest of the year.** About 2.5 GB, mostly PyTorch, ten minutes on a normal
connection.

### The 3-line smoke test

Put these three lines in `smoke.py` and run it:

```python
import numpy, pandas, matplotlib, sklearn, torch
from sklearn.datasets import load_digits
print("Level 3 ready ·", "numpy", numpy.__version__, "· torch", torch.__version__,
      "· digits", load_digits().images.shape)
```

Real output from the machine this course was written on:

```text
Level 3 ready · numpy 1.26.4 · torch 2.2.1 · digits (1797, 8, 8)
```

Your version numbers will differ and that is fine. **What must match is `(1797, 8, 8)`** — that is
1,797 images, each 8 pixels tall and 8 pixels wide, and it proves that the image dataset of this level
is already sitting on your disk with no download required.

Then two more short checks, both in [orientation §5](teacher-guide/00-orientation.md), which take one
minute between them: **autograd works** (it should print `6.0`) and **a chart can be saved to a file**
(a `.png` should appear). Do all three in Week 0, alone, with nobody watching.

---

## 🧰 Materials for the Whole Year

### The box

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  📦  THE 36-WEEK BOX — sort it once, in week 0                          │
   ├─────────────────────────────────────────────────────────────────────────┤
   │                                                                         │
   │   □  1 laptop YOU ARE ALLOWED TO INSTALL ON               weeks 1–36    │
   │      (macOS, Windows or Linux. ~4 GB free. NO GPU needed.)               │
   │   □  1 notebook, used ONLY for this course                weeks 1–36    │
   │      · front: the Bug Log (one page per error, all year)                │
   │      · middle: THE MATHS BOOK — every hand calculation                  │
   │      · back: results tables, with the seed written next to each         │
   │   □  Pencils + a good eraser                              weeks 1–36    │
   │   □  40 sheets of 5mm GRAPH PAPER                         weeks 10, 12, │
   │      (this is the level where graph paper does real work)  13, 14, 24,  │
   │                                                            28, 29       │
   │   □  1 ruler with millimetres                             weeks 12, 24  │
   │      (used to MEASURE a slope. Not decoration.)                         │
   │   □  1 pack of index cards (~60)                          weeks 2, 8,   │
   │      (the three piles · the four cells · shape dominoes)    17, 21       │
   │   □  1 calculator, or the phone's                         weeks 12–14,  │
   │      (needs e^x and ln. Almost all of them do.)             32          │
   │   □  4 coloured pens or highlighters                      weeks 6, 9,   │
   │      (forward pass in blue, backward pass in red — w17/18)  17, 18      │
   │   □  1 roll of masking tape                               week 28       │
   │      (k-means on the floor, 6 taped points)                             │
   │   □  2 sheets of poster paper (A2+)                       weeks 27, 36  │
   │   □  1 printer, or a willingness to hand-copy             ~14 weeks     │
   │                                                                         │
   │   FROM AROUND THE HOUSE, no purchase needed:                            │
   │   □  A kitchen timer, for the 15-minute struggle rule — all year        │
   │   □  A staircase or a hill you can stand on — week 12                   │
   │      (walk down it and say "which way is down" out loud. It works.)     │
   │   □  Someone willing to be an audience for 10 minutes — weeks 19, 36    │
   │   □  A second terminal window — weeks 3, 23, 35                         │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘
```

### The digital side

| Tool | Weeks | Account? | Cost | Installs? | Internet after install? |
|---|---|:--:|:--:|:--:|:--:|
| **Python 3.11+** (3.10 works) | all | no | free | **yes** | no |
| **numpy** | all | no | free | yes (pip) | no |
| **pandas** | 1–11, 30 | no | free | yes (pip) | no |
| **matplotlib** | all | no | free | yes (pip) | no |
| **scikit-learn** | all | no | free | yes (pip) | no |
| **PyTorch** (`torch`) | 20–36 | no | free | yes (pip) | no |
| **VS Code** (or IDLE, which ships with Python) | all | no | free | yes | no |

> **⚠️ Watch out — read this before Week 1.** Nothing in this level uploads anything anywhere. There
> are no accounts, no API keys, no cloud services and no chatbots in this entire course. The only
> network access needed is `pip install`, once, in Week 0. **Week 35 runs an HTTP server bound to
> `127.0.0.1`** — that is your own machine talking to itself, and the teacher file says so in three
> places, because it is the one moment a parent may reasonably ask.

---

## 🛟 If Something Goes Wrong

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'torch'` — but pip said it installed | You installed into one Python and are running another. Run `python -c "import sys; print(sys.executable)"` — the path **must** contain `.venv`. If not: activate again, and in VS Code re-pick the interpreter. Orientation §5, row 2. |
| `ModuleNotFoundError: No module named 'torchvision'` | **Correct and expected.** Nothing in this course imports it. If a student's file does, they got the line from the internet — Weeks 24–27 explain what to write instead. |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (1797x32 and 16x10)` | The commonest error of the whole year. Two numbers in the message; the second number of the first pair must equal the first number of the second pair. Orientation §4, error 1. |
| `RuntimeError: mat1 and mat2 must have the same dtype, but got Long and Float` | Whole numbers went into a layer that wants decimals. `torch.tensor(a, dtype=torch.float32)` or `.float()`. Orientation §4, error 2. |
| The loss goes 35 → 6906 → 1359681 → `inf` → `nan` | Learning rate too big. Divide it by ten and run again. Orientation §4, error 6. |
| The loss never moves and no error appears | Ninety per cent of the time it is a missing `optimizer.zero_grad()`. Orientation §4, error 3 — and it is the nastiest one, because there is no traceback. |
| The same script gives a different accuracy every run | A seed is missing. `random_state=0` on every split and every model, `torch.manual_seed(0)` at the top. Orientation §4, error 14. **A number you cannot reproduce is not a result.** |
| A score jumped to 0.97 and everybody is delighted | Be suspicious, out loud, in front of the student. Week 6 exists for this. Orientation §4, error 8. |
| `plt.show()` shows nothing | Not a real problem. Every chart in this course also calls `fig.savefig(...)`. Open the PNG. Orientation §4, error 13. |
| A training run is taking minutes, not seconds | Something got bigger than the teacher file says it should be. Check the batch size, the epoch count, and that you are on `load_digits` and not something you downloaded. Every run in this course is under ~30 seconds. |
| The lesson ran out of time | Cut the ✍️ practice, never the 🔢 maths or the 🎲 activity. In this level the hand-arithmetic *is* the lesson; the typing can move to homework. |
| **The student says "I don't get the maths"** | **Do not re-explain it.** Go back to numbers: pick three, do the arithmetic together, ask them what they notice. Orientation §10 is entirely about this sentence and it is the most important page in the file. |
| **You** don't understand the maths | Section 1 of the orientation is a twelve-page maths course for an adult who has never done calculus, worked entirely on real numbers. Then say "I don't know, let's measure it" out loud — that is on the syllabus too. |

---

## ▶️ Start Here

> ### 1. 📕 Teachers, read this first — once, cover to cover, ~2 hours
> ### 👉 **[teacher-guide/00-orientation.md](teacher-guide/00-orientation.md)**
>
> It contains: a twelve-page maths course for an adult who has never done calculus (functions, graphs,
> slope of a line, slope of a *curve* measured numerically, why that is the whole of machine learning,
> grids and shapes, multiplying grids, averaging errors) · a Python-and-PyTorch mini-course · how to
> read a traceback and the **14 errors this level actually produces** · what "engineering" adds on top
> of Level 2 · the offline install guide with a 12-row troubleshooting table · the 20 questions
> students ask · the 15 things adults get wrong teaching this material · the 70-minute lesson shape ·
> **how to help without taking the keyboard** · **what to do when they say "I don't get the maths"** ·
> how to mark code and how to mark a written explanation · and a pre-flight checklist.
>
> Two hours. It is the difference between teaching this course and surviving it.

> ### 2. 🔧 Then do the Week 0 setup, alone, with nobody watching
> ### 👉 **Orientation §5** — and get all three smoke tests passing: imports, autograd, a saved chart

> ### 3. 📗 Then open Week 1 with the student
> ### 👉 **[student-guide/week-01.md](student-guide/week-01.md)**

> ### 4. 📘 And set the first homework
> ### 👉 **[workbook/week-01.md](workbook/week-01.md)**

---

## 🧾 The Promise

Thirty-six weeks from now, someone will show your student a model that scores 0.97 and ask them if it
is any good.

They will not be impressed. They will ask what the baseline was. They will ask which four numbers are
in the confusion matrix and which of the two mistakes costs more. They will ask whether the scaler was
fitted before or after the split, and whether that 0.97 was on rows the model had ever seen. They will
ask for the seed.

And when someone says *"but how does it actually learn?"*, they will not say "gradient descent" and
change the subject. They will pick up a pencil and say:

> *"Here's a curve. Here's the point we're standing on. I nudge the weight by a thousandth and the
> error moves by this much — divide, and that's the slope, six point oh. Positive slope means going
> right makes it worse, so we go left. Do that for every weight at once and that's the gradient. Do it
> a thousand times and that's training. I wrote the loop in week 15 — twenty-five lines, no framework
> — and in week 18 I did all four gradient arrays of a two-layer network by hand and checked them to
> one part in a million. PyTorch does it in one line now, and I know exactly what that line is doing,
> because I did it first. Want to see the loss curve?"*

That sentence is the whole level. It started with a fourteen-year-old being shown that
`model.fit(X, y)` was one line hiding five decisions.

---

[⬅ Level 3 modules](../README.md) · [Teacher Orientation](teacher-guide/00-orientation.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md) · [Figure style guide](figures/STYLE.md) · [Glossary](../glossary.md) · [Level 2 course](../../level-2-builder/36-week-course/README.md)

**The four term papers:** [Assessments home](assessments/README.md) · [Term 1](assessments/term-1-test.md) · [Term 2](assessments/term-2-test.md) · [Term 3](assessments/term-3-test.md) · [Term 4](assessments/term-4-test.md)

**Projects:** [Fifty ideas](projects/project-ideas.md) · [The worked example](projects/worked-example-project.md) · [The Ship It capstone](projects/capstone.md)

**The reference module set this course was built from:** [Modules](../README.md) · [Module capstone](../capstone.md) · [Module assessment](../assessment.md) · [Glossary](../glossary.md)
