# Week 12 — How Steep Is the Hill Right Here?

[⬅ Week 11](week-11.md) · [Course Home](../README.md) · [Week 13 ➡](week-13.md) · [Student Guide](../student-guide/week-12.md) · [Workbook](../workbook/week-12.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — **the most important lesson in Level 3.** Everything from Week 15 to Week 27 stands on it. |
| **Big idea** | Many models — logistic regression, and every neural network — find their best numbers by trying a value, asking *"which way is downhill"*, and stepping, and `fit()` never showed how. **You can measure "downhill" with two subtractions.** |
| **New vocabulary** | loss · loss surface · slope at a point · derivative · numerical gradient · learning rate · gradient descent |
| **New maths** | **The slope of a curve at ONE point**, measured by nudging the input by a tiny step: `(f(w + h) − f(w − h)) ÷ 2h`. Computed by hand at `x = 1`, `3` and `5`, shown to equal `2 × x`, **and only then** named the derivative. |
| **New syntax** | `np.linspace(a, b, n)` · `np.argmin(arr)` · `ax.annotate("...", xy=(x, y))` |
| **Dataset** | **10 hand-typed points**: hours of revision against exam marks. `(1, 20) (2, 28) (3, 36) (4, 44) (5, 52) (6, 60) (7, 68) (8, 76) (9, 84) (10, 92)`. Then the same table generated with numpy, seed 0, plus a wobbly version. **Nothing loads, nothing downloads, and the answer is hidden in the data on purpose.** |
| **Materials** | **Three sheets of squared graph paper per student**, plus one big sheet for the wall · **a real staircase, ramp or sloping corridor** you can walk on · a calculator each (phones fine) · printed workbook pages 12.1–12.6 · **last week's `BY HAND \| np.trapz` board still up** · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, matplotlib. **No scikit-learn needed at all this week.** No new installs. |
| **Prep time** | 30 minutes the night before — **and this is the week to spend all thirty.** 5 minutes on the day. |
| **Expected runtime of the code** | `valley.py`, `slope.py` and `walk.py` are **all under half a second each.** Nothing this week takes any time at all; the whole point is that the arithmetic is small enough to check on paper. |

> **⚠️ Watch out:** the order of this lesson is not negotiable and it is the whole design. **You measure three slopes numerically first. You write 2, 6 and 10 on the board. Only when somebody in the room notices that those are 2×1, 2×3 and 2×5 do you say the word *derivative*.** A teacher who writes `d/dx(x²) = 2x` on the board in the first ten minutes has destroyed the lesson and cannot get it back. Nothing in the file uses the word before minute 22. Keep it that way.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Turn a guess into a number** by computing the loss for eight candidate values of one weight, and sketch the resulting valley on graph paper.
2. **Measure the slope of a curve at a single point** by nudging the input by 0.001 and dividing, and **get 6.000 at x = 3 for x × x.**
3. **Show that the measured slopes 2, 6 and 10 at x = 1, 3 and 5 are exactly 2 × x**, and only then use the word *derivative*.
4. **Use the sign of the slope to decide which way to step**, and walk eight steps downhill by hand to find the best weight.

Observable evidence: eight (w, loss) pairs plotted as a valley on graph paper; the numbers 9.006001, 8.994001, 0.012000 and 6.000 written in a column; three slopes on the board with `2 × x` written underneath in somebody else's handwriting; and an eight-row table of `w ← w − 0.3 × slope` ending at 7.996068.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The three complete runnable files are in the Prep Checklist**, printed once each, in full.

> **📌 And a note about you.** If you have never done calculus, **this section is written for you and it will work.** There is no calculus in this lesson. There are no limits, no proofs, no rules to memorise. There is one subtraction, one division, and a number you can check on a phone. By the end of this section you will have measured a derivative with your own hand, and you will be able to teach it, and you will understand it better than most people who learned it from a textbook — because they learned the symbol and you will have measured the thing.

### 1. What has been hidden from the student for nine weeks

They have typed this, or something like it, about forty times:

```python
model.fit(X_train, y_train)
```

For logistic regression and for every neural network, something inside that line does the following (a plain `LinearRegression` reaches its best line by algebra instead, and trees and nearest-neighbours work in other ways again, but this loop is the engine of everything from here on):

1. Picked a value for a weight. Any value. Zero, usually.
2. Worked out **how wrong** that value made the model.
3. Worked out **which direction would make it less wrong.**
4. Took a small step in that direction.
5. Went back to step 2, a few hundred times.

**Steps 2 and 4 are easy to describe.** Step 3 is the one nobody has explained, and it is the whole of today.

### 2. Step 2 first: turning "how wrong" into a number

> **Loss** — one number saying how wrong a model currently is. Big is bad. Zero is perfect.

Here is the smallest honest example that exists, and it is the one the whole lesson uses.

**Ten students.** We know how many hours each of them revised, and what they scored:

| hours | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| marks | 20 | 28 | 36 | 44 | 52 | 60 | 68 | 76 | 84 | 92 |

**Those marks sit exactly on a line, on purpose.** Every extra hour is worth exactly 8 marks, and a student who revised nothing at all would get 12. Check it: `8 × 1 + 12 = 20` ✅, `8 × 10 + 12 = 92` ✅.

Now suppose we already know the 12 — a student who does nothing scores 12, that is just how the exam is marked. **The one thing we do not know is how much an hour of revision is worth.** Call it `w`. Our model is:

```
predicted marks  =  w × hours  +  12
```

**One unknown number.** `w` is the only knob. And the answer, which we have hidden in the data on purpose, is **8**.

> **💡 Try this:** the reason to hide a known answer inside the data is that **you can then tell whether the method found it.** Real data never does this. Every method in this course gets tested on a problem whose answer we already know, first.

**How wrong is a guess?** Take `w = 6` — a guess that an hour of revision is worth 6 marks. Work out what the model predicts, subtract the truth, square it, and average. Here is the whole thing, and it is ten subtractions you can do in your head:

```
w = 6:

  hours       1    2    3    4    5    6    7    8    9   10
  predicted  18   24   30   36   42   48   54   60   66   72        (6 × hours + 12)
  actual     20   28   36   44   52   60   68   76   84   92
  error      −2   −4   −6   −8  −10  −12  −14  −16  −18  −20        (predicted − actual)
  squared     4   16   36   64  100  144  196  256  324  400

  the squares add up to 1540
  1540 ÷ 10  =  154.0
```

**The loss at w = 6 is 154.** One number. That is step 2, done, forever.

**Why square the errors?** Two reasons, both worth saying out loud. First, some errors are negative and some positive, and if you just added them up they would cancel and a terrible model would look perfect. Second, squaring **punishes big misses much harder than small ones** — being out by 20 is not twice as bad as being out by 10, it is four times as bad. That is a choice somebody made, and it is a reasonable one.

### 3. Eight guesses, and the shape they make

Now do the same arithmetic for eight different guesses. This is the real output of `valley.py`:

```text
candidates [ 0.  2.  4.  6.  8. 10. 12. 14.]
   w      loss
  0.0    2464.00
  2.0    1386.00
  4.0     616.00
  6.0     154.00
  8.0       0.00
 10.0     154.00
 12.0     616.00
 14.0    1386.00
np.argmin(losses) = 4
so the best of the eight is w = 8.0
```

**Plot those eight points and you get a valley.** Down, down, down, down to the bottom at zero, then back up, symmetrically.

> **Loss surface** — the shape you get by plotting the loss against the value of a weight. With one weight it is a curve. With two it is a landscape. With a hundred thousand it is a thing nobody can draw, and this course never pretends otherwise.

![Eight guesses, and the valley they draw](../figures/fig-w12-1-loss-valley-eight-guesses.svg)
*Figure 12.1 — Eight guesses, and the valley they draw. Every loss on the curve is an average of ten squared errors, and one of them is worked out in full so you can check it.*

**Two things to have ready.**

**One — the valley is symmetric and that is not a coincidence.** Guessing 6 (two too low) and guessing 10 (two too high) give **exactly the same loss, 154.** Being wrong in either direction by the same amount is equally bad, because the errors get squared. Point this out; it is the thing that makes the curve a *valley* rather than a slide.

**Two — eight guesses is a terrible method and you should say so.** It worked here only because 8 happened to be one of our eight candidates. If the answer had been 8.3, our grid would have missed it. And with **two** weights you would need 8 × 8 = 64 guesses, with three you need 512, and a real network has a hundred thousand knobs. **Guessing does not scale, and that is the whole motivation for the rest of the lesson.**

> **🧑‍🏫 If a student asks** *"why not just use more guesses?"* — Because of the counting above. Write `8` then `8 × 8 = 64` then `8 × 8 × 8 = 512` on the board and say *"a small network has a hundred thousand knobs. Eight to the power of a hundred thousand."* Nobody argues after that.

### 4. 🔢 The new maths: how steep is it, right here?

**This is the week's one new idea and it is the most important thing in the course. Take it slowly.**

In Week 10 the class measured steepness **between two points** on the ROC curve: rise over run, both of them read off the paper. Today we want the steepness **at one point.** And here is the trick, which is so simple it feels like cheating:

> **🔢 The maths, slowly:** you cannot measure a slope at a single point, because a slope needs two points. **So take two points that are almost the same one.** Nudge the input a tiny bit to the left, nudge it a tiny bit to the right, see how much the output changed, and divide by how far you nudged.

Let us do it on the simplest curve there is: `f(x) = x × x`. **What is the slope at x = 3?**

Take a nudge of `h = 0.001`, and work out the value just above and just below:

```
f(3.001)  =  3.001 × 3.001  =  9.006001
f(2.999)  =  2.999 × 2.999  =  8.994001
```

**Do those two multiplications yourself, on paper, right now.** They are the whole lesson.

Now: the output went **up** by

```
9.006001 − 8.994001  =  0.012000        <- the rise
```

and to make that happen we moved **across** by

```
3.001 − 2.999  =  0.002                 <- the run
```

so the steepness is

```
0.012000 ÷ 0.002  =  6.000
```

**Six. That is the answer, and there was no calculus in it.** Two multiplications, one subtraction, one division. A calculator does it in eight seconds.

![The slope at one point is a rise over a run](../figures/fig-w12-2-tangent-line-with-numeric-slope.svg)
*Figure 12.2 — The slope at one point is a rise over a run. The same division, drawn with a nudge big enough to see — and it gives 6.000 as well, because for this curve the nudge size does not matter.*

> **Slope at a point** — how steeply a curve is climbing or falling right where you are standing. Measured by nudging the input a tiny bit each way and dividing the change in output by the change in input.

> **Numerical gradient** — the slope obtained by that nudge-and-divide method. It is slow, it needs no cleverness at all, **and it is honest, as long as the nudge is not absurdly small.** You will use it in Week 19 to check something far harder.

**Why nudge BOTH ways?** You could do `(f(3.001) − f(3)) ÷ 0.001` and get 6.001 — close, but not exact. Nudging symmetrically, one step each way, cancels out the error and lands on 6.000 dead on. **It is the same amount of work and it is more accurate, so we always do it that way.** (For the parabolas in this lesson the symmetric version is not just more accurate, it is exactly right, whatever nudge you use. Figure 12.2 uses a nudge of half a unit and still gets 6.000.)

**Now the bit that turns a trick into an idea.** Do the same measurement at two more points. This is the real output of `slope.py`:

```text
f(x) = x * x,   h = 0.001
   x      f(x+h)       f(x-h)      difference   / (2h)   2 * x
 1.0     1.002001     0.998001     0.004000   2.0000     2.0
 3.0     9.006001     8.994001     0.012000   6.0000     6.0
 5.0    25.010001    24.990001     0.020000  10.0000    10.0
```

**Three slopes: 2, 6 and 10, at x = 1, 3 and 5.**

Put those three pairs on the board and say nothing. Somebody will see it.

```
    at x = 1  the slope is  2
    at x = 3  the slope is  6
    at x = 5  the slope is 10
```

**Two times one. Two times three. Two times five.** The slope of `x × x` is `2 × x`, every time, at every point. **And now — only now — the word is allowed:**

> **Derivative** — the slope of a curve at a point, as a rule you can use at every point. The derivative of `x × x` is `2 × x`. It is not a new kind of number and it is not a new operation; **it is the answer to the nudge-and-divide question, written down once instead of measured every time.**

![Nudge, subtract, divide - three times](../figures/fig-w12-3-nudge-and-divide-arithmetic.svg)
*Figure 12.3 — Nudge, subtract, divide - three times. Three points, the same five lines of arithmetic each, and the shortcut rule confirmed three times out of three.*

**This is the sentence to have in your pocket when a student asks whether this is "real" calculus:**

> *"Yes. Completely. The number a calculus class gets by applying a rule is the number you just got by nudging and dividing — and you got it without being told the rule. In a calculus class you would learn about twenty of these rules. In this course you will only ever need the nudge, because the computer does the rules for you from Week 20 onwards."*

**One honest warning about nudge size**, and it is worth showing because it is a real trap. Real output:

```text
--- three sizes of nudge at x = 3 on x * x ---
h = 1            slope 6.0000000000
h = 0.1          slope 6.0000000000
h = 0.01         slope 6.0000000000
h = 0.001        slope 6.0000000000
h = 1e-06        slope 6.0000000008
h = 1e-12        slope 6.0005334035
```

**Smaller is not better.** Going down to a nudge of a millionth is fine; going to a millionth of a millionth makes the answer **worse**, because you are subtracting two numbers that are nearly identical and the computer only stores about sixteen digits. **`h = 0.001` is the sweet spot and it is what this whole course uses.** If a student asks why not use an infinitely small nudge, the honest answer is *"that is what calculus does, and it is exactly why calculus exists — but a computer cannot, so it uses 0.001 and checks."*

### 5. Which way is downhill? Read the sign.

Now put the two halves together. We have a valley, and we can measure how steep it is anywhere on it. **How do we get to the bottom?**

Measure the slope where you are standing, and look at its **sign**.

Here is the loss for the ten students again, with the slope measured at each of the eight candidate values by nudging. Real output:

```text
w   0.0  loss   2464.00  slope   -616.00
w   2.0  loss   1386.00  slope   -462.00
w   4.0  loss    616.00  slope   -308.00
w   6.0  loss    154.00  slope   -154.00
w   8.0  loss      0.00  slope     -0.00
w  10.0  loss    154.00  slope    154.00
w  12.0  loss    616.00  slope    308.00
w  14.0  loss   1386.00  slope    462.00
```

**Read the sign column.** To the left of 8 every slope is **negative**. To the right of 8 every slope is **positive**. And **at** 8 the slope is **zero**.

- A **negative** slope means the ground is going *down* as you go right → **so go right.**
- A **positive** slope means the ground is going *up* as you go right → **so go left.**
- A slope of **zero** means the ground is flat → **you are at the bottom. Stop.**

**And there is one arithmetic rule that does both cases at once**, which is the elegant bit:

> **Gradient descent update rule:** `new w  =  old w  −  (learning rate) × slope`

> **Learning rate** — how big a step to take. A small positive number. It is your stride length.

**The minus sign is the entire idea.** The slope points uphill, so you step the *opposite* way, and subtracting a negative number moves you right while subtracting a positive number moves you left. **One formula, both directions, no `if` statement.**

Work it in both directions, and print both, because a student will not believe it otherwise:

```
standing at w = 2, where the slope is −12 (on the one-student loss):
    2 − 0.3 × (−12)  =  2 + 3.6   =  5.6      moved RIGHT, towards 8

standing at w = 14, where the slope is +12:
   14 − 0.3 × (+12)  =  14 − 3.6  =  10.4     moved LEFT, towards 8
```

![Which way is downhill? Read the sign.](../figures/fig-w12-5-board-which-way-is-downhill.svg)
*Figure 12.4 — Which way is downhill? Read the sign. The same bowl twice, the same rule twice, and both arrows heading towards 8.*

> **Gradient descent** — measure the slope, step the opposite way, repeat. That is the whole algorithm, and it is what sits inside `fit()` for logistic regression and for every neural network.

### 6. Eight steps, by hand

For the by-hand walk we shrink the problem to **one student** — the first one, who revised 1 hour and got 20 marks — because then the loss becomes as simple as it is possible to be:

```
loss(w)  =  (w × 1 + 12 − 20) ²  =  (w − 8) ²
```

**A parabola with its bottom exactly at 8.** And the slope, by nudging, is `2 × (w − 8)` — which you can check against the rule for `x × x` shifted along.

Now walk. Start at `w = 2`, learning rate `0.3`. This is the real output of `walk.py`:

```text
step    w        loss      slope      lr x slope     new w
   0 2.000000   36.000000 -12.000000     -3.600000   5.600000
   1 5.600000    5.760000  -4.800000     -1.440000   7.040000
   2 7.040000    0.921600  -1.920000     -0.576000   7.616000
   3 7.616000    0.147456  -0.768000     -0.230400   7.846400
   4 7.846400    0.023593  -0.307200     -0.092160   7.938560
   5 7.938560    0.003775  -0.122880     -0.036864   7.975424
   6 7.975424    0.000604  -0.049152     -0.014746   7.990170
   7 7.990170    0.000097  -0.019661     -0.005898   7.996068
after eight steps w = 7.996068    the answer we hid in the data was 8
```

**Read that table three times, because it contains everything.**

- **The `w` column marches towards 8** and never overshoots.
- **The loss column collapses**: 36 → 5.76 → 0.92 → 0.15 → 0.02 → 0.004 → 0.0006 → 0.0001.
- **The slope shrinks too**: −12 → −4.8 → −1.92 → −0.77 → −0.31 → −0.12 → −0.05 → −0.02. **A flattening slope means you are arriving.** That is the single most useful diagnostic in the entire rest of the course.
- **The steps get shorter** — 3.6, then 1.44, then 0.576 — automatically, without anybody telling them to, **because the step is proportional to the slope and the slope is dying.**

![Eight steps downhill, and the arithmetic of one step](../figures/fig-w12-4-steps-down-a-bowl-with-coordinates.svg)
*Figure 12.5 — Eight steps downhill, and the arithmetic of one step. All eight coordinates printed; the arrows get shorter every time because the ground gets flatter.*

**Every one of those rows is one multiplication and one subtraction.** Row 0, longhand:

```
slope at w = 2:      2 × (2 − 8)  =  2 × (−6)  =  −12
the step:            0.3 × (−12)  =  −3.6
the new w:           2 − (−3.6)   =  2 + 3.6   =  5.6
```

**Do all eight yourself tonight.** After the first two you will notice that the gap to 8 gets multiplied by 0.4 every time — 6, then 2.4, then 0.96, then 0.384 — and once you have seen that, you can predict every row without any arithmetic at all. **That is a lovely thing to have in your pocket when a student is stuck.**

### 7. The learning rate, and what happens when it is wrong

The learning rate is the single most consequential number anybody chooses in this course. Real output, on the full ten-student loss:

```text
lr = 0.001  after 25 steps  w =         7.1905   loss =          25.2260
lr = 0.01   after 25 steps  w =         8.0000   loss =           0.0000
lr = 0.026  after 25 steps  w =        14.3073   loss =        1531.6139
lr = 0.03   after 25 steps  w =      5135.8303   loss =  1012343768.1032
```

Read it like a doctor reading a chart:

- **`lr = 0.001`** — nothing is broken, it is just **slow.** After 25 steps it has crawled from 2 to 7.19 and it is still going. Fix: bigger steps, or more of them.
- **`lr = 0.01`** — arrived. `w = 8.0000` exactly, loss 0. Extra steps cost time and buy nothing.
- **`lr = 0.026`** — **overshooting.** Every step jumps past the bottom and lands slightly further out than it started. It is walking *away* from the answer, slowly.
- **`lr = 0.03`** — **catastrophe.** `w = 5135` and a loss of a billion. Each step leaps clean over the valley and lands higher up the far wall, then leaps back even higher.

> **⚠️ Watch out:** notice that `0.01` settles, `0.026` already does not (after 25 steps its loss, 1531, is *bigger* than the 1386 it started with) and `0.03` explodes. **There is a hard edge just below 0.026, not a gentle degradation.** The rule of thumb for the rest of the course: *if your loss is going up instead of down, first check that the update subtracts the slope; if it does, your learning rate is too big — divide it by ten and try again.*

**And note something important about the two learning rates in this lesson.** For the **one-student** loss `(w − 8)²`, `lr = 0.3` works beautifully. For the **ten-student** loss, `0.3` explodes instantly — real output:

```text
what one wrong step looks like: lr = 0.3 on the ten-student loss
  step 0  w           140.6000  loss            676936.2600
  step 1  w         -2922.4600  loss         330622438.7526
  step 2  w         64771.1660  loss      161479305330.3224
  step 3  w      -1431257.9630  loss    78868106891062.0312
```

**Same rule, same code, same starting point, and one is fine and one is a disaster.** Why? Because the ten-student valley is *thirty-eight times steeper* — its slope at w = 2 is −462, not −12. **A stride length that suits one hillside will throw you off another one**, and that is why the learning rate has to be chosen for the problem and not looked up. Say this out loud; it saves confusion in Weeks 15 and 21.

### 8. Every line of this week's code, explained to someone who has never programmed

```python
hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
marks = np.array([20, 28, 36, 44, 52, 60, 68, 76, 84, 92])
```
Two lists of ten numbers, stored as numpy arrays so that arithmetic happens to all ten at once.

```python
def loss(w):
    guess = w * hours + 12
    return ((guess - marks) ** 2).mean()
```
A named recipe. Give it a `w` and it hands back one number. Line by line: `w * hours` multiplies **all ten** hours by `w` in one go; `+ 12` adds 12 to all ten; `- marks` subtracts the ten real marks, giving ten errors; `** 2` squares all ten; `.mean()` averages them. **Five operations, ten numbers each, one number out.**

> **⚠️ Watch out:** `** 2` means "squared". `^ 2` in Python does something completely different and does **not** error. On the array `[−2, −4, −6]`, `** 2` gives `[4, 16, 36]` and `^ 2` gives `[−4, −2, −8]`. It is in the Debugging Clinic.

```python
candidates = np.linspace(0, 14, 8)
```
`np.linspace(a, b, n)` gives `n` **evenly spaced** numbers from `a` to `b`, **including both ends.** So this is `0, 2, 4, 6, 8, 10, 12, 14`. **The `8` is not optional** — leave it out and numpy gives you 50 numbers instead of 8, silently.

```python
losses = []
for w in candidates:
    losses.append(loss(w))
losses = np.array(losses)
```
Start with an empty list, work out the loss for each candidate, stick it on the end of the list, and at the end turn the list into a numpy array so it can average and compare itself.

```python
np.argmin(losses)
```
**The position of the smallest value, not the value.** `np.argmin` on our eight losses gives **4**, because the smallest loss is the fifth one in the list and Python counts from 0. To get the *value*, use `np.min`. To get *the w that produced it*, use `candidates[np.argmin(losses)]`. **Confusing these three is the single most common numpy slip there is** and it produces no error at all.

```python
ax.annotate("best of the eight: w = 8.0, loss 0.00", xy=(8.0, 0.0))
```
Write a label on a chart at an exact data position. `xy=(8.0, 0.0)` is *where*, in the chart's own units — w = 8 across, loss = 0 up. **`xy` is not optional**; leave it off and you get `TypeError: Axes.annotate() missing 1 required positional argument: 'xy'`.

```python
h = 0.001
s = (loss(w + h) - loss(w - h)) / (2 * h)
```
**The whole of the new maths, in one line.** Work out the loss a hair to the right, work out the loss a hair to the left, subtract, and divide by twice the hair. **Note the brackets round `2 * h`** — without them Python divides by 2 and then multiplies by `h`, which gives an answer a million times too small and no error message.

```python
w = w - lr * s
```
One step downhill. Multiply the slope by the stride length and subtract.

```python
rng = np.random.default_rng(0)
wobble = np.round(rng.normal(0, 4, 10), 1)
```
Week 1's random-number generator, seeded so it gives the same answer every time. `rng.normal(0, 4, 10)` gives ten random numbers centred on 0 that are typically about 4 away from it — a wobble to add to the ten perfect marks, so that we can see what a valley looks like when the data is not perfect.

### 9. The three misconceptions you will actually meet

**"The slope is a formula you look up."** No. **The slope is a measurement**, and today you measure it. The formula `2 × x` is a shortcut somebody noticed *after* doing the measurement enough times. If a student has already met derivatives at school, this is the most valuable thing you can offer them: they have the rule and they have never once checked it.

**"You subtract the slope, so a positive slope must be good."** The minus sign confuses everybody once. **Do both directions on the board with real numbers** — Figure 12.4 — and do not move on until somebody can explain why subtracting a negative number moves you right.

**"The loss going down means the model is right."** The loss going down means the model is *less wrong than it was.* Our loss reaches exactly zero only because we planted a perfect line in the data. On the wobbly version, real output:

```text
finer search of 201 values between 7 and 9:
best w = 7.9900   loss 8.9106
```

**The best possible loss is 8.91, not 0**, because ten real students do not sit on a line. **A loss that stops falling is not a failure; it is the floor of the data.** Say this once today and it will save an argument in Week 22.

### 10. How deep to go, and where to stop

| Idea | Verdict |
|---|---|
| The words *limit*, *infinitesimal*, `dy/dx`, `lim h→0` | **No. Not once.** `h = 0.001`, measured, and the phrase "a tiny nudge". |
| Symbolic differentiation rules — product rule, chain rule, quotient rule | **No.** One shortcut is *noticed* today (`x × x` → `2 × x`) and two more appear in the homework, each confirmed by measurement first. **Never a rule before its measurement.** |
| Proving that the nudge method is right | **No proofs in this course.** The evidence is that it agrees with the rule three times out of three, and it will agree again in Week 20 with a machine that uses a different method entirely. |
| The **gradient** — one slope per knob, all at once | **Week 15.** Today there is exactly **one** knob and the word "gradient" only appears inside the phrase "numerical gradient", as the name of the nudge. |
| Slopes chained together through several stages | **Week 18.** Do not hint at it. |
| Squared error being the wrong loss for classification | **Week 14.** Today's data is marks out of 100 and squared error is exactly right for it. |
| Momentum, Adam, learning-rate schedules | **Week 26**, and only Adam. |
| Local minima, saddle points, "what if the valley has two bottoms" | **Name it, do not develop it.** Honest line: *"our valley has one bottom because squared error on a straight line always does. A neural network's does not, and that is one reason they are hard."* |

---

### 11. 🧭 The Growing Map — the week the loop symbol turns black

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week it changes in three ways at once, so it is worth the full two minutes.

![The Level 3 pipeline in Week 12: stage three opens, the loop symbol turns black, and the slope tile is this week's box](../figures/fig-w12-0-where-this-fits.svg)

*Figure 12.0 — Week 12's version. Two stages finished in plain white, stage three solid because we are
now inside it, and its first tile gold. The ↻ on stage three is black for the first time.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask "which box did we do today?"** They point at the gold tile, *slope · chance ·
   loss*. Then ask the sharper version: *"which of those three words did we actually do?"* The answer
   is **slope, and only slope** — chance is next week, loss is the week after. Being able to say *"one
   third of a tile"* is exactly the kind of orientation the map exists to give.
2. **Make them find the thing that changed colour.** The ↻ on stage three has been grey in every
   figure since Week 1, and it is black from today. Somebody will spot it; let them say what it means
   before you do. *"We are inside the training loop now — it used to be a closed box."* It is the only
   mark in the whole set that changes colour for a reason other than progress, and this is the week.
3. **Tie it to the number on the board.** Point at `6.000` — the slope of `x × x` at `x = 3`, which
   the class measured by nudging — and then at the gold tile. *"That number is what filling in that box
   looked like. Everything in the three dashed stages to the right is built out of numbers like it."*

> **🧑‍🏫 Why this is worth two minutes.** Today is the most abstract lesson in Level 3 and the one most
> likely to produce *"but why are we doing this?"* The map answers that question geometrically: the
> three dashed stages to the right of the gold tile **all stand on today's division.** A learner who has
> seen that will forgive a lesson about the slope of `x × x`.

**Two things to notice, so you can answer if asked.**

- **Stage three went solid this week, not next.** A stage box goes solid the moment any one of its tiles
  is reached, and stays solid for the rest of the year. Nothing on the map ever un-fills.
- **One thread lit, and it is the new one.** `learning signal` has not been lit on its own before. From
  here to Week 23 it is the busiest thread in the level, which is the honest shape of the spring term.

---

## 🧰 Prep Checklist

### 30 minutes the night before — and spend all thirty on this one

- [ ] **Do the nudge yourself. On paper. With a pen. Right now.** This is the single most important item in the whole prep list and it takes four minutes:

```
3.001 × 3.001  =  9.006001
2.999 × 2.999  =  8.994001
                  --------
     subtract  =  0.012000

0.012000 ÷ 0.002  =  6.000
```

**If you have not done that arithmetic with your own hand, do not teach the lesson.** Everything else in the week is scaffolding around those four lines.

- [ ] **Then do it at x = 1 and x = 5**, so that you have written 2, 6 and 10 yourself and felt the moment where 2×x appears:

```
1.001 × 1.001 = 1.002001    0.999 × 0.999 = 0.998001    diff 0.004000   ÷ 0.002 = 2.000
5.001 × 5.001 = 25.010001   4.999 × 4.999 = 24.990001   diff 0.020000   ÷ 0.002 = 10.000
```

- [ ] **Do the loss at w = 6 by hand.** Ten errors, ten squares, add, divide by ten:

```
errors    −2  −4  −6  −8  −10  −12  −14  −16  −18  −20
squares    4  16  36  64  100  144  196  256  324  400     add up to 1540
1540 ÷ 10  =  154
```

- [ ] **Do all eight descent steps by hand.** They take six minutes and there is a shortcut you will spot after two: **the gap to 8 gets multiplied by 0.4 every step.** 6 → 2.4 → 0.96 → 0.384 → 0.1536 → 0.06144 → 0.024576 → 0.0098304 → 0.00393216. And `8 − 0.00393216 = 7.99606784`, which rounds to the **7.996068** the code prints.

- [ ] **Find a staircase.** Or a ramp, or a sloping corridor, or a hill outside the door. **The hook is a physical walk and it does not work sitting down.** You need somewhere you can take three steps and say "which way is down" out loud.

- [ ] **Type and run all three files yourself.** They are short and they take a second between them.

**File one — `valley.py`:**

```python
"""valley.py - eight guesses and a valley.  Week 12."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
marks = np.array([20, 28, 36, 44, 52, 60, 68, 76, 84, 92])
print("hours", hours)
print("marks", marks)

def loss(w):
    guess = w * hours + 12
    return ((guess - marks) ** 2).mean()

print()
print("check by hand at w = 6:")
print("  guesses", 6 * hours + 12)
print("  errors ", 6 * hours + 12 - marks)
print("  squared", (6 * hours + 12 - marks) ** 2)
print("  mean   ", ((6 * hours + 12 - marks) ** 2).mean())

candidates = np.linspace(0, 14, 8)
print()
print("candidates", candidates)
losses = np.array([loss(w) for w in candidates])
print("   w      loss")
for i in range(len(candidates)):
    print("%5.1f  %9.2f" % (candidates[i], losses[i]))
print("np.argmin(losses) =", np.argmin(losses))
print("so the best of the eight is w =", candidates[np.argmin(losses)])

fine = np.linspace(0, 16, 161)
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(fine, [loss(w) for w in fine], color="tab:blue")
ax.scatter(candidates, losses, s=70, color="crimson", zorder=3)
ax.annotate("best of the eight: w = 8.0, loss 0.00", xy=(8.0, 0.0))
ax.set_xlabel("w (marks per hour of revision)")
ax.set_ylabel("loss (average squared error)")
ax.set_title("Eight guesses, one valley")
plt.tight_layout()
plt.savefig("valley.png")
print("saved valley.png")
```

Real output:

```text
hours [ 1  2  3  4  5  6  7  8  9 10]
marks [20 28 36 44 52 60 68 76 84 92]

check by hand at w = 6:
  guesses [18 24 30 36 42 48 54 60 66 72]
  errors  [ -2  -4  -6  -8 -10 -12 -14 -16 -18 -20]
  squared [  4  16  36  64 100 144 196 256 324 400]
  mean    154.0

candidates [ 0.  2.  4.  6.  8. 10. 12. 14.]
   w      loss
  0.0    2464.00
  2.0    1386.00
  4.0     616.00
  6.0     154.00
  8.0       0.00
 10.0     154.00
 12.0     616.00
 14.0    1386.00
np.argmin(losses) = 4
so the best of the eight is w = 8.0
saved valley.png
```

**File two — `slope.py`:**

```python
"""slope.py - measure how steep a curve is, at one point.  Week 12."""
import numpy as np

def f(x):
    return x * x

h = 0.001
print("f(x) = x * x,   h = %.3f" % h)
print("   x      f(x+h)       f(x-h)      difference   / (2h)   2 * x")
for x in [1.0, 3.0, 5.0]:
    up, down = f(x + h), f(x - h)
    print("%4.1f  %11.6f  %11.6f  %11.6f  %7.4f  %6.1f"
          % (x, up, down, up - down, (up - down) / (2 * h), 2 * x))

print()
def g(x):
    return x * x * x
print("g(x) = x * x * x")
print("   x      g(x+h)       g(x-h)      difference   / (2h)   3 * x * x")
for x in [1.0, 3.0, 5.0]:
    up, down = g(x + h), g(x - h)
    print("%4.1f  %11.6f  %11.6f  %11.6f  %9.6f  %9.4f"
          % (x, up, down, up - down, (up - down) / (2 * h), 3 * x * x))

print()
def k(x):
    return 5 * x
print("k(x) = 5 * x")
for x in [1.0, 3.0, 5.0]:
    up, down = k(x + h), k(x - h)
    print("x = %4.1f   slope %.6f   the rule says 5" % (x, (up - down) / (2 * h)))

print()
print("--- three sizes of nudge at x = 3 on x * x ---")
for hh in [1.0, 0.1, 0.01, 0.001, 0.000001, 1e-12]:
    print("h = %-12g slope %.10f" % (hh, (f(3 + hh) - f(3 - hh)) / (2 * hh)))

print()
print("--- now the real loss, same trick ---")
hours = np.arange(1, 11)
marks = 8 * hours + 12
def loss(w):
    return (((w * hours + 12) - marks) ** 2).mean()
print("   w     loss(w)   loss(w+h)   loss(w-h)     slope    77 x (w - 8)")
for w in [2.0, 6.0, 8.0, 12.0]:
    s = (loss(w + h) - loss(w - h)) / (2 * h)
    print("%5.1f %9.4f %11.6f %11.6f %10.4f %12.1f"
          % (w, loss(w), loss(w + h), loss(w - h), s, 77 * (w - 8)))
```

Real output:

```text
f(x) = x * x,   h = 0.001
   x      f(x+h)       f(x-h)      difference   / (2h)   2 * x
 1.0     1.002001     0.998001     0.004000   2.0000     2.0
 3.0     9.006001     8.994001     0.012000   6.0000     6.0
 5.0    25.010001    24.990001     0.020000  10.0000    10.0

g(x) = x * x * x
   x      g(x+h)       g(x-h)      difference   / (2h)   3 * x * x
 1.0     1.003003     0.997003     0.006000   3.000001     3.0000
 3.0    27.027009    26.973009     0.054000  27.000001    27.0000
 5.0   125.075015   124.925015     0.150000  75.000001    75.0000

k(x) = 5 * x
x =  1.0   slope 5.000000   the rule says 5
x =  3.0   slope 5.000000   the rule says 5
x =  5.0   slope 5.000000   the rule says 5

--- three sizes of nudge at x = 3 on x * x ---
h = 1            slope 6.0000000000
h = 0.1          slope 6.0000000000
h = 0.01         slope 6.0000000000
h = 0.001        slope 6.0000000000
h = 1e-06        slope 6.0000000008
h = 1e-12        slope 6.0005334035

--- now the real loss, same trick ---
   w     loss(w)   loss(w+h)   loss(w-h)     slope    77 x (w - 8)
  2.0 1386.0000 1385.538039 1386.462038  -462.0000       -462.0
  6.0  154.0000  153.846038  154.154039  -154.0000       -154.0
  8.0    0.0000    0.000038    0.000039    -0.0000          0.0
 12.0  616.0000  616.308038  615.692039   308.0000        308.0
```

**File three — `walk.py`:**

```python
"""walk.py - eight steps downhill, by nudging.  Week 12."""
import numpy as np

h, lr = 0.001, 0.3

def one_student_loss(w):
    return (w * 1 + 12 - 20) ** 2

print("--- one student: 1 hour, 20 marks.  loss(w) = (w - 8) squared ---")
print("step    w        loss      slope      lr x slope     new w")
w = 2.0
for step in range(8):
    L = one_student_loss(w)
    s = (one_student_loss(w + h) - one_student_loss(w - h)) / (2 * h)
    new = w - lr * s
    print("%4d %8.6f %11.6f %10.6f %13.6f %10.6f" % (step, w, L, s, lr * s, new))
    w = new
print("after eight steps w = %.6f    the answer we hid in the data was 8" % w)

print()
print("--- and the shortcut rule agrees: slope of (w - 8) squared is 2 x (w - 8) ---")
for wv in [2.0, 5.6, 7.04]:
    print("w = %.2f  nudge %.6f   2 x (w - 8) = %.6f"
          % (wv, (one_student_loss(wv + h) - one_student_loss(wv - h)) / (2 * h),
             2 * (wv - 8)))

print()
print("--- all ten students, lr = 0.01, twenty-five steps ---")
hours = np.arange(1, 11)
marks = 8 * hours + 12
def loss(w):
    return (((w * hours + 12) - marks) ** 2).mean()
w, lr2 = 2.0, 0.01
for step in range(26):
    s = (loss(w + h) - loss(w - h)) / (2 * h)
    if step in [0, 1, 2, 3, 4, 10, 25]:
        print("step %2d   w %.6f   loss %11.6f   slope %11.4f" % (step, w, loss(w), s))
    w = w - lr2 * s
print("final w %.6f" % w)

print()
print("--- what a learning rate that is too big does ---")
for lr3 in [0.001, 0.01, 0.026, 0.03]:
    w = 2.0
    for step in range(25):
        s = (loss(w + h) - loss(w - h)) / (2 * h)
        w = w - lr3 * s
    print("lr = %-6s after 25 steps  w = %14.4f   loss = %16.4f" % (lr3, w, loss(w)))

print()
print("--- homework shape: (w - 4) squared, lr 0.3, six steps from w = 0 ---")
def hw(w):
    return (w - 4) ** 2
w = 0.0
for step in range(6):
    s = (hw(w + h) - hw(w - h)) / (2 * h)
    print("step %d  w %.6f  loss %.6f  slope %.6f  ->  %.6f"
          % (step, w, hw(w), s, w - 0.3 * s))
    w = w - 0.3 * s
print("after six steps w = %.6f, target 4" % w)
```

Real output:

```text
--- one student: 1 hour, 20 marks.  loss(w) = (w - 8) squared ---
step    w        loss      slope      lr x slope     new w
   0 2.000000   36.000000 -12.000000     -3.600000   5.600000
   1 5.600000    5.760000  -4.800000     -1.440000   7.040000
   2 7.040000    0.921600  -1.920000     -0.576000   7.616000
   3 7.616000    0.147456  -0.768000     -0.230400   7.846400
   4 7.846400    0.023593  -0.307200     -0.092160   7.938560
   5 7.938560    0.003775  -0.122880     -0.036864   7.975424
   6 7.975424    0.000604  -0.049152     -0.014746   7.990170
   7 7.990170    0.000097  -0.019661     -0.005898   7.996068
after eight steps w = 7.996068    the answer we hid in the data was 8

--- and the shortcut rule agrees: slope of (w - 8) squared is 2 x (w - 8) ---
w = 2.00  nudge -12.000000   2 x (w - 8) = -12.000000
w = 5.60  nudge -4.800000   2 x (w - 8) = -4.800000
w = 7.04  nudge -1.920000   2 x (w - 8) = -1.920000

--- all ten students, lr = 0.01, twenty-five steps ---
step  0   w 2.000000   loss 1386.000000   slope   -462.0000
step  1   w 6.620000   loss   73.319400   slope   -106.2600
step  2   w 7.682600   loss    3.878596   slope    -24.4398
step  3   w 7.926998   loss    0.205178   slope     -5.6212
step  4   w 7.983210   loss    0.010854   slope     -1.2929
step 10   w 7.999998   loss    0.000000   slope     -0.0002
step 25   w 8.000000   loss    0.000000   slope     -0.0000
final w 8.000000

--- what a learning rate that is too big does ---
lr = 0.001  after 25 steps  w =         7.1905   loss =          25.2260
lr = 0.01   after 25 steps  w =         8.0000   loss =           0.0000
lr = 0.026  after 25 steps  w =        14.3073   loss =        1531.6139
lr = 0.03   after 25 steps  w =      5135.8303   loss =  1012343768.1032

--- homework shape: (w - 4) squared, lr 0.3, six steps from w = 0 ---
step 0  w 0.000000  loss 16.000000  slope -8.000000  ->  2.400000
step 1  w 2.400000  loss 2.560000  slope -3.200000  ->  3.360000
step 2  w 3.360000  loss 0.409600  slope -1.280000  ->  3.744000
step 3  w 3.744000  loss 0.065536  slope -0.512000  ->  3.897600
step 4  w 3.897600  loss 0.010486  slope -0.204800  ->  3.959040
step 5  w 3.959040  loss 0.001678  slope -0.081920  ->  3.983616
after six steps w = 3.983616, target 4
```

**Expected runtime: all three files together, under one and a half seconds.** If your `slope.py` does not print `6.0000` at `x = 3.0`, check the brackets round `2 * h`.

- [ ] **Break it on purpose, twice, so you have seen both live.**
  1. `s = (f(x + h) - f(x - h)) / 2 * h` — brackets missing round `2 * h`. **No error.** You get `0.000006` instead of `6.000000`, which is a factor of a million out. This is deliberate mistake one.
  2. `w = w + lr * s` — plus instead of minus. **No error.** The loss goes 92, 236, 604, 1546, 3958 — **up, and fast.** This is deliberate mistake two and it is the one that teaches the sign.

- [ ] **Print workbook pages 12.1–12.6.**
- [ ] **Three sheets of squared graph paper per student**, plus one big sheet for the wall with axes already drawn: `w` from 0 to 16 across, `loss` from 0 to 2500 up.
- [ ] **A calculator each.** There are about sixty divisions in this lesson.
- [ ] **Do not wipe last week's `BY HAND | np.trapz` board.** You will point at that tick when you compare the measured slope with the shortcut rule, and it saves you a paragraph.

### 5 minutes on the day

- [ ] Terminal in the working folder. **All three `.py` files deleted or renamed** — they type them.
- [ ] The big graph paper on the wall with axes drawn, **blank otherwise**.
- [ ] Graph paper handed out, three sheets each.
- [ ] Calculators out.
- [ ] The staircase or ramp identified, and you know how you are getting the class to it and back inside four minutes.
- [ ] Workbook 12.1 out. Nothing filled in.
- [ ] Bug Log open at a fresh page.
- [ ] **The word "derivative" written on a folded piece of paper in your pocket**, to be unfolded at minute 22 and not before. This sounds like theatre. It is theatre, and it works.

### Fallback if the laptops fail

**This is the most computer-proof lesson of the entire year, and arguably the best version of it.** All four objectives are pencil-and-paper work.

1. **The staircase.** Objective 4's intuition, and it needs no electricity by definition.
2. **The eight losses, by hand.** Eight rows, ten squarings each — that is a lot, so **split them across the room, one candidate per pair**, and collect the answers on the board. Ten minutes, and objective 1 is complete with a valley on the wall. All eight answers are in the Answer Key.
3. **The three nudges.** `3.001 × 3.001` on a calculator, `2.999 × 2.999`, subtract, divide. **Objectives 2 and 3 need a calculator and nothing else**, and the moment where 2, 6, 10 turns into 2×x is *better* without a screen, because nobody can suspect the computer of arranging it.
4. **The eight descent steps.** One multiplication and one subtraction per row. **Objective 4, complete**, and the whole table is in the Answer Key.

| If this fails | Do this instead |
|---|---|
| `slope.py` prints `0.000006` at x = 3 | Brackets missing: it must be `/ (2 * h)`, not `/ 2 * h`. **Deliberate mistake one arriving early, which is fine.** |
| `TypeError: can only concatenate list (not "int") to list` | `hours` was typed as a plain Python list, not `np.array([...])`. `w * hours` on a list *repeats the list* instead of multiplying it. |
| `np.linspace(0, 14)` gives 50 candidates | The `8` was left off. `np.linspace` defaults to 50. |
| `np.argmin` gives 4 and a student writes "the best w is 4" | It gives the **position**, not the value. `candidates[np.argmin(losses)]` gives 8.0. |
| `TypeError: Axes.annotate() missing 1 required positional argument: 'xy'` | `ax.annotate("text")` with no position. Add `xy=(8.0, 0.0)`. |
| The loss goes **up** every step | `w = w + lr * s` instead of `w - lr * s`. **Deliberate mistake two arriving by accident — teach it there and then.** |
| The loss explodes to a billion | The learning rate is too big. On the ten-student loss, 0.03 explodes and 0.01 works. **Divide by ten.** |
| A student has already done calculus and is bored | Send them to the "flying" path immediately: measure the slope of `x × x × x` at three points, notice `3 × x × x`, then try to guess the pattern for `x⁴` **before** measuring it, and check. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Walk Down a Real Staircase | 7 | 7 | Feet, fog, "which way is down" |
| 🧠 Concept & Maths — Nudge and Divide | 18 | 25 | The valley, then three slopes, then the word |
| 💻 Live-Code Together — `valley.py` and `slope.py` | 18 | 43 | Paper checked against code. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Foggy Hillside | 20 | 63 | Three students per point, then eight steps by hand |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Walk Down a Real Staircase (7 minutes)

**Do this:** Take the class to the staircase, ramp or sloping corridor. **Actually go.** This is four minutes of walking and it is worth it.

**Say this, standing at the top:**

> "I want you to imagine that it is so foggy you cannot see more than the length of your own foot. You are somewhere on a hillside, and you want to get to the bottom, and you cannot see the bottom. You cannot see anything.
>
> **What can you still do?**"

*Somebody will say: feel the ground.*

> "You can feel the ground under your feet. That is all you have got. So — do it."

**Do this:** Have one student stand on a step and describe out loud, in words, what their two feet can tell them.

**Ask this:** "Put your left foot forward. Is the ground higher or lower than where you are standing?"

*Answer: lower.*

**Ask this:** "Now put your right foot backwards. Higher or lower?"

*Answer: higher.*

> "So forwards is down and backwards is up, and you did not need a map, and you did not need to see the valley. **You needed two feet and one comparison.** Take a step forwards."

**Do this:** Get three or four students to take a step each, saying "down" out loud as they go. Then back to the room.

**Say this, once you are all sitting down:**

> "That is the entire lesson. Everything else today is arithmetic.
>
> Since Week 3 you have typed `model.fit(X, y)` about forty times, and inside many of those models (logistic regression now, every neural network to come) something has been standing on a foggy hillside with two feet, going *'is it lower this way? Yes. Step.'* — a few hundred times over. **Nobody has ever shown you how it feels the ground.**
>
> Today you find out. And the answer is: **two subtractions and a division.** That is it. That is the whole secret."

**Do this:** Write this on the board and leave it there all lesson.

```
   how wrong am I?              ->   a number.  we call it the LOSS.
   which way is downhill?       ->   ???        <- today
   step that way, a bit         ->   easy.
   go back to the top           ->   easy.
```

---

### 🧠 Concept & Maths — Nudge and Divide (18 minutes)

**Step 1 (7 min) — the loss, and the valley.**

**Do this:** Write the ten students on the board.

```
hours    1    2    3    4    5    6    7    8    9   10
marks   20   28   36   44   52   60   68   76   84   92
```

**Ask this:** "Every extra hour is worth how many marks? And what does somebody who revises nothing get?"

*Hoped-for answer:* 8 marks an hour, and 12 for nothing.

*If they cannot see it:* point at the gaps. 20 to 28 is 8. 28 to 36 is 8. And 20 − 8 = 12.

> "So the answer is `marks = 8 × hours + 12`, and you found it in fifteen seconds by looking, and a computer cannot look. **We are going to hide that 8 from ourselves and make a machine find it**, and the reason we are using data where we already know the answer is so that we can tell whether the machine worked.
>
> The 12 we will give away for free. The **one** thing we do not know is the 8. Call it `w`."

**Do this:** Write the model:

```
predicted marks  =  w × hours  +  12
```

**Say this:**

> "Now guess. Somebody give me a value for `w`."

Take whatever they say; then insist on 6, because the arithmetic is clean.

**Do this:** Build the loss table on the board, out loud, one row at a time. **Get the class to call out the errors.**

```
w = 6
  predicted   18   24   30   36   42   48   54   60   66   72
  actual      20   28   36   44   52   60   68   76   84   92
  error       −2   −4   −6   −8  −10  −12  −14  −16  −18  −20
  squared      4   16   36   64  100  144  196  256  324  400
```

**Ask this:** "Why square them?"

*Hoped-for answer:* so the negatives do not cancel out.

> "So the minuses do not cancel. If I just added those errors up I would get −110, and if half of them had been positive I might have got zero, and a model that is wrong about everything would look perfect. **Squaring makes every mistake count as a mistake.** It also makes a big miss hurt more than a small one, which is a choice somebody made and it is a reasonable one."

**Ask this:** "Add the squares up and divide by ten."

```
1540 ÷ 10  =  154
```

> "**One hundred and fifty-four.** That is the loss at `w = 6`. One number, meaning 'this is how wrong you are'. Big is bad, zero is perfect."

**Do this:** Now hand out the other seven candidates — `w = 0, 2, 4, 8, 10, 12, 14` — one per pair, calculators out, **four minutes.** Collect the answers on the big graph paper on the wall as they come in.

```
  w         0      2      4      6      8     10     12     14
  loss   2464   1386    616    154      0    154    616   1386
```

**Ask this:** "What shape is that?"

*Hoped-for answer:* a valley, a U, a bowl.

**Ask this — and this is the good question:** "Why do `w = 6` and `w = 10` give the *same* loss?"

*Hoped-for answer:* they are both 2 away from 8, and the errors get squared so the sign does not matter.

> "**A valley.** And a symmetric one, because being two too low is exactly as bad as being two too high once you square it. It has a name — the **loss surface** — and today it is a curve because we have one knob. Two knobs would make it a landscape. A neural network has a hundred thousand knobs and nobody can draw its loss surface at all, ever. **That is why we are learning to walk on it with our feet instead of looking at it.**"

**Ask this:** "So — we found the answer. Eight guesses and the winner is 8. Why is that not the end of the lesson?"

*Hoped-for answer:* we got lucky; 8 was one of our guesses.

**Do this:** Write on the board:

```
   1 knob,   8 guesses each  ->  8
   2 knobs                   ->  8 × 8      =  64
   3 knobs                   ->  8 × 8 × 8  =  512
   100,000 knobs             ->  8 to the power of a hundred thousand
```

> "**Guessing does not scale.** So we go back to the staircase."

**Step 2 (8 min) — 🔢 nudge and divide.**

**Do this:** Clear a space. Write one thing on the board:

```
   f(x) = x × x
```

**Say this:**

> "Forget marks and revision for four minutes. Simplest curve there is. `x` times `x`.
>
> I want to know **how steep it is at x = 3.** Not between two points — in Week 10 we did between two points, and it was rise over run. I want the steepness **at** three. One place.
>
> And there is a problem: a slope needs two points. So here is the trick, and it is the whole of today.
>
> **Take two points that are almost the same one.**"

**Do this:** Write it on the board, one line at a time, and **do the multiplications out loud.**

```
   a hair to the right:   3.001 × 3.001  =  9.006001
   a hair to the left:    2.999 × 2.999  =  8.994001
```

**Ask this:** "How much did the answer change?"

```
   9.006001 − 8.994001  =  0.012000
```

**Ask this:** "And how far did we move to make that happen?"

```
   3.001 − 2.999  =  0.002
```

**Ask this:** "So how steep is it?"

```
   0.012000 ÷ 0.002  =  6.000
```

> "**Six.** And notice what just happened: **that is rise over run again.** Exactly what you did in Week 10 on the ROC curve. The only difference is that the two points are a thousandth of a unit apart instead of a tenth."

**Do this:** Now the bit that makes it an idea. Split the room into three groups.

> "Group one: do it at **x = 1**. Group two: **x = 3** again, to check us. Group three: **x = 5.** Calculators. Two minutes. I want four numbers from each of you: the value above, the value below, the difference, and the difference divided by 0.002."

**Do this:** Collect the three answers on the board. **Nothing else. No commentary.**

```
   at x = 1     1.002001 − 0.998001 = 0.004000     ÷ 0.002 =  2
   at x = 3     9.006001 − 8.994001 = 0.012000     ÷ 0.002 =  6
   at x = 5    25.010001 − 24.990001 = 0.020000    ÷ 0.002 = 10
```

**Do this:** Underline the three answers. **2, 6, 10.** Then stand back and say nothing for ten seconds.

**Ask this:** "Anybody?"

*Hoped-for answer:* they are double the x.

*If nobody sees it:* write `1  3  5` on one line and `2  6  10` underneath it, aligned. Then wait again.

> "**Two times one. Two times three. Two times five.** The slope of `x × x` is `2 × x`. Always. Everywhere. And you did not look that up in a book — **you measured it three times and then noticed it.**"

**Do this:** Take the folded paper out of your pocket. Unfold it. It says **DERIVATIVE**.

> "It has a name. This is it. This is the whole thing.
>
> **A derivative is the slope of a curve at a point, written down as a rule so you do not have to measure it every time.** That is all. People spend a term being frightened of that word and it means *the number you just worked out on a calculator.*
>
> There is a whole subject about finding those rules quickly, and there are about twenty of them, and **you are not going to learn any of them**, because from Week 20 the computer will do them for you. What you needed is the thing underneath, and you have it: **nudge, subtract, divide.**"

**Step 3 (3 min) — name the rest, and the sign.**

Blockquote each on the board.

> **Loss** — one number saying how wrong the model is. Big is bad, zero is perfect.

> **Loss surface** — the shape you get by plotting loss against the value of a weight.

> **Numerical gradient** — a slope measured by nudging and dividing. Slow, and honest while the nudge is sensible.

> **Learning rate** — how big a step you take. Your stride length.

> **Gradient descent** — measure the slope, step the opposite way, repeat.

**Do this:** The sign. Two mini-bowls on the board, side by side, exactly as in Figure 12.4.

**Ask this:** "I am standing on the left wall at `w = 2` and I measure the slope. It comes out **negative twelve.** Which way should I move?"

*Hoped-for answer:* right.

> "Right, towards 8. And here is the rule that does it:
>
> **new w = old w − (learning rate) × slope**"

**Do this:** Work it, with the numbers, on the board:

```
   2 − 0.3 × (−12)  =  2 + 3.6  =  5.6      moved RIGHT ✅
```

**Ask this:** "Now I am on the right wall at `w = 14`, and the slope is **plus twelve.** Same formula. What happens?"

```
   14 − 0.3 × (+12)  =  14 − 3.6  =  10.4    moved LEFT ✅
```

> "**One rule, both directions, no decisions.** Subtracting a negative moves you right; subtracting a positive moves you left. **The minus sign is the whole algorithm**, and it is the thing you will get wrong once, this week, and never again."

---

### 💻 Live-Code Together — `valley.py` and `slope.py` (18 minutes)

**You never touch their keyboard.** They type; you type the same thing on the shared screen.

**Step 1 (6 min) — `valley.py`.**

New file. Everything down to `so the best of the eight is`. (Full text in the Prep Checklist.)

> **Say this, about the one new function:** "`np.linspace(0, 14, 8)` means *eight evenly spaced numbers from 0 to 14, including both ends.* So 0, 2, 4, 6, 8, 10, 12, 14. **The 8 is not optional** — leave it off and numpy hands you fifty numbers without complaining."

**Ask before running:** "What will the `w = 6` row say?"

*Hoped-for answer:* 154. It is on the board in their own handwriting.

Run it. Real output:

```text
hours [ 1  2  3  4  5  6  7  8  9 10]
marks [20 28 36 44 52 60 68 76 84 92]

check by hand at w = 6:
  guesses [18 24 30 36 42 48 54 60 66 72]
  errors  [ -2  -4  -6  -8 -10 -12 -14 -16 -18 -20]
  squared [  4  16  36  64 100 144 196 256 324 400]
  mean    154.0

candidates [ 0.  2.  4.  6.  8. 10. 12. 14.]
   w      loss
  0.0    2464.00
  2.0    1386.00
  4.0     616.00
  6.0     154.00
  8.0       0.00
 10.0     154.00
 12.0     616.00
 14.0    1386.00
np.argmin(losses) = 4
so the best of the eight is w = 8.0
```

**Do this:** Point at `errors` and then at the same row on the board, in their handwriting. **Every one of the ten numbers matches.** Let that land.

> **Say this:** "Your paper and the computer agree on all ten errors, all ten squares and the average. That is not luck. **You are not learning to trust the computer; you are learning that the computer is doing what you just did, faster.**"

**Ask this:** "`np.argmin(losses)` printed **4.** Our best `w` is **8**. What is going on?"

*Hoped-for answer:* 4 is the position, not the value.

> **Say this:** "`argmin` gives you **where** the smallest thing is, not **what** it is. The smallest loss is the fifth in the list, and Python counts from zero, so 4. To get the value you want, you have to go and fetch it: `candidates[4]`, which is 8.0.
>
> **`np.min` gives you the value. `np.argmin` gives you the position.** Mixing those up produces no error at all, ever, and it is one of the most common bugs in numpy."

Add the plotting block and run again. `saved valley.png`. Open it.

> **Say this about `annotate`:** "`ax.annotate("text", xy=(8.0, 0.0))` writes a label at an exact spot **in the chart's own units** — 8 across, 0 up. Not pixels. That `xy=` is compulsory; leave it off and it crashes."

**Step 2 (6 min) — `slope.py` and 🐞 DELIBERATE MISTAKE ONE.**

New file. Type the `x × x` section — **but leave the brackets off `2 * h`**:

```python
def f(x):
    return x * x

h = 0.001
for x in [1.0, 3.0, 5.0]:
    up, down = f(x + h), f(x - h)
    print("x = %.1f   slope %.6f" % (x, (up - down) / 2 * h))
```

Real output:

```text
x = 1.0   slope 0.000002
x = 3.0   slope 0.000006
x = 5.0   slope 0.000010
```

**Do this:** Point at the board where it says **6.000**. Then at the screen where it says **0.000006**.

**Ask this:** "Was that an error?"

*Answer:* no.

**Ask this:** "Six, and nought point nought nought nought nought nought six. How far out is that?"

*Hoped-for answer:* a million.

> **Say this:** "A factor of a million, no crash, no warning. Because `/ 2 * h` means *divide by 2, then multiply by h* — Python works left to right — and I meant *divide by (2 times h)*. **Brackets.**
>
> And notice how you caught it: **you had the right answer on paper first.** If you had gone straight to the code you would have written down 0.000006 and moved on, and everything after it would have been wrong. **That is what doing the arithmetic by hand first is for.**"

Fix it — `/ (2 * h)` — and run the full first section:

```text
f(x) = x * x,   h = 0.001
   x      f(x+h)       f(x-h)      difference   / (2h)   2 * x
 1.0     1.002001     0.998001     0.004000   2.0000     2.0
 3.0     9.006001     8.994001     0.012000   6.0000     6.0
 5.0    25.010001    24.990001     0.020000  10.0000    10.0
```

> **Say this:** "Last column is the shortcut rule. Two out of two, three times out of three. **Same tick we drew last week between `BY HAND` and `np.trapz`.**"

**Do this:** Bug Log entry, sixty seconds. Message: *none*. Symptom: an answer a million times too small. Fix: *brackets round `2 * h`*.

**Step 3 (3 min) — a second and third curve, and how small a nudge can be.**

Add the `x × x × x` and `5 × x` sections and run:

```text
g(x) = x * x * x
   x      g(x+h)       g(x-h)      difference   / (2h)   3 * x * x
 1.0     1.003003     0.997003     0.006000   3.000001     3.0000
 3.0    27.027009    26.973009     0.054000  27.000001    27.0000
 5.0   125.075015   124.925015     0.150000  75.000001    75.0000

k(x) = 5 * x
x =  1.0   slope 5.000000   the rule says 5
x =  3.0   slope 5.000000   the rule says 5
x =  5.0   slope 5.000000   the rule says 5
```

**Ask this:** "For `x × x × x` the measured answer is 3.000001 and the rule says 3. Which one is right?"

*Hoped-for answer:* the rule; the measurement is very slightly off.

> **Say this:** "The rule. My nudge is not infinitely small, so I am off by a millionth. **And that is honest and it is fine** — nobody has ever cared about the sixth decimal place of a slope.
>
> And look at the straight line, `5 × x`. **The slope is 5 everywhere.** Of course it is. A straight line has one steepness and it never changes."

Add the nudge-size section:

```text
--- three sizes of nudge at x = 3 on x * x ---
h = 1            slope 6.0000000000
h = 0.1          slope 6.0000000000
h = 0.01         slope 6.0000000000
h = 0.001        slope 6.0000000000
h = 1e-06        slope 6.0000000008
h = 1e-12        slope 6.0005334035
```

**Ask this:** "Smaller nudge, better answer. True or false?"

*Hoped-for answer:* somebody will say true; the table says otherwise.

> **Say this:** "**False, and there is a floor.** A nudge of a millionth is fine. A nudge of a millionth of a millionth is **worse** — 6.0005 instead of 6.0000 — because I am subtracting two numbers that are nearly identical, and the computer only keeps about sixteen digits. Subtracting almost-equal numbers throws digits away.
>
> **`h = 0.001` for the rest of the year.** That is the whole rule."

**Step 3b (3 min) — 🐞 DELIBERATE MISTAKE TWO: the sign.**

Type the descent loop, **with a plus**:

```python
def L(w):
    return (w - 8) ** 2

h, lr = 0.001, 0.3
w = 2.0
for i in range(5):
    s = (L(w + h) - L(w - h)) / (2 * h)
    w = w + lr * s
    print("step %d  w %.4f  loss %.4f" % (i, w, L(w)))
```

Real output:

```text
step 0  w -1.6000  loss 92.1600
step 1  w -7.3600  loss 235.9296
step 2  w -16.5760  loss 603.9798
step 3  w -31.3216  loss 1546.1882
step 4  w -54.9146  loss 3958.2419
```

**Ask this:** "Read me the loss column."

*Hoped-for answer:* it is going up. Fast.

> **Say this:** "Ninety-two, two hundred and thirty-six, six hundred, one and a half thousand, four thousand. **We are climbing.** And `w` has gone from 2 to minus fifty-five, in the wrong direction, away from 8, faster and faster.
>
> One character. **Plus instead of minus.** The slope points *uphill*, so if you add it you go uphill.
>
> **And here is the rule for the rest of your life: if your loss is going up, look at the sign first, and the learning rate second.**"

Fix it to `w = w - lr * s` and run:

```text
step 0  w 5.6000  loss 5.7600
step 1  w 7.0400  loss 0.9216
step 2  w 7.6160  loss 0.1475
step 3  w 7.8464  loss 0.0236
step 4  w 7.9386  loss 0.0038
```

**Bug Log. Second entry, and make sure the words "the loss went up" are in it.**

---

### 🎲 Their Turn — The Foggy Hillside (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: three students per point measure the slope of `w × w` at `w = 1, 3, 5` on graph paper with `h = 0.001`, and all three answers go on the board **before anybody says the word derivative**; then everybody walks eight steps downhill by hand and compares their final `w` with the 8 hidden in the data.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand between the valley on the wall and the three slopes on the board.

**Say this:**

> "Look at what is on the walls.
>
> A valley you built out of eighty subtractions and eighty squarings. Three slopes you measured with a calculator — **two, six and ten** — and then noticed were `2 × x`. And eight rows of a table that starts at 2 and ends at **7.996068**, where the answer hidden in the data was **8**.
>
> Nothing in that sentence needed calculus. It needed a subtraction and a division, done twice."

**Do this:** Go back to the board from the hook and fill in the gap.

```
   how wrong am I?              ->   a number.  the LOSS.
   which way is downhill?       ->   nudge, subtract, divide.  READ THE SIGN.
   step that way, a bit         ->   w = w − lr × slope
   go back to the top           ->   repeat.
```

**Say this:**

> "**That is the engine inside `fit()`** for logistic regression and for every neural network. Every time you fitted one of those since Week 3, a loop like this ran, a few hundred times (a plain `LinearRegression` reaches its best line by algebra instead, and trees and nearest-neighbours work in other ways again, but you now know what the loop is).
>
> And you should feel slightly annoyed with me, because it took nine weeks."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "Two things to know about what happens next.
>
> **The first is a promise.** In Week 20 a machine called PyTorch is going to work out slopes for you, and it will not nudge and it will not divide — it uses a completely different method. And the first thing we will do with it is ask it for the slope of `x × x` at `x = 3`. **It is going to say six.** Not 5.9998. Six. And when it does, you will know it is right, **because you measured it yourself with a calculator in Week 12.** That is what today buys you: for the rest of this course, you can check the machine.
>
> **The second is a warning.** Today we had **one** knob. Next week we get a model whose answers have to come out between 0 and 1 — because 'how likely is it that this is fraud' cannot be 92 marks — and after that, a loss that is right for probabilities instead of exam marks. And by Week 18 there will be a hundred knobs, all connected to each other, and the question *'how much did each one contribute to the error'* becomes the hardest thing you will do this year.
>
> **All of it is today's arithmetic. Nudge, subtract, divide, read the sign, step.** Nothing else ever gets added."

**Do this:** Hand out the homework and read the last part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `TypeError: can only concatenate list (not "int") to list` | "You tried to add a number to a list, and lists do not do that." | `hours = [1, 2, 3, ...]` typed as a plain Python list, then `w * hours + 12`. | `hours = np.array([1, 2, 3, ...])`. **Then the arithmetic happens to every element.** |
| `TypeError: Axes.annotate() missing 1 required positional argument: 'xy'` | "You told me what to write but not where." | `ax.annotate("best of the eight")` with no position. | `ax.annotate("best of the eight", xy=(8.0, 0.0))`. The position is in the chart's own units. |
| `AttributeError: 'list' object has no attribute 'mean'` | "Plain Python lists cannot average themselves." | `losses` built by appending and then `losses.mean()`. | `np.array(losses).mean()`. |
| `IndexError: index 8 is out of bounds for axis 0 with size 8` | "There is no eighth thing in a list of eight, because I count from zero." | `candidates[len(candidates)]` instead of `candidates[np.argmin(losses)]`. | Eight items are numbered 0 to 7. |
| `ZeroDivisionError: float division by zero` | "You divided by nothing." | `h = 0` — a nudge of zero. | A nudge has to be a real nudge. `h = 0.001`. **And this is the honest reason calculus exists: you cannot actually set the nudge to zero.** |
| `ValueError: x and y must have same first dimension, but have shapes (161,) and (8,)` | "Those two lists are different lengths." | Plotting the eight candidate losses against the 161-point fine grid. | Plot `candidates` against `losses`, and `fine` against the fine losses. Two separate calls. |
| **No error. The slope comes out `0.000006` instead of `6.000000`.** | Nothing crashed. Your answer is a million times too small. | Brackets: `/ 2 * h` divides by 2 *then multiplies* by h. | `/ (2 * h)`. **Sanity check: the slope of `x × x` at 3 is about 6, so an answer near zero is wrong before you read another line.** |
| **No error. The slope comes out `12.000000` instead of `6.000`.** | Nothing crashed. Exactly twice the right answer. | Dividing by `h` instead of by `2 * h`. You moved a nudge each way, so you moved **two** nudges in total. | `/ (2 * h)`. **Sanity check: if your answer is exactly double the shortcut rule's, you divided by half the distance you actually travelled.** |
| **No error. The loss goes UP every step, fast.** | Nothing crashed. You are climbing the hill. | `w = w + lr * s`. The slope points uphill, so adding it goes uphill. | `w = w - lr * s`. **If your loss rises, check the sign before anything else.** |
| **No error. `w` becomes 5135.8303 and the loss becomes a billion.** | Nothing crashed. Your stride is longer than the valley. | Learning rate too big. On the ten-student loss, `0.026` slowly diverges and `0.03` explodes. | **Divide the learning rate by ten and run it again.** No other diagnosis first. |
| **No error. `np.argmin` says 4 and the student writes "the best w is 4".** | Nothing crashed. You read the position as the value. | `print(np.argmin(losses))` instead of `print(candidates[np.argmin(losses)])`. | `np.min` gives the value, `np.argmin` gives the position, `candidates[np.argmin(...)]` gives the thing you actually want. |
| **No error. `np.linspace(0, 14)` produces 50 rows instead of 8.** | Nothing crashed. numpy filled in a default. | The third argument was left off. | `np.linspace(0, 14, 8)`. |
| **No error. Every squared error comes out negative.** | Nothing crashed, and the arithmetic is nonsense. | `error ^ 2` instead of `error ** 2`. On `[−2, −4, −6]`, `** 2` gives `[4, 16, 36]` and `^ 2` gives `[−4, −2, −8]`. | `** 2`. **`^` is not "to the power of" in Python, and it does not complain.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two, and they are the two you will use most for the rest of the year.

23. **"What do you expect that number to be, roughly, before you look?"** The slope of `x × x` at 3 is about 6. So `0.000006` and `6001` are both wrong **before you read a single line of code.** A student who computes on paper first has a check; a student who does not has nothing.

24. **"Is the loss going up or down?"** For any descent loop that misbehaves. Up means the sign or the learning rate. Down but stalling means the learning rate is too small. **Two questions, two answers, and it covers almost everything for the next fifteen weeks.**

And the sentence for this week:

> **"Every single thing in this lesson can be checked on a calculator. That is not a limitation of the lesson — it is the whole reason to trust it."**

---

## 🎲 The Activity, In Full

### The Foggy Hillside

**What it is.** Two halves. In the first, **three students per point** measure the slope of `w × w` at `w = 1`, `3` and `5` with `h = 0.001`, and all three answers go on the board **before anybody says the word derivative.** In the second, **everybody walks eight steps downhill by hand** on `(w − 8)²` and compares their final `w` with the answer hidden in the data.

**Why three students per point.** Because the pattern has to be **discovered by the room and not announced by the adult.** If one person computes all three answers, they see 2, 6, 10 in sequence and half of them spot it. If three separate groups each own one number and the three numbers go up on the board together, **the whole room sees them at once and somebody always shouts.** That moment is what the lesson is for and it is worth engineering.

> **📌 What the board should look like when all three groups have finished is Figure 12.3 above** — three panels, the same five lines of arithmetic each, and a tick under every one.

### Setup

- **Three groups**, however you like. With fewer than three students, one person does all three but **writes each answer on a separate card, face down, and turns all three over at once.** The reveal has to be simultaneous.
- **Graph paper and a calculator each.**
- **A clear strip of board, divided into three columns headed `x = 1`, `x = 3`, `x = 5`.** Nothing else written on it.
- **Your folded piece of paper with DERIVATIVE on it, still in your pocket.**

### Part 1 — three slopes (8 minutes)

**Minute 0–1 — the instruction, word for word.** Read it out; do not paraphrase, because the precision matters.

> "Your group has one number: 1, 3 or 5. Call it `x`.
>
> **Four things, in this order, on your graph paper.**
>
> One: work out `x` plus nought point nought nought one, times itself. Write down all six decimal places.
> Two: work out `x` minus nought point nought nought one, times itself. All six decimals.
> Three: **subtract** the second from the first.
> Four: **divide** by nought point nought nought two.
>
> Do not tell anybody your answer. Do not come and ask me if it is right. **When you have it, write it on a card and put the card face down.**"

**Minute 1–5 — they work.** Walk round. Answer exactly one kind of question: *"is my subtraction right?"* Answer nothing else. **In particular, if somebody asks "why 0.002?" say "because you moved a thousandth each way, so you moved two thousandths in total" and walk away.**

The three groups' working:

```
   x = 1:   1.001 × 1.001  =   1.002001
            0.999 × 0.999  =   0.998001
            subtract       =   0.004000
            ÷ 0.002        =   2.000

   x = 3:   3.001 × 3.001  =   9.006001
            2.999 × 2.999  =   8.994001
            subtract       =   0.012000
            ÷ 0.002        =   6.000

   x = 5:   5.001 × 5.001  =  25.010001
            4.999 × 4.999  =  24.990001
            subtract       =   0.020000
            ÷ 0.002        =  10.000
```

**Minute 5–7 — the simultaneous reveal.** All three cards turned over at the same time, all three numbers written on the board at the same time, in their three columns.

```
        x = 1        x = 3        x = 5
          2            6           10
```

**Do this:** Say nothing. Count to ten in your head.

**Ask this:** "Anybody?"

*If nobody sees it after ten more seconds:* write `1   3   5` on the line above, carefully aligned, and wait again. Somebody always gets it within five seconds of the alignment.

**Minute 7–8 — the word.** Unfold the paper. Say the two sentences from the Concept segment and no more. **Do not develop it, do not generalise it, do not mention any other function. The next eight minutes are needed for the walk.**

### Part 2 — eight steps downhill (12 minutes)

**Minute 0–2 — set it up.** On the board:

```
   loss(w) = (w − 8) × (w − 8)          <- one student: 1 hour, 20 marks

   the rule:   new w  =  old w  −  0.3 × slope

   start at    w = 2
```

**Say this:**

> "You are on the foggy hillside. You are standing at 2. You cannot see the bottom. **Eight steps. Go.**
>
> For each step: measure the slope by nudging — or use the shortcut you just discovered, `2 × (w − 8)`, if you trust it — then multiply by nought point three, then subtract."

> **💡 Try this:** let them choose whether to nudge or use the shortcut, **and require the first two rows to be done both ways.** They will match, and that is the point of the whole term: a shortcut you have verified is a shortcut you may use.

**Minute 2–10 — they walk.** Eight rows, one multiplication and one subtraction each. The table:

| step | w | loss | slope | 0.3 × slope | new w |
|---|---|---|---|---|---|
| 0 | 2.000000 | 36.000000 | −12.000000 | −3.600000 | 5.600000 |
| 1 | 5.600000 | 5.760000 | −4.800000 | −1.440000 | 7.040000 |
| 2 | 7.040000 | 0.921600 | −1.920000 | −0.576000 | 7.616000 |
| 3 | 7.616000 | 0.147456 | −0.768000 | −0.230400 | 7.846400 |
| 4 | 7.846400 | 0.023593 | −0.307200 | −0.092160 | 7.938560 |
| 5 | 7.938560 | 0.003775 | −0.122880 | −0.036864 | 7.975424 |
| 6 | 7.975424 | 0.000604 | −0.049152 | −0.014746 | 7.990170 |
| 7 | 7.990170 | 0.000097 | −0.019661 | −0.005898 | 7.996068 |

**Minute 10–12 — read the table out loud, three times.**

**Ask this:** "What is the `w` column doing?"

*Hoped-for answer:* creeping up on 8 and never going past it.

**Ask this:** "What is the **slope** column doing?"

*Hoped-for answer:* getting smaller.

> "**That is the most useful thing on the page.** The slope started at −12 and finished at −0.02. **A flattening slope means you are arriving.** You do not need to be told when to stop; the hill tells you."

**Ask this:** "And what are the steps doing?"

*Hoped-for answer:* getting shorter — 3.6, then 1.44, then 0.576.

> "Getting shorter, **and nobody told them to.** The step is the slope times the stride, and the slope is dying, so the steps die with it. **The algorithm slows down automatically as it arrives**, and that is a free gift from one multiplication."

**Ask this, last:** "Your final `w` is 7.996068. What was hidden in the data?"

*Answer:* 8.

> "Eight. You found a number you were not told, from ten exam results, using two subtractions and a division, eight times. **That is machine learning. There is nothing else in it.**"

### What "finished" looks like

- Three columns on the board reading **2, 6, 10**, with `2 × x` written underneath in a student's handwriting.
- Each student's graph paper carrying **six decimal places** on at least one of the nudge calculations.
- An eight-row table ending at **7.996068**.
- Somebody having said out loud: *"the slope is getting smaller."*

### Variation — easier

**Cut part 1 to one point, `x = 3`, done by everybody together**, with you doing the two multiplications on the board and the class doing the subtraction and the division. **Objective 2 is complete.** Then just *tell* them 2 and 10 and ask what the pattern is — objective 3 survives as a pattern-spotting task instead of a measurement.

**Cut part 2 to four steps instead of eight**, and hand out the table with the `slope` column already filled in. Their job is only `0.3 × slope` and the subtraction. **Objective 4 is complete** — the sign and the step are the objective, not the slope-measuring.

**And use the shortcut, not the nudge, in part 2.** `2 × (w − 8)` at `w = 2` is `2 × (−6) = −12`. One multiplication instead of two six-decimal squarings.

### Variation — harder

1. **Guess before you measure.** They have `x × x → 2 × x` and `x × x × x → 3 × x × x`. **Ask them to predict the rule for `x × x × x × x` and then check it by nudging at x = 2.** (Prediction: `4 × x × x × x`, which at x = 2 is 32. The nudge at x = 2 with h = 0.001 gives 32.000008.) **Predict, measure, check is a perfectly good way to discover a rule.**
2. **Find the learning rate that just barely works** on the ten-student loss. They will find that 0.01 is fine, 0.026 slowly wanders off, and 0.03 explodes to a billion. **Then ask why the same 0.3 that worked perfectly on the one-student loss destroys the ten-student one.** (Because the ten-student valley is 38.5 times steeper — its slope at w = 2 is −462 instead of −12.) This is a genuinely deep question and a student who gets it has understood learning rates better than most tutorials explain them.
3. **The wobbly data.** Run `noisy.py` (in the Answer Key) and find that the best `w` is **7.99** and the best loss is **8.9106**, not 0. **Ask what the 8.91 is.** (The part of the exam marks that revision hours cannot explain. It is the floor of the data, and no amount of descent gets below it.) **A student who understands that a loss which stops falling is not a bug has saved themselves three weeks of confusion in Term 3.**
4. **The honest question:** *"our valley has one bottom. Does every valley?"* No. Squared error on a straight line always gives one bowl, which is why today worked so cleanly. A neural network's loss surface has many bottoms, and gradient descent finds *a* bottom rather than *the* bottom, and in practice that turns out to be mostly fine and nobody fully knows why. **Tell them that is genuinely an open question and that they have just asked a research-level one.**

---

## ❓ Questions Students Ask This Week

**"Is this real calculus?"**
**Yes. Completely.** The number a calculus class computes by applying a rule is the number you just got by nudging and dividing. A calculus course teaches you about twenty rules for getting there quickly without a calculator, plus the machinery for proving the rules are right. **You are skipping the rules and keeping the thing.** And from Week 20 a computer does the rules for you, so the nudge is what you will actually use — including in Week 19, where you will use it to check a piece of code that is far too complicated to trust.

**"Why nudge both ways instead of just forwards?"**
Because it is more accurate for the same work. Forwards only, at x = 3 with h = 0.001, gives **6.001**. Both ways gives **6.000**. The errors from the two sides cancel. **For the parabolas in this lesson the symmetric version is not merely more accurate, it is exact** — which is why Figure 12.2 can use a nudge of half a unit and still get 6.000 on the nose.

**"Why not make the nudge infinitely small?"**
Because a computer cannot. Look at the table: `h = 1e-12` gives **6.0005334035**, which is worse than `h = 0.001`. Subtracting two numbers that agree to fifteen digits throws away almost all your digits. **And that is exactly why calculus was invented** — it gets the answer for a nudge of literally zero, by reasoning instead of arithmetic. We are using 0.001 and checking, which is what every numerical library on earth does when it needs to verify something.

**"How do you know when to stop stepping?"**
**Watch the slope.** In our eight steps it went −12, −4.8, −1.92, −0.77, −0.31, −0.12, −0.05, −0.02. When it is small, you have arrived, because a small slope means flat ground and flat ground means the bottom. In practice people stop when the loss stops improving by more than some tiny amount, or after a fixed number of steps, whichever comes first. **In this course, mostly a fixed number, because it is simpler and it is honest.**

**"Where does the learning rate come from? Who picks 0.3?"**
A person picks it, by trying values. There is no formula. **And it depends on the shape of the hill, not on any principle** — 0.3 is perfect on the one-student loss and catastrophic on the ten-student one, because the second valley is 38.5 times steeper. The professional method is genuinely just: try 0.1; if the loss goes up, try 0.01; if it barely moves, try 1. **This is one of the places where machine learning is much less scientific than it looks, and it is fine to say so.**

**"What if the valley has two bottoms?"**
🤔 **Nobody fully agrees about this and it is one of the honest open questions in the field.** For today's problem — squared error, one straight line — the valley provably has exactly one bottom, so descent with a sensible learning rate finds it. For a neural network, the surface has an enormous number of bottoms, and gradient descent finds whichever one it happens to walk into. The classical worry was that this would be a disaster. **In practice it usually is not**, and the explanations offered are contested: some say most bottoms in very high dimensions are about equally good; some say the real obstacles are flat regions rather than wrong bottoms; some say the noise in mini-batch training shakes you out of bad ones. **All of those are partly true and none of them is a complete answer.** A student who asks this has asked a research question, and they should be told so.

**"Why square the errors instead of just ignoring the minus signs?"**
You could — that is a real loss function and it is called mean absolute error. Squaring has two advantages here: it punishes big misses much harder, which is usually what you want, and **its slope is much better behaved.** Absolute error has a corner at zero where the slope suddenly flips from −1 to +1 with nothing in between, which makes descent jumpy. Squared error's slope changes smoothly. **Choosing a loss is a real decision and Week 14 makes a different one, on purpose, for probabilities.**

**"We already knew the answer was 8. What was the point?"**
**That is exactly the point.** You test a method on a problem whose answer you know, so that when it says 7.996068 you can tell it worked. If we had started with real data we would have got a number and had no way of knowing whether it was right. **Every method in this course gets tested on a planted answer first** — the numpy network in Week 19 gets checked against a nudge, the PyTorch network in Week 23 gets checked against the numpy one. That habit is worth more than any single technique.

**"Does the loss always reach zero?"**
No, and ours only did because we planted a perfect line. On the wobbly version of the same ten students the best possible loss is **8.9106**, and no amount of stepping gets below it, because ten real students do not sit on a line. **A loss that stops falling above zero is not a failure. It is the floor of your data**, and confusing the two causes people to train models for three days for nothing.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **You say "derivative" in the first ten minutes.** | It is the word you know for the thing, and it slips out. | **This is the one unrecoverable mistake in the week.** Half the room will stop thinking and start trying to remember school. The folded paper in your pocket exists to stop you. If it slips out anyway: *"forget I said that, we are going to measure it first"*, and mean it. |
| Students think `2 × x` is a rule to memorise. | It looks like every other rule they have been given. | Go back to the three columns on the board. *"Where did that come from?"* **You measured it.** Then make them measure `x × x × x` and notice a different rule, so that "noticing rules" becomes the skill rather than "knowing rules". |
| The eight loss calculations eat the whole Concept segment. | Eighty subtractions and eighty squarings is a lot of arithmetic. | **Do `w = 6` together, then delegate one candidate per pair.** Four minutes, calculators mandatory. If you are still behind at minute 18, hand out the other six answers and move on — **the valley's shape is the objective, not the eighty squarings.** |
| The minus sign in the update rule confuses everybody. | It genuinely is confusing, once. | Do both walls, with real numbers, on the board — Figure 12.4. `2 − 0.3 × (−12) = 5.6` and `14 − 0.3 × (+12) = 10.4`. **Do not move on until a student explains it back to you.** |
| A student who has done calculus dismisses the whole lesson. | They have the rule and they think the rule is the point. | Give them harder variation 1 immediately: **predict the rule for `x⁴` and then check it by nudging.** Then ask them to explain, with the nudge, why the slope of `5 × x` is 5 everywhere. **A student who has only ever applied rules finds "prove it with arithmetic" genuinely novel.** |
| The nudge arithmetic comes out wrong because somebody rounded. | `3.001 × 3.001` is 9.006001 and a student who writes 9.006 gets a difference of 0.012 by luck, and at x = 5 the rounding breaks it. | **Insist on six decimal places, out loud, before they start.** It is on the activity instruction card for exactly this reason. |
| Everybody's descent table has a different final `w`. | One arithmetic slip early propagates through all eight rows. | **Check row 0 before anybody does row 1.** `slope −12`, `step −3.6`, `new w 5.6`. Everybody. Then release them. |
| The loss going up gets treated as "the model is learning". | It is going *somewhere* and things are changing. | **This is deliberate mistake two and the reason it is in the lesson.** Make the rule a chant: *"loss up, check the sign."* |
| It finishes at minute 55 because the class is quick. | It happens with a confident group. | Go to harder variation 3 — the wobbly data, best loss 8.9106 — and spend the last ten minutes on *"what is the 8.91?"* **It is one of the most valuable ten minutes available anywhere in the term.** |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the ten-student loss entirely. **Use one student and one student only** — 1 hour, 20 marks — so the loss is `(w − 8) × (w − 8)` and every number in the lesson is small.

**Cut:** `x × x × x`, `5 × x`, the nudge-size table, `np.linspace`, `np.argmin` and the plot. **Objectives 2, 3 and 4 need none of them.**

**Cut:** measuring the slope by nudging in part 2 of the activity. **Give them the shortcut `2 × (w − 8)`** and let the walk be the objective.

**Copy this exactly.** Hand it over on paper and let them change one number:

```python
# slope_small.py - how steep is x times x, right here?
def f(x):
    return x * x

x = 3.0                       # <-- CHANGE ONLY THIS NUMBER
h = 0.001

up = f(x + h)
down = f(x - h)
print("f(x + h) =", up)
print("f(x - h) =", down)
print("difference =", up - down)
print("divided by 2h =", (up - down) / (2 * h))
print("and 2 times x is", 2 * x)
```

Real output at `x = 3.0`:

```text
f(x + h) = 9.006001
f(x - h) = 8.994001
difference = 0.011999999999998678
divided by 2h = 5.999999999999339
and 2 times x is 6.0
```

> **⚠️ Watch out:** the last two numbers are **not tidy**, and that is deliberate — this version prints every digit the computer is holding instead of rounding to four decimals. The difference reads `0.011999999999998678` instead of a clean `0.012`, and the slope reads `5.999999999999339` instead of `6`. **Do not hide this and do not apologise for it.** Say: *"the computer's answer is five point nine nine nine nine nine nine nine nine nine nine nine — which is six, to eleven decimal places. The wobble is in how the computer stores 0.001, not in your maths."* Then point at their paper, where the same subtraction came out as exactly `0.012000`, and say: *"your hand is tidier than the computer here, and you are both right."* **That is a genuinely reassuring thing for a struggling student to hear**, and it is true. `slope.py` prints a clean `6.0000` only because it formats to four decimals with `%.4f`.

**The maths, with everything hard removed.** Do not say "slope", "derivative" or "gradient". Say:

> "How much does the answer change if I change the question a tiny bit?
>
> Change the question by a thousandth. See how much the answer moves. **That's it.** If the answer moved a lot, the curve is steep here. If it barely moved, the curve is flat here."

Then the sign, with two sentences and no formula:

> "**If the ground goes down to the right, go right. If the ground goes down to the left, go left.** The number tells you which. A negative number means go right."

### If the student is flying

1. **Predict, then measure.** They have `x × x → 2 × x` and `x × x × x → 3 × x × x`. **Predict the rule for `x⁴`, then check it by nudging at x = 2.** (Prediction `4 × x³` = 32; the nudge gives 32.000008.) Then `x⁵` at x = 2. (`5 × x⁴` = 80.) **Predict, measure, check is a perfectly good way to discover a rule.**
2. **Find the edge of stability.** On the ten-student loss, bisect between 0.026 (wanders off) and 0.03 (explodes) and find where the behaviour changes. Then ask **why** there is a hard edge rather than a gradual decline. (Each step multiplies the distance-to-the-answer by `1 − lr × 77`. When that multiplier is bigger than 1 in size, you diverge — which happens at `lr = 2 ÷ 77 = 0.02597`. **A student who derives that number has done something genuinely impressive.**)
3. **The wobbly data.** Run `noisy.py` from the Answer Key. Best `w` is 7.99, best loss **8.9106**. Ask what 8.91 is, and whether more steps would ever reduce it. (No. It is the part of the marks that hours cannot explain.)
4. **Two knobs.** Let `b` be unknown as well as `w`, so the model is `w × hours + b` and there are **two** slopes to measure. Ask them to nudge each knob separately, get two numbers, and step both. **They will have invented the gradient**, three weeks early, and Week 15 will be a victory lap. Do not push them to write the loop; the insight is the prize.
5. **The honest question:** *"we did 8 steps and got 7.996068. How many steps to get to 8 exactly?"* **Never.** Each step multiplies the gap by 0.4, and 0.4 to any power is not zero. Gradient descent gets arbitrarily close and never arrives. **Ask whether that matters.** (Almost never — 7.996068 predicts marks to within 0.04 — and noticing that "close enough" is a real engineering answer rather than a cop-out is worth a lot.)

### If the student won't engage today

Do the staircase and nothing else. **Two feet, one comparison, three steps, "which way is down".** Four minutes, no paper, no screen, and it is the entire big idea.

If they will do one written thing, make it **one nudge**:

```
3.001 × 3.001  =  9.006001
2.999 × 2.999  =  8.994001
                  --------
                  0.012000

0.012000 ÷ 0.002  =  6
```

**Five lines, one calculator, ninety seconds — and it is objective 2 complete.** That is the single most important calculation in Level 3 and it is five lines long. If nothing else happens today, that happening is enough.

If they will do nothing at all: ask them one question and let it sit. *"You are on a hill in thick fog and you want to get down. You are not allowed to look. What do you do?"* **Everybody has an answer to that, and their answer is gradient descent.**

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the nudge, on a point they have not done.** Say: *"`f(x) = x × x`. I have worked out that `f(4.001) = 16.008001` and `f(3.999) = 15.992001`. What is the slope at 4, and does the shortcut rule agree?"*

> **A good answer:** `16.008001 − 15.992001 = 0.016000`, then `0.016000 ÷ 0.002 = 8.000`, **and** `2 × 4 = 8`, so yes. A student who divides by 0.001 gets 16 — **ask them how far apart 4.001 and 3.999 are.** A student who cannot say whether the rule agrees has the arithmetic without objective 3.

**Check 2 — the sign, in the direction they did not practise.** Say: *"I am standing at `w = 12` and I measure the slope. It comes out **plus twenty**. My learning rate is 0.1. Where do I go next, and is that towards the answer or away from it?"*

> **A good answer:** `12 − 0.1 × 20 = 12 − 2 = 10`, so **left**, and since the answer is 8, that is **towards** it. A student who says 14 has added instead of subtracted — the most common slip and worth catching now. A student who gets 10 but cannot say whether it is towards or away has not connected the arithmetic to the picture; point at the valley on the wall.

**Check 3 — what the loss is, and what a flattening slope means.** Say: *"In our eight steps the slope went from minus twelve down to minus nought point nought two. What does that tell me, and how would I know if I had the learning rate wrong?"*

> **A good answer** says a shrinking slope means **the ground is flattening, so we are arriving at the bottom** — and that a wrong learning rate shows up as **the loss going up** (too big) or **barely moving** (too small). Accept "the loss stops changing" for arrival. **The unacceptable answer is "the model is getting better" with nothing about flatness or the bottom** — that is a description, not an understanding. Ask: *"and what is the slope at the very bottom?"* (Zero.)

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot compute a loss from a guess. Thinks `fit()` is still magic. Cannot say what the nudge is for. |
| **2 — Emerging** | Computes the loss for a given `w` with the table in front of them. Does one nudge correctly when told the recipe. Gets the sign of the step wrong about half the time. |
| **3 — Secure** | Computes eight losses and sketches the valley unaided. Nudges at any point and gets the right slope to three decimals. Confirms `2 × x` from their own three measurements. Steps in the right direction from either wall. |
| **4 — Fluent** | Says without prompting that a shrinking slope means arrival. Explains why the minus sign works in both directions. Notices that the steps get shorter on their own. Predicts the sign of the slope from which side of the valley they are on, before computing it. |
| **5 — Extending** | Predicts the rule for `x⁴` before measuring it, and checks. Works out why `lr = 0.3` destroys the ten-student loss but not the one-student one. Asks whether every valley has one bottom, or whether you ever actually reach 8. Wonders what happens with two knobs — which is Week 15 arriving early. |

---

## 📤 Homework to Assign

**Say this, word for word:**

> "Two pages, about an hour, and **all of it is by hand.** There is code at the end but the code is only there to mark you.
>
> **Page 12.1 — nine slopes.** Three functions, three points each. `x × x`, then `x × x × x`, then `5 × x`, at `x = 1`, `x = 3` and `x = 5`. **Nine nudges, all by hand, six decimal places on every multiplication.** And beside each one, write the shortcut rule's answer and put a **tick or a cross.**
>
> I want to see crosses. A page of nine ticks with no working is a page I do not believe.
>
> **Page 12.2 — six steps downhill on a new valley.** The loss is `(w − 4) × (w − 4)`. Start at `w = 0`. Learning rate `0.3`. Six rows, tabulated: `w`, the loss, the slope, `0.3 × slope`, and the new `w`. **Then compare your final `w` with 4** and write one sentence saying how close you got and why you did not land exactly on it.
>
> **Page 12.3 — check yourself with code.** Type the three files, run them, and tick off every number that matches your handwriting. If one does not match, **find out which of the two of you is wrong before you write anything else.**
>
> **And the last thing, which is one sentence.** In your own words, with no symbols at all: **what is a derivative?** If your sentence contains the word 'derivative', start again."

| Page | What it is | Time |
|---|---|---|
| 12.1 | Nine numeric slopes by hand, each with the shortcut rule and a tick or cross | 25 min |
| 12.2 | Six steps of `w ← w − 0.3 × slope` on `(w − 4)²`, tabulated, compared with 4 | 15 min |
| 12.3 | Type and run `valley.py`, `slope.py`, `walk.py`; tick every matching number | 15 min |
| 12.4 | The eight losses on the ten-student data, checked against the code | 5 min |
| 12.5 | One sentence: what is a derivative, no symbols, and not using the word | 5 min |
| 12.6 | Vocabulary (7 terms) and the Bug Log's two silent bugs | 5 min |

---

## 🔑 Answer Key

### Page 12.1 — Nine slopes by hand

**`h = 0.001`, so every division is by `0.002`.**

**Function one: `f(x) = x × x`. The rule is `2 × x`.**

| x | `f(x + h)` | `f(x − h)` | difference | `÷ 0.002` | rule `2 × x` | |
|---|---|---|---|---|---|---|
| 1 | 1.002001 | 0.998001 | 0.004000 | **2.0000** | 2 | ✅ |
| 3 | 9.006001 | 8.994001 | 0.012000 | **6.0000** | 6 | ✅ |
| 5 | 25.010001 | 24.990001 | 0.020000 | **10.0000** | 10 | ✅ |

**Function two: `g(x) = x × x × x`. The rule is `3 × x × x`.**

| x | `g(x + h)` | `g(x − h)` | difference | `÷ 0.002` | rule `3 × x²` | |
|---|---|---|---|---|---|---|
| 1 | 1.003003 | 0.997003 | 0.006000 | **3.000001** | 3 | ✅ (out by a millionth) |
| 3 | 27.027009 | 26.973009 | 0.054000 | **27.000001** | 27 | ✅ |
| 5 | 125.075015 | 124.925015 | 0.150000 | **75.000001** | 75 | ✅ |

**Function three: `k(x) = 5 × x`. The rule is `5`.**

| x | `k(x + h)` | `k(x − h)` | difference | `÷ 0.002` | rule | |
|---|---|---|---|---|---|---|
| 1 | 5.005 | 4.995 | 0.010 | **5.000000** | 5 | ✅ |
| 3 | 15.005 | 14.995 | 0.010 | **5.000000** | 5 | ✅ |
| 5 | 25.005 | 24.995 | 0.010 | **5.000000** | 5 | ✅ |

**Nine for nine.** The complete `slope.py` and its real output are printed in full in the **🧰 Prep Checklist** above.

**Three things to say about this page:**

1. **`x × x × x` comes out 3.000001, not 3.000000.** That is **correct and it is not a mistake.** The nudge is not infinitely small, so the measurement is off in the sixth decimal. **A student who wrote 3.000001 and put a tick has understood it. A student who wrote 3.000000 has rounded, and should be gently caught.**
2. **`5 × x` has the same slope everywhere.** Obvious once you see it — a straight line has one steepness. **But it is worth asking about**, because it is the first hint that some slopes depend on where you are and some do not.
3. **The pattern across the three functions.** `x²` → `2x`. `x³` → `3x²`. If a student volunteers that `x⁴` should give `4x³`, **they have discovered the power rule from three data points** and you should say so out loud. The check: at x = 2, `4 × 2³ = 32`, and the nudge gives **32.000008**.

**Common wrong answers:**

- **Dividing by 0.001.** Gives double: 4, 12, 20. **Ask: how far apart are 3.001 and 2.999?**
- **Rounding to three decimals.** `3.001 × 3.001 ≈ 9.006` and `2.999 × 2.999 ≈ 8.994` gives a difference of 0.012, which is right by luck at x = 3 and **wrong at x = 5**, where you need the fourth, fifth and sixth decimals to see 0.020000 rather than 0.020. **Six decimals, every time.**
- **Forwards-only nudges.** `(f(3.001) − f(3)) ÷ 0.001 = 6.001`. Not wrong, just less accurate — **worth full marks if they say so.**

### Page 12.2 — Six steps downhill on `(w − 4)²`

Loss `(w − 4) × (w − 4)`, slope `2 × (w − 4)`, learning rate `0.3`, starting at `w = 0`.

| step | w | loss | slope | `0.3 × slope` | new w |
|---|---|---|---|---|---|
| 0 | 0.000000 | 16.000000 | −8.000000 | −2.400000 | **2.400000** |
| 1 | 2.400000 | 2.560000 | −3.200000 | −0.960000 | **3.360000** |
| 2 | 3.360000 | 0.409600 | −1.280000 | −0.384000 | **3.744000** |
| 3 | 3.744000 | 0.065536 | −0.512000 | −0.153600 | **3.897600** |
| 4 | 3.897600 | 0.010486 | −0.204800 | −0.061440 | **3.959040** |
| 5 | 3.959040 | 0.001678 | −0.081920 | −0.024576 | **3.983616** |

**After six steps, `w = 3.983616`. The target was 4.**

**Machine check** — real output from `walk.py`:

```text
--- homework shape: (w - 4) squared, lr 0.3, six steps from w = 0 ---
step 0  w 0.000000  loss 16.000000  slope -8.000000  ->  2.400000
step 1  w 2.400000  loss 2.560000  slope -3.200000  ->  3.360000
step 2  w 3.360000  loss 0.409600  slope -1.280000  ->  3.744000
step 3  w 3.744000  loss 0.065536  slope -0.512000  ->  3.897600
step 4  w 3.897600  loss 0.010486  slope -0.204800  ->  3.959040
step 5  w 3.959040  loss 0.001678  slope -0.081920  ->  3.983616
after six steps w = 3.983616, target 4
```

**The sentence — full marks looks like this:**

> "I got to 3.983616, which is 0.016 short of 4. **I did not land exactly on it because each step is proportional to the slope, and the slope gets smaller as I get closer**, so the steps get smaller too — 2.4, then 0.96, then 0.384. The gap gets multiplied by 0.4 every step, and multiplying by 0.4 never actually reaches zero. **More steps would get me closer and no number of steps would get me there.**"

**Accept also:** "the slope at 4 is exactly 0, so once I got there I would stop moving — but I can only get there by taking a step of exactly the right size, and my steps are always a bit too small."

**Send back:** "I made a rounding error." **They did not.** The 0.016 is not an error, it is how the algorithm works, and that distinction is the point of the question.

**Common wrong answers:**

- **Step 0 giving `w = −2.4`.** They added instead of subtracting. `0 − 0.3 × (−8) = 0 + 2.4`. **Point at the two walls on the board.**
- **The gap not shrinking by a constant factor.** One arithmetic slip early. **Check: is `w − 4` being multiplied by 0.4 each row?** −4, −1.6, −0.64, −0.256, −0.10240, −0.040960, −0.016384. If one row breaks the pattern, that is the row.
- **Six identical steps of 2.4.** They used the slope from step 0 for all six rows. **The slope has to be re-measured at the new `w` every single time.** This is the most instructive mistake on the page.

### Page 12.3 — The three files, checked

All three complete files and their real outputs are printed in full in the **🧰 Prep Checklist** above. Check the student's output on these five numbers:

| Must be exactly | If it is not |
|---|---|
| `mean    154.0` | The 12 has been left out of `w * hours + 12`, or the `.mean()` is a `.sum()` (which gives 1540). |
| `np.argmin(losses) = 4` | `np.linspace(0, 14, 8)` has different arguments. |
| `6.0000` at `x = 3.0` in `slope.py` | Brackets missing round `2 * h`. You will see `0.000006`. |
| `after eight steps w = 7.996068` | Either the sign is wrong (`w` runs away negative) or a slope was reused instead of re-measured. |
| `after six steps w = 3.983616` | Same two suspects. |

### Page 12.4 — The eight losses on the ten-student data

Every error is `(w − 8) × hours`, because the predicted mark is `w × hours + 12` and the real mark is `8 × hours + 12`, so the 12s cancel and what is left is the gap in `w`, multiplied by the hours.

| w | the ten errors | sum of squares | loss (÷ 10) |
|---|---|---|---|
| 0 | −8, −16, −24, … −80 | 24640 | **2464.00** |
| 2 | −6, −12, −18, … −60 | 13860 | **1386.00** |
| 4 | −4, −8, −12, … −40 | 6160 | **616.00** |
| 6 | −2, −4, −6, … −20 | 1540 | **154.00** |
| **8** | 0, 0, 0, … 0 | **0** | **0.00** |
| 10 | +2, +4, +6, … +20 | 1540 | **154.00** |
| 12 | +4, +8, +12, … +40 | 6160 | **616.00** |
| 14 | +6, +12, +18, … +60 | 13860 | **1386.00** |

**A shortcut worth pointing out if a student finds the eighty squarings tedious.** The squares of 1 to 10 add up to **385**, and every row's errors are just `(w − 8)` times those ten hour values — so the sum of squares is `(w − 8)² × 385` every single time. At `w = 6`: `4 × 385 = 1540`, and `1540 ÷ 10 = 154`. **One multiplication instead of ten squarings**, and it also explains why the slope in `slope.py` came out as exactly `77 × (w − 8)`.

**Two things to check they noticed:**

1. **The valley is symmetric.** `w = 6` and `w = 10` both give 154; `w = 4` and `w = 12` both give 616; `w = 2` and `w = 14` both give 1386. **Because the errors get squared, so a miss of −2 and a miss of +2 cost the same.**
2. **The loss at `w = 8` is exactly zero**, which only happens because a perfect line was planted in the data. **On real data it never happens.**

**And if they ran the wobbly version** (`noisy.py`, in the block below), the real output is:

```python
"""noisy.py - the same ten students, but real ones.  Week 12."""
import numpy as np

hours = np.arange(1, 11)
marks_clean = 8 * hours + 12
print("np.arange version :", hours, marks_clean)

rng = np.random.default_rng(0)
wobble = np.round(rng.normal(0, 4, 10), 1)
marks = marks_clean + wobble
print("wobble            :", wobble)
print("marks with wobble :", marks)

def loss(w):
    return (((w * hours + 12) - marks) ** 2).mean()

grid = np.linspace(0, 14, 8)
print()
print("   w      loss")
for w in grid:
    print("%5.1f  %9.4f" % (w, loss(w)))
print("np.argmin ->", np.argmin([loss(w) for w in grid]),
      " best of the eight w =", grid[np.argmin([loss(w) for w in grid])])

fine = np.linspace(7.0, 9.0, 201)
fl = np.array([loss(w) for w in fine])
print("finer search of 201 values between 7 and 9:")
print("best w = %.4f   loss %.4f" % (fine[np.argmin(fl)], fl.min()))
print("the exact answer, by algebra: %.6f"
      % ((hours * (marks - 12)).sum() / (hours * hours).sum()))
```

```text
np.arange version : [ 1  2  3  4  5  6  7  8  9 10] [20 28 36 44 52 60 68 76 84 92]
wobble            : [ 0.5 -0.5  2.6  0.4 -2.1  1.4  5.2  3.8 -2.8 -5.1]
marks with wobble : [20.5 27.5 38.6 44.4 49.9 61.4 73.2 79.8 81.2 86.9]

   w      loss
  0.0  2468.7520
  2.0  1391.7920
  4.0   622.8320
  6.0   161.8720
  8.0     8.9120
 10.0   163.9520
 12.0   626.9920
 14.0  1398.0320
np.argmin -> 4  best of the eight w = 8.0

finer search of 201 values between 7 and 9:
best w = 7.9900   loss 8.9106
```

The last line of the file also prints `the exact answer, by algebra: 7.993247`.

**The point of this block, and it is worth ten minutes if you have them:** the best achievable loss is **8.9106, not 0.** No amount of descent gets below it. **That 8.91 is the part of these ten students' marks that revision hours cannot explain** — mood, sleep, luck, whether they had breakfast. **A loss that stops falling above zero is not a bug; it is the floor of your data.**

### Page 12.5 — One sentence: what is a derivative?

**Full marks looks like any of these.** The test is that it describes a *measurement*, contains no symbols, and does not use the word.

> "How much the answer changes when you change the question by a tiny bit, divided by how tiny the bit was."

> "How steep a curve is at exactly the spot you are standing on, worked out by taking one small step each way and seeing how far up or down you went."

> "It is a rise over a run where the run is nearly nothing."

> "The number that tells you which way is downhill and how steeply, right here."

**Send back:**

- Anything containing `dy/dx`, `f'(x)`, `lim`, or the word "derivative".
- **"The rate of change."** Technically true and it is a phrase they have memorised, not a sentence they mean. Ask: *"the rate of change of what, with respect to what, and how would you measure it with a calculator?"*
- **"2x."** That is the answer for one particular curve, not what the thing is.

### Page 12.6 — Vocabulary and Bug Log

> **Loss** — one number saying how wrong the model is right now. Big is bad, zero is perfect. Ours is the average of the ten squared errors.

> **Loss surface** — the shape you get by plotting the loss against the value of a weight. One knob makes a curve; two make a landscape; a hundred thousand make something nobody can draw.

> **Slope at a point** — how steeply the curve is climbing or falling exactly where you are standing.

> **Derivative** — the slope at a point, written down as a rule that works at every point. For `x × x` it is `2 × x`, and we found that by measuring, not by being told.

> **Numerical gradient** — a slope measured by nudging the input a tiny bit each way and dividing. Slow, needs no cleverness, and honest while the nudge is sensible. We will use it in Week 19 to check something we cannot check any other way.

> **Learning rate** — how big a step you take downhill. Your stride length. 0.3 works on one valley and destroys another.

> **Gradient descent** — measure the slope, step the opposite way, repeat. This is what sits inside `fit()` for logistic regression and for every neural network.

**Bug Log — both entries are silent.**

**Entry one.**
Message: *none.* Symptom: the slope printed `0.000006` when I had 6 on paper.
Meaning: `/ 2 * h` divides by 2 and then multiplies by h, because Python works left to right. I meant *divide by two lots of h.*
Fix: brackets — `/ (2 * h)`.
The rule I am keeping: **know roughly what the answer should be before you look at the screen. An answer a million times out is obvious the moment you have an expectation.**

**Entry two.**
Message: *none.* Symptom: the loss went 92, 236, 604, 1546, 3958 — **up**, and `w` ran off to −55.
Meaning: I wrote `w = w + lr * s`. The slope points uphill, so adding it walks uphill.
Fix: `w = w - lr * s`.
The rule I am keeping: **if the loss is going up, check the sign first and the learning rate second.**

### Answers to every question posed in the lesson

**Hook — "what can you still do in the fog?"** Feel the ground under your feet: compare the height just in front with the height just behind.

**Hook — "left foot forward: higher or lower?"** Lower. So forwards is downhill.

**Concept step 1 — "what is an extra hour worth, and what does nothing get?"** 8 marks an hour, and 12 for nothing. `marks = 8 × hours + 12`.

**Concept step 1 — "why square the errors?"** So the negatives do not cancel out, and so a big miss hurts more than a small one. Without squaring, the ten errors at `w = 6` add to −110, and a model that was wrong in both directions could add to zero and look perfect.

**Concept step 1 — "add the squares and divide by ten."** `1540 ÷ 10 = 154`.

**Concept step 1 — "what shape is that?"** A valley, symmetric about `w = 8`.

**Concept step 1 — "why do `w = 6` and `w = 10` give the same loss?"** Both are 2 away from the answer, and squaring throws the sign away.

**Concept step 1 — "why is eight guesses not the end of the lesson?"** Because 8 happened to be one of the guesses, and because with two knobs you need 64 guesses, with three 512, and with a hundred thousand knobs the number has no name.

**Concept step 2 — "how much did the answer change?"** `9.006001 − 8.994001 = 0.012000`.

**Concept step 2 — "how far did we move?"** `3.001 − 2.999 = 0.002`.

**Concept step 2 — "so how steep is it?"** `0.012000 ÷ 0.002 = 6.000`.

**Concept step 2 — "anybody?"** 2, 6 and 10 are `2 × 1`, `2 × 3` and `2 × 5`. The slope of `x × x` is `2 × x`.

**Concept step 3 — "slope is negative twelve. Which way?"** Right. `2 − 0.3 × (−12) = 5.6`.

**Concept step 3 — "at `w = 14` with slope +12?"** `14 − 0.3 × (+12) = 10.4`. Left. Same rule.

**Live-code step 1 — "what will the `w = 6` row say?"** 154.

**Live-code step 1 — "`argmin` printed 4 but the best `w` is 8?"** `argmin` gives the **position** of the smallest value, counting from zero. `candidates[4]` is 8.0. `np.min` would give the value 0.00.

**Live-code step 2 — "was that an error?"** No. `0.000006` instead of `6.000000` — a factor of a million, silently.

**Live-code step 2 — "how far out is that?"** A million.

**Live-code step 3 — "3.000001 or 3? Which is right?"** The rule, 3. The nudge is not infinitely small so the measurement is off by a millionth, and nobody has ever cared about the sixth decimal of a slope.

**Live-code step 3 — "smaller nudge, better answer: true or false?"** **False.** `h = 1e-12` gives 6.0005334035, worse than `h = 0.001`. Subtracting two almost-identical numbers throws digits away.

**Live-code step 3b — "read me the loss column."** 92.16, 235.93, 603.98, 1546.19, 3958.24 — going **up**, fast, because a plus was used instead of a minus.

**Activity part 2 — "what is the `w` column doing?"** Creeping up on 8 without overshooting.

**Activity part 2 — "what is the slope column doing?"** Shrinking: −12 to −0.02. **A flattening slope means you are arriving.**

**Activity part 2 — "what are the steps doing?"** Getting shorter — 3.6, 1.44, 0.576 — automatically, because the step is the slope times the stride and the slope is dying.

**Activity part 2 — "your final `w` is 7.996068. What was hidden in the data?"** 8.

**Harder variation 1 — "what is the rule for `x⁴`?"** `4 × x × x × x`. At `x = 2` the rule gives 32 and the nudge gives 32.000008.

**Harder variation 2 — "why does 0.3 destroy the ten-student loss?"** Because that valley is 38.5 times steeper: its slope at `w = 2` is −462 instead of −12. **A stride that suits one hillside throws you off another.** The edge of stability is at `lr = 2 ÷ 77 = 0.02597`, which is why 0.026 wanders and 0.03 explodes.

**Harder variation 3 — "what is the 8.91?"** The part of these ten students' marks that revision hours cannot explain. It is the floor of the data, and no amount of descent gets below it.

**Harder variation 4 / flying 5 — "how many steps to reach 8 exactly?"** Never. Each step multiplies the gap by 0.4, and 0.4 to any power is not zero. **Gradient descent gets arbitrarily close and never arrives, and that is almost always fine.**

---

## 🔮 Next Week Preview

Next week has a problem that today's model cannot solve, and it is a small, obvious one. Today's model answered *"how many marks?"* and the answer could be 20 or 92 or, if you gave it a silly `w`, 4,000. **Next week the question is "is this pizza order going to be late?", and the answer has to be a chance — a number between 0 and 1, never 1.4, never minus 3.** So the class builds a squasher: something that takes any number at all, from minus a million to plus a million, and folds it into the gap between 0 and 1. The maths is one new button on the calculator — `e` to the power of minus something — evaluated by hand for `z = −2`, `0`, `1.4` and `3`, and then those four points get plotted and **the S-curve appears out of four dots.** After that, Week 14 asks how wrong a *probability* can be, which turns out to need a different loss from today's squared error, and Week 15 puts all three together and runs the descent loop on a real classifier from scratch. **Today's arithmetic does not change once between here and Week 27.** Nudge, subtract, divide, read the sign, step. Everything after this is that loop with more knobs.

**To prep early:** three things. **One — check your calculator has an `e^x` button**, or find out how your phone does it (on iOS, turn the calculator sideways). You will need `e^2`, `e^0`, `e^−1.4` and `e^−3` and it is embarrassing to discover at minute 12 that you cannot get them. **Two — do not wipe the valley or the three slopes.** Week 13's squasher gets its own curve drawn on the same wall, and in Week 14 you will point back at today's `2, 6, 10` when the same nudge gets used on a curve nobody can guess the rule for. **Three — keep every student's eight-step descent table.** In Week 21, PyTorch will run this exact loop in five lines and print the same numbers, and the students who still have their handwriting from Week 12 get to hold the two side by side. That is the best moment in Term 2 and it costs you one folder.
