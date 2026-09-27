# Week 24 — Why Flattening a Picture Throws Away the Picture

[⬅ Week 23](week-23.md) · [Course Home](../README.md) · [Week 25 ➡](week-25.md) · [Student Guide](../student-guide/week-24.md) · [Workbook](../workbook/week-24.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one parameter count, sixteen sums by hand, and a new kind of layer |
| **Big idea** | Flattening a picture tells the model that the pixel directly above and a pixel across the room are equally related. **A convolution is a small grid of weights that slides — and it keeps the neighbourhood.** |
| **New vocabulary** | convolution · kernel / filter · feature map · weight sharing · locality · channel |
| **New maths** | **None.** Sixteen sums of nine multiplications, all done by hand. The output-size *rule* is next week; today they count the windows. |
| **New syntax** | `torch.from_numpy(a).float()` · `t.unsqueeze(0)` · `nn.Conv2d(1, 4, kernel_size=3)` · `conv.weight.data = ...` |
| **Dataset** | 6 × 6 and 8 × 8 pictures **written out inline with numpy** — a half-bright bar, a vertical stripe, a cross, and a noisy square. Plus `load_digits()` for the hook. **Nothing downloads. No internet needed. No torchvision.** |
| **Materials** | **Squared paper, two sheets per student** — this is the week's most important material · pencils **with rubbers** · printed workbook pages 24.1–24.6 · the **PARAMETER COUNT** wall sheet, still up, with two spare rows · the Bug Log |
| **Tech needed** | Laptop with Python 3, numpy, matplotlib, scikit-learn, **torch**. **No new installs. No torchvision — we write our own pictures.** |
| **Prep time** | 30 minutes the night before, **including doing the sixteen cells in pencil yourself** · 5 minutes on the day |
| **Expected runtime of the code** | `flatten_cost.py` **instant**. `by_hand.py` **instant**. `kernels.py` writes a 4 × 4 grid of pictures in **about 2 seconds**. `shuffle_pixels.py` trains two MLPs in **under a second**. |

> **⚠️ Watch out:** the activity is sixteen sums done in pencil and then checked against `nn.Conv2d`, cell by cell. **If one cell disagrees, stop the lesson and find it.** It will be one of three things every time: the window slid the wrong way, a row of the kernel got skipped, or somebody used the mirrored kernel and got −24 instead of +24. Finding it is the lesson. Waving it through is the one thing that makes Weeks 25, 26 and 27 impossible.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compute the parameter count of a dense layer on a flattened image and of a convolution over the same image** — 1,040 against 10 — and say which one is throwing weights away.
2. **Slide a 3 × 3 kernel over a 6 × 6 picture by hand and fill in all sixteen output cells**, then match every one against `nn.Conv2d` with the same nine numbers loaded in.
3. **Explain weight sharing**: the same nine numbers applied at every position, and what that buys — one rule that works everywhere, and a count that does not grow with the picture.
4. **Design a kernel that finds vertical edges and one that finds horizontal edges**, and show each firing on the right picture and staying silent on the wrong one.

Observable evidence: a pencilled 4 × 4 grid reading `0 24 24 0` four times, beside a printed one that matches; the two numbers 1,040 and 10 on the wall with a one-line verdict; and a 4 × 4 figure of twelve feature maps with a sentence per kernel.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There is multiplying and adding, sixteen times. If you can do `1 × 10 + 0 × 10 + (−1) × 2` you can teach every part of this lesson, and the sixteen repetitions are the point rather than an obstacle.

But **you must do the sixteen cells in pencil yourself before class.** Not read them — do them. Twenty minutes tonight, on squared paper. There is no way to referee a disagreement between a student's pencil and the computer if you have not been the pencil.

There are four ideas.

### 1. What flattening actually threw away

Last week's digits model reached 96.67% treating each 8 × 8 picture as 64 numbers in a row. Here is the uncomfortable thing about that.

Take the 64 columns and **shuffle them** — one shuffle, the same shuffle applied to every single picture. Now the pictures are unrecognisable to a person. Train exactly the same network on them:

```text
the new column order starts: [16, 36, 27, 8, 44, 23, 53, 4]
the pictures as they are     test accuracy 0.9667
the same 64 columns shuffled test accuracy 0.9704
```

**It did not notice.** In fact the shuffled version scored a shade higher, and that difference — 0.0037 of 540 test digits, so **two digits** — is noise. Run it with another seed and it goes the other way.

**Sit with that for a moment, because it is the whole week.** A picture whose pixels have been shuffled is not a picture. A model that trains to the same score on both is not looking at a picture. It is looking at 64 unrelated numbers and finding a pattern in them, which happens to work, and which will fall apart the moment a digit is written two pixels to the left.

Why can't it tell? Because of what `nn.Linear` is. Every weight connects one *input slot* to one *output unit*. Slot 19 and slot 20 are next-door pixels in the real picture, and slot 19 and slot 27 are one directly above the other — **but nothing in the layer says so.** To `nn.Linear` there are sixty-four unrelated coordinates, and "next to" is not a concept it can hold.

![Flattening throws the neighbourhood away](../figures/fig-w24-1-flatten-destroys-the-neighbourhood.svg)
*Figure 24.1 — Flattening throws the neighbourhood away. A touches C in slot 20, and A touches B eight slots away in slot 27, and a dense layer cannot tell which of those means "touching".*

> **locality** — what a pixel means is mostly decided by the pixels immediately around it. An edge is a local event. You do not need the top-left corner to understand the bottom-right one.

🍕 **The analogy that works, and it is worth telling in full.** Somebody hands you 64 numbered envelopes. Each one contains the brightness of one square of a photograph, and they arrive in a random order that nobody will tell you. You *could* eventually learn "envelope 41 is usually bright on a seven". You would have to learn that separately for all 64 envelopes, and if the seven slid two squares to the left, every single thing you learned would be wrong.

Now instead somebody hands you a small magnifying glass and says: *slide this over the whole photo and tell me wherever you see a corner.* **One rule. Works everywhere on the page.** That is a convolution.

### 2. The price, in numbers you can count

This is objective 1 and it is the fastest way to make the argument land, because it is arithmetic.

An 8 × 8 picture, flattened to 64 numbers, into a dense layer with 16 units:

```
weights = 16 × 64 = 1024
biases  =               16
                    ------
total   =            1040
```

A single 3 × 3 convolution over the same 8 × 8 picture:

```
weights = 3 × 3 =  9
bias    =          1
                 ---
total   =         10
```

```
1040 ÷ 10 = 104
```

**A hundred and four times fewer learnable numbers.** And the smaller one is the one that knows what a neighbourhood is. That is not a compromise; it is a better tool.

And the gap grows fast, because **a convolution's count does not depend on the size of the picture at all.** On a 64 × 64 picture:

```
nn.Linear(4096, 256)              1,048,832 numbers
nn.Conv2d(1, 4, kernel_size=3)           40 numbers
```

Over a million against forty. Say the numbers out loud; they are the argument.

### 3. The convolution itself, done by hand — this is the section to prepare

> **kernel** (also called a **filter**) — a small grid of numbers, usually 3 × 3, that slides across the picture. At every position you multiply each of its nine numbers by the picture number underneath it and add up all nine.

> **feature map** — the grid of answers that comes out. One number per position where the kernel sat.

> **convolution** — the whole sliding-and-summing operation.

Here is the entire thing, on numbers you can check. **The picture:** 6 × 6, bright left half, dark right half. Every row identical.

```
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
```

**The kernel:** a vertical-edge finder — plus down the left column, minus down the right, nothing in the middle.

```
  1   0  −1
  1   0  −1
  1   0  −1
```

**Position (0, 0).** The window covers rows 0–2 and columns 0–2. Everything there is 10:

```
window          kernel         products
10  10  10       1  0  −1      10   0  −10
10  10  10   ×   1  0  −1  =   10   0  −10
10  10  10       1  0  −1      10   0  −10
```

```
row by row:  (10 + 0 − 10) + (10 + 0 − 10) + (10 + 0 − 10)  =  0 + 0 + 0  =  0
```

**Zero.** Which makes sense: that window is completely flat. No edge, no response.

**Position (0, 1).** Slide the window one column right. Now every row of the window reads `10, 10, 2`:

```
one row:      (1 × 10)  +  (0 × 10)  +  (−1 × 2)   =   10 − 2   =   8
three rows:   8 + 8 + 8                            =   24
```

**Twenty-four.** The edge is inside the window and the filter shouts.

![One output cell of the feature map, worked out in full](../figures/fig-w24-2-kernel-sliding-one-cell-computed.svg)
*Figure 24.2 — One output cell of the feature map, worked out in full. One row gives 8, three rows give 24, and 4 × 4 = 16 windows fit.*

**Position (0, 2).** Window reads `10, 2, 2` in every row:

```
one row:      (1 × 10) + (0 × 2) + (−1 × 2)  =  10 − 2  =  8
three rows:   24
```

**Position (0, 3).** Window reads `2, 2, 2`. Flat again:

```
one row:      2 − 2 = 0    →    total 0
```

**And then the rows.** Every row of this picture is identical, so every row of the output is identical. All sixteen cells:

```
   0   24   24    0
   0   24   24    0
   0   24   24    0
   0   24   24    0
```

**How many cells is that, and why sixteen?** Count the window positions. A 3-wide window on a 6-wide picture can start at column 0, 1, 2 or 3 — four places. Same going down — four places. **4 × 4 = 16.**

```
across:  6 − 3 + 1 = 4
down:    6 − 3 + 1 = 4
cells:   4 × 4 = 16
```

⚠️ **Do not turn that into the general rule today.** The full rule with stride and padding in it — `(n + 2p − k) ÷ s + 1` — is **Week 25's one new piece of maths**, and it gets a whole lesson. Today they *count the positions*. If a student derives the rule themselves, be delighted, write it on the board, and say "that is next week's lesson and you have just done it".

**The one thing that will trip somebody up in the room.** Use the mirrored kernel — `−1, 0, 1` instead of `1, 0, −1` — and every 24 becomes a **−24**. Nothing is wrong; the filter is now looking for dark-to-bright instead of bright-to-dark. Our `stripe` picture (dark left, bright right) gives exactly that:

```text
stripe  -> feature maps (3, 6, 6)
   vertical edge    biggest   +0.00   smallest  -24.00
```

**A negative feature map is a filter firing at the opposite polarity, not a mistake.** Say it once before it happens.

### 4. Weight sharing, and the channel

> **weight sharing** — the same nine numbers are used at every position. You do not learn a fresh set of weights per place in the picture.

This is what makes the count small, and it is also what makes the model *useful*, and those are two separate benefits worth naming separately.

**The count.** Nine weights and one bias, used at all sixteen positions. A dense layer producing the same 4 × 4 map from those 36 pixels would need `36 × 16 + 16 = 592` numbers.

**The usefulness.** A dense layer would have to learn "there is an edge here" **separately, sixteen times**, once per position — and it would need training examples with an edge in each of the sixteen places. The convolution learns it once and gets all sixteen for free. That is why convolutions need so much less data.

![The same nine numbers, used everywhere](../figures/fig-w24-3-weight-sharing-nine-numbers-everywhere.svg)
*Figure 24.3 — The same nine numbers, used everywhere. 9 + 1 = 10 for the convolution against 36 × 16 + 16 = 592 for the dense layer.*

And the proof that the count is independent of the picture:

```text
learnable numbers in this layer: 10
picture  6 x  6  ->  feature map  4 x  4  =   16 cells,   still 10 learnable numbers
picture  8 x  8  ->  feature map  6 x  6  =   36 cells,   still 10 learnable numbers
picture 16 x 16  ->  feature map 14 x 14  =  196 cells,   still 10 learnable numbers
picture 64 x 64  ->  feature map 62 x 62  = 3844 cells,   still 10 learnable numbers
```

**Same ten numbers, 3,844 output cells.** `nn.Linear` cannot say that about anything.

> **channel** — one slice of depth. Our digits are greyscale, so the picture has **one** channel. A colour photo has three: red, green, blue. And after a convolution the channels are no longer colours — they are **whatever each filter found**. Filter 0's channel might be "vertical edge"; filter 1's might be "horizontal edge".

That is why `nn.Conv2d(1, 4, kernel_size=3)` reads the way it does: **one channel in, four channels out** — four different filters, four feature maps, four learned ideas.

```text
nn.Conv2d(1, 4, kernel_size=3) - four filters
   weight   (4, 1, 3, 3)   36 numbers
   bias     (4,)           4 numbers
   total: 40
```

Read that shape out loud: **four filters, each looking at one input channel, each 3 by 3.** 4 × 1 × 3 × 3 = 36, plus one bias per filter = 40.

### 5. Every line of this week's code, explained to somebody who has never programmed

```python
bar = np.zeros((6, 6))
bar[:, 0:3] = 10.0
bar[:, 3:6] = 2.0
```

Build a 6 × 6 grid of zeros, then fill it in. `bar[:, 0:3]` means "every row, columns 0 up to but not including 3" — the left half — and set all of it to 10. Then the right half to 2. **We write our own pictures because then you know exactly what went in**, which is worth more here than any downloaded dataset.

```python
t = torch.from_numpy(bar).float().unsqueeze(0).unsqueeze(0)
```

Three steps and the last one twice.

- `torch.from_numpy(bar)` — make a tensor out of the numpy grid.
- `.float()` — make the numbers 32-bit decimals. numpy defaults to 64-bit; torch layers insist on 32. **Leave this out and you get `Input type (double) and bias type (float) should be the same`**, which is in the Clinic.
- `.unsqueeze(0)` — **add a new dimension of size 1 at the front.** A `(6, 6)` grid becomes `(1, 6, 6)`. Do it again and you get `(1, 1, 6, 6)`.

**Why does `nn.Conv2d` want four numbers in the shape?** Because it always expects `(batch, channels, height, width)` — how many pictures, how many colour layers each, and then the picture itself. Our one greyscale 6 × 6 picture is one picture with one channel, so `(1, 1, 6, 6)`.

🍕 **The way to say `unsqueeze`:** you have one photo. `unsqueeze` puts it in an envelope, and then puts the envelope in a box. Nothing about the photo changed; it is now wrapped in the two layers of packaging the machine expects.

```python
conv = nn.Conv2d(1, 4, kernel_size=3)
```

One channel in, four filters out, each filter 3 × 3. Like `nn.Linear`, it arrives with random numbers in it, ready to be trained.

```python
conv.weight.data = torch.from_numpy(kernel).float().reshape(1, 1, 3, 3)
conv.bias.data = torch.zeros(1)
```

**Today we are not training it — we are setting its weights by hand so we can check the arithmetic.** `conv.weight` is the block of learnable numbers; `.data` is how you reach in and overwrite them.

The `.reshape(1, 1, 3, 3)` matters: our kernel is a flat `(3, 3)` grid and the layer wants `(filters, in_channels, height, width)`. **Leave the reshape out and you get `RuntimeError: weight should have at least three dimensions`.**

**And `conv.bias.data = torch.zeros(1)` is not optional today.** PyTorch put a small random number in the bias, and it gets added to every output cell:

```text
the bias PyTorch made for us: 0.088204
[[ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]]
```

**Every cell is off by exactly 0.088204**, which is not a rounding error and not a mistake — it is the bias doing its job. Zero it and you get the clean `0 24 24 0`. **This is the second deliberate mistake in the live-code and it is worth every second**, because "my answer is 24.088 and yours is 24" is exactly the kind of near-miss that makes a student distrust their own arithmetic.

> **⚠️ Watch out:** `0.088204` is the number *you* will see only because every file this week starts with `torch.manual_seed(0)`. That line tells PyTorch to make the same "random" numbers every time, so the page and your screen match. Without it the bias is a different small number on every single run — still the same amount in all sixteen cells, still the same lesson, but not the number printed here. **If your bias is not 0.088204, check the seed line is there before you go looking for a real bug.**

```python
with torch.no_grad():
    out = conv(t)
print(out[0][0].numpy())
```

`with torch.no_grad():` — the Week 23 line: do not record anything, we are only measuring. `out` has shape `(1, 1, 4, 4)`, so `out[0][0]` is "the first picture's first channel", a plain 4 × 4 grid, and `.numpy()` turns it back into something that prints tidily.

### 6. How deep to go, and where to stop

**Go this far:** the shuffled-pixels demonstration; the two parameter counts, 1,040 and 10, with the verdict; sixteen cells in pencil and sixteen cells from `nn.Conv2d` agreeing exactly; weight sharing said in words and proved with the four picture sizes; a vertical kernel and a horizontal kernel each firing on the right picture.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **The output-size rule `(n + 2p − k) ÷ s + 1`** | **Week 25, and it is that week's one new piece of maths.** Today they *count* the window positions: 6 − 3 + 1 = 4 across, 4 down, 16 cells. If a student derives the rule, praise them and name the week. **Do not write the general form on the board.** |
| `stride`, `padding` | **Week 25.** Everything today is stride 1, no padding. |
| `nn.MaxPool2d`, `nn.Flatten` | **Week 25.** |
| Training a convolution — letting it *learn* the nine numbers | **Week 26.** Today every kernel is chosen by hand, which is the point: they see what the numbers do before anything learns them. |
| `nn.CrossEntropyLoss`, ten classes, a real CNN | **Week 26.** |
| Looking at learned filters as pictures | **Week 26.** |
| Multiple input channels — a 3 × 3 filter over RGB having 27 weights | Mention in one sentence if asked. Everything we have is one channel. **Weeks 26 and 27** deal with stacks. |
| Cross-correlation versus true convolution | See the Questions section. **One sentence if asked, and no more.** |
| CIFAR-10, `torchvision`, colour photos | Not available here, and not needed. See the callout below. |

> **💡 When you have internet:** `pip install torchvision` gives you CIFAR-10 — 60,000 colour photos, 32 × 32, in ten classes — and `torchvision.datasets.CIFAR10(root="./data", download=True)` fetches it. It is the classic dataset for this material and the learned first-layer filters are genuinely beautiful. **Nothing in this course needs it**, no exercise depends on it, and the pictures we write with numpy are actually better for learning what a kernel does, because you can see exactly what went in. Treat it as a holiday project.

The sentence to keep in your head: **today the student finds out that the model has never seen a picture, and meets the layer that can.**

---

### 7. 🧭 The Growing Map — a new box opens

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week the map actually moves — a tile goes white and the one below it goes gold — so
the two minutes are worth taking properly.

![The Level 3 pipeline in Week 24: the images and CNNs tile opens on the convolution that keeps the neighbourhood](../figures/fig-w24-0-where-this-fits.svg)

*Figure 24.0 — Week 24's version. `numpy brain · PyTorch` is finished in plain white; `images · CNNs` is
gold for the first time. The ↻ on stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and expect a wrong answer first.** Several will point at the tile
   that just went white, because that is where they have been living for five weeks. The gold box is the
   new one, *images · CNNs*. Then the anchoring question: **"what is the first thing this box threw out?"**
   The answer is on the wall — **1,040 against 10** — and in their pencilled grid: `0 24 24 0`, four times.
   *"A flatten costs a thousand and forty weights and still cannot tell that two pixels were touching.
   Nine numbers can."*
2. **Point at the ↻ on stage three and say what has not changed.** It is still black, still open, still the
   same loop. *"We have a new kind of layer. We have not got a new kind of learning. Next month's network
   trains with exactly the five lines from Week 21."* This matters because "CNN" sounds to a 14-year-old
   like a different subject.
3. **Say how long this box takes and what is in it.** Four weeks: today the convolution, Week 25 the sizes
   on paper, Week 26 a network that reads handwriting, Week 27 augmentation and transfer. *"Today was the
   pencil. In three weeks you will have something that reads digits better than you can read other
   people's."*

> **🧑‍🏫 Why this is worth two minutes.** The hook shuffled the pixels of a digit and the MLP did not care.
> That is an unsettling demonstration, and a couple of students will leave thinking everything they built
> in the last five weeks was wrong. The map is the correction: the tile above went **white**, not grey. It
> was finished, it was correct, and it is what makes today possible — a convolution is Week 17's grid
> multiply on a sliding window, and they could not have seen that a month ago.

**One thing to notice, so you can answer if asked.** The threads are `representation` and `model`, and
`representation` is the lead. Say it in one line if it comes up: *"a feature map is the picture rewritten
in the kernel's language"* — the same idea as Week 4's scaling and Week 16's squashed activation, third
time around. The spiral is doing its job here, and naming it out loud is free.

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Do the sixteen cells in pencil, on squared paper, yourself. Twenty minutes.** This is not optional and it is not the same as reading them. Draw the 6 × 6 picture with its 10s and 2s, draw the 3 × 3 kernel, draw a blank 4 × 4, and fill in all sixteen. You are looking for the answer `0 24 24 0` in every row. **When a student's pencil disagrees with the computer tomorrow, you will need to have been the pencil.**
- [ ] **Find squared paper.** Two sheets per student. Freehand grids waste four minutes and produce work nobody can check.
- [ ] **Type and run `shuffle_pixels.py`. This is the hook, and you must have seen it yourself.** The complete file:

```python
"""shuffle_pixels.py - the same MLP on the real pictures and on shuffled columns."""
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digits = load_digits()
y = digits.target
order = np.random.default_rng(0).permutation(64)
print("the new column order starts:", order[:8].tolist())


def train_and_score(X):
    torch.manual_seed(0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.30,
                                              stratify=y, random_state=0)
    X_tr_t = torch.from_numpy(X_tr).float()
    X_te_t = torch.from_numpy(X_te).float()
    Y_tr_t = torch.from_numpy(np.eye(10)[y_tr]).float()
    loader = DataLoader(TensorDataset(X_tr_t, Y_tr_t), batch_size=32, shuffle=True)
    model = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Dropout(0.2), nn.Linear(64, 10))
    loss_fn = nn.BCEWithLogitsLoss()
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    for epoch in range(15):
        model.train()
        for xb, yb in loader:
            opt.zero_grad(); loss_fn(model(xb), yb).backward(); opt.step()
    model.eval()
    with torch.no_grad():
        return (model(X_te_t).numpy().argmax(axis=1) == y_te).mean()


plain = digits.data / 16.0
print("the pictures as they are     test accuracy %.4f" % train_and_score(plain))
print("the same 64 columns shuffled test accuracy %.4f" % train_and_score(plain[:, order]))
```

You must see **exactly** this:

```text
the new column order starts: [16, 36, 27, 8, 44, 23, 53, 4]
the pictures as they are     test accuracy 0.9667
the same 64 columns shuffled test accuracy 0.9704
```

**Expected runtime: under two seconds** for both 15-epoch runs. This is exactly Week 23's architecture — `64 → 64 → 10` with dropout 0.2, 4,810 learnable numbers — which is why the unshuffled line reads the same 0.9667 the student saw last week. **`plain[:, order]` is the whole trick:** it reorders the 64 columns once and applies that same order to all 1,797 rows. If your two numbers are not 0.9667 and 0.9704, a seed is missing — `torch.manual_seed(0)` **inside** `train_and_score` so both runs start from the same weights, `random_state=0` in `train_test_split`, and `default_rng(0)` for the column order.

- [ ] **Type and run `flatten_cost.py`.** The complete file:

```python
"""flatten_cost.py - price a dense layer and a convolution on the same 8x8 picture."""
import torch.nn as nn

dense = nn.Linear(64, 16)
print("nn.Linear(64, 16) - the flattened 8x8 picture into 16 units")
for name, p in dense.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in dense.parameters()))

print()
conv1 = nn.Conv2d(1, 1, kernel_size=3)
print("nn.Conv2d(1, 1, kernel_size=3) - one 3x3 filter on the same picture")
for name, p in conv1.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in conv1.parameters()))

print()
conv4 = nn.Conv2d(1, 4, kernel_size=3)
print("nn.Conv2d(1, 4, kernel_size=3) - four filters")
for name, p in conv4.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in conv4.parameters()))

print()
print("1040 divided by 10 =", 1040 // 10, "times fewer numbers")
print()
print("and on a 64x64 picture:")
print("   nn.Linear(4096, 256) needs      ",
      sum(p.numel() for p in nn.Linear(4096, 256).parameters()))
print("   nn.Conv2d(1, 4, kernel_size=3) needs",
      sum(p.numel() for p in nn.Conv2d(1, 4, kernel_size=3).parameters()))
```

You must see **exactly** this:

```text
nn.Linear(64, 16) - the flattened 8x8 picture into 16 units
   weight   (16, 64)       1024 numbers
   bias     (16,)          16 numbers
   total: 1040

nn.Conv2d(1, 1, kernel_size=3) - one 3x3 filter on the same picture
   weight   (1, 1, 3, 3)   9 numbers
   bias     (1,)           1 numbers
   total: 10

nn.Conv2d(1, 4, kernel_size=3) - four filters
   weight   (4, 1, 3, 3)   36 numbers
   bias     (4,)           4 numbers
   total: 40

1040 divided by 10 = 104 times fewer numbers

and on a 64x64 picture:
   nn.Linear(4096, 256) needs       1048832
   nn.Conv2d(1, 4, kernel_size=3) needs 40
```

**Expected runtime: instant.** No seed needed — nothing here is random, only counted.

- [ ] **Type and run `by_hand.py`.** The complete file:

```python
"""by_hand.py - sixteen output cells by hand, then the same sixteen from nn.Conv2d."""
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)   # so the random starting bias is the same one printed below

bar = np.zeros((6, 6))
bar[:, 0:3] = 10.0
bar[:, 3:6] = 2.0
print("the picture (6 x 6): bright left half, dark right half")
print(bar)

kernel = np.array([[1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0]])
print("\nthe kernel (3 x 3): a vertical-edge finder")
print(kernel)

by_hand = np.zeros((4, 4))
for r in range(4):
    for c in range(4):
        window = bar[r:r + 3, c:c + 3]
        by_hand[r, c] = (window * kernel).sum()
print("\nby hand, sixteen windows, sixteen sums:")
print(by_hand)

t = torch.from_numpy(bar).float().unsqueeze(0).unsqueeze(0)
print("\nthe picture as a tensor:", tuple(t.shape))

conv = nn.Conv2d(1, 1, kernel_size=3)
conv.weight.data = torch.from_numpy(kernel).float().reshape(1, 1, 3, 3)
conv.bias.data = torch.zeros(1)
print("conv.weight shape      :", tuple(conv.weight.shape))
print("learnable numbers      :", sum(p.numel() for p in conv.parameters()))

with torch.no_grad():
    out = conv(t)
print("the output as a tensor :", tuple(out.shape))
print("\nfrom nn.Conv2d:")
print(out[0][0].numpy())
print("\nall sixteen cells agree?", np.allclose(by_hand, out[0][0].numpy()))
```

You must see **exactly** this:

```text
the picture (6 x 6): bright left half, dark right half
[[10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]]

the kernel (3 x 3): a vertical-edge finder
[[ 1.  0. -1.]
 [ 1.  0. -1.]
 [ 1.  0. -1.]]

by hand, sixteen windows, sixteen sums:
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]

the picture as a tensor: (1, 1, 6, 6)
conv.weight shape      : (1, 1, 3, 3)
learnable numbers      : 10
the output as a tensor : (1, 1, 4, 4)

from nn.Conv2d:
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]

all sixteen cells agree? True
```

**Expected runtime: instant.** **Check your pencil grid against that printout now**, before class. If they disagree, you have found the disagreement in your kitchen instead of in front of thirty people.

- [ ] **Run `kernels.py` and open `feature_maps.png`.** The complete file is in the Answer Key under page 24.4. It writes a 4 × 4 grid of pictures — four pictures down, the original plus three feature maps across — in about two seconds. **Look at it.** The vertical-edge column lights up on the bar and the stripe and does nothing on a flat region; the average column blurs everything and finds no edges at all.
- [ ] **Break it on purpose, twice.** These are the two deliberate mistakes in the live-code:
  1. Feed the 6 × 6 tensor in without any `unsqueeze`: `RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [6, 6]`.
  2. Set the weights and **forget** `conv.bias.data = torch.zeros(1)`. No error. Every cell reads 24.088203 instead of 24.
- [ ] **Print workbook pages 24.1–24.6.** Page 24.1 must have the 6 × 6 picture pre-printed with its 10s and 2s, the 3 × 3 kernel, and a blank 4 × 4 grid. **Do not make them draw the grids in class.**
- [ ] **Add two rows to the PARAMETER COUNT wall sheet**: `dense on 8×8` and `conv 3×3 on 8×8`.

### 5 minutes on the day

- [ ] Editor open, terminal ready. `by_hand.py` and `flatten_cost.py` **deleted or renamed** — they type them.
- [ ] Squared paper and pencils out. **Pencils with rubbers.** They will make a mistake and they need to be able to fix it without starting again.
- [ ] Workbook 24.1 out, face down.
- [ ] Wall sheet with the two new rows, blank.
- [ ] Bug Log out.
- [ ] Last week's `digits_mlp.pt` and the three digit files still in the folder — the hook uses them.

### Fallback if the laptops fail

**This week is the best paper week of the term.** The central activity is already pencil and squared paper, and objective 2 does not need a computer at all — only the *check* does.

1. **The shuffle, on paper.** Print one digit as an 8 × 8 grid of numbers, then print the same 64 numbers in a shuffled order as a long row. Ask: *"which one can you read?"* Then: *"which one does a dense layer see?"* **The hook, complete, and arguably better** — they can hold both versions in their hands.
2. **The two parameter counts.** 16 × 64 + 16 = 1040 and 3 × 3 + 1 = 10, and 1040 ÷ 10 = 104. **Objective 1, complete, in four minutes.**
3. **The sixteen cells, unchanged.** This is the activity and it needs no electricity. **Objective 2's first half, complete.** For the check, put the printed `0 24 24 0` block on the board *after* everybody has finished, not before.
4. **Weight sharing on paper.** One kernel drawn once, four window outlines on the picture, and the two counts: 10 for the convolution, 36 × 16 + 16 = 592 for a dense layer doing the same job. **Objective 3, complete.**
5. **Design the horizontal kernel.** Give them the vertical one and one instruction: *"now make one that finds a left-to-right edge instead of an up-and-down one."* The answer is the vertical kernel rotated: `1 1 1 / 0 0 0 / −1 −1 −1`. Then apply it by hand to the top-left window of the cross. **Objective 4, complete, and this is the most satisfying five minutes of the paper version.**

| If this fails | Do this instead |
|---|---|
| `RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [6, 6]` | Two `.unsqueeze(0)` calls are missing. `nn.Conv2d` needs `(batch, channels, height, width)`. This is deliberate mistake one. |
| `RuntimeError: Input type (double) and bias type (float) should be the same` | `.float()` missing after `torch.from_numpy`. numpy makes 64-bit decimals; torch wants 32-bit. |
| `RuntimeError: weight should have at least three dimensions` | `.reshape(1, 1, 3, 3)` missing when assigning the kernel. |
| Every output cell is 24.088203 instead of 24 | The bias was never zeroed. `conv.bias.data = torch.zeros(1)`. This is deliberate mistake two. |
| The output is all −24 where you expected +24 | The kernel is mirrored: `−1, 0, 1` instead of `1, 0, −1`. Nothing is broken — it is finding dark-to-bright instead. |
| The feature map is 6 × 6 when you expected 4 × 4 | The picture is 8 × 8, not 6 × 6. Count the window positions: 8 − 3 + 1 = 6. |
| A window opens instead of a file being written | `matplotlib.use("Agg")` missing, or below `import matplotlib.pyplot`. It must be above. |
| A student's pencil grid disagrees with the computer | **Stop the lesson.** It is one of three things: the window slid the wrong way, a kernel row got skipped, or the kernel is mirrored. Find it. That is the lesson. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Shuffle the Pixels | 7 | 7 | Last week's model scores the same on unreadable pictures |
| 🧠 Concept & Maths — Locality, the Price, the Slide | 18 | 25 | The envelopes; 1,040 against 10; one cell worked on the board |
| 💻 Live-Code Together — `flatten_cost.py` then `by_hand.py` | 18 | 43 | The counts, then the sixteen cells. **Two deliberate mistakes.** |
| 🎲 Their Turn — Kernel on Graph Paper | 20 | 63 | Sixteen cells in pencil, then checked cell by cell |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Shuffle the Pixels (7 minutes)

**Do this:** Put last week's digit on the screen, as text art.

```text
.=@@@...
.@@@@-..
.*=-@-..
...=@-..
...@@...
..:@@.-.
..@@@@@.
.-@@@@@.
```

**Say this:**

> "Last week you built a model that reads that as a two, and it got 96.67% on 540 digits it had never seen. Good model. It is on disk, in a file, and you can open it in a fresh terminal.
>
> Today I am going to break it, and I am going to break it in a way that should worry you."

**Do this:** Write on the board:

```
one shuffle of the 64 columns,  the same shuffle for every picture
```

**Say this:**

> "I am going to shuffle the 64 columns. Not randomly per picture — one single shuffle, worked out once, applied to all 1,797 pictures identically. Column 0 always goes where column 16 was, and so on.
>
> A person cannot read the result. It is not a picture any more; it is confetti.
>
> **Predict the accuracy.** The model trains from scratch on the shuffled version, same architecture, same 15 epochs."

**Do this:** Take three predictions and write them on the board. Most will say something between 20% and 60%.

Run it:

```text
the new column order starts: [16, 36, 27, 8, 44, 23, 53, 4]
the pictures as they are     test accuracy 0.9667
the same 64 columns shuffled test accuracy 0.9704
```

**Do this:** Say nothing for five seconds. Let them read the second number.

**Ask this:** "Which one did better?"

*Hoped-for answer:* the shuffled one.

> **Say this:** "The confetti did better. By 0.0037, which on 540 digits is **two digits**, so honestly it is a tie — but a tie is the point. **The model cannot tell the difference between a picture and confetti.**
>
> And if it cannot tell the difference, then whatever it is doing, it is not looking at a picture."

**Ask this:** "Why can't it tell? Think about what `nn.Linear` actually holds."

*Hoped-for answer:* every weight joins one input slot to one unit; nothing says which slots are neighbours.

*If nobody has it:* draw eight boxes in a row on the board, number them, and ask *"which of these boxes is above box 3?"* There is no answer. That is the problem.

**Do this:** Hold up an imaginary handful of envelopes and tell the analogy.

> "Sixty-four numbered envelopes, each with the brightness of one little square, handed to you in an order nobody will tell you. You could learn 'envelope 41 is usually bright on a seven'. You would have to learn that separately for all sixty-four. And if somebody wrote the seven two squares to the left, **everything you learned would be wrong.**
>
> Now instead I give you a magnifying glass and say: slide this over the whole page and tell me wherever you see a corner. **One rule. Works everywhere.**
>
> That second thing has a name and by the end of today you will have done sixteen of them in pencil."

**Do this:** Write on the board and leave it up all lesson:

> **locality** — what a pixel means is decided by its neighbours. Flattening throws the neighbours away.

---

### 🧠 Concept & Maths — Locality, the Price, the Slide (18 minutes)

#### Part A — the price (5 minutes)

**Say this:**

> "Before we build the new thing, let's find out what the old thing costs. Eight by eight picture, flattened, into a layer with 16 units. **Count it.** You have been counting parameters for two weeks."

**Do this:** Write it on the board and let them do it.

```
weights = 16 × 64  =  ?
biases  =             ?
total   =             ?
```

*Expected:* 1024, 16, **1040**.

*If somebody drops the biases:* it is the third week running. Point at the bias line and wait.

**Say this:**

> "One thousand and forty numbers, to look at a picture with 64 pixels in it. Now here is the cost of the sliding magnifying glass, and it is nine numbers and a bias."

```
weights = 3 × 3  =  9
bias    =           1
total   =          10
```

**Ask this:** "How many times smaller?"

*Hoped-for answer:* 1040 ÷ 10 = 104.

> "A hundred and four times fewer, **and the small one is the one that knows what a neighbourhood is.** That is not a trade-off. That is a better tool that is also cheaper."

**Do this:** Write both numbers on the wall sheet, in the two new rows.

**Say this:**

> "And it gets more lopsided, fast. A 64 by 64 photograph — still small, still greyscale — into 256 units."

```
nn.Linear(4096, 256)              1,048,832
nn.Conv2d(1, 4, kernel_size=3)           40
```

> "A million against forty. And the forty **does not change** if the photo gets bigger, which we will prove in a minute."

#### Part B — one cell, on the board (9 minutes)

**Do this:** Draw the 6 × 6 picture on the board, big, with its 10s and 2s. Then the 3 × 3 kernel beside it. Then a blank 4 × 4 to the right.

```
 10  10  10   2   2   2          1   0  −1
 10  10  10   2   2   2          1   0  −1
 10  10  10   2   2   2          1   0  −1
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
```

**Say this:**

> "Left half bright, right half dark. There is a vertical edge down the middle and you can see it. The question is how a machine sees it.
>
> That little 3 by 3 grid is the magnifying glass. It has a name: a **kernel**, or a **filter** — both words mean the same thing and you will meet both. Plus down the left, minus down the right, nothing in the middle.
>
> Here is what you do with it. Put it over the top-left corner of the picture. Multiply each of its nine numbers by the picture number underneath. Add up all nine. That gives you **one** number, and that number goes in the top-left of the answer grid.
>
> Then slide it one square right and do it again. Let's do the first one together."

**Do this:** Circle rows 0–2, columns 0–2 on the board. Write the nine products out.

```
window          kernel         products
10  10  10       1  0  −1      10   0  −10
10  10  10   ×   1  0  −1  =   10   0  −10
10  10  10       1  0  −1      10   0  −10
```

**Ask this:** "Add up the top row of products."

*Hoped-for answer:* 10 + 0 − 10 = 0.

**Ask this:** "And the whole thing?"

*Hoped-for answer:* 0.

> "Zero. And that makes sense — look at the window. It is completely flat. Every number in it is 10. **There is no edge there, and the filter says nothing.** A kernel that reports zero is not broken; it is telling you it did not find its thing."

**Do this:** Rub out the circle and draw it one column right — rows 0–2, columns 1–3.

**Ask this:** "What does each row of the window read now?"

*Hoped-for answer:* 10, 10, 2.

**Do this:** Work it on the board, slowly.

```
one row:      (1 × 10)  +  (0 × 10)  +  (−1 × 2)   =   10 − 2   =   8
three rows:   8 + 8 + 8                            =   24
```

> "Twenty-four. The edge is inside the window now and the filter **shouts**. Zero when there is nothing there, 24 when there is. That is a detector."

**Ask this:** "Slide it one more. Rows 0 to 2, columns 2 to 4. What does each row read, and what is the answer?"

*Hoped-for answer:* 10, 2, 2 → 10 − 2 = 8 per row → 24.

**Ask this:** "One more. Columns 3 to 5."

*Hoped-for answer:* 2, 2, 2 → flat → 0.

**Do this:** Fill in the first row of the answer grid: `0 24 24 0`.

**Ask this:** "Now — how many cells are in the whole answer grid? Count the places the window can sit."

*Hoped-for answer:* four across, four down, sixteen.

*If they guess 36 (the picture size):* ask *"can the window start at column 4? What would it hang off the end of?"*

**Do this:** Write the counting out, and **stop there**:

```
across:  starts at column 0, 1, 2 or 3  →  6 − 3 + 1 = 4
down:    the same                       →  6 − 3 + 1 = 4
cells:   4 × 4 = 16
```

> **Say this:** "Sixteen. And that grid of sixteen answers has a name too: a **feature map**. It is a map of where the filter found its feature.
>
> And if somebody is already working out a general formula for that — good, hold it, write it in the margin. **That is next week's entire lesson.** Today you count."

#### Part C — weight sharing (4 minutes)

**Ask this:** "How many times did I change the kernel while I was sliding it?"

*Hoped-for answer:* never.

> **Say this:** "Never. **The same nine numbers, at all sixteen positions.** That has a name: **weight sharing**, and it buys you two completely different things.
>
> **The first is cheap.** Nine weights and a bias is ten numbers. A dense layer making the same 4 by 4 answer grid out of those 36 pixels would need 36 × 16 + 16 = 592.
>
> **The second is the one that actually matters.** The dense layer would have to learn 'there's an edge here' **sixteen separate times** — once for each position — and it would need training pictures with an edge in each of the sixteen places. The convolution learns it **once** and gets all sixteen for free.
>
> That is why these things work on far less data than you would expect."

**Do this:** Hand out squared paper and workbook 24.1, and say the activity is coming. Do not start it yet.

---

### 💻 Live-Code Together — `flatten_cost.py` then `by_hand.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — the two counts.**

```python
"""flatten_cost.py - price a dense layer and a convolution on the same 8x8 picture."""
import torch.nn as nn

dense = nn.Linear(64, 16)
print("nn.Linear(64, 16) - the flattened 8x8 picture into 16 units")
for name, p in dense.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in dense.parameters()))

print()
conv1 = nn.Conv2d(1, 1, kernel_size=3)
print("nn.Conv2d(1, 1, kernel_size=3) - one 3x3 filter on the same picture")
for name, p in conv1.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in conv1.parameters()))
```

**Ask before running:** "The conv layer's weight — what shape do you think prints?"

*Most will say (3, 3).* Run it:

```text
nn.Linear(64, 16) - the flattened 8x8 picture into 16 units
   weight   (16, 64)       1024 numbers
   bias     (16,)          16 numbers
   total: 1040

nn.Conv2d(1, 1, kernel_size=3) - one 3x3 filter on the same picture
   weight   (1, 1, 3, 3)   9 numbers
   bias     (1,)           1 numbers
   total: 10
```

> **Say this:** "1040 and 10, exactly as you counted. **Both of those numbers were on the board before we ran anything**, which is the habit from Week 22 and it is not going away.
>
> Now the shape: `(1, 1, 3, 3)`. **Four numbers, and it is still nine weights.** Read them out loud in order: one filter, looking at one input channel, three high, three wide. 1 × 1 × 3 × 3 = 9.
>
> Why write it with four numbers instead of two? Because next week the pictures get channels, and the week after that we have thirty-two filters, and by then you want the layout to have been the same all along."

Add the four-filter version:

```python
conv4 = nn.Conv2d(1, 4, kernel_size=3)
print("nn.Conv2d(1, 4, kernel_size=3) - four filters")
for name, p in conv4.named_parameters():
    print("   %-8s %-14s %d numbers" % (name, str(tuple(p.shape)), p.numel()))
print("   total:", sum(p.numel() for p in conv4.parameters()))
```

```text
nn.Conv2d(1, 4, kernel_size=3) - four filters
   weight   (4, 1, 3, 3)   36 numbers
   bias     (4,)           4 numbers
   total: 40
```

> "Four filters. `(4, 1, 3, 3)` — four of them, each one channel in, each 3 by 3. Thirty-six weights, four biases, one per filter. **Four different detectors, forty numbers, and each one produces its own feature map.** Those output maps are called **channels**, and after a conv layer a channel is not a colour any more — it is whatever that filter found."

**Step 2 (4 min) — write the picture and the kernel.**

```python
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)   # so the bias in step 4 is the 0.088204 printed here

bar = np.zeros((6, 6))
bar[:, 0:3] = 10.0
bar[:, 3:6] = 2.0
print(bar)

kernel = np.array([[1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0]])
print(kernel)
```

```text
[[10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]
 [10. 10. 10.  2.  2.  2.]]
[[ 1.  0. -1.]
 [ 1.  0. -1.]
 [ 1.  0. -1.]]
```

> **Say this:** "That is the picture from the board, and we wrote it ourselves in three lines. **This is better than downloading a dataset for today**, because there is nothing about that picture you do not know."

Then the by-hand loop:

```python
by_hand = np.zeros((4, 4))
for r in range(4):
    for c in range(4):
        window = bar[r:r + 3, c:c + 3]
        by_hand[r, c] = (window * kernel).sum()
print(by_hand)
```

```text
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]
```

> "Sixteen windows, sixteen sums, and the first row is `0 24 24 0` — **which is exactly what we got on the board.** `bar[r:r+3, c:c+3]` cuts out the window; `(window * kernel).sum()` multiplies the nine pairs and adds them. Two loops and no library at all. **This is what `nn.Conv2d` does.**"

**Step 3 (4 min) — 🐞 DELIBERATE MISTAKE ONE: feed the picture straight in.**

```python
conv = nn.Conv2d(1, 1, kernel_size=3)
conv(torch.from_numpy(bar).float())
```

Run it. Real output:

```text
RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [6, 6]
```

**Ask this:** "It wants three or four numbers in the shape and we gave it two. What could the other two possibly be?"

*Hoped-for answer:* something about how many pictures and how many colour layers.

> **Say this:** "`nn.Conv2d` always wants four: **how many pictures, how many channels each, how tall, how wide.** Every time. Our one greyscale 6 by 6 picture is one picture with one channel, so it should be `(1, 1, 6, 6)`.
>
> And the tool that adds a 1 at the front is `unsqueeze(0)`. **One photo, put in an envelope, and the envelope put in a box.** Nothing about the photo changes; it is just wrapped the way the machine expects."

Fix it live:

```python
t = torch.from_numpy(bar).float().unsqueeze(0).unsqueeze(0)
print("the picture as a tensor:", tuple(t.shape))
```

```text
the picture as a tensor: (1, 1, 6, 6)
```

**Do this:** Bug Log, ninety seconds. Make sure the words *"batch, channels, height, width"* are in the entry.

**Step 4 (6 min) — load the kernel, and 🐞 DELIBERATE MISTAKE TWO.**

```python
conv.weight.data = torch.from_numpy(kernel).float().reshape(1, 1, 3, 3)
with torch.no_grad():
    out = conv(t)
print(out[0][0].numpy())
```

Run it. Real output:

```text
[[ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]
 [ 0.08820419 24.088203   24.088203    0.08820419]]
```

**Do this:** Say nothing. Point at 24.088203, then at the 24 on the board.

**Ask this:** "Nearly right. What has been added to every single cell, and where did it come from?"

*Hoped-for answer:* about 0.088, added everywhere — the bias.

*If they say "a rounding error":* ask *"is it the same amount in every cell?"* It is, exactly. Rounding errors are not identical sixteen times.

> **Say this:** "0.088204, in all sixteen cells, and it is not a rounding error — **it is the bias.** We set the nine weights and left the bias alone, so PyTorch's random starting value is still in there, being added to every window's answer.
>
> Today we are not training this thing, we are checking arithmetic — so the bias has to go."

Fix it live:

```python
conv.bias.data = torch.zeros(1)
with torch.no_grad():
    out = conv(t)
print(out[0][0].numpy())
print("all sixteen cells agree?", np.allclose(by_hand, out[0][0].numpy()))
```

```text
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]
all sixteen cells agree? True
```

**Do this:** Bug Log. **This is the most valuable entry of the week** — a wrong answer that is nearly right, with no error message. The words to get into it: *"a bias is added to every cell of the feature map."*

> **Say this:** "`all sixteen cells agree? True`. Sixteen sums we did on the board and in a loop, and sixteen from a PyTorch layer, and every one matches.
>
> **`nn.Conv2d` is not doing anything you cannot do with a pencil.** It is doing it 3,844 times on a 64 by 64 picture instead of sixteen times, and it will do it fast enough to be useful, and it will learn the nine numbers for itself starting in Week 26. But it is this."

---

### 🎲 Their Turn — Kernel on Graph Paper (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: draw the 6 × 6 picture on squared paper, slide the kernel by hand, fill all sixteen cells in pencil, then load the identical nine numbers into `nn.Conv2d` and check every cell. **Any disagreement stops the lesson until it is found.**

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Hold up one student's pencilled grid next to the printout on the screen.

**Say this:**

> "Sixteen cells in pencil. Sixteen cells from PyTorch. Every one the same.
>
> Three things to take away.
>
> **One.** Flattening throws away which pixels are next to which. Your digits model scored the same on shuffled confetti — 0.9667 against 0.9704 — because it never knew the difference. **It was never looking at a picture.**
>
> **Two.** A convolution is nine numbers that slide. Nine weights and a bias, ten numbers, against 1,040 for a dense layer on the same 8 by 8 picture. **A hundred and four times fewer, and it is the one that keeps the neighbourhood.**
>
> **Three.** The same nine numbers at every position — **weight sharing** — which is why the count does not grow when the picture does. Ten numbers on a 6 by 6, ten numbers on a 64 by 64 with 3,844 output cells."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last thing, and it is next week's door.
>
> Our 6 by 6 picture gave a 4 by 4 answer. The 8 by 8 one gave 6 by 6. You got both of those by counting where the window fits, and counting is fine when the picture is six wide.
>
> Next week the window starts jumping two at a time, and we start gluing rings of zeros round the edge so the corners get a fair hearing — and then you cannot count it any more, you have to work it out. **Which is next week's one piece of maths, and it is one line long, and if you cannot do it on paper the error message will find you.**"

**Do this:** Hand out the homework and read part one out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `RuntimeError: Expected 3D (unbatched) or 4D (batched) input to conv2d, but got input of size: [6, 6]` | "You gave me a flat grid. I need to know how many pictures and how many channels." | The two `.unsqueeze(0)` calls are missing. | `torch.from_numpy(img).float().unsqueeze(0).unsqueeze(0)` → `(1, 1, 6, 6)`. **`nn.Conv2d` always wants (batch, channels, height, width).** |
| `RuntimeError: Input type (double) and bias type (float) should be the same` | "Your picture is 64-bit decimals and my weights are 32-bit." | `.float()` missing after `torch.from_numpy`. numpy's default is float64. | Add `.float()`. **Every tensor made from numpy in this course gets it.** |
| `TypeError: conv2d() received an invalid combination of arguments - got (numpy.ndarray, Parameter, Parameter, ...)` | "That is a numpy array, not a tensor." | The picture went in without `torch.from_numpy`. | `conv(torch.from_numpy(img).float().unsqueeze(0).unsqueeze(0))`. |
| `RuntimeError: weight should have at least three dimensions` | "The nine numbers you handed me are a flat 3 by 3; a kernel needs four dimensions." | `.reshape(1, 1, 3, 3)` missing when assigning to `conv.weight.data`. | `torch.from_numpy(kernel).float().reshape(1, 1, 3, 3)`. |
| `RuntimeError: shape '[1, 1, 3, 3]' is invalid for input of size 6` | "You asked me to fold six numbers into a shape that needs nine." | The kernel was typed with a row missing, or a row has two numbers instead of three. | Count the numbers in the kernel. A 3 × 3 has **nine**. |
| `TypeError: cannot assign 'torch.FloatTensor' as parameter 'weight' (torch.nn.Parameter or None expected)` | "You tried to replace the parameter itself, not the numbers in it." | `conv.weight = tensor` instead of `conv.weight.data = tensor`. | **`.data` is how you reach the numbers inside.** Add it. |
| `RuntimeError: Given groups=1, weight of size [1, 4, 3, 3], expected input[1, 1, 6, 6] to have 4 channels, but got 1 channels instead` | "I was built expecting four channels in and your picture has one." | The two numbers are the wrong way round: `nn.Conv2d(4, 1, ...)` instead of `nn.Conv2d(1, 4, ...)`. | **Channels in first, filters out second.** One greyscale picture is `nn.Conv2d(1, ...)`. |
| `RuntimeError: Calculated padded input size per channel: (6 x 6). Kernel size: (9 x 9). Kernel size can't be greater than actual input size` | "Your magnifying glass is bigger than the page." | `kernel_size=9` on a 6 × 6 picture. | Kernel must fit. On a 6 × 6, the biggest usable is 6 — and 3 is what everybody uses. |
| **No error. Every cell is 24.088203 instead of 24.** | Nothing crashed. All sixteen answers are off by the same amount. | `conv.bias.data = torch.zeros(1)` missing, so PyTorch's random starting bias is added to every cell. | Zero the bias. **The tell is that the error is identical in all sixteen cells** — a rounding error would not be. |
| **No error. Every 24 is a −24.** | Nothing crashed. The filter is looking for the opposite thing. | The kernel is mirrored: `−1, 0, 1` instead of `1, 0, −1`. | **Nothing to fix if that is what you wanted.** A negative feature map means dark-to-bright instead of bright-to-dark. Flip the kernel or accept the sign. |
| **No error. The feature map is 6 × 6 when you predicted 4 × 4.** | Nothing crashed; the picture is not the size you thought. | The picture is 8 × 8. | Count the window positions: 8 − 3 + 1 = 6. **Print the picture's shape before you predict the output's.** |
| **No error. One pencil cell disagrees with the printout.** | The most important bug of the week. | One of three things: the window slid down instead of right, a kernel row got skipped, or the kernel is mirrored. | **Re-do that one window out loud, nine products at a time.** Do not re-do all sixteen. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three.

23. **"How many numbers are in the shape, and what is each one?"** For every conv error. Four: pictures, channels, height, width. A student who can say all four out loud has fixed most of this week's errors before they finish the sentence.

24. **"Is the error the same in every cell, or different?"** The single best question for a nearly-right feature map. **Identical in every cell means a bias.** Different in every cell means the arithmetic.

25. **"Do that one window again, out loud, nine products at a time."** When a pencil cell disagrees. **Never re-do all sixteen** — find the one and it will be one of the three causes. Re-doing everything hides the mistake and takes five minutes you do not have.

And the sentence for this week:

> **"A feature map that is off by the same amount everywhere has a bias in it. A feature map with the wrong sign has a mirrored kernel. Neither of those is a maths mistake, and neither produces an error message."**

---

## 🎲 The Activity, In Full

### Kernel on Graph Paper

**What it is.** Sixteen sums in pencil, then sixteen from `nn.Conv2d`, then a cell-by-cell comparison. It is the only activity this term where a single disagreement stops the class, and that rule is the reason it works.

### Setup

- **Squared paper, two sheets each.** Not optional.
- **A pencil with a rubber.** Also not optional.
- Workbook page 24.1, pre-printed with the 6 × 6 picture (10s on the left, 2s on the right), the 3 × 3 kernel, and a blank 4 × 4 grid.
- Laptops **closed** for part 1.
- The 6 × 6 picture and the kernel still on the board from the concept segment.

### Part 1 — sixteen cells in pencil (10 minutes)

Read the instruction once and then say nothing:

> **"Sixteen cells. For each one: put the window over the picture, multiply the nine pairs, add them up, write the answer in the box. Laptops closed. You have ten minutes and you will not need all of them."**

**The answer, all sixteen:**

```
   0   24   24    0
   0   24   24    0
   0   24   24    0
   0   24   24    0
```

**Watch for exactly three failure modes.** Learn these three; they cover almost every mistake you will see.

1. **The window slid down instead of right.** The first row of their grid reads `0 0 0 0` or has values in the wrong places. Ask: *"which cell of the answer are you filling in — the one across or the one down?"*
2. **A kernel row got skipped**, so the answers are 8 or 16 instead of 24. Ask: *"how many rows did you add up?"* Three.
3. **The kernel is mirrored**, so everything is −24. Ask: *"read me your kernel's top row."* If it is `−1 0 1`, nothing is wrong with their arithmetic at all — say so, and say what it means.

**Sit on your hands.** Do not walk round correcting. Ten minutes of sixteen sums is the objective.

**A note on speed.** Most students will finish in five minutes once they notice that every row of the picture is identical, so every row of the answer must be identical. **That noticing is worth praising out loud** — it is the same reasoning that makes convolutions efficient in the first place.

### Part 2 — check it, cell by cell (7 minutes)

> **"Laptops open. Type this. Do not change your pencil grid."**

They type `by_hand.py` from the Prep Checklist — but **only the second half**, the `nn.Conv2d` part, because the loop version would do their homework for them:

```python
import numpy as np
import torch
import torch.nn as nn

bar = np.zeros((6, 6))
bar[:, 0:3] = 10.0
bar[:, 3:6] = 2.0

kernel = np.array([[1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0]])

t = torch.from_numpy(bar).float().unsqueeze(0).unsqueeze(0)
conv = nn.Conv2d(1, 1, kernel_size=3)
conv.weight.data = torch.from_numpy(kernel).float().reshape(1, 1, 3, 3)
conv.bias.data = torch.zeros(1)
with torch.no_grad():
    out = conv(t)
print(out[0][0].numpy())
```

```text
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]
```

> **"Now compare. Cell by cell. Read them out: zero, twenty-four, twenty-four, zero."**

**And the rule, stated out loud before anyone starts comparing:**

> **"If one cell disagrees, we stop and find it. Not later — now. Put your hand up."**

Mean it. And when it happens, do it in front of everybody, with the three questions above, and finish by thanking them. **A room that has watched one disagreement get found is a room that will keep checking.**

### Part 3 — design the horizontal one (3 minutes)

> **"You have a kernel that finds up-and-down edges. Make one that finds left-and-right edges instead. Nine numbers."**

The answer is the same kernel rotated a quarter turn:

```
  1   1   1
  0   0   0
 −1  −1  −1
```

Then one question and one check:

**Ask this:** "Run it on the bar picture — the one with the vertical edge. What will it say?"

*Hoped-for answer:* nothing, zero everywhere.

```text
bar     -> feature maps (3, 6, 6)
   vertical edge    biggest  +24.00   smallest   +0.00
   horizontal edge  biggest   +0.00   smallest   +0.00
```

**Zero everywhere.** The horizontal detector is completely silent on a vertical edge, and that is exactly right. **A detector that fires at everything is not a detector.**

### What "finished" looks like

- A pencilled 4 × 4 reading `0 24 24 0` four times.
- A printed 4 × 4 reading the same, and the student has read them out loud against each other.
- A second kernel, written by them, that produces zeros on the bar picture.
- The student can say, unprompted: *"the same nine numbers, sixteen times, and I never changed them."*

### Variation — easier

**Do four cells instead of sixteen** — just the top row. Every row of the picture is identical, so the top row of the answer *is* the answer, repeated. Say that out loud as permission: **"work out one row, then copy it down three times, and tell me why you are allowed to."**

**And use a 4 × 4 picture instead of 6 × 6**, so there are only four cells in total. Three columns of 10 and one of 2:

```
picture              kernel          answer (2 × 2)
10  10  10   2        1  0  −1         0   24
10  10  10   2        1  0  −1         0   24
10  10  10   2        1  0  −1
10  10  10   2
```

The window can start at column 0 or column 1 — `4 − 3 + 1 = 2` — and the same going down, so **four cells, four sums**:

```
cell (0,0):  window rows are 10, 10, 10  →  10 + 0 − 10 = 0 per row  →  0 + 0 + 0  =   0
cell (0,1):  window rows are 10, 10,  2  →  10 + 0 −  2 = 8 per row  →  8 + 8 + 8  =  24
```

**Confirmed against `nn.Conv2d`:**

```text
[[ 0. 24.]
 [ 0. 24.]]
```

Four sums, and **objective 2 is complete**.

**Give them the check code complete** so all they do is run it and compare.

### Variation — harder

1. **Predict the whole feature map for the cross, all thirty-six cells, before running it.** The cross is 8 × 8 so the map is 6 × 6, and the real answer is:

```text
[[  0. -27. -27.  27.  27.   0.]
 [  0. -18. -18.  18.  18.   0.]
 [  0.  -9.  -9.   9.   9.   0.]
 [  0.  -9.  -9.   9.   9.   0.]
 [  0. -18. -18.  18.  18.   0.]
 [  0. -27. -27.  27.  27.   0.]]
```

Then the question that makes it worth it: **why are there negatives, and why do the numbers get smaller towards the middle?** Negatives because the left edge of the cross's vertical bar is a dark-to-bright step, the mirror image of the right edge. Smaller in the middle because the horizontal bar of the cross fills those windows with 9s on both sides, so the pluses and minuses partly cancel. **Explaining the 18 and the 9 unaided is a level-5 answer.**

2. **Design a kernel that finds a diagonal edge**, and test it on the cross and on the noisy picture. There is no single right answer, which is the interesting part — `1 1 0 / 1 0 −1 / 0 −1 −1` is one.

3. **Design a kernel that does nothing at all** — the identity. `0 0 0 / 0 1 0 / 0 0 0`, and the feature map is the middle of the picture, unchanged. Then: *"how big is the output, and why is it smaller than the input if the kernel does nothing?"* Because the window still cannot hang off the edge. **That is next week's padding, arrived at from the right direction.**

4. **Prove weight sharing empirically.** Run the same ten-number conv on four picture sizes and print the count each time:

```text
learnable numbers in this layer: 10
picture  6 x  6  ->  feature map  4 x  4  =   16 cells,   still 10 learnable numbers
picture  8 x  8  ->  feature map  6 x  6  =   36 cells,   still 10 learnable numbers
picture 16 x 16  ->  feature map 14 x 14  =  196 cells,   still 10 learnable numbers
picture 64 x 64  ->  feature map 62 x 62  = 3844 cells,   still 10 learnable numbers
```

Then: *"how many numbers would a dense layer need for the last row, to produce the same 3,844 outputs from 4,096 pixels?"* `3844 × 4096 + 3844 = 15,748,868`. **Fifteen and a half million against ten.**

5. **The honest question:** *"our vertical kernel gave 24 on the bar and 27 on the cross. Is the cross's edge sharper?"* No — the cross is made of 9s and 0s, so each row contributes `9 − 0 = 9`, and three rows give 27. The bar is 10s and 2s, so each row gives `10 − 2 = 8` and three rows give 24. **The number depends on the contrast, not on how "edge-like" it is**, which is why real networks normalise their inputs. That connects straight back to Week 4.

---

## ❓ Questions Students Ask This Week

**"If the shuffled pictures worked just as well, was last week a waste of time?"**

No, and the reason is worth saying carefully. **Last week's model works.** 96.67% is a real score on 540 real digits it had never seen, and the engineering — the class, the batches, the file, the `predict.py` — is all still exactly right and all still used in Week 26.

What the shuffle test shows is that the model is **fragile in a specific way**. It learned which of 64 particular slots tend to be bright for each digit. Move a digit two pixels left and every one of those slots changes, so it fails — and `load_digits` happens to be a very tidy dataset where everything is centred, which is why it got away with it. **A model that gets the right answer for a reason that will not survive contact with reality is a real thing to worry about**, and finding out how yours is fragile is most of engineering.

**"Where do the nine numbers come from?"**

Today, from you. You chose `1 0 −1` because you wanted a vertical edge, and it works.

For about thirty years that is how computer vision was done — people designed filters by hand, published them, and gave them names. Then in 2012 a network called AlexNet won an image competition by an embarrassing margin, and its trick was almost rude: **do not design the nine numbers, make them weights and let gradient descent find them.** When researchers drew the learned first-layer filters as little pictures, they looked like — edge detectors and colour blobs. The same things people had been hand-drawing all along.

**That is Week 26**, and the fact that you are choosing them by hand today is deliberate: you will recognise what the trained ones are for.

**"Why is the answer smaller than the picture?"**

Because the window cannot hang off the edge. A 3-wide window on a 6-wide picture has four places to start, not six. So a 6 × 6 gives a 4 × 4, and you lose one ring of cells all the way round.

**And it has a consequence people find unfair when it is pointed out:** the corner pixel of your picture takes part in exactly **one** of the sixteen sums, while a middle pixel takes part in nine. The model gets nine times less evidence about corners. There is a fix — you glue a ring of zeros round the edge before you slide — and it is **next week**.

**"What is the difference between a kernel and a filter?"**

Nothing. They are two words for the same 3 × 3 grid of numbers, and different textbooks prefer different ones. You will meet both, sometimes in the same paragraph. **Use whichever you like and recognise both.**

(If you want to be pedantic: some authors say "kernel" for the 3 × 3 slice that looks at one channel and "filter" for the whole stack of them across all channels. Almost nobody is consistent about it, so do not build anything on the distinction.)

**"Could I use a 1 × 1 kernel? A 6 × 6 one?"**

Both are legal and both are used.

A **1 × 1** kernel looks at one pixel at a time, so it cannot see a neighbourhood at all — which sounds useless and is not, because with several input channels it becomes a way of mixing channels together. That is beyond this level but it is a real technique.

A **6 × 6** on a 6 × 6 picture gives a 1 × 1 answer: one number for the whole picture, and 37 learnable numbers instead of 10. In between, `3 × 3` won. Two 3 × 3 layers stacked see the same 5 × 5 region as one 5 × 5 layer, and cost 18 weights instead of 25, and give you an extra squash in the middle. **The whole field converged on 3 × 3 and it was an empirical result, not a proof.**

**"Does the filter fire more strongly on a sharper edge?"**

Not exactly — and this one catches people out, so it is worth being precise. Our vertical kernel gives **24** on the bar and **27** on the cross. The cross's edge is not sharper; the cross is made of 9s and 0s, so every row contributes `9 − 0 = 9`, and three rows give 27. The bar is 10s and 2s, so `10 − 2 = 8` per row and 24 in total.

**The number depends on the contrast of the picture, not on how edge-like the edge is.** Which means a brightly-lit photo produces bigger feature maps than a dim one of the same scene, and that is a nuisance you fix by standardising the input — Week 4's lesson, arriving in a new place.

**"Isn't this the same as blurring in a photo app?"**

Yes, genuinely, and it is worth saying so because it demystifies the whole thing. Blur, sharpen, edge-detect, emboss — those are all 3 × 3 or 5 × 5 kernels slid across the picture, exactly as you did with a pencil. Our third kernel, nine copies of one-ninth, **is** a blur: it replaces every pixel with the average of its nine neighbours.

```text
bar     -> feature maps (3, 6, 6)
   average          biggest  +10.00   smallest   +2.00
```

The image-editing people got there decades earlier. **The only new idea in a CNN is letting the nine numbers be learned instead of chosen**, and then stacking a few dozen of them.

**"So should anyone ever flatten an image into a dense layer?"** *(Nobody fully agrees, and here is why.)*

**This has become a live argument again, after twenty years of the answer being obviously "no".** Be straight about it.

**What everybody agrees on:** for a small dataset, a convolution wins, and it is not close. The assumption baked into a conv layer — nearby pixels are related — is *true of pictures*, and it is free. You get it without spending any training data on learning it. On 1,797 digits or 50,000 photos, that is decisive.

**Where it splits.** The old position: never flatten, the inductive bias is what makes vision work. The newer position, which has won some very large arguments since about 2020: with enough data — hundreds of millions of images — a model *without* the assumption can learn something better than the assumption, because our assumption is only approximately right. Objects have parts that relate across the whole image, and a conv layer's insistence on locality is a limit as well as a gift. The architectures that do this are called Vision Transformers, and at large scale they beat CNNs.

**And there is a third position which is the honest one:** the argument is not really about pictures, it is about **whether you have enough data to learn the thing you would otherwise have to assume.** Every inductive bias is a loan against your dataset. If your dataset is small, take the loan gratefully. If it is enormous, you can afford to buy the truth outright and it will be better than the loan.

What to tell a 14-year-old, out loud: **"on your laptop, with your data, use the convolution — it is a hundred times cheaper and it already knows something true. And know that 'the model should be told less and shown more' is a real position that keeps winning at scales you and I will never train at."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The sixteen cells get skipped or shortened** | It is ten minutes of arithmetic and it feels slow | **Do not cut it.** It is objective 2, and it is the only place in the course where the student personally executes a convolution. Cut part 3 or the harder variations instead. A student who has not done the sixteen sums cannot debug a shape error in Week 25. |
| A pencil cell disagrees and gets waved through | Stopping feels like losing time | **Stop.** Three questions — which way did the window slide, how many rows did you add, read me your kernel's top row — and it is found in ninety seconds. Waving it through is what makes Weeks 25, 26 and 27 impossible. |
| The output-size rule gets taught | Somebody derives it, and it is only one line | Be delighted, write it in the margin, and say *"that is next week's lesson and you have just done it."* **Do not put the general form on the board.** Week 25 needs the derivation-by-counting to land first, or the formula becomes a thing to memorise. |
| The 24.088 output gets read as a rounding error | It looks like one | One question: *"is it the same amount in every cell?"* It is, exactly, sixteen times. **Rounding errors are not identical.** |
| The negative feature map gets treated as a bug | Nobody expects a detector to produce minus numbers | Say it **before** it happens, in the concept segment. A mirrored kernel finds the opposite polarity, and a negative is a correct answer to a different question. |
| The four numbers in the conv shape become a thing to memorise | `(4, 1, 3, 3)` looks arbitrary | Read it out loud every single time it appears: *"four filters, one channel in, three high, three wide."* Never let the shape be spoken as four digits. |
| `unsqueeze` gets explained as "add a 1" and nothing more | That is what it does | Give it the meaning too: *"one photo, in an envelope, in a box."* A student who knows what the two 1s **mean** will fix their own shape errors; one who knows the incantation will not. |
| The parameter counts get printed but never compared | The comparison is the objective, not the printing | **Both numbers on the wall sheet, in the two columns, and the verdict said out loud.** 1,040 against 10. |
| Somebody asks about colour images and the lesson goes to 27 channels | It is a completely reasonable question | One sentence: *"a 3 × 3 filter on a colour image has 3 × 3 × 3 = 27 weights, one for each colour layer, plus a bias. Same idea, three times the numbers. Weeks 26 and 27."* Then stop. |
| The activity becomes a typing exercise | Part 2 is twelve lines and part 1 is ten minutes of pencil | **Laptops closed for part 1.** Say it and mean it, exactly as in Week 22. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the 6 × 6 picture down to a 4 × 4 one, so there are four cells instead of sixteen. The easier variation has the numbers: the answer is `0 24 / 0 24`. **Four sums still delivers objective 2**, because the skill is one window, done properly, and then repeated.

**Cut:** the third kernel (the average) and part 3 of the activity.

**Cut:** the four-picture-size weight-sharing proof. Say it in words instead: *"the same nine numbers, everywhere."*

**Give them the check code complete.** Nothing in today's learning is in typing an `unsqueeze`.

**And give explicit permission to use the repeated-rows shortcut:** *"every row of this picture is the same, so every row of the answer is the same. Work out the top row and copy it down. Tell me why that is allowed."*

**The copy-this-exactly scaffold**, and it is short on purpose:

```python
import numpy as np

picture = np.array([[10.0, 10.0, 2.0, 2.0],
                    [10.0, 10.0, 2.0, 2.0],
                    [10.0, 10.0, 2.0, 2.0],
                    [10.0, 10.0, 2.0, 2.0]])
kernel = np.array([[1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0],
                   [1.0, 0.0, -1.0]])

window = picture[0:3, 0:3]
print("the window:")
print(window)
print("the nine products:")
print(window * kernel)
print("their sum:", (window * kernel).sum())
```

```text
the window:
[[10. 10.  2.]
 [10. 10.  2.]
 [10. 10.  2.]]
the nine products:
[[10.  0. -2.]
 [10.  0. -2.]
 [10.  0. -2.]]
their sum: 24.0
```

Then three questions and nothing else: **"how many products are there? what is each row of products adding up to? and what is 8 + 8 + 8?"** Nine; 8; 24. **That is one convolution cell, completely, and it is the whole idea.**

**The version of the arithmetic with nothing hard in it.** One table, one row per window, and only the adding left:

| window contents (each row) | 1 × first | 0 × second | −1 × third | one row | three rows |
|---|---|---|---|---|---|
| 10, 10, 10 | 10 | 0 | −10 | **0** | **0** |
| 10, 10, 2 | 10 | 0 | −2 | **8** | **24** |
| 10, 2, 2 | 10 | 0 | −2 | **8** | **24** |
| 2, 2, 2 | 2 | 0 | −2 | **0** | **0** |

Four rows, and the last column is the answer: **0, 24, 24, 0**. That is objective 2, delivered with a calculator.

**One thing you must not cut:** the comparison of the pencil grid with the printout, cell by cell. If the whole lesson collapses to one sentence, make it *"a convolution is nine multiplications and an addition, done over and over, and I did it with a pencil."*

### If the student is flying

None of these need syntax from a later week.

1. **Predict all thirty-six cells of the cross's feature map** (harder variation 1) and then explain the 18s and the 9s. **The best twenty minutes available today**, and the explanation — pluses and minuses partly cancelling where the horizontal bar fills the window — is genuinely hard.
2. **Design an identity kernel** (harder variation 3), then answer *"why is the output smaller if the kernel does nothing?"* — because the window still cannot hang off the edge. **That is padding, arrived at from the right direction, a week early.**
3. **The fifteen-million comparison** (harder variation 4): a dense layer producing 3,844 outputs from 4,096 pixels needs `3844 × 4096 + 3844 = 15,748,868` numbers. The conv needs 10.
4. **Design a diagonal detector** (harder variation 2) and test it on all four pictures. There is no unique answer and arguing about which is better is the point.
5. **The contrast question** (harder variation 5): 24 on the bar, 27 on the cross, and the reason is the pixel values, not the edges. Then the follow-up: *"what would you do about that before feeding real photographs in?"* Standardise them — Week 4, in a new costume.
6. **The honest question:** *"the shuffled model scored 0.9704 and the normal one scored 0.9667. Have I just proved that shuffling helps?"* No — 0.0037 of 540 rows is two digits, and a different seed reverses it. **You have proved that this measurement cannot tell the two apart**, which is a different and more useful statement. Week 11's small-denominator lesson, again.

### If the student won't engage today

**Close the laptop. Squared paper and a pencil, and nothing else.**

Better still: **let them draw the picture.** Any 6 × 6 pattern they like, in numbers 0 to 9. Their initial. A smiley face. A diagonal.

Three instructions and nothing else:

> **"Draw me a 6 by 6 picture. Any numbers you like, 0 to 9."**
>
> **"Here are nine numbers. Slide them over your picture, sixteen times, and write down what comes out."**
>
> **"Now show me where in your answer grid the edges of your drawing are."**

The last instruction is the whole lesson and it works on any picture they invent, which is why letting them choose costs nothing. **A student who can point at their own feature map and say "that big number is where my line was" has objective 2 and most of objective 4**, and they got there by drawing.

If there is appetite for one more, hand them the four-row table from the struggling path. Two objectives out of four, on paper, in twelve minutes. The typing survives; Week 25 does all of it again with stride and padding, and Week 26 lets the numbers learn themselves.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the price (spoken, 45 seconds)**

> "An 8 by 8 picture. **How many learnable numbers in `nn.Linear(64, 16)`, how many in one 3 by 3 convolution, and which of the two knows that pixels have neighbours?**"

*Good answer:* "16 × 64 = 1024 weights plus 16 biases, so 1,040. The convolution is 9 weights plus 1 bias, so 10. The convolution is the one that knows about neighbours, and it is 104 times smaller."

**What to catch:** an answer that gets both numbers and cannot say which is the better tool. Push once: *"which one would still work if the digit moved two pixels left?"*

**Check 2 — one cell (written on paper, 90 seconds)**

> "Here is a window and a kernel. **Give me the one number that comes out, and show the arithmetic.**"

```
window          kernel
 10  10   2      1   0  −1
 10  10   2      1   0  −1
 10  10   2      1   0  −1
```

*Good answer:* "(1 × 10) + (0 × 10) + (−1 × 2) = 8 for one row, and three identical rows, so 8 + 8 + 8 = **24**."

**Full marks needs the arithmetic, not just the 24.** A student who writes 24 with no working may have remembered it from the board.

**Check 3 — weight sharing (spoken, 60 seconds)**

> "The same 3 by 3 kernel is used at all sixteen positions instead of learning sixteen different ones. **Give me two separate things that buys you.**"

*Good answer:* "One, it's cheap — ten numbers instead of 592 for a dense layer doing the same job, and the ten don't grow when the picture gets bigger. Two, and this is the better one, it only has to learn 'this is an edge' once. A dense layer would have to learn it separately for every position, and it would need training pictures with an edge in each place."

**The second reason is the one that matters** and it is the one students miss. A student who gives only the count has half the answer; push with *"and what does the dense layer have to learn sixteen times?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say what flattening loses. Computes a convolution cell only with the teacher's hand on the page. Confuses the picture's size with the feature map's. |
| **2 — Emerging** | Counts the dense parameters but not the conv ones, or vice versa. Gets one convolution cell right and loses track by cell four. Uses "kernel" and "feature map" interchangeably. |
| **3 — Secure** | Computes 1,040 and 10 unaided and says which tool is better and why. Fills in all sixteen cells correctly and checks them against `nn.Conv2d`. Explains weight sharing in words. Designs a horizontal-edge kernel and predicts that it stays silent on a vertical edge. **This is the target.** |
| **4 — Strong** | Predicts the feature map's size by counting the window positions, before running anything. Diagnoses a uniformly-offset feature map as a bias and a sign-flipped one as a mirrored kernel, without help. Reads `(4, 1, 3, 3)` out loud as four filters, one channel, three by three. |
| **5 — Exceptional** | Predicts all 36 cells of the cross's feature map and explains the 18s and 9s as partial cancellation. Notices that the response size depends on the picture's contrast rather than the edge's sharpness, and connects it back to Week 4's standardising. Says that the shuffled model's 0.9704 is a measurement limit rather than a result. Derives the output-size rule from counting and recognises it as a general statement. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, three pages, and the first one produces a picture I am going to put on the wall.
>
> **First, page 24.4 — four pictures, three kernels, twelve feature maps, one figure.** Build four 8 by 8 pictures in numpy: the bar, the stripe, the cross, and a noisy one. Write three kernels by hand: a vertical-edge finder, a horizontal-edge finder, and an averager. Apply all three to all four, and save the whole lot as **one labelled figure** — four rows, four columns, the original picture and then its three feature maps. Then **one sentence per kernel** saying what that kernel found. Not what it is called. What it found.
>
> **Second, page 24.5 — the parameter-count comparison, written up.** Dense against conv, on the 8 by 8 picture and again on a 64 by 64 one. **Both numbers, the division, and a one-line verdict.** The verdict is the marked part and it has to be a sentence, not a number.
>
> **Third, page 24.6 — six short questions.** Ten minutes. One of them asks you to work out a convolution cell by hand and I want all nine products written down."

**Workbook pages:** 24.1, 24.2, 24.3 in class · **24.4, 24.5, 24.6** at home.

**Expected time:** 30 min on the four pictures, three kernels and the figure · 15 min on the counts and the verdict · 15 min on the six questions. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the first is the real one. **One — do the twelve maps have labels, and does each sentence say what the kernel *found* rather than what it is called?** *"The vertical-edge kernel finds vertical edges"* scores nothing; *"it lit up in a bright stripe down the middle of the bar picture and went completely flat on the noisy one, so it is reporting where brightness steps sideways"* is full marks. **Two — is the verdict on page 24.5 a sentence with a reason in it?** *"1040 against 10, so conv is smaller"* is half; *"1,040 against 10, a hundred and four times fewer, and the small one is also the one that knows which pixels are neighbours"* is full. **Three — on the by-hand cell, are all nine products written?** The answer is worth nothing on its own — nine products, a row sum, and a total is the answer.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 24.1 — Kernel on Graph Paper (in class)

*The 6 × 6 picture and the 3 × 3 kernel are printed on the page. Fill in all sixteen cells.*

**The picture:**

```
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
 10  10  10   2   2   2
```

**The kernel:**

```
  1   0  −1
  1   0  −1
  1   0  −1
```

**The answer, all sixteen cells:**

```
   0   24   24    0
   0   24   24    0
   0   24   24    0
   0   24   24    0
```

**The arithmetic, one window per distinct case:**

| window, each row | one row | three rows | cell |
|---|---|---|---|
| 10, 10, 10 | (1×10) + (0×10) + (−1×10) = 0 | 0 + 0 + 0 | **0** |
| 10, 10, 2 | (1×10) + (0×10) + (−1×2) = 8 | 8 + 8 + 8 | **24** |
| 10, 2, 2 | (1×10) + (0×2) + (−1×2) = 8 | 8 + 8 + 8 | **24** |
| 2, 2, 2 | (1×2) + (0×2) + (−1×2) = 0 | 0 + 0 + 0 | **0** |

**And why sixteen cells:** the window can start at column 0, 1, 2 or 3 — `6 − 3 + 1 = 4` — and the same going down. **4 × 4 = 16.**

**Confirmed against `nn.Conv2d`:**

```text
by hand, sixteen windows, sixteen sums:
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]

the picture as a tensor: (1, 1, 6, 6)
conv.weight shape      : (1, 1, 3, 3)
learnable numbers      : 10
the output as a tensor : (1, 1, 4, 4)

from nn.Conv2d:
[[ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]
 [ 0. 24. 24.  0.]]

all sixteen cells agree? True
```

**Marking notes.** Three failure shapes and their causes: **all rows different** means the window slid down instead of right; **8s or 16s instead of 24s** means a kernel row was skipped; **−24s throughout** means the kernel is mirrored, which is not an arithmetic error at all and should be marked correct with a note about polarity. **Praise loudly** any student who worked out one row and copied it down having noticed that every row of the picture is identical — that is the reasoning that makes convolutions efficient.

### Page 24.2 — The parameter-count comparison (in class)

*Both layers, on the same 8 × 8 picture, and then on a 64 × 64 one.*

| Layer | weights | biases | total |
|---|---|---|---|
| `nn.Linear(64, 16)` | 16 × 64 = **1024** | **16** | **1040** |
| `nn.Conv2d(1, 1, kernel_size=3)` | 3 × 3 = **9** | **1** | **10** |
| `nn.Conv2d(1, 4, kernel_size=3)` | 4 × 1 × 3 × 3 = **36** | **4** | **40** |
| `nn.Linear(4096, 256)` on 64 × 64 | 256 × 4096 = **1048576** | **256** | **1048832** |
| `nn.Conv2d(1, 4, kernel_size=3)` on 64 × 64 | **36** | **4** | **40** |

```
1040 ÷ 10 = 104
1048832 ÷ 40 = 26220.8
```

**Confirmed against PyTorch:**

```text
nn.Linear(64, 16)                  total: 1040
nn.Conv2d(1, 1, kernel_size=3)     total: 10
nn.Conv2d(1, 4, kernel_size=3)     total: 40
nn.Linear(4096, 256) needs         1048832
nn.Conv2d(1, 4, kernel_size=3)     40
```

**The point to make out loud:** rows 3 and 5 are **the same layer** and **the same 40 numbers**, on a picture with sixty-four times as many pixels. The dense layer's count grew by a factor of a thousand. **A convolution's count does not depend on the size of the picture.**

### Page 24.3 — Predict the shape (in pen, before running)

| Question | Answer |
|---|---|
| What shape does `nn.Conv2d` need its input in? | `(batch, channels, height, width)` — **four numbers, always** |
| One greyscale 6 × 6 picture, as a tensor for `nn.Conv2d`? | **(1, 1, 6, 6)** — one picture, one channel |
| `torch.from_numpy(img).float()` on a 6 × 6 numpy grid gives what shape? | **(6, 6)** |
| …and after two `.unsqueeze(0)` calls? | **(1, 1, 6, 6)** |
| What shape is `conv.weight` for `nn.Conv2d(1, 1, kernel_size=3)`? | **(1, 1, 3, 3)** — nine numbers |
| What shape is `conv.weight` for `nn.Conv2d(1, 4, kernel_size=3)`? | **(4, 1, 3, 3)** — thirty-six numbers |
| `nn.Conv2d(1, 1, kernel_size=3)` on a `(1, 1, 8, 8)` input gives what? | **(1, 1, 6, 6)** — because 8 − 3 + 1 = 6 |
| `nn.Conv2d(1, 3, kernel_size=3)` on a `(1, 1, 8, 8)` input gives what? | **(1, 3, 6, 6)** — three filters, three feature maps |

**The last two are the ones to talk about.** The **second** number of the output shape is the number of filters, and the **last two** come from counting window positions. A student who has those two facts separately can predict any conv shape in this course.

### Page 24.4 — Four pictures, three kernels, one figure

**The complete file:**

```python
"""kernels.py - four pictures, three kernels, twelve feature maps in one figure."""
import numpy as np
import torch
import torch.nn as nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- the four pictures, written out with numpy ---
bar = np.zeros((8, 8)); bar[:, 0:4] = 10.0; bar[:, 4:8] = 2.0
stripe = np.zeros((8, 8)); stripe[:, 4:] = 8.0
cross = np.zeros((8, 8)); cross[3:5, :] = 9.0; cross[:, 3:5] = 9.0
noisy = np.round(np.random.default_rng(0).uniform(0, 9, size=(8, 8)), 0)
pictures = [("bar", bar), ("stripe", stripe), ("cross", cross), ("noisy", noisy)]

# --- the three kernels, written out by hand ---
vertical = np.array([[1., 0., -1.], [1., 0., -1.], [1., 0., -1.]])
horizontal = np.array([[1., 1., 1.], [0., 0., 0.], [-1., -1., -1.]])
average = np.full((3, 3), 1.0 / 9.0)
kernels = [("vertical edge", vertical), ("horizontal edge", horizontal), ("average", average)]

conv = nn.Conv2d(1, 3, kernel_size=3)
conv.weight.data = torch.from_numpy(np.stack([vertical, horizontal, average])).float().reshape(3, 1, 3, 3)
conv.bias.data = torch.zeros(3)
print("conv.weight shape:", tuple(conv.weight.shape))
print("learnable numbers:", sum(p.numel() for p in conv.parameters()))

fig, axes = plt.subplots(4, 4, figsize=(9, 9))
for r, (pname, picture) in enumerate(pictures):
    t = torch.from_numpy(picture).float().unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        maps = conv(t)[0].numpy()
    print("\n%-7s -> feature maps %s" % (pname, tuple(maps.shape)))
    axes[r][0].imshow(picture, cmap="gray")
    axes[r][0].set_title("picture: " + pname)
    for c, (kname, _) in enumerate(kernels):
        m = maps[c]
        print("   %-16s biggest %+7.2f   smallest %+7.2f" % (kname, m.max(), m.min()))
        axes[r][c + 1].imshow(m, cmap="gray")
        axes[r][c + 1].set_title(kname)
    for ax in axes[r]:
        ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()
plt.savefig("feature_maps.png", dpi=110)
print("\nwrote feature_maps.png")

print("\nthe vertical kernel on the cross, all 36 cells:")
t = torch.from_numpy(cross).float().unsqueeze(0).unsqueeze(0)
with torch.no_grad():
    print(conv(t)[0][0].numpy())
```

**The real output:**

```text
conv.weight shape: (3, 1, 3, 3)
learnable numbers: 30

bar     -> feature maps (3, 6, 6)
   vertical edge    biggest  +24.00   smallest   +0.00
   horizontal edge  biggest   +0.00   smallest   +0.00
   average          biggest  +10.00   smallest   +2.00

stripe  -> feature maps (3, 6, 6)
   vertical edge    biggest   +0.00   smallest  -24.00
   horizontal edge  biggest   +0.00   smallest   +0.00
   average          biggest   +8.00   smallest   +0.00

cross   -> feature maps (3, 6, 6)
   vertical edge    biggest  +27.00   smallest  -27.00
   horizontal edge  biggest  +27.00   smallest  -27.00
   average          biggest   +8.00   smallest   +0.00

noisy   -> feature maps (3, 6, 6)
   vertical edge    biggest  +12.00   smallest  -10.00
   horizontal edge  biggest  +14.00   smallest  -13.00
   average          biggest   +6.00   smallest   +3.11

wrote feature_maps.png

the vertical kernel on the cross, all 36 cells:
[[  0. -27. -27.  27.  27.   0.]
 [  0. -18. -18.  18.  18.   0.]
 [  0.  -9.  -9.   9.   9.   0.]
 [  0.  -9.  -9.   9.   9.   0.]
 [  0. -18. -18.  18.  18.   0.]
 [  0. -27. -27.  27.  27.   0.]]
```

![Three kernels, three different things found](../figures/fig-w24-4-three-kernels-three-feature-maps.svg)
*Figure 24.4 — Three kernels, three different things found. Vertical and horizontal both reach ±27 on the cross; the averager reaches +8 and finds no edges at all.*

**The three sentences, at full marks:**

> **Vertical edge.** "It lit up as a bright stripe down the middle of the bar picture, reaching +24, and stayed at exactly 0 on the flat left and right thirds. On the stripe picture it reached −24 instead of +24, because that edge goes dark-to-bright rather than bright-to-dark. So it is reporting **where brightness steps sideways, and which way.**"
>
> **Horizontal edge.** "It was completely silent on the bar and the stripe — biggest +0.00, smallest +0.00 — because neither of them has a top-to-bottom step anywhere. On the cross it reached +27 and −27, on the top and bottom edges of the horizontal bar. So it reports **where brightness steps up-and-down**, and it is the vertical kernel turned a quarter turn."
>
> **Average.** "It found no edges at all. On the bar its answers run from +2 to +10, which are just the picture's own two brightness levels, and on the noisy picture it squashed everything into +3.11 to +6.00 — a much narrower band than the original 0 to 9. So it is **smoothing, not detecting**: it replaces each pixel with the average of its nine neighbours."

**Marking notes.** The mark is for **what it found, from the evidence on the page**. A sentence that only restates the kernel's name scores nothing. The two best observations, both worth calling out if you see them: **the horizontal kernel's exact zeros on the bar** (a detector that stays silent is doing its job), and **the averager narrowing the noisy picture's range** from 0–9 to 3.11–6.00, which is what "blur" means in numbers.

### Page 24.5 — The counts, and the verdict

**The two comparisons:**

```
8 × 8 picture
   nn.Linear(64, 16)                16 × 64 + 16   =   1,040
   nn.Conv2d(1, 1, kernel_size=3)    3 × 3  +  1   =      10
   1040 ÷ 10 = 104 times fewer

64 × 64 picture
   nn.Linear(4096, 256)            256 × 4096 + 256 = 1,048,832
   nn.Conv2d(1, 4, kernel_size=3)   4 × 3 × 3 +  4  =        40
   1,048,832 ÷ 40 = 26,220.8 times fewer
```

**The verdict, at full marks:**

> "On the 8 × 8 picture the dense layer needs 1,040 learnable numbers and the convolution needs 10 — a hundred and four times fewer — and the convolution is *also* the one that knows which pixels are neighbours, so it is smaller and better rather than smaller and worse. And the gap grows with the picture: on a 64 × 64 image the dense layer needs over a million while the convolution still needs 40, because a convolution's count depends on the size of its kernel and not on the size of the picture."

**Marking notes.** *"Conv is smaller"* is half a mark. The verdict has to contain **a reason**, and the best ones contain two: the count, and the fact that the cheaper layer is the one with the right assumption baked in. **A student who spots that rows 3 and 5 are the same 40 numbers has understood weight sharing**, and that is worth saying on the page.

### Page 24.6 — Six short questions

**1. What does flattening an image throw away, and how do you know it matters?**

Which pixels are next to which. **The evidence:** shuffle the 64 columns of `load_digits` — one shuffle, applied identically to every picture — retrain the same network, and the accuracy does not fall: **0.9704 shuffled against 0.9667 unshuffled**, a difference of two digits out of 540. A person cannot read the shuffled pictures at all. **A model that scores the same on both was never using the arrangement.**

**2. A 3 × 3 kernel slides over a 10 × 10 picture, one step at a time, no padding. How big is the feature map, and how did you get it?**

**8 × 8.** The window can start at column 0 through column 7 — that is `10 − 3 + 1 = 8` places — and the same going down. 8 × 8 = 64 cells.

**3. `nn.Conv2d(1, 6, kernel_size=3)`. How many learnable numbers, and what shape is `weight`?**

`weight` is **(6, 1, 3, 3)** — six filters, one input channel, three by three — so 6 × 1 × 3 × 3 = **54 weights**, plus **6 biases**, one per filter. **60 numbers.**

**4. Work out this cell by hand. Write all nine products.**

```
window            kernel
 9   9   0        1   1   1
 9   9   0        0   0   0
 0   0   0       −1  −1  −1
```

```
row 0:  (1 × 9) + (1 × 9) + (1 × 0)      =   9 + 9 + 0   =   18
row 1:  (0 × 9) + (0 × 9) + (0 × 0)      =   0 + 0 + 0   =    0
row 2:  (−1 × 0) + (−1 × 0) + (−1 × 0)   =   0 + 0 + 0   =    0
```

```
18 + 0 + 0 = 18
```

**18.** And the nine products in full: 9, 9, 0, 0, 0, 0, 0, 0, 0.

*(This is a real window from the cross picture, and 18 is a real cell of its horizontal-edge feature map.)*

**5. Explain weight sharing to somebody who has not done this lesson, in two sentences — one about cost and one about learning.**

**Cost:** the same nine numbers are used at every position, so the layer has 10 learnable numbers instead of one set per position — and that 10 does not change when the picture gets bigger. **Learning:** it only has to learn "this is an edge" once, whereas a dense layer would have to learn it separately for every position and would need training pictures with an edge in each place.

**6. Your feature map comes out as `[[0.0882, 24.0882], [0.0882, 24.0882]]` and you expected `[[0, 24], [0, 24]]`. What is wrong, and how do you know it is that and not an arithmetic mistake?**

The **bias** was never zeroed, so PyTorch's random starting value — 0.088204 here — is being added to every cell. **How you know:** the error is *exactly the same amount in every cell*. An arithmetic mistake would be wrong differently in different cells. Fix with `conv.bias.data = torch.zeros(1)`.

### Answers to every question posed in the lesson

**Hook — "predict the accuracy on the shuffled pictures."** Most of the room will guess between 20% and 60%. The real answer is **0.9704**, against **0.9667** unshuffled — a two-digit difference on 540 rows, so a tie.

**Hook — "which one did better?"** The **shuffled** one, by 0.0037. Which is noise, and the point: **the model cannot tell a picture from confetti.**

**Hook — "why can't it tell?"** Because every weight in `nn.Linear` joins one input slot to one output unit, and nothing anywhere in the layer records which slots are neighbours. Ask which box is above box 3 in a row of numbered boxes: there is no answer.

**Concept A — the dense count.** 16 × 64 = 1024 weights, plus 16 biases, = **1040**.

**Concept A — "how many times smaller?"** 1040 ÷ 10 = **104**.

**Concept B — "add up the top row of products."** 10 + 0 − 10 = **0**. **"And the whole thing?"** **0** — the window is completely flat.

**Concept B — "what does each row of the window read now?"** `10, 10, 2`. And `(1 × 10) + (0 × 10) + (−1 × 2) = 8` per row, three rows, **24**.

**Concept B — the third window, columns 2 to 4.** Each row reads `10, 2, 2`. `(1 × 10) + (0 × 2) + (−1 × 2) = 8`, three rows, **24**.

**Concept B — the fourth window, columns 3 to 5.** Each row reads `2, 2, 2`. `2 − 2 = 0`, **0**.

**Concept B — "how many cells are in the answer grid?"** **16.** Four starting columns (`6 − 3 + 1 = 4`) and four starting rows.

**Concept C — "how many times did I change the kernel?"** **Never.** That is weight sharing.

**Live-code step 1 — "what shape does the conv weight print?"** Most will say `(3, 3)`. It prints **`(1, 1, 3, 3)`** — one filter, one input channel, three high, three wide — and it is still nine weights.

**Live-code step 3 — "it wants three or four numbers and we gave it two. What are the other two?"** How many **pictures** (the batch) and how many **channels** each picture has. Our one greyscale picture is `(1, 1, 6, 6)`.

**Live-code step 4 — "what has been added to every cell, and where from?"** **0.088204**, in all sixteen cells, and it came from the **bias** — which we never set, so PyTorch's random starting value is still in there. The tell that it is not a rounding error: it is identical sixteen times.

**Activity part 3 — "run the horizontal kernel on the bar. What will it say?"** **Nothing — zero everywhere.** Real output: `horizontal edge  biggest +0.00   smallest +0.00`. A detector that is silent on the wrong thing is a working detector.

**Harder variation 1 — "why are there negatives in the cross's feature map, and why do the numbers get smaller towards the middle?"** Negatives because the vertical bar of the cross has **two** edges: its left edge is a dark-to-bright step and its right edge is bright-to-dark, and the kernel reports them with opposite signs. Smaller in the middle because rows 2, 3 and 4 of the picture sit across the cross's horizontal bar, where the window is filled with 9s on both sides, so the pluses and the minuses partly cancel — 27 becomes 18, then 9.

**Harder variation 3 — "why is the output smaller if the kernel does nothing?"** Because the *window* still cannot hang off the edge, regardless of what is in it. The identity kernel returns the middle 4 × 4 of a 6 × 6 picture unchanged and loses the outer ring. **The fix is padding, and it is Week 25.**

**Harder variation 4 — "how many numbers would a dense layer need for the 64 × 64 row?"** To make 3,844 outputs from 4,096 pixels: `3844 × 4096 + 3844 = 15,748,868`. **Fifteen and a half million against ten.**

**Harder variation 5 — "24 on the bar and 27 on the cross. Is the cross's edge sharper?"** **No.** The cross is 9s and 0s, so each row contributes `9 − 0 = 9` and three rows give 27. The bar is 10s and 2s, so `10 − 2 = 8` per row and 24. **The response depends on the picture's contrast, not on how edge-like the edge is** — which is why real inputs get standardised, exactly as in Week 4.

**Flying 6 — "have I proved shuffling helps?"** No. 0.0037 of 540 rows is **two digits**, and a different seed reverses the order. What has been proved is that **this measurement cannot tell the two models apart**, which is a smaller and much more useful claim. Week 11's lesson about small denominators, in a new costume.

---

## 🔮 Next Week Preview

Next week is the one piece of maths in this run of the course, and it is one line long: `(n + 2p − k) ÷ s + 1`, rounded down. The student will not meet it as a formula first. They will count window positions on an 8 × 8 grid by hand — with the window jumping two at a time instead of one, and with a ring of zeros glued round the edge so the corner pixels stop being cheated — and only once they have counted three different cases will the line get written down, beside the counts it reproduces. Then `nn.MaxPool2d(2)`, which halves the height and width and has no learnable numbers at all, and `nn.Flatten()`, which is where the shape error everybody meets actually happens: get the number after the flatten wrong by one and `nn.Linear` prints both numbers at you.

**To prep early:** three things. **One — keep the squared paper out**, because Week 25 counts window positions on an 8 × 8 grid three times with different strides and paddings, and it is the same activity shape as this week. **Two — do the twelve output-size calculations from the workbook yourself tonight**, and print the shape beside each; the whole lesson turns on the teacher being able to say "yes, and now print it" with confidence. **Three — keep `load_digits` in mind and reshape it once tonight**, so you have seen `digits.data.reshape(-1, 1, 8, 8)` produce `(1797, 1, 8, 8)` with your own eyes. Week 25 uses it, Week 26 trains a CNN on it, and the reshape from a flat 64 back into a picture is the moment the two halves of this term join up.
