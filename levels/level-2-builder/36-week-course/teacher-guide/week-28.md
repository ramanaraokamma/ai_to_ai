# Week 28 — X and y: Turning Your Table Into a Question

[⬅ Week 27](week-27.md) · [Course Home](../README.md) · [Week 29 ➡](week-29.md) · [Student Guide](../student-guide/week-28.md) · [Workbook](../workbook/week-28.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the first week of Term 4, and the week Level 1's vocabulary finally becomes code |
| **Big idea** | Every model needs the table split into `X` (what you measured) and `y` (what you want back) — Level 1's *features* and *label*, finally spelled out in code. |
| **New vocabulary** | `X` · `y` · feature matrix · target · Euclidean distance |
| **New syntax** | `from sklearn.datasets import load_iris` · `X = df[["a", "b"]]` (two brackets) · `np.sqrt(x)` · `((row_a - row_b) ** 2).sum()` |
| **Materials** | Printed workbook pages 28.1–28.6 · **squared / graph paper, two sheets** · a ruler with millimetres · a pencil · a calculator · **the sheet from Week 1 of Level 1** where the student wrote what a feature and a label are |
| **Tech needed** | One laptop with Python 3, numpy, pandas, matplotlib **and scikit-learn**. Scikit-learn is new this term — install it *before* the lesson (see Prep). |
| **Prep time** | 20 minutes the night before (15 of which is running the code yourself), 5 minutes on the day |

> **⚠️ Watch out:** the install is the only thing in this week that can eat your lesson. `pip install scikit-learn` downloads about 30 MB and takes a couple of minutes on a good connection. **Do it the night before, and run the smoke test.** If it fails on the day you still have a complete paper lesson — see the Prep Checklist fallback.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Split a table into `X` and `y`** and state the shape of each one out loud.
2. **Explain why `X` needs two sets of brackets and `y` needs one**, in terms of *table* versus *column*.
3. **Load a dataset that ships inside scikit-learn** and print its shape.
4. **Compute the distance between two feature rows by hand on paper**, showing all four steps.
5. **Match the hand-computed distance to numpy's answer to two decimal places.**

Observable evidence: a workbook page with `X.shape` and `y.shape` written in ink, a sheet of graph paper with two points, a right-angled triangle and a ruler measurement on it, and a terminal showing `3.23` next to a hand-written `3.23`.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**Read this section even if you skip everything else.** It is written for somebody who has never programmed and has never met machine learning. It takes about twenty minutes and it will make you genuinely able to answer "but why?" in class.

### 1. What this term is actually about, in one paragraph

For twenty-seven weeks the student has been *describing* data: putting it in tables, cleaning it, drawing it. This term they start *predicting* with it. A prediction machine — a **model** — is a thing you show a pile of examples with the answers filled in, and which then produces an answer for an example it has never seen.

Every such machine, without exception, wants the data handed to it in exactly two pieces. Not one, not three. Two. This week is about those two pieces and nothing else. **We do not train a model this week.** That is next week. This week we lay the table.

### 2. The two pieces, and why they have such odd names

> **`X`** — the table of measurements. One **row per example**, one **column per measurement**.
> **`y`** — the answers. One value per row, lined up with `X` row for row.

The names come from school algebra, where `y = f(x)` means "y depends on x". A capital `X` because it is a *table* (many rows, many columns), a small `y` because it is a *single column*. Everybody in the world uses these two letters, so the student may as well meet them now. **They are the only two single-letter variable names allowed in this whole course**, and it is worth saying that out loud, because Weeks 1–27 banned them.

The student already knows both of these ideas under different names. In Level 1 they called them **features** and the **label**. Nothing new is being taught here except the spelling.

| Level 1 word | This week's word | What it is |
|---|---|---|
| feature | a column of `X` | one thing you measured |
| the features, all of them | `X`, the **feature matrix** | the whole block of measurements |
| label | `y`, the **target** | the answer you want back |

> **Feature matrix** — a rectangle of numbers: every row is one example, every column is one measurement. "Matrix" is just the maths word for "rectangle of numbers".
> **Target** — the column you are trying to predict. Also called the label.

![One table, two jobs](../figures/fig-w28-1-table-splits-into-x-and-y.svg)
*Figure 28.1 — One table splits into two. The measurements go into `X`. The answer goes into `y`. The song's name goes into neither.*

### 3. The rule that breaks things silently: rows must stay lined up

This is the one thing in this section that will actually bite you.

`X` and `y` are two separate objects. Nothing inside Python is watching to make sure row 4 of `X` still belongs to answer 4 of `y`. If the student sorts one and not the other, or filters one and not the other, **Python will not complain**. The model will train happily on scrambled data and produce a score that looks plausible and means nothing.

So the habit, and please enforce it out loud every week from now on:

> **Do all your filtering and sorting on the whole table. Pull out `X` and `y` last, and never touch them again.**

![The two shapes have to agree](../figures/fig-w28-5-shapes-must-line-up.svg)
*Figure 28.2 — Count the rows in both, every time. Four rows of measurements need four answers, and nothing in Python will tell you when they do not.*

### 4. The brackets. This is the confusing bit, and here is the whole of it

The student has been using `df["column"]` since Week 21. This week they meet `df[["a", "b"]]` and the extra brackets look like a typo. They are not.

```python
one = playlist["bpm"]          # ONE bracket  -> a single column
two = playlist[["bpm"]]        # TWO brackets -> a table that has one column in it
```

Here is the thing that makes it click, and it is worth drawing on paper:

- **The inner brackets are a list.** `["bpm", "minutes"]` is a list of two column names — the same kind of list they built in Week 11.
- **The outer brackets are "look this up in the table."**

So `playlist[["bpm", "minutes"]]` reads as: *look up, in the table, this list of two names.* Ask for a list of names, get a table back. Ask for one name, get one column back.

And that maps exactly onto what we need:

| We want | Brackets | What comes back | Its shape |
|---|---|---|---|
| `X` — a table of measurements | two | a table | `(10, 2)` |
| `y` — one column of answers | one | a column | `(10,)` |

**That shape `(10,)` is not a typo either.** It means "ten things, in a single line". Python writes a one-item description with a trailing comma so you can tell `(10,)` — ten things in a row — from `(10, 1)` — ten rows of one column each. A model wants `y` as `(10,)`. If a student hands it `(10, 1)` they will get a warning, and next week they will meet it.

### 5. Euclidean distance: it is Pythagoras, and it is not new maths

Next week's model works by asking "which known examples is this new one *closest* to?" So we need to be able to say how far apart two rows are. Here is the entire idea.

Walk 3 metres east and 4 metres north. How far are you from where you started? **Not 7.** You went diagonally. The straight-line distance is √(3² + 4²) = √25 = **5**. That is Pythagoras' theorem, which the student may or may not have met in maths yet — it does not matter, because we are going to do it as four counting steps rather than as a theorem.

> **Euclidean distance** — straight-line distance. Subtract, square, add up, square-root.

Say it as a four-step recipe and never as a formula:

1. **Subtract**, column by column. You get one gap per column.
2. **Square** each gap. (Squaring throws the minus signs away, which is exactly what you want — a gap of −3 is just as big as a gap of +3.)
3. **Add** the squares up. One number now.
4. **Square root** it.

Two flowers, using petal length and petal width:

```
flower A = (1.4, 0.2)        flower B = (4.4, 1.4)

step 1  subtract :   1.4 − 4.4 = −3.0      0.2 − 1.4 = −1.2
step 2  square   :   (−3.0)² = 9.00        (−1.2)² = 1.44
step 3  add      :   9.00 + 1.44 = 10.44
step 4  root     :   √10.44 = 3.23
```

![Measure it, or work it out. Same answer.](../figures/fig-w28-4-distance-by-ruler-and-formula.svg)
*Figure 28.3 — Plot the two flowers, and the distance is a line you can measure with a ruler. The four steps give the same number without the ruler.*

**Why bother with the four steps if you can use a ruler?** Because iris has four measurements per flower, not two, and the wine dataset next fortnight has thirteen. You cannot draw thirteen directions on a sheet of paper. But you can still subtract thirteen times, square thirteen times, add them up and take a root. **The arithmetic works in as many columns as you like; the picture only works in two.** That sentence is the whole reason the four steps exist, and it is worth saying to the student word for word.

### 6. Every line of this week's code, explained to somebody who has never programmed

Here is the complete new syntax for the week. Four things.

```python
from sklearn.datasets import load_iris
```

`sklearn` is the library. `sklearn.datasets` is a room inside it that holds a few small, famous datasets. `load_iris` is a function in that room. This line says: *go into that room and fetch me the thing called `load_iris`, so I can use its name directly.* The student has done this since Week 12 with their own files (`from stats import mean`), so the shape is familiar; only the names are new.

> **⚠️ Watch out:** the thing you install is called **scikit-learn** and the thing you import is called **sklearn**. Two different names for one library. This is genuinely annoying and it is nobody's fault; it is a historical accident. Expect to say it three times.

```python
iris = load_iris()
```

The round brackets *run* the function. Without them you have not fetched the data, you have fetched the machine that fetches the data — and the error message you get later will be confusing. `iris` now holds a bundle: `iris.data` is the table of measurements, `iris.target` is the answers, `iris.feature_names` is the list of column names, `iris.target_names` is the list of flower names.

```python
X = playlist[["bpm", "minutes"]]
y = playlist["mood"]
```

Covered in section 4. Two brackets for the table, one for the column.

```python
gaps = flower_a - flower_b
```

If `flower_a` and `flower_b` are **numpy arrays** (Week 17), this subtracts them column by column and hands back an array of gaps. If they are plain Python **lists**, it crashes — you cannot subtract one list from another. That crash is in the Debugging Clinic and it is a good one to meet.

```python
squares = gaps ** 2
```

`**` is "to the power of" (Week 3). On a numpy array it squares *every* number at once, with no loop. This is the whole point of Weeks 17–20 paying off.

```python
total = squares.sum()
```

Adds every number in the array up (Week 18). Note the brackets — `squares.sum` without them gives you the machine rather than the answer, and produces a genuinely baffling error message. It is in the Clinic.

```python
distance = np.sqrt(total)
```

Square root. That is all `np.sqrt` does.

And the whole thing on one line, which is what the syntax ladder calls for:

```python
distance = np.sqrt(((flower_a - flower_b) ** 2).sum())
```

**Read it from the inside out**, and teach the student to do the same: innermost brackets first (subtract), then square, then `.sum()`, then `np.sqrt`. Four steps, written right to left. If a student finds the one-liner unreadable, let them keep the four separate lines forever. **The four-line version is not the beginner version; it is the readable version.**

### 7. The three misconceptions you will actually meet

**Misconception 1 — "`X` is the answer, because x is what you solve for in maths."**

Very common, and it comes from algebra lessons where `x` is the unknown. Here it is the opposite: `X` is everything you already know, and `y` is the unknown. The fix that works: point at the table and say *"`X` is what you can measure with a ruler. `y` is what you have to be told."* Then have them say which is which for three examples out loud.

**Misconception 2 — "the more columns in `X`, the better."**

They met the truth in Level 1 (a useless column lands exactly on the baseline; a leaky column is worse than useless) and they will meet it again in Week 31. This week the specific instance is the `song` column. A song's *name* appears in exactly one row. A model can only memorise "Rocket → hype", which tells it nothing about a song it has not heard. **Names, IDs and row numbers never go in `X`.** If a student wants to include `song`, do not just say no — ask "what would the model do with the name of a song it has never seen?" and wait.

**Misconception 3 — "the distance number means something on its own."**

It does not. A distance of 12.01 between two songs sounds big; a distance of 3.23 between two flowers sounds small. But the songs were measured in beats per minute (numbers in the hundreds) and the flowers in centimetres (numbers under seven). **A distance is only ever meaningful compared to other distances in the same table.** This is the seed of Week 30's whole lesson, and if a student notices it this week, write their name next to it in the margin and tell them they are two weeks early.

### 8. How deep to go, and where to stop

**Go this far:** `X` and `y`, both shapes, the bracket rule, loading iris, the four distance steps, matching hand arithmetic to numpy.

**Stop before:**
- **Training anything.** No `fit`, no `predict`, no model of any kind. That is Week 29 and it is the whole of Week 29. If a student asks "so how do we actually guess?", the honest answer is *"next week, and it is three lines"* — and then do not spoil it.
- **Scaling.** You will be tempted, because `bpm` in the hundreds against `minutes` under six is an obvious problem and the student may well spot it. If they do: brilliant, write it on the wall, it is Week 30's entire lesson. Do not teach it today.
- **train/test splitting.** Week 29.
- **Any other distance.** There are others (Manhattan, cosine). Not this year.
- **`.values` and numpy-vs-pandas conversions.** Keep `X` as a DataFrame this week. Sklearn accepts DataFrames perfectly happily. Adding `.values` adds a concept and buys nothing today.

---

### 9. 🧭 The Growing Map — two minutes on the stage that just opened

The student guide carries one figure each week that is deliberately not about the week's topic: the
same five-stage pipeline, one more piece filled in. It is the only place either book shows the learner
the shape of the whole year. This week's is the biggest single change it has made since Week 10.

![The Level 2 pipeline in Week 28: the last stage opens at the X, y, kNN and trees tile](../figures/fig-w28-0-where-this-fits.svg)

*Figure 28.0 — Week 28's version. The last stage, `PREDICT & CHECK`, goes solid and the gold badge
lands on its first tile, weeks 28 to 31. One dashed box left on the map. Two threads lit:
representation and model.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and read the three things written in the gold tile — `X, y`, `kNN`, `trees`.** Ask
   *"which of those three did we actually do today?"* You want a finger on **`X, y`** and nothing else.
   Then push once: *"and what is X?"* The answer you are listening for is **the measurements**, or
   the four flower columns, or *the table without the answer column* — any of those is right. If they
   say "the data", ask which part.
2. **Then the question about the shape of the map:** *"count the solid stages — four and a bit out of
   five. So why are we not nearly finished?"* Let it sit. The honest answer is that the last box is
   five weeks long and holds the whole of the capstone, and hearing that now prevents the
   *"we've basically done it"* slump that arrives around Week 32.
3. **Have them ink their own copy** and write their two shapes — `(150, 4)` and `(150,)` — inside the
   tile. Insist on the trailing comma in the second one. It is the entire difference between a table
   and a column, and they have now met it in three different notations.

> **🧑‍🏫 Why this is worth two minutes.** This is a week of two letters and some brackets, and from the
> inside it can feel like the smallest lesson of the term. The map is what tells them otherwise: a
> stage that has been dashed since September is now solid, and it went solid because they can name what
> goes in and what comes out. That is genuinely the whole of the term's setup, and a learner who sees
> it as an arrival rather than a bracket rule types `df[["a", "b"]]` with intent next week.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Install scikit-learn, and do it tonight.** In the terminal, inside the project folder and with the virtual environment active:

  ```bash
  pip install scikit-learn
  ```

  It will print a lot of lines and finish with something like `Successfully installed scikit-learn-1.7.1`. The exact version number does not matter as long as it is 1.0 or higher.

- [ ] **Run the smoke test yourself.** Create a file called `sklearn_check.py` and type this in:

  ```python
  # sklearn_check.py
  # Check that the four libraries are installed and can be imported.

  import numpy as np                      # numbers in arrays (week 17)
  import pandas as pd                     # tables with names on (week 21)
  import matplotlib                       # charts (week 25)
  import sklearn                          # the new one: machine learning

  print("numpy      ", np.__version__)    # print the version of each library
  print("pandas     ", pd.__version__)
  print("matplotlib ", matplotlib.__version__)
  print("scikit-learn", sklearn.__version__)
  print("All four libraries are here.")
  ```

  Run it with `python3 sklearn_check.py`. You should see four version numbers and the last line. Yours will differ from mine; that is fine.

  ```text
  numpy       1.26.4
  pandas      1.5.3
  matplotlib  3.7.1
  scikit-learn 1.7.1
  All four libraries are here.
  ```

  > **🐞 If you see this error:** `ModuleNotFoundError: No module named 'sklearn'` — the install did not land in the Python you are running. Check the virtual environment is active (your prompt should show its name) and try `python3 -m pip install scikit-learn`.

- [ ] **Run the iris loader yourself**, so nothing surprises you on the shared screen. Create `iris_shapes.py`:

  ```python
  # iris_shapes.py
  # A real dataset that comes free inside scikit-learn: 150 iris flowers.

  import numpy as np
  import pandas as pd
  from sklearn.datasets import load_iris   # the new import this week

  iris = load_iris()                       # load it. No file, no download.

  print("X shape:", iris.data.shape)       # the measurements
  print("y shape:", iris.target.shape)     # the answers
  print()
  print("the four things measured:")
  for name in iris.feature_names:          # loop over the column names
      print("   ", name)
  print()
  print("the three kinds of flower:", iris.target_names)
  print("how many of each:", np.bincount(iris.target))
  print()

  # Put it in a DataFrame so week 21-24 skills still work.
  flowers = pd.DataFrame(iris.data, columns=iris.feature_names)
  flowers["species"] = iris.target_names[iris.target]

  # Show just the two petal columns and the answer, so it fits the screen.
  print(flowers[["petal length (cm)", "petal width (cm)", "species"]].head(3))
  ```

  Expected output, exactly:

  ```text
  X shape: (150, 4)
  y shape: (150,)

  the four things measured:
      sepal length (cm)
      sepal width (cm)
      petal length (cm)
      petal width (cm)

  the three kinds of flower: ['setosa' 'versicolor' 'virginica']
  how many of each: [50 50 50]

     petal length (cm)  petal width (cm) species
  0                1.4               0.2  setosa
  1                1.4               0.2  setosa
  2                1.3               0.2  setosa
  ```

- [ ] **Do the distance by hand yourself, with a pencil.** √10.44 = 3.23. Two minutes. It buys you fifteen minutes of confidence.
- [ ] Print workbook pages 28.1–28.6.
- [ ] **Find the Level 1 Week 1 sheet** where the student wrote, in their own words, what a feature is and what a label is. This is the emotional centre of the lesson. If it is genuinely lost, the fallback is below.
- [ ] Read section 4 (the brackets) twice. It is the thing you will be asked about most.

### 5 minutes on the day

- [ ] Laptop on, terminal open, virtual environment active, editor open on an empty file.
- [ ] Run `sklearn_check.py` once, now, before the student arrives. If it works now it will work in ten minutes.
- [ ] Two sheets of graph paper and a millimetre ruler on the table.
- [ ] The Week 1 sheet, face down, where the student cannot see it.
- [ ] A blank sheet headed **SHAPES** in big letters, landscape. Every shape found today gets written on it.

### Fallback if a laptop or an install fails

| If this fails | Do this instead |
|---|---|
| **scikit-learn will not install** | The whole lesson runs on paper and one graph. The iris numbers you need are printed on workbook page 28.3 — twelve real rows, copied out. Do the split, the shapes and the distance by hand; type the code next week when the install is fixed. **You lose nothing today except the printout of `(150, 4)`.** |
| **No laptop at all** | Same as above. This is the most paper-friendly week of Term 4, deliberately, because the term's install lands here. |
| **The student cannot find their Week 1 sheet** | Ask them to write the two definitions again, right now, from memory, before you say anything else about the lesson. Then keep that sheet. It works nearly as well and it is a fair test. |
| **No graph paper** | Any lined paper turned sideways, or draw a 10×10 grid with a ruler. Or use the pre-drawn grid on workbook page 28.4. |
| **The student read ahead and already knows about kNN** | Excellent. Hand them the keyboard and make *them* explain to you why `X` needs two brackets. Then give them the harder distance question from Differentiation → flying. Do **not** let them train a model today; hold that line, because next week's lesson is built on the anticipation. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Read Your Own Handwriting From Six Months Ago | 7 | 7 | The Week 1 sheet comes back out |
| 🧠 Concept — Two Pieces, Two Shapes, Two Brackets | 16 | 23 | `X`, `y`, and why the brackets differ |
| 💻 Live-Code Together — Split a Table, Load Iris | 18 | 41 | Both of you typing; two deliberate mistakes |
| 🎲 Their Turn — Ruler, Pythagoras, numpy | 20 | 61 | Three routes to 3.23, and they must agree |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Read Your Own Handwriting From Six Months Ago (7 minutes)

**Do this:** Sit down with the Week 1 sheet still face down. Do not open the laptop yet.

**Say this:**

> "Before we start anything today, I want you to read something out loud. It's not mine. You wrote it."

*(Turn the sheet over and slide it across.)*

> "Somewhere on there you wrote down, in your own words, what a **feature** is and what a **label** is. Read me both of them, exactly as you wrote them."

Let them read it. Let it be a bit awkward or a bit funny or a bit wrong. Do not correct anything.

> "Right. Now — was that hard to read back? Do you still agree with it?"

*(However they answer.)*

> "Here's why I dug that out. You have been ready for today's lesson for **six months**. You already know what a feature is. You already know what a label is. You know features go in and the label comes out. You know a name column is useless because it only shows up once. You know all of it.
>
> What you haven't had, until today, is the **spelling**. And that's genuinely all today is. The whole world of machine learning agrees on two letters for those two things, and they are `X` and `y`. Capital X. Small y.
>
> `X` is your features. All of them, in a block. `y` is your label, in a single column.
>
> And I want to be honest about the size of today's lesson, because it's smaller than it looks. We are not going to make anything predict anything today. Not one guess. Today we lay the table. Next week we eat."

**Do this:** Write on the SHAPES sheet, big:

```
X  =  what you measured        (a TABLE)
y  =  what you want back       (one COLUMN)
```

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "In the fruit-bowl table from Level 1 — colour, mass, length, and then apple/orange/banana — what's `X` and what's `y`?" | `X` = colour, mass, length. `y` = the fruit name. | If they put the fruit name in `X`, say: "If you already know it's an apple, what are you predicting?" and wait. |
| "Guessing which club someone joins from their age and their practice hours. `X`? `y`?" | `X` = age and hours. `y` = the club. | If they hesitate, ask the two questions in order: "What can you measure?" then "What has to be told to you?" |
| "Why do you reckon everybody uses two letters instead of proper names?" | Because it's the same two things every single time, in every problem. | If they say "because programmers are lazy" — fair, and half right. Add: "and because it's the *only* place in this course where a one-letter name is allowed." |
| "Anything on your Week 1 sheet you'd change now?" | Anything. This is a free question. | If they say no, that is a fine answer. If they spot something wrong, that is a better one. Either way, keep the sheet. |

---

### 🧠 Concept — Two Pieces, Two Shapes, Two Brackets (16 minutes)

**Do this:** Put workbook page 28.2 between you — the ten-song playlist table. Nothing on the laptop yet.

| song | bpm | minutes | **mood** |
|---|---|---|---|
| Monsoon | 68 | 4.2 | **chill** |
| Rocket | 148 | 3.1 | **hype** |
| Lantern | 80 | 3.8 | **chill** |
| Corridor | 160 | 2.8 | **hype** |
| Firecracker | 152 | 3.4 | **hype** |
| Slow Bus | 72 | 5.1 | **chill** |
| Neon | 168 | 2.6 | **hype** |
| Paper Boat | 76 | 4.6 | **chill** |
| Stadium | 140 | 3.0 | **hype** |
| Rooftop | 84 | 5.4 | **chill** |

**Say this — part 1, the split:**

> "Ten songs off a playlist. For each one somebody measured two things: the **beats per minute**, which is how fast it feels, and how many **minutes** long it is. And then somebody listened to it and wrote down whether it's a chill song or a hype song.
>
> Point at the columns that go into `X`."

Let them point. `bpm` and `minutes`.

> "Point at the column that is `y`."

`mood`.

> "And what happens to `song`?"

Wait for it. If they say "it goes in X", ask the question: *"What would a machine do with the name of a song it has never heard?"*

> "Nothing. It goes in neither. A song's name shows up in exactly one row of this table. A machine can memorise 'Rocket is hype' and that helps it precisely never, because next time you'll hand it something called 'Umbrella' and it has learnt nothing at all.
>
> **Names, ID numbers and row numbers never go in `X`.** Not because it's a rule somebody made up — because there's nothing in there to learn."

**Say this — part 2, the shapes:**

> "Now the bit I actually want you to be able to say out loud, because I'm going to ask you for it every week for the rest of the year. **The shape.**
>
> `X` is ten rows and two columns. So we write its shape as `(10, 2)`. Rows first, columns second. Always in that order.
>
> `y` is ten answers, in one line. And here's where Python does something that looks like a typo. It writes that shape as `(10,)`. Ten, comma, nothing.
>
> Say it: 'ten comma nothing'."

Have them say it. It sounds ridiculous, which is why it sticks.

> "That trailing comma is Python telling you, on purpose: *this is a single line of ten things, not a table.* Because there's another shape it could have been — `(10, 1)`, which means ten rows of one column each. A skinny table. And a model wants `y` as a single line, not a skinny table. So the comma matters."

**Do this:** Write on the SHAPES sheet:

```
X.shape  =  (10, 2)     rows, then columns
y.shape  =  (10,)       ten comma nothing
```

**Say this — part 3, the brackets:**

> "Last thing before we type. How do we get those two pieces out of the table?
>
> You already know how to get one column. You've been doing it since Week 21: `playlist["mood"]`. One bracket, one name, one column back. That's `y`, done.
>
> For `X` we need **two** columns, and Python does something that looks like a mistake:

```
playlist[["bpm", "minutes"]]
```

> Two square brackets on each side. And it is not a typo. Look at what's actually happening. What's `["bpm", "minutes"]` on its own?"

Wait. They know this. It is a list — Week 11.

> "It's a **list**. A list of two column names. So the inner brackets are just a list, exactly the same as `[1, 2, 3]`. And the outer brackets are the normal 'look this up in the table' brackets.
>
> So the whole thing reads: **look up, in the table, this list of names.** Ask for a *list* of names, get a *table* back. Ask for *one* name, get *one column* back.
>
> One bracket, a column. Two brackets, a table. `y` wants a column. `X` wants a table."

![One bracket or two?](../figures/fig-w28-2-one-bracket-two-brackets.svg)
*Figure 28.4 — Ask for one name and you get a column. Ask for a list of names and you get a table. `y` wants the first. `X` wants the second.*

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "`X` has shape `(10, 2)`. What's the 10 and what's the 2?" | 10 songs, 2 measurements. Rows then columns. | If they swap them, point at the table and count out loud together. Then write "rows, then columns" on the SHAPES sheet and underline it twice. |
| "Why not put `song` in `X`?" | It's unique to one row; there's nothing to learn from it. | If they say "because it's words not numbers" — that's a real and different objection, and worth crediting. Reply: "Good, that's true too. But `mood` is words as well and it's fine. The killer is that a name never repeats." |
| "What's the shape of `y`?" | `(10,)`. | If they say `(10, 1)`, say: "Close, and it's a real shape — but it means a skinny table. We want a single line." |
| "If I added a third measurement — how loud it is — what changes?" | `X.shape` becomes `(10, 3)`. `y` doesn't change at all. | If they change `y` too, go back to the table and count the answers. Adding a column never adds an answer. |
| "How many brackets for a table? How many for a column?" | Two. One. | Drill this until it's instant. It is the most-typed mistake of the term. |

---

### 💻 Live-Code Together — Split a Table, Load Iris (18 minutes)

**Two chairs, one keyboard, and the student types.** You dictate; they type; you both read the output before moving on. If you have two machines, type in parallel — but you still read every output out loud before continuing.

**Do this:** New file, saved as `x_and_y.py` in the project folder.

**Keystroke sequence — part 1, build the table (4 minutes).**

Dictate exactly this. The comments are part of the dictation; do not skip them.

```python
# x_and_y.py
# Split one table into X (what we measured) and y (what we want back).

import pandas as pd

playlist = pd.DataFrame({
    "song":    ["Monsoon", "Rocket", "Lantern", "Corridor", "Firecracker",
                "Slow Bus", "Neon", "Paper Boat", "Stadium", "Rooftop"],
    "bpm":     [68, 148, 80, 160, 152, 72, 168, 76, 140, 84],
    "minutes": [4.2, 3.1, 3.8, 2.8, 3.4, 5.1, 2.6, 4.6, 3.0, 5.4],
    "mood":    ["chill", "hype", "chill", "hype", "hype",
                "chill", "hype", "chill", "hype", "chill"],
})

print(playlist)
```

Run it:

```text
          song  bpm  minutes   mood
0      Monsoon   68      4.2  chill
1       Rocket  148      3.1   hype
2      Lantern   80      3.8  chill
3     Corridor  160      2.8   hype
4  Firecracker  152      3.4   hype
5     Slow Bus   72      5.1  chill
6         Neon  168      2.6   hype
7   Paper Boat   76      4.6  chill
8      Stadium  140      3.0   hype
9      Rooftop   84      5.4  chill
```

Ten seconds of "yes, that's the table on the page", and move on.

**Keystroke sequence — part 2, ⚠️ DELIBERATE MISTAKE NUMBER ONE (5 minutes).**

**Do this:** Delete the `print(playlist)` line. Now type this, deliberately wrong, with one bracket:

```python
X = playlist["bpm", "minutes"]
print(X)
```

**Say this before you run it:**

> "Now. I'm going to get this wrong on purpose, because I want you to see the error *before* you make it yourself at ten o'clock tonight with nobody to ask. I've used one bracket where I need two. Watch."

Run it. You get this — and it is long:

```text
Traceback (most recent call last):
  File ".../pandas/core/indexes/base.py", line 3802, in get_loc
    return self._engine.get_loc(casted_key)
  ...
KeyError: ('bpm', 'minutes')

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/you/project/x_and_y.py", line 15, in <module>
    X = playlist["bpm", "minutes"]
  File ".../pandas/core/frame.py", line 3807, in __getitem__
    indexer = self.columns.get_loc(key)
  File ".../pandas/core/indexes/base.py", line 3804, in get_loc
    raise KeyError(key) from err
KeyError: ('bpm', 'minutes')
```

**Say this:**

> "Right. That is a *wall* of text and I want to teach you how to not be frightened of it. Same rule as always: **read the last line first.**
>
> `KeyError: ('bpm', 'minutes')`
>
> `KeyError` means 'I looked for a name and there is no column with that name.' And look what it says it went looking for: `('bpm', 'minutes')` — both of them, joined together, as one single name. Because with one bracket, that's what pandas thinks I asked for. One column, whose name is the pair 'bpm-and-minutes'. There isn't one. So: KeyError.
>
> And ignore everything in the middle. All those lines about `base.py` and `frame.py` are pandas showing you its own insides. **The line you care about is the one with your own filename in it**, which is line 15, which is the line I just typed."

Now fix it in front of them — add the second bracket:

```python
X = playlist[["bpm", "minutes"]]
print(X)
```

Run. The two-column table appears. Say: *"One character. That's the whole bug."*

**Keystroke sequence — part 3, the shapes (4 minutes).**

Replace the `print(X)` line and add:

```python
X = playlist[["bpm", "minutes"]]        # TWO brackets -> a table of features
y = playlist["mood"]                    # ONE bracket  -> a single column

print("X is a", type(X).__name__)       # what kind of thing did we get?
print("y is a", type(y).__name__)
print()
print("X.shape:", X.shape)              # (rows, columns)
print("y.shape:", y.shape)              # (rows,)  <- one number, then a comma
print()
print("first three rows of X:")
print(X.head(3))
print()
print("first three labels:")
print(y.head(3))
```

Run it:

```text
X is a DataFrame
y is a Series

X.shape: (10, 2)
y.shape: (10,)

first three rows of X:
   bpm  minutes
0   68      4.2
1  148      3.1
2   80      3.8

first three labels:
0    chill
1     hype
2    chill
Name: mood, dtype: object
```

**Say this:**

> "There it is. `X` is a **DataFrame** — that's pandas' word for a table. `y` is a **Series** — pandas' word for a single column. Two brackets gave a table, one bracket gave a column, exactly as advertised.
>
> And read me the two shapes."

Have them read `(10, 2)` and `(10,)` out loud. Have them write both on the SHAPES sheet themselves.

**Keystroke sequence — part 4, iris (5 minutes).**

**Do this:** New file, `iris_shapes.py`. Dictate the file from the Prep Checklist above, exactly as printed there. Run it. The output is in the Prep Checklist and should match line for line.

**Say this:**

> "Hundred and fifty flowers. Four measurements each. Somebody actually went out and measured a hundred and fifty irises with a ruler, in 1936, and it is still the first dataset everybody learns on. You did not download anything — it came inside the library.
>
> `X shape: (150, 4)`. A hundred and fifty rows, four columns. `y shape: (150,)`. A hundred and fifty answers, ten comma nothing style. Same two shapes as our playlist, just bigger.
>
> Fifty of each flower, look — `[50 50 50]`. Perfectly balanced, which is unusual and convenient and we will come back to why that matters."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "The traceback was fifteen lines. Which line mattered?" | The last one, and the one with our filename in it. | If they say "all of them", say: "Read me the third line." Then: "What did that tell you about your bug?" Nothing. That's the point. |
| "`KeyError: ('bpm', 'minutes')` — what did pandas think I wanted?" | One column with a weird two-part name. | If they can't say it, point at the brackets in the error and the brackets in the code side by side. |
| "iris `X` is `(150, 4)`. How many flowers, how many measurements?" | 150 flowers, 4 measurements. | If reversed, ask "would somebody measure four flowers a hundred and fifty times?" |
| "Where's the file the iris data came from?" | There isn't one — it's inside the library. | This surprises them. Worth a sentence: "Somebody put it in the box for you." |

---

### 🎲 Their Turn — Ruler, Pythagoras, numpy (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–7:** plot the two flowers on graph paper, draw the triangle, measure the slanted line with a ruler.
- **Minutes 7–13:** the four steps with a pencil. √10.44.
- **Minutes 13–20:** the same thing in numpy, including ⚠️ **deliberate mistake number two**. All three answers must agree to 2 dp.

---

## 🐞 The Debugging Clinic

Every error below was produced by actually running a broken version of this week's code. The messages are copied out verbatim; the long middle sections of the tracebacks are trimmed with `...` where they only show the library's own insides.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `KeyError: ('bpm', 'minutes')` | "I went looking for a column whose name is that whole pair, and there isn't one." | `playlist["bpm", "minutes"]` — one bracket where two are needed. | Add the inner brackets: `playlist[["bpm", "minutes"]]`. |
| `KeyError: "['minute'] not in index"` | "One of the names on your list is not a column in this table." Note it names the culprit. | A typo in a column name — `minute` for `minutes`. | Fix the spelling. `print(playlist.columns)` shows the exact names, including any stray spaces. |
| `TypeError: unsupported operand type(s) for -: 'list' and 'list'` | "You cannot subtract one list from another. Lists are not numbers." | `flower_a = [1.4, 0.2]` instead of `np.array([1.4, 0.2])`. | Wrap both in `np.array(...)`. Only numpy arrays subtract column by column. |
| `AttributeError: 'function' object has no attribute 'data'` | "The thing you're asking for `.data` from is a machine, not data." | `iris = load_iris` — the brackets were left off, so `iris` holds the function itself. | `iris = load_iris()`. The brackets are what run it. |
| `TypeError: 'tuple' object is not callable` | "You put brackets after something that isn't a function." | `iris.data.shape()` — `shape` is already the answer; it is not a machine you run. | Drop the brackets: `iris.data.shape`. (Compare `.sum()`, which *is* a machine and does need them.) |
| `TypeError: loop of ufunc does not support argument 0 of type builtin_function_or_method which has no callable sqrt method` | "You asked me for the square root of a machine instead of a number." | `total = (gaps ** 2).sum` — the brackets after `sum` were forgotten. | `total = (gaps ** 2).sum()`. |
| `ImportError: cannot import name 'load_irs' from 'sklearn.datasets'` | "That room exists, but there is nothing in it with that name." | Typo in the function name: `load_irs` for `load_iris`. | Fix the spelling. |
| `ModuleNotFoundError: No module named 'sklearn'` | "There is no library by that name in the Python I am running." | scikit-learn is not installed, or is installed in a different Python. | `pip install scikit-learn` with the virtual environment active. Remember: install **scikit-learn**, import **sklearn**. |
| `SyntaxError: invalid syntax` pointing at `import scikit-learn` | "The hyphen is a minus sign to me, and this is not arithmetic." | The student typed the *install* name into an `import` line. | `import sklearn`. Say it out loud: "install scikit-learn, import sklearn." |

### How to teach debugging without giving the answer

The escalation ladder, in order. Do not skip a rung, and count to ten in your head between rungs.

1. **"Read me the last line."** Out loud. Nothing else. Half of all bugs die here.
2. **"Which line of *your* file is it pointing at?"** Teach them to scan the traceback for their own filename and ignore everything else.
3. **"What was Python looking for, and what did it find?"** Every error message names both. `KeyError: ('bpm', 'minutes')` tells you exactly what it went hunting for.
4. **"What did you change since it last worked?"** If the answer is "loads", that is the real lesson: run it more often.
5. **Point at the line. Say nothing.** Just your finger on the screen.
6. **Point at the character.**
7. **Only now, tell them.** And when you do, say what the *class* of mistake was, not just the fix: "that's a brackets-versus-no-brackets one, and you'll meet it again."

> **🧑‍🏫 If a student asks:** *"Why is the error so long when the mistake is one character?"* — because the error is a *route map*. Python is showing you every room it walked through on its way to the crash. The first rooms are pandas' rooms and you did not write them. The last line is the crash, and the line with your filename is where you sent it in the wrong direction. Reading a traceback is a skill, and being able to ignore 80% of it is most of the skill.

---

## 🎲 The Activity, In Full

### Two Flowers, Three Ways to the Same Number

The point of this activity is not the arithmetic. It is the **agreement**. The student measures a length with a ruler, computes it with a pencil, and computes it with numpy, and all three come out at 3.23. When the same number arrives by three completely different routes, it stops being a formula you were told and becomes a fact about the world.

### Setup

**On the table:** graph paper, a millimetre ruler, a pencil, a calculator, workbook page 28.4 (the pre-drawn grid, as backup), the laptop with the editor open.

**On the board or SHAPES sheet, written before you start:**

```
flower A  =  (1.4, 0.2)
flower B  =  (4.4, 1.4)
```

Tell them where those numbers came from: they are rows 0 and 65 of the real iris table, using **petal length** and **petal width** only. Flower A is a *setosa*; flower B is a *versicolor*. Two of the four measurements, because two is all you can draw.

### Step 1 — Plot them (7 minutes)

1. Draw two axes in the bottom-left corner of the graph paper. Across the bottom: **petal length, in cm, 0 to 6**. Up the side: **petal width, in cm, 0 to 2**.
2. **Agree the scale out loud and write it on the sheet: 1 cm on the paper = 0.5 cm of flower.** So one unit of flower is two centimetres of paper. This matters — if they use a different scale on each axis the triangle will be the wrong shape and the ruler answer will be wrong.
3. Mark flower A at (1.4, 0.2). Mark flower B at (4.4, 1.4). Use a **circle** for A and a **triangle** for B — different shapes, not just different colours, so it still reads in pencil.
4. Join A to B with a straight line.
5. Now complete the right-angled triangle: from A, go straight across to sit underneath B; then straight up to B.

![A row is a point](../figures/fig-w28-3-row-as-a-point.svg)
*Figure 28.5 — Two numbers become one dot. The two dots become a triangle, and the distance is the slanted side.*

### Step 2 — Measure it, then work it out (6 minutes)

**Measure first.** Put the ruler on the slanted line. It should read about **6.5 cm on the paper**. Divide by 2 (because 2 cm of paper = 1 unit of flower) and you get **≈ 3.25**.

**Say this:**

> "Write that down and put a box round it. That is a measurement, so it's allowed to be a bit off. Rulers and pencils are not exact. We're going to see how close we got."

**Now the four steps, with a pencil.** Have them write all four lines out; do not let them do it in their head.

```
step 1   subtract      1.4 − 4.4 = −3.0        0.2 − 1.4 = −1.2
step 2   square        (−3.0)² = 9.00          (−1.2)² = 1.44
step 3   add up        9.00 + 1.44 = 10.44
step 4   square root   √10.44 = 3.2310988...
                                = 3.23  (2 dp)
```

**Ask, before they take the root:** *"Is your answer going to be bigger or smaller than 10.44?"* The answer is smaller, and a surprising number of people have to think about it. Square roots of numbers above 1 always come down.

### Step 3 — And now numpy (7 minutes)

**Do this:** New file, `distance_by_hand.py`. **⚠️ Deliberate mistake number two goes here.** Dictate this first, with plain lists:

```python
import numpy as np
flower_a = [1.4, 0.2]
flower_b = [4.4, 1.4]
gaps = flower_a - flower_b
print(gaps)
```

Run it:

```text
Traceback (most recent call last):
  File "/Users/you/project/distance_by_hand.py", line 4, in <module>
    gaps = flower_a - flower_b
TypeError: unsupported operand type(s) for -: 'list' and 'list'
```

**Say this:**

> "Last line. `TypeError: unsupported operand type(s) for -: 'list' and 'list'`. Unpack that. `operand` means 'a thing an operator works on'. The operator is the minus sign. And it's telling me the two things I gave it are both **lists**.
>
> You cannot subtract one list from another. A list is a row of boxes; it isn't a number. Back in Week 11 you found that adding two lists glues them together instead of adding them up — this is the same family of surprise.
>
> **numpy arrays** are the things that subtract column by column. That's exactly what we built them for in Week 17. One word each side and we're fixed."

Fix it in front of them:

```python
flower_a = np.array([1.4, 0.2])
flower_b = np.array([4.4, 1.4])
```

Run again: `[-3.  -1.2]`. **The same two gaps they wrote in pencil.** Stop and point at that. Then dictate the rest:

```python
# distance_by_hand.py
# The distance between two flowers, one step at a time.

import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()

# Columns 2 and 3 are petal length and petal width. 2:4 means "columns 2 and 3".
flower_a = iris.data[0, 2:4]             # row 0, the two petal columns
flower_b = iris.data[65, 2:4]            # row 65, the two petal columns

print("flower A:", flower_a, iris.target_names[iris.target[0]])
print("flower B:", flower_b, iris.target_names[iris.target[65]])
print()

gaps = flower_a - flower_b               # step 1: subtract, column by column
print("step 1  subtract   :", gaps)

squares = gaps ** 2                      # step 2: square each gap
print("step 2  square     :", squares)

total = squares.sum()                    # step 3: add the squares up
print("step 3  add up     :", total)

distance = np.sqrt(total)                # step 4: square root of the total
print("step 4  square root:", distance)
print()
print("distance rounded to 2 dp:", round(distance, 2))
print()
print("all four steps in one line:", np.sqrt(((flower_a - flower_b) ** 2).sum()))
```

Real output:

```text
flower A: [1.4 0.2] setosa
flower B: [4.4 1.4] versicolor

step 1  subtract   : [-3.  -1.2]
step 2  square     : [9.   1.44]
step 3  add up     : 10.440000000000003
step 4  square root: 3.2310988842807027

distance rounded to 2 dp: 3.23

all four steps in one line: 3.2310988842807027
```

> **🧑‍🏫 If a student asks:** *"Why does it say `10.440000000000003`? We got 10.44."* — **You are both right, and the computer is the one being slightly odd.** Computers store decimals in binary, the way we store thirds in decimal. One third is 0.3333… forever; you have to stop somewhere, and where you stop is a tiny error. `1.44` is one of the numbers that does not fit exactly in binary, so what got stored was a hair over. Add it to 9 and the hair is still there, thirteen decimal places down. It makes no difference to anything you will ever do — and it is why we round before we report. This is not a bug in Python. Every programming language on earth does this, and every professional has met it.

**Now the agreement.** Write all three on the SHAPES sheet, side by side:

```
ruler        ≈  3.25       (a measurement, allowed to be a bit off)
pencil          3.23       (exact arithmetic, rounded)
numpy           3.23       (exact arithmetic, rounded)
```

**Say this:**

> "Two of those agree to the last digit, and the third one agrees as well as a pencil line and a plastic ruler can. You did not take my word for anything today. You measured it, you worked it out, and you got the machine to work it out, and all three came back with the same answer.
>
> And here's the sentence I actually want you to leave with. The ruler only worked because there were **two** measurements. Iris has four. Next fortnight we'll use a wine dataset with **thirteen**. You cannot draw thirteen directions on a piece of paper — but you can still subtract thirteen times, square thirteen times, add them up and take one root. **The arithmetic goes as far as you like. The picture stops at two.**"

### What "finished" looks like

- A sheet of graph paper with two labelled axes, a written scale, two differently-shaped points, and a right-angled triangle.
- A ruler measurement, in a box, written down **before** the arithmetic was done.
- Four lines of pencil arithmetic, one per step, with `10.44` and `3.23` visible.
- A terminal showing `3.23`.
- All three numbers written next to each other, and the student able to say why the ruler one is slightly different.

### Variation — easier

- **Use nicer numbers.** Do the plain 3-and-4 version first: two points 3 units apart across and 4 up. √(9 + 16) = √25 = **exactly 5**, and the ruler agrees beautifully. Then, and only then, do the real flowers.
- **Pre-draw the axes** on the graph paper before class, with the scale already written on.
- **Do steps 1 and 2 orally together** and let them write only steps 3 and 4.
- **Drop the numpy part entirely** and finish with the ruler-and-pencil agreement. That delivers objectives 1, 4 and 5 completely. Type the code next lesson.

### Variation — harder

1. **A third flower.** Row 100 of iris is a *virginica* with petals `(6.0, 2.5)`. Compute A-to-C and B-to-C as well. Then the question: **"Which of the three pairs is closest together, and does that match which two are the same species?"** *(A–B = 3.23, A–C = 5.14, B–C = 1.94. The closest pair is B–C, and they are* different *species — versicolor and virginica. That is a genuinely interesting failure, and it is why next week's model asks several neighbours to vote instead of trusting the closest one.)*
2. **All four columns.** Do the distance between rows 0 and 65 using all four measurements instead of two. Four subtractions, four squares, one root. `iris.data[0]` and `iris.data[65]` with no slicing. **Ask them to predict, before computing, whether the answer will be bigger or smaller than 3.23.** *(Bigger — 3.63. Adding more columns can only add more squares, and squares are never negative, so a distance never shrinks when you add a column.)*
3. **Break the line-up on purpose.** Sort `X` by `bpm` but leave `y` alone. Print them side by side and find the row where the mood no longer matches the song. Then write one sentence on why Python did not warn you.
4. **Zero distance.** Find two rows of iris whose petal distance is exactly 0.00 *(rows 0 and 1 — both `(1.4, 0.2)`)*. Then: "Are they the same flower?" *(No. They are two different flowers with identical petals. Same point, different plant. This matters next week when a model has to choose between them.)*

---

## ❓ Questions Students Ask This Week

**"Why capital X and small y? Is that just to be annoying?"**

There is an actual reason. A capital letter is the convention for a *table* — many rows, many columns. A small letter is the convention for a single line of values. So `X` is capital because it is a rectangle and `y` is small because it is a line. It comes from maths notation that is older than computers, and the whole world now agrees on it, so you will see the same two letters in every book, every tutorial and every library. It is one of the very few things in this field that nobody argues about.

**"Can `y` be a number instead of a category?"**

Yes, and that is a genuinely different kind of problem. If `y` is chill-or-hype, you are picking from a short list, and a guess is simply right or wrong. If `y` is *how many minutes long the song is*, you are predicting a number, and a guess can be *nearly* right — 3.1 when the truth was 3.2 is a good guess, not a wrong one. Level 1 called these two things classification and regression. We do the first kind for the next four weeks and the number kind in Week 32.

**"What if two columns are measured in totally different sizes? `bpm` is in the hundreds and `minutes` is under six."**

**That is the best question anybody can ask this week, and you have just found Week 30's entire lesson two weeks early.** The honest answer: it is a real and serious problem, it will wreck a model that measures distance, and there is a standard fix. Do not let me explain it today — write it on the wall with your name and the date, and hold me to it in a fortnight. *(Teacher: mean it. Write it on the wall. This is the single best moment in the week if it happens.)*

**"Why is the iris dataset flowers? Nobody cares about flowers."**

Fair. It is flowers because a statistician called Ronald Fisher used it in 1936, and it stuck — the way "hello, world" stuck. What makes it useful is not the flowers: it is that it is small enough to print, it has three classes rather than two, and two of the three classes genuinely overlap, so a model *cannot* get 100% and you get to see honest mistakes. A dataset where everything works is a bad teaching dataset. There is also a real problem with its history worth knowing: Fisher was a prominent eugenicist, and some people now avoid the dataset for that reason and use others instead. Both positions are held by serious people.

**"Does the order of the columns in `X` matter?"**

No, and yes. **For the arithmetic, no**: swap `bpm` and `minutes` and every distance comes out identical, because addition does not care what order you add things in. **For your sanity, yes**: `model.coef_` in Week 32 and `feature_importances_` in Week 31 hand you back a list of numbers *in the order of your columns*, with no names attached. If you shuffle the columns between two runs and forget, you will read the wrong number as the wrong feature. So pick an order and keep it.

**"How far apart do two things have to be before they count as 'far'?"** *(Answer honestly: nobody has a general answer.)*

**Nobody agrees on this, and it is not a dodge — it is a real open question in how these systems get used.** A distance of 3.23 is meaningless on its own. It is not big or small; it is 3.23 *of whatever units the columns happened to be in.* Change centimetres to millimetres and the same two flowers are 32.3 apart, without a single flower moving. So the only honest use of a distance is **comparing it with other distances in the same table**: this flower is closer to that one than to the third one. Where people genuinely disagree is what to do when the columns are in different units — how much to squash the big ones, whether to squash them at all, whether some columns *deserve* more say than others. There is a standard default (Week 30's), it is a good default, and it is a choice rather than a fact. Practitioners argue about it constantly.

**"Could I just include the song name and let the machine sort it out?"**

You can put it in, and something worse than an error will happen: it will appear to work brilliantly and be worthless. Every name is unique, so a model can look up "Rocket → hype" perfectly and score 100% on the songs it has already seen. Then the first new song arrives, its name has never appeared before, and the model has nothing at all. Level 1 had a word for a column that scores perfectly and helps never — a **leak**. The three-second test still applies: *at the moment I need the answer, does this value tell me anything about a case I have not seen?* A name never does.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| scikit-learn is not installed and the lesson stalls in minute 2 | The install was left to the day | Switch to the paper version immediately — page 28.3 has twelve real iris rows printed. Do not spend lesson time on pip. Fix the install afterwards, alone. |
| The student writes `X` as one bracket every single time | Two brackets look like a typo, and the brain corrects typos | Do not just correct it. Make them say the sentence out loud each time: **"a list of names, so a table comes back."** Three or four repetitions and it lands. |
| Shapes get read backwards — `(150, 4)` as four flowers | Nothing in the notation says which is which | Enforce the phrase **"rows, then columns"** every single time a shape is spoken, all term. Write it on the SHAPES sheet and point at it rather than saying it. |
| The `(10,)` trailing comma is dismissed as a typo | It looks exactly like a typo | Show them `(10, 1)` next to `(10,)` and ask which is the skinny table. The comma is doing a job: it says "there is no second number". |
| The ruler answer disagrees with the arithmetic by a lot | Different scale on the two axes, so the triangle is the wrong shape | Check the scale first, before anything else. Write it on the paper: **1 cm of paper = 0.5 cm of flower**, on *both* axes. |
| The student uses their head for step 2 and gets 1.44 wrong | Squaring a decimal is genuinely fiddly | Insist all four steps are written on paper, one line each. And a calculator is fine — this is not an arithmetic test. |
| A minus sign survives into step 2 | They wrote `−3.0² = −9` | Say it in words: "minus three, times minus three." Two negatives. Then have them do `(−1.2)²` out loud the same way. A squared number can never come out negative. |
| The output shows `10.440000000000003` and confidence collapses | It looks like the whole method just failed | Have the "if a student asks" answer ready and treat it as interesting rather than embarrassing. It is a real fact about computers and it is worth two honest minutes. |
| The student tries to train something | The whole term has been advertised as "make it predict" | Hold the line kindly: "Next week, and it's three lines of code, and you'll be ready for it. Today we lay the table." Then give them a harder-variation task so the energy has somewhere to go. |
| Fifteen minutes disappear into what "matrix" means | It is a scary word and it is on the page | One sentence and move on: "a rectangle of numbers." Nothing else about matrices is needed this year. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** iris. Do the whole lesson on the ten-song playlist. Ten rows you can see beats a hundred and fifty you cannot, and every objective except number 3 is fully deliverable on the playlist alone.

**Cut:** the one-line version of the distance. Four separate lines, forever, with four `print`s. It is not the beginner version — it is the readable version, and plenty of professionals write it that way.

**Reteach the shapes physically.** Cut the ten-song table into ten paper strips. Then cut each strip in two: the `bpm`/`minutes` end and the `mood` end. Put all ten measurement-halves in one pile and all ten answer-halves in another, **keeping them in order**. Count each pile out loud. "Ten rows and two columns." "Ten answers." Then deliberately shuffle one pile and ask what has just been broken. Physically sorting objects makes the line-up rule obvious in a way that no amount of explanation does.

**Copy-this-exactly scaffold.** Give them this and nothing else. Every line already correct, only the blanks to fill:

```python
import numpy as np

flower_a = np.array([1.4, 0.2])          # petal length, petal width
flower_b = np.array([4.4, 1.4])

gaps = flower_a - flower_b               # step 1
print("gaps:", gaps)                     # you should see [-3.  -1.2]

squares = gaps ** 2                      # step 2
print("squares:", squares)               # you should see [9.   1.44]

total = squares.sum()                     # step 3
print("total:", total)                    # you should see about 10.44

distance = np.sqrt(total)                 # step 4
print("distance:", round(distance, 2))    # you should see 3.23
```

Each `print` carries the answer it should produce. They fix the first line that disagrees and no others. This is a real professional technique, not a crutch — say so.

**The one thing you must not cut:** the ruler-and-pencil agreement. If the lesson collapses to one idea, make it *"a row of numbers is a point, and the distance between two points is something you can measure."*

### If the student is flying

Everything here uses only syntax they already have. Nothing new.

1. **The third flower** (Variation — harder, item 1). B and C are the closest pair and they are different species. Let that sit unresolved; it is Week 30.
2. **Four columns instead of two** (item 2), with the prediction made first. 3.61.
3. **Distance from one row to every row, with no loop.** They have broadcasting from Week 18 and `axis=1` from Week 19. This is the real payoff:

   ```python
   # distance_to_all.py
   # One mystery flower against six known ones, and no loop for the arithmetic.

   import numpy as np

   # Six real rows copied out of the iris table: petal length, petal width.
   six = np.array([[1.4, 0.2],              # rows 0-2 of iris: all setosa
                   [1.4, 0.2],
                   [1.3, 0.2],
                   [4.7, 1.4],              # rows 50-52 of iris: all versicolor
                   [4.5, 1.5],
                   [4.9, 1.5]])
   names = ["setosa", "setosa", "setosa",
            "versicolor", "versicolor", "versicolor"]

   mystery = np.array([3.0, 1.0])           # a flower somebody handed us

   print("the six known flowers:")
   print(six)
   print("shape:", six.shape)
   print()
   print("mystery flower:", mystery)
   print()

   gaps = six - mystery                     # broadcasting: one row against six rows
   squares = gaps ** 2                      # square every number in the block
   totals = squares.sum(axis=1)             # axis=1 -> add across each row
   distances = np.sqrt(totals)              # square root of each total

   print("distance to each of the six:", np.round(distances, 2))
   print()

   closest = distances.min()                # the smallest distance in the array
   for i in range(6):                       # walk the six and print them tidily
       mark = "  <- closest" if distances[i] == closest else ""
       print(f"  {names[i]:<11} distance {distances[i]:.2f}{mark}")
   ```

   ```text
   the six known flowers:
   [[1.4 0.2]
    [1.4 0.2]
    [1.3 0.2]
    [4.7 1.4]
    [4.5 1.5]
    [4.9 1.5]]
   shape: (6, 2)

   mystery flower: [3. 1.]

   distance to each of the six: [1.79 1.79 1.88 1.75 1.58 1.96]

     setosa      distance 1.79
     setosa      distance 1.79
     setosa      distance 1.88
     versicolor  distance 1.75
     versicolor  distance 1.58  <- closest
     versicolor  distance 1.96
   ```

   Then the question that sets up next week: **"The closest one is a versicolor. But look at the whole list — how confident are you?"** *(Not very. 1.58, 1.75, 1.79, 1.79 — the top four are almost tied and they are not all the same species. Next week's model asks several of them to vote instead of trusting the single closest, and this is exactly why.)*

4. **Break the line-up on purpose** (item 3), then write the one-sentence explanation of why Python said nothing.
5. **Design the leak.** "Invent a column for the playlist table that would score perfectly and be useless. Make it subtle enough that I might not notice." Good answers: `times_i_skipped_it`, `which_workout_playlist_it_is_on`, `the_filename`.

### If the student won't engage today

Do the Hook and the graph paper, and stop.

The Week 1 sheet is a genuinely good moment even on a bad day — it costs nothing and it is about them rather than about Python. Then go straight to the graph paper and make it a game rather than a lesson: **"Guess The Distance."** You name two points, they eyeball the distance, then you both measure with the ruler. Best of ten. Keep score.

> (0,0) and (3,4) → 5 · (1,1) and (4,5) → 5 · (0,0) and (5,0) → 5 · (2,3) and (2,8) → 5 · (0,0) and (1,1) → 1.41 · (0,0) and (2,2) → 2.83 · (1,2) and (4,6) → 5 · (0,5) and (5,0) → 7.07 · (3,3) and (6,7) → 5 · (0,0) and (6,8) → 10

Four of those are 5, which is a nice trap and provokes the right question. That game delivers objectives 4 and 5 completely and takes twelve minutes. The code survives to next lesson perfectly well; Week 29 opens with a recap anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the split (spoken, with a table in front of them)**

> "Here's a table: five columns — pupil name, hours of sleep, minutes of exercise, screen time, and then whether they felt tired the next day. Tell me `X`, tell me `y`, and tell me what happens to the leftover column."

*Good answer:* `X` = sleep, exercise, screen time. `y` = tired-or-not. The name goes in neither, because a name only ever appears once. **What to catch:** putting `tired` into `X` (they have not separated the question from the evidence), or putting `name` into `X` (they have not internalised the leak). Full marks needs all three parts.

**Check 2 — the shapes (spoken)**

> "That table has forty rows. What's the shape of `X`? What's the shape of `y`?"

*Good answer:* `X` is `(40, 3)`. `y` is `(40,)`. **What to catch:** `(3, 40)` — they have reversed rows and columns; go back to the SHAPES sheet and read the phrase off it. Also catch `(40, 1)` for `y`, which is close and worth a nudge: "that's a skinny table; we want a single line."

**Check 3 — the distance (written, 90 seconds)**

> "Two points. Point one is at (2, 1). Point two is at (5, 5). Write me all four steps and the answer."

*Good answer:*

```
step 1   2 − 5 = −3        1 − 5 = −4
step 2   (−3)² = 9         (−4)² = 16
step 3   9 + 16 = 25
step 4   √25 = 5
```

Full marks needs all four lines written down, not just the 5. **What to catch:** an answer of 7 (they added the gaps instead of the squares) — draw the triangle and ask which is longer, the two straight sides or the slanted one. Also catch a negative answer at step 2.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say which column is `y`. Puts the answer column inside `X`. Cannot state a shape at all. |
| **2 — Emerging** | Splits the table correctly when prompted. Reads shapes but reverses rows and columns. Does the distance with the four steps written out for them. |
| **3 — Secure** | Splits a fresh table into `X` and `y` unaided, states both shapes correctly and in the right order, uses two brackets for `X` without being told, and computes a distance by hand in four steps that matches numpy to 2 dp. **This is the target.** |
| **4 — Strong** | Explains *why* two brackets give a table (a list of names goes in, a table comes out). Explains why a name column is excluded, using Level 1's leak language. Predicts, before computing, that adding a column can only make a distance bigger. |
| **5 — Exceptional** | Notices unprompted that `bpm` in the hundreds will swamp `minutes` under six, and can say *why* using the squares. Sees that a distance is only meaningful relative to other distances in the same table. Spots that two flowers can sit at distance 0.00 and still be two different flowers. |

---

## 📤 Homework to Assign

**Say this:**

> "Two things, about an hour altogether, and the second one is the one that matters.
>
> **First, pages 28.5 and 28.6 — build `X` and `y` from your own table.** Use the table you have been carrying since Week 21. Write down `X.shape` and `y.shape` in ink, and next to each one write, in words, what the numbers mean: 'ten rows, meaning ten songs' — not just the digits. If your own table has gone walkabout, page 28.5 has the ten-song playlist printed on it and you can use that.
>
> **Second, one distance, twice, and they must match.** Pick any two rows of your table. Compute the distance between them **on paper**, all four steps, each on its own line — subtract, square, add, root. Then compute the same distance in numpy. Then write both numbers next to each other, rounded to two decimal places, and they had better be the same.
>
> And one thing I want you to notice while you do it, and write one sentence about: **look at which column made the biggest contribution at step 2.** Not step 4. Step 2, where the squares are. One of your columns is going to be doing nearly all the work, and I want you to notice which and say how much. That sentence is worth more marks than the distance is."

**Workbook pages:** 28.1, 28.2, 28.3 and 28.4 in class; **28.5 and 28.6** at home.

**Expected time:** 20 min for `X` and `y` and the shapes · 25 min for the distance done twice · 15 min for page 28.6. About 60 minutes.

---

## 🔑 Answer Key

Every code block below was run before it was pasted here, and the outputs are real.

### Page 28.1 — Which column is which?

| # | The table | `X` | `y` | Column excluded, and why |
|---|---|---|---|---|
| (a) | song, bpm, minutes, **mood** | bpm, minutes | mood | `song` — a name appears in exactly one row, so there is nothing in it that transfers to a new song. |
| (b) | flower id, petal length, petal width, sepal length, sepal width, **species** | the four measurements | species | `flower id` — a row number. It carries no information about the plant at all. |
| (c) | pupil name, hours slept, minutes of exercise, screen time hours, **felt tired** | hours slept, minutes of exercise, screen time hours | felt tired | `pupil name` — unique per row. |
| (d) | date, temperature at 9am, cloud cover, wind speed, **rained today** | temperature, cloud cover, wind speed | rained today | `date` — every date appears once. *(Worth a note if a student argues: you could turn a date into `month` or `day_of_week`, which do repeat, and those are perfectly good features. The raw date is not.)* |
| (e) | shop, price, distance in km, rating out of 5, **would order again** | price, distance, rating | would order again | `shop` — a name. *(A student who says "but the same shop could appear twice" has made a genuinely good point. If shops repeat, the column carries something. Credit it, and note the honest reply: the moment a new shop appears you are stuck again.)* |

**28.1(f) In (a), what would happen if you put `mood` inside `X` as well?**
The model would score 100% and be worthless. `mood` *is* the answer, so you would be handing over the answer and then asking for it back. Level 1 called this a **leak**. The test is unchanged: at the moment you need the prediction, do you have this value? For a brand-new song you do not — that is the whole reason you wanted a prediction.

**28.1(g) Why is a row number never a feature?**
Because it describes where the row happens to sit in your file, not the thing the row is about. Sort the file differently and every row number changes while nothing about any song changes. A feature has to be a property of the thing.

### Page 28.2 — Shapes

| # | Table | `X.shape` | `y.shape` |
|---|---|---|---|
| (a) | 10 songs, 2 measurements | `(10, 2)` | `(10,)` |
| (b) | 150 flowers, 4 measurements | `(150, 4)` | `(150,)` |
| (c) | 40 pupils, 3 measurements | `(40, 3)` | `(40,)` |
| (d) | 178 wines, 13 measurements | `(178, 13)` | `(178,)` |
| (e) | 6 fruits, 2 measurements | `(6, 2)` | `(6,)` |
| (f) | 1 new flower you want a guess for, 4 measurements | `(1, 4)` | — there is no `y`; that is the whole point |

**28.2(g) What does the comma in `(10,)` mean?**
It means "there is no second number". It marks the shape as a single line of ten values rather than a table. Without it, `(10)` would just be the number ten in brackets. Compare `(10, 1)`, which means ten rows of one column each — a skinny table, not a line.

**28.2(h) You add a fourth measurement to a 40-row table. What changes?**
`X.shape` becomes `(40, 4)`. `y.shape` stays `(40,)`. Adding a column never adds an answer.

**28.2(i) You delete five rows from the table. What changes?**
Both. `X.shape` becomes `(35, 3)` and `y.shape` becomes `(35,)`. **They must always change together** — and the reason to delete rows from the whole table, before pulling `X` and `y` out, is that then it is impossible to get this wrong.

### Page 28.3 — Twelve iris rows, on paper

The twelve printed rows (real rows from `load_iris`, petal columns only):

| row | petal length | petal width | species |
|---|---|---|---|
| 0 | 1.4 | 0.2 | setosa |
| 1 | 1.4 | 0.2 | setosa |
| 2 | 1.3 | 0.2 | setosa |
| 3 | 1.5 | 0.2 | setosa |
| 50 | 4.7 | 1.4 | versicolor |
| 51 | 4.5 | 1.5 | versicolor |
| 52 | 4.9 | 1.5 | versicolor |
| 65 | 4.4 | 1.4 | versicolor |
| 100 | 6.0 | 2.5 | virginica |
| 101 | 5.1 | 1.9 | virginica |
| 102 | 5.9 | 2.1 | virginica |
| 103 | 5.6 | 1.8 | virginica |

**28.3(a) `X.shape` and `y.shape` for this printed table.**
`X.shape` is `(12, 2)`. `y.shape` is `(12,)`.

**28.3(b) Which two species overlap, just by looking?**
Versicolor (4.4–4.9 long) and virginica (5.1–6.0 long) sit next to each other and nearly touch. Setosa (1.3–1.5) is miles away from both. **Prediction worth writing down now:** any model will find setosa easy and confuse the other two. It will turn out to be exactly right, in Week 30.

**28.3(c) Distance between row 0 and row 3.**

```
step 1   1.4 − 1.5 = −0.1        0.2 − 0.2 = 0.0
step 2   (−0.1)² = 0.01          0.0² = 0.00
step 3   0.01 + 0.00 = 0.01
step 4   √0.01 = 0.1
```

**0.10.** Two setosas, almost the same point.

**28.3(d) Distance between row 50 and row 100.**

```
step 1   4.7 − 6.0 = −1.3        1.4 − 2.5 = −1.1
step 2   (−1.3)² = 1.69          (−1.1)² = 1.21
step 3   1.69 + 1.21 = 2.90
step 4   √2.90 = 1.7029...  = 1.70
```

**1.70.**

**28.3(e) Distance between row 0 and row 100.**

```
step 1   1.4 − 6.0 = −4.6        0.2 − 2.5 = −2.3
step 2   (−4.6)² = 21.16         (−2.3)² = 5.29
step 3   21.16 + 5.29 = 26.45
step 4   √26.45 = 5.1430...  = 5.14
```

**5.14.**

**28.3(f) Put those three distances in order and say what the order tells you.**
0.10 < 1.70 < 5.14. Two setosas are almost on top of each other; a versicolor and a virginica are moderately apart; a setosa and a virginica are far apart. **Distance is behaving like similarity** — and that is the entire idea next week's model runs on.

Confirmed in code:

```python
# check_page_283.py
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()

for i, j in [(0, 3), (50, 100), (0, 100)]:
    a = iris.data[i, 2:4]                 # petal length and width of row i
    b = iris.data[j, 2:4]
    gaps = a - b
    print(f"rows {i:3d} and {j:3d}:  gaps {gaps}  squares {gaps ** 2}"
          f"  total {round((gaps ** 2).sum(), 4)}"
          f"  distance {round(float(np.sqrt(((a - b) ** 2).sum())), 2)}")
```

```text
rows   0 and   3:  gaps [-0.1  0. ]  squares [0.01 0.  ]  total 0.01  distance 0.1
rows  50 and 100:  gaps [-1.3 -1.1]  squares [1.69 1.21]  total 2.9  distance 1.7
rows   0 and 100:  gaps [-4.6 -2.3]  squares [21.16  5.29]  total 26.45  distance 5.14
```

### Page 28.4 — The graph paper page

**28.4(a) The plot.** Axes labelled `petal length (cm)` 0–6 across and `petal width (cm)` 0–2 up. Scale written on the sheet. Flower A `(1.4, 0.2)` as a circle, flower B `(4.4, 1.4)` as a triangle, joined, with the right-angled triangle completed.

**28.4(b) Ruler measurement.** About **6.5 cm of paper**, which at 2 cm of paper per unit is **≈ 3.25**. Anything from 3.1 to 3.4 is a correct measurement. Mark the honesty of writing it down before doing the arithmetic, not the accuracy.

**28.4(c) The four steps.** `−3.0` and `−1.2` → `9.00` and `1.44` → `10.44` → **`3.23`**.

**28.4(d) Why doesn't the ruler give exactly 3.23?**
Because a ruler and a pencil are physical objects. The pencil line has width, the point is a blob a millimetre across, and reading a ruler to better than half a millimetre is not possible by eye. The arithmetic has none of those problems. **The right conclusion is not "the ruler is wrong" — it is that measurements carry uncertainty and calculations do not.**

**28.4(e) Which step throws away the minus signs, and why is that fine?**
Step 2, squaring. It is fine because a gap of −3 and a gap of +3 are the same size of gap — all we want to know is *how far apart*, not which one was bigger. And it is more than fine, it is necessary: without squaring, a gap of +3 in one column and −3 in another would cancel out and two very different rows would come out at distance 0.

### Page 28.5 — `X` and `y` from your own table

Mark the structure, not the choice of table. Model answer using the ten-song playlist:

```python
# my_x_and_y.py
# Build X and y from my own table, and state both shapes.

import pandas as pd

playlist = pd.DataFrame({
    "song":    ["Monsoon", "Rocket", "Lantern", "Corridor", "Firecracker",
                "Slow Bus", "Neon", "Paper Boat", "Stadium", "Rooftop"],
    "bpm":     [68, 148, 80, 160, 152, 72, 168, 76, 140, 84],
    "minutes": [4.2, 3.1, 3.8, 2.8, 3.4, 5.1, 2.6, 4.6, 3.0, 5.4],
    "mood":    ["chill", "hype", "chill", "hype", "hype",
                "chill", "hype", "chill", "hype", "chill"],
})

X = playlist[["bpm", "minutes"]]        # two brackets, so a table comes back
y = playlist["mood"]                    # one bracket, so a column comes back

print("X.shape:", X.shape, "-> 10 songs, 2 measurements each")
print("y.shape:", y.shape, "-> 10 answers, in one line")
print()
print(X.head(3))
print()
print(y.head(3))
```

```text
X.shape: (10, 2) -> 10 songs, 2 measurements each
y.shape: (10,) -> 10 answers, in one line

   bpm  minutes
0   68      4.2
1  148      3.1
2   80      3.8

0    chill
1     hype
2    chill
Name: mood, dtype: object
```

**28.5(a) In words, what does each number in `X.shape` mean?**
The 10 is how many songs there are — one row per song. The 2 is how many things were measured about each song. Rows first, columns second.

**28.5(b) Which column did you leave out of both `X` and `y`, and why?**
`song`. Every song name appears in exactly one row, so a model could only memorise it, and memorising a name tells you nothing about a song you have not heard.

**28.5(c) What would you have to change to add a third measurement?**
Add the column to the DataFrame, then add its name to the list inside the inner brackets: `playlist[["bpm", "minutes", "loudness"]]`. `X.shape` becomes `(10, 3)`. `y` does not change.

### Page 28.6 — One distance, twice

Model answer, Monsoon against Lantern (both chill songs):

**On paper:**

```
Monsoon = (68, 4.2)        Lantern = (80, 3.8)

step 1   subtract      68 − 80 = −12          4.2 − 3.8 = 0.4
step 2   square        (−12)² = 144           0.4² = 0.16
step 3   add up        144 + 0.16 = 144.16
step 4   square root   √144.16 = 12.0066...   = 12.01
```

**In numpy:**

```python
# one_distance_twice.py
# The distance between two songs, on paper and in numpy.

import numpy as np

monsoon = np.array([68.0, 4.2])          # bpm, minutes
lantern = np.array([80.0, 3.8])

gaps = monsoon - lantern
squares = gaps ** 2
total = squares.sum()
distance = np.sqrt(total)

print("gaps    :", gaps)
print("squares :", squares)
print("total   :", total)
print("distance:", distance)
print("2 dp    :", round(distance, 2))
```

```text
gaps    : [-12.    0.4]
squares : [144.     0.16]
total   : 144.16
distance: 12.006664815842907
2 dp    : 12.01
```

**Paper: 12.01. numpy: 12.01. They match.** ✅

**28.6(a) Which column contributed most at step 2, and by how much?**
`bpm`, overwhelmingly. It contributed 144 out of 144.16 — that is **99.89%** of the total. `minutes` contributed 0.16, or **0.11%**.

**28.6(b) Write one sentence about what that means.**
Full-credit answer, in the student's own words, containing this idea:

> Nearly all of the distance came from the beats per minute, so if I used this distance to decide which songs are similar I would basically be sorting by bpm and ignoring the length completely — not because length does not matter, but because bpm happens to be measured in bigger numbers.

**28.6(c) What would happen if you measured length in *seconds* instead of minutes?**
The lengths become 252 and 228 instead of 4.2 and 3.8, so the gap becomes 24 instead of 0.4, and squared, 576 instead of 0.16. Now **length** contributes 576 of 720, which is 80%, and bpm contributes 20%. **Nothing about the songs changed. Only the units changed, and the answer flipped.** That is Week 30 in one sentence, and a student who gets here has arrived early.

Confirmed:

```python
# units_flip.py
import numpy as np

# Same two songs, length measured in minutes, then in seconds.
for unit, a, b in [("minutes", np.array([68.0, 4.2]), np.array([80.0, 3.8])),
                   ("seconds", np.array([68.0, 252.0]), np.array([80.0, 228.0]))]:
    squares = (a - b) ** 2
    total = squares.sum()
    print(f"length in {unit}:")
    print(f"   bpm share    : {100 * squares[0] / total:.2f} %")
    print(f"   length share : {100 * squares[1] / total:.2f} %")
    print(f"   distance     : {np.sqrt(total):.2f}")
```

```text
length in minutes:
   bpm share    : 99.89 %
   length share : 0.11 %
   distance     : 12.01
length in seconds:
   bpm share    : 20.00 %
   length share : 80.00 %
   distance     : 26.83
```

### Lesson questions posed in the Say-this scripts

- *"Fruit bowl: what's `X` and `y`?"* → `X` = colour, mass, length. `y` = the fruit name.
- *"Age and practice hours predicting a club: `X`? `y`?"* → `X` = age, hours. `y` = club.
- *"Why two letters instead of proper names?"* → Because it is the same two objects in every single problem, so the world agreed on two symbols. The only single-letter names allowed in this course.
- *"What happens to the `song` column?"* → Neither `X` nor `y`. A name appears in one row only, so there is nothing in it that transfers.
- *"`(10, 2)` — what's the 10 and what's the 2?"* → 10 songs, 2 measurements. Rows, then columns.
- *"What's the shape of `y`?"* → `(10,)` — ten comma nothing. A single line, not a skinny table.
- *"Add a third measurement — what changes?"* → `X.shape` becomes `(10, 3)`; `y` unchanged.
- *"How many brackets for a table, how many for a column?"* → Two, and one.
- *"The traceback was fifteen lines. Which line mattered?"* → The last one, plus the one naming your own file.
- *"`KeyError: ('bpm', 'minutes')` — what did pandas think you wanted?"* → A single column whose name was that whole pair.
- *"iris `X` is `(150, 4)` — how many flowers?"* → 150 flowers, 4 measurements each.
- *"Where's the file the iris data came from?"* → There is no file. It ships inside the library.
- *"Is √10.44 going to be bigger or smaller than 10.44?"* → Smaller. Square roots of numbers above 1 always come down.
- *"Why doesn't the ruler give exactly 3.23?"* → Pencil lines have width and eyes read rulers to about half a millimetre. Measurements carry uncertainty; arithmetic does not.
- *"Six flowers, closest is versicolor — how confident are you?"* → Not very: 1.58, 1.75, 1.79, 1.79 are nearly tied and not all the same species. Which is exactly why next week's model asks several neighbours to vote.

---

## 🔮 Next Week Preview

Week 29 is the one the whole level has been walking towards: **the student trains a model.** It takes three lines. You make a `KNeighborsClassifier`, you call `.fit()` on it with the `X` and `y` you built this week, and you call `.predict()` — and something that has never seen a flower before names one correctly. The idea underneath is the one they already used in the canteen on their first day at a new school: look at the handful of examples nearest to the new one and go with the majority. That is genuinely the entire algorithm, and it is a real one that real systems run on today. The second half of the week is the discipline that makes the first half mean anything: **hide 20% of your rows before you start, and never let the model see them until the very end.** Level 1 did this with a sealed envelope; next week the envelope comes back, the student signs across the flap, and then does the same cut in one line of code.

**Prep early:** three things. **One — a real deck of playing cards and an envelope** the student can sign across the flap; the physical version of the split is the moment the lesson lands, and a photocopied paper deck does not have the same weight. **Two — keep this week's `x_and_y.py` and `iris_shapes.py` files;** Week 29 opens by adding to them rather than starting fresh, and re-typing the DataFrame eats eight minutes. **Three — keep the SHAPES sheet on the wall.** From next week there are four shapes on it instead of two — `X_train`, `X_test`, `y_train`, `y_test` — and the fact that the row counts have to add up is how the student will catch their own mistakes for the rest of the year.

---

[⬅ Week 27](week-27.md) · [Course Home](../README.md) · [Week 29 ➡](week-29.md) · [Student Guide](../student-guide/week-28.md) · [Workbook](../workbook/week-28.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
