# Workbook — Week 11: Gates: Memory That Adds Instead of Multiplies

**Name:** ________________________________  **Date:** ______________

[⬅ Week 10](week-10.md) · [📖 Read the chapter first](../student-guide/week-11.md) · [Course Home](../README.md) · [Next ➡](week-12.md)

---

> **Rules for this workbook.** Six pages and a Bug Log: **by hand first** (dials, then one LSTM unit), then **your own run** (the cell check, the dial grid, the seeds and the forget bias), then a short report. Pages 11.1 and 11.2 need a calculator with a **power key** (`x^y`) and an **`e^x` key**. Pages 11.3 to 11.5 copy numbers that **your own `week11.py` printed**.
>
> **Pen first, then run.** Write every prediction before you run anything. Use **one colour of pen for predictions and another for measurements** on page 11.4.
>
> **Where the numbers came from.** Every worked example and every answer was printed by a real CPU run (PyTorch, `torch.manual_seed(...)` with the seed named on the page). By-hand numbers are plain arithmetic and match exactly. On another computer or PyTorch build the **last digit** of a number such as `5.77e-02` can move, and the gaps on page 11.3 (about `1e-08`) can differ; the **exponent** and the shape of every table will not.
>
> **Copy exponents in full.** `2.05e-09` means `0.00000000205`. If you drop the `e-09` you are wrong by a factor of a billion.
>
> **There is no language model and no stand-in in this workbook.** Every layer is real PyTorch with **untrained, seeded random weights**, run on random numbers. **Nothing is trained today**, nothing is downloaded and nothing needs the internet.
>
> Carry **four decimals** in every calculation. Run any check file from a folder of your own, and delete what it writes.

---

![Map of the 36 weeks with Week 11, Gates, highlighted in Term 2](../figures/fig-w11-0-where-this-fits.svg)
*Figure W11.0 — Week 11 gives the loop gates, so memory can be added to instead of rewritten.*

## ✅ Warm-Up (5 min, before anything else)

**W1.** Last week forty slopes of about one half were multiplied together. Without a calculator: is the answer **tiny / near 1 / large** (circle one)? ____________

**W2.** In Week 6 a residual highway added the input to `f(x)`. If the slope of `f` is `0.5`, what is the slope of `x + f(x)`? ____________ In one word, why does an **addition** keep the slope from shrinking? ____________

**W3.** The sigmoid squasher (Level 3) turns any score into a number between ______ and ______ . What does it give for a score of exactly `0`? ____________

**W4.** `nn.GRU` gave its second answer as one note of shape `(1, 16)`. The second answer of `nn.LSTM` is **one tensor / a pair of tensors** (circle one).

---

## 🎛️ Page 11.1 — Dials by Hand (15 min)

A **gate** is a dial between 0 and 1. The network makes the dial from a score: `dial = sigmoid(score) = 1 / (1 + e^(-score))`. Use your `e^x` key for `e^(-score)`, and your power key for `f ** 40`. Write a **prediction** first (**near 0**, **near one half**, **near 1**), then the answer to four decimals.

**Worked example (done for you; scores your page does not use).** `sigmoid(-1) = 1 / (1 + e^1) = 1 / 3.7183 =` **`0.2689`**: a negative score gives a dial below one half. `sigmoid(4) =` **`0.9820`**: a large score gives a dial close to 1. Now forty steps of a *constant* dial: `0.7 ** 40 =` **`6.367e-07`** (that is `0.0000006367`), so even a dial of `0.7` leaves almost nothing. And counting: multiplying by `0.8` first drops below one half at the **4th** multiplication (`0.8, 0.64, 0.512, 0.4096`).

| Part | Question | My prediction (near 0 / near one half / near 1) | My answer |
|:--:|---|:--:|:--:|
| a | `sigmoid(-2)` | | |
| b | `sigmoid(0)` | | |
| c | `sigmoid(1)` | | |
| d | `sigmoid(3)` | | |
| e | `sigmoid(5)` | | |

| Part | Question | My prediction (tiny / middling / near 1) | My answer |
|:--:|---|:--:|:--:|
| f | `0.5 ** 40` (a dial of exactly one half, forty times) | | |
| g | `0.88 ** 40` | | |
| h | `0.99 ** 40` | | |

**i. Counting.** Multiplying by `0.95` again and again: how many multiplications until the value is **first below one half**? Write each value (four decimals) until you get there: ______________________________ . Answer: ____________

**j. The dial that keeps half.** From Week 10, forty people each passing on 95% left `0.1285`. Try these dials in `f ** 40` and find the one that leaves **closest to one half**:

| dial | `0.98` | `0.982` | `0.983` | `0.985` |
|:--:|:--:|:--:|:--:|:--:|
| `f ** 40` | | | | |

Closest to `0.5000`: ____________

**k. Look at b and f together.** A dial of exactly one half is what an **untrained** gate gives (a score near 0). In one sentence, what does that say about forty steps? ___________________________________________

**l. Look at g and h together.** The dials `0.88` and `0.99` look close. How far apart are their answers after forty steps? ___________________________________________

**Check file** (run it only after the tables are written):

```python
# check111.py - Week 11 workbook page 11.1: check the dial answers.
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

for z in [-2, 0, 1, 3, 5]:
    print(f"  a-e) sigmoid({z}) = {sigmoid(z):.4f}")
for label, f in [("f", 0.5), ("g", 0.88), ("h", 0.99)]:
    print(f"  {label}) {f} ** 40 = {f ** 40:.4g}")
value, k = 1.0, 0
while value > 0.5:
    value = value * 0.95
    k = k + 1
print(f"  i) 0.95 first below one half after {k} multiplications ({value:.4f})")
for f in [0.98, 0.982, 0.983, 0.985]:
    print(f"  j) {f} ** 40 = {f ** 40:.4f}")
```

Which parts did my hand answer miss by more than `0.0005`? ____________ The slip (the sign of the score, `e^z` instead of `e^-z`, a rounded step)? ___________________________________________

---

## 🧮 Page 11.2 — One Unit, by Hand (Week 8's spike · 25 min)

One LSTM unit run for three steps on the spike `x = [1, 0, 0]`. These are **the same dials as the lesson's block 2, with one change: the forget dial is `sigmoid(2)`**, not `sigmoid(3)`.

> **The recipe, at every step `t`:**
> input dial `i = sigmoid(5x - 2.5)` · candidate `g = tanh(2x)` · **memory `c = f x (old c) + i x g`** · note `h = o x tanh(c)`
> with **`f = sigmoid(2) = 0.8808`** (the same at every step) and **`o = sigmoid(1) = 0.7311`**. The memory starts at `c = 0`.

If your calculator has no `tanh` key: `tanh(a) = (e^(2a) - 1) / (e^(2a) + 1)`. `tanh(0) = 0`.

**Worked example (done for you; a different forget dial, `f = sigmoid(1) = 0.7311`, so your numbers will be different).** Step 1: `i = sigmoid(2.5) = 0.9241`, `g = tanh(2) = 0.9640`, `c = 0.7311 x 0 + 0.9241 x 0.9640 =` **`0.8909`**, `h = 0.7311 x tanh(0.8909) = 0.7311 x 0.7118 =` **`0.5204`**. Step 2 (`x = 0`): `i = sigmoid(-2.5) = 0.0759`, `g = tanh(0) = 0`, so `c = 0.7311 x 0.8909 + 0.0759 x 0 =` **`0.6513`**, which is **`73.1%`** of step 1. Step 3: `c =` **`0.4761`**, **`53.4%`**. (Notice that `73.1` is just `f`, and `53.4` is `f x f`.)

**Fill in your own** (forget dial `f = sigmoid(2) = 0.8808`):

| Step | `x` | `i` | `g` | `c = f x (old c) + i x g` | `h = o x tanh(c)` | `c` as % of step 1 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 1 | | | | | 100.0 |
| 2 | 0 | | | | | |
| 3 | 0 | | | | | |

**a.** At steps 2 and 3, `x = 0`, so `g =` ______ and the new part `i x g =` ______ . In one sentence, what does the memory do at those steps? ___________________________________________

**b. The slope back.** The memory update `c = f x (old c) + i x g` is a sum, so (Week 6) the slope of `c` with respect to the **old** `c` is the number that multiplies it: ______ . From step 3 back to step 1 you cross two such steps: slope `= f x f =` ____________ (compare with your last percentage).

**c. A dial of one half.** Redo the memory column with `f = sigmoid(0) = 0.5` (the same `i`, `g` and step 1):

| Step | 1 | 2 | 3 |
|:--:|:--:|:--:|:--:|
| `c` | | | |
| `c` as % of step 1 | 100.0 | | |

What pattern do the percentages follow, and what Week 8 or Week 10 number does that remind you of? ___________________________________________

**d.** Which dial, `sigmoid(2)` or `sigmoid(0)`, would you want if the network must remember the spike? ____________

**e. Predict (before the key).** Keep `f = sigmoid(2) = 0.8808` and let forty steps go by with `x = 0` all the way. The share of the spike still in the memory would be closest to `0.5`, `0.006` or `0.000000001`? My guess: ____________ Test it with your calculator: `0.8808 ** 40 =` ____________

**Check file:**

```python
# check112.py - Week 11 workbook page 11.2: the hand unit with a forget dial of sigmoid(2), spike (1, 0, 0).
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

for label, fz in [("f = sigmoid(2)", 2.0), ("f = sigmoid(0)", 0.0)]:
    f, o, c = sigmoid(fz), sigmoid(1.0), 0.0
    memory = []
    print(label, "=", round(f, 4))
    print("step  x    i       g       c       h     c as % of step 1")
    for t, x in enumerate([1, 0, 0], start=1):
        i = sigmoid(5 * x - 2.5)
        g = math.tanh(2 * x)
        c = f * c + i * g
        h = o * math.tanh(c)
        memory.append(c)
        print(f"  {t}   {x}   {i:.4f}  {g:.4f}  {c:.4f}  {h:.4f}   {100 * c / memory[0]:.1f}")
    print("slope back from step 3 to step 1: f ** 2 =", round(f ** 2, 4))
```

Did the first table match mine? ____________ The first row I got wrong, and why: ___________________________________________

---

![Two bar panels over four steps: the RNN note falls to 11.8 percent of step 1, the LSTM memory only to 86.4 percent](../figures/fig-w11-1-rewrite-versus-add.svg)
*Figure W11.1 — A memory that is scaled and added to keeps its past; a note that is rewritten at every step loses it.*

## 🧩 Page 11.3 — The Cell From Scratch (block 3 · 20 min)

**Part 1: count before you look.** An `nn.LSTMCell(D, H)` takes `D` numbers in and keeps `H` numbers of memory. Its scores come in **four groups of `H`** (input dial, forget dial, candidate, output dial), so `weight_ih` has `4 x H` rows and `weight_hh` has `4 x H` rows. The total count is

> **`4 x (H x D + H x H + H + H)`**

**Worked example (done for you).** `D = 2`, `H = 5`: `weight_ih` is `(20, 2)`, `weight_hh` is `(20, 5)`, `bias_ih` is `(20,)`. Count `= 4 x (5x2 + 5x5 + 5 + 5) = 4 x 45 =` **`180`**.

| `D` | `H` | `weight_ih` shape | `weight_hh` shape | `bias_ih` shape | numbers in the cell |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 8 | | | | |
| 6 | 10 | | | | |

**Check file for Part 1:**

```python
# check113.py - Week 11 workbook page 11.3: count the numbers in a cell BEFORE looking, then look.
import torch
import torch.nn as nn

for D, H in [(2, 5), (3, 8), (6, 10), (4, 16)]:
    cell = nn.LSTMCell(D, H)
    mine = 4 * (H * D + H * H + H + H)
    print(f"D = {D}, H = {H}: weight_ih {tuple(cell.weight_ih.shape)}  weight_hh {tuple(cell.weight_hh.shape)}  bias_ih {tuple(cell.bias_ih.shape)}  numbers {sum([p.numel() for p in cell.parameters()])}  formula {mine}")
```

Did my counts match the first two lines? ____________ The last line is the cell of your lesson (`D = 4`, `H = 16`): its count is ____________ . Last week's `nn.RNN` of the same size had `352`. The ratio `count / 352` is ______ : one group of scores for the RNN, ______ groups for the LSTM.

**Part 2: your step against PyTorch's.** Block 3 of your `week11.py` ran **your own** `lstm_step` and `nn.LSTMCell` side by side for five steps. Copy what it printed:

| Step | biggest gap in `h` | biggest gap in `c` |
|:--:|:--:|:--:|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

`allclose` printed: ____________ ____________

**a.** The biggest gap in the whole table: ____________ . Is it **below `1e-06`**? ____________

**b.** Finish in your own words: *"A gap of about `1e-08` means ___________________________________________."* (Hint: float32 keeps about seven digits, and the two versions add the same numbers in a different order.)

**c.** Which slice of the 64 scores is the **forget** dial: `z[0:16]`, `z[16:32]`, `z[32:48]` or `z[48:64]`? ____________ How do you know, from the order in which `lstm_step` slices them? ___________________________________________

**d.** If a gap were of order `1` instead of `1e-08`, what would be the first thing to suspect? ___________________________________________

---

## 🎲 Page 11.4 — The Dial Grid (blocks 6 and 7 · 30 min)

The experiment: *how much the last output cares about the **first** word, as a fraction of how much it cares about the **last** word*, for four layers and four sequence lengths `T`. Seed 0. The four layers are an `nn.RNN`, an `nn.GRU`, an `nn.LSTM` (defaults), and an `nn.LSTM` with the **forget bias set to 2**.

**Three letters** (the cut-offs are ours, chosen so you can commit):

- **T** tiny: below `1e-6`
- **S** small: `1e-6` up to `1e-2`
- **L** level: above `1e-2`

**Worked example (done for you; lengths your grid does not use, seed 0).** At `T = 5` the RNN printed `4.11e-02` (`0.0411`, above `0.01`): **L**. At `T = 30` the RNN printed `2.42e-08` (`0.0000000242`): **T**. At `T = 30` the default LSTM printed `1.70e-06` (`0.0000017`, just above `1e-6`): **S**, although it is already small, because the cut-off is ours. At `T = 30` the LSTM with forget bias 2 printed `1.47e-01`: **L**.

### Step 1 — predict all 16 cells before running anything (first colour of pen)

Write one letter in each cell.

| layer | T = 10 | T = 20 | T = 40 | T = 80 |
|---|:--:|:--:|:--:|:--:|
| rnn | | | | |
| gru | | | | |
| lstm | | | | |
| lstm, forget bias 2 | | | | |

### Step 2 — run blocks 6 and 7 and copy the numbers **with their exponents** (second colour of pen)

The first three rows come from block 6; the fourth row comes from the **last table** of block 7 (the row for forget bias `2.0`).

| layer | T = 10 | T = 20 | T = 40 | T = 80 |
|---|:--:|:--:|:--:|:--:|
| rnn | | | | |
| gru | | | | |
| lstm | | | | |
| lstm, forget bias 2 | | | | |

### Step 3 — colour in which predictions were right

Correct predictions: ______ / 16. **The score is not the point. The pattern of the misses is.** My misses were mostly in row(s): ____________ and in the direction of (too hopeful / too gloomy / mixed): ____________

### Step 4 — one sentence per row

Each sentence gives a **direction** (falls, rises, hovers) and **one number copied with its exponent**.

- **rnn:** ___________________________________________
- **gru:** ___________________________________________
- **lstm:** ___________________________________________
- **lstm, forget bias 2:** ___________________________________________

**a.** Look at the **gru** and **lstm** rows. Before the run, did you predict **L** for them at `T = 40` or `T = 80`? ____________ What did you see? ___________________________________________

**b. The sentence that must appear somewhere on this page.** Complete it from the grid: *"At default settings, the gates by themselves ______________________________."*

**c.** Between `T = 20` and `T = 40`, by roughly what factor did the **rnn** number fall? (divide the `T = 20` value by the `T = 40` value; round to a power of ten) ____________ And the **forget bias 2** row between the same two lengths? ____________

**d. The question that makes the activity.** *"Did anything learn?"* Answer **yes** or **no**, and say why in one sentence that uses the words *starting point*: ___________________________________________

---

## 🌱 Page 11.5 — Three Seeds, and the Forget Bias (block 7 · 20 min)

Block 7 first ran **three seeds** at `T = 40` for five rows, then swept **the forget bias** at four lengths for seed 0. Copy both tables from your run.

**Worked example (done for you; seed 3, which block 7 did not use).** At `T = 40`: rnn `1.4e-09`, default lstm `6.0e-08`, lstm with forget bias 2 `2.8e-02`. At `T = 20`, seed 3, forget bias 0 gave `9.26e-05` and forget bias 3 gave `5.85e-01`: the same layer, one number different, about **6,300 times** apart (`0.585 / 0.0000926`). *Notice:* the default lstm beat the rnn here (`6.0e-08` against `1.4e-09`), and the gap of about 40 times is within what the seeds wander, as the table below will show.

**Table 1: seeds, `T = 40`, first word over last word.**

| layer | seed 0 | seed 1 | seed 2 |
|---|:--:|:--:|:--:|
| rnn | | | |
| gru | | | |
| lstm | | | |
| lstm, forget bias 0 | | | |
| lstm, forget bias 2 | | | |

**Table 2: the dial, seed 0.**

| forget bias (sigmoid of it) | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| 0.0 (0.500) | | | | |
| 1.0 (0.731) | | | | |
| 2.0 (0.881) | | | | |
| 4.0 (0.982) | | | | |

**a. Spread against gap.** In Table 1, the **lstm** row runs from ____________ to ____________ across the three seeds: the biggest is about ______ times the smallest. The gap between the `lstm, forget bias 0` row and the `lstm, forget bias 2` row at seed 0 is about ______ times. Which is bigger, the **spread between seeds** or the **gap made by the dial**? ____________

**b.** From Table 1 alone, can you say the lstm is better than the gru at `T = 40`? ____________ Why or why not? (Look at the three gru values and the three lstm values.) ___________________________________________

**c.** In Table 2, the row for bias `0.0` and the row for bias `2.0`, at `T = 80`: how many powers of ten apart? ____________ At bias `4.0`, does the number fall as `T` goes from 40 to 80? ____________ By roughly what factor? ____________

**d.** Link to page 11.1: a dial of `0.881` leaves `0.881 ** 40 =` ____________ of a signal after forty steps. Does that match the *size* of the `T = 40` entry in the bias `2.0` row of Table 2 (the same order of magnitude)? ____________ (They need not agree exactly: the dial changes from step to step and the layer also has a recurrent weight.)

**e. The sentence of the page.** Write one sentence for Table 2 that gives the direction and one number with its exponent, **and says what was not shown**: ___________________________________________

___________________________________________

---

![Four panels for forget bias 0, 1, 2 and 4 showing the dial rising from 0.510 to 0.981 and the first-to-last gradient ratio rising from 1.93e-09 to 1.08](../figures/fig-w11-2-forget-bias-dial.svg)
*Figure W11.2 — One number in the bias, set before training, decides whether the first step can still reach the last.*

## 📝 Page 11.6 — The Report (20 min)

Write **four sentences**, in your own words, to someone who has not done this week.

**Rules.** Every number must have been printed by **your own run in the last 24 hours**; copy it **with its exponent**; state the **seed**.

1. The ratio at `T = 40` for the default LSTM and for the LSTM with forget bias 2, with the seed: ___________________________________________
2. **Why** that happens, in one sentence (what is the memory updated by, and what is the slope back through it?): ___________________________________________
3. What the dial starts at in an untrained LSTM, and what happens to the highway at default settings: ___________________________________________
4. What this week did **not** show. (Hint: was anything trained?) ___________________________________________

**Self-marking** (tick what your report has):

- ☐ Two numbers with exponents, one default and one with the forget bias, from my own run, seed stated (2 marks)
- ☐ The cause in one sentence: the memory is updated by **adding**, and the slope back is the forget gate (1 mark)
- ☐ That at default settings the gates alone did not help, or that the dial starts near one half (1 mark)
- ☐ What was **not** shown: nothing was trained, so this is about the starting point (2 marks)

**Marks: ______ / 6.** A sentence that says "the LSTM solves vanishing gradients" loses the last two marks, because this week measured an untrained layer on random numbers.

---

## 📓 Page 11.6b — The Bug Log

The Bug Log is the most useful page of the course. Copy only the **last line** of a traceback, not all of it.

**Copy this sentence in your own handwriting:**

> **"An LSTM has a highway; whether the highway is open at the start depends on where the dial is set, and setting it is not learning."**

___________________________________________________________________________

**Entry 1: Break It On Purpose, block 1 (the state is a pair).** I predicted it would: ____________ . Actually it: ____________ . The last line of the error: ___________________________________________ . What `hx[0]` was, and what the cell wanted there: ___________________________________________ . The fix: ___________________________________________

**Entry 2: Break It On Purpose, block 2 (`fill_` on a tracked knob).** The last line of the error: ___________________________________________ . The one line of difference from blocks 4 and 5, which did the same `fill_` without an error: ___________________________________________ . In my own words, what "I am editing, not learning" means: ___________________________________________

**Entry 3: the silent one (DELIBERATE).** Add this under block 7 in a scratch copy of `week11.py`. It prints **no error**. It turns the dial on the **wrong group** of the bias. Predict first: will the answer look like the right group, like no dial at all, or something in between? ____________

```python
# DELIBERATE BUG 11.6-C (SILENT): the dial was turned on the WRONG GROUP. [0:H] is the INPUT gate, not the forget gate.
def make_layer_wrong(seed, value):
    torch.manual_seed(seed)
    layer = nn.LSTM(D, H)
    with torch.no_grad():
        layer.bias_ih_l0[0:H].fill_(value)
        layer.bias_hh_l0[0:H].fill_(0.0)
    return layer

def first_over_last(layer, seed):
    sizes = reach(layer, 40, seed)
    return sizes[0] / sizes[-1]

print("T = 40, first word / last word, seed 0:")
print("  wrong group [0:H]   ", f"{first_over_last(make_layer_wrong(0, 2.0), 0):.1e}")
print("  right group [H:2H]  ", f"{first_over_last(make_layer('lstm', 0, 2.0), 0):.1e}")
print("  no dial at all      ", f"{first_over_last(make_layer('lstm', 0), 0):.1e}")
```

What it printed: wrong group ____________ , right group ____________ , no dial at all ____________ . How many powers of ten short of the right group is the wrong one? ______ . The **tell** that nothing was wrong *loudly*: ___________________________________________ . The fix (which slice, and how I can check the order of the four groups): ___________________________________________

**Entry 4: the prediction I got most wrong** on page 11.4 was the layer ____________ at `T = ______` . I predicted ______ , the number was ____________ . The reason I was wrong: ___________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (do this last, from memory)

- ☐ Say what a gate is, in one sentence with the words *dial* and *sigmoid*.
- ☐ Write the memory update `c = f x (old c) + i x g` from memory, and say what the slope back through it is.
- ☐ Say why a dial of one half is Week 10's disease again (`0.5 ** 40`), and why a dial of `0.95` or more is not.
- ☐ Say what `nn.LSTM` returns as its **second** answer, and how that differs from `nn.GRU`.
- ☐ Say which slice of the bias is the forget group, and why the `fill_` needs `torch.no_grad()`.
- ☐ Say what this week did **not** show.

**Ticks:** ______ / 6 . **The one I could not tick, and when I will redo it:** ___________________________________________

**Next week.** Week 12 puts an LSTM to work on something real: **231 names**, learned letter by letter, so it can invent new ones. Nothing from this week was trained yet. **If page 11.4 is blank, do it before Week 12.**

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact. Measured numbers may differ in the last digit on another CPU or PyTorch build; the exponents and the shape of each table will not. These answers are for the pages in **this workbook**.

### Warm-Up

**W1.** **Tiny** (`0.5 ** 40` is about `1e-12`). **W2.** `1 + 0.5 =` **1.5**; the slope of a **sum** is the sum of the slopes, so the `1` from the added input always survives. **W3.** Between **0** and **1**; for a score of `0` it gives **0.5**. **W4.** **A pair of tensors**, `(h_n, c_n)`.

### Page 11.1

| Part | Prediction | Answer |
|:--:|:--:|:--:|
| a `sigmoid(-2)` | near 0 | **0.1192** |
| b `sigmoid(0)` | one half | **0.5000** |
| c `sigmoid(1)` | between one half and 1 | **0.7311** |
| d `sigmoid(3)` | near 1 | **0.9526** |
| e `sigmoid(5)` | near 1 | **0.9933** |
| f `0.5 ** 40` | tiny | **9.095e-13** |
| g `0.88 ** 40` | tiny / middling | **0.0060** |
| h `0.99 ** 40` | near 1 / middling | **0.669** |

**i.** **14** multiplications (the value is `0.4877`; at 13 it is still `0.5133`). **j.**

| dial | `0.98` | `0.982` | `0.983` | `0.985` |
|:--:|:--:|:--:|:--:|:--:|
| `f ** 40` | 0.4457 | 0.4836 | **0.5037** | 0.5463 |

`0.983` is closest to `0.5`. **k.** A dial of exactly one half leaves about `9e-13` after forty steps: nothing. An untrained gate starts there. **l.** `0.006` against `0.669`: about **110 times** apart (`0.669 / 0.006`), although the dials differ by only `0.11`. *Common errors:* `sigmoid(0) = 0` (it is one half); `0.88 ** 40` rounded to `0.9`; using `e^z` instead of `e^-z` (gives `1 - sigmoid`, the wrong way round).

### Page 11.2

With `f = sigmoid(2) = 0.8808`:

| Step | `x` | `i` | `g` | `c` | `h` | `c` as % of step 1 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 1 | 0.9241 | 0.9640 | **0.8909** | 0.5204 | 100.0 |
| 2 | 0 | 0.0759 | 0.0000 | **0.7847** | 0.4791 | 88.1 |
| 3 | 0 | 0.0759 | 0.0000 | **0.6912** | 0.4377 | 77.6 |

**a.** `g = tanh(0) = 0` and `i x g = 0`: nothing new is written, so the memory just **shrinks by the factor `f`** (each step is `0.8808` of the one before). **b.** The number that multiplies the old `c` is **`f = 0.8808`**; over two steps `f x f =` **0.7758**, which matches `77.6%` up to rounding. **c.**

| Step | 1 | 2 | 3 |
|:--:|:--:|:--:|:--:|
| `c` | 0.8909 | 0.4454 | 0.2227 |
| `c` as % of step 1 | 100.0 | 50.0 | 25.0 |

It **halves every step**: exactly the Week 8 note (`100, 47.7, 23.6` ...) and the Week 10 compounding. **d.** `sigmoid(2)` (the bigger dial keeps more). **e.** **`0.006`**; `0.8808 ** 40 = 0.0062` (the lesson's block 1 printed `6.238e-03` for `sigmoid(2) ** 40`). Even a dial of `0.88` leaves very little after forty steps; you need `0.95` or more to keep a real share. *Common errors:* putting `tanh` around the **old** `c` inside the update (the update has no `tanh` there); adding `h` instead of `c`; reusing the step-1 `i` at step 2 (at `x = 0` it is `0.0759`).

### Page 11.3

**Part 1.**

| `D` | `H` | `weight_ih` | `weight_hh` | `bias_ih` | numbers |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 8 | (32, 3) | (32, 8) | (32,) | **416** |
| 6 | 10 | (40, 6) | (40, 10) | (40,) | **720** |

(`4 x (8x3 + 8x8 + 8 + 8) = 4 x 104 = 416`; `4 x (10x6 + 10x10 + 10 + 10) = 4 x 180 = 720`.) The lesson's cell is **1408** (`4 x (64 + 256 + 16 + 16)`); `1408 / 352 = 4`: **one** group of scores for the RNN, **four** for the LSTM.

**Part 2** (from block 3):

| Step | biggest gap in `h` | biggest gap in `c` |
|:--:|:--:|:--:|
| 1 | 0.0e+00 | 0.0e+00 |
| 2 | 7.5e-09 | 1.5e-08 |
| 3 | 3.7e-09 | 7.5e-09 |
| 4 | 3.7e-09 | 7.5e-09 |
| 5 | 1.5e-08 | 3.0e-08 |

`allclose`: `True True`. **a.** `3.0e-08` (in `c`, step 5); **yes**, far below `1e-06`. Accept any gap at or below `1e-06`. **b.** *"A gap of about `1e-08` is float rounding, so my step and PyTorch's are the same calculation."* **c.** **`z[16:32]`**, the second slice: `lstm_step` takes the input dial from `z[0:H]`, the forget dial from `z[H:2*H]`, the candidate from `z[2*H:3*H]` and the output dial from `z[3*H:4*H]`, and PyTorch's cell agreed with that order. **d.** The groups are in the **wrong order** (usually input and forget swapped), or only `h` was passed in as the state (Bug Log entry 1).

### Page 11.4

The measured grid (seed 0; letters from the cut-offs):

| layer | T = 10 | T = 20 | T = 40 | T = 80 |
|---|:--:|:--:|:--:|:--:|
| rnn | 6.72e-03 (S) | 1.77e-05 (S) | 1.99e-10 (T) | 6.48e-20 (T) |
| gru | 2.84e-02 (L) | 1.49e-04 (S) | 1.36e-08 (T) | 6.71e-18 (T) |
| lstm | 7.65e-03 (S) | 2.53e-04 (S) | 2.05e-09 (T) | 6.64e-16 (T) |
| lstm, forget bias 2 | 3.54e-01 (L) | 3.10e-01 (L) | 5.77e-02 (L) | 3.37e-02 (L) |

**Step 3:** do not mark the T/S/L score; look for a student who predicted **L** for the gru and lstm rows and then said what surprised them. **Step 4, model sentences:**

- **rnn:** falls by a huge factor along the row: `6.72e-03` at 10 and `2.0e-10` at 40, `6.5e-20` at 80.
- **gru:** the same shape, a little higher at short lengths (`2.84e-02` at 10), still `6.71e-18` at 80.
- **lstm:** the same shape (`7.65e-03` at 10, `6.64e-16` at 80).
- **lstm, forget bias 2:** barely falls: `3.54e-01` at 10 and `3.37e-02` at 80, within a factor of about 10.

**a.** Students often predict **L** for the gru and lstm rows because "gates fix memory"; the numbers say **T** at `T = 40` and `T = 80`. **b.** *"At default settings, the gates by themselves did not help (the gru and lstm rows fall as far as the rnn row)."* **c.** `1.77e-05 / 1.99e-10` is about **100,000 (`1e5`)** for the rnn; the forget bias 2 row: `0.310 / 0.0577` is about **5** (a factor of ten at most). **d.** **No.** Nothing was trained; we only looked at the *starting point* of untrained layers on random numbers, and the bias is a number we wrote in.

### Page 11.5

**Table 1:**

| layer | seed 0 | seed 1 | seed 2 |
|---|:--:|:--:|:--:|
| rnn | 2.0e-10 | 6.3e-11 | 3.1e-10 |
| gru | 1.4e-08 | 1.5e-09 | 8.9e-10 |
| lstm | 2.0e-09 | 7.1e-08 | 6.8e-09 |
| lstm, forget bias 0 | 9.8e-10 | 4.3e-09 | 4.2e-09 |
| lstm, forget bias 2 | 5.8e-02 | 1.3e-01 | 2.2e-01 |

**Table 2:**

| forget bias (sigmoid) | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| 0.0 (0.500) | 7.20e-03 | 4.86e-05 | 9.83e-10 | 3.92e-17 |
| 1.0 (0.731) | 1.07e-01 | 2.95e-02 | 3.52e-04 | 1.44e-06 |
| 2.0 (0.881) | 3.54e-01 | 3.10e-01 | 5.77e-02 | 3.37e-02 |
| 4.0 (0.982) | 7.23e-01 | 8.46e-01 | 3.52e-01 | 1.61e-01 |

**a.** The lstm row runs from `2.0e-09` to `7.1e-08`: about **35 times** between the smallest and biggest. The dial gap at seed 0 is `5.77e-02 / 9.83e-10`, about **`6e7`** (sixty million; accept "seven to eight orders"). **The dial is bigger**, by about six orders of magnitude more than the seed spread (a factor of about 35). **b.** **No.** The gru values (`1.4e-08, 1.5e-09, 8.9e-10`) and the lstm values (`2.0e-09, 7.1e-08, 6.8e-09`) overlap in range and the seeds disagree on which is bigger; with three seeds the gap is inside the spread. **c.** Bias 0 at `T = 80` is `3.92e-17` and bias 2 is `3.37e-02`: **15 powers of ten** apart (accept 15 to 16). At bias `4.0` the number does fall from `3.52e-01` to `1.61e-01`: a factor of **about 2**. **d.** `0.881 ** 40` is about `0.006` (`0.0060`; the lesson's `0.8808 ** 40` is `6.238e-03`). The table's `T = 40` entry for bias 2 is `5.77e-02`: **ten times bigger**, not the same, but both are enormously bigger than `1e-09`; the point is that a dial near 1 keeps something where one half keeps nothing. **e.** Model: *"With seed 0, moving the forget bias from 0 to 2 changed the `T = 40` ratio from `9.83e-10` to `5.77e-02`, far more than the spread between seeds; I did not train anything, so this is about the starting point, not learning."* **Also accept** "the dial opens the highway at the start". *Common errors:* "the LSTM is better than the GRU" from three seeds; "the LSTM learns longer sequences" (nothing was trained).

### Page 11.6

Model: *"With seed 0 and T = 40, the pull of the first word as a fraction of the last word was 2.05e-09 for an LSTM at default settings and 5.77e-02 for an LSTM with the forget bias set to 2. An LSTM adds to its memory, so the slope back through it is the forget gate. At the start of training the gate's score is near zero, so the dial is near one half, and at default settings the gates alone did not open the highway; setting the bias to 2 makes the dial 0.88. I measured an untrained layer on random numbers, so this does not show that the LSTM learns long memories."*

| Criterion | Marks |
|---|:--:|
| Two numbers **with exponents**, from their own run, seed stated, one default and one with the forget bias | 2 |
| Cause in one sentence (the memory is updated by adding; the slope is the forget gate) | 1 |
| At default settings the gates alone did not help, or the dial starts near one half | 1 |
| States what was **not** shown: nothing was trained | 2 |

### Page 11.6b and Self-Check

**Entry 1.** It stops with an error (no output). The last line is `ValueError: LSTMCell: Expected hx[0] to be 1D or 2D, got 0D instead`. `hx[0]` is the first thing in the state: it was handed the single tensor `h`, so the first piece was one number (0-D), but the cell expected a row of 16 (1-D) with a memory next to it. Fix: `h, c = cell(x40[0], (h, c))`, starting from `(torch.zeros(H), torch.zeros(H))`.

**Entry 2.** The last line is `RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.` The one line of difference: `with torch.no_grad():` around the `fill_`. "Editing, not learning" means we write a number into a knob by hand, and PyTorch must not record that as a step it will differentiate through.

**Entry 3.** Real output:

```text
T = 40, first word / last word, seed 0:
  wrong group [0:H]    1.2e-07
  right group [H:2H]   5.8e-02
  no dial at all       2.0e-09
```

The wrong group is about **five** powers of ten short (`5.8e-02` against `1.2e-07`: a factor of about half a million), yet it is a *little better* than no dial (`2.0e-09`), so it looks like "it did something". **The tell:** no error and a number that moved in the hoped direction; the only protection is to compare against the right group and the no-dial row before believing a change. **Fix:** `[H:2 * H]` for the forget group (the order is input, forget, candidate, output, as in block 3's slices).

**Entry 4.** Your own; a good one names the layer and the exponent, and says what you assumed (usually "the gru would stay level").

**Self-Check:** if you could tick fewer than four, redo pages 11.1 and 11.2 first.
