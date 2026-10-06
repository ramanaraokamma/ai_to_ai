# Week 18 — Term 2 Checkpoint: Eight Loops You Never Have to Write Again

[⬅ Week 17](week-17.md) · [Course Home](../README.md) · [Week 19 ➡](week-19.md) · [Student Guide](../student-guide/week-18.md) · [Workbook](../workbook/week-18.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟪 Review — the Loop Retirement Party, and an honest list of what needs going back over |
| **Big idea** | Array maths replaces a whole `for` loop with one line, and the one line is easier to read **and** harder to get wrong. |
| **New vocabulary** | vectorized · elementwise · broadcasting · arange · silent success |
| **New syntax** | `arr * 2` · `arr1 + arr2` · `np.arange(n)` · `np.zeros((r, c))` |
| **Materials** | **Eight index cards, one loop written on each** (see Prep — write these the night before) · a "revisit" tray or just a marked-out space on the table · printed workbook pages 18.1–18.6 · the Bug Log from all of Term 2 · the student's Week 7–15 Python files, open |
| **Tech needed** | Laptop with Python 3 **and numpy working**. There is no paper version of this lesson — if numpy is not installed, stop and fix that instead, and do this lesson next week. |
| **Prep time** | 25 minutes the night before (15 of them are writing the eight cards) · 5 minutes on the day |

> **⚠️ Watch out:** the last thing that happens in this lesson is a sum that produces **nine numbers when three were wanted**, and does not complain. Do not warn them. The student must catch it by printing the answer's shape — which is exactly the habit Week 17 was building — and if you tip them off, the habit does not get tested.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Rewrite a `for` loop as one line of array maths** and get byte-identical output.
2. **Add and multiply two arrays elementwise**, and say what must be true of their shapes.
3. **Build arrays with `np.arange` and `np.zeros`** instead of typing the numbers.
4. **Explain how broadcasting can silently do something you did not mean.**
5. **Produce a list of the weeks that need revisiting** — their own, written down, with reasons.

Observable evidence: eight loops rewritten as one-liners with `identical? True` printed beside each; a `(3, 3)` shape spotted and explained; a completed Term 2 reflection sheet; and a written "revisit" list naming specific weeks and specific reasons.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**This is a review week with one new idea in it.** The new idea is small and it is the payoff for everything since Week 7. Read this section once and you can run the whole lesson.

### 1. The whole idea, in one comparison

Here is a loop the student has written many times since Week 7:

```python
doubled_loop = []                        # start with an empty list
for score in scores:                     # visit every score once
    doubled_loop.append(score * 2)       # double it and add it to the list
```

And here is the same job, on an array:

```python
doubled_line = score_arr * 2
```

That is the entire lesson. One line for four. And the argument for it is not mainly that it is shorter.

> **vectorized** — an operation written on a whole array at once, with the visiting-every-item done inside numpy instead of by your loop.

**Count the places you can go wrong in each version.** The loop has four:

1. forgetting `doubled_loop = []`, or putting it inside the loop by accident;
2. writing `scores` where you meant `doubled_loop` in the `.append`;
3. getting the indentation wrong so the append happens outside the loop;
4. forgetting to use the result and printing the wrong variable.

Every one of those is a real mistake your student has actually made this term, and three of the four produce no error message. The one-liner has **one** place to go wrong: the formula.

That is the real argument, and it is the one to make to a 12-year-old: **the one-liner is not just shorter, it is a smaller target.** The four lines of loop are not the interesting part of the job — they are the *machinery of visiting things*, and machinery you type by hand is machinery you can get wrong.

![Four lines become one, and the answer does not move](../figures/fig-w18-1-loop-becomes-one-line.svg)
*Figure 18.1 — Both give 96 24 154 10 126 60. Not nearly. Exactly.*

### 2. Elementwise: two arrays, position by position

> **elementwise** — the operation is done to each matching pair of positions on its own. Position 0 with position 0, position 1 with position 1, and stop.

```python
score_arr = np.array([48, 12, 77, 5, 63, 30])
balls_arr = np.array([32, 20, 55, 9, 41, 28])
print(score_arr + balls_arr)
```

```text
[ 80  32 132  14 104  58]
```

48 + 32 = 80. 12 + 20 = 32. Hand-check the first two in front of the student; it takes ten seconds and it converts "magic" into "arithmetic".

**The one thing that must be true:** the two arrays must line up. Six and six works. Six and four does not — give it six runs and only four ball-counts and it stops:

```text
ValueError: operands could not be broadcast together with shapes (6,) (4,)
```

**Say that this error is good news**, in exactly the same words you used last week for the ragged block. numpy could have stopped at the fourth pair and given you a short answer, or padded with zeros. It refused, because there is no honest answer.

![Elementwise means position by position](../figures/fig-w18-2-elementwise-pairing.svg)
*Figure 18.2 — Cell 0 only ever meets cell 0. It never meets cell 3.*

**And `*` does not mean what a mathematician might expect.** `a * b` on two arrays multiplies position by position — it is *not* the matrix multiplication from senior maths. If a parent with a maths degree looks over your shoulder and frowns, that is why. Elementwise is all this course ever needs.

### 3. Broadcasting: when the shapes are not the same and it works anyway

Why does `score_arr * 2` work at all? Six numbers and one number are not the same shape.

> **broadcasting** — numpy's rule for making two different shapes work together, by reusing the smaller one wherever it is short.

The analogy is a shop sign. A pizza shop puts **10% off everything** on one big sign in the window. It does not write "10% off" on four hundred separate price tags. Everyone understands the sign applies to every item. Broadcasting is the sign — and numpy does not actually copy the number two six times in memory, it just reads the same value over and over, which is why it costs nothing.

The everyday cases are all completely safe:

| What you write | Shapes | What happens |
|---|---|---|
| `arr * 2` | `(6,)` and one number | the 2 is reused for all six |
| `arr + 5` | `(6,)` and one number | the 5 is reused for all six |
| `arr1 + arr2` | `(6,)` and `(6,)` | pair by pair, no reusing needed |
| `celsius * 9 / 5 + 32` | `(4,)` and three single numbers | the whole formula, applied to every cell |

And then there is the case that is the sting of this lesson.

### 4. The silent success — the one thing to plant on purpose

> **silent success** — code that runs, prints an answer, and is wrong. No error, no warning.

Here it is. Three scores, and three bonuses — but the bonuses were typed with one set of brackets too many, so they came out as a column instead of a row:

```python
scores = np.array([48, 12, 77])          # shape (3,)
bonus = np.array([[1],                   # shape (3, 1)  <- a COLUMN
                  [2],
                  [3]])
answer = scores + bonus
print(answer)
print("answer.shape:", answer.shape)
```

```text
[[49 13 78]
 [50 14 79]
 [51 15 80]]
answer.shape: (3, 3)
```

**Three numbers plus three numbers gave nine numbers.** Nothing crashed. Nothing warned.

What happened: numpy lined the shapes up from the right, saw a `(3,)` and a `(3, 1)`, found a `1` in the bonus's column direction and a missing direction in the scores' row direction, and reused both to fill a 3×3 grid. Every row of the grid is the scores plus one bonus. The three answers the student actually wanted — 49, 14, 80 — are in there, sitting on the diagonal, surrounded by six numbers that mean nothing.

![Broadcasting stretched it, and nothing complained](../figures/fig-w18-3-broadcasting-stretch.svg)
*Figure 18.3 — The extra brackets made a column, not a row, and broadcasting was happy to stretch both.*

**The fix, at this level, is to retype the brackets:**

```python
bonus = np.array([1, 2, 3])              # shape (3,)  - one set of brackets
print(scores + bonus)
```

```text
[49 14 80]
```

*(There is a function called `reshape` that does this without retyping. Do not teach it. Retyping the brackets makes the student look at the brackets, which is where the mistake was.)*

**And the check that catches it is the one thing to take out of this lesson:**

> **Print the shape of the answer. Three numbers in should not give nine out.**

This is Week 17's habit — print `.shape` — arriving with a reason. Last week it was hygiene. This week it is the only thing between the student and a wrong answer.

### 5. Two ways to build an array without typing the numbers

Both replace a loop, which is why they are here.

**`np.arange(n)` — the counting numbers.**

```python
print(np.arange(6))
```

```text
[0 1 2 3 4 5]
```

> **arange** — "array range". Builds the counting numbers, starting at 0, stopping **before** the number you gave it.

It is `range()` from Week 7, producing an array instead of something you have to loop over. And it has the same off-by-one to talk about: `np.arange(6)` gives six numbers, **0 to 5**, not 1 to 6. Ask "how many numbers, and what's the last one?" and make them answer both. Six, and five.

The loop it retires:

```python
numbers = []
for i in range(6):
    numbers.append(i)
```

**`np.zeros((r, c))` — a blank block of a given shape.**

```python
print(np.zeros((2, 3)))
```

```text
[[0. 0. 0.]
 [0. 0. 0.]]
```

Two things students trip over, and both are worth saying before they happen:

- **The double brackets are compulsory.** `np.zeros((2, 3))` — the inner pair is the *shape*, which is one thing, a pair of numbers. `np.zeros(3, 4)` gives `TypeError: Cannot interpret '4' as a data type`, because the second slot in `np.zeros` is for the dtype, and `4` is not a dtype. Baffling message; easy fix; worth planting.
- **The zeros come out as decimals.** `0.` with a dot. `np.zeros` gives `float64` by default, because a blank you are about to fill with real measurements is far more often decimals than whole numbers. Print `.dtype` and read it — that is Week 17 paying for itself again.

The loop it retires is a loop inside a loop, which is the most error-prone shape in the whole of Term 2:

```python
grid = []
for row in range(2):
    this_row = []
    for col in range(3):
        this_row.append(0.0)
    grid.append(this_row)
```

Six lines and two indent levels, replaced by one short line.

### 6. What "identical" means, and the trap in checking it

The student is going to run both versions of eight loops and check they agree. Here is the thing that will confuse them, and you should be ready for it:

```python
print("loop:", doubled_loop)
print("line:", doubled_line)
```

```text
loop: [96, 24, 154, 10, 126, 60]
line: [ 96  24 154  10 126  60]
```

**Those two lines look different.** One has commas; the other has spaces and some padding. A student comparing them by eye will say "no, they're not identical" and they will be *right about the printing and wrong about the numbers.*

The check that actually answers the question:

```python
print("identical?", list(doubled_line) == doubled_loop)
```

```text
identical? True
```

`list(...)` turns the array back into a plain list so that like is compared with like. **And the reason the printing differs at all is Week 17's lesson:** a list prints with commas, an array prints with spaces and lines its columns up. Same six numbers, two different kinds of container, two different ways of showing themselves.

Make this explicit, out loud, once. Otherwise half the class will spend the lab believing their correct answers are wrong.

### 7. Not every loop retires, and that is worth teaching

Do not let the lesson become "loops are bad". They are not, and three of the loops your student wrote this term cannot be replaced with anything they know:

| The loop | Can it retire today? | Why |
|---|---|---|
| Double every number | **yes** | `arr * 2` |
| Add two columns together | **yes** | `arr1 + arr2` |
| Build the numbers 0 to n | **yes** | `np.arange(n)` |
| Total a column | **yes** | `sum(arr)` — Python's own `sum`, from Week 12, works fine on an array |
| Keep only the scores above 50 | **not yet** | needs a boolean mask — **Week 20** |
| Count how many players per team | **no** | needs the team *names*, which an array does not have. This one belongs to a dictionary, forever. |
| Ask the user for a guess until they get it right | **no** | a `while` loop waiting on a human. Arrays have nothing to say about it. |
| Print a formatted table row by row | **no** | that is output, not arithmetic. |

**The honest rule:** array maths retires loops that do **arithmetic to every number**. It does nothing for loops that make decisions about text, wait for people, or produce printed output. A student who leaves with "loops are for people and text, arrays are for numbers" has a genuinely useful heuristic.

### 8. The review half: what this checkpoint is really for

This is the second of three checkpoints, and its job is not to teach. It is to produce **an honest list of what needs going back over**, written by the student, before Term 3 stacks pandas and charts and models on top.

The mechanism is the Loop Retirement Party, and it is diagnostic on purpose. When a student cannot rewrite a loop as one line, the reason is almost never "they don't know `arr * 2`". It is one of these:

| Card won't retire | The real gap | Go back to |
|---|---|---|
| Cannot say what the loop *did* | reading a loop | **Week 7** |
| Cannot find the accumulator | `total += x` | **Week 7** |
| Cannot get the numbers out of the records | comprehensions | **Week 14–15** |
| Turns the list into an array and then loops over it anyway | what an array is *for* | **Week 17** |
| Cannot predict the shape | `.shape` | **Week 17** |
| The one-liner runs but the outputs differ | reading output carefully | today, §6 |

**That table is the actual output of this week.** The eight one-liners are the vehicle.

![The Term 2 ladder, rung by rung](../figures/fig-w18-4-term2-ladder-so-far.svg)
*Figure 18.4 — Anything on this ladder that wobbles is a rung to go back and stand on again.*

### 9. The three misconceptions you will actually meet

**Misconception 1 — "the printing is different so the answers are different."**
`[96, 24, 154]` versus `[ 96  24 154]`. Address it before the lab starts, with `list(arr) == loop_result` on the screen, or you will spend the lab on it.

**Misconception 2 — "`arr * 2` works on lists too."**
It does something. `[48, 12, 77] * 2` gives `[48, 12, 77, 48, 12, 77]` — the list repeated. Six numbers become twelve, and **nothing complains.** This is the single most common numpy mistake in the world, and it is worth planting deliberately because the fix is to notice you forgot `np.array()`.

**Misconception 3 — "if it ran, the shapes must have been right."**
The `(3, 3)` answer is the whole antidote. Shapes that are wrong sometimes stop you and sometimes quietly give you more numbers than you asked for. The only defence is printing the shape.

### 10. How deep to go, and where to stop

**Go this far:** `arr * 2`, `arr + 5`, `arr ** 2`, `arr1 + arr2`, `arr1 / arr2`, a full formula like `celsius * 9 / 5 + 32`; `np.arange(n)`; `np.zeros((r, c))`; `sum(arr)`; the `list(...) == ...` identity check; the `(3,)` + `(3, 1)` sting; and the reflection sheet with a revisit list.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `arr[1, 2]`, `arr[:, 0]` — two-number indexing and slicing | **Week 19** |
| `arr.mean(axis=0)`, `arr.sum(axis=1)` | **Week 19.** `sum(arr)` on a 1-D array is fine and needs no axis. |
| `arr > 50` and boolean masks | **Week 20.** This is the answer to "how do I keep only the big ones?" and it is one week away. Say so and move on. |
| `.reshape()` | Not this term. Retyping the brackets teaches more. |
| `np.ones`, `np.full`, `np.linspace`, `np.random` | Mention `np.ones` in one line if asked. `linspace` belongs with drawing curves in Week 25. |
| Matrix multiplication, `@`, dot products | Not in Level 2. If a parent raises it, `*` is elementwise and that is deliberate. |
| Timing comparisons as a main activity | Fine as an extension. It is a nice fact and it is not this week's objective. |

The line to hold in your head all lesson: **today is the week the student learns that a wrong shape can be worse than a crash.** Everything else is a shorter way of writing what they can already write.

---

### 11. 🧭 The Growing Map — two minutes to close Term 2

The student guide carries one figure that is not about this week's content: the same pipeline every
week, with one more piece filled in. On a checkpoint week it does a second job as well — it is the only
honest picture of how far through the year the student actually is.

![The Level 2 pipeline in Week 18: the last week inside the dicts, rows and files tile, and Term 2 closes with eight loops retired](../figures/fig-w18-0-where-this-fits.svg)

*Figure 18.0 — Week 18's version. Sixth and last week inside the `dicts · rows · files` tile, weeks 13
to 18. Two threads lit: toolcraft and representation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask this week's question:** *"the picture is identical to last week's. Name the thing
   that changed, that a picture cannot show."* You want something close to *"the same job now takes one
   line instead of five."* Follow it with the count — *how many loops did we retire?* **Eight.** Have
   them say the number; it is the deliverable and it deserves saying out loud.
2. **Then the arithmetic that makes a checkpoint honest:** *"we are eighteen weeks into thirty-six —
   count the solid boxes."* Two stages of five, four tiles of ten. They will spot that they are half way
   through the year and not half way across the map, and they should hear from you why that is fine:
   stages three to five move faster *because* Term 2 was slow. Said now, it prevents a term of quiet
   worry.
3. **Have them add the retirement list to their own copy** — the eight loops in the margin beside the
   gold tile, crossed out. It is the most satisfying annotation of the year and it takes thirty seconds.

> **🧑‍🏫 Why this is worth two minutes.** Review weeks feel like nothing happened, because no new box
> lights up. The map lets you show progress that is real but invisible: the box is the same, the code
> inside it is a fifth of the length, and their own "revisit" list is the other half of the checkpoint. A
> learner who ends Term 2 believing they stood still starts Term 3 defensive.

> **⚠️ Watch out:** the "half way through the year, not half way across the map" line is reassurance, not
> a target. Do not let it turn into a pace warning.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Check numpy still works.** Four seconds: `python3 -c "import numpy; print(numpy.__version__)"`. If it fails, **do not run this lesson** — fix the install and do a Week 17 consolidation instead. There is no paper version of a numpy lab.
- [ ] **Print workbook pages 18.1–18.6.**
- [ ] **Write the eight loop cards. This is the lesson and it takes fifteen minutes.** Eight index cards, one loop per card, in the student's own handwriting if possible — and **wherever you can, copy the loop out of their actual Week 7 to Week 15 files.** A loop they wrote themselves retires far more satisfyingly than one from a book.

If their files are gone, these eight work:

```
CARD 1   doubled = []
         for score in scores:
             doubled.append(score * 2)

CARD 2   bumped = []
         for score in scores:
             bumped.append(score + 5)

CARD 3   squares = []
         for score in scores:
             squares.append(score ** 2)

CARD 4   fahrenheit = []
         for c in celsius:
             fahrenheit.append(c * 9 / 5 + 32)

CARD 5   totals = []
         for i in range(len(scores)):
             totals.append(scores[i] + balls[i])

CARD 6   rates = []
         for i in range(len(scores)):
             rates.append(scores[i] / balls[i] * 100)

CARD 7   numbers = []
         for i in range(10):
             numbers.append(i)

CARD 8   grid = []
         for row in range(3):
             this_row = []
             for col in range(4):
                 this_row.append(0.0)
             grid.append(this_row)
```

- [ ] **Mark out a "revisit" space** on the table — a tray, a plate, or a rectangle of paper with REVISIT written on it. Cards that fail go there, physically. It matters that it is physical.
- [ ] **Type and run the code yourself.** One file, `retire.py`:

```python
"""retire.py - eight loops from weeks 7-15, retired. Both versions, then the proof."""

import numpy as np

# ---------------------------------------------------------------- the data
scores = [48, 12, 77, 5, 63, 30]                 # six scores, typed by hand
balls = [32, 20, 55, 9, 41, 28]                  # balls faced by the same six
celsius = [21.0, 24.5, 30.0, 18.5]               # four temperatures

score_arr = np.array(scores)
balls_arr = np.array(balls)
celsius_arr = np.array(celsius)

print("=" * 60)

# --- LOOP 1: double every score -----------------------------------------
loop1 = []
for s in scores:
    loop1.append(s * 2)
line1 = score_arr * 2
print("1  double every score")
print("   loop:", loop1)
print("   line:", line1)
print("   identical?", list(line1) == loop1)

# --- LOOP 2: give everyone 5 bonus runs ---------------------------------
loop2 = []
for s in scores:
    loop2.append(s + 5)
line2 = score_arr + 5
print("2  add 5 to every score")
print("   loop:", loop2)
print("   line:", line2)
print("   identical?", list(line2) == loop2)

# --- LOOP 3: square every score ----------------------------------------
loop3 = []
for s in scores:
    loop3.append(s ** 2)
line3 = score_arr ** 2
print("3  square every score")
print("   loop:", loop3)
print("   line:", line3)
print("   identical?", list(line3) == loop3)

# --- LOOP 4: celsius to fahrenheit -------------------------------------
loop4 = []
for c in celsius:
    loop4.append(c * 9 / 5 + 32)
line4 = celsius_arr * 9 / 5 + 32
print("4  celsius to fahrenheit")
print("   loop:", loop4)
print("   line:", line4)
print("   identical?", list(line4) == loop4)

# --- LOOP 5: runs plus balls, position by position ---------------------
loop5 = []
for i in range(len(scores)):
    loop5.append(scores[i] + balls[i])
line5 = score_arr + balls_arr
print("5  runs + balls, pair by pair")
print("   loop:", loop5)
print("   line:", line5)
print("   identical?", list(line5) == loop5)

# --- LOOP 6: strike rate = runs / balls * 100 -------------------------
loop6 = []
for i in range(len(scores)):
    loop6.append(scores[i] / balls[i] * 100)
line6 = score_arr / balls_arr * 100
print("6  strike rate for each player")
print("   loop:", [round(x, 2) for x in loop6])
print("   line:", np.round(line6, 2))
print("   identical?", list(line6) == loop6)

# --- LOOP 7: build the numbers 0 to 9 ---------------------------------
loop7 = []
for i in range(10):
    loop7.append(i)
line7 = np.arange(10)
print("7  the numbers 0 to 9")
print("   loop:", loop7)
print("   line:", line7)
print("   identical?", list(line7) == loop7)

# --- LOOP 8: an empty 3-row, 4-column grid ---------------------------
loop8 = []
for row in range(3):
    this_row = []
    for col in range(4):
        this_row.append(0.0)
    loop8.append(this_row)
line8 = np.zeros((3, 4))
print("8  an empty 3 by 4 grid")
print("   loop:", loop8)
print("   line:")
print(line8)
print("   identical?", [list(r) for r in line8] == loop8)
print("=" * 60)
```

Run `python3 retire.py`. You must see **exactly**:

```text
============================================================
1  double every score
   loop: [96, 24, 154, 10, 126, 60]
   line: [ 96  24 154  10 126  60]
   identical? True
2  add 5 to every score
   loop: [53, 17, 82, 10, 68, 35]
   line: [53 17 82 10 68 35]
   identical? True
3  square every score
   loop: [2304, 144, 5929, 25, 3969, 900]
   line: [2304  144 5929   25 3969  900]
   identical? True
4  celsius to fahrenheit
   loop: [69.8, 76.1, 86.0, 65.3]
   line: [69.8 76.1 86.  65.3]
   identical? True
5  runs + balls, pair by pair
   loop: [80, 32, 132, 14, 104, 58]
   line: [ 80  32 132  14 104  58]
   identical? True
6  strike rate for each player
   loop: [150.0, 60.0, 140.0, 55.56, 153.66, 107.14]
   line: [150.    60.   140.    55.56 153.66 107.14]
   identical? True
7  the numbers 0 to 9
   loop: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   line: [0 1 2 3 4 5 6 7 8 9]
   identical? True
8  an empty 3 by 4 grid
   loop: [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
   line:
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
   identical? True
============================================================
```

**Eight Trues.** Note how different the `loop:` and `line:` printing looks in cards 1, 3, 4, 5 and 6, and how the `identical?` line settles it. That contrast is the thing you must set up before the lab, or you will spend the lab on it.

- [ ] **Run the sting yourself**, in its own file, and let it annoy you:

```python
"""bonus18.py - three scores, three bonuses, and nine answers."""

import numpy as np

scores = np.array([48, 12, 77])          # three scores
bonus = np.array([[1],                   # three bonuses... one per line
                  [2],
                  [3]])

print("scores.shape:", scores.shape)
print("bonus.shape :", bonus.shape)

answer = scores + bonus
print(answer)
print("answer.shape:", answer.shape)
print("we put in 3 and 3. How many came out?")
```

```text
scores.shape: (3,)
bonus.shape : (3, 1)
[[49 13 78]
 [50 14 79]
 [51 15 80]]
answer.shape: (3, 3)
we put in 3 and 3. How many came out?
```

- [ ] **Break three more things on purpose**, so you have met each message:
  1. `print([48, 12, 77] * 2)` on a plain list → `[48, 12, 77, 48, 12, 77]`, silently.
  2. `print([48, 12, 77] + 5)` on a plain list → `TypeError: can only concatenate list (not "int") to list`.
  3. `np.zeros(3, 4)` → `TypeError: Cannot interpret '4' as a data type`.
- [ ] **Read your whole Term 2 Bug Log**, Weeks 10 to 17, and pick the **three entries you think were the most valuable.** You are going to ask the student for their three, and you want yours ready.
- [ ] **Delete or rename `retire.py`.** They write it, card by card.

### 5 minutes on the day

- [ ] Editor open, terminal in the same folder, numpy proven working.
- [ ] **The eight cards face down in a stack** in the middle of the table. The REVISIT space marked out beside them.
- [ ] The student's Week 7–15 files open in the editor, in tabs. They will want to look.
- [ ] The Term 2 Bug Log on the table, open.
- [ ] Workbook 18.1 (reflection) and 18.2 out; 18.3–18.6 held back.
- [ ] Figure 18.4 printed or on screen — the ladder. You will point at it in the Wrap.

### Fallback if the laptop or the install fails

**Be straight about this: there is no good paper version of this lesson.** The whole point is running both versions and diffing the output, and you cannot run anything on paper. If numpy is broken, do this instead and move the party to next week:

1. **Do the reflection half properly, and give it the whole hour.** Page 18.1, the Term 2 reflection sheet, plus the Bug Log review. Read every entry from Weeks 10 to 17 out loud. Ask for their three most valuable. That is genuinely worth an hour and it is the half of this week that matters most for Term 3.
2. **Do the eight cards as a *paper* exercise:** for each card, write the one-liner *next to it* without running it. Do not mark them right or wrong — collect them, check them yourself, and hand them back next week with the party. A prediction written down is worth a great deal even unrun.
3. **Sort the cards into three piles by hand:** *retires with `arr * 2`-style maths*, *needs something we haven't learned yet* (cards about keeping only the big ones — that is Week 20), and *will never retire* (anything about names, text or waiting for a person). That is §7 of this file, done with hands, and it is a real idea.
4. **Fix the install before Week 19**, which is `axis=0` versus `axis=1` and is even less doable on paper.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | `python3 -m pip install numpy`. If it will not go tonight, run the reflection lesson above and move the party. |
| Their Week 7–15 files are gone | Use the eight generic cards from the Prep list. Slightly less satisfying, entirely functional. |
| The lab runs long and only five cards get done | **Completely fine.** Five retired loops with `identical? True` beside each delivers objective 1. Cards 7 and 8 (arange and zeros) can be the homework. **Do not cut the sting** — it is the last five minutes and it is the most important thing in the lesson. |
| A card's two versions disagree and nobody can see why | Into the REVISIT pile, immediately, and move on. Do not debug it for ten minutes. **The pile is the point of the lesson**, not an admission of failure. |
| They want to use `.reshape()` because they found it online | Let them, then ask them to also do it by retyping the brackets, and ask which version made them look at the mistake. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Count the Ways to Get It Wrong | 7 | 7 | The four-line loop on the board. Count its failure modes. |
| 🧠 Concept — One Sign in the Window | 16 | 23 | vectorized, elementwise, broadcasting, arange, zeros — and the printing trap |
| 💻 Live-Code Together — Cards 1 and 5 | 18 | 41 | Two cards retired together. Two deliberate mistakes: one silent, one loud |
| 🎲 Their Turn — The Loop Retirement Party | 20 | 61 | Cards 2, 3, 4, 6, 7, 8, the revisit pile, and the sting |
| 🔑 Wrap & Assign | 9 | 70 | Reflection sheet, three checks, the revisit list, homework |

---

### 🪝 Hook — Count the Ways to Get It Wrong (7 minutes)

**Do this:** Write this on the board, by hand, exactly as it is. Eight cards face down beside you. Nothing on the screen yet.

```
doubled = []
for score in scores:
    doubled.append(score * 2)
```

**Say this:**

> "You have written this loop, or something extremely like it, about twenty times since Week 7. It doubles every score. It works. There is nothing wrong with it.
>
> I want you to do something different with it today. **Count the ways you could get it wrong.** Not 'is it right' — I'm telling you it's right. How many *different mistakes* could a person make while typing those three lines? Go through it slowly."

Let them work. Prompt with "what if you forgot the first line?" if they stall. Write each one on the board as they find it.

They should get to something like:

1. Forget `doubled = []` → `NameError: name 'doubled' is not defined`.
2. Put `doubled = []` **inside** the loop → it gets emptied every time, and you end up with one number.
3. `scores.append(...)` instead of `doubled.append(...)` → you add to the list you are looping over, which is a genuine nightmare.
4. Indentation wrong → the append happens once, after the loop.
5. Print `scores` at the end instead of `doubled`.

> "Five. And here's the part I want you to notice. **Which of those five would Python actually complain about?**"

Let them work through it. Only the first reliably crashes.

> "One. **One out of five gives you an error message.** The other four give you an answer, and it's the wrong one, and nothing tells you.
>
> And now look at what those three lines are actually *for*. What's the interesting part — the part that is the job?"

*Times two.*

> "`* 2`. That's the job. Everything else — the empty list, the `for`, the `append`, the indentation — is **machinery for visiting things one at a time.** It's not the idea. It's the plumbing. And you type it by hand, every time, and four out of five ways of getting the plumbing wrong don't tell you.
>
> Today you retire the plumbing."

**Do this:** Turn over card 1 and put it on the table. Then fan out the other seven, still face down.

> "Eight cards. Eight loops out of your own files from the last eleven weeks. One at a time, you're going to replace each one with **a single line**, run both, and check that the answers match exactly.
>
> And any card where they *don't* match goes there —" *(point at the REVISIT space)* "— and that pile is what we do next. It is not a pile of failures. It is a list."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How many ways could you get those three lines wrong?" | Four or five. | If they say "none, it's easy", ask what happens if `doubled = []` goes inside the loop. Then have them run it. |
| "How many of those would Python complain about?" | One. | If they think most would, run one silently-wrong version now. Thirty seconds, and it changes the room. |
| "Which bit of the loop is the actual job?" | `* 2`. | If they say "the for loop", ask: "if I gave you a machine that visited every number for you, what would you still have to tell it?" |
| "So what's the rest of it?" | Machinery for visiting things. | Any wording is fine. "Plumbing", "the boring bit", "the going-round part" all work. |
| "What goes in the revisit pile?" | Any card whose two versions disagree. | Say explicitly, now: **that pile is the goal, not the shame.** Say it before any card fails. |

---

### 🧠 Concept — One Sign in the Window (16 minutes)

**Do this:** Board work. Leave the eight cards where they are.

**Say this — part 1, the word:**

> "One word for what you're about to do."

Write it up:

> **vectorized** — the instruction is written once, for the whole array. numpy does the visiting.

> "`score_arr * 2`. **One instruction. Six numbers.** You never write the going-round part, so you never get the going-round part wrong.
>
> And it's faster, quite a lot faster — about twenty times, on a million numbers. But I want to be honest with you: **you have six numbers, and both versions are instant.** The speed is not why we're doing this today. We're doing it because one line has one place to go wrong and four lines have five."

**Say this — part 2, elementwise:**

> "Now two arrays instead of one. Six runs, six balls. Add them together."

Write on the board:

```
runs   48  12  77   5  63  30
balls  32  20  55   9  41  28
       --  --  ---  --  ---  --
total  80  32  132  14  104  58
```

> "That's called **elementwise.** Position by position. The 48 meets the 32 and nothing else. **Cell zero only ever meets cell zero.** It never meets cell three.
>
> Check the first two with me. 48 plus 32?"

*80.*

> "12 plus 20?"

*32.*

> "Good. It's just arithmetic, done six times, by somebody else.
>
> So — **what has to be true about the two arrays for that to work?**"

Let them get there.

*They have to be the same length.*

> "They have to line up. Six and six. What if I gave you six runs and four balls?"

*You'd run out.*

> "You would, and numpy refuses. It says `operands could not be broadcast together with shapes` and then prints both shapes at you. Which is **good news**, exactly like last week's ragged block — it could have stopped at four and given you a short answer, and instead it stopped you."

**Say this — part 3, broadcasting:**

> "But hold on. Look back at the first one. `score_arr * 2`. That's **six** numbers and **one** number. They don't line up at all. Why did that work?"

Let them puzzle. Then:

> "Because of a rule with a big name and a simple idea. **Broadcasting.**
>
> Think of a pizza shop. There's a sign in the window: **10% off everything.** How many price tags did they have to rewrite?"

*None.*

> "None. One sign, four hundred items, and everybody understands it applies to all of them. **Broadcasting is the sign.** When one side is smaller, numpy reuses it wherever it's short. It doesn't even copy the number — it just reads the same one over and over, which is why it's free.
>
> That rule is doing you a favour about nine times out of ten. And the tenth time it does something you absolutely did not mean, and doesn't tell you. We'll get to that one at the end and I'm not going to warn you again."

**Say this — part 4, two ways to build an array:**

> "Two more, and both of them retire a loop as well."

```python
print(np.arange(6))
```

```text
[0 1 2 3 4 5]
```

> "**`np.arange`** — 'array range'. It's Week 7's `range`, handing you an array. And it has the same trap: **how many numbers, and what's the last one?**"

*Six numbers. Last one is five.*

> "Six and five. Starts at nought, stops *before* the number you gave it. If you got that wrong, that's a Week 7 rung and it goes on your revisit list."

```python
print(np.zeros((2, 3)))
```

```text
[[0. 0. 0.]
 [0. 0. 0.]]
```

> "**`np.zeros`** — a blank block, whatever shape you ask for. And **look very carefully at the brackets.** `np.zeros` open bracket, open bracket, two comma three, close, close. **Two pairs.** Why?
>
> Because the shape is *one thing*: a pair of numbers. It goes in one slot, so it needs its own brackets. If you write `np.zeros(3, 4)` you get an error that makes no sense at all — I'll show you later.
>
> And notice the zeros. `0.` with a dot on the end. What does the dot mean?"

*They're decimals.*

> "Decimals. `np.zeros` gives you `float64`. Which you know because you'd print `.dtype` — that's last week, and it hasn't stopped mattering."

**Say this — part 5, the printing trap, and do NOT skip this:**

> "Last thing before we type, and if I don't tell you this you will spend twenty minutes thinking you're wrong when you're right.
>
> When you print the loop's answer and the one-liner's answer, **they will not look the same.**"

Write both on the board:

```
loop: [96, 24, 154, 10, 126, 60]
line: [ 96  24 154  10 126  60]
```

> "Commas in one. Spaces and some padding in the other. **Same six numbers.** Different kind of container, so they show themselves differently — that's last week: a list prints with commas, an array prints with spaces and lines its columns up.
>
> So you don't compare them with your eyes. You do this:"

```python
print("identical?", list(doubled_line) == doubled_loop)
```

> "`list(...)` turns the array back into a plain list, so you're comparing like with like, and then Python answers the question properly. **`True` means every number matches.** That's the line that decides whether a card retires or goes in the pile."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What does vectorized mean?" | One instruction for the whole array; numpy does the visiting. | If they say "faster", accept it and add: "and *why* is that not the main reason?" |
| "In elementwise addition, what does cell 0 meet?" | Cell 0. Only ever cell 0. | If they say "all of them", draw the pairing lines from Figure 18.2. |
| "What must be true of the two shapes?" | They have to line up — same length. | If they say "same numbers in them", clarify: same *shape*, any values. |
| "Why does `arr * 2` work when the shapes don't match?" | Broadcasting — the single number gets reused. | If they cannot say, the shop sign is the whole answer. Use it and move on. |
| "`np.arange(6)` — how many, and what's the last?" | Six, and five. | **Both halves.** If they get either wrong, write "Week 7 — range" on the revisit list right now, in front of them. |
| "Why two pairs of brackets in `np.zeros((2, 3))`?" | Because the shape is one thing — a pair — going into one slot. | If they don't know, that is fine. Tell them, and tell them the error message they'll get if they forget. |
| "`loop:` and `line:` print differently. Are the answers different?" | No — same numbers, different container. | This one you must confirm out loud rather than leaving to discovery. It is not a productive struggle. |

---

### 💻 Live-Code Together — Cards 1 and 5 (18 minutes)

**You never touch the keyboard.** Predictions before every run. Two cards done together; the other six are theirs.

**Step 1 (2 min).** New file, `retire.py`. The data first:

```python
"""retire.py - eight loops from weeks 7-15, retired."""

import numpy as np

scores = [48, 12, 77, 5, 63, 30]         # a plain Python LIST, from Week 11
balls = [32, 20, 55, 9, 41, 28]          # balls faced by the same six
```

**Step 2 — CARD 1, the loop half (2 min).** Card 1 face up on the table.

```python
doubled_loop = []                        # start with an empty list
for score in scores:                     # visit every score once
    doubled_loop.append(score * 2)       # double it and add it to the list
print("loop:", doubled_loop)
```

Run it. Real output:

```text
loop: [96, 24, 154, 10, 126, 60]
```

> **Say this:** "That's the answer we have to match. Write it down — `96 24 154 10 126 60`. If the one-liner gives us anything else, we've got a problem."

**Step 3 — ⚠️ FIRST DELIBERATE MISTAKE (5 min).** This is the most common numpy mistake in the world and you should walk them straight into it.

> **Say this:** "Right. One line. You want every score doubled. Type: `print("line:", scores * 2)`."

```python
print("line:", scores * 2)
```

**Ask before running:** "What do you expect?" *Six doubled numbers.*

Run it. Real output:

```text
loop: [96, 24, 154, 10, 126, 60]
line: [48, 12, 77, 5, 63, 30, 48, 12, 77, 5, 63, 30]
```

> **Say this:** *(let them read it)* "Talk me through what happened."

*It printed the numbers twice.*

> "It did. **Twelve numbers, and not one of them is doubled.** And no error. No warning.
>
> Count them again — how many did we start with, and how many came out?"

*Six. Twelve.*

> "Six in, twelve out. **That check just caught a bug for the second time this term** — remember `12 written, 11 loaded` in Week 16? Same move. Count what goes in, count what comes out.
>
> Now — why? What is `scores`? Look at the line where we made it."

*It's a list.*

> "It's a **list**, not an array. And `* 2` on a list means something completely different: it means *give me the list twice*. `"ab" * 2` gives `abab`; you've seen that since Week 3 when you drew lines with `"=" * 20`. Same rule. **A list times two is the list repeated.**
>
> One missing step. Make it an array first."

```python
score_arr = np.array(scores)             # the same six numbers, as an array
doubled_line = score_arr * 2             # no loop. One instruction, six numbers.
print("line:", doubled_line)
```

Run it. Real output:

```text
loop: [96, 24, 154, 10, 126, 60]
line: [ 96  24 154  10 126  60]
```

> **Say this:** "Now look at those two lines. Are they the same?"

Let somebody say no. Somebody always does.

> "They look different. Commas in one, spaces in the other. **The numbers are the same.** Prove it — don't argue about it."

```python
print("identical?", list(doubled_line) == doubled_loop)
```

```text
identical? True
```

> "`True`. Card 1 retires."

**Do this:** Physically move card 1 off the table, into a "retired" pile. Make it a small ceremony. It is a party.

**Bug Log the list-times-two bug now.** It has no error message and it will happen to them again.

**Step 4 — CARD 5, both halves (5 min).** Card 5 face up: two lists added position by position.

```python
loop5 = []
for i in range(len(scores)):             # 0, 1, 2, 3, 4, 5
    loop5.append(scores[i] + balls[i])   # the i-th of each, added
print("loop:", loop5)

balls_arr = np.array(balls)
line5 = score_arr + balls_arr            # one line. Six pairs.
print("line:", line5)
print("identical?", list(line5) == loop5)
```

**Ask before running:** "Two things. What's the first number, and what will `identical?` say?" *80, and True.*

Run it. Real output:

```text
loop: [80, 32, 132, 14, 104, 58]
line: [ 80  32 132  14 104  58]
identical? True
```

> **Say this:** "Look at what disappeared from the loop version. `range(len(scores))`. `scores[i]`. `balls[i]`. **All the index-juggling is gone**, and index-juggling is where off-by-one errors live. That's the card I'd most want retired if I could only have one."

**Do this:** Card 5 to the retired pile.

**Step 5 — ⚠️ SECOND DELIBERATE MISTAKE (4 min).** The `np.zeros` brackets, which produces a genuinely baffling message.

> **Say this:** "One more before you take over. Card 8 needs a blank three-by-four grid. Type `np.zeros(3, 4)`."

```python
print(np.zeros(3, 4))
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "retire.py", line 28, in <module>
    print(np.zeros(3, 4))
TypeError: Cannot interpret '4' as a data type
```

> **Say this:** "That message is nonsense, isn't it. *Cannot interpret 4 as a data type.* We never mentioned a data type.
>
> Here's what happened. `np.zeros` has two slots. Slot one is **the shape.** Slot two is **the dtype** — the kind of number, from last week. We handed it a `3` and a `4`, so it put the 3 in the shape slot and then tried to read the 4 as a *kind of number*, and there is no kind of number called four.
>
> **The shape is one thing.** It's a pair. It needs its own brackets."

```python
print(np.zeros((3, 4)))
```

```text
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
```

> "And the lesson to take from that error, which is worth more than the fix: **when a message mentions something you never typed, you have probably put a value in the wrong slot.** That's a Week 10 idea — parameters, in order — and it will happen to you all year."

**Bug Log it**, with the translation in their own words.

---

### 🎲 Their Turn — The Loop Retirement Party (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–13:** cards 2, 3, 4, 6, 7 and 8 — six cards, roughly two minutes each. Every card gets `identical?` printed. Any card that fails goes in the REVISIT space and they move on.
- **Minutes 13–17:** the sting — `(3,)` plus `(3, 1)` — and the shape check that catches it.
- **Minutes 17–20:** read the revisit pile out loud and turn it into a written list with reasons.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the eight cards (two already in the retired pile from the live-code), the REVISIT space, the Term 2 Bug Log, workbook page 18.3.

**On the screen:** `retire.py`, with cards 1 and 5 done.

### The rules of the party

1. **One card at a time.** Loop version first, then the one-liner, then `identical?`. Never skip the loop version — it is what defines the right answer.
2. **`identical?` must print `True`** before a card retires. Not "looks right". `True`.
3. **A card whose versions disagree goes in the REVISIT space immediately**, and you move on. No debugging for more than sixty seconds.
4. **Say out loud what each retired card's one line does** before running it. "Multiply every score by two." If they cannot say it, they cannot check it.

### The eight cards, retired

The complete `retire.py`, and its real output, is in the Prep Checklist above — that is the same file the student builds, card by card. Here are the eight lines on their own, which is what should end up on the board:

| Card | The loop | The one line |
|---|---|---|
| 1 | double every score | `score_arr * 2` |
| 2 | add 5 to every score | `score_arr + 5` |
| 3 | square every score | `score_arr ** 2` |
| 4 | celsius to fahrenheit | `celsius_arr * 9 / 5 + 32` |
| 5 | runs + balls, pair by pair | `score_arr + balls_arr` |
| 6 | strike rate for each player | `score_arr / balls_arr * 100` |
| 7 | the numbers 0 to 9 | `np.arange(10)` |
| 8 | a blank 3 by 4 grid | `np.zeros((3, 4))` |

**Eight cards. Twenty-seven lines of loop replaced by eight lines of arithmetic, and every single one gave `identical? True`.**

**Two cards worth pausing on:**

**Card 4** is the one to be pleased about. `celsius * 9 / 5 + 32` is *the formula off the page*. Three operations, three broadcasts, one line, no loop. Say it out loud: **"you wrote the formula, and it happened to every number."** That is the sentence this whole term has been walking towards.

**Card 6** produces the messy output, and the messiness is instructive:

```text
6  strike rate for each player
   loop: [150.0, 60.0, 140.0, 55.56, 153.66, 107.14]
   line: [150.    60.   140.    55.56 153.66 107.14]
   identical? True
```

The loop's answer is shown rounded to two places for readability; the array is rounded with `np.round`. **They still print differently and they are still identical** — the `identical?` check is done on the unrounded values. If a student objects that `150.0` and `150.` are different, that is a good objection with a boring answer: same number, two ways of writing it, and Python's `==` knows.

### The sting (4 minutes, and it is the most important thing today)

**Do this:** New file, `bonus18.py`. Dictate it exactly, including the extra brackets, and **say nothing about them.**

> **Say this:** "Last one, and it's not from a card. Three players, and I want to give each of them a different bonus — one run for the first, two for the second, three for the third."

```python
"""bonus18.py - three scores, three bonuses, and nine answers."""

import numpy as np

scores = np.array([48, 12, 77])          # three scores
bonus = np.array([[1],                   # three bonuses... one per line
                  [2],
                  [3]])

print("scores.shape:", scores.shape)
print("bonus.shape :", bonus.shape)

answer = scores + bonus
print(answer)
print("answer.shape:", answer.shape)
print("we put in 3 and 3. How many came out?")
```

**Ask before running:** "Three numbers plus three numbers. **How many numbers come out?**"

*Three.*

> "Write it down. Three."

Run it. Real output:

```text
scores.shape: (3,)
bonus.shape : (3, 1)
[[49 13 78]
 [50 14 79]
 [51 15 80]]
answer.shape: (3, 3)
we put in 3 and 3. How many came out?
```

**Do this:** Say nothing for five seconds. Let them count.

> **Say this:** "How many came out?"

*Nine.*

> "Nine. Did anything crash?"

*No.*

> "Did anything warn you?"

*No.*

> "So let's find the actual answer in there. What should the first player get? 48 plus 1."

*49.*

> "Where is it?"

*Top left.*

> "Second player, 12 plus 2?"

*14.*

> "Where's that?"

*The middle.*

> "And 77 plus 3 is 80 — bottom right. **Your three answers are on the diagonal.** They're in there, surrounded by six numbers that mean absolutely nothing — 13 is Kabir's score plus Asha's bonus, which is not a thing anybody wanted.
>
> Now read the two shapes at the top. `(3,)` and `(3, 1)`."

*One's a row and one's a column.*

> "**One is a row and one is a column**, and that's the whole bug. Look back at how you typed the bonus. How many sets of brackets?"

*Two.*

> "Two, and it should have been one. One extra pair of brackets, and instead of three numbers you got a column of three rows — and broadcasting was perfectly happy to stretch a row and a column into a grid, because that's exactly what it's designed to do. It did what you asked. You asked wrong.
>
> Fix it. One set of brackets."

```python
bonus = np.array([1, 2, 3])              # shape (3,)  - one set of brackets
print(scores + bonus)
```

```text
[49 14 80]
```

> "Three numbers. 49, 14, 80.
>
> **Here's what I want you to take out of this room, and it's the whole reason today happened in this order.** Last week you learned to print `.shape` and it felt like tidiness. It isn't tidiness. **It is the only thing that catches this.** There was no error. There was no warning. The one and only signal was `(3, 3)` where you expected `(3,)`, and you would only have seen it if you'd printed it.
>
> **Three numbers in should not give nine out. Print the shape of the answer.**"

**Bug Log this** as the last entry of Term 2, under *errors with no error message*. It is the best entry in the book.

### The revisit pile, turned into a list (3 minutes)

**Do this:** Look at the REVISIT space. Whatever is in it — including nothing — read it out.

> **Say this:** "Right. What's in the pile?"

For each card, one question: **"what would you need to go back over to retire this?"** Then write it on page 18.6 as a specific line, not a vague one.

Use this to translate:

| Card wouldn't retire because… | Write this on the revisit list |
|---|---|
| couldn't say what the loop did | **Week 7 — reading a `for` loop out loud** |
| lost track of the accumulator | **Week 7 — `total += x`** |
| couldn't get the numbers out of the records | **Week 15 — comprehensions** |
| made an array and then looped over it anyway | **Week 17 — what an array is for** |
| couldn't predict the shape | **Week 17 — `.shape`** |
| got `np.arange(6)`'s last number wrong | **Week 7 — `range` stops before** |
| outputs looked different but were the same | **Week 18 — `list(arr) == loop_result`** |

> **Say this:** "If that pile is empty, brilliant, and I want one thing from you anyway: **which week of Term 2 would you least like to be tested on tomorrow?** Write that one down instead. Everybody has one, including me."

**That last question is the safety net**, and it is why the section works even for a student who retired all eight cards.

### What "finished" looks like

- Eight one-liners written, run, and each with `identical? True` printed beside it. *(Five is a completely acceptable version of this.)*
- `np.arange` and `np.zeros` both used, and the double brackets on `zeros` understood.
- The `(3, 3)` spotted, explained, and fixed by retyping the brackets.
- Page 18.1, the Term 2 reflection sheet, filled in.
- **A written revisit list with at least one specific line on it**, naming a week and a thing.

### Variation — easier

- **Five cards, not eight.** Keep 1 (`* 2`), 2 (`+ 5`), 5 (`arr1 + arr2`), 7 (`arange`) and the sting. Card 4 (the formula) and card 8 (the nested loop) are the two hardest and both can be homework.
- **Give them the loop half already written** for every card, and have them write only the one-liner. Writing the loops again is not the objective; retiring them is.
- **Drop the `identical?` line** and compare by reading the numbers aloud together, one at a time. Slower, and it makes "identical" mean something concrete.
- **Skip cards 6 and 8.** Division producing long decimals and a 2-D grid are both extra cognitive load on top of the main idea.
- **Do the sting with two numbers instead of three**, so the wrong answer is a 2×2 with four numbers in it. Four instead of two is easier to see than nine instead of three.

### Variation — harder

None of these need syntax from a later week.

1. **The loop that will not retire.** Give them a ninth card: `big = []` / `for s in scores:` / `if s > 50:` / `big.append(s)`. Ask them to retire it. They cannot — and the interesting part is working out *why*: array maths does the same thing to every number, and this loop does different things to different numbers. **That is exactly what Week 20's boolean masks are for.** A student who can say that sentence has understood the boundary of this week's tool.
2. **A loop that will never retire.** Card ten: `counts = {}` / `for r in squad:` / `counts[r["team"]] = counts.get(r["team"], 0) + 1`. Why not? Because it needs the **team names**, and an array does not have any. Some loops are about words, and words are what dictionaries are for. Ask: *"is that a limitation of numpy, or is numpy the wrong tool?"*
3. **Time it themselves.** Both halves, on a million numbers, three times each, and report the *range* rather than one number. A measurement taken once is not a measurement.
4. **Predict five broadcasts.** For each pair of shapes, will it work, and what shape comes out? `(6,)` and `(6,)`; `(6,)` and one number; `(6,)` and `(4,)`; `(3,)` and `(3, 1)`; `(2, 3)` and `(3,)`. Write predictions first. *(Works `(6,)`; works `(6,)`; refuses; works and gives `(3, 3)` — the trap; works and gives `(2, 3)`.)*
5. **How wrong is wrong?** Take the `(3, 3)` answer and total it with `sum()`. It gives `[150 42 237]` instead of `143`. Then the question: *"if you'd printed only the total and never the array, would you have noticed?"* (No. And that is why you print the shape, not just the answer.)
6. **Retire a loop from their capstone-to-be.** Look ahead at what the Week 34 project will need — averages, differences, percentages of a total — and write each one as a one-liner now, on their own data. Then keep the file. It is genuinely useful in sixteen weeks.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code, on numpy 1.26.

> **🧑‍🏫 If a student asks:** the exact wording of numpy's own errors changes a little between numpy versions, and Python 3.11 and newer add `~~~^^^` arrows under the failing part of the line. The *meaning* of each message below does not change.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: operands could not be broadcast together with shapes (3,) (4,)` | "These two don't line up and I won't guess." | Two arrays of different lengths added or multiplied. | Print both shapes. Then work out which one is wrong — usually one list has a value missing or an extra one. |
| `TypeError: can only concatenate list (not "int") to list` | "You asked me to glue a number onto a list." | `scores + 5` where `scores` is a plain **list**, not an array. | `np.array(scores) + 5`. The `+` you want only exists on arrays. |
| `TypeError: Cannot interpret '4' as a data type` | "You put a 4 where the kind-of-number goes." | `np.zeros(3, 4)` — the shape's brackets are missing, so the 4 landed in the dtype slot. | `np.zeros((3, 4))`. The shape is one thing and needs its own brackets. |
| `TypeError: arange() requires stop to be specified.` | "You didn't tell me where to stop." | `np.arange()` with nothing in it. | `np.arange(10)`. |
| `numpy.core._exceptions._UFuncNoLoopError: ufunc 'add' did not contain a loop with signature matching types (dtype('int64'), dtype('<U1')) -> None` | "I don't know how to add a number to a piece of writing." | Adding an array of numbers to text, or to an array whose dtype came out as text — often the Week 17 `<U21` bug, one row further on. | Print `.dtype` on **both** sides. One of them is text when you thought it was numbers. |
| `IndexError: index 7 is out of bounds for axis 0 with size 4` | "You asked for slot 7 and there are four slots." | An index left over from the loop version. | Remember: the one-liner has no indexes. If you are still writing `arr[i]`, the loop has not actually retired. |
| `NameError: name 'np' is not defined` | "I don't know what `np` is." | The `import numpy as np` line is missing, or is below the code that uses it. | Put it at the top of the file. Imports first, always. |
| `AttributeError: 'list' object has no attribute 'shape'` | "A list hasn't got a shape." | `scores.shape` where `scores` is a plain list. | `np.array(scores).shape`. And this is a useful error — it is Python telling you which of the two things you are holding. |
| **No error, six numbers became twelve** | Nothing is wrong as far as Python is concerned. | `scores * 2` on a plain **list**. On a list, `* 2` means *the list, twice*. | `np.array(scores) * 2`. And count what went in against what came out — that check has now caught a bug three weeks running. |
| **No error, three plus three gave nine** | Nothing is wrong as far as numpy is concerned. | One side is a `(3, 1)` column instead of a `(3,)` row — one extra pair of brackets. Broadcasting stretched both. | Retype the brackets: `np.array([1, 2, 3])`. And **print the answer's shape**, every time. |
| **No error, the two versions print differently** | Nothing is wrong at all. | A list prints with commas; an array prints with spaces and aligned columns. | `list(arr) == loop_result`. Compare like with like. |
| **No error, `np.zeros` gave decimals when you wanted whole numbers** | Nothing is wrong; this is the default. | `np.zeros` is `float64` unless you say otherwise. | Usually leave it. If you really need whole numbers: `np.zeros((3, 4), dtype=int)`. |

### How to teach debugging without giving the answer

The moves stand: read the last line; find the line number; say the complaint in your own words; compare characters; *"which `File` line is the last one?"*; *"how many went in and how many came out?"*; *"what does `type()` say?"*; *"print the shape and the dtype."*

This week adds the last one of Term 2, and it is the one that catches the errors that are not errors:

10. **"How many numbers did you put in, and how many came out?"** Not "does it look right". A count. It caught the missing CSV header in Week 16, it caught `scores * 2` on a list today, and it caught nine-instead-of-three. **Three different bugs, three different weeks, one question.**

And the sentence for this week, which is the Term 2 summary:

> **"Half of Term 2's worst bugs never produced an error message. `'104'` from a file. `<U21` from one typo. A list repeated instead of doubled. Nine numbers instead of three. In every single case the fix was cheap and the *catch* was a habit: count what comes out, and print its shape."**

---

## ❓ Questions Students Ask This Week

**"Is a loop bad now?"**

No, and this matters. Array maths retires loops that do **the same arithmetic to every number**. It does nothing at all for the other three kinds of loop your student writes:

- loops that make a decision about text — counting how many players per team needs the team *names*, and an array has none;
- loops that wait for a person — the `while` loop in the Week 8 guessing game;
- loops that produce printed output, row by row.

A good working sentence: **loops are for people and words, arrays are for numbers.** And even for numbers, you will still write a loop when you are collecting values one at a time as you go, because arrays are a fixed size and lists grow. Build a list, then `np.array()` it once, at the end.

**"Why does `scores * 2` on a list duplicate it instead of doubling it?"**

Because `*` on a list has always meant "repeat", since long before numpy existed. It is the same rule as `"=" * 20` from Week 3, which drew a line of twenty equals signs. Python asks the *thing on the left* what `*` should mean, and a list's answer is "give me copies of myself".

An array's answer is "multiply every one of my numbers". Same symbol, two completely different jobs, decided by what is on the left. That is why the one-word fix — `np.array(...)` — is the whole fix, and why the bug is so hard to see: **there is nothing wrong with the line you are looking at.** The mistake is on the line above.

**"How much faster is it, really?"**

For a million numbers, doubling them: about 20 milliseconds with a Python loop, about 1 with an array. Twenty times. Try it yourself; your numbers will be different from anyone else's, and if you run it three times they will be different from each other, which is worth knowing about all measurements.

For your six numbers: no difference you could ever measure. **The speed is not why you are doing this.** You are doing it because the one line has one place to go wrong and the loop has five, and because in Week 29 you will hand an array to a machine-learning model, and whether that array has the right shape decides whether the model works.

**"Why does `np.zeros` need double brackets when `np.arange` doesn't?"**

Because they are asking for different things. `np.arange(10)` needs **one number** — where to stop. `np.zeros((3, 4))` needs **one shape**, and a shape is a *pair* of numbers travelling together as a single item, so it needs brackets round it to hold it together.

If you write `np.zeros(3, 4)` numpy reads the 3 as the shape and then tries to read the 4 as the *kind* of number, which is what its second slot is for — hence the baffling `Cannot interpret '4' as a data type`. And there is a general lesson in that: **when an error message mentions something you never typed, you have probably put a value in the wrong slot.**

**"Why did `np.zeros` give me `0.` instead of `0`?"**

`np.zeros` makes `float64` — decimals — by default. The reasoning is that a blank block is usually about to be filled with real measurements, and real measurements have decimal points. If you genuinely want whole numbers: `np.zeros((3, 4), dtype=int)`.

The habit to notice here is Week 17 paying for itself. You found this out by printing `.dtype`, or by spotting a dot that you did not type. Both count.

**"The two versions print differently. Are they actually the same?"**

Yes, and this is the question that eats the most time in this lesson, so here it is properly. `[96, 24, 154]` is how a **list** prints — commas between the values. `[ 96  24 154]` is how an **array** prints — spaces, and padding so the columns line up, because arrays are meant to be looked at in rows and columns.

Same six numbers. Two different containers, two different ways of showing themselves. Do not compare them with your eyes; write `list(arr) == loop_result` and let Python answer.

**"Is broadcasting a good feature or a bad one?"** *(Nobody fully agrees, and here is why.)*

**This one is genuinely argued about by people who write numerical software for a living**, and it is worth being honest with a 12-year-old that they have just met a real design controversy rather than a settled fact.

The case for it is overwhelming and you have felt it already today. Without broadcasting, `scores * 2` would be an error — you would have to build an array of six 2s first, every time, and `celsius * 9 / 5 + 32` would need three of them. Almost every formula you will ever write would triple in length and become much harder to read. And it costs nothing: numpy does not really copy the 2 six times, it just reads the same value repeatedly. **The feature that makes numpy pleasant to write is broadcasting.**

The case against is the thing you saw at the end of the lesson. Broadcasting makes some **mistakes impossible to detect**. A `(3,)` and a `(3, 1)` are almost certainly a typo — nobody deliberately adds a row of three to a column of three — and numpy cheerfully produces nine numbers and says nothing. Experienced people lose real hours to this, and it has put wrong numbers into real published work. A stricter rule — *shapes must match exactly, say what you mean* — would catch every one of those, at the cost of making every formula longer.

Where does that leave you? With the position the whole numerical-computing world has actually settled on, which is not "broadcasting is good" or "broadcasting is bad" but a **habit**: *broadcasting is powerful enough to be worth the danger, so you check the shape of your answers.* Newer array libraries have tightened some of the edges precisely because of bugs like today's, and none of them have removed it, because nobody wants to write the long version.

So: use it, enjoy it, and **print the shape.** That is not a compromise. That is what expertise looks like here.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| Twenty minutes are lost to "the printing is different so it's wrong" | Because it genuinely looks different and the student is being careful, which is a virtue | **Pre-empt it in the Concept segment**, on the board, with `list(arr) == loop_result` shown before the lab starts. If it happens anyway, stop the room and do it once for everybody. |
| The revisit pile is treated as a pile of failures | Because a pile of things you couldn't do looks exactly like a pile of failures | Say what it is **before the first card fails**: "this pile is the whole point of today; it's a list, not a verdict." Then put one card in it yourself, on purpose, with a card you know is hard. |
| Nobody puts anything in the revisit pile, and the reflection is empty | Because all eight retired, which is a good outcome | Use the safety-net question: *"which week of Term 2 would you least like to be tested on tomorrow?"* Everybody has an answer. Write theirs down. |
| The sting gets tipped off, by you or by a keen student | It is very hard not to warn somebody | Do not warn them. If somebody in the room guesses "nine", say "write it down and let's see" and run it anyway — being right about a prediction is also a good outcome, and the shape check still needs demonstrating. |
| The `(3, 3)` is shrugged off — "but the right answers are in there" | They are, on the diagonal | Push once: *"if you'd printed only the total and never looked at the array, would you have known?"* Then show them: `sum()` of the wrong answer gives `[150 42 237]` instead of `143`. That lands. |
| The lab runs long and the sting gets cut | Eight cards plus a reflection sheet is a lot | **Cut cards 6 and 8. Never cut the sting.** If you have five minutes left and three cards to go, do the sting instead. It is the objective; the cards are practice. |
| A student writes the one-liner and then loops over the array anyway | Because the loop is the familiar move and the array feels like an ingredient | This is a real diagnostic and it means Week 17 did not land. Ask: *"what did the array do for you there?"* If they cannot answer, put **Week 17** on the revisit list. |
| `.reshape()` appears from the internet | Because searching "numpy fix shape" returns it in the first result | Let them use it, then ask them to also fix it by retyping the brackets, and ask which version made them notice **where the mistake was**. The answer is the brackets, every time. |
| The eight cards are generic rather than from their own files | Because finding their Week 7 file takes ten minutes | It works either way and it is meaningfully better with their own code. Do the finding the night before, not in the lesson. |
| The reflection sheet is filled in with "it was fine" | Because reflection sheets invite that | Do not accept a general answer. Ask for **a week number and a thing**. "Week 15, the comprehension with the `if` in it" is a usable answer; "loops" is not. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** cards 4, 6 and 8 — the formula, the division, and the nested loop. Five cards is a complete lesson.

**Cut:** `np.zeros` entirely, including the double-brackets bug. `np.arange` is the more useful of the two and much easier.

**Give them the loop half already written** for every card. Rewriting loops they have already written is not the objective and it eats the clock.

**Reteach — one card, done four times.** Take card 1 and only card 1. Loop version. Run it. Write the six answers on paper. One-liner. Run it. Read the six answers off the screen and check them against the paper, one at a time, out loud. Then `identical?` and get the `True`. **Then do it again with card 2, then card 5.** Three cards, done slowly, with the answers checked by hand, delivers objectives 1 and 2 completely. A student who has hand-checked six numbers against a one-liner believes array maths in a way that a student who has read eight `True`s does not.

**The copy-this-exactly scaffold.** One file. This runs:

```python
import numpy as np

scores = [48, 12, 77]

loop = []
for score in scores:
    loop.append(score * 2)
print("loop:", loop)

score_arr = np.array(scores)
line = score_arr * 2
print("line:", line)

print("identical?", list(line) == loop)
```

```text
loop: [96, 24, 154]
line: [ 96  24 154]
identical? True
```

Then one question: **"how many lines did the loop take, and how many did the one-liner take?"** Four and two. And of those two, one was just making the array.

**One thing you must not cut:** the sting, and the shape check. If this lesson collapses to a single sentence, make it *"three numbers in should not give nine out — print the shape of the answer."*

### If the student is flying

None of these need syntax from a later week.

1. **The loop that will not retire yet** (Variation-harder 1) — keep only the scores above 50 — and the sentence about why array maths cannot do it. This is the single best preparation for Week 20 available.
2. **The loop that will never retire** (Variation-harder 2) — the counting dictionary — and the question of whether that is numpy's failure or the wrong tool.
3. **Predict five broadcasts** (Variation-harder 4). Written down first. This is the highest-value fifteen minutes in the whole week for a strong student.
4. **How wrong is wrong?** (Variation-harder 5). `sum()` of the `(3, 3)` gives `[150 42 237]` instead of `143`. A wrong answer that is itself an array of wrong answers.
5. **Time it themselves** (Variation-harder 3), reporting a range from three runs rather than a single number.
6. **Write the Term 2 exam.** "Six questions that would tell you whether somebody had really understood Weeks 10 to 17. One per pair of weeks. And write the answers." Setting the questions requires knowing what matters, which is a different and harder skill than answering them — and you can genuinely use their questions in Week 27.

### If the student won't engage today

**The eight cards, and the board. Close the laptop.**

Lay the eight cards out face up. Then one instruction:

> **"Sort these into two piles: the ones where the same thing happens to every number, and the ones where it doesn't."**

That is a sorting task, it takes six minutes, it needs no typing, and it is genuinely the deep idea of this week — array maths retires the first pile and cannot touch the second.

Then, for two or three cards from the first pile, write the one line next to the card **without running it.** Do not mark them. Collect them.

Then do the reflection sheet, out loud, as a conversation rather than a form. Ask three questions and write down what they say:

- **"Which week of Term 2 made the most sense?"**
- **"Which one would you least like to be tested on tomorrow?"**
- **"What's the best entry in your Bug Log, and why that one?"**

That is objective 5 delivered completely, which is the objective this checkpoint exists for. The eight one-liners survive perfectly well to Week 19, which needs arrays anyway and will happily start with a warm-up that retires three loops.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the one-liner (on paper, 60 seconds)**

> "Here's a loop. Write me the one line that replaces it."

```python
result = []
for score in scores:
    result.append(score + 10)
```

*Good answer:* `np.array(scores) + 10`, or `score_arr + 10` if the array already exists.

**What to catch:** `scores + 10` with no `np.array` is the important miss — that is the `TypeError` from the clinic. Ask: *"is `scores` a list or an array?"*

**Check 2 — the shapes (spoken, 60 seconds)**

> "I add two arrays together and get an answer with shape `(3, 3)`. I was expecting three numbers. What went wrong?"

*Good answer:* "One of them was a column — a `(3, 1)` — instead of a row. Broadcasting stretched them both into a grid. I probably typed an extra pair of brackets."

**Full marks needs the *cause*, not just the description.** "Broadcasting happened" is a level-2 answer. Push once: *"why did it have anything to stretch?"*

**Check 3 — the silent one (spoken, and it is the one that matters, 90 seconds)**

> "`scores * 2` printed twelve numbers and none of them were doubled. There was no error. What happened, and what is the one check that would have caught it?"

*Good answer:* "`scores` was a plain list, and `* 2` on a list means the list repeated. The check is counting: six went in and twelve came out."

**What to catch:** a student who names the cause but not the check has half of it. The check is the transferable half — it caught the CSV header in Week 16 and it caught the nine-instead-of-three today. Ask for it explicitly.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot turn a loop into a one-liner without copying. Believes the two printed outputs are different answers. Cannot say what `.shape` would tell them. |
| **2 — Emerging** | Writes `arr * 2` and `arr + 5` when the array already exists. Forgets `np.array()` and does not notice the list got repeated. Uses `identical?` when reminded. |
| **3 — Secure** | Retires a loop unaided, including making the array first. Adds two arrays elementwise and says their shapes must line up. Uses `np.arange` and `np.zeros` with the right brackets. Checks with `list(arr) == loop_result` rather than by eye. **This is the target.** |
| **4 — Strong** | Explains broadcasting with the shop-sign idea. Spots the `(3, 3)` from the shape alone and fixes it by retyping the brackets. Explains *why* `scores * 2` on a list repeats it — because `*` asks the thing on the left what it means. Produces a specific revisit list with weeks and reasons. |
| **5 — Exceptional** | Says which loops can never retire and why — the ones that need names, or people, or produce output. Predicts the result of `(2, 3)` + `(3,)` correctly. Argues both sides of "is broadcasting a good feature", and lands on the habit rather than a verdict. Connects the four silent bugs of Term 2 — `'104'`, `<U21`, list-times-two, nine-instead-of-three — as one family with one check. |

---

## 📤 Homework to Assign

**Say this:**

> "Two halves, and I care about both. About an hour.
>
> **First half — retire eight of your own loops.** Page 18.4. **Your own**, out of your own files from Weeks 7 to 15. Go and find them. Eight is not many — you have written dozens.
>
> For each one: write the loop version, run it, **write down the answer.** Then write the one line, run it, and print `identical?` with the `list(...) == ...` check. **Eight `True`s** on the page.
>
> If a loop won't retire, **don't force it.** Write down which one and *why you think it won't* — and if the reason is 'it only does something to some of the numbers', you have found Week 20 two weeks early and I want to know about it.
>
> **Second half — the reflection.** Pages 18.5 and 18.6, and this is the half I read most carefully.
>
> **One:** for each week from 10 to 17, one word — *solid*, *shaky*, or *lost*. Eight words. Be honest; nobody is marking the words.
>
> **Two:** your revisit list. **At least two lines, and each line names a week and a thing.** 'Week 15, the comprehension with the `if` in it' is a line I can do something with. 'Loops' is not.
>
> **Three:** read your Bug Log from Week 10 all the way to today and pick **the three entries that were worth the most.** One sentence each on why. And I'll tell you now what I expect at least one of them to be: **an error with no error message.** There are four of those in Term 2 and they are the most valuable things in the book.
>
> **Four:** one sentence. **What is the one check that would have caught three of Term 2's silent bugs?** Six words will do."

**Workbook pages:** 18.1, 18.2, 18.3 in class · **18.4, 18.5, 18.6** at home.

**Expected time:** 10 min finding their own eight loops · 25 min retiring and proving them · 10 min on the eight solid/shaky/lost words · 10 min on the revisit list · 10 min on the Bug Log three. **About 65 minutes.**

> **🧑‍🏫 What to look for when you mark it:** two things. **One — is the revisit list specific?** A week number and a thing. This list is what you teach from in the first ten minutes of Weeks 19, 20 and 21, so a vague one costs you three lessons. **Two — did they pick a silent bug as one of their Bug Log three?** If they did, they have learned the actual lesson of Term 2: the check is never "did it run". If they picked three crashes, that is worth a conversation — ask them which of Term 2's bugs *didn't* crash, and watch them find four.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 18.1 — Term 2 reflection sheet

*One word for each week: solid, shaky, or lost. Then the questions.*

| Week | What it was | Their word |
|---|---|---|
| 10 | Functions with parameters, `return`, defaults | |
| 11 | Lists, index from 0, `append` | |
| 12 | Slicing, `sorted`, importing your own file | |
| 13 | Dictionaries, `.get()` with a fallback | |
| 14 | A list of dicts is a table | |
| 15 | Filter, group, and the row count | |
| 16 | CSV out, CSV back, convert on load | |
| 17 | Arrays, `.shape`, `.dtype` | |

There are no right answers to the words. **What you are marking is whether the following four have real content in them.**

**18.1(a) Which week of Term 2 made the most sense, and why?**
Any answer with a *reason* is a good answer. The most common are Week 11 (lists feel concrete) and Week 14 (a table is a familiar thing). Watch for Week 16 — a student who says the CSV week made the most sense usually means *"I finally saw why any of this was for anything"*, which is worth writing down.

**18.1(b) Which one would you least like to be tested on tomorrow?**
The most common honest answers are Week 15 (comprehensions with conditions) and Week 17 (`(3, 1)` versus `(3,)`). Both are correct diagnoses of genuinely hard things. **Whatever they say goes straight onto the revisit list.**

**18.1(c) Name one thing you can do now that you could not do in Week 9.**
Model answers, in rough order of depth: *"put my data in a file and get it back"*; *"answer a question about a table without counting by hand"*; *"look at an error and know which line to go to"*; *"tell whether something is text or a number, and check rather than assume."* That last one is the best available answer and it is worth saying so.

**18.1(d) In Week 9 you turned repeated blocks into functions. What did Term 2 turn repeated *work* into?**
Two good answers, and both are right. **Tools** — `records.py`, `filter_by`, `group_count`, `save_csv`: written once, pointed at anything. And **one-liners** — array maths, which retires the loop entirely. The pattern across the whole term is the same: *stop typing the machinery; name it once and reuse it.*

### Page 18.2 — Loop or one-liner?

*For each loop, say whether it retires today, needs something you haven't learned, or will never retire.*

| # | The loop does this | Verdict | The one line, or why not |
|---|---|---|---|
| (a) | doubles every score | **retires** | `arr * 2` |
| (b) | adds two columns pair by pair | **retires** | `arr1 + arr2` |
| (c) | builds the numbers 0 to 19 | **retires** | `np.arange(20)` |
| (d) | totals a column | **retires** | `sum(arr)` — Python's own `sum`, from Week 12 |
| (e) | makes a blank 5 by 3 grid | **retires** | `np.zeros((5, 3))` |
| (f) | squares every score | **retires** | `arr ** 2` |
| (g) | keeps only the scores above 50 | **not yet** | needs a boolean mask — **Week 20** |
| (h) | counts how many players per team | **never** | needs the team *names*, and an array has none. This belongs to a dictionary. |
| (i) | asks for a guess until the user gets it right | **never** | a `while` loop waiting on a person. Arrays have nothing to say about people. |
| (j) | prints one formatted table row per record | **never** | that is output, not arithmetic. |

**18.2(k) State the rule in one sentence.**
**Array maths retires loops that do the same arithmetic to every number.** It cannot help with loops that make decisions about text, wait for a person, or produce printed output.

**18.2(l) What is different about (g)?**
It does something to **some** of the numbers and not others, and array maths does the same thing to all of them. That is not a permanent limit — a **boolean mask** in Week 20 is precisely the tool for "only the ones where…", and it is one line as well.

**18.2(m) Is (h) numpy's failure, or the wrong tool?**
The wrong tool, and it is worth being clear about it. Counting per team needs the team names, and an array cannot hold names alongside numbers — that was Week 17's whole trade. This is not something numpy should be better at; it is something a dictionary already does perfectly. **From Week 21, `pandas` does both at once, which is exactly what it is for.**

### Page 18.3 — Shapes that work and shapes that don't

*For each pair, will it work? If so, what shape comes out?*

| # | Shapes | Works? | Result shape | Why |
|---|---|---|---|---|
| (a) | `(6,)` and `(6,)` | yes | `(6,)` | they line up exactly — six pairs, six answers |
| (b) | `(6,)` and one number | yes | `(6,)` | broadcasting reuses the single number six times |
| (c) | `(6,)` and `(4,)` | **no** | — | `ValueError` — six and four cannot pair up, and numpy will not guess |
| (d) | `(3,)` and `(3, 1)` | yes — **and this is the trap** | `(3, 3)` | one is a row and one is a column; both get stretched into a grid |
| (e) | `(2, 3)` and `(3,)` | yes | `(2, 3)` | the row of three is reused for each of the two rows |
| (f) | `(3, 1)` and `(3, 1)` | yes | `(3, 1)` | identical shapes, three pairs |
| (g) | `(2, 3)` and `(2,)` | **no** | — | line them up from the right: 3 against 2. Not equal, neither is 1. Refused. |

**18.3(h) Which of these seven is the dangerous one, and why?**
**(d).** It is the only one that *works* while almost certainly being a mistake. Nobody deliberately adds a row of three to a column of three. It produces nine numbers instead of three, does not complain, and hides the three answers you wanted on the diagonal.

**18.3(i) Which are good news, and why?**
**(c) and (g).** They stop you. numpy could have paired up as many as it could and given you a short answer, or padded with zeros — and then you would have had made-up numbers in your data with nothing to tell you. **An error you can read beats a wrong answer you cannot see.**

**18.3(j) In (d), how do you fix it?**
Retype the brackets so the column becomes a row: `np.array([1, 2, 3])` instead of `np.array([[1], [2], [3]])`. One set of brackets, not two.

**18.3(k) What is the one check that would have caught (d)?**
Printing the shape of the answer. `(3, 3)` where you expected `(3,)`. **There is no other signal — no error, no warning, and the numbers you wanted are all present.**

### Page 18.4 — Retire eight of your own loops

The student's loops are their own. Model answer, using the eight-song playlist from Week 16:

```python
"""hw18.py - eight loops from my own weeks 7-15 files, retired. Both versions, then the proof."""

import numpy as np

plays = [120, 45, 300, 60, 210, 95, 180, 220]      # eight songs from Week 14
minutes = [3.5, 4.2, 2.8, 5.1, 3.9, 3.3, 3.1, 2.6]

plays_arr = np.array(plays)
minutes_arr = np.array(minutes)

checks = []

# 1  Week 7: print every play count doubled
loop = []
for pl in plays:
    loop.append(pl * 2)
line = plays_arr * 2
print("1  double every play count")
print("   loop:", loop)
print("   line:", line)
checks.append(("1", list(line) == loop))

# 2  Week 7: add 10 plays to everything
loop = []
for pl in plays:
    loop.append(pl + 10)
line = plays_arr + 10
print("2  add 10 plays to every song")
print("   loop:", loop)
print("   line:", line)
checks.append(("2", list(line) == loop))

# 3  Week 7: total seconds instead of minutes
loop = []
for m in minutes:
    loop.append(m * 60)
line = minutes_arr * 60
print("3  minutes to seconds")
print("   loop:", loop)
print("   line:", line)
checks.append(("3", list(line) == loop))

# 4  Week 12: plays per minute for each song
loop = []
for i in range(len(plays)):
    loop.append(plays[i] / minutes[i])
line = plays_arr / minutes_arr
print("4  plays per minute")
print("   loop:", [round(x, 2) for x in loop])
print("   line:", np.round(line, 2))
checks.append(("4", list(line) == loop))

# 5  Week 12: total plays
loop_total = 0
for pl in plays:
    loop_total += pl
line_total = sum(plays_arr)
print("5  total plays")
print("   loop:", loop_total)
print("   line:", line_total)
checks.append(("5", line_total == loop_total))

# 6  Week 15: each song's share of the total, as a percentage
loop = []
for pl in plays:
    loop.append(pl / loop_total * 100)
line = plays_arr / line_total * 100
print("6  each song's share of all plays, as a percentage")
print("   loop:", [round(x, 2) for x in loop])
print("   line:", np.round(line, 2))
checks.append(("6", list(line) == loop))

# 7  Week 7: the track numbers 0 to 7
loop = []
for i in range(8):
    loop.append(i)
line = np.arange(8)
print("7  track numbers 0 to 7")
print("   loop:", loop)
print("   line:", line)
checks.append(("7", list(line) == loop))

# 8  Week 11: a blank 8-row, 3-column sheet to fill in later
loop = []
for row in range(8):
    loop.append([0.0, 0.0, 0.0])
line = np.zeros((8, 3))
print("8  a blank 8 by 3 sheet")
print("   loop rows:", len(loop), " loop columns:", len(loop[0]))
print("   line shape:", line.shape)
checks.append(("8", [list(r) for r in line] == loop))

print()
labels = [f"{pair[0]}:{pair[1]}" for pair in checks]     # a list comprehension, Week 14
print("identical?", ", ".join(labels))
answers = [pair[1] for pair in checks]                   # just the True/False column
print("all eight identical?", answers.count(True) == len(answers))
```

Real output:

```text
1  double every play count
   loop: [240, 90, 600, 120, 420, 190, 360, 440]
   line: [240  90 600 120 420 190 360 440]
2  add 10 plays to every song
   loop: [130, 55, 310, 70, 220, 105, 190, 230]
   line: [130  55 310  70 220 105 190 230]
3  minutes to seconds
   loop: [210.0, 252.0, 168.0, 306.0, 234.0, 198.0, 186.0, 156.0]
   line: [210. 252. 168. 306. 234. 198. 186. 156.]
4  plays per minute
   loop: [34.29, 10.71, 107.14, 11.76, 53.85, 28.79, 58.06, 84.62]
   line: [ 34.29  10.71 107.14  11.76  53.85  28.79  58.06  84.62]
5  total plays
   loop: 1230
   line: 1230
6  each song's share of all plays, as a percentage
   loop: [9.76, 3.66, 24.39, 4.88, 17.07, 7.72, 14.63, 17.89]
   line: [ 9.76  3.66 24.39  4.88 17.07  7.72 14.63 17.89]
7  track numbers 0 to 7
   loop: [0, 1, 2, 3, 4, 5, 6, 7]
   line: [0 1 2 3 4 5 6 7]
8  a blank 8 by 3 sheet
   loop rows: 8  loop columns: 3
   line shape: (8, 3)

identical? 1:True, 2:True, 3:True, 4:True, 5:True, 6:True, 7:True, 8:True
all eight identical? True
```

**Hand-check two, with the student, on paper:**

```
card 1:  120 x 2 = 240   ✔      45 x 2 = 90    ✔
card 4:  120 / 3.5 = 34.2857... = 34.29  ✔
card 5:  120+45=165 · +300=465 · +60=525 · +210=735 · +95=830 · +180=1010 · +220=1230  ✔
card 6:  120 / 1230 x 100 = 9.756... = 9.76  ✔   and all eight shares add to 100
```

That last line is a free cross-check worth pointing out: **the eight percentages must add up to 100.** If they do not, the total is wrong.

**Three things to mark, in this order:**

1. **Eight `True`s.** Binary, and it is objective 1.
2. **Did they use `list(...) == ...`?** A student who compared by eye and wrote "same" has not done the check, and will believe a wrong answer one day.
3. **Card 5 is different from the others and it is worth a tick if they noticed.** It is an *accumulator* loop — one number out, not a list — so the one-liner is `sum(arr)`, not `arr` something. Python's own `sum` from Week 12, working perfectly on an array.

**18.4(a) Which of your eight loops was the most satisfying to retire, and why?**
Usually card 4 or 6 — anything with `range(len(...))` and indexes in it, because all the index-juggling disappears. Model answer: *"the plays-per-minute one, because the loop version had `plays[i]` and `minutes[i]` in it and I always have to check I've got the `i`s in the right places. The one line just says plays divided by minutes."*

**18.4(b) Did any refuse to retire? Which, and why?**
Any honest answer is good. The two expected ones: a loop with an `if` in it (needs Week 20's mask) and a loop building a counting dictionary (needs names, so it never retires). **A student who correctly identifies the `if` loop as "not yet, and I think there's a tool coming" has done something genuinely impressive.**

### Page 18.5 — The identical-output proof

**18.5(a) Why do the loop's answer and the one-liner's answer print differently?**
Because they are different **containers**. A list prints with commas between the values; an array prints with spaces, and pads the numbers so the columns line up, because arrays are meant to be read in rows and columns. Same numbers, two ways of showing them.

**18.5(b) Write the line that settles it properly.**

```python
print("identical?", list(line_answer) == loop_answer)
```

`list(...)` turns the array back into a plain list so like is compared with like, and then Python compares every value.

**18.5(c) Why not just read the numbers and check by eye?**
Two reasons, and the second is the real one. With six numbers you *can* — but with sixty you cannot, and with six hundred you certainly cannot. And more importantly: **checking by eye is exactly the habit that let `90` through in Week 16.** A number that looks plausible is not a check. `True` is a check.

**18.5(d) `identical?` printed `False`. What do you do first?**
Print both answers, in full, and find the **first** position where they differ. Not the second — the first, because everything after it may just be a knock-on. Then ask what is different about that position. (This is exactly the mismatch-finder move from Week 16, applied to arrays.)

### Page 18.6 — The revisit pile

**18.6(a) Your revisit list. At least two lines, each naming a week and a thing.**

What a **good** list looks like:

> *"Week 7 — `range(6)` stops at 5, and I keep thinking it stops at 6."*
> *"Week 15 — the comprehension with the `if` in the middle. I can read it but I can't write it."*
> *"Week 17 — telling `(3,)` from `(3, 1)`. I got that one wrong today and I got it wrong in the homework too."*

What an **unusable** list looks like: *"loops"*, *"numpy"*, *"most of it"*, *"nothing"*.

**Send a vague one back.** This list is what you teach from in the first ten minutes of Weeks 19, 20 and 21 — a vague list costs you three lessons.

**18.6(b) Your three best Bug Log entries from Term 2, one sentence each on why.**

The four silent bugs of Term 2, which is what you are hoping they pick from:

| The bug | Week | Why it is the best kind of entry |
|---|---|---|
| `max()` said the top score was `90` | 16 | The answer was wrong, plausible, and produced no error at all. |
| `dtype` came out `<U21` from one typo | 17 | One word in a list turned every number into writing, silently. |
| `scores * 2` gave twelve numbers | 18 | The line you are looking at is fine. The mistake is the line above. |
| three plus three gave nine | 18 | The right answers were *present*, on the diagonal, surrounded by nonsense. |

And the loud ones worth keeping: the two-`File` `KeyError` from Week 15 (read the **last** `File` line); `TypeError: can only concatenate str (not "int") to str` from Week 16; the ragged-block `ValueError` from Week 17.

**If all three of their picks are crashes**, ask one question: *"which of this term's bugs didn't crash?"* and watch them find four. That conversation is worth more than the page.

**18.6(c) One sentence: what check would have caught three of Term 2's silent bugs?**

Model answer:

> *"Count how many things went in and how many came out."*

Twelve rows written, eleven loaded — Week 16. Six numbers in, twelve out — today. Three plus three, nine out — today. **One question, three bugs, three different weeks.** And its close relative, which catches the other one: *print the shape and the dtype.*

**18.6(d) One sentence: what is the difference between "it ran" and "it's right"?**

Model answer:

> *"'It ran' means Python understood me. 'It's right' means I asked for the thing I actually wanted — and Python has no way of knowing the difference, so that part is my job."*

**That sentence is the whole of Term 2.** Mark it properly. A student who can write it will produce an honest capstone in Week 35.

### Answers to every question posed in the lesson

- *"How many ways could you get those three lines wrong?"* → Four or five: no empty list; the empty list inside the loop; appending to the wrong list; wrong indentation; printing the wrong variable.
- *"How many of those would Python complain about?"* → One. The other four give you a wrong answer quietly.
- *"Which bit of the loop is the actual job?"* → `* 2`. Everything else is machinery for visiting things.
- *"What goes in the revisit pile?"* → Any card whose two versions disagree. It is a list, not a verdict.
- *"48 plus 32?"* → 80. *"12 plus 20?"* → 32. Elementwise is just arithmetic, done six times, by somebody else.
- *"What has to be true about the two arrays?"* → Their shapes have to line up. Six and six works; six and four is refused.
- *"Why does `arr * 2` work when the shapes don't match?"* → Broadcasting. The single number is reused wherever it is needed, like one 10%-off sign in a shop window.
- *"`np.arange(6)` — how many numbers, and what's the last one?"* → Six, and five. Starts at 0, stops before 6.
- *"Why two pairs of brackets in `np.zeros((2, 3))`?"* → Because the shape is one thing — a pair of numbers — going into one slot.
- *"What does the dot in `0.` mean?"* → It is a decimal. `np.zeros` gives `float64` by default.
- *"`loop:` and `line:` print differently. Are the answers different?"* → No. A list prints with commas, an array with spaces and aligned columns. Same numbers.
- *"What do you expect from `scores * 2`?"* (on a list) → Twelve numbers, none of them doubled: the list repeated. And no error.
- *"How many did we start with, how many came out?"* → Six and twelve. That count is the check.
- *"Why does a list do that?"* → Because `*` on a list has always meant "repeat", the same as `"=" * 20` in Week 3. Python asks the thing on the *left* what `*` means.
- *"What disappeared from card 5's loop version?"* → `range(len(scores))`, `scores[i]` and `balls[i]` — all the index-juggling, which is where off-by-one errors live.
- *"Three numbers plus three numbers — how many come out?"* → Should be three. Actually nine, with shape `(3, 3)`, and nothing complains.
- *"Where are the three answers you wanted?"* → On the diagonal: 49 top left, 14 in the middle, 80 bottom right. Surrounded by six numbers nobody asked for.
- *"What's the one check that catches it?"* → Print the shape of the answer. `(3, 3)` where you expected `(3,)`.
- *"Cannot interpret '4' as a data type — what happened?"* → The 4 landed in `np.zeros`'s second slot, which is for the dtype. The shape needed its own brackets. And the general lesson: when a message mentions something you never typed, you have put a value in the wrong slot.

---

## 🔮 Next Week Preview

Term 3 starts, and it starts by taking the one thing we have carefully avoided for two weeks: **which direction?** So far every array operation has treated all the numbers as one heap. Week 19 asks the question that makes a table a table — *do you want the average of each row, or the average of each column?* — and gives the student `axis=0` and `axis=1` to say which. It is one keyword, it is two characters different, and picking the wrong one gives you a beautifully formatted, completely confident, entirely wrong answer, because both answers are numbers and both look plausible. The lesson is a rainfall grid — cities down the side, months across the top — and the rule is that **row 1 gets hand-checked on paper with a calculator before anybody believes a single thing the code says.** This week's habit of printing the answer's shape turns out to be the tell: if you asked for a per-city average and got twelve numbers back, you asked the wrong direction, and the shape said so.

**Prep early:** three things, and the first one is five minutes well spent. **Read the revisit lists** from tonight's homework, and plan to spend the first ten minutes of Week 19 on whatever is on them — that is what the list is for, and Week 19's lesson is short enough to afford it. **Keep `retire.py` and any array files**, because Week 19 opens with a two-minute warm-up that retires three more loops before the new idea arrives. And **find a calculator and put it on the table**, because the hand-check of row 1 is not optional next week: it is the thing that decides whether the student believes `axis=0` or checks it, and that difference is the entire reason Week 19 exists.

---

[⬅ Week 17](week-17.md) · [Course Home](../README.md) · [Week 19 ➡](week-19.md) · [Student Guide](../student-guide/week-18.md) · [Workbook](../workbook/week-18.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
