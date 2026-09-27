# Week 17 — One Number for Every Score: NumPy Arrays

[⬅ Week 16](week-16.md) · [Course Home](../README.md) · [Week 18 ➡](week-18.md) · [Student Guide](../student-guide/week-17.md) · [Workbook](../workbook/week-17.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — a new kind of container, and the two things you print to understand it |
| **Big idea** | An **array** is a list that knows its shape and does maths to all of its numbers at once. |
| **New vocabulary** | array · numpy · shape · dtype · alias |
| **New syntax** | `import numpy as np` · `np.array([...])` · `arr.shape` · `arr.dtype` |
| **Materials** | Graph paper, or a sheet with a grid drawn on it · a pencil **with a rubber on the end** · the twelve index cards from Week 14 · printed workbook pages 17.1–17.6 · the Bug Log |
| **Tech needed** | Laptop with Python 3 and the editor. **numpy must be installed** — this is the first week all year that needs something installed, and it is the only thing that can eat this lesson. `records.py` and `squad_data.py` from Week 15/16 must still exist. |
| **Prep time** | 20 minutes the night before (15 of them are the install) · 5 minutes on the day |

> **⚠️ Watch out:** install numpy **the night before**, on the machine the student will actually use, and run `import numpy` to prove it. Do not discover a broken install at minute three of the lesson. If it will not install at all, the paper version in the Fallback section is genuinely good — this week's ideas are shape and kind, and both can be taught with a pencil and a rubber.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Import a library under a short alias** and explain what the alias is for.
2. **Build a 1-D and a 2-D array** from numbers typed out by hand.
3. **Read `.shape`** and say what each number in it means.
4. **Read `.dtype`** and explain why an array holds only one kind of number.
5. **Predict the shape of an array before running the code**, and explain any prediction they got wrong.

Observable evidence: `arrays.py`, which builds a 1-D array, a 2-D array and a decimal array and prints `.shape` and `.dtype` for all three; a workbook page with six predictions written *before* any code ran, all six checked, and a written sentence for every miss.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to know any numpy to teach this.** There are two facts in this lesson and they are both things you can print. Read this section once and you will be ahead of the student all lesson.

### 1. What numpy is, and why it exists at all

> **numpy** — a library of tools for working with blocks of numbers. Not part of Python; you install it once and then import it.

Everything the student has built so far is made of Python **lists** and **dictionaries**. Those are wonderfully flexible: a list can hold `[1, "cat", 3.5, True]` — four completely different kinds of thing in four slots — and nobody complains.

That flexibility is not free. To hold four different kinds of thing, a list cannot hold the things themselves; it holds a row of **references** — little notes saying "the thing you want is over there." Every single value in the list is a separate object sitting somewhere else in memory, and each one carries its own label saying what kind of thing it is.

So when you write a loop that doubles every number in a list, the computer does this, per number: follow the note, find the object, ask it what kind of thing it is, work out what doubling means for that kind, do it, make a *new* object to hold the answer, put a note about it in the new list. Six steps, a million times.

An **array** does not work that way.

> **array** — a block of memory holding many values of **one single kind**, laid out end to end with nothing in between.

Because every value is the same kind and therefore the same size, numpy knows exactly where value number 40,000 is without hunting: it is 40,000 slots along from the start. And because they are all the same kind, it does not have to ask about the kind even once — it asks once, at the top, and then does the arithmetic in fast compiled code that Python never touches.

![A list is a cloakroom. An array is an egg box.](../figures/fig-w17-1-list-vs-array.svg)
*Figure 17.1 — The list is more flexible. The array knows more about itself, and that is what buys the speed.*

**The analogy to use in the room, and it is exact.** A Python list is a **cloakroom**: numbered hooks, and on each hook a *ticket*, and the ticket tells you which locker downstairs your coat is in. To count the red coats you take every ticket, walk down, open a locker, look, walk back. A numpy array is an **egg box**: twelve identical slots, twelve eggs, all touching. Counting is glancing.

**How much faster, honestly?** For a million numbers, roughly twenty times. But here is the thing to tell the student, and it is true: **the speed is not why we are learning this.** The speed matters when you have a million numbers, and they have twelve. The reason we are learning it is that next week `celsius * 9 / 5 + 32` will replace four lines of loop with one line that says what it means — and that every model in this course, and every model in Level 3, and the giant language models in Level 4, all do their arithmetic exactly this way. **Learn to think in arrays now and everything after it is easier.**

### 2. The alias, and why everybody uses the same one

```python
import numpy as np
```

> **alias** — a shorter name you give something so you can type it more often.

That is the whole of it. `import numpy` on its own works perfectly, and then you write `numpy.array(...)` every time. `as np` means "and from now on, in this file, `np` means numpy."

**Two things worth saying out loud:**

- It is a *nickname within this file only*. It changes nothing about numpy itself, and another file can call it something else. It is exactly Week 12's `from stats import mean` idea — a naming decision, made by you, at the top of the file.
- **Everybody writes `np`.** Not `numpy`, not `numby`, not `n`. This is a convention, not a rule, and it is worth following anyway, because it means every numpy example on the internet reads like your code and yours reads like theirs. Conventions are how strangers cooperate.

If a student wants to write `import numpy as banana`, it will work. Let them try it once, laugh, and then say the real reason to write `np`.

### 3. Building an array

Only one way in, this week: you hand `np.array()` a **list**.

```python
import numpy as np

runs = np.array([48, 12, 77, 5])
print(runs)
```

```text
[48 12 77  5]
```

Two things to notice about that output, and the student will spot both:

- **There are no commas.** A printed array uses spaces, not commas. A printed list uses commas. That is the fastest way to tell at a glance which one you are looking at, and it is worth pointing out.
- **The columns are lined up.** `5` is printed as ` 5` with a space in front, so it lines up with `48`. numpy does that on purpose, because arrays are for looking at in rows and columns.

**The mistake everyone makes once**, and you are going to plant it: forgetting the brackets.

```python
runs = np.array(48, 12, 77, 5)
```

```text
Traceback (most recent call last):
  File "arrays.py", line 7, in <module>
    runs = np.array(48, 12, 77, 5)           # four scores... or so we hope
TypeError: array() takes from 1 to 2 positional arguments but 4 were given
```

Python is saying: *I was expecting one thing and you gave me four.* `np.array` wants **one list**, not four numbers. This is Week 10's parameters lesson arriving in a new place: the function has a fixed number of slots, and you handed it too many things.

For a 2-D array — a block with rows and columns — you hand it a **list of lists**, one inner list per row:

```python
table = np.array([
    [48, 32],                            # Asha:  runs, balls
    [12, 20],                            # Ravi
    [77, 55],                            # Nita
    [5,  9],                             # Sam
])
print(table)
```

```text
[[48 32]
 [12 20]
 [77 55]
 [ 5  9]]
```

Laying it out one row per line, as above, is not required by Python — but it makes the shape visible in the source code, and a 12-year-old who does this will make far fewer mistakes. Insist on it.

### 4. `.shape` — the first of the two facts

> **shape** — a pair of numbers (or just one) saying how big the array is in each direction. `(3, 4)` means **3 rows and 4 columns**.

```python
print(runs.shape)      # (4,)
print(table.shape)     # (4, 2)
```

```text
(4,)
(4, 2)
```

Three things you must be able to explain, because all three get asked:

**"Why is there a comma in `(4,)` with nothing after it?"** Because `(4,)` is a *pair-like thing with one item in it* — Python's way of writing a one-item tuple. Without the comma, `(4)` would just be the number 4 in brackets. The comma is Python saying "this is a collection, and it happens to have one thing in it". Tell the student to read `(4,)` out loud as **"four, and that's the only direction there is."**

**"Which number is rows?"** The first one. Always. `(4, 2)` is four rows, two columns. **Rows first, then columns**, exactly like reading a sentence: you go along a row, then down to the next one.

**"Is `(4, 2)` the same as `(2, 4)`?"** No, and this is worth thirty seconds of the lesson. Same eight numbers, different arrangement, different array — and next week, doing arithmetic between a `(4, 2)` and a `(2, 4)` will fail, and doing arithmetic between the wrong pair of shapes will *succeed* and give nonsense.

![Shape is rows first, then columns](../figures/fig-w17-2-shape-rows-by-columns.svg)
*Figure 17.2 — The first number in the shape is always how many rows. Swap them and you have a different array.*

### 5. `.dtype` — the second of the two facts

> **dtype** — the one kind of thing every cell in the array holds. `int64` for whole numbers, `float64` for decimals, `bool` for true/false.

```python
print(runs.dtype)      # int64
print(np.array([3.2, 4.0, 5.5]).dtype)   # float64
```

```text
int64
float64
```

**What the names mean, in one line each, in case a student asks:**

| dtype | What it holds | The number in the name |
|---|---|---|
| `int64` | whole numbers, positive or negative | 64 bits of space per number, which is a *lot* — about 9 followed by 18 zeros |
| `float64` | numbers with a decimal point | 64 bits, giving about 15 reliable digits |
| `bool` | `True` or `False`, nothing else | — |
| `<U21` | text, up to 21 characters per cell | the 21 is the longest string it saw |

> **⚠️ Watch out:** on **Windows** you will often see `int32` where this file says `int64`. It is the same idea in a smaller box. Everything in this lesson works identically; only the number in the name differs. Say so once and move on, and do not let it become a thing.

**The reason an array can only hold one kind** goes right back to §1: the values are laid out end to end with nothing in between, and to know where value 40,000 is, every value must be the same size. Different kinds are different sizes. So the array picks one kind, for all of it, forever.

**Which means: if you put one word in a list of numbers, numpy has to choose — and it chooses text.**

```python
mixed = np.array([1, 2, "three"])
print(mixed)
print(mixed.dtype)
```

```text
['1' '2' 'three']
<U21
```

Look at what happened. Every number turned into writing. The `1` is now `'1'`. And **nothing complained.** This is the planted bug, and it is exactly last week's lesson wearing different clothes: last week `48` became `'48'` on the way through a file; this week `1` becomes `'1'` on the way into an array. Same failure, same fix, same check — **read the dtype.**

Why does it choose text rather than refusing? Because there *is* a kind that can hold all three of `1`, `2` and `three`: text. There is no kind that can hold `three` as a number. Given a choice between "convert everything to the one kind that fits" and "refuse", numpy converts. It is arguably the wrong choice, and it is the choice it makes.

![An array is all one flavour, and one word decides which](../figures/fig-w17-3-dtype-one-kind-only.svg)
*Figure 17.3 — One word in a list of numbers converts every number in it to writing. No error, no warning.*

**A quieter version of the same trap**, which is worth having in your pocket for a fast student:

```python
runs = np.array([48, 12, 77, 5])
print("dtype:", runs.dtype)
runs[0] = 99.9          # put a decimal into a whole-number array
print(runs)
```

```text
dtype: int64
[99 12 77  5]
```

`99.9` went in and `99` is in there. The `.9` is gone, silently, because the array is `int64` and a whole-number box has nowhere to put a decimal. If your data has decimals, say so when you build it: `np.array([48, 12, 77, 5], dtype=float)`.

### 6. When numpy refuses: the ragged block

This is the error the student will actually hit, and it is a good one.

```python
ragged = np.array([[1, 2, 3],
                   [4, 5]])
```

```text
Traceback (most recent call last):
  File "arrays.py", line 38, in <module>
    ragged = np.array([[1, 2, 3],
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (2,) + inhomogeneous part.
```

That message is a mouthful and you should translate it, not read it:

> "numpy is asking: *how many rows, and how many columns?* It found two rows, so the first number is 2. Then it looked at the columns and found three in one row and two in the other. There is no single number that is both three and two. **A block with ragged rows has no shape, so numpy stops.**"

`inhomogeneous` is just a long word for *not all the same*. Tell them that; do not let a Latin word be the thing that defeats them.

**And say why this is good news.** numpy caught a mistake instead of guessing. It could have padded the short row with a zero — and then the student would have a silent extra zero in their data forever. Refusing is kinder.

![A ragged block is not a shape, so numpy refuses](../figures/fig-w17-4-shape-mismatch-error.svg)
*Figure 17.4 — Count the numbers in every row before you blame numpy.*

### 7. What you lose, and why it is worth it

This is the honest part of the lesson and you should not skip it.

Last week's dataset looked like this:

```python
{"name": "Asha", "team": "Falcons", "runs": 48, "balls": 32, "out": True}
```

Every value carries its label. You cannot misread it.

An array of the same data looks like this:

```text
[[ 48  32]
 [ 12  20]
 [ 77  55]
 [  5   9]]
```

**The names are gone. The column headings are gone.** There is nothing in that array that says the second column is balls. If you get the columns the wrong way round, numpy will do the arithmetic perfectly and hand you a confidently wrong answer.

So why do it? Because arrays can do maths to everything at once, and dictionaries cannot. **This is a trade, made on purpose, and both halves are real:**

| | list of dicts | array |
|---|---|---|
| Can hold text, numbers and true/false together | yes | no — one kind only |
| Every value carries its own label | yes | **no** |
| Arithmetic on the whole thing in one line | no | **yes** |
| Knows its own shape | no | yes |
| What a wrong column costs you | a `KeyError` — loud | a wrong number — silent |

The resolution arrives in Week 21, and it is worth previewing in one sentence: **pandas gives you an array with the labels put back on.** Today the student loses the labels on purpose so that they can feel what pandas is for when it arrives.

### 8. The three misconceptions you will actually meet

**Misconception 1 — "`(4,)` is a typo."**
It looks like one. It is Python's way of writing a one-item tuple, and the comma is load-bearing. The cure: have them print `runs.shape` and `table.shape` next to each other and read both out loud. One direction versus two directions.

**Misconception 2 — "an array is just a faster list."**
It is a *different thing that is also faster*. The differences that will bite them are the ones that are not about speed: one kind only, and it knows its shape. A student who thinks "faster list" will happily write `np.array([1, 2, "three"])` and be baffled later.

**Misconception 3 — "shape is how many numbers there are."**
`(4, 2)` is not 8. It is four rows of two. The number of numbers is four times two, and this week we do not even have a word for that. Ask "how many rows? how many columns?" every single time, and never accept a single number as an answer to "what shape is it?".

### 9. How deep to go, and where to stop

**Go this far:** `import numpy as np`; `np.array` from a list and from a list of lists; `.shape` for 1-D and 2-D; `.dtype` for `int64`, `float64`, `bool` and text; the six predictions, checked; the `[1, 2, "three"]` surprise; the ragged-block error; and the sentence *"what an array costs you is the labels."*

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `arr * 2`, `arr1 + arr2` — any arithmetic on arrays | **Week 18.** It is very tempting, because it is the fun part. Do not. Today is about knowing what you are holding; next week is about doing things to it. |
| `np.arange`, `np.zeros`, `np.linspace` | **Week 18.** Today every array is typed out by hand, on purpose, so that the shape is something they chose rather than something a function produced. |
| `arr[1, 2]`, `arr[:, 0]` — two-number indexing and slicing | **Week 19.** `arr[0]` for a whole row is fine if it comes up, because that is Week 11's list indexing and they already have it. |
| `.mean(axis=0)`, `.sum(axis=1)` | **Week 19.** Every year somebody teaches `axis` in the same lesson as `shape` and every year it goes badly. One idea at a time. |
| `arr > 50`, boolean masks | **Week 20.** |
| `.ndim` and `.size` | Fine to mention to a fast student — `.ndim` is how many directions, `.size` is how many numbers altogether. Neither is needed today, and adding them dilutes the two that matter. |
| `.reshape()` | Not this term. When a student's array is the wrong shape today, the fix is to **retype the brackets**, which teaches more. |
| Why 64 bits, integer overflow, floating-point error | One sentence if asked. `float64` gives about 15 reliable digits; beyond that, Level 3. |

The line to hold in your head all lesson: **today is the week the student learns to print `.shape` and `.dtype` before believing anything.** Everything else is one function call.

---

### 10. 🧭 The Growing Map — two minutes on the box that did not move

The student guide carries one figure that is not about this week's content: the same pipeline every
week, with one more piece filled in. It is the only place either book shows the learner the *shape* of
what they are building rather than this week's topic.

![The Level 2 pipeline in Week 17: still the dicts, rows and files tile, now holding every score in one array that knows its shape](../figures/fig-w17-0-where-this-fits.svg)

*Figure 17.0 — Week 17's version. Fifth week inside the `dicts · rows · files` tile, weeks 13 to 18 —
the box is unchanged and what sits inside it is not. One thread lit: representation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask the honest question first:** *"we are in the same box as last week — so what did we
   swap out inside it?"* You want *"the list became an array."* Then get the two words said out loud:
   **shape** and **dtype**. If a student can name those two, this lesson landed, whatever else the
   install did to your morning.
2. **Then the better question:** *"the word `numpy` is printed over there in stage three — so why is our
   gold box still in stage two?"* Let them argue. The answer worth arriving at is *because today numpy is
   only holding the numbers; using it to fix a real dataset starts in Week 19.* That sentence is the
   whole reason the map is worth drawing.
3. **Have them annotate their own copy:** `.shape` and `.dtype` written inside the gold tile. Two words,
   five seconds, and they will point at them again in Weeks 19, 20 and 28.

> **🧑‍🏫 Why this is worth two minutes.** An install week feels like a new subject — new command, new
> import, something downloaded off the internet — and a student who thinks today was a new subject will
> treat `.shape` as trivia. The map says the opposite: same stage, same job, better container. That is
> the framing that makes *predict the shape, then check it* feel like a habit rather than a hoop.

> **⚠️ Watch out:** do not use the map to explain what an array is. It cannot, and it is not trying to.
> It answers *where are we*, and nothing else.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Install numpy. This is the one thing that can ruin the lesson, so do it now, on the machine the student will use.**

```bash
pip install numpy
```

If that errors, try these in order — one of them will work:

```bash
pip3 install numpy
python3 -m pip install numpy
```

Then prove it, in a terminal:

```bash
python3 -c "import numpy; print(numpy.__version__)"
```

You must see a version number. Anything recent is fine:

```text
1.26.4
```

If you see `ModuleNotFoundError: No module named 'numpy'`, the install did not take. The usual cause is that `pip` installed into a different Python than `python3` runs — which is exactly what `python3 -m pip install numpy` fixes, because it uses the same Python either way. **Solve this tonight.**

- [ ] **Print workbook pages 17.1–17.6.**
- [ ] **Find graph paper**, or draw a grid of squares on a blank sheet: 12 rows, 5 columns, big enough to write in. The Hook needs it.
- [ ] **Find a pencil with a rubber on the end.** You are going to rub things out in front of them, and it matters that it is a rubbing-out and not a crossing-out.
- [ ] **Check `squad_data.py` and `records.py` from last week still run.** Week 17 imports them once.
- [ ] **Type and run the code yourself.** One file, `arrays.py`, in the same folder:

```python
"""arrays.py - my first numpy arrays."""

import numpy as np                       # bring numpy in, and call it np from now on

print("numpy version:", np.__version__)

# --- 1. one row of numbers: a 1-D array -------------------------------------
runs = np.array([48, 12, 77, 5])         # ONE list, in one set of brackets
print("runs      :", runs)
print("shape     :", runs.shape)
print("dtype     :", runs.dtype)

# --- 2. a block of numbers: a 2-D array -------------------------------------
table = np.array([
    [48, 32],                            # Asha:  runs, balls
    [12, 20],                            # Ravi
    [77, 55],                            # Nita
    [5,  9],                             # Sam
])
print("table     :")
print(table)
print("shape     :", table.shape)
print("dtype     :", table.dtype)

# --- 3. decimals give a different dtype -------------------------------------
overs = np.array([3.2, 4.0, 5.5])
print("overs     :", overs)
print("shape     :", overs.shape)
print("dtype     :", overs.dtype)

# --- 4. one word in the list, and everything changes ------------------------
mixed = np.array([1, 2, "three"])
print("mixed     :", mixed)
print("shape     :", mixed.shape)
print("dtype     :", mixed.dtype)
```

Run `python3 arrays.py`. You must see **exactly** this (with your own version number on line 1):

```text
numpy version: 1.26.4
runs      : [48 12 77  5]
shape     : (4,)
dtype     : int64
table     :
[[48 32]
 [12 20]
 [77 55]
 [ 5  9]]
shape     : (4, 2)
dtype     : int64
overs     : [3.2 4.  5.5]
shape     : (3,)
dtype     : float64
mixed     : ['1' '2' 'three']
shape     : (3,)
dtype     : <U21
```

- [ ] **Break it on purpose, twice.**
  1. Change line 8 to `runs = np.array(48, 12, 77, 5)` — no brackets. You must get `TypeError: array() takes from 1 to 2 positional arguments but 4 were given`. Put the brackets back.
  2. Add a ragged block at the bottom and read the `ValueError` in full. It is a mouthful and you want to have already translated it once.
- [ ] **Look hard at the `mixed` line.** `['1' '2' 'three']` with quote marks round the numbers. If that does not make you wince slightly, read it again — that wince is what you are trying to produce in the room.
- [ ] **Note your own `dtype`.** If you are on Windows and see `int32`, that is fine and normal. Know it before a student asks.

### 5 minutes on the day

- [ ] Editor open, terminal in the same folder, `numpy` proven working (run the one-line check again — it takes four seconds and it buys peace of mind).
- [ ] Graph paper and the pencil-with-rubber on the table. The twelve index cards beside them.
- [ ] `arrays.py` **deleted**, or renamed. They type it.
- [ ] Workbook 17.1–17.3 out; **17.4 held back until the predictions on 17.2 and 17.3 are written down and cannot be changed.** This is the whole design of the lesson.
- [ ] Bug Log out, with a fresh line under *errors with no error message* — there is one more today.

### Fallback if the laptop or the install fails

**This week's paper version is unusually faithful, because both of this week's ideas are physical.**

1. **The grid.** On graph paper, draw the twelve-record table with all five columns and the header row. Twelve rows, five columns. This takes six minutes and it is worth it.
2. **The rubbing out.** Hand them the rubber. *"Rub out the header row. Now rub out the name column."* What is left is a block of numbers with no labels. **That is an array**, and they made it. Ask: "what have you lost?" *(You can't tell which column is which.)* Ask: "what have you got that you didn't have before?" *(A neat rectangle. Every cell the same kind of thing.)*
3. **Shape.** Count the rows out loud. Count the columns out loud. Write `(12, 3)` under the block. Then have them draw a *different* block from the same numbers — three rows of twelve — and write `(3, 12)` under it. **Same numbers, different shape.** That is objective 3, done, on paper.
4. **dtype.** Ask them to write a single word above the block saying what kind of thing every cell holds. `whole numbers`. Then: *"now write the word 'three' in one cell instead of a 3. What kind of thing does every cell hold now?"* They will realise the answer has to cover the word too. That is objective 4, and it lands harder on paper than on screen.
5. **The predictions.** Workbook page 17.2 needs no computer at all. Do all six predictions on paper and check them next week, or check them on your own machine and read the answers out.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` in the lesson | Do not debug it live for more than three minutes. Switch to the paper version, set the install as homework with the three commands written down, and check it yourself before Week 18 — **Week 18 needs numpy and cannot be done on paper.** |
| `pip` works but `python3` still cannot find numpy | `python3 -m pip install numpy`. This uses the same Python that runs your code, which is the whole point. |
| A file called `numpy.py` in the folder | `AttributeError: partially initialized module 'numpy' has no attribute 'array' (most likely due to a circular import)`. Their file is being imported instead of the real numpy. Rename it. Standing rule all year, third appearance: never name a file after a library. |
| The version number is old (1.20-something) | Fine. Everything in Weeks 17–20 works. Do not spend the lesson upgrading. |
| `squad_data.py` from Week 15 is missing | Skip the "twelve records into an array" step and type the four-row `table` by hand. It delivers everything. |
| They see `int32` and this file says `int64` | Windows. Same idea, smaller box. Say so once. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Rub Out the Words | 7 | 7 | Draw the table on graph paper, then rub out the header and the names |
| 🧠 Concept — Two Things You Can Print | 16 | 23 | array vs list; the alias; shape; dtype; and the six predictions **written down** |
| 💻 Live-Code Together — `arrays.py` | 18 | 41 | Both kinds of array built. Two deliberate mistakes: one loud, one silent |
| 🎲 Their Turn — Predict Six, Check Six | 20 | 61 | The prediction game, and one sentence per miss |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Rub Out the Words (7 minutes)

**Do this:** Graph paper on the table. Twelve index cards beside it. The pencil-with-rubber in your hand. Nothing on the screen.

**Say this:**

> "Draw me your twelve-record table on this graph paper. Header row across the top — `name`, `team`, `runs`, `balls`, `out` — then one row per player. The squares are already there, so use them: one thing per square.
>
> Go. I'll help with the spelling."

Let them draw it. It takes four or five minutes and it is not wasted time — they are about to destroy it, and it needs to exist first.

**Do this:** When it is done, hold up the pencil, rubber end first.

> "Right. Rub out the header row."

They will hesitate. Let them hesitate; then have them do it.

> "Now rub out the `name` column. All twelve names."

They will hesitate more.

> "And the `team` column. And the `out` column — those are words too."

**Do this:** Wait until there is nothing left but a block of numbers. Then say nothing for three seconds and let them look at it.

> "Look at what's left. **A rectangle of numbers.** No words anywhere. That thing has a name — it's called an **array** — and it is what we're learning today.
>
> First question. **What have you lost?**"

*You can't tell which column is which. You don't know whose row is whose.*

> "Right. And that's a real loss — that's not me being dramatic. If somebody handed you that block of numbers you could not tell me who scored 104.
>
> Second question, and it's the harder one. **What have you got that you didn't have before?**"

Let them struggle. Prompts if needed: *"look at the shape of it. Look at what's in every square."*

*It's a neat rectangle. Every square has a number in it.*

> "Both of those. It's a **perfect rectangle** — twelve rows, three columns, no gaps, nothing ragged. And **every single square holds the same kind of thing.** A number. Not a name in one and a number in another.
>
> That is the whole trade of today. **You give up the labels, and what you get back is a shape and a single kind.** And next week you'll find out what that buys you, which is quite a lot."

**Do this:** Write on the board: `(12, 3)`.

> "Count the rows out loud."

*Twelve.*

> "Count the columns."

*Three.*

> "Twelve rows, three columns. Written like that: **twelve comma three**. Rows first, always. That pair of numbers is called the **shape**, and printing it is going to be the most useful thing you do all term."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What have you lost by rubbing out the words?" | The labels — which column is which, and whose row is whose. | If they say "nothing important", point at column 2 and ask "is that balls or runs?" |
| "What have you gained?" | A perfect rectangle, and every cell holds the same kind of thing. | If they only get "it's tidier", ask: "what's in every single square now?" |
| "Rows or columns first?" | Rows. | If they get it wrong, do not correct with a rule — have them count the rows out loud first, then the columns. The order they counted *is* the order. |
| "Why couldn't we keep the names in the block?" | Because then some cells would hold words and some numbers. | This is a hard question and any partial answer is good. It is the seed of `dtype` and you will come back to it. |
| "Is `(12, 3)` the same as `(3, 12)`?" | No. | If they say yes, ask them to draw the `(3, 12)` version. Watching it not fit the page is the argument. |

---

### 🧠 Concept — Two Things You Can Print (16 minutes)

**Do this:** Leave the rubbed-out grid on the table. Board work.

**Say this — part 1, the two definitions:**

> "Two words on the board, then two things you can print, then you're going to make some predictions and I'm going to make you write them down."

Write them up and leave them:

> **array** — a block of numbers, all the same kind, laid out end to end.
> **numpy** — the library that makes arrays. Somebody else wrote it; you import it.

> "You already know what a **list** is. A list will hold anything — `[1, "cat", 3.5, True]` — four different kinds of thing in four slots, and Python doesn't blink.
>
> An array won't do that. **An array holds one kind of thing and nothing else.** That sounds like a limitation, and it is, and it is also the entire reason arrays are useful."

Draw the cloakroom and the egg box, or use Figure 17.1.

> "A list is a **cloakroom.** Numbered hooks, and on each hook there's a *ticket*, and the ticket tells you which locker downstairs your coat is in. To count the red coats you take a ticket, walk down, open a locker, look, walk back. Twelve times.
>
> An array is an **egg box.** Twelve slots, twelve eggs, all touching, all the same. You don't fetch anything. You glance.
>
> That's it. That's the difference, and everything else follows from it."

**Say this — part 2, the alias:**

> "First line of the file, and everybody on Earth writes it exactly this way."

```python
import numpy as np
```

> "`import numpy` — go and get the numpy toolkit. And `as np` — **and from now on, in this file, I'm calling it `np`.** That's called an **alias**. A nickname.
>
> Why bother? Because you're going to type it forty times in a lesson and `numpy.array` is six characters longer than `np.array` every single time.
>
> And why `np` specifically, and not `n` or `numbers` or `banana`? Because **everybody** writes `np`. Every book, every tutorial, every bit of code you'll ever paste from the internet. It's not a rule — `import numpy as banana` genuinely works — it's a **convention**, and conventions are how strangers manage to read each other's work. Follow it."

**Say this — part 3, the two things you print:**

> "Now the two facts. Every array carries them, and printing them is 80% of getting numpy right."

Write on the board:

```
arr.shape   ->  how big, in each direction.  Rows first.
arr.dtype   ->  what ONE kind of thing every cell holds.
```

> "`.shape` you already invented, on the graph paper. Twelve rows, three columns: `(12, 3)`.
>
> One warning about it, because it looks like a mistake. If there's only one direction — just a row of numbers, no columns — the shape comes out as `(4,)`. With a comma and nothing after it. **That's not a typo.** The comma is Python's way of saying 'this is a *pair-like thing*, it just happens to have one item in it'. Read it out loud as *'four, and that's the only direction there is.'*"

> "`.dtype` is the new one, and it's short for **data type** — the kind of thing. Remember `type()` from Week 2? `int`, `float`, `str`, `bool`? Same idea, one important difference: `type()` asks about **one value**. `.dtype` asks about **all of them at once**, and it only gets one answer, because there is only one answer.
>
> Which raises a question I want you to sit with. Look at the block you rubbed out. What if I put a word back in one of those squares? What kind of thing does every cell hold now?"

Let them think. Someone will get to "you'd have to say words".

> "You would. And that's exactly what numpy does, and it does it without telling you. Hold on to that."

**Say this — part 4, and this is the design of the lesson:**

> "Before we type anything, you're going to make six predictions and write them down in pen where you can't quietly change them.
>
> Page 17.2. Six arrays. For each one, write **what shape you think it'll be** and **what kind of thing you think every cell will hold.** Guess. Being wrong is completely fine — what's not fine is deciding what you thought *after* you've seen the answer, because then you learn nothing.
>
> Take four minutes. Go."

**Do this:** Have them fill in the prediction columns on page 17.2 and 17.3. Circulate but do not confirm or deny anything. Not a nod, not a face. This is hard and it matters.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What can a list hold that an array can't?" | Different kinds of thing at the same time. | If they say "more stuff", clarify with an example: `[1, "cat", 3.5]`. |
| "What does `as np` do?" | Gives numpy a shorter name, just in this file. | If they think it changes numpy itself, say: "another file could call it something else and numpy wouldn't notice." |
| "Why does `(4,)` have a comma?" | Because it's a collection with one item in it, not just the number 4. | If they still think it's a typo, print `(4)` and `(4,)` and show that Python treats them differently. |
| "In `(12, 3)`, which is rows?" | 12. Rows first. | Have them count the rows on the graph paper out loud again. Do not give a rule they have to remember. |
| "What's the difference between `type()` and `.dtype`?" | `type()` asks about one value; `.dtype` asks about every value at once. | If they say "nothing", print `type(runs)` — which gives `ndarray` — beside `runs.dtype`, which gives `int64`. Two different questions. |
| "What happens if one cell has a word in it?" | Everything has to become words. | Any answer that notices there is a *problem* is a good answer. Do not resolve it — it is coming in ten minutes. |

---

### 💻 Live-Code Together — `arrays.py` (18 minutes)

**You never touch the keyboard.** Predictions before every run.

**Step 1 (2 min).** New file, `arrays.py`. Two lines:

```python
"""arrays.py - my first numpy arrays."""

import numpy as np                       # bring numpy in, and call it np from now on

print("numpy version:", np.__version__)
```

Run it. Real output:

```text
numpy version: 1.26.4
```

> **Say this:** "That's it. That's the whole install proved. If you get a version number, numpy is on your machine and working. If you get `ModuleNotFoundError`, we have a problem to solve and it's got nothing to do with today's ideas.
>
> Also — `np.__version__`, with two underscores each side. Those double underscores are a Python convention meaning 'this is information *about* the thing, rather than part of what it does'. You don't need to type it again today."

**Step 2 — ⚠️ FIRST DELIBERATE MISTAKE (4 min).** This is the natural mistake and you should dictate it wrongly on purpose.

> **Say this:** "Now build an array from four scores. Type: `runs = np.array` open bracket, forty-eight comma twelve comma seventy-seven comma five, close bracket."

```python
runs = np.array(48, 12, 77, 5)           # four scores... or so we hope
print(runs)
```

**Ask before running:** "What do you expect?" *Four numbers.*

Run it. Real output:

```text
numpy version: 1.26.4
Traceback (most recent call last):
  File "arrays.py", line 7, in <module>
    runs = np.array(48, 12, 77, 5)           # four scores... or so we hope
TypeError: array() takes from 1 to 2 positional arguments but 4 were given
```

> **Say this:** "Read the last line and say it in your own words."

*It takes one or two things and I gave it four.*

> "Exactly right. **`np.array` wants one thing: a list.** I gave it four separate numbers and it has nowhere to put numbers two, three and four.
>
> This is Week 10 again — a function has a fixed number of slots, and you handed it too many things. Same error family, new function.
>
> So put the numbers **in a list first**, and hand it the list. One extra pair of brackets."

```python
runs = np.array([48, 12, 77, 5])         # ONE list, in one set of brackets
print("runs      :", runs)
print("shape     :", runs.shape)
print("dtype     :", runs.dtype)
```

**Ask before running:** "Three lines. What will they say?" *Take their predictions on all three.*

Run it. Real output:

```text
numpy version: 1.26.4
runs      : [48 12 77  5]
shape     : (4,)
dtype     : int64
```

> **Say this:** "Three things to notice, and the third one is the important one.
>
> **One: no commas.** Look at how it printed — `[48 12 77 5]` with spaces. A *list* prints with commas. An *array* prints with spaces. That's the fastest way there is to tell which one you're holding, and you'll use it all year.
>
> **Two: look at the `5`.** There's an extra space in front of it, so it lines up under the `77`. numpy did that on purpose, because arrays are for looking at in rows and columns.
>
> **Three: the shape is `(4,)`.** Four, comma, nothing. One direction only. Say it out loud: *four, and that's the only direction there is.*"

**Bug Log the `TypeError` now**, with the fix as "put the numbers in a list first".

**Step 3 (4 min).** The 2-D array. Insist on the one-row-per-line layout.

```python
table = np.array([
    [48, 32],                            # Asha:  runs, balls
    [12, 20],                            # Ravi
    [77, 55],                            # Nita
    [5,  9],                             # Sam
])
print("table     :")
print(table)
print("shape     :", table.shape)
print("dtype     :", table.dtype)
```

> **Say this:** "Notice the shape of what you typed. **One inner list per row**, each on its own line. You don't have to lay it out like that — Python doesn't care — but you should, because now the shape of the code is the shape of the array and you can see mistakes with your eyes.
>
> Predict the shape before we run. How many rows? How many columns?"

*Four rows, two columns.*

Run it. Real output:

```text
table     :
[[48 32]
 [12 20]
 [77 55]
 [ 5  9]]
shape     : (4, 2)
dtype     : int64
```

> "Four comma two. And look at the printing — numpy put the rows on separate lines and lined the columns up. It knows it's a rectangle, so it draws one.
>
> Now the question from the Hook. **Which column is balls?**"

*The second one.*

> "How do you know?"

*Because you told me. / Because of the comment.*

> "Because of the **comment**. There is nothing in that array that says so. If you got the columns the wrong way round, numpy would do the maths perfectly and hand you a wrong answer with a straight face. **That's what you paid for the rectangle.**"

**Step 4 (3 min).** Decimals, and a second dtype.

```python
overs = np.array([3.2, 4.0, 5.5])
print("overs     :", overs)
print("shape     :", overs.shape)
print("dtype     :", overs.dtype)
```

**Ask before running:** "Shape? Dtype?" *(3,) and something-to-do-with-decimals.*

Run it. Real output:

```text
overs     : [3.2 4.  5.5]
shape     : (3,)
dtype     : float64
```

> **Say this:** "`float64` — decimals. And look at the middle one. You typed `4.0` and it printed `4.` with a dot and nothing after it. That dot is numpy telling you *'this is a decimal number that happens to be exactly four'*, which is a different thing from the whole number four. Same as Week 2: `4` and `4.0` are not the same kind of thing."

**Step 5 — ⚠️ SECOND DELIBERATE MISTAKE (5 min).** This one does not crash, and you must let them believe it for a moment.

> **Say this:** "Last one. Somebody typing a list of numbers gets distracted and writes one of them as a word. It happens constantly. Type this."

```python
mixed = np.array([1, 2, "three"])
print("mixed     :", mixed)
print("shape     :", mixed.shape)
print("dtype     :", mixed.dtype)
```

**Ask before running:** "Two questions. Will it crash? And if it doesn't, what's the dtype?"

Take their answers. Most students say it will crash. Then run it. Real output:

```text
mixed     : ['1' '2' 'three']
shape     : (3,)
dtype     : <U21
```

> **Say this:** *(pause)* "Read me the first line."

*Quote one quote, quote two quote, quote three quote.*

> "There are **quote marks round the numbers.** The `1` isn't a one any more. It's the character `1`. Both of your numbers turned into writing because one of the three was a word, and **nothing complained.**
>
> Why? Because an array holds **one** kind of thing. numpy looked at a one, a two and the word 'three' and asked itself: *is there any single kind of thing that can hold all three of those?* And there is — writing. There is no kind that can hold 'three' as a number. So it converted everything to writing, because that's the one that fits.
>
> And `<U21`? `U` means text. The 21 is how many characters it's got room for. You don't need the details — **what you need is to have read the dtype and gone 'hang on, that's not int64.'**
>
> Where have you seen this before?"

Let them find it. It is last week.

> "Last week. `48` went into a file and came back as `'48'`. Same failure. **A thing that could only hold one kind of thing turned your numbers into writing, and never said a word about it.** Same check, too: read the dtype."

**Bug Log this**, under *errors with no error message*.

---

### 🎲 Their Turn — Predict Six, Check Six (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–3:** re-read the six predictions they wrote in the Concept segment. **No changing them.**
- **Minutes 3–12:** build all six, print shape and dtype for each, tick or cross every prediction.
- **Minutes 12–17:** one written sentence for every miss. This is the objective and it is not optional.
- **Minutes 17–20:** the ragged block, on purpose, and the `ValueError` translated into their own words.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the rubbed-out graph paper, workbook page 17.2 with **six predictions already written in pen**, page 17.4 blank, the Bug Log.

**On the screen:** `arrays.py` from the live-code, with a blank space at the bottom.

**The one rule that makes this work:** the predictions were written before any code ran and they may not be edited. If a student wants to change one, have them write the new guess *next to* the old one and mark which came first.

### The six arrays

```python
"""six.py - predict the shape and the dtype of all six BEFORE you run this."""

import numpy as np

one   = np.array([10, 20, 30])
two   = np.array([[1, 2, 3],
                  [4, 5, 6]])
three = np.array([2.5, 3.5, 4.5, 5.5])
four  = np.array([1, 2, 3.0])
five  = np.array([[7],
                  [8],
                  [9]])
six   = np.array([True, False, True])

print(f"{'array':<8}{'shape':<10}{'dtype'}")
print("-" * 28)
for name, arr in [("one", one), ("two", two), ("three", three),
                  ("four", four), ("five", five), ("six", six)]:
    print(f"{name:<8}{str(arr.shape):<10}{arr.dtype}")
```

Real output:

```text
array   shape     dtype
----------------------------
one     (3,)      int64
two     (2, 3)    int64
three   (4,)      float64
four    (3,)      float64
five    (3, 1)    int64
six     (3,)      bool
```

### Which two they will get wrong, and why

Two of the six are designed to be missed. Do not tip them off.

**`four = np.array([1, 2, 3.0])` → `float64`.** Almost every student predicts `int64`, because two out of the three numbers are whole. But an array holds **one** kind, and it has to be a kind that can hold `3.0` without losing anything. A whole-number box cannot hold `3.0`'s decimal point; a decimal box can hold `1` perfectly well as `1.0`. So numpy picks the one that loses nothing: `float64`. **The rule to draw out of it: numpy picks the kind that can hold everything, not the kind most of the values already are.** This is exactly the same reasoning as `[1, 2, "three"]` becoming text, and a student who sees that connection has had a very good lesson.

**`five = np.array([[7], [8], [9]])` → `(3, 1)`.** Most students predict `(3,)`, because it is three numbers. But every `7` is inside its own inner list, and an inner list is a **row**. So it is three rows of one column each — a column, standing up. This is the single most important shape in the whole of numpy, because next week `(3,)` and `(3, 1)` added together will produce nine numbers instead of three, and nothing will complain. **Do not explain that today.** Just make sure they have written `(3, 1)` down and can say what the `1` is.

### The scoring, and the sentences

For each of the six, on page 17.4:

| # | Predicted shape | Actual shape | ✔/✘ | Predicted dtype | Actual dtype | ✔/✘ |
|---|---|---|---|---|---|---|

And then, **the part that is actually the objective:**

> **One sentence for every single cross.** Not "I got it wrong". A sentence that says *what you thought* and *what is actually true*.

Model sentences, for the two designed misses:

> *"I said `four` would be int64 because two of the three numbers are whole numbers. It's float64, because an array only gets one kind and the kind has to be able to hold 3.0 without throwing the decimal away."*

> *"I said `five` would be (3,) because there are three numbers in it. It's (3, 1), because each number is inside its own inner list, and an inner list is a row — so it's three rows of one column."*

**This is the assessable output of the week.** A student who predicted six out of six correctly has learned less than a student who missed two and wrote those two sentences. Say that out loud, before they start.

### The ragged block (3 minutes)

**Do this:** After the six are checked, one more, at the bottom of the file.

> **Say this:** "One more. This one is going to break, and I want you to read the message and translate it for me."

```python
ragged = np.array([[1, 2, 3],
                   [4, 5]])
print(ragged.shape)
```

Real output (the line number will be wherever this landed in *their* file — mine was 38):

```text
Traceback (most recent call last):
  File "arrays.py", line 38, in <module>
    ragged = np.array([[1, 2, 3],
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (2,) + inhomogeneous part.
```

> **Say this:** "That's a mouthful. Let's take it apart. `inhomogeneous` is a long word for **not all the same**. And `dimensions` means directions — rows and columns.
>
> So numpy is saying: *I got as far as counting the rows. There are two. Then I tried to count the columns, and I found three in one row and two in the other, and there's no number that is both.*
>
> Now — **is this good news or bad news?**"

Let them argue. Steer to the answer:

> "It's good news. Look at what numpy *could* have done instead. It could have stuck a zero on the end of the short row and carried on, and then you'd have a made-up zero sitting in your data forever and no way of knowing. **It refused instead, and refusing is kinder.**
>
> Write it in the Bug Log with the translation in your own words. When you meet this in Week 20, at two in the afternoon, you will not want to be translating Latin."

### What "finished" looks like

- `arrays.py` builds a 1-D array, a 2-D array and a decimal array, and prints `.shape` and `.dtype` for all three.
- Six predictions, written in pen **before** the code ran, all six checked against real output.
- **One written sentence per miss**, saying what they thought and what is true.
- The `TypeError` from the missing brackets and the `ValueError` from the ragged block are both in the Bug Log, with translations.
- The student can point at the rubbed-out graph paper and say what an array costs you.

### Variation — easier

- **Four arrays, not six.** Keep `one` (the easy one, to build confidence), `two` (the 2-D one), `four` (the float surprise) and `five` (the `(3, 1)` surprise). The two surprises are the lesson; the easy ones are the warm-up.
- **Predict shape only, not dtype.** Shape is the more useful of the two and it is much more intuitive. Do dtype as a whole-class demonstration instead of a prediction.
- **Skip the mixed-types array.** It is the richest thing in the lesson and it is also the fourth idea. Save it for Week 18's warm-up, where it will land just as well.
- **Give them `arrays.py` finished** and have them only add the print lines for shape and dtype. The understanding is in reading the output, not in typing the arrays.
- **Do the whole lesson on graph paper** from the Fallback section. Draw, rub out, count rows, count columns, write the shape. That is objectives 2, 3 and 4 with no computer at all.

### Variation — harder

None of these need syntax from a later week.

1. **`.ndim` and `.size`.** Add them to the prediction table. `.ndim` is how many directions there are (1 for a row, 2 for a block); `.size` is how many numbers there are altogether. Then the good question: *"which of shape, ndim and size could you work out from the others?"* (`ndim` is how many numbers are in the shape. `size` is them multiplied together. **Shape is the only one that is really new information** — and that is why it is the one we print.)
2. **Make numpy pick each of the four dtypes on purpose.** Write four arrays, one each for `int64`, `float64`, `bool` and text, and for each one write *why* numpy had no other choice.
3. **Force the dtype.** `np.array([48, 12, 77, 5], dtype=float)` and read the result: `[48. 12. 77. 5.]`. Then: *"when would you want to do that, before you have any decimals?"* (When more decimals are coming — a total you are about to divide, an average you are about to store. Deciding the kind up front is a design decision, not a reaction.)
4. **The silent truncation.** `runs[0] = 99.9` on an `int64` array gives `[99 12 77 5]` and the `.9` is gone with no warning. Then: *"is that better or worse than the ragged-block error, and why?"* (Much worse. The error stopped you. This didn't.)
5. **Two shapes, same numbers.** Build the twelve scores as `(12,)`, then as `(2, 6)`, then as `(6, 2)`, then as `(1, 12)`, then as `(12, 1)`. Five arrays, same twelve numbers, five different shapes. Then: *"which one is the twelve scores, and which ones are something else?"* (All five hold the same numbers. Only some of them mean anything. **Shape is meaning, not just size.**)
6. **The honest cost.** Take the Week 15 `group_count` and ask: *"could you do that on an array?"* (No — grouping needs the team names, and the names are exactly what you rubbed out.) Then: *"so which of the two would you keep, if you could only have one?"* There is no right answer and the argument is the point. It is also the exact question pandas exists to refuse to answer.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

> **🧑‍🏫 If a student asks:** Python 3.11 and newer draw little `~~~^^^` arrows under the exact part of the line that failed. Older Pythons don't, and neither does numpy's own error above. Both are saying the same thing.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | "There's no numpy on this machine, or not on the one I'm using." | numpy is not installed, or `pip` installed it into a different Python than `python3` runs. | `python3 -m pip install numpy` — the `-m` makes it the *same* Python. Then prove it with `python3 -c "import numpy; print(numpy.__version__)"`. |
| `ModuleNotFoundError: No module named 'nunpy'` | "There's no library with that name." | A typo in the import line. Read the name in the message. | Fix the spelling. The error is quoting exactly what you typed — that is the fastest way to spot it. |
| `TypeError: array() takes from 1 to 2 positional arguments but 4 were given` | "I take one thing and you gave me four." | `np.array(48, 12, 77, 5)` — the list brackets are missing. | `np.array([48, 12, 77, 5])`. Numbers go in a list first. |
| `ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (2,) + inhomogeneous part.` | "Your rows aren't all the same length, so there's no shape." | A ragged list of lists — three numbers in one row, two in another. | Count the numbers in every row. Make them match. (`inhomogeneous` = not all the same.) |
| `TypeError: 'tuple' object is not callable` | "You put brackets after something that isn't a function." | `runs.shape()`. `.shape` is a **fact about** the array, not a thing you do to it. | `runs.shape`, no brackets. Same for `.dtype`. |
| `AttributeError: 'numpy.ndarray' object has no attribute 'Shape'. Did you mean: 'shape'?` | "There's no `Shape`, but there is a `shape`." | A capital letter. Python is case-sensitive. | Lower case: `runs.shape`. Read the "Did you mean" — Python is telling you the answer. |
| `AttributeError: module 'numpy' has no attribute 'Array'. Did you mean: 'array'?` | Same mistake, on the function. | `np.Array([...])` with a capital A. | `np.array([...])`. |
| `AttributeError: partially initialized module 'numpy' has no attribute 'array' (most likely due to a circular import)` | "The thing I imported as numpy is importing itself." | **There is a file called `numpy.py` in the folder**, so `import numpy` found theirs. | Rename their file. Standing rule all year: never name a file after a library. |
| `IndexError: index 7 is out of bounds for axis 0 with size 4` | "You asked for slot 7 and there are only four slots." | `runs[7]` on a four-number array. | Slots are 0, 1, 2, 3. Week 11's lesson with numpy's wording — `axis 0` just means "the first direction". |
| **No error, dtype is `<U21`** | Nothing is wrong as far as numpy is concerned. | One value in the list is text — often a typo like `"3"` for `3`, or a word. **Every number in the array is now writing.** | Find the text in the list and make it a number. And print `.dtype` on every array you build. |
| **No error, dtype is `float64` when you expected `int64`** | Nothing is wrong at all — this is correct. | One value has a decimal point, so numpy picked the kind that can hold everything. | Nothing to fix. But know that it happened, because it changes how the numbers print. |
| **No error, `99.9` became `99`** | Nothing is wrong as far as numpy is concerned. | Assigning a decimal into an `int64` array. There is nowhere to put the `.9`. | Build the array as decimals in the first place: `np.array([...], dtype=float)`. |

### How to teach debugging without giving the answer

The moves stand: read the last line, find the line number, say the complaint in your own words, compare characters, and *"which `File` line is the last one?"*. Last week added *"how many went out and how many came back?"* and *"what does `type()` say?"*. This week adds one more, and it is the numpy move:

9. **"Print the shape. Print the dtype."** Two lines. Before you form any theory at all. Something like 80% of numpy confusion is an array that is not the shape you think it is or not the kind you think it is, and both are one word away from being visible.

And the sentence for this week:

> **"With numpy, do not reason about what your array probably is. Print `.shape` and `.dtype` and read them. It takes four seconds and it is more reliable than you are."**

---

## ❓ Questions Students Ask This Week

**"Why is there a comma in `(4,)`?"**

Because `(4,)` is a **tuple with one item in it**, and Python needs a way to write that down. Without the comma, `(4)` is just the number four with brackets round it, exactly like `(2 + 3)` is five. The comma is what makes it a collection.

Why does the shape have to be a collection at all, even for one direction? So that `.shape` always answers the same *kind* of question. `(4,)` and `(4, 2)` and `(4, 2, 3)` are all "here is a size for each direction" — one number, two numbers, three numbers. If a 1-D array's shape were just `4`, then code that reads shapes would have to handle two different sorts of answer. Read it out loud as *"four, and that's the only direction there is."*

**"Is an array just a faster list?"**

It is faster, and calling it "a faster list" will get a student into trouble, because the differences that bite are not about speed:

- An array holds **one kind of thing.** A list holds anything.
- An array knows its **shape.** A list only knows its length.
- An array can do maths to all of its numbers at once. A list cannot. *(That is next week.)*
- An array is a **fixed size.** You cannot `.append` to it. A list grows happily.

That last one surprises people. If you need to collect values one at a time as you go, **use a list**, and turn it into an array at the end. That is exactly what they will do with `column(squad, "runs")` — build a list, then `np.array()` it.

**"How much faster, really?"**

For a million numbers, doubling them all: about twenty times faster with an array than with a Python loop. On a laptop, roughly 20 milliseconds against 1.

And here is the honest bit, which is worth saying to a 12-year-old: **for twelve numbers, it makes no difference you could ever notice.** Both are instant. So the speed is not why we are doing this today. We are doing it because next week one line will replace four, and because every model in this course does its arithmetic this way. The speed becomes the reason later, when the data is big — and by then you will already think in arrays.

**"Why does `[1, 2, 3.0]` make everything decimals?"**

Because an array gets **one** kind for all of it, and numpy picks the kind that can hold every value **without losing anything.**

Think about the two options. Make it whole numbers: `3.0` would have to become `3`, and the decimal point is thrown away — information lost. Make it decimals: `1` becomes `1.0`, which is the same number written differently — nothing lost. So numpy picks decimals.

Exactly the same reasoning makes `[1, 2, "three"]` into text: text can hold `1` (as the character `1`), and numbers cannot hold `three`. **numpy always picks the kind that can hold everything.** Once you have that sentence, both surprises stop being surprises.

**"What does the 64 in `int64` mean?"**

How many bits of space each number gets — 64 of them, which is eight bytes. That is room for whole numbers up to about 9 with 18 zeros after it, which is more than enough for anything in this course.

There is a `float64` too, with 64 bits split between the digits and where the decimal point goes; it gives about 15 reliable digits. And on Windows you will often see `int32`, which is half the space and still holds numbers up to about 2 billion. **Nothing in Weeks 17 to 20 changes because of any of this.** It is worth one sentence and no more.

**"Can I put words in an array?"**

Yes, and numpy will do it — you get a `<U`-something dtype and every cell holds text. It is legal and it is occasionally useful.

It is also almost always a sign that something went wrong, because the reason to use an array is arithmetic, and you cannot do arithmetic on words. If you find yourself with a text array you did not intend, you have probably got a typo in a list of numbers. **If your data is genuinely words, a list or a dictionary is the better tool** — and from Week 21, a pandas DataFrame, which lets one column be words and another be numbers, which is exactly what you want.

**"Which is better — a list of dictionaries, or an array?"** *(Nobody fully agrees, and here is why.)*

**Neither, and people who work with data argue about the boundary every day.** It is worth being straight about this rather than pretending there is a right answer.

The array wins whenever the answer is a number computed from many numbers. Averages, totals, distances, every model in this course. One line instead of a loop, twenty times faster, and — the part that matters more — **a line you can read and check.** `celsius * 9 / 5 + 32` is the formula. A four-line loop is the formula *plus* the machinery of visiting each item, and the machinery is where the mistakes live.

The list of dictionaries wins whenever the labels matter, which is more often than beginners expect. Real data is mixed: a name, a category, three numbers, a true/false. Real questions are about categories: *how many per team?* And real mistakes are about columns: with a dictionary, asking for a field that is not there gives you a loud `KeyError`; with an array, asking for the wrong column gives you a **number**, and the number is wrong, and nobody tells you.

There is a genuine disagreement underneath this, and it is about **where you want your safety.** One camp says: convert to arrays as early as possible, keep the fast numeric core small and clean, and be careful at the edges. The other says: keep the labels for as long as you possibly can, because the cost of a silent wrong column is far higher than the cost of a slow loop. Both camps ship real software.

What everybody agrees on is the thing that resolves it, and it arrives in Week 21: **pandas**, which is an array with the labels put back on. That is genuinely the best of both, and it is also slower and more complicated than either, which is why it did not come first. Today the student loses the labels on purpose. In four weeks they will get them back, and they will know exactly what they are for.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **numpy is not installed and the lesson dies at minute three** | Because it was installed on a different machine, or by a different Python | This is why the Prep Checklist has it first. If it happens anyway: **do not debug for more than three minutes.** Switch to the graph-paper version, which teaches this week completely, and set the install as homework with the three commands written down. Then fix it yourself before Week 18, which cannot be done on paper. |
| `(4,)` is read as a typo and quietly ignored | It genuinely looks like a mistake | Print `runs.shape` and `table.shape` on adjacent lines and have them read both out loud. One direction versus two. Then have them say *"four, and that's the only direction there is."* |
| The predictions get changed after the answers appear | Because being wrong feels bad and a pencil is right there | **Pen, not pencil, for the prediction column.** And say the reason out loud before they start: *"a prediction you changed afterwards teaches you nothing, and the whole point of today is the sentences you write about your misses."* |
| A miss gets recorded as "I got it wrong" with no sentence | Because it is the fastest way to fill the box | Hand it back. The sentence *is* the objective, not the tick. Give them the model sentence from the Activity section as a shape to copy. |
| `.shape()` with brackets, repeatedly | Every other thing they have used all year needed brackets | Do not just remove the brackets. Ask: *"is the shape something the array **does**, or something the array **is**?"* It is a fact about it, like your height. You don't call your height. |
| The `<U21` array is shrugged off — "so it's text, who cares" | Because the numbers still look like numbers on the screen | Point at the quote marks. Then connect it to last week out loud: *"this is `'104'` again. Last week it came from a file. This week it came from one typo in a list. Same failure."* If they still shrug, next week's `arr * 2` on a text array will make the point for you. |
| Somebody teaches `arr * 2` because it is fun | It is very fun | Hold the line. Today is *what am I holding*. Next week is *what can I do to it*. A student who does arithmetic on an array whose shape they cannot predict will spend Week 18 confused about which of two new things went wrong. |
| The 2-D array is typed all on one line | Because it works | It works and it hides mistakes. Retype it one row per line, with a comment naming each row, and say why: **the shape of the code should be the shape of the array.** |
| The Hook's grid-drawing eats fifteen minutes | Twelve rows by five columns is a lot of writing | Cut it to six rows. The rubbing-out is the lesson, not the drawing. Or pre-draw the grid yourself and let them fill in six rows. |
| A student is upset about rubbing out work they just did | Reasonable! It took them five minutes | Say the real thing: *"we're not throwing it away, we're finding out what it costs to throw it away."* And keep the cards — the labels still exist, just not in the array. That is the honest position and it is also what pandas is for. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** `.dtype` as a prediction. Do it as a demonstration you narrate, and keep the predictions to shape only. Shape is the more useful of the two and much more intuitive.

**Cut:** the mixed-types array. It is the deepest idea here and it is the fourth one. It will land perfectly as Week 18's warm-up.

**Cut:** four of the six arrays. Keep `one` (confidence), `two` (2-D), and `five` (the `(3, 1)` surprise, which matters most for next week).

**Give them the arrays already written**, and have them do nothing but read shape and dtype off the screen and tick their predictions. The understanding lives in the reading, not the typing.

**Reteach — with the graph paper and the rubber, and nothing else.** The Hook is the entire lesson. Draw the grid. Rub out the words. Count rows out loud, count columns out loud, write `(12, 3)`. Then draw the same numbers as three rows of twelve and write `(3, 12)` under it, and ask which one is the table they started with. Then write one word above the block saying what kind of thing every cell holds. **That is objectives 2, 3 and 4, on paper, in twelve minutes**, and a student who leaves the room able to say *"rows first, then columns, and every cell is the same kind of thing"* has had a successful lesson whether or not any Python ran.

**The copy-this-exactly scaffold.** One file. This runs:

```python
import numpy as np

scores = np.array([48, 12, 77, 5])
print(scores)
print("shape:", scores.shape)
print("dtype:", scores.dtype)

block = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(block)
print("shape:", block.shape)
print("dtype:", block.dtype)
```

```text
[48 12 77  5]
shape: (4,)
dtype: int64
[[1 2 3]
 [4 5 6]]
shape: (2, 3)
dtype: int64
```

Then one question, out loud: **"how many rows in the second one, and how many columns?"** Two and three. That is the objective.

**One thing you must not cut:** printing `.shape`. If this lesson collapses to a single sentence, make it *"rows first, then columns — and print it, don't guess it."*

### If the student is flying

None of these need syntax from a later week.

1. **`.ndim` and `.size`** (Variation-harder 1), and the good question about which of the three is really new information.
2. **Force each of the four dtypes on purpose** (Variation-harder 2), with a written reason for each.
3. **`dtype=float` up front** (Variation-harder 3), and when you would want it before you have any decimals.
4. **Five shapes, same twelve numbers** (Variation-harder 5). `(12,)`, `(2, 6)`, `(6, 2)`, `(1, 12)`, `(12, 1)`. Then: which of these *means* anything?
5. **The honest cost** (Variation-harder 6). Could you do `group_count` on an array? No — you rubbed out the names. So which would you keep?
6. **Measure the speed themselves.** This needs `import time`, which is nothing new, and one loop, which they have had since Week 7:

```python
import time
import numpy as np

count = 1_000_000
numbers = list(range(count))
start = time.perf_counter()
doubled = [n * 2 for n in numbers]
list_time = time.perf_counter() - start
print(f"list : {1000 * list_time:.1f} ms")
```

*(Their numbers will differ from anybody else's, and that is the point: run it three times and watch it wobble. A measurement you only took once is not a measurement. Do not give them the array half — that is `arr * 2`, and it is next week.)*

### If the student won't engage today

**Graph paper, a pencil with a rubber, and the twelve cards. Close the laptop.**

Draw the table. Six rows is plenty.

Then hand them the rubber and say one thing:

> **"Rub out every word."**

When the words are gone, ask two questions and let the silence work:

> **"What can't you tell me any more?"**
>
> **"What's true about every single square now that wasn't true before?"**

Then count the rows out loud, count the columns out loud, and write the pair of numbers underneath.

That is the entire lesson. It takes ten minutes, it delivers objectives 2, 3 and 4, and it gives them the one thing they need for next week — the idea that a block of numbers has a *shape*, and that the shape is something you count rather than something you assume. The typing survives to Week 18, which is a lab and will need it anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — shape (spoken, 45 seconds)**

> "I've got an array with shape `(5, 3)`. How many rows, how many columns, and how many numbers altogether?"

*Good answer:* "Five rows, three columns, fifteen numbers."

**What to catch:** a student who says "three rows, five columns" has the order backwards, which will cost them badly in Week 19. Do not just correct it — have them draw it, counting the rows out loud first.

**Check 2 — dtype (spoken, 60 seconds)**

> "`np.array([1, 2, 3.0])` has dtype `float64`, not `int64`. Why?"

*Good answer:* "Because an array only gets one kind of thing for all of it, and it has to be a kind that can hold `3.0` without losing the decimal. Whole numbers couldn't hold it. Decimals can hold `1` fine, as `1.0`. So numpy picks decimals."

**Full marks needs the reason, not the rule.** "Because there's a decimal in it" is a level-2 answer. Push once: *"why does one decimal decide it for all three?"*

**Check 3 — predict, on paper, no computer (90 seconds)**

> "Write me the shape and the dtype of these two, without running them:
> `np.array([[7], [8], [9]])` and `np.array([True, False])`"

*Good answer:* `(3, 1)` and `int64`; `(2,)` and `bool`.

**What to catch:** `(3,)` for the first one is the expected miss and it is the important one. Ask: *"how many inner lists are there, and what is an inner list?"* Three, and it is a row. So three rows of one column.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot build an array without copying. Reads `(4,)` as a typo. Cannot say which number in a shape is rows. |
| **2 — Emerging** | Builds a 1-D array with the pattern given. Reads shape and dtype off the screen when told where to look. Gets rows and columns the right way round when reminded. |
| **3 — Secure** | Writes `import numpy as np` and builds both a 1-D and a 2-D array unaided. Prints `.shape` and `.dtype` without being asked. Says what each number in a shape means. Explains why an array holds only one kind. **This is the target.** |
| **4 — Strong** | Predicts shapes correctly, including `(3, 1)` for a column. Explains `float64` from `[1, 2, 3.0]` in terms of "the kind that can hold everything". Translates the ragged-block `ValueError` into their own words. Says what an array costs you — the labels. |
| **5 — Exceptional** | Connects `<U21` to last week's `'104'` unprompted, as the same failure. Argues both sides of "array or list of dicts" and says the answer depends on whether a wrong column would be loud or silent. Notices that shape carries meaning, not just size — that `(12, 1)` and `(1, 12)` hold the same numbers and are not the same thing. |

---

## 📤 Homework to Assign

**Say this:**

> "Short one this week, and the marking is all in one column. About forty-five minutes.
>
> **First — and this is the whole assignment — predict.** Page 17.4. There are six arrays written out for you. **Before you touch a computer**, write down for each one what shape you think it will be and what dtype you think it will have. **In pen.** Twelve guesses, six arrays.
>
> **Second, check all six.** Page 17.5. Type them into a file, print `.shape` and `.dtype` for each one, and tick or cross every single guess against the real output.
>
> **Third — and this is the bit I'm actually marking — one sentence for every cross.** Not 'I got it wrong'. A sentence that says **what you thought** and **what is actually true.** Like this: *'I said it would be int64 because most of the numbers are whole. It's float64, because an array only gets one kind and the kind has to be able to hold 3.5 without throwing away the decimal.'*
>
> **If you got all twelve right, you have a problem**, and I mean that. It means you either guessed after you ran it, or these were too easy for you — and if it's the second one, come and tell me and I'll give you harder ones. **The sentences are worth more than the ticks.**
>
> **Fourth, one line at the bottom.** Look back at your Week 16 dataset. Which of your five columns *could* go into an array, and which could not, and why?"

**Workbook pages:** 17.1, 17.2, 17.3 in class · **17.4, 17.5, 17.6** at home.

**Expected time:** 10 min on the twelve predictions · 15 min typing and checking · 15 min on the sentences · 5 min on the last line. **About 45 minutes.**

> **🧑‍🏫 What to look for when you mark it:** two things, and the second one is the real one. **One — are the predictions in pen, and do some of them have crosses?** A page of twelve ticks in pencil is not evidence of anything. **Two — does every cross have a sentence that names what they thought?** That sentence is the entire objective of this week. A student who wrote "I said (3,) because there are three numbers in it — it's (3, 1) because each number is in its own inner list, and an inner list is a row" has understood something they will need badly in Week 18, and they have understood it because they were wrong first.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 17.1 — List or array?

*For each statement, say whether it is true of a list, an array, or both.*

| # | Statement | List | Array |
|---|---|---|---|
| (a) | Can hold `[1, "cat", 3.5, True]` all at once | ✔ | ✘ — one kind only |
| (b) | Knows how many rows and columns it has | ✘ — only a length | ✔ |
| (c) | Prints with commas between the values | ✔ | ✘ — spaces |
| (d) | You can `.append` to it | ✔ | ✘ — a fixed size |
| (e) | Has a `.dtype` | ✘ | ✔ |
| (f) | Comes with Python; nothing to install | ✔ | ✘ — numpy is installed separately |
| (g) | Holds its values end to end with nothing in between | ✘ | ✔ |
| (h) | You build it from square brackets | ✔ | ✔ — but through `np.array([...])` |

**17.1(i) In one sentence, what does an array cost you that a list of dictionaries does not?**
**The labels.** An array is only numbers, so nothing in it says which column is which or whose row is whose — and if you get a column wrong, you get a wrong number rather than an error.

**17.1(j) In one sentence, what does an array give you that a list cannot?**
It knows its own **shape**, every value is the same **kind**, and (from next week) it can do arithmetic to all of its numbers in one line.

**17.1(k) You need to collect numbers one at a time as a program runs, then do maths to all of them. Which do you use, and when do you switch?**
Collect into a **list**, because a list grows and an array does not. Then `np.array(...)` it **once**, at the end, when the collecting is finished. This is exactly what `np.array(column(squad, "runs"))` does.

### Page 17.2 — Predict the shape

*Fill in the prediction column in pen, before running anything.*

| # | The array | Predicted shape | Actual shape |
|---|---|---|---|
| (a) | `np.array([10, 20, 30])` | | `(3,)` |
| (b) | `np.array([[1, 2, 3], [4, 5, 6]])` | | `(2, 3)` |
| (c) | `np.array([2.5, 3.5, 4.5, 5.5])` | | `(4,)` |
| (d) | `np.array([1, 2, 3.0])` | | `(3,)` |
| (e) | `np.array([[7], [8], [9]])` | | `(3, 1)` ← **the miss** |
| (f) | `np.array([True, False, True])` | | `(3,)` |

**17.2(g) Which of the six did you get wrong, and why?**
Almost always **(e)**. The expected wrong answer is `(3,)`, on the grounds that there are three numbers. The truth: each number is inside **its own inner list**, and an inner list is a row. So it is three rows of one column each — `(3, 1)`. A column, standing up.

**17.2(h) How many numbers are in an array with shape `(3, 1)`? And in one with shape `(1, 3)`?**
**Three, both times.** Same numbers, different arrangement. One is a column, the other is a row. They are not the same array, and next week that difference will produce nine numbers where you wanted three.

**17.2(i) Write out, in brackets, the list-of-lists you would type to get shape `(2, 4)`.**

```python
np.array([[1, 2, 3, 4],
          [5, 6, 7, 8]])
```

Two inner lists (two rows), four numbers in each (four columns).

### Page 17.3 — Predict the dtype

| # | The array | Predicted dtype | Actual dtype |
|---|---|---|---|
| (a) | `np.array([10, 20, 30])` | | `int64` |
| (b) | `np.array([[1, 2, 3], [4, 5, 6]])` | | `int64` |
| (c) | `np.array([2.5, 3.5, 4.5, 5.5])` | | `float64` |
| (d) | `np.array([1, 2, 3.0])` | | `float64` ← **the miss** |
| (e) | `np.array([[7], [8], [9]])` | | `int64` |
| (f) | `np.array([True, False, True])` | | `bool` |
| (g) | `np.array([1, 2, "three"])` | | `<U21` ← **the other miss** |

**17.3(h) State the rule that explains both (d) and (g) in one sentence.**
**numpy picks the one kind that can hold every value without losing anything.** A whole-number box cannot hold `3.0`'s decimal point, so `(d)` becomes decimals. Nothing numeric can hold the word `three`, and text can hold `1` as the character `1`, so `(g)` becomes text.

**17.3(i) In (g), what happened to the `1` and the `2`?**
They became **text**: `'1'` and `'2'`. Printed output is `['1' '2' 'three']` — note the quote marks. They are no longer numbers and arithmetic on them will either crash or glue characters together.

**17.3(j) Where have you seen this exact failure before?**
**Week 16.** `48` was written to a CSV and came back as `'48'`. Same failure: a container that can only hold one kind of thing turned the numbers into writing, and said nothing about it. Same check, too: read the type.

**17.3(k) Why is `float64` in (d) not a bug?**
Because nothing was lost. `1` stored as `1.0` is the same number written differently. Compare it with `(g)`, where `1` stored as `'1'` genuinely **is** a loss — you cannot add one to it any more.

### Page 17.4 — Build six, check six

The six homework arrays and their real output:

```python
"""hw17.py - the six homework arrays. Predict shape and dtype FIRST."""

import numpy as np

a = np.array([7, 7, 7, 7, 7, 7])
b = np.array([[1.5, 2.5],
              [3.5, 4.5],
              [5.5, 6.5]])
c = np.array([0])
d = np.array([[1, 2, 3, 4]])
e = np.array([100, 200, 300.0, 400])
f = np.array(["pop", "rock", "folk"])

print(f"{'array':<8}{'shape':<10}{'dtype':<10}{'ndim'}")
print("-" * 34)
for name, arr in [("a", a), ("b", b), ("c", c), ("d", d), ("e", e), ("f", f)]:
    print(f"{name:<8}{str(arr.shape):<10}{str(arr.dtype):<10}{arr.ndim}")
```

Real output:

```text
array   shape     dtype     ndim
----------------------------------
a       (6,)      int64     1
b       (3, 2)    float64   2
c       (1,)      int64     1
d       (1, 4)    int64     2
e       (4,)      float64   1
f       (3,)      <U4       1
```

**The answer table, with what to say about each:**

| # | Shape | Dtype | What this one is teaching |
|---|---|---|---|
| `a` | `(6,)` | `int64` | The easy one. Six whole numbers, one direction. |
| `b` | `(3, 2)` | `float64` | Three inner lists, two numbers each. Rows first. Every value has a decimal point, so `float64` is no surprise. |
| `c` | `(1,)` | `int64` | **A common miss.** One number in a list is still an array, and its shape is `(1,)` — not `1`, and not `()`. One slot, in one direction. |
| `d` | `(1, 4)` | `int64` | **A common miss.** The double brackets make it *one row of four*, which is a different thing from `np.array([1, 2, 3, 4])` with shape `(4,)`. Same four numbers, different shape. |
| `e` | `(4,)` | `float64` | **The designed miss.** Three whole numbers and one `300.0`, and the single decimal decides it for all four. Same rule as page 17.3(d). |
| `f` | `(3,)` | `<U4` | Text on purpose, so it is not a mistake. `<U4` because `"rock"` and `"folk"` are the longest at four characters. |

**17.4(a) Compare `c` and `a`. What is the same, and what is different?**
Both are 1-D — both shapes have one number in them, so both are a single row. `a` has six slots, `c` has one. `(1,)` is a perfectly ordinary array that happens to have one number in it.

**17.4(b) Compare `d` with `np.array([1, 2, 3, 4])`. Same numbers?**
**Yes — same four numbers, different shape.** `d` is `(1, 4)`: one row, four columns, and it is 2-D. The other is `(4,)`: four numbers in one direction, and it is 1-D. The extra pair of brackets is the whole difference. This distinction does nothing today and matters enormously in Week 19.

**17.4(c) Which of your twelve predictions did you get wrong? Write a sentence for each.**

Model sentences for the three designed misses:

> *"I said `c` would have shape `1`. It's `(1,)`, because a shape is always a collection of sizes, one per direction — even when there's only one direction and only one number in it."*

> *"I said `d` would be `(4,)`. It's `(1, 4)`, because there are two sets of brackets: the outer one is the array and the inner one is a row. So it's one row of four, not four numbers on their own."*

> *"I said `e` would be int64 because three of the four numbers are whole. It's float64, because the array only gets one kind and it has to be able to hold `300.0` without throwing the decimal away."*

**Mark the sentences, not the ticks.** Full marks needs *what I thought* and *what is true*, both present.

### Page 17.5 — Your own three

*Build three arrays of your own — one 1-D, one 2-D, and one that you expect to come out `float64`. Predict, then check.*

Model answer, using the twelve records from Week 14:

```python
"""mine17.py - three arrays of my own, from my own data."""

import numpy as np

from records import column
from squad_data import squad

# 1-D: one column of the table
runs = np.array(column(squad, "runs"))
print("runs :", runs)
print("shape:", runs.shape, " dtype:", runs.dtype)

# 2-D: two columns, one row per player
tall = np.array([[r["runs"], r["balls"]] for r in squad])
print("tall shape:", tall.shape, " dtype:", tall.dtype)

# a float64 one on purpose: overs bowled are decimals, so store decimals
overs = np.array([3.2, 4.0, 5.5, 6.1])
print("overs:", overs)
print("shape:", overs.shape, " dtype:", overs.dtype)
```

Real output:

```text
runs : [ 48  12  77   5  63  30   0  41  55  22  90 104]
shape: (12,)  dtype: int64
tall shape: (12, 2)  dtype: int64
overs: [3.2 4.  5.5 6.1]
shape: (4,)  dtype: float64
```

*(Their shapes will be their own numbers. Check the first number of the 2-D shape against how many records they have, not against this page.)*

**Mark:** the 1-D shape has one number in it and matches the number of values; the 2-D shape has two numbers in it, rows first, and the first number matches the number of inner lists; the float array's dtype really is `float64`. Anyone who used `column()` from their own `records.py` gets a tick for reusing their own tool.

**17.5(a) Your 2-D array — what does each of the two numbers in the shape mean, for your data?**
Model: *"`(12, 2)` — twelve rows because there are twelve players, and two columns because I put runs and balls in each row."* The words *"because"* twice is what you are marking.

**17.5(b) What is not in your 2-D array that was in the original records?**
The **names**, the **teams**, and the **out** column — everything that was words. And the column headings. Nothing in the array says the second column is balls; only a comment does.

### Page 17.6 — Which of your columns could be an array?

*Look at your Week 16 dataset. For each of your five columns, could it go into a numeric array on its own?*

Model answer, for the thirty-song playlist:

| Column | Into a numeric array? | Why |
|---|---|---|
| `title` | no | words — it would give a `<U` text array, and there is no arithmetic to do on it |
| `artist` | no | words, and it is a category — this is what you group by, which arrays cannot do |
| `genre` | no | words, and a category |
| `minutes` | **yes** | decimal numbers — `float64` |
| `plays` | **yes** | whole numbers — `int64` |

**17.6(a) Write one sentence explaining the pattern.**
Model answer:

> *"The columns that can go into a numeric array are the ones I would do arithmetic on — add up, average, compare. The ones that can't are words, and the words are exactly the ones I need for grouping and for knowing which row is which."*

**17.6(b) Could you put all five columns into one array?**
Only by turning everything into text, which would make `plays` unusable for arithmetic — the `<U21` problem, deliberately, across the whole table. **So no, not usefully.** Which is exactly the gap `pandas` fills in Week 21: a table where one column can be words and another can be numbers.

### Answers to every question posed in the lesson

- *"What have you lost by rubbing out the words?"* → The labels: which column is which, and whose row is whose.
- *"What have you gained?"* → A perfect rectangle with no gaps, and every cell holding the same kind of thing.
- *"Rows or columns first?"* → Rows. Always. `(12, 3)` is twelve rows, three columns.
- *"Why couldn't we keep the names in the block?"* → Because then some cells would hold words and some would hold numbers, and an array holds one kind only.
- *"Is `(12, 3)` the same as `(3, 12)`?"* → No. Same numbers, different arrangement, different array.
- *"What can a list hold that an array can't?"* → Different kinds of thing at the same time.
- *"What does `as np` do?"* → Gives numpy a shorter name, inside this file only.
- *"Why does `(4,)` have a comma?"* → Because it is a collection with one item in it, not just the number four in brackets.
- *"What's the difference between `type()` and `.dtype`?"* → `type()` asks about one value; `.dtype` asks about every value at once, and gets one answer because there is only one answer.
- *"What happens if one cell has a word in it?"* → Every cell becomes text.
- *"What do you expect from `np.array(48, 12, 77, 5)`?"* → `TypeError` — it takes one thing (a list) and you gave it four numbers.
- *"Which column is balls?"* → The second one, and **only the comment says so.** Nothing in the array does.
- *"Shape and dtype of `np.array([3.2, 4.0, 5.5])`?"* → `(3,)` and `float64`. And `4.0` prints as `4.` — the dot is numpy telling you it is a decimal.
- *"Will `np.array([1, 2, "three"])` crash?"* → No. It gives `['1' '2' 'three']` with dtype `<U21`, and says nothing.
- *"Where have you seen this before?"* → Week 16. `48` went into a CSV and came back as `'48'`. Same failure, same check.
- *"Is the ragged-block error good news or bad news?"* → Good news. numpy could have padded the short row with a made-up zero and carried on; refusing is kinder.
- *"What does `inhomogeneous` mean?"* → Not all the same. Here: the rows are not all the same length, so there is no shape.

---

## 🔮 Next Week Preview

Next week is the Term 2 checkpoint, and it has a party in it. **The Loop Retirement Party.** Eight loops from Weeks 7 to 15 go on eight cards, laid out on the table, and one at a time the student rewrites each as a single line of array maths — `scores * 2`, `runs + balls`, `celsius * 9 / 5 + 32` — runs *both* versions, and checks that the outputs are identical, character for character. Any card whose two versions disagree goes in a "revisit" pile, and that pile is the term's honest report on itself. The new syntax is tiny: arithmetic straight onto an array, and two functions that build arrays without typing the numbers, `np.arange` and `np.zeros`. And at the end there is a sting that is the exact mirror of this week's `<U21`: two arrays of three numbers are added together, nothing crashes, and **nine numbers come out.** The student has to catch it by printing the answer's shape — which is precisely the habit this week was building.

**Prep early:** three things. **Write the eight loop cards tonight** — index cards, one loop per card, copied out of the student's own Week 7 to Week 15 files if you still have them, because a loop they wrote themselves retires far more satisfyingly than one from a book. **Make sure numpy really is working**, because Week 18 is a numpy lab and there is no paper version of it; if this week ran on graph paper, the install is now the most urgent thing on your list. And **have the Bug Log to hand with the `<U21` entry findable**, because next week's silent bug is the same shape and the best thing you can do is have the student find their own note about it and say "this again".

---

[⬅ Week 16](week-16.md) · [Course Home](../README.md) · [Week 18 ➡](week-18.md) · [Student Guide](../student-guide/week-17.md) · [Workbook](../workbook/week-17.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
