# Week 21 — The Five-Line Loop

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Student Guide](../student-guide/week-21.md) · [Workbook](../workbook/week-21.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the five lines you will type for the rest of your life |
| **Big idea** | Every training run in every framework is the **same five lines in the same order** — and each one has a specific failure if you drop it. |
| **New vocabulary** | optimizer · `zero_grad` · `step` · `no_grad` · gradient accumulation |
| **New maths** | **None.** The only arithmetic is one gradient and one step, both worked by hand on six numbers. |
| **New syntax** | `torch.optim.SGD([w], lr=0.1)` · `optimizer.zero_grad()` · `optimizer.step()` · `with torch.no_grad():` |
| **Dataset** | **Six hand-typed points** — the hours-versus-marks pairs from Week 12: **(1, 20), (2, 28), (3, 36), (4, 44), (5, 52), (6, 60)**. Nothing loads, nothing downloads, and the answer is hidden in the data on purpose. |
| **Materials** | **Five large index cards, one line of code on each** — cut and written before class · the printed workbook (all of it: Warm-Up through Self-Check, with the Answers section torn off or folded away) · Blu-tack or tape for sticking results on the wall · the Bug Log · last week's `6 + 27 = 33` still on the wall |
| **Tech needed** | Laptop with Python 3, PyTorch and matplotlib. **No new installs.** No dataset, no internet. |
| **Prep time** | 25 minutes the night before (10 of them writing the five cards) · 5 minutes on the day |
| **Expected runtime of the code** | `fit_line.py` **about 1 second** for all 400 steps. `drop_a_line.py` runs six variants in **under 2 seconds**. Nothing today is slow. |

> **⚠️ Watch out:** save the `zero_grad` card for **last**. It is the only one of the five whose removal produces **no error message at all**, and almost every student predicts it will crash. If you do it first, the surprise is spent and the other four become bookkeeping. **Order matters: forward, loss, backward, step, and then zero_grad last.**

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Write the canonical training loop from a blank file**: `zero_grad`, forward, loss, `backward`, `step`, in that order.
2. **Delete each of the five lines in turn** and record exactly what happens — **including the ones that produce no error at all**.
3. **Explain why gradients accumulate by default**, and read a run where the gradient refuses to shrink.
4. **Use `torch.no_grad()` when measuring rather than learning**, and say what it saves.

Observable evidence: `fit_line.py` reporting `w = 8.0014` and `b = 11.9939` against the hidden line `8x + 12`; a five-row table with a **prediction, a result and the error message if any**, of which at least one row says *"no error, but wrong"*; and one measurement taken inside a `with torch.no_grad():` block with the `requires_grad` of the result printed as `False`.

---

## 🧑‍🏫 What YOU Need to Know First

This section is the background you need before teaching: what an optimizer is, the five lines, and the arithmetic worked by hand.

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable files are in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week.** There is one gradient and one step, and both are done by hand on six numbers in §3 below. If you can multiply six pairs of numbers and add them up, you can teach this whole lesson. Give this section twenty minutes and do the arithmetic in §3 with a real calculator — that is the part that makes you convincing in the room.

### 1. What an optimizer is

Last week ended with a complaint: we had all the slopes and we did not use them. Today we use them, and the object that does it is called an **optimizer**.

> **optimizer** — an object that holds a list of your knobs and knows the rule for updating them. You hand it the knobs once, at the start. After that, `optimizer.step()` updates every one of them.

```python
optimizer = torch.optim.SGD([w, b], lr=0.05)
```

`SGD` stands for **stochastic gradient descent**, and the only part of that name worth explaining today is that it is **exactly the update rule from Week 15**:

```text
w ← w − lr × slope
```

`[w, b]` is the list of knobs. `lr=0.05` is the learning rate — the size of the step. **The optimizer contains no cleverness at all in this form.** It is a bookkeeper: it remembers which tensors are knobs so that one call can update all of them, instead of you writing one line per knob.

🍕 **The analogy.** The optimizer is the person holding the clipboard with everybody's name on it. `backward()` works out who is to blame and by how much. `step()` is the clipboard person going down the list and adjusting each person by their own amount. `zero_grad()` is rubbing out yesterday's numbers before you start writing today's.

### 2. The five lines, and why the order is forced

```python
for step in range(400):
    optimizer.zero_grad()                  # 1. wipe last step's slopes
    pred = hours @ w + b                   # 2. predict with today's knobs
    loss = ((pred - marks) ** 2).mean()    # 3. one number for how wrong
    loss.backward()                        # 4. one slope per knob
    optimizer.step()                       # 5. move every knob downhill
```

![The five lines, in order, and the job of each](../figures/fig-w21-1-five-lines-in-order-with-jobs.svg)
*Figure 21.1 — The five lines, in order, and the job of each. Line 5's arithmetic: 0 − 0.05 × (−326.6667) = 16.3333.*

**The order is not a matter of taste, and this is the thing to be crisp about:**

- **4 needs 3.** `backward()` starts from a loss. Without line 3 there is nothing to walk back from.
- **3 needs 2.** The loss compares a prediction with the truth. Without line 2 there is no prediction — or worse, there is **last iteration's** prediction, which is a different and nastier bug.
- **5 needs 4.** `step()` applies the slopes. Without line 4 there are no new slopes, so it either does nothing or applies a stale one.
- **1 has to be first**, because line 4 **adds** into `.grad` rather than overwriting it. That is last week's `6 + 27 = 33`, and it is the whole reason line 1 exists.

**Two words that are worth spelling out because they sound interchangeable and are not:**

> **`zero_grad`** — wipe the slopes to zero. Does not touch the weights.
>
> **`step`** — move the weights using the slopes. Does not touch the slopes.

A student who swaps those two in their head will produce a loop that looks right and learns nothing.

> **gradient accumulation** — the fact that `.grad` adds rather than replaces. Deliberate: it lets you split a batch too big for memory into pieces and sum their gradients. The price is that you must wipe `.grad` yourself, every step, for ever.

### 3. The arithmetic, done by hand on the six points

**Do this on a calculator before you teach.** It is the only maths in the week and it makes every number on the screen predictable.

The six points, which are the ones from Week 12:

| hours | marks |
|---|---|
| 1 | 20 |
| 2 | 28 |
| 3 | 36 |
| 4 | 44 |
| 5 | 52 |
| 6 | 60 |

**These marks sit exactly on a line, on purpose: `marks = 8 × hours + 12`.** Check it: `8 × 1 + 12 = 20` ✅, `8 × 6 + 12 = 60` ✅. **The point of hiding a known answer in the data is that you can tell whether the loop found it.** Real data never does this, and Week 22 goes back to data that wobbles.

**We start both knobs at zero: `w = 0`, `b = 0`.** So every prediction is 0, and every error is `0 − marks`:

```text
errors:  −20, −28, −36, −44, −52, −60
```

**The loss** is the mean of the squared errors:

```text
400 + 784 + 1296 + 1936 + 2704 + 3600  =  10720
10720 ÷ 6  =  1786.6667
```

**And the screen prints `1786.6666`.** Same number; float32 shows six digits.

**The slope for `w`.** From Week 15: the slope of a mean-squared error with respect to a weight is *twice the average of (error × the input that weight multiplies)*. So multiply each error by its hours value and add them up:

```text
(−20 × 1) + (−28 × 2) + (−36 × 3) + (−44 × 4) + (−52 × 5) + (−60 × 6)
= −20 − 56 − 108 − 176 − 260 − 360
= −980

slope for w  =  2 × (−980) ÷ 6  =  −1960 ÷ 6  =  −326.6667
```

**The slope for `b`.** The bias multiplies 1 for every row, so it is just twice the average error:

```text
(−20) + (−28) + (−36) + (−44) + (−52) + (−60)  =  −240
slope for b  =  2 × (−240) ÷ 6  =  −480 ÷ 6  =  −80.0
```

**Then one step, with `lr = 0.05`:**

```text
w ← 0 − 0.05 × (−326.6667)  =  0 + 16.3333  =  16.3333
b ← 0 − 0.05 × (−80.0)      =  0 + 4.0      =   4.0
```

**And the loss after that one step: 650.5742.** From 1786.6666 to 650.5742 — **the first step does more than the next fifty put together.**

Every one of those numbers appears on the screen. Here is the real first line of the run:

```text
step   0  loss  1786.6666  w 16.3333  b  4.0000  dL/dw  -326.6667
```

**Note what the printed `w` is:** the value **after** the step, because the print comes after `optimizer.step()`. The loss and the gradient on that line belong to the *old* `w` (which was 0). Say that out loud; a student comparing `loss 1786.6666` against `w 16.3333` and trying to make them consistent is confused for a good reason.

### 4. Why the learning rate is 0.05, and what 0.1 does

The syntax line for this week is written `torch.optim.SGD([w], lr=0.1)` because that is the shape of the call. **On this data 0.1 is too big and it explodes.** That is not an embarrassment; it is the best thirty seconds of the lesson, because they hunted learning rates by hand in Week 15 and this is the same hunt with a real tool.

Real numbers, `lr = 0.1`, same six points:

```text
  step  0 loss 1786.6666259765625 w 32.66666793823242
  step  1 loss 8553.408203125 w -39.355560302734375
  step  2 loss 41215.35546875 w 118.61631774902344
  step  3 loss 198849.859375 w -228.6627655029297
  step  4 loss 959614.3125 w 534.0220336914062
  step 19 loss 1.7220197853167616e+16 w -70216040.0
```

**The signs alternate and the numbers grow.** `w` goes 32.7, then −39.4, then 118.6, then −228.7: it is leaping over the bottom of the valley and landing further up the other side each time. By step 19 the loss is 1.7 followed by sixteen digits, and by step 400 it is `nan`.

And the same code at three learning rates, after 400 steps:

| learning rate | after 400 steps |
|---|---|
| `0.01` | `w 8.5199`, `b 9.7743`, loss `0.960224` — right direction, still crawling |
| **`0.05`** | **`w 8.0014`, `b 11.9939`, loss `0.000007`** — this is ours |
| `0.1` | `w nan`, `b nan`, loss `nan` — gone |

**Nothing about this is new** except that a library is doing the stepping. It is Week 15's three panels — too small, about right, diverged — with `optimizer.step()` in place of `w -= lr * grad`.

### 5. Every line of `fit_line.py`, explained to somebody who has never programmed

```python
import torch

torch.manual_seed(0)
```

`torch.manual_seed(0)` fixes PyTorch's random-number generator. **Nothing today is random** — the six points are typed, and both knobs start at exactly 0 — so the seed changes nothing. It is there because **every file in this course sets its seed**, and a habit that has exceptions is not a habit.

```python
hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])
```

Six rows, one column each — shape `(6, 1)` both. **Columns, not flat lines**, and that is Week 19's `(200,)` versus `(200, 1)` bug again: if `marks` were flat, `pred - marks` would broadcast into a 6 × 6 grid and every number afterwards would be wrong with no error.

```python
w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
```

The two knobs. `w` is shape `(1, 1)` so that `hours @ w` works: `(6, 1) @ (1, 1)` gives `(6, 1)`. `b` is a single number that gets added to all six rows by broadcasting. **`requires_grad=True` on both** — last week's flag, meaning "record what happens to this, I want its slope".

```python
optimizer = torch.optim.SGD([w, b], lr=0.05)
```

Hand the two knobs to the optimizer, once. The square brackets make a list — **and they matter**: pass the tensor on its own and you get `TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor`.

```python
for step in range(400):
```

Four hundred trips round the loop. Each trip is one **step** — one update of both knobs. Since we use all six rows every time, one step is also one epoch, and Week 23 is where those two words come apart.

```python
    optimizer.zero_grad()
```

**Line 1.** Clear `w.grad` and `b.grad` (set them to `None`, or zero them). **Nothing else happens** — the weights are untouched. Without this, line 4 adds today's slope on top of yesterday's, and the pile grows.

```python
    pred = hours @ w + b
```

**Line 2.** The prediction for all six rows at once. `@` is grid-times-grid; the `+ b` adds the bias to every row.

```python
    loss = ((pred - marks) ** 2).mean()
```

**Line 3.** Subtract the truth, square (so being 5 under is as bad as 5 over, and being 50 out is far worse than being 5 out), then average the six. **One number.** `backward()` needs exactly one number to start from; give it six and you get `RuntimeError: grad can be implicitly created only for scalar outputs`.

```python
    loss.backward()
```

**Line 4.** Last week's line. It reads the recording backwards and **adds** the slope into `w.grad` and `b.grad`.

```python
    optimizer.step()
```

**Line 5.** For every knob in the list: `knob ← knob − 0.05 × its slope`. That is the entire content of `SGD`.

```python
    if step % 50 == 0 or step == 399:
        print("step %3d  loss %10.4f  w %7.4f  b %7.4f  dL/dw %10.4f"
              % (step, loss.item(), w.item(), b.item(), w.grad.item()))
```

Print on every fiftieth step and on the last one. **`.item()` on all four**, exactly as last week — these are numbers going into a printout, and there is no reason to keep 400 recordings alive to make a log.

### 6. What you will actually see on the screen, with the real numbers

**This is the real output of `fit_line.py`. You will see exactly this.**

```text
step   0  loss  1786.6666  w 16.3333  b  4.0000  dL/dw  -326.6667
step  50  loss     2.8163  w  8.8773  b  8.2442  dL/dw     0.3261
step 100  loss     0.4466  w  8.3493  b 10.5044  dL/dw     0.1299
step 150  loss     0.0708  w  8.1391  b 11.4044  dL/dw     0.0517
step 200  loss     0.0112  w  8.0554  b 11.7628  dL/dw     0.0206
step 250  loss     0.0018  w  8.0221  b 11.9056  dL/dw     0.0082
step 300  loss     0.0003  w  8.0088  b 11.9624  dL/dw     0.0033
step 350  loss     0.0000  w  8.0035  b 11.9850  dL/dw     0.0013
step 399  loss     0.0000  w  8.0014  b 11.9939  dL/dw     0.0005

found:  marks = 8.0014 x hours + 11.9939
wanted: marks = 8 x hours + 12
```

**Five things in there, and the fifth is the whole objective.**

1. **`loss 1786.6666` at step 0** — the number you computed by hand in §3.
2. **`dL/dw −326.6667` at step 0** — also computed by hand, and the `w 16.3333` on the same line is `0 − 0.05 × (−326.6667)`. **Point at all three and do the arithmetic out loud.**
3. **The gradient shrinks as the loss falls**: −326.6667, then 0.3261, then 0.1299, down to 0.0005. **A flattening slope means you are near the bottom.** That is Week 12's picture, live.
4. **`w` is nearly right long before `b` is**: at step 50, `w` is 8.88 and `b` is only 8.24. The bias takes longer because it gets a smaller share of the gradient — its slope is `−80` against `w`'s `−326.7`.
5. **`found: 8.0014 x hours + 11.9939`.** We hid `8x + 12` in the data and the loop found it to three decimal places, with nobody telling it either number. **That is the objective, and it is worth a pause.**

![Four hundred steps of the five-line loop](../figures/fig-w21-4-loss-falling-over-four-hundred-steps.svg)
*Figure 21.2 — Four hundred steps of the five-line loop. Step 0 loss 1786.666626, step 399 loss 0.000007.*

### 7. What each missing line actually does

This is the lesson's second half, so know all five before you walk in. **Three of the five produce no error.**

![Delete one line. Three of the five make no noise.](../figures/fig-w21-3-drop-each-line-what-breaks.svg)
*Figure 21.3 — Delete one line. Three of the five make no noise.*

**Drop line 1, `optimizer.zero_grad()` — no error, and the run is ruined.**

```text
  step   0  loss    1786.6666  dL/dw      -326.6667  w    16.3333
  step   1  loss     650.5742  dL/dw      -129.8889  w    22.8278
  step   2  loss    2737.1262  dL/dw       277.0704  w     8.9743
  step   3  loss      31.9444  dL/dw       244.9432  w    -3.2729
  step 399  loss    2907.9082  dL/dw      -247.1715  w     5.3946
w 5.3946  b 18.9274  loss 2907.908203
```

Read the gradient column: −326.7, then −129.9, then +277.1, then +244.9. **Those are sums of every slope so far**, so `w` keeps being pushed by old slopes after it has passed the bottom and the walk thrashes. (The sizes do not grow without limit — over the 400 steps they stay between roughly 0 and 340 — they just never shrink. This is undamped oscillation, not an explosion.) After 400 steps the loss is **2907.9082 — worse than the 1786.6666 it started at** — and `w` is 5.3946 when the answer is 8. **No error, no warning, and a plausible-looking log.**

**Drop line 2, the forward line — crashes, and the message is last week's.** If `pred` is computed once before the loop, the first `backward()` consumes that graph and the second finds it gone:

```text
  step 0 finished, loss 1786.6666
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.
```

**Note it completes step 0 first.** The crash is on step 1, which is a good detail: the loop is not wrong, it is *stale*.

**Drop line 3, the loss line — the same crash, for the same reason.** A loss computed once outside the loop is one graph, read once.

**Drop line 4, `loss.backward()` — no error, and nothing happens at all.**

```text
w 0.0000  b 0.0000  loss 1786.666626  w.grad None
```

`w.grad` is `None`, so `step()` has nothing to apply and skips those knobs silently. **Four hundred steps, zero learning, no complaint.** The tell is that `w.grad` is `None` rather than a number — last week's diagnosis, doing real work.

**Drop line 5, `optimizer.step()` — no error, and nothing happens either.**

```text
w 0.0000  b 0.0000  loss 1786.666626  dL/dw -326.6667
```

The gradient is computed perfectly, every step, and then thrown away by the next `zero_grad()`. **This is the saddest loop in the file: it does all the work and never acts on it.**

**How to tell drop-4 and drop-5 apart, which is the good question:** look at `w.grad`. If it is `None`, `backward()` never ran. If it holds `−326.6667`, `backward()` ran and `step()` did not.

### 8. `no_grad`, and what it saves

> **`torch.no_grad()`** — a block inside which PyTorch does not record anything. Use it whenever you are **measuring rather than learning**.

```python
with torch.no_grad():
    pred = hours @ w + b
    gap = (pred - marks).abs().mean()
```

The `with ... :` shape is a block that switches something on at the top and off again at the bottom. Inside it, nothing gets a `grad_fn`, so nothing is stored for a backward pass that is never going to happen.

**The evidence, from a real run:**

```text
measuring WITH the recorder on:
  requires_grad: True   grad_fn: AddBackward0
measuring with torch.no_grad():
  requires_grad: False   grad_fn: None
  average miss: 0.0023 marks
```

**What it saves is memory and time**, and the reason is exactly last week's `.item()` lesson: recording means keeping every intermediate value in case a slope is needed. If no slope will ever be needed, that storage is pure waste. On six points it is invisible. On a validation pass over 20,000 images it is the difference between fitting in memory and not.

**Say the rule as a sentence and make them repeat it: "if you are not going to call `backward()`, wrap it in `no_grad()`."** Every evaluation, every prediction on new data, every plot of a model's output.

*(There is a second reason, which is worth one line: inside `no_grad()` you cannot accidentally build a graph that leaks into your training. In this level that never happens, so keep it as an aside.)*

### 9. The three misconceptions you will actually meet

**Misconception 1 — "`zero_grad` resets the model."**
It resets the **slopes**, not the weights. The knobs keep everything they have learned. A student who believes otherwise will conclude the loop cannot possibly work, and they are reasoning correctly from a wrong premise. The cure is one demonstration: print `w` before and after `zero_grad()` and watch it not change.

**Misconception 2 — "if the loss goes down, the loop is right."**
The dropped-`zero_grad` run goes down at step 1 (1786 → 650) and is a wreck by step 399 (2907). **The first few steps of a broken loop often look fine.** The cure is to make them read the whole log, and to ask for the *final* loss, not the second one.

**Misconception 3 — "the order doesn't really matter as long as all five are there."**
It matters, and the failure is silent. Put `step()` before `backward()` (with `zero_grad()` still at the top) and `step()` finds the gradient just wiped, so it moves nothing, and `backward()` then fills a gradient that the next `zero_grad()` throws away: `w` never leaves 0.0000. (It would only be "one step behind" if `zero_grad()` were also missing, and then it is the pile-up again.) Put `zero_grad()` at the end and, contrary to what people expect, it is fine — once per trip is all that matters. The silent one is the first. **The five lines are an order, not a set.**

### 10. How deep to go, and where to stop

**Go this far:** the five lines typed from memory in the right order; the step-0 arithmetic done by hand and matched to the screen; each line deleted and its consequence recorded, including three silent ones; `no_grad` used once with `requires_grad` printed as `False`.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| `nn.Linear`, `nn.Sequential`, `nn.ReLU` | **Week 22, next week.** Today the knobs are two tensors you typed, and that is what makes the five lines readable. |
| `nn.MSELoss()` | **Week 22.** Today's loss is written out, so the students can see the subtraction and the squaring. |
| `momentum=0.9`, `Adam` | **Week 26** brings `Adam`. Today `SGD` is exactly Week 15's rule and nothing more. |
| Learning-rate schedules, warm-up, decay | Not in this level. If asked: *"yes, people change the learning rate as they go. Not this year."* |
| Mini-batches, `DataLoader`, epochs versus steps | **Week 23.** Today all six rows go through every step, so one step is one epoch. Say that once so the distinction has somewhere to land later. |
| `model.eval()` / `model.train()` | **Week 23**, with real models that behave differently while training. Today `no_grad` is the only measuring tool. |
| Early stopping, best-checkpoint restore | **Week 22** watches validation loss; stopping rules are not in this level. |
| Why it is called *stochastic* gradient descent | One sentence if asked: *"because normally you feed it a random handful of rows at a time rather than all of them. We use all six, so ours is not stochastic at all today."* Then stop. |

The line to hold all lesson: **five lines, in that order, and each one has its own way of failing.**

---

### 11. 🧭 The Growing Map — the same box, and the five lines that live in it

The student guide carries a figure called **Where This Fits**: the same picture every week with one
more piece filled in. Nothing moves this week either — and the two minutes are best spent pointing out
that the five lines they just learned are what all the dashed boxes on the right are made of.

![The Level 3 pipeline in Week 21: still the numpy and PyTorch tile, now the five-line training loop](../figures/fig-w21-0-where-this-fits.svg)

*Figure 21.0 — Week 21's version. Third week inside the gold `numpy brain · PyTorch` tile. The ↻ on
stage three is black, as it has been since Week 12 — and today it got its five-line spelling.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "which of today's five lines is the ↻?"** Same gold
   tile, third of five weeks. The answer is: **all of them.** Point at the loop symbol on stage three
   and then at the five index cards on the wall. *"That symbol has been black since Week 12. Those five
   cards are what is inside it, in the order you will type for the rest of your life."*
2. **Anchor it on the card that produced no error.** Hold up `optimizer.zero_grad()` and the result it
   was paired with: `1786.6666 → 2907.9082`, no traceback, loss going **up**. *"Three of these five
   break silently. That is the whole reason this got a lesson of its own instead of being a footnote
   in Week 22."* Then the gradient column: not-shrinking (swinging, sign flips) means the pile, `None` means no `backward()`,
   right-but-frozen means no `step()`.
3. **Point right and make the promise concrete.** `images · CNNs`, `no labels · words`, `ship it`.
   *"Every one of those boxes runs these exact five lines. From Week 22 on we stop explaining them and
   just type them — so if one of them is still fuzzy, this is the week to ask."* That invitation is
   worth more than another explanation.

> **🧑‍🏫 Why this is worth two minutes.** This is the last week the training loop is the *subject*
> rather than the scaffolding. From Week 22 the five lines appear in every file without comment, and a
> student who has not internalised them will spend the rest of the level unable to debug their own
> runs. Showing them on the map, inside a stage that is already finished and black, says the thing you
> want them to take away: **this is not new material, it is the permanent furniture.**

**One thing to notice, so you can answer if asked.** `learning signal` and `model` are lit, and
`evaluation` is dark — even though the lesson ended with `w = 8.0014` against a hidden `8x + 12`. The
distinction is real and worth one sentence: **checking that a fit recovered a line you hid is a test of
the loop, not an evaluation of a model.** No split, no held-out data, nothing reported to anybody. That
is why the thread stays off.

---

## 🧰 Prep Checklist

This section lists what to prepare before class, including the complete runnable files.

### 25 minutes the night before

- [ ] **Write the five index cards.** Ten minutes, and do it now — writing them in class costs five minutes of the clinic. One line per card, large enough to read from the back of the room:

```text
CARD 1   optimizer.zero_grad()
CARD 2   pred = hours @ w + b
CARD 3   loss = ((pred - marks) ** 2).mean()
CARD 4   loss.backward()
CARD 5   optimizer.step()
```

- [ ] **Type and run `fit_line.py` yourself.** The complete file:

```python
"""fit_line.py - the five-line loop, on six hours-vs-marks points."""
import torch

torch.manual_seed(0)

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])

w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)

for step in range(400):
    optimizer.zero_grad()                    # 1. wipe last step's slopes
    pred = hours @ w + b                     # 2. forward
    loss = ((pred - marks) ** 2).mean()      # 3. how wrong
    loss.backward()                          # 4. fill in every slope
    optimizer.step()                         # 5. take one step downhill

    if step % 50 == 0 or step == 399:
        print("step %3d  loss %10.4f  w %7.4f  b %7.4f  dL/dw %10.4f"
              % (step, loss.item(), w.item(), b.item(), w.grad.item()))

print()
print("found:  marks = %.4f x hours + %.4f" % (w.item(), b.item()))
print("wanted: marks = 8 x hours + 12")
```

Run `python3 fit_line.py`. You must see **exactly** the output in §6, ending:

```text
found:  marks = 8.0014 x hours + 11.9939
wanted: marks = 8 x hours + 12
```

**Expected runtime: about 1 second.**

- [ ] **Do the step-0 arithmetic on a calculator yourself.** All of it, out loud:

```text
errors at w = 0, b = 0:  −20, −28, −36, −44, −52, −60
loss    = (400 + 784 + 1296 + 1936 + 2704 + 3600) ÷ 6 = 10720 ÷ 6 = 1786.6667
dL/dw   = 2 × (−20−56−108−176−260−360) ÷ 6 = 2 × (−980) ÷ 6 = −326.6667
dL/db   = 2 × (−240) ÷ 6 = −80.0
w after = 0 − 0.05 × (−326.6667) = 16.3333
b after = 0 − 0.05 × (−80.0) = 4.0
```

**If you have not done those six lines yourself, do not teach the lesson.** They are the difference between "the computer says 1786.6666" and "we knew it would say 1786.6666".

- [ ] **Run `drop_a_line.py`** (full file in the Answer Key, under Build It Part B) so all six variants are familiar and neither traceback surprises you. **Runtime under 2 seconds.**
- [ ] **Run `pile_up.py`** (Answer Key, under Do the Maths by Hand, item M4). Four backwards, no wipe: `−326.6667`, `−653.3334`, `−980.0001`, `−1306.6667`. **This is the demonstration that justifies line 1.**
- [ ] **Run `measure.py`** (Answer Key, under Build It Part C) for the `no_grad` evidence and the loss-curve PNG.
- [ ] **Break it on purpose, twice**, so both deliberate mistakes are muscle memory:
  1. `torch.optim.SGD(w, lr=0.05)` without the brackets. Real message: `TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor`.
  2. `lr=0.1`. **No error.** The loss goes 1786 → 8553 → 41215 → 198849 and by step 400 everything is `nan`.
- [ ] **Print the whole workbook** — and remove its **✅ Answers** section at the end (the student must not see it).
- [ ] **Blu-tack or tape on the desk**, for sticking result slips on the wall during the clinic.
- [ ] **Leave last week's `6 + 27 = 33` on the wall.** You will point at it in the first two minutes.

### 5 minutes on the day

- [ ] Editor open, terminal ready. **`fit_line.py` deleted or renamed** — they type it, from the cards.
- [ ] Five cards **shuffled and face down** on the desk. **Card 1 kept separately at the bottom of the pile** — the `zero_grad` card is played last, on purpose.
- [ ] The six points on the board: **(1, 20), (2, 28), (3, 36), (4, 44), (5, 52), (6, 60)** — and **not** the line they came from. That is the thing they are looking for.
- [ ] A blank five-row table drawn on the wall sheet: *line removed · predicted · what happened · error message*.
- [ ] Workbook open at **🛠️ Build It, Part B** (the five-row table), with **🔢 Do the Maths by Hand** marked for M1–M3.
- [ ] Bug Log out.

### Fallback if the laptops fail

**The Drop-a-Line Clinic is a card activity. It genuinely does not need computers**, as long as you have run the six variants yourself and can read out the results.

1. **Order the five lines from scratch.** Shuffle the cards, hand them out, and have the class put them in order **by argument, not memory**: *"which of these needs a loss to exist first?"* Ten minutes, and it is objective 1 without a keyboard.
2. **The step-0 arithmetic, done by the class.** Six multiplications and an addition give `−980`; then `× 2 ÷ 6` gives `−326.6667`; then `0 − 0.05 × (−326.6667) = 16.3333`. **Objective 1's understanding, complete, on paper.**
3. **The pile-up, on paper.** *"If the slope is −326.6667 every time and nobody wipes it, what does `.grad` say after four backwards?"* `4 × 326.6667 = 1306.6668`. **That is objective 3 with a calculator**, and it is the best paper item of the week.
4. **Remove a card, predict, and reveal.** You read out the real result from your own run. The predictions are the lesson; the running is only the referee.
5. **`no_grad` on paper.** Two boxes: one holding `19.9953` with a tail of receipts stapled on, one holding `19.9953` on its own. *"You are printing this and never differentiating it. Which do you want?"* **Objective 4, delivered in two minutes.**

| If this fails | Do this instead |
|---|---|
| `TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor` | The brackets are missing: `SGD([w, b], lr=0.05)`. |
| The loss becomes `nan` within a few steps | The learning rate is too big. Ours is 0.05; 0.1 explodes on this data. |
| The loss never changes at all | Either `backward()` or `step()` is missing. `print(w.grad)` tells you which: `None` means no `backward()`. |
| The loss goes down then wanders up | `zero_grad()` is missing. Check the gradient column: if the magnitudes are not shrinking and the signs keep flipping, that is the pile. |
| `w` is `nan` but the loss printed fine at step 0 | Same as above — divergence takes two or three steps to show up in the log. |
| `RuntimeError: grad can be implicitly created only for scalar outputs` | `.mean()` (or `.sum()`) is missing from the loss line. `backward()` needs one number. |
| The final `w` is 8.5199, not 8.0014 | `lr=0.01` instead of `0.05`. Not wrong — just not finished. 400 more steps would get there. |
| A student's numbers differ in the fourth decimal | Check `lr`, the number of steps, and that both knobs start at 0.0. There is no randomness in this file at all, so **identical inputs must give identical output.** |

---

## ⏱️ The Lesson, Minute by Minute

This section is the timed plan for the lesson.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Find the Line I Hid | 7 | 7 | Six points on the board, and the answer is not given |
| 🧠 Concept — Five Cards, One Order | 18 | 25 | Order them by argument; the step-0 arithmetic by hand; the pile-up |
| 💻 Live-Code Together — `fit_line.py` | 18 | 43 | Type it from the cards, run it, match the hand numbers. **Two deliberate mistakes.** |
| 🎲 Their Turn — The Drop-a-Line Clinic | 20 | 63 | Remove a card, predict, run, stick the result on the wall |
| 🔑 Wrap & Assign | 7 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Find the Line I Hid (7 minutes)

**Do this:** Write only the six pairs on the board. **Do not write the line.**

```text
hours:  1    2    3    4    5    6
marks: 20   28   36   44   52   60
```

**Say this:**

> "Six students, six revision sessions, six test results. Week 12's numbers — you have met them before.
>
> There is a straight line hiding in there. I know what it is and I am not telling you. **In about twenty minutes a five-line program is going to find it, and neither of us will have told it anything except these twelve numbers.**"

**Ask this:** "Can anyone see it? Do not guess — work it out."

*Most classes get it in under a minute:* every extra hour adds 8 marks, and at 0 hours you would have 12. So `marks = 8 × hours + 12`.

*If somebody spots it:* **"Good. Now cover it up, because the interesting question is not what the line is — it is whether a machine that starts by guessing `w = 0` and `b = 0` can walk its way to it."** Write `8` and `12` on a piece of paper, fold it, and put it under something. You will unfold it at the end.

*If nobody spots it:* fine, leave it. It is better if the reveal comes from the program.

**Say this:**

> "Last week we got all the slopes and then did absolutely nothing with them. We knew which way was downhill and we stood still. That was on purpose, because I wanted today to be about one thing.
>
> Today we step. And the whole of today is **five lines of code**.
>
> Not five lines for this problem. **Five lines for every problem.** The training loop for a network that sorts photographs, the loop for the thing that suggests what you watch next, the loop somebody ran last month on ten thousand computers to train a language model — it is these five lines. More data, more knobs, more machines. Same five lines, same order.
>
> And every one of them has its own way of failing. Three of the five fail **silently** — no error, no warning, and a log that looks fine. Working out which three is what we are doing in the second half."

**Do this:** Put the five shuffled cards face up on the desk where everyone can see them.

> "There they are. In the wrong order. Let us fix that first."

---

### 🧠 Concept — Five Cards, One Order (18 minutes)

**Do this (6 min) — order the cards by argument.**

Stick the five cards on the wall in a deliberately wrong order, for example: `backward`, `step`, forward, `zero_grad`, loss.

**Ask this:** "Which of these five cannot possibly go first?"

*Hoped-for answer:* `loss.backward()` — it needs a loss to exist.

> "Right. `backward()` needs something to walk backwards from. So the loss card comes before it."

**Ask this:** "And what does the loss card need?"

*A prediction — so the forward card comes before the loss card.*

**Ask this:** "Where does `step()` go?"

*After `backward()`, because it applies the slopes.*

**Do this:** You now have four cards in order: forward, loss, `backward`, `step`. **Hold up `zero_grad` and say nothing for a moment.**

**Ask this:** "Last one. Where does wiping the slopes go, and why?"

*Some will say the end — "tidy up after yourself".*

**Do this:** Point at last week's `6 + 27 = 33` on the wall.

> **Say this:** "Remember Thursday. We called `backward()` on `x²` and got 6. Then on `x³` and got **33**, not 27. `.grad` **adds**.
>
> So if `zero_grad` goes at the end, what happens on the very first trip round the loop? Nothing bad — the grads are empty anyway. And on the second? You have just wiped the slope you were about to use... no, worse: you wipe at the end of trip one, then trip two adds its slope to an empty box, which is fine, and then...
>
> Actually, let us be honest: **putting it at the end also works, as long as it is there once per trip.** What does not work is leaving it out. And the reason we all write it first is that it is the only position where you can look at a loop and *know* the grads are clean before `backward()` runs. **First, every time, and then you never have to think about it again.**"

Stick the five cards up in final order, numbered 1 to 5. **Leave them there all lesson.**

**Do this (7 min) — the step-0 arithmetic, on the board, with the class.**

> "Before we run anything, we are going to predict the first line of output. All of it."

Work through it with them, writing every line:

```text
both knobs start at 0, so every prediction is 0
errors:  0−20, 0−28, 0−36, 0−44, 0−52, 0−60  =  −20, −28, −36, −44, −52, −60

loss = mean of the squares
     = (400 + 784 + 1296 + 1936 + 2704 + 3600) ÷ 6
     = 10720 ÷ 6
     = 1786.6667
```

**Ask this:** "Now the slope for `w`. From Week 15 — what do you multiply each error by?"

*By the input that `w` multiplies — the hours.*

```text
(−20 × 1) + (−28 × 2) + (−36 × 3) + (−44 × 4) + (−52 × 5) + (−60 × 6)
= −20 − 56 − 108 − 176 − 260 − 360
= −980

dL/dw = 2 × (−980) ÷ 6 = −326.6667
```

**Ask this:** "The slope is negative. What does a negative slope tell us to do to `w`?"

*Increase it.* Then:

```text
w ← 0 − 0.05 × (−326.6667) = +16.3333
```

> **Say this:** "So before we run a single line, we know what the first row of output says: **loss 1786.6666, slope −326.6667, and `w` jumps from 0 to 16.3333.** If the screen says anything else, one of us has made a mistake, and we will find out which in about six minutes."

**Do this (5 min) — the pile-up, live.** This is the demonstration that makes line 1 non-negotiable.

```python
w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
for i in range(4):
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    print("after backward %d:  w.grad = %10.4f" % (i + 1, w.grad.item()))
```

**Ask before running:** "Same weights, same six points, four times. What will the four numbers be?"

*Most say −326.6667 four times.* Run it:

```text
after backward 1:  w.grad =  -326.6667
after backward 2:  w.grad =  -653.3334
after backward 3:  w.grad =  -980.0001
after backward 4:  w.grad = -1306.6667
```

**Do this:** Write `4 × 326.6667 = 1306.6668` on the board next to the last row.

![Four backward() calls, no zero_grad()](../figures/fig-w21-2-gradients-piling-up-without-zero-grad.svg)
*Figure 21.4 — Four backward() calls, no zero_grad(). The four bars grow, and the fifth one is back to 326.6667 after the wipe.*

> **Say this:** "Nothing about the data changed. Nothing about the weights changed. **The true slope was −326.6667 every single time, and the pile grew.**
>
> Now imagine that inside a loop that runs four hundred times, where each step also multiplies by the learning rate. Every step now carries all the old slopes along with the new one, so the steps stop being the size you asked for, and — this is the important part — **nothing goes red.** That is why card 1 exists."

---

### 💻 Live-Code Together — `fit_line.py` (18 minutes)

**You never touch their keyboard.**

**Step 1 (4 min) — the data and the knobs, and 🐞 DELIBERATE MISTAKE ONE.**

```python
"""fit_line.py - the five-line loop, on six hours-vs-marks points."""
import torch

torch.manual_seed(0)

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])
print("hours", tuple(hours.shape), " marks", tuple(marks.shape))

w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD(w, lr=0.05)        # <-- the mistake
```

```text
hours (6, 1)  marks (6, 1)
Traceback (most recent call last):
  File "fit_line.py", line 12, in <module>
    optimizer = torch.optim.SGD(w, lr=0.05)
TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor
```

**Ask this:** "It wants an *iterable of Tensors*. What is it complaining about?"

*Hoped-for answer:* it wants a list, and we gave it one tensor on its own.

> **Say this:** "The optimizer takes a **list** of knobs, because a real model has hundreds and you hand them all over at once. Even with one knob, it wants the list: `SGD([w], lr=0.05)`. We have two, so `SGD([w, b], lr=0.05)`.
>
> And notice the shapes on the first line: `(6, 1)` and `(6, 1)`. **Columns, both of them.** If `marks` were a flat line of six numbers, `pred - marks` would quietly become a 6 × 6 grid — that is Week 19's bug, and it does not announce itself."

Fix it. **Bug Log, sixty seconds.**

**Step 2 (5 min) �� the five lines, typed from the cards.**

**Do this:** Point at the wall. Have them read the cards out in order while typing.

```python
for step in range(400):
    optimizer.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    optimizer.step()

    if step % 50 == 0 or step == 399:
        print("step %3d  loss %10.4f  w %7.4f  b %7.4f  dL/dw %10.4f"
              % (step, loss.item(), w.item(), b.item(), w.grad.item()))
```

**Ask before running:** "Board says the first row will be loss 1786.6666, slope −326.6667, `w` 16.3333. Ready?"

```text
step   0  loss  1786.6666  w 16.3333  b  4.0000  dL/dw  -326.6667
step  50  loss     2.8163  w  8.8773  b  8.2442  dL/dw     0.3261
step 100  loss     0.4466  w  8.3493  b 10.5044  dL/dw     0.1299
...
step 399  loss     0.0000  w  8.0014  b 11.9939  dL/dw     0.0005

found:  marks = 8.0014 x hours + 11.9939
wanted: marks = 8 x hours + 12
```

**Do this:** Unfold the piece of paper from the hook. `8` and `12`.

> **Say this:** "**8.0014 and 11.9939.** We never told it either number. It started at zero and zero, and it walked there in four hundred steps using nothing but twelve numbers and the direction of downhill.
>
> Look at the first row: 1786.6666, −326.6667, 16.3333. **All three are the numbers we worked out on the board with a calculator.** That is the last thing I will say about trusting the library. You predicted its output.
>
> One thing to notice about that first row, because it looks inconsistent: the loss and the slope belong to the **old** `w`, which was 0. The `w` printed is the **new** one, after the step. The print comes after `optimizer.step()`."

**Ask this:** "Read the `dL/dw` column down the page. What is happening to it, and what does that mean?"

*Hoped-for answer:* it is shrinking — from −326 to 0.0005 — so we are getting near the bottom, where the ground is flat.

> "Exactly Week 12's picture. **A flattening slope means you are arriving.** And notice `w` was nearly right by step 50 while `b` was still miles out — `b`'s slope was −80 against `w`'s −326.7, so it moves more slowly. Different knobs learn at different speeds, and that is a real problem in real models. It is one of the reasons Week 26's optimizer exists."

**Step 3 (4 min) — 🐞 DELIBERATE MISTAKE TWO: turn the learning rate up.**

Change `lr=0.05` to `lr=0.1` and run.

```text
step   0  loss  1786.6666  w 32.6667  b  8.0000  dL/dw  -326.6667
step  50  loss 26762685107439987340656851953213505536.0000  w 2768102711420256256.0000  b 646571867162804224.0000  dL/dw -40281413326085292032.0000
step 100  loss        inf  w 340482156895263333900541597585506304.0000  b 79529625672631113398087385067028480.0000  dL/dw -4954694134455749336546261015568842752.0000
step 150  loss        nan  w     nan  b     nan  dL/dw        nan
step 200  loss        nan  w     nan  b     nan  dL/dw        nan
step 250  loss        nan  w     nan  b     nan  dL/dw        nan
step 300  loss        nan  w     nan  b     nan  dL/dw        nan
step 350  loss        nan  w     nan  b     nan  dL/dw        nan
step 399  loss        nan  w     nan  b     nan  dL/dw        nan

found:  marks = nan x hours + nan
```

**Read the three stages in that log, because they are three different things.** At step 50 the loss is a real number with 38 digits in it. At step 100 it is `inf` — bigger than a float32 can hold. At step 150 it is `nan`, because the arithmetic reached `inf` minus `inf`, which has no answer. **Overflow first, then nonsense.**

**Ask this:** "Did it crash? And what is `nan`?"

*Hoped-for answer:* no crash; `nan` means "not a number".

**Do this:** Show the first four steps with a smaller loop so they can watch it happen:

```text
  step  0 loss 1786.6666259765625 w 32.66666793823242
  step  1 loss 8553.408203125 w -39.355560302734375
  step  2 loss 41215.35546875 w 118.61631774902344
  step  3 loss 198849.859375 w -228.6627655029297
```

> **Say this:** "Read the `w` column: 32.7, then minus 39.4, then plus 118.6, then minus 228.7. **It is leaping straight over the bottom of the valley and landing higher up the other side, every time.** Week 15, panel three. The only difference is that a library is doing the leaping.
>
> And the loss: 1786, 8553, 41215, 198849. By step 19 it is 1.7 times ten to the sixteenth, and by step 400 the numbers are too big for a float32 to hold, so they become `nan`. **`nan` poisons everything it touches** — once one weight is `nan`, every prediction is `nan` for ever.
>
> One dial, two hundredths of a difference, and the whole run is dead. Nothing in the code was wrong."

Put it back to 0.05. **Bug Log** — and the entry should say *"no error, and the loss goes UP"*.

**Step 4 (5 min) — measuring, with `no_grad`.**

```python
pred_recorded = hours @ w + b
print("recorder on :", pred_recorded.requires_grad,
      type(pred_recorded.grad_fn).__name__)

with torch.no_grad():
    pred_quiet = hours @ w + b
    gap = (pred_quiet - marks).abs().mean()
print("recorder off:", pred_quiet.requires_grad, pred_quiet.grad_fn)
print("average miss: %.4f marks" % gap.item())
```

```text
recorder on : True AddBackward0
recorder off: False None
average miss: 0.0023 marks
```

> **Say this:** "Same arithmetic, twice. The first one came back carrying a **receipt** — `requires_grad: True`, `grad_fn: AddBackward0` — because PyTorch assumed we might want to differentiate it. The second one came back with **nothing attached**.
>
> We are printing this number, not learning from it. The receipt is pure waste: it means PyTorch held on to every intermediate value in case we called `backward()`, and we were never going to.
>
> On six points that costs nothing. On a validation set of twenty thousand images it is the difference between fitting in memory and crashing. **The rule, and say it back to me: if you are not going to call `backward()`, wrap it in `no_grad()`.**
>
> And the answer itself: **0.0023 marks.** On a test out of 60, our line is wrong by about two thousandths of a mark. That is what four hundred steps bought."

---

### 🎲 Their Turn — The Drop-a-Line Clinic (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **remove one card, predict what breaks, run it, write the real result on a slip and stick it on the wall.** Cards 2 to 5 first; **card 1 last**, because it produces no error and everybody gets it wrong.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at the wall with the five cards and the five result slips.

**Say this:**

> "Five lines. Look at what happens when each one goes missing.
>
> **Card 2, the forward line — crash.** Card 3, the loss line — **crash.** Those two are your friends: they stop, and they name the problem.
>
> **Card 4, `backward` — no error.** `w.grad` stays `None`, nothing moves, four hundred steps of nothing.
>
> **Card 5, `step` — no error.** Every slope computed perfectly and thrown away.
>
> **Card 1, `zero_grad` — no error, and this is the one you all got wrong.** The loss goes down at first, so it looks like it is working. Four hundred steps later it is 2907.9082, having started at 1786.6666. **It ended worse than it started, and nothing anywhere said so.**
>
> Three of five make no noise. That is the lesson of the week, and it is bigger than PyTorch: **the failures that matter in this subject usually do not raise errors.** You find them by reading the numbers, not the console."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last thing, and it is next week's door.
>
> Count the knobs in today's program. Two: `w` and `b`. I typed them both by hand, passed them both to the optimizer by hand, and used them both by name in the forward line.
>
> Week 19's network had sixty-five. Are you going to type sixty-five tensors and list all sixty-five in the optimizer?
>
> Next week you meet `nn.Linear` — one object that holds a whole layer's weights and biases for you, hands them all to the optimizer in one go, and does the grid multiply when you call it. **And the five lines do not change. Not one of them.** That is what makes them worth learning today."

**Do this:** Hand out the homework. Read the second part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor` | "I want a list of knobs and you gave me one bare tensor." | `SGD(w, lr=0.05)` without brackets. | `SGD([w, b], lr=0.05)`. Even a single knob goes in a list. |
| `RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed).` | "The recording was freed when I read it, and you asked again." | The forward line (or the loss line) is **outside** the loop, so the same graph is read twice. | Put both inside the loop. **Every step needs a fresh forward pass.** |
| `RuntimeError: grad can be implicitly created only for scalar outputs` | "`backward()` needs one number to start from and you gave me six." | `.mean()` or `.sum()` missing from the loss line. | `loss = ((pred - marks) ** 2).mean()`. A loss is always one number. |
| `RuntimeError: size mismatch, got input (6), mat (6x1), vec (2)` | "These two blocks do not fit together." | `w` built as a flat `(2,)` tensor instead of `(1, 1)`, or `hours` and `w` the wrong way round. | Print both shapes. `hours` is `(6, 1)`, so `w` must be `(1, 1)`. |
| `RuntimeError: Only Tensors of floating point and complex dtype can require gradients` | "You cannot ask for the slope of a whole number." | `torch.tensor([[0]], requires_grad=True)` — no decimal point. | `[[0.0]]`. |
| `RuntimeError: expected m1 and m2 to have the same dtype, but got: long long != float` | "One grid holds whole numbers and the other decimals." | `hours = torch.tensor([[1], [2], ...])` — the `.0` left off. | Put the decimal points in: `[[1.0], [2.0], ...]`. |
| **No error. `w` and the loss are both `nan` by step 150 (the loss is already `inf` by step 51).** | Nothing crashed. The run is dead and every future prediction is `nan`. | The learning rate is too big — 0.1 on this data. The loss goes 1786 → 8553 → 41215 → 198849 first. | Turn it down. Ours is 0.05. **Watch the first four steps, not the last one.** |
| **No error. The loss never moves off 1786.666626, and `w.grad` is `None`.** | Nothing crashed and nothing learned. | `loss.backward()` is missing, so there are no slopes for `step()` to apply. | Add line 4. **`None` is the diagnosis: no backward has ever run.** |
| **No error. The loss never moves, and `w.grad` is `−326.6667`.** | Nothing crashed and nothing learned. | `optimizer.step()` is missing. The slopes are computed and then wiped by the next `zero_grad()`. | Add line 5. **The `.grad` value is how you tell this apart from the one above.** |
| **No error. The loss falls at first, then wanders and ends higher than it started.** | Nothing crashed. The model is worse than when you began. | `optimizer.zero_grad()` is missing, so gradients pile up and `w` is pushed by old slopes as well as the new one. | Add line 1. **Tell-tale: the gradient column never shrinks, and the signs flip.** |
| **No error. The loss is exactly the same every step and never changes at all.** | Nothing crashed. | The forward line is outside the loop **and** you added `retain_graph=True` to make the crash go away. | Take `retain_graph` out and put the forward pass back inside the loop. **The error was telling the truth.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds two, and both are about loops that run perfectly and learn nothing.

21. **"Read the gradient column, not the loss column."** A gradient that refuses to shrink (swinging in size, flipping sign) means the pile. A gradient of `None` means no `backward()`. A gradient that is right while nothing moves means no `step()`. **One column, three different diagnoses.**

22. **"What was the loss at the START, and what is it at the END?"** Not "is it going down" — the broken-`zero_grad` loop goes down at step 1. The comparison that catches it is first against last: **1786.6666 against 2907.9082.**

And the sentence for this week:

> **"Three of the five lines fail without saying anything. Read the numbers, not the console."**

---

## 🎲 The Activity, In Full

This section gives the main activity in full, step by step.

### The Drop-a-Line Clinic

**What it is.** Twenty minutes with five index cards on the wall. One card comes down, the class predicts what breaks, somebody runs it, and the real result goes up on a slip beside the card. **Card 1 is played last, on purpose, because it is the one everybody gets wrong.**

### Setup

- A working `fit_line.py` (theirs, from the live-code).
- **Five index cards** on the wall, numbered 1 to 5.
- **Five blank slips of paper** and something to stick them up with.
- Workbook **🛠️ Build It, Part B**, which is the five-row table: *line removed · what I predicted · what happened · the error message if any*.
- A pen.

### The rules, read out once

> **"One card comes down. Before anyone runs anything, everybody writes a prediction in the table — one line, and it has to say whether you think it will crash or not.**
>
> **Then we run it. Then somebody writes the real result on a slip and sticks it under the card.**
>
> **Only one card is missing at a time. Put it back before we take the next one."**

### The order to run them in, and what happens

**Card 2 first, the forward line (4 minutes).** Put `pred = hours @ w + b` **above** the loop instead of inside it.

Most predict a crash, and they are right — but not on the step they expect:

```text
  step 0 finished, loss 1786.6666
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed).
```

**The good question here: "why did step 0 work?"** Because the graph existed; `backward()` read it and freed it. Step 1 asked for a receipt that had already been thrown away. **A stale forward pass, not a wrong one.**

**Card 3 next, the loss line (2 minutes).** Same failure, same message, and that is the point: *the loss and the forward pass are one thing, and both belong inside the loop.*

**Card 4, `loss.backward()` (4 minutes).** Now the surprises start.

```text
w 0.0000  b 0.0000  loss 1786.666626  w.grad None
```

**No error.** Four hundred steps, and both knobs are exactly where they started. Ask: *"how would you know, from the log alone, that this was the missing line?"* **`w.grad` is `None`.**

**Card 5, `optimizer.step()` (4 minutes).**

```text
w 0.0000  b 0.0000  loss 1786.666626  dL/dw -326.6667
```

**Also no error, and also nothing learned** — but `w.grad` holds a real number. **The two silent failures look identical in the loss column and completely different in the gradient column.** That comparison is the most useful thing in the activity.

**Card 1 last, `optimizer.zero_grad()` (6 minutes).** Take the predictions first, out loud, and write the count on the board: how many think it will crash?

Then run it:

```text
  step   0  loss    1786.6666  dL/dw      -326.6667  w    16.3333
  step   1  loss     650.5742  dL/dw      -129.8889  w    22.8278
  step   2  loss    2737.1262  dL/dw       277.0704  w     8.9743
  step   3  loss      31.9444  dL/dw       244.9432  w    -3.2729
  step 399  loss    2907.9082  dL/dw      -247.1715  w     5.3946
w 5.3946  b 18.9274  loss 2907.908203
```

**Let the room look at step 1 before you say anything.** The loss went **down**, 1786 → 650. It looks like it is working.

Then step 2: up to 2737. Step 3: down to 31.9. Step 399: **2907.9082**.

> **Say this:** "No error. No warning. A log that starts by looking exactly like a successful run. And after four hundred steps the model is **worse than it was before it trained** — 2907 against 1786.
>
> Read the gradient column. −326, −129, +277, +244. **Those are piles, not slopes.** The true slope never had those values; they are sums of every slope so far.
>
> Whoever predicted a crash: you were reasoning sensibly. Missing something that important *should* be an error. It is not, and that is a fact about the tool you now know and most people find out the hard way."

### What "finished" looks like

- Five slips on the wall under five cards.
- Build It Part B with five rows filled: prediction, result, and error message where there was one.
- **At least one row saying "no error, but wrong"** — ideally three.
- The student can answer: *"how do you tell a missing `backward` from a missing `step`?"* **Look at `.grad`: `None` versus a real number.**

### Variation — easier

**Do two cards, not five: card 5 (`step`) and card 1 (`zero_grad`).** Those two are the whole idea — one does nothing, and one does something much worse than nothing while looking fine.

And **hand them the loop complete** with a comment marking the line to delete, so the activity is about predicting and reading, not editing.

Scaffold the prediction with a two-choice question instead of a blank line: *"will it (a) crash, or (b) run and give the wrong answer?"* **Both are (b), and finding that out is the lesson.**

### Variation — harder

1. **Swap two lines instead of deleting one.** Put `optimizer.step()` **before** `loss.backward()`. It runs, no error, and it learns **nothing**: `zero_grad()` has just wiped the gradient, so `step()` moves nothing, and `backward()` fills a gradient the next trip throws away. `w` stays 0.0000 while `w.grad` reads −326.6667. Ask them to prove it. (Print `w` and `w.grad` together and compare with the correct run.)
2. **Put `zero_grad()` at the end of the loop** instead of the start. It works fine. Ask why, and why we still write it first. (Because at the end you have to reason about the first iteration; at the start you never do.)
3. **Find the learning rate where it breaks.** Sweep 0.01, 0.05, 0.06, 0.07, 0.1. Real answers: 0.01 gets `w 8.5199` after 400 steps, 0.05 gets `8.0014`, and by 0.07 it is `nan`. **Ask where exactly the boundary is** — the honest answer is that it depends on the data as well as the model, which is why Week 15's hunt existed.
4. **Add `retain_graph=True`** to make the card-2 crash go away, then explain why that is a bad fix. (It works, the loss never changes, and you have hidden a real bug behind a flag the error message suggested.)
5. **Count the steps versus the epochs.** Today all six rows go through every step, so 400 steps is 400 epochs. Ask what would change if they fed three rows at a time. (800 steps for the same 400 epochs — and that is Week 23.)
6. **Measure what `no_grad` saves.** Time is hard to measure honestly at this size, so measure the evidence instead: with the recorder on, `pred.grad_fn` is `AddBackward0`; with it off, `None`. Then the argument: **what has to be stored for a backward pass that never happens?**

---

## ❓ Questions Students Ask This Week

This section collects questions students ask this week, with suggested answers.

**"Why doesn't PyTorch just zero the gradients for me?"**

Because sometimes you genuinely want them to add up, and the library cannot tell which you meant.

The real use is a batch too big for memory. Suppose you want the gradient over 1,000 rows and only 250 fit at once: run four forward-and-backward passes, let the gradients pile up, then take one step. If each piece's loss is divided by 4 first (or you use a sum rather than a mean), the total is exactly the gradient over 1,000 rows, and you never held more than 250 rows in memory. **That is a genuinely useful thing and it is the reason for the default.**

**And it is contested.** Plenty of experienced people think the default should have been the safe one, with accumulation as the opt-in — it is the single most common PyTorch bug in the world, and it costs beginners hours. Other frameworks made the other choice. **Nobody fully agrees, and you are allowed to think the default is wrong**; you still have to type line 1 every time.

**"Is `SGD` really just `w = w - lr * grad`? That seems too simple to have a name."**

In the form we are using, yes, exactly that. `torch.optim.SGD([w, b], lr=0.05)` with no other arguments does precisely what you wrote by hand in Week 15.

The name carries history rather than complexity. **"Stochastic"** means the gradient is normally computed on a random handful of rows rather than all of them — ours uses all six, so today's SGD is not even stochastic. And `SGD` can do more if you ask: `momentum=0.9` makes it keep a bit of its previous direction, like a ball rolling rather than a hiker stepping. **We are not touching that; Week 26 brings `Adam`, which is where optimizers get genuinely clever.**

**"Why 400 steps? How do you know when to stop?"**

Today it is cheating: we know the answer, so we can see when `w` reaches 8. **In real work you do not know**, and the honest answer is that you watch a curve.

What people actually do — and this is Week 22 — is watch the loss on data the model is **not** learning from. While that number keeps falling, keep going. When it flattens, you have finished. When it starts *rising* while the training loss keeps falling, you have gone too far and you are memorising rather than learning.

For now: 400 is enough to get three decimal places on this problem, and it takes a second.

**"What is `nan`, and why does it never recover?"**

`nan` means "not a number", and it is what floating-point arithmetic produces when it is asked something meaningless — infinity minus infinity, zero divided by zero, or a number too big to store.

It never recovers because **`nan` is contagious**: `nan` plus anything is `nan`, `nan` times zero is `nan`. Once one weight becomes `nan`, the next prediction is `nan`, so the loss is `nan`, so the gradient is `nan`, so every weight becomes `nan`. The run is over; there is nothing to salvage.

**The practical habit: if you see `nan`, do not look at the last step, look at the first four.** The cause is almost always a learning rate too large, and the first few steps show it clearly before everything turns to `nan`.

**"Does `no_grad` make the model worse?"**

No, and this is a fear worth killing quickly. `no_grad` changes **nothing** about the numbers coming out — the same weights, the same arithmetic, the same prediction to the last digit. All it does is stop PyTorch storing the extra bookkeeping it would need if you later asked for a slope.

The only way it can hurt you is if you accidentally wrap your **training** step in it. Then no gradients get recorded and nothing learns — which, by now, you know how to diagnose: `w.grad` is `None`.

**"We fitted a straight line. Couldn't scikit-learn have done this in one line?"**

Yes, and it would have been better at it. `LinearRegression().fit(X, y)` would find `w = 8` and `b = 12` exactly, instantly, using algebra rather than four hundred steps — for a straight line there is a formula, and it is a better tool.

**We are not here for the line. We are here for the loop.** Once the model is a network with sixty-five knobs and a ReLU in the middle, there is no formula, and this loop is the only thing that works. **Using it on a problem where you already know the answer is how you find out whether the loop is correct.** That is exactly why the data has `8x + 12` hidden in it.

**"Could I use these five lines on Week 19's network?"**

Yes, and that is next week — with `nn.Linear` so you do not have to name sixty-five tensors. **The five lines will not change at all.** That is the claim of the week and it holds for every model in this course, from today's two knobs to Week 26's convolutional network on 1,797 digit images.

**"What if I put the print statement in a different place — does that matter?"**

Not to the model, but it changes what the numbers mean, and it catches people. Ours prints **after** `optimizer.step()`, so the `w` on each row is the *new* value while the loss and the gradient belong to the old one. Print before `step()` and all four numbers describe the same moment.

Neither is wrong. **Just know which one you have**, because a student trying to check `loss` against `w` on the same line will not be able to make it work otherwise.

---

## ⚠️ Where This Lesson Goes Wrong

This section lists the places the lesson tends to go wrong and what to do right then.

| What happens | Why | What to do right now |
|---|---|---|
| **The `zero_grad` card is played first** | It is line 1, so it feels natural to start there | **Play it last.** It is the only silent-and-catastrophic one, and its whole teaching value is the room getting the prediction wrong together. |
| The step-0 arithmetic gets skipped for time | It is six multiplications and it looks like a detour | It is the only maths in the week and it turns the screen from an oracle into a check. **Cut a drop-a-line card instead** — cards 2 and 3 have the same failure, so you can do one of them. |
| Everybody predicts "crash" for every card and nothing is learned from being wrong | Predictions feel like a formality | Take a **show of hands and write the count on the board** before running. Public, specific, and countable. A prediction nobody recorded is a prediction nobody was wrong about. |
| The broken-`zero_grad` log gets read as "working" because step 1 improves | It genuinely does improve at step 1 | **Ask for the first and last loss, always.** 1786.6666 versus 2907.9082. Make it the standard question for the rest of the year. |
| Missing-`backward` and missing-`step` get treated as the same bug | They look identical in the loss column | Put both result slips side by side and point at `.grad`: **`None` versus `−326.6667`.** That contrast is the sharpest thing in the lesson. |
| A student adds `retain_graph=True` because the message suggested it | The error message literally suggests it | *"The message is guessing at what you wanted. Read what happened next: the loss stopped changing. You hid the bug."* |
| The learning-rate explosion is shown at step 400 only, so it just looks like `nan` | `nan` is the end of the story, not the story | **Show steps 0 to 3**: 32.7, −39.4, +118.6, −228.7. The alternating signs are the lesson; `nan` is only the funeral. |
| `no_grad` is presented as a performance tip and forgotten | It sounds optional | Tie it to something they already believe: *"this is last week's `.item()` lesson again — do not keep a receipt you will never read."* Then make them say the rule back. |
| The lesson runs out of time before `no_grad` | It is the fourth objective and it is at the end | **Compress the clinic to three cards** (5, 1, and either 2 or 3) and keep `no_grad`. It takes four minutes and it is on the homework. |
| Somebody points out sklearn could fit this line instantly, and it deflates the room | They are right | Agree immediately and enthusiastically, then say why we are here: **no formula exists for a network, and you cannot test a loop on a problem whose answer you do not know.** |

---

## 🧭 Differentiation

This section adjusts the lesson for students who struggle and students who move fast.

### If the student is struggling

**Cut:** the clinic from five cards to two — card 5 (`step`) and card 1 (`zero_grad`). Nothing else is load-bearing.

**Cut:** the `lr = 0.1` explosion. It is a repeat of Week 15 and it can be homework.

**Cut:** the `dL/dw` column from the printout. Loss, `w` and `b` are enough to see it working.

**Give them the loop complete**, with the five lines commented `# 1.` to `# 5.`. Typing five lines is not the objective; **knowing why they are in that order is.**

**The version of the arithmetic that skips everything hard.** The only maths is one gradient, so give it as a filled-in table with two blanks:

| step | what to multiply | answer |
|---|---|---|
| the errors, at `w = 0` | `0 − 20`, `0 − 28`, … | `−20, −28, −36, −44, −52, −60` |
| each error × its hours | `−20 × 1`, `−28 × 2`, … | `−20, −56, −108, −176, −260, −360` |
| add them up | | `−980` |
| times 2, divided by 6 | `2 × (−980) ÷ 6` | **`__________`** |
| the step | `0 − 0.05 × (−326.6667)` | **`__________`** |

Two blanks: `−326.6667` and `16.3333`. **Then run the file and find both numbers on the first line of output.** That is objective 1's understanding, delivered with a calculator.

**The copy-this-exactly scaffold.** Twelve lines, runs alone:

```python
import torch

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])
w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)

for step in range(400):
    optimizer.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    optimizer.step()

print("w = %.4f   b = %.4f   loss = %.6f" % (w.item(), b.item(), loss.item()))
```

```text
w = 8.0014   b = 11.9939   loss = 0.000007
```

Then three questions and nothing else: **"which line makes the guess? which line says how wrong it is? which line moves the knobs?"** — the `pred` line; the `loss` line; `optimizer.step()`. **That is objective 1, in twelve lines.**

**One thing you must not cut:** deleting `optimizer.zero_grad()` and seeing the final loss come out **higher** than the starting loss with no error. If the whole lesson collapses to one fact, make it *"a training loop can be badly broken and never say a word."*

### If the student is flying

None of these need syntax from a later week.

1. **Swap `step()` and `backward()`** (harder variation 1) and prove that `w` never moves even though `w.grad` holds a perfectly good −326.6667. **This is the most subtle bug available today** and it never errors.
2. **`zero_grad()` at the end of the loop** (harder variation 2): it works. Ask why we still write it first. The answer is about reasoning, not correctness.
3. **The learning-rate boundary** (harder variation 3): 0.06 works, 0.07 is `nan`. Ask whether that boundary is a property of the optimizer or of the data. **It is both, and that is why Week 15's hunt existed.**
4. **`retain_graph=True`** (harder variation 4) as a study in bad fixes.
5. **Fit a line to data that does *not* sit on a line.** Change one mark from 44 to 48 and re-run. The loss no longer goes to zero — it bottoms out around a non-zero number — and `w` and `b` land near but not on 8 and 12. **Ask what the leftover loss is.** (It is the part of the data no straight line can explain, and that is the honest normal case: Week 22 goes back to it.)
6. **The honest question:** *"our loss reached 0.000007. Is that a good model or a memorised one?"* On six points sitting exactly on a line, it is neither — **the answer was in the data and we found it.** A student who says "you cannot tell without data it has not seen" has understood Week 2 and is ready for Week 22.

### If the student won't engage today

**Close the laptop. Five cards and a calculator.**

Hand them the five cards shuffled and ask for one thing:

> **"Put these in an order that could possibly work. You do not have to know what they mean — just argue about which ones need the others to have happened first."**

That conversation is objective 1, and it needs no Python at all. *Which of these needs a loss? Which makes the loss? Which needs a prediction?*

Then one arithmetic question, on the calculator:

> **"The slope is −326.6667. The step size is 0.05. Start at zero. Where do you land?"**

`0 − 0.05 × (−326.6667) = 16.3333`. And then:

> **"Do it four times without wiping the slope: what is 4 × 326.6667?"**

`1306.6668`. *"That is what happens when you forget the first card, and nothing on the screen tells you."*

**Objectives 1 and 3, delivered with five bits of card and a calculator**, in about twelve minutes. The typing survives; next week uses all five lines again unchanged.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the five lines from memory (written, 60 seconds)**

> "Blank paper. **Write the five lines of the training loop, in order.** You may use short names. Then, beside each one, three words on what it does."

*Good answer:* `optimizer.zero_grad()` (wipe the slopes) · `pred = ...` (predict) · `loss = ...` (how wrong) · `loss.backward()` (fill in slopes) · `optimizer.step()` (move the knobs).

**What to catch:** `step` before `backward`. Ask *"what would `step` be applying?"* and wait.

**Check 2 — the silent failure (spoken, 60 seconds)**

> "A student's loop trains for 400 steps with **no errors**. The loss starts at 1786.6666 and ends at **2907.9082**. **Which line is missing, and how can you tell?**"

*Good answer:* "`optimizer.zero_grad()`. The gradients are piling up instead of being wiped, so each step carries every old slope along with it and it keeps overshooting. You can tell because the loss ended higher than it started, and if you print the gradient column it never shrinks and the signs keep flipping."

**Full marks needs the mechanism** — accumulation making each step carry all the old slopes — not just the name of the line.

**Check 3 — the two do-nothings, and `no_grad` (spoken, 90 seconds)**

> "Two loops both run 400 steps with no error, and in both of them `w` never leaves 0.0000. In one, `w.grad` is `None`. In the other, `w.grad` is `−326.6667`. **Which line is missing in each?** And then: **when should you wrap something in `torch.no_grad()`, and what does it save?**"

*Good answer:* "`None` means `backward()` never ran, so line 4 is missing. A real gradient with nothing moving means `step()` is missing, line 5. And you use `no_grad` whenever you are measuring instead of learning — evaluating, predicting, plotting — because otherwise PyTorch stores everything it would need for a backward pass you are never going to do. It saves memory and time, and the result is identical."

**What to catch:** "`no_grad` makes it faster" with no mechanism. Push once: *"faster because it stops doing what?"*

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot order the five lines. Believes a loop with no error message must be working. Cannot say what `zero_grad` does. |
| **2 — Emerging** | Types the loop correctly from a model. Knows `backward` gives slopes and `step` moves weights. Recognises the missing line when told what the log looks like. |
| **3 — Secure** | Writes all five lines from blank in the right order and says what each does. Fits `8x + 12` and reports `w = 8.0014`, `b = 11.9939`. Fills in all five rows of the drop-a-line table, including a "no error, but wrong" row. Uses `no_grad` for measuring. **This is the target.** |
| **4 — Strong** | Predicts the step-0 numbers — 1786.6666, −326.6667, 16.3333 — before running. Distinguishes missing `backward` from missing `step` by looking at `.grad`. Explains accumulation as the reason line 1 exists, with `4 × 326.6667 = 1306.6668`. Diagnoses `nan` by reading the first four steps rather than the last. |
| **5 — Exceptional** | Explains why accumulation is the *default* — splitting a batch too large for memory — and can argue both sides of whether that was the right choice. Spots that `zero_grad` at the end of the loop also works, and says why the front is still better. Shows that swapping `step` and `backward` runs silently one step behind. Says what the leftover loss means when the data does not sit on a line. |

---

## 📤 Homework to Assign

This section gives the homework and the words to introduce it. **The workbook has twelve sections, not two pages**, so the table below says which are done in class, which are the core homework, and which are extra. The split is a suggestion for this guide; the key below answers every section whichever ones you set.

**Say this:**

> "About an hour, two parts, and the second one is the one I care about. Both are in the **🛠️ Build It** section near the end of your workbook.
>
> **First, Build It Part A — fit the line.** Six points, the five-line loop, four hundred steps. Write your predicted step-0 row from your maths-by-hand answers **before** you run it. Then report **the `w` and the `b` it found**, to four decimal places, and write beside them the line I hid in the data. If your numbers are not close to 8 and 12, do not fix the numbers — find the missing line.
>
> **Second, Build It Part B — delete each line in turn and fill in the table.** Five rows. Four columns: **which line you removed, what you predicted, what actually happened, and the error message if there was one.**
>
> Two rules on that table. **One: write the prediction before you run it.** In pen. **Two: at least one of your five rows must say 'no error, but wrong'** — and if you have got three of them, you have done it properly.
>
> And copy the error messages **exactly**. Not 'it crashed'. The real words, including the bit that says *'a second time'*, because that phrase is the clue.
>
> The other sections — Warm-Up, Predict the Output, the two Practice Sets, Fix the Broken Program and the rest — are listed on the sheet I am handing you. Do the ones I have ticked."

**Workbook sections, in the order they appear:**

| Workbook section | Items | Where | Approx. time |
|---|---|---|---|
| ✅ Warm-Up | W1–W5 (last week's tensors and autograd) | Home, first | 5 min |
| 🔢 Do the Maths by Hand | M1–M4 | **In class** — the Concept segment works M1–M3 on the board; M4 goes with the `pile_up.py` demonstration | 15 min |
| 🔎 Predict the Output | P1–P4 | Home | 10 min |
| ✍️ Practice Set A — Read It | A1–A6 | Home | 25 min |
| ✍️ Practice Set B — Write It | B1–B5 | Home (B5 is the long one, about 25 lines) | 30 min |
| 🐞 Fix the Broken Program | three bugs, Runs 1–4 | Home | 20 min |
| 🧩 Puzzle of the Week | Part 1 (learning-rate boundary), Part 2 (Order Puzzle) | Extra | 20 min |
| 🤔 Think Deeper | T1, T2 | Extra | 15 min |
| 🛠️ Build It — Parts A and B | fit the line; five-row table | **Core homework** (Part B is also filled in live during the Drop-a-Line Clinic) | **about 60 min** |
| 🛠️ Build It — Part C, Stretch, Bug Log | `no_grad` once; learning-rate sweep | Stretch | 20 min |
| 🎨 Draw It | one trip round the loop, four questions | Extra | 10 min |
| 📊 Self-Check | ten "I can..." rows | Home, last | 3 min |

**Expected time for the core homework:** 20 min on the fit and the report (Part A) · 30 min on the five deletions and the table (Part B) · 10 min copying messages accurately. **About 60 minutes.** Everything else is on top of that, so choose; do not set the whole workbook in one week.

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — are the predictions in pen and clearly written before the results?** A table where every prediction matches every result exactly is a table that was filled in backwards. **Two — are the error messages verbatim?** *"Trying to backward through the graph a second time"* is a result; *"it crashed"* is not, and the difference is whether they can search for it in two years' time. **Three — does the `zero_grad` row explain the mechanism?** The answer that earns full marks says something like *"the gradients added up instead of being wiped, so each step carried every old slope along with it, so it kept overshooting and ended worse than it started — 1786.6666 to 2907.9082."* A student who writes *"it broke"* has watched the failure without understanding it, and that is worth one line of feedback: **"what happened to the gradient column?"**

---

## 🔑 Answer Key

Every workbook section and item, in workbook order, so you can mark from this page alone. The values come from the workbook's own **✅ Answers** section, re-checked by running the code. Teacher-only notes (wrong-answer maps, marking tips) are marked **Marking** or **Watch for**. The complete runnable files `drop_a_line.py`, `pile_up.py` and `measure.py` sit under Build It Part B, Maths item M4 and Build It Part C.

### Warm-Up

*Last week's tensors and autograd. W1–W5.*

**W1.** **One:** the default decimal type is `float32`, about seven digits, so `2.1` prints as `2.0999999046325684` — numpy would say `float64`. **Two:** a tensor can be **tracked**: set `requires_grad=True` and the results grow a `grad_fn` in the printout, and you can call `backward()` on them. Both are visible on a screen.

**W2.** It is **the recording**: `z` remembers that a matrix multiply produced it and which tensors went in. **It is there because one of the inputs (`w`) had `requires_grad=True`**, so PyTorch started tracking.

**W3.** **33**, because the slopes are `6` and `27` and **`.grad` adds instead of replacing.**

**W4.** Either **`backward()` has not been called yet**, or **`requires_grad=True` is missing** on that tensor. `print(w.requires_grad)` tells you which.

**W5.** **200 tensors, each still carrying the whole graph that made it** — visible as the `grad_fn` in the printout. The first thing to break is plotting: `Can't call numpy() on Tensor that requires grad`. And the memory cost is real — about six times as much for the same numbers.

**Watch for:** W3 answered "27" (thinks the second call replaced the first) or "9" (adds the wrong things). Only 33 is right, and the reason has to say *adds instead of replacing* — this is the fact that the whole of line 1 depends on today.


### Do the Maths by Hand

*No new maths; calculator only. Both knobs start at zero. M1–M4.*

**M1.**

```text
errors:        −20   −28   −36   −44   −52   −60
squared:       400   784  1296  1936  2704  3600
sum:           10720
÷ 6:           1786.6667
```

**M1(a).** **Both are right.** `10720 ÷ 6` is `1786.66666…` repeating for ever. Your calculator rounds the seventh digit up to `1786.6667`; the screen is showing you `float32`, which holds about seven digits and lands on `1786.6666`. **Same number, different number of digits kept.**

**M2.**

```text
(−20 × 1) = −20    (−28 × 2) = −56    (−36 × 3) = −108
(−44 × 4) = −176   (−52 × 5) = −260   (−60 × 6) = −360

sum:  −980
× 2:  −1960
÷ 6:  −326.6667
```

**M2(a).** **Increase it.** A negative slope means the loss falls as `w` rises, so you go that way. The `−` in `w ← w − lr × slope` turns the negative slope into a positive step.

**M2(b).** `w ← 0 − 0.05 × (−326.6667) = 0 + 16.3333 = 16.3333`.

**M3.**

```text
sum of the errors:  −240
× 2 ÷ 6:            −80.0

b ← 0 − 0.05 × (−80.0) = 0 + 4.0 = 4.0
```

**M3(a).** **`w` moves faster, by about four times**: `326.6667 ÷ 80 = 4.08`.

**M3(b).** **Yes.** At step 50, `w` has travelled from 0 to 8.88 (already past 8) while `b` has only reached 8.24 out of 12. **Different knobs learn at different speeds**, and this is one of the reasons Week 26's optimizer exists.

**The whole of step 0 in one block** (this is also the predicted step-0 row in Build It Part A):

```text
predictions with w = 0, b = 0:   all six are 0
errors (pred − marks):           −20, −28, −36, −44, −52, −60

squared:                         400, 784, 1296, 1936, 2704, 3600
sum:                             10720
loss = 10720 ÷ 6               = 1786.6667

each error × its hours:          −20, −56, −108, −176, −260, −360
sum:                             −980
dL/dw = 2 × (−980) ÷ 6         = −326.6667

sum of the errors:               −240
dL/db = 2 × (−240) ÷ 6         = −80.0

w ← 0 − 0.05 × (−326.6667)     = 16.3333
b ← 0 − 0.05 × (−80.0)         = 4.0
```

**And the loss after that single step is 650.5742**, down from 1786.6666. **The first step does more than the next fifty combined.**

Every one of these numbers appears in the real first line of output:

```text
step   0  loss  1786.6666  w 16.3333  b  4.0000  dL/dw  -326.6667
```

**Marking:** `1786.6667` (accept `1786.67`), `−326.6667`, `−80`, `16.3333`, `4.0`. The `b` slope is the one people miss — it is the errors added up with no multiplication, because the bias multiplies 1 on every row.

**M4 — the pile-up.**

| after | `w.grad` |
|---|---|
| 1 backward | **−326.6667** |
| 2 backwards | **−653.3334** |
| 3 backwards | **−980.0001** |
| 4 backwards | **−1306.6668** |

**M4(a).** `4 × 326.6667 = 1306.6668`.

**M4(b).** *Because each of the four additions happens in `float32`, which keeps about seven digits, so a tiny rounding error accumulates and the fourth total lands on `1306.6667` instead.* **That is last week's dtype lesson, turning up somewhere you were not looking for it.**

**M4(c).** **Four times as big as you meant.** The step is `lr × .grad`, and the `lr` is unchanged, so a gradient four times too large is a step four times too large. **In a real loop the pile is not four times the slope but the running total of every slope so far, which is why the run swings about instead of settling.**

**`pile_up.py` is the live demonstration behind M4.** The complete file:

```python
"""pile_up.py - what 'gradients add up' actually means."""
import torch

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])

w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)

print("same weights, same data, four backward() calls, no zero_grad:")
for i in range(4):
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    print("  after backward %d:  w.grad = %10.4f   (%d x -326.6667 = %10.4f)"
          % (i + 1, w.grad.item(), i + 1, (i + 1) * -326.6667))

print()
print("now wipe it and do one more:")
w.grad.zero_()
b.grad.zero_()
pred = hours @ w + b
loss = ((pred - marks) ** 2).mean()
loss.backward()
print("  after zero_() and one backward: w.grad = %.4f" % w.grad.item())
```

Real output:

```text
same weights, same data, four backward() calls, no zero_grad:
  after backward 1:  w.grad =  -326.6667   (1 x -326.6667 =  -326.6667)
  after backward 2:  w.grad =  -653.3334   (2 x -326.6667 =  -653.3334)
  after backward 3:  w.grad =  -980.0001   (3 x -326.6667 =  -980.0001)
  after backward 4:  w.grad = -1306.6667   (4 x -326.6667 = -1306.6668)

now wipe it and do one more:
  after zero_() and one backward: w.grad = -326.6667
```

*(The four growing bars, and the fifth one after the wipe, are **Figure 21.4** in the Concept segment above.)*

**The point to insist on:** the true slope was `−326.6667` on all four occasions. **Nothing about the data or the weights changed.** The last row differs from `4 × 326.6667` in the fourth decimal (`1306.6667` against `1306.6668`) because each addition is done in float32 — a nice, harmless reminder of last week's dtype lesson.

**Marking:** M3 is the one people miss. If the `dL/db` answer is a multiple of the hours (for example −980 × 2 ÷ 6), they multiplied by the input; the bias multiplies 1.


### Predict the Output

*P1–P4. Predictions in pen before anything runs.*

**P1.**

```text
tensor([[6.]])
None
tensor([[3.]], requires_grad=True)
```

**Line 2: expected `tensor([[0.]])`, got `None`.** Modern PyTorch's `zero_grad()` **throws the box away** rather than filling it with zero — it is slightly faster, and the effect on the next `backward()` is the same, because `backward()` adds into an empty box either way.

**So `None` is a completely normal thing to see just after `zero_grad()`.** And last week's rule still stands: `None` means nobody has written there.

**Line 3: no, `zero_grad()` did not change `w`.** It is still `3.0`. **That proves the two jobs are separate: `zero_grad` touches slopes only.**

**P2.** The slope of `w × w` at `w = 3` is `2 × 3 = **6**`. So `3 − 0.1 × 6 = 2.4`.

```text
2.4000000953674316
6.0
```

**Line 1 is not exactly 2.4 because it is `float32`** — 2.4 has no exact binary form, so you get it right to about seven digits and then it stops.

**Line 2 proves that `step()` does not touch the slopes.** It moved `w` from 3.0 to 2.4 and left `w.grad` sitting on `6.0`, exactly where `backward()` put it. **Which is precisely why you must wipe it yourself.**

**P3.**

```text
torch.Size([3, 1])
torch.Size([3, 3])
5.333333492279053
```

By hand: `1 × 2 + 1 = **3**`, `2 × 2 + 1 = **5**`, `3 × 2 + 1 = **7**`. The three marks are 3, 5, 7. **The model is perfect, so the loss should be `0.0`.**

**It was `5.333333492279053`.** The extra numbers came from **broadcasting**: `pred` is a `(3, 1)` column and `marks` is a `(3,)` flat row, so `pred - marks` became a **3 × 3 grid** comparing every prediction with every mark — including the six pairs that belong to different students.

**The one-word fix:** `marks.reshape(-1, 1)` — make it a **column**. *(Writing `marks = torch.tensor([[3.0], [5.0], [7.0]])` in the first place is the same fix.)*

**P4.**

```text
True False
False True
8.0 8.0
```

**Line 3 in one sentence:** *`no_grad` gave exactly the same answer, `8.0`, while storing nothing for a backward pass that was never going to happen.* **Same numbers, less bookkeeping. That is the entire trade.**

**Marking:** the surprise is P1 line 2 (`None`, not `tensor([[0.]])`) and P3 (a wrong loss with no error). A student who predicted all four right has probably seen them before; ask which one they would have got wrong a week ago.


### Practice Set A

*Read It. A1–A6.*

**A1.** optimizer → **(iii)** · `zero_grad` → **(iv)** · `step` → **(v)** · `no_grad` → **(i)** · gradient accumulation → **(ii)**

**A2.** The correct order and jobs:

| # | line | job |
|---|---|---|
| 1 | `optimizer.zero_grad()` | wipe last step's slopes |
| 2 | `pred = hours @ w + b` | predict with today's knobs |
| 3 | `loss = ((pred − marks) ** 2).mean()` | one number for how wrong |
| 4 | `loss.backward()` | one slope per knob |
| 5 | `optimizer.step()` | move every knob downhill |

**A2(a).**

- **line 2 after line 1:** so that the slopes are clean before the pass that will add to them.
- **line 3 after line 2:** the loss compares a prediction with the truth, and without line 2 there is no prediction — or worse, there is **last iteration's**.
- **line 4 after line 3:** `backward()` starts from a loss. Without one there is nothing to walk back from.
- **line 5 after line 4:** `step()` applies the slopes, so the slopes have to exist first.

**A2(b).** Because **it is the only position where you can look at a loop and *know* the gradients are clean before `backward()` runs.** Putting it at the end also works (see the Order Puzzle), but then you have to reason about what happens on the first iteration. **First, every time, and then you never think about it again.**

**A3.**

| # | What happens | The fix |
|---|---|---|
| a | `TypeError: params argument given to the optimizer should be an iterable of Tensors or dicts, but got torch.FloatTensor` | `SGD([w, b], lr=0.05)` — a list, even for one knob |
| b | `RuntimeError: grad can be implicitly created only for scalar outputs` | `.mean()` on the loss line |
| c | `RuntimeError: expected m1 and m2 to have the same dtype, but got: long long != float` | `[[1.0], [2.0], [3.0]]` |
| d | Completes step 0, then `RuntimeError: Trying to backward through the graph a second time ...` | Put the forward line **inside** the loop |
| e | **No error.** `pred - marks` broadcasts into a 3 × 3 grid (6 × 6 with the full data) and every number afterwards is about the wrong question | Make it a column: `[[20.0], [28.0], [36.0]]` |
| f | **No error.** `step()` applies the freshly-wiped gradient, so nothing moves — 400 steps and `w` stays `0.0000` | Put `backward()` before `step()` |

**A3(g).** **e and f.**

**A3(h).** For **e**, print `marks.shape` — `(3,)` instead of `(3, 1)` — or notice `(pred - marks).shape` is `(3, 3)`. For **f**, `w` never leaves `0.0000` while `w.grad` holds a perfectly good `−326.6667`. **The gradient is right and nothing moves.**

**A4.** i → **Q** · ii → **S** · iii → **P** · iv → **T** · v → **R**

**A4(f).** **Q (`None`) and T (`False`).** `None` means **no slope has ever been written into that box** — it is an absence. `False` means **this tensor is genuinely not being tracked** — it is a fact about the tensor, deliberately arranged by the `no_grad` block. **One is "nothing has happened yet"; the other is "nothing is going to."**

**A5.**

**Log W — `optimizer.zero_grad()` is missing.** Giveaway: **the gradient column never shrinks and flips sign** (−326.7, −129.9, +277.1, and still around ±250 at step 399) and **the final loss, 2907.9082, is higher than the starting 1786.6666.** Those are piles, not slopes.

**Log X — `loss.backward()` is missing.** Giveaway: **`dL/dw` is `None` on every line.** No backward pass ever ran, so `step()` had nothing to apply.

**Log Y — `optimizer.step()` is missing.** Giveaway: **`dL/dw` is a perfectly correct `−326.6667` on every line, and nothing moves.** The slopes were computed and then wiped, 400 times.

**Log Z — nothing is missing. The learning rate is too big** (`0.1` instead of `0.05`). Giveaway: **step 0 is fine, then `w` alternates in sign** (32.7, −39.4, +118.6) while the loss grows, and it ends in `nan`.

**A5(a).** **The question is: what does `dL/dw` say?** X says **`None`** — no `backward()`. Y says **`−326.6667`** — `backward()` ran, `step()` did not.

**A5(b).** **The learning rate**, changed from `0.05` to **`0.1`**. `0 − 0.1 × (−326.6667) = 32.6667`, exactly twice the healthy step.

**A5(c).** **Easiest → hardest: Z, X, Y, W.** Z screams — the numbers are absurd within three steps and end in `nan`. X and Y are obvious *if you print the gradient*, and invisible if you only watch the loss. **W is the hardest by a long way**, because it goes down at step 1 and produces a plausible-looking log all the way through; the only thing that catches it is comparing the **first** loss with the **last** one.

**A6.**

**a)** `zero_grad` wipes **the slopes** and never touches **the weights**. `step` moves **the weights** and never touches **the slopes**.

**b)** Line 1 exists because line 4 **adds into `.grad`** instead of **overwriting it**.

**c)** Three of the five lines fail with **no error at all**. The comparison that catches the worst of them is **the first loss (1786.6666)** against **the last loss (2907.9082)**.

**d)** by looking at **`w.grad`**: `None` means **`backward()` never ran**, and `−326.6667` means **`backward()` ran and `step()` did not**.

**e)** `no_grad` changes **nothing** about the answer, and saves **the memory and time of storing every intermediate value for a backward pass that will never happen**.

**f)** look at the **first four** steps.

**Watch for:** in A5(c) students put **W** easiest because "the loss goes down" at step 1. It is the hardest, and the only thing that catches it is first loss against last loss. In A3, (e) and (f) are the two that students label as errors; both are silent.


### Practice Set B

*Write It. B1–B5. Accept any code that produces the expected output; the versions below are the model.*

**B1.**

```python
import torch

w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)
print("w", tuple(w.shape), " b", tuple(b.shape), " w.grad", w.grad)
```

```text
w (1, 1)  b (1,)  w.grad None
```

`w` is `(1, 1)` so that `hours @ w` works — `(6, 1) @ (1, 1)` gives `(6, 1)`. `b` is a single number that broadcasts across all six rows.

**B2.**

```python
import torch

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])
w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)

optimizer.zero_grad()
pred = hours @ w + b
loss = ((pred - marks) ** 2).mean()
loss.backward()
print("before step: w = %.4f   w.grad = %.4f   loss = %.4f"
      % (w.item(), w.grad.item(), loss.item()))
optimizer.step()
print("after  step: w = %.4f   w.grad = %.4f" % (w.item(), w.grad.item()))
```

```text
before step: w = 0.0000   w.grad = -326.6667   loss = 1786.6666
after  step: w = 16.3333   w.grad = -326.6667
```

**B2(a).** *`step()` moved `w` from 0 to 16.3333 and left `w.grad` sitting on exactly the same `−326.6667`, so it moves the weights and does not touch the slopes — which is why they have to be wiped by something else.*

**B3.**

```python
import torch

torch.manual_seed(0)
hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])
w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)

for step in range(400):
    optimizer.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    optimizer.step()

print("w = %.4f   b = %.4f   loss = %.6f" % (w.item(), b.item(), loss.item()))
```

```text
w = 8.0014   b = 11.9939   loss = 0.000007
```

**B4.**

```python
with torch.no_grad():
    pred = hours @ w + b
    gap = (pred - marks).abs().mean()
print("requires_grad", pred.requires_grad, " grad_fn", pred.grad_fn)
print("average miss %.4f marks" % gap.item())
```

```text
requires_grad False  grad_fn None
average miss 0.0023 marks
```

**B4(a).** Without `.abs()`, a prediction that is **2 too high** and one that is **2 too low** would cancel out, and a model that was wildly wrong in both directions could report an average miss of zero. **You want the *size* of each miss, not its direction.**

**B5.**

```python
"""b5w21.py - run the loop five ways and report one row each."""
import torch

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])


def fresh():
    torch.manual_seed(0)
    w = torch.tensor([[0.0]], requires_grad=True)
    b = torch.tensor([0.0], requires_grad=True)
    return w, b, torch.optim.SGD([w, b], lr=0.05)


def run(label, skip=None):
    w, b, opt = fresh()
    for step in range(400):
        if skip != "zero_grad":
            opt.zero_grad()
        pred = hours @ w + b
        loss = ((pred - marks) ** 2).mean()
        if skip != "backward":
            loss.backward()
        if skip != "step":
            opt.step()
    grad = "None" if w.grad is None else "%.4f" % w.grad.item()
    print("%-22s %12.4f %9.4f %9.4f %10s" % (label, loss.item(), w.item(), b.item(), grad))


print("%-22s %12s %9s %9s %10s" % ("run", "final loss", "w", "b", "w.grad"))
run("all five lines")
run("no zero_grad", skip="zero_grad")
run("no backward", skip="backward")
run("no step", skip="step")
```

```text
run                      final loss         w         b     w.grad
all five lines               0.0000    8.0014   11.9939     0.0005
no zero_grad              2907.9082    5.3946   18.9274  -247.1715
no backward               1786.6666    0.0000    0.0000       None
no step                   1786.6666    0.0000    0.0000  -326.6667
```

**Read the last two rows across.** Identical in every column except the last, where one says `None` and the other says `−326.6667`. **That single column is the whole diagnosis.**

**Why `fresh()` has to be a function:** because each run needs **brand-new knobs starting at zero and a brand-new optimizer holding them.** Make them once at the top and run 2 starts wherever run 1 finished, so every row after the first is measuring something meaningless.

### Fix the Broken Program

*Three bugs: dtype, runtime, silent logic. The step-0 hand check and Runs 1–4 were re-run and reproduce the printed logs exactly.*

**Bug 1 — line 6, `km = torch.tensor([[1], [2], [3], [4], [5]])`. A dtype bug.**

**`km` holds whole numbers**, so its dtype is `int64` — which PyTorch calls `long long` in this message. The missing character is the **`.0`** (or just the `.`) on each of the five values. `minutes` and `w` are decimals, so the multiply refuses.

**The fix:** `km = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]])`.

**Bug 2 — the traceback names line 16, `loss.backward()`, but the wrong line is line 15**, `loss = ((pred - minutes) ** 2)`. **The `.mean()` is missing.**

`loss` is holding **five** numbers, one per delivery, because `(pred - minutes) ** 2` squares each row separately and nothing collapses them.

**Why `backward()` needs one number:** *"how much does the loss change if I nudge this knob?"* only has an answer if there is **one** loss. Five losses is five different questions, and PyTorch will not guess which one you meant.

**The fix:** `loss = ((pred - minutes) ** 2).mean()`.

**Bug 3 — `optimizer.zero_grad()` is missing from the top of the loop. A silent logic bug.**

**The `dL/dw` column is wrong in two ways: the magnitudes do not shrink, and the sign keeps flipping.** In a healthy run the gradient falls steadily towards zero. −192.0, +209.3, −122.3, +193.3 are not slopes at all; they are **sums of every slope so far**, so `w` keeps being pushed by old slopes after it has passed the answer.

**`w` is thrashing** — 9.6, then −0.1, then 14.8, then −4.2. It is leaping past the answer and back again, never settling. It ends at `−4.2352` when the answer is 6.

**The missing line:** `optimizer.zero_grad()`, as the first line inside the loop.

**Step 0 by hand:**

```text
errors:        −16   −22   −28   −34   −40
squared sum:   256 + 484 + 784 + 1156 + 1600  =  4280
÷ 5:           856.0                     ← matches 856.0000  ✅

each error × its km:  −16, −44, −84, −136, −200   sum = −480
× 2 ÷ 5:                                −192.0    ← matches −192.0000  ✅
w ← 0 − 0.05 × (−192.0)               = +9.6      ← matches 9.6000     ✅
```

**Step 0 is identical in both runs**, because on the very first trip there is nothing in `.grad` to pile onto. **The bug only bites from step 1 onwards** — which is exactly why it survives so long. *(That is also the answer to the "byte-for-byte identical" question.)*

**Comparing the two `dL/dw` columns:** in Run 4 it **shrinks monotonically towards zero** (−192.0 → 0.0240 → 0.0008 → 0.0000), which is what arriving at the bottom of a valley looks like. In Run 3 it stays large and **changes sign**, which is what a pile looks like. **Run 4 is the healthy one.**

**Ranking: bug 3 ≫ bug 2 > bug 1.** Bugs 1 and 2 crash on the first trip and name the problem. Bug 3 costs the most because **it produces a running program with a plausible log.** The habit that catches it: **compare the first loss with the last loss, and read the gradient column.** Not *"is it going down"* — it went down between steps 0 and 200 in Run 3 too.

**Watch for:** Bug 2 located at "line 16" because that is what the traceback names. The traceback names where the error surfaced; the bug is on line 15.


### Puzzle of the Week

**Part 1 — the learning-rate boundary.** Real output, all five rows printed with the same formatting:

```text
lr 0.01  w   8.5199  b   9.7743  loss 0.960224
lr 0.05  w   8.0014  b  11.9939  loss 0.000007
lr 0.06  w   8.0003  b  11.9986  loss 0.000000
lr 0.07  w      nan  b      nan  loss nan
lr 0.10  w      nan  b      nan  loss nan
```

| `lr` | `w` | `b` | final loss | verdict |
|---|---|---|---|---|
| `0.01` | `8.5199` | `9.7743` | `0.960224` | too small |
| `0.05` | `8.0014` | `11.9939` | `0.000007` | about right |
| **`0.06`** | **`8.0003`** | **`11.9986`** | **`0.000000`** | **about right — very slightly better** |
| **`0.07`** | **`nan`** | **`nan`** | **`nan`** | **too big — dead** |
| `0.1` | `nan` | `nan` | `nan` | too big — dead |

*(The `0.06` loss is not truly zero — it is about four ten-millionths, and `%.6f` has run out of places to show it. **A printed `0.000000` is a formatting limit, not a fact.**)*

**Part 1(a).** **Between `0.06` and `0.07`.** There is no single "right" number; there is a cliff, and it is very close to a value that works beautifully.

**Part 1(b).** **A model answer.** *For the optimizer:* `SGD` takes a fixed step of `lr × slope`, with no memory and no adaptation, so how big a step is safe is entirely determined by that one number. *For the data:* the slopes themselves come from the data — our `dL/dw` starts at `−326.6667` because the marks run up to 60 and the hours up to 6. The cliff comes from the inputs: a nudge to `w` changes each prediction by `hours × nudge`, so with hours up to 6 a step that is too big gets amplified up to 6 times. Squash the hours down (say to 0.1–0.6) and the same `lr` would be perfectly safe. (Scaling the *marks* down would shrink the first slopes but would **not** move the cliff: `lr = 0.1` still gives `nan` with marks divided by 10.) **It is both**, and the honest conclusion is that a learning rate is not a property of an algorithm — it is a property of an algorithm **and** the numbers you feed it. That is exactly why Week 15 made you hunt for one instead of giving you a rule, and why Week 4's scaling lesson matters even when the model does not care about scale.

**Part 1(c).** **Run it for longer.** `lr = 0.01` is walking in the right direction and simply has not arrived; a few thousand more steps would get there. **The cost is time** — and on a real model that is hours or days of computing, which is why nobody just turns the learning rate down and waits.

**Part 1(d).** **You watch a curve.** Try a few values that differ by roughly a factor of three (0.001, 0.003, 0.01, 0.03, 0.1), plot the loss for the first fifty steps of each, and pick the largest one whose loss is falling smoothly rather than jumping. **And you check the first four steps, not the last one**, because divergence is visible immediately and `nan` tells you nothing about the cause. There is no formula, and pretending otherwise would be dishonest.

**Part 2 — the Order Puzzle.**

| # | order | verdict | correct? |
|---|---|---|---|
| 1 | Z F L B S | **learns** | **yes** — this is the canonical loop |
| 2 | F L B S Z | **learns** | **yes** — `zero_grad` at the end works |
| 3 | Z F L S B | **runs and learns nothing** | no — and **no error at all** |
| 4 | Z B F L S | **crashes on the first line it reaches** | — there is no `loss` yet to walk back from |
| 5 | F L Z B S | **learns** | **yes** — the wipe still happens before `backward()` |

Real output, all four of the non-canonical orders run for 400 steps:

```text
2 F L B S Z -> w 8.0014  b 11.9939  loss 0.000007  w.grad None
3 Z F L S B -> w 0.0000  b 0.0000  loss 1786.666626  w.grad -326.6667
4 Z B F L S -> UnboundLocalError: local variable 'loss' referenced before assignment
5 F L Z B S -> w 8.0014  b 11.9939  loss 0.000007  w.grad 0.0005
```

**Orders 2 and 5 land on exactly the same `8.0014` and `11.9939` as the canonical order** — all three are genuinely correct loops. Order 4's message is Python's, not PyTorch's: you asked to differentiate a variable that does not exist yet. *(Written at the top level of a file rather than inside a function, the same mistake says `NameError: name 'loss' is not defined`.)*

**Part 2(a).** **Number 2 works because `zero_grad` only has to happen once per trip, before the next `backward()`.** Wiping at the *end* of trip 1 leaves the box empty at the start of trip 2, which is exactly what wiping at the *start* of trip 2 would have achieved.

**We still write it first because of the first iteration.** With the wipe at the end, you have to stop and reason: *"is `.grad` clean on the very first trip?"* (It is — it starts as `None`.) With the wipe at the front, that question never arises. **The order that requires no reasoning is the order to write.**

**Part 2(b).** Trip by trip:

1. `zero_grad()` — `w.grad` becomes `None`.
2. forward and loss — fine, a real prediction and a real number.
3. `step()` — **the optimizer looks for a gradient and there is nothing there**, so it skips `w` and `b` entirely. `w` does not move.
4. `backward()` — fills `w.grad` with a perfectly correct `−326.6667`.
5. Next trip begins with `zero_grad()`, which **throws that gradient away before anything uses it.**

So every trip computes the right slope, one line too late, and discards it. **400 steps, `w = 0.0000`, `w.grad = −326.6667`, and no error whatsoever.** Note that this is indistinguishable from a missing `step()` by looking at the log — the tell is reading the code.

**Part 2(c).** **Number 4**, the crash, without hesitation. It stops immediately and tells you what is wrong. **Number 3 is the one to fear**: it runs, it looks fine, and it wastes however long it takes you to notice that `w` has not moved.

### Think Deeper

*Open answers. Mark against the points named, not the wording.*

**T1 — a model answer.** Take them one at a time. **A missing `step()`:** a library *could* detect this. It knows gradients were computed, and it could warn if `.grad` is overwritten without any parameter having changed. Nobody does, but it is possible. **A missing `backward()`:** also detectable — `step()` could notice that every gradient it was asked to apply is `None` and say so. Arguably it should. **A missing `zero_grad()`:** this one genuinely cannot be detected, because accumulating is sometimes exactly what you asked for — that is the whole point of the default — and the library cannot know whether four backwards were four pieces of one batch or four mistakes.

So the honest verdict is: two of the three are missed opportunities, and one is unavoidable. And the general lesson is bigger than PyTorch: **in this subject the failures that matter usually do not raise errors.** What I will check every run: **the first loss against the last loss**, and **the gradient column shrinking rather than growing.** Two habits, thirty seconds, and they catch all three.

**T2 — a model answer.** **You cannot tell**, and that is the whole answer. A loss of `0.000007` on the data you trained on tells you the model fits those six points; it says nothing about whether it would work on a seventh student. In this particular case we happen to know it is a good model, but **not because of the loss** — because we hid `8x + 12` in the data ourselves and can see it found it. **Take that knowledge away and `0.000007` is uninterpretable.**

What I would need is **data the model has not learned from.** A seventh student who revised for 7 hours: the model predicts `8.0014 × 7 + 11.9939 = 68.0037`, and the real line says 68. That comparison is a measurement; the training loss is not.

And when the data does **not** sit on a line, the loss will **stop falling at some non-zero number**, and that leftover is the part of the data no straight line can explain. Our wobbled pizza example bottomed out at `0.560000` and stayed there — nothing broken, just an honest limit. **A loss that reaches zero on real data is more likely to be a warning than a triumph.**

### Build It — Fit the Hidden Line, Then Break It Five Ways

#### Part A — fit the line

*The predicted step-0 row comes from M1–M3: loss `1786.6666`, `w` `16.3333`, `dL/dw` `−326.6667`. The complete `fit_line.py` is in the Prep Checklist.* Real output:

```text
step   0  loss  1786.6666  w 16.3333  b  4.0000  dL/dw  -326.6667
step  50  loss     2.8163  w  8.8773  b  8.2442  dL/dw     0.3261
step 100  loss     0.4466  w  8.3493  b 10.5044  dL/dw     0.1299
step 150  loss     0.0708  w  8.1391  b 11.4044  dL/dw     0.0517
step 200  loss     0.0112  w  8.0554  b 11.7628  dL/dw     0.0206
step 250  loss     0.0018  w  8.0221  b 11.9056  dL/dw     0.0082
step 300  loss     0.0003  w  8.0088  b 11.9624  dL/dw     0.0033
step 350  loss     0.0000  w  8.0035  b 11.9850  dL/dw     0.0013
step 399  loss     0.0000  w  8.0014  b 11.9939  dL/dw     0.0005

found:  marks = 8.0014 x hours + 11.9939
wanted: marks = 8 x hours + 12
```

**The answer to report: `w = 8.0014`, `b = 11.9939`, against the hidden line `8x + 12`.** Accept anything above `w = 7.99` and `b = 11.9`.

**The three questions to read off the log:**

1. The `dL/dw` column **shrinks steadily, from −326.6667 to 0.0005.** A flattening slope means arrival — Week 12's picture, seen from inside a loop.
2. **`w` is closer** at step 50 (8.88 against 8; `b` is 8.24 against 12), because `w`'s slope started at −326.7 and `b`'s at −80, so `w` moves about four times as fast.
3. **No; it never reaches exactly 8 and 12.** Each step is proportional to the remaining slope, so the steps shrink as you approach.

**Three things worth a comment when you mark:**

1. **`w` arrives before `b`**, for the reason above.
2. **The gradient shrinking to 0.0005** is the sign of arrival.
3. **It never reaches 8 and 12**, and it never will.

#### Part B — the five-row table

The complete file:

```python
"""drop_a_line.py - delete each of the five lines and see what happens."""
import traceback
import torch

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])


def fresh():
    torch.manual_seed(0)
    w = torch.tensor([[0.0]], requires_grad=True)
    b = torch.tensor([0.0], requires_grad=True)
    return w, b, torch.optim.SGD([w, b], lr=0.05)


print("### 0. all five lines present")
w, b, opt = fresh()
for step in range(400):
    opt.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    opt.step()
print("w %.4f  b %.4f  loss %.6f" % (w.item(), b.item(), loss.item()))

print()
print("### 1. no optimizer.zero_grad()")
w, b, opt = fresh()
for step in range(400):
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    opt.step()
    if step in (0, 1, 2, 3, 399):
        print("  step %3d  loss %12.4f  dL/dw %14.4f  w %10.4f"
              % (step, loss.item(), w.grad.item(), w.item()))
print("w %.4f  b %.4f  loss %.6f" % (w.item(), b.item(), loss.item()))

print()
print("### 2. no forward line (pred computed once, before the loop)")
w, b, opt = fresh()
pred = hours @ w + b
try:
    for step in range(400):
        opt.zero_grad()
        loss = ((pred - marks) ** 2).mean()
        loss.backward()
        opt.step()
        print("  step %d finished, loss %.4f" % (step, loss.item()))
except RuntimeError:
    traceback.print_exc()

print()
print("### 3. no loss line (loss computed once, before the loop)")
w, b, opt = fresh()
loss = ((hours @ w + b - marks) ** 2).mean()
try:
    for step in range(400):
        opt.zero_grad()
        pred = hours @ w + b
        loss.backward()
        opt.step()
        print("  step %d finished, loss %.4f" % (step, loss.item()))
except RuntimeError:
    traceback.print_exc()

print()
print("### 4. no loss.backward()")
w, b, opt = fresh()
for step in range(400):
    opt.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    opt.step()
print("w %.4f  b %.4f  loss %.6f  w.grad %s"
      % (w.item(), b.item(), loss.item(), w.grad))

print()
print("### 5. no optimizer.step()")
w, b, opt = fresh()
for step in range(400):
    opt.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
print("w %.4f  b %.4f  loss %.6f  dL/dw %.4f"
      % (w.item(), b.item(), loss.item(), w.grad.item()))
```

Real output, runtime under 2 seconds (the two tracebacks arrive on the error stream, so on your screen they may appear before the headings — that is normal):

```text
### 0. all five lines present
w 8.0014  b 11.9939  loss 0.000007

### 1. no optimizer.zero_grad()
  step   0  loss    1786.6666  dL/dw      -326.6667  w    16.3333
  step   1  loss     650.5742  dL/dw      -129.8889  w    22.8278
  step   2  loss    2737.1262  dL/dw       277.0704  w     8.9743
  step   3  loss      31.9444  dL/dw       244.9432  w    -3.2729
  step 399  loss    2907.9082  dL/dw      -247.1715  w     5.3946
w 5.3946  b 18.9274  loss 2907.908203

### 2. no forward line (pred computed once, before the loop)
  step 0 finished, loss 1786.6666
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.

### 3. no loss line (loss computed once, before the loop)
  step 0 finished, loss 1786.6666
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.

### 4. no loss.backward()
w 0.0000  b 0.0000  loss 1786.666626  w.grad None

### 5. no optimizer.step()
w 0.0000  b 0.0000  loss 1786.666626  dL/dw -326.6667
```

**The five-row table, filled in:**

| Line removed | Error? | What happened | The tell |
|---|---|---|---|
| `optimizer.zero_grad()` | **No error** | Loss 1786.6666 → **2907.9082** after 400 steps. `w = 5.3946`, `b = 18.9274`. Worse than it started. | The gradient column **never shrinks and flips sign**: −326.7, −129.9, +277.1, +244.9. Those are piles, not slopes. |
| `pred = hours @ w + b` | **RuntimeError** | Completes step 0, crashes on step 1: *"Trying to backward through the graph a second time"*. | It worked once. The graph was freed when it was read. |
| `loss = ((pred - marks) ** 2).mean()` | **RuntimeError** | Identical failure and identical message. | The loss and the forward pass are one thing; both belong inside the loop. |
| `loss.backward()` | **No error** | 400 steps, `w` and `b` never leave `0.0000`, loss stuck at `1786.666626`. | **`w.grad` is `None`** — no backward pass ever ran. |
| `optimizer.step()` | **No error** | 400 steps, `w` and `b` never leave `0.0000`, loss stuck at `1786.666626`. | **`w.grad` is `−326.6667`** — the slope was computed and never used. |

**Three of the five rows say "no error".** That is the objective, and a table with fewer than three has probably conflated something.

**The `zero_grad` sentence (the one being marked):** *"The gradients added up instead of being wiped, so each step carried every old slope along with it, so it kept overshooting the bottom and ended up worse than it started — 1786.6666 at step 0 and 2907.9082 at step 399."* **Accept nothing that does not name accumulation and use both numbers.**

**The separating question for the last two rows:** what does `w.grad` say? `None` in the no-`backward` run; `−326.6667` in the no-`step` run.

**How many rows say "no error"?** Three. **How many predictions were right** is the student's own count; it is not marked, but a count of 5 / 5 is suspicious (see the marking note above).

#### Part C — `no_grad`, once

The complete file:

```python
"""measure.py - measuring is not learning, so turn the recorder off."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

torch.manual_seed(0)

hours = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
marks = torch.tensor([[20.0], [28.0], [36.0], [44.0], [52.0], [60.0]])

w = torch.tensor([[0.0]], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)
optimizer = torch.optim.SGD([w, b], lr=0.05)

history = []
for step in range(400):
    optimizer.zero_grad()
    pred = hours @ w + b
    loss = ((pred - marks) ** 2).mean()
    loss.backward()
    optimizer.step()
    history.append(loss.item())

print("first loss %.4f   last loss %.6f" % (history[0], history[-1]))

pred_recorded = hours @ w + b
print()
print("measuring WITH the recorder on:")
print("  requires_grad:", pred_recorded.requires_grad,
      "  grad_fn:", type(pred_recorded.grad_fn).__name__)

with torch.no_grad():
    pred_quiet = hours @ w + b
    gap = (pred_quiet - marks).abs().mean()
print("measuring with torch.no_grad():")
print("  requires_grad:", pred_quiet.requires_grad, "  grad_fn:", pred_quiet.grad_fn)
print("  average miss: %.4f marks" % gap.item())

print()
print("predictions after training:")
with torch.no_grad():
    for i in range(6):
        print("  %d hours -> predicted %7.4f   real %5.1f"
              % (hours[i].item(), (hours[i] @ w + b).item(), marks[i].item()))

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(history)
ax.set_yscale("log")
ax.set_xlabel("step")
ax.set_ylabel("loss (log scale)")
ax.set_title("400 steps of the five-line loop")
plt.tight_layout()
plt.savefig("loss_curve.png", dpi=120)
print()
print("wrote loss_curve.png")
print("loss at steps 0, 100, 200, 300, 399: %.4f %.4f %.4f %.4f %.6f"
      % (history[0], history[100], history[200], history[300], history[399]))
```

Real output:

```text
first loss 1786.6666   last loss 0.000007

measuring WITH the recorder on:
  requires_grad: True   grad_fn: AddBackward0
measuring with torch.no_grad():
  requires_grad: False   grad_fn: None
  average miss: 0.0023 marks

predictions after training:
  1 hours -> predicted 19.9953   real  20.0
  2 hours -> predicted 27.9968   real  28.0
  3 hours -> predicted 35.9982   real  36.0
  4 hours -> predicted 43.9996   real  44.0
  5 hours -> predicted 52.0010   real  52.0
  6 hours -> predicted 60.0024   real  60.0

wrote loss_curve.png
loss at steps 0, 100, 200, 300, 399: 1786.6666 0.4466 0.0112 0.0003 0.000007
```

| | `requires_grad` | `grad_fn` |
|---|---|---|
| recorder on | `True` | `AddBackward0` |
| inside `no_grad()` | `False` | `None` |

**The average miss: 0.0023 marks.** **The two numbers are identical** — `no_grad` changes nothing about the arithmetic. What it saves is the storage of every intermediate value that would have been needed for a backward pass that is never going to happen.

**What to look for:** `requires_grad: True` and a `grad_fn` outside the block, `False` and `None` inside it. **That contrast is the whole answer** — with the recorder off, nothing is stored for a backward pass that will never happen.

**And the six predictions are worth reading out**: 19.9953 for 20, 60.0024 for 60. **The average miss is 0.0023 of a mark.**

#### Stretch — the learning-rate sweep

*Run the same loop for 400 steps at `lr = 0.01`, `0.05` and `0.1`. Report `w`, `b` and the final loss.*

```text
lr 0.01 after 400: w 8.519876480102539 b 9.774307250976562 loss 0.960224449634552
lr 0.05 after 400: w 8.001418113708496 b 11.993927955627441 loss 7.36106994736474e-06
lr 0.10 after 400: w nan b nan loss nan
```

| learning rate | `w` | `b` | final loss | diagnosis |
|---|---|---|---|---|
| `0.01` | `8.5199` | `9.7743` | `0.960224` | **too small** — right direction, not finished. More steps would get there. |
| `0.05` | `8.0014` | `11.9939` | `0.000007` | **about right** |
| `0.1` | `nan` | `nan` | `nan` | **too big** — diverged and died |

**And the first four steps at `lr = 0.1`, which is the part that teaches:**

```text
  step  0 loss 1786.6666259765625 w 32.66666793823242
  step  1 loss 8553.408203125 w -39.355560302734375
  step  2 loss 41215.35546875 w 118.61631774902344
  step  3 loss 198849.859375 w -228.6627655029297
  step  4 loss 959614.3125 w 534.0220336914062
  step 19 loss 1.7220197853167616e+16 w -70216040.0
```

**The two sentences to look for:**

1. *"At 0.1 the signs of `w` alternate — 32.7, −39.4, +118.6, −228.7 — so it is jumping over the bottom of the valley and landing higher each time."*
2. *"These are Week 15's three panels: too small crawls, about right walks down, too big leaps and climbs. The only difference is that `optimizer.step()` is doing the stepping."*

**The honest extra note, worth full credit:** the boundary is somewhere between 0.06 (works, `w = 8.0003`) and 0.07 (`nan`), and it depends on the data as much as on the code — which is why there is no universal "right" learning rate and why Week 15 made them hunt for one.

#### The Bug Log

No fixed answer; any two real entries. Two model entries, both reproduced above:

| What I saw | What it means | Cause | Fix |
|---|---|---|---|
| `RuntimeError: Trying to backward through the graph a second time ...` | The graph was freed by the first `backward()` and the loop tried to use it again | `pred` (or `loss`) computed once, above the `for` line | Put the forward and loss lines inside the loop |
| **No message.** Loss went 1786.6666 → 2907.9082 and the `dL/dw` column flipped sign | Gradients were piling up | `optimizer.zero_grad()` missing | `optimizer.zero_grad()` as the first line of the loop |


### Draw It

**A good drawing has:** five stations round the circle, **numbered 1 to 5**; arrows going **one way only**; a box labelled `w.grad` that is **emptied at station 1 and filled at station 4**; a box labelled `w` that **only station 5 touches**; the step-0 numbers written on the relevant stations — `loss 1786.6666` at station 3, `−326.6667` at station 4, and `0 → 16.3333` at station 5; and a mark showing which stations can be dropped silently.

**The four questions.** **Station 1 empties `w.grad`; station 4 fills it.** **Station 5 is the only one that touches `w`.** `−326.6667` belongs on station 4 (or on the arrow out of it); `16.3333` belongs on station 5. **The three stations that can be removed with no error are 1, 4 and 5** — `zero_grad`, `backward` and `step`. Stations 2 and 3 both crash.

### Self-Check

No right answers here, but the honest bar: 😀 means you could do it now on blank paper with nothing open. 🙂 means you could do it with your chapter beside you. 😕 is the one to ask about first — and make sure **"name the three failures that produce no error"** is not a 😕, because from Week 22 onwards the models get big enough that reading a log carefully is the only debugging tool you have left.

---

### Answers to every question posed in the lesson

**Hook — "Can anyone see the line hiding in the six points?"**
`marks = 8 × hours + 12`. Every extra hour adds 8 marks; at 0 hours the line would sit at 12.

**Concept — "Which of the five cannot possibly go first?"**
`loss.backward()` — it needs a loss to exist. Then the loss needs a prediction, so the forward line precedes it, and `step()` follows `backward()`.

**Concept — "Where does `zero_grad` go, and why?"**
First, because `backward()` **adds** into `.grad` (`6 + 27 = 33`, from last week). Putting it at the end also works if it happens once per trip; putting it first means you never have to reason about the first iteration.

**Concept — "Now the slope for `w`. What do you multiply each error by?"**
The input that `w` multiplies — the hours. `(−20 × 1) + (−28 × 2) + … + (−60 × 6) = −980`, then `2 × (−980) ÷ 6 = −326.6667`.

**Concept — "A negative slope. What does that tell us to do to `w`?"**
Increase it: `w ← 0 − 0.05 × (−326.6667) = +16.3333`.

**Concept — "Four backwards, same data. What will the four numbers be?"**
`−326.6667`, `−653.3334`, `−980.0001`, `−1306.6667`. **`4 × 326.6667 = 1306.6668`.**

**Live-code — "It wants an *iterable of Tensors*. What is it complaining about?"**
The optimizer takes a **list** of knobs. `SGD([w, b], lr=0.05)`, not `SGD(w, lr=0.05)`.

**Live-code — "Read the `dL/dw` column. What is happening, and what does it mean?"**
It shrinks from −326.6667 to 0.0005. **A flattening slope means you are arriving at the bottom.** Week 12's picture, from inside the loop.

**Live-code — "Did it crash at `lr = 0.1`? And what is `nan`?"**
No crash. `nan` is "not a number". The loss first overflows to `inf` (step 51), and `inf` minus `inf` has no answer, which is `nan`. It is contagious: once one weight is `nan`, everything downstream is `nan` for ever.

**Activity — "How would you know, from the log alone, that `backward` was the missing line?"**
`w.grad` is `None`. If `step()` were the missing one, `w.grad` would hold `−326.6667` instead.

**Wrap — "How many of the five failures produce no error?"**
**Three:** missing `zero_grad`, missing `backward`, missing `step`. The other two — a stale forward pass and a stale loss — both raise *"Trying to backward through the graph a second time"*.

---

## 🔮 Next Week Preview

Next week the knobs stop being tensors you typed. The student meets **`nn.Linear`** — one object that holds a whole layer's weights and biases, hands them all to the optimizer in one call, and does the grid multiply when you call it — plus `nn.ReLU`, `nn.Sequential` for stacking them, and `nn.BCEWithLogitsLoss`, which applies the sigmoid for you and does it in a numerically safe way. The task is to rebuild **Week 19's exact 2 → 16 → 1 network** in four lines and prove the parameter shapes are identical to the ones they built by hand. Then the second half, which is the real content: two loss curves on the same axes, training and validation, and the epoch where the validation curve stops improving marked with a vertical line. **And the five lines from today do not change at all** — that is the claim to make out loud when `nn.Sequential` appears, because it is what makes today worth having spent a whole lesson on.

**To prep early:** leave the five cards on the wall — next week points at them and says "unchanged" — and keep this week's `w = 8.0014, b = 11.9939` result somewhere visible, because next week's first exercise is the same fit with `nn.Linear(1, 1)` in place of the two hand-typed tensors, and the numbers should land in the same place. You will also want Week 19's parameter count (`2 × 16 + 16 + 16 × 1 + 1 = 65`) to hand, because `sum(p.numel() for p in model.parameters())` has to agree with it. Nothing new to install.
