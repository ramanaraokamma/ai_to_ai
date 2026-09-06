# Week 15 — Filter It, Group It, Count It

[⬅ Week 14](week-14.md) · [Course Home](../README.md) · [Week 16 ➡](week-16.md) · [Student Guide](../student-guide/week-15.md) · [Workbook](../workbook/week-15.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — two reusable functions written, then six questions answered with them |
| **Big idea** | Filtering keeps the rows that pass a test; grouping counts how many rows share a value. And **every group answer must be reported with its row count.** |
| **New vocabulary** | filter · group · counting dictionary · key function · row count |
| **New syntax** | `[r for r in rows if r["age"] > 12]` · `sorted(rows, key=...)` · `sum(numbers)` · `max(counts, key=counts.get)` |
| **Materials** | The twelve index cards from Week 14 · **four sheets of paper as bucket labels** · a pen · printed workbook pages 15.1–15.6 · the Bug Log · a calculator |
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

```
[ r          for r in rows        if r[key] == value ]
  └── 3 ──┘  └──── 1 ────┘        └────── 2 ───────┘

1. for r in rows           ->  go through the records one at a time, calling each one r
2. if r[key] == value      ->  ...but only bother with the ones where this is true
3. r                       ->  ...and for those, put the WHOLE RECORD in the new list
```

Two things to be clear about, because they are the two things students get wrong:

- **What goes in the new list is `r` — the whole record**, not one field. Last week the comprehension said `r["runs"]` and gave you a list of numbers. This week it says `r` and gives you a list of records. **Filtering does not change what a row is; it changes how many rows there are.**
- **`==`, not `=`.** One equals sign assigns; two ask a question. The student has known this since Week 5. Getting it wrong here gives `SyntaxError: invalid syntax` with the caret sitting on the `=`.

Why is the key passed in as an argument, rather than written into the function? Because then the same function works on any table you will ever build. `filter_by(squad, "team", "Tigers")` and `filter_by(playlist, "genre", "pop")` are the same function. **That is Week 12's lesson — write the tool, not the one-off — arriving one level up**, and it is worth saying out loud when they type it.

For a filter that is not an exact match — greater than, less than — you write the comprehension directly, because there is no single value to pass:

```python
big_scores = [r for r in squad if r["runs"] > 50]
```

### 3. The counting dictionary — the one pattern to memorise

This is the most reused four lines in this entire course. Learn it well enough to write it from memory, because you will.

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

And it fails, immediately, on the very first row:

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

**Neither of those crashed.** That is the whole point. `max(counts)` looks at the *keys* — the team names — and returns the one that comes last alphabetically. `Tigers` beats `Owls` beats `Hawks` beats `Falcons` as words, and the counts are never consulted. It is a confident, wrong, silent answer.

`max(counts, key=counts.get)` says: *go through the keys, and for each one, judge it by what `counts.get` says about it.* Now the numbers decide.

**And there is a second thing hiding here that you should plan to discuss.** Falcons and Tigers both have 4. It is a **tie**, and `max` does not tell you — it just returns the first one it met, which is Falcons because Falcons was typed first. So the honest answer to "which is the biggest team?" is *"Falcons and Tigers, four each"*, and the code as written cannot say that. Do not fix it in code today. **Just make the student notice that the program gave a single answer to a question with two answers.** That is a better lesson than a fix.

(A student who remembers Level 1 may recognise this: it is the same "slippery thing" as a tie in a baseline. Say so if they get there.)

### 7. The sting: an average hides how many rows it came from

Here is the output the whole lab is built to produce:

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

All three are professional. What is *not* acceptable is printing `Owls 104.00` next to `Falcons 35.50` with no counts, because a reader will conclude the Owls are four times better at batting, and they will be reasoning correctly from what you showed them.

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

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print workbook pages 15.1–15.6.**
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
- [ ] Workbook 15.1–15.3 out, 15.4–15.6 held back.
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

New file `lab15.py`:

```python
"""lab15.py - asking the twelve records six questions."""

from records import filter_by, column
from squad_data import squad

tigers = filter_by(squad, "team", "Tigers")
print("Tigers rows:", len(tigers), "of", len(squad))
print("Tigers     :", column(tigers, "name"))
```

**Ask before running:** "Two lines out. How many Tigers, and who?"

Run it. Real output:

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

Add the call in `lab15.py`:

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

### Setup

**On the table:** the four card piles from the Hook, still in their piles. The four bucket labels. A calculator. Workbook page 15.3. The blank landscape answers sheet.

**On the answers sheet, before anything else:** write the minimum group size the student chose in the Concept segment, in a box, at the top. `MIN_GROUP = 3` or whatever they said. **It has to be up there before the answers appear.**

### The rules

1. **Every answer is written with its row count.** No exceptions, including the easy ones. `5 of 12`, not `5`.
2. **After every `group_count`, add the buckets up** and check against `len(rows)`.
3. **The minimum group size was decided first** and does not move once the answers are visible.
4. **No answer gets a verdict before it gets a number.** If they say "the Owls are best" before computing it, say: "Might be. Count it."

### The six questions

The complete file. Add to `lab15.py`.

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

```
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

Add to the bottom of `lab15.py` — or make it a separate `honest.py`:

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

Real output:

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
| **No error, the buckets add up to 11** | Nothing is wrong as far as Python is concerned. | A row has a stray space or a different capital in the group field — `"Tigers "` and `"Tigers"` are two different buckets. | `print(counts)` and read the keys. Two nearly-identical keys is the tell. (Cleaning this properly is Week 24.) |
| **No error, an average of 104.00 from one row** | Nothing is wrong as far as Python is concerned. | Nothing. The arithmetic is correct. **This is the dangerous one.** | Print the row count beside every average, and set a minimum group size before you look at the answers. |

### How to teach debugging without giving the answer

The four moves stand — read the last line, find the line number, say the complaint in your own words, then compare characters. This week adds two:

5. **"Which `File` line is the last one?"** That is where it broke. With two files in play, students read the first `File` line, go to `lab15.py`, find nothing wrong, and get stuck for five minutes. One question fixes it forever.
6. **"Do the buckets add up?"** This is the move for errors that produce no message. Three of the twelve rows in the table above have no error message at all, and this check catches two of them.

And the sentence for this week, which is the harder half of debugging:

> **"Half the mistakes this week don't produce an error message. `max(counts)` gives a wrong answer politely, and an average of one row is arithmetically perfect. The check is not 'did it run?' — it is 'does this answer make sense next to its row count?'"**

---

## ❓ Questions Students Ask This Week

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

It helps with a different problem, not this one. The median (the middle value, from your Week 12 toolkit) is more robust when one enormous value drags the average around — the Hawks' 55.67 is pulled up hard by Omar's 90, and their median of 55 is arguably more representative. But **no summary statistic can rescue a group of one.** The median of a single value is that value, exactly like the mean. The problem is not which average you chose; it is that there is nothing to average.

**"How many rows do you need before an average means anything?"** *(Nobody fully agrees, and here is why.)*

**There is no number, and anybody who gives you one without asking questions first is guessing.** It is worth being straight with a 12-year-old about this, because the temptation is to invent a rule and pretend it is a fact.

What everyone agrees on: **one row is not an average**, and it should never be printed next to real averages without a warning. Two is barely better. Beyond that, the honest answer is *it depends*, on three things:

*How spread out the values are.* If every Falcon scores between 34 and 36, then three of them tell you a great deal. If they score 5, 12, 48 and 77, then four of them barely tell you anything, because the next Falcon could be anywhere. **Spread, not count, is what actually decides how much you know** — and measuring spread properly is Week 26 and 27.

*What the answer will be used for.* An average used to decide which snack to buy for a party can rest on very little. An average used to decide who gets picked for a team, or who gets extra help in maths, needs far more — not because the maths changes, but because **the cost of being wrong lands on a person.**

*Whether the rows were picked fairly.* A hundred rows chosen badly can be worse than five chosen well. If all hundred of your Falcons are the four who bat first, your average tells you about opening batters, not about Falcons — and no amount of extra rows fixes a wrong selection.

People who do statistics for a living argue about thresholds constantly, and the honest position is that it is a judgement about consequences and spread, not a fact about arithmetic. What you can *always* do, and what this whole lesson is training, is the easy half: **print the row count next to the answer, and decide your minimum before you look at the results.** Then the reader gets to make the judgement too, which is the most honest thing available to you.

---

## ⚠️ Where This Lesson Goes Wrong

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

### If the student is struggling

**Cut:** `sorted` and the key function completely. Q6 can be answered by looking at the printed table.

**Cut:** `max(counts, key=counts.get)`. They can read the biggest count off the printed dictionary with their eyes, which is honestly what most people do.

**Cut:** three of the six questions. Keep Q1, Q3 and Q5.

**Give them `group_count` already written.** The understanding lives in the hand-trace, not in the typing. Trace it on paper with the cards, five turns minimum, then hand them the finished function and have them *use* it.

**Reteach — with the piles and the calculator.** This whole lab works on a table with no computer at all. Four piles. Count each. Add the counts, check twelve. Total each pile's runs with the calculator. Divide by the pile size. **Write every answer as `<number> from <n> players`, in that exact format, every time.** That format is the objective. A student who leaves the room writing answers in that shape has had a successful lesson whether or not any Python ran.

**The copy-this-exactly scaffold.** Two files. This runs:

`records.py`:

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

`lab15.py`:

```python
from records import filter_by, group_count
from squad_data import squad

print(group_count(squad, "team"))

tigers = filter_by(squad, "team", "Tigers")
print(len(tigers), "Tigers of", len(squad))
```

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

```
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

**Say this:**

> "Your own twelve records, your own two tools, six answers — and one sentence that I care about more than the other six things put together. About an hour.
>
> **First, the tools.** Page 15.4. Write `filter_by()` and `group_count()` into your own `records.py`, and **the key goes in as an argument** — not hard-coded to `genre` or `team` or whatever your column is called. If your function only works on your own table, you have written an answer. I want a tool.
>
> **Second, six questions.** Page 15.5. Point them at the twelve records you built last week. Here they are: how many rows in each category; which category has the most; how many rows are above some number you choose; the average of one number column for one category; that same average for **every** category; and your top three rows sorted by one number.
>
> **And every single answer gets its row count.** Not '183 plays'. **'183 plays, from 5 songs.'** Every one, including the ones where it feels silly. I will hand back a page that is missing one.
>
> **Also print the sum check.** After you group, add the buckets up and print that they come to the number of rows you started with. One line. It is the cheapest way there is of knowing you have not lost anything.
>
> **Third, one sentence.** Page 15.6. **Which of your six answers do you trust least, and why?** Not 'they're all fine'. Pick one. If one of your categories has only one or two rows in it, that is almost certainly your answer, and I want you to say so in your own words — and then tell me what you would do about it."

**Workbook pages:** 15.1, 15.2, 15.3 in class · **15.4, 15.5, 15.6** at home.

**Expected time:** 15 min writing the two tools · 25 min on the six questions · 10 min on the sum check and tidying the output · 10 min on the trust sentence. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** two things, in this order. **One — is the key an argument?** A `group_count(rows)` with `"genre"` written inside the function is the defect that matters, because Week 16 imports these tools and points them at a CSV. **Two — does every answer carry its row count?** That is the habit this whole week exists to build, and it is much easier to insist on now than in Week 34 when there are a hundred rows and a deadline.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 15.1 — Filter or group?

*For each question, say whether it is a filter or a group, and what the answer's shape is.*

| # | Question | Filter or group? | What comes back |
|---|---|---|---|
| (a) | "Show me the Tigers." | filter | a smaller list of records — 4 of them |
| (b) | "How many players per team?" | group | a dictionary, one key per team |
| (c) | "Who scored more than 50?" | filter | a smaller list of records — 5 of them |
| (d) | "How many players got out, and how many didn't?" | group | a dictionary with two keys, `True` and `False` |
| (e) | "What's the Hawks' average?" | filter, then arithmetic | one number — and it needs its row count |
| (f) | "Which team is biggest?" | group, then `max` | one key — and it cannot express a tie |

**15.1(g) What is the one thing a filter changes, and the one thing it never changes?**
It changes **how many rows** you have. It never changes **what a row is** — every record that comes out still has all of its labels and all of its fields. Five cards out of twelve are still cards.

**15.1(h) After `tigers = filter_by(squad, "team", "Tigers")`, what does `len(squad)` say?**
`12`. Still twelve. `filter_by` builds a **new** list; it does not touch the original. This is worth running rather than believing.

### Page 15.2 — Trace the counting dictionary

*Trace `group_count(squad, "team")` by hand for the first six records. Fill in the table.*

| Turn | record | `bucket` | `counts.get(bucket, 0)` | `counts` afterwards |
|---|---|---|---|---|
| 1 | Asha | `Falcons` | `0` (never seen) | `{'Falcons': 1}` |
| 2 | Ravi | `Falcons` | `1` | `{'Falcons': 2}` |
| 3 | Nita | `Falcons` | `2` | `{'Falcons': 3}` |
| 4 | Sam | `Falcons` | `3` | `{'Falcons': 4}` |
| 5 | Kabir | `Tigers` | `0` (never seen) | `{'Falcons': 4, 'Tigers': 1}` |
| 6 | Meera | `Tigers` | `1` | `{'Falcons': 4, 'Tigers': 2}` |

**Final result after all twelve:** `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}`

**15.2(a) Add the four counts up. What should the total be, and why does it matter?**
4 + 4 + 3 + 1 = **12**, which is `len(squad)`. It matters because grouping is supposed to put *every* row in exactly one bucket. If the total came to 11, one row went somewhere you did not expect — most likely into a fifth bucket you never noticed, because its team field had a stray space or a different capital.

**15.2(b) What does `counts.get(bucket, 0)` do the first time a bucket is seen, and every time after?**
The first time, there is no such key, so it hands back the fallback `0` — and `0 + 1` is `1`. Every time after, the key exists, so it hands back the count so far, and one more gets added. One expression, both cases, no `if` needed.

**15.2(c) Predict, then run: what happens with `counts[bucket] += 1` instead?**

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

Because `+=` means "take what is there and add one", and on the first Falcon there is nothing there.

**15.2(d) This traceback has two `File` lines. Which one is where the program broke, and what is the other one for?**
The **last** one — `records.py, line 19` — is where it broke. The one above it, `lab15.py, line 10`, is where the function was *called from*. Together they are a trail of who called who, and you read it from the bottom.

### Page 15.3 — The six questions

Full working file and its real output are in *The Activity, In Full* above. The six answers:

| Q | Question | Answer | Row count |
|---|---|---|---|
| 1 | players per team | `{'Falcons': 4, 'Tigers': 4, 'Hawks': 3, 'Owls': 1}` | 12 of 12 accounted for |
| 2 | biggest team | `Falcons, with 4 players` — **but it is a tie with Tigers** | 4 of 12 |
| 3 | scored more than 50 | `['Nita', 'Kabir', 'Iqbal', 'Omar', 'Priya']` | 5 of 12 |
| 4 | Falcons average | `35.50 runs` | from 4 players |
| 5 | average per team | Falcons 35.50 · Tigers 33.50 · Hawks 55.67 · **Owls 104.00** | 4 · 4 · 3 · **1** |
| 6 | top three | Priya 104 · Omar 90 · Nita 77 | 3 of 12 |

**Hand checks — do at least one of these with the student:**

```
Falcons:  48 + 12 = 60 · 60 + 77 = 137 · 137 + 5 = 142 · 142 / 4 = 35.5     ✔
Tigers:   63 + 30 = 93 · 93 + 0 = 93 · 93 + 41 = 134 · 134 / 4 = 33.5       ✔
Hawks:    55 + 22 = 77 · 77 + 90 = 167 · 167 / 3 = 55.666... = 55.67        ✔
Owls:     104 / 1 = 104.0                                                    ✔
Total:    142 + 134 + 167 + 104 = 547 = sum of the whole runs column         ✔
```

That last line is a free cross-check worth pointing out: **the four group totals add back up to the whole-column total**, which means no row was counted twice or missed.

**15.3(a) Q2 says Falcons. Is that the whole truth?**
No. Falcons and Tigers both have four players, so the honest answer is *"Falcons and Tigers, four each"*. `max` returned Falcons because Falcons was typed first, and `max` has no way to report a tie. The number is not wrong; the answer is incomplete.

**15.3(b) Which of the six answers do you trust least, and why?**
**Q5's Owls line.** `104.00 runs from 1 player` is arithmetically perfect and useless as an average: it is Priya's individual score with a division by one applied to it. Printed beside the Falcons' 35.50 it invites the reader to conclude the Owls are three times the batting side, which is not something the data can support.

**15.3(c) What are the three defensible things to do about it?**
Print it with the row count next to it and let the reader judge. Print it with an explicit warning. Or do not print the average at all and report "Owls: 1 player, too few to average". What is not defensible is printing `104.00` beside `35.50` with no counts.

**15.3(d) Why must the minimum group size be decided before you see the answers?**
Because a rule chosen afterwards is a rule chosen to produce the answer you already wanted. If you look first and *then* decide that groups under three do not count, you have not applied a standard — you have removed a number you did not like, and you will not even notice you did it.

### Page 15.4 — Your two tools

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

**The two things to mark, in this order:**

1. **Is `key` an argument?** `def group_count(rows):` with `"genre"` written inside the body is the defect that matters. Send it back — Week 16 imports these functions and points them at a CSV, and a hard-coded key will break it.
2. **Does `group_count` use `.get(bucket, 0)`?** A four-line `if bucket in counts: ... else: ...` version is **completely correct** and should get full marks. Say so, and then show the one-line version beside it as the reason `.get()` exists.

Everything else — variable names, docstrings, whether `column` exists at all — is theirs.

### Page 15.5 — Six answers, six row counts

The student's dataset is theirs. Model answer on the twelve-song playlist from Week 14:

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

**Hand checks:**

```
pop:    120 + 300 = 420 · +95 = 515 · +180 = 695 · +220 = 915 · 915 / 5 = 183.0   ✔
rock:   45 + 210 = 255 · +130 = 385 · 385 / 3 = 128.333... = 128.33               ✔
folk:   60 + 75 = 135 · +40 = 175 · 175 / 3 = 58.333... = 58.33                   ✔
indie:  65 / 1 = 65.0                                                             ✔
Counts: 5 + 3 + 3 + 1 = 12 = len(playlist)                                        ✔
```

**Mark:** every answer carries a row count; the sum check is printed and correct; `Q3` uses a condition comprehension rather than `filter_by` (an exact-match function cannot do "greater than", and noticing that is worth a tick).

### Page 15.6 — The answer you trust least

**15.6(a) Which of your six answers do you trust least, and why?**

Model answer for the playlist above:

> *"Q5's indie line. It says indie songs average 65 plays, but there is only one indie song in my playlist, so that is just Kite Season's play count divided by one. Next to pop's 183 from five songs it makes indie look unpopular, and I have no idea whether indie songs are unpopular — I have one of them."*

**Full marks needs three things:** which answer, **the row count**, and **what a reader would wrongly conclude**. An answer that says only "the indie one because it's small" has two of the three; ask for the third out loud.

**15.6(b) What would you do about it?**
Any of the three defensible options, stated clearly: print it with the count, print it with a warning, or do not print it. **Extra credit for a fourth answer that some students find:** *collect more indie songs.* That is often the genuinely right answer and it is worth saying so — the problem is not the arithmetic, it is that there is not enough data yet, and no amount of clever code fixes that.

**15.6(c) Write the one sentence you would put at the top of your six answers.**
Model answer: *"All of these come from 12 songs, and every average below has the number of songs it came from printed next to it — the indie figure comes from a single song and should not be compared with the others."*

**This sentence is the whole point of the week.** Mark it properly. A student who can write it will produce an honest capstone in Week 35.

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
