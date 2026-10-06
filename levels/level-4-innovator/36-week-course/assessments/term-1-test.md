# 📝 Term 1 Test — Weeks 1–9: Train It On Purpose

[⬅ Course home](../README.md) · Term 1 of 4 · covers Weeks 1–8 (Week 9 is the review week)

---

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │   AI ACADEMY · LEVEL 4 INNOVATOR                                     │
   │   TERM 1 TEST — Train It On Purpose                                  │
   │   Covers Weeks 1–8. Nothing later appears anywhere on this test.     │
   │                                                                      │
   │   PART 1 · THE PAPER           70 minutes      75 marks              │
   │   PART 2 · THE DEMO            15 minutes      15 marks              │
   │                                                                      │
   │   Section A   20 multiple choice          1 mark each     20 marks   │
   │   Section B    8 "what does this print"   2 marks each    16 marks   │
   │   Section C    4 "find the bug"           3 marks each    12 marks   │
   │   Section D    3 "do the arithmetic"      5 marks each    15 marks   │
   │   Section E    1 longer question on real curves           12 marks   │
   │                                                                      │
   │   PART 1:  ⛔ NO COMPUTER.   ✅ A CALCULATOR, YES.                  │
   │   PART 2:  ✅ A COMPUTER AND YOUR OWN WEEK 1–8 FILES. NO NETWORK.   │
   │                                                                      │
   │      A programmer who can only find out what code does by running   │
   │      it cannot debug. Part 1 is run in your head. Part 2 is where   │
   │      you prove the head was right, with a machine, in front of      │
   │      someone.                                                        │
   │                                                                      │
   │   SUGGESTED TIME   A 15 · B 15 · C 12 · D 15 · E 13 minutes         │
   │                                                                      │
   │   INSTRUCTIONS FOR THE PAPER                                         │
   │   · Pencil. Answer every question. "Don't know" is allowed and       │
   │     costs nothing extra; a blank tells nobody anything.              │
   │   · Section A: circle ONE letter. If you guessed, write "not sure".  │
   │   · Section B: write EVERY line the program prints, in order.        │
   │   · Section C: say (i) what is wrong, (ii) what happens when it      │
   │     runs, (iii) the fixed line.                                      │
   │   · Section D: show every line of working. A bare number scores      │
   │     less than a number with its working.                             │
   │   · Section E: use the numbers in the tables. Quote them.            │
   │                                                                      │
   │   WHAT IS ALLOWED ON THE PAPER                                       │
   │   ✅  Pencil, pen, eraser, ruler, a calculator                       │
   │   ✅  Rough paper. Working earns marks                               │
   │   ❌  A computer, a phone, your notes, your .py files                │
   │   ❌  A search engine, a chatbot, another person                     │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘
```

> **🧑‍🏫 Teacher, read this box once before you hand anything out.**
>
> **What this file is.** The Week 9 review week already contains a paper (in that week's own guide).
> **This is a second paper of the same shape with every number different** — a different question on
> every topic, no question repeated. Use it as the formal Term 1 test, as the re-sit after the
> remediation fortnight, or as practice. Nothing on it appears in the Week 9 paper, so a student who has
> sat that one has not seen this one. It is **not** a replacement: the Week 9 paper is the one the
> student self-marks.
>
> **You do not need to know Python or machine learning to run or mark this.** The answer key at the
> bottom gives every answer, every piece of working, and the *real printed output* of every code block.
> Compare, do not work out.
>
> **What "real" means here.** Every code block on this file — on the paper and in the key — was run from
> the `36-week-course/` folder on a CPU, one thread (`torch.set_num_threads(1)`), Python 3.10.10,
> torch 2.2.1, numpy 1.26.4, with the seeds shown, and the output pasted in unedited (tracebacks only
> have the file path shortened). Every number in the Section E tables was printed by the course's own
> `l4lib.spirals.run` harness. **The tables on the paper are printed numbers: print them, do not
> regenerate them on the day.** On a different CPU or torch build the last digit of a loss can move.
>
> **There is no language model, no scripted backend and no stand-in anywhere on this test.** Nothing
> here is a "stand-in, not a model", because Term 1 never uses one; the first scripted backend arrives
> in Week 23.
>
> **Run the paper first, then the demo, the same day if you can.** Say out loud, before you start:
> *"Everything on this test is something you have already done with your own hands. It is an X-ray,
> not a grade. If a question looks strange, read it twice, write what you do know, and move on."*
> Then say nothing until the timer goes. Do not explain any answer afterwards; the remediation
> section at the end of this file says what to do with the pattern.

---

# 📄 PART 1 — THE PAPER

**Name: ____________________   Date: ______________   Time allowed: 70 minutes   Total: 75 marks**

---

# 🅰️ Section A — Multiple Choice

*20 questions · 1 mark each · circle ONE letter · the week each question comes from is in brackets*

---

**A1.** [W1] A model is asked to pick one of **four** classes and knows nothing: it gives every class the
same probability. Its log loss is closest to:

- (a) 0.250
- (b) 0.693
- (c) 1.386
- (d) 4.000

---

**A2.** [W1] What does the lone `*` do in `def run(*, lr, epochs):`?

- (a) It makes the arguments optional
- (b) It forces every argument after it to be passed by name, so a sweep cannot silently swap two numbers
- (c) It lets the function take any number of arguments
- (d) It makes the function run faster

---

**A3.** [W1] At the last epoch, a validation-loss curve is still falling steeply. The most honest reading is:

- (a) The model has converged
- (b) The model is overfitting
- (c) It has not finished learning: more epochs, or a larger `lr`, are the one-knob things to test
- (d) The validation set is broken

---

**A4.** [W2] PyTorch's `SGD(..., momentum=0.9)` keeps a velocity `v = 0.9*v + g`. If the gradient `g`
stays the same for many steps, `v` settles near:

- (a) 0.9 × g
- (b) 1 × g
- (c) 90 × g
- (d) 10 × g

---

**A5.** [W2] A running average is updated by `avg = 0.9*avg + 0.1*new`. It starts at 0, and the first new
value is 10. After one update `avg` is:

- (a) 1.0
- (b) 9.0
- (c) 0.1
- (d) 10.0

---

**A6.** [W3] The root-mean-square (the "typical size") of the list `[0, 10]` is closest to:

- (a) 5.00
- (b) 7.07
- (c) 10.00
- (d) 50.00

---

**A7.** [W3] What is the tiny number `eps` (epsilon) for in Adam?

- (a) It makes the first step bigger
- (b) It decays the weights
- (c) It stops a division by zero when a weight's "typical gradient size" is zero
- (d) It adds momentum

---

**A8.** [W3] Two weights get a first gradient of **0.5** and **500**. Adam, `lr = 0.01`. On the very first
step the two weights move by:

- (a) about 0.01 each
- (b) 0.005 and 5
- (c) 0.0001 and 0.1
- (d) neither moves

---

**A9.** [W4] A base `lr` of 0.3, scheduled by `LambdaLR` with `lambda s: 1 / (1 + s)`. After
`scheduler.step()` has been called **twice**, `get_last_lr()` gives:

- (a) 0.3
- (b) 0.15
- (c) 0.075
- (d) 0.1

---

**A10.** [W4] A warmup of `W = 20` steps uses the multiplier `(s + 1) / W`, with `s` counted from 0.
At `s = 9` the multiplier is:

- (a) 0.05
- (b) 0.5
- (c) 0.45
- (d) 1.0

---

**A11.** [W4] 840 training examples, batch size 128, 40 epochs. Steps per epoch are `840 // 128`. The
number of optimizer steps in the whole run is:

- (a) 42
- (b) 280
- (c) 240
- (d) 6

---

**A12.** [W4] The same 840 examples, 40 epochs, once with batch 32 and once with batch 256. How many
optimizer steps does each run take? (Use `840 // batch` steps per epoch.)

- (a) 26 and 3
- (b) 1040 and 120
- (c) 1080 and 160
- (d) 40 and 40

---

**A13.** [W5] In train mode, `nn.Dropout(0.3)` zeroes each number with probability 0.3. Each number it
**keeps** is multiplied by:

- (a) 0.7
- (b) 0.3
- (c) 1.0
- (d) about 1.43

---

**A14.** [W5] You keep a snapshot of the weights from the best epoch, so you can ship them. "Best" means:

- (a) the epoch with the lowest validation loss
- (b) the epoch with the lowest training loss
- (c) the last epoch
- (d) the epoch where training accuracy first reaches 100%

---

**A15.** [W5] `AdamW` with `lr = 0.01` and `weight_decay = 0.5`. Before the usual step, every weight is
multiplied by `1 − lr × weight_decay`. That is:

- (a) 0.5
- (b) 0.99
- (c) 0.995
- (d) 0.9995

---

**A16.** [W6] In train mode, which layer **cannot** work on a batch of exactly **one** example?

- (a) `nn.LayerNorm`
- (b) `nn.BatchNorm1d`
- (c) both of them
- (d) neither of them

---

**A17.** [W6] `y = x + f(x)`. Near some `x`, `f` has slope **−0.4**. The slope of `y` there is:

- (a) −0.4
- (b) 0.4
- (c) 1.4
- (d) 0.6

---

**A18.** [W6] Why does a residual connection (`x + f(x)`) help a deep network train?

- (a) The error on its way back has a road of slope exactly 1 around every block, so it does not have to shrink block by block
- (b) It gives the network fewer parameters
- (c) It normalises every example
- (d) It removes the need for a learning rate

---

**A19.** [W7] Three seeds each, validation loss at epoch 60. Baseline (plain SGD): `0.653 ± 0.020`.
Candidate (SGD with momentum): `0.042 ± 0.007`. By the twice-the-spread rule the candidate is:

- (a) worse
- (b) inside noise
- (c) better
- (d) unknowable without a test set

---

**A20.** [W8] How many numbers (parameters) are inside `nn.RNN(3, 4)`? (It has two weight tables and two
bias lists.)

- (a) 36
- (b) 12
- (c) 16
- (d) 28

---

# 🅱️ Section B — What Does This Print?

*8 questions · 2 marks each · write EVERY line the program prints, exactly. Rounding is done inside the code.*

---

**B1.** [W1]

```py
def run_toy(*, lr, batch_size, seed=0):
    return f"lr={lr} bs={batch_size} seed={seed}"

print(run_toy(batch_size=32, lr=0.01))
```

---

**B2.** [W2]

```py
avg = 0.0
for g in [20, 20, 0]:
    avg = 0.9 * avg + 0.1 * g
    print(round(avg, 2))
```

---

**B3.** [W3]

```py
import torch
x = torch.tensor([5.0, -12.0])
print(round(torch.sqrt((x * x).mean()).item(), 2))
```

---

**B4.** [W4]

```py
import torch
p = torch.tensor([0.0], requires_grad=True)
opt = torch.optim.SGD([p], lr=0.3)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1 / (1 + s))
for _ in range(3):
    opt.step()
    sched.step()
    print(round(sched.get_last_lr()[0], 4))
```

---

**B5.** [W5]

```py
import copy
w = [1.0, 2.0]
snap = copy.deepcopy(w)
alias = w
w.append(9.0)
print(len(alias), len(snap), alias is w, snap is w)
```

---

**B6.** [W6] (Layer norm subtracts the row's mean and divides by the row's spread. `eps` is so small it does not change four decimals. `weight` starts at 1 and `bias` at 0.)

```py
import torch
import torch.nn as nn
ln = nn.LayerNorm(3)
x = torch.tensor([[1.0, 2.0, 3.0]])
print([round(v, 4) for v in ln(x)[0].tolist()])
```

---

**B7.** [W7]

```py
from itertools import product
grid = list(product([3e-3, 1e-2], [0.0, 0.1], [0, 1, 2]))
print(len(grid))
print(grid[1])
print(grid[-1])
```

---

**B8.** [W8] (`emb` and `rnn` start from random weights, which do not matter here: the question is about shapes.)

```py
import torch
import torch.nn as nn
emb = nn.Embedding(10, 6)
rnn = nn.RNN(6, 7, batch_first=True)
ids = torch.tensor([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [0, 0, 0, 0, 0]])
out, h_n = rnn(emb(ids))
print(tuple(out.shape), tuple(h_n.shape))
```

---

# 🅲 Section C — Find and Fix the Bug

*4 questions · 3 marks each · for each: **(i)** what is wrong · **(ii)** what happens when it runs (an error, with what its last line means in plain words — or a silent wrong result) · **(iii)** the fixed line.*

---

**C1.** [W1]

```py
def sweep(*, lr, batch_size):
    return lr * batch_size

print(sweep(0.01, 64))
```

---

**C2.** [W5] The programmer wanted `best` to be a frozen copy of the weights at the moment it was saved, so the
two numbers printed at the end would be **equal**. (You cannot work out the exact numbers from the code; say what is wrong.)

```py
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Linear(1, 1, bias=False)
best = model.state_dict()                      # "save the weights at the best epoch"
at_best = round(best["weight"].item(), 4)

opt = torch.optim.SGD(model.parameters(), lr=0.5)
x = torch.tensor([[2.0]])
loss = (model(x) - 10.0) ** 2
opt.zero_grad()
loss.backward()
opt.step()                                     # training carries on after the best epoch

print(at_best, round(best["weight"].item(), 4))
```

---

**C3.** [W6]

```py
import torch
import torch.nn as nn
torch.manual_seed(0)
net = nn.Sequential(nn.Linear(2, 8), nn.LayerNorm(4), nn.Linear(8, 2))
x = torch.tensor([[0.5, -1.0], [1.5, 2.0]])
print(net(x).shape)
```

---

**C4.** [W8] The programmer has **two** sentences and expects the final note of each. The last line prints a shape.
What should it print, and what does it print instead?

```py
import torch
import torch.nn as nn
torch.manual_seed(0)
rnn = nn.RNN(3, 4)
x = torch.ones(2, 5, 3)          # 2 sentences, 5 words, 3 numbers per word
out, h_n = rnn(x)
print(h_n.shape)
```

---

# 🅳 Section D — Do the Arithmetic

*3 questions · 5 marks each · show every line of working · four decimal places.*

---

**D1.** [W2] `f(w) = w²`, so the gradient is `g = 2w`. Start at `w = 1.0`, `lr = 0.2`, three steps.
Momentum is PyTorch's: `v = 0.9·v + g` (`v` starts at 0), then `w = w − 0.2·v`.

| Step | SGD: w before | g | w after |
|:--:|:--:|:--:|:--:|
| 1 | 1.0000 | | |
| 2 | | | |
| 3 | | | |

| Step | Momentum: w before | g | v | w after |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.0000 | | | |
| 2 | | | | |
| 3 | | | | |

**(a)** Fill both tables. *(SGD: 2 marks. Momentum: 2 marks.)*
**(b)** The minimum of `w²` is at `w = 0`. After three steps, which run is closer to it, and what did the other one do? *(1 mark)*

---

**D2.** [W3]
**(a)** The root-mean-square of `[5, −12]`: square, average, root. Show all three. *(2 marks)*
**(b)** Adam, `lr = 0.02`. A weight sits at `1.00` and its **first** gradient is `−4`. Where is the weight after one step? *(2 marks)*
**(c)** Same, but the first gradient is `−4000`. Where is the weight, and in one sentence, why? *(1 mark)*

---

**D3.** [W8] A cell: `new note = tanh( 0.5 × x + 1.0 × old note )`, start note `0`. (You have a calculator with a `tanh` key.)
**(a)** Inputs `x = [2, 0, 0]`: write `0.5·x + 1.0·old` and the new note, for each of the three steps. *(3 marks)*
**(b)** Inputs `x = [0, 0, 2]`: write the **last** note only. *(1 mark)*
**(c)** The inputs add up to the same number both times. In one sentence: what does the pair of final notes show about this cell? *(1 mark)*

---

# 🅴 Section E — Reading Real Curves

*12 marks. The numbers are real, printed by the course harness. **Train** is the average training loss during that epoch; **val** is the validation loss after it; **acc** is validation accuracy. A coin gives a loss of 0.693 and an accuracy of 46.9% on this data.*

Four runs of the same network (4 blocks unless the label says 16) on the same data. AdamW at `lr = 3e-3` unless the label says otherwise, 60 epochs,
seed 1. Each differs from that default in **one** thing, named in the label.

```text
                                      ep 1    ep 5   ep 10   ep 20   ep 40   ep 60
J  depth=16, plain          train    0.694   0.693   0.693   0.693   0.693   0.693
                            val      0.695   0.696   0.695   0.696   0.695   0.695
                            acc      46.9%   46.9%   46.9%   46.9%   46.9%   46.9%
K  depth=16, residual=True  train    1.089   0.056   0.043   0.034   0.014   0.023
                            val      0.461   0.051   0.057   0.037   0.040   0.035
                            acc      76.4%   97.8%   98.9%   99.2%   98.9%   99.2%
L  SGD lr=0.05              train    0.694   0.693   0.693   0.692   0.690   0.681
                            val      0.697   0.696   0.695   0.695   0.692   0.680
                            acc      46.9%   46.9%   46.9%   46.9%   46.9%   56.4%
M  momentum lr=0.05         train    0.694   0.692   0.653   0.446   0.043   0.013
                            val      0.696   0.694   0.624   0.486   0.026   0.051
                            acc      46.9%   46.9%   52.8%   74.4%   99.2%   98.9%
```

**E(a)** *(4 marks, 1 each)* For each of **J, K, L, M**: say in one plain sentence what the run is doing, and quote
**one number** from the table that shows it.

**E(b)** *(4 marks)* A classmate ran the default network at `lr = 1e-2` with and without a cosine schedule, **three seeds each**
(0, 1, 2), 60 epochs, and wrote: *"The cosine schedule halves the loss, so it is clearly better."* The table is the
validation loss at epoch 60.

```text
 schedule    steps   val at epoch 60 (seeds 0, 1, 2)     mean +/- spread
 none          780   [0.059, 0.09, 0.139]               0.096 +/- 0.033
 cosine        780   [0.042, 0.064, 0.05]               0.052 +/- 0.009
```

Use the twice-the-spread rule. Show the gap, twice the larger spread, and the verdict *(3 marks)*. Then say what you would run next
before telling anyone the schedule helps *(1 mark)*.

**E(c)** *(4 marks)* Take run **J**. Write **one row of a playbook**: **SYMPTOM → CHECK → ACTION**. The symptom must quote a number. The check
must be something cheap enough to do in seconds. The action must change **one** knob. Then say what you would run **before** you wrote
the action into the playbook for good.

*End of the paper.*

---

# 💻 PART 2 — THE DEMO

**15 minutes · 15 marks · a computer, your own week files, and the `l4lib` folder. No network, no chatbot.**
*Teacher: sit beside the student. The marks are for what you **watch** and **hear**, so keep the checklist in the marking scheme next to you.*

Open a terminal in the `36-week-course/` folder. Run `export PYTHONPATH="$PWD"` once. Each demo is a new file.
**Say your prediction out loud before you run anything.** A prediction you make after seeing the output does not count.

**Demo 1 — "Check my hand arithmetic" · 5 marks · Weeks 2 and 3**
Write `demo1.py`. **(i)** Using `torch.optim.SGD` with `lr = 0.2` and `momentum = 0.9`, take three steps on `f(w) = w * w` from
`w = 1.0`, printing `w` after each. Your three numbers must match your momentum column of **D1**. **(ii)** Using `torch.optim.Adam` with
`lr = 0.02`, take **one** step from `w = 1.00` with a gradient of `−4`, then again with a gradient of `−4000`. Print both weights. They must
match **D2 (b) and (c)**.

**Demo 2 — "Same bag, different story" · 5 marks · Week 8**
Write `demo2.py`. Set `torch.manual_seed(1)`. Make the four-word vocabulary `the, cat, chased, mouse`, the sentences
`the cat chased the mouse` and `the mouse chased the cat`, an `nn.Embedding(4, 3)` and an `nn.RNN(3, 4, batch_first=True)`
(create them in that order). Print: whether the **bag views** (the average of each sentence's word vectors) are equal, whether the
**final states** are equal, and the size of the difference between the final states.
Predict all three answers first. Then say in one sentence what this does **and does not** show.

**Demo 3 — "Say the row out loud" · 5 marks · Weeks 1, 6 and 7**
Write `demo3.py` with two calls to the course harness, imported as in Week 1 (`from l4lib.spirals import run`): `run("a tag", depth=16, epochs=10, seed=1)`, and the same again with `residual=True` added.
Read the two printed lines. In **thirty seconds**, out loud: the symptom (with a number), the one knob that differs, the cheap check you did,
and what you would still have to run before writing it in a playbook.

*End of Part 2.*

---

# 📊 MARKING SCHEME

**Paper: 75 marks. Demo: 15 marks. Report them separately** — the paper is "can you run code in your head", the demo is
"can you prove it on a machine, in front of someone". A student who is strong on one and weak on the other has told you something that one
sum would hide.

> **Mark Section A first.** It is fast, and the pattern of wrong answers tells you where to look in the rest.
> Below each answer in the key is a sentence on why the wrong options were tempting.

## Section A — 20 marks

| Q | Ans | Week | | Q | Ans | Week |
|:--:|:--:|:--:|---|:--:|:--:|:--:|
| A1 | **c** | W1 | | A11 | **c** | W4 |
| A2 | **b** | W1 | | A12 | **b** | W4 |
| A3 | **c** | W1 | | A13 | **d** | W5 |
| A4 | **d** | W2 | | A14 | **a** | W5 |
| A5 | **a** | W2 | | A15 | **c** | W5 |
| A6 | **b** | W3 | | A16 | **b** | W6 |
| A7 | **c** | W3 | | A17 | **d** | W6 |
| A8 | **a** | W3 | | A18 | **a** | W6 |
| A9 | **d** | W4 | | A19 | **c** | W7 |
| A10 | **b** | W4 | | A20 | **a** | W8 |

No half marks. Two letters circled scores 0. A guess marked "not sure" that is right still scores 1; count the "not sure" ones
separately, because a student who is right and knows they are unsure needs a different conversation from one who is wrong and
sure.

## Section B — 16 marks

**2 marks for every line exactly right. 1 mark if the idea is right and one digit or sign is wrong. 0 otherwise.**
Count lines: a correct first line and a missing second line is 1.

| Q | Exact output | The trap |
|:--:|---|---|
| B1 | `lr=0.01 bs=32 seed=0` | Printing the arguments in the order the call wrote them is fine; the trap is thinking the call needs them in signature order (it does not), or forgetting the default `seed=0`. |
| B2 | `2.0` · `3.8` · `3.42` | Forgetting the `0.9 ×` on the second line (3.8 is `0.9×2.0 + 0.1×20`, not `2.0 + 2.0`). Writing `3.4` for the last. |
| B3 | `9.19` | Stopping before the root (`84.5`) or taking the mean of the raw numbers (`−3.5`). |
| B4 | `0.15` · `0.1` · `0.075` | Printing `0.3`, `0.15`, `0.1`: that is the `lr` *before* each `sched.step()`. The print comes after it, so the first line is already the multiplier `1/2`. Writing `0.3` three times ignores the schedule. |
| B5 | `3 2 True False` | Thinking `alias = w` copies the list (then `alias` would be length 2). It is a second name for the same list; `deepcopy` is the real copy. |
| B6 | `[-1.2247, 0.0, 1.2247]` | Mean 2, deviations −1, 0, 1, spread `√(2/3) = 0.8165`, each divided: `−1/0.8165`. Common slip: dividing by 2 or by 3 instead of 0.8165, giving `−0.5` and `−0.3333`. |
| B7 | `12` · `(0.003, 0.0, 1)` · `(0.01, 0.1, 2)` | Writing 7 (2+2+3). It is `2 × 2 × 3`. The **last** entry varies fastest. |
| B8 | `(3, 5, 7) (1, 3, 7)` | `(3, 5, 6)` (the input size, not the note size) or `h_n` as `(3, 7)` (missing the leading 1). |

## Section C — 12 marks

**3 marks each: (i) the bug named = 1 · (ii) what happens = 1 · (iii) a correct fix = 1.**

| Q | (i) The bug | (ii) What happens | (iii) The fix |
|:--:|---|---|---|
| C1 | Positional arguments to a function whose `*` makes every argument keyword-only | **Loud.** `TypeError: sweep() takes 0 positional arguments but 2 were given` | `print(sweep(lr=0.01, batch_size=64))` |
| C2 | `model.state_dict()` is not a copy: `best` is a live view of the same numbers, so later training rewrites it | **Silent.** Nothing errors; the two printed numbers differ (`-0.0075` then `20.0225`), so the "best" weights are the last weights | `best = copy.deepcopy(model.state_dict())` (and `import copy`) |
| C3 | `nn.LayerNorm(4)` is told 4 features, but the layer before it produces 8 | **Loud.** `RuntimeError: Given normalized_shape=[4], expected input with shape [*, 4], but got input of size[2, 8]` | `nn.LayerNorm(8)` |
| C4 | `nn.RNN(3, 4)` was built without `batch_first=True`, so it read the `(2, 5, 3)` tensor as 2 time steps of a batch of 5 | **Silent.** It prints `torch.Size([1, 5, 4])` — five final states, not two. Should be `torch.Size([1, 2, 4])` | `rnn = nn.RNN(3, 4, batch_first=True)` |

For C2 and C4, a student who says "it crashes" has not understood the bug. Accept "it prints something wrong" for (ii).
Accept any fix that produces the expected result; the key fixes above were run (see the key).

## Section D — 15 marks

| Part | Marks | What earns them |
|---|:--:|---|
| D1 SGD table | 2 | 0.6000 · 0.3600 · 0.2160, with the `g` column 2.0000 · 1.2000 · 0.7200. 1 mark if one row is wrong. |
| D1 momentum table | 2 | `v` 2.0000 · 3.0000 · 2.7000; `w` 0.6000 · 0.0000 · −0.5400. 1 mark if `v` is right but `w` has a slip. |
| D1(b) | 1 | **Plain SGD** (0.2160, versus momentum's −0.5400, which is 0.54 from zero). Momentum rolled **past** the minimum. |
| D2(a) | 2 | squares `25, 144` · mean `84.5` · root `9.1924`. 1 mark for the right method and an arithmetic slip. |
| D2(b) | 2 | `1.0200`. Negative gradient moves the weight **up**. 1 mark for `0.9800` (sign wrong). |
| D2(c) | 1 | `1.0200`, with "the first Adam step is `lr` in size, whatever the size of the gradient (the typical size cancels the scale)". |
| D3(a) | 3 | `1.0 → 0.7616` · `0.7616 → 0.6420` · `0.6420 → 0.5663`. 1 mark per row. |
| D3(b) | 1 | `0.7616` (the first two notes are 0). |
| D3(c) | 1 | Order matters: **the same bag of inputs gives different final notes** (0.5663 against 0.7616), so a cell that reads in order can tell them apart. Bonus words ("the early spike fades, the late one is still fresh") are welcome, not required. |

## Section E — 12 marks

| Part | Marks | What earns them |
|---|:--:|---|
| E(a) J | 1 | Stuck at the coin for all 60 epochs; quotes e.g. `val 0.695 at epoch 60` or `acc 46.9%` throughout. |
| E(a) K | 1 | Learns: `val 0.051 at epoch 5`, `0.035 at epoch 60`, `acc 99.2%`. (A rough start — `train 1.089` at epoch 1 is above the coin — is a bonus observation.) |
| E(a) L | 1 | Barely leaves the coin: `val 0.695 at epoch 10`, `0.680 at epoch 60`, `acc 56.4%`; too slow, not failed. |
| E(a) M | 1 | Sits at the coin, then falls: `val 0.694 at epoch 5`, `0.486 at epoch 20`, `0.026 at epoch 40`, `acc 98.9%`. L and M differ only in momentum. |
| E(b) numbers | 3 | **gap** `|0.096 − 0.052| = 0.044` · **twice the larger spread** `2 × 0.033 = 0.066` · **verdict: inside noise** (0.044 < 0.066). One mark each. The classmate's "halves the loss" is a gap in means with no spread. |
| E(b) next | 1 | More seeds (e.g. ten), because the noise is one wild run: `0.139` at seed 2 makes the spread 0.033. Accept also "look at each seed" *if* they say it is suggestive, not proof (cosine is lower on all three seeds in the table). |
| E(c) symptom | 1 | A sentence with a number: e.g. "train and val both ≈ 0.69 and accuracy 46.9% from epoch 1 to epoch 60: no learning". |
| E(c) check | 1 | Cheap and quick: "print the gradient size for the first block against the last", "does the loss move at all in the first 5 epochs", "is `lr` wildly small?" Any check that can be run in seconds. |
| E(c) action | 1 | **One** knob: `residual=True` (the Week 6 fix, and what K did). "Raise `lr` **and** add residual" scores 0 here: that is two knobs. |
| E(c) before | 1 | Run it at **three seeds** and apply the twice-the-spread rule; K is one seed only. Bonus: rule out `lr` by trying a second value. |

## Part 2 — the demo, 15 marks

| | Marks | The teacher watches for |
|---|:--:|---|
| **Demo 1** | 5 | prediction said first (1) · momentum prints `0.6000`, `0.0000`, `-0.5400` (2; `-0.0000` is the same number) · Adam prints `1.0200` twice (2) |
| **Demo 2** | 5 | prediction said first (1) · prints `bag views equal: True` (1) · `final states equal: False` (1) · a non-zero difference, `0.6244` with the stated seed and construction order (1) · the sentence: *"the states differ because the cell reads in order; they do not yet **mean** anything, because the weights are random"* (1) |
| **Demo 3** | 5 | both lines run (1) · symptom with a number: plain `val 0.695  acc 46.9%` (1) · names the knob (`residual`) and the check (1) · says the residual line reached `val 0.057  acc 98.9%` (1) · says it is **one seed**, so three are needed before it goes in a playbook (1) |

> **Reference output of the three demos** (what a correct `demo1.py`, `demo2.py` and `demo3.py` print) is in the key. If the student's
> numbers differ in the last digit on your machine, that is the CPU; a difference in the first digit is a bug — ask them to find it
> (the Debugging Clinic habit of Week 9).

## How to read the score

These thresholds are suggestions; nothing in the course depends on them.

| Paper | What it probably means |
|:--:|---|
| 60–75 | Term 2 can start as planned. |
| 45–59 | Fine to start Term 2. Redo the one or two weeks in the grid below that scored under 60%. |
| under 45 | Do **not** read this as a verdict. Check Section A against the demo first: a student who knew it at the machine and lost it on paper needs a different plan from one who lost it on both. Redo at most two weeks, then re-sit the Week 9 paper. |

### The per-week grid

Add up the marks the student earned on these questions, and divide by the total shown.

| Week | Questions | Marks available | Redo this week if under |
|:--:|---|:--:|:--:|
| [1](../student-guide/week-01.md) | A1–A3, B1, C1 | 8 | 5 |
| [2](../student-guide/week-02.md) | A4–A5, B2, D1, E(a) L and M | 11 | 7 |
| [3](../student-guide/week-03.md) | A6–A8, B3, D2 | 10 | 6 |
| [4](../student-guide/week-04.md) | A9–A12, B4 | 6 | 4 |
| [5](../student-guide/week-05.md) | A13–A15, B5, C2 | 8 | 5 |
| [6](../student-guide/week-06.md) | A16–A18, B6, C3, E(a) J and K | 10 | 6 |
| [7](../student-guide/week-07.md) | A19, B7, E(b), E(c) | 11 | 7 |
| [8](../student-guide/week-08.md) | A20, B8, C4, D3 | 11 | 7 |
| **Total** | | **75** | |

Three weeks carry Term 2: **Week 2** (the running average is Week 11's gate), **Week 6** (the residual road is Week 11's highway)
and **Week 8** (the cell is Week 10's whole subject). If any of those is under the threshold, redo it first.

---

# ✅ ANSWER KEY

> **🧑‍🏫 Do not show this to the student until after the test is marked.** It contains every answer and names the mistakes the
> student is expected to make. **Every code block in this key was run, and the real output is pasted in unedited.**

## Section A — why each answer, and why the wrong ones were tempting

<details>
<summary><b>A1 – A3 · Week 1</b></summary>

**A1 — (c) 1.386.** Guessing evenly over 4 classes gives each a probability of 0.25, and the loss is `−ln(0.25) = ln 4`. (b) is the
two-class coin; students who only remember "0.693 is a coin" pick it. (a) is the probability, not the loss. (d) is the number of classes.

**A2 — (b).** A sweep calls the harness hundreds of times, and `run(0.001, 64, 0)` is unreadable and silently swaps two numbers if the
signature is ever reordered. (a) confuses `*` with defaults; (c) is `*args`, a different construct; (d) is nonsense but tempting if the
student knows nothing.

**A3 — (c).** A curve that is still falling has not finished. The one-knob tests are more epochs (`epochs` is set-up) or a larger `lr`.
(a) "converged" needs a flat curve; (b) overfitting needs validation to rise while training falls.
</details>

<details>
<summary><b>A4 – A5 · Week 2</b></summary>

**A4 — (d) 10 × g.** `v = 0.9v + g` settles where `v = 0.9v + g`, so `0.1v = g` and `v = 10g`. The afacts run below shows it:
after sixty steps of `g = 1`, `v = 9.982`. (a) is the share that *stays*, not the total; (b) is plain SGD; (c) multiplies by 0.9 twice over.

**A5 — (a) 1.0.** `0.9 × 0 + 0.1 × 10 = 1.0`. (d) is the student who forgot the average starts at 0 and that it moves slowly;
(b) is `0.9 × 10`, the two weights swapped.
</details>

<details>
<summary><b>A6 – A8 · Week 3</b></summary>

**A6 — (b) 7.07.** Squares `0, 100`; mean `50`; root `7.0711`. (a) is the plain mean (`5`), which is what "typical" sounds like
and is wrong because RMS squares first. (d) stops before the root.

**A7 — (c).** Epsilon is added to what you divide by, so a zero never appears. (a) is wrong in the other direction: it should be too small to
change any normal step. (b) and (d) are what AdamW and momentum do.

**A8 — (a).** The first Adam step is `lr × g / (typical size of g)`, and after one gradient the typical size is `|g|`, so the step is `lr`
(to within eps) for a gradient of 0.5 **and** of 500. (b) is plain SGD thinking (`lr × g`, so a bigger gradient means a bigger step); (c) is a mix-up of the division; (d) confuses "tiny gradient" with "no move".
</details>

<details>
<summary><b>A9 – A12 · Week 4</b></summary>

**A9 — (d) 0.1.** After two steps the multiplier is `1/(1+2) = 1/3`, and `0.3 × 1/3 = 0.1`. (b) is one step (`1/2`); (c) is three steps'
worth; (a) ignores the schedule.

**A10 — (b) 0.5.** `(9 + 1)/20`. (c) is the off-by-one: using `s/20` gives `0.45`, which is what counting from 0 but forgetting the `+ 1` looks like.

**A11 — (c) 240.** `840 // 128 = 6` (six whole batches, 72 examples left over), and `6 × 40 = 240`. (b) rounds up to 7 batches and
gets 280; `//` throws the leftovers away. (d) is the per-epoch count; (a) is 840 ÷ 20.

**A12 — (b) 1040 and 120.** Batch 32: `840 // 32 = 26` per epoch × 40 = 1040. Batch 256: `840 // 256 = 3` × 40 = 120. The bigger batch takes
about 8.7 times **fewer** steps, which is why "bigger batch is better/worse" is confounded with the number of steps. (c) rounds up; (a) forgets the
epochs; (d) is the epoch count.
</details>

<details>
<summary><b>A13 – A15 · Week 5</b></summary>

**A13 — (d) about 1.43.** Survivors are multiplied by `1 / (1 − 0.3) = 1 / 0.7 = 1.4286`, so the *average* stays the same. (a) is the keep
probability; (b) is the drop probability; (c) would make the layer's output smaller on average.

**A14 — (a).** Ship the weights from the lowest **validation** loss. (b) and (d) are what overfitting *chases*; (c) is the common slip of
shipping whatever the loop ended on.

**A15 — (c) 0.995.** `1 − 0.01 × 0.5 = 1 − 0.005 = 0.995`. (b) forgets the `× 0.5` (that is `1 − 0.01`); (a) is the weight decay itself;
(d) has an extra zero.
</details>

<details>
<summary><b>A16 – A18 · Week 6</b></summary>

**A16 — (b).** Batch norm takes its mean and spread from the *other examples in the batch*, and one example has no others. Layer norm looks
at one example's own features only. (c) is the student who remembers "a norm fails" without knowing which. (a) is the reverse of the truth.

**A17 — (d) 0.6.** `1 + (−0.4) = 0.6`. Nudge `x` by 0.001 and `y` moves by 0.0006 (the afacts run below). (a) forgets the 1; (b) drops the sign;
(c) adds `0.4` instead of `−0.4`.

**A18 — (a).** Around every block there is a route whose slope is exactly 1, so the error coming back has something that does not shrink as it
passes each block. (b), (c) and (d) are each true of some other technique, and false of this one.
</details>

<details>
<summary><b>A19 – A20 · Weeks 7 and 8</b></summary>

**A19 — (c) better.** Gap `|0.653 − 0.042| = 0.611`. Twice the larger spread is `2 × 0.020 = 0.040`. `0.611 > 0.040`, so a real difference,
and lower loss is better. (a) reads a *lower* number as worse; (b) is the student who never divides; (d) is a test-set answer to a question
that was about the validation table. The run that produced these three-seed numbers is the `a19` block.

**A20 — (a) 36.** `4 × 3` (input to note) `+ 4 × 4` (note to note) `+ 4 + 4` (two bias lists) `= 12 + 16 + 4 + 4 = 36`. (d) 28 forgets both
biases; (b) and (c) are each one weight table only.
</details>

### The Section A facts, run

```py
import math
import torch
torch.set_num_threads(1)

print("A1  ln 4            =", round(math.log(4), 4))
v = 0.0
for n in range(60):
    v = 0.9 * v + 1.0                       # the same gradient, g = 1, sixty times
print("A4  velocity after 60 steps of g=1 =", round(v, 3))
print("A5  0.9*0 + 0.1*10  =", round(0.9 * 0 + 0.1 * 10, 2))
x = torch.tensor([0.0, 10.0])
print("A6  rms [0, 10]     =", round(torch.sqrt((x * x).mean()).item(), 4), "  (mean would be", x.mean().item(), ")")

p = torch.tensor([0.0], requires_grad=True)
opt = torch.optim.SGD([p], lr=0.3)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1 / (1 + s))
for _ in range(2):
    opt.step(); sched.step()
print("A9  lr after 2 steps =", round(sched.get_last_lr()[0], 4))
print("A10 warmup multiplier at s=9, W=20 =", (9 + 1) / 20)
print("A11 steps =", (840 // 128) * 40, " (per epoch", 840 // 128, ")")
print("A12 batch 32:", (840 // 32) * 40, " batch 256:", (840 // 256) * 40, " ceil trap:", -(-840 // 32) * 40, -(-840 // 256) * 40)
print("A13 dropout survivor scale 1/0.7 =", round(1 / 0.7, 4))
print("A15 weight decay fee 1 - 0.01*0.5 =", round(1 - 0.01 * 0.5, 4))

a = torch.tensor([0.0]); b = torch.tensor([0.001])
f = lambda t: t + (-0.4) * t                # y = x + f(x), f has slope -0.4
print("A17 slope of y =", round(((f(b) - f(a)) / 0.001).item(), 3))
import torch.nn as nn
rnn = nn.RNN(3, 4)
print("A20 parameters in nn.RNN(3, 4) =", sum(q.numel() for q in rnn.parameters()), "  (4x3 + 4x4 + 4 + 4 =", 4*3 + 4*4 + 4 + 4, ")")
```
```text
A1  ln 4            = 1.3863
A4  velocity after 60 steps of g=1 = 9.982
A5  0.9*0 + 0.1*10  = 1.0
A6  rms [0, 10]     = 7.0711   (mean would be 5.0 )
A9  lr after 2 steps = 0.1
A10 warmup multiplier at s=9, W=20 = 0.5
A11 steps = 240  (per epoch 6 )
A12 batch 32: 1040  batch 256: 120  ceil trap: 1080 160
A13 dropout survivor scale 1/0.7 = 1.4286
A15 weight decay fee 1 - 0.01*0.5 = 0.995
A17 slope of y = 0.6
A20 parameters in nn.RNN(3, 4) = 36   (4x3 + 4x4 + 4 + 4 = 36 )
```

### A19, run

```py
import numpy as np
import torch
torch.set_num_threads(1)
from l4lib.spirals import run

def three(**kw):
    v = [run("x", verbose=False, seed=s, **kw)["val"][-1] for s in (0, 1, 2)]
    return [round(x, 3) for x in v], round(float(np.mean(v)), 3), round(float(np.std(v)), 3)

for name, kw in [("SGD lr=0.05", dict(optimizer="sgd", lr=0.05)),
                 ("momentum lr=0.05", dict(optimizer="momentum", lr=0.05))]:
    vals, m, s = three(**kw)
    print(f"{name:<18} val at epoch 60 {vals}  mean {m}  spread {s}")
```
```text
SGD lr=0.05        val at epoch 60 [0.648, 0.68, 0.63]  mean 0.653  spread 0.02
momentum lr=0.05   val at epoch 60 [0.034, 0.051, 0.041]  mean 0.042  spread 0.007
```

---

## Section B — outputs, run

<details>
<summary><b>B1 – B4</b></summary>

**B1**
```text
lr=0.01 bs=32 seed=0
```
The `*` forces names; `seed` has a default so it is allowed to be missing.

**B2**
```text
2.0
3.8
3.42
```
`0.9 × 0 + 0.1 × 20 = 2.0`; `0.9 × 2.0 + 0.1 × 20 = 1.8 + 2.0 = 3.8`; `0.9 × 3.8 + 0.1 × 0 = 3.42`.

**B3**
```text
9.19
```
Squares `25, 144` → mean `84.5` → root `9.1924` → `9.19`.

**B4**
```text
0.15
0.1
0.075
```
After the first `sched.step()` the multiplier is `1/(1+1) = 0.5` → `0.3 × 0.5 = 0.15`; then `1/3` → `0.1`; then `1/4` → `0.075`.
</details>

<details>
<summary><b>B5 – B8</b></summary>

**B5**
```text
3 2 True False
```
`alias` is the same list as `w` (so it grew to 3, and `alias is w` is `True`). `snap` is a deep copy (still 2, and not `w`).

**B6**
```text
[-1.2247, 0.0, 1.2247]
```
Mean `2`; deviations `−1, 0, 1`; mean of squares `2/3 = 0.6667`; root `0.8165`; `−1 / 0.8165 = −1.2247`.

**B7**
```text
12
(0.003, 0.0, 1)
(0.01, 0.1, 2)
```
Two learning rates × two decays × three seeds = `2 × 2 × 3 = 12`. The index-1 entry changes the last list first.

**B8**
```text
(3, 5, 7) (1, 3, 7)
```
`out` is `(batch 3, time 5, note 7)`; `h_n` is `(1 layer, batch 3, note 7)`.
</details>

---

## Section C — bugs, run

<details>
<summary><b>C1 – C2</b></summary>

**C1** — the real traceback:
```text
Traceback (most recent call last):
  File "c1.py", line 4, in <module>
    print(sweep(0.01, 64))
TypeError: sweep() takes 0 positional arguments but 2 were given
```
Fix: `print(sweep(lr=0.01, batch_size=64))`.

**C2** — the printed result of the buggy code (the two numbers are the weight at the best epoch, and the "best" weights after more training):
```text
-0.0075 20.0225
```
`state_dict()` hands back the live tensors, not copies, so one gradient step rewrites what `best` points to. The fixed program:
```py
import copy
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Linear(1, 1, bias=False)
best = copy.deepcopy(model.state_dict())
at_best = round(best["weight"].item(), 4)

opt = torch.optim.SGD(model.parameters(), lr=0.5)
x = torch.tensor([[2.0]])
loss = (model(x) - 10.0) ** 2
opt.zero_grad()
loss.backward()
opt.step()

print(at_best, round(best["weight"].item(), 4), round(model.weight.item(), 4))
```
```text
-0.0075 -0.0075 20.0225
```
`best` stays at `-0.0075` while the model moves on to `20.0225`.
</details>

<details>
<summary><b>C3 – C4</b></summary>

**C3** — the real traceback (the long middle is PyTorch's own frames; the last line is the one to read):
```text
Traceback (most recent call last):
  File "c3.py", line 6, in <module>
    print(net(x).shape)
  File ".../site-packages/torch/nn/modules/module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File ".../site-packages/torch/nn/modules/module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File ".../site-packages/torch/nn/modules/container.py", line 217, in forward
    input = module(input)
  File ".../site-packages/torch/nn/modules/module.py", line 1511, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File ".../site-packages/torch/nn/modules/module.py", line 1520, in _call_impl
    return forward_call(*args, **kwargs)
  File ".../site-packages/torch/nn/modules/normalization.py", line 201, in forward
    return F.layer_norm(
  File ".../site-packages/torch/nn/functional.py", line 2546, in layer_norm
    return torch.layer_norm(input, normalized_shape, weight, bias, eps, torch.backends.cudnn.enabled)
RuntimeError: Given normalized_shape=[4], expected input with shape [*, 4], but got input of size[2, 8]
```
Plain words: the layer after `Linear(2, 8)` hands over rows of 8 numbers, but `LayerNorm(4)` was told the last dimension is 4. The fixed program:
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
net = nn.Sequential(nn.Linear(2, 8), nn.LayerNorm(8), nn.Linear(8, 2))
x = torch.tensor([[0.5, -1.0], [1.5, 2.0]])
print(net(x).shape)
```
```text
torch.Size([2, 2])
```

**C4** — the printed result of the buggy code:
```text
torch.Size([1, 5, 4])
```
Without `batch_first=True` the layer reads the first dimension as time, so it saw 2 steps of 5 sentences. No error, because the numbers fit. The fixed program:
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
rnn = nn.RNN(3, 4, batch_first=True)
x = torch.ones(2, 5, 3)
out, h_n = rnn(x)
print(h_n.shape)
```
```text
torch.Size([1, 2, 4])
```
</details>

---

## Section D — worked answers

```py
import torch

def steps(momentum):
    w = torch.tensor([1.0], requires_grad=True)
    opt = torch.optim.SGD([w], lr=0.2, momentum=momentum)
    out = []
    for _ in range(3):
        opt.zero_grad(set_to_none=True)
        loss = w * w                              # gradient is 2w
        loss.backward()
        g = w.grad.item()
        opt.step()
        out.append((round(g, 4), round(w.item(), 4)))
    return out

print("plain SGD   (g, w after):", steps(0.0))
print("momentum 0.9 (g, w after):", steps(0.9))

# the velocity by hand
w, v = 1.0, 0.0
for i in range(3):
    g = 2 * w
    v = 0.9 * v + g
    w = w - 0.2 * v
    print(f"step {i+1}: g={g:.4f}  v={v:.4f}  w={w:.4f}")
```
```text
plain SGD   (g, w after): [(2.0, 0.6), (1.2, 0.36), (0.72, 0.216)]
momentum 0.9 (g, w after): [(2.0, 0.6), (1.2, 0.0), (0.0, -0.54)]
step 1: g=2.0000  v=2.0000  w=0.6000
step 2: g=1.2000  v=3.0000  w=-0.0000
step 3: g=-0.0000  v=2.7000  w=-0.5400
```

**D1 (a)** Plain SGD: `w ← w − 0.2 × 2w`, so each step multiplies `w` by `0.6`.

| Step | SGD: w before | g | w after |
|:--:|:--:|:--:|:--:|
| 1 | 1.0000 | 2.0000 | **0.6000** |
| 2 | 0.6000 | 1.2000 | **0.3600** |
| 3 | 0.3600 | 0.7200 | **0.2160** |

| Step | Momentum: w before | g | v = 0.9·v + g | w after = w − 0.2·v |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.0000 | 2.0000 | 0.9×0 + 2.0 = **2.0000** | 1.0 − 0.4000 = **0.6000** |
| 2 | 0.6000 | 1.2000 | 0.9×2.0 + 1.2 = **3.0000** | 0.6 − 0.6000 = **0.0000** |
| 3 | 0.0000 | 0.0000 | 0.9×3.0 + 0.0 = **2.7000** | 0.0 − 0.5400 = **−0.5400** |

**D1 (b)** Plain SGD ends at `0.2160`. Momentum ends at `−0.5400`, which is further away, on the other side. At step 2 the weight was sitting exactly on the minimum
with a velocity of `3.0`; the velocity does not vanish when the gradient does, so it rolled through. (The code prints `-0.0000` for a value a hair below zero: the same number.)

**D2** ```text
a) squares [25.0, 144.0]  mean 84.5  rms 9.1924
gradient     -4.0: weight after one Adam step = 1.0200
gradient  -4000.0: weight after one Adam step = 1.0200
```

(a) squares `25` and `144`; average `(25 + 144) / 2 = 84.5`; root `√84.5 = 9.1924`.
(b) The first step is `lr` in size, moving against the gradient's sign. The gradient is `−4` (negative), so the weight goes **up**: `1.00 + 0.02 = 1.0200`.
(c) `1.0200` again. After one gradient the typical size is `|g|`, so the step is `lr × g / |g| = ±lr` whatever the size of `g` (to within eps).

**D3** ```text
x = [2, 0, 0]: [(1.0, 0.7616), (0.7616, 0.642), (0.642, 0.5663)]
x = [0, 0, 2]: [(0.0, 0.0), (0.0, 0.0), (1.0, 0.7616)]
nn.RNN [2.0, 0.0, 0.0] [0.7616, 0.642, 0.5663]
nn.RNN [0.0, 0.0, 2.0] [0.0, 0.0, 0.7616]
```

(a)

| Step | x | 0.5·x + 1.0·(old note) | new note = tanh of that |
|:--:|:--:|---|---|
| 1 | 2 | 1.0 + 0 = **1.0000** | tanh(1.0000) = **0.7616** |
| 2 | 0 | 0 + 0.7616 = **0.7616** | tanh(0.7616) = **0.6420** |
| 3 | 0 | 0 + 0.6420 = **0.6420** | tanh(0.6420) = **0.5663** |

(b) Steps 1 and 2 add 0 to 0, so the note stays `0.0000`. Step 3: `0.5 × 2 + 0 = 1.0`, `tanh(1.0) = 0.7616`.
(c) Same inputs, same total, final notes `0.5663` and `0.7616`: the cell is **not** a bag; the note remembers that the spike was early (and faded) or late (still fresh). The last line of the `nn.RNN` check agrees with the by-hand numbers.

---

## Section E — worked answers

The tables printed on the paper came from these two blocks.

```py
import torch
torch.set_num_threads(1)
from l4lib.spirals import run

runs = [("J", "depth=16, plain",                dict(depth=16)),
        ("K", "depth=16, residual=True",        dict(depth=16, residual=True)),
        ("L", "SGD lr=0.05",                    dict(optimizer="sgd", lr=0.05)),
        ("M", "momentum lr=0.05",               dict(optimizer="momentum", lr=0.05))]
cols = [0, 4, 9, 19, 39, 59]
print(f"{'':<34}" + "".join(f"ep {c+1}".rjust(8) for c in cols))
for name, label, kw in runs:
    h = run(name, verbose=False, seed=1, **kw)
    print(f"{name}  {label:<24} train " + "".join(f"{h['train'][c]:8.3f}" for c in cols))
    print(f"{'':<28}val   " + "".join(f"{h['val'][c]:8.3f}" for c in cols))
    print(f"{'':<28}acc   " + "".join(f"{h['acc'][c]*100:7.1f}%" for c in cols))
```
```text
                                      ep 1    ep 5   ep 10   ep 20   ep 40   ep 60
J  depth=16, plain          train    0.694   0.693   0.693   0.693   0.693   0.693
                            val      0.695   0.696   0.695   0.696   0.695   0.695
                            acc      46.9%   46.9%   46.9%   46.9%   46.9%   46.9%
K  depth=16, residual=True  train    1.089   0.056   0.043   0.034   0.014   0.023
                            val      0.461   0.051   0.057   0.037   0.040   0.035
                            acc      76.4%   97.8%   98.9%   99.2%   98.9%   99.2%
L  SGD lr=0.05              train    0.694   0.693   0.693   0.692   0.690   0.681
                            val      0.697   0.696   0.695   0.695   0.692   0.680
                            acc      46.9%   46.9%   46.9%   46.9%   46.9%   56.4%
M  momentum lr=0.05         train    0.694   0.692   0.653   0.446   0.043   0.013
                            val      0.696   0.694   0.624   0.486   0.026   0.051
                            acc      46.9%   46.9%   52.8%   74.4%   99.2%   98.9%
```

**E(a)** — model sentences:
- **J (depth 16, plain)** — stuck: train and val sit at the coin for the whole run (`val 0.695` at epoch 60, `acc 46.9%` at every column). Nothing is learned.
- **K (depth 16, residual)** — learns fast: `val 0.051` by epoch 5, `0.035` at epoch 60, `acc 99.2%`. The epoch-1 `train 1.089` is a rough first epoch, not a failure.
- **L (SGD, lr 0.05)** — barely leaves the coin: `val 0.695` at epoch 10, `0.680` at epoch 60, `acc 56.4%`. Very slow, and perhaps about to take off; not a dead run.
- **M (momentum, lr 0.05)** — the same start as L, then it falls: `val 0.694` at epoch 5, `0.486` at epoch 20, `0.026` at epoch 40, `acc 98.9%`. L and M differ only in momentum.

**E(b)**

```py
import numpy as np
import torch
torch.set_num_threads(1)
from l4lib.spirals import run

print(" schedule    steps   val at epoch 60 (seeds 0, 1, 2)     mean +/- spread")
for name, kw in [("none", dict(lr=1e-2)), ("cosine", dict(lr=1e-2, schedule="cosine"))]:
    v = [run("x", verbose=False, seed=s, **kw)["val"][-1] for s in (0, 1, 2)]
    print(f" {name:<10}  {13*60:>5}   {str([round(x, 3) for x in v]):<34} {np.mean(v):.3f} +/- {np.std(v):.3f}")
```
```text
 schedule    steps   val at epoch 60 (seeds 0, 1, 2)     mean +/- spread
 none          780   [0.059, 0.09, 0.139]               0.096 +/- 0.033
 cosine        780   [0.042, 0.064, 0.05]               0.052 +/- 0.009
```

```py
gap = abs(0.096 - 0.052)
print("gap            =", round(gap, 3))
print("2 x larger spread =", round(2 * 0.033, 3))
print("verdict        =", "inside noise" if gap < 2 * 0.033 else "a real difference")
```
```text
gap            = 0.044
2 x larger spread = 0.066
verdict        = inside noise
```

- gap `|0.096 − 0.052| = 0.044`
- twice the larger spread: `2 × 0.033 = 0.066`
- `0.044 < 0.066`: **inside noise**. The step counts are equal (780 each), so the comparison is at least fair on steps. But the "no schedule" row has a wild seed (`0.139`), and that one run makes the spread wide.
- Next: more seeds (say ten) for each. Note that cosine is lower on each of the three seeds, which is suggestive and not a proof. A student may also say "a cosine run with a different `lr`" — accept as a follow-up, not a replacement.

**E(c)** — a model row:

> **SYMPTOM:** train and val loss both ≈ 0.69 and accuracy 46.9% at epoch 1 and still at epoch 60 (run J, depth 16, plain). → **CHECK:** do the first 5 epochs move at all, and is the gradient size at the first block tiny next to the last block? (seconds) → **ACTION:** set `residual=True`, changing nothing else. → **Before it goes in the playbook:** run it at three seeds (0, 1, 2) and apply the twice-the-spread rule, because K is one seed; and rule out `lr` by checking that a second `lr` does not fix J.

---

## Part 2 — the demo, reference output

**Demo 1** — what a correct `demo1.py` prints:
```py
import torch
torch.set_num_threads(1)

# Part (i): three steps on f(w) = w*w from w = 1.0, lr = 0.2, momentum 0.9
w = torch.tensor([1.0], requires_grad=True)
opt = torch.optim.SGD([w], lr=0.2, momentum=0.9)
for i in range(3):
    opt.zero_grad(set_to_none=True)
    (w * w).backward()
    opt.step()
    print(f"step {i + 1}: w = {w.item():.4f}")

# Part (ii): Adam's first step, two very different gradients, lr = 0.02, start w = 1.00
for grad in (-4.0, -4000.0):
    w = torch.tensor([1.00], requires_grad=True)
    opt = torch.optim.Adam([w], lr=0.02)
    (grad * w.sum()).backward()
    opt.step()
    print(f"gradient {grad:>8}: w after one Adam step = {w.item():.4f}")
```
```text
step 1: w = 0.6000
step 2: w = 0.0000
step 3: w = -0.5400
gradient     -4.0: w after one Adam step = 1.0200
gradient  -4000.0: w after one Adam step = 1.0200
```

**Demo 2** — what a correct `demo2.py` prints:
```py
import torch
import torch.nn as nn
torch.manual_seed(1)

vocab = ["the", "cat", "chased", "mouse"]
ids = {w: i for i, w in enumerate(vocab)}
a = "the cat chased the mouse"
b = "the mouse chased the cat"
x_ids = torch.tensor([[ids[w] for w in a.split()], [ids[w] for w in b.split()]])

emb = nn.Embedding(4, 3)
rnn = nn.RNN(3, 4, batch_first=True)
vecs = emb(x_ids)
out, h_n = rnn(vecs)

bag = vecs.mean(dim=1)
print("ids:", x_ids.tolist())
print("bag views equal:  ", torch.allclose(bag[0], bag[1], atol=1e-6))
print("final states equal:", torch.allclose(h_n[0, 0], h_n[0, 1], atol=1e-6))
print("size of difference:", round((h_n[0, 0] - h_n[0, 1]).norm().item(), 4))
```
```text
ids: [[0, 1, 2, 0, 3], [0, 3, 2, 0, 1]]
bag views equal:   True
final states equal: False
size of difference: 0.6244
```

The `ids` line is the sentence as word numbers; the two are the same five numbers in a different order. The bag views are equal, so a bag cannot tell them apart; the final states are not. The numbers mean nothing yet, because the weights are random.
**The sentence to listen for:** the states *can* depend on the order; this does not show the cell understands anything.

**Demo 3** — what a correct `demo3.py` prints:
```py
import torch
torch.set_num_threads(1)
from l4lib.spirals import run

run("depth 16, plain, 10 epochs",    depth=16,                 epochs=10, seed=1)
run("depth 16, residual, 10 epochs", depth=16, residual=True,  epochs=10, seed=1)
```
```text
depth 16, plain, 10 epochs   train 0.693  val 0.695  acc  46.9%
depth 16, residual, 10 epochs train 0.043  val 0.057  acc  98.9%
```

The first line is J's symptom (`val 0.695`, `acc 46.9%`); the second is K's cure (`val 0.057`, `acc 98.9%`). These are 10-epoch runs, so they differ from the 60-epoch
table on the paper. The right thing to hear: one knob (`residual`), one seed, so **three seeds before this goes in a playbook**.

---

## 🧭 What this test does and does not show

1. **It is one sample.** A student who was ill, hungry or anxious scores lower than they know. Treat the pattern across weeks as the information and the total as almost none.
2. **Multiple choice can be guessed.** Twenty 4-option questions guessed at random average 5 marks. That is why only 20 of the 75 marks are there and why every wrong option was built from a real mistake.
3. **The Section E tables are one network, one dataset and one seed set.** They show four *symptoms*, not four laws. "Depth 16 without residuals stalls" is true of this network and these seeds; nothing on this test claims it about other networks.
4. **The demo marks a conversation.** The student's own words at the machine are the evidence; do not help, and do not mark a sentence the student was handed.
5. **Not on this test, on purpose:** anything from Weeks 10 onwards. If a student writes "vanishing gradient", "LSTM", or "attention" anywhere, do not mark it wrong and do not mark it extra; it comes from next term. Say so kindly on the sheet.

**Nothing on the ladder is used before its week.** The constructs on this test are, by week: W1 keyword-only `*`, `torch.set_num_threads`; W2
`SGD(momentum=)`, `zero_grad(set_to_none=True)`; W3 `Adam`, `torch.sqrt`; W4 `lambda`, `LambdaLR`, `step()`, `get_last_lr()`; W5 `copy.deepcopy(model.state_dict())`;
W6 `nn.LayerNorm`; W7 `itertools.product`; W8 `nn.Embedding`, `nn.RNN(batch_first=True)`, `out, h_n = rnn(x)`. Section D's "root-mean-square" is Week 3's maths, the "twice the spread" rule is Week 7's,
and the "slope of a sum" (A17) is Week 6's.
