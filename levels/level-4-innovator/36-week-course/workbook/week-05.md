# Workbook — Week 5: Four Ways to Stop Memorising

**Name:** ________________________________  **Date:** ______________

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [📖 Read the chapter first](../student-guide/week-05.md) · [Next ➡ Week 6](week-06.md)

---

> **Rules for this workbook.** Every number you write in a report must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the Answers were produced by real runs on one CPU thread (`torch.set_num_threads(1)`, torch 2.2.1, numpy 1.26.4). If your third decimal differs, that is fine. If the *shape* differs, tell your teacher.
>
> Run everything from inside `36-week-course/` (with `export PYTHONPATH="$PWD"`) so that `from l4lib.spirals import ...` works. **Import `l4lib`. Never copy it.** Pages 5.5 and 5.6 also need your own `lab.py` and `patience.py` from the lesson.
>
> **This week has no new maths.** You need only: multiply by a number just under 1, and `//` ("how many whole ones fit"). **Pages 5.3 and 5.4 are paper and calculator only. No code.**
>
> **The sentence of the week:** *"Which column would I get to keep?"* Say it out loud before you write any conclusion.

---

![Level 4 map with four rows of nine tiles, one row per term; in the first row week 5 is highlighted with a pointer above it, weeks 1 to 4 are outlined solid, and every later tile has a dashed outline](../figures/fig-w05-0-where-this-fits.svg)
*Figure W5.0 — Where this fits: week 5 of 36 sits in term 1, "train it on purpose"; the tiles still dashed are the weeks to come.*

## ✅ Warm-Up (5 min)

Five from **last week** and earlier. No looking back.

**W1.** A loop calls `opt.step()` but never `sched.step()`. Does the learning rate change? ____________

**W2.** `840 // 150` = ______ steps per epoch. How many points are left out in each epoch? ______

**W3.** What number is the loss of a model that guesses between two classes? ____________

**W4.** "What did I hold fixed?" Finish the sentence in your own words: *If two things changed at once, it is called a* ____________.

**W5.** Why do we run several seeds instead of one?

________________________________________________________________

---

## 📖 Page 5.1 — Match the Word to the Thing

Write the letter of the meaning beside each word.

| Word | Letter | | Meaning |
|---|:--:|---|---|
| overfitting | ____ | **A** | An independent copy of the weights at the best epoch. |
| validation loss | ____ | **B** | Multiply every weight by `1 − lr × wd` every step. |
| best epoch | ____ | **C** | Training loss low, validation loss high and (usually) rising. |
| patience | ____ | **D** | Zero a share `p` of the numbers during training; scale the rest by `1 / (1 − p)`. |
| snapshot | ____ | **E** | The loss on points the network never trains on. |
| dropout | ____ | **F** | A change after which the class is still true. |
| weight decay | ____ | **G** | Fresh random noise added to the training inputs every epoch. |
| jitter | ____ | **H** | The epoch where validation loss was lowest (known only afterwards). |
| label-preserving | ____ | **I** | How many epochs with no improvement to wait before stopping. |

**Two in your own words.** *Memorising* is: ______________________________________________

*Learning* is: ______________________________________________________________________

**One that is easy to mix up.** Why is "training loss is low" not enough to say a model is good?

________________________________________________________________

---

## 🔮 Page 5.2 — Predict the Output

Write your prediction **in pen, before** you run anything. Then run it and write what happened beside it.

**P1.** A layer that zeroes half the numbers, shown ten ones.

```python
import torch
import torch.nn as nn
torch.manual_seed(0)
drop = nn.Dropout(0.5)
x = torch.ones(10)
drop.eval()
print(drop(x))
```

My prediction: ______________________ Real: ______________________

**P2.** Same layer, same `x`, but `drop.train()` instead of `drop.eval()`. Which values can appear in the output? ______ and ______. About how many of each? ______________________

**P3.** `nn.Dropout(0.2)` in train mode on a thousand ones. What value does a **survivor** have? (Do the sum `1 / (1 − p)` first.) ______________

`nn.Dropout(0.75)`: survivor value ______________  `nn.Dropout(0.0)`: survivor value ______________

**P4.**

```python
import numpy as np
rng = np.random.default_rng(0)
a = rng.normal(0, 0.1, size=(2, 3))
print(a.shape)
print(a.dtype)
```

Shape: ______________ dtype: ______________ (Hint: it is the one the model will complain about.)

**P5.**

```python
import copy
import torch
import torch.nn as nn
lin = nn.Linear(1, 1, bias=False)
alias = lin.state_dict()
snap = copy.deepcopy(lin.state_dict())
# ... now one training step is taken on lin ...
```

After the step, which of `alias["weight"]` and `snap["weight"]` has moved? ______________ Why? ______________________________________________

**P6.**

```python
import torch
g = torch.Generator().manual_seed(0)
order = torch.randperm(6, generator=g)
print(len(order))
print(sorted(order.tolist()))
```

Length: ______ The sorted list: ______________________________ (The *order* in `order` is mixed up. What is true about the *set* of numbers?) ______________________

**Check P1 to P6 by running them.** Write down any prediction you got wrong, and why: ______________________________________________

---

## 🔢 Page 5.3 — Stopping and the Fee, by Hand

**Pencil, paper and calculator. No code.**

### (a) When does the loop stop?

The rule: after each epoch, if this validation loss is the lowest so far, remember this epoch as the **best epoch**. Then compute `counter = epoch − best epoch`. **Stop as soon as `counter >= patience`.** Epochs are counted from 0.

Ten made-up validation losses:

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| val | 0.70 | 0.40 | 0.30 | 0.25 | 0.26 | 0.24 | 0.27 | 0.28 | 0.29 | 0.30 |
| best so far | | | | | | | | | | |
| best epoch so far | | | | | | | | | | |
| counter | | | | | | | | | | |

**Patience 3.** Stops at epoch ______ and keeps epoch ______ (loss ______).

**Patience 5.** Stops at epoch ______ (or write *never*).

**Patience 1.** Stops at epoch ______ and keeps epoch ______ (loss ______). Which better epoch did it miss? ______

### (b) A second list

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| val | 0.90 | 0.50 | 0.45 | 0.47 | 0.44 | 0.46 | 0.48 | 0.50 | 0.52 |

Best epoch: ______ (loss ______). Patience 2 stops at epoch ______. Patience 4 stops at epoch ______.

### (c) A trap list

| epoch | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| val | 0.80 | 0.55 | 0.41 | 0.36 | 0.37 | 0.33 | 0.34 | 0.35 | 0.36 | 0.31 |

Patience 1 stops at epoch ______ keeping epoch ______. Patience 2 stops at epoch ______ keeping epoch ______. Patience 3 stops at epoch ______ keeping epoch ______.

Patience 4: does it stop? ______ (Look at epoch 9 before you answer.) The lowest loss on the whole list is at epoch ______ . Which of patience 1, 2, 3 stop **before** reaching it? ______

### (d) The fee

`weight decay` multiplies each weight by `1 − lr × wd` on every step (when the gradient is zero, only the fee acts).

| lr | wd | fee `1 − lr × wd` | weight 1.0 after one step | after two steps |
|:--:|:--:|:--:|:--:|:--:|
| 0.003 | 0.3 | | | |
| 0.01 | 0.1 | | | |
| 0.01 | 0.5 | | | |
| 0.003 | 0.0 | | | |

Two steps means *multiply the result of step one by the fee again*. **Do not raise to a power.** Four decimals.

**F1.** A weight of **4.0**, `lr = 0.01`, `wd = 0.5`. After one step: ______ After two steps: ______

**F2.** A weight of **0.0** and a fee of 0.995. After one step: ______ What does that tell you about which weights the fee bites? __________________________

**F3.** If `wd = 0.0`, what is the fee? ______ So what does "weight decay 0" do? ________________

### (e) Dropout

| p | Share zeroed | Survivor value `1 / (1 − p)` | Average of the output |
|:--:|:--:|:--:|:--:|
| 0.5 | | | |
| 0.25 | | | |
| 0.2 | | | |
| 0.0 | | | |

**E1.** Why scale the survivors up at all? What would the **average** of the output be if you zeroed half and did not scale? ______________________________________________

**E2.** At `p = 0.0`, does anything happen? ______ (This is why the `Dropout(p=0.0)` you saw in Week 1 was harmless.)

---

## 🔢 Page 5.4 — Steps and Points (the Lab's Arithmetic)

The lab uses **120 training points**, batch **40**, and **250** epochs. The harness drops the short last batch.

| Batch | Steps per epoch (`120 // batch`) | Points used per epoch | Points left out | Steps in 250 epochs |
|:--:|:--:|:--:|:--:|:--:|
| 40 | | | | |
| 50 | | | | |
| 64 | | | | |
| 120 | | | | |

**A1.** How many parameters does the network have, and how many per training point? (16,962 parameters.) 16,962 ÷ 120 = ______ . Does a network with that many numbers to set find it **easy** or **hard** to memorise 120 points? ______________

**A2.** Pick the right word. If I see **training loss 0.000 and validation loss 0.75**, the model has (learned / memorised). If training loss is 0.19 and validation loss is 0.23, the gap is ______ and I would call that (learning / memorising).

**A3.** In the lab the validation set is 360 points. Which tensor does `fit` measure the validation loss on, and which one does it train on? ______________________

---

## 🎲 Page 5.5 — The Four-Cure Table and the Report

### (a) Your class table (seed 0)

Build `lab.py` and `patience.py` as in the lesson. Run the five rows with **seed 0** and write what your own screen prints. (The shape matters more than the third decimal.)

| Row | best epoch | best val | final val | **shipped val** (what you would deliver) |
|---|:--:|:--:|:--:|:--:|
| no cure | | | | |
| early stop (p=25) | | | | |
| dropout 0.3 | | | | |
| weight decay 0.3 | | | | |
| jitter 0.1 | | | | |

**Say the sentence.** Which column would you be allowed to brag about? ______________ Why? ____________________________________________

Why is the early-stop row's **final val** *not* what you would ship? ______________________________

### (b) Five seeds (0 to 4)

Fill with the **mean** over seeds 0 to 4, and the lowest and highest in brackets.

| Row | best val (mean, lowest .. highest) | final val (mean, lowest .. highest) |
|---|---|---|
| no cure | | |
| early stop (p=25) | | |
| dropout 0.3 | | |
| weight decay 0.3 | | |
| jitter 0.1 | | |

**Do the ranges of "best val" overlap?** ______ Draw the five ranges as bars on this number line (0.10 to 0.30):

```text
0.10        0.15        0.20        0.25        0.30
|-----------|-----------|-----------|-----------|
```

### (c) A different dose (so you cannot copy the class table)

Save this as `wb_table.py` next to `lab.py`:

```python
# wb_table.py
from lab import *

rows = [
    ("no cure",            lambda s: fit(seed=s)),
    ("early stop (p=10)",  lambda s: fit(seed=s, patience=10)),
    ("dropout 0.5",        lambda s: fit(seed=s, dropout=0.5)),
    ("weight decay 1.0",   lambda s: fit(seed=s, wd=1.0)),
    ("jitter 0.2",         lambda s: fit(seed=s, jitter=0.2)),
]
SEEDS = [10, 11, 12]
print("seeds", SEEDS, "- each cell is the mean of 3 runs")
print(f"{'row':<18} {'best epoch':>10} {'best val':>9} {'final val':>10}")
for name, go in rows:
    hs = [go(s) for s in SEEDS]
    print(f"{name:<18} {np.mean([h['best_ep'] for h in hs]):>10.0f} "
          f"{np.mean([h['best_val'] for h in hs]):>9.3f} {np.mean([h['val'][-1] for h in hs]):>10.3f}")
```

**Before you run it, predict** (circle one for each): the early-stop row, compared with the no-cure row, will have a best val that is **lower / the same / higher**.  Jitter 0.2 will have the **lowest / not the lowest** final val.

Your run (about 5 seconds):

| Row | best epoch | best val | final val |
|---|:--:|:--:|:--:|
| no cure | | | |
| early stop (p=10) | | | |
| dropout 0.5 | | | |
| weight decay 1.0 | | | |
| jitter 0.2 | | | |

**C1.** Compare the early-stop row's **best epoch** with the no-cure row's. Which is earlier? ______ What does a *small patience* risk? (Remember Page 5.3 (c).) ______________________________________________

**C2.** Which row has the lowest final val? ______ Is the gap to the next row bigger than the spread between seeds? (You only see means here; what extra thing would you need to look at to answer?) ______________________________________________

**C3.** The early-stop row's "final val" is the loss **when the run stopped**. Its **shipped val** is its ______ val.

### (d) The lab report

Fill the template with **your own** numbers.

```
On ____ points, with ____ seeds, I ran ____ cures, one at a time, plus a control.
The mean best validation loss was between ____ and ____ for all of them,
and the ranges (overlap / do not overlap).
The mean final validation loss ranged from ____ to ____.
What I would ship is ____________________, because _______________________________
_____________________________________________________________________________.
One thing I did not test: ______________________________________________________
```

**Check yourself (four yes answers = secure).** Did I say the number of points and of seeds? ____ Did I say which column I used? ____ Did I avoid the words "best cure"? ____ Did I name one untested thing? ____

**Someone says:** *"Jitter is the best cure."* Using your tables, what one question do you ask first? ____________________________________________

![Two panels of range bars, one row per cure, with a diamond at the mean of five seeds: the best-validation bars overlap heavily, the final-validation bars sit lower for every cure than for no cure](../figures/fig-w05-2-four-cures-five-seeds.svg)
*Figure W5.2 — Over five seeds the best-val bars overlap; the final-val means are what separate the cures.*

---

## 📈 Page 5.6 — Read a Curve

This is a real run (**seed 10, no cure**), from the same `lab.py`, printed at chosen epochs.

```text
 epoch   train    val
     0   0.688   0.683
    10   0.428   0.516
    22   0.182   0.227
    40   0.113   0.243
    60   0.102   0.319
    80   0.053   0.353
   120   0.001   0.597
   180   0.000   0.695
   249   0.000   0.750

best val 0.227 at epoch 22; final val 0.750; final train 0.000
gap at best: 0.046  gap at end: 0.75
```

**R1.** Circle (with a highlighter) the **best epoch** row. What is the validation loss there? ______

**R2.** What is the training loss doing from epoch 120 on? ______ And the validation loss? ______

**R3.** Epoch 0 shows about 0.69 on both. Where does that number come from? ______ What does it tell you about the network at epoch 0? ______________

**R4.** Would you be happy to ship the epoch-249 model? ______ Compare 0.750 with the coin-flip loss. ______________________________

**R5.** Using this curve, the loop is run with `patience = 10`. It stops at epoch ______ and keeps epoch ______. (Real run: `patience 10 -> (22, 32)`; do the arithmetic first: `22 + 10 =` ______ .) With `patience = 50` it stops at epoch ______.

**R6.** Why can't you know on epoch 22 that epoch 22 is the best? ______________________________________________

**R7.** Complete: *"The best epoch is only known __________, so the thing to keep is the __________."*

![Line chart of loss against epoch: a solid training line falling to zero, a dashed validation line that bottoms out at epoch 59 then climbs to 0.906, and a bracket marking the final gap](../figures/fig-w05-1-memorising-train-val-gap.svg)
*Figure W5.1 — Training loss reaching 0.000 does not mean the model is good: validation loss turned upward after epoch 59.*

---

## 🐞 Page 5.7 — Fix the Broken Programs

Each of D1 to D4 is **deliberately broken**. Read the **last line** of the message first. S1 to S6 run without an error: they are the dangerous ones.

**D1 — DELIBERATE ERROR**

```python
import torch.nn as nn
drop = nn.Dropout(30)
```

Last line: `ValueError: dropout probability has to be between 0 and 1, but got 30`

What range does it want? ______ The author meant "30 percent". Fix: ______________________________

**D2 — DELIBERATE ERROR**

```python
import numpy as np
import torch
from lab import Xs, make_model

rng = np.random.default_rng(0)
noisy = Xs + torch.tensor(rng.normal(0, 0.1, size=Xs.shape))
print(noisy.dtype)
model = make_model()
out = model(noisy)
```

Last line: `RuntimeError: mat1 and mat2 must have the same dtype, but got Double and Float`

Which is the noise, and which is the weights? ______________________ What did the **first print** already tell you? ______________ Fix: ______________________________________________

**D3 — DELIBERATE ERROR**

```python
import torch
g = torch.Generator().manual_seed(0)
order = torch.randperm(120, g)
```

Last line begins: `TypeError: randperm() received an invalid combination of arguments - got (int, torch._C.Generator)`

What is the generator supposed to be written as? ______ Fix: ______________________________

**D4 — DELIBERATE ERROR**

```python
import numpy as np
from lab import Xs
rng = np.random.default_rng(0)
noise = rng.normal(0, 0.1, size=Xs)
```

Last line begins: `TypeError: expected a sequence of integers or a single integer, got 'tensor(...`

`size=` wants a ______ , and the author gave it ______ . Fix: ______________________________

### The six that do not crash

For each, the first number is from the **correct** program, the second from the **buggy** one. Both are real runs (seed 0, 250 epochs, `lab.py` settings). Name the mistake and write the fix.

| # | What the student saw | The mistake | The fix |
|:-:|---|---|---|
| S1 | `best_state` was saved with `model.state_dict()` and no copy. After `load_state_dict(saved)` the validation loss is **0.906** (correct code: **0.179**). | | |
| S2 | Dropout 0.3, and `model.eval()` was never called before validating. Final val is **0.426** (correct: **0.634**). "Better!" | | |
| S3 | Jitter 0.2, but the noise was drawn **once** above the epoch loop. Best val **0.285**, final **0.782** (correct: **0.140** and **0.194**). | | |
| S4 | The same `+ noise` line was applied to the **validation** points. Best **0.229** (correct: **0.140**). | | |
| S5 | `AdamW(model.parameters(), lr=3e-3)` with no `weight_decay=`. The "no cure" control finishes at **0.626** instead of **0.906**. | | |
| S6 | `np.random.default_rng()` with no argument. Run twice, the numbers differ. | | |

**S2 trap.** The buggy number is **lower**. Why is a lower number not a good thing here? ______________________________________________

**S5.** Why is this a problem for an *experiment* (not just for the code)? ______________________________

---

## 📓 Page 5.8 — The Bug Log

Copy the **last line** of every error or surprise you meet this week, not the whole traceback.

| # | Last line (copied) | What it meant | The fix | Caught by (message / print / nobody) |
|:-:|---|---|---|:-:|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Your sentence for this week:** *"A number that got better after I changed something is a ______ until I know what I measured."* Complete it from memory: ______________________________

**Which bug was silent (no error, wrong answer)?** How would you have found it? ______________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. Dropout in `train()` mode: survivors are multiplied by ______ . In `eval()` mode it returns ______ .
2. What goes wrong if `model.eval()` is forgotten before measuring validation loss? ______________________________
3. Why does the snapshot need `copy.deepcopy`? ______________________________
4. Weight decay multiplies each weight by ______ every step.
5. Jitter must be drawn (once / every epoch). It is added to the (training / validation) inputs only.
6. Which column of the four-cure table tells the truth about what you would ship? ______________
7. Which is the *cheapest* cure, and why does it need no change to the network? ______________________________

**How sure am I?** (circle one per line)

| I can say what overfitting looks like in two numbers | 1 2 3 4 5 |
|---|---|
| I can find where early stopping stops, by hand | 1 2 3 4 5 |
| I can say why `eval()` and `deepcopy` matter | 1 2 3 4 5 |
| I can say which column to trust | 1 2 3 4 5 |

---

# ✂️ ANSWERS — keep this page folded until you have finished

### Warm-Up

- **W1.** No. The scheduler's clock only moves when `sched.step()` is called (Week 4).
- **W2.** `840 // 150` = **5**; left out **90**.
- **W3.** About **0.693**, which is `ln 2`.
- **W4.** A **confound**.
- **W5.** One seed is one lucky or unlucky start. Several seeds show the spread, so you can tell a real gap from noise.

### Page 5.1

overfitting **C**, validation loss **E**, best epoch **H**, patience **I**, snapshot **A**, dropout **D**, weight decay **B**, jitter **G**, label-preserving **F**.

Own words: *memorising* = getting the training points right (loss near 0.000) by fitting their particulars, so unseen points go badly; *learning* = fitting what is true of new points too. "Training loss is low" is not enough because a network that has simply memorised the training points also has a low training loss; only the **validation** loss, from points it never trained on, shows which one happened.

### Page 5.2

Real output of the code (CPU, seeded):

- **P1.** `tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])`: ten ones (eval mode drops nothing and scales nothing).
- **P2.** Each entry is **0** or **2**; about five of each; the average is about 1. (The exact pattern is seeded; yours matches only if you set the same seed.)
- **P3.** `1 / 0.8 =` **1.25**; `1 / 0.25 =` **4.0**; `p = 0.0` gives `1 / 1 =` **1.0** (nothing happens). A real run of `nn.Dropout(0.2)` on a thousand ones gave a survivor value of 1.25, and `nn.Dropout(0.75)` on two thousand ones gave 4.0.
- **P4.** `(2, 3)` and `float64`.
- **P5.** `alias["weight"]` has moved (it is the live weight); `snap["weight"]` has not (it is a deep copy). (Checked by a real run: `alias` equalled the live weight and `snap` still held its starting value.)
- **P6.** `6` and `[0, 1, 2, 3, 4, 5]`: a shuffle contains every number once. The seeded generator makes the same shuffle each time you re-create it with the same seed.

### Page 5.3

**(a)** Best so far by epoch: 0.70, 0.40, 0.30, 0.25, 0.25, 0.24, 0.24, 0.24, 0.24 (nine entries, because the loop stops at epoch 8 for patience 3). Best epoch so far: 0, 1, 2, 3, 3, 5, 5, 5, 5. Counter (`epoch − best epoch`): 0, 0, 0, 0, 1, 0, 1, 2, **3**.

- **Patience 3:** stops at epoch **8**, keeps epoch **5** (0.24).
- **Patience 5:** **never** (the list ends first; the counter reaches only 4 at epoch 9).
- **Patience 1:** stops at epoch **4**, keeps epoch **3** (0.25). It missed epoch **5** (0.24), one epoch away.

(Real run of the stopping rule on this list: patience 3 gives `(5, 8)`, patience 5 gives `(5, None)`, patience 1 gives `(3, 4)`.)

**(b)** Best is epoch **4** (0.44). Patience 2 stops at epoch **6**; patience 4 stops at epoch **8**. (Real run: `(4, 6)` and `(4, 8)`.)

**(c)** Patience 1: epoch **4**, keeping epoch **3**. Patience 2: epoch **7**, keeping epoch **5**. Patience 3: epoch **8**, keeping epoch **5**. **Patience 4: no.** Epoch 9 (0.31) is a new best, so the counter resets to 0 before it reaches 4. The lowest loss on the list is at epoch **9**; patience **1, 2 and 3** all stop before it (at epochs 4, 7 and 8). (Real run: `(3, 4)`, `(5, 7)`, `(5, 8)`, then `(9, None)` for patience 4 and 5.)

*Marking:* the point is that a short patience can stop in a shallow dip before the real bottom.

**(d)** The fee and the weight 1.0.

| lr | wd | fee | after one | after two |
|:--:|:--:|:--:|:--:|:--:|
| 0.003 | 0.3 | 0.9991 | 0.9991 | 0.9982 |
| 0.01 | 0.1 | 0.9990 | 0.9990 | 0.9980 |
| 0.01 | 0.5 | 0.9950 | 0.9950 | 0.9900 |
| 0.003 | 0.0 | 1.0000 | 1.0000 | 1.0000 |

(`0.9990 × 0.9990 = 0.9980` to four decimals; `0.995 × 0.995 = 0.990025`, which rounds to 0.9900.)

- **F1.** `4.0 × 0.995 =` **3.98**; then `3.98 × 0.995 =` **3.9601**. Real `AdamW` run with zero gradient: `[3.98, 3.9601]`.
- **F2.** `0.0 × 0.995 =` **0.0**. The fee only bites weights that are not already zero.
- **F3.** The fee is `1 − 0 =` **1**; weight decay 0 multiplies by 1, i.e. does nothing.

**(e)** Dropout.

| p | Share zeroed | Survivor value | Average of output |
|:--:|:--:|:--:|:--:|
| 0.5 | 0.5 | 2.0 | about 1 |
| 0.25 | 0.25 | 1.3333 | about 1 |
| 0.2 | 0.2 | 1.25 | about 1 |
| 0.0 | 0.0 | 1.0 | exactly 1 |

- **E1.** Scaling keeps the average the same as without dropout. Zeroing half and not scaling would give an average of about **0.5**, so the next layer would see numbers half as big in training as in testing.
- **E2.** No: `p = 0.0` zeroes nothing and multiplies by `1 / 1 = 1`.

### Page 5.4

| Batch | Steps/epoch | Used | Left out | Steps in 250 epochs |
|:--:|:--:|:--:|:--:|:--:|
| 40 | 3 | 120 | 0 | 750 |
| 50 | 2 | 100 | 20 | 500 |
| 64 | 1 | 64 | 56 | 250 |
| 120 | 1 | 120 | 0 | 250 |

(Real output of `120 // batch`: 3, 2, 1, 1. At batch 64 the lab uses 64 of the 120 points per epoch; a different 64 each epoch because the points are reshuffled.)

- **A1.** 16,962 ÷ 120 = **141.35**, about 141 numbers per training point. **Easy** to memorise: there is far more room than the data needs.
- **A2.** Training 0.000 and validation 0.75: **memorised**. Training 0.19 and validation 0.23: gap **0.04** (0.23 − 0.19); call it **learning**. (The seed-10 curve above had gap 0.046 at its best epoch.)
- **A3.** `fit` trains on `Xs, ys` (120 points) and measures validation loss on `Xva, yva` (360 points).

### Page 5.5

**(a)** Class table, seed 0 (reference run):

| Row | best epoch | best val | final val | shipped val |
|---|:--:|:--:|:--:|:--:|
| no cure | 59 | 0.179 | 0.906 | 0.906 (no snapshot kept) |
| early stop (p=25) | 59 | 0.179 | 0.227 (at the stop, epoch 84) | **0.179** (the snapshot) |
| dropout 0.3 | 70 | 0.201 | 0.634 | 0.634 |
| weight decay 0.3 | 61 | 0.140 | 0.274 | 0.274 |
| jitter 0.1 | 81 | 0.130 | 0.318 | 0.318 |

**Which column tells the truth?** *Shipped val.* Best val is a hindsight number. The early-stop row's final val (0.227) is the loss at the stopping epoch, not the snapshot you would deliver (0.179). (If a cure has early stopping added on top, its shipped val is its best val.)

**(b)** Five-seed means (seeds 0 to 4), range in brackets:

| Row | best val | final val |
|---|---|---|
| no cure | 0.204 (0.159 .. 0.264) | 0.803 (0.435 .. 1.285) |
| early stop (p=25) | 0.212 (0.159 .. 0.264) | 0.351 at the stop · 0.212 shipped |
| dropout 0.3 | 0.190 (0.122 .. 0.257) | 0.575 (0.449 .. 0.732) |
| weight decay 0.3 | 0.185 (0.138 .. 0.246) | 0.389 (0.274 .. 0.537) |
| jitter 0.1 | 0.149 (0.113 .. 0.180) | 0.366 (0.197 .. 0.524) |

**Yes**, every "best val" range overlaps every other. The cures differ in the **final val** column, which is how far the validation loss climbs if you do not stop. Early stopping is cheapest; its shipped value is a bit flattering because it used the validation set to pick the epoch.

**(c)** Reference run, seeds 10, 11, 12, means:

```text
seeds [10, 11, 12] - each cell is the mean of 3 runs
row                best epoch  best val  final val
no cure                    66     0.164      0.576
early stop (p=10)          23     0.216      0.288
dropout 0.5               214     0.245      0.446
weight decay 1.0          151     0.169      0.244
jitter 0.2                145     0.141      0.188
```

(For seed 10 alone, the p=10 run stopped at epoch 32.)

- *Predictions:* any honest guess is full marks if written before the run. The two that surprise people: early stop with patience 10 has a **higher** best val (0.216) than no cure (0.164), and jitter 0.2 **is** the lowest on both best and final val here.
- **C1.** The early-stop row's best epoch (23) is far earlier than the no-cure row's (66). A small patience **stops in a shallow dip before the real bottom**: with `patience = 10` the loop quit before it reached the lower value that no cure found later. A bigger patience (25 in the class table) did not have this problem on seed 0.
- **C2.** Jitter 0.2 has the lowest final val (0.188), then weight decay 1.0 (0.244). To say whether the gap is bigger than the spread between seeds you would need the **per-seed** values (lowest to highest), not only the means; with three seeds you should not claim more than "looks lower here".
- **C3.** Its **best** val (0.216).

**(d)** Target wording (any equivalent is fine):

```
On 120 points, with 5 seeds, I ran 4 cures, one at a time, plus a control.
The mean best validation loss was between 0.149 and 0.212 for all of them,
and every range overlaps. The mean final validation loss ranged from 0.351 (at the stop) to 0.803.
What I would ship is the early-stop snapshot (mean 0.212), because it needs no change to the
network and I know when to stop; weight decay or jitter give lower final values but I would still
want a held-out test set before trusting any of them.
One thing I did not test: a different draw of the 120 points, or a third set never used for picking.
```

**Marking points.** Number of points and seeds stated? Which column used? Avoids "best cure"? Names one untested thing? **Four yes answers = secure.**

**"Jitter is the best cure."** Accept: "Is the gap bigger than the spread between seeds?" or "Which column, and on how many seeds?" **Do not accept** agreement. On seeds 0 to 4 every best-val range overlaps; on seeds 5 to 7 (the homework) jitter 0.1 (best val 0.159) is not the lowest: all five rows are between 0.150 and 0.160.

### Page 5.6

- **R1.** Epoch **22**, validation loss **0.227**.
- **R2.** Training loss: **0.001 then 0.000** (it has hit the floor). Validation loss: **climbing** (0.597, 0.695, 0.750).
- **R3.** `ln 2` (about 0.693), the loss of a two-class coin. At epoch 0 the network has learned nothing, so it is guessing.
- **R4.** No: 0.750 is **worse than the coin** (0.693), and the training loss says 0.000 even though the model is bad on new points.
- **R5.** `22 + 10 = 32`: stops at epoch **32**, keeps epoch **22**. With patience 50 it stops at epoch **72** (`22 + 50`). (Real run: `(22, 32)` and `(22, 72)`; patience 25 gives `(22, 47)` and patience 5 gives `(16, 21)`, which stopped before epoch 22 on a shallower dip.)
- **R6.** Because you only see the validation losses up to now. Epoch 22 is the best only because the epochs after it were worse, and you have not seen them yet.
- **R7.** *"The best epoch is only known **afterwards**, so the thing to keep is the **snapshot**."*

### Page 5.7

- **D1.** Between 0 and 1: a share, not a percentage. Fix: `nn.Dropout(0.3)`.
- **D2.** The noise is **float64** ("Double"); the weights are **float32** ("Float"). The first `print(noisy.dtype)` had already said `torch.float64`. Fix: `torch.tensor(noise, dtype=torch.float32)`. (The addition `Xs + tensor` works silently and gives float64; the error only appears later, in the model.)
- **D3.** As a keyword: `generator=g`. Fix: `torch.randperm(120, generator=g)`.
- **D4.** A **shape**; the author gave it the **data**. Fix: `size=Xs.shape`.

| # | Mistake | Fix |
|:-:|---|---|
| S1 | No `copy.deepcopy`: `state_dict()` returned live tensors, so the "saved best" tracked the live model to the end. | `copy.deepcopy(model.state_dict())` |
| S2 | Dropout still on when measuring. | `model.eval()`, then `torch.no_grad()` |
| S3 | Noise drawn once, so the network memorises one fixed noisy copy. | Draw the noise **inside** the epoch loop |
| S4 | The measuring stick was bent: jitter was applied to the validation set. | Only the **training** inputs get jitter |
| S5 | `AdamW` defaults to `weight_decay=0.01`, so "no cure" was a small cure. | `weight_decay=0.0` when you mean none |
| S6 | Unseeded generator. | `np.random.default_rng(seed)` |

- **S2 trap.** The lower number measures a different thing: a model with units randomly off, which is not the model you would ship. A lower number from a changed measurement is not an improvement. (Real `twice.py`: the same model and data gave 0.3621 and then 0.3263 in train mode, and 0.2807 twice in eval mode.)
- **S5.** It changes the control. If the control quietly gets a small cure, every comparison against it is shrunk. (Real run: same best val 0.179 at epoch 59, final **0.626** instead of **0.906**.)

### Page 5.8 and Self-Check

Bug Log: any real entries are fine if the **last line** (not the whole traceback) was copied and the fix works. Sentence: *"…is a **suspect** until I know what I measured."* ("Warning" or "question" is also fine.) The silent bugs (S1 to S6) show nothing on their own; a printout of the dtype, the validation loss twice in a row, and the loaded-back validation loss catches S1, S2, S3.

1. Multiplied by `1 / (1 − p)` (2.0 at p = 0.5); in `eval()` it returns its input unchanged (all ones for a vector of ones).
2. Dropout stays on, so validation is measured on a different, randomly damaged model and the loss changes every time you ask.
3. `state_dict()` returns live tensors; without a copy the "snapshot" keeps changing with the model.
4. `1 − lr × wd`.
5. **Every epoch**; **training** inputs only.
6. **Shipped val**.
7. **Early stopping**: it only watches the validation curve and keeps a snapshot, so the network itself is unchanged.

---

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [📖 Chapter](../student-guide/week-05.md) · [Next ➡ Week 6](week-06.md)
