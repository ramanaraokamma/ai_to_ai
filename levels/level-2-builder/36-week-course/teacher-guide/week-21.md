# Week 21 — Tables With Names On: Meet the DataFrame

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Student Guide](../student-guide/week-21.md) · [Workbook](../workbook/week-21.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the labels come back, and two commands you run on every table forever |
| **Big idea** | A **DataFrame** is a table where the columns have names and the rows have an index, so you never again have to remember "column 3". |
| **New vocabulary** | DataFrame · Series · index · column name · NaN |
| **New syntax** | `pd.DataFrame({...})` · `df.head()` · `df.info()` · `df["col"]` |
| **Materials** | **Week 14's hand-formatted table printout, on paper** · the printed workbook (Warm-Up, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Build It, Draw It, Self-Check) · a blank ten-row grid template (Figure 21.6) · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, **and pandas installed**. This is the second and last install of the course, and it is the one thing that can eat the lesson. `squad_data.py` from Week 14/15 must still exist. |
| **Prep time** | 25 minutes the night before (15 of them are the install) · 5 minutes on the day |

> **⚠️ Watch out:** install pandas **the night before, on the machine the student will actually use**, and prove it by running `import pandas`. It is a bigger download than numpy and it can be slow. Do not discover a broken install at minute three of the lesson. The paper fallback in the Prep section is genuinely good — this week's ideas are *names on columns* and *reading a health report* — but it is a fallback, not the plan.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build a DataFrame from a dictionary of columns** — and from a list of dictionaries, in one call.
2. **Read `df.head()`** and explain what every part of the printout is, including the numbers down the left.
3. **Read `df.info()` line by line**: how many rows, what the columns are called, what kind of thing each holds, and how many of its cells are actually filled in.
4. **Explain what the index is** and why it is not one of the columns.
5. **Notice a whole-number column printing as decimals** and say what caused it.

Observable evidence: `table.py`, which builds a DataFrame from Week 14's twelve records and prints `head()`, `info()` and one column; a ten-row DataFrame about the student's own week; and a written line-by-line explanation of every line of that table's `info()` output, including why one column is a float when only whole numbers were typed.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to know any pandas to teach this.** There is one new container and two commands you print. Read this section once — about fifteen minutes — and you are comfortably ahead of the student.

### 1. Why this week exists, and why it is a relief

For four weeks the student has been paying a price on purpose. Here is the price, in one picture.

Week 17 asked them to rub the words off a table until only a rectangle of numbers was left. That rectangle is a numpy array: it knows its shape, it does maths to everything at once, and it is fast. And it has **absolutely no idea what its columns are called.**

So they have been keeping the names *separately*:

```python
names = np.array(["Aarav", "Bela", ...])      # ten names
tests = np.array(["Quiz1", "Quiz2", ...])     # five test names
scores = np.array([[72, 65, ...], ...])       # a ten-by-five grid
```

Three separate objects, held together by nothing but hope and the fact that the lengths happen to match. Last week they saw what happens when the lengths *stop* matching — a loud `IndexError` if they were lucky, and if they were unlucky, a wrong column and a confident wrong number.

And what happens if you try to keep everything in one array? Try it:

```python
rows = np.array([[r["name"], r["team"], r["runs"], r["balls"], r["out"]]
                 for r in squad])
print(rows[:3])
print("shape:", rows.shape, " dtype:", rows.dtype)
print("total runs:", rows[:, 2].sum())
```

```text
[['Asha' 'Falcons' '48' '32' 'True']
 ['Ravi' 'Falcons' '12' '20' 'True']
 ['Nita' 'Falcons' '77' '55' 'False']]
shape: (12, 5)  dtype: <U21
Traceback (most recent call last):
  File "allnumpy.py", line 10, in <module>
    print("total runs:", rows[:, 2].sum())
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/numpy/core/_methods.py", line 49, in _sum
    return umr_sum(a, axis, dtype, out, keepdims, initial, where)
numpy.core._exceptions._UFuncNoLoopError: ufunc 'add' did not contain a loop with signature matching types (dtype('<U21'), dtype('<U21')) -> None
```

**Every number became writing.** `48` is now `'48'`, and you cannot add up writing. That is Week 17's `<U21` lesson, applied to a whole table at once: an array holds **one kind of thing**, so a table with names in it becomes a table of nothing but names.

> **This week's one sentence:** "A DataFrame is a numpy array with the labels put back on — and each column is allowed to be a different kind of thing."

That is the whole lesson, and it is genuinely a relief for a student who has been carrying three objects around.

![A bare block of numbers with question marks becomes a grid with named columns and an index](../figures/fig-w21-1-dataframe-named-grid.svg)
*Figure 21.1 — Same numbers, with the names put back on. One column is even allowed to be words.*

### 2. The two containers, and only two

> **DataFrame** — a whole table. Columns with names, rows with an index. Each column may hold a different kind of thing.
>
> **Series** — one column, on its own, still carrying the row labels and its own name.

That is the entire pandas type system as far as this course is concerned. **A DataFrame is a set of Series that all share one index.** `df["runs"]` hands you one of them.

The analogy that works, and it is worth drawing:

> "A numpy array is a table of numbers drawn on graph paper. You find things by counting squares — 'third column along, I think.' A DataFrame is the same table printed as a proper spreadsheet: **column headings across the top, row numbers down the side.** Same numbers, but now you can say *'the runs column'* instead of *'column 2, probably'*."

Here is the whole four-week arc in one table, which is worth putting on the board:

| Week | The container | One row is | Columns have names? | Maths on everything at once? | Mixed kinds in one table? |
|---|---|---|---|---|---|
| 14 | list of dicts | a `dict` | ✅ yes — the keys | ❌ no, you loop | ✅ yes |
| 17 | numpy array | a row of numbers | ❌ no, just positions | ✅ yes | ❌ no — one kind only |
| **21** | **DataFrame** | **a labelled row** | ✅ **yes** | ✅ **yes** | ✅ **yes** |

**Be honest about the cost**, because there is one: pandas is slower than raw numpy and it is a much bigger, more complicated library with far more ways to write the same thing. That is exactly why it did not come first. The student needed to feel the pain of missing labels before the cure would mean anything.

### 3. Building one — two ways in, and they are the same call

**Way one: a dictionary of columns.** Each key becomes a column name; each list becomes that column's values.

```python
ages = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, 13, 12, 11],
})
print(ages)
```

```text
   name  age
0  Asha   12
1  Ravi   13
2  Nita   12
3   Sam   11
```

**Read the shape of that code out loud**, because it is the thing students get backwards: **the key is a column name and the list running down the page is a column, not a row.** Two keys, two columns. Four items in each list, four rows.

**Way two: a list of dictionaries — which is Week 14's dataset, unchanged.**

```python
squad_df = pd.DataFrame(squad)
```

One call. Every dictionary becomes a row; every key becomes a column name. **This is the moment of the lesson** — the student spent a whole week of Term 2 writing f-string format codes to line that table up by hand, and pandas does it in one call and lines it up better.

> **🧑‍🏫 If a student asks:** *"which way is better?"* Neither. Use the dict-of-lists when you are typing data in by hand column by column, which is most of the time in this course. Use the list-of-dicts when you already *have* a list of dicts, which is what happens when data arrives from a file or a website. They produce exactly the same thing.

### 4. `df.head()` — and the four things in the printout

```python
print(squad_df.head())
```

```text
    name     team  runs  balls    out
0   Asha  Falcons    48     32   True
1   Ravi  Falcons    12     20   True
2   Nita  Falcons    77     55  False
3    Sam  Falcons     5      9   True
4  Kabir   Tigers    63     41   True
```

`.head()` shows the **first five rows**. `.head(3)` shows three. That is all it does, and it is the single most-used command in pandas, because you run it every time you touch a new table.

Four things in that printout, and the student should be able to name all four:

1. **The column names**, along the top: `name`, `team`, `runs`, `balls`, `out`. They came from the dictionary keys.
2. **The index**, down the left: `0 1 2 3 4`. **These are the row labels, and they are not a column.** More on this next.
3. **The values**, one per cell.
4. **The alignment.** Every column lined up in a tidy block (pandas right-aligns both text and numbers in columns), and pandas worked out every column's width for itself. Nobody typed a format code.

### 5. The index — and the one thing to be firm about

> **index** — the row labels down the left-hand side. By default they are the counting numbers `0, 1, 2, …`, but they do not have to be.

**The index is not a column.** This is worth thirty seconds of being firm, because it causes real confusion later.

The proof is short and satisfying. There are five column names — `name`, `team`, `runs`, `balls`, `out` — and `df.info()` will say "total 5 columns". The index is not among them. And asking for it by number fails:

```python
print(squad_df[0])
```

```text
KeyError: 0
```

There is no column called `0`. Square brackets on a DataFrame mean *"give me the column with this name"*, and `0` is not a name.

![A DataFrame with a heavy frame round its columns; the grey index column sits outside the frame](../figures/fig-w21-2-index-is-not-a-column.svg)
*Figure 21.2 — The index labels rows. Column names label columns. Two different jobs.*

**What the index is for**, in one sentence a 12-year-old can use: *"it's the row's name, like the name on a coat peg."* Right now those names are just 0, 1, 2, 3 — but they could be dates, or player names, or sensor IDs, and in Week 22 they will meet `df.loc[1, "age"]`, which looks a row up **by its name** rather than by counting.

And the honest note: **a default index of 0, 1, 2 is doing nothing useful yet.** Say so. It becomes useful the moment rows get filtered out and the numbers stop being consecutive — which happens in Week 22, and which is precisely when a student who thought the index was "just the row count" gets confused.

### 6. `df["col"]` — and what comes back is a Series

```python
print(squad_df["runs"])
```

```text
0      48
1      12
2      77
3       5
4      63
5      30
6       0
7      41
8      55
9      22
10     90
11    104
Name: runs, dtype: int64
```

Three things in that output and the last line is the interesting one:

1. **The index came with it.** `0` to `11`, down the left. The column did not forget which rows its values belong to. That is the whole difference between this and `arr[:, 2]`.
2. **The values.**
3. **A footer:** `Name: runs, dtype: int64`. The Series knows its own **name** and its own **kind**. An array knew its kind; it never knew its name.

![A DataFrame with the runs column lifted out, still carrying its index and a Name and dtype footer](../figures/fig-w21-3-series-vs-dataframe.svg)
*Figure 21.3 — A Series carries three things: the values, the index they sit on, and its own name.*

You can prove the two types out loud, and it is worth doing once:

```python
print("the whole table is a:", type(squad_df))
print("one column is a    :", type(squad_df["runs"]))
```

```text
the whole table is a: <class 'pandas.core.frame.DataFrame'>
one column is a    : <class 'pandas.core.series.Series'>
```

**The mistake that will happen, guaranteed:** `df["Runs"]` with a capital R. Column names are text, and text is case-sensitive. It gives a `KeyError`, and pandas's traceback for it is **nineteen lines long**, which is a shock after numpy's four. That is a teaching opportunity and Step 5 of the live-code uses it deliberately.

### 7. `df.info()` — the twelve-line health report, and how to read it

This is the most valuable command in the whole of pandas and it deserves its own five minutes.

```python
squad_df.info()
```

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    12 non-null     object
 1   team    12 non-null     object
 2   runs    12 non-null     int64 
 3   balls   12 non-null     int64 
 4   out     12 non-null     bool  
dtypes: bool(1), int64(2), object(2)
memory usage: 524.0+ bytes
```

**Note there is no `print()` around it.** `info()` prints for itself and hands back nothing, so `print(df.info())` would print the report and then print the word `None` underneath. Mention it once; it confuses people.

Now read it, line by line. Every line is a check that can fail:

| Line | What it says | The check it gives you |
|---|---|---|
| `<class 'pandas.core.frame.DataFrame'>` | This really is a DataFrame. | If it says `Series`, you handed pandas one column when you meant the table. |
| `RangeIndex: 12 entries, 0 to 11` | Twelve rows, labelled 0 to 11. | **Is twelve the number you expected?** If you typed twelve records and this says eleven, you lost one. |
| `Data columns (total 5 columns):` | Five columns follow. | Count them against how many names you typed. |
| `#  Column  Non-Null Count  Dtype` | The heading of the little table underneath. | — |
| `0   name    12 non-null     object` | Column 0 is `name`, twelve of its twelve cells hold something, and it is text. | **Non-null count.** Anything less than 12 means holes. |
| `2   runs    12 non-null     int64` | Column 2 is `runs`, no holes, whole numbers. | **Dtype.** A column you meant to be numbers showing `object` is an alarm. |
| `dtypes: bool(1), int64(2), object(2)` | The tally: one true/false column, two whole-number, two text. | Adds to 5. If it doesn't, you miscounted your columns. |
| `memory usage: 524.0+ bytes` | How much space it takes. | Ignore it. It is the least interesting line and students fixate on it. |

![Five stacked bands, each holding one line of the info printout with a plain explanation](../figures/fig-w21-4-info-line-by-line.svg)
*Figure 21.4 — Every line of `info()` is a check you can fail. Read all five out loud.*

**Two words to define plainly, because they will be asked:**

> **`object`** — pandas's word for "a column of general Python things", which in practice almost always means **text**. Seeing `object` on a column you expected to be numbers is the loudest warning sign in pandas.

> **non-null** — how many cells actually have something in them. "Null" means empty. `12 non-null` out of `12 entries` means nothing is missing.

**And the sentence to say:** *"`head()` shows you what the table looks like. `info()` tells you whether you can trust it. Run both, on every table, every time, before you do anything else."*

### 8. `NaN` — and why one hole turns whole numbers into decimals

This is the planted surprise and it is the deepest idea in the week.

Build a tiny table of ages, all whole numbers:

```python
ages = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, 13, 12, 11],
})
```

```text
   name  age
0  Asha   12
1  Ravi   13
2  Nita   12
3   Sam   11
```

```text
 1   age     4 non-null      int64
```

Now build the same table with **one age never written down** — `None` instead of `13`:

```python
holed = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, None, 12, 11],
})
```

```text
   name   age
0  Asha  12.0
1  Ravi   NaN
2  Nita  12.0
3   Sam  11.0
```

```text
 1   age     3 non-null      float64
```

**Three things changed and nobody was warned about any of them.**

1. `None` became **`NaN`**.
2. `12` became **`12.0`** — every whole number in the column grew a decimal point.
3. The dtype went from `int64` to **`float64`**, and the count from `4 non-null` to `3 non-null`.

![Two small age tables side by side: 12, 13, 12, 11 as int64; then 12.0, NaN, 12.0, 11.0 as float64](../figures/fig-w21-5-hole-makes-a-float.svg)
*Figure 21.5 — One hole, and the whole column changes kind.*

> **NaN** — pandas's marker for "there is nothing here". It stands for "Not a Number", and it is itself a decimal.

**Why the whole column changes, and this is the bit to get right.** Go back to Week 17: a column holds **one kind of thing**. `NaN` is a decimal. So the moment one cell holds a `NaN`, the column has to be a kind that can hold decimals — and the only kind that can hold both `12` and `NaN` is `float64`. A whole-number box has nowhere to put a `NaN`. So pandas converts the entire column, silently, because it has no choice.

**This is exactly Week 17's rule, third appearance:** *the container picks the one kind that can hold everything.* Week 17: one word in a list of numbers made everything text. Week 18: one decimal made everything `float64`. Week 21: one hole makes everything `float64`. **Same rule, three costumes.** A student who spots that connection has had a very good term.

**Say the practical version out loud:** *"if you typed whole numbers and pandas shows you decimals, you have a hole somewhere. Go and find it — `info()` will tell you which column and how many."*

### 9. The three misconceptions you will actually meet

**Misconception 1 — "the index is the first column."**
It looks like one; it prints like one. It is not one of the five columns, `info()` does not count it, and `df[0]` is a `KeyError`. Cure: count the column names in `head()`, then count the number after "total" in `info()`. Both are five. Where is the index in that five?

**Misconception 2 — "`12.0` and `12` are the same, so who cares."**
The *value* is the same; the **kind** is not, and the change of kind is a message. It is telling you a hole exists somewhere in that column. A student who shrugs at `12.0` will merrily average a column with three missing values in it and never know.

**Misconception 3 — "pandas replaces numpy."**
It does not. A DataFrame is built *on top of* numpy — every column is a numpy array underneath, and every bit of the axis work from Week 19 and the mask work from Week 20 is still doing the actual arithmetic. Nothing from the last four weeks is wasted. Say so plainly; students worry about this.

### 10. How deep to go, and where to stop

**Go this far:** `import pandas as pd`; building a DataFrame from a dict of lists and from a list of dicts; `df.head()` and `df.head(3)`; `df.info()` read out loud, line by line, all of it; `df["col"]` and the fact that it is a Series with an index and a name; the index is not a column; and the `None` → `NaN` → `float64` surprise, traced back to Week 17's one-kind rule.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `df.loc[...]`, `df.iloc[...]` | **Week 22.** This is the big one and it is very tempting, because "how do I get one *row*?" is the first question a student asks. Answer honestly: *"next week, and it needs two new words."* |
| `df[df["age"] > 12]` — filtering | **Week 22.** They have masks from last week and will guess this. If one does, let them try it, admire it, and then say: "yes — and next week we'll do it properly, including the bit where the index goes weird." |
| `df.sort_values(...)` | **Week 22.** |
| `df.isna()`, `df.fillna()`, `df.dropna()`, `df.astype()` | **Week 23.** Today's job is to *notice* the hole, not to fix it. Noticing is the harder skill and it deserves its own week. |
| `pd.read_csv()` / `df.to_csv()` | **Week 23.** Everything today is typed in by hand on purpose, so the student knows exactly what is in the table. |
| `df.groupby(...)` | **Week 24.** |
| `df.describe()` | **Week 34.** It is lovely and it produces eight rows of statistics that will swamp today's two commands. |
| `df.shape`, `df.columns`, `df.dtypes` | Fine to mention if a student asks — they are all facts, no brackets, like numpy's `.shape`. **Do not build on them**, because `info()` already contains all three and this week is about reading `info()`. |
| `.mean()` on a Series | Week 24's ground. If a fast student wants arithmetic on a column, give them `df["sleep"] * 60`, which is Week 18's array maths on a Series and needs nothing new. |
| Setting a custom index | Week 22, and lightly. Today: "it doesn't have to be 0, 1, 2" is enough. |

The line to hold in your head all lesson: **today the student learns to run two commands on a new table and read the second one out loud.** `head()` and `info()`. Everything else is one call.

---

### 11. 🧭 The Growing Map — two minutes on the second word

The student guide carries one figure that is not about this week's content: the same pipeline every
week, with one more piece filled in. Today it does one job particularly well — it shows a learner that
the container they just met is the one every remaining box needs.

![The Level 2 pipeline in Week 21: still stage three's numpy and DataFrames tile, now the table has names on its columns](../figures/fig-w21-0-where-this-fits.svg)

*Figure 21.0 — Week 21's version. Third week inside the `numpy · DataFrames` tile, weeks 19 to 22, and
the week its second word finally arrives. One thread lit: representation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and put a finger on the second word.** Ask *"which of the two words in the gold tile did we
   meet today?"* You want **DataFrames** — and then the follow-up that matters: *"what did it give back
   that the array had taken away?"* The **names**. Say the shape of the answer out loud: Week 14's
   labels, Week 17's whole-grid maths, one container.
2. **Then the question that makes the picture pay:** *"point at every box on this map that will need a
   DataFrame."* Let them travel right — clean it, see it, predict and check, capstone. It is all of them.
   **That** is why two commands on a new table is worth a whole lesson, and a finger moving across a
   picture argues it better than any sentence from you.
3. **Have them annotate their own copy:** circle `DataFrames`, and write **head() then info(), every
   time** beside it. It is the habit the next fifteen weeks assume they already have.

> **🧑‍🏫 Why this is worth two minutes.** After an install and two new commands, a student can easily
> file today under "more library stuff". The map reframes it as the container the rest of the course runs
> on, which is both true and motivating. It also quietly answers the question they will ask in Week 23 —
> *why did we bother with numpy at all?* — because the gold tile holds both words, in that order, and
> they can see the order was chosen.

> **⚠️ Watch out:** the box has not moved, and some students read a still box as a wasted week. Say
> plainly that today was the biggest change of the term and the map cannot show it, because swapping the
> container happens *inside* a box.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Install pandas. This is the one thing that can ruin the lesson, so do it now, on the machine the student will use.**

```bash
pip install pandas
```

If that errors, try these in order — one of them will work:

```bash
pip3 install pandas
python3 -m pip install pandas
```

Then **prove it**, in a terminal:

```bash
python3 -c "import pandas; print(pandas.__version__)"
```

You must see a version number. Anything recent is fine:

```text
1.5.3
```

If you see `ModuleNotFoundError: No module named 'pandas'`, the install did not take. The usual cause is the same as Week 17's: `pip` installed into a *different* Python than `python3` runs — which is exactly what `python3 -m pip install pandas` fixes, because it uses the same Python either way. **Solve this tonight.**

> **📌 Version note:** pandas 2.x prints everything in this file identically, with one exception — the `memory usage:` line in `info()` may show a different number. That line is the least interesting one on the page. If your numbers differ from this file *only* there, you are fine. The one other difference to expect on 2.x is in long tracebacks: the number of lines and the pandas file paths and line numbers can differ from the nineteen-line one printed here, so count the lines on your own screen before you tell the class "nineteen". The recipe (last line first, then your own `File` line) does not change.

- [ ] **Print the whole Week 21 workbook** (`workbook/week-21.md`, every section down to the Self-Check). **Stop before the ✅ Answers section at the end** — that is a `<details>` block with every answer in it, so do not print it for the student.
- [ ] **Find Week 14's hand-formatted table printout**, on paper if you still have it, or re-run their old file and print it. **The Hook is built on putting it next to pandas's output**, and it takes ten seconds if you prepared and four minutes if you did not.
- [ ] **Check `squad_data.py` still exists and still runs.** Today imports it once.
- [ ] **Print the blank ten-row grid** (Figure 21.6, left panel). The student fills in their own week on it before typing anything.
- [ ] **Type and run the code yourself.** Two files. First, `table.py`:

```python
"""table.py - the twelve records, handed to pandas."""

import pandas as pd                        # everybody calls it pd
from squad_data import squad               # the twelve dictionaries from Week 14

print("pandas version:", pd.__version__)
print("how many records:", len(squad))

squad_df = pd.DataFrame(squad)             # a list of dicts, straight in
print()
print(squad_df)

print()
print(squad_df.head())

print()
squad_df.info()

print()
print(squad_df["runs"])
print("the whole table is a:", type(squad_df))
print("one column is a    :", type(squad_df["runs"]))
```

Run `python3 table.py`. You must see **exactly** this (with your own version number on line 1):

```text
pandas version: 1.5.3
how many records: 12

     name     team  runs  balls    out
0    Asha  Falcons    48     32   True
1    Ravi  Falcons    12     20   True
2    Nita  Falcons    77     55  False
3     Sam  Falcons     5      9   True
4   Kabir   Tigers    63     41   True
5   Meera   Tigers    30     28  False
6     Dev   Tigers     0      3   True
7    Zara   Tigers    41     39   True
8   Iqbal    Hawks    55     44   True
9    Lena    Hawks    22     18   True
10   Omar    Hawks    90     61  False
11  Priya     Owls   104     70  False

    name     team  runs  balls    out
0   Asha  Falcons    48     32   True
1   Ravi  Falcons    12     20   True
2   Nita  Falcons    77     55  False
3    Sam  Falcons     5      9   True
4  Kabir   Tigers    63     41   True

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    12 non-null     object
 1   team    12 non-null     object
 2   runs    12 non-null     int64 
 3   balls   12 non-null     int64 
 4   out     12 non-null     bool  
dtypes: bool(1), int64(2), object(2)
memory usage: 524.0+ bytes

0      48
1      12
2      77
3       5
4      63
5      30
6       0
7      41
8      55
9      22
10     90
11    104
Name: runs, dtype: int64
the whole table is a: <class 'pandas.core.frame.DataFrame'>
one column is a    : <class 'pandas.core.series.Series'>
```

Second, `ages.py` — the planted surprise:

```python
"""ages.py - one missing age, and what it does to the whole column."""

import pandas as pd

# --- a DataFrame from a dictionary of columns -------------------------------
# each KEY becomes a column name; each LIST becomes that column's values
ages = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, 13, 12, 11],
})
print(ages)
ages.info()

# --- now with one age never written down -----------------------------------
holed = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, None, 12, 11],            # Ravi's age is missing
})
print()
print(holed)
holed.info()
print()
print(holed["age"])
```

Real output:

```text
   name  age
0  Asha   12
1  Ravi   13
2  Nita   12
3   Sam   11
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    4 non-null      object
 1   age     4 non-null      int64 
dtypes: int64(1), object(1)
memory usage: 192.0+ bytes

   name   age
0  Asha  12.0
1  Ravi   NaN
2  Nita  12.0
3   Sam  11.0
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   name    4 non-null      object 
 1   age     3 non-null      float64
dtypes: float64(1), object(1)
memory usage: 192.0+ bytes

0    12.0
1     NaN
2    12.0
3    11.0
Name: age, dtype: float64
```

- [ ] **Break it on purpose, twice.**
  1. Change `squad_df["runs"]` to `squad_df["Runs"]`, capital R. You get a **nineteen-line** traceback ending in `KeyError: 'Runs'`. Count the lines. Read only the last one. That is the whole skill and you will model it in front of them.
  2. Change `pd.DataFrame` to `pd.dataframe`, lower-case d. You get `AttributeError: module 'pandas' has no attribute 'dataframe'` (on pandas 1.5.3 / Python 3.10 there is no suggestion; some other versions add `Did you mean: 'DataFrame'?`). The quoted name is the clue.
- [ ] **Look hard at the two `age` columns in `ages.py`.** `12` and `12.0`. If that does not make you look twice, read it again — that second look is what you are trying to produce in the room.
- [ ] **Put Week 14's printout next to pandas's printout on your desk.** Look at them side by side for ten seconds. That is the Hook, and you should have felt it before they do.

### 5 minutes on the day

- [ ] Editor open, terminal in the same folder, `squad_data.py` present. **Run the one-line pandas check again** — it takes four seconds and buys peace of mind.
- [ ] `table.py` and `ages.py` **deleted or renamed** — they type them.
- [ ] **Week 14's paper printout on the table, face down.** You are going to reveal it.
- [ ] Blank ten-row grid printed and ready for the activity.
- [ ] Workbook out, open at **Practice Set A, question A2** (the snack `info()` prediction table). **A2's answer column filled in pen before any code runs.**
- [ ] Bug Log out, with the Week 17 `<U21` entry and the Week 18 `float64` entry **findable** — today's silent surprise is the same rule for the third time and the student should find their own old notes.

### Fallback if the laptop or the install fails

**This week's paper version is unusually good**, because both of today's commands produce *printouts you read*, and a printout can be on paper.

1. **The reveal.** Week 14's hand-formatted table and pandas's output, side by side. Ask what is different. *(Answer: nothing much — and one of them took thirty lines and the other took one.)* That is the Hook, on paper, complete.
2. **Label the printout.** Hand them the pandas output and four coloured pens. Circle and label: the **column names**, the **index**, one **value**, and one whole **column**. Then the hard question: *"how many columns are there?"* Five. *"Is the index one of them?"* No. **That is objectives 2 and 4, on paper.**
3. **Read `info()` out loud, line by line, from the printed page.** Eleven lines. For each, they say in their own words what it tells you. This is *literally* the homework and it needs no computer at all. **Objective 3, complete.**
4. **The hole, on paper.** Show them the two `age` columns printed side by side — `12, 13, 12, 11` and `12.0, NaN, 12.0, 11.0`. Ask three questions: *"what's different about Ravi? What's different about everybody else? And why should everybody else change when only Ravi's is missing?"* Then have them find the Week 17 and Week 18 Bug Log entries and say what the three have in common. **Objective 5, and it lands harder on paper than on screen** because the two columns are next to each other instead of forty lines apart.
5. **Build a DataFrame on paper.** Blank ten-row grid, four column names of their choosing, ten rows of their own week. Then write out, by hand, what `info()` *would* say about it: how many entries, how many columns, and for each column its name, its non-null count and its dtype. **That is genuinely the whole homework**, done in pencil, and it is a harder and better exercise than typing it.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` in the lesson | Do not debug live for more than three minutes. Switch to the paper version — it delivers all five objectives — set the install as homework with the three commands written down, and check it yourself before Week 22, **which cannot be done on paper.** |
| `pip` works but `python3` still cannot find pandas | `python3 -m pip install pandas`. Same Python either way; that is the whole point of the `-m`. |
| A file called `pandas.py` in the folder | You get `AttributeError: module 'pandas' has no attribute '__version__'` or similar nonsense. Their file is being imported instead of the real pandas. Rename it. **Standing rule all year, fourth appearance: never name a file after a library.** |
| The install is very slow | Normal. pandas is a much bigger download than numpy. This is why it is on the night-before list. |
| `squad_data.py` is missing | Type the four-row `ages` DataFrame instead and use it for everything. It delivers all five objectives; you lose only the "I wrote thirty lines to do that" moment, which you can replace by showing them Week 14's printout and telling them. |
| The version is 2.x and `memory usage` differs | Fine. Only traceback lengths and paths may also differ (count the lines on your own screen). |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Thirty Lines, or One | 7 | 7 | Week 14's hand-built table, revealed next to pandas's |
| 🧠 Concept — Names On Top, Index Down the Side | 16 | 23 | DataFrame and Series; the index; the two commands; predictions **in pen** |
| 💻 Live-Code Together — `table.py` | 18 | 41 | Build, head, info, one column. Two deliberate mistakes: one loud, one silent |
| 🎲 Their Turn — Your Own Week, In Ten Rows | 20 | 61 | Build it on paper, then in code, then read `info()` out loud |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Thirty Lines, or One (7 minutes)

**Do this:** Week 14's printout face down on the table. Nothing on the screen. Sit down.

**Say this:**

> "Do you remember Week 14? You had twelve cricketers, each one a dictionary, and you wanted them printed as a neat table. Names lined up, numbers lined up, a header row across the top.
>
> How long did that take you?"

Let them remember. It was most of a lesson.

> "You wrote a header line with format codes in it — `:<7` and `:>5` and all of that. Then you wrote a loop. Then you had to make the header widths match the row widths, and when they didn't, the whole thing went wonky and you had to count characters.
>
> Here's what you produced."

**Do this:** Turn the printout over. Let them look at it. It is genuinely good work and they should be a bit proud of it.

```text
 #  NAME   TEAM      RUNS BALLS  OUT  
----------------------------------------
 0  Asha   Falcons     48    32  True
 1  Ravi   Falcons     12    20  True
 2  Nita   Falcons     77    55  False
 3  Sam    Falcons      5     9  True
 4  Kabir  Tigers      63    41  True
```

> "That's yours. It's good. It took you about thirty lines and a lot of counting.
>
> Now watch."

**Do this:** On the screen, in front of them, type these three lines and nothing else. This is the one moment in the year you type instead of them.

```python
import pandas as pd
from squad_data import squad
print(pd.DataFrame(squad))
```

Run it:

```text
     name     team  runs  balls    out
0    Asha  Falcons    48     32   True
1    Ravi  Falcons    12     20   True
2    Nita  Falcons    77     55  False
3     Sam  Falcons     5      9   True
4   Kabir   Tigers    63     41   True
5   Meera   Tigers    30     28  False
6     Dev   Tigers     0      3   True
7    Zara   Tigers    41     39   True
8   Iqbal    Hawks    55     44   True
9    Lena    Hawks    22     18   True
10   Omar    Hawks    90     61  False
11  Priya     Owls   104     70  False
```

**Do this:** Say nothing for five seconds. Put the paper next to the screen.

> **Say this:** "One line. `pd.DataFrame(squad)`. **Your own data, unchanged — the same twelve dictionaries, the same file.**
>
> Look at what it did without being asked. It found the column names. It worked out how wide each column needed to be. It lined every column up in a tidy block, numbers and words alike. It numbered the rows. And it did the two-digit row numbers — look at 10 and 11 — lined up under the one-digit ones, which is the exact thing that went wrong for you in Week 14."

> "Now. Was Week 14 a waste of time?"

Let them answer. Steer, honestly:

> "No — for two reasons. **One:** you now know what that one line is doing, because you have done it by hand. Someone who has only ever called `pd.DataFrame` thinks it's magic. You know it's a header row and some width arithmetic. **Two:** in a minute I'm going to show you something this table is quietly getting wrong, and you'll only spot it because you know what's underneath.
>
> This thing has a name. It's called a **DataFrame**, and it's the container we'll use for the rest of the year — and the rest of Level 3, and honestly the rest of your life if you ever work with data."

**Do this:** Write on the board and leave it up:

> **DataFrame** — a table where the columns have names and the rows have an index.

> "And here's the one sentence that says what it is, given everything you already know:
>
> **A DataFrame is a numpy array with the labels put back on — and each column is allowed to be a different kind of thing.**
>
> Remember Week 17, when I made you rub the words off your table with a rubber? **You're getting them back today.** And you now know exactly what they were worth, because you've spent four weeks without them."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What's different between your table and pandas's?" | Almost nothing — and one took thirty lines. | If they list small formatting differences, agree, and then ask "which of those differences would you rather spend a lesson on?" |
| "What did pandas work out for itself?" | The column names, the widths, the alignment, the row numbers. | Point at the 10 and 11 lining up. That is the exact bug they had. |
| "Where did the column names come from?" | The dictionary keys. | If they do not know, open `squad_data.py` and read one record out loud. The keys are right there. |
| "Was Week 14 wasted?" | No — you now know what the one line is doing. | If they say yes, ask: "so what *is* it doing?" A student who can answer has just proved the point. |
| "What did you lose in Week 17, and what are you getting back?" | The labels — which column is which and whose row is whose. | Put the rubbed-out graph paper next to the screen if you still have it. |
| "Does this replace numpy?" | No — it's built on top of it. | This will come up. Answer plainly: every column is a numpy array underneath, and every axis and mask you learned still does the actual work. |

---

### 🧠 Concept — Names On Top, Index Down the Side (16 minutes)

**Do this:** Both printouts still on the table. Board work.

**Say this — part 1, the two containers:**

> "There are exactly two containers in pandas that you need. Two. That's the whole thing."

Write both up and leave them:

> **DataFrame** — a whole table. Named columns, an index down the side. Each column can be a different kind of thing.
> **Series** — one column on its own, still carrying the row labels and its own name.

> "And the relationship between them is simple: **a DataFrame is a set of Series that all share one index.** When you ask for one column, you get one Series out.
>
> Here's the picture. A numpy array is a table of numbers drawn on **graph paper** — you find things by counting squares. 'Third column along, I think.' A DataFrame is the same table printed as a proper **spreadsheet**: headings across the top, row numbers down the side. Same numbers. But now you can say *the runs column* instead of *column 2, probably.*"

**Do this:** Draw the four-week comparison table on the board. It is the single most useful thing you can leave up.

```text
                 one row is    named columns?  maths at once?  mixed kinds?
W14 list of dicts   a dict          yes             no            yes
W17 numpy array     numbers         NO              yes           NO
W21 DataFrame       a labelled row  YES             YES           YES
```

> "Look at the bottom row. **It's got every yes.** So why didn't we start here?
>
> Two reasons, and both are honest. **One:** pandas is slower and much more complicated — there are about six ways to write everything, and you'd have drowned. **Two, and it's the real one:** if I'd given you named columns on day one, you'd never have known what they were worth. You've spent four weeks keeping a `names` array and a `tests` array next to your data and hoping the lengths matched. **Last week one of them didn't match and you got an error.** Today that stops."

**Say this — part 2, the index, and be firm:**

> "Now the thing that confuses everybody. Look at pandas's printout. Down the left-hand side: 0, 1, 2, 3, and so on. What is that?"

*The row numbers.*

> "Right — and here's the important bit. **That is not a column.**"

Write on the board: **the index is the row's name, not a value in the table.**

> "Prove it with me. Count the column names across the top of that printout."

*Name, team, runs, balls, out. Five.*

> "Five. In a minute, `info()` is going to tell us 'total 5 columns'. **Five, not six.** The index isn't in the count.
>
> And if you try to ask for it like a column — `df[0]` — you get a `KeyError`, because there is no column called zero.
>
> Think of it as **the name on a coat peg.** The peg has a name so you can find your coat. The name isn't your coat.
>
> Now — right now those names are just 0, 1, 2, 3, and honestly they're not doing anything useful for you yet. **They start earning their keep next week**, when you throw some rows away and the numbers stop being in order — and then having the row keep its original name turns out to matter quite a lot."

**Say this — part 3, the two commands:**

> "Two commands. You will run these on every single table you ever meet, for the rest of your life, before you do anything else with it."

Write them up:

```text
df.head()   ->  what does it LOOK like?      (the first five rows)
df.info()   ->  can I TRUST it?              (rows, columns, kinds, holes)
```

> "`head()` is the easy one. First five rows. `head(3)` gives you three. That's all it does, and it's the most-used command in pandas.
>
> `info()` is the one that matters, and it prints **twelve lines**, and I am going to make you read every single one of them out loud. Because **every line of it is a check that can fail.**
>
> Does it say twelve rows? You typed twelve records — does it agree?
>
> Does it say five columns? Count them.
>
> And here's the new one, and it's the whole reason `info()` exists: for every column, it tells you **how many of its cells actually have something in them.** It calls that the *non-null count*. Twelve out of twelve means nothing's missing. **Eleven out of twelve means somebody's data is gone and you were about to average it anyway.**"

> "One warning about `info()` before we type it. You **don't** put `print()` round it. It prints for itself. If you write `print(df.info())` you get the report, and then the word `None` underneath it, which looks broken and isn't."

**Say this — part 4, one more word:**

> "Last word before you type, and it's the one I want you watching for. **`object`.**
>
> When `info()` tells you what kind of thing is in a column, it'll say `int64` for whole numbers and `float64` for decimals — both of those you know from Week 17. And for text it says **`object`**, which is a silly name meaning 'general Python stuff', which in practice means writing.
>
> Here's why it matters. If a column you *meant* to be numbers says `object`, **something has gone wrong** — there's a word or a stray space or an empty cell in there somewhere, and none of your arithmetic will work. `object` on a number column is the loudest alarm bell in pandas. Watch for it all year."

**Say this — part 5, Practice Set A, question A2, in pen:**

> "**Practice Set A, question A2, in pen, before we touch the keyboard.**
>
> There's a small DataFrame written out for you — six snacks, four columns. **Predict `info()`.** How many entries? How many columns? And for each of the four columns: its name, how many of its cells are filled in, and what kind of thing it holds.
>
> That's about eighteen guesses. Some of them are easy. **At least one of them is not**, and I'm not telling you which. In pen. Five minutes."

**Do this:** Circulate. Confirm nothing. The `stars` column has a `None` in it and will come out `float64` with `5 non-null` — do not let a face give that away.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What are the two containers in pandas?" | DataFrame (the table) and Series (one column). | If they add more, cut it back: two. |
| "What comes back from `df["runs"]`?" | A Series — one column, with the index and its own name. | If they say "a list" or "an array", let it stand for now; the live-code prints the type. |
| "How many columns has the squad table got?" | Five. | If they say six, point at the column names and count them. Then ask what the sixth one would be called. |
| "Is the index a column?" | No — it's the row's name. | Do not just assert it. Ask: "what's it called, then? Every column's got a name." |
| "What does `head()` tell you? What does `info()` tell you?" | What it looks like; whether you can trust it. | If they conflate them, say: "one is a photo, one is a health check." |
| "What is a non-null count?" | How many cells in that column actually have something in them. | If unsure: "if you typed twelve and it says eleven, what happened to one of them?" |
| "You expected numbers and `info()` says `object`. Good or bad?" | Bad — there's text hiding in a number column. | Any answer that treats it as a warning is fine. |
| "Why didn't we start with pandas in Week 14?" | Because we wouldn't have known what named columns were worth. | Also acceptable: "because it's slower and more complicated." Both are true. |

---

### 💻 Live-Code Together — `table.py` (18 minutes)

**You never touch the keyboard** from here on. Predictions before every run.

**Step 1 (3 min).** New file, `table.py`. Prove the install first.

```python
"""table.py - the twelve records, handed to pandas."""

import pandas as pd                        # everybody calls it pd
from squad_data import squad               # the twelve dictionaries from Week 14

print("pandas version:", pd.__version__)
print("how many records:", len(squad))
```

Run it. Real output:

```text
pandas version: 1.5.3
how many records: 12
```

> **Say this:** "Two lines and the whole install is proved. If you get a version number, pandas is on your machine and working.
>
> And `as pd` — same idea as `as np` from Week 17. A nickname, inside this file only. **And exactly like `np`, everybody on Earth writes `pd`.** Not `pandas`, not `panda`, not `p`. Every book, every tutorial, every bit of code you'll ever paste. Follow the convention; it's how strangers read each other's work.
>
> The second line is a check, not decoration. **Twelve records.** Remember that number — in about four minutes something else is going to tell us twelve, and we want the two to agree."

**Step 2 (3 min).** One call.

```python
squad_df = pd.DataFrame(squad)             # a list of dicts, straight in
print()
print(squad_df)
```

Run it. Real output:

```text

     name     team  runs  balls    out
0    Asha  Falcons    48     32   True
1    Ravi  Falcons    12     20   True
2    Nita  Falcons    77     55  False
3     Sam  Falcons     5      9   True
4   Kabir   Tigers    63     41   True
5   Meera   Tigers    30     28  False
6     Dev   Tigers     0      3   True
7    Zara   Tigers    41     39   True
8   Iqbal    Hawks    55     44   True
9    Lena    Hawks    22     18   True
10   Omar    Hawks    90     61  False
11  Priya     Owls   104     70  False
```

> **Say this:** "Note the capital **D** and capital **F** in `pd.DataFrame`. Both capitals. Get one wrong and pandas will tell you so, quite politely, in a minute.
>
> Now — where did the column names come from? Open `squad_data.py` and read me one record."

*`{"name": "Asha", "team": "Falcons", "runs": 48, ...}`*

> "**The keys.** Each key became a column name, each dictionary became a row. Twelve dictionaries, twelve rows. Five keys, five columns. Nothing was invented.
>
> And notice `out` — the `True`/`False` column. Sitting happily next to columns of numbers and columns of words. **Try that in a numpy array** and every number in the whole table turns into writing, which is exactly what Week 17 warned you about. This is the thing a DataFrame can do that an array cannot."

**Step 3 (3 min).** `head()`.

```python
print()
print(squad_df.head())
```

**Ask before running:** "How many rows will that print?"

Run it. Real output:

```text

    name     team  runs  balls    out
0   Asha  Falcons    48     32   True
1   Ravi  Falcons    12     20   True
2   Nita  Falcons    77     55  False
3    Sam  Falcons     5      9   True
4  Kabir   Tigers    63     41   True
```

> **Say this:** "Five. `head()` always gives you the first five unless you tell it otherwise — `head(3)` gives three.
>
> Why does that exist? Because a real table has fifty thousand rows in it and you do **not** want to print fifty thousand rows to check that the column names came out right. `head()` is 'let me have a look at it'.
>
> Now — four things in that printout. Name all four."

Take them: column names, index, values, alignment.

> "And which of those four is not part of your data?"

*The index.*

> "The index. **Not a column.** Count the column names. Five. Hold that number."

**Step 4 (5 min).** `info()`, read out loud, all of it. **Do not rush this — it is the objective.**

```python
print()
squad_df.info()
```

**Ask before running:** "It's going to say a number of rows and a number of columns. What will they be?"

*Twelve and five.*

Run it. Real output:

```text

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    12 non-null     object
 1   team    12 non-null     object
 2   runs    12 non-null     int64 
 3   balls   12 non-null     int64 
 4   out     12 non-null     bool  
dtypes: bool(1), int64(2), object(2)
memory usage: 524.0+ bytes
```

**Do this:** Now go line by line. Point at each one on the screen and ask them to say it in their own words before you do. This takes three minutes and it is the most valuable three minutes of the lesson.

> "**Line one.** `<class 'pandas.core.frame.DataFrame'>`. What's it telling you?"

*It's a DataFrame.*

> "It's a DataFrame. Which sounds pointless — of course it is, you just made one. But it's the first thing to check when something baffling happens, because if you accidentally handed it *one column* it would say `Series` here and you'd know instantly.
>
> **Line two.** `RangeIndex: 12 entries, 0 to 11`. Two facts in there. What are they?"

*Twelve rows. Numbered 0 to 11.*

> "Twelve rows, named 0 to 11. And what did line two of the *file* say, four minutes ago?"

*Twelve records.*

> "Twelve. **They agree.** That's a check and it just passed. If this said eleven, you'd have lost a cricketer somewhere between the file and the table, and you'd want to know that now rather than in an hour.
>
> **Line three.** `Data columns (total 5 columns)`. Count them on the printout above."

*Five.*

> "Five. And the index isn't one of them, which is the thing I've been going on about.
>
> **Now the little table.** Four headings: a number, the Column name, the **Non-Null Count**, and the **Dtype**. One row per column. Read me the `runs` line."

*Two, runs, twelve non-null, int64.*

> "In English: **column number 2 is called `runs`, twelve of its twelve cells have something in them, and they're whole numbers.**
>
> That middle number is the new idea and it is the reason `info()` exists. **Non-null means 'not empty'.** Twelve out of twelve means nothing's missing. If it said `9 non-null` you'd have three holes, and if you'd averaged that column without looking you'd have got an answer and never known.
>
> Now read me the `name` line."

*Zero, name, twelve non-null, object.*

> "**`object`.** That's pandas's word for 'general Python stuff', which nearly always means text. `name` is words, so `object` is correct here.
>
> But **write this down**: if a column you *meant* to be numbers ever says `object`, something is wrong. There's a word in it, or a stray space, or an empty cell — and none of your arithmetic will work. `object` on a number column is the loudest alarm bell in pandas.
>
> **Second-to-last line.** `dtypes: bool(1), int64(2), object(2)`. That's a tally. One true/false column, two whole-number, two text. Add them up."

*Five.*

> "Five, which matches. Another free check.
>
> **Last line.** `memory usage`. Ignore it. It's the least interesting line on the page and everybody stares at it."

**Step 5 — ⚠️ FIRST DELIBERATE MISTAKE (2 min).** Dictate it wrongly. This one is loud, and the *length* of the error is the lesson.

> **Say this:** "Now pull out one column. Square brackets and the name — type `print(squad_df["Runs"])`."

```python
print()
print(squad_df["Runs"])
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3802, in get_loc
    return self._engine.get_loc(casted_key)
  File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 165, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 5745, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 5753, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'Runs'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "table.py", line 20, in <module>
    print(squad_df["Runs"])
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pandas/core/frame.py", line 3807, in __getitem__
    indexer = self.columns.get_loc(key)
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3804, in get_loc
    raise KeyError(key) from err
KeyError: 'Runs'
```

**Do this:** Let them look at the wall of text. Let it be alarming for five seconds.

> **Say this:** "Right. That is **nineteen lines** of error for one wrong letter. Welcome to pandas.
>
> Do not panic and do not read the middle. **Read the last line.** What does it say?"

*KeyError: 'Runs'.*

> "`KeyError: 'Runs'`. And you have met `KeyError` before — Week 13, dictionaries. It means *'there's no key with that name.'* A DataFrame's columns work exactly like a dictionary's keys, which is not a coincidence: you built this thing out of dictionaries.
>
> So — is there a column called `Runs`?"

*No. It's `runs`, lower case.*

> "Lower case. **Column names are text, and text is fussy about capitals.** One letter.
>
> Two more things about this traceback, and then we move on. Look at the middle: *'The above exception was the direct cause of the following exception.'* That means pandas hit a problem deep inside itself, then wrapped it up and handed it to you. **You get told twice.** Annoying, and harmless.
>
> And look for the `File` line that names *your* file. There it is: `File "table.py", line 20`. **That's the only line in nineteen that you can do anything about.** Everything else is inside pandas. Find your own file's line, read the last line, ignore the rest."

Fix it:

```python
print()
print(squad_df["runs"])
print("the whole table is a:", type(squad_df))
print("one column is a    :", type(squad_df["runs"]))
```

Run it. Real output:

```text

0      48
1      12
2      77
3       5
4      63
5      30
6       0
7      41
8      55
9      22
10     90
11    104
Name: runs, dtype: int64
the whole table is a: <class 'pandas.core.frame.DataFrame'>
one column is a    : <class 'pandas.core.series.Series'>
```

> **Say this:** "Three things in that output and the last line is the good one.
>
> **One: the index came with it.** 0 to 11, down the left. The column did not forget which rows its values belong to. Compare that with `arr[:, 2]` in numpy, which gives you twelve bare numbers and no idea whose they are.
>
> **Two: `Name: runs, dtype: int64`.** It knows its own name *and* its own kind. An array knew its kind. It never knew its name.
>
> **Three:** the table is a `DataFrame` and one column is a `Series`. There it is, in writing. **Two containers, and that's all there are.**"

**Bug Log the `KeyError`**, with the fix as "check the capital letters — column names are case-sensitive" and one extra note: *"pandas tracebacks are long. Read the last line, then find your own filename."*

**Step 6 — ⚠️ SECOND DELIBERATE MISTAKE (2 min).** This one **does not crash.** New file, `ages.py`. Do not warn them.

> **Say this:** "New file, `ages.py`. And a different way to build a DataFrame — from a dictionary where each key is a column name and each list is a whole column."

```python
"""ages.py - one missing age, and what it does to the whole column."""

import pandas as pd

ages = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, 13, 12, 11],
})
print(ages)
ages.info()
```

**Ask before running:** "What dtype will `age` be?" *int64.*

Run it. Real output:

```text
   name  age
0  Asha   12
1  Ravi   13
2  Nita   12
3   Sam   11
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    4 non-null      object
 1   age     4 non-null      int64 
dtypes: int64(1), object(1)
memory usage: 192.0+ bytes
```

> **Say this:** "`int64`, four non-null. As predicted. Now — somebody forgot to write Ravi's age down. In Python, 'there's nothing here' is `None`. Type the same table again with `None` where the 13 was."

```python
holed = pd.DataFrame({
    "name": ["Asha", "Ravi", "Nita", "Sam"],
    "age":  [12, None, 12, 11],            # Ravi's age is missing
})
print()
print(holed)
holed.info()
```

**Ask before running:** "Will it crash? And what will change?"

Most say it will crash, or that only Ravi's row changes. Run it. Real output:

```text

   name   age
0  Asha  12.0
1  Ravi   NaN
2  Nita  12.0
3   Sam  11.0
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   name    4 non-null      object 
 1   age     3 non-null      float64
dtypes: float64(1), object(1)
memory usage: 192.0+ bytes
```

**Do this:** Silence. Let them read it.

> **Say this:** "Read me Asha's age."

*Twelve point zero.*

> *(pause)* "**Twelve point zero.** You typed `12`. Nobody touched Asha. Read me Nita's."

*Twelve point zero.*

> "And Sam's is `11.0`. **Every whole number in that column grew a decimal point, and only Ravi's was missing.**
>
> Three things changed and nothing warned you about any of them. Find all three in the output."

Take them: `None` became `NaN`; the numbers grew decimal points; the dtype went `int64` → `float64` and the count went `4` → `3 non-null`.

> "**`NaN`** is pandas for 'there's nothing here'. The letters stand for 'Not a Number', which is confusing, because `NaN` **is** a decimal number as far as the computer is concerned. And that's the whole explanation.
>
> Say it with me: a column holds **one kind of thing.** That's Week 17 and it hasn't changed. `NaN` is a decimal. So what's the only kind that can hold both `12` and `NaN`?"

*Decimals.*

> "Decimals. A whole-number box has nowhere to put a `NaN`. So pandas converted the **entire column**, silently, because there was nothing else it could do.
>
> Now go and find your Bug Log. Week 17: what happened when you put one word in a list of numbers?"

*Everything became text.*

> "And Week 18-ish, when one number in a list had a decimal point?"

*Everything became float64.*

> "And today, when one cell is empty?"

*Everything becomes float64.*

> "**Three times. Same rule, three costumes.** *A container picks the one kind that can hold everything.*
>
> And here's the thing to actually take away, because it's a check you can use forever: **if you typed whole numbers and pandas is showing you decimals, you have a hole somewhere.** Go and find it. `info()` will tell you which column and how many."

**Bug Log this**, under *errors with no error message*. In the "what the student sees" column: *"12 printed as 12.0."*

---

### 🎲 Their Turn — Your Own Week, In Ten Rows (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–5:** the **blank paper template.** Four column names of their choosing, ten rows of their own week, filled in with a pencil.
- **Minutes 5–12:** the same table typed as `pd.DataFrame({...})`, then `head()`.
- **Minutes 12–18:** **`info()` read out loud, line by line**, in their own words. This is the objective and it is not optional.
- **Minutes 18–20:** one `None` goes in, on purpose, and they predict what changes before running it.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the printed **blank ten-row grid** (Figure 21.6, left panel); a pencil; the workbook open at Practice Set A, question A2, with the snack predictions already in pen; the Bug Log with the Week 17 and Week 18 entries findable.

**On the screen:** a new file, `myweek.py`.

![Two ten-row tables: a blank template with question-mark headers, and a filled example with a NaN](../figures/fig-w21-6-my-week-blank-and-filled.svg)
*Figure 21.6 — The blank on the left is what they fill in with a pencil. The one on the right is what finished looks like.*

**The one rule that makes this work:** *the paper goes first.* They fill in the grid with a pencil before they type anything, so the data is a decision they made rather than something that appeared as they typed.

### Part 1 — the paper table (5 minutes)

> **Say this:** "Ten rows about **your own week.** Ten days — you can go over a weekend, that's fine. And four columns, and **you choose them.** Three of them have to be numbers you can actually find out.
>
> Some suggestions if you're stuck: hours of sleep. Hours of screen time. Steps, if your phone counts them. Minutes of homework. Number of times somebody in your house said your name in that irritated voice.
>
> One column should be words — the day of the week is the obvious one.
>
> Fill it in with a pencil. **Guess if you have to, but write down that you guessed.**"

Two things to insist on while they fill it in:

1. **At least one column must be decimals** — hours of sleep as `7.5` rather than `7` is the natural one. They will need it in a moment.
2. **At least one column must be whole numbers** — steps, or minutes. **They will need this one even more**, because it is the column the hole goes into.

### Part 2 — type it (7 minutes)

The dict-of-columns form. **Read it out loud as they type:** *"key, colon, and then a whole column running down the page."*

```python
"""myweek.py - ten days of my own week, as a DataFrame."""

import pandas as pd

my_week = pd.DataFrame({
    "day":    ["Mon", "Tue", "Wed", "Thu", "Fri",
               "Sat", "Sun", "Mon", "Tue", "Wed"],
    "sleep":  [7.5, 8.0, 6.5, 7.0, 6.0, 9.5, 9.0, 7.5, 8.0, 7.0],
    "screen": [1.5, 2.0, 3.5, 1.0, 4.0, 5.5, 4.5, 2.0, 1.5, 3.0],
    "steps":  [6200, 8100, 4300, 7700, 3900, 11200, 9800, 6600, 7400, 5100],
})

print(my_week)
print()
print(my_week.head(3))
```

**Ask before running:** "How many rows? How many columns? And which of the four will be `object`?"

Real output:

```text
   day  sleep  screen  steps
0  Mon    7.5     1.5   6200
1  Tue    8.0     2.0   8100
2  Wed    6.5     3.5   4300
3  Thu    7.0     1.0   7700
4  Fri    6.0     4.0   3900
5  Sat    9.5     5.5  11200
6  Sun    9.0     4.5   9800
7  Mon    7.5     2.0   6600
8  Tue    8.0     1.5   7400
9  Wed    7.0     3.0   5100

   day  sleep  screen  steps
0  Mon    7.5     1.5   6200
1  Tue    8.0     2.0   8100
2  Wed    6.5     3.5   4300
```

> **Say this:** "Look at `day`. **'Mon' appears twice** — rows 0 and 7. Is that a problem?
>
> No — and this is what the index is quietly for. Two rows can have the same `day`, but they should not have the same **index**. Row 0 and row 7 are different rows, even though their day column says the same thing. The index is the row's *name*, and each row is meant to have its own. (pandas will not stop you giving two rows the same name, but then asking for that name gives you two rows back, which is almost never what you want.)"

### Part 3 — `info()`, read out loud (6 minutes)

```python
print()
my_week.info()
```

Real output:

```text

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   day     10 non-null     object 
 1   sleep   10 non-null     float64
 2   screen  10 non-null     float64
 3   steps   10 non-null     int64  
dtypes: float64(2), int64(1), object(1)
memory usage: 448.0+ bytes
```

**Do this:** They read it out loud. Every line. In their own words. Do not do it for them — you did that in Step 4 and the point is that they can now do it themselves.

Then three questions:

> **"Does the number of entries match the number of rows you filled in on the paper?"** Ten. If not, they have lost or gained a row while typing and the paper just caught it.
>
> **"Which column is `object`, and is that right?"** `day`, and yes — it is words.
>
> **"Which are `float64`, and why?"** `sleep` and `screen`, because they typed values like `7.5`. **And no holes anywhere**, so that is the only reason. Hold that thought.

### Part 4 — the hole, predicted first (2 minutes)

> **Say this:** "Last thing. Go to your `steps` column and change **one** value to `None`. Any one. Pretend your phone was flat that day.
>
> Before you run it: **write down three things you think will change.**"

Take their predictions, then run.

Real output:

```text
   day  sleep  screen   steps
0  Mon    7.5     1.5  6200.0
1  Tue    8.0     2.0  8100.0
2  Wed    6.5     3.5  4300.0
3  Thu    7.0     1.0  7700.0
4  Fri    6.0     4.0  3900.0
5  Sat    9.5     5.5     NaN
6  Sun    9.0     4.5  9800.0
7  Mon    7.5     2.0  6600.0
8  Tue    8.0     1.5  7400.0
9  Wed    7.0     3.0  5100.0
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   day     10 non-null     object 
 1   sleep   10 non-null     float64
 2   screen  10 non-null     float64
 3   steps   9 non-null      float64
dtypes: float64(3), object(1)
memory usage: 448.0+ bytes
```

> **Say this:** "**Still ten entries.** The row didn't go anywhere — it's still row 5 and it still has a day in it. The *cell* is empty; the row is fine.
>
> But `steps` says **9 non-null** now, and the dtype is `float64`, and every step count on the page has grown a decimal point. `6200` is `6200.0`. **Nobody's steps changed.**
>
> Now look at the tally line, and compare it with the tally line from a minute ago. Read me both."

*Before: `float64(2), int64(1), object(1)`. After: `float64(3), object(1)`.*

> "**The `int64` has vanished completely.** Not moved, not renamed — gone, because there is now no whole-number column left in the whole table. One missing step count wiped out an entire category from the summary line.
>
> And notice that the two tallies both still add up to four, which is the number of columns. **That check still passes, and the table is still not what you typed.** Same lesson as last week's normalization: a check that cannot fail is not much of a check.
>
> One habit to take from this, and it is worth having: **read the per-column lines, not the tally.** The per-column lines have names on them — `steps  9 non-null  float64` tells you *which* column and *how many* are missing. The tally just says how many of each kind there are. **The line with a name on it is always the more useful line.**"

### What "finished" looks like

- A paper grid, filled in with a pencil, ten rows, four columns the student chose.
- `myweek.py` builds the same table with `pd.DataFrame({...})` and prints `head(3)` and `info()`.
- **The number of entries matches the number of rows on the paper.**
- The student can read every line of their own `info()` out loud, in their own words, without being prompted.
- One `None` has gone in, three changes were predicted first, and all three were found.
- Both of today's bugs are in the Bug Log — the nineteen-line `KeyError` and the silent `12.0`.
- The student can say why the index is not a column.

### Variation — easier

- **Five rows, not ten.** Every idea survives and the typing halves.
- **Three columns:** one of words, one of decimals, one of whole numbers. That is the minimum that makes `info()` interesting, because it produces all three dtypes.
- **Give them the `my_week` block already typed** and have them only add `head()` and `info()`. The learning today is in **reading** the output, not in typing the data.
- **Skip the `None` experiment in class** and demonstrate it yourself with the four-row `ages` table, which is small enough to see all at once.
- **Cut `df["col"]`.** The two commands are the objective. One column can wait for next week, which is entirely about picking things out.
- **Do the whole thing on paper** from the Fallback section: label a printed table, then write out what `info()` *would* say about their own grid. That is objectives 2, 3, 4 and 5 with no computer.

### Variation — harder

None of these need syntax from a later week.

1. **Array maths on a Series.** `my_week["sleep"] * 60` turns hours into minutes, and it is Week 18's `arr * 2` on a Series:

```python
print(my_week["sleep"] * 60)
```

```text
0    450.0
1    480.0
2    390.0
3    420.0
4    360.0
5    570.0
6    540.0
7    450.0
8    480.0
9    420.0
Name: sleep, dtype: float64
```

Then the good question: *"the index came through unchanged, and so did the name. Should the name still say `sleep` when the numbers are now minutes?"* **No, arguably — and pandas has no way of knowing.** A unit is a thing only you know about. That is a real and honest limitation.

2. **Make a column come out as `object` on purpose.** Put quotes round one of the step counts: `"6200"` instead of `6200`. The whole column becomes `object` (the values keep their own kinds: the numbers stay numbers and only the quoted one is text, unlike `NaN`, where every value really is converted to a decimal), and it is `10 non-null` so nothing looks missing. Then: *"which is worse — one hole that turns the column into decimals, or one quote mark that turns the column into `object`? And which is easier to spot?"* (The quote mark is worse and harder to spot, because the count still says 10 and the printed values still look like numbers. This is Week 16's CSV lesson and Week 17's `<U21` lesson, arriving for the third time.)
3. **Two rows with the same day.** Already true if they used Mon twice. Then: *"could two rows have the same index?"* They should not (pandas allows it, but a repeated name picks out two rows). *"So what is the index actually for?"* Giving each row its own name. That is a genuinely deep answer and Week 22 depends on it.
4. **Predict `info()` for a table you have not built.** Write out a dict-of-lists on paper, with one `None` and one quoted number hidden in it, and have them write the whole `info()` report before typing it. Then check. This is much harder than it sounds and it is the single best exercise in the week.
5. **Build the same ten rows both ways** — once as a dict of columns, once as a list of ten dictionaries — and print both. They are identical. Then: *"which was less typing? Which was less error-prone?"* (The dict of columns is less typing. The list of dicts is harder to get wrong, because each row's values sit next to their own names, so you cannot accidentally put a value in the wrong column.)
6. **The honest question.** *"This table says you slept 7.5 hours on Monday. Where did that number come from?"* Almost certainly a guess, or a phone that measures something adjacent to sleep. **Nothing in the DataFrame records how a number was obtained** — the column has a name and a kind and no history. That is the seed of Week 24's cleaning log and Week 34's honesty paragraph.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

> **🧑‍🏫 If a student asks:** pandas tracebacks are much longer than numpy's — nineteen lines is normal, and some are longer. **The rule does not change: read the last line, then find the `File` line that names your own file.** Everything in between is inside pandas and there is nothing you can do about it.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | "There's no pandas on this machine, or not on the one I'm using." | pandas is not installed, or `pip` installed it into a different Python than `python3` runs. | `python3 -m pip install pandas` — the `-m` makes it the *same* Python. Prove it with `python3 -c "import pandas; print(pandas.__version__)"`. |
| `KeyError: 'Runs'` at the end of **nineteen** lines | "There is no column with that name." | A capital letter, or a typo, or a stray space in the column name. Column names are case-sensitive text. | `squad_df["runs"]`. And read the name in the message — it quotes exactly what you asked for, which is the fastest way to spot the difference. |
| `KeyError: 0` | "There is no column called 0." | `squad_df[0]` — trying to get the first *row* by number. **Square brackets on a DataFrame mean columns, not rows.** | Rows come in Week 22, with `.loc` and `.iloc`. Today, ask for a column by its name. |
| `AttributeError: module 'pandas' has no attribute 'dataframe'` | "There's no `dataframe` in pandas." | Lower-case d. `pd.dataframe(...)`. | `pd.DataFrame(...)` — capital D **and** capital F. Read the quoted name and compare it with the spelling you meant (some versions add a "Did you mean" suggestion; read it if you see it). |
| `ValueError: All arrays must be of the same length` | "Your columns aren't the same height, so this isn't a table." | One list in the dictionary has more or fewer items than the others — usually a missed comma or one value too many. | Count the items in every list. This is Week 17's ragged-array error wearing a pandas coat, and it is good news: pandas refused rather than guessing. |
| `TypeError: 'method' object is not subscriptable` | "You used square brackets on something that needs round ones." | `df.head[3]` instead of `df.head(3)`. | `df.head(3)`. `head` is a verb — something the table *does* — so it takes round brackets. |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | "You tried to add a number to a word." | `df["runs"] + df["name"]` — adding a number column to a text column. | Only add columns of the same kind. Check `info()` first: `runs` is `int64` and `name` is `object`. |
| `ValueError: DataFrame constructor not properly called!` | "That isn't a shape I can make a table out of." | `pd.DataFrame("Asha", 48)` — handing it loose values instead of a dictionary or a list of dictionaries. | `pd.DataFrame({"name": ["Asha"], "runs": [48]})`. Note the **lists** — even a one-row column is a list. |
| `AttributeError: module 'pandas' has no attribute '__version__'` | "The thing I imported as pandas isn't pandas." | **There is a file called `pandas.py` in the folder**, so `import pandas` found theirs. | Rename their file. Standing rule all year, fourth appearance: never name a file after a library. |
| **No error, `print(df.info())` printed `None` at the bottom** | Nothing is wrong. `info()` prints for itself and hands back nothing. | The extra `print()`. | `df.info()` on its own, no `print`. |
| **No error, `df.info` printed the whole table and then a `>`** | Nothing is wrong. You asked for the method itself instead of calling it. | Missing brackets: `df.info` instead of `df.info()`. | `df.info()`. Same rule as numpy: **a verb takes brackets, a fact doesn't.** |
| **No error, whole numbers are printing as `12.0`** | Nothing is wrong as far as pandas is concerned. | **There is a hole in that column.** `NaN` is a decimal, so the whole column became decimals. | Run `info()` and look at the non-null count for that column. Fixing the hole is Week 23; today, noticing it is the job. |
| **No error, a number column says `object`** | Nothing is wrong as far as pandas is concerned. | One value is text — a quote mark round a number, a stray space, or a word. | Find it and make it a number. **This is the loudest alarm in pandas and it never raises an error.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds one that is specific to pandas and saves a great deal of panic:

12. **"How many lines is that error, and which one is the last one?"**

Ask it *before* looking at anything else. It turns a wall of text into one sentence, and it works every time. The follow-up is: **"which `File` line has your filename in it?"** Those two questions together handle every pandas traceback in this course.

And the sentence for this week:

> **"Run `head()` and `info()` on every table before you do anything to it. If the numbers you typed came back with decimal points, you have a hole."**

---

## ❓ Questions Students Ask This Week

**"Why isn't the index a column? It looks exactly like one."**

Because it has a different job. Columns hold **what you measured**. The index holds **which row this is**.

The tests are all short and all agree. `info()` says "total 5 columns" and the index is not among them. The index has no name of its own in the printout. And `df[0]` is a `KeyError`, because square brackets ask for a column *by name* and the index has no name to ask for.

The reason to be firm about it now is Week 22. The moment you throw some rows away, the index stops being 0, 1, 2, 3 and becomes something like 0, 3, 4, 7 — the *original* names of the rows that survived. A student who thinks the index is "the row count" finds that baffling. A student who thinks it is "the row's name" finds it obvious.

**"Is `df["runs"]` a list?"**

No, and the difference matters. It is a **Series**, and it carries three things a list does not: the **index** (so it knows which rows the values belong to), a **name** (`runs`), and a single **dtype** for all of it.

Underneath, the values really are a numpy array — so everything from Weeks 17 to 20 is still true of them, and `df["sleep"] * 60` works exactly like `arr * 2`. A Series is best thought of as *"a numpy array that remembers what its rows are called and what it is called."*

**"Why does `object` mean text? That's a terrible name."**

It is a terrible name, and it is historical. Underneath, pandas stores each column as a numpy array, and numpy has fixed-size kinds like `int64` and `float64`. Text has no fixed size — "Sam" and "Priyadarshini" are different lengths — so pandas stores a column of text as an array of **references to Python objects** sitting elsewhere in memory. Hence `object`.

Which means `object` really means *"general Python things"*, and text is simply the most common such thing. A column of Python lists, or dates before you convert them, would also say `object`.

**What you actually need from this:** `object` on a column you expected to be numbers means something is wrong. That is the whole practical content, and it will save you hours all year.

**"Why did `12` become `12.0`? That's the same number."**

The value is the same; the **kind** is not, and the change of kind is a message.

A column holds one kind of thing — Week 17's rule, and it has not changed. `NaN`, pandas's marker for "nothing here", is itself a decimal. So a column containing both `12` and `NaN` has to be a kind that can hold decimals, and there is only one: `float64`. `12` stored as a decimal prints as `12.0`.

**Why does pandas not have a whole-number kind with a "missing" slot in it?** Genuinely good question. For most of pandas's history it did not, for exactly the reason above. Newer versions have added one — an optional `Int64`, capital I — but it is not the default and you will not meet it here. So `12.0` remains the honest signal that a hole exists.

**"Is pandas replacing numpy? Did I waste four weeks?"**

Absolutely not, and this worries students so answer it properly.

**A DataFrame is built on top of numpy.** Every column is a numpy array underneath. When you compute a mean, numpy does the arithmetic. When you compare a column with a number, you get a mask — the same mask you learned last week. `axis=0` and `axis=1` still mean the same two directions and pandas uses those exact words.

What pandas adds is a **layer of labels** on top: column names, an index, and permission for each column to be a different kind. It is a jacket, not a replacement. And you needed the four weeks, because a student who meets `df.groupby(...)` without ever having written the loop it replaces has learned an incantation rather than an idea.

**"Should I always use a DataFrame then, if it can do everything?"**

Mostly yes, for tables — and there are honest exceptions.

Use a plain numpy array when your data is genuinely **all one kind and you only want arithmetic**: an image, a big grid of measurements, the `X` you feed to a model in Week 29. Arrays are faster, they use less memory, and there is far less of the library to remember.

Use a DataFrame whenever the columns **mean different things** — which is nearly always true of data about the world, because the world comes with names, categories and holes in it.

And there is a real cost to pandas that you should say out loud: it is a big library with about six ways to write everything, and that is genuinely confusing. It is why we spent four weeks on arrays first.

**"How much of a table can you understand from `head()` and `info()` alone?"** *(Nobody fully agrees, and here is why.)*

**Less than you would like, and people who work with data argue about what to look at next.** It is worth being straight about this.

**What everybody agrees on:** run both, always, first. `head()` tells you the column names are what you think and the values look like the right sort of thing. `info()` tells you how many rows there are, what kind each column is, and where the holes are. Nobody argues about this; skipping it is simply a mistake, and every experienced person has been burned by skipping it.

**Where it splits.** One camp says: **next, print the summary statistics** — the mean, the minimum, the maximum of every numeric column, which you will meet as `describe()` in Week 34. It is one line and it catches impossible values instantly, like an age of 900 or a negative price. The other camp says: **next, draw a picture**, because a table of averages hides shapes that a chart shows immediately — two clumps of students, or one enormous outlier, or a value that repeats suspiciously often. That is Weeks 25 to 27. Both camps are right and neither order is wrong.

**And there is a third position that is harder and probably the most honest:** none of it is enough, because the important questions are not in the table at all. `info()` will happily tell you that a column has ten non-null values and never tell you that three of them were guessed, that the phone was in a bag on Tuesday, or that "Mon" means two different Mondays. **The data does not record how it was made.** The only fix is a human writing it down — which is Week 24's cleaning log and Week 35's honesty paragraph, and it is the part of this subject that no library will ever do for you.

What to tell a 12-year-old, out loud: **"`head()` and `info()` tell you what's in the table. They cannot tell you where it came from. Only you can write that down."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **pandas is not installed and the lesson dies at minute three** | It was installed by a different Python, or on a different machine, or the download stalled | This is why it is first on the Prep list. If it happens anyway: **do not debug for more than three minutes.** Switch to the paper version, which delivers all five objectives, set the install as homework with the three commands written down, and fix it yourself before Week 22 — which cannot be done on paper. |
| The index is read as the first column, repeatedly | It prints exactly like one | Do not just assert it. Count the column names in `head()`, then read "total 5 columns" from `info()`. Then ask what the sixth column would be *called*. The silence is the argument. |
| `info()` gets skimmed and declared "fine" | It is eleven lines of dense text and it looks like boilerplate | Make them read it **out loud, line by line, in their own words.** All eleven. It takes three minutes and it is the objective. A skimmed `info()` is the same as no `info()`. |
| `memory usage` becomes the most interesting line | It has a number in it and it sounds technical | One sentence: "how much space it takes; ignore it." Then move on and do not return to it. |
| `12.0` is shrugged off — "same number, who cares" | It *is* the same number | Point at the non-null count in the same output: `3 non-null`, not 4. The `12.0` is the *symptom*; the missing value is the *disease*. Then have them find the Week 17 and Week 18 Bug Log entries and say what all three have in common. |
| The nineteen-line traceback causes genuine panic | It is genuinely alarming after four weeks of four-line numpy errors | Say the length out loud before you read it: *"that's nineteen lines for one wrong letter."* Then read only the last line. Then find the `File` line with their filename. **Naming the length defuses it.** |
| `print(df.info())` and the mysterious `None` | Every other thing they print needs `print()` | One sentence: "`info()` prints for itself, so it hands nothing back, and `print` prints the nothing." Then remove the `print`. |
| A student writes `pd.dataframe` and cannot see why it failed | Capital letters in the middle of a word are unusual | Read the quoted name out loud: `'dataframe'` — **the computer told you exactly which name it could not find.** Getting a student to compare it with the spelling they meant (and to read a `Did you mean` suggestion if their version prints one) is worth more than fixing it for them. |
| Somebody teaches `df[df["runs"] > 50]` because they have masks | It is one line and it works and it is thrilling | Let them admire it, then hold the line: *"yes — and next week we do it properly, including the bit where the index goes strange afterwards."* Filtering with an index that is no longer 0, 1, 2 is exactly what Week 22 is for, and doing it today means doing it badly. |
| The activity's four columns are all words | Because words are easier to make up | Insist before they start: **at least one decimal column and at least one whole-number column.** Without those, `info()` is boring and the `None` experiment does not work. |
| The paper grid gets skipped "to save time" | Typing feels faster | It is not about the time. The paper grid is what lets them check that `RangeIndex: 10 entries` matches reality. Without it, `info()` is a report about nothing. |
| The `dtypes:` tally line gets more attention than the per-column lines | It is one short line and it looks like a summary | It **is** a summary, and it has no column names in it. Say the rule: **the line with a name on it is the more useful line.** `steps  9 non-null  float64` tells you which column and how many are missing; `float64(3), object(1)` tells you neither. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** `df["col"]` and the Series entirely. The two commands — `head()` and `info()` — are the objective, and next week is *entirely* about picking things out. Nothing is lost.

**Cut:** the ten-row table to five rows and three columns: one of words, one of decimals, one of whole numbers. That is the minimum that makes `info()` interesting, and it still produces all three dtypes.

**Cut:** the list-of-dicts route. Do everything with `pd.DataFrame({...})`, which is the form they will use all year.

**Give them the data block already typed.** All of today's learning is in **reading** two printouts. None of it is in typing values.

**Reteach — with a printed table and four coloured pens, and nothing else.** This is the whole lesson:

1. Hand them the printed pandas output.
2. *"Circle the column names."* Five of them.
3. *"Circle the numbers down the left."* **That's the index.** Label it "row names".
4. *"How many columns are there?"* Five. *"Is the index one of them?"* No. *"What would it be called?"* It hasn't got a name.
5. *"Circle one value. Now circle one whole column."*
6. Then hand them the printed `info()` and go line by line. For each line, they say what it tells you. Eleven lines, three minutes.

A student who leaves the room able to point at a printed table and say *"those are the column names, those down the side are the row names, and there are five columns not six"* has succeeded, whether or not any Python ran.

**The copy-this-exactly scaffold.** One file, eight lines. This runs:

```python
import pandas as pd

snacks = pd.DataFrame({
    "snack": ["samosa", "vada", "idli"],
    "price": [15, 20, 10],
})

print(snacks)
snacks.info()
```

```text
    snack  price
0  samosa     15
1    vada     20
2    idli     10
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   snack   3 non-null      object
 1   price   3 non-null      int64 
dtypes: int64(1), object(1)
memory usage: 176.0+ bytes
```

Then three questions and nothing else: **"how many rows? how many columns? and which column is words?"** Three, two, and `snack`. That is objectives 1, 2 and 3.

**One thing you must not cut:** reading `info()` out loud. If the whole lesson collapses to one sentence, make it *"run `info()` and read every line."*

### If the student is flying

None of these need syntax from a later week.

1. **Array maths on a Series** (Variation-harder 1): `my_week["sleep"] * 60`, and the honest question about whether the name should still say `sleep`.
2. **Make a column `object` on purpose** (Variation-harder 2): quote marks round one number. Then which is worse — the hole or the quote mark — and which is harder to spot.
3. **Predict a whole `info()` report before building the table** (Variation-harder 4), with one `None` and one quoted number hidden in it. **This is the best exercise in the week** and it is genuinely hard.
4. **Build the same table both ways** (Variation-harder 5) — dict of columns and list of dicts — and argue about which is less error-prone.
5. **Could two rows share an index?** (Variation-harder 3.) They should not (pandas allows it, but a repeated name picks out two rows). So what is the index for? Giving each row its own name. Week 22 depends on this.
6. **The honest question** (Variation-harder 6): *"where did the 7.5 come from?"* The DataFrame has names and kinds and **no history.**

### If the student won't engage today

**Close the laptop. One printed table and four coloured pens.**

Better still: **let them pick the table.** Five songs with a length and a play count. Five players with goals and matches. Five snacks with a price and a rating. Anything with rows, columns and a couple of numbers, invented by them, written out by hand on the blank grid.

Then three instructions and nothing else:

> **"Write a name at the top of every column."**
>
> **"Number the rows down the left, starting at zero."**
>
> **"Now tell me: how many columns have you got?"**

Whatever they say, follow with: *"is the row-number strip one of them?"*

That is objectives 1, 2 and 4, delivered in ten minutes with a pen, and it is the half of the lesson that everything from here to Week 36 sits on. The typing survives to next week, which is entirely about picking things out of a table and starts fresh anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the index (spoken, 45 seconds)**

> "Here's a printed table with the columns `day`, `sleep`, `steps` and the numbers 0 to 9 down the left. **How many columns has it got, and what are the numbers down the left?**"

*Good answer:* "Three columns. The numbers down the left are the index — the row names — and they're not a column."

**What to catch:** "four columns". Do not correct with a rule; ask what the fourth one is *called*.

**Check 2 — reading `info()` (spoken, 60 seconds)**

> "`info()` says `RangeIndex: 10 entries, 0 to 9` and then, for one column, `steps  9 non-null  float64`. **Tell me three things that tells you.**"

*Good answer:* "There are ten rows. The `steps` column has one empty cell, because nine out of ten are filled. And it holds decimals."

**Full marks needs the gap being noticed** — that 9 is not 10. A student who reads all three fields but does not comment on the missing one is a level-3 answer; push once: *"ten rows and nine values. Where's the tenth?"*

**Check 3 — the silent surprise (spoken, 90 seconds)**

> "Somebody typed a column of whole numbers — 6200, 8100, 4300 and so on. It came back printing as `6200.0`, `8100.0`. **Nothing crashed. What happened, and where would you look to confirm it?**"

*Good answer:* "There's a missing value somewhere in that column. `NaN` is a decimal, and a column can only hold one kind, so the whole column became decimals. I'd look at the non-null count in `info()` — it'll be less than the number of entries."

**What to catch:** "pandas just prints numbers like that." It does not — the earlier `ages` table printed `12`, not `12.0`. Show them both outputs side by side.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot build a DataFrame without copying. Reads the index as a column. Cannot say what `head()` shows. |
| **2 — Emerging** | Builds a DataFrame from a dict of lists with the pattern given. Runs `head()` and `info()` when told to. Reads individual numbers off `info()` but does not check them against anything. |
| **3 — Secure** | Builds a DataFrame unaided from a dict of columns **and** from a list of dicts. Runs both commands without being asked. **Reads every line of `info()` out loud in their own words.** Says the index is the row's name, not a column. Explains `12.0` as a hole in the column. **This is the target.** |
| **4 — Strong** | Checks the entry count against the number of rows they actually typed, and the column count against the names they typed. Spots `object` on a number column as an alarm. Connects `NaN` → `float64` back to Week 17's one-kind rule unprompted. Reads a nineteen-line traceback by going to the last line and then to their own filename. |
| **5 — Exceptional** | Says without prompting that `12.0` is the symptom and the non-null count is the disease. Argues that the index matters because it is meant to be a different name for every row, and predicts that filtering will make it non-consecutive. Says that `head()` and `info()` cannot tell you where the data came from, and that only a person writing it down can. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, and most of the marking is on one part.
>
> **First, finish the Build It section of your workbook — 'Your Own Week, In Ten Rows'.** You did the paper grid, `myweek.py`, and your first look at `info()` in class. Tonight is the rest of it. Tick off the step checklist, and make sure the paper grid is in pencil and still has your row count written on it. **You chose the columns:** one must be words, at least one decimals — hours of sleep is the easy one — and **at least one whole numbers**, steps or minutes of homework, because you need it for the hole experiment.
>
> **Second, and this is the part I'm actually marking: 'info(), line by line, in my own words.' Write what every single line of your `info()` is telling you.** Every line in the table. In your own words, not mine. If it says `RangeIndex: 10 entries, 0 to 9`, I want a sentence saying *ten rows, named zero to nine, and that matches the ten rows on my paper.* If it says `object`, I want a sentence saying what `object` means and whether it's right for that column. Then do 'The three checks' under it.
>
> **And one specific thing I will be looking for: if any column is a decimal when you typed whole numbers, tell me why.** If none of them is, say so — that's a real answer.
>
> **Third, the hole experiment, still in Build It.** Take one value out of your whole-number column and put `None` there. **Before you run it, write down three things you think will change.** Then run it, fill in the before-and-after table, and write the one sentence: why did *everybody else's* number change when only one was missing? Finish 'The same rule, three times' and the two Bug Log entries.
>
> **Fourth, two more sections.** 'Predict the Output' — four small snippets, prediction in pen *before* you run anything; two of them run cleanly and are not what you typed. And 'Fix the Broken Program' — three bugs, one of each kind."

**What is assigned, and what is not.** The workbook is much bigger than one evening. The split, in the order of the workbook:

| Section | When | Needed for the mark? |
|---|---|---|
| ✅ Warm-Up (W1–W5) | **In class**, first five minutes | No. Last week's recall; mark it from the key below |
| 🔎 Predict the Output (P1–P4) | **At home** | Yes |
| ✍️ Practice Set A — Read It | **A2 in class** (the lesson's part 5, in pen); **the rest optional** | A2 only |
| ✍️ Practice Set B — Write It | Optional (B5 is the same program as Build It — see below) | No |
| 🐞 Fix the Broken Program | **At home** | Yes |
| 🧩 Puzzle of the Week | Optional — a good one for a student who finishes early | No |
| 🤔 Think Deeper (T1, T2) | Optional, or a conversation at the next lesson | No |
| 🛠️ Build It | **Steps 1–9 in class** (the activity); **steps 10–12 and all the tables at home** | **Yes — the marked part** |
| 🎨 Draw It | Optional | No |
| 📊 Self-Check | **At home**, last, honestly | No marks; read it |

**Expected time:** 20 min for the `info()` line-by-line table and the three checks · 10 min for the hole experiment and its sentence · 10 min on the 'same rule, three times' table and the Bug Log · 10 min on Predict the Output · 10 min on Fix the Broken Program. **About an hour.** Anything marked optional is on top of that.

> **🧑‍🏫 What to look for when you mark it:** three things, and the second is the real one. **One — does the entry count match the number of rows on their paper grid?** (Build It, 'The three checks', check 1.) If they did not fill in the paper, they cannot answer this and the check did not happen. **Two — is every line of `info()` explained in their own words?** Eleven table rows, eleven sentences — the Build It table lists the two `#`/`---` heading lines as rows of their own. A page that says "it tells you about the DataFrame" for line one and skips to the dtypes has not done the work, and this is the objective. **Three — does the hole sentence explain why *everybody else* changed?** The good sentence is something like *"`NaN` is a decimal and a column can only hold one kind of thing, so the whole column had to become decimals even though only one value was missing."* A sentence about the one missing value has spotted the obvious half and missed the point.

---

## 🔑 Answer Key

Every workbook section and item, in workbook order, so you can mark from this page alone. Values are taken from the workbook's own ✅ Answers section and were re-checked by running the code (pandas 1.5.3).

### ✅ Warm-Up

*Five questions about last week.*

| Item | Answer |
|---|---|
| **W1** | **Shape `(10, 5)`** — the same shape as the data. It holds **`True` and `False`, one per cell**, fifty of them, dtype `bool`. It is **not** a shorter list of the high scores. |
| **W2** | The nineteen were `False`, so they are **simply not in the answer.** They did **not** become zeros — a zero score and a missing score are different things. *(The answer is one long row, not a grid, because students have different numbers of high scores and there is no rectangle shaped like that.)* |
| **W3** | **Python treats `True` as 1 and `False` as 0.** Adding a mask up adds one for every yes and nothing for every no, which is counting. |
| **W4** | **The formula guarantees both.** Subtracting the smallest makes the smallest zero; dividing by the gap makes the largest one. **A check that cannot fail is not a check.** A range check — `scores[scores > 100]` giving `[950]` — would have caught it, because it brings knowledge from outside the formula. |
| **W5** | **A verb takes brackets; a fact does not.** `.min()` is something the array **does**; `.shape` is something the array **is**. |

### 🔎 Predict the Output

*Four snippets, prediction in pen first. All four run; the workbook warns that two of them are not what you typed (P3 and P4 are the ones that bite). The /16 self-score at the bottom of the section is the student's own count and needs no key.*

**P1 — which way round is a column?** Real output:

```text
  snack  price
0  idli     10
1  dosa     30
2  vada     20
3
0    10
1    30
2    20
Name: price, dtype: int64
```

- **Prediction:** **3 rows, 2 columns.**
- **Which number became the rows?** **Three** — the length of each list. Two keys give two columns; three items give three rows. *(Getting this backwards is the most common beginner mistake with `pd.DataFrame({...})`.)*
- **The extra line** is the footer `Name: price, dtype: int64`. It carries **the column's own name** and **the one dtype shared by all its values.** A numpy array knew its dtype; it never knew its name.

**P2 — two ways to ask.** Real output: `menu["snack"]` prints `idli`, `dosa`, `vada` with the footer `Name: snack, dtype: object`; then `menu[0]` ends in a long traceback whose last line is `KeyError: 0`.

- **Will it work?** No — `KeyError: 0`.
- **In their own words:** *"There is no column called 0."*
- **Fill the blank:** square brackets on a DataFrame ask for **columns**, not **rows**. The index is not a column, so it has no name to ask for. Rows arrive next week, with two new words.
- *(Also worth noticing: `snack` printed `dtype: object` — pandas's word for text.)*

**P3 — one hole.** Real output:

```text
   pet  legs
0  cat     4
1  dog     4
2  rat     4
   pet  legs
0  cat   4.0
1  dog   NaN
2  rat   4.0
```

- **Will `b` crash?** **No.** **All three** `legs` values look different (`4` became `4.0` twice, plus the `NaN`).
- **How many changed appearance / how many did you change?** **3** and **1**.
- **The two `info()` lines:**

```text
from a:   1   legs    3 non-null      int64
from b:   1   legs    2 non-null      float64
```

- **Symptom and disease:** **the `float64` is the symptom; the `2 non-null` is the disease.** The decimal point is what you *see*; the missing value is what is wrong. A person who shrugs at `4.0` will average a column with holes in it and never know.
- **Why the whole column changed:** `NaN` is a decimal and a column holds one kind of thing, so the only kind that can hold both `4` and `NaN` is decimals.

**P4 — one quote mark.** Real output:

```text
   pet legs
0  cat    4
1  dog    4
2  rat    4
```

then the `legs` line of `info()`:

```text
 1   legs    3 non-null      object
```

then `print(c["legs"] * 2)`:

```text
0     8
1    44
2     8
Name: legs, dtype: object
```

- **`print(c)`:** three ordinary-looking 4s. The only clue is that the `legs` header sits one space closer to its column than when all three were numbers — far too subtle to rely on.
- **Is the column fine?** **No.** The count is 3 so nothing is missing; one value is *the wrong kind*.
- **The three values printed:** **`8`, `44`, `8`.**
- **Which one is not like the others, and why?** **`44`.** The two real integers were multiplied (`4 * 2 = 8`); the text `"4"` was **repeated** (`"4" * 2 = "44"`) — `*` on text means *repeat*, Week 11's rule, still true. No error, a confident nonsense answer. This is what `object` on a number column costs you.
- **Teacher note:** marks for noticing that *nothing* in `print(c)` warns them; this is the loudest lesson in the section.

### ✍️ Practice Set A — Read It

**A1 — match and label.** DataFrame → **(iii)** · Series → **(v)** · index → **(iv)** · column name → **(i)** · NaN → **(ii)**.

Labelling: **(a)** the header row `name team runs balls out`; **(b)** the `0 1 2` strip down the left; **(c)** any one whole row, such as `1 Ravi Falcons 12 20 True`; **(d)** any one whole column, which is a Series.

- **A1(e)** **Five** — `name`, `team`, `runs`, `balls`, `out`.
- **A1(f)** **No.** Any three of: (1) `info()` says "total 5 columns" and the index is not counted; (2) it has no column name — the strip has nothing written above it; (3) `df[0]` raises `KeyError: 0`, because there is no column named `0`.
- **A1(g)** A **Series**. It carries the **values**, the **index** they belong to, and its own **name** (plus one dtype for all of it). The footer `Name: runs, dtype: int64` is where the last two show up.
- **A1(h)** **Names on the columns, an index on the rows, and permission for each column to be a different kind of thing.** *(Any two of the three earns the mark.)*
- **A1(i)** **Arithmetic on everything at once**, in one line, plus a shape it knows about. *(Week 17's answer, still true.)*
- **A1(j)** Two honest reasons: (1) **it is slower and much more complicated** — a big library with several ways to write everything; (2) **you would not have known what named columns were worth.** Four weeks of carrying a separate `names` array around is what makes this week feel like a relief instead of a formality.

**A2 — predict `info()`** (this is the lesson's part 5, done in class, in pen). The table is `snacks`: samosa, vada, idli, dosa, poha, upma, with `stars` holding one `None`.

| # | Question | Answer |
|---|---|---|
| a | entries | **6**, named 0 to 5 |
| b | columns | **4** |
| c | `snack` | `6 non-null`, **`object`** (it is words) |
| d | `price` | `6 non-null`, **`int64`** (whole numbers, no holes) |
| e | `spicy` | `6 non-null`, **`bool`** |
| f | `stars` | **`5 non-null`, `float64`** ← the miss |
| g | the `dtypes:` tally | `bool(1), float64(1), int64(1), object(1)` |

Real output:

```text
    snack  price  spicy  stars
0  samosa     15   True    4.5
1    vada     20   True    4.0
2    idli     10  False    3.5
3    dosa     40  False    5.0
4    poha     25  False    NaN
5    upma     20   True    3.0
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 6 entries, 0 to 5
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   snack   6 non-null      object 
 1   price   6 non-null      int64  
 2   spicy   6 non-null      bool   
 3   stars   5 non-null      float64
dtypes: bool(1), float64(1), int64(1), object(1)
memory usage: 278.0+ bytes
```

- **A2(h) Which did you get wrong?** Almost always **(f)**. The expected wrong answer is `6 non-null`, on the grounds that there are six snacks. There *are* six rows — `RangeIndex: 6 entries` is right — but one of `stars`'s cells holds nothing, so only **five** are non-null. **The row did not disappear; the cell is empty.** Model sentence: *"I said `stars` would be 6 non-null because there are six snacks. It's 5, because one cell has `None` in it — the row is still there, but that one cell holds nothing."*
- **A2(i) What did the `None` change?** **Only the non-null count**, 6 to 5. `stars` already had `4.5`, so it was going to be `float64` with or without the hole.
- **A2(j) The only clue?** **The count, and nothing else.** No `12.0`-style giveaway, because the column was always decimals. Which is exactly why you read `info()` rather than glancing at the printed table.
- **A2(k)** **`price`.** It is `int64` now; one `None` would turn it into `float64` and print `15` as `15.0`.
- **A2(l)** The tally adds to **four**, and there are **four** columns. A free check, and it passes.

**A3 — spot the bug.**

| # | What happens | The fix |
|---|---|---|
| a | `AttributeError: module 'pandas' has no attribute 'dataframe'` | `pd.DataFrame(...)` — capital D **and** capital F. Read the name in quotes and compare it with the spelling you meant |
| b | A nineteen-line traceback ending `KeyError: 'Runs'` | `squad_df["runs"]`. Column names are case-sensitive text |
| c | A nineteen-line traceback ending `KeyError: 0`. Square brackets mean **columns** | Ask for a column by name. Rows come next week |
| d | **No error.** It prints the whole report, then the word `None` underneath | `squad_df.info()` on its own. `info()` prints for itself and hands nothing back |
| e | `TypeError: 'method' object is not subscriptable` | `squad_df.head(3)` — **round** brackets. `head` is a verb |
| f | `ValueError: All arrays must be of the same length` | Count the items in every list. Three days, two step counts — not a rectangle |

- **A3(g)** **(d).** It prints the report correctly and then a lonely `None`, which looks broken and isn't.
- **A3(h)** **(b) and (c)** are both nineteen lines. The recipe never changes: *how many lines is it, and what does the last one say? Then: which `File` line has my own filename in it?* *(Say the length out loud first — "nineteen lines for one wrong letter" removes the panic in about two seconds. On pandas 2.x the count may differ; see the version note in Prep.)*

**A4 — match code to output.** i → **P** · ii → **Q** · iii → **T** · iv → **S** · v → **R**.

- **A4(f)** **`T` and `R`** end with a `Name:` line; `S` does not. **A `Name:` footer means you are looking at a Series — one column.** A whole DataFrame has several columns, each with its own name, so it prints no footer. *(And `v` shows `head()` works on a Series too, footer and all.)*

**A5 — say what every line of `info()` tells you** (the five lines in Figure W21.1).

| Line | Model sentence |
|---|---|
| 1 `<class 'pandas.core.frame.DataFrame'>` | This really is a DataFrame — a whole table, not a single column. If it said `Series`, I had handed pandas one column by mistake. |
| 2 `RangeIndex: 10 entries, 0 to 9` | Ten rows, named 0 to 9. I check that ten against the number of rows I actually typed. |
| 3 `Data columns (total 4 columns):` | Four columns follow. I typed four names, so that matches. The index is **not** one of the four. |
| 4 ` 3   steps   9 non-null   float64` | Column 3 is `steps`. **Nine** of its cells hold something, and it holds decimals. |
| 5 `dtypes: float64(3), object(1)` | A tally: three decimal columns and one text column. Adds to four, matching the column count. |

- **A5(a)** **The `10` in line 2 and the `9` in line 4.** One cell in `steps` is empty — the row did not disappear, the cell is empty. The `float64` is the knock-on effect: `NaN` is a decimal.
- **A5(b)** **Line 4** — the only one with a column name on it, so it says **which** column and **how many** are missing. The tally says neither (`float64(3)` does not say which three, or why).
- **A5(c)** It would mean **`steps` has text in it** (a quote mark, a stray space, a word). And it would be **worse**: with `9 non-null float64` there are two signals (short count, decimal points); with `10 non-null object` there is one — the dtype. The count says nothing is missing, the values look like numbers, and no error is ever raised.

**A6 — finish the sentence.**

- **a)** …with **the labels put back on**, and each column is allowed to **be a different kind of thing**.
- **b)** The index is the **row's name** (its label), not a **column**.
- **c)** `head()` tells you **what the table looks like** (the first five rows). `info()` tells you **whether you can trust it**.
- **d)** …because **`info()` prints for itself and hands nothing back**, so `print` would show the report and then the word `None`.
- **e)** …**you have a hole somewhere**, and the command that tells you where is **`info()`** (its non-null count).
- **f)** …means **one of its values is text**, and it raises **no error at all**.

### ✍️ Practice Set B — Write It

**B1.**

```python
import pandas as pd

library = pd.DataFrame({
    "book":  ["Wonder", "Holes", "Coraline"],
    "pages": [320, 233, 176],
})

print(library)
```

```text
       book  pages
0    Wonder    320
1     Holes    233
2  Coraline    176
```

Marks: a **dict of columns**, each key a column name, each list running *down* the page; capital D, capital F. *"Key, colon, and then a whole column running down the page."* Two keys, two columns; three items, three rows.

**B2.**

```python
print(library.head(2))
print()
library.info()
```

```text
     book  pages
0  Wonder    320
1   Holes    233

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 2 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   book    3 non-null      object
 1   pages   3 non-null      int64 
dtypes: int64(1), object(1)
memory usage: 176.0+ bytes
```

`head(2)` has `print()` round it because it *hands you back* a table. `info()` does not, because it prints for itself and returns nothing — `print(library.info())` would add a stray `None`.

**B3.**

```python
print(library["pages"])
print("the whole table is a:", type(library))
print("one column is a    :", type(library["pages"]))
```

```text
0    320
1    233
2    176
Name: pages, dtype: int64
the whole table is a: <class 'pandas.core.frame.DataFrame'>
one column is a    : <class 'pandas.core.series.Series'>
```

**B4.**

```python
by_columns = pd.DataFrame({
    "book":  ["Wonder", "Holes", "Coraline"],
    "pages": [320, 233, 176],
})

by_rows = pd.DataFrame([
    {"book": "Wonder",   "pages": 320},
    {"book": "Holes",    "pages": 233},
    {"book": "Coraline", "pages": 176},
])

print(by_columns)
print()
print(by_rows)
print()
print("are they the same table?", by_columns.equals(by_rows))
```

The output is the B4 expected output in the workbook: the same three-row table twice, then `are they the same table? True`.

- **B4(a)** **The dict of columns** — each column name once instead of once per row (with ten rows and four columns, 4 names against 40).
- **B4(b)** **The list of dicts.** Every value sits next to its own key. In the dict-of-columns version, one missed or extra value shifts everything after it under the wrong name, and pandas only notices if the lists end up different lengths — two cancelling mistakes go unnoticed. *(Students often say "the dict of columns, because it is shorter"; that answers (a), not (b).)*

**B5 — `myweek.py`.** The model program and its output are the same as the one in **Build It** below (the ten-row `my_week` table: `info()` shows `10 entries`, `total 4 columns`, `float64(2), int64(1), object(1)`, `memory usage: 448.0+ bytes`). Their columns will be their own. **The second version, with one `None` in `steps`**, prints `steps` as `6200.0 … NaN … 5100.0` and `info()` ends:

```text
 3   steps   9 non-null      float64
dtypes: float64(3), object(1)
memory usage: 448.0+ bytes
```

- **B5(a)** Three good predictions: the missing value prints as **`NaN`**; the dtype goes **`int64` to `float64`**; the non-null count goes **10 to 9**. *(A fourth almost nobody predicts: every other step count grows a decimal point.)*
- **B5(b)** `before: dtypes: float64(2), int64(1), object(1)` / `after : dtypes: float64(3), object(1)`. **The `int64` vanishes completely** — after the conversion there is no whole-number column left in the table.
- **B5(c)** **No.** Both tallies still add to four. The check passed and the table is still not what you typed. *A check that cannot fail is not much of a check.* Read the per-column lines instead; one of them says `9 non-null`.

### 🐞 Fix the Broken Program

Three bugs in `snacks21.py`, met in this order.

| Bug | Line | Kind | What the student should say | The fix |
|---|---|---|---|---|
| **1** | 7 | **Syntax** | Run 1 prints nothing at all (a `SyntaxError` happens before the program runs). The message ends in a question, and **it is right**: the comma is missing at the end of the `price` line, after the closing `]`. | `"price": [15, 20, 10, "40", 25, 20],` |
| **2** | 16 | **Runtime** | `KeyError: 'Price'`. **Asked for** `'Price'`; **actually called** `'price'`. The message quotes exactly what you asked for, so hold the two strings side by side. The `File` line to act on is `File "snacks21.py", line 16`; the rest of the nineteen lines are inside pandas. | `snacks["price"]` |
| **3** | 7 | **Logic**, no error message | Column **`price`** says **`object`**; it should say **`int64`**. The count is 6 of 6, so nothing is missing; one value is the wrong *kind*. The culprit is the **quote mark** round `"40"` (two characters, and either would do it). | `"price": [15, 20, 10, 40, 25, 20],` |

- **The fixed `info()` lines:**

```text
 1   price   6 non-null      int64
dtypes: bool(1), float64(1), int64(1), object(1)
```

- **Fixed program's last line:** `the prices: 0    15 … 5    20` with the footer `Name: price, dtype: int64`.
- **Is the bug visible in `head(3)`?** **Not usefully.** The only trace is one space less before `price` in the header (`snack price  spicy  stars` against `snack  price  spicy  stars`), because pandas pads a column of numbers wider than one of text. `dosa`, the row holding the quote mark, is row 3 and is not in `head(3)` at all. One character of whitespace is not a check.
- **Bug 3 versus the `stars` hole:**

| Fault | Announces itself? | Which field of `info()` catches it |
|---|---|---|
| `stars` has a `None` | **Yes** — prints as `NaN` | the **Non-Null Count** — `5`, not `6` |
| `price` has a `"40"` | **No** — count 6, values look like numbers, no error | the **Dtype** — `object` where you expected `int64` |

  The sentence to keep: **a hole shows up in the count; text-where-you-wanted-numbers shows up in the dtype. Read both fields, on every column, every time.**

### 🧩 Puzzle of the Week

**Part 1 — the whole report.** Twelve blanks. Real output:

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   city    5 non-null      object 
 1   temp    5 non-null      int64  
 2   rain    4 non-null      float64
 3   coast   5 non-null      bool   
 4   pop     5 non-null      object 
dtypes: bool(1), float64(1), int64(1), object(2)
memory usage: 293.0+ bytes
```

- **Part 1(a)** The two most-missed blanks are **`rain`'s count** (people write 5) and **`pop`'s dtype** (people write `int64`). `coast` being `bool` is the third.
- **Part 1(b)**

| Column | The fault | Which field shows it | Visible in `print(mystery)`? |
|---|---|---|---|
| `rain` | one value is missing (`None`) | the **Non-Null Count** — `4`, not `5` | **Yes** — `NaN` on Shimla's row |
| `pop` | one value is text (`"16700000"`) | the **Dtype** — `object`, not `int64` | **No** — all five print as ordinary numbers |

  `rain` was going to be `float64` anyway, so only the count tells you; for `pop` the count is a perfect 5 and only the dtype tells you. **Two faults, two fields, and neither field catches both.**
- **Part 1(c)** **Into `float64`:** put a `None` in `temp`, or type one temperature with a decimal point, like `31.5` — only the count distinguishes them. **Into `object`:** put quote marks round one temperature (`"31"`), or a word or stray space in there.

**Part 2 — the three sick tables.**

| Report | What is wrong | How to find the culprit |
|---|---|---|
| **A** `10 entries`, `steps 9 non-null float64` | **One `steps` value is missing.** `NaN` is a decimal, so the whole column became `float64` | Print the table and look for the `NaN` |
| **B** `10 entries`, `steps 10 non-null object` | **One `steps` value is text** (a quote mark, stray space or word). Nothing is missing | Print the column and look for the odd one out, or try arithmetic: `print(df["steps"] * 2)` and look for a value that got *repeated* rather than *doubled* |
| **C** `9 entries`, `steps 9 non-null int64` | **A whole row is missing.** `steps` itself is perfect | Count the items in each of the four lists: nine all round means a dropped row (a missing comma gluing two values, or a line deleted while editing) |

- **Part 2(a)** **Easiest to hardest: A, C, B.** A has two signals (`NaN` in capitals, and every value visibly changed). C is invisible *in the report*, but is obvious the moment you compare `9 entries` with the ten rows on paper. B is hardest: perfect count, values look like numbers, no error.
- **Part 2(b)** **Report C.** `9 entries` and `9 non-null` are perfectly consistent — the table is internally flawless. You have to know you meant ten, and that fact lives outside the data.
- **Part 2(c)** **The paper grid, filled in first, in pencil.** It is the only independent record of how many rows there were supposed to be.

### 🤔 Think Deeper

Open-ended; there is no single right answer. Mark for the ideas below.

- **T1** (were the four weeks without labels worth it?): a good paragraph says that carrying a separate `names` array and hoping the lengths matched is what made named columns feel like a relief rather than a formality (the same point as A1(j)), that you now know what the one `pd.DataFrame` line is doing, and that an array is still the right tool when everything is one kind and all you want is arithmetic or a block of numbers for a model. A paragraph that says "no, we should have started with pandas" is allowed if it is argued; probe it with "what would you not have known?".
- **T2** (what a DataFrame cannot record): a good paragraph names things like *guessed* values, the phone in a bag on Tuesday, two "Mon" rows being two different Mondays; says it is **the person's job** to record them, because `info()` can only see what is in the table; and suggests somewhere outside it — a note beside the paper grid, a comment in the file, or an extra column. This connects to the Bug Log and to Puzzle Part 2(c): the paper is the record the computer cannot keep for you.

### 🛠️ Build It — Your Own Week, In Ten Rows

Their columns will be their own. **Check the entry count against the rows on their paper grid, not against this page.** Mark: ten rows on paper and `10 entries` in `info()`; four column names typed and `total 4 columns`; at least one `object` column, at least one `float64`, at least one `int64`.

Model program (`myweek.py`), actually run:

```python
"""myweek.py - ten days of my own week, as a DataFrame."""

import pandas as pd

print("pandas version:", pd.__version__)

my_week = pd.DataFrame({
    "day":    ["Mon", "Tue", "Wed", "Thu", "Fri",
               "Sat", "Sun", "Mon", "Tue", "Wed"],
    "sleep":  [7.5, 8.0, 6.5, 7.0, 6.0, 9.5, 9.0, 7.5, 8.0, 7.0],
    "screen": [1.5, 2.0, 3.5, 1.0, 4.0, 5.5, 4.5, 2.0, 1.5, 3.0],
    "steps":  [6200, 8100, 4300, 7700, 3900, 11200, 9800, 6600, 7400, 5100],
})

print()
print("--- the whole thing ---")
print(my_week)

print()
print("--- head(3) ---")
print(my_week.head(3))

print()
print("--- info(), read this out loud ---")
my_week.info()

print()
print("--- one column is a Series ---")
print(my_week["sleep"])
```

```text
pandas version: 1.5.3

--- the whole thing ---
   day  sleep  screen  steps
0  Mon    7.5     1.5   6200
1  Tue    8.0     2.0   8100
2  Wed    6.5     3.5   4300
3  Thu    7.0     1.0   7700
4  Fri    6.0     4.0   3900
5  Sat    9.5     5.5  11200
6  Sun    9.0     4.5   9800
7  Mon    7.5     2.0   6600
8  Tue    8.0     1.5   7400
9  Wed    7.0     3.0   5100

--- head(3) ---
   day  sleep  screen  steps
0  Mon    7.5     1.5   6200
1  Tue    8.0     2.0   8100
2  Wed    6.5     3.5   4300

--- info(), read this out loud ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10 entries, 0 to 9
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype  
---  ------  --------------  -----  
 0   day     10 non-null     object 
 1   sleep   10 non-null     float64
 2   screen  10 non-null     float64
 3   steps   10 non-null     int64  
dtypes: float64(2), int64(1), object(1)
memory usage: 448.0+ bytes

--- one column is a Series ---
0    7.5
1    8.0
2    6.5
3    7.0
4    6.0
5    9.5
6    9.0
7    7.5
8    8.0
9    7.0
Name: sleep, dtype: float64
```

**The three checks, on the model table.**

1. **Entry count against the paper:** `RangeIndex: 10 entries, 0 to 9` and ten rows on paper. They agree. If not, a row was lost or doubled while typing, and only the paper could have told you.
2. **Column count against the names typed:** `total 4 columns`, four names typed. They agree. The index is not one of the four.
3. **Is any column a decimal when you typed whole numbers?** **No** — `steps` is `int64`. The number that proves it is the count: `steps 10 non-null int64`. *(If it had said `float64`, the count is what tells you whether that was typed `7.5` or a missing value.)* Two acceptable forms, both of which must be reasoned: *"No. `steps` is `int64` and I typed whole numbers, and its count is 10 out of 10."* or *"Yes — `steps` came out `float64`. A value is missing: its count is 9, not 10. `NaN` is a decimal and a column holds one kind of thing, so the whole column became decimals."* **Mark the reasoning.** "Because pandas does that" is not an answer.

**`info()` line by line — model answers.** This is the marked part.

| Line | What it tells me |
|---|---|
| `<class 'pandas.core.frame.DataFrame'>` | This is a DataFrame — a whole table, not a single column. If it said `Series` I had handed pandas one column by mistake. |
| `RangeIndex: 10 entries, 0 to 9` | Ten rows, named 0 to 9. **That matches the ten rows on my paper grid**, so nothing was lost or doubled while typing. |
| `Data columns (total 4 columns):` | Four columns follow. I typed four names, so that matches too. The index is not one of the four. |
| `#  Column  Non-Null Count  Dtype` | The headings of the little table under it: the column's number, its name, how many cells are filled, and what kind of thing it holds. |
| `---  ------  --------------  -----` | Just a divider. Nothing to read. |
| ` 0   day     10 non-null     object` | Column 0 is `day`. All ten cells filled. `object` means text — correct, because days are words. |
| ` 1   sleep   10 non-null     float64` | Column 1 is `sleep`. All ten filled. `float64` means decimals, which is right because I typed values like 7.5. |
| ` 2   screen  10 non-null     float64` | Same as `sleep`: ten values, decimals because I typed halves. |
| ` 3   steps   10 non-null     int64` | Column 3 is `steps`. Ten filled. `int64` means whole numbers, which is right — you cannot take half a step. |
| `dtypes: float64(2), int64(1), object(1)` | The tally: two decimal columns, one whole-number, one text. **Adds to four**, matching the column count. |
| `memory usage: 448.0+ bytes` | How much space the table takes. Not interesting. The `+` means it is an estimate, because text is stored elsewhere. |

**What loses the marks:** *"it tells you about the DataFrame"* for line one, then skipping to the dtypes. One sentence per line. And the sentence for line two has to mention the paper, or the check did not happen.

**Two side questions from the model table.** `Mon` appears twice, in rows 0 and 7: **not a problem** — two rows may share a value; what they should not share is the **index**, whose job is to name each row. (pandas allows a repeated index, but asking for that name then returns two rows.) And `sleep` and `screen` are `float64` **because decimals were typed, not because anything is missing** — the counts are 10 of 10; `info()`'s count is what tells you which.

**The hole experiment, both columns filled** (model: one `steps` value set to `None`).

| | Before the `None` | After the `None` |
|---|---|---|
| `RangeIndex: ___ entries` | **10** | **10 — unchanged** |
| `total ___ columns` | **4** | **4 — unchanged** |
| `steps` non-null count | **10** | **9** |
| `steps` dtype | **`int64`** | **`float64`** |
| how the values print | `6200` | **`6200.0`** |
| the `dtypes:` tally | `float64(2), int64(1), object(1)` | **`float64(3), object(1)`** |

- **Three things that changed:** the missing value prints as **`NaN`**; the dtype went **`int64` to `float64`** and every step count grew a decimal point; the non-null count went **10 to 9**. *(The vanished `int64` in the tally is a fourth.)*
- **One thing that did NOT change:** **`RangeIndex: 10 entries`** — the row did not disappear; only one cell is empty. *(Also acceptable: `day`, `sleep`, `screen`, or the column count.)*
- **The sentence being marked.** Model: *"`NaN` is a decimal, and a column can only hold one kind of thing, so the only kind that can hold both 6200 and `NaN` is decimals — which means every step count in the column had to become a decimal, even though only one value was missing."* **Mark for the reasoning about *one kind*.** A sentence that only says "because one was missing" has described the cause and not the mechanism.

**The same rule, three times.**

| Week | What one odd thing went in | What the whole container became |
|---|---|---|
| 17 | one **word** in a list of numbers | everything became text — `<U21`, and `48` became `'48'` |
| 18 | one **decimal** in a list of whole numbers | everything became `float64` |
| **21** | one **hole** (`None`) in a column of whole numbers | everything became `float64`, and `6200` became `6200.0` |

**The rule:** *A container picks the one kind that can hold everything in it.* Same rule, three costumes; a student who spots the connection has had a very good term. *(A fourth costume, from this week's Worked Example 2: one quote mark round a number makes the whole column `object`.)* Fastest to notice is today's (`12` becoming `12.0` shows in the printed table); most dangerous is Week 17's `<U21`, because `'48'` prints as `48` and the next arithmetic either crashes confusingly or silently glues characters together. Any well-argued comparison earns the mark.

**Bug Log entries, done properly** (one loud, one silent):

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| Nineteen lines of traceback ending `KeyError: 'Runs'` | There is no column with that name | A capital letter. Column names are case-sensitive text | `df["runs"]`. Read the last line first, then find the `File` line with my own filename |
| Whole numbers printing as `6200.0`. **No error.** | The column had to become decimals | One cell is empty, and `NaN` is a decimal, so the whole column changed kind | Run `info()` and read the non-null count. Fixing the hole is Week 23; today, noticing it is the job |

### 🎨 Draw It

Open-ended; mark against these five things:

1. **The heavy frame goes round the columns only**, with a header rule under the names.
2. **The index strip is drawn outside that frame**, in grey, labelled *"row names — not a column"*. Four columns inside, not five.
3. **Ten rows, numbered from zero** — so the last one is 9, not 10.
4. **Each column labelled with its dtype and non-null count**, with the two number columns distinguished for the right reason: a `float64` because decimals were typed (count 10) versus a `float64` because a value is missing (count 9).
5. **The thing that earns the marks:** every other value in the `NaN` column marked with a note (`142` written as `142.0`) — they all changed and nobody touched them.

The three write-in questions: **How many entries?** 10. **How many columns?** 4. **Which column is `object`, and why?** The words column, because it holds words — and the follow-up worth answering unprompted: *if a number column had said `object`, that would be a bug (a quote mark or stray space)*. **Which is `int64`?** The whole-number column that did *not* get the hole. **What did the one `NaN` change?** Model: *"the non-null count dropped from 10 to 9, the dtype went from `int64` to `float64`, every other value in that column grew a decimal point, and the `int64` disappeared from the tally line, because no whole-number column was left."*

### 📊 Self-Check

No right answers; it is a record of where the student is, most useful when honest. Three rows matter most. **"Read every line of `df.info()` out loud in my own words"** is the week's objective — if it is not a 😀, the fix is not more reading but doing it out loud, once, on a table they built (eleven lines, three minutes). **"Explain what the index is, and why it is not a column"** — if 😕, next week will be genuinely confusing; redo the three proofs from A1(f). **"Notice a whole-number column printing as decimals and say what caused it"** — if 😀, they have the most useful habit in pandas.

### Answers to every question posed in the lesson

- *"What's different between your table and pandas's?"* → Almost nothing — and one took thirty lines and the other took one.
- *"What did pandas work out for itself?"* → The column names, the widths, the alignment, the row numbering, including lining 10 and 11 up under the single digits.
- *"Where did the column names come from?"* → The dictionary keys.
- *"Was Week 14 wasted?"* → No. You now know what the one line is doing, and you know what missing labels cost.
- *"What did you lose in Week 17 and what are you getting back?"* → The labels: which column is which and whose row is whose.
- *"Does this replace numpy?"* → No. Every column is a numpy array underneath; axes and masks still do the arithmetic.
- *"What are the two containers in pandas?"* → DataFrame (the table) and Series (one column).
- *"How many columns has the squad table got?"* → Five. The index is not one of them.
- *"Is the index a column?"* → No. It is the row's name. It has no column name and `df[0]` is a `KeyError`.
- *"What does `head()` tell you? What does `info()` tell you?"* → What it looks like; whether you can trust it.
- *"How many rows will `head()` print?"* → Five, unless you say otherwise.
- *"Name the four things in the `head()` printout."* → Column names, index, values, alignment.
- *"Which of the four is not part of your data?"* → The index.
- *"How many rows and columns will `info()` say?"* → Twelve and five.
- *"Line one — what's it telling you?"* → It really is a DataFrame.
- *"Line two?"* → Twelve rows, named 0 to 11 — and it agrees with `len(squad)`.
- *"Read me the `runs` line."* → Column 2 is `runs`, twelve of twelve cells filled, whole numbers.
- *"What is a non-null count?"* → How many cells actually have something in them.
- *"You expected numbers and it says `object` — good or bad?"* → Bad. There is text hiding in a number column.
- *"Add up the dtypes tally."* → Five, matching the column count.
- *"What does `memory usage` tell you?"* → How much space it takes. Ignore it.
- *"How many lines is that error, and what does the last one say?"* → Nineteen, and `KeyError: 'Runs'`.
- *"Is there a column called `Runs`?"* → No. It is `runs`. Column names are case-sensitive.
- *"Which `File` line can you do something about?"* → The one with your own filename in it: `File "table.py", line 20`.
- *"What dtype will `age` be?"* → `int64` — until a `None` goes in.
- *"Will the `None` version crash?"* → No. It prints `NaN` and changes the whole column to `float64`.
- *"Read me Asha's age."* → `12.0`. Nobody touched Asha.
- *"What's the only kind that can hold both `12` and `NaN`?"* → Decimals — `float64`.
- *"Where have you seen this rule before?"* → Week 17 (`<U21`) and Week 18 (`float64`). Three costumes, one rule.
- *"'Mon' appears twice. Is that a problem?"* → Two rows may share a value; an index is meant to be different for every row.
- *"Does the entry count match your paper grid?"* → It must. If not, a row was lost or doubled while typing.

---

## 🔮 Next Week Preview

Next week answers the question every student asks about ten minutes into this one: **"that's lovely, but how do I get one *row*?"** Square brackets on a DataFrame ask for a *column*, so `df[0]` is a `KeyError` and there is no obvious way in. Week 22 gives two ways, and the whole lesson is about knowing which one you are using: **`df.loc[1, "age"]`** looks a row up **by its name** — its index label — and a column up by *its* name, which reads beautifully and is what you want almost always. **`df.iloc[1, 2]`** looks both up **by counting**, which is exactly Week 19's `arr[1, 2]` and is what you want when you genuinely mean "the second row, third column". Two brackets, two ideas, and the trap is that on a fresh table with a default index **they give the same answer** — so the difference is invisible until it matters.

And then it matters, hard, because Week 22 also brings **filtering**: `df[df["age"] > 12]`, which is last week's boolean mask applied to a whole table at once. The rows that survive **keep their original index labels** — so a filtered table's index reads something like `0, 3, 4, 7`, with gaps. At that moment `.loc[1]` and `.iloc[1]` stop agreeing, permanently, and a student who thought the index was "just the row count" has a very confusing afternoon. Which is precisely why this week was firm about the index being a **name**.

**Prep early:** three things, and none of them is an install, which will be a relief. **Keep this week's `myweek.py` and `table.py`** — next week works on exactly these two tables, and the "look what happened to the index" moment needs a table they already know by heart. **Have the printed `head()` output to hand with the index circled**, because the single hardest idea next week is that `0, 3, 4, 7` are names and not positions, and a circled printout beats any amount of explaining. And **read the `info()` explanations from tonight's homework before the lesson.** They are the best evidence you will get all term of whether the student is *reading* output or *skimming* it — and Week 22 is a lesson where skimming produces a confident wrong answer within about four minutes.

---

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Student Guide](../student-guide/week-21.md) · [Workbook](../workbook/week-21.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
