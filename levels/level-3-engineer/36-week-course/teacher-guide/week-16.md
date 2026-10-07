# Week 16 — One Neuron, By Hand

[⬅ Week 15](week-15.md) · [Course Home](../README.md) · [Week 17 ➡](week-17.md) · [Student Guide](../student-guide/week-16.md) · [Workbook](../workbook/week-16.md)

---

## 📋 At a Glance

This table is the lesson in one view: what is taught, what you need to have ready, and what the code costs.

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the first time the word *neuron* is allowed in the room, and it turns out to be three things they can already do |
| **Big idea** | A **neuron** is three things you already do: multiply each input by a weight, add them up with a bias, then squash. Stacking them is only interesting *because* of the squash. |
| **New vocabulary** | neuron / unit · pre-activation `z` · activation `a` · ReLU · tanh · layer · hidden layer · MLP |
| **New maths** | **the shape of a grid of numbers** — rows × columns, written `(3, 2)`, counted off a printout, and established as the first thing you print when anything is confusing |
| **New syntax** | `np.maximum(0, z)` · `np.tanh(z)` · `arr.reshape(r, c)` · `arr.T` |
| **Dataset** | Hand-typed 3-input rows and small 3×2 grids. Then, in the last five minutes only, a **first look** at `make_moons(random_state=0)` — 400 points, ships inside scikit-learn, no download. |
| **Materials** | **Six index cards per group**, large, written in thick pen: three input cards, three weight cards, one bias card (see 🎲) · the printed workbook (`workbook/week-16.md`, every section; the homework uses M2 and Build It, see 📤) · the Bug Log · a calculator per student that has an `e^x` key · a wide clear space on the board for the four-row table |
| **Tech needed** | Laptop with Python 3, numpy, matplotlib, scikit-learn. **No PyTorch this week** — that is Week 20. No internet, no downloads. |
| **Prep time** | 20 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | Every file today runs in **under 2 seconds**. Nothing trains. The `make_moons` scatter takes about 1 second including the plot. |

> **⚠️ Watch out:** the temptation this week is to draw a network with twenty circles and forty lines on the board in the first five minutes. **Don't.** Today there is **one** neuron and it has **three** inputs. If the student cannot compute one neuron's output on paper for three different squashes, a picture of twenty of them is decoration. The twenty-circle drawing is Week 19's job and it will land properly then.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compute a single neuron's output by hand** from three inputs, three weights and a bias, for **ReLU, sigmoid and tanh** — and get the same three numbers numpy gets.
2. **State the shape of an array before running anything**, and be right eight times out of eight.
3. **Prove on paper, in three lines, that two layers with no squash between them collapse into one straight line** — and give the numbers for one row that show it.
4. **Explain why ReLU is the default hidden activation**, using the slope of sigmoid as the contrast.

Observable evidence: a four-row table on the board with `z`, ReLU, sigmoid and tanh filled in by hand and then confirmed on screen; three lines of substitution ending in `out = 1.1x₁ + 0.4x₂ + 0.3`; eight shape predictions written in pen *before* anything ran; and a sentence naming the number `0.25` as the reason ReLU won.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

There is **one new mathematical idea** this week and it is not calculus. It is **the shape of a grid of numbers**. That is genuinely all. Everything else today is multiplication and addition on numbers small enough to check with a calculator. Twenty minutes with this section is enough; if you only have eight, read §2 and §5.

### 1. What a neuron actually is, in one paragraph with no jargon

> **neuron** (also called a **unit**) — a tiny machine that takes several numbers in, multiplies each one by its own weight, adds them all up, adds one extra number called the bias, and then passes the total through a squashing function.

That is it. Three steps: **multiply, add, squash.** The student has done the first two since Week 15 — a weighted sum is what `(X * w).sum(axis=1)` computed. **The only new part is the squash.**

The two halves have names, and both names are worth using from today because every error message and every book uses them:

> **pre-activation** (written `z`) — the number you get *before* squashing. It is the weighted sum plus the bias, and it can be any number at all: −40, 0, 6,000.

> **activation** (written `a`) — the number you get *after* squashing. It is the neuron's actual output, the thing it passes on.

🍕 **The analogy, and it carries the whole lesson.** A neuron is one judge on a talent-show panel with a very simple brain. She scores each act by weighing three things: **singing** (weight `0.4`), **dancing** (weight `−0.7` — she hates dancing), and **stage presence** (weight `1.2`). She is also permanently grumpy, so she subtracts `0.5` from everything before she says anything. That `−0.5` is the **bias**.

Her internal grumbling is `z`. Then she has to turn that grumbling into a public verdict, and *how* she does that is her **activation function**. If she gives a thumbs up worth exactly what she felt when she felt good, and stays silent when she felt bad, she is a **ReLU** judge.

**The bias is what lets a neuron be picky.** With `b = −0.5`, an act has to earn at least `+0.5` from the three features before the judge says anything at all. Without a bias, the threshold is stuck at exactly zero for ever. That sentence is worth saying out loud — students routinely think the bias is a decoration.

### 2. The full arithmetic, done four times, before any code

**The neuron for the whole lesson.** Weights `w = [0.4, −0.7, 1.2]`, bias `b = −0.5`. Write these on the board and leave them there.

> **🔢 The maths, slowly:** row one is `x = [2.0, 1.0, 0.5]`. Multiply each input by its own weight, in order:
>
> ```text
> 2.0 × 0.4    = 0.8
> 1.0 × (−0.7) = −0.7
> 0.5 × 1.2    = 0.6
> the bias     = −0.5
> ```
>
> Now add the four of them up, left to right, saying it aloud: **`0.8 − 0.7 = 0.1`**, then **`0.1 + 0.6 = 0.7`**, then **`0.7 − 0.5 = 0.20`**.
>
> **`z = 0.20`.** That is the pre-activation, and it is four multiplications and three additions. Nothing else happened.

Now the three squashes, on that one number:

| Squash | What it does, in words | On `z = 0.20` | The arithmetic |
|---|---|---|---|
| **ReLU** | "if it is negative, say zero; otherwise repeat it" | **0.200** | `0.20` is positive, so it comes straight through |
| **sigmoid** | "squash it into the range 0 to 1" | **0.550** | `e^(−0.20) = 0.818731`; `1 ÷ (1 + 0.818731) = 1 ÷ 1.818731 = 0.549834` |
| **tanh** | "squash it into the range −1 to +1" | **0.197** | the calculator's `tanh` key: `tanh(0.20) = 0.197375` |

Do the second row on the board with them, because it is the interesting one. `x = [−1.0, 2.0, 0.0]`:

```text
−1.0 × 0.4    = −0.4
 2.0 × (−0.7) = −1.4
 0.0 × 1.2    =  0.0
 the bias      = −0.5
                 -----
z              = −2.30
```

| Squash | On `z = −2.30` | Why |
|---|---|---|
| **ReLU** | **0.000** | negative, so it says nothing at all |
| **sigmoid** | **0.091** | `e^(2.30) = 9.974182`; `1 ÷ 10.974182 = 0.091123` |
| **tanh** | **−0.980** | the only one of the three that can hand back a negative number |

![One neuron: multiply, add, squash](../figures/fig-w16-1-neuron-weighted-inputs-into-activation.svg)
*Figure 16.1 — One neuron: multiply, add, squash. `0.8 − 0.7 + 0.6 − 0.5 = 0.20`, and ReLU passes it through unchanged.*

**Two more rows finish the table, and they are the two you will run in class:** `x = [0, 0, 1]` gives `z = 1.2 − 0.5 = 0.70`, and `x = [1, 1, 1]` gives `z = 0.4 − 0.7 + 1.2 − 0.5 = 0.40`.

![Three squashes, on the same two numbers](../figures/fig-w16-2-relu-sigmoid-tanh-side-by-side.svg)
*Figure 16.2 — Three squashes, on the same two numbers. Only tanh returns a negative number: `−0.980`.*

### 3. The one new maths idea: the shape of a grid of numbers

> **shape** — how many rows and how many columns a grid of numbers has, written as two numbers in brackets: **rows first, columns second.**

A grid with three rows and two columns has shape `(3, 2)`. Say it out loud as **"three by two"**.

That is the entire new idea. What makes it worth a section is this: **from today until the end of the year, the shape is the first thing you print when anything is confusing.** Not the values. The shape. A large share of the errors from here to Week 27 are shape errors, and every single one of them is diagnosed by printing two numbers.

**Count them off a real printout with your finger.** Here is a grid of six numbers:

```text
[[1 2]
 [3 4]
 [5 6]]
```

Count the rows going **down**: `1 2` is one, `3 4` is two, `5 6` is three. **Three rows.** Now count the numbers going **across** any one row: `1`, `2`. **Two columns.** Shape `(3, 2)`. The brackets tell you the same thing if you look: there are three inner `[...]` groups, and two numbers inside each.

Three things you can do to a shape, and all three are today's syntax:

| Code | What it does | Shape before | Shape after |
|---|---|---|---|
| `G.T` | flip the grid on its diagonal — rows become columns | `(3, 2)` | `(2, 3)` |
| `G.reshape(2, 3)` | keep the same six numbers, re-lay them out in a new grid | `(3, 2)` | `(2, 3)` |
| `np.maximum(0, G)` | squash every number, one at a time | `(3, 2)` | `(3, 2)` — unchanged |

**`G.T` and `G.reshape(2, 3)` give the same *shape* and different *numbers*, and this is the misconception of the week.** Look:

```text
G       = [[1 2]      G.T             = [[1 3 5]      G.reshape(2, 3) = [[1 2 3]
           [3 4]                        [2 4 6]]                        [4 5 6]]
           [5 6]]
```

Both answers are `(2, 3)`. But `G.T` reads *down the columns* of the original, and `G.reshape` reads *along the rows*. **Transpose rearranges; reshape just re-brackets.** The check is the sentence: `3 × 2 = 6` and `2 × 3 = 6`, so both hold the same six numbers — reshape can only ever produce a shape whose two numbers multiply to the same total.

![The same six numbers, three shapes](../figures/fig-w16-3-grid-with-its-shape-labelled.svg)
*Figure 16.3 — The same six numbers, three shapes. `3 × 2 = 6` and `2 × 3 = 6`, so both grids hold the same six numbers.*

**The one gotcha that will trip somebody today, and it is worth knowing before class.** A *flat* list of numbers has a shape with only one number in it, and a comma with nothing after it:

```python
a = np.array([1.0, 2.0, 3.0])
print(a.shape)      # (3,)
print(a.T.shape)    # (3,) -- transposing it does NOTHING
```

`(3,)` means "three numbers, no rows and columns at all". **Transposing a flat list has no effect**, because there is nothing to flip. If a student needs a column, they have to make it two-dimensional first: `a.reshape(1, 3).T` gives `(3, 1)`. That trailing comma in `(3,)` is not a typo and it is not a mistake in the printout. It is Python's way of saying "this is a shape with exactly one number in it".

You will also want the word **axis** once, because next week's code uses it and Week 19 leans on it:

> **axis 0** goes **down the rows**. **axis 1** goes **across the columns**. Rows first, columns second — exactly the same order as the shape.

### 4. Layers, hidden layers, and MLP — three words, defined and then left alone

Three pieces of vocabulary the student needs to have *heard* today, and will *use* next week:

> **layer** — a row of neurons that all see the same inputs and each have their own weights and bias.

> **hidden layer** — a layer whose outputs you never look at directly. They exist only to feed the next layer. "Hidden" means hidden from you, not mysterious.

> **MLP** (multi-layer perceptron) — inputs, then one or more hidden layers, then an output layer, with every neuron connected to every neuron in the next layer. It is the plainest kind of neural network and it is what the class builds in Week 19.

**Do not draw a big MLP today.** Say the three words, point at the two-layer example in §5 as the smallest possible one, and move on. If you spend ten minutes on architecture, you lose the ten minutes you need for the collapse proof, which is the actual point of the lesson.

### 5. The heart of the lesson: why the squash is not optional

Here is the thing to get right, because it is the reason neural networks exist at all rather than being a slower way to draw a straight line.

**Take two layers with no squash between them.** One hidden layer of two units, then one output. Weights chosen so the arithmetic is easy:

```text
h1 =  0.5·x₁ + 0.8·x₂ + 0.1
h2 = −0.3·x₁ + 0.2·x₂ + 0.05

out = 1.0·h1 − 2.0·h2 + 0.3
```

> **🔢 The maths, slowly.** Substitute the first two lines into the third. Take it one bracket at a time and do not skip a step.
>
> ```text
> out = 1.0 × (0.5x₁ + 0.8x₂ + 0.1) − 2.0 × (−0.3x₁ + 0.2x₂ + 0.05) + 0.3
> ```
>
> Multiply out the first bracket: `0.5x₁ + 0.8x₂ + 0.1`.
>
> Multiply out the second bracket, remembering the `−2.0` flips every sign:
> `−2.0 × (−0.3x₁) = +0.6x₁`, `−2.0 × (0.2x₂) = −0.4x₂`, `−2.0 × 0.05 = −0.1`.
>
> Now collect. The `x₁` terms: `0.5 + 0.6 = 1.1`. The `x₂` terms: `0.8 − 0.4 = 0.4`. The plain numbers: `0.1 − 0.1 + 0.3 = 0.3`.
>
> ```text
> out = 1.1x₁ + 0.4x₂ + 0.3
> ```
>
> **One line. One weighted sum. One bias.** The two-layer network has not just *become* a single layer — it always *was* one, written out the long way.

**That is the whole argument, and it is three lines of GCSE algebra.** No calculus, no matrices, no proof. Ten layers with no squash would collapse the same way, into one line. Depth without a squash buys **exactly nothing**.

**Now show it with a number, because algebra convinces about half the room and a number convinces the rest.** Take `x = [2.0, −1.0]`:

```text
h1 = 0.5(2.0) + 0.8(−1.0) + 0.1  =  1.0 − 0.8 + 0.1  =  0.30
h2 = −0.3(2.0) + 0.2(−1.0) + 0.05 = −0.6 − 0.2 + 0.05 = −0.75

no squash:  out = 1.0(0.30) − 2.0(−0.75) + 0.3 = 0.30 + 1.50 + 0.30 = 2.10
one line:   out = 1.1(2.0) + 0.4(−1.0) + 0.3   = 2.20 − 0.40 + 0.30 = 2.10   ← same
```

**And now put a ReLU in the middle.** `h2` was `−0.75`, and ReLU turns that into `0`:

```text
with ReLU:  out = 1.0(0.30) − 2.0(0) + 0.3 = 0.30 + 0 + 0.30 = 0.60
```

**`2.10` against `0.60`. A gap of exactly `1.50`, and the one-line version cannot produce it.** The `−0.75` was cut to zero, and a rule that cuts *some rows and not others* is not a straight line — that is the bend. (Sigmoid and tanh bend too, by curving instead of cutting.) Say that sentence in class.

![With no squash, two layers are one straight line](../figures/fig-w16-4-no-squash-two-layers-collapse-to-a-line.svg)
*Figure 16.4 — With no squash, two layers are one straight line. With ReLU the `−0.75` becomes `0`, the answer drops from `2.1` to `0.6`, and the gap is `1.5`.*

### 6. Why ReLU is the default, in one number

Every book says "ReLU is the default hidden activation" and almost none of them say why in a way a 14-year-old can check. Here is the version that works, and it takes ninety seconds with a calculator.

**Measure how steep each squash is, using Week 12's nudge.** Pick a point, step a thousandth either side, subtract, divide by `0.002`. That is all "how steep is it here" means, and the class has been doing it for four weeks.

| At `z =` | sigmoid's steepness | tanh's steepness | ReLU's steepness |
|---|---|---|---|
| 0.0 | **0.250000** | 1.000000 | 0.500000 (the corner — see below) |
| 1.0 | 0.196612 | 0.419974 | **1.000000** |
| 2.0 | 0.104994 | 0.070651 | **1.000000** |
| 5.0 | 0.006648 | 0.000182 | **1.000000** |
| 10.0 | 0.000045 | 0.000000 | **1.000000** |

**Read the sigmoid column out loud.** The very steepest sigmoid ever gets is `0.25`, right in the middle. By `z = 5` it is `0.0066` — essentially flat. And here is why that matters, and it is the only bit of Week 18 you should trail today:

In two weeks the class will learn that **slopes multiply along a chain**. Five layers of sigmoid means multiplying five of those numbers together, and the best case is

```text
0.25 × 0.25 × 0.25 × 0.25 × 0.25 = 0.0009765625
```

**One thousandth of the signal survives five layers.** With ReLU, every one of those numbers is exactly `1.00`, so `1 × 1 × 1 × 1 × 1 = 1` and the signal arrives at full strength. That is the main reason (ReLU is also cheap to compute). It is a multiplication you can do on a calculator, and it is a big part of why very deep sigmoid networks were so hard to train before ReLU became standard around 2010–2012. (The full chain also multiplies in the weights; Week 18 adds that.)

> **🧑‍🏫 If a student asks:** *"why does ReLU's steepness say `0.5` at zero?"* — because ReLU has a **corner** there, and a corner has no single steepness. Nudging up gives slope 1, nudging down gives slope 0, and averaging the two nudges gives `0.5`. **This is not a fact anybody discovered; it is a choice.** numpy's two-sided nudge splits the difference; PyTorch, when you get there in Week 20, will tell you `0`. Both are defensible. **Say plainly that maths has a genuine hole here and engineering filled it with a decision**, because a student who spots that on their own has spotted something real.

### 7. Every line of `neuron.py`, explained to somebody who has never programmed

```python
import numpy as np
```

Fetches the library that does arithmetic on whole grids of numbers at once. `as np` means "and let me call it `np` for short".

```python
np.random.seed(0)
np.set_printoptions(precision=6, suppress=True)
```

The first line fixes the dice so that anything random comes out the same every time you run it — nothing today is random, but it is a habit worth having in every file. The second says: when you print decimals, show six places, and **don't** use scientific notation like `1e-05`. It only affects printing, never the maths.

```python
w = np.array([0.4, -0.7, 1.2])
b = -0.5
```

`np.array([...])` builds a grid from a list. This list has no inner lists, so it is a **flat** list of three numbers — shape `(3,)`. `b` is one ordinary number.

```python
rows = np.array([[2.0, 1.0, 0.5],
                 [-1.0, 2.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0]])
```

**Lists inside a list.** The outer list holds the rows; each inner list is one row's three numbers. Four inner lists, three numbers each, so shape `(4, 3)`.

```python
print("rows.shape =", rows.shape)
```

`.shape` is not a function you call with brackets — it is a property the grid carries around. **This is the line to make into a reflex.**

```python
def relu(z):
    return np.maximum(0, z)
```

`def` starts a named recipe. `np.maximum(0, z)` compares `0` against `z` **one number at a time** and keeps whichever is bigger. Hand it a single number and you get a single number; hand it a grid of a thousand and you get a grid of a thousand. That per-number behaviour is why it is `np.maximum` and not Python's built-in `max` — the built-in tries to compare a whole grid against `0` in one go and gives up with `The truth value of an array with more than one element is ambiguous`.

```python
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))
```

Week 13's squasher, unchanged. `np.exp(x)` is `e^x`, the button on the calculator.

```python
for r in rows:
    z = (r * w).sum() + b
```

`for r in rows:` means "do the following once for each row, calling it `r`". `r * w` multiplies **matching positions** — first with first, second with second, third with third — giving three products. `.sum()` adds those three up. Then `+ b` adds the bias. **That one line is "multiply, add".**

```python
    print("%-18s %8.2f %8.3f %9.3f %8.3f"
          % (str(r), z, relu(z), sigmoid(z), np.tanh(z)))
```

The `%` string is a layout instruction: `%8.3f` means "a decimal number, eight characters wide, three places after the point". It is there so the columns line up under each other on screen. `np.tanh(z)` is the third squash, and numpy has it built in.

### 8. The three misconceptions you will actually meet

**Misconception 1 — "the bias is just a rounding-off number, you could leave it out."**
No. The bias is the neuron's **threshold**. With `b = −0.5` the three features have to earn more than `0.5` before the neuron says anything. Set `b = 0` and the threshold is pinned at exactly zero for ever, which is one specific and usually wrong choice. **The demonstration:** run row `[0, 0, 1]` with the bias (`z = 0.70`, ReLU says `0.700`) and then without it (`z = 1.20`, ReLU says `1.200`). Different neuron, different opinions.

**Misconception 2 — "`.T` and `.reshape` are the same thing, they both gave `(2, 3)`."**
Same shape, different numbers, and Figure 16.3 exists entirely for this. `G.T` reads down the columns: `1 3 5 / 2 4 6`. `G.reshape(2, 3)` reads along the rows: `1 2 3 / 4 5 6`. **Make them read both printouts aloud, left to right.** The shapes agree; the contents do not.

**Misconception 3 — "the squash is there to keep the numbers tidy."**
This is the one that matters and it is the objective. The squash is there **so that the second layer is not a waste of money.** Without it, two layers *are* one layer — three lines of algebra prove it and one row of numbers shows it (`2.10` versus `0.60`). Tidiness is a side effect. If a student leaves believing the squash is cosmetic, the lesson has failed even if every number on their sheet is right.

### 9. How deep to go, and where to stop

**Go this far:** one neuron computed by hand for three squashes, four rows; the shape of a grid counted off a printout and printed in code; `.T` versus `.reshape` distinguished by their contents; the collapse proved in three lines of algebra and confirmed with one row of numbers; ReLU's steepness of `1` contrasted with sigmoid's best-ever `0.25`; the words *layer*, *hidden layer* and *MLP* said once each.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **`A @ B`, matrix multiply, any `@` at all** | **Week 17, next week.** Today every neuron is one row at a time with `(r * w).sum()`. Reaching for `@` today wastes next week's entire lesson. |
| Networks with more than two layers, drawings of many neurons | **Week 19.** Say *layer*, *hidden layer* and *MLP*, point at the two-layer example, stop. |
| **Backpropagation, gradients of a network, the chain rule** | **Week 18.** You may say "in two weeks we work out how much each weight contributed" and nothing more. |
| **softmax** | **Week 17.** Three squashes is already three. A fourth is a squash too far. |
| Dead ReLUs | **Week 19**, where they can be counted in a real trained network. Today ReLU returning `0` is just "the judge said nothing". |
| `nn.Linear`, `nn.ReLU`, PyTorch, tensors | **Weeks 20–22.** No torch this week at all. |
| Why `sqrt(2/n)` is the right size for a starting weight | **Week 18** (He initialization). Today all the weights are typed by hand. |
| Vanishing gradients as a named phenomenon | Name-drop only if a student gets there. The `0.25⁵ = 0.00098` arithmetic is enough today; the name arrives in Week 19. |

The line to hold all lesson: **one neuron, three inputs, three squashes, and the shape printed before anything else.**

---

### 10. 🧭 The Growing Map — the same box, the second of four weeks

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week nothing moves, and the two minutes are spent explaining why that is fine.

![The Level 3 pipeline in Week 16: still the descent, neuron and layer tile, now one neuron by hand](../figures/fig-w16-0-where-this-fits.svg)

*Figure 16.0 — Week 16's version. Second week inside the gold `descent · neuron · layer` tile. The ↻ on
stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "which word?"** The box is the same gold tile as last
   week, *descent · neuron · layer*. The word is **neuron** — the second of four weeks in a four-week
   tile. Week 15 was descent, Week 17 is the layer, Week 18 is what holds them together.
2. **Anchor it on the three lines of substitution.** `out = 1.1x₁ + 0.4x₂ + 0.3` is still on the board:
   two layers with no squash between them, collapsed into one straight line. *"That is why the word in
   this box is neuron and not just weighted sum. The squash is the difference, and without it this box
   would not need to exist."*
3. **Point at stage four and say what it is not.** `REAL NETWORKS` is still dashed. *"We built what a
   network is made of, not a network. The twenty-circle picture is Week 19."* Students who have seen
   neural networks online often assume they are behind; the dashed box is the honest answer.

> **🧑‍🏫 Why this is worth two minutes.** The temptation this week is to feel small — one neuron, three
> inputs, done by hand. The map reframes the scale: everything in the two dashed stages on the right is
> made of the thing they built today, thousands of times over. That is not a small week, it is the
> smallest possible complete unit.

**One thing to notice, so you can answer if asked.** The threads changed: `representation` is lit
alongside `model`, and `learning signal` went dark for one week. That is deliberate — nothing trained
today. The squashed activation is a **new description of the row**, which is representation, and it is
the same idea as Week 4's scaling wearing different clothes.

---

## 🧰 Prep Checklist

Use this section to get everything ready before class. It holds the complete runnable files.

### 20 minutes the night before

- [ ] **Write the six index cards.** Thick pen, big enough to read from the back of the room. Three input cards, three weight cards, one bias card:

```text
   x1 = 2.0        x2 = 1.0        x3 = 0.5

   w1 = 0.4        w2 = -0.7       w3 = 1.2

   b = -0.5
```

  Make a **second set** with the four rows' inputs on the back of the three input cards, so one person can flip to the next row without reshuffling: back of card 1 reads `-1.0 / 0.0 / 1.0`, back of card 2 reads `2.0 / 0.0 / 1.0`, back of card 3 reads `0.0 / 1.0 / 1.0`.

- [ ] **Type and run `neuron.py` yourself.** The complete file:

```python
"""neuron.py - one neuron, by hand, checked in numpy."""
import numpy as np

np.random.seed(0)
np.set_printoptions(precision=6, suppress=True)

w = np.array([0.4, -0.7, 1.2])
b = -0.5

rows = np.array([[2.0, 1.0, 0.5],
                 [-1.0, 2.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0]])

print("w.shape    =", w.shape)
print("rows.shape =", rows.shape)
print()

def relu(z):
    return np.maximum(0, z)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

print("%-18s %8s %8s %9s %8s" % ("row", "z", "ReLU", "sigmoid", "tanh"))
for r in rows:
    z = (r * w).sum() + b
    print("%-18s %8.2f %8.3f %9.3f %8.3f"
          % (str(r), z, relu(z), sigmoid(z), np.tanh(z)))
```

Run `python3 neuron.py`. You must see **exactly** this:

```text
w.shape    = (3,)
rows.shape = (4, 3)

row                       z     ReLU   sigmoid     tanh
[2.  1.  0.5]          0.20    0.200     0.550    0.197
[-1.  2.  0.]         -2.30    0.000     0.091   -0.980
[0. 0. 1.]             0.70    0.700     0.668    0.604
[1. 1. 1.]             0.40    0.400     0.599    0.380
```

**Runtime: well under a second.**

- [ ] **Run `shapes8.py`** (full file in the Answer Key, under Build It Part B) so the three printouts are familiar. **Under a second.**
- [ ] **Run `collapse.py`** (full file in the Answer Key, under M4 — "The chapter's own collapse"). The line you care about is the last one: **`biggest disagreement between two layers and one line: 4.440892098500626e-16`**. **Under a second.**
- [ ] **Run `moons_look.py`** (Answer Key, last section, "Not in the workbook — the `make_moons` first look") and **look at `moons.png`**. You will show it for ninety seconds at the end. **About 1 second.**
- [ ] **Do these four things on your own calculator.** If you have not, you cannot answer *"where did 0.550 come from?"*, and somebody will ask:

| Keys | Result |
|---|---|
| `0.2`, make it negative, `e^x` | `0.818731` |
| `+ 1 =`, then `1/x` | **`0.549834`** — that is sigmoid(0.20) |
| `2.3`, `e^x` | `9.974182` |
| `+ 1 =`, then `1/x` | **`0.091123`** — that is sigmoid(−2.30) |

- [ ] **Break it on purpose, twice**, so both deliberate mistakes in the live-code are muscle memory:
  1. Write `max(0, z)` instead of `np.maximum(0, z)` where `z` is a grid. Real message: `ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()`.
  2. Write `G.reshape(4, 2)` on a six-number grid. Real message: `ValueError: cannot reshape array of size 6 into shape (4,2)`.
- [ ] **Print the workbook, `workbook/week-16.md`, without its ✅ Answers section** (it is the last section, inside a `<details>` block — cut it off before printing, or the student has the answers). Read its ✅ Answers section yourself first: the 🔑 Answer Key below follows the workbook item by item.
- [ ] **Clear a wide space on the board** for a five-column, four-row table. You will fill it in by hand before any laptop is opened.

### 5 minutes on the day

- [ ] Six index cards on the desk, in order, weights face down.
- [ ] Editor open, terminal ready. **`neuron.py` deleted or renamed** — they type it.
- [ ] `w = [0.4, −0.7, 1.2]` and `b = −0.5` already on the board, top left, boxed.
- [ ] The blank five-column table drawn on the board: `row | z | ReLU | sigmoid | tanh`.
- [ ] A calculator per student, and check the `e^x` key works on yours.
- [ ] Bug Log out. Week 15's loss curves still on the wall.

### Fallback if the laptops fail

**This week barely notices a power cut.** Every number today fits on a calculator, and the activity was already unplugged.

1. **Run the whole Human Neuron activity** (🎲 below) and give it twenty-five minutes instead of twenty. Four rows through the cards, out loud.
2. **Fill the four-row table entirely by hand.** Twelve squash results plus four `z` values. With a calculator that is about twelve minutes, and the class does the work the laptop would have done.
3. **The collapse proof needs no computer at all.** Three lines of substitution, then the row `[2.0, −1.0]` giving `2.10` with no squash and `0.60` with ReLU. **This is objective 3 in full, in chalk.**
4. **The steepness table, on calculators.** Give three students `z = 0`, `z = 2`, `z = 5` and have them nudge sigmoid by a thousandth either side. They will get `0.25`, `0.105`, `0.0066`. Then `0.25` to the power five on the calculator: `0.0009765625`. **That is objective 4, delivered with five calculators.**
5. **The shapes, on paper.** Write the six-number grid on the board three ways — as `(3, 2)`, transposed, and reshaped — and have them count rows and columns with a finger. Objective 2 works better on paper than on screen anyway.

| If this fails | Do this instead |
|---|---|
| `ValueError: The truth value of an array with more than one element is ambiguous` | They wrote `max` instead of `np.maximum`. Python's `max` cannot compare a whole grid against a number. |
| `ValueError: cannot reshape array of size 6 into shape (4,2)` | `4 × 2 = 8` and there are only 6 numbers. Reshape can never invent or discard a number. |
| `ValueError: operands could not be broadcast together with shapes (2,3) (4,)` | The weight list has four numbers and the rows have three columns. Print both shapes; the mismatch is visible immediately. |
| `a.T` printed the same thing as `a` and a student thinks numpy is broken | `a` is flat, shape `(3,)`. There is nothing to flip. `a.reshape(1, 3).T` gives `(3, 1)`. |
| `AttributeError: 'list' object has no attribute 'shape'` | They forgot `np.array(...)`. A plain Python list has no shape. |
| sigmoid comes out as `0.5498...` and the board says `0.550` | Same number. The board is rounded to three places; `print("%.3f" % ...)` makes them match. |
| Everyone can compute `z` but nobody believes the collapse | You did the algebra and skipped the number. Do `[2.0, −1.0]`: `2.10` without the squash, `0.60` with. **The gap of 1.5 is the lesson.** |

---

## ⏱️ The Lesson, Minute by Minute

Use this section to run the class. The table gives the shape of the hour; the steps that follow give the words to say.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Grumpy Judge | 7 | 7 | Three cards, one bias, one number on the board before the word *neuron* is used |
| 🧠 Concept & Maths — z, a, and the shape | 18 | 25 | Three squashes on two numbers; the shape counted off a printout; `.T` versus `.reshape` |
| 💻 Live-Code Together — `neuron.py` | 18 | 43 | Build it, run it, match the board. **Two deliberate mistakes.** |
| 🎲 Their Turn — Human Neuron, then take the Squasher away | 20 | 63 | Four rows through the cards, then the collapse on the board |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, ninety seconds of `make_moons`, homework |

---

### 🪝 Hook — The Grumpy Judge (7 minutes)

**Do this:** Laptops shut. Hand the three input cards to three students, the three weight cards to a fourth, the bias card to a fifth. Write nothing on the board except the blank table.

**Say this:**

> "Talent show. Three of you are holding an act's scores — singing, dancing, stage presence. Read them out.
>
> **Two point zero. One point zero. Nought point five.**
>
> Now, there is one judge. She has opinions, and they are written on those three cards over there. Read them out.
>
> **Singing, times nought point four. Dancing, times minus nought point seven — she hates dancing. Stage presence, times one point two.**
>
> And one more card. She is permanently grumpy, so before she says anything at all she subtracts nought point five. Read it.
>
> **Minus nought point five.**
>
> Right. Multiply each score by its weight and tell me the four numbers."

**Do this:** Write them on the board as they come, in a column:

```text
   0.8
  -0.7
   0.6
  -0.5
```

**Ask this:** "Add them up. Out loud, left to right."

*Hoped-for answer:* `0.8 − 0.7 = 0.1`, `+ 0.6 = 0.7`, `− 0.5 = 0.20`.

*If somebody gets `1.0`:* they dropped the bias. Point at the fifth card and ask them to read it again. **Do not correct it yourself** — the bias getting forgotten is the whole reason it is a separate card held by a separate person.

**Do this:** Write `z = 0.20` on the board, large, and box it.

**Say this:**

> "Nought point two. Now — that is the judge's private grumbling. It is not her verdict yet. She has to turn a private feeling into a public score, and how she does that is the only genuinely new thing in today's lesson.
>
> If she is the simplest kind of judge, she does this: **if I felt bad, I say nothing. If I felt good, I say exactly what I felt.** She felt `+0.20`, so she says `0.20`.
>
> That judge has a name, and it is the ugliest name in this subject: **ReLU**. It stands for rectified linear unit, which tells you nothing, so forget the words and remember the rule: **negatives become zero, positives come through untouched.**
>
> And the whole thing you just did — multiply each input by a weight, add them up, add the bias, squash — has a name too. **That is a neuron.** One. You just ran one, with five people and a piece of card, and there was no calculus in it.
>
> Every model in the news is millions of those. Not millions of *ideas* — millions of *that*."

**Ask this:** "Before we go on — why do you think she has that separate grumpy card? What would change if it were zero?"

*Hoped-for answer:* she would say something for anything above zero; the bias moves the point where she starts speaking.

*If they say "nothing much":* try it. `[0, 0, 1]` gives `z = 0.70` with the bias and `z = 1.20` without. Two different judges. **The bias is the threshold, and threshold is the word to write down.**

---

### 🧠 Concept & Maths — z, a, and the shape (18 minutes)

**Do this (6 min) — the second row, and the other two squashes.** Flip the input cards to their backs: `x = [−1.0, 2.0, 0.0]`.

Work it on the board with them:

```text
−1.0 × 0.4    = −0.4
 2.0 × (−0.7) = −1.4
 0.0 × 1.2    =  0.0
 bias         = −0.5
                -----
z             = −2.30
```

**Ask this:** "ReLU judge. What does she say?"

*Hoped-for answer:* nothing — zero.

> **Say this:** "Nothing. Silence. `z` was `−2.30`, and ReLU turns every negative into a flat zero. She had an opinion and she kept it to herself.
>
> Now — two other judges exist, and they are the ones you meet in every book, so we are going to run the same two numbers past all three.
>
> **The sigmoid judge** you already know from Week 13. She never says zero and she never says one; she squashes everything into the gap between. **The tanh judge** is her cousin, and the difference is that tanh can say a **negative** number — it runs from minus one to plus one."

**Do this:** Fill in the two rows of the board table, on calculators, with them:

```text
row              z        ReLU   sigmoid     tanh
[2, 1, 0.5]    0.20      0.200     0.550    0.197
[-1, 2, 0]    -2.30      0.000     0.091   -0.980
```

Walk the sigmoid keystrokes out loud for `−2.30`: **`2.3`, `e^x` → `9.974182`. Plus one → `10.974182`. `1/x` → `0.091123`.** Round to three places: `0.091`.

**Ask this:** "One of those twelve numbers is negative. Which, and what does that tell you?"

*Hoped-for answer:* tanh's `−0.980`; only tanh can go below zero.

> **Say this:** "Only tanh. ReLU's floor is zero. Sigmoid's floor is zero and it never reaches it. Tanh is the only one of the three that can hand the next layer a negative number, and that is genuinely useful sometimes — which is why it is still around."

**Do this (7 min) — the new maths: the shape.** Write this on the board and nothing else:

```text
[[1 2]
 [3 4]
 [5 6]]
```

**Ask this:** "How many rows, and how many numbers across?"

*Three rows, two across.* Write `(3, 2)` beside it.

> **Say this:** "Three by two. **Rows first, columns second, always, for the rest of your life.** Six numbers, and the brackets tell you the layout: three inner groups, two numbers in each.
>
> This is the only new maths this week, and it does not look like maths. It looks like counting, because it is counting. But here is the promise I am making you: **from today until Christmas, when something goes wrong, the first thing you print is the shape.** Not the numbers. The shape. Two numbers, and they will tell you what is broken about nine times out of ten."

**Do this:** Write the other two grids beside it:

```text
G.T = [[1 3 5]        G.reshape(2, 3) = [[1 2 3]
       [2 4 6]]                          [4 5 6]]
```

**Ask this:** "Both of those are `(2, 3)`. So are they the same grid?"

*Hoped-for answer:* no — the numbers are in different places.

*If they say yes:* read both aloud, left to right, and let them hear it. **"One, three, five" versus "one, two, three."** Then: *"same shape, different contents. Shape is not identity."*

> **Say this:** "`.T` is a flip on the diagonal — it reads **down the columns** of the original. `.reshape` keeps the numbers in the order they were and just re-draws the brackets — it reads **along the rows**.
>
> And here is the check that stops reshape going wrong: **`3 × 2 = 6`, and `2 × 3 = 6`.** Reshape can never invent a number and never throw one away. Ask for `(4, 2)` — that is eight cells — and it refuses, and we will see it refuse in about ten minutes."

**Do this (5 min) — the steepness table, and the reason ReLU won.** This is objective 4 and it takes five minutes on calculators.

> **Say this:** "One more thing about the three judges, and it is the reason almost everybody uses ReLU and almost nobody uses sigmoid in the middle of a network.
>
> You have been measuring steepness since Week 12. Nudge a thousandth up, nudge a thousandth down, subtract, divide by nought point zero zero two. Three of you do sigmoid at `z = 0`, `z = 2` and `z = 5`."

Real answers, so you can mark instantly: **`0.250000`, `0.104994`, `0.006648`.**

**Do this:** Write on the board, large:

```text
sigmoid's steepest is 0.25, ever
ReLU's steepness is 1, everywhere it fires

0.25 × 0.25 × 0.25 × 0.25 × 0.25 = 0.0009765625
1    × 1    × 1    × 1    × 1    = 1
```

> **Say this:** "In two weeks you will find out that when you stack layers, **their steepnesses multiply.** So five sigmoid layers hand the first layer about **one thousandth** of the signal. Five ReLU layers hand it **all of it.**
>
> That is not an opinion or a fashion. It is that multiplication, and it is a big part of why very deep networks were so hard to train until people switched to ReLU around 2010–2012. You have just done, on a calculator, a piece of the arithmetic behind that change."

---

### 💻 Live-Code Together — `neuron.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — the weights, and the shape reflex.**

```python
import numpy as np

np.random.seed(0)
np.set_printoptions(precision=6, suppress=True)

w = np.array([0.4, -0.7, 1.2])
b = -0.5

rows = np.array([[2.0, 1.0, 0.5],
                 [-1.0, 2.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0]])

print("w.shape    =", w.shape)
print("rows.shape =", rows.shape)
```

```text
w.shape    = (3,)
rows.shape = (4, 3)
```

**Ask this:** "`(3,)`. There is a comma and then nothing. Is that a typo?"

*Hoped-for answer:* no — it means one number in the shape.

> **Say this:** "Not a typo. `w` is a **flat** list: three numbers, no rows and columns. Python writes a one-number shape with a trailing comma so you cannot mistake it for a plain number in brackets. And `rows` is `(4, 3)` — **four rows, three columns.** Four acts, three scores each. Say it out loud: four by three."

**Step 2 (5 min) — 🐞 DELIBERATE MISTAKE ONE: `max` instead of `np.maximum`.**

Type this, with the wrong function:

```python
def relu(z):
    return max(0, z)

z_all = (rows * w).sum(axis=1) + b
print(relu(z_all))
```

Real output:

```text
Traceback (most recent call last):
  File "neuron.py", line 17, in <module>
    print(relu(z_all))
  File "neuron.py", line 14, in relu
    return max(0, z)
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

**Do this:** Say nothing for five seconds. Let them read it.

**Ask this:** "'The truth value of an array is ambiguous.' What do you think Python is complaining about?"

*Hoped-for answer:* it is trying to compare a whole grid against zero and does not know what a yes-or-no answer would even mean.

> **Say this:** "Exactly that. Python's built-in `max` looks at two things and asks *'is this one bigger?'* — one question, one yes-or-no answer. I handed it **four numbers at once**, and 'is `[0.2, −2.3, 0.7, 0.4]` bigger than zero' has no single answer. Some of them are.
>
> **numpy's version asks the question once per number.** `np.maximum(0, z)` walks along the grid, compares each number against zero on its own, and hands back a grid the same shape. That is the whole difference, and it is a difference you will meet a hundred more times: **built-in Python functions work on one thing; numpy functions work on every cell.**"

Fix it to `np.maximum(0, z)`, re-run:

```text
[0.2 0.  0.7 0.4]
```

**Bug Log, ninety seconds**, with the sentence *"`max` asks one question; `np.maximum` asks one question per cell."*

**Step 3 (5 min) — the loop, and matching the board.**

```python
def relu(z):
    return np.maximum(0, z)

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

print("%-18s %8s %8s %9s %8s" % ("row", "z", "ReLU", "sigmoid", "tanh"))
for r in rows:
    z = (r * w).sum() + b
    print("%-18s %8.2f %8.3f %9.3f %8.3f"
          % (str(r), z, relu(z), sigmoid(z), np.tanh(z)))
```

```text
row                       z     ReLU   sigmoid     tanh
[2.  1.  0.5]          0.20    0.200     0.550    0.197
[-1.  2.  0.]         -2.30    0.000     0.091   -0.980
[0. 0. 1.]             0.70    0.700     0.668    0.604
[1. 1. 1.]             0.40    0.400     0.599    0.380
```

**Do this:** Walk to the board and put a tick beside each of the eight numbers the class computed by hand. Do it slowly and out loud.

> **Say this:** "Eight numbers, eight ticks. And the two rows you did not do are there too, so let us check one of them by mental arithmetic. Row three is `[0, 0, 1]`. Nought times nought point four, nought times minus nought point seven, one times one point two, minus nought point five. **One point two minus nought point five is nought point seven.** The screen says `0.70`.
>
> There is nothing in this program you cannot do with a pencil. It is just faster."

**Step 4 (4 min) — 🐞 DELIBERATE MISTAKE TWO: reshape to a shape that cannot exist.**

```python
G = np.array([[1, 2], [3, 4], [5, 6]])
print("G.shape       =", G.shape)
print("G.T           =", G.T.shape)
print(G.reshape(4, 2))
```

```text
G.shape       = (3, 2)
G.T           = (2, 3)
Traceback (most recent call last):
  File "neuron.py", line 30, in <module>
    print(G.reshape(4, 2))
ValueError: cannot reshape array of size 6 into shape (4,2)
```

**Ask this:** "Read the message. It names two numbers. What are they and why do they disagree?"

*Hoped-for answer:* size 6 is how many numbers there are; `(4, 2)` needs eight.

> **Say this:** "Six numbers in, eight cells asked for. numpy will not invent two numbers and it will not throw two away, so it stops. **This is the friendliest error message you will get all year: it tells you the total it has and the total you asked for, and the fix is arithmetic.**
>
> Which shapes are legal for six numbers? `(1, 6)`, `(2, 3)`, `(3, 2)`, `(6, 1)`. Anything whose two numbers multiply to six."

Fix it to `G.reshape(2, 3)` and print both it and `G.T` side by side. **Bug Log.**

---

### 🎲 Their Turn — Human Neuron, then take the Squasher away (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: run all four rows through the six cards with a human Adder and a human Squasher, then send the Squasher out of the room and watch two layers collapse into one straight line.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the completed board table. Write four things underneath it:

```text
z   = multiply, add          the pre-activation, any number at all
a   = squash                 the activation, the neuron's output
(3, 2)                       rows first, columns second, printed FIRST
no squash                    two layers ARE one layer: 1.1x1 + 0.4x2 + 0.3
```

**Say this:**

> "Four things, and that is the week.
>
> **`z` is multiply-and-add.** You have been doing that since Week 15. It can be any number: minus forty, six thousand, nought point two.
>
> **`a` is the squash.** ReLU says nothing when it is unhappy. Sigmoid squeezes into nought-to-one. Tanh squeezes into minus-one-to-one and is the only one that can hand back a negative.
>
> **`(3, 2)` means three rows, two columns**, and it is the first thing you print when anything is confusing. I will hold you to that for the rest of the year.
>
> **And the big one: with no squash, two layers are one layer.** You proved it in three lines of algebra and then you proved it again with `2.1` against `0.6`. Depth without a squash is an expensive way to draw a straight line."

**Do this — ninety seconds, and it is the hook for the next four weeks.** Open `moons.png` on the screen. Say nothing at first; let them look at two interleaving crescents.

```text
X.shape = (400, 2)
y.shape = (400,)
first three rows of X:
[[-0.49511301  0.96602758]
 [ 1.71424117 -0.49933902]
 [ 1.3702969  -0.37944818]]
first three labels  : [0 1 1]
class counts        : [200 200]
```

> **Say this:** "Four hundred points, two features, two classes, two hundred each. Look at the shape of it — two crescents, hooked into each other.
>
> **Take a ruler and try to separate them with one straight line.** You cannot. Not with a clever line, not with the best line — there is no straight line that gets these right.
>
> Everything you have built this term draws a straight line. So for the next four weeks the whole job is: **build something that can bend.** And you already know what the bend is made of, because you met it today. It is the squash."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Do this:** Hand out the homework. Read the second half out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()` | "You asked me one yes-or-no question about many numbers." | Python's built-in `max(0, z)` or `if z > 0:` used on a whole grid. | `np.maximum(0, z)`. For the `if`, you almost never want one — you want `(z > 0)`, which gives one True/False **per cell**. |
| `ValueError: cannot reshape array of size 6 into shape (4,2)` | "Six numbers cannot fill eight cells." | `G.reshape(4, 2)` on a six-number grid. | Pick a shape whose two numbers multiply to 6: `(2, 3)`, `(3, 2)`, `(1, 6)`, `(6, 1)`. |
| `ValueError: operands could not be broadcast together with shapes (2,3) (4,)` | "Three columns cannot be paired with four weights." | The weight list has the wrong number of weights for the number of features. | Print both shapes. One weight per column, always. |
| `AttributeError: 'list' object has no attribute 'shape'` | "A plain Python list does not know its own shape." | `w = [0.4, -0.7, 1.2]` without `np.array(...)`. | Wrap it: `np.array([0.4, -0.7, 1.2])`. |
| `TypeError: 'tuple' object is not callable` | "`.shape` is a property, not a function." | Written `arr.shape()` with brackets. | Drop the brackets: `arr.shape`. |
| `AttributeError: module 'numpy' has no attribute 'max imum'` (or `'maxium'`, `'maximium'`) | "There is no function with that name." | Typo in `np.maximum`. It is genuinely easy to misspell. | `np.maximum` — m-a-x-i-m-u-m. Note it is **not** `np.max`, which is a different function that finds the single largest value. |
| **No error. `a.T` prints exactly the same thing as `a`.** | Nothing is wrong. | `a` is flat — shape `(3,)`. There is nothing to flip. | If you need a column: `a.reshape(1, 3).T` gives shape `(3, 1)`. |
| **No error. `np.max(0, z)` returns something odd or crashes with `AxisError`.** | `np.max` and `np.maximum` are different functions. | `np.max(arr)` finds the single biggest number; `np.maximum(a, b)` compares two things cell by cell. | For ReLU you always want **`np.maximum`**. |
| **No error. Every sigmoid answer is `0.5`.** | Nothing crashed; every `z` is zero. | The bias was left out **and** the weights are all zero, or `w` was defined but never used in the sum. | Print `z` before squashing. If `z` is all zeros, the multiply-and-add never happened. |
| **No error. The `z` column is right but every squash column is identical.** | Nothing crashed. | The same function got called three times — usually `relu(z)` pasted into all three slots. | Read the print line back, slot by slot: `relu(z)`, `sigmoid(z)`, `np.tanh(z)`. |
| **No error, and the answer is off by exactly the bias.** | Arithmetic slip, not a code bug. | `+ b` missing from `(r * w).sum() + b`. | This is the single most common error of the week and it is why the bias is a separate index card. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds the move that will matter most for the next twelve weeks, and it is one line long.

21. **"Print the shape."** Before anything else. Every time. `print(arr.shape)`. If the two numbers are not what the student expected, the bug is upstream of where they are looking. Say it so often this term that they start saying it back to you.

22. **"Read the error message out loud and tell me the two numbers in it."** Almost every message this week and next names two numbers that failed to agree — `size 6` and `shape (4,2)`, `(2,3)` and `(4,)`. **The two numbers are the diagnosis.** A student who reads the message aloud has usually solved it by the end of the sentence.

And the sentence for this week:

> **"`z` is multiply-and-add. `a` is squash. And if you do not know what shape something is, you do not know what your program is doing — so print it."**

---

## 🎲 The Activity, In Full

### Human Neuron, then take the Squasher away

**What it is.** Two halves. First, six students *become* one neuron and run four rows of data through themselves out loud — that is objective 1, and doing it with bodies rather than a keyboard is why it sticks. Then the Squasher is sent out of the room and the class discovers on the board that the two-layer network they thought they had was always just a straight line — that is objective 3, and it is the intellectual centre of the week.

### Setup

- **Six index cards**, written thick and large: three inputs, three weights, one bias (that is seven pieces of card; the bias-holder can also be the card-flipper).
- **Six roles**, assigned out loud and swapped between rows so nobody sits still:
  - **three Input holders** — read your number when pointed at
  - **one Weight holder** — read the matching weight
  - **one Adder** — does the running total out loud, and *only* out loud
  - **one Squasher** — applies ReLU, and says the rule before the answer
- Board table drawn, blank: `row | z | ReLU | sigmoid | tanh`.
- The workbook's **M4 — prove the collapse** face down on desks (it is the same proof, on a new network). **Do not let them turn it over yet.**

![Human Neuron: who holds which card](../figures/fig-w16-6-human-neuron-card-setup.svg)
*Figure 16.5 — Human Neuron: who holds which card. The Adder reads out `0.8 − 0.7 + 0.6 − 0.5` and gets `z = 0.20`.*

### Part 1 — four rows through the neuron (10 minutes)

**The script, and it is the same four times.** You point; they speak.

> **You:** "Input one." **Them:** "Two point oh."
> **You:** "Weight one." **Them:** "Times nought point four."
> **You:** "Product." **Adder:** "Nought point eight."
>
> … repeat for inputs two and three …
>
> **You:** "Bias." **Bias holder:** "Minus nought point five."
> **You:** "Adder — the running total, out loud."
> **Adder:** "Nought point eight, minus nought point seven is nought point one, plus nought point six is nought point seven, minus nought point five is **nought point two.**"
> **You:** "Squasher — the rule first, then the answer."
> **Squasher:** "Negatives become zero, positives come through. It is positive, so **nought point two.**"

Write `0.20` in the table. **Swap roles. Next row.**

The four rows and their answers, so you can mark at a glance:

| row | `z` | ReLU | sigmoid | tanh |
|---|---|---|---|---|
| `[2, 1, 0.5]` | **0.20** | 0.200 | 0.550 | 0.197 |
| `[−1, 2, 0]` | **−2.30** | 0.000 | 0.091 | −0.980 |
| `[0, 0, 1]` | **0.70** | 0.700 | 0.668 | 0.604 |
| `[1, 1, 1]` | **0.40** | 0.400 | 0.599 | 0.380 |

**Then the calculators come out** for the sigmoid and tanh columns — eight more numbers, about four minutes. **Insist the Squasher says the rule before the answer, every single time.** It is the difference between a student who knows what ReLU is and one who has memorised that it sometimes says zero.

**Watch for exactly two failure modes.** First, the bias getting dropped — you will hear it because the Adder's running total is short one step. Point at the bias card, do not say the number. Second, a student reading `−0.7` as a subtraction of `0.7` from the *input* rather than a multiplication *by* `−0.7`. Slow that row down and have them say "times minus nought point seven".

![The finished board: four rows through one neuron](../figures/fig-w16-5-board-one-neuron-worked.svg)
*Figure 16.6 — The finished board: four rows through one neuron. `w.shape` is `(3,)` and `rows.shape` is `(4, 3)`, and printing them is the first thing you do.*

### Part 2 — send the Squasher out of the room (10 minutes)

**Do this:** Rub out the neuron. Draw a two-layer network on the board — two inputs, **two** hidden units, one output — and write the weights up:

```text
h1 =  0.5·x1 + 0.8·x2 + 0.1
h2 = -0.3·x1 + 0.2·x2 + 0.05

out = 1.0·h1 - 2.0·h2 + 0.3
```

**Say this:**

> "Two layers. Two judges in the middle, and a head judge who combines their two verdicts. This is a network, properly — the two in the middle are a **hidden layer**, because you never look at what they say, they only report upwards.
>
> But I have made one change. **The Squasher has left the room.** There is no ReLU anywhere. `h1` and `h2` are just weighted sums, and so is `out`.
>
> Now do something for me. Substitute the top two lines into the bottom one, and simplify. Take your time with the minus two."

**Do this:** Let them work for three minutes. Then take it on the board, one collect at a time:

```text
out = 1.0(0.5x1 + 0.8x2 + 0.1) - 2.0(-0.3x1 + 0.2x2 + 0.05) + 0.3

x1 terms:  0.5 + 0.6 = 1.1
x2 terms:  0.8 - 0.4 = 0.4
numbers:   0.1 - 0.1 + 0.3 = 0.3

out = 1.1·x1 + 0.4·x2 + 0.3
```

**Ask this:** "Count the layers in that answer."

*Hoped-for answer:* one.

*If somebody says two:* point at the line. There is no `h` anywhere. It is one weighted sum of the two inputs plus one bias.

> **Say this:** "One. **One weighted sum, one bias, one straight line.** The two-layer network did not *become* a single layer — it always was one, we had just written it out the long way.
>
> Ten layers would do the same. A hundred. **Without a squash in the middle, depth is worth exactly nothing.**"

**Do this — the number that finishes it.** Run the row `x = [2.0, −1.0]` on the board:

```text
h1 = 0.30      h2 = -0.75

no squash:  out = 0.30 + 1.50 + 0.30 = 2.10
one line:   out = 2.20 - 0.40 + 0.30 = 2.10     same
with ReLU:  h2 becomes 0, so out = 0.30 + 0 + 0.30 = 0.60
```

**Ask this:** "Two point one against nought point six. Where did the difference go?"

*Hoped-for answer:* ReLU threw away the `−0.75`.

> **Say this:** "ReLU threw the minus nought point seven five in the bin. And that is not damage — **that is the bend.** ReLU cuts some rows and leaves others alone, and a rule that behaves differently in different places is not a straight line.
>
> Bring the Squasher back in. She is the reason the second layer is worth paying for."

![With no squash, two layers are one straight line](../figures/fig-w16-4-no-squash-two-layers-collapse-to-a-line.svg)
*Figure 16.7 — With no squash, two layers are one straight line. With ReLU the `−0.75` becomes `0`, the answer drops from `2.1` to `0.6`, and the gap is `1.5`.*

### What "finished" looks like

- The four-row table on the board, completely filled, and the same table on the screen from `neuron.py` with every number matching.
- Three lines of substitution in each student's own handwriting, ending in `out = 1.1x₁ + 0.4x₂ + 0.3`.
- The row `[2.0, −1.0]` worked both ways: `2.10` and `0.60`.
- Two Bug Log entries minimum.
- Every student can say, unprompted: **"with no squash, two layers are one layer."**

### Variation — easier

**Do two rows, not four** — `[2, 1, 0.5]` and `[−1, 2, 0]`. One positive `z`, one negative. That is enough to see what ReLU does.

**Do only ReLU** in Part 1, and add sigmoid at the end if there is time. Twelve numbers becomes four.

**For the collapse, skip the algebra entirely and use only numbers.** Give them the two-layer weights and the row `[2.0, −1.0]`, and have them compute `out` with no squash. Then hand them the single line `out = 1.1x₁ + 0.4x₂ + 0.3` as a *gift*, already simplified, and ask them to compute that too. **Both come out `2.10`, and that surprise is the whole lesson.** Then add the ReLU and get `0.60`. No substitution, no collecting terms — three arithmetic answers and the point lands.

### Variation — harder

1. **Find the row where all three squashes agree to two decimal places.** They will need to reason: sigmoid and tanh only agree near… nowhere, actually — sigmoid at `z = 0` is `0.5` and tanh is `0`. **The honest answer is that there is no such row**, and working out *why* (sigmoid is centred on 0.5, tanh on 0) is worth more than finding one.
2. **Design a bias.** "Give me a bias that makes this neuron say nothing at all for every one of the four rows." The largest `z` without the bias is `1.20` (row 3), so any `b` below `−1.20` does it. Check `b = −1.3` on all four.
3. **Three layers, no squash.** Add a third layer to the collapse and show it collapses just as far. It is the same substitution twice, and it kills the idea that "well, maybe with *more* layers it works".
4. **The `(3,)` versus `(1, 3)` versus `(3, 1)` trio.** Build all three from the same numbers, print all three shapes, transpose all three, and explain each result. Two of the six answers surprise people.
5. **Which squash is fastest?** ReLU is one comparison. Sigmoid is an exponential, a division and an addition. Ask them to guess the ratio, then time it with a loop over a large array. **The ratio is real and it is part of why ReLU won**, though the gradient argument matters more.

---

## ❓ Questions Students Ask This Week

**"Is a neuron actually like a brain cell?"**

Barely, and it is worth being honest because the name does real damage.

A real neuron receives signals from thousands of others, fires in **timed spikes** rather than a single number, changes its own wiring, and does chemistry we still do not fully understand. What we build takes a weighted sum and squashes it. **The word "neuron" is a 1940s analogy that stuck**, and it is closer to marketing than biology.

The honest version: **the maths was loosely inspired by a cartoon of a brain cell from the 1940s, and then it turned out to work for reasons that have nothing to do with brains.** Say that. It is more interesting than the myth, and it protects them from a lot of nonsense they will read online.

**"Who chooses the weights? Do you always type them in?"**

No, and this is a good question because today is the *only* week they are typed by hand.

Today's weights are typed so that every number can be checked. **From Week 19 the weights start as small random numbers and the training loop from Week 15 moves them.** That is what "learning" means in this subject: the loop nudges every weight a little bit against its slope, over and over, and the weights end up somewhere useful. Nobody typed the weights of a real model; there are millions of them and no human has ever looked at most of them.

**"Why is it called ReLU? That is a terrible name."**

It is a terrible name and you should say so. "Rectified linear unit" — *rectified* is borrowed from electronics, where a rectifier is a component that lets current through one way and blocks it the other; *linear* because for positive numbers it does nothing at all; *unit* because "neuron" was taken.

**None of that helps you use it.** The rule is: negatives become zero, positives come through untouched. That is `max(0, z)` and it is one line. **A lot of this subject is a simple idea with an intimidating name attached, and knowing that is genuinely useful.**

**"Which squash should I use? Is ReLU always right?"**

Here is the honest split, and it is the practical answer:

| Where | Use | Why |
|---|---|---|
| **hidden layers** | **ReLU** | slope is exactly 1 where it fires, so signal survives many layers |
| **output, two classes** | **sigmoid** | you need a number between 0 and 1, because it is a probability |
| **output, many classes** | softmax (next week) | you need several numbers that add up to 1 |
| **output, a quantity** | **nothing at all** | a house price is not squashed into 0-to-1 |

**And "always" is too strong.** There are variants — leaky ReLU, GELU, and half a dozen others — and which one is best in which situation is **genuinely not settled**. People run experiments and argue. What *is* settled is that a squash of some kind has to be there, and that plain ReLU is a good default that is very hard to beat by much.

**"Does the order of the inputs matter?"**

No, as long as the weights travel with them. Input 1 with weight 1, input 2 with weight 2 — if you shuffle both lists the same way, `z` is identical, because addition does not care about order.

**But if you shuffle the inputs and not the weights, you get a different, wrong number.** That is a real bug and it is silent — no error, just a worse model. It is one of the reasons the shape and the column order of a table matter so much, and why Week 3's pipeline existed.

**"Why do we bother with `z` at all? Why not just have the output?"**

Because `z` is where the interesting things happen and where the bugs live.

Three concrete reasons. **One:** `z` tells you whether a ReLU fired, and in Week 19 a unit whose `z` is negative for every single row is a dead unit — you can only find that by looking at `z`. **Two:** the backward pass in Week 18 needs the *sign* of `z`, not the output, to know which gate was open. **Three:** in Week 22 you will meet loss functions that want `z` handed to them raw, because squashing first and then taking a logarithm loses precision.

**"Is this really all a neural network is?"**

Yes, and you should say so flatly, because it is the single most useful thing they will hear this term.

Multiply, add, squash. Stack them. Nudge the weights against their slopes, over and over. **That is the whole of it.** What separates a lesson from a model that writes essays is the *number* of neurons, the cleverness of how they are wired, and about a hundred million times more data — but not a new idea. There is no chapter you have not been told about.

---

## ⚠️ Where This Lesson Goes Wrong

Use this section to spot the usual ways the lesson goes off course, and what to do right away.

| What happens | Why | What to do right now |
|---|---|---|
| **A twenty-circle network gets drawn in the first ten minutes** | It is the picture everybody expects, and it is fun to draw | **Rub it out.** Today is one neuron and three inputs. The big picture with shapes annotated is Week 17's figure and Week 19's project, and it lands properly there. Drawing it today buys you awe and costs you the collapse proof. |
| The collapse is proved with algebra and never with a number | The algebra feels like the rigorous version, so it feels like enough | **Do the row `[2.0, −1.0]`.** `2.10` with no squash, `0.60` with ReLU. About half the room only believes the number, and they are not wrong to want it. |
| `.T` and `.reshape` get taught as "two ways to change the shape" | They do both change the shape, and both gave `(2, 3)` | Put both printouts on the board and **read them aloud**: "one, three, five" against "one, two, three". Same shape, different contents. Ten seconds, and it prevents a bug that is invisible in Week 17. |
| The bias gets quietly dropped and nobody notices for ten minutes | It is one number among four and it is the last one | It is on a **separate card, held by a separate person**, precisely so that its absence is audible in the Adder's running total. If it still goes missing, hand that card to the student who dropped it. |
| Sigmoid and tanh get skipped for time | ReLU is the important one, so the other two feel optional | They are objective 1 and half of objective 4. **Cut a row, not a squash.** Two rows × three squashes is six numbers and it is enough; four rows × one squash is four numbers and it is not. |
| "Why ReLU?" is answered with "because it works better" | It is true, and it is the answer most books give | **It teaches the student that this subject is folklore.** Do the calculator arithmetic instead: sigmoid's steepest is `0.25`, and `0.25⁵ = 0.00098`. Ninety seconds, and it is a fact they can check. |
| The word *neuron* is used before the arithmetic has been done | It is the title of the lesson | The hook does the arithmetic with cards and **then** names it. That order is deliberate: a student who has already computed `0.20` hears "neuron" as a label for something they did, not as a mystery to be explained. |
| Somebody asks about brains and the lesson goes there for ten minutes | It is a genuinely interesting question | Give the honest ninety-second answer from the Questions section — a 1940s cartoon that turned out to work for unrelated reasons — and move on. Offer to come back to it at the end if there is time. |
| The `(3,)` trailing comma is treated as a typo and glossed over | It looks like a mistake | It will cause a real bug within two weeks. **Show it, name it, and show `a.reshape(1, 3).T`.** Thirty seconds now saves twenty minutes in Week 17. |
| `make_moons` is shown at the start and eats the lesson | It is the most visually interesting thing in the file | It belongs in the **last ninety seconds**, as the question the next four weeks answer. Shown early, it invites "so how do we do it?" and today's answer is "not yet". |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** rows 3 and 4 of the table. Two rows — one positive `z`, one negative — carry the whole idea.

**Cut:** tanh from the live table. Do ReLU and sigmoid, and mention tanh as "sigmoid's cousin that can go negative" with the single number `−0.980` from Figure 16.2.

**Cut:** the algebra in Part 2. Use the numbers-only version in **Variation — easier**.

**Give them `neuron.py` complete.** There is nothing to learn from typing four lists. The learning is in the four `z` values and the twelve squashes.

**The version of the maths that skips the algebra.** One calculator drill, four keypress sequences, and it *is* objective 1:

| Do this on a calculator | Answer |
|---|---|
| `2 × 0.4`, then `1 × (−0.7)`, then `0.5 × 1.2` | `0.8`, `−0.7`, `0.6` |
| Add those three and then subtract `0.5` | **`0.20`** |
| `0.2`, negative, `e^x`, `+1 =`, `1/x` | **`0.549834`** |
| `0.2`, `tanh` | **`0.197375`** |

**Four sequences, and the last two are two of the three squashes.** Then find those same numbers on the screen in `neuron.py`'s first row. That is objective 1, done with a calculator and a printout.

**The copy-this-exactly scaffold.** Nine lines, runs alone:

```python
import numpy as np

w = np.array([0.4, -0.7, 1.2])
b = -0.5
x = np.array([2.0, 1.0, 0.5])

z = (x * w).sum() + b
print("z    =", z)
print("ReLU =", np.maximum(0, z))
```

```text
z    = 0.20000000000000007
ReLU = 0.20000000000000007
```

Then three questions. **"What is `2 × 0.4`?"** (`0.8` — and it is inside that `z`.) **"Which line does the multiply-and-add?"** (The `z =` line.) **"Why is ReLU's answer the same as `z`?"** (Because `z` is positive, so it comes straight through.)

**And one thing to say about that printout, because a student will ask.** `0.20000000000000007` is not a mistake — it is the computer's version of `0.20`. Decimals in binary are like a third in decimal: they do not always end. **`print("%.2f" % z)` gives `0.20`.** It is worth thirty seconds because it comes up every week from here on.

**One thing you must not cut:** the moment when the two-layer network turns out to be one line. If the whole lesson collapses to one sentence, make it *"without the squash, two layers are one layer."*

### If the student is flying

None of these need syntax from a later week.

1. **The bias-design challenge** (harder variation 2): find a bias that silences the neuron on all four rows. It requires them to notice that the largest un-biased `z` is `1.20`, which means reading the table as data rather than as answers.
2. **Three layers, no squash** (harder variation 3), collapsed the same way. It kills "maybe deeper is different" permanently.
3. **The `(3,)` / `(1, 3)` / `(3, 1)` trio** (harder variation 4). Six printouts, and two of them are surprising. This is the deepest available idea today, because it is the thing that will break their Week 17 code.
4. **Which squash is fastest** (harder variation 5), timed on a big array. Then the honest follow-up: *"is speed why ReLU won, or is it the slope?"* (Mostly the slope. Speed is a bonus.)
5. **The corner question.** What is ReLU's steepness at exactly `z = 0`? Our two-sided nudge says `0.5`. PyTorch will say `0`. **Ask them which is right.** Neither — the function has a corner and there is no single answer, so every library makes a documented decision. Getting to "this is a decision, not a fact" unaided is a level-5 moment.
6. **The honest challenge:** *"invent a squash of your own, and tell me why it is bad."* Almost anything they invent will either be a straight line in disguise (so it collapses) or have a flat region that kills the slope. Both failures are exactly the two properties the lesson was about.

### If the student won't engage today

**Close the laptop. Six cards and one calculator.**

Do the Human Neuron with them as the **Adder** — the role that has to speak the running total out loud and cannot hide.

Then change the framing to something with stakes they choose. Ask them to name three things that decide whether a film is worth watching, then have them set the three weights themselves and pick how grumpy the judge is.

> **"Your three features. Your three weights. Your bias. Now score this film: `[8, 3, 6]`. What does your judge say?"**

They have built a neuron, chosen its parameters, and computed an activation — objective 1, without the word *neuron* appearing until afterwards.

Then one question with a ruler in your hand, pointing at `moons.png` on paper:

> **"Separate the two crescents with this ruler. One straight line. Go."**

They cannot. Nobody can. **"That is what the rest of this term is about, and the thing that fixes it is the squash you just were."**

The typing survives; Week 17 uses all of it again.

---

## ✅ Assessing Understanding

Use this section to check, with exact wording, whether the lesson landed.

Three checks, five minutes, exact wording.

**Check 1 — one neuron, spoken (60 seconds)**

> "Weights are `0.4`, `−0.7`, `1.2`. Bias is `−0.5`. The row is `[1, 1, 1]`. **Give me `z`, and then tell me what a ReLU neuron says and what a tanh neuron says.**"

*Good answer:* "`0.4 − 0.7 + 1.2 − 0.5 = 0.40`. ReLU says `0.400` because it is positive. Tanh says `0.380`, which I would need the calculator for, but it is a bit less than `0.4` and definitely between −1 and 1."

**What to catch:** an answer of `1.1` — that is the three products added with the bias dropped. Do not correct it; ask *"how many numbers did you add?"* and wait.

**Check 2 — the shape, on paper (45 seconds)**

> "I have a grid with shape `(4, 3)`. **What is the shape of its transpose? How many numbers are in it? And name one shape I could reshape it to and one I could not.**"

*Good answer:* "Transpose is `(3, 4)`. Twelve numbers, because `4 × 3 = 12`. I could reshape it to `(2, 6)` or `(6, 2)` or `(12, 1)`. I could not do `(5, 3)`, because that is fifteen cells and I only have twelve."

**Full marks needs the multiplication.** A student who names a legal shape without saying `4 × 3 = 12` has pattern-matched. Ask *"how do you know?"*

**Check 3 — the collapse (spoken, 90 seconds)**

> "I build a network with three hidden layers and no squash anywhere. I train it perfectly. **What kind of thing have I built, and how would you convince me in three lines?**"

*Good answer:* "A straight line — one weighted sum of the inputs plus one bias. I'd substitute each layer into the next and collect the terms, and everything with an `x` in it collects into one weight per input. We did it with two layers and got `1.1x₁ + 0.4x₂ + 0.3`. And I'd show you a row: with no squash it gave `2.1`, with ReLU it gave `0.6`."

**What to catch:** "it wouldn't work very well." That is not the answer. It is not that it works *badly* — it is that it is **exactly** a single layer, no better and no worse. Push once: *"how much worse than one layer?"* The answer is *"not worse at all — identical."*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot get `z` without help; drops the bias. Reads `(3, 2)` as "three point two" or cannot say which number is the rows. Thinks the squash makes the numbers tidier. |
| **2 — Emerging** | Computes `z` correctly when the four terms are written out for them. Applies ReLU. Reads a shape off a printout when asked. Can say "you need a squash" without saying why. |
| **3 — Secure** | Computes `z` and all three squashes for a new row, unaided, with a calculator. Predicts a shape before running and is usually right. Reproduces the three-line collapse and states that two layers become one. **This is the target.** |
| **4 — Strong** | Gets eight shape predictions out of eight, including the `(3,)` trailing-comma case. Distinguishes `.T` from `.reshape` by their **contents**, not just their shape. Explains ReLU's advantage with the number `0.25` and the multiplication `0.25⁵`. Diagnoses `The truth value of an array is ambiguous` without help. |
| **5 — Exceptional** | Explains that the collapse is *exact* — a no-squash network is not a worse network, it is identically a linear one. Notices that ReLU's slope at exactly zero is a library decision rather than a mathematical fact. Predicts that stacking sigmoids will multiply small slopes together **before** being told, and connects it to why very deep sigmoid networks were hard to train. Designs a bias that silences the neuron on every row and can say how they found it. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, two jobs, and the second one has an unusual instruction so listen for it.
>
> **First, workbook M2 and Build It Part A — six rows, three squashes, eighteen numbers.** Same judge as today: weights `0.4`, `−0.7`, `1.2`, bias `−0.5`. Six new rows. For each one: work out `z`, then ReLU, then sigmoid, then tanh, **in pen, on the page**. Then write `b5w16.py` (B5), run it, and put a **tick or a cross** beside every one of the eighteen in the Build It table. **I want to see crosses.** Eighteen ticks with no working is a page I do not believe.
>
> **Second, Build It Part B — eight shapes, and here is the unusual bit. Write your prediction for all eight BEFORE you run anything.** In pen. Then run the script once, and for every one you got wrong, write **one line** saying what you had thought and what was actually true.
>
> That one line is what I am marking. Not the right answer — the sentence about the miss. If you got all eight right first time, tell me which one you were least sure about and why."

**Workbook split (the old page-number split no longer applies — the workbook is organised by section, not by page):** **in class**, only M4 is on the desks (face down, for the activity's collapse moment); **at home, required:** M2, then B5 (`b5w16.py`), then **Build It Part A and Part B**; **at home, next tier** (for the student who finishes early, or over a longer week): M1, M3, M4, P1–P4 and the Warm-Up; **the rest** — Practice Sets A and B (B1–B4), Fix the Broken Program, Puzzle of the Week, Think Deeper, Draw It, the Build It stretch and Bug Log, and Self-Check — is the extended set, to be chosen by the student or assigned across the week. There is no `make_moons` section in the workbook; the ninety-second look is done in class only.

**Expected time:** 35 min on the eighteen numbers with a calculator (M2 and Build It Part A) · 20 min on the eight shapes and the miss-sentences (Build It Part B). **About 55 minutes** — allow extra if B5 is the first program the student has written from a spec; the next tier adds roughly another hour (estimate, not timed).

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — is `z` right on all six rows?** A wrong `z` makes all three squashes wrong, so mark `z` first and do not penalise a correct squash of a wrong `z` twice. **Two — are there crosses in the Build It Part A table?** Eighteen unmarked ticks means the hand answers were written after the run, which is the one thing the page exists to prevent. **Three — do the "if I missed it, why" sentences in Build It Part B name a *reason*?** *"I put `(2, 3)` and it was `(3, 2)`"* is a correction, not a sentence. The one that earns full marks is *"I read the columns first — rows come first"*, or *"I forgot that transposing a flat list does nothing because there is nothing to flip."* A student whose eight sentences all say "I got it wrong" has done the page and missed the point, and that is worth one line of feedback: **"tell me what you were thinking, not what you scored."**

---

## 🔑 Answer Key

**This key follows the shipped student workbook (`workbook/week-16.md`) section by section and item by item** — Warm-Up, Do the Maths by Hand (M1–M4), Predict the Output (P1–P4), Practice Set A (A1–A6), Practice Set B (B1–B5), Fix the Broken Program, Puzzle of the Week, Think Deeper (T1–T2), Build It, Draw It and Self-Check — using the workbook's own labels, so you can mark from this page alone. The workbook has sections, not numbered pages; **there is no "Page 16.N" anywhere in it.** Values are taken from the workbook's own Answers section at the end of the file, and the arithmetic has been re-checked. Where the lesson itself needs a longer script or table (the eighteen numbers, the eight shapes, the chapter's collapse, the slopes table, the error snippets, `make_moons`), it sits under the workbook item it serves.

### Warm-Up

*Five questions about last week (Week 15, gradient descent from scratch). Not taught again this week, so expect some rust.*

| Item | Answer | What to listen for |
|---|---|---|
| **W1** | **One number per knob.** A model with three knobs has a gradient of three numbers — a **list**, not a single value. `[−0.375, +0.125, 0.000]` is a gradient. | "How many" is *the number of weights*. A student who says "one" has forgotten that a gradient is a list. |
| **W2** | Because **the gradient points uphill** and you want to go down. Subtracting takes you the opposite way to the slope. Write `+` and the loss climbs, smoothly and forever. | The word *uphill*. |
| **W3** | `−ln(0.5) = 0.693147`. Every weight starts at zero, so every score is zero, so every probability is `0.5`. **It is the loss of a model that is guessing.** | The blank is `0.5`. |
| **W4** | The `−` in `w -= lr * grad` has become a `+`. **One character.** A loss that rises *smoothly* with a sensible learning rate is this bug and essentially nothing else — a bad learning rate makes it jump about, not climb tidily. | "Sign of the update line". |
| **W5** | **The model's.** The loop is correct and converged; the model draws a **straight line** (it predicts "late" when `z ≥ 0`, the equation of a line) and the data is not straight. **That is the reason Weeks 16 to 19 exist.** | Blaming the model, with the word *straight*. |

### Do the Maths by Hand

*Calculator only, no code. M1 is counting; M2 to M4 are the arithmetic the shape is wrapped around.*

#### M1 — count the shape off the printout

| grid | shape | how many numbers |
|---|---|---|
| `P` | **(4, 2)** | **8** |
| `Q` | **(2, 3)** | **6** |
| `R` | **(4, 1)** | **4** |
| `S` | **(1, 6)** | **6** |
| `T` | **(3,)** | **3** |
| `U` | **(1, 1)** | **1** |

**M1(a).** **`T`, which is `(3,)`.** The lone comma is Python saying *"this shape has exactly one number in it"* — three numbers, flat, with no rows and columns at all. It is not a typo and not a printing bug. (The question says "only one number *in the shape*"; a student who answers `U` has read it as "one number in the grid" — `U` is `(1, 1)`, two numbers in its shape.)

**M1(b).** `(1, 8)`, `(2, 4)`, `(4, 2)`, `(8, 1)` — **anything whose two numbers multiply to 8** (and `(8,)` if flat shapes are allowed).

**M1(c).** `3 × 3 = 9` and `P` has **8**. numpy will not invent a ninth number, so it refuses.

**Marking tip.** The commonest M1 slip is writing columns first — `P` as `(2, 4)`. Ask them to count with a finger going *down* first.

#### M2 — six neuron outputs, three squashes, eighteen numbers (also Build It Part A)

*Weights `w = [0.4, −0.7, 1.2]`, bias `b = −0.5`. For each row: `z` first, then the three squashes to three decimal places. These are the rows in the student workbook's M2 and Build It Part A.*

**The `z` arithmetic, shown in full for every row:**

| Row | The four terms | `z` |
|---|---|---|
| `[1, 0, 1]` | `0.4 + 0.0 + 1.2 − 0.5` | **1.10** |
| `[0, 1, 2]` | `0.0 − 0.7 + 2.4 − 0.5` | **1.20** |
| `[3, 2, 0]` | `1.2 − 1.4 + 0.0 − 0.5` | **−0.70** |
| `[2, 0, 0.5]` | `0.8 + 0.0 + 0.6 − 0.5` | **0.90** |
| `[−1, −1, 0]` | `−0.4 + 0.7 + 0.0 − 0.5` | **−0.20** |
| `[0.5, 1.5, 1]` | `0.2 − 1.05 + 1.2 − 0.5` | **−0.15** |

**The eighteen squash answers, with the sigmoid arithmetic spelled out:**

| Row | `z` | ReLU | sigmoid | how sigmoid was got | tanh |
|---|---|---|---|---|---|
| `[1, 0, 1]` | 1.10 | **1.100** | **0.750** | `e^(−1.1) = 0.332871`; `1 ÷ 1.332871 = 0.750260` | **0.800** |
| `[0, 1, 2]` | 1.20 | **1.200** | **0.769** | `e^(−1.2) = 0.301194`; `1 ÷ 1.301194 = 0.768525` | **0.834** |
| `[3, 2, 0]` | −0.70 | **0.000** | **0.332** | `e^(0.7) = 2.013753`; `1 ÷ 3.013753 = 0.331812` | **−0.604** |
| `[2, 0, 0.5]` | 0.90 | **0.900** | **0.711** | `e^(−0.9) = 0.406570`; `1 ÷ 1.406570 = 0.710950` | **0.716** |
| `[−1, −1, 0]` | −0.20 | **0.000** | **0.450** | `e^(0.2) = 1.221403`; `1 ÷ 2.221403 = 0.450166` | **−0.197** |
| `[0.5, 1.5, 1]` | −0.15 | **0.000** | **0.463** | `e^(0.15) = 1.161834`; `1 ÷ 2.161834 = 0.462570` | **−0.149** |

**The check script, and its real output:**

```python
"""homework_check.py - eighteen numbers, checked."""
import numpy as np

np.random.seed(0)

w = np.array([0.4, -0.7, 1.2])
b = -0.5

rows = np.array([[1.0, 0.0, 1.0],
                 [0.0, 1.0, 2.0],
                 [3.0, 2.0, 0.0],
                 [2.0, 0.0, 0.5],
                 [-1.0, -1.0, 0.0],
                 [0.5, 1.5, 1.0]])

sigmoid = lambda z: 1.0 / (1.0 + np.exp(-z))

print("%-20s %8s %8s %9s %8s" % ("row", "z", "ReLU", "sigmoid", "tanh"))
for r in rows:
    z = (r * w).sum() + b
    print("%-20s %8.2f %8.3f %9.3f %8.3f"
          % (str(r), z, np.maximum(0, z), sigmoid(z), np.tanh(z)))
```

```text
row                         z     ReLU   sigmoid     tanh
[1. 0. 1.]               1.10    1.100     0.750    0.800
[0. 1. 2.]               1.20    1.200     0.769    0.834
[3. 2. 0.]              -0.70    0.000     0.332   -0.604
[2.  0.  0.5]            0.90    0.900     0.711    0.716
[-1. -1.  0.]           -0.20    0.000     0.450   -0.197
[0.5 1.5 1. ]           -0.15    0.000     0.463   -0.149
```

**Three things worth a comment when you mark this.** Row 6's `z` is `−0.15`, a whisker below zero — **ReLU says `0.000` and tanh says `−0.149`, and a student who wrote `0.000` for tanh has confused the two.** Row 5 and row 6 have the same ReLU answer (`0.000`) from different negative `z` values (`−0.20` and `−0.15`); ReLU threw away two different numbers and nobody downstream can tell. And three of the six ReLU answers are `0.000`, which is not a mistake — **it is what a picky neuron does a lot of the time.** A common slip on the sigmoid column is to skip the negate and get `1 − sigmoid(z)` (row 1 would read `0.250` rather than `0.750`).

**M2(b).** **Three** negatives: `−0.604`, `−0.197`, `−0.149`. **All three are in the tanh column.** ReLU's floor is a hard zero. Sigmoid's floor is zero too, and it never even reaches it — it squeezes everything into the gap between 0 and 1. **Tanh is the only one of the three allowed to say "actively bad".**

**M2(c).** Row 5 lost **`−0.20`** and row 6 lost **`−0.15`**. **No, you cannot get either back.** Both arrive at the next layer as `0`, and nothing downstream can tell them apart — or tell either from `−47.5`. That is exactly the point of T1.

**Eight-place values, for anyone checking a calculator properly:**

```text
z =  1.1000  relu=1.100000  sig=0.75026011  tanh= 0.80049902
z =  1.2000  relu=1.200000  sig=0.76852478  tanh= 0.83365461
z = -0.7000  relu=0.000000  sig=0.33181223  tanh=-0.60436778
z =  0.9000  relu=0.900000  sig=0.71094950  tanh= 0.71629787
z = -0.2000  relu=0.000000  sig=0.45016600  tanh=-0.19737532
z = -0.1500  relu=0.000000  sig=0.46257015  tanh=-0.14888503
```

#### M3 — how steep is each squash, by nudging

**Sigmoid at `z = 1.0`:**

```text
e^(−1.001) = 0.367512,  so  sigmoid(1.001) = 1 ÷ 1.367512 = 0.73125515
e^(−0.999) = 0.368248,  so  sigmoid(0.999) = 1 ÷ 1.368248 = 0.73086192

it moved:  0.73125515 − 0.73086192 = 0.00039323
we moved:  0.002

0.00039323 ÷ 0.002 = 0.196615
```

The chapter's table says **`0.196612`**, and Python with every digit gets `0.196612`. **Accept anything from `0.196` to `0.197`.**

> **⚠️ Watch out:** the thing being subtracted is about **four ten-thousandths**. A student who rounds the two sigmoids to four places first (`0.7313` and `0.7309`) gets `0.0004 ÷ 0.002 = 0.2`, which is wrong in the second digit. **When you subtract two nearly-equal numbers, every digit thrown away earlier comes back magnified.** Keep eight places on this item.

**M3(a).** `tanh(1.001) = 0.76201381`, `tanh(0.999) = 0.76117386`:

```text
(0.76201381 − 0.76117386) ÷ 0.002 = 0.00083995 ÷ 0.002 = 0.419975
```

**`0.419974` to six places** — the chapter's number for tanh at `z = 1.0`. **About twice as steep as sigmoid at `z = 1`** (and four times as steep at `z = 0`): tanh wins in the middle and loses at the edges.

**M3(b).** **No calculator needed, and the answer is `1`.** ReLU at `z = 1` is firing, and while it fires it repeats its input exactly — nudge the input up by a thousandth and the output goes up by a thousandth. `0.002 ÷ 0.002 = 1`.

**M3(c).** `0.25⁵ = 0.0009765625` — about **one thousandth** of the signal survives five sigmoid layers. `1⁵ = 1` — **all** of it. That one comparison is the main reason ReLU is the default (not the only one: it is also cheap).

**The lesson's own slopes script and table** (the chapter's Trick 4; it gives the same `0.196612` and `0.419974` and the answers to the chapter questions below):

*Measure the steepness of each squash by nudging, then answer the three questions.*

```python
"""slopes.py - why ReLU is the default hidden activation."""
import numpy as np

np.random.seed(0)
sigmoid = lambda z: 1.0 / (1.0 + np.exp(-z))
h = 0.001

print("%6s %12s %12s %12s" % ("z", "sigmoid slope", "tanh slope", "ReLU slope"))
for z in [0.0, 1.0, 2.0, 5.0, 10.0]:
    s = (sigmoid(z + h) - sigmoid(z - h)) / (2 * h)
    t = (np.tanh(z + h) - np.tanh(z - h)) / (2 * h)
    r = (np.maximum(0, z + h) - np.maximum(0, z - h)) / (2 * h)
    print("%6.1f %12.6f %12.6f %12.6f" % (z, s, t, r))

print()
print("five sigmoid layers stacked: 0.25 ** 5 =", 0.25 ** 5)
print("five ReLU    layers stacked: 1.00 ** 5 =", 1.0 ** 5)
```

```text
     z sigmoid slope   tanh slope   ReLU slope
   0.0     0.250000     1.000000     0.500000
   1.0     0.196612     0.419974     1.000000
   2.0     0.104994     0.070651     1.000000
   5.0     0.006648     0.000182     1.000000
  10.0     0.000045     0.000000     1.000000

five sigmoid layers stacked: 0.25 ** 5 = 0.0009765625
five ReLU    layers stacked: 1.00 ** 5 = 1.0
```

**Q1 — "What is the steepest sigmoid ever gets, and where?"**
**`0.25`, at `z = 0`.** Everywhere else it is less. That is a hard ceiling.

**Q2 — "Multiply five sigmoid slopes together at their very best. What survives?"**
`0.25 × 0.25 × 0.25 × 0.25 × 0.25 = 0.0009765625` — **about one thousandth.** And that is the *best* case; at `z = 5` a single layer already contributes `0.0066`, so five of those would be about `1.3e-11`. Five ReLU layers give `1 × 1 × 1 × 1 × 1 = 1` — **all of it.**

**Q3 — "Why is ReLU's slope `0.500000` at `z = 0`?"**
Because ReLU has a **corner** there and a corner has no single steepness. Nudge up and the slope is 1; nudge down and it is 0; the two-sided nudge averages them to `0.5`. **This is a place where the maths genuinely has no answer and every library makes a documented decision** — PyTorch, in Week 20, will report `0`. A student who writes *"there isn't one answer, so somebody chose"* has understood something most textbooks skip.

**One honest note for marking:** the tanh column at `z = 0` says `1.000000`, which is **four times steeper than sigmoid**. So why is tanh not the default? Because it flattens out just as badly further along — by `z = 5` it is `0.000182`, *worse* than sigmoid. Tanh is better near the middle and worse at the edges. ReLU never flattens at all on the side that fires, and that is the whole argument.

#### M4 — prove the collapse, in three lines

*The workbook uses a **new** network (not the chapter's), so a student cannot copy the class proof.*

```text
h1 =  0.2·x₁ + 1.5·x₂ − 0.4
h2 =  0.6·x₁ − 0.9·x₂ + 0.2
out = 2.0·h1 + 1.0·h2 − 0.1

out = 2.0(0.2x₁ + 1.5x₂ − 0.4) + 1.0(0.6x₁ − 0.9x₂ + 0.2) − 0.1

x₁ terms:        0.4 + 0.6 = 1.0
x₂ terms:        3.0 − 0.9 = 2.1
plain numbers:  −0.8 + 0.2 − 0.1 = −0.7

out = 1.0·x₁ + 2.1·x₂ − 0.7
```

**M4(a).** On `x = [3.0, 2.0]`:

```text
two layers:  h1 = 0.2(3) + 1.5(2) − 0.4 = 0.6 + 3.0 − 0.4 = 3.20
             h2 = 0.6(3) − 0.9(2) + 0.2 = 1.8 − 1.8 + 0.2 = 0.20
             out = 2.0(3.20) + 1.0(0.20) − 0.1 = 6.4 + 0.2 − 0.1 = 6.50

one line:    out = 1.0(3) + 2.1(2) − 0.7 = 3.0 + 4.2 − 0.7 = 6.50
```

**They agree. Exactly** — the same function written two ways.

**M4(b).** On `x = [1.0, 4.0]` with ReLU on `h1` and `h2`:

```text
h1 = 0.2(1) + 1.5(4) − 0.4 = 0.2 + 6.0 − 0.4 =  5.80
h2 = 0.6(1) − 0.9(4) + 0.2 = 0.6 − 3.6 + 0.2 = −2.80    ← h2 gets binned

with ReLU:  out = 2.0(5.80) + 1.0(0) − 0.1 = 11.60 − 0.1 = 11.50
no squash:  out = 2.0(5.80) + 1.0(−2.80) − 0.1 = 11.6 − 2.8 − 0.1 = 8.70
the gap:    11.50 − 8.70 = 2.80
```

**M4(c).** **The gap is exactly the contribution that got thrown away.** `h2` was `−2.80` and its weight into the output is `1.0`, so binning it removed `1.0 × (−2.80) = −2.80` from the answer, which *raised* the answer by `2.80`. **ReLU bends the line because it cuts some rows and leaves others alone; a rule that behaves differently in different places is not a straight line.**

**Marking tip.** If `x₁` and `x₂` collect wrongly here, B4's gap column will not be zero — the student has a built-in check. The usual slip is sign: `1.0 × (−0.9x₂)` collected as `+0.9`.

**The chapter's own collapse** (the one proved in class with `h1 = 0.5x1 + 0.8x2 + 0.1`, used by A6(e), T1 and the activity; `collapse.py` in the Prep Checklist is this file):

*Two layers, no squash. Substitute and simplify.*

```text
h1 =  0.5·x1 + 0.8·x2 + 0.1
h2 = -0.3·x1 + 0.2·x2 + 0.05
out = 1.0·h1 - 2.0·h2 + 0.3
```

**Line 1 — substitute:**

```text
out = 1.0(0.5x1 + 0.8x2 + 0.1) - 2.0(-0.3x1 + 0.2x2 + 0.05) + 0.3
```

**Line 2 — multiply out both brackets.** The `−2.0` flips every sign inside the second one:

```text
out = 0.5x1 + 0.8x2 + 0.1 + 0.6x1 - 0.4x2 - 0.1 + 0.3
```

**Line 3 — collect:**

```text
x1:      0.5 + 0.6  =  1.1
x2:      0.8 - 0.4  =  0.4
numbers: 0.1 - 0.1 + 0.3  =  0.3

out = 1.1·x1 + 0.4·x2 + 0.3
```

**One weighted sum, one bias, one straight line.**

*Now the check with numbers, for `x = [2.0, −1.0]`:*

```text
h1 = 0.5(2.0) + 0.8(-1.0) + 0.1  = 1.0 - 0.8 + 0.1  =  0.30
h2 = -0.3(2.0) + 0.2(-1.0) + 0.05 = -0.6 - 0.2 + 0.05 = -0.75

no squash:  out = 1.0(0.30) - 2.0(-0.75) + 0.3 = 0.30 + 1.50 + 0.30 = 2.10
one line:   out = 1.1(2.0) + 0.4(-1.0) + 0.3   = 2.20 - 0.40 + 0.30 = 2.10
with ReLU:  h2 -> 0, so out = 0.30 - 0 + 0.30 = 0.60

the gap:    2.10 - 0.60 = 1.50
```

**The script, and its real output:**

```python
"""collapse.py - with no squash, two layers are one straight line."""
import numpy as np

np.random.seed(0)
np.set_printoptions(precision=6, suppress=True)

def two_layers_no_squash(x1, x2):
    h1 = 0.5 * x1 + 0.8 * x2 + 0.1
    h2 = -0.3 * x1 + 0.2 * x2 + 0.05
    return 1.0 * h1 - 2.0 * h2 + 0.3

def one_straight_line(x1, x2):
    return 1.1 * x1 + 0.4 * x2 + 0.3

def two_layers_with_relu(x1, x2):
    h1 = np.maximum(0, 0.5 * x1 + 0.8 * x2 + 0.1)
    h2 = np.maximum(0, -0.3 * x1 + 0.2 * x2 + 0.05)
    return 1.0 * h1 - 2.0 * h2 + 0.3

tests = [(2.0, -1.0), (1.0, 2.0), (0.0, 0.5), (-1.0, -1.0), (3.0, 3.0)]

print("%-14s %14s %14s %10s %14s" % ("(x1, x2)", "two layers", "one line", "gap", "with ReLU"))
for x1, x2 in tests:
    a = two_layers_no_squash(x1, x2)
    b = one_straight_line(x1, x2)
    c = two_layers_with_relu(x1, x2)
    print("%-14s %14.6f %14.6f %10.6f %14.6f"
          % ("(%.1f, %.1f)" % (x1, x2), a, b, abs(a - b), c))

gaps = [abs(two_layers_no_squash(a, b) - one_straight_line(a, b)) for a, b in tests]
print()
print("biggest disagreement between two layers and one line:", max(gaps))
```

```text
(x1, x2)           two layers       one line        gap      with ReLU
(2.0, -1.0)          2.100000       2.100000   0.000000       0.600000
(1.0, 2.0)           2.200000       2.200000   0.000000       2.200000
(0.0, 0.5)           0.500000       0.500000   0.000000       0.500000
(-1.0, -1.0)        -1.200000      -1.200000   0.000000       0.000000
(3.0, 3.0)           4.800000       4.800000   0.000000       4.300000

biggest disagreement between two layers and one line: 4.440892098500626e-16
```

**Three things to point at in that table.** The `gap` column is `0.000000` on **every** row — the two-layer network and the single line are not "close", they are the same function. The last line says the biggest disagreement anywhere is `4.44e-16`, which is **zero as far as a computer is concerned**; it is the same rounding wobble that makes `0.1 + 0.2` print as `0.30000000000000004`. And the `with ReLU` column disagrees on **three of the five rows** — rows `(2.0, −1.0)`, `(−1.0, −1.0)` and `(3.0, 3.0)` — which is precisely the network doing something a line cannot.

### Predict the Output

*Prediction in pen first. One of the four prints something that is not a shape and is not a number either (P4 line 4, `()`).*

**P1.**

```text
(3,)
(3,)
(3, 1)
(1, 3)
```

**Lines 1 and 2 are identical.** `a.T` did nothing at all, and there was **no error**. A flat `(3,)` has no rows and columns to swap, so transposing it is a no-op. **To get a column you must make it 2-D first:** `a.reshape(3, 1)`.

**P2.**

```text
[1 3 5]
[1 2 3]
False
```

**Same shape, different grid.** `G.T` reads **down the columns** of the original — one, three, five. `G.reshape(2, 3)` reads **along the rows** — one, two, three. `np.array_equal` compares the *contents*, not the shape, so it says `False`. **Shape is not identity.**

**P3.**

```text
[0.  0.2 0.7]
0.7
(3,)
```

**`np.maximum`** compares **two things, cell by cell**, and returns a grid the same shape as what went in — it is the ReLU. **`np.max`** looks *inside one array* and returns **the single largest number in it**. Two letters apart, completely different jobs, and mixing them up is a real bug that does not crash.

**P4.**

```text
(2, 3)
(2,)
(3,)
()
```

**Line 1 keeps six numbers** because `rows * w` is a **cell-by-cell** multiply: each row's three values are paired against the three weights, giving three products **per row**. Nothing has been added yet. The adding is `.sum(axis=1)`, line 2, which turns six products into two weighted sums.

**Line 4 is `()`** — an **empty** shape, because `.sum()` with no axis adds up *everything* and gives back a single number with no rows and columns. On its own, `(rows * w).sum()` prints **`-1.0999999999999999`** — the total of all six products, `0.7 + (−1.8) = −1.1`, with the usual binary wobble on the last digit.

**Scoring line:** "How many of the answers on this page did you get right? ___ / 14" (P1 has four lines, P2 three, P3 three, P4 four). Accept the student's own count and ask which one surprised them — usually P1 line 2 or P4 line 4.

### Practice Set A

**A1.** neuron → **(vii)** · pre-activation `z` → **(iv)** · activation `a` → **(i)** · ReLU → **(v)** · tanh → **(viii)** · layer → **(iii)** · hidden layer → **(vi)** · MLP → **(ix)** · shape → **(ii)**

**A2.** The spam-filter printout (`w = [0.9, 1.4, −0.6]`, `b = −1.5`, four texts):

| Question | Answer |
|---|---|
| a | **Four texts, three features each** — that is what `(4, 3)` says, rows first |
| b | Because `w` was built from a flat list with no inner brackets. It is **one weight per feature, in a line** — not a grid. `(3,)` and `(3, 1)` hold the same three numbers but behave differently |
| c | One **feature**, across all four texts. Row 0 of `rows.T` is every text's exclamation-mark count. **Same twelve numbers, a different question** |
| d | **Both had a negative `z`** — `−3.3` and `−0.7`. ReLU silences anything negative |
| e | **`−0.997283` and `−0.604368`, both from tanh.** It is the only squash of the three that can go below zero |
| f | Because there are **four rows**, and a neuron produces **one number per row**. One `z` per text |

**A2(g).** `3 × (−0.6) + (−1.5) = −1.8 − 1.5 = −3.3`. Three shouted words, each weighted `−0.6`, plus the grumpy bias. The blanks are **`−0.6`** and **`−1.5`**.

**A2(h).** **Tanh's `−0.997283`.** ReLU says *"nothing"* and sigmoid says *"very unlikely"*, but both are small positive numbers or zero. Tanh says **"actively, definitely not spam"** — it has a direction, not only a size.

**A3.**

| # | What happens | The fix |
|---|---|---|
| a | `TypeError: 'tuple' object is not callable`. `.shape` is a **property**, not a function | drop the brackets: `rows.shape` |
| b | `ValueError: The truth value of an array with more than one element is ambiguous` | `np.maximum(0, z)` — it asks the question once per cell |
| c | `AttributeError: 'list' object has no attribute 'shape'`. A plain Python list has no shape | wrap it: `np.array([0.4, -0.7, 1.2])` |
| d | `ValueError: cannot reshape array of size 6 into shape (4,2)`. `4 × 2 = 8`, and there are 6 | any shape multiplying to 6: `(2,3)`, `(3,2)`, `(1,6)`, `(6,1)` |
| e | `ValueError: operands could not be broadcast together with shapes (n,3) (4,)`. Four weights, three columns | delete the fourth weight. **One weight per column, always** |
| f | **No error, and nothing happens.** `a` is flat `(3,)`, so there is nothing to flip and `col` has the same shape and numbers as `a` | `a.reshape(3, 1)`, or `a.reshape(1, 3).T` |

**A3(g).** **f.** Nothing crashes, `col` looks plausible, and the shape is quietly still `(3,)`. **How you would notice: `print(col.shape)`** — this week's whole reflex, and f is the reason it exists.

**A4.** i → **R** · ii → **T** · iii → **Q** · iv → **P** · v → **S**

**A4(f).** **`Q` (`[-0.9800964]`)**: ReLU cannot return a negative number and sigmoid lives strictly between 0 and 1, so neither could have made it. It must be **tanh**. (`S`, `[0.5]`, is sigmoid's answer at `z = 0`.)

**A5.** The eight boxes of the "Label the neuron" figure, in order:

| # | the step | answer |
|---|---|---|
| 1 | `1.0 × 0.4` | **0.4** |
| 2 | `0.0 × (−0.7)` | **0.0** |
| 3 | `1.0 × 1.2` | **1.2** |
| 4 | the bias `b` | **−0.5** |
| 5 | `z` = add rows 1–4 | **1.10** |
| 6 | `ReLU(z)` | **1.100** |
| 7 | `sigmoid(z)` | **0.750** |
| 8 | `tanh(z)` | **0.800** |

Underneath: `w.shape` is **`(3,)`**, six rows of three is **`(6, 3)`**, and the squash that can return a negative number is **tanh**.

**A5(a).** **Box 2, the product `0.0 × (−0.7)`.** It is zero because the **input** was zero, not because anything squashed it. `w₂ = −0.7` is perfectly alive — it simply had nothing to multiply. **An absent input contributes nothing, whatever its weight.**

**A5(b).** **Boxes 4, 5, 6, 7 and 8** — every box from the bias downwards. Boxes 1 to 3 are input × weight and have nothing to do with `b`. Without the bias, `z` would be `1.60` and all three squash answers would change.

**A6.**

**a)** **multiply each input by its own weight**, **add the products plus a bias**, **squash the total**.

**b)** `z` is the number **before** the squash and can be **any number at all — `−40`, `0`, `6000`**; `a` is the number **after** the squash.

**c)** `(4, 3)` means **4** rows and **3** columns, and **rows come first**.

**d)** `.T` reads **down the columns** and `.reshape` reads **along the rows**. Same shape out, **different numbers** inside.

**e)** With no squash, two layers are **one layer, written out the long way**, and the chapter's single line is `out = 1.1·x₁ + 0.4·x₂ + 0.3`.

**f)** ReLU's slope is **1** everywhere it fires, while sigmoid's steepest is ever **0.25** — and `0.25⁵` is about a thousandth.

### Practice Set B

**B1.**

```python
import numpy as np

z = np.array([-2.3, 0.2, 0.7])
print(np.maximum(0, z), np.maximum(0, z).shape)
```

```text
[0.  0.2 0.7] (3,)
```

**B2.**

```python
import numpy as np

w = np.array([0.4, -0.7, 1.2])
b = -0.5
x = np.array([1.0, 0.0, 1.0])

z = (x * w).sum() + b

print("z       = %.2f" % z)
print("ReLU    = %.6f" % np.maximum(0, z))
print("sigmoid = %.6f" % (1.0 / (1.0 + np.exp(-z))))
print("tanh    = %.6f" % np.tanh(z))
```

```text
z       = 1.10
ReLU    = 1.100000
sigmoid = 0.750260
tanh    = 0.800499
```

`0.4 + 0 + 1.2 − 0.5 = 1.10`. **If they wrote `1.10` on the page first, tick it.**

**B3.**

```python
import numpy as np

rows = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 2.0]])
w = np.array([0.4, -0.7, 1.2])

print("%-22s %s" % ("rows", rows.shape))
print("%-22s %s" % ("rows.T", rows.T.shape))
print("%-22s %s" % ("w", w.shape))
print("%-22s %s" % ("w.reshape(3, 1)", w.reshape(3, 1).shape))
print("%-22s %s" % ("np.maximum(0, rows)", np.maximum(0, rows).shape))
```

```text
rows                   (2, 3)
rows.T                 (3, 2)
w                      (3,)
w.reshape(3, 1)        (3, 1)
np.maximum(0, rows)    (2, 3)
```

**B3(a).** **Yes, those two are the same grid here** — but only because every number in this `rows` is already zero or positive. `np.maximum(0, rows)` squashes **every cell in place**, so the shape is untouched and no number moves; with a negative cell the *value* would change to `0` but would still sit in the same place. It is `.T` and `.reshape` that give the same shape with the numbers *moved*. **A squash never changes a shape; a rearrangement never changes the count.**

**B4.**

```python
import numpy as np

def two_layers_no_squash(x1, x2):
    h1 = 0.2 * x1 + 1.5 * x2 - 0.4
    h2 = 0.6 * x1 - 0.9 * x2 + 0.2
    return 2.0 * h1 + 1.0 * h2 - 0.1

def one_line(x1, x2):
    return 1.0 * x1 + 2.1 * x2 - 0.7

for x1, x2 in [(3.0, 2.0), (1.0, 4.0), (-2.0, 0.5)]:
    a = two_layers_no_squash(x1, x2)
    b = one_line(x1, x2)
    print("(%.1f, %.1f)  two layers %9.6f   one line %9.6f   gap %.6f"
          % (x1, x2, a, b, abs(a - b)))
```

```text
(3.0, 2.0)  two layers  6.500000   one line  6.500000   gap 0.000000
(1.0, 4.0)  two layers  8.700000   one line  8.700000   gap 0.000000
(-2.0, 0.5)  two layers -1.650000   one line -1.650000   gap 0.000000
```

**Three rows, three zeros.** If **one** row disagrees, the `x₁` or `x₂` collection in M4 has a slip; if **all three** disagree, the plain numbers were collected wrongly.

**B5.** The program the student writes is their own; this is the reference `b5w16.py`, with the answer-key hand answers typed in:

```python
"""b5w16.py - six rows through one neuron, three squashes, marked against my paper."""
import numpy as np

np.random.seed(0)
np.set_printoptions(precision=6, suppress=True)

w = np.array([0.4, -0.7, 1.2])
b = -0.5

rows = np.array([[1.0, 0.0, 1.0],
                 [0.0, 1.0, 2.0],
                 [3.0, 2.0, 0.0],
                 [2.0, 0.0, 0.5],
                 [-1.0, -1.0, 0.0],
                 [0.5, 1.5, 1.0]])

# my eighteen hand answers, in the order ReLU, sigmoid, tanh
by_hand = [[1.100, 0.750, 0.800],
           [1.200, 0.769, 0.834],
           [0.000, 0.332, -0.604],
           [0.900, 0.711, 0.716],
           [0.000, 0.450, -0.197],
           [0.000, 0.463, -0.149]]

print("w.shape    =", w.shape)
print("rows.shape =", rows.shape)
print()
print("%-20s %7s %8s %9s %8s" % ("row", "z", "ReLU", "sigmoid", "tanh"))
worst = 0.0
misses = 0
for i in range(len(rows)):
    r = rows[i]
    z = (r * w).sum() + b
    got = [float(np.maximum(0, z)), 1.0 / (1.0 + np.exp(-z)), float(np.tanh(z))]
    print("%-20s %7.2f %8.3f %9.3f %8.3f" % (str(r), z, got[0], got[1], got[2]))
    for k in range(3):
        mine = by_hand[i][k]
        theirs = got[k]
        gap = abs(mine - theirs)
        worst = max(worst, gap)
        if gap > 0.0005:
            misses += 1
print()
print("numbers checked      : 18")
print("misses (gap > 0.0005): %d" % misses)
print("biggest gap          : %.6f" % worst)
```

```text
w.shape    = (3,)
rows.shape = (6, 3)

row                        z     ReLU   sigmoid     tanh
[1. 0. 1.]              1.10    1.100     0.750    0.800
[0. 1. 2.]              1.20    1.200     0.769    0.834
[3. 2. 0.]             -0.70    0.000     0.332   -0.604
[2.  0.  0.5]           0.90    0.900     0.711    0.716
[-1. -1.  0.]          -0.20    0.000     0.450   -0.197
[0.5 1.5 1. ]          -0.15    0.000     0.463   -0.149

numbers checked      : 18
misses (gap > 0.0005): 0
biggest gap          : 0.000499
```

**Mark the student's own program, not a copy of this one:** it must set the seed and print options, print `w.shape` and `rows.shape`, use **their** hand answers (not these), and count a miss as a gap **greater than** `0.0005`. Three misses from honest hand slips is the program doing its job.

**"Try this".** At a threshold of `0.0001` several numbers "miss" — `0.800` against `0.80049902` is a gap of `0.000499`. **Nothing is wrong.** Rounding to three places can be off by up to `0.0005` by definition, so a threshold *tighter* than that asks three-place answers to be four-place answers. **The threshold has to match the precision you wrote down.**

### Fix the Broken Program

*`broken16.py`, four rows through one neuron. Three bugs — a shape bug, a runtime bug, a silent logic bug.*

**Bug 1 — line 7, `w = np.array([0.4, -0.7, 1.2, 0.9])`. A shape bug.** (The error surfaces on line 21, `z_all = ...`, but the fault is the fourth weight.)

The message names `(4,3)` and `(4,)`. **The `3` counts the feature columns in `rows`** — each row has three numbers. **The `4` counts the weights supplied.** One weight per column, always, so the fourth weight has nothing to multiply and numpy stops. *(The nasty part: `rows` also has four **rows**, so the `4` on the right is **not** the `4` on the left. Read what each number counts, not where it sits.)*

**The fix:** `w = np.array([0.4, -0.7, 1.2])`.

**Bug 2 — line 16, `return max(0, z)`. A runtime bug.** (It fires from the call on line 23.)

Python's built-in `max` asks **one** yes-or-no question — *"is this one bigger?"* — and the student handed it **four** numbers at once, so *"is `[0.7, −1.8, 1.2, 0.9]` bigger than zero"* has no single answer. The two blanks on the page are **one** question and **four** numbers.

**The fix:** `return np.maximum(0, z)`. **Built-in Python functions work on one thing; numpy functions work on every cell.**

**Bug 3 — lines 21 and 27: `+ b` is missing from both.** A silent logic bug.

Every `z` in the Run 3 table is exactly **`0.5` too big**: `0.70` instead of `0.20`, `−1.80` instead of `−2.30`, `1.20` instead of `0.70`, `0.90` instead of `0.40`. `0.5` is the size of the bias, and the bias is negative, so leaving it out raises every score. **The two guilty lines are `z_all = (rows * w).sum(axis=1)` and `z = (r * w).sum()`.**

**The fix:** `+ b` on both. (Fixing only one gives a program whose two printouts disagree, which is its own kind of horrible.) The Run 4 table confirms it: `z_all = [0.2 −2.3 0.7 0.4]`.

**Ranking by time cost: bug 3 ≫ bug 2 ≈ bug 1.** Bugs 1 and 2 crash on the spot and the message names the exact problem — one prints both shapes, the other prints the offending line. Bug 3 produces a program that runs, prints a tidy table, and is wrong in eleven of the twelve squash numbers (row 2's ReLU is `0.000` either way). **Only a hand-checked row or a table to compare against catches it.**

**Could you spot it from `sigmoid(z)` alone?** **Yes, but only by doing arithmetic.** The sigmoid column is `0.668, 0.142, 0.769, 0.711`, and nothing about those looks wrong — they are all sensible probabilities. You would have to **take one row and compute `z` by hand**: `2×0.4 + 1×(−0.7) + 0.5×1.2 − 0.5 = 0.20`, then `sigmoid(0.20) = 0.550`, which is not `0.668`. **One hand-checked row is the whole defence.**

**Bug Log entry (Build It):** bug 3 is the new category — *no error, no crash, every number wrong.*

#### The stand-alone error snippets used in class

*These are the lesson's live-code versions of the same three messages (and of A3 b, d, e, f). They are not workbook items; use them if a student needs the error shown on its own.*

*Run each broken snippet, paste the real message, name the two numbers in it, fix it.*

**Error 1 — Python's `max` on a grid.**

```python
import numpy as np
z = np.array([-2.3, 0.2, 0.7])
print(max(0, z))
```

```text
Traceback (most recent call last):
  File "bad_max.py", line 3, in <module>
    print(max(0, z))
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

**What it means:** `max` asked one yes-or-no question — "is this bigger?" — about three numbers at once, and there is no single answer.
**The fix:** `np.maximum(0, z)` → `[0.  0.2 0.7]`. It asks the question once per cell.

**Error 2 — a reshape that cannot exist.**

```python
import numpy as np
G = np.array([[1, 2], [3, 4], [5, 6]])
print(G.reshape(4, 2))
```

```text
Traceback (most recent call last):
  File "bad_reshape.py", line 3, in <module>
    print(G.reshape(4, 2))
ValueError: cannot reshape array of size 6 into shape (4,2)
```

**The two numbers:** `size 6` (what there is) against `(4,2)`, which needs `4 × 2 = 8` cells.
**The fix:** any shape whose two numbers multiply to 6 — `G.reshape(2, 3)`, `(6, 1)`, `(1, 6)` or `(3, 2)`.

**Error 3 — one weight too many.**

```python
import numpy as np
rows = np.array([[2.0, 1.0, 0.5], [-1.0, 2.0, 0.0]])
w = np.array([0.4, -0.7, 1.2, 0.9])
print((rows * w).sum(axis=1))
```

```text
Traceback (most recent call last):
  File "bad_bcast.py", line 4, in <module>
    print((rows * w).sum(axis=1))
ValueError: operands could not be broadcast together with shapes (2,3) (4,) 
```

**The two numbers:** the `3` in `(2,3)` — three columns of data — against the `4` in `(4,)` — four weights.
**The fix:** delete the fourth weight. **One weight per column, always.** And the diagnosis is `print(rows.shape, w.shape)`, which is this week's reflex.

**A fourth, for anybody who wants it — the one that gives no error at all:**

```python
import numpy as np
a = np.array([1.0, 2.0, 3.0])
print("a.shape   =", a.shape)
print("a.T.shape =", a.T.shape)
print("a.reshape(1, 3).T.shape =", a.reshape(1, 3).T.shape)
```

```text
a.shape   = (3,)
a.T.shape = (3,)
a.reshape(1, 3).T.shape = (3, 1)
```

**Nothing crashed and nothing happened.** Transposing a flat list does nothing, because a flat list has no rows and columns to swap. To get a column you must make it 2-D first. **This is the silent one, and it is the one that will bite in Week 17.**

### Puzzle of the Week

**Part 1 — which squash made this?**

| # | `z` | answer | which squash | why |
|---|---|---|---|---|
| 1 | −3.0 | 0.000 | **ReLU** | sigmoid gives `0.047`, tanh gives `−0.995`. Only ReLU is exactly 0 |
| 2 | 0.0 | 0.500 | **sigmoid** | ReLU gives 0, tanh gives 0 |
| 3 | 2.0 | 0.964 | **tanh** | ReLU gives 2.000, sigmoid gives 0.881 |
| 4 | 1.5 | 1.500 | **ReLU** | it repeated its input, which only ReLU does |
| 5 | −1.0 | −0.762 | **tanh** | it is negative |
| 6 | 0.0 | 0.000 | **ReLU or tanh** | both give exactly 0 at `z = 0` |

**Part 1(a).** **ReLU and tanh.** `ReLU(0) = 0` and `tanh(0) = 0` — they agree at exactly one point, and that is the point given. **One measurement is not always enough to identify a function**; the cure is a second, different `z`.

**Part 1(b).** Because **the answer is negative**, and only one of the three squashes may return a negative number. The *sign* is the whole diagnosis.

**Part 1(c).** `ReLU = 2.000`, `sigmoid = 0.881`, `tanh = 0.964`. ReLU is ruled out because it would have repeated `2.0` exactly; sigmoid because `0.881 ≠ 0.964`. **Both were ruled out by arithmetic, not by taste.**

**Part 2 — the Mystery Judge.**

**Part 2(a).** The row `[0, 0, 0]` feeds **nothing** in, so every weight is multiplied by zero. **Whatever comes out must be the bias, on its own.** It is the row to start with because it isolates one unknown — and it is why the bias exists: the only knob with an opinion about an empty row.

**Part 2(b).** `b = −0.20`. Then each other row is one weight plus the bias:

```text
w₁ + (−0.20) =  0.30  →  w₁ =  0.50
w₂ + (−0.20) = −0.40  →  w₂ = −0.20
w₃ + (−0.20) =  1.50  →  w₃ =  1.70
```

**Part 2(c).** `z = 2(0.50) + 1(−0.20) + 1(1.70) − 0.20 = 1.00 − 0.20 + 1.70 − 0.20 = 2.30`.

`ReLU = 2.300` · `sigmoid = 0.909` · `tanh = 0.980`. *(`e^(−2.3) = 0.100259`, so `1 ÷ 1.100259 = 0.908877`.)*

**Part 2(d).** **They are wrong.** Three rows give three equations in **four** unknowns — the three weights and the bias — one short. With only `[1,0,0]`, `[0,1,0]`, `[0,0,1]` you would know `w₁ + b`, `w₂ + b`, `w₃ + b`, so you could find the **differences** between weights but never any one of them. **The empty row is not a spare; it is the fourth equation.**

**Part 2(e).** **Rows 2 and 4 become useless.** Their `z` values are `−0.40` and `−0.20`, so after a ReLU both would be recorded as `0.000`, and *any* negative number produces `0.000`; `w₂` and `b` could no longer be recovered, only known to be negative. **What to do: feed rows that push `z` positive, or ask for `z` instead of `a`.** For `w₂` feed a *negative* input, e.g. `[0, −5, 0]`, giving `z = (−0.20)(−5) − 0.20 = 0.80`. For `b`, use `[0, 0, 1]` and `[0, 0, 2]` (`1.50` and `3.20`), whose difference gives `w₃ = 1.70` and then `b = 1.50 − 1.70 = −0.20`. **A squash that clips is a squash that destroys evidence** — the same fact as T1.

### Think Deeper

**T1 — a model answer.** It is a cost *and* a bend, and the measurement shows the bend. With no squash, the chapter's two-layer network is exactly `1.1x₁ + 0.4x₂ + 0.3` — a straight line, however many layers are stacked. Put ReLU back in and the row `[2.0, −1.0]` goes from `2.10` to `0.60`. **That gap of `1.50` exists only because ReLU cut something off for that row and not for others.** If the cutting were uniform — everything halved, say — it would still be a line. **The bend comes from the rule behaving differently in different places.**

**A squash that keeps all its information can still bend.** Sigmoid and tanh never throw anything away — each output traces back to exactly one input — and neither is a straight line, so a network built from them does *not* collapse. So losing information is not what makes a squash useful: **not being a straight line is.** ReLU happens to bend by cutting, and that cut has a real cost: a unit whose `z` is negative on *every* row is permanently silent and (its slope being zero there) gets no training signal to revive it — the "dead ReLU", met properly in Week 19. **For ReLU the cut is the bend, and the price is that some units can die.**

**T2 — a model answer.** With `double(z) = 2z` between the layers:

```text
h1 = 0.5x₁ + 0.8x₂ + 0.1      →  double →  1.0x₁ + 1.6x₂ + 0.2
h2 = −0.3x₁ + 0.2x₂ + 0.05    →  double → −0.6x₁ + 0.4x₂ + 0.10

out = 1.0(1.0x₁ + 1.6x₂ + 0.2) − 2.0(−0.6x₁ + 0.4x₂ + 0.10) + 0.3
    = (1.0 + 1.2)x₁ + (1.6 − 0.8)x₂ + (0.2 − 0.2 + 0.3)
    = 2.2x₁ + 0.8x₂ + 0.3
```

**Still one straight line.** The collapse happens exactly as before; `double` only doubled two of the three coefficients, which different weights could have done anyway.

So the property a squash must have is **not** "makes numbers smaller" and **not** "keeps numbers in a range". It is: **it must not be a straight line itself.** `2z` is a straight line through the origin, so a layer of it composes with its neighbours into another line. ReLU is two straight pieces with a **corner**, and the corner is the point — which row you are on decides which piece you get, something no single line can imitate.

**"Squashing" is a slightly misleading word.** Sigmoid and tanh squash, into `(0,1)` and `(−1,1)`. ReLU does not squash on the side that fires — it repeats its input exactly, with no ceiling. **The honest name for what all three share is "not a straight line"** — *non-linearity*. **Put a bend in it, or depth is free money you cannot spend.**

**Marking tip.** Full marks need all of: the `2.10`/`0.60` numbers used, a clear statement that sigmoid can bend without losing information (T1), and the worked `2.2x₁ + 0.8x₂ + 0.3` with the word *straight* (T2). A T2 that says "yes it still collapses" with no algebra shown is half marks.

### Build It

*Two parts. Part A is about being wrong in pen; Part B is about being right before you run anything.*

**Part A — the eighteen numbers.** The table is in **M2** above, to three and eight decimal places. Marking notes:

- **`z` first.** If the student's `z` is wrong, all three squashes on that row are wrong and it counts as **one** mistake, not three — but they write three crosses, because that is what a marker sees. On the workbook page, "how many of the eighteen did it poison?" has the answer **three** per bad `z`.
- **The column that causes most crosses is usually sigmoid**, because it needs four calculator presses in order: negate, `e^x`, `+1`, `1/x`. Skipping the negate gives `1 − sigmoid(z)`; row 1 would read `0.250` rather than `0.750`. **If the sigmoid column looks like one minus the right answer, that is the slip.**
- **"Zero crosses with no working" is not believed.** The page exists to make the hand column come *before* the run.
- A cross is a gap over `0.0005` against numpy (the same test `b5w16.py` applies), so a hand answer rounded carelessly in the third place is a genuine cross.

**Part B — the eight shapes.** The workbook table has columns *my prediction · what it printed · ✓/✗ · if I missed it, why — one line*; the real answers are below (predictions, real output, and why), with the script:

*Write all eight predictions in pen first. Then run once. Item 4 is a deliberate error.*

| # | Expression | Prediction | Real | Why |
|:--:|---|---|---|---|
| 1 | `A.shape` (`A = [[1, 2, 3], [4, 5, 6]]`) | `(2, 3)` | **`(2, 3)`** | Two rows, three columns. Rows first. |
| 2 | `A.T.shape` | `(3, 2)` | **`(3, 2)`** | Rows become columns: `[[1 4], [2 5], [3 6]]`. |
| 3 | `A.reshape(3, 2).shape` | `(3, 2)` | **`(3, 2)`** | Same shape as #2, **different grid**: `[[1 2], [3 4], [5 6]]`. It reads along the rows. |
| 4 | `A.reshape(4, 2)` | *(not a shape)* | **`ValueError: cannot reshape array of size 6 into shape (4,2)`** | `4 × 2 = 8` but `A` holds 6 numbers. numpy will not invent two or throw two away. |
| 5 | `v.shape` (`v = [2.0, 4.0, 6.0]`) | `(3,)` | **`(3,)`** | Flat: three numbers, no rows and columns. One number in the shape, hence the trailing comma. |
| 6 | `v.T.shape` | `(3,)` | **`(3,)`** | Nothing to flip in a flat list, so transposing does nothing, silently. |
| 7 | `v.reshape(3, 1).shape` | `(3, 1)` | **`(3, 1)`** | `3 × 1 = 3`, so it is legal. One tall column. |
| 8 | `(rows * w).sum(axis=1).shape` | `(6,)` | **`(6,)`** | Six rows in, one weighted sum per row, so six numbers in a flat list. |

**The script, and its real output:**

```python
"""shapes8.py - eight shapes, predicted in pen first."""
import numpy as np
np.random.seed(0)

A = np.array([[1, 2, 3],
              [4, 5, 6]])
v = np.array([2.0, 4.0, 6.0])
w = np.array([0.4, -0.7, 1.2])
rows = np.array([[1.0, 0.0, 1.0],
                 [0.0, 1.0, 2.0],
                 [3.0, 2.0, 0.0],
                 [2.0, 0.0, 0.5],
                 [-1.0, -1.0, 0.0],
                 [0.5, 1.5, 1.0]])

print("1. A.shape                       =", A.shape)
print("2. A.T.shape                     =", A.T.shape)
print("3. A.reshape(3, 2).shape         =", A.reshape(3, 2).shape)
print("5. v.shape                       =", v.shape)
print("6. v.T.shape                     =", v.T.shape)
print("7. v.reshape(3, 1).shape         =", v.reshape(3, 1).shape)
print("8. (rows * w).sum(axis=1).shape  =", (rows * w).sum(axis=1).shape)
print()
print("4. A.reshape(4, 2) ->")
print(A.reshape(4, 2))
```

```text
1. A.shape                       = (2, 3)
2. A.T.shape                     = (3, 2)
3. A.reshape(3, 2).shape         = (3, 2)
5. v.shape                       = (3,)
6. v.T.shape                     = (3,)
7. v.reshape(3, 1).shape         = (3, 1)
8. (rows * w).sum(axis=1).shape  = (6,)

4. A.reshape(4, 2) ->
Traceback (most recent call last):
  File "shapes8.py", line 25, in <module>
    print(A.reshape(4, 2))
ValueError: cannot reshape array of size 6 into shape (4,2)
```

**The ones that are supposed to catch people, and what a good miss-sentence looks like.** Items 5 and 6 are the silent pair: `v` is flat, so `v.T` has no rows and columns to swap and quietly returns the same `(3,)`. A good sentence: *"I thought transposing would make it a column, but a flat list has nothing to flip."* Items 2 and 3 both print `(3, 2)` and are different grids; a student who assumes `.T` and `.reshape` give the same thing has only compared the shapes, not the contents. Item 4 is the only non-shape: the last line of the traceback is the answer, and the arithmetic `4 × 2 = 8` against 6 numbers is what refused it. A good sentence for item 8: *"I expected `(6, 3)` because I was multiplying a grid, but `sum(axis=1)` collapses each row to one number."*

**Item 4's last line, verbatim:** `ValueError: cannot reshape array of size 6 into shape (4,2)`. The arithmetic: `4 × 2 = 8` against `A` holding **6** numbers. **numpy will not invent two numbers and will not throw two away.**

**Items 5 and 6, in one sentence:** *"`v` is flat — `(3,)` — so there are no rows and columns to swap, and transposing it does nothing at all, silently."*

**Items 2 and 3 are the pair worth noticing.** Both print `(3, 2)` and **they are different grids**: `A.T` is `[[1 4], [2 5], [3 6]]` and `A.reshape(3, 2)` is `[[1 2], [3 4], [5 6]]`.

**The sentence being marked:**

> *"The shape is two numbers that say how the data is laid out, and almost every array bug is a disagreement between two shapes — so printing it first turns a mysterious crash into arithmetic I can do in my head."*

**Accept** any answer naming *diagnosis*, *the two clashing numbers*, or *"it tells me what the error message is about to tell me"*. **Do not accept** *"so I know how big it is"* — size is not the point; **agreement** is.

**Stretch — the silent neuron.**

```text
with no bias at all, the four class rows give z = 0.70, −1.80, 1.20, 0.90
so the biggest is 1.20, and any bias below −1.20 silences every row

b = −1.3:   z = [−0.6, −3.1, −0.1, −0.4]   ReLU = [0, 0, 0, 0]    silent on all four  ✅
b = −1.0:   z = [−0.3, −2.8,  0.2, −0.1]   ReLU = [0, 0, 0.2, 0]  not silent          ❌
```

The two blanks are **`1.20`** and **`−1.20`**. *(These `z` values use `w = [0.4, −0.7, 1.2]` on the chapter's four rows `[2,1,0.5]`, `[−1,2,0]`, `[0,0,1]`, `[1,1,1]`.)*

**Bug or waste?** **Waste, on this data.** Not a bug — the neuron does exactly what its numbers say — but it contributes nothing to any prediction. **Worse than waste: because ReLU's slope is zero there, no gradient ever reaches it, so no training wakes it up.** That is Week 19's "dead ReLU", and the student has just built one on purpose.

**The Bug Log** (two entries): any two real ones. Expect the "no error, every number wrong" row to be bug 3 of Fix the Broken Program (missing `+ b`), and a shape row such as the `(4,3)`/`(4,)` broadcast message. Full marks need the *cause* and *fix* columns filled, not just "what I saw".

### Draw It

**A good drawing has:** three input wires, each labelled with both its value and its weight (`2.0` with `×0.4`, `1.0` with `×−0.7`, `0.5` with `×1.2`); the **bias on its own fourth wire with no input attached to it**; the three products written out (`0.8`, `−0.7`, `0.6`); the running total ending at **`z = 0.20`**; a box for the squash with **the rule inside it**, not just the name — *"negatives become zero, positives come through"*; the activation `a = 0.200` leaving on the right; and the two shapes `(3,)` and `(4, 3)` in a corner.

**The four questions.** **Three wires in, three weights on them** — a fourth weight drawn on the bias wire is the commonest slip; the bias is not multiplied by anything. **The bias attaches to nothing**; that is why it can have an opinion about an empty row. **Inside the squash box: a rule, not a name** — "ReLU" tells a reader nothing, "negatives → 0" tells them everything. And **`z = 0.20` is before the box, `a = 0.200` is after it.** A drawing with only one number there is half a neuron.

### Self-Check

No right answers; the honest bar: 😀 means you could do it now on a blank sheet with nothing open, 🙂 with the chapter beside you, 😕 is the one to ask about first. Make sure **"count the shape off a printout, rows first"** is not a 😕, because next week is nothing but shapes, and the week after that is shapes with transposes in them. The last row ("read `ValueError: cannot reshape array of size 6 into shape (4,2)` and fix it in ten seconds") should be a 😀 by the end of Fix the Broken Program.

### Not in the workbook — the `make_moons` first look

*Used only in the last ninety seconds of class (🔑 Wrap & Assign) and as the hook for Weeks 17–19. The shipped workbook has no `make_moons` section; this is a teacher demonstration and an optional stretch for a student who asks for a longer look.*

*Load it, print the shapes, plot it, and answer one question with a ruler.*

```python
"""moons_look.py - a first look at the data a straight line cannot split."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons

np.random.seed(0)

X, y = make_moons(n_samples=400, noise=0.25, random_state=0)

print("X.shape =", X.shape)
print("y.shape =", y.shape)
print("first three rows of X:")
print(X[:3])
print("first three labels  :", y[:3])
print("class counts        :", np.bincount(y))

fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(X[y == 0, 0], X[y == 0, 1], marker="o", label="class 0")
ax.scatter(X[y == 1, 0], X[y == 1, 1], marker="^", label="class 1")
ax.set_xlabel("feature 1")
ax.set_ylabel("feature 2")
ax.set_title("make_moons(n_samples=400, noise=0.25, random_state=0)")
ax.legend()
fig.tight_layout()
plt.savefig("moons.png", dpi=110)
print("saved moons.png")
```

```text
X.shape = (400, 2)
y.shape = (400,)
first three rows of X:
[[-0.49511301  0.96602758]
 [ 1.71424117 -0.49933902]
 [ 1.3702969  -0.37944818]]
first three labels  : [0 1 1]
class counts        : [200 200]
saved moons.png
```

**Runtime: about 1 second**, including saving the figure.

**Q — "Lay a ruler on the picture. What is the best you can do with one straight line, and roughly how many points does it get wrong?"**

**No straight line separates them.** Two hundred of each class, hooked together like two links of a chain. The best single line gets somewhere around **85–88%** — a student who eyeballs "about fifty wrong" is in the right area, and the exact number does not matter. What matters is the reason: **the boundary that would work is curved, and a weighted sum plus a bias can only ever draw something straight.**

**Two details worth noticing in that printout.** `y.shape` is `(400,)` — flat, not `(400, 1)`, the same flat-list point as `v` in Build It Part B. And `np.bincount(y)` gives `[200 200]`, so the classes are perfectly balanced and **accuracy is a fair measure here** — which will not be true of the fraud data from Term 1, and it is worth one sentence connecting the two.

### Answers to every question posed in the lesson

**Hook — "Add them up. Out loud, left to right."**
`0.8 − 0.7 = 0.1`; `0.1 + 0.6 = 0.7`; `0.7 − 0.5 = 0.20`. **`z = 0.20`.**

**Hook — "Why does she have that separate grumpy card? What would change if it were zero?"**
The bias is the neuron's **threshold** — how much the features have to earn before it says anything. With `b = −0.5` the features must total more than `0.5`. With `b = 0` the threshold is pinned at exactly zero, which is one arbitrary choice out of infinitely many. Demonstrate with row `[0, 0, 1]`: `z = 0.70` with the bias, `z = 1.20` without.

**Concept — "ReLU judge. What does she say?" (on `z = −2.30`)**
**Nothing — `0.000`.** ReLU flattens every negative to zero.

**Concept — "One of those twelve numbers is negative. Which, and what does that tell you?"**
Tanh's `−0.980`. **Only tanh can return a negative number**; ReLU's floor is zero and sigmoid's floor is zero-but-never-reached. That is the one practical difference between sigmoid and tanh.

**Concept — "How many rows, and how many numbers across?"**
Three rows, two columns. **`(3, 2)`.** Rows first, always.

**Concept — "Both of those are `(2, 3)`. So are they the same grid?"**
No. `G.T` reads down the original's columns and gives `1 3 5 / 2 4 6`. `G.reshape(2, 3)` reads along the rows and gives `1 2 3 / 4 5 6`. **Same shape, different contents.**

**Live-code — "`(3,)`. There is a comma and then nothing. Is that a typo?"**
No. It is a shape with exactly **one** number in it, meaning a flat list with no rows and columns. Python writes the trailing comma so it cannot be mistaken for a number in brackets.

**Live-code — "'The truth value of an array is ambiguous.' What is Python complaining about?"**
It was asked one yes-or-no question about four numbers at once. `max(0, z)` compares two things; `np.maximum(0, z)` compares cell by cell and hands back a grid.

**Live-code — "Read the message. It names two numbers. What are they and why do they disagree?"**
`size 6` — the numbers that exist — against `shape (4,2)`, which needs eight cells. Reshape cannot invent or discard numbers.

**Activity — "Count the layers in that answer." (`out = 1.1x₁ + 0.4x₂ + 0.3`)**
**One.** There is no `h` in the expression: it is a single weighted sum of the two inputs, plus one bias.

**Activity — "Two point one against nought point six. Where did the difference go?"**
ReLU set `h2` from `−0.75` to `0`, so the `−2.0 × (−0.75) = +1.50` contribution vanished. **`2.10 − 1.50 = 0.60`.** Cutting that value for some rows and not others is exactly how ReLU bends the network.

**Wrap — "Separate the two crescents with one straight line."**
Impossible. That is the question the next four weeks answer, and the answer is built from the squash they met today.

---

## 🔮 Next Week Preview

Next week the neuron gets multiplied — literally. Doing sixteen neurons one at a time with a Python loop is unbearably slow, and it turns out a **whole layer for a whole batch of rows is one operation**: a grid times a grid, written `A @ B`. The lesson is built around one rule and one failure. The rule is **the inner two numbers must match and the outer two survive**: `(3,2) @ (2,4) → (3,4)`. The failure is the shape mismatch, which is the error message the class will see more than any other for the rest of the year — so they will produce it five times on purpose and learn to read the two numbers in it. The activity is **Shape Dominoes**: twelve shape pairs on index cards, sorted into "these multiply" and "these do not", with the answer shape written on the back of every card in the first pile.

**To prep early:** write the **twelve Shape Dominoes cards** tonight, one shape pair per index card, and leave the backs blank. Eight that work: `(3,2)×(2,4)`, `(4,2)×(2,3)`, `(4,3)×(3,1)`, `(1,3)×(3,1)`, `(3,1)×(1,3)`, `(2,2)×(2,2)`, `(16,750)×(750,1)`, `(2,750)×(750,16)`. Four that do not: `(2,4)×(3,2)`, `(2,3)×(1,4)`, `(3,1)×(5,2)`, `(750,2)×(16,1)`. Keep **today's four-row table and the collapse line `out = 1.1x₁ + 0.4x₂ + 0.3` on the wall** — next week's forward pass uses the same `0.5, 0.8, −0.3, 0.2` weights and the same `1.0, −2.0` output weights, extended by one hidden unit, so the numbers will look familiar on purpose. Nothing new to install.
