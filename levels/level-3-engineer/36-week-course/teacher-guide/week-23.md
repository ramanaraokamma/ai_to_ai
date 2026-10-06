# Week 23 — Same Brain, Real Framework

[⬅ Week 22](week-22.md) · [Course Home](../README.md) · [Week 24 ➡](week-24.md) · [Student Guide](../student-guide/week-23.md) · [Workbook](../workbook/week-23.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — three builds, one artifact, and the Clean Room Test with torch |
| **Big idea** | A model you cannot reload in a fresh process is not finished. **The weights go in a file, the architecture goes in a module both scripts import, and `predict.py` has no training code in it at all.** |
| **New vocabulary** | `Dataset` · `DataLoader` · batch · epoch versus step · `state_dict` · `model.eval()` · inference |
| **New maths** | **None.** One division rounded up — 1257 ÷ 32 — done three ways and made to agree. |
| **New syntax** | `class Net(nn.Module)` with `super().__init__()` and `forward(self, x)` · `TensorDataset(X, y)` + `DataLoader(ds, batch_size=32, shuffle=True)` · `model.eval()` / `model.train()` · `torch.save(model.state_dict(), p)` + `model.load_state_dict(torch.load(p))` |
| **Dataset** | `make_moons(random_state=0)` for the identity proof, then **`load_digits()`** — 1,797 handwritten digits, 8×8 greyscale, 64 columns, shipped inside scikit-learn. **Nothing downloads. No internet needed. No torchvision.** |
| **Materials** | Printed workbook pages 23.1–23.6 · the **PARAMETER COUNT** wall sheet from Week 22, still up · a printed **CLEAN ROOM** checklist with seven tick-boxes, one per student · the Bug Log · Week 22's `layers.py` on disk |
| **Tech needed** | Laptop with Python 3, numpy, scikit-learn, matplotlib, **torch**. **No new installs.** `load_digits` is part of scikit-learn and loads instantly offline. |
| **Prep time** | 30 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `same_brain.py` **instant**. `train_digits.py` trains 15 epochs, 600 optimizer steps, and saves the weights in **0.2 seconds**. `predict_digits.py` **instant**. Nothing this week takes longer than a breath. |

> **⚠️ Watch out:** the temptation in this lab is to let `predict.py` import from `train_digits.py`, because that is one line shorter and it works. **Do not allow it.** The whole discipline of the week is the dependency direction: both scripts import the *architecture* from a third small file, and `predict.py` knows nothing about training. The grep at the end of the lesson is not a formality — it is the deliverable.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build a network as an `nn.Module` subclass** and show it has the same parameters as the `nn.Sequential` version — same four shapes, same 65 numbers, byte-identical weights, identical output on the same input.
2. **Load data with `TensorDataset` and `DataLoader`**, and compute how many optimizer steps one epoch contains **three different ways** — by dividing, by counting the loop, by asking the DataLoader — and make all three agree.
3. **Train a 64 → 64 → 10 MLP on `load_digits` past 95% test accuracy in under 20 seconds** and report the split alongside the number.
4. **Save the weights with `torch.save`, reload them in a fresh process, and ship a `predict.py` that imports no training code** — proven with a grep and with `model.eval()` giving the same answer five times running.

Observable evidence: two printed parameter lists with `identical: True` underneath; three printed numbers all reading 40; the line `FINAL: test accuracy 0.9667 on 540 held-out digits`; a `predict_digits.py` that classifies three digits in a fresh terminal; and a pasted before-and-after of the `model.eval()` experiment.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There is one division, rounded up, and you will do it three times on purpose. What is new is *engineering*: four ideas about how a trained model gets out of the room it was trained in. Give this section twenty minutes; it is the longest prep of the term and it is worth it, because everything in Weeks 26, 27, 34 and 35 sits on it.

### 1. Why write a class at all, when `nn.Sequential` works?

Last week's model was a list of parts:

```python
model = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
```

That is perfect for a straight line of parts. It stops being enough the moment you want anything that is not a straight line — a value used twice, a branch, a shape printed halfway through. So PyTorch offers a second way: you write a small class with two halves.

> **`nn.Module`** — the base class for anything with learnable numbers in it. You inherit from it and fill in two methods.

> **`__init__`** — "declare the parts you will need". Runs once, when the model is built.
> **`forward`** — "say how one batch flows through those parts". Runs every time you call the model.

Here is the same network as a class:

```python
class MoonNet(nn.Module):
    def __init__(self):
        super().__init__()                      # never forget this line
        self.fc1 = nn.Linear(2, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))
```

**Line by line, for somebody who has never written a class.**

- `class MoonNet(nn.Module):` — "I am defining a new kind of thing called `MoonNet`, and it is a kind of `nn.Module`." The bracket means "inherits from"; the student has seen `class` in Level 2 only in passing, so say it out loud: *a class is a template. `MoonNet()` builds one.*
- `def __init__(self):` — the setup method. Python runs it when you write `MoonNet()`. `self` is "the particular model being built"; every method gets it as its first argument and you never pass it in yourself.
- `super().__init__()` — **"do `nn.Module`'s own setup first."** This is the line that gets forgotten, and forgetting it does not produce a subtle bug: it produces `AttributeError: cannot assign module before Module.__init__() call`, immediately, on the next line. That message is in the Clinic and it is worth being pleased about — PyTorch catches this one for you.
- `self.fc1 = nn.Linear(2, 16)` — build a layer and hang it on the model under the name `fc1`. The name is yours to choose; `fc` is short for "fully connected", which is the older name for `nn.Linear`. **Because you assigned it to `self`, PyTorch now knows about its weights** and will hand them to the optimizer.
- `def forward(self, x):` — the method that does the work. `x` is one batch.
- `return self.fc2(torch.relu(self.fc1(x)))` — read it inside out: push `x` through `fc1`, squash with ReLU, push through `fc2`, hand the result back.

**And the one rule about calling it: write `model(x)`, never `model.forward(x)`.** They look equivalent and they are not — `model(x)` runs some bookkeeping first that some layers depend on. Say it once, firmly, and if you see `.forward(` on a screen, fix it.

![The two halves of a network class](../figures/fig-w23-1-nn-module-class-anatomy.svg)
*Figure 23.1 — The two halves of a network class. Declare the parts on the left; say how a batch flows on the right; and 4160 + 650 = 4810 learnable numbers.*

**The identity proof, and why it is the first thing you do.** Set the seed, build one of each, and compare:

```text
Sequential:
   0.weight   (16, 2)
   0.bias     (16,)
   2.weight   (1, 16)
   2.bias     (1,)
Module subclass:
   fc1.weight (16, 2)
   fc1.bias   (16,)
   fc2.weight (1, 16)
   fc2.bias   (1,)

Sequential parameters     : 65
Module subclass parameters: 65
weights byte-identical    : True
same output on the same input: True
```

**Only the names changed.** `nn.Sequential` names its children by *position* — 0, 1, 2 — and the class names them by the *attribute* you chose — `fc1`, `fc2`. Same shapes, same 65 numbers, same answers.

And the names matter more than they look, which is §4's problem: a `state_dict` saved from one will **not** load into the other, because the keys are different. That is the second-nastiest error of the week and it is in the Clinic.

### 2. Batches, epochs and steps — and the division you must do three ways

Until this week every training run pushed *all* the training rows through at once. That is fine for 300 moons. It is not how anything real is trained, and it is not what the student will meet in Week 26.

> **`TensorDataset(X, y)`** — pairs up a table of features with its answers so that "row 7" means one `(features, answer)` pair.
> **`DataLoader(ds, batch_size=32, shuffle=True)`** — hands you the rows in shuffled groups of 32, one group at a time, in a `for` loop.
> **batch** — one group of rows, pushed through together.
> **epoch** — one full lap of the training data.
> **step** (or iteration) — one nudge of the weights. **One batch is one step.**

Here is the arithmetic that matters, on this week's real numbers. 1,257 training digits, 32 at a time:

```text
1257 ÷ 32 = 39.28…                 →  round UP  →  40 batches
39 full batches × 32 rows = 1248
1257 − 1248 = 9                    →  the last batch has 9 rows
1248 + 9 = 1257                    ✅ every row used once, none twice
```

**Round up, never down.** Rounding down would throw away the last 9 digits, and the check `1248 + 9 = 1257` is what catches that.

![A DataLoader cuts the rows into batches](../figures/fig-w23-2-dataloader-cutting-rows-into-batches.svg)
*Figure 23.2 — A DataLoader cuts the rows into batches. 39 × 32 = 1248, and 1257 − 1248 = 9 rows in the last one.*

Then:

```text
15 epochs × 40 steps = 600 optimizer steps
```

**Why insist on three separate ways of getting 40?** Because the three ways fail differently, and a student who has only one of them cannot tell a wrong answer from a right one. Dividing checks your understanding. Counting checks your loop. Asking the DataLoader checks that the object you built is the object you think you built. If the three disagree, exactly one thing is wrong and you now know which.

![One epoch, three ways to count the steps](../figures/fig-w23-3-epoch-versus-step-arithmetic.svg)
*Figure 23.3 — One epoch, three ways to count the steps. Divide, count, ask — all three say 40, and 15 × 40 = 600.*

**And the reason it matters beyond today:** *"I trained for 15 epochs"* tells you almost nothing. Fifteen epochs at batch size 32 is 600 weight updates; fifteen epochs at batch size 512 is 45 (`ceil(1257 ÷ 512) = 3` batches, times 15). **More than thirteen times fewer.** Two people comparing "15 epochs" are comparing nothing at all unless they also say the batch size. Make the student say both, out loud, whenever they report a run.

**What `shuffle=True` actually does.** It reshuffles before every lap. Here it is on ten rows, four at a time, so you can see the whole thing:

```text
epoch 0:  [6, 7, 1, 4] [2, 0, 9, 8] [3, 5]
epoch 1:  [2, 4, 7, 0] [8, 9, 5, 3] [6, 1]
epoch 2:  [7, 4, 5, 1] [9, 3, 8, 2] [0, 6]

batches per epoch: 3  (10 rows, 4 at a time)
```

Three batches every epoch — 4, 4 and 2 — and every epoch the same ten rows land in different company. **Shuffle the training loader. Never shuffle the test loader**, because you want the same order every time so the measurement repeats.

### 3. `load_digits` — the image dataset of this level

```python
from sklearn.datasets import load_digits
digits = load_digits()
```

1,797 handwritten digits, each an 8 × 8 grid of brightnesses from 0 to 16, already flattened into 64 columns. `digits.data` is `(1797, 64)`; `digits.target` is 1,797 whole numbers from 0 to 9.

**It ships inside scikit-learn.** It does not download. It loads in a few milliseconds. You will use it in Weeks 24, 25, 26 and 27 as well, so it is worth loading it once tonight and printing a digit as text so you know what you are looking at:

```text
   .=@@@...
   .@@@@-..
   .*=-@-..
   ...=@-..
   ...@@...
   ..:@@.-.
   ..@@@@@.
   .-@@@@@.
   row 1528   true 2   guessed 2   correct
```

That is a two. Squint and you will see it. **Show that on the screen in the hook** — a student who has seen the actual picture will care about the accuracy number in a way they will not otherwise.

**Two preparation details, and both matter.**

`X = digits.data / 16.0` — divide by 16 so every number sits between 0 and 1. The same standardising instinct from Week 4, done the simplest possible way because we happen to know the maximum.

The answers need one more step. Our loss is still Week 22's `BCEWithLogitsLoss`, which compares a grid of scores against a grid of answers of the same shape. The network has 10 outputs, so it produces a `(1257, 10)` grid — and the answers have to be a `(1257, 10)` grid too. So each answer becomes a row of ten numbers with a single 1 in it:

```text
the digit 6  →  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
```

`np.eye(10)[y]` does exactly that: `np.eye(10)` is a 10 × 10 grid with 1s down its diagonal, and indexing it by the answers picks out the right row for each.

> **🧑‍🏫 If a student asks "isn't there a loss made for ten classes?"** — yes, and it is `nn.CrossEntropyLoss`, and it is **Week 26**. It takes one column of whole numbers instead of ten columns of 0s and 1s, which is tidier. Say the name, say the week, and do not sketch it. Today's ten-column trick works, reaches 96.67%, and uses only the loss they already understand.

And to read the answer back out we take the biggest of the ten scores, using the same `argmax` idea they have had since Week 12:

```python
scores = model(X_te_t).numpy()
pred = scores.argmax(axis=1)
```

`axis=1` means "across each row" — for every digit, which of its ten scores is largest.

### 4. The artifact: `state_dict`, `torch.save`, and the module both scripts import

This is the part of the week that is really about engineering, and it is the part that will matter in the capstone.

> **`state_dict()`** — a plain dictionary of *name → block of numbers*. It is the model's **weights**, not the model's **code**.

For our digits network it holds exactly four entries:

```text
   fc1.weight (64, 64)
   fc1.bias   (64,)
   fc2.weight (10, 64)
   fc2.bias   (10,)
```

```text
4096 + 64 + 640 + 10 = 4810 numbers in the file
```

```python
torch.save(model.state_dict(), "digits_mlp.pt")            # out
model.load_state_dict(torch.load("digits_mlp.pt"))         # back in
```

![The weights go out to a file and come back](../figures/fig-w23-4-state-dict-out-to-a-file-and-back.svg)
*Figure 23.4 — The weights go out to a file and come back. 4096 + 64 + 640 + 10 = 4810 numbers, and the biggest difference after reloading is 0.000000.*

🍕 **The analogy that works.** A `state_dict` is a set of tuning-peg positions for a guitar. Useless without a guitar of the same shape; exactly what you need if you already have one.

**So you must build the same architecture first, and this is the whole reason the third file exists.** If `train_digits.py` declares the class and `predict_digits.py` declares it again, the two declarations will drift — somebody changes 64 to 128 in one file and not the other — and the load will fail, or worse, quietly load into a differently-shaped thing. So:

```text
digits_net.py        holds the class.  Imported by both.
train_digits.py      imports it, trains, saves digits_mlp.pt
predict_digits.py    imports it, loads digits_mlp.pt, predicts.  No training code.
```

**The arrows only ever point one way: both scripts point at `digits_net.py`, and `predict_digits.py` never points at `train_digits.py`.** Draw that on the board. It is the single most transferable idea in the week.

**And when it goes wrong, the error is very good.** Load a subclass's weights into an `nn.Sequential`:

```text
RuntimeError: Error(s) in loading state_dict for Sequential:
	Missing key(s) in state_dict: "0.weight", "0.bias", "2.weight", "2.bias".
	Unexpected key(s) in state_dict: "fc1.weight", "fc1.bias", "fc2.weight", "fc2.bias".
```

Read it out loud: *"I wanted these four names and I found those four names."* Nothing about that is mysterious once you know that `state_dict` keys are names.

Load them into a class with the right names and the wrong widths:

```text
RuntimeError: Error(s) in loading state_dict for Net:
	size mismatch for fc1.weight: copying a param with shape torch.Size([64, 64]) from checkpoint, the shape in current model is torch.Size([32, 64]).
```

Even better: it prints both shapes. **A file of numbers cannot tell you the architecture, so PyTorch checks it against the one you built and complains precisely.**

### 5. `model.eval()` — the line whose absence is silent

Last week's code already had `model.eval()` and `model.train()` in it and you were told to say one sentence and move on. This is the week.

> **`model.eval()`** — switch the model into *measuring* mode. Dropout stops dropping.
> **`model.train()`** — switch it back into *learning* mode. Dropout resumes.
> **inference** — using a trained model to answer a question. No learning, no gradients, no dropout.

Our digits network has `nn.Dropout(0.2)` in it. Here is the same handwritten 9, put through five times, before and after:

```text
row 37, true label 9

model.train()  - dropout is ON
   try 1: guess 5   score for 9 = -1.7783
   try 2: guess 9   score for 9 = +0.6095
   try 3: guess 3   score for 9 = -3.0162
   try 4: guess 9   score for 9 = -1.8427
   try 5: guess 5   score for 9 = -0.8994

model.eval()   - dropout is OFF
   try 1: guess 9   score for 9 = -1.6703
   try 2: guess 9   score for 9 = -1.6703
   try 3: guess 9   score for 9 = -1.6703
   try 4: guess 9   score for 9 = -1.6703
   try 5: guess 9   score for 9 = -1.6703
```

**Read the top block again.** The same image, the same weights, five goes: 5, 9, 3, 9, 5. **Three different answers to one question.** And no error, no warning, nothing on the screen to tell you anything is wrong.

The bottom block: 9, 9, 9, 9, 9, and the score is `−1.6703` every single time to four decimal places.

**That is the whole argument for `model.eval()` and it is why we do it as an experiment rather than as a rule.** A student who has seen a model give three answers to one question will never forget the line.

⚠️ **And a second line that does a different job.** `with torch.no_grad():` tells PyTorch to stop recording the receipt from Week 20 — it makes measuring faster and uses less memory. It does **not** turn off dropout. `model.eval()` does **not** turn off recording. **You need both, and they are not substitutes.** Put both in every measuring block, every time, and say why once:

```python
model.eval()
with torch.no_grad():
    scores = model(X_te_t)
```

### 6. How deep to go, and where to stop

**Go this far:** the class written and proved identical to the `nn.Sequential`; the DataLoader arithmetic done three ways; the digits MLP trained past 95% with the split reported; the weights saved, reloaded in a fresh process, and `predict.py` shipped and grepped; the `model.eval()` experiment run and pasted.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `nn.CrossEntropyLoss`, `logits.argmax(dim=1)` | **Week 26.** Today's ten-column `BCEWithLogitsLoss` reaches 96.67% and uses only Week 22's loss. Name the week and move on. |
| Writing your own `Dataset` subclass with `__len__` and `__getitem__` | Not needed in this level. `TensorDataset` covers everything we do. If a student wants to, let them — it is two methods — but it is not on the objective list. |
| `nn.Conv2d`, images as 2-D | **Weeks 24–27.** Today the digit is a flat row of 64 numbers, and next week the student finds out what that costs. |
| Coding early stopping with `patience` | **Week 34.** Today the model just trains for 15 epochs. |
| `drop_last=True`, `num_workers`, samplers | Not in this level. If the 9-row last batch causes trouble later, we will meet it then. |
| GPUs, `.to(device)`, `cuda`, `mps` | Not in this level as a lesson. Everything here runs on a laptop CPU in under a second. If a student asks, say: *"a GPU would be slower on 1,257 rows — moving the data costs more than the arithmetic saves."* |
| Pickling the whole model with `torch.save(model, ...)` | Mention it exists and that we do not do it: **it saves code as well as numbers, which means loading a file can run somebody else's program.** a `state_dict` does not, provided you load it with `weights_only=True`. |

The sentence to keep in your head: **today the model becomes a file, and the file is the deliverable.**

---

### 7. 🧭 The Growing Map — the tile closes today

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. This week is the **last** week in the gold tile, so the two minutes are a closing-off
rather than an orientation.

![The Level 3 pipeline in Week 23: the numpy and PyTorch tile closes with the same brain reloaded in a fresh process](../figures/fig-w23-0-where-this-fits.svg)

*Figure 23.0 — Week 23's version. Fifth and final week in the gold `numpy brain · PyTorch` tile; next week
the box underneath it opens. The ↻ on stage three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "what closed it?"** The box is the same gold tile it has
   been for five weeks. What closed it is the thing in their hands: **the Clean Room checklist with seven
   ticks**, a `.pt` file on disk, and a `predict_digits.py` that survived the grep. *"Five weeks ago a
   network was maths on a whiteboard. Now it is a file you can email."*
2. **Count the five weeks out loud, pointing at the one gold box.** Week 19 the brain by hand, Week 20
   tensors, Week 21 the five-line loop, Week 22 layers and the overfitting curve, Week 23 the artifact.
   *"One box. Five weeks. That is what a box on this map costs."* This is the moment the map stops being
   decoration and starts being a measure of effort.
3. **Then point at `images · CNNs` and say what is coming.** Still dashed today, gold next week. *"Next
   week we stop pretending a picture is a row of sixty-four numbers."* If you want one sentence to plant
   it: the digits they just classified at 96% were **flattened**, and that is about to be treated as a
   mistake.

> **🧑‍🏫 Why this is worth two minutes.** This is a lab week, and lab weeks end with everybody's head
> inside their own terminal. Two minutes on the map is what turns three files on a laptop into "we
> finished something that took five weeks" — and it is the frame you will want again in Week 34, when the
> same ritual comes back with their own project attached.

**One thing to notice, so you can answer if asked.** The threads are `model` and `impact`, and `impact` is
lit for only the fourth time in the level. It is lit because of one line: `FINAL: test accuracy 0.9667 on
540 held-out digits`. That line is written for a reader, not for the author — which is the same reason
Week 3's model card lit `impact`. If a student asks why saving a file counts as impact, that is the
answer: a saved model is the first thing in this course that somebody else can use without you in the room.

---

## 🧰 Prep Checklist

This section lists everything to set up before the lesson, including the complete runnable files.

### 30 minutes the night before

- [ ] **Print the CLEAN ROOM checklist**, one per student. Seven boxes:

```text
[ ] digits_net.py holds the class, and nothing else
[ ] train_digits.py imports it
[ ] predict_digits.py imports it
[ ] predict_digits.py does NOT import train_digits.py
[ ] predict_digits.py has no optimizer, no loss, no backward, no DataLoader
[ ] predict_digits.py calls model.eval()
[ ] run it twice on the same digit and get the same answer
```

- [ ] **Load `load_digits` yourself and print a digit as text.** Two minutes, and it changes how you talk about the dataset:

```python
from sklearn.datasets import load_digits
digits = load_digits()
print(digits.data.shape, digits.target.shape, digits.data.max())
for r in range(8):
    print("".join(".:-=+*#@"[min(int(v), 7)] for v in digits.data[1528].reshape(8, 8)[r]))
print("this is a", digits.target[1528])
```

```text
(1797, 64) (1797,) 16.0
.=@@@...
.@@@@-..
.*=-@-..
...=@-..
...@@...
..:@@.-.
..@@@@@.
.-@@@@@.
this is a 2
```

- [ ] **Create the three files.** They are the lesson. Type all three now and run them in order.

**File 1 — `digits_net.py`. The architecture, in one place.**

```python
"""digits_net.py - the architecture, in one place, imported by both scripts."""
import torch.nn as nn


class DigitNet(nn.Module):
    def __init__(self):
        super().__init__()                 # never forget this line
        self.fc1 = nn.Linear(64, 64)
        self.act = nn.ReLU()
        self.drop = nn.Dropout(0.2)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        h = self.act(self.fc1(x))
        h = self.drop(h)
        return self.fc2(h)
```

**File 2 — `train_digits.py`.**

```python
"""train_digits.py - train the digits MLP and save its weights."""
import time
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from digits_net import DigitNet

torch.manual_seed(0)

digits = load_digits()
X = digits.data / 16.0
y = digits.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.30,
                                          stratify=y, random_state=0)
print("train rows %d   test rows %d   features %d" % (len(X_tr), len(X_te), X.shape[1]))

X_tr_t = torch.from_numpy(X_tr).float()
X_te_t = torch.from_numpy(X_te).float()
Y_tr_t = torch.from_numpy(np.eye(10)[y_tr]).float()
print("X_tr_t", tuple(X_tr_t.shape), "  Y_tr_t", tuple(Y_tr_t.shape))

train_ds = TensorDataset(X_tr_t, Y_tr_t)
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
print("rows in the dataset :", len(train_ds))
print("batches per epoch   :", len(train_loader))

model = DigitNet()
print("learnable numbers   :", sum(p.numel() for p in model.parameters()))

loss_fn = nn.BCEWithLogitsLoss()
opt = torch.optim.Adam(model.parameters(), lr=0.005)

t0 = time.time()
steps = 0
for epoch in range(15):
    model.train()
    running = 0.0
    for xb, yb in train_loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
        running += loss.item()
        steps += 1
    model.eval()
    with torch.no_grad():
        scores = model(X_te_t).numpy()
    acc = (scores.argmax(axis=1) == y_te).mean()
    print("epoch %2d  steps %3d  train loss %.4f  test acc %.4f"
          % (epoch, steps, running / len(train_loader), acc))

print("\nseconds: %.1f" % (time.time() - t0))
print("optimizer steps in total:", steps)
print("FINAL: test accuracy %.4f on %d held-out digits" % (acc, len(X_te)))

torch.save(model.state_dict(), "digits_mlp.pt")
print("saved digits_mlp.pt")
for name, tensor in torch.load("digits_mlp.pt").items():
    print("   %-10s %s" % (name, tuple(tensor.shape)))
```

Run `python3 train_digits.py`. You must see **exactly** this:

```text
train rows 1257   test rows 540   features 64
X_tr_t (1257, 64)   Y_tr_t (1257, 10)
rows in the dataset : 1257
batches per epoch   : 40
learnable numbers   : 4810
epoch  0  steps  40  train loss 0.3707  test acc 0.6833
epoch  1  steps  80  train loss 0.2386  test acc 0.8241
epoch  2  steps 120  train loss 0.1633  test acc 0.8796
epoch  3  steps 160  train loss 0.1204  test acc 0.8944
epoch  4  steps 200  train loss 0.0949  test acc 0.9352
epoch  5  steps 240  train loss 0.0811  test acc 0.9519
epoch  6  steps 280  train loss 0.0713  test acc 0.9463
epoch  7  steps 320  train loss 0.0609  test acc 0.9556
epoch  8  steps 360  train loss 0.0559  test acc 0.9519
epoch  9  steps 400  train loss 0.0492  test acc 0.9593
epoch 10  steps 440  train loss 0.0473  test acc 0.9648
epoch 11  steps 480  train loss 0.0444  test acc 0.9648
epoch 12  steps 520  train loss 0.0419  test acc 0.9611
epoch 13  steps 560  train loss 0.0383  test acc 0.9704
epoch 14  steps 600  train loss 0.0356  test acc 0.9667

seconds: 0.2
optimizer steps in total: 600
FINAL: test accuracy 0.9667 on 540 held-out digits
saved digits_mlp.pt
   fc1.weight (64, 64)
   fc1.bias   (64,)
   fc2.weight (10, 64)
   fc2.bias   (10,)
```

**Expected runtime: 0.2 seconds of training**, plus about a second of imports. **The `seconds:` line is the only one that will differ on your machine** — it is a stopwatch, not a result. Every other line must match exactly. If your test accuracy is not 0.9667, a seed is missing: `torch.manual_seed(0)` at the top and `random_state=0` in `train_test_split`.

**File 3 — `predict_digits.py`. This is the deliverable.**

```python
"""predict_digits.py - classify three digits. No training code lives here."""
import numpy as np
import torch
from sklearn.datasets import load_digits

from digits_net import DigitNet

model = DigitNet()
model.load_state_dict(torch.load("digits_mlp.pt"))
model.eval()                      # dropout OFF - critical
print("loaded digits_mlp.pt, dropout is off")

digits = load_digits()
rng = np.random.default_rng(0)
picks = rng.integers(0, len(digits.data), size=3)
print("picked rows:", picks.tolist())

for i in picks:
    row = digits.data[i] / 16.0
    x = torch.from_numpy(row).float().reshape(1, 64)
    with torch.no_grad():
        scores = model(x)
    guess = int(scores.numpy().argmax(axis=1)[0])
    print()
    for r in range(8):
        print("   " + "".join(".:-=+*#@"[min(int(v), 7)] for v in digits.data[i].reshape(8, 8)[r]))
    print("   row %d   true %d   guessed %d   %s"
          % (i, digits.target[i], guess, "correct" if guess == digits.target[i] else "WRONG"))
```

Run `python3 predict_digits.py`. You must see **exactly** this:

```text
loaded digits_mlp.pt, dropout is off
picked rows: [1528, 1144, 918]

   .=@@@...
   .@@@@-..
   .*=-@-..
   ...=@-..
   ...@@...
   ..:@@.-.
   ..@@@@@.
   .-@@@@@.
   row 1528   true 2   guessed 2   correct

   ..@@@@-.
   .@@@@@=.
   .@@@....
   .@@@@...
   .@@@@+..
   ...:@*..
   ..-@@:..
   ..@@#...
   row 1144   true 5   guessed 5   correct

   ..@@@:..
   ..@=@+..
   ...*@-..
   ..-@@@..
   ....=@-.
   .+#..@@.
   .#@:*@=.
   ..@@@*..
   row 918   true 3   guessed 3   correct
```

- [ ] **Run the grep yourself**, so you can run it in front of them:

```bash
grep -E "optimizer|loss_fn|backward|\.step\(\)|DataLoader|train_test_split" predict_digits.py ; echo "exit=$?"
```

```text
exit=1
```

**`exit=1` means grep found nothing, which is the pass.** Say that out loud — an exit code of 1 looking like a failure and meaning success is exactly the sort of thing that derails a lesson.

- [ ] **Run `same_brain.py` and `steps.py`.** Both are in the Answer Key with their real output. Both are instant.
- [ ] **Break it on purpose, twice.** These are the two deliberate mistakes in the live-code:
  1. Delete `super().__init__()`. You get `AttributeError: cannot assign module before Module.__init__() call` on the very next line.
  2. Load `digits_mlp.pt` into an `nn.Sequential(nn.Linear(64,64), nn.ReLU(), nn.Linear(64,10))`. You get the `Missing key(s)` / `Unexpected key(s)` error in full.
- [ ] **Print workbook pages 23.1–23.6.**
- [ ] **Leave the PARAMETER COUNT wall sheet up** and put a fifth row on it: `64 → 64 → 10`. The `by hand` column already says 4810 from last week's activity.

### 5 minutes on the day

- [ ] Editor open, terminal ready. All three files **deleted or renamed** — they type them.
- [ ] Wall sheet up with the fifth row.
- [ ] CLEAN ROOM checklists handed out face down.
- [ ] Workbook 23.1 out. **The two shape lists get predicted in pen before anything runs.**
- [ ] Bug Log out.
- [ ] **One terminal window you can close dramatically.** The Clean Room Test needs a visible "everything is gone" moment.

### Fallback if the laptops fail

**Two of the four objectives are arithmetic and paperwork, so this week's paper version is stronger than you would expect.**

1. **The identity proof on paper.** Write the two parameter lists on the board — `0.weight (16, 2)` … and `fc1.weight (16, 2)` … — and have them match the four pairs and total both to 65. **Objective 1, complete.**
2. **Steps three ways, four times.** Give four `(rows, batch_size)` pairs and have them do each one three ways: divide and round up, count the full batches plus the leftover, and state what `len(loader)` will print. The four answers are in the Answer Key. **Objective 2, complete, and this is the better version** — on paper they cannot let the computer do the division for them.
3. **The dependency arrows.** Three boxes on the board — `digits_net.py`, `train_digits.py`, `predict_digits.py` — and they draw the arrows. Then one question: *"which arrow must not exist?"* **Objective 4's discipline, complete.**
4. **The `model.eval()` experiment, read rather than run.** Give them the printed before-and-after block from §5 and two questions: *"how many different answers did it give to the same picture?"* (three: 5, 9, 3) and *"which block would you ship?"* **Objective 4's other half, complete.**
5. **The digit as text on paper.** Print the 8 × 8 grid of numbers for row 1528 and have them shade in every cell above 8. A two appears. It takes four minutes and it is the best possible introduction to Week 24.

| If this fails | Do this instead |
|---|---|
| `AttributeError: cannot assign module before Module.__init__() call` | `super().__init__()` is missing, or below the first `self.fc1 = ...`. It must be the first line of `__init__`. |
| `batches per epoch` prints 39 | `batch_size` is 32 and the rows are 1,248, not 1,257 — check the split is `test_size=0.30`. Or the loader has `drop_last=True`, which throws the last 9 rows away. |
| Test accuracy is not 0.9667 | A seed. `torch.manual_seed(0)` **above** `DigitNet()`, `random_state=0` in `train_test_split`. |
| `RuntimeError: Error(s) in loading state_dict` with `Missing key(s)` | The class being loaded into is not the class that was saved from. Compare the names in the message. This is deliberate mistake two. |
| `predict_digits.py` gives a different answer every run | `model.eval()` is missing. Deliberate, if you are doing the experiment; a bug otherwise. |
| `ModuleNotFoundError: No module named 'digits_net'` | The three files are not in the same folder, or the terminal is in a different folder. `pwd` and `ls`. |
| `load_digits` seems to hang | It does not download; it cannot hang. Something else is being imported. Check the top of the file for a stray `torchvision`. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Close the Terminal | 6 | 6 | Last week's model, deleted in front of them |
| 🧠 Concept — The Class, the Batch, the File | 12 | 18 | Two halves of a class; the division three ways; the three-file diagram |
| 💻 Live-Code Together — `same_brain.py` then `steps.py` | 20 | 38 | The identity proof and the arithmetic. **Two deliberate mistakes.** |
| 🎲 Their Turn — Build It and Ship It | 26 | 64 | Three files, 96.67%, and the Clean Room Test |
| 🔑 Wrap & Assign | 6 | 70 | Three checks, the takeaway, homework |

> **📌 Why this is not the standard 7 / 18 / 18 / 20 / 7 shape.** Week 23 is a **lab**: there is no new maths, so the concept segment shrinks, and the students have three files to build and then ship, so "their turn" grows. The total is still 70 minutes and the five segments are still the five segments.

---

### 🪝 Hook — Close the Terminal (6 minutes)

**Do this:** Open last week's `overfit.py`, run it, and let the class watch the loss numbers scroll past.

**Say this:**

> "There it is again. Four thousand four hundred and seventeen learnable numbers, trained for fifteen hundred epochs. That is a working model. It knows something about moons.
>
> Watch."

**Do this:** Close the terminal window. Deliberately, slowly, and with the mouse so everybody sees the click.

**Say this:**

> "Gone. All four thousand four hundred and seventeen of them. Every epoch of that training, deleted, because those numbers only ever existed inside the program that was making them.
>
> That has been true of every model you have built since Week 20. **You have never once kept one.**"

**Ask this:** "Last term, in Week 3, we solved this exact problem for a scikit-learn pipeline. What did we do?"

*Hoped-for answer:* saved it to a file with `joblib.dump`, then loaded it in a fresh script.

*If they do not remember:* prompt with *"what was the Clean Room Test?"* — close everything, open a script that does no training, and make a prediction.

**Say this:**

> "Right. Week 3's rule, and it has not changed: **the artifact is the deliverable.** A model that only exists in the terminal you trained it in is a demo, not a model.
>
> So today we do it with torch. And we do it on something that will actually make you want to keep the model."

**Do this:** Run the digit-printer from the Prep Checklist and put this on the screen:

```text
.=@@@...
.@@@@-..
.*=-@-..
...=@-..
...@@...
..:@@.-.
..@@@@@.
.-@@@@@.
this is a 2
```

**Ask this:** "What is that?"

*Hoped-for answer:* a two.

> "A two. Somebody wrote that by hand, and it is an 8 by 8 grid of brightnesses, 64 numbers, and there are 1,797 of them in a dataset that ships inside scikit-learn. Nothing downloads. It loads in the time it takes you to blink.
>
> **By the end of this lesson you will have a file on disk that reads handwriting**, and a second program that opens that file, has no training code in it at all, and tells you what the digit is. That second program is the thing you would give somebody."

**Do this:** Draw the three boxes on the board and leave them up all lesson:

```text
       digits_net.py
        (the class)
         ↗        ↖
train_digits.py   predict_digits.py
   (trains,        (loads, predicts,
    saves)          no training code)
```

**Ask this:** "There is one arrow that must not exist on that diagram. Which one?"

*Hoped-for answer:* an arrow from `predict_digits.py` to `train_digits.py`.

*If they cannot see it:* ask *"if the prediction script imports the training script, what happens when you run it?"* — it runs the training. Every time. On somebody else's laptop.

---

### 🧠 Concept — The Class, the Batch, the File (12 minutes)

#### Part A — the two halves of a class (5 minutes)

**Do this:** Draw two boxes on the board, side by side, exactly as in Figure 23.1.

```text
   __init__                        forward
   "declare the parts"             "say how a batch flows"
   runs once                       runs every call

   fc1   64 in → 64 out            (32, 64)  batch in
   ReLU                            (32, 64)  after fc1 and ReLU
   dropout 0.2                     (32, 64)  after dropout
   fc2   64 in → 10 out            (32, 10)  ten scores each
```

**Say this:**

> "A class is a template. You write it once and then build as many as you like from it. And a PyTorch network class has exactly two halves, and it helps enormously to keep them separate in your head.
>
> The left half is a **shopping list**. 'I will need a 64-to-64 layer, a squash, a dropout, and a 64-to-10 layer.' It says nothing about the order.
>
> The right half is the **route**. 'A batch comes in, goes through fc1, gets squashed, gets dropped, goes through fc2, comes out.' It builds nothing; it only routes.
>
> And there is one line at the top of the left half that you must never leave out: `super().__init__()`. It means 'do the parent class's setup first'. Leave it out and PyTorch stops you immediately, which is the friendliest possible outcome."

**Ask this:** "In the right-hand box, the shape is (32, 64) three times and then (32, 10). Where does the 32 come from, and why does it never change?"

*Hoped-for answer:* 32 is the batch size — 32 digits at a time — and layers only change the *second* number.

*If they say "the features":* point at the fourth line, where 64 became 10 but 32 did not, and ask again.

#### Part B — the division, three ways (4 minutes)

**Do this:** Write on the board:

```text
1257 training digits.  32 at a time.  How many batches?
```

**Ask this:** "Do the division."

*Expected:* 39.28.

**Ask this:** "So — 39 or 40?"

*Hoped-for answer:* 40, because the leftovers still have to go somewhere.

*If they say 39:* ask *"what happens to the last nine digits?"*

**Do this:** Write the whole check out, and make them do the subtraction:

```text
39 × 32 = 1248
1257 − 1248 = 9
1248 + 9 = 1257        ✅  so 40 batches: thirty-nine of 32 and one of 9
```

**Say this:**

> "Forty. And I am going to make you get that number three separate ways in a minute, which sounds like a waste of time and is not.
>
> **Divide.** That checks whether *you* understand it.
> **Count the loop.** That checks whether your *loop* is doing what you think.
> **Ask the DataLoader.** That checks whether the *object* you built is the object you meant.
>
> Three ways, three different things being tested. If they disagree, exactly one thing is broken and you now know which."

**Do this:** Write the second number and box it:

```text
15 epochs × 40 steps = 600 optimizer steps
```

**Say this:**

> "And this is the one that matters when you tell somebody about a run. **An epoch is a lap. A step is one nudge of the weights.** Fifteen laps at 32 rows a batch is six hundred nudges. Fifteen laps at 512 rows a batch would be forty-five. More than thirteen times fewer.
>
> So *'I trained for 15 epochs'* is not a fact about anything until you also say the batch size. Say both. Always."

#### Part C — the file, and what is in it (3 minutes)

**Say this:**

> "Last thing before we build. When you save a model, what actually goes in the file?"

**Do this:** Write the four lines on the board:

```text
fc1.weight  (64, 64)   4096
fc1.bias    (64,)        64
fc2.weight  (10, 64)    640
fc2.bias    (10,)        10
                      ------
                        4810
```

**Say this:**

> "Four names and four blocks of numbers. That is all. **It is called a `state_dict` and it holds the model's numbers, not the model's code.**
>
> Which is exactly why the third file exists. The file cannot tell you it was a 64-to-64-to-10 network — so you have to build that shape yourself first and then pour the numbers in. If the shape you build is wrong, PyTorch tells you, in detail, with both shapes printed. If both scripts declare the shape separately, one day they will disagree, and it will be a Tuesday afternoon in Week 34.
>
> **One file holds the class. Both scripts import it.** That is today's discipline."

🍕 **Say this analogy out loud; it lands every time:**

> "A `state_dict` is the peg positions on a guitar. Useless on its own. Exactly what you want if you already have a guitar of the same shape."

---

### 💻 Live-Code Together — `same_brain.py` then `steps.py` (20 minutes)

**You never touch their keyboard.**

**Step 1 (5 min) — write the class, with 🐞 DELIBERATE MISTAKE ONE.**

> **Say this:** "Let's write last week's moons network as a class. I'll leave out one line on purpose and see if PyTorch notices."

Type this — with no `super().__init__()`:

```python
import torch
import torch.nn as nn


class MoonNet(nn.Module):
    def __init__(self):
        self.fc1 = nn.Linear(2, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


MoonNet()
```

Run it. Real output:

```text
Traceback (most recent call last):
  File "same_brain.py", line 13, in <module>
    MoonNet()
  File "same_brain.py", line 7, in __init__
    self.fc1 = nn.Linear(2, 16)
  File ".../torch/nn/modules/module.py", line 1716, in __setattr__
    raise AttributeError(
AttributeError: cannot assign module before Module.__init__() call
```

**Ask this:** "Read the last line. What is it telling you to do, and where?"

*Hoped-for answer:* call `Module.__init__()` before assigning anything — so, at the top of our `__init__`.

> **Say this:** "That is one of the best error messages in PyTorch. It does not just say 'error'. It names the thing you skipped and tells you it has to happen *before* what you did.
>
> `super().__init__()` — 'super' means the class I inherited from, `nn.Module`. Run its setup first, then hang my own layers on. **It is the first line of every `__init__` you will ever write.**"

Fix it live by adding one line.

**Do this:** Bug Log, sixty seconds. **This is a friendly error and it is worth saying so** — the student's log is filling up with hostile ones.

**Step 2 (7 min) — the identity proof.**

```python
torch.manual_seed(0)
seq = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
torch.manual_seed(0)
cls = MoonNet()

print("Sequential:")
for name, p in seq.named_parameters():
    print("   %-10s %s" % (name, tuple(p.shape)))
print("Module subclass:")
for name, p in cls.named_parameters():
    print("   %-10s %s" % (name, tuple(p.shape)))

print()
print("Sequential parameters     :", sum(p.numel() for p in seq.parameters()))
print("Module subclass parameters:", sum(p.numel() for p in cls.parameters()))
print("weights byte-identical    :",
      torch.equal(seq[0].weight, cls.fc1.weight)
      and torch.equal(seq[0].bias, cls.fc1.bias)
      and torch.equal(seq[2].weight, cls.fc2.weight)
      and torch.equal(seq[2].bias, cls.fc2.bias))

x = torch.tensor([[1.0, 2.0], [-0.5, 0.5]])
print("same output on the same input:", torch.equal(seq(x), cls(x)))
print("that output:", seq(x).reshape(-1).tolist())
```

**Ask before running:** "Two lists of four shapes are about to print. What will be the same and what will be different?"

*Hoped-for answer:* the shapes will be the same; the names will differ.

Run it:

```text
Sequential:
   0.weight   (16, 2)
   0.bias     (16,)
   2.weight   (1, 16)
   2.bias     (1,)
Module subclass:
   fc1.weight (16, 2)
   fc1.bias   (16,)
   fc2.weight (1, 16)
   fc2.bias   (1,)

Sequential parameters     : 65
Module subclass parameters: 65
weights byte-identical    : True
same output on the same input: True
that output: [0.059556588530540466, 0.0902349054813385]
```

> **Say this:** "Sixty-five and sixty-five. `identical: True`. Same output on the same input, down to the last decimal place.
>
> **They are the same model.** Not similar — the same. The only difference is that `nn.Sequential` names its children by position, 0 and 2, and the class names them by the attribute name I chose, `fc1` and `fc2`.
>
> And why is the second one `2` and not `1`? Same as last week: the ReLU is part 1 and has no numbers, so it never appears — but it keeps its slot.
>
> Hold on to those names. In fifteen minutes they are going to be the reason a load fails."

**Step 3 (4 min) — the arithmetic, three ways.**

```python
import math
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)
X = torch.zeros(1257, 64)
Y = torch.zeros(1257, 10)
loader = DataLoader(TensorDataset(X, Y), batch_size=32, shuffle=True)

print("way 1 - divide and round up:", math.ceil(1257 / 32))
print("        39 x 32 = %d, and %d - %d = %d left over" % (39 * 32, 1257, 39 * 32, 1257 - 39 * 32))

counted = 0
sizes = []
for xb, yb in loader:
    counted += 1
    sizes.append(xb.shape[0])
print("way 2 - count the loop      :", counted)
print("        first batch %d rows, last batch %d rows, all rows %d"
      % (sizes[0], sizes[-1], sum(sizes)))

print("way 3 - ask the DataLoader  :", len(loader))
print()
print("15 epochs x %d steps = %d optimizer steps" % (len(loader), 15 * len(loader)))
```

Run it:

```text
way 1 - divide and round up: 40
        39 x 32 = 1248, and 1257 - 1248 = 9 left over
way 2 - count the loop      : 40
        first batch 32 rows, last batch 9 rows, all rows 1257
way 3 - ask the DataLoader  : 40

15 epochs x 40 steps = 600 optimizer steps
```

> **Say this:** "Forty, forty, forty. And the middle line is the one I want you to notice: **first batch 32 rows, last batch 9 rows, all rows 1257.** Every row used exactly once. The last batch is smaller and that is completely normal.
>
> Six hundred steps. Write that down next to '15 epochs' every single time you report a run."

**Step 4 (4 min) — 🐞 DELIBERATE MISTAKE TWO: load into the wrong shape.**

> **Say this:** "Suppose I trained with the class and then, in the prediction script, I got lazy and used an `nn.Sequential` instead. Same shapes, right? 64 to 64 to 10."

```python
wrong = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 10))
wrong.load_state_dict(torch.load("digits_mlp.pt"))
```

Run it. Real output:

```text
RuntimeError: Error(s) in loading state_dict for Sequential:
	Missing key(s) in state_dict: "0.weight", "0.bias", "2.weight", "2.bias".
	Unexpected key(s) in state_dict: "fc1.weight", "fc1.bias", "fc2.weight", "fc2.bias".
```

**Ask this:** "It found four names and wanted four different names. Are the shapes wrong?"

*Hoped-for answer:* no — the shapes are fine, the *names* are wrong.

> **Say this:** "The shapes are perfect. 64 by 64 and 10 by 64, exactly right. **The names are wrong**, because a `state_dict` is a dictionary of names, and `nn.Sequential` calls its layers 0 and 2 while my class calls them fc1 and fc2.
>
> And this is the entire argument for putting the class in its own file that both scripts import. **You cannot get the names wrong if there is only one place the names are written.**"

Fix it live: `from digits_net import DigitNet`, then `DigitNet()`.

**Do this:** Bug Log. Make sure the words *"a state_dict is a dictionary of names"* are in it.

**Do this, if you have ninety seconds:** show the other one too, right names and wrong widths, because the message is even better:

```text
RuntimeError: Error(s) in loading state_dict for Net:
	size mismatch for fc1.weight: copying a param with shape torch.Size([64, 64]) from checkpoint, the shape in current model is torch.Size([32, 64]).
```

*"Both shapes printed. The file's, and yours. That is a message you can act on without thinking."*

---

### 🎲 Their Turn — Build It and Ship It (26 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: build the three files, train past 95% and report the split with the number, save the weights, then the Clean Room Test — close everything, run `predict_digits.py`, classify three digits, and tick all seven boxes on the checklist.

---

### 🔑 Wrap & Assign (6 minutes)

**Do this:** Have one student read out their `FINAL:` line. Write it on the board.

```text
FINAL: test accuracy 0.9667 on 540 held-out digits
```

**Say this:**

> "Read what is on that line, because the shape of the sentence matters as much as the number. **A score, and the pile it came from.** Not '96.67% accurate' — '96.67% on 540 held-out digits'. Somebody who reads the first one cannot tell whether you tested on your training data. Somebody who reads the second one can.
>
> Three things to take away.
>
> **One.** A class and a `Sequential` are the same model. Two halves: declare the parts, say how a batch flows. `super().__init__()` first, always.
>
> **Two.** An epoch is a lap and a step is a nudge. 1,257 rows at 32 a time is 40 steps, and you got that number three different ways and made them agree. Fifteen epochs is six hundred steps, and you say both.
>
> **Three, and this is the one.** Point at the board."

**Do this:** Point at the three-box diagram.

> "One file holds the class. Both scripts import it. **`predict_digits.py` contains no training code**, and you proved it with a grep that printed nothing at all.
>
> And `model.eval()` — one line, no error message if you forget it, and without it the same handwritten nine gets called a five, a nine, a three, a nine and a five. **Five goes, three answers.** That is what you are protecting against."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last thing, and it is next week's door.
>
> You just got 96.67% on handwriting with a model that thinks a digit is a flat row of 64 numbers in no particular order. Shuffle those 64 columns — the same shuffle for every image — and it would train to just about the same score (tried: 96.5% to 96.7%). It would never notice.
>
> Which means it is not looking at a picture. **Next week we find out what that costs, and what to use instead.**"

**Do this:** Hand out the homework and read part three out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: cannot assign module before Module.__init__() call` | "You hung a layer on a model that has not been set up yet." | `super().__init__()` missing from `__init__`, or written after the first `self.fc1 = ...`. | Make `super().__init__()` **the first line** of `__init__`. |
| `NotImplementedError: Module [Net] is missing the required "forward" function` | "You told me the parts but not the route." | `forward` not defined, or misspelled — `foward`, `Forward`, `forwards`. | Define `def forward(self, x):`. Spelling matters and there is no warning for a near-miss. |
| `RuntimeError: Error(s) in loading state_dict for Sequential:` `Missing key(s) ... "0.weight"` `Unexpected key(s) ... "fc1.weight"` | "The file's four names are not this model's four names." | Trained with a class and loaded into an `nn.Sequential`, or the layer attribute got renamed. | Build the **same class** the weights came from. Better: put the class in one file both scripts import. |
| `RuntimeError: ... size mismatch for fc1.weight: copying a param with shape torch.Size([64, 64]) ... the shape in current model is torch.Size([32, 64]).` | "Right names, wrong widths." | The class was edited after training — 64 changed to 32 in one file and not the other. | Read both shapes in the message; make the class match the file, or retrain. |
| `FileNotFoundError: [Errno 2] No such file or directory: 'digits_mlp.pt'` | "There is no saved model here." | `predict_digits.py` run before `train_digits.py`, or from a different folder. | Run the trainer first. Then `ls` and check you are in the folder the `.pt` file is in. |
| `AssertionError: Size mismatch between tensors` | "Your features and your answers have different numbers of rows." | `TensorDataset(X_tr_t, Y_te_t)` — a train/test mix-up in the names. | Print both shapes first. Row counts must match: `(1257, 64)` and `(1257, 10)`. |
| `TypeError: 'int' object is not callable` **from inside `dataset.py`** | A confusing message with a simple cause: you put numpy arrays into `TensorDataset`. | `TensorDataset(np.zeros((10, 64)), ...)` — numpy has `.size` as a number, torch has `.size()` as a method. | `torch.from_numpy(arr).float()` first. **`TensorDataset` takes tensors only.** |
| `numpy.exceptions.AxisError: axis 1 is out of bounds for array of dimension 1` | "You asked for the biggest in each row of something that has no rows." | One digit passed as a flat 64 instead of a `(1, 64)` batch, so the output is `(10,)` and `argmax(axis=1)` has no axis 1. | `.reshape(1, 64)` — **one row is still a batch, a batch of one.** |
| `ModuleNotFoundError: No module named 'digits_net'` | "There is no file called digits_net.py where I am looking." | The three files are in different folders, or the terminal is somewhere else. | `pwd`, `ls`. All three files live together. |
| **No error. `predict_digits.py` gives a different answer every run.** | Nothing crashed; the model is not repeatable. | `model.eval()` missing, so `nn.Dropout(0.2)` is still switching units off. | `model.eval()` immediately after `load_state_dict`. **Run it twice on the same digit as a test.** |
| **No error. `predict_digits.py` prints training output.** | Nothing crashed; the prediction script trained a model. | `import train_digits` at the top. Importing a script *runs* it. | Import from `digits_net`, never from `train_digits`. The grep catches this. |
| **No error. `batches per epoch` is 39, not 40.** | Nothing crashed; nine digits are being silently discarded. | `drop_last=True` on the DataLoader. | Remove it. And check `39 × 32 = 1248`, which is 9 short of 1257. |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three.

20. **"Read me the two lists of names."** For any `state_dict` error. `Missing key(s)` is what the model wanted; `Unexpected key(s)` is what the file had. A student who reads both lists out loud has diagnosed it.

21. **"Run it twice and tell me if you get the same answer."** For anything to do with inference. It is a two-second test and it catches the missing `model.eval()`, which has no error message of its own.

22. **"Do your three step counts agree?"** For any batching confusion. If divide says 40 and the loop says 39, the loop is wrong. If the loop says 40 and `len(loader)` says 39, the loader is wrong. **The disagreement tells you where to look**, which is the entire point of having three.

And the sentence for this week:

> **"A `state_dict` is a dictionary of names. Every loading error you will ever see is either a name that does not match or a shape that does not match, and the message tells you which."**

---

## 🎲 The Activity, In Full

This section gives the full setup, stages and variations for the lab, so you can run it without the minute-by-minute plan.

### Build It and Ship It

**What it is.** Three stages, and stage three is the one that counts. Build the three files. Train past 95% and report the split with the number. Then the Clean Room Test with torch: close everything, run `predict_digits.py`, and classify three digits picked at random.

### Setup

- Three empty files in one folder: `digits_net.py`, `train_digits.py`, `predict_digits.py`.
- The CLEAN ROOM checklist, one per student, face down until stage 3.
- Workbook page 23.3, which is the same checklist with room for the pasted evidence.
- The three-box diagram still on the board.

### Stage 1 — the three files (12 minutes)

> **"Three files, in this order. `digits_net.py` first, because the other two import it."**

`digits_net.py` is fourteen lines and they have all of it from the live-code. `train_digits.py` is the long one. `predict_digits.py` is short.

**Watch for exactly three failure modes.**

1. **`super().__init__()` missing.** They saw it fifteen minutes ago and they will still do it. The error is immediate and clear; let them read it.
2. **The class declared in `train_digits.py` as well.** *"How many files say what the shape of this network is?"* One. Delete the other.
3. **`from train_digits import DigitNet` in the prediction script.** This is the big one. It *works*, which is why it is dangerous. Ask: *"run it and tell me what it prints first."* It prints fifteen epochs of training.

**Sit on your hands for the first eight minutes.** The typing is not the objective, but the folder discipline is, and they have to feel the pull of the shortcut to learn not to take it.

### Stage 2 — train it and report it (7 minutes)

> **"Run the trainer. When it finishes, read me the last three lines."**

```text
optimizer steps in total: 600
FINAL: test accuracy 0.9667 on 540 held-out digits
saved digits_mlp.pt
```

Three questions, in this order:

1. **"How many steps, and how many epochs?"** *(600 steps, 15 epochs, batch size 32. All three numbers or the answer is incomplete.)*
2. **"Which rows was that 0.9667 measured on?"** *(The 540 held-out test rows, 30% of 1,797, stratified, `random_state=0`. Never trained on.)*
3. **"How many numbers went into the file?"** *(4096 + 64 + 640 + 10 = 4810.)*

**And a fourth, if somebody finishes early:** *"epoch 13 got 0.9704 and epoch 14 got 0.9667. Which do you report?"* The honest answer is 0.9667, because that is the model you saved — and the better answer is *"this is exactly what early stopping is for, and it is Week 34."*

### Stage 3 — the Clean Room Test (7 minutes)

This is the stage the lesson exists for. Run it like a ritual.

> **"Close the editor. Close every terminal. Everything you have in memory is now gone."**

Wait until every laptop is showing a desktop. **Do not let anyone keep a Python session open.**

> **"New terminal. One command: `python3 predict_digits.py`."**

```text
loaded digits_mlp.pt, dropout is off
picked rows: [1528, 1144, 918]

   .=@@@...
   .@@@@-..
   .*=-@-..
   ...=@-..
   ...@@...
   ..:@@.-.
   ..@@@@@.
   .-@@@@@.
   row 1528   true 2   guessed 2   correct
```

*(All three digits, in full, are in the Prep Checklist. Rows 1528, 1144 and 918; a 2, a 5 and a 3; all three correct.)*

> **"Now the grep. Type this exactly."**

```bash
grep -E "optimizer|loss_fn|backward|\.step\(\)|DataLoader|train_test_split" predict_digits.py ; echo "exit=$?"
```

```text
exit=1
```

**Say this:** *"Nothing printed. Exit code 1 means grep found none of those words. **That is the pass.** Your prediction script contains no training code at all."*

> **"Last thing: run `predict_digits.py` again. Same three digits, same three answers?"**

Yes — because `model.eval()` is there. Tick box seven.

### What "finished" looks like

- Three files in one folder plus `digits_mlp.pt`.
- All seven boxes on the CLEAN ROOM checklist ticked.
- The `FINAL:` line written out with **both** the score and the pile it came from.
- Two identical runs of `predict_digits.py`.
- The student can say, unprompted: *"the prediction script doesn't know how to train. It only knows how to load."*

### Variation — easier

**Give them `digits_net.py` and `train_digits.py` complete**, and have them write only `predict_digits.py` — which is fourteen lines and contains the entire discipline of the week.

Then cut the digit-drawing loop and print just the guess:

```python
import torch
from sklearn.datasets import load_digits
from digits_net import DigitNet

model = DigitNet()
model.load_state_dict(torch.load("digits_mlp.pt"))
model.eval()

digits = load_digits()
x = torch.from_numpy(digits.data[1528] / 16.0).float().reshape(1, 64)
with torch.no_grad():
    scores = model(x)
print("true", digits.target[1528], " guessed", int(scores.numpy().argmax(axis=1)[0]))
```

```text
true 2  guessed 2
```

**Eleven lines, and objective 4 is complete.** Then the grep, then run it twice. That is the week.

And skip the three-ways arithmetic down to one way: `print(len(train_loader))`, and check it against `1257 ÷ 32` rounded up on a calculator. **Two ways instead of three still teaches the habit.**

### Variation — harder

1. **Add a fourth way of counting the steps.** Sum the batch sizes as they go by and divide by nothing at all: `sum(sizes)` must be 1,257 and `len(sizes)` must be 40. Then answer: *"which of the four ways would catch `drop_last=True`?"* **The sum**, because it would come to 1,248, not 1,257. The loop and `len(loader)` would both say 39 and agree with each other (the division, rounded up, would still say 40 and flag a disagreement; a student who rounded down to 39 gets all three agreeing on the wrong answer).

2. **Break the artifact on purpose, three different ways**, and predict each error message before running it: rename `fc1` to `layer1` in `digits_net.py` after training; change 64 to 32; delete the `.pt` file. Three predictions, three real messages, one Bug Log entry each. **This is the most useful twenty minutes available to a strong student today.**

3. **Prove the reload is exact.** Load the same file into two fresh models and compare every score on all 1,797 digits:

```python
print("biggest difference over all %d rows and 10 scores: %.6f"
      % (len(X), float((sa - sb).abs().max())))
```

```text
biggest difference over all 1797 rows and 10 scores: 0.000000
numbers in the file: 4810
```

**Exactly 0.000000, not "close".** Ask why exact rather than approximate: because loading copies the numbers, it does not recompute anything. **This is the guarantee you need before you ship an artifact**, and it is the check Week 34 formalises.

4. **Find a digit the model gets wrong.** Loop over the 540 test rows, print the first five it misses as text art, and look at them. Several are genuinely ambiguous. Then the honest question: *"of the 18 it got wrong, how many would you have got wrong?"* That is a very good five minutes.

5. **Change the batch size to 512 and keep 15 epochs.** Predict the step count first: `ceil(1257 / 512) = 3`, so 45 steps instead of 600 — **more than thirteen times fewer**. Run it and watch the accuracy fall. Then the point: *"we did not train less; we trained the same number of epochs. Epochs are not the unit that matters."*

---

## ❓ Questions Students Ask This Week

**"Why not just use `nn.Sequential` forever? The class is more typing."**

For today's network, you could, and you would be fine. The class earns its keep the moment the route through the parts is not a straight line — a shape printed halfway through, a value used twice, a branch — and in Week 27 we do exactly that when we freeze some layers and not others.

But the reason to learn it *now* is the names. `nn.Sequential` calls its layers 0, 1, 2 by position, which means **inserting a layer renames everything after it and breaks every saved file.** A class calls them `fc1` and `fc2` by the name you chose, and adding `fc3` leaves the others alone. When you have a `.pt` file you care about, that difference stops being cosmetic.

**"Why does the file only hold numbers? Wouldn't it be easier if it held the whole model?"**

You can do that — `torch.save(model, "whole.pt")` — and PyTorch will let you, and it is a bad idea for one specific reason.

Saving the whole model saves *code*, and loading it therefore **runs** code. Which means a `.pt` file downloaded from the internet can do anything to your machine that a Python program can do. A `state_dict` is 4,810 numbers and four names; loaded with `torch.load(path, weights_only=True)` the worst it can do is fail to load. (A plain `torch.load` of an old-style `.pt` is still pickle underneath, so even a state_dict file should only come from someone you trust.)

The secondary reasons are practical: a numbers-only file is smaller, it survives a PyTorch upgrade, and it moves between machines without caring what your folders are called.

**"How does the model know which of the ten scores is the answer?"**

It doesn't, and that is a nice thing to be precise about. **The model produces ten numbers and has no opinion about them at all.** `argmax(axis=1)` is *our* rule: whichever of the ten is biggest, call that the answer.

Which means you can change the rule without retraining. You could say "only answer if the biggest score is above 2.0, otherwise say don't know" — and that is a three-way system with a "send it to a human" column, which is exactly the shape Week 8 predicted when somebody asked about a fifth cell.

**"Why 30% for the test set? Week 2 said 20%."**

Because 1,797 rows is not many, and 20% of it is 360 test digits, which is a shakier measurement than we would like. 30% gives us 540. The cost is 180 fewer training rows.

**There is no correct number and anybody who tells you 20% is a rule is repeating a habit.** What matters is that you chose it before you looked, you said which pile the score came from, and you did not touch the test rows while tuning. Those three things are the discipline; the percentage is a judgement call about how much measurement you can afford.

**"If dropout makes the answer random, why have it at all?"**

Dropout is only random **while training**, and that is the whole trick. During training, randomly switching units off stops the network relying on any one of them, which is Week 22's brake. During inference, `model.eval()` switches it off and the model becomes completely deterministic.

So the answer is: it is random exactly when randomness helps and switched off exactly when it would hurt. **The single line that separates those two worlds is `model.eval()`**, which is why forgetting it is so expensive and why we spent five minutes proving it with the same handwritten nine five times.

**"Our model gets 96.67%. What's the other 3.33%?"**

Eighteen digits out of 540. Go and look at them — it takes six lines and it is the best thing you can do with a spare five minutes.

Some of them are genuinely ambiguous: a 3 that could be an 8, a 9 written like a 4. Some are not, and those are the interesting ones, because the model is failing at something a person finds easy. **And a big part of why is next week's lesson:** this model sees a digit as 64 numbers in a row with no idea which ones are next to each other. It has no built-in idea that a 9 has a loop *above* a stroke: it can only learn, pixel position by pixel position, what each spot tends to look like for a 9, and it gets no help from the fact that neighbouring pixels belong together.

**"Should the architecture live in its own file, or should I just copy it into both scripts?"** *(Nobody fully agrees, and here is why.)*

**This is a live argument among working engineers and the two positions are both defensible.** Be straight about it.

**The position we teach, and the majority one:** one definition, imported by both. Duplication drifts. Somebody changes 64 to 128 in the trainer, forgets the predictor, and gets a size mismatch — or, on a bad day, a load that succeeds into the wrong shape. One source of truth cannot disagree with itself.

**The other position, and it is not silly:** an inference script that imports nothing from your project is easier to ship. Paste the class in, and `predict.py` plus `model.pt` is the entire delivery — no folder structure, no import path, nothing to install. Plenty of production systems do exactly this on purpose, and Module 6 of the reference modules writes `predict.py` that way for exactly this reason.

**And there is a third position which is the honest one:** the argument only exists because the file format threw the architecture away. Some formats do not — they store the shape alongside the numbers — and then there is nothing to keep in sync. **The disagreement is not really about good style; it is about working around a gap in the file format**, and reasonable people patch that gap at different ends.

What to tell a 14-year-old, out loud: **"one file, imported by both, and we grep to prove it. When you meet a project that pastes it instead, you'll know why they did and what it costs them."**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **`predict.py` imports the trainer** | It is one line shorter and it works | Catch it in stage 1: *"run it and tell me what it prints first."* Fifteen epochs of training. **Then the grep, in front of everybody.** This is the discipline of the week and it must be enforced once, publicly and cheerfully. |
| The class gets declared in two files | Copy-paste is faster than an import | One question: *"how many files say what shape this network is?"* Then delete one. Then break it on purpose so they see the size mismatch. |
| `super().__init__()` gets skipped and the error gets read as scary | It is an `AttributeError` in a stack of library frames | Read the **last line only**, out loud: *"cannot assign module before Module.__init__() call."* It names the missing thing and says where it goes. This is a friendly error and framing it that way matters. |
| Steps and epochs get used as if they were the same word | They are both "how long did it train" in everyday speech | Every time somebody says "epochs", ask *"and how many steps?"* Fifteen and six hundred. **Both numbers or neither.** |
| The last small batch looks like a bug | 39 batches of 32 and one of 9 feels wrong | Do the check on the board: `1248 + 9 = 1257`. **A smaller final batch means no row was thrown away**, which is the desirable outcome. |
| `model.eval()` gets taught as a rule instead of shown | It is one line and the rule is easy to state | **Run the experiment.** Five goes, three different answers to the same nine. A rule is forgotten; that printout is not. |
| The Clean Room Test gets skipped because time is short | It is at the end, and stage 1 always overruns | **Cut stage 1 instead** — hand out `digits_net.py` and `train_digits.py` complete. Stage 3 is the objective. A lab that ends without the artifact working in a fresh process has taught the wrong lesson. |
| `exit=1` from the grep is read as a failure | An exit code of 1 usually is | Say it before you run it: *"grep prints 1 when it finds nothing, and finding nothing is what we want."* |
| The score gets reported without the pile | "96.67%" is shorter than the whole sentence | Insist on the sentence, every time, all lesson: **a score and the pile it came from.** It is Week 2's rule and Week 34 marks it. |
| Somebody trains for 200 epochs to push past 98% | Very reasonable instinct, and it will overfit | Let them, it takes three seconds — but make them predict the two numbers first and write the prediction down. Then point at Week 22's Figure 22.4. |
| A student pastes the whole model with `torch.save(model, ...)` because it is fewer lines | It is fewer lines and it works | Let it work, then ask: *"if I emailed you that file, what would opening it be allowed to do to your laptop?"* Anything. That is the answer. |

---

## 🧭 Differentiation

This section gives ways to adjust the lesson for a student who is struggling, flying or disengaged.

### If the student is struggling

**Cut:** the identity proof down to the parameter *counts* only — 65 and 65 — and skip `torch.equal`. Objective 1's point is "same model, different names", and two matching totals plus two lists of names carries it.

**Cut:** the three-ways arithmetic to two ways: `len(loader)` and a calculator.

**Cut:** the text-art digit drawing in `predict_digits.py`. It is lovely and it is not an objective.

**Give them `digits_net.py` and `train_digits.py` complete**, and have them write only `predict_digits.py`. The eleven-line version is in the easier variation above and it delivers objective 4 whole.

**The copy-this-exactly scaffold for the class**, which is the part that stalls people:

```python
import torch
import torch.nn as nn


class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


torch.manual_seed(0)
net = TinyNet()
for name, p in net.named_parameters():
    print(name, tuple(p.shape), p.numel())
print("total:", sum(p.numel() for p in net.parameters()))
```

```text
fc1.weight (4, 2) 8
fc1.bias (4,) 4
fc2.weight (1, 4) 4
fc2.bias (1,) 1
total: 17
```

Then three questions and nothing else: **"which line declares the parts? which line says how a batch flows? and does 8 + 4 + 4 + 1 come to the total?"** `__init__`; `forward`; yes, 17.

**The version of the arithmetic with nothing hard in it.** One table, and only the division to do:

| rows | batch size | full batches | leftover | total batches |
|---|---|---|---|---|
| 100 | 10 | | | |
| 100 | 30 | | | |
| 1257 | 32 | | | |

*(10, 0, 10 · 3, 10, 4 · 39, 9, 40.)* Three divisions and three subtractions. **That is objective 2.**

**One thing you must not cut:** the Clean Room Test. If the whole lesson collapses to one sentence, make it *"a model you cannot open in a fresh terminal is not finished."*

### If the student is flying

None of these need syntax from a later week.

1. **Break the artifact three ways and predict each message** (harder variation 2). Rename a layer, change a width, delete the file. Three predictions, three real tracebacks. **The best use of this student's twenty minutes.**
2. **The fourth way of counting** (harder variation 1), ending in *"which way catches `drop_last=True`?"* — the sum, because 1,248 ≠ 1,257 and it says which rows are missing; the loop and `len(loader)` both ask the same loader and agree on the wrong answer. **A check that three methods agree is not the same as a check that they are right**, and noticing that unaided is a level-5 observation.
3. **Prove the reload is exact** (harder variation 3): `0.000000`, and explain why exact rather than approximate.
4. **Look at all eighteen wrong digits** (harder variation 4) and sort them into "I'd have got that wrong too" and "how did it miss that?". The second pile is next week's motivation, arrived at from evidence.
5. **Batch size 512** (harder variation 5): 45 steps instead of 600, and the accuracy falls. Then the sentence: *"epochs are not the unit."*
6. **The honest question:** *"epoch 13 scored 0.9704 and epoch 14 scored 0.9667. We saved epoch 14. Did we lose anything real, or is 0.0037 noise?"* Thirty-seven ten-thousandths of 540 rows is **two digits**. It is noise, and the honest answer is that you cannot tell those two models apart with 540 test rows — which is Week 11's lesson about small denominators arriving in a new costume.

### If the student won't engage today

**Close the laptop. Three boxes and some arrows.**

Draw the three file names on paper and hand them the pen.

Three instructions and nothing else:

> **"Three boxes: the class, the trainer, the predictor. Draw the arrows for who needs who."**
>
> **"Now draw the arrow that must NOT be there, and cross it out."**
>
> **"Last one. If I delete the trainer's file completely, does the predictor still work?"**

The answers: both scripts point at the class file; the forbidden arrow is predictor → trainer; and **yes, it still works** — which is the entire point of the week and can be arrived at with a pen in six minutes.

Then, if there is any appetite left, the four-row batch table from the struggling path. Two objectives out of four, on paper, and objective 4's *idea* is the one that Weeks 34 and 35 are built on. The typing survives; Week 26 rebuilds all of it on a CNN.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the class (spoken, 45 seconds)**

> "A network class has two methods. **Name them, and say what each one is for in one sentence.**"

*Good answer:* "`__init__` declares the parts the model will need and runs once when you build it. `forward` says how one batch flows through those parts and runs every time you call the model."

**What to catch:** an answer that puts the routing in `__init__`. Push once: *"which one runs every time you make a prediction?"*

**Check 2 — steps and epochs (spoken, 60 seconds)**

> "Nine hundred training rows, batch size 100, twelve epochs. **How many batches in one epoch, how many optimizer steps altogether, and how big is the last batch?**"

*Good answer:* "900 ÷ 100 = 9 exactly, so 9 batches, no leftover, and the last batch is a full 100. Twelve epochs × 9 = 108 steps."

**Full marks needs all three.** And this one has no remainder on purpose — a student who says "10 batches, last one has 0 rows" has memorised "round up" without understanding it.

**Check 3 — the artifact (spoken, 90 seconds)**

> "You email me `digits_mlp.pt` and nothing else. **Can I use it? What else do I need, and what one line must I remember to call?**"

*Good answer:* "Not on its own — the file is only 4,810 numbers and four names, it doesn't say what shape the network was. You need `digits_net.py` so you can build the same class first, then load the numbers into it. And you have to call `model.eval()`, or the dropout stays on and you'll get a different answer every time you run it."

**What to catch:** *"just load it"*. Ask: *"load it into what?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Copies a class without knowing which half does what. Uses epoch and step interchangeably. Cannot say what is inside a `.pt` file. Prediction script imports the trainer. |
| **2 — Emerging** | Writes the class with help and remembers `super().__init__()` after being reminded. Gets 40 from `len(loader)` but cannot derive it. Saves and loads when following the steps, and forgets `model.eval()`. |
| **3 — Secure** | Writes the class unaided, both halves, and shows it has the same 65 numbers as the `Sequential`. Derives 40 three ways and makes them agree. Trains past 95% and reports the score with the pile it came from. Ships a `predict.py` with no training code and calls `model.eval()`. **This is the target.** |
| **4 — Strong** | Reads a `state_dict` error and says immediately whether it is a name problem or a shape problem. Reports steps and batch size unprompted whenever epochs are mentioned. Runs inference twice as a matter of habit to check it repeats. Explains why the class lives in its own file. |
| **5 — Exceptional** | Notices that three agreeing step counts can all be wrong together, and names the fourth check that would catch `drop_last=True`. Argues that saving the whole model is a security decision, not a convenience one. Says that the 0.0037 gap between epoch 13 and epoch 14 is two digits out of 540 and therefore not a result. Connects the flat 64-column input to next week without being prompted. |

---

## 📤 Homework to Assign

This section gives the wording to use when you set the homework.

**Say this:**

> "About an hour, three pages, and the third one is an experiment, not a question.
>
> **First, page 23.4 — finish the digits MLP and its `predict.py`.** If it already works, run it once more and paste the output. I want three things on the page: the `FINAL:` line **with the split in it**, the four `state_dict` names with their shapes, and the grep with its `exit=1`.
>
> **Second, page 23.5 — count the optimizer steps in one epoch three different ways, and make all three agree.** By dividing and rounding up. By counting the loop. By asking the DataLoader. **All three printed numbers pasted on the page**, and one sentence saying what you would do if they disagreed.
>
> **Third, page 23.6 — the `model.eval()` experiment, and this is the one I care about.** Take one digit. Push it through the model five times with `model.train()` and paste all five answers. Then call `model.eval()` and push the same digit through five more times and paste those. **Then two sentences: what changed, and why that matters if you were shipping this to somebody.**"

**Workbook pages:** 23.1, 23.2, 23.3 in class · **23.4, 23.5, 23.6** at home.

**Expected time:** 25 min finishing the files and pasting the three pieces of evidence · 15 min on the three step counts · 20 min on the eval experiment and the two sentences. **About 60 minutes.**

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — does the `FINAL:` line name the pile?** *"0.9667 on 540 held-out digits"* is full marks; *"96.67% accurate"* is not, and it is worth one line of feedback every week until it sticks. **Two — are all three step counts actually pasted?** A page that says "they agree" without the three numbers has not done the task; the whole skill is the comparison. **Three — do the ten pasted predictions actually differ in the first block and match in the second?** If all ten are identical, `model.eval()` was called before the `train()` block, or `nn.Dropout` is missing from the class — and that is worth chasing, because the student has not seen the thing the page exists to show them. If the first five differ and the second five match, the point has landed, and the two sentences will usually say so.

---

## 🔑 Answer Key

Every question restated, so you can mark from this page alone.

### Page 23.1 — The identity proof (in pen, before running)

*Predict both lists of shapes and both totals, then check.*

| | `nn.Sequential` | class `MoonNet` |
|---|---|---|
| first grid | `0.weight` **(16, 2)** | `fc1.weight` **(16, 2)** |
| first bias | `0.bias` **(16,)** | `fc1.bias` **(16,)** |
| second grid | `2.weight` **(1, 16)** | `fc2.weight` **(1, 16)** |
| second bias | `2.bias` **(1,)** | `fc2.bias` **(1,)** |
| total | **65** | **65** |

**The complete file, and its real output:**

```python
"""same_brain.py - the class version and the Sequential version are one model."""
import torch
import torch.nn as nn


class MoonNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


torch.manual_seed(0)
seq = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
torch.manual_seed(0)
cls = MoonNet()

print("Sequential:")
for name, p in seq.named_parameters():
    print("   %-10s %s" % (name, tuple(p.shape)))
print("Module subclass:")
for name, p in cls.named_parameters():
    print("   %-10s %s" % (name, tuple(p.shape)))

print()
print("Sequential parameters     :", sum(p.numel() for p in seq.parameters()))
print("Module subclass parameters:", sum(p.numel() for p in cls.parameters()))
print("weights byte-identical    :",
      torch.equal(seq[0].weight, cls.fc1.weight)
      and torch.equal(seq[0].bias, cls.fc1.bias)
      and torch.equal(seq[2].weight, cls.fc2.weight)
      and torch.equal(seq[2].bias, cls.fc2.bias))

x = torch.tensor([[1.0, 2.0], [-0.5, 0.5]])
print("same output on the same input:", torch.equal(seq(x), cls(x)))
print("that output:", seq(x).reshape(-1).tolist())
```

```text
Sequential:
   0.weight   (16, 2)
   0.bias     (16,)
   2.weight   (1, 16)
   2.bias     (1,)
Module subclass:
   fc1.weight (16, 2)
   fc1.bias   (16,)
   fc2.weight (1, 16)
   fc2.bias   (1,)

Sequential parameters     : 65
Module subclass parameters: 65
weights byte-identical    : True
same output on the same input: True
that output: [0.059556588530540466, 0.0902349054813385]
```

**The required sentence about the names, at full marks:**

> "The shapes and the numbers are identical — 65 either way, and `torch.equal` says True on all four blocks. Only the names differ: `nn.Sequential` names its children by position, so the layers are 0 and 2 with the ReLU occupying slot 1, while the class names them by the attribute I chose. That matters because a `state_dict` is keyed by those names, so weights saved from one will not load into the other."

**Marking notes.** A student who predicted `(2, 16)` for the first shape has made Week 22's transpose slip; refer them to Figure 22.1 rather than writing out the correction. A student who cannot say *why* the second Sequential layer is `2` has not connected it to the ReLU, and that is a thirty-second fix.

### Page 23.2 — Steps in one epoch, four times (in class)

*For each row: full batches, leftover, total batches, and steps in 15 epochs.*

| rows | batch size | full batches | leftover | total batches | 15 epochs |
|---|---|---|---|---|---|
| 100 | 10 | 10 | **0** | **10** | 150 |
| 100 | 30 | 3 | **10** | **4** | 60 |
| 1257 | 32 | 39 | **9** | **40** | 600 |
| 1257 | 512 | 2 | **233** | **3** | 45 |

**The arithmetic, in full, for the two that matter:**

```text
1257 ÷ 32 = 39.28…    round up → 40
39 × 32 = 1248        1257 − 1248 = 9        1248 + 9 = 1257 ✅

1257 ÷ 512 = 2.455…   round up → 3
2 × 512 = 1024        1257 − 1024 = 233      1024 + 233 = 1257 ✅
```

**Row 1 is the trap and it is deliberate.** 100 ÷ 10 = 10 exactly, so there is **no leftover** and the last batch is a full 10. A student who writes "11 batches, last one has 0 rows" has learned "round up" as a ritual rather than as an idea.

**Row 4 is the one to talk about.** Same data, same 15 epochs, **45 steps instead of 600.** Thirteen times fewer nudges of the weights. That is why "15 epochs" alone is not a statement about anything.

**Confirmed against the DataLoader:**

```text
way 1 - divide and round up: 40
        39 x 32 = 1248, and 1257 - 1248 = 9 left over
way 2 - count the loop      : 40
        first batch 32 rows, last batch 9 rows, all rows 1257
way 3 - ask the DataLoader  : 40

15 epochs x 40 steps = 600 optimizer steps
```

### Page 23.3 — The CLEAN ROOM checklist (in class)

*All seven, with what counts as evidence.*

| | Box | Evidence |
|---|---|---|
| 1 | `digits_net.py` holds the class, and nothing else | The file is 14 lines: one import, one class, two methods. No `train`, no `print`. |
| 2 | `train_digits.py` imports it | `from digits_net import DigitNet` |
| 3 | `predict_digits.py` imports it | `from digits_net import DigitNet` |
| 4 | `predict_digits.py` does **not** import `train_digits.py` | No line beginning `from train_digits` or `import train_digits` |
| 5 | No optimizer, no loss, no backward, no DataLoader in `predict_digits.py` | The grep prints nothing and reports `exit=1` |
| 6 | `predict_digits.py` calls `model.eval()` | The line is there, immediately after `load_state_dict` |
| 7 | Two runs give the same answer | Two pasted runs, identical |

**The grep, and the thing to say about it:**

```bash
grep -E "optimizer|loss_fn|backward|\.step\(\)|DataLoader|train_test_split" predict_digits.py ; echo "exit=$?"
```

```text
exit=1
```

**`exit=1` is the pass.** grep exits 1 when it finds no matches. Say it before you run it or somebody will spend two minutes trying to fix a success.

**Box 4 is the one that fails.** `from train_digits import DigitNet` works perfectly and is therefore very attractive. The demonstration that kills it: run `predict_digits.py` and watch fifteen epochs of training scroll past before the prediction appears. *"You just retrained the model in order to use it."*

### Page 23.4 — Finish the digits MLP and its `predict.py`

**The three pieces of evidence, in full.**

**One — the `FINAL:` line, with the split:**

```text
optimizer steps in total: 600
FINAL: test accuracy 0.9667 on 540 held-out digits
```

**At full marks the student can also say where 540 came from:** 30% of 1,797 is 539.1, and `train_test_split(test_size=0.30, stratify=y, random_state=0)` gives 540 test and 1,257 train. `540 + 1257 = 1797` ✅.

**Two — the four names in the file, with their shapes and the total:**

```text
saved digits_mlp.pt
   fc1.weight (64, 64)
   fc1.bias   (64,)
   fc2.weight (10, 64)
   fc2.bias   (10,)
```

```text
4096 + 64 + 640 + 10 = 4810
```

And PyTorch agrees: `learnable numbers   : 4810`. **This is the fifth row of the Week 22 wall sheet, now confirmed by a real network.**

**Three — the grep:**

```text
exit=1
```

**And the prediction run itself:**

```text
loaded digits_mlp.pt, dropout is off
picked rows: [1528, 1144, 918]
   row 1528   true 2   guessed 2   correct
   row 1144   true 5   guessed 5   correct
   row 918   true 3   guessed 3   correct
```

*(The full text-art digits are in the Prep Checklist.)*

**Marking notes.** Two failure shapes to watch for. **A `FINAL:` line without the pile** — *"96.67% accurate"* — is the Week 2 habit slipping and it is worth one line of feedback. **A grep that prints something** means training code is in the prediction script; nine times out of ten the culprit is `from train_digits import DigitNet`, and the fix is one word.

**Praise if you see it:** a student who reports epoch 13's 0.9704 *and* the saved model's 0.9667 and explains why they reported the second has understood something Week 34 will formalise.

### Page 23.5 — Three ways, all agreeing

**The complete file, and its real output:**

```python
"""steps.py - how many optimizer steps in one epoch? Three ways, one answer."""
import math
import torch
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(0)
X = torch.zeros(1257, 64)
Y = torch.zeros(1257, 10)
loader = DataLoader(TensorDataset(X, Y), batch_size=32, shuffle=True)

print("way 1 - divide and round up:", math.ceil(1257 / 32))
print("        39 x 32 = %d, and %d - %d = %d left over" % (39 * 32, 1257, 39 * 32, 1257 - 39 * 32))

counted = 0
sizes = []
for xb, yb in loader:
    counted += 1
    sizes.append(xb.shape[0])
print("way 2 - count the loop      :", counted)
print("        first batch %d rows, last batch %d rows, all rows %d"
      % (sizes[0], sizes[-1], sum(sizes)))

print("way 3 - ask the DataLoader  :", len(loader))
print()
print("15 epochs x %d steps = %d optimizer steps" % (len(loader), 15 * len(loader)))
```

```text
way 1 - divide and round up: 40
        39 x 32 = 1248, and 1257 - 1248 = 9 left over
way 2 - count the loop      : 40
        first batch 32 rows, last batch 9 rows, all rows 1257
way 3 - ask the DataLoader  : 40

15 epochs x 40 steps = 600 optimizer steps
```

**The required sentence — "what would you do if they disagreed?"** Full marks:

> "Each way tests something different, so the pattern of disagreement tells me where to look. If the division says 40 and the loop and `len(loader)` both say 39, the DataLoader is not the one I think I built — most likely `drop_last=True`, which throws away the last 9 rows (the loop only agrees with `len(loader)` because it is counting the same loader). If the loop says fewer than `len(loader)`, something is breaking out of it early. And if all three say 39, I should check the sum of the batch sizes, because three methods can agree with each other and still all be wrong: `sum(sizes)` would be 1,248, not 1,257, and that is the check that catches it."

**Marking notes.** The three pasted numbers are the task; a sentence claiming agreement without them scores nothing. The last part of the sentence above — **three agreeing answers can be wrong together** — is a level-5 observation and should be praised loudly if it appears unprompted.

### Page 23.6 — The `model.eval()` experiment

**The complete file, and its real output:**

```python
"""eval_test.py - the same digit, five times, with dropout on and then off."""
import torch
from sklearn.datasets import load_digits

from digits_net import DigitNet

torch.manual_seed(0)

model = DigitNet()
model.load_state_dict(torch.load("digits_mlp.pt"))

digits = load_digits()
row = 37
x = torch.from_numpy(digits.data[row] / 16.0).float().reshape(1, 64)
print("row %d, true label %d" % (row, digits.target[row]))

model.train()          # dropout ON
print("\nmodel.train()  - dropout is ON")
for i in range(5):
    with torch.no_grad():
        scores = model(x).numpy()
    print("   try %d: guess %d   score for 9 = %+.4f" % (i + 1, scores.argmax(axis=1)[0], scores[0][9]))

model.eval()           # dropout OFF
print("\nmodel.eval()   - dropout is OFF")
for i in range(5):
    with torch.no_grad():
        scores = model(x).numpy()
    print("   try %d: guess %d   score for 9 = %+.4f" % (i + 1, scores.argmax(axis=1)[0], scores[0][9]))
```

```text
row 37, true label 9

model.train()  - dropout is ON
   try 1: guess 5   score for 9 = -1.7783
   try 2: guess 9   score for 9 = +0.6095
   try 3: guess 3   score for 9 = -3.0162
   try 4: guess 9   score for 9 = -1.8427
   try 5: guess 5   score for 9 = -0.8994

model.eval()   - dropout is OFF
   try 1: guess 9   score for 9 = -1.6703
   try 2: guess 9   score for 9 = -1.6703
   try 3: guess 9   score for 9 = -1.6703
   try 4: guess 9   score for 9 = -1.6703
   try 5: guess 9   score for 9 = -1.6703
```

**Sentence one — what changed?** Full marks:

> "With `model.train()` the dropout layer was still switching about 13 of the 64 hidden units off at random on every forward pass, and a different random set each time (about 13, not always exactly 13) — so the same picture got five different sets of ten scores and three different answers: 5, 9, 3, 9, 5. After `model.eval()` the dropout stops dropping, the forward pass is exactly the same arithmetic every time, and all five runs give 9 with a score of −1.6703 to four decimal places."

*(0.2 × 64 = 12.8, so "about 13 of 64" is the honest phrasing.)*

**Sentence two — why it matters if you were shipping this?** Full marks:

> "Because nothing goes wrong on the screen. There is no error and no warning — the model just gives a different answer to the same question depending on when you asked, so two people checking the same digit would disagree and neither could reproduce the other's result. And it costs real accuracy: measured over all 540 test digits, these same weights score 0.9519, 0.9444, 0.9463, 0.9481 and 0.9500 on five passes with dropout still on, against exactly 0.9667 every single time after `model.eval()`. So forgetting one line loses about two points — and, worse, loses the ability to quote a single number at all."

**Marking notes.** Three things. **All ten predictions must be pasted**, not summarised. **If all ten agree**, `model.eval()` was called too early or the class has no `nn.Dropout` — chase it, because the student has not seen the thing the page exists to show. And **the best answers notice that there is no error message**; that is the actual danger, and a student who says so has understood why this is a lab and not a lecture.

**Praise if you see it:** anyone who points out that `with torch.no_grad()` is in *both* blocks and did not prevent the randomness has separated the two lines' jobs properly. `no_grad` stops the recording; `eval` stops the dropping. They are not substitutes.

### Answers to every question posed in the lesson

**Hook — "in Week 3 we solved this problem for a scikit-learn pipeline. What did we do?"** Saved the fitted pipeline to a file with `joblib.dump`, then loaded it in a fresh script that did no fitting — the Clean Room Test. **The rule has not changed: the artifact is the deliverable.**

**Hook — "what is that?"** A handwritten **2**, row 1528 of `load_digits`, drawn as text art from its 64 brightness numbers.

**Hook — "which arrow must not exist?"** An arrow from `predict_digits.py` to `train_digits.py`. If the prediction script imports the training script, **importing it runs it** — so every prediction retrains the model first.

**Concept A — "where does the 32 come from, and why does it never change?"** It is the batch size — 32 digits at once. A layer changes the *second* number of the shape, never the first: `(32, 64)` becomes `(32, 10)` because `fc2` has 10 outputs. **The batch dimension goes first and stays put.**

**Concept B — "do the division."** 1257 ÷ 32 = **39.28125**.

**Concept B — "so, 39 or 40?"** **40.** 39 × 32 = 1248, and 1257 − 1248 = 9 rows would otherwise be thrown away. The check is `1248 + 9 = 1257`.

**Live-code step 1 — "read the last line. What is it telling you, and where?"** `cannot assign module before Module.__init__() call` — call `nn.Module`'s own setup **before** hanging any layer on `self`. So `super().__init__()` is the first line of `__init__`.

**Live-code step 2 — "what will be the same and what will be different?"** The four **shapes** and the total 65 will be identical; the four **names** will differ — `0.weight`/`2.weight` against `fc1.weight`/`fc2.weight`.

**Live-code step 4 — "it found four names and wanted four different names. Are the shapes wrong?"** **No.** `(64, 64)` and `(10, 64)` are exactly right. It is the *names* that do not match, because a `state_dict` is a dictionary keyed by name and `nn.Sequential` numbers its layers by position.

**Activity stage 2 — "how many steps, and how many epochs?"** **600 steps, 15 epochs, batch size 32.** All three numbers, or the answer is incomplete.

**Activity stage 2 — "which rows was 0.9667 measured on?"** The **540 held-out test rows** — 30% of 1,797, stratified, `random_state=0`, never trained on.

**Activity stage 2 — "how many numbers went into the file?"** 4096 + 64 + 640 + 10 = **4810**.

**Activity stage 2 — "epoch 13 got 0.9704 and epoch 14 got 0.9667. Which do you report?"** **0.9667**, because that is the model that was saved. And the difference, 0.0037 of 540 rows, is **two digits** — not a result you could defend. Keeping the best epoch's weights is early stopping, and it is Week 34.

**Activity stage 3 — "same three digits, same three answers?"** **Yes**, because `model.eval()` is in the file. If it were not, the answers would move — see page 23.6.

**Harder variation 1 — "which of the four ways would catch `drop_last=True`?"** **The sum of the batch sizes.** With `drop_last=True` the divide-and-round-up would still say 40 while the loop and `len(loader)` would both say 39 — but if the student had *predicted* 39 for some other reason, all three could agree on 39 and be wrong. `sum(sizes)` would come to **1248, not 1257**, and only that check notices the nine missing digits.

**Harder variation 3 — "why exactly 0.000000, rather than close?"** Because loading a `state_dict` **copies the numbers**; it does not recompute anything. Both models then perform bit-for-bit identical arithmetic on identical inputs. Anything other than exactly zero would mean the two models are not the same model.

**Harder variation 5 — batch size 512, 15 epochs.** `ceil(1257 / 512) = 3`, so **45 steps** instead of 600 — thirteen times fewer weight updates for the same number of epochs. Accuracy falls accordingly. **The epochs did not change; the training did.**

---

## 🔮 Next Week Preview

Next week the lesson turns on the sentence this one ended with. The digits model you just shipped treats each picture as 64 numbers in a row, and it has no idea which of them are neighbours — shuffle the 64 columns the same way for every image and it would train to just about the same 96.67% (a shuffled run landed at 96.5%). So we price that out: a dense layer on a flattened 8 × 8 picture costs `16 × 64 + 16 = 1040` learnable numbers, and a 3 × 3 convolution over the same picture costs `9 + 1 = 10`. Then the class draws a 6 × 6 image on graph paper, slides a 3 × 3 vertical-edge kernel across it by hand, fills in all sixteen output cells in pencil, and loads the identical nine numbers into `nn.Conv2d` to check every one. Any disagreement stops the lesson until it is found.

**To prep early:** three things. **One — squared paper.** Two sheets per student, because they will draw a 6 × 6 grid, a 3 × 3 kernel and a 4 × 4 feature map, and doing that freehand wastes four minutes and produces unreadable work. **Two — do the sixteen cells yourself tonight**, in pencil, on the 6 × 6 image whose left half is 10 and right half is 2. The answer is four rows of `0 24 24 0`, and if you have not done it by hand you cannot referee the disagreement when it happens. **Three — keep this week's `digits_mlp.pt` and all three files.** Week 25 reshapes the same digits into `(1797, 1, 8, 8)` and Week 26 trains a CNN on them, and the four-row comparison table in Week 26 needs today's 4,810 parameters and today's 0.9667 to compare against.
