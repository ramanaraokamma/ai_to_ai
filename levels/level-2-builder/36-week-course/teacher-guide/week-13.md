# Week 13 — Labels Instead of Numbers: Dictionaries

[⬅ Week 12](week-12.md) · [Course Home](../README.md) · [Week 14 ➡](week-14.md) · [Student Guide](../student-guide/week-13.md) · [Workbook](../workbook/week-13.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one new container, met four ways |
| **Big idea** | A dictionary looks things up **by name** instead of by position, which is what you want the moment a thing has fields. |
| **New vocabulary** | dictionary · key · value · key-value pair · `KeyError` |
| **New syntax** | `{"key": value}` · `player["key"]` · `player["new"] = v` · `player.get("k", 0)` |
| **Materials** | 5 blank index cards (or A4 cut into six) · a pen · printed workbook pages 13.1–13.6 · the student's Bug Log notebook · a pencil |
| **Tech needed** | Laptop with Python 3 and the editor from Week 0. Nothing installed this week — no numpy, no pandas. A complete paper version is in the Prep Checklist if the laptop dies. |
| **Prep time** | 15 minutes the night before · 5 minutes on the day |

> **⚠️ Watch out:** the square brackets in `player["runs"]` look exactly like the square brackets in `scores[2]` from Week 11, and they do **not** mean the same thing. This is the single biggest confusion of the week and §*What YOU Need to Know First* deals with it head-on. Read that bit even if you skip everything else.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build a dictionary** with five keys and read a value back out by naming its key.
2. **Add a new key and overwrite an existing one**, and say out loud that the two are the same keystroke — Python decides which happened by looking at whether the key was already there.
3. **Use `.get()` with a fallback** so that a missing key returns a value of their choosing instead of stopping the program.
4. **Read a `KeyError` traceback** and name the three usual causes: a typo, a plural, a capital letter.
5. **Say when filling a missing number with `0` is a quiet lie**, using an example where the invented zero changes an average.

Observable evidence: a file on screen that prints five player cards; a `KeyError` traceback pasted into the Bug Log with the fix written underneath in the student's own words; and a spoken answer to "what did the made-up zero do to the average?"

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to know any Python to teach this lesson.** Everything below is written for somebody who has never programmed. Read it once, type the code in the Prep Checklist once, and you will be ahead of the student.

### 1. The problem this week solves

Last week the student built a toolkit that worked on a list of numbers. A list looks like this:

```python
scores = [45, 12, 88, 0, 103]
```

That is a row of numbered boxes. Box 0 holds 45, box 1 holds 12, and so on. To get a number out you count along: `scores[4]` is 103.

Here is the question a list cannot answer: **who scored the 103?**

Somebody did. The number is sitting right there. But a list of numbers stores only numbers, and a number does not remember whose it was, or what day it was, or which ground. All of that was thrown away the moment the list was typed.

What the student needs is a container where the boxes have **names on them** instead of numbers. That container is called a dictionary.

> **Dictionary** — a container that stores pairs. You give it a name (the *key*) and it hands you back the thing stored under that name (the *value*).

The name "dictionary" comes from a paper dictionary: you do not count to word 4,912, you look up "volcano". Programmers also call this a *map*, a *hash*, or an *associative array*. You will only ever say **dictionary**, and in code it is spelled `dict`.

### 2. Every line of this week's first program, explained

This is the whole of `cards.py`. Seven lines. I will explain each one as if you had never seen a program.

```python
# cards.py - one cricketer, stored as a dictionary

# Asha's whole innings, written on one card.
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}

print(asha)              # the whole card, all five labelled fields
print(asha["name"])      # look up ONE field by its label
print(asha["runs"])      # the label is "runs", not "the third one along"
print(len(asha))         # how many labelled fields are on the card
```

**Line 1 and line 3 — the `#` lines.** Anything after a `#` is a *comment*. Python ignores it completely. It is a note for the human. The student has been writing these since Week 1.

**Line 4 — the dictionary itself.** This is the only genuinely new line. Take it apart from the outside in:

- `asha =` means *"make a box named `asha` and put the following thing in it."* The student has done this since Week 2. Nothing new.
- `{ ... }` — **curly braces**. On most keyboards, hold Shift and press the `[` and `]` keys. Curly braces are how Python knows "this is a dictionary". Square brackets `[ ]` would make a list instead.
- Inside the braces are five **pairs**, separated by commas. Each pair is written `key: value` — a name, a colon, then the thing.
- `"name": "Asha"` is one pair. The key is the text `name`. The value is the text `Asha`.
- `"runs": 48` is another. The key is `runs`; the value is the number 48.

> **Key-value pair** — one name-and-thing couple inside a dictionary. `"runs": 48` is one pair.

Notice which things have quotes and which do not. **Keys have quotes because they are text.** Values have quotes only when the value is itself text. `48` and `32` are numbers, so no quotes. `True` is Python's word for yes, so no quotes.

If you read line 4 aloud the way a human would, it says: *"Asha's card. Under `name` is Asha, under `runs` is 48, under `balls` is 32, under `team` is Falcons, and under `out` is yes."*

**Line 6 — `print(asha)`.** Prints the whole dictionary. Python shows it back to you like this:

```text
{'name': 'Asha', 'runs': 48, 'balls': 32, 'team': 'Falcons', 'out': True}
```

Two things to notice, because a student will ask both. Python prints text with **single** quotes even though you typed double quotes — the two are interchangeable in Python and it just prefers single ones when printing. And the pairs come back **in the order you typed them**. That has been guaranteed since Python 3.7 and you can rely on it.

**Line 7 — `print(asha["name"])`.** This is the lookup. `asha["name"]` means *"go to the dictionary called `asha` and hand me whatever is stored under the label `name`."* It prints `Asha`.

**Line 9 — `print(len(asha))`.** `len` means length. For a list it was "how many slots". For a dictionary it is **how many pairs**, which is 5. Not 10 — a pair counts once, not twice.

### 3. The one thing that confuses everybody: square brackets do two jobs

The student has met square brackets before, in Week 11:

```python
scores[2]        # give me slot number 2 of this LIST
```

Now they meet:

```python
asha["runs"]     # give me the value stored under the label "runs" in this DICTIONARY
```

Same brackets. Completely different question. Here is the way to say it that works:

> **The brackets mean "look inside this thing". What goes in the brackets tells you how you are looking — a number means count, a word in quotes means read the label.**

Two consequences worth having ready:

- `scores["two"]` is meaningless — a list has no labels. Python raises `TypeError: list indices must be integers`.
- `asha[0]` is meaningless *for this dictionary* — there is no key called `0`. Python raises `KeyError: 0`. (Strictly, a dictionary is *allowed* to have a number as a key. We never do it in this course, and you should not raise it unless a student does.)

If the student says "so how do I know which one it is?", the answer is: **look at how the container was made.** Square brackets when it was built → list. Curly braces with colons → dictionary. That is the only tell, and it is enough.

### 4. Adding and changing are the same keystroke

```python
asha["runs"] = 51            # the key ALREADY exists -> this CHANGES the value
asha["ground"] = "Pune"      # the key is NEW -> this ADDS a sixth field
```

Run it and you get:

```text
51
{'name': 'Asha', 'runs': 51, 'balls': 32, 'team': 'Falcons', 'out': True, 'ground': 'Pune'}
6
```

There is no `add` command and no `change` command. You assign to a key, and **Python looks to see whether that key was already there.** If it was, the old value is replaced and gone. If it was not, a new pair is created on the end.

Why this matters for teaching: it means a **typo silently creates a new field instead of changing the one you meant.**

```python
asha["Runs"] = 51
```

That does not fix Asha's runs. It quietly gives her a sixth field called `Runs` while `runs` still says 48. No error, no warning, wrong answer. Say this out loud in the lesson; it is the reason capital letters matter so much this week.

### 5. Why a name beats a position — the demo that lands

This one is worth typing yourself, because it is the argument for the whole week.

```python
# Four facts about Asha's innings, as a plain list.
asha_list = ["Asha", 48, 32, "Falcons"]
print("by position:", asha_list[1], "runs")     # slot 1 is the runs

# The same four facts, as a dictionary.
asha_dict = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons"}
print("by name    :", asha_dict["runs"], "runs")

# Now the scorer decides to record the ground, and writes it in SECOND.
asha_list = ["Asha", "Pune", 48, 32, "Falcons"]
asha_dict = {"name": "Asha", "ground": "Pune", "runs": 48, "balls": 32, "team": "Falcons"}

print("by position, after the insert:", asha_list[1], "runs")   # WRONG, and silent
print("by name, after the insert    :", asha_dict["runs"], "runs")   # still right
```

Real output:

```text
by position: 48 runs
by name    : 48 runs
by position, after the insert: Pune runs
by name, after the insert    : 48 runs
```

Look at the third line. The program cheerfully reports **"Pune runs"**. Nothing crashed. Nobody was warned. Somebody added a field at the front and every position after it shifted by one, and the program that counted to slot 1 is now reading the wrong thing forever.

> **The point to say out loud:** positions shift when the data changes shape. Names do not. That is the entire reason dictionaries exist.

![Counting shifts, names do not](../figures/fig-w13-2-lookup-by-name-not-position.svg)
*Figure 13.1 — The same five values and the same insert. On the left the answer changed and no error message appeared.*

### 6. `KeyError` — the crash of the week, and its three causes

Ask a dictionary for a key it does not have and Python stops the program:

```python
print(asha["Runs"])
```

```text
Traceback (most recent call last):
  File "cards.py", line 8, in <module>
    print(asha["Runs"])
          ~~~~^^^^^^^^
KeyError: 'Runs'
```

> **`KeyError`** — the error Python raises when you ask a dictionary for a key it does not have.

Teach the student to read it **from the bottom up**, exactly as in Week 1:

1. **Last line first.** `KeyError: 'Runs'` — the word in quotes is the key Python could not find. Python is not being vague. It is naming the exact thing you asked for.
2. **Then the line number.** `line 8` — that is where you asked.
3. **Then the `~~~^^^` marks**, if your Python is 3.11 or newer. The `^` marks sit under the exact part of the line that failed. On Python 3.10 or older you get the same message without them; nothing is missing that matters.

There are three causes, and between them they account for almost every `KeyError` a beginner ever sees:

| Cause | What it looks like | Real key |
|---|---|---|
| **A typo** | `asha["rusn"]` | `runs` |
| **A plural** | `asha["ball"]` or `asha["run"]` | `balls`, `runs` |
| **A capital letter** | `asha["Runs"]`, `asha["Name"]` | `runs`, `name` |

Make the student say the three out loud. In the activity they will produce a real one, and then you ask "which of the three was it?"

### 7. `.get()` — asking politely

Sometimes a missing key means your data is broken and you *want* the program to stop. Sometimes a missing key is completely normal and you have a sensible answer ready. For the second case there is `.get()`:

```python
# the card, fresh again — earlier in the lesson you changed runs to 51,
# so re-make it here and this block stands on its own
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}

print(asha.get("runs", 0))       # the key IS there -> you get the real value
print(asha.get("catches", 0))    # the key is NOT there -> you get your fallback, 0
print(asha.get("catches"))       # no fallback given -> Python hands back None
print(asha["runs"])              # square brackets: the real value, or a crash
```

```text
48
0
None
48
```

| You write | Key is there | Key is missing |
|---|---|---|
| `asha["runs"]` | hands back the value | 💥 `KeyError`, program stops |
| `asha.get("runs")` | hands back the value | hands back `None` |
| `asha.get("runs", 0)` | hands back the value | hands back `0` |

`None` is Python's word for "nothing here". The student met it in Week 10, when a function with no `return` handed back `None`.

**The rule of thumb to teach:** use `["key"]` when a missing key means somebody has made a mistake and you want to hear about it loudly. Use `.get("key", something)` when a hole is expected and you have an honest answer for it.

### 8. The quiet lie — where the maths of Level 1 comes back

This is the part of the lesson that is not about Python at all, and it is the part that matters most.

Sam batted. The scorer's pen died. Nobody wrote his runs down. So Sam's card is missing the `runs` field, and a program that says `sam.get("runs", 0)` will report that **Sam scored zero**.

Sam did not score zero. Nobody knows what Sam scored. Those are different facts and the fallback has quietly turned one into the other. Here is what it costs:

```python
# The four Falcons: Asha 48, Ravi 12, Nita 77, Sam ???
average_if_sam_scored_zero = (48 + 12 + 77 + 0) / 4    # we INVENTED a 0 for Sam
average_leaving_sam_out    = (48 + 12 + 77) / 3        # we said "we don't know"

print(f"Falcons average if Sam 'scored 0': {average_if_sam_scored_zero:.2f}")
print(f"Falcons average leaving Sam out  : {average_leaving_sam_out:.2f}")
print(f"The 0 we made up moved the answer by "
      f"{average_leaving_sam_out - average_if_sam_scored_zero:.2f} runs")
```

```text
Falcons average if Sam 'scored 0': 34.25
Falcons average leaving Sam out  : 45.67
The 0 we made up moved the answer by 11.42 runs
```

**Eleven and a half runs**, invented by one keystroke, with no error message. The student met exactly this idea in Level 1 as *"out of how many?"* — a number with no denominator is not an answer. Say the connection out loud; they will remember Level 1 better than you expect.

The honest rule:

> **A fallback is fine when it is a fact. It is a lie when it is a guess wearing a fact's clothes.**
>
> - Missing `catches` for a player nobody watched in the field → `0` is probably honest, because we would have noticed a catch.
> - Missing `runs` because the pen died → `0` is a lie. Leave the row out, and say how many rows you left out.

![A fallback is a value you invented](../figures/fig-w13-3-get-with-fallback.svg)
*Figure 13.2 — The yes branch gives you something somebody measured. The no branch gives you something you typed.*

### 9. The three misconceptions you will actually meet

**Misconception 1 — "a dictionary is in alphabetical order."**
It is not, and the name is misleading. A dictionary keeps the pairs **in the order you typed them**, and nothing sorts them. If a student expects `balls` to come before `name`, show them `print(asha)` and count the pairs off against the line they typed. (Python 3.6 and earlier really did scramble the order, which is where this belief comes from. Do not mention that unless asked.)

**Misconception 2 — "`asha[0]` should give me the first pair."**
It will not; it raises `KeyError: 0`. A dictionary has no first, second or third. It has labels. The fix in their head is not "use the right number", it is "there are no numbers here". This one is worth catching early because it is a hangover from Week 11 and it is *reasonable*.

**Misconception 3 — "`.get()` fixed the bug."**
`.get()` never fixes a bug. It stops the program from complaining about one. If the key is missing because you typed `"Runs"`, `.get("Runs", 0)` will happily report zero runs forever and never mention it again. Say this exactly:

> "`.get()` is a decision, not a repair. If you don't know why the key is missing, you are not ready to give it a fallback."

### 10. How deep to go, and where to stop

**Go this far:** build a dictionary; read a value by key; add a key; overwrite a key; `len()`; `.get()` with and without a fallback; read a `KeyError`; the honesty question about zero.

**Stop before all of these — they belong to later weeks and pre-empting them makes next week's lesson flat:**

| Do not teach today | Where it lives |
|---|---|
| `.items()`, `.keys()`, `.values()`, looping over a dictionary | **Week 14** |
| `"runs" in asha` as a test | **Week 14** — but see the note in Homework; the student meets it once, tonight |
| A **list of dictionaries** (a table) | **Week 14.** This is the big one. Resist it hard. |
| Filtering and grouping records | **Week 15** |
| Saving to a CSV file | **Week 16** |
| A dictionary inside a dictionary | Not in this course at all; Level 3 |
| `del asha["out"]`, `.pop()`, dict comprehensions | Not in this course |

If a student asks "could I put all five players in one thing?" — that is exactly next week's question and it is a wonderful thing to have asked. Write their name and the date in the margin, say "that is Week 14 and you got there a week early", and do not answer it.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print workbook pages 13.1–13.6.**
- [ ] **Cut five index cards** (or A4 into six). Write nothing on them yet — the student writes them.
- [ ] **Type and run the code yourself.** Not read — typed. Make a file called `cards.py` in the course folder and put exactly this in it:

```python
# cards.py - one cricketer, stored as a dictionary

# Asha's whole innings, written on one card.
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}

print(asha)              # the whole card, all five labelled fields
print(asha["name"])      # look up ONE field by its label
print(asha["runs"])      # the label is "runs", not "the third one along"
print(len(asha))         # how many labelled fields are on the card
```

Then run it with `python3 cards.py`. You must see **exactly** this:

```text
{'name': 'Asha', 'runs': 48, 'balls': 32, 'team': 'Falcons', 'out': True}
Asha
48
5
```

- [ ] **Now break it on purpose.** Change line 8 to `print(asha["Runs"])` — capital R — and run it again. You must see a `KeyError`. Read the last line. Change it back. **Do this yourself before you do it in front of a child.**
- [ ] **Read §5 and §8 above** (names beat positions; the quiet lie). Those are the two bits you will be asked "why?" about.
- [ ] Have the Bug Log page open in the student's notebook.

### 5 minutes on the day

- [ ] Editor open on the course folder, with the `.venv` interpreter selected. A terminal open in the same folder.
- [ ] Five blank cards and a pen on the table, to your left.
- [ ] `cards.py` **deleted or renamed** — the student types it from scratch. If you leave your copy there they will read it instead of typing it, and typing it is the lesson.
- [ ] Workbook pages 13.1–13.3 out, 13.4–13.6 kept back for homework.

### Fallback if the laptop or the install fails

**This week has a complete paper version and it is genuinely good.** Everything except the traceback can be done on cards.

1. Do the whole card activity below with pen and paper (25 minutes of real work).
2. For the `KeyError`, use the card physically: hold up a card and ask for "Asha's *Runs*, capital R". The correct response is *"there is no field called Runs on this card"* — which is precisely what `KeyError: 'Runs'` means. Have the student write the traceback out by hand from this file into the Bug Log, and label the three parts (last line, line number, caret marks).
3. Set the typing as the homework instead, and let the workbook pages carry the rest.

| If this fails | Do this instead |
|---|---|
| No laptop at all | The card version above. Nothing essential is lost except live tracebacks; copy one by hand from §6. |
| Python is installed but the editor will not open | Run from the terminal with any text editor, even Notepad or TextEdit in plain-text mode. `python3 cards.py` works the same. |
| The student's file is called `dict.py` and imports break weirdly | Rename it. Python found *their* file where a library was expected. Delete the `__pycache__` folder beside it. Standing rule all year. |
| They cannot find the curly brace key | On a UK/US keyboard it is Shift plus the two keys to the right of `P`. On some layouts it needs AltGr. Find it together **before** the live-code segment — losing four minutes to a keyboard hunt kills the momentum. |
| Everything works but they are two lines behind and panicking | Stop dictating. Wait. Let them catch up in silence. Never read ahead of the slowest typist. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Who Scored the 103? | 7 | 7 | Last week's list cannot answer an obvious question |
| 🧠 Concept — Boxes With Labels On | 16 | 23 | Cards on the table; keys, values, pairs; why names beat counting |
| 💻 Live-Code Together — `cards.py` | 18 | 41 | They type it. Two deliberate mistakes, both fixed in front of them |
| 🎲 Their Turn — Five Cards, One Crash | 20 | 61 | Five players typed as dictionaries; a planted `KeyError`; the quiet zero |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Who Scored the 103? (7 minutes)

**Do this:** Open last week's file, or just write the list on paper where they can see it. Say nothing about dictionaries yet.

```python
scores = [45, 12, 88, 0, 103, 7, 61, 34, 90, 22]
```

**Say this:**

> "This is what you built last week. Twenty cricket scores — here's ten of them — and your toolkit could tell me the total, the average, the biggest and the smallest. That was real work and it works.
>
> So I've got one more question for it. Look at the 103. Somebody scored a hundred and three. **Who?**"

Wait. Let them look. There is nothing to find.

> "You can't tell me, can you. And it isn't because you've forgotten. It's because the list never knew. When you typed `103`, the number went in and everything else about it fell on the floor — who it was, what day it was, which ground, whether they were out. Gone.
>
> Ask your toolkit anything you like about *numbers* and it's brilliant. Ask it anything about the *person* and it has nothing at all."

**Do this:** Put one blank index card on the table between you. Slide the pen across.

> "So we're going to stop storing numbers, and start storing **things**. Write me one card about one cricketer. Five facts. Name, runs, balls, team, and whether they got out. Write the label on the left and the fact on the right, like a form."

Let them write it. Do not correct the layout. When they finish, pick it up and hold it so they can see it.

> "Right. Now — what are Asha's runs?"

They read it off. Instantly.

> "Notice what you just did. You did **not** count to the second thing on the card. You looked for the word 'runs' and read what was next to it. That's the whole lesson. Today you're going to teach Python to do that.
>
> And it has a name that is slightly annoying, because it has nothing to do with spelling. It's called a **dictionary**."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Who scored the 103?" | You can't tell — the list doesn't store names. | If they guess a name, say: "You might be right. Can you *prove* it from the list?" They cannot. That is the point. |
| "How did you find Asha's runs on the card so fast?" | I read the label. | If they say "it was near the top" — press once: "If I'd written the five facts in a different order, would you still have found it?" Yes. Because of the label. |
| "Why not just always remember that runs is the second thing?" | Because you'd have to remember it for every kind of card, forever, and it changes if anyone adds a field. | If they say "it's easy to remember" — agree, then say: "It is, for one card. Come back to me at thirty cards with eight fields each." |

---

### 🧠 Concept — Boxes With Labels On (16 minutes)

**Do this:** Keep the card in view the whole time. Write on the board or a sheet, in this order.

**Say this — part 1, the three words:**

> "Three words, and then we type. Here's the card." *(hold it up)*
>
> "Every line on it is a **pair** — a label and a fact. The label is called the **key**. The fact is called the **value**. Together they're a **key-value pair**."

Write these three, in a box, and leave them up all lesson:

> **key** — the label you look something up by. In this course a key is always a word in quotes.
> **value** — the thing stored under that label. A number, a word, a yes/no — anything.
> **key-value pair** — one label-and-fact couple. `"runs": 48` is one pair.

> "Your card has five pairs on it. Count them. Five labels, five facts."

![One card, five labelled fields](../figures/fig-w13-1-dict-labelled-card.svg)
*Figure 13.3 — Five key-value pairs on one card. The pink boxes are the labels you chose; the blue boxes are the data.*

**Say this — part 2, how you write it in Python:**

> "Python writes a card with **curly braces**. Not the square brackets you used for lists last week — curly ones. Find them on your keyboard now: hold Shift and press the two keys just right of the P.
>
> Inside the braces you write the pairs. A label in quotes, then a **colon**, then the fact, then a **comma** before the next pair. Like this."

Write it out slowly, saying each character:

```python
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}
```

> "Read it back to me in English."

Their answer should sound like: *"Asha's card: under name is Asha, under runs is 48, under balls is 32, under team is Falcons, under out is yes."* Accept any version with the words "under" or "the label" in it.

> "One thing to notice, because it catches everybody. **The labels always have quotes.** They're words. The facts have quotes only if the fact is itself a word. `48` is a number, so no quotes. `Falcons` is a word, so quotes. `True` is Python's own word for yes, so no quotes and a capital T."

**Say this — part 3, getting a fact back out:**

> "To read one fact, you name the label:"

```python
asha["runs"]
```

> "Say that out loud as English: *'in Asha, the runs'*. Not 'Asha bracket runs'. **'In Asha, the runs.'**
>
> Now — and this is the bit I need you to be suspicious about — those are the same square brackets you used last week for `scores[2]`. Same symbol. Different question. Last week the brackets meant *count along to slot 2*. Today they mean *read the label*. The brackets only ever mean 'look inside this thing'. **What you put in them tells you how you're looking: a number means count, a word in quotes means read the label.**"

**Say this — part 4, why we are bothering:**

> "Here's why this is worth learning instead of just remembering that runs is the second thing." *(Take a fresh card and copy their card onto it, but write the ground in as the second line.)*
>
> "Same player. Same facts. But the scorer decided to record the ground as well, and wrote it in second. Now: on this new card, what is the second thing?"

The ground.

> "Right. So if I'd written a program that said 'the runs are the second thing', that program now confidently tells me Asha scored *Pune*. It doesn't crash. It doesn't warn me. It just quietly answers the wrong question forever.
>
> Now ask the label question on the new card. What are Asha's runs?"

48.

> "Still 48. **Counting shifts when the data changes shape. Labels don't.** That's it. That's the reason dictionaries exist and you can stop wondering."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "In `"runs": 48`, which is the key and which is the value?" | `runs` is the key, 48 is the value. | If they swap them, point at the card: "which one is the label you wrote on the left?" |
| "Why does `48` have no quotes but `Falcons` does?" | 48 is a number; Falcons is text. | If they say "you forgot them" — good, honest answer. Reply: "Fair. What happened in Week 2 when you put quotes round a number?" It stopped being a number. |
| "How many pairs on the card? What will `len` say?" | Five, and 5. | If they say 10 (counting labels and facts separately) — recount pointing at whole lines. A pair is one line. |
| "`scores[2]` and `asha["runs"]` — same brackets. What's different?" | One counts, one reads a label. | If they cannot say it, give them the sentence and have them repeat it: "a number means count, a word means read the label." |
| "Could I ask for `asha[0]`?" | No — there's no label called 0. | Do not just say no. Say: "Try it in a minute and read what Python says." It says `KeyError: 0`, which is the honest answer. |

---

### 💻 Live-Code Together — `cards.py` (18 minutes)

**You never touch the keyboard.** You read a line out loud, they type it, and before every single run you ask "what do you think it will print?" That question is the lesson; the typing is just how it gets in.

Here is the exact keystroke sequence. Keep it in this order.

**Step 1 (2 min).** New file, saved as `cards.py` in the course folder.

Dictate exactly:

```python
# cards.py - one cricketer, stored as a dictionary

# Asha's whole innings, written on one card.
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}

print(asha)
```

Say the punctuation out loud as you dictate: *"curly brace… quote name quote… colon… quote Asha quote… comma…"* Do not speed up. When a 12-year-old types a dictionary literal for the first time it takes about ninety seconds and that is normal.

**Ask before running:** "What comes out?"
Hoped-for: *the whole card*. If they say "Asha" — good guess, wrong, and much better than not guessing.

Run it. Real output:

```text
{'name': 'Asha', 'runs': 48, 'balls': 32, 'team': 'Falcons', 'out': True}
```

> **Say this:** "Look — Python printed it with single quotes even though you typed double ones. It just prefers singles when it talks back. And notice the pairs came out in the order you typed them. That's guaranteed; you can rely on it."

**Step 2 (3 min).** Add three lines:

```python
print(asha["name"])
print(asha["runs"])
print(len(asha))
```

**Ask before running:** "Three more lines. Tell me all three answers before we run it."
Hoped-for: `Asha`, `48`, `5`.

Run it. Real output (all four lines now):

```text
{'name': 'Asha', 'runs': 48, 'balls': 32, 'team': 'Falcons', 'out': True}
Asha
48
5
```

**Step 3 — ⚠️ FIRST DELIBERATE MISTAKE (4 min).** This is planned. Do not warn them.

> **Say this:** "Right. I want the runs, but I'm going to type it the way a person actually types it, with a capital R because it's a name of a thing. Change that line to a capital R."

They type:

```python
print(asha["Runs"])
```

**Ask before running:** "Prediction?"
Most students predict 48. Let them.

Run it. Real output:

```text
Traceback (most recent call last):
  File "cards.py", line 8, in <module>
    print(asha["Runs"])
          ~~~~^^^^^^^^
KeyError: 'Runs'
```

> **Say this:** "Oh good, an error. Right — **last line first.** Read me the last line."
>
> *`KeyError: 'Runs'`*
>
> "So what's Python telling you? It's not being vague. It's not saying 'something went wrong'. It's saying: **you asked me for a key called `Runs`, and there is no key called `Runs`.** And it's completely correct. Look at your own line 3. What did you call it?"
>
> *`runs`, small r.*
>
> "`Runs` and `runs` are two different labels as far as Python is concerned, in exactly the way that `Asha` and `asha` are two different words. There is no key called `Runs` on this card, so there is nothing to hand you, so it stops.
>
> And see those little `^` marks under the line? Those point at the exact bit that failed. Python is being as helpful as it knows how." *(If your Python is 3.10 or older there will be no `^` marks. Say so and move on — nothing is missing that matters.)*

**Do this:** Have them fix it to lowercase and run again. It prints `48`.

Then **the Bug Log entry, right now, while it is warm.** Three columns in their notebook: the error message, what it meant in their own words, what fixed it. Something like: *`KeyError: 'Runs'` · I asked for a label that isn't on the card · changed R to r.*

> **Say this:** "There are three reasons you'll ever see a `KeyError`, and I want you to be able to say all three. A typo. A plural — `ball` instead of `balls`. And a capital letter. Which was yours?"

![Read the last line, change one letter, run again](../figures/fig-w13-4-keyerror-pinned.svg)
*Figure 13.4 — The last line names the key it could not find. Nothing else in the traceback is as useful.*

**Step 4 — ⚠️ SECOND DELIBERATE MISTAKE (3 min).** Also planned.

> **Say this:** "Now take the quotes off. Just `asha[runs]`, no quotes. Feels tidier, doesn't it."

```python
print(asha[runs])
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "cards.py", line 8, in <module>
    print(asha[runs])
               ^^^^
NameError: name 'runs' is not defined. Did you mean: 'round'?
```

> **Say this:** "Different error. Read the last line. `NameError: name 'runs' is not defined.`
>
> That's a different complaint entirely. `KeyError` meant 'that label isn't on the card'. `NameError` means 'I've never heard of that word at all'. Without the quotes, Python didn't think `runs` was a label — it thought it was a **variable**, a box with a name on it, like the boxes you made in Week 2. And there is no box called `runs`. So it says so.
>
> The quotes are what turn a word into a label. Take them off and Python goes looking for a box instead.
>
> Also — look what it guessed. *Did you mean 'round'?* It's trying to be helpful and it's completely wrong. Python's suggestions are guesses. Read them, don't obey them."

Put the quotes back. Run it. `48`.

**Step 5 (3 min).** Add a key, change a key.

```python
asha["runs"] = 51
print(asha["runs"])
asha["ground"] = "Pune"
print(asha)
print(len(asha))
```

**Ask before running:** "Two of those lines look identical. One changes something and one adds something. Which is which, and how does Python know?"
Hoped-for: `runs` already exists so it changes; `ground` is new so it adds. Python knows by looking.

Run it. Real output:

```text
51
{'name': 'Asha', 'runs': 51, 'balls': 32, 'team': 'Falcons', 'out': True, 'ground': 'Pune'}
6
```

> **Say this:** "Six pairs now. And here's the sting in that: if I'd typed `asha["Runs"] = 51` with a capital R, Python wouldn't have crashed at all. It would have quietly given Asha a *sixth* field called `Runs` while `runs` still said 48. No error. Wrong answer. That's why the capital letters matter so much."

**Step 6 (3 min).** `.get()`.

```python
print(asha.get("catches", 0))
print(asha.get("catches"))
```

**Ask before running:** "There's no `catches` on this card. We just saw that asking with square brackets crashes. What do you think `.get` does?"

Run it. Real output:

```text
0
None
```

> **Say this:** "`.get` asks politely. With a fallback, you get the fallback. Without one, you get `None` — Python's word for 'nothing here', which you met in Week 10.
>
> Now, careful. `.get` did **not** fix anything. It just decided what to say when the answer is missing. If the reason `catches` is missing is that I typed it wrong, `.get` will cheerfully tell me zero catches for the rest of my life and never mention it. **`.get` is a decision, not a repair.**"

---

### 🎲 Their Turn — Five Cards, One Crash (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–5:** write the five index cards by hand. Physical first.
- **Minutes 5–14:** type all five as dictionaries in `scorecard.py` and print them as lines.
- **Minutes 14–18:** the planted `KeyError`, read and fixed, logged.
- **Minutes 18–20:** the quiet zero, and the question about Sam.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** five blank index cards, a pen, the laptop, workbook page 13.2, the Bug Log open.

**On screen:** an empty file called `scorecard.py`.

![Five cards, one set of labels](../figures/fig-w13-5-five-cards-same-labels.svg)
*Figure 13.5 — What finished looks like, and the one defect to hunt for: a capital letter on one card's label.*

### Step 1 — Write the cards by hand (5 minutes)

Five cricketers. **Every card gets exactly the same five labels, in the same order.** That rule is not fussiness; it is the whole reason next week works.

| name | runs | balls | team | out |
|---|---|---|---|---|
| Asha | 48 | 32 | Falcons | yes |
| Ravi | 12 | 20 | Falcons | yes |
| Nita | 77 | 55 | Falcons | no |
| Kabir | 63 | 41 | Tigers | yes |
| Meera | 30 | 28 | Tigers | no |

Now do the drill that makes the point, out loud, fast:

> "Asha's runs." — 48.
> "Kabir's team." — Tigers.
> "Meera's balls." — 28.
> "Ravi's *Runs*, capital R." — *there's no such label on the card.*

That last one is the `KeyError`, done with hands. Say so: **"Hold on to that answer. Python says exactly the same thing, in five words."**

### Step 2 — Type all five as dictionaries (9 minutes)

The complete file. `out` becomes `True`/`False` — Python's words for yes and no, from Week 5.

```python
# scorecard.py - five cricketers, five labelled fields each

# Each card is one dictionary. Every card uses the SAME five keys.
asha  = {"name": "Asha",  "runs": 48, "balls": 32, "team": "Falcons", "out": True}
ravi  = {"name": "Ravi",  "runs": 12, "balls": 20, "team": "Falcons", "out": True}
nita  = {"name": "Nita",  "runs": 77, "balls": 55, "team": "Falcons", "out": False}
kabir = {"name": "Kabir", "runs": 63, "balls": 41, "team": "Tigers",  "out": True}
meera = {"name": "Meera", "runs": 30, "balls": 28, "team": "Tigers",  "out": False}

def card_line(player):
    """Turn one player dictionary into one tidy line of text."""
    strike_rate = player["runs"] / player["balls"] * 100   # runs per 100 balls
    return f"{player['name']:<6}{player['team']:<9}{player['runs']:>4} runs  SR {strike_rate:6.1f}"

print("=" * 44)
print(card_line(asha))
print(card_line(ravi))
print(card_line(nita))
print(card_line(kabir))
print(card_line(meera))
print("=" * 44)

# A field that nobody wrote on the cards.
print("Asha's catches:", asha.get("catches", 0))     # 0, and no crash
print("Asha's runs   :", asha.get("runs", 0))        # the real 48
```

Real output:

```text
============================================
Asha  Falcons    48 runs  SR  150.0
Ravi  Falcons    12 runs  SR   60.0
Nita  Falcons    77 runs  SR  140.0
Kabir Tigers     63 runs  SR  153.7
Meera Tigers     30 runs  SR  107.1
============================================
Asha's catches: 0
Asha's runs   : 48
```

**Three things to say while they type:**

1. `card_line` is a function with a parameter, from Week 10. Nothing new. What *is* new is that the thing being passed in is a whole card, not one number — **one argument, five facts**. That is the payoff.
2. The strike rate is Week 3 arithmetic and Week 3 formatting: `runs / balls * 100`, printed with `:6.1f`. That means *six characters wide, one decimal place*. The same colon controls the widths on the other fields too: **`:<6` means "six characters wide, pushed left"** and **`:>4` means "four wide, pushed right"**. Left for words, right for numbers — which is why the 48 and the 12 have their units sitting under each other. It is all the same mini-language as Week 3's `:.2f`; you are only using more of it.
3. ⚠️ **The quote juggling.** The f-string is wrapped in double quotes, so inside the braces the key must use **single** quotes: `{player['name']}`. This is the number one typo of the whole month. If you use double quotes inside on Python 3.10 or 3.11 you get `SyntaxError: f-string: unmatched '['`. On Python 3.12 and newer it happens to work — which is worse, because it will break the day they run their file on a different machine. **Teach single quotes inside, always.**

### Step 3 — The planted `KeyError` (4 minutes)

**Say this:** "Add one line at the bottom. Ask for Ravi's runs — but type it the way you'd write it on a form, with a capital R."

```python
print(ravi["Runs"])
```

Real output:

```text
Traceback (most recent call last):
  File "scorecard.py", line 29, in <module>
    print(ravi["Runs"])
          ~~~~^^^^^^^^
KeyError: 'Runs'
```

Now run the four-question routine, and make them answer each one before you move on:

1. "Which line does Python say?" — line 29.
2. "Read me the last line." — `KeyError: 'Runs'`.
3. "In English, what is it telling you?" — *there is no label called `Runs`.*
4. "Which of the three usual causes was it — typo, plural, or capital letter?" — capital letter.

Fix it. Log it. Then do it once more, their choice of cause, and have them predict the message before running. A student who can predict a traceback has understood it.

### What "finished" looks like

- Five cards on the table, all with the same five labels in the same order.
- `scorecard.py` runs and prints five aligned lines plus the two `.get()` lines.
- At least one real `KeyError` traceback in the Bug Log with the fix written in the student's own words — **their** words, not yours.
- The student can point at `asha["runs"]` and at `scores[2]` and say what is different about the brackets.
- The student can say, unprompted, what the invented zero did to the Falcons' average.

### Variation — easier

- **Three cards, not five.** Asha, Ravi, Kabir. Nothing is lost.
- **Three keys, not five.** `name`, `runs`, `team`. Drop `balls` and `out`, and drop `card_line` entirely — just `print(asha["name"], asha["runs"])` five times. The lesson is the labelled lookup, not the formatting.
- **Give them the first dictionary to copy character for character**, then have them do the rest by pattern. Copying one line exactly is a legitimate scaffold; copying all five is not.
- If curly braces are defeating them, type the braces yourself *once*, out loud, then hand back the keyboard. That is the one keystroke I will let you take.

### Variation — harder

1. **Predict the traceback.** They write, on paper, the exact three lines Python will print for `nita["Team"]` — before running it. Then run it and compare word for word. Getting the wording right is real understanding.
2. **The silent typo.** Have them type `asha["Balls"] = 40` and then `print(asha)` and `print(len(asha))`. Ask: "did anything go wrong? How would you ever know?" *(Six pairs instead of five, and two nearly-identical labels. Nothing crashed.)* This is a genuinely unsettling result and worth five minutes.
3. **Which fallback is honest?** Give them four missing fields and ask, for each, whether `.get(field, 0)` is a fact or a guess: `catches` (nobody was watching the field), `runs` (the pen died), `balls` (the ball counter was on their phone), `out` (the match is still going). *(Only the first is defendable, and even that is arguable. See the Questions section.)*
4. **A card that isn't a person.** "Make a dictionary for something that isn't a cricketer, with five keys, and don't tell me what it is. I'll guess from the keys." Good answers: a pizza order, a bus route, a phone.

---

## 🐞 The Debugging Clinic

Every message below was produced by running a broken version of this week's actual code. The tracebacks are copied verbatim.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `KeyError: 'Runs'` | "You asked for a key called `Runs`. There is no key called `Runs`." | A capital letter. `Runs` and `runs` are different labels. | Match the spelling on the line where the dictionary was built, character for character. |
| `KeyError: 'ball'` | Same thing, different key. | A plural. The key is `balls`. | Scroll up to the dictionary and read the real key. Do not guess. |
| `KeyError: 0` | "There is no key called `0`." | Reaching for a dictionary the way you reach into a list. | A dictionary has labels, not positions. Use `asha["name"]`. |
| `NameError: name 'runs' is not defined. Did you mean: 'round'?` | "I've never heard of the word `runs` at all." | The quotes were left off: `asha[runs]`. Python looked for a *variable* called `runs`. | Put the quotes back: `asha["runs"]`. Ignore the "did you mean" — it is a guess and it is wrong. |
| `TypeError: 'dict' object is not callable` | "You tried to *run* the dictionary like a function." | Round brackets instead of square: `asha("runs")`. | Square brackets for looking inside. Round brackets are for calling functions. |
| `SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='?` | Python could not even read the line. | An `=` instead of a `:` inside the braces: `{"name" = "Asha"}`. | Colons inside a dictionary, always. `=` belongs outside, where you name the box. |
| `SyntaxError: invalid syntax` with the caret under the middle of the line | Python could not read the line. | A **missing comma** between two pairs: `{"name": "Asha" "runs": 48}`. | One comma between every pair. Count them: five pairs needs four commas. |
| `AttributeError: 'dict' object has no attribute 'Get'. Did you mean: 'get'?` | "Dictionaries can't do `Get`." | A capital G on `.get`. | Lowercase: `.get`. Here the "did you mean" **is** right — but check it, don't trust it. |
| `TypeError: can only concatenate str (not "int") to str` | "You tried to glue a number onto some text with `+`." | `asha["name"] + " scored " + asha["runs"]` — runs is a number. | Use an f-string: `f"{asha['name']} scored {asha['runs']}"`. Or `str(asha["runs"])`. Same error as Week 2's `"5" + 5`. |
| `SyntaxError: f-string: unmatched '['` | Python got lost inside your f-string. | Double quotes inside a double-quoted f-string: `f"{asha["runs"]}"`. | Single quotes inside: `f"{asha['runs']}"`. **Note:** Python 3.12+ accepts the double-quoted version. Teach single quotes anyway, or their file breaks on the next machine. |
| No error, but a field appears twice with different capitals | Nothing went wrong as far as Python is concerned. | `asha["Runs"] = 51` created a *new* key instead of changing `runs`. | `print(asha)` and read the keys. Then `print(len(asha))` — if it went up when you expected it to stay put, you made a new field. |

### How to teach debugging without giving the answer

Four moves, in this order. Do not skip to move 3 because you are in a hurry.

1. **"Read me the last line."** Out loud, all of it, including the bit in quotes. About half of all beginner errors are solved by this alone, because the last line names the exact thing that is wrong.
2. **"What line number?"** Then: "put your finger on that line." Not your finger — theirs.
3. **"Say what Python is complaining about, in your own words."** If they cannot, the problem is comprehension, not the code, and *that* is what you should be teaching for the next two minutes.
4. **Only now**, and only if all three failed: "compare that word to the line where you built the dictionary. Character by character. Out loud."

Two things to say every single week, until they say them for you:

> **"Oh good, an error."** Mean it. An error is Python telling you exactly where it stopped and why, which is enormously more useful than a wrong answer with no complaint.
>
> **"The error message is not the enemy. The silent wrong answer is."** `asha["Runs"] = 51` never complains, and that is the dangerous one.

---

## ❓ Questions Students Ask This Week

**"Why is it called a dictionary if it isn't in alphabetical order?"**

Because of what you *do* with a paper dictionary, not how it is arranged. When you look up "volcano" you do not count to word 4,912 — you go straight to the word. That is the resemblance: you fetch by name. The alphabetical ordering of a paper dictionary is just how paper solves the finding problem; Python solves it a different way, and keeps your pairs in the order you typed them. Other languages call the same thing a map, a hash or an associative array, which are all better names and none of which caught on in Python.

**"Can the value be another dictionary?"**

Yes, and it is very useful, and we are not doing it in this course. A value can be a number, some text, a `True`/`False`, a list, or another dictionary. Once you nest them you need two lookups to reach a value and the errors get much harder to read, so it waits until you have a real reason. If a student asks because they *have* a real reason, let them try it and be ready for a `KeyError` that names the inner key rather than the outer one.

**"What if two keys are the same?"**

The later one wins and the earlier one silently vanishes. `{"runs": 48, "runs": 51}` gives you a dictionary with one pair in it, `runs: 51`, and `len()` says 1. No error. This is worth doing live — it is a good five-second demonstration that a dictionary cannot hold the same label twice, which is exactly what you want from a card.

**"Is `asha["runs"]` faster than `scores[2]`?"**

Practically, no, and for anything you will write this year the difference is invisible. Looking up a key does a little arithmetic on the text of the key to work out where to look, so it is not "searching" the way you would search a shelf — it goes more or less straight there, however many pairs there are. Counting to slot 2 in a list is a shade quicker still. Neither will ever be the reason your program is slow.

**"Can I use a number as a key?"**

Yes: `{1: "Asha", 2: "Ravi"}` is a legal dictionary and `d[1]` gives `"Asha"`. We never do it in this course, for a good reason: it looks exactly like a list index and makes the confusing thing more confusing. If a student does it by accident, the tell is a `KeyError: 0` where they expected the first item.

**"Why not just use variables? `asha_runs = 48`, `asha_balls = 32`…"**

You can, for one player. Try it for thirty and the problem becomes obvious: you cannot write one piece of code that works for all of them, because every variable has a different name and your program has to mention each one by hand. With a dictionary you write `player["runs"]` once and it works for whoever you hand it. That is the whole argument, and next week it becomes overwhelming.

**"What should a missing number be filled with?"** *(Nobody fully agrees, and here is why.)*

**This is a genuine open argument among people who do this for a living, and it is not a dodge to say so.** There are three defensible answers and they conflict.

*Fill it with zero.* Everything downstream keeps working — sums, averages, charts. The cost is that you have invented a fact. Sam's missing runs become "Sam scored 0", the Falcons' average drops from 45.67 to 34.25, and nothing anywhere warns you.

*Leave it as nothing (`None`).* You have told the truth: the value is unknown. The cost is that every piece of code that touches that column now has to cope with a hole, and if you forget one, it crashes — possibly months later.

*Refuse to run at all until somebody fixes the data.* The purest option. The cost is that real data always has holes, so a program that refuses to run on imperfect data refuses to run.

Which one is right depends entirely on **what the number is and what happens if you are wrong**. A missing "number of catches" filled with zero is probably harmless. A missing rainfall reading filled with zero says "it did not rain", which you do not know, and could end up in a flood model. A missing test score filled with zero says a child failed. Same keystroke, wildly different consequences.

What everybody *does* agree on, and what you should insist on all year: **whatever you fill in, write down that you filled it in, and how many.** An answer that says "average 45.67 runs, from 3 of the 4 players — Sam's card was blank" is honest. The same number with no note is not. That habit is the whole of Week 23 and 24, and it starts today.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| They write `asha[0]` and get `KeyError: 0`, and conclude dictionaries are broken | It is a completely reasonable transfer from Week 11. Lists worked that way six days ago. | Do not correct it, *demonstrate* it. Hold up the card: "point at field zero." They cannot — there is no field zero, there are five labels. Then: "Python said exactly that." |
| The capital-letter `KeyError` is fixed by them without reading the message | They spotted the difference visually and just retyped it | Fine that it works; not fine as a habit. Make them go back and say the last line out loud anyway. Then plant a *plural* error, which is much harder to spot by eye, and watch them need the message. |
| Curly braces cannot be found and four minutes evaporate | Keyboard layouts vary and nobody has told them | Find the key together **in the Prep, before the lesson**, on their actual keyboard. If it is genuinely awkward (some AltGr layouts), type the braces yourself once and hand the keyboard straight back. |
| The f-string with double quotes inside works on their machine | They are on Python 3.12 or newer, where it is legal | Say the true thing: "That runs here and it will break on a school computer running an older Python. Use single quotes inside and it works everywhere." Show them the `SyntaxError` from this file so they recognise it later. |
| `.get()` becomes their default, and real typos get silently buried | `.get()` never crashes, and not crashing feels like winning | Say the line and keep saying it: **"`.get()` is a decision, not a repair."** Then set the rule: `.get()` only when you can say out loud *why* the key might be missing and *why* your fallback is honest. Otherwise square brackets, and let it crash. |
| The invented zero gets shrugged at — "it's only a bit different" | 34.25 and 45.67 are both just numbers on a screen | Make it concrete and personal. "Your class average on a test is 45.67. One person was off sick, so the school records them as 0. Now it's 34.25. Which number goes in the report? Which one is true?" That version lands. |
| They want all five players in one thing, now | Because it is the obviously right idea and they have spotted it | Celebrate it loudly and refuse it. "That is Week 14 and you got there a week early — write your name and today's date next to it." If you give it to them today you will spend next week teaching something they already half-know badly. |
| Everything works, and they are bored by minute 40 | Five cards of typing is repetitive if the idea landed at minute 20 | Jump straight to Variation-harder item 2 (the silent typo). It is genuinely surprising and it will occupy a fast student for ten minutes. |
| A comma goes missing and the `SyntaxError` points somewhere baffling | Python notices the problem at the *next* thing it reads, not where the comma should have been | Teach the rule instead of the fix: "when a `SyntaxError` points at something that looks fine, look at the line **above** and the character **before**." Then count: five pairs, four commas. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the `card_line` function and the strike rate entirely. Print with plain `print(asha["name"], asha["runs"])`. The f-string formatting is Week 3 revision and it is not what today is for.

**Cut:** two of the five keys. `name`, `runs`, `team` is a complete dictionary.

**Reteach — do it with the cards, not the screen.** The concept lands physically almost every time. Lay out the five cards. You call a label; they read the value. Then take one card away and ask for a field that is not on it — that is `.get()` versus `KeyError`, done with hands. Only go back to the keyboard when the card version is fast and confident.

**The copy-this-exactly scaffold.** Give them this on paper and have them type it character for character, then change only the words in bold to their own:

```python
player = {"name": "Asha", "runs": 48, "team": "Falcons"}
print(player["name"])
print(player["runs"])
print(player["team"])
```

Three keys, three lookups, nothing else. When that runs, add one more key on a new line and print it. Then stop. **A student who can build a three-key dictionary and read all three values back has met this week's objective 1 and 2.** That is a good lesson.

**One thing you must not cut:** the `KeyError`. Even if they type nothing else all lesson, they must see one real `KeyError`, read the last line out loud, and say what it means. That is the skill that carries into every remaining week of the year.

### If the student is flying

No new syntax needed for any of these.

1. **Predict the traceback, word for word.** Before running, they write all three lines Python will print for `nita["Team"]`. Compare character by character. Getting the wording exactly right is a real and rare skill.
2. **The silent typo hunt.** Give them a file where somebody has typed `"Balls"` on one card and `"balls"` on the other four. Nothing crashes. Their job: find it using only `print(player)` and `len(player)`, and then write one sentence on why this is worse than a crash.
3. **Make the fallback lie.** "Here are Asha 48, Ravi 12, Nita 77. Add a fourth player whose `runs` key is missing. Now compute the average two ways — filling with zero, and leaving them out. Which is bigger? By how much? Which would you put in a report, and what sentence would you write next to it?"
4. **Design the card.** "You're building a school's lost-property system. What five keys? Now — which of your five keys would you be uncomfortable emailing to a stranger?" (Almost always the one naming the child.) This is Level 1's privacy work arriving in code, and it is a superb ten minutes.
5. **Two cards, one label.** "Both Nita and Omar have a key called `runs`. Are those the same label?" *(Same word, different dictionaries. A key is only a label inside its own dictionary — which is precisely why next week's table works.)*

### If the student won't engage today

**Do the cards and nothing else.** Do not open the laptop.

Five index cards, five labels each, and then play **"Read Me the Label"**: you name a player and a field, they read it back, as fast as they can, twenty in a row. Then you start slipping in the impossible ones — *"Ravi's catches"*, *"Meera's Runs with a capital R"*, *"Asha's field number two"* — and every time the honest answer is **"that isn't a label on this card"**, which is the definition of `KeyError` in the student's own mouth.

That game delivers objectives 1 and 4 completely, takes twelve minutes, needs no electricity, and is a legitimately good lesson. The typing is not going anywhere; `scorecard.py` can be next week's warm-up and Week 14 will be stronger for having the cards already written.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — build and read (on paper, 90 seconds)**

> "Write me a dictionary called `pizza` with three keys: `size`, `toppings` and `price`. Then write the one line that prints just the price."

*Good answer:*

```python
pizza = {"size": "large", "toppings": 3, "price": 8.5}
print(pizza["price"])
```

**What to accept:** any sensible values; single or double quotes; any order of keys. **What to catch:** square brackets instead of curly ones (that is a list, and it has no labels); `=` instead of `:` inside the braces; missing quotes round the keys.

**Check 2 — read the error (spoken)**

> "I run a program and it says `KeyError: 'Team'`. Tell me two things: what Python is complaining about, and the three usual causes."

*Good answer:* "It's saying there's no key called `Team` in that dictionary. The three causes are a typo, a plural, and a capital letter." Full marks needs **both halves**. If they only say "it's broken", prompt once: "which word is it telling you about?"

**Check 3 — the honesty question (spoken)**

> "A player's card has no `runs` on it because the scorer's pen died. I use `.get("runs", 0)` and the program runs perfectly. What have I just told everybody, and is it true?"

*Good answer:* "You've said they scored zero, and you don't know that. It'll pull the average down." This is the check that separates level 3 from level 4. If they say "it's fine, it didn't crash", ask the follow-up: "Would you be happy if that were your test score?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot build a dictionary without copying. Uses `[0]` to reach into it. Reads a traceback as "it broke" and waits to be told the fix. |
| **2 — Emerging** | Builds a dictionary with help on the braces and colons. Reads a value by key when reminded of the exact spelling. Recognises `KeyError` as being about a key but cannot say which one. |
| **3 — Secure** | Builds a five-key dictionary unaided. Reads values by key. Adds and overwrites keys and can say how Python tells them apart. Reads `KeyError` from the last line up and names which of the three causes it was. **This is the target.** |
| **4 — Strong** | Uses `.get()` with a fallback and can justify the fallback. Explains why `asha["Runs"] = 51` is more dangerous than a crash. Explains what the invented zero did to the average, with the two numbers. |
| **5 — Exceptional** | Predicts a traceback word for word before running it. Argues both sides of the missing-number question and says what it depends on. Sees, unprompted, that the five cards want to live in one container, and can say why the shared keys are what makes that possible. |

---

## 📤 Homework to Assign

**Say this:**

> "Two pages, about an hour, and there's a crash in the middle that I want you to cause on purpose.
>
> **First, five cards in code.** Page 13.4. Five player dictionaries, all five with exactly the same five keys — same spelling, same capitals, same order. Not four keys on one and five on the rest. Identical. That rule is going to matter enormously next week and I'm not telling you why yet.
>
> **Then, break it deliberately.** Page 13.5. Ask one of your players for a field that isn't there. Run it. **Copy the whole traceback into your Bug Log by hand** — all of it, not just the last line — and underneath write, in your own words, what Python was telling you and which of the three usual causes you used.
>
> **Then fix it two different ways.** Same page. Once with `.get()` and a fallback. Once by asking first, with `in`, which is a tool you have not met yet — it is on the page, copy it exactly and it will work; I will explain it properly on Monday. Then write me **one sentence** on which of the two you would actually use, and why. There is no correct answer to that. There is a correct *reason*.
>
> **Last, page 13.6, the honesty page.** Four missing fields, and for each one you say whether filling it with zero is a fact or a guess. One of them is genuinely arguable and I want to hear the argument."

**Workbook pages:** 13.1, 13.2, 13.3 in class · **13.4, 13.5, 13.6** at home.

**Expected time:** 20 min typing the five cards · 15 min on the crash and the two fixes · 15 min on the honesty page · 10 min on the Bug Log entry. **About 60 minutes.**

> **🧑‍🏫 A note on `in`:** `"runs" in player` is formally Week 14's syntax and you have not taught it. It appears once tonight, printed on the page for the student to copy, because the homework needs two genuinely different fixes and `.get()` is the only other one they have. Say plainly that it is next week's tool arriving early. Next week it gets its full explanation, and the student will already have typed it once — which makes that lesson easier, not harder.

---

## 🔑 Answer Key

Every question is restated, so you can mark from this page alone.

### Page 13.1 — What is the key, what is the value?

*For each pair, name the key and the value, and say whether the value is text, a number or a True/False.*

| # | Pair | Key | Value | Kind |
|---|---|---|---|---|
| (a) | `"name": "Asha"` | `name` | `Asha` | text |
| (b) | `"runs": 48` | `runs` | `48` | number |
| (c) | `"out": True` | `out` | `True` | True/False |
| (d) | `"team": "Falcons"` | `team` | `Falcons` | text |
| (e) | `"strike_rate": 150.0` | `strike_rate` | `150.0` | number (a decimal) |

**13.1(f) Why do all five keys have quotes, but only two of the five values do?**
Because the keys are all text — they are words used as labels. A value only needs quotes when the value itself is text. `48` and `150.0` are numbers and `True` is Python's own word for yes, so quotes on any of those would change what they are. `"48"` is the *text* four-eight, and you cannot add it up.

**13.1(g) How many key-value pairs are in `{"a": 1, "b": 2, "c": 3}`, and what does `len()` say?**
Three pairs, and `len()` says `3`. Not 6 — a pair counts once. `len` counts labels, not items of information.

### Page 13.2 — Build it and read it

**13.2(a) Write a dictionary called `asha` with the five fields from your card, then print the whole thing, then print just the runs.**

```python
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}
print(asha)
print(asha["runs"])
```

```text
{'name': 'Asha', 'runs': 48, 'balls': 32, 'team': 'Falcons', 'out': True}
48
```

**Mark:** curly braces; a colon in every pair; a comma between pairs and **not** after the last one (a trailing comma is legal, so do not mark it wrong); quotes on all five keys.

**13.2(b) `scores[2]` and `asha["runs"]` use the same brackets. Write one sentence on what is different.**
Model answer: *"The brackets both mean 'look inside this thing', but a number inside means count along to that slot, and a word in quotes means read the label — so `scores[2]` counts and `asha["runs"]` reads a label."*

**13.2(c) Predict, then run: what does `print(len(asha))` say?**
`5`.

**13.2(d) Predict, then run: what does `print(asha[0])` say?**

```text
Traceback (most recent call last):
  File "cards.py", line 4, in <module>
    print(asha[0])
          ~~~~^^^
KeyError: 0
```

Because there is no key called `0`. A dictionary has labels, not positions. **Mark generously on wording, strictly on the idea.**

### Page 13.3 — Add it and change it

**13.3(a) Starting from Asha's five-key card, change her runs to 51 and add a `ground` of `"Pune"`. Print the dictionary and its length after each step.**

```python
asha = {"name": "Asha", "runs": 48, "balls": 32, "team": "Falcons", "out": True}

asha["runs"] = 51            # the key ALREADY exists -> this CHANGES the value
print(asha["runs"])          # 51, the old 48 is gone

asha["ground"] = "Pune"      # the key is NEW -> this ADDS a sixth field
print(asha)                  # the new pair went on the end
print(len(asha))             # six labelled fields now
```

```text
51
{'name': 'Asha', 'runs': 51, 'balls': 32, 'team': 'Falcons', 'out': True, 'ground': 'Pune'}
6
```

**13.3(b) Both lines are written the same way. How does Python decide whether to change or to add?**
It looks to see whether the key is already there. If it is, the old value is replaced and lost. If it is not, a new pair is created on the end. There is no separate "add" command and no separate "change" command — which is why a typo in a key adds a field instead of changing one.

**13.3(c) What does `asha["Runs"] = 60` do? Does anything go wrong?**
It creates a **new sixth key** called `Runs` with the value 60, and leaves `runs` exactly as it was. Nothing goes wrong as far as Python is concerned: no error, no warning. `len(asha)` goes up by one, and the dictionary now has two nearly identical labels. This is worse than a crash, because a crash tells you where to look.

**13.3(d) What happens if you type the same key twice: `{"runs": 48, "runs": 51}`?**
The later one wins. You get `{'runs': 51}` — one pair — and `len()` says `1`. No error. A dictionary cannot hold the same label twice, which is exactly what you want from a card.

### Page 13.4 — Five cards in code

*Type five player dictionaries with the same five keys, then print three specific facts.*

Model answer (the student's names and numbers will differ; mark the structure):

```python
# hw13.py - Week 13 homework: five cards, one KeyError, two fixes

# --- Part 1: five dictionaries, all with the SAME five keys ------------------
asha  = {"name": "Asha",  "runs": 48, "balls": 32, "team": "Falcons", "out": True}
ravi  = {"name": "Ravi",  "runs": 12, "balls": 20, "team": "Falcons", "out": True}
nita  = {"name": "Nita",  "runs": 77, "balls": 55, "team": "Falcons", "out": False}
kabir = {"name": "Kabir", "runs": 63, "balls": 41, "team": "Tigers",  "out": True}
meera = {"name": "Meera", "runs": 30, "balls": 28, "team": "Tigers",  "out": False}

print(asha["name"], "scored", asha["runs"])
print(kabir["name"], "plays for", kabir["team"])
```

```text
Asha scored 48
Kabir plays for Tigers
```

**Mark hard on one thing only: are the five keys spelled identically on all five cards?** Same words, same capitals. A `Team` on card three is the defect to catch, and it will cost them dearly next week if it survives. Everything else — names, numbers, spacing, order of the five dictionaries — is theirs.

### Page 13.5 — Break it, read it, fix it twice

**13.5(a) Ask one of your players for a field that is not on their card. Paste the whole traceback.**

```python
meera = {"name": "Meera", "runs": 30, "balls": 28, "team": "Tigers", "out": False}
print(meera["catches"])
```

```text
Traceback (most recent call last):
  File "hw13_crash.py", line 2, in <module>
    print(meera["catches"])
          ~~~~~^^^^^^^^^^^
KeyError: 'catches'
```

*(On Python 3.10 or older the `~~~^^^` line is absent. Everything else is identical. Do not mark that as a mistake.)*

**13.5(b) In your own words: what is Python telling you, and which of the three usual causes was it?**
Model answer: *"It's telling me I asked the dictionary for a label called `catches`, and there is no label called `catches` on Meera's card, so it had nothing to hand back and it stopped. It wasn't a typo or a capital letter — I asked for a field that genuinely doesn't exist."*

Accept any wording that contains **the name of the key** and **the idea that it is not there**. Reject "it broke" and "the dictionary is wrong".

**13.5(c) Fix it with `.get()`. 13.5(d) Fix it with `in`. 13.5(e) Which would you use, and why?**

```python
# --- FIX ONE - .get() with a fallback ---------------------------------------
print("Meera's catches (fallback):", meera.get("catches", 0))

# --- FIX TWO - ask first, then look ----------------------------------------
if "catches" in meera:                      # is there a key called "catches"?
    print("Meera's catches (checked):", meera["catches"])
else:
    print("Meera's catches (checked): not recorded")
```

```text
Meera's catches (fallback): 0
Meera's catches (checked): not recorded
```

**13.5(e) — there is no correct answer, only correct reasoning.** Both of these are full marks:

> *"I'd use `.get()` because it's one short line and zero catches is a sensible thing to say about a player nobody watched in the field."*

> *"I'd use the `in` version because it can print 'not recorded', which is the truth. `.get()` has to make something up, and 0 looks like a real measurement."*

**Zero marks** for "the second one, because it's longer" or any answer that does not mention what happens to the *reader* of the output. Push in the margin: "what does somebody reading your output think happened?"

### Page 13.6 — Fact or guess?

*For each missing field, is filling it with `0` a fact or a guess?*

| # | The missing field | Verdict | Why |
|---|---|---|---|
| (a) | `catches` — nobody was watching the fielders | **Arguable, leaning fact** | If a catch had happened, somebody would almost certainly have noticed. So 0 is a reasonable inference. It is still an inference, and it should be noted. |
| (b) | `runs` — the scorer's pen died mid-innings | **Guess** | They batted. They scored something. 0 is a number you invented, and it drags every average down. |
| (c) | `balls` — the ball counter was on somebody's phone | **Guess** | They faced deliveries. 0 balls faced is impossible for someone who batted, and it will make the strike rate divide by zero. |
| (d) | `out` — the match is still going | **Neither — the question is wrong** | `out` is not a number. Filling it with `0` says "not out", which is *true right now* and may be false in four minutes. The honest value is "we do not know yet". |

**13.6(e) One of these four is genuinely arguable. Which, and what is the argument on each side?**
**(a), `catches`.** *For zero:* a catch is a visible, memorable event; if nobody recorded one, almost certainly none happened, so 0 is very likely the true value. *Against zero:* nobody was watching, so we have no evidence either way, and writing 0 turns "no evidence" into "evidence of none". If ten players' catches are all filled with 0 and one of them actually took three, the fielding statistics are now quietly wrong and nothing will ever flag it.

**Full marks needs both sides.** A student who argues only one side has answered half the question — say so, and ask for the other half out loud.

**13.6(f) Write the one sentence you would put next to an average computed from a table with holes in it.**
Model answer: *"Falcons average 45.67 runs, from 3 of the 4 players — Sam's card had no runs on it, so he is not in this number."*

The three things that must be there: **the number**, **how many rows it came from**, and **what was left out**. This sentence is the habit the whole rest of the year is built on; mark it seriously.

### Answers to every question posed in the lesson

- *"Who scored the 103?"* → You cannot tell. A list of numbers stores only numbers; everything else was thrown away when the list was typed.
- *"How did you find Asha's runs on the card so fast?"* → By reading the label, not by counting to a position.
- *"Why not remember that runs is the second thing?"* → Because it stops being true the moment anyone adds a field, and it fails silently when it does.
- *"In `"runs": 48`, which is the key?"* → `runs` is the key; `48` is the value.
- *"Why does 48 have no quotes but Falcons does?"* → 48 is a number; Falcons is text. Quotes round 48 would make it the *text* "48", which cannot be added up.
- *"How many pairs, and what does `len` say?"* → Five pairs; `len` says 5.
- *"`scores[2]` versus `asha["runs"]` — what's different?"* → Both mean "look inside", but a number counts to a slot and a quoted word reads a label.
- *"Could I ask for `asha[0]`?"* → No. `KeyError: 0` — there is no key called `0`.
- *"What will `print(asha)` show?"* → The whole dictionary, in the order you typed it, with single quotes round the text.
- *"Two lines look identical — which adds and which changes?"* → `asha["runs"] = 51` changes, because `runs` already exists. `asha["ground"] = "Pune"` adds, because `ground` is new. Python decides by looking.
- *"There's no `catches` on the card. What will `.get` do?"* → With a fallback, hand back the fallback (`0`). Without one, hand back `None`. Either way, no crash.
- *"Which of the three causes was your `KeyError`?"* → For `asha["Runs"]`: a capital letter. For `asha["ball"]`: a plural. For `asha["rusn"]`: a typo.
- *"Ravi's Runs, capital R — read it off the card."* → There is no label called `Runs` on the card. Which is `KeyError: 'Runs'`, in English.
- *"What did the invented zero do to the average?"* → Moved it from 45.67 runs to 34.25 runs — 11.42 runs of pure invention, with no warning.
- *"Did anything go wrong when you typed `asha["Balls"] = 40`?"* → No error at all. It quietly made a sixth field. `len()` went from 5 to 6, and that is the only clue you get.

---

## 🔮 Next Week Preview

Next week the five cards get stacked. That is genuinely the whole idea: put the five player dictionaries into one list and you have not built something new — **you have built a table**, where one dictionary is one row and the five keys are the five column names. Everything Level 1 taught about tables, rows and columns arrives back in code, and it arrives for free, because the student already typed the hard part today. The new tools are small: `.items()` to walk through one card field by field, `"runs" in player` to ask whether a field exists before reaching for it, a one-line comprehension to pull a whole column out, and `enumerate()` to put a row number beside every row while printing. By the end of next week the student will print a twelve-row table with a numbered header, out of nothing but dictionaries and f-strings, and it will look like something a computer produced.

**Prep early:** three things. **Keep the five index cards** — next week opens by stacking them and fanning them out into a column, and buying new cards is a waste. **Keep `scorecard.py`** on disk; next week's file starts by copying those five dictionaries into a list. And **check the five keys are spelled identically on all five cards**, tonight, before the student's homework hardens the mistake. One card with `Team` instead of `team` will produce a `KeyError` halfway through next week's loop, which is a fine teaching moment if you planned it and a twenty-minute derailment if you did not.

---

[⬅ Week 12](week-12.md) · [Course Home](../README.md) · [Week 14 ➡](week-14.md) · [Student Guide](../student-guide/week-13.md) · [Workbook](../workbook/week-13.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
