# Week 26 — A Network That Reads Digits

[⬅ Week 25](week-25.md) · [Course Home](../README.md) · [Week 27 ➡](week-27.md) · [Student Guide](../student-guide/week-26.md) · [Workbook](../workbook/week-26.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the shortest real CNN there is, trained live, and then you look inside it |
| **Big idea** | Once shapes stop being a mystery, a CNN is a **short stack** — conv, squash, pool, repeat, flatten, classify. It trains in three seconds on 1,257 real digits, and **its first-layer filters are pictures you can look at**. Nobody drew them. |
| **New vocabulary** | logits (ten of them) · argmax · softmax · Adam · parameter count · learned filter |
| **New maths** | **None.** Everything today is a multiply, an add, a count and one logarithm the student met in Week 14. This week practises Weeks 14, 21, 22, 23 and 25. |
| **New syntax** | `nn.CrossEntropyLoss()` · `logits.argmax(dim=1)` · `torch.optim.Adam(model.parameters(), lr=1e-3)` · `sum(p.numel() for p in model.parameters())` |
| **Dataset** | `load_digits()` reshaped to `(1797, 1, 8, 8)` and divided by 16. **It ships inside scikit-learn. Nothing downloads. No internet needed. No torchvision.** |
| **Materials** | Printed workbook pages 26.1–26.7 · the **PARAMETER COUNT** sheet from Week 22, with one blank row left · **THE SHAPE LADDER** sheet from Week 25, still up · **a big blank sheet headed FILTER VOTE with eight numbered boxes** · the Bug Log · Week 23's dense-MLP numbers to hand |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn, matplotlib, **torch**. **No new installs.** |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `digits_cnn.py` trains 40 epochs of 40 steps in **about 3 seconds** on this machine — up to about 12 on a slow laptop. `filters.py` trains both networks and writes a PNG in **about 4 seconds**. **Time it on your own machine before you say a number out loud.** |

> **⚠️ Watch out:** the trap door this week is `nn.CrossEntropyLoss`. **It applies the softmax for you, internally.** If a student squashes the ten scores themselves and hands the *probabilities* to the loss, **nothing goes red** — the loss just reads around 1.48 instead of 0.02 for a confident correct answer, the model trains badly, and it looks like a bad architecture. This is the same shape of bug as Week 22's double sigmoid, and it will come back in Week 33. **Show it on purpose, with both numbers on the screen, or you will be silently debugging it for three more weeks.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build and train the CNN** on `load_digits` to about 98% test accuracy in under fifteen seconds, and **report the number with the split named**: "0.9796 on 540 held-out rows, trained on 1,257".
2. **Explain why `CrossEntropyLoss` takes ten raw scores rather than ten probabilities**, and say where the softmax went — with the two loss numbers (`0.0244` and `1.4818`) as the evidence.
3. **Render the eight learned first-layer filters as pictures** and describe what at least two of them appear to respond to, **with a number** — not "it looks edgy" but "it answers +2.830 to a bright-left edge and −1.219 to a bright-top one".
4. **Compare the CNN against the Week 23 dense MLP** on parameters, seconds, train accuracy and test accuracy, and **say which of the four comparisons actually matters** and why.

Observable evidence: `digits_cnn.py` printing `parameters: 1898` and `test accuracy : 0.9796 (529 of 540 test rows)`; workbook page 26.1 with the three per-layer parameter counts computed by hand **before** printing; `filters.png` saved to disk with two filters described numerically; and a four-row comparison table with one sentence naming the row they would put in a report.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There is one logarithm, and the student met it in Week 14 as the surprise meter. There are three multiplications for the parameter count. Everything else is Weeks 21 to 25 with pictures in it. What you need from your prep is (a) exactly what `CrossEntropyLoss` does that a student cannot see, and (b) how to talk about a learned filter honestly without over-claiming.

### 1. The whole network, in one picture, with every number on it

The stack is the one they predicted the shapes for last week. Nothing about it is new except that the numbers inside it are now going to change.

![One digit becomes ten scores](../figures/fig-w26-1-cnn-stack-with-shapes-annotated.svg)
*Figure 26.1 — One digit becomes ten scores. Spatial size goes down, channel count goes up, and 80 + 1,168 + 650 = 1,898 weights in the whole network.*

**The weight counts, and do these three by hand right now** — page 26.1 asks the student to do exactly this before printing it, and you cannot mark it if you have not done it.

> **A conv layer's weight count:**
> ```
> (in_channels × k × k × out_channels)  +  out_channels
>                                          └── one bias per filter
> ```

```text
conv1  Conv2d(1, 8, 3)   :  1 × 3 × 3 × 8  + 8  =    72 + 8  =    80
conv2  Conv2d(8, 16, 3)  :  8 × 3 × 3 × 16 + 16 =  1152 + 16 =  1168
fc     Linear(64, 10)    :         64 × 10 + 10 =   640 + 10 =   650
                                                             -------
total                                                           1898
```

**And the thing to say out loud twice: the conv counts do not contain the picture size anywhere.** `1 × 3 × 3 × 8 + 8` has no 8×8 in it. The same 80 weights would work on a 200×200 photograph. The `Linear` layer is the only part of the network that cares how big the picture was, and it cares completely — that is why last week's arithmetic mattered.

Compare with Week 23's dense network on the same digits: `64 → 64 → 10` is `64 × 64 + 64 = 4,160` plus `64 × 10 + 10 = 650`, which is **4,810**. So the CNN does the same job with **2,912 fewer weights**, and the difference is entirely that a conv layer reuses its nine numbers at every position instead of learning a fresh weight per pixel.

### 2. Ten logits, one argmax, and where the softmax went

This is the part of the week you must be able to teach without hesitating, because the trap door is here.

The network's last layer is `nn.Linear(64, 10)`. So for each picture it produces **ten numbers**. Not ten probabilities — ten plain numbers, positive or negative, of any size at all.

> **Logits** — the raw, unsquashed scores a network produces, one per class. There are ten of them here, one per digit. They are not probabilities: they do not add up to 1 and they can be negative.

Here are the real ten for one held-out digit, straight off the screen:

```text
[-10.94   4.46 -10.63  -4.69  -0.29  -7.80  -7.97  -3.30   0.14  -1.70]
```

> **Argmax** — "which slot holds the biggest number?" Not the biggest number itself: **its position.** Here the biggest is `4.46` and it is in slot 1, so `argmax` is **1**, and the model's answer is *the digit one*. The true label is also 1.

![Ten scores, one winner](../figures/fig-w26-2-ten-logits-into-one-argmax.svg)
*Figure 26.2 — Ten scores, one winner. The biggest of the ten is 4.46 in slot 1; squashed it becomes a chance of 0.9759, and the loss is −ln(0.9759) = 0.0244.*

> **Softmax** — the step that turns ten raw scores into ten chances that add up to 1. Bigger score → bigger chance, and the biggest score always gets the biggest chance, so **softmax never changes the argmax.**

**Here is the whole softmax on those ten numbers, done by hand, and it is worth doing once yourself.** You do it in three steps. First subtract the biggest score from all of them, which changes nothing about the answer and stops the arithmetic exploding:

```text
biggest = 4.46
slot 1:   4.46 − 4.46 =   0.00     e^0.00    = 1.000000
slot 8:   0.14 − 4.46 =  −4.32     e^−4.32   = 0.013300
slot 4:  −0.29 − 4.46 =  −4.75     e^−4.75   = 0.008652
slot 9:  −1.70 − 4.46 =  −6.16     e^−6.16   = 0.002112
slot 7:  −3.30 − 4.46 =  −7.76     e^−7.76   = 0.000426
slot 3:  −4.69 − 4.46 =  −9.15     e^−9.15   = 0.000106
the other four are all smaller than 0.00001 — call them zero
                                    ---------
                              total  1.024606
```

Then divide each by the total. For the winner:

```text
chance of digit 1  =  1.000000 ÷ 1.024606  =  0.9760
```

Then the loss, which is Week 14's surprise meter applied to the chance you gave the *right* answer:

```text
loss  =  −ln(0.9760)  =  0.0243
```

**PyTorch prints `0.9759` and `0.0244`**, because it used the full-precision scores rather than our two-decimal versions. **That is a rounding gap of one in the last place, and pointing it out is worth doing: your paper agrees with the machine to three decimals, and the fourth is the two decimals you threw away.**

Now the part that matters:

> **`nn.CrossEntropyLoss` does the softmax itself, inside, and then takes the log.** So you hand it the **ten raw scores**. If you softmax them first, you have squashed twice, and the numbers are wrong.

Here is the evidence, and it is the single most important pair of numbers this week:

```text
loss on the RAW scores      : 0.0244      ← correct
loss on the squashed numbers: 1.4818      ← wrong, and nothing warns you
```

**No error. No warning. Nothing red.** The loss just sits at about 1.48 for an answer the model got completely right, so every gradient is wrong, and the network trains badly for a reason that is invisible.

**Why 1.4818 and not something obviously silly?** Because after one softmax the ten numbers are all between 0 and 1 — quite close together. Squash *those* and you get ten numbers that are all near 0.1, so the loss is close to `−ln(0.1) = 2.303`, the loss of a model that is guessing. **The bug makes a confident model look like a guessing model.** That is exactly why it is so hard to spot: it does not crash, it just makes everything mediocre.

> **🧑‍🏫 If a student asks:** *"if the softmax is inside the loss, how do I ever get probabilities out?"* You call it yourself, at the end, when you want to *show* somebody a chance: `torch.softmax(logits, dim=1)`. **Just never on the way into the loss.** The rule that covers both: **the loss gets logits; humans get probabilities.**

### 3. Adam, in one honest paragraph

Since Week 21 the student has used `torch.optim.SGD`, which does exactly what they wrote by hand in Week 15: `w ← w − lr × slope`, the same learning rate for every weight, for ever.

> **Adam** — an optimiser that keeps a separate, automatically-adjusted step size for each individual weight, based on how that weight's slopes have been behaving recently. Weights whose slopes have been small and steady get bigger steps; weights whose slopes have been large and jumpy get smaller ones.

**You do not need to teach how it does that, and you must not.** What you need to say, and it is enough:

- **It is the same five-line loop.** `zero_grad`, forward, loss, `backward`, `step`. Nothing about the loop changes. Only the name in one line changes.
- **`lr=1e-3` is Adam's usual starting point**, and it is written `1e-3` rather than `0.001` because that is how everybody writes it and the student will see it that way in every example they ever read. `1e-3` means `0.001`.
- **It converges much faster on this problem.** That is the whole reason we swap: 40 epochs of Adam gets to 98%, and plain SGD at the same learning rate would still be crawling.
- **It is not magic and it is not always better.** There is a real, ongoing argument about whether Adam generalises as well as well-tuned SGD on big problems. Say so if asked; do not pretend it is settled.

> **🧑‍🏫 If a student asks "why not always use Adam then?"** Honest answer: *"most people mostly do, and it is a completely reasonable default. But it keeps two extra numbers per weight, so it uses three times the memory, and on some large problems carefully-tuned plain SGD ends up slightly better on the test set. Nobody fully agrees about why."*

### 4. Every new line of this week's code, explained to somebody who has never programmed

Four new lines. Here they are with nothing assumed.

**New line 1 — counting the weights.**

```python
print("parameters:", sum(p.numel() for p in model.parameters()))
```

Read it inside out. `model.parameters()` hands back every block of learnable numbers in the network, one block at a time — the conv weights, the conv biases, the linear weights, the linear bias. `p.numel()` is "**num**ber of **el**ements": how many individual numbers are in this block. `sum(...)` adds them all up. **So the whole line is "go through every block of weights, count the numbers in it, add them up."**

It prints `1898`. And the student computed 1,898 on paper five minutes earlier. **That agreement is the point of the line.**

**New line 2 — the loss for ten classes.**

```python
loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(model(xb), yb)
```

`model(xb)` gives the ten raw scores per picture — shape `(32, 10)` for a batch of 32. `yb` is the true labels — shape `(32,)`, and each entry is a plain whole number from 0 to 9. **Not one-hot, not a probability: the digit itself.**

`CrossEntropyLoss` then, for each row: softmaxes the ten scores, picks out the chance it gave the true label, takes minus the natural log of it, and averages over the batch. **One number out.**

**Two dtype traps and both are in the Clinic.** The labels must be `long` (whole numbers), or you get `expected scalar type Long but found Float`. And the labels must be shape `(32,)`, not `(32, 1)`, or you get `0D or 1D target tensor expected, multi-target not supported`.

**New line 3 — turning ten scores into one answer.**

```python
pred = logits.argmax(dim=1)
```

`dim=1` means "look along the row". The tensor is `(540, 10)` — 540 pictures, ten scores each — so `dim=1` runs across the ten and returns the position of the biggest, giving `(540,)`: one answer per picture.

**`dim=0` would be a disaster and it produces no error.** It would look *down* each column across all 540 pictures and answer "which picture had the highest score for digit 3?" — ten numbers instead of 540. It is in the Clinic and it is worth demonstrating.

**New line 4 — the optimiser.**

```python
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
```

Same shape as Week 21's `SGD([w], lr=0.1)`. You hand it the things it is allowed to change — `model.parameters()`, all 1,898 of them — and how big a step to take. **`model.parameters()` and not `model`**: hand it the model itself and you get `TypeError: optimizer can only optimize Tensors, but one of the params is torch.nn.modules.conv.Conv2d` (a `Sequential` is iterable, so PyTorch walks its layers and complains about the first one).

### 5. What you will actually see on the screen, with the real numbers

**This is the real output of `digits_cnn.py`. You will see exactly this, except the `seconds` line.**

```text
pictures: (1797, 8, 8)   labels: (1797,)
darkest pixel: 0.0   brightest pixel: 1.0
train rows: 1257   test rows: 540
train tensor: (1257, 1, 8, 8)   test tensor: (540, 1, 8, 8)
parameters: 1898
steps per epoch: 40
epoch  1  train loss 2.2796
epoch 10  train loss 0.3488
epoch 20  train loss 0.1467
epoch 30  train loss 0.0922
epoch 40  train loss 0.0663

seconds        : 3.1
train accuracy : 0.9881  (1242 of 1257 train rows)
test accuracy  : 0.9796  (529 of 540 test rows)
```

**Six things in there, and the second is the one to slow down on.**

1. **`darkest pixel: 0.0   brightest pixel: 1.0`.** We divided by 16 because `load_digits` stores brightness as a whole number from 0 to 16. **Dividing by 16 is this week's entire preprocessing step**, and it is Week 4's scaling idea in one character. If you skip it the network still trains, just worse and slower — worth mentioning, not worth demonstrating.
2. **`epoch 1 train loss 2.2796`.** Look at that number and compare it to `ln(10) = 2.3026`, which is the loss of a model picking one of ten at random. **2.2796 is barely better than random**, and it should be, because at the start of epoch 1 the eight filters are the random noise Week 25 ended on. **This is a free sanity check you should install as a habit: a ten-class network's first loss should be close to 2.30. If it starts at 0.4, something is leaking. If it starts at 8, something is broken.**
3. **`steps per epoch: 40`.** 1,257 rows at 32 at a time. `1257 ÷ 32 = 39.28`, so 39 full batches of 32 and one last batch of 9, which is 40. Week 23 already made them do this arithmetic three ways; do it once out loud again.
4. **`parameters: 1898`.** Matches the paper. Point at the PARAMETER COUNT wall sheet.
5. **`train accuracy 0.9881` against `test accuracy 0.9796`.** A gap of about one point. **That is a small and healthy gap** — Week 22's overfitting lesson said to watch it, and this is what "not much overfitting" looks like: 1,242 of 1,257 at home, 529 of 540 on the exam.
6. **`529 of 540`.** Always print the counts next to the ratio. `0.9796` sounds precise; `529 of 540` tells you that one more correct answer would move it to 0.9815, so the fourth decimal place is not real.

### 6. The learned filters, and how to talk about them honestly

This is the payoff of the week and it is also the place where it is easiest to say something untrue.

After training, `model[0].weight` holds the eight 3×3 filters. Rendered as pictures, they look like this — light cells are positive weights, dark cells are negative:

![The eight filters it taught itself](../figures/fig-w26-3-eight-learned-filters-enlarged.svg)
*Figure 26.3 — The eight filters it taught itself. Filter 6's left column is all positive and its right column all negative; a bright-left edge scores +2.830 and a bright-top edge −1.219.*

**Filter 6, all nine numbers:**

```text
  0.509  −0.129  −0.149
  0.382  −0.507  −0.767
  0.761   0.348  −0.550
```

**Left column: all three positive. Right column: all three negative.** So it adds up what is on the left and subtracts what is on the right. Slide it over a place where the picture is bright on the left and dark on the right and it produces a big positive number; slide it over a flat region and the pluses and minuses cancel. **That is a vertical edge detector, and nobody wrote it. Gradient descent found it.**

**And here is how to make that claim checkable rather than a story.** Build two test patches — one bright on the left, one bright on the top — and multiply them against each filter. The real numbers:

| filter | answer to a bright-LEFT edge | answer to a bright-TOP edge | what that suggests |
|---:|---:|---:|---|
| 0 | +0.750 | −1.651 | mildly prefers left-bright; dislikes top-bright |
| 1 | −1.887 | −3.428 | **negative to everything** — it fires on blank paper, not ink |
| 2 | −0.956 | −0.032 | likes ink but not a left-right split |
| 3 | +0.543 | +0.158 | weak, no clear preference |
| **4** | +0.503 | **+3.760** | **a horizontal edge detector: bright above, dark below** |
| 5 | −0.876 | +0.212 | weak |
| **6** | **+2.830** | −1.219 | **a vertical edge detector: bright left, dark right** |
| 7 | +2.916 | +3.041 | likes both — its nine weights are positive except the bottom-right two, so it is best read as an **ink-total** filter (weights sum to +2.837), not a clear corner detector |

**Say the honest version out loud, because it is better teaching than the tidy version:**

> "Two of the eight are clearly edge detectors and you can prove it with a number. One of them, filter 1, is negative almost everywhere — it responds to *the absence of ink*, which is a perfectly sensible thing to measure and not what anybody would have thought to hand-design. And three or four of them are weak and hard to describe, and if I tell you a confident story about filter 3 I am making it up."

That last sentence is the one that separates teaching from performance. **A 3×3 filter is nine numbers. Some of them mean something clear. Some of them do not, and pretending otherwise teaches students that interpretation is storytelling.**

### 7. The three misconceptions you will actually meet

**Misconception 1 — "softmax is part of the model."**
It is not, and this is the week's trap door. In our stack the model ends at `nn.Linear(64, 10)` and its output is ten raw scores. The softmax lives **inside the loss** during training, and **in your own code** when you want to show a human a percentage. **Cure:** put the two loss numbers on the screen side by side — `0.0244` and `1.4818` — and say *"same picture, same answer, same model. One of those two is what happens if you squash first."*

**Misconception 2 — "the model outputs probabilities, so the biggest one is the answer."**
Half right: the biggest one *is* the answer. But it does not output probabilities, and the distinction matters because a student who believes it will hand probabilities to the loss. **Cure:** show the ten raw scores. There is a `−10.94` in there. **A probability cannot be −10.94.**

**Misconception 3 — "98% means it basically works."**
It means 529 of 540, so **11 held-out digits were read wrong**. Whether that is fine depends entirely on what the reading is for — a postcode sorter reading 11 addresses wrong in 540 is a bad afternoon for eleven people. **Cure:** print the counts beside the ratio, always, and name the split. This is Week 8's discipline, unchanged, and next week takes it further by naming *which* eleven.

### 8. How deep to go, and where to stop

**Go this far:** the parameter count by hand and then printed; the ten logits and the argmax; why the loss takes logits, with both numbers; Adam as a name and a faster step; training live; rendering the eight filters and describing two of them with numbers; the four-row comparison against Week 23.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **The confusion matrix, and which digits it confuses** | **Week 27, next week.** Somebody will ask "which ones did it get wrong?" and it is a great question. Answer: *"eleven of them, and next week we find out exactly which and why."* **Do not build a confusion matrix today** — it is next week's opening move and you will spend fifteen minutes you do not have. |
| Data augmentation | **Week 27.** |
| Transfer learning, freezing, `requires_grad = False` | **Week 27.** |
| How Adam actually works (moments, decay rates) | **Nowhere in this level.** It needs running averages of squared gradients and it would eat the lesson. The honest line: *"it keeps a separate step size per weight and adjusts them as it goes. How, exactly, is a level above this one."* |
| `nn.Dropout` | Week 22 taught it. It is deliberately **not** in this stack, because with 1,898 weights on 1,257 rows the train/test gap is one point and there is nothing to regularise. **If a student asks why there is no dropout, that is a level-4 question and the answer is the one-point gap.** |
| Validation splits for choosing the epoch count | **Already theirs since Week 2**, and worth one honest sentence — see the note in the live-code, step 4. Do not build one today; it costs ten minutes and the week has no hyperparameter to choose. |
| Saliency maps, feature visualisation beyond layer 1 | Not in this level. And be honest if asked: **layer 1 is the only layer that renders into something a human can read.** |
| CIFAR-10, colour images, `torchvision` | Not available offline. There is one callout about it in the student guide and it is optional. |

The line to hold in your head all lesson: **today the student trains a thing that can see, and then looks at what it decided to look for.** The measurement of *how* it fails is next week.

---

### 9. 🧭 The Growing Map — the same box, and the week it pays out

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week the gold box does not move, but for the first time in this tile it produces
something that works, and the two minutes should say so.

![The Level 3 pipeline in Week 26: still the images and CNNs tile, now a network that reads handwritten digits](../figures/fig-w26-0-where-this-fits.svg)

*Figure 26.0 — Week 26's version. Third week inside the gold `images · CNNs` tile. The ↻ on stage three is
black, as it has been since Week 12 — and today that loop ran 1,600 times in about three seconds.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "what did the last two weeks buy us?"** The box is the same
   gold tile, *images · CNNs*, third of four weeks. The answer to the second question is on two wall
   sheets: **THE SHAPE LADDER** from Week 25 gave them the number after `Flatten`, and **PARAMETER COUNT**
   now has its last row filled in — **1,898** against Week 23's **4,810**. *"Two weeks of pencil work, and
   today it assembled into ninety-eight per cent on handwriting."*
2. **Anchor it on the FILTER VOTE sheet.** Hold up the eight numbered boxes. *"Nobody in this room drew any
   of those. They are the only part of a neural network you can look at directly, and you looked at them
   the same way a researcher does."* Then the one honest caveat, which they should hear from you and not
   from the internet: layer 1 renders, layer 2 onwards does not.
3. **Point at the ↻ on stage three and then at stage five.** The ↻ has been black since Week 12, and today
   it turned a network with 1,898 weights into a digit reader using the **same five lines from Week 21**.
   Stage five is still dashed: *"nothing today was about shipping. That is Weeks 34 to 36, and by then this
   will be the easy part of your project."*

> **🧑‍🏫 Why this is worth two minutes.** This is the most satisfying week of the term and the easiest one
> to mis-remember as magic. The map is the antidote: point at the two white tiles to the left and name what
> came from where — the loop from stage three, the loss from Week 14, the `DataLoader` from Week 23, the
> sizes from last week. *"There is nothing in today's file that we have not built. That is why it worked
> the first time."*

**One thing to notice, so you can answer if asked.** `evaluation` is lit again, for the first time since
Term 1, alongside `model`. It is lit because of the four-row comparison table against Week 23 — parameters,
seconds, train accuracy, test accuracy — and specifically because objective 4 asks them to say **which of
the four actually matters**. That judgement, not the 0.9796, is the evaluation work this week. If a student
puts *seconds* in their report, ask them who the report is for.

---

## 🧰 Prep Checklist

### 25 minutes the night before

- [ ] **Do the three parameter counts by hand.** Three minutes. `1 × 3 × 3 × 8 + 8 = 80`. `8 × 3 × 3 × 16 + 16 = 1168`. `64 × 10 + 10 = 650`. Total `1898`. **Write them on a sticky note.** Page 26.1 is these three sums and you will be marking twelve of them.
- [ ] **Type and run `digits_cnn.py` yourself, and time it.** The complete file:

```python
"""digits_cnn.py - a network that reads digits."""
import time

import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)
np.random.seed(0)

# ---------- 1. the pictures ----------
digits = load_digits()
X = digits.images / 16.0
y = digits.target
print("pictures:", X.shape, "  labels:", y.shape)
print("darkest pixel:", X.min(), "  brightest pixel:", X.max())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=0, stratify=y)
print("train rows:", len(X_train), "  test rows:", len(X_test))

Xtr = torch.from_numpy(X_train).float().unsqueeze(1)
Xte = torch.from_numpy(X_test).float().unsqueeze(1)
ytr = torch.from_numpy(y_train).long()
yte = torch.from_numpy(y_test).long()
print("train tensor:", tuple(Xtr.shape), "  test tensor:", tuple(Xte.shape))

# ---------- 2. the model ----------
model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(64, 10),
)
print("parameters:", sum(p.numel() for p in model.parameters()))

# ---------- 3. the loop ----------
loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=32, shuffle=True)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
print("steps per epoch:", len(loader))

t0 = time.perf_counter()
for epoch in range(1, 41):
    model.train()
    total = 0.0
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        total += loss.item() * len(yb)
    if epoch % 10 == 0 or epoch == 1:
        print("epoch %2d  train loss %.4f" % (epoch, total / len(ytr)))
seconds = time.perf_counter() - t0

model.eval()
with torch.no_grad():
    tr_acc = (model(Xtr).argmax(dim=1) == ytr).float().mean().item()
    te_pred = model(Xte).argmax(dim=1)
    te_acc = (te_pred == yte).float().mean().item()
print()
print("seconds        : %.1f" % seconds)
print("train accuracy : %.4f  (%d of %d train rows)"
      % (tr_acc, int((model(Xtr).argmax(1) == ytr).sum()), len(ytr)))
print("test accuracy  : %.4f  (%d of %d test rows)"
      % (te_acc, int((te_pred == yte).sum()), len(yte)))

# ---------- 4. one row of ten scores ----------
with torch.no_grad():
    logits = model(Xte[:1])
print()
print("the ten raw scores for test picture 0:")
print(np.round(logits.numpy()[0], 2))
print("argmax  :", logits.argmax(dim=1).item(), "   true label:", yte[0].item())
probs = torch.softmax(logits, dim=1)
print("squashed:", np.round(probs.numpy()[0], 4))
print("they add up to:", round(probs.sum().item(), 6))
print("loss on the RAW scores      : %.4f" % loss_fn(logits, yte[:1]).item())
print("loss on the squashed numbers: %.4f" % loss_fn(probs, yte[:1]).item())
print("minus ln of the true chance : %.4f"
      % (-torch.log(probs[0, yte[0]])).item())
```

Run `python3 digits_cnn.py`. You must see **exactly** this, except the `seconds` line:

```text
pictures: (1797, 8, 8)   labels: (1797,)
darkest pixel: 0.0   brightest pixel: 1.0
train rows: 1257   test rows: 540
train tensor: (1257, 1, 8, 8)   test tensor: (540, 1, 8, 8)
parameters: 1898
steps per epoch: 40
epoch  1  train loss 2.2796
epoch 10  train loss 0.3488
epoch 20  train loss 0.1467
epoch 30  train loss 0.0922
epoch 40  train loss 0.0663

seconds        : 3.1
train accuracy : 0.9881  (1242 of 1257 train rows)
test accuracy  : 0.9796  (529 of 540 test rows)

the ten raw scores for test picture 0:
[-10.94   4.46 -10.63  -4.69  -0.29  -7.8   -7.97  -3.3    0.14  -1.7 ]
argmax  : 1    true label: 1
squashed: [0.000e+00 9.759e-01 0.000e+00 1.000e-04 8.400e-03 0.000e+00 0.000e+00
 4.000e-04 1.300e-02 2.100e-03]
they add up to: 1.0
loss on the RAW scores      : 0.0244
loss on the squashed numbers: 1.4818
minus ln of the true chance : 0.0244
```

**Expected runtime: about 3 seconds on this machine, up to about 12 on a slow laptop. Time yours and write the number down**, because you are going to say it out loud in the hook and being wrong by a factor of four in front of the class is avoidable.

**If your accuracy is not 0.9796, one of the seeds is missing.** `torch.manual_seed(0)` before the model is built, and `random_state=0, stratify=y` in the split. Both matter.

- [ ] **Run `filters.py` too** — the complete file is in the Answer Key under page 26.5. It trains both networks and saves `filters.png`. **Open the PNG and look at it before the lesson.** You need to have seen the eight smudges so you are not surprised by how unimpressive they are at first glance. **They are unimpressive until you put a number on them, which is the point.**
- [ ] **Break it on purpose, twice.**
  1. `loss_fn(torch.softmax(logits, dim=1), yte[:1])` gives **1.4818**, no error, no warning. This is deliberate mistake one.
  2. `logits.argmax(dim=0)` on a batch of 540 gives ten numbers instead of 540, no error at all. This is deliberate mistake two.
- [ ] **Print workbook pages 26.1–26.7.**
- [ ] **Put up the FILTER VOTE sheet:** one big sheet, eight numbered boxes, nothing else. The class writes their guesses in the boxes **before** you say anything.
- [ ] **Check both wall sheets are still up:** THE SHAPE LADDER from Week 25 (you walk it in the first two minutes) and PARAMETER COUNT from Week 22 (you add one row to it). **Make sure PARAMETER COUNT has a blank row under `64 → 64 → 10 | 4810`.**

### 5 minutes on the day

- [ ] Editor open, terminal ready. `digits_cnn.py` **deleted or renamed** — they type it.
- [ ] `matplotlib` set to write files, not windows. `matplotlib.use("Agg")` is in `filters.py` already; check it runs headless.
- [ ] FILTER VOTE sheet on the wall, eight empty boxes.
- [ ] THE SHAPE LADDER and PARAMETER COUNT both visible from every seat.
- [ ] Workbook 26.1 out. **The three parameter sums done in pen before any code runs.**
- [ ] Bug Log out.

### Fallback if the laptops fail

**This week needs a computer for the training run, and there is no way round that.** But three of the four objectives survive on paper, and the fourth survives if you can print one thing.

1. **The parameter count, by hand.** Page 26.1 is three multiplications. **Objective 4's most important row, complete, in ten minutes**, and it is the row that does not need a machine: 1,898 against 4,810.
2. **The ten logits and the argmax.** Write the real ten numbers on the board from §2 of this file. *"Which is biggest? Which slot is it in? What does the model think this digit is?"* **Objective 2's first half, on paper.**
3. **The softmax by hand.** The three-step arithmetic in §2 — subtract the max, exponentiate, divide — needs a calculator with an `e^x` key and nothing else. Then `−ln(0.9760) = 0.0243`. **Objective 2, complete**, and honestly it lands *better* by hand than on a screen.
4. **The filters, from Figure 26.3.** Print it, or project it from this file. The nine numbers of filter 6 are on it, and the vote works exactly as designed: *"left column all positive, right column all negative. What is it looking for?"* **Objective 3, complete, with the +2.830 as the evidence.**
5. **Objective 1 is the casualty.** Say so: *"the one thing we cannot do without a machine is watch it learn. It takes three seconds and it is your homework."*

| If this fails | Do this instead |
|---|---|
| `parameters:` prints something other than 1898 | Count the layers. The commonest cause is a third conv block copied in by accident, or a wrong `Linear` size (`Linear(32, 10)` prints `parameters: 1578` and only fails later, on the first forward pass). |
| Accuracy is about 0.10 and the loss never falls | Nothing is learning: `opt.step()` or `loss.backward()` is missing, or the labels are wrong. (Softmaxed numbers handed to the loss do **not** do this - that model learns, badly. One-hot labels raise an error.) **0.10 on ten classes is chance.** |
| Accuracy is 0.9796 but seconds is 40, not 3 | Slow laptop, and it is fine. Say the real number. **Never read this file's 3.1 out as if it were theirs.** |
| The loss starts at 0.4 instead of 2.28 | Something has leaked, or the model was already trained (the cell was run twice). **Restart and rerun. A ten-class network cannot honestly start below about 2.3.** |
| `filters.png` is eight grey squares that look like nothing | **That is correct and expected.** They are nine pixels each. Go straight to the numbers: the bright-left and bright-top answers in §6. **The numbers are the evidence; the picture is the hook.** |
| A student wants to know which digits it got wrong | *"Eleven of them, and next week we find out exactly which and why — that is the whole first half of Week 27."* **Do not build a confusion matrix today.** |

---

## ⏱️ The Lesson, Minute by Minute

This section is the plan to teach from, segment by segment. The table gives the shape; the steps below give the words.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — 1,898 Numbers That Have Never Seen a Digit | 7 | 7 | The parameter count on paper; the wall sheet; the claim |
| 🧠 Concept — Ten Scores, and Where the Softmax Went | 18 | 25 | Logits, argmax, softmax by hand, the two loss numbers |
| 💻 Live-Code Together — `digits_cnn.py` | 18 | 43 | Data, model, loop, train live. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Filter Vote | 20 | 63 | Render the eight filters; vote before anybody speaks; then the numbers |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the four-row table, homework |

---

### 🪝 Hook — 1,898 Numbers That Have Never Seen a Digit (7 minutes)

**Do this:** Stand at THE SHAPE LADDER sheet from last week. Nothing on the screen.

**Say this:**

> "Last week you filled this in. Six shapes, `(4, 1, 8, 8)` down to `(4, 64)`, all of them from one division you worked out with a card.
>
> And at the end I said something you might not have noticed. **Every number we pushed through that stack was a zero, and the eight filters in the first layer were random noise.** PyTorch invented them when you built the layer. They had never seen a digit and they did not do anything useful.
>
> Today those numbers get chosen. And before we let anything choose them, I want to know **how many numbers there are.**"

**Do this:** Write the conv formula on the board:

```text
a conv layer's weights  =  (in × k × k × out)  +  out
                                                  └── one bias per filter
```

**Ask this:** "First layer: one channel in, eight filters, window 3 by 3. How many numbers?"

*Let them work it out. `1 × 3 × 3 × 8 = 72`, plus 8 biases, = 80.*

*If somebody says 72:* ask *"how many filters?"* Eight. *"So how many biases?"* Eight. **The biases are the thing that gets forgotten, every week, all year.**

**Ask this:** "Second layer: eight channels in, sixteen filters, 3 by 3."

*`8 × 3 × 3 × 16 = 1152`, plus 16, = 1,168.*

**Ask this:** "And the `Linear` at the end: 64 numbers in, 10 out."

*`64 × 10 = 640`, plus 10, = 650.*

**Do this:** Add them on the board, big:

```text
   80
 1168
  650
------
 1898
```

**Do this:** Walk to the PARAMETER COUNT sheet from Week 22 and write in the blank row: `CNN on digits: 1,898`. Point at the row above it: `64 → 64 → 10: 4,810`.

**Say this:**

> "Look at those two numbers next to each other. Week 23's dense network on the exact same digits: **4,810** weights. Today's network: **1,898**. **Less than half**, and the difference is not that we cut corners — it is that a conv layer uses the same nine numbers at every position in the picture instead of learning a fresh weight for every pixel.
>
> Now here is the claim, and you get to check it in about twenty minutes.
>
> **Those 1,898 numbers are random noise right now. In three seconds of training, on 1,257 handwritten digits, they will get good enough to read 529 out of 540 digits it has never seen.**
>
> Three seconds. And then — this is the part I actually care about — **we are going to draw the eight filters in the first layer as pictures and look at what it decided to look for.** Nobody tells it. Nobody hand-designs an edge detector. It works out that edges are worth measuring, from nothing but 1,257 digits and a slope."

**Ask this:** "What do you think a filter that has learned something useful looks like?"

*Take any answer. Write two or three guesses on the board. Do not evaluate them.*

> "Hold those. We will come back and check."

---

### 🧠 Concept — Ten Scores, and Where the Softmax Went (18 minutes)

**Say this:**

> "The last layer of this network is `Linear(64, 10)`. Sixty-four numbers in, **ten numbers out**. One per digit.
>
> And I want to be very careful about what those ten numbers are, because this is the one thing this week that goes wrong silently."

**Do this:** Write the real ten on the board, exactly:

```text
digit:      0      1      2      3      4      5      6      7      8      9
score:  −10.94  4.46 −10.63  −4.69  −0.29  −7.80  −7.97  −3.30   0.14  −1.70
```

**Ask this:** "What does this network think this digit is?"

*Hoped-for answer:* one.

**Ask this:** "How did you decide?"

*Hoped-for answer:* it is the biggest.

> "The biggest. **4.46.** And notice what you did: you did not care what the number *was*, you cared **which slot it was in.** That has a name."

**Do this:** Write on the board and box it:

> **argmax** — not the biggest number, but **the position** of the biggest number. Here the biggest is 4.46, in slot 1, so argmax = 1.

**Ask this:** "Now. Are those ten numbers probabilities?"

*Hoped-for answer:* no.

*If they say yes:* point at the `−10.94` and say nothing.

> "There is a **minus ten point nine four** in there. A probability cannot be negative and they do not add up to one. These are just... scores. Raw, unsquashed scores. They have a name too."

**Do this:** Write:

> **logits** — the raw scores a network produces, one per class. Not probabilities. They can be negative and they do not add to 1.

**Say this:**

> "Now, we do want probabilities eventually, because 'the model says 1' is less useful than 'the model says 1, and it is 97% sure'. So there is a step that turns ten scores into ten chances. It is called **softmax**, and we are going to do it by hand, right now, on those exact ten numbers, because you have all the maths you need."

**Do this:** Three steps on the board. Do them one at a time and let the room do the arithmetic.

> "**Step one. Subtract the biggest score from all of them.** Why? Because it changes nothing about which is biggest, and it stops the numbers exploding when we exponentiate. The biggest is 4.46, so:"

```text
slot 1:   4.46 − 4.46 =   0.00
slot 8:   0.14 − 4.46 =  −4.32
slot 4:  −0.29 − 4.46 =  −4.75
slot 9:  −1.70 − 4.46 =  −6.16
...and the rest are all below −7
```

> "**Step two. Put each one through e-to-the-power-of.** Same button you used in Week 13 for the S-curve. `e^0` is 1. `e^−4.32` is small. `e^−7` and below is basically nothing."

```text
e^0.00   = 1.000000
e^−4.32  = 0.013300
e^−4.75  = 0.008652
e^−6.16  = 0.002112
the rest add up to about 0.000541
                --------
          total   1.024606
```

> "**Step three. Divide each by the total.** Which for the winner is:"

```text
1.000000 ÷ 1.024606  =  0.9760
```

> "**97.6% sure it is a one.** And the other 2.4% is spread across the other nine, mostly on 8 and 4 — which, when you think about what a badly-written 1 looks like at eight pixels across, is not stupid.
>
> And one more line, and it is Week 14's surprise meter, unchanged. **How wrong were we?** Minus the log of the chance we gave the right answer:"

```text
loss  =  −ln(0.9760)  =  0.0243
```

> "0.0243. Nearly zero, because we were nearly certain and we were right. If we had said 0.10 — a pure guess between ten options — the loss would have been `−ln(0.10) = 2.30`. **Hold on to that 2.30. It is the number a fresh network starts at, and you will see it on the screen in ten minutes.**"

**Do this:** Now the trap door. Write on the board, and leave a gap:

```text
loss on the RAW ten scores      :  0.0244
loss on the SQUASHED ten numbers:  ?
```

**Say this:**

> "Here is the thing that catches everybody, including me, and it caught me while I was writing this lesson.
>
> **`CrossEntropyLoss` does the softmax itself. Inside. You never see it.** So you hand it the ten raw scores — the `−10.94` and the `4.46` — and it does all three steps we just did, plus the log, and gives you one number.
>
> So what happens if you helpfully squash them yourself first, and hand it the ten chances?"

**Ask this:** "Guess. Bigger, smaller, or an error?"

*Take votes. Most say error.*

> "**No error.** Nothing. No warning, no red text, no hint of any kind. It squashes your already-squashed numbers a second time, and the loss comes out..."

**Do this:** Fill in the gap:

```text
loss on the RAW ten scores      :  0.0244
loss on the SQUASHED ten numbers:  1.4818
```

> "**1.4818.** For a digit the model got completely right, with 97.6% confidence.
>
> And here is why that particular number is so nasty. After one softmax, the ten numbers are all between 0 and 1, so they are quite close together. Squash *those* and you get ten numbers all near 0.1 — which is what a **guessing** model looks like. `−ln(0.1)` is 2.30, and 1.48 is on the way there.
>
> **So the bug does not crash. It makes a confident model look mediocre.** You would spend an afternoon adding layers and changing learning rates, and the architecture was fine all along."

**Do this:** Write the rule on the board and leave it up all lesson:

> **The loss gets logits. Humans get probabilities.**

**Say this:**

> "One more new name and then we build it. Since Week 21 you have used `SGD` — 'take the slope, multiply by the learning rate, step'. Today we swap one word for another: **Adam**.
>
> All it does is keep **a separate step size for every single weight**, and adjust each one as it goes. A weight whose slope has been small and steady for a while gets a bigger step. A weight whose slope keeps flipping sign gets a smaller, more careful one.
>
> **How it does that is a level above this one and I am not going to pretend otherwise.** What you need to know is: it is the same five-line loop, the word `SGD` becomes `Adam`, `lr=1e-3` — which is just `0.001` written the way everybody writes it — and it gets there several times faster on this problem. That is the entire reason we are using it."

**Do this:** Hand out page 26.1 — the three parameter sums, in pen — and give them four minutes. Then page 26.2, the FILTER VOTE prediction: *"before we train anything, sketch what you think a useful 3×3 filter would look like."*

---

### 💻 Live-Code Together — `digits_cnn.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — the pictures, and the one preprocessing step.**

```python
"""digits_cnn.py - a network that reads digits."""
import time

import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)
np.random.seed(0)

digits = load_digits()
X = digits.images / 16.0
y = digits.target
print("pictures:", X.shape, "  labels:", y.shape)
print("darkest pixel:", X.min(), "  brightest pixel:", X.max())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=0, stratify=y)
print("train rows:", len(X_train), "  test rows:", len(X_test))

Xtr = torch.from_numpy(X_train).float().unsqueeze(1)
Xte = torch.from_numpy(X_test).float().unsqueeze(1)
ytr = torch.from_numpy(y_train).long()
yte = torch.from_numpy(y_test).long()
print("train tensor:", tuple(Xtr.shape), "  test tensor:", tuple(Xte.shape))
```

**Ask before running:** "Week 23 used `digits.data`, which was `(1797, 64)`. I'm using `digits.images`. What shape will that be?"

*Hoped-for answer:* `(1797, 8, 8)`.

Run it:

```text
pictures: (1797, 8, 8)   labels: (1797,)
darkest pixel: 0.0   brightest pixel: 1.0
train rows: 1257   test rows: 540
train tensor: (1257, 1, 8, 8)   test tensor: (540, 1, 8, 8)
```

> **Say this:** "Two things worth stopping on.
>
> **`digits.images` is `(1797, 8, 8)` and `digits.data` is `(1797, 64)`.** Same numbers. Same 1,797 digits. One of them has been flattened and one has not. **Week 23 used the flat one, because a dense layer wants a row. We want the square one, because a conv layer wants a picture.** Same data, two shapes, and the shape is the whole difference between the two networks.
>
> **`/ 16.0`.** `load_digits` stores brightness as a whole number from 0 to 16, and we divide so it runs 0 to 1 instead. That is Week 4's scaling in one character. It is not compulsory — the network trains without it, just worse — and it is the only preprocessing this whole week has.
>
> And `.unsqueeze(1)`: 1,257 pictures of 8 by 8 becomes 1,257 pictures of **1 channel** of 8 by 8. Last week's four numbers, in last week's order. Notice it is `unsqueeze(1)` and not `unsqueeze(0)` this time — the batch dimension is already there, so the channel goes in at position 1."

**Step 2 (3 min) — the model, and the number they already computed.**

```python
model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(64, 10),
)
print("parameters:", sum(p.numel() for p in model.parameters()))
```

**Ask before running:** "Page 26.1. What is it going to say?"

*1,898.*

```text
parameters: 1898
```

> **Say this:** "1,898, and you knew that before the machine did. **That is the whole reason we do the arithmetic on paper first** — the machine is confirming you, not informing you.
>
> Read the counting line inside out. `model.parameters()` hands back every block of learnable numbers, one at a time. `p.numel()` is 'number of elements' — how many numbers in this block. `sum` adds them up.
>
> And look at where the `64` came from in `Linear(64, 10)`. **Last week.** `16 × 2 × 2`. If you had written 32 there, this line would never have run."

**Step 3 (4 min) — the loop, which is Week 21's five lines.**

```python
loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=32, shuffle=True)
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
print("steps per epoch:", len(loader))

t0 = time.perf_counter()
for epoch in range(1, 41):
    model.train()
    total = 0.0
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        total += loss.item() * len(yb)
    if epoch % 10 == 0 or epoch == 1:
        print("epoch %2d  train loss %.4f" % (epoch, total / len(ytr)))
seconds = time.perf_counter() - t0
```

**Ask before running:** "1,257 rows, 32 at a time. How many steps per epoch?"

*`1257 ÷ 32 = 39.28`, so 39 full batches and one of 9: **40**.*

**Ask this, before it runs:** "And what will the loss be at the very start, before it has learned anything?"

*Hoped-for answer:* about 2.3, because `−ln(0.1) = 2.30`.

*If nobody gets it:* point at the board where `−ln(0.10) = 2.30` is still written.

Run it:

```text
steps per epoch: 40
epoch  1  train loss 2.2796
epoch 10  train loss 0.3488
epoch 20  train loss 0.1467
epoch 30  train loss 0.0922
epoch 40  train loss 0.0663
```

> **Say this:** "**2.2796.** And you predicted 2.30, which is what a model picking one of ten at random scores. **Install that as a habit right now: a fresh ten-class network's first loss should be close to 2.30.** If it starts at 0.4, something has leaked. If it starts at 8, something is broken. It is a free check and it costs you nothing.
>
> Then 0.35, 0.15, 0.09, 0.066. **Falling and flattening.** And the five lines in the middle are the exact five lines from Week 21 — `zero_grad`, forward, loss, `backward`, `step`. Nothing about the loop changed. Only what is inside the model."

> **🧑‍🏫 Say this out loud, honestly, because it matters:** "I print the training loss every ten epochs and then look at the test set once, at the end. **I did not use the test set to choose 40 epochs** — I chose 40 because the training loss had stopped falling much. If I had run it at 30, 40 and 50 and picked whichever gave the best *test* number, I would have been doing the thing Weeks 2 and 9 told you never to do. **Say what you chose and how you chose it, every time.**"

**Step 4 (3 min) — the accuracies, both of them, with counts.**

```python
model.eval()
with torch.no_grad():
    tr_acc = (model(Xtr).argmax(dim=1) == ytr).float().mean().item()
    te_pred = model(Xte).argmax(dim=1)
    te_acc = (te_pred == yte).float().mean().item()
print()
print("seconds        : %.1f" % seconds)
print("train accuracy : %.4f  (%d of %d train rows)"
      % (tr_acc, int((model(Xtr).argmax(1) == ytr).sum()), len(ytr)))
print("test accuracy  : %.4f  (%d of %d test rows)"
      % (te_acc, int((te_pred == yte).sum()), len(yte)))
```

```text
seconds        : 3.1
train accuracy : 0.9881  (1242 of 1257 train rows)
test accuracy  : 0.9796  (529 of 540 test rows)
```

> **Say this:** "**Three seconds.** 1,898 numbers that were random noise when the lesson started can now read **529 out of 540** handwritten digits they have never seen.
>
> Two accuracies, and always both. **0.9881 at home, 0.9796 on the exam.** A gap of about one point. That is Week 22's overfitting gap and **one point is a small, healthy gap** — the model has not memorised its homework, it has actually learned something.
>
> And the counts. `529 of 540`. **Always print the counts next to the ratio**, because `0.9796` looks precise to four decimal places and it is not: one more correct answer takes it to 0.9815. The fourth decimal is noise."

**Ask this:** "Eleven wrong. Which eleven?"

*Somebody will want to know.*

> "Best question of the lesson, and it is the whole first half of next week. **Next week we find out exactly which, and which pair of digits it cannot tell apart, and the physical reason why.** Today: eleven, and we know that honestly."

**Step 5 (2 min) — 🐞 DELIBERATE MISTAKE ONE: squash first.**

```python
with torch.no_grad():
    logits = model(Xte[:1])
print(np.round(logits.numpy()[0], 2))
probs = torch.softmax(logits, dim=1)
print("loss on the RAW scores      : %.4f" % loss_fn(logits, yte[:1]).item())
print("loss on the squashed numbers: %.4f" % loss_fn(probs, yte[:1]).item())
```

```text
[-10.94   4.46 -10.63  -4.69  -0.29  -7.8   -7.97  -3.3    0.14  -1.7 ]
loss on the RAW scores      : 0.0244
loss on the squashed numbers: 1.4818
```

**Do this:** Point at the board where you wrote the two numbers twenty minutes ago. They match.

**Ask this:** "Did anything go red?"

*No.*

> **Say this:** "Nothing. No error, no warning. **Same model, same picture, same correct answer, and two completely different losses.** One of them is right and one of them makes the model look like it is guessing.
>
> And you cannot tell which by looking at the code. You can only tell by knowing that **`CrossEntropyLoss` softmaxes for you.** Which is why it is on the board."

**Do this:** Bug Log entry, ninety seconds. **This is the most valuable entry of the week.** Message: *"no message at all"*. Meaning: *"the loss softmaxed my already-softmaxed numbers, so a confident model scored like a guessing one."* Fix: *"hand the loss the raw ten scores. Softmax only when a human is going to read the number."*

**Step 6 (2 min) — 🐞 DELIBERATE MISTAKE TWO: `dim=0`.**

> **Say this:** "One more, and this one is a single character."

```python
with torch.no_grad():
    all_logits = model(Xte)
print("shape of all the scores:", tuple(all_logits.shape))
print("argmax(dim=1) gives:", tuple(all_logits.argmax(dim=1).shape))
print("argmax(dim=0) gives:", tuple(all_logits.argmax(dim=0).shape))
```

```text
shape of all the scores: (540, 10)
argmax(dim=1) gives: (540,)
argmax(dim=0) gives: (10,)
```

**Ask this:** "540 pictures went in. Which of those two answers is one-per-picture?"

*`dim=1`.*

> **Say this:** "`dim=1` runs **along the row** — across the ten scores for one picture — and gives you 540 answers, one per picture. Correct.
>
> `dim=0` runs **down the column** — across all 540 pictures for one digit — and answers 'which picture had the highest score for digit 3?' Ten numbers. **Completely useless, and no error whatsoever.**
>
> The way to remember it: **`dim=1` is the dimension you want to collapse.** You have `(540, 10)` and you want `(540,)`, so you are getting rid of dimension 1. And the check that catches it every time: **count the answers. There should be one per picture.**"

---

### 🎲 Their Turn — The Filter Vote (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: render the eight learned filters at eight times magnification, put them on the wall, have the class vote on what each one is looking for **before you say a word**, and then test the two most confident votes with a real number.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Draw the four-row table on the board, and fill it in with the class.

| | CNN | dense MLP (Week 23) |
|---|---:|---:|
| parameters | 1,898 | 4,810 |
| seconds to train | 3.1 | 0.4 |
| train accuracy | 0.9881 | 0.9889 |
| test accuracy | **0.9796** | **0.9722** |

![Two networks, four rows](../figures/fig-w26-4-cnn-versus-dense-four-row-table.svg)
*Figure 26.4 — Two networks, four rows. 529 of 540 against 525 of 540, with 2,912 fewer weights — and four digits out of 540 is inside the wobble.*

**Ask this:** "Four rows. **Which one would you put in a report, and which one is the least honest?**"

*Take answers. The hoped-for one: test accuracy in the report; train accuracy is the least honest.*

**Say this:**

> "**Test accuracy goes in the report**, because it is the only row measured on digits the model has never seen. Train accuracy is the least honest row on the board — it is the model's mark on its own homework, and both networks score about 0.988 on it, which tells you nothing.
>
> And now the part I want you to be able to argue.
>
> **The CNN won the test row: 0.9796 against 0.9722.** In counts, that is **529 out of 540 against 525 out of 540. Four digits.**
>
> **Four digits out of 540 is inside the wobble.** Change the seed and it could go the other way. **So the honest sentence is not 'the CNN is more accurate'. It is 'the CNN matched it, four digits better, which is inside run-to-run noise.'**
>
> But look at the top row. **1,898 against 4,810. That is 2,912 fewer weights, and that is not inside any wobble at all** — it is exactly reproducible, and it comes from the fact that a conv layer reuses nine numbers everywhere instead of learning one per pixel. **So the row that actually matters here is the parameter count**, and the accuracy row is the row that gets over-claimed in write-ups.
>
> And the thing the parameter count is really telling you: **the CNN's 80 first-layer weights would work unchanged on a 200-by-200 photograph.** The dense network's 4,160 are welded to 8×8 for ever. On these tiny pictures that costs nothing. On a real photo it is the difference between a network that fits on a phone and one that does not."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "Two things to take away.
>
> **One.** `CrossEntropyLoss` does the softmax for you. **The loss gets logits. Humans get probabilities.** And if you get it wrong, nothing goes red — the loss just goes from 0.02 to 1.48 and your model looks mediocre.
>
> **Two.** Nobody designed those filters. **Two of the eight are edge detectors and we proved it with a number.** In 1990 that was somebody's PhD. Today it took three seconds and 1,257 digits.
>
> And next week: eleven digits out of 540 came back wrong. **Next week we find out which eleven, we find the one pair the model genuinely cannot tell apart, and then we buy back accuracy two ways without collecting a single new picture.**"

**Do this:** Hand out the homework and read the third part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `RuntimeError: expected scalar type Long but found Float` | "The labels have to be whole numbers and yours are decimals." | `torch.from_numpy(y_train).float()` instead of `.long()`. **Pictures are floats; labels are longs.** | `ytr = torch.from_numpy(y_train).long()`. Say the rule out loud: `.float()` for the `X`, `.long()` for the `y`. |
| `RuntimeError: Expected floating point type for target with class probabilities, got Long` | "You gave me a grid of 0s and 1s where I wanted a list of digits." | Labels one-hot encoded into shape `(32, 10)`. | `CrossEntropyLoss` wants **the digit itself**: a `(32,)` tensor of whole numbers 0–9. No one-hot anywhere in PyTorch. |
| `RuntimeError: 0D or 1D target tensor expected, multi-target not supported` | "The labels are shaped `(32, 1)` and I want `(32,)`." | An extra `unsqueeze` on the labels, or a reshape copied from a regression example. | `yb.squeeze()`, or just do not unsqueeze the labels. **Only the pictures need extra dimensions.** |
| `IndexError: Target 10 is out of bounds.` | "You said 10 classes and handed me a label of 10." | Labels 1–10 instead of 0–9, usually after adding 1 somewhere. | Labels must run `0` to `n_classes − 1`. Ten classes means labels 0–9. Check `y.min()` and `y.max()`. |
| `TypeError: optimizer can only optimize Tensors, but one of the params is torch.nn.modules.conv.Conv2d` | "You handed the optimiser the model, not its weights." | `torch.optim.Adam(model, lr=1e-3)`. | `torch.optim.Adam(model.parameters(), lr=1e-3)`. **The `()` on `parameters` is doing real work.** |
| `RuntimeError: mean(): could not infer output dtype. Input dtype must be either a floating point or complex dtype. Got: Bool` | "You averaged a list of true/falses." | `(pred == y).mean()` — comparing gives Booleans, and you cannot average those. | `(pred == y).float().mean()`. Turn the trues into 1.0 first. |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x64 and 32x10)` | Last week's error, back again. | `nn.Linear(32, 10)`. The 64 came from `16 × 2 × 2`; the 32 you typed. | `nn.Linear(64, 10)`. **Week 25's whole lesson, and it will keep happening — which is why Week 25 exists.** |
| **No error. The loss falls slowly (about 1.6 after 20 epochs where it should be about 0.4) and test accuracy ends a couple of points low (0.937 against 0.961).** | Nothing crashed. Every gradient was computed from a double-squashed number. | `loss_fn(torch.softmax(logits, dim=1), yb)`. | Hand the loss the **raw** logits. **The loss gets logits; humans get probabilities.** Note the 2.30 check does **not** catch this one: a fresh double-squashed network also starts near 2.30. |
| **No error. `argmax` returns 10 numbers instead of 540.** | Nothing crashed. Your accuracy is computed from nonsense. | `argmax(dim=0)` instead of `argmax(dim=1)`. | `dim=1`. **Then count the answers: there must be one per picture.** |
| **No error. Accuracy is about 0.10 (chance) and the loss never moves off 2.30.** | Nothing crashed. Nothing learned. | `opt.step()` missing (or `loss.backward()` missing), or the optimiser was built from the wrong list so no weights are in it. (A missing `zero_grad()` is a *different* silent bug: gradients pile up and the model still learns, just badly - 0.78 test accuracy on this network.) | Check the five lines are all present and in order. Then `print(len(list(model.parameters())))` — this network has **6** blocks of weights (two convs with weight+bias, one linear with weight+bias). |
| **No error. Train accuracy is 0.988 and test accuracy is 0.34.** | Nothing crashed. | The test tensor was built from the *training* rows, or the split was done twice with different seeds. | One split, one seed, and print all four row counts. **1257 + 540 = 1797.** Make the addition every time. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and two of them are about errors that never announce themselves.

20. **"What should the loss be before it has learned anything?"** For ten classes, `−ln(1/10) = 2.30`. **A first loss far from 2.30 is a bug, and this check costs nothing and catches a broken loop, a leak and a wrong class count. It does NOT catch the double-softmax, which also starts near 2.30 - that one needs the "is there a softmax before the loss?" question.**

21. **"Count the answers."** For any `argmax`, ask how many answers came out and how many pictures went in. If they differ, it is `dim`.

22. **"Print the counts, not just the ratio."** `0.9796` invites four decimal places of false confidence. `529 of 540` invites the correct question, which is *"how much would one more move it?"*

And the sentence for this week:

> **"The two worst bugs this week produce no message at all. One makes a good model look mediocre; the other makes a broken model look fine. Both are caught by two numbers you can predict in advance: the loss should start near 2.30, and there should be one answer per picture."**

---

## 🎲 The Activity, In Full

This section describes the week's activity in full, so you can run it without opening anything else.

### The Filter Vote

**What it is.** Train the network, pull out the eight 3×3 filters it learned, render them big, put them on the wall, and **have the class vote on what each one is looking for before the teacher says a single word.** Then test the two most confident votes against a real number.

The point is not that they guess right. **The point is the order: look, guess, then measure.** A student who has committed to a guess in public reads the measurement completely differently from one who was told the answer.

### Setup

- The FILTER VOTE sheet on the wall: eight numbered boxes, nothing else in them.
- Workbook page 26.2 (their pre-training sketch of what a useful filter might look like) already filled in from the concept segment.
- Workbook page 26.3: eight boxes matching the wall, plus a column headed `and the number says`.
- `filters.py` typed and ready to run, or given out complete if time is tight.

### Part 1 — render the eight filters (5 minutes)

They add this to the end of their file. **`matplotlib.use("Agg")` goes at the very top of the file, before `import matplotlib.pyplot`,** or you get a window nobody asked for.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

w = model[0].weight.detach().numpy()[:, 0]
print("first-layer weight shape:", tuple(model[0].weight.shape))
print("filter 6, all nine numbers:")
print(np.round(w[6], 3))

fig, axes = plt.subplots(1, 8, figsize=(12, 2))
for i, ax in enumerate(axes):
    ax.imshow(w[i], cmap="gray", interpolation="nearest")
    ax.set_title("filter %d" % i, fontsize=9)
    ax.axis("off")
fig.suptitle("the eight 3x3 filters conv1 learned")
plt.tight_layout()
plt.savefig("filters.png", dpi=110)
plt.close(fig)
print("saved filters.png")
```

```text
first-layer weight shape: (8, 1, 3, 3)
filter 6, all nine numbers:
[[ 0.509 -0.129 -0.149]
 [ 0.382 -0.507 -0.767]
 [ 0.761  0.348 -0.55 ]]
saved filters.png
```

**`.detach()` means "give me the numbers and drop the gradient bookkeeping".** Without it, numpy refuses: `RuntimeError: Can't call numpy() on Tensor that requires grad`. Say it once; it is a one-word fix they will need all year.

**`[:, 0]` drops the input-channel dimension**, turning `(8, 1, 3, 3)` into `(8, 3, 3)` — eight 3×3 grids — because our pictures have only one channel.

**`interpolation="nearest"` is load-bearing.** Without it matplotlib smooths the nine pixels into a blur and you cannot see which cell is which.

### Part 2 — everybody looks, nobody speaks (4 minutes)

Open `filters.png`. Project it, or have everybody open their own.

> **"Four minutes. Look at all eight. Do not say anything out loud. On page 26.3, for each one, write down in a few words what you think it is looking for — and if you have no idea, write 'no idea'. 'No idea' is a real answer and I want to see it where it is true."**

**Sit on your hands and say nothing.** The urge to help here is enormous and you must resist it.

**Be ready for the honest reaction, which is disappointment.** They are nine grey pixels. They look like smudges. If somebody says so out loud, agree:

> **"Yes. They are nine numbers each and they look like nothing much. That is exactly why we are about to put a number on them instead of trusting our eyes."**

### Part 3 — the vote (5 minutes)

Go box by box on the wall sheet. For each filter, take one or two descriptions and **write them in the box, without comment.** Where there is disagreement, write both. Where the room says "no idea", **write "no idea" in the box** — that is data.

**What you will actually get, roughly:**

- Filter 4 and filter 6 attract confident, specific answers — "light on top dark on the bottom", "light on the left".
- Filter 1 attracts "it's all dark" and confusion, because it is negative nearly everywhere.
- Filters 3 and 5 attract "no idea", and correctly.

### Part 4 — test the two most confident votes (6 minutes)

> **"Right. Two of you were confident. Let's find out."**

Build two test patches and slide each filter over them:

```python
vert = np.array([[1., 1., -1.], [1., 1., -1.], [1., 1., -1.]])   # bright LEFT
horiz = vert.T                                                    # bright TOP
print("filter   bright-LEFT edge   bright-TOP edge")
for i in range(8):
    print("  %d      %+14.3f   %+12.3f"
          % (i, (w[i] * vert).sum(), (w[i] * horiz).sum()))
```

```text
filter   bright-LEFT edge   bright-TOP edge
  0              +0.750         -1.651
  1              -1.887         -3.428
  2              -0.956         -0.032
  3              +0.543         +0.158
  4              +0.503         +3.760
  5              -0.876         +0.212
  6              +2.830         -1.219
  7              +2.916         +3.041
```

**Then, and this is the moment, do one of them by hand on the board so the number is not magic.** Filter 6 against the bright-left patch, row by row:

```text
row 0:  0.509 × 1  +  (−0.129) × 1  +  (−0.149) × (−1)  =  0.509 − 0.129 + 0.149  =  +0.529
row 1:  0.382 × 1  +  (−0.507) × 1  +  (−0.767) × (−1)  =  0.382 − 0.507 + 0.767  =  +0.642
row 2:  0.761 × 1  +    0.348  × 1  +  (−0.550) × (−1)  =  0.761 + 0.348 + 0.550  =  +1.659
                                                                                    -------
                                                                                     +2.830
```

**Read out the three answers that matter:**

- **Filter 6: `+2.830` to a bright-left edge, `−1.219` to a bright-top one.** It is a vertical edge detector. **Whoever voted "light on the left" was right, and here is the number.**
- **Filter 4: `+3.760` to a bright-top edge, `+0.503` to a bright-left one.** The same idea, rotated. A horizontal edge detector.
- **Filter 1: `−1.887` and `−3.428`. Negative to everything.** It fires on **blank paper**, not on ink. Nobody would think to hand-design that, and it is a perfectly sensible thing to measure.

**And say the honest thing about filters 3 and 5:**

> **"Three and five answer less than one unit to either patch, with no clear preference, which is nearly nothing. They are weak, and I cannot tell you a story about them. If I did, I would be making it up. Two of the eight are clearly edge detectors, one is a blank-paper detector, and three or four of them do something I cannot name. That is the honest result and it is what the picture actually shows."**

### What "finished" looks like

- `filters.png` saved to disk and looked at.
- Page 26.3 with eight guesses, including at least one honest "no idea".
- The FILTER VOTE wall sheet filled in, in the class's words, with disagreements left in.
- Two filters described **with a number**: "filter 6 answers +2.830 to a bright-left edge and −1.219 to a bright-top one, so it is a vertical edge detector."
- One row of the `+2.830` arithmetic worked out by hand.
- The student can say, unprompted: *"nobody chose those numbers."*

### Variation — easier

**Skip the rendering entirely and go straight to the nine numbers.** Print filter 6 and filter 4 as grids of numbers and ask one question about each:

```text
filter 6:                      filter 4:
  0.509  −0.129  −0.149          −0.185   0.784   0.742
  0.382  −0.507  −0.767           0.469   0.383  −0.196
  0.761   0.348  −0.550          −0.105  −0.977  −0.681
```

> **"Which column of filter 6 is all positive? Which is all negative? So what is it adding up and what is it subtracting?"**
>
> **"Now filter 4. Not columns — rows. Which row is positive and which is negative?"**

Left column positive, right column negative → adds the left, subtracts the right → **vertical edge**. Top row positive, bottom row negative → **horizontal edge**. **That is objective 3, complete, with no picture and no code at all**, and it is arguably clearer than the rendering.

**And pre-print the response table** so the only thing left is to circle the two biggest numbers in it.

### Variation — harder

1. **Find the filter that likes a diagonal.** Build `diag = np.array([[1,1,-1],[1,-1,-1],[-1,-1,-1]], dtype=float)` and score all eight against it. Then the honest question: *"is the winner a diagonal detector, or does it just like anything with a lot of ink on the top left?"* **Test it: score the same filter against an all-ink patch of nines and see whether the diagonal answer was actually special.** Filter 7 is the interesting one here — it answers well to almost everything, which is a warning about over-reading.
2. **Score every filter against a plain all-ink patch** (`np.ones((3,3))`). The answer is just the sum of the filter's nine weights. Filter 2 gives **+3.463** and filter 1 gives **−1.707**, and neither is an edge detector at all. **The lesson: some filters measure "how much ink is here", which is useful and boring.**
3. **Retrain with a different seed and render again.** `torch.manual_seed(1)`. Some of the eight filters will look similar and some completely different, and **the order will certainly change** — filter 6 will not be the vertical one any more. Then the real question: *"if the numbering changes, what is actually stable?"* **The set of things measured, roughly, but not which slot measures what. That is a level-5 insight and it is why people plot all the filters rather than picking one.**
4. **Sixteen filters instead of eight.** `Conv2d(1, 16, 3, padding=1)` and update the second conv's input. Predict the new parameter count before printing it: conv1 becomes `1 × 3 × 3 × 16 + 16 = 160`, conv2 becomes `16 × 3 × 3 × 16 + 16 = 2320`, total `160 + 2320 + 650 = 3130`. **Then the honest measurement: does the test accuracy actually improve?** Usually barely, and finding that out is worth more than the improvement would have been.
5. **The softmax by hand, on all ten.** The full three-step arithmetic is in the Answer Key under page 26.7. **Then the check: do the ten chances add to exactly 1.0000?** They must, and if they do not, the arithmetic is wrong somewhere.

---

## ❓ Questions Students Ask This Week

**"Why doesn't the model just output probabilities? It seems like extra work."**

Two reasons, and the second is the real one.

**One: you do not always need them.** If all you want is the answer, the argmax of the raw scores is the same as the argmax of the probabilities — softmax never changes which one is biggest. So squashing is wasted work at prediction time.

**Two, and this is why it is built this way: doing the softmax and the log together, inside the loss, is numerically safer.** Look back at our ten scores. There is a `−10.94` in there, and `e^−10.94` is about 0.0000177. On a bigger network you can get scores of +100 or −110: `e^100` is bigger than the biggest number the computer's format can hold, so it becomes `inf` (and `inf ÷ inf` is `nan`), while a chance as small as `e^−110` rounds to exactly zero, and then `ln(0)` is minus infinity and your training run fills up with `nan`. (`e^−40` is tiny, about 4 × 10⁻¹⁸, but still representable - the trouble starts around ±90 to ±100.) **`CrossEntropyLoss` rearranges the arithmetic so that never happens.** This is the same reason Week 22's loss was called `BCEWithLogitsLoss`: the words "with logits" in a loss name mean *"give me the raw scores and I will do the squash safely."*

**"How does Adam actually work?"**

It keeps two running averages for every single weight: roughly, how big the recent slopes have been, and how much they have been jumping around. Then it takes a big step where the slope has been small and consistent, and a small careful step where it has been large and erratic.

**Beyond that, honestly, is a level above this one**, and I would rather say so than give you a sentence that sounds like an explanation and is not. What you can take now: **it is the same five-line loop, and `lr=1e-3` is the number to start at.**

**And one honest caveat, because it matters:** Adam is not automatically better. It keeps two extra numbers per weight, so it uses about three times the memory, and on some large problems a carefully tuned plain SGD ends up slightly better on the test set. **Nobody fully agrees about why.** Most people use Adam most of the time and that is a reasonable default, not a proof.

**"Only 98%? I thought these things were amazing."**

**98% of 540 is 529 right and 11 wrong**, and whether that is amazing depends completely on what you are doing with it.

Reading postcodes: 11 letters in 540 going to the wrong town is a bad day for eleven people, and real postal sorters run several nines rather than two. Reading a hobby project's scanned notebook: completely fine.

**And be honest about the data too.** These are 8×8 pictures — sixty-four pixels, less than the icons on your phone. A human reading them gets some wrong as well. **A big part of the remaining 2% is not the model being stupid; it is the pictures not containing enough information.** Next week we look at exactly which eleven and you will see that for yourself.

**"Could I train it for longer and get 100%?"**

You can get the **training** accuracy to 100%, fairly easily, and that is the trap. Train for 200 epochs and it will memorise all 1,257 training digits perfectly, and the test accuracy will sit where it is or drift down. **That is Week 22's overfitting, and it is why we always report the two numbers together.**

The interesting version of your question is: *what would raise the **test** number?* Three honest answers. **More pictures** — which is next week's first half, and you can manufacture some. **A model that starts from something already trained** — next week's second half. **Or more pixels**, which is the one we cannot do, because 8×8 is what we have.

**"Why 8 filters? Why not 3, or 50?"**

Genuinely a choice, and mostly a habit. **Here is the honest reasoning behind 8 for this lesson:** it is enough that different filters can specialise, it is small enough that all eight fit on one row of a figure and a class can vote on them in five minutes, and it keeps the network at 1,898 weights so the parameter count is something a person can hold in their head.

**And you can test it.** Variation-harder 4 doubles it to 16, which takes the network to 3,130 weights, and the test accuracy barely moves. **On this data, 8 is already enough**, and finding that out yourself is worth more than being told a rule. On a real photograph the first layer usually has 32 or 64, because there are far more useful things to measure in a colour photo than in a 64-pixel digit.

**"Which is better, the CNN or the dense network?"** *(Nobody fully agrees, and here is why.)*

**On this data, honestly: it is a draw on accuracy and a win for the CNN on size, and anybody who tells you the CNN is clearly better on 8×8 digits is over-claiming.**

Look at the numbers. 529 of 540 against 525 of 540. **Four digits.** With 540 test rows, the run-to-run wobble on an accuracy near 0.97 is roughly ±0.7 points either way, so four digits is inside it. Change the seed and it might flip. **The correct sentence is "they are level".**

Where the CNN wins is not in doubt: **1,898 weights against 4,810**, exactly reproducible, and — more importantly — the conv layers' weight counts **do not depend on the picture size at all.** Those 80 first-layer weights would work on a 200×200 photograph. The dense network's 4,160 are welded to 8×8 for ever, and on a 200×200 colour photo the equivalent dense layer would need about 7.7 million.

**So why is it a draw here?** Because an 8×8 digit is so small that there is barely any "structure" left to exploit. The whole argument for convolution is that nearby pixels are related and a feature worth finding in one corner is worth finding in another — and at 8×8 the digit fills the frame, so there is almost no "elsewhere" for a feature to move to. **Convolution's advantage grows with the picture. On sixty-four pixels it has almost no room to show up.**

**And that is the genuinely unsettled part.** There is an active argument in the field about how much of a CNN's advantage on real images is the locality assumption and how much is just that the architecture happens to be easy to optimise — and recent architectures that throw the locality assumption away do very well *if you give them enough data*. **Nobody has a clean experiment that separates those two explanations, and the answer probably depends on how much data you have.** What you should do about that: report both rows, name the split, and say which difference is inside the noise. That is the whole professional skill.

**"Are the filters always edge detectors?"**

**No, and it is worth being precise.** Two of our eight clearly are. One (filter 1) fires on blank paper. One (filter 2) mostly measures how much ink is present. And three or four do something I cannot name honestly.

**What is consistently true across every image network anybody has looked at** is that the first layer tends to learn *local, simple, orientation-sensitive things* — edges, blobs, brightness gradients — because those are the most useful nine-degrees-of-freedom measurements you can make about a small patch of any natural picture. That is a real and slightly startling result: it is roughly what neuroscientists recorded in cat visual cortex in 1959.

**But the second layer already renders into something no human can read**, and by the tenth layer, interpretation is guesswork with pictures attached. **Layer 1 is the only layer you get to look at. Be suspicious of anybody who claims otherwise.**

---

## ⚠️ Where This Lesson Goes Wrong

This section lists the ways this lesson tends to slip, and what to do when it happens.

| What happens | Why | What to do right now |
|---|---|---|
| **The double-softmax is explained but never shown** | It is abstract and the lesson is running late | **Show the two numbers.** `0.0244` and `1.4818`, on the same screen, on the same picture. It is ninety seconds and it is the reason the week has a Watch-out box. Cut the `dim=0` demo before you cut this one. |
| Softmax gets taught as "part of the model" | Every diagram on the internet draws it on the end of the network | Say the rule three times: **"the loss gets logits, humans get probabilities."** Then write it on the board and leave it there all lesson. |
| The parameter count gets printed before anybody computes it | It is one line and it is right there | **Do page 26.1 in pen first.** The value of `parameters: 1898` is entirely that it agrees with a number the student already owns. Printed first, it is trivia. |
| The biases get forgotten in the count | 72 and 1,152 are the interesting products; the `+8` and `+16` feel like decoration | *"How many filters?"* Eight. *"How many biases?"* Eight. **A total short by exactly 8 + 16 + 10 = 34 is the missing-biases error**, and it is the same error Week 22 flagged. Same feedback, every week, until it stops. |
| The training run is announced as "three seconds" and takes forty | You read this file's number instead of your own | **Time it on your machine the night before and say YOUR number.** A slow laptop is not a failure and the class does not care — but being wrong by a factor of ten in front of them costs you something. |
| Somebody asks which digits it got wrong and the lesson becomes Week 27 | It is the obvious question and it is a good one | *"Eleven of them. Next week we find out exactly which, and why, and it is the whole first half of the lesson."* **Do not build a confusion matrix today.** It costs fifteen minutes and it steals next week's hook. |
| The filters are rendered and the room is disappointed | They are nine grey pixels and they look like smudges | **Agree out loud**, immediately: *"yes, they look like nothing. That is why we are about to put a number on them."* Then go to the +2.830. **The number is the payoff, not the picture.** |
| A confident story gets told about filter 3 | Teachers hate saying "I don't know" in front of a class | Say it anyway, and say why: *"filter 3 answers +0.54 and +0.16 to the two patches, which is nearly nothing. I cannot tell you what it does. If I made something up, I would be teaching you that interpretation is storytelling."* **This is the single most valuable sentence in the activity.** |
| `matplotlib` opens a window and blocks the whole class | `matplotlib.use("Agg")` was not at the top of the file | It must come **before** `import matplotlib.pyplot as plt`, at the very top. Then `plt.savefig(...)` and open the PNG. **Never an interactive window.** |
| The test row gets read as "the CNN is better" | 0.9796 beats 0.9722 and that is what winning looks like | **Convert to counts, out loud: 529 against 525. Four digits out of 540.** Then ask *"would you bet on that surviving a different seed?"* **The parameter count is the row that is not inside the noise, and saying so is the professional skill.** |
| Adam becomes a twenty-minute detour into moments and decay rates | A strong student read the docs | *"It keeps a separate step size per weight and adjusts them as it goes. Exactly how is a level above this one, and I would rather say that than give you a sentence that sounds like an explanation."* **Then move.** |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the softmax by hand. The two loss numbers — `0.0244` and `1.4818` — carry objective 2 on their own. *"The loss does a squash for you; if you squash first it squashes twice and the number goes wrong."* That is the objective; the ten exponentials are the proof.

**Cut:** the filter rendering, and go straight to the nine numbers of filters 6 and 4 (Variation-easier). **It is arguably better teaching anyway** and it needs no matplotlib.

**Cut:** the `dim=0` demonstration.

**Give them `digits_cnn.py` complete.** Every bit of the learning today is in the parameter count, the two loss numbers and the filters, and none of it is in typing an import block.

**The version of the arithmetic that skips everything hard.** Three multiplications and an addition, with the structure pre-written:

| Layer | in | window | out | Weights | Biases | Total |
|---|---:|---:|---:|---|---|---|
| conv1 | 1 | 3 × 3 | 8 | 1 × 3 × 3 × 8 = | 8 | |
| conv2 | 8 | 3 × 3 | 16 | 8 × 3 × 3 × 16 = | 16 | |
| linear | 64 | — | 10 | 64 × 10 = | 10 | |
| | | | | | | **grand total** |

Three rows. **Every multiplication is already written out; they only do the arithmetic.** Then one question: **"which layer has the most weights, and is it the one you expected?"** conv2, with 1,168 — and no, most people expect the `Linear`. **That is objective 4's key row, delivered with a calculator.**

**The copy-this-exactly scaffold.** Eleven lines, and it runs on its own:

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
scores = torch.tensor([[-10.94, 4.46, -10.63, -4.69, -0.29,
                        -7.80, -7.97, -3.30, 0.14, -1.70]])
label = torch.tensor([1])
print("argmax          :", scores.argmax(dim=1).item())
chances = torch.softmax(scores, dim=1)
print("chance of digit 1: %.4f" % chances[0, 1].item())
print("loss on scores   : %.4f" % nn.CrossEntropyLoss()(scores, label).item())
print("loss on chances  : %.4f" % nn.CrossEntropyLoss()(chances, label).item())
```

```text
argmax          : 1
chance of digit 1: 0.9760
loss on scores   : 0.0243
loss on chances  : 1.4817
```

> **⚠️ Watch out:** these three numbers are `0.9760`, `0.0243` and `1.4817`, while the full run of `digits_cnn.py` prints `0.9759`, `0.0244` and `1.4818`. **Nothing is wrong.** The ten scores above were copied off the screen **rounded to two decimals**, so the fourth decimal of everything downstream moves by one. Say that out loud if a student spots it — **it is a free lesson in where rounding goes once you carry it forward**, and it is the honest answer rather than "don't worry about it".

Then three questions and nothing else: **"what does the model think it is? how sure is it? and which of those two losses is the right one?"** One; 97.6%; the first. **That is objective 2 in eleven lines, with no training run at all.**

**One thing you must not cut:** the two loss numbers side by side. If the whole lesson collapses to one sentence, make it *"the loss gets the raw scores, never the squashed ones, and if you get it wrong nothing goes red."*

### If the student is flying

None of these need syntax from a later week.

1. **Retrain with a different seed and render the filters again** (Variation-harder 3). Then *"the numbering changed. What is actually stable?"* **The best question available today**, and the answer — the rough set of things measured, but not which slot measures what — is a genuine insight about why people plot all the filters rather than quoting one.
2. **Score every filter against an all-ink patch** (Variation-harder 2). Filter 2 gives +3.463 and filter 1 gives −1.707. **Neither is an edge detector, and both are doing something sensible.** This is the antidote to "all first-layer filters are edge detectors".
3. **Sixteen filters** (Variation-harder 4): predict 3,130 parameters, then measure whether the accuracy improves. **It barely does, and that is the result.**
4. **The full softmax on all ten by hand** (Variation-harder 5), then check the ten chances add to exactly 1.0000.
5. **The honest noise question:** *"the CNN got 529 of 540 and the dense network got 525. How would you find out whether that difference is real?"* Run both with five different seeds and look at the spread. **They have everything they need to do this and it takes four minutes of compute.** A student who does it and reports "the two ranges overlap" has done a real experiment and should be told so loudly.
6. **Find the digit the model was least sure about.** Take the softmax of all 540 test rows, find the row whose biggest chance is smallest, print that picture as numbers and look at it. **It is usually genuinely ambiguous**, and seeing that is worth more than another accuracy point.

### If the student won't engage today

**Close the laptop. Ten numbers on a piece of paper.**

Write the real ten logits down and nothing else:

```text
digit:      0      1      2      3      4      5      6      7      8      9
score:  −10.94  4.46 −10.63  −4.69  −0.29  −7.80  −7.97  −3.30   0.14  −1.70
```

Then three questions and nothing else:

> **"Which is biggest?"**
>
> **"Which digit does that belong to?"**
>
> **"So what does the machine think this is?"**

4.46; slot 1; a one. **That is argmax, delivered in ninety seconds with no code**, and it is half of objective 2.

Then, if they will take one more: **"which two digits did it think were the next most likely?"** 8 (`0.14`) and 4 (`−0.29`). **And then the good question, which is not a maths question: "does that make sense for a badly-written 1 at eight pixels across?"** It does, and working that out is the most interesting thing in the lesson.

If they will take a third thing: **the nine numbers of filter 6, and "which column is positive?"** Objective 3, on paper, in two minutes.

The typing survives. Week 27 rebuilds this network in its first five minutes.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — where the softmax went (spoken, 60 seconds)**

> "You built the network. The last layer is `Linear(64, 10)`. **What exactly comes out of it, and what do you hand to the loss?**"

*Good answer:* "Ten raw scores — logits. They can be negative and they don't add to 1. And you hand the loss those raw scores, not squashed ones, because `CrossEntropyLoss` does the softmax itself. If you squash first, the loss goes from 0.02 to about 1.48 and nothing warns you."

**What to catch:** "ten probabilities". Ask *"can a probability be minus ten point nine?"* **Full marks needs the words "raw" and "the loss does it itself".**

**Check 2 — the parameter count, cold (spoken, 60 seconds)**

> "`nn.Conv2d(8, 16, 3)`. **How many numbers does that layer contain, and show me the arithmetic.**"

*Good answer:* "8 × 3 × 3 × 16 = 1,152 weights, plus 16 biases, one per filter, so **1,168**."

**What to catch:** 1,152 with no biases. Ask *"how many filters?"* Sixteen. *"So how many biases?"* **And the level-4 follow-up if they got it instantly: "does that number change if the picture is 200 by 200 instead of 8 by 8?"** No — and that is the whole point of a conv layer.

**Check 3 — which row goes in the report (spoken, 90 seconds)**

> "Your CNN got **529 of 540** on the test set with **1,898** weights. The dense network got **525 of 540** with **4,810** weights. **Which of those two differences would you put in a report, and which one would you be careful about?**"

*Good answer:* "The weight counts — 1,898 against 4,810, that's 2,912 fewer, and it's exactly reproducible. I'd be careful about the accuracy: 529 against 525 is four digits out of 540, which is inside the run-to-run wobble, so I'd say they're level rather than claiming the CNN is better. If I wanted to claim it I'd rerun with several seeds first."

**What to catch:** "the CNN is more accurate". Push once: *"how many digits is that, and would it survive a different seed?"* **A student who converts a ratio into counts before deciding whether a difference is real has learned the most transferable thing in Term 3.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say what the last layer outputs. Thinks the ten numbers are probabilities. Counts conv weights without the biases and cannot fix it when asked. |
| **2 — Emerging** | Trains the network by copying the file. Computes the parameter count with the structure given. Knows `argmax` gives the answer but not what `dim=1` means. Says "98%" without the counts or the split. |
| **3 — Secure** | Computes all three parameter counts unaided including biases and gets 1,898 before printing it. Explains that the last layer gives ten raw scores and that the loss does the softmax, **with the two loss numbers as evidence.** Reports accuracy as "0.9796, 529 of 540 held-out rows, trained on 1,257". Describes two filters with a number. **This is the target.** |
| **4 — Strong** | Predicts that a fresh ten-class network's first loss will be near 2.30, and uses it as a check. Notices that the conv parameter counts do not contain the picture size and says why that matters. Converts 0.9796 versus 0.9722 into 529 against 525 unprompted and calls it inside the noise. Spots that `argmax(dim=0)` gives the wrong number of answers. |
| **5 — Exceptional** | Explains *why* the double-softmax lands near the guessing loss rather than somewhere obviously wrong. Retrains with a different seed, notices the filter numbering changes, and asks what is actually stable across runs. Says honestly that three of the eight filters cannot be described and refuses to invent a story. Designs the multi-seed experiment that would settle whether the four-digit accuracy difference is real. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, three pages, and the last one is the one I mark hardest.
>
> **First, page 26.4 — train it and report it properly.** Run the file. **Report train accuracy and test accuracy, and name the row counts on both.** Not '98%'. *'0.9881 on 1,257 training rows and 0.9796 on 540 held-out rows.'* **And write the seconds it took on your machine, not mine.** Then one sentence: is that gap between the two numbers big or small, and how do you know?
>
> **Second, page 26.5 — save the filter grid and describe two of them with numbers.** Run the filter code, save `filters.png`, **put it in your workbook**. Then pick two filters and for each one write: the nine numbers, what you think it responds to, and **the number that supports you** — its answer to the bright-left patch and to the bright-top patch. **A description with no number in it does not count.** And if you want full marks, pick one filter you *cannot* describe and say so honestly.
>
> **Third, page 26.6 — the four-row comparison table, against Week 23's dense network.** Four rows: parameters, seconds, train accuracy, test accuracy. Two columns: your CNN, and Week 23's 64 → 64 → 10. **Then one sentence: which row would you put in a report, and why.** And I will tell you now that there is a wrong answer that looks right, so think about how big each difference actually is before you write it.
>
> Page 26.7 is a stretch: the whole softmax on all ten numbers by hand. It has one satisfying check in it."

**Workbook pages:** 26.1, 26.2, 26.3 in class · **26.4, 26.5, 26.6** at home · 26.7 optional.

**Expected time:** 15 min training and reporting with the counts named · 25 min on the filter grid and two numerical descriptions · 20 min on the comparison table and the sentence · **about 60 minutes**, plus 15 more for the stretch.

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — are the row counts named on both accuracies?** "98%" is not a result; "529 of 540 held-out, trained on 1,257" is. Same feedback as Week 8 and it should be nearly automatic by now. **Two — does each filter description have a number attached?** "It looks like an edge detector" is a guess. "It answers +2.830 to a bright-left edge and −1.219 to a bright-top one" is a measurement, and it is the difference between interpreting a model and telling a story about one. **Praise loudly anybody who admits they cannot describe one.** **Three — does the sentence on 26.6 pick the parameter count, or does it pick the accuracy?** The accuracy difference is four digits out of 540 and it is inside the run-to-run wobble. The parameter difference is 2,912 and it is exact. **A student who reports "the CNN is more accurate" has done the arithmetic and missed the lesson, and this is the single most useful line of feedback you will write this week: "how many digits is four, out of 540, and would it survive a different seed?"**

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 26.1 — The parameter count, by hand, in pen before running

*For each layer, compute the number of learnable numbers. A conv layer is `(in × k × k × out) + out`. A linear layer is `(in × out) + out`.*

| Layer | Arithmetic | Weights | Biases | Total |
|---|---|---:|---:|---:|
| `Conv2d(1, 8, 3, padding=1)` | 1 × 3 × 3 × 8 = 72, plus 8 | 72 | 8 | **80** |
| `ReLU()` | nothing to learn | 0 | 0 | **0** |
| `MaxPool2d(2)` | nothing to learn | 0 | 0 | **0** |
| `Conv2d(8, 16, 3, padding=1)` | 8 × 3 × 3 × 16 = 1,152, plus 16 | 1,152 | 16 | **1,168** |
| `ReLU()` | nothing to learn | 0 | 0 | **0** |
| `MaxPool2d(2)` | nothing to learn | 0 | 0 | **0** |
| `Flatten()` | nothing to learn | 0 | 0 | **0** |
| `Linear(64, 10)` | 64 × 10 = 640, plus 10 | 640 | 10 | **650** |
| | | | | **1,898** |

**The verification file:**

```python
"""params.py - price the network before you train it."""
import torch.nn as nn

model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.Linear(64, 10))

for i, layer in enumerate(model):
    n = sum(p.numel() for p in layer.parameters())
    print("layer %d  %-12s %6d weights" % (i, type(layer).__name__, n))
print("total  :", sum(p.numel() for p in model.parameters()))

dense = nn.Sequential(nn.Flatten(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 10))
print("dense 64 -> 64 -> 10:", sum(p.numel() for p in dense.parameters()))
```

**The real output:**

```text
layer 0  Conv2d           80 weights
layer 1  ReLU              0 weights
layer 2  MaxPool2d         0 weights
layer 3  Conv2d         1168 weights
layer 4  ReLU              0 weights
layer 5  MaxPool2d         0 weights
layer 6  Flatten           0 weights
layer 7  Linear          650 weights
total  : 1898
dense 64 -> 64 -> 10: 4810
```

**Marking notes.** **A total of 1,864 is the missing-biases error** — short by exactly 8 + 16 + 10 = 34 — and it is the same error Week 22 flagged. One line of feedback, every week, until it stops. **A total of 818 means they used 8 × 3 × 3 (plus 16 biases) for conv2 and forgot to multiply by the 16 filters.** And **anybody who writes 0 for the ReLU, the pools and the flatten without hesitating has understood something important**: three of the eight layers in this network contain nothing to learn at all.

**The observation worth praising:** **conv2 is the biggest layer, with 1,168 of the 1,898.** Most people expect the `Linear` to dominate, because in Week 23's dense network it did. A student who notices that and says *"the big layer moved"* is at level 4.

### Page 26.2 — Before training: what would a useful 3×3 filter look like?

*A sketch, in pen, before any code runs. There is no wrong answer and it is not marked for accuracy.*

**What to expect, and what to do with it.** Most students draw either a bullseye (bright centre, dark surround) or a half-and-half split. **Both are real things that real first layers learn**, and the split one is right — filters 4 and 6 are exactly that.

**The point of the page is that they committed to something before seeing the answer.** Mark it present or absent, not right or wrong, and **read two of them out loud during the vote** — including one that turned out to be wrong. It makes the wrong ones safe to have.

### Page 26.3 — The filter vote

*Eight boxes, one per filter. What do you think it is looking for? Then, beside each, the number.*

| filter | the nine numbers (rounded) | bright-LEFT | bright-TOP | honest description |
|---:|---|---:|---:|---|
| 0 | `+0.092 +0.307 −0.803` / `−0.526 +0.157 +0.704` / `+0.443 +0.657 +0.482` | +0.750 | −1.651 | weakly prefers bright-left; dislikes bright-top |
| 1 | `−0.155 −0.515 −0.369` / `−0.783 −0.661 −0.084` / `−0.059 +0.377 +0.543` | −1.887 | −3.428 | **negative to everything — it fires on blank paper, not ink** |
| 2 | mostly positive | −0.956 | −0.032 | likes ink in general; no left-right preference |
| 3 | mixed | +0.543 | +0.158 | **weak. Cannot be described honestly.** |
| **4** | `−0.185 +0.784 +0.742` / `+0.469 +0.383 −0.196` / `−0.105 −0.977 −0.681` | +0.503 | **+3.760** | **horizontal edge detector: bright above, dark below** |
| 5 | mixed | −0.876 | +0.212 | **weak.** Six positive weights (sum +3.070) make it ink-like, with a mild dislike of bright-left; no clean story. |
| **6** | `+0.509 −0.129 −0.149` / `+0.382 −0.507 −0.767` / `+0.761 +0.348 −0.550` | **+2.830** | −1.219 | **vertical edge detector: bright left, dark right** |
| 7 | `+0.478 +0.491 +0.006` / `+0.656 +0.744 +0.563` / `+0.847 −0.340 −0.608` | +2.916 | +3.041 | likes both — positive except the bottom-right two cells, weights sum +2.837, so best read as an **ink-total** filter; two test patches cannot support "corner" |

*(Note: the exact nine numbers for filters 2, 3 and 5 are printed by `filters.py`; the five reproduced here are the ones you will be asked about, because they are the ones that can be described — or, in filter 0's case, only weakly.)*

**Filter 6's arithmetic against the bright-left patch, in full**, so a student can check it:

```text
the patch:   1   1  −1        the filter:   0.509  −0.129  −0.149
             1   1  −1                      0.382  −0.507  −0.767
             1   1  −1                      0.761   0.348  −0.550

row 0:  0.509 − 0.129 + 0.149  =  +0.529
row 1:  0.382 − 0.507 + 0.767  =  +0.642
row 2:  0.761 + 0.348 + 0.550  =  +1.659
                                  -------
                                   +2.830
```

**Marking notes.** **Two filters described with a number is full marks.** The two that can be described are 4 and 6, and either counts. **An honest "no idea" for filters 3 and 5 is worth marks and should be said so, out loud.** The thing to mark down is a confident story with no number attached — "filter 3 detects curves" is unsupported and the follow-up question is *"what number tells you that?"*

### Page 26.4 — Train it and report it properly

*Run `digits_cnn.py`. Report both accuracies with their row counts, and the seconds on your machine.*

**The real output, in full**, is in the Prep Checklist. The three numbers to mark:

```text
seconds        : 3.1              (theirs will differ; anything from 2 to 15 is normal)
train accuracy : 0.9881  (1242 of 1257 train rows)
test accuracy  : 0.9796  (529 of 540 test rows)
```

**A full-marks report sentence:**

> *"Trained on 1,257 handwritten digits in 3.1 seconds. Train accuracy 0.9881 — 1,242 of 1,257. Test accuracy 0.9796 — 529 of 540 held-out digits it never saw. The gap between them is about one accuracy point, which is small: the model got 15 of its own training digits wrong and 11 of the held-out ones, so it has not memorised its homework. If the train number had been 1.0000 and the test number 0.93, that gap would be overfitting."*

**Marking notes.** **The row counts must be there on both.** And **the seconds must be their own** — a student reporting 3.1 seconds on a machine that took 14 has copied the file's number, which is the same offence as copying an answer.

**One thing to praise:** anybody who notes that `1257 + 540 = 1797` and that all 1,797 digits are accounted for. That addition check is Week 8's habit applied to a new place.

### Page 26.5 — The filter grid, and two filters with numbers

**The complete file:**

```python
"""filters.py - look at the eight filters, and price the two networks."""
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

np.random.seed(0)

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.images / 16.0, digits.target, test_size=0.30, random_state=0,
    stratify=digits.target)
Xtr = torch.from_numpy(X_train).float().unsqueeze(1)
Xte = torch.from_numpy(X_test).float().unsqueeze(1)
ytr = torch.from_numpy(y_train).long()
yte = torch.from_numpy(y_test).long()


def make_cnn():
    return nn.Sequential(
        nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Flatten(), nn.Linear(64, 10))


def make_dense():
    return nn.Sequential(nn.Flatten(), nn.Linear(64, 64), nn.ReLU(),
                         nn.Linear(64, 10))


def train(model, epochs=40):
    loader = DataLoader(TensorDataset(Xtr, ytr), batch_size=32, shuffle=True)
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    t0 = time.perf_counter()
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            loss_fn(model(xb), yb).backward()
            opt.step()
    secs = time.perf_counter() - t0
    model.eval()
    with torch.no_grad():
        tr = (model(Xtr).argmax(1) == ytr).float().mean().item()
        te = (model(Xte).argmax(1) == yte).float().mean().item()
    return secs, tr, te


torch.manual_seed(0)
cnn = make_cnn()
c_s, c_tr, c_te = train(cnn)
torch.manual_seed(0)
dense = make_dense()
d_s, d_tr, d_te = train(dense)

print("row                   CNN     dense MLP")
print("parameters       %8d      %8d"
      % (sum(p.numel() for p in cnn.parameters()),
         sum(p.numel() for p in dense.parameters())))
print("seconds          %8.1f      %8.1f" % (c_s, d_s))
print("train accuracy   %8.4f      %8.4f" % (c_tr, d_tr))
print("test accuracy    %8.4f      %8.4f" % (c_te, d_te))
print("test correct     %5d/540      %5d/540"
      % (round(c_te * 540), round(d_te * 540)))

w = cnn[0].weight.detach().numpy()[:, 0]
print()
print("first-layer weight shape:", tuple(cnn[0].weight.shape))
for i in (4, 6):
    print("filter %d:" % i)
    print(np.round(w[i], 3))

fig, axes = plt.subplots(1, 8, figsize=(12, 2))
for i, ax in enumerate(axes):
    ax.imshow(w[i], cmap="gray", interpolation="nearest")
    ax.set_title("filter %d" % i, fontsize=9)
    ax.axis("off")
fig.suptitle("the eight 3x3 filters conv1 learned")
plt.tight_layout()
plt.savefig("filters.png", dpi=110)
plt.close(fig)
print("saved filters.png")

vert = np.array([[1., 1., -1.], [1., 1., -1.], [1., 1., -1.]])
horiz = vert.T
print()
print("filter   answer to a bright-LEFT edge   answer to a bright-TOP edge")
for i in range(8):
    print("  %d      %+22.3f   %+25.3f"
          % (i, (w[i] * vert).sum(), (w[i] * horiz).sum()))
```

**The real output:**

```text
row                   CNN     dense MLP
parameters           1898          4810
seconds               3.1           0.4
train accuracy     0.9881        0.9889
test accuracy      0.9796        0.9722
test correct       529/540        525/540

first-layer weight shape: (8, 1, 3, 3)
filter 4:
[[-0.185  0.784  0.742]
 [ 0.469  0.383 -0.196]
 [-0.105 -0.977 -0.681]]
filter 6:
[[ 0.509 -0.129 -0.149]
 [ 0.382 -0.507 -0.767]
 [ 0.761  0.348 -0.55 ]]
saved filters.png

filter   answer to a bright-LEFT edge   answer to a bright-TOP edge
  0                      +0.750                      -1.651
  1                      -1.887                      -3.428
  2                      -0.956                      -0.032
  3                      +0.543                      +0.158
  4                      +0.503                      +3.760
  5                      -0.876                      +0.212
  6                      +2.830                      -1.219
  7                      +2.916                      +3.041
```

**Expected runtime: about 4 seconds.**

**A full-marks pair of descriptions:**

> **Filter 6.** `0.509 −0.129 −0.149 / 0.382 −0.507 −0.767 / 0.761 0.348 −0.550`. Its whole left column is positive and its whole right column is negative, so it adds up whatever is on the left and subtracts whatever is on the right. **It answers +2.830 to a bright-left edge and −1.219 to a bright-top one, so it is a vertical edge detector**, and it prefers bright-on-the-left specifically rather than any vertical edge.
>
> **Filter 4.** `−0.185 0.784 0.742 / 0.469 0.383 −0.196 / −0.105 −0.977 −0.681`. Top row mostly positive, bottom row all negative. **It answers +3.760 to a bright-top edge and only +0.503 to a bright-left one, so it is the same idea rotated: a horizontal edge detector.**
>
> **And one I cannot describe: filter 3.** It answers +0.543 and +0.158 — nearly nothing to both patches — and its nine numbers do not have a pattern I can name. I do not know what it does.

**Marking notes.** **A number per description, or it does not count.** And **the honest "cannot describe" earns marks, explicitly.** The failure mode to mark down is a confident label with nothing behind it.

### Page 26.6 — The four-row comparison table

| Row | CNN | dense MLP (Week 23) | Difference |
|---|---:|---:|---|
| parameters | **1,898** | **4,810** | CNN uses **2,912 fewer** |
| seconds to train | 3.1 | 0.4 | dense is about **8× faster** |
| train accuracy | 0.9881 (1,242 / 1,257) | 0.9889 (1,243 / 1,257) | dense by **1 digit** |
| **test accuracy** | **0.9796 (529 / 540)** | **0.9722 (525 / 540)** | CNN by **4 digits** |

**A full-marks sentence:**

> *"I would put the **parameter count** in a report: 1,898 against 4,810, which is 2,912 fewer weights and is exactly reproducible. I would be careful with the test accuracy: 529 against 525 is only four digits out of 540, which is inside the run-to-run wobble, so the honest statement is that the two networks are level on accuracy while the CNN is less than half the size. And the reason the size matters more than four digits is that the conv layers' weight counts do not depend on the picture size at all — the same 80 first-layer weights would work on a 200×200 photograph, while the dense network's 4,160 are welded to 8×8."*

**Marking notes.** **The wrong answer that looks right is "the CNN is more accurate, so I'd report the test row."** It is not wrong that test accuracy is the row you report in general — Week 8 through 11 drilled that, and it is right. What is wrong is treating a four-digit difference as a finding. **The distinction you are marking is between "which row is meaningful in principle" and "which difference is big enough to claim".** Both are correct answers to different questions, and a student who names both is at level 5:

> *"Test accuracy is the row that belongs in a report, because it is the only one measured on unseen data. But the test difference here is four digits out of 540 and I would report it as 'level'. The difference I would actually claim is the parameter count."*

**And mark down, gently, any answer that picks train accuracy.** Both networks score about 0.988 on their own homework and it tells you nothing.

### Page 26.7 — Stretch: the whole softmax, by hand

*Take the ten real scores. Do all three steps. Check the ten chances add to 1.*

```text
the ten scores:
 −10.94   4.46  −10.63   −4.69   −0.29   −7.80   −7.97   −3.30    0.14   −1.70
```

**Step 1 — subtract the biggest, which is 4.46:**

| slot | score | score − 4.46 |
|---:|---:|---:|
| 0 | −10.94 | −15.40 |
| 1 | 4.46 | 0.00 |
| 2 | −10.63 | −15.09 |
| 3 | −4.69 | −9.15 |
| 4 | −0.29 | −4.75 |
| 5 | −7.80 | −12.26 |
| 6 | −7.97 | −12.43 |
| 7 | −3.30 | −7.76 |
| 8 | 0.14 | −4.32 |
| 9 | −1.70 | −6.16 |

**Step 2 — `e^` each one:**

```text
slot 0:  e^−15.40  =  0.000000    (2 × 10^−7, call it zero)
slot 1:  e^  0.00  =  1.000000
slot 2:  e^−15.09  =  0.000000
slot 3:  e^ −9.15  =  0.000106
slot 4:  e^ −4.75  =  0.008652
slot 5:  e^−12.26  =  0.000005
slot 6:  e^−12.43  =  0.000004
slot 7:  e^ −7.76  =  0.000426
slot 8:  e^ −4.32  =  0.013300
slot 9:  e^ −6.16  =  0.002112
                      --------
              total   1.024606
```

**Step 3 — divide each by 1.024606:**

```text
slot 1:  1.000000 ÷ 1.024606  =  0.9760
slot 8:  0.013300 ÷ 1.024606  =  0.0130
slot 4:  0.008652 ÷ 1.024606  =  0.0084
slot 9:  0.002112 ÷ 1.024606  =  0.0021
slot 7:  0.000426 ÷ 1.024606  =  0.0004
slot 3:  0.000106 ÷ 1.024606  =  0.0001
slots 0, 2, 5, 6                 0.0000
                                 ------
                          total   1.0000  ✅
```

**The satisfying check: they add to 1.0000.** They must, because every one of them was divided by the same total. **If a student's ten do not add to 1, the arithmetic is wrong somewhere and they can find it themselves — which is the whole reason the check exists.**

**And the loss:**

```text
loss  =  −ln(0.9760)  =  0.0243
```

**PyTorch prints `0.9759` and `0.0244`.** The gap is in the fourth decimal place and it is entirely because we rounded the ten scores to two decimals before starting. **Say that out loud to any student who worries about it: your paper agrees with the machine to three decimals, and the fourth decimal is the two you threw away.**

### Answers to every question posed in the lesson

**Hook — "one channel in, eight filters, 3 by 3. How many numbers?"** `1 × 3 × 3 × 8 = 72` weights, plus **8 biases**, one per filter, = **80**.

**Hook — "eight channels in, sixteen filters."** `8 × 3 × 3 × 16 = 1152`, plus 16, = **1,168**.

**Hook — "64 in, 10 out."** `64 × 10 = 640`, plus 10, = **650**. **Total 1,898**, against Week 23's **4,810**.

**Hook — "what do you think a useful filter looks like?"** No wrong answer. The two things real first layers commonly learn are a **half-and-half split** (which is an edge detector, and filters 4 and 6 are exactly that) and a **bright-centre-dark-surround blob**. Take the guesses and write them down; do not evaluate them.

**Concept — "what does this network think this digit is?"** A **one**. The biggest of the ten is `4.46` and it is in slot 1.

**Concept — "how did you decide?"** It is the biggest. **And notice you cared about its position, not its value — that is argmax.**

**Concept — "are those ten numbers probabilities?"** **No.** There is a `−10.94` in there, and they do not add to 1. They are **logits**: raw, unsquashed scores.

**Concept — the softmax, step by step.** Subtract 4.46 from all ten; exponentiate; total is **1.024606**; divide. The winner gets `1.000000 ÷ 1.024606 = 0.9760`, so **97.6% sure it is a one**. Then `−ln(0.9760) = 0.0243`.

**Concept — "guess: bigger, smaller, or an error?"** **Neither — no error at all**, and the loss goes from `0.0244` to **`1.4818`**. And 1.4818 is on the way to `−ln(0.1) = 2.30`, the loss of a guessing model, because a second softmax pushes ten numbers that are already between 0 and 1 towards all being near 0.1.

**Live-code step 1 — "`digits.data` was `(1797, 64)`. What is `digits.images`?"** `(1797, 8, 8)`. **Same 1,797 digits, same numbers, one flattened and one not.**

**Live-code step 2 — "what will `parameters:` print?"** `1898`, and they knew before the machine did.

**Live-code step 3 — "1,257 rows, 32 at a time. How many steps?"** `1257 ÷ 32 = 39.28`, so 39 full batches of 32 and one final batch of 9: **40**.

**Live-code step 3 — "what will the loss be before it has learned anything?"** About **2.30**, because `−ln(1/10) = 2.3026`. It prints **2.2796**. **Install this as a permanent check.**

**Live-code step 4 — "eleven wrong. Which eleven?"** Next week, and it is the whole first half of it. Today: eleven, honestly counted.

**Live-code step 5 — "did anything go red?"** **No.** Same model, same picture, same correct answer, two completely different losses, and nothing warned you.

**Live-code step 6 — "which of those two answers is one-per-picture?"** `dim=1`, which gives `(540,)`. `dim=0` gives `(10,)` and answers a question nobody asked.

**Wrap — "which row would you put in a report, and which is least honest?"** **Test accuracy** goes in the report; **train accuracy** is the least honest row on the board, because it is the model's mark on its own homework and both networks score about 0.988 on it.

**Wrap — the four-digit question.** 529 against 525 is **four digits out of 540**, which is inside the run-to-run wobble. **1,898 against 4,810 is 2,912 and is exact.** The parameter count is the difference you can defend.

**Variation-harder 2 — the all-ink patch.** Scoring against `np.ones((3,3))` is just the sum of the filter's nine weights. Filter 2 gives **+3.463**, filter 5 gives **+3.070**, filter 7 gives **+2.837**, and filter 1 gives **−1.707**. **None of those four is an edge detector**, and three of them are broadly "how much ink is here" measurements. **This is the honest antidote to "first layers learn edge detectors".**

**Variation-harder 3 — a different seed.** The eight filters come out different, and **the numbering certainly changes** — filter 6 will not be the vertical one. What is roughly stable is the *set* of things measured: usually one or two edge-ish filters, one ink-total filter, and several that cannot be described. **Which slot holds which is arbitrary, and that is why people plot all of them.**

**Variation-harder 4 — sixteen filters.** conv1 becomes `1 × 3 × 3 × 16 + 16 = 160`; conv2 becomes `16 × 3 × 3 × 16 + 16 = 2,320`; the flatten is still `16 × 2 × 2 = 64` so the linear stays 650. **Total 3,130.** And the test accuracy barely moves, **which is the result**: on this data eight filters is already enough.

---

## 🔮 Next Week Preview

Next week is the Term 3 checkpoint, and it starts from the eleven digits this lesson got wrong. First the ten-class confusion matrix, and the discovery that **four of the eleven mistakes are the same two digits confusing each other** — a real 8 called a 1 three times, and a real 1 called an 8 once — followed by the physical diagnosis, which is that at 8×8 an 8's two loops fill in and what is left is a bright bar down the middle columns, exactly like a 1. Then the two ways to buy accuracy without collecting a single new picture. **Augmentation:** shift every training digit one pixel up, down, left and right with `np.roll`, turning 1,257 rows into 6,285, and watch 0.9796 become **0.9926** — with a beautiful trap on the way, because rolling the ink *round* the edge instead of blanking it buys exactly **zero** points. Then **transfer learning**, done honestly: train the conv stack on digits 0 to 4, freeze it, retrain only the ten-way head on digits 5 to 9, and put the frozen number and the unfrozen number on the board side by side — where the frozen backbone turns out to buy speed rather than accuracy, and saying so out loud is the point of the week.

**To prep early:** three things. **One — leave the PARAMETER COUNT sheet and THE SHAPE LADDER up.** Week 27 adds a row to the first and reuses the second unchanged, and it is the last week either of them is needed, so they come down at the end. **Two — save this week's `digits_cnn.py` and `filters.png` somewhere the student can find them.** Week 27's first table row is *this* week's 0.9796, and retyping the network burns eight minutes of a checkpoint that has three experiments to get through. **Three — run next week's `see_it.py` tonight and time the whole thing**, because it trains six networks and the augmented one alone is about fifteen seconds; the total is around forty, and knowing that in advance is the difference between a calm lesson and a lesson where you are watching a progress bar in silence.
