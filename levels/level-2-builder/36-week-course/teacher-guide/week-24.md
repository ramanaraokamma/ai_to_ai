# Week 24 — Mess Detective

[⬅ Week 23](week-23.md) · [Course Home](../README.md) · [Week 25 ➡](week-25.md) · [Student Guide](../student-guide/week-24.md) · [Workbook](../workbook/week-24.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — Mess Detective. Forty broken rows, four repairs, six questions, one trap. |
| **Big idea** | `groupby` answers *"what's the average per house?"* in one line — **and hides how many rows each answer came from.** |
| **New vocabulary** | duplicate · string method · derived column · groupby · aggregate |
| **New syntax** | `df.drop_duplicates()` · `df["c"].value_counts()` · `df["c"].str.strip().str.title()` · `df["new"] = ...` · `df.groupby("c")["v"].mean()` |
| **Materials** | Printed workbook pages 24.1–24.10 · **last week's cleaning log sheet, continued — not a fresh one** · a printed copy of the forty-row table (for the paper fallback and for circling things) · the Bug Log |
| **Tech needed** | Laptop with Python 3 and pandas. **`house_raw.csv` must exist in the student's folder before class** — the prep script writes it. A paper fallback exists; see Prep. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |

> **⚠️ Watch out:** the planted trap is that **one house has two members**. Its average score is 95.00, it sits proudly at the top of the table, and `groupby(...).mean()` says nothing at all about where it came from. **Do not warn the student.** Let them read out "Gold is the best house" and then ask one question: *"how many people is Gold?"* That question is the lesson.

> **💡 Try this:** open `house_raw.csv` in a plain text editor before class and look at the `house` column with your own eyes. You will find you cannot see the difference between `Blue` and ` Blue`. Neither can the student. **That is why the count is the evidence and your eyes are not.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Remove duplicate rows** with `drop_duplicates()` and **state exactly how many went, and which**.
2. **Tidy several spellings of one word into one** with `.str.strip().str.title()`, and say why `title` alone is not enough (strip is also needed).
3. **Add a derived column** computed from columns already in the table.
4. **Group by a column and aggregate**, and **report the group sizes alongside the averages**.
5. **Print the before and after shape** of the table and account for the difference out loud.

Observable evidence: the sentence *"forty rows in, thirty-eight out, and the two that went were Bela Roy and Farah Aziz"*; fourteen spellings collapsing to four houses in one line; a `groupby` result with an `n` column beside the average; and the group sizes printed and checked to sum to 38.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**Read this once, slowly — about 25 minutes. It contains everything you need.** You do not need to have programmed before.

### 1. What this lab is for

Last week the student repaired a **twelve**-row table, and could see every problem with their eyes. This week the table has **forty** rows, which is past the point where eyes work. So the diagnosis has to be done with commands, and the commands become the evidence.

Three of the four repairs are quick. The fourth — `groupby` — is the most powerful single line of pandas in this whole course, and it comes with a trap that the entire term has been building towards.

**The lab in one sentence:** find the mess with commands, fix it in four lines, add a column that was not there, then ask six questions — and never report an average without saying how many rows it came from.

### 2. The table, and the four things wrong with it

The prep script writes `house_raw.csv`: 40 rows, 6 columns — `name`, `age`, `house`, `club`, `hours`, `score`. **Run `make_house_data.py` from the Prep Checklist below first** — none of the blocks in this section can run until that file exists. Here is what a diagnosis finds. **Run every one of these before class so the numbers are in your head.**

```python
import pandas as pd

raw = pd.read_csv("house_raw.csv")

print("shape           :", raw.shape)
print("duplicate rows  :", raw.duplicated().sum())
print("house spellings :", raw["house"].nunique())
print("club spellings  :", raw["club"].nunique())
print("holes per column:")
print(raw.isna().sum())
```

```text
shape           : (40, 6)
duplicate rows  : 2
house spellings : 14
club spellings  : 8
holes per column:
name     0
age      6
house    0
club     0
hours    0
score    0
dtype: int64
```

**Four numbers, four problems, and they are the same four as last week:**

| The problem | The number | The fix, this week |
|---|---|---|
| The same row twice | **2** duplicate rows | `drop_duplicates()` |
| Several spellings of one thing | **14** house spellings, **8** club spellings | `.str.strip().str.title()` |
| Holes | **6** missing ages | `fillna(13)` — last week's skill, revised |
| Text pretending to be numbers | none this week | — |

Fourteen spellings. There are **four** houses. That gap is the hook.

### 3. `duplicated()` and `drop_duplicates()`

> **duplicate** — a row that is identical to another row in every single column.

**Always look at them before you delete them.** This is a judgement, not a keystroke.

```python
print(raw[raw.duplicated(keep=False)])
```

```text
          name   age  house   club  hours  score
1     Bela Roy  14.0    Red  music    5.0     90
5   Farah Aziz  12.0  green  chess    6.0     95
34    Bela Roy  14.0    Red  music    5.0     90
37  Farah Aziz  12.0  green  chess    6.0     95
```

- `raw.duplicated()` — go down the table and mark each row `True` if you have already seen an identical row above it. **The first copy is marked `False`**; only the later ones are marked `True`. That is why `duplicated().sum()` says 2 and not 4.
- `keep=False` — "show me **both** copies, not just the second one". Without it you only see rows 34 and 37 and you cannot compare them with anything.
- **Four rows, two people.** Two pupils genuinely called Bela Roy would be a coincidence. Two rows where the name, the age, the house, the club, the hours **and** the score all match is a typing slip — somebody scrolled and lost their place. **Every single field matching is the giveaway**, and it is the reason you can delete with a clear conscience.

```python
clean = raw.copy()
print("before:", clean.shape)
clean = clean.drop_duplicates()
print("after :", clean.shape)
clean = clean.reset_index(drop=True)
```

```text
before: (40, 6)
after : (38, 6)
```

- `drop_duplicates()` — keep the first copy of each row, throw the later copies away.
- **`clean = ` on the front is not optional.** Like `sort_values`, like `fillna`, this hands you back a *new table*. Without the assignment nothing changes and nothing warns you. That is the third week running with the same silent bug, and this week it should be the student who spots it.
- `reset_index(drop=True)` — renumber the surviving rows 0, 1, 2, … and throw the old numbering away. Without `drop=True` the old numbers become an extra column, which nobody wants. This is optional but tidy; do it once, immediately after the drop, and never again.

**The habit that matters more than the command:** print the shape before and after, and **be able to account for the difference out loud.** `40 − 2 = 38`, and the two that went were Bela Roy and Farah Aziz. A student who can say that sentence will catch a mistaken drop later. A student who only says "it worked" will not.

![Two rows went. You have to be able to name them.](../figures/fig-w24-2-duplicate-rows-removed.svg)
*Figure 24.1 — Print the shape before and after. If you cannot account for the difference, stop and look again.*

### 4. `value_counts()` — the count that beats your eyes

```python
print(raw["house"].value_counts())
```

```text
Red       8
Green     5
Blue      5
green     4
blue      4
red       3
BLUE      3
RED       2
blue      1
 Blue     1
GREEN     1
green     1
gold      1
Gold      1
Name: house, dtype: int64
```

- `value_counts()` — count how many times each different value appears, biggest first.
- **Fourteen lines.** There are four houses in this school.
- And look at lines 9, 10 and 12. `blue`, ` Blue` and `green` **appear twice in this list**, which is impossible — unless they are not actually the same piece of writing. One has a space on the end. One has a space on the front. **You cannot see it, and that is the point.**

> **The sentence to say out loud, and to mean: the computer is right. Those really are fourteen different pieces of writing. `"Blue"` and `"Blue "` are as different to a computer as `"Blue"` and `"Banana"`.**

That reframe matters. Students want to say the computer is being stupid. It is being exact, and exactness is the only reason it can be trusted at all.

### 5. The `.str` accessor, and why `title` alone is not enough

> **string method** — a command that works on writing. `strip` removes spaces from the ends; `title` makes the first letter a capital and the rest lower case.

> **`.str`** — the doorway that lets a string method work on **a whole column at once** instead of one value at a time. Without `.str` pandas has no idea you meant to do it to every cell.

```python
clean["house"] = clean["house"].str.strip().str.title()
print(clean["house"].value_counts())
print("nunique:", clean["house"].nunique())
```

```text
Blue     14
Red      12
Green    10
Gold      2
Name: house, dtype: int64
nunique: 4
```

**Read the chain left to right — it happens in the order you read it:**

1. `clean["house"]` — the house column, 38 pieces of writing.
2. `.str.strip()` — take the spaces off both ends of every one. `"blue "` becomes `"blue"`. `" Blue"` becomes `"Blue"`.
3. `.str.title()` — capital first letter, everything else lower case. `"blue"`, `"BLUE"` and `"Blue"` all become `"Blue"`.
4. `clean["house"] = ` — put the repaired column back. **Again, no assignment means nothing happened.**

**Fourteen became four.** And the arithmetic checks out: Blue was `Blue` 5 + `blue` 4 + `BLUE` 3 + `blue ` 1 + ` Blue` 1 = **14**. Nothing was lost, nothing was invented. Make the student do that sum; it is thirty seconds and it turns a magic trick into arithmetic.

**Now a real trap, worth staging.** What if you do `title` without `strip`? Here it is on a fresh, still-messy copy, so you can see it for yourself:

```python
messy = pd.read_csv("house_raw.csv").drop_duplicates().reset_index(drop=True)
print(messy["house"].str.title().value_counts())
print("nunique:", messy["house"].str.title().nunique())
```

```text
Red       12
Blue      12
Green      9
Blue       1
 Blue      1
Green      1
Gold       1
Gold       1
Name: house, dtype: int64
nunique: 8
```

**Eight, not four** — and the printout looks like it worked. `Blue` appears three times (one with a trailing space, one with a leading space). `Green` appears twice. `Gold` appears twice. The spaces are still there, and **a space prints as nothing**, so the output looks like pandas has lost its mind.

> **You need `strip` AND `title`. `title` on its own leaves the spaces, and the spaces print as nothing, so the bug is invisible in the output and visible only in the count.** (Teacher note: `.str.strip().str.title()` and `.str.title().str.strip()` give identical results, so the order is a habit, not a rule. Do not tell the student that reversing them breaks anything; it does not. Leaving `strip` out is the bug.)

![Five spellings are five houses until you say otherwise](../figures/fig-w24-1-four-spellings-one-house.svg)
*Figure 24.2 — strip first, then title. Title on its own leaves the spaces, and the spaces print as nothing.*

**The `club` column gets the same treatment**, and it is a good second repetition because the target case is different — club names read better in lower case, so `.str.lower()` rather than `.str.title()`:

```python
clean["club"] = clean["club"].str.strip().str.lower()
print(clean["club"].value_counts())
```

```text
chess    14
music    12
art      12
Name: club, dtype: int64
```

Eight spellings, three clubs, and 14 + 12 + 12 = **38**. Every row accounted for.

### 6. The six missing ages, and a derived column

**First, last week's repair, done now so nothing later trips over a hole.** There are six missing ages:

```python
print("median age:", clean["age"].median())
clean["age"] = clean["age"].fillna(13).astype(int)
print("holes in age now:", clean["age"].isna().sum())
```

```text
median age: 13.0
holes in age now: 0
```

That is exactly Week 23, with six holes instead of three. **It has a cost, and section 10 is about the cost** — do not let it slide past as routine.

Now the new thing.

> **derived column** — a new column worked out from columns you already have. Nothing new arrives from outside; the table does arithmetic on itself.

```python
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)
print(clean.head())
```

```text
         name  age  house   club  hours  score  points_per_hour
0  Aarav Shah   13    Red  chess    3.5     72            20.57
1    Bela Roy   14    Red  music    5.0     90            18.00
2     Chen Wu   13   Blue  chess    2.0     55            27.50
3  Divya Nair   13   Blue    art    4.5     83            18.44
4   Emeka Obi   13  Green  music    3.0     61            20.33
```

- `clean["score"] / clean["hours"]` — divide the whole score column by the whole hours column, **row by row**. 38 divisions, one line. This is Week 18's vectorized arithmetic, on named columns.
- `.round(2)` — two decimal places, so the numbers are readable.
- `clean["points_per_hour"] = ` — **a name on the left that does not exist yet creates a new column.** That is the whole syntax. If the name already exists, it is overwritten instead, silently, so choose new names carefully.
- Hand-check row 0: 72 ÷ 3.5 = 20.571… → **20.57** ✔. Do this out loud, every time you make a derived column.

**And the reason derived columns are interesting, not just useful:** they can turn the story upside down.

```python
print(clean.sort_values("points_per_hour", ascending=False).head(5)[["name", "house", "score", "hours", "points_per_hour"]])
```

```text
           name  house  score  hours  points_per_hour
18    Sami Aden  Green     48    0.5             96.0
7    Hugo Silva    Red     45    0.5             90.0
32   Greta Hahn   Blue     42    0.5             84.0
6    Gita Menon   Blue     78    1.5             52.0
14  Omar Haddad   Blue     52    1.0             52.0
```

**The top three by points-per-hour are three of the lowest scorers in the school** — 48, 45 and 42. They all worked half an hour. **A new column made a new ranking, and neither ranking is a lie.** Which one you report is a choice, and it is the same kind of choice as fill-versus-drop last week: defensible either way, indefensible unaccounted for.

This is also a good place to be honest with a sharp student: dividing by 0.5 doubles a number, so `points_per_hour` mostly measures *who did the least work*, not who is best. That is a real weakness of the measure and worth saying so.

![A new column, worked out once per row](../figures/fig-w24-5-derived-column-per-row.svg)
*Figure 24.3 — A derived column can turn the ranking upside down. So choose it on purpose.*

### 7. `groupby` — split, apply, combine

> **`groupby`** — sort the rows into piles by the value in one column, do one calculation on each pile, and stack the answers into a small result table.

> **aggregate** — squash many rows into one number: a mean, a count, a maximum.

The analogy, and it is a good one because it is physically true: you have 38 exam papers. You **sort them into piles by house** — that is the *split*. You add up each pile and divide by its size — that is the *apply*. You write the four averages on one sheet — that is the *combine*.

```python
print(clean.groupby("house")["score"].mean().round(2))
```

```text
house
Blue     74.36
Gold     95.00
Green    65.20
Red      74.25
Name: score, dtype: float64
```

**Read the line right to left, which is how it was built:**

- `clean.groupby("house")` — make the piles, one per different value in the `house` column.
- `["score"]` — of everything in each pile, I only care about the score column.
- `.mean()` — one average per pile.
- `.round(2)` — two decimal places.

**Hand-check one pile every single time.** Gold has two members with 97 and 93: 97 + 93 = **190**, and 190 ÷ 2 = **95.00** ✔. That check takes ten seconds and it is what converts `groupby` from magic into arithmetic.

**One line.** In Week 15 this same answer took a loop, a dictionary, an `if` and about fifteen lines, and every one of those lines was theirs to get wrong. Say that out loud — the student wrote that code and remembers it.

![Sort into piles, then one number per pile](../figures/fig-w24-3-groupby-buckets-then-mean.svg)
*Figure 24.4 — 38 rows in, 4 rows out. Hand-check one pile every time.*

### 8. The trap, and it is the whole point of the lab

Look at that result again. **Gold, 95.00, top of the table.** Gold is the best house in the school by a mile.

Except: **how many people is Gold?**

```python
print(clean.groupby("house")["score"].size())
```

```text
house
Blue     14
Gold      2
Green    10
Red      12
Name: score, dtype: int64
```

**Two.** Gold is two people. One of them being off school that day would leave Gold's average resting on a single pupil's score (97 or 93), and one ordinary pupil joining would cut its lead over Blue by about a third.

**Nothing in the `.mean()` output told you that.** Four numbers, four house names, and no hint that one of them came from two rows and another from fourteen. The printout was completely honest and completely misleading, and the student read "Gold is the best house" straight off it.

The fix is one command, and it must become automatic:

```python
print(clean.groupby("house").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

```text
        n    avg
house           
Blue   14  74.36
Gold    2  95.00
Green  10  65.20
Red    12  74.25
```

- `.agg(...)` — do several aggregations at once, and name each result column.
- The pattern is `new_name=("existing_column", "what_to_do")`. So `n=("score", "size")` means *"make a column called `n` holding how many rows are in each pile"*.
- Available operations: `"size"`, `"count"`, `"sum"`, `"mean"`, `"median"`, `"min"`, `"max"`.
- The result is a small table with the house names down the side. Those house names are now the **index** — the row labels — which is Week 21's idea coming back.

> **The rule, and put it on the board: never print a group average without its group size beside it. Every single time. `agg(n=..., avg=...)`, or you will mislead yourself.**

**And the check that goes with it:** the group sizes must add up to the number of rows in the table.

```python
sizes = clean.groupby("house")["score"].size()
print("sizes sum to", sizes.sum(), "and the table has", len(clean), "rows")
```

```text
sizes sum to 38 and the table has 38 rows
```

14 + 12 + 10 + 2 = 38 ✔. If those two numbers ever disagree, **rows have gone missing**, and §9 explains the usual reason.

![The average hides how many it came from](../figures/fig-w24-4-groupby-hides-group-size.svg)
*Figure 24.5 — Print .size() next to .mean(), every single time, before you say a word out loud.*

### 9. The second silent trap: `groupby` drops holes, without saying so

This one is worth knowing about because it will happen to somebody. **If the column you group by has holes in it, those rows silently vanish from the result.** Here it is on a fresh copy where the six missing ages have **not** been filled:

```python
holey = pd.read_csv("house_raw.csv").drop_duplicates().reset_index(drop=True)
sizes = holey.groupby("age")["score"].size()
print(sizes)
print("sums to", sizes.sum(), "but the table has", len(holey), "rows")
```

```text
age
12.0    10
13.0    12
14.0    10
Name: score, dtype: int64
sums to 32 but the table has 38 rows
```

**Thirty-two, not thirty-eight. Six rows are simply not in the answer, and nothing said so.** They are the six pupils whose ages nobody recorded — there is no pile for them, so they were left out.

That is exactly why the sum check exists, and it is why the lab fills the ages before asking anything about age. It is also the same lesson as last week from a different angle: **repairs change answers, and so do repairs you forgot to make.**

**One more thing about `groupby` that surprises people.** Group by two columns and you get only the combinations that **actually happen**:

```python
print(clean.groupby(["house", "club"]).size())
```

```text
house  club 
Blue   art       2
       chess     3
       music     9
Gold   art       2
Green  art       8
       chess     1
       music     1
Red    chess    10
       music     2
dtype: int64
```

Four houses times three clubs is twelve possible combinations. **Nine appear.** There is no Red/art, no Gold/chess and no Gold/music — and pandas does not show them as zero, it just leaves them out. Read a `groupby` result knowing it is *a list of what exists*, not a complete grid.

### 10. What the age fill cost

The fill happened back in section 6 and it looked routine. It was not.

**Before** the fill, the twelve pupils with a *known* age of 13 average **71.92**. **After** filling six unknowns with 13, the age-13 group has **eighteen** pupils and averages **73.11**:

```text
      n    avg
age           
12   10  84.80
13   18  73.11
14   10  61.00
```

**The fill added six people to one group and moved its average.** That is not a bug — it is what filling means. But it means the log must say so, and it means the general rule from last week applies with force: *never fill a column with a guess and then make that column the subject of your question.* Question 4 of the lab is a question about age, and the age column contains six guesses.

### 11. The three misconceptions you will actually meet

**Misconception 1: "the computer is being stupid about `Blue` and `Blue `."** It is being exact. Two pieces of writing are the same only if every character matches, and a space is a character. Reframe it as a *feature*: if the computer quietly decided that `Blue ` and `Blue` were the same, it would also have to decide about `Blu` and `Bleu`, and then you could never trust it about anything.

**Misconception 2: "Gold is the best house."** They will say it, out loud, from a perfectly honest printout. **Do not correct it with information.** Ask one question — *"how many people is Gold?"* — and let them go and find out. The self-correction is the lesson; a correction from you is just a fact.

**Misconception 3: "`groupby` gives you the answer."** `groupby` gives you *a* number. Which number depends on what you cleaned, what you filled, what you grouped by, and what you chose to aggregate. Five defensible pipelines give five different tables. The result of `groupby` is the *start* of a claim, not the end of one.

### 12. How deep to go, and where to stop

**Go this deep:**
- Look at duplicates before deleting them, and be able to name which rows went.
- Shape before, shape after, account for the difference out loud.
- `strip` before `title`, and the count — not the printout — is the evidence.
- Hand-check one group every time.
- **`.size()` beside `.mean()`, always.**
- Group sizes must sum to the number of rows.

**Stop before all of this:**
- **`drop_duplicates(subset=[...])`** — dropping on *some* columns rather than all. Real and useful; a much bigger judgement call ("is one pupil allowed two rows?"). Mention it exists if asked.
- **`.str.replace()`, `.str.contains()`, regular expressions.** A whole world. Not today.
- **`pivot_table`, `unstack`, multi-index gymnastics.** The two-column `groupby` printout above is as far as this course goes with nested groups.
- **`transform`, `apply`, `lambda`.** The professional way to fill each group with its own median. Beyond this course.
- **Weighted averages, standard deviation, confidence.** The *right* answer to "is Gold's 95 meaningful?" is statistics the student does not have yet. The honest and sufficient answer this week is **"two rows is not enough to say anything"**, and that answer is not a placeholder — it is correct.

---

### 13. 🧭 The Growing Map — stage three closes

The student guide carries a figure called **Where This Fits** — the same picture every week with one
more piece filled in. It is the only page that shows the learner the *shape* of the year rather than
the week. Today is the last lesson in stage three, which makes it a better-than-usual two minutes.

![The Level 2 pipeline in Week 24: still the holes and duplicates tile, the last box of stage three](../figures/fig-w24-0-where-this-fits.svg)

*Figure 24.0 — Week 24's version. The gold is on the same tile as last week, "holes · duplicates" —
and it is the last box in stage three. **Data** and **evaluation** are lit.*

**What to do with it, in about two minutes at the end of the lab:**

1. **Show it and ask a Week 24 question:** *"`groupby`, and the count you printed beside every mean —
   which box was that?"* The honest answer is *"the same one as last week"*, and that is the answer you
   want: today was the second half of one tile, not a new idea bolted on. Then the good one: *"what
   happens to this box next week?"* It goes white, and the gold jumps a whole stage right.
2. **Then count with them:** *"how many stages are solid now?"* Three of five. *"And we still have not
   drawn a single chart."* That sentence does more for motivation than any promise about next week.
3. **Have them update their own copy** — and write **`n = 2`** next to this tile. That is the Gold
   house. It is the smallest note in their notebook and the one most likely to stop them believing a
   number later.

> **🧑‍🏫 Why this is worth two minutes.** Labs feel like tidying up. The map is what turns forty
> repaired rows into a *stage you finished*, and end-of-stage is the only moment in the term where a
> learner can see a month of work as one shape. Do not skip it today of all days.

> **⚠️ Watch out:** **evaluation** is lit this week and some teachers assume that is a mistake, because
> nothing was scored. It is not. Printing the group size beside the mean *is* evaluation — it is asking
> how much a number is worth before you believe it, which is the same question Week 32 asks about
> accuracy. If a student asks why the pill is on, that is the sentence.

---

## 🧰 Prep Checklist

### 20 minutes the night before

**1. Create the data file (5 minutes).** Make `make_house_data.py` in the student's folder and run it **once**.

```python
# make_house_data.py - run this ONCE. It writes the broken 40-row table.
rows_text = """name,age,house,club,hours,score
Aarav Shah,13,red,Chess,3.5,72
Bela Roy,14,Red,music,5.0,90
Chen Wu,,BLUE,chess,2.0,55
Divya Nair,13,blue ,art,4.5,83
Emeka Obi,,Green,music,3.0,61
Farah Aziz,12,green,chess,6.0,95
Gita Menon,13, Blue,art,1.5,78
Hugo Silva,14,RED,MUSIC,0.5,45
Ivy Chen,12,Blue,chess,4.0,88
Jai Kapoor,13,green,art,2.5,67
Kira Das,14,Red,chess,3.0,74
Liam Byrne,,blue,music,5.5,81
Maya Iyer,12,Green, art,2.0,59
Noor Khan,13,red,chess,4.0,86
Omar Haddad,14,Blue,music,1.0,52
Priya Rao,12,GREEN,art,3.5,70
Quinn Reid,13,Red,chess,2.5,64
Rhea Bose,,blue,music,4.5,92
Sami Aden,14,Green,art,0.5,48
Tara Joshi,12,Red,chess ,5.0,97
Uma Pillai,13,Blue,music,3.0,76
Viraj Sen,14,green ,art,2.0,63
Wren Adeyemi,12,Red,chess,3.5,80
Xu Lin,13,BLUE,music,1.5,57
Yara Fadel,,Green,art,4.0,85
Zane Cooper,14,red,chess,2.5,69
Anika Verma,12,Blue,Music,5.0,93
Bruno Costa,13,green,art,1.0,50
Cleo Marks,14,Red,chess,3.0,73
Dev Anand,12,blue,music,4.5,89
Elif Demir,13,gold,art,2.0,97
Finn Walsh,,RED,chess,3.5,79
Greta Hahn,14,Blue,music,0.5,42
Hana Sato,12,Gold ,art,5.5,93
Bela Roy,14,Red,music,5.0,90
Ismail Toure,13,Red,chess,2.0,62
Jia Park,12,blue,music,4.0,84
Farah Aziz,12,green,chess,6.0,95
Kofi Mensah,14,Green,art,1.5,54
Lena Fischer,13,BLUE,chess,3.0,71
"""

with open("house_raw.csv", "w") as f:
    f.write(rows_text)

print("house_raw.csv written -", rows_text.count("\n") - 1, "data rows")
```

```text
house_raw.csv written - 40 data rows
```

**Open `house_raw.csv` in a plain text editor and try to spot the two spaces.** Line 5 is `Divya Nair,13,blue ,art,4.5,83` — trailing space. Line 8 is `Gita Menon,13, Blue,art,1.5,78` — leading space. **You will not see them, and neither will your student.** That is the single most useful thing to have experienced before you teach this.

**2. Run the diagnosis yourself (5 minutes).** Type it out; do not paste.

```python
# detect.py - Week 24 prep. What is wrong with this table?
import pandas as pd

raw = pd.read_csv("house_raw.csv")

print("shape           :", raw.shape)
print("duplicate rows  :", raw.duplicated().sum())
print("house spellings :", raw["house"].nunique())
print("club spellings  :", raw["club"].nunique())
print("holes per column:")
print(raw.isna().sum())
print("--- both copies of every duplicate")
print(raw[raw.duplicated(keep=False)])
print("--- the house column as it arrived")
print(raw["house"].value_counts())
```

**This is the exact output. If yours differs anywhere, stop and find out why.**

```text
shape           : (40, 6)
duplicate rows  : 2
house spellings : 14
club spellings  : 8
holes per column:
name     0
age      6
house    0
club     0
hours    0
score    0
dtype: int64
--- both copies of every duplicate
          name   age  house   club  hours  score
1     Bela Roy  14.0    Red  music    5.0     90
5   Farah Aziz  12.0  green  chess    6.0     95
34    Bela Roy  14.0    Red  music    5.0     90
37  Farah Aziz  12.0  green  chess    6.0     95
--- the house column as it arrived
Red       8
Green     5
Blue      5
green     4
blue      4
red       3
BLUE      3
RED       2
blue      1
 Blue     1
GREEN     1
green     1
gold      1
Gold      1
Name: house, dtype: int64
```

**3. Run the whole lab yourself (8 minutes).** Create `mess_detective.py`. This is the file the student builds in class, and running it once now is the difference between teaching confidently and reading aloud.

```python
# mess_detective.py - Week 24. Find the mess, fix it, count it, group it.
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.copy()

print("=== STEP 1: drop the duplicates")
print("before:", clean.shape)
clean = clean.drop_duplicates()
print("after :", clean.shape)
clean = clean.reset_index(drop=True)

print("=== STEP 2: fourteen house spellings become four")
clean["house"] = clean["house"].str.strip().str.title()
print(clean["house"].value_counts())

print("=== STEP 3: eight club spellings become three")
clean["club"] = clean["club"].str.strip().str.lower()
print(clean["club"].value_counts())

print("=== STEP 4: the six missing ages")
print("median age:", clean["age"].median())
clean["age"] = clean["age"].fillna(13).astype(int)
print(clean.isna().sum())

print("=== STEP 5: a column that was not there")
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)
print(clean.head())

print("=== STEP 6: average score per house, WITH the group size")
print(clean.groupby("house").agg(n=("score", "size"), avg=("score", "mean")).round(2))

print("=== STEP 7: the check that must always pass")
sizes = clean.groupby("house")["score"].size()
print("sizes sum to", sizes.sum(), "and the table has", len(clean), "rows")
```

Real output:

```text
=== STEP 1: drop the duplicates
before: (40, 6)
after : (38, 6)
=== STEP 2: fourteen house spellings become four
Blue     14
Red      12
Green    10
Gold      2
Name: house, dtype: int64
=== STEP 3: eight club spellings become three
chess    14
music    12
art      12
Name: club, dtype: int64
=== STEP 4: the six missing ages
median age: 13.0
name     0
age      0
house    0
club     0
hours    0
score    0
dtype: int64
=== STEP 5: a column that was not there
         name  age  house   club  hours  score  points_per_hour
0  Aarav Shah   13    Red  chess    3.5     72            20.57
1    Bela Roy   14    Red  music    5.0     90            18.00
2     Chen Wu   13   Blue  chess    2.0     55            27.50
3  Divya Nair   13   Blue    art    4.5     83            18.44
4   Emeka Obi   13  Green  music    3.0     61            20.33
=== STEP 6: average score per house, WITH the group size
        n    avg
house           
Blue   14  74.36
Gold    2  95.00
Green  10  65.20
Red    12  74.25
=== STEP 7: the check that must always pass
sizes sum to 38 and the table has 38 rows
```

**Delete `mess_detective.py` before class.** The student builds it.

**4. Print (2 minutes).** Workbook pages 24.1–24.10, plus **one copy of the forty-row table printed out** for circling and for the paper fallback. Find last week's cleaning log sheets — the log **continues** on the same paper.

### 5 minutes on the day

- `ls` in the terminal. Confirm `house_raw.csv` is there.
- `house_raw.csv` open in a text editor on a second tab.
- Last week's cleaning log on the table, with the next free line ready.
- Write on the board and leave up all lesson:

```
SHAPE BEFORE   ->   SHAPE AFTER   ->   ACCOUNT FOR THE DIFFERENCE

  never print   .mean()   without   .size()   beside it
```

### Fallback if the laptop or the install fails

**The paper version works, and the trap survives completely intact.**

Print the forty-row table. Then:

1. **Find the duplicates with a pencil (5 min).** Go down the `name` column and ring any name you see twice. Bela Roy and Farah Aziz. Then check *every field* of both copies and confirm they match. `40 − 2 = 38`.
2. **Tally the houses (10 min).** Five-bar gates, one column per spelling, exactly as they find them — `Red`, `red`, `RED` as three separate columns. They will produce fourteen columns and complain. **That complaint is the lesson.** Then let them merge the columns by hand and get Blue 14, Red 12, Green 10, Gold 2.
3. **The groupby, by hand (15 min).** Four piles of paper slips, or four columns on a whiteboard. Add each pile's scores and divide by its size. The sums are Blue **1041**, Red **891**, Green **652**, Gold **190**. Divide: 1041 ÷ 14 = **74.36**, 891 ÷ 12 = **74.25**, 652 ÷ 10 = **65.20**, 190 ÷ 2 = **95.00**.
4. **The trap, on paper (5 min).** Write the four averages on the board **with no counts**. Ask *"which is the best house?"* They will say Gold. Then write the counts beside them. Watch the room change. **This is more powerful on paper than on screen, because they did the division themselves.**

Do the typing next lesson as a warm-up. Week 25 is matplotlib and needs a clean table, so keep the paper answers.

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Four Houses, Fourteen Names | 7 | 7 | value_counts on the raw column. Count the houses. |
| 🧠 Concept — Split, Apply, Combine | 16 | 23 | duplicates, .str, derived columns, groupby |
| 💻 Live-Code Together — Four Repairs | 18 | 41 | Teacher types, student types along. Two deliberate mistakes |
| 🎲 Their Turn — Six Questions, One Trap | 20 | 61 | The six groupby questions, and Gold |
| 🔑 Wrap & Assign | 9 | 70 | The rule, three checks, homework |

---

### 🪝 Hook — Four Houses, Fourteen Names (7 minutes)

**Do this:** Terminal open, `house_raw.csv` loaded, nothing else on screen. **Do not show the table.** Type exactly this and nothing more.

```python
import pandas as pd
raw = pd.read_csv("house_raw.csv")
print(raw["house"].value_counts())
```

```text
Red       8
Green     5
Blue      5
green     4
blue      4
red       3
BLUE      3
RED       2
blue      1
 Blue     1
GREEN     1
green     1
gold      1
Gold      1
Name: house, dtype: int64
```

**Say this:**

> "This is a real school. Forty pupils. That command counted up how many are in each house.
>
> **How many houses has this school got?**"

Let them count. They will say four. Then they will look again and be less sure.

> "Count the **lines** on the screen for me."

*Fourteen.*

> "Fourteen. So according to the computer, this school has fourteen houses. Is the computer wrong?"

Let them argue. You want somebody to say *"it's just spelling"*.

> "Right — `Red`, `red` and `RED` are the same house and three different pieces of writing. Fine. But now look harder. **Look at line nine and line five.**"

Point at `blue 1` and `blue 4`.

> "`blue` appears **twice** in this list. Same spelling, same letters, two separate lines. That's impossible, isn't it? A count can't list the same thing twice.
>
> Unless they're not the same thing. Anyone?"

Let them work. Someone gets there or nobody does; both are fine.

> "One of them has **a space on the end.** `blue` and `blue-space`. And there's another one — ` Blue` — with a space on the **front**. And I'm going to be completely straight with you: **you cannot see them.** I can't see them. There is no way to look at that screen and tell which is which.
>
> So here's the thing I want you to take seriously today, and it goes against your instincts. **The computer is right.** Those really are fourteen different pieces of writing. To a computer, `"Blue"` and `"Blue "` are as different as `"Blue"` and `"Banana"`. It is not being stupid. It is being **exact**, and being exact is the only reason you can trust it about anything at all.
>
> Which means: **your eyes are not the evidence. The count is the evidence.**"

**Do this:** Now the plan for the lab.

> "Forty rows. Too many to check by eye — that's deliberate. So today you're a detective, and you work from counts, not from looking. There are four things wrong with this table. You'll find all four with commands, fix all four, and then ask it six questions.
>
> And one of your six answers is going to be wrong. Not wrong arithmetic — the arithmetic will be perfect. **Wrong conclusion.** Your job is to be the person who notices."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How many houses has this school got?" | Four — then doubt. | If they say fourteen, ask whether `Red` and `red` are different houses in real life. |
| "Why does `blue` appear twice in the count?" | One has a hidden space. | If nobody gets it, tell them, then show the raw text file. The reveal is worth the time. |
| "Is the computer wrong?" | No — it is being exact. | If they insist it is stupid, ask: "if it decided `Blue ` was `Blue`, should it also decide `Blu` is `Blue`? Where does it stop?" |
| "So what is the evidence — your eyes or the count?" | The count. | Write it on the board. It is the sentence the whole lab runs on. |

---

### 🧠 Concept — Split, Apply, Combine (16 minutes)

**Do this:** Board work plus a few typed lines. Keep the value_counts output on screen.

**Say this — part 1, duplicates:**

> "Problem one. Somebody typed this list in, scrolled, lost their place, and typed two rows again."

```python
print(raw.duplicated().sum())
```

```text
2
```

> **duplicate** — a row identical to another row in every single column.

> "Two. Now — **do not delete them yet.** Look at them first. Always. This is a decision, not a keystroke."

```python
print(raw[raw.duplicated(keep=False)])
```

```text
          name   age  house   club  hours  score
1     Bela Roy  14.0    Red  music    5.0     90
5   Farah Aziz  12.0  green  chess    6.0     95
34    Bela Roy  14.0    Red  music    5.0     90
37  Farah Aziz  12.0  green  chess    6.0     95
```

> "Four rows, two people. `keep=False` means 'show me **both** copies', so I can compare them.
>
> Now the judgement. **Could there be two pupils genuinely called Bela Roy?** Of course. Happens all the time. So how do I know this is a mistake?"

Let them find it.

> "**Every single field matches.** Same name, same age, same house, same club, same hours, **and the same score to the mark.** Two different people with the same name would not both score exactly 90 after exactly 5 hours. That's not a coincidence — that's a typing slip.
>
> That reasoning is the professional part. The command is one word."

**Say this — part 2, the string repair:**

> **string method** — a command that works on writing. `strip` takes spaces off the ends. `title` makes the first letter capital and the rest small.

> **`.str`** — the doorway that applies a string method to a **whole column at once**.

Write the chain on the board and read it left to right:

```
clean["house"].str.strip().str.title()
                    |          |
              take spaces   Capitalise
              off the ends  properly
```

> "Left to right. `strip` first, as a habit. And **leaving `strip` out matters more than anything else on this board**, because it produces an answer that looks completely fine.
>
> Why? Because if you `title` and never `strip`, `blue-space` becomes `Blue-space`. And on screen **a space prints as nothing.** So you get two lines that both say `Blue`, and it looks like the computer has broken. The bug is invisible in the printout and visible only in the count.
>
> Say it back to me: strip and —"

*Title.*

**Say this — part 3, a derived column:**

> **derived column** — a new column worked out from columns you already have.

> "We've got scores and we've got hours. So we can ask a question nobody put in the table: **how many marks did each pupil get per hour of work?**"

```
clean["points_per_hour"] = clean["score"] / clean["hours"]
       |                        |
   a name that doesn't      divide the whole column
   exist yet -> a NEW       by the whole column,
   column appears           row by row
```

> "That's it. **A name on the left that doesn't exist yet makes a new column.** And the division happens 38 times, one per row, from one line — that's the array maths from Week 18, on named columns.
>
> Hand-check the first one with me. Aarav got 72 in 3.5 hours. 72 divided by 3.5?"

*About 20.6.*

> "20.57. **Hand-check one row every time you make a new column.** It takes ten seconds and it has caught more mistakes than any other habit in this course."

**Say this — part 4, groupby. This is the big one.**

> "Now the most powerful line of pandas you will learn all year. Think about a stack of 38 exam papers on the desk.
>
> Step one: you sort them into piles by house. Four piles. That's called the **split**.
> Step two: you add up each pile and divide by how many are in it. That's the **apply**.
> Step three: you write the four averages on one sheet. That's the **combine**.
>
> Split, apply, combine. And `groupby` does all three."

Write it up:

```
clean.groupby("house")["score"].mean()
        |         |        |       |
    make the   pile by  only care  one number
    piles      house    about      per pile
                        score
```

> **`groupby`** — sort rows into piles by one column, do a calculation on each pile, stack the answers into a small table.

> **aggregate** — squash many rows into one number: a mean, a count, a maximum.

> "And here's what I want you to feel. **In Week 15 you wrote this.** A loop, a dictionary, an `if`, about fifteen lines, and every one of them yours to get wrong. Remember it?
>
> One line. Same answer. Sorted, labelled, and done.
>
> One promise before we run it, though. **Hand-check one pile, every single time.** If a pile has two members and you can add them in your head, do it. `groupby` is not magic and you should never let it feel like magic."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How do you know the Bela Roy rows are a mistake?" | Every field matches, including the score. | If they say "same name", push: "could two people share a name? What makes this different?" |
| "Why do we need `strip` as well as `title`?" | Otherwise the spaces survive, and they print as nothing so you can't see them. | Show it: `.str.title()` alone gives eight houses and a printout that looks broken. |
| "What does a name on the left that doesn't exist do?" | Makes a new column. | If they say "an error", just run it. |
| "72 in 3.5 hours — points per hour?" | About 20.6. | Do it on paper if they hesitate. The arithmetic is the point. |
| "What are the three steps of groupby?" | Split, apply, combine. | Use the exam-papers story again with actual paper. It is physical for a reason. |
| "What are you going to do every time you use groupby?" | Hand-check one pile. | Make them say it. You will hold them to it in ten minutes. |

---

### 💻 Live-Code Together — Four Repairs (18 minutes)

**Do this:** Student types in their own `mess_detective.py`. You type on the shared screen. Last week's cleaning log is beside the keyboard and **every repair gets a line before the next line of code is typed.**

---

**Step 0 — the copy, and the shape.**

```python
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.copy()
print("before:", clean.shape)
```

```text
before: (40, 6)
```

> "Write that number down. On paper. **Forty rows, six columns.** Everything we do today has to be accountable against it."

---

**Step 1 — DELIBERATE MISTAKE ONE. The silent one, and it should be the student who catches it.**

**Type this, exactly, with no `clean =` on the front.**

```python
clean.drop_duplicates()
print("after :", clean.shape)
```

```text
after : (40, 6)
```

Say nothing. Wait.

> "What did I ask for?"

*Drop the duplicates.*

> "And how many rows have we got?"

*Forty. Still forty.*

> "**Any error?**"

*No.*

> "Third week running. Who can tell me the rule?"

You want: *it gave you a copy and you threw it away.* If the student produces that sentence unprompted, **say so out loud and make a thing of it** — that is genuine progress, and it is worth more than the command.

```python
clean = clean.drop_duplicates()
print("after :", clean.shape)
clean = clean.reset_index(drop=True)
```

```text
after : (38, 6)
```

> "Forty to thirty-eight. **Now account for it. Two rows went — which two?**"

*Bela Roy and Farah Aziz.*

> "Good. That sentence is the whole habit: **'forty in, thirty-eight out, and the two that went were Bela Roy and Farah Aziz.'** If you can't say which rows went, you don't know that the right ones went.
>
> And `reset_index(drop=True)` renumbers the survivors 0 to 37 and throws the old numbering away. Do it once, right after the drop, and never again."

**Do this:** Log line, on last week's sheet.

```
 8 | drop_duplicates(): 40 rows -> 38 | Bela Roy and Farah Aziz each appeared
   |                                  | twice with EVERY field identical, incl.
   |                                  | the exact score. A typing slip, not two
   |                                  | people. Keeping both would double-count
   |                                  | them in every average.
```

---

**Step 2 — DELIBERATE MISTAKE TWO. `title` without `strip`.**

**Type this. Do not flag it.**

```python
clean["house"] = clean["house"].str.title()
print(clean["house"].value_counts())
```

```text
Red       12
Blue      12
Green      9
Blue       1
 Blue      1
Green      1
Gold       1
Gold       1
Name: house, dtype: int64
```

> "Better! Fourteen down to... hang on. Read me the lines."

*Red, Blue, Green, Blue, Blue, Green, Gold, Gold.*

> "`Blue` **three times**. `Green` twice. `Gold` twice. Eight lines for four houses, and the screen is telling me `Blue` is not the same as `Blue`.
>
> Is the computer broken?"

Let them get there. They saw this in the Hook.

> "**The spaces are still there.** `title` capitalises; it doesn't tidy. And a space prints as nothing, so the output looks insane while being perfectly correct.
>
> This is the worst kind of bug in this entire course: **no error, and a printout that makes you doubt the computer instead of your code.** Watch what one extra command does."

```python
clean["house"] = clean["house"].str.strip().str.title()
print(clean["house"].value_counts())
print("nunique:", clean["house"].nunique())
```

> **Note for you:** it is fine to run the full chain on the column you have already titled. `" Blue"` titled is still `" Blue"`, and `strip` then takes the space off, so the second pass lands on the right answer. Do **not** be tempted to write `raw["house"]` on the right-hand side to "start fresh" — `raw` has 40 rows and `clean` has 38, pandas would line them up by row label, and you would silently get Red 13 and Blue 13. **Never mix a 40-row column into a 38-row table.** It is a good thing to say out loud, because a sharp student will suggest exactly that.

```text
Blue     14
Red      12
Green    10
Gold      2
Name: house, dtype: int64
nunique: 4
```

> "**Four.** Now the arithmetic, because I promised you no magic. Blue was `Blue` five, `blue` four, `BLUE` three, and the two with hidden spaces one each. Five plus four plus three plus one plus one?"

*Fourteen.*

> "And Blue now has fourteen. **Nothing lost, nothing invented.** That sum is your proof.
>
> Same treatment for the clubs, except clubs read better in lower case, so `lower` instead of `title`."

```python
clean["club"] = clean["club"].str.strip().str.lower()
print(clean["club"].value_counts())
```

```text
chess    14
music    12
art      12
Name: club, dtype: int64
```

> "Fourteen plus twelve plus twelve?"

*Thirty-eight.*

> "Every row accounted for."

**Do this:** Two log lines, both with the reason.

```
 9 | house: .str.strip().str.title() | value_counts() showed 14 spellings of 4
   | 14 spellings -> 4 houses        | houses, two with spaces I could not see.
   |                                 | strip AND title: title alone leaves the
   |                                 | spaces and they print as nothing.
   |                                 | 5+4+3+1+1 = 14, so nothing was lost.
10 | club: .str.strip().str.lower()  | 8 spellings of 3 clubs. lower not title
   | 8 spellings -> 3 clubs          | because club names read better small.
   |                                 | 14+12+12 = 38, all rows accounted for.
```

---

**Step 3 — the six missing ages. Last week's skill.**

```python
print(clean.isna().sum())
print("median age:", clean["age"].median())
clean["age"] = clean["age"].fillna(13).astype(int)
print(clean.isna().sum())
```

```text
name     0
age      6
house    0
club     0
hours    0
score    0
dtype: int64
median age: 13.0
name     0
age      0
house    0
club     0
hours    0
score    0
dtype: int64
```

> "Six holes, median 13, filled, converted, zero holes. You did all of this last week — the only new thing is that there are six instead of three.
>
> But there is a cost, and it is going to show up in about ten minutes. **What did I just do to six pupils?**"

*Decided they're 13.*

> "So if one of your six questions is about **age**, how much do you trust the answer?"

Let that hang. Do not resolve it. Log line:

```
11 | Filled 6 missing ages with 13,  | 13 is the median of the 32 ages we know.
   | then astype(int)                | WARNING: 6 of the 18 "13-year-olds" are
   |                                 | 13 only because I said so. Do NOT trust
   |                                 | any answer that groups by age.
```

---

**Step 4 — the derived column.**

```python
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)
print(clean.head())
```

```text
         name  age  house   club  hours  score  points_per_hour
0  Aarav Shah   13    Red  chess    3.5     72            20.57
1    Bela Roy   14    Red  music    5.0     90            18.00
2     Chen Wu   13   Blue  chess    2.0     55            27.50
3  Divya Nair   13   Blue    art    4.5     83            18.44
4   Emeka Obi   13  Green  music    3.0     61            20.33
```

> "A seventh column, and nothing new came in from outside — the table did arithmetic on itself. **Hand-check row 2 with me: 55 divided by 2?**"

*27.5.*

> "Print the shape. **Thirty-eight rows, seven columns.** Six became seven and no rows moved."

---

**Step 5 — the first groupby, and the hand-check.**

```python
print(clean.groupby("house")["score"].mean().round(2))
```

```text
house
Blue     74.36
Gold     95.00
Green    65.20
Red      74.25
Name: score, dtype: float64
```

> "One line. Fifteen lines of Week 15, gone.
>
> **Now hand-check a pile. Which one can you do in your head?**"

They should pick Gold, because it has the biggest gap from the others. Show them the two rows:

```python
print(clean[clean["house"] == "Gold"])
```

```text
          name  age house club  hours  score  points_per_hour
30  Elif Demir   13  Gold  art    2.0     97            48.50
33   Hana Sato   12  Gold  art    5.5     93            16.91
```

> "97 plus 93?"

*190.*

> "Divided by 2?"

*95.*

> "**95.00.** Matches. Not magic — arithmetic, done by somebody else.
>
> Right. Six questions. Off you go."

**Say nothing about how many people Gold is.** They have just seen the two rows on screen and it will still not stop them. That is fine, and it is the point.

---

### 🎲 Their Turn — Six Questions, One Trap (20 minutes)

Full instructions in the next section. In outline: six `groupby` questions, hand-checking one pile each time (14 minutes); then the Gold conversation and the rule (6 minutes).

---

### 🔑 Wrap & Assign (9 minutes)

**Do this:** Put the plain `.mean()` output back on screen, on its own, with no counts.

```text
house
Gold     95.00
Blue     74.36
Red      74.25
Green    65.20
Name: score, dtype: float64
```

**Say this:**

> "That's the table you'd put in a report. Every number on it is correct. I've checked the arithmetic and so have you.
>
> Now read me the headline."

*Gold is the best house.*

> "And how many people is Gold?"

*Two.*

> "**Two.** So if one of them had a cold that day and didn't sit the test, what happens to Gold?"

Let them work it out. One member: 97 or 93 — still top. But with one row the number is just that pupil's score, and one ordinary extra pupil (73) would cut Gold's lead over Blue by about a third. The honest point is the fragility.

> "Gold's average is **two people**. Blue's is fourteen. And that printout — a perfectly honest printout, with no mistakes in it at all — **does not tell you that.**
>
> Nothing was wrong. No error. No bad arithmetic. **The number just didn't say enough**, and I read a conclusion off it that it couldn't support. That's the most common way people mislead themselves with data, and it happens to professionals, in newspapers, every single week.
>
> So one rule, and it goes in the Bug Log in your handwriting."

Write it on the board:

```
NEVER print .mean() without .size() beside it.
  agg(n=("score","size"), avg=("score","mean"))

And check: the group sizes must add up to len(df).
```

> "Second line matters too. **14 plus 12 plus 10 plus 2 is 38, and the table has 38 rows.** If those ever disagree, rows have gone missing from your answer and nothing told you. It happens whenever you group by a column that still has holes in it.
>
> And one last thing, which is the term in a sentence. Two weeks ago you learnt that two commands one letter apart can give two different answers with no error. Last week you learnt that filling a hole changes the answer, with no error. Today: **an average can be completely correct and completely misleading, with no error.**
>
> **Real data work isn't mostly about errors. It's about being the person who asks the extra question.**"

**Do this:** Run the three checks from "Assessing Understanding". Assign the homework. Hand out pages 24.1–24.10.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of **this week's actual code**, on Python 3.10 and pandas 1.5.3. Tracebacks are trimmed to the first and last lines, which are the ones that matter, and those are exact.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: 'Series' object has no attribute 'strip'` | "A whole column hasn't got a `strip`." | `clean["house"].strip()` — the `.str` doorway is missing. | `clean["house"].str.strip()`. `.str` is what says "do this to every cell". |
| `AttributeError: Can only use .str accessor with string values!. Did you mean: 'std'?` | "This column isn't writing, so string commands make no sense on it." | `.str` used on a number column — `clean["age"].str.strip()`. | Check `dtypes`. `.str` is only for `object` columns. (Ignore the "did you mean std" suggestion; it is a red herring.) |
| `AttributeError: 'function' object has no attribute 'str'` | "You gave me the command itself, not the result of running it." | Brackets missing: `.str.strip.str.title()` instead of `.str.strip().str.title()`. | Add the empty brackets after `strip`. Every method needs them, even with nothing inside. |
| `KeyError: 'hosue'` | "There is no column with that name to group by." | A typo in the column name inside `groupby`. | `print(clean.columns.tolist())` and copy the name exactly. |
| `KeyError: 'Column not found: scoer'` | "I made the piles, then couldn't find that column in them." | A typo in the column name **after** the `groupby`. | Same fix. Note the message wording is different — that tells you which of the two brackets is wrong. |
| `KeyError: 'hour'` | "No column called that." | `clean["score"] / clean["hour"]` — the column is `hours`. | Add the `s`. This is the most common derived-column bug. |
| `ValueError: Length of values (3) does not match length of index (38)` | "You gave me 3 values for 38 rows." | `clean["new"] = [1, 2, 3]` — a hand-typed list instead of a calculation on existing columns. | A derived column comes from other columns, or from one single value repeated. Not from a short list. |
| `TypeError: You have to supply one of 'by' and 'level'` | "Group by **what**?" | `groupby()` with empty brackets. | Name the column: `groupby("house")`. |
| **`<pandas.core.groupby.generic.DataFrameGroupBy object at 0x10650b460>`** | "You printed the piles themselves, not a number." | `print(clean.groupby("house"))` with no aggregation. | Add what to do with each pile: `["score"].mean()`. The piles are not a result. |
| **`<bound method GroupBy.size of ...>`** | "You printed the command, not what it returns." | `.size` with no brackets. | `.size()`. |
| `FutureWarning: The default value of numeric_only in DataFrameGroupBy.mean is deprecated.` | "You asked for the mean of everything, including the words." | `clean.groupby("house").mean()` with no column picked out. | Pick the column: `groupby("house")["score"].mean()`. Pandas will silently drop the text columns for you, and relying on that is how you end up averaging the wrong thing. |
| **No error, the shape is still `(40, 6)` after dropping duplicates** | Nothing is wrong. `drop_duplicates` returned a copy. | No `clean = ` on the front. | `clean = clean.drop_duplicates()`. Third week for this one — it should be the student who spots it. |
| **No error, still eight houses after `.str.title()`** | Nothing is wrong. `title` capitalises; it does not remove spaces. | `strip` missing. | `.str.strip().str.title()` (strip first, by habit). And trust `nunique()`, not the printout. |
| **No error, `value_counts()` shows the same word twice** | Nothing is wrong. They are genuinely different pieces of writing. | A leading or trailing space you cannot see. | `.str.strip()`. To prove it to a doubter: `print(clean["house"].unique())` shows the quote marks, and the spaces inside them. |
| **No error, the group sizes don't add up to `len(df)`** | Nothing is wrong. `groupby` silently ignores rows whose group value is a hole. | Grouping by a column that still has `NaN` in it — usually `age`, before the fill. | `fillna` the grouping column first, or accept the loss **and write it in the log**. Always run the sum check. |
| **No error, and a two-member group is at the top of the table** | Nothing is wrong. The arithmetic is perfect. | `.mean()` printed without `.size()`. | `agg(n=("score", "size"), avg=("score", "mean"))`. **This is the lesson, not a bug.** |

### How to teach debugging without giving the answer

Everything from Terms 1 and 2 still applies. This week adds two questions, and neither of them is about an error message:

15. **"Do the group sizes add up to the number of rows?"** One line, and it catches silently-dropped rows, an accidental extra filter, and a bad merge. It is the same instinct as Week 18's "how many went in and how many came out", applied to a summary instead of an array.

16. **"How many rows is that number made of?"** Ask it about *every* average, every time, including your own. It is not a debugging question — it is the question that stops a correct number being used to say a wrong thing.

And the sentence for this week, which is the sentence for the whole term:

> **"By now you have met three bugs that produce no error message: the wrong `loc`, the repair that never happened, and the average that came from two rows. Nothing on the screen warns you about any of them. Only the extra question does."**

---

## 🎲 The Activity, In Full

### Part A — Six Questions, Hand-Checked (14 minutes)

**Setup.** Student has `mess_detective.py` working through Step 5. Workbook page 24.6 has the six questions printed with space for an answer, a group size, **and a hand-check**. The board carries the rule: *never `.mean()` without `.size()`*.

**The rule that makes this activity work:** every answer must be reported as **the number AND how many rows it came from**. An answer without its `n` does not count, even if it is right.

---

**Question 1 — "How many pupils in each house?"**

```python
print(clean.groupby("house")["score"].size())
sizes = clean.groupby("house")["score"].size()
print("sizes sum to", sizes.sum(), "and the table has", len(clean), "rows")
```

```text
house
Blue     14
Gold      2
Green    10
Red      12
Name: score, dtype: int64
sizes sum to 38 and the table has 38 rows
```

**Hand-check:** 14 + 12 + 10 + 2 = 38 ✔. **Gold is already on screen as 2 and it will still not stop them.**

---

**Question 2 — "What is the average score in each house?"**

```python
print(clean.groupby("house").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

```text
        n    avg
house           
Blue   14  74.36
Gold    2  95.00
Green  10  65.20
Red    12  74.25
```

**Hand-check Gold:** 97 + 93 = 190, 190 ÷ 2 = **95.00** ✔
**Hand-check Green if they want a harder one:** the ten Green scores are 48, 50, 54, 59, 61, 63, 67, 70, 85, 95 → sum **652**, and 652 ÷ 10 = **65.20** ✔

---

**Question 3 — "What is the average score in each club?"**

```python
print(clean.groupby("club").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

```text
        n    avg
club            
art    12  70.58
chess  14  76.07
music  12  71.83
```

**Hand-check:** 12 + 14 + 12 = 38 ✔. And notice: **all three groups are big.** Chess winning by five marks over twelve-plus rows is a much sturdier claim than Gold's twenty-mark lead over two. Ask them which of the two results they would be willing to say out loud in assembly.

---

**Question 4 — "What is the average score at each age?"**

```python
print(clean.groupby("age").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

```text
      n    avg
age           
12   10  84.80
13   18  73.11
14   10  61.00
```

**Hand-check:** 10 + 18 + 10 = 38 ✔.

**And now the second trap, and this one they are armed for.** Ask: *"why has age 13 got eighteen pupils when 12 and 14 have ten each?"*

**Because we filled six missing ages with 13.** Six of those eighteen are 13 only because we said so. Before the fill, the twelve pupils with a *known* age of 13 averaged **71.92**; after it, eighteen pupils average **73.11**.

> **This is the rule from last week, biting: never fill a column with a guess and then make that column the subject of your question.** Question 4 is a question about age, and the age column contains six guesses. The answer is not worthless — but it must be reported with that sentence attached.

---

**Question 5 — "What are the average hours worked in each house?"**

```python
print(clean.groupby("house").agg(n=("hours", "size"), avg_hours=("hours", "mean")).round(2))
```

```text
        n  avg_hours
house               
Blue   14       3.18
Gold    2       3.75
Green  10       2.60
Red    12       3.17
```

Green works the least and scores the least. **Do not let them call that cause and effect** — it is two numbers going the same way on ten rows. Good question to ask: *"what would you need to know to be sure?"*

---

**Question 6 — "Who gets the most marks per hour of work?"**

```python
print(clean.sort_values("points_per_hour", ascending=False).head(5)[["name", "house", "score", "hours", "points_per_hour"]])
```

```text
           name  house  score  hours  points_per_hour
18    Sami Aden  Green     48    0.5             96.0
7    Hugo Silva    Red     45    0.5             90.0
32   Greta Hahn   Blue     42    0.5             84.0
6    Gita Menon   Blue     78    1.5             52.0
14  Omar Haddad   Blue     52    1.0             52.0
```

**Hand-check:** 48 ÷ 0.5 = **96.0** ✔

**And the best conversation of the lesson.** The top three are the three **lowest scorers in the school** — 48, 45 and 42. They all worked half an hour.

Ask: *"is Sami Aden the best pupil in the school?"* Then: *"is `points_per_hour` a good measure of anything?"*

The honest answer, and it is worth saying plainly: **dividing by half an hour doubles your number, so `points_per_hour` mostly measures who did the least work.** A derived column is a choice, and a choice can be a bad one. That is not a reason never to make derived columns — it is a reason to say which column you ranked by.

---

**What "finished" looks like for Part A:** six answers, each with its `n` written beside it, at least three hand-checks done on paper, and the sizes-sum-to-38 check printed at least once. **An answer with no `n` beside it is not finished**, however correct.

### Part B — The Gold Conversation (6 minutes)

**Setup.** Put the plain `.mean()` output back on screen with the counts removed. Ask the question straight.

**Step 1 — the claim.** *"Which is the best house?"*

They say Gold. Let them. **Do not react.**

**Step 2 — the one question.** *"How many people is Gold?"*

Let them go and find out, even though it was on screen four minutes ago in Question 1. **Finding it themselves is the whole event.**

**Step 3 — the fragility, out loud.** Ask, in this order:

1. *"What are Gold's two scores?"* → 97 and 93.
2. *"If one of them had been off school, what would Gold's average be?"* → 97 or 93. Still top, and now from **one** row.
3. *"If one average pupil — say 73 — joined Gold, what happens?"* → (97 + 93 + 73) ÷ 3 = **87.67**. Still top, but the lead over Blue has shrunk from 20.6 marks to 13.3 (about a third) from one person arriving.
4. *"How many pupils would have to join Blue to move it 20 marks?"* → an absurd number. **That is the difference between fourteen rows and two.**

**Step 4 — the sentence, written down.** Workbook page 24.7:

> *"Gold has the highest average score (95.00), but it has only ______ members, so ______________________."*

**Full marks needs the consequence, not just the number.** Model answers are in the Answer Key.

**Step 5 — the rule, in their handwriting, in the Bug Log.**

```
Never print .mean() without .size() beside it.
And check that the group sizes add up to len(df).
```

### Variation — easier

Cut to **three** questions: 1, 2 and 3. Skip the derived column entirely — the `groupby` trap is the objective and it survives with three questions.

Give them the `agg` line as a printed template with two blanks:

```python
print(clean.groupby("_______").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

For the hand-check, give them the four pile sums so they only have to divide: Blue **1041**, Red **891**, Green **652**, Gold **190**.

If the string chain is the blocker, do it in two separate lines with a `nunique()` between them so they see the two stages happen:

```python
messy = pd.read_csv("house_raw.csv").drop_duplicates().reset_index(drop=True)
messy["house"] = messy["house"].str.strip()
print(messy["house"].nunique())        # 11 - the spaces have gone
messy["house"] = messy["house"].str.title()
print(messy["house"].nunique())        # 4 - now the capitals have gone
```

```text
11
4
```

### Variation — harder

1. **Two columns at once.** `clean.groupby(["house", "club"]).size()` gives nine rows. Four houses times three clubs is twelve. *"Which three are missing, and does that mean nobody is in them or that pandas didn't tell you?"* (No Red/art, no Gold/chess, no Gold/music. Pandas only lists what exists — it does not show zeros.)
2. **Four statistics in one line.**
   ```python
   print(clean.groupby("house").agg(n=("name", "size"), avg_score=("score", "mean"),
                                    avg_hours=("hours", "mean"), best=("score", "max")).round(2))
   ```
   ```text
           n  avg_score  avg_hours  best
   house                                
   Blue   14      74.36       3.18    93
   Gold    2      95.00       3.75    97
   Green  10      65.20       2.60    95
   Red    12      74.25       3.17    97
   ```
   Then the good question: *"Red's best score is 97, the same as Gold's. Does that change how you feel about Gold's average?"*
3. **Break the sum check on purpose.** Re-run Question 4 **before** filling the ages. The sizes come to 32, not 38. *"Six rows are missing from that answer. Where did they go, and why didn't pandas say anything?"*
4. **A better derived column.** *"`points_per_hour` rewards doing nothing. Design a column that doesn't."* Any defensible answer counts — `score - hours * 10`, or ranking by score and only using hours to break ties. **The point is that a derived column is a design decision, and that a 12-year-old can make one.**
5. **The minimum group size.** *"Write a rule for our class: how many rows does a group need before you're allowed to say its average out loud?"* Then apply their own rule to the six answers. There is no correct number, and defending a choice is the exercise.

---

## ❓ Questions Students Ask This Week

**"Why doesn't pandas ignore spaces automatically?"**

Because it cannot know which spaces you meant. Sometimes a space is real data — a name like `de Souza`, an address, a sentence. If pandas silently trimmed everything, it would eventually destroy something you needed, and you would have no way to find out. **It is more useful to have a tool that is exact and a `strip` command than a tool that quietly tidies up behind you.** Exactness is what makes it trustworthy.

**"Is it wrong to delete the duplicate rows?"**

Not if you looked at them first and can say why. Every field matched, including the exact score after the exact hours, so it is a typing slip. **It would be wrong to delete them without looking**, and it would be wrong to delete them without a log line. There is a real case where you would keep both: if the table were "one row per test attempt" rather than "one row per pupil", two identical rows might be two genuine attempts that happened to score the same. **What a row means decides the answer**, and only you know what a row means.

**"How many people does a group need before its average means something?"**

**Nobody agrees, and this is the honest "nobody agrees" question of the week.** There is no number that is correct.

Some rules of thumb people genuinely use: never report a group smaller than 5; never report one smaller than 30 (that comes from a statistics result about how averages behave, and it is widely quoted and widely misapplied); report any size you like but always print it. Medical researchers work with groups of 12 when 12 is all the patients there are. Opinion polls want a thousand.

What everybody *does* agree on is much more useful than a number: **print the size, always, so the reader can decide for themselves.** That is why the rule of this lesson is not "ignore small groups" but "never hide the size". And a second thing everybody agrees on: **two is not enough**, for anything.

**"`groupby` gave me the houses in a weird order. Can I sort it?"**

They come out in alphabetical order of the group name, which is why Gold sits second. Sort the result by adding `.sort_values("avg", ascending=False)` on the end. **But notice what sorting by average does: it puts the two-member group at the top.** Sorting is presentation, and presentation can mislead all by itself. If you sort by average, print the size — which is the rule again, arriving from a new direction.

**"Could I use `.str.lower()` instead of `.str.title()`?"**

Yes, and it works just as well — you would get `blue`, `red`, `green`, `gold`, still four houses. The choice is cosmetic. **What matters is that you pick one and use it everywhere**, because `Blue` and `blue` are two houses again the moment you are inconsistent. This lab uses `title` for houses (they are proper names) and `lower` for clubs (they are ordinary words). That is a style decision, and it belongs in the log.

**"Why is `agg` written so strangely? `n=("score", "size")` looks like nothing else we've done."**

It is a genuinely odd-looking piece of syntax and you are right to notice. Read it as a sentence: **"make me a column called `n`, from the `score` column, by counting how many rows are in the pile."** The name you want goes on the left of the `=`; the pair in brackets is *which column* and *what to do with it*. Once you have written it four times it stops looking strange. It is worth the oddness because it is the only way to get the count and the average side by side in one command.

**"Our answer for Q4 is different from the one in the book. Is one of us wrong?"**

Probably neither. **Check your logs first, not your code.** If you filled the six missing ages with 13 and somebody else dropped those rows, your age-13 group has eighteen pupils and theirs has twelve, and your averages will differ. That is last week's lesson, and it is why the log travels with the answer. The only way to be *wrong* here is to have no log, because then nobody — including you — can tell which of the two things you did.

**"If `groupby` only shows combinations that exist, how do I know what's missing?"**

You have to work it out yourself, and that is a real weakness of the tool. Four houses times three clubs is twelve possible pairs; `groupby(["house", "club"]).size()` shows nine; so three do not occur. **The absence is invisible unless you do the multiplication.** Get into the habit of asking "how many combinations *should* there be?" before reading a two-column groupby. There are tools that fill the gaps in with zeros; they are a later lesson.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The student reads "Gold is the best house" and you correct them. | The instinct to teach is to supply the fact. | **Don't.** Ask one question — *"how many people is Gold?"* — and let them go and look. The correction has to be theirs or it is not learnt. |
| `.str.title()` is used without `strip`, the printout looks broken, and the student decides pandas is buggy. | The spaces print as nothing, so the output genuinely looks impossible. | Have `print(clean["house"].unique())` ready — it prints the quote marks, and the spaces show up inside them. Then point at Figure 24.2. |
| `drop_duplicates()` runs, no error, and the shape is still 40. | Missing assignment. Third week running. | Deliberate Mistake One. **Let the student catch it** — ask "any error? what did you ask for? what did you get?" and stay quiet. If they name the rule unprompted, say so out loud; it is real progress. |
| The whole lesson runs out of time before `groupby`. | The four repairs are satisfying and easy to over-explain. | Hard rule: **be typing `groupby` by minute 38.** If you are not, drop the `club` repair (it is a repetition of the `house` one) and drop the derived column. Never drop `groupby` or the Gold conversation. |
| Averages get reported with no group size, all lesson, and the rule does not stick. | Nothing forces it — the code runs fine either way. | Make the workbook table *require* an `n` box beside every answer, and refuse to accept an answer with the box empty. The paper design does the enforcing, not you. |
| The student decides Green scores badly **because** they work fewer hours. | The two numbers do go the same way, and that is genuinely suggestive. | Do not squash it — it is a good hypothesis. Ask *"what would you need to know to be sure?"* and let them list things. Then say the sentence: two numbers moving together on ten rows is a **reason to look further**, not a conclusion. |
| Hand-checking gets skipped because "it obviously worked". | It is the slowest part and it feels redundant. | Insist on Gold at minimum — 97 + 93 = 190, 190 ÷ 2 = 95. Ten seconds. It is also the number that sets up the entire trap, so skipping it costs you the lesson. |
| The cleaning log is started fresh instead of continued. | It feels like a new lesson, so a new sheet feels natural. | Continue last week's numbering — this week's first entry is number 8. **The point is that the log grows with the work**, and a log that restarts every lesson has already lost its purpose. |
| The student fixes the spellings by hand-editing the CSV. | Forty rows is just about editable, and they can see the problem. | Say it plainly: *"you fixed fourteen spellings and left no trace that anything was ever wrong. One line does all forty rows and the line **is** the record."* Then run the one-liner and let it be obviously better. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut, in this order:** the derived column, then the `club` repair (a straight repetition of `house`), then questions 4, 5 and 6. **Never cut `groupby` or the Gold conversation.** A student who cleaned one column and understood why a two-member average is not a result has had an excellent lesson.

**Reteach `groupby` with actual paper.** Write the 38 scores on slips — or take ten of them, which is enough. Then physically:

1. **Sort them into piles by house.** Say the word: *split*.
2. **Add each pile and divide by its size.** Say the word: *apply*.
3. **Write the four answers on one sheet.** Say the word: *combine*.

Then hold up the four-slip pile and the fourteen-slip pile **side by side, in the air**, and ask which average you would trust. The physical difference in thickness does the whole lesson, and nothing on a screen matches it.

**The copy-this-exactly scaffold.** Five blanks, nothing else to decide:

```python
# detective.py - fill in the five blanks. Nothing else needs changing.
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.copy()

print("before:", clean.shape)              # (40, 6)

# 1. Throw away the repeated rows. (Careful: something goes on the LEFT.)
clean = clean._______________()
print("after :", clean.shape)              # (38, 6)

# 2. Spaces off the ends FIRST, then capital letters.
clean["house"] = clean["house"].str._______().str._______()
print(clean["house"].value_counts())       # four houses

# 3. Average score per house, with the group size beside it.
print(clean.groupby("______").agg(n=("score", "____"), avg=("score", "mean")).round(2))
```

Answers: `drop_duplicates` · `strip` · `title` · `house` · `size`. Then ask the one question that must be asked out loud: **"which house has the highest average, and how many people is it?"**

**One sentence to leave them with:** *"An average with no count beside it is not an answer."*

### If the student is flying

1. **The missing combinations.** `clean.groupby(["house", "club"]).size()` gives nine rows out of twelve possible. Find the three that are missing (no Red/art, no Gold/chess, no Gold/music) and explain why pandas showed nine rather than twelve-with-zeros.
2. **Four statistics in one `agg`**, then the good question: Red's best score is 97, exactly the same as Gold's best. Does that change how they feel about Gold's 95.00 average?
3. **Break the sum check.** Run Question 4 before filling the ages: the sizes come to 32, not 38. Then explain, in writing, where six rows went and why nothing warned them.
4. **Design a better derived column.** `points_per_hour` rewards doing almost nothing. Design one that does not, defend it, and show it applied. Any defensible design is a full-mark answer.
5. **Write the minimum-group-size rule.** *"How many rows does a group need before you may say its average out loud?"* Pick a number, defend it, then apply it to all six answers and see how many survive. There is no right number, and that is the exercise.
6. **Clean it in a function.** Wrap all four repairs in `def clean_table(raw):` that returns the clean table. This is Week 10's function, doing real work, and it is the first line of the toolkit they will want in Week 34.

### If the student won't engage today

**Lead with the argument, not the code.** Write four averages on a whiteboard with no counts. *"Which house wins the trophy?"* They will pick Gold. Then write the counts. *"Still Gold? It's two people. Is that fair?"* **This is a fairness argument, and twelve-year-olds are extremely willing to have fairness arguments.** It is also the entire intellectual content of the lab, and it needs no laptop.

**Or make it theirs.** *"Your favourite team's top scorer has the best goals-per-game in the league. He played two games. Is he the best striker in the league?"* Same trap, their subject.

**The minimum viable lesson, if the day is a write-off:** the Hook (fourteen spellings, four houses) plus the Gold conversation on paper. Eight minutes. Then one line typed together — `clean["house"].str.strip().str.title()` — and stop. Week 25 is matplotlib and needs a clean table, so run the four repairs yourself and leave the file ready.

---

## ✅ Assessing Understanding

Run all three in the last five minutes. Say them exactly as written.

**Check 1 — account for the difference.** *"You started with forty rows and finished with thirty-eight. Account for the difference."*

> **A good answer:** two rows went, and they were the second Bela Roy and the second Farah Aziz — duplicates where every field matched. **Naming the two people is what makes this a pass**, not just saying "two duplicates went". If they cannot name them, have them re-run `raw[raw.duplicated(keep=False)]` — and make the point: if you cannot say which rows went, you do not know the right ones went.

**Check 2 — the string chain.** *"Why do we need `strip` as well as `title`?"*

> **A good answer:** because `title` only changes capital letters. If the spaces are still there, `"Blue "` becomes `"Blue "` — still a different word from `"Blue"` — and you end up with eight houses instead of four. Full marks adds the sting: **"and you can't see it, because a space prints as nothing, so the printout looks like the computer is broken."** If they say "because `strip` has to go first", gently correct it: either order works, what matters is that `strip` is there at all. Ask what `title` actually does to a space.

**Check 3 — the trap.** *"Gold has the highest average score in the school, 95.00. Should Gold get the trophy?"*

> **A good answer starts with a question of their own** — *"how many people is Gold?"* — or goes straight to it: Gold is two people, so its average is fragile in a way Blue's fourteen is not. Full marks names the consequence: one pupil joining or leaving Gold moves the number enormously, and no such thing could happen to a fourteen-row average. **A student who says "yes, 95 is the highest" has learnt the commands and missed the entire lab.** Send them back to Question 1's output, which has been on their own screen for twenty minutes.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot run the four repairs without the scaffold. Uses `.strip()` without `.str`. Reads `groupby` output as "the answer" with no sense that anything is behind it. |
| **2 — Emerging** | Runs the repairs with the printed template. Gets `groupby(...)["score"].mean()` out. Forgets the assignment sometimes and does not notice. Reports averages with no group size unless reminded. |
| **3 — Secure** | All four repairs unprompted, `strip` before `title`. Prints shape before and after and can account for the difference. Uses `groupby` and hand-checks one pile. Prints `.size()` beside `.mean()` when reminded once. |
| **4 — Fluent** | Prints `n` beside every average **without being told**. Catches the two-member group and states the consequence in writing. Runs the sizes-sum-to-38 check as a matter of course. Catches a missing assignment alone. |
| **5 — Extending** | Notices that filling six ages inflated the age-13 group and says so unprompted. Argues that `points_per_hour` is a badly designed measure and proposes a better one. Defends a minimum group size and applies it to their own six answers. |

**Where to draw the line:** Level 3 is a pass for Week 24. **Level 4 is the real target of this lab**, and specifically Check 3 — the capstone in Weeks 34–35 is graded largely on whether the student reports group sizes without being asked.

---

## 📤 Homework to Assign

**Say this:**

> "Finish Mess Detective. Same table, same forty rows — you've done most of the repairs, so this is mainly the writing.
>
> Three things I'm marking.
>
> **One: the before and after shape, with the difference accounted for.** Not 'it worked'. `(40, 6)` to `(38, 6)`, and **name the two rows that went.**
>
> **Two: the full cleaning log**, continued on last week's sheet — do not start a new one. This week's first entry is number eight. Every line needs a reason, same as last week.
>
> **Three, and this is the one I'll read first: all six `groupby` answers, each one reported WITH its row count.** An answer without its `n` beside it doesn't count, even if the number is right. And put the sizes-sum-to-38 check in your file so I can see it.
>
> One extra sentence at the bottom: **the one answer out of your six that you would not say out loud in assembly, and why.** There is more than one defensible choice there, and I care about the reason, not which one you pick."

**Workbook pages: 24.1 to 24.10.**

| Page | What it is | Time |
|---|---|---|
| 24.1 | Warm-Up — five vocabulary words matched to five plain definitions | 4 min |
| 24.2 | Predict the Output — six printouts to predict before running | 8 min |
| 24.3 | Practice Set A — Read It — read a `value_counts()` and a `groupby` result | 8 min |
| 24.4 | Practice Set B — Write It — the four repairs, before/after shape | 12 min |
| 24.5 | Fix the Broken Program — four bugs in `detective.py` | 8 min |
| 24.6 | Build It — the six groupby answers, each with its `n` | 12 min |
| 24.7 | The Gold sentence — the trap, written out | 4 min |
| 24.8 | Think Deeper — three written questions | 6 min |
| 24.9 | Draw It — split, apply, combine, with the group sizes on it | 4 min |
| 24.10 | Self-Check — six statements, tick or cross | 4 min |

**Total: about 70 minutes.** If it is running long, cut 24.9 and two questions from 24.6. **Never cut 24.7.**

---

## 🔑 Answer Key

Every line of code below was run on Python 3.10 with pandas 1.5.3, and every output block is copied from the real run.

### The clean starting point

Every page from 24.6 onwards assumes this. It is printed at the top of the workbook.

```python
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.drop_duplicates().reset_index(drop=True)
clean["house"] = clean["house"].str.strip().str.title()
clean["club"] = clean["club"].str.strip().str.lower()
clean["age"] = clean["age"].fillna(13).astype(int)
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)
print(clean.shape)
```

```text
(38, 7)
```

### Page 24.1 — Warm-Up: vocabulary

| Word | Plain definition |
|---|---|
| **duplicate** | A row identical to another row in every single column. |
| **string method** | A command that works on writing — `strip` takes spaces off the ends, `title` fixes the capitals. |
| **derived column** | A new column worked out from columns you already have. |
| **groupby** | Sort the rows into piles by one column, do a calculation on each pile, stack the answers into a small table. |
| **aggregate** | Squash many rows into one number — a mean, a count, a maximum. |

Bonus, and ask for it: **the three words for what `groupby` does** — split, apply, combine.

### Page 24.2 — Predict the Output

| # | The code | The real output | The point |
|---|---|---|---|
| 1 | `print(raw.shape)` | `(40, 6)` | Before anything happens. |
| 2 | `print(raw.duplicated().sum())` | `2` | Two, not four. The **first** copy is not counted as a duplicate. |
| 3 | `print(raw["house"].nunique())` | `14` | Fourteen spellings of four houses. |
| 4 | `print(raw["club"].nunique())` | `8` | Eight spellings of three clubs. |
| 5 | `print(clean["house"].value_counts())` | see below | Four houses, and Gold is 2. |
| 6 | `print(clean.groupby("house")["score"].size().sum())` | `38` | The check that must always pass. |

Item 5:

```text
Blue     14
Red      12
Green    10
Gold      2
Name: house, dtype: int64
```

**Item 2 is the one worth arguing about.** Most students predict 4 because four rows are involved. `duplicated()` marks a row `True` only if an identical row appeared **above** it, so the first Bela Roy is `False` and the second is `True`.

### Page 24.3 — Practice Set A: Read It

Given this printout:

```text
Red       8
Green     5
Blue      5
green     4
blue      4
red       3
BLUE      3
RED       2
blue      1
 Blue     1
GREEN     1
green     1
gold      1
Gold      1
Name: house, dtype: int64
```

1. **"How many lines, and how many houses?"** — 14 lines, 4 houses.
2. **"`blue` appears on two separate lines. How is that possible?"** — they are not the same piece of writing. One has a trailing space. Two pieces of writing are the same only if every character matches, and a space is a character.
3. **"Which lines have an invisible space, and which end is it on?"** — the second `blue` (count 1) has a **trailing** space; ` Blue` has a **leading** space. There is also a second `green` (count 1) with a trailing space, which is easy to miss, and the single `Gold` (count 1) has a trailing space too (so four lines in all).
4. **"Add up every Blue spelling. What should Blue's count be after cleaning?"** — 5 + 4 + 3 + 1 + 1 = **14** ✔. That sum is the proof nothing was lost.
5. **"The counts add to 40, but the clean table has 38 rows. Why?"** — this is the **raw** column, before the two duplicate rows were removed. Neither duplicate was Blue or Gold, so only Red and Green lose one each.
6. **"Given this printout, would `.str.title()` on its own be enough?"** — no. It fixes the capitals and leaves the spaces, so you get **8** distinct values, and the printout looks broken because a space prints as nothing. `strip` first.

Then, given this `groupby` result:

```text
house
Blue     74.36
Gold     95.00
Green    65.20
Red      74.25
Name: score, dtype: float64
```

7. **"What is missing from this table that you would need before believing it?"** — **the group sizes.** Gold's 95.00 comes from 2 rows and Blue's 74.36 from 14, and nothing here says so.
8. **"Why is Gold second in the list when it has the highest average?"** — `groupby` sorts by the **group name**, alphabetically, not by the answer. Blue, Gold, Green, Red.

### Page 24.4 — Practice Set B: the four repairs

Complete working file, run end to end:

```python
# detective.py - Week 24 homework. Four repairs, accounted for.
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.copy()

# ---------- DIAGNOSE (before touching anything)
print("shape           :", raw.shape)
print("duplicate rows  :", raw.duplicated().sum())
print("house spellings :", raw["house"].nunique())
print("club spellings  :", raw["club"].nunique())
print("missing ages    :", raw["age"].isna().sum())

# ---------- REPAIR 1: the duplicates
print("before:", clean.shape)
clean = clean.drop_duplicates()
print("after :", clean.shape)
clean = clean.reset_index(drop=True)

# ---------- REPAIR 2: fourteen house spellings become four
clean["house"] = clean["house"].str.strip().str.title()
print(clean["house"].value_counts())

# ---------- REPAIR 3: eight club spellings become three
clean["club"] = clean["club"].str.strip().str.lower()
print(clean["club"].value_counts())

# ---------- REPAIR 4: the six missing ages
print("median age:", clean["age"].median())
clean["age"] = clean["age"].fillna(13).astype(int)
print(clean.isna().sum())

# ---------- a column that was not there
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)
# hand-check row 0: 72 / 3.5 = 20.571... -> 20.57

print("final shape:", clean.shape)
print(clean.dtypes)
```

Real output:

```text
shape           : (40, 6)
duplicate rows  : 2
house spellings : 14
club spellings  : 8
missing ages    : 6
before: (40, 6)
after : (38, 6)
Blue     14
Red      12
Green    10
Gold      2
Name: house, dtype: int64
chess    14
music    12
art      12
Name: club, dtype: int64
median age: 13.0
name     0
age      0
house    0
club     0
hours    0
score    0
dtype: int64
final shape: (38, 7)
name                object
age                  int64
house               object
club                object
hours              float64
score                int64
points_per_hour    float64
dtype: object
```

**The accounting sentence, which is the graded part:** *"Forty rows in, thirty-eight out. The two that went were the second Bela Roy and the second Farah Aziz, both exact duplicates. Six columns became seven because I added `points_per_hour`. No other row moved."*

### Page 24.5 — Fix the Broken Program

The broken file as printed in the workbook:

```python
# detective.py - four bugs.
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.copy()

clean.drop_duplicates()                                    # BUG 1
clean["house"] = clean["house"].strip().title()            # BUG 2
clean["points_per_hour"] = clean["score"] / clean["hour"]  # BUG 3
print(clean.groupby("house")["score"].mean())              # BUG 4
```

**Bug 1 — the silent one.** No error. `drop_duplicates` returns a new table and nothing catches it, so `clean` still has 40 rows. Fix: `clean = clean.drop_duplicates()`.

**Bug 2.** `AttributeError: 'Series' object has no attribute 'strip'`. A whole column has no `strip` — the `.str` doorway is missing. Fix: `clean["house"].str.strip().str.title()`.

**Bug 3.** `KeyError: 'hour'`. The column is `hours`. Fix: `clean["hours"]`.

**Bug 4 — the one that is not a syntax bug at all.** This line runs perfectly and produces a correct, misleading table: four averages with no group sizes, and a two-member house at the top. Fix:

```python
print(clean.groupby("house").agg(n=("score", "size"), avg=("score", "mean")).round(2))
```

**Give the mark for Bug 4 only if the student says *why*** — that the average hides how many rows it came from. Spotting that a working line is the worst bug in the file is the whole point of this page.

Fixed file output:

```text
        n    avg
house           
Blue   14  74.36
Gold    2  95.00
Green  10  65.20
Red    12  74.25
```

### Page 24.6 — Build It: the six answers, each with its `n`

Complete working file:

```python
# six_questions.py - Week 24 homework. Six answers, every one with its count.
import pandas as pd

raw = pd.read_csv("house_raw.csv")
clean = raw.drop_duplicates().reset_index(drop=True)
clean["house"] = clean["house"].str.strip().str.title()
clean["club"] = clean["club"].str.strip().str.lower()
clean["age"] = clean["age"].fillna(13).astype(int)
clean["points_per_hour"] = (clean["score"] / clean["hours"]).round(2)

print("=== Q1: how many in each house?")
print(clean.groupby("house")["score"].size())
sizes = clean.groupby("house")["score"].size()
print("check: sizes sum to", sizes.sum(), "and the table has", len(clean), "rows")

print("=== Q2: average score per house")
print(clean.groupby("house").agg(n=("score", "size"), avg=("score", "mean")).round(2))

print("=== Q3: average score per club")
print(clean.groupby("club").agg(n=("score", "size"), avg=("score", "mean")).round(2))

print("=== Q4: average score per age")
print(clean.groupby("age").agg(n=("score", "size"), avg=("score", "mean")).round(2))

print("=== Q5: average hours per house")
print(clean.groupby("house").agg(n=("hours", "size"), avg_hours=("hours", "mean")).round(2))

print("=== Q6: most marks per hour of work")
print(clean.sort_values("points_per_hour", ascending=False).head(5)[["name", "house", "score", "hours", "points_per_hour"]])
```

Real output:

```text
=== Q1: how many in each house?
house
Blue     14
Gold      2
Green    10
Red      12
Name: score, dtype: int64
check: sizes sum to 38 and the table has 38 rows
=== Q2: average score per house
        n    avg
house           
Blue   14  74.36
Gold    2  95.00
Green  10  65.20
Red    12  74.25
=== Q3: average score per club
        n    avg
club            
art    12  70.58
chess  14  76.07
music  12  71.83
=== Q4: average score per age
      n    avg
age           
12   10  84.80
13   18  73.11
14   10  61.00
=== Q5: average hours per house
        n  avg_hours
house               
Blue   14       3.18
Gold    2       3.75
Green  10       2.60
Red    12       3.17
=== Q6: most marks per hour of work
           name  house  score  hours  points_per_hour
18    Sami Aden  Green     48    0.5             96.0
7    Hugo Silva    Red     45    0.5             90.0
32   Greta Hahn   Blue     42    0.5             84.0
6    Gita Menon   Blue     78    1.5             52.0
14  Omar Haddad   Blue     52    1.0             52.0
```

**Hand-checks the student should have written down:**

| Group | The arithmetic | Result |
|---|---|---|
| Gold score | 97 + 93 = 190, 190 ÷ 2 | **95.00** ✔ |
| Green score | sum of 48, 50, 54, 59, 61, 63, 67, 70, 85, 95 = 652, 652 ÷ 10 | **65.20** ✔ |
| Blue score | sum = 1041, 1041 ÷ 14 = 74.357… | **74.36** ✔ |
| Red score | sum = 891, 891 ÷ 12 | **74.25** ✔ |
| Sami's rate | 48 ÷ 0.5 | **96.0** ✔ |
| All group sizes | 14 + 12 + 10 + 2 | **38** ✔ |

**Marking notes.** Full marks needs the `n` beside **every** answer, and the sizes-sum check printed at least once. **Q4 needs one extra sentence** to earn full marks: age 13 has eighteen pupils because six missing ages were filled with 13, and six of those eighteen are 13 only because we said so. Before the fill, the twelve pupils with a *known* age of 13 averaged **71.92**; after it, eighteen average **73.11**.

### Page 24.7 — The Gold sentence

> *"Gold has the highest average score (95.00), but it has only ______ members, so ______________________."*

**Model answers, both full marks:**

> *"Gold has the highest average score (95.00), but it has only **2** members, so the number is far too fragile to compare with Blue's, which comes from 14. If one Gold pupil had been off school the average would have been 97 or 93 — from a single row. If one ordinary pupil scoring 73 joined Gold, the average would drop to 87.67 and the lead over Blue would shrink by about a third. Nothing that small could happen to a fourteen-row average, and the plain `.mean()` printout gave me no way to know any of this."*

> *"Gold has the highest average score (95.00), but it has only **2** members, so all it really tells me is that two particular pupils did well. It is not a fact about a house. Blue's 74.36 is a fact about a house, because fourteen different people had to agree to produce it. I should print `.size()` next to `.mean()` so that nobody reads my table the way I read it first."*

**Three real partial answers, and what to say to each:**

| What they wrote | What is missing | Say this |
|---|---|---|
| *"…only 2 members, so it isn't fair."* | The mechanism. Right instinct, no reasoning. | "Not fair **how**? What could happen to two people that couldn't happen to fourteen?" |
| *"…only 2 members, so we need more data."* | True, and it dodges the question. | "You've got the data you've got. What can you honestly say about Gold **today**, in one sentence?" |
| *"…only 2 members, so the average is wrong."* | This one is **wrong** and must be corrected. | "No — the average is exactly right. 97 plus 93 over 2 is 95.00; you checked it yourself. **The number is correct and the conclusion isn't.** That distinction is the whole lesson." |

### Page 24.8 — Think Deeper

**1. "Both duplicate rows had the same name AND the same score. Why does that make you confident it's a mistake rather than two pupils with the same name?"**

Because it is not just the name. **Every single field matches** — name, age, house, club, hours *and* the score to the mark. Two different people called Bela Roy could easily exist, but they would not both be 14, both in Red, both in music club, both have done exactly 5.0 hours, and both score exactly 90. The chance of all six agreeing is negligible; a scrolling slip while typing is common. The strongest answers also notice that **what a row means decides this**: if the table were one row per *test attempt*, two identical rows might be two genuine attempts, and deleting one would be wrong.

**2. "`groupby(...).mean()` gave a correct answer that led you to a wrong conclusion. Is that pandas's fault?"**

No, and this is worth stating plainly. Pandas computed exactly what it was asked: the mean score per house. It has no idea what you intend to *claim*. **The gap is between "a correct number" and "a supported conclusion", and only a person can close it.** A full answer notices that this is why the fix is a habit rather than a command — `.size()` beside `.mean()` does not make pandas smarter, it makes *you* harder to fool. Some students argue that pandas ought to warn you about tiny groups; that is a reasonable design opinion, and the counter-argument is that pandas cannot know what counts as tiny for your question.

**3. "You made `points_per_hour` and it put the three lowest scorers in the school at the top. Is it a good column?"**

Not for the question "who is best". Dividing by 0.5 hours doubles the number, so `points_per_hour` mostly rewards **doing as little work as possible**: Sami Aden scored 48 out of 100 in half an hour and tops the table, while Farah Aziz scored 95 in six hours and is nowhere near it. It is a fine column for a genuinely different question — *"who gets the most out of the time they put in?"* — but it is a bad column for *"who is doing well?"*

Full marks proposes an alternative and defends it. Real answers students give: rank by score and only use hours to break ties; `score - hours * 5` to penalise nothing-doers; or ignore anybody with under one hour as too little to judge. **All are defensible.** The point is that a derived column is a **design decision made by a person**, and that person can be twelve.

### Page 24.9 — Draw It

The student draws split, apply, combine, in three labelled stages.

Required on the drawing:

1. **Split** — four piles, and **the number of rows written on each pile**: Blue 14, Red 12, Green 10, Gold 2. The Gold pile must be visibly the smallest.
2. **Apply** — one machine or arrow per pile, labelled `mean()`.
3. **Combine** — a small four-row table on the right, one row per pile: Blue 74.36, Red 74.25, Green 65.20, Gold 95.00.
4. **The arithmetic somewhere on the page:** 14 + 12 + 10 + 2 = 38, with a note that 38 is the number of rows in the table.

Full marks requires the **group sizes** on the piles and the sum check written out. A drawing with the four averages and no sizes has drawn the trap rather than the lesson — which is a useful thing to say out loud while marking. Compare with Figures 24.4 and 24.5 in this chapter.

### Page 24.10 — Self-Check

| # | Statement | Tick or cross | Why |
|---|---|---|---|
| 1 | "`raw.duplicated().sum()` counts all the copies, so two repeated rows give 4." | ✗ | It gives **2**. The first copy of each row is not marked as a duplicate; only later copies are. |
| 2 | "`df["house"].strip()` removes the spaces from every value in the column." | ✗ | It raises `AttributeError`. You need `.str.strip()` — `.str` is the doorway to doing it to every cell. |
| 3 | "`.str.title()` on its own would have been enough to fix the house column." | ✗ | It leaves the spaces, so you get 8 values instead of 4 — and the printout looks broken because a space prints as nothing. |
| 4 | "`df["new"] = df["a"] / df["b"]` creates a new column." | ✓ | A name on the left that does not exist yet creates a column. If it does exist, it is overwritten, silently. |
| 5 | "If a group has the highest average, it is the best group." | ✗ | Not without its size. Gold's 95.00 comes from two rows; one pupil joining or leaving would move it enormously. |
| 6 | "The group sizes from `groupby` should add up to the number of rows in the table." | ✓ | If they do not, rows have been silently dropped — usually because the grouping column still has holes in it. |

### Answers to every question posed in the lesson

**Hook.** *"How many houses?"* — four, printed as fourteen. *"Why does `blue` appear twice?"* — one copy has a hidden trailing space; ` Blue` has a leading one. *"Is the computer wrong?"* — no, it is being exact, and exactness is what makes it trustworthy. *"What is the evidence?"* — the count, not your eyes.

**Concept.** *"How do you know the Bela Roy rows are a mistake?"* — every field matches, including the exact score. *"Why do we need `strip` as well as `title`?"* — `title` only changes capitals, so the spaces survive and print as nothing; you get 8 values and a printout that looks broken. *"What does a name on the left that doesn't exist do?"* — creates a new column. *"72 in 3.5 hours?"* — 20.57. *"Three steps of groupby?"* — split, apply, combine. *"What will you do every time?"* — hand-check one pile.

**Live-code.** Step 1 → shape still `(40, 6)`, **no error**, because `drop_duplicates` returned a copy; then `(38, 6)`, and the two rows that went were the second Bela Roy and the second Farah Aziz. Step 2 → `title` alone gives **8** values with `Blue` printed three times; `strip` then `title` gives **4**, and 5 + 4 + 3 + 1 + 1 = 14 proves nothing was lost. Clubs: 14 + 12 + 12 = 38. Step 3 → six holes, median **13.0**, filled, zero holes; six pupils are now 13 because we said so. Step 4 → 55 ÷ 2 = **27.5**; shape `(38, 7)`. Step 5 → Gold 97 + 93 = 190, 190 ÷ 2 = **95.00** ✔.

**Activity Part A.** All six outputs are under Page 24.6. Q1 sizes: Blue 14, Gold 2, Green 10, Red 12, summing to 38. Q2 averages: 74.36, 95.00, 65.20, 74.25. Q3: art 70.58 (12), chess 76.07 (14), music 71.83 (12). Q4: 12 → 84.80 (10), 13 → 73.11 (18), 14 → 61.00 (10) — and the 18 is six fills. Q5 hours: Blue 3.18, Gold 3.75, Green 2.60, Red 3.17. Q6: Sami Aden 96.0, Hugo Silva 90.0, Greta Hahn 84.0, then Gita Menon and Omar Haddad tied on 52.0.

*"Is Sami Aden the best pupil in the school?"* — no; he scored 48. *"Is `points_per_hour` a good measure?"* — of "who gets most from their time", maybe; of "who is doing well", no, because dividing by half an hour doubles the number.

**Activity Part B.** Gold's two scores are 97 and 93. One member absent → 97 or 93, from a single row. One average pupil (73) joining → (97 + 93 + 73) ÷ 3 = **87.67**. Model sentences and the three partial answers are under Page 24.7.

**Harder variation.** `groupby(["house", "club"]).size()` gives **9** rows of 12 possible — missing are Red/art, Gold/chess and Gold/music, and pandas lists only what exists rather than showing zeros. The four-statistic `agg` output is in the "harder" section above; Red's best score is 97, equal to Gold's, which is worth pointing at. Grouping by `age` before the fill gives sizes summing to **32**, not 38 — the six pupils with no recorded age have no pile to go in, and nothing warns you.

**Wrap.** *"Which is the best house?"* — Gold by average, and Gold is two people, so the average is not a fact about a house. *"Do the sizes add up?"* — 14 + 12 + 10 + 2 = 38 = `len(clean)` ✔.

---

## 🔮 Next Week Preview

Next week the table stops being a table. **Week 25 is the first chart** — `matplotlib`, one line plotted, axes labelled, title on, saved to a PNG file the student can actually show somebody. And it arrives at exactly the right moment, because this week ended with a printout that was completely correct and completely misleading, and **a chart can do that ten times faster than a table can.** The lesson is deliberately strict about labels: a chart with no title and no axis names is not a chart, it is a decoration, and it will be marked as one. The student will also meet a new flavour of silent failure — code that runs, prints nothing, produces no error, and writes no file, because nobody called `savefig`.

**Prep early:** check `python3 -c "import matplotlib"` prints nothing on the student's machine, **today, not next week** — if matplotlib needs installing, that is a twenty-minute job you do not want to discover at minute three of a lesson. Keep the clean forty-row table and the cleaning log: Week 25 charts this data, and the very first chart the student draws will be the four house averages — at which point the question *"where are the group sizes?"* comes straight back, in a new form.
