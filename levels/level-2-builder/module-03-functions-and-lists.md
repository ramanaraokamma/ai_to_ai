# Module 3 — Functions and Lists: Building Your Own Tools

**Level 2 · Module 3 · ~3.5 hours · Prereqs: Modules 1–2 (variables, types, f-strings, if/elif/else, for and while loops, accumulators)**

[⬅ Previous](module-02-decisions-and-loops.md) · [Level 2 Home](README.md) · [Next ➡](module-04-dictionaries-and-datasets.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** define a function with parameters and a return value, and call it from another file.
2. **You will be able to** explain the difference between *printing* a value and *returning* one — and say why returning is almost always what you want.
3. **You will be able to** create, index, slice, append to, sort, and loop over a list.
4. **You will be able to** write a list comprehension and say what the equivalent `for` loop would be.
5. **You will be able to** split a program across two files and `import` your own module.

---

## 🪝 The Hook

Look back at your Module 2 mini-project. In `grade.py` you wrote a validation loop to read one number safely. Then in `guess.py` you wrote *almost the same loop again*. Then again for the replay prompt. Three near-identical blocks, each slightly different, each independently able to be wrong.

Now imagine you find a bug in that validation logic. You have to fix it in three places. Miss one, and your program is broken in a way that only shows up on Tuesdays.

There is a second problem hiding in the same project. `grade.py` read five scores — but it never *kept* them. It added each one to a total and threw it away. Want the median? Want to sort them? Want to print them again at the end? Too late. They're gone.

This module fixes both. A **function** lets you write a piece of logic once, name it, and use it everywhere. A **list** lets you hold many values in one variable instead of throwing them away. Together they are how every real program is built — including every line of pandas and scikit-learn you'll write later in this level.

---

## 🧠 The Concept

### 1. `def`, parameters vs arguments, `return`, and default values

#### The plain-language explanation

A **function** is a named block of code you write once and run whenever you like.

> **Definition — function:** a named, reusable block of code that optionally takes inputs and optionally hands back a result.

You have already *used* functions: `print()`, `int()`, `input()`, `len()`, `range()`. Those came with Python. Now you write your own with `def`.

```python
def greet():                       # def NAME() : starts the definition
    print("Hello!")                # indented = the function's body
    print("Nice to meet you.")

greet()                            # this is a CALL — it actually runs the body
greet()                            # call it again — same code, no retyping
```

Output:

```
Hello!
Nice to meet you.
Hello!
Nice to meet you.
```

Two separate things happen here, and mixing them up is the classic beginner confusion:

```
   DEFINING                          CALLING
   def greet():                      greet()
   "Here is a recipe named greet."   "Cook the recipe named greet, now."
   Nothing runs.                     The body runs.
   Happens once.                     Happens as often as you like.
```

If you define a function and never call it, **nothing happens**. That's not a bug — that's the point.

#### Parameters and arguments

A function gets much more useful when you can hand it different values each time.

> **Definition — parameter:** a name in the function's definition that stands for a value it will receive.
>
> **Definition — argument:** the actual value you hand over when you call it.

```python
def greet(name):                   # `name` is the PARAMETER
    print(f"Hello, {name}!")

greet("Ramana")                    # "Ramana" is the ARGUMENT
greet("Anu")
```

Output:

```
Hello, Ramana!
Hello, Anu!
```

The memory hook: **P**arameter is in the definition (**P** for "placeholder"). **A**rgument is what you **a**ctually pass.

#### `return`: the thing that makes functions powerful

`print()` shows something on screen. `return` hands a value **back to the code that called the function**, so it can be used.

> **Definition — `return`:** immediately ends the function and sends a value back to whoever called it.

```python
def double(n):
    return n * 2                   # send the answer back

result = double(21)                # result now holds 42
print(result)
print(double(5) + double(10))      # 10 + 20 — you can use returned values in maths
```

Output:

```
42
30
```

Now compare with a printing version:

```python
def double_print(n):
    print(n * 2)                   # shows it, but hands back nothing

result = double_print(21)          # prints 42... and result gets NOTHING
print(result)
print(double_print(5) + double_print(10))     # this will crash
```

Output:

```
42
None
10
20
Traceback (most recent call last):
  File "demo.py", line 7, in <module>
    print(double_print(5) + double_print(10))
TypeError: unsupported operand type(s) for +: 'NoneType' and 'NoneType'
```

> **Definition — `None`:** Python's word for "no value at all." A function with no `return` gives back `None`.

#### 🍕 The analogy

This is *the* distinction to get right, so here's the anchor:

- **A function that prints is a waiter who shouts your order across the restaurant.** Everyone hears it. Nobody can eat it.
- **A function that returns is a waiter who brings the plate to your table.** Now you can eat it, share it, weigh it, or take a photo.

You can always print a returned value: `print(double(21))`. You can *never* recover a printed value. **So: return by default. Print only at the very edge of your program, where a human is actually reading.**

```
   ┌──────────────┐   returns 42    ┌──────────────┐
   │  double(21)  │ ──────────────► │  your code   │ ──► store it, add it,
   └──────────────┘                 └──────────────┘     print it, whatever
                                          ✅ useful

   ┌──────────────┐   prints 42     ┌──────────────┐
   │ double_pr(21)│ ─────► screen   │  your code   │ ──► gets None
   └──────────────┘                 └──────────────┘
                                          ❌ dead end
```

#### `return` ends the function immediately

```python
def grade(mark):
    if mark >= 90:
        return "A"                 # returns AND exits — nothing below runs
    if mark >= 75:
        return "B"
    if mark >= 60:
        return "C"
    if mark >= 35:
        return "D"
    return "F"                     # only reached if all the ifs failed

print(grade(92), grade(80), grade(60), grade(35), grade(12))
```

Output:

```
A B C D F
```

Notice: because `return` exits, you don't even need `elif` here. Each `return` makes the ones below unreachable for that call. Both styles are fine; this one is common in real code.

#### Multiple parameters and default values

```python
def rectangle_area(length, width):        # two parameters, in order
    return length * width

print(rectangle_area(12.5, 4))            # 12.5 * 4 = 50.0
```

Output:

```
50.0
```

> **Definition — default value:** a value a parameter takes if the caller doesn't supply one.

```python
def price_with_tax(price, tax_percent=18):    # tax_percent has a default
    return price * (1 + tax_percent / 100)

print(price_with_tax(1000))                   # uses the default 18
print(price_with_tax(1000, 5))                # overrides it with 5
print(price_with_tax(price=1000, tax_percent=0))   # naming arguments is allowed
```

Output:

```
1180.0
1050.0
1000.0
```

Check by hand: 1000 × 1.18 = 1180 ✔. 1000 × 1.05 = 1050 ✔. 1000 × 1.00 = 1000 ✔

Two rules about defaults:
- Parameters **with** defaults must come **after** parameters without. `def f(a=1, b)` is a `SyntaxError`.
- Naming arguments at the call site (`tax_percent=0`) makes long calls readable and lets you skip the order.

#### Docstrings

> **Definition — docstring:** a string on the first line of a function's body that explains what it does.

```python
def value_range(numbers):
    """Return the difference between the largest and smallest number."""
    return max(numbers) - min(numbers)

print(value_range([3, 9, 1, 7]))       # 9 - 1 = 8
print(value_range.__doc__)             # Python stores the docstring for you
```

Output:

```
8
Return the difference between the largest and smallest number.
```

Write one for every function. It takes four seconds and it is the difference between a toolkit and a pile of code.

---

### 2. Scope: what a function can and cannot see

#### The plain-language explanation

> **Definition — scope:** the region of a program where a particular name exists.

Variables created **inside** a function live only inside it. When the function ends, they're gone. This is deliberate, and it's what makes functions safe to reuse.

```python
def compute():
    secret = 99                    # created inside — LOCAL to compute()
    return secret * 2

print(compute())
print(secret)                      # this will fail
```

Output:

```
198
Traceback (most recent call last):
  File "demo.py", line 6, in <module>
    print(secret)
NameError: name 'secret' is not defined
```

The other direction usually works — a function *can* read a variable created outside it:

```python
PASS_MARK = 35                     # created outside — GLOBAL

def has_passed(mark):
    return mark >= PASS_MARK       # reading the global is fine

print(has_passed(40))
print(has_passed(30))
```

Output:

```
True
False
```

But **assigning** to it inside the function creates a brand-new local variable that shadows the global:

```python
count = 0

def add_one():
    count = count + 1              # Python sees an assignment -> treats count as local
    return count

print(add_one())
```

Output:

```
Traceback (most recent call last):
  File "demo.py", line 5, in <module>
    print(add_one())
  File "demo.py", line 4, in add_one
    count = count + 1
UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

Python decided `count` was local (because you assign to it), then found you were reading it before assigning. The fix is *not* to reach for the `global` keyword — it's to pass the value in and return the new one:

```python
count = 0

def add_one(current):
    return current + 1             # takes a value, gives a value, touches nothing outside

count = add_one(count)
count = add_one(count)
print(count)
```

Output:

```
2
```

#### 🍕 The analogy

A function is a **kitchen with a serving hatch**. Ingredients go in through the hatch (parameters). A finished dish comes out through the hatch (return). What happens inside — the mess, the half-chopped onions, the local variables — is invisible from the dining room, and it's cleared away when service ends.

A function that reaches out and rearranges the dining room while cooking is a function nobody can trust. Two people calling it get different results depending on what happened earlier. **Take inputs, give an output, change nothing else** — that habit will save you more debugging hours than anything else in this level.

#### The tiny concrete example

```python
x = "outside"

def show():
    x = "inside"                   # a NEW local x; the outer one is untouched
    print(f"in the function : {x}")

show()
print(f"after the function: {x}")
```

Output:

```
in the function : inside
after the function: outside
```

Two different variables that happen to share a name. Same word, different rooms.

---

### 3. Lists: indexing from 0, slicing, `len()`, append/remove, sorting

#### The plain-language explanation

> **Definition — list:** an ordered collection of values stored in a single variable, written in square brackets and separated by commas.

```python
scores = [45, 0, 112, 67, 8]        # five values, one variable
names = ["Rohit", "Anu", "Kiran"]   # lists can hold strings
mixed = [1, "two", 3.0, True]       # they CAN hold mixed types (rarely a good idea)
empty = []                          # a list with nothing in it
```

#### Indexing: positions start at 0

```
   scores = [ 45,   0,  112,  67,   8 ]
   index      0     1    2     3    4        ◄── counting forward from 0
   index     -5    -4   -3    -2   -1        ◄── counting backward from -1
```

```python
scores = [45, 0, 112, 67, 8]

print(scores[0])        # the FIRST item
print(scores[2])        # the third item
print(scores[-1])       # the LAST item
print(scores[-2])       # second from the end
print(len(scores))      # how many items
```

Output:

```
45
112
8
67
5
```

**Why start at 0?** Because then the index tells you *how far from the start* you are. The first item is zero steps from the start. It makes the arithmetic clean, and it's why `len(scores) - 1` is always the last valid index — 5 items, last index 4.

Going past the end:

```python
print(scores[5])
```

Output:

```
Traceback (most recent call last):
  File "demo.py", line 1, in <module>
    print(scores[5])
IndexError: list index out of range
```

That's the off-by-one error from Module 2, now with a name you'll recognise instantly.

#### 🍕 The analogy

A list is **a row of numbered lockers in a corridor**. The locker numbers start at 0 and run along the wall. You can:

- open one locker (`scores[2]`)
- count the lockers (`len(scores)`)
- take a photo of lockers 1 through 3 (a **slice**)
- add a new locker on the end (`append`)
- swap what's inside a locker (`scores[0] = 50`)

You cannot open locker 5 if there are only 5 lockers, because they're numbered 0 to 4.

#### Slicing

> **Definition — slice:** a new list made from part of an existing list, written `list[start:stop]` — start included, **stop excluded** (the same rule as `range`).

```python
scores = [45, 0, 112, 67, 8]

print(scores[1:4])      # items 1, 2, 3  (NOT 4)
print(scores[:3])       # from the start up to (not including) 3
print(scores[2:])       # from 2 to the end
print(scores[:])        # a full copy
print(scores[-2:])      # the last two
```

Output:

```
[0, 112, 67]
[45, 0, 112]
[112, 67, 8]
[45, 0, 112, 67, 8]
[67, 8]
```

A slice always gives you `stop - start` items. `scores[1:4]` → 4 − 1 = 3 items ✔

#### Changing a list

Lists are **mutable** — you can change them in place.

> **Definition — mutable:** able to be changed after it's created. Lists are mutable; strings and numbers are not.

```python
scores = [45, 0, 112]

scores.append(67)             # add one item to the END
print(scores)

scores.insert(1, 99)          # put 99 at position 1, shifting everything right
print(scores)

scores.remove(0)              # remove the first item EQUAL TO 0 (by value)
print(scores)

last = scores.pop()           # remove AND return the last item
print(last, scores)

scores[0] = 50                # replace by position
print(scores)

print(112 in scores)          # is this value present?
print(scores.index(112))      # at what position?
print(scores.count(50))       # how many times does it appear?
```

Output:

```
[45, 0, 112, 67]
[45, 99, 0, 112, 67]
[45, 99, 112, 67]
67 [45, 99, 112]
[50, 99, 112]
True
2
1
```

⚠️ `remove(0)` removes the *value* 0, not the item at *position* 0. To remove by position use `pop(0)` or `del scores[0]`. This confusion costs everyone an afternoon once.

#### Sorting — the two ways, and the trap

```python
scores = [45, 0, 112, 67, 8]

ordered = sorted(scores)          # returns a NEW sorted list; original untouched
print(ordered)
print(scores)                     # still in the original order

scores.sort()                     # sorts IN PLACE; returns None
print(scores)

scores.sort(reverse=True)         # biggest first
print(scores)
```

Output:

```
[0, 8, 45, 67, 112]
[45, 0, 112, 67, 8]
[0, 8, 45, 67, 112]
[112, 67, 45, 8, 0]
```

⚠️ **The trap:** `ordered = scores.sort()` gives you `None`, because `.sort()` returns nothing. Use `sorted()` when you want a new list, `.sort()` when you want to rearrange the one you have. When in doubt, use `sorted()` — it never surprises you by mutating something you were still using.

#### Useful built-ins that take a list

```python
scores = [45, 0, 112, 67, 8]

print(sum(scores))                # 45+0+112+67+8
print(min(scores))
print(max(scores))
print(len(scores))
print(sum(scores) / len(scores))  # the mean
```

Output:

```
232
0
112
5
46.4
```

Check: 45 + 0 + 112 + 67 + 8 = 232 ✔. 232 ÷ 5 = 46.4 ✔

Yes — `sum`, `min`, and `max` do in one word what took you a whole accumulator loop in Module 2. That loop was not wasted time: you now know exactly what these are doing, which means you'll know what to do when you need something they don't provide (like a median).

#### The copy trap

```python
a = [1, 2, 3]
b = a                # NOT a copy — b is another label on the SAME list
b.append(4)
print(a)
print(b)
```

Output:

```
[1, 2, 3, 4]
[1, 2, 3, 4]
```

Both changed, because there was only ever one list with two labels on it. To make a real copy:

```python
a = [1, 2, 3]
b = a[:]             # a slice of everything = a new list
# or: b = list(a)    # also works
b.append(4)
print(a)
print(b)
```

Output:

```
[1, 2, 3]
[1, 2, 3, 4]
```

Remember the lunchbox picture from Module 1? `b = a` puts a second label on the same lunchbox. `b = a[:]` makes a new lunchbox and copies the contents across.

---

### 4. Looping over a list, and `enumerate()`

#### The plain-language explanation

You met this at the end of Module 2. Now the full picture — three ways to loop, and when each is right.

**Way 1 — over the items (best when you don't need positions):**

```python
scores = [45, 0, 112]
for score in scores:
    print(score)
```

Output:

```
45
0
112
```

**Way 2 — over the indexes (when you need the position):**

```python
scores = [45, 0, 112]
for i in range(len(scores)):        # i = 0, 1, 2
    print(f"index {i} holds {scores[i]}")
```

Output:

```
index 0 holds 45
index 1 holds 0
index 2 holds 112
```

This works, but `range(len(...))` is clunky and it's where off-by-one bugs breed. There's a better way.

**Way 3 — `enumerate()` (both at once, and the one you should reach for):**

> **Definition — `enumerate()`:** wraps a list so each pass of the loop gives you both the position and the item.

```python
scores = [45, 0, 112]
for i, score in enumerate(scores):
    print(f"index {i} holds {score}")
```

Output:

```
index 0 holds 45
index 1 holds 0
index 2 holds 112
```

Humans count from 1, so `enumerate` lets you start elsewhere:

```python
players = ["Rohit", "Anu", "Kiran"]
for rank, name in enumerate(players, start=1):
    print(f"{rank}. {name}")
```

Output:

```
1. Rohit
2. Anu
3. Kiran
```

#### 🍕 The analogy

- Looping over items = **eating your way along a plate of samosas**. You care about the samosas, not their positions.
- Looping over indexes = **calling out seat numbers in an exam hall**. You care about the seats.
- `enumerate` = **a register**: seat number *and* name, together, in one pass.

#### The tiny concrete example

Find *where* the highest score is, not just what it is:

```python
scores = [45, 0, 112, 67, 8]

best_value = scores[0]              # assume the first is the best so far
best_index = 0

for i, score in enumerate(scores):
    if score > best_value:
        best_value = score
        best_index = i

print(f"Highest score {best_value} was innings number {best_index + 1}")
```

Output:

```
Highest score 112 was innings number 3
```

Note the `+ 1`: index 2 is the *third* innings. That translation between 0-based positions and 1-based human counting is a permanent part of programming. Do it explicitly and comment it.

⚠️ **Don't change a list's length while looping over it.** This skips items in a way that looks like magic:

```python
nums = [1, 2, 3, 4]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)
```

Output:

```
[1, 3]
```

That happens to be right here, but only by luck. With `[2, 4, 6]` you'd get `[4]`. **Build a new list instead** — which is exactly what comprehensions are for.

---

### 5. List comprehensions, and importing your own module

#### The plain-language explanation — comprehensions

You will write this shape hundreds of times:

```python
squares = []                        # empty accumulator list
for n in range(1, 6):
    squares.append(n * n)           # build it up
print(squares)
```

Output:

```
[1, 4, 9, 16, 25]
```

Python has a one-line way to write exactly that.

> **Definition — list comprehension:** a compact way to build a new list by transforming and/or filtering an existing one, written `[expression for item in source]`.

```python
squares = [n * n for n in range(1, 6)]
print(squares)
```

Output:

```
[1, 4, 9, 16, 25]
```

Read it in the order the loop happens: **"for n in range(1,6) ... take n*n ... collect them into a list."** The confusing part is that the *result* is written first. Here's the map:

```
   [ n * n     for n in range(1, 6) ]
     └──┬──┘   └────────┬─────────┘
        │               │
        │               └── 2nd: where the values come from
        └── 3rd: what to do with each one     (1st: the [ ] says "make a list")

   Equivalent loop:
       result = []
       for n in range(1, 6):          ◄── the "for" part
           result.append(n * n)       ◄── the expression part
```

#### With a filter

```python
scores = [45, 0, 112, 67, 8, 89]

fifties = [s for s in scores if s >= 50]        # keep only these
print(fifties)

doubled = [s * 2 for s in scores]               # transform every one
print(doubled)

big_doubled = [s * 2 for s in scores if s >= 50]   # filter AND transform
print(big_doubled)
```

Output:

```
[112, 67, 89]
[90, 0, 224, 134, 16, 178]
[224, 134, 178]
```

Order of reading, always: **source → filter → expression.** Take each `s` from `scores`; keep it only if `s >= 50`; then compute `s * 2`.

#### 🍕 The analogy

A comprehension is a **factory conveyor with an inspector and a machine**.

```
   scores ──► [ inspector: s >= 50? ] ──► [ machine: s * 2 ] ──► new list
              rejects go in the bin        keeps go on the belt
```

The `for` part is the belt, the `if` part is the inspector, the expression is the machine at the end.

#### When *not* to use one

```python
# Fine — one clear transformation
names_upper = [n.upper() for n in names]

# Please don't — a comprehension is not a place to hide a whole program
result = [x*2 if x > 0 else (x*3 if x < -5 else 0) for row in grid for x in row if x != 7]
```

**Rule: if you can't read it aloud in one breath, write a loop.** Clarity beats cleverness every single time.

#### The plain-language explanation — importing your own module

In Module 2 you wrote `import random` to borrow someone else's tools. **Any `.py` file you write is a module you can import the same way.**

> **Definition — module (yours):** any `.py` file. Import it by filename without the `.py`, and you get everything defined inside it.

Two files in the **same folder**. `shapes.py` holds the tools:

```python
# shapes.py — a tiny toolkit of shape functions.

def area_rectangle(length, width):
    """Return the area of a rectangle."""
    return length * width

def area_triangle(base, height):
    """Return the area of a triangle."""
    return base * height / 2

if __name__ == "__main__":          # runs ONLY when this file is run directly
    print("self-test:", area_rectangle(2, 3), area_triangle(4, 5))   # 6 10
```

`main.py` borrows them:

```python
# main.py — uses the shapes toolkit.

import shapes                                   # no .py, no quotes

print(shapes.area_rectangle(12.5, 4))           # module.function(...)  -> 50.0
print(shapes.area_triangle(10, 6))              # 10*6/2                -> 30.0
```

Run `python3 main.py`:

```
50.0
30.0
```

Check: 12.5 × 4 = 50 ✔. 10 × 6 ÷ 2 = 30 ✔ — and notice the self-test line did **not** print.

Two import styles:

```python
import shapes                                  # then: shapes.area_triangle(10, 6)
from shapes import area_triangle               # then: area_triangle(10, 6)
```

The first is clearer in a big program (you can always see where a function came from). The second is shorter. Use the first while learning.

#### The `if __name__ == "__main__":` guard

Without that guard, the self-test line would run **every time somebody imported the module** — so `python3 main.py` would print `self-test: 6 10` before doing its own work. That's almost never what you want.

Treat the guard as a magic spell for now: **"only run this bit if I'm the file being run."** You'll meet the machinery behind `__name__` in Level 3.

⚠️ Two import gotchas that waste hours:

1. Both files must be in the **same folder** (that's true for everything in this level).
2. Never name your file after a real module. `random.py`, `math.py`, `csv.py`, `statistics.py` will shadow the real thing and produce baffling errors. Prefix yours: `my_stats.py`.

---

## 🔍 Worked Example

**The problem.** Build a `median()` function from scratch and trace it on both an odd-length and an even-length list. The median is the middle value when the numbers are sorted — the "typical" value that isn't dragged around by one huge outlier.

### Step 1 — Why the median matters at all

Take five monthly pocket-money amounts: 200, 250, 300, 250, 12000 (one kid's grandmother visited).

- Mean: (200 + 250 + 300 + 250 + 12000) ÷ 5 = 13000 ÷ 5 = **2600**
- Median: sort → 200, 250, **250**, 300, 12000 → middle is **250**

The mean says a typical kid gets 2600. Not one of them does. The median says 250, which describes four of the five. **One extreme value drags the mean and leaves the median alone.** That's why you'll compute both for the rest of this course.

### Step 2 — The algorithm in words

1. Sort a **copy** of the numbers (never wreck the caller's list).
2. Let `n` be how many there are.
3. If `n` is **odd**, the answer is the single middle item, at index `n // 2`.
4. If `n` is **even**, the answer is the average of the two middle items, at `n // 2 - 1` and `n // 2`.

### Step 3 — Why `n // 2` is the middle for odd lengths

Trace it for n = 5, positions 0,1,2,3,4:

- `5 // 2` = 2. Index 2 is the third of five — two below it, two above it. **Exactly the middle** ✔

For n = 7, positions 0..6: `7 // 2` = 3. Index 3 has three below and three above ✔

The pattern holds because integer division throws away the half.

### Step 4 — Why the even case needs two items

For n = 6, positions 0..5, there is no single middle — items at index 2 and 3 are equally central.

- `6 // 2` = 3 → the upper middle
- `6 // 2 - 1` = 2 → the lower middle

Average them.

### Step 5 — Write it

```python
def median(numbers):
    """Return the middle value of a list of numbers.

    For an even count, return the average of the two middle values.
    """
    ordered = sorted(numbers)             # a NEW sorted list; caller's list untouched
    n = len(ordered)

    if n == 0:                            # guard: no median of nothing
        return None

    middle = n // 2                       # index of the upper-middle item

    if n % 2 == 1:                        # odd count -> one middle item
        return ordered[middle]
    else:                                 # even count -> average the two middles
        return (ordered[middle - 1] + ordered[middle]) / 2
```

### Step 6 — Trace the ODD case: `[45, 0, 112, 67, 8]`

| Step | Value |
|---|---|
| `sorted(numbers)` | `[0, 8, 45, 67, 112]` |
| `n` | 5 |
| `n == 0`? | No |
| `middle = 5 // 2` | 2 |
| `n % 2` | `5 % 2` = 1 → **odd branch** |
| `ordered[2]` | **45** |

Sanity check: with 0 and 8 below, 67 and 112 above, 45 is genuinely in the middle ✔

```python
print(median([45, 0, 112, 67, 8]))
```

Output:

```
45
```

### Step 7 — Trace the EVEN case: `[45, 0, 112, 67, 8, 89]`

| Step | Value |
|---|---|
| `sorted(numbers)` | `[0, 8, 45, 67, 89, 112]` |
| `n` | 6 |
| `middle = 6 // 2` | 3 |
| `n % 2` | `6 % 2` = 0 → **even branch** |
| `ordered[middle - 1]` = `ordered[2]` | 45 |
| `ordered[middle]` = `ordered[3]` | 67 |
| `(45 + 67) / 2` | 112 / 2 = **56.0** |

```python
print(median([45, 0, 112, 67, 8, 89]))
```

Output:

```
56.0
```

### Step 8 — Test the edge cases

Every function you write deserves four tests: normal, smallest, weird, and empty.

```python
print(median([7]))                     # a single item: middle of one is itself
print(median([4, 8]))                  # two items: their average
print(median([5, 5, 5, 5]))            # all the same
print(median([]))                      # empty: our guard returns None
```

Trace each:
- `[7]`: n=1, middle = 0, odd → `ordered[0]` = **7**
- `[4, 8]`: n=2, middle = 1, even → (`ordered[0]` + `ordered[1]`)/2 = (4+8)/2 = **6.0**
- `[5,5,5,5]`: n=4, middle = 2, even → (5+5)/2 = **5.0**
- `[]`: n=0 → guard returns **None**

Output:

```
7
6.0
5.0
None
```

### Step 9 — Prove it doesn't wreck the caller's list

```python
data = [45, 0, 112, 67, 8]
print(median(data))
print(data)                            # must be UNCHANGED
```

Output:

```
45
[45, 0, 112, 67, 8]
```

Untouched ✔ — because `sorted()` returns a new list rather than rearranging the original. Had we written `numbers.sort()` inside the function, the caller's data would have been silently reordered. That's a **side effect**, and side effects in a "just tell me a number" function are how trust dies.

---

## 💻 Hands-On

### Part A — Function basics (20 minutes)

New file, `func_basics.py`:

```python
# func_basics.py — the shapes of a function, one at a time.

# --- 1. No inputs, no output: just does something ---
def banner():
    """Print a divider line."""
    print("=" * 40)

# --- 2. Takes an input, prints (returns nothing useful) ---
def shout(text):
    """Print text in capitals. Returns None."""
    print(text.upper() + "!")

# --- 3. Takes an input, RETURNS a value: the useful shape ---
def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit and return the number."""
    return c * 9 / 5 + 32

# --- 4. Two inputs, one with a default ---
def bmi(weight_kg, height_m=1.6):
    """Return body mass index = weight / height squared."""
    return weight_kg / (height_m ** 2)

# --- 5. A decision inside a function ---
def bmi_category(value):
    """Return a one-word category for a BMI number."""
    if value < 18.5:
        return "under"
    elif value < 25:
        return "healthy"
    elif value < 30:
        return "over"
    else:
        return "obese"

# ---- Use them ----
banner()
shout("hello")
print(celsius_to_fahrenheit(37))            # 37*9/5 + 32 = 98.6
print(celsius_to_fahrenheit(100))           # 100*9/5 + 32 = 212.0
print(celsius_to_fahrenheit(0))             # 0 + 32 = 32.0
banner()

my_bmi = bmi(50, 1.6)                       # 50 / 2.56 = 19.53125
print(f"BMI {my_bmi:.1f} is {bmi_category(my_bmi)}")

print(f"BMI with default height: {bmi(50):.1f}")     # same as above

# Proving the print-vs-return point:
result = shout("test")                      # shout prints but returns nothing
print(f"shout returned: {result}")
```

Expected output:

```
========================================
HELLO!
98.6
212.0
32.0
========================================
BMI 19.5 is healthy
BMI with default height: 19.5
TEST!
shout returned: None
```

Check the arithmetic: 37 × 9 = 333, ÷ 5 = 66.6, + 32 = **98.6** ✔. 1.6² = 2.56, 50 ÷ 2.56 = **19.53125** → `19.5` ✔

### Part B — List surgery (20 minutes)

New file, `list_lab.py`:

```python
# list_lab.py — every list operation you need, once each.

scores = [45, 0, 112, 67, 8, 89, 34, 101]
print(f"start        : {scores}")
print(f"length       : {len(scores)}")

# --- indexing ---
print(f"first        : {scores[0]}")
print(f"third        : {scores[2]}")
print(f"last         : {scores[-1]}")
print(f"last index   : {len(scores) - 1}")

# --- slicing (stop is EXCLUDED, same as range) ---
print(f"first three  : {scores[:3]}")
print(f"middle 2..5  : {scores[2:5]}")
print(f"last two     : {scores[-2:]}")
print(f"a full copy  : {scores[:]}")

# --- built-in summaries ---
print(f"sum          : {sum(scores)}")
print(f"min / max    : {min(scores)} / {max(scores)}")
print(f"mean         : {sum(scores) / len(scores):.2f}")

# --- sorted() makes a new list; the original is untouched ---
print(f"sorted copy  : {sorted(scores)}")
print(f"original     : {scores}")
print(f"top 3        : {sorted(scores, reverse=True)[:3]}")

# --- adding and removing ---
scores.append(50)                     # add to the end
print(f"after append : {scores}")
scores.insert(0, 7)                   # add at the front
print(f"after insert : {scores}")
removed = scores.pop()                # remove and return the last
print(f"popped {removed}    : {scores}")
scores.remove(0)                      # remove the VALUE 0 (not position 0)
print(f"after remove : {scores}")

# --- searching ---
print(f"is 112 there : {112 in scores}")
print(f"where is 112 : {scores.index(112)}")
print(f"how many 8s  : {scores.count(8)}")

# --- the copy trap ---
a = [1, 2, 3]
b = a                                 # same list, two labels
c = a[:]                              # a genuine copy
b.append(999)
print(f"a={a}  b={b}  c={c}")
```

Expected output:

```
start        : [45, 0, 112, 67, 8, 89, 34, 101]
length       : 8
first        : 45
third        : 112
last         : 101
last index   : 7
first three  : [45, 0, 112]
middle 2..5  : [112, 67, 8]
last two     : [34, 101]
a full copy  : [45, 0, 112, 67, 8, 89, 34, 101]
sum          : 456
min / max    : 0 / 112
mean         : 57.00
sorted copy  : [0, 8, 34, 45, 67, 89, 101, 112]
original     : [45, 0, 112, 67, 8, 89, 34, 101]
top 3        : [112, 101, 89]
after append : [45, 0, 112, 67, 8, 89, 34, 101, 50]
after insert : [7, 45, 0, 112, 67, 8, 89, 34, 101, 50]
popped 50    : [7, 45, 0, 112, 67, 8, 89, 34, 101]
after remove : [7, 45, 112, 67, 8, 89, 34, 101]
is 112 there : True
where is 112 : 2
how many 8s  : 1
a=[1, 2, 3, 999]  b=[1, 2, 3, 999]  c=[1, 2, 3]
```

The last line is the one to stare at. `b.append(999)` changed `a` too, because `b = a` never made a second list.

### Part C — Comprehensions (15 minutes)

New file, `comp_lab.py`. For each comprehension, the equivalent loop is written above it so you can see the translation.

```python
# comp_lab.py — every comprehension paired with the loop it replaces.

scores = [45, 0, 112, 67, 8, 89, 34, 101]

# ---- 1. transform every item ----
halves_loop = []
for s in scores:
    halves_loop.append(s / 2)
halves_comp = [s / 2 for s in scores]
print(halves_loop == halves_comp, halves_comp)

# ---- 2. filter, keep some ----
fifties_loop = []
for s in scores:
    if s >= 50:
        fifties_loop.append(s)
fifties_comp = [s for s in scores if s >= 50]
print(fifties_loop == fifties_comp, fifties_comp)

# ---- 3. filter AND transform ----
big_pct_loop = []
for s in scores:
    if s >= 50:
        big_pct_loop.append(round(s / 112 * 100))
big_pct_comp = [round(s / 112 * 100) for s in scores if s >= 50]
print(big_pct_loop == big_pct_comp, big_pct_comp)

# ---- 4. build from range ----
cubes = [n ** 3 for n in range(1, 6)]
print(cubes)

# ---- 5. work on strings ----
players = ["rohit", "anu", "kiran", "dev"]
capitalised = [p.capitalize() for p in players]
short_names = [p for p in players if len(p) <= 3]
print(capitalised)
print(short_names)

# ---- 6. counting with a comprehension + len ----
duck_count = len([s for s in scores if s == 0])
print(f"ducks: {duck_count}")
```

Expected output:

```
True [22.5, 0.0, 56.0, 33.5, 4.0, 44.5, 17.0, 50.5]
True [112, 67, 89, 101]
True [100, 60, 79, 90]
[1, 8, 27, 64, 125]
['Rohit', 'Anu', 'Kiran', 'Dev']
['anu', 'dev']
ducks: 1
```

Check #3 by hand: 112/112 = 100%. 67/112 = 0.598 → 60. 89/112 = 0.7946 → 79. 101/112 = 0.9018 → 90 ✔

### Part D — Split a program across two files (20 minutes)

Make both files in the same folder.

`temps.py`:

```python
# temps.py — a small temperature toolkit. Import this; don't run it for real work.

def c_to_f(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32

def f_to_c(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9

def describe(celsius):
    """Return a one-word description of a Celsius temperature."""
    if celsius < 0:
        return "freezing"
    elif celsius < 15:
        return "cold"
    elif celsius < 25:
        return "pleasant"
    elif celsius < 35:
        return "hot"
    else:
        return "dangerous"

def hottest_day(temps):
    """Return (index, value) of the hottest temperature in a list."""
    best_i = 0
    best_v = temps[0]
    for i, t in enumerate(temps):
        if t > best_v:
            best_i = i
            best_v = t
    return best_i, best_v          # returning TWO values at once — Python allows this

# This block runs ONLY when you do: python3 temps.py
if __name__ == "__main__":
    print("self-test:")
    print("  0C  ->", c_to_f(0))         # 32.0
    print("  100C->", c_to_f(100))       # 212.0
    print("  98.6F->", round(f_to_c(98.6), 1))   # 37.0
```

`weather.py`:

```python
# weather.py — a week's report, built entirely from imported tools.

import temps                                  # our own module, same folder

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
CELSIUS = [21, 24, 29, 33, 36, 31, 27]        # a hot week in Bengaluru

print("DAY   °C    °F     FEELS")
print("-" * 30)
for day, c in zip(DAYS, CELSIUS):             # zip pairs two lists item by item
    f = temps.c_to_f(c)
    print(f"{day}  {c:>3}  {f:>5.1f}   {temps.describe(c)}")

print("-" * 30)
best_i, best_v = temps.hottest_day(CELSIUS)   # unpacking two returned values
print(f"Hottest: {DAYS[best_i]} at {best_v}°C")
print(f"Average: {sum(CELSIUS) / len(CELSIUS):.1f}°C")
print(f"Days above 30: {len([c for c in CELSIUS if c > 30])}")
```

> **Definition — `zip()`:** pairs up two lists item by item, so you can loop over both at once.

Run `python3 temps.py` first:

```
self-test:
  0C  -> 32.0
  100C-> 212.0
  98.6F-> 37.0
```

Then run `python3 weather.py`:

```
DAY   °C    °F     FEELS
------------------------------
Mon   21   69.8   pleasant
Tue   24   75.2   pleasant
Wed   29   84.2   hot
Thu   33   91.4   hot
Fri   36   96.8   dangerous
Sat   31   87.8   hot
Sun   27   80.6   hot
------------------------------
Hottest: Fri at 36°C
Average: 28.7°C
Days above 30: 3
```

Notice `weather.py` printed **no** self-test lines. That's the `if __name__ == "__main__":` guard doing its job.

Check the average: 21+24+29+33+36+31+27 = 201. 201 ÷ 7 = 28.714... → **28.7** ✔. Days above 30: 33, 36, 31 = **3** ✔

---

## ✍️ Practice

### 1. [Warm-up] Five tiny functions

Write `tiny.py` with five functions, each with a docstring, each **returning** (never printing):

- `square(n)` → n × n
- `is_even(n)` → `True` or `False`
- `initials(first, last)` → `"R.K."` from `"Ramana"`, `"Kamma"`
- `discount(price, percent=10)` → the price after the discount
- `longest(words)` → the longest string in a list of strings

Then call each one and print the result.

**Done looks like:** `square(7)` → 49, `is_even(10)` → True, `initials("Ramana", "Kamma")` → `R.K.`, `discount(500)` → 450.0, `discount(500, 25)` → 375.0, `longest(["hi", "hello", "hey"])` → `hello`.

### 2. [Warm-up] Slice practice

Given `letters = ["a","b","c","d","e","f","g","h"]`, write `slices.py` that prints each of these on its own line, using **only** slicing (no loops):

first three · last three · the middle four · everything except the first · everything except the last · a reversed copy (hint: `letters[::-1]`) · every second letter (hint: a step in the slice)

**Done looks like:** seven printed lists, and `letters` is unchanged at the end (print it to prove it).

### 3. [Build] Word statistics

Write `word_stats.py` with four functions that each take a **list of words** and return a value:

- `word_count(words)` → how many
- `average_length(words)` → mean number of characters, as a float
- `longest_word(words)` → the longest one
- `words_starting_with(words, letter)` → a new list of the words starting with that letter (case-insensitive)

Test them on `["banana", "apple", "cherry", "avocado", "blueberry", "apricot"]`.

**Done looks like:** count 6, average length 6.67, longest `blueberry`, and `words_starting_with(fruits, "A")` returns `['apple', 'avocado', 'apricot']`. Every function returns; only the test section prints. Check the average by counting the letters on paper before you trust the code.

### 4. [Build] Rewrite loops as comprehensions

Write `rewrite.py`. For each of these five loops, write the equivalent one-line comprehension, then assert they match.

```python
nums = [12, 7, 30, 4, 25, 18, 9]

# a) all the numbers doubled
# b) only the numbers above 10
# c) the string form of each number (use str())
# d) the remainder of each number when divided by 5
# e) the numbers above 10, halved and rounded to 1 decimal place
```

Use `assert loop_version == comp_version` after each pair. An `assert` that passes prints nothing; one that fails raises `AssertionError`.

**Done looks like:** the file runs with no output except a final `print("All 5 match.")`. If it prints that, every comprehension is right.

### 5. [Stretch] A `mode()` function

The **mode** is the most frequently occurring value. Write `mode.py` with:

- `mode(numbers)` → the value that appears most often. If several tie, return the **smallest** of the tied values. If the list is empty, return `None`.
- A test section proving it works on `[3,1,3,7,3]` → 3, `[1,1,2,2,3]` → 1, `[5]` → 5, `[]` → None.

**Constraint:** you may not use any library. Use lists, loops, and `.count()`.

**Done looks like:** all four tests pass with `assert`, and you can explain in a comment why the tie rule needs `sorted()`.

### 6. [Stretch] The trimmed mean

An outlier can wreck a mean (remember the ₹12,000 grandmother). One standard fix is a **trimmed mean**: throw away the highest and lowest values, then average what's left.

Write `trimmed.py` with `trimmed_mean(numbers, trim=1)` that removes `trim` items from each end of the *sorted* list before averaging.

Then compare all three measures on the pocket money data `[200, 250, 300, 250, 12000]`:

| Measure | Value |
|---|---|
| mean | ? |
| median | ? |
| trimmed mean (trim=1) | ? |

**Done looks like:** a printed comparison table, correct handling of `trim=0`, and a guard that returns `None` if trimming would leave nothing (e.g. `trimmed_mean([1,2], trim=1)`). Add a 3-sentence comment on when a trimmed mean would be *dishonest* to use.

---

## 🤔 Think Deeper

### 1. Your `median()` function returns `None` for an empty list. Is that the right choice, or should it crash?

*How to reason about it:* Imagine `median()` buried inside a bigger program that computes a class average and emails it to parents. If the list is empty because of a data-loading bug, which is better: an email saying "class median: None", an email saying "class median: 0", or a loud crash before any email is sent? Now imagine the same function in a quick script you're running yourself. Notice the answer flips. Then ask what *information* the caller needs to make its own decision, and whether `None` gives them that.

### 2. Your Stats Toolkit will compute a mean, median, min, max, and range for real people's scores. Which single number would you show a class, and what does your choice hide?

*How to reason about it:* Take a real distribution — say 18 students around 60 and 2 students at 5 — and compute all five numbers. Ask what a parent, a student, and a teacher each *do* with the number after they read it. Notice that "the honest number" depends on the decision it feeds. Then consider showing more than one, and ask why almost nobody does.

### 3. Functions are supposed to take inputs and give outputs without touching anything else. But `list.sort()` deliberately changes the list you give it. Why would Python's designers build something that breaks the rule they recommend?

*How to reason about it:* Think about a list of one million numbers. `sorted()` must build a second list of a million numbers; `.sort()` doesn't. Estimate the memory cost. Then think about a function that sorts *and* returns, and ask what happens when a reader assumes it only did one of those. Notice that this is a trade between **speed** and **surprise**, and that the right answer changes with the size of the data — a theme that comes back hard in Module 5 when you meet numpy.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Function defined but nothing happens | You defined it and never called it | `def greet():` writes the recipe; `greet()` cooks it. You need both |
| `result = my_func(x)` gives `None` | The function printed instead of returning | Change the last line from `print(answer)` to `return answer` |
| `ordered = scores.sort()` gives `None` | `.sort()` sorts in place and returns nothing | Use `ordered = sorted(scores)` |
| `IndexError: list index out of range` | Used `scores[len(scores)]`; the last valid index is `len - 1` | Use `scores[-1]` for the last item, or `range(len(scores))` for indexes |
| `scores.remove(0)` deleted the wrong thing | `.remove()` takes a **value**, not a position | Use `scores.pop(0)` or `del scores[0]` to remove by position |
| Changing a list while looping over it skips items | The loop's internal position shifts when items disappear | Build a new list with a comprehension instead |
| `b = a` then editing `b` also changes `a` | Assignment copies the *label*, not the list | Use `b = a[:]` or `b = list(a)` for a real copy |
| `UnboundLocalError` on a variable you can see above | Assigning to a name inside a function makes it local everywhere in that function | Pass it in as a parameter and return the new value |
| `ModuleNotFoundError: No module named 'stats'` | The two files aren't in the same folder, or you ran from elsewhere | `cd` into the folder first, and check with `ls` that both `.py` files are there |
| Your `random.py` breaks `import random` | You named a file after a built-in module | Rename it. Prefix personal modules: `my_random.py` |
| A comprehension nobody can read | Cramming filters, conditionals, and nested loops into one line | If you can't read it aloud in one breath, write a normal loop |
| Function works on one list, wrecks it for the caller | You used `.sort()` or `.append()` on the parameter | Work on a copy: `ordered = sorted(numbers)` |

---

## 🛠️ Mini-Project: Stats Toolkit

**Time: 60–90 minutes**

### Goal

Build a **reusable** statistics module — `stats.py` — with five functions that all *return*, plus a `main.py` that imports it and reports on 20 cricket scores. This is your first two-file program, and it's a genuine tool you will re-use in Module 6 to sanity-check pandas.

### Starter steps

**Step 1 — Plan the interface on paper before coding.**

| Function | Takes | Returns | Edge case |
|---|---|---|---|
| `mean(numbers)` | a list of numbers | a float | empty → `None` |
| `median(numbers)` | a list of numbers | a number | empty → `None`; even count → average of two middles |
| `minimum(numbers)` | a list of numbers | a number | empty → `None` |
| `maximum(numbers)` | a list of numbers | a number | empty → `None` |
| `value_range(numbers)` | a list of numbers | a number | empty → `None` |

**Step 2 — Write `stats.py` one function at a time**, and test each with `if __name__ == "__main__":` before writing the next. Do not write all five then run.

**Step 3 — Do not use the `statistics` library.** The whole point is to build them. (Also: don't name your file `statistics.py`.)

**Step 4 — Write `main.py`** with the 20 scores as a list, import `stats`, and print a report.

**Step 5 — Verify by hand.** Sort the 20 numbers on paper. Check the median by counting to the middle. Check the total with a calculator. If your code disagrees with your paper, find out which is wrong before moving on.

### `stats.py`

```python
# stats.py — a small statistics toolkit. Every function RETURNS; none of them print.

def mean(numbers):
    """Return the arithmetic mean (average), or None for an empty list."""
    if len(numbers) == 0:                 # guard against dividing by zero
        return None
    return sum(numbers) / len(numbers)


def median(numbers):
    """Return the middle value; for an even count, the average of the two middles.

    Returns None for an empty list. The caller's list is never modified.
    """
    if len(numbers) == 0:
        return None
    ordered = sorted(numbers)             # a NEW list, so the caller's stays intact
    n = len(ordered)
    middle = n // 2                       # index of the upper-middle item
    if n % 2 == 1:                        # odd count -> one clear middle
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2   # even -> average two


def minimum(numbers):
    """Return the smallest value, or None for an empty list."""
    if len(numbers) == 0:
        return None
    smallest = numbers[0]                 # assume the first is smallest
    for n in numbers:                     # then check every one
        if n < smallest:
            smallest = n                  # found a new champion
    return smallest


def maximum(numbers):
    """Return the largest value, or None for an empty list."""
    if len(numbers) == 0:
        return None
    largest = numbers[0]
    for n in numbers:
        if n > largest:
            largest = n
    return largest


def value_range(numbers):
    """Return largest minus smallest (the spread), or None for an empty list."""
    if len(numbers) == 0:
        return None
    return maximum(numbers) - minimum(numbers)    # reuse our own functions


# ---- Self-tests: run ONLY when you do `python3 stats.py` ----
if __name__ == "__main__":
    # assert stops the program with an AssertionError if the claim is false.
    assert mean([2, 4, 6]) == 4.0                  # 12 / 3
    assert mean([]) is None

    assert median([3, 1, 2]) == 2                  # sorted [1,2,3], middle is 2
    assert median([4, 1, 3, 2]) == 2.5             # sorted [1,2,3,4], (2+3)/2
    assert median([7]) == 7
    assert median([]) is None

    assert minimum([5, 2, 9]) == 2
    assert maximum([5, 2, 9]) == 9
    assert value_range([5, 2, 9]) == 7             # 9 - 2

    # Prove we never modify the caller's list.
    original = [3, 1, 2]
    median(original)
    assert original == [3, 1, 2], "median must not reorder the caller's list"

    print("All stats.py self-tests passed. ✅")
```

Run `python3 stats.py`:

```
All stats.py self-tests passed. ✅
```

> **Definition — `assert`:** a line that says "this must be true." If it is, nothing happens. If it isn't, the program stops with an `AssertionError` and your message.

### `main.py`

```python
# main.py — report on a season of 20 cricket scores using the stats toolkit.

import stats                                # our own module, same folder

SCORES = [45, 0, 112, 67, 8, 89, 34, 101, 23, 56,
          77, 4, 90, 19, 63, 38, 72, 15, 50, 26]   # 20 innings

WIDTH = 46

print("=" * WIDTH)
print("  SEASON REPORT — 20 INNINGS")
print("=" * WIDTH)

# --- the raw data, 10 per line, so a human can eyeball it ---
for i, score in enumerate(SCORES, start=1):        # start=1 so humans count from 1
    print(f"{score:>4}", end="")                   # 4 characters wide, no newline
    if i % 10 == 0:                                # after every 10th, break the line
        print()

print("-" * WIDTH)

# --- the five toolkit numbers ---
print(f"  Innings      : {len(SCORES)}")
print(f"  Total runs   : {sum(SCORES)}")
print(f"  Mean         : {stats.mean(SCORES):.2f}")
print(f"  Median       : {stats.median(SCORES)}")
print(f"  Lowest       : {stats.minimum(SCORES)}")
print(f"  Highest      : {stats.maximum(SCORES)}")
print(f"  Range        : {stats.value_range(SCORES)}")

print("-" * WIDTH)

# --- derived facts, using comprehensions ---
fifties = [s for s in SCORES if s >= 50]
ducks = [s for s in SCORES if s == 0]
above_mean = [s for s in SCORES if s > stats.mean(SCORES)]

print(f"  Fifty-plus   : {len(fifties)}  {fifties}")
print(f"  Ducks        : {len(ducks)}")
print(f"  Above mean   : {len(above_mean)} of {len(SCORES)}")

print("-" * WIDTH)

# --- mean vs median: which describes this season better? ---
m = stats.mean(SCORES)
md = stats.median(SCORES)
if m > md:
    print(f"  Mean ({m:.2f}) > median ({md}): a few big scores are")
    print("  pulling the average up. The median is the fairer")
    print("  description of a typical innings.")
elif m < md:
    print(f"  Mean ({m:.2f}) < median ({md}): a few very low scores")
    print("  are dragging the average down.")
else:
    print(f"  Mean and median agree at {m}: a balanced season.")

print("=" * WIDTH)
```

### Expected output

```
==============================================
  SEASON REPORT — 20 INNINGS
==============================================
  45   0 112  67   8  89  34 101  23  56
  77   4  90  19  63  38  72  15  50  26
----------------------------------------------
  Innings      : 20
  Total runs   : 989
  Mean         : 49.45
  Median       : 47.5
  Lowest       : 0
  Highest      : 112
  Range        : 112
----------------------------------------------
  Fifty-plus   : 10  [112, 67, 89, 101, 56, 77, 90, 63, 72, 50]
  Ducks        : 1
  Above mean   : 10 of 20
----------------------------------------------
  Mean (49.45) > median (47.5): a few big scores are
  pulling the average up. The median is the fairer
  description of a typical innings.
==============================================
```

### Check every number by hand

Sorted, the 20 scores are:

```
0, 4, 8, 15, 19, 23, 26, 34, 38, 45, 50, 56, 63, 67, 72, 77, 89, 90, 101, 112
```

- **Total:** add them in pairs from the ends — (0+112) + (4+101) + (8+90) + (15+89) + (19+77) + (23+72) + (26+67) + (34+63) + (38+56) + (45+50) = 112 + 105 + 98 + 104 + 96 + 95 + 93 + 97 + 94 + 95 = **989** ✔
- **Mean:** 989 ÷ 20 = **49.45** ✔
- **Median:** 20 items, so `middle = 20 // 2 = 10`. Average `ordered[9]` and `ordered[10]` = **45** and **50** → (45 + 50) / 2 = **47.5** ✔
- **Min / Max / Range:** 0, 112, 112 − 0 = **112** ✔
- **Fifty-plus:** 50, 56, 63, 67, 72, 77, 89, 90, 101, 112 = **10** ✔
- **Above the mean of 49.45:** the same ten (50 is above 49.45) = **10** ✔

### Success criteria checklist

- [ ] `stats.py` has all five functions, each with a docstring
- [ ] **Every function returns; none of them print** — check by reading each one
- [ ] Median is correct for an even count *and* an odd count, proved by `assert`
- [ ] Every function returns `None` (not a crash) for an empty list
- [ ] `median()` does not reorder the caller's list, proved by `assert`
- [ ] `python3 stats.py` prints only "All self-tests passed"
- [ ] `python3 main.py` prints the full report and **no** self-test lines
- [ ] `main.py` uses at least two list comprehensions
- [ ] Every number in the report is verified by hand on paper
- [ ] Both files are in the same folder, and neither is named `statistics.py`

### 🚀 Level it up

**Extension 1 — add three more functions to `stats.py`:**

- `mode(numbers)` — most common value, smallest on a tie (see Practice 5)
- `spread(numbers)` — return the *mean absolute deviation*: the average distance of each value from the mean. For our data: sum of `abs(score - 49.45)` over all 20, divided by 20.
- `percentile(numbers, p)` — the value below which `p` percent of the data falls. Use the simple "nearest rank" method: sort, then take index `int(p / 100 * len(numbers))`, clamped to the last valid index. Test that `percentile(SCORES, 50)` is close to your median.

**Extension 2 — a text histogram in `main.py`:**

```
    0 |
    4 | #
    8 | ##
   15 | #####
   ...
  112 | ########################################
```

Scale so the maximum score fills 40 characters: `bars = int(score / stats.maximum(SCORES) * 40)`.

**Extension 3 — the real test of a toolkit.** Create a *third* file, `test_stats.py`, that imports `stats` and runs 15 assertions covering: empty lists, one-item lists, two-item lists, all-identical lists, negative numbers, and floats. If all 15 pass it prints `15/15 ✅`. A toolkit you haven't tried to break is a toolkit you don't yet trust.

---

## 🔑 Key Takeaways

- **A function is a named recipe.** `def` writes it; `name()` runs it. Defining without calling does nothing.
- **Return, don't print.** A returned value can be stored, added, compared, and printed. A printed value is gone forever.
- **Variables inside a function stay inside.** Take inputs through parameters, hand results back through `return`, and change nothing else.
- **Lists hold many values in one variable, indexed from 0.** The last item is at `len(list) - 1`, or just `list[-1]`.
- **Slices and `range()` share one rule: the stop value is excluded.** `scores[1:4]` gives three items.
- **`sorted()` returns a new list; `.sort()` rearranges the one you have and returns `None`.** Prefer `sorted()` inside functions so you never surprise your caller.
- **A comprehension is a loop plus an accumulator, written on one line.** Use it when it reads clearly; write the loop when it doesn't.
- **Any `.py` file is a module you can `import`** — and `if __name__ == "__main__":` keeps its self-tests from firing when someone imports it.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Function** | A named block of code you can run whenever you want | `def mean(numbers):` |
| **Define vs call** | Writing the recipe vs cooking it | `def greet():` vs `greet()` |
| **Parameter** | The placeholder name in the function's definition | `def greet(name):` |
| **Argument** | The real value you hand over when calling | `greet("Anu")` |
| **`return`** | Send a value back to whoever called the function | `return n * 2` |
| **`None`** | Python's word for "no value at all" | what a function without `return` gives back |
| **Default value** | A value used when the caller doesn't supply one | `def f(price, tax=18):` |
| **Docstring** | A short string at the top of a function explaining it | `"""Return the mean."""` |
| **Scope** | The part of a program where a name exists | a local variable dies when its function ends |
| **Local variable** | A variable created inside a function | invisible from outside |
| **Global variable** | A variable created outside all functions | readable inside, but don't assign to it there |
| **Side effect** | A change a function makes to something outside itself | `.sort()` reordering your list |
| **List** | An ordered collection of values in one variable | `[45, 0, 112]` |
| **Index** | A value's position in a list, counting from 0 | `scores[0]` is the first |
| **Negative index** | Counting backwards from the end | `scores[-1]` is the last |
| **Slice** | A new list made from part of another; stop is excluded | `scores[1:4]` |
| **Mutable** | Able to be changed after creation | lists are; strings aren't |
| **`append`** | Add one item to the end of a list | `scores.append(50)` |
| **`pop`** | Remove and hand back an item (last one by default) | `scores.pop()` |
| **`sorted()` vs `.sort()`** | New sorted list vs rearrange in place | `sorted(s)` / `s.sort()` |
| **`enumerate()`** | Loop giving you position and item together | `for i, s in enumerate(scores):` |
| **`zip()`** | Loop over two lists side by side | `for d, c in zip(days, temps):` |
| **List comprehension** | A one-line way to build a list from another | `[s * 2 for s in scores if s > 50]` |
| **Module** | A `.py` file you can import for its tools | `import stats` |
| **`import`** | Bring another file's functions into this one | `import random` |
| **`__main__` guard** | Code that runs only when this file is run directly | `if __name__ == "__main__":` |
| **`assert`** | A line claiming something must be true; crashes if it isn't | `assert mean([2,4]) == 3.0` |
| **Median** | The middle value when sorted — not dragged by outliers | median of 200,250,250,300,12000 is 250 |
| **Outlier** | A value far away from all the others | the ₹12,000 |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### Practice 1 — Five tiny functions

```python
# tiny.py — five small functions, all returning.

def square(n):
    """Return n multiplied by itself."""
    return n * n


def is_even(n):
    """Return True if n divides by 2 with no remainder."""
    return n % 2 == 0          # this comparison already IS a bool - just return it


def initials(first, last):
    """Return initials like 'R.K.' from a first and last name."""
    return f"{first[0].upper()}.{last[0].upper()}."     # [0] is the first character


def discount(price, percent=10):
    """Return the price after taking off `percent` percent."""
    return price * (1 - percent / 100)


def longest(words):
    """Return the longest string in a list. Ties go to the first one found."""
    if len(words) == 0:
        return None
    best = words[0]
    for word in words:
        if len(word) > len(best):
            best = word
    return best


# ---- try them out ----
print(square(7))                              # 49
print(is_even(10), is_even(7))                # True False
print(initials("Ramana", "Kamma"))            # R.K.
print(discount(500))                          # 450.0  (default 10%)
print(discount(500, 25))                      # 375.0
print(longest(["hi", "hello", "hey"]))        # hello
```

Output:

```
49
True False
R.K.
450.0
375.0
hello
```

**The common mistake in `is_even`:** writing

```python
if n % 2 == 0:
    return True
else:
    return False
```

That works, but `n % 2 == 0` is *already* `True` or `False`. Returning it directly is shorter and clearer. Whenever you see `if <something>: return True else: return False`, delete it and return the something.

**Why `discount` returns a float:** `1 - 10/100` is `0.9`, a float, and `500 * 0.9` is `450.0`. If you want a whole number, the caller can round it — the function shouldn't decide that for them.

---

### Practice 2 — Slice practice

```python
# slices.py — seven slices, no loops.

letters = ["a", "b", "c", "d", "e", "f", "g", "h"]        # indexes 0..7

print(letters[:3])          # first three: indexes 0,1,2
print(letters[-3:])         # last three: indexes 5,6,7
print(letters[2:6])         # the middle four: indexes 2,3,4,5
print(letters[1:])          # everything except the first
print(letters[:-1])         # everything except the last
print(letters[::-1])        # a reversed COPY (step of -1)
print(letters[::2])         # every second letter (step of 2)

print(letters)              # proof: unchanged
```

Output:

```
['a', 'b', 'c']
['f', 'g', 'h']
['c', 'd', 'e', 'f']
['b', 'c', 'd', 'e', 'f', 'g', 'h']
['a', 'b', 'c', 'd', 'e', 'f', 'g']
['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
['a', 'c', 'e', 'g']
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
```

**The full slice form is `list[start:stop:step]`.** Leave any part out and Python uses a sensible default: start of the list, end of the list, step of 1.

**Why `letters[::-1]` reverses:** the step is −1, so it walks backwards, and the empty start/stop mean "the whole thing." It makes a **new** list — the original is untouched, which the last line proves.

**Why 8 items with step 2 gives 4:** indexes 0, 2, 4, 6 — it stops before it would need index 8.

---

### Practice 3 — Word statistics

```python
# word_stats.py — four functions over a list of words. All return.

def word_count(words):
    """Return how many words are in the list."""
    return len(words)


def average_length(words):
    """Return the mean number of characters per word, or None if empty."""
    if len(words) == 0:
        return None
    total_chars = 0
    for word in words:
        total_chars += len(word)          # accumulator over character counts
    return total_chars / len(words)


def longest_word(words):
    """Return the longest word. Ties go to the first one found."""
    if len(words) == 0:
        return None
    best = words[0]
    for word in words:
        if len(word) > len(best):
            best = word
    return best


def words_starting_with(words, letter):
    """Return a new list of words starting with `letter`, ignoring case."""
    target = letter.lower()               # normalise the letter we're looking for
    return [w for w in words if w.lower().startswith(target)]


# ---- tests (the only place that prints) ----
fruits = ["banana", "apple", "cherry", "avocado", "blueberry", "apricot"]

print(f"count            : {word_count(fruits)}")
print(f"average length   : {average_length(fruits):.2f}")
print(f"longest          : {longest_word(fruits)}")
print(f"starting with A  : {words_starting_with(fruits, 'A')}")
print(f"starting with b  : {words_starting_with(fruits, 'b')}")
print(f"empty list mean  : {average_length([])}")
```

Output:

```
count            : 6
average length   : 6.67
longest          : blueberry
starting with A  : ['apple', 'avocado', 'apricot']
starting with b  : ['banana', 'blueberry']
empty list mean  : None
```

Check the average length by hand, letter by letter: banana 6, apple 5, cherry 6, avocado 7, blueberry 9, apricot 7. Running total: 6 + 5 = 11, + 6 = 17, + 7 = 24, + 9 = 33, + 7 = **40**. Then 40 ÷ 6 = 6.6666... → **6.67** ✔

Notice that `longest_word` returns `blueberry` (9 letters) and not `avocado` or `apricot` (7 each) — and that if two words tied at 9, the **first** one found would win, because the comparison is `>` and not `>=`. That's a design choice; write it in the docstring so nobody has to guess.

`.startswith()` is a string method that returns `True`/`False`. `w.lower().startswith("a")` handles `"Apple"` and `"apple"` identically, which is why `words_starting_with(fruits, 'A')` finds the lowercase entries.

---

### Practice 4 — Rewrite loops as comprehensions

```python
# rewrite.py — five loops, five comprehensions, five assertions.

nums = [12, 7, 30, 4, 25, 18, 9]

# a) all the numbers doubled
loop_a = []
for n in nums:
    loop_a.append(n * 2)
comp_a = [n * 2 for n in nums]
assert loop_a == comp_a

# b) only the numbers above 10
loop_b = []
for n in nums:
    if n > 10:
        loop_b.append(n)
comp_b = [n for n in nums if n > 10]
assert loop_b == comp_b

# c) the string form of each number
loop_c = []
for n in nums:
    loop_c.append(str(n))
comp_c = [str(n) for n in nums]
assert loop_c == comp_c

# d) the remainder of each number when divided by 5
loop_d = []
for n in nums:
    loop_d.append(n % 5)
comp_d = [n % 5 for n in nums]
assert loop_d == comp_d

# e) the numbers above 10, halved and rounded to 1 decimal place
loop_e = []
for n in nums:
    if n > 10:
        loop_e.append(round(n / 2, 1))
comp_e = [round(n / 2, 1) for n in nums if n > 10]
assert loop_e == comp_e

print("All 5 match.")
```

Output:

```
All 5 match.
```

The values, if you print them:

| Part | Result |
|---|---|
| a | `[24, 14, 60, 8, 50, 36, 18]` |
| b | `[12, 30, 25, 18]` |
| c | `['12', '7', '30', '4', '25', '18', '9']` |
| d | `[2, 2, 0, 4, 0, 3, 4]` |
| e | `[6.0, 15.0, 12.5, 9.0]` |

Check (d) by hand: 12 % 5 = 2 ✔. 7 % 5 = 2 ✔. 30 % 5 = 0 ✔. 4 % 5 = 4 (4 is smaller than 5, so the whole thing is remainder) ✔. 25 % 5 = 0 ✔. 18 % 5 = 3 ✔. 9 % 5 = 4 ✔

**The structural point:** every single comprehension has the shape `[expression for item in source if condition]`, and the `if` is optional. In the loop version the `if` sits *above* the `append`; in the comprehension it goes at the *end*. Same logic, different word order.

---

### Practice 5 — A `mode()` function

```python
# mode.py — the most common value, ties broken by taking the smallest.

def mode(numbers):
    """Return the most frequently occurring value.

    If several values tie for most frequent, return the smallest of them.
    Returns None for an empty list.
    """
    if len(numbers) == 0:
        return None

    best_value = None
    best_count = 0

    # sorted() means we meet candidates smallest-first, so the FIRST one to
    # reach the top count wins - and a later tie can never displace it,
    # because we use a strict > comparison.
    for value in sorted(numbers):
        count = numbers.count(value)       # how many times this value appears
        if count > best_count:             # strictly greater: ties keep the earlier
            best_count = count
            best_value = value

    return best_value


if __name__ == "__main__":
    assert mode([3, 1, 3, 7, 3]) == 3          # 3 appears three times
    assert mode([1, 1, 2, 2, 3]) == 1          # 1 and 2 both twice -> smaller wins
    assert mode([5]) == 5                      # one item is its own mode
    assert mode([]) is None                    # empty guard
    assert mode([9, 9, 2, 2, 2]) == 2          # 2 appears three times, 9 twice
    print("All mode tests passed. ✅")
```

Output:

```
All mode tests passed. ✅
```

**Why the tie rule needs `sorted()`:** consider `[1, 1, 2, 2, 3]`. Without sorting, the loop meets values in the order 1, 1, 2, 2, 3. It sets `best = 1, count = 2`. Then it meets 2 with count 2 — but `2 > 2` is false, so 1 keeps the crown. That happens to be right here *by accident*, because 1 came first in the data.

Now try `[2, 2, 1, 1]`. Unsorted, the loop meets 2 first and keeps it — wrong, we wanted 1. With `sorted()` the loop always meets 1 before 2, so the smallest tied value is always the one that claims the top count first, and the strict `>` protects it. **`sorted()` turns "whichever came first in the data" into "whichever is smallest," which is a rule you can state.**

**Efficiency note:** `numbers.count(value)` scans the whole list every time, so this is slow for big lists (it does length × length work). For 20 cricket scores that's 400 tiny operations — invisible. For a million values it would be catastrophic. You'll learn the fast way — a counting dictionary — in Module 4.

---

### Practice 6 — The trimmed mean

```python
# trimmed.py — mean, median, and trimmed mean compared on outlier-heavy data.

def mean(numbers):
    """Return the arithmetic mean, or None for an empty list."""
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)


def median(numbers):
    """Return the middle value; average the two middles for an even count."""
    if len(numbers) == 0:
        return None
    ordered = sorted(numbers)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def trimmed_mean(numbers, trim=1):
    """Return the mean after removing `trim` items from each end of the sorted list.

    Returns None if trimming would leave nothing (or if trim is negative).
    """
    if trim < 0:
        return None
    if len(numbers) - 2 * trim <= 0:          # nothing would survive the trim
        return None

    ordered = sorted(numbers)
    if trim == 0:
        kept = ordered                        # slicing [0:len] also works, but be explicit
    else:
        kept = ordered[trim:-trim]            # drop `trim` from each end
    return sum(kept) / len(kept)


if __name__ == "__main__":
    pocket = [200, 250, 300, 250, 12000]

    print("POCKET MONEY (rupees):", sorted(pocket))
    print("-" * 42)
    print(f"  {'mean':<22} {mean(pocket):>10.2f}")
    print(f"  {'median':<22} {median(pocket):>10.2f}")
    print(f"  {'trimmed mean (trim=1)':<22} {trimmed_mean(pocket, 1):>10.2f}")
    print("-" * 42)

    # edge cases
    assert trimmed_mean([1, 2, 3, 4], 0) == 2.5        # no trim = ordinary mean
    assert trimmed_mean([1, 2], 1) is None             # 2 - 2 = 0 items left
    assert trimmed_mean([1, 2, 3], 1) == 2             # keeps only the middle
    assert trimmed_mean([1, 2, 3], -1) is None         # negative trim rejected
    print("All trimmed_mean edge cases passed. ✅")

# WHEN A TRIMMED MEAN IS DISHONEST:
# Trimming throws away the extremes on purpose, so it is dishonest whenever the
# extremes are the point. If you are measuring hospital waiting times, the two
# people who waited 14 hours are exactly the people the report exists to find,
# and averaging them away makes the service look fine. The rule: trim to describe
# a typical case, never to make a problem disappear - and always say you trimmed.
```

Output:

```
POCKET MONEY (rupees): [200, 250, 250, 300, 12000]
------------------------------------------
  mean                      2600.00
  median                     250.00
  trimmed mean (trim=1)      266.67
------------------------------------------
All trimmed_mean edge cases passed. ✅
```

**The comparison table:**

| Measure | Value | What it says |
|---|---|---|
| mean | 2600.00 | "kids get ₹2600" — true of nobody |
| median | 250.00 | "a typical kid gets ₹250" — true of three of the five |
| trimmed mean (trim=1) | 266.67 | "typical kid gets ₹267" — close to the median, and uses more of the data |

Check the trimmed mean by hand: sorted is `[200, 250, 250, 300, 12000]`. Drop one from each end → `[250, 250, 300]`. Sum = 800. 800 ÷ 3 = 266.666... = **266.67** ✔

Check the mean: 200 + 250 + 300 + 250 + 12000 = 13,000. ÷ 5 = **2600** ✔

**Why `ordered[trim:-trim]` fails when `trim == 0`:** `ordered[0:0]` is an empty list, because `-0` is just `0`. That's why the code special-cases `trim == 0`. It's a genuinely sneaky bug and the reason the `assert trimmed_mean([1,2,3,4], 0) == 2.5` test exists — without that test you'd ship it broken and only notice weeks later.

</details>

---

[⬅ Previous](module-02-decisions-and-loops.md) · [Level 2 Home](README.md) · [Next ➡](module-04-dictionaries-and-datasets.md)
