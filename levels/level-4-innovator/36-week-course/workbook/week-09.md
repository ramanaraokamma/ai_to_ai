# Workbook — Week 9: Review and Assessment 1 (The X-Ray)

**Name:** ________________________________  **Date:** ______________

[⬅ Week 8](week-08.md) · [📖 Read the chapter first](../student-guide/week-09.md) · [Course Home](../README.md) · [Next ➡](week-10.md)

---

> **Rules for this workbook.** This week has **one real paper** (the 75-mark Term 1 checkpoint your teacher hands you in class) and **this workbook is everything around it**: the night-before map, practice on **numbers that are not on the paper**, the marking pages, and the Bug Log. **Nothing in here is the paper, and nothing in here is a teacher file.**
>
> **Pen first, then run.** Pages 9.2 to 9.6 are by hand with a calculator. You write your answer *before* you open the check file. The digits in the worked examples and the answers came from real CPU runs (PyTorch, `torch.manual_seed(0)` where anything is random, one seed per run). By-hand numbers are plain arithmetic and will match exactly. The loss tables on page 9.7 are real printed output from `l4lib.spirals.run`; on another CPU or PyTorch build the **last digit** of a loss can move, but not the shape of the story.
>
> **Nothing new today.** No new idea, no new syntax. If a page uses something you do not recognise, that is a **finding**, not a failure: write the week you think it came from in the margin.
>
> **There is no language model and no stand-in anywhere in this workbook.** Everything is plain PyTorch on the CPU, or arithmetic.
>
> Run any check file from the folder that contains `l4lib/`. Carry **four decimals** in every calculation.

---

## ✅ Warm-Up (5 min, before anything else)

Five questions, one per *kind* of thing the paper will ask. No notes.

**W1.** A two-class model guesses 50-50 on every example. Its log loss is about ____________ (a number to three decimals).

**W2.** Plain SGD with `lr = 0.1` at gradient 4 moves a weight by ____________. (Hold that: page 9.2 builds on it.)

**W3.** Last week a cell gave a different final note when the **same inputs** came in a different order. A bag of words gives the **same / different** (circle one) answer for the same two orders.

**W4.** A gap between two runs is "inside noise" when it is **smaller / bigger** (circle one) than ____________ times the spread.

**W5.** Which of the four weeks' habits do you trust least right now? (Circle: **Reading a curve · Hand-stepping an optimizer · Unrolling the cell · Is-it-noise**) ____________ Write why, in a few words: _____________________________________________

---

## 🗺️ Page 9.1 — The Confidence Map (the night before; 10 minutes, do not study)

For each line ask: **could I do this right now with only a pen and a calculator?** Tick **Yes**, **Maybe** or **No**. Be honest; nobody sees this page but you. Then, for each **No**, do the workbook page in the last column for **20 minutes at most**, and then stop. Do not try to learn everything in one night.

| Week | I can... | Yes | Maybe | No | Page to redo |
|:--:|---|:--:|:--:|:--:|---|
| 1 | Say what loss a guessing two-class model has. Tell two runs apart by their **whole curves**, not their last number. Call a keyword-only function. | ☐ | ☐ | ☐ | 1.1, 1.3 |
| 2 | Step by hand with plain SGD **and** with PyTorch momentum (`v = 0.9·v + g`). | ☐ | ☐ | ☐ | 2.1, 2.8 · today's **9.2** |
| 3 | Compute a root-mean-square. Say what Adam's **first** step looks like. | ☐ | ☐ | ☐ | Week 3 by-hand page · today's **9.3** |
| 4 | Say what a `LambdaLR` multiplier does. Count optimizer steps. | ☐ | ☐ | ☐ | 4.3, 4.4 |
| 5 | Name the free cure for overfitting. Say what dropout does in eval mode. Say why a snapshot needs `copy.deepcopy`. | ☐ | ☐ | ☐ | Week 5 cure table · today's **9.8** |
| 6 | Say why batch norm leans on the other examples. Find the slope of `x + f(x)` by nudging. Say what `clip_grad_norm_` returns. | ☐ | ☐ | ☐ | Week 6 by-hand page · today's **9.8** |
| 7 | Say whether a gap is bigger than twice the spread. Write a SYMPTOM → CHECK → ACTION row. | ☐ | ☐ | ☐ | 7.3, 7.4 · today's **9.6**, **9.7** |
| 8 | Say why a bag cannot see order. Give the shapes of `x`, `out`, `h_n`. Unroll the cell. | ☐ | ☐ | ☐ | 8.3, 8.4 · today's **9.4**, **9.5** |

**Count your Noes:** ______ . **Rule:** if you have more than three, still do only the **two** you ticked No for that you think are worst, and **stop at 20 minutes each**. A tired head does arithmetic worse than a rested one.

*After the paper*, come back to this page and write, beside each week, whether your **guess** about yourself was right. That comparison is worth more than the mark.

My guess about myself, before: Weeks I thought were soft: ____________ . After the paper, the weeks that were actually soft: ____________ .

---

## 🏃 Page 9.2 — Hand Steps, New Numbers (Week 2 · 15 min)

**Same method as Week 2, different numbers from the paper.** `f(w) = w²`, gradient `g = 2w`. Start at **`w = 1.5`**, **`lr = 0.1`**, three steps.

**Worked example (done for you): the first SGD step.** `g = 2 × 1.5 = 3.0000`. The step is `0.1 × 3.0000 = 0.3000`. New `w = 1.5000 − 0.3000 =` **`1.2000`**.

**Plain SGD** (`w ← w − 0.1·g`). Fill in the rest.

| Step | w before | g = 2w | step = 0.1·g | w after |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.5000 | 3.0000 | 0.3000 | 1.2000 |
| 2 | 1.2000 | | | |
| 3 | | | | |

**Momentum, PyTorch's form** (`v ← 0.9·v + g`, then `w ← w − 0.1·v`; **`v` starts at 0**; there is **no `0.1`** on the `g`).

| Step | w before | g = 2w | v = 0.9·v + g | step = 0.1·v | w after |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.5000 | | | | |
| 2 | | | | | |
| 3 | | | | | |

**9.2a.** After step 1, do the two tables agree? ____________ Why? (one short sentence) ___________________________________________

**9.2b.** After step 3, which rule is **closer to the minimum at 0**? ____________ By how much (the difference of the two `w`'s)? ____________

**9.2c.** In the momentum table the step size **grows** from step 1 to step 3 even though the gradient **shrinks**. Where does the growth come from? ___________________________________________

**9.2d. Predict, then check.** The minimum is at `w = 0`. If you took **two more** momentum steps, do you think the weight would stop at 0, or go past it? My guess: ____________ (Write it, *then* turn to the answers or run the check file below.)

**Check file** (run it only after your tables are written):

```python
# check92.py - Week 9 workbook page 9.2: check the hand steps on PRACTICE numbers.
import torch

p = torch.nn.Parameter(torch.tensor([1.5]))
opt = torch.optim.SGD([p], lr=0.1, momentum=0.9)
for step in range(1, 6):
    opt.zero_grad()
    (p * p).sum().backward()
    opt.step()
    print(step, round(p.item(), 4))
```

Write what it printed for steps 1 to 5: ____________ ____________ ____________ ____________ ____________

Did your hand `w after` at steps 1, 2, 3 match? ____________ If not, which column first disagreed? ____________

---

## 📏 Page 9.3 — Typical Size, and Adam's First Step (Week 3 · 10 min)

**Worked example (done for you): root-mean-square of `[3, -4]`.** Square: `9, 16`. Average: `12.5`. Root: `3.5355`. (Not the plain mean `-0.5`. Not the length `5`. Not `12.5`, which is the step *before* the root.)

**9.3a.** Root-mean-square of `[5, -12]`. Fill each step.

| Squares | Average of the squares | Root |
|:--:|:--:|:--:|
| ______ , ______ | ______ | ______ |

**9.3b.** For the same list, write the three **wrong** answers a hurried person gives, and say which slip each one is.

| Wrong answer | The slip |
|:--:|---|
| ______ | forgot to ____________ |
| ______ | took the plain ____________ , so the signs cancelled |
| ______ | took the ____________ of the vector, not the typical size |

**9.3c.** Now `[500, -1200]` (every number 100 times bigger). The root-mean-square is ____________ . It is ______ times bigger than 9.3a's answer. So root-mean-square **scales / does not scale** with the numbers (circle one).

**Adam's first step.** After **one** gradient, the "typical size of the gradient" is just `|g|`. So the step is `lr × g / |g|` = `lr`, with the sign of `g`, to within a tiny epsilon. A **positive** gradient moves the weight **down**; a **negative** one moves it **up**.

**9.3d.** `lr = 0.02`, a weight at `1.00`, a first gradient of **`-3`**. After one Adam step the weight is ____________ .

**9.3e.** Same, but the first gradient is **`-3000`**. After one step the weight is ____________ . In one sentence, why is it the same as 9.3d? _______________________________________________

**9.3f.** What does AdamW change, in your own words? (One sentence.) _______________________________________________

---

## 🧶 Page 9.4 — Unroll the Cell, New Weights (Week 8 · 15 min)

The cell is `new note = tanh( W_x × x + W_h × old note )`, and the start note is `0`. **Different weights from the paper and from Week 8:** `W_x = 1.0`, `W_h = -0.5` (note the **minus**). Both biases are zero. A calculator with a `tanh` key.

**Worked example (done for you): step 1 for `x = [1, 0, 1]`.** `1.0 × 1 + (−0.5) × 0 = 1.0000`. `tanh(1.0000) =` **`0.7616`**.

**Inputs `x = [1, 0, 1]`.**

| Step | x | W_x·x + W_h·(old note) | new note = tanh of that |
|:--:|:--:|---|:--:|
| 1 | 1 | 1.0×1 + (−0.5)×0 = 1.0000 | 0.7616 |
| 2 | 0 | 1.0×0 + (−0.5)×0.7616 = ______ | ______ |
| 3 | 1 | 1.0×1 + (−0.5)×(______) = ______ | ______ |

**Inputs `x = [1, 1, 0]`** (same inputs, different order).

| Step | x | W_x·x + W_h·(old note) | new note = tanh of that |
|:--:|:--:|---|:--:|
| 1 | 1 | 1.0000 | 0.7616 |
| 2 | 1 | ______ | ______ |
| 3 | 0 | ______ | ______ |

**9.4a.** The two inputs add up to the same total, ______ . The two **last notes** are ______ and ______ . Same or different? ____________

**9.4b.** What would a bag of words say about these two sequences? ____________ . So a bag **can / cannot** (circle) tell them apart, and the cell **can / cannot** (circle).

**9.4c. Look at the signs.** Last week's weights were both positive and every note stayed above 0. Here `W_h` is negative. What happened to the note at step 2 of the first table, and why? ___________________________________________

**9.4d.** Which of these two things is the cell **remembering** at step 3: (i) the whole sentence so far, exactly; (ii) a single squashed summary of it? Circle one. In one sentence, what is lost? ___________________________________________

**Check file:**

```python
# check94.py - Week 9 workbook page 9.4: unroll the cell with nn.RNN, W_x = 1.0, W_h = -0.5.
import torch
import torch.nn as nn

rnn = nn.RNN(1, 1, batch_first=True)
rnn.weight_ih_l0.data = torch.tensor([[1.0]])
rnn.weight_hh_l0.data = torch.tensor([[-0.5]])
rnn.bias_ih_l0.data = torch.zeros(1)
rnn.bias_hh_l0.data = torch.zeros(1)

for xs in ([1, 0, 1], [1, 1, 0]):
    out, h_n = rnn(torch.tensor(xs, dtype=torch.float32).reshape(1, 3, 1))
    print(xs, [round(v, 4) for v in out.flatten().tolist()])
```

Write what it printed: `[1, 0, 1]` → ____________________ `[1, 1, 0]` → ____________________

---

## 📐 Page 9.5 — Say the Shapes (Week 8 · 5 min, predict first)

A batch of **3** sentences, each **6** words long, each word an id from a vocabulary of **6**. `emb = nn.Embedding(6, 2)` and `rnn = nn.RNN(2, 7, batch_first=True)`.

**Write the shapes before you run anything.** (A shape is a tuple like `(3, 6)`.)

| Name | What it is | My predicted shape | Printed shape |
|---|---|:--:|:--:|
| `ids` | the sentences as ids | | |
| `emb(ids)` | each id looked up as 2 numbers | | |
| `out` | the note after **every** word | | |
| `h_n` | the **last** note only | | |

**9.5a.** How many numbers live in the embedding table? ____________ (rows × columns). How many in the RNN? ____________ *(Hint: `2×7` for `W_x`, `7×7` for `W_h`, and **two** biases of 7.)*

**9.5b.** Why does `h_n` start with a `1`? ___________________________________________

**9.5c.** Which of `out` and `h_n` would you use to make a prediction **after every word**? ____________ After the **last word** only? ____________

**Check file:**

```python
# check95.py - Week 9 workbook page 9.5: shapes and counts.
import torch
import torch.nn as nn

torch.manual_seed(0)
emb = nn.Embedding(6, 2)
rnn = nn.RNN(2, 7, batch_first=True)
ids = torch.tensor([[0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], [1, 1, 1, 1, 1, 1]])
e = emb(ids)
out, h_n = rnn(e)
print(tuple(ids.shape), tuple(e.shape), tuple(out.shape), tuple(h_n.shape))
print(sum(p.numel() for p in emb.parameters()), sum(p.numel() for p in rnn.parameters()))
```

---

## 🔍 Page 9.6 — Is the Gap Bigger Than the Spread? (Week 7 · 10 min)

**The rule (Week 7):** `gap = |mean A − mean B|`. `spread =` the **larger** of the two standard deviations (divide by `n`). **Inside noise** if `gap < 2 × spread`. It is a **screening rule we chose**, not a statistical test.

**Worked example (done for you).** A: `0.039 ± 0.008`, B: `0.034 ± 0.007`. Gap `0.005`. Twice the larger spread `0.016`. `0.005 < 0.016` → **inside noise**.

Validation loss at epoch 60, three seeds each (0, 1, 2):

```text
 run   val at epoch 60 (seeds 0, 1, 2)    mean    spread (SD, divide by n)
  A    [0.050, 0.060, 0.040]              0.0500   0.0082
  B    [0.032, 0.040, 0.026]              0.0327   0.0057
  C    [0.046, 0.052, 0.040]              0.0460   0.0049
```

**9.6a. A against B.** Gap ____________ . Larger spread ____________ . Twice the larger spread ____________ . Verdict (inside noise / bigger): ____________

**9.6b. A against C.** Gap ____________ . Larger spread ____________ . Twice the larger spread ____________ . Verdict: ____________

**9.6c.** In 9.6a the verdict is a **close call**. In one sentence, what would you do **before** you wrote "B beats A" in a playbook? ___________________________________________

**9.6d.** A friend runs **one seed each** and says "B (0.033) is lower than A (0.050) so B is better." Write the **two numbers** you would ask for first: ____________ and ____________ .

**9.6e. Hold-equal.** The classmate in the paper's Question E(b) compared two runs whose **step counts** were 780 and 180. Using only the sentence "steps = (examples ÷ batch) × epochs", what are the steps for **840 examples, batch 120, 10 epochs**? ____________

---

## 📉 Page 9.7 — Read Four New Curves (Week 1 and Week 7 · 15 min)

Four runs of the same network on the spirals data. Each is AdamW, 60 epochs, seed 0, and they differ in **one** thing only: the learning rate. **Real numbers** from `l4lib.spirals.run`. **Train** is the average training loss during that epoch; **val** is the loss on the validation set after it. A coin gives **0.693**.

```text
                           ep 1     ep 5    ep 10    ep 20    ep 40    ep 60
W  lr=0.001   train       0.691    0.494    0.085    0.021    0.016    0.018
              val         0.678    0.420    0.073    0.029    0.085    0.026
X  lr=1e-05   train       0.694    0.694    0.693    0.692    0.690    0.683
              val         0.693    0.692    0.692    0.691    0.688    0.679
Y  lr=1       train   7837888.5    0.752    0.704    0.696    0.696    0.714
              val      5632.9      0.705    0.736    0.710    0.697    0.694
Z  lr=0.01    train       0.658    0.077    0.069    0.031    0.020    0.013
              val         0.540    0.060    0.125    0.049    0.136    0.059
```

Final accuracy: **W** 99.4% · **X** 55.3% · **Y** 46.9% · **Z** 99.2%.

**Worked example (done for you): the habit.** *"X: it is barely moving. Val goes 0.693 at epoch 1 to 0.679 at epoch 60, which is almost the coin."* A symptom, a **name for the curve**, and **one number from the table**.

**9.7a.** Do the same for **W, Y, Z**. One sentence each, name the curve, and quote **one number**.

W: ___________________________________________________________

Y: ___________________________________________________________

Z: ___________________________________________________________

**9.7b.** In Y the first *train* number is `7837888.5` and the first *val* number is `5632.9`. Why are they different numbers for the same epoch? (Read what the labels say.) ___________________________________________

**9.7c.** W and Z both end at about 99% accuracy. Fill in the table from **only** the printed epochs.

| | val at epoch 20 | val at epoch 40 | val at epoch 60 | did val go **up** from 20 to 40? |
|:--:|:--:|:--:|:--:|:--:|
| W | | | | |
| Z | | | | |

**9.7d.** For Z, the table shows val at only six epochs out of 60. Why can't you say from this table **which epoch had the lowest val loss**? ___________________________________________ *(The check below prints the lowest from all 60.)*

**9.7e. A playbook row.** Pick the curve **Y**. Write one row.

| SYMPTOM | CHECK (cheap, seconds) | ACTION (change **one** knob) |
|---|---|---|
| | | |

What would you run **before** you wrote that action into the playbook for good? ___________________________________________

**Check file:**

```python
# check97.py - Week 9 workbook page 9.7: regenerate one row of the table, and the best epoch.
from l4lib.spirals import run

hist = run("wb", lr=1e-2, verbose=False)
print("val at epochs 20, 40, 60:", [round(hist["val"][e - 1], 3) for e in (20, 40, 60)])
best = min(range(60), key=lambda i: hist["val"][i])
print("lowest val", round(hist["val"][best], 3), "at epoch", best + 1)
print("final accuracy", f"{hist['acc'][-1] * 100:.1f}%")
```

---

## 🐞 Page 9.8 — Break It on Purpose (the four bugs from Weeks 1, 5, 6, 8 · 25 min)

The paper's Section C has four "find the bug" questions. **This page has four different ones**, so you can practise the *method* without seeing the paper. **Each program is deliberately broken.** Do **not** run it first. For each: write **(i)** what the bug is, **(ii)** what you think happens when it runs, **(iii)** the fixed line. *Then* run it.

**The reading method (use it every time):** read the **last line** of the error; find **your own file's** line just above it; ask what you expected that line to do.

**Bug 9.8-A. (Week 1)** `price` and `count` must be passed by name.

```python
# DELIBERATE BUG 9.8-A: a keyword-only function called with positional arguments.
def total(*, price, count):
    return price * count

print(total(2.5, 4))
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 9.8-B. (Week 5, SILENT)** The programmer wants the same answer twice. The code prints **two lines**. Predict both before you run.

```python
# DELIBERATE BUG 9.8-B (SILENT): the same input, two modes.
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Dropout(0.3), nn.Linear(16, 1))
x = torch.ones(1, 3)
model.eval()
with torch.no_grad():
    a = model(x).item()
    b = model(x).item()
print(a == b)
model.train()
with torch.no_grad():
    c = model(x).item()
    d = model(x).item()
print(c == d)
```

Line 1 will print ____________ . Line 2 will print ____________ . Why? ___________________ What one line before the "evaluation" would you add to any training script? ___________________

**Bug 9.8-C. (Week 6)** A layer of batch norm, fed one example.

```python
# DELIBERATE BUG 9.8-C (loud): batch norm given a batch of one example, in train mode.
import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.Sequential(nn.Linear(3, 5), nn.BatchNorm1d(5))
print(layer(torch.ones(1, 3)).shape)
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) A fix that keeps train mode: ___________________ A fix that changes the **mode**: ___________________

**Bug 9.8-D. (Week 8)** The programmer wanted the notes after every word, shape `(4, 7, 6)`.

```python
# DELIBERATE BUG 9.8-D (loud): nn.RNN hands back a pair; only one name was kept.
import torch
import torch.nn as nn
torch.manual_seed(0)
rnn = nn.RNN(2, 6, batch_first=True)
out = rnn(torch.ones(4, 7, 2))
print(out.shape)
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**After you have written all four predictions, run them.** Save each as its own file (`bad_a.py` ... `bad_d.py`), run it, and copy the **last line** of the output here. For B, copy both lines.

| Bug | Last line of the real output | Did my prediction match? |
|:--:|---|:--:|
| A | | |
| B | | |
| C | | |
| D | | |

**Slope check (Week 6, no code).** `y = x + f(x)`, and near some `x` the function `f` has slope `0.5`. The slope of `y` there is ____________ . If `f` instead has slope `-1`, the slope of `y` is ____________ , and the "highway" has just **switched off** for the gradient. (Do the nudge on paper if unsure: `y(x + 0.001) − y(x)`, divided by `0.001`.)

---

## 📝 Page 9.9 — Mark Your Own Paper (the same evening, a different colour of pen)

**After the paper.** Your teacher gives you the **marking sheet** (short answers only). Use a pen of a **different colour** from the one you used on the paper. In A, B and C be strict. In D and E mark the **working**, not just the final number.

**The per-week grid.** The "Questions" column tells you which questions belong to which week. Marks available and the "redo if" line are fixed; fill in the rest.

| Week | Topic | Questions | Marks available | Marks earned | % | Redo if marks ≤ | Circle? |
|:--:|---|---|:--:|:--:|:--:|:--:|:--:|
| 1 | Reading a curve; the coin | A1, A2, B1, C1, E(a) | **11** | | | 6 | |
| 2 | Momentum; the running average | A3-A5, B2, D1 | **10** | | | 5 | |
| 3 | Adam; typical size | A6-A8, B3, D2 | **10** | | | 5 | |
| 4 | Schedules; batch size and steps | A9-A11, B4, E(b) | **9** | | | 5 | |
| 5 | Overfitting cures | A12-A14, B5, C2 | **8** | | | 4 | |
| 6 | Norms, residuals, clipping | A15-A17, B6, C3 | **8** | | | 4 | |
| 7 | The sweep; "is it noise?" | A18, B7, E(c) | **7** | | | 4 | |
| 8 | Order; the recurrent cell | A19, A20, B8, C4, D3 | **12** | | | 7 | |
| | **Total** | | **75** | | | | |

*(Marks earned ÷ marks available × 100 = %. A week needs a redo if you scored **60% or less** of its marks, which is the "redo if" column.)*

**Circle at most two weeks.** Choose the **lowest percentages**. If there is a tie, go in this order: **Week 8, then Week 2, then Week 6**: Weeks 10 to 13 lean on those three directly.

My two weeks: ______ and ______ . Redo for week ______ on (day and time) ____________________ . Redo for week ______ on ____________________ .

**Why at most two?** A list of eight redos is a list nobody does. Two is a plan.

**Total mark:** ______ / 75 . **Pattern, not number:** one week at 30% and seven at 90% is a very different X-ray from eight weeks at 65%. Mine looks like: ___________________________________________

**Section E, your own words.** Write one sentence about what Section E taught you about reading a table that you did not know before: ___________________________________________

> **If you wrote "vanishing gradient" or "LSTM" anywhere on the paper**, that is not wrong and not extra: it is from next term, and it is a good sign you have read ahead. Your teacher will say so on the sheet.

---

## 📓 Page 9.10 — The Bug Log

The Bug Log is the most useful page of the course. Today's entries come from the paper and from page 9.8.

**Entry 1: the answer I was most surprised to get wrong.**
*"The answer I was most surprised to get wrong was ______________, because I thought ____________________________."*

_______________________________________________________________________________

**Entry 2: a slip, not a gap.** Find one mark you lost that you **knew** how to get (a rounding slip, a missed sign, a swapped column). What was it, and what is the **one habit** that would have saved it?

Mark lost: ____________________ Habit: _______________________________________

**Entry 3: a bug from page 9.8 that I mispredicted.** (Skip if you got all four.)

| What I predicted | What actually happened | The sentence that would have told me |
|---|---|---|
| | | |

**Entry 4: the silent one.** Bug 9.8-B ran **without an error**. Write, in your own words, **why a silent bug is more dangerous than a loud one** and what you would check to catch it: ___________________________________________

**Entry 5: the rule I will follow in Term 2.** One sentence: ___________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (do this last, from memory)

Seven things, no scrolling up. Tick only if you could do it **now**.

- ☐ Say what log loss a guessing two-class model has, and why it is not 0.5. *(Hint: it is about 0.693.)*
- ☐ Write the PyTorch momentum update in two lines, and say what the two tables did differently after step 1.
- ☐ Say why Adam's first step does not depend on how big the gradient is.
- ☐ Say what `clip_grad_norm_` does **and** what it returns.
- ☐ Say why a dropout layer in train mode makes two scores for the same input differ.
- ☐ Say what "inside noise" means in one sentence, with the number `2`.
- ☐ Give `out` and `h_n` shapes for `x` of shape `(batch, words, k)` and `nn.RNN(k, m, batch_first=True)`.

**Ticks:** ______ / 7 . **The one I could not tick, and when I will redo it:** ___________________________________________

**Next week.** Week 10 trains **the cell from Week 8** for real, and measures what happens to the gradient at the *first* word as the sentence gets longer. It leans on three things from this week: the clean unroll (page 9.4), the running update (page 9.2) and the slope of `x + f(x)` (page 9.8). If your grid shows Week 8 or Week 2 under 60%, **redo those two first.**

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact. Curve tables may differ in the last digit on another CPU or PyTorch build. These answers are for the pages in **this workbook**. They are not the paper's answers, and this page does **not** contain any of them.

### Warm-Up

**W1.** About **0.693** (`-log(0.5)`). **W2.** `0.1 × 4 =` **0.4**. **W3.** The cell gives a **different** final note; a bag gives the **same** answer (identical counts). **W4.** **Smaller** than **2** times the spread. **W5.** Any honest answer; the aim is to compare it with the paper's grid later.

### Page 9.1

No right answer. The point is the **gap between your guess and the grid**. If you ticked "Yes" for a week and scored 40% on it, that is the most valuable finding of the page: the week is softer than you feel.

### Page 9.2

**SGD**

| Step | w before | g | step | w after |
|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.5000 | 3.0000 | 0.3000 | 1.2000 |
| 2 | 1.2000 | 2.4000 | 0.2400 | 0.9600 |
| 3 | 0.9600 | 1.9200 | 0.1920 | 0.7680 |

**Momentum**

| Step | w before | g | v = 0.9·v + g | step | w after |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 1.5000 | 3.0000 | 0.9×0 + 3.0 = **3.0000** | 0.3000 | **1.2000** |
| 2 | 1.2000 | 2.4000 | 0.9×3.0 + 2.4 = **5.1000** | 0.5100 | **0.6900** |
| 3 | 0.6900 | 1.3800 | 0.9×5.1 + 1.38 = **5.9700** | 0.5970 | **0.0930** |

**9.2a.** **Yes** (both `1.2000`). The velocity starts at 0, so on step 1 `v = g` and momentum equals plain SGD. **9.2b.** **Momentum**, at `0.0930` against `0.7680`: a difference of **0.6750**. **9.2c.** The velocity **adds up** past gradients (`v = 0.9·v + g`), so while the gradient keeps the same sign `v` keeps building, even though the gradient itself shrinks (`3.0 → 2.4 → 1.38`). **9.2d.** **It goes past 0.** Real output of the check file:

```text
1 1.2
2 0.69
3 0.093
4 -0.4629
5 -0.8706
```

At step 4 the weight is `-0.4629`: it has overshot the minimum, because the stored velocity (`0.9 × 5.97 = 5.373`, plus `g = 2 × 0.093 = 0.186`, so `v = 5.559`) is still pushing it left. (That overshoot is why momentum can ring around a valley. A guess of "stops at 0" is the usual one; the overshoot is the finding.) Note the check file prints rounded to 4 places; `1.2` is `1.2000`.

### Page 9.3

**9.3a.** Squares `25, 144`; average `84.5`; root **9.1924**.

**9.3b.** Wrong answers: **84.5** (forgot to take the **root**); **−3.5** (took the plain **mean**, signs cancel: `(5 − 12) / 2`); **13.0** (took the **length** of the vector: `√(25 + 144)`).

**9.3c.** `[500, -1200]` → **919.24**; it is **100** times bigger. Root-mean-square **scales** with the numbers.

**9.3d.** `1.00 + 0.02 =` **1.02**. (Negative gradient, so the weight moves **up** by `lr`.) **9.3e.** **1.02** too. Adam divides the gradient by its own typical size, which after one gradient is `|g|`; the size cancels and only the sign is left, times `lr`. The check, a real Adam step, printed `1.02` for both `-3` and `-3000`. **9.3f.** AdamW shrinks the weights **directly** (weight decay applied to the weights themselves) instead of putting decay through the gradient that Adam then rescales.

### Page 9.4

**`x = [1, 0, 1]`**

| Step | x | W_x·x + W_h·(old note) | new note |
|:--:|:--:|---|:--:|
| 1 | 1 | 1.0000 | **0.7616** |
| 2 | 0 | 0 + (−0.5)×0.7616 = **−0.3808** | tanh(−0.3808) = **−0.3634** |
| 3 | 1 | 1 + (−0.5)×(−0.3634) = **1.1817** | tanh(1.1817) = **0.8280** |

**`x = [1, 1, 0]`**

| Step | x | W_x·x + W_h·(old note) | new note |
|:--:|:--:|---|:--:|
| 1 | 1 | 1.0000 | **0.7616** |
| 2 | 1 | 1 + (−0.5)×0.7616 = **0.6192** | tanh(0.6192) = **0.5506** |
| 3 | 0 | 0 + (−0.5)×0.5506 = **−0.2753** | tanh(−0.2753) = **−0.2685** |

**9.4a.** Total **2** both times. Last notes **0.8280** and **−0.2685**. **Different.** **9.4b.** The bag says **identical**; a bag **cannot** tell them apart, the cell **can**. **9.4c.** The note at step 2 is **negative** (`−0.3634`): with `W_h = −0.5` and a zero input, the old positive note is *flipped and halved*, so the sign changed. (The state is a signed summary, not a running count.) **9.4d.** **(ii)** a single squashed summary. What is lost: the cell cannot recover the exact words; only one number per cell, passed through `tanh`, survives. Check-file output (from `nn.RNN`, matches the hand table):

```text
[1, 0, 1] [0.7616, -0.3634, 0.828]
[1, 1, 0] [0.7616, 0.5506, -0.2685]
```

(`0.828` is `0.8280`; Python drops the trailing zero.)

### Page 9.5

| Name | Shape |
|---|:--:|
| `ids` | `(3, 6)` |
| `emb(ids)` | `(3, 6, 2)` |
| `out` | `(3, 6, 7)` |
| `h_n` | `(1, 3, 7)` |

Real output of the check file:

```text
(3, 6) (3, 6, 2) (3, 6, 7) (1, 3, 7)
12 77
```

**9.5a.** Embedding: `6 × 2 =` **12**. RNN: `2×7 + 7×7 + 7 + 7 = 14 + 49 + 14 =` **77**. **9.5b.** The first number is the **number of layers** (one cell stacked once); `h_n` is shaped `(layers, batch, hidden)`. **9.5c.** After every word: **`out`**. After the last word only: **`h_n`** (it is `out[:, -1]`, reshaped with the layer axis in front).

### Page 9.6

**9.6a.** Means: A `0.0500`, B `0.0327`. Gap **0.0173**. Larger spread **0.0082** (A). Twice **0.0163**. `0.0173 > 0.0163` → **bigger than noise, only just.** **9.6b.** A `0.0500` against C `0.0460`: gap **0.0040**. Larger spread **0.0082**; twice **0.0163**. `0.0040 < 0.0163` → **inside noise.** **9.6c.** Any of: **run more seeds**, or re-run with different seeds, before trusting a gap that clears the line by `0.001`; the rule is a screen, and 3 seeds is few. **9.6d.** The **mean** and the **spread** (or: the other seeds' values). **9.6e.** `(840 ÷ 120) × 10 = 7 �� 10 =` **70** steps.

### Page 9.7

**9.7a.** Model answers (yours may use different words and numbers, as long as each sentence names the curve and each number is *in the table*):

- **W:** **learns fast and well**: val falls from `0.678` at epoch 1 to `0.073` at epoch 10, and ends at `0.026` (99.4%). *(Mild wobble: val is `0.029` at epoch 20 and `0.085` at epoch 40, then back down.)*
- **Y:** **blows up, then sits on the coin**: the first-epoch train loss is `7837888.5` and val is `5632.9`, then it hovers near `0.69` (val `0.694` at epoch 60) at **46.9%**.
- **Z:** **learns quickly but is noisy**: val `0.060` at epoch 5, but it goes **up and down** (`0.125` at epoch 10, `0.049` at epoch 20, `0.136` at epoch 40) and ends at `0.059`.

**9.7b.** **Train** is the **average over every step during the epoch**, including the first huge steps; **val** is measured **once, after** the epoch, on the validation set, with the weights as they ended up. Different things, so different numbers. **9.7c.**

| | val ep 20 | val ep 40 | val ep 60 | up from 20 to 40? |
|:--:|:--:|:--:|:--:|:--:|
| W | 0.029 | 0.085 | 0.026 | **yes** (`0.029 → 0.085`) |
| Z | 0.049 | 0.136 | 0.059 | **yes** (`0.049 → 0.136`) |

**9.7d.** The table shows **6 of the 60 epochs**; the lowest value could sit at any of the epochs not printed. Real output of the check file:

```text
val at epochs 20, 40, 60: [0.049, 0.136, 0.059]
lowest val 0.012 at epoch 31
final accuracy 99.2%
```

The lowest `0.012` is at **epoch 31**, which is not printed. That is why you keep the best weights with `copy.deepcopy`, rather than trusting the last epoch (Week 5).

**9.7e.** A good row: **SYMPTOM** the first-epoch train loss is huge (`7837888.5`) and val then sits near `0.69` → **CHECK** print the loss of the first three epochs and see whether the first is enormous, and whether val is stuck near the `0.693` coin → **ACTION** lower `lr` **by one step of 10×** (for example `1.0` to `0.1`), **one knob**. **Before you write it in for good**, run it on **at least three seeds** and check the gap is bigger than twice the spread. (A student who writes "clip the gradient" has picked a plausible one-knob action; it is **not guaranteed to work**, so credit comes from a **check** that the action was *measured* rather than assumed.)

### Page 9.8

Real outputs, each program run on its own:

```text
A  TypeError: total() takes 0 positional arguments but 2 were given
B  True
   False
C  ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 5])
D  AttributeError: 'tuple' object has no attribute 'shape'
```

(The real traceback has more lines above each last line. For C the middle lines are inside PyTorch.)

**A.** (i) the `*` makes every argument keyword-only; the call passed them by **position**. (ii) A **loud** error: `TypeError`, the function takes **0** positional arguments but **2** were given. (iii) `total(price=2.5, count=4)`.

**B.** Line 1 **True** (eval: dropout is off, same answer). Line 2 **False** (train: dropout is **on**, a different random half is zeroed each call). **Silent** bug: in a real script the call happens in **train** mode, no error, and the "validation score" is a **noisy** one. Add **`model.eval()`** (before the evaluation, and `model.train()` again afterwards).

**C.** (i) Batch norm takes mean and spread **across the batch** for each feature; with **one** example there is no spread to compute. (ii) `ValueError: Expected more than 1 value per channel when training`. (iii) Give it **two or more** examples, e.g. `torch.ones(2, 3)`, or switch to `layer.eval()` (which uses stored running statistics instead).

**D.** (i) `nn.RNN` returns a **pair**, `(out, h_n)`; only one name was kept, so `out` is the whole **tuple**. (ii) `AttributeError: 'tuple' object has no attribute 'shape'`. (iii) `out, h_n = rnn(torch.ones(4, 7, 2))`. Then `out.shape` is `(4, 7, 6)`.

**Slope check.** Slope `1 + 0.5 =` **1.5**. For `f` slope `−1`: `1 + (−1) =` **0**, "the highway has switched off", because the two slopes cancel exactly.

### Page 9.9

No fixed answer: your marks. Two things to check: (1) the `Marks earned` column adds to your total; (2) you circled **at most two** weeks, and each has a **day and time** next to it. The tie order is **8, then 2, then 6**.

### Page 9.10 and Self-Check

Your own words. A good **Entry 4** says: a silent bug **runs**, prints a plausible number and gets written into a report, so nothing tells you to look; the **check** is to ask whether the result is **repeatable** (here: same input, same answer, twice) and whether the **mode** (`train`/`eval`) is the one you meant. A good **Entry 5** is short and about a *habit* ("write the shapes before running", "quote a number from the table"), not a topic.

**Self-Check:** if you could tick fewer than five, you now have your **two** redos; they are the same as the ones on page 9.9.
