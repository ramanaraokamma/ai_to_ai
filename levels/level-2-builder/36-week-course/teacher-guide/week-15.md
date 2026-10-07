# Week 15 — Filter It, Group It, Count It

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Student Guide](../student-guide/week-15.md) · [Workbook](../workbook/week-15.md)

---

## 📋 At a Glance

This table is the whole lesson on one screen: what it is, how long it takes, and what you need.

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — two reusable functions written, then six questions answered with them |
| **Big idea** | Filtering keeps the rows that pass a test; grouping counts how many rows share a value. And **every group answer must be reported with its row count.** |
| **New vocabulary** | filter · group · counting dictionary · key function · row count |
| **New syntax** | `[r for r in rows if r["age"] > 12]` · `sorted(rows, key=...)` · `max(counts, key=counts.get)` |
| **Materials** | The twelve index cards from Week 14 · **four sheets of paper as bucket labels** · a pen · the printed Week 15 workbook (Build It and Draw It are the homework) · the Bug Log · a calculator |
| **Tech needed** | Laptop with Python 3 and the editor. `squad.py` from Week 14 must exist and run. Still nothing installed. |
| **Prep time** | 15 minutes the night before · 5 minutes on the day |

> **⚠️ Watch out:** the punchline of this lab is that **the Owls have exactly one player**, so "the Owls average 104 runs" is really "Priya scored 104" wearing a statistician's hat. Do not fix that, do not mention it early, and do not let the student tidy the data. The whole lesson is aimed at it.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Filter records** with a comprehension and a condition, and **report how many survived** out of how many started.
2. **Count records into a grouping dictionary**, one bucket per value, and check that the bucket counts add up to the number of rows.
3. **Sort a list of records by one field**, using a named key function.
4. **Find the key with the biggest value** in a counting dictionary with `max(counts, key=counts.get)`, and say what happens on a tie.
5. **Report every group answer together with its row count**, and say why a one-row group should probably not be reported as an average at all.

Observable evidence: `records.py` containing `filter_by()` and `group_count()` that take the key as an argument; six printed answers, each with a row count beside it; and a written sentence naming which answer the student trusts least and why.

---

## 🧑‍🏫 What YOU Need to Know First

This section is your background reading. It covers each idea in the order the lesson meets it, with the traps to expect.

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**No Python needed to start.** There are exactly two ideas this week and they are both things you already do with your hands.

### 1. The two questions that cover most of data work

Look at any table for long enough and almost every question you have about it is one of two shapes:

- **"Show me only the rows where ___."** That is **filtering**.
- **"How many rows of each kind are there?"** That is **grouping**.

> **Filter** — keep only the records that pass a test, and throw the rest away. What comes out is still records, with all their labels, just fewer of them.
> **Group** — put every record into a bucket according to the value of one field. Nothing is thrown away; you are only deciding which pile each row belongs to.

The physical versions are a sieve and a laundry pile, and both are worth doing with the cards before any code happens.

**Filtering is a sieve.** You tip the whole pack of twelve cards through, and only the players who scored more than fifty fall out the bottom. Five come out. Seven stay behind. **Five plus seven is twelve**, and if it is not, you dropped a card.

**Grouping is sorting laundry.** You do not throw any socks away. You make a pile per colour and then count each pile. The counting dictionary *is* the set of piles — one key per pile, one number per pile.

![A filter is a sieve](../figures/fig-w15-1-filter-sieve.svg)
*Figure 15.1 — What comes out of a filter is still rows. The counts must add back up to what went in.*

### 2. Filtering, in code, line by line

```python
def filter_by(rows, key, value):
    """Keep only the rows where rows[key] equals value."""
    return [r for r in rows if r[key] == value]
```

That is a Week 14 comprehension with three extra words on the end. Read it in order:

```text
[ r          for r in rows        if r[key] == value ]
  └── 3 ──┘  └──── 1 ────┘        └────── 2 ───────┘

1. for r in rows           ->  go through the records one at a time, calling each one r
2. if r[key] == value      ->  ...but only bother with the ones where this is true
3. r                       ->  ...and for those, put the WHOLE RECORD in the new list
```

Be clear about two things. Students often get both wrong:

- **What goes in the new list is `r` — the whole record**, not one field. Last week the comprehension said `r["runs"]` and gave you a list of numbers. This week it says `r` and gives you a list of records. **Filtering does not change what a row is; it changes how many rows there are.**
- **`==`, not `=`.** One equals sign assigns; two ask a question. The student has known this since Week 5. Getting it wrong here gives `SyntaxError: invalid syntax` with the caret sitting on the `=`.

Why is the key passed in as an argument, rather than written into the function? Because then the same function works on any table you will ever build. `filter_by(squad, "team", "Tigers")` and `filter_by(playlist, "genre", "pop")` are the same function. **That is Week 12's lesson — write the tool, not the one-off — arriving one level up**, and it is worth saying out loud when they type it.

For a filter that is not an exact match — greater than, less than — you write the comprehension directly, because there is no single value to pass:

```python
big_scores = [r for r in squad if r["runs"] > 50]
```

### 3. The counting dictionary — the one pattern to memorise

This is the most reused four lines in this entire course. Learn it well enough to write it from memory, because you will.

Here is the whole function. Each line has a comment saying what it does.

```python
def group_count(rows, key):
    """Count how many rows share each value of key. One bucket per value."""
    counts = {}                                     # no buckets yet
    for r in rows:                                  # look at every row once
        bucket = r[key]                             # which bucket does this row go in?
        counts[bucket] = counts.get(bucket, 0) + 1  # count so far (0 if new), plus one
    return counts
```

Real output on the twelve records:

```text
{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
```

**Unpack the fourth line**, because it does two jobs in one go and it is the only clever thing this week:

```python
counts[bucket] = counts.get(bucket, 0) + 1
#                └──────────┬────────┘
#           "the count so far, or 0 if I have never seen this bucket"
```

Trace it by hand, which is exactly what you should do with the student:

| Turn | record | `bucket` | `counts.get(bucket, 0)` | `counts` afterwards |
|---|---|---|---|---|
| 1 | Asha | `Falcons` | `0` (never seen) | `{'Falcons': 1}` |
| 2 | Ravi | `Falcons` | `1` | `{'Falcons': 2}` |
| 3 | Nita | `Falcons` | `2` | `{'Falcons': 3}` |
| 4 | Sam | `Falcons` | `3` | `{'Falcons': 4}` |
| 5 | Kabir | `Tigers` | `0` (never seen) | `{'Falcons': 4, 'Tigers': 1}` |
| … | … | … | … | … |
| 12 | Priya | `Owls` | `0` (never seen) | `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}` |

**And then the check that matters:** 4 + 4 + 3 + 1 = 12 = `len(squad)`. **If the bucket counts do not add up to the row count, you dropped a row.** Insist on this every single time; it is the cheapest correctness check in the whole course and it catches real damage.

`.get(bucket, 0)` is doing the work here, and it is exactly the tool from Week 13. Without it you need four lines and an `if`:

```python
if bucket in counts:
    counts[bucket] = counts[bucket] + 1
else:
    counts[bucket] = 1
```

Identical result. **This is why `.get()` exists**, and it is a good moment to say so — last week's polite-asking tool turns out to be the thing that makes the most useful pattern in data work fit on one line.

> **Counting dictionary** — a dictionary used as a set of tally marks: one key per bucket, one number per bucket, built with `counts[b] = counts.get(b, 0) + 1`.

![Grouping: one bucket per value](../figures/fig-w15-2-grouping-tally-buckets.svg)
*Figure 15.2 — Nothing is thrown away. The counts must sum to the number of rows.*

### 4. `+=` will bite you, and it is a good bite

The student learned `total += x` in Week 7. It is the natural thing to write here:

```python
counts[bucket] += 1
```

And it fails, immediately, on the very first row. This is the traceback you get:

```text
Traceback (most recent call last):
  File "lab15.py", line 10, in <module>
    print(group_count(squad, "team"))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "records.py", line 19, in group_count
    counts[bucket] += 1
    ~~~~~~^^^^^^^^
KeyError: 'Falcons'
```

Why: `+=` means *take what is there and add one*. On the first Falcon there is nothing there — no key called `Falcons` yet — so Python cannot take what is there. `KeyError`.

**This traceback has two `File` lines, and that is worth ten minutes on its own.** The first says `lab15.py, line 10` — that is *where you called the function from*. The second says `records.py, line 19` — that is *where it actually broke*. Teach the rule:

> **The last `File` line is where it broke. The ones above it are the trail of who called who.** Read the bottom of the traceback, always.

This is the first two-file traceback of the year, and every remaining week will produce them.

### 5. `sorted` with a key function

`sorted()` came in Week 12 and worked on numbers. It cannot sort records on its own — a dictionary is not bigger or smaller than another dictionary — so you have to tell it **which field to look at**. You do that by handing it a function:

```python
def runs_of(player):
    """The key function: given one player, hand back the number to sort on."""
    return player["runs"]

ranked = sorted(squad, key=runs_of, reverse=True)
```

> **Key function** — a small function you hand to `sorted` (or `max`) that takes one item and returns the one value you want it judged on.

Three things to know:

1. **`key=runs_of`, with no brackets after `runs_of`.** You are handing over the function *itself*, not the result of running it. `key=runs_of()` tries to run it with no arguments and gives `TypeError: runs_of() missing 1 required positional argument: 'player'`. The mental model: you are handing `sorted` a *tool*, and `sorted` will use it twelve times. If you use it yourself first you have nothing left to hand over.
2. **`reverse=True` means biggest first.** Without it you get smallest first. Both are keyword arguments from Week 10.
3. **`sorted` moves whole records.** Nita's name, team, runs and balls all travel together. Nothing is separated from its labels — which is exactly what you *lose* when you pull a column out with a comprehension.

![Sorting moves whole rows, not values](../figures/fig-w15-4-sort-by-one-field.svg)
*Figure 15.3 — The key function is how you tell `sorted` which one of the five fields to look at.*

### 6. `max(counts, key=counts.get)` — and the silent wrong answer

You have `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}` and you want the biggest team. The obvious thing is wrong:

```python
print("biggest team (wrong):", max(counts))
print("biggest team (right):", max(counts, key=counts.get))
```

```text
biggest team (wrong): Tigers
biggest team (right): Falcons
```

**Neither of those crashed.** That is the whole point.

`max(counts)` looks at the *keys* — the team names — and returns the one that comes last alphabetically. `Tigers` beats `Owls` beats `Hawks` beats `Falcons` as words, and the counts are never consulted. It is a confident, wrong, silent answer.

`max(counts, key=counts.get)` says: *go through the keys, and for each one, judge it by what `counts.get` says about it.* Now the numbers decide.

**A second thing is hiding here, and you should plan to discuss it.** Falcons and Tigers both have 4. It is a **tie**, and `max` does not tell you. It just returns the first one it met, which is Falcons because Falcons was typed first.

So the honest answer to "which is the biggest team?" is *"Falcons and Tigers, four each"*, and the code as written cannot say that. Do not fix it in code today. **Just make the student notice that the program gave a single answer to a question with two answers.** That is a better lesson than a fix.

(A student who remembers Level 1 may recognise this: it is the same "slippery thing" as a tie in a baseline. Say so if they get there.)

### 7. The sting: an average hides how many rows it came from

Here is the output the whole lab is built to produce. It is the average-per-team output from the six questions in The Activity, In Full:

```text
Q5  average runs per team
    Falcons    35.50 runs   from 4 player(s)
    Tigers     33.50 runs   from 4 player(s)
    Hawks      55.67 runs   from 3 player(s)
    Owls      104.00 runs   from 1 player(s)
```

Read the Owls line. **104.00 runs.** It is the highest average on the board by a mile. It is also just Priya's score, because Priya is the only Owl. Dividing one number by one does not make it an average; it makes it the same number wearing a hat.

> **Row count** — how many records an answer was computed from. An answer without its row count is not an answer.

This is Level 1's *"out of how many?"* arriving with a keyboard attached, and the student will recognise it if you name it. In Level 1 they learned that "60% accurate" means nothing until you know whether that was 6 out of 10 or 600 out of 1000. Same idea, same fix: **print the denominator.**

The decision the student has to make out loud is not "is this number right?" — it is right, 104 divided by 1 is 104. The decision is **"should I report it at all?"** And there are only three defensible answers:

1. **Report it with the count printed loudly.** "Owls: 104.00 from 1 player." Honest, and it lets the reader decide.
2. **Report it with a warning.** "Owls: 104.00 from 1 player — too few rows to call this an average."
3. **Do not report it.** Say "Owls: 1 player, not enough to average" and print nothing else.

All three are professional. What is *not* acceptable is printing `Owls 104.00` next to `Falcons 35.50` with no counts, because a reader will conclude the Owls are three times better at batting, and they will be reasoning correctly from what you showed them.

![An average hides how many rows it came from](../figures/fig-w15-3-average-hides-group-size.svg)
*Figure 15.4 — The tallest bar is one person. Printing the row count is what stops the chart lying.*

**One more rule, and it matters:** decide the minimum group size **before** you look at the answers. If you decide afterwards, you are choosing a rule that happens to exclude the number you did not like, and you will not even notice you are doing it. Three is a reasonable minimum for this dataset. Write it in the code as a named value so it is visible:

```python
MIN_GROUP = 3        # decided BEFORE looking at the answers
```

### 8. The three misconceptions you will actually meet

**Misconception 1 — "filtering deletes the rows."**
It does not touch the original list. `filter_by` **builds a new list** and hands it back; `squad` still has twelve records afterwards. Prove it in one line: print `len(squad)` after every filter and watch it stay at 12. Students who believe filtering is destructive get very nervous about running things twice, and nervous students stop experimenting.

**Misconception 2 — "the group with the biggest average is the best group."**
Not if it has one member. This is the whole lesson and it will not land the first time. The reframe that works: *an average is a summary of several things. If there is only one thing, there is nothing to summarise.*

**Misconception 3 — "`max(counts)` gives the biggest count."**
It gives the biggest **key**, judged as text. It is the most dangerous line in this week's code precisely because it never complains. Show the two lines side by side, once, and make them read both answers out loud.

### 9. How deep to go, and where to stop

**Go this far:** `filter_by` with an exact match; a comprehension with a `>` condition; `group_count`; the sum-check against `len(rows)`; `sorted` with a named key function; `max(counts, key=counts.get)`; averages per group with row counts printed; a minimum group size decided in advance.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| Saving any of this to a CSV file | **Week 16** |
| `lambda` (`key=lambda r: r["runs"]`) | Not in this course. A named function is clearer and does the same job. If a student finds `lambda` online, let them use it and make them explain it. |
| `df.groupby("team")["runs"].mean()` | **Week 24.** It is one line and it does all of today's work, and it also hides the row counts, which is exactly why today comes first. |
| Two-condition filters (`and` inside the comprehension) | Fine as an extension if a fast student wants it — the `and` is Week 6. Do not build the lesson on it. |
| `min()`, `sorted()` on the counting dictionary's `.items()` | Mention only if asked |
| Median instead of mean for a small group | Worth a sentence if a student raises it; the maths belongs to Week 12's toolkit |

The line to hold in your head all lesson: **today is the week the student learns to print the denominator.** Everything else is syntax.

---

### 10. 🧭 The Growing Map — two minutes, and one honest question

The student guide carries one figure that is not about this week's content: the same five-stage pipeline
every week, with one more piece filled in. It is the only place either book shows the learner the
*shape* of the year rather than today's topic.

![The Level 2 pipeline in Week 15: still the dicts, rows and files tile, now filtering and grouping rows](../figures/fig-w15-0-where-this-fits.svg)

*Figure 15.0 — Week 15's version. Third week inside the `dicts · rows · files` tile, weeks 13 to 18.
One thread lit: data.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, then ask a doing question, not a naming one:** *"we are in the same box as last week — so
   what did we do to the rows today?"* You want two verbs: **kept some** and **counted them into
   groups**. If they say "filter and group", make them say what each one does to a row.
2. **Then the better question:** *"what does every answer we wrote today have printed next to it?"* The
   row count. Then point along the dashed stages and say it once: **that habit is the reason the last
   box on this map says *check*.** Sixteen weeks early, and they will meet it again.
3. **Have them write one line on their own copy**, under the gold tile: *filter, group, and always the
   count.* Nothing else changes on their map this week — which is itself worth them seeing.

> **🧑‍🏫 Why this is worth two minutes.** The denominator habit is the single most transferable thing in
> this term, and it is also the easiest to hear as nagging. Putting it on the map makes it structural
> instead of personal: it is not that you keep asking them for row counts, it is that the last stage of
> the year is called PREDICT **& CHECK** and this is where checking starts.

---

## 🧰 Prep Checklist

This checklist gets the room, the files and your own run-through ready before the lesson.

### 15 minutes the night before

- [ ] **Print the whole Week 15 workbook** (Warm-Up through Self-Check; keep the Answers page for yourself).
- [ ] **Find the twelve index cards from Week 14** and check `squad.py` still runs. This lab imports those twelve records; if the file is broken you will lose fifteen minutes.
- [ ] **Write four bucket labels** on four sheets of paper: `Falcons`, `Tigers`, `Hawks`, `Owls`. Lay them face down.
- [ ] **Type and run the code yourself.** Three files this time. Make them in the course folder.

`squad_data.py` — just the twelve records, moved out of last week's file:

```python
"""squad_data.py - the twelve records from Week 14, kept in their own file."""

squad = [
    {"name": "Asha",  "team": "Falcons", "runs": 48,  "balls": 32, "out": True},
    {"name": "Ravi",  "team": "Falcons", "runs": 12,  "balls": 20, "out": True},
    {"name": "Nita",  "team": "Falcons", "runs": 77,  "balls": 55, "out": False},
    {"name": "Sam",   "team": "Falcons", "runs": 5,   "balls": 9,  "out": True},
    {"name": "Kabir", "team": "Tigers",  "runs": 63,  "balls": 41, "out": True},
    {"name": "Meera", "team": "Tigers",  "runs": 30,  "balls": 28, "out": False},
    {"name": "Dev",   "team": "Tigers",  "runs": 0,   "balls": 3,  "out": True},
    {"name": "Zara",  "team": "Tigers",  "runs": 41,  "balls": 39, "out": True},
    {"name": "Iqbal", "team": "Hawks",   "runs": 55,  "balls": 44, "out": True},
    {"name": "Lena",  "team": "Hawks",   "runs": 22,  "balls": 18, "out": True},
    {"name": "Omar",  "team": "Hawks",   "runs": 90,  "balls": 61, "out": False},
    {"name": "Priya", "team": "Owls",    "runs": 104, "balls": 70, "out": False},
]
```

`records.py` — the tools:

```python
"""records.py - tools that work on ANY list of dictionaries, not just cricketers."""

def filter_by(rows, key, value):
    """Keep only the rows where rows[key] equals value."""
    return [r for r in rows if r[key] == value]

def column(rows, key):
    """Pull one column out of the rows as a plain list of values."""
    return [r[key] for r in rows]

def group_count(rows, key):
    """Count how many rows share each value of key. One bucket per value."""
    counts = {}                                     # start with no buckets at all
    for r in rows:                                  # look at every row once
        bucket = r[key]                             # which bucket does this row go in?
        counts[bucket] = counts.get(bucket, 0) + 1  # count so far (0 if new) plus one
    return counts
```

`check.py` — a three-line smoke test:

```python
from records import filter_by, group_count, column
from squad_data import squad

print(len(filter_by(squad, "team", "Tigers")), "Tigers of", len(squad))
print(group_count(squad, "team"))
print(sum(column(squad, "runs")), "runs in total")
```

Run `python3 check.py`. You must see **exactly**:

```text
4 Tigers of 12
{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
547 runs in total
```

- [ ] **Break `group_count` on purpose.** Change the counting line to `counts[bucket] += 1` and run it. You must get a `KeyError: 'Falcons'` **with two `File` lines in it.** Read both. Put it back. This is the planted bug and you must have met it before the student does.
- [ ] **Run the two `max` lines yourself** and see that one says `Tigers` and one says `Falcons`, and that neither complains. This is the moment of the lesson and it is worth thirty seconds of your own surprise.
- [ ] **Read §7 above** (the sting). That is what the lesson is *for*, and you will be improvising around it.

### 5 minutes on the day

- [ ] Editor open with `squad_data.py` and `records.py`; terminal in the same folder.
- [ ] Twelve cards squared up in a pile in the middle of the table. Four bucket labels face down beside them.
- [ ] A calculator on the table. There is real arithmetic today.
- [ ] `check.py` **deleted.** They write the tools.
- [ ] Workbook out, open at Practice Set A (A1–A5 pair with today's lesson); Build It and Draw It held back for the homework.
- [ ] A blank sheet, landscape, for the answers board. You will write six answers on it and every one gets a row count.

### Fallback if the laptop or the install fails

**This lab has an excellent paper version — better than most, because grouping is physically a sorting task.**

1. Sort the twelve cards into four piles by team. Count each pile. Write `4, 4, 3, 1` and check the sum is 12. That is `group_count`, done with hands.
2. Sieve the pile: deal the twelve cards into "more than 50 runs" and "not". Five and seven. Check the sum. That is `filter_by`.
3. With the calculator, total each team's runs and divide by the pile size. Write each answer **with the pile size next to it.** That is objective 5, complete, and it is the objective that matters.
4. When you reach the Owls, stop and have the argument. It works better on paper than on screen, because the pile of one card is visibly a pile of one card.
5. Set the coding as the homework.

| If this fails | Do this instead |
|---|---|
| `squad.py` from Week 14 is missing or broken | Type the twelve records fresh into `squad_data.py`. Six is enough if time is short — but keep Priya, and keep her as the only Owl. |
| `ModuleNotFoundError: No module named 'records'` | The two files are not in the same folder, or the terminal is in the wrong folder. `cd` to the folder holding both, then run. This is Week 12's lesson and it will happen again. |
| They named a file `records.py` and something else broke | `records` is not a standard library name, so this one is safe. `csv.py`, `random.py` and `statistics.py` are not. Standing rule all year: never name a file after a library. |
| Averages come out as whole numbers with no decimals | `sum(runs) / len(runs)` always gives a decimal in Python 3. If they see `35` not `35.5` they have used `//` (Week 3's floor division) instead of `/`. |
| `ZeroDivisionError` on a group that does not exist | Correct behaviour, and a good moment. See the Debugging Clinic — the fix is to check `len(rows)` before dividing, which is the same discipline as printing the row count. |

---

## ⏱️ The Lesson, Minute by Minute

This section is your script for the whole lesson. The table is the overview. The segments below it give the words to say and the steps to follow.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Sort the Pile By Hand | 7 | 7 | Twelve cards into four piles. Count them. 4+4+3+1=12. |
| 🧠 Concept — Sieve and Buckets | 16 | 23 | Filter vs group; the counting-dictionary line traced by hand |
| 💻 Live-Code Together — `records.py` | 18 | 41 | They type both tools. Two deliberate mistakes: one crash, one silent |
| 🎲 Their Turn — Six Questions, Six Row Counts | 20 | 61 | The six answers, and the argument about the Owls |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Sort the Pile By Hand (7 minutes)

**Do this:** Twelve cards in a squared-up pile in the middle of the table. Four bucket labels still face down. Say nothing about code.

**Say this:**

> "Twelve cards. Twelve players. Here's a question somebody actually asks about a cricket squad: **which team has the most players in it?**
>
> Don't look through the pile and count in your head. **Do it with your hands.** Show me how you'd work it out."

Let them do it. Almost every student will start dealing the cards into piles. The moment they do:

> "Stop — say what you're doing out loud."

*"I'm making a pile for each team."*

> "Right. That's the entire idea of today and you just invented it without being told. Carry on."

**Do this:** Turn the four bucket labels over and slide them under the piles as they form. Let them finish dealing.

> "Now count each pile and say the numbers."

*Falcons 4. Tigers 4. Hawks 3. Owls 1.*

**Do this:** Write on the board: `4 + 4 + 3 + 1 = 12`.

> "Add them up. Twelve. And how many cards did we start with? Twelve.
>
> **Hold on to that check**, because it is the cheapest way there is to know you have not made a mistake. If the piles add up to twelve, no card fell on the floor. If they add up to eleven, one did, and you'd never notice it any other way."

> "Now the other kind of question. **Show me only the players who scored more than fifty.** Hands again."

They deal the twelve into two piles: yes and no. Five and seven.

> "Five out. And how many stayed? Seven. Five plus seven?"

*Twelve.*

> "Same check. Now — look at the five cards that came out. Are they still cards?"

*Yes.*

> "Do they still have all five labels on them?"

*Yes.*

> "That's important. **The sieve didn't turn them into anything else.** It didn't rub the names off. Five cards came out, exactly the same shape as the twelve that went in, just fewer of them.
>
> Those two things you just did with your hands have names. Making piles by team is **grouping**. Tipping the pack through a test is **filtering**. Today you write both of them as functions that work on any table, and then you use them to answer six questions — and there's a trap in one of the six that I'm not going to warn you about."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which team has the most players?" | Falcons and Tigers, four each. | **If they name only one, do not correct it yet.** Note it. It comes back in the live-code, where the program will make the same mistake. |
| "The piles add up to twelve. Why do I care?" | Because if they didn't, a card went missing. | If they shrug, take one card off the table when they are not looking and have them recount. That lands. |
| "Are the five filtered cards still cards?" | Yes, with all their labels. | If they say "they're just the runs now", hold one up and read the team off it. |
| "Which of the four piles do you trust least, and why?" | The Owls — there's only one card in it. | This is the whole lesson and if they get it in the Hook, brilliant. Say "remember that" and move on. Do not spend it now. |

---

### 🧠 Concept — Sieve and Buckets (16 minutes)

**Do this:** Leave the four piles on the table. Write on the board as you go.

**Say this — part 1, the two words and the two shapes:**

> "Two definitions and then the only clever line of the day."

Write them up and leave them:

> **filter** — keep only the rows that pass a test. Fewer rows, same shape.
> **group** — put every row in a bucket by the value of one field. Same rows, sorted into piles.

> "The difference matters. **A filter throws rows away. Grouping throws nothing away** — every card is still on the table, it's just in a pile. That's why the piles add up to twelve and the sieve gives you five and seven."

**Say this — part 2, the filter in code:**

> "The filter is last week's one-liner with three words bolted on. You already know most of it."

Write it out, saying each part:

```python
[r for r in rows if r[key] == value]
```

> "Read it in order. `for r in rows` — go through the records one at a time. `if r[key] == value` — but only bother with the ones where this is true. And the `r` at the front — for those, put **the whole record** in the new list.
>
> Compare that to last week. Last week the front said `r["runs"]` and you got twelve *numbers*. This week the front says `r` and you get five *records*. **Filtering doesn't change what a row is. It changes how many rows there are.**
>
> And two equals signs, not one. One equals sign means 'make this box hold that'. Two means 'is this the same as that?'. You've known that since Week 5 and you will still get it wrong once today."

**Say this — part 3, the counting dictionary, traced by hand:**

> "Now the buckets. And this is genuinely the most useful four lines in this whole course — you will type them for the rest of your life. Here they are."

```python
counts = {}                                     # no buckets yet
for r in rows:                                  # every row, once
    bucket = r[key]                             # which bucket?
    counts[bucket] = counts.get(bucket, 0) + 1  # count so far (0 if new), plus one
```

> "The last line does two jobs at once, so let's do it by hand. Get your pencil. I'll read the cards, you keep the dictionary."

**Do this:** Genuinely trace it, out loud, with the student writing the dictionary after each card. Do at least the first five. Do not skip this; it is the difference between typing the line and understanding it.

| Turn | card | `bucket` | `counts.get(bucket, 0)` | write this |
|---|---|---|---|---|
| 1 | Asha | Falcons | 0 — never seen it | `{'Falcons': 1}` |
| 2 | Ravi | Falcons | 1 | `{'Falcons': 2}` |
| 3 | Nita | Falcons | 2 | `{'Falcons': 3}` |
| 4 | Sam | Falcons | 3 | `{'Falcons': 4}` |
| 5 | Kabir | Tigers | 0 — never seen it | `{'Falcons': 4, 'Tigers': 1}` |

> "See what `.get` is for. **The first time you meet a bucket, there's nothing there, so `.get` hands you a zero and you write one.** Every time after that it hands you the count so far and you write one more. That's the whole trick, and it's the tool you learned last week doing the one job it was made for."

Finish the trace, or jump to the end:

```text
{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
```

> "Four plus four plus three plus one. Twelve. **Every single time you group anything, add the buckets up and check.** It costs one line and it catches the worst kind of mistake there is — the one where the answer looks fine."

**Say this — part 4, the row count:**

> "Last thing before we type, and it's the thing I actually want you to take out of the door.
>
> Look at the Owls pile. One card. Priya. Now — what's the Owls' average score?"

*104.*

> "Is that right?"

*Yes… ?*

> "It is. 104 divided by 1 is 104, and there's nothing wrong with the arithmetic. So here's the real question: **if I write '104' on the board next to the Falcons' 35.5, what will somebody reading the board believe?**"

Let them get there. That the Owls are much better.

> "And are they?"

*You can't tell. There's one of them.*

> "That's it. That's today. **An average with no row count next to it isn't an answer, it's a shape.** You met this in Level 1 and it was three words long: *out of how many?* Same idea, and today you'll be typing the denominator yourself."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "In `[r for r in rows if ...]`, what ends up in the new list?" | The whole record. | If they say "the runs", point at last week's comprehension and put the two side by side. The difference is one word at the front. |
| "First time we meet Hawks, what does `counts.get("Hawks", 0)` give?" | 0. | If they say "nothing" or "an error", that is the right instinct for `counts["Hawks"]` — and it is exactly why we use `.get`. |
| "Why check that the buckets add up to twelve?" | Because if they don't, a row went missing. | If they say "to be sure", push once: "sure of *what*, exactly?" |
| "The Owls average 104. Is the number wrong?" | No — the number is right. Reporting it without the count is what's wrong. | This distinction is subtle and worth insisting on. The arithmetic is not the problem. |
| "What's the smallest pile you'd be willing to call an average?" | Any argued answer. Three is sensible. | Whatever they say, write it on the board **now, before the answers appear.** Then say why that mattered. |

---

### 💻 Live-Code Together — `records.py` (18 minutes)

**You never touch the keyboard.** Predictions before every run.

**Step 1 (3 min).** Move the data into its own file. New file `squad_data.py`, and copy last week's twelve records into it — a copy-paste is entirely fine here; the typing was last week's lesson.

> **Say this:** "Two files, like Week 12. The data lives in one, the tools live in another, and the questions live in a third. That way when your tools are right, they stay right, and you can point them at somebody else's data tomorrow."

**Step 2 (4 min).** New file `records.py`. Dictate:

```python
"""records.py - tools that work on ANY list of dictionaries, not just cricketers."""

def filter_by(rows, key, value):
    """Keep only the rows where rows[key] equals value."""
    return [r for r in rows if r[key] == value]

def column(rows, key):
    """Pull one column out of the rows as a plain list of values."""
    return [r[key] for r in rows]
```

Then make a new file, `lab15.py`, that uses the tools:

```python
"""lab15.py - asking the twelve records six questions."""

from records import filter_by, column
from squad_data import squad

tigers = filter_by(squad, "team", "Tigers")
print("Tigers rows:", len(tigers), "of", len(squad))
print("Tigers     :", column(tigers, "name"))
```

**Ask before running:** "Two lines out. How many Tigers, and who?"

Run it. Here is the real output:

```text
Tigers rows: 4 of 12
Tigers     : ['Kabir', 'Meera', 'Dev', 'Zara']
```

> **Say this:** "Note what I printed. Not just '4' — **'4 of 12'.** Get in that habit now, on the easy one, and you will still have it in Week 34 when it matters.
>
> And notice the function doesn't know the word 'cricket' anywhere. `filter_by(playlist, "genre", "pop")` would work, and so would `filter_by(dinners, "day", "Tuesday")`. **You wrote a tool, not an answer.**"

**Step 3 — ⚠️ FIRST DELIBERATE MISTAKE (5 min).** Planned. This one is the natural mistake and you should let them make it themselves.

> **Say this:** "Now the buckets. Add `group_count` to `records.py`. You want to add one to a bucket each time — and you already know how to add one to something, from Week 7. Use that."

Almost every student writes:

```python
def group_count(rows, key):
    """Count how many rows share each value of key. One bucket per value."""
    counts = {}
    for r in rows:
        bucket = r[key]
        counts[bucket] += 1
    return counts
```

Add the call in `lab15.py`. **Two edits, and the first one is easy to forget:** put `group_count` on the import line as well, or you will get `NameError: name 'group_count' is not defined` instead of the error we are here for.

```python
from records import filter_by, column, group_count      # <-- group_count added
```

Then, at the bottom of the file:

```python
print(group_count(squad, "team"))
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "lab15.py", line 10, in <module>
    print(group_count(squad, "team"))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "records.py", line 19, in group_count
    counts[bucket] += 1
    ~~~~~~^^^^^^^^
KeyError: 'Falcons'
```

> **Say this:** "Oh good — and this one's new, look at it. **Two `File` lines.** You've only ever had one before.
>
> Read them from the bottom. `records.py, line 19` — that's where it actually broke. And the one above it, `lab15.py, line 10`, tells you *who called it*. So the trail reads: 'line 10 of lab15 called `group_count`, and inside `group_count`, line 19 of records blew up.'
>
> **Rule for the rest of the year: the LAST File line is where it broke.** Everything above is the trail of who called who.
>
> Now the last line. `KeyError: 'Falcons'`. What does `+=` actually mean?"

*Take what's there and add one.*

> "Right. And on the very first Falcon, what's there?"

*Nothing.*

> "Nothing at all — there's no key called Falcons yet. So Python can't take what's there, and it says so. `KeyError`.
>
> Which is exactly why the line is written the way I showed you. `counts.get(bucket, 0)` means *the count so far, or nought if I've never seen this one.* Change it."

```python
        counts[bucket] = counts.get(bucket, 0) + 1  # count so far (0 if new) plus one
```

Run it. Real output:

```text
Tigers rows: 4 of 12
Tigers     : ['Kabir', 'Meera', 'Dev', 'Zara']
{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
```

Bug Log it now, and log the **two-File-line rule** as a separate entry. That rule is worth more than the fix.

**Step 4 — ⚠️ SECOND DELIBERATE MISTAKE (4 min).** This one does not crash. That is the point, and you must let them believe the wrong answer for about twenty seconds before the second line runs.

> **Say this:** "Now — which team is biggest? There's a thing called `max` that gives you the biggest of something. Try it on the counts."

```python
counts = group_count(squad, "team")
print("biggest team (wrong):", max(counts))
print("biggest team (right):", max(counts, key=counts.get))
```

Have them type only the first `print` and run it.

```text
biggest team (wrong): Tigers
```

> **Say this:** "Tigers. Does that look right?"

Let them agree. Some will. Then:

> "Look back at the counts. Falcons 4, Tigers 4, Hawks 3, Owls 1. **Tigers is not the biggest.** It's tied at the top, but it isn't the biggest, and something worse than that is going on.
>
> There was no error. Nothing complained. Python did exactly what you asked, which was not what you meant. `max` looked at the **team names** — the keys — and gave you the one that comes last in the alphabet. F, then H, then O, then T. Tigers wins as a *word*. **It never looked at the numbers at all.**"

Now the second line.

```text
biggest team (right): Falcons
```

> "`key=counts.get` says: 'go through the team names, and judge each one by what `counts.get` says about it.' Now the numbers decide.
>
> And **look what it did with the tie.** Falcons and Tigers both have four. `max` gave one answer to a question with two answers, and it gave the one that happened to be typed first. It didn't lie to you — it just can't say 'they're tied' because you never asked it to. What's the honest answer to 'which team is biggest'?"

*Falcons and Tigers, four each.*

> "Which your program cannot say. That's fine. **You** can say it, and that's why a human writes the sentence at the end."

Bug Log this one too, under a heading of its own: **a wrong answer with no error message.**

**Step 5 (2 min).** The key function and the ranking.

```python
def runs_of(player):
    """Key function: given one player, hand back the number to sort on."""
    return player["runs"]

ranked = sorted(squad, key=runs_of, reverse=True)
for position, player in enumerate(ranked[:3], start=1):
    print(f"{position}. {player['name']:<7}{player['runs']:>4} runs")
```

Real output:

```text
1. Priya   104 runs
2. Omar     90 runs
3. Nita     77 runs
```

> **Say this:** "Two things. First: **`key=runs_of`, with no brackets.** You're handing `sorted` the tool, not the result of using it. If you write `runs_of()` you try to use it yourself, with nothing to use it on, and Python says *missing 1 required positional argument*.
>
> Second: look what `sorted` moved. **Whole records.** Priya's name and her 104 travelled together, and so did her team and her balls. Nothing got separated from its labels — which is exactly what you *do* lose when you pull a column out with a comprehension."

---

### 🎲 Their Turn — Six Questions, Six Row Counts (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–12:** the six questions, answered in code, each with its row count.
- **Minutes 12–17:** the Owls argument, out loud, and the decision written down.
- **Minutes 17–20:** add the `MIN_GROUP` guard and re-run.

---

## 🎲 The Activity, In Full

This section gives the full setup, the rules and the code for the six-question lab.

### Setup

**On the table:** the four card piles from the Hook, still in their piles. The four bucket labels. A calculator. Workbook Practice Set A, A5 (the trace), for reference. The blank landscape answers sheet.

**On the answers sheet, before anything else:** write the minimum group size the student chose in the Concept segment, in a box, at the top. `MIN_GROUP = 3` or whatever they said. **It has to be up there before the answers appear.**

### The rules

1. **Every answer is written with its row count.** No exceptions, including the easy ones. `5 of 12`, not `5`.
2. **After every `group_count`, add the buckets up** and check against `len(rows)`.
3. **The minimum group size was decided first** and does not move once the answers are visible.
4. **No answer gets a verdict before it gets a number.** If they say "the Owls are best" before computing it, say: "Might be. Count it."

### The six questions

Here is the complete `lab15.py`. Add the new code to the file you already have.

```python
"""lab15.py - six questions about twelve players, every answer with its row count."""

from records import filter_by, group_count, column
from squad_data import squad

def runs_of(player):
    """The key function: given one player, hand back the number to sort on."""
    return player["runs"]

print("=" * 46)
print(f"{len(squad)} rows, {len(squad[0])} columns")
print("=" * 46)

# --- Q1: how many players in each team? -------------------------------------
team_counts = group_count(squad, "team")
print("\nQ1  players per team")
print("   ", team_counts)
print("    rows accounted for:", sum(team_counts.values()), "of", len(squad))

# --- Q2: which team has the most players? -----------------------------------
biggest = max(team_counts, key=team_counts.get)
print("\nQ2  biggest team")
print(f"    {biggest}, with {team_counts[biggest]} players")

# --- Q3: who scored more than 50? -------------------------------------------
big_scores = [r for r in squad if r["runs"] > 50]
print("\nQ3  players who scored more than 50")
print("   ", column(big_scores, "name"))
print(f"    {len(big_scores)} of {len(squad)} players")

# --- Q4: what did the Falcons average? --------------------------------------
falcons = filter_by(squad, "team", "Falcons")
falcon_runs = column(falcons, "runs")
print("\nQ4  Falcons average")
print("    runs:", falcon_runs)
print(f"    average {sum(falcon_runs) / len(falcon_runs):.2f} runs  (from {len(falcons)} players)")

# --- Q5: average runs per team, EVERY answer with its row count -------------
print("\nQ5  average runs per team")
for team in team_counts:
    team_rows = filter_by(squad, "team", team)
    team_runs = column(team_rows, "runs")
    average = sum(team_runs) / len(team_runs)
    print(f"    {team:<8} {average:7.2f} runs   from {len(team_rows)} player(s)")

# --- Q6: the top three scorers ----------------------------------------------
ranked = sorted(squad, key=runs_of, reverse=True)
print("\nQ6  top three scorers")
for position, player in enumerate(ranked[:3], start=1):
    print(f"    {position}. {player['name']:<7}{player['runs']:>4} runs")
```

Real output:

```text
==============================================
12 rows, 5 columns
==============================================

Q1  players per team
    {'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
    rows accounted for: 12 of 12

Q2  biggest team
    Falcons, with 4 players

Q3  players who scored more than 50
    ['Nita', 'Kabir', 'Iqbal', 'Omar', 'Priya']
    5 of 12 players

Q4  Falcons average
    runs: [48, 12, 77, 5]
    average 35.50 runs  (from 4 players)

Q5  average runs per team
    Falcons    35.50 runs   from 4 player(s)
    Tigers     33.50 runs   from 4 player(s)
    Hawks      55.67 runs   from 3 player(s)
    Owls      104.00 runs   from 1 player(s)

Q6  top three scorers
    1. Priya   104 runs
    2. Omar     90 runs
    3. Nita     77 runs
```

**Hand-check one answer with the calculator, on paper, in front of them.** Q4 is the right one:

```text
48 + 12 = 60
60 + 77 = 137
137 + 5 = 142
142 / 4 = 35.5
```

Matched. Say why you did it: *"now you know what the right answer looks like, so if the code ever disagrees with you, one of you is wrong and you'll know to check."*

### The argument (5 minutes, and it is the point of the lab)

**Do this:** Point at the Q5 output. Say nothing for a moment. Let them read it.

**Say this:**

> "Read me the four averages."

*35.5, 33.5, 55.67, 104.*

> "So which team is the best at batting?"

Most students say the Owls. Let them.

> "Right. Now read me the row counts."

*4, 4, 3, and… one.*

> "One. So say the Owls line out loud again, but say the whole thing."

*"The Owls average 104 runs, from one player."*

> "And what does 104 divided by 1 actually mean?"

*It's just Priya's score.*

> "It's just Priya's score. Dividing a number by one doesn't turn it into an average — it turns it into the same number with a hat on.
>
> So here's your decision, and it is a real decision that grown-ups get paid to make: **do you report it?** You've got three choices and all three are defensible. Print it with the count next to it, and let the reader work it out. Print it with a warning on it. Or don't print it at all and just say 'one player, not enough'.
>
> What's not allowed is printing `Owls 104.00` next to `Falcons 35.50` with nothing else, because anybody reading that will conclude the Owls are three times better, and they'll be reasoning perfectly correctly from what you showed them. **You'd have misled them without writing a single false number.**
>
> Which do you choose? And why?"

**Take whatever they choose.** Write it on the answers sheet as a sentence in their own words. Then point at the `MIN_GROUP = 3` box you wrote before the answers appeared:

> "And notice we picked three *before* we saw that the Owls had one. If we'd picked it afterwards, we'd have been choosing a rule that happens to get rid of the number we didn't like. That's a real trap and it has caught much cleverer people than us."

### The guard (3 minutes)

Add the guard to the bottom of `lab15.py`, or make it a separate `honest.py`. This version is the separate file:

```python
"""honest.py - the same averages, but the small groups say so out loud."""

from records import filter_by, group_count, column
from squad_data import squad

MIN_GROUP = 3        # decided BEFORE looking at the answers

team_counts = group_count(squad, "team")

print("average runs per team")
print("-" * 52)
for team in team_counts:
    rows = filter_by(squad, "team", team)
    runs = column(rows, "runs")
    average = sum(runs) / len(runs)
    if len(rows) < MIN_GROUP:
        print(f"{team:<8} {average:7.2f}   from {len(rows)} row(s)  <-- too few rows to call this an average")
    else:
        print(f"{team:<8} {average:7.2f}   from {len(rows)} row(s)")
print("-" * 52)
print(f"minimum group size we agreed on: {MIN_GROUP}")
```

Run it. Here is the real output:

```text
average runs per team
----------------------------------------------------
Falcons    35.50   from 4 row(s)
Tigers     33.50   from 4 row(s)
Hawks      55.67   from 3 row(s)
Owls      104.00   from 1 row(s)  <-- too few rows to call this an average
----------------------------------------------------
minimum group size we agreed on: 3
```

> **Say this:** "That's a program that tells the truth about itself. Notice it still prints the number — it doesn't hide anything. It just refuses to let you read it without knowing what it is."

### What "finished" looks like

- `records.py` holds `filter_by`, `group_count` and `column`, and **none of them mention cricket**.
- Six answers printed, **every one with a row count**.
- `sum(team_counts.values())` printed and equal to 12.
- One answer hand-checked on paper and matched.
- A written sentence saying which answer the student trusts least, and why.
- `MIN_GROUP` in the code as a named value, chosen before the answers appeared.

### Variation — easier

- **Three questions, not six.** Q1 (counts), Q3 (a filter with a count), Q5 (averages with row counts). Q5 is the one you may never cut.
- **Skip `sorted` and the key function entirely.** It is the least load-bearing tool this week and Q6 can be answered by reading the table.
- **Give them `group_count` finished** and have them only *use* it. The trace-by-hand in the Concept segment is where the understanding lives, not in the typing.
- **Do all the arithmetic on the calculator, on paper, from the card piles**, and use the code only to check. That is a completely legitimate version of this lab and it delivers objectives 1, 2 and 5.
- **Six records instead of twelve.** Keep Priya as the only Owl.

### Variation — harder

1. **`group_sum` and `group_average`.** Write `group_sum(rows, group_key, value_key)` using the same counting-dictionary shape, then build `group_average` **out of `group_sum` and `group_count`** without rewriting the loop. Then the question: "if you later fix a bug in `group_count`, what happens to `group_average`?" *(It gets fixed for free. That is the argument for building tools out of tools.)*
2. **Report the tie honestly.** "Q2 said Falcons. The truth is Falcons and Tigers. Make the program say the true thing." *(Find the biggest count first, then keep every key whose count equals it. Two lines, no new syntax.)*
3. **A two-condition filter.** `[r for r in squad if r["team"] == "Falcons" and r["runs"] > 20]` — the `and` is from Week 6. Then: "how many rows, and is that enough to average?" *(Two rows. It is not.)*
4. **The real zero versus the missing zero.** Dev scored 0 — a measured zero, off three balls. "If somebody's card had *no* runs field and you filled it with `.get("runs", 0)`, could you tell them apart afterwards? What would you do instead?" This is Week 13's honesty question with real teeth, and the answer is genuinely hard: once the zero is written down, you cannot.
5. **Group by something you invent.** Add a computed field first — `player["fifty"] = player["runs"] >= 50` — then `group_count(squad, "fifty")`. *(`{False: 7, True: 5}` — and it agrees with the Q3 filter, which is a free cross-check. Point that out; two routes to the same number is how you know both are right.)*
6. **Break the sum check on purpose.** Give them a `group_count` with `return counts` accidentally inside the loop and ask them to find it using only the sum check. *(The counts add up to 1, not 12.)*

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `KeyError: 'Falcons'` with **two** `File` lines | "There's nothing in the Falcons bucket yet, so I can't add one to it." | `counts[bucket] += 1`. `+=` needs the key to already exist. | `counts[bucket] = counts.get(bucket, 0) + 1`. And read the **last** `File` line — that is where it broke. |
| `ZeroDivisionError: division by zero` | "You divided by nought." | A filter matched no rows, so `len(rows)` is 0, and `sum(runs) / len(runs)` has nothing to divide by. | Print `len(rows)` **before** you divide, and don't divide if it is 0. Which is the same discipline as printing the row count. |
| `TypeError: runs_of() missing 1 required positional argument: 'player'` | "You tried to use the key function yourself, with nothing to use it on." | `key=runs_of()` — brackets. | `key=runs_of`, no brackets. You are handing over the tool, not the result. |
| `TypeError: get expected at least 1 argument, got 0` | Same mistake, on `max`. | `key=counts.get()` — brackets. | `key=counts.get`, no brackets. |
| `TypeError: 'str' object is not callable` | "You gave me text where a function belongs." | `sorted(squad, key="runs")`. `key=` needs a function, not a field name. | Write a named key function that returns `player["runs"]` and pass that. |
| `TypeError: unsupported operand type(s) for +: 'int' and 'dict'` | "You tried to add a dictionary to a number." | `sum(squad)` — totalling the *records* instead of a column. | Pull the column out first: `sum(column(squad, "runs"))`. |
| `SyntaxError: invalid syntax` with the caret on an `=` | Python could not read the condition. | One equals sign in a test: `if r["team"] = "Tigers"`. | Two: `==`. One assigns, two ask. |
| `KeyError: 'team'` from inside `group_count` | Row *n* has no key called `team`. | One record was typed with `Team`, or is missing the field. | Fix the record. Or `r.get(key, "MISSING")` if holes are expected — and then the `MISSING` bucket tells you how many. |
| `ModuleNotFoundError: No module named 'records'` | "I can't find a file called `records.py`." | The terminal is in a different folder from the files, or the file is misnamed. | `cd` to the folder holding both files. Check the spelling. Week 12's lesson, again. |
| **No error, `max(counts)` says `Tigers`** | Nothing is wrong as far as Python is concerned. | `max` without `key=` compares the **keys as text** and never looks at the counts. | `max(counts, key=counts.get)`. And check the answer against the printed counts by eye, every time. |
| **No error, five buckets where you expected four (the buckets still add up to 12)** | Nothing is wrong as far as Python is concerned. | A row has a stray space or a different capital in the group field — `"Tigers "` and `"Tigers"` are two different buckets. | `print(counts)` and read the keys. Two nearly-identical keys is the tell. (Cleaning this properly is Week 24.) |
| **No error, an average of 104.00 from one row** | Nothing is wrong as far as Python is concerned. | Nothing. The arithmetic is correct. **This is the dangerous one.** | Print the row count beside every average, and set a minimum group size before you look at the answers. |

### How to teach debugging without giving the answer

The four moves stand — read the last line, find the line number, say the complaint in your own words, then compare characters. This week adds two:

5. **"Which `File` line is the last one?"** That is where it broke. With two files in play, students read the first `File` line, go to `lab15.py`, find nothing wrong, and get stuck for five minutes. One question fixes it forever.
6. **"Do the buckets add up?"** This is the move for a dropped row, which produces no message (for example a `return` indented inside the loop, so the counts add up to 1, not 12). It does **not** catch the three silent rows in the table above — `max(counts)`, the stray-space bucket and the one-row average all still add up to 12. For those the moves are "count the buckets and compare with what you expected" and "read the row count beside the answer".

And the sentence for this week, which is the harder half of debugging:

> **"Half the mistakes this week don't produce an error message. `max(counts)` gives a wrong answer politely, and an average of one row is arithmetically perfect. The check is not 'did it run?' — it is 'does this answer make sense next to its row count?'"**

---

## ❓ Questions Students Ask This Week

These are the questions students usually ask, with answers you can give in your own words.

**"Does filtering delete the rows from the original table?"**

No. `filter_by` builds a **new** list and hands it back; `squad` still has all twelve records afterwards. Prove it in one line — print `len(squad)` after the filter and watch it stay at 12. This matters more than it sounds: students who think filtering is destructive become afraid to run things twice, and a student who is afraid to experiment stops learning.

**"Why write `filter_by` at all? The comprehension is one line already."**

Two reasons and the second is the real one. The small reason: `filter_by(squad, "team", "Tigers")` reads like the question you asked, and `[r for r in squad if r["team"] == "Tigers"]` reads like machinery. The real reason: **the function is now a thing you own.** Point it at a playlist, at a set of bus journeys, at somebody else's table, and it works — and if you find a bug in it, you fix it once and everything that uses it gets better. That is Week 12's argument, and it is the difference between having written some code and having built a tool.

**"Why does `max(counts)` give the wrong answer instead of an error?"**

Because it is not a wrong answer to the question Python was asked. `max` on a dictionary compares the **keys**, and comparing text is a perfectly legal thing to do — `"Tigers"` really does come after `"Falcons"` alphabetically. Python has no way to know you meant the counts. This is the single most important shape of bug in data work: **the program did exactly what you said, and what you said was not what you meant.** No error message will ever save you from that; only checking the answer against something you already know will.

**"What if two groups tie?"**

`max` returns the first one it met, and says nothing about the tie. In our data Falcons and Tigers both have four, and `max(counts, key=counts.get)` says `Falcons` purely because Falcons was typed first. That is not a lie, but it is not the whole truth either, and the honest answer to "which team is biggest?" is "two of them, four each". Fixing that in code is a fine extension: find the biggest count, then keep every key whose count equals it.

**"Is a zero in the data the same as a missing value?"**

**No, and this is one of the most important distinctions in the whole course.** Dev scored 0 runs off 3 balls. That is a *measurement*: somebody watched, he was dismissed without scoring, and the zero is a fact. A player whose card has no `runs` field at all is a *hole*: nobody knows what they scored. Both look like `0` in a column of numbers, and once you have filled the hole with a zero you can never tell them apart again. Which is why last week's rule stands: a fallback is fine when it is a fact and a lie when it is a guess. If you must fill holes, count how many you filled and say so.

**"Should I use the median instead of the mean for a small group?"**

It helps with a different problem, not this one. The median (the middle value, from your Week 12 toolkit) is more robust when one enormous value drags the average around — the Falcons' 35.5 is pulled up by Nita's 77, and their median of 30 (the middle of 5, 12, 48, 77 is (12 + 48) / 2) is arguably more representative. But **no summary statistic can rescue a group of one.** The median of a single value is that value, exactly like the mean. The problem is not which average you chose; it is that there is nothing to average.

**"How many rows do you need before an average means anything?"** *(Nobody fully agrees, and here is why.)*

**There is no number, and anybody who gives you one without asking questions first is guessing.**

It is worth being straight with a 12-year-old about this. The temptation is to invent a rule and pretend it is a fact.

What everyone agrees on: **one row is not an average**, and it should never be printed next to real averages without a warning. Two is barely better.

Beyond that, the honest answer is *it depends*, on three things:


*How spread out the values are.* If every Falcon scores between 34 and 36, then three of them tell you a great deal. If they score 5, 12, 48 and 77, then four of them barely tell you anything, because the next Falcon could be anywhere. **Spread matters as much as count in deciding how much you know** — and measuring spread properly is Week 26 and 27.

*What the answer will be used for.* An average used to decide which snack to buy for a party can rest on very little. An average used to decide who gets picked for a team, or who gets extra help in maths, needs far more — not because the maths changes, but because **the cost of being wrong lands on a person.**

*Whether the rows were picked fairly.* A hundred rows chosen badly can be worse than five chosen well. If all hundred of your Falcons are the four who bat first, your average tells you about opening batters, not about Falcons — and no amount of extra rows fixes a wrong selection.

People who do statistics for a living argue about thresholds constantly, and the honest position is that it is a judgement about consequences and spread, not a fact about arithmetic. What you can *always* do, and what this whole lesson is training, is the easy half: **print the row count next to the answer, and decide your minimum before you look at the results.** Then the reader gets to make the judgement too, which is the most honest thing available to you.

---

## ⚠️ Where This Lesson Goes Wrong

Use this table when the lesson stalls. Find what you see in the left column, then do what the right column says.

| What happens | Why | What to do right now |
|---|---|---|
| The Owls result is shrugged off — "so it's a small team, who cares" | 104 and 35.5 are both just numbers on a screen | Make it personal and specific. "Your class averaged 62% on a test. Another class has one student in it and she got 94%. The newsletter prints both averages side by side with no class sizes. Is that honest?" That version lands every time. |
| They "fix" the data by inventing more Owls | Because the one-row group feels like a mistake in the data | Stop it immediately, and say the real reason: **the one-row group is the truth.** Priya really is the only Owl. Inventing rows to make your statistics look better has a name and it is a serious one. |
| `max(counts)` is accepted because it did not crash | Not crashing genuinely feels like success | This is the whole reason it is a planted bug. Make them read `Tigers` out loud, then read the counts out loud, and sit in the gap. Then log it in the Bug Log **as an error**, even though there was no error message. |
| The two-`File` traceback sends them to the wrong file for five minutes | They read the first `File` line, which is the *caller*, not the crash | One question: "which `File` line is the last one?" Then make them say the rule back to you. Log it. Every remaining week produces these. |
| The row counts get dropped from the easy answers | Printing "5 of 12" feels like padding when the answer is obviously 5 | Enforce it on the trivial ones precisely *because* they are trivial. The habit has to be automatic by Week 34, and habits are built where they are cheap. If they drop one, hand the sheet back. |
| The minimum group size gets chosen after the results appear | It is the natural time to think about it | Put the box on the sheet **before** any answer is written, in the Concept segment. If it did not happen, stop and do it now, and then say out loud why the order matters: a rule chosen afterwards is a rule chosen to get the answer you wanted. |
| The buckets add to 11 and nobody notices, because nobody checked | The dictionary looks perfectly fine | `print(sum(counts.values()), "of", len(rows))` on the same line as the counts, every single time. Make it part of the shape of the code, not a thing you remember to do. |
| `sorted(squad, key=runs_of())` — the brackets | Every other function they have ever used needed brackets | Do not just remove them. Ask: "what does `runs_of()` give back?" *An error, because it needs a player.* "So what are you handing to `sorted`?" *Nothing.* "Right — you're handing over the **tool**, and `sorted` will use it twelve times." |
| The lab runs long and Q5 gets cut | Six questions plus an argument is a lot for 20 minutes | **Cut Q2 and Q6, never Q5.** Q5 is the lesson; the rest is practice. If you only get through Q1, Q3 and Q5, you have taught this week completely. |
| A student finds `lambda` online and uses it | Because a search for "sort by field python" returns it immediately | Let them, and then make them explain it to you in English. If they can, it is fine and they have learned something real. If they cannot, that is the argument for the named function, and they will make it themselves. |

---

## 🧭 Differentiation

This section shows how to change the lesson for a student who is struggling, flying, or not engaged today.

### If the student is struggling

**Cut:** `sorted` and the key function completely. Q6 can be answered by looking at the printed table.

**Cut:** `max(counts, key=counts.get)`. They can read the biggest count off the printed dictionary with their eyes, which is honestly what most people do.

**Cut:** three of the six questions. Keep Q1, Q3 and Q5.

**Give them `group_count` already written.** The understanding lives in the hand-trace, not in the typing. Trace it on paper with the cards, five turns minimum, then hand them the finished function and have them *use* it.

**Reteach — with the piles and the calculator.** This whole lab works on a table with no computer at all. Four piles. Count each. Add the counts, check twelve. Total each pile's runs with the calculator. Divide by the pile size. **Write every answer as `<number> from <n> players`, in that exact format, every time.** That format is the objective. A student who leaves the room writing answers in that shape has had a successful lesson whether or not any Python ran.

**The copy-this-exactly scaffold.** Two files. This runs:

`records.py`, the two tools with the docstrings removed:

```python
def filter_by(rows, key, value):
    return [r for r in rows if r[key] == value]

def group_count(rows, key):
    counts = {}
    for r in rows:
        bucket = r[key]
        counts[bucket] = counts.get(bucket, 0) + 1
    return counts
```

`lab15.py`, which uses them:

```python
from records import filter_by, group_count
from squad_data import squad

print(group_count(squad, "team"))

tigers = filter_by(squad, "team", "Tigers")
print(len(tigers), "Tigers of", len(squad))
```

Run `lab15.py`. This is the real output:

```text
{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
4 Tigers of 12
```

**One thing you must not cut:** the row count. If this lesson collapses to a single sentence, make it *"never write an average without writing how many things it came from."* That sentence is worth more than every line of syntax this week.

### If the student is flying

None of these need new syntax.

1. **`group_sum` and `group_average`** built out of the two tools they already have (Variation-harder 1). Then the question about inheriting bug fixes for free.
2. **Report the tie honestly** (Variation-harder 2). Falcons *and* Tigers.
3. **Two routes to one number** (Variation-harder 5). Add a computed `fifty` field, group by it, and check the `True` count against the Q3 filter. Two independent routes agreeing is how professionals decide they believe a number.
4. **Group by two things at once.** "How many players per team *who got out*?" They will have to filter first and then group, and the interesting part is that the counts no longer add to 12 — they add to however many got out. Ask them to print both denominators. *(8 of 12 were out.)*
5. **Which answer would change most if one row were wrong?** "Suppose one card has a typo in the runs. Which of your six answers is most sensitive to it, and why?" *(The Owls average — one row is 100% of the group. Q3's count of 5 would change by at most one. That is a genuinely deep idea about sample size and it arrives free from this dataset.)*
6. **Write the sentence a newspaper would print.** "One sentence about this squad that is true, interesting, and cannot be misread." Then: "now write one that is true and *does* mislead." Comparing the two is the whole of Week 27, arriving twelve weeks early.

### If the student won't engage today

**Cards, four bucket labels, and a calculator. Close the laptop.**

Deal the twelve cards into four team piles. Count each. Write the four numbers, add them, check twelve. Then total each pile's runs on the calculator and divide by the pile size. Write each answer on paper in this exact shape, and nothing else:

```text
Falcons   35.50  from 4 players
Tigers    33.50  from 4 players
Hawks     55.67  from 3 players
Owls     104.00  from 1 player
```

Then ask one question and let the silence do the work: **"Which team is best at batting?"**

That is the entire lesson. It takes fifteen minutes, it delivers objectives 1, 2 and 5, and the argument it starts is exactly the argument the code was only ever a vehicle for. The typing survives perfectly well to next week — and Week 16 needs a working `records.py`, so it will get written either way.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the counting line (on paper, 90 seconds)**

> "Write me the four lines that count how many players are in each team. You may not look at the screen."

*Good answer:*

```python
counts = {}
for r in squad:
    bucket = r["team"]
    counts[bucket] = counts.get(bucket, 0) + 1
```

**What to accept:** any variable names; the two middle lines merged into one (`counts[r["team"]] = counts.get(r["team"], 0) + 1`) is correct and slightly harder to read. **What to catch:** `+=` (the planted bug — ask what it means, and what is there the first time); forgetting `counts = {}`; `counts.get(bucket)` with no `0`, which gives `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` and is worth running.

**Check 2 — the silent wrong answer (spoken)**

> "`max(counts)` printed `Tigers`. The counts are Falcons 4, Tigers 4, Hawks 3, Owls 1. What did `max` actually do, and why was there no error?"

*Good answer:* "It compared the team names as text and gave the last one alphabetically. There was no error because comparing words is a legal thing to do — it just wasn't what I meant." Full marks needs **both** halves: what it compared, and why nothing complained.

**Check 3 — the row count (spoken, and it is the one that matters)**

> "The Owls average 104 runs. The Falcons average 35.5. Which team is better at batting?"

*Good answer:* "You can't tell — there's only one Owl, so 104 is just Priya's score." **Full marks needs the row count in the answer**, not just hesitation.

**What to catch:** "the Owls" with no qualification is a level-2 answer, and worth one follow-up: "how many Owls are there?" A student who then corrects themselves has understood it. A student who says "one, but 104 is still bigger" has not, and needs the class-newsletter version from the table above.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot write a filter without copying. Writes `counts[b] += 1` and cannot say why it failed. Reads an average with no thought about how many rows made it. |
| **2 — Emerging** | Filters with the comprehension given. Uses `group_count` when it is already written. Prints answers without row counts unless reminded. Accepts `max(counts)` because it ran. |
| **3 — Secure** | Writes `filter_by` and `group_count` unaided, with the key as an argument. Checks that the buckets sum to the row count. Prints every answer with its row count. Uses `max(counts, key=counts.get)` and knows why the plain version is wrong. **This is the target.** |
| **4 — Strong** | Sorts records with a named key function and knows why there are no brackets after it. Reads a two-`File` traceback to the right file first time. Says out loud that the Owls average should not be reported next to the others, and why. Sets a minimum group size before looking at results. |
| **5 — Exceptional** | Spots the Falcons/Tigers tie and says the program cannot express it. Distinguishes Dev's measured 0 from a missing value and explains why the distinction is unrecoverable once filled. Argues that spread matters as much as count when deciding whether to trust an average. Builds `group_average` out of `group_sum` and `group_count` and explains what that buys. |

---

## 📤 Homework to Assign

This section gives you the words to assign the homework, the workbook sections it uses, and what to look for when you mark it.

**Say this:**

> "Your own twelve records, your own two tools, six answers — and one sentence that I care about more than the other six things put together. About an hour.
>
> **First, the tools.** Workbook, **Build It, Part 1.** Write `filter_by()` and `group_count()` into your own `records.py`, and **the key goes in as an argument** — not hard-coded to `genre` or `team` or whatever your column is called. If your function only works on your own table, you have written an answer. I want a tool.
>
> **Second, six questions.** **Build It, Part 2.** Point them at the twelve records you built last week. Here they are: how many rows in each category; which category has the most; how many rows are above some number you choose; the average of one number column for one category; that same average for **every** category; and your top three rows sorted by one number.
>
> **And every single answer gets its row count.** Not '183 plays'. **'183 plays, from 5 songs.'** Every one, including the ones where it feels silly. I will hand back a page that is missing one.
>
> **Also print the sum check.** After you group, add the buckets up and print that they come to the number of rows you started with. One line. It is the cheapest way there is of knowing you have not lost anything. Then **Part 3**: pick one average and check it by hand with a calculator.
>
> **Third, one sentence.** **Build It, Part 4.** **Which of your six answers do you trust least, and why?** Not 'they're all fine'. Pick one. If one of your categories has only one or two rows in it, that is almost certainly your answer, and I want you to say so in your own words — and then tell me what you would do about it. Finish with **Part 5, the Bug Log** (at least one entry with no error message), and the **Draw It** page: your six answers with the denominator beside every one."

**Workbook sections:** the **core homework is Build It (Parts 1–5) and Draw It**. The rest of the workbook is practice that follows the lesson: **Warm-Up, Predict the Output, Practice Set A (A1–A6), Practice Set B (B1–B5), Fix the Broken Program, Puzzle of the Week, Think Deeper and Self-Check.** Suggested split: Warm-Up, Predict the Output and Practice Set A on a second sitting or in the first few minutes of next session, because they only need what was taught today; Practice Set B, Fix the Broken Program, Puzzle and Think Deeper as extra practice at your discretion (B1–B4 and the Fix are the best ones to pick if you pick two); Self-Check last. Practice Set B5 and Build It use the student's **own** twelve records, so there is no single right answer for those — mark against the checks below.

**Expected time:** the core homework is about **60 minutes** — 15 min writing the two tools · 25 min on the six questions · 10 min on the sum check, the hand check and tidying the output · 10 min on the trust sentence. Warm-Up, Predict and Practice Set A add roughly 30 minutes more; Set B, Fix, Puzzle and Think Deeper another hour or so. Do not assign all of it in one week.

> **🧑‍🏫 What to look for when you mark it:** two things, in this order. **One — is the key an argument?** A `group_count(rows)` with `"genre"` written inside the function is the defect that matters, because Week 16 imports these tools and points them at a CSV. **Two — does every answer carry its row count?** That is the habit this whole week exists to build, and it is much easier to insist on now than in Week 34 when there are a hundred rows and a deadline.

---

## 🔑 Answer Key

Organised in the same order as the workbook, section by section and item by item. Every question is restated briefly, so you can mark from this page alone. Values are the workbook's own Answers section, re-run and confirmed on the twelve-record `squad`, the twelve-song `playlist` from Week 14 and the `canteen.py` data. The workbook's squad is the one in `squad_data.py` (see the Prep Checklist). The in-class six-question activity is keyed at the end of this section.

### ✅ Warm-Up (5 min) — five questions about last week

| # | Question | Answer |
|---|---|---|
| W1 | `len(squad)` and `len(squad[0])` | **12** (rows) and **5** (fields in the first record: name, team, runs, balls, out — the number of columns *if every record has the same keys*) |
| W2 | Print the runs of the last row, without 11 | `print(squad[-1]["runs"])` → `104`. `-1` is the last slot (Week 11); better than `squad[11]` because it survives a thirteenth player |
| W3 | Why is `"Asha" in squad[0]` `False`? | `in` checks the **keys**, not the values. `Asha` is a value stored under `name`; there is no *label* called `Asha` |
| W4 | One-line comprehension for the `runs` column, and what it throws away | `all_runs = [r["runs"] for r in squad]` — throws away **every label**: twelve numbers with no idea which player each belongs to, and no way back |
| W5 | `for row in enumerate(squad):` — what is `row`, and what is the error for `row["name"]`? | `row` is a **pair**, `(0, {...})` — position and record. `row["name"]` → `TypeError: tuple indices must be integers or slices, not str`, because a pair is counted, not labelled |

**What to watch for:** W3 is the usual stumble (students say "because Asha isn't a key" without saying `in` looks at keys). W4's second half is the point — "it throws away the labels" is full marks; "nothing" is not.

### 🔎 Predict the Output — P1 to P4

*The prediction is the exercise: two of the four give a wrong answer with no error message, and the score line is out of 9 answers.*

| # | Real output | Why |
|---|---|---|
| P1 | `{'pop': 3, 'rock': 2}` then `5 of 5` | Three pop, two rock; 3 + 2 = 5 = rows, so the sum check passes. Buckets appear in the order first met (`pop` first, because Blue Lights came first) |
| P2 | `cherry`, `banana`, `9` | `max(counts)` is the biggest **key**, judged as text (cherry is last alphabetically; the numbers are never looked at). `max(counts, key=counts.get)` is the key with the biggest **count**. `max(counts.values())` is the biggest **count itself**, with no idea which key it belonged to |
| P3 | `2`, `3`, `['Asha', 'Omar']` | Two rows pass `> 40`; `len(rows)` is still 3 because filtering builds a new list; Dev's `0` is not more than 40 |
| P4 | A traceback ending `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | The `0` is missing from `.get`; `counts.get(team)` returns `None` the first time and `None + 1` is meaningless. Fix: `counts.get(team, 0) + 1` |

Here is the real traceback for the last prediction:

```text
Traceback (most recent call last):
  File "p4.py", line 3, in <module>
    counts[team] = counts.get(team) + 1
                   ~~~~~~~~~~~~~~~~~^~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

**Where students go wrong:** P2 — most predict `banana` for the first line (they read it as "biggest count"); that is the Week 15 misconception in one line. P4 — most predict `{'Falcons': 2, 'Tigers': 1}` because the line *looks* right; it is one character from correct, and that is the best near-miss of the week. The "which one surprised you most" box has no wrong answer, but "none" after missing P2 deserves a conversation. The workbook's score line is out of 9: P1 has two printed lines (the counts and the `5 of 5`), P2 has three, P3 has three and P4 has one.

### ✍️ Practice Set A — Read It

**A1. Filter or group?**

| # | Question | Filter or group? | What comes back |
|---|---|---|---|
| a | "Show me the Tigers." | filter | a smaller list of records — 4 of them |
| b | "How many players per team?" | group | a dictionary, one key per team |
| c | "Who scored more than 50?" | filter | a smaller list of records — 5 of them |
| d | "How many got out, and how many didn't?" | group | a dictionary with two keys, `True` and `False` |
| e | "What's the Hawks' average?" | filter, then arithmetic | one number — and it needs its row count |
| f | "Which team is biggest?" | group, then `max` | one key — and it cannot express a tie |

**A1(g) What is the one thing a filter changes, and the one thing it never changes?**
It changes **how many rows** you have. It never changes **what a row is** — every record that comes out still has all of its labels and all of its fields. Five cards out of twelve are still cards.

**A1(h) After `tigers = filter_by(squad, "team", "Tigers")`, what does `len(squad)` say?**
`12`. Still twelve. `filter_by` builds a **new** list; it does not touch the original. This is worth running rather than believing — a student who thinks filtering is destructive gets nervous about running things twice.

**A2. Spot the bug** (`counts[r["team"]] += 1` on an empty dictionary).
The last line of the traceback is `KeyError: 'Falcons'`. It fails on the **first** row because `+=` means "take what is there and add one", and on the very first Falcon `counts` is empty, so there is nothing to take. The fix:

```python
    counts[r["team"]] = counts.get(r["team"], 0) + 1
```

**A3. Match the code to the output.** a → **3** · b → **4** · c → **1** · d → **2**. Real output: a is `3` (Asha's 48, Omar's 90 **and** Zara's 41 are above 40; Dev's 0 is not), b is `179` (48 + 0 + 90 + 41), c is `{'Falcons': 1, 'Tigers': 2, 'Hawks': 1}`, d is `Tigers`. **Yes, the counts add up:** 1 + 2 + 1 = **4** = the number of rows. Dev's 0 is inside the 179, contributing nothing but still counted as a row, which is right for a measured zero.

**A4. Label the diagram** (Figure W15.1, boxes A–E).

- **A** — the **row count** for that bucket
- **B** — the **bucket label** / the **key** of the counting dictionary
- **C** — the **counting dictionary** (the whole set of buckets)
- **D** — the **group you would not report an average for** (the one-row group)
- **E** — the **sum check** — proof every row went into exactly one bucket and none was dropped

The extra: the **Owls**, because there is only one row. An average summarises several things; with one thing there is nothing to summarise, and 104 ÷ 1 is Priya's score with a division applied. *(The workbook figure is the authority for letters A–E; check the student's labels against the figure, not just this list.)*

**A5. Trace the counting dictionary** (`group_count(squad, "team")`, first six records).

| Turn | record | `bucket` | `counts.get(bucket, 0)` | `counts` afterwards |
|---|---|---|---|---|
| 1 | Asha | `Falcons` | `0` (never seen) | `{'Falcons': 1}` |
| 2 | Ravi | `Falcons` | `1` | `{'Falcons': 2}` |
| 3 | Nita | `Falcons` | `2` | `{'Falcons': 3}` |
| 4 | Sam | `Falcons` | `3` | `{'Falcons': 4}` |
| 5 | Kabir | `Tigers` | `0` (never seen) | `{'Falcons': 4, 'Tigers': 1}` |
| 6 | Meera | `Tigers` | `1` | `{'Falcons': 4, 'Tigers': 2}` |

**After all twelve:** `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}`. **4 + 4 + 3 + 1 = 12**, and `len(squad)` is **12**. It matters because grouping is supposed to put *every* row in exactly one bucket. If the total came to 11, a row was dropped and went into no bucket at all. (A stray space or a different capital does not change the total — it makes an extra bucket, and the total is still 12. Noticing that needs a different check: count the buckets.)

Teacher-only follow-ups to ask while they trace:

- **What does `counts.get(bucket, 0)` do the first time a bucket is seen, and every time after?** The first time there is no such key, so it hands back the fallback `0`, and `0 + 1` is `1`. Every time after, the key exists, so it hands back the count so far, and one more gets added. One expression, both cases, no `if`.
- **What happens with `counts[bucket] += 1` instead?** This is the planted bug; see the traceback below. Because `+=` means "take what is there and add one", and on the first Falcon there is nothing there.

```text
Traceback (most recent call last):
  File "lab15.py", line 10, in <module>
    print(group_count(squad, "team"))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "records.py", line 19, in group_count
    counts[bucket] += 1
    ~~~~~~^^^^^^^^
KeyError: 'Falcons'
```

- **Two `File` lines — which is where it broke?** The **last** one, `records.py, line 19`. The one above, `lab15.py, line 10`, is where the function was *called from*. Together they are a trail of who called who, read from the bottom.

**A6. Every answer needs its denominator.**

| The sentence | Verdict | The fix |
|---|---|---|
| "The Owls average 104 runs." | **not honest enough** | "The Owls average 104 runs — from one player, so it is not really an average at all." |
| "Five of the twelve players scored more than fifty." | **honest** | Nothing to fix; the number **and** the denominator are both there |
| "Falcons are the biggest team." | **not honest enough** | "Falcons and Tigers are tied on four players each, out of twelve." The tie is the missing bit |
| "The Hawks average 55.67 runs, from 3 players." | **honest** | Nothing to fix — though "and Omar's 90 pulls it up a long way" would be even better |
| "Average spend is 41.67 rupees a day." | **not honest enough** | "Monday's average spend is 41.67 rupees, from 3 orders." Which day? How many orders? |

### ✍️ Practice Set B — Write It

**B1. Two lines** — names of everybody who faced more than 40 balls, and how many out of how many.

```python
big = [r for r in squad if r["balls"] > 40]
print([r["name"] for r in big])
print(len(big), "of", len(squad))
```

```text
['Nita', 'Kabir', 'Iqbal', 'Omar', 'Priya']
5 of 12
```

Nita 55, Kabir 41, Iqbal 44, Omar 61, Priya 70. **Kabir's 41 counts** (41 is more than 40) — a boundary worth checking, Week 5 again. The second line must say `5 of 12`, not a bare `5`.

**B2. `filter_by`, written by the student.**

```python
def filter_by(rows, key, value):
    """Keep only the rows where rows[key] equals value."""
    return [r for r in rows if r[key] == value]
```

Two calls on completely different tables, for example `print(len(filter_by(squad, "team", "Tigers")), "of", len(squad))` and `print(len(filter_by(playlist, "genre", "pop")), "of", len(playlist))`.

**The two things to mark, in this order:**

1. **Is `key` an argument?** `def group_count(rows):` with `"genre"` written inside the body is the defect that matters. Send it back — Week 16 imports these functions and points them at a CSV, and a hard-coded key will break it.
2. **Does `group_count` use `.get(bucket, 0)`?** A four-line `if bucket in counts: ... else: ...` version is **completely correct** and gets full marks. Say so, then show the one-line version beside it as the reason `.get()` exists.

Everything else — variable names, docstrings, whether `column` exists at all — is theirs.

**B3. `group_count`, written by the student.** The reference `records.py` for the whole week (with `column`, which later sections use):

```python
"""records.py - tools that work on ANY list of dictionaries."""

def filter_by(rows, key, value):
    """Keep only the rows where rows[key] equals value."""
    return [r for r in rows if r[key] == value]

def column(rows, key):
    """Pull one column out of the rows as a plain list of values."""
    return [r[key] for r in rows]

def group_count(rows, key):
    """Count how many rows share each value of key. One bucket per value."""
    counts = {}                                     # start with no buckets at all
    for r in rows:                                  # look at every row once
        bucket = r[key]                             # which bucket does this row go in?
        counts[bucket] = counts.get(bucket, 0) + 1  # count so far (0 if new) plus one
    return counts
```

The check line after calling it: `print(sum(counts.values()), "of", len(rows))`. The `if bucket in counts: ... else: ...` version (`counts[bucket] = counts[bucket] + 1` / `counts[bucket] = 1`) gets full marks. Done looks like: key is an argument, `.get(bucket, 0)` is there, and the sum check is printed without being asked twice.

**B4. Key function and top three.**

```python
def balls_of(player):
    """Key function: given one player, hand back the number to sort on."""
    return player["balls"]


ranked = sorted(squad, key=balls_of, reverse=True)
for position, player in enumerate(ranked[:3], start=1):
    print(f"{position}. {player['name']:<7}{player['balls']:>4} balls")
print("rows in squad still:", len(squad))
```

```text
1. Priya    70 balls
2. Omar     61 balls
3. Nita     55 balls
rows in squad still: 12
```

**Mark three things:** `key=balls_of` with **no brackets** (the one everybody gets wrong once; with brackets the error is `missing 1 required positional argument: 'player'`), `reverse=True` because biggest first was asked for, and **the original is untouched** — `sorted` built a new list, so `squad` still has twelve records in typed order.

**B5. Averages per group with the honest guard** (on the student's **own** twelve records). Model answer on the twelve-song playlist:

```python
"""hw15.py - averages per group, with the honest guard."""

from records import filter_by, group_count, column
from playlist_data import playlist

MIN_GROUP = 3        # decided BEFORE looking at the answers

genre_counts = group_count(playlist, "genre")
print("songs per genre   :", genre_counts)
print("rows accounted for:", sum(genre_counts.values()), "of", len(playlist))

print()
print("average plays per genre")
print("-" * 56)
for genre in genre_counts:
    rows = filter_by(playlist, "genre", genre)
    plays = column(rows, "plays")
    average = sum(plays) / len(plays)
    if len(rows) < MIN_GROUP:
        print(f"{genre:<7}{average:8.2f} plays   from {len(rows)} song(s)  <-- too few to average")
    else:
        print(f"{genre:<7}{average:8.2f} plays   from {len(rows)} song(s)")
print("-" * 56)
print(f"minimum group size agreed first: {MIN_GROUP}")
```

```text
songs per genre   : {'pop': 5, 'rock': 3, 'folk': 3, 'indie': 1}
rows accounted for: 12 of 12

average plays per genre
--------------------------------------------------------
pop      183.00 plays   from 5 song(s)
rock     128.33 plays   from 3 song(s)
folk      58.33 plays   from 3 song(s)
indie     65.00 plays   from 1 song(s)  <-- too few to average
--------------------------------------------------------
minimum group size agreed first: 3
```

**Hand checks:**

```text
pop:    120 + 300 = 420 · +95 = 515 · +180 = 695 · +220 = 915 · 915 / 5 = 183.0   ✔
rock:   45 + 210 = 255 · +130 = 385 · 385 / 3 = 128.333... = 128.33               ✔
folk:   60 + 75 = 135 · +40 = 175 · 175 / 3 = 58.333... = 58.33                   ✔
indie:  65 / 1 = 65.0                                                             ✔
Counts: 5 + 3 + 3 + 1 = 12 = len(playlist)                                        ✔
```

**Mark:** `MIN_GROUP` is a **named value** at the top, not a `3` buried in the `if`; the workbook box "I chose it before I saw the answers" is ticked **honestly** (if they tick "no", praise that and move on). The sum check is printed. Every line carries its row count, and the one-row group says so out loud rather than being quietly dropped.

### 🐞 Fix the Broken Program — `canteen.py`

**Bug 1 — one equals sign.**

- (a) `r["form"] = form` is an **assignment**, not a question. One `=` means "put this in that"; two mean "is this the same as that?". Inside an `if` you are asking a question, so it must be `==`. Week 5 again.
- (b) `    rows = [r for r in orders if r["form"] == form]`
- (c) Because a `SyntaxError` means Python could not read the file at all. It reads the whole thing before it runs a single line, so nothing above the mistake gets a chance to happen. The program is not "partly working"; it has not started.

**Bug 2 — `+=` on an empty bucket.**

- (a) "Take what is there and add one."
- (b) **Nothing.** There is no key called `7A` yet; `counts` is empty.
- (c) `    counts[bucket] = counts.get(bucket, 0) + 1`
- (d) Only one `File` line because the counting loop is in the same file as the call. If `group_count` had lived in `records.py` and been called from `canteen.py` there would be two — one for the caller and one for the crash. **And you read the last one.**

**Bug 3 — the silent one.**

- (a) **7B**, with three orders. The program said **7C**.
- (b) `max(counts)` compared the **form names as text** (`"7A"`, `"7B"`, `"7C"`) and handed back the last one alphabetically. It never looked at the counts.
- (c) Nothing is wrong as far as Python is concerned: comparing text is legal and `"7C"` does come after `"7B"`. The program did exactly what was said, and what was said was not what was meant.
- (d) `print("biggest form   :", max(counts, key=counts.get))`
- (e) `7C 120.0` is from **one** order (Priya's). Three defensible options: print it with the count beside it; print it with a warning; or do not print the average and say "7C: 1 order, not enough to average". Not allowed: `7C 120.0` under `7A 32.5` with nothing else, because a reader will conclude 7C are the big spenders.
- (f) The two changes:

```python
print("rows accounted:", sum(counts.values()), "of", len(orders))
```

```python
    print(f"{form}  {sum(spends) / len(spends):7.2f}   from {len(rows)} order(s)")
```

The fully fixed program prints:

```text
orders per form: {'7A': 2, '7B': 3, '7C': 1}
rows accounted: 6 of 6
biggest form   : 7B
7A    32.50   from 2 order(s)
7B    35.00   from 3 order(s)
7C   120.00   from 1 order(s)
```

Hand check: 7A is 40 + 25 = 65, ÷ 2 = 32.50; 7B is 60 + 15 + 30 = 105, ÷ 3 = 35.00.

- (g) **Bug 3, and it is not close.** Bugs 1 and 2 stopped and pointed at the exact spot. Bug 3 printed a tidy, confident report with the wrong form named biggest. *The error message is not the enemy. The silent wrong answer is.* Accept a reasoned different choice, but a student who picks Bug 1 or 2 has not yet felt this.

### 🧩 Puzzle of the Week — The Tally Detective

**Part A** (`{'pop': 5, 'rock': 3, 'folk': 3, 'indie': 1}`):

- (a) **12 rows**, because grouping puts every row in exactly one bucket: 5 + 3 + 3 + 1 = 12.
- (b) **Four** different values — one bucket per distinct value.
- (c) `max(counts)` → **`rock`**: it compares keys as words (folk, indie, pop, rock) and `rock` is last. The counts are never consulted.
- (d) `max(counts, key=counts.get)` → **`pop`**; `max(counts.values())` → **`5`**.
- (e) **`indie`**, with one row. One song is not an average — it is that song's play count with a division by one applied.

**Part B** (the missing Tiger: `{'Falcons': 4, 'Tigers': 3, 'Tigers ': 1, 'Hawks': 3, 'Owls': 1}`):

- (a) **Yes:** 4 + 3 + 1 + 3 + 1 = 12. **The sum check passed.**
- (b) Expected **four** buckets; there are **five**.
- (c) One record's team was typed `"Tigers "` with a **trailing space**, so it is a different piece of text and therefore a different bucket.
- (d) **Catches:** dropped rows — the total comes out short. **Misses:** a row in the *wrong* bucket — it is still counted, just somewhere else, so the total is perfect and the answer is wrong. This is the important part of the whole puzzle.
- (e) **Count the buckets and compare with how many you expected** — e.g. `print(len(counts), "buckets")` and read the keys. (Cleaning stray spaces and capitals properly is Week 24; *noticing* them is this week.)

**Part C** (one wrong row among twelve):

| The answer | How much could one wrong row move it? | Why |
|---|---|---|
| Owls average (1 row) | **completely** — any amount | The one row **is** 100% of the group. Change 104 to 14 and the answer changes by 90 |
| Falcons average (4 rows) | by **one quarter** of the error | A 40-run typo moves the average by 10 |
| "5 of 12 scored over 50" | by **at most 1** | A wrong runs value can push one player across the line or back: 5 becomes 4 or 6 |
| Total runs (547) | by exactly the size of the error | A 40-run typo makes it 587 or 507, without changing the shape of any conclusion |

**Most fragile: the Owls average.** Rule: *the smaller the group, the more one row can move its answer* — which is why the row count is the first thing to look at, not the last.

**Part D** (own data; one-row group). Three allowed sentences, for the playlist's `indie`: (1) "Indie averages 65 plays, from 1 song." (2) "Indie averages 65 plays, from 1 song — too few to call this an average." (3) "Indie: 1 song, not enough to average." **Not allowed:** "Indie averages 65 plays." — arithmetically perfect and it misleads without a single false number. Full credit also for the fourth answer, *collect more indie songs*.

### 🤔 Think Deeper

Open-ended; mark against the model answers.

**T1. How many rows do you need before an average means anything?** Full marks needs: "one row is not an average" (two is barely better) · at least **two of the three dependencies** — **how spread out the values are** (spread matters as much as count), **what the answer will be used for** (the cost of being wrong lands on a person), and **whether the rows were picked fairly** (a hundred badly chosen rows can be worse than five well chosen) · and the always-do-this rule at the end: **print the row count beside the number and decide the minimum before looking at results.**

**T2. Is `max` giving one answer to a two-answer question a bug?** Full marks needs: a side taken · the observation that `max` is doing what it is defined to do and never claimed to report ties · and a real answer to the Week 34 question rather than "I'll be careful" (by eye works for four buckets; with a hundred rows and thirty buckets it will not, so the check belongs in the program). The two-line code fix, verified on the twelve records:

```python
best = max(counts.values())
winners = [k for k in counts if counts[k] == best]
```

```text
counts : {'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}
biggest count: 4
winners: ['Falcons', 'Tigers']
```

### 🛠️ Build It — the core homework (own twelve records)

**Part 1 — Your two tools.** Check the six boxes: `records.py` exists next to the data file; `filter_by(rows, key, value)` and `group_count(rows, key)` take the **key as an argument**; `group_count` uses `.get(bucket, 0)`; neither function names any column or the topic. The deciding question is **is the key an argument?** — `def group_count(rows, key):` is a tool, `def group_count(rows):` is an answer. The reference tools are in **Practice Set B, B3** above. The "could I point them at somebody else's table tomorrow?" box should be **yes**; if "no", the "what is stopping them" line should name the hard-coded column. Troubleshooting: `ModuleNotFoundError: No module named 'records'` means the terminal is in a different folder or the file name is misspelled (Week 12's lesson).

**Part 2 — Six questions, six row counts.** The student's dataset is theirs. Mark in this order:

- **(1)** Does every answer carry a row count? A bare number gets sent back.
- **(2)** Does the sum check pass? `sum(counts.values())` equals `len(rows)`.
- **(3)** Are there the number of buckets expected? This is the check the sum test cannot do. Five where four were expected means a stray space or capital.
- **(4)** If two categories are tied for Q2, does the student write the honest "X and Y, tied on N each" that the program cannot say?

Q3 should use a condition comprehension, not `filter_by`. An exact-match function cannot do "greater than", and noticing that is worth a tick.

Here is a model answer on the twelve-song playlist from Week 14:

```python
"""hw15.py - Week 15 homework: six questions, every answer with its row count."""

from records import filter_by, group_count, column
from playlist_data import playlist

def plays_of(song):
    """Key function: given one song, hand back the number to sort on."""
    return song["plays"]

print(f"{len(playlist)} rows, {len(playlist[0])} columns\n")

# Q1
genre_counts = group_count(playlist, "genre")
print("Q1  songs per genre:", genre_counts)
print("    rows accounted for:", sum(genre_counts.values()), "of", len(playlist))

# Q2
top_genre = max(genre_counts, key=genre_counts.get)
print(f"\nQ2  biggest genre: {top_genre} ({genre_counts[top_genre]} songs of {len(playlist)})")

# Q3
popular = [s for s in playlist if s["plays"] > 150]
print("\nQ3  songs with more than 150 plays:", column(popular, "title"))
print(f"    {len(popular)} of {len(playlist)} songs")

# Q4
pop = filter_by(playlist, "genre", "pop")
pop_plays = column(pop, "plays")
print("\nQ4  pop plays:", pop_plays)
print(f"    average {sum(pop_plays) / len(pop_plays):.2f} plays (from {len(pop)} songs)")

# Q5
print("\nQ5  average plays per genre")
for genre in genre_counts:
    rows = filter_by(playlist, "genre", genre)
    plays = column(rows, "plays")
    print(f"    {genre:<6}{sum(plays) / len(plays):8.2f} plays   from {len(rows)} song(s)")

# Q6
ranked = sorted(playlist, key=plays_of, reverse=True)
print("\nQ6  top three by plays")
for position, song in enumerate(ranked[:3], start=1):
    print(f"    {position}. {song['title']:<14}{song['plays']:>5} plays")
```

Real output:

```text
12 rows, 5 columns

Q1  songs per genre: {'pop': 5, 'rock': 3, 'folk': 3, 'indie': 1}
    rows accounted for: 12 of 12

Q2  biggest genre: pop (5 songs of 12)

Q3  songs with more than 150 plays: ['Ghost Town', 'Neon Streets', 'Late Bus', 'Corner Shop']
    4 of 12 songs

Q4  pop plays: [120, 300, 95, 180, 220]
    average 183.00 plays (from 5 songs)

Q5  average plays per genre
    pop     183.00 plays   from 5 song(s)
    rock    128.33 plays   from 3 song(s)
    folk     58.33 plays   from 3 song(s)
    indie    65.00 plays   from 1 song(s)

Q6  top three by plays
    1. Ghost Town      300 plays
    2. Corner Shop     220 plays
    3. Neon Streets    210 plays
```

**Part 3 — Hand-check one answer.** Model, on the pop songs: 120 + 300 = 420 · +95 = 515 · +180 = 695 · +220 = 915 · 915 / 5 = 183.0, matching the code. Why it is worth doing even when the code is right: now the student knows what the right answer *looks like*, so if the code ever disagrees one of them is wrong and they will go and check, instead of believing the screen because it is a screen.

**Part 4 — The answer you trust least.** Full marks needs three things: **which** answer, **its row count**, and **what a reader would wrongly conclude.** Model answer for the playlist:

> *"Q5's indie line. It says indie songs average 65 plays, but there is only one indie song in my playlist, so that is just Kite Season's play count divided by one. Next to pop's 183 from five songs it makes indie look unpopular, and I have no idea whether indie songs are unpopular — I have one of them."*

An answer that says only "the indie one because it's small" has two of the three; ask for the third out loud. **What would you do about it:** any of the three defensible options (print it with the count, print it with a warning, do not print it). **Extra credit for a fourth:** *collect more indie songs* — the problem is not the arithmetic, it is that there is not enough data yet, and no amount of clever code fixes that. **The sentence at the top of all six answers**, model answer:

> *"All of these come from 12 songs, and every average below has the number of songs it came from printed next to it — the indie figure comes from a single song and should not be compared with the others."*

**This sentence is the whole point of the week.** Mark it properly.

A student who can write it will produce an honest capstone in Week 35.

**Part 5 — The Bug Log.** Two entries, and at least one must have **no error message** at all. Model entries: (1) `KeyError: 'Falcons'` with two `File` lines (`lab15.py` line 10 and `records.py` line 19) — `+=` means "take what is there and add one" and there is nothing there the first time; fix `counts[bucket] = counts.get(bucket, 0) + 1`. (2) **No error message:** `max(counts)` printed `Tigers` while the counts were Falcons 4, Tigers 4, Hawks 3, Owls 1 — `max` compared the names as words; fix `max(counts, key=counts.get)` and read the answer against the printed counts. **The two-`File`-line rule:** the **last** `File` line is where the program broke; the ones above are the trail of who called who, read from the bottom up.

### 🎨 Draw It

No single right drawing. A strong one: **(1)** the third column (the denominator) is filled in for every row; **(2)** the one-row group is **ringed and explained**, not left out ("one song — Kite Season's play count with a division by one applied"); **(3)** `MIN_GROUP` appears with a note that it was chosen first; **(4)** one box says what a reader would wrongly conclude. Test: **cover the third column — does the second column now tell a lie?** If yes, the third column is not decoration. An empty third column is the mistake.

### 📊 Self-Check

The "I can…" grid is the student's own rating; ask about any 😕. **True or false:**

| Statement | Answer |
|---|---|
| Filtering deletes rows from the original table | **FALSE** — it builds a new list |
| What comes out of a filter is still records, with all their labels | **TRUE** |
| Grouping throws some rows away | **FALSE** — that is why the buckets add up |
| `counts[bucket] += 1` works the first time you meet a bucket | **FALSE** — `KeyError` |
| `max(counts)` gives you the biggest count | **FALSE** — the biggest **key**, as text |
| `max` tells you when there is a tie | **FALSE** — it hands back the first and says nothing |
| `key=runs_of()` is the right way to pass a key function | **FALSE** — no brackets; hand over the tool, not the result |
| `sorted` moves whole records, not just values | **TRUE** |
| The first `File` line in a traceback is where the program broke | **FALSE** — the **last** one |
| An average of 104 from one row is arithmetically wrong | **FALSE** — it is perfect; reporting it without its row count is what is wrong |
| If the buckets add up, the grouping must be correct | **FALSE** — a row in the **wrong** bucket is still counted |

### 🎲 In-class activity — the six questions on the squad (not in the workbook)

This is the key for *The Activity, In Full* above (the squad, Falcons / Tigers / Hawks / Owls). The student's workbook does not contain these items; they are the in-class lab. Full working file and real output are in *The Activity, In Full*. The six answers:

| Q | Question | Answer | Row count |
|---|---|---|---|
| 1 | players per team | `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}` | 12 of 12 accounted for |
| 2 | biggest team | `Falcons, with 4 players` — **but it is a tie with Tigers** | 4 of 12 |
| 3 | scored more than 50 | `['Nita', 'Kabir', 'Iqbal', 'Omar', 'Priya']` | 5 of 12 |
| 4 | Falcons average | `35.50 runs` | from 4 players |
| 5 | average per team | Falcons 35.50 · Tigers 33.50 · Hawks 55.67 · **Owls 104.00** | 4 · 4 · 3 · **1** |
| 6 | top three | Priya 104 · Omar 90 · Nita 77 | 3 of 12 |

**Hand checks — do at least one of these with the student:**

```text
Falcons:  48 + 12 = 60 · 60 + 77 = 137 · 137 + 5 = 142 · 142 / 4 = 35.5     ✔
Tigers:   63 + 30 = 93 · 93 + 0 = 93 · 93 + 41 = 134 · 134 / 4 = 33.5       ✔
Hawks:    55 + 22 = 77 · 77 + 90 = 167 · 167 / 3 = 55.666... = 55.67        ✔
Owls:     104 / 1 = 104.0                                                    ✔
Total:    142 + 134 + 167 + 104 = 547 = sum of the whole runs column         ✔
```

That last line is a free cross-check: **the four group totals add back up to the whole-column total**, which means no row was counted twice or missed.

**Is Q2's "Falcons" the whole truth?** No. Falcons and Tigers both have four players, so the honest answer is "Falcons and Tigers, four each". `max` returned Falcons because Falcons was typed first, and `max` has no way to report a tie. The number is not wrong; the answer is incomplete.

**Which of the six do you trust least?** **Q5's Owls line.** `104.00 runs from 1 player` is arithmetically perfect and useless as an average: it is Priya's score with a division by one applied. Beside the Falcons' 35.50 it invites the reader to conclude the Owls are three times the batting side, which the data cannot support.

**Three defensible things to do about it:** print it with the row count beside it; print it with an explicit warning; or do not print the average and report "Owls: 1 player, too few to average". Not defensible: `104.00` beside `35.50` with no counts.

**Why must the minimum group size be decided before you see the answers?** Because a rule chosen afterwards is a rule chosen to produce the answer you already wanted. If you look first and *then* decide that groups under three do not count, you have not applied a standard — you have removed a number you did not like.

### Answers to every question posed in the lesson

- *"Which team has the most players?"* → Falcons and Tigers, four each. It is a tie, and the program cannot say so.
- *"The piles add up to twelve. Why do I care?"* → Because if they did not, a row went missing, and nothing else would have told you.
- *"Are the five filtered cards still cards?"* → Yes, with all five labels. A filter changes how many rows you have, never what a row is.
- *"Which of the four piles do you trust least?"* → The Owls. One card.
- *"In `[r for r in rows if ...]`, what ends up in the new list?"* → The whole record. Last week the front said `r["runs"]` and gave numbers; this week it says `r` and gives records.
- *"First time we meet Hawks, what does `counts.get("Hawks", 0)` give?"* → `0`. Which is why `0 + 1` is the right first count.
- *"Why check that the buckets add up to twelve?"* → To know no row was dropped or put in a bucket you did not notice.
- *"The Owls average 104. Is the number wrong?"* → No. The arithmetic is perfect. Reporting it without its row count is what is wrong.
- *"What's the smallest pile you'd call an average?"* → Any argued answer; three is sensible for this data. The important part is that it was chosen **before** the answers appeared.
- *"How many Tigers, and who?"* → 4 of 12: Kabir, Meera, Dev, Zara.
- *"What does `+=` actually mean, and what's there the first time?"* → "Take what is there and add one" — and the first time there is nothing there, so `KeyError`.
- *"Which `File` line is where it broke?"* → The **last** one. The ones above are the trail of who called who.
- *"`max(counts)` says Tigers. Does that look right?"* → No. It compared the team names as text and returned the last alphabetically, without ever looking at the counts. And it did not complain.
- *"What's the honest answer to 'which team is biggest'?"* → Falcons and Tigers, four each — which the program as written cannot express.
- *"What does `runs_of()` give back, with the brackets?"* → An error: `missing 1 required positional argument: 'player'`. You are meant to hand `sorted` the tool, not the result.
- *"What did `sorted` move?"* → Whole records. Every field travelled with its row.
- *"Which team is best at batting?"* → You cannot tell from this data. The Owls' 104 is one player's score, and one row is not an average.

---

## 🔮 Next Week Preview

Next week the dataset leaves the program. Everything the student has built so far vanishes the moment the file stops running, and a project you have to retype every morning is not a project. So Week 16 writes the twelve records out to a **CSV file** — a plain text file with the column names on the first line and one row per line after that, which is the format every spreadsheet on Earth can open — and then reads them back in and proves, field by field, that nothing changed on the way. Which is where the trap is, and it is a beautiful one: **everything read back out of a CSV file is text.** The number 104 goes in as a number and comes back as the characters `1`, `0`, `4`, and the student's `max()` will then cheerfully report that the highest score in the squad is 95, because `'95'` beats `'104'` when you compare words letter by letter. No crash. No warning. The whole project is a 30-record dataset written, loaded, converted back to real numbers, and checked — and the checking is the point.

**Prep early:** three things. **Keep `records.py`, `squad_data.py` and `lab15.py` exactly as they are** — Week 16 adds two functions to `records.py` and reuses the rest, so a working folder saves twenty minutes. **Check the homework's `group_count` takes the key as an argument**, because next week points that same function at data loaded from a file and a hard-coded key will break it. And **find out how to open a CSV file in a spreadsheet** on whatever machine you have — Google Sheets, Excel or Numbers, any is fine. Seeing their own typed dictionaries appear as a real spreadsheet grid is the best thirty seconds of Week 16, and it is worth not fumbling.

---

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Student Guide](../student-guide/week-15.md) · [Workbook](../workbook/week-15.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
