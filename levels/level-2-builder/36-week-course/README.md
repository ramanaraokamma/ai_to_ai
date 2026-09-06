```
   █████╗ ██╗    ██████╗  █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗
  ██╔══██╗██║   ██╔════╝ ██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝
  ███████║██║   ██║      ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝
  ██╔══██║██║   ██║      ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝
  ██║  ██║██║   ╚██████╗ ██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║
  ╚═╝  ╚═╝╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │        L E V E L   2   ·   B U I L D E R                          │
  │        ────────────────────────────────────────                  │
  │        T H E   3 6 - W E E K   C O U R S E                        │
  │                                                                  │
  │        One class a week. 60–75 minutes. All of it code.           │
  │        A teacher who knows neither Python nor AI can teach it.    │
  │                                                                  │
  │        print("hello")  ─────►  the overfitting curve              │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

# 🔨 Level 2 Builder — The 36-Week Course

### *One school year. One class a week. From a blank file to three trained models on an honest split — by a Grade 7 student who had never written a line of code in September.*

**Learner:** one 7th grader, age ~12, fresh out of Level 1 · **Teacher:** any adult — **no Python, no AI required**
**Coding:** every single week · **Maths:** fractions, percentages, negative numbers, `y = mx + c`
**Rhythm:** 36 weeks × one 60–75 minute class + ~60 min of workbook homework

[⬅ Back to Level 2 modules](../README.md) · [**Start here: Teacher Orientation**](teacher-guide/00-orientation.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md) · [Figure style guide](figures/STYLE.md)

---

## 🪝 What This Is

The nine Level 2 modules next door are excellent and they are **not a course**. They are a book, and
the book assumes a motivated reader with four free hours, a working install, and nobody waiting on
them. It gets a keen learner from `print("hello")` to an overfitting curve in about twenty weeks.

This folder turns that book into a **school year**. Same code, same honesty, same refusal to say
"magic" — but sliced into 36 sittings, each one small enough to actually happen on a Tuesday evening
when the install is fine, the learner is tired, and nobody has typed a colon correctly all week.

The single design constraint that shaped every page:

> **The teacher opens the week's file 20 minutes before class, and that is all the preparation they
> get. They do not know Python. They must be able to teach a confident, correct 70-minute lesson
> from that one file — including reading, explaining, and debugging code they have never seen.**

That is a harder promise than Level 1's, because now there is code on the screen and code fails in
public. So three things are true of every week in this folder:

1. **Every code block in this course was actually run before it was pasted**, and every output shown
   is the real output. If a number appears in a fenced `text` block, a machine printed it.
2. **Every week teaches one real error on purpose** — a genuine traceback, copied from a genuine
   failed run, explained line by line, then fixed. Errors are curriculum here, not accidents. A
   student who cannot read a traceback cannot program, and neither can their teacher.
3. **Nothing is introduced before the week that introduces it.** The [syntax ladder](#-the-syntax-ladder)
   below is the enforcement mechanism. Max **4 new pieces of syntax** and **5 new words** per week,
   all year. That cap is the most important pacing decision in this level.

### What the student walks out with in June

- A **`stats.py` toolkit they wrote themselves** and still `import` in week 33
- A **30-record dataset** they typed, saved to CSV, and loaded back with the round trip proved row by row
- A **cleaning log** for a deliberately broken 40-row table — every repair numbered, with a reason
- **Five labelled charts** that answer five stated questions, plus one deliberately misleading chart
  next to its honest fix, with the arithmetic of the lie written out
- **Three trained models** — kNN, a decision tree, and a linear regression — compared on **one** split
- **The single most important graph in machine learning**: their own training score climbing while
  their own test score falls off a cliff, with the overfitting point marked and named
- A **Bug Log** of ~40 real error messages they hit, each with the fix in their own words
- And the reflex that matters most: being handed a spreadsheet and a question, and going from file to
  defensible answer without asking anyone what to type next

---

## 👤 Who This Is For

| | |
|---|---|
| **The learner** | One 7th grader, around 12. **Has finished Level 1** and has never written a line of code. Can do fractions, percentages, negative numbers, and is meeting `y = mx + c`. Types slowly and inaccurately — which is fine, and is part of what this year fixes. |
| **The teacher** | You. A parent, a general classroom teacher, a librarian, a volunteer. **You are not expected to know Python. You are not expected to know AI.** Read [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) once — it contains a complete Python mini-course for adults, the 12 errors beginners hit, and a bulletproof install guide — and you are ready for all 36 weeks. |
| **The setting** | A kitchen table, a classroom, a library corner. **One laptop you are allowed to install software on.** That is the entire technical requirement, and it is a real one — sort it in week 0. |
| **Group size** | Written for one learner. Every activity has a "if you have 2–6 students" note in the teacher file. Above 8, pair them at one keyboard each and add 10 minutes to every activity. |

### What Level 1 gave them — and why week 1 should feel like a superpower

Level 1 was not a warm-up. Your student already believes six things that most adults learning Python
have to be argued into, and **week 1 opens by naming all six out loud**:

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │  THEY ALREADY KNOW (by hand)          ─►  THIS YEAR THEY LEARN THE SPELLING │
   ├────────────────────────────────────────────────────────────────────────────┤
   │  a table of rows and columns          ─►  pd.DataFrame(...)         week 21 │
   │  an index card per example            ─►  a dict, then a row        week 13 │
   │  features and a label column          ─►  X and y                   week 28 │
   │  "hide 20% before you train"          ─►  train_test_split(0.2)     week 29 │
   │  accuracy = correct ÷ total           ─►  accuracy_score(y, pred)   week 30 │
   │  a hand-drawn confusion matrix        ─►  confusion_matrix(...)     week 30 │
   │  "it memorized instead of learning"   ─►  the train/test gap        week 33 │
   │  a data card                          ─►  a cleaning log            week 24 │
   │  "which chart is fooling me?"         ─►  a truncated y-axis, fixed week 27 │
   └────────────────────────────────────────────────────────────────────────────┘
```

**Not one idea in that right-hand column is new to them.** They are learning spellings, not concepts.
Say that out loud in week 1 and mean it — it is the difference between a year that feels like a
promotion and a year that feels like starting over.

> **💡 Try this:** In week 1, before you open Python at all, have them tell *you* what a feature is,
> what a label is, and why you hide test data. Write their answers on a sheet and pin it up. In week
> 29 you will take it down and point at it, and they will realise they have been ready for four
> months.

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
   │  · "What YOU need to    │  · The concept, written  │  · Predict-the-output    │
   │    understand first" —  │    for a 12-year-old     │    before you run it     │
   │    including the Python │  · Every code block      │  · The week's build      │
   │    you don't know yet   │    complete and runnable │  · A self-check          │
   │  · Minute-by-minute     │  · The real output in a  │  · Full answer key at    │
   │    lesson script        │    separate block        │    the bottom, sealed    │
   │  · The EXACT code to    │  · 🐞 this week's error, │    behind a "don't look   │
   │    type, and what its   │    read and fixed        │    yet" line — every     │
   │    real output is       │  · Figures               │    answer worked in full │
   │  · 🐞 the planted bug   │  · Vocabulary            │  · Bug Log page          │
   │    and how to stage it  │  · Key takeaways         │                          │
   │  · What students get    │  · What to do if stuck   │                          │
   │    wrong, and the fix   │                          │                          │
   │  · Answers to every     │                          │                          │
   │    question they'll ask │                          │                          │
   │  · Marking guidance     │                          │                          │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  WHEN                   │                          │                          │
   │  20 min before class    │  In class + re-read      │  Between classes,        │
   │                         │  during homework         │  ~60 min                 │
   └─────────────────────────┴──────────────────────────┴──────────────────────────┘
```

**The rules:**

1. **The student never opens the teacher guide.** It contains the answers, the planted bug, and the
   "what they'll get wrong" notes. Reading it spoils the discovery the lesson is built around.
2. **The teacher does not skip the teacher guide**, even on weeks that look easy. The first section
   of every teacher file is *"What you need to understand before you teach this"*, and in this level
   that section teaches **you** the Python before it asks you to teach it. That is where your
   confidence comes from. It is also where the real output of every code block lives, so you can
   tell instantly whether the thing on your student's screen is right.
3. **The workbook answer key is at the bottom of the workbook**, not hidden in another file. The
   student is trusted with it and told, in writing, to struggle for fifteen minutes first. Fifteen
   minutes of struggle is the lesson; the answer is just the receipt.
4. **Nobody pastes code.** Not the student, not you. Fingers have to learn where the colons and
   brackets go. This costs about 15 extra minutes a week and is the highest-return 15 minutes in
   the level.

---

## 🗓️ The Four Terms

Nine weeks each. Each term answers one question, and the student should be able to answer it out loud
at the end — while showing you a file that runs.

```
   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 1  ·  WEEKS 1–9  ·  SAY IT IN PYTHON                                ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  How do you give a computer an instruction it cannot        ║
   ║                 misunderstand — and read what it says back when you       ║
   ║                 get it wrong?                                             ║
   ║                                                                           ║
   ║  Ends with: a working About-Me Bot, a number-guessing game that survives   ║
   ║  bad input, a Bug Log with a dozen real tracebacks in it, and the first    ║
   ║  function the student ever wrote — invented because they were sick of      ║
   ║  retyping the same five lines.                                            ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 2  ·  WEEKS 10–18  ·  BUILD YOUR OWN TOOLBOX                        ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  How do you package your own tools, and hold a whole        ║
   ║                 dataset inside your program?                              ║
   ║                                                                           ║
   ║  Ends with: 🧰 stats.py — their own imported library — plus a 30-record    ║
   ║  dataset saved to CSV and read back, and the first array that does maths   ║
   ║  to fifty numbers in one line.                                            ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 3  ·  WEEKS 19–27  ·  REAL TABLES, HONEST PICTURES                  ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  How do you load a real, messy table, clean it honestly,    ║
   ║                 and draw a picture that does not lie?                     ║
   ║                                                                           ║
   ║  Ends with: 🔍 a deliberately broken 40-row table repaired with a          ║
   ║  numbered cleaning log, and five labelled charts — one of which is a       ║
   ║  lie the student built on purpose and then confessed to in writing.        ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 4  ·  WEEKS 28–36  ·  THREE LINES THAT PREDICT                      ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  Can you train a model, prove the score is honest, and      ║
   ║                 catch it memorising instead of learning?                  ║
   ║                                                                           ║
   ║  Ends with: 🏆 three models on one honest split, an accuracy-vs-k plot,    ║
   ║  a tree whose rules the student reads out loud in English, and the         ║
   ║  overfitting curve — then the Data Detective capstone and showcase.        ║
   ║  This is the term the whole level was built to earn.                      ║
   ╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 All 36 Weeks

**Type key:** 🟦 teach · 🟩 lab · 🟨 project · 🟪 review · 🟥 assessment · 🎪 capstone

| Week | Term | Title | Big idea | New syntax | Type | Homework |
|:--:|:--:|---|---|---|:--:|---|
| 1 | 1 | Make the Computer Say Something | A program is a list of instructions in a file, run top to bottom, and the computer does exactly what you typed — including the part you didn't mean. | `print("...")` · `#` comment · `+ - * /` · `print(a, b, c)` | 🟦 teach | Type and run three files by hand (no pasting); start the Bug Log with your first three error messages |
| 2 | 1 | Boxes With Names On: Variables and Types | A variable is a named box holding one value, and the value's type decides what `+` even means. | `name = value` · `type(x)` · `int("12")` · `float("3.5")` | 🟦 teach | Nine naming-and-type exercises, plus the `"5" + 5` investigation written up in your own words |
| 3 | 1 | Printing Like a Pro: f-strings and Real Maths | An f-string drops a value straight into a sentence, and `:.2f` decides how many decimals a reader gets to see. | `f"..."` · `f"{x:.2f}"` · `//` and `%` · `**` | 🟩 lab | Build `receipt.py`: a pizza bill with per-slice cost printed to exactly 2 decimal places, every line commented |
| 4 | 1 | The About-Me Bot | `input()` always hands you text, so you must convert it yourself — and Python tells you exactly where you forgot. | `input("...")` · `int(input(...))` · `str(x)` · `round(x, 2)` | 🟨 project | Finish the About-Me Bot: 6 questions, 2 derived numbers, a formatted card, every line commented, 3 real tracebacks pasted into the Bug Log |
| 5 | 1 | Questions With Yes/No Answers | A comparison is a question whose answer is `True` or `False`; `if` runs a block only when the answer is `True`. | `==` `!=` · `<` `>` `<=` `>=` · `if ...:` · `else:` | 🟦 teach | Predict eight booleans before running them, then build `ticket_price.py` version 1 and test it on 5 ages |
| 6 | 1 | More Than Two Doors: elif, and, or, not | An `if/elif/else` chain checks in order and stops at the first `True` — which is exactly how a correct-looking chain hides a wrong answer. | `elif ...:` · `and` · `or` · `not` | 🟦 teach | Find why a grade chain gives everyone an A, reorder it, and prove the fix with a 5-value test table |
| 7 | 1 | Doing It 100 Times Without Typing It 100 Times | A `for` loop repeats a block once per item, and an accumulator variable carries a running total across the repeats. | `for i in range(n):` · `range(start, stop, step)` · `+=` · `"=" * 20` | 🟩 lab | Print a times-table grid with `range`, then total and average 12 scores with an accumulator — and hand-check the average |
| 8 | 1 | Guess & Grade | A `while` loop repeats until its condition goes False, which is how a program waits for a human to get it right. | `while ...:` · `break` · `continue` · `random.randint(a, b)` | 🟨 project | Finish `guess.py` (hints, 7-attempt limit, replay) and `grade.py` (total, average, highest, letter); both must survive `"banana"` as input |
| 9 | 1 | Term 1 Checkpoint — You Keep Typing the Same Five Lines | When the same block appears three times, give it a name. A function is a named block you can run whenever you want. | `def name():` · `name()` · `return value` | 🟪 review | Term 1 reflection sheet; find three repeated blocks in your weeks 1–8 files and turn each into a function that gives the same output |
| 10 | 2 | Functions That Take Something and Give Something Back | A parameter is a box the function fills from whoever called it, and `return` is the only way a value gets back out. | `def f(a, b):` parameters · `def f(a, b=0):` default · `f(b=3)` keyword arg · `None` | 🟦 teach | Write five tiny functions from a spec sheet, then find the missing-`return` bug that makes a function print the right answer and hand back `None` |
| 11 | 2 | Many Values, One Name: Lists | A list is a row of numbered slots — and the first slot is number 0, not 1. | `[1, 2, 3]` · `scores[0]` / `scores[-1]` · `len(scores)` · `scores.append(x)` | 🟦 teach | Twelve list-surgery drills, then cause an `IndexError` on purpose, paste the traceback, and write the one-line fix |
| 12 | 2 | Your Own Stats Toolkit | Once your functions live in their own file you can `import` them into any program you write, forever. | `scores[1:4]` slicing · `sorted(scores)` · `for score in scores:` · `import stats` / `from stats import mean` | 🟩 lab | Finish `stats.py` + `main.py` on 20 cricket scores; prove `median()` is right for an odd-length AND an even-length list |
| 13 | 2 | Labels Instead of Numbers: Dictionaries | A dictionary looks things up by name instead of by position, which is what you want the moment a thing has fields. | `{"key": value}` · `d["key"]` · `d["new"] = v` · `d.get("k", 0)` | 🟦 teach | Build five player dictionaries with the same five keys, then cause a `KeyError`, read it, and fix it two different ways |
| 14 | 2 | One Dict Per Row: Your First Dataset in Code | A list of dictionaries **is** a table: one dict is a row, and the keys are the column names. | `d.items()` · `"key" in d` · `[r["x"] for r in rows]` · `enumerate(rows)` | 🟦 teach | Type a 12-record dataset with 5 keys and print it as an aligned table with a numbered header row |
| 15 | 2 | Filter It, Group It, Count It | Filtering keeps the rows that pass a test; grouping counts how many rows share a value. | `[r for r in rows if ...]` · `sorted(rows, key=...)` · `sum(numbers)` · `max(d, key=d.get)` | 🟩 lab | Write `filter_by()` and `group_count()`, run them on your 12 records, and answer six questions — each answer with its row count |
| 16 | 2 | The Record Store: Save It and Load It Back | A CSV is your dataset written out as plain text — and everything read back from one is a string until you convert it. | `import csv` · `with open(p, "w", newline="") as f:` · `csv.DictWriter` · `csv.DictReader` | 🟨 project | Finish the Record Store: 30 records, 5 keys, written to CSV and loaded back, with the round trip proved field by field on row 1 |
| 17 | 2 | One Number for Every Score: NumPy Arrays | An array is a list that knows its shape and does maths to all of its numbers at once. | `import numpy as np` (aliasing) · `np.array([...])` · `.shape` · `.dtype` | 🟦 teach | Predict the shape and dtype of six arrays *before* running anything, then check all six and explain every miss |
| 18 | 2 | Term 2 Checkpoint — Eight Loops You Never Have to Write Again | Array maths replaces a whole `for` loop with one line, and the one line is easier to read *and* harder to get wrong. | `arr * 2` elementwise · `arr1 + arr2` · `np.arange(n)` · `np.zeros((r, c))` | 🟪 review | Term 2 reflection sheet; rewrite eight loops from weeks 7–15 as array one-liners and prove each output is byte-identical |
| 19 | 3 | Down the Columns or Across the Rows? | `axis=0` walks down a column, `axis=1` walks across a row — and picking the wrong one gives you a confident wrong answer. | `arr[1, 2]` · `arr[:, 0]` · `arr.mean(axis=0)` · `arr.sum(axis=1)` | 🟦 teach | The rainfall grid: per-city and per-month means, with row 1 hand-checked on paper before you trust the code |
| 20 | 3 | The Vectorized Gradebook | A boolean mask is a yes/no array you use to pull out only the values you care about. | `arr > 50` · `arr[mask]` · `arr.min()` / `arr.max()` · `np.round(arr, 2)` | 🟩 lab | Finish the Vectorized Gradebook — zero `for` loops anywhere — plus 0-to-1 normalization done by hand for one row and matched to the code |
| 21 | 3 | Tables With Names On: Meet the DataFrame | A DataFrame is a table where the columns have names and the rows have an index, so you never again have to remember "column 3". | `pd.DataFrame({...})` · `df.head()` · `df.info()` · `df["col"]` | 🟦 teach | Build a 10-row DataFrame about your own week, then write out what every line of `df.info()` is telling you |
| 22 | 3 | Picking Rows and Columns Without Guessing | `loc` picks by name, `iloc` picks by position, and a boolean filter picks by asking a question. | `df.loc[row, col]` · `df.iloc[i, j]` · `df[df["age"] > 12]` · `df.sort_values("col")` | 🟦 teach | Ten selection drills, then the `loc`/`iloc` trap: the same call on a custom index returns two different rows — explain why |
| 23 | 3 | Holes, Text-That-Should-Be-Numbers, and Duplicates | Real data arrives broken in four predictable ways, and each one has a named fix that you must write down. | `pd.read_csv()` / `df.to_csv()` · `df.isna().sum()` · `df["c"].fillna(v)` · `df["c"].astype(int)` | 🟦 teach | Repair a 12-row broken table and produce a numbered cleaning log: one line per repair, each with a *reason*, not just a *what* |
| 24 | 3 | Mess Detective | `groupby` answers "what's the average per house?" in one line — and hides how many rows each answer came from. | `df.drop_duplicates()` · `df["c"].str.strip().str.title()` · `df["new"] = ...` · `df.groupby("c")["v"].mean()` | 🟩 lab | Finish Mess Detective on the broken 40-row table: before/after shape, full cleaning log, six `groupby` answers each reported **with its row count** |
| 25 | 3 | Drawing the Table: Your First Chart | A chart with no axis labels is a decoration. The labels are what turn it into evidence. | `fig, ax = plt.subplots(figsize=(6,4))` · `ax.plot(x, y, marker="o")` · `ax.set_title()` / `set_xlabel()` / `set_ylabel()` · `fig.savefig(...)` | 🟦 teach | Three fully labelled line charts from your week-21 DataFrame, saved as PNGs, each with a one-sentence caption saying what it shows |
| 26 | 3 | Five Questions, Five Chart Shapes | The question decides the chart: comparison → bar, spread → histogram, relationship → scatter. | `ax.bar()` · `ax.hist(values, bins=n)` · `ax.scatter(x, y)` · `df["c"].value_counts()` | 🟦 teach | Match eight questions to chart shapes, build four of them, and write one sentence per chart naming what it *hides* |
| 27 | 3 | Term 3 Checkpoint — Build a Lie, Then Confess | You can make a 2% difference look enormous without changing a single number — just by starting the y-axis somewhere else. | `ax.legend()` · `ax.set_ylim(bottom, top)` · `plt.subplots(1, 2)` · `df["a"].corr(df["b"])` | 🟪 review | Term 3 reflection sheet; the Five-Chart Data Story in narrative order, plus the lie-and-fix pair side by side with the arithmetic of the exaggeration |
| 28 | 4 | X and y: Turning Your Table Into a Question | Every model needs the table split into `X` (what you measured) and `y` (what you want back) — Level 1's features and label, finally spelled out in code. | `from sklearn.datasets import load_iris` · `X = df[["a","b"]]` double brackets · `np.sqrt(x)` · `((a - b) ** 2).sum()` | 🟦 teach | Build `X` and `y` from your own table with the right shapes stated; compute one distance by hand on paper, then in numpy, and match to 2 dp |
| 29 | 4 | Nearest Neighbours, and the 20% You Must Hide | kNN guesses by letting the k closest examples vote — and the score only means anything on rows the model never saw. | `KNeighborsClassifier(n_neighbors=k)` · `model.fit(X_train, y_train)` · `model.predict(X_test)` · `train_test_split(X, y, test_size=0.2, random_state=42)` | 🟦 teach | Run the full cycle on iris; report the score on the training rows AND the held-back rows, and explain the gap in two sentences |
| 30 | 4 | Classifier Lab: Scaling, k, and the Confusion Matrix | If one feature is measured in thousands it drowns out the others — so you scale, and you fit the scaler on the training rows only. | `accuracy_score(y_test, pred)` · `confusion_matrix(y_test, pred)` · `StandardScaler().fit(X_train)` + `.transform()` · `stratify=y` | 🟩 lab | Finish Classifier Lab: accuracy-vs-k plot for k = 1…25, a scaled/unscaled comparison table, and your chosen `k` with a written reason |
| 31 | 4 | Trees You Can Read Out Loud | A decision tree is a stack of yes/no questions, and you can print the exact rules it learned. | `DecisionTreeClassifier(max_depth=3)` · `export_text(tree, feature_names=...)` · `tree.feature_importances_` · `plot_tree(...)` | 🟦 teach | Train a depth-3 tree, write its rules out as English sentences, then find one row it gets wrong and say which rule caught it |
| 32 | 4 | Predicting a Number: Lines, MAE, and R² | When the answer is a number instead of a category you fit a line — and you measure the error in the units of the thing itself. | `LinearRegression()` · `model.coef_` / `model.intercept_` · `mean_absolute_error(...)` · `r2_score(...)` | 🟦 teach | Fit a line by hand through six points, then with sklearn; state the slope in real units ("+3.4 marks per extra hour") and say what MAE means in marks |
| 33 | 4 | Model Bake-Off and the Overfitting Cliff | A training score that climbs while the test score falls is memorising, not learning — and it has a picture. | `DecisionTreeRegressor(max_depth=d)` · `mean_squared_error(...)` + `np.sqrt` for RMSE · `ax.axvline(x, linestyle="--")` · `load_diabetes()` | 🟩 lab | Finish Model Bake-Off: three models on **one** split, a results table, and the depth curve with the overfitting point marked and named |
| 34 | 4 | Data Detective, Part 1: Your Question and Your 100 Rows | A data project starts with a question you could be wrong about, and 100 rows you collected yourself. | `df.describe()` | 🎪 capstone | Capstone milestones 1–3: question locked in writing, 100+ rows collected, the raw file saved untouched, and a numbered cleaning log |
| 35 | 4 | Data Detective, Part 2: Charts, Models, and What I Got Wrong | The most valuable page in any data project is the one titled "what I got wrong". | *(no new syntax — that is the point)* | 🎪 capstone | Capstone milestones 4–6: five captioned charts in narrative order, three models on one split, the results table, and the "what I got wrong" section |
| 36 | 4 | Showcase Day: Read Your Notebook Out Loud | You can take a question, a messy table and a keyboard, and produce an answer you are willing to defend. | *(none)* | 🟥 assessment | No new homework — complete the Level 3 gate self-check and write a letter to yourself about what you want to build next |

---

## 📆 Year at a Glance

```
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 1 · SAY IT IN PYTHON              "Instructions it can't mistake?"    │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │  W1  │  W2  │  W3  │  W4  │  W5  │  W6  │  W7  │  W8  │  W9  │             │
   │ 🟦   │ 🟦   │ 🟩   │ 🟨   │ 🟦   │ 🟦   │ 🟩   │ 🟨   │ 🟪   │             │
   │print │ vars │  f-  │ABOUT │ if / │ elif │ for  │GUESS │ ✦CHK │             │
   │  ()  │types │string│ -ME  │ else │and/or│range │  &   │POINT │             │
   │      │      │  //% │ BOT  │      │ not  │  +=  │GRADE │ def  │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │  ───────── module 1 ─────────   ───────── module 2 ─────────  ─ m3 starts ─ │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 2 · BUILD YOUR OWN TOOLBOX          "Your own tools, your own data?"   │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W10  │ W11  │ W12  │ W13  │ W14  │ W15  │ W16  │ W17  │ W18  │             │
   │ 🟦   │ 🟦   │ 🟩🧰 │ 🟦   │ 🟦   │ 🟩   │ 🟨   │ 🟦   │ 🟪   │             │
   │param │lists │STATS │dicts │list- │filt- │RECORD│numpy │ ✦CHK │             │
   │return│ [0]  │TOOL- │ {}   │  of- │ er / │STORE │array │POINT │             │
   │      │ len  │ KIT  │ .get │dicts │group │ CSV  │shape │ vec  │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │ ────── module 3 ──────   ────────── module 4 ──────────  ── module 5 ────   │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 3 · REAL TABLES, HONEST PICTURES     "Clean it — and don't lie?"       │
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W19  │ W20  │ W21  │ W22  │ W23  │ W24  │ W25  │ W26  │ W27  │             │
   │ 🟦   │ 🟩   │ 🟦   │ 🟦   │ 🟦🔑 │ 🟩🔍 │ 🟦   │ 🟦   │ 🟪   │             │
   │axis 0│GRADE-│Data- │ loc  │ isna │ MESS │first │ bar  │ ✦CHK │             │
   │  / 1 │ BOOK │Frame │ iloc │fillna│DETEC-│chart │ hist │POINT │             │
   │      │masks │ info │filter│astype│ TIVE │labels│scatt │ LIE  │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │ ── module 5 ──   ─────────── module 6 ───────────   ─── module 7 ───        │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │  TERM 4 · THREE LINES THAT PREDICT        "Train it — and catch it cheating?"│
   ├──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┤
   │ W28  │ W29  │ W30  │ W31  │ W32  │ W33  │ W34  │ W35  │ W36  │             │
   │ 🟦   │ 🟦⚡ │ 🟩   │ 🟦   │ 🟦   │ 🟩🔑 │ 🎪   │ 🎪   │ 🟥🎓 │             │
   │ X, y │ kNN  │CLASS-│ tree │ line │ BAKE │detec-│detec-│SHOW- │             │
   │ dist-│ fit  │IFIER │rules │ MAE  │ -OFF │ tive │ tive │ CASE │             │
   │ ance │split │ LAB  │depth │  R²  │curve │ p1   │ p2   │      │             │
   ├──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┤
   │ ────── module 8 ──────   ────── module 9 ──────  ── CAPSTONE ──  ─ FINAL ─  │
   └─────────────────────────────────────────────────────────────────────────────┘

   LEGEND
   🟦 teach — new syntax, worked example, everyone types
   🟩 lab   — hands-on build, end to end, it runs by the end of class
   🟨 proj  — a program gets finished and handed in
   🟪 review— term checkpoint: debug drills + consolidation + one new idea
   🟥 test  — the final assessment
   🎪 capstone
   ⚡ the week the first real model is trained
   🔑 the two most important lessons in the level (w23 cleaning honestly, w33 overfitting)
   🧰 the week the student's own library is born
   🔍 the week a broken table gets repaired with a written log
   ✦  term checkpoint week
```

> **⚠️ Watch out:** Do not teach Week 29 and Week 33 in the same fortnight if you can help it.
> Week 29 ends with the student proud of a model that scored well. Week 33 exists to show that the
> score can be a lie about a memoriser. That gap needs a couple of weeks of pride sitting in between,
> or the lesson does not bite. This is the same structural warning Level 1 gives about weeks 17 and
> 19–22, and it exists for the same reason.

---

## 🪜 The Syntax Ladder

**This is the spine of the course.** Every Python construct in Level 2, in the week it first appears.
Nothing is ever used before the week it appears here.

Use it two ways:
- **"Have we met dictionaries yet?"** → search the table, read the week number. Five seconds.
- **A student uses something you don't recognise** → find it here. If its week is *after* this week,
  they got it from the internet, and the honest move is: "Nice — where did you find that? We meet it
  properly in week 13. Can you explain it to me?"

| Week | New construct | What it does in one line |
|:--:|---|---|
| 1 | `print("text")` | Puts text on the screen |
| 1 | `# a comment` | A note for humans; Python ignores it |
| 1 | `+ - * /` | Add, subtract, multiply, divide. `/` always gives a decimal |
| 1 | `print(a, b, c)` | Prints several things on one line, separated by spaces |
| 2 | `name = value` | Puts a value in a named box. The name goes on the left, always |
| 2 | `type(x)` | Tells you what kind of value `x` is |
| 2 | `int("12")` | Turns text that looks like a whole number into a whole number |
| 2 | `float("3.5")` | Turns text that looks like a decimal into a decimal |
| 3 | `f"Hi {name}"` | A string with values dropped into it |
| 3 | `f"{x:.2f}"` | The same, rounded to 2 decimal places for display |
| 3 | `//` and `%` | Whole-number divide, and the remainder left over |
| 3 | `**` | Raise to a power. `2 ** 3` is 8 |
| 4 | `input("prompt")` | Asks the human a question. **Always hands back text** |
| 4 | `int(input("Age? "))` | Ask, then convert straight away — the safe habit |
| 4 | `str(x)` | Turns a number into text so you can glue it onto a string |
| 4 | `round(x, 2)` | Rounds a number to 2 decimal places (a real number, not just display) |
| 5 | `==` and `!=` | Is it equal? Is it not equal? Two equals signs, not one |
| 5 | `<` `>` `<=` `>=` | Less than, greater than, and the "or equal to" versions |
| 5 | `if condition:` | Run the indented block only if the condition is `True` |
| 5 | `else:` | Run this block instead, when the `if` was `False` |
| 6 | `elif condition:` | Another question, asked only if all the ones above were `False` |
| 6 | `and` | `True` only when both sides are `True` |
| 6 | `or` | `True` when either side is `True` |
| 6 | `not` | Flips `True` to `False` and back |
| 7 | `for i in range(n):` | Repeat the block `n` times, with `i` counting 0, 1, 2 … |
| 7 | `range(start, stop, step)` | The same counting, but you choose where it starts, stops and how it steps |
| 7 | `total += x` | Short for `total = total + x`. The accumulator move |
| 7 | `"=" * 20` | Twenty equals signs. Multiplying a string repeats it |
| 8 | `while condition:` | Keep repeating for as long as the condition stays `True` |
| 8 | `break` | Leave the loop right now |
| 8 | `continue` | Skip the rest of this trip round the loop and start the next one |
| 8 | `random.randint(a, b)` | A random whole number from `a` to `b`, both included |
| 9 | `def name():` | Give a block of code a name |
| 9 | `name()` | Run the block that has that name |
| 9 | `return value` | Hand a value back out of the function to whoever called it |
| 10 | `def f(a, b):` | Parameters — boxes the caller fills in |
| 10 | `def f(a, b=0):` | A default value, used when the caller doesn't supply one |
| 10 | `f(b=3)` | A keyword argument — name the parameter you're filling |
| 10 | `None` | Python's word for "no value". What a function with no `return` gives back |
| 11 | `[1, 2, 3]` | A list — many values under one name |
| 11 | `scores[0]` / `scores[-1]` | The first slot / the last slot. Counting starts at 0 |
| 11 | `len(scores)` | How many items are in it |
| 11 | `scores.append(x)` | Add `x` to the end |
| 12 | `scores[1:4]` | A slice: slots 1, 2 and 3. The stop number is not included |
| 12 | `sorted(scores)` | A **new** sorted list. Leaves the original alone |
| 12 | `for score in scores:` | Walk through the items themselves, not the numbers 0, 1, 2 |
| 12 | `import stats` / `from stats import mean` | Use functions you wrote in another file |
| 13 | `{"name": "Asha"}` | A dictionary — values looked up by name, not position |
| 13 | `player["name"]` | Get the value stored under that key. `KeyError` if it isn't there |
| 13 | `player["team"] = "Blue"` | Add or overwrite a key |
| 13 | `player.get("overs", 0)` | Get it if it's there, otherwise use this fallback instead of crashing |
| 14 | `player.items()` | Every key and its value, as pairs you can loop over |
| 14 | `"age" in player` | Is there a key called `age`? `True` or `False` |
| 14 | `[r["score"] for r in rows]` | A list comprehension — build a new list in one line |
| 14 | `enumerate(rows)` | Loop and get the position number at the same time |
| 15 | `[r for r in rows if r["age"] > 12]` | A comprehension with a filter — keep only the rows that pass |
| 15 | `sorted(rows, key=...)` | Sort a list of records by one field |
| 15 | `sum(numbers)` | Add a whole list up. You wrote this by hand in week 7 |
| 15 | `max(counts, key=counts.get)` | The key with the biggest value |
| 16 | `import csv` | The standard-library tool for CSV files |
| 16 | `with open(path, "w", newline="") as f:` | Open a file, and close it automatically when the block ends |
| 16 | `csv.DictWriter(f, fieldnames=...)` | Write a list of dictionaries out as a CSV |
| 16 | `csv.DictReader(f)` | Read a CSV back as dictionaries. **Everything comes back as text** |
| 17 | `import numpy as np` | Import a library under a short nickname |
| 17 | `np.array([1, 2, 3])` | An array — a list that knows its shape and does maths all at once |
| 17 | `arr.shape` | `(rows, columns)`. The most-checked thing in this level |
| 17 | `arr.dtype` | What kind of number is inside — `int64`, `float64` |
| 18 | `arr * 2` | Doubles **every** number. No loop |
| 18 | `arr1 + arr2` | Adds them slot by slot. Shapes must fit |
| 18 | `np.arange(5)` | `[0 1 2 3 4]` as an array |
| 18 | `np.zeros((2, 3))` | A 2-row, 3-column array of zeros, to fill in later |
| 19 | `arr[1, 2]` | Row 1, column 2. One pair of brackets, one comma |
| 19 | `arr[:, 0]` | Every row, column 0 — the whole first column |
| 19 | `arr.mean(axis=0)` | One mean **per column** (walks down) |
| 19 | `arr.sum(axis=1)` | One total **per row** (walks across) |
| 20 | `arr > 50` | An array of `True`/`False` — a mask |
| 20 | `arr[mask]` | Only the values where the mask was `True` |
| 20 | `arr.min()` / `arr.max()` | Smallest and largest |
| 20 | `np.round(arr, 2)` | Round every number in the array |
| 21 | `pd.DataFrame({...})` | A table with named columns and a numbered index |
| 21 | `df.head()` | The first five rows, to check it loaded right |
| 21 | `df.info()` | Row count, column names, dtypes, and how many values are missing |
| 21 | `df["steps"]` | One column, as a Series |
| 22 | `df.loc[1, "age"]` | Pick by **name** (index label and column name) |
| 22 | `df.iloc[1, 2]` | Pick by **position**. Counts from 0 |
| 22 | `df[df["age"] > 12]` | Only the rows where the question is `True` |
| 22 | `df.sort_values("steps")` | A new frame, sorted by that column |
| 23 | `pd.read_csv(path)` / `df.to_csv(path, index=False)` | Load a CSV into a frame; write a frame back out |
| 23 | `df.isna().sum()` | How many values are missing, per column |
| 23 | `df["age"].fillna(12)` | Fill the holes. **Write down what you filled and why** |
| 23 | `df["age"].astype(int)` | Force a column to be whole numbers |
| 24 | `df.drop_duplicates()` | Remove repeated rows |
| 24 | `df["house"].str.strip().str.title()` | Tidy text: trim spaces, fix capitals. Four spellings become one |
| 24 | `df["rate"] = df["runs"] / df["balls"]` | A derived column, computed from the ones you have |
| 24 | `df.groupby("house")["runs"].mean()` | One number per group. **Always report the group sizes too** |
| 25 | `fig, ax = plt.subplots(figsize=(6, 4))` | Make one figure with one drawing box |
| 25 | `ax.plot(x, y, marker="o")` | A line chart with a dot on every real data point |
| 25 | `ax.set_title()` / `set_xlabel()` / `set_ylabel()` | The three labels that make a chart evidence |
| 25 | `fig.savefig("f.png", dpi=120, bbox_inches="tight")` | Save it. Always save it — windows don't work everywhere |
| 26 | `ax.bar(names, values)` | Bar chart — comparing separate things |
| 26 | `ax.hist(values, bins=8)` | Histogram — the shape of one column's spread |
| 26 | `ax.scatter(x, y)` | Scatter — is there a relationship between two numbers? |
| 26 | `df["house"].value_counts()` | How many rows per value. The bar chart's raw material |
| 27 | `ax.legend()` | Names the series. Required the moment there are two |
| 27 | `ax.set_ylim(0, 100)` | Set the y-axis by hand. The honest use, and the dishonest one |
| 27 | `fig, axes = plt.subplots(1, 2)` | Two charts side by side, so the lie sits next to the fix |
| 27 | `df["hours"].corr(df["score"])` | The correlation `r`. **Not** a cause |
| 28 | `from sklearn.datasets import load_iris` | A real dataset that ships with the library |
| 28 | `X = df[["length", "width"]]` | Two brackets = a table of features. One bracket = one column |
| 28 | `np.sqrt(x)` | Square root |
| 28 | `((row_a - row_b) ** 2).sum()` | The inside of the distance formula, in one line |
| 29 | `KNeighborsClassifier(n_neighbors=3)` | Make an untrained kNN model that asks the 3 nearest |
| 29 | `model.fit(X_train, y_train)` | Train it. This is the whole of "learning" |
| 29 | `model.predict(X_test)` | Get a guess for every row it never saw |
| 29 | `train_test_split(X, y, test_size=0.2, random_state=42)` | Cut the deck. Hide 20% before you train |
| 30 | `accuracy_score(y_test, pred)` | Correct ÷ total. Level 1's number, computed for you |
| 30 | `confusion_matrix(y_test, pred)` | Which class got mistaken for which. Level 1's grid, printed |
| 30 | `StandardScaler().fit(X_train)` then `.transform(X_test)` | Put features on the same scale. **Fit on train only** |
| 30 | `stratify=y` | Keep the same class mix in both halves of the split |
| 31 | `DecisionTreeClassifier(max_depth=3)` | A stack of yes/no questions, at most 3 deep |
| 31 | `export_text(tree, feature_names=[...])` | Print the actual rules it learned, as text |
| 31 | `tree.feature_importances_` | How much each feature was actually used |
| 31 | `plot_tree(tree, ...)` | Draw the tree |
| 32 | `LinearRegression()` | Fit the straight line of best fit |
| 32 | `model.coef_` / `model.intercept_` | The slope(s) and the intercept — `m` and `c` |
| 32 | `mean_absolute_error(y_test, pred)` | Average miss, in the units of the thing itself |
| 32 | `r2_score(y_test, pred)` | How much of the variation the line explains. 1.0 is perfect |
| 33 | `DecisionTreeRegressor(max_depth=d)` | A tree that predicts a number instead of a category |
| 33 | `np.sqrt(mean_squared_error(y, pred))` | RMSE — like MAE but punishes big misses harder |
| 33 | `ax.axvline(x, linestyle="--")` | A vertical line. Used to mark where overfitting starts |
| 33 | `load_diabetes()` | A built-in dataset with a number to predict |
| 34 | `df.describe()` | Count, mean, min, quartiles, max for every numeric column |

**Deliberately NOT in this level** — so you can say "not yet" with confidence: classes and `self`,
`try`/`except`, `lambda`, `while True` with `else`, generators, `*args`, f-string `=`, `zip`, sets,
tuples-as-a-topic, `pathlib`, decorators, `pipeline`, cross-validation, seaborn, plotly, and anything
from PyTorch. Several of those are Level 3. None of them are needed to do everything in this course.

---

## 🧰 Materials for the Whole Year

### The box

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  📦  THE 36-WEEK BOX — buy once, in week 0                              │
   ├─────────────────────────────────────────────────────────────────────────┤
   │                                                                         │
   │   □  1 laptop or desktop YOU ARE ALLOWED TO INSTALL ON    weeks 1–36    │
   │      (macOS, Windows or Linux — all three work. ~4 GB free.)            │
   │   □  1 notebook, used ONLY for this course                weeks 1–36    │
   │      · front section: the Bug Log (one page per error, all year)        │
   │      · back section: hand-checked arithmetic                            │
   │   □  Pencils + a good eraser                              weeks 1–36    │
   │   □  1 pack of index cards (~40)                          weeks 11, 13, │
   │      (lists as slots, dicts as cards, the deck cut)             28, 29  │
   │   □  20 sheets of graph paper (5mm)                       weeks 19, 25, │
   │                                                              26, 32, 33 │
   │   □  4 coloured pens or highlighters                      weeks 9, 23,  │
   │      (marking up tracebacks and cleaning logs)                 27, 33   │
   │   □  1 ruler with millimetres                             weeks 32, 33  │
   │   □  1 pad of sticky notes                                weeks 2, 11,  │
   │      (variable-name tags stuck on real objects)                 19, 22  │
   │   □  2 sheets of poster paper (A2+)                       weeks 34–36   │
   │   □  1 printer, or a willingness to hand-copy             ~10 weeks     │
   │   □  A phone or camera to photograph a screen             weeks 4, 30   │
   │                                                                         │
   │   FROM AROUND THE HOUSE, no purchase needed:                            │
   │   □  A deck of playing cards — the train/test split, weeks 29, 30       │
   │   □  A kitchen timer, for the 15-minute struggle rule — all year        │
   │   □  Someone willing to be an audience for 10 minutes — weeks 12, 36    │
   │   □  Data about your own life to collect — weeks 21, 34                 │
   │      (steps, screen time, bedtimes, pocket money, bus times)            │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘
```

### The digital side

| Tool | Weeks | Account? | Cost | Installs? |
|---|---|---|---|---|
| **Python 3.9+** (3.11+ recommended) | all | no | free | **yes** |
| **numpy** | 17–36 | no | free | yes (pip) |
| **pandas** | 21–36 | no | free | yes (pip) |
| **matplotlib** | 25–36 | no | free | yes (pip) |
| **scikit-learn** | 28–36 | no | free | yes (pip) |
| **VS Code** (or IDLE, which ships with Python) | all | no | free | yes |
| **JupyterLab** | 34–36 (capstone) | no | free | yes (pip) |

> **⚠️ Watch out — read this before week 1.** Nothing in this level uploads any data anywhere. Every
> dataset is typed out in the file, generated by the code, or built into scikit-learn. **There are no
> accounts, no API keys, no cloud services, and no chatbots in this entire course.** The only network
> access needed is `pip install`, once, in week 0. That is a deliberate design choice and it makes
> the privacy conversation from Level 1 easy to keep.

### The one-time setup: 45 minutes, in week 0

**Do it in week 0. Not in week 1.** Setup problems in week 6 feel like failure. Setup problems in
week 0 are just setup. Budget 45 minutes and expect to use 30.

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  ⏱️  WEEK 0 SETUP — 45 MINUTES, ONCE, BEFORE YOU MEET THE STUDENT     │
   ├───────────────────────────────────────────────────────────────────────┤
   │                                                                       │
   │  1. PYTHON (15 min)                                                   │
   │     In a terminal:   python3 --version                                │
   │     Want: 3.9 or higher. Ideally 3.11+.                               │
   │     If not: python.org/downloads                                      │
   │     ⚠️ WINDOWS: tick "Add python.exe to PATH" on the FIRST screen.    │
   │        That one checkbox is ~90% of all Windows setup pain.           │
   │                                                                       │
   │  2. A FOLDER AND A VENV (10 min)                                      │
   │       mkdir -p ~/ai-academy/level2 && cd ~/ai-academy/level2          │
   │       python3 -m venv .venv                                           │
   │       source .venv/bin/activate      # macOS / Linux                  │
   │       .venv\Scripts\activate         # Windows PowerShell             │
   │     Your prompt must now start with (.venv). That prefix is the       │
   │     whole game, and it does NOT stick between terminal sessions.      │
   │                                                                       │
   │  3. THE FOUR LIBRARIES (10 min, ~300 MB)                              │
   │       pip install --upgrade pip                                       │
   │       pip install numpy pandas matplotlib scikit-learn jupyterlab     │
   │                                                                       │
   │  4. THE SMOKE TEST (5 min)  ← the one that actually matters           │
   │     Make smoke.py with these three lines and run it:                  │
   │                                                                       │
   │       import numpy, pandas, matplotlib, sklearn                       │
   │       from sklearn.datasets import load_iris                          │
   │       print("Level 2 ready ·", numpy.__version__, load_iris().data.shape)
   │                                                                       │
   │     ✅ PASS:  Level 2 ready · 1.26.4 (150, 4)                         │
   │               (your version number will differ — that's fine)         │
   │     ❌ FAIL:  ModuleNotFoundError → it is almost always the venv.     │
   │               See the troubleshooting table in the orientation.       │
   │                                                                       │
   │  5. PROVE A CHART CAN APPEAR (5 min)                                  │
   │     Charts fail differently from everything else, so test them        │
   │     separately. The orientation has the 8-line smoke_plot.py.         │
   │     ✅ PASS: a window pops up, OR a smoke_plot.png file appears.      │
   │        Either one is a pass. Every chart in this course uses          │
   │        savefig, exactly so that a missing window never blocks you.    │
   │                                                                       │
   │  6. EDITOR (5 min)                                                    │
   │     VS Code + the Microsoft Python extension. Then:                   │
   │     Ctrl+Shift+P → "Python: Select Interpreter" → pick the one with   │
   │     .venv in its path. Skipping that click is the #1 mystery bug.     │
   │                                                                       │
   ├───────────────────────────────────────────────────────────────────────┤
   │  ✅ ALL SIX DONE?  You are set up for the entire school year.         │
   │  Write the `source .venv/bin/activate` line on a sticky note and      │
   │  put it on the laptop. You will need it every single session.         │
   └───────────────────────────────────────────────────────────────────────┘
```

> ### 👉 **The full install guide — with every command for macOS, Windows and Linux, and a troubleshooting table covering the 12 most likely failures — is Section 4 of [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md).** Do not improvise the install. It is written out.

---

## 🛟 If Something Goes Wrong

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` — but pip said it installed | You installed into one Python and are running another. Run `python -c "import sys; print(sys.executable)"` — the path **must** contain `.venv`. If not: activate again, and in VS Code re-pick the interpreter. Orientation §4, row 2. |
| `python: command not found`, or Windows opens the Microsoft Store | Try `python3`, then `py -3`. Then re-run the installer with **Add to PATH** ticked, and open a **new** terminal. Orientation §4, row 1. |
| `error: externally-managed-environment` | You skipped the venv. This error is doing you a favour. Do setup step 2. Never use `--break-system-packages`. |
| `plt.show()` shows nothing | Not a real problem. Every chart in this course also calls `fig.savefig(...)`. Open the PNG. Orientation §4, row 4. |
| `IndentationError` on a line that looks fine | Tabs mixed with spaces. In VS Code: bottom bar → **Spaces: 4** → *Convert Indentation to Spaces*. Then leave it on spaces forever. |
| The student's file is named `random.py` / `csv.py` / `stats.py` and imports break weirdly | Python found *their* file instead of the library. Rename it and delete the `__pycache__` folder beside it. (Week 12 deliberately names a file `stats.py` — and the teacher file for that week explains exactly why that is safe there and not elsewhere.) |
| A lesson ran out of time | Cut the ✍️ practice, never the 💻 code block or the 🎲 activity. Practice moves to homework; the typing is where the learning lives. |
| The student is stuck and frustrated | **Do not take the keyboard.** Orientation §8 is entirely about this and it is the single most important teaching skill in this level. Read it before week 1. |
| The student is bored | You are explaining for too long. Every explanation in every teacher file is capped at 12 minutes for a reason. Get to the keyboard. |
| **You** don't understand the code | Section 1 of the orientation is a complete Python mini-course written for an adult who has never programmed. Search it. Then say "I don't know, let's find out" out loud — that is on the syllabus too. |

---

## ▶️ Start Here

> ### 1. 📕 Teachers, read this first — once, cover to cover, ~90 minutes
> ### 👉 **[teacher-guide/00-orientation.md](teacher-guide/00-orientation.md)**
>
> It contains a complete Python mini-course for an adult who has never programmed, an annotated real
> traceback plus the 12 errors every beginner hits, what machine learning adds on top, the
> bulletproof install guide, the 20 questions students ask in a coding class, the 15 things adults
> get wrong when teaching beginners to program, the lesson shape, **how to help without taking the
> keyboard**, how to mark code, and a pre-flight checklist.
>
> Ninety minutes. It is the difference between teaching this course and surviving it.

> ### 2. 🔧 Then do the week 0 setup, alone, with nobody watching
> ### 👉 **Orientation Section 4** — and get both smoke tests passing

> ### 3. 📗 Then open Week 1 with the student
> ### 👉 **[student-guide/week-01.md](student-guide/week-01.md)**

> ### 4. 📘 And set the first homework
> ### 👉 **[workbook/week-01.md](workbook/week-01.md)**

---

## 🧾 The Promise

Thirty-six weeks from now, someone will send your student a spreadsheet and ask them what it says.

They will not open it and squint. They will load it in pandas, print `df.info()`, notice that the
`age` column came in as `object` because three rows say `"unknown"`, fix it, **log the fix and the
reason**, chart the distribution with both axes labelled, notice the outlier, chase it down, and only
*then* answer the question — with the number of rows stated out loud and the y-axis starting at zero.

And when someone says *"can you make it predict?"*, they will say:

> *"Yes. But first I'm holding back 20% of these rows, and the number I tell you will be the score on
> those — not on the ones it learned from. I'll give you both, actually, because the gap between them
> is the interesting part. If the training score is 100% and the test score is 74%, it didn't learn
> anything. It memorised. Want to see the curve?"*

That sentence is the whole level. It started with `print("hello")` in week 1.

---

[⬅ Level 2 modules](../README.md) · [Teacher Orientation](teacher-guide/00-orientation.md) · [Week 1 student guide](student-guide/week-01.md) · [Week 1 workbook](workbook/week-01.md) · [Figure style guide](figures/STYLE.md) · [Glossary](../glossary.md) · [Capstone](../capstone.md) · [Assessment pack](../assessment.md) · [Level 1 course](../../level-1-explorer/36-week-course/README.md)
