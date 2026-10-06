# Week 25 — Work Out the Size Before You Run It

[⬅ Week 24](week-24.md) · [Course Home](../README.md) · [Week 26 ➡](week-26.md) · [Student Guide](../student-guide/week-25.md) · [Workbook](../workbook/week-25.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one division, done on paper, that stops the commonest error in this whole level |
| **Big idea** | Every conv and pool layer changes height and width by a rule you can do on paper. **If you cannot do it on paper, the shape error will find you** — and the error will print two numbers, one of which you typed yourself. |
| **New vocabulary** | stride · padding · max pooling · receptive field · flatten |
| **New maths** | **The output-size rule: `(n + 2p − k) ÷ s + 1`, rounded down.** Derived by counting window positions on an 8×8 grid by hand *before* the formula is written down. That is the only new maths this week, and it is one division. |
| **New syntax** | `nn.Conv2d(..., stride=2, padding=1)` · `nn.MaxPool2d(2)` · `nn.Flatten()` · `t.view(t.size(0), -1)` |
| **Dataset** | 8×8 pictures **written inline with numpy** — a half-bright bar you type in four lines — plus `load_digits()` reshaped to `(1797, 1, 8, 8)` if you get to the stretch. **Nothing downloads. No internet needed. No torchvision.** |
| **Materials** | **Squared paper for everybody, and a pen — not a pencil** · printed workbook pages 25.1–25.7 · a big sheet on the wall headed **THE SHAPE LADDER** with six blank rows · the PARAMETER COUNT sheet from Week 22, still up · the Bug Log · a strip of card 3 squares wide per student (the "window") |
| **Tech needed** | Laptop with Python 3, numpy, **torch**. Torch has been installed since Week 20. **No new installs.** |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `shapes.py` and `sizes.py` are both **instant** — under a second each. Nothing trains this week. |

> **⚠️ Watch out:** the whole lesson turns on the order of two things. **Count the window positions with a card on squared paper FIRST. Write the rule down SECOND.** If you write `(n + 2p − k) ÷ s + 1` on the board before anybody has slid a card along a row of eight squares, you have handed a 14-year-old four letters to memorise, and they will memorise them wrong and be unable to check themselves for the rest of the level. **The rule is a shortcut for a count. Do the count.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Count the window positions** of a 3-wide window on 8 squares by hand — sliding a card, writing down the start columns — and then **derive the rule from what they counted**, not from a formula they were given.
2. **Apply `(n + 2p − k) ÷ s + 1`, rounded down**, to twelve layer configurations and match every printed shape, explaining any miss.
3. **Predict all six shapes** through an 8×8 → conv → pool → conv → pool → flatten stack **in pen, before running it**, and read the real error when one prediction is wrong.
4. **Explain what padding is for and what stride 2 costs you**, each in one sentence with a number in it.

Observable evidence: a sheet of squared paper with six pencilled window positions and the count `6` circled; workbook page 25.1 with six shapes written **in pen** before any code ran, and the printed shape written beside each; twelve hand-computed output sizes with the printed number beside each; and one real traceback pasted into the Bug Log with the numbers `64` and `32` circled and labelled *"picture"* and *"mine"*.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is one new piece of mathematics this week and it is a division.** If you can work out "how many 3-square windows fit along 8 squares" you already know it. What takes fifteen minutes of your prep is not the maths; it is understanding *why a wrong answer here produces a specific error message with two specific numbers in it*, because that is what you will be debugging in the room.

### 1. The thing that makes this week necessary

Last week the student learned that a **convolution** slides a small grid of weights over a picture and writes down one number at each position. They did it by hand on a 6×6 with a 3×3 kernel and got a 4×4 answer.

They probably did not notice that **6 became 4**.

They will notice this week, because this week they stack layers, and the sizes compound. Put a conv on an 8×8 and you get a 6×6. Pool that and you get a 3×3. Conv that and you get a 1×1. Do it once more and PyTorch stops and shouts at you. The single most common error in this entire level looks like this, and here it is, copied from a real run:

```text
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**Two numbers.** `64` and `32`. One of them came from the picture, by arithmetic you could have done on paper. The other one you typed. **The whole lesson is: know which is which.**

![The error names two numbers. Only one is yours.](../figures/fig-w25-5-two-numbers-in-the-error.svg)
*Figure 25.1 — The error names two numbers. Only one is yours. The 64 came out of the picture; the 32 you typed, so the 32 is the one to change.*

That figure is the one to look at hardest during your prep. **It is also the answer to "but why do we need the rule?"** — because without it you cannot tell which of the two numbers in the error message to change, so you guess, and guessing costs twenty minutes per bug for the rest of the level.

### 2. The rule, derived by counting — do this yourself, on paper, now

Get a sheet of squared paper. Draw a row of **8 squares**. Cut a strip of card **3 squares wide**. This is the whole derivation and it takes two minutes.

Put the card at the far left, so it covers squares 0, 1, 2. That is **one** position. Slide it right by one square: 1, 2, 3. **Two.** Keep going:

```
start 0  covers 0 1 2
start 1  covers 1 2 3
start 2  covers 2 3 4
start 3  covers 3 4 5
start 4  covers 4 5 6
start 5  covers 5 6 7
```

Now the card is hanging off the end. **Six positions.** So a 3-wide window on 8 squares gives an answer that is **6 long**.

![Count the places a 3-wide window fits](../figures/fig-w25-1-window-positions-counted-on-a-grid.svg)
*Figure 25.2 — Count the places a 3-wide window fits. Six positions, counted; the rule is a shortcut for that count.*

**Now — and only now — write the arithmetic that gets you 6 without sliding the card.** The last legal start is 5. Why 5? Because the window is 3 wide, so its last square is at 5 + 2 = 7, which is the last square there is. So the last start is `8 − 3 = 5`. And the starts run 0, 1, 2, 3, 4, 5 — which is **`5 + 1 = 6` of them**, because counting from zero always gives you one more than the last number.

```
8 − 3 = 5        the last place the window can start
5 + 1 = 6        there are six starts, counting the one at zero
```

**That `+ 1` is the whole reason people get this wrong, and it is worth saying out loud twice: you add one because you counted the start at zero.** It is the same `+1` as "there are 11 fence posts in a 10-metre fence".

Now two knobs, one at a time.

**Stride.** The **stride** is how far the window jumps between positions. So far it jumped 1. Make it jump 2 and you only use the starts 0, 2, 4 — **three** positions, not six.

```
8 − 3 = 5        the last place it could start
5 ÷ 2 = 2.5      how many 2-square jumps fit into that
round down → 2   you cannot take half a jump
2 + 1 = 3        three positions, counting the one at zero
```

**Rounding down is not a subtlety, it is the point.** You cannot take two and a half steps. In Python `//` does this for you, and in the formula it is written `floor`.

![Stride 2 halves the output](../figures/fig-w25-3-stride-two-halves-the-output.svg)
*Figure 25.3 — Stride 2 halves the output. Six starts become three; the picture did not shrink, you just looked at it half as often.*

**Padding.** The **padding** is a ring of zeros you glue around the outside of the picture before you slide anything. With one ring, an 8×8 becomes a 10×10, so:

```
(8 + 2) − 3 = 7      note the 2: one ring adds one square on EACH side
7 ÷ 1 = 7
7 + 1 = 8            the answer comes out the same size as the picture
```

**`k=3` with `p=1` and `s=1` keeps the size exactly the same, and that is why almost every real network uses it.** It means you can stack ten conv layers and the picture does not quietly evaporate.

Put the three together and you have the whole rule:

> **The output-size rule.** For a picture `n` squares across, a window `k` wide, jumping `s` at a time, with `p` rings of zeros around the outside:
>
> ```
> out = (n + 2p − k) ÷ s + 1,  rounded down
> ```
>
> Apply it to the height and to the width **separately**. It is the same rule for convolution and for pooling.

**Every letter, in one line each, in the order they appear:**

| Letter | Plain English | On our stack |
|---|---|---|
| `n` | how many squares across the picture is | 8 |
| `p` | how many rings of zeros you glued round it | 1 |
| `k` | how many squares wide the window is | 3 |
| `s` | how far the window jumps each step | 1 |

**And the four numbers you should be able to produce from memory by the end of the lesson**, because they cover almost everything:

| n | k | s | p | Arithmetic | out |
|---:|---:|---:|---:|---|---:|
| 8 | 3 | 1 | 0 | (8 + 0 − 3) ÷ 1 + 1 = 5 + 1 | **6** |
| 8 | 3 | 1 | 1 | (8 + 2 − 3) ÷ 1 + 1 = 7 + 1 | **8** ← same size in, same size out |
| 8 | 2 | 2 | 0 | (8 + 0 − 2) ÷ 2 + 1 = 3 + 1 | **4** ← halved |
| 8 | 3 | 2 | 1 | (8 + 2 − 3) ÷ 2 + 1 = 3.5 → 3, then + 1 | **4** ← also halved |

**Do all four with a calculator right now, before you teach them.** Ten seconds each. If you have not, you will fumble the rounding on row 4 in front of the room.

### 3. Why padding matters beyond size — and this is the "but why?" answer

There is a second reason for padding, and it is better than the first.

Without padding, count how many windows a **corner** pixel of an 8×8 sits inside. Just one: the window that starts at the corner. Now count for a pixel in the **middle**: nine.

**So the model gets nine times more evidence about the middle of the picture than about the corners.** Add one ring of zeros and the corner is now inside **four** windows instead of one. Still fewer than nine, but four times better.

```
padding 0:  corner pixel is in 1 window,  middle pixel is in 9
padding 1:  corner pixel is in 4 windows, middle pixel is in 9
```

![A ring of zeros lets the window reach the edge](../figures/fig-w25-2-padding-ring-of-zeros.svg)
*Figure 25.4 — A ring of zeros lets the window reach the edge. Same size in, same size out, and the corner gets four times the hearing it had.*

> **🧑‍🏫 If a student asks:** *"isn't adding fake zeros cheating?"* It is a real objection and the honest answer is **yes, a bit.** The zeros are not data; you made them up. Every border pixel's answer is partly computed from numbers nobody measured. That is a genuine, known cost, and it is why you sometimes see a faint frame effect around the edge of a feature map. The trade is: made-up zeros at the border, or the border barely counted at all. **Almost everybody takes the zeros. Nobody pretends it is free.**

### 4. Max pooling, in one paragraph and one worked grid

> **Max pooling** — slide a small window (almost always 2×2, jumping 2) and keep **only the biggest number** in each window. It has no weights at all: nothing to learn, nothing to train.

Here is the whole idea on sixteen numbers. Take this 4×4:

```
  4   1  |  0   2
  2   9  |  3   1
 --------+--------
  0   0  |  7   5
  1   3  |  6   8
```

Four windows of four. Biggest in each: 9, 3, 3, 8.

```
  9   3
  3   8
```

**Sixteen numbers became four, and the two loudest (the 9 and the 8) both survived.** That is the deal: you throw away *exactly where* the strong response was and keep *that there was one*. It costs you position and buys you two things — the tensor gets four times smaller, so the next layer is four times cheaper, and the network cares less about exactly where inside a block an edge was: pixel 4 or pixel 5 gives the same answer, as long as both sit in the same 2×2 block.

And the size check: `(4 + 0 − 2) ÷ 2 + 1 = 1 + 1 = 2`. **The same rule.** Say that out loud; students expect pooling to have its own rule and it does not.

### 5. Flatten, and the one place the shape rule earns its keep

At the end of a conv stack the data is a small block: `(4, 16, 2, 2)` — four pictures, sixteen feature maps each, two by two. But `nn.Linear` — which the student has known since Week 22 — wants **one flat row per example**.

> **Flatten** — squash every dimension except the batch into one long row. `(4, 16, 2, 2)` becomes `(4, 64)`, because `16 × 2 × 2 = 64`.

**That `64` is the number the whole lesson is for.** It is the number you must write into `nn.Linear(64, 10)`. Get it wrong and you get Figure 25.1.

There are two ways to write it and they do the same thing:

```python
nn.Flatten()                 # a layer you drop into the stack
t.view(t.size(0), -1)        # a method you call on the tensor
```

`t.size(0)` is "however many rows are in this batch — don't ask me, look". `-1` means "you work out the rest so the total number of numbers stays the same". **Both come out `(4, 64)`, and it is worth printing both once so nobody thinks they are different operations.**

### 6. Receptive field — vocabulary this week, arithmetic never

> **Receptive field** — how much of the *original* picture one cell of a later feature map can see.

One cell of the first conv's output looked at a 3×3 patch. After a pool, each cell covers a 2×2 area of those, so it now depends on about 4×4 of the original. After the second conv, about 8×8. After the second pool, about 10×10 — **which is bigger than the whole 8×8 picture.**

You do not need a formula for this and **you must not teach one**; there is one new piece of maths this week and it is the output-size rule. What you need is the empirical fact, which the stretch code prints: **switch on one pixel at a time and see which ones can change the top-left cell of the final 2×2 map.** The answer is the top-left 7×7 — **49 of the 64 pixels**, clipped by the edge of the picture.

Say it like this: *"by the last layer, one cell is looking at nearly the whole digit. That is part of why a stack of layers can use the whole digit, where one cell of a single conv layer sees only a 3×3 patch."*

### 7. The three misconceptions you will actually meet

**Misconception 1 — "the +1 is a fudge factor."**
It is the fence-post `+1` and nothing else. **Cure:** make them slide the card and *say the start numbers out loud* — "zero, one, two, three, four, five" — then ask "how many did you say?" Six. "And what was the last one?" Five. **The gap between 5 and 6 is the `+1`, and it is because counting started at zero.** Nobody who has said the numbers out loud gets this wrong again.

**Misconception 2 — "stride 2 shrinks the picture."**
It does not. The picture is exactly the same picture. **Stride 2 shrinks the ANSWER, because you looked at the picture half as often.** Cure: point at Figure 25.3 and cover the output block with your hand. The row of eight squares is identical in both bands. Only the number of triangles changed.

**Misconception 3 — "padding adds information."**
Padding adds *zeros*, and a zero is not information. What it buys is that the window can now be centred on an edge pixel, so edge pixels get counted more. **Cure:** the 1-versus-4-versus-9 counts in §3. Concrete, checkable, and it answers the objection honestly instead of dodging it.

### 8. How deep to go, and where to stop

**Go this far:** count the window positions with a card; derive the rule from the count; apply it with stride and padding; predict six shapes through a stack in pen; read one real shape error and identify which of its two numbers you typed.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **Training a CNN on digits.** Nothing trains this week and that is deliberate. | **Week 26, next week.** If somebody asks whether this thing can actually read a digit: *"next week, and it takes about three seconds."* |
| Rendering the learned filters as pictures | **Week 26.** |
| `nn.CrossEntropyLoss`, ten-class output, `argmax` | **Week 26.** Today the stack ends at `Flatten()` and one `Linear`, and we never even look at its output values. |
| The receptive-field recurrence (`RF + (k−1) × jump`) | **Nowhere in this level as a formula.** Teach the word and the empirical count. A second formula this week will cost you the first one. |
| `padding="same"` as a string | Not in this level. It exists and it works, but it hides the arithmetic, which is precisely today's subject. Mention it exists if asked, and say *"we are learning to do it ourselves first."* |
| Dilation, transposed convolution, `ceil_mode` | Not in this level. If a student finds `ceil_mode=True` in the docs, admire it and move on. |
| Average pooling | Mention in one line if asked — same rule, keeps the mean instead of the biggest. Do not build with it. |
| Batch normalisation | Not in this level. |

The line to hold in your head all lesson: **today the student learns that shapes are arithmetic, not luck.** Everything about *what the network learns* is next week.

---

### 9. 🧭 The Growing Map — the same box, and the quietest week in it

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week nothing moves and nothing trains, and the two minutes are spent defending that.

![The Level 3 pipeline in Week 25: still the images and CNNs tile, now the output-size rule done on paper](../figures/fig-w25-0-where-this-fits.svg)

*Figure 25.0 — Week 25's version. Second week inside the gold `images · CNNs` tile. The ↻ on stage three is
black, as it has been since Week 12 — though nothing went round it today.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "what is on the ladder?"** The box is the same gold tile as
   last week, *images · CNNs*. The answer to the second question is on the wall: **THE SHAPE LADDER**, six
   rows, filled in **in pen before anything ran**. *"That sheet is today. Six shapes, predicted, then
   checked."*
2. **Anchor it on the two circled numbers in the Bug Log.** Somebody's traceback has **64** and **32** in
   it, labelled *"picture"* and *"mine"*. Hold it up. *"One of those two numbers was typed by a person and
   one was worked out by the computer. Knowing which is which took us seventy minutes and one division,
   and it will save every one of you an afternoon before June."*
3. **Point at the ↻ and say why it is idle.** It is black — the loop has been open since Week 12 — but
   nothing went round it today, and that is deliberate. *"No weights moved today. We were measuring the
   pipe before we put water in it. Next week the same stack trains in three seconds, and it only trains
   because the number after `Flatten` is right."*

> **🧑‍🏫 Why this is worth two minutes.** A week with no training and no accuracy number feels to a student
> like a week that did not count, and the map is the fastest rebuttal there is: the gold box has not
> moved, so this was *inside* the work, not beside it. It is also worth saying plainly that the commonest
> error in the whole level is a shape error, and that professionals still get it — Figure 25.1 is somebody
> at work, weekly.

**One thing to notice, so you can answer if asked.** Only **one** thread is lit — `representation`, alone.
Say why if asked, because it is precise: nothing was modelled, nothing was measured, nothing was steered.
The only thing that changed today is **the shape the picture is written in** as it moves down the stack,
and that is exactly what the representation thread tracks. A single lit pill is not a thin week; it is a
week that knows what it is about.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Cut one 3-square-wide card strip per student.** Five minutes. Use the same squared paper you are handing out so the widths match exactly — a card that is 3.2 squares wide ruins the count and the student will blame themselves.
- [ ] **Do the card slide yourself, on paper, out loud.** Two minutes. Draw 8 squares, slide the card, say "zero, one, two, three, four, five", write **6**. **If you have not physically done this, do not teach this lesson.** It is the whole derivation.
- [ ] **Do these four by hand with a calculator**, and write them on a sticky note you keep beside you: `(8+0−3)÷1+1 = 6`, `(8+2−3)÷1+1 = 8`, `(8+0−2)÷2+1 = 4`, `(8+2−3)÷2+1 = 4` (the last one is `3.5` rounded down to `3`, then `+1`). **Row four is the one you will fumble.**
- [ ] **Type and run `shapes.py` yourself.** The complete file:

```python
"""shapes.py - work out the size before you run it."""
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)
np.random.seed(0)

# ---------- 1. one 8x8 picture, typed by hand ----------
img = np.zeros((8, 8), dtype=np.float32)
img[:, 0:4] = 10.0
img[:, 4:8] = 2.0
print("--- the picture ---")
print(img.astype(int))
print("numpy shape :", img.shape)

x = torch.from_numpy(img).float().unsqueeze(0).unsqueeze(0)
print("torch shape :", tuple(x.shape))

# ---------- 2. count the window positions ----------
print()
print("--- how many places does a 3-wide window fit on 8 numbers? ---")
starts = [s for s in range(8) if s + 3 <= 8]
print("start columns:", starts)
print("that is", len(starts), "positions")
print("the rule    : (8 + 0 - 3) // 1 + 1 =", (8 + 0 - 3) // 1 + 1)
print("Conv2d(1, 1, 3) says:", tuple(nn.Conv2d(1, 1, 3)(x).shape))

# ---------- 3. the shape ladder ----------
print()
print("--- the shape ladder: four pictures through the stack ---")
batch = torch.zeros(4, 1, 8, 8)
stack = [("input", None),
         ("Conv2d(1, 8, 3, padding=1)", nn.Conv2d(1, 8, 3, padding=1)),
         ("ReLU()", nn.ReLU()),
         ("MaxPool2d(2)", nn.MaxPool2d(2)),
         ("Conv2d(8, 16, 3, padding=1)", nn.Conv2d(8, 16, 3, padding=1)),
         ("ReLU()", nn.ReLU()),
         ("MaxPool2d(2)", nn.MaxPool2d(2)),
         ("Flatten()", nn.Flatten())]
h = batch
for name, layer in stack:
    if layer is not None:
        h = layer(h)
    print("%-28s %s" % (name, tuple(h.shape)))

print()
print("t.view(t.size(0), -1) gives the same thing:",
      tuple(h.view(h.size(0), -1).shape))
```

Run `python3 shapes.py`. You must see **exactly** this:

```text
--- the picture ---
[[10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]
 [10 10 10 10  2  2  2  2]]
numpy shape : (8, 8)
torch shape : (1, 1, 8, 8)

--- how many places does a 3-wide window fit on 8 numbers? ---
start columns: [0, 1, 2, 3, 4, 5]
that is 6 positions
the rule    : (8 + 0 - 3) // 1 + 1 = 6
Conv2d(1, 1, 3) says: (1, 1, 6, 6)

--- the shape ladder: four pictures through the stack ---
input                        (4, 1, 8, 8)
Conv2d(1, 8, 3, padding=1)   (4, 8, 8, 8)
ReLU()                       (4, 8, 8, 8)
MaxPool2d(2)                 (4, 8, 4, 4)
Conv2d(8, 16, 3, padding=1)  (4, 16, 4, 4)
ReLU()                       (4, 16, 4, 4)
MaxPool2d(2)                 (4, 16, 2, 2)
Flatten()                    (4, 64)

t.view(t.size(0), -1) gives the same thing: (4, 64)
```

**Expected runtime: under one second.** Nothing trains.

- [ ] **Break it on purpose.** Save this as `stack.py` and run it:

```python
"""stack.py - deliberately mis-size the Linear layer."""
import torch
import torch.nn as nn

torch.manual_seed(0)
batch = torch.zeros(4, 1, 8, 8)
net = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32, 10))          # <-- wrong on purpose: should be 64
logits = net(batch)
print(tuple(logits.shape))
```

The real last three lines:

```text
  File "/private/tmp/w25f/stack.py", line 12, in <module>
    logits = net(batch)
...
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**Read it once and say out loud which number is yours.** The `32`. Because you typed `nn.Linear(32, 10)`. The `64` came out of `16 × 2 × 2`.

- [ ] **Print workbook pages 25.1–25.7.**
- [ ] **Put up the wall sheet: THE SHAPE LADDER**, six blank rows, with two columns headed `my prediction (pen)` and `what it printed`. It stays up until Week 27.
- [ ] **Check the PARAMETER COUNT sheet from Week 22 is still on the wall.** You point at it twice this week and add a row to it next week.

### 5 minutes on the day

- [ ] Editor open, terminal ready. `shapes.py` and `stack.py` **deleted or renamed** — they type them.
- [ ] Squared paper out, one sheet each, **plus the 3-square card strips**, one each, on the desk before they sit down.
- [ ] **Pens, not pencils**, for page 25.1. The point of pen is that you cannot quietly fix a wrong prediction.
- [ ] THE SHAPE LADDER sheet blank on the wall.
- [ ] Bug Log out.

### Fallback if the laptops fail

**This week's paper version loses almost nothing**, because the derivation is already a card on squared paper and the rule is one division.

1. **The card slide.** Eight squares, a 3-wide card, count the starts. **Objective 1, complete, in four minutes.**
2. **The stride and padding variations, on paper.** Slide the card two at a time: three positions. Draw a ring of squares round an 8×8 and slide again: eight positions. **Both halves of objective 4, complete.**
3. **Twelve divisions.** Workbook page 25.4 is twelve rows of arithmetic and needs no computer at all. Do six in class, six at home.
4. **The shape ladder, in pen, on the wall sheet.** They can predict all six shapes without a machine. You then read the six correct shapes out from this file's Answer Key and they mark their own. **Objective 3 minus the traceback.**
5. **The traceback, read from Figure 25.1.** Project it or pass it round on paper. *"Two numbers. Which one did you type?"* **This works on paper and it is the sentence the week exists for.**

| If this fails | Do this instead |
|---|---|
| The printed shape is `(4, 8, 6, 6)` where you expected `(4, 8, 8, 8)` | `padding=1` is missing from `Conv2d`. It is the single commonest typo of the week. |
| `MaxPool2d(2)` on a 3×3 gives 1, and then the next conv errors | The stack was built with unpadded convs, so 8 → 6 → 3 → 1 → **stop**. This is the whole reason for `padding=1`; it is a teaching moment, not a disaster. |
| A student's card strip is not exactly 3 squares wide | Their count comes out 5 or 7 and they think they cannot count. Swap the card, out loud, and say "the card was wrong, not you." |
| Somebody writes the rule with `p` instead of `2p` | Ask *"how many sides did you glue a ring onto?"* Two. That is the 2. |
| The whole room writes the ladder in pencil | Let it go once, then say the reason out loud: *"pen means I can see what you actually thought."* |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Two Numbers in an Error | 7 | 7 | The traceback, before any theory. Which one did you type? |
| 🧠 Concept & Maths — Count, Then Write the Rule | 18 | 25 | Card on squared paper; the count; the rule; stride; padding |
| 💻 Live-Code Together — `shapes.py` | 18 | 43 | The picture, the count confirmed, the ladder. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Shape Ladder | 20 | 63 | Six shapes in pen, all at once; then print them; read the one miss |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Two Numbers in an Error (7 minutes)

**Do this:** Nothing on the screen except one line, typed large:

```text
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**Say this:**

> "This is the error you are going to get most often for the rest of this course. Not a typo, not a misspelt variable — this one. It is the error you get when a network's plumbing does not line up.
>
> Look at it properly. **It contains four numbers**: 4, 64, 32 and 10. And here is the thing I want you to notice before you know anything else about it.
>
> **Two of those numbers I typed with my own fingers. Two of them came out of the picture.** And until you can tell which is which, this error takes you twenty minutes. Once you can, it takes ten seconds."

**Do this:** Write on the board, leaving the right-hand side blank:

```
4    came from ?
64   came from ?
32   came from ?
10   came from ?
```

**Ask this:** "Have a guess. Which of these four do you think a person chose?"

*Hoped-for answer:* the 10, because there are ten digits.

> "The 10, yes — ten classes, ten answers, somebody chose that. Good.
>
> And the 4? Four pictures in the batch. Somebody chose that too.
>
> So the argument is between the 64 and the 32. One of those came out of the picture by arithmetic. The other one I typed, and I typed it **wrong**."

**Ask this:** "How would you find out which?"

*Hoped-for answer:* look at the code / print the shapes.

*If they say "run it again":* fine, and it will fail identically, because a shape error is not random. Say so: **"a shape error is the most reliable thing in this course. It fails exactly the same way every time, which is a gift."**

> "You look at the code, and you can — but you would still have to work out what the picture *should* have turned into, and that is arithmetic you have never done. **So today we learn the arithmetic.** It is one division and it takes two minutes to derive.
>
> By the end of the lesson you will look at `(4x64 and 32x10)` and say, without opening the file: *the 64 is the picture, the 32 is mine, change the 32 to 64.* And then you will go home and do it on purpose so you have seen it once with your own eyes."

**Do this:** Hold up a sheet of squared paper and a 3-square card strip.

> "And this is the entire mathematical apparatus."

---

### 🧠 Concept & Maths — Count, Then Write the Rule (18 minutes)

**Do this:** Everyone draws a row of **8 squares** on their squared paper and numbers them 0 to 7. **Number them yourself on the board, out loud, starting at zero.** That zero is going to matter in four minutes.

**Say this:**

> "Eight squares. This is one row of a picture. And this card is the window — three squares wide. It is the thing that slides.
>
> Put the card at the far left. Read me the numbers it covers."

*0, 1, 2.*

> "That is one position. Slide it right by one square. Read them."

*1, 2, 3.*

> "Two. Keep going, and **say the start number out loud each time.** Not the whole window — just the leftmost square."

**Do this:** Let the whole room chant the start numbers together. *"Zero. One. Two. Three. Four. Five."* Then stop them — the card is hanging off the end.

**Ask this:** "How many numbers did you just say?"

*Hoped-for answer:* six.

**Ask this:** "And what was the last one?"

*Hoped-for answer:* five.

> "**Five was the last start, and there were six starts.** Six, not five. Hold on to that; it is the only thing in this lesson that trips people up.
>
> So: a 3-wide window on 8 squares gives an answer **6 long**. You did not calculate that. You counted it. Write **6** on your paper and circle it."

**Do this:** Now build the arithmetic on the board, one line at a time, asking for each line before you write it.

**Ask this:** "Why couldn't the card start at square 6?"

*Hoped-for answer:* because it is 3 wide, so it would need squares 6, 7, 8 and there is no square 8.

> "Right. The window's last square is 2 to the right of its start. So the last legal start is `8 − 3`, which is 5."

```
8 − 3 = 5        the last place the window can start
```

**Ask this:** "And how do I get from 'the last start is 5' to 'there are 6 starts'?"

*Hoped-for answer:* add one, because you started at zero.

```
5 + 1 = 6        six starts, because you counted the one at zero
```

> "**That `+ 1` is a fence post.** Ten metres of fence with a post every metre needs eleven posts, because there is one at the very beginning. Same `+1`. Same reason. It is not a fudge."

**Do this:** Now the two knobs, one at a time, still with the card.

> "Knob one. **Stride.** So far the card jumped one square. Make it jump **two**. Slide it: zero, two, four — and now it is off the end. How many?"

*Three.*

> "Three, not six. So stride 2 **halves the answer**. And here is the sentence I want back from you at the end of the lesson: **the picture did not get smaller. You looked at it half as often.** The eight squares are still there. You just skipped every other window."

```
8 − 3 = 5
5 ÷ 2 = 2.5      how many 2-square jumps fit
round down → 2   you cannot take half a jump
2 + 1 = 3
```

**Ask this:** "Why do I round *down* and not to the nearest?"

*Hoped-for answer:* because half a jump isn't a jump / the card would hang off the end.

> "Because two and a half jumps puts the card half off the end of the paper. **Down, always down.**"

> "Knob two. **Padding.** Draw one extra square on each end of your row, and write `0` in both. That is padding of one. Nine — sorry, ten squares now. Slide the card from the leftmost new square."

*Zero through seven — eight positions.*

```
(8 + 2) − 3 = 7      one ring adds one square on EACH side, so + 2
7 ÷ 1 = 7
7 + 1 = 8            the answer is the same size as the picture
```

> "**Eight in, eight out.** That is the setting almost every real network uses — window 3, jump 1, one ring of zeros — because it means you can stack layer after layer and the picture never quietly shrinks away to nothing."

**Do this:** Now, and only now, write the rule on the board and box it.

```
out  =  (n + 2p − k) ÷ s + 1,   rounded down

n = how wide the picture is          p = rings of zeros round the outside
k = how wide the window is           s = how far it jumps each step
```

> "Four letters, and you have already used all four. **This is a shortcut for the counting you just did with a card. If you ever forget it, get a card.**"

**Ask this:** "There is a second reason for padding and it is better than the first. Look at your row with the ring of zeros on it. How many windows does square 0 sit inside?"

*Let them count. Without padding: one. With padding: two along a row (and 4 in the 2-D version).*

> "Without the zeros, the corner square of a picture is inside exactly **one** window. A square in the middle is inside **nine**. So the model gets nine times more evidence about the middle of a picture than about the corners. **Add one ring of zeros and the corner goes from 1 window to 4.** Still not nine. Four times better than one."

**Do this:** Write on the board and leave it up:

```
padding 0:  corner in 1 window,  middle in 9
padding 1:  corner in 4 windows, middle in 9
```

**Do this:** Hand out workbook page 25.2 — four configurations, by hand, five minutes. Then page 25.1: **the six shapes, in pen.**

> "Pen. Six shapes. You have four minutes and no computer, and I will be able to tell afterwards exactly what you thought."

---

### 💻 Live-Code Together — `shapes.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — one picture, typed by hand.**

```python
"""shapes.py - work out the size before you run it."""
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)
np.random.seed(0)

img = np.zeros((8, 8), dtype=np.float32)
img[:, 0:4] = 10.0
img[:, 4:8] = 2.0
print("--- the picture ---")
print(img.astype(int))
print("numpy shape :", img.shape)

x = torch.from_numpy(img).float().unsqueeze(0).unsqueeze(0)
print("torch shape :", tuple(x.shape))
```

**Ask before running:** "`img.shape` will print `(8, 8)`. What will `x.shape` print?"

*Most will say `(8, 8)`.* Run it:

```text
numpy shape : (8, 8)
torch shape : (1, 1, 8, 8)
```

> **Say this:** "Four numbers, not two. `unsqueeze(0)` twice, so two 1s got glued on the front.
>
> Read them right to left: **8 wide, 8 tall, 1 channel, 1 picture in the batch.** Conv2d refuses to look at anything that is not shaped `(batch, channels, height, width)` — always four numbers, always in that order.
>
> `unsqueeze(0)` means 'add a new dimension of size 1 at position 0'. Doing it twice adds two. It does not change a single pixel value; it changes how the numbers are *labelled*. Same 64 numbers, different box around them."

**Step 2 (4 min) — the count, confirmed by the machine.**

```python
print()
print("--- how many places does a 3-wide window fit on 8 numbers? ---")
starts = [s for s in range(8) if s + 3 <= 8]
print("start columns:", starts)
print("that is", len(starts), "positions")
print("the rule    : (8 + 0 - 3) // 1 + 1 =", (8 + 0 - 3) // 1 + 1)
print("Conv2d(1, 1, 3) says:", tuple(nn.Conv2d(1, 1, 3)(x).shape))
```

```text
start columns: [0, 1, 2, 3, 4, 5]
that is 6 positions
the rule    : (8 + 0 - 3) // 1 + 1 = 6
Conv2d(1, 1, 3) says: (1, 1, 6, 6)
```

> **Say this:** "Three ways of getting the same 6, on one screen. **The card on your paper. The rule. And PyTorch.** Look at `[0, 1, 2, 3, 4, 5]` — that is literally the list you chanted.
>
> `//` is the rounding-down divide. `5 // 1` is 5, and `5 // 2` would be 2, not 2.5. It is the `floor` in the rule, spelled as two slashes.
>
> And `(1, 1, 6, 6)`: the batch stayed 1, the channels stayed 1, and **both** the 8s became 6s — because the rule applies to height and width separately, and they happened to be the same."

**Step 3 (3 min) — 🐞 DELIBERATE MISTAKE ONE: pass the picture in without the extra dimensions.**

> **Say this:** "Let me try that with the plain 8×8, without all the unsqueezing. It's the same numbers, after all."

Type and run:

```python
print(nn.Conv2d(1, 1, 3)(torch.from_numpy(img)).shape)
```

Real output:

```text
RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [8, 8]
```

**Do this:** Point at `[8, 8]` at the end of the line.

**Ask this:** "It printed your shape back at you. What is it complaining about?"

*Hoped-for answer:* it wants 4 numbers and got 2.

> **Say this:** "Read the message: it wants **3D or 4D** and got something of size `[8, 8]`, which is 2D. It is not confused about the pixels. It is confused about the box.
>
> This is the friendliest error in the whole level, because **it prints the shape it got.** Almost every torch error about shapes does. Get in the habit: when you see a shape error, the shape you need is already on the screen."

**Do this:** Bug Log entry, sixty seconds. Message: `Expected 3D (unbatched) or 4D (batched) input to conv2d ... got input of size: [8, 8]`. Meaning: *"conv wants (batch, channels, height, width) and I gave it (height, width)."* Fix: *"`.unsqueeze(0)` twice, or `t.view(1, 1, 8, 8)`."*

**Step 4 (5 min) — the shape ladder.**

```python
print()
print("--- the shape ladder: four pictures through the stack ---")
batch = torch.zeros(4, 1, 8, 8)
stack = [("input", None),
         ("Conv2d(1, 8, 3, padding=1)", nn.Conv2d(1, 8, 3, padding=1)),
         ("ReLU()", nn.ReLU()),
         ("MaxPool2d(2)", nn.MaxPool2d(2)),
         ("Conv2d(8, 16, 3, padding=1)", nn.Conv2d(8, 16, 3, padding=1)),
         ("ReLU()", nn.ReLU()),
         ("MaxPool2d(2)", nn.MaxPool2d(2)),
         ("Flatten()", nn.Flatten())]
h = batch
for name, layer in stack:
    if layer is not None:
        h = layer(h)
    print("%-28s %s" % (name, tuple(h.shape)))
```

**Do this:** **Before running, go round the room and collect the six predictions from page 25.1, in pen, and write them on the wall sheet.** Do not correct anything. Then run it.

```text
input                        (4, 1, 8, 8)
Conv2d(1, 8, 3, padding=1)   (4, 8, 8, 8)
ReLU()                       (4, 8, 8, 8)
MaxPool2d(2)                 (4, 8, 4, 4)
Conv2d(8, 16, 3, padding=1)  (4, 16, 4, 4)
ReLU()                       (4, 16, 4, 4)
MaxPool2d(2)                 (4, 16, 2, 2)
Flatten()                    (4, 64)
```

![The shape ladder](../figures/fig-w25-4-shape-ladder-through-the-stack.svg)
*Figure 25.5 — The shape ladder. Six shapes, each with the arithmetic that produced it, and the batch size 4 riding along untouched all the way down.*

> **Say this, one line at a time, pointing:**
>
> "**Line 1.** `(4, 1, 8, 8)`. Four pictures, one channel, eight by eight.
>
> **Line 2.** `(4, 8, 8, 8)`. Two things changed and one thing did not. The channels went **1 → 8**, because I asked for 8 filters and each filter makes its own answer grid. The height and width stayed **8**, because `(8 + 2 − 3) ÷ 1 + 1 = 8` — window 3, one ring of zeros, jump 1. **Same size in, same size out.**
>
> **Line 3.** `ReLU()` changed nothing at all. It went through every number and replaced the negatives with zero. **A squash never changes a shape.** Say that out loud once; it saves an hour later.
>
> **Line 4.** `(4, 8, 4, 4)`. The 8 channels are untouched — pooling does not mix channels. The 8 by 8 became 4 by 4: `(8 + 0 − 2) ÷ 2 + 1 = 4`. Halved.
>
> **Line 5.** `(4, 16, 4, 4)`. Channels 8 → 16 because 16 filters. Height and width unchanged again — same padding.
>
> **Line 7.** `(4, 16, 2, 2)`. Halved again. `(4 + 0 − 2) ÷ 2 + 1 = 2`.
>
> **Line 8.** `(4, 64)`. **This is the line the lesson is for.** Sixteen channels of two by two is `16 × 2 × 2 = 64` numbers per picture, laid out flat in one row. Four pictures, sixty-four numbers each. And **64 is the number you must write into `nn.Linear`.**"

**Ask this:** "Which number is the same on every single line?"

*Hoped-for answer:* the 4.

> "The batch size. **It rides along untouched from top to bottom.** Nothing you do to a picture changes how many pictures you have. If you ever see the first number change, something is very wrong."

**Step 5 (2 min) — the two ways to flatten.**

```python
print()
print("t.view(t.size(0), -1) gives the same thing:",
      tuple(h.view(h.size(0), -1).shape))
```

```text
t.view(t.size(0), -1) gives the same thing: (4, 64)
```

> **Say this:** "`t.size(0)` means 'however many rows are in this batch — look, don't ask me'. And `-1` means 'you work the rest out, keeping the total number of numbers the same'. Sixty-four is the only thing that fits, so it computes 64 for you.
>
> Two spellings, one operation. `nn.Flatten()` is a layer you drop in a stack; `t.view(t.size(0), -1)` is a method you call inside a `forward`. **Use whichever, but know they are the same thing.**"

**Step 6 (2 min) — 🐞 DELIBERATE MISTAKE TWO: the mis-sized `Linear`.**

> **Say this:** "Right. One more layer and this is a real classifier. Ten digits, so ten outputs. And the flatten gave us... let me see, 16 channels of 2 by 2, that's — 32."

Type it wrong, deliberately, and say the wrong arithmetic out loud:

```python
net = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32, 10))
print(tuple(net(batch).shape))
```

Real output:

```text
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**Do this:** Say nothing. Walk to the board where the hook is still written. Point at the blank right-hand side.

**Ask this:** "Now. Which number did I type?"

*Hoped-for answer:* the 32.

**Ask this:** "And where did the 64 come from?"

*Hoped-for answer:* 16 × 2 × 2.

> **Say this:** "There it is. **Two numbers, and only one of them is mine.** I said '16 channels of 2 by 2, that's 32' — I multiplied 16 by 2 and forgot the second 2. `16 × 2 × 2 = 64`, and the machine knew, because it had actually done it.
>
> And look at how the error is written: `(4x64 and 32x10)`. The two inner numbers — the 64 and the 32 — are the ones that have to match. **This is Week 17 all over again**: a grid times a grid, and the inner numbers must agree. Nothing new has happened. It just has pictures in it now."

Fix it live:

```python
    nn.Linear(64, 10))
```

```text
(4, 10)
```

> "`(4, 10)`. Four pictures, ten numbers each. Ten scores, one per digit. **That is next week.**"

**Do this:** Bug Log. **This is the most valuable entry of the term.** Ninety seconds, and make sure both of these sentences are in it: *"the first number of the pair comes from the picture"* and *"the second one is the one I typed"*.

---

### 🎲 Their Turn — The Shape Ladder (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: six shapes predicted in pen on paper by everybody at once, transcribed onto the wall sheet before anything runs, then printed; the one wrong prediction gets its real traceback produced on purpose and the two numbers in it circled.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at THE SHAPE LADDER wall sheet with both columns filled in. Read the six printed shapes out loud, slowly.

**Say this:**

> "Six shapes. `(4, 1, 8, 8)`, `(4, 8, 8, 8)`, `(4, 8, 4, 4)`, `(4, 16, 4, 4)`, `(4, 16, 2, 2)`, `(4, 64)`.
>
> And every single one of them came from one division. `(n + 2p − k) ÷ s + 1`, rounded down. Which you did not memorise from a book — **you counted it with a card on squared paper, and then you worked out the shortcut.**
>
> Two sentences to take away, and I want a number in each.
>
> **Padding.** One ring of zeros keeps an 8 at 8 instead of dropping it to 6, and it takes the corner pixel from sitting in 1 window to sitting in 4.
>
> **Stride 2.** It halves the answer — six window starts become three — and it costs you the three windows you skipped. The picture did not shrink. **You looked at it half as often.**"

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "Last thing, and it is next week's door.
>
> Every shape on that wall sheet is a shape of numbers we never looked at. We put zeros in and got zeros out. We never trained anything. Those eight filters in the first layer? **Right now they are random noise** — PyTorch made them up when you built the layer.
>
> Next week we let gradient descent choose those numbers, on 1,257 real handwritten digits, and it takes about three seconds. And then — this is the good bit — **we draw the eight filters as pictures and look at what it decided to look for.** Nobody tells it. It works it out."

**Do this:** Hand out the homework and read the second part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)` | "The flatten produced 64 numbers per picture and your Linear layer was expecting 32." | `nn.Linear(32, 10)` after a flatten that gives 64. The 64 came from the picture; the 32 you typed. | Work out the flatten length with the rule: 16 channels × 2 × 2 = 64. Then `nn.Linear(64, 10)`. **Or print `h.shape` on the line before the flatten.** |
| `RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [8, 8]` | "Conv2d wants four numbers in the shape and you gave it two." | An 8×8 array handed straight to a conv layer, with no batch and no channel dimension. | `x = t.unsqueeze(0).unsqueeze(0)`, or `t.view(1, 1, 8, 8)`. The order is always **(batch, channels, height, width)**. |
| `RuntimeError: Given groups=1, weight of size [4, 1, 3, 3], expected input[4, 8, 8, 8] to have 1 channels, but got 8 channels instead` | "This layer was built for 1 input channel and it has been handed 8." | The second conv was written `nn.Conv2d(1, 16, 3)` instead of `nn.Conv2d(8, 16, 3)`. | **The first number of `Conv2d` must equal the channel count coming in**, which is the second number of the shape above it. Read the message: it tells you both — 1 expected, 8 got. |
| `RuntimeError: Calculated padded input size per channel: (4 x 4). Kernel size: (5 x 5). Kernel size can't be greater than actual input size` | "The window is bigger than what is left of the picture." | A 5×5 conv applied deep in the stack, after two pools have taken the picture down to 4×4. | Either use a smaller window, or add padding, or pool one fewer time. **Do the ladder on paper and you see this coming three layers early.** |
| `RuntimeError: Given input size: (16x1x1). Calculated output size: (16x0x0). Output size is too small` | "You asked me to pool a 1×1 and there is nothing left to pool." | One pool too many: 8 → 4 → 2 → 1 → **stop**. | Count your pools. Each one halves. Starting from 8 you get exactly three before you run out. |
| `RuntimeError: shape '[4, 32]' is invalid for input of size 256` | "You asked for 4 × 32 = 128 numbers and I have 256." | `t.view(4, 32)` on a `(4, 16, 2, 2)` tensor, which holds 4 × 64 = 256 numbers. | `t.view(t.size(0), -1)` and let it work the 64 out. **`-1` cannot be wrong; a number you typed can.** |
| `RuntimeError: Input type (double) and bias type (float) should be the same` | "Your numbers are 64-bit and the layer's are 32-bit." | `torch.from_numpy(...)` on a numpy array that defaulted to `float64`. | `.float()` right after `from_numpy`, every time. Or build the array with `dtype=np.float32`. |
| `TypeError: conv2d() received an invalid combination of arguments - got (numpy.ndarray, Parameter, Parameter, ...)` | "That is a numpy array, not a tensor." | A numpy array handed straight to a layer, with no `torch.from_numpy`. | `torch.from_numpy(a).float()`. The clue is the word `numpy.ndarray` in the first line of the message. |
| **No error. Every conv output is 2 smaller than you expected.** | Nothing crashed. Your ladder is right, your code is not. | `padding=1` was left off. `Conv2d(1, 8, 3)` is `padding=0`. | Add `padding=1`. **And note the trap: `nn.Conv2d(1, 8, 3, 1)` does NOT set padding — the fourth positional argument is `stride`.** Always name it: `padding=1`. |
| **No error. The shapes are right but the network is bigger than you expected.** | Nothing crashed. | The flatten happened before the pools instead of after, so `Linear` got 8 × 8 × 16 = 1,024 inputs instead of 64 — a `Linear` layer 16 times bigger (10,250 weights and biases instead of 650). | Print the shape on the line before `Flatten()`. **The ladder is not decoration; it is the audit.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and all three are about a message that has already told you the answer.

17. **"Read me the last line, and only the last line."** Every shape error in torch names the shapes. The student who reads the middle of the traceback is reading library code they did not write.

18. **"Which of those two numbers did you type?"** This is the whole week in one question, and it works on every single shape mismatch for the rest of the course. The one you typed is the one you change.

19. **"Print the shape on the line before the one that broke."** One line, `print(h.shape)`, costs three seconds and ends the argument. **A student who guesses a shape twice in a row should be made to print it.**

And the sentence for this week:

> **"A shape error is arithmetic you did not do. It is never bad luck, it is never random, and it fails identically every single time — which makes it the easiest bug in this course to fix and the most expensive one to guess at."**

---

## 🎲 The Activity, In Full

### The Shape Ladder

**What it is.** Everybody predicts all six shapes through the stack, **in pen, at the same time, with no computer open.** Then the predictions go on the wall. Then it runs. Then the one wrong prediction gets built into a real broken program on purpose, so the class sees the traceback that a wrong prediction actually produces.

The point is not that they get it right. **The point is that the wrong prediction has a visible consequence with two numbers in it.**

### Setup

- Workbook page 25.1: the six blank shapes with the layer names beside them, and a wide right-hand column headed `what it printed`.
- **Pens.** Not pencils. This is load-bearing.
- THE SHAPE LADDER wall sheet, six blank rows, two columns.
- Laptops **closed** for part 1. Say so out loud.

### Part 1 — six shapes, in pen, no computer (7 minutes)

Write the stack on the board, exactly this, and nothing else:

```
a batch of 4 pictures, 1 channel, 8 by 8
  conv, window 3, 8 filters, one ring of zeros
  ReLU
  max pool, window 2, jump 2
  conv, window 3, 16 filters, one ring of zeros
  ReLU
  max pool, window 2, jump 2
  flatten
```

Then read the instruction once and say nothing at all:

> **"Six shapes. Four numbers each, except the last one. In pen. You have seven minutes and your laptop stays shut. If you are stuck on a line, do the division on the side of the page where I can see it."**

**Sit on your hands.** This is the seven minutes in which the rule becomes theirs.

**Watch for exactly three failure modes**, and do not fix any of them yet:

1. **The channel count copied down unchanged.** They apply the rule to height and width and forget that 8 filters means 8 channels.
2. **The `+1` dropped**, so the pools give 3 instead of 4.
3. **The last line written as `(4, 16, 2, 2)` again**, because they did not multiply.

### Part 2 — the predictions go on the wall (3 minutes)

Go round the room. **Write every prediction on the wall sheet, in the `my prediction (pen)` column, without comment.** If two students disagree, write both. Disagreement on the wall is the most useful thing in the room.

**Do not say which is right.** Do not raise an eyebrow.

### Part 3 — run it (4 minutes)

Laptops open. They type the ladder loop from the live-code segment (or reopen `shapes.py`) and run it. As each shape prints, they write it in the `what it printed` column and **circle any line where their pen and the print disagree.**

The six correct shapes:

| Layer | Shape | Why |
|---|---|---|
| input | `(4, 1, 8, 8)` | 4 pictures, 1 channel, 8 by 8 |
| conv 3×3, 8 filters, pad 1 | `(4, 8, 8, 8)` | channels 1 → 8; `(8 + 2 − 3) ÷ 1 + 1 = 8` |
| max pool 2×2 | `(4, 8, 4, 4)` | channels unchanged; `(8 + 0 − 2) ÷ 2 + 1 = 4` |
| conv 3×3, 16 filters, pad 1 | `(4, 16, 4, 4)` | channels 8 → 16; `(4 + 2 − 3) ÷ 1 + 1 = 4` |
| max pool 2×2 | `(4, 16, 2, 2)` | `(4 + 0 − 2) ÷ 2 + 1 = 2` |
| flatten | `(4, 64)` | `16 × 2 × 2 = 64` |

### Part 4 — the one wrong prediction gets a traceback (6 minutes)

Pick the most interesting miss on the wall — ideally somebody's last line, and ideally one that came out **32**. Say whose it is only if they are happy about it; otherwise say "somebody wrote 32, and I want to show you something".

> **"Right. Let's find out what would have happened if you had believed that number."**

They add one line to the stack, using the **wrong** number from the wall:

```python
net = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32, 10))
print(tuple(net(batch).shape))
```

```text
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**Read the last line out loud, slowly, and have somebody come to the board and circle the two numbers.** Then two questions, in this order:

> **"Which one came from the picture?"** (The 64.)
>
> **"Which one came from you?"** (The 32.)

**Then the fix, and they type it themselves:** `nn.Linear(64, 10)` → `(4, 10)`.

### What "finished" looks like

- Page 25.1 with six shapes in pen, six printed shapes beside them, and every disagreement circled.
- THE SHAPE LADDER wall sheet with both columns full.
- At least one division written in the margin per pooled line — evidence they used the rule rather than a pattern.
- One real traceback in the Bug Log with `64` and `32` circled and labelled **picture** and **mine**.
- The student can say, unprompted: *"the batch size never changes."*

### Variation — easier

**Cut the stack to four lines and drop the second conv block entirely:** input, conv (8 filters, pad 1), pool, flatten. Four shapes: `(4, 1, 8, 8)`, `(4, 8, 8, 8)`, `(4, 8, 4, 4)`, `(4, 128)`. Note the flatten is `8 × 4 × 4 = 128` here.

**And pre-fill the channel counts on the page**, leaving only the height and width blank. The channels are a copying job; the height and width are the objective. `(4, 8, __, __)` with the 8 already there removes the failure mode that is not being assessed.

**One more scaffold that works very well:** let them keep the card and the squared paper on the desk while they do it. **The card is not cheating. The card is the derivation.**

### Variation — harder

1. **Add a third block and predict it before running.** After `(4, 16, 2, 2)`, another pad-1 conv with 32 filters keeps 2×2 → `(4, 32, 2, 2)`, and then a third pool gives `(4, 32, 1, 1)`, flatten `(4, 32)`. **And then ask for a fourth pool.** It errors: `Given input size: (32x1x1). Calculated output size: (32x0x0). Output size is too small.` Genuinely satisfying to predict an error and be right.
2. **Do the whole ladder again with every `padding=1` removed.** 8 → 6 → 3 → 1 → **the pool fails**. Then the question: *"how many pad-free conv-pool blocks does an 8×8 picture support?"* One complete block: the second conv still fits (down to 1×1), but the pool after it fails.
3. **Replace the pools with stride-2 convs.** `Conv2d(8, 16, 3, stride=2, padding=1)` on a 8×8 gives `(4, 16, 4, 4)` — the same shape as conv-then-pool, in one layer instead of two. Then the honest question: *"what is different, if the shapes are identical?"* The stride-2 conv has weights and can learn what to keep; the pool always keeps the biggest. **That is a real answer to a real question and it is a level-5 conversation.**
4. **Work backwards.** *"I want the flatten to give exactly 100 numbers, starting from an 8×8. Find a stack that does it."* One answer: 25 filters and two pools, since `25 × 2 × 2 = 100`. There are others. Genuinely hard and completely checkable.
5. **The receptive field, empirically.** Switch on one pixel at a time and see which ones can change the top-left cell of the final 2×2 map. The code is in the Answer Key under page 25.7. The answer is the top-left **7×7 — 49 of the 64 pixels.** Then the good question: *"why not all 64?"* Because the top-left cell is in the corner, and the corner's window is clipped by the edge of the picture.

---

## ❓ Questions Students Ask This Week

**"Why is it `2p` and not `p`?"**

Because a ring goes all the way round, so it adds one square on the **left** and one on the **right**. The width grows by two, not one. Draw it: eight squares with one extra on each end is ten squares.

**And the check that settles it in five seconds:** `p=1` on an 8 with `k=3, s=1` must give 8 back, because that is the whole point of same padding. `(8 + 2 − 3) ÷ 1 + 1 = 8` ✅. With `p` instead of `2p`: `(8 + 1 − 3) ÷ 1 + 1 = 7` ❌. **Wrong formula, wrong answer, and the answer you already know is right catches it.**

**"Why round down? Why not round to the nearest?"**

Because you cannot take part of a step. If the last full jump lands the window at start 4 and there is only one square left, you do not get a window there — the card hangs off the paper and there is nothing under two thirds of it.

**Try it with the card**, honestly, and it becomes obvious in about four seconds. That is the fastest cure for this question and it is why the cards are on the desks.

**"Isn't padding with zeros lying to the model?"**

**Yes, a bit, and it is worth being straight about it.** Those zeros are not measurements. Nobody photographed them. Every answer along the border of a feature map is computed partly from numbers that were invented, which is why you sometimes see a faint frame effect around the edge of a feature map.

The trade is: made-up zeros at the border, or the border barely counted at all (in 1 window instead of 9). **Almost everybody takes the zeros, and nobody claims it is free.** There are alternatives — you can pad by repeating the edge pixel, or by mirroring the picture — and they are marginally better and hardly ever used, because the zeros are good enough and simpler.

**"Which should I use to shrink the picture — pooling, or a stride-2 conv?"** *(Nobody fully agrees, and here is why.)*

**This one is genuinely unsettled, and it has moved twice in the last fifteen years.** Be straight about it.

The shapes come out identical. `conv(pad 1) → pool 2` and `conv(stride 2, pad 1)` both take an 8×8 to a 4×4. So the argument is about what happens to the *numbers*.

**The case for pooling:** it has no weights, so it adds nothing to overfit with, it costs nothing to store, and "keep the biggest response in this neighbourhood" is a sensible, human-understandable thing to do. It was in LeNet in 1998 and it is still in half the networks people build today.

**The case for stride-2 convolution:** the pool throws information away according to a rule *you* chose, before the network had any say. A stride-2 conv has weights, so it can **learn** what to keep. Several influential papers around 2015 argued pooling was an unnecessary hand-designed step and got fine results without it.

**Where it stands:** most modern architectures use strided convolutions in the middle and one pool at the very end, and honestly some of that is fashion. **Nobody can show you a decisive experiment that settles it for all data, and people who claim otherwise are usually generalising from one dataset.** What you should take from that: when two designs give the same shapes and comparable results, the choice is an engineering preference and you should say so in your write-up rather than pretending it was forced.

**"How do I know how many pools I'm allowed?"**

Count halvings. Each 2×2 pool halves the size, rounding down. From 8: `8 → 4 → 2 → 1`, and then you are done, because there is nothing left to halve — a fourth pool errors out with `Calculated output size: (32x0x0). Output size is too small`.

**So an 8×8 picture supports exactly three pools, and our stack uses two.** That is not an accident; it is why the stack is two blocks and not four, and it is worth saying out loud: **the size of the picture puts a hard ceiling on how deep the network can go.** A 32×32 photo supports five. A 224×224 photo supports seven.

**"Does the ReLU change the shape?"**

**No. Never. Not once, in any network, ever.** It walks through every number and replaces the negatives with zeros. Same count of numbers, same arrangement, same shape.

The same is true of every squash — sigmoid, tanh, ReLU. **They are element-by-element, which is a phrase worth learning: it means "one number in, one number out, nothing mixes".** Shapes only change when numbers get combined or rearranged: a conv, a pool, a flatten, a matrix multiply.

**"Why does the batch size stay 4 the whole way down?"**

Because nothing you do to a picture changes how many pictures you have. Every layer this week treats the batch dimension as a stack of independent jobs: it does the same thing to picture 1 as to picture 2, and never lets them meet.

**And that is worth one more sentence, because it is why batching works at all.** If layers mixed pictures together, you could not put 4 in a batch and get the same answers as putting them through one at a time. You can, and you should check it once: run one picture alone and check its ten numbers match row 0 of the batch of four. **A layer that fails that check has a bug.**

**"The filters are random? Then what were we even computing?"**

Shapes, and only shapes. Every number we printed today was a zero, and the eight filters in the first layer are whatever numbers PyTorch invented when the layer was built.

**And that is the right way round, honestly.** Shapes are a plumbing problem and you can solve it completely, on paper, before you own any data. What the filters should contain is a learning problem and it needs data and a gradient. **We separated them on purpose: this week the plumbing, next week the water.**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The formula goes on the board before anybody slides a card** | It feels efficient, and it is how every textbook does it | **Do it the other way round.** Cards on squared paper, chant the six start numbers, circle the 6 — *then* derive the shortcut. A student who has counted can rebuild the rule; a student who memorised it cannot check it. |
| The `+1` is dropped, repeatedly, all lesson | It genuinely looks like it does not belong | Go back to the chant. *"Say the start numbers again. How many did you say? What was the last one?"* **Six, and five.** Then the fence posts. Do it three times if you have to; it is the single highest-value repetition of the week. |
| Rounding *up* on the stride-2 rows | 2.5 looks like it should become 3 | Hand them the card. Ask them to put it at start 6 on an 8-square row. **It hangs off, visibly, and the question answers itself.** |
| The channel count gets copied down unchanged | The rule is about height and width, and they applied it faithfully | *"How many filters did you ask for?"* Sixteen. *"So how many answer grids come out?"* Sixteen. **The second number of the shape is the filter count of the layer above it.** |
| **The ladder is done in pencil and quietly corrected** | Nobody likes being wrong on a wall | Say the reason out loud, once, kindly: *"pen means I get to see what you actually thought, and the wrong ones are the useful ones."* Then put a wrong prediction on the wall yourself. |
| The mis-sized `Linear` moment gets skipped because time is short | It is at minute 41 and the lesson is running late | **Do not skip it.** It is ninety seconds and it is the reason the week exists. Cut the `t.view` demo instead — that is a nice-to-know; the traceback is the objective. |
| `padding=1` gets passed positionally as `Conv2d(1, 8, 3, 1)` | It looks like the next argument | It sets **stride**, silently, and the output comes out 6 instead of 8 with no error at all. **Show it once**: `Conv2d(1, 4, 3, 1)` on an 8×8 gives `(1, 4, 6, 6)`. Then the rule: *"always name it `padding=1`."* |
| Somebody asks about training and the lesson turns into next week | It is the obvious next question and it is a good one | *"Next week, and it takes three seconds. Today the plumbing, next week the water."* Then point at the wall sheet. **Do not start a training loop today; you will run out of time and teach both things badly.** |
| The receptive field turns into a second formula | A strong student finds the recurrence online and wants it on the board | Do not put it on the board. *"That is real and it is right, and there is one new piece of maths this week. Show me instead which pixels can change the last cell — switch them on one at a time."* **The empirical version is better teaching and it is in the Answer Key.** |
| The room concludes shapes are a chore | Today's outputs are all zeros; nothing exciting happens | **Frame it as the week that stops you losing twenty minutes.** Then, at the wrap, say out loud what next week does with these shapes. Ending on "we look at the filters it invented" leaves the right taste. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the stride knob entirely. Padding and the plain `s=1` case carry both halves of the lesson. Every layer we build for the rest of Term 3 uses `s=1` convs and `s=2` pools, and the pool's stride is the default they never type.

**Cut:** `t.view(t.size(0), -1)`. `nn.Flatten()` alone is enough, and the two-spellings point is a nice-to-know.

**Cut:** the ladder from six shapes to four (Variation-easier), with the channel counts pre-filled.

**Give them `shapes.py` complete.** Every bit of the learning today is in the card, the division and the traceback, and none of it is in typing an import block.

**The version of the arithmetic that skips the algebra.** No letters at all. One table, and the only thing left to do is the division:

| The picture is | The window is | It jumps | Rings of zeros | Do this | Answer |
|---|---|---|---|---|---|
| 8 wide | 3 wide | 1 | none | 8 − 3 = 5, then 5 + 1 | |
| 8 wide | 3 wide | 1 | one ring (+2) | 8 + 2 − 3 = 7, then 7 + 1 | |
| 8 wide | 2 wide | 2 | none | 8 − 2 = 6, 6 ÷ 2 = 3, then 3 + 1 | |
| 4 wide | 2 wide | 2 | none | 4 − 2 = 2, 2 ÷ 2 = 1, then 1 + 1 | |

Four rows. **Every subtraction and division is already written out; they only do the arithmetic.** Then one question and nothing else: **"which row gives you back the number you started with?"** Row 2. **That is objective 4's first half, delivered with a calculator.**

**The copy-this-exactly scaffold.** Seven lines, and it runs on its own:

```python
import torch
import torch.nn as nn

x = torch.zeros(1, 1, 8, 8)
print("start          ", tuple(x.shape))
print("after conv pad1", tuple(nn.Conv2d(1, 4, 3, padding=1)(x).shape))
print("after pool 2   ", tuple(nn.MaxPool2d(2)(nn.Conv2d(1, 4, 3, padding=1)(x)).shape))
```

```text
start           (1, 1, 8, 8)
after conv pad1 (1, 4, 8, 8)
after pool 2    (1, 4, 4, 4)
```

Then three questions and nothing else: **"which number stayed 1? which number became 4 because I asked for 4 filters? and which two numbers got halved?"** The first; the second; the last two. **That is objectives 1 and 3 in seven lines.**

**One thing you must not cut:** the mis-sized `Linear` traceback. If the whole lesson collapses to one sentence, make it *"the error names two numbers and one of them is yours."*

### If the student is flying

None of these need syntax from a later week.

1. **The pad-free ladder** (Variation-harder 2): 8 → 6 → 3 → 1 → error. Then *"how many complete conv-pool blocks does an 8×8 support without padding?"* One (a second conv fits, its pool does not). **This is the best five minutes available today** because it makes padding's purpose arithmetical rather than decorative.
2. **Stride-2 conv versus conv-then-pool** (Variation-harder 3): identical shapes, different behaviour. Then *"which would you choose, and can you prove it?"* They cannot prove it, nobody can, and finding that out is the lesson.
3. **Work backwards to a flatten of exactly 100** (Variation-harder 4). Genuinely hard, completely checkable.
4. **The receptive field, empirically** (Variation-harder 5). The code is in the Answer Key. The answer is 49 of 64 pixels, and the follow-up — *"why not all 64?"* — is a level-5 question.
5. **Predict an error before it happens.** Ask them to write down, in pen, the exact error text they expect from a fourth pool. Then run it. `Given input size: (32x1x1). Calculated output size: (32x0x0). Output size is too small.` **A student who predicts an error message word for word has genuinely understood the machine.**
6. **The honest question:** *"the batch size rides along unchanged. Prove it matters."* Run one picture alone and check its ten numbers equal row 0 of the batch of four. If they do not, the layer has a bug. **This is a real test that real engineers write.**

### If the student won't engage today

**Close the laptop. Squared paper and a card strip.**

Better still: **let them choose the grid.** Not a digit — a minesweeper board, a crossword, a Scrabble rack, the pixels of a sprite from a game they like. Anything laid out in squares where a small window sliding over it makes sense.

Then three instructions and nothing else:

> **"Draw eight squares. Number them starting at zero."**
>
> **"Slide the card from the left and say the start number out loud each time. Stop when it hangs off."**
>
> **"How many numbers did you say? And what was the last one?"**

That is six and five — **objective 1 delivered with a piece of card in four minutes**, and it is the half of the lesson everything else hangs off. Then one more, if they will take it: *"now jump two at a time. How many?"* Three. **Half. Objective 4's second half, no computer, no code, no typing.**

The rest survives. Week 26 rebuilds this exact ladder before it trains anything, and Week 27 rebuilds it again.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — derive it, don't recall it (spoken, 60 seconds)**

> "A row of **10** squares. A window **4** wide. It jumps **1** at a time, no padding. **How many positions?** And I want to hear how you got it, not just the number."

*Good answer:* "Last start is 10 − 4 = 6, and counting from zero that's 6 + 1 = **7**."

**What to catch:** the answer `6`. Ask *"what was the last start, and did you count the one at zero?"* Do not give the `+1`; ask for it.

**Check 2 — the two sentences with numbers in them (spoken, 90 seconds)**

> "Two sentences, and **each one has to have a number in it.** One: what is padding for? Two: what does stride 2 cost you?"

*Good answer:* "Padding keeps the size the same — an 8 stays an 8 instead of dropping to 6 — and it takes the corner pixel from being in 1 window to being in 4. Stride 2 halves the answer: six window starts become three, so you skip three of the windows. The picture is the same size; you just look at it half as often."

**Full marks needs a number in each sentence.** "Padding stops it shrinking" with no number is a level-2 answer, and say so: *"how much would it have shrunk?"*

**Check 3 — the error, cold (spoken, 60 seconds)**

> "You run your network and it says: **`mat1 and mat2 shapes cannot be multiplied (8x128 and 64x10)`**. **Which number do you change, and why?**"

*Good answer:* "The 64, in my `Linear` layer, and I change it to 128. The 128 came out of the picture — it's the flatten length — and the 64 is what I typed. And I could check the 128 by working the ladder out: it'd be something like 32 channels of 2 by 2."

**What to catch:** any answer that changes the 128, or that says "I'd try both". Push once: *"which of those two numbers is written in your file?"* **A student who cannot answer this cannot debug next week's network, so it is worth the extra thirty seconds.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say how many 3-wide windows fit on 8 squares, even with a card. Reads a shape error as random. Copies shapes down from the layer above. |
| **2 — Emerging** | Gets the count right with the card in hand. Applies the rule when the numbers are handed over in the right order, but drops the `+1` on the pooled rows and rounds 2.5 up. |
| **3 — Secure** | Derives the rule from the count unaided, rounds down correctly, applies it to height and width separately, predicts all six shapes in the ladder including `16 × 2 × 2 = 64`, and **says which of the two numbers in a shape error came from the picture.** This is the target. |
| **4 — Strong** | Explains padding with the 1-versus-4-versus-9 window counts, not just "it stops it shrinking". Spots that `Conv2d(1, 8, 3, 1)` sets stride and not padding. Knows an 8×8 supports exactly three pools and can say why. Prints a shape rather than guessing it twice. |
| **5 — Exceptional** | Predicts an error message word for word before running it. Works backwards from a required flatten length to a stack that produces it. Notices unprompted that a stride-2 conv and a conv-then-pool give identical shapes, asks what is different about the numbers, and says honestly that the choice between them is not settled. Measures the receptive field empirically and explains why the corner cell sees 49 pixels and not 64. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, three pages, and the middle one is the one I care about most.
>
> **First, page 25.4 — twelve output sizes, by hand.** Twelve rows: the picture width, the window, the jump, the rings of zeros. **Write the arithmetic out, not just the answer** — the subtraction, the division, the rounding, the plus one. Then run `sizes.py`, which prints what PyTorch says, and **write the printed number beside each of your twelve.** If they match, tick it. **If they do not match, you write one sentence saying what you did instead of what the rule says.** Not 'I got it wrong'. *'I rounded 2.5 up to 3 instead of down to 2.'* That sentence is the whole point of the page.
>
> **Second, page 25.5 — break it on purpose.** Build the stack from today. Then **deliberately put the wrong number in the `Linear` layer after the flatten.** Any wrong number you like. Run it. **Paste the real error into your workbook, all of the last line.** Then two labels: circle the number that came from the picture and write *picture* next to it, circle the number you typed and write *mine* next to it. **And one sentence: how you would have known the right number without running anything.**
>
> **Third, page 25.6 — two sentences, and each one needs a number in it.** What is padding for? What does stride 2 cost you? One sentence each. **A sentence with no number in it does not count**, and I will hand it back.
>
> Page 25.7 is a stretch and it is optional. It measures how much of the picture the very last cell can see, and the answer surprised me the first time."

**Workbook pages:** 25.1, 25.2, 25.3 in class · **25.4, 25.5, 25.6** at home · 25.7 optional.

**Expected time:** 25 min on the twelve calculations and checking them · 20 min breaking the `Linear` layer and labelling the error · 10 min on the two sentences · **about 55 minutes**, plus 15 more if they do the stretch.

> **🧑‍🏫 What to look for when you mark it:** three things, and the second is the real one. **One — is the arithmetic written out, or just the answers?** Twelve correct numbers with no working is a page that might have been produced by pattern-matching, and the first stride-2 layer in Week 26 will find out. **Two — does the traceback on page 25.5 have both numbers labelled?** *Picture* and *mine*. This is the page that decides whether Weeks 26, 27, 33 and 34 cost them ten seconds or twenty minutes per bug, and it is worth a full line of feedback. **Three — do both sentences on 25.6 contain a number?** "Padding stops the image shrinking" is true and useless. "Padding keeps an 8 at 8 instead of 6, and takes the corner pixel from 1 window to 4" is the same idea with the evidence attached. **A rule you can only state in words is a rule you cannot check. A rule you can state in numbers checks itself.**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 25.1 — The six shapes, in pen, before running

*The stack: a batch of 4 pictures, 1 channel, 8 by 8 → conv window 3 with 8 filters and one ring of zeros → ReLU → max pool 2 → conv window 3 with 16 filters and one ring of zeros → ReLU → max pool 2 → flatten.*

| # | Layer | Shape | The arithmetic |
|---|---|---|---|
| 1 | input | **(4, 1, 8, 8)** | given: 4 pictures, 1 channel, 8 by 8 |
| 2 | conv 3×3, 8 filters, pad 1 | **(4, 8, 8, 8)** | channels 1 → 8. `(8 + 2 − 3) ÷ 1 + 1 = 7 + 1 = 8` |
| 3 | max pool 2×2 | **(4, 8, 4, 4)** | channels unchanged. `(8 + 0 − 2) ÷ 2 + 1 = 3 + 1 = 4` |
| 4 | conv 3×3, 16 filters, pad 1 | **(4, 16, 4, 4)** | channels 8 → 16. `(4 + 2 − 3) ÷ 1 + 1 = 3 + 1 = 4` |
| 5 | max pool 2×2 | **(4, 16, 2, 2)** | `(4 + 0 − 2) ÷ 2 + 1 = 1 + 1 = 2` |
| 6 | flatten | **(4, 64)** | `16 × 2 × 2 = 64` |

*(The ReLU lines are not counted as shapes because they do not change one: `(4, 8, 8, 8)` in, `(4, 8, 8, 8)` out.)*

**Marking notes.** **The three misses to expect, in order of frequency.** (a) Line 6 written as **32** — they did `16 × 2` and forgot the second 2. This is the miss the activity is built around, and it is the miss that produces the traceback. (b) Lines 3 and 5 written as **3** and **1** — the `+1` dropped. (c) Lines 2 and 4 with the channel count copied down from the line above. **Full marks does not require six right answers; it requires six answers in pen with the division shown for lines 3 and 5.**

### Page 25.2 — Four configurations, by hand, in class

| # | n | k | s | p | Arithmetic | out |
|---|---:|---:|---:|---:|---|---:|
| a | 8 | 3 | 1 | 0 | `(8 + 0 − 3) ÷ 1 + 1 = 5 + 1` | **6** |
| b | 8 | 3 | 1 | 1 | `(8 + 2 − 3) ÷ 1 + 1 = 7 + 1` | **8** |
| c | 8 | 2 | 2 | 0 | `(8 + 0 − 2) ÷ 2 + 1 = 3 + 1` | **4** |
| d | 8 | 3 | 2 | 1 | `(8 + 2 − 3) ÷ 2 + 1 = 3.5 → 3, then 3 + 1` | **4** |

**Row (d) is the row that separates level 2 from level 3.** `7 ÷ 2 = 3.5`, rounded **down** to 3, then `+ 1` gives 4. A student who wrote 5 rounded up. A student who wrote 4 with no working may have guessed, because (c) also gives 4 — **ask them which one produced the 3.5.**

**And the observation worth praising:** rows (c) and (d) both give 4. **Both halve an 8.** So there are two different ways to halve a picture, and next week's stack uses the pool version. A student who spots that unprompted is at level 4.

### Page 25.3 — The shape ladder audit

*For each of your six predictions, write the printed shape beside it and circle any disagreement. Then, for each circled line, one sentence: what did you do that the rule does not do?*

The six printed shapes are the table on page 25.1. **The sentences are what you mark.** Good ones:

- *"I wrote 3 for the pool. I did 8 ÷ 2 = 4 and then subtracted 1 for some reason. The rule says `(8 − 2) ÷ 2 + 1`, which is 4."*
- *"I wrote (4, 1, 8, 8) again after the conv. I forgot that 8 filters means 8 channels out."*
- *"I wrote 32 at the end. I multiplied 16 by 2 and stopped. It's 16 × 2 × 2 because the map is 2 wide AND 2 tall."*

**Anything that says only "I got it wrong" scores nothing on this page**, and say why: *"which number did you use, and where did it come from?"*

### Page 25.4 — Twelve output sizes, by hand, then checked

*For each row, apply `(n + 2p − k) ÷ s + 1`, rounded down. Write the arithmetic. Then run `sizes.py` and write the printed number beside each.*

| # | n | k | s | p | kind | Arithmetic, in full | out |
|---|---:|---:|---:|---:|---|---|---:|
| a | 8 | 3 | 1 | 0 | conv | `(8 + 0 − 3) = 5`; `5 ÷ 1 = 5`; `5 + 1` | **6** |
| b | 8 | 3 | 1 | 1 | conv | `(8 + 2 − 3) = 7`; `7 ÷ 1 = 7`; `7 + 1` | **8** |
| c | 8 | 2 | 2 | 0 | pool | `(8 + 0 − 2) = 6`; `6 ÷ 2 = 3`; `3 + 1` | **4** |
| d | 8 | 5 | 1 | 0 | conv | `(8 + 0 − 5) = 3`; `3 ÷ 1 = 3`; `3 + 1` | **4** |
| e | 8 | 5 | 1 | 2 | conv | `(8 + 4 − 5) = 7`; `7 ÷ 1 = 7`; `7 + 1` | **8** |
| f | 8 | 3 | 2 | 0 | conv | `(8 + 0 − 3) = 5`; `5 ÷ 2 = 2.5 → 2`; `2 + 1` | **3** |
| g | 8 | 3 | 2 | 1 | conv | `(8 + 2 − 3) = 7`; `7 ÷ 2 = 3.5 → 3`; `3 + 1` | **4** |
| h | 7 | 3 | 1 | 0 | conv | `(7 + 0 − 3) = 4`; `4 ÷ 1 = 4`; `4 + 1` | **5** |
| i | 7 | 2 | 2 | 0 | pool | `(7 + 0 − 2) = 5`; `5 ÷ 2 = 2.5 → 2`; `2 + 1` | **3** |
| j | 6 | 3 | 3 | 0 | conv | `(6 + 0 − 3) = 3`; `3 ÷ 3 = 1`; `1 + 1` | **2** |
| k | 4 | 2 | 2 | 0 | pool | `(4 + 0 − 2) = 2`; `2 ÷ 2 = 1`; `1 + 1` | **2** |
| l | 4 | 3 | 1 | 1 | conv | `(4 + 2 − 3) = 3`; `3 ÷ 1 = 3`; `3 + 1` | **4** |

**The verification file. Run it and it prints all twelve:**

```python
"""sizes.py - twelve output sizes, by hand and by PyTorch."""
import torch
import torch.nn as nn

CASES = [("a", 8, 3, 1, 0, "conv"), ("b", 8, 3, 1, 1, "conv"),
         ("c", 8, 2, 2, 0, "pool"), ("d", 8, 5, 1, 0, "conv"),
         ("e", 8, 5, 1, 2, "conv"), ("f", 8, 3, 2, 0, "conv"),
         ("g", 8, 3, 2, 1, "conv"), ("h", 7, 3, 1, 0, "conv"),
         ("i", 7, 2, 2, 0, "pool"), ("j", 6, 3, 3, 0, "conv"),
         ("k", 4, 2, 2, 0, "pool"), ("l", 4, 3, 1, 1, "conv")]

print(" #   n   k   s   p  kind   by hand   PyTorch  agree")
for tag, n, k, s, p, kind in CASES:
    hand = (n + 2 * p - k) // s + 1
    layer = (nn.Conv2d(1, 1, k, stride=s, padding=p) if kind == "conv"
             else nn.MaxPool2d(k, stride=s, padding=p))
    real = layer(torch.zeros(1, 1, n, n)).shape[-1]
    print(" %s %3d %3d %3d %3d  %-5s %7d %9d  %s"
          % (tag, n, k, s, p, kind, hand, real, "yes" if hand == real else "NO"))
```

**The real output, exactly:**

```text
 #   n   k   s   p  kind   by hand   PyTorch  agree
 a   8   3   1   0  conv        6         6  yes
 b   8   3   1   1  conv        8         8  yes
 c   8   2   2   0  pool        4         4  yes
 d   8   5   1   0  conv        4         4  yes
 e   8   5   1   2  conv        8         8  yes
 f   8   3   2   0  conv        3         3  yes
 g   8   3   2   1  conv        4         4  yes
 h   7   3   1   0  conv        5         5  yes
 i   7   2   2   0  pool        3         3  yes
 j   6   3   3   0  conv        2         2  yes
 k   4   2   2   0  pool        2         2  yes
 l   4   3   1   1  conv        4         4  yes
```

**Runtime: under one second.**

**The four rows to talk about, and it is worth doing in Week 26's first two minutes:**

- **(b), (e) and (l) all give the starting size back.** `k=3, p=1` (on an 8 and on a 4) and `k=5, p=2`. **The pattern is `p = (k − 1) ÷ 2`**, so `k=3 → p=1`, `k=5 → p=2`, `k=7 → p=3`. A student who spots that has found same padding by themselves and should be told so.
- **(f) and (i) both need rounding down**, and they are the two rows most people get wrong. Both come out to `2.5 → 2`.
- **(i) with an odd input:** 7 is odd, so a 2×2 pool cannot halve it evenly. It gives 3, not 3.5 and not 4. **The last column of the picture is simply dropped**, and that is worth knowing before it happens to somebody's data.
- **(j) has stride 3 and a window of 3**, which means the windows do not overlap at all: squares 0–2, then 3–5. Two positions, no double-counting. **Stride equal to the window size is exactly the non-overlapping case, which is what pooling almost always does.**

### Page 25.5 — Break it on purpose

*Build the stack. Put a deliberately wrong number in the `Linear` after the flatten. Run it. Paste the real error. Label both numbers.*

**The file:**

```python
"""stack.py - deliberately mis-size the Linear layer."""
import torch
import torch.nn as nn

torch.manual_seed(0)
batch = torch.zeros(4, 1, 8, 8)
net = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32, 10))          # <-- wrong on purpose: should be 64
logits = net(batch)
print(tuple(logits.shape))
```

**The real traceback, first and last lines:**

```text
Traceback (most recent call last):
  File "/private/tmp/w25f/stack.py", line 12, in <module>
    logits = net(batch)
  ...
  File ".../torch/nn/modules/linear.py", line 116, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (4x64 and 32x10)
```

**The labels:**

- **`4`** — the batch size. **Mine**, but harmless: it is how many pictures I put in.
- **`64`** — **from the picture.** `16 channels × 2 × 2 = 64`. The flatten produced it and I cannot change it without changing the stack.
- **`32`** — **mine.** I typed `nn.Linear(32, 10)`. **This is the number to change.**
- **`10`** — **mine**, and correct: ten digits, ten scores.

**The sentence: how you would have known without running anything.** *"Walk the ladder. 8×8 → pad-1 conv keeps 8×8 → pool gives 4×4 → pad-1 conv keeps 4×4 → pool gives 2×2, with 16 channels. So the flatten is 16 × 2 × 2 = 64, and `Linear` must start at 64."*

**Marking notes.** **Both labels must be there.** A pasted traceback with no labels is a screenshot, and say so: *"which of those two numbers is written in your file?"* And accept any wrong number they chose — 32, 128, 100, whatever — as long as the labelling is right. **A student who chose 128 and correctly labelled the 64 as coming from the picture has met the objective exactly.**

### Page 25.6 — Two sentences with numbers in them

**Padding — a full-marks answer:**

> *"Padding is a ring of zeros round the outside so the window can reach the edge pixels. With one ring, a window-3 stride-1 conv takes an 8 to an 8 instead of dropping it to 6 — so you can stack layers without the picture disappearing. And it means the corner pixel sits inside 4 windows instead of 1, where a middle pixel sits inside 9, so the corners stop being ignored."*

**Stride 2 — a full-marks answer:**

> *"Stride 2 makes the window jump two squares instead of one, so on 8 squares you get 3 window starts instead of 6 and the answer comes out half the size. What it costs you is the 3 windows you skipped — you never looked at those positions. And the picture itself did not shrink: it is still 8 squares. You just looked at it half as often."*

**Marking notes.** **A number in each sentence, or it comes back.** The three numbers that earn full marks are: **8 stays 8 instead of 6** (padding's size job), **1 window versus 4** (padding's fairness job), and **6 starts become 3** (stride's cost). Any two of the three is secure; all three is level 4. **And mark hard on "the picture shrinks" for stride** — it does not, and the misconception causes real confusion when they meet a stride-2 conv in a diagram.

### Page 25.7 — Stretch: how much of the picture does the last cell see?

*Switch on one pixel at a time and find out which pixels can change the top-left cell of the final 2×2 feature map.*

```python
import numpy as np
import torch
import torch.nn as nn

back = nn.Sequential(nn.Conv2d(1, 1, 3, padding=1, bias=False), nn.MaxPool2d(2),
                     nn.Conv2d(1, 1, 3, padding=1, bias=False), nn.MaxPool2d(2))
with torch.no_grad():
    for p in back.parameters():
        p.fill_(1.0)

mask = np.zeros((8, 8), dtype=int)
for r in range(8):
    for c in range(8):
        x = torch.zeros(1, 1, 8, 8)
        x[0, 0, r, c] = 1.0
        if back(x)[0, 0, 0, 0].item() != 0:
            mask[r, c] = 1
print("pixels that can change the TOP-LEFT cell of the final 2x2 map:")
print(mask)
print("count:", mask.sum(), "of 64")
```

**The real output:**

```text
pixels that can change the TOP-LEFT cell of the final 2x2 map:
[[1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [1 1 1 1 1 1 1 0]
 [0 0 0 0 0 0 0 0]]
count: 49 of 64
```

**The answer: the top-left 7×7 — 49 of the 64 pixels.** That region is the **receptive field** of that cell.

**And the good follow-up, which is why this is the stretch:** *"why not all 64?"* Because that cell is in the corner, so its window is clipped by the edge of the picture. **A cell in the middle of a bigger picture would see 10×10.** Two convs and two pools reach further than the 8×8 picture is wide, which is why the last layer of this stack can, in effect, look at nearly the whole digit at once — whereas one cell of a single conv layer sees only a 3×3 patch.

**Do not turn this into a formula.** The count is the lesson.

### Answers to every question posed in the lesson

**Hook — "which of those four numbers did a person choose?"** The `10` (ten digits, ten answers) and the `4` (four pictures in the batch) are both choices. The argument is between the `64` and the `32`. **The `64` came out of the picture — `16 × 2 × 2`. The `32` was typed, and typed wrong.**

**Hook — "how would you find out which?"** Read the code, and work the ladder out on paper. Or, faster: `print(h.shape)` on the line before the flatten. **A shape error fails identically every time, so there is no rush and nothing to reproduce.**

**Concept — "how many numbers did you just say?"** Six. **"And what was the last one?"** Five. **The gap between five and six is the `+1`, and it exists because the count started at zero.**

**Concept — "why couldn't the card start at square 6?"** Because the window is 3 wide, so from start 6 it would need squares 6, 7 and 8, and there is no square 8. **The last legal start is `8 − 3 = 5`.**

**Concept — "how do I get from 'last start is 5' to 'six starts'?"** Add one, for the start at zero. Fence posts.

**Concept — stride 2, "how many?"** Three: starts 0, 2 and 4. `(8 − 3) ÷ 2 = 2.5`, rounded **down** to 2, then `+ 1 = 3`. **Half of six.**

**Concept — "why round down and not to the nearest?"** Because 2.5 jumps would put the window half off the end of the paper. Try it with the card.

**Concept — padding, "how many positions?"** Eight, starts 0 to 7 on the padded row. `(8 + 2 − 3) ÷ 1 + 1 = 8`. **Same size in, same size out.**

**Concept — "how many windows does the corner sit inside?"** Without padding, **1**; with one ring, **4**; a middle pixel, **9**, either way.

**Live-code step 1 — "`img.shape` is `(8, 8)`. What will `x.shape` be?"** `(1, 1, 8, 8)`. Two `unsqueeze(0)` calls glue two 1s on the front. **Conv2d only accepts `(batch, channels, height, width)`.**

**Live-code step 3 — "it printed your shape back at you. What is it complaining about?"** It wants 3 or 4 numbers in the shape and got 2: `got input of size: [8, 8]`. **The shape it needs is printed in the message.**

**Live-code step 4 — "which number is the same on every single line?"** The batch size, 4. **Nothing you do to a picture changes how many pictures you have.**

**Live-code step 6 — "which number did I type?"** The `32`. **"Where did the 64 come from?"** `16 × 2 × 2`. The mistake was saying "16 channels of 2 by 2, that's 32" — multiplying by one 2 and forgetting the other.

**Wrap — the two sentences.** Padding: one ring keeps 8 at 8 instead of 6, and takes the corner from 1 window to 4. Stride 2: six starts become three, so the answer halves; the picture is unchanged, you looked at it half as often.

**Variation-harder 1 — a third block, then a fourth pool.** Third pad-1 conv with 32 filters: `(4, 32, 2, 2)`. Third pool: `(4, 32, 1, 1)`, and the flatten would be `32 × 1 × 1 = 32`. **A fourth pool errors:** `RuntimeError: Given input size: (32x1x1). Calculated output size: (32x0x0). Output size is too small.`

**Variation-harder 2 — the pad-free ladder.** `8 → 6` (conv), `→ 3` (pool), `→ 1` (conv), and then the pool fails. **So an 8×8 picture supports only one complete pad-free conv-pool block: the second conv fits, but the pool after it fails.** That is the arithmetical reason padding exists.

**Variation-harder 3 — stride-2 conv versus conv-then-pool.** `Conv2d(8, 16, 3, stride=2, padding=1)` on `(4, 8, 8, 8)` gives `(4, 16, 4, 4)` — identical to conv-then-pool. **What differs is that the strided conv has weights and can learn what to keep, while the pool always keeps the biggest.** Which is better is not settled; see the Questions section.

**Variation-harder 4 — a flatten of exactly 100.** `25 × 2 × 2 = 100`: two pad-1 convs with 25 filters in the second, and two pools. Also `100 × 1 × 1` with three pools and 100 filters, and `4 × 5 × 5` if you use unpadded convs on a bigger picture. **Several right answers, all checkable by running it.**

**Variation-harder 5 — the receptive field.** The top-left 7×7, **49 of 64 pixels**, clipped by the corner. Code and output on page 25.7.

---

## 🔮 Next Week Preview

Next week the filters stop being random. The same stack the class predicted the shapes for this week gets `nn.CrossEntropyLoss`, `torch.optim.Adam`, and 1,257 real handwritten digits from `load_digits` — and in **about three seconds** it goes from noise to **529 of 540 held-out digits read correctly**, with only **1,898 weights**, which is a number the class computes by hand before printing it. Then the two moments that make the week: `CrossEntropyLoss` takes **ten raw scores** and not ten probabilities — with the arithmetic to prove it, because handing it the squashed numbers turns a loss of `0.0244` into `1.4818` and nothing goes red — and then the eight first-layer filters get rendered at eight times magnification and **the class votes on what each one is looking for before anybody says a word.** Two of them turn out to be edge detectors, and nobody programmed that.

**To prep early:** three things. **One — leave THE SHAPE LADDER sheet up.** Week 26 walks the same six shapes in its first two minutes and adds the parameter count to each row; redrawing it costs eight minutes of a lesson that needs all seventy. **Two — check the PARAMETER COUNT sheet from Week 22 has a spare row**, because Week 26 adds `CNN: 1,898` right under `64 → 64 → 10: 4,810`, and putting those two numbers side by side is the single best moment of the week. **Three — run next week's `digits_cnn.py` tonight, on the machine you will teach from, and time it.** It takes about three seconds here, but a slow laptop can take twelve, and you want to know which before you say a number out loud to a room.
