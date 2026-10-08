# Week 9 — Review and Assessment 1: What Did Eight Weeks Leave Behind?

[⬅ Week 8](week-08.md) · [Course Home](../README.md) · [Week 10 ➡](week-10.md) · [Student Guide](../student-guide/week-09.md) · [Workbook](../workbook/week-09.md)

---

![Map of the 36 weeks with Week 9, Review and Assessment 1, highlighted at the end of the first eight weeks](../figures/fig-w09-0-where-this-fits.svg)
*Figure 9.0 — Week 9 is the first review: an X-ray of Weeks 1 to 8 before Term 2 builds on them.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 75 minutes in class (2 to settle, 70 for the paper, 3 to hand in), then the marking homework (~45 min) |
| **Type** | 🟥 Assessment — **no new material at all.** Weeks 1-8 on paper, no computer. |
| **Big idea** | The paper is not a grade; it is a **map**. It finds, week by week, what stuck and what did not, so that the per-week remediation table (below) tells the student exactly which page to redo *before* Term 2 builds on it. Weeks 10-13 lean on Weeks 2, 6 and 8 directly. |
| **New vocabulary** | **None.** (If you catch yourself teaching a word today, stop: it is not in the paper.) |
| **New maths** | **None.** The paper *tests* the four hand-calculable ideas of Term 1 — the running average (W2), the root-mean-square (W3), the slope of a sum (W6), and the four-step cell unroll (W8) — plus "is the gap bigger than the spread" (W7). Each is in the 🔢 section below, worked for you first. |
| **New syntax** | **None.** Every line of code on the paper uses a construct from Weeks 1-8, listed in section 4. |
| **The paper** | 75 marks. **A** 20 multiple choice (1 each) · **B** 8 "what does this print" (2 each) · **C** 4 "find the bug" (3 each) · **D** 3 arithmetic (5 each) · **E** 1 extended question on real loss curves (12). Printed in full in [The Paper, in Full](#-the-paper-in-full) below; the key is at the bottom. |
| **Dataset** | The same generated spirals (`make_spirals`, seed 0: 840 train / 360 validation) — but **only in Question E, as printed numbers.** The student runs nothing. **Nothing downloads. No internet.** |
| **Model** | Real PyTorch on the CPU, used by *you* in the prep to produce the Section E tables. **There is no language model and no stand-in anywhere in this week.** |
| **Materials** | The printed paper (one copy, single-sided) · the printed **marking sheet** (short answers only — the one page you may hand over afterwards) · a pen · a calculator (phone in calculator mode is fine; **airplane mode on**) · scrap paper · a timer · the remediation table (Handout C) |
| **Prep time** | 25 minutes the night before (mostly printing and reading the key) · 3 minutes on the day |
| **Expected runtime of the code** | Every block in the prep finishes in **under a second**, except the Section E table (16 training runs, about **10 seconds** on the author's CPU). Anything over **60 seconds** means something is wrong (see Fallback). The *student* runs no code today. |

> **⚠️ Watch out:** the thing that goes wrong this week is **the teacher rescuing the student mid-paper.** A student who sees a frown from you at question 7 will change an answer that was right. Your job for 70 minutes is to be a quiet adult in a chair.
>
> The second thing that goes wrong is **marking by the final number only**. A wrong number with the right working earns most of the marks, and a right number with no working earns fewer (see the marking rules in 📤 and the key). The value of the paper is the *pattern* of lost marks, not the total.

---

## 🎯 Lesson Objectives

By the end of the lesson the student has, **with no computer and no notes:**

1. **Read a loss curve** from a printed table and name its symptom in one plain sentence with a number from the table (flat · slow but learning · blew up then stuck · learned then collapsed).
2. **Do an optimizer step by hand** — three steps of SGD and of PyTorch-style momentum on `f(w) = w²` — and compute the first Adam step.
3. **Name which normalisation fails at a batch of one** and say why, in one sentence.
4. **Unroll a three-step recurrent cell** with given weights, and say why the same inputs in a different order give a different final note.
5. **Decide whether a gap between two runs is bigger than the spread**, using the twice-the-spread rule from Week 7.

Observable evidence: a scored paper; a filled **per-week mark grid** (Handout B of the key); and, most important, **a remediation table with at most two weeks circled** for the student to redo during the following fortnight.

---

## 🧑‍🏫 What YOU Need to Know First

This section is your own preparation. Read it before class: it says what the student does, works every hand calculation for you, and lists what to expect on the paper.

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist**, in the **🐞 Debugging Clinic** and in the **🔑 Answer Key** was run, in order, from one folder (`36-week-course/`), on a CPU, with one thread and the seeds shown; the outputs below are the real printed output. The Clinic blocks that are *deliberate mistakes* are marked and their tracebacks are real. The copies of the code that appear **inside the paper** are the very same text as the blocks the key runs. **Timing lines vary run to run; every other number repeated exactly on a second full run on the same machine.** Different CPU or PyTorch build: the last digit of a loss can move. **The loss tables that go on the paper are printed numbers, so they do not depend on your laptop at all** — print them, do not re-generate them on the day.

### 1. What the student is doing today, in one paragraph

Nothing new. For 70 minutes the student answers a paper about the last eight weeks: twenty multiple-choice questions (one each), eight short programs whose output they must say, four short programs with a bug they must find and fix, three pieces of arithmetic (a two-optimizer hand table, a root-mean-square and a first Adam step, a three-step cell unroll), and one longer question built on **real loss curves and a real three-seed table printed from this course's own spirals harness**. They may use a calculator. They may not use a computer, notes, or you. Afterwards they are handed the *marking sheet*, mark their own paper in a different colour of pen as homework, fill the per-week grid, and circle the (at most two) weeks to redo.

Why on paper? Because the standard of the whole term — *you can say what a program will print before you run it* — is best tested with the laptop closed. Why self-marking? Because the act of comparing their own working to the sheet is the best 45 minutes of review on offer, and it is why the marking sheet has *working* on it and not just answers.

### 2. 🔢 The maths you need — taught to you first

**There is no new idea.** But you will mark five hand-calculations, so do each of these yourself, once, with a calculator, *before* class. They are the same ones the student did in the week shown.

**(a) The running average (Week 2) — and the "×10" trap.** PyTorch's `momentum=0.9` keeps a velocity `v = 0.9 × v + g` (**no `0.1`**) and moves the weight by `lr × v`. The *average* form, `0.9 × old + 0.1 × new`, is a tenth of it. Question D1 uses the **PyTorch form**, on `f(w) = w²` from `w = 2.0`, `lr = 0.1`, gradient `2w`:

**Plain SGD** (`w ← w − 0.1·g`):

| Step | w before | g = 2w | step = 0.1·g | w after |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 2.0000 | 4.0000 | 0.4000 | **1.6000** |
| 2 | 1.6000 | 3.2000 | 0.3200 | **1.2800** |
| 3 | 1.2800 | 2.5600 | 0.2560 | **1.0240** |

**Momentum** (`v ← 0.9·v + g`, then `w ← w − 0.1·v`; `v` starts at 0):

| Step | w before | g = 2w | v = 0.9·v + g | step = 0.1·v | w after |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 2.0000 | 4.0000 | 0.9×0 + 4.0 = **4.0000** | 0.4000 | **1.6000** |
| 2 | 1.6000 | 3.2000 | 0.9×4.0 + 3.2 = **6.8000** | 0.6800 | **0.9200** |
| 3 | 0.9200 | 1.8400 | 0.9×6.8 + 1.84 = **7.9600** | 0.7960 | **0.1240** |

The two rules agree after step 1 because the velocity starts at 0; they part at step 2. `key.py` in the prep checks all six numbers against `torch.optim`.

**(b) Root-mean-square (Week 3).** "The typical size, ignoring sign": square each number, average the squares, take the square root. `[3, -4]` → squares `9, 16` → mean `12.5` → root **3.5355**. (Not the mean, `-0.5`. Not the length, `5`. Not `12.5`: that is the step before the root — a very common slip.) The same recipe on `[6, -8]`: squares `36, 64`, mean `50`, root **7.0711**.

**(c) Adam's first step (Week 3).** The first step moves a weight by `lr × g / (typical size of g + tiny epsilon)`. After one gradient the "typical size" is just `|g|`, so the step is `lr × (±1)` = **`lr`, whatever the size of `g`** — to within epsilon. Gradient 6, `lr = 0.01`: step `0.01`. Gradient 6000: step `0.01`. (The sign follows the gradient's sign: a positive gradient moves the weight *down*.) Do **not** bring in bias-correction words on the paper; the key defines the step in one line.

**(d) The slope of a sum (Week 6).** For `y = x + f(x)` the slope is "1, plus whatever `f` does". If `f` has slope `0.3` there, `y` has slope **1.3**. The student met it by *nudging*: compute `y` at `x` and at `x + 0.001`, divide the change by `0.001`. Question A16 and the clinic need nothing more than that.

**(e) The four-step cell (Week 8) — here three steps.** `new note = tanh( 1.0 × x + 0.5 × old note )`, start note `0`. Inputs `x = [0, 1, 1]`:

| Step | x | 1.0·x + 0.5·(old note) | new note = tanh of that |
|:--:|:--:|---|---|
| 1 | 0 | 0 + 0.5×0 = **0.0000** | tanh(0.0000) = **0.0000** |
| 2 | 1 | 1 + 0.5×0.0000 = **1.0000** | tanh(1.0000) = **0.7616** |
| 3 | 1 | 1 + 0.5×0.7616 = **1.3808** | tanh(1.3808) = **0.8811** |

And the same inputs in the order `x = [1, 1, 0]`: notes `0.7616, 0.8811, 0.4141` (the last: `0 + 0.5 × 0.8811 = 0.4405`, `tanh = 0.4141`). The inputs add up to **2** both times — a bag would call them the same — and the final notes are `0.8811` and `0.4141`. `key.py` checks all of these against `nn.RNN`.

**(f) "Is the gap bigger than the spread?" (Week 7).** `gap = |mean A − mean B|`, `spread = larger of the two SDs` (divide-by-`n`, `ddof=0`). Verdict: **inside noise** if `gap < 2 × spread`. Question A18 and E(b) use it. It is a *screening rule we chose*, not a statistical test (Week 7 said so, and so should you).

> **🚫 What you must NOT do with any of these today.** Do not teach a shortcut on the day. Do not say "remember the trick". If a student asks what `tanh(1.3808)` is, they have a calculator; if they do not know what `tanh` is, that is a finding for the grid, not a thing to fix at minute 31.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| Every loss, accuracy and seed-table number on the paper (Section E) | **Real.** Printed by `l4lib.spirals.run` on a CPU, one thread, seeds shown. Reproduced by the prep. |
| Every "what does this print" output (Section B) and every traceback (Section C, Clinic) | **Real.** Produced by running the code below. |
| The hand-arithmetic answers (Section D) | **Computed twice:** by hand in section 2, and by `torch.optim` / `nn.RNN` in `key.py`. They agree. |
| The weights `W_xh = 1.0`, `W_hh = 0.5` in D3 | **Chosen by us** so arithmetic is easy. Not learned. |
| Any language model, scripted client or `FakeClient` | **Not present.** The scripted backend first appears in Week 23. |
| The pass mark (45 of 75) | **A proposal.** The README leaves the pass mark and remediation content to the owner (Open Questions). Change it if the owner has decided otherwise; nothing in this file depends on 45. |

> **Say to the student, out loud, before they start:** *"Everything on this paper is something you have already done with your own hands. It is not a race and it is not a grade. It is an X-ray. If a question looks strange, read it twice, write down what you do know, and move on."*

### 4. The constructs the paper uses — all old, none new

Nothing is new this week. For your reference, here is **every** construct the paper leans on and the week it came from, so you can check "nothing is used before its week" at a glance:

| Week | Construct on the paper | Where |
|:--:|---|---|
| 1 | keyword-only `*` in `def run(*, lr, epochs)` · `math.log` (Level 2) | B1, C1 |
| 2 | `SGD(momentum=0.9)` *(described in words, never called)* | A3-A5, D1 |
| 3 | `torch.sqrt` · `Tensor.mean()` · `torch.tensor` | B3 |
| 4 | `LambdaLR` · `lambda s: ...` · `scheduler.step()` · `get_last_lr()` | A9-A11, B4 |
| 5 | `nn.Dropout(p)` · `copy.deepcopy` · eval mode | A12-A14, B5, C2 |
| 6 | `nn.BatchNorm1d` · `clip_grad_norm_` | A15-A17, B6, C3 |
| 7 | `itertools.product` · mean ± spread | A18, B7, E |
| 8 | `nn.Embedding` · `nn.RNN(batch_first=True)` · `out, h_n = rnn(x)` | A19-A20, B8, C4, D3 |

**Teacher-only code.** The prep blocks below use `nn.Parameter` and assign `.grad` by hand (the paper's code does not): they are for *you* and are not on the student's ladder. `torch.randn` is also avoided on the paper for the same reason (Week 10).

Not on the paper, on purpose, because they are later rungs: `retain_grad`, `torch.stack` (Week 10), LSTM and GRU (Week 11), `F.cross_entropy`, `torch.cat` (Week 12), `F.softmax`, `torch.multinomial` (Week 13), attention (Week 14). **If a student writes "vanishing gradient" or "LSTM" anywhere, do not mark it wrong and do not mark it extra; it is from next term.** Say so kindly on the sheet.

### 5. What the numbers will say

These are printed by the prep blocks. Read them before class so nothing surprises you.

- **Section E, the four curves (P, Q, R, S).** All four use the Week 1 harness with AdamW, 60 epochs, seed 0, and differ only in `lr`: `3e-6, 3e-4, 0.3, 3e-2`. **P** never leaves the coin (val `0.693` at epoch 1, `0.691` at epoch 60). **Q** sits near the coin at first, then falls (val `0.617` at epoch 5, `0.489` at epoch 10, `0.081` at epoch 20, `0.031` at epoch 60). **R** blows up (epoch-1 *train* loss `1188.9`, val `3.248`) and ends at the coin (`0.723`, 46.9%). **S is the interesting one:** it *learns* (val `0.050` at epoch 20, `0.061` at epoch 40) and then **collapses** in the last twenty epochs back to the coin (val `0.600` at epoch 50, `0.684` at epoch 60, 46.9%). It is not a fluke: all three seeds collapse at this `lr` (final val `0.684, 0.607, 0.693`), and the prep prints that.
- **Section E(b), batch size.** Batch 64: `0.039 ± 0.008`, 780 steps. Batch 256: `0.034 ± 0.007`, **180** steps. Gap `0.005`; twice the larger spread `0.016`. **Inside noise** — and the 256-run took 4.3 times *fewer* steps. The classmate's claim "256 is better" is unsupported; "256 is worse" would also be unsupported.
- **The three one-knob changes for S** (not on the paper; your model answer for E(c) and for a student who asks "but what *would* work?"): `lr = 3e-3` → val `0.037, 0.050, 0.030`; cosine decay → `0.060, 0.057, 0.065`; clipping at 1.0 → `0.427, 0.042, 0.485` (**does not reliably fix it**: two of the three seeds end far from healthy). All three seeds, all measured in the prep.
- **The shape facts behind A20 and B8.** `(2, 4, 3)` in, `nn.RNN(3, 5)`: `out (2, 4, 5)`, `h_n (1, 2, 5)`.

### 6. The honest limits of today

1. **One paper is one sample.** A student who is ill, hungry or anxious scores lower than they know. Treat 45 as a prompt for a conversation, never a verdict. The *pattern across weeks* carries the information; the total barely does.
2. **Multiple choice can be guessed.** Twenty 4-option questions guessed at random average 5 marks (`20 × 0.25`). That is why there are only 20 of 75 marks there, and why every option in Section A was built from a real wrong answer from the earlier weeks, so a wrong choice *means* something (the key names what).
3. **Weeks 3, 5 and 6 had no teacher guide on disk when this one was written.** Questions A6-A8, A12-A14, A15-A17, B3, B5, B6, C2, C3 and D2 were built from the README rows for those weeks and from the reference module, not from the weeks' own guides. **Before you print:** open the Week 3, 5 and 6 teacher guides and check that (i) Week 3 calls the RMS "typical size" and describes AdamW as decaying the weight directly, (ii) Week 5 uses `copy.deepcopy(model.state_dict())` and `model.eval()`, (iii) Week 6 says a batch norm needs more than one example in train mode. If a week's wording differs, change the *wording* of the question and the key together; the numbers will not change.
4. **The Section E tables are from one dataset and one harness.** They show four *symptoms*, not four laws. "`3e-2` collapses" is true of this 16,962-parameter network, this data and this seed set; nothing about other networks.
5. **The self-marking is honest only if the sheet gives working.** A sheet that shows only answers invites a student to "correct" their paper to match. The marking sheet in Handout A shows working for every arithmetic question for that reason.

### 7. The misconceptions you will actually see, and where

| On the paper | A student writes | What it tells you |
|---|---|---|
| A1 | "0.500" | Confuses the *probability* (0.5) with the *loss* (0.693). Week 1. |
| A3 | "v = 0.9·v + 0.1·g" | Learned the average, not PyTorch's form; the ×10 of Week 2 did not land. |
| A6 / D2a | "12.5" or "−0.5" | Stopped before the root; or took the mean, not the root-mean-square. |
| A11 | "780" | Used the batch-64 step count, not 840 // 256 = 3 per epoch. |
| A13 | "zeroes half" | Thinks eval mode still drops units. Week 5. |
| A15 | "it uses the wrong learning rate" | Did not retain *why* a batch of 2 is noisy. Week 6. |
| A16 | "0.7" or "1.0" | Not the slope of a sum: subtracted, or forgot `f`. Week 6. |
| B5 | "2 2" | Thinks `=` copies a dictionary. Week 5 (snapshot). |
| D1 | momentum "w after" = 1.4 | Used `0.1·v` with the *average* form; Week 2's ×10 again. |
| D3 | second ordering gives the same final note | Thinks "same inputs → same output". The whole of Week 8. |
| E(b) | "256 is better, 0.034 < 0.039" | Reads one gap without the spread or the steps. Weeks 4 and 7. |

### 8. How deep to go, and where to stop

Today you teach **nothing**. If, while they work, the student asks a question, the only legal answers are *"read it again"*, *"write what you know"*, and *"I can't help with that one, move on."* Afterwards, in the wrap, explain **no** wrong answers; promise to go through the pattern next time. Real explaining happens in the remediation fortnight, where it will stick because the student has just discovered the gap for themselves.

### 9. 🧭 Where Week 9 sits

```text
   TERM 1 — TRAIN IT ON PURPOSE                               TERM 2 — MEMORY, THEN ATTENTION
   W1  curves      W2 momentum   W3 Adam    W4 schedule       W10 forty multiplications (needs W8 + W6)
   W5  overfit     W6 norms      W7 playbook   W8 a cell  ──►  W11 gates (needs W6's highway)
                                                               W12-13 names, sampling (need W1, W8)
                          ┌───────────────┐                    W14 attention (new again)
                          │  W9  PAPER    │  one week to find out what to redo BEFORE you build on it
                          └───────────────┘
```
Three weeks are load-bearing for Term 2: **Week 6** (the residual highway is the gate of Week 11), **Week 8** (the cell is Week 10's whole subject) and **Week 2** (the running average returns as the gate in Week 11). If the grid shows weeks 2, 6 or 8 under 60%, those three are the ones to redo first; see the remediation table.

---

## 🧰 Prep Checklist

You need this because the paper is only as reliable as your key. Work through the steps in order; each one confirms that your machine agrees with the printed numbers.

### 25 minutes the night before

**☐ 1. Smoke test and folder check (1 minute).** Open a terminal **in the `36-week-course/` folder** — the folder that *contains* `l4lib/` — and run the first block. If it says `ModuleNotFoundError: No module named 'l4lib'` you are in the wrong folder (that is the commonest error of the whole year). `pip` returning **403** is the proxy, and it is **not an error**: nothing is installed this year.

**Block P1 — set-up and the data fingerprint**

Run this first; it loads the data and prints its fingerprint.

```python
# week09.py - Week 9 prep. Run the blocks below in order, from the folder that contains l4lib/.
import io, math
import numpy as np
import torch
import torch.nn as nn
torch.set_num_threads(1)
from l4lib.spirals import get_data, run

Xtr, ytr, Xva, yva = get_data()
print("shapes      :", tuple(Xtr.shape), tuple(Xva.shape))
print("class-1 in val:", int(yva.sum()), "of", len(yva))
```
```text
shapes      : (840, 2) (360, 2)
class-1 in val: 191 of 360
```

If your numbers differ from these, **stop**: you are not teaching from the same data and none of the Section E tables below will match what the paper says. (840 train, 360 validation, 191 class-1 is the fingerprint the Week 1 guide uses too.)

**☐ 2. Compute the key (3 minutes).** Every hand-arithmetic answer on the paper, from code. This file is *teaching* nothing new; it is there so that **you** can see the hand answers and `torch` agree.

**Block P2 — `key.py`: Section D, every number**

Run this to compute every Section D answer and compare the hand results with `torch`.

```python
# key.py - Week 9: every hand-arithmetic answer on the paper, computed.
# D1: three steps of SGD and of momentum on f(w) = w*w, from w = 2.0, lr = 0.1.
def track(momentum):
    w = nn.Parameter(torch.tensor([2.0]))
    opt = torch.optim.SGD([w], lr=0.1, momentum=momentum)
    ws = []
    for _ in range(3):
        opt.zero_grad(set_to_none=True)
        (w * w).sum().backward()
        opt.step()
        ws.append(round(w.item(), 4))
    return ws

print("D1 SGD, torch.optim      :", track(0.0))
print("D1 momentum, torch.optim :", track(0.9))

w, v, hand = 2.0, 0.0, []            # the same momentum track, in plain Python
for _ in range(3):
    g = 2 * w
    v = 0.9 * v + g
    w = w - 0.1 * v
    hand.append(round(w, 4))
print("D1 momentum, by hand     :", hand)

# D2: root-mean-square, then Adam's first step.
for nums in ([3.0, -4.0], [6.0, -8.0]):
    t = torch.tensor(nums)
    print("D2a", nums, "mean of squares", (t * t).mean().item(),
          " rms", round(torch.sqrt((t * t).mean()).item(), 4))
for g in (6.0, 6000.0):
    w = nn.Parameter(torch.tensor([0.50]))
    opt = torch.optim.Adam([w], lr=0.01)
    w.grad = torch.tensor([g])
    opt.step()
    print(f"D2b/c Adam, g = {g:>6}: w 0.50 -> {w.item():.4f}  (moved {0.50 - w.item():.4f})")

# D3: the three-step cell, by hand, then with nn.RNN (our weights, both biases zero).
def unroll(xs):
    h, notes = 0.0, []
    for x in xs:
        h = math.tanh(1.0 * x + 0.5 * h)
        notes.append(round(h, 4))
    return notes

print("D3 [0,1,1] by hand:", unroll([0, 1, 1]))
print("D3 [1,1,0] by hand:", unroll([1, 1, 0]))

cell = nn.RNN(1, 1, batch_first=True)
cell.weight_ih_l0.data = torch.tensor([[1.0]])
cell.weight_hh_l0.data = torch.tensor([[0.5]])
cell.bias_ih_l0.data = torch.zeros(1)
cell.bias_hh_l0.data = torch.zeros(1)
for xs in ([0.0, 1.0, 1.0], [1.0, 1.0, 0.0]):
    out, h_n = cell(torch.tensor(xs).reshape(1, 3, 1))
    print("D3", xs, "nn.RNN:", [round(v, 4) for v in out[0, :, 0].tolist()],
          " match:", torch.allclose(out[0, :, 0], torch.tensor(unroll(xs)), atol=1e-4))
```
```text
D1 SGD, torch.optim      : [1.6, 1.28, 1.024]
D1 momentum, torch.optim : [1.6, 0.92, 0.124]
D1 momentum, by hand     : [1.6, 0.92, 0.124]
D2a [3.0, -4.0] mean of squares 12.5  rms 3.5355
D2a [6.0, -8.0] mean of squares 50.0  rms 7.0711
D2b/c Adam, g =    6.0: w 0.50 -> 0.4900  (moved 0.0100)
D2b/c Adam, g = 6000.0: w 0.50 -> 0.4900  (moved 0.0100)
D3 [0,1,1] by hand: [0.0, 0.7616, 0.8811]
D3 [1,1,0] by hand: [0.7616, 0.8811, 0.4141]
D3 [0.0, 1.0, 1.0] nn.RNN: [0.0, 0.7616, 0.8811]  match: True
D3 [1.0, 1.0, 0.0] nn.RNN: [0.7616, 0.8811, 0.4141]  match: True
```

Check three things. (a) The three momentum lines agree: `[1.6, 0.92, 0.124]`. (b) The RMS of `[3, -4]` is `3.5355` and the *mean of squares* is `12.5` — the wrong answer to A6 and D2a is sitting in that output. (c) Adam moves the weight by exactly `0.0100` for **both** a gradient of 6 and a gradient of 6000. That equality *is* Week 3.

**☐ 3. Check the facts behind Sections A and B (2 minutes).**

**Block P3 — `facts.py`: the multiple-choice numbers**

Run this to print one line of evidence for each Section A question.

```python
# facts.py - Week 9: the numbers behind Section A. One line per question.
print("A1  ln 2 (the coin)             :", round(math.log(2), 3))
print("A5  0.9**6, 0.9**7              :", round(0.9 ** 6, 3), round(0.9 ** 7, 3), "-> half-life about 7")
print("A6  rms of [3,-4]               :", round(torch.sqrt(torch.tensor([9.0, 16.0]).mean()).item(), 4))

w = nn.Parameter(torch.tensor([1.0]))                      # A7: Adam's first step, gradient 1000
opt = torch.optim.Adam([w], lr=0.01)
w.grad = torch.tensor([1000.0])
opt.step()
print("A7  Adam first step, g = 1000   :", round(1.0 - w.item(), 4), "(lr is 0.01)")

p = nn.Parameter(torch.zeros(1))                           # A9: LambdaLR, two steps
o = torch.optim.SGD([p], lr=0.1)
s = torch.optim.lr_scheduler.LambdaLR(o, lambda k: 0.5 ** k)
for _ in range(2):
    o.step()
    s.step()
print("A9  lr after two steps          :", [round(v, 4) for v in s.get_last_lr()])
print("A10 warmup multiplier at s=4    :", (4 + 1) / 10)
print("A11 steps: 840 // 256, x 60     :", 840 // 256, 840 // 256 * 60, "   (batch 64:", 840 // 64 * 60, ")")

d = nn.Dropout(0.5)                                        # A13: dropout in eval mode
d.eval()
print("A13 dropout (eval) on ones      :", d(torch.ones(6)).tolist())

f = lambda x: 0.3 * x                                      # A16: the slope of a sum, by nudging
x0, nudge = 1.0, 0.001
slope = ((x0 + nudge) + f(x0 + nudge) - (x0 + f(x0))) / nudge
print("A16 slope of x + 0.3x, nudged   :", round(slope, 3))
print("A18 gap, 2 x spread             :", round(abs(0.041 - 0.039), 3), round(2 * max(0.010, 0.008), 3))

r = nn.RNN(3, 5, batch_first=True)                         # A20: shapes
o2, h2 = r(torch.zeros(2, 4, 3))
print("A20 out, h_n shapes             :", tuple(o2.shape), tuple(h2.shape))
```
```text
A1  ln 2 (the coin)             : 0.693
A5  0.9**6, 0.9**7              : 0.531 0.478 -> half-life about 7
A6  rms of [3,-4]               : 3.5355
A7  Adam first step, g = 1000   : 0.01 (lr is 0.01)
A9  lr after two steps          : [0.025]
A10 warmup multiplier at s=4    : 0.5
A11 steps: 840 // 256, x 60     : 3 180    (batch 64: 780 )
A13 dropout (eval) on ones      : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
A16 slope of x + 0.3x, nudged   : 1.3
A18 gap, 2 x spread             : 0.002 0.02
A20 out, h_n shapes             : (2, 4, 5) (1, 2, 5)
```

**☐ 4. Reprint-check the Section E tables (about 10 seconds of computing).** These two blocks produce the numbers that are **printed on the paper**. Run them to confirm your machine agrees, then print the *paper's* copy, not this output. (If the S-curve in Block P4 does **not** show the collapse on your machine — a different PyTorch build can move it — **do not change the paper**: the paper's table is the truth for the day; tell the student nothing.)

**Block P4 — the four curves of E(a)**

Run this to print the four loss curves that go on the paper.

```python
# Section E(a): four runs, AdamW, 60 epochs, seed 0. Only lr differs.
curves = {"P": 3e-6, "Q": 3e-4, "R": 0.3, "S": 3e-2}
shown = [1, 5, 10, 20, 40, 50, 60]                       # epochs, counting from 1
def big(v):                                   # a loss over 100 is shown to 1 decimal: its last digit is not stable
    return f"{v:.3f}" if v < 100 else f"{v:.1f}"
print(" " * 20 + "".join(f"{'ep ' + str(e):>9}" for e in shown))
hists = {}
for name, lr in curves.items():
    h = run("paper", lr=lr, verbose=False)
    hists[name] = h
    label = f"{name}  lr={lr:<8g}"
    print(label + "train " + "".join(f"{big(h['train'][e - 1]):>9}" for e in shown))
    print(" " * len(label) + "val   " + "".join(f"{big(h['val'][e - 1]):>9}" for e in shown))
print()
for name in curves:
    print(name, "final accuracy", f"{hists[name]['acc'][-1] * 100:.1f}%")
```
```text
                         ep 1     ep 5    ep 10    ep 20    ep 40    ep 50    ep 60
P  lr=3e-06   train     0.694    0.694    0.694    0.693    0.693    0.693    0.692
              val       0.693    0.693    0.693    0.692    0.692    0.692    0.691
Q  lr=0.0003  train     0.693    0.651    0.533    0.107    0.022    0.016    0.013
              val       0.690    0.617    0.489    0.081    0.035    0.031    0.031
R  lr=0.3     train    1188.9    0.694    0.694    0.696    0.703    0.701    0.701
              val       3.248    0.695    0.695    0.712    0.692    0.692    0.723
S  lr=0.03    train     0.629    0.191    0.426    0.126    0.018    0.259    0.658
              val       0.415    0.143    0.419    0.050    0.061    0.600    0.684

P final accuracy 53.1%
Q final accuracy 99.4%
R final accuracy 46.9%
S final accuracy 46.9%
```

Note the **R** row: the first *train* number is `1188.9`. That is not a typo: it is the average training loss over the first epoch, wrecked by a few huge steps. The first *validation* number (after the epoch) is `3.248`. Students will ask which is "the" loss; the answer is *"the table says which one it is printing, read the label"*.

**Block P5 — the seed table of E(b), and the fixes for S (your model answer)**

Run this to print the batch-size table and the three one-knob fixes for curve S.

```python
# Section E(b): batch 64 against batch 256, AdamW lr 3e-3, three seeds (0, 1, 2), 60 epochs.
rows = {}
for bs in (64, 256):
    vals = [run("paper", lr=3e-3, batch_size=bs, seed=s, verbose=False)["val"][-1] for s in range(3)]
    rows[bs] = vals
    steps = (840 // bs) * 60
    print(f"batch {bs:>3}  steps {steps:>4}  val {[round(v, 3) for v in vals]}"
          f"  mean {np.mean(vals):.3f} +/- {np.std(vals):.3f}")
gap = abs(np.mean(rows[256]) - np.mean(rows[64]))
spread = max(np.std(rows[256]), np.std(rows[64]))
print(f"gap {gap:.3f}   2 x spread {2 * spread:.3f}   ->",
      "INSIDE NOISE" if gap < 2 * spread else "bigger than noise")

# Section E(c), teacher only: S at three seeds, and three one-knob fixes.
def final_vals(**kw):
    return [round(run("paper", seed=s, verbose=False, **kw)["val"][-1], 3) for s in range(3)]
print("S as printed   lr=3e-2          :", final_vals(lr=3e-2))
print("fix: lr 3e-3                    :", final_vals(lr=3e-3))
print("fix: cosine decay, lr 3e-2      :", final_vals(lr=3e-2, schedule="cosine"))
print("not a fix: clip at 1.0, lr 3e-2 :", final_vals(lr=3e-2, clip=1.0))

# Where does S fall apart? The training loss of the curve printed in P4, epochs 48-55.
print("S train loss, epochs 48-55      :", [round(v, 3) for v in hists["S"]["train"][47:55]])
```
```text
batch  64  steps  780  val [0.037, 0.05, 0.03]  mean 0.039 +/- 0.008
batch 256  steps  180  val [0.033, 0.043, 0.025]  mean 0.034 +/- 0.007
gap 0.005   2 x spread 0.016   -> INSIDE NOISE
S as printed   lr=3e-2          : [0.684, 0.607, 0.693]
fix: lr 3e-3                    : [0.037, 0.05, 0.03]
fix: cosine decay, lr 3e-2      : [0.06, 0.057, 0.065]
not a fix: clip at 1.0, lr 3e-2 : [0.427, 0.042, 0.485]
S train loss, epochs 48-55      : [0.309, 0.389, 0.259, 0.433, 1.697, 0.72, 0.694, 0.689]
```

Read that last line carefully. **Clipping did not rescue S** (two of three seeds still end far from healthy, at `0.427` and `0.485`). A student who writes "clip the gradient" as the *action* for E(c) has chosen a plausible-sounding knob that, **measured, does not work here.** That is not a lost mark for the idea (the key gives it credit for being a one-knob action) but it **is** a lost mark for the *evidence* if they claim it works. See the marking guide for E(c).

**☐ 5. Print.** Print **one** copy of [The Paper](#-the-paper-in-full) single-sided (so there is room to work), and **one** copy of the **marking sheet** (Handout A of the key — *only* the block between the two "✂ PRINT" lines). Print the **per-week grid** (Handout B) and the **remediation table** (Handout C) on one page. **Do not print the rest of this file.** Never hand the student any page of this guide except those three.

**☐ 6. Check Weeks 3, 5 and 6 (5 minutes).** See "Honest limits", item 3. Open those teacher guides, check the three wordings, and edit the paper and the key **together** if they differ.

**☐ 7. Decide the remediation slots.** The remediation table gives each weak week a 20-minute redo. Find two slots in the coming fortnight *now* (before Week 10 or in it) and write them on the table. A remediation plan with no time attached does not happen.

### 3 minutes on the day

**☐ 8.** Clear the desk: pen, calculator (airplane mode **on**), scrap paper, water. **The laptop is shut and out of reach**, because this paper's whole point is "no computer". Put the timer where you can both see it. Put the paper face down.

### Fallback if the laptops fail

**Nothing about the lesson needs a laptop.** The student's paper is printed numbers. If *your* laptop fails the night before, the Section E tables in the paper are already printed, and the key's numbers are in this file: the prep only confirms them. Do the lesson from the printed pages.

---

## ⏱️ The Lesson, Minute by Minute

This section is the script for the day. This week's lesson has the usual five-part shape, but four of the five parts are deliberately **empty**. That is the design: nothing is taught, so nothing can be "rescued".

| Segment | Minutes | Clock | What happens |
|---|:--:|:--:|---|
| 🪝 Hook — The Promise | 2 | 0:00-0:02 | Desk cleared, laptop away. You read the three rules and the X-ray sentence. |
| 🧠 Concept & Maths | 0 | — | **None.** There is nothing to explain. |
| 💻 Live-Code Together | 0 | — | **None.** No computer today. |
| 🎲 Their Turn — The Paper | 70 | 0:02-1:12 | Sections A to E, with five time-checks. You say the *time*, nothing else. |
| 🔑 Wrap & Assign | 3 | 1:12-1:15 | Paper in. Marking sheet out. Say what the homework is. Nothing about right or wrong answers. |

### 🪝 Hook — The Promise (2 minutes)

Say, slowly, *from the page, not from memory*:

> *"This is not a test you pass or fail. It is an X-ray of the last eight weeks. You have 70 minutes, a calculator and a pen. No computer, no notes, and I can't help, because the X-ray only works if I don't. If a question looks strange, write down what you do know and move on: partial working earns marks. When it is over you will mark it yourself, and the marks will tell us which two weeks to go back to before the hard bit starts."*

Then: *"Questions?"* Answer **only** about logistics (where to write, the calculator, the toilet). Turn the paper over. Start the timer.

![Two bars split into sections A to E: marks 20, 16, 12, 15, 12 and minutes 15, 15, 12, 15, 13](../figures/fig-w09-1-the-paper-marks-and-minutes.svg)
*Figure 9.1 — The paper is 75 marks in 70 minutes, and Section E, the biggest question, needs its own 13 minutes.*

### 🎲 Their Turn — The Paper (70 minutes)

Sit **to the side and a little behind**. Do something quiet and boring: read, mark something else. Do not watch the page: a student who feels watched writes the answer they think you want.

**The five time-checks.** At each time below say *only* the sentence on the right, in a normal voice:

| Clock | Say | What it is for |
|:--:|---|---|
| **0:17** | *"Seventeen minutes. Section A is usually done by now."* | A is 20 one-mark questions; a student still on A at 0:17 will starve E. |
| **0:32** | *"Thirty-two minutes. Moving on from B is fine."* | B is 8 short programs, about 2 minutes each. |
| **0:44** | *"Forty-four minutes. Section C should be finished."* | C is 4 bugs, about 3 minutes each. |
| **0:59** | *"An hour. You have thirteen minutes for E. Start it now."* | E is 12 marks, **the largest single question on the paper.** |
| **1:10** | *"Two minutes. Finish the sentence you are on."* | Stops the half-finished answer. |

**If they ask you something during the paper.** Three legal replies: *"Read it again."* / *"Write what you do know."* / *"I can't help with that one — move on."* Never a fourth. **If they say "I don't get it":** *"That is useful. Write 'did not get it' next to it and go on. It is the most useful thing you can write."* (Marking rule 4: an honest *"don't know"* is recorded on the grid and is worth more than a lucky guess.)

**If they finish early.** With more than 10 minutes left: *"Go back through, starting from the end, and check each one against your own working."* **Do not** let them leave; do not let them start the next week. If they finish with more than 20 minutes left something is wrong (blank sections? tell them to try every question, even by guessing in A).

**If they are visibly upset.** Stop the clock if you must. *"This is the X-ray, not the grade. Nobody here is keeping score but you."* A calm minute costs a mark or two and is worth it. If the student cannot continue, write the time on the paper, collect it, and mark only what is there; add the missing-section marks to the grid as *"not attempted — rest of paper"* (do not score it zero in the remediation table, see "Assessing Understanding").

![Four homework steps above eight week boxes, with Weeks 8, 2 and 6 ringed 1, 2, 3 as the tie-break order](../figures/fig-w09-2-redo-rule-at-most-two.svg)
*Figure 9.2 — Marks become a plan of at most two redos; if marks tie, Week 8 goes first, then Week 2, then Week 6.*

### 🔑 Wrap & Assign (3 minutes)

1. **At 1:12: "Pens down."** Take the paper. Do not read it in front of them.
2. **Hand over the marking sheet** (the printed Handout A and the grid, Handout B) and a pen of a *different colour* from the one used on the paper.
3. **Say the homework once:** *"Mark your own paper tonight against this sheet, in the other colour. Give yourself marks for working, not just answers: the sheet tells you how. Then fill in the grid, and circle at most two weeks. Bring it next time."*
4. **Say one true thing about the paper**, whatever the result: *"Whatever you got, the thing I care about is whether you can tell me, on the grid, where the marks went."*
5. Do **not** discuss any question. If they ask, *"Tonight, with the sheet. Then we'll talk about the pattern."*

---

## 🐞 The Debugging Clinic

This week the clinic is **short and different**: the four bugs the paper asks the student to find, produced by running them, with the real tracebacks you will want to hold in your head while you mark Section C. There is nothing to *plant* in class: the student has already met each of these in Weeks 1, 5, 6 and 8. Use this clinic **in the remediation fortnight**, on whichever bug the student missed.

Every error below was produced by running the code. **Paths will differ on your machine**; they are shown as `/home/you/l4/`. Tracebacks from PyTorch run through several of its own files; the long middle of those is replaced by a line reading `... frames inside torch (elided) ...`, and **the last line is the real, complete last line**. Each block is a *deliberate* mistake.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (It says what went wrong; the lines above say where.)
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What would you change, and what do you predict will happen?"* — and let them run it.

### Bug C1 — positional arguments to a keyword-only function (loud, Week 1)

Run this deliberate mistake; it fails with the traceback shown.

```python
# DELIBERATE BUG C1 (loud): a keyword-only function called with positional arguments.
def run(*, lr, epochs):
    return lr * epochs

print(run(0.01, 60))
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad1.py", line 5, in <module>
    print(run(0.01, 60))
TypeError: run() takes 0 positional arguments but 2 were given
```

Look at the last line of the traceback: it names the bug.

**Read it:** the `*` in `def run(*, lr, epochs)` means *every* argument must be named. `run(0.01, 60)` passes them by position, so Python says the function takes **0 positional arguments** and that **2 were given**. **Fix:** `run(lr=0.01, epochs=60)`. **What the `*` is for:** *so that a sweep can never pass `lr` and `epochs` in the wrong order* — the answer a full-marks student gives for "why is the function written that way?". Marking: 1 for "keyword-only / positional", 1 for the exact fix with names, 1 for what it would do (an error, with the message in their own words is fine).

### Bug C2 — dropout still on at validation (SILENT, Week 5)

Run this deliberate mistake; nothing fails, which is the problem.

```python
# DELIBERATE BUG C2 (SILENT): validation with dropout still switched on.
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Dropout(0.5), nn.Linear(32, 1))
x = torch.ones(1, 4)
with torch.no_grad():
    a = model(x).item()
    b = model(x).item()
print(round(a, 4), round(b, 4))
```
```text
0.4182 0.2724
```

Look at the two numbers: the same input gave different outputs.

**Read it:** nothing is raised. The *same* input given to the *same* model twice produces two **different** numbers, because the model is still in **train mode**, where `nn.Dropout` randomly zeroes half the units *every call*. **Fix:** `model.eval()` before validating (and `model.train()` again before the next epoch). **Why it is the most instructive of the four:** a validation loss that wobbles from run to run *looks* like "noisy data". The question *"is the same input giving the same output?"* takes ten seconds and is the cheapest check in the whole of Term 1. Marking: 1 for "dropout / train mode", 1 for `model.eval()`, 1 for the *consequence* ("the same input gives different answers; validation is noisy and pessimistic").

And the fix, to see the two numbers become one (this block is **not** a mistake):

```python
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Dropout(0.5), nn.Linear(32, 1))
model.eval()                                  # the one-line fix: dropout is now off
x = torch.ones(1, 4)
with torch.no_grad():
    print(round(model(x).item(), 4), round(model(x).item(), 4))
```
```text
0.3225 0.3225
```

### Bug C3 — batch norm on a batch of one (loud, Week 6)

Run this deliberate mistake; it fails with the traceback shown.

```python
# DELIBERATE BUG C3 (loud): batch norm given a batch of one example, in train mode.
import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.Sequential(nn.Linear(4, 8), nn.BatchNorm1d(8))
one_example = torch.tensor([[1.0, 2.0, 3.0, 4.0]])
print(layer(one_example).shape)
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 7, in <module>
    print(layer(one_example).shape)
  ... frames inside torch (elided) ...
ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 8])
```

Look at the last line of the traceback: it names the bug.

**Read it:** batch norm in train mode computes a mean and spread **across the examples in the batch**, and *"more than 1 value per channel"* is exactly the sentence "you need at least two examples". With one example there is nothing to compute a spread from. **Fix** (any one earns the mark): batch of 2 or more; `nn.LayerNorm(8)`, which uses each example's own features; or `.eval()`, which switches to the stored running statistics. **A trap in the marking:** a student who writes "BatchNorm has no running average" is *half* right; the running statistics exist and are what eval mode uses. Give the mark for any of the three fixes with the right reason, not for "use a bigger batch" without the reason.

### Bug C4 — keeping one name for a pair (loud, Week 8)

Run this deliberate mistake; it fails with the traceback shown.

```python
# DELIBERATE BUG C4 (loud): nn.RNN hands back a pair; only one name was kept.
import torch
import torch.nn as nn
torch.manual_seed(0)
rnn = nn.RNN(3, 4, batch_first=True)
x = torch.ones(2, 5, 3)
out = rnn(x)
last = out[:, -1]
print(last.shape)
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad4.py", line 8, in <module>
    last = out[:, -1]
TypeError: tuple indices must be integers or slices, not tuple
```

Look at the last line of the traceback: it names the bug.

**Read it:** `rnn(x)` returns **two** things — the note after every word, and the last note. Keeping one name keeps the pair as a *tuple*, and indexing a tuple with `[:, -1]` (two things inside the square brackets) is not allowed. The words `tuple indices` in the message are the clue. **Fix:** `out, h_n = rnn(x)`, then `out[:, -1]` (or `h_n[0]`). *(Week 8's clinic met the sibling error `AttributeError: 'tuple' object has no attribute 'shape'`. Same bug, different line; award the marks for either reading.)*

---

## 🎲 The Activity, In Full

This section holds the paper itself, exactly as the student sees it, followed by setup and variations.

### The Paper, in Full

> **How to use this section.** Everything between the two lines marked `✂ PAPER STARTS` and `✂ PAPER ENDS` is what the student sees. Print exactly that. Everything *outside* them is for you. The code on the paper is the same text that the key runs (Handout A), and the Section E tables are the printed numbers of Blocks P4 and P5.

✂ PAPER STARTS

**Term 1 Checkpoint — Review and Assessment 1**

**Name: ____________________   Date: ______________   Time allowed: 70 minutes   Total: 75 marks**

**Rules.** Calculator allowed. No computer. No notes. Write on the paper. **Show your working** in Sections B-E: a wrong number with the right working still earns marks. If you do not know, write *"don't know"*: that is useful information and costs nothing extra. Every question is about something you have already done with your own hands.

| Section | What | Marks | Suggested time |
|:--:|---|:--:|:--:|
| **A** | 20 multiple choice (circle one letter) | 20 | 15 min |
| **B** | 8 "what does this print?" | 16 | 15 min |
| **C** | 4 "find the bug" | 12 | 12 min |
| **D** | 3 arithmetic | 15 | 15 min |
| **E** | One longer question on real loss curves | 12 | 13 min |

---

## Section A — Multiple choice (20 marks, 1 each). Circle ONE letter.

**A1.** A two-class model gives every example a 50-50 guess. Its log loss is closest to:
**A.** 0.000  **B.** 0.500  **C.** 0.693  **D.** 1.000

**A2.** Two runs both end with a validation loss of 0.69. One used `lr = 1e-6`, the other `lr = 0.1`. The best way to tell what happened in each is to:
**A.** compare the two final losses  **B.** compare the two whole curves, starting at epoch 1  **C.** count each model's parameters  **D.** re-run both on a different dataset

**A3.** In `torch.optim.SGD(..., momentum=0.9)`, the velocity `v` is updated by:
**A.** `v = 0.9*v + 0.1*g`  **B.** `v = 0.9*v + g`  **C.** `v = g`  **D.** `v = 0.1*v + 0.9*g`

**A4.** The velocity starts at 0. On the very first step, SGD with momentum moves the weight:
**A.** the same distance as plain SGD  **B.** ten times as far  **C.** half as far  **D.** not at all

**A5.** "The half-life of a 0.9 running average" is about:
**A.** 1 step  **B.** 7 steps  **C.** 10 steps  **D.** 90 steps

**A6.** The root-mean-square of the list `[3, -4]` is closest to:
**A.** -0.5  **B.** 3.54  **C.** 5.0  **D.** 12.5

**A7.** On its very first step, Adam moves a weight whose gradient is **1000** by about:
**A.** 1000 × `lr`  **B.** `lr`  **C.** `lr` / 1000  **D.** 0

**A8.** What does AdamW change compared with Adam plus `weight_decay`?
**A.** It removes the learning rate  **B.** It shrinks the weights directly, instead of through the gradient that Adam then rescales  **C.** It adds momentum  **D.** It needs no epsilon

**A9.** A base `lr` of 0.1, scheduled by `LambdaLR` with `lambda s: 0.5 ** s`. After `scheduler.step()` has been called **twice**, `get_last_lr()` gives:
**A.** 0.2  **B.** 0.05  **C.** 0.025  **D.** 0.0125

**A10.** A warmup of `W = 10` steps uses the multiplier `(s + 1) / W`, with `s` counted from 0. At `s = 4` the multiplier is:
**A.** 0.1  **B.** 0.4  **C.** 0.5  **D.** 1.0

**A11.** There are 840 training examples, the batch size is 256, and the run is 60 epochs. The number of optimizer steps is:
**A.** 60  **B.** 180  **C.** 780  **D.** 1560

**A12.** Which cure for overfitting costs nothing, and changes neither the model nor the data?
**A.** dropout  **B.** weight decay  **C.** augmentation  **D.** early stopping

**A13.** An `nn.Dropout(0.5)` layer that is in **eval** mode:
**A.** zeroes half the values  **B.** passes its input through unchanged  **C.** zeroes all the values  **D.** doubles the values

**A14.** To keep "the best weights so far" so that later training cannot overwrite them, write:
**A.** `best = model.state_dict()`  **B.** `best = copy.deepcopy(model.state_dict())`  **C.** `best = model`  **D.** `best = model.eval()`

**A15.** Batch norm breaks at a batch size of 2 because:
**A.** it has no parameters  **B.** its mean and spread come from the other examples in the batch, and two examples make them extremely noisy  **C.** it only works on images  **D.** it uses the wrong learning rate

**A16.** `y = x + f(x)`. Near some `x`, `f` has slope 0.3. The slope of `y` there is:
**A.** 0.3  **B.** 0.7  **C.** 1.0  **D.** 1.3

**A17.** `clip_grad_norm_(params, 1.0)`:
**A.** does nothing unless a value is NaN  **B.** rescales the gradients so their total length is at most 1, and returns the length they had before  **C.** sets every gradient to 1  **D.** clips the weights to between -1 and 1

**A18.** Baseline validation loss `0.039 ± 0.008`; candidate `0.041 ± 0.010`; three seeds each. By the twice-the-spread rule the candidate is:
**A.** worse  **B.** better  **C.** inside noise  **D.** unknowable without a test set

**A19.** To a bag of words, "dog bit postman" and "postman bit dog" are:
**A.** completely different  **B.** identical counts  **C.** the first is longer  **D.** one has a negative count

**A20.** `x` has shape `(2, 4, 3)` (sentences, words, numbers per word). With `rnn = nn.RNN(3, 5, batch_first=True)` and `out, h_n = rnn(x)`, the shape of `h_n` is:
**A.** `(2, 4, 5)`  **B.** `(1, 2, 5)`  **C.** `(2, 5)`  **D.** `(4, 2, 5)`

---

## Section B — What does this print? (16 marks, 2 each)

Write exactly what the program prints. Show any working beside it. (Rounding is done inside the code, so what you write should match to the digit.)

**B1.** *(Week 1)*
```py
import math
print(round(-math.log(0.25), 3))
```

**B2.** *(Week 2)*
```py
avg = 0.0
for g in [10, 10, 0]:
    avg = 0.9 * avg + 0.1 * g
    print(round(avg, 2))
```

**B3.** *(Week 3)*
```py
import torch
x = torch.tensor([300.0, -400.0])
print(round(torch.sqrt((x * x).mean()).item(), 1))
```

**B4.** *(Week 4)*
```py
import torch
p = torch.tensor([0.0], requires_grad=True)
opt = torch.optim.SGD([p], lr=0.1)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 0.5 ** s)
for _ in range(3):
    opt.step()
    sched.step()
print(sched.get_last_lr())
```

**B5.** *(Week 5)*
```py
import copy
state = {"w": [1, 2]}
alias = state
snap = copy.deepcopy(state)
state["w"].append(3)
print(len(alias["w"]), len(snap["w"]))
```

**B6.** *(Week 6)*
```py
import torch
w = torch.tensor([1.0, 1.0], requires_grad=True)
(3 * w[0] + 4 * w[1]).backward()
before = torch.nn.utils.clip_grad_norm_([w], 1.0)
print(round(before.item(), 1), [round(v, 2) for v in w.grad.tolist()])
```

**B7.** *(Week 7)*
```py
from itertools import product
combos = list(product([0.1, 0.01], ["a", "b", "c"]))
print(len(combos), combos[0], combos[-1])
```

**B8.** *(Week 8)*  (the numbers are the *shapes*; `emb` and `rnn` start from random weights, which do not matter here)
```py
import torch
import torch.nn as nn
emb = nn.Embedding(5, 3)
rnn = nn.RNN(3, 4, batch_first=True)
ids = torch.tensor([[0, 1, 2, 3], [4, 3, 2, 1]])
out, h_n = rnn(emb(ids))
print(tuple(out.shape), tuple(h_n.shape))
```

---

## Section C — Find the bug (12 marks, 3 each)

Each program has one bug. For each: **(i)** say what the bug is, **(ii)** say what happens when it runs (an error — say what the last line means — or a wrong result), and **(iii)** write the fixed line.

**C1.** *(Week 1)*
```py
def run(*, lr, epochs):
    return lr * epochs

print(run(0.01, 60))
```

**C2.** *(Week 5)*  The programmer wanted the same score both times. (Do not try to work out the numbers: they come from random weights. Say what is wrong.)
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Dropout(0.5), nn.Linear(32, 1))
x = torch.ones(1, 4)
with torch.no_grad():
    a = model(x).item()
    b = model(x).item()
print(round(a, 4), round(b, 4))
```

**C3.** *(Week 6)*
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.Sequential(nn.Linear(4, 8), nn.BatchNorm1d(8))
one_example = torch.tensor([[1.0, 2.0, 3.0, 4.0]])
print(layer(one_example).shape)
```

**C4.** *(Week 8)*  The programmer wanted the note after the last word.
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
rnn = nn.RNN(3, 4, batch_first=True)
x = torch.ones(2, 5, 3)
out = rnn(x)
last = out[:, -1]
print(last.shape)
```

---

## Section D — Arithmetic (15 marks, 5 each)

Show every line of working. Four decimal places.

**D1.** *(Week 2)* `f(w) = w²`, so the gradient is `g = 2w`. Start at `w = 2.0`, `lr = 0.1`. Fill both tables for **three** steps. Momentum is PyTorch's: `v = 0.9·v + g` (`v` starts at 0), then `w = w − 0.1·v`.

| Step | SGD: w before | g | w after |
|:--:|:--:|:--:|:--:|
| 1 | 2.0000 | | |
| 2 | | | |
| 3 | | | |

| Step | Momentum: w before | g | v | w after |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 2.0000 | | | |
| 2 | | | | |
| 3 | | | | |

*(SGD columns: 2 marks. Momentum columns: 3 marks.)*

**D2.** *(Week 3)* **(a)** The "typical size" (root-mean-square) of `[6, -8]`: square, average, root. *(2 marks)*  **(b)** Adam, `lr = 0.01`, a weight at 0.50, and a **first** gradient of `+6`. Where is the weight after one step? *(2 marks)*  **(c)** Same, but the first gradient is `+6000`. Where is the weight, and in one sentence, why? *(1 mark)*

**D3.** *(Week 8)* A cell: `new note = tanh(1.0 × x + 0.5 × old note)`, start note `0`. **(a)** Inputs `x = [0, 1, 1]`: write the note after each of the three steps. *(3 marks)* **(b)** Inputs `x = [1, 1, 0]`: write the **last** note. *(1 mark)* **(c)** The inputs add up to the same number both times. In one sentence, what does the pair of final notes show? *(1 mark)*

---

## Section E — Reading real curves (12 marks)

Four runs of the same network on the same data. They differ in **one** thing only: the learning rate. Each is AdamW, 60 epochs, seed 0. The numbers are real. **Train** is the average training loss during that epoch; **val** is the validation loss after it. A coin gives 0.693.

```text
                         ep 1     ep 5    ep 10    ep 20    ep 40    ep 50    ep 60
P  lr=3e-06   train     0.694    0.694    0.694    0.693    0.693    0.693    0.692
              val       0.693    0.693    0.693    0.692    0.692    0.692    0.691
Q  lr=0.0003  train     0.693    0.651    0.533    0.107    0.022    0.016    0.013
              val       0.690    0.617    0.489    0.081    0.035    0.031    0.031
R  lr=0.3     train    1188.9    0.694    0.694    0.696    0.703    0.701    0.701
              val       3.248    0.695    0.695    0.712    0.692    0.692    0.723
S  lr=0.03    train     0.629    0.191    0.426    0.126    0.018    0.259    0.658
              val       0.415    0.143    0.419    0.050    0.061    0.600    0.684
```

**E(a)** *(4 marks, 1 each)* For each of **P, Q, R, S**: say in one plain sentence what the curve is doing, and quote **one number** from the table that shows it.

**E(b)** *(4 marks)* A classmate ran batch 64 and batch 256 at `lr = 3e-3`, **three seeds each** (0, 1, 2), 60 epochs, and wrote: *"Batch 256 is better, because 0.034 is lower than 0.039."* The table is the validation loss at epoch 60.

```text
 batch  steps   val at epoch 60 (seeds 0, 1, 2)      mean +/- spread
    64    780   [0.037, 0.05, 0.03]               0.039 +/- 0.008
   256    180   [0.033, 0.043, 0.025]             0.034 +/- 0.007
```

Use the twice-the-spread rule to decide whether the classmate is justified. Show: the gap, twice the larger spread, and the verdict. Then name **one thing the two runs did not hold equal**, other than the batch size, that makes the comparison harder to read. *(Hint: look at the "steps" column.)*

**E(c)** *(4 marks)* Take curve **S**. Write **one row of a playbook**: **SYMPTOM → CHECK → ACTION**. The check must be something cheap that you could do in seconds. The action must change **one** knob. Then say what you would run **before** you wrote the action into the playbook for good.

✂ PAPER ENDS

### Setup (2 minutes)

Nothing to set up beyond the desk. The paper is the entire activity.

### What "finished" looks like

Every section has *something* written in it, and at least two of the questions say *"don't know"* or show crossed-out working, which is a **good** sign: it means the student was honest. A paper with no crossed-out working and no "don't know" at all is either an excellent student or one who guessed everything and wrote it down cleanly — look at the Section D working to tell which.

### Variation — shorter (a 60-minute slot)

Sit **A, B, C, D** in class in 52 minutes (63 marks: 20 + 16 + 12 + 15; the 60% line scales to **38 of 63**), and give **E** as a *closed-book take-home*, timed by the student at **13 minutes**, within 24 hours, on the honour system. Say the rules aloud. The E marks (12) then join the grid on the usual rows. This is the only variation the grid supports without recomputing.

### Variation — an anxious or slow student

Split the paper into two 40-minute sittings on different days (A-C then D-E). **Not** more time on one day: fatigue is itself a distortion, and a long paper makes it worse.

### Variation — harder (a student who finishes in 40 minutes with 70+ marks)

Add **one** optional question afterwards, *not* on the paper: *"The cell in D3 uses `0.5` for `W_hh`. Compute the first note after a single input of 1 followed by **ten** zeros, and say what happens to it. Do not use the word 'gradient'."* (Answer in the key's *Answers to every question posed in the lesson*; it previews Week 10 and uses only `tanh` and a calculator.)

---

## ❓ Questions Students Ask This Week

Use this table to answer a question in one honest sentence, and to see when the answer must wait until the paper is handed in.

| They ask | Honest answer | Notes |
|---|---|---|
| "Why no computer?" | "Because the paper is asking what is in *your* head, not what the computer knows. Everything on it, you have done by hand at least once." | If they say "but nobody works without a computer" — *"True. And nobody can debug one who can't predict what it will print."* |
| "Is this for a grade?" | "No. It's an X-ray. The only person it reports to is you, and then me." | Mean it. Do not record a mark anywhere except the grid. |
| "Can I use my notes / the workbook?" | "Not today. The marking sheet tonight is your notes." | |
| "What if I get under 45?" | "Then we go back to the two weeks that need it, for 20 minutes each. It's a plan, not a punishment." | The 45 is a proposal (section 3). Never use the word "fail". |
| "Can I do it again?" | "After the remediation fortnight there is a *new* paper of the same shape, not the same one: Assessment 2 re-tests the key ideas inside Weeks 9-17." | Do not write a re-sit paper. Weeks 10-17 recycle W2, W6 and W8 anyway. |
| "Why does the table say 1188.9 for R?" | "That's the *average* training loss over the first epoch, wrecked by a few huge steps. The validation loss after that epoch is 3.248." | See Block P4. |
| "Why isn't clipping the fix for S?" *(afterwards)* | "We tried it: three seeds, and two ended far from healthy (0.43, 0.49). Lowering the learning rate, or a cosine decay, fixed all three." | Show the Block P5 line. **Only after** the paper is handed in. |
| "Is 'inside noise' the same as 'equal'?" | "No. It means *three seeds can't tell them apart*. It is the crude cousin of a proper test, and it stops us fooling ourselves." | Same sentence as Week 7. |
| "Why is `h_n` shaped `(1, 2, 5)`?" | "The leading 1 is 'one layer'." | Week 8, Clinic mistake 7. |
| "What's `tanh` of 1.3808?" | "0.8811. You have a calculator." | A student without a `tanh` key: tell them to write the sum (1.3808) and what they would do; give that step's mark if the sum (1.3808) is right. |

---

## ⚠️ Where This Lesson Goes Wrong

These are the failures to watch for, most common first.

1. **You help.** The commonest failure. A raised eyebrow changes an answer. Sit to the side.
2. **You hand over the wrong page.** The student must get only Handouts A, B and C. The rest of this file contains every answer *and the mistakes the student is expected to make*.
3. **The paper runs over.** Seventy minutes is *tight*. The five time-checks exist so E is not left in the last four minutes. If E is not attempted at all, mark A-D and treat E as a take-home (see "Variation — shorter").
4. **Marking by the final number.** The marks are in the *working*. D1 (5 marks) is two small tables; a student who gets the arithmetic wrong at step 2 and then does the rest *correctly from their own wrong number* loses one mark, not four. Follow the key's "follow-through" notes.
5. **Treating 45 as pass/fail.** The only decision the total drives is how many weeks to redo (at most two). A 70 with a 3/10 on Week 2 means **redo Week 2**, whatever the total.
6. **Scoring the self-marking as the real mark.** Students mark generously or harshly. The teacher **re-marks D and E only** (about 10 minutes), because those are the judgment sections. A disagreement of more than 3 marks in total is a conversation, not an accusation.
7. **Teaching in the wrap.** Resist. The wrap is three minutes, and none of them is for a right answer.
8. **Weeks 3, 5, 6 wording drift** (Honest limits, item 3). If those guides say it differently, the student will lose a mark to *your* wording, not their own error.
9. **The S curve doesn't collapse on your laptop.** It does not matter: the paper's table is printed. It would matter only if you re-generated the table on the day instead of printing it.

---

## 🧭 Differentiation

The paper stays the same for every student. What changes is the sitting, the support around it, and what follows.

### If the student is struggling

- **Same paper, two sittings** (A-C, then D-E), on different days. Not extra time on one day.
- **Read Section E aloud** if reading, not maths, is the barrier. Do not paraphrase; read the words.
- **Calculators for everything** (already allowed). A student who spends 5 minutes on `tanh` by hand has been unfairly treated by the paper.
- **After the paper**, the remediation table is for *at most two* weeks, even if five are low. Pick the one that Term 2 needs most (priority order: **Week 8 → Week 2 → Week 6**), then the lowest remaining.
- **Do not repeat the paper.** Redo the *page* that went wrong (Handout C names it) and ask the **teacher check question** from the table out loud afterwards. A spoken correct answer, in your own words, is the exit ticket.

### If the student is flying

- **70+ in under 55 minutes:** give the "harder" question from the Activity (the cell, one spike, ten zeros), orally, afterwards. It previews Week 10 using only `tanh` and a calculator.
- **Have them write two new Section C questions** — one *loud* bug and one *silent* one — for the **next** student, with the real traceback for the loud one, produced by running it. It is the best test of whether they understand the bug and the cheapest way to test whether the paper is any good. (Do not add them to this paper; they are a candidate for Assessment 2's bank.)
- **Not** more content from Week 10. Today is a review.

### If the student won't engage today

- A flat "I don't care" on the day usually means **one** of: tired, afraid, or "this isn't for a mark so why". Do not argue. Use the X-ray sentence again, shorter: *"Nobody sees this but us. Do the sections you like first."* **They may do the sections in any order.** Take Section D first if that is where the confidence is.
- If they sit 15 minutes with nothing on the page, stop. *"Today is not the day. We'll do it on Thursday."* A paper written under protest produces a map of the protest.
- **Never bribe.** Never threaten. A single "yes, but you can't unlearn what you learned" is enough.

---

## ✅ Assessing Understanding

This section tells you how to mark the paper and how to read the pattern of lost marks, because the pattern matters more than the total.

### The marking rules

1. **Working earns marks.** Sections B-E are marked for *method first, number second*. A right number with no working: **half marks** on 2- and 3-mark questions, **at most 3** on a 5-mark question. (This is the rule that makes "show your working" real. Say it in the key, and mean it.)
2. **Follow-through.** If an early number is wrong, mark later lines *from the student's own number*. The key's "follow-through" notes say where it matters (D1, D3a, E(b)).
3. **Rounding.** In Section B, the program's own rounding is part of the question, so `1.386` is 2 marks and `1.39` is **1** (right idea, sloppy to the digit); `1.4` is 1. In Section D, accept any answer within **0.001** of the key for full marks.
4. **"Don't know"** scores 0 *on that question* but is recorded as **"honest"** on the grid, and a paper with several honest "don't knows" and no wild guesses gets **a tick** (see "Reading the pattern").
5. **Vocabulary from next term** is neither penalised nor rewarded (section 4).

### Reading the pattern

- **The total** is the *least* informative number.
- **The per-week fraction** (Handout B) tells you what to redo. **Under 60% of the marks in a week** goes in the "redo" column; **80% or over** is "secure".
- **Pairs that matter.** Weeks 2 and 8 together low usually means *the running update* (a number that feeds back into itself) has not landed. That is the whole of Weeks 10 and 11; redo both before Week 10.
- **When the total and the pattern disagree, the pattern wins.** A made-up student, to practise the arithmetic (this is an illustration, **not** data from anyone): marks by week `9/11, 4/10, 8/10, 7/9, 6/8, 5/8, 3/7, 6/12` for a total of **48**, which the scale below calls "Secure". The grid says otherwise: Week 2 is 40%, Week 7 is 43% and Week 8 is 50%, three weeks at or under their "redo" line (4 ≤ 5, 3 ≤ 4, 6 ≤ 7). The rule is **circle at most two**, with the priority order Week 8 → Week 2 → Week 6: so **circle Weeks 8 and 2**, and write Week 7 on the side as "first thing to re-check in Assessment 2". The honest summary for this student is *"Getting there"*, not *"Secure"*, even though 48 is above 45.
- **Section C versus Section B.** A student who can say what a program prints (B) but cannot find a bug in it (C) knows the *rule* but has not yet read a traceback: that is a different remediation (read three of the Clinic tracebacks aloud) from not knowing the rule.
- **Section A high, D low.** Knows the words; cannot do the sums. Redo the by-hand pages. **A low, D high:** does the sums and cannot name them — the vocabulary list from each week's guide.

### Mastery scale for this paper

| Level | Marks (of 75) | Looks like | What you do |
|---|:--:|---|---|
| **Flying** | 60-75 | Section D almost clean; E(c) names a check and a one-knob action; at most one week under 80% | Offer the harder question; ask for two new bug questions. |
| **Secure** | 45-59 | At most two weeks under 60%; D mostly right | Redo the circled weeks (20 min each), then move on. |
| **Getting there** | 30-44 | Three or four weeks under 60% | Redo **two** (priority order Week 8 → Week 2 → Week 6), spoken check, and **slow** Week 10 down by one session if needed. Tell the owner before Term 2 builds on shaky ground. |
| **Needs a conversation** | under 30 | Many blanks, or the paper was not attempted seriously | **Do not mark it as a result.** Talk first: tired? afraid? bored? A paper written under protest is a map of the protest. Then see "If the student won't engage". |

*(The 45 line is the proposal from section 3; it is 60% of 75. The scale is a guide, not a ruling.)*

### Teacher re-mark: only D and E

Self-marking covers A, B and C well: those answers are *checkable*. D and E need judgment (is "typical size" the same as "root-mean-square" in the student's words? is the check *cheap*?). Re-mark D (15) and E (12) yourself, in about 10 minutes, **in front of the student if they are willing**. If your total for D+E differs from theirs by more than 3, talk about *why*.

---

## 📤 Homework to Assign

The homework turns the paper into a plan. Say it once, as in the wrap, and assign these steps:

1. **Mark your own paper** against the printed sheet (Handout A), in the *other colour*. For D and E, mark the **working**, not only the answer. *(Estimated 30 minutes.)*
2. **Fill the per-week grid** (Handout B): the marks you got, out of the marks available, for each of the eight weeks, and the percentage. *(5 minutes.)*
3. **Circle at most two weeks** in the remediation table (Handout C): the lowest, but with the priority order Week 8, Week 2, Week 6 breaking ties. Write a day and time for each redo next to the circle. *(5 minutes.)*
4. **One sentence in the Bug Log**: *"The answer I was most surprised to get wrong was ___, because I thought ___."* *(5 minutes.)*

**Next time you bring:** the marked paper, the grid, the circled table. No new code. If a student comes back having *redone* a week's page already, that is a lovely surprise; do not insist on it.

---

## 🔑 Answer Key

> **Handouts A, B and C are the three printed pages for the paper; they are not workbook pages.** (The workbook's own Pages 9.1-9.10 are practice pages on different numbers; their answers are under "Workbook answers" below, and the workbook's own answer page repeats them.) **How this key is laid out.** **Handout A** is the student's marking sheet: *print only the block between the two ✂ lines*. **Handout B** is the per-week grid. **Handout C** is the remediation table. Then comes everything for **you**: the wrong-option map for Section A, the marking notes for B-E, the model answers, and the answers to every question posed in the lesson. The B and C outputs come from the blocks run below; the D numbers from Block P2.

### Handout A — The marking sheet (the one page the student may keep)

✂ PRINT FROM HERE

**Marking sheet — Term 1 Checkpoint.** Use a different colour. For every question, put the marks you earned in the margin. For B-E, mark the *working* too: the sheet says how many marks each step is worth.

**Section A (1 mark each).**

| Q | Ans | Why |
|:--:|:--:|---|
| A1 | **C** | A coin is `ln 2 = 0.693`. (0.5 is the *probability*, not the loss.) |
| A2 | **B** | Both end at the coin; only the *curve* shows that one never moved and one blew up first. |
| A3 | **B** | PyTorch keeps `v = 0.9·v + g`: no `0.1`. The average form is a tenth of it. |
| A4 | **A** | `v` starts at 0, so step 1 is `lr × g`, exactly plain SGD. |
| A5 | **B** | `0.9⁶ = 0.531`, `0.9⁷ = 0.478`: about 7 steps to fall to half. |
| A6 | **B** | Squares `9, 16`, average `12.5`, **root** `3.54`. (12.5 is the step before the root.) |
| A7 | **B** | First step is `lr × g / |g|` = `lr`, whatever `g` is. |
| A8 | **B** | AdamW shrinks each weight directly, instead of adding decay to the gradient that Adam then rescales. |
| A9 | **C** | `0.1 × 0.5² = 0.025`. |
| A10 | **C** | `(4 + 1) / 10 = 0.5`. |
| A11 | **B** | `840 // 256 = 3` steps per epoch, `3 × 60 = 180`. (780 is batch 64.) |
| A12 | **D** | Early stopping is free: keep the weights from the best validation epoch. |
| A13 | **B** | Eval mode turns dropout off: the input passes through unchanged. |
| A14 | **B** | `copy.deepcopy` makes a snapshot later training cannot overwrite; plain assignment is the same object. |
| A15 | **B** | Batch norm's mean and spread come from the other examples; with two they are wildly noisy. |
| A16 | **D** | Slope of a sum: `1 + 0.3 = 1.3`. |
| A17 | **B** | Rescales the gradients to length ≤ 1 and returns the length *before* clipping. |
| A18 | **C** | Gap `0.002` is under `2 × 0.010 = 0.020`: inside noise. |
| A19 | **B** | Same words, same counts: the bag cannot tell them apart. |
| A20 | **B** | `h_n` is `(1, B, H)` = `(1, 2, 5)`; the leading 1 is "one layer". |

**Section B (2 marks each).** Exact output = 2. Right method, wrong last digit or format = 1.

| Q | Prints | Working |
|:--:|---|---|
| B1 | `1.386` | `-ln(0.25) = ln 4 = 1.386`: a four-class coin. |
| B2 | `1.0 / 1.9 / 1.71` (one per line) | `0.1×10 = 1.0`; `0.9×1.0 + 1.0 = 1.9`; `0.9×1.9 + 0 = 1.71`. |
| B3 | `353.6` | squares `90000, 160000`; mean `125000`; root `353.55…` → `353.6`. |
| B4 | `[0.0125]` | after 3 steps the multiplier is `0.5³ = 0.125`; `0.1 × 0.125 = 0.0125`, inside a list. |
| B5 | `3 2` | `alias` is the *same* dictionary (it grew to 3); `snap` is a copy (still 2). |
| B6 | `5.0 [0.6, 0.8]` | the length of `[3, 4]` is 5, printed *before* clipping; then the gradient is scaled by `1/5` to `[0.6, 0.8]`. |
| B7 | `6 (0.1, 'a') (0.01, 'c')` | `2 × 3 = 6` combinations; the first pairs `0.1` with `'a'`, the last `0.01` with `'c'`. |
| B8 | `(2, 4, 4) (1, 2, 4)` | `out` is `(sentences, words, note) = (2, 4, 4)`; `h_n` is `(1, 2, 4)`. |

**Section C (3 marks each: bug 1, what happens 1, fix 1).**

| Q | The bug | What happens | The fix |
|:--:|---|---|---|
| C1 | `run` is keyword-only (`*`) but was called by position | `TypeError: run() takes 0 positional arguments but 2 were given` | `run(lr=0.01, epochs=60)` |
| C2 | The model is still in train mode: dropout is on | Nothing is raised. The same input gives two *different* outputs (`0.4182 0.2724`) | `model.eval()` before validating |
| C3 | Batch norm in train mode needs more than one example | `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 8])` | A batch of 2+, or `nn.LayerNorm(8)`, or `.eval()` |
| C4 | `nn.RNN` returns a *pair*; only one name was kept, so `out` is a tuple | `TypeError: tuple indices must be integers or slices, not tuple` | `out, h_n = rnn(x)` then `out[:, -1]` (or `h_n[0]`) |

**Section D (5 marks each).** Marks are in brackets.

*D1 SGD (2):* `w after` = **1.6000, 1.2800, 1.0240** (`g` = 4.0000, 3.2000, 2.5600). One mark for the `g` column, one for `w after`.
*D1 Momentum (3):* `g` = 4.0000, 3.2000, 1.8400; `v` = **4.0000, 6.8000, 7.9600**; `w after` = **1.6000, 0.9200, 0.1240**. One mark for `g`, one for `v`, one for `w after`. *(If `v` used `0.1·g` instead, you have written the average form and the step is a tenth too small; this is the "×10" of Week 2.)*

*D2:* **(a) 7.0711** (squares 36, 64; mean 50; root 7.0711) [2]. **(b) 0.49** (moves by `lr = 0.01`; a *positive* gradient pushes the weight **down**) [2]. **(c) 0.49** again: the first Adam step is `lr` whatever the size of the gradient, because it divides the gradient by its own typical size [1].

*D3 (a):* notes **0.0000, 0.7616, 0.8811** [3: one each]. **(b)** last note **0.4141** [1] (notes 0.7616, 0.8811, 0.4141). **(c)** "The inputs add to 2 both times, but the final notes are different (0.8811 against 0.4141), so the cell's answer depends on the **order**, which a bag of words cannot do" [1].

**Section E (12 marks).**

*E(a) (1 each: the symptom + one correct number).*
**P** — flat: never leaves the coin; val `0.693` at epoch 1 and `0.691` at epoch 60.
**Q** — slow but learning: still near the coin at epoch 5 (val `0.617`), then falls steadily to `0.031` at epoch 60.
**R** — blew up, then stuck at the coin: epoch-1 train loss `1188.9`; ends at val `0.723` (46.9% accuracy).
**S** — learned, then collapsed: val `0.050` at epoch 20 and `0.061` at epoch 40, back to `0.600` at epoch 50 and `0.684` at epoch 60 (46.9%).

*E(b) (4):* gap `0.005` [1]; twice the larger spread `0.016` [1]; verdict **inside noise** — "0.034 is not shown to be better than 0.039" [1]; **the number of steps was not equal: 780 against 180** (any equivalent answer — the same `lr` for both batch sizes also earns the mark) [1].

*E(c) (4):* the **symptom** with a number (e.g. "validation loss `0.061` at epoch 40 and `0.684` at epoch 60: it learned and then fell back to the coin") [1]; a **cheap check** (e.g. "print the training loss for epochs 40-60 and see where it jumps" or "print the gradient length each epoch") [1]; a **one-knob action** (e.g. "lower `lr` to `3e-3`", or "add cosine decay") [1]; and the **evidence step** ("run it at three seeds and compare with the baseline using the twice-the-spread rule") [1].

✂ PRINT TO HERE

### Handout B — The per-week grid (print this, with Handout C)

| Week | Topic | Questions | Marks available | Marks earned | % | Redo if marks ≤ | Circle? |
|:--:|---|---|:--:|:--:|:--:|:--:|:--:|
| 1 | Reading a loss curve; the coin | A1, A2, B1, C1, E(a) | **11** | | | 6 | |
| 2 | Momentum; the running average | A3-A5, B2, D1 | **10** | | | 5 | |
| 3 | Adam; typical size | A6-A8, B3, D2 | **10** | | | 5 | |
| 4 | Schedules; batch size and steps | A9-A11, B4, E(b) | **9** | | | 5 | |
| 5 | Overfitting cures | A12-A14, B5, C2 | **8** | | | 4 | |
| 6 | Norms, residuals, clipping | A15-A17, B6, C3 | **8** | | | 4 | |
| 7 | The sweep; "is it noise?" | A18, B7, E(c) | **7** | | | 4 | |
| 8 | Order; the recurrent cell | A19, A20, B8, C4, D3 | **12** | | | 7 | |
| | **Total** | | **75** | | | | |

*(11 + 10 + 10 + 9 + 8 + 8 + 7 + 12 = 75. "Redo if marks ≤" is the highest whole mark strictly under 60% of the week's marks; a week of 10 marks is redone at 5 or fewer, since 6 of 10 is exactly 60%.)*

### Handout C — The remediation table (print with Handout B)

Circle at most **two** weeks. Priority order if there is a tie: **Week 8, Week 2, Week 6**. Each redo is 20 minutes plus the spoken check.

| Week | Redo this (20 min) | The teacher's spoken check (the student answers aloud, no paper) | Why Term 2 needs it |
|:--:|---|---|---|
| 1 | Workbook **Page 1.3** (the coin, by hand) and the six-curve grid, **Page 1.1** | "Two runs both end at 0.69. How do you tell what each did?" → *the curve, from epoch 1* | Every Term 2 lab starts by reading a curve. |
| 2 | Workbook **Page 2.1** (the hand table) and **Page 2.8** (a second hand table with new numbers) | "Momentum step 2: what is `v`, and why isn't it `0.1`-something?" → *`0.9·v + g`; PyTorch keeps no `0.1`* | The running update returns as the gate in Week 11. |
| 3 | Workbook **Page 3.1** (the three-optimizer table, with Adam's first step) and **Page 3.3** (RMS on `[3, -4]` then `[300, -400]`) | "Why is Adam's first step the same for a gradient of 1 and of 1000?" → *it divides by the gradient's own typical size* | Adam is the default optimizer for every later lab. |
| 4 | Workbook **Page 4.3** (the schedule by hand) and **Page 4.4** (counting steps) | "Batch 256 against 64: what is not equal besides the batch?" → *the number of steps* | Every later comparison has the "what did I hold fixed?" question. |
| 5 | Workbook **Page 5.3** (stopping and the fee, by hand) and **Page 5.5** (the four-cure table, and the `deepcopy` snapshot) | "Which column of the cure table do you trust, and why?" → *best validation loss; the final one depends on when you stopped* | Early stopping and `eval()` are used in every training script from now on. |
| 6 | Workbook **Page 6.3** (normalise by hand, including batch norm on a pair) and **Page 6.4** (slope of `x + f(x)` by nudging) | "What is the slope of `x + f(x)` when `f` has slope 0.3?" → *1.3* | The residual highway is Week 11's gate. |
| 7 | Workbook **Page 7.3** (is it noise?) and **Page 7.4** (read four curves) | "Gap 0.002, spreads 0.008 and 0.010: bigger than noise?" → *no, 0.002 is under 0.020* | Every lab from here reports mean ± spread. |
| 8 | Workbook **Page 8.3** (unroll the cell by hand) and **Page 8.4** (shapes) | "Same inputs in a different order: same final note?" → *no; the note depends on the order* | **Week 10 is entirely about this cell.** |

### Teacher-only: the map of wrong answers in Section A

| Q | Wrong option | It usually means |
|:--:|---|---|
| A1 | B (0.500) | Confuses probability and loss. |
| A1 | D (1.000) | Guessing; or "a coin is a 1-in-1 loss". |
| A2 | A | Believes "same final number, same story". The entire point of Week 1. |
| A3 | A (`0.1·g`) | Learned the average form, not PyTorch's (Week 2's ×10). |
| A3 | D | Guess. |
| A4 | B (ten times) | Confuses with the *steady state* of momentum (about ten times the gradient). It is right *later*, not on step 1. |
| A5 | C (10) / D (90) | Reads the 0.9 as the half-life, or does `0.9 × 100`. |
| A6 | A (−0.5) | The mean, not the RMS. |
| A6 | C (5.0) | The length (Week 2's `.norm()`), not the typical size. |
| A6 | D (12.5) | Stopped before the root. |
| A7 | A | Thinks Adam steps scale with the gradient, like SGD. |
| A7 | C / D | Over-correcting. |
| A8 | C | Mixed up AdamW with momentum. |
| A9 | B (0.05) | Applied the multiplier once (`0.5¹`) or counted from 1. |
| A9 | D (0.0125) | Three calls instead of two. |
| A10 | B (0.4) | Forgot the `+ 1`. |
| A11 | C (780) | Used batch 64. |
| A11 | D (1560) | Used batch 32. |
| A11 | A (60) | Counted epochs. |
| A12 | A-C | Thinks regularisers are free. |
| A13 | A | Thinks eval mode still drops units: the reference module's "single most common PyTorch bug" (Week 5). |
| A13 | D | Remembers the `1/(1−p)` scaling and attaches it to the wrong mode. |
| A14 | A | The reference trap: `state_dict()` returns the *live* tensors; training overwrites them. |
| A15 | D | Fashionable guess; no mechanism. |
| A16 | A (0.3) | Forgot the "1 +". |
| A16 | B (0.7) | Subtracted. |
| A16 | C (1.0) | Knows the highway slope but forgot `f`'s contribution. |
| A17 | D | Confuses clipping gradients with clamping weights. |
| A18 | A / B | Reads `0.041 > 0.039` as a verdict. |
| A19 | A | Cannot say what a bag throws away. |
| A20 | A (2, 4, 5) | Reports `out`, not `h_n`. |
| A20 | C | Drops the leading 1. |
| A20 | D | Time-first layout (forgot `batch_first`). |

### Teacher-only: marking notes for Section B

- **B1** `1.386`: `-math.log(0.25)` is the loss of a four-class guesser. The student does not need to know why `ln 4`; `0.25 → 1.386` by calculator is enough. Mark `1.39` as 1.
- **B2** Three lines. Give 1 mark for the first two lines right and 1 for the third, or 1 for the right three numbers if they printed them on one line. (The *trap* is the printing: each pass of the loop prints.)
- **B3** `353.6`. A student who writes `12.5`-style (stopped before the root) writes `125000.0`: 1 mark if the working shows the mean of squares.
- **B4** `[0.0125]`, **with the square brackets**. A student who writes `0.0125` has missed that `get_last_lr()` returns a list: 1 mark.
- **B5** `3 2`. The mark scheme: 1 for each number. A student who writes `2 2` thinks `=` copies.
- **B6** `5.0 [0.6, 0.8]`: 1 for each half. The *5.0 is printed before the clipping is seen*, a very common slip is `1.0 [...]`.
- **B7** `6 (0.1, 'a') (0.01, 'c')`. The tuple formatting (parentheses and quotes) is part of what `print` shows; a student who writes `0.1 a` has the idea: 1.
- **B8** `(2, 4, 4) (1, 2, 4)`. 1 for each.

### Teacher-only: follow-through notes for D and E

- **D1.** If `w` after step 1 is wrong, mark steps 2 and 3 *from the student's own number*: the `g = 2w` and `v` lines are right if they follow from it. One slip costs the column's one mark, not the whole table.
- **D2(a)** If the student stops at `50` (the mean of squares), they get 1 of 2 (right method, forgot the root). **(b)** `0.49`: if they write `0.51` (moved the wrong way), 1 of 2: the size is right, the direction is not. **(c)** Full mark needs *both* the number and a reason; the reason may be in the student's words ("it divides by its own size").
- **D3(a)** One mark per note. If step 2 is wrong, step 3 is right *from the student's own step 2*: give it. **(c)** needs both the observation (different) and the lesson (order matters); "they are different" alone is half a mark — round it down.
- **E(b)** If the gap is miscalculated from the printed means, the verdict mark follows from their own gap and their own `2 × spread`.

### Teacher-only: model answers and exemplars for E(c)

**A full-marks answer (4/4).** *"Symptom: S learns (val 0.061 at epoch 40) then collapses back to the coin (0.684 at epoch 60). Check: print the training loss for every epoch from 40 to 60 and see where it jumps (it jumps at epoch 52). Action: lower `lr` to 3e-3 (one knob). Before it goes in the playbook: run three seeds at the new `lr` and compare with the baseline using the twice-the-spread rule."* (Block P5 prints the training loss of S for epochs 48-55; use it afterwards to show *where* the jump is.)

**A 3/4 answer.** Symptom with number; a one-knob action; a check that is *not cheap* ("train a bigger model"); evidence step. Lost mark: the check.

**A 2/4 answer.** *"S is bad. Lower the learning rate. Check that it works."* The symptom has no number, and "check that it works" is not an evidence step (how many seeds? compared with what?). Mark: one for the action, one for the (vague) symptom — be generous on whichever the student's words land closest to.

**A 1/4 answer.** *"Clip the gradient and it will work."* One knob (1), but no number, no check, no evidence, and **it does not work here** (Block P5: two of three seeds end at `0.427` and `0.485`).

### Workbook answers (the practice pages 9.1-9.10)

All values were rerun on CPU, seed 0, torch 2.2.1. **Warm-Up:** W1 0.693; W2 0.4; W3 a cell gives a different final note, a bag gives the same; W4 smaller than 2 times the spread; W5 any honest answer.

- **Page 9.2** (`w = 1.5`, `lr = 0.1`). SGD: w after 1.2000, 0.9600, 0.7680. Momentum: v = 3.0000, 5.1000, 5.9700; w after 1.2000, 0.6900, 0.0930. 9.2a yes (v starts at 0); 9.2b momentum, 0.0930 against 0.7680, a difference of 0.6750; 9.2c the velocity adds up past gradients; 9.2d it goes past 0: the check file prints 1.2, 0.69, 0.093, -0.4629, -0.8706.
- **Page 9.3.** 9.3a squares 25 and 144, average 84.5, root 9.1924. 9.3b wrong answers 84.5 (forgot the root), -3.5 (plain mean), 13.0 (the length). 9.3c 919.24, 100 times bigger, so it scales. 9.3d 1.02. 9.3e 1.02 too (the gradient's size cancels). 9.3f AdamW applies the decay to the weights directly rather than through the gradient.
- **Page 9.4** (`W_x = 1.0`, `W_h = -0.5`). `[1, 0, 1]`: notes 0.7616, -0.3634, 0.8280 (pre values 1.0000, -0.3808, 1.1817). `[1, 1, 0]`: notes 0.7616, 0.5506, -0.2685 (pre values 1.0000, 0.6192, -0.2753). 9.4a total 2; last notes 0.8280 and -0.2685, different. 9.4b a bag cannot tell them apart; the cell can. 9.4c the note at step 2 is negative because `W_h` is negative. 9.4d (ii), a single squashed summary.
- **Page 9.5.** Shapes `(3, 6)`, `(3, 6, 2)`, `(3, 6, 7)`, `(1, 3, 7)`; the embedding has 12 numbers and the RNN 77 (2x7 + 7x7 + 7 + 7).
- **Page 9.6.** 9.6a gap 0.0173, larger spread 0.0082, twice 0.0163: bigger, only just. 9.6b gap 0.0040 against 0.0163: inside noise. 9.6e (840 / 120) x 10 = 70 steps.
- **Page 9.7.** The check file prints `val at epochs 20, 40, 60: [0.049, 0.136, 0.059]`, `lowest val 0.012 at epoch 31` and `final accuracy 99.2%`. 9.7c: val went up from epoch 20 to 40 for both W (0.029 to 0.085) and Z (0.049 to 0.136). Y's first-epoch train 7837888.5 and val 5632.9 differ because train is averaged over the epoch's steps and val is measured once after.
- **Page 9.8.** A `TypeError: total() takes 0 positional arguments but 2 were given`; B prints `True` then `False` (add `model.eval()`); C `ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 5])`; D `AttributeError: 'tuple' object has no attribute 'shape'`. Slope check 1.5, then 0.
- **Pages 9.1, 9.9, 9.10 and Self-Check.** The per-week grid on Page 9.9 matches Handout B (marks 11, 10, 10, 9, 8, 8, 7, 12 = 75; redo thresholds 6, 5, 5, 5, 4, 4, 4, 7; tie order 8, 2, 6). The other answers are in the student's own words.

### Answers to every question posed in the lesson

| In the lesson | Answer |
|---|---|
| *"Questions?"* (Hook) | Logistics only. |
| *"What is the half-life of 0.9?"* (A5) | About 7. |
| *"Read it again" / "Write what you do know"* | The only legal prompts; nothing else. |
| **Harder variation:** one spike (input 1) then ten zeros, `W_xh = 1.0`, `W_hh = 0.5`, no gradient words | Block below: each note is a little under half the one before, so after ten zeros the note is about a thousandth of the first. |

```python
h, notes = 0.0, []
for x in [1.0] + [0.0] * 10:
    h = math.tanh(1.0 * x + 0.5 * h)
    notes.append(round(h, 5))
print(notes)
print("last / first:", round(notes[-1] / notes[0], 5))
```
```text
[0.76159, 0.3634, 0.17973, 0.08962, 0.04478, 0.02239, 0.01119, 0.0056, 0.0028, 0.0014, 0.0007]
last / first: 0.00092
```

*(The sentence a student should reach: "the note fades about half each step, so ten steps leaves it almost gone; that is next week.")*

---

## 🔮 Next Week Preview

**Week 10 — Forty Multiplications: Why Memory Fades** (🟩 lab). The cell from Week 8 is trained for real, and the student measures what happens to the gradient at the **first** word as the sentence gets longer (T = 10, 20, 40, 80). The new maths idea is **compounding** — a number multiplied by itself T times — met on paper first (`0.9526` multiplied forty times is `0.143`; `0.95` forty times; `1.05` forty times). Three new constructs: `h.retain_grad()`, `torch.stack`, `torch.randn(T, ...)`.

```python
print("0.9526 ** 40 =", round(0.9526 ** 40, 3))
```
```text
0.9526 ** 40 = 0.143
```

**What from today carries over:** the clean unroll of D3 (Week 8), the running update (Week 2) and the highway slope (Week 6). **If the grid shows Week 8 or Week 2 under 60%, those are the two redos to do before Week 10.** Nothing else from Term 1 is on the critical path.
