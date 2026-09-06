# 📕 Teacher Orientation — Everything You Need, Before You Teach Any Code

### *Read this once, cover to cover. About 90 minutes. Then you can teach all 36 weeks, including the Python.*

[⬅ Back to the course](../README.md) · [Week 1 student guide](../student-guide/week-01.md) · [Week 1 workbook](../workbook/week-01.md) · [Figure style guide](../figures/STYLE.md)

---

## 🪝 You Do Not Need to Know Python to Teach This

Read that again, because you almost certainly did not believe it.

**You do not need to know Python. You do not need to know machine learning. You have never opened a
terminal and that is fine.** By the end of this file you will have both, at the level this course
needs, and you will be ahead of most adults you know.

Here is why that is true and not just encouraging noise.

1. **The language is smaller than it looks.** All 36 weeks of this course run on about ten ideas:
   a value, a name for a value, a type, a decision, a repeat, a named block of code, a numbered list,
   a labelled record, a library somebody else wrote, and an error message. That is it. Section 1 of
   this file teaches all ten with examples you can run in the next twenty minutes.

2. **Every line of code in this course has already been run.** Not checked by eye — *run*. Every
   output you see in a `text` block is the real output a machine printed. So when your student's
   screen shows something different, you do not need to reason about whether the book is right. The
   book is right. Something on the screen is different, and the teacher file tells you the four
   likeliest reasons.

3. **Every lesson is fully scripted, including the code.** The teacher file for each week gives you
   the exact code to type, its exact output, the exact planted bug, the exact traceback it produces,
   and the exact fix. You are not improvising at the keyboard in front of a child.

4. **Being stuck in public is on the syllabus.** This is the big difference from Level 1. Code fails
   visibly, immediately, and often. A teacher who says *"I don't know why that broke — read me the
   last line of the error and let's find out together"* is modelling the actual job. Section 8 makes
   that concrete.

### What is actually being asked of you

| You need to | You do NOT need to |
|---|---|
| Read the week's teacher file for 20 minutes before class | Read anything else, ever |
| Have got both week-0 smoke tests to pass, once | Understand how pip works |
| Be able to find the last line of an error message | Be able to fix it before your student does |
| Count, divide, and turn a fraction into a percentage | Know any maths past `y = mx + c` |
| Be willing to type a wrong thing on purpose | Be a programmer |
| Refuse to touch the student's keyboard | Be patient at a supernatural level (18 minutes will do) |

### One warning, and it is the important one

There is exactly one way to teach this course badly, and it is this:

> **Taking the keyboard.**

The student is stuck. There is a missing colon on line 4. You can see it. It would take you two
seconds. You reach over.

You have just deleted the lesson. The lesson was not "the program works". The lesson was "I found the
thing that was wrong." A working program you did not fix teaches nothing and quietly teaches
something worse: *this is a thing adults do and I can't.*

**Section 8 of this file is entirely about this one skill.** It is the most important section here.
If you read nothing else, read that.

---

# 📖 Section 1 — Python for the Absolute Beginner, in Fifteen Pages

This is your own mini-course. Read it straight through at a keyboard, typing the examples. It takes
about 40 minutes and it is everything you need for all 36 weeks.

**Every example below has been run.** The output blocks are real.

---

## 1.1 — What a program actually is

> **A program** is a text file containing instructions, which a computer reads from the top and does
> one at a time, in order, exactly as written.

That is the entire concept. Three things in it matter:

- **It is a text file.** Not a special document. A plain file, with `.py` on the end. You could write
  one in Notepad.
- **In order, from the top.** Line 1, then line 2, then line 3. No cleverness, no rearranging.
- **Exactly as written.** This is the one beginners fight. The computer is not being difficult, it is
  being *literal*. If you write the word `pizzaa` it looks for something called `pizzaa`. It will not
  guess.

> **🧑‍🏫 The one-line version to say out loud:** "A computer is not smart. It is fast, and it is
> extremely literal. Almost every bug you will ever have is you assuming it guessed what you meant."

Here is a complete program. Type it into a file called `a1.py`:

```python
# a1.py - the smallest complete program
print("Hello. I do exactly what you say.")
print(7 * 6)
print("7" * 6)
```

Run it (Section 4 shows you how to run a file; for now assume you typed `python3 a1.py`):

```text
Hello. I do exactly what you say.
42
777777
```

Look at the last two lines. `7 * 6` gave **42**. `"7" * 6` gave **777777**. Same star, two completely
different jobs, decided entirely by whether there were quote marks. That is types, and it is §1.3.

---

## 1.2 — Running a file, and the two windows you will live in

You need two windows open, side by side, all year:

```
   ┌─────────────────────────────┬─────────────────────────────────────┐
   │  THE EDITOR                 │  THE TERMINAL                       │
   │  (VS Code, or IDLE)         │  (Terminal / PowerShell)            │
   │                             │                                     │
   │  Where you WRITE the file.  │  Where you RUN the file, and where  │
   │  Nothing happens here when  │  the answers and the errors appear. │
   │  you type. Typing is safe.  │                                     │
   │                             │  $ python3 a1.py                    │
   │  Save with Ctrl+S / Cmd+S   │  Hello. I do exactly what you say.  │
   │  ▲ every single time        │                                     │
   └─────────────────────────────┴─────────────────────────────────────┘
```

The loop, forever, is: **edit → save → run → read → edit.**

> **⚠️ Watch out:** The single most common wasted minute of the whole year is *running a file you
> forgot to save*. The terminal happily runs the old version and you both stare at an error you
> already fixed. When something makes no sense at all, the first question is always: **"did you
> save?"** Say it kindly, say it every week.

Three ways to run a file. Pick one and stick to it:

| How | Command / click | Best for |
|---|---|---|
| Terminal | `python3 a1.py` (macOS/Linux) or `python a1.py` (Windows) | What this course assumes. You see the real error message. |
| VS Code ▷ button | Top right of the editor | Fast, but it opens its own terminal panel — same thing. |
| IDLE | `F5` | Fallback if the others won't install. Works fine. |

---

## 1.3 — Values, and the four types

> **A value** is a piece of data — a number, a piece of text, a yes/no.
> **A type** is what *kind* of value it is, which decides what you are allowed to do with it.

Four types carry this whole course:

| Type | Means | Looks like | Notes |
|---|---|---|---|
| `str` | **string** — text | `"Asha"`, `"12"`, `"hello world"` | Always in quotes. Either `"` or `'`, but be consistent. |
| `int` | **integer** — whole number | `12`, `0`, `-4` | No quotes, no decimal point. |
| `float` | number with a decimal point | `3.5`, `8.50`, `-0.25` | The name means "floating point". Ignore why. |
| `bool` | **boolean** — yes or no | `True`, `False` | Exactly those two words, capital first letter. |

You can always ask:

```python
print(type("Asha"))
print(type(12))
print(type(3.5))
print(type(True))
```

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

**Why this matters more than it sounds.** `"12"` and `12` look the same on the screen and are not the
same thing at all. One is a piece of text that happens to contain two digits. The other is a number.
Text can be glued together; numbers can be added. Confusing the two is the number one beginner error
in this entire level, and it is the whole plot of week 2 and week 4.

---

## 1.4 — Variables: a box with a name on it

> **A variable** is a name that holds one value, so you can use the value again later without
> retyping it.

```python
pizza_price = 8.50
slices = 8
price_per_slice = pizza_price / slices
print(price_per_slice)
print(round(price_per_slice, 2))
```

```text
1.0625
1.06
```

Three rules that answer 90% of variable questions:

1. **The name goes on the left of the `=`.** `pizza_price = 8.50` means "put 8.50 in the box called
   pizza_price". It does **not** mean "these two things are equal". Reading `=` as "gets" instead of
   "equals" fixes a surprising amount of confusion.
2. **The right-hand side is worked out first.** In `price_per_slice = pizza_price / slices`, Python
   does the division first, gets `1.0625`, and *then* puts it in the box.
3. **Assigning again replaces what was there.** `total = 0` then `total = total + 5` leaves 5 in the
   box. The old value is gone.

**Naming.** Use names a 12-year-old would pick: `scores`, `total`, `pizza_price`, `student_name`.
Lowercase, words joined by underscores, no spaces, no starting with a digit. Never `x`, `tmp`, or
`foo`. This is not fussiness — in week 24 your student will be reading their own code from week 12,
and `average_runs` will save them where `a` would not.

> **💡 Try this:** Give your student a pad of sticky notes in week 2. Write `pizza_price` on one and
> stick it to an actual box. Put a piece of paper with `8.50` inside. Peel the note off, stick it on
> a different box. That is reassignment, and they will never forget it.

---

## 1.5 — Strings vs numbers, and the error you will meet fifty times

Watch what `+` does to two strings:

```python
first_name = "Asha"
last_name = "Rao"
full_name = first_name + " " + last_name
print(full_name)
print(len(full_name))
print(full_name.upper())
print(full_name.lower())
print("Rao" in full_name)
```

```text
Asha Rao
8
ASHA RAO
asha rao
True
```

`+` between strings **glues** (the word is *concatenate*). `len()` counts characters — note it says 8,
because the space counts. `.upper()` and `.lower()` give you back a new string. `in` asks a yes/no
question.

Now the collision. Type this into a file and run it:

```python
age = "12"
print(age + 5)
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/age_bug.py", line 2, in <module>
    print(age + 5)
TypeError: can only concatenate str (not "int") to str
```

Read the last line in English: *"I can only glue text onto text. You gave me a number."* Python does
**not** guess. Some languages would quietly produce `"125"`, which is worse, because it would be wrong
and silent.

The fix is to say which one you meant:

```python
age = "12"
print(int(age) + 5)        # I meant the number: 17
print(age + str(5))        # I meant the text: "125"
```

```text
17
125
```

`int()`, `float()` and `str()` are **conversions**. They do not change the box; they make a new value
of a different type.

---

## 1.6 — f-strings: putting values into sentences

Gluing with `+` gets ugly fast. Python has a better way — put an `f` before the opening quote, and
then anything in `{curly braces}` gets worked out and dropped in:

```python
name = "Asha"
runs = 42
balls = 37
strike_rate = runs / balls * 100
print(f"{name} scored {runs} off {balls} balls.")
print(f"Strike rate: {strike_rate:.1f}")
```

```text
Asha scored 42 off 37 balls.
Strike rate: 113.5
```

`{strike_rate:.1f}` means "show this as a decimal number with 1 digit after the point". `:.2f` gives
two. This matters for money, and it matters for honesty — a number printed as `113.5135135135` is
pretending to a precision it does not have.

> **🧑‍🏫 If a student asks** *"why is there an f?"* — "It stands for *format*. It's a signal to Python:
> look inside the curly braces, work that bit out, and put the answer here. Without the `f`, the
> braces are just braces."

---

## 1.7 — `input()`: asking the human, and the trap in it

```python
age_text = input("How old are you? ")
age = int(age_text)
print("Next year you will be", age + 1)
```

Typing `12` gives:

```text
How old are you? Next year you will be 13
```

**The trap, and it catches literally everybody:** `input()` **always** gives you a string. Always. Even
when the human types `12`. If you forget to convert, you get the §1.5 error, or worse, no error at
all and a wrong answer:

```python
age_text = "12"          # this is what input() would have handed you
age = age_text           # we forgot to convert it
print(age * 2)           # we wanted 24
```

```text
1212
```

No crash. No warning. Just `1212` where you wanted `24`. This is the most valuable bug in the course
and week 4 is built around it.

> **⚠️ Watch out:** Do not let the student put `input()` in the middle of a long program while they
> are still learning. Every time they run it to test something they have to retype all six answers.
> The teacher files tell them to hard-code the values while debugging and put `input()` back at the
> end. That habit — *make the loop between edit and result as short as possible* — is real
> engineering, taught in week 4.

---

## 1.8 — Making a decision: `if` / `elif` / `else`

> **A condition** is a question with a `True` or `False` answer.
> **`if`** runs an indented block of code only when the condition is `True`.

```python
pocket_money = 250
pizza_price = 300

if pocket_money >= pizza_price:
    print("You can buy the pizza.")
else:
    short_by = pizza_price - pocket_money
    print(f"You are {short_by} rupees short.")
```

```text
You are 50 rupees short.
```

Two things carry all the weight here:

**The colon.** `if ...:` ends with a colon. Every single time. A missing colon is the most common
syntax error in the entire level.

**The indentation.** The lines under the `if` are pushed in by four spaces. **In Python, indentation is
not decoration — it is how the language knows which lines belong to the `if`.** In most languages you
would use curly brackets. Python uses the spaces you can see. This is genuinely nicer once you are
used to it, and genuinely brutal for the first month.

For more than two paths, use `elif` (short for "else if"):

```python
mark = 74

if mark >= 80:
    grade = "A"
elif mark >= 70:
    grade = "B"
elif mark >= 60:
    grade = "C"
else:
    grade = "D"

print(f"Mark {mark} is grade {grade}")
```

```text
Mark 74 is grade B
```

> **⚠️ Watch out — the order trap, and it is week 6's whole lesson.** Python checks the conditions
> **top to bottom and stops at the first `True` one**. If you write `if mark >= 60` first, then a mark
> of 95 is `>= 60`, so it stops there and awards a C. Everybody gets a C, no error appears, and the
> program looks perfect. This is the first bug your student meets that produces *wrong answers rather
> than crashes*, and those are the dangerous kind.

Comparison operators, for reference:

| Write | Means |
|---|---|
| `==` | is equal to (**two** equals signs) |
| `!=` | is not equal to |
| `<` `>` | less than, greater than |
| `<=` `>=` | less than or equal to, greater than or equal to |

And to combine conditions: `and` (both must be true), `or` (either will do), `not` (flips it).

> **⚠️ `=` vs `==` is worth being fussy about all year.** One equals sign puts a value in a box. Two
> equals signs ask a question. Python will refuse to run `if score = 7:` and the error even suggests
> the fix, which is more help than most languages give.

---

## 1.9 — Repeating: `for` and `while`

> **A loop** runs the same block of code more than once.

**`for` — when you know how many times.**

```python
for step in range(4):
    print("step", step)
```

```text
step 0
step 1
step 2
step 3
```

Note it printed 0, 1, 2, 3 — **four numbers, starting at zero, stopping before four.** `range(4)`
means "four numbers beginning at 0". This off-by-one feeling never fully goes away and week 7 spends
real time on it.

**The accumulator pattern**, which the student will use for the rest of their life:

```python
scores = [7, 9, 8, 10, 6]
total = 0
for score in scores:
    total = total + score
print("Total:", total)
print("Average:", total / len(scores))
```

```text
Total: 40
Average: 8.0
```

Read it out loud: *start the total at zero; for each score, add it on; at the end, divide.* That is
how a computer averages, and it is exactly how a human would do it with a pencil.

**`while` — when you don't know how many times.**

```python
attempts = 0
secret = 7
guess = 0

while guess != secret:
    attempts = attempts + 1
    guess = attempts          # pretend the human guesses 1, 2, 3, ...
    print("Guess number", attempts, "was", guess)

print("Got it in", attempts, "guesses.")
```

```text
Guess number 1 was 1
Guess number 2 was 2
Guess number 3 was 3
Guess number 4 was 4
Guess number 5 was 5
Guess number 6 was 6
Guess number 7 was 7
Got it in 7 guesses.
```

> **⚠️ Watch out:** a `while` loop whose condition never becomes `False` runs forever. Your student
> **will** write one, probably in week 8. It is not a disaster: press **Ctrl+C** in the terminal and
> it stops. Teach them Ctrl+C in week 8 *before* they need it, and treat the infinite loop as a
> normal event, because it is.

---

## 1.10 — Lists: many values, one name

> **A list** is an ordered row of values under one name. Each position is a **slot**, and the slots are
> numbered **from zero**.

```python
scores = [7, 9, 8, 10, 6]
print(scores[0])
print(scores[-1])
print(scores[1:4])
print(len(scores))
scores.append(5)
print(scores)
print(sorted(scores))
print(scores)
```

```text
7
6
[9, 8, 10]
5
[7, 9, 8, 10, 6, 5]
[5, 6, 7, 8, 9, 10]
[7, 9, 8, 10, 6, 5]
```

Line by line:

| Line | What happened |
|---|---|
| `scores[0]` → `7` | Slot 0 is the **first** item. Counting starts at zero. |
| `scores[-1]` → `6` | Negative counts from the end. `-1` is last. Very handy. |
| `scores[1:4]` → `[9, 8, 10]` | A **slice**: from slot 1 up to *but not including* slot 4. |
| `len(scores)` → `5` | Five items — before the append. |
| `.append(5)` | Adds to the end, changing the list in place. |
| `sorted(scores)` | Gives back a **new** sorted list… |
| `print(scores)` again | …and leaves the original **unchanged**. |

That last pair is worth ten minutes of your own time. `sorted(x)` returns something new;
`x.sort()` changes `x` and returns nothing. Confusing them produces a very confident `None`.

The zero-based counting is the single largest source of injury in this level, which is why every
figure in this course draws list indices as pink numbers underneath the boxes, in every week, forever.

---

## 1.11 — Dictionaries: looking things up by name

> **A dictionary** holds values you look up by a **key** (a name) rather than by a position.

```python
player = {"name": "Asha", "runs": 42, "balls": 37}
print(player["name"])
print(player["runs"])
player["team"] = "Blue"
print(player)
print(player.get("overs", 0))
for key, value in player.items():
    print(key, "->", value)
```

```text
Asha
42
{'name': 'Asha', 'runs': 42, 'balls': 37, 'team': 'Blue'}
0
name -> Asha
runs -> 42
balls -> 37
team -> Blue
```

- `player["name"]` looks up by key. If the key isn't there you get a `KeyError` (§2.6).
- `player["team"] = "Blue"` adds a key that didn't exist. Assigning to a key that *did* exist replaces
  it. Same syntax, two behaviours — worth pointing out.
- `player.get("overs", 0)` says *"give me `overs`, or 0 if there isn't one"*. It does not crash. That
  is sometimes exactly right and sometimes a quiet lie, which is a week 15 discussion.
- `.items()` hands you each key with its value.

**Why dictionaries matter so much in this course.** A list of dictionaries **is a table**:

```python
players = [
    {"name": "Asha", "runs": 42},
    {"name": "Ravi", "runs": 17},
]

for row in players:
    print(row["name"], "made", row["runs"])
```

```text
Asha made 42
Ravi made 17
```

One dictionary is one **row**. The keys are the **column names**. That is Level 1's index cards,
typed out — and in week 21 the exact same shape becomes a pandas DataFrame. Week 14 is where the
student sees it, and it is one of the best moments in the year.

---

## 1.12 — Functions: giving a block of code a name

> **A function** is a named block of code. You **call** it by name to run it. It can take values in
> (**parameters**) and hand one value back out (**return**).

```python
def average(numbers):
    """Give back the mean of a list of numbers."""
    total = sum(numbers)
    return total / len(numbers)

print(average([7, 9, 8]))
print(average([10, 10, 10, 0]))
```

```text
8.0
7.5
```

Anatomy:

```
   def average(numbers):
   ▲   ▲       ▲       ▲
   │   │       │       └── colon. always.
   │   │       └────────── the PARAMETER: a box the caller fills in
   │   └────────────────── the NAME you'll call it by
   └────────────────────── "define"

       return total / len(numbers)
       ▲
       └── hands the value back OUT. Without this, the caller gets None.
```

Two things to be clear about in your own head, because students ask both:

**1. `print` and `return` are completely different.** `print` puts characters on the screen for a
human. `return` hands a value back to the code that called the function, so it can be used. A
function that prints but doesn't return looks fine when you test it and is useless inside a bigger
program. That specific bug is week 10's homework.

**2. Names inside a function are private.** A variable created inside a function does not exist
outside it. That is called **scope**, it is a feature, and it is what makes functions safe to reuse.

The payoff arrives in week 12: put your functions in a file called `stats.py`, and then any program
you write can say `import stats` and use them. Your student builds their own library and then uses it
for the next 24 weeks.

---

## 1.13 — Libraries and `import`: using code other people wrote

> **A library** (also *module*, also *package*) is a file or folder of code somebody else wrote, which
> you can use without understanding how it works inside.

```python
import random
random.seed(7)
print(random.randint(1, 100))
print(random.randint(1, 100))
```

```text
42
20
```

(`random.seed(7)` makes the "random" numbers repeat identically every run. That is how this course can
promise you an exact output for a random program — and it is a real technique, not a cheat.)

Four libraries carry the second half of the course. You will not need to understand their insides,
and neither will your student:

| Library | Nickname | Arrives | What it is for |
|---|---|---|---|
| `numpy` | `np` | week 17 | Arrays: do maths to a thousand numbers in one line |
| `pandas` | `pd` | week 21 | Tables with named columns — a spreadsheet you can program |
| `matplotlib.pyplot` | `plt` | week 25 | Charts |
| `scikit-learn` | `sklearn` | week 28 | Models, splits, scores. Machine learning |

`import numpy as np` means "load numpy, and let me call it `np` for short". The nicknames are a
worldwide convention, not our invention — every tutorial on earth uses them, so we do too.

---

## 1.14 — What the four libraries actually look like

You do not need this to teach weeks 1–16, but reading it now means nothing in the second half will
surprise you.

**numpy — maths without loops.**

```python
import numpy as np

scores = np.array([[7, 9, 8],
                   [10, 6, 5]])
print(scores.shape)
print(scores * 2)
print(scores.mean(axis=0))
print(scores.mean(axis=1))
print(scores[scores > 7])
```

```text
(2, 3)
[[14 18 16]
 [20 12 10]]
[8.5 7.5 6.5]
[8. 7.]
[ 9  8 10]
```

`(2, 3)` means 2 rows, 3 columns. `scores * 2` doubled every number with no loop at all.
`axis=0` walked **down the columns** (three answers, one per column). `axis=1` walked **across the
rows** (two answers, one per row). And `scores[scores > 7]` pulled out only the values above 7.

The `axis=0` / `axis=1` confusion is universal and permanent. The trick that actually works:
**`axis=0` collapses the rows, so you get one answer per column.** Say it that way round.

**pandas — the same thing, with names on the columns.**

```python
import pandas as pd

classmates = pd.DataFrame({
    "name":  ["Asha", "Ravi", "Meera", "Sam", "Nina"],
    "age":   [12, 12, 13, None, 12],
    "steps": [8400, 6100, 11200, 7300, 9950],
})

print(classmates)
print()
print("Missing values per column:")
print(classmates.isna().sum())
print()
print("Average steps:", classmates["steps"].mean())
```

```text
    name   age  steps
0   Asha  12.0   8400
1   Ravi  12.0   6100
2  Meera  13.0  11200
3    Sam   NaN   7300
4   Nina  12.0   9950

Missing values per column:
name     0
age      1
steps    0
dtype: int64

Average steps: 8590.0
```

Three things to notice, because your student will:

- The `0 1 2 3 4` down the left is the **index**. It is not a column. It is how pandas names rows.
- `age` shows `12.0` not `12`, because one value is missing and a column with a hole in it has to be
  decimal. That surprises everyone. Week 23.
- `NaN` means "not a number" — pandas' word for a hole. Sam's age is genuinely missing, and the
  honest response is to write down what you did about it, not to quietly fill it in.

**matplotlib — charts.** One figure, one drawing box (`ax`), then you tell `ax` what to draw and how
to label it. Always `savefig` at the end. That is the whole model.

---

## 1.15 — The shape of a Python file, and the two whitespace rules

A typical file from week 12 onwards:

```python
# 1. Comment saying what the file is for
# stats.py - my own toolkit of number functions

# 2. Imports, all at the top
import csv

# 3. Function definitions
def average(numbers):
    return sum(numbers) / len(numbers)

# 4. The code that actually does something, at the bottom
scores = [7, 9, 8]
print(average(scores))
```

```text
8.0
```

**Whitespace rule 1 — indentation is four spaces, and it means something.** Everything indented under
an `if`, `for`, `while` or `def` belongs to it. Getting it wrong is a real error, not a style issue.

**Whitespace rule 2 — never mix tabs and spaces.** A tab and four spaces look identical on screen and
are different characters. Python refuses. In VS Code: click **Spaces: 4** in the bottom bar → *Convert
Indentation to Spaces*, and turn *Insert Spaces* on permanently. Do this in week 0. It saves an hour.

> **✅ You now know enough Python to teach every week of this course.** Genuinely. Everything after
> here is either an error message, a library call, or a teaching skill.

---

# 🐞 Section 2 — How to Read a Traceback

This is the skill. Not "how to avoid errors" — nobody avoids errors. **A student who can read a
traceback can program. A student who cannot, cannot.** Same for you.

## 2.0 — An annotated real traceback

Here is a genuine failed run. The file computes averages and one of the lists is empty.

```python
# average.py
def average(numbers):
    total = sum(numbers)
    return total / len(numbers)

def report(name, numbers):
    print(name, "averaged", average(numbers))

report("Asha", [8, 9, 10])
report("Ravi", [])
```

```text
Asha averaged 9.0
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/average.py", line 10, in <module>
    report("Ravi", [])
  File "/private/tmp/ai-academy/level2/average.py", line 7, in report
    print(name, "averaged", average(numbers))
  File "/private/tmp/ai-academy/level2/average.py", line 4, in average
    return total / len(numbers)
ZeroDivisionError: division by zero
```

Now the annotations, and the order you read them in:

```
   READ IT IN THIS ORDER:  ③ ← ① ← ②

   Asha averaged 9.0                                    ④ the program WORKED
                                                           until it didn't. Line 8
                                                           was fine. Something
                                                           changed on line 9.

   Traceback (most recent call last):                   ① "most recent call LAST"
   ┌─────────────────────────────────────────────┐         ⇒ the useful bit is at
   │ File "...average.py", line 10           │         the BOTTOM. Do not read
   │   report("Ravi", [])                         │         this top-down.
   │ File "...average.py", line 7, in report │
   │   print(name, "averaged", average(numbers))  │      ② the CHAIN: line 10 called
   │ File "...average.py", line 4, in average│         line 7, which called
   │   return total / len(numbers)                │         line 4. Where it BROKE
   └─────────────────────────────────────────────┘         is the last one: line 4.
                                                           Where it STARTED is the
                                                           first one: line 10.
   ZeroDivisionError: division by zero                  ③ START HERE. Always.
   ▲                  ▲                                   Two parts, both matter:
   │                  └── what specifically went wrong    · type of problem
   └───────────────────── the KIND of problem              · which thing caused it
```

**The three-question routine. Teach this in week 1 and use the same three questions all year:**

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  READING AN ERROR — THE THREE QUESTIONS                              │
   │                                                                      │
   │   1. WHAT KIND?     Read the last line, before the colon.            │
   │                     "ZeroDivisionError"                              │
   │                                                                      │
   │   2. WHICH THING?   Read the last line, after the colon.             │
   │                     "division by zero"                               │
   │                                                                      │
   │   3. WHICH LINE?    Read the LAST "File ... line N" above it.        │
   │                     "line 4" — and if that's inside a function,      │
   │                     the first File line tells you who called it.     │
   └──────────────────────────────────────────────────────────────────────┘
```

Then, and only then, look at the code. In this case: `len(numbers)` is 0 because `report("Ravi", [])`
passed an empty list. The fix is a decision, not a typo — should `average([])` crash, or return
`None`, or return 0? That is a genuine design question and it is week 12's discussion.

> **🧑‍🏫 If a student asks** *"why is it so long?"* — "Because it's showing you the whole chain of who
> called who. It's being helpful. The bottom line is the answer; everything above it is the trail of
> breadcrumbs showing how you got there."

> **💡 One thing to say once and then never again:** the long `/private/tmp/ai-academy/level2/...` path
> in these tracebacks is just where the file happened to live on the machine that ran it. Your
> student's will show *their* folder. The path is never the interesting part — the line number and the
> last line are.

> **💡 Try this:** Make it a ritual. Whenever an error appears, the student reads the **last line
> out loud** before touching anything. Out loud, every time, all year. It takes four seconds and it
> converts a wall of red into a sentence. Adults who cannot debug are almost always adults who never
> learned to read the last line first.

---

## 2.1 — `NameError` — you used a name Python has never heard of

```python
scores = [7, 9, 8]
print(scroes)
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/scores_bug.py", line 2, in <module>
    print(scroes)
NameError: name 'scroes' is not defined. Did you mean: 'scores'?
```

**In English:** "You asked me for something called `scroes` and I have never been told what that is."

**Almost always one of three things:**
1. A typo (here — and modern Python even suggests the right spelling).
2. You used the name **before** the line that creates it. Order matters.
3. You created it inside a function and are using it outside (**scope**, §1.12).

**Fix:** correct the spelling, or move the `name = ...` line above the line that uses it.

---

## 2.2 — `TypeError` — you did something to a type that can't do it

```python
print("You will be " + 13 + " next year")
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/greet_bug.py", line 1, in <module>
    print("You will be " + 13 + " next year")
TypeError: can only concatenate str (not "int") to str
```

**In English:** "I can glue text to text. `13` is a number. Pick one."

**Fix:** three good options, and they teach different things:

```python
print("You will be " + str(13) + " next year")   # convert the number to text
print("You will be", 13, "next year")            # let print handle it (adds spaces)
print(f"You will be {13} next year")             # f-string - the one to prefer
```

```text
You will be 13 next year
You will be 13 next year
You will be 13 next year
```

All three give the identical sentence. Prefer the third — it is the one this course uses from week 3
on, and it is the one that stays readable when there are four values instead of one.

**Where it comes from 90% of the time:** an `input()` you forgot to wrap in `int()`.

---

## 2.3 — `IndentationError` — the spaces at the front are wrong

Two flavours. **Missing indentation:**

```python
total = 0
for score in [7, 9, 8]:
total = total + score
print(total)
```

```text
  File "/private/tmp/ai-academy/level2/total_bug.py", line 3
    total = total + score
    ^
IndentationError: expected an indented block after 'for' statement on line 2
```

**In English:** "You promised me a block on line 2 by ending it with a colon. Line 3 isn't indented,
so there's no block."

**Fix:** push line 3 in by four spaces.

**Unexpected indentation:**

```python
total = 0
    print(total)
```

```text
  File "/private/tmp/ai-academy/level2/indent_bug.py", line 2
    print(total)
IndentationError: unexpected indent
```

**In English:** "This line is pushed in, but there's nothing above it that opens a block."
**Fix:** move it back to the left margin.

**And the nasty cousin — `TabError`:**

```text
  File "/private/tmp/ai-academy/level2/tab_bug.py", line 3
    print("tab")
TabError: inconsistent use of tabs and spaces in indentation
```

**In English:** "Some of these lines are indented with tabs and some with spaces, and I can't tell
what you meant." **Fix:** VS Code bottom bar → *Convert Indentation to Spaces*. This is the one error
where the screen genuinely lies to you, so do not let a student hunt it for ten minutes — name it and
fix it.

---

## 2.4 — `SyntaxError` from a missing colon

```python
scores = [7, 9, 8]
for score in scores
    print(score)
```

```text
  File "/private/tmp/ai-academy/level2/loop_bug.py", line 2
    for score in scores
                       ^
SyntaxError: expected ':'
```

**In English:** "This sentence isn't finished. I need a colon here."

**In this course, `if`, `elif`, `else`, `for`, `while` and `def` all end with a colon. All six. Every
time.** Modern Python names the missing character, which is a genuine kindness — older versions just
said "invalid syntax" and pointed vaguely.

> **⚠️ Watch out:** A `SyntaxError` can be reported on the line *after* the real problem, because
> Python only notices something is missing when it reaches something that cannot follow. If the
> reported line looks perfect, **look at the line above it.** Teach that in week 5 and it saves an
> hour across the year.

---

## 2.5 — `IndexError` — you asked for a slot that isn't there

```python
scores = [7, 9, 8]
print(scores[3])
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/slot_bug.py", line 2, in <module>
    print(scores[3])
IndexError: list index out of range
```

**In English:** "There is no slot 3."

**And this is the zero-counting injury, exactly.** The list has three items. They live in slots 0, 1
and 2. There is no slot 3. `scores[len(scores)]` is *always* wrong; `scores[len(scores) - 1]` is the
last one, and `scores[-1]` is nicer.

**Fix:** count from zero, or use `scores[-1]`.

---

## 2.6 — `KeyError` — you asked for a dictionary key that isn't there

```python
player = {"name": "Asha", "runs": 42}
print(player["overs"])
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/key_bug.py", line 2, in <module>
    print(player["overs"])
KeyError: 'overs'
```

**In English:** "There's no key called `overs` in this dictionary."

**Almost always:** a typo in the key, a plural (`run` vs `runs`), or a capital (`Name` vs `name`).
Keys are case-sensitive.

**Two fixes, and they mean different things:**

```python
player = {"name": "Asha", "runs": 42}

print(player.get("overs", 0))       # give me 0 if it's missing - no crash
if "overs" in player:               # check first, then decide what to do
    print(player["overs"])
else:
    print("We have no overs figure for Asha.")
```

```text
0
We have no overs figure for Asha.
```

`.get(key, 0)` is convenient and is sometimes a quiet lie — filling a missing number with zero says
"they bowled zero overs" when the truth is "we don't know". Week 15 argues about exactly this, and it
is a direct descendant of Level 1's data-card honesty.

---

## 2.7 — `ZeroDivisionError` — you divided by zero

```python
scores = []
total = 0
print(total / len(scores))
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/average_bug.py", line 3, in <module>
    print(total / len(scores))
ZeroDivisionError: division by zero
```

**In English:** "You asked me to divide by zero. There is no answer to that."

**In this course it is nearly always the same cause:** averaging an **empty list**. `len([])` is 0.

**Fix:** check first.

```python
scores = []
total = 0

if len(scores) == 0:
    print("No scores yet.")
else:
    print(total / len(scores))
```

```text
No scores yet.
```

This is a good bug because the fix is a judgement call, not a typo. What *should* the average of no
scores be? There is no correct answer, and saying so out loud is a real lesson.

---

## 2.8 — `ModuleNotFoundError` — Python can't find the library

```python
import pandaz
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/import_bug.py", line 1, in <module>
    import pandaz
ModuleNotFoundError: No module named 'pandaz'
```

**In English:** "I looked for a library with that name and there isn't one."

**Three causes, in order of likelihood:**

1. **A typo.** `pandaz`, `numpi`, `matplotlib.pyplt`, `sklearn.datsets`.
2. **The virtual environment is not active** — this is the big one, and it is Section 4's row 2. The
   library *is* installed, into a Python you are not currently running. Diagnose it with:
   ```bash
   python -c "import sys; print(sys.executable)"
   ```
   The path it prints **must** contain `.venv`. If it doesn't, run the activate line again.
3. **It genuinely isn't installed.** `pip install pandas`, inside the activated venv.

> **⚠️ Watch out — the self-inflicted version.** If the student names their own file `random.py`,
> `csv.py`, `statistics.py` or `numpy.py`, Python finds *their* file instead of the real library and
> the errors become surreal. Rename the file and delete the `__pycache__` folder next to it. (Week 12
> deliberately creates a file called `stats.py`, which is safe because there is no library called
> `stats` — and the week 12 teacher file explains exactly that distinction.)

---

## 2.9 — `ValueError` from converting text that isn't a number

```python
age_text = "twelve"
age = int(age_text)
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/convert_bug.py", line 2, in <module>
    age = int(age_text)
ValueError: invalid literal for int() with base 10: 'twelve'
```

**In English:** "You asked me to turn this into a whole number. It says `twelve`. I can't."

**In English, the useful part:** *the right type, the wrong value*. `int("12")` is fine. `int("twelve")`
is not. Neither is `int("12.5")`, which surprises people — that needs `float()` first.

**Fix, and it is week 8's mini-project:** don't trust the human. Loop until they type something usable.
Week 8 does it with `.isdigit()` and a `while` loop, no `try`/`except` needed — that is Level 3.

---

## 2.10 — `AttributeError` — that thing doesn't have that

```python
scores = [7, 9, 8]
print(scores.lenght)
```

```text
Traceback (most recent call last):
  File "/private/tmp/ai-academy/level2/method_bug.py", line 2, in <module>
    print(scores.lenght)
AttributeError: 'list' object has no attribute 'lenght'
```

**In English:** "Lists don't have anything called `lenght`."

**Two causes:**
1. A spelling mistake (`lenght`, `apend`, `sortt`).
2. Asking the wrong kind of thing. A list has `.append()`; a string doesn't. A DataFrame has `.head()`;
   a list doesn't. From week 21 this becomes the standard signal for *"you thought that was a
   DataFrame and it's actually a Series"*.

Note also that `len(scores)` is a **function you wrap around** the list, while `scores.append(5)` is a
**method you attach to it with a dot**. Python has both and there is no deep rule. Do not pretend
there is; just say "that one's a wrapper, that one's a dot, you'll remember them".

---

## 2.11 — Off-by-one — no error at all, and one row silently missing

This is the first of the two **silent** bugs, and silent bugs are the dangerous kind.

```python
scores = [7, 9, 8, 10]
for position in range(1, len(scores)):
    print("Score number", position, "is", scores[position])
```

```text
Score number 1 is 9
Score number 2 is 8
Score number 3 is 10
```

**No error. Clean output. Looks completely fine.** And the first score, 7, was never printed. `range(1, 4)`
starts at 1, so slot 0 was skipped.

**Fix:** `range(len(scores))` — or better, drop the counting entirely:

```python
scores = [7, 9, 8, 10]
for score in scores:
    print(score)
```

```text
7
9
8
10
```

**How to catch it:** count the output. Four scores in, four lines out. Three lines means one is
missing. Getting your student to check the *number* of output lines against the number of inputs is a
professional habit and it starts in week 7.

---

## 2.12 — Changing a list while looping over it

The second silent bug, and the strangest-looking one in the course.

```python
scores = [7, 0, 0, 9, 8]
for score in scores:
    if score == 0:
        scores.remove(score)
print(scores)
```

```text
[7, 0, 9, 8]
```

**One of the zeros survived.** The code says "remove every zero" and it removed one of the two. No
error, no warning.

**Why:** the loop keeps its own position counter. It looks at slot 1 (a zero), removes it, and
everything shifts left — the second zero moves into slot 1. But the loop has finished with slot 1 and
moves on to slot 2. The second zero is stepped straight over.

**Fix — build a new list instead of editing the one you're walking:**

```python
scores = [7, 0, 0, 9, 8]
kept = []
for score in scores:
    if score != 0:
        kept.append(score)
print(kept)
```

```text
[7, 9, 8]
```

**Rule to teach, in these words:** *never add to or remove from a list while you are looping over it.
Build a new one.* It is one sentence, it is always right, and it prevents a class of bug that
professionals still hit.

---

## 2.13 — The error summary table

Photocopy this and tape it inside the notebook. It is also the back page of every workbook.

| Error | The message says | It means, in English | First thing to check |
|---|---|---|---|
| `NameError` | `name 'x' is not defined` | I've never heard of `x` | Spelling; is the line that creates it *above*? |
| `TypeError` | `can only concatenate str...` | Wrong kind of value for that operation | Did an `input()` need `int()`? |
| `IndentationError` | `expected an indented block` | The spaces at the front are wrong | Four spaces under every colon line |
| `TabError` | `inconsistent use of tabs and spaces` | Mixed tabs and spaces | Convert Indentation to Spaces |
| `SyntaxError` | `expected ':'` | The sentence isn't finished | The colon. Then the line *above* |
| `IndexError` | `list index out of range` | No such slot | Slots start at 0; last is `-1` |
| `KeyError` | `'overs'` | No such key in the dictionary | Spelling, plural, capital letter |
| `ZeroDivisionError` | `division by zero` | Nothing divided by nothing | Is the list empty? |
| `ModuleNotFoundError` | `No module named 'x'` | Can't find that library | Spelling; then is `.venv` active? |
| `ValueError` | `invalid literal for int()` | Right type, impossible value | Is the text actually a number? |
| `AttributeError` | `'list' object has no attribute` | That thing can't do that | Spelling; is it the type you think? |
| **no error, one row missing** | — | Off-by-one | Count the output lines |
| **no error, wrong result** | — | Changed a list while looping it | Build a new list |
| **no error, `None` appears** | — | A function printed instead of returning | Is there a `return`? |

---

# 🤖 Section 3 — What Machine Learning Adds On Top

Your student did Level 1, so they already have all of this. This section is for **you**, in adult
language, in fifteen minutes.

## 3.1 — The one-paragraph version

There are two ways to make a computer produce an answer.

**Way one: somebody writes the rule.** `if temperature < 20: turn_on_heating()`. A human thought hard,
worked out the rule, and typed it. Predictable, explainable, fixable by editing one line. Most
software in the world is this, correctly.

**Way two: the computer works out the rule from examples.** You collect many examples **with the right
answer attached**, and a program adjusts itself until it gets most of them right. Nobody typed the
rule. That is **machine learning**.

Way two exists because way one hits a wall. Try writing if-then rules for "is this a photo of a cat".
Pointy ears — so are foxes. Whiskers — invisible at that resolution. Fur — so is a rug. Every rule you
add breaks two others. Level 1 spent four weeks making your student feel that wall personally.

## 3.2 — The five words, and their Python spellings

| Word | Means | In this course |
|---|---|---|
| **Feature** | One measured description of one example | A column. Together: `X` |
| **Label** | The answer you want back | A column. On its own: `y` |
| **Training** | Reading labelled examples and producing a model | `model.fit(X_train, y_train)` |
| **Model** | The learned thing. Given features, it guesses a label | the `model` object |
| **Prediction** | A guess for one example | `model.predict(X_test)` |

```
   ┌──────────────┐       ┌────────────┐        ┌───────────┐       ┌────────────┐
   │  a TABLE     │  ───► │  TRAINING  │  ───►  │  a MODEL  │ ───►  │  a GUESS   │
   │  X  +  y     │       │  .fit()    │        │           │       │ .predict() │
   └──────────────┘       └────────────┘        └───────────┘       └────────────┘
      you build it        3 seconds, once        a pile of            for a row it
      (weeks 13-24)       (week 29)              numbers              never saw
```

**Everything hard about machine learning is on the left-hand side of that diagram.** `fit`, `predict`
and `score` are three lines of code. They arrive in week 29 and take one lesson. The table underneath
them takes twenty-four weeks, and that ordering is the single most deliberate decision in this level.

## 3.3 — The train/test rule, which is the whole point

> **Testing a model on the examples it learned from is cheating.** You must hide some examples before
> training, and never let the model see them until you score it.

Level 1 did this with a sealed envelope of photos. Python does it in one line — this is a **single line
quoted for discussion**, not a runnable program; the complete program is three paragraphs down:

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

Read it as: *cut the deck; keep 80% to learn from; lock 20% in a drawer.*

Here is the whole of machine learning, on real data, with the real output:

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

wine = load_wine()
X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

print("Rows used for training:", len(X_train))
print("Rows held back:        ", len(X_test))
print("Score on rows it TRAINED on:", round(model.score(X_train, y_train), 3))
print("Score on rows it NEVER SAW:", round(model.score(X_test, y_test), 3))
```

```text
Rows used for training: 142
Rows held back:         36
Score on rows it TRAINED on: 0.824
Score on rows it NEVER SAW: 0.75
```

**That is it. That is the machine learning.** Fourteen lines, four of which are imports.

And look at the last two numbers. 82.4% on rows it studied. 75% on rows it hadn't seen. **The second
number is the honest one**, and it is lower, and it is *always* lower. When a student reports a score,
your only question is: *"on the training rows or the held-back rows?"* Ask it every single time from
week 29 to week 36.

> **🧑‍🏫 If a student asks** *"why is `random_state=42` there?"* — "It makes the random cut come out
> the same every time you run it, so your score is repeatable and we can compare yours to mine. 42 is
> a joke that programmers have been making since 1979. Any number works."

## 3.4 — Overfitting, with a real picture

> **Overfitting** is when a model learns the specific examples instead of the general pattern. It
> scores brilliantly on what it studied and badly on anything new.

Level 1 called this "memorising instead of learning". Here it is, measured — a decision tree let to
grow deeper and deeper on the same data:

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.3, random_state=0, stratify=wine.target)

print("depth  train   test")
for depth in [1, 2, 3, 5, 10, 20]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0)
    tree.fit(X_train, y_train)
    train_score = round(tree.score(X_train, y_train), 3)
    test_score = round(tree.score(X_test, y_test), 3)
    print(f"{depth:5d}  {train_score:.3f}  {test_score:.3f}")
```

```text
depth  train   test
    1  0.702  0.667
    2  0.927  0.852
    3  0.984  0.963
    5  1.000  0.944
   10  1.000  0.944
   20  1.000  0.944
```

Read down the two number columns and say what you see out loud:

- **Depth 1** — bad at both. It is too simple to have learned the pattern. That is **underfitting**.
- **Depth 3** — 98.4% train, 96.3% test. Close together, both high. **This is the best model in the
  table**, and week 33 is about being able to say why.
- **Depth 5 and beyond** — train hits a **perfect 100%**, and test *drops* to 94.4%. The tree has
  memorised every training row. It is not better. It is worse, and it looks better.

**That gap — 100% versus 94.4% — is the most important number in the level.** Your student produces
their own version of this table in week 33, plots it, and marks the point where the two lines part
company.

> **⚠️ Watch out:** the temptation, for you and for them, is to celebrate the 1.000. Do not. Week 33
> exists so that a training score of 100% becomes a *warning sign* in your student's head rather than
> a trophy. When you see 1.000 in a train column, say "hmm" out loud.

## 3.5 — What scikit-learn actually gives you

Every model in the library — kNN, decision tree, linear regression, and the hundreds you will not
touch — has the **same three methods**. That is the library's one big idea, and it is a genuinely
beautiful piece of design:

| Method | Does | Reads as |
|---|---|---|
| `.fit(X, y)` | Learns from labelled examples | "study these" |
| `.predict(X)` | Guesses labels for new rows | "what about these?" |
| `.score(X, y)` | Reports how many it got right | "how did you do?" |

Which means: **once your student can train one model, they can train any model, by changing one
line.** That is why week 33 can compare three completely different algorithms in one lesson without
teaching three sets of syntax.

Two metric families they will meet:

- **Classification** (which one? a category) → `accuracy_score`, `confusion_matrix`. Both are Level 1
  ideas: correct ÷ total, and the grid of what-got-mistaken-for-what.
- **Regression** (how much? a number) → `mean_absolute_error` ("on average I'm off by 3.4 marks") and
  `r2_score` ("the line explains 89% of the variation"). MAE is the one to trust, because it is in the
  units of the actual thing.

Here it is on six made-up study-hours-to-marks points, with the real output:

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

hours  = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
marks  = np.array([32, 41, 48, 55, 61, 70])

line = LinearRegression()
line.fit(hours, marks)

print("slope     :", round(float(line.coef_[0]), 2), "marks per hour")
print("intercept :", round(float(line.intercept_), 2), "marks")
guesses = line.predict(hours)
print("MAE       :", round(mean_absolute_error(marks, guesses), 2), "marks")
print("R squared :", round(r2_score(marks, guesses), 3))
```

```text
slope     : 7.34 marks per hour
intercept : 25.47 marks
MAE       : 0.66 marks
R squared : 0.997
```

That slope is `y = mx + c` with `m = 7.34` and `c = 25.47`. **Say the slope in real units** — "each
extra hour of study is worth about 7.3 marks" — because a number with units attached is a number a
12-year-old can argue with, and `0.997` is not.

> **⚠️ Watch out:** this example scores an `R²` of 0.997 because the six points were chosen to sit
> almost on a line. Real data does not. The week 32 lesson uses a real sklearn dataset where R² is
> around 0.5, precisely so that nobody leaves thinking lines fit everything.

## 3.6 — And the Level 1 ethics all still apply, with numbers now

Nothing in Level 1 is retired. It is upgraded:

| Level 1 habit | Level 2 version |
|---|---|
| "Out of how many?" | Print `len(X_test)` next to every score. Every time. |
| "What's the baseline?" | If 60% of rows are class A, then 60% is the score to beat, not 0%. |
| A data card | A **cleaning log**: every repair, numbered, with a reason. Week 23–24. |
| "Who's missing from the data?" | `df.groupby("group")` and compare the scores per group. |
| "Confidence isn't correctness" | A model can be confidently wrong, and now you can print the number. |
| "Which chart is fooling me?" | Build a lie with `ax.set_ylim()`, then confess in writing. Week 27. |

---

# 🔧 Section 4 — The Bulletproof Install Guide

**Do this in week 0, alone, before the student is in the room.** Budget 45 minutes. If you install in
week 1 with a 12-year-old watching, you will spend the lesson on PATH variables and they will
conclude programming is mostly waiting.

## 4.1 — Step 1: Python 3.11 or newer (15 min)

Check first. Open a terminal — **macOS:** the Terminal app · **Windows:** PowerShell · **Linux:** your
terminal — and type:

```bash
python3 --version
```

| You see | Do |
|---|---|
| `Python 3.11.x` or higher | ✅ Done with this step. |
| `Python 3.9.x` or `3.10.x` | ✅ Fine for the whole course. Everything here runs on 3.9+. |
| `Python 2.7.x` | ❌ Ancient. Install a new one; do **not** remove the old one — your OS may need it. |
| `command not found` | Try `python --version`. If that fails too, install below. |

Download from **[python.org/downloads](https://www.python.org/downloads/)**.

> **⚠️ Watch out — Windows users, the single most important click in this course:** on the **first**
> screen of the installer, tick **"Add python.exe to PATH"** before pressing Install. Leaving it
> unticked causes about 90% of Windows setup pain, and the symptom (`'python' is not recognized`)
> does not mention PATH at all.

> **⚠️ Watch out — macOS users:** the `python3` that ships with macOS is fine to *check* with, but
> install a real one from python.org (or `brew install python@3.12`). The system one is missing pieces
> and Apple can change it in an OS update, breaking your class in March.

> **⚠️ Watch out — Linux users:** you almost certainly have Python. You may not have `pip` or `venv`.
> On Debian/Ubuntu: `sudo apt install python3-pip python3-venv python3-tk`. That last one gives you
> chart windows; without it charts still save to PNG, which is all this course needs.

## 4.2 — Step 2: a folder and a virtual environment (10 min)

> **A virtual environment** (venv) is a private box of Python libraries belonging to one project.
> Install into the box and you can never break another project — or your operating system — by
> upgrading something.

```bash
# 1) One folder for the entire year. Never delete this.
mkdir -p ~/ai-academy/level2
cd ~/ai-academy/level2

# 2) Create the private box (makes a hidden .venv folder)
python3 -m venv .venv

# 3) Step INTO the box
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows PowerShell
```

After step 3 your prompt starts with `(.venv)`. **That prefix is the whole game.**

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  (.venv) you@laptop level2 %                                        │
   │   ▲▲▲▲▲▲                                                            │
   │   this. EVERY new terminal, you must run the activate line again.   │
   │   It does not stick between sessions. Put it on a sticky note.      │
   └─────────────────────────────────────────────────────────────────────┘
```

## 4.3 — Step 3: the four libraries (10 min, ~300 MB)

```bash
pip install --upgrade pip
pip install numpy pandas matplotlib scikit-learn jupyterlab
```

| Package | Does | First needed |
|---|---|---|
| `numpy` | Fast arrays and array maths | week 17 |
| `pandas` | Named, cleanable tables | week 21 |
| `matplotlib` | Charts | week 25 |
| `scikit-learn` (imports as `sklearn`) | Models, splits, metrics, built-in datasets | week 28 |
| `jupyterlab` | Notebooks — optional until the capstone | week 34 |

Minimum versions this course's outputs were produced against: `numpy 1.24+`, `pandas 1.5+`,
`matplotlib 3.6+`, `scikit-learn 1.2+`. Newer is fine.

## 4.4 — Step 4: the smoke test (5 min) — the one that actually matters

Create `smoke.py` in `~/ai-academy/level2` and **type** these three lines:

```python
import numpy, pandas, matplotlib, sklearn
from sklearn.datasets import load_iris
print("Level 2 ready ·", numpy.__version__, pandas.__version__, sklearn.__version__, load_iris().data.shape)
```

```bash
python smoke.py
```

```text
Level 2 ready · 1.26.4 1.5.3 1.7.1 (150, 4)
```

Your version numbers will differ — that is fine. What matters is that it printed at all, and that
`(150, 4)` at the end. **That is real: 150 iris flowers, 4 measurements each.** You have just loaded
your first dataset and you have not reached week 1.

If instead you see `ModuleNotFoundError: No module named 'pandas'` — see §4.7 row 2. It is almost
always the venv.

## 4.5 — Step 5: prove a chart can appear (5 min)

Charts fail differently from everything else, so test them separately. Create `smoke_plot.py`:

```python
import matplotlib.pyplot as plt                     # the standard nickname

fig, ax = plt.subplots(figsize=(5, 3))              # one figure, one drawing box
ax.plot([1, 2, 3, 4], [2, 4, 8, 16], marker="o")    # four points, joined
ax.set_title("If you can read this, matplotlib works")
ax.set_xlabel("week")
ax.set_ylabel("pizzas eaten")
fig.savefig("smoke_plot.png", dpi=120, bbox_inches="tight")   # always save
plt.show()                                          # try to pop a window too
```

```bash
python smoke_plot.py
```

**Two possible passes, and both are completely fine:**

1. A window pops up with a rising line. Perfect.
2. No window, but a file called `smoke_plot.png` appears in the folder. **Also perfect** — your setup
   just has no window system. Every chart in this course calls `savefig`, exactly so this never blocks
   a lesson.

**Only a fail if neither happens.** Read the terminal and see §4.7 row 4.

## 4.6 — Step 6: an editor (5 min)

| Option | Get it | Best for |
|---|---|---|
| **VS Code** ✅ recommended | [code.visualstudio.com](https://code.visualstudio.com/), then install the **Python** extension by Microsoft | All 36 weeks. Colours, squiggles, a ▷ Run button. |
| **JupyterLab** | already installed — run `jupyter lab` | The capstone, weeks 34–36 |
| **IDLE** | ships with Python | A fallback if the others won't install. It genuinely works. |

In VS Code: **File → Open Folder →** pick `ai-academy/level2`. Then `Ctrl+Shift+P` → type
"Python: Select Interpreter" → choose the one with **`.venv`** in its path.

> **⚠️ Watch out:** skipping that last click is the single most confusing bug in this course. Your
> terminal works, your smoke test passes, and VS Code's Run button says `ModuleNotFoundError`. It is
> not a mystery — VS Code is running a different Python. Pick the `.venv` one.

## 4.7 — Troubleshooting: the 12 things that actually go wrong

| # | Symptom | Most likely cause | Fix |
|:--:|---|---|---|
| 1 | `python: command not found`, or on Windows typing `python` **opens the Microsoft Store** | Not installed, or "Add to PATH" was unticked, or Windows' fake `python.exe` alias is intercepting | Try `python3`, then `py -3` (Windows). Then re-run the python.org installer → **Modify → Add to PATH** → open a **new** terminal (PATH only applies to new ones). On Windows also: *Settings → Apps → Advanced app settings → App execution aliases* → switch **off** both "App Installer python.exe" toggles. |
| 2 | `ModuleNotFoundError: No module named 'pandas'` — **even though pip said it installed** | You installed into one Python and are running another. 90% of the time: venv not activated, or VS Code on the system interpreter | Prove which Python: `python -c "import sys; print(sys.executable)"`. The path **must** contain `.venv`. If not: run the activate line again, and in VS Code `Ctrl+Shift+P` → *Python: Select Interpreter* → the `.venv` one. Belt and braces: install with `python -m pip install pandas`, never bare `pip`. |
| 3 | `error: externally-managed-environment` on `pip install` | Modern macOS (Homebrew) and Debian/Ubuntu **refuse** to let pip touch the system Python | This error is your friend: it means you skipped the venv. Do §4.2, activate, retry. Do **not** use `--break-system-packages`, however tempting. It does exactly what it says. |
| 4 | `plt.show()` runs and **nothing appears**, or `UserWarning: FigureCanvasAgg is non-interactive` | No GUI backend — normal on plain Linux, over SSH, in WSL, in a bare terminal | Not a real problem. Always `fig.savefig("name.png", dpi=120, bbox_inches="tight")` and open the PNG. Every chart in weeks 25–36 does. Want windows on Linux: `sudo apt install python3-tk`. In VS Code, a notebook shows charts inline. |
| 5 | `pip: command not found` but `python3` works | pip not installed separately (some Linux distros), or you are outside the venv | Use `python3 -m pip install ...` — that always finds the pip belonging to the Python you're running. On Debian/Ubuntu: `sudo apt install python3-pip`. |
| 6 | `pip` fails with `SSL: CERTIFICATE_VERIFY_FAILED` | A school or office network inspecting traffic, or missing macOS certificates | macOS: run *"Install Certificates.command"* inside `/Applications/Python 3.x/`. On a school network: do the one-time install on a home network or a phone hotspot. |
| 7 | `pip` hangs, times out, or says `Could not find a version` behind a corporate firewall | A proxy that pip doesn't know about | `pip install --proxy http://user:pass@proxyhost:port numpy pandas matplotlib scikit-learn`. Ask IT for the proxy string. Or install once at home — the venv folder is portable if the OS matches. |
| 8 | Permission denied / `Access is denied` when installing | You are trying to write into a system folder | You should be in a venv, where this cannot happen. If you must go global, `pip install --user`. **Never** `sudo pip install` — that is how operating systems get broken. |
| 9 | `IndentationError: unexpected indent` on a line that looks perfect | Tabs mixed with spaces | VS Code: bottom-right status bar → click **Spaces: 4** → *Convert Indentation to Spaces*. Then set *Editor: Insert Spaces* on, forever. |
| 10 | Imports break strangely after the student names a file | The file is called `random.py`, `csv.py`, `statistics.py`, `numpy.py`… so Python finds theirs first | Rename the file (`my_random.py`) and delete the `__pycache__` folder beside it. |
| 11 | `ImportError: numpy.core.multiarray failed to import`, or `ValueError: numpy.dtype size changed` | Mismatched binaries — pandas or sklearn built against numpy 1.x, numpy 2.x installed underneath | `pip install --upgrade --force-reinstall numpy pandas scikit-learn`. If it persists: `pip install "numpy<2"`. Nuclear option that always works: delete the `.venv` folder and redo §4.2–4.3. Three minutes, breaks nothing else. **That is what a venv is for.** |
| 12 | Everything worked last week and today nothing imports | New terminal session, venv not activated | Run the activate line. This is not a bug, it is how venvs work, and it will happen roughly weekly all year. Sticky note. |

> **💡 Try this:** After you finish setup, write these two lines on a sticky note and put it on the
> laptop lid:
> ```
> cd ~/ai-academy/level2 && source .venv/bin/activate
> python3 filename.py
> ```
> You will use them both, every week, thirty-six times.

## 4.8 — The setup completion checklist

- [ ] `python3 --version` prints 3.9 or higher
- [ ] `~/ai-academy/level2` exists and contains a `.venv` folder
- [ ] My prompt shows `(.venv)` after I run the activate line
- [ ] `python smoke.py` prints `Level 2 ready ... (150, 4)`
- [ ] `python smoke_plot.py` produces a window **or** a `smoke_plot.png` file
- [ ] VS Code is open on the `level2` folder with the `.venv` interpreter selected
- [ ] VS Code is set to spaces, not tabs
- [ ] The activate command is on a sticky note on the laptop
- [ ] I have run `python3 a1.py` from §1.1 and seen `777777`

---

# ❓ Section 5 — The 20 Questions Students Ask in a Coding Class

These come up. Not "might" — do. Short, honest, correct answers you can read aloud.

**1. "Why does it care about ONE missing bracket? It's obvious what I meant."**
Because it genuinely cannot tell. Programming languages are unforgiving on purpose: a language that
guessed would guess wrong occasionally, and a program that is silently wrong is far worse than one
that refuses to run. Being fussy is a safety feature.

**2. "Why do we count from zero? That's stupid."**
It is a fair complaint and it has a real reason: the index is the *offset* from the start. Slot 0 is
"zero steps along". It made the original computers faster, everyone copied it, and now it is
everywhere. You will hate it for a month and then stop noticing.

**3. "Can I just copy this from the internet?"**
Yes, in real life, constantly — professionals do it all day. But not this year, and here is the honest
reason: your fingers have to learn where the colons go, and pasted code teaches them nothing. Type
everything until about week 20. After that, paste, but only if you can say what every line does.

**4. "Is my program good?"**
Three separate questions, and you should ask all three. Does it run? Does it do the job? Can somebody
else read it? Most beginners stop at the first. Section 9 grades exactly those three.

**5. "Why is my answer 1212 instead of 24?"**
Because you multiplied *text* instead of a number. `input()` always hands you text. Wrap it in `int()`.
This will happen to you about twenty more times and then never again.

**6. "How do real programmers remember all this?"**
They don't. They look things up dozens of times a day, forever. What they remember is the *shape* of
things — that a loop needs a colon, that lists count from zero, that the last line of an error is the
useful one. Shapes, not spellings.

**7. "Why is there red everywhere? Did I break it?"**
No. Nothing is broken and nothing can be. Red means Python is telling you something in the only way
it can. An error message is the computer being helpful — the alternative is a program that quietly
does the wrong thing, which is much worse.

**8. "Can I break the computer?"**
Not with anything in this course. The worst you can do is fill the screen with output or start a loop
that never ends, and Ctrl+C stops that. Nothing here deletes files or changes settings.

**9. "Is this how real AI is made?"**
Yes, actually. The library you use in week 29 — scikit-learn — is used by real companies for real
work. Very large models like chatbots use different, bigger tools, but the ideas you are using (a
table, features, a split, a score) are exactly the same ones.

**10. "Why is machine learning only three lines?"**
Because someone else already wrote the hard part and shared it. The three lines are genuinely all
there is. Everything difficult about the job is getting the table right, which is why we spend
twenty-four weeks there and one week on `fit`.

**11. "Why do we have to hide 20% of the data? Isn't more data better?"**
More data for *training* is better. But if you score the model on rows it studied, you are asking a
student to mark their own exam using the answer sheet they revised from. The 20% is the only honest
exam you have.

**12. "Can I make a game?"**
Yes, and you already are — week 8 is a real number-guessing game with hints and a replay loop. Games
with graphics need extra libraries that are outside this course, but everything you learn here is
what those libraries sit on top of.

**13. "Which programming language is the best?"**
There isn't one, any more than there's a best language for talking. Python is the best for *this* job
— data and machine learning — because that is where its libraries are. If you want phone apps or
websites, different languages win.

**14. "Why is my code different from yours if it gives the same answer?"**
Then both are right. There are always several correct ways. What matters is whether somebody else can
read yours. If two versions both work, prefer the shorter one that still explains itself.

**15. "Do I have to write comments? The code works without them."**
You will read your own week-12 code in week 33 and not recognise it. That is not a failure of memory,
it happens to everyone. A comment says *why* — the code already says *what*. Weeks 1–18 comment every
line, and after that only the surprising ones.

**16. "How long should this take me?"**
Longer than you think, and that is normal, not a sign you're bad at it. A five-line program can take
twenty minutes the first time. Professionals spend most of their day not writing code — they are
reading, testing, and finding out why something didn't work.

**17. "Can the model be wrong?"**
Always. Every model in this course has an accuracy below 100% and that is normal operation, not a
fault. The engineering question is never "is it wrong?" but "how often, on what, and does that matter
here?"

**18. "Why do we do it by hand first if the computer can do it?"**
So that you can tell when the computer is wrong. You will hand-compute one distance in week 28 and one
average in week 7, and forever after you will know what the right answer looks like. That is the
entire skill.

**19. "Am I bad at this because I get so many errors?"**
No — and the opposite is closer to true. The number of errors you hit is mostly about how much code
you are writing. Someone with no errors this week wrote nothing this week. Keep the Bug Log; by
March it will be the proudest thing in your notebook.

**20. "What can I build after this?"**
Anything with a table in it. Predict your own test scores from hours studied. Chart a year of your
own step counts. Sort your music by tempo. Level 3 adds neural networks and the maths underneath —
but you will not need to wait for it to build something real.

---

# ⚠️ Section 6 — The 15 Things Adults Get Wrong When Teaching Beginners to Program

Not criticism. These are the standard mistakes, most of them made with the best intentions by
people who are good at programming. You may be about to make several.

**1. Wrong: taking the keyboard.**
Right: never. Point at the screen, ask a question, sit on your hands. This is the big one and it has
its own section (§8). Every time you fix it for them you teach "you can't".

**2. Wrong: explaining before they've tried.**
Right: let them run the broken thing first. A ten-second failure creates a question, and an
explanation answering a real question lands about four times harder than one answering nothing.

**3. Wrong: treating errors as failures.**
Right: errors are the curriculum. Every week of this course *plans* one. If a lesson produces no error
messages, something has gone wrong with the lesson. Say "oh good, an error" and mean it.

**4. Wrong: saying "just" or "simply".**
Right: banned all year. "You just add a colon" tells a struggling 12-year-old that the thing they
found hard is trivial, which means the problem must be them. Nothing is simple the first time. Say
"the next bit is a colon" instead.

**5. Wrong: teaching the elegant version first.**
Right: teach the clumsy version that they can follow, then improve it. A `for` loop with an
accumulator in week 7, `sum()` in week 15, a numpy one-liner in week 18. Three months apart, on
purpose. Showing the one-liner first teaches magic.

**6. Wrong: introducing eight new things because they're all related.**
Right: four pieces of syntax per week, five new words, and that is a ceiling not a target. It feels
painfully slow to you. It is not slow to them. The [syntax ladder](../README.md#-the-syntax-ladder)
is there to keep you honest.

**7. Wrong: letting them paste code they don't understand.**
Right: type everything until about week 20. And the rule after that is: you may paste it if you can
say out loud what each line does. Otherwise it isn't your program.

**8. Wrong: "you don't need to know how that works."**
Right: say instead "you don't need to know **yet**, and here's the one-sentence version." There is a
real difference between a black box you chose to close and one nobody will open for you. `fit()` is
the second kind unless you say the sentence.

**9. Wrong: fixing the symptom you can see.**
Right: find out what they *believed*. A student who writes `if score = 7` may have a typo, or may
genuinely think `=` compares. One takes two seconds; the other takes five minutes and matters far
more. Ask "what did you expect that line to do?"

**10. Wrong: praising the child ("you're so clever").**
Right: praise the specific move ("you read the last line of the error first — that's the habit").
Praising the habit makes the habit repeat. Praising the child makes them afraid of the next hard
thing.

**11. Wrong: writing the code while they watch, "to demonstrate".**
Right: they type, always, even during the worked example. You read the line out loud, they type it.
Slower, and it is the difference between watching swimming and swimming.

**12. Wrong: caring about style before it runs.**
Right: get it working, *then* tidy it. Correcting variable names in a program that crashes is
demoralising and out of order. Readability is week-by-week homework, not an in-the-moment correction.

**13. Wrong: assuming the mistake is stupid.**
Right: almost every beginner mistake is a **reasonable guess about a rule that doesn't exist**.
`age + 5` where age is `"12"` is a perfectly sensible expectation — most humans would do that
conversion automatically. Treat the guess as intelligent, then explain the actual rule.

**14. Wrong: skipping the hand-computation because the computer can do it.**
Right: week 7's average, week 19's row mean, week 28's distance, week 32's line — all done on paper
*first*. A student who has never computed one by hand cannot tell a wrong answer from a right one, and
that is the only thing this course is really teaching.

**15. Wrong: needing to know the answer.**
Right: "I don't know — read me the last line and let's find out" is the most valuable sentence you
will say all year. You are not the reference manual. You are the person who stays calm and reads
carefully, and that is a rarer and more useful thing to model.

---

# 🕐 Section 7 — How to Run a Lesson

Every week uses the same five-part shape. Same order, same timings, thirty-six times. The
predictability is deliberate: neither of you spends any energy wondering what happens next.

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │  THE STANDARD 70-MINUTE CODING LESSON                                      │
   ├──────┬─────────────────────────────────────────────────────────────────────┤
   │      │                                                                     │
   │ 0:00 │  🪝  HOOK  (5 min)  — SCREENS OFF / LIDS DOWN                       │
   │      │  One story, one prediction, one question with a wrong obvious        │
   │      │  answer. Never a definition. The teacher file gives you the exact    │
   │      │  hook. Ends with the student wanting to try something.               │
   │      │  ⚠️ Laptop closed for these five minutes. Non-negotiable.            │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:05 │  🧠  CONCEPT  (12 min — HARD CEILING)                               │
   │      │  The new idea. Concrete anchor first, formal name second, always     │
   │      │  in that order. Bold the new word, one-line definition, move on.     │
   │      │  Max 5 new words and 4 new pieces of syntax. It's in the file.       │
   │      │  ⏰ Still talking at 12 minutes? Stop mid-sentence and go to the     │
   │      │     keyboard. You can finish the point afterwards and it will land   │
   │      │     better, because by then they'll have typed it.                   │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:17 │  💻  TYPE IT TOGETHER  (18 min)  ← the new bit, vs Level 1          │
   │      │  You read each line out loud. THEY type it. Every line.              │
   │      │  Before pressing Run: "what do you think it will print?" — they      │
   │      │  say it or write it. Every single time. Then run it.                 │
   │      │  ⚠️ Never touch the keyboard. Never dictate faster than they type.   │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:35 │  🐞  BREAK IT ON PURPOSE  (10 min)  ← also new, also essential      │
   │      │  The teacher file names this week's planted bug. They introduce it   │
   │      │  deliberately, read the traceback out loud, say what it means in     │
   │      │  English, and fix it. Then it goes in the Bug Log.                   │
   │      │  This block is why this course produces people who can debug.        │
   │      │  Cut it and you have a course that produces people who can copy.    │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:45 │  🎲  BUILD / ACTIVITY  (20 min)  ← the heart of the lesson          │
   │      │  They extend it, or build the week's thing, or do the unplugged      │
   │      │  activity with cards and paper. Hands on. Minimal talking from you.  │
   │      │  If the lesson is running late, cut anything else — never this.      │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 1:05 │  🔑  LAND IT  (5 min)                                               │
   │      │  Three things, in this order:                                        │
   │      │   1. "Tell me the big idea in one sentence, in your own words."      │
   │      │      Their words. Wait. Don't accept the file's sentence recited.    │
   │      │   2. Write the week's vocabulary and new syntax into the notebook —  │
   │      │      the construct, and what it does, in their own words.            │
   │      │   3. Read the homework aloud together and check they can do STEP     │
   │      │      ONE. Not the whole thing. Just step one.                        │
   │      │                                                                     │
   │ 1:10 │  ✅ DONE. The file they wrote today is SAVED and NAMED properly.    │
   └──────┴─────────────────────────────────────────────────────────────────────┘
```

### Squeezing it into 60 minutes

Cut in exactly this order and no other:

1. The second half of the 🎲 build (finish it as homework) — saves up to 10 min
2. The vocabulary write-up (moves to homework) — saves 4 min
3. The concept block down to 6 minutes (the student guide covers it in writing) — saves 6 min

**Never cut the 🪝 hook** (five minutes buys sixty-five minutes of attention), **never cut 🐞 break it
on purpose** (it is the point of the level), and **never cut the one-sentence summary** (it is your
only real evidence anything landed).

### Stretching to 75+ minutes

Add the ✍️ practice questions in class instead of setting them, or run the *"level it up"* extension
in the teacher file. Do **not** add more syntax. The four-per-week cap is the cap.

### The three rituals that make a coding lesson work

These three cost about ninety seconds a week between them and they change everything.

```
   1. PREDICT BEFORE YOU RUN.
      Before every single Run, they say or write what it will print.
      Wrong predictions are the most valuable thing in the room — a wrong
      prediction is a belief made visible, and now you can fix the belief
      rather than the line.

   2. READ THE LAST LINE OUT LOUD.
      Every error. Out loud. Before touching anything. Four seconds.
      This is how a wall of red becomes a sentence.

   3. SAVE AND NAME IT.
      Every file gets a real name (week07_times_table.py, not Untitled1.py)
      and lives in ~/ai-academy/level2. In week 33 they will import week
      12's stats.py. That only works if week 12's file still exists.
```

### Six rules of thumb that work every week

1. **Concrete anchor first, name second.** "You know how a pizza bill splits between four people?
   That's what a variable is for." Never the other way round.
2. **Never say a term without defining it in the same breath.** One line, plain, first time, bolded.
3. **Ask before you tell.** "What do you think that will print?" costs eight seconds and doubles what
   they remember.
4. **Let the wrong answer live for a minute.** Don't correct instantly. "Interesting — how could we
   check?" is nearly always the better next sentence. In this course you *can* check, in four seconds,
   which is a luxury Level 1 didn't have.
5. **Break it on purpose, every week.** The planted bug is in the teacher file. Students love breaking
   things and it is the fastest route to understanding.
6. **End with them talking, not you.** If your voice is the last one in the room, you don't know what
   they learned.

---

# 🙌 Section 8 — How to Help Without Taking the Keyboard

**This is the most important section in this file.** It is the single skill that determines whether
your student ends the year able to program or able to follow instructions.

## 8.1 — Why the keyboard matters so much

The student is stuck. There is a missing colon on line 4. You can see it from where you're standing.

If you reach over and type it, three things happen, and only the first one is good:

1. The program runs. (Two seconds saved.)
2. **The student does not learn to find a missing colon**, which they will need to do roughly four
   hundred more times this year.
3. **The student learns that when things get hard, an adult takes over.** That lesson is expensive and
   it lasts.

The stuck moment is not an obstacle to the lesson. **The stuck moment IS the lesson.** Debugging is
not a skill you learn after programming; it is 70% of programming, and this is where it is taught.

> **⚠️ Watch out:** This is genuinely uncomfortable. Watching a child stare at a screen for four
> minutes with a fixable error in front of them is one of the harder things this course asks of you.
> It gets easier once you've seen them find it themselves twice.

## 8.2 — The escalation ladder

**Always start at rung 1. Only go up one rung at a time. Wait at least 30 seconds between rungs.**

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  THE HELP LADDER — climb slowly, and never skip a rung                   │
   ├──────────────────────────────────────────────────────────────────────────┤
   │                                                                          │
   │  RUNG 0   SAY NOTHING. Count to fifteen, silently.                       │
   │           It will feel like a minute. Most of the time the answer         │
   │           arrives at about second eleven, from them.                      │
   │                                                                          │
   │  RUNG 1   "Read me the last line of the error, out loud."                │
   │           Solves it outright about a third of the time.                   │
   │                                                                          │
   │  RUNG 2   "What did you expect that line to do?"                         │
   │           This is the diagnostic question. Their answer tells you         │
   │           whether it's a typo or a belief. Those need different help.     │
   │                                                                          │
   │  RUNG 3   "Which line number does the error say?"                        │
   │           Narrows the search without doing the search.                    │
   │                                                                          │
   │  RUNG 4   "Put a print() in and let's see what's actually in there."     │
   │           The universal debugging move, and the most transferable         │
   │           thing you can teach. Not "what should be in there" —           │
   │           what IS in there.                                              │
   │                                                                          │
   │  RUNG 5   "Something on line 4 isn't right. Compare it, character by     │
   │           character, with line 7 which works."                           │
   │           Names the line. Does not name the fault.                        │
   │                                                                          │
   │  RUNG 6   "It's about the punctuation at the end of line 4."             │
   │           Names the KIND of fault. Still doesn't say the answer.          │
   │                                                                          │
   │  RUNG 7   "Line 4 is missing a colon."                                   │
   │           You have told them. Fine — you got here honestly.               │
   │           THEY still type it. You do not touch the keyboard.             │
   │                                                                          │
   │  ─────────────────────────────────────────────────────────────────────   │
   │  THERE IS NO RUNG 8. You never type in their file. Not once, all year.   │
   └──────────────────────────────────────────────────────────────────────────┘
```

Most sessions you will never go past rung 4. If you find yourself at rung 6 or 7 twice in one lesson,
the lesson is too hard for today — that is information about pacing, not about the student.

## 8.3 — The seven sentences

Learn these. Say them instead of the thing you were about to say.

| Instead of | Say |
|---|---|
| "You're missing a colon." | **"Read me the last line out loud."** |
| "That should be `==`." | **"What did you expect that line to do?"** |
| "It's not working because…" | **"What's actually in that variable right now? Let's print it."** |
| "Here, let me." | **"You drive. I'll navigate."** |
| "No, that's wrong." | **"Run it and let's see."** |
| "It should be 8.0." | **"What did you predict? What did you get? What's the difference telling us?"** |
| "You've been stuck a while." | **"Tell me what the program is supposed to do, in order, out loud."** |

That last one is called **rubber-ducking** — explaining your code out loud to something that cannot
help. It works absurdly often, because the bug is usually in the gap between what you *think* the code
says and what it says. Teach the student to do it to a pen when you are not there.

## 8.4 — When to actually intervene

There are three cases where waiting is wrong, and you should step in fast:

| Situation | Why waiting is wrong | Do |
|---|---|---|
| **An environment problem** (venv not active, wrong interpreter, library missing) | This is not their bug and there is nothing to learn from it. It is plumbing. | Fix it fast, out loud, name it: "this one's my department, it's the venv again." |
| **Tabs vs spaces** | The screen genuinely lies. No amount of looking will reveal it. | Name it and fix the setting. Do not let them hunt. |
| **Frustration has become distress** | Nothing is learned past that point. | Stop. Stand up. Get a drink. Come back to a *smaller* problem, or end early. A lesson stopped at 50 minutes on a good note beats a lesson finished in tears. |

**The 18-minute rule:** if a single bug has eaten 18 minutes and the student is no longer generating
new ideas, go up the ladder fast to rung 6 or 7. Struggle is productive; grinding is not. The line
between them is whether they are still *trying things*.

## 8.5 — Two chairs and one keyboard

Physically, this is what works:

- **The student sits in front of the laptop.** Always. You sit beside, slightly back, at an angle
  where you can see the screen but are not leaning over it.
- **You point with a finger, or with words — never with the cursor.** Taking the mouse is taking the
  keyboard.
- **Keep your hands somewhere visibly not-the-keyboard.** In your lap, holding a notebook, holding a
  pen. It sounds silly. It works.
- **Once a lesson, swap: they teach you the last five minutes.** Physically move seats if you can. It
  changes what their brain does with the material.

> **💡 Try this:** In week 1, say out loud: *"I have one rule this year — I will never touch your
> keyboard. Not once. Even if it's driving me mad. If you want something typed, you type it."*
> Then keep it. In April they will remind you of it, and that is the moment you know it worked.

---

# ✏️ Section 9 — How to Mark Code

## 9.1 — The three questions, in this order

Code gets graded on exactly three things, and **the order is the grading**.

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  1. DOES IT RUN?                                          (pass / fail) │
   │     Run it. Yourself. Actually run it.                                  │
   │     A program that crashes is not finished, however good it looks.      │
   │     This is binary and it is not negotiable — and it is the ONLY        │
   │     binary one.                                                        │
   │                                                                        │
   │  2. DOES IT DO THE JOB?                                   (the marks)   │
   │     Does the output match what was asked, on the input that was         │
   │     asked, AND on one input you make up yourself?                       │
   │     ⚠️ Always try one input they didn't think of. Empty list. Zero.     │
   │        The word "banana" where a number was wanted. This is where       │
   │        the real learning is, and they will thank you by week 20.        │
   │                                                                        │
   │  3. CAN SOMEBODY ELSE READ IT?                             (the habit)  │
   │     Variable names that say what they hold. Comments on the            │
   │     surprising lines. No dead code left lying around.                  │
   │     Never mark this before 1 and 2 pass. Tidying a broken program       │
   │     is out of order and it is demoralising.                            │
   └─────────────────────────────────────────────────────────────────────────┘
```

## 9.2 — Be strict about exactly four things

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  BE STRICT ABOUT                                                    │
   │                                                                     │
   │   1. IT RUNS.  No credit for "it nearly works". Run it.             │
   │                                                                     │
   │   2. THE ARITHMETIC IS SHOWN SOMEWHERE BY HAND.                     │
   │      Not just the program's answer. Somewhere in the workbook you    │
   │      want to see  40 ÷ 5 = 8.0  in pencil. Level 1's habit,         │
   │      and the only defence against a confident wrong program.        │
   │                                                                     │
   │   3. THE FRACTION IS THERE, next to every score.                    │
   │      "75%" without "27 out of 36" hides how small the test was.     │
   │      From week 29 to week 36, no bare percentages. Ever.            │
   │                                                                     │
   │   4. NO "MAGIC" WORDS.                                              │
   │      Banned all year: magic · it just knows · the AI figured it out │
   │      it's smart · it thinks · it understands · obviously · easy     │
   │      Also banned in YOUR speech: "just" and "simply".               │
   │      Circle it. Ask for the sentence again. Every single time.      │
   └─────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────┐
   │  BE RELAXED ABOUT                                                   │
   │   · Spelling and handwriting (unless you cannot read it)            │
   │   · Their own words instead of the book's — actively prefer theirs  │
   │   · A wrong answer with visible good reasoning — worth most marks   │
   │   · A clumsy solution that works. Working beats elegant, all year.  │
   │   · Getting there by an unexpected route                            │
   │   · Extra prints left in from debugging (that's evidence of         │
   │     debugging, which is what you wanted)                            │
   │   · Variable names that are long and awkward but honest             │
   └─────────────────────────────────────────────────────────────────────┘
```

## 9.3 — The four-tick scheme

Use this on every workbook exercise. Ten minutes a week.

| Mark | Means | Say |
|:--:|---|---|
| ✓✓ | It runs, it does the job, and it reads well | "This is the code I wanted. Read me line 6 and tell me why it's there." |
| ✓ | It runs and does the job; unreadable or uncommented | "Correct. Now make it readable — I'll come back in five minutes and try to read it out loud." |
| ~ | It doesn't run, but the thinking is visibly right | **This is worth more than a bare ✓.** "Your logic is right, one thing slipped. What does the last line of the error say?" |
| ✗ | It runs but does the wrong thing, or the reasoning shows a misconception | Do **not** correct in writing. Find the belief and reteach it in three minutes at the start of next class. |

> **⚠️ Watch out:** ✗ is for a *silent wrong answer*, and it is more serious than ~. A program that
> crashes announces its problem. A program that quietly prints `1212` instead of `24` is the thing
> that gets people hurt in real life, and it deserves the more serious mark. Say that out loud — a
> 12-year-old finds it genuinely interesting that a crash is the *good* outcome.

## 9.4 — Giving feedback on code

- **Ask, don't tell.** "What's in `total` at this point?" surfaces the misconception. "That should be
  0" hides it.
- **Two ticks, one question.** Per file: name two genuinely good things, ask one question that sends
  them back to the code. More than one question and they stop reading.
- **Praise the process, not the child.** "You put a print in to see what was in the variable — that's
  exactly the move" beats "you're so clever". The first makes the habit repeat.
- **Praise the honest failure loudest of all.** A student who writes *"my average came out 1212
  because I forgot int() and I found it by printing the type"* has done better work than one whose
  program worked first time and who cannot say why. Say so, out loud, in those words.
- **Read their code out loud to them.** Line by line, flatly, as written. It is the fastest possible
  readability feedback, it takes ninety seconds, and it is impossible to argue with.

## 9.5 — Marking the term checkpoints (weeks 9, 18, 27)

Mark these **together, out loud, right after the lesson** — not later, alone, in red pen. For each
wrong answer ask: *"which week does this belong to?"* Then write the week number in the margin.

At the end you have a list of weeks to revisit, which is the entire point of a checkpoint.

**There is no grade. Do not give a grade.** The output of a checkpoint is a list of weeks, not a
number. Then actually revisit them — five minutes at the start of the next three lessons.

## 9.6 — Marking the capstone (weeks 34–36)

Use the rubric in [`../../capstone.md`](../../capstone.md). Score each row with the student sitting
next to you, and make them argue for their own score on at least two rows.

**The rows that matter most are the cleaning log and the "what I got wrong" section.** A modest
project with a brutally honest write-up is better work than a flashy one that over-claims. Grade
accordingly and say why, out loud, in front of them.

And one specific thing to look for: **did they report the test score, or the training score?** If the
notebook says "my model was 100% accurate" and the number came from `score(X_train, y_train)`, that is
the one error in this whole course that should cost real marks. It is the thing the entire year was
built to prevent.

---

# ✅ Section 10 — The Pre-Flight Checklist

Run this every week. Four minutes, and it prevents about 90% of lessons that go wrong.

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  ⏱️  BEFORE EVERY CLASS — 4 MINUTES                                     │
   ├─────────────────────────────────────────────────────────────────────────┤
   │                                                                         │
   │  20 MINUTES BEFORE                                                      │
   │   □  Read this week's teacher-guide file, all of it                     │
   │   □  Read "What YOU need to understand first" TWICE                    │
   │   □  ⭐ TYPE AND RUN THIS WEEK'S CODE YOURSELF, from scratch,           │
   │        in a scratch file. All of it. Do not read it — RUN it.           │
   │        If you cannot get it to run cold, the student definitely can't,  │
   │        and you have just found the thing that would have eaten the      │
   │        lesson.                                                          │
   │   □  ⭐ TRIGGER THIS WEEK'S PLANTED BUG YOURSELF and read the real      │
   │        traceback, so you recognise it instantly when it appears.        │
   │   □  Do the week's hand-arithmetic on paper                             │
   │   □  Say the week's big idea out loud in one sentence, in your words    │
   │                                                                         │
   │  5 MINUTES BEFORE                                                       │
   │   □  Terminal open, in ~/ai-academy/level2, with (.venv) showing        │
   │   □  Editor open on the level2 folder, .venv interpreter selected       │
   │   □  Last week's file still runs (open it, run it — 10 seconds)         │
   │   □  Notebook out, open at the Bug Log page                             │
   │   □  Materials for THIS week on the table (check the week's list)       │
   │   □  Last week's homework is here and you have looked at it             │
   │   □  One thing from last week to open with — a good answer, a bug       │
   │      worth revisiting, or a question you owed them                      │
   │   □  Phone on silent, face down. Yours too.                             │
   │   □  Laptop CLOSED, ready for the screens-off hook                      │
   │                                                                         │
   │  AS YOU START                                                           │
   │   □  Water within reach                                                 │
   │   □  60–75 minutes genuinely protected — no doorbell, no "quick call"   │
   │   □  Your hands are somewhere that is not the keyboard                  │
   │                                                                         │
   ├─────────────────────────────────────────────────────────────────────────┤
   │  THE THREE QUESTIONS TO ASK YOURSELF FIRST                              │
   │                                                                         │
   │   1. "What is the ONE sentence I want them saying at 1:10?"             │
   │   2. "What exactly are their hands doing today?"                        │
   │   3. "Which error are we going to meet on purpose, and do I know        │
   │       what its last line says?"                                        │
   │                                                                         │
   │  If you can answer all three, the lesson will be fine.                  │
   │  If you can't answer any, re-read the teacher file.                     │
   └─────────────────────────────────────────────────────────────────────────┘
```

### The end-of-class 60-second review (for you, not them)

One line in the back of your own notebook:

```
   Week ___ · Landed: ______________ · Didn't: ______________
            · Bugs we met: ______________________________
            · Owed them an answer to: _____________________
            · Did I touch the keyboard?  Y / N
```

Thirty-six of those lines is a genuinely useful record. The "bugs we met" column becomes the revision
list for weeks 9, 18 and 27. And that last question is the one that keeps you honest.

### The one-page cheat sheet to keep next to the laptop

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  ACTIVATE     cd ~/ai-academy/level2 && source .venv/bin/activate   │
   │  RUN          python3 filename.py                                   │
   │  STOP A LOOP  Ctrl+C                                                │
   │  WHICH PYTHON python -c "import sys; print(sys.executable)"          │
   │                                                                     │
   │  WHEN IT BREAKS — the three questions                               │
   │    1. What KIND?    last line, before the colon                     │
   │    2. Which THING?  last line, after the colon                      │
   │    3. Which LINE?   the LAST "File ... line N"                      │
   │                                                                     │
   │  WHEN THEY'RE STUCK — the ladder                                    │
   │    0. count to fifteen, silently                                    │
   │    1. "Read me the last line out loud."                             │
   │    2. "What did you expect that line to do?"                        │
   │    3. "Which line does the error say?"                              │
   │    4. "Let's print it and see what's actually in there."            │
   │    5. name the line. 6. name the kind of fault. 7. say the answer.  │
   │    THERE IS NO RUNG 8. Never touch their keyboard.                  │
   │                                                                     │
   │  DID YOU SAVE?   ← ask this first, every time, all year             │
   └─────────────────────────────────────────────────────────────────────┘
```

---

# 🧾 Last Thing

You are going to spend a school year teaching a 12-year-old that a wall of red text is a sentence, and
that the sentence is usually helpful.

That is a better education in thinking than most people get anywhere, and it happens to be delivered
through the skill that will shape their working life. You do not need to be a programmer to hand it
over.

You need three things: to have run the code before class, to protect the block where their hands are
on the keyboard, and to keep your own hands off it for thirty-six weeks running.

Everything else is in the files. And every number in every one of them was printed by a machine that
actually ran the code.

> ### 👉 Next: **[Week 1 — Make the Computer Say Something](../student-guide/week-01.md)**

---

[⬅ Course home](../README.md) · [Week 1 student guide](../student-guide/week-01.md) · [Week 1 workbook](../workbook/week-01.md) · [Syntax ladder](../README.md#-the-syntax-ladder) · [Level 2 glossary](../../glossary.md) · [Capstone](../../capstone.md) · [Assessment pack](../../assessment.md) · [Figure style guide](../figures/STYLE.md)
