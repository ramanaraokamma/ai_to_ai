# Week 19 — Down the Columns or Across the Rows?

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Student Guide](../student-guide/week-19.md) · [Workbook](../workbook/week-19.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one keyword, two directions, and the habit that catches a wrong answer |
| **Big idea** | `axis=0` walks **down** a column and `axis=1` walks **across** a row — and picking the wrong one gives you a confident wrong answer. |
| **New vocabulary** | axis · row · column · 2-D indexing · hand-check |
| **New syntax** | `arr[1, 2]` · `arr[:, 0]` · `arr.mean(axis=0)` · `arr.sum(axis=1)` |
| **Materials** | **Graph paper** (or a printed grid) · a pencil · **a calculator** — this is not optional today · printed workbook pages 19.1–19.6 · the Bug Log · a highlighter if you have one |
| **Tech needed** | Laptop with Python 3 and numpy working. Nothing new to install. `rainfall.py` is typed from scratch, so no earlier file is needed. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |

> **⚠️ Watch out:** the second deliberate mistake in this lesson **does not crash.** It runs, it prints a tidy row of numbers, and it answers a completely different question from the one asked. Do not warn the student. They must catch it by **counting the answers** — six months should give six numbers — and if you tip them off, the habit never gets tested. This is the whole point of the week.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Index one cell of a 2-D array** with one pair of brackets and one comma: `rain[1, 2]`.
2. **Take a whole column or a whole row** using a colon: `rain[:, 0]` and `rain[1, :]`.
3. **Compute one mean per column with `axis=0`** and say, *before running it*, how many answers to expect.
4. **Compute one total per row with `axis=1`** and check the count of answers against the number of labels.
5. **Hand-check one row on paper** before trusting any array result — and say what they will do if the pencil and the code disagree.

Observable evidence: `rainfall.py`, which prints the shape, one cell, one whole row, one whole column, a per-month mean and a per-city mean, with the count of answers printed beside each; a workbook page with row 1 and column 1 worked out in pencil *before* the code ran; and one written sentence explaining how the count of answers tells you which axis you used.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to know any numpy to teach this.** There is exactly one new idea today and it is a direction. Read this section once — it takes about fifteen minutes — and you will be ahead of the student for the whole lesson.

### 1. What the problem actually is

Last week the student learned that an array can do arithmetic to all of its numbers at once. `scores * 2` doubles everything. `runs + balls` adds two arrays pair by pair. In every one of those cases numpy treated the whole block of numbers as **one heap** and did the same thing to every number in it.

That is fine right up until your block of numbers is a **table**. And a table is the whole point of data.

Here is the table this lesson uses. Four cities down the side, six months across the top, rainfall in millimetres:

```text
             Jan   Feb   Mar   Apr   May   Jun
Chennai       25    10     5    15    40    55
Pune           2     4    10    20    36    90
Shimla        65    70    60    45    51   105
Kochi         22    26    54   120   300   480
```

Now ask an obvious question: **what is the average rainfall?**

That question has no single answer, and that is not a trick. It has *three* answers:

| The question you meant | The answer | How many numbers |
|---|---|---|
| average over the whole table | 71.25 | **1** |
| average **per city** — how wet is each city? | 25, 27, 66, 167 | **4** |
| average **per month** — how wet is each month? | 28.5, 27.5, 32.25, 50, 106.75, 182.5 | **6** |

All three are correct averages of that table. Only one of them answers the question you had in your head. **Choosing which one is what `axis` is for.**

### 2. `axis` — the one new word, and the one sentence that makes it stick

> **axis** — a direction through an array. `axis=0` runs **down** the rows. `axis=1` runs **across** the columns.

The numbering comes straight from last week's `.shape`. `rain.shape` is `(4, 6)`. The **first** number in the shape — the 4, the rows — is **axis 0**. The **second** number — the 6, the columns — is **axis 1**. That is the whole rule, and it is worth saying out loud: *the axis number is just the position in the shape.*

Now, the sentence. There are three popular ways to explain `axis` and two of them will fail your student. Here is the one that works:

> **The axis you name is the axis that gets eaten.**

Say it exactly like that, every single time, all lesson. Then unpack it:

- `rain.mean(axis=0)` — you named **axis 0**, the rows. So the **rows get eaten.** Four rows go in; the "four" disappears. What is left is the six columns, so you get **six numbers, one per column, one per month.**
- `rain.mean(axis=1)` — you named **axis 1**, the columns. So the **columns get eaten.** Six columns go in; the "six" disappears. What is left is the four rows, so you get **four numbers, one per row, one per city.**

![Six pink arrows point down out of the grid into one row of six month averages](../figures/fig-w19-1-axis0-collapses-rows.svg)
*Figure 19.1 — `axis=0` eats the rows. Four rows go in, and six answers come out — one for each month.*

![Four pink arrows point right out of the grid into one column of four city averages](../figures/fig-w19-2-axis1-collapses-columns.svg)
*Figure 19.2 — `axis=1` eats the columns. Six columns go in, and four answers come out — one for each city.*

**Why "the axis you name gets eaten" and not "axis 0 means columns"?** Because the second one is a fact with no reason behind it, so a 12-year-old will remember it for eleven minutes. "The axis you name gets eaten" is a rule you can *re-derive* in the moment, and it also tells you the answer's shape, which is the thing that catches mistakes. Insist on the eating.

**The two explanations to avoid, and why:**

| Tempting explanation | Why it backfires |
|---|---|
| *"axis=0 means down, so it gives you column answers."* | It is true, and it contains a swap — "down" produces "column" — which is exactly the swap the student is already confused about. You have added a step, not removed one. |
| *"axis=0 is vertical, axis=1 is horizontal."* | Fine for a 2-D table and useless the moment there is a third direction, which there will be in Level 3. It also gives no clue about how many answers come out. |

### 3. The count of answers is the tell, and you should treat it as a rule

This is the single most valuable habit in the lesson, and it is not really about numpy at all.

**Before you run any line with an axis in it, say how many answers you expect. Then count them.**

- Four cities. Asked for one answer per city? **Expect four numbers.** Got six? Wrong axis.
- Six months. Asked for one answer per month? **Expect six numbers.** Got four? Wrong axis.

That is it. And notice what it costs: nothing. You already know how many cities you have, because you typed the labels.

The reason this matters so much is the thing in the next section: the wrong axis does not crash.

### 4. The wrong axis is a *silent* mistake — and this is the point of the week

Suppose the student wants the average rainfall in **January**. January is a column. Columns are what survive when you eat the rows, so this is `axis=0`. But they type `axis=1`:

```python
print(rain.mean(axis=1))
```

```text
[ 25.  27.  66. 167.]
```

Nothing crashed. Four beautifully formatted decimal numbers. The first one is `25.0` and the student writes down *"January: 25.0 mm"*.

The real answer for January is **28.5**.

`25.0` is not a random wrong number. It is Chennai's average across all six months, which is a perfectly good number that answers a question nobody asked. And 25.0 is *plausible* — it is in the right range, it looks like rainfall, there is nothing about it that says "I am wrong".

![Two panels: axis=1 gives four answers with a red cross, axis=0 gives six with a green tick](../figures/fig-w19-4-wrong-axis-confident-answer.svg)
*Figure 19.4 — Both lines ran. Both printed. Only one of them answered the question that was asked.*

**Say the general version of this to the student, because it is one of the most important ideas in the whole course:**

> "Most mistakes you have made so far were **loud**. Python stopped, printed a traceback, and told you where. This one is **quiet**. It gives you a number, and the number is wrong, and nobody tells you. From here on, most of the mistakes are going to be this kind — and the only defence is a check you run on purpose."

Two checks defend against it, and both are cheap:

1. **Count the answers.** Six months, six numbers.
2. **Hand-check one of them.** One row, one calculator, thirty seconds.

### 5. Two-number indexing: one pair of brackets, one comma

> **2-D indexing** — naming one cell of a block with two numbers: the row first, then the column, in one pair of square brackets, separated by a comma.

```python
print(rain[1, 2])
```

```text
10
```

Read `rain[1, 2]` out loud as **"row one, column two"**, and read it in that order always. Row first. It is the same order as `.shape` — rows first, then columns — and it is the same order as reading a page: along a row, then down to the next one.

**The thing that catches everybody, and it is not really about numpy.** In English, "row 1" means the first row. In Python, `rain[1]` is the **second** row, because counting starts at 0. So `rain[1, 2]` is *Pune in March*, not *Chennai in February*.

This is Week 11's lesson (`scores[0]` is the first score) arriving in two directions at once, so it hurts twice as much. **Do not fight it with a rule. Fight it with a habit:** whenever you write an index, point at the cell on the paper grid at the same time. Every time, all lesson.

> **🧑‍🏫 If a student asks:** *"Can I write `rain[1][2]` instead?"* Yes, and it gives the same answer — `10`. It works because `rain[1]` hands you the whole row as an array, and then `[2]` picks out of that. But it makes two arrays instead of one number, and it will not let you write the colon trick in the next section. **Teach one form: `rain[1, 2]`.** Mention that the other one works if they ask, and then go back to the comma.

### 6. The colon: "everything in this direction"

This is the second half of today's indexing, and it is genuinely elegant.

> A **colon** in an index position means *"every one of these"*.

```python
print(rain[1, :])      # row 1, EVERY column  -> all of Pune's months
print(rain[:, 0])      # EVERY row, column 0  -> January for all four cities
```

```text
[ 2  4 10 20 36 90]
[25  2 65 22]
```

![Two panels showing a tinted column and a tinted row, each collapsing into a strip](../figures/fig-w19-3-colon-takes-the-whole-column.svg)
*Figure 19.3 — One number picks one. A colon takes every one in that direction.*

**Three things to be ready for.**

**(a) `rain[1]` and `rain[1, :]` are the same thing.** If you leave the second position off entirely, numpy assumes you meant "all of them". So `rain[1]` gives Pune's whole row too. Both are fine. **Prefer `rain[1, :]` while learning**, because the colon is *visible*, so the student can see that a decision was made about the second direction. An invisible decision is a decision you forget you made.

**(b) There is no short form for a column.** You cannot write `rain[, 0]`. Try it and Python refuses before it even runs the file:

```text
  File "rainfall.py", line 20
    print(rain[, 0])
               ^
SyntaxError: invalid syntax
```

The colon is compulsory in the row position. Which is a small piece of luck, because a column is the harder one to picture and it is good that it takes a deliberate keystroke.

**(c) A column prints as a row, and this confuses people.** `rain[:, 0]` gives `[25  2 65 22]` printed left to right, even though you took a column. Its shape is `(4,)` — four numbers, one direction. **numpy does not remember that they used to be standing up.** Say so once, plainly:

> "You took a column and it printed as a row. That's not a bug. A column of four numbers and a row of four numbers are the same four numbers — being upright isn't something the array keeps."

### 7. `.sum(axis=...)` works exactly the same way, and totals are your friend

Everything above is true of `.sum` as well:

```python
print(rain.sum(axis=1))     # one total per city   -> 4 numbers
print(rain.sum(axis=0))     # one total per month  -> 6 numbers
```

```text
[ 150  162  396 1002]
[114 110 129 200 427 730]
```

And now the nicest check in the whole lesson, which you should absolutely use:

```python
print(rain.sum(axis=1).sum())   # add up the four city totals
print(rain.sum(axis=0).sum())   # add up the six month totals
print(rain.sum())               # add up the whole grid
```

```text
1710
1710
1710
```

**Three different routes to the same number.** Add the grid up in rows, add it up in columns, or add it all up at once — all three always agree, because they are the same numbers added in different orders. **Be clear about what that means:** in numpy the three totals can never disagree, so this line cannot catch a wrong axis or a mistyped number (a wrong `axis` still gives three matching totals; a ragged row is refused when the array is built). It is a check on *understanding*, and on **hand-added** margins, where your own arithmetic can slip.

Call this the **corner check**, because on paper it lands in the bottom-right corner where the margin row meets the margin column. Accountants have cross-footed tables like this for centuries. On paper it catches real arithmetic slips; in code it is free but always agrees.

### 8. The hand-check, and why it is a graded part of the week

> **hand-check** — working out one of the answers yourself, on paper, with a calculator, *before* you look at what the code said.

The order matters enormously and it is the whole design of the lesson:

1. Pencil first. Write the answer down where you cannot quietly change it.
2. Then run the code.
3. Then compare.

If you run the code first, you are not checking anything — you are confirming. A number on the screen is extremely persuasive, and a 12-year-old (and, honestly, a 45-year-old) who has already seen `25.0` will do arithmetic that arrives at 25.0.

Today's hand-check, worked out in full so you have it ready:

**Row 1 — Pune.** Row 1 is the *second* row, because rows are numbered from 0.

```text
2 + 4 + 10 + 20 + 36 + 90 = 162
162 / 6 = 27.0
```

Six months, so divide by six. The code must say `27.` in the second slot of `rain.mean(axis=1)`.

**Column 1 — February.** Column 1 is the *second* column, for the same reason.

```text
10 + 4 + 70 + 26 = 110
110 / 4 = 27.5
```

Four cities, so divide by four. The code must say `27.5` in the second slot of `rain.mean(axis=0)`.

![Row 1 pulled out, added up by hand to 162, divided by 6 to give 27.0, matching a terminal panel](../figures/fig-w19-6-hand-check-row-one.svg)
*Figure 19.6 — Pencil first. Then the code. Then compare.*

**Notice what I chose on purpose:** 27.0 and 27.5. The row answer and the column answer are almost the same number. That is deliberate and you should not mention it. It means a student who does one hand-check sloppily, or who mixes up which is which, gets a *near miss* rather than an obvious miss — which is exactly what happens in real data work, and exactly why counting the answers matters more than eyeballing them.

**And the sentence to say when the pencil and the code disagree:**

> "The code is not automatically right. The pencil is not automatically right. **Something is wrong and you now have to find out which one**, and that is not a bad afternoon — that is the job."

### 9. The three misconceptions you will actually meet

**Misconception 1 — "axis=0 means the answer is about rows."**
This is the big one and it is completely natural. `axis=0` *is* the rows — and naming them is how you **get rid of** them. The answer is about whatever is left over. Cure: never say "axis 0 means rows" as a standalone sentence. Always say the whole thing: *"axis 0 names the rows, so the rows get eaten, so the answers are one per column."* Make them say the whole sentence too.

**Misconception 2 — "row 1 is the first row."**
In English it is. In Python it is not. This will produce off-by-one errors all lesson and the fix is not a rule, it is pointing. Every time an index is written, someone's finger goes on the paper grid. If a student writes `rain[1, 2]` and points at Chennai/February, that is the moment to catch it, not later.

**Misconception 3 — "if it printed numbers, it worked."**
Two weeks of `TypeError` and `IndexError` have trained the student that a run without a traceback is a run that succeeded. This week breaks that, on purpose. Cure: the count. A run that produced the wrong *number of answers* did not succeed, no matter how neat the output looked.

### 10. How deep to go, and where to stop

**Go this far:** `arr[row, col]` for one cell; `arr[r, :]` and `arr[:, c]` for a whole row and a whole column; `.mean(axis=0)` and `.mean(axis=1)`; `.sum(axis=0)` and `.sum(axis=1)`; the count-the-answers check; the corner check; one hand-checked row and one hand-checked column; and the sentence *"the axis you name gets eaten."*

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `arr > 50`, masks, `arr[mask]` | **Week 20.** Very tempting once the grid is on screen. Don't — today the student has one new idea and it is a direction. |
| `.min()`, `.max()`, `np.round()` | **Week 20.** `.sum` and `.mean` are enough to make the axis point twice. |
| `argmin` / `argmax` — "which test was hardest" | **Not in this course as syntax.** Next week the student finds the hardest test with a mask, which reuses what they already have. Do not introduce a second new idea to answer a question a mask answers. |
| Slices with two numbers: `arr[1:3, 2:]` | **Not this term.** The colon on its own is today's idea. A colon with numbers around it is a second idea wearing the same clothes, and it will blur the first. |
| `.reshape()`, `keepdims=True` | Not this term. When the shape is wrong today, the fix is to look at the brackets or the axis. |
| A third axis / 3-D arrays | Level 3. If asked: "yes, there are more directions, and the rule doesn't change — the axis you name still gets eaten." |
| `axis=-1` | Mention only if a student meets it online. It means "the last direction", which for a table is `axis=1`. Do not build on it. |
| `.std()`, `.var()` | Not needed. `mean` and `sum` carry the whole lesson. |

The line to hold in your head all lesson: **today is the week the student learns to say how many answers they expect before they press run.** That is the deliverable. The syntax is four characters.

---

### 11. 🧭 The Growing Map — two minutes on a box that finally moved

The student guide carries one figure that is not about this week's content: the same pipeline every
week, with one more piece filled in. This is the first week since Week 13 that the gold has actually
moved, and it has moved into a new stage — so today the map is worth slightly more than usual.

![The Level 2 pipeline in Week 19: stage three opens and its numpy and DataFrames tile is this week's box](../figures/fig-w19-0-where-this-fits.svg)

*Figure 19.0 — Week 19's version. Stage three, clean it, goes solid for the first time, and its first
tile — `numpy · DataFrames`, weeks 19 to 22 — is this week's box. One thread lit: representation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and read the gold tile's two words aloud.** Ask *"which of those two are we living in
   today, and which one is still two weeks off?"* You want a finger on **numpy**, and **DataFrames**
   named as Week 21. Then the today question: *"and what is the new word inside numpy this week?"* —
   **axis**, with one hand going down and one going across as they say it.
2. **Then the better question:** *"the wrong axis did not crash. Which box on this map would have caught
   it?"* The answer is **none of them** — what caught it today was a pencil, a calculator and counting
   the answers. Sit in that for a moment. It is the argument for the hand-check, and it is far more
   convincing coming from the picture than from you.
3. **Have them update their own copy:** `axis=0 ↓` and `axis=1 →` written inside the newly gold tile,
   arrows drawn properly. They will point at that annotation again in Week 24.

> **🧑‍🏫 Why this is worth two minutes.** Changing stage is the clearest progress signal the course has,
> and it lands today for the first time in six weeks. It also frames the lesson correctly: `axis` is not
> more numpy trivia, it is the first skill in *cleaning*, where the failure mode stops being a traceback
> and becomes a confident wrong answer. Learners who see that shift stop reading "it ran" as "it
> worked" — the single most valuable habit in Term 3.

> **⚠️ Watch out:** resist ticking stage two off out loud as "done for ever". Week 21 builds a table and
> Week 23 opens a real CSV. Stage two is white, not gone.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Prove numpy still works.** Four seconds:

```bash
python3 -c "import numpy; print(numpy.__version__)"
```

```text
1.26.4
```

If that fails, go back to Week 17's Prep Checklist and fix the install tonight. **This lesson has a good paper version, but the paper version is a fallback, not the plan.**

- [ ] **Print workbook pages 19.1–19.6.**
- [ ] **Find graph paper**, or print Figure 19.5's grid twice — once for you, once for them.
- [ ] **Find a calculator and put it on the table.** A phone calculator is fine. The hand-check is not optional this week and "I'll do it in my head" is how a hand-check becomes a guess.
- [ ] **Type and run the code yourself.** One file, `rainfall.py`. Type it; do not paste it — you want to have made a small mistake tonight rather than in front of them.

```python
"""rainfall.py - one grid, two directions. Week 19."""

import numpy as np                          # bring numpy in, call it np

# --- the grid: 4 cities DOWN, 6 months ACROSS -------------------------------
#            Jan  Feb  Mar  Apr  May  Jun
rain = np.array([
    [ 25,  10,   5,  15,  40,  55],         # row 0 - Chennai
    [  2,   4,  10,  20,  36,  90],         # row 1 - Pune
    [ 65,  70,  60,  45,  51, 105],         # row 2 - Shimla
    [ 22,  26,  54, 120, 300, 480],         # row 3 - Kochi
])

cities = np.array(["Chennai", "Pune", "Shimla", "Kochi"])
months = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

print("shape :", rain.shape)                # rows first, then columns
print("cities:", cities.shape)              # must match the FIRST number of shape
print("months:", months.shape)              # must match the SECOND number of shape

# --- one cell: row first, then column, one comma between them ---------------
print("rain[1, 2] =", rain[1, 2])           # row 1, column 2 = Pune in March

# --- a whole row, and a whole column ---------------------------------------
print("rain[1, :] =", rain[1, :])           # every month for Pune
print("rain[:, 0] =", rain[:, 0])           # January for every city

# --- one answer PER MONTH: eat the rows, so axis=0 --------------------------
month_mean = rain.mean(axis=0)              # 4 rows squashed away -> 6 answers
print("per month :", month_mean)
print("how many? :", month_mean.shape, "- should be 6, one per month")

# --- one answer PER CITY: eat the columns, so axis=1 -----------------------
city_mean = rain.mean(axis=1)               # 6 columns squashed away -> 4 answers
print("per city  :", city_mean)
print("how many? :", city_mean.shape, "- should be 4, one per city")

# --- totals, the same two directions ---------------------------------------
city_total = rain.sum(axis=1)               # one total per city
month_total = rain.sum(axis=0)              # one total per month
print("city totals :", city_total)
print("month totals:", month_total)

# --- the cross-check: three routes to the same total --------------------------
print("city totals add to :", city_total.sum())
print("month totals add to:", month_total.sum())
print("whole grid adds to :", rain.sum())

# --- the report, with the labels put back on -------------------------------
print()
print("City      Total  Mean")
print("-" * 22)
for i in range(len(cities)):                # a loop for PRINTING only
    print(f"{cities[i]:<9} {city_total[i]:>5} {city_mean[i]:>5.1f}")
```

Run `python3 rainfall.py`. You must see **exactly** this:

```text
shape : (4, 6)
cities: (4,)
months: (6,)
rain[1, 2] = 10
rain[1, :] = [ 2  4 10 20 36 90]
rain[:, 0] = [25  2 65 22]
per month : [ 28.5   27.5   32.25  50.   106.75 182.5 ]
how many? : (6,) - should be 6, one per month
per city  : [ 25.  27.  66. 167.]
how many? : (4,) - should be 4, one per city
city totals : [ 150  162  396 1002]
month totals: [114 110 129 200 427 730]
city totals add to : 1710
month totals add to: 1710
whole grid adds to : 1710

City      Total  Mean
----------------------
Chennai     150  25.0
Pune        162  27.0
Shimla      396  66.0
Kochi      1002 167.0
```

- [ ] **Break it on purpose, twice.** These are the two you will do in front of the student, and you want to have seen both already.
  1. Change `rain[1, 2]` to `rain[1, 6]` — "June is the sixth month". You must get `IndexError: index 6 is out of bounds for axis 1 with size 6`.
  2. Change `rain.mean(axis=0)` to `rain.mean(axis=1)` on the per-month line. **It will not crash.** You will get four numbers where six belong. Sit and look at that for ten seconds. That feeling is the lesson.
- [ ] **Do the hand-check yourself, on paper, with the calculator.** Row 1: `2 + 4 + 10 + 20 + 36 + 90 = 162`, `162 / 6 = 27.0`. Column 1: `10 + 4 + 70 + 26 = 110`, `110 / 4 = 27.5`. Write both down. You are about to ask a 12-year-old to do this and it will go better if you have felt how long it takes (about ninety seconds each).
- [ ] **Notice that 27.0 and 27.5 are nearly the same.** Do not point it out tomorrow. Just know it is there.

### 5 minutes on the day

- [ ] Editor open, terminal in the same folder. `rainfall.py` **deleted or renamed** — they type it.
- [ ] Graph paper, pencil, **calculator** on the table before they sit down.
- [ ] Workbook 19.1–19.3 out. **19.2's "how many answers?" column must be filled in before any code runs**, in pen.
- [ ] Bug Log out, with the *errors with no error message* section findable — there is a new entry today and it is a good one.
- [ ] The Week 18 revisit list beside you. If it names something, spend the first five minutes of the Hook on it; this lesson has room.

### Fallback if the laptop or the install fails

**This week's paper version is not a consolation prize.** The activity is *designed* to happen on paper first, and the code only confirms it. If there is no computer at all, you lose the confirmation and keep the lesson.

1. **Draw the grid** on graph paper: four cities down, six months across, headers on. Six minutes.
2. **Draw two empty margins** — a column down the right and a row along the bottom, as in Figure 19.5 — and an empty corner box where they meet.
3. **Fill the right-hand margin.** One number per city: add the row, divide by six. Four answers. Ask before they start: *"how many numbers will be in this margin?"* Four. **They have just done `axis=1`.**
4. **Fill the bottom margin.** One number per month: add the column, divide by four. Six answers. Ask first: *"how many now?"* Six. **They have just done `axis=0`.**
5. **Fill the corner two ways** — add the row totals, add the column totals. Both must give 1710. That is the corner check, on paper, and it is more convincing with a pencil than with a print statement.
6. **Then the naming.** Write on the board: *the margin down the side ate the columns → `axis=1`. The margin along the bottom ate the rows → `axis=0`.* Have them label their own two margins with those words. **That is objectives 3, 4 and 5 delivered with no computer.**

| If this fails | Do this instead |
|---|---|
| numpy is missing | Do not debug for more than three minutes. Do the paper version in full, set the install as homework with Week 17's three commands written down, and fix it yourself before Week 20 — **Week 20 is a numpy lab and has no paper version.** |
| The graph-paper grid eats fifteen minutes | Pre-draw the grid yourself before the lesson and have them fill in only the numbers. The drawing is not the lesson; the margins are. |
| No calculator anywhere | Six two-digit numbers can be added on paper; that is fine and takes two minutes. Do **not** allow "in my head" for the division — `162 / 6` in your head is where a hand-check silently becomes a guess. |
| The student refuses to hand-check because "the computer is right" | Do the wrong-axis demo *first*, before the hand-check. Once they have watched the computer print a confident wrong number, the argument is over and you did not have to make it. |
| A student's grid has a typo in it | **Excellent.** Their hand-added margin totals will disagree with the code's totals (the code's three totals will still agree with each other). Let it show, let them find it, and put it in the Bug Log. This is the best possible thing that can happen today. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Three Averages, One Table | 7 | 7 | The same question gets three different right answers, on paper |
| 🧠 Concept — The Axis You Name Gets Eaten | 16 | 23 | axis 0 and axis 1; 2-D indexing; the colon; and the counts **written down** |
| 💻 Live-Code Together — `rainfall.py` | 18 | 41 | Both directions built. Two deliberate mistakes: one loud, one silent |
| 🎲 Their Turn — The Rainfall Grid, Pencil First | 20 | 61 | Hand-check row 1 and column 1, then confirm with code |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Three Averages, One Table (7 minutes)

**Do this:** Nothing on the screen. Graph paper and pencil on the table. Draw — or hand over pre-drawn — the four-by-six rainfall grid with its headers. If you are pre-drawing, do it before they arrive.

**Say this:**

> "This is rainfall. Four cities down the side — Chennai, Pune, Shimla, Kochi. Six months across the top — January to June. Every number is millimetres of rain that fell in that city in that month.
>
> Twenty-four numbers. One question. **What's the average rainfall?**
>
> Go on. Work it out."

**Do this:** Let them start. Almost every student starts adding along a row, or starts adding everything. Let them get about forty seconds in, then stop them.

> "Hold on. Put the pencil down. I want to ask you something first.
>
> **How many numbers is your answer going to be?**"

Let that sit. It is a strange question and it should feel strange.

> "Because I can see three different answers on this page and all three of them are correct.
>
> **One number** — add up all twenty-four, divide by twenty-four. That's the average rainfall of this entire piece of paper. It's 71.25, and I'm not sure what you'd do with it.
>
> **Four numbers** — one per city. How wet is Chennai on average, how wet is Pune. That's four answers because there are four cities.
>
> **Six numbers** — one per month. How wet is January on average, across all the cities. That's six answers because there are six months.
>
> Same table. Same twenty-four numbers. Three completely different, completely correct answers. So when you asked yourself 'what's the average', **you hadn't finished asking the question yet.**"

**Do this:** Write on the board, and leave it up all lesson:

```text
one number   -> the whole table
four numbers -> one per CITY   (there are 4 cities)
six numbers  -> one per MONTH  (there are 6 months)
```

> "Here's the deal for today. The computer will happily give you any of those three. It will never ask which one you meant. It will never tell you that you picked the wrong one.
>
> So the first thing you're going to learn today isn't a piece of Python. It's a habit: **before you ask a computer for an average, decide how many answers you expect.** Four or six. If you get four when you wanted six, you asked the wrong question and the answer is wrong — and it'll look completely fine."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How many numbers is your answer going to be?" | It depends what I'm averaging — per city or per month. | If they say "one", accept it as one of the three and then ask: "would one number tell you which city to take an umbrella to?" |
| "Why are there four city answers and six month answers?" | Because there are four cities and six months. | If they are unsure, have them count the rows out loud, then the columns. The count of labels *is* the count of answers. |
| "Which of the three answers would a weather forecaster want?" | Probably the six — one per month — because they are talking about seasons. Or the four, if they are comparing cities. | Any defended answer is right. The point is that the *question* decides, not the data. |
| "If I gave you six numbers when you wanted four, would you notice?" | Yes — I'd count them. | If they say "no", say: "good, that's honest. That's exactly what we're fixing today." |
| "Is 71.25 wrong?" | No. It is a correct average of a thing nobody asked about. | If they say "yes, it's wrong", correct this carefully: **it is right and useless.** That distinction matters all year. |

---

### 🧠 Concept — The Axis You Name Gets Eaten (16 minutes)

**Do this:** Grid still on the table. Board work. Nothing typed yet.

**Say this — part 1, the two directions have numbers:**

> "You already know the shape of this table. Count the rows."

*Four.*

> "Count the columns."

*Six.*

> "So the shape is `(4, 6)`. Rows first — that's Week 17 and it hasn't changed.
>
> Now the new bit, and it's tiny. **Those two positions in the shape have numbers.** The first one — the rows — is called **axis 0**. The second one — the columns — is called **axis 1**."

Write on the board:

```text
shape (4, 6)
       |  |
       |  +--- axis 1 : the columns : 6 of them
       +------ axis 0 : the rows    : 4 of them
```

> "That's the whole naming scheme. **The axis number is just the position in the shape.** First position, axis 0. Second position, axis 1. Nothing to memorise."

**Say this — part 2, the sentence that carries the whole week:**

> "Here's the sentence. I'm going to say it about forty times today and I want you saying it too.
>
> **The axis you name is the axis that gets eaten.**
>
> Watch. I say `axis=0`. Axis 0 is the rows. So the **rows get eaten** — all four of them get squashed together and disappear. What's left?"

*The columns.*

> "The columns. Six of them. So I get **six answers, one per month.** Draw it."

**Do this:** On the grid, draw six downward arrows out of the bottom of the six columns, and six empty boxes underneath. Point at Figure 19.1 if you have it printed.

> "Now the other one. I say `axis=1`. Axis 1 is the columns. So the **columns get eaten** — all six squashed together, gone. What's left?"

*The rows.*

> "Four rows. **Four answers, one per city.** Draw that too."

**Do this:** Four arrows out of the right-hand side, four empty boxes.

> "And notice what you can now do that you couldn't do five minutes ago. **You can predict the number of answers before you run anything.** Name axis 0, get six. Name axis 1, get four. If you name axis 0 and six numbers come out, you're on track. If four come out, you've made a mistake — and it's the kind of mistake that doesn't crash."

**Say this — part 3, pointing at one cell:**

> "Before the averages, one smaller thing: how do you point at a single cell?
>
> One pair of square brackets, two numbers, one comma. **Row first, then column.** Like this."

Write on the board: `rain[1, 2]`

> "Read it out loud with me: **row one, column two.**
>
> Now put your finger on it."

**Do this:** Wait. Most students will point at Chennai/February. Do not correct with words.

> "Say the row number out loud as you count down from the top. Start at zero."

*Zero... one.* — their finger moves to Pune.

> "And the column, starting at zero."

*Zero, one, two.* — March.

> "**Pune, March. Ten millimetres.** Not Chennai, not February. Rows and columns both start at zero, so 'row 1' is the *second* row. In English, row 1 is the first row. In Python it isn't. That's going to catch you today, and the cure isn't a rule — it's your finger. **Every single time you write an index, put your finger on the cell.**"

**Say this — part 4, the colon:**

> "Last piece. What if you want a whole row, or a whole column?
>
> You put a **colon** where the number would go, and a colon means **'every one of these'**."

Write on the board:

```text
rain[1, :]   ->  row 1, EVERY column   ->  all six of Pune's months
rain[:, 0]   ->  EVERY row, column 0   ->  January, in all four cities
```

> "Read the second one out loud: **'every row, column zero.'** Now put your finger on all four of those cells."

Let them trace the January column.

> "One more thing about that, and it surprises people. When we run it, `rain[:, 0]` will print `[25 2 65 22]` — **sideways.** You took a column and it printed as a row. That's not a bug. Four numbers standing up and four numbers lying down are the same four numbers. **numpy doesn't remember that they used to be a column.**"

**Say this — part 5, and this is the design of the lesson:**

> "Right. **Workbook page 19.2, in pen, before we touch the keyboard.**
>
> There are eight lines of code on that page. Next to each one, write **how many numbers you think will come out.** Not what the numbers are — just *how many.* One? Four? Six? Twenty-four?
>
> In pen, because I don't want you deciding what you thought after you've seen the answer. Being wrong is completely fine. Quietly changing your guess is not.
>
> Four minutes. Go."

**Do this:** Circulate. Say nothing that confirms or denies. Not a nod, not a face. This is genuinely hard and it matters.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What is axis 0?" | The rows — the first number in the shape. | If they say "the columns", have them read the shape out loud, then point: "which number is rows? So which position is it in?" |
| "I write `axis=1`. What gets eaten?" | The columns. So the answers are one per row — one per city. | If they say "the rows get eaten", say the sentence again and have them repeat it: *the axis you name is the axis that gets eaten.* Then re-ask. |
| "I want one number per month. Which axis?" | 0 — because months are columns, and to keep the columns you have to eat the rows. | This is the hard direction. Walk it: "months are columns. Do you want to keep columns or eat them? Keep. So what do you eat? Rows. What number is rows?" |
| "What does `rain[2, 4]` point at?" | Shimla, May — 51. | If they land on Pune/April, count out loud from zero with your finger on the paper. Do not give the rule. |
| "What does the colon mean?" | Every one of them, in that direction. | If they say "all the numbers", tighten it: "all of them in *which* direction? The colon is in one position, not both." |
| "How many numbers will `rain[:, 0]` give me?" | Four — one per city. | If they say six, ask: "how many rows does the colon cover?" |
| "How many will `rain.sum(axis=1)` give me?" | Four. | If wrong, back to the sentence. Then have them draw the four arrows. |

---

### 💻 Live-Code Together — `rainfall.py` (18 minutes)

**You never touch the keyboard.** They type every character. Predictions before every single run — *how many numbers?*

**Step 1 (4 min).** New file, `rainfall.py`. The grid and the labels.

```python
"""rainfall.py - one grid, two directions. Week 19."""

import numpy as np                          # bring numpy in, call it np

# --- the grid: 4 cities DOWN, 6 months ACROSS -------------------------------
#            Jan  Feb  Mar  Apr  May  Jun
rain = np.array([
    [ 25,  10,   5,  15,  40,  55],         # row 0 - Chennai
    [  2,   4,  10,  20,  36,  90],         # row 1 - Pune
    [ 65,  70,  60,  45,  51, 105],         # row 2 - Shimla
    [ 22,  26,  54, 120, 300, 480],         # row 3 - Kochi
])

cities = np.array(["Chennai", "Pune", "Shimla", "Kochi"])
months = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

print("shape :", rain.shape)                # rows first, then columns
print("cities:", cities.shape)              # must match the FIRST number of shape
print("months:", months.shape)              # must match the SECOND number of shape
```

**Ask before running:** "Three lines of output. What will they say?"

Run it. Real output:

```text
shape : (4, 6)
cities: (4,)
months: (6,)
```

> **Say this:** "One row per line and a comment naming the city — same rule as Week 17. **The shape of the code should be the shape of the array**, so you can see mistakes with your eyes instead of finding them with a print statement.
>
> And look at what those last two lines are for. `cities` has four names. The first number of the shape is four. `months` has six names, and the second number of the shape is six. **Those two lines are a check, not decoration.** If you ever type a row with five numbers in it by accident, this is where you find out."

**Step 2 — ⚠️ FIRST DELIBERATE MISTAKE (4 min).** Dictate it wrongly on purpose. This is the natural mistake and it is loud.

> **Say this:** "Now point at one cell. I want June for Pune. Pune is row 1. And June is the sixth month, so — type `print("June for Pune:", rain[1, 6])`."

```python
print("June for Pune:", rain[1, 6])
```

**Ask before running:** "Will this work?" *(Most say yes.)*

Run it. Real output:

```text
shape : (4, 6)
cities: (4,)
months: (6,)
Traceback (most recent call last):
  File "rainfall.py", line 20, in <module>
    print("June for Pune:", rain[1, 6])
IndexError: index 6 is out of bounds for axis 1 with size 6
```

> **Say this:** "Read the last line and tell me what it's complaining about."

*Index 6 is out of bounds. There are only six.*

> "Exactly. And read the middle of it too, because numpy has just used today's word at you: **'for axis 1'.** It's telling you *which direction* you got wrong. Not the rows — the columns. That's genuinely helpful and you should get used to reading it.
>
> So: six columns, and the last one is number...?"

*Five.*

> "Five. Zero, one, two, three, four, five. **June is column 5**, not column 6. This is Week 11's off-by-one, in a second direction. Fix it."

```python
print("June for Pune:", rain[1, 5])
print("rain[1, 2] =", rain[1, 2])           # row 1, column 2 = Pune in March
```

Run it. Real output (last two lines):

```text
June for Pune: 90
rain[1, 2] = 10
```

> **Say this:** "Ninety. Put your finger on it — Pune, June. And ten: Pune, March. Both right.
>
> **Bug Log this one.** `IndexError ... for axis 1 with size 6`. And write the useful bit in the fix column: **the message tells you which axis you got wrong.** You will want that in about four minutes."

**Step 3 (3 min).** The colon.

```python
print("rain[1, :] =", rain[1, :])           # every month for Pune
print("rain[:, 0] =", rain[:, 0])           # January for every city
```

**Ask before running:** "How many numbers from each line? Say both before I press it."

*Six, then four.*

Run it. Real output (last two lines):

```text
rain[1, :] = [ 2  4 10 20 36 90]
rain[:, 0] = [25  2 65 22]
```

> **Say this:** "Six and four. You called it.
>
> Now the odd one. Look at the second line. You asked for a **column** — every row, column zero — and it printed **sideways**, as a row. Is that wrong?"

Let them argue for a moment.

> "It's not wrong. It's four numbers, and four numbers are four numbers. Being a column isn't something the array keeps — that was just where they happened to be sitting. If you want to know what shape it is, don't guess: print `rain[:, 0].shape` and read it. It's `(4,)`. One direction, four numbers."

**Step 4 — ⚠️ SECOND DELIBERATE MISTAKE (4 min).** This one **does not crash.** Do not warn them. Do not smile.

> **Say this:** "Right, the real thing. I want the average rainfall **for each month.** Six answers, one per month. Type this."

```python
month_mean = rain.mean(axis=1)              # per month... or so we hope
print("per month :", month_mean)
```

**Ask before running:** "How many numbers should come out?"

*Six.*

Run it. Real output (last line):

```text
per month : [ 25.  27.  66. 167.]
```

**Do this:** Say nothing. Wait. Let them read it. Count silently to five.

> **Say this:** "So. January's average rainfall is 25 millimetres. Write that down."

Let them start writing. Then:

> "Actually — hang on. **How many numbers are there?**"

*Four.*

> "And how many months are there?"

*Six.*

*(pause)*

> "So what have we got?"

*Four answers for six months.*

> "Four answers for six months. **And Python didn't say a word.** No traceback, no warning, no red text. It printed four tidy decimal numbers with a full stop after each one and let me write down a wrong answer about January.
>
> What did it actually give us?"

*The averages per city.*

> "Per city. `25.0` is Chennai's average across all six months. It's a perfectly good number. It answers a question nobody asked. **And it's in the right range — 25 millimetres is a believable amount of rain.** Nothing about that number looks wrong.
>
> Why did it happen? Say the sentence."

*The axis you name gets eaten.*

> "I named axis 1. Axis 1 is the columns. So the columns got eaten, so the answers are one per row — one per **city**. I asked for the wrong direction and I got exactly what I asked for.
>
> Fix it. And add a line that would have caught it."

```python
month_mean = rain.mean(axis=0)              # 4 rows squashed away -> 6 answers
print("per month :", month_mean)
print("how many? :", month_mean.shape, "- should be 6, one per month")
```

Run it. Real output (last two lines):

```text
per month : [ 28.5   27.5   32.25  50.   106.75 182.5 ]
how many? : (6,) - should be 6, one per month
```

> **Say this:** "Six. And January is **28.5**, not 25.0. Both of those are believable numbers about rain. Only one of them is the answer.
>
> Look at that second print line. It costs you eight seconds to type and it makes the mistake **impossible to miss**. From today, when you write an axis, you write the count check underneath it. Every time.
>
> **Bug Log.** This goes under *errors with no error message* — and it is the best entry in the book so far, because there is no message to write down. In the 'what the student sees' column, write: **'four numbers instead of six.'** That's the whole error."

**Step 5 (3 min).** The other direction, and the corner check.

```python
city_mean = rain.mean(axis=1)               # 6 columns squashed away -> 4 answers
print("per city  :", city_mean)
print("how many? :", city_mean.shape, "- should be 4, one per city")

city_total = rain.sum(axis=1)               # one total per city
month_total = rain.sum(axis=0)              # one total per month
print("city totals :", city_total)
print("month totals:", month_total)

print("city totals add to :", city_total.sum())
print("month totals add to:", month_total.sum())
print("whole grid adds to :", rain.sum())
```

**Ask before running:** "The last three lines. What do you think happens?"

Run it. Real output:

```text
per city  : [ 25.  27.  66. 167.]
how many? : (4,) - should be 4, one per city
city totals : [ 150  162  396 1002]
month totals: [114 110 129 200 427 730]
city totals add to : 1710
month totals add to: 1710
whole grid adds to : 1710
```

> **Say this:** "Three routes, one number. Add it up in rows: 1710. Add it up in columns: 1710. Add the whole thing at once: 1710.
>
> That's not a coincidence and it's not magic — it's the same twenty-four numbers, added in three different orders. **All three of those always agree.** That is the point of the check on paper, where your adding-up can slip; in numpy they cannot disagree, so a match proves nothing about the axis or the data.
>
> Accountants have been doing this for centuries. It's called cross-footing. On paper it catches slips in your adding-up; in Python it's one line that will always agree, so use it to prove you understand the two directions."

**Step 6 (optional, if there is time).** The labelled report — the loop that only prints.

```python
print()
print("City      Total  Mean")
print("-" * 22)
for i in range(len(cities)):                # a loop for PRINTING only
    print(f"{cities[i]:<9} {city_total[i]:>5} {city_mean[i]:>5.1f}")
```

```text

City      Total  Mean
----------------------
Chennai     150  25.0
Pune        162  27.0
Shimla      396  66.0
Kochi      1002 167.0
```

> **Say this:** "One last thing worth naming. There's a `for` loop in this file — after four weeks of retiring loops. Look at what it does: **it prints.** It doesn't add anything up, it doesn't work anything out. All the arithmetic happened in two lines with axes in them.
>
> That's the rule from here on: **arrays do the maths, loops do the printing.** And the loop is what puts the names back on, which is the thing the array threw away."

---

### 🎲 Their Turn — The Rainfall Grid, Pencil First (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–2:** the two empty margins get drawn on their graph paper, and the corner box.
- **Minutes 2–8:** **row 1 and column 1, by hand, with the calculator.** Written in pen. Nobody touches a keyboard.
- **Minutes 8–15:** the code confirms both. Every axis line gets a count printed under it.
- **Minutes 15–18:** the corner check, three ways.
- **Minutes 18–20:** the sentence for 19.6 gets started out loud, so nobody goes home with a blank page.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** graph paper with the four-by-six grid drawn and filled in; a pencil; **a calculator**; workbook page 19.3 (the hand-check) and page 19.2 (the counts, already written in pen); the Bug Log.

**On the screen:** `rainfall.py` from the live-code, with room at the bottom.

**The one rule that makes this work:** *the pencil goes first.* Both hand-checks are written in pen before any code runs, and they may not be edited afterwards. If a student wants to change one, they write the new answer beside the old one and mark which came first.

![A graph-paper sheet with the rainfall grid and two empty yellow margins plus a corner box](../figures/fig-w19-5-rainfall-grid-setup.svg)
*Figure 19.5 — Draw the two margins and the corner box before you start. Pencil goes in the yellow boxes.*

### Part 1 — the two margins, drawn (2 minutes)

Down the right-hand side of the grid, an empty column, four boxes tall. Along the bottom, an empty row, six boxes wide. Where they meet, one corner box.

Before they write a single number, ask both questions:

> **"How many numbers go in the side margin?"** — Four. One per city.
>
> **"How many go in the bottom margin?"** — Six. One per month.

If they can answer those two, they have already understood today's lesson and the rest is arithmetic.

### Part 2 — the hand-check, in pen (6 minutes)

**Row 1 first.** Say the trap out loud before they start, because you want them to get it right and *know why*:

> "Row 1. Careful — **row 1 is the second row.** Rows are numbered from zero, so row 0 is Chennai and row 1 is Pune. Put your finger on it. Pune."

```text
2 + 4 + 10 + 20 + 36 + 90 = 162
162 / 6 = 27.0
```

> "Why divide by six?"

*Six months.*

**Then column 1.**

> "Column 1 — same trap, other direction. Column 0 is January, so column 1 is **February.** Trace it down with your finger: 10, 4, 70, 26."

```text
10 + 4 + 70 + 26 = 110
110 / 4 = 27.5
```

> "Why divide by four?"

*Four cities.*

**Both written in pen, on page 19.3, before any code runs.** Then, and only then:

> "Now go and see whether the computer agrees with you."

### Part 3 — the code confirms (7 minutes)

They add this to the bottom of `rainfall.py`:

```python
# --- the hand-check ---------------------------------------------------------
# Row 1 is PUNE (row 0 is Chennai). By pencil:
#   2 + 4 + 10 + 20 + 36 + 90 = 162, and 162 / 6 = 27.0
print()
print("row 1 by hand : 162 / 6 = 27.0")
print("row 1 by code :", rain[1, :].sum(), "/ 6 =", rain.mean(axis=1)[1])

# Column 1 is FEBRUARY (column 0 is January). By pencil:
#   10 + 4 + 70 + 26 = 110, and 110 / 4 = 27.5
print("col 1 by hand : 110 / 4 = 27.5")
print("col 1 by code :", rain[:, 1].sum(), "/ 4 =", rain.mean(axis=0)[1])
```

Real output:

```text

row 1 by hand : 162 / 6 = 27.0
row 1 by code : 162 / 6 = 27.0
col 1 by hand : 110 / 4 = 27.5
col 1 by code : 110 / 4 = 27.5
```

Two things to draw out while they look at it:

1. **`rain.mean(axis=1)[1]` has two ones in it and they mean different things.** The `axis=1` says *eat the columns*. The `[1]` says *and then give me the second of the answers.* Ask which one they could change to get Shimla's average. (The second: `[2]`.)
2. **`rain[1, :].sum()` and `rain.sum(axis=1)[1]` give the same 162.** Two routes. The first takes the row out and adds it; the second adds all four rows and picks one. Both are fine. Ask which one they would use if they wanted all four totals. (The second — it does all four at once.)

### Part 4 — the corner check (3 minutes)

On paper: add the four side-margin totals. Add the six bottom-margin totals. Both go in the corner box.

```text
150 + 162 + 396 + 1002 = 1710
114 + 110 + 129 + 200 + 427 + 730 = 1710
```

> **Say this:** "One number, reached two ways. If your two ways disagree, you have made a slip in your adding-up and you have just found it without anybody telling you. **That is what a check is.**"

### What "finished" looks like

- `rainfall.py` prints the shape, one cell, one whole row, one whole column, a per-month mean and a per-city mean.
- **Every axis line has a count printed under it** — `(6,)` for months, `(4,)` for cities.
- Row 1 and column 1 are worked out **in pen, on paper, before the code ran**, and both match.
- The corner check gives 1710 by three routes.
- The wrong-axis mistake is in the Bug Log, under *errors with no error message*, with "four numbers instead of six" written where the error message would go.
- The student can say, unprompted, *"the axis you name is the axis that gets eaten."*

### Variation — easier

- **Cut the grid to three cities and four months.** Twelve numbers. Every idea survives; the arithmetic stops being the hard part. Use Chennai, Pune, Shimla and Jan–Apr, and hand-check row 1 as `2 + 4 + 10 + 20 = 36`, `36 / 4 = 9.0`.
- **Hand-check the row only, not the column.** The row is much easier to trace with a finger. Do the column as a whole-class demonstration you narrate.
- **Give them `rainfall.py` up to the end of Step 3** — grid, labels, indexing — and have them add only the two axis lines and the two count lines. The understanding is in choosing the axis and reading the count, not in typing the grid.
- **Do all of Part 1 and Part 2 and stop.** Two margins filled in pencil, with the counts predicted first, is the entire lesson. The code can be tomorrow's warm-up.
- **Skip `.sum` entirely.** `.mean` twice makes the axis point completely.
- **Never let the index be a guess.** Finger on the cell, count out loud from zero, every time. If nothing else survives today, this survives.

### Variation — harder

None of these need syntax from a later week.

1. **The second grid.** Workbook 19.5's step data — three friends down, five days across — with both directions, both counts, and one hand-check. Different shape, so the counts are 3 and 5 instead of 4 and 6, which is the point.
2. **Make the two hand-checks disagree on purpose.** Have them change one number in the grid *on paper only* and not in the code, then run the check and watch it fail. Then ask the good question: *"which one is wrong — the paper or the code?"* (The paper, this time. Next time it might not be.)
3. **Predict the whole output before running.** Not just the counts — the actual numbers, all ten of them, for `.mean(axis=0)` and `.mean(axis=1)`. Then run. This takes real work and it is enormously good for them.
4. **Which single cell would you change to make Pune the wettest city?** Pune's total is 162 and Kochi's is 1002, so no single cell change can do it while cells stay realistic — the honest answer is *"you can't, and finding that out is the answer."* Then: *"which single cell would make Pune wetter than Chennai?"* (Chennai is 150 and Pune is 162, so Pune already is. Which is itself worth noticing — a student who assumed the top row was the biggest has learned something.)
5. **Two axes, one after the other.** `rain.sum(axis=1).mean()` — add up each city, then average the four totals. That is 1710 / 4 = 427.5. Then: *"is that the same as `rain.mean()`?"* (No: `rain.mean()` is 71.25, because it divides by 24, not 4. **Averaging totals and averaging numbers are different things**, and this is a genuinely deep trap that adults fall into constantly.)
6. **The honest question.** *"This table has no year in it. Is January 2024 or January 2019? Does the average of six Januaries from six different years mean anything?"* There is no right answer and the argument is excellent. It is also exactly the question Week 27 is about.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

> **🧑‍🏫 If a student asks:** numpy's own errors sometimes print several `File` lines from inside numpy itself before the useful one. **Read the last line first, always.** Then look for the `File` line that names *your* file — that is the one you can do something about.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `IndexError: index 6 is out of bounds for axis 1 with size 6` | "You asked for column 6. There are six columns, so the last one is number 5." | Counting columns from 1. "June is the sixth month, so column 6." | `rain[1, 5]`. Columns are 0, 1, 2, 3, 4, 5. Note that numpy tells you **which axis** — that is the direction you got wrong. |
| `IndexError: index 4 is out of bounds for axis 0 with size 4` | Same mistake, on the rows. | `rain[4, 0]` — asking for the fifth of four cities. | `rain[3, 0]`. And read `axis 0`: it is the *rows* you overran, not the columns. |
| `numpy.exceptions.AxisError: axis 2 is out of bounds for array of dimension 2` | "There is no third direction in this array." | `rain.mean(axis=2)`. A table has exactly two directions, numbered 0 and 1. | `axis=0` or `axis=1`. On older numpy this reads `numpy.AxisError` — same thing. |
| `SyntaxError: invalid syntax` with a `^` under the comma | "I can't even read this line." | `rain[, 0]` — trying to leave the row position empty. | `rain[:, 0]`. The colon is compulsory; there is no short form for a column. |
| `IndexError: too many indices for array: array is 2-dimensional, but 3 were indexed` | "You gave me three numbers and this thing only has two directions." | `rain[1, 2, 3]` — an extra comma and number, usually a typo. | Two numbers, one comma: `rain[1, 2]`. |
| ``IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices`` | "You put something in the brackets that isn't a position." | `rain[:, "Jan"]` — using the month's *name* as a column index. | `rain[:, 0]`. An array has no idea what its columns are called. **This is exactly what Week 21 fixes.** |
| `TypeError: 'numpy.ndarray' object is not callable` | "You put round brackets after something that isn't a function." | `rain(1, 2)` with round brackets instead of square ones. | `rain[1, 2]`. Square brackets point at things; round brackets call functions. |
| `TypeError: 'tuple' object is not callable` | "You put brackets after something that isn't a function." | `rain.mean(axis=0).shape()`. `.shape` is a fact, not an action. | `rain.mean(axis=0).shape`, no brackets. Third appearance of this one; it is in the Bug Log from Week 17. |
| `TypeError: 'str' object cannot be interpreted as an integer` | "The axis has to be a number and you gave me writing." | `rain.mean(axis="0")` — quote marks round the zero. | `rain.mean(axis=0)`. No quotes: it is a number, not a name. |
| **No error, four numbers instead of six** | Nothing is wrong as far as numpy is concerned. Both are legal averages. | The wrong axis. `axis=1` when the question was about columns. | Count the answers against the count of labels. Six months means six numbers. **This is the week's headline bug and it has no message.** |
| **No error, but the student's hand-added totals disagree with the code's** | Nothing is wrong as far as numpy is concerned. (The code's own three totals cannot disagree.) | A slip in the paper adding, or a grid typed differently from the paper (a ragged row would instead be refused with a `ValueError` when the array is built). | Print `rain.shape` and compare it with `len(cities)` and `len(months)`. Then find the row or column whose paper total differs from the code's. |
| **No error, `rain[:, 0]` printed sideways** | Nothing is wrong at all. This is correct. | A column and a row of the same four numbers are the same array. Shape `(4,)`. | Nothing to fix. Print `.shape` if you doubt it. |

### How to teach debugging without giving the answer

The moves all still stand: read the last line, find *your* file's line number, say the complaint in your own words, compare characters, print `.shape` and `.dtype` before forming a theory. This week adds one, and it is the most important one so far because it works on errors that have no message:

10. **"How many answers did you expect, and how many did you get?"**

Ask it before you look at anything else. It costs one sentence, it needs no Python knowledge from you, and it catches the entire class of mistakes that this week introduces. If the counts differ, the student has an axis problem and they can find it themselves. If the counts match and the answer still looks wrong, *now* you have a genuinely interesting bug.

And the sentence for this week:

> **"An answer that ran is not an answer that's right. Count it, then hand-check one of it."**

---

## ❓ Questions Students Ask This Week

**"Why is it called axis 0 and axis 1 and not rows and columns?"**

Because "rows and columns" runs out. A table has two directions. A stack of tables — one per year, say — has three. A colour image has three (height, width, and which colour). A batch of a thousand images has four. There is no word for the fourth direction, so numpy numbers them instead, starting at 0 like everything else in Python.

The useful consequence: **the rule you learn today never changes.** In a three-direction array, `axis=0` still names the first direction and naming it still eats it. In Level 3 you will meet arrays with four directions and this exact sentence will still be the whole story.

**"How do I remember which is which?"**

Don't remember it — **read it.** Print `.shape`. It is `(4, 6)`. The 4 is the first number, so rows are axis 0. The 6 is second, so columns are axis 1. You are not memorising a fact; you are reading one off the screen.

And then use the eating sentence to get from there to the answer. `axis=0` names the rows, so the rows go, so you get one answer per column. Two steps, both re-derivable, nothing to forget at two in the afternoon.

**"Why does `rain[:, 0]` print sideways?"**

Because a column is not a *kind* of array — it is just where some numbers happened to be sitting. When you pull them out you have four numbers and one direction, shape `(4,)`, and numpy prints anything one-directional left to right.

If it helps: think of the grid as a chocolate bar and `rain[:, 0]` as snapping off one strip. Once it is in your hand, whether it *used* to be vertical or horizontal is not a property of the strip. (There *is* a way to keep a column upright as a `(4, 1)` array, and Week 18's sting shows why that can bite you. It is not needed today.)

**"Is `rain[1][2]` wrong?"**

No. It gives `10`, exactly like `rain[1, 2]`. It works because `rain[1]` hands you Pune's whole row, and then `[2]` picks the third thing out of that row.

Two reasons to write the comma version anyway. **One:** it makes one number instead of making a whole row and then throwing it away, which matters when the grid is large. **Two, and this is the real one:** you cannot write the colon trick in the double-bracket form. `rain[:, 0]` has no `rain[...][...]` equivalent, and a column is exactly the thing you need it for. Learn one form and let it be the one that does everything.

**"What if I want the average of just some of the rows?"**

That is a real question and the honest answer is: **not yet, but soon, and you already have half of it.** You could pull out the rows you want by hand — `rain[1, :]` and `rain[2, :]` — and average those. What you cannot yet do is say "all the rows where the total is over 300" in one line, and that is next week: a mask.

Say the timeline out loud, because it makes the course feel like a course: *"today you can name a direction. Next week you can name a condition. In Week 22 you can do it to a table with names on."*

**"How is `rain.mean()` different from `rain.mean(axis=0).mean()`?"**

This is a fantastic question and the answer surprises people.

- `rain.mean()` adds all twenty-four numbers and divides by 24. That is 71.25.
- `rain.mean(axis=0).mean()` averages each column, then averages those six answers. That is *also* 71.25 — because every column has the same number of cities in it, so nothing gets unfairly weighted.

Now the trap. `rain.sum(axis=1).mean()` is **not** 71.25. It is 1710 / 4 = **427.5**, because you added up each city first and then averaged four big totals. **Averaging totals and averaging numbers are different things.**

This matters far beyond numpy. If one city had reported for three months and another for six, then `mean(axis=0).mean()` would *also* stop matching `mean()`, because you would be treating a three-month average as equal to a six-month one. Adults get this wrong in newspapers constantly. It is called the average-of-averages trap, and Week 27 is partly about it.

**"Should I hand-check every single answer?"** *(Nobody fully agrees, and here is why.)*

No — and there is no agreed rule for how much is enough. This is a genuine, live argument among people who work with data for a living, and it is worth being honest about rather than pretending there is a number.

**What everybody agrees on:** hand-check **at least one**, and hand-check it **before** you look at the code's answer. One check catches an enormous share of real mistakes, because most mistakes are not subtle — they are a wrong axis, a wrong column, a typo, a division by the wrong count. Any of those will make your one hand-check fail.

**Where it splits.** One camp says: check one value per new calculation, then move on, because your time is better spent on the *next* check than on the eleventh instance of the same one. The other says: check one at each *end* — the smallest and the largest — because middle-sized answers hide mistakes and extremes expose them. Both are defended by serious people.

**And there is a third position that is harder and probably right:** the number of hand-checks is the wrong question. What matters is whether you have **something that would notice.** A count check that runs every time is worth more than ten hand-checks you did once in March, because the count check is still running in June when you have forgotten what the file does. (The corner check is not an example: in numpy it always agrees, so it would not notice a wrong axis. A built-in check has to compare against something independent, like the count of labels.)

What you should tell a 12-year-old, out loud: **"one hand-check, always, before you believe anything. And then build a check into the file so it keeps checking after you've stopped paying attention."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **"axis=0 means rows, so it gives me the rows"** — said confidently, all lesson | The name of the axis and the shape of the answer point in opposite directions, and the name is the thing they hear | Never let "axis 0 means rows" stand as a whole sentence. Insist on the full one, out loud, from them: *"axis 0 names the rows, so the rows get eaten, so I get one answer per column."* Then make them draw the six arrows. Words are losing this fight; arrows win it. |
| The hand-check is done **after** the code and quietly matches it | A number on a screen is enormously persuasive, and the arithmetic bends to fit | Pen, not pencil, for the hand-check column. Collect page 19.3 before anybody runs anything if you have to. And say why out loud: *"a check you do afterwards isn't a check, it's agreeing."* |
| The wrong-axis bug is spotted by you, not by them | You could not bear the silence | Let the silence run. Count to five. Their job is to notice that four is not six; if you say it, the habit belongs to you and not to them. The Hook exists to make this noticing possible — go back to the board and point at "six numbers -> one per MONTH". |
| `rain[1, 2]` is read as "second row, third column" and pointed at Chennai/February | English rows start at 1 | Do not give the rule again. Finger on the paper, count out loud from zero, both directions. Every single time an index gets written, for the whole lesson. It is tedious and it works. |
| The grid takes fifteen minutes to draw and there is no lesson left | Twenty-four numbers with headers is real writing for a 12-year-old | Pre-draw it. Print Figure 19.5 and hand it over. **The drawing is not the lesson; the two margins are.** |
| The counts are predicted as "lots" or left blank | "How many?" feels like a question with no way of knowing | Point at the labels. *"How many cities did you type? Four. So how many city answers can there possibly be?"* The count of answers is never a mystery — it is the count of labels, which they typed themselves. |
| A student adds `.shape` after everything and stops reading it | It has become a ritual rather than a check | Ask "what should that say?" *before* they run it. A printed shape nobody predicted is decoration. A predicted shape that got confirmed is a check. |
| The paper margin totals disagree with the code's totals and get ignored as "probably rounding" | Because they want to be finished | Stop everything. This is the most valuable twelve minutes of the week. Print `rain.shape`, compare it with `len(cities)` and `len(months)`, and then add the rows up by hand until you find the odd one. Then Bug Log it. A found typo is worth more than a finished worksheet. |
| Somebody teaches masks because the grid is right there | `rain[rain > 100]` is very fun and one keystroke away | Hold the line. Today has one new idea and it is a direction. A student who meets masks and axes in the same hour will spend next week unable to tell which of two new things broke. |
| The averages get written down with no units | Because the array has no units in it | Say it: *"28.5 what?"* Millimetres. Nothing in the array knows that. Nothing in the array knows these are cities, either. This is Week 17's cost, still being paid, and it is what Week 21 starts to fix. |
| A fast student asks about `axis=-1` after reading online | It is everywhere on the internet | One sentence: "it means the last direction, which for a table is axis 1." Then park it. Do not build anything on it today. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** `.sum` entirely. `.mean` in two directions makes the whole point, and the corner check can be a demonstration you narrate.

**Cut:** the column hand-check. Do the row only — tracing a row with a finger is far easier than tracing a column — and do the column as a demonstration.

**Cut:** the grid to **three cities and four months.** Twelve numbers. Chennai, Pune, Shimla; Jan to Apr. Row 1 hand-checks as `2 + 4 + 10 + 20 = 36`, then `36 / 4 = 9.0`. Column 1 hand-checks as `10 + 4 + 70 = 84`, then `84 / 3 = 28.0`. Every idea survives and the arithmetic stops being the obstacle.

**Reteach — with the two margins and nothing else.** This is the whole lesson and it needs no computer:

1. Grid on paper. Empty margin down the side, empty margin along the bottom.
2. *"How many boxes in the side margin?"* Four. *"Why?"* Four cities.
3. Fill them: add the row, divide by six.
4. *"How many in the bottom margin?"* Six. *"Why?"* Six months.
5. Fill them: add the column, divide by four.
6. Now label the margins in their own handwriting: **side margin = `axis=1`** (it ate the columns), **bottom margin = `axis=0`** (it ate the rows).

A student who leaves the room able to say *"four cities means four answers, and to get them I have to eat the six months"* has succeeded, whether or not a line of Python ran.

**The copy-this-exactly scaffold.** One file, six lines. This runs:

```python
import numpy as np

rain = np.array([[25, 10, 5],
                 [2, 4, 10]])

print(rain.mean(axis=0))     # eats the 2 rows -> 3 answers
print(rain.mean(axis=1))     # eats the 3 columns -> 2 answers
```

```text
[13.5  7.   7.5]
[13.33333333  5.33333333]
```

Then two questions, out loud, and nothing else: **"how many numbers came out of the first line, and how many rows are there? And the second line?"** Three out of a two-row grid; two out of a three-column grid. **The count is the objective.** A student who can answer those two has objectives 3 and 4.

**One thing you must not cut:** predicting the count before pressing run. If the whole lesson collapses to one sentence, make it *"say how many answers you expect, then count them."*

### If the student is flying

None of these need syntax from a later week.

1. **The second grid** (Variation-harder 1): three friends, five days, both directions, both counts, one hand-check. A different shape forces the counts to be re-derived rather than remembered.
2. **Predict all ten numbers**, not just the counts (Variation-harder 3), then run. Hard, slow, and extremely good for them.
3. **The average-of-averages trap** (Variation-harder 5). `rain.sum(axis=1).mean()` is 427.5 and `rain.mean()` is 71.25. Ask them to explain the difference in one sentence before you do. This is a genuinely deep idea and a strong 12-year-old can get it.
4. **Break the grid on purpose.** Change one number in the code but not on the paper margins, compare the printed `sum(axis=1)` and `sum(axis=0)` with the paper totals, and find the changed cell *using only the mismatching row and column totals*. (The code's three corner-check totals will still agree with each other, which is itself worth noticing.) This is real debugging and it is very satisfying.
5. **The missing-year question** (Variation-harder 6). *"Whose January is this?"* No right answer; excellent argument.
6. **Two grids, same numbers, different shape.** Have them type the same twenty-four numbers as `(6, 4)` instead of `(4, 6)` and run both axis lines on it. The answers are completely different and nothing crashes. Then the question: *"which of these two grids is the rainfall data?"* (Only the one whose shape matches the labels. **Shape is meaning** — Week 17's idea, arriving with teeth.)

### If the student won't engage today

**Close the laptop. Graph paper, pencil, calculator.**

Draw a small grid — three by four is plenty — and fill it with something they actually care about. Goals scored by three players over four matches. Minutes of screen time for three days across four apps. Money spent by three people on four days. **Let them choose the thing and let them make up the numbers.**

Then two questions, and nothing else:

> **"Give me one number for each player."** *(Let them work out that they have to add along the row. Three answers.)*
>
> **"Now give me one number for each match."** *(Add down the column. Four answers.)*

Then one more, quietly:

> **"How did you know it was three answers the first time and four the second?"**

Because there are three players and four matches. That is the entire lesson, delivered in ten minutes with a pencil, and it is objectives 3, 4 and 5. The typing survives to next week, which is a lab and needs it anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the count (spoken, 45 seconds)**

> "I have an array with shape `(5, 3)`. I write `.mean(axis=0)`. **How many numbers come out?**"

*Good answer:* "Three. Axis 0 is the rows, naming it eats the five rows, and what's left is three columns."

**What to catch:** "five" means they think naming an axis *keeps* it. Do not correct with the rule — draw it. Five arrows down, three boxes underneath.

**Check 2 — the direction, from the question (spoken, 60 seconds)**

> "Four cities down, six months across. **I want to know which month was wettest. Which axis, and why?**"

*Good answer:* "axis=0. Months are the columns, and I want to keep the columns, so I have to eat the rows — and the rows are axis 0. I should get six answers."

**Full marks needs the count.** "axis=0" on its own is a level-3 answer; push once: *"and how many numbers should come back?"*

**Check 3 — the silent bug (spoken, 90 seconds)**

> "Somebody wanted one average per month and got back **four** numbers. Nothing crashed. **What did they do, and how would you have caught it?**"

*Good answer:* "They used `axis=1` instead of `axis=0`, so it averaged per city. I'd catch it by counting: six months should give six numbers, and four isn't six. And I'd hand-check one row on paper."

**What to catch:** a student who says "Python would have told them" has not absorbed the week. Go back to the live-code output and read it out loud again: four numbers, no traceback, no warning.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot point at `rain[1, 2]` without help. Reads "row 1" as the first row. Cannot say what `axis` is for. |
| **2 — Emerging** | Indexes one cell correctly when reminded to count from zero. Uses an axis when told which one. Reads the count off the screen but does not predict it. |
| **3 — Secure** | Writes `arr[1, 2]`, `arr[:, 0]` and `arr[1, :]` unaided. Chooses the axis from the question and **says the count before running.** Hand-checks one row on paper. Says *"the axis you name gets eaten."* **This is the target.** |
| **4 — Strong** | Catches a wrong axis from the count alone, without being prompted. Explains why the wrong axis produces a *plausible* answer, not a silly one. Uses the corner check. Can go from "which month was wettest" to `axis=0` out loud, deriving it rather than recalling it. |
| **5 — Exceptional** | Says unprompted that the count check is a check that keeps running after you stop paying attention. Explains the average-of-averages trap: `rain.sum(axis=1).mean()` is not `rain.mean()`. Notices that the labels are the only thing that says which direction is which, and that nothing in the array knows — connecting straight to Week 17's cost and Week 21's fix. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, and the marking is mostly in two places.
>
> **First, page 19.4 — the rainfall grid, properly.** Type the grid, print the shape, and then print **both** directions: one mean per city and one mean per month. **Under every axis line, print the count.** If you print six numbers and label them 'per city', I'm going to circle it, because there aren't six cities.
>
> **Second — and this is the part I'm actually marking — page 19.3's hand-check, in pen, before you run anything.** Row 1 by hand. Six numbers added up, divided by six. Write the answer down. Then, and only then, run the code and see if it agrees. If you do it the other way round you have learned nothing and I will be able to tell, because your handwriting will be too tidy.
>
> **Third, page 19.5 — a grid that isn't mine.** Three friends, five days, step counts. Same two directions. **But the counts are different now** — three and five, not four and six — so you can't copy yesterday's numbers. Hand-check one row of it too.
>
> **Fourth, page 19.6 — one sentence.** How does the number of answers tell you which axis you used? One sentence, your own words, no code in it.
>
> **And one last line at the bottom of 19.6.** Run the per-month line with the wrong axis on purpose. Write down what came out and what didn't happen."

**Workbook pages:** 19.1, 19.2, 19.3 in class · **19.4, 19.5, 19.6** at home.

**Expected time:** 15 min on 19.4 · 10 min on the hand-checks in pen · 20 min on 19.5's new grid · 10 min on 19.6's sentence and the wrong-axis experiment. **About 55 minutes.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — is the count printed under every axis line?** Not once at the bottom: under each. **Two — is the hand-check in pen, and does it show the working?** `162 / 6 = 27.0` with the six numbers added out, not just `27`. **Three — does 19.6's sentence mention the labels?** The good sentence is something like *"I know how many answers to expect because I know how many cities I typed, so if the count is different I used the wrong axis."* A sentence that only says "axis 0 is rows" has not understood the week. The count is the check, and the count comes from the labels.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 19.1 — Point at the cell (paper, no computer)

*The grid, for reference. Row and column numbers are Python's, so they start at 0.*

```text
             col 0  col 1  col 2  col 3  col 4  col 5
              Jan    Feb    Mar    Apr    May    Jun
row 0 Chennai   25     10      5     15     40     55
row 1 Pune       2      4     10     20     36     90
row 2 Shimla    65     70     60     45     51    105
row 3 Kochi     22     26     54    120    300    480
```

**(a) What is `rain[0, 0]`?** `25` — Chennai, January. The top-left cell.

**(b) What is `rain[1, 2]`?** `10` — Pune, March. **Not** Chennai/February.

**(c) What is `rain[2, 4]`?** `51` — Shimla, May.

**(d) What is `rain[3, 5]`?** `480` — Kochi, June. The bottom-right cell, and the wettest number on the page.

**(e) Write the index pair for Kochi in April.** `rain[3, 3]` → `120`. Kochi is the fourth city, so row 3; April is the fourth month, so column 3.

**(f) Write the index pair for Chennai in June.** `rain[0, 5]` → `55`.

**(g) What is `rain[1, :]`?** Pune's whole row: `[ 2  4 10 20 36 90]`. Six numbers.

**(h) What is `rain[:, 0]`?** January for every city: `[25  2 65 22]`. Four numbers. **And it prints as a row**, even though it is a column, because four numbers with one direction have shape `(4,)`.

**(i) Somebody writes `rain[1, 6]` to get June for Pune. What happens, and why?**
`IndexError: index 6 is out of bounds for axis 1 with size 6`. There are six columns and they are numbered 0 to 5, so June is column **5**. The message also says *which* direction was overrun — `axis 1`, the columns.

**(j) In one sentence: why is "row 1" a dangerous phrase?**
Because in English row 1 is the first row and in Python `rain[1]` is the **second** row — rows are numbered from 0. Say "row index 1" or point at the cell.

### Page 19.2 — How many answers? (predict in pen, before running)

*For each line, how many numbers come out?*

| # | The line | How many | Why |
|---|---|---|---|
| (a) | `rain.shape` | **2** | A pair: rows then columns. `(4, 6)`. |
| (b) | `rain[1, 2]` | **1** | One cell. `10`. |
| (c) | `rain[1, :]` | **6** | One row, and a row is six months long. |
| (d) | `rain[:, 0]` | **4** | One column, and a column is four cities tall. |
| (e) | `rain.mean()` | **1** | No axis named, so nothing is left standing: one number for the whole grid. `71.25`. |
| (f) | `rain.mean(axis=0)` | **6** | Names the rows, so the four rows are eaten; six columns survive. **One per month.** |
| (g) | `rain.mean(axis=1)` | **4** | Names the columns, so the six columns are eaten; four rows survive. **One per city.** |
| (h) | `rain.sum(axis=0)` | **6** | Same direction as (f). `.sum` and `.mean` behave identically. |

Real output, so you can mark against it:

```text
shape : (4, 6)
rain[1, 2] = 10
rain[1, :] = [ 2  4 10 20 36 90]
rain[:, 0] = [25  2 65 22]
per month : [ 28.5   27.5   32.25  50.   106.75 182.5 ]
per city  : [ 25.  27.  66. 167.]
month totals: [114 110 129 200 427 730]
whole thing mean: 71.25
```

**19.2(i) Which two of these eight give the same count as each other, but answer different questions?**
**(c) and (f)** both give six numbers. (c) is *Pune's six months* — real rainfall, one city. (f) is *six monthly averages* — one number per month, across all four cities. **Same count, completely different meaning**, which is exactly why counting is a *first* check and not the only one.

*(Also acceptable: (d) and (g) both give four. One is January's four real values; the other is four city averages.)*

**19.2(j) You wanted one answer per month and got four numbers. What went wrong?**
The axis. `axis=1` was used instead of `axis=0`, so the columns were eaten and the answers came out one per **city**. Nothing crashed, because averaging per city is a perfectly legal thing to ask for.

### Page 19.3 — The hand-check (in pen, before any code)

**(a) Row 1. Which city is it?**
**Pune.** Row 0 is Chennai, so row 1 is the second city.

**(b) Add row 1 up, showing the working.**

```text
2 + 4 = 6
6 + 10 = 16
16 + 20 = 36
36 + 36 = 72
72 + 90 = 162
```

Total: **162**.

**(c) What do you divide by, and why?**
**Six**, because there are six months in the row.

**(d) The mean of row 1.**
`162 / 6 = ` **27.0**

**(e) Column 1. Which month is it?**
**February.** Column 0 is January.

**(f) Add column 1 up, showing the working.**

```text
10 + 4 = 14
14 + 70 = 84
84 + 26 = 110
```

Total: **110**.

**(g) What do you divide by, and why?**
**Four**, because there are four cities in the column.

**(h) The mean of column 1.**
`110 / 4 = ` **27.5**

**(i) Now run the code. Do both match?**

```text
row 1 by hand : 162 / 6 = 27.0
row 1 by code : 162 / 6 = 27.0
col 1 by hand : 110 / 4 = 27.5
col 1 by code : 110 / 4 = 27.5
```

Yes. **Mark the working, not the answer** — a student who wrote `27.0` with no addition shown has not hand-checked anything.

**(j) 27.0 and 27.5 are nearly the same number. Why is that worth noticing?**
Because if you had mixed the two up, the answer would still have *looked* fine. A wrong answer that is wildly wrong is easy to catch. A wrong answer that is nearly right is the dangerous kind — and it is why the **count** matters more than the look of the number. Four answers can never be six answers, however plausible they are.

**(k) What will you do if the pencil and the code disagree?**
Find out which one is wrong. Neither is automatically right. Check the addition, then check that the grid you typed matches the grid on the paper, then check the axis and the count. *(Any answer that refuses to assume the computer is right gets full marks.)*

### Page 19.4 — The rainfall grid, both directions

Complete working code, actually run:

```python
"""hw19.py - the rainfall grid, both directions, with the count printed every time."""

import numpy as np

rain = np.array([
    [ 25,  10,   5,  15,  40,  55],         # row 0 - Chennai
    [  2,   4,  10,  20,  36,  90],         # row 1 - Pune
    [ 65,  70,  60,  45,  51, 105],         # row 2 - Shimla
    [ 22,  26,  54, 120, 300, 480],         # row 3 - Kochi
])
cities = np.array(["Chennai", "Pune", "Shimla", "Kochi"])
months = np.array(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

# --- 1. the two facts, before anything else --------------------------------
print("shape:", rain.shape, " dtype:", rain.dtype)
print("cities:", len(cities), " months:", len(months))

# --- 2. per city: one answer per ROW, so eat the columns: axis=1 -----------
city_mean = rain.mean(axis=1)
print()
print("PER CITY  (axis=1) ->", city_mean.shape, "answers")
print("City      Total   Mean")
print("-" * 23)
for i in range(len(cities)):
    print(f"{cities[i]:<9} {rain.sum(axis=1)[i]:>5}  {city_mean[i]:>6.2f}")

# --- 3. per month: one answer per COLUMN, so eat the rows: axis=0 ---------
month_mean = rain.mean(axis=0)
print()
print("PER MONTH (axis=0) ->", month_mean.shape, "answers")
print("Month  Total   Mean")
print("-" * 20)
for i in range(len(months)):
    print(f"{months[i]:<6} {rain.sum(axis=0)[i]:>5}  {month_mean[i]:>6.2f}")

# --- 4. the hand-check ----------------------------------------------------
# Row 1 is PUNE (row 0 is Chennai). By pencil:
#   2 + 4 + 10 + 20 + 36 + 90 = 162, and 162 / 6 = 27.0
print()
print("row 1 by hand : 162 / 6 = 27.0")
print("row 1 by code :", rain[1, :].sum(), "/ 6 =", rain.mean(axis=1)[1])

# Column 1 is FEBRUARY (column 0 is January). By pencil:
#   10 + 4 + 70 + 26 = 110, and 110 / 4 = 27.5
print("col 1 by hand : 110 / 4 = 27.5")
print("col 1 by code :", rain[:, 1].sum(), "/ 4 =", rain.mean(axis=0)[1])

# --- 5. the cross-check ---------------------------------------------------
print()
print("city totals add to :", rain.sum(axis=1).sum())
print("month totals add to:", rain.sum(axis=0).sum())
print("whole grid adds to :", rain.sum())
```

Real output:

```text
shape: (4, 6)  dtype: int64
cities: 4  months: 6

PER CITY  (axis=1) -> (4,) answers
City      Total   Mean
-----------------------
Chennai     150   25.00
Pune        162   27.00
Shimla      396   66.00
Kochi      1002  167.00

PER MONTH (axis=0) -> (6,) answers
Month  Total   Mean
--------------------
Jan      114   28.50
Feb      110   27.50
Mar      129   32.25
Apr      200   50.00
May      427  106.75
Jun      730  182.50

row 1 by hand : 162 / 6 = 27.0
row 1 by code : 162 / 6 = 27.0
col 1 by hand : 110 / 4 = 27.5
col 1 by code : 110 / 4 = 27.5

city totals add to : 1710
month totals add to: 1710
whole grid adds to : 1710
```

**Mark:** the shape line is present; **`(4,)` appears next to the per-city block and `(6,)` next to the per-month block**; the two hand-check lines agree; the three totals all read 1710. The `for` loops are for printing only — no arithmetic happens inside them.

**19.4(a) Which is the wettest city, and which is the wettest month?**
Wettest city: **Kochi**, mean 167.0 mm, total 1002. Wettest month: **June**, mean 182.5 mm, total 730.

**19.4(b) The wettest month's mean (182.5) is bigger than the wettest city's mean (167.0). Is that a contradiction?**
No, and it is worth thinking about. They are averages of different-sized groups. 182.5 is June averaged over **four** cities — and Kochi's 480 mm of June rain pulls it right up. 167.0 is Kochi averaged over **six** months, including a 22 mm January that pulls it down. Different groups, different sizes, different answers. Neither one is "the average rainfall".

**19.4(c) Why does the corner check work?**
Because all three routes add up the **same twenty-four numbers**, just in different orders. Adding along the rows first, or down the columns first, or all at once, cannot change the total — so in numpy they always agree. That is why the check cannot catch a wrong axis or a mistyped number; it confirms the arithmetic and the idea, and on paper it catches slips in your own adding-up.

### Page 19.5 — A different grid: three friends, five days

*Three friends down, five days across. Step counts.*

Complete working code, actually run:

```python
"""steps.py - a second grid: 3 friends DOWN, 5 days ACROSS."""

import numpy as np

steps = np.array([
    [ 8000,  6000,  9000,  7500,  4000],    # row 0 - Ali
    [12000, 11000,  9000, 13500,  9500],    # row 1 - Bea
    [ 4000,  4000,  6000,  3000,  4500],    # row 2 - Cy
])
friends = np.array(["Ali", "Bea", "Cy"])
days = np.array(["Mon", "Tue", "Wed", "Thu", "Fri"])

print("shape:", steps.shape)
print("steps[2, 3] =", steps[2, 3])
print("steps[:, 4] =", steps[:, 4])
print("steps[0, :] =", steps[0, :])
print("per day  (axis=0):", steps.mean(axis=0), "->", steps.mean(axis=0).shape)
print("per friend (axis=1):", steps.mean(axis=1), "->", steps.mean(axis=1).shape)
print("day totals   :", steps.sum(axis=0))
print("friend totals:", steps.sum(axis=1))
print("cross-check  :", steps.sum(axis=0).sum(), steps.sum(axis=1).sum(), steps.sum())
```

Real output:

```text
shape: (3, 5)
steps[2, 3] = 3000
steps[:, 4] = [4000 9500 4500]
steps[0, :] = [8000 6000 9000 7500 4000]
per day  (axis=0): [8000. 7000. 8000. 8000. 6000.] -> (5,)
per friend (axis=1): [ 6900. 11000.  4300.] -> (3,)
day totals   : [24000 21000 24000 24000 18000]
friend totals: [34500 55000 21500]
cross-check  : 111000 111000 111000
```

**19.5(a) Before running: how many numbers from `axis=0`, and how many from `axis=1`?**
`axis=0` eats the three rows, so **five** answers — one per day. `axis=1` eats the five columns, so **three** answers — one per friend. **Note that both counts changed from the rainfall grid.** A student who wrote 6 and 4 has copied yesterday's answer instead of thinking.

**19.5(b) Hand-check row 1. Show the working.**
Row 1 is **Bea** (row 0 is Ali).

```text
12000 + 11000 = 23000
23000 + 9000  = 32000
32000 + 13500 = 45500
45500 + 9500  = 55000
```

`55000 / 5 = ` **11000.0**. And the code says `11000.` in the second slot. ✔

**19.5(c) Hand-check column 1.**
Column 1 is **Tuesday** (column 0 is Monday). `6000 + 11000 + 4000 = 21000`, and `21000 / 3 = ` **7000.0**. ✔ Divide by **three**, because there are three friends.

**19.5(d) What is `steps[2, 3]`, in words?**
**Cy on Thursday: 3000 steps.** Row 2 is the third friend; column 3 is the fourth day.

**19.5(e) Which friend walked most, and which day was quietest?**
Bea walked most: 55000 steps, mean 11000. Friday was quietest: 18000 steps total, mean 6000.

**19.5(f) The corner check.**
`24000 + 21000 + 24000 + 24000 + 18000 = 111000` and `34500 + 55000 + 21500 = 111000`. Both agree with `steps.sum()`. ✔

**19.5(g) Why are all five day-averages whole numbers here, when the rainfall ones weren't?**
Because every column of this grid happens to add up to a multiple of three, and there are three friends. It is a property of these particular numbers, not of `axis=0`. **A tidy answer is not evidence of a correct answer.**

### Page 19.6 — The count sentence, and the wrong-axis experiment

**(a) One sentence: how does the number of answers tell you which axis you used?**

Model answers, any of which gets full marks:

> *"The axis I name gets eaten, so the number of answers is the size of the direction that's left — six months means axis 0, four cities means axis 1."*

> *"I know how many cities and months I typed, so I know how many answers to expect. If the count is different, I used the wrong axis."*

**What to mark:** the sentence must connect the count to something the student **already knows** — the number of labels they typed. A sentence that only says "axis 0 is rows" has restated a fact and answered nothing.

**(b) The experiment. Run the per-month line with the wrong axis on purpose. What came out?**

```python
print("per month, wrong axis:", rain.mean(axis=1))
print("per month, right axis:", rain.mean(axis=0))
```

```text
per month, wrong axis: [ 25.  27.  66. 167.]
per month, right axis: [ 28.5   27.5   32.25  50.   106.75 182.5 ]
```

**(c) What didn't happen?**
**No error. No warning. No traceback.** Python printed four tidy numbers and stopped. There was nothing on the screen to suggest anything was wrong.

**(d) What is 25.0 actually the average of?**
**Chennai, across all six months.** It is a correct answer to a question nobody asked.

**(e) Why is a wrong answer of 25.0 more dangerous than a wrong answer of 25000?**
Because 25 millimetres is a **believable** amount of rain, so nothing about it makes you look twice. 25000 mm would be obviously absurd and you would catch it instantly. **Plausible wrong answers are the dangerous ones** — which is why you count the answers instead of eyeballing them.

**(f) Write your Bug Log entry for this one.**

Model:

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| Four numbers instead of six. No error at all. | numpy averaged the direction I named away, which was the wrong one. | `axis=1` when the question was about columns. | `axis=0`. And print the count under every axis line, so it cannot happen quietly. |

### Answers to every question posed in the lesson

- *"How many numbers is your answer going to be?"* → It depends on the question: one for the whole table, four per city, six per month.
- *"Why four city answers and six month answers?"* → Because there are four cities and six months. The count of answers is the count of labels.
- *"Is 71.25 wrong?"* → No. It is a correct average of something nobody asked about. Right and useless.
- *"What is axis 0?"* → The rows — the first number in the shape.
- *"I write `axis=1`. What gets eaten?"* → The columns. So the answers are one per row: one per city.
- *"I want one number per month. Which axis?"* → 0. Months are columns; to keep the columns you have to eat the rows, and rows are axis 0.
- *"What does `rain[1, 2]` point at?"* → Pune, March. 10 mm. Row 1 is the second row.
- *"What does `rain[2, 4]` point at?"* → Shimla, May. 51 mm.
- *"What does the colon mean?"* → Every one of them, in that one direction.
- *"How many numbers will `rain[:, 0]` give?"* → Four, one per city — and it prints sideways.
- *"How many will `rain.sum(axis=1)` give?"* → Four.
- *"Will `rain[1, 6]` work?"* → No. `IndexError: index 6 is out of bounds for axis 1 with size 6`. June is column 5.
- *"Six columns, so the last one is number...?"* → Five.
- *"How many numbers should come out of the per-month line?"* → Six.
- *"How many are there? How many months are there?"* → Four, and six. That gap is the bug.
- *"What did it actually give us?"* → The averages per city.
- *"Why did it happen?"* → The axis you name is the axis that gets eaten. Naming axis 1 ate the columns.
- *"Last three lines — what happens?"* → 1710, three times.
- *"Why divide row 1 by six?"* → Six months in the row.
- *"Why divide column 1 by four?"* → Four cities in the column.
- *"Which of the two ones in `rain.mean(axis=1)[1]` would you change to get Shimla?"* → The second one: `[2]`.
- *"Which route would you use for all four totals?"* → `rain.sum(axis=1)` — it does all four at once.
- *"You took a column and it printed as a row. Is that wrong?"* → No. Four numbers, shape `(4,)`. Being upright is not something the array keeps.

---

## 🔮 Next Week Preview

Next week is a lab, and it is the one where the student builds something that looks like a real tool. **The Vectorized Gradebook:** ten students down, five tests across, and eight questions answered with **zero `for` loops doing any arithmetic anywhere in the file.** The new idea is the **boolean mask** — write `scores > 50` and you get back an array of `True` and `False`, exactly the same shape as the scores, one answer per cell. The important move is to *look at the mask before using it*: print it, put a highlighter over the printed grid, and see that it is a thing in its own right rather than a step on the way to a filter. Then `scores[mask]` pulls out only the values you want — and the answer comes back **shorter than the question**, which is the first surprise. This week's axis work does all the heavy lifting: `mask.sum(axis=1)` counts passes per student and `mask.sum(axis=0)` counts passes per test, and both add up to `mask.sum()` whichever way you go, so the check that catches a wrong axis is still the count against the labels.

And there is a sting, and it is the exact sibling of this week's silent bug. One score gets typed as **950** instead of 95. Nothing crashes. The per-student mean for that one student goes daft in a way you might notice — but the **0-to-1 normalization silently squashes everybody else into the bottom twelfth of the scale**, so every other student's score becomes a number between 0.01 and 0.08 and the whole thing still looks like a tidy grid of decimals. The check that catches it is a range check — *no test score can be above 100* — and it is one line with a mask in it.

**Prep early:** three things. **Print the ten-by-five score grid on paper** and find a highlighter, because the mask lands twice as hard when it is drawn on top of the numbers by hand. **Keep this week's rainfall grid on the table**, because next week opens by asking for one mean per student and one mean per test on a bigger grid, and the student should recognise it as the same question with different labels. And **read the hand-check pages from tonight's homework before the lesson**, because next week asks for a normalization done by hand for one row, and a student who cut corners on this week's pencil work will cut them again — better to know that in advance than to discover it at minute fifty.

---

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Student Guide](../student-guide/week-19.md) · [Workbook](../workbook/week-19.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
