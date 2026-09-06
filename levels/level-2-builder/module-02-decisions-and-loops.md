# Module 2 — Decisions and Loops: Programs That Choose and Repeat

**Level 2 · Module 2 · ~3.5 hours · Prereqs: Module 1 (variables, types, f-strings, input, tracebacks)**

[⬅ Previous](module-01-python-from-zero.md) · [Level 2 Home](README.md) · [Next ➡](module-03-functions-and-lists.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** write `if` / `elif` / `else` chains that handle every case exactly once, with no gaps and no overlaps.
2. **You will be able to** combine comparisons with `and`, `or`, and `not`, and predict the result before running.
3. **You will be able to** write `for` loops over `range()` and `while` loops with a clear stopping condition — and escape an infinite loop.
4. **You will be able to** use an accumulator variable to total, count, and find a maximum.
5. **You will be able to** find and fix an off-by-one bug by tracing the loop on paper.

---

## 🪝 The Hook

Your Module 1 programs had one flaw you probably didn't notice: they did the *same thing every time*. Feed `bill_split.py` a bill of ₹1,240 or ₹12, it runs the identical five instructions. It never says "wait, that's a strange number, are you sure?"

And they were short. Suppose your teacher hands you 200 test scores and asks for the average, the highest, and how many students failed. With Module 1 tools you would type 200 variables. Nobody does that. Nobody *can* do that.

Two ideas fix both problems, and they are the last two ideas you need before your programs stop being calculators and start being *programs*. The first is **choosing**: do this, but only if that. The second is **repeating**: do this again, and again, until something changes.

Every AI system you will ever build is made of these two ideas, stacked millions deep.

---

## 🧠 The Concept

### 1. Booleans and comparison operators

#### The plain-language explanation

In Module 1 you met `bool` — the type with exactly two values, `True` and `False`. You mostly ignored it. Now it becomes the most important type in the language, because **every decision a computer makes is a boolean**.

You produce booleans by **comparing** things. A comparison is a question with a yes/no answer, and Python answers it with `True` or `False`.

> **Definition — comparison operator:** a symbol that compares two values and produces `True` or `False`.

| Operator | Reads as | Example | Result |
|---|---|---|---|
| `==` | "is equal to" | `5 == 5` | `True` |
| `!=` | "is not equal to" | `5 != 3` | `True` |
| `<` | "is less than" | `3 < 5` | `True` |
| `>` | "is greater than" | `3 > 5` | `False` |
| `<=` | "is less than or equal to" | `5 <= 5` | `True` |
| `>=` | "is greater than or equal to" | `3 >= 5` | `False` |

#### 🍕 The analogy

`=` and `==` look almost the same and mean completely different things. Here's how to keep them straight:

- `=` is a **delivery van**. `score = 47` delivers 47 into the box labelled `score`. It changes the world.
- `==` is a **judge**. `score == 47` looks at the box, looks at 47, and rules "same" or "not same". It changes nothing; it just reports.

One van, one judge. If you write `if score = 47:` Python stops you with a `SyntaxError`, which is a kindness — in some older languages that line silently sets the score to 47 and then always runs the branch.

#### The tiny concrete example with real numbers

Your school's pass mark is 35 out of 100.

```python
mark = 42                # this student's score
pass_mark = 35

print(mark >= pass_mark)      # 42 >= 35
print(mark == 100)            # is it a perfect score?
print(mark != 42)             # is it anything other than 42?
print(mark < 35)              # did they fail?
```

Output:

```
True
False
False
False
```

Comparisons work on strings too. Strings compare **alphabetically** (technically by character code, so all capitals sort before all lowercase):

```python
print("apple" < "banana")     # a comes before b
print("Zebra" < "apple")      # capital Z (90) < lowercase a (97)
print("cat" == "Cat")         # case matters
```

Output:

```
True
True
False
```

That last one bites people constantly. `"yes" == "Yes"` is `False`. When you compare user input, normalise it first with `.lower()`:

```python
answer = "YES"
print(answer.lower() == "yes")
```

Output:

```
True
```

> **Definition — method:** a function that belongs to a value and is called with a dot, like `answer.lower()`. You'll meet many of these; for now, `.lower()`, `.strip()` (removes spaces at the ends), and `.isdigit()` (is this text made only of digits?) are the three you need.

```python
messy = "  Yes  "
print(messy.strip())              # "Yes"  — spaces removed
print(messy.strip().lower())      # "yes"  — chained: strip first, then lower
print("42".isdigit())             # True
print("4.2".isdigit())            # False — the dot is not a digit
print("abc".isdigit())            # False
```

Output:

```
Yes
yes
True
False
False
```

`.isdigit()` will be your bad-input guard for the whole module.

---

### 2. `if` / `elif` / `else` and the order-matters trap

#### The plain-language explanation

An `if` statement runs a block of code **only when** a boolean is `True`.

```python
temperature = 38

if temperature > 37.5:
    print("You have a fever.")
    print("Rest and drink water.")

print("Report finished.")
```

Output:

```
You have a fever.
Rest and drink water.
Report finished.
```

Three pieces of punctuation carry all the meaning here:

```
   if temperature > 37.5:
   ▲       ▲            ▲
   │       │            └── the COLON: "the block starts now"
   │       └── the CONDITION: anything that produces True or False
   └── the keyword

       print("You have a fever.")     ◄── INDENTED 4 spaces = inside the if
       print("Rest and drink water.")  ◄── still indented = still inside
   print("Report finished.")           ◄── not indented = always runs
```

> **Definition — block:** a group of lines that belong together, marked by being indented the same amount.

**Python uses indentation as real syntax.** In most languages indentation is decoration; in Python it is the thing that says what's inside what. Four spaces is the convention. Your editor will do it for you when you press Enter after a colon.

Add `else` for "otherwise", and `elif` (short for "else if") for extra cases:

```python
temperature = 36.4

if temperature > 37.5:
    print("Fever.")
elif temperature > 37.0:
    print("Slightly warm.")
elif temperature > 35.0:
    print("Normal.")
else:
    print("Too cold — check the thermometer.")
```

Output:

```
Normal.
```

#### 🍕 The analogy

An `if/elif/else` chain is a **queue of bouncers at one door**. Each person walks up to bouncer #1. If bouncer #1 says yes, they go in and **the rest of the bouncers never see them**. Only if #1 says no do they move to #2.

```
   value ──► [ if cond1 ]──True──► block 1 ──┐
                  │False                      │
                  ▼                           │
             [ elif cond2 ]──True──► block 2 ─┤
                  │False                      ├──► rest of program
                  ▼                           │
             [ elif cond3 ]──True──► block 3 ─┤
                  │False                      │
                  ▼                           │
             [ else      ]────────► block 4 ──┘

   EXACTLY ONE block runs. Never zero (if there's an else). Never two.
```

That "exactly one" guarantee is the whole point of `elif`. Compare with separate `if` statements, which are separate doors with separate bouncers — a value can go through all of them.

#### The order-matters trap

Here is the bug that gets *everybody*. Grade a mark out of 100:

```python
mark = 92

if mark >= 35:
    print("Grade: D")
elif mark >= 60:
    print("Grade: C")
elif mark >= 75:
    print("Grade: B")
elif mark >= 90:
    print("Grade: A")
else:
    print("Grade: F")
```

Output:

```
Grade: D
```

A 92 got a D. Why? Because `92 >= 35` is `True`, bouncer #1 said yes, and the other three bouncers never got a look. Every mark from 35 to 100 gets a D.

**The rule: in a chain of overlapping conditions, order from most restrictive to least restrictive.** For "greater than" chains, that means **highest threshold first**.

```python
mark = 92

if mark >= 90:
    print("Grade: A")
elif mark >= 75:
    print("Grade: B")
elif mark >= 60:
    print("Grade: C")
elif mark >= 35:
    print("Grade: D")
else:
    print("Grade: F")
```

Output:

```
Grade: A
```

Now trace it for `mark = 62`: `62 >= 90`? No. `62 >= 75`? No. `62 >= 60`? **Yes** → C. Correct, and notice you did not need to write `elif mark >= 60 and mark < 75`. The chain already guarantees you only reach line 3 if the first two failed. **Every `elif` silently carries "and none of the above."** That is why chains are cleaner than separate `if`s.

#### The tiny concrete example with a coverage check

Whenever you write a chain, check two things:

1. **No gaps** — is every possible input handled? (An `else` at the end guarantees this.)
2. **No wrong overlaps** — for any input, is the *first* matching branch the one you want?

| Input mark | 90? | 75? | 60? | 35? | Branch taken | Correct? |
|---|---|---|---|---|---|---|
| 100 | ✓ | — | — | — | A | ✔ |
| 90 | ✓ | — | — | — | A | ✔ (boundary) |
| 89 | ✗ | ✓ | — | — | B | ✔ |
| 60 | ✗ | ✗ | ✓ | — | C | ✔ (boundary) |
| 35 | ✗ | ✗ | ✗ | ✓ | D | ✔ (boundary) |
| 34 | ✗ | ✗ | ✗ | ✗ | F | ✔ |
| 0 | ✗ | ✗ | ✗ | ✗ | F | ✔ |

**Always test the boundaries.** The values right at the edge — 90, 89, 35, 34 — are where 90% of logic bugs live.

---

### 3. Logical operators: `and`, `or`, `not`

#### The plain-language explanation

Real conditions are rarely one comparison. "Can I go out?" depends on homework being done **and** it not raining. Python gives you three words to combine booleans.

> **Definition — logical operator:** a word (`and`, `or`, `not`) that combines or flips boolean values.

| Operator | True when... | Memory hook |
|---|---|---|
| `A and B` | **both** are True | strict — everything must pass |
| `A or B` | **at least one** is True | generous — one is enough |
| `not A` | A is False | flip it |

The complete truth tables — memorise these, they never change:

| A | B | `A and B` | `A or B` |
|---|---|---|---|
| True | True | **True** | **True** |
| True | False | False | **True** |
| False | True | False | **True** |
| False | False | False | False |

| A | `not A` |
|---|---|
| True | False |
| False | True |

#### 🍕 The analogy

- **`and` is a pizza order for two picky people.** Both must approve the topping. One veto kills it.
- **`or` is a cricket team selection with two selectors.** If *either* selector likes you, you're in.
- **`not` is a mirror.** Whatever you show it, it shows the opposite.

One critical warning about `or`: in English, "you can have tea or coffee" usually means *one, not both*. In Python, `or` means "at least one, and both is fine too." `True or True` is `True`.

#### The tiny concrete example with real numbers

Cricket team eligibility: a player must be **at least 13**, have played **at least 5 matches**, and **not** be injured.

```python
age = 14
matches = 7
injured = False

eligible = age >= 13 and matches >= 5 and not injured
print(eligible)

# Trace it piece by piece:
print(age >= 13)          # 14 >= 13
print(matches >= 5)       # 7 >= 5
print(not injured)        # not False
print(True and True and True)
```

Output:

```
True
True
True
True
True
```

Now change one thing — the player twisted an ankle:

```python
age = 14
matches = 7
injured = True

print(age >= 13 and matches >= 5 and not injured)   # True and True and False
```

Output:

```
False
```

One `False` anywhere in an `and` chain sinks the whole thing.

#### Precedence: which happens first

When you mix them, Python evaluates in this order: **comparisons first, then `not`, then `and`, then `or`.**

```python
print(True or False and False)
```

Work it out: `and` binds tighter, so this is `True or (False and False)` = `True or False` = `True`.

Output:

```
True
```

If you meant `(True or False) and False` — which is `False` — you must write the brackets. **Rule for your own sanity: when you mix `and` with `or`, always add brackets even if you don't need them.** Future-you will thank present-you.

#### The chained comparison shortcut

Python lets you write mathematical ranges directly:

```python
mark = 72
print(60 <= mark < 75)                    # the Python-idiomatic way
print(mark >= 60 and mark < 75)           # the long way — identical meaning
```

Output:

```
True
True
```

`60 <= mark < 75` reads exactly like maths and is easier to get right than the `and` version. Use it for ranges.

⚠️ **The `or` trap that everyone hits once:**

```python
answer = "maybe"
print(answer == "yes" or "y")      # WRONG — but prints something!
```

Output:

```
y
```

Wait, what? You asked a yes/no question and got the letter `y` back. Here is why: `answer == "yes"` is `False`. Then Python evaluates `False or "y"`. Python's `or` doesn't return `True`/`False` — it returns **the first side that counts as "truthy"**, and a non-empty string always counts as truthy. So the whole expression is `"y"`.

> **Definition — truthy / falsy:** when Python needs a yes/no answer from a non-boolean, empty things (`""`, `0`) count as `False` and everything else counts as `True`.

Inside an `if`, `"y"` is truthy, so **the branch always runs, no matter what the user typed**:

```python
answer = "maybe"
if answer == "yes" or "y":
    print("You said yes!")      # this WILL print, wrongly
```

Output:

```
You said yes!
```

The fix — spell out both comparisons in full:

```python
answer = "maybe"
if answer == "yes" or answer == "y":
    print("You said yes!")
else:
    print("Not a yes.")
```

Output:

```
Not a yes.
```

**Rule: every side of an `or` must be a complete comparison.**

---

### 4. `for` loops, `range()`, and `while` loops

#### The plain-language explanation — `for`

A **loop** repeats a block of code. The `for` loop repeats it a **known number of times**, or once for each item in a collection.

> **Definition — `for` loop:** repeats a block once for each value produced by something, with a variable that takes on each value in turn.

```python
for i in range(5):
    print(i)
```

Output:

```
0
1
2
3
4
```

Read it as: "for each value `i` in the sequence 0,1,2,3,4 — print it."

`range()` is the number generator. Three forms:

| Call | Produces | Notes |
|---|---|---|
| `range(5)` | 0, 1, 2, 3, 4 | starts at 0, **stops before** 5 |
| `range(2, 6)` | 2, 3, 4, 5 | start included, **stop excluded** |
| `range(0, 10, 3)` | 0, 3, 6, 9 | third number is the step |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 | negative step counts down |

**`range(5)` gives you five numbers, but the last one is 4, not 5.** This trips up every single beginner, and it is the source of the "off-by-one bug" you'll meet in sub-concept 5. Say it out loud: *"range stops before the number you give it."*

Why start at 0 and stop early? Because then `range(n)` always gives exactly `n` values, and `range(a, b)` always gives exactly `b - a` values. `range(2, 6)` gives 6 − 2 = 4 values. Clean arithmetic, forever.

#### 🍕 The analogy

A `for` loop is a **conveyor belt in a pizza kitchen**. The belt carries a fixed number of bases past you. For each base that arrives, you do the same job. When the last base passes, the belt stops on its own. You never have to decide when to stop — the belt knows.

A `while` loop is completely different. It's **stirring a pot until it thickens**. You don't know how many stirs. You check after each stir and keep going while it's still thin. If you never check, or the sauce never thickens, you stir forever.

#### The plain-language explanation — `while`

> **Definition — `while` loop:** repeats a block for as long as a condition stays `True`, checking the condition before each repeat.

```python
countdown = 3

while countdown > 0:
    print(countdown)
    countdown = countdown - 1     # THIS LINE is what eventually stops the loop

print("Liftoff!")
```

Output:

```
3
2
1
Liftoff!
```

Trace it precisely:

| Check # | `countdown` before check | `countdown > 0`? | Prints | `countdown` after |
|---|---|---|---|---|
| 1 | 3 | True | `3` | 2 |
| 2 | 2 | True | `2` | 1 |
| 3 | 1 | True | `1` | 0 |
| 4 | 0 | **False** | — | loop ends |

Every `while` loop needs three things, and missing any one is a bug:

```
   ┌─────────────────────────────────────────────┐
   │  1. SET UP   countdown = 3                  │  before the loop
   │  2. CHECK    while countdown > 0:           │  the condition
   │  3. CHANGE       countdown = countdown - 1  │  inside the loop
   └─────────────────────────────────────────────┘
        Miss #3 and you have an INFINITE LOOP.
```

#### Infinite-loop rescue

```python
countdown = 3
while countdown > 0:
    print(countdown)
    # oops — forgot to change countdown
```

This prints `3` forever, thousands of lines a second.

**To stop it: press `Ctrl` and `C` together in the terminal.** (Both macOS and Windows — it's Ctrl, not Cmd, even on a Mac.) You'll see:

```
3
3
3
^C
Traceback (most recent call last):
  File "loop.py", line 3, in <module>
    print(countdown)
KeyboardInterrupt
```

`KeyboardInterrupt` means "you stopped me." That's not a bug in your code — that's you winning. Then go find the missing "change" line.

#### The tiny concrete example — which loop to pick

| Situation | Loop | Why |
|---|---|---|
| Print the 7 times table (1–10) | `for` | You know it's exactly 10 rows |
| Keep asking until the user types a number | `while` | You have no idea how many bad tries they'll make |
| Total up 30 scores | `for` | Exactly 30 |
| Guessing game until they win or run out | `while` | Depends on their guesses |

**Rule of thumb: if you can say the number of repeats out loud before starting, use `for`. Otherwise use `while`.**

The 7 times table, both ways:

```python
# for version — 10 rows, known in advance
for n in range(1, 11):                 # 1..10 (stops before 11)
    print(f"7 x {n} = {7 * n}")
```

Output:

```
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

---

### 5. Accumulators, counters, `break`, `continue`, and off-by-one bugs

#### The plain-language explanation — the accumulator pattern

> **Definition — accumulator:** a variable created before a loop and updated inside it, so that after the loop it holds a result built from every pass.

This is *the* most reused pattern in all of programming. Three flavours:

**Flavour 1 — total (start at 0, add):**

```python
total = 0                        # start empty
for n in range(1, 6):            # 1,2,3,4,5
    total = total + n            # add this one to the running total
print(total)
```

Output:

```
15
```

Trace: total goes 0 → 1 → 3 → 6 → 10 → 15. (1+2+3+4+5 = 15 ✔)

**Flavour 2 — counter (start at 0, add 1 when something is true):**

```python
count = 0                        # how many multiples of 3 are there in 1..20?
for n in range(1, 21):           # 1..20
    if n % 3 == 0:               # divisible by 3?
        count = count + 1
print(count)
```

Output:

```
6
```

Check: 3, 6, 9, 12, 15, 18 — six of them ✔

**Flavour 3 — maximum (start at the worst possible value, replace when beaten):**

```python
highest = -1                     # -1 is lower than any real score, so anything beats it
for score in [34, 78, 12, 78, 55]:      # a list of numbers — more on lists in Module 3
    if score > highest:
        highest = score          # this one is the new champion
print(highest)
```

Output:

```
78
```

Trace: highest goes −1 → 34 → 78 → (12 loses) → (78 ties, `>` is false, no change) → (55 loses) → **78** ✔

#### 🍕 The shorthand you'll use forever

`total = total + n` is so common Python gives you a shortcut:

```python
total += n        # exactly the same as: total = total + n
count += 1        # exactly the same as: count = count + 1
lives -= 1        # exactly the same as: lives = lives - 1
money *= 2        # exactly the same as: money = money * 2
```

> **Definition — augmented assignment:** `+=`, `-=`, `*=`, `/=` — shortcuts that update a variable using its own current value.

Rewritten:

```python
total = 0
for n in range(1, 101):     # 1..100
    total += n
print(total)
```

Output:

```
5050
```

(That's the famous sum 1..100. Check with the formula n(n+1)/2 = 100 × 101 / 2 = 5050 ✔)

#### `break` and `continue`

Two words that change a loop's flow:

> **Definition — `break`:** immediately leave the loop entirely, skipping any remaining passes.
>
> **Definition — `continue`:** skip the rest of *this* pass and jump straight to the next one.

```python
# break — stop as soon as you find what you want
for n in range(1, 100):
    if n * n > 500:
        print(f"The first square over 500 is {n} squared = {n * n}")
        break                 # found it; don't check 24..99
```

Output:

```
The first square over 500 is 23 squared = 529
```

Check: 22² = 484 (not over 500), 23² = 529 (over) ✔

```python
# continue — skip the ones you don't care about
for n in range(1, 11):
    if n % 2 == 0:
        continue              # even? skip the print, go to next n
    print(n, end=" ")         # end=" " prints a space instead of a newline
print()                       # a bare print() ends the line
```

Output:

```
1 3 5 7 9 
```

```
   break:                       continue:
   ┌───────────┐                ┌───────────┐
   │  pass 1   │                │  pass 1   │
   │  pass 2   │                │  pass 2 ──┼──skip rest of body
   │  pass 3 ──┼──► OUT         │  pass 3   │
   │  pass 4   │  (never runs)  │  pass 4   │
   └───────────┘                └───────────┘
   leaves the loop              leaves only this pass
```

#### Off-by-one bugs

> **Definition — off-by-one bug:** a loop that runs one time too many or one time too few, usually because of a `range()` boundary.

This is the single most common bug in programming. Three examples:

**Bug A — forgot that range stops early.**

```python
# Goal: print 1 to 10
for n in range(1, 10):
    print(n, end=" ")
```

Output:

```
1 2 3 4 5 6 7 8 9 
```

Only nine numbers. Fix: `range(1, 11)`.

**Bug B — counted the fence posts wrong.**

```python
# Goal: print 5 dashes between 5 items
for i in range(5):
    print("item")
    print("-----")
```

That prints a dash *after the last item too* — 5 dashes for 5 items, when you want 4 *between* them. This is the classic **fence-post problem**: 5 fence panels need 6 posts, and 5 items have only 4 gaps.

**Bug C — the `while` that runs once extra.**

```python
attempts = 0
while attempts <= 3:            # <= gives FOUR attempts: 0,1,2,3
    print(f"Attempt {attempts}")
    attempts += 1
```

Output:

```
Attempt 0
Attempt 1
Attempt 2
Attempt 3
```

Four, not three. Fix: `while attempts < 3:`.

**The cure for all three: trace the first two and the last two passes on paper before you run.** Write a tiny table with columns for the loop variable and any accumulator. It takes 60 seconds and saves 30 minutes.

---

## 🔍 Worked Example

**The problem.** A cricket team's last 8 innings scores are: 45, 0, 112, 67, 8, 89, 34, 101.

Write a program that reports:

1. total runs
2. average
3. highest score
4. how many "fifties" (scores of 50 or more)
5. how many ducks (score of exactly 0)
6. for each score, a one-word verdict

I'll trace the accumulators through all 8 passes.

### Step 1 — Set up the accumulators before the loop

```python
scores = [45, 0, 112, 67, 8, 89, 34, 101]    # 8 innings

total = 0          # accumulator: running sum, starts empty
highest = -1       # accumulator: best so far, starts below any real score
fifties = 0        # counter
ducks = 0          # counter
```

Why `highest = -1` and not `highest = 0`? Because a score of 0 is a real score. If I started at 0 and every innings were a duck, `0 > 0` is `False`, so `highest` would stay 0 — which happens to be right here, but the habit is dangerous. Starting below every possible value is always safe. (You'll learn an even better way in Module 3 using `max()`.)

### Step 2 — Trace the loop by hand

The loop body will be:

```python
for score in scores:
    total += score
    if score > highest:
        highest = score
    if score >= 50:
        fifties += 1
    if score == 0:
        ducks += 1
```

| Pass | `score` | `total` after | `score > highest`? | `highest` after | `>= 50`? | `fifties` | `== 0`? | `ducks` |
|---|---|---|---|---|---|---|---|---|
| start | — | 0 | — | −1 | — | 0 | — | 0 |
| 1 | 45 | 45 | 45 > −1 ✓ | 45 | no | 0 | no | 0 |
| 2 | 0 | 45 | 0 > 45 ✗ | 45 | no | 0 | **yes** | 1 |
| 3 | 112 | 157 | 112 > 45 ✓ | 112 | **yes** | 1 | no | 1 |
| 4 | 67 | 224 | 67 > 112 ✗ | 112 | **yes** | 2 | no | 1 |
| 5 | 8 | 232 | 8 > 112 ✗ | 112 | no | 2 | no | 1 |
| 6 | 89 | 321 | 89 > 112 ✗ | 112 | **yes** | 3 | no | 1 |
| 7 | 34 | 355 | 34 > 112 ✗ | 112 | no | 3 | no | 1 |
| 8 | 101 | 456 | 101 > 112 ✗ | 112 | **yes** | 4 | no | 1 |

Final: `total = 456`, `highest = 112`, `fifties = 4`, `ducks = 1`.

Verify the total by hand: 45 + 0 = 45. +112 = 157. +67 = 224. +8 = 232. +89 = 321. +34 = 355. +101 = **456** ✔

### Step 3 — The average

```python
average = total / 8
```

456 ÷ 8 = **57.0** exactly (8 × 57 = 456) ✔

### Step 4 — The verdict chain

For each score, one word. Order from most restrictive down:

| Condition | Verdict |
|---|---|
| `score >= 100` | CENTURY |
| `score >= 50` | FIFTY |
| `score >= 20` | steady |
| `score >= 1` | poor |
| `else` | DUCK |

Trace all 8: 45→poor... wait, 45 ≥ 20, so **steady**. Let me redo carefully:

- 45: ≥100? no. ≥50? no. ≥20? **yes** → steady
- 0: ≥100? no. ≥50? no. ≥20? no. ≥1? no → **DUCK**
- 112: ≥100? **yes** → CENTURY
- 67: ≥100? no. ≥50? **yes** → FIFTY
- 8: ≥100? no. ≥50? no. ≥20? no. ≥1? **yes** → poor
- 89: ≥50? **yes** → FIFTY
- 34: ≥20? **yes** → steady
- 101: ≥100? **yes** → CENTURY

### Step 5 — The whole program

```python
# innings_report.py — summarise a season of cricket scores.

scores = [45, 0, 112, 67, 8, 89, 34, 101]     # the season's 8 innings

total = 0             # accumulator for the sum
highest = -1          # accumulator for the max; -1 is below any real score
fifties = 0           # counter for scores >= 50
ducks = 0             # counter for scores exactly 0

print("INNINGS  SCORE  VERDICT")
print("-" * 26)

innings = 0                          # which innings number we're on
for score in scores:                 # one pass per score
    innings += 1                     # innings 1, 2, 3, ...

    total += score                   # add to the running total
    if score > highest:              # strictly greater, so ties don't churn
        highest = score
    if score >= 50:
        fifties += 1
    if score == 0:
        ducks += 1

    # Most restrictive condition FIRST, or every score becomes "poor".
    if score >= 100:
        verdict = "CENTURY"
    elif score >= 50:
        verdict = "FIFTY"
    elif score >= 20:
        verdict = "steady"
    elif score >= 1:
        verdict = "poor"
    else:
        verdict = "DUCK"

    print(f"{innings:>7}  {score:>5}  {verdict}")

average = total / innings            # innings is 8 by now

print("-" * 26)
print(f"Total runs : {total}")
print(f"Average    : {average:.2f}")
print(f"Highest    : {highest}")
print(f"Fifties    : {fifties}")
print(f"Ducks      : {ducks}")
```

### Step 6 — The exact output

```
INNINGS  SCORE  VERDICT
--------------------------
      1     45  steady
      2      0  DUCK
      3    112  CENTURY
      4     67  FIFTY
      5      8  poor
      6     89  FIFTY
      7     34  steady
      8    101  CENTURY
--------------------------
Total runs : 456
Average    : 57.00
Highest    : 112
Fifties    : 4
Ducks      : 1
```

Every number matches the hand trace. That's the standard you want: **predict, then run, then compare.** If they differ, one of the two is wrong and you get to find out which — that's how you actually learn.

---

## 💻 Hands-On

### Part A — Comparison and boolean drills (20 minutes)

Open the interactive shell (`python3`) and predict each answer **out loud before pressing Enter**. Keep score.

```python
>>> 5 == 5.0
>>> "5" == 5
>>> 3 != 3
>>> "Apple" == "apple"
>>> "Apple".lower() == "apple"
>>> 10 > 5 > 2
>>> True and False
>>> True or False
>>> not (3 > 5)
>>> (4 > 2) and (2 > 4)
>>> 7 % 2 == 0
>>> "  yes ".strip() == "yes"
```

Answers, with the reasoning:

```
True     # 5 and 5.0 are numerically equal even though types differ
False    # a str is never equal to an int
False    # 3 IS equal to 3, so "not equal" is False
False    # capital A != lowercase a
True     # .lower() turns "Apple" into "apple" first
True     # chained: (10>5) and (5>2)
False    # and needs both
True     # or needs one
True     # 3>5 is False, not False is True
False    # 2>4 is False, so the and fails
False    # 7%2 is 1, and 1 != 0
True     # strip() removes the spaces on both ends
```

If you got 10+ right, move on. If not, work through the truth tables again — this stuff must become automatic.

### Part B — Your first branching program (20 minutes)

New file, `ticket_price.py`:

```python
# ticket_price.py — cinema pricing with age bands and a discount day.

print("=== TICKET PRICING ===")

age_text = input("Your age: ")                 # comes in as a string

# Guard against bad input using .isdigit() — no crash, a clear message instead.
if not age_text.isdigit():
    print("Please type a whole number for age. Run again.")
else:
    age = int(age_text)                        # safe now: we know it's all digits

    # Age bands, ordered so each person matches exactly one.
    if age < 3:
        price = 0
        band = "infant"
    elif age < 13:
        price = 120
        band = "child"
    elif age < 18:
        price = 180
        band = "teen"
    elif age < 60:
        price = 250
        band = "adult"
    else:
        price = 150
        band = "senior"

    day = input("Day of week (e.g. tuesday): ").strip().lower()

    # Tuesday is discount day, but free tickets can't get cheaper.
    if day == "tuesday" and price > 0:
        discount = price * 0.30                # 30% off
        price = price - discount
        print(f"Tuesday discount applied: -{discount:.0f}")

    print(f"Band  : {band}")
    print(f"Price : {price:.0f} rupees")
```

Run it four times and check against your own hand calculation:

| Input | Expected band | Expected price |
|---|---|---|
| `15`, `monday` | teen | 180 |
| `15`, `Tuesday` | teen | 126 (180 − 54) |
| `2`, `tuesday` | infant | 0 |
| `abc`, — | — | the "please type a whole number" message |

Sample run:

```
=== TICKET PRICING ===
Your age: 15
Day of week (e.g. tuesday): Tuesday
Tuesday discount applied: -54
Band  : teen
Price : 126 rupees
```

Check: 30% of 180 = 54. 180 − 54 = 126 ✔. Note `.strip().lower()` turned `"Tuesday"` into `"tuesday"` so the comparison worked.

### Part C — Loop drills (25 minutes)

New file, `loop_drills.py`:

```python
# loop_drills.py — six small loops, one idea each.

print("--- 1. count up ---")
for i in range(5):                       # 0,1,2,3,4  (stops BEFORE 5)
    print(i, end=" ")
print()

print("--- 2. count down ---")
for i in range(5, 0, -1):                # 5,4,3,2,1  (negative step)
    print(i, end=" ")
print()

print("--- 3. evens only, two ways ---")
for i in range(0, 11, 2):                # step of 2: 0,2,4,6,8,10
    print(i, end=" ")
print()
for i in range(11):                      # 0..10, filter with a condition
    if i % 2 != 0:
        continue                         # odd -> skip this pass
    print(i, end=" ")
print()

print("--- 4. accumulate a total ---")
total = 0
for i in range(1, 11):                   # 1..10
    total += i                           # shorthand for total = total + i
print(f"1+2+...+10 = {total}")           # 55

print("--- 5. a while loop with a clear stop ---")
balance = 1000                           # rupees in a piggy bank
weeks = 0
while balance >= 150:                    # keep going while we can afford a week
    balance -= 150                       # spend 150 a week
    weeks += 1                           # count the week
print(f"Lasts {weeks} weeks, {balance} left over")

print("--- 6. break out early ---")
for n in range(1, 1000):
    if n % 7 == 0 and n % 5 == 0:        # first multiple of BOTH 7 and 5
        print(f"First number divisible by 35: {n}")
        break                            # stop; no point checking 36..999
```

Expected output:

```
--- 1. count up ---
0 1 2 3 4 
--- 2. count down ---
5 4 3 2 1 
--- 3. evens only, two ways ---
0 2 4 6 8 10 
0 2 4 6 8 10 
--- 4. accumulate a total ---
1+2+...+10 = 55
--- 5. a while loop with a clear stop ---
Lasts 6 weeks, 100 left over
--- 6. break out early ---
First number divisible by 35: 35
```

Check drill 5 by hand: 1000 ÷ 150 = 6 remainder 100. Six full weeks, 100 rupees left, which is less than 150 so the loop stops ✔

### Part D — Safe input with a `while` loop (20 minutes)

This is the pattern you will reuse in every interactive program you write for the rest of Level 2. Learn it properly.

New file, `safe_input.py`:

```python
# safe_input.py — keep asking until the user gives something usable.

# --- Pattern 1: keep asking until we get a whole number ---
number_text = ""                                   # start with something invalid
while not number_text.isdigit():                   # loop WHILE it's still bad
    number_text = input("Type a whole number: ")
    if not number_text.isdigit():                  # only complain if still bad
        print("  That wasn't a whole number. Try again.")
number = int(number_text)                          # guaranteed safe
print(f"Thanks — you typed {number}, and double it is {number * 2}.")

# --- Pattern 2: keep asking until we get one of a fixed set of answers ---
choice = ""
while choice != "rock" and choice != "paper" and choice != "scissors":
    choice = input("rock, paper, or scissors? ").strip().lower()
    if choice != "rock" and choice != "paper" and choice != "scissors":
        print("  Pick one of the three.")
print(f"You chose {choice}.")

# --- Pattern 3: a replay loop ---
plays = 0
again = "yes"
while again == "yes":
    plays += 1
    print(f"  ...playing round {plays}...")
    again = input("Play again? (yes/no) ").strip().lower()
print(f"You played {plays} rounds. Bye!")
```

Sample run:

```
Type a whole number: seven
  That wasn't a whole number. Try again.
Type a whole number: 7.5
  That wasn't a whole number. Try again.
Type a whole number: 7
Thanks — you typed 7, and double it is 14.
rock, paper, or scissors? Lizard
  Pick one of the three.
rock, paper, or scissors? Rock
You chose rock.
  ...playing round 1...
Play again? (yes/no) yes
  ...playing round 2...
Play again? (yes/no) no
You played 2 rounds. Bye!
```

Notice the shape of the pattern, because it's always the same:

```
   ┌────────────────────────────────────────────┐
   │  1. set the variable to something INVALID  │
   │  2. while it is still invalid:             │
   │  3.     ask again                          │
   │  4.     if still invalid: complain         │
   │  5. now use it, knowing it's good          │
   └────────────────────────────────────────────┘
```

Step 1 is the one people forget. If you don't set `number_text = ""` first, the `while` line crashes with a `NameError` because there's nothing to check yet.

### Part E — Random numbers (10 minutes)

Your guessing game needs a secret number the computer picks. That comes from Python's `random` toolbox.

> **Definition — module:** a file of ready-made Python tools that you bring into your program with `import`.

```python
# random_demo.py — one new tool: random.randint.

import random                       # bring in the random-numbers toolbox

secret = random.randint(1, 100)     # a whole number from 1 to 100, BOTH ends included
print(secret)

for i in range(5):
    print(random.randint(1, 6), end=" ")   # five dice rolls
print()
```

Sample output (yours will differ — that's the point):

```
73
4 2 6 1 3 
```

⚠️ Important difference from `range`: `random.randint(1, 100)` **includes** 100. `range(1, 100)` **excludes** it. Two functions, two different boundary rules. Read the docs, or test it — never assume.

---

## ✍️ Practice

### 1. [Warm-up] Predict the boolean

Write `predict.py`. For each of these ten expressions, put your predicted answer in a comment, then print the real one:

`8 > 3 and 3 > 8` · `8 > 3 or 3 > 8` · `not (8 > 3)` · `"b" > "a"` · `5 % 2 == 1` · `10 // 3 == 3` · `not True and False` · `not (True and False)` · `1 <= 1 <= 1` · `"" == " "`

**Done looks like:** ten lines of output, your prediction in a comment above each, and a final comment saying how many you got right out of ten.

### 2. [Warm-up] FizzBuzz

Write `fizzbuzz.py` that loops from 1 to 30 and prints, on each line:

- `FizzBuzz` if the number is divisible by both 3 and 5,
- `Fizz` if divisible by 3 only,
- `Buzz` if divisible by 5 only,
- otherwise the number itself.

**Done looks like:** exactly 30 lines. Line 15 says `FizzBuzz`, line 9 says `Fizz`, line 10 says `Buzz`, line 7 says `7`. **Warning:** get the order of your conditions right or you'll never see `FizzBuzz`.

### 3. [Build] Times-table grid

Write `tables.py` that prints a full 1–9 multiplication grid using two loops, one inside the other (a **nested loop**), with aligned columns and a header row.

Target output:

```
      1   2   3   4   5   6   7   8   9
   +------------------------------------
 1 |   1   2   3   4   5   6   7   8   9
 2 |   2   4   6   8  10  12  14  16  18
 3 |   3   6   9  12  15  18  21  24  27
 4 |   4   8  12  16  20  24  28  32  36
 5 |   5  10  15  20  25  30  35  40  45
 6 |   6  12  18  24  30  36  42  48  54
 7 |   7  14  21  28  35  42  49  56  63
 8 |   8  16  24  32  40  48  56  64  72
 9 |   9  18  27  36  45  54  63  72  81
```

**Hints:** `print(x, end="")` prints without moving to a new line; a bare `print()` ends the line. `f"{value:>4}"` right-aligns in 4 characters.

**Done looks like:** the grid is aligned exactly, and you used two `for` loops (not nine print statements).

### 4. [Build] Score statistics with validation

Write `score_stats.py` that:

1. asks how many scores will be entered (re-ask until it's a whole number **and** greater than 0),
2. loops that many times, asking for each score, re-asking on non-numeric or out-of-range (0–100) input,
3. reports total, average (2 dp), highest, lowest, count of passes (≥ 35) and count of fails.

**Done looks like:** running it with 5, then typing `abc`, `150`, `-4`, `72`, `88`, `31`, `95`, `60` produces total 346, average 69.20, highest 95, lowest 31, passes 4, fails 1 — with three complaint messages and zero tracebacks.

### 5. [Stretch] The collatz staircase

Pick any positive whole number. If it's even, halve it. If it's odd, triple it and add 1. Repeat. It always seems to reach 1 eventually — nobody has proved why. This is the **Collatz conjecture**, an unsolved maths problem you can explore with a `while` loop.

Write `collatz.py` that asks for a starting number and prints the whole chain, then reports how many steps it took and the highest value reached along the way.

For 27 the chain is famously long — 111 steps, peaking at 9232.

**Done looks like:** for input `6` it prints `6 3 10 5 16 8 4 2 1` and reports 8 steps, peak 16. For input `27` it reports 111 steps and peak 9232. Add a safety valve: `break` if steps exceed 1000, so a bug can't hang your machine.

### 6. [Stretch] Find the bug and prove it

Below is a program meant to count how many students passed a 40-mark test. It has **three** bugs — one logic bug, one off-by-one bug, and one that only shows up for a particular input.

```python
marks = [38, 12, 40, 5, 22, 40, 0]
passed = 0
i = 0
while i <= len(marks):
    if marks[i] > 20:
        passed = passed + 1
    i = i + 1
print("Passed:", passed / len(marks) * 100, "%")
```

(`len(marks)` gives the number of items — 7 here. `marks[i]` gets the item at position `i`, counting from 0. You'll meet both properly in Module 3.)

For each bug, write: what goes wrong, which line, and the fix. Then write a corrected version that reports "4 of 7 students passed (57.1%)" — assuming the pass mark is 20 **or above**.

**Done looks like:** a three-row table of bugs, and a fixed program whose output you verified by counting the marks by hand.

---

## 🤔 Think Deeper

### 1. Your `ticket_price.py` decides who pays what based on a single number — age. What happens when a rule that looks perfectly fair as an `if/elif` chain meets a person it wasn't designed for?

*How to reason about it:* List five real people who would be badly served by the cinema chain — someone who turned 13 yesterday, someone whose ID says one age and whose life says another, a 59-year-old on a pension, a carer accompanying a disabled child. For each, ask: is the problem the *code*, the *rule*, or the *fact that a rule has to be a small number of boxes*? Then notice that the model you trained in Level 1 was also a rule made of boxes — it just found its own boundaries instead of you typing them. Which is easier to argue with?

### 2. A `while` loop that never ends will run until you kill it. Should Python protect you by refusing to run loops it thinks might be infinite?

*How to reason about it:* First, try to write the rule Python would need: "stop if the condition variable doesn't change." Now try to break your own rule — write a loop that legitimately runs for hours without any variable changing in an obvious way (a web server, a game loop, a program waiting for a sensor). Then look up "the halting problem" and notice that this exact question was proved *unanswerable* in 1936, before computers existed. What does it tell you that a practical annoyance turns out to be a deep mathematical limit?

### 3. `break` lets you jump out of a loop from the middle. Some programmers say `break` and `continue` make code harder to read and should be avoided. Others say banning them creates worse code. Who is right?

*How to reason about it:* Take your Practice 5 Collatz program and rewrite the safety valve without `break` — you'll need to add a condition to the `while` line. Compare the two versions. Which one makes the *main* stopping rule easier to see? Now do the same for a search loop that stops at the first match. Notice that the answer may be different for the two cases, and that "always" and "never" are usually the wrong shape of answer in programming.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `IndentationError: expected an indented block` | You wrote `if x > 5:` and then didn't indent the next line | Every line after a `:` that belongs inside must be indented (4 spaces). Your editor does this on Enter — don't fight it |
| `if x = 5:` → `SyntaxError` | Confusing "gets" with "equals" | `=` assigns, `==` compares. In an `if`, you almost always want `==` |
| Grade chain gives everyone a D | Conditions ordered least-restrictive first, so the loosest one catches everybody | Order `elif` chains from **most** restrictive to **least** (highest threshold first) |
| `if answer == "yes" or "y":` always runs | You wrote a comparison on the left of `or` and a bare string on the right | Write both sides in full: `answer == "yes" or answer == "y"` |
| `range(1, 10)` gives 1–9, not 1–10 | Forgetting that `range` stops **before** the end value | Use `range(1, 11)`. Say "stops before" every time you type it |
| Loop prints forever | A `while` whose condition variable never changes inside the loop | Press **Ctrl-C** to stop, then find the missing `+= 1` or `-= 1` |
| `while count < 3` runs 4 times | Used `<=` when you meant `<`, or started the counter at 1 instead of 0 | Trace the first and last two passes in a table before running |
| Accumulator reset inside the loop | `total = 0` accidentally placed inside the loop body | The accumulator's setup line goes **before** the loop, always |
| `NameError` on the `while` line | Checking a variable that hasn't been created yet | Set it to an obviously-invalid starting value before the loop |
| Comparing user input fails on `"Yes"` | Case and stray spaces | Normalise every text input: `input(...).strip().lower()` |
| `.isdigit()` rejects `-5` and `3.5` | It only accepts characters 0-9 | That's often what you want. For decimals or negatives you need a different check — or wait for Module 3 tools |

---

## 🛠️ Mini-Project: Guess & Grade

**Time: 75–90 minutes**

Two programs in one folder. Both must survive a user who types garbage.

---

### Part 1 — `guess.py`: the number-guessing game

#### Goal

The computer picks a secret whole number from 1 to 100. The player gets **7 attempts**. After each wrong guess, the program says "higher" or "lower" and how many attempts remain. When the game ends — win or lose — it offers a replay.

Why 7 attempts? Because with perfect halving you can always find a number in 1–100 in 7 guesses: 100 → 50 → 25 → 13 → 7 → 4 → 2 → 1. That's the **binary search** idea, and it's why 7 is exactly fair.

#### Starter steps

1. `import random` at the top.
2. Write the outer replay loop first: `playing = True` … `while playing:` … at the end ask "again?" and set `playing = False` if not.
3. Inside, pick the secret and set `attempts_used = 0` and `won = False`.
4. Write the inner loop: `while attempts_used < 7 and not won:`
5. Inside that: get input as text, guard with `.isdigit()`, `continue` if bad (**do not** count a bad input as an attempt).
6. Convert, increment `attempts_used`, compare with `==`, `<`, `>`, print the hint.
7. After the inner loop, print win or lose. On a loss, reveal the number.

#### Reference implementation

```python
# guess.py — guess the secret number in 7 tries, with a replay loop.

import random                                # for random.randint

LOW = 1                                      # smallest possible secret
HIGH = 100                                   # largest possible secret
MAX_ATTEMPTS = 7                             # 7 is enough if you halve each time

print("=" * 42)
print("  GUESS THE NUMBER")
print(f"  I'm thinking of a number {LOW}-{HIGH}.")
print(f"  You get {MAX_ATTEMPTS} tries.")
print("=" * 42)

wins = 0                                     # accumulator across all games
games = 0                                    # accumulator across all games
playing = True                               # controls the replay loop

while playing:                               # ---- one pass = one full game ----
    secret = random.randint(LOW, HIGH)       # both ends included
    attempts_used = 0                        # counter, reset every game
    won = False                              # flag: did they get it this game?
    games += 1

    print(f"\n--- Game {games} ---")

    # Inner loop: keep going while tries remain AND they haven't won.
    while attempts_used < MAX_ATTEMPTS and not won:
        remaining = MAX_ATTEMPTS - attempts_used
        guess_text = input(f"Guess ({remaining} left): ").strip()

        # Guard 1: must be all digits.
        if not guess_text.isdigit():
            print("  Whole numbers only, please. (That try was free.)")
            continue                          # skip the rest; do NOT count it

        guess = int(guess_text)               # safe: we know it's digits

        # Guard 2: must be in range.
        if guess < LOW or guess > HIGH:
            print(f"  Stay between {LOW} and {HIGH}. (That try was free.)")
            continue

        attempts_used += 1                    # only real guesses cost a try

        if guess == secret:
            won = True                        # ends the inner loop
        elif guess < secret:
            print("  Higher ⬆")
        else:
            print("  Lower ⬇")

    # ---- game over: report ----
    if won:
        wins += 1
        if attempts_used == 1:
            print("✅ Got it in 1 try. Suspicious.")
        else:
            print(f"✅ Got it in {attempts_used} tries. The number was {secret}.")
    else:
        print(f"❌ Out of tries. The number was {secret}.")

    print(f"Record: {wins} won / {games} played")

    # ---- replay prompt, itself validated ----
    answer = ""
    while answer != "yes" and answer != "no" and answer != "y" and answer != "n":
        answer = input("Play again? (yes/no) ").strip().lower()
        if answer != "yes" and answer != "no" and answer != "y" and answer != "n":
            print("  Please answer yes or no.")

    if answer == "no" or answer == "n":
        playing = False                       # ends the outer loop

print(f"\nFinal record: {wins} of {games}. Thanks for playing.")
```

Sample run:

```
==========================================
  GUESS THE NUMBER
  I'm thinking of a number 1-100.
  You get 7 tries.
==========================================

--- Game 1 ---
Guess (7 left): fifty
  Whole numbers only, please. (That try was free.)
Guess (7 left): 500
  Stay between 1 and 100. (That try was free.)
Guess (7 left): 50
  Lower ⬇
Guess (6 left): 25
  Higher ⬆
Guess (5 left): 37
  Higher ⬆
Guess (4 left): 43
  Lower ⬇
Guess (3 left): 40
✅ Got it in 5 tries. The number was 40.
Record: 1 won / 1 played
Play again? (yes/no) no

Final record: 1 of 1. Thanks for playing.
```

---

### Part 2 — `grade.py`: the grade calculator

#### Goal

Ask how many scores there are, read that many scores with validation, then report total, average, highest, lowest, and a letter grade for the average.

#### Reference implementation

```python
# grade.py — read N validated scores and report statistics plus a letter grade.

print("=" * 42)
print("  GRADE CALCULATOR")
print("=" * 42)

# ---- Step 1: how many scores? Must be a whole number, at least 1. ----
count_text = ""
while not count_text.isdigit() or int(count_text) < 1:
    count_text = input("How many scores? ").strip()
    if not count_text.isdigit():
        print("  Type a whole number.")
    elif int(count_text) < 1:
        print("  Need at least 1 score.")
count = int(count_text)

# ---- Step 2: accumulators, set up BEFORE the loop ----
total = 0            # running sum
highest = -1         # below any valid score, so the first score always wins
lowest = 101         # above any valid score, so the first score always wins
passes = 0           # counter for scores >= 35

# ---- Step 3: read exactly `count` scores, re-asking on bad input ----
for i in range(count):                              # i goes 0..count-1
    score_text = ""
    valid = False
    while not valid:
        score_text = input(f"  Score {i + 1} of {count}: ").strip()
        if not score_text.isdigit():
            print("    Whole numbers only (0-100).")
        elif int(score_text) > 100:
            print("    Max is 100.")
        else:
            valid = True                            # ends the validation loop

    score = int(score_text)

    total += score                                  # accumulate
    if score > highest:
        highest = score
    if score < lowest:
        lowest = score
    if score >= 35:
        passes += 1

# ---- Step 4: derived numbers ----
average = total / count
fails = count - passes

# ---- Step 5: letter grade — MOST restrictive condition first ----
if average >= 90:
    letter = "A"
elif average >= 75:
    letter = "B"
elif average >= 60:
    letter = "C"
elif average >= 35:
    letter = "D"
else:
    letter = "F"

# ---- Step 6: report ----
print("-" * 42)
print(f"  Scores entered : {count}")
print(f"  Total          : {total}")
print(f"  Average        : {average:.2f}")
print(f"  Highest        : {highest}")
print(f"  Lowest         : {lowest}")
print(f"  Passed (>=35)  : {passes}")
print(f"  Failed         : {fails}")
print(f"  Letter grade   : {letter}")
print("-" * 42)
```

Sample run:

```
==========================================
  GRADE CALCULATOR
==========================================
How many scores? five
  Type a whole number.
How many scores? 4
  Score 1 of 4: 88
  Score 2 of 4: 120
    Max is 100.
  Score 2 of 4: 92
  Score 3 of 4: seventy
    Whole numbers only (0-100).
  Score 3 of 4: 70
  Score 4 of 4: 30
------------------------------------------
  Scores entered : 4
  Total          : 280
  Average        : 70.00
  Highest        : 92
  Lowest         : 30
  Passed (>=35)  : 3
  Failed         : 1
  Letter grade   : C
------------------------------------------
```

Check by hand: 88 + 92 + 70 + 30 = 280 ✔. 280 ÷ 4 = 70.00 ✔. Highest 92, lowest 30 ✔. Three scores ≥ 35 (88, 92, 70), one below (30) ✔. Average 70 → not ≥ 90, not ≥ 75, but ≥ 60 → **C** ✔

---

### Success criteria checklist

- [ ] `guess.py` runs, picks a different number each game, and never crashes
- [ ] Typing `abc`, `-5`, `0`, or `500` produces a clear message, not a traceback
- [ ] A rejected input does **not** consume one of the 7 attempts
- [ ] "Higher"/"Lower" hints are correct (check: if secret is 40 and you guess 25, it must say higher)
- [ ] The replay loop works, and answering `no` exits cleanly
- [ ] `grade.py` re-asks on bad input and on out-of-range input, indefinitely
- [ ] All five statistics are correct, verified by hand on a 4-score run
- [ ] The letter grade chain is ordered highest-threshold-first
- [ ] Every accumulator is initialised **before** its loop
- [ ] Every loop's stopping condition is one you can explain out loud

### 🚀 Level it up

**Extension for `guess.py`:** add a difficulty menu before each game — Easy (1–50, 8 tries), Normal (1–100, 7 tries), Hard (1–1000, 10 tries). Then add a **"warmer/colder"** hint: track the distance from the previous guess and say `🔥 warmer` or `🧊 colder`. (First guess has no previous, so handle that case.)

**Extension for `grade.py`:** after the report, print a text histogram — one row per score, with a bar made of `#` characters scaled so 100 marks = 40 characters:

```
   88 | ###################################
   92 | #####################################
   70 | ############################
   30 | ############
```

**Hint:** `bar_length = int(score / 100 * 40)` then `print(f"{score:>5} | {'#' * bar_length}")`.

**Real challenge:** make `grade.py` reject a score typed as `85.5` with a helpful message ("whole numbers only — round it first"), rather than silently rejecting it as "not digits". The user should be able to tell *why* their input was refused.

---

## 🔑 Key Takeaways

- **Every decision is a boolean.** Comparisons (`==`, `<`, `>=`) produce `True`/`False`; `and`, `or`, `not` combine them.
- **`elif` chains guarantee exactly one branch runs** — and every `elif` silently means "and none of the above."
- **Order matters enormously.** Put the most restrictive condition first, or the loosest one swallows everything.
- **Use `for` when you know the count, `while` when you don't.** And `range(n)` stops *before* `n`.
- **Every `while` loop needs three parts:** set up, check, and change. Missing the change gives you an infinite loop — Ctrl-C is your rescue.
- **The accumulator pattern is universal:** initialise before the loop, update inside it, use after it. Totals, counters, and maximums are all the same shape.
- **Trace loops on paper before running.** A five-row table beats an hour of staring.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Boolean** | A value that is either `True` or `False`, nothing else | `is_raining = True` |
| **Comparison operator** | A symbol that asks a yes/no question about two values | `age >= 13` |
| **`==` vs `=`** | `==` asks "same?"; `=` puts a value into a name | `if x == 5:` vs `x = 5` |
| **Condition** | The boolean expression an `if` or `while` checks | `mark >= 35` |
| **Block** | Lines that belong together, marked by matching indentation | the indented lines under an `if` |
| **Indentation** | The spaces at the start of a line — in Python this is real syntax | 4 spaces per level |
| **`if` / `elif` / `else`** | Choose exactly one path out of several | grade chains |
| **`and`** | True only when both sides are true | `age >= 13 and fit` |
| **`or`** | True when at least one side is true | `day == "sat" or day == "sun"` |
| **`not`** | Flips true to false and back | `not injured` |
| **Chained comparison** | Writing a range the way maths does | `60 <= mark < 75` |
| **Loop** | A block of code that repeats | `for`, `while` |
| **`for` loop** | Repeat once per item, a known number of times | `for i in range(10):` |
| **`range()`** | Generates a run of numbers; stops **before** the end value | `range(1, 11)` → 1..10 |
| **`while` loop** | Repeat as long as a condition stays true | `while lives > 0:` |
| **Infinite loop** | A loop whose condition never becomes false | fix it, or press Ctrl-C |
| **Accumulator** | A variable built up across a loop's passes | `total += score` |
| **Counter** | An accumulator that counts how many times something happened | `passes += 1` |
| **Augmented assignment** | `+=`, `-=`, `*=` — update a variable from itself | `count += 1` |
| **`break`** | Leave the whole loop right now | stop at the first match |
| **`continue`** | Skip the rest of this pass, go to the next | ignore bad input |
| **Off-by-one bug** | A loop that runs one time too many or too few | `range(1,10)` when you meant 1–10 |
| **Flag** | A boolean variable used to remember that something happened | `won = True` |
| **Nested loop** | A loop inside another loop | a multiplication grid |
| **Module** | A file of ready-made tools you `import` | `import random` |
| **Method** | A function attached to a value, called with a dot | `text.strip()`, `text.lower()` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### Practice 1 — Predict the boolean

```python
# predict.py — guess first, then check.

# guess: False  (3 > 8 is False, and needs both)
print(8 > 3 and 3 > 8)          # False

# guess: True   (8 > 3 is True, or needs only one)
print(8 > 3 or 3 > 8)           # True

# guess: False  (8 > 3 is True, not flips it)
print(not (8 > 3))              # False

# guess: True   (b comes after a alphabetically)
print("b" > "a")                # True

# guess: True   (5 % 2 is 1, and 1 == 1)
print(5 % 2 == 1)               # True

# guess: True   (10 // 3 is 3, throwing away the .333)
print(10 // 3 == 3)             # True

# guess: False  (not binds tighter than and: (not True) and False = False and False)
print(not True and False)       # False

# guess: True   (brackets first: True and False = False, then not False = True)
print(not (True and False))     # True

# guess: True   (chained: 1<=1 and 1<=1)
print(1 <= 1 <= 1)              # True

# guess: False  (empty string is not the same as a string containing one space)
print("" == " ")                # False

# I got __ out of 10.
```

Output:

```
False
True
False
True
True
True
False
True
True
False
```

**The two worth staring at:** `not True and False` versus `not (True and False)`. Same words, different brackets, opposite answers. `not` binds tighter than `and`, so the first one is `(not True) and False`. When in doubt, add brackets.

---

### Practice 2 — FizzBuzz

```python
# fizzbuzz.py — the classic. Order of conditions is everything.

for n in range(1, 31):                        # 1..30 (stops before 31)
    if n % 3 == 0 and n % 5 == 0:             # MOST restrictive first!
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
```

Output:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
Fizz
22
23
Fizz
Buzz
26
Fizz
28
29
FizzBuzz
```

**Why the order matters:** if you test `n % 3 == 0` first, then 15 prints `Fizz` and you never see `FizzBuzz` at all. The "both" case is the most restrictive — fewest numbers satisfy it — so it goes first. Only 15 and 30 reach it in this range.

**An alternative that avoids the ordering trap** (worth understanding, though the version above is clearer):

```python
for n in range(1, 31):
    output = ""                     # accumulate a string instead of branching
    if n % 3 == 0:
        output += "Fizz"
    if n % 5 == 0:
        output += "Buzz"
    if output == "":                # neither applied
        output = str(n)
    print(output)
```

Same output. Here the accumulator is a *string*, which is a nice reminder that `+=` works on strings too.

---

### Practice 3 — Times-table grid

```python
# tables.py — a 9x9 multiplication grid with two nested loops.

# --- header row: the column numbers ---
print("   ", end="")                       # 3 spaces to clear the row-label column
for col in range(1, 10):                   # 1..9
    print(f"{col:>4}", end="")             # each column is 4 characters wide
print()                                    # end the header line

# --- separator line ---
print("   +" + "-" * 36)                   # 9 columns x 4 chars = 36 dashes

# --- one line per row ---
for row in range(1, 10):                   # OUTER loop: rows 1..9
    print(f"{row:>2} |", end="")           # row label, then the bar
    for col in range(1, 10):               # INNER loop: columns 1..9
        print(f"{row * col:>4}", end="")   # the product, right-aligned in 4
    print()                                # end this row's line
```

Output:

```
      1   2   3   4   5   6   7   8   9
   +------------------------------------
 1 |   1   2   3   4   5   6   7   8   9
 2 |   2   4   6   8  10  12  14  16  18
 3 |   3   6   9  12  15  18  21  24  27
 4 |   4   8  12  16  20  24  28  32  36
 5 |   5  10  15  20  25  30  35  40  45
 6 |   6  12  18  24  30  36  42  48  54
 7 |   7  14  21  28  35  42  49  56  63
 8 |   8  16  24  32  40  48  56  64  72
 9 |   9  18  27  36  45  54  63  72  81
```

**How the nesting works:** the outer loop runs 9 times. For *each* of those, the inner loop runs 9 times. Total: 9 × 9 = 81 products printed. The `print()` with no arguments after the inner loop is what moves to the next line — leave it out and you get one enormous line.

**The `end=""` trick:** by default `print` adds a newline. `end=""` says "add nothing," so the next print continues on the same line. This is how you build a line piece by piece.

---

### Practice 4 — Score statistics with validation

```python
# score_stats.py — read N validated scores and report six statistics.

# --- Ask how many, re-asking until it's a whole number > 0 ---
count_text = ""
while not count_text.isdigit() or int(count_text) == 0:
    count_text = input("How many scores? ").strip()
    if not count_text.isdigit():
        print("  Whole numbers only.")
    elif int(count_text) == 0:
        print("  Need at least one score.")
count = int(count_text)

# --- Accumulators, set up BEFORE the loop ---
total = 0
highest = -1          # below every valid score
lowest = 101          # above every valid score
passes = 0

# --- Read exactly `count` valid scores ---
for i in range(count):                                  # i = 0..count-1
    score_text = ""
    ok = False
    while not ok:
        score_text = input(f"Score {i + 1}: ").strip()
        if not score_text.isdigit():
            print("  Not a whole number — try again.")
        elif int(score_text) > 100:
            print("  Scores go up to 100 — try again.")
        else:
            ok = True                                   # .isdigit() already blocks "-4"

    score = int(score_text)
    total += score
    if score > highest:
        highest = score
    if score < lowest:
        lowest = score
    if score >= 35:
        passes += 1

# --- Report ---
average = total / count
print("-" * 34)
print(f"Count   : {count}")
print(f"Total   : {total}")
print(f"Average : {average:.2f}")
print(f"Highest : {highest}")
print(f"Lowest  : {lowest}")
print(f"Passes  : {passes}")
print(f"Fails   : {count - passes}")
```

Run with `5`, then `abc`, `150`, `-4`, `72`, `88`, `31`, `95`, `60`:

```
How many scores? 5
Score 1: abc
  Not a whole number — try again.
Score 1: 150
  Scores go up to 100 — try again.
Score 1: -4
  Not a whole number — try again.
Score 1: 72
Score 2: 88
Score 3: 31
Score 4: 95
Score 5: 60
----------------------------------
Count   : 5
Total   : 346
Average : 69.20
Highest : 95
Lowest  : 31
Passes  : 4
Fails   : 1
```

Check by hand: 72 + 88 = 160. +31 = 191. +95 = 286. +60 = **346** ✔. 346 ÷ 5 = **69.2** ✔. Highest 95, lowest 31 ✔. Scores ≥ 35: 72, 88, 95, 60 = **4** ✔.

**Note on `-4`:** `.isdigit()` returns `False` for `"-4"` because the minus sign isn't a digit. So it's caught by the first branch, with a slightly imprecise message. That's the limitation flagged in Common Mistakes — good enough here, but worth knowing.

---

### Practice 5 — The Collatz staircase

```python
# collatz.py — the unsolved 3n+1 problem, explored with a while loop.

n_text = ""
while not n_text.isdigit() or int(n_text) < 1:
    n_text = input("Starting number (1 or more): ").strip()
    if not n_text.isdigit() or int(n_text) < 1:
        print("  Need a whole number of at least 1.")
n = int(n_text)

start = n                     # remember it for the report
steps = 0                     # counter
peak = n                      # accumulator: highest value seen
SAFETY = 1000                 # safety valve so a bug can't hang the machine

print(f"{n}", end="")

while n != 1 and steps < SAFETY:      # stop at 1, or bail out if something's wrong
    if n % 2 == 0:
        n = n // 2                    # even: halve it (// keeps it an int)
    else:
        n = 3 * n + 1                 # odd: triple and add one

    steps += 1
    if n > peak:
        peak = n
    print(f" {n}", end="")

print()                               # end the chain line

if steps >= SAFETY:
    print(f"Gave up after {SAFETY} steps — something is wrong.")
else:
    print(f"Start {start}: reached 1 in {steps} steps, peaking at {peak}.")
```

Run with `6`:

```
Starting number (1 or more): 6
6 3 10 5 16 8 4 2 1
Start 6: reached 1 in 8 steps, peaking at 16.
```

Trace it by hand: 6 is even → 3. 3 is odd → 10. 10 even → 5. 5 odd → 16. 16 → 8 → 4 → 2 → 1. That's 8 arrows, so 8 steps ✔. Highest value along the way is 16 ✔.

Run with `27` (the chain is long, so only the summary is shown here):

```
Start 27: reached 1 in 111 steps, peaking at 9232.
```

**Why `//` and not `/`:** `6 / 2` gives `3.0`, a float. Then `3.0 % 2` still works, but you'd print `3.0 10.0 5.0` — ugly, and floats eventually lose precision on huge numbers. `//` keeps everything an integer.

**Why the safety valve:** you're implementing an *unproven* conjecture. Nobody has proved every number reaches 1. If you found a counterexample you'd be famous — but far more likely, you'd have a typo. The `steps < SAFETY` condition means a typo costs you one second instead of a frozen terminal.

---

### Practice 6 — Find the bug and prove it

**The bug table:**

| # | Bug type | Line | What goes wrong | Fix |
|---|---|---|---|---|
| 1 | Off-by-one | 4 | `while i <= len(marks)` runs with `i = 7`, but the last valid position is 6. Crashes with `IndexError: list index out of range` | `while i < len(marks):` |
| 2 | Logic | 5 | `marks[i] > 20` means "more than 20", so a mark of exactly 20 doesn't count. The spec says 20 **or above** | `if marks[i] >= 20:` |
| 3 | Reporting | 8 | It prints a percentage, not "4 of 7". Also `4 / 7 * 100 = 57.14285714285714` — unformatted, ugly | Print both the count and a formatted percentage |

**Bug 1 in detail.** `marks` has 7 items at positions 0,1,2,3,4,5,6. `len(marks)` is 7. The condition `i <= 7` lets the loop run with `i = 7`, and `marks[7]` doesn't exist:

```
Traceback (most recent call last):
  File "buggy.py", line 5, in <module>
    if marks[i] > 20:
IndexError: list index out of range
```

This is the classic off-by-one: **the number of items and the last valid index differ by one.**

**Bug 3, the "only shows up for a particular input" one.** If `marks` were empty, `len(marks)` would be 0 and line 8 would be a `ZeroDivisionError`. Worth guarding.

**Corrected version:**

```python
# passes_fixed.py — count how many students scored 20 or above.

marks = [38, 12, 40, 5, 22, 40, 0]      # 7 students

passed = 0                               # counter
i = 0                                    # index, starts at 0

while i < len(marks):                    # FIX 1: < not <=
    if marks[i] >= 20:                   # FIX 2: >= not >
        passed += 1
    i += 1

if len(marks) == 0:                      # FIX 3a: guard against divide-by-zero
    print("No marks to report.")
else:
    percent = passed / len(marks) * 100
    print(f"{passed} of {len(marks)} students passed ({percent:.1f}%)")
```

Output:

```
4 of 7 students passed (57.1%)
```

Count by hand: 38 ✔, 12 ✗, 40 ✔, 5 ✗, 22 ✔, 40 ✔, 0 ✗. That's **4 out of 7** ✔. 4 ÷ 7 = 0.5714... × 100 = 57.14... → `57.1%` ✔

**A cleaner rewrite** using a `for` loop, which sidesteps the whole index problem:

```python
marks = [38, 12, 40, 5, 22, 40, 0]

passed = 0
for mark in marks:                       # no index at all -> no off-by-one possible
    if mark >= 20:
        passed += 1

print(f"{passed} of {len(marks)} students passed ({passed / len(marks) * 100:.1f}%)")
```

Output:

```
4 of 7 students passed (57.1%)
```

**The lesson:** when you loop over items and don't need their positions, loop over the items directly. An index you never write is an index you can never get wrong. You'll do a lot more of this in Module 3.

</details>

---

[⬅ Previous](module-01-python-from-zero.md) · [Level 2 Home](README.md) · [Next ➡](module-03-functions-and-lists.md)
