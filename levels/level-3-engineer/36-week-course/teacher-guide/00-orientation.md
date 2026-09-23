# 📕 Teacher Orientation — Everything You Need, Including the Maths

### *Read this once, cover to cover, with a pen and a piece of paper. About two hours. Then you can teach all 36 weeks — including the derivatives, the matrix shapes and the backpropagation.*

[⬅ Course home](../README.md) · [Week 1 teacher guide](week-01.md) · [Week 1 student guide](../student-guide/week-01.md) · [Figure style guide](../figures/STYLE.md)

---

## 🪝 You Do Not Need to Know Calculus to Teach This

Let me be completely direct about the thing you are probably worried about.

Level 3 contains derivatives, gradients, matrix multiplication and backpropagation. Those four words
are why adults quietly hand this material to somebody else. So here is the actual situation:

> **Every piece of maths in this course is arithmetic. All of it. There is not one symbolic
> manipulation in the whole year that a student is required to perform.**

A derivative, in this course, is this: you have a number. You nudge it by one thousandth. You see how
much the answer moved. You divide. That is the whole thing, and it is not a simplification — it is
what the word means, and it is how every neural network on earth is checked for correctness.

Here it is, right now, in six lines you can run in the next thirty seconds:

```python
def height(x):
    return x * x

h = 0.001
up   = height(3 + h)
down = height(3 - h)
print("how far up:", up - down, "  how far along:", 2 * h)
print("slope at x = 3 is", round((up - down) / (2 * h), 6))
```

```text
how far up: 0.011999999999998678   how far along: 0.002
slope at x = 3 is 6.0
```

**That is a derivative.** A calculus textbook would tell you the derivative of `x²` is `2x`, and at
`x = 3` that is 6. Same number. The textbook gets it faster; you got it by measuring, and you can
explain what it *means*, which is the part that matters here and the part that most people who learned
the rules cannot do.

So: you will not learn calculus in this file. You will learn to **measure slopes with subtraction and
division**, and that is genuinely, sufficiently, all of it.

### What is actually being asked of you

| You do NOT need to | You DO need to |
|---|---|
| Know calculus | Be able to subtract, divide, and read a table of numbers |
| Know linear algebra notation | Be able to count rows and columns in a grid |
| Know Python before you start | Read §2 of this file once, with a pen |
| Know what a neural network is | Believe, out loud, that "I don't know, let's measure it" is a good sentence |
| Get every answer right in class | Do the week's arithmetic yourself, on paper, before class. **This is the non-negotiable one.** |
| Be fast | Be willing to be slow in public |

### One warning, and it is the important one

Every teacher file in this course opens with a section called **🧑‍🏫 The Maths You Need, Taught To You
First**. On the fifteen weeks that carry a new mathematical idea, that section is long — sometimes
250 lines — and it teaches you the idea from nothing, on real numbers, with the arithmetic done out.

**Do not skim it. Do it.** With a pencil, on paper, the night before. It takes 15 to 25 minutes.

The reason is not that you might be asked a question you cannot answer — that is fine, and §9 tells you
exactly what to say. The reason is that **a student can tell the difference between an adult who has
done the arithmetic and an adult who has read about it**, within about ninety seconds, and what they
conclude is *"this is the kind of thing you read about, not the kind of thing you do."* That conclusion
is the failure mode of this entire level.

Do the arithmetic. It is six numbers. You will be fine.

---
---

# 📖 Section 1 — Maths for the Absolute Beginner, in Twelve Pages

Everything mathematical in Level 3, from nothing. Every single example in this section was actually run
on a computer and the output pasted, so if you follow along you will get the same numbers.

You need: a pencil, paper, and a calculator with `e^x` and `ln` on it (your phone has one).

> **📌 About the code blocks in this file.** Within a numbered sub-section, **each block carries on
> from the one above it** — the `import` lines and the data are typed once, in the first block that
> needs them, exactly as they would be in a single file you build up as you go. If you copy one block
> on its own and get `NameError: name 'np' is not defined`, that is why, and nothing is broken. Copy
> the sub-section's blocks in order into one file and it runs. Every output shown below is the real
> output of doing exactly that, with a seed set.

---

## 1.1 — What a function is

A **function** is a rule with an input and an output. Put a number in, get a number out. Same number
in, same number out, every time.

That is it. No graphs yet, no notation yet.

Here is one: *"predicted exam mark = 8 times the hours you studied, plus 12."*

```python
def marks(hours):
    return 8 * hours + 12

for h in [0, 1, 2, 3, 5]:
    print("hours:", h, " predicted marks:", marks(h))
```

```text
hours: 0  predicted marks: 12
hours: 1  predicted marks: 20
hours: 2  predicted marks: 28
hours: 3  predicted marks: 36
hours: 5  predicted marks: 52
```

Three words for the same idea, all of which appear in this course:

| Written as | Read as | Means |
|---|---|---|
| `marks(3)` | "marks of three" | put 3 in, get the answer out |
| `f(x) = 8x + 12` | "f of x equals…" | the same rule, with shorter names |
| `y = 8x + 12` | — | the same rule again, from Level 2 |

**The two numbers in that rule have names, and they will not change all year.** The `8` is called the
**weight** — how much the answer moves for every one unit of input. The `12` is called the **bias** —
where the answer starts when the input is zero. A neural network with 3,000 numbers in it has 3,000 of
exactly these two things and nothing else.

> **🔢 The maths, slowly:** the whole of machine learning is: *"I have a rule with some numbers in it.
> I do not know the right numbers. Find them by trying and correcting."* That is the sentence. Every
> remaining page in this section is machinery for the words "trying and correcting".

---

## 1.2 — Reading a graph, and the only two questions to ask

Six students told us how many hours they studied and what they scored:

| hours | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| marks | 22 | 30 | 33 | 45 | 51 | 62 |

Drawn on graph paper: hours goes along the bottom, marks goes up the side, and each student is one dot.

**The only two questions you ever ask about a graph in this course:**

1. **What is one dot?** (Here: one student.) If you cannot answer this, nothing else on the chart means
   anything, and this is the single most common thing students skip.
2. **Which way is up?** (Here: up = more marks; right = more hours.) Every chart in this course labels
   both axes, because a chart without labels is a decoration.

Now the useful part. Our rule from 1.1 said `marks = 8 × hours + 12`. Is `8` a good weight? Try three:

```python
import numpy as np
hours = np.array([1, 2, 3, 4, 5, 6])
marks = np.array([22, 30, 33, 45, 51, 62])

for m in [6.0, 7.0, 8.0]:
    pred = m * hours + 12
    err = np.abs(pred - marks).mean()
    print(f"slope m = {m}:  predictions {pred}  mean absolute error {err:.4f}")
```

```text
slope m = 6.0:  predictions [18. 24. 30. 36. 42. 48.]  mean absolute error 7.5000
slope m = 7.0:  predictions [19. 26. 33. 40. 47. 54.]  mean absolute error 4.0000
slope m = 8.0:  predictions [20. 28. 36. 44. 52. 60.]  mean absolute error 1.8333
```

**8 is better than 7 is better than 6.** We now have a *number that says how wrong we are* — 1.8333
marks off, on average — and we can compare guesses. That number has a name that runs through the whole
year: it is the **loss**.

> **loss** — one number saying how wrong the model currently is. Lower is better. Zero is perfect.

---

## 1.3 — Slope of a straight line: rise over run

Your student already met this in Level 2 as `y = mx + c`. Reminding yourself takes ninety seconds.

Take two points on a straight line. Point A is at `(1, 20)`. Point B is at `(4, 44)`.

```
   how far UP  did we go from A to B?   44 − 20 = 24     ← the RISE
   how far ALONG did we go from A to B?  4 −  1 =  3     ← the RUN
   slope = rise ÷ run = 24 ÷ 3 = 8
```

```python
x1, y1 = 1.0, 20.0
x2, y2 = 4.0, 44.0
print("rise =", y2 - y1)
print("run  =", x2 - x1)
print("slope = rise / run =", (y2 - y1) / (x2 - x1))
```

```text
rise = 24.0
run  = 3.0
slope = rise / run = 8.0
```

**Slope 8 means: every one step to the right, the line goes up eight.** And the sign matters more than
the size:

| Slope | The line is | Walking to the right takes you |
|---|---|---|
| `+8` | going up | **up** |
| `−8` | going down | **down** |
| `0` | flat | nowhere — you are at the top or the bottom |

Hold on to the last row. **A slope of zero means you have arrived**, and that fact is what tells a
neural network to stop.

---

## 1.4 — Slope of a *curve*, at one single point — the whole trick

A straight line has one slope everywhere. A curve does not: `x²` is nearly flat near zero and very
steep out at `x = 5`. So "the slope of a curve" is a meaningless question. **"The slope of a curve at
one particular point"** is the real question, and here is how you answer it with subtraction.

> **The trick:** to find the slope at `x = 3`, do not look at the whole curve. Look at `x = 2.999` and
> `x = 3.001` — a hair either side. Between two points that close together, *any* curve is
> indistinguishable from a straight line. So use rise over run on those two points.

```python
def height(x):
    return x * x

for x in [1.0, 3.0, 5.0]:
    h = 0.001
    up   = height(x + h)
    down = height(x - h)
    slope = (up - down) / (2 * h)
    print("at x =", x, " f(x+h) =", up, " f(x-h) =", down, " slope =", round(slope, 6))
```

```text
at x = 1.0  f(x+h) = 1.0020009999999997  f(x-h) = 0.998001  slope = 2.0
at x = 3.0  f(x+h) = 9.006001  f(x-h) = 8.994001  slope = 6.0
at x = 5.0  f(x+h) = 25.010001000000003  f(x-h) = 24.990000999999996  slope = 10.0
```

**Do the middle row by hand right now.** It takes twenty seconds and it is the most valuable twenty
seconds in this file:

```
   f(3.001) = 3.001 × 3.001 = 9.006001
   f(2.999) = 2.999 × 2.999 = 8.994001
   rise = 9.006001 − 8.994001 = 0.012
   run  = 3.001 − 2.999      = 0.002
   slope = 0.012 ÷ 0.002 = 6
```

Now look at the three answers: at `x = 1` the slope is 2, at `x = 3` it is 6, at `x = 5` it is 10.

**2, 6, 10 — that is exactly two times x, every time.** You have just discovered, by measuring, the
first rule of calculus: the slope of `x²` at any point is `2x`. A calculus class states that rule and
proves it. You measured it. Both are correct; only one of them is memorable.

> **This number has a name.** The slope of a function at one point is called its **derivative**. That
> is the whole definition. Week 12 introduces the word in exactly this order — measure first, name
> second — and **the word must never appear in your classroom before the arithmetic has.**

Two practical notes you will need in class:

1. **Why `h = 0.001` and not `h = 0.000001`?** Because computers store numbers with limited precision.
   Look at `f(x+h) = 1.0020009999999997` above — that trailing `...97` should be a clean `1.002001`.
   With a tiny enough `h` you are subtracting two nearly-identical numbers and the noise swamps the
   answer. `0.001` is the sweet spot and this course uses it everywhere.
2. **Why nudge *both* ways** — `(f(x+h) − f(x−h)) / 2h` rather than `(f(x+h) − f(x)) / h`? Because
   straddling the point is more accurate. Both work; the straddling version is what Weeks 12, 18 and 20
   use, and it is why the number above came out as an exact `6.0`.

---

## 1.5 — "The slope tells you which way is downhill" — and that is the whole of machine learning

This is the single most important page in this file. Take your time.

Go back to the six students. We want the best weight `m` in `marks = m × hours + 12`. Let us make the
loss into a *hill* by computing it for lots of values of `m`:

```python
import numpy as np
hours = np.array([1, 2, 3, 4, 5, 6])
marks = np.array([22, 30, 33, 45, 51, 62])

def error_for(m):
    """Average squared miss if we predict marks = m * hours + 12."""
    pred = m * hours + 12
    return float(((pred - marks) ** 2).mean())

print(" slope m    average squared error")
for m in [5.0, 6.0, 7.0, 7.5, 8.0, 8.5, 9.0, 10.0]:
    print(f"   {m:>4.1f}         {error_for(m):>10.4f}")
```

```text
 slope m    average squared error
    5.0           148.3333
    6.0            69.8333
    7.0            21.6667
    7.5            8.9583
    8.0            3.8333
    8.5            6.2917
    9.0            16.3333
   10.0           59.1667
```

**Sketch that on graph paper.** `m` along the bottom, error up the side. It is a valley — steep on the
left, steep on the right, with a bottom somewhere near `m = 8`. Machine learning people call it the
**loss surface**, and finding its bottom is the entire job.

Now: suppose you are standing at `m = 5` and you cannot see the whole valley — you only know the error
right where you are. **Which way should you step?** Measure the slope, exactly as in 1.4:

```python
h = 0.001
for m in [5.0, 8.0, 10.0]:
    slope = (error_for(m + h) - error_for(m - h)) / (2 * h)
    direction = "go RIGHT (increase m)" if slope < 0 else "go LEFT (decrease m)"
    print(f"at m = {m:>4.1f}  slope of the error hill = {slope:>9.4f}   ->  {direction}")
```

```text
at m =  5.0  slope of the error hill =  -93.6667   ->  go RIGHT (increase m)
at m =  8.0  slope of the error hill =   -2.6667   ->  go RIGHT (increase m)
at m = 10.0  slope of the error hill =   58.0000   ->  go LEFT (decrease m)
```

Read that table out loud. At `m = 5` the slope is **negative**, meaning walking right takes you *down*
— so increase `m`. At `m = 10` the slope is **positive**, meaning walking right takes you *up* — so
decrease `m`. At `m = 8` the slope is only `−2.6667`, nearly flat: we are almost at the bottom.

**In every case: step in the opposite direction to the slope.** That sentence, written as arithmetic,
is the most important line in the level:

```
   new value  =  old value  −  (step size) × (slope)
```

Do it eight times and watch:

```python
def slope_at(m, h=0.001):
    return (error_for(m + h) - error_for(m - h)) / (2 * h)

m = 5.0
lr = 0.02
print(f"{'step':>4} {'m':>8} {'error':>10} {'slope':>10}")
for step in range(9):
    print(f"{step:>4} {m:>8.4f} {error_for(m):>10.4f} {slope_at(m):>10.4f}")
    m = m - lr * slope_at(m)
```

```text
step        m      error      slope
   0   5.0000   148.3333   -93.6667
   1   6.8733    26.0900   -36.8422
   2   7.6102     7.1776   -14.4913
   3   7.9000     4.2516    -5.6999
   4   8.0140     3.7990    -2.2420
   5   8.0588     3.7289    -0.8818
   6   8.0765     3.7181    -0.3469
   7   8.0834     3.7164    -0.1364
   8   8.0861     3.7162    -0.0537
```

It found `m ≈ 8.086`. Brute-force search over two thousand values of `m` says the true best is
`8.088`, with error `3.7161`. **The eight-step walk got there.**

> ### 🔑 That table is machine learning. All of it.
>
> Everything else in this level — sigmoid, log loss, layers, backpropagation, PyTorch, CNNs — is
> machinery for doing that same walk when there are 3,000 knobs instead of one. The walk never changes.
> **Measure the slope. Step against it. Repeat.**

Three names for things in that table, which you now own:

> **loss** — the error number. The height of the hill.
> **learning rate** — the `0.02`. Your stride length. Too small and you crawl; too big and you leap
> over the valley and up the far side (Week 15 shows this happening on purpose).
> **gradient descent** — the name of the whole walk.

And two failure modes you will see in class, both of which are now obvious:

| Symptom | What is happening | Fix |
|---|---|---|
| The error barely moves over 500 steps | Stride far too small | Multiply the learning rate by 10 |
| The error goes 35 → 6906 → 1359681 → `inf` → `nan` | Stride so big it leaps up the far wall, every time, getting worse | Divide the learning rate by 10 |

---

## 1.6 — A grid of numbers, and its shape

Weeks 16 to 27 are about grids. Here is everything you need, and it is genuinely small.

A **grid of numbers** is numbers in rows and columns. Its **shape** is `(how many rows, how many
columns)` — rows first, always, no exceptions.

Start a file called `grids.py`. Sections 1.6 and 1.7 build it up together.

```python
import numpy as np
A = np.array([[1, 2],
              [3, 4],
              [5, 6]])
print("A =")
print(A)
print("A.shape =", A.shape)
```

```text
A =
[[1 2]
 [3 4]
 [5 6]]
A.shape = (3, 2)
```

**Three rows, two columns: shape `(3, 2)`.** Count them on the printout. That is the entire concept.

The formal word is **matrix**, and this course says "grid" first and "matrix" second, all year.

What makes shapes worth a page is not the idea, it is the habit:

> ### 🔑 In this level, `print(x.shape)` is a reflex, not a debugging step.
>
> Roughly half of all errors from Week 16 onwards are a shape that is not what somebody assumed. The
> teacher files print shapes constantly and on purpose. When a student is stuck and you do not know
> why, **"what shape is it?"** is your single most productive sentence, and it works even when you have
> no idea what the code does.

Three shapes with a meaning attached, so the numbers stop being abstract:

| Shape | In this course, that is |
|---|---|
| `(1797, 64)` | 1,797 handwritten digits, each flattened into 64 pixel values |
| `(1797, 1, 8, 8)` | the same digits kept as pictures: 1,797 images, 1 colour channel, 8 tall, 8 wide |
| `(64, 32)` | one layer's weights: 64 numbers coming in, 32 going out |

---

## 1.7 — Multiplying two grids, and why the inner numbers must match

This is the one piece of notation in the level that looks like real maths. It is a bookkeeping rule.

To multiply grid `A` by grid `B`, you take **one row of A and one column of B**, multiply them
position by position, and add the results up. That one number goes in the output.
```
   A is (3, 2)          B is (2, 4)
   ┌───┬───┐            ┌────┬────┬────┬────┐
   │ 1 │ 2 │            │ 10 │ 20 │ 30 │ 40 │
   ├───┼───┤            ├────┼────┼────┼────┤
   │ 3 │ 4 │            │ 50 │ 60 │ 70 │ 80 │
   ├───┼───┤            └────┴────┴────┴────┘
   │ 5 │ 6 │
   └───┴───┘

   Row 0 of A is (1, 2).   Column 0 of B is (10, 50).
   1 × 10  +  2 × 50  =  10 + 100  =  110       ← goes in output position (0, 0)
```

Carry on in `grids.py`, below what you already have:

```python
B = np.array([[10, 20, 30, 40],
              [50, 60, 70, 80]])
print("B.shape =", B.shape)
C = A @ B
print("C = A @ B")
print(C)
print("C.shape =", C.shape)
print("--- one cell by hand: row 0 of A, column 0 of B ---")
print(1 * 10 + 2 * 50)
```

```text
B.shape = (2, 4)
C = A @ B
[[110 140 170 200]
 [230 300 370 440]
 [350 460 570 680]]
C.shape = (3, 4)
--- one cell by hand: row 0 of A, column 0 of B ---
110
```

**Check a second cell yourself.** Output position (1, 2) uses row 1 of A, which is `(3, 4)`, and column
2 of B, which is `(30, 70)`: `3 × 30 + 4 × 70 = 90 + 280 = 370`. Look at the printout — row 1, column
2 is `370`. It works.

### The shape rule, and it is the only rule

```
   (3, 2) @ (2, 4)  →  (3, 4)
       ▲    ▲
       └────┘
    these two MUST be equal.
    they vanish. the outer two survive.
```

Row 0 of A has two numbers in it. Column 0 of B has two numbers in it. You can pair them up. If B had
three rows, you could not — one number would have no partner, and there is no sensible thing to do
about that. So numpy refuses. Add one more line to the bottom of `grids.py`:

```python
print((B @ A).shape)     # B is (2, 4), A is (3, 2) — 4 does not match 3
```

```text
Traceback (most recent call last):
  File "/private/tmp/l3g/grids.py", line 19, in <module>
    print((B @ A).shape)     # B is (2, 4), A is (3, 2) — 4 does not match 3
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 3 is different from 4)
```

That last line is ugly and you can ignore nearly all of it. **`size 3 is different from 4`** is the
message. Four wanted to meet three, and could not.

> **🧑‍🏫 If a student asks** *"so why is the order allowed to matter? 3 × 4 and 4 × 3 are the same!"* —
> For plain numbers, yes. For grids, no, and this is one of the two genuinely surprising facts in the
> level. `A @ B` and `B @ A` are different operations and usually one of them does not even exist. Do
> not smooth this over; write both shapes on the board and let it be strange.

**Every use of `@` in this course means the same thing in English:** *"push a whole batch of examples
through a whole layer of a network, all at once."* Week 17 makes that sentence concrete. Until then,
"grid times grid, inner numbers must match" is all you need.

---

## 1.8 — Averaging errors, and the trap in it

We need one number for "how wrong were we over five students". There is a trap, and it takes thirty
seconds to fall into:

```python
import numpy as np
truth      = np.array([58, 71, 64, 80, 49])
prediction = np.array([60, 65, 64, 88, 55])
error = prediction - truth
print("errors        :", error)
print("sum of errors :", error.sum(), "  <-- the cancelling trap")
print("absolute errors:", np.abs(error))
print("MAE  =", np.abs(error).mean())
print("squared errors:", error ** 2)
print("MSE  =", (error ** 2).mean())
print("RMSE =", np.sqrt((error ** 2).mean()))
```

```text
errors        : [ 2 -6  0  8  6]
sum of errors : 10   <-- the cancelling trap
absolute errors: [2 6 0 8 6]
MAE  = 4.4
squared errors: [ 4 36  0 64 36]
MSE  = 28.0
RMSE = 5.291502622129181
```

**The trap:** the raw errors are `2, −6, 0, 8, 6`. Some are too high, some too low, and adding them lets
them cancel. A model that is 40 marks over on one student and 40 under on another would score a perfect
zero. So you must remove the signs, and there are exactly two ways:

| Name | What you do | The number here | Meaning in plain English |
|---|---|---|---|
| **MAE** — mean absolute error | Drop the minus signs, average | `4.4` | "typically we are 4.4 marks out" |
| **MSE** — mean squared error | Square them, average | `28.0` | in *squared marks*, which nobody can picture |
| **RMSE** | Square-root the MSE | `5.2915` | back in marks, but big misses punished harder |

MAE is the one to say out loud to a human, because it is in the units of the thing itself. MSE is the
one the maths prefers, because squaring makes a smooth curve you can measure the slope of — which is
exactly what 1.5 needed. Both appear in this course and the teacher files say which and why.

> **🔢 The maths, slowly:** check `MAE = 4.4` by hand. `2 + 6 + 0 + 8 + 6 = 22`, and `22 ÷ 5 = 4.4`.
> Then MSE: `4 + 36 + 0 + 64 + 36 = 140`, and `140 ÷ 5 = 28`. Every formula in this course gets this
> treatment, every time, in front of the student.

---

## 1.9 — Two special numbers: `e` and `ln`

Weeks 13 and 14 need these. They are calculator buttons and you will not need to know why they exist.

**`e` is a number: 2.718281828…** — like π, it just has that value. It shows up in the S-shaped
squasher that turns any score into a probability.

**`ln` is the "un-do" button for `e`.** `ln(x)` answers: "e to what power gives me x?"

The only two things you need to be able to read:

```python
import numpy as np
for z in [-2.0, 0.0, 1.4, 3.0]:
    print("z =", z, " e**(-z) =", round(float(np.exp(-z)), 6),
          " sigmoid =", round(float(1 / (1 + np.exp(-z))), 6))
```

```text
z = -2.0  e**(-z) = 7.389056  sigmoid = 0.119203
z = 0.0  e**(-z) = 1.0  sigmoid = 0.5
z = 1.4  e**(-z) = 0.246597  sigmoid = 0.802184
z = 3.0  e**(-z) = 0.049787  sigmoid = 0.952574
```

**The sigmoid** is `1 ÷ (1 + e^(−z))`. Feed it any number at all and out comes something between 0 and
1, which is what a probability has to be. Note `sigmoid(0) = 0.5` exactly — a raw score of zero means
"no idea". Big positive score → near 1. Big negative → near 0. That is Week 13, and there is nothing
more to it than that table.

```python
for p in [0.9, 0.5, 0.1, 0.02]:
    print("p =", p, " -ln(p) =", round(float(-np.log(p)), 6))
```

```text
p = 0.9  -ln(p) = 0.105361
p = 0.5  -ln(p) = 0.693147
p = 0.1  -ln(p) = 2.302585
p = 0.02  -ln(p) = 3.912023
```

**`−ln(p)` is a surprise meter**, and Week 14 teaches it exactly that way. You said 90% and it
happened: surprise 0.105, barely a shrug. You said 2% and it happened: surprise 3.912, you were
astonished, and you should be penalised heavily. That is **log loss**, and the whole reason classifiers
use it is that it punishes *confident* wrongness rather than merely wrongness.

Memorise one number: **0.6931**. That is `−ln(0.5)`, the loss of a model answering "50/50" to
everything. When a student's loss sits at `0.6931` and will not move, the model has learned nothing at
all, and you can diagnose that from across the room. It happens roughly four times a year.

---

## 1.10 — Slopes multiply along a chain — all of backpropagation, in one page

Week 18 is the hardest week in the level and this is its whole content.

Suppose two things happen in a row: `w` affects `z`, and `z` affects `L`. You want to know how much `w`
affects `L`. The answer is you **multiply the two slopes**.

🍕 **Analogy that works with students:** every extra hour of rain adds 3 minutes of traffic. Every extra
minute of traffic adds 2 pizzas going cold. So every extra hour of rain costs 6 cold pizzas. You did
not need to know anything about pizza and rain directly — you chained through traffic.

Now with real numbers. Let `z = 3w + 1` and `L = z²`, starting at `w = 2`:

```python
def forward(w):
    z = 3 * w + 1          # first stage
    L = z * z              # second stage
    return z, L

w = 2.0
z, L = forward(w)
print("w =", w, " z =", z, " L =", L)

h = 0.001
z_up, _ = forward(w + h)
z_dn, _ = forward(w - h)
dz_dw = (z_up - z_dn) / (2 * h)
print("slope of z with respect to w :", round(dz_dw, 6))

dL_dz = ((z + h) ** 2 - (z - h) ** 2) / (2 * h)
print("slope of L with respect to z :", round(dL_dz, 6))

print("multiply them              :", round(dz_dw * dL_dz, 6))

_, L_up = forward(w + h)
_, L_dn = forward(w - h)
print("measured straight through   :", round((L_up - L_dn) / (2 * h), 6))
```

```text
w = 2.0  z = 7.0  L = 49.0
slope of z with respect to w : 3.0
slope of L with respect to z : 14.0
multiply them              : 42.0
measured straight through   : 42.0
```

**Read the last two lines again.** Multiplying the two stage-slopes gave 42. Measuring the whole thing
in one go gave 42. They agree, and they always will.

That is the **chain rule**. In a calculus class it is a symbolic rule with brackets in it. Here it is
"stage slopes multiply, and you can check it by measuring".

> ### 🔑 And that is backpropagation.
>
> A neural network is a chain of stages: input → layer 1 → squash → layer 2 → loss. To find out how
> much one weight buried in layer 1 contributed to the final error, you multiply the slopes along the
> path from that weight to the error. Doing it for every weight at once, sweeping backwards from the
> loss, is called **backpropagation** — and it is called "back" because you start at the error and walk
> towards the inputs, reusing what you already computed instead of starting over for each weight.
>
> **The phrase to use in class, all year, is "how much did each knob contribute to the error".** Not
> "the chain rule". The chain rule is the arithmetic; blame assignment is the meaning.

**And the check.** Because you can also measure the answer directly by nudging (`42.0`, above), you can
always verify a hand-derived gradient. That check is called a **gradient check**, students do it in
Weeks 18, 19 and 20, and it is why nobody in this course ever has to *trust* their calculus. They test
it. If the two numbers agree to six decimal places, the derivation is right. If not, it is wrong. There
is no ambiguity and no appeal to authority, and that is a very good thing to hand a fourteen-year-old.

---
---

# 🐍 Section 2 — Python and PyTorch for the Absolute Beginner

Enough to read every line of code in this course. If you have taught Level 2, skim 2.1–2.4 and read
2.5 onwards properly.

## 2.1 — Variables, lists, loops, functions

```python
# --- variables ---
name = "Asha"
hours = 4
rate = 7.5
print(name, "studied", hours, "hours")
print("predicted marks:", hours * rate + 12)

# --- a list ---
scores = [58, 71, 64, 80, 49]
print("first:", scores[0], " last:", scores[-1], " how many:", len(scores))

# --- a loop ---
total = 0
for s in scores:
    total = total + s
print("total:", total, " mean:", total / len(scores))

# --- a function ---
def mean(numbers):
    return sum(numbers) / len(numbers)

print("mean() says:", mean(scores))
```

```text
Asha studied 4 hours
predicted marks: 42.0
first: 58  last: 49  how many: 5
total: 322  mean: 64.4
mean() says: 64.4
```

Four rules that cover ninety per cent of Python confusion:

1. **`=` means "put this in that box".** It is not the `=` of algebra. `total = total + s` is a perfectly
   sensible instruction: work out the right-hand side, then put it in `total`.
2. **Counting starts at 0.** `scores[0]` is the first one. `scores[-1]` is the last one.
3. **The colon-and-indent is structure, not decoration.** Everything indented under `for s in scores:`
   happens once per item. Wrong indentation is wrong meaning, silently.
4. **`return` is the only way a value gets out of a function.** A function that prints but does not
   return hands back `None`, and `None + 1` is an error four lines later.

## 2.2 — Imports

```python
import numpy as np              # "get numpy, call it np"
import torch                    # "get torch"
import torch.nn as nn           # "get the nn part of torch, call it nn"
from sklearn.datasets import load_digits    # "get just this one thing"
```

`np.mean(...)` reads as *"the mean that lives inside numpy"*. The dot is "inside". That is all the dot
ever means.

## 2.3 — numpy arrays: a list that knows its shape and does maths all at once

```python
import numpy as np
scores = np.array([58, 71, 64, 80, 49])
print("the array      :", scores)
print("shape          :", scores.shape)
print("dtype          :", scores.dtype)
print("every score +5 :", scores + 5)
print("mean           :", scores.mean())

grid = np.array([[58, 71], [64, 80], [49, 55]])
print("grid:")
print(grid)
print("grid.shape         :", grid.shape)
print("mean down columns  :", grid.mean(axis=0))
print("mean across rows   :", grid.mean(axis=1))
```

```text
the array      : [58 71 64 80 49]
shape          : (5,)
dtype          : int64
every score +5 : [63 76 69 85 54]
mean           : 64.4
grid:
[[58 71]
 [64 80]
 [49 55]]
grid.shape         : (3, 2)
mean down columns  : [57.         68.66666667]
mean across rows   : [64.5 72.  52. ]
```

Three things to notice, all of which matter later:

- **`scores + 5` adds 5 to everything** with no loop. That is the reason numpy exists.
- **`dtype` is what kind of number is in the slots.** `int64` = whole numbers, `float64` = decimals.
  Week 20 onwards, dtype causes real errors — a layer that wants decimals will refuse whole numbers.
- **`axis=0` walks down columns, `axis=1` walks across rows.** Two answers, both plausible, and picking
  the wrong one gives you a confident wrong number with no error. Say the direction out loud every time.

## 2.4 — A DataFrame: a table with column names

```python
import pandas as pd
df = pd.DataFrame({
    "student": ["Asha", "Ravi", "Nita", "Sam"],
    "hours":   [4, 1, 6, 3],
    "marks":   [58, 22, 79, 41],
})
print(df)
print()
print("shape:", df.shape)
X = df[["hours"]]
y = df["marks"]
print("X shape:", X.shape, " y shape:", y.shape)
```

```text
  student  hours  marks
0    Asha      4     58
1    Ravi      1     22
2    Nita      6     79
3     Sam      3     41

shape: (4, 3)
X shape: (4, 1) y shape: (4,)
```

**`X` and `y` are the two names you will see 400 times this year.** `X` is everything the model is
allowed to look at — always a *table*, hence the double brackets and the shape `(4, 1)`. `y` is the one
thing you want it to predict — always a single column, hence shape `(4,)`. Capital `X`, lower-case `y`,
by universal convention, and every teacher file says why in Week 1.

## 2.5 — Tensors: numpy arrays that remember what happened to them

Here is the entire reason PyTorch exists, in nine lines.

```python
import torch
w = torch.tensor(3.0, requires_grad=True)
loss = w * w
loss.backward()
print("w      =", w)
print("loss   =", loss)
print("w.grad =", w.grad)
print("loss.item() =", loss.item())
print("w.grad.item() =", w.grad.item())
```

```text
w      = tensor(3., requires_grad=True)
loss   = tensor(9., grad_fn=<MulBackward0>)
w.grad = tensor(6.)
loss.item() = 9.0
w.grad.item() = 6.0
```

**Look at `w.grad`: it is 6.0.** That is the slope of `w²` at `w = 3` — the exact number you measured
by hand in §1.4 with two subtractions and a division. PyTorch got it without measuring anything,
because it *recorded* that `loss` was made by multiplying `w` by itself, and then walked that recording
backwards.

Four pieces of vocabulary, and they carry the rest of the year:

| Thing | What it is |
|---|---|
| **tensor** | numpy's array, plus the ability to remember its own history |
| **`requires_grad=True`** | "track this one — I am going to want its slope" |
| **`loss.backward()`** | "walk the recording backwards and fill in every slope" |
| **`.grad`** | the drawer the slope lands in |

And **`.item()`** pulls a plain Python number out of a one-value tensor. It looks cosmetic. It is not —
see error 5 in §4.

## 2.6 — What a training loop is

Five lines, in this order, forever, in every framework. Here they are fitting `y = 8x + 12` from six
points. Runs in about one second.

```python
import torch

torch.manual_seed(0)

X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
y = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])

model = torch.nn.Linear(1, 1)                       # one weight, one bias
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(401):
    optimizer.zero_grad()            # 1. wipe last round's slopes
    pred = model(X)                  # 2. forward: guess
    loss = loss_fn(pred, y)          # 3. how wrong?
    loss.backward()                  # 4. slope for every knob
    optimizer.step()                 # 5. nudge every knob downhill
    if epoch % 100 == 0:
        print(f"epoch {epoch:>4}  loss {loss.item():>10.4f}  "
              f"weight {model.weight.item():>7.4f}  bias {model.bias.item():>7.4f}")
```

```text
epoch    0  loss  1746.4574  weight  3.2239  bias  1.3262
epoch  100  loss     7.6645  weight  9.4688  bias  5.7119
epoch  200  loss     3.6891  weight  9.0190  bias  7.6375
epoch  300  loss     1.7756  weight  8.7070  bias  8.9734
epoch  400  loss     0.8546  weight  8.4905  bias  9.9002
```

**Read what happened.** The data was made with weight 8 and bias 12. The model started with random
junk (`3.22` and `1.33`), the loss started at 1746, and 400 downhill steps later the loss is `0.85` and
the weight is `8.49` heading for 8. It is finding the answer by walking downhill — §1.5, with two
knobs instead of one, done for you.

**The five lines, and what each one is:**

| # | Line | In English | If you drop it |
|:--:|---|---|---|
| 1 | `optimizer.zero_grad()` | Wipe last round's slopes | **No error. It silently learns wrong.** The worst bug in the level |
| 2 | `pred = model(X)` | Guess, with the current knobs | Nothing to be wrong about |
| 3 | `loss = loss_fn(pred, y)` | One number for how wrong | Nothing to measure |
| 4 | `loss.backward()` | Fill in every knob's slope | `.grad` stays `None`; step does nothing |
| 5 | `optimizer.step()` | Nudge every knob against its slope | Loss never moves at all |

Week 21 makes the student delete each line in turn and write down what happened. Do that yourself once,
before Week 21. It takes four minutes and it is the best four minutes of PyTorch preparation available.

## 2.7 — Two words for "how long have we been training"

| Word | Means |
|---|---|
| **epoch** | one full pass over all the training rows |
| **step** (or iteration) | one nudge of the knobs — one `optimizer.step()` |

If you have 1,200 rows and you use 32 at a time, one epoch contains `1200 ÷ 32 = 37.5 → 38` steps.
Week 23 makes students compute that three different ways until the arithmetic agrees.

## 2.8 — A neuron, in numpy, by hand

For completeness, because Week 16 is where the year turns. A **neuron** multiplies each input by a
weight, adds a bias, and squashes.

```python
import numpy as np
x = np.array([2.0, -1.0, 0.5])
w = np.array([0.4, -0.7, 1.2])
b = -0.5

z = (x * w).sum() + b
print("each product:", x * w)
print("their total :", (x * w).sum())
print("plus bias   : z =", z)
print("ReLU(z)     =", max(0.0, z))
print("sigmoid(z)  =", round(float(1 / (1 + np.exp(-z))), 6))
print("tanh(z)     =", round(float(np.tanh(z)), 6))
```

```text
each product: [0.8 0.7 0.6]
their total : 2.1
plus bias   : z = 1.6
ReLU(z)     = 1.6
sigmoid(z)  = 0.832018
tanh(z)     = 0.921669
```

Check it by hand: `2.0 × 0.4 = 0.8`, `−1.0 × −0.7 = 0.7`, `0.5 × 1.2 = 0.6`. Total `2.1`. Minus `0.5`
gives `1.6`. **ReLU** is the simplest squash there is: keep positives, turn negatives into zero. A
network with 3,000 of these in it is doing nothing you have not just done with a calculator.

## 2.9 — The five-word glossary you can hide behind all year

If you remember only five things from this section, remember these:

| Word | The one-line version |
|---|---|
| **loss** | one number for how wrong we are. Lower is better |
| **gradient** | one slope per knob. Its opposite direction is downhill |
| **shape** | rows × columns. Print it when confused. Print it when not confused |
| **epoch** | one pass over all the data |
| **artifact** | the saved file that *is* the model |

---
---

# 🔧 Section 3 — What "Engineering" Adds On Top of Level 2

Level 2 taught a student to get a model working. Level 3 is about the difference between *working* and
*trustworthy*, and there are five ideas in that gap. You should be able to say all five out loud.

### 3.1 — Measurement: "it's 94% accurate" is not a sentence

Ask three questions of any score, always, out loud, in front of the student:

1. **94% of what?** Which rows? How many of them? If the answer is "the ones it trained on", it is not
   a result, it is a memory test.
2. **Compared to what?** If 94% of the rows are one class, then *always guessing that class* scores 94%,
   and the model has added nothing. That comparison number is the **baseline** and Week 2 makes it
   mandatory.
3. **How many of each mistake?** 94% accurate can mean "caught every fraud, a few false alarms" or
   "caught none of them". Those are different products. Week 8 gives you the four numbers that tell
   them apart.

### 3.2 — Splits: three piles, and one you only open once

```
   ┌──────────────── 2,020 rows ────────────────┐
   │  TRAIN 60%      │  VAL 20%   │  TEST 20%   │
   │  learn from     │  choose    │  open ONCE  │
   │  these          │  with      │  at the end │
   │                 │  these     │             │
   └─────────────────┴────────────┴─────────────┘
```

Level 2 had two piles. Three exist because **choosing is a kind of fitting.** If you try eight models
and keep whichever scored best on the test set, you have just fitted your *choice* to the test set, and
that score is now optimistic. So: fit weights on train, make every decision on validation, and open
test once, at the very end, to report a number. Week 2.

### 3.3 — Leakage: the reason a great score is bad news

**Leakage** is information reaching the model that will not exist when it has to predict for real. It
is the most expensive mistake in applied machine learning and it always looks like success.

Three flavours, all in Week 6, each with real numbers:

| Flavour | What happened | The tell |
|---|---|---|
| **Target leakage** | A feature exists only *because* the outcome already happened — `customer_called_support` is only there if the delivery was late | AUC 0.978 in testing, useless in production |
| **Temporal leakage** | You trained on the future and tested on the past | Random split 0.79, honest time split 0.56 |
| **Preprocessing leakage** | A mean, a scaler, or a feature selection computed *before* the split, so the training saw the test rows | 75% accuracy on data that is literally random noise |

That last one is worth showing you now, because it is shocking and it takes eight seconds to run:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
X = rng.normal(size=(200, 2000))          # PURE NOISE
y = rng.integers(0, 2, size=200)          # a coin flip

# --- WRONG: pick the best 20 columns using every row, labels included
sel = SelectKBest(f_classif, k=20).fit(X, y)
X_small = sel.transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(X_small, y, test_size=0.3, random_state=0)
bad = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print("WRONG (selection before the split):", round(bad.score(X_te, y_te), 4))

# --- RIGHT: selection lives inside the pipeline, refitted on each training fold
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))
scores = cross_val_score(pipe, X, y, cv=5)
print("RIGHT (selection inside the pipeline):", round(scores.mean(), 4))
```

```text
WRONG (selection before the split): 0.75
RIGHT (selection inside the pipeline): 0.555
```

**There is no signal in that data. None. It is random numbers and coin flips.** The leaky version
reports 75% accuracy. If a student ever hands you a surprisingly good score, this is the first thing
to suspect, and being visibly suspicious in front of them is one of the most valuable things you do
all year.

### 3.4 — Baselines: the number you must beat

Before any model, build the dumbest possible predictor and write down its score. Always guess the
common class. Predict the average. Use one hand-written if-statement. **A model that cannot beat that
should be deleted**, and a student who has internalised this will never again be impressed by an
unanchored percentage. Week 2.

### 3.5 — Reproducibility: a number you cannot reproduce is not a result

This is the sentence of the level. Watch what happens without a seed:

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_wine(return_X_y=True)
print("--- no random_state anywhere: five runs of the SAME code ---")
for run in range(5):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3)
    tree = DecisionTreeClassifier(max_depth=3).fit(X_tr, y_tr)
    print("  run", run, "accuracy", round(tree.score(X_te, y_te), 4))
```

```text
--- no random_state anywhere: five runs of the SAME code ---
  run 0 accuracy 0.8704
  run 1 accuracy 0.9074
  run 2 accuracy 0.8333
  run 3 accuracy 0.9815
  run 4 accuracy 0.9074
```

> **⚠️ Watch out:** those five numbers are the only ones in this entire course that **will not match on
> your machine**, and that is the point of the block. The same code, five times, unchanged, gives
> anything from 83% to 98%. A student who runs it once and gets `0.9815` will tell you their model is
> 98% accurate. It is not. It got lucky with which rows landed where.

The same code with the seed set:

```text
--- random_state=0 everywhere: five runs of the SAME code ---
  run 0 accuracy 0.9444
  run 1 accuracy 0.9444
  run 2 accuracy 0.9444
  run 3 accuracy 0.9444
  run 4 accuracy 0.9444
```

**Every code block in this course sets a seed** — `random_state=0`, `np.random.seed(0)`,
`torch.manual_seed(0)` — so the numbers in the teacher file are the numbers on the screen. Insist on
this from Week 1. It is a professional habit and it is easy to build at fourteen.

### 3.6 — And the artifact: the thing you actually hand over

Level 2's deliverable was a chart and a number. Level 3's is a **file** — a fitted pipeline saved to
disk, loadable in a program that contains no training code, with a card beside it saying what it is,
what it was measured on, and where it breaks. Weeks 3, 23, 34 and 35 are about this, and it is the
reason the level is called Engineer.

---
---

# 🐞 Section 4 — How to Read a Traceback, and the 14 Errors This Level Produces

## 4.0 — The three-step rule, and the Level 3 wrinkle

In Level 2, tracebacks were four lines long. In Level 3 they go through PyTorch and can be thirteen
lines. **The rule does not change:**

1. **Read the LAST line.** It has the error type and the message. Everything else is context.
2. **Find the line that names YOUR file.** In a long traceback there is usually exactly one, and it is
   near the top. That is where you look.
3. **Ignore everything in between.** Those are frames inside a library and there is nothing you can do
   about any of them.

Here is a real one, from a real run:

```python
# shapes.py -- a two-layer network on the digits dataset
import torch
import torch.nn as nn
from sklearn.datasets import load_digits

digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32)   # (1797, 64)

model = nn.Sequential(
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(16, 10),        # <-- 16 should be 32
)

print(model(X).shape)
```

```text
Traceback (most recent call last):
  File "/private/tmp/l3o/shapes.py", line 15, in <module>          ← ★ YOUR FILE. Line 15.
    print(model(X).shape)
  File ".../torch/nn/modules/module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File ".../torch/nn/modules/module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File ".../torch/nn/modules/container.py", line 217, in forward
    input = module(input)
  File ".../torch/nn/modules/module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File ".../torch/nn/modules/module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File ".../torch/nn/modules/linear.py", line 116, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1797x32 and 16x10)   ← ★ READ THIS FIRST
```

**Thirteen lines, one of which is yours.** Read the last line: two shapes, `1797x32` and `16x10`. From
§1.7 you know the inner numbers must match: `32` wants to meet `16`. They do not. Now look at the code
and find the `16` — third layer, and it should be `32`.

> **🧑‍🏫 If a student asks** *"why is it printing so much about files I never wrote?"* — Because the
> error happened deep inside PyTorch, and it is politely showing you the whole route it took to get
> there. It is a receipt, not an accusation. Read the destination and your own stop, ignore the rest.

**Teach them to say the error out loud before touching anything.** "Runtime error, mat one and mat two
shapes cannot be multiplied, one-seven-nine-seven by thirty-two, and sixteen by ten." Saying it slows
the hand down and about a third of the time the fix arrives mid-sentence.

---

## The 14 errors, in the order you will meet them

### Error 1 — Shape mismatch in a matrix multiply *(the commonest error of the year)*

```text
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1797x32 and 16x10)
```

**English:** "You asked me to multiply a grid that is 1797 by 32 with a grid that is 16 by 10. The
inner two numbers, 32 and 16, are not the same, so there is nothing I can do."

**Fix:** the second number of the first pair must equal the first number of the second pair. One of
them is wrong; find which. In numpy the same error reads `size 3 is different from 4`.

**How to help without giving it away:** *"Read me the two shapes. Now which two numbers have to match?
Which one is wrong?"* That is often the entire intervention.

---

### Error 2 — Wrong dtype: `Long` and `Float`

```python
import torch
import torch.nn as nn
X = torch.tensor([[1, 2], [3, 4]])          # whole numbers -> int64 -> "Long"
model = nn.Linear(2, 1)
print(model(X))
```

```text
RuntimeError: mat1 and mat2 must have the same dtype, but got Long and Float
```

**English:** "You gave me whole numbers. This layer works in decimals. I will not quietly convert them
for you." `Long` is PyTorch's word for whole numbers; `Float` is decimals.

**Cause:** `torch.tensor([[1, 2], [3, 4]])` — no decimal points anywhere, so PyTorch made it `Long`.

**Fix:** `torch.tensor(a, dtype=torch.float32)` or `.float()` on the way in. Weeks 20 and 24 teach the
habit of always saying the dtype.

**And the confusing cousin**, which goes the other way:

```python
import torch, torch.nn as nn
logits = torch.tensor([[2.0, 1.0, 0.1]])
target = torch.tensor([0.0])            # should be a whole-number class index
print(nn.CrossEntropyLoss()(logits, target))
```

```text
RuntimeError: expected scalar type Long but found Float
```

This is `CrossEntropyLoss` complaining that your *labels* are decimals. Class labels must be whole
numbers — `y.long()`. Same words, opposite fix. Both are in the Week 26 debugging clinic.

---

### Error 3 — Forgetting `optimizer.zero_grad()` *(the worst one — there is no error)*

There is **no traceback**. The model trains and learns something wrong. Watch — run this twice, once
exactly as written and once with the `opt.zero_grad()` line put back in as the first line of the loop:

```python
import torch
torch.manual_seed(0)
X = torch.tensor([[1.0], [2.0], [3.0]])
y = torch.tensor([[3.0], [5.0], [7.0]])
model = torch.nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.01)
print("--- WITHOUT optimizer.zero_grad() ---")
for epoch in range(5):
    loss = ((model(X) - y) ** 2).mean()
    loss.backward()
    print(f"epoch {epoch}  loss {loss.item():8.4f}  weight.grad {model.weight.grad.item():10.4f}")
    opt.step()
```

```text
--- WITHOUT optimizer.zero_grad() ---
epoch 0  loss  22.7439  weight.grad   -20.5908
epoch 1  loss  17.9815  weight.grad   -38.9015
epoch 2  loss  10.5111  weight.grad   -52.9049
epoch 3  loss   3.5556  weight.grad   -61.0517
epoch 4  loss   0.1155  weight.grad   -62.4421
```

```text
--- WITH zero_grad ---
epoch 0  loss  22.7439  weight.grad   -20.5908
epoch 1  loss  17.9815  weight.grad   -18.3107
epoch 2  loss  14.2170  weight.grad   -16.2835
epoch 3  loss  11.2414  weight.grad   -14.4812
epoch 4  loss   8.8893  weight.grad   -12.8788
```

**English:** PyTorch *adds* new slopes to whatever is already in `.grad`. Without wiping, epoch 3's
slope is epochs 0+1+2+3 stacked on top of each other — look at the left column marching to `−62` while
the honest one shrinks towards zero. The steps get wildly too big and the run becomes garbage.

**The tell:** the gradient magnitude **growing** epoch after epoch instead of shrinking. On this toy
problem the runaway version happens to reach a low loss faster, which is exactly why it is dangerous —
on anything real it explodes.

**Fix:** `optimizer.zero_grad()` as the **first** line inside the loop, every time, forever.

---

### Error 4 — Calling `.backward()` twice

```python
import torch
w = torch.tensor(3.0, requires_grad=True)
loss = w * w
loss.backward()
loss.backward()
```

```text
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors
after they have already been freed). Saved intermediate values of the graph are freed when you call
.backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph
a second time...
```

**English:** "I threw away my notes after you asked me the first time." The recording is deleted once
`backward()` has used it, because keeping it would waste memory.

**Fix:** almost always it means the forward pass has accidentally been moved *outside* the loop. Compute
`loss` fresh inside the loop, every iteration. **Ignore the advice about `retain_graph=True`** — it
silences the symptom and hides the real bug, and nothing in this course needs it.

**The other version of the same confusion:**

```python
import torch
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x * 2
y.backward()
```

```text
RuntimeError: grad can be implicitly created only for scalar outputs
```

**English:** "You asked for the slope of something that is a whole list, not one number." Slopes come
from one number. Add `.mean()` or `.sum()` first.

---

### Error 5 — Printing a tensor instead of `.item()`

No error. Two symptoms: unreadable output, and a program that gets slower and eats memory.

```python
import torch
torch.manual_seed(0)
model = torch.nn.Linear(4, 1)
X = torch.randn(200, 4)
y = torch.randn(200, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.01)

wrong, right = [], []
for i in range(5):
    opt.zero_grad()
    loss = ((model(X) - y) ** 2).mean()
    loss.backward(); opt.step()
    wrong.append(loss)          # the tensor, with its whole history attached
    right.append(loss.item())   # a plain number
print("wrong list:", wrong[:2], "...")
print("right list:", right)
print("type in the wrong list:", type(wrong[0]).__name__)
print("type in the right list:", type(right[0]).__name__)
print("does the wrong one still carry a graph? grad_fn =", wrong[0].grad_fn is not None)
```

```text
wrong list: [tensor(1.6095, grad_fn=<MeanBackward0>), tensor(1.5869, grad_fn=<MeanBackward0>)] ...
right list: [1.6094536781311035, 1.5869207382202148, 1.5653423070907593, 1.5446773767471313, 1.5248866081237793]
type in the wrong list: Tensor
type in the right list: float
does the wrong one still carry a graph? grad_fn = True
```

**English:** `losses.append(loss)` stores the tensor **and its entire recorded history**. Do that for
2,000 epochs and you are holding 2,000 computation graphs in memory that you will never use.

**Fix:** `losses.append(loss.item())`. One method call, and it is why `.item()` is taught in Week 20
rather than being left to chance.

---

### Error 6 — NaN loss from too high a learning rate

```python
import torch
torch.manual_seed(0)
X = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
y = torch.tensor([[3.0], [5.0], [7.0], [9.0]])
model = torch.nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.9)   # far too big
for epoch in range(60):
    opt.zero_grad()
    loss = ((model(X) - y) ** 2).mean()
    loss.backward()
    opt.step()
    if epoch % 10 == 0:
        print(f"epoch {epoch:>3}  loss {loss.item()}")
```

```text
epoch   0  loss 35.09282684326172
epoch  10  loss 3.0664192729649317e+24
epoch  20  loss inf
epoch  30  loss inf
epoch  40  loss nan
epoch  50  loss nan
```

**English:** the steps are so long that every one overshoots the valley and lands further up the far
side. The numbers double, then square, then exceed what a computer can store (`inf`), then `inf` minus
`inf` gives `nan` — "not a number" — and from that moment every number in the model is `nan` forever.

**Fix:** divide the learning rate by 10. Then again. `1e-3` is a sane default for Adam; `0.01` for SGD.

**Tell the student the diagnosis rule and make them memorise it:** *loss going up = learning rate too
big. Loss not moving = learning rate too small, or a missing `zero_grad`.* Week 15 has them cause both
on purpose.

---

### Error 7 — All predictions are one class

No error. A great-looking accuracy and a completely useless model.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score

X, y = make_classification(n_samples=4000, n_features=8, n_informative=3,
                           weights=[0.995, 0.005], flip_y=0.02, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=0)
m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
pred = m.predict(X_te)
print("positives in test  :", int(y_te.sum()), "of", len(y_te))
print("positives predicted:", int(pred.sum()))
print("unique predictions :", np.unique(pred))
print("accuracy           :", round(accuracy_score(y_te, pred), 4))
print("recall             :", round(recall_score(y_te, pred), 4))
print(confusion_matrix(y_te, pred))
```

```text
positives in test  : 14 of 1000
positives predicted: 0
unique predictions : [0]
accuracy           : 0.986
recall             : 0.0
[[986   0]
 [ 14   0]]
```

**English:** 98.6% accurate, and it has never once said yes. Every single positive was missed —
**recall is 0.0**. This is the accuracy paradox and it is Week 8's entire reason for existing.

**How to catch it:** `np.unique(pred)` should show both classes. Or look at the confusion matrix and
notice a column of zeros. Never report accuracy on an imbalanced problem without the four counts
beside it.

**Fix:** it is usually not a bug — it is the honest consequence of rare positives. Lower the threshold
(Week 10), report recall and precision instead (Weeks 8–9), or weight the classes.

---

### Error 8 — Data leakage: scaling before the split

No error. A number that is too good.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[2.0], [4.0], [6.0], [8.0], [100.0]])
print("all five values:", X.ravel())
# WRONG: scaler learns from all five, including the row we are about to hide
s_bad = StandardScaler().fit(X)
print("WRONG  mean the scaler learned:", round(float(s_bad.mean_[0]), 4),
      " spread:", round(float(s_bad.scale_[0]), 4))
X_tr, X_te = X[:4], X[4:]
s_good = StandardScaler().fit(X_tr)
print("RIGHT  mean the scaler learned:", round(float(s_good.mean_[0]), 4),
      " spread:", round(float(s_good.scale_[0]), 4))
print("WRONG  scaled test row:", np.round(s_bad.transform(X_te), 4).ravel())
print("RIGHT  scaled test row:", np.round(s_good.transform(X_te), 4).ravel())
```

```text
all five values: [  2.   4.   6.   8. 100.]
WRONG  mean the scaler learned: 24.0  spread: 38.0526
RIGHT  mean the scaler learned: 5.0  spread: 2.2361
WRONG  scaled test row: [1.9972]
RIGHT  scaled test row: [42.4853]
```

**English:** the hidden row is `100`, wildly unlike the four training rows. Fit the scaler on all five
and it learns a mean of 24 and a spread of 38, so `100` scales to a harmless-looking `2.0`. Fit it
honestly on the four training rows and `100` scales to **42.5** — a monster, which is what it actually
is. The leaky version smuggled knowledge of the test row into the preprocessing.

**Fix:** put the scaler inside a `Pipeline` (Week 3). Then it is *structurally impossible* to fit it on
the wrong rows, which is a much better guarantee than remembering.

---

### Error 9 — `ModuleNotFoundError`

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'torchvision'
```

**English:** "You asked me to import something that is not installed."

**Two completely different causes, and you must tell them apart:**

1. **`torchvision`** — this is **correct and expected**. It is not installed, and **nothing in this
   course needs it.** A student hitting this got the line from a tutorial. Weeks 24–27 explain what to
   write instead. Do not install it to make the error go away.
2. **`torch`, `sklearn`, `pandas`, `numpy`, `matplotlib`** — this is a virtual environment problem, not
   a code problem. Run `python -c "import sys; print(sys.executable)"`. The path must contain `.venv`.
   If it does not, you are running a different Python from the one you installed into. See §5.

---

### Error 10 — Off-by-one in a train/test index

No error. One row lives in both halves.

```python
import numpy as np
X = np.arange(20).reshape(20, 1)
n_train = 14
# WRONG - one row lives in both halves
X_tr, X_te = X[:n_train], X[n_train - 1:]
print("WRONG   train rows:", X_tr.ravel())
print("WRONG   test rows :", X_te.ravel())
print("WRONG   rows in both:", sorted(set(X_tr.ravel()) & set(X_te.ravel())))
print("WRONG   total rows counted:", len(X_tr) + len(X_te), "out of", len(X))
X_tr, X_te = X[:n_train], X[n_train:]
print("RIGHT   rows in both:", sorted(set(X_tr.ravel()) & set(X_te.ravel())))
print("RIGHT   total rows counted:", len(X_tr) + len(X_te), "out of", len(X))
```

```text
WRONG   train rows: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13]
WRONG   test rows : [13 14 15 16 17 18 19]
WRONG   rows in both: [13]
WRONG   total rows counted: 21 out of 20
RIGHT   rows in both: []
RIGHT   total rows counted: 20 out of 20
```

**English:** `X[:14]` and `X[13:]` overlap at row 13, so the model was tested on a row it trained on.
With 20 rows that is 5% contamination; with a time-ordered split it can be much worse.

**Fix:** `X[:n]` and `X[n:]`. And the check that catches it every time, which every teacher file uses:
**the two pile sizes must add up to the total.** `14 + 7 = 21`, and there are only 20 rows. Caught.

---

### Error 11 — Forgetting `model.eval()`

No error. Predictions that change every time you ask for them.

```python
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Dropout(0.5), nn.Linear(32, 1))
x = torch.ones(1, 4)
print("--- still in training mode: same input, five predictions ---")
for i in range(5):
    print("  ", round(model(x).item(), 6))
model.eval()
print("--- after model.eval(): same input, five predictions ---")
for i in range(5):
    print("  ", round(model(x).item(), 6))
```

```text
--- still in training mode: same input, five predictions ---
   0.418212
   0.272352
   -0.158818
   0.166699
   0.439044
--- after model.eval(): same input, five predictions ---
   0.322522
   0.322522
   0.322522
   0.322522
   0.322522
```

**English:** dropout randomly switches units off *during training*, on purpose, to stop the model
memorising. It must be switched off when you are measuring or predicting. `model.eval()` does that;
`model.train()` puts it back.

**Fix:** `model.eval()` before every evaluation and every prediction. `model.train()` before you resume
training. Week 23's homework is exactly the experiment above.

---

### Error 12 — Silently comparing accuracy on different splits

No error. Three numbers, all true, all meaning different things.

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_wine(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          stratify=y, random_state=0)
t = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
print("accuracy on the TRAINING rows :", round(t.score(X_tr, y_tr), 4))
print("accuracy on the TEST rows     :", round(t.score(X_te, y_te), 4))
print("accuracy on ALL the rows      :", round(t.score(X, y), 4))
```

```text
accuracy on the TRAINING rows : 1.0
accuracy on the TEST rows     : 0.9444
accuracy on ALL the rows      : 0.9831
```

**English:** this is one model, measured three ways. `1.0` is a memory test. `0.9831` is mostly a memory
test with some honesty mixed in. **`0.9444` is the only reportable number**, and it is the smallest —
which is why students drift towards the others.

**Fix:** say the split out loud with every score, always: *"0.9444 on the 54 test rows."* Make it a
sentence pattern. The teacher files never print a bare score, all year.

---

### Error 13 — The matplotlib window that never appears

```text
script finished, nothing was saved
```

No error, no chart, no window. This is a configuration difference, not a bug, and it is not worth one
minute of lesson time.

**Fix, and the course-wide policy:** **every chart in this course calls `fig.savefig("name.png")`.**
Never rely on a window. Open the PNG file. If you want to see it interactively too, add `plt.show()`
after the save — but the save comes first, so a missing window can never block a lesson.

---

### Error 14 — A seed not set, so the numbers change

Covered in §3.5 with real output. It is here in the list of fourteen because it is the *most common
cause of a student and a teacher disagreeing about whether the code worked.*

**Fix:** at the top of every file, `np.random.seed(0)` and `torch.manual_seed(0)`; on every split and
model, `random_state=0`. **Then a number that differs from the teacher file means something real is
different**, which is exactly what you want debugging to feel like.

---

## 4.15 — The error summary table

Print this and put it next to the laptop.

| # | Message or symptom | Meaning in six words | Fix |
|:--:|---|---|---|
| 1 | `mat1 and mat2 shapes cannot be multiplied (a×b and c×d)` | inner numbers b and c differ | fix one layer's size |
| 2 | `must have the same dtype, but got Long and Float` | whole numbers given to a decimal layer | `.float()` |
| 2b | `expected scalar type Long but found Float` | labels must be whole numbers | `y.long()` |
| 3 | loss weird, gradients **growing** | slopes piling up | `optimizer.zero_grad()` first in loop |
| 4 | `Trying to backward through the graph a second time` | notes already thrown away | forward pass inside the loop |
| 4b | `grad can be implicitly created only for scalar outputs` | asked for the slope of a list | `.mean()` first |
| 5 | `[tensor(1.6095, grad_fn=...), ...]` | stored the history, not the number | `.item()` |
| 6 | loss → `inf` → `nan` | learning rate far too big | divide it by 10 |
| 7 | high accuracy, `unique(pred)` is `[0]` | never says yes; recall 0.0 | threshold / class weights / report recall |
| 8 | score suspiciously good | preprocessing saw the test rows | put it in a `Pipeline` |
| 9 | `ModuleNotFoundError: torchvision` | expected — never needed here | do not install it |
| 9b | `ModuleNotFoundError: torch` | wrong Python is running | activate the venv |
| 10 | pile sizes add to more than the total | overlapping split | `X[:n]` and `X[n:]` |
| 11 | same input, different prediction | dropout still on | `model.eval()` |
| 12 | three different accuracies | three different row sets | always name the split |
| 13 | no chart, no window, no error | display config | `fig.savefig(...)` |
| 14 | numbers differ every run | no seed | `random_state=0` everywhere |

**And the Bug Log.** The student keeps one all year: one page per error, with the real message, what it
meant in their own words, and the fix. By Week 36 it is 40 pages long and it is the single most useful
artifact of the year. Insist on it from Week 1.

---
---

# 🔧 Section 5 — The Offline Setup Guide

**Do it in Week 0. Not in Week 1.** Setup problems in Week 20 feel like failure. Setup problems in
Week 0 are just setup. Budget 45 minutes and expect to use 30.

> **The headline, so you can stop worrying:** the only time this course needs the internet is the one
> `pip install` below. **No dataset in any of the 36 weeks downloads anything.** `torchvision` is not
> needed and must not be installed.

### Step 1 — Python (10 min)

```bash
python3 --version
```

Want 3.11 or newer; 3.10 works fine (this course was written on 3.10.10). If it is missing or older,
get it from [python.org/downloads](https://python.org/downloads).

> **⚠️ Windows:** tick **"Add python.exe to PATH"** on the *first* installer screen. That one checkbox
> is about 90% of all Windows setup pain. Then open a **new** terminal.

### Step 2 — A folder and a virtual environment (10 min)

```bash
# 1) One folder for the entire year. Never delete this.
mkdir -p ~/ai-academy/level3
cd ~/ai-academy/level3

# 2) Create the private box (makes a hidden .venv folder)
python3 -m venv .venv

# 3) Step INTO the box
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows PowerShell
```

Your prompt must now start with `(.venv)`. **That prefix is the whole game, and it does not survive
closing the terminal.** Write the activate line on a sticky note and stick it to the laptop.

### Step 3 — The stack: one command, ~2.5 GB, 10 min (5 min)

```bash
pip install --upgrade pip
pip install "numpy>=1.26" "pandas>=2.0" "matplotlib>=3.7" "scikit-learn>=1.4" "torch>=2.1"
```

That is the whole year. `joblib` arrives automatically with scikit-learn. **Do not install
`torchvision`, `seaborn`, `jupyterlab`, `flask` or anything else.** Most of the download is PyTorch.

### Step 4 — Smoke test 1: the imports and the dataset (3 min)

`smoke.py`:

```python
import numpy, pandas, matplotlib, sklearn, torch
from sklearn.datasets import load_digits
print("Level 3 ready ·", "numpy", numpy.__version__, "· torch", torch.__version__,
      "· digits", load_digits().images.shape)
```

```text
Level 3 ready · numpy 1.26.4 · torch 2.2.1 · digits (1797, 8, 8)
```

✅ **PASS:** you get a line like that. Version numbers will differ — fine. **`(1797, 8, 8)` must
match**: that is the image dataset of this level, already on your disk, no download.
❌ **FAIL:** `ModuleNotFoundError` → it is the venv, 95% of the time. See the table below.

### Step 5 — Smoke test 2: autograd (2 min)

The one that proves PyTorch can actually do the thing this course is built on.

```python
import torch
w = torch.tensor(3.0, requires_grad=True)
(w * w).backward()
print("autograd ready · slope of w*w at w=3 is", w.grad.item(), "(should be 6.0)")
```

```text
autograd ready · slope of w*w at w=3 is 6.0 (should be 6.0)
```

✅ **PASS:** it prints `6.0`. That number is §1.4, done by machine. If this passes, Weeks 20–36 will
work.

### Step 6 — Smoke test 3: a chart can be saved (2 min)

Charts fail differently from everything else, so test them separately.

```python
import matplotlib
matplotlib.use("Agg")          # write to a file, never a window
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([1, 2, 3], [2, 4, 9], marker="o")
ax.set_title("smoke test"); ax.set_xlabel("x"); ax.set_ylabel("y")
fig.savefig("smoke_plot.png", dpi=100)
print("wrote smoke_plot.png")
```

```text
wrote smoke_plot.png
```

✅ **PASS:** a `smoke_plot.png` file exists and opens. **A window is not required and never will be.**

### Step 7 — Editor (5 min)

VS Code plus the Microsoft Python extension. Then: `Ctrl+Shift+P` → *"Python: Select Interpreter"* →
pick the one with `.venv` in its path. **Skipping that click is the number-one mystery bug of the year.**

### Step 8 — Timing check (3 min, optional but reassuring)

Run this once so you know your laptop is fast enough. It trains a small convolutional network on 1,347
handwritten digits and tests it on 450 it has never seen. This is Week 26's model, in miniature.

```python
import time
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.manual_seed(0)
d = load_digits()
X = torch.tensor(d.images / 16.0, dtype=torch.float32).unsqueeze(1)   # (1797, 1, 8, 8)
y = torch.tensor(d.target, dtype=torch.long)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          stratify=d.target, random_state=0)

model = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(8 * 4 * 4, 10),
)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

t0 = time.time()
for epoch in range(400):
    opt.zero_grad()
    loss = loss_fn(model(X_tr), y_tr)
    loss.backward()
    opt.step()
    if epoch % 100 == 0:
        print(f"epoch {epoch:>3} loss {loss.item():.4f}")
model.eval()
with torch.no_grad():
    acc = (model(X_te).argmax(dim=1) == y_te).float().mean().item()
print("test accuracy:", round(acc, 4), " seconds:", round(time.time() - t0, 2))
```

```text
epoch   0 loss 2.3208
epoch 100 loss 1.3350
epoch 200 loss 0.5000
epoch 300 loss 0.2706
test accuracy: 0.9533  seconds: 8.6
```

**8.6 seconds, 95.3% on unseen digits, no GPU, no download.** That is Week 26, in miniature. The four
loss numbers and the accuracy are seeded and will match on your machine; **only the `seconds:` figure
will differ**, because that depends on your laptop. On the machine this course was written on it varies
between about 7.5 and 9 seconds. If your machine takes 40 seconds instead, everything still works — add
five minutes to Weeks 26 and 27.

### 5.9 — Troubleshooting: the 12 things that actually go wrong

| # | Symptom | Cause | Fix |
|:--:|---|---|---|
| 1 | `python: command not found`, or Windows opens the Microsoft Store | Python not on PATH | Try `python3`, then `py -3`. Re-run the installer with **Add to PATH** ticked. Open a **new** terminal |
| 2 | `ModuleNotFoundError` for torch/sklearn although pip said OK | Installed into one Python, running another | `python -c "import sys; print(sys.executable)"` — path must contain `.venv`. Activate again; re-pick the VS Code interpreter |
| 3 | `error: externally-managed-environment` | You skipped the venv | Do Step 2. **Never** use `--break-system-packages` |
| 4 | Prompt lost its `(.venv)` after closing the terminal | Venvs do not persist | Re-run the activate line. This is normal and happens every session |
| 5 | `pip install torch` fails or times out | Big download, flaky network or a proxy | Retry on a better connection; `pip install --timeout 120 torch`. Do this in Week 0, never in Week 20 |
| 6 | `ModuleNotFoundError: No module named 'torchvision'` | A tutorial line got copied in | **Expected. Do not install it.** Nothing here needs it — see Weeks 24–27 |
| 7 | `ImportError: numpy.core.multiarray failed to import` | numpy and torch built against different numpy majors | `pip install --upgrade --force-reinstall numpy torch` inside the venv |
| 8 | `plt.show()` shows nothing | Backend has no display | Not a problem — every chart also calls `savefig`. Open the PNG |
| 9 | A student's file is called `random.py` / `json.py` / `torch.py` | Python found their file instead of the library | Rename it and delete the `__pycache__` folder beside it |
| 10 | `IndentationError` on a line that looks fine | Tabs mixed with spaces | VS Code bottom bar → **Spaces: 4** → *Convert Indentation to Spaces*. Leave it on spaces forever |
| 11 | Training takes minutes, laptop fan screaming | Batch size or epoch count much larger than the file says | Check both against the teacher file. Every run in this course is under ~30 seconds |
| 12 | `UserWarning: ... does not have valid feature names` | A `Pipeline` was fitted on a DataFrame and predicted on a numpy array | Harmless, but fix it: pass a DataFrame with the same column names. Week 3 covers it |

### 5.10 — The setup completion checklist

```
   ☐  python3 --version  →  3.10 or newer
   ☐  Prompt shows (.venv)
   ☐  smoke.py prints a version line AND (1797, 8, 8)
   ☐  autograd smoke prints 6.0
   ☐  smoke_plot.png exists and opens
   ☐  VS Code interpreter has .venv in its path
   ☐  The activate line is on a sticky note on the laptop
   ☐  torchvision is NOT installed, and you know that is correct
```

All eight ticked? **You are set up for the entire school year and you will not need the internet
again.**

---
---

# ❓ Section 6 — The 20 Questions Students Ask in This Level

Honest answers. Say the honest one.

**1. "Is this how ChatGPT works?"**
Same ingredients, unimaginably bigger, plus two architectural ideas you meet in Level 4. Genuinely the
same: weights, a bias, a loss function, gradient descent, `loss.backward()`, and the training loop you
will write in Week 21 — that loop is *the* loop, unchanged. Genuinely different: scale (billions of
weights against your 700), the transformer/attention architecture, and a training bill in the tens of
millions of dollars. Nobody has a secret extra kind of maths. **Level 4 builds a tiny GPT with exactly
what you learn this year plus attention.** Say all of that; do not undersell either half.

**2. "Why do I have to do it by hand if the computer can do it?"**
Because in Week 18 you will compute four gradient arrays by hand, and in Week 20 PyTorch will produce
the identical numbers to eight decimal places — and at that moment you will know that `loss.backward()`
is not magic, it is your arithmetic done faster. People who skip the hand version cannot debug. When
their loss goes to `nan` they have no model of what happened, and they start changing lines at random.

**3. "Is this real calculus?"**
Yes. The number you measure in Week 12 by nudging is exactly the number a calculus class computes with
rules, and Week 12 proves it agrees on three different functions. A calculus class gives you speed and
generality. You have the meaning, which is the harder half.

**4. "Why is it called a neural network? Is it like a brain?"**
Historically the inspiration, and honestly: barely. A neuron here multiplies, adds and squashes. A real
neuron is a living cell of staggering complexity that nobody fully understands. The name stuck from the
1940s. **Call it a network of weighted sums** and you will never be confused by a headline again.

**5. "Why does my accuracy change every time I run it?"**
Because something random is unseeded — which rows landed in which pile, or the starting weights. §3.5
has the five-run demonstration. Set the seed. A number you cannot reproduce is not a result.

**6. "My model is 98% accurate — is that good?"**
Unknown until you say two more things: 98% of *which rows*, and what the baseline scored. If 98% of
rows are one class, guessing that class always is also 98%, and your model has added nothing. See
error 7 in §4 — the model that scored 0.986 and never once said yes.

**7. "Why do we hide the test data? Isn't that wasteful?"**
It is the only honest measurement available. A score on rows the model has already seen tells you how
well it remembers, and you did not want a memory. Level 3 goes further with three piles, because
*choosing* a model on the test set is also a way of fitting to it.

**8. "Can't we just use a bigger network?"**
Sometimes, and it is the wrong reflex. Bigger nets overfit faster and hide bad features. Week 27
measures how much augmentation buys versus how much a bigger model buys, on real numbers, and the
answer surprises people. Also: your best score this year will come from a feature you invented in
Week 5, not from more layers.

**9. "What's the difference between a weight and a parameter?"**
Nothing important. "Parameter" means any learnable number — weights *and* biases. `nn.Linear(64, 32)`
has 2,048 weights and 32 biases, so 2,080 parameters. Week 26 counts them.

**10. "Why is there a bias? Why not just weights?"**
Without a bias, every prediction must pass through zero. `marks = 8 × hours` says zero hours gives zero
marks. The bias is the `+12` that lets the line sit where it actually belongs.

**11. "Why ReLU? It looks like it does nothing."**
It does almost nothing, and that is why it works: it is cheap, and its slope is exactly 1 for positive
inputs so gradients pass through undiminished. Sigmoid's slope tops out at 0.25, so five stacked
sigmoids shrink a gradient to `0.25⁵ ≈ 0.001` and the early layers stop learning. Week 16 shows both.

**12. "What happens if I use no activation function at all?"**
Your ten-layer network collapses into a single straight line. Week 16 proves it algebraically on two
layers, in three lines. **The squash is the only reason depth means anything.**

**13. "Why does the loss go up sometimes even when it's working?"**
With mini-batches, each step is measured on a different handful of rows, so the number wobbles. What
matters is the trend over an epoch. But if it goes up *and keeps going*, that is error 6: learning rate
too big.

**14. "Can I use my GPU?"**
Nothing in this course needs one — every run is under about 30 seconds on a CPU. `.to("cuda")` or
`.to("mps")` exists and Week 20 names it in one sentence. Chasing a working GPU install costs more
lesson time than it saves, every time.

**15. "Why can't I just download a model that already works?"**
You can, and professionals do — that is transfer learning, Week 27. But you will be the person who has
to say why it is wrong for your data, and that requires knowing what is inside it. Also: this course
runs offline, so Week 27 does transfer learning honestly with no download, by freezing a backbone you
trained yourself.

**16. "Why are all the pictures 8×8? That's tiny."**
Because 1,797 tiny images train in nine seconds, which means you can run the experiment four times in
one lesson and *see* what changed. A 50,000-image dataset teaches you to wait. Every idea in Weeks
24–27 — kernels, stride, padding, feature maps, pooling, transfer learning — is exactly the same at
8×8 as at 1024×1024.

**17. "Why is the maths so ugly?"** *(usually meaning sigma notation or `∂L/∂w`)*
Because it is compressed. `Σ` means "add up all of these" and this course writes the full sum beside it
every time. `∂L/∂w` means "if I nudge w, how much does L move" — which you have measured with a
calculator. **The notation is shorthand for arithmetic you can already do.** Nothing is hiding.

**18. "Did I break it?"** *(after a traceback)*
No. A traceback means Python understood you well enough to tell you precisely what was impossible. The
frightening ones are the runs with **no** error and a wrong answer — errors 3, 7, 8, 10, 11 and 12 in
§4. A traceback is the good outcome.

**19. "Is my model biased?"**
Probably, in some way, and the engineering answer is: measure it. Week 35's subgroup metrics table
computes precision and recall separately per group, because an overall number can hide a model that
works well for most people and badly for some. This is Level 1's ethics with arithmetic attached.

**20. "What do I do with this?"**
Ship it. Weeks 34 and 35 turn a model into a file, a command-line tool, a local service, a log with
latency, and a card that says where it breaks. That is the difference between a notebook and a thing —
and it is the whole point of the word Engineer.

---
---

# ⚠️ Section 7 — The 15 Things Adults Get Wrong Teaching This Material

**1. Teaching the symbol before the number.** Writing `∂L/∂w` on the board before anyone has measured a
slope with a calculator. This is the number-one failure of this level and it is unrecoverable in the
moment. **Numbers first, name second, symbol third, and often skip the third.**

**2. Apologising for the maths.** *"Sorry, this bit is horrible."* You have just told them it is
reasonable to give up. Say instead: *"This bit is subtraction and division. Watch."*

**3. Saying "just".** *"Just take the derivative."* *"Just reshape it."* Nothing in this level is
"just". The word tells a struggling student that their difficulty is unreasonable.

**4. Explaining for longer than twelve minutes.** Every explanation in every teacher file is capped at
twelve minutes for a reason. If they are bored, you are still talking. Get to the arithmetic.

**5. Taking the keyboard.** See §9. It is the most damaging habit available to you and it feels
helpful.

**6. Skipping the hand calculation "because the code does it".** The code is a *check* on the hand
calculation, not a replacement. A student who has only ever seen the code has no way to know when the
code is wrong, and in this level the code is wrong regularly and silently.

**7. Rushing Week 12.** Everything from Week 15 to Week 27 stands on it. If Week 12 needs two weeks,
take two weeks. Compress Week 5.

**8. Teaching Weeks 18 and 20 in the same week.** Week 18 is four gradient arrays by hand and it is
exhausting and glorious. Week 20 is PyTorch doing it in one line. Put seven days between them or the
hand work retroactively becomes pointless.

**9. Being pleased by a high score.** When a number comes out at 0.97, the correct facial expression is
suspicion, out loud. *"Hm. What's the baseline? Which rows? Did anything leak?"* Model this until they
do it without you. It is the single most transferable habit in the level.

**10. Fixing the bug yourself because it is faster.** It is faster and it teaches nothing. Read the last
line of the traceback *together*. Ask "what shape is it?" Wait.

**11. Letting a number be reported without its split.** *"I got 94%."* → *"94% on what?"* Every time.
All year. It takes two seconds and it builds the reflex that Level 4 assumes.

**12. Treating a `nan` loss as a mystery.** It is not a mystery, it is error 6, and the fix is dividing
the learning rate by ten. Have that ready. Mystery is corrosive.

**13. Skipping the model card and the Bug Log because they are "not the real work".** They are the real
work. The word in the level title is Engineer, not Modeller. A model nobody can load, and whose
failures nobody wrote down, is a hobby.

**14. Comparing this student to a university course.** Different thing entirely. A 14-year-old who has
hand-computed a gradient and checked it numerically understands something that a large fraction of
people shipping models professionally do not. Say so.

**15. Not doing the week's arithmetic yourself the night before.** Fifteen to twenty-five minutes,
with a pencil. This is the one item on this list that, if you get it right, covers for getting several
of the others wrong.

---
---

# 🕐 Section 8 — How to Run a Lesson

## The standard 70-minute shape

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  ⏱️  THE 70-MINUTE LESSON                                                 │
   ├──────┬──────────────────────┬────────────────────────────────────────────┤
   │  min │  part                │  what happens                              │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │  0–7 │  🪝 HOOK             │  A concrete thing. A question you don't     │
   │      │  (7 min)             │  answer yet. Last week's result on screen.  │
   │      │                      │  NO new vocabulary in this part.            │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │ 7–23 │  🔢 THE MATHS,       │  Pencils. Paper. THREE TO FIVE REAL         │
   │      │  BY HAND             │  NUMBERS, worked out by everyone including  │
   │      │  (16 min)            │  you. The new word gets said at MINUTE ~20, │
   │      │                      │  after the arithmetic is already done.      │
   │      │                      │  On the 21 weeks with no new maths, this    │
   │      │                      │  becomes 🧠 CONCEPT and runs 12 min.        │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │23–45 │  💻 LIVE-CODE         │  You type, they type, same file, same time. │
   │      │  TOGETHER            │  Nobody pastes. The code CHECKS the         │
   │      │  (22 min)            │  arithmetic from the last part — that is    │
   │      │                      │  the payoff and it must actually happen.    │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │45–47 │  🐞 THE PLANTED BUG   │  You break it on purpose. Real traceback.   │
   │      │  (2–5 min)           │  Read the LAST line. Fix it. Bug Log.       │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │47–65 │  🎲 THEIR TURN        │  They build/extend/break it alone.          │
   │      │  (18 min)            │  You sit on your hands. See §9.             │
   ├──────┼──────────────────────┼────────────────────────────────────────────┤
   │65–70 │  🔑 CLOSE            │  Three takeaways, said by THEM not you.     │
   │      │  (5 min)             │  Read the homework out loud. Set the timer.  │
   └──────┴──────────────────────┴────────────────────────────────────────────┘
```

### Squeezing into 60 minutes

Cut in this order: the ✍️ practice (→ homework), then five minutes off "their turn", then the extension
in the activity. **Never cut the 🔢 maths-by-hand and never cut the planted bug.** The hand arithmetic
is the lesson; the bug is where debugging confidence comes from.

### Stretching to 75+

Add the "if the student is flying" variation in the teacher file, or spend the extra time making them
*explain the maths back to you* while you write down what they say. That transcript is the best
assessment evidence you will get.

### The four rituals that make a Level 3 lesson work

1. **Pencils before keyboards.** Every week. Non-negotiable. Paper first, code second, and the code's
   job is to agree with the paper.
2. **Print the shape.** Any time anything is confusing, from Week 16 onwards: `print(x.shape)`. Make it
   a reflex, not a last resort.
3. **Name the split.** No score is ever spoken without the rows it came from. *"0.944 on the 54 test
   rows."*
4. **The Bug Log entry, before the fix is forgotten.** Real message, what it meant in their words, the
   fix. Ninety seconds, every week, forty pages by June.

### Six rules of thumb that work every week

- If they are quiet and typing, **say nothing.**
- If they are quiet and *not* typing, ask *"what does the last line say?"*
- If they are frustrated, go back to three numbers on paper.
- If they finish early, ask them to break it and predict what breaks.
- If *you* are lost, say *"I don't know — let's measure it"* and nudge something by 0.001.
- If the arithmetic and the code disagree, **stop everything.** That disagreement is the most valuable
  event of the week and it is always instructive, whichever one turns out to be wrong.

---
---

# 🙌 Section 9 — How to Help Without Taking the Keyboard

## 9.1 — Why this matters more here than in Level 2

In Level 2 taking the keyboard cost them a piece of typing practice. In Level 3 it costs them the
belief that the maths is *theirs*. A student who watches an adult fix a shape error learns that shape
errors are fixed by adults.

**The rule: your hands do not touch their keyboard. Ever. All year.** If you must show something, use
your own machine, or paper.

## 9.2 — The escalation ladder

Work down it. Wait ten full seconds between rungs. Ten seconds is much longer than it feels and it is
where most of the learning happens.

```
   1.  "Hm."                                        ← often enough. Just be present.
   2.  "Read me the last line of the error."
   3.  "What did you expect it to do?"
   4.  "What shape is it?"        ← the Level 3 super-question, weeks 16–36
   5.  "Print it. What actually came out?"
   6.  "Which line was the last one that definitely worked?"
   7.  "Do those two numbers have to match?"        ← for every shape error
   8.  "What did we get on paper for this one?"     ← for every maths mismatch
   9.  "Nudge it by 0.001 and divide. What do you get?"   ← for every slope question
  10.  "Look at the teacher file's version of this line — what's different?"
  11.  Point at the line. Do not say what is wrong with it.
  12.  Say what is wrong with it. Let them type the fix.
```

You will rarely get past rung 5. Rungs 11 and 12 are the last resort and they are still not *you
typing*.

## 9.3 — The eight sentences

Keep these on a card. They cover almost everything.

1. *"Read me the last line."*
2. *"What shape is it?"*
3. *"What did you expect?"*
4. *"Show me on paper first."*
5. *"Which two numbers have to match?"*
6. *"What's the baseline?"*
7. *"On which rows?"*
8. *"I don't know. Let's measure it."*

Number 8 is the most important one in the list, and saying it honestly — with genuine curiosity, then
actually measuring — is the single best teaching moment available to you in this level. **Modelling
"I don't know, so I will measure" is more of the syllabus than any individual fact.**

## 9.4 — When to actually intervene

Take over the *thinking* (never the keyboard) when:

- **Twelve minutes of genuine stuck**, with real attempts, and morale is going. Twelve minutes, not
  three. Use a timer if you drift.
- **The blocker is a fact they cannot deduce** — that `nn.Conv2d` wants a batch dimension, say. Facts
  are gifts; give them freely. Reasoning is not.
- **It is an install problem.** Never make a student debug a venv. Fix it on your own time, apologise
  for the interruption, move on.
- **Tears, or the beginning of them.** Stop. Close the laptop. Do three numbers on paper. The lesson
  can lose fifteen minutes; it cannot lose the student.

## 9.5 — "I don't get the maths" — the most important page in this file

This sentence will be said to you, out loud, probably four or five times this year, most likely in
Weeks 12, 14, 17, 18 and 32. **What you do in the next sixty seconds decides whether this level works.**

### What NOT to do

- ❌ **Do not re-explain it.** They did not fail to hear you. Saying the same thing more slowly, or
  louder, or with a different analogy, is the reflex and it does not work. It also communicates
  *"the problem is your listening."*
- ❌ **Do not say "it's easy really"** or "you'll get it later". Both are dismissals.
- ❌ **Do not skip ahead** *"we can come back to it"*. In this level, you cannot. Week 12 is load-bearing.
- ❌ **Do not reach for a fifth analogy.** Analogies are for the first exposure. They do not repair a
  broken one.

### What TO do — the three-number rescue

**Stop talking. Pick up a pencil. Do the smallest version with real numbers, together, out loud.**

The script, which works for every mathematical idea in this level:

> **You:** *"OK. Forget all of it. Give me a number between 1 and 5."*
> **Them:** *"Three."*
> **You:** *"Right. Three times three is nine — write that down. Now three-point-oh-oh-one times
> itself. Use the calculator."*
> **Them:** *"Nine point zero zero six zero zero one."*
> **You:** *"And two-point-nine-nine-nine times itself?"*
> **Them:** *"Eight point nine nine four zero zero one."*
> **You:** *"Take the small one away from the big one."*
> **Them:** *"Zero point zero one two."*
> **You:** *"And how far apart were the two numbers you put in?"*
> **Them:** *"Zero point zero zero two."*
> **You:** *"Divide."*
> **Them:** *"Six."*
> **You:** *"That's it. That's the thing you said you didn't get. You just did it."*

Then — and only then — put the word back on it: *"the slope of x-squared at three is six, and the word
for that is derivative."*

### Why this works

Because "I don't get the maths" is almost never about the maths. It is one of four things, and all four
are fixed by doing arithmetic on three specific numbers:

| What they actually mean | What the three-number rescue does |
|---|---|
| "I don't know what the symbols refer to" | Replaces every symbol with a number they chose |
| "I can't hold five abstract things at once" | Reduces it to one thing at a time, written down |
| "I don't believe I'm the kind of person who does this" | Gives them a completed correct calculation in their own handwriting |
| "I lost the thread four minutes ago and was embarrassed to say" | Restarts from a place that cannot be lost |

### The follow-up, next lesson

Ask them to do the same three numbers again, cold, at the start of the next session. If they can, it
landed. If they cannot, do it again — cheerfully, with different numbers, no comment on the repeat. Two
or three cycles of that fixes it permanently. Re-explaining, no matter how many times, does not.

> ### 🔑 The one-line version
> **When they say "I don't get the maths", the answer is never more words. It is three numbers and a
> pencil.**

---
---

# ✏️ Section 10 — How to Mark Code, and How to Mark an Explanation

## 10.1 — Marking code: the four questions, in this order

1. **Does it run?** If not, is the error *understood*? A student who pastes the traceback and writes
   "shape mismatch, my second layer says 16 and should say 32, out of time" has demonstrated more than
   one who has working code they cannot explain. Give real credit for that.
2. **Is the number right?** Compare against the teacher file. **If the seed is set and the number
   differs, something real is different** — that is a finding, not a rounding issue.
3. **Was the arithmetic checked by hand anywhere?** In this level, a result with no hand check attached
   is half a result. Look for the paper.
4. **Is the split named?** Any reported score must say which rows it came from. This is worth marks and
   should be worth marks from Week 2.

## 10.2 — Be strict about exactly five things

Everything else, be generous. These five, be immovable:

| Be strict about | Why |
|---|---|
| **A seed in every file that prints a number** | A number you cannot reproduce is not a result |
| **The split named beside every score** | Otherwise the score means nothing and they know it |
| **A baseline before a model score** | Otherwise "0.94" is unanchored |
| **Preprocessing inside the `Pipeline`** | It is the structural defence against leakage; remembering is not |
| **One Bug Log entry per real error** | It is the artifact that compounds all year |

Be relaxed about: variable names, comment density, whether they used a loop or a comprehension, chart
prettiness, and file organisation. None of those is what this year is for.

## 10.3 — The four-tick scheme for a week's work

| Ticks | Means | Looks like |
|:--:|---|---|
| ✓✓✓✓ | Mastered | Runs, numbers match, hand check present and correct, split named, and they can explain *why* it works when asked a question not on the sheet |
| ✓✓✓ | Solid | Runs, numbers match, hand check present. Explanation is mostly recall |
| ✓✓ | Getting there | Runs with help, or numbers match but no hand check, or a hand check with an arithmetic slip they can find when prompted |
| ✓ | Attempted | Real attempt visible, errors pasted, stuck point identified in writing |

**A ✓ with a well-written stuck point is a genuinely good outcome and should be said out loud.** The
failure state is a blank page, not a wrong answer.

## 10.4 — How to mark a *written explanation of a result*

New in this level, and the harder half. From Week 5 onwards students write things like *"the
`is_weekend` feature changed AUC by 0.0000 so I deleted it"* or *"the model gets this review wrong
because bag-of-words threw away the word order"*.

Mark those against five questions:

| Question | A good answer | A weak answer |
|---|---|---|
| **Is there a number in it?** | "ΔAUC was −0.0012, so I deleted it" | "it didn't really help" |
| **Does it say which rows?** | "0.9444 on the 54 test rows" | "94%" |
| **Is the mechanism named, not just the effect?** | "the scaler learned a mean of 24 because it saw the hidden row" | "there was leakage" |
| **Is it in the language of the application?** | "a real customer's card gets declined at a petrol pump" | "a false positive" |
| **Does it say what would change their mind?** | "if the gap held up on a second seed I'd believe it" | — |

Three of five is good work for a 14-year-old. Five of five is what the capstone rubric asks for, and
by Week 35 it is reachable.

> **⚠️ Watch out:** the commonest weak explanation in this level is **fluent and wrong** — a confident
> paragraph using "overfitting", "gradient" and "leakage" correctly-ish, with no number in it anywhere.
> Do not reward it. Ask: *"which number in your own results tells me that?"* If there isn't one, the
> explanation is a guess wearing vocabulary.

## 10.5 — Marking the term checkpoints and the capstone

- **Weeks 9, 18 and 27** each have a paper in `assessments/`. Mark the paper, then mark the *reflection
  sheet* separately and more generously: it is for them, not for you.
- **Week 18** deserves a special note. Four gradient arrays by hand, gradient-checked. If they get it,
  say clearly and without hedging that this is the hardest thing in the level and they have done it. If
  they get it with three arithmetic slips they found themselves, that is the same achievement.
- **Weeks 34–36** use the [capstone rubric](../projects/capstone.md#-grading-rubric). The heaviest
  weight is on **"can somebody else run this from a cold start"** — not on accuracy. A 78%-accurate
  model that loads, logs, and documents its own limits beats a 94% model in a notebook, and the rubric
  is built to say so.

---
---

# ✅ Section 11 — The Pre-Flight Checklist

Run this before every single class. It takes eight minutes and prevents about 80% of lesson disasters.

```
   ┌───────────────────────────────────────────────────────────────────────────┐
   │  ✈️  PRE-FLIGHT — 8 MINUTES, BEFORE EVERY CLASS                            │
   ├───────────────────────────────────────────────────────────────────────────┤
   │                                                                           │
   │  THE NIGHT BEFORE (20–25 min)                                             │
   │  ☐  Read the whole teacher file for this week, start to finish             │
   │  ☐  🔢 DO THE ARITHMETIC IN THE "MATHS YOU NEED" SECTION, ON PAPER,        │
   │     WITH A PENCIL. Not read. Done. ← the one that matters most             │
   │  ☐  Run every code block in the Prep Checklist and check the output        │
   │     matches the file. If it doesn't, find out why NOW                     │
   │  ☐  Cause the planted bug yourself once, so you have seen the traceback     │
   │  ☐  Note the ONE sentence you want them to leave with                     │
   │                                                                           │
   │  ON THE DAY (8 min)                                                       │
   │  ☐  Terminal open, prompt shows (.venv)                                   │
   │  ☐  Last week's file still runs (30 seconds — catches a broken install)     │
   │  ☐  Printed workbook pages on the table                                   │
   │  ☐  PENCILS, ERASER, GRAPH PAPER out and visible before they sit down       │
   │  ☐  Calculator to hand (weeks 12–14, 32)                                  │
   │  ☐  The Bug Log notebook on the table, open                                │
   │  ☐  Phone face-down and out of sight. Yours as well as theirs              │
   │                                                                           │
   │  IN THE FIRST 60 SECONDS                                                  │
   │  ☐  Ask them to tell YOU what last week's number was, and on which rows    │
   │                                                                           │
   ├───────────────────────────────────────────────────────────────────────────┤
   │  IF THE LAPTOP IS DEAD:  every teacher file has a paper-only fallback in   │
   │  its Prep section, and in this level the fallbacks are genuinely good —    │
   │  the maths was always the lesson and the maths runs on graph paper.         │
   └───────────────────────────────────────────────────────────────────────────┘
```

### The end-of-class 60-second review — for you, not them

Four questions, in your own notebook, every week:

1. **Did they do arithmetic with their own pencil today?** (If no, the lesson did not happen.)
2. **Did the code check the arithmetic, and did they see it agree?**
3. **What did they say back to me in their own words that I did not say first?**
4. **What is the one thing I should re-ask at the start of next week?**

Question 3 is your real assessment. Everything else is bookkeeping.

### The one-page cheat sheet to keep next to the laptop

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  LEVEL 3 · THE CARD                                                   │
   ├───────────────────────────────────────────────────────────────────────┤
   │  SLOPE AT A POINT   (f(x+0.001) − f(x−0.001)) / 0.002                 │
   │  THE UPDATE         new = old − (step size) × (slope)                 │
   │  SHAPES             (3,2) @ (2,4) → (3,4).  inner two MUST match      │
   │  THE FIVE LINES     zero_grad → forward → loss → backward → step      │
   │  LOSS = 0.6931      the model is saying 50/50 to everything           │
   │  LOSS → nan         learning rate too big. divide by 10               │
   │  GRADIENTS GROWING  you forgot optimizer.zero_grad()                  │
   │  SCORE TOO GOOD     something leaked. check the Pipeline               │
   │  SAME INPUT, DIFFERENT ANSWER   you forgot model.eval()               │
   │  NUMBERS CHANGE EACH RUN        you forgot the seed                   │
   ├───────────────────────────────────────────────────────────────────────┤
   │  THE EIGHT SENTENCES                                                  │
   │  "Read me the last line."        "What shape is it?"                  │
   │  "What did you expect?"          "Show me on paper first."            │
   │  "Which two numbers must match?" "What's the baseline?"                │
   │  "On which rows?"                "I don't know. Let's measure it."     │
   ├───────────────────────────────────────────────────────────────────────┤
   │  "I DON'T GET THE MATHS"  →  never more words. three numbers and a     │
   │                              pencil. §9.5.                            │
   └───────────────────────────────────────────────────────────────────────┘
```

---
---

# 🧾 Last Thing

You are about to teach a fourteen-year-old to compute a derivative by measurement, assign blame
backwards through a network, and ship the result as a file somebody else can run. Some of the adults
who will hear about this year cannot do the second of those three.

You will not know every answer. That is not the job. The job is:

- **Do the week's arithmetic on paper, the night before.** Fifteen minutes. This is the whole deal.
- **Keep your hands off their keyboard.**
- **Say "I don't know — let's measure it"** and then actually measure it, in front of them, by nudging
  something by a thousandth and dividing.
- **When they say "I don't get the maths", reach for a pencil and three numbers, not for more words.**

That last one is the entire orientation compressed into a sentence, and if you only remember one thing
from these two hours, remember that.

Now go and do the Week 0 setup, alone, with nobody watching. Then open Week 1.

---

[⬅ Course home](../README.md) · [**Week 1 teacher guide ➡**](week-01.md) · [Week 1 student guide](../student-guide/week-01.md) · [Week 1 workbook](../workbook/week-01.md) · [Figure style guide](../figures/STYLE.md) · [Assessments](../assessments/README.md) · [The Ship It capstone](../projects/capstone.md) · [Level 3 glossary](../../glossary.md)
