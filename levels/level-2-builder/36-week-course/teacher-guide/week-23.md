# Week 23 — Holes, Text-That-Should-Be-Numbers, and Duplicates

[⬅ Week 22](week-22.md) · [Course Home](../README.md) · [Week 24 ➡](week-24.md) · [Student Guide](../student-guide/week-23.md) · [Workbook](../workbook/week-23.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the four ways real data arrives broken, and the log that keeps you honest |
| **Big idea** | Real data arrives broken in **four predictable ways**, and each one has a named fix. Every fix is a **decision**, so it gets written down with a reason. |
| **New vocabulary** | missing value · isna · fillna · astype · cleaning log |
| **New syntax** | `pd.read_csv()` / `df.to_csv()` · `df.isna().sum()` · `df["c"].fillna(v)` · `df["c"].astype(int)` |
| **Materials** | Printed workbook (all sections, Warm-Up to Self-Check) · **a large sheet of paper ruled into two columns headed WHAT I DID and WHY I DID IT** — this is the cleaning log and it must be on paper · a pen · the Bug Log |
| **Tech needed** | Laptop with Python 3 and pandas. **`club_raw.csv` must exist in the student's folder before class** — the prep script writes it. A paper version exists; see Prep. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |

> **⚠️ Watch out:** the lesson's real content is an **argument** with no right answer — should three unknown ages be filled with the median or should those rows be dropped? Both are defensible, they give answers five whole marks apart, and the student must pick one **and write down why**. If you settle the argument for them, you have taught a keystroke instead of a habit.

> **💡 Try this:** one helper appears this week that is not in the syntax table above — `pd.to_numeric(column, errors="coerce")`. It is unavoidable: `astype(int)` cannot get past the word `unknown` on its own, and `to_numeric` is the step that turns `unknown` into a countable hole. Treat it as the doorway to `astype`, not as a fifth thing to memorise.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Load a CSV into a DataFrame** with `pd.read_csv` and **write one back out** with `df.to_csv(..., index=False)`.
2. **Count the missing values in every column** with `df.isna().sum()` and say the number out loud.
3. **Fill a hole** with `fillna`, and **record in writing what they filled it with and why**.
4. **Force a column to the right type** with `astype(int)`, and explain what was blocking it.
5. **Name all four ways data arrives broken**, from memory, without the book open.

Observable evidence: `df.info()` read aloud with `object` correctly identified in the `age` column; the sentence *"three rows say `unknown`, so pandas treats the whole column as writing"*; a numbered cleaning log on paper with **a reason on every line**; and a saved `club_clean.csv` that reads back with `age` as `int64`.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**Read this once, slowly — about 25 minutes. It teaches you the Python and the judgement.** You do not need to have programmed before.

### 1. Why this week exists, and why it is the most important week of the term

Everything the student has done so far used a table **they typed themselves**. So every age was a number, every house was spelled the same way every time, and no cell was empty. That is not what data is like.

Real data is collected by tired people on paper forms, typed in by somebody else, and exported by a program that made its own decisions. It arrives with holes in it. It arrives with the word `unknown` sitting in a column of numbers. It arrives with the same child entered twice because somebody scrolled and lost their place.

**The honest fact about data work, and it is worth telling a 12-year-old plainly: you will spend more time cleaning the table than asking it questions.** That is not a failure of your skills. That is the job.

And the deeper point, which is the one this week is really for: **every repair changes the answer.** If you fill three missing ages with 13, then every later calculation treats three children as 13 years old — including the calculation you were trying to make. That is not cheating and it is not wrong. It is what filling *means*. But it has to be **written down**, or in six weeks nobody, including the student, will know whether the number they are reporting came from the world or from a repair.

### 2. The four kinds of broken — the spine of the whole week

There are four, they cover almost everything, and the student must be able to name all four from memory by the end of the lesson.

| # | The problem | How you spot it | The named fix | Which week |
|---|---|---|---|---|
| 1 | **A hole** — nobody filled that cell in | `df.isna().sum()` is not zero | `fillna(value)` or `dropna()` | **This week** |
| 2 | **Text pretending to be numbers** — one word turns a whole column into writing | `df.info()` says `object` where you expected a number | `to_numeric(..., errors="coerce")` then `astype(int)` | **This week** |
| 3 | **The same row twice** | `df.duplicated().sum()` is not zero | `drop_duplicates()` | Next week |
| 4 | **Four spellings of one word** | `df["col"].value_counts()` shows `Blue`, `blue`, `BLUE` | `.str.strip().str.title()` | Next week |

**This week fixes the first two and only names the last two.** That split is deliberate: naming all four is a memory job the student can do today, and fixing all four in one 70-minute lesson is not. Next week fixes 3 and 4 on a bigger table.

![Real data arrives broken in four ways](../figures/fig-w23-1-four-kinds-of-broken.svg)
*Figure 23.1 — Week 23 fixes the first two. Week 24 fixes the last two. Naming all four is this week's job.*

### 3. Reading a file, line by line

```python
import pandas as pd                        # the pandas toolbox, nicknamed pd

raw = pd.read_csv("club_raw.csv")           # read the file into a table
print(raw)                                  # show it
```

- `pd.read_csv("club_raw.csv")` — open that file, read the first line as the **column names**, and read every line after it as a row. CSV means "comma-separated values": a plain text file where commas mark the edges of the cells. You could open it in a text editor and read it with your eyes, and you should, once.
- `raw = ...` — the name `raw` is a promise to yourself: *this is the untouched original and I will not modify it.* Every clean-up happens on a copy. That habit costs nothing and saves whole afternoons.
- The file must be **in the same folder** as the Python file, or `read_csv` will not find it. That is the single most common failure in this lesson and its error message is in the Debugging Clinic.

Here is our table. **Every example in this file uses it**, so if you run the two lines above now, you can follow along with everything below — the only exception is the four-value `hours` demo in section 6, which stands on its own.

```text
          name      age  house   club  hours  score
0   Aarav Shah       13    red  chess    3.5     72
1     Bela Roy       14    Red  music    5.0     90
2      Chen Wu  unknown   BLUE  chess    2.0     55
3   Divya Nair       13  blue     art    NaN     83
4    Emeka Obi  unknown  Green  music    4.5     61
5   Farah Aziz       12  green  chess    6.0     95
6   Gita Menon       13   Blue    art    1.5     78
7   Hugo Silva       14    RED  music    0.5     45
8     Ivy Chen       12   Blue  chess    4.0     88
9   Jai Kapoor       13  green    art    3.5     67
10    Bela Roy       14    Red  music    5.0     90
11    Kira Das  unknown    Red  chess    3.0     74
```

**Twelve rows, and all four problems are visible in that printout if you know where to look.** Point at each one before you type anything:

- `NaN` in row 3's `hours` — a **hole**.
- `unknown` three times in `age` — **text pretending to be numbers**.
- Rows 1 and 10, both `Bela Roy`, identical — **the same row twice**.
- `red`, `Red`, `RED`, `BLUE`, `blue `, ` Blue`, `Blue`, `green`, `Green` — **nine spellings of three houses**.

### 4. `info()` — the four lines that matter

```python
raw.info()
```

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 6 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   name    12 non-null     object 
 1   age     12 non-null     object 
 2   house   12 non-null     object 
 3   club    12 non-null     object 
 4   hours   11 non-null     float64
 5   score   12 non-null     int64  
dtypes: float64(1), int64(1), object(4)
memory usage: 704.0+ bytes
```

Note it is `raw.info()` with round brackets and **no** `print` — `info` prints for itself.

Read it in this order, out loud, every time:

1. **`12 entries`** — twelve rows. Does that match what you expected? Here, yes.
2. **The `Non-Null Count` column.** `Non-null` means "has something in it". `hours` says **11 non-null out of 12** — one hole. Everything else says 12.
3. **The `Dtype` column.** This is where the lesson lives. `score` is `int64`, whole numbers — fine. `hours` is `float64`, decimals — fine. And **`age` is `object`.**
4. **`object` is pandas's word for "writing", or "a mixture I have given up describing".**

> **The sentence the student has to be able to say: "`age` is `object`, so pandas thinks the ages are writing, not numbers."**

And then the question that unlocks everything: **why?** Nine of the twelve ages are perfectly good numbers. But three of them say `unknown`, and `unknown` is a word. A column in pandas has to be **one kind of thing all the way down**. One word forces the whole column to be writing.

**The analogy to use, and it lands every time:** it is a queue at a shop till marked *"basket only"*. One person with a trolley and the whole queue has to be treated as a trolley queue. One word in a column of numbers and the whole column is words.

### 5. `isna().sum()` — counting the holes, and the trap in it

> **missing value** — a cell where nobody put anything. Pandas prints it as `NaN`.

> **`NaN`** — short for "Not a Number". It is pandas's marker for *nothing was recorded here*.

```python
print(raw.isna().sum())
```

```text
name     0
age      0
house    0
club     0
hours    1
score    0
dtype: int64
```

Read it inside out:

- `raw.isna()` — go through every single cell and ask "is this one missing?" You get back a table the same shape as the original, full of `True` and `False`. You can print it; it is worth doing once.
- `.sum()` — add up each column. `True` counts as 1 and `False` counts as 0, so the sum is *how many holes in that column*.

**And now the trap, which is the whole point of running this before the type fix.** Look at `age`: **zero missing.** But three rows say `unknown`! Are those not missing?

They are missing in the real world and not missing to pandas, because **`"unknown"` is a perfectly good piece of writing.** Something is in the cell. Pandas is not lying; it is answering exactly the question you asked.

> **The rule, and put it on the board: `isna()` finds *empty* cells. It does not find cells that contain a word meaning "empty".**

That is why you check `info()` **and** `isna()`. `info()` catches the disguised holes by showing you `object` where you expected a number. `isna()` catches the honest ones.

### 6. `NaN` is not zero, and this is worth three minutes on its own

Get this wrong and every average the student computes for the rest of the course is wrong. Type this tiny four-value example out and run it in front of them:

```python
import pandas as pd

hours = pd.Series([3.5, 5.0, None, 4.5])   # a single column with a hole in it
print(hours)
print("mean:", hours.mean())
```

```text
0    3.5
1    5.0
2    NaN
3    4.5
dtype: float64
mean: 4.333333333333333
```

**3.5 + 5.0 + 4.5 = 13.0, and 13.0 ÷ 3 = 4.333.** Pandas **stepped over the hole**: it added the three real numbers and divided by **three**, not four. That is almost always the sensible thing to do, and it is silent.

Now what would happen if `NaN` were zero?

```python
print("if the hole were 0:", hours.fillna(0).mean())
```

```text
if the hole were 0: 3.25
```

**4.33 against 3.25.** Same four cells, and filling with zero invented a club member who did nothing. Say it in these words:

> **`NaN` is not `0`. `NaN` is not `""`. `NaN` means *nobody told us*. Zero means *we asked and the answer was none*. Those are different facts and they give different answers.**

And the other half of the story — the one command that refuses to step over a hole:

```python
print(hours.astype(int))
```

```text
IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer
```

Pandas will average around a hole quietly, but it will **not** pretend a hole is a whole number. That refusal is a gift, and it gives you the rule that orders the whole repair:

> **Deal with the hole first. Then change the type. Never the other way round.**

![A hole is a void, not a zero](../figures/fig-w23-2-nan-hole-in-the-grid.svg)
*Figure 23.2 — pandas will average around a hole quietly. It will not pretend a hole is a whole number.*

### 7. The type repair, in two steps, and why the count goes UP

**Step one — try it the obvious way, so the student sees the wall.**

```python
clean = raw.copy()                      # work on a copy, never the original
clean["age"] = clean["age"].astype(int) # turn the ages into whole numbers
```

```text
ValueError: invalid literal for int() with base 10: 'unknown'
```

**Read that message with them, because it is unusually helpful.** "Invalid literal for int()" means *"I tried to turn a piece of writing into a whole number and this particular piece of writing is not one."* And then it tells you exactly which one: `'unknown'`, in quotes. Python has handed you the culprit.

**Step two — turn the words into holes first.**

```python
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
print(clean["age"])
```

```text
0     13.0
1     14.0
2      NaN
3     13.0
4      NaN
5     12.0
6     13.0
7     14.0
8     12.0
9     13.0
10    14.0
11     NaN
Name: age, dtype: float64
```

- `pd.to_numeric(column, ...)` — go through the column and turn everything you can into a number.
- `errors="coerce"` — **and anything you cannot convert, turn into `NaN` instead of crashing.** "Coerce" just means "force it". Without this word, `to_numeric` stops at `unknown` exactly like `astype` did.
- The dtype is now `float64` — decimals, not whole numbers. Why? **Because a column with any `NaN` in it cannot be whole numbers.** An ordinary whole-number column (`int64`) has no value that means "missing", so pandas uses decimals, where `NaN` is allowed. This is not a mistake to fix; it is a stage to pass through.

**Now run the hole count again, and this is the moment to make a fuss about:**

```python
print(clean.isna().sum())
```

```text
name     0
age      3
house    0
club     0
hours    1
score    0
dtype: int64
```

**`age` went from 0 missing to 3 missing.** Ask the student: *"did we just break it?"*

**No.** There were always three ages nobody knew. They were hidden inside a word. What `to_numeric` did was make them **countable, and therefore arguable**. Say it this way:

> **The repair did not make the holes. It made them visible.**

That sentence is the intellectual centre of the week, and it is worth writing on the board.

![The repair did not make the holes. It made them visible.](../figures/fig-w23-3-text-column-pretending.svg)
*Figure 23.3 — Same twelve rows. Same three unknowns. The only thing that changed is what you can see.*

### 8. The argument: fill or drop? (There is no right answer, and that is the lesson)

Three ages are unknown. Two honest options.

**Option A — fill them in with a stand-in.**

```python
print(clean["age"].median())      # the middle of the nine we know
print(clean["age"].mean())        # the average of the nine we know
```

```text
13.0
13.11111111111111
```

```python
clean["age"] = clean["age"].fillna(13)      # put 13 in the three holes
clean["age"] = clean["age"].astype(int)     # now it is safe to make them whole
print(clean["age"].head(5))
```

```text
0    13
1    14
2    13
3    13
4    13
Name: age, dtype: int64
```

- `fillna(13)` — put 13 wherever there is a hole in this column. It leaves everything else alone.
- **`clean["age"] = ...` on the left is not optional.** `fillna` hands you back a *repaired copy*, exactly as `sort_values` did last week. Without the assignment, nothing changes and nothing warns you. That is this week's silent bug.
- **`astype(int)` only works now**, because the holes are gone. Run the same line one step earlier and you get `IntCastingNaNError`.

**Median or mean?** The median, and the reason is Week 3's argument doing real work: one age typed as 130 by a slipped finger drags the *mean* up to 24.8 and leaves the *median* sitting at 13. Also — and a 12-year-old enjoys this one — the mean here is **13.111…**, and **nobody is 13.111 years old.** The median is a real age somebody actually is.

**Option B — throw those three rows away.**

```python
dropped = raw.copy()                                              # a fresh copy
dropped["age"] = pd.to_numeric(dropped["age"], errors="coerce")   # words -> holes
dropped = dropped.dropna(subset=["age"])                          # holes -> gone
dropped["age"] = dropped["age"].astype(int)
print(dropped.index.tolist())
```

```text
[0, 1, 3, 5, 6, 7, 8, 9, 10]
```

- `dropna(subset=["age"])` — delete any row whose `age` is a hole. `subset=["age"]` means *only look at that column* — otherwise a hole anywhere would cost you the row.
- Nine rows survive, and they keep their original labels — `0, 1, 3, 5, 6, 7, 8, 9, 10`. Rows 2, 4 and 11 are gone. That is Week 22's fact again: filtering and dropping keep the labels.

**Now the part that makes the argument real.** Ask one question of both versions: *"what is the average score of the 13-year-olds?"* Here is the whole comparison as one runnable file, and note that neither version touches the other:

```python
import pandas as pd

raw = pd.read_csv("club_raw.csv")

filled = raw.copy()                                             # option A
filled["age"] = pd.to_numeric(filled["age"], errors="coerce")
filled["age"] = filled["age"].fillna(13).astype(int)

dropped = raw.copy()                                            # option B
dropped["age"] = pd.to_numeric(dropped["age"], errors="coerce")
dropped = dropped.dropna(subset=["age"])
dropped["age"] = dropped["age"].astype(int)

print("filled :", len(filled[filled["age"] == 13]), "pupils,",
      filled[filled["age"] == 13]["score"].mean())
print("dropped:", len(dropped[dropped["age"] == 13]), "pupils,",
      dropped[dropped["age"] == 13]["score"].mean())
```

```text
filled : 7 pupils, 70.0
dropped: 4 pupils, 75.0
```

**Seventy against seventy-five.** Same file. Same tools. Same question. **Five whole marks apart, and both numbers are honest.**

| | Fill with the median | Drop the rows |
|---|---|---|
| Keeps every row | ✅ 12 rows | ❌ 9 rows |
| Invents facts | ⚠️ yes — 3 ages are now guesses | ✅ no |
| Answer to "average score at 13" | **70.0**, from 7 pupils | **75.0**, from 4 pupils |
| Good when | the missing column is not what you are asking about | the missing column **is** what you are asking about |

**The general rule worth giving them, because it will save them in Week 24 and again in the capstone:** *never fill a column with a guess and then make that column the subject of your question.* Here we filled `age` and then asked a question **about age**. That is exactly the wrong order, and it moved the answer by five marks.

![Two honest answers. You must say which one you gave.](../figures/fig-w23-5-fill-or-drop-two-answers.svg)
*Figure 23.4 — Neither answer is wrong. An answer with no cleaning log beside it is.*

### 9. The cleaning log — and why an entry without a reason is worthless

> **cleaning log** — a written, numbered record of every change you made to the raw data, and **the reason for each one**.

Here is why it is not optional. When the student reports *"the 13-year-olds average 70"*, three completely different things could be behind that number:

- The 13-year-olds really average 70.
- They average 70 **because three unknown ages were filled with 13**, and those three children happen to score badly.
- They average 70 **because the two top scorers were dropped** for having no recorded age.

**The number is identical in all three cases.** Only the log tells them apart. That is the whole argument, and it is not a school argument — it is why scientific papers have a methods section.

A good entry has three parts: **what you did**, **how many cells it touched**, and **why**.

```text
CLEANING LOG - club_raw.csv, 12 rows
  1. Turned age from writing into numbers with to_numeric(errors="coerce")
     - three rows said "unknown", and that one word made the whole column
       object, which blocked astype(int).
  2. Filled 3 missing ages with 13 - 13 is the median of the 9 ages we know,
     and the median is not dragged around by one silly value. WARNING: those
     3 ages are guesses now, not measurements. Do not use this column to
     answer questions about age.
  3. Made age whole numbers with astype(int) - nobody is 13.0 years old.
  4. Filled 1 missing hours with 3.5, the median of the 11 we know - Divya
     was on the trip, so 0 would have been a lie.
  5. Found 1 duplicate row (Bela Roy, twice, identical) - NOT removed. No
     tool for it until next week, so it is flagged here so it is not
     forgotten.
  6. Found 9 spellings of 3 houses - NOT fixed. Next week's job.
```

**Entries 5 and 6 are the ones that make this a real log rather than a chore.** They record something *found and deliberately not fixed*. A log that only lists fixes is a to-do list. A log that also lists known, unfixed problems is a piece of honest work.

**The failure mode to police, hard, from the first entry:** an entry with a WHAT and no WHY. *"Filled 1 blank hours with 3.5."* Filled with **what** and **why 3.5**? In six weeks nobody, the student least of all, will be able to say. Make them fill the WHY column before they write the next line.

![A log entry without a reason is not a log entry](../figures/fig-w23-4-cleaning-log-numbered.svg)
*Figure 23.5 — Every repair is a decision. The log is where the decision is written down.*

### 10. Saving it back out

```python
clean.to_csv("club_clean.csv", index=False)
```

- `to_csv("club_clean.csv")` — write this table out as a comma-separated file with that name.
- **`index=False` matters and is easy to skip.** Without it, pandas writes the row labels out as an extra unnamed first column, and when you read the file back you get a mystery column called `Unnamed: 0`. Nine times out of ten the row labels are just `0, 1, 2, …` and worth nothing, so `index=False` is the default habit.
- **Write to a NEW filename.** `club_raw.csv` must survive untouched, because if the log is wrong you need to be able to start again.

Read it back and check the types stuck:

```python
back = pd.read_csv("club_clean.csv")
print(back.dtypes)
```

```text
name      object
age        int64
house     object
club      object
hours    float64
score      int64
dtype: object
```

`age` is `int64` on the way back in. **That is the proof the repair was real** and not just something that looked right on screen.

### 11. The three misconceptions you will actually meet

**Misconception 1: "`NaN` is zero."** Or "it's empty text", or "it's nothing so it doesn't matter". It matters enormously — 4.33 against 3.25 on four numbers. Do not argue; run the two-line demo in §6. Nine seconds, and it settles it permanently.

**Misconception 2: "We broke the file — `age` had no missing values and now it has three."** Extremely common and completely understandable, because the number went **up** after a repair. The answer is a sentence, and it should be the same sentence every time: **"the three ages were always missing. They were hiding inside a word. Now they are countable."**

**Misconception 3: "Filling is the safe choice because you don't lose any data."** Filling feels safe because the row count does not drop. But filling **invents facts**, and dropping does not. Neither is safe; they are unsafe in different directions. The 70-versus-75 demonstration is the argument, and it should be run live rather than described.

### 12. How deep to go, and where to stop

**Go this deep:**
- Read `info()` in the four-step order, out loud, every time.
- `object` means writing, and one word is enough to cause it.
- `isna()` finds empty cells, not cells containing the word "empty".
- `NaN` is not zero.
- Holes first, then type.
- Every repair is a decision, and the decision goes on paper with a reason.

**Stop before all of this:**
- **`inplace=True`.** Many books write `df["age"].fillna(13, inplace=True)`. It is being phased out of pandas, it produces confusing warnings, and it hides the "you must catch the result" lesson that Week 22 just taught. **Always assign.**
- **`SettingWithCopyWarning`.** If the student sees it, the honest answer is: *"pandas is not sure whether you meant to change the copy or the original. `clean = raw.copy()` at the start avoids it."* Do not go further.
- **Interpolation, forward-fill, group medians.** `fillna(method="ffill")` and filling with each house's own median are both real and both better. Both belong to a later course.
- **`errors="ignore"` and `errors="raise"`.** `coerce` is the one worth knowing. Mention the others exist if asked.
- **Fixing the duplicates and the spellings.** They are next week's whole lesson. Naming them today is enough, and the log entry that says "found, not fixed" is the correct answer today.

---

### 13. 🧭 The Growing Map — the gold moves down a box

The student guide carries a figure called **Where This Fits**. Same picture every week, one more piece
filled in. It is the only page that shows the learner the *shape* of the year instead of this week's
content, and this is the first week since Week 19 where the gold has actually moved.

![The Level 2 pipeline in Week 23: the numpy and DataFrames tile is finished and the holes and duplicates tile opens](../figures/fig-w23-0-where-this-fits.svg)

*Figure 23.0 — Week 23's version. The "numpy · DataFrames" tile has turned plain white and the gold has
dropped to "holes · duplicates". Two pills are lit: **data** and **impact**.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask what changed.** *"Something on this picture is different from last week — what?"*
   The first CLEAN tile went white. That moment of noticing is worth more than any explanation you
   could give, because it means they are reading the map rather than looking at it.
2. **Then anchor today:** *"we spent the whole lesson on holes, wrong types, duplicates and messy
   text — which box is that?"* The gold tile is labelled *holes · duplicates*, so the label reads
   itself back at them. Follow up with *"we have a clean table now — why is `SEE IT` still dashed?"*
3. **Have them update their own copy** and write the four kinds of broken underneath the tile, in a
   column. Four words. That list is the spine of both this week and next.

> **🧑‍🏫 Why this is worth two minutes.** This is the week learners most often feel they are doing
> admin rather than learning — typing `fillna` is not exciting. The map is the antidote: it shows that
> cleaning is one of ten boxes in the year, not a detour from it, and that the two stages on the right
> are sitting on top of it.

> **⚠️ Watch out:** **impact** lights up for the first time in a while, and it is worth thirty seconds.
> Ask *"why would a thread called impact be lit in a lesson about missing numbers?"* The answer you are
> fishing for is that a fill or a drop changes somebody's row, and somebody outside the room has to be
> able to check why. Do not turn this into a quiz — if nobody gets it, say it yourself and move on.

---

## 🧰 Prep Checklist

This section lists what to get ready before class, so the files and the paper log exist when the lesson starts.

### 20 minutes the night before

**1. Rule the cleaning log sheet (3 minutes).** One sheet of A4, landscape, a line down the middle:

```text
   CLEANING LOG - club_raw.csv, 12 rows
   -------------------------------------------------------------
   #  |  WHAT I DID                    |  WHY I DID IT
   ---+--------------------------------+------------------------
   1  |                                |
   2  |                                |
   3  |                                |
   4  |                                |
   5  |                                |
   6  |                                |
```

**The WHY column must be physically wider than the WHAT column.** That is not decoration. It is the whole design of the lesson made visible before a word is written in it.

**2. Create the data file (5 minutes).** Make a file called `make_club_data.py` in the student's folder and run it **once**. It writes the broken CSV that the whole lesson uses.

```python
# make_club_data.py - run this ONCE. It writes the broken file for Week 23.
raw_text = """name,age,house,club,hours,score
Aarav Shah,13,red,chess,3.5,72
Bela Roy,14,Red,music,5.0,90
Chen Wu,unknown,BLUE,chess,2.0,55
Divya Nair,13,blue ,art,,83
Emeka Obi,unknown,Green,music,4.5,61
Farah Aziz,12,green,chess,6.0,95
Gita Menon,13, Blue,art,1.5,78
Hugo Silva,14,RED,music,0.5,45
Ivy Chen,12,Blue,chess,4.0,88
Jai Kapoor,13,green,art,3.5,67
Bela Roy,14,Red,music,5.0,90
Kira Das,unknown,Red,chess,3.0,74
"""

with open("club_raw.csv", "w") as f:
    f.write(raw_text)

print("club_raw.csv written")
```

```text
club_raw.csv written
```

**Open `club_raw.csv` in a plain text editor and look at it with your eyes.** Row 4 ends `art,,83` — two commas in a row, which is how an empty cell looks in a CSV. Row 4's house is `blue ` with a space after it and row 7's is ` Blue` with a space before it. You cannot see those spaces on screen, which is exactly why they are in there.

**3. Run this yourself first (8 minutes).** Create `clean_club.py` and type this in. **The whole lesson is here**, so if you can run this you can teach it.

```python
# clean_club.py - Week 23. Find the breaks, repair two of them, log everything.
import pandas as pd

raw = pd.read_csv("club_raw.csv")        # the untouched original
clean = raw.copy()                        # every repair happens on the copy

print("--- STEP 1: what have we got?")
print(raw)
raw.info()

print("--- STEP 2: how many holes?")
print(raw.isna().sum())

print("--- STEP 3: make the hidden holes visible")
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
print(clean.isna().sum())

print("--- STEP 4: the middle age of the ones we know")
print(clean["age"].median())

print("--- STEP 5: fill, then convert. In that order.")
clean["age"] = clean["age"].fillna(13)
clean["age"] = clean["age"].astype(int)
clean["hours"] = clean["hours"].fillna(3.5)
print(clean.isna().sum())

print("--- STEP 6: the repaired table")
print(clean)

print("--- STEP 7: save it under a NEW name")
clean.to_csv("club_clean.csv", index=False)
print(pd.read_csv("club_clean.csv").dtypes)
```

Run `python3 clean_club.py`. **This is the exact output. If yours differs, stop and find out why before class.**

```text
--- STEP 1: what have we got?
          name      age  house   club  hours  score
0   Aarav Shah       13    red  chess    3.5     72
1     Bela Roy       14    Red  music    5.0     90
2      Chen Wu  unknown   BLUE  chess    2.0     55
3   Divya Nair       13  blue     art    NaN     83
4    Emeka Obi  unknown  Green  music    4.5     61
5   Farah Aziz       12  green  chess    6.0     95
6   Gita Menon       13   Blue    art    1.5     78
7   Hugo Silva       14    RED  music    0.5     45
8     Ivy Chen       12   Blue  chess    4.0     88
9   Jai Kapoor       13  green    art    3.5     67
10    Bela Roy       14    Red  music    5.0     90
11    Kira Das  unknown    Red  chess    3.0     74
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 6 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   name    12 non-null     object 
 1   age     12 non-null     object 
 2   house   12 non-null     object 
 3   club    12 non-null     object 
 4   hours   11 non-null     float64
 5   score   12 non-null     int64  
dtypes: float64(1), int64(1), object(4)
memory usage: 704.0+ bytes
--- STEP 2: how many holes?
name     0
age      0
house    0
club     0
hours    1
score    0
dtype: int64
--- STEP 3: make the hidden holes visible
name     0
age      3
house    0
club     0
hours    1
score    0
dtype: int64
--- STEP 4: the middle age of the ones we know
13.0
--- STEP 5: fill, then convert. In that order.
name     0
age      0
house    0
club     0
hours    0
score    0
dtype: int64
--- STEP 6: the repaired table
          name  age  house   club  hours  score
0   Aarav Shah   13    red  chess    3.5     72
1     Bela Roy   14    Red  music    5.0     90
2      Chen Wu   13   BLUE  chess    2.0     55
3   Divya Nair   13  blue     art    3.5     83
4    Emeka Obi   13  Green  music    4.5     61
5   Farah Aziz   12  green  chess    6.0     95
6   Gita Menon   13   Blue    art    1.5     78
7   Hugo Silva   14    RED  music    0.5     45
8     Ivy Chen   12   Blue  chess    4.0     88
9   Jai Kapoor   13  green    art    3.5     67
10    Bela Roy   14    Red  music    5.0     90
11    Kira Das   13    Red  chess    3.0     74
--- STEP 7: save it under a NEW name
name      object
age        int64
house     object
club      object
hours    float64
score      int64
dtype: object
```

**4. Delete `club_clean.csv` before class (10 seconds).** The student should create it themselves.

**5. Print (2 minutes).** The whole workbook (Warm-Up through Self-Check) and one blank cleaning log sheet per student, plus a spare — they will want to rewrite it.

### 5 minutes on the day

- Terminal open in the folder. Run `ls` (or `dir` on Windows) and check `club_raw.csv` is in the list. **This is the single most common way this lesson fails.**
- `club_raw.csv` open in a plain text editor on a second tab, so you can show them the raw commas.
- Cleaning log sheet on the table, blank, WHY column facing them.
- Write on the board and leave up all lesson:

```text
1. a hole            ->  isna().sum()          ->  fillna
2. text pretending   ->  info() says object    ->  to_numeric, astype
3. the same row twice->  duplicated().sum()    ->  next week
4. four spellings    ->  value_counts()        ->  next week
```

### Fallback if the laptop or the install fails

**The paper version of this lesson is genuinely good, because the argument is the lesson and the argument needs no computer.**

Print `club_raw.csv` as a big table, exactly as pandas prints it, with `unknown` in three age cells and one blank `hours` cell. Then:

1. **Find the four breaks with a pencil.** Circle the blank cell. Circle the three `unknown`s. Circle the two Bela Roy rows. Circle every different spelling of Blue. Count them out loud: one hole, three words, two identical rows, nine spellings.
2. **The median by hand.** Write the nine known ages in a row, cross them off from both ends, and land on 13. This is better than `.median()` for understanding, honestly.
3. **The argument, and the arithmetic.** Give them the seven scores of the filled 13-year-olds (72, 55, 83, 61, 78, 67, 74 → 490 ÷ 7 = **70.0**) and the four scores of the known ones (72, 83, 78, 67 → 300 ÷ 4 = **75.0**). Let them do both divisions. **Five marks apart, on paper, in their own handwriting** — that is more convincing than any screen.
4. **Write the cleaning log.** This was always going to be on paper.

Do the typing next lesson as a twenty-minute warm-up. Week 24 needs `club_raw.csv` skills but not the `club_clean.csv` file.

---

## ⏱️ The Lesson, Minute by Minute

This section is the plan for the whole lesson, one segment at a time. The table gives the running order and the sections below give the words to use.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Form Nobody Filled In | 7 | 7 | A real broken paper form. Four things wrong with it. |
| 🧠 Concept — Four Kinds of Broken | 16 | 23 | info, object, isna, NaN-is-not-zero, and the rule about order |
| 💻 Live-Code Together — Diagnose, Repair, Log | 18 | 41 | Teacher types, student types along. Two deliberate mistakes |
| 🎲 Their Turn — The Argument, and the Log | 20 | 61 | Fill or drop, both computed, the decision written down |
| 🔑 Wrap & Assign | 9 | 70 | Name all four from memory, three checks, homework |

---

### 🪝 Hook — The Form Nobody Filled In (7 minutes)

**Do this:** Laptop closed. Hold up a piece of paper on which you have hand-written a deliberately awful club sign-up sheet. Write it out for real, by hand, before class — the messiness has to look human.

```text
        CHESS CLUB SIGN-UP
   Name          Age     House
   Aarav          13     red
   Bela           14     Red
   Chen         dunno    BLUE
   Divya          13     blue
   Emeka         ---     Green
   Bela           14     Red
   Kira        not sure   Red
```

**Say this:**

> "This is a real sign-up sheet. I mean it — this is what they look like when a class of twelve-year-olds fills one in on a Tuesday lunchtime.
>
> I want you to be the computer for a minute. I'm going to ask you the simplest possible question about this sheet. **What is the average age of the chess club?**"

Let them start. They will begin adding. Then they will stop.

> "What's the problem?"

*Three of them don't have an age.*

> "Right. So what do you do? And be specific, because 'work it out' isn't an instruction a computer can follow."

Let them propose. You will get, in roughly this order: *put 13 in* · *leave them out* · *ask them* · *put 0*.

> "Hold on to `put 0`. If I put zero in for Chen, what's the average age of the chess club?"

Let them do it. It drops hard.

> "So zero isn't 'I don't know'. **Zero is a number, and it's a wrong one.** 'I don't know' isn't a number at all, and that's going to turn out to matter a lot today.
>
> Now — other than the missing ages, tell me everything else that's wrong with this sheet."

Give them time. Point at things if they stall. You want all four:

1. Three ages missing — and written three *different* ways: `dunno`, `---`, `not sure`.
2. Bela is on there twice.
3. `red`, `Red`, `BLUE`, `blue`, `Green` — how many houses is that?
4. Nobody knows if `blue` and `BLUE` are the same house.

> "Four things. And here's what I want you to know before we open the laptop: **that's it.** Real data breaks in about four ways, and they're the four on that sheet, and every one of them has a name and a fix.
>
> The fixes are the easy part. The hard part is that **every fix changes the answer.** If I write 13 in for Chen, I've invented a fact. Not a lie exactly — but an invention. And in six weeks, when somebody looks at my average and asks 'is that real?', I need to be able to say what I did and why.
>
> So today you get a second sheet of paper, and it's the more important one."

**Do this:** Put the ruled cleaning log sheet down next to the sign-up sheet. Tap the WHY column.

> "Every repair goes on this sheet. Not just what you did — **why.** If the WHY column is empty, the line doesn't count."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What's the average age of the chess club?" | "You can't, three are missing." | If they average the four they can, ask whether that's the club's average or those four's average. |
| "If we put 0 for Chen, what happens?" | The average falls a long way. | Make them actually compute it. The size of the drop is the argument. |
| "So is 0 the same as 'I don't know'?" | No. Zero is a number. | If they say "close enough", ask what a club member with zero hours did, versus one who never handed the form in. |
| "What else is wrong with this sheet?" | All four, eventually. | Point silently at Bela's two rows, then at the four spellings. Let them name them. |
| "Why does the WHY column matter?" | So somebody can check the number later. | If they say "so you remember", accept it and upgrade it: "including you, in six weeks, when you've forgotten." |

---

### 🧠 Concept — Four Kinds of Broken (16 minutes)

**Do this:** Open a terminal. `python3 clean_club.py` is *not* what you run — you type the diagnosis live, line at a time, in a fresh file. Board already shows the four-line table from prep.

**Say this — part 1, the file:**

> "That sign-up sheet has been typed into a file. A CSV — that just means a plain text file where commas mark the edges of the cells. Have a look at it as text first, because it is worth seeing once."

**Do this:** Show `club_raw.csv` in the text editor. Point at row 4: `Divya Nair,13,blue ,art,,83`.

> "See the two commas together, `art,,83`? That's an **empty cell**. Nothing between the commas. And see the space after `blue`? Neither will you, on screen, in about thirty seconds. Remember it's there."

```python
import pandas as pd
raw = pd.read_csv("club_raw.csv")
print(raw)
```

> "`read_csv` — read a comma-separated file into a table. First line becomes the column names, every line after becomes a row.
>
> And I've called it `raw`, which is a promise to myself: **this is the original and I don't touch it.** Everything I repair happens on a copy. If I get the repair wrong, I want to be able to start again."

```text
          name      age  house   club  hours  score
0   Aarav Shah       13    red  chess    3.5     72
1     Bela Roy       14    Red  music    5.0     90
2      Chen Wu  unknown   BLUE  chess    2.0     55
3   Divya Nair       13  blue     art    NaN     83
4    Emeka Obi  unknown  Green  music    4.5     61
5   Farah Aziz       12  green  chess    6.0     95
6   Gita Menon       13   Blue    art    1.5     78
7   Hugo Silva       14    RED  music    0.5     45
8     Ivy Chen       12   Blue  chess    4.0     88
9   Jai Kapoor       13  green    art    3.5     67
10    Bela Roy       14    Red  music    5.0     90
11    Kira Das  unknown    Red  chess    3.0     74
```

> "`NaN` in Divya's hours. That's pandas's word for a hole — 'Not a Number'. It's what an empty cell looks like once it's in a table."

**Say this — part 2, `info()`:**

> "One command tells you the state of every column. And there's a right way to read it — four steps, in order, out loud, every single time."

```python
raw.info()
```

> "Step one: how many rows? `12 entries`. Is that what I expected? Yes.
>
> Step two: the `Non-Null Count` column. Non-null means 'has got something in it'. Read me `hours`."

*11 non-null.*

> "Out of twelve. **One hole.** Everything else says twelve.
>
> Step three, and this is where today lives: the `Dtype` column. `score` is `int64` — whole numbers. `hours` is `float64` — decimals. And `age` is —"

*object.*

> "Step four: **`object` is pandas's word for writing.** So say the whole sentence for me: pandas thinks the ages are —"

*Writing. Not numbers.*

> "Which is mad, isn't it? Nine of the twelve are perfectly good numbers. So **why**?"

Let them find it. It is on the screen.

> "Three rows say `unknown`. And `unknown` is a word. Here's the rule: **a column in pandas has to be one kind of thing all the way down.** One word in a column of numbers, and the whole column becomes words.
>
> It's a shop till marked *basket only*. One person turns up with a trolley, and now it's a trolley queue."

**Say this — part 3, counting the holes, and the trap:**

```python
print(raw.isna().sum())
```

```text
name     0
age      0
house    0
club     0
hours    1
score    0
dtype: int64
```

> "`isna` asks every cell 'are you missing?' and `.sum()` counts the yeses per column. So: `hours`, one hole. Good.
>
> Now read me `age`."

*Zero.*

> "**Zero missing ages.** But we just looked at three rows that say `unknown`. Are those ages missing or not?"

Let them wrestle with it. This is a genuinely good confusion.

> "They're missing **in real life** and not missing **to pandas** — because there *is* something in the cell. The word 'unknown' is a perfectly good piece of writing. Pandas isn't lying to you. It answered exactly the question you asked.
>
> Which gives us today's most useful rule:" *(write it up)*

> **`isna()` finds empty cells. It does not find cells that contain a word meaning "empty".**

> "That's why you run `info()` **and** `isna()`. `info()` catches the disguised ones by showing you `object` where you wanted a number. `isna()` catches the honest ones."

**Say this — part 4, NaN is not zero. Do not skip this. Type it live.**

> "One more thing before we repair anything, and it's the one that will bite you for the rest of your life if you get it wrong. Four numbers, one hole."

```python
hours = pd.Series([3.5, 5.0, None, 4.5])
print("mean:", hours.mean())
print("if the hole were 0:", hours.fillna(0).mean())
```

```text
mean: 4.333333333333333
if the hole were 0: 3.25
```

> "3.5 plus 5 plus 4.5 is 13. Thirteen divided by **three** is 4.33. Pandas **stepped over the hole** — added the three real numbers, divided by three, not four. Quietly. It didn't ask.
>
> And if we'd filled the hole with zero: 3.25. **Same four cells. A completely different answer**, because zero invented a club member who did nothing.
>
> So:" *(board)*

```text
NaN is not 0.        0 means: we asked, the answer was none.
NaN is not "".       NaN means: nobody told us.
```

> "Last thing, and it's a gift. Pandas will happily average round a hole. But watch what it says if you ask it for whole numbers."

```python
print(hours.astype(int))
```

```text
IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer
```

> "It refuses. It will average round a hole, but it will **not pretend a hole is a whole number.** Which tells you the order to do everything in today:" *(board, and box it)*

```text
Deal with the hole FIRST. Then change the type. Never the other way round.
```

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What does `object` mean in `info()`?" | Writing, or a mixture. | If they say "an object", give them the plain word: writing. |
| "Why is `age` writing when nine of them are numbers?" | Because three say `unknown`, and one word forces the whole column. | If stuck, use the basket-only queue. |
| "How many missing ages does `isna` report?" | Zero. | Then immediately: "and how many ages do we actually not know?" Three. Hold both facts at once. |
| "Is `NaN` the same as 0?" | No. | Run the two-line demo again rather than explaining. |
| "3.5, 5, nothing, 4.5. Average?" | 4.33 — divide by three. | If they say 3.25, they divided by four. Ask what they did with the hole. |
| "So what order do we repair in?" | Hole first, then type. | Point at the boxed rule. Make them read it back. |

---

### 💻 Live-Code Together — Diagnose, Repair, Log (18 minutes)

**Do this:** Student types in their own `clean_club.py`. You type on the shared screen. The **paper log** is beside the keyboard, and **every repair gets a line written on it before the next line of code is typed.** Enforce that from repair one. It is the habit, not the code.

---

**Step 1 — the copy.**

```python
clean = raw.copy()
```

> "One line, and it's the most professional thing you'll type today. `raw` stays untouched forever. `clean` is where the repairs go. If I make a mess, I still have the original."

---

**Step 2 — DELIBERATE MISTAKE ONE. Try the obvious thing.**

**Type this and run it. Do not warn them.**

```python
clean["age"] = clean["age"].astype(int)
```

```text
ValueError: invalid literal for int() with base 10: 'unknown'
```

> "Last line. Read it out."

*ValueError: invalid literal for int() with base 10: 'unknown'*

> "Take it in two halves. **'Invalid literal for int'** means: *I tried to turn a piece of writing into a whole number, and that piece of writing isn't one.* And then — this is the kind bit — it tells you exactly which piece of writing broke it. In quotes. `'unknown'`.
>
> Python has handed you the culprit's name. Most errors don't. So what do we do about `unknown`?"

Let them propose. Someone will say "delete it" or "change it to 13".

> "Both of those are decisions, and we'll make one in a minute. But first there's something to do that isn't a decision at all."

---

**Step 3 — make the hidden holes visible.**

```python
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
print(clean.isna().sum())
```

```text
name     0
age      3
house    0
club     0
hours    1
score    0
dtype: int64
```

> "`to_numeric` — turn everything in this column into a number if you can. `errors="coerce"` — **and anything you can't, turn into a hole instead of crashing.** Coerce just means force.
>
> Now look at the count. `age` was zero. It's three."

Pause. Let it be uncomfortable.

> "Did we just break the file?"

Let them argue. Some will say yes.

> "**No.** There were always three ages nobody knew. They were **hiding inside a word**, where nothing could count them. All we've done is turn them into holes we can count, and argue about, out loud.
>
> Say it with me, because it's the sentence of the week: **the repair didn't make the holes. It made them visible.**"

**Do this:** Write log entry 1 on the paper, out loud, in front of them, with the WHY.

```text
1 | Turned age from writing into numbers | three rows said "unknown", and that
  | with to_numeric(errors="coerce")     | one word made the whole column object,
  |                                      | which blocked astype(int)
```

---

**Step 4 — the middle age.**

```python
print(clean["age"].median())
print(clean["age"].mean())
```

```text
13.0
13.11111111111111
```

> "Two ways to describe the nine ages we know. Which one goes in the holes?"

Let them argue. Then:

> "Two reasons for the median. One is the Week 3 argument: if somebody's finger slipped and typed 130, the **mean** would run off to nearly 25 and the **median** wouldn't move at all. The other reason you can see on the screen: the mean is **13.111**. Nobody is 13.111 years old. The median is an age somebody actually is."

---

**Step 5 — fill, then convert. In that order.**

```python
clean["age"] = clean["age"].fillna(13)
clean["age"] = clean["age"].astype(int)
print(clean["age"].head(5))
```

```text
0    13
1    14
2    13
3    13
4    13
Name: age, dtype: int64
```

> "`fillna(13)` — put 13 in the holes, leave everything else alone. And now `astype(int)` works, because the holes have gone. Same command that crashed two minutes ago.
>
> That's the boxed rule, done for real."

**Do this:** Log entries 2 and 3, with the warning written into entry 2.

```text
2 | Filled 3 missing ages with 13 | 13 is the median of the 9 we know, and the
  |                              | median isn't dragged about by one silly value.
  |                              | WARNING: those 3 ages are GUESSES now.
3 | astype(int) on age           | nobody is 13.0 years old on a register
```

---

**Step 6 — DELIBERATE MISTAKE TWO. The silent one.**

**Type this, exactly, without the `clean["hours"] =` on the front.**

```python
clean["hours"].fillna(3.5)
print(clean.isna().sum())
```

```text
name     0
age      0
house    0
club     0
hours    1
score    0
dtype: int64
```

Say nothing. Let them read it.

> "What did I ask for?"

*Fill the hours hole.*

> "And how many holes has hours got?"

*One. Still one.*

> "**No error. Nothing red.** So what happened?"

Let them get there. Someone will remember last week.

> "Same thing as `sort_values`. `fillna` doesn't repair your column — it **hands you back a repaired copy**, and I threw it away the instant it printed. To keep it, you have to catch it in the name."

```python
clean["hours"] = clean["hours"].fillna(3.5)
print(clean.isna().sum())
```

```text
name     0
age      0
house    0
club     0
hours    0
score    0
dtype: int64
```

> "Zeros all the way down. **Now** it's repaired.
>
> Bug Log, please, and it's the same line as last week with a new name on it: **`fillna` gives you a copy. So does `sort_values`. So does `astype`. If there is no `=` on the left, nothing happened.**"

---

**Step 7 — flag what you found and did not fix.**

> "Two things left on that sheet — Bela twice, and nine spellings of three houses. We haven't got the tools until next week. So what do we do with them?"

*Write them down.*

> "Exactly. **A log that only lists fixes is a to-do list. A log that also lists what you found and deliberately didn't fix is honest work.**"

```text
5 | Found 1 duplicate row (Bela Roy,   | no tool for it until next week, so it
  | twice, identical) - NOT removed    | is flagged here so it isn't forgotten
6 | Found 9 spellings of 3 houses      | next week's job
  | - NOT fixed                        |
```

---

**Step 8 — save it out.**

```python
clean.to_csv("club_clean.csv", index=False)
back = pd.read_csv("club_clean.csv")
print(back.dtypes)
```

```text
name      object
age        int64
house     object
club      object
hours    float64
score      int64
dtype: object
```

> "New filename. **Never overwrite the raw file** — if the log turns out to be wrong you need to start again.
>
> `index=False` — don't write the row labels out. Without it you get a mystery extra column called `Unnamed: 0` when you read it back, and everybody meets that one once.
>
> And look: `age` comes back in as `int64`. **That's the proof the repair was real**, not just something that looked right on screen for a minute."

---

### 🎲 Their Turn — The Argument, and the Log (20 minutes)

Full instructions in the next section. In outline: the student computes the *same question* both ways — filled and dropped — writes both answers down, **picks one**, and writes the reason on the log (14 minutes); then names all four kinds of broken from memory with the board covered (6 minutes).

---

### 🔑 Wrap & Assign (9 minutes)

**Do this:** Cover the four-line board table with a sheet of paper. Laptop closed. Log sheet on the table.

**Say this:**

> "Board's covered. **Name me the four ways data arrives broken.** Not the commands — the four problems."

Wait. Prompt with *"one of them is about spelling"* if needed. You want: a hole · text pretending to be numbers · the same row twice · several spellings of one thing.

> "Good. Now the two numbers from today. What's the average score of the thirteen-year-olds?"

They should look uncomfortable, and then say: *it depends.*

> "**It depends.** That's the correct answer, and it took you a whole lesson to earn the right to say it. Seventy, if you filled the three unknown ages. Seventy-five, if you dropped those rows. **Five marks apart. Both honest. Neither one is the answer on its own.**
>
> Which means the number is worth nothing without this —" *(hold up the log)* "— beside it. That's not a school rule. Real scientists publish a methods section for exactly this reason: so somebody else can see what you did to the data before you drew a conclusion from it.
>
> One last line for the Bug Log."

Write on the board:

```text
fillna, astype and sort_values all hand you a COPY.
No "=" on the left means nothing happened, and nothing warns you.
```

**Do this:** Run the three quick checks from "Assessing Understanding". Assign homework. Hand out the workbook and a fresh log sheet.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of **this week's actual code**, on Python 3.10 and pandas 1.5.3. Tracebacks are trimmed to the first and last lines, which are the ones that matter, and those are exact.

> **Version note.** These messages and `info()` printouts are from pandas 1.5.3. On pandas 3.0 and later, a column of text is shown as `str`, not `object`, so the `age` column would read `str` in `info()` and the lesson's "`object` means writing" wording will not match the screen. This was not tested here (the course machine has pandas 1.5.3). If the laptop has pandas 3, say "`str` here, `object` in the book — both mean writing", or install 1.5/2.x.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `FileNotFoundError: [Errno 2] No such file or directory: 'clubraw.csv'` | "There is no file by that name where I am standing." | A typo in the filename (`clubraw` for `club_raw`), or the Python file is in a different folder from the CSV. | Run `ls` (or `dir`) in the terminal and read the real filename. Filenames are case-sensitive and underscores count. |
| `ValueError: invalid literal for int() with base 10: 'unknown'` | "You asked me to turn writing into a whole number, and this bit of writing isn't one." | `astype(int)` on a column that still has words in it. | `pd.to_numeric(col, errors="coerce")` first, then fill the holes, **then** `astype(int)`. |
| `IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer` | "There's a hole in this column and a hole is not a whole number." | `astype(int)` run before `fillna`. The two steps in the wrong order. | Fill (or drop) first, then convert. This is the boxed rule. |
| `KeyError: 'Age'` | "I have no column by that name." | Capital letter. The column is `age`. | Print `df.columns.tolist()` and copy the name exactly. |
| `AttributeError: 'DataFrame' object has no attribute 'isnull_sum'` | "There is no command by that name." | Half-remembered syntax. It is two commands: `.isna()` then `.sum()`. | `df.isna().sum()`. (`df.isnull().sum()` also works — `isnull` and `isna` are the same command with two names.) |
| `ValueError: Must specify a fill 'value' or 'method'.` | "Fill them with **what**?" | `fillna()` with empty brackets. | Name the value: `fillna(13)`, or `fillna(df["age"].median())`. |
| `ValueError: invalid literal for int() with base 10: 'unknown'` — *again, after filling* | Same message, later. | `fillna("unknown")` — filling holes with the word that caused the problem, then converting. | Fill with a **number**. Filling a numeric column with text puts you back where you started. |
| **No error, the hole is still there** | Nothing is wrong. `fillna` returned a copy. | `df["hours"].fillna(3.5)` with no `df["hours"] =` on the front. | `df["hours"] = df["hours"].fillna(3.5)`. Then re-run `isna().sum()` to prove it. |
| **No error, the column is still `object` after `to_numeric`** | Nothing is wrong. `to_numeric` returned a copy too. | Same missing assignment, one line earlier. | `df["age"] = pd.to_numeric(df["age"], errors="coerce")`. |
| **No error, `isna().sum()` reports 0 missing ages** | Nothing is wrong. Those cells are not empty; they contain a word. | The word `unknown` is real writing, so nothing is missing as far as pandas is concerned. | Run `info()` too. `object` where you expected a number is the tell. |
| **No error, missing values went UP after a repair** | Nothing is wrong, and this is the repair working. | `to_numeric(errors="coerce")` converted `unknown` into countable holes. | Nothing to fix. Say the sentence: the repair made the holes visible, it did not make them. |
| **No error, an extra column called `Unnamed: 0` appeared** | Nothing is wrong. The row labels were saved as data. | `to_csv("out.csv")` without `index=False`. | `to_csv("out.csv", index=False)`, and write the file again. |
| **No error, every average is slightly different from a friend's** | Nothing is wrong with either program. | One of you filled the holes and the other dropped the rows. | This is the lesson, not a bug. Compare cleaning logs. Whoever has no log cannot defend their number. |
| `SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame` | "I am not sure whether you meant to change the copy or the original." | Repairing a column of a table that was itself produced by a filter. | Start with `clean = raw.copy()` and repair `clean`. That is why the copy line exists. |

### How to teach debugging without giving the answer

All the moves from Terms 1 and 2 still work. This week adds two, and both are about *checking a repair actually happened*:

13. **"Run the count again."** After every `fillna`, `to_numeric` or `astype`, re-run `df.isna().sum()` or `df.info()`. Not "does it look right" — the count. This catches the missing-assignment bug in four seconds, and it is the same habit as Week 18's "how many went in and how many came out".

14. **"Is there an `=` on the left?"** Almost every silent failure this week is one missing assignment. Ask the question rather than pointing at the line. After the second time, the student asks it themselves.

And the sentence for this week:

> **"Half the bugs in data work aren't errors. They're repairs you thought you made and didn't, and answers that quietly changed because of a repair you forgot you made. The count and the log are how you catch both."**

---

## 🎲 The Activity, In Full

This section gives the full set-up and steps for the two parts of the student's turn, so you can run them without improvising.

### Part A — Fill or Drop: compute both, then choose (14 minutes)

**Setup.** Student at the keyboard with `clean_club.py` open and working through Step 8. Cleaning log sheet beside them with entries 1–6 already written. The workbook's **Build It** page open beside it (Part 4 uses the same WHAT / WHY layout).

**The question, and write it on the board so it stays put:**

```text
What is the average SCORE of the 13-year-olds in this club?
```

**Step 1 — build both versions (6 minutes).** Dictate this; do not paste it. Add it to the bottom of the file.

```python
# --- version A: fill the three unknown ages with the median
filled = raw.copy()
filled["age"] = pd.to_numeric(filled["age"], errors="coerce")
filled["age"] = filled["age"].fillna(13).astype(int)

# --- version B: drop the three rows instead
dropped = raw.copy()
dropped["age"] = pd.to_numeric(dropped["age"], errors="coerce")
dropped = dropped.dropna(subset=["age"])
dropped["age"] = dropped["age"].astype(int)

print("A - filled :", len(filled), "rows total")
print(filled[filled["age"] == 13][["name", "age", "score"]])
print("   average score at 13:", filled[filled["age"] == 13]["score"].mean())

print("B - dropped:", len(dropped), "rows total")
print(dropped[dropped["age"] == 13][["name", "age", "score"]])
print("   average score at 13:", dropped[dropped["age"] == 13]["score"].mean())
```

`filled["age"].fillna(13).astype(int)` is two repairs chained on one line — fill, then convert — and it reads left to right in the order they happen. Point that out; it is the boxed rule in one line.

The real output:

```text
A - filled : 12 rows total
          name  age  score
0   Aarav Shah   13     72
2      Chen Wu   13     55
3   Divya Nair   13     83
4    Emeka Obi   13     61
6   Gita Menon   13     78
9   Jai Kapoor   13     67
11    Kira Das   13     74
   average score at 13: 70.0
B - dropped: 9 rows total
         name  age  score
0  Aarav Shah   13     72
3  Divya Nair   13     83
6  Gita Menon   13     78
9  Jai Kapoor   13     67
   average score at 13: 75.0
```

**Step 2 — the pause (2 minutes).** Ask exactly these, and wait for each:

1. *"How many thirteen-year-olds in version A?"* → 7.
2. *"In version B?"* → 4.
3. *"Which three extra people are in A?"* → Chen Wu, Emeka Obi, Kira Das — **the three whose age we do not know.**
4. *"So what did we do to them?"* → decided they were 13.
5. *"And the two answers?"* → 70.0 and 75.0.
6. *"Which one is right?"* → **Neither, on its own.** If they pick one confidently, ask them to prove the other one wrong. They cannot.

**Step 3 — hand-check one (2 minutes).** Do the arithmetic on paper. It converts the lesson from a screen event into a fact.

- Version B: 72 + 83 + 78 + 67 = **300**, and 300 ÷ 4 = **75.0** ✔
- Version A: 300 + 55 + 61 + 74 = **490**, and 490 ÷ 7 = **70.0** ✔

**Step 4 — the decision, in writing (4 minutes). This is the graded item of the week.** On the cleaning log sheet (same layout as the workbook's **Build It, Part 4**):

> *I chose to __________ the three unknown ages.*
> *I chose it because __________________________________.*
> *This means the number I am reporting is __________, and the thing somebody should be suspicious about is __________.*

**Both choices earn full marks.** What does not earn marks is a blank reason, or a reason that is really a restatement (*"because I filled them"*). See the Answer Key for the two model answers and three real partial ones.

**Step 5 — the log entry that names the cost (2 minutes).** Whichever they chose, one more line goes on the log:

```text
7 | Answered "average score at 13" | I FILLED the ages, so 3 of those 7
  | using the filled version: 70.0 | pupils are only 13 because I said so.
  |                                | Dropping instead gives 75.0. Anybody
  |                                | using this number should know that.
```

**What "finished" looks like for Part A:** two numbers on the page (70.0 and 75.0), one of them circled, a written reason, and a log entry that names the other answer. **A student who has 70.0 and no mention of 75.0 has not finished**, however clean their code is.

### Part B — Name All Four, Board Covered (6 minutes)

**Setup.** Cover the four-line board table. The workbook's **Practice Set A, item A1** has a four-row empty grid: *the problem · how you spot it · the named fix*.

Student fills it in from memory. Then check it against the board together. Full marks:

| The problem | How you spot it | The named fix |
|---|---|---|
| A hole — nobody filled the cell in | `isna().sum()` is not zero | `fillna(value)` or `dropna()` |
| Text pretending to be numbers | `info()` says `object` where a number belongs | `to_numeric(errors="coerce")`, then `astype` |
| The same row twice | `duplicated().sum()` is not zero | `drop_duplicates()` — next week |
| Several spellings of one thing | `value_counts()` shows `Blue`, `blue`, `BLUE` | `.str.strip().str.title()` — next week |

**Accept plain-English spotting** — "the average looks weird", "the column says object", "I saw the same name twice", "value counts had too many houses" all count. **The names of the four problems are the graded bit**, because next week's lesson opens by asking for them.

### Variation — easier

Cut Part A to version A only, and **give them version B's answer as a printed number**: *"a classmate did it the other way and got 75.0. Write down why yours is different."* All the intellectual content survives and half the typing goes.

For the log, give them the WHAT column already filled in and have them write only the WHY. That is the harder and more valuable half, and it is where the time should go.

If naming all four from memory stalls, give initial letters on the board: `h___`, `t___ pretending`, `the same r__ twice`, `four s________`.

### Variation — harder

1. **A third option.** *"Instead of the whole club's median, fill each pupil's age with the median of **their own club**. Does the answer move again?"* The chess members whose ages we know are 13, 12, 12 → median **12**; music's are 14, 14, 14 → median **14**; art's are 13, 13, 13 → median **13**. So Chen Wu and Kira Das become 12 and Emeka Obi becomes 14. The average score of the **12-year-olds** is then **78.0** from four pupils, where median-filling gave **91.5** from two. A third answer to the same question, and the point lands hard: there are not two answers, there are as many answers as there are defensible repairs.
2. **Break it deliberately.** *"Fill the ages with the mean instead of the median. What is in the age column now, and why is it wrong on a register?"* → `13.111…`, and `astype(int)` chops it to 13 anyway, silently, which is worth seeing.
3. **Sabotage.** *"Add a row to `club_raw.csv` with an age of 130. Re-run everything. Which of the median and the mean moved?"* The median stays at 13; the mean jumps. This is Week 3's argument, proved on their own data.
4. **Audit a classmate.** Swap logs. *"Read only their log — not their code — and tell me one number in their report you would not trust, and why."* This is peer review, and it is exactly what the log is for.

---

## ❓ Questions Students Ask This Week

This section gives short answers to the questions that come up most often this week.

**"Why doesn't pandas just work out that `unknown` means missing?"**

Because it cannot know. `unknown` might genuinely be somebody's answer. So might `-`, `999`, `TBD`, `?`, `dunno`, or `no idea mate`. Pandas *does* recognise a short standard list of tokens as missing — an empty cell, and the literal words `NA`, `N/A`, `n/a`, `NaN`, `nan`, `null`, `NULL` and a few oddities that spreadsheets emit — and beyond that it refuses to guess, because guessing on your behalf is how data gets silently corrupted. **Anything else, you have to tell it about.** (There is a way to say so as you load the file, `pd.read_csv(path, na_values=["unknown"])`, and it is worth showing a keen student. `to_numeric` is the general tool, because data does not always arrive from a CSV.)

**"Is filling in missing values cheating?"**

No — **as long as you say you did it.** Filling is a normal, published, everyday technique with a proper name (imputation). It becomes dishonest at exactly one moment: when you report the answer and do not mention the repair. That is why the log is half the lesson. The version of this that *is* cheating is filling the holes, getting a nicer number, and quietly deleting the log entry.

**"Which is better, fill or drop?"**

**Genuinely nobody agrees, and this one is worth being honest about rather than pretending there is a rule.** The honest answer is: it depends on what the missing column is *for*.

If you are asking about scores and a few ages are missing, filling the ages costs you almost nothing — the ages are just along for the ride. If you are asking a question **about age**, filling is close to fatal, because you are inventing the very thing you are measuring. That is precisely the trap in today's lesson: we filled `age` and then asked a question about age, and the answer moved five marks.

Professional statisticians have argued about this for a century, and they have built much cleverer answers than either of ours — filling from similar rows, filling several different ways and reporting the spread, or modelling the missingness itself. All of them still require you to write down what you did. **The written reason, not the choice, is the professional part.**

**"Why did the column turn into decimals when I only had whole numbers?"**

Because a hole cannot live in a whole-number column. An ordinary whole-number column (`int64`) has no value that means "missing", so as soon as one `NaN` appears, the column becomes `float64`, where `NaN` is allowed. It is not a mistake; it is a stage you pass through on the way to `astype(int)`. Fill the holes and the decimals go away.

**"Can I fix the raw file by hand instead? It's only twelve rows."**

You can, and for twelve rows it is faster. **Don't.** Two reasons, and the second is the real one. First, next week's file has forty rows and the capstone's has a hundred; hand-editing does not scale. Second, and much more important: an edit you make by hand **leaves no trace**. Repairs in code are repeatable, checkable, and visible to somebody reading your file. If you hand-edit, the only record that anything was ever wrong is your memory.

**"What if I fill a hole and later find out the real value?"**

Then you put the real value in and **add a log line saying you did**. This happens constantly in real work — somebody finds the paper form, or the missing pupil comes back to school. The log grows; it never gets rewritten to look tidy. A log with a correction in it is more trustworthy than one without, not less.

**"Does the log have to be on paper? Can't it be comments in the code?"**

It can, and in professional work it usually is — a list of strings built up as the program runs, or a block comment at the top of the file. **Paper is better for now**, for one specific reason: on paper the WHY column is physically there and physically empty, staring at you. In code it is far too easy to write `# filled the ages` and move on. Once the habit is solid, move it into the code. This course moves it into the code in Week 34.

**"The two Bela Roy rows — how do you know that's a mistake and not two people called Bela Roy?"**

You do not, and that is exactly why `drop_duplicates` waits until next week and today's log says *"found, not fixed"*. Two pupils genuinely called Bela Roy would be a coincidence. Two rows with the same name, **the same age, the same house, the same club, the same hours and the same score** are a typing slip — every single field matching is the giveaway. But it is a judgement, and the honest move is to look at both rows before deleting either. Next week you will see them side by side and decide out loud.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| `FileNotFoundError` at minute nine and the lesson stalls. | The CSV is not in the same folder as the Python file, or is named slightly differently. | Prevent it: check `ls` in the 5-minute prep. If it happens anyway, `ls` in the terminal, read the real name, fix the string. Do not debug in the abstract. |
| The student panics when missing values go **up** after a repair, and wants to undo it. | Every instinct says a repair should reduce a problem count. | Have the sentence ready and say it immediately: *"the three ages were always missing — they were hiding inside a word."* Then point at Figure 23.3. |
| Every log entry has a WHAT and an empty WHY. | Writing WHAT is nearly free; writing WHY requires deciding something. | Police it from entry one. Do not let the second line be written until the first WHY is filled. Point at Figure 23.5 once, then just tap the column. |
| The student picks fill-or-drop instantly and cannot say why. | They think there is a right answer and are guessing at it. | Make them compute **both**. Do not accept a choice made before both numbers are on the page. The choosing is not the skill; the defending is. |
| `fillna` runs, no error appears, and the student believes the column is repaired for the rest of the lesson. | Missing assignment. Nothing warns you. | This is Deliberate Mistake Two and it must not be cut for time. Then make "run the count again" automatic. |
| The whole lesson turns into an argument about whether zero counts as missing. | It is a genuinely interesting question and it eats fifteen minutes. | Answer it once, firmly and correctly: *"zero means we asked and the answer was none. `NaN` means nobody told us. Both are facts and they are different facts."* Then move on. |
| The student fixes the house spellings anyway, having spotted them. | They can see the problem and want it gone. It is a good instinct. | Praise it, then hold the line: *"write it on the log as found-not-fixed. Next week you get the tool, and you'll do all forty rows in one line."* Fixing nine spellings by hand today teaches the wrong lesson. |
| The 70-versus-75 demonstration is skipped for time and the log becomes a chore. | The log has no motive without two different answers to the same question. | If you are short, cut Part B (naming the four) rather than Part A. The four can be named in next week's warm-up. The argument cannot be recreated later. |

---

## 🧭 Differentiation

This section says what to cut, add or change for a student who is struggling, flying or not engaging.

### If the student is struggling

**Cut, in this order:** the `to_csv` step, then Part B, then version B of the argument (give them 75.0 as a printed number instead of making them compute it). **Never cut the log.** A student who repaired one column and wrote one honest reason has had a successful lesson.

**Reteach the type problem with physical objects.** Get a shoebox and some cards. Write `13`, `14`, `12` on three cards and `unknown` on a fourth. *"This box is a column. What kind of box is it?"* — a numbers box. Drop in the `unknown` card. *"Now what kind of box is it?"* It is a mixed box, and the only word that describes everything in it is *writing*. **That is `object`.** Then take the `unknown` card out and replace it with an empty card — a hole. *"Now it's a numbers box with a gap in it."* That is `float64` with a `NaN`.

**The copy-this-exactly scaffold.** Four blanks, nothing else to decide:

```python
# repair.py - fill in the four blanks. Nothing else needs changing.
import pandas as pd

raw = pd.read_csv("club_raw.csv")
clean = raw.copy()

# 1. How many holes in each column? (two commands joined together)
print(clean.____().sum())

# 2. Turn the words in age into holes we can count.
clean["age"] = pd.to_numeric(clean["age"], errors="______")

# 3. Put 13 in every hole in the age column.
clean["age"] = clean["age"].______(13)

# 4. Now the holes are gone, make them whole numbers.
clean["age"] = clean["age"].astype(___)

print(clean["age"])
```

Answers: `isna` · `coerce` · `fillna` · `int`. Then the one question that must be asked and answered aloud: *"why couldn't step 4 come before step 3?"*

**One sentence to leave them with:** *"Fix the holes first, then fix the type. And write down why."*

### If the student is flying

None of these need syntax beyond this week's plus a Week 22 filter.

1. **A third answer.** Fill each pupil's age with **their own club's** median instead of the whole club's. This one needs `loc` on the *left* of an `=`, which is new, so introduce it as "put this value into the cells the filter picked out":

   ```python
   import pandas as pd

   byclub = pd.read_csv("club_raw.csv")
   byclub["age"] = pd.to_numeric(byclub["age"], errors="coerce")

   print("chess median:", byclub[byclub["club"] == "chess"]["age"].median())
   print("music median:", byclub[byclub["club"] == "music"]["age"].median())
   print("art   median:", byclub[byclub["club"] == "art"]["age"].median())

   byclub.loc[byclub["age"].isna() & (byclub["club"] == "chess"), "age"] = 12
   byclub.loc[byclub["age"].isna() & (byclub["club"] == "music"), "age"] = 14
   byclub["age"] = byclub["age"].astype(int)

   print("12-year-olds:", len(byclub[byclub["age"] == 12]),
         "average score", byclub[byclub["age"] == 12]["score"].mean())
   print("13-year-olds:", len(byclub[byclub["age"] == 13]),
         "average score", byclub[byclub["age"] == 13]["score"].mean())
   ```

   ```text
   chess median: 12.0
   music median: 14.0
   art   median: 13.0
   12-year-olds: 4 average score 78.0
   13-year-olds: 4 average score 75.0
   ```

   **A third number for the same question** — the 12-year-olds average 78.0 here and 91.5 under the whole-club median fill. Much better conversation than "fill or drop".
2. **Break the median.** Add a row to the CSV with age 130. Re-run. The median holds at 13; the mean jumps. Week 3's argument on their own data.
3. **Load it better.** Show them `pd.read_csv("club_raw.csv", na_values=["unknown"])` and let them discover that `age` arrives as `float64` with three holes already counted, no `to_numeric` needed. Then ask the good question: *"why teach the harder way first?"* (Because data does not always come from a CSV, and because you should be able to fix a column you already have.)
4. **Write the log in code.** Build a list of strings as the program runs and print it at the end. This is the Week 34 pattern, arriving eleven weeks early:
   ```python
   log = []
   log.append("1. to_numeric on age - three rows said 'unknown', blocking astype")
   log.append("2. filled 3 ages with median 13 - WARNING, these are guesses")
   for line in log:
       print(line)
   ```
5. **Peer audit.** Swap logs with somebody (or with you). *"Read only the log. Name one number in their report you wouldn't trust, and say why."*

### If the student won't engage today

**The paper sign-up sheet is the way in, because it is an argument, not a lesson.** *"Three people didn't write their age. I need the club's average age for the office by lunchtime. What do I do? And whatever you say, somebody is going to complain — who, and why?"* That is a conversation a twelve-year-old will have willingly, and it is the entire intellectual content of the week.

**If that doesn't land, make the data theirs.** Type six rows about their own things — six matches, six songs, six games — and leave two cells blank on purpose. *"What do I put here?"* Suddenly it matters whether zero is a lie.

**The minimum viable lesson, if the day is a write-off:** the four kinds of broken, named, on paper, with one example each. Three minutes. Then `raw.info()` on the real file, and read the `object` line out loud together. That is enough for Week 24 to work, because Week 24 re-diagnoses everything from scratch on a bigger table anyway.

---

## ✅ Assessing Understanding

Run all three in the last five minutes. Say them exactly as written.

**Check 1 — the four, from memory.** *"Board's covered. Name the four ways real data arrives broken."*

> **A good answer:** a hole · text pretending to be numbers · the same row twice · several spellings of one thing. Any sensible wording counts — "a gap", "words in a number column", "a repeat", "spelling". Three out of four is a pass; two is a re-teach, and the re-teach is thirty seconds with the printed sign-up sheet. **This is the check that matters most, because next week's lesson opens by asking for it.**

**Check 2 — the `object` sentence.** *"`info()` says the `age` column is `object`. Nine of the twelve ages are perfectly good numbers. Explain it to somebody who wasn't here."*

> **A good answer:** three rows say `unknown`, `unknown` is a word, and a column has to be one kind of thing all the way down — so one word makes the whole column writing. Bonus, and praise it loudly: *"which is why `isna` said zero missing ages — there's something in those cells."* If they only say "because of the unknowns", push once: *"but only three of them. Why does that affect the other nine?"*

**Check 3 — the number that is not an answer.** *"What is the average score of the thirteen-year-olds in this club?"*

> **A good answer starts with "it depends".** Then: 70.0 if you filled the three unknown ages with 13, 75.0 if you dropped those rows. Full marks adds *"and my log says which one I did"*. A student who confidently says one number without the condition attached has learnt the keystrokes and missed the lesson — send them back to the two printouts and ask which one they are quoting.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot load the CSV without help. Reads `info()` as a wall of text. Believes `NaN` is zero, or that a blank cell and the word "unknown" are the same to pandas. |
| **2 — Emerging** | Loads the file and runs `isna().sum()`. Can fill a hole when told what to fill it with. Repairs sometimes silently fail because the assignment is missing. Log entries have a WHAT and no WHY. |
| **3 — Secure** | Reads `info()` in order and identifies `object` unprompted. Repairs a column in the right order — holes, then type — and re-runs the count to check. Every log entry has a reason. Names at least three of the four kinds of broken. |
| **4 — Fluent** | Explains why the missing count went **up** after a repair. Computes both fill and drop, states both answers, chooses one and defends it in writing. Names all four kinds from memory. Catches a missing assignment without help. |
| **5 — Extending** | Produces a third defensible answer (group-wise fill) and explains why "there are two answers" was itself too simple. Audits somebody else's log and names a number they would not trust. Argues both sides of fill-versus-drop with the *question being asked* as the deciding factor. |

**Where to draw the line:** Level 3 is a pass. **Level 4 on Check 3 specifically is the one to push for**, because the capstone in Week 34 is graded almost entirely on it.

---

## 📤 Homework to Assign

This section gives the words to use when you set the homework.

**Say this:**

> "One job, about an hour, and it's today's lesson on a different table. A **reading log** — twelve rows, six columns, and it's broken in exactly the same four ways as the club register. Different words, same four problems.
>
> Your job: diagnose it before you touch it, repair the two we can repair, and produce a **numbered cleaning log** — one line per repair, **each with a reason.** I will read the WHY column first and the code second. A line with no reason on it doesn't count, and I'd rather have four honest lines than eight lazy ones.
>
> And one extra sentence at the bottom, which is the bit I actually care about: **whose ages were missing, and why might that matter?** Look at those three rows. Look at what else is in them. Then tell me what filling their ages with 12 does to any question you might want to ask about age.
>
> There's a fresh log sheet in your pack. Use it. The WHY column is the wide one for a reason."

**Workbook sections, in the order they appear in `workbook/week-23.md`:** Warm-Up (W1–W5) · Predict the Output (P1–P4) · Practice Set A — Read It (A1–A6) · Practice Set B — Write It (B1–B5) · Fix the Broken Program (Bugs 1–4) · Puzzle of the Week (a–g) · Think Deeper (T1–T3) · Build It — The Cleaning Log (Parts 1–6) · Draw It · Self-Check. The workbook has no page numbers; find things by the section name and item label.

| Workbook section | What it is | Time |
|---|---|---|
| Warm-Up | W1–W5: five questions about **last week** (`loc`/`iloc`, filtering, booleans, `sort_values`, the row label) | 5 min |
| Predict the Output | P1–P4: four snippets to predict before running — the useless `isna()` count, a hole is not a zero, the repair that never happened, the number that goes up | 8 min |
| Practice Set A — Read It | A1–A6: name the four kinds of broken, read an `info()` printout, fact-or-guess, spot the bug, label the diagram, read the traceback | 12 min |
| Practice Set B — Write It | B1–B5: one-line, two-line and filter exercises, repair-and-prove, then the whole `repair_reading.py` | 15 min |
| Fix the Broken Program | four bugs in `repair_reading.py`, three that crash and one silent | 8 min |
| Puzzle of the Week | (a)–(g): the fill that changes the answer, hand-checked both ways | 6 min |
| Think Deeper | T1–T3: three written paragraphs, T2 being "whose ages were missing?" | 8 min |
| Build It — The Cleaning Log | Parts 1–6: diagnose, who is missing, repairs, **the numbered log**, the sentence at the bottom, the Bug Log | 15 min |
| Draw It | a column with a hole, before and after | 3 min |
| Self-Check | the can-do grid, then twelve true-or-false statements | 4 min |

**Total: more than an hour if all of it is done in one sitting, so spread it over two evenings.** (The earlier plan of one hour was written for a shorter workbook.) If it is running long, cut the **Warm-Up, Draw It and the Puzzle**. **Never cut Build It Part 4 (the log), Build It Part 5, or Think Deeper T2** — they are the same question, and it is the graded one.

---

## 🔑 Answer Key

This section holds the working files and the answers to every homework item. Keep it away from the student.

Every line of code below was run on Python 3.10 with pandas 1.5.3, and every output block is copied from the real run. Item labels (W1, P1, A3, B2, T1 …) are the workbook's own; the workbook ends with its own Answers section, and this key agrees with it value for value.

### The homework file

The workbook prints this script; the student runs it once to create the file.

```python
# make_reading_data.py - run this ONCE. It writes the broken reading log.
raw_text = """name,age,genre,pages,minutes,rating
Anya Sharma,12,fantasy,320,45,4
Ben Osei,13,Fantasy,410,60,5
Cara Diaz,not given,SCIFI,150,,3
Dara Singh,12,scifi ,280,35,4
Eli Mensah,13,mystery,360,50,5
Fay Turner,not given, Mystery,120,20,2
Gus Nkemdi,12,fantasy,300,40,4
Hana Ito,11,MYSTERY,90,15,3
Ben Osei,13,Fantasy,410,60,5
Ira Volkov,not given,scifi,200,30,3
Jun Park,12,Mystery,340,55,4
Kai Brown,13,fantasy ,380,45,5
"""

with open("reading_raw.csv", "w") as f:
    f.write(raw_text)

print("reading_raw.csv written")
```

```text
reading_raw.csv written
```

Loaded with `pd.read_csv("reading_raw.csv")`, it looks like this:

```text
           name        age     genre  pages  minutes  rating
0   Anya Sharma         12   fantasy    320     45.0       4
1      Ben Osei         13   Fantasy    410     60.0       5
2     Cara Diaz  not given     SCIFI    150      NaN       3
3    Dara Singh         12    scifi     280     35.0       4
4    Eli Mensah         13   mystery    360     50.0       5
5    Fay Turner  not given   Mystery    120     20.0       2
6    Gus Nkemdi         12   fantasy    300     40.0       4
7      Hana Ito         11   MYSTERY     90     15.0       3
8      Ben Osei         13   Fantasy    410     60.0       5
9    Ira Volkov  not given     scifi    200     30.0       3
10     Jun Park         12   Mystery    340     55.0       4
11    Kai Brown         13  fantasy     380     45.0       5
```

### Warm-Up — W1 to W5 (last week's material)

| # | Answer |
|---|---|
| **W1** | The **row labels would have to stop matching the positions.** Any one of three things does it: a custom `index`, **filtering**, or **sorting** into a named copy. On a table pandas numbered itself every label equals its position, so `loc` and `iloc` agree on every row and nothing is being tested. |
| **W2** | **Something else** — the original labels of the surviving rows, for example `2, 5, 9`. Filtering **keeps** the labels; it does not renumber. That lets you trace a survivor back to the raw data, and it is why `iloc[0]` and `loc[0]` mean different things on a filtered table (`loc[0]` may not exist at all). |
| **W3** | **Twelve things, and they are True/False answers**, one per row, labels still attached, with `dtype: bool` at the bottom. **Not rows** — the rows appear only when you wrap it in `df[ ... ]`. |
| **W4** | **No.** `sort_values` hands back a sorted **copy** and throws it away if nothing catches it. One-line proof: `print(df)` straight afterwards shows the original order. To keep it: `by_rating = df.sort_values("rating")`. |
| **W5** | It is the **row's label** — your **receipt**, telling you *which* row you actually got. It catches a `loc`/`iloc` mix-up in four seconds. |

**Marking.** These are recall from Week 22 and should be quick. W1 is the one most often half-answered: "the index" without naming *how* it stops matching is half marks. W4 echoes this week's silent-bug theme (a copy that nobody catches) — point at that after marking it.

### Predict the Output — P1 to P4

All four use `raw = pd.read_csv("reading_raw.csv")`.

**P1 — the count that is right and useless.** Real output:

```text
(12, 6)
0           12
1           13
2    not given
3           12
Name: age, dtype: object
name       0
age        0
genre      0
pages      0
minutes    1
rating     0
dtype: int64
```

The table actually does not know **3** ages. `isna()` reported **0**. Both are correct: `isna()` asks "is this cell empty?", and a cell holding the words `not given` is not empty. The tell is `dtype: object` on the line above — a column of ages has no business being writing. **This is the item worth arguing about, because most students predict `age 3`.** That is why `info()` is run as well as `isna()`.

**P2 — a hole is not a zero.** Real output:

```text
336.6666666666667
252.5
3 4
```

Line 1 divides by **three** (1010 ÷ 3) — pandas stepped over the hole silently. Line 2 divides by **four** (1010 ÷ 4) — filling with 0 invented a reader who read nothing. About **84** pages apart from four numbers. `count()` counts cells with something in them (3); `len()` counts all cells (4). That gap is the whole of `NaN`.

**P3 — the repair that never happened.** Real output:

```text
1
0
```

**No error on line 2, and the hole was still there.** `fillna` returns a repaired copy and line 2 threw it away. The one difference between line 2 and line 4 is `clean["minutes"] = ` on the front. It is the most dangerous bug so far because **nothing tells you**: the program runs, the log claims a repair, and every later average divides by the wrong number.

**P4 — the number that goes UP.** Real output:

```text
before: 0 object
after : 3 float64
```

**No, the repair did not break the file.** The repair did not make the holes; it made them **visible** — they were hiding inside the words `not given`. `float64`, not `int64`, because a hole cannot live in a whole-number column; `astype(int)` comes only after the fill.

**Marking.** The "how many of four right" and "which surprised you" lines are self-report; do not mark them. Expect P1 and P4 to be predicted wrong — that is the design, and a wrong prediction that is honestly recorded is full marks.

### Practice Set A — Read It (A1 to A6)

**A1. The four kinds of broken, from memory.**

| # | The problem | How you spot it | The named fix |
|---|---|---|---|
| 1 | A hole — nobody filled the cell in | `df.isna().sum()` is not zero | `fillna(value)` or `dropna()` |
| 2 | Text pretending to be numbers | `df.info()` says `object` where a number belongs | `to_numeric(errors="coerce")` then `astype` |
| 3 | The same row twice | `df.duplicated().sum()` is not zero | `drop_duplicates()` — next week |
| 4 | Several spellings of one thing | `df["col"].value_counts()` shows `Blue`, `blue`, `BLUE` | `.str.strip().str.title()` — next week |

Accept any sensible wording for the problems. **The names are the graded part.** **A1(e):** **1 and 2.** Numbers 3 and 4 are named this week and fixed next week; a student who writes "next week" in the fix column has understood the plan and should get the mark.

**A2. Read the health report.** The `info()` printout given in the workbook:


```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 6 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   name     12 non-null     object 
 1   age      12 non-null     object 
 2   genre    12 non-null     object 
 3   pages    12 non-null     int64  
 4   minutes  11 non-null     float64
 5   rating   12 non-null     int64  
dtypes: float64(1), int64(2), object(3)
memory usage: 704.0+ bytes
```

- **(a)** 12 rows — the line `RangeIndex: 12 entries, 0 to 11`.
- **(b)** `minutes`, one hole: 11 non-null out of 12.
- **(c)** `age`. Its dtype says `object`, and ages are numbers.
- **(d)** Three rows say `not given`, and one word forces the whole column to be writing. Nine good numbers do not save it.
- **(e)** Because it has a hole in it, and a hole cannot live in a whole-number column. Pandas has to use decimals, where `NaN` is allowed. Fill the hole and `astype(int)` and the decimals go away.
- **(f)** **No.** Names *are* writing, so `object` is exactly right for `name`. **`object` is only a problem where you expected numbers.** This catches the student who has learnt "object is bad" instead of the actual idea.

**A3. Fact or guess?**

| # | The fill | Answer | Why |
|---|---|---|---|
| a | `DNP` → `0` minutes | **Fact** | Did not play means exactly zero minutes on the pitch. Nothing is invented. |
| b | blank age → median 12 | **Guess** | Nobody knows that person's age; 12 is a reasonable stand-in, still a stand-in. |
| c | blank `minutes` → `0` | **Guess, and a bad one** | Zero claims they read for no time; if they read 150 pages that is false. |
| d | `absent` → class median | **Guess** | They did not sit the test; inventing a mark changes the class average. |
| e | blank `pages` → `0` for a 5-star rating | **Guess, and an obviously wrong one** | Nobody gives five stars to a book they read none of. |

**A3(f).** **(e), and (c) very nearly** — both use 0 to mean "we don't know" and both make a claim the rest of the row contradicts. The honest options are to fill with the median **and log it**, or to leave the hole and let pandas step over it while **printing the count beside any average that touches it**.

**A4. Spot the bug.**

| # | The line | The fix |
|---|---|---|
| a | `astype(int)` with `not given` still in it | `pd.to_numeric(..., errors="coerce")`, then `fillna`, **then** `astype(int)`. Error: `ValueError: invalid literal for int() with base 10: 'not given'` |
| b | `pd.to_numeric(clean["age"])` | Add `errors="coerce"`, or it stops dead at the first word: `ValueError: Unable to parse string "not given" at position 2` |
| c | `clean["minutes"].fillna(45)` | `clean["minutes"] = clean["minutes"].fillna(45)`. No error without it, and no repair either |
| d | `raw.isnull_sum()` | It is **two** commands: `raw.isna().sum()` (`raw.isnull().sum()` is the same command under another name) |
| e | `.fillna()` with empty brackets | Fill with **what**? `fillna(45)` or `fillna(clean["minutes"].median())`. `ValueError: Must specify a fill 'value' or 'method'.` |
| f | `to_csv("reading_clean.csv")` | Add `index=False`, or reading it back shows a mystery column called `Unnamed: 0` |
| g | `pd.read_csv("reading.csv")` | The file is `reading_raw.csv`; run `ls` and read the real name |
| h | `fillna("not given").astype(int)` | Fill a numeric column with a **number**. Filling with the word that caused the problem puts you back where you started |

**A5. Label the diagram.**

| Box | Phrase |
|---|---|
| **A** | how many rows the table has |
| **B** | `object`, and this one is CORRECT — names are writing |
| **C** | `object` where a number belongs — a word is blocking it |
| **D** | `float64` because there is a hole in the column |
| **E** | one cell is empty: 11 filled out of 12 |

**A5(f).** **B is fine.** The column is `name`, and names are writing. The test is not "does it say object" but **"did I expect a number here?"**

**A6. Read the traceback.** Read the **last** line first: it names the kind of error and the exact thing that broke. "Invalid literal for int()" means "I tried to turn a piece of writing into a whole number, and this piece is not one." The culprit is in quotes at the very end: `'not given'`. It is a *kind* message because it **names the culprit** — most errors only say that something failed. The three steps of the fix, in order:

1. `clean["age"] = pd.to_numeric(clean["age"], errors="coerce")` — words become countable holes
2. `clean["age"] = clean["age"].fillna(12)` — deal with the holes (or `dropna`)
3. `clean["age"] = clean["age"].astype(int)` — **now** the type change is safe

**Marking.** Step order in A6 is the graded part: a student who writes `astype` before `fillna` has the Bug 2 misconception again.

### Practice Set B — Write It (B1 to B5)

**B1.**

```python
print(raw.isna().sum())
```

Output: the six-row column count shown under P1 (`minutes 1`, everything else 0, then `dtype: int64`). `isna()` asks every cell "are you empty?" and returns a table of True/False; `.sum()` adds each column, and `True` counts as 1.

**B2.**

```python
clean = raw.copy()
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
print(clean["age"].isna().sum())
print(clean["age"].dtype)
```

```text
3
float64
```

The count went **up** from 0 to 3, and that is a success: the repair made three hidden holes visible. (The workbook's template shows three comment lines; the copy line is the third, so accept either layout.)

**B3.**

```python
print(clean[clean["age"].isna()][["name", "genre", "pages", "rating"]])
```

```text
         name     genre  pages  rating
2   Cara Diaz     SCIFI    150       3
5  Fay Turner   Mystery    120       2
9  Ira Volkov     scifi    200       3
```

Week 22's boolean filter with a new question inside. Marks are for **noticing** that these three read 150, 120 and 200 pages — three of the four lowest in the table — with ratings 3, 2, 3. This is the seed of the Puzzle and of Think Deeper T2.

**B4.**

```python
print("holes before:", clean["minutes"].isna().sum())
print("median      :", clean["minutes"].median())
clean["minutes"] = clean["minutes"].fillna(clean["minutes"].median())
print("holes after :", clean["minutes"].isna().sum())
```

```text
holes before: 1
median      : 45.0
holes after : 0
```

The count printed **after** the repair is the point — it is the four-second habit that catches the missing-`=` bug. "It looks right" is not proof.

**B5. The whole program.** Complete working file, run end to end:


```python
# repair_reading.py - Week 23 homework. Diagnose, repair two, log everything.
import pandas as pd

raw = pd.read_csv("reading_raw.csv")     # the untouched original
clean = raw.copy()                        # all repairs happen here

# ---------- DIAGNOSE (before touching anything)
print("shape          :", raw.shape)
print("duplicate rows :", raw.duplicated().sum())
print("genre spellings:", raw["genre"].nunique())
print("holes per column:")
print(raw.isna().sum())
raw.info()

# ---------- REPAIR 1: make the hidden holes visible
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
print("holes in age, now visible:", clean["age"].isna().sum())

# ---------- who is missing? (you must look before you decide)
print(clean[clean["age"].isna()][["name", "genre", "pages", "rating"]])

# ---------- REPAIR 2: fill with the median, then convert
print("median age    :", clean["age"].median())
clean["age"] = clean["age"].fillna(12)
clean["age"] = clean["age"].astype(int)

# ---------- REPAIR 3: the honest hole in minutes
print("median minutes:", clean["minutes"].median())
clean["minutes"] = clean["minutes"].fillna(45)
clean["minutes"] = clean["minutes"].astype(int)

# ---------- CHECK
print(clean.isna().sum())
print(clean)
clean.info()

# ---------- SAVE, under a new name
clean.to_csv("reading_clean.csv", index=False)
print(pd.read_csv("reading_clean.csv").dtypes)
```

Real output:

```text
shape          : (12, 6)
duplicate rows : 1
genre spellings: 10
holes per column:
name       0
age        0
genre      0
pages      0
minutes    1
rating     0
dtype: int64
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 6 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   name     12 non-null     object 
 1   age      12 non-null     object 
 2   genre    12 non-null     object 
 3   pages    12 non-null     int64  
 4   minutes  11 non-null     float64
 5   rating   12 non-null     int64  
dtypes: float64(1), int64(2), object(3)
memory usage: 704.0+ bytes
holes in age, now visible: 3
         name     genre  pages  rating
2   Cara Diaz     SCIFI    150       3
5  Fay Turner   Mystery    120       2
9  Ira Volkov     scifi    200       3
median age    : 12.0
median minutes: 45.0
name       0
age        0
genre      0
pages      0
minutes    0
rating     0
dtype: int64
           name  age     genre  pages  minutes  rating
0   Anya Sharma   12   fantasy    320       45       4
1      Ben Osei   13   Fantasy    410       60       5
2     Cara Diaz   12     SCIFI    150       45       3
3    Dara Singh   12    scifi     280       35       4
4    Eli Mensah   13   mystery    360       50       5
5    Fay Turner   12   Mystery    120       20       2
6    Gus Nkemdi   12   fantasy    300       40       4
7      Hana Ito   11   MYSTERY     90       15       3
8      Ben Osei   13   Fantasy    410       60       5
9    Ira Volkov   12     scifi    200       30       3
10     Jun Park   12   Mystery    340       55       4
11    Kai Brown   13  fantasy     380       45       5
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 6 columns):
 #   Column   Non-Null Count  Dtype 
---  ------   --------------  ----- 
 0   name     12 non-null     object
 1   age      12 non-null     int64 
 2   genre    12 non-null     object
 3   pages    12 non-null     int64 
 4   minutes  12 non-null     int64 
 5   rating   12 non-null     int64 
dtypes: int64(4), object(2)
memory usage: 704.0+ bytes
name       object
age         int64
genre      object
pages       int64
minutes     int64
rating      int64
dtype: object
```

**Marking notes.** `minutes` may be left as `float64` — that is a defensible choice and needs a log line saying so. `age` **must** end up `int64`. A student who filled `minutes` with `0` instead of `45` has made an error worth talking about, not just marking wrong: Cara Diaz read 150 pages, so she cannot have read for zero minutes.

### Fix the Broken Program — Bugs 1 to 4

The broken file as printed in the workbook:

```python
# repair_reading.py - four bugs.
import pandas as pd

raw = pd.read_csv("reading.csv")                 # BUG 1
clean = raw.copy()

clean["age"] = clean["age"].astype(int)          # BUG 2
clean["age"] = pd.to_numeric(clean["age"])       # BUG 3
clean["minutes"].fillna(45)                      # BUG 4

print(clean.isna().sum())
```

**Bug 1.** `FileNotFoundError: [Errno 2] No such file or directory: 'reading.csv'`. The file is called `reading_raw.csv`. Fix the string. Run `ls` and read the real name rather than guessing.

**Bug 2.** `ValueError: invalid literal for int() with base 10: 'not given'`. `astype(int)` cannot get past a word. It also comes **before** the conversion that would have helped, so the two lines are in the wrong order. Fix: delete this line and let the `to_numeric` line come first.

**Bug 3.** No `errors="coerce"`, so `to_numeric` also stops dead on `not given`:

```text
ValueError: Unable to parse string "not given" at position 2
```

Fix: `pd.to_numeric(clean["age"], errors="coerce")`.

**Bug 4 — the silent one, and the one to praise loudly if they find it.** No error at all. `fillna` returned a repaired copy and nothing caught it, so `minutes` still has its hole and the printed count still says 1. Fix: `clean["minutes"] = clean["minutes"].fillna(45)`.

**In plain words, per bug (the workbook asks for each):** Bug 1 — "there is no file by that name where I am standing"; the one command is `ls` (macOS/Linux) or `dir` (Windows). Bug 2 — the culprit is the quoted `'not given'` at the end, and the two faults are *what it tried to do* (`astype` cannot get past a word) and *where it sits* (before the `to_numeric` line); even in the right order, `astype` before `fillna` would hit `IntCastingNaNError`. Bug 3 — `errors="coerce"` is missing; "coerce" means *force it*, i.e. "anything you cannot turn into a number, turn into a hole instead of crashing"; `at position 2` is the row where it gave up (Cara Diaz). Bug 4 — the student asked for the hole to be filled and the printout still says `minutes 1`.

**Most dangerous: Bug 4**, because bugs 1–3 stopped the program and named the problem, while Bug 4 ran perfectly and did not do what it said. **The four-second habit:** after every `fillna`, `to_numeric` or `astype`, print `df.isna().sum()` — the count, not "does it look right" — and ask "is there an `=` on the left?"


The corrected middle of the file — note the `print` at the end, which is how you prove the repairs actually landed:

```python
clean["age"] = pd.to_numeric(clean["age"], errors="coerce")
clean["age"] = clean["age"].fillna(12).astype(int)
clean["minutes"] = clean["minutes"].fillna(45)
print(clean.isna().sum())
```

```text
name       0
age        0
genre      0
pages      0
minutes    0
rating     0
dtype: int64
```

### Puzzle of the Week — (a) to (g)

> *"Fill the three missing ages with 12. Then answer: what is the average number of pages read by the 12-year-olds? Now do it again, dropping those three rows instead. Why did the answer move so much?"*

```python
# puzzle.py - the same question, answered two honest ways.
import pandas as pd

raw = pd.read_csv("reading_raw.csv")

filled = raw.copy()                                             # fill with the median
filled["age"] = pd.to_numeric(filled["age"], errors="coerce")
filled["age"] = filled["age"].fillna(12).astype(int)

dropped = raw.copy()                                            # drop instead
dropped["age"] = pd.to_numeric(dropped["age"], errors="coerce")
dropped = dropped.dropna(subset=["age"])
dropped["age"] = dropped["age"].astype(int)

print("filled :", len(filled[filled["age"] == 12]), "readers,",
      round(filled[filled["age"] == 12]["pages"].mean(), 2), "pages")
print("dropped:", len(dropped[dropped["age"] == 12]), "readers,",
      round(dropped[dropped["age"] == 12]["pages"].mean(), 2), "pages")
```

```text
filled : 7 readers, 244.29 pages
dropped: 4 readers, 310.0 pages
```

**(a)** Prediction: most students say "close". They are not — the gap is 65.71 pages. Mark the prediction as honest, not right.

| | How many readers? | Average pages |
|---|---|---|
| filled with the median 12 | **7** | **244.29** |
| dropped those three rows | **4** | **310.0** |

**(c)** **65.71 pages apart** (about 66).

**(d) Dropped, by hand.** The four known 12-year-olds: Anya 320, Dara 280, Gus 300, Jun 340. 320 + 280 + 300 + 340 = **1240**, and 1240 ÷ 4 = **310.0**.

**(e) Filled, by hand.** The same four plus Cara 150, Fay 120, Ira 200: 1240 + 470 = **1710**, and 1710 ÷ 7 = **244.29**.

**(f) Why it moved so much:** the three readers whose ages are unknown read **150, 120 and 200 pages** — three of the four lowest counts in the whole table (only Hana Ito's 90 is lower). Filling their age with 12 dropped all three into the 12-year-old group and pulled its average down by 66 pages. They are not a random three: their ratings (3, 2, 3) are also among the lowest, and Cara is also missing a minutes figure.

**(g) The rule:** *never fill a column with a guess and then make that column the subject of your question.* We guessed at `age` and then grouped by `age`.

### Think Deeper — T1 to T3

**T1. "`isna()` said zero missing ages when three ages were unknown. Is pandas wrong?"**

No. There is something in those cells — the words `not given`. `isna()` asks "is this cell empty?" and the honest answer is no. Pandas answered exactly the question it was asked. **The mistake was ours: we asked "how many empty cells" when we meant "how many ages don't we know".** Those are different questions, and the way you catch the difference is to run `info()` as well, and notice `object` where a number belongs.

**Marking T1.** Full marks needs (1) the exact question `isna()` asks, (2) whose mistake it was, stated as two different questions, and (3) `info()` plus **what specifically** to look for in it (`object` where a number belongs). "Run `info()` too" alone is half marks.

**T2. "Whose ages were missing, and why might that matter?"** *(This is the graded question of the homework.)*

```text
         name     genre  pages  rating
2   Cara Diaz     SCIFI    150       3
5  Fay Turner   Mystery    120       2
9  Ira Volkov     scifi    200       3
```

Cara Diaz, Fay Turner and Ira Volkov. And they are **not a random three**: they are three of the four lightest readers in the table (150, 120, 200 pages against a top of 410; only Hana Ito's 90 is lower), their ratings are 3, 2 and 3 (the lowest in the table, though Hana Ito also has a 3), and Cara is also the one missing a minutes figure. **In this table the missing ages sit among the lightest readers. Three rows cannot prove why, but they are the first thing to look at.**

Why that matters, and a full-mark answer says at least one of these:

- These three *might* be the **newest members**, who joined late and had no form filled in. That is a guess to go and check, not something the table shows.
- Filling their age with the median 12 **moves all three of them into one group at once**, and all three are light readers, so they drag that group's average down. The 12-year-olds' average pages drops 66.
- Any question **about age** is now partly a question about **who forgot to fill in a form**, which is not what anybody wanted to measure.
- The general principle: **missing data is often not random.** Ask who is missing before you decide what to do about it. If you fill in the gaps without looking at whose gaps they are, you can invent a pattern that was never there.

**Marking T2.** The three names alone are half marks. Full marks needs (1) the observation that they are the *lightest readers*, not a random three, and (2) the consequence for a question about age. The general principle about missingness not being random is a bonus — praise it loudly.

**T3. "Should the cleaning log travel with the results, or is it just working-out?"**

**It must travel with the results.** A number and its log are one object, and separating them is how misleading claims get made without anybody lying. Reporting "the 12-year-olds read 244 pages on average" without the log hides that three of those seven twelve-year-olds are only twelve **because we said so**. The strongest answers notice that this is exactly why scientific papers have a methods section, and that "I did the cleaning, trust me" is not a methods section.

**Marking T3.** The strongest answers name the *three different worlds behind one number*. Recognising the methods-section parallel, or the show-your-working parallel from maths, is full marks.

### Build It — The Cleaning Log (Parts 1 to 6)

**Part 1 — the diagnosis, filled in.**

| What I checked | The command | The number |
|---|---|---|
| rows and columns | `raw.shape` | **(12, 6)** |
| the same row twice | `raw.duplicated().sum()` | **1** (Ben Osei, rows 1 and 8) |
| spellings of genre | `raw["genre"].nunique()` | **10** — for three genres |
| holes, per column | `raw.isna().sum()` | **`minutes` 1**, everything else 0 |
| writing where numbers belong | `raw.info()` | **`age` is `object`** |

Both tick-boxes are honesty checks: the student ran `info()` **and** `isna()` and knows why both were needed (P1), and opened the CSV as plain text to see `SCIFI,150,,3`.

**Part 2 — who is missing.** Cara Diaz (row 2, 150 pages, rating 3), Fay Turner (row 5, 120, 2), Ira Volkov (row 9, 200, 3). In common: **three of the four lightest readers in the table**, with the lowest ratings bar Hana Ito's 3 — see T2. This must be done **before** choosing fill or drop.

**Part 3 — the repairs.** `age` filled with **12** (median of the nine known), then `astype(int)`, count after **0**; `minutes` filled with **45** (median of the eleven known, **not 0**), count after **0**; `reading_clean.csv` saved with `index=False` and `age` reads back as **`int64`**. A student who left `minutes` as `float64` should have said so in the log (see the Marking notes under B5).

| Repair | What I filled with | The count after |
|---|---|---|
| `age` | 12 | 0 |
| `minutes` | 45 | 0 |

**Part 4 — the log. This is the bit being marked.** Model answer, full marks. Seven entries, each with a reason. Wording will vary; the WHY column is what is being marked.


```text
CLEANING LOG - reading_raw.csv, 12 rows, 6 columns
--------------------------------------------------------------------------
 #  WHAT I DID                          WHY I DID IT
--------------------------------------------------------------------------
 1  Worked on a copy called clean;       If a repair turns out to be wrong I
    never touched reading_raw.csv        need to be able to start again.

 2  Turned age from writing into         info() said age was object. Three rows
    numbers with to_numeric             said "not given", and one word makes the
    (errors="coerce")                   whole column writing, which blocked
                                        astype(int). This made 3 hidden holes
                                        countable - it did not create them.

 3  Filled 3 missing ages with 12        12 is the median of the 9 ages I know.
                                        The median isn't dragged about by one
                                        wrong value the way the mean is.
                                        WARNING: those 3 ages are guesses now.
                                        Do not use this column to answer
                                        questions about age.

 4  astype(int) on age                   Nobody is 12.0 years old. Also proves
                                        the holes really are gone - it would
                                        have crashed otherwise.

 5  Filled 1 missing minutes with 45     45 is the median of the 11 I know.
                                        I did NOT use 0: Cara read 150 pages,
                                        so she cannot have read for 0 minutes.

 6  Found 1 duplicate row (Ben Osei,     No tool for it until next week. Flagged
    twice, every field identical)        here so it isn't forgotten. Every single
    - NOT removed                       field matching means a typing slip, not
                                        two people with the same name.

 7  Found 10 spellings of 3 genres       Next week's job.
    (fantasy/Fantasy/"fantasy ",
    scifi/SCIFI/"scifi ",
    mystery/Mystery/MYSTERY/" Mystery")
    - NOT fixed
--------------------------------------------------------------------------
```

**Marking.** Entries 2, 3 and 5 are where the marks are. Entry 3 must mention that the ages are now guesses. Entry 5 must say **why 45 and not 0** — that is the entry that shows the student understood `NaN` is not zero. Entries 6 and 7 earn credit for recording something found and deliberately not fixed.
The workbook requires **at least two** *found, not fixed* lines; entries 6 and 7 are those two.

**Three real partial answers, and what to say to each:**

| What they wrote | What is missing | Say this |
|---|---|---|
| *"3. Filled the ages."* | Filled with what? Why that? | "Filled with **what**? And why that number rather than any other?" |
| *"3. Filled 3 ages with 12 because 12 is the median."* | The consequence. Good WHAT, half a WHY. | "Good. Now one more line: what does somebody reading your report need to be careful about because of this?" |
| *"5. Filled minutes with 0."* | This one is wrong, not just thin. | Don't just mark it. Ask: "Cara read 150 pages. How long did that take her?" Then: "so what did filling 0 claim about her?" |

**Part 5 — the sentence at the bottom.** See Think Deeper T2. The three names plus **"they are among the lightest readers in the table, so filling their age moves the whole 12-year-old group"** is a full-mark answer.

**Part 6 — the Bug Log.** No single right answer; each row needs all four columns. The strong entry for this week is the silent one: *what happened* "hole still there after `fillna`" · *error message?* **none** · *what fixed it* `clean["minutes"] = ...` · *check next time* "print `isna().sum()` after every repair; look for the `=`". A second good row is the missing `errors="coerce"`.

### Draw It

The student draws one column, six cells, twice.


**Before:** the six cells hold `12`, `13`, `not given`, `12`, `13`, `11`. Labels required: a badge on the column reading **`object`**, an arrow to the `not given` cell reading **"one word makes the whole column writing"**, and a note reading **"holes found: 0"**.

**After (following `to_numeric(errors="coerce")`):** the cells hold `12.0`, `13.0`, an empty dashed cell marked **`NaN`**, `12.0`, `13.0`, `11.0`. Labels required: a badge reading **`float64`**, and a note reading **"holes found: 1"**.

Full marks needs three things: the badge changing from `object` to `float64`, the hole count going **up**, and the `NaN` cell drawn as **empty** rather than as a zero. Compare with Figure 23.3 in this chapter.

The three bottom boxes in the workbook's sample answer: **"the `not given` cell"** · **"UP, from 0 to 1"** · *"the repair didn't make the hole — it made it visible, so I can count it and argue about it"*. A strong extra annotation: an arrow to the `float64` badge saying "not `int64`, because a hole can't live in a whole-number column — that comes after the fill". **The tell that it is wrong:** a `0` drawn in the hole, or the count going down.

### Self-Check

The first table (eight "I can…" rows with 😀 / 🙂 / 😕) is self-assessment and has no key. Use it as a conversation: any 😕 on "Explain why a missing count went **up** after a repair" or "Compute both fill and drop, and defend the one I chose" means re-teach that item next week before moving on.

The twelve true-or-false statements:

| # | Statement | Answer | Why |
|---|---|---|---|
| 1 | "`NaN` and `0` mean the same thing." | FALSE | `0` means we asked and the answer was none. `NaN` means nobody told us. On four numbers: 336.67 against 252.5. |
| 2 | "If `isna().sum()` says 0, the column has no missing data." | FALSE | It has no **empty cells**. It may be full of words meaning "empty", like `not given`. Check `info()` too. |
| 3 | "`object` in `info()` always means something is wrong." | FALSE | `name` is `object` and that is correct. `object` is only a problem where you expected numbers. |
| 4 | "You must deal with the holes before you can use `astype(int)`." | TRUE | A hole is not a whole number, and pandas refuses with `IntCastingNaNError`. |
| 5 | "`df["age"].fillna(13)` on its own repairs the column." | FALSE | It hands you a repaired **copy**. Without `df["age"] = ` on the front, nothing changes and nothing warns you. |
| 6 | "A cleaning log entry needs the reason, not just what you did." | TRUE | Without the reason, nobody — including you, in six weeks — can tell whether the number came from the world or from a repair. |
| 7 | "One word in a column of numbers makes the whole column writing." | TRUE | A column has to be one kind of thing all the way down. |
| 8 | "`to_numeric` without `errors="coerce"` still works on `not given`." | FALSE | `ValueError: Unable to parse string "not given" at position 2`. Coerce turns it into a hole instead of a crash. |
| 9 | "Filling is the safe option because you keep all your rows." | FALSE | Filling **invents facts**; dropping does not. Neither is safe — they are unsafe in different directions. |
| 10 | "A missing count going up after a repair means the repair failed." | FALSE | It means the repair **worked**. The holes were always there, hiding in a word. |
| 11 | "`to_csv("out.csv")` writes exactly the columns you can see." | FALSE | It also writes the row labels, as a mystery column called `Unnamed: 0`. Use `index=False`. |
| 12 | "The mean is a safer thing to fill a hole with than the median." | FALSE | The mean is dragged about by one silly value; the median does not move. A mean also gives ages like 12.33, and nobody is 12.33 years old. |

**A note on row 12 for the teacher.** The workbook's own answer quotes "13.111…" and "an age typed as 130 sends it to nearly 25". Those are the **chess-club** numbers from the lesson, not the reading log. On the reading log the mean of the nine known ages is **12.33** (111 ÷ 9) and the median is **12**. The verdict (FALSE) and the reasoning are unaffected; if the student quotes 13.111 they are remembering the lesson, not making an error.


### Answers to every question posed in the lesson

**Hook.** *"Average age of the chess club?"* — you cannot say; three ages are unknown. *"If we put 0 for Chen?"* — the average falls a long way, so 0 is a wrong number rather than a missing one. *"Is 0 the same as 'I don't know'?"* — no; 0 is a measurement, missing is the absence of one. *"What else is wrong with the sheet?"* — Bela twice; four or five spellings of the houses; the three unknowns written three different ways.

**Concept.** *"What does `object` mean?"* — writing, or a mixture pandas has stopped describing. *"Why is `age` writing when nine are numbers?"* — three say `unknown`, and a column must be one kind of thing all the way down. *"How many missing ages does `isna` report?"* — zero, because those cells are not empty. *"Is `NaN` the same as 0?"* — no. *"3.5, 5, nothing, 4.5 — average?"* — 4.33; pandas divided by three. *"What order do we repair in?"* — hole first, then type.

**Live-code.** Step 2 → `ValueError: invalid literal for int() with base 10: 'unknown'`, and Python names the culprit in quotes. Step 3 → missing ages go from 0 to 3; **the repair made them visible, it did not make them**. Step 4 → median 13.0, mean 13.111…; the median wins because it resists one silly value and because nobody is 13.111 years old. Step 5 → `age` becomes `int64`. Step 6 → the hole is still there because there was no `=` on the left; **no error**. Step 7 → found-not-fixed goes on the log. Step 8 → `age` reads back as `int64`, which proves the repair was real.

**Activity Part A.** Filled: 7 pupils aged 13, average score **70.0** (490 ÷ 7). Dropped: 4 pupils, average **75.0** (300 ÷ 4). The three extra people in the filled version are Chen Wu, Emeka Obi and Kira Das — the three whose ages nobody knows. Neither answer is right on its own.

**Two model decisions, both full marks:**

> *"I chose to **fill** the three unknown ages with 13, because I did not want to throw away three real pupils' real scores just because a form was missing. This means the number I am reporting (70.0) treats three pupils as thirteen when nobody actually knows, and the thing somebody should be suspicious about is that all three of them score below the class average, so the fill pulled the answer down."*

> *"I chose to **drop** the three rows, because the question I am answering is about a particular age group, and if I invent the ages then I am inventing the group. This means the number I am reporting (75.0) only comes from **four** pupils, and the thing somebody should be suspicious about is that four is a very small group to say anything about — one different pupil would move it a long way."*

**Three real partial decisions, and what to say:** *"I filled them because it's easier"* → "easier for whom? What did it cost?" · *"I dropped them because you shouldn't make things up"* → "good principle. Now what did it cost you?" · *"I filled them because 13 is the median"* → "that's why 13. Why fill rather than drop?"

**Activity Part B.** The four-row grid is in the table under "Part B" above.

**Harder variation.** Group-wise fill: the chess ages we know are 13, 12, 12 → median **12**; music 14, 14, 14 → **14**; art 13, 13, 13 → **13**. Chen Wu and Kira Das become 12, Emeka Obi becomes 14, and the 12-year-olds then average **78.0** from four pupils against **91.5** from two under the whole-club fill — a third answer to the same question, which is the point. Filling with the mean gives ages of 13.111…, and `astype(int)` then chops them to 13 silently. Adding a row with age 130 leaves the median at **13.0** and sends the mean to **24.8** — Week 3's argument, on their own data.

**Wrap.** The four kinds of broken: a hole · text pretending to be numbers · the same row twice · several spellings of one thing. Average score of the 13-year-olds: **it depends** — 70.0 filled, 75.0 dropped, and the log says which.

---

## 🔮 Next Week Preview

This section says what next week covers and what to prepare now.

Next week is a lab, and it is the payoff for this one. The table goes from twelve rows to **forty**, which is too many to eyeball — so the diagnosis has to be done with commands rather than eyes. The student meets the last two kinds of broken and fixes them properly: `drop_duplicates()` removes two rows and they have to be able to **name which two**, and `.str.strip().str.title()` collapses fourteen spellings into four houses in a single line.

Then `groupby` arrives, and it is the most powerful line of pandas in this whole course: `df.groupby("house")["score"].mean()` does in one line what fifteen lines of Week 15 loops used to do.

With it comes the trap that the whole term has been building towards — one house has **two members**, its average is 95.00, it sits proudly at the top of the table, and the average says nothing whatsoever about how many rows it came from. The student prints `.size()` next to `.mean()`, or they mislead themselves.

**Prep early, and this one is worth doing before the weekend:** run the Week 24 prep script so `house_raw.csv` exists, then run `raw["house"].value_counts()` yourself and count the spellings — there are **fourteen**, and seeing that number with your own eyes is what will let you sound confident about it in class. Also keep this week's cleaning log sheets: next week's log continues on the same paper, because next week's table has the *same four problems* and the student should feel the log growing rather than starting again.
