# Week 10 — Functions That Take Something and Give Something Back

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one new idea (a function can take things in and hand one thing back) applied five times, then broken on purpose |
| **Big idea** | A parameter is a box the function fills from whoever called it, and `return` is the only way a value gets back out. |
| **New vocabulary** | parameter · argument · default value · scope · `None` |
| **New syntax** | `def f(a, b):` · `def f(a, b=0):` · `f(b=3)` · `None` |
| **Materials** | Printed workbook pages 10.1–10.6 · the student's notebook, open at the Bug Log · pencil · **four index cards and a marker pen** for the Hook · a calculator |
| **Tech needed** | Python 3, an editor, one terminal. **No libraries at all this week** — nothing to install, nothing to import. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the whole week hinges on one word — `print` versus `return`. Do not let the lesson become "five more functions". It is "five more functions **that hand something back**", and the planted bug at minute 55 is the part they will remember in June.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Write a function with two parameters** and call it with two arguments, in the right order.
2. **Say out loud, correctly, the difference between a parameter and an argument** — the name in the definition, the value at the call.
3. **Give a parameter a default value** and explain when the default gets used and when it does not.
4. **Explain why a variable created inside a function does not exist outside it**, using the word *scope*.
5. **Find a function that prints the right answer but returns `None`**, diagnose it by printing what came back, and fix it.

Observable evidence: a file with five working functions, a test line for each showing three inputs, and a Bug Log entry containing a real `TypeError` traceback with the one-word fix written next to it.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to have programmed before to teach this.** Everything below is written for an adult who has never written a line of code, and it is written in the order you will need it. Read it once, then do the Prep Checklist. About 25 minutes.

### 1. What Week 9 gave them, and the one hole in it

In Week 9 the student learned to name a block of code. `def print_banner():` writes the recipe; `print_banner()` cooks it. Two separate acts, and telling them apart is most of Week 9:

```
   DEFINING                            CALLING
   def print_banner():                 print_banner()
   "Here is a recipe."                 "Cook it, now."
   Nothing runs. You do it once.       The body runs. As often as you like.
```

**A function you define and never call does nothing at all.** That is not a bug; it is the point. If a student runs a file and gets no output whatsoever, the first question is always "did you call it?"

Week 9 also introduced `return value`. But every Week 9 function did the *same thing every time*. `print_banner()` prints twenty equals signs and that is all it will ever do; it cannot print thirty, because there is nowhere to *tell* it thirty.

**That is the hole this week fills.** A function becomes genuinely useful the moment the caller can hand it different values each time.

### 2. Parameter and argument — two words for the two halves

Here is the whole idea in six lines:

```python
def double(number):                 # `number` is the PARAMETER
    return number * 2               # the body uses it like any other variable

print(double(6))                    # 6 is the ARGUMENT
print(double(0))
print(double(-3))
```

```text
12
0
-6
```

> **Parameter** — the *name* you write inside the brackets of the definition. It is an empty box with a label on it.
>
> **Argument** — the *value* you write inside the brackets when you call it. It is what goes in the box.

The two words describe the same box at two different moments: empty when you wrote the definition, full when somebody calls it. **The memory hook that sticks:** **P**arameter is a **P**laceholder; **A**rgument is what you **A**ctually pass.

**Why the distinction matters, and it genuinely does:** the parameter name is *private to the function*. Write `pizza_price = 6` and then `double(pizza_price)`, and the function has never heard of `pizza_price` — it only knows that something arrived and that in here it is called `number`. That is exactly why one function works on a pizza price, a step count and a cricket score. **Rename `number` to `n` and every caller still works**, because callers do not know or care what the box is labelled.

![A parameter is an empty box. The caller fills it.](../figures/fig-w10-1-parameter-boxes-filled-by-caller.svg)
*Figure 10.1 — The names live in the definition. The values live at the call.*

### 3. Two parameters, and why order is the whole game

```python
def change_left(paid, cost):        # two parameters, comma between them
    return paid - cost              # one value goes back out

print(change_left(100, 65))         # paid 100, cost 65
print(change_left(100, 100))        # spent it all
print(change_left(50, 65))          # not enough money
print(change_left(65, 100))         # the SAME two numbers, swapped over
```

```text
35
0
-15
-35
```

Line by line, for somebody who has never programmed:

| Line | What Python does |
|---|---|
| `def change_left(paid, cost):` | Creates a recipe called `change_left`. It expects two values. It will call the first one `paid` and the second one `cost`. The colon means "the body starts on the next line, indented." |
| `    return paid - cost` | Four spaces of indent = this line is inside the recipe. Work out `paid` minus `cost`, then hand that number back to whoever asked, and stop. |
| `print(change_left(100, 65))` | Run the recipe with 100 in the first box and 65 in the second. Take whatever comes back — 35 — and print it. |

**Nothing checks that you got the order right.** `change_left(65, 100)` gives `-35`, which is a perfectly good number and completely wrong. Python cannot help you here, because both boxes take numbers. This is worth saying out loud: **the order of arguments is a promise you make and Python does not check.** Section 6 below is how you make that promise visible.

### 4. `print` versus `return` — the most important paragraph in this file

This is the idea that separates a student who can build things from a student who can only make things appear on screen. Take it slowly.

`print()` puts characters on the screen for a human to read. `return` hands a value **back into the program** so the program can use it.

Here is a function that prints:

```python
def add_scores(first, second):
    print(first + second)              # prints. Hands nothing back.

add_scores(2, 3)                       # 5 appears on screen. Looks perfect.
total = add_scores(2, 3)               # now try to KEEP the answer
print("total is:", total)
print(total * 2)                       # and now try to use it
```

```text
5
5
total is: None
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_bug.py", line 7, in <module>
    print(total * 2)                       # and now try to use it
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Read that output carefully, because it is the shape of the whole lesson.

- The first `5` came from `add_scores(2, 3)` on its own. **It worked.**
- The second `5` came from the same call on the `total = ...` line — the printing still happened.
- Then `total is: None`. The variable `total` got **nothing**.
- Then it crashed, because you cannot multiply nothing by 2.

Now the same function with **one word changed**:

```python
def add_scores(first, second):
    return first + second              # hands the answer back out

print(add_scores(2, 3))                # print it out here, at the edge
total = add_scores(2, 3)
print("total is:", total)
print(total * 2)
```

```text
5
total is: 5
10
```

> **🍕 The analogy to use, word for word:** *"A function that prints is a waiter who shouts your order across the restaurant. Everybody hears it. Nobody can eat it. A function that returns is a waiter who brings the plate to your table. Now you can eat it, share it, weigh it, take a photo of it."*

The rule that follows: **you can always print a returned value; you can never get a printed value back.** So return inside every function, and print once, at the very edge of the program where a human is actually reading.

![Printing shouts it. Returning hands it over.](../figures/fig-w10-2-print-vs-return.svg)
*Figure 10.2 — The 5 on the glass is gone. The 5 in your hand can be used.*

### 5. `None` — Python's word for "nothing at all"

> **`None`** — Python's word for "no value". A function that never reaches a `return` hands back `None`.

`None` is not zero and it is not an empty piece of text. Zero is a number you can add to. `None` is the absence of a value, and almost anything you try to do with it fails immediately — which, once you know the word, is extremely helpful, because the crash happens near the mistake instead of miles away.

The three tracebacks `None` produces, which you will see this week:

```text
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
TypeError: unsupported format string passed to NoneType.__format__
TypeError: object of type 'NoneType' has no len()
```

**Whenever you see the letters `NoneType` in a traceback, say this out loud: "something handed back nothing, and then we tried to use it."** Nine times out of ten in this course, that something is a function whose last line says `print` where it should say `return`.

### 6. Default values, and the one rule about their order

Sometimes a parameter has an obvious usual answer. A pizza has eight slices unless somebody says otherwise.

```python
def slice_cost(pizza_price, slices=8):     # slices has a DEFAULT of 8
    return pizza_price / slices           # rupees per slice

print(slice_cost(400))                    # no second argument -> uses 8
print(slice_cost(400, 4))                 # second argument given -> uses 4
print(slice_cost(400, 1))                 # one giant slice
print(slice_cost(400, slices=16))         # naming it: a KEYWORD ARGUMENT
print(slice_cost(pizza_price=400))        # you may name the first one too
```

```text
50.0
100.0
400.0
25.0
50.0
```

Check the arithmetic by hand: 400 ÷ 8 = 50 ✔ · 400 ÷ 4 = 100 ✔ · 400 ÷ 1 = 400 ✔ · 400 ÷ 16 = 25 ✔

> **Default value** — a value a parameter takes when the caller does not supply one.

The picture that makes it land: **the box is not empty. The definition already put an 8 in it.** If the caller hands over a value, it goes in and the 8 is never used. If the caller says nothing, the 8 is what the function works with.

![A default value is already sitting in the box](../figures/fig-w10-4-default-value-used.svg)
*Figure 10.3 — A default is not a rule. It is a sensible guess the caller may overrule.*

**The one rule: parameters with defaults must come after parameters without them.** Break it and Python refuses to even start the file:

```python
def slice_cost(slices=8, pizza_price):
    return pizza_price / slices
```

```text
  File "/Users/you/ai-academy/level2/week10_defaults.py", line 1
    def slice_cost(slices=8, pizza_price):
                             ^^^^^^^^^^^
SyntaxError: non-default argument follows default argument
```

The reason is worth knowing so you can answer "why?". If it were allowed, `slice_cost(400)` would be ambiguous — is 400 the slices or the price? Python removes the ambiguity by insisting the ones you *must* supply come first.

**Keyword arguments** (`slices=16` at the call) are the cure for the order problem in section 3. `change_left(paid=100, cost=65)` cannot be got the wrong way round, because you named the boxes. Teach it as "a way of showing your work", not as a separate topic.

### 7. Scope — same word, different rooms

> **Scope** — the part of a program where a particular name exists.

A variable created inside a function lives only inside it. When the function finishes, it is gone.

```python
def bus_fare(age):
    fare = 30                          # `fare` is made INSIDE bus_fare
    if age < 5:
        fare = 0
    elif age < 18:
        fare = 15
    elif age >= 60:
        fare = 10
    return fare                        # the VALUE gets out; the name does not

print(bus_fare(4))
print(bus_fare(12))
print(bus_fare(35))
print(bus_fare(60))
print(fare)                            # this line will fail
```

```text
0
15
30
10
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_scope.py", line 18, in <module>
    print(fare)                            # this line will fail
NameError: name 'fare' is not defined
```

Look at what did and did not happen. All four calls worked. The number 15 definitely existed. And the moment we asked for `fare` from outside, Python said it had never heard of it.

> **🍕 The analogy:** *a function is a kitchen with a serving hatch. Ingredients go in through the hatch. A finished plate comes out through the hatch. The mess inside — the half-chopped onions, the local variables — is invisible from the dining room and it gets cleared away when service ends.*

![A name made inside a function stays inside](../figures/fig-w10-3-scope-walls.svg)
*Figure 10.4 — Values travel through the hatch. Names do not.*

And the mirror image: the same word used inside and outside is **two different boxes**. Run `pocket_money = 200`, then a function whose body sets `pocket_money = 0` and prints it, then print `pocket_money` again outside:

```text
inside the function : 0
after the function   : 200
```

That is not Python being awkward. **It is the single feature that makes it safe to use a function somebody else wrote.** If a function could quietly rewrite your variables, you would have to read every line of every function before daring to call it. In Week 12 the student imports `stats.py`; in Week 29 they call `model.fit(...)`, thousands of lines written by strangers. Both are only survivable because a function takes inputs, gives an output, and changes nothing else.

### 8. The three misconceptions you will actually meet

**Misconception 1 — "It printed the right answer, so it works."** This is the big one and the reason for the planted bug. A printing function *looks* identical to a returning function when you test it on its own; the difference only shows up when you try to keep the answer. Do not explain it. Let the `TypeError` explain it, then have them fix it. The sentence to keep using all term: **"Showing me the answer is not the same as giving me the answer."**

**Misconception 2 — "The parameter and the argument have to have the same name."** Very common, from a reasonable instinct. Kill it with a demonstration: define `double(number)`, call it as `double(pizza_price)`, then as `double(7)`. Ask: "What is 7 called inside the function?" (Answer: `number`.)

**Misconception 3 — "A variable is a variable, so of course I can see it."** Do not argue. Run it. `NameError: name 'fare' is not defined` in their own terminal settles it in four seconds and no amount of explaining does.

And a fourth thing that is not a misconception but will happen: a student defines five beautiful functions, runs the file, gets **no output at all** — zero lines, no error, exit code 0 — and concludes Python is broken. **"You wrote the recipe and never cooked it."**

### 9. How deep to go, and where to stop

**Go this far:** parameters, arguments, two of them, order matters, one default value, one keyword argument at a call, `return` versus `print`, `None`, and a local variable dying at the end of the call.

**Stop before:**

- **`global`.** A student who wants to change an outer variable from inside a function will find this word on the internet. It works and it is a bad habit. Say: "That word exists and there's a better way — take the value in as a parameter and return the new one." Do not teach it.
- **Returning more than one value.** `return index, value` is legal and lovely. It needs tuples. Week 12's stretch, at the earliest.
- **Docstrings.** `"""Explain the function."""` is a good habit and a new construct on a week that already has four. `#` comments do the same job today. If they write one anyway, praise it and move on.
- **Mutable default arguments** (`def f(items=[])` has a famous trap) and **type hints** (`def double(number: int) -> int:`). Both are real; both are noise for a 12-year-old in week 10.

![One call, four steps, one value back](../figures/fig-w10-5-call-and-return-round-trip.svg)
*Figure 10.5 — Leave step 4 out and the caller gets `None`. That is the whole bug of this week.*

---

### 10. 🧭 The Growing Map — a new stage and a second thread

The student guide's **Where This Fits** figure shows the same pipeline every week with one more piece
filled in. Two things change on it this week, and both are worth naming out loud.

![The Level 2 pipeline in Week 10: stage one is finished and the first tile of stage two, functions and lists, is where you are](../figures/fig-w10-0-where-this-fits.svg)

*Figure 10.0 — Week 10's version. Stage one is complete: both tiles plain white, never re-tinted. The
gold badge has crossed into `HOLD THE DATA`, and the thread strip has two pills lit for the first time.*

**How to run it, in about two minutes:**

1. **Show it and ask:** *"your function took a number in and handed one back today — which box did that
   open?"* They point at the gold `functions · lists` tile in the second stage. Then point at the arrow
   they just crossed, and at the two white boxes behind it.
2. **Ask about the bottom strip:** *"there are two lit now — why?"* The honest answer is the one to
   give: Weeks 1–9 were craft, and deciding what a function's parameters are is the first genuinely AI
   idea of the year, because it is a decision about **how you represent a job**.
3. **Then the dashed question, and the copy.** Three stages and six tiles still dotted; they update
   their pencil map, and this week they get to fill in a new stage heading.

> **🧑‍🏫 Why this is worth two minutes.** Week 10 is the hinge of Level 2 and it is easy for it to pass
> unremarked, because `def double(number):` looks like a small edit to Week 9. The map is what makes the
> size of the change visible: new stage, new thread, and everything from here needs both.

> **⚠️ Watch out:** do not let the thread strip become a vocabulary test. "Representation" is a label on
> a thread they will meet twenty more times, not a word they need to define today.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print workbook pages 10.1–10.6.** Page 10.2 (the spec sheet) is the one that gets written on most — print it single-sided so there is room in the margin.
- [ ] **Write four index cards for the Hook.** One word per card, big:
      `PAID` · `COST` · `100` · `65`. Keep the two name cards separate from the two number cards.
- [ ] **Run this code yourself first.** Make a file called `week10_functions.py` in `~/ai-academy/level2` and type exactly this:

```python
# week10_functions.py
# Functions that take something in and give something back.

# ---- 1. One parameter: a box the caller fills ----
def double(number):                 # `number` is the PARAMETER
    return number * 2               # hand the answer back out

print(double(6))                    # 6 is the ARGUMENT
print(double(0))                    # awkward input: zero
print(double(-3))                   # awkward input: a negative

# ---- 2. Two parameters, in order ----
def change_left(paid, cost):        # two parameters, comma between them
    return paid - cost              # one value goes back out

print(change_left(100, 65))         # paid 100, cost 65
print(change_left(100, 100))        # spent it all
print(change_left(50, 65))          # awkward: not enough money

# ---- 3. Order matters ----
print(change_left(65, 100))         # the SAME two numbers, swapped over
```

Run it with `python3 week10_functions.py`. You must see **exactly** this:

```text
12
0
-6
35
0
-15
-35
```

- [ ] **Then break it on purpose, so you have seen the bug before they do.** Make `week10_bug.py`:

```python
# week10_bug.py
# THE PLANTED BUG. This function looks perfect. It is not.

def add_scores(first, second):
    print(first + second)              # <-- prints. Does NOT hand anything back.

add_scores(2, 3)                       # looks right: 5 appears on screen
add_scores(10, 40)                     # looks right again: 50 appears

total = add_scores(2, 3)               # now try to KEEP the answer
print("total is:", total)              # what is in total?
print(total * 2)                       # and now try to use it
```

You must see exactly this, ending in a crash:

```text
5
50
5
total is: None
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_bug.py", line 12, in <module>
    print(total * 2)                       # and now try to use it
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

*(Your file path will be your own folder. The path is never the interesting part.)*

- [ ] **Read section 4 above once more.** It is the section you will be asked "but why?" about.

### 5 minutes on the day

- [ ] Editor open, `week10_functions.py` **closed and unopened** — the student types it from blank.
- [ ] Terminal open, already `cd`-ed into `~/ai-academy/level2`, with the virtual environment activated if you use one. (Nothing this week needs it, but the habit is worth keeping.)
- [ ] Four index cards face-down on the table.
- [ ] Notebook open at the Bug Log page.
- [ ] Font size on the shared screen bumped up to about 18pt. Every argument this lesson is about a single character in brackets.

### Fallback if something fails

| If this fails | Do this instead |
|---|---|
| The laptop will not start, or Python will not run | **The whole lesson works on paper.** The Hook is already unplugged. For the Concept and the activity, the student writes the five functions on paper and *you* are the computer: they hand you a function and an argument, you read the body out loud and say what comes back. This is genuinely good — many teachers do it deliberately. Homework then becomes "type these five in and check my answers." |
| The editor loses the file / it will not save | Type into the terminal instead: run `python3` on its own to get the `>>>` prompt, and define functions there. Warn them the prompt forgets everything when it closes, so this is for today only. |
| The student has already read ahead and knows all of this | Skip to the planted bug at minute 40 and give them the harder version: three functions in one file, and only one of them has the missing `return`. Then hand them the extension in Differentiation → flying. |
| The student cannot get the four-space indent right and everything is an `IndentationError` | In VS Code, click the bottom bar where it says `Spaces: 4` → *Convert Indentation to Spaces*. Then never touch tabs again all year. Row 5 of the troubleshooting table in the orientation. |
| You are running short and it is minute 55 with no bug shown | Cut the fifth function (`bus_fare`). **Never** cut the planted bug. The bug is the lesson. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Two Cards and Two Numbers | 7 | 7 | A function is a form with blanks on it. You fill the blanks. |
| 🧠 Concept — Parameter, Argument, Return, None | 16 | 23 | The four words, with the concrete thing first every time |
| 💻 Live-Code Together — `week10_functions.py` | 18 | 41 | They type it. Two deliberate mistakes, fixed in front of them. |
| 🎲 Their Turn — Five From the Spec Sheet, Then the Bug | 20 | 61 | Build from a written spec; then diagnose the missing `return` |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the vocabulary, homework step one |

---

### 🪝 Hook — Two Cards and Two Numbers (7 minutes)

**Do this:** Lids down. Laptop closed. Put the two *name* cards face-up on the table, side by side, with a gap between them: `PAID` and `COST`. Keep `100` and `65` in your hand.

**Say this:**

> "Last week you learned to give a block of code a name. You wrote `print_banner()` and every time you called it, you got twenty equals signs. Always twenty. It could never give you thirty, because there was nowhere to *tell* it thirty.
>
> Today we fix that, and I want to do it with cards before we do it with a keyboard.
>
> Look at these two cards. These are not values. These are **labels on two empty boxes.** One is called PAID. One is called COST. That is all a function's brackets are — a little form with named blanks on it, waiting for somebody to fill them in.
>
> Here is the form: `change_left(paid, cost)`. And here is what it promises to do: it will tell me how much money I have left."

*(Now hold up `100` and `65`.)*

> "I went out with a hundred rupees and I spent sixty-five. Fill in my form. Which card goes on which box?"

Let them place the cards. They will get it right. Then:

> "Good. Now watch what happens if I do this."

*(Swap the two number cards over: `65` on PAID, `100` on COST.)*

> "Is that still a form I can fill in?"

Let them answer. Then, and this is the important beat:

> "Yes. It is. It's a perfectly legal form. Python will fill it in exactly like that, do the sum, and hand me back **minus thirty-five**, without one word of complaint. It will not say 'are you sure?' It will not underline anything in red.
>
> That is the first thing I want you to take away today. **The order of the values is a promise you make, and the computer does not check it.** A wrong answer that looks like an answer is much more dangerous than a crash, and it is the thing we spend the whole of the rest of this year learning to catch.
>
> Right. Two words, and then we go to the keyboard. The names on the boxes — PAID and COST — are called **parameters**. The values you put in them — 100 and 65 — are called **arguments**. Parameter, placeholder. Argument, what you actually pass."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which card goes on PAID?" | 100. | If they hesitate, read the sentence again slowly: "I *went out with* a hundred." The words in the story map onto the box names. |
| "If I swap them, does the computer complain?" | No. It gives −35 and thinks it did its job. | If they say "it would know it's wrong" — this is the belief to break today. Reply: "How? Both boxes take a number. It has no idea what money is." |
| "So whose job is it to get the order right?" | Mine. The person calling it. | If they say "the function's" — good instinct, wrong answer, and there *is* a way to make the function help. Say: "Hold that thought, we'll come back to it at minute 35." (That is keyword arguments.) |
| "What's the difference between a parameter and an argument?" | The parameter is the name in the definition; the argument is the value at the call. | Do not expect this yet. If they can only say "one's a box and one's a number", that is a pass for minute 7. |

---

### 🧠 Concept — Parameter, Argument, Return, None (16 minutes)

**Do this:** Lids still down. Notebook open. You are going to write four things in their notebook, and nothing else.

**Say this — part 1, the two words, on the board or on paper:**

> "Here is the smallest possible function that takes something in.
>
> ```
> def double(number):
>     return number * 2
> ```
>
> Two lines. Read the first one with me: 'define a function called double, that expects one thing, and inside the function that thing will be called number.' Read the second one: 'hand back number times two.'
>
> Now I call it: `double(6)`. What comes back?"

Wait for 12.

> "Right. Now here is the question that catches everybody. Inside the function, what is the 6 called?"

Let them think. The answer is `number`. If they say "6", say: "6 is what it *is*. What is it *called*?"

> "It's called `number`. The function doesn't know I typed 6. It doesn't know where 6 came from. It doesn't know that outside, I might have had that 6 in a variable called `pizza_price` or `cricket_score`. All it knows is: something arrived, and in here we call it `number`.
>
> And **that** is why one function can be used a thousand times. It never has to know anything about the outside world."

Write into the notebook, exactly these two lines:

> **Parameter** — the name in the definition. An empty box with a label.
> **Argument** — the value at the call. What goes in the box.

**Say this — part 2, `return` versus `print`, the heart of the lesson:**

> "Now the big one. Bigger than the last two put together.
>
> You already know `print`. `print` puts something on the screen so a human can read it. Today's word is `return`, and it does something different: it hands a value **back into your program** so the program can use it.
>
> Here's why that matters. Imagine you ask me to work out a total. Two ways I could answer.
>
> Way one: I stand up and **shout the answer across the room**. You heard it. Everybody heard it. But you can't do anything with it — you can't put it in your pocket, you can't add it to something else, you can't hand it to somebody at the next table.
>
> Way two: I write it on a piece of paper and **put the paper in your hand**. Now it's yours. Add it up. Fold it. Read it out loud if you want to — that's still your choice.
>
> `print` is shouting. `return` is putting it in your hand. And here is the rule that follows, which I want you to write down: **you can always print something that was returned. You can never get back something that was only printed.**"

Write into the notebook:

> **`return`** — hand one value back to whoever called the function.
> Rule: **return inside the function. print once, at the edge.**

**Say this — part 3, `None`:**

> "Last word, and it's the strangest one. What do you think happens if a function never returns anything at all? What comes back?
>
> Something does come back. Python always hands something back. If you never said `return`, what comes back is a special value that means *nothing at all*, and it is spelled with a capital N: `None`.
>
> `None` is not zero. Zero is a number — you can add three to zero. `None` is the *absence* of a value, and almost anything you try to do with it falls over immediately. Which sounds annoying and is actually a gift, because it means the crash happens right next to the mistake instead of three files away.
>
> So: any time you see the letters `NoneType` in an error message — and you will see them today — the sentence to say out loud is: **'something handed back nothing, and then I tried to use it.'**"

Write into the notebook:

> **`None`** — Python's word for "no value". What a function with no `return` hands back.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Inside `double`, what is the 6 called?" | `number`. | If they say "6", ask again with the emphasis: "What is it *called*?" If still stuck, point at the card labelled PAID from the Hook. |
| "Could I rename `number` to `n` and still call `double(6)`?" | Yes — nobody outside cares what the box is labelled. | If they say no, do it live in 10 seconds at minute 25 and let the run settle it. |
| "Why not just print inside the function? It's fewer lines." | Because then the answer is gone. You can't keep it or use it. | This is the correct question to be asked and you should be pleased. If they push, say: "Hold on to that — in twenty minutes I'm going to write a function that does exactly that, and I want you to break it." |
| "Is `None` the same as 0?" | No. 0 is a number you can do maths with. `None` is nothing. | If they say yes, promise a demonstration: `0 * 2` works, `None * 2` crashes. Do it at the keyboard in a moment. |
| "So how many things can a function hand back?" | One. | If they say "as many as you like" — technically there's a trick for that, and it is not this week. Say: "One, for now. There's a way round it and it's a few weeks off." |

---

### 💻 Live-Code Together — `week10_functions.py` (18 minutes)

**Do this:** Lids up. **The student types every single character. You never touch the keyboard.** You read each line aloud; they type it. Before every single Run, they say what they think will happen.

**Say this to start:**

> "New file. Call it `week10_functions.py` — with the underscores, and with `.py` on the end. Save it in the ai-academy folder before you type anything into it, because a file that isn't saved anywhere can't be run."

**The exact keystroke sequence.** Read out the words in bold; the student types the code.

**Step 1 (2 min).** "Two comment lines first, so future-you knows what this is."

```python
# week10_functions.py
# Functions that take something in and give something back.
```

**Step 2 (3 min).** *Add to the same file.* "Now our smallest function. Type `def`, space, `double`, open bracket, `number`, close bracket, **colon**. Then Enter — and notice the editor has moved you in four spaces on its own. That indent is Python's way of knowing what's inside the function."

```python
# ---- 1. One parameter: a box the caller fills ----
def double(number):                 # `number` is the PARAMETER
    return number * 2               # hand the answer back out
```

> **⚠️ Watch out:** after the `return` line they must press Enter **and then Backspace or Shift-Tab** to come back out to the left margin. If the next line stays indented, Python thinks it is still inside the function. This is the single most common thing that goes wrong in the next ten minutes.

**Step 3 (2 min).** *Add to the bottom of the same file.* "Three calls. Before you run: what three numbers are we about to see?"

```python
print(double(6))                    # 6 is the ARGUMENT
print(double(0))                    # awkward input: zero
print(double(-3))                   # awkward input: a negative
```

They predict 12, 0, −6. **Run it.**

```text
12
0
-6
```

> **💡 Try this:** point at the `-6` and ask "did we have to do anything special to make negative numbers work?" (No. The function never asked what kind of number it was.) That is a small, true, satisfying thing.

### ⛔ Deliberate mistake number one — the missing colon

**Do this, at about minute 8.** Say: "I want to show you something. Go up to the `def` line and delete the colon at the end. Just the colon. Then run it."

```python
def double(number)                 # `number` is the PARAMETER
    return number * 2               # hand the answer back out
```

```text
  File "/Users/you/ai-academy/level2/week10_functions.py", line 5
    def double(number)                 # `number` is the PARAMETER
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: expected ':'
```

**Say this:**

> "Read the last line out loud. — 'SyntaxError: expected colon.' That is Python being about as helpful as it ever gets. It has even drawn an arrow at the exact character where it wanted one.
>
> Notice something else: nothing ran at all. No 12, no 0, no minus 6. A SyntaxError means Python couldn't even read the file, let alone start doing what it said. That's actually the easiest kind of error to have.
>
> Put the colon back."

**Ask this:** "What's the difference between an error that stops everything before it starts, and an error halfway through?" *(Hoped-for: the second one means some of it worked. If they don't get there, say it yourself — they will need it in ten minutes when the planted bug prints a correct-looking 5 before it dies.)*

**Step 4 (4 min).** *Add to the bottom of the same file.* "Now two parameters. Same shape, comma in the middle."

```python
# ---- 2. Two parameters, in order ----
def change_left(paid, cost):        # two parameters, comma between them
    return paid - cost              # one value goes back out

print(change_left(100, 65))         # paid 100, cost 65
print(change_left(100, 100))        # spent it all
print(change_left(50, 65))          # awkward: not enough money
```

Predict, then **Run.**

```text
12
0
-6
35
0
-15
```

> **🧑‍🏫 If a student asks** *"why did it print the first three again?"* — "Because it runs the whole file, top to bottom, every time. Your old lines are still in there." This surprises people more than you would expect.

**Step 5 (2 min).** *Add to the bottom of the same file.* "And now the card trick from the beginning, in code."

```python
# ---- 3. Order matters ----
print(change_left(65, 100))         # the SAME two numbers, swapped over
```

**Run.** Last line reads `-35`.

**Say this:**

> "There it is. Minus thirty-five. No error. No warning. No red anything. Python filled the boxes in the order I gave them, did the subtraction, and handed me a confidently wrong answer.
>
> This is why we test our functions on three inputs instead of one, and this is why one of the three is always an awkward one."

### ⛔ Deliberate mistake number two — the one that matters

**Do this, at about minute 15.** Say: "One more thing before you take over. I'm going to make a change that looks harmless."

Have them scroll to `double` and change the `return` to a `print`, and add one line at the bottom:

```python
def double(number):
    print(number * 2)               # was: return number * 2

answer = double(6)
print("answer is:", answer)
```

Predict first — most students say `12` then `answer is: 12`. **Run.**

```text
12
answer is: None
```

**Say this, slowly:**

> "Look at that. The twelve is *there*. It printed. The function did the maths perfectly and it put the right answer on the screen.
>
> And `answer` is `None`. Nothing. The 12 went on the glass and the box came back empty.
>
> Change `print` back to `return` and run it again."

```text
12
answer is: 12
```

> "One word. That's the whole difference. And in a minute I'm going to give you a file where I've made that exact mistake on purpose and not told you where."

Have them save. Then the notebook: **one line in the Bug Log — "answer is: None → a function printed instead of returning. Fix: change `print` to `return`."**

---

### 🎲 Their Turn — Five From the Spec Sheet, Then the Bug (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–13:** workbook page 10.2. Build the five functions in `week10_toolkit.py`, testing each on three inputs before starting the next one. **One at a time, run after each.** A student who writes all five and then runs will get five errors at once and will not know which is which.
- **Minutes 13–20:** workbook page 10.4. Open `week10_broken.py`, find the missing `return`, and write down *why it looked correct*.

You should be almost silent for these twenty minutes. When they get stuck, use the escalation ladder from the orientation: point at the line number in the error, then ask what the last line says, then ask what they expected. Do not type.

---

## 🐞 The Debugging Clinic

Every one of these tracebacks came from actually running a broken version of this week's code. Your student will produce most of them today.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `SyntaxError: expected ':'` with an arrow under the closing bracket | Python could not read the line at all. Nothing ran. | The colon at the end of the `def` line is missing. | Put the colon after the closing bracket: `def double(number):` |
| `IndentationError: expected an indented block after function definition on line 1` | The `def` line promised a body and the next line was flush left. | The body was never indented, or the editor is mixing tabs and spaces. | Indent the body four spaces. If it looks indented already, it is tabs — VS Code bottom bar → *Convert Indentation to Spaces*. |
| `TypeError: change_left() missing 1 required positional argument: 'cost'` | You gave the function fewer values than it has boxes. | Called `change_left(100)` when it needs two. | Supply the second argument, or give `cost` a default in the definition. The message names the box it is still waiting for. |
| `TypeError: double() takes 1 positional argument but 2 were given` | You gave more values than there are boxes. | Called `double(6, 7)`. Often a stray comma, or two functions being confused. | Count the names in the definition and the values at the call. They must match. |
| `SyntaxError: non-default argument follows default argument` | The definition itself is illegal, so the file never starts. | Written `def slice_cost(slices=8, pizza_price):` — a default before a non-default. | Move every parameter with an `=` to the end: `def slice_cost(pizza_price, slices=8):` |
| `TypeError: slice_cost() got an unexpected keyword argument 'slice'` | You named a box that does not exist. | Typed `slice=4` when the parameter is `slices`. Singular/plural is the usual culprit. | Match the name in the definition exactly, character for character. |
| `TypeError: slice_cost() got multiple values for argument 'pizza_price'` | You filled the same box twice. | Wrote `slice_cost(400, pizza_price=500)`. The 400 already went into `pizza_price`. | Pick one way: either all by position or name the ones you mean. |
| `NameError: name 'fare' is not defined` | Python has never heard of that name *here*. | Using a variable outside the function that created it. (Or a plain typo.) | `return` the value out, and store it in a variable outside: `fare = bus_fare(12)`. |
| `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'` | You did maths on nothing. | A function printed instead of returning, so the caller got `None`. | Change that function's last line from `print(...)` to `return ...`. |
| `TypeError: unsupported format string passed to NoneType.__format__` | An f-string tried to format nothing. | Same cause: `f"Rs {amount:.2f}"` where `amount` came back as `None`. | Same fix. Find the function that fed it and give it a `return`. |
| `UnboundLocalError: local variable 'score_total' referenced before assignment` | Python decided the name was local *because you assign to it*, then found you read it first. | Doing `score_total = score_total + 1` inside a function, meaning the outer one. | Do not reach for `global`. Pass it in and return the new value: `def add_one(current): return current + 1`. |
| **No output at all. No error. Exit code 0.** | The file ran perfectly and was asked to do nothing. | Functions were defined and never called. | Add a call: `print(double(6))`. This is not an error, and that is why it confuses people. |

*(Wording note: `UnboundLocalError` reads slightly differently on Python 3.12 and later — "cannot access local variable ... where it is not associated with a value". Same error, same fix.)*

### How to teach debugging without giving the answer

You can see the missing colon from where you are standing. Do not type it. Do not point at it. Work down this ladder and stop the moment they take over:

1. **"Read the last line out loud."** Just that. Four seconds. This alone solves about a third of everything.
2. **"What kind of error is it?"** The word before the colon. `SyntaxError`, `NameError`, `TypeError`.
3. **"What does it say after the colon?"** The specific thing. `'cost'`. `expected ':'`.
4. **"Which line number?"** The last `File ..., line N` above the error.
5. **"Go and look at that line. Read it out to me."** Nine times in ten they spot it while reading it aloud.
6. **"What did you expect that line to do?"** This is the question that finds logic bugs, where there is no error message at all.
7. Only now: **"Compare your line 6 with mine."** And even then, let them find the difference.

**The specific move for this week's planted bug**, because there is no traceback pointing at the guilty function: teach them to *print what came back*.

```python
def weekly_saving(pocket_money, spent):
    print(pocket_money - spent)

came_back = weekly_saving(200, 145)
print("what came back was:", came_back)
print("its type is:", type(came_back))
```

```text
55
what came back was: None
its type is: <class 'NoneType'>
```

Two extra lines and the invisible becomes visible. **This is the most transferable skill in the week:** when you cannot see what a function gave you, catch it in a variable and print it.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** workbook page 10.2 (the spec sheet), page 10.3 (the test table), page 10.4 (the bug hunt), a pencil, a calculator, the notebook open at the Bug Log.

**On the screen:** a new empty file called `week10_toolkit.py`, and — not yet opened — `week10_broken.py`.

### Part 1 — The spec sheet (13 minutes)

The rule of the activity, said once and enforced: **write one function, test it on three inputs, run it, and only then start the next one.**

Here is the spec sheet exactly as it appears on workbook page 10.2. It says what each function must *do*, never how.

| # | Name | Takes | Gives back | Test on these three |
|---|---|---|---|---|
| 1 | `double` | one number | that number times two | `6` · `0` · `-3` |
| 2 | `change_left` | money paid, then the cost | how much is left | `(100, 65)` · `(100, 100)` · `(50, 65)` |
| 3 | `slice_cost` | the pizza price, and how many slices — **8 if not told** | the cost of one slice | `(400)` · `(400, 4)` · `(400, 1)` |
| 4 | `is_even` | one whole number | `True` if it divides by 2 exactly, else `False` | `10` · `7` · `0` |
| 5 | `bus_fare` | an age | the fare: free under 5, ₹15 under 18, ₹30 under 60, ₹10 for 60 and over | `4` · `12` · `60` |

**Why each third test is awkward, and why that matters.** Say this out loud when you hand the sheet over:

> "Look at the third test in every row. Zero. Spending exactly what you had. One slice. Zero again. And sixty exactly. Those aren't random. Every one of them sits on a boundary or is a number people forget about. **A function that works on 6 and 7 tells you almost nothing. A function that works on 0 and on the exact boundary tells you something real.**"

The finished file, which is also the answer key:

```python
# week10_toolkit.py — five tiny functions, built from the spec sheet.
# Every one of them RETURNS. Not one of them prints.

def double(number):
    # Give back the number multiplied by two.
    return number * 2

def change_left(paid, cost):
    # Give back how much money is left after paying.
    return paid - cost

def slice_cost(pizza_price, slices=8):
    # Give back the cost of one slice. A whole pizza is 8 slices unless told otherwise.
    return pizza_price / slices

def is_even(number):
    # Give back True if the number divides by 2 with nothing left over.
    return number % 2 == 0

def bus_fare(age):
    # Give back the fare in rupees for someone of this age.
    if age < 5:
        return 0                   # under 5 travels free
    elif age < 18:
        return 15                  # child fare
    elif age < 60:
        return 30                  # adult fare
    else:
        return 10                  # senior fare

# ---- three tests each, and one of the three is awkward on purpose ----
print("double        :", double(6), double(0), double(-3))
print("change_left   :", change_left(100, 65), change_left(100, 100), change_left(50, 65))
print("slice_cost    :", slice_cost(400), slice_cost(400, 4), slice_cost(400, 1))
print("is_even       :", is_even(10), is_even(7), is_even(0))
print("bus_fare      :", bus_fare(4), bus_fare(12), bus_fare(60))
```

```text
double        : 12 0 -6
change_left   : 35 0 -15
slice_cost    : 50.0 100.0 400.0
is_even       : True False True
bus_fare      : 0 15 10
```

### Part 2 — The bug hunt (7 minutes)

**Do this:** hand them `week10_broken.py` (workbook page 10.4 has it printed, and it should also be on the machine — you can type it in during prep in about ninety seconds). Say only this:

> "Three functions. Two of them are fine. One of them prints when it should return. Run it first. Then find it. Do not read the code looking for it — that is slow and you will miss it. Run it, read the last line, and follow the trail."

```python
# week10_broken.py — GIVEN TO YOU WITH A BUG IN IT.
# Three functions. Two are fine. One prints when it should return.
# Do NOT guess. Run it, read the last line, then find it.

def weekly_saving(pocket_money, spent):
    # Should give back how much is left over each week.
    print(pocket_money - spent)

def yearly_saving(weekly, weeks=52):
    # Should give back the saving for a whole year.
    return weekly * weeks

def rupees(amount):
    # Should give back the amount as a tidy piece of text.
    return f"Rs {amount:.2f}"

# ---- the report ----
left_each_week = weekly_saving(200, 145)
print("left each week:", rupees(left_each_week))
print("saved in a year:", rupees(yearly_saving(left_each_week)))
```

```text
55
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_broken.py", line 22, in <module>
    print("left each week:", rupees(left_each_week))
  File "/Users/you/ai-academy/level2/week10_broken.py", line 17, in rupees
    return f"Rs {amount:.2f}"
TypeError: unsupported format string passed to NoneType.__format__
```

This traceback is a small gift, and it is worth walking through with them:

- The **55 printed**, which is the right answer. So something worked.
- The last line says `NoneType`. So something handed back nothing.
- The bottom `File` line points at **line 17, inside `rupees`** — but `rupees` is innocent. It is only the place where the damage showed up.
- The `File` line **above** it says line 22 — that is who called it, and line 22 is where `left_each_week` gets used.
- Where did `left_each_week` come from? Line 21. `weekly_saving`. **That** is the guilty function.

The fix is one word, on line 7:

```python
def weekly_saving(pocket_money, spent):
    # Should give back how much is left over each week.
    return pocket_money - spent
```

```text
left each week: Rs 55.00
saved in a year: Rs 2860.00
```

Check by hand: 200 − 145 = 55 ✔ · 55 × 52 = 2,860 ✔

### What "finished" looks like

- Five functions in `week10_toolkit.py`, every one of them with `return` and none of them with `print` inside.
- Fifteen test results printed — three per function — and the awkward one in each row actually run, not skipped.
- `week10_broken.py` fixed, and its output showing `Rs 55.00` and `Rs 2860.00`.
- **A Bug Log entry** containing the real `NoneType.__format__` traceback, the one-word fix, and — this is the part that earns the marks — one sentence saying *why the bug looked correct*.

### Variation — easier

- **Three functions, not five.** Keep `double`, `change_left` and `slice_cost`. Those cover one parameter, two parameters and a default, which is the entire syntax of the week. Drop `is_even` (it needs `%` and returning a comparison) and `bus_fare` (it needs a whole `if/elif/else` chain inside a function).
- **Two tests each, not three** — but keep the awkward one. If you only run one test, run the awkward one.
- **Give them the first function typed out** and have them copy its shape. Copying a shape you can see is a real and respectable way to learn syntax.
- **Do the bug hunt together, out loud**, with them driving the keyboard and you asking the seven questions from the ladder above.
- **The one thing you must not cut:** the moment where a printing function gives back `None`. Everything else in this week is replaceable.

### Variation — harder

1. **Two bugs, not one.** Make a copy of `week10_broken.py` and also delete the `return` from `yearly_saving`. Now the first fix reveals the second, which is exactly what real debugging feels like.
2. **Make `change_left` refuse to be got wrong.** Challenge: "Call `change_left` in a way that cannot possibly be the wrong way round." *(Answer: `change_left(paid=100, cost=65)`. Keyword arguments at the call site.)* Then ask which is better and make them argue it.
3. **Design a default worth having.** "Add a default to `bus_fare` so that calling `bus_fare()` with nothing at all gives the adult fare." *(`def bus_fare(age=30):` — and then ask whether that is a *good* idea. It isn't, particularly: a fare with no age is a bit meaningless, and a default that hides a missing value is how bad data gets into real systems. That argument is worth five minutes.)*
4. **Break the default rule on purpose and read the error.** Have them write `def slice_cost(slices=8, pizza_price):` and produce the `SyntaxError` themselves, then explain in writing *why* Python forbids it. The reason — `slice_cost(400)` would be ambiguous — is a genuinely satisfying thing for a 12-year-old to work out.
5. **One function calling another.** Add `def slice_cost_rounded(pizza_price, slices=8): return round(slice_cost(pizza_price, slices), 2)`. It works, and it is the first time they see a function use a function they wrote. That is the shape of every program from here on.

---

## ❓ Questions Students Ask This Week

**"Why can't I just print inside the function? It's fewer lines and it works."**

It does work, right up until you want to *do* anything with the answer — add it to something, compare it, save it, put it in a sentence. The printed value is gone the instant it hits the screen; there is no way to get it back. And you lose nothing by returning, because the caller can always print it. The honest summary is: printing inside a function is not wrong, it is just a dead end, and you cannot tell it is a dead end from inside the function.

**"Does the argument have to have the same name as the parameter?"**

No, and it usually doesn't. The parameter name is the function's private label. You can call `double(pizza_price)`, or `double(7)`, or `double(scores_total)` — inside the function all three are called `number`. This is precisely what makes a function reusable: it does not need to know anything about the world outside it.

**"What if I want to give back two things?"**

You can, and there is a neat trick for it that we are not doing today. For now: one function, one answer. If you want two numbers, write two functions, or return the one that is actually the answer and let the caller work the other out. (The trick is `return a, b` and it needs an idea called a tuple; it turns up as a stretch task in a couple of weeks.)

**"Is `None` the same as zero, or the same as an empty message?"**

No, and this is worth getting straight. Zero is a number — you can add to it, multiply it, compare it. An empty piece of text is text — you can measure its length. `None` is the *absence* of a value; almost anything you try to do with it crashes immediately. That sounds unhelpful and is actually the point: it crashes near the mistake, so you can find the mistake.

**"If a function can see variables from outside it, why do we bother passing things in?"**

Because a function that reads whatever happens to be lying around outside it gives *different answers at different times*, depending on what ran before. You can never test it, because there is no such thing as "the input". A function that takes what it needs through its brackets gives the same answer for the same inputs, forever, no matter what else is going on. That property has a boring name — it is called being *pure* — and it is worth more debugging hours than anything else you will learn this year.

**"Is it ever OK for a function to print instead of return?"** *(Answer this one honestly: people who do this for a living genuinely disagree.)*

**Nobody fully agrees, and here is why it is not a dodge.** The strict position is that a function should compute and return, and printing should happen in exactly one place, at the edge of the program where a human is reading. That position is right often enough that we teach it as a rule, and every function in this course follows it.

But there are real, respectable exceptions. A function whose *entire job* is to display something — draw a chart, print a formatted report, write a table to the screen — has nothing to return, and forcing it to return would be silly. Real programs also print *while* they work, to say how far they have got; professionals call that logging, and there are whole libraries for doing it well, and people argue about those too. And there is a third camp who say the strict rule is fine for libraries and needless ceremony for a fifty-line script you will delete tomorrow.

What everybody does agree on is the half that matters this week: **a function that computes an answer must return it.** The disagreement is only about functions whose job is showing, not working out. So the honest version of the rule is: *if the function has an answer, return the answer.*

**"Why does Python make me put the colon and the indent? It knows what I mean."**

It really doesn't, and the indent is how it finds out. The four spaces are the only thing telling Python which lines are inside the function and which line is the first one after it. Other languages use curly brackets for this and end up with more punctuation; Python decided to use the layout you were going to write anyway. The colon is the signpost saying "an indented block starts here" — it appears before `if`, before `for`, before `while` and before `def`, always for the same reason.

**"What happens if I define two functions with the same name?"**

The second one wins, silently, and the first one is gone — no error, no warning. This is the same rule as putting a value in a box that already had something in it. It is worth trying once, because it will happen by accident when a file gets long, and the symptom (a function behaving like a completely different function) is baffling if you have never seen the cause.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The lesson becomes "write five functions" and the `return` point never lands | The functions are fun and the bug is at the end | Move the bug forward. Do the second deliberate mistake (`print` instead of `return` in `double`) at minute 15 as written, not at minute 25. If you are behind, cut the fifth function, never the bug. |
| The student writes all five functions and then runs, and gets a wall of errors | It feels efficient, and it is the opposite | Enforce one-at-a-time from the first function. Say it as a rule with a reason: "Five errors at once is five puzzles. One error at a time is one puzzle." If they have already done it, do not delete anything — comment out four functions and their tests, get one green, uncomment the next. |
| Everything is an `IndentationError` and morale collapses | The editor is inserting tabs, or Enter after `return` left them indented | Fix the setting once, at the machine level: VS Code bottom bar → `Spaces: 4` → *Convert Indentation to Spaces*. Then teach the reflex: after the last line of a function body, press Enter and then Backspace once. |
| The student "fixes" the missing-`return` bug by deleting the line that broke | The traceback pointed at line 22, so line 22 looks guilty | Ask one question: "If you delete that line, do you still get the answer you wanted?" Then walk the `File` lines from the bottom upward together. **The line that breaks is almost never the line that is wrong** — this is the most useful debugging idea of the term. |
| A student uses `global` (usually found on the internet) to get a value out of a function | It works, and it is the first thing a search suggests | Do not call it wrong, because it isn't. Say: "That works. There's a way that keeps working when your program gets big, and it's the one every function in this course uses — take the value in, hand the new one back." Then show `count = add_one(count)`. |
| The function has a default and the student puts it first | It reads better in English — "eight slices of a four-hundred-rupee pizza" | Let the `SyntaxError` do the teaching; it is unusually clear. Then give the reason, because they will ask: with a default first, `slice_cost(400)` could mean either box. |
| `slice_cost(400)` returns `50.0` and the student says the answer is wrong because of the `.0` | Dividing with `/` in Python always gives a decimal, even for exact answers | Two true things: `/` always produces a decimal, and that is deliberate; and `f"{cost:.2f}"` from Week 3 is how you control what a *reader* sees. The function should hand back the real number and let the caller decide how to show it. |
| The student cannot say the difference between parameter and argument, but the code all works | The words are much harder than the idea | Do not let it slide — objective 2 is the words. Use the index cards again: hold up `PAID` ("parameter — it's a name") and `100` ("argument — it's a value"). Then ask for it back in their own words at the wrap. |
| The file runs and prints nothing, and the student decides Python is broken | Functions defined, none called | Ask "how many times did you *call* one?" This is a good moment for the recipe line: writing the recipe is not cooking. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut** to three functions — `double`, `change_left`, `slice_cost` — and two tests each, keeping the awkward one. That is one parameter, two parameters and a default: the entire syntax of the week, in about twelve minutes.

**Reteach** with the cards, not with words. Lay out `PAID` and `COST`, and be the computer yourself. They hand you two number cards and say "change_left"; you say the answer out loud and put a written answer card in their hand. Then do it again but *shout* the answer instead of handing over the card, and refuse to give them the paper. The difference between shouting and handing over is the whole lesson, and it lands better as a physical joke than as an explanation.

**A copy-this-exactly scaffold.** Give them this on paper and let them fill in only the underlined parts. Copying a shape you can see is legitimate learning at this stage.

```python
def ________(________):
    # Give back ____________________
    return ________

print(________(____))       # test 1
print(________(____))       # test 2
print(________(____))       # test 3  <- the awkward one
```

**Reduce** the writing load: they may say their tests out loud while you type the `print` lines, as long as *they* type every `def` and every `return`. The typing that matters is the function itself.

**One thing you must not cut:** a printing function handing back `None`, seen with their own eyes on their own screen.

### If the student is flying

None of these needs any syntax beyond this week's four items.

1. **Two bugs in one file** (Variation — harder, item 1). Fixing one reveals the next. Then ask: "Which was easier to find, the first or the second? Why?"
2. **A function that calls a function.** `slice_cost_rounded(pizza_price, slices=8)` returning `round(slice_cost(pizza_price, slices), 2)`. Then the follow-up that makes it a real lesson: "What happens if you fix a bug in `slice_cost`? How many functions did you just fix?"
3. **Write the spec sheet for somebody else.** They invent five functions — name, what it takes, what it gives back, and three tests including one awkward one — and *you* implement them from their sheet alone, deliberately taking them literally. Every place you get it "wrong" is a place their spec was vague. This is the single best exercise in this week and it teaches precision better than any amount of correcting.
4. **The boundary hunt.** `bus_fare` has four bands, so it has three boundaries: 5, 18 and 60. Ask for a test table with **two rows per boundary** — the value itself and one below it. Six tests. Then: "Change `age < 18` to `age <= 18` and say exactly which of your six results changes." *(The 18-year-old moves from ₹30 to ₹15.)* Off-by-one on a boundary is the most common wrong answer in real software, and this is the cheapest possible place to meet it.
5. **Keyword arguments as documentation.** Rewrite all fifteen test calls using keyword arguments — `double(number=6)`, `change_left(paid=100, cost=65)`. Then the honest question: "That's much longer. When is it worth it?" *(When there are several parameters of the same type, or when a reader six months later would have to go and look up the order.)*

### If the student won't engage today

Do the Hook and the cards, properly, and nothing else.

Then play **Fill In My Form**, which delivers objectives 1 and 2 completely and takes about ten minutes. You say a function name and what it does; they tell you the parameters and give you the arguments for a case you describe.

> "`ticket_price` — it needs an age and whether it's a weekend." · "`journey_time` — distance and speed." · "`total_bill` — the price of one thing and how many you bought." · "`change_left` — I had ₹500 and bought three ₹90 books. How many arguments does that need? Is it two, or three?" *(Genuinely interesting: it depends on whether the function multiplies for you.)*

Then reverse it: you give them a function definition and they tell you the story. `def marks_lost(total, scored):` → "how many marks did I drop?"

Ten minutes, no keyboard, and both hard words used correctly a dozen times. The typing can be homework; the file will still be blank tomorrow.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the two words (spoken)**

> "I've written `def slice_cost(pizza_price, slices=8):` and then further down I've written `slice_cost(400, 4)`. Point at a parameter. Now point at an argument."

*Good answer:* parameter = `pizza_price` or `slices`; argument = `400` or `4`. Full marks needs one of each and no hesitation between them. **What to catch:** pointing at `8` and calling it an argument. It is a *default value* sitting in a parameter — a fair mistake, and worth one sentence of correction: "8 is what's already in the box. An argument is what the caller sends."

**Check 2 — the default (spoken)**

> "Same function. I call `slice_cost(400)`. How much does one slice cost, and where did the number of slices come from?"

*Good answer:* ₹50, and the 8 came from the definition because I didn't say. Both halves are needed. **What to catch:** an answer of 400 (ignored the default entirely) or "it would crash" (the commonest wrong answer, and the exact belief the figure exists to fix).

**Check 3 — the bug (written, one sentence)**

> "Write me one sentence. A friend's function prints the right answer every time she tests it, but when she writes `total = her_function(5)` and prints `total`, she gets `None`. What's wrong, and what should she change?"

*Good answer:* the function prints instead of returning, so nothing comes back; change `print` to `return` on its last line. **This is the check that separates level 3 from level 4.** If they can only say "it's broken", prompt once: "Where did the right answer go?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Can define a function with no parameters but not with one. Uses `print` inside every function and does not see the difference. Cannot say why a file with only `def`s produces no output. |
| **2 — Emerging** | Writes a one-parameter function when copying a shape. Sometimes says `return`, sometimes `print`, with no rule behind the choice. Uses "parameter" and "argument" interchangeably. Needs a prompt to spot the missing `return`. |
| **3 — Secure** | Writes a two-parameter function unaided and calls it correctly. Uses `return` by default. Says the parameter/argument difference correctly out loud. Gives a parameter a default value and says when it is used. Finds the missing-`return` bug from the traceback. **This is the target.** |
| **4 — Strong** | Explains scope in their own words and predicts a `NameError` before running. Diagnoses an unfamiliar `NoneType` traceback by printing what came back. Chooses keyword arguments when the order could be misread. Tests boundary values without being asked. |
| **5 — Exceptional** | Writes a function that calls another function they wrote, and can say why fixing the inner one fixes both. Argues both sides of "should a function ever print". Works out for themselves why a default parameter must come last. Writes a spec sheet precise enough that somebody else can implement it without asking a question. |

---

## 📤 Homework to Assign

**Say this:**

> "Two pages, about an hour, and the second one is the one I actually care about.
>
> **First, finish the spec sheet.** Pages 10.2 and 10.3. All five functions in `week10_toolkit.py`, every one of them returning, and every one tested on the three inputs on the sheet — including the awkward third one. Write the results into the table on page 10.3 **before** you run it, then run it and mark yourself. Getting a prediction wrong is more interesting than getting it right, so don't cheat by running first.
>
> **Second, the bug hunt.** Page 10.4. `week10_broken.py` has three functions in it and exactly one of them prints when it should return. Three things I want written down, in this order:
>
> One: the **real error message**, copied character for character into the Bug Log. Not a summary. The actual traceback.
>
> Two — and this is the marks — **one sentence saying why the bug looked correct.** Not "because I made a mistake". Something like: "it printed 55, and 55 was the right answer, so nothing looked wrong until the answer had to be used."
>
> Three: the fix, which is one word, and the output after fixing it.
>
> **Then page 10.5**, which is four predictions about scope. Write your answer down first. Then run them. Three of the four will surprise somebody, and I would quite like it to be you.
>
> Before you close the book tonight, page 10.6: this week's five words and four bits of syntax, in your own words. Not mine."

**Workbook pages:** 10.1 and 10.2 started in class; **10.2 finished, 10.3, 10.4, 10.5, 10.6** at home.

**Expected time:** 25 min for the five functions and the test table · 20 min for the bug hunt and the write-up · 10 min for the scope predictions · 5 min for vocabulary. **About 60 minutes.**

---

## 🔑 Answer Key

### Page 10.1 — Parameter or argument?

For each line, name what is underlined.

| # | The line | Underlined | Answer |
|---|---|---|---|
| a | `def double(number):` | `number` | **Parameter** — a name in the definition. |
| b | `print(double(6))` | `6` | **Argument** — a value at the call. |
| c | `def change_left(paid, cost):` | `cost` | **Parameter.** The second one. |
| d | `change_left(100, 65)` | `100` | **Argument.** It goes into `paid`, because it is first. |
| e | `def slice_cost(pizza_price, slices=8):` | `8` | **Neither, exactly — it is a default value.** It is what is already sitting in the parameter `slices`. Accept "part of the parameter" with the word *default* in the answer. |
| f | `slice_cost(400, slices=16)` | `slices=16` | **A keyword argument** — an argument that names the box it is going into. |
| g | `pizza_price = 400` then `slice_cost(pizza_price)` | `pizza_price` at the call | **Argument.** Confusingly it has the same name as the parameter, and that changes nothing at all — inside the function it is only ever called `pizza_price` because that is what the *definition* says. |

**10.1(h) In one sentence, what is the difference?**
The parameter is the name written in the definition; the argument is the value handed over when the function is called. Same box, two moments.

**10.1(i) Can a parameter and an argument have the same name?**
Yes, and it is common, and it means nothing special. They are still two different things: one is a label inside the function, the other is a value outside it. Renaming the parameter would not break the call.

### Page 10.2 — The spec sheet

Complete working file, run, with its real output:

```python
# week10_toolkit.py — five tiny functions, built from the spec sheet.
# Every one of them RETURNS. Not one of them prints.

def double(number):
    # Give back the number multiplied by two.
    return number * 2

def change_left(paid, cost):
    # Give back how much money is left after paying.
    return paid - cost

def slice_cost(pizza_price, slices=8):
    # Give back the cost of one slice. A whole pizza is 8 slices unless told otherwise.
    return pizza_price / slices

def is_even(number):
    # Give back True if the number divides by 2 with nothing left over.
    return number % 2 == 0

def bus_fare(age):
    # Give back the fare in rupees for someone of this age.
    if age < 5:
        return 0                   # under 5 travels free
    elif age < 18:
        return 15                  # child fare
    elif age < 60:
        return 30                  # adult fare
    else:
        return 10                  # senior fare

# ---- three tests each, and one of the three is awkward on purpose ----
print("double        :", double(6), double(0), double(-3))
print("change_left   :", change_left(100, 65), change_left(100, 100), change_left(50, 65))
print("slice_cost    :", slice_cost(400), slice_cost(400, 4), slice_cost(400, 1))
print("is_even       :", is_even(10), is_even(7), is_even(0))
print("bus_fare      :", bus_fare(4), bus_fare(12), bus_fare(60))
```

```text
double        : 12 0 -6
change_left   : 35 0 -15
slice_cost    : 50.0 100.0 400.0
is_even       : True False True
bus_fare      : 0 15 10
```

**Notes on each function, for marking:**

- **`double`** — full marks needs `return`, not `print`. `-3` doubling to `-6` needs no special code, and it is worth pointing that out.
- **`change_left`** — `change_left(50, 65)` giving `-15` is **correct**, not a bug. A student who adds an `if` to stop it going negative has made a design decision, not a fix; ask them who decided that ₹-15 should be reported as ₹0, and whether that is honest. Both answers are defensible; the *deciding* is the point.
- **`slice_cost`** — the default must be written `slices=8` in the definition, not handled with an `if` inside the body. If they wrote the `if` version, it works, and the default is shorter and says what it means. Also: the answers come out `50.0` and not `50`, because `/` always gives a decimal in Python. That is not an error.
- **`is_even`** — the shortest correct body is `return number % 2 == 0`, because a comparison *is already* `True` or `False`. If they wrote `if number % 2 == 0: return True else: return False`, it is correct and it is four lines doing one line's job — worth showing them the shorter version once. And `is_even(0)` being `True` is right: zero divides by two exactly.
- **`bus_fare`** — the four bands must be checked in order, and because every branch `return`s, the chain stops at the first match. `bus_fare(60)` gives **10**, not 30: `60 < 60` is `False`, so it falls through to the `else`. That is the whole reason 60 is the awkward test.

### Page 10.3 — The test table

Predict first, then run. Correct values:

| Function | Test 1 | Test 2 | Test 3 (awkward) | Why test 3 is awkward |
|---|---|---|---|---|
| `double` | `double(6)` → **12** | `double(0)` → **0** | `double(-3)` → **-6** | Negatives are the case people forget to try. |
| `change_left` | `(100, 65)` → **35** | `(100, 100)` → **0** | `(50, 65)` → **-15** | Exactly zero is a boundary; a negative is a real answer, not an error. |
| `slice_cost` | `(400)` → **50.0** | `(400, 4)` → **100.0** | `(400, 1)` → **400.0** | One slice means the whole pizza — and it proves the division is real division. |
| `is_even` | `is_even(10)` → **True** | `is_even(7)` → **False** | `is_even(0)` → **True** | Nearly everyone predicts `False` for zero. |
| `bus_fare` | `bus_fare(4)` → **0** | `bus_fare(12)` → **15** | `bus_fare(60)` → **10** | 60 sits exactly on a boundary; `60 < 60` is False. |

**10.3(a) Which prediction did you get wrong, and why?**
The two that catch almost everybody are `is_even(0)` → `True` and `bus_fare(60)` → `10`. Mark the honesty, not the accuracy: a student who wrote a wrong prediction and then explained the gap has learned more than one who wrote nothing until after running it.

**10.3(b) `slice_cost(400)` gave `50.0`, not `50`. Is that a bug?**
No. Dividing with `/` in Python always produces a decimal number, even when the answer is exact. If you want a reader to see `50.00`, that is the caller's job with an f-string: `f"{slice_cost(400):.2f}"`. The function should hand back the true number and let whoever is printing decide how it looks.

### Page 10.4 — The bug hunt

**(a) Paste the real error message.**

```text
55
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_broken.py", line 22, in <module>
    print("left each week:", rupees(left_each_week))
  File "/Users/you/ai-academy/level2/week10_broken.py", line 17, in rupees
    return f"Rs {amount:.2f}"
TypeError: unsupported format string passed to NoneType.__format__
```

**(b) Which function is guilty, and how do you know?**

`weekly_saving`. The reasoning, and full marks needs the chain, not just the name:

1. The last line says **`NoneType`** — so something handed back nothing.
2. The bottom `File` line points at line 17, inside `rupees` — but that is only where the damage *showed up*. `rupees` was handed a `None` and did the best it could.
3. The `File` line above it points at line 22 — that is who called `rupees`, and what it passed in was `left_each_week`.
4. `left_each_week` was set on line 21, from `weekly_saving(200, 145)`.
5. `weekly_saving` ends with `print`, not `return`. **Guilty.**

**(c) Why did the bug look correct? (one sentence)**

Model answer: *"It printed 55, and 55 was the right answer, so the function looked like it worked — the mistake only showed up when the answer had to be used somewhere instead of just read."*

Accept any sentence containing both halves: **the right answer appeared**, and **nothing came back**. Do not accept "because I typed the wrong word" — that says what happened, not why it was invisible.

**(d) The fix, and the output afterwards.**

One word on line 7: `print` becomes `return`.

```python
def weekly_saving(pocket_money, spent):
    # Should give back how much is left over each week.
    return pocket_money - spent
```

```text
left each week: Rs 55.00
saved in a year: Rs 2860.00
```

Hand-check: 200 − 145 = 55 ✔ · 55 × 52 = 2,860 ✔ · `Rs 2860.00` because `:.2f` always shows two decimal places.

**(e) How could you have found it in two lines instead of by reading the whole file?**

Catch what came back and print it. A complete file that does nothing but diagnose:

```python
# diagnose.py -- what did that function actually hand back?

def weekly_saving(pocket_money, spent):
    print(pocket_money - spent)        # the bug, copied as-is

came_back = weekly_saving(200, 145)
print("what came back was:", came_back)
print("its type is:", type(came_back))
```

```text
55
what came back was: None
its type is: <class 'NoneType'>
```

**(f) `yearly_saving` has a default of `52`. Was that used?**

Yes. `yearly_saving(left_each_week)` supplies only one argument, so `weeks` used its default of 52. Calling `yearly_saving(55, 12)` would give 660 — a year of monthly saving instead of weekly.

### Page 10.5 — Scope predictions

Write your answer first, then run each one.

**(a)**

```python
def bus_fare(age):
    fare = 15
    return fare

print(bus_fare(12))
print(fare)
```

**Prediction:** most people expect `15` then `15`.
**What actually happens:**

```text
15
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week10_scope.py", line 6, in <module>
    print(fare)
NameError: name 'fare' is not defined
```

**Why:** `fare` was created inside `bus_fare`, so it only existed while the call was running. The *value* 15 escaped through the `return`. The *name* never left the room.

**(b)**

```python
pocket_money = 200

def spend_it_all():
    pocket_money = 0
    print("inside the function :", pocket_money)

spend_it_all()
print("after the function   :", pocket_money)
```

```text
inside the function : 0
after the function   : 200
```

**Why:** two different boxes that happen to share a word. Assigning to `pocket_money` inside the function made a brand-new local box; the outer one was never touched. Same word, different rooms.

**(c)**

```python
PASS_MARK = 35

def has_passed(mark):
    return mark >= PASS_MARK

print(has_passed(40))
print(has_passed(30))
```

```text
True
False
```

**Why:** *reading* an outside variable from inside a function is allowed. This is the one that goes the way people expect. (Whether it is a good idea is another matter — a function that reads things from outside itself is harder to test, which is exactly the argument in "Questions Students Ask".)

**(d)**

```python
score_total = 0

def add_one():
    score_total = score_total + 1
    return score_total

print(add_one())
```

```text
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/hw10_scope.py", line 7, in <module>
    print(add_one())
  File "/Users/you/ai-academy/level2/hw10_scope.py", line 4, in add_one
    score_total = score_total + 1
UnboundLocalError: local variable 'score_total' referenced before assignment
```

**Why, and this is the subtle one:** because there is an *assignment* to `score_total` somewhere in the function, Python decides the name is local for the whole function — before it runs a single line. Then the very first thing that line does is *read* it, and the local box is still empty. Hence "referenced before assignment".

**The fix, and it is not `global`:** take the value in and hand the new one back.

```python
score_total = 0

def add_one(current):
    return current + 1

score_total = add_one(score_total)
score_total = add_one(score_total)
print(score_total)
```

```text
2
```

*(On Python 3.12 and later the message reads "cannot access local variable 'score_total' where it is not associated with a value". Same error, same reason, same fix.)*

**10.5(e) Which of the four surprised you, and what did you believe before?**
Mark the honesty. The two that surprise most people are (a) — because the value clearly existed — and (d), because the outer variable is right there on the screen. A good answer names the belief: "I thought a variable was a variable and anything could see it."

### Page 10.6 — Vocabulary and syntax, in your own words

Accept any wording that is *correct and theirs*. These are the reference versions:

| Term | A good answer contains | A wrong answer to watch for |
|---|---|---|
| **parameter** | A name in the definition; an empty labelled box. | "The number you give it" — that's the argument. |
| **argument** | The value handed over at the call. | Confusing it with the default value. |
| **default value** | What the parameter holds when the caller says nothing. | "The answer if it goes wrong." |
| **scope** | The part of the program where a name exists. | "How big the function is." |
| **`None`** | Python's word for no value; what you get back when there was no `return`. | "Zero", or "an error". |

| Syntax | What it does |
|---|---|
| `def f(a, b):` | Makes a function with two empty boxes, filled in that order by the caller. |
| `def f(a, b=0):` | The same, but `b` already has 0 in it, so the caller may leave it out. |
| `f(b=3)` | Fills the box called `b` by name, so the order cannot be got wrong. |
| `None` | No value at all. What comes back from a function that never returned. |

### Answers to the questions posed in the lesson scripts

- *"Which card goes on PAID?"* → 100. The story said "I went out with a hundred."
- *"If I swap the cards, does the computer complain?"* → No. It returns −35 and believes it has done its job. Both boxes take a number; Python has no idea what money is.
- *"So whose job is it to get the order right?"* → The caller's. And keyword arguments (`change_left(paid=100, cost=65)`) are how you make that promise impossible to break.
- *"Inside `double`, what is the 6 called?"* → `number`. The function's private label for whatever arrives.
- *"Could I rename `number` to `n` and still call `double(6)`?"* → Yes. Callers never know what the box is labelled.
- *"Why not just print inside the function?"* → Because the answer is then gone; you cannot store, add, compare or reuse it. You can always print a returned value.
- *"Is `None` the same as 0?"* → No. `0 * 2` is 0. `None * 2` crashes with `TypeError`.
- *"How many things can a function hand back?"* → One, this week. There is a trick for more and it is a few weeks off.
- *"What's the difference between an error that stops everything before it starts and one halfway through?"* → A `SyntaxError` means Python could not even read the file, so nothing ran. A `TypeError` halfway through means part of the program worked — which is exactly what makes the missing-`return` bug hard to see, because the correct answer prints first.
- *"Did we have to do anything special to make negative numbers work?"* → No. The function never asked what kind of number it was given.
- *"Why did it print the first three lines again?"* → Python runs the whole file from the top every time you run it.

---

## 🔮 Next Week Preview

Week 11 answers a question that has been quietly building since Week 7: **where do you put twenty numbers?** So far every value has had its own box with its own name, which is fine for two and unbearable for twenty. Next week the student meets the **list** — many values under one name, laid out in a row of numbered slots — and immediately runs into the thing that trips up every programmer alive: *the first slot is number 0, not 1.* The lesson is built around index cards on the table with slot numbers written underneath in pink, because reaching for a card that isn't there is a much better way to meet `IndexError` than reading about it. By the end they can build a list, open any slot, reach the last item with `-1`, count with `len()`, add one more with `append()`, and produce an `IndexError` on purpose and explain it.

**Prep early:** you need **four index cards and a marker pen** — the same four you used for this week's Hook will do, blank side up. Write nothing on them until the lesson. You will also want a pink or red pen specifically, because the slot numbers going *under* the cards in a different colour from the values *on* the cards is what makes the picture work. And keep `week10_toolkit.py`: in Week 12 those five functions become the shape of the student's very first two-file program, and `stats.py` is a straight sequel to the spec sheet they filled in this week.

---

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
