# Module 1 — Python From Zero: Variables, Types, and Talking to the Computer

**Level 2 · Module 1 · ~3 hours · Prereqs: Level 1 complete (you know what a feature, a label, and training data are). No programming experience.**

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 2 Home](README.md) · [Next ➡](module-02-decisions-and-loops.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** run a Python file from the terminal and from an editor, and know which one you are using.
2. **You will be able to** store and print values using variables, f-strings, and comments.
3. **You will be able to** name the type of any value (`str`, `int`, `float`, `bool`) and convert between them safely.
4. **You will be able to** read a traceback, find the line number, and fix the error yourself.
5. **You will be able to** write a 30-line program from a blank file without copying it from anywhere.

---

## 🪝 The Hook

In Level 1 you trained a model to tell cats from dogs by dragging pictures into boxes. You never typed a line of code. That was on purpose — you needed to understand *learning from examples* before worrying about semicolons.

But here is the wall you hit. Teachable Machine gave you one button: "Train". You could not ask it *"what happens if I use only 20 photos instead of 200?"* You could not ask *"which photos did it get wrong, and were they all taken indoors?"* You could not feed it a spreadsheet of cricket scores instead of images.

Every one of those questions needs the same thing: a way to tell a computer, precisely, what to do with data. That is what a programming language is. Not magic — just a very literal-minded assistant who does exactly what you say, in order, and complains loudly when your instructions don't make sense.

Today you meet that assistant. Its name is Python.

---

## 🧠 The Concept

### 1. Running Python: the interpreter, `.py` files, and `print()`

#### The plain-language explanation

A **program** is a list of instructions written down in a file. A **programming language** is the set of rules for writing those instructions so a machine can follow them. Python is one such language.

But a file full of Python text is just... text. Something has to *read* it and *do* it. That something is the **Python interpreter** — a program already installed on your computer that reads your instructions one line at a time, top to bottom, and performs each one.

> **Definition — interpreter:** the program that reads your Python file line by line and actually performs the instructions.

There are two ways to talk to it:

```
   WAY 1 — The interactive shell (a conversation)
   ┌──────────────────────────────────────────┐
   │  you type one line  ──►  it answers      │
   │  you type one line  ──►  it answers      │
   │  ...forgets everything when you close it │
   └──────────────────────────────────────────┘

   WAY 2 — A .py file (a written recipe)
   ┌──────────────────────────────────────────┐
   │  hello.py:                               │
   │     line 1  ─┐                           │
   │     line 2   ├─► python3 hello.py ─► out │
   │     line 3  ─┘                           │
   │  saved forever, re-runnable, shareable   │
   └──────────────────────────────────────────┘
```

You will use Way 1 to poke at small things, and Way 2 for everything you actually keep.

#### 🍕 The analogy

The interactive shell is like standing next to a chef and saying "chop an onion" — she chops it, you see the result, then you say the next thing. A `.py` file is a **written recipe** you hand over: she reads it top to bottom and does every step without stopping to ask you.

Recipes are better when you want the same dish twice. That is why almost all real code lives in files.

#### The tiny concrete example

The very first instruction anyone learns is `print()`. It means "show this on the screen."

```python
print("Hello, Ramana")
```

Output:

```
Hello, Ramana
```

Three things to notice, because each one is a rule you will use forever:

| Piece | What it is | Rule |
|---|---|---|
| `print` | the name of a built-in **function** — a named action | must be spelled exactly, lowercase |
| `(` ... `)` | the parentheses that say "run it, with this input" | never optional |
| `"Hello, Ramana"` | a piece of text, wrapped in quotes | quotes must match: `"..."` or `'...'` |

> **Definition — function:** a named action you can run. You "call" it by writing its name followed by parentheses.

If you leave out the quotes, Python thinks `Hello` is the name of something and goes looking for it. It will not find it. You will get an error. That is fine — you will learn to read errors in sub-concept 5.

---

### 2. Variables and assignment, plus naming rules that keep code readable

#### The plain-language explanation

A **variable** is a name you attach to a value so you can use the value later without retyping it.

> **Definition — variable:** a label that points at a value stored in the computer's memory.

You create one with `=`, which in Python does **not** mean "is equal to". It means **"put the thing on the right into the name on the left."** Read it out loud as "gets":

```python
score = 47          # read: "score GETS 47"
```

The value can be changed later by assigning again. The name stays; what it points at changes.

```python
score = 47
score = 52
print(score)
```

Output:

```
52
```

#### 🍕 The analogy

A variable is a **labelled lunchbox**. The label on the lid says `score`. Inside is a sandwich. Tomorrow you can throw out the sandwich and put in pasta — the label still says `score`, but what's inside is different. When someone asks "what's in `score`?", they get whatever is in there *right now*.

```
      name              value in memory
   ┌─────────┐          ┌──────────┐
   │  score  │ ───────► │    52    │
   └─────────┘          └──────────┘
   the label            the lunchbox contents
```

#### The tiny concrete example with real numbers

You bought 3 pizzas at ₹450 each and split the bill among 5 friends.

```python
pizzas = 3               # how many pizzas
price_each = 450         # rupees per pizza
friends = 5              # how many people split it

total = pizzas * price_each      # 3 * 450 = 1350
share = total / friends          # 1350 / 5 = 270.0

print(total)
print(share)
```

Output:

```
1350
270.0
```

Notice `270.0`, not `270`. Division in Python always produces a decimal number. That is a type rule, and types are next.

#### Naming rules — the hard rules and the kind rules

**Hard rules (Python enforces these; break one and you get an error):**

| Rule | Good | Bad |
|---|---|---|
| Start with a letter or `_` | `score2` | `2score` |
| Letters, digits, underscores only | `top_score` | `top-score`, `top score` |
| Case matters | `score` ≠ `Score` | assuming they're the same |
| Can't be a reserved word | `class_size` | `class`, `if`, `for`, `print` (last one works but breaks `print`) |

**Kind rules (Python doesn't care; humans reading your code do):**

- Use `snake_case`: all lowercase, words joined by underscores. `total_minutes`, not `TotalMinutes` or `tm`.
- Say what the thing *is*, not what type it is. `student_count`, not `num1`.
- Single letters are only okay for maths (`x`, `y`) and short counters.

Bad naming is the #1 reason people cannot read their own code from two weeks ago. You will write hundreds of files in this course. Name things like a future stranger has to read them — because in two weeks, you are that stranger.

#### Comments

A **comment** is a note to humans. Python ignores everything after a `#` on a line.

> **Definition — comment:** text in your file that Python skips, written to explain *why* the code does what it does.

```python
# Convert screen time to a yearly figure so it feels real.
daily_minutes = 190          # measured from phone settings, Monday-Sunday average
yearly_hours = daily_minutes * 365 / 60
print(yearly_hours)
```

Output:

```
1155.8333333333333
```

Good comments explain **why**, not **what**. `x = x + 1  # add one to x` is useless. `x = x + 1  # count this student as present` is gold.

---

### 3. Types: `str`, `int`, `float`, `bool` — and why `'5' + 5` is an error

#### The plain-language explanation

Every value in Python has a **type** — a category that decides what you are allowed to do with it.

> **Definition — type:** the category a value belongs to, which determines what operations make sense on it.

The four you need today:

| Type | Full name | What it holds | Examples |
|---|---|---|---|
| `str` | string | text | `"pizza"`, `"47"`, `""`, `"Ramana"` |
| `int` | integer | whole numbers | `47`, `0`, `-3`, `1000000` |
| `float` | floating point | numbers with a decimal point | `3.5`, `270.0`, `-0.25` |
| `bool` | boolean | one of exactly two values | `True`, `False` |

You can ask Python the type of anything with the `type()` function:

```python
print(type("pizza"))
print(type(47))
print(type(3.5))
print(type(True))
```

Output:

```
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

Read `<class 'str'>` as "this is a string." (`class` is a word we will properly meet in Level 3. Ignore it for now.)

#### 🍕 The analogy

Types are the difference between **the number 5** and **the character "5" painted on a jersey**.

You can add the number 5 to another number. You cannot add a painted jersey to a number — the question is nonsense. But you *can* stitch two jerseys together into one longer strip of fabric.

That is exactly how Python behaves:

```python
print(5 + 5)          # two numbers → arithmetic
print("5" + "5")      # two strings → stitching (called concatenation)
```

Output:

```
10
55
```

Same symbol `+`, two totally different jobs, decided entirely by the *types* of the things around it.

> **Definition — concatenation:** joining two strings end to end with `+`.

#### Why `'5' + 5` is an error

Now mix them:

```python
print("5" + 5)
```

Output:

```
Traceback (most recent call last):
  File "/Users/you/demo.py", line 1, in <module>
    print("5" + 5)
TypeError: can only concatenate str (not "int") to str
```

Python is being *honest*, not difficult. It genuinely does not know which you meant:

- Did you want `10` (treat the jersey as a number)?
- Did you want `"55"` (paint the number onto a jersey)?

Some languages guess. Guessing is how a bank once charged someone `"100"` + `50` = `"10050"` rupees. Python refuses to guess. You must say which you meant:

```python
print(int("5") + 5)      # "make it a number first" → 10
print("5" + str(5))      # "make it text first"     → "55"
```

Output:

```
10
55
```

#### The tiny concrete example with real numbers

Three operations on numbers you should know now:

```python
print(7 / 2)      # true division  → always a float
print(7 // 2)     # floor division → whole part only
print(7 % 2)      # modulo         → the remainder
print(7 ** 2)     # power          → 7 squared
```

Output:

```
3.5
3
1
49
```

`%` (modulo) looks strange but you will use it constantly. "What is the remainder when I divide?" answers questions like *"is this number even?"* (`n % 2 == 0`) and *"how many minutes left over after full hours?"* (`total_minutes % 60`).

Worked by hand: 7 ÷ 2 = 3 with 1 left over. So `7 // 2` is `3` and `7 % 2` is `1`. Check: `3 * 2 + 1 = 7`. ✔

---

### 4. f-strings and formatted output

#### The plain-language explanation

You will constantly want to print a sentence with a value inside it. The clumsy way:

```python
name = "Ramana"
age = 12
print("Hi " + name + ", you are " + str(age) + " years old.")
```

That works, but it is ugly, and you had to remember `str(age)`. The good way is an **f-string**.

> **Definition — f-string:** a string with an `f` in front of the opening quote, where anything inside `{curly braces}` is replaced by the value of that expression.

```python
name = "Ramana"
age = 12
print(f"Hi {name}, you are {age} years old.")
```

Output:

```
Hi Ramana, you are 12 years old.
```

The `f` is not optional. Without it you get the braces printed literally:

```python
print("Hi {name}")     # forgot the f
```

Output:

```
Hi {name}
```

#### 🍕 The analogy

An f-string is a **fill-in-the-blanks form**. You write the sentence once with blanks:

```
"Hi ______, you are ______ years old."
```

and Python fills each blank with the current value. Change the variable, re-run, the form fills itself in again.

#### The tiny concrete example with real numbers

f-strings can do arithmetic inside the braces, and can control decimal places with `:.2f` ("show as a float with 2 decimal places").

```python
runs = 347                 # total runs scored this season
matches = 9                # matches played

print(f"You scored {runs} runs in {matches} matches.")
print(f"Average: {runs / matches}")
print(f"Average: {runs / matches:.2f}")
print(f"Average: {runs / matches:.1f}")
```

Output:

```
You scored 347 runs in 9 matches.
Average: 38.55555555555556
Average: 38.56
Average: 38.6
```

Work it by hand: 347 ÷ 9 = 38.5555... . Rounded to 2 places → 38.56. Rounded to 1 place → 38.6. ✔

Two more formatting tricks worth knowing right now:

```python
big = 1234567
print(f"{big:,}")            # comma separators
print(f"{0.734:.1%}")        # show a fraction as a percentage
```

Output:

```
1,234,567
73.4%
```

---

### 5. `input()`, type conversion, and reading tracebacks without panic

#### The plain-language explanation — `input()`

`input()` stops the program, shows a prompt, waits for the human to type something and press Enter, and hands back what they typed.

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

A run of it:

```
What is your name? Ramana
Hello, Ramana!
```

**The single most important fact about `input()`:** it *always* gives you a `str`. Always. Even if the human types `12`.

```python
age = input("Age? ")       # human types: 12
print(type(age))
```

Output:

```
Age? 12
<class 'str'>
```

So `age * 2` would give you `"1212"`, not `24`. That is the trap. You must convert.

#### Type conversion (casting)

> **Definition — type conversion (casting):** turning a value of one type into an equivalent value of another type, using `int()`, `float()`, `str()`, or `bool()`.

```python
print(int("12"))          # str → int
print(float("3.5"))       # str → float
print(str(12))            # int → str
print(int(3.9))           # float → int  (chops off, does NOT round)
print(float(12))          # int → float
```

Output:

```
12
3.5
12
3
12.0
```

⚠️ `int(3.9)` is `3`, not `4`. `int()` **truncates** — it throws away everything after the decimal point. If you want proper rounding use `round(3.9)` which gives `4`.

Casting fails when the text isn't a valid number:

```python
print(int("twelve"))
```

Output:

```
Traceback (most recent call last):
  File "/Users/you/demo.py", line 1, in <module>
    print(int("twelve"))
ValueError: invalid literal for int() with base 10: 'twelve'
```

Also note: `int("3.5")` **fails** too, because `"3.5"` is not a whole number written down. Use `float("3.5")` and then `int(...)` if you truly want the whole part.

#### 🍕 The analogy — casting

Casting is **currency exchange**. `int("12")` swaps a text-note that reads "12" for an actual coin worth 12. The exchange counter will refuse a note that reads "twelve", and it will refuse a note that reads "3.5" if you asked specifically for whole coins.

#### Reading tracebacks without panic

> **Definition — traceback:** the block of text Python prints when it gives up, showing where it stopped and why.

Every traceback has the same three parts. Learn to find them and errors stop being scary.

```
Traceback (most recent call last):
  File "/Users/you/profile.py", line 4, in <module>          ◄── ① WHERE
    total = price * quantity                                  ◄── ② THE LINE
NameError: name 'quantity' is not defined                     ◄── ③ WHAT & WHY
```

**Always read the LAST line first.** That is the actual error. The stuff above it is the path Python took to get there.

```
  ┌──────────────────────────────────────────────────────┐
  │  HOW TO READ A TRACEBACK                             │
  │                                                      │
  │  1. Jump to the LAST line   → error type + message   │
  │  2. Find the line number    → "line 4"               │
  │  3. Open that line in your editor                    │
  │  4. Check the line ABOVE it too (unclosed brackets   │
  │     make Python blame the next line)                 │
  └──────────────────────────────────────────────────────┘
```

The five errors you will meet this week:

| Error type | Plain-English meaning | Typical cause |
|---|---|---|
| `SyntaxError` | "That isn't Python." | missing `)`, missing quote, missing `:` |
| `NameError` | "You used a name I've never seen." | typo, or used before assigning |
| `TypeError` | "Right names, wrong kinds of thing." | `"5" + 5` |
| `ValueError` | "Right kind of thing, impossible value." | `int("twelve")` |
| `ZeroDivisionError` | "You divided by zero." | `total / count` when `count` is 0 |

Note the difference between the last two, because it trips everyone up:

- `int("twelve")` → **`ValueError`**. You gave `int()` a string, which is the right *type*, but "twelve" isn't a *value* it can use.
- `int(["a"])` → **`TypeError`**. You gave it a completely wrong kind of thing.

#### The tiny concrete example

Here is a five-line program with three bugs. Read the tracebacks, not the code, to fix it.

```python
# buggy.py
name = input("Name? ")
age = input("Age? ")
next_year = age + 1
print(f"Next year {nme} will be {next_year}")
```

Run 1:

```
Name? Ramana
Age? 12
Traceback (most recent call last):
  File "buggy.py", line 4, in <module>
    next_year = age + 1
TypeError: can only concatenate str (not "int") to str
```

Last line: `TypeError`, str + int. Line 4. `age` came from `input()` so it's a str. Fix: `age = int(input("Age? "))`.

Run 2:

```
Name? Ramana
Age? 12
Traceback (most recent call last):
  File "buggy.py", line 5, in <module>
    print(f"Next year {nme} will be {next_year}")
NameError: name 'nme' is not defined
```

Last line: `NameError`, `nme`. Line 5. Typo. Fix: `name`.

Run 3:

```
Name? Ramana
Age? 12
Next year Ramana will be 13
```

Fixed. Two tracebacks, two fixes, zero panic. **That loop — run, read the last line, fix, run again — is what programming actually is.** Not typing perfect code. Nobody types perfect code.

---

## 🔍 Worked Example

**The problem.** Build a program that turns raw screen-time numbers into something a person can actually feel. Take a daily screen time in hours (a decimal, like 3.2), and report:

1. minutes per day
2. hours per year
3. full 24-hour days per year
4. what percentage of waking life that is (assume 16 waking hours a day)

I will trace every number.

### Step 1 — Write down the inputs as variables

```python
hours_per_day = 3.2        # a float, because 3.2 has a decimal point
days_per_year = 365        # an int
waking_hours_per_day = 16  # an int; we assume 8 hours of sleep
```

Types so far: `float`, `int`, `int`.

### Step 2 — Minutes per day

```python
minutes_per_day = hours_per_day * 60
```

Arithmetic by hand: 3.2 × 60 = **192.0**

Type check: `float × int → float`. Whenever a float touches an int in arithmetic, the answer is a float. So `minutes_per_day` is `192.0`, not `192`.

### Step 3 — Hours per year

```python
hours_per_year = hours_per_day * days_per_year
```

By hand: 3.2 × 365. Break it up: 3 × 365 = 1095, and 0.2 × 365 = 73. Total = **1168.0**

### Step 4 — Full 24-hour days per year

```python
days_of_screen = hours_per_year / 24
```

By hand: 1168 ÷ 24. 24 × 48 = 1152. Remainder 16. 16 ÷ 24 = 0.6666... So **48.666666...**

Let's also get the whole part and the leftover hours separately:

```python
whole_days = int(days_of_screen)              # truncate
leftover_hours = hours_per_year % 24          # remainder
```

- `int(48.6666...)` = **48**
- `1168.0 % 24` = **16.0** (because 24 × 48 = 1152, and 1168 − 1152 = 16)

Sanity check: 48 days and 16 hours. 48 × 24 + 16 = 1152 + 16 = 1168. ✔

### Step 5 — Percentage of waking life

```python
waking_hours_per_year = waking_hours_per_day * days_per_year
fraction = hours_per_year / waking_hours_per_year
```

- 16 × 365 = **5840**
- 1168 ÷ 5840 = **0.2** exactly (because 5840 × 0.2 = 1168) ✔

So 20% of waking life.

### Step 6 — The whole program

```python
# screen_time.py — turn a daily screen-time figure into numbers you can feel.

hours_per_day = 3.2            # daily average, in hours (a decimal)
days_per_year = 365            # ignore leap years
waking_hours_per_day = 16      # assume 8 hours of sleep

minutes_per_day = hours_per_day * 60                 # 3.2 * 60      = 192.0
hours_per_year = hours_per_day * days_per_year       # 3.2 * 365     = 1168.0
days_of_screen = hours_per_year / 24                 # 1168 / 24     = 48.666...
whole_days = int(days_of_screen)                     # truncate      = 48
leftover_hours = hours_per_year % 24                 # remainder     = 16.0

waking_hours_per_year = waking_hours_per_day * days_per_year   # 16*365 = 5840
fraction = hours_per_year / waking_hours_per_year              # 1168/5840 = 0.2

print("===== SCREEN TIME REPORT =====")
print(f"Per day        : {hours_per_day} h  ({minutes_per_day:.0f} minutes)")
print(f"Per year       : {hours_per_year:,.0f} hours")
print(f"That is        : {whole_days} full days and {leftover_hours:.0f} hours")
print(f"Waking life    : {fraction:.1%}")
print("==============================")
```

### Step 7 — The exact output

```
===== SCREEN TIME REPORT =====
Per day        : 3.2 h  (192 minutes)
Per year       : 1,168 hours
That is        : 48 full days and 16 hours
Waking life    : 20.0%
==============================
```

Every number in that output was computed by hand above. That habit — predicting the output before running — is what separates people who debug in ten seconds from people who stare for an hour.

---

## 💻 Hands-On

### Part A — Get Python running (15 minutes)

**Step 1. Check if you already have it.** Open a terminal (macOS: Terminal app; Windows: PowerShell; Linux: your terminal) and type:

```bash
python3 --version
```

You want to see something like `Python 3.11.6`. Any `3.9` or higher is fine for this whole level.

On Windows, if `python3` isn't found, try:

```bash
python --version
```

If neither works, install from [python.org/downloads](https://www.python.org/downloads/). On the Windows installer, **tick the box that says "Add Python to PATH"** before clicking Install. That box causes 90% of Windows setup pain when it's left unticked.

**Step 2. Try the interactive shell.**

```bash
python3
```

You'll see `>>>`. That's the prompt. Type:

```
>>> 2 + 2
4
>>> "pizza" * 3
'pizzapizzapizza'
>>> exit()
```

`exit()` gets you out. (Ctrl-D on macOS/Linux also works.)

**Step 3. Get an editor.** Install [VS Code](https://code.visualstudio.com/) (free). Open it, go to the Extensions panel (the four-squares icon), search "Python", install the one by Microsoft. That gives you colours, error squiggles, and a Run button.

**Step 4. Make a folder for this level.**

```bash
mkdir -p ~/ai-academy/level2
cd ~/ai-academy/level2
```

Then in VS Code: File → Open Folder → pick `ai-academy/level2`. Keep every file from this level here.

### Part B — Your first file (10 minutes)

In VS Code, File → New File, save it as `hello.py` inside that folder. Type this **by hand** (do not copy-paste — your fingers need to learn the punctuation):

```python
# hello.py — my first Python program.

print("Hello, world.")            # print text
print(2 + 2)                      # print the result of arithmetic
print("2 + 2")                    # print the text "2 + 2" (quotes = text!)
```

Run it two ways:

**From the terminal:**

```bash
python3 hello.py
```

**From VS Code:** click the ▷ Run button in the top right.

Expected output either way:

```
Hello, world.
4
2 + 2
```

If line 3 and line 4 look surprising, re-read sub-concept 3. Quotes change everything.

### Part C — Variables and types (20 minutes)

New file, `types_tour.py`:

```python
# types_tour.py — a guided tour of Python's four basic types.

# ---- str: text, always in quotes ----
player = "Rohit"                       # a string
print(player, type(player))            # print() can take several things, comma-separated

# ---- int: whole numbers, no quotes, no decimal point ----
runs = 264                             # an integer
print(runs, type(runs))

# ---- float: numbers with a decimal point ----
strike_rate = 152.75                   # a float
print(strike_rate, type(strike_rate))

# ---- bool: exactly True or False, capital first letter ----
is_captain = False                     # a boolean
print(is_captain, type(is_captain))

print("-" * 40)                        # a divider line: "-" repeated 40 times

# ---- Arithmetic ----
balls_faced = 173                      # how many balls he faced
sr = runs / balls_faced * 100          # strike rate = runs per 100 balls
print(f"Strike rate: {sr:.2f}")        # 264/173 = 1.5260... -> *100 -> 152.60

# ---- Same symbol, different jobs, decided by type ----
print(3 + 4)                           # numbers add        -> 7
print("3" + "4")                       # strings join       -> 34
print("ha" * 3)                        # string * int       -> hahaha
# print("3" + 4)                       # <-- uncomment this to see a TypeError

# ---- Converting on purpose ----
print(int("3") + 4)                    # 7
print("3" + str(4))                    # 34
print(int(9.99))                       # 9   (truncates, does not round)
print(round(9.99))                     # 10  (rounds properly)
```

Expected output:

```
Rohit <class 'str'>
264 <class 'int'>
152.75 <class 'float'>
False <class 'bool'>
----------------------------------------
Strike rate: 152.60
7
34
hahaha
7
34
9
10
```

Now **uncomment** the `print("3" + 4)` line and run again. Read the traceback. Find the line number. Then comment it back out. You just deliberately caused and diagnosed an error — do this often, on purpose. It's the cheapest way to learn.

### Part D — Input and conversion (20 minutes)

New file, `bill_split.py`:

```python
# bill_split.py — split a restaurant bill, with tip, among friends.

print("=== BILL SPLITTER ===")

# input() ALWAYS returns a string, so we wrap it in float()/int() immediately.
bill = float(input("Total bill amount (rupees): "))     # e.g. 1240.50
people = int(input("How many people?          : "))     # e.g. 4
tip_percent = float(input("Tip percent (e.g. 10)     : "))  # e.g. 10

tip_amount = bill * tip_percent / 100     # 1240.50 * 10 / 100 = 124.05
grand_total = bill + tip_amount           # 1240.50 + 124.05   = 1364.55
per_person = grand_total / people         # 1364.55 / 4        = 341.1375

print("-" * 30)
print(f"Bill        : {bill:>10.2f}")     # >10 means right-align in 10 characters
print(f"Tip ({tip_percent:.0f}%)   : {tip_amount:>10.2f}")
print(f"Grand total : {grand_total:>10.2f}")
print(f"Each pays   : {per_person:>10.2f}")
print("-" * 30)
```

Run it and type `1240.50`, `4`, `10`. Expected output:

```
=== BILL SPLITTER ===
Total bill amount (rupees): 1240.50
How many people?          : 4
Tip percent (e.g. 10)     : 10
------------------------------
Bill        :    1240.50
Tip (10%)   :     124.05
Grand total :    1364.55
Each pays   :     341.14
```

Check by hand: 10% of 1240.50 is 124.05. Sum is 1364.55. Divided by 4 is 341.1375, shown to 2 places as 341.14. ✔

Now break it on purpose, twice:

1. Run again and type `four` for the number of people. You get a `ValueError`. Read it.
2. Run again and type `0` for the number of people. You get a `ZeroDivisionError`. Read it.

You cannot fix either of those yet — fixing them needs `if` statements, which is Module 2. For now, just recognise the tracebacks. Knowing the name of a problem is half of solving it.

### Part E — Debug drill (15 minutes)

Save this as `debug_me.py` exactly as written. It has **four** bugs. Run it, fix the first traceback, run again, repeat.

```python
# debug_me.py — four bugs. Fix them one traceback at a time.
Name = input("Your name: ")
height_cm = input("Your height in cm: ")
height_m = height_cm / 100
print(f"Hi {name}, you are {height_m} m tall.)
```

Bugs, in the order Python will find them (don't peek until you've tried):

<details><summary>Click to reveal the four bugs</summary>

1. **Line 5, `SyntaxError`** — the f-string is missing its closing `"`. Python finds syntax errors *before running anything*, so this one appears first even though it's on the last line. Fix: `print(f"Hi {name}, you are {height_m} m tall.")`
2. **Line 4, `TypeError`** — `height_cm` is a `str` from `input()`, and you can't divide a string. Fix: `height_cm = float(input("Your height in cm: "))`
3. **Line 5, `NameError`** — the variable is `Name` (capital N) but you used `name`. Python is case-sensitive. Fix: rename the variable to `name` on line 2 (lowercase is the convention).
4. **Cosmetic, not an error** — 162 cm prints as `1.62`, but 170 cm prints as `1.7`. Fix the formatting: `{height_m:.2f}`.

Fixed version:

```python
# debug_me.py — fixed.
name = input("Your name: ")                              # lowercase name
height_cm = float(input("Your height in cm: "))          # convert to a number
height_m = height_cm / 100                               # 162 / 100 = 1.62
print(f"Hi {name}, you are {height_m:.2f} m tall.")      # closing quote + 2 decimals
```

Output for `Ramana` / `162`:

```
Your name: Ramana
Your height in cm: 162
Hi Ramana, you are 1.62 m tall.
```

</details>

---

## ✍️ Practice

### 1. [Warm-up] Name that type

Write `type_quiz.py`. For each of these eight values, first **write your guess in a comment**, then print the real type with `type()`:

`42` · `42.0` · `"42"` · `True` · `4 + 2` · `4 / 2` · `"4" * 2` · `42 > 40`

**Done looks like:** eight lines of output, and a comment above each showing your guess. Count how many you got right out of eight.

### 2. [Warm-up] Rectangle report

Write `rectangle.py` that stores `length = 12.5` and `width = 4` as variables, then prints exactly three lines using f-strings:

```
Length 12.5 m, width 4 m
Area: 50.00 square metres
Perimeter: 33.00 metres
```

**Done looks like:** output matches character for character, every number comes from a variable (no number typed twice), and areas show exactly 2 decimal places.

### 3. [Build] Seconds decoder

Write `seconds.py` that asks the user for a whole number of seconds and prints it as hours, minutes, and seconds.

For input `7325` it must print:

```
7325 seconds = 2 h 2 m 5 s
```

**Hints:** you need `//` and `%`. 7325 ÷ 3600 = 2 remainder 125. 125 ÷ 60 = 2 remainder 5.

**Done looks like:** correct output for `7325`, `59`, `3600`, and `86399`. Write the four expected outputs in comments at the bottom of the file and check each one.

### 4. [Build] Study-time cost calculator

Write `study_cost.py` that asks for four things: hours studied per day (decimal allowed), days per week, weeks in the term, and the cost per hour of a tutor in rupees. It prints a formatted card:

```
========================================
  STUDY PLAN
========================================
  Hours/day    : 2.5
  Days/week    : 5
  Weeks        : 14
  ------------------------------------
  Total hours  : 175.0
  Tutor cost   : 87,500
  Cost/week    : 6,250
========================================
```

**Done looks like:** the box is aligned, money has comma separators (`{value:,.0f}`), all four values come from `input()` with correct conversions, and a decimal input for hours/day works.

### 5. [Stretch] Traceback triage

Create `broken.py` containing exactly this:

```python
temperature_c = input("Temp in C: ")
temperature_f = temperature_c * 9 / 5 + 32
print("That is " + temperature_f + " degrees F")
print(f"Or {tempature_f:.1f} F")
```

For each bug: write down (a) the error type, (b) the line number Python reports, (c) a one-sentence plain-English explanation, and (d) the fix. Then produce a fully working version.

**Done looks like:** a table of at least three bugs with all four columns filled in, plus a working file that turns `37` into `98.6`.

### 6. [Stretch] The rounding investigation

Run this in the interactive shell:

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(f"{0.1 + 0.2:.2f}")
```

You will get a surprising second line. Write `rounding.py` that:

- reproduces all three results,
- prints `0.1 + 0.2` to 20 decimal places using `{value:.20f}`,
- and contains a 4-sentence comment explaining, in your own words, why a computer that stores numbers in binary cannot store `0.1` exactly (hint: think about how you cannot write 1/3 exactly in decimal — 0.3333... never ends).
- Finally, show a *safe* way to compare: print `abs((0.1 + 0.2) - 0.3) < 0.000001`.

**Done looks like:** the file runs, and your explanation uses the 1/3 analogy without copying the wording above.

---

## 🤔 Think Deeper

### 1. Python refuses to guess what `"5" + 5` means. Other languages (like JavaScript) happily return `"55"`. Which behaviour is better, and does the answer change depending on what the program is for?

*How to reason about it:* Think about two very different programs — a quick script you'll run once to count lines in a file, and the software that computes a hospital's medicine dosages. For each, ask: what is the cost of the program **stopping** versus the cost of it **quietly producing a wrong answer**? Notice that "better" is not a property of the language alone; it's a property of the language *plus the stakes*.

### 2. Every variable name you choose is a tiny act of communication. Is there such a thing as a *dishonest* variable name, and could one cause real harm?

*How to reason about it:* Imagine a program that assigns each student a number and stores it in a variable called `risk_score`. Now imagine the same number stored in `attendance_gap_days`. Same number, same maths — but which one will a teacher trust more, and which one invites a decision it wasn't built for? Look for names that *imply a meaning the data does not actually carry*. Then ask who is harmed when the reader believes the name over the data.

### 3. `input()` always returns a string, and you have to remember to convert. Should Python just be smart and give you a number when the user types digits?

*How to reason about it:* Play out the edge cases. What should `input()` return if the user types `007` (a jersey number, or seven?), `1,240` (a bill with a comma), `+91 9876543210` (a phone number), or `2024-01-15`? For each, decide what a "smart" system should do, and notice how quickly the smart rules start contradicting each other. Then ask: who does the current dumb-but-predictable rule protect?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `age = input("Age? ")` then `age + 1` → `TypeError` | You *see* a number on screen and forget `input()` hands back text | Convert at the moment of input: `age = int(input("Age? "))` |
| `print("Hi {name}")` prints the braces literally | Forgot the `f` before the opening quote | `print(f"Hi {name}")` — the `f` is what activates the braces |
| `NameError: name 'totl' is not defined` | Typo, or you assigned it *after* you used it | Read the name in the error, search your file for it, check spelling and order. Python runs top to bottom — a variable must be assigned on an earlier line |
| `int("3.5")` → `ValueError` | You assume `int()` can handle any number-ish text | `int()` only accepts whole numbers written as text. Use `float("3.5")`, or `int(float("3.5"))` if you truly want `3` |
| `int(3.9)` gives `3` and you expected `4` | Assuming `int()` rounds | `int()` truncates. Use `round(3.9)` to round |
| `SyntaxError` pointing at a line that looks perfect | An unclosed `(` or `"` on the line **above** — Python keeps reading until it fails | Always check the previous line first when a `SyntaxError` makes no sense |
| Writing `5 = x` instead of `x = 5` | Reading `=` as "equals" instead of "gets" | The name always goes on the **left**. `=` means "put the right side into the left name" |
| Saving your file as `hello.py.txt` | Editor added an extension you can't see | In VS Code check the tab title, or run `ls` in the terminal to see the real filename |
| Naming a file `random.py` or `math.py` | Seems like a sensible name | Those clash with Python's own built-in modules and cause bizarre errors later. Prefix yours: `my_math.py` |

---

## 🛠️ Mini-Project: About-Me Bot

**Time: 60–90 minutes**

### Goal

Write a single program, `about_me.py`, that interviews the user with **six questions**, converts the numeric answers to the right types, computes **two derived numbers** the user did not type, and prints a formatted profile card.

### Starter steps

**Step 1 — Plan on paper first.** Before writing any code, write down your six questions and, for each one, the type you need:

| # | Question | Raw type from `input()` | Type you need | Conversion |
|---|---|---|---|---|
| 1 | Your name? | `str` | `str` | none |
| 2 | Your city? | `str` | `str` | none |
| 3 | Your age in years? | `str` | `int` | `int(...)` |
| 4 | Your height in metres? | `str` | `float` | `float(...)` |
| 5 | Screen time per day (hours)? | `str` | `float` | `float(...)` |
| 6 | Favourite number? | `str` | `int` | `int(...)` |

At least one question **must** accept a decimal — that's the `float` requirement.

**Step 2 — Choose your two derived numbers.** These must be things the user did *not* type. Pick two:

- age in days: `age * 365`
- minutes of screen time per year: `screen_hours * 60 * 365`
- days of your life spent on a screen so far: `screen_hours * 365 * age / 24`
- your height in feet: `height_m * 3.28084`
- what percentage of a 90-year life you've used: `age / 90`

**Step 3 — Write the skeleton with comments only.** Literally type the comments before the code:

```python
# about_me.py — interviews the user and prints a profile card.

# --- 1. Collect the six answers -------------------------------

# --- 2. Compute the derived numbers ---------------------------

# --- 3. Print the card ----------------------------------------
```

**Step 4 — Fill in section 1**, one line at a time, running the program after every two lines. Do not write all 20 lines then run. Run early, run often.

**Step 5 — Fill in section 2.** Print each derived value on its own plain line first to check the arithmetic. Do the maths on paper for your own answers and compare.

**Step 6 — Fill in section 3.** Make it pretty. Use `"=" * 44` for divider lines, `:>10` to right-align, `:,.0f` for big numbers with commas, `:.1f` for one decimal.

**Step 7 — Comment every line.** The success criteria demand it. Explain *why*, not *what*.

### A reference implementation

Use this only if you're stuck for more than 15 minutes — try yours first.

```python
# about_me.py — interviews the user and prints a formatted profile card.
# Every input() returns text, so numeric answers are converted immediately.

WIDTH = 44                      # card width in characters; one place to change the look
LIFESPAN = 90                   # assumed lifespan in years, used for the % calculation

print("=" * WIDTH)              # top border: "=" repeated 44 times
print("  ABOUT-ME BOT · answer 6 quick questions")
print("=" * WIDTH)

# --- 1. Collect the six answers -------------------------------------------
name = input("1. What is your name?              ")          # text, no conversion
city = input("2. Which city do you live in?      ")          # text, no conversion
age = int(input("3. How old are you (years)?        "))      # whole number -> int
height_m = float(input("4. How tall are you (metres)?      "))  # decimal   -> float
screen_h = float(input("5. Screen hours per day?           "))  # decimal   -> float
fav = int(input("6. Your favourite whole number?    "))      # whole number -> int

# --- 2. Compute the derived numbers ---------------------------------------
age_days = age * 365                     # rough age in days (ignores leap years)
screen_min_year = screen_h * 60 * 365    # minutes of screen time in one year
height_ft = height_m * 3.28084           # metres -> feet, for a second unit
life_used = age / LIFESPAN               # fraction of an assumed 90-year life
fav_cubed = fav ** 3                     # a little arithmetic on the fun answer

# --- 3. Print the card ----------------------------------------------------
print()                                              # a blank line for breathing room
print("=" * WIDTH)
print("  PROFILE CARD".ljust(WIDTH))                 # ljust pads the text out to WIDTH
print("=" * WIDTH)
print(f"  Name         : {name}")
print(f"  City         : {city}")
print(f"  Age          : {age} years")
print(f"  Height       : {height_m:.2f} m  ({height_ft:.1f} ft)")
print("-" * WIDTH)
print("  THINGS YOU DIDN'T TELL ME:")
print(f"  You have been alive about {age_days:,} days.")
print(f"  You spend {screen_min_year:,.0f} minutes a year on screens.")
print(f"  That is {screen_min_year / 60 / 24:.1f} full days of screen per year.")
print(f"  You have used {life_used:.1%} of a {LIFESPAN}-year life.")
print(f"  Your favourite number cubed is {fav_cubed:,}.")
print("=" * WIDTH)
```

Example run:

```
============================================
  ABOUT-ME BOT · answer 6 quick questions
============================================
1. What is your name?              Ramana
2. Which city do you live in?      Bengaluru
3. How old are you (years)?        12
4. How tall are you (metres)?      1.52
5. Screen hours per day?           2.5
6. Your favourite whole number?    7

============================================
  PROFILE CARD
============================================
  Name         : Ramana
  City         : Bengaluru
  Age          : 12 years
  Height       : 1.52 m  (5.0 ft)
--------------------------------------------
  THINGS YOU DIDN'T TELL ME:
  You have been alive about 4,380 days.
  You spend 54,750 minutes a year on screens.
  That is 38.0 full days of screen per year.
  You have used 13.3% of a 90-year life.
  Your favourite number cubed is 343.
============================================
```

Check the arithmetic by hand: 12 × 365 = 4,380 ✔. 2.5 × 60 = 150 minutes/day, × 365 = 54,750 ✔. 54,750 ÷ 60 = 912.5 hours ÷ 24 = 38.02 days ✔. 12 ÷ 90 = 0.1333 = 13.3% ✔. 7³ = 343 ✔.

### Success criteria checklist

- [ ] Runs from the terminal with `python3 about_me.py` with no traceback
- [ ] Asks exactly six questions
- [ ] At least one question accepts a decimal, and the program handles `2.5` correctly
- [ ] At least two printed numbers are **derived** — never typed by the user
- [ ] Every single line of code has a comment explaining *why* it exists
- [ ] Uses f-strings everywhere (no `+` string joining)
- [ ] At least one number formatted with `:,` and one with `:.1f` or `:.2f`
- [ ] The card has visible top, middle, and bottom borders
- [ ] You verified every derived number by hand on paper

### 🚀 Level it up

**Extension:** add a "twin finder" section. Ask the user for a **birth year** as a 7th question and compute:

- what day-of-the-week-ish age bracket they're in (`age // 5 * 5` gives a 5-year bracket: 12 → 10)
- how many days until their next birthday if their birthday is on day 200 of the year and today is day 245 — you'll need `%` to wrap around 365
- a "screen time equivalent": how many 3-hour movies their yearly screen time equals (`screen_min_year / 60 / 3`)

Bonus challenge: make the card width a single variable at the top, then change it from 44 to 60 and confirm **every** border resizes without you editing more than one line. If you have to edit two lines, you've hard-coded something you shouldn't have.

---

## 🔑 Key Takeaways

- **Python runs top to bottom, literally.** It does exactly what you wrote, in the order you wrote it — never what you meant.
- **`=` means "gets", not "equals".** The name on the left receives whatever the right side evaluates to.
- **Every value has a type, and the type decides what operations mean.** `+` adds numbers and joins strings; mixing them is an error on purpose.
- **`input()` always returns a `str`.** Convert with `int()` or `float()` at the moment you read it, not three lines later.
- **f-strings are how you print.** `f"...{value:.2f}..."` — the `f` activates the braces, and the `:` starts a format spec.
- **A traceback is a gift, not a scolding.** Read the last line for *what*, the line number for *where*, then fix one thing and re-run.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Interpreter** | The program that reads your Python file and does what it says | Running `python3 hello.py` starts the interpreter on your file |
| **Script / `.py` file** | A saved list of instructions you can re-run any time | `about_me.py` |
| **Function** | A named action you can run by writing its name and `()` | `print("hi")`, `int("5")`, `type(3.5)` |
| **Variable** | A label attached to a value so you can reuse it | `score = 47` |
| **Assignment** | Putting a value into a name, using `=` | `total = pizzas * price` |
| **Comment** | A note for humans that Python ignores | `# convert to minutes` |
| **Type** | The category of a value, deciding what you can do with it | `int`, `float`, `str`, `bool` |
| **`str` (string)** | Text, always inside quotes | `"Bengaluru"` |
| **`int` (integer)** | A whole number, no decimal point | `47` |
| **`float`** | A number with a decimal point | `3.2` |
| **`bool` (boolean)** | Exactly `True` or `False`, nothing else | `is_captain = False` |
| **Concatenation** | Joining two strings end to end with `+` | `"pi" + "zza"` → `"pizza"` |
| **Type conversion (cast)** | Turning one type into another on purpose | `int("12")` → `12` |
| **f-string** | A string with an `f` in front, where `{}` gets filled in with values | `f"Score: {runs}"` |
| **Format spec** | The bit after `:` inside braces that controls how a number looks | `{x:.2f}`, `{n:,}`, `{p:.1%}` |
| **Traceback** | The report Python prints when it gives up, saying where and why | `NameError: name 'nme' is not defined` |
| **`SyntaxError`** | "That isn't valid Python" — usually a missing bracket or quote | `print("hi"` |
| **`NameError`** | "I've never heard of that name" — usually a typo | using `totl` when you defined `total` |
| **`TypeError`** | "Those kinds of things don't go together" | `"5" + 5` |
| **`ValueError`** | "Right kind of thing, but I can't use that value" | `int("twelve")` |
| **Modulo (`%`)** | The remainder after division | `7 % 2` → `1` |
| **Floor division (`//`)** | Division that throws away the fraction | `7 // 2` → `3` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### Practice 1 — Name that type

```python
# type_quiz.py — guess first, then check.

# guess: int
print(42, type(42))                # <class 'int'>

# guess: float  (the .0 makes it a float even though the value is whole)
print(42.0, type(42.0))            # <class 'float'>

# guess: str    (quotes = text, always)
print("42", type("42"))            # <class 'str'>

# guess: bool
print(True, type(True))            # <class 'bool'>

# guess: int    (int + int stays int)
print(4 + 2, type(4 + 2))          # 6 <class 'int'>

# guess: float  (/ ALWAYS produces a float, even 4/2)
print(4 / 2, type(4 / 2))          # 2.0 <class 'float'>

# guess: str    (string * int repeats the string)
print("4" * 2, type("4" * 2))      # 44 <class 'str'>

# guess: bool   (a comparison always produces True or False)
print(42 > 40, type(42 > 40))      # True <class 'bool'>
```

Full output:

```
42 <class 'int'>
42.0 <class 'float'>
42 <class 'str'>
True <class 'bool'>
6 <class 'int'>
2.0 <class 'float'>
44 <class 'str'>
True <class 'bool'>
```

**The two that catch almost everyone:** `4 / 2` is `2.0` (a float, not an int) and `"4" * 2` is `"44"` (a string, not 8). If you got 6 or more right, you're in good shape.

---

### Practice 2 — Rectangle report

```python
# rectangle.py — area and perimeter from two variables.

length = 12.5                          # metres
width = 4                              # metres (an int; mixing with a float is fine)

area = length * width                  # 12.5 * 4 = 50.0
perimeter = 2 * (length + width)       # 2 * 16.5 = 33.0

print(f"Length {length} m, width {width} m")
print(f"Area: {area:.2f} square metres")
print(f"Perimeter: {perimeter:.2f} metres")
```

Output:

```
Length 12.5 m, width 4 m
Area: 50.00 square metres
Perimeter: 33.00 metres
```

By hand: 12.5 × 4 = 50 ✔. 12.5 + 4 = 16.5, × 2 = 33 ✔.

Note that `{area}` alone would print `50.0` — one decimal place, not two. The `:.2f` is what forces `50.00`.

---

### Practice 3 — Seconds decoder

```python
# seconds.py — convert a total number of seconds to h/m/s.

total = int(input("Seconds: "))        # whole number of seconds

hours = total // 3600                  # how many whole hours fit
remainder = total % 3600               # seconds left over after the hours
minutes = remainder // 60              # whole minutes in what's left
seconds = remainder % 60               # final leftover seconds

print(f"{total} seconds = {hours} h {minutes} m {seconds} s")

# Expected outputs, checked by hand:
# 7325  -> 7325 // 3600 = 2, rem 125; 125 // 60 = 2, rem 5   -> "2 h 2 m 5 s"
# 59    -> 59 // 3600 = 0,  rem 59;   59 // 60  = 0, rem 59  -> "0 h 0 m 59 s"
# 3600  -> 3600 // 3600 = 1, rem 0;   0 // 60   = 0, rem 0   -> "1 h 0 m 0 s"
# 86399 -> 86399 // 3600 = 23, rem 3599; 3599//60 = 59, rem 59 -> "23 h 59 m 59 s"
```

Four verification runs:

```
Seconds: 7325
7325 seconds = 2 h 2 m 5 s

Seconds: 59
59 seconds = 0 h 0 m 59 s

Seconds: 3600
3600 seconds = 1 h 0 m 0 s

Seconds: 86399
86399 seconds = 23 h 59 m 59 s
```

**Why 86399 is the good test case:** it is one second short of a full day, so it catches an off-by-one anywhere in the chain. 23 × 3600 = 82,800. 86,399 − 82,800 = 3,599. 59 × 60 = 3,540. 3,599 − 3,540 = 59. ✔

**Common wrong approach:** computing `minutes = total // 60` (which gives 122 for 7325, not 2). You must take the remainder *after* removing the hours.

---

### Practice 4 — Study-time cost calculator

```python
# study_cost.py — how much a term of tutoring actually costs.

WIDTH = 40                                           # card width, one place to change it

print("Enter your study plan:")

hours_day = float(input("  Hours per day  : "))      # decimal allowed -> float
days_week = int(input("  Days per week  : "))        # whole number    -> int
weeks = int(input("  Weeks in term  : "))            # whole number    -> int
rate = float(input("  Tutor rate/hr  : "))           # rupees per hour -> float

total_hours = hours_day * days_week * weeks          # 2.5 * 5 * 14 = 175.0
total_cost = total_hours * rate                      # 175 * 500    = 87500.0
cost_per_week = total_cost / weeks                   # 87500 / 14   = 6250.0

print("=" * WIDTH)
print("  STUDY PLAN")
print("=" * WIDTH)
print(f"  Hours/day    : {hours_day}")
print(f"  Days/week    : {days_week}")
print(f"  Weeks        : {weeks}")
print("  " + "-" * (WIDTH - 4))
print(f"  Total hours  : {total_hours}")
print(f"  Tutor cost   : {total_cost:,.0f}")
print(f"  Cost/week    : {cost_per_week:,.0f}")
print("=" * WIDTH)
```

Run with `2.5`, `5`, `14`, `500`:

```
Enter your study plan:
  Hours per day  : 2.5
  Days per week  : 5
  Weeks in term  : 14
  Tutor rate/hr  : 500
========================================
  STUDY PLAN
========================================
  Hours/day    : 2.5
  Days/week    : 5
  Weeks        : 14
  ------------------------------------
  Total hours  : 175.0
  Tutor cost   : 87,500
  Cost/week    : 6,250
========================================
```

By hand: 2.5 × 5 = 12.5 hours/week. × 14 weeks = 175 hours ✔. 175 × 500 = 87,500 ✔. 87,500 ÷ 14 = 6,250 ✔.

**Why `:,.0f` and not `:,`?** Because `total_cost` is a `float` (`87500.0`), and `{87500.0:,}` prints `87,500.0` with a trailing `.0`. The `.0f` chops the decimals off. Try both and see.

---

### Practice 5 — Traceback triage

**The bug table:**

| # | Error type | Reported line | Plain English | Fix |
|---|---|---|---|---|
| 1 | `TypeError` | 2 | `temperature_c` is a string from `input()`, and you can't multiply a string by 9 and then divide it | `temperature_c = float(input("Temp in C: "))` |
| 2 | `TypeError` | 3 | You tried to join text with `+` to a `float`; `+` won't mix types | Use an f-string: `print(f"That is {temperature_f} degrees F")` |
| 3 | `NameError` | 4 | `tempature_f` is a misspelling of `temperature_f` | Fix the spelling |
| 4 | *(not an error)* | 3 | `98.60000000000001` looks unprofessional | Format it: `{temperature_f:.1f}` |

Note that bugs 2 and 3 only *appear* after you fix bug 1 — Python stops at the first failure, so you find bugs one at a time. That's normal.

Actually, bug 2 is subtle: `"That is " + temperature_f` where `temperature_f` is a float gives:

```
TypeError: can only concatenate str (not "float") to str
```

Fixed file:

```python
# temperature.py — Celsius to Fahrenheit, fixed.

temperature_c = float(input("Temp in C: "))          # convert text -> number
temperature_f = temperature_c * 9 / 5 + 32           # 37 * 9 = 333, /5 = 66.6, +32 = 98.6
print(f"That is {temperature_f:.1f} degrees F")      # f-string, one decimal place
```

Run:

```
Temp in C: 37
That is 98.6 degrees F
```

By hand: 37 × 9 = 333. 333 ÷ 5 = 66.6. 66.6 + 32 = 98.6 ✔

---

### Practice 6 — The rounding investigation

```python
# rounding.py — why 0.1 + 0.2 is not 0.3.

print(0.1 + 0.2)                       # 0.30000000000000004
print(0.1 + 0.2 == 0.3)                # False  (!!)
print(f"{0.1 + 0.2:.2f}")              # 0.30   (formatting hides the problem)

print(f"{0.1 + 0.2:.20f}")             # 0.30000000000000004441
print(f"{0.1:.20f}")                   # 0.10000000000000000555
print(f"{0.2:.20f}")                   # 0.20000000000000001110

# WHY THIS HAPPENS:
# In decimal, one third cannot be written down exactly - 0.3333... never ends,
# so if you only have room for 16 digits you have to stop somewhere and be
# slightly wrong. A computer has the same problem, but in binary (base 2), and
# the fractions that don't fit are different ones: 1/10 is one of them.
# So 0.1 is stored as the closest binary number available, which is a hair too
# big, and when you add two hairs-too-big numbers the error becomes visible.

# THE SAFE WAY TO COMPARE two floats: ask if they are CLOSE, not EQUAL.
print(abs((0.1 + 0.2) - 0.3) < 0.000001)     # True
```

Output:

```
0.30000000000000004
False
0.30
0.30000000000000004441
0.10000000000000000555
0.20000000000000001110
True
```

**The rule to carry forever:** never write `if some_float == some_other_float`. Always write `if abs(a - b) < tiny_number`. You'll use this again in Level 2 Module 5 when comparing arrays, and in Level 3 when checking whether a model's loss has stopped changing.

**Why `abs()`?** Because `(0.1 + 0.2) - 0.3` might be a tiny positive number *or* a tiny negative number depending on rounding. `abs()` gives the distance regardless of direction: `abs(-0.0000001)` is `0.0000001`.

</details>

---

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 2 Home](README.md) · [Next ➡](module-02-decisions-and-loops.md)
