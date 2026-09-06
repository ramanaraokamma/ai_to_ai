# Module 5 — NumPy: Thinking in Arrays

**Level 2 · Module 5 · ~4 hours · Prereqs: Modules 1–4 (types, loops, functions, lists, list comprehensions, dictionaries, list-of-dicts datasets)**

[⬅ Previous](module-04-dictionaries-and-datasets.md) · [Level 2 Home](README.md) · [Next ➡](module-06-pandas-tables.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** create numpy arrays six different ways and read their `shape`, `dtype`, `ndim`, and `size`.
2. **You will be able to** do arithmetic on a whole array at once, and explain what **broadcasting** does when two shapes don't match — including when it refuses.
3. **You will be able to** compute sums, means, mins, and maxes along a chosen **axis**, and say out loud which direction `axis=0` and `axis=1` collapse.
4. **You will be able to** select data with **boolean masks** instead of writing `if` statements inside loops.
5. **You will be able to** treat a row of numbers as a **vector** and compute the distance between two vectors — the exact operation your first machine-learning model will use in Module 8.

---

## 🪝 The Hook

Here's a job for your Module 3 skills. A weather station records the temperature every minute for a year. That's 525,600 numbers. Convert them all from Celsius to Fahrenheit.

```python
fahrenheit = []
for c in celsius:
    fahrenheit.append(c * 9 / 5 + 32)
```

That works. It takes about a fifth of a second and eleven characters of typing per idea. Now do it again for humidity. Now for the pressure. Now find the average temperature for each of the 365 days, which means a loop inside a loop. Now find every minute where it was above 35 °C *and* the humidity was above 80%, which means a loop with a compound `if` inside it. Your file is getting long and every loop is a fresh chance to write `<` where you meant `<=`.

There is a different way to think, and one line of it replaces that whole loop:

```python
fahrenheit = celsius * 9 / 5 + 32
```

Not a loop. Not a comprehension. You wrote the *formula*, once, and applied it to half a million numbers. It also runs about twenty times faster.

That's **NumPy**. Every model you will ever train — the kNN in Module 8, the neural networks in Level 3, the giant language models in Level 4 — does its arithmetic exactly this way. Learn to think in arrays now and everything after it gets easier.

---

## 🧠 The Concept

### 0. Getting NumPy

```bash
pip install numpy
```

If that errors, try `pip3 install numpy` or `python3 -m pip install numpy`. Check it worked:

```python
import numpy as np
print(np.__version__)      # e.g. 1.26.4 — any recent version is fine
```

`import numpy as np` is the standard line. Everyone writes `np`. Do the same, so other people's code reads like yours.

---

### 1. Why lists are slow and arrays are fast

#### The plain-language explanation

A Python **list** can hold anything: `[1, "cat", 3.5, True, [9]]`. That flexibility has a price. The list doesn't actually store the numbers — it stores a row of *addresses*, each pointing off somewhere else in memory to a full Python object that knows its own type.

> **Definition — array (`numpy.ndarray`):** a block of memory holding many values of **one** type, laid out end to end with nothing in between.

Because every value in an array is the same type and the same size, numpy knows exactly where value number 40,000 sits: `start + 40000 × 8 bytes`. No hunting. And the actual adding is done by compiled C code that never asks "what type is this?" even once.

#### 🍕 The analogy

A Python list is a cloakroom: numbered hooks, each holding a *ticket*, and the ticket tells you which locker downstairs your coat is in. To count the red coats you fetch every ticket, walk down, open a locker, look.

A numpy array is an egg carton: twelve identical slots, twelve eggs, all touching. Counting is glancing.

```
PYTHON LIST  [1, 2, 3]
  ┌────┬────┬────┐
  │ ●  │ ●  │ ●  │   ← three addresses
  └─┬──┴─┬──┴─┬──┘
    ▼    ▼    ▼
  [int 1][int 2][int 3]   ← three separate objects, scattered, ~28 bytes each

NUMPY ARRAY  np.array([1, 2, 3])
  ┌────────┬────────┬────────┐
  │   1    │   2    │   3    │   ← the numbers themselves, 8 bytes each, side by side
  └────────┴────────┴────────┘
```

#### 🔍 Tiny concrete example

```python
import numpy as np
import time

N = 1_000_000

py_list = list(range(N))
t0 = time.perf_counter()
doubled_list = [x * 2 for x in py_list]         # the Module 3 way
t1 = time.perf_counter()

np_array = np.arange(N)
t2 = time.perf_counter()
doubled_array = np_array * 2                    # the numpy way
t3 = time.perf_counter()

print(f"list  : {1000 * (t1 - t0):6.1f} ms")
print(f"array : {1000 * (t3 - t2):6.1f} ms")
print(f"speedup: {(t1 - t0) / (t3 - t2):.0f}x")
```

Typical output (your exact numbers will differ — the *ratio* is the point):

```
list  :   19.9 ms
array :    0.8 ms
speedup: 24x
```

Memory too:

```python
import sys
print(np.array([1, 2, 3]).nbytes)                          # 24  (3 × 8 bytes)
print(sum(sys.getsizeof(i) for i in [1, 2, 3]))            # 84  (28 bytes per int object)
```

> **Definition — vectorized:** an operation written on whole arrays at once, with the looping done inside numpy's C code instead of your Python code. Your goal for this whole module is to write vectorized code.

The speed is nice. The *readability* is why you'll actually keep doing it: `celsius * 9 / 5 + 32` says what it means.

---

### 2. Creating arrays: `array`, `zeros`, `ones`, `arange`, `linspace`, `random`

#### The plain-language explanation

Six ways to make an array. You'll use all six within a month.

#### 🍕 The analogy

Six ways to get a tray of cupcakes: bring your own (`array`), an empty tray of paper cases (`zeros`), a tray of identical plain ones (`ones` / `full`), a numbered row (`arange`), an evenly-spaced row between two points (`linspace`), and a surprise assortment (`random`).

#### 🔍 Tiny concrete examples

```python
import numpy as np

a = np.array([1, 2, 3, 4])              # from a Python list
print(a)                                 # [1 2 3 4]

b = np.array([[1, 2, 3],
              [4, 5, 6]])                # from a list of lists -> 2-D
print(b)
# [[1 2 3]
#  [4 5 6]]

print(np.zeros(4))                       # [0. 0. 0. 0.]     ← floats!
print(np.zeros((2, 3)))                  # a 2-row, 3-column block of 0.0
print(np.ones(3, dtype=int))             # [1 1 1]           ← forced to int
print(np.full((2, 2), 7))                # [[7 7]
                                         #  [7 7]]
print(np.arange(0, 10, 2))               # [0 2 4 6 8]   start, stop(exclusive), step
print(np.linspace(0, 1, 5))              # [0.   0.25 0.5  0.75 1.  ]  start, stop(INCLUSIVE), how many
```

`arange` and `linspace` look similar and answer different questions:

| Function | You say | You get | Use it when |
|---|---|---|---|
| `np.arange(0, 10, 2)` | the **step** | `[0 2 4 6 8]` — stop excluded | you know the gap between values |
| `np.linspace(0, 1, 5)` | the **count** | `[0. 0.25 0.5 0.75 1.]` — stop included | you know how many points you want |

`linspace` will be your best friend when you draw smooth curves in Module 7.

**Random numbers, done properly:**

```python
rng = np.random.default_rng(42)          # 42 is the SEED
print(rng.integers(0, 10, size=5))       # [0 7 6 4 4]
print(np.round(rng.random(3), 3))        # [0.697 0.094 0.976]  floats in [0, 1)
```

> **Definition — seed:** a starting number for the random generator. Same seed → same "random" numbers, every run, on every machine.

Seeding is not cheating. It is what makes your results **reproducible** — a word you'll meet constantly from Module 8 onwards, where `random_state=42` decides which rows go into your test set. If you can't reproduce your own result, you can't debug it, and neither can anyone else.

---

### 3. `shape`, `dtype`, indexing, and 2-D slicing

#### The plain-language explanation

Every array carries four facts about itself. Print them whenever something surprises you — this is 80% of numpy debugging.

> **Definition — `shape`:** a tuple of the size in each direction. `(3, 4)` means 3 rows and 4 columns.

> **Definition — `dtype`:** the single type every element has — `int64`, `float64`, `bool`.

> **Definition — `ndim`:** how many dimensions. 1 for a row of numbers, 2 for a table.

> **Definition — `size`:** the total number of elements. For `(3, 4)` that's 12.

#### 🍕 The analogy

`shape` is the dimensions of a chocolate bar: 3 rows by 4 squares. `size` is how many squares you get. `dtype` is what the squares are made of — and a bar is all one flavour, always.

#### 🔍 Tiny concrete example

Our running example for this module — three students, four tests:

```python
scores = np.array([
    [80,  60,  90,  70],     # student 0
    [50,  40,  75,  65],     # student 1
    [95,  85, 100,  90],     # student 2
])

print(scores.shape)      # (3, 4)      3 rows, 4 columns
print(scores.dtype)      # int64
print(scores.ndim)       # 2
print(scores.size)       # 12
```

```
                 test0 test1 test2 test3     ← axis 1 runs this way ▶
              ┌──────┬─────┬─────┬─────┐
   student0   │  80  │  60 │  90 │  70 │
   student1   │  50  │  40 │  75 │  65 │     ← axis 0 runs downward ▼
   student2   │  95  │  85 │ 100 │  90 │
              └──────┴─────┴─────┴─────┘
                        shape = (3, 4)
                                 ▲  ▲
                          axis 0 ┘  └ axis 1
```

**Indexing — one comma, two numbers:**

```python
print(scores[0])          # [80 60 90 70]   ← a whole row (student 0)
print(scores[0, 2])       # 90              ← row 0, column 2. THE numpy way.
print(scores[0][2])       # 90              ← works, but slower and less clear
print(scores[-1, -1])     # 90              ← last row, last column
```

**Slicing — `:` means "everything in this direction":**

```python
print(scores[:, 1])       # [60 40 85]      ← every row, column 1  = all of test 1
print(scores[1, :])       # [50 40 75 65]   ← row 1, every column  = all of student 1
print(scores[1:, 2:])     # [[ 75  65]      ← rows 1-onward, columns 2-onward
                          #  [100  90]]
print(scores[:, -1])      # [70 65 90]      ← the last column
```

Read `scores[rows, columns]` as *"pick these rows, then within them pick these columns."*

**The `dtype` trap you must know about:**

```python
x = np.array([1, 2, 3])
print(x.dtype)            # int64
x[0] = 3.9                # assign a float into an int array...
print(x)                  # [3 2 3]   ← the .9 is GONE, silently truncated
```

No warning. No error. Just a quietly wrong number. If your data has decimals, say so up front:

```python
x = np.array([1, 2, 3], dtype=float)     # or np.array([1.0, 2, 3])
x[0] = 3.9
print(x)                                  # [3.9 2.  3. ]  ✔
print(np.array([1, 2, 3]).astype(float))  # [1. 2. 3.]  — convert an existing array
```

Note also: **division always produces floats**, even from ints.

```python
print((np.array([1, 2, 3]) / 2))          # [0.5 1.  1.5]
print((np.array([1, 2, 3]) / 2).dtype)    # float64
```

---

### 4. Elementwise math and broadcasting

#### The plain-language explanation

Arithmetic on arrays happens **elementwise**: position by position, no loop written by you.

> **Definition — elementwise:** the operation is applied to each matching pair of positions independently.

```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)      # [11 22 33 44]
print(b - a)      # [ 9 18 27 36]
print(a * b)      # [10 40 90 160]     ← NOT matrix multiplication, just position-by-position
print(b / a)      # [10. 10. 10. 10.]
print(a ** 2)     # [ 1  4  9 16]
```

But what about `a * 2`? The shapes don't match — one is four numbers, the other is one number. Numpy stretches the smaller one to fit. That stretching is **broadcasting**.

> **Definition — broadcasting:** numpy's rule for making two different-shaped arrays work together by virtually repeating the smaller one along the directions where it has size 1 (or is missing entirely).

#### 🍕 The analogy

A pizza shop puts a 10% discount on everything. You don't write "10% off" on 400 separate price tags. You write it once on a big sign and everyone understands it applies to every item. Broadcasting is the sign. Numpy doesn't actually copy the number 400 times in memory — it just reads the same value over and over, which is why it costs nothing.

#### 🔍 Tiny concrete example 1 — scalar with array (the easiest case)

```python
prices = np.array([120, 250, 80, 340])
print(prices * 0.9)        # [108. 225.  72. 306.]
print(prices + 10)         # [130 260  90 350]
```

Check one by hand: 120 × 0.9 = 108 ✔. 250 × 0.9 = 225 ✔.

#### 🔍 Tiny concrete example 2 — row with matrix

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])              # shape (2, 3)

bonus = np.array([10, 20, 30])         # shape (3,)
print(m + bonus)
# [[11 22 33]
#  [14 25 36]]
```

The row `[10, 20, 30]` got applied to **every row** of `m`. Column 0 got +10, column 1 got +20, column 2 got +30.

```
    m            bonus (stretched down)         result
[[1 2 3]    +    [[10 20 30]              =   [[11 22 33]
 [4 5 6]]         [10 20 30]]                  [14 25 36]]
   (2,3)              (3,) → (2,3)
```

#### 🔍 Tiny concrete example 3 — column with matrix

```python
per_student = np.array([[100],
                        [200]])        # shape (2, 1)  ← a COLUMN
print(m + per_student)
# [[101 102 103]
#  [204 205 206]]
```

Now it stretched sideways: row 0 got +100 everywhere, row 1 got +200 everywhere.

#### The rule, stated properly

Line the two shapes up **from the right**. For each position, they're compatible if the sizes are equal, or one of them is 1, or one shape has run out.

```
  m       (2, 3)              m         (2, 3)
  bonus      (3,)             per_stu   (2, 1)
          ───────                      ───────
 compare  3 vs 3  ✔ equal    compare   3 vs 1  ✔ one is 1 → stretch
          2 vs -  ✔ missing            2 vs 2  ✔ equal
 result  (2, 3)               result   (2, 3)
```

#### 🔍 Tiny concrete example 4 — when it refuses

```python
m + np.array([1, 2])
```

```
ValueError: operands could not be broadcast together with shapes (2,3) (2,)
```

Line them up from the right: 3 vs 2. Not equal, neither is 1. Refused.

This error is *good news*. It means numpy caught a mistake instead of silently doing something odd. When you see it, the first thing to do — always — is print both shapes:

```python
print(m.shape, np.array([1, 2]).shape)     # (2, 3) (2,)
```

Nine times out of ten you meant a column and wrote a row. Fix with `reshape`:

```python
print(m + np.array([1, 2]).reshape(2, 1))
# [[2 3 4]
#  [6 7 8]]
```

---

### 5. `axis=0` vs `axis=1`, boolean masks, and a row as a vector

#### 5a. Aggregating along an axis

> **Definition — aggregate:** squash many numbers into one — a sum, mean, min, max, or count.

With no axis, you get one number for the whole array:

```python
print(scores.sum())      # 900
print(scores.mean())     # 75.0
print(scores.max())      # 100
print(scores.min())      # 40
```

With an axis, you get one number **per row** or **per column** — and the axis you name is the one that *disappears*.

```python
print(scores.mean(axis=1))    # [75.  57.5 92.5]     ← 3 numbers = one per STUDENT
print(scores.mean(axis=0))    # [75. 61.67 88.33 75.] ← 4 numbers = one per TEST
```

#### 🍕 The analogy

`axis=0` is a hydraulic press coming down from above: it flattens all the rows together and leaves one squashed row. `axis=1` is a press coming in from the side: it flattens all the columns together and leaves one squashed column.

**The memory trick that actually works:** *the axis you name is the axis that gets eaten.*

```
scores.shape = (3, 4)          axis 0 is rows,  axis 1 is columns

  scores.mean(axis=0)  →  eats axis 0 (the 3)  →  shape (4,)  →  one number PER COLUMN
  scores.mean(axis=1)  →  eats axis 1 (the 4)  →  shape (3,)  →  one number PER ROW


           t0   t1   t2   t3
        ┌────┬────┬────┬────┐
   s0   │ 80 │ 60 │ 90 │ 70 │ ──mean(axis=1)──▶ 75.0
   s1   │ 50 │ 40 │ 75 │ 65 │ ──────────────────▶ 57.5
   s2   │ 95 │ 85 │100 │ 90 │ ──────────────────▶ 92.5
        └─┬──┴─┬──┴─┬──┴─┬──┘
          │    │    │    │
      mean(axis=0)  │    │
          ▼    ▼    ▼    ▼
        75.0 61.67 88.33 75.0
```

Everyone mixes these up at first. The cure is to **print the shape of the result** and ask "is that the number of students or the number of tests?"

Hand-check student 0: (80 + 60 + 90 + 70) / 4 = 300 / 4 = **75.0** ✔
Hand-check test 1: (60 + 40 + 85) / 3 = 185 / 3 = **61.666…** ✔

Other aggregations work the same way, plus two that return *positions* instead of values:

```python
print(scores.sum(axis=1))       # [300 230 370]
print(scores.max(axis=0))       # [ 95  85 100  90]   best score on each test
print(scores.argmax(axis=1))    # [2 2 2]             WHICH test each student did best on
print(scores.mean(axis=0).argmin())   # 1             which test was hardest (lowest average)
print(scores.std())             # 17.795130420052185  spread of all 12 scores
```

> **Definition — `argmin` / `argmax`:** returns the **index** of the smallest/largest value, not the value itself. `arg` is short for "argument", meaning "the input position that produced it."

`argmin` is how you turn a number back into a name:

```python
test_names = np.array(["Quiz", "Essay", "Practical", "Final"])
hardest = scores.mean(axis=0).argmin()
print(f"hardest test: {test_names[hardest]} (avg {scores.mean(axis=0)[hardest]:.2f})")
# hardest test: Essay (avg 61.67)
```

#### 5b. Boolean masks

> **Definition — boolean mask:** an array of `True`/`False` the same shape as your data, made by comparing the data to something. You use it to pick out elements.

```python
temps = np.array([31.2, 28.5, 35.0, 22.1, 39.4, 30.0])

mask = temps > 30
print(mask)              # [ True False  True False  True False]
print(temps[mask])       # [31.2 35.  39.4]     ← only the True positions
```

That's the whole idea, and it replaces this:

```python
hot = []
for t in temps:                # the Module 2 way
    if t > 30:
        hot.append(t)
```

Masks compose:

```python
print(mask.sum())        # 3      True counts as 1 — this COUNTS the hot days
print(mask.any())        # True   was there at least one?
print(mask.all())        # False  were they all?
print(temps[mask].mean())# 35.199999999999996   average of just the hot days
print(temps.mean())      # 31.033333333333335   average of all days
```

**Combining conditions — and the parentheses that everyone forgets:**

```python
print(temps[(temps > 25) & (temps < 35)])     # [31.2 28.5 30. ]
print(temps[(temps < 25) | (temps > 38)])     # [22.1 39.4]
print(temps[~(temps > 30)])                   # [28.5 22.1 30. ]   ~ means NOT
```

| Python (Module 2) | NumPy on arrays |
|---|---|
| `and` | `&` |
| `or` | `\|` |
| `not` | `~` |

⚠️ **You must wrap each comparison in parentheses.** `temps > 25 & temps < 35` fails with a confusing error, because `&` binds tighter than `>`. Write `(temps > 25) & (temps < 35)`. Every time.

⚠️ **You cannot use `and`/`or` on arrays.** `(temps > 25) and (temps < 35)` raises *"The truth value of an array with more than one element is ambiguous."* Python's `and` wants one True/False and you handed it six.

**`np.where` — the vectorized if/else:**

```python
print(np.where(temps > 30, "hot", "ok"))
# ['hot' 'ok' 'hot' 'ok' 'hot' 'ok']

print(np.where(temps > 30, temps, 0))
# [31.2  0.  35.   0.  39.4  0. ]
```

Read it as: *where the condition is True use the second thing, otherwise use the third.*

#### 5c. A row of numbers is a vector

> **Definition — vector:** a list of numbers describing one thing. Three test scores, two map coordinates, four measurements of a flower — each is a vector, and a vector is exactly one row of your array.

This is the bridge to machine learning, so slow down here.

If a point on a map is `[3, 4]`, how far is it from the origin `[0, 0]`? Pythagoras: √(3² + 4²) = √25 = 5.

```python
v = np.array([3, 4])
print(np.sqrt((v ** 2).sum()))    # 5.0
```

Read that inside-out: square each element → `[9, 16]`; sum them → `25`; square root → `5.0`.

The distance between two vectors is the same idea on their difference:

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
diff = a - b                       # [-3 -3 -3]
print(np.sqrt((diff ** 2).sum()))  # 5.196152422706632
```

By hand: differences −3, −3, −3. Squares 9, 9, 9. Sum 27. √27 = 5.196… ✔

> **Definition — Euclidean distance:** the straight-line distance between two vectors: square the differences, add them up, take the square root. It works in 2 dimensions, in 3, and in 300 — the formula never changes.

Write it as a function you'll reuse:

```python
def distance(a, b):
    """Euclidean distance between two equal-length vectors."""
    return np.sqrt(((a - b) ** 2).sum())
```

In Module 8 you'll build a model whose entire idea is: *to guess the label of a new thing, find the rows with the smallest distance to it.* You just wrote the engine.

One more operation worth naming, because it shows up in every neural network in Level 3:

```python
print((a * b).sum())    # 32     multiply position-by-position, then add up
print(a @ b)            # 32     the same thing, spelled with @
```

By hand: 1×4 + 2×5 + 3×6 = 4 + 10 + 18 = **32** ✔

> **Definition — dot product:** multiply two vectors position by position and add the results. One number out.

---

## 🔍 Worked Example

**The question:** *Given the 3×4 score table, find each student's average, each test's average, the hardest test, every score rescaled to 0–1, and how many scores were passes (≥ 70).*

We'll do every step by hand first, then confirm with code.

### Step 0 — the data

|  | test0 | test1 | test2 | test3 |
|---|---|---|---|---|
| **student0** | 80 | 60 | 90 | 70 |
| **student1** | 50 | 40 | 75 | 65 |
| **student2** | 95 | 85 | 100 | 90 |

`shape = (3, 4)`, `size = 12`, `dtype = int64`

### Step 1 — per-student averages (`axis=1`, eats the 4 columns → 3 numbers)

```
student0: (80 + 60 + 90 + 70) / 4 = 300 / 4 = 75.0
student1: (50 + 40 + 75 + 65) / 4 = 230 / 4 = 57.5
student2: (95 + 85 + 100 + 90) / 4 = 370 / 4 = 92.5
```

`scores.mean(axis=1)` → `[75.  57.5 92.5]`, shape `(3,)` ✔ three students, three numbers.

### Step 2 — per-test averages (`axis=0`, eats the 3 rows → 4 numbers)

```
test0: (80 + 50 + 95) / 3 = 225 / 3 = 75.0
test1: (60 + 40 + 85) / 3 = 185 / 3 = 61.666...
test2: (90 + 75 + 100) / 3 = 265 / 3 = 88.333...
test3: (70 + 65 + 90) / 3 = 225 / 3 = 75.0
```

`scores.mean(axis=0)` → `[75. 61.66666667 88.33333333 75.]`, shape `(4,)` ✔

**Cross-check that catches most axis mistakes:** the sum of the row means times 4 must equal the sum of the column means times 3, because both equal the grand total.
Rows: (75 + 57.5 + 92.5) × 4 = 225 × 4 = 900.
Columns: (75 + 61.667 + 88.333 + 75) × 3 = 300 × 3 = 900. ✔
And `scores.sum()` = 900 ✔

### Step 3 — the hardest test

The smallest column mean is 61.667, at index **1**.

```python
scores.mean(axis=0).argmin()      # 1
```

So test1 is hardest. Note `argmin` gave us `1`, the *position* — not `61.667`, the value. That position is what lets you look up the test's name.

### Step 4 — rescale every score to 0–1 (min-max normalization)

> **Definition — min–max normalization:** slide and squash a set of numbers so the smallest becomes 0 and the largest becomes 1, using `(x − min) / (max − min)`.

Global min = 40, global max = 100, so range = 100 − 40 = **60**.

```
80 → (80 − 40) / 60 = 40 / 60 = 0.6667
60 → (60 − 40) / 60 = 20 / 60 = 0.3333
90 → (90 − 40) / 60 = 50 / 60 = 0.8333
70 → (70 − 40) / 60 = 30 / 60 = 0.5000
50 → (50 − 40) / 60 = 10 / 60 = 0.1667
40 → (40 − 40) / 60 =  0 / 60 = 0.0000   ← the minimum always lands on 0
75 → (75 − 40) / 60 = 35 / 60 = 0.5833
65 → (65 − 40) / 60 = 25 / 60 = 0.4167
95 → (95 − 40) / 60 = 55 / 60 = 0.9167
85 → (85 − 40) / 60 = 45 / 60 = 0.7500
100 → (100 − 40) / 60 = 60 / 60 = 1.0000  ← the maximum always lands on 1
90 → (90 − 40) / 60 = 50 / 60 = 0.8333
```

Twelve divisions by hand. In numpy it's **one line**, and broadcasting does all twelve:

```python
normalized = (scores - scores.min()) / (scores.max() - scores.min())
```

```
[[0.66666667 0.33333333 0.83333333 0.5       ]
 [0.16666667 0.         0.58333333 0.41666667]
 [0.91666667 0.75       1.         0.83333333]]
```

Every hand value matches. `scores.min()` is a single number (a scalar), so it broadcasts across all 12 positions; so does the range. Two scalars, twelve results, zero loops.

You'll meet this exact formula again in Module 8 as the reason distance-based models need scaling.

### Step 5 — the pass mask (≥ 70)

```
[[80≥70 T, 60≥70 F, 90≥70 T, 70≥70 T],
 [50≥70 F, 40≥70 F, 75≥70 T, 65≥70 F],
 [95≥70 T, 85≥70 T, 100≥70 T, 90≥70 T]]
```

```python
passed = scores >= 70
print(passed)
print(passed.sum())            # 8      total passes
print(passed.sum(axis=1))      # [3 1 4]  passes per student
print(passed.sum(axis=0))      # [2 1 3 2] passes per test
```

Hand count: row 0 has T,F,T,T = 3 ✔. Row 1 has F,F,T,F = 1 ✔. Row 2 is all four = 4 ✔. Total 3 + 1 + 4 = **8** ✔ — and 2 + 1 + 3 + 2 = 8 too, which is the same cross-check as Step 2.

⚠️ Note `70 >= 70` is `True`. That's the difference between `>` and `>=` and it changes the answer by one whole score. Decide which you mean *before* you type it.

### Step 6 — the honest caution

Three students is not a class, and "test1 is the hardest" rests on three scores. Also notice student2 scored highest on every single test — with data this small, one strong student can drag every "test difficulty" number around. Real conclusions need real sample sizes, which is exactly why the mini-project uses ten students and the capstone demands a hundred rows.

---

## 💻 Hands-On

Create `module05/`. Write one file, `arrays_tour.py`, and run it. Predict each output before you look.

```python
"""arrays_tour.py — a guided tour of numpy. Run it, then change the numbers and run it again."""

import numpy as np

# ============================================================ 1. CREATING
print("=" * 60)
print("1. CREATING ARRAYS")
print("=" * 60)

a = np.array([1, 2, 3, 4])                 # from a list
print("from list     :", a)
print("zeros(4)      :", np.zeros(4))                    # floats
print("ones(3,int)   :", np.ones(3, dtype=int))
print("full((2,2),7) :\n", np.full((2, 2), 7))
print("arange(0,10,2):", np.arange(0, 10, 2))            # step given
print("linspace(0,1,5):", np.linspace(0, 1, 5))          # count given

rng = np.random.default_rng(42)            # seeded -> same numbers every run
print("rng.integers  :", rng.integers(0, 10, size=5))
print("rng.random    :", np.round(rng.random(3), 3))

# =========================================================== 2. INSPECTING
print("\n" + "=" * 60)
print("2. SHAPE, DTYPE, INDEXING, SLICING")
print("=" * 60)

scores = np.array([
    [80,  60,  90,  70],                   # student 0
    [50,  40,  75,  65],                   # student 1
    [95,  85, 100,  90],                   # student 2
])

print("shape :", scores.shape)             # (3, 4)
print("dtype :", scores.dtype)             # int64
print("ndim  :", scores.ndim)              # 2
print("size  :", scores.size)              # 12

print("scores[0]     :", scores[0])        # whole row
print("scores[0, 2]  :", scores[0, 2])     # single cell
print("scores[:, 1]  :", scores[:, 1])     # whole column
print("scores[-1, -1]:", scores[-1, -1])   # bottom-right
print("scores[1:, 2:]:\n", scores[1:, 2:]) # bottom-right block

# ======================================================== 3. ELEMENTWISE
print("\n" + "=" * 60)
print("3. ELEMENTWISE MATH AND BROADCASTING")
print("=" * 60)

x = np.array([1, 2, 3, 4])
y = np.array([10, 20, 30, 40])
print("x + y  :", x + y)                   # [11 22 33 44]
print("x * y  :", x * y)                   # position by position
print("x ** 2 :", x ** 2)
print("y / x  :", y / x)                   # always float

print("scores + 5 (scalar broadcast):\n", scores + 5)

curve = np.array([0, 5, 0, 10])            # shape (4,) -> one bonus per TEST
print("curve shape:", curve.shape, " scores shape:", scores.shape)
print("scores + curve (row broadcast down):\n", scores + curve)

effort = np.array([[1], [2], [3]])         # shape (3,1) -> one bonus per STUDENT
print("scores + effort (column broadcast across):\n", scores + effort)

try:
    scores + np.array([1, 2, 3])           # (3,4) vs (3,) -> 4 vs 3, refused
except ValueError as e:
    print("broadcast refused:", e)

# ======================================================== 4. AGGREGATING
print("\n" + "=" * 60)
print("4. AGGREGATING ALONG AN AXIS")
print("=" * 60)

print("whole-array sum :", scores.sum())            # 900
print("whole-array mean:", scores.mean())           # 75.0

student_avg = scores.mean(axis=1)                   # eats axis 1 -> one per STUDENT
test_avg = scores.mean(axis=0)                      # eats axis 0 -> one per TEST
print("mean(axis=1) shape", student_avg.shape, "->", student_avg)
print("mean(axis=0) shape", test_avg.shape, "->", np.round(test_avg, 2))

# the cross-check: both routes must reach the same grand total
print("check:", student_avg.sum() * 4, "==", test_avg.sum() * 3, "==", scores.sum())

test_names = np.array(["Quiz", "Essay", "Practical", "Final"])
hardest = test_avg.argmin()
print(f"hardest test: index {hardest} = {test_names[hardest]} (avg {test_avg[hardest]:.2f})")

# ============================================================ 5. MASKS
print("\n" + "=" * 60)
print("5. BOOLEAN MASKS")
print("=" * 60)

temps = np.array([31.2, 28.5, 35.0, 22.1, 39.4, 30.0])
hot = temps > 30
print("temps :", temps)
print("mask  :", hot)
print("hot days      :", temps[hot])
print("how many hot  :", hot.sum())
print("any hot?      :", hot.any(), "  all hot?", hot.all())
print("mean of hot   :", round(temps[hot].mean(), 2))
print("mean of all   :", round(temps.mean(), 2))
print("25 < t < 35   :", temps[(temps > 25) & (temps < 35)])     # parentheses required
print("t<25 or t>38  :", temps[(temps < 25) | (temps > 38)])
print("NOT hot       :", temps[~hot])
print("labelled      :", np.where(temps > 30, "hot", "ok"))

passed = scores >= 70
print("pass mask:\n", passed)
print("passes total:", passed.sum(),
      " per student:", passed.sum(axis=1),
      " per test:", passed.sum(axis=0))

# =========================================================== 6. VECTORS
print("\n" + "=" * 60)
print("6. A ROW IS A VECTOR")
print("=" * 60)


def distance(p, q):
    """Euclidean distance between two equal-length vectors."""
    return np.sqrt(((p - q) ** 2).sum())


print("length of [3,4]         :", distance(np.array([3, 4]), np.array([0, 0])))
print("distance [1,2,3]-[4,5,6]:", round(distance(np.array([1, 2, 3]),
                                                  np.array([4, 5, 6])), 4))

# how similar are student 0 and student 2, as score-vectors?
print("student0 vs student1:", round(distance(scores[0], scores[1]), 2))
print("student0 vs student2:", round(distance(scores[0], scores[2]), 2))
print("dot product [1,2,3]·[4,5,6]:", np.array([1, 2, 3]) @ np.array([4, 5, 6]))

# ====================================================== 7. NORMALIZATION
print("\n" + "=" * 60)
print("7. NORMALIZATION IN ONE LINE")
print("=" * 60)

normalized = (scores - scores.min()) / (scores.max() - scores.min())
print("min", scores.min(), " max", scores.max(), " range", scores.max() - scores.min())
print(np.round(normalized, 4))
print("normalized min/max:", normalized.min(), normalized.max())
```

### Expected output

```
============================================================
1. CREATING ARRAYS
============================================================
from list     : [1 2 3 4]
zeros(4)      : [0. 0. 0. 0.]
ones(3,int)   : [1 1 1]
full((2,2),7) :
 [[7 7]
 [7 7]]
arange(0,10,2): [0 2 4 6 8]
linspace(0,1,5): [0.   0.25 0.5  0.75 1.  ]
rng.integers  : [0 7 6 4 4]
rng.random    : [0.697 0.094 0.976]

============================================================
2. SHAPE, DTYPE, INDEXING, SLICING
============================================================
shape : (3, 4)
dtype : int64
ndim  : 2
size  : 12
scores[0]     : [80 60 90 70]
scores[0, 2]  : 90
scores[:, 1]  : [60 40 85]
scores[-1, -1]: 90
scores[1:, 2:]:
 [[ 75  65]
 [100  90]]

============================================================
3. ELEMENTWISE MATH AND BROADCASTING
============================================================
x + y  : [11 22 33 44]
x * y  : [ 10  40  90 160]
x ** 2 : [ 1  4  9 16]
y / x  : [10. 10. 10. 10.]
scores + 5 (scalar broadcast):
 [[ 85  65  95  75]
 [ 55  45  80  70]
 [100  90 105  95]]
curve shape: (4,)  scores shape: (3, 4)
scores + curve (row broadcast down):
 [[ 80  65  90  80]
 [ 50  45  75  75]
 [ 95  90 100 100]]
scores + effort (column broadcast across):
 [[ 81  61  91  71]
 [ 52  42  77  67]
 [ 98  88 103  93]]
broadcast refused: operands could not be broadcast together with shapes (3,4) (3,) 

============================================================
4. AGGREGATING ALONG AN AXIS
============================================================
whole-array sum : 900
whole-array mean: 75.0
mean(axis=1) shape (3,) -> [75.  57.5 92.5]
mean(axis=0) shape (4,) -> [75.   61.67 88.33 75.  ]
check: 900.0 == 900.0 == 900
hardest test: index 1 = Essay (avg 61.67)

============================================================
5. BOOLEAN MASKS
============================================================
temps : [31.2 28.5 35.  22.1 39.4 30. ]
mask  : [ True False  True False  True False]
hot days      : [31.2 35.  39.4]
how many hot  : 3
any hot?      : True   all hot? False
mean of hot   : 35.2
mean of all   : 31.03
25 < t < 35   : [31.2 28.5 30. ]
t<25 or t>38  : [22.1 39.4]
NOT hot       : [28.5 22.1 30. ]
labelled      : ['hot' 'ok' 'hot' 'ok' 'hot' 'ok']
pass mask:
 [[ True False  True  True]
 [False False  True False]
 [ True  True  True  True]]
passes total: 8  per student: [3 1 4]  per test: [2 1 3 2]

============================================================
6. A ROW IS A VECTOR
============================================================
length of [3,4]         : 5.0
distance [1,2,3]-[4,5,6]: 5.1962
student0 vs student1: 39.37
student0 vs student2: 36.74
dot product [1,2,3]·[4,5,6]: 32

============================================================
7. NORMALIZATION IN ONE LINE
============================================================
min 40  max 100  range 60
[[0.6667 0.3333 0.8333 0.5   ]
 [0.1667 0.     0.5833 0.4167]
 [0.9167 0.75   1.     0.8333]]
normalized min/max: 0.0 1.0
```

### Things worth staring at

- **`scores + curve` vs `scores + effort`.** Same array, two different bonus shapes, two completely different meanings. A `(4,)` row means *per test*; a `(3,1)` column means *per student*. Getting this wrong is a silent, plausible-looking bug — check the shape, always.
- **Student 0 is *closer* to student 2 (36.74) than to student 1 (39.37)** — even though student 2 beat them on every single test and student 1 lost on every single test. Check it: `scores[0] - scores[1]` is `[30 20 15 5]`, so √(900+400+225+25) = √1550 = 39.37. And `scores[0] - scores[2]` is `[-15 -25 -10 -20]`, so √(225+625+100+400) = √1350 = 36.74. Distance doesn't care about *direction*, only about size, so it can call "much better than you" a nearer neighbour than "a bit worse than you". **Remember that when Module 8 asks you to trust "nearest".**
- **`check: 900.0 == 900.0 == 900`.** Build the habit of printing a cross-check line. Axis bugs don't announce themselves.

---

## ✍️ Practice

Work in `module05/`. `import numpy as np` at the top of everything. **No `for` loops over the data in any of these** unless the exercise explicitly asks for one.

### 1. [Warm-up] Six arrays, four facts

Create six arrays: one from a list of 5 numbers, `np.zeros((3, 2))`, `np.ones(4, dtype=int)`, `np.arange(5, 26, 5)`, `np.linspace(-1, 1, 9)`, and `rng.integers(1, 7, size=(2, 3))` with seed 0. For each, print its `shape`, `dtype`, `ndim`, and `size` on one labelled line.

**Done looks like:** six labelled lines, and you can say out loud why `np.zeros((3,2)).dtype` is `float64` while `np.ones(4, dtype=int).dtype` is `int64`.

### 2. [Warm-up] Celsius to Fahrenheit with a mask

Given `c = np.array([21.0, 25.5, 30.0, 38.2, 41.0, 15.5, 33.3])`, convert to Fahrenheit with one vectorized line. Then print how many days were above 100 °F, and the **Celsius** values of exactly those days.

**Done looks like:** the count is `2` and the Celsius values printed are `[38.2 41.0]`. Zero loops, zero `if` statements.

### 3. [Build] Rainfall grid

Build this 4-weeks × 7-days rainfall array (millimetres):

```python
rain = np.array([
    [ 0.0, 12.5,  3.0,  0.0,  8.2,  0.0,  1.5],
    [22.0,  5.5,  0.0,  0.0,  0.0,  4.4,  9.1],
    [ 0.0,  0.0, 18.7,  6.3,  0.0,  0.0,  0.0],
    [ 3.3,  7.7, 11.1,  0.0,  2.2, 15.0,  0.0],
])
days = np.array(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
```

Report: total rain per week; average rain per day-of-week; the name of the wettest day-of-week; which week number (1–4) was driest; and how many completely dry days there were in the month.

**Done looks like:** weekly totals `[25.2 41. 25. 39.3]`, wettest day-of-week `Wed`, driest week `3`, and `13` dry days. State which axis you used for each answer and why.

### 4. [Build] Per-column normalization with broadcasting

Given this 5×3 array where the columns are on wildly different scales:

```python
m = np.array([
    [10., 200.,  3.],
    [20., 150.,  9.],
    [30., 300.,  6.],
    [40., 100., 12.],
    [50., 250., 15.],
])
```

Normalize **each column separately** to 0–1 using `(m - col_min) / (col_max - col_min)`, with no loops. Then prove it worked by printing the min and max of each column of the result.

**Done looks like:** `n.min(axis=0)` prints `[0. 0. 0.]` and `n.max(axis=0)` prints `[1. 1. 1.]`, and you can explain in one sentence what shapes broadcast together to make it work.

### 5. [Stretch] Nearest neighbours by hand

Given six points and one query point:

```python
points = np.array([[1., 2.], [4., 6.], [0., 0.], [3., 3.], [7., 1.], [2., 5.]])
query = np.array([2., 3.])
```

Compute the distance from `query` to **all six** points in one vectorized expression (no loop). Then print the three closest points and their distances, in order.

**Done looks like:** the three nearest are `[3,3]` at distance `1.0`, `[1,2]` at `1.4142`, and `[2,5]` at `2.0`. Verify the first one by hand on paper. *(You have just written the core of a k-nearest-neighbors model — hold that thought until Module 8.)*

### 6. [Stretch] Prove the speedup

Compute the sum of the squares of the first 1,000,000 whole numbers (0 through 999,999) two ways: with a plain Python `for` loop, and with numpy. Time both with `time.perf_counter()`. Print both answers, assert they're equal, and print the speedup as a multiple.

**Done looks like:** both give `333332833333500000`, the assert passes, and you print a speedup of roughly 20–60× (your machine's number will differ). Write one sentence explaining where the saved time actually went.

---

## 🤔 Think Deeper

### 1. Min–max normalization uses the largest and smallest values. What happens when one of them is a typo?

*How to reason about it:* take the 3×4 score table and change one score from 100 to 1000 (a slipped finger on the keyboard). Recompute the normalized array. Notice that *every one of the twelve numbers* changes, and eleven of them get squashed into the bottom tenth of the range. Then ask the general question: which statistics does one bad value destroy, and which shrug it off? Compute the mean and the median of a column before and after. This is why "look at your data before you scale it" is a rule, and it will come back in Module 8 when you choose between `MinMaxScaler` and `StandardScaler`.

### 2. Broadcasting silently succeeded, but did it do what you meant?

*How to reason about it:* `scores + curve` and `scores + effort` both run without error, and both produce a full 3×4 array of plausible-looking numbers. Only one is the bonus you intended. Ask: if numpy *had* raised an error, would you have found the bug faster? Consider the trade-off between a helpful language that guesses and a strict language that refuses. Then invent a rule you'll actually follow — for instance, "print the shape of anything I'm about to broadcast" — and decide whether you'd rather have your tools be convenient or safe when the answer will be published.

### 3. A school wants to rank teachers by their students' average scores. What does the array *not* contain?

*How to reason about it:* the array holds only scores. List five things it does not hold that would change the ranking — who taught which students, class sizes, how many students started the year behind, whether one class had a substitute for six weeks, whether the tests were the same. Now consider that the arithmetic is *perfectly correct* either way: `mean(axis=0)` cannot be wrong. Getting the maths right and getting the answer right are different achievements, and confusing them is how bad decisions get a spreadsheet to hide behind.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `axis=0` when you wanted per-row results | The names sound backwards: axis 0 is *rows*, but naming it collapses the rows | Remember **the axis you name is the axis that disappears**, then check `result.shape` against your row/column count |
| `ValueError: operands could not be broadcast together with shapes (3,4) (3,)` | You passed a per-row vector where numpy expects it lined up from the right | `print(a.shape, b.shape)`, then `b.reshape(-1, 1)` to make it a column |
| `TypeError` or a strange error from `temps > 25 & temps < 35` | `&` binds tighter than `>`, so Python evaluates `25 & temps` first | Parenthesise every comparison: `(temps > 25) & (temps < 35)` |
| `ValueError: The truth value of an array with more than one element is ambiguous` | You used `and`/`or`/`if` on a whole array | Use `&`, `\|`, `~` for elementwise; use `.any()` or `.all()` when you genuinely need one True/False |
| A decimal you stored vanished: `x[0] = 3.9` gave `3` | The array's `dtype` is `int64` and assignment truncates without warning | Create it as float: `np.array([1, 2, 3], dtype=float)` or `.astype(float)` |
| `argmax` gave 2 and you printed it as if it were a score | `argmax` returns a *position*, `max` returns a *value* | Use the position to look up: `names[scores.argmax()]` |
| Writing a `for` loop over array rows out of habit | It's what Modules 2–3 taught, and it works | Before writing any loop, ask "is there an axis argument or a mask for this?" — there usually is |
| `np.zeros(3)` gave floats when you wanted ints | `zeros`/`ones`/`empty` default to `float64` | Pass `dtype=int` |
| Comparing floats with `==` and getting `False` for equal-looking numbers | Float arithmetic has tiny rounding errors | Use `np.isclose(a, b)` or `np.allclose(arr1, arr2)` instead of `==` |

---

## 🛠️ Mini-Project — Vectorized Gradebook

### Goal

Build a **10 students × 5 tests** score array and answer eight questions about it using **zero `for` loops over the data**. Every result must be cross-checked against a value you computed by hand.

(You may loop for *printing* the final report — printing isn't computing.)

### The data

Use exactly this so your numbers match the checks below:

```python
import numpy as np

names = np.array(["Aarav", "Bela", "Chen", "Divya", "Emeka",
                  "Farah", "Gita", "Hugo", "Ivy", "Jai"])

tests = np.array(["Quiz1", "Quiz2", "Midterm", "Project", "Final"])

scores = np.array([
    [72, 65, 58, 88, 70],     # Aarav
    [90, 84, 77, 95, 92],     # Bela
    [55, 48, 40, 70, 61],     # Chen
    [83, 79, 66, 91, 85],     # Divya
    [61, 57, 52, 80, 68],     # Emeka
    [95, 92, 88, 99, 97],     # Farah
    [78, 70, 63, 85, 74],     # Gita
    [45, 38, 30, 62, 50],     # Hugo
    [88, 81, 72, 93, 89],     # Ivy
    [67, 60, 55, 76, 71],     # Jai
])
```

### Starter steps

**Step 1 — verify the shape (5 min).** Print `scores.shape`, `scores.dtype`, `scores.size`. Assert the shape is `(10, 5)` and that `len(names) == scores.shape[0]` and `len(tests) == scores.shape[1]`. If these don't line up, every later answer is wrong in a way that looks fine.

**Step 2 — per-student averages (10 min).** One line with an axis. Print each student's name and average, sorted highest first (use `np.argsort`, and remember `[::-1]` reverses).

**Step 3 — per-test averages (10 min).** One line with the *other* axis. Print each test's name and average.

**Step 4 — hardest and easiest test (10 min).** Use `argmin`/`argmax` on the test averages and print the names, not the indices.

**Step 5 — normalize (20 min).** Do it **twice**:
- globally: `(scores - scores.min()) / (scores.max() - scores.min())`
- per test: subtract each test's min and divide by each test's range, using broadcasting from `axis=0` aggregates

Print both, rounded to 3 decimals, and write a comment explaining when you'd want each. (Hint: per-test normalization answers *"how did this student do relative to everyone on this test?"*; global normalization answers *"how big is this score on the school's overall scale?"*)

**Step 6 — pass/fail mask (15 min).** Passing is ≥ 60. Print the boolean mask, the total number of passes, passes per student, passes per test, and the names of students who passed **everything** (`mask.all(axis=1)` as a mask on `names`).

**Step 7 — two more of your own (20 min).** For example: who was above the class average? Which student improved most from Quiz1 to Final? Which test had the widest spread (`ptp` or `max - min` along an axis)?

**Step 8 — hand-check and report (20 min).** In comments, show the arithmetic for student 1 (Aarav) and test 1 (Quiz1). Then print a tidy report.

### Cross-check values (yours must match)

| Quantity | Value |
|---|---|
| `scores.shape` | `(10, 5)` |
| Aarav's average | `70.6` — because 72 + 65 + 58 + 88 + 70 = 353, and 353 / 5 = 70.6 |
| Quiz1 average | `73.4` — because the column sums to 734, and 734 / 10 = 73.4 |
| All student averages | `[70.6 87.6 54.8 80.8 63.6 94.2 74. 45. 84.6 65.8]` |
| All test averages | `[73.4 67.4 60.1 83.9 75.7]` |
| Hardest test | `Midterm` (60.1) |
| Easiest test | `Project` (83.9) |
| Global min / max | `30` / `99` |
| Class mean | `72.1` |
| Passes (≥ 60) per student | `[4 5 2 5 3 5 5 1 5 4]` |
| Passes per test | `[8 7 5 10 9]` |
| Passed everything | `Bela, Divya, Farah, Gita, Ivy` |

Note the two pass-count rows both add to 39. If yours don't, you have an axis bug.

### Success criteria checklist

- [ ] `grep -c "for " gradebook.py` finds loops only in printing sections — none doing arithmetic on `scores`
- [ ] Every one of the eight answers matches the cross-check table
- [ ] Student 1 and Test 1 are verified by hand, with the arithmetic written in a comment
- [ ] Both normalizations produced, with a comment saying when each is the right choice
- [ ] Names are printed, never bare indices — `argmin` output is always looked up
- [ ] A printed cross-check line proving `student_avg.sum() * 5 == test_avg.sum() * 10 == scores.sum()`
- [ ] A `# WHAT THIS ARRAY DOESN'T KNOW` comment listing three things about these students that no score can capture

### 🚀 Level it up

Add **z-score standardization** alongside min–max:

```python
z = (scores - scores.mean(axis=0)) / scores.std(axis=0)
```

> **Definition — z-score:** how many standard deviations a value sits above (+) or below (−) the mean of its column.

Print the z-scores rounded to 2 decimals. Check that each column of `z` now has mean ≈ 0 (use `np.round(z.mean(axis=0), 10)`) and standard deviation ≈ 1. Then answer: *which single score in the whole gradebook is the most unusual for its test?* Use `np.abs(z).argmax()` together with `np.unravel_index` to turn that flat position back into a (student, test) pair:

```python
flat = np.abs(z).argmax()
row, col = np.unravel_index(flat, z.shape)
print(f"most unusual: {names[row]} on {tests[col]} (z = {z[row, col]:.2f})")
```

This is exactly `StandardScaler` from scikit-learn, which you'll call by name in Module 8. You just built it in one line.

---

## 🔑 Key Takeaways

- A numpy **array** stores one type in one contiguous block, which is why it's roughly 20–50× faster than a list and uses a fraction of the memory.
- **Vectorized** code — `celsius * 9 / 5 + 32` — replaces the loop, and reads like the formula it is. If you're writing a `for` loop over numbers, stop and look for the array version.
- Always know your `shape` and `dtype`. Printing them is the first move in every numpy bug you will ever have.
- **Broadcasting** stretches a smaller array to fit a bigger one, comparing shapes from the right. It's what makes `(scores - min) / range` work on 12 numbers at once — and it will silently do the *wrong* stretch if you hand it a row where you meant a column.
- **The axis you name is the axis that disappears.** `mean(axis=0)` collapses rows and gives one number per column; `mean(axis=1)` collapses columns and gives one number per row.
- **Boolean masks** replace `if` inside loops: `temps[temps > 30]`. Combine with `&`, `|`, `~` — never `and`, `or`, `not` — and parenthesise every comparison.
- A **row of numbers is a vector**, and the **Euclidean distance** between two vectors is `np.sqrt(((a - b) ** 2).sum())`. That one line is the whole engine of the first model you'll train.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| array (`ndarray`) | A grid of numbers all of the same type, stored side by side | `np.array([[1,2],[3,4]])` |
| vectorized | Doing the maths on the whole array at once, no loop written by you | `c * 9/5 + 32` |
| `shape` | How many rows and columns — the array's dimensions | `(3, 4)` = 3 rows, 4 columns |
| `dtype` | The one type every element has | `int64`, `float64`, `bool` |
| `ndim` | How many dimensions: 1 = a row, 2 = a table | `scores.ndim` → `2` |
| `size` | Total number of elements | `(3,4)` → `12` |
| `arange` | Counts from start to stop, taking a **step** you choose | `np.arange(0,10,2)` → `[0 2 4 6 8]` |
| `linspace` | Puts a **count** of evenly spaced points between two ends | `np.linspace(0,1,5)` |
| seed | A starting number that makes "random" repeatable | `np.random.default_rng(42)` |
| elementwise | Position by position, independently | `[1,2] * [3,4]` → `[3,8]` |
| broadcasting | Stretching a smaller array to fit a bigger one | `scores + 5`, `scores + [0,5,0,10]` |
| axis | A direction through the array: 0 = down the rows, 1 = across the columns | `mean(axis=0)` |
| aggregate | Squash many numbers into one | `sum`, `mean`, `min`, `max`, `std` |
| `argmin` / `argmax` | The **position** of the smallest / biggest value | `[9,3,7].argmin()` → `1` |
| boolean mask | A True/False array used to pick elements out | `temps[temps > 30]` |
| vector | One row of numbers describing one thing | `[80, 60, 90, 70]` = one student |
| Euclidean distance | Straight-line distance: square, add, square-root | `√((1-4)² + (2-5)²)` |
| dot product | Multiply position by position, then add it all up | `[1,2,3] @ [4,5,6]` → `32` |
| min–max normalization | Squash numbers so the smallest is 0 and the largest is 1 | `(x - min) / (max - min)` |
| z-score | How many standard deviations from the mean | `(x - mean) / std` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Six arrays, four facts

```python
import numpy as np

rng = np.random.default_rng(0)

arrays = {
    "from list      ": np.array([3, 1, 4, 1, 5]),
    "zeros((3,2))   ": np.zeros((3, 2)),
    "ones(4,int)    ": np.ones(4, dtype=int),
    "arange(5,26,5) ": np.arange(5, 26, 5),
    "linspace(-1,1,9)": np.linspace(-1, 1, 9),
    "rng.integers   ": rng.integers(1, 7, size=(2, 3)),
}

for label, a in arrays.items():
    print(f"{label} shape={str(a.shape):<8} dtype={str(a.dtype):<8} "
          f"ndim={a.ndim}  size={a.size}")
```

Output:

```
from list       shape=(5,)    dtype=int64    ndim=1  size=5
zeros((3,2))    shape=(3, 2)  dtype=float64  ndim=2  size=6
ones(4,int)     shape=(4,)    dtype=int64    ndim=1  size=4
arange(5,26,5)  shape=(5,)    dtype=int64    ndim=1  size=5
linspace(-1,1,9) shape=(9,)   dtype=float64  ndim=1  size=9
rng.integers    shape=(2, 3)  dtype=int64    ndim=2  size=6
```

*(The exact column spacing depends on your f-string — the four facts are what matter.)*

**Why `zeros` is float and `ones(4, dtype=int)` is int:** `np.zeros` and `np.ones` default to `float64`, because most numeric work involves decimals and a float can hold any small integer exactly. Passing `dtype=int` overrides the default. `np.array([3,1,4,1,5])` looks at what you actually gave it — all whole numbers — and picks `int64`.

**Why `arange(5, 26, 5)` has 5 elements:** it produces 5, 10, 15, 20, 25 and stops *before* 26. The stop value is always excluded. If you'd written `arange(5, 25, 5)` you'd have got only four values, which is the classic off-by-one from Module 2 wearing a new hat.

---

### 2. [Warm-up] Celsius to Fahrenheit with a mask

```python
import numpy as np

c = np.array([21.0, 25.5, 30.0, 38.2, 41.0, 15.5, 33.3])

f = c * 9 / 5 + 32                     # one vectorized line, all 7 at once
print("Fahrenheit:", np.round(f, 2))

hot = f > 100                          # boolean mask, same shape as f
print("mask      :", hot)
print("count     :", hot.sum())        # True counts as 1
print("celsius of hot days:", c[hot])  # index the ORIGINAL array with the mask
```

Output:

```
Fahrenheit: [ 69.8   77.9   86.   100.76 105.8   59.9   91.94]
mask      : [False False False  True  True False False]
count     : 2
celsius of hot days: [38.2 41. ]
```

**Hand check:** 38.2 × 9 / 5 = 343.8 / 5 = 68.76, + 32 = **100.76** ✔ (just over 100).
And 21.0 × 9 / 5 = 37.8, + 32 = **69.8** ✔

**The key move** is `c[hot]`, not `f[hot]`. The mask was *built* from `f` but has the same shape as `c`, so it can index either. Building a mask from one array and applying it to a matching one is a pattern you'll use constantly — in Module 6 it becomes `df[df["temp_f"] > 100]`.

---

### 3. [Build] Rainfall grid

```python
import numpy as np

rain = np.array([
    [ 0.0, 12.5,  3.0,  0.0,  8.2,  0.0,  1.5],
    [22.0,  5.5,  0.0,  0.0,  0.0,  4.4,  9.1],
    [ 0.0,  0.0, 18.7,  6.3,  0.0,  0.0,  0.0],
    [ 3.3,  7.7, 11.1,  0.0,  2.2, 15.0,  0.0],
])
days = np.array(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

# axis=1 eats the 7 days -> one total per WEEK
weekly = rain.sum(axis=1)
print("weekly totals :", weekly)

# axis=0 eats the 4 weeks -> one average per DAY-OF-WEEK
daily = rain.mean(axis=0)
print("daily averages:", np.round(daily, 3))

wettest = daily.argmax()
print(f"wettest day-of-week: {days[wettest]} ({daily[wettest]:.2f} mm avg)")

driest = weekly.argmin()
print(f"driest week: week {driest + 1} ({weekly[driest]:.1f} mm)")

dry_days = (rain == 0).sum()
print("completely dry days:", dry_days)
print("month total:", rain.sum())
```

Output:

```
weekly totals : [25.2 41.  25.  39.3]
daily averages: [6.325 6.425 8.2   1.575 2.6   4.85  2.65 ]
wettest day-of-week: Wed (8.20 mm avg)
driest week: week 3 (25.0 mm)
completely dry days: 13
month total: 130.5
```

**Axis reasoning, stated:**

| Question | Axis | Why |
|---|---|---|
| total per week | `axis=1` | a week is a *row*; collapse the 7 days inside it |
| average per day-of-week | `axis=0` | a day-of-week is a *column*; collapse the 4 weeks |
| dry-day count | none | count over the whole grid, so no axis |

**Hand check — week 1:** 0 + 12.5 + 3.0 + 0 + 8.2 + 0 + 1.5 = 25.2 ✔
**Hand check — Wednesday:** (3.0 + 0.0 + 18.7 + 11.1) / 4 = 32.8 / 4 = 8.2 ✔
**Cross-check:** weekly totals sum to 25.2 + 41.0 + 25.0 + 39.3 = 130.5, and `rain.sum()` = 130.5 ✔

**A caution about `driest + 1`:** `argmin` returns a 0-based index, and humans number weeks from 1. That `+ 1` is a translation between machine counting and human counting, and forgetting it is one of the most common off-by-one bugs there is. Say what your numbers mean in the label.

⚠️ Also note `(rain == 0)` works here because these values were typed in as exact literals like `0.0`. For *computed* floats you'd use `np.isclose(rain, 0)` instead — `0.1 + 0.2 == 0.3` is `False` in every language that uses floats.

---

### 4. [Build] Per-column normalization with broadcasting

```python
import numpy as np

m = np.array([
    [10., 200.,  3.],
    [20., 150.,  9.],
    [30., 300.,  6.],
    [40., 100., 12.],
    [50., 250., 15.],
])

col_min = m.min(axis=0)             # shape (3,) -> [ 10. 100.   3.]
col_max = m.max(axis=0)             # shape (3,) -> [ 50. 300.  15.]
print("col_min:", col_min, " shape", col_min.shape)
print("col_max:", col_max, " shape", col_max.shape)

n = (m - col_min) / (col_max - col_min)
print(np.round(n, 3))

print("column mins:", n.min(axis=0))     # [0. 0. 0.]
print("column maxs:", n.max(axis=0))     # [1. 1. 1.]
```

Output:

```
col_min: [ 10. 100.   3.]  shape (3,)
col_max: [ 50. 300.  15.]  shape (3,)
[[0.    0.5   0.   ]
 [0.25  0.25  0.5  ]
 [0.5   1.    0.25 ]
 [0.75  0.    0.75 ]
 [1.    0.75  1.   ]]
column mins: [0. 0. 0.]
column maxs: [1. 1. 1.]
```

**The broadcast, spelled out:**

```
m         (5, 3)
col_min      (3,)
          ───────
compare   3 vs 3  ✔ equal
          5 vs -  ✔ col_min has no second dimension, so it repeats down all 5 rows
result    (5, 3)
```

So `col_min` is virtually stacked five times, once per row, and each column gets subtracted by its own minimum. One line, fifteen subtractions and fifteen divisions.

**Hand check — row 0, column 1:** (200 − 100) / (300 − 100) = 100 / 200 = **0.5** ✔
**Hand check — row 3, column 1:** (100 − 100) / 200 = **0.0** ✔ (it's the column minimum, so it must land on 0.)

**Why per-column and not global:** globally the min is 3 and the max is 300, so column 0 (10–50) would be squashed into 0.023–0.157 and column 2 (3–15) into 0.0–0.04. Both would become almost invisible next to column 1. Per-column normalization gives each measurement an equal say — which is precisely why Module 8 insists you scale features before a distance-based model.

**A trap to know about:** if any column were constant (say every value 7), then `col_max - col_min` would be 0 and you'd divide by zero, producing `nan`. Real cleaning code checks for that:

```python
rng_ = col_max - col_min
rng_[rng_ == 0] = 1              # a constant column normalizes to all-zeros instead of nan
n = (m - col_min) / rng_
```

---

### 5. [Stretch] Nearest neighbours by hand

```python
import numpy as np

points = np.array([[1., 2.], [4., 6.], [0., 0.], [3., 3.], [7., 1.], [2., 5.]])
query = np.array([2., 3.])

# points is (6,2), query is (2,) -> broadcasts across all six rows
diffs = points - query                       # (6, 2)
dists = np.sqrt((diffs ** 2).sum(axis=1))    # axis=1 eats the x,y pair -> (6,)
print("distances:", np.round(dists, 4))

order = np.argsort(dists)                    # positions, nearest first
print("order    :", order)

print("three nearest:")
for rank, i in enumerate(order[:3], start=1):     # printing loop, not a computing loop
    print(f"  {rank}. point {points[i]} at distance {dists[i]:.4f}")
```

Output:

```
distances: [1.4142 3.6056 3.6056 1.     5.3852 2.    ]
order    : [3 0 5 1 2 4]
three nearest:
  1. point [3. 3.] at distance 1.0000
  2. point [1. 2.] at distance 1.4142
  3. point [2. 5.] at distance 2.0000
```

**Hand check — point `[3, 3]` vs query `[2, 3]`:**

```
differences: 3 − 2 = 1,  3 − 3 = 0
squares:     1,          0
sum:         1
√1 =         1.0     ✔
```

**Hand check — point `[1, 2]`:** differences −1 and −1 → squares 1 and 1 → sum 2 → √2 = 1.41421… ✔

**The shape story, step by step** — this is the part worth internalising:

```
points        (6, 2)
query            (2,)          broadcasts: 2 vs 2 ✔, then 6 vs missing ✔
points - query (6, 2)          six difference-vectors
** 2           (6, 2)          all squared
.sum(axis=1)   (6,)            axis 1 (the x,y pair) is eaten -> one number per point
np.sqrt        (6,)            six distances
```

If you accidentally wrote `.sum(axis=0)` you'd get **two** numbers instead of six, and they'd be meaningless. That's exactly why the checklist says *print the shape and ask whether it's the number of points*.

**Note there's a tie:** points `[4,6]` and `[0,0]` are both at distance 3.6056. `argsort` breaks the tie by original order, arbitrarily. In Module 8, a tie like this among the k nearest neighbours can decide a prediction — and "the model picked whichever row happened to come first in the file" is not a satisfying explanation for a decision about a person.

---

### 6. [Stretch] Prove the speedup

```python
import numpy as np
import time

N = 1_000_000

# --- the Python way ---------------------------------------------------
t0 = time.perf_counter()
total_py = 0
for i in range(N):
    total_py += i * i
t1 = time.perf_counter()

# --- the numpy way ----------------------------------------------------
t2 = time.perf_counter()
a = np.arange(N)
total_np = (a * a).sum()
t3 = time.perf_counter()

loop_time = t1 - t0
np_time = t3 - t2

print("python loop answer:", total_py)
print("numpy answer      :", total_np)
assert total_py == total_np, "the two answers disagree!"

print(f"python loop : {loop_time:.4f} s")
print(f"numpy       : {np_time:.4f} s")
print(f"speedup     : {loop_time / np_time:.0f}x")
```

Output (your times will differ; the ratio is what matters):

```
python loop answer: 333332833333500000
numpy answer      : 333332833333500000
python loop : 0.0490 s
numpy       : 0.0012 s
speedup     : 41x
```

**Where the time went.** In the Python loop, each of the million turns does a lot of invisible work: fetch the next integer object, check that `*` is defined for its type, allocate a *new* integer object to hold `i * i`, check `+=` for the accumulator's type, allocate another object. Roughly five bookkeeping steps per one arithmetic step. In numpy, `a * a` hands the whole million-element block to a compiled C loop that already knows every value is an `int64`, so it does one multiply per element with no type checking and no object allocation — and then `.sum()` does the same for the addition.

**One honest caveat:** numpy allocates a temporary million-element array to hold `a * a` before summing it. For arrays big enough to strain your memory, `np.dot(a, a)` or `(a.astype(np.int64) ** 2).sum()` behave differently on memory. At this size it makes no practical difference, but "vectorized" doesn't mean "free" — it means "the loop moved somewhere faster."

**And a correctness caveat worth knowing:** this sum reaches 3.3 × 10¹⁷, which fits comfortably inside `int64`'s limit of about 9.2 × 10¹⁸. Push `N` to 10 million and numpy will silently **overflow and wrap around to a wrong answer**, while Python's own integers grow as large as they need to. Vectorized code is faster, but it inherits the fixed-size types that make it fast. Add `a = np.arange(N, dtype=np.float64)` if you need the headroom, and accept a little rounding instead.

</details>

---

[⬅ Previous](module-04-dictionaries-and-datasets.md) · [Level 2 Home](README.md) · [Next ➡](module-06-pandas-tables.md)
