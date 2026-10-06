# Workbook — Week 18: Review and Assessment 2 (The Second X-Ray)

**Name:** ________________________________  **Date:** ______________

[⬅ Week 17](week-17.md) · [📖 Read the chapter first](../student-guide/week-18.md) · [Course Home](../README.md) · [Next ➡](week-19.md)

---

![The 36 week tiles in four term lanes; weeks 1 to 17 solid, week 18 tinted pink with a thick border and a pointer above it, weeks 19 to 36 dashed](../figures/fig-w18-0-where-this-fits.svg)
*Figure 18.0 — Week 18 of 36, the Term 2 review and paper, sits at the end of term 2; weeks 1 to 17 are done and weeks 19 to 36 are still ahead.*

> **Rules for this workbook.** This week has **one real paper** (the 75-mark Term 2 checkpoint your teacher hands you in class) and **this workbook is everything around it**: the night-before map, practice on **numbers that are not on the paper**, the marking pages, and the Bug Log. **Nothing in here is the paper, and nothing in here is a teacher file.**
>
> **Pen first, then run.** Pages 18.2 to 18.6 are by hand with a calculator. You write your answer *before* you open the check file. The digits in the worked examples and the answers came from real CPU runs (PyTorch, one thread, `torch.manual_seed(0)` wherever anything is random). By-hand numbers are plain arithmetic and will match exactly. The table on page 18.7 is real printed output of `check187.py`, which trains a small model for about five seconds; on another CPU or PyTorch build the **last digit** of a loss can move, but not the shape of the story.
>
> **Nothing new today.** No new idea, no new syntax, no new word. If a page uses something you do not recognise, that is a **finding**, not a failure: write the week you think it came from in the margin.
>
> **There is no language model and no stand-in anywhere in this workbook.** Everything is plain PyTorch on the CPU, or arithmetic. The three-word "sentences" on page 18.4 are invented numbers chosen so the arithmetic is easy. They are not learned.
>
> Run any check file from the folder that contains `l4lib/` (only page 18.7 needs it). Carry **four decimals** in every calculation and round only the answer. Use a calculator with `e^x` and a power key (a phone is fine, in airplane mode).

---

## ✅ Warm-Up (5 min, before anything else)

Five questions, one per *kind* of thing the paper will ask. No notes.

**W1.** A slope of `0.5` is multiplied in three times in a row. What is left? ____________

**W2.** A model that knows nothing about **20** symbols gives each one `1/20`. Its first loss should be `ln 20` = ____________ (three decimals).

**W3.** Four scores are all `0`. The softmax gives each a chance of ____________ .

**W4.** To hide the future, the mask is applied **before / after** (circle one) the softmax, with the number **0 / -inf** (circle one).

**W5.** Which of the eight weeks do you trust least right now? (Circle a week: **10 · 11 · 12 · 13 · 14 · 15 · 16 · 17**) ____________ Write why, in a few words: _____________________________________________

---

## 🗺️ Page 18.1 — The Confidence Map (the night before; 10 minutes, do not study)

For each line ask: **could I do this right now with only a pen and a calculator?** Tick **Yes**, **Maybe** or **No**. Be honest; nobody sees this page but you. Then, for each **No**, do the page in the last column for **20 minutes at most**, and then stop. Do not try to learn everything in one night.

| Week | I can... | Yes | Maybe | No | Page to redo |
|:--:|---|:--:|:--:|:--:|---|
| 10 | Multiply a slope through a loop and say roughly what is left. Say which disease **clipping** can cure. | ☐ | ☐ | ☐ | 10.1, 10.4 · today's **18.2** |
| 11 | Say what the slope back through the memory track is. Make a dial from a bias. Say why an LSTM does **not** fix fading by itself. | ☐ | ☐ | ☐ | 11.1, 11.5 · today's **18.2** |
| 12 | Say what teacher forcing is. Build the shifted input with `torch.cat`. Say when a validation loss is worse than knowing nothing. | ☐ | ☐ | ☐ | 12.4, 12.5 · today's **18.7**, **18.8** |
| 13 | Turn scores into chances at a temperature. Keep the top k, or the top-p set. Say what greedy and exposure bias mean. | ☐ | ☐ | ☐ | 13.2, 13.3 · today's **18.3**, **18.8** |
| 14 | Do the three-word attention pass with a pen. Say which of `Wq`, `Wk`, `Wv` does not change the weights. | ☐ | ☐ | ☐ | 14.1, 14.4 · today's **18.4** |
| 15 | Say why the scores are divided by `sqrt(d)`. Build a causal mask. Say what shape a width cut into heads has. | ☐ | ☐ | ☐ | 15.2, 15.3 · today's **18.4**, **18.5** |
| 16 | Say why attention alone cannot tell `dog bit man` from `man bit dog`. Count the knobs in one block. | ☐ | ☐ | ☐ | 16.2, 16.4 · today's **18.6** |
| 17 | Say what a model that knows nothing should score at step 0. Say what the gap between train and validation does and does not tell you. | ☐ | ☐ | ☐ | 17.3, 17.4, 17.6 · today's **18.7** |

**Count your Noes:** ______ . **Rule:** if you have more than three, still do only the **two** you ticked No for that you think are worst, and **stop at 20 minutes each**. A tired head does arithmetic worse than a rested one.

*After the paper*, come back to this page and write, beside each week, whether your **guess** about yourself was right. That comparison is worth more than the mark.

My guess about myself, before: Weeks I thought were soft: ____________ . After the paper, the weeks that were actually soft: ____________ .

---

## 🔁 Page 18.2 — Compounding and the Forget Dial (Weeks 10 and 11 · 15 min)

**Compounding** means multiplying the same number in again and again. `0.9` forty times is **not** `0.9 × 40`.

**Worked example (done for you): a slope of `0.7`, five steps back.** Start with `1`. Multiply by `0.7` each step: `0.7`, `0.49`, `0.343`, `0.2401`, `0.16807`. About **`0.1681`** is left.

Fill in the rest of this slope of `0.85`, so you see the shape before you use the power key. **Four decimals.**

| Step | Before | Times 0.85 | After |
|:--:|:--:|:--:|:--:|
| 1 | 1.0000 | 0.85 | 0.8500 |
| 2 | 0.8500 | | |
| 3 | | | |
| 4 | | | |

**18.2a.** Use the power key: `0.85` for **20** steps back is ____________ . Is that fading or blowing up? ____________

**18.2b.** `1.15` for **20** steps back is ____________ (two decimals). Fading or blowing up? ____________

**18.2c.** Each number is only `0.15` away from 1, yet the two answers are far apart. In one sentence, why is `0.85 × 20 = 17` the wrong way to think about it? ___________________________________________

**18.2d.** A slope of `0.85` first falls **below `0.1`** after how many steps? Guess: ______ . (Try your calculator: multiply by `0.85` again and again, counting.) Found: ______ .

**Clipping.** `clip_grad_norm_` rescales a gradient whose **length** is bigger than a limit, and it **returns the length it had before**. Limit `1`.

**18.2e.** A gradient is `[24, 32]`. Its length is `sqrt(24² + 32²)` = ____________ . After clipping to `1` it becomes `[ ____ , ____ ]` (each number divided by the length). The call returns ____________ .

**18.2f.** A different gradient has length `0.0000004`. After clipping to `1` its length is ____________ . So clipping can cure **fading / blowing up / both** (circle one). Why? ___________________________________________

**The forget dial.** The dial is `1 / (1 + e^-bias)`. The slope back through the memory track is the dial at every step.

**Worked example (done for you): bias `0.5`.** `e^-0.5 = 0.6065`, so the dial is `1 / 1.6065 =` **`0.6225`**. Over **six** steps: `0.6225 ^ 6 =` **`0.0582`**.

| Bias | Dial | Dial ^ 6 (six steps back) |
|:--:|:--:|:--:|
| 0.5 | 0.6225 | 0.0582 |
| -1 | | |
| 0 | | |
| 1.5 | | |
| 2.5 | | |

**18.2g.** How many times more signal survives six steps with bias `1.5` than with bias `0`? ____________ (divide the two last-column numbers)

**18.2h.** A new LSTM has its forget bias at the default, `0`. Does it already have a good memory? ____________ Which bias from the table would you choose if you wanted the signal to survive? ____________

**Check file** (run it only after your tables are written):

```python
# check182.py - Week 18 workbook page 18.2: compounding, the forget dial, and clipping. PRACTICE numbers.
import math
import torch

print("0.7 ** 5    :", round(0.7 ** 5, 4))
print("0.85 ** 20  :", round(0.85 ** 20, 4))
print("1.15 ** 20  :", round(1.15 ** 20, 2))

steps = 0
left = 1.0
while left >= 0.1:
    left = left * 0.85
    steps = steps + 1
print("0.85 first drops below 0.1 after", steps, "steps (left:", round(left, 4), ")")


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


print("bias   dial    dial ** 6")
for bias in [0.5, -1, 0, 1.5, 2.5]:
    f = sigmoid(bias)
    print(f"{bias:4}   {f:.4f}  {f ** 6:.5f}")
print("bias 1.5 against bias 0, six steps:", round(sigmoid(1.5) ** 6 / 0.5 ** 6, 1), "times more survives")

c = torch.tensor([24.0, 32.0])                            # the gradient of (p * c).sum() is c itself
for label, scale in [("big gradient", 1.0), ("tiny gradient", 1e-8)]:
    p = torch.nn.Parameter(torch.zeros(2))
    (p * (c * scale)).sum().backward()
    before = torch.nn.utils.clip_grad_norm_([p], max_norm=1.0)
    print(label, "| returned (length before):", f"{float(before):.1e}", "| length after:", f"{float(p.grad.norm()):.1e}")
```

Write what it printed for `0.85 ** 20`: ____________ For the first step count below 0.1: ____________ For the clipped `[24, 32]` length after: ____________

![Left, two bars on a log scale: 0.95 compounded 30 times leaves 0.2146 (below the unchanged line), 1.10 leaves 17.45 (above it). Right, three bars for a forget dial: 0.00391, 0.08159 and 0.67794 left after 8 steps.](../figures/fig-w18-1-compounding-and-dials.svg)
*Figure 18.1 — Practice numbers, not the paper's: a slope near 1 fades or blows up when compounded, and a bigger forget bias keeps more signal.*

---

## 🎲 Page 18.3 — Scores to Chances, and Who Gets Kept (Week 13 · 15 min)

**Worked example (done for you): scores `[3, 0, 0]`, temperature 1.** `e^3 = 20.086`, `e^0 = 1`, `e^0 = 1`. Total `22.086`. Chances: `20.086 / 22.086 =` **`0.9094`**, `1 / 22.086 =` **`0.0453`**, **`0.0453`**. They add to 1.

Now five scores: **`[2.0, 1.5, 0.5, 0.0, -1.0]`**. Call the letters 0 to 4, left to right.

**18.3a. Temperature 1.** Fill in the exponentials, their total, and the chances.

| Letter | 0 | 1 | 2 | 3 | 4 | Total |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
| score | 2.0 | 1.5 | 0.5 | 0.0 | -1.0 | |
| `e^score` | | | | | | |
| chance | | | | | | 1.0000 |

**18.3b. Temperature 0.5.** First divide every score by `0.5`: the scores become `[ ___ , ___ , ___ , ___ , ___ ]`. The chance of letter 0 is now ____________ (it needs its own exponentials and total).

**18.3c. Temperature 2.** The chance of letter 0 is ____________ . Put the three chances of letter 0 (T = 0.5, 1, 2) in order from biggest to smallest: ____________ A **low** temperature makes the top letter **more / less** sure (circle one).

**18.3d. Greedy.** Greedy always picks letter ____________ . At which of the three temperatures does sampling look most like greedy? ____________

**18.3e. Top-k, with k = 2.** Which letters are kept? ____________ Their chances were ____________ and ____________ . Now the kept letters' chances must add to 1 again: divide each by their sum. The new chances are ____________ and ____________ .

**18.3f. Top-p.** Put the letters in order of chance (here they are already in order), and write the **running total**:

| After letter | 0 | 1 | 2 | 3 | 4 |
|:--|:--:|:--:|:--:|:--:|:--:|
| running total | | | | | |

How many letters does top-p keep for **p = 0.6**? ______ For **p = 0.8**? ______ For **p = 0.95**? ______ (The rule: count how many running totals are **below** p, then add one. Say in a few words why the `+ 1`: ___________________________________________)

**18.3g.** In a sentence, say what exposure bias is, with the words *trained* and *own guesses*: ___________________________________________

**Check file:**

```python
# check183.py - Week 18 workbook page 18.3: scores to chances, top-k and top-p. PRACTICE numbers.
import torch
import torch.nn.functional as F

scores = torch.tensor([2.0, 1.5, 0.5, 0.0, -1.0])
print("worked example [3, 0, 0]:", [round(x, 4) for x in F.softmax(torch.tensor([3.0, 0.0, 0.0]), dim=-1).tolist()])
for temp in [1.0, 0.5, 2.0]:
    p = F.softmax(scores / temp, dim=-1)
    print("temperature", temp, "->", [round(x, 4) for x in p.tolist()])

p = F.softmax(scores, dim=-1)
vals, idx = torch.topk(p, 2)
print("top-k 2 keeps letters", idx.tolist(), "chances", [round(x, 4) for x in F.softmax(scores[idx] , dim=-1).tolist()])
sorted_p, ids = torch.sort(p, descending=True)
running = torch.cumsum(sorted_p, dim=-1)
print("running total:", [round(x, 4) for x in running.tolist()])
for top in [0.6, 0.8, 0.95]:
    print("top-p", top, "keeps", int((running < top).sum().item()) + 1, "letters")
```

Did your 18.3a chances match? ____________ Which of 18.3f's answers surprised you? ____________

---

## 🔍 Page 18.4 — The Attention Pass, Then Both Dials (Weeks 14 and 15 · 25 min)

This is the page to do again if the grid shows Week 14, 15 or 16 soft. **Same method as Weeks 14 and 15, different numbers from the paper and from the warm-ups in the chapter.** Three words with invented 2-number vectors:

```text
   sun = [1, 1]      Wq = identity     Wk = identity     Wv = [[1, 0],
   hot = [0, 2]                                                 [1, 1]]
   day = [2, 1]
```

Because `Wq` and `Wk` are the identity, `Q = K = X`. A row of `X` times `Wv` is: first number of the row times the first row of `Wv`, plus the second number times the second row of `Wv`.

**Worked example (done for you): the first value row.** `sun = [1, 1]`. `1 × [1, 0] + 1 × [1, 1] = [2, 1]`. So the first row of `V` is **`[2, 1]`**.

**18.4a.** Write all of `V`. Row 2 (`hot`): `[ ___ , ___ ]`. Row 3 (`day`): `[ ___ , ___ ]`.

**18.4b. The table of scores** (each word's row dotted with each word's row). The diagonal is each word dotted with itself. Fill it in:

| | sun | hot | day |
|:--|:--:|:--:|:--:|
| sun | 2 | | |
| hot | | | |
| day | | | |

**Part 1. No dials. Work out the answer for `hot` (row 2) only.**

**18.4c.** Exponentials of row 2: `[ ____ , ____ , ____ ]`, total ____________ . Weights (four decimals): `[ ____ , ____ , ____ ]`. Do they add to 1? ____________

**18.4d.** The blended output for `hot`: weights times `V`. `[ ____ , ____ ]`

**Part 2. Both dials on, for every row.** Dial 1: divide every score by `sqrt(2)` (`d = 2`). Dial 2: hide the future, **before** the softmax (a word may look only at itself and earlier words).

**18.4e.** Row 1 (`sun`) can see only itself. Its weights are `[ ___ , ___ , ___ ]`. Its output is just `V`'s first row: `[ ___ , ___ ]`.

**18.4f.** Row 2 (`hot`) can see `sun` and itself. Scores `[2, 4]` divided by `sqrt(2)` are `[ ______ , ______ ]`. Exponentials `[ ______ , ______ ]`, total ______ . Weights `[ ______ , ______ , ______ ]`. Output `[ ______ , ______ ]`.

**18.4g.** Row 3 (`day`) can see all three. Scores `[3, 2, 5]` divided by `sqrt(2)`: `[ ______ , ______ , ______ ]`. Exponentials `[ ______ , ______ , ______ ]`, total ______ . Weights `[ ______ , ______ , ______ ]`.

**18.4h.** Did the mask change anything in row 3? ____________ Why or why not? ___________________________________________

**18.4i.** Row 3 **without** the divide would have weights `[0.1142, 0.0420, 0.8438]`. With the divide they are the ones you wrote in 18.4g. Did the biggest weight go up or down? ____________ Is the softmax now **harder** or **softer**? ____________

**18.4j.** Which of `Wq`, `Wk`, `Wv` could you change without changing any of the weights? ____________ What would it change instead? ___________________________________________

**Check file:**

```python
# check184.py - Week 18 workbook page 18.4: the attention pass, with and without the two dials. PRACTICE numbers.
# sun = [1, 1], hot = [0, 2], day = [2, 1]. Wq and Wk are the identity. Wv = [[1, 0], [1, 1]].
import math
import torch
import torch.nn.functional as F

X = torch.tensor([[1.0, 1.0], [0.0, 2.0], [2.0, 1.0]])
Wv = torch.tensor([[1.0, 0.0], [1.0, 1.0]])
V = X @ Wv
scores = X @ X.transpose(-2, -1)
print("V      :", V.tolist())
print("scores :", scores.tolist())

weights = F.softmax(scores, dim=-1)
print("plain weights, row 2:", [round(x, 4) for x in weights[1].tolist()])
print("plain output, row 2 :", [round(x, 3) for x in (weights @ V)[1].tolist()])

scaled = scores / math.sqrt(2)                                     # dial 1: divide by sqrt(d), d = 2
future = torch.tril(torch.ones(3, 3)) == 0
hidden = scaled.masked_fill(future, float("-inf"))                 # dial 2: hide the future BEFORE the softmax
both = F.softmax(hidden, dim=-1)
print("scaled scores, row 2:", [round(x, 3) for x in scaled[1].tolist()])
print("both dials, weights :", [[round(x, 4) for x in row] for row in both.tolist()])
print("both dials, sums    :", [round(x, 4) for x in both.sum(dim=-1).tolist()])
print("both dials, output  :", [[round(x, 3) for x in row] for row in (both @ V).tolist()])
print("row 3, exponentials of the scaled scores:", [round(math.exp(x), 3) for x in scaled[2].tolist()])

without_divide = F.softmax(scores[2], dim=-1)                      # row 3 with the divide switched off
print("row 3 weights with the divide  :", [round(x, 4) for x in both[2].tolist()])
print("row 3 weights without the divide:", [round(x, 4) for x in without_divide.tolist()])
```

Where did your hand numbers first disagree with the file (write the question number, or "none")? ____________

![Left, a 3 by 3 grid of attention weights for cat, sat, down with the hidden future struck through and each row summing to 1.0. Right, the down row blending three value rows with weights 0.2483, 0.5035, 0.2483 into the output 3.007, 1.0.](../figures/fig-w18-2-practice-attention-pass.svg)
*Figure 18.2 — Practice numbers, not the paper's: scores become weights that sum to 1, hide the future, and blend the value rows.*

---

## 📐 Page 18.5 — Heads and the Mask (Week 15 · 10 min, predict first)

**18.5a. Shapes.** A tensor `x` has shape `(3, 6, 12)`: 3 examples, 6 places, 12 numbers per place. We cut the 12 into **3 heads**.

- Each head gets ______ numbers.
- `x.view(3, 6, 3, 4)` has shape ____________ .
- After `.transpose(1, 2)` the shape is ____________ .
- In words: the shape is `(batch, ______ , ______ , ______ )`.

**18.5b. Build a mask by hand.** For 4 places, draw the grid that `torch.tril(torch.ones(4, 4))` makes (1 = may look, 0 = hidden).

```text
   place 1:   [ ___  ___  ___  ___ ]
   place 2:   [ ___  ___  ___  ___ ]
   place 3:   [ ___  ___  ___  ___ ]
   place 4:   [ ___  ___  ___  ___ ]
```

How many places are hidden? ______ How many can be seen? ______

**18.5c. Mask before the softmax.** Suppose every score is `0`. Hide the future with `-inf` **before** the softmax. The weights in the **third** row are `[ ______ , ______ , ______ , ______ ]`. The row sums of all four rows are `[ ___ , ___ , ___ , ___ ]`.

**18.5d. Mask after the softmax (a deliberate mistake).** Same scores, but softmax first and then zero the hidden places. Before the zeroing every place has a weight of ______ . After zeroing, the four row sums are `[ ______ , ______ , ______ , ______ ]`. Which check would have caught this? ___________________________________________

**18.5e.** In one sentence, why does `-inf` give the hidden places **exactly** zero? (Think of `e` to a hugely negative power.) ___________________________________________

**Check file:**

```python
# check185.py - Week 18 workbook page 18.5: heads and the mask. PRACTICE numbers.
import torch
import torch.nn.functional as F

x = torch.zeros(3, 6, 12)
split = x.view(3, 6, 3, 4)
print("split  :", tuple(split.shape))
print("swapped:", tuple(split.transpose(1, 2).shape))

mask = torch.tril(torch.ones(4, 4))
print(mask)
print("places to hide:", int((mask == 0).sum().item()), "| places that can be seen:", int(mask.sum().item()))

flat = torch.zeros(4, 4)
right = F.softmax(flat.masked_fill(mask == 0, float("-inf")), dim=-1)
wrong = F.softmax(flat, dim=-1).masked_fill(mask == 0, 0.0)
print("hide BEFORE the softmax, row sums:", [round(x, 4) for x in right.sum(dim=-1).tolist()])
print("zero AFTER the softmax,  row sums:", [round(x, 4) for x in wrong.sum(dim=-1).tolist()])
print("row 3, hidden before:", [round(x, 4) for x in right[2].tolist()])
```

---

## 🔢 Page 18.6 — Count the Block (Week 16 · 15 min)

One block at width **`d = 14`**. Its pieces (as in class): two `LayerNorm(14)` (each has 14 scales and 14 shifts); `q`, `k`, `v`, each `Linear(14, 14, bias=False)`; `proj = Linear(14, 14)` **with** a bias; `up = Linear(14, 56)` and `down = Linear(56, 14)`, both with biases. The causal mask is a buffer and is **not** counted.

**Worked example (done for you): one `Linear` with a bias.** `Linear(14, 14)` has `14 × 14 = 196` weights and `14` biases: **210**. That is `proj`.

**18.6a.** The two layer norms: ____________
**18.6b.** `q`, `k`, `v` (no biases): ____________
**18.6c.** `proj`: **210** (worked). Attention total (`q, k, v` and `proj`): ____________
**18.6d.** `up`: `14 × 56 + 56 =` ____________ . `down`: `56 × 14 + 14 =` ____________ . MLP total: ____________
**18.6e.** The whole block: ____________ . Check with `12d² + 10d`: ____________
**18.6f.** Three blocks are kept in an `nn.ModuleList`. Together they have ____________ knobs. If they were kept in a **plain list**, `model.parameters()` would count ____________ of them, and no error would be raised. Why? ___________________________________________

**18.6g. Not just a formula.** The hidden width of the MLP is changed from `4d` to **`2d`** (so `up = Linear(14, 28)`, `down = Linear(28, 14)`). The MLP now has ____________ knobs, and the block ____________ . (Does `12d² + 10d` still apply? ____________ )

**18.6h.** Attention on its own cannot tell `dog bit man` from `man bit dog`. Say why in one sentence, then say what is added to fix it. ___________________________________________

**Check file:**

```python
# check186.py - Week 18 workbook page 18.6: count one block at d = 14, by piece.
import torch.nn as nn

d = 14
pieces = {
    "two layer norms": [nn.LayerNorm(d), nn.LayerNorm(d)],
    "q, k, v (no bias)": [nn.Linear(d, d, bias=False) for _ in range(3)],
    "proj": [nn.Linear(d, d)],
    "up": [nn.Linear(d, 4 * d)],
    "down": [nn.Linear(4 * d, d)],
}
total = 0
for name, layers in pieces.items():
    n = sum(p.numel() for layer in layers for p in layer.parameters())
    total += n
    print(f"{name:20s} {n}")
print("block at d = 14:", total, " formula 12d^2 + 10d:", 12 * d * d + 10 * d)
print("three blocks:", 3 * total)
d = 14
mlp_narrow = (d * 2 * d + 2 * d) + (2 * d * d + d)                 # the hidden width is 2d instead of 4d
print("mlp with hidden width 2d:", mlp_narrow, " block:", 56 + 588 + 210 + mlp_narrow)
d = 24
print("formula at d = 24:", 12 * d * d + 10 * d)
```

---

## 📉 Page 18.7 — Read a Real Table, and Say What You Would Check Next (Weeks 12 and 17 · 20 min)

**Real numbers.** `check187.py` trains a small letter model on the **same 6,972-character text** as your TinyGPT, with the **same split** (the last tenth held back). It is not a transformer: it sees only the **4 letters before** the one it must guess, and has 15,868 knobs. **Loss** is the average surprise (`-ln` of the chance given to the true next letter); a model that knows nothing about 28 characters scores `ln 28 = 3.332`.

```text
step   train     val
   0  3.368  3.371
  50  1.690  1.763
 100  1.210  1.444
 200  0.738  1.357
 400  0.507  1.767
 600  0.489  2.056
 800  0.484  2.218
1000  0.483  2.332

Three models that only count, scored on the same validation letters:
   knows nothing (uniform)    3.332
   knows letter frequencies   2.854
   knows the previous letter  2.031
```

**Worked example (done for you): the habit.** *"At step 0 the model is as bad on the unseen text as on the seen text: train 3.368 and val 3.371, both near 3.332."* A table, a step, and **numbers from the table**.

**18.7a.** At which printed step is the validation loss lowest, and what is it? ____________

**18.7b.** The gap (val minus train) at step 0: ____________ . At step 200: ____________ . At step 1000: ____________ . Which direction is it moving? ____________

**18.7c.** At step 0 the gap is nearly zero even though the model is bad. In a sentence, why? ___________________________________________

**18.7d.** The first-loss check: the step-0 train loss is `3.368`. How far from `ln 28 = 3.332` is it? ____________ Does it pass (within about 0.1)? ____________

**18.7e.** How much does the step-200 validation loss beat the "previous letter" counter? ____________ What about the step-1000 validation loss: better or worse than that counter, and by how much? ____________

**18.7f.** A classmate says: *"Train loss 0.483 means it is 95% right."* Write a reply of two sentences. Hint: what *is* a loss, and what does `0.483` measure? ___________________________________________

**18.7g.** Write a reply of three or four sentences to: *"The training loss is still falling, so the model is still getting better."* It must (1) quote two numbers from the table, (2) say which loss is the fairer one for text the model has not seen, (3) say what you would do to stop at a better point (a Week 5 idea), and (4) name one check that **one run cannot answer**.

___________________________________________________________________________

___________________________________________________________________________

___________________________________________________________________________

**18.7h.** This table has one seed and 694 validation letters. Name two things it **cannot** tell you: ___________________________________________

**Check file** (it needs `l4lib/`, so run it from the folder that contains it; about five seconds):

```python
# check187.py - Week 18 workbook page 18.7: a small letter model with a 4-letter memory, and three counters, on Week 17's text.
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from l4lib.corpus import TEXT

torch.set_num_threads(1)
torch.manual_seed(0)

chars = sorted(set(TEXT))
stoi = {c: i for i, c in enumerate(chars)}
ids = torch.tensor([stoi[c] for c in TEXT])
V = len(chars)
n = int(0.9 * len(ids))                                   # the last tenth is held back
K = 4                                                     # the model sees the 4 letters before


def windows(part):
    X = torch.stack([part[i:i + K] for i in range(len(part) - K)])
    return X, part[K:]


Xtr, ytr = windows(ids[:n])
Xva, yva = windows(ids[n:])

emb = nn.Embedding(V, 8)
lin1 = nn.Linear(K * 8, 256)
lin2 = nn.Linear(256, V)
params = list(emb.parameters()) + list(lin1.parameters()) + list(lin2.parameters())


def model(X):
    h = emb(X).view(X.shape[0], -1)                       # 4 letters, 8 numbers each, side by side: 32 numbers
    return lin2(F.relu(lin1(h)))


opt = torch.optim.Adam(params, lr=3e-3)
print("knobs:", sum(p.numel() for p in params), " windows:", len(Xtr), "train,", len(Xva), "val")
print("step   train     val")
for step in range(1001):
    if step in (0, 50, 100, 200, 400, 600, 800, 1000):
        with torch.no_grad():
            tr = F.cross_entropy(model(Xtr), ytr).item()
            va = F.cross_entropy(model(Xva), yva).item()
        print(f"{step:4d}  {tr:.3f}  {va:.3f}")
    loss = F.cross_entropy(model(Xtr), ytr)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()

# three models that only count, scored on the SAME validation windows
train_ids = ids[:n].tolist()
last_val = Xva[:, -1].tolist()                            # the letter just before each target
targets = yva.tolist()
freq = [1.0] * V
for c in train_ids:
    freq[c] += 1
pair = [[1.0] * V for _ in range(V)]
for a, b in zip(train_ids[:-1], train_ids[1:]):
    pair[a][b] += 1
print("knows nothing (uniform)    :", round(math.log(V), 3))
print("knows letter frequencies   :", round(sum(-math.log(freq[t] / sum(freq)) for t in targets) / len(targets), 3))
print("knows the previous letter  :", round(sum(-math.log(pair[a][t] / sum(pair[a])) for a, t in zip(last_val, targets)) / len(targets), 3))
```

Did your run print the same step-200 and step-1000 validation numbers? ____________ (If the last digit differs, the shape is what matters.)

---

## 🐞 Page 18.8 — Break It on Purpose (four bugs from Weeks 10, 12, 13, 14-15 · 25 min)

The paper's Section C has four "find the bug" questions. **This page has four different ones**, so you can practise the *method* without seeing the paper. **Each program is deliberately broken.** Do **not** run it first. For each: write **(i)** what the bug is, **(ii)** what you think happens when it runs, **(iii)** the fixed line. *Then* run it.

**The reading method (use it every time):** if it prints an error, read the **last line**, find **your own file's** line just above it, and ask what you expected that line to do. If it prints **no** error, ask what should be *true* of the output and check it: do the rows add to 1? Do the chances add to 1? Is the number the size you worked out by hand?

**Bug 18.8-A. (Weeks 14-15, SILENT)** The programmer wants each **row** of weights to add to 1. The code prints two lines; predict both.

```python
# DELIBERATE BUG 18.8-A (SILENT): the softmax is taken down the columns, not along each row.
import torch
import torch.nn.functional as F
scores = torch.tensor([[2.0, 0.0, 1.0],
                       [0.0, 1.0, 3.0],
                       [1.0, 1.0, 0.0]])
weights = F.softmax(scores, dim=0)
print([[round(x, 3) for x in row] for row in weights.tolist()])
print([round(x, 3) for x in weights.sum(dim=-1).tolist()])
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 18.8-B. (Week 13, SILENT)** A temperature of `0.5` should make letter 0 (score 2) more likely, roughly 0.86 of the time. The code prints two lines.

```python
# DELIBERATE BUG 18.8-B (SILENT): the temperature is applied AFTER the softmax.
import torch
import torch.nn.functional as F
torch.manual_seed(0)
scores = torch.tensor([2.0, 1.0, 0.0])
temperature = 0.5
probs = F.softmax(scores, dim=-1) / temperature
print([round(x, 3) for x in probs.tolist()], round(probs.sum().item(), 3))
picks = torch.multinomial(probs, 1000, replacement=True)
print("share of picks that were letter 0:", (picks == 0).float().mean().item())
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 18.8-C. (Week 12, loud)** The start token `27` should slide in at the front of each of the two names.

```python
# DELIBERATE BUG 18.8-C (loud): the start token is 1-D but the names are 2-D.
import torch
names = torch.tensor([[4, 9, 1], [7, 2, 5]])
start = torch.full((2,), 27)
shifted = torch.cat([start, names[:, :-1]], dim=1)
print(shifted)
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 18.8-D. (Week 10, SILENT)** The programmer wants `0.9` compounded ten times, which should be about `0.349`.

```python
# DELIBERATE BUG 18.8-D (SILENT): the slope is reset to 1.0 on every pass of the loop.
dial = 0.9
for _ in range(10):
    slope = 1.0
    slope = slope * dial
print(slope)
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Which bug ran without any error?** ____________ **Which one told you where it was broken?** ____________

---

## 📝 Page 18.9 — Mark Your Own Paper (the same evening, a different colour of pen)

**After the paper.** Your teacher gives you the **marking sheet** (short answers only). Use a pen of a **different colour** from the one you used on the paper. In A, B and C be strict. In D and E mark the **working**, not just the final number.

**The per-week grid.** The "Questions" column tells you which questions belong to which week. Marks available and the "redo if" line are fixed; fill in the rest.

| Week | Topic | Questions | Marks available | Marks earned | % | Redo if marks ≤ | Circle? |
|:--:|---|---|:--:|:--:|:--:|:--:|:--:|
| 10 | Compounding; vanishing and exploding; clipping | A1-A3, B1, C3, D2(b, c) | **11** | | | 6 | |
| 11 | Gates; the forget dial | A4-A7, D2(a, d) | **6** | | | 3 | |
| 12 | Teacher forcing; padding; train against validation; novelty | A8-A10, B7, B8, E(a) | **11** | | | 6 | |
| 13 | Greedy, temperature, top-k, top-p; exposure bias | A11-A14, B2-B4, C2 | **13** | | | 7 | |
| 14 | Attention by hand; weighted average | A15, A16, D1 | **7** | | | 4 | |
| 15 | Divide by `sqrt(d)`; the mask; heads | A17, A18, B5, B6, C1 | **9** | | | 5 | |
| 16 | Positions; the block; counting knobs | A19, C4, D3 | **9** | | | 5 | |
| 17 | TinyGPT; the first-loss check; the gap | A20, E(b), E(c) | **9** | | | 5 | |
| | **Total** | | **75** | | | | |

*(Marks earned ÷ marks available × 100 = %. A week needs a redo if you scored **60% or less** of its marks, which is the "redo if" column.)*

**Circle at most two weeks.** Choose the **lowest percentages**. If there is a tie, go in this order: **Week 16, then Week 15, then Week 17**: Week 19 takes your TinyGPT apart and leans on those three directly.

My two weeks: ______ and ______ . Redo for week ______ on (day and time) ____________________ . Redo for week ______ on ____________________ .

**Where to redo it.** The chapter's remediation table names the pages; the ones from today are:

| If the circled week is... | Today's page to redo as well |
|:--:|---|
| 10 or 11 | 18.2 |
| 13 | 18.3 |
| 14 | 18.4 (then ask your teacher for the second set of numbers) |
| 15 | 18.4 and 18.5 |
| 16 | 18.6 |
| 12 or 17 | 18.7 |

**Why at most two?** A list of eight redos is a list nobody does. Two is a plan.

**Total mark:** ______ / 75 . **Pattern, not number:** one week at 30% and seven at 90% is a very different X-ray from eight weeks at 65%. Mine looks like: ___________________________________________

**Section E, your own words.** Write one sentence about what Section E taught you about reading a table that you did not know before: ___________________________________________

> **If you wrote "ablation" or "scaling law" anywhere on the paper**, that is not wrong and not extra: it is from next term, and it is a good sign you have read ahead. Your teacher will say so on the sheet.

---

## 📓 Page 18.10 — The Bug Log

The Bug Log is the most useful page of the course. Today's entries come from the paper and from page 18.8.

**Entry 1: the answer I was most surprised to get wrong.**
*"The answer I was most surprised to get wrong was ______________, because I thought ____________________________."*

_______________________________________________________________________________

**Entry 2: a slip, not a gap.** Find one mark you lost that you **knew** how to get (a rounding slip, a missed `+ 1`, a swapped row and column). What was it, and what is the **one habit** that would have saved it?

Mark lost: ____________________ Habit: _______________________________________

**Entry 3: a bug from page 18.8 that I mispredicted.** (Skip if you got all four.)

| What I predicted | What actually happened | The sentence that would have told me |
|---|---|---|
| | | |

**Entry 4: the silent ones.** Three of the four bugs on page 18.8 ran **without an error**. Write, in your own words, **what you would check to catch each**: ___________________________________________

**Entry 5: the week I will redo first, and the rule I will follow in Term 3.** One sentence: ___________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (do this last, from memory)

Seven things, no scrolling up. Tick only if you could do it **now**.

- ☐ Compound a slope with the power key, and say which disease clipping can and cannot cure.
- ☐ Make a forget dial from a bias, and say why the default LSTM does not fix fading by itself.
- ☐ Turn three scores into chances by hand, and count what top-p keeps (with the `+ 1`).
- ☐ Do the attention pass for one row, and say what the weights add to.
- ☐ Say why the mask goes before the softmax and why it uses `-inf`.
- ☐ Count the knobs in one block at a width you choose, and check with `12d² + 10d`.
- ☐ Say what a model that knows nothing about `V` symbols scores at step 0, and what the train-against-validation gap does and does not tell you.

**Ticks:** ______ / 7 . **The one I could not tick, and when I will redo it:** ___________________________________________

**Next week.** Week 19 opens the TinyGPT you built in Week 17 and deletes its parts one at a time: the mask, the positions, the residual road and the layer norm. It leans on three things from this paper: the mask and the divide (page 18.4 and 18.5), positions and the block (page 18.6), and the first-loss check and the gap (page 18.7). If your grid shows Week 16, 15 or 17 under 60%, **redo those first.**

---

[⬅ Week 17](week-17.md) · [📖 Chapter](../student-guide/week-18.md) · [Course Home](../README.md) · [Next ➡](week-19.md)

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact to the digits shown; where you carried fewer decimals, anything within `0.002` is fine. These answers are for the pages in **this workbook**. They are not the paper's answers, and this page does **not** contain any of them.

### Warm-Up

**W1.** `0.5 × 0.5 × 0.5 =` **0.125**. **W2.** `ln 20 =` **2.996**. **W3.** **0.25** (four equal chances add to 1). **W4.** **Before**, with **-inf**. **W5.** Any honest answer; the aim is to compare it with the grid later.

### Page 18.1

No right answer. The point is the **gap between your guess and the grid**. If you ticked "Yes" for a week and scored 40% on it, that is the most valuable finding of the page: the week is softer than you feel.

### Page 18.2

Slope table: step 2 `0.8500 × 0.85 =` **0.7225**; step 3 **0.6141**; step 4 **0.5220**.

**18.2a.** **0.0388**: about 4% is left. **Fading.** **18.2b.** **16.37**: **blowing up**. **18.2c.** Multiplying `0.85 × 20` adds; compounding multiplies the *result* again, so every step takes 15% off what is *left*, and the rest shrinks faster than any sum would say. A number a little under 1 shrinks the signal; a number a little over 1 grows it; and twenty steps magnify a small gap. **18.2d.** **15** steps (after 14 you are at `0.1028`, after 15 at `0.0874`).

**18.2e.** Length `sqrt(576 + 1024) = sqrt(1600) =` **40**. Clipped: `[24/40, 32/40] =` **`[0.6, 0.8]`** (length 1). The call returns **40** (the length *before*). **18.2f.** Still **0.0000004**: clipping only scales a gradient *down*, and this one is already under the limit. It can cure **blowing up only**: it can turn the volume down, never up.

| Bias | Dial | Dial ^ 6 |
|:--:|:--:|:--:|
| 0.5 | 0.6225 | 0.0582 |
| -1 | 0.2689 | 0.00038 |
| 0 | 0.5000 | 0.0156 |
| 1.5 | 0.8176 | 0.2987 |
| 2.5 | 0.9241 | 0.6229 |

**18.2g.** `0.2987 / 0.015625 =` about **19** times (the file prints 19.1). **18.2h.** **No**: at bias 0 only `0.0156` (about 1.6%) survives six steps, which is why Week 11's LSTM needs the forget bias raised. Bias **2.5** (0.6229) keeps the most of the five.

The check file printed:

```text
0.7 ** 5    : 0.1681
0.85 ** 20  : 0.0388
1.15 ** 20  : 16.37
0.85 first drops below 0.1 after 15 steps (left: 0.0874 )
bias   dial    dial ** 6
 0.5   0.6225  0.05817
  -1   0.2689  0.00038
   0   0.5000  0.01562
 1.5   0.8176  0.29865
 2.5   0.9241  0.62292
bias 1.5 against bias 0, six steps: 19.1 times more survives
big gradient | returned (length before): 4.0e+01 | length after: 1.0e+00
tiny gradient | returned (length before): 4.0e-07 | length after: 4.0e-07
```

### Page 18.3

**18.3a.**

| Letter | 0 | 1 | 2 | 3 | 4 | Total |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
| score | 2.0 | 1.5 | 0.5 | 0.0 | -1.0 | |
| `e^score` | 7.389 | 4.482 | 1.649 | 1.000 | 0.368 | 14.887 |
| chance | 0.4963 | 0.3010 | 0.1107 | 0.0672 | 0.0247 | 1.0000 |

(Adding the rounded exponentials gives `14.888`; the last digit of a chance can move by one. Fine.)

**18.3b.** Scores `[4, 3, 1, 0, -2]`; exponentials `54.598, 20.086, 2.718, 1.000, 0.135`, total `78.537`; letter 0: **0.6952**. **18.3c.** **0.3518**. In order: T = 0.5 (**0.6952**), T = 1 (**0.4963**), T = 2 (**0.3518**). A low temperature makes the top letter **more** sure.
**18.3d.** Letter **0** (the biggest score). The **lowest** temperature, **0.5**.
**18.3e.** Letters **0 and 1**. Chances `0.4963` and `0.3010`, which add to `0.7973`. Divide: `0.4963 / 0.7973 =` **0.6225** and `0.3010 / 0.7973 =` **0.3775**.
**18.3f.** Running totals: **0.4963, 0.7974, 0.9081, 0.9753, 1.0000**. Top-p 0.6 keeps **2**; 0.8 keeps **3**; 0.95 keeps **4**. The `+ 1`: the letter that **crosses** the line is kept too; without it you would keep a set that adds to *less* than p. (At p = 0.8 the second running total, `0.7974`, is just under 0.8, so the third letter is needed. This is the one people miss.)
**18.3g.** During training the model is always handed the **true** letters; when it generates it reads its **own guesses**, which it was never trained on, so one unlikely letter can push it somewhere it has hardly seen.

The check file printed:

```text
worked example [3, 0, 0]: [0.9094, 0.0453, 0.0453]
temperature 1.0 -> [0.4963, 0.301, 0.1107, 0.0672, 0.0247]
temperature 0.5 -> [0.6952, 0.2557, 0.0346, 0.0127, 0.0017]
temperature 2.0 -> [0.3518, 0.274, 0.1662, 0.1294, 0.0785]
top-k 2 keeps letters [0, 1] chances [0.6225, 0.3775]
running total: [0.4963, 0.7974, 0.9081, 0.9753, 1.0]
top-p 0.6 keeps 2 letters
top-p 0.8 keeps 3 letters
top-p 0.95 keeps 4 letters
```

### Page 18.4

**18.4a.** `hot = [0, 2]`: `0 × [1, 0] + 2 × [1, 1] =` **`[2, 2]`**. `day = [2, 1]`: `2 × [1, 0] + 1 × [1, 1] =` **`[3, 1]`**. So `V = [[2, 1], [2, 2], [3, 1]]`.

**18.4b.**

| | sun | hot | day |
|:--|:--:|:--:|:--:|
| sun | 2 | 2 | 3 |
| hot | 2 | 4 | 2 |
| day | 3 | 2 | 5 |

(The table is symmetric because `Q = K`.)

**18.4c.** Row 2 scores `[2, 4, 2]`. Exponentials **`7.389, 54.598, 7.389`**, total **69.376**. Weights **`0.1065, 0.7870, 0.1065`**; they add to 1.
**18.4d.** `0.1065 × [2, 1] + 0.7870 × [2, 2] + 0.1065 × [3, 1] =` **`[2.107, 1.787]`**.

**18.4e.** Weights **`[1, 0, 0]`**; output **`[2, 1]`**.
**18.4f.** Scaled scores `[2, 4] / 1.4142 =` **`[1.414, 2.828]`**. Exponentials **`[4.113, 16.919]`**, total **21.032**. Weights **`[0.1956, 0.8044, 0]`** (the third place is hidden *before* the softmax, so it is exactly 0). Output `0.1956 × [2, 1] + 0.8044 × [2, 2] =` **`[2.000, 1.804]`**.
**18.4g.** Scaled scores **`[2.121, 1.414, 3.536]`**. Exponentials **`[8.342, 4.113, 34.313]`**, total **46.769**. Weights **`[0.1784, 0.0879, 0.7337]`**.
**18.4h.** **No.** The last word has nothing after it, so the mask hides nothing in that row. The mask only changes the rows above. **18.4i.** The biggest weight went **down** (`0.8438` to `0.7337`); the softmax is **softer**. At a bigger width the raw scores would be huge and the softmax would collapse to a hard pick; the divide keeps it soft.
**18.4j.** **`Wv`.** It does not change the weights (they come from `Q` and `K`); it changes **what gets averaged**.

The check file printed:

```text
V      : [[2.0, 1.0], [2.0, 2.0], [3.0, 1.0]]
scores : [[2.0, 2.0, 3.0], [2.0, 4.0, 2.0], [3.0, 2.0, 5.0]]
plain weights, row 2: [0.1065, 0.787, 0.1065]
plain output, row 2 : [2.107, 1.787]
scaled scores, row 2: [1.414, 2.828, 1.414]
both dials, weights : [[1.0, 0.0, 0.0], [0.1956, 0.8044, 0.0], [0.1784, 0.0879, 0.7337]]
both dials, sums    : [1.0, 1.0, 1.0]
both dials, output  : [[2.0, 1.0], [2.0, 1.804], [2.734, 1.088]]
row 3, exponentials of the scaled scores: [8.342, 4.113, 34.313]
row 3 weights with the divide  : [0.1784, 0.0879, 0.7337]
row 3 weights without the divide: [0.1142, 0.042, 0.8438]
```

(The `plain weights` line is row 2 of the no-dial pass: it is 18.4c. The three rows of `both dials` are 18.4e, f and g.)

### Page 18.5

**18.5a.** Each head gets **4** numbers. `(3, 6, 3, 4)`. After the swap `(3, 3, 6, 4)`. In words: `(batch, heads, places, numbers per head)`.
**18.5b.**

```text
   place 1:   [ 1  0  0  0 ]
   place 2:   [ 1  1  0  0 ]
   place 3:   [ 1  1  1  0 ]
   place 4:   [ 1  1  1  1 ]
```

**6** hidden, **10** visible (`1 + 2 + 3 + 4`).
**18.5c.** Row 3: **`[0.3333, 0.3333, 0.3333, 0]`**. Row sums **`[1, 1, 1, 1]`**.
**18.5d.** Every place first has `1/4 =` **0.25**. After zeroing, the row sums are **`[0.25, 0.50, 0.75, 1.00]`**. Checking that every **row adds to 1** would have caught it. Nothing raises an error, which is why it is dangerous.
**18.5e.** `e` to a hugely negative power is as close to zero as you like, and `e^-inf` is exactly 0, so the hidden place adds nothing to the total and takes nothing from the others; the row still adds to 1.

The check file printed:

```text
split  : (3, 6, 3, 4)
swapped: (3, 3, 6, 4)
tensor([[1., 0., 0., 0.],
        [1., 1., 0., 0.],
        [1., 1., 1., 0.],
        [1., 1., 1., 1.]])
places to hide: 6 | places that can be seen: 10
hide BEFORE the softmax, row sums: [1.0, 1.0, 1.0, 1.0]
zero AFTER the softmax,  row sums: [0.25, 0.5, 0.75, 1.0]
row 3, hidden before: [0.3333, 0.3333, 0.3333, 0.0]
```

### Page 18.6

**18.6a.** `2 × 2 × 14 =` **56**. **18.6b.** `3 × 196 =` **588**. **18.6c.** `588 + 210 =` **798**. **18.6d.** `up` `14 × 56 + 56 =` **840**; `down` `56 × 14 + 14 =` **798**; MLP **1,638**. **18.6e.** `56 + 798 + 1,638 =` **2,492**. Formula: `12 × 196 + 10 × 14 = 2,352 + 140 =` **2,492**.
**18.6f.** `3 × 2,492 =` **7,476**. In a plain list, `model.parameters()` counts **none** of the blocks' knobs (only whatever else the model holds): PyTorch finds knobs only in things stored as layers or inside an `nn.ModuleList`, so a plain list hides them, and training would not update them. No error is raised, so you only catch it by counting against the number you worked out by hand.
**18.6g.** `up` `14 × 28 + 28 = 420`, `down` `28 × 14 + 14 = 406`: MLP **826**. Block `56 + 798 + 826 =` **1,680**. **No**, the formula assumed a hidden width of `4d`.
**18.6h.** Attention compares the words and averages them, and the same set of vectors gives the same scores whichever order they came in, so it has no idea of order. A **position** vector (one for each place) is added to each word's vector first.

The check file printed:

```text
two layer norms      56
q, k, v (no bias)    588
proj                 210
up                   840
down                 798
block at d = 14: 2492  formula 12d^2 + 10d: 2492
three blocks: 7476
mlp with hidden width 2d: 826  block: 1680
formula at d = 24: 7152
```

### Page 18.7

Real printed output (this is the table above):

```text
knobs: 15868  windows: 6270 train, 694 val
step   train     val
   0  3.368  3.371
  50  1.690  1.763
 100  1.210  1.444
 200  0.738  1.357
 400  0.507  1.767
 600  0.489  2.056
 800  0.484  2.218
1000  0.483  2.332
knows nothing (uniform)    : 3.332
knows letter frequencies   : 2.854
knows the previous letter  : 2.031
```

**18.7a.** Step **200**, validation **1.357**. **18.7b.** Step 0: `3.371 - 3.368 =` **0.003**. Step 200: `1.357 - 0.738 =` **0.619**. Step 1000: `2.332 - 0.483 =` **1.849**. The gap is **growing**. **18.7c.** At step 0 the model has learned nothing specific to the training text, so it is equally bad at the text it has seen and the text it has not; the gap opens only once it learns things that belong to the training text alone.
**18.7d.** `3.368 - 3.332 =` **0.036**. **Yes**, it passes: the model starts out knowing nothing, as it should.
**18.7e.** Step 200: `2.031 - 1.357 =` **0.674** better. Step 1000: `2.332 - 2.031 =` **0.301 worse**. By step 1000 a table that just counts previous letters beats it on unseen text.
**18.7f.** A loss is an average *surprise*, in nats, not a percentage; `0.483` means a *typical* chance of about `e^-0.483 = 0.62` for the true next letter on the training text, which is not "95% right". It also says nothing about text the model has not seen; the validation loss is `2.332`.
**18.7g.** A good reply has all four: (1) two numbers, e.g. "training goes from 1.210 at step 100 to 0.483 at step 1000, but validation goes from 1.357 at step 200 to 2.332"; (2) validation is the fairer one, since the model never studied that text; (3) stop near step 200 where validation is lowest (save a snapshot of the best weights, or use a schedule or dropout, as in Week 5); (4) one run cannot tell you whether step 200 would be the best point on another seed, or on other text. **Not** enough: "it is overfitting, so it is bad".
**18.7h.** Any two of: whether another seed gives the same best step; whether a longer or different text behaves the same; whether a transformer (with more than 4 letters of memory) would do better; whether 694 validation letters are enough to trust small differences. (The table shows a *shape*: validation falls, bottoms out, rises. It is not a law.)

### Page 18.8

Real outputs, each program run on its own:

```text
A  [[0.665, 0.155, 0.114], [0.09, 0.422, 0.844], [0.245, 0.422, 0.042]]
   [0.935, 1.356, 0.709]
B  [1.33, 0.489, 0.18] 2.0
   share of picks that were letter 0: 0.6740000247955322
C  IndexError: Dimension out of range (expected to be in range of [-1, 0], but got 1)
D  0.9
```

**A.** (i) `dim=0` takes the softmax **down each column**, so the *columns* add to 1 and the *rows* do not. (ii) **Silent**: no error; the second line shows row sums of `0.935, 1.356, 0.709`, not 1. (iii) `F.softmax(scores, dim=-1)`. The check that catches it: do the rows add to 1?

**B.** (i) The division by the temperature came **after** the softmax, so the chances now add to `2.0` (`1.33 + 0.489 + 0.18`), and the scores were never sharpened. (ii) **Silent**: `torch.multinomial` accepts any non-negative numbers and does not check that they add to 1, so it still picks, and letter 0 comes up about `0.67` of the time, the same as temperature 1 would give (`0.665`), not the `0.86` that a temperature of 0.5 should. (iii) `probs = F.softmax(scores / temperature, dim=-1)` (divide the **scores**, then softmax). The fixed version gives chances `0.867, 0.117, 0.016` and letter 0 about 0.86 of the time in 1,000 picks. The check that catches it: print `probs.sum()`.

**C.** (i) `start` is **one-dimensional** (`(2,)`) but `names[:, :-1]` is two-dimensional, and `dim=1` does not exist for the start token. (ii) **Loud**: `IndexError: Dimension out of range`. The last line is the one to read; the line above it is **your** `torch.cat`. (iii) `start = torch.full((2, 1), 27)`, which gives `tensor([[27, 4, 9], [27, 7, 2]])`.

**D.** (i) `slope = 1.0` is **inside** the loop, so it is reset to 1 on every pass and only the last multiplication survives. (ii) **Silent**: it prints `0.9` (one step of compounding, not ten). (iii) Move `slope = 1.0` **above** the `for`. Then it prints `0.3487`. The check that catches it: you worked out `0.9 ^ 10` by hand to be about 0.349, and the printed number is nowhere near it.

### Page 18.9

No fixed answer: your marks. Two things to check: (1) the `Marks earned` column adds to your total; (2) you circled **at most two** weeks, and each has a **day and time** next to it. The tie order is **16, then 15, then 17**.

### Page 18.10 and Self-Check

Your own words. A good **Entry 4** says: a silent bug **runs**, prints a plausible number and gets written into a report, so nothing tells you to look. The check for each: for A, ask whether the **rows** add to 1; for B, print the **sum** of the chances before sampling; for D, compare with the number you worked out **by hand** (or print the value inside the loop). A good **Entry 5** is short and about a *habit* ("work out the number by hand before I run it", "check that the rows add to 1"), not a topic.

**Self-Check:** if you could tick fewer than five, you now have your **two** redos; they are the same as the ones on page 18.9.
