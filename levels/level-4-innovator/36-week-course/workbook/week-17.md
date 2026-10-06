# Workbook — Week 17: Build TinyGPT

**Name:** ________________________________  **Date:** ______________

[⬅ Week 16](week-16.md) · [📖 Read the chapter first](../student-guide/week-17.md) · [Course Home](../README.md) · [Next ➡](week-18.md)

---

![The 36 week tiles in four term lanes; weeks 1 to 16 solid, week 17 tinted pink with a thick border and a pointer above it, weeks 18 to 36 dashed](../figures/fig-w17-0-where-this-fits.svg)
*Figure 17.0 — Week 17 of 36, the TinyGPT lab, sits in term 2 (memory, then attention); weeks 1 to 16 are done and weeks 18 to 36 are still ahead.*

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the worked examples and in the answers came from real CPU runs (PyTorch 2.2.1, one thread, `torch.manual_seed(0)` wherever anything is random). The by-hand numbers (`-ln`, counts, windows) are plain arithmetic and will match exactly. The **knob counts, shapes and `ln 28`** will match on your machine exactly. The **losses and samples** matched on repeat runs here, but another PyTorch build can move a digit, and **step times always differ**.
>
> **Predict first, then run.** On pages 17.1, 17.3, 17.4, 17.5 and 17.7 you write your guess *before* you run anything. A wrong guess is useful. A guess written after the run is not a guess.
>
> **This week something really is trained.** Page 17.5 uses your `train.py` from class (about 90 seconds). Every other check file here is small: under 3 seconds. **There is no scripted backend and no stand-in anywhere in this workbook.** The model is real and the text is real, but the text is only 6,972 characters, so the model is a toy.
>
> **Keep your class files.** Pages 17.3 to 17.7 import your `tinygpt.py` from class (the `Block` from Week 16 and the `TinyGPT`). Run everything from the folder that contains `l4lib/`. Nothing here downloads anything.
>
> Use a **calculator with an `ln` key** (a phone will do, in airplane mode) and carry **three decimals** on every `-ln`.

---

## ✅ Warm-Up (5 min)

Five quick questions about **Weeks 1 and 16**.

**W1.** A two-class model that guesses 50-50 has log loss `ln 2` = ____________ (three decimals).

**W2.** One block at width `d` has `12 d^2 + 10 d` knobs. At `d = 10` that is ____________ .

**W3.** Why does a stack of blocks go in an `nn.ModuleList` and not a plain list? Finish: *PyTorch has to be able to* ________________________________

**W4.** The mask is a buffer, not a knob. Is it counted in the knobs? ____________

**W5.** A model knows nothing about 28 characters, so it gives each one `1/28`. Write what you expect its loss to be, as an `ln`: ____________ . (You will get the number on page 17.4.)

---

## 🪟 Page 17.1 — Windows and the Shift (by hand, then run)

One step of training cuts **windows** out of the text. For a text of `N` characters and a window of `T`, a start `s` gives

> `x = text[s : s + T]` and `y = text[s + 1 : s + T + 1]`

Here is a practice text (not the class text), 16 characters, **counting the spaces**:

```text
a red fox ran up
```

Number the characters from 0. Fill the start of the table first: `a`=0, `_`(space)=1, `r`=2, ...

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| a | _ | r | | | | | | | | | | | | | |

Window length `T = 6`. **Mark a space as `_`.**

**Part A — two windows.**

| Start `s` | `x` (6 characters) | `y` (6 characters) |
|:--:|---|---|
| 0 | ____________ | ____________ |
| 7 | ____________ | ____________ |

**Part B — the questions inside one window.** The window `x = a red_` (start 0) is not one question but six. Finish the table: the prefix the model has seen, and the character it must say next.

| Place | Prefix the model sees | True next character (this is `y` at that place) |
|:--:|---|:--:|
| 0 | `a` | `_` |
| 1 | `a_` | ____ |
| 2 | ____________ | ____ |
| 3 | ____________ | ____ |
| 4 | ____________ | ____ |
| 5 | ____________ | ____ |

**Part C — how many starts, how many questions.**

1. The last start that still leaves room for a full `y` is `s =` ____ . (Work it out: `y` ends at `s + T`, and `y` must not run past the end.)
2. The number of valid starts is `N - T =` ____ , so the call is `torch.randint(` ____ `, (B,))`. (The top number is **not** included.)
3. A batch has `B = 8` windows of `T = 6`. Questions asked in one step: ____ x ____ = ____ .
4. In class the batch was `B = 32`, `T = 64`: ____________ questions per step.
5. The class text has 6,274 training characters and 698 validation characters. The `randint` top for each (with `T = 64`): train ____________ , validation ____________ .

**Part D — check.** Run this. It uses a function you did not write but can read: `window(s)` is just the two slices above.

```python
# check171.py - Week 17 workbook page 17.1: windows and the shift, on a PRACTICE string (not the class one).
import torch

torch.manual_seed(0)
text = "a red fox ran up"                      # 16 characters, counting the spaces
T = 6                                         # window length
print("length:", len(text), "  T:", T)


def window(s):
    return text[s:s + T], text[s + 1:s + T + 1]


for s in (0, 7):
    x, y = window(s)
    print(f"start {s}:  x = |{x}|  y = |{y}|")

print("number of valid starts:", len(text) - T, "  (0 .. " + str(len(text) - T - 1) + ")")

starts = torch.randint(len(text) - T, (4,))   # four random starts, each from 0 to len - T - 1
print("random starts:", starts.tolist())
for s in starts.tolist():
    x, y = window(s)
    print(f"start {s}:  x = |{x}|  y = |{y}|")

B = 8
print("questions in a batch of", B, "windows:", B * T)
```

```text
length: 16   T: 6
start 0:  x = |a red |  y = | red f|
start 7:  x = |ox ran|  y = |x ran |
number of valid starts: 10   (0 .. 9)
random starts: [4, 9, 3, 0]
start 4:  x = |d fox |  y = | fox r|
start 9:  x = | ran u|  y = |ran up|
start 3:  x = |ed fox|  y = |d fox |
start 0:  x = |a red |  y = | red f|
questions in a batch of 8 windows: 48
```

Compare with your table. Then write: why is every `y` row just `x` moved one place? ________________________________

**What did the four random starts show?** One of them is `9`. What is `y` for it, and what would have happened at `s = 10`? ________________________________________________

![Two rows of character cells, x above and y below, where y is x moved one place left; below them 64 questions times 32 windows equals 2,048 questions.](../figures/fig-w17-1-one-window-many-questions.svg)
*Figure 17.1 — Moving the window one place left gives a next-character answer at every place, so one step asks 2,048 questions.*

---

## 🎯 Page 17.2 — Beat the Ladder, on Your Own Cards

You scored six class cards. Now the same game on a page.

**The rule again.** Write up to three letters and how sure you are of each (the numbers add up to 1 or less). You **may not** give any letter a probability of 0. Everything you did not list shares the rest equally: `(1 - listed) / (28 - letters listed)`. Score = `-ln(p)` of the share on the true letter. Lower is better.

**Keep next to you:**

| p | 0.9 | 0.5 | 0.25 | 0.1 | 0.01 | 1/28 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `-ln p` | 0.105 | 0.693 | 1.386 | 2.303 | 4.605 | 3.332 |

**The ladder from class.**

| Rung | Score (mean `-ln p`) |
|---|:--:|
| Knows nothing | 3.332 |
| Knows letter frequencies | 2.855 |
| Knows the previous letter | 2.033 |
| TinyGPT (fill in after page 17.5) | ______ |

**Part A — score a friend's guesses (by hand first).** A friend always lists the same letters: `e` 0.6, `a` 0.2, `o` 0.1. Score three true letters.

| True letter | Probability the friend gave it | Working | `-ln p` |
|:--:|---|---|:--:|
| `e` | ______ | | ______ |
| `a` | ______ | | ______ |
| `u` (not listed) | ______ = (1 - ____) / ____ | | ______ |

A second friend writes only `t` 0.9. True letter `s`: p = ____________ , score = ____________ .

A third friend writes `0` for a letter that turns out to be the true one. Their score is `-ln 0`, which is ____________ . Why does the rule forbid it? ________________________________

**Part B — check.** Run this, then edit the `friend` list for Part C.

```python
# check172.py - Week 17 workbook page 17.2: score some guesses with -ln(p). V = 28 characters.
import math

V = 28


def score(guess, true_letter):
    listed = sum(guess.values())
    share = (1 - listed) / (V - len(guess))          # what is left, shared by the letters not listed
    p = guess.get(true_letter, share)
    return p, -math.log(p)


friend = [({"e": 0.6, "a": 0.2, "o": 0.1}, "e"),
          ({"e": 0.6, "a": 0.2, "o": 0.1}, "a"),
          ({"e": 0.6, "a": 0.2, "o": 0.1}, "u"),
          ({"t": 0.9}, "t"),
          ({"t": 0.9}, "s")]
for guess, true_letter in friend:
    p, s = score(guess, true_letter)
    print(f"guess {guess}  true '{true_letter}'  p = {p:.4f}  score = {s:.3f}")

print("mean of the five:", round(sum(score(g, t)[1] for g, t in friend) / len(friend), 3))
```

```text
guess {'e': 0.6, 'a': 0.2, 'o': 0.1}  true 'e'  p = 0.6000  score = 0.511
guess {'e': 0.6, 'a': 0.2, 'o': 0.1}  true 'a'  p = 0.2000  score = 1.609
guess {'e': 0.6, 'a': 0.2, 'o': 0.1}  true 'u'  p = 0.0040  score = 5.521
guess {'t': 0.9}  true 't'  p = 0.9000  score = 0.105
guess {'t': 0.9}  true 's'  p = 0.0037  score = 5.598
mean of the five: 2.669
```

Did you match all five scores? ☐ yes ☐ no, and the slip was: ________________________________

**Part C — four new cards.** Each card is the text up to the hidden letter. **Guess first.** Only then look up the hidden letters in the answers page (Page 17.2, Part C) and score yourself. (The cards are from the class text, not the six from class.)

| Card | Context | Your letters and probabilities | Your `p` on the true letter | `-ln p` |
|:--:|---|---|:--:|:--:|
| 1 | `the rope maker made ro_` | | | |
| 2 | `under the bridge the water was co_` | | | |
| 3 | `the market opened at no_` | | | |
| 4 | `a window is a door for sound and l_` | | | |
| | **mean over the four** | | | ______ |

Where does your mean sit on the ladder? ________________________________

**Part D — think.**

1. Four cards is a tiny sample. Would your rung change with four more? ________ (circle: **probably / possibly / nobody knows**). Why? ________________________________
2. The model that counts only the previous letter sees one character. You see the whole phrase. On which card did seeing more help you most? ____ What did you give the true letter? ________
3. Which card was hardest? ____ Could anybody have known the next letter? ________

---

## 🔢 Page 17.3 — Count the Model

**Part A — the class model, `d = 128`, 4 blocks, `V = 28`, `T = 64`. Fill in BEFORE you run anything.**

| Part | Working | Count |
|---|---|:--:|
| character table | `V x d` = ____ x ____ | ______ |
| place table | `T x d` = ____ x ____ | ______ |
| one block | `12 d^2 + 10 d` | ______ |
| four blocks | 4 x ______ | ______ |
| final norm | `2 d` | ______ |
| output layer | `d x V + V` | ______ |
| **all** | | ______ |

Last week's prediction (page 16.5) was ____________ . Does it match? ☐ yes ☐ no. The `nested.py` from class printed the same number for the whole tree.

**Part B — a practice model, `d = 32`, 3 blocks, 4 heads (not from class).** Still `V = 28`, `T = 64`.

| Part | Working | Your prediction |
|---|---|:--:|
| character table | | ______ |
| place table | | ______ |
| one block | `12 x 32^2 + 10 x 32` | ______ |
| three blocks | | ______ |
| final norm | | ______ |
| output layer | | ______ |
| **all** | | ______ |

Run this. It builds the model and counts every part with `.numel()`.

```python
# check173.py - Week 17 workbook page 17.3: count the knobs of a PRACTICE TinyGPT (d = 32, 3 blocks) by part, then by formula.
import torch
from tinygpt import TinyGPT

torch.manual_seed(0)
V, d, H, L, T = 28, 32, 4, 3, 64
model = TinyGPT(V, d, H, L, T)

parts = {"tok": model.tok, "pos": model.pos, "blocks": model.blocks, "ln_f": model.ln_f, "head": model.head}
for name, part in parts.items():
    print(f"{name:<7}", sum(p.numel() for p in part.parameters()))

predicted = V * d + T * d + L * (12 * d * d + 10 * d) + 2 * d + (d * V + V)
actual = sum(p.numel() for p in model.parameters())
print("predicted:", predicted, " actual:", actual, " match:", predicted == actual)

# whose count is wrong? the three friends of part C, at d = 128 and 4 blocks
true_count = 28 * 128 + 64 * 128 + 4 * (12 * 128 * 128 + 10 * 128) + 2 * 128 + (128 * 28 + 28)
print("true count at d = 128:", true_count)
print("Ana  (true + biases on q, k, v):", true_count + 3 * 128 * 4)
print("Ben  (every norm counted as d, not 2d):", true_count - 9 * 128)
```

```text
tok     896
pos     2048
blocks  37824
ln_f    64
head    924
predicted: 41756  actual: 41756  match: True
true count at d = 128: 807196
Ana  (true + biases on q, k, v): 808732
Ben  (every norm counted as d, not 2d): 806044
```

Did your prediction match? ☐ yes ☐ no. If not, which line was off, and by how much? ________________________________

**Part C — whose count is wrong?** The true count at `d = 128` with 4 blocks is the number from Part A. Three friends disagree. For each, say what they most likely did, and then find out.

| Friend | Their count | How far from the true count | Most likely slip |
|---|:--:|:--:|---|
| Ana | 808,732 | ______ | |
| Ben | 806,044 | ______ | |
| Cy | 15,644 | ______ | |

Hints: *Ana's gap divides exactly by 128. Ben's is a multiple of 9. Cy's count is about the size of everything except one part.* The last three lines of `check173.py` print the first two cases; Cy is page 17.7, program B.

**Part D — change one setting.** Predict, by changing **one term** in Part A, the total if

1. the window `T` were 32 instead of 64 (keep everything else): ____________
2. the vocabulary `V` were 40 instead of 28: ____________

Which two parts change in each case? (1) ____________ (2) ____________ and ____________ . Does the mask count? ________

---

## 📐 Page 17.4 — The First-Loss Check

A model that knows nothing gives every character `1/V`, so its loss is `-ln(1/V) = ln(V)`. **The check:** build the model, take one batch, and see if the first loss is within **0.05** of `ln(V)`.

**Part A — by hand.** `ln 2 = 0.693`, `ln 10 = 2.303`. A model that knows nothing over 50 choices scores about ____________ . (Check your calculator: `ln 50`.)

**Part B — predict.** The default output layer gives scores with a bigger spread than the calm one (the class `calm_head=False` versus `True`). Before running, for a model with `d = 64` and 2 blocks on a real batch:

| | Your prediction of the first loss | PASS or FAIL? |
|---|---|:--:|
| `calm_head=False` | ______ | ______ |
| `calm_head=True` | ______ | ______ |

**Part C — run.** The last block also tries the check on **unshifted** targets (`y` the same as `x`). Predict that one too: PASS or FAIL? ______

```python
# check174.py - Week 17 workbook page 17.4: the first-loss check on a PRACTICE model (d = 64, 2 blocks), and what it cannot see.
import math
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

torch.manual_seed(0)
chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
d, H, L, T, B = 64, 4, 2, 64, 32

starts = torch.randint(len(data) - T, (B,))
x = torch.stack([data[s:s + T] for s in starts])
y = torch.stack([data[s + 1:s + T + 1] for s in starts])
print(f"ln({V}) = {math.log(V):.4f}")


def first_loss(calm, targets):
    torch.manual_seed(0)
    model = TinyGPT(V, d, H, L, T, calm_head=calm)
    with torch.no_grad():
        _, loss = model(x, targets)
    gap = abs(loss.item() - math.log(V))
    return loss.item(), gap, "PASS" if gap < 0.05 else "FAIL"


for calm in (False, True):
    loss, gap, verdict = first_loss(calm, y)
    print(f"calm_head={calm}:  honest y   first loss {loss:.4f}  distance {gap:.4f}  {verdict}")

loss, gap, verdict = first_loss(True, x)
print(f"calm_head=True:   y = x (no shift)  first loss {loss:.4f}  distance {gap:.4f}  {verdict}")

for other in (2, 10, 50):
    print(f"a model that knows nothing over {other} choices:  ln({other}) = {math.log(other):.3f}")
```

```text
ln(28) = 3.3322
calm_head=False:  honest y   first loss 3.5636  distance 0.2314  FAIL
calm_head=True:  honest y   first loss 3.3479  distance 0.0157  PASS
calm_head=True:   y = x (no shift)  first loss 3.3368  distance 0.0046  PASS
a model that knows nothing over 2 choices:  ln(2) = 0.693
a model that knows nothing over 10 choices:  ln(10) = 2.303
a model that knows nothing over 50 choices:  ln(50) = 3.912
```

**Part D — read it.**

1. Write the `calm_head=False` distance: ______ . One sentence: what does a `FAIL` of about this size tell you, and what does it **not** tell you? ________________________________________________
2. The unshifted model (`y = x`) **passed** the check. What does that teach you about what the check can see? ________________________________________________
3. Fill the blanks: *a first loss far **below** `ln(V)` is suspicious, because a brand-new model knows nothing: I should check that I am really scoring an untrained model, and remember that a leak in* ____________ *is* ____________ *at step 0; a first loss far **above** it means* ____________ .

---

## 🏃 Page 17.5 — The Run (the lab deliverable)

Run your `train.py` from class, unchanged, from the folder that contains `l4lib/`. It takes about 90 seconds; note what else is running on your laptop. **Write your seed here: ______** (the class file uses `torch.manual_seed(0)`).

**Predict first** (before you run):

| | My prediction |
|---|---|
| Step time in ms (one step = one batch) | ______ |
| At step 300, will the sample contain sentences? | ______ |
| Train loss at the end | ______ |
| Validation loss at the end | ______ |
| Will validation be above or below train? | ______ |

**Report.** Copy from your own terminal, not from anybody's page.

| Item | My run |
|---|---|
| Knobs | ______ |
| First loss (step 0): train / val | ______ / ______ |
| Distance of the step-0 train loss from `ln 28 = 3.332` | ______ |
| Step time | ______ ms |
| Final train / val | ______ / ______ |
| Gap (val - train) | ______ |
| Passes over the training text | ______ |
| Real words in 1,000 characters at step 0 / 300 / 1499 | ___% / ___% / ___% |

**The three samples.** Copy the first 100 characters of each.

Step 0: ________________________________________________________________

Step 300: ________________________________________________________________

Step 1499: ________________________________________________________________

**Order them without the labels.** Cover the step numbers. What one piece of evidence tells you the step-1499 sample is the latest? ________________________________________________

**The real-word share.** It counts words that appear in the training text. What can it tell you? ________________ What can it not tell you? ________________

**Did any number fall outside what you expected?** If yes, before accepting it check: the `STEPS` line, the learning rate, the shift of `y`, the model size. Which did you check? ________________

**Optional: a shorter run (predict first).** Change `STEPS` to `600` in a copy of `train.py` (not the original) and predict whether the gap will be **bigger / smaller / about the same**: ______ . Run it and write the gap you measured: ______ . Do not borrow anyone's number. Page 17.6 shows a run of someone else's to read.

**Delete any copy you made** when you are done, so you keep one `train.py`.

![Left, a chart of training loss (solid) and validation loss (dashed) against step, with a dashed line at ln 28 and a bracket marking the final gap. Right, two bars: the first-loss distance for calm_head=False (long, FAIL) and calm_head=True (short, PASS).](../figures/fig-w17-2-loss-gap-and-first-check.svg)
*Figure 17.2 — Training loss keeps falling while validation flattens, and a calm output layer starts within 0.05 of ln 28.*

---

## 🧐 Page 17.6 — What the Gap Means

**Part A — read a run that is not yours.** This is a real run of the same model with `STEPS = 600` (seed 0, one thread, about 36 seconds). It is a *different* run from the one in class. Fill in the gaps (validation minus train, three decimals).

| Step | Train | Validation | Gap |
|:--:|:--:|:--:|:--:|
| 0 | 3.349 | 3.351 | ______ |
| 250 | 1.980 | 1.956 | ______ |
| 300 | 1.906 | 1.915 | ______ |
| 500 | 1.781 | 1.808 | ______ |
| 599 | 1.777 | 1.808 | ______ |
| FINAL | 1.757 | 1.800 | ______ |

1. In this run the gap at the end is small. Is this a **better** model than your 1,500-step run? Compare the two validation losses: ________________________________
2. A small gap and a good model are **not** the same thing. Write one sentence to say why. ________________________________________________
3. At step 250 the gap is negative. Is that a problem? ________________ (hint: both numbers are estimates from 20 random batches, and the model is still bad at everything)

**Part B — your own gap.** Write a two-sentence answer about your 1,500-step run and one sentence about what you did **not** test, then one experiment.

1. What the gap is, as a number with its direction: ________________________________________________
2. What it means (which number is the fairer one for text the model has not seen?): ________________________________________________
3. What it does **not** mean, and what we did not run: ________________________________________________
4. One concrete next experiment (say what you would change and what you would measure): ________________________________________________

**Part C — mark yourself** (one mark each, be honest):

- ☐ I stated the gap as a number and said validation is higher.
- ☐ I said the validation number is the fairer one for unseen text.
- ☐ I linked it to the model fitting the text it saw, and used the growth of the gap across checkpoints as my evidence.
- ☐ I said what I did **not** test (more data, less training, dropout, other seeds).
- ☐ I named one concrete next experiment.

Score: ____ / 5. Any answer that says *"so the model is bad"* or *"so the model understands English"* loses the last two marks.

---

## 🐞 Page 17.7 — Break It on Purpose

Every program below is **deliberately broken**. Write the "Predict" line **before** you run. Each file is self-contained except for the `tinygpt.py` you made in class. **Two are silent**: they run, and the only sign is a number you must check.

**Program A (deliberate).**

```python
import torch
import torch.nn.functional as F

torch.manual_seed(0)
scores = torch.randn(4, 6, 28)                 # (B, T, V): scores for 4 windows of 6 places
targets = torch.randint(28, (4, 6))            # (B, T): the true next character at each place
loss = F.cross_entropy(scores, targets)
print("loss:", loss.item())
```

Predict: runs or error? ____________ Last line: ________________________________ Fix: ________________________

**Program B (deliberate, SILENT).**

```python
import torch
import torch.nn as nn
from tinygpt import Block

torch.manual_seed(0)


class Tiny(nn.Module):
    def __init__(self, d, H, L, T):
        super().__init__()
        self.blocks = [Block(d, H, T) for _ in range(L)]
        self.head = nn.Linear(d, 28)


model = Tiny(16, 2, 3, 8)
print("knobs PyTorch can see:", sum(p.numel() for p in model.parameters()))
print("knobs I meant        :", 3 * (12 * 16 * 16 + 10 * 16) + (16 * 28 + 28))
```

Predict: does it run? ______ The two numbers will be ______ and ______ . Which one is right? ______ Fix: ________________________

**Program C (deliberate).** Generation that forgets to keep only the last `T` places. Here `T = 8`.

```python
import torch
import torch.nn.functional as F
from tinygpt import TinyGPT

torch.manual_seed(0)
model = TinyGPT(28, 16, 2, 1, 8)               # a small model: 8 places


@torch.no_grad()
def generate_bad(model, idx, n_new):
    for _ in range(n_new):
        logits, _ = model(idx)                 # the whole history, however long
        probs = F.softmax(logits[:, -1, :], dim=-1)
        idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
    return idx


out = generate_bad(model, torch.zeros(1, 1, dtype=torch.long), 12)
print("made", out.shape[1], "characters")
```

Predict: after how many characters does it stop? ______ Last line: ________________________________ Fix: ________________________

**Program D (deliberate, SILENT).** `y` is not moved one place. The training loss should look wonderful.

```python
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT

torch.manual_seed(0)
chars = sorted(set(TEXT))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
train_data, val_data = data[:6274], data[6274:]
T, B = 32, 16


def get_batch(src, shift):
    starts = torch.randint(len(src) - T, (B,))
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + shift:s + shift + T] for s in starts])    # shift = 1 is honest; shift = 0 is the bug
    return x, y


model = TinyGPT(28, 32, 4, 2, T)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
for step in range(300):
    x, y = get_batch(train_data, 0)                                   # DELIBERATE: no shift
    _, loss = model(x, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
print("training loss at step 299 (y = x):", round(loss.item(), 3))

with torch.no_grad():
    x, y = get_batch(val_data, 1)                                     # honest targets, text the model never trained on
    _, honest = model(x, y)
print("loss on honest targets:", round(honest.item(), 3))
```

Predict: training loss at step 299, roughly? ______ Loss on honest targets (validation text)? ______ Which of the two would you report, and which number is a bug alarm? ________________

**Program E (deliberate).** The `randint` top one too big.

```python
import torch

torch.manual_seed(0)
text = torch.arange(100, 110)                  # ten pretend characters
T = 4
starts = torch.randint(len(text) - T + 1, (12,))      # DELIBERATE: the top is one too big
print("starts:", starts.tolist())
x = torch.stack([text[s:s + T] for s in starts])
y = torch.stack([text[s + 1:s + T + 1] for s in starts])
print("x", tuple(x.shape), " y", tuple(y.shape))
```

Predict: runs or error? ______ Last line: ________________________________ Fix: ________________________

**My own slip.** Write down one mistake you made this week that was not in this list: ________________________________________________

---

## 📓 Page 17.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Add a row for every real error you hit this week, not only the deliberate ones.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more; this week there were two in the workbook): write the one I made, or nearly made. ________________________________________________

**The habit for silent mistakes.** Fill in the blanks: *after I build a model I count the* ____________ *and compare with my* ____________ ; *before I train I run the* ____________ *check, and I remember that it cannot see a wrong* ____________ ; *when a training loss looks too good I score the model on* ____________ *targets.*

Write this sentence in your own handwriting:

> **"Check the size, check the first loss, and never say the model understands."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **What is one question in a training step? What is `y` compared with `x`? How many questions in a batch of 32 windows of 64?**

________________________________________________________________

2. **Why must the top number of `torch.randint` be `N - T`?**

________________________________________________________________

3. **Name the parts of `TinyGPT` in order, and say which one is a module made of modules.**

________________________________________________________________

4. **What loss should an untrained model have on 28 characters, and why? What does a `FAIL` of 0.17 tell you, and what can the check never catch?**

________________________________________________________________

5. **Train loss 0.9, validation loss 1.4. What do you say, and what do you not say?**

________________________________________________________________

6. **Your friend says "it writes English now".** What do you say? Use "real words" and "a character at a time".

________________________________________________________________

7. *Parking Lot.* The class run is one seed on 6,972 characters. Write one thing that would need to be true before you called a result about "transformers" rather than about this run: ________________________________

**Mark yourself.** Tick the first line you can honestly say.

- [ ] **Not yet:** I cannot say why `y` is `x` moved one place.
- [ ] **Developing:** I can cut windows and count questions, but my knob count is off by a bias or a norm, or I say "FAIL means it will not train".
- [ ] **Secure:** I get 807,196 by part, 41,756 at `d = 32` with three blocks, predict the step-0 loss near `ln 28`, and write the gap as a number with a direction.
- [ ] **Fluent:** I explained why the first-loss check passes on unshifted targets, read a small gap in a worse model correctly, and named a control I did not run.

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-17.md) · [Next ➡](week-18.md)

---
---

# ✂️ ANSWERS - keep this page folded until you have finished

*Numbers come from real runs: CPU, PyTorch 2.2.1, one thread, `torch.manual_seed(0)` wherever anything is random. The by-hand numbers are plain arithmetic and should match to three decimals (within 0.001 of rounding). The knob counts, shapes and `True`/`False` lines will match on any build; losses may move a digit, and step times always differ.*

### Warm-Up

- **W1.** 0.693.
- **W2.** `12 x 100 + 10 x 10 =` **1,300**.
- **W3.** ...see the blocks inside the model, so that `model.parameters()` reaches them (for the optimizer and the count).
- **W4.** No. A buffer is saved with the model but is not a knob.
- **W5.** `ln 28` (= 3.332).

### Page 17.1

The table: `a`(0) `_`(1) `r`(2) `e`(3) `d`(4) `_`(5) `f`(6) `o`(7) `x`(8) `_`(9) `r`(10) `a`(11) `n`(12) `_`(13) `u`(14) `p`(15).

| Start | `x` | `y` |
|:--:|---|---|
| 0 | `a red_` | `_red_f` |
| 7 | `ox_ran` | `x_ran_` |

(With `_` for the space, as `check171.py` prints them with spaces.)

Part B:

| Place | Prefix | True next |
|:--:|---|:--:|
| 0 | `a` | `_` |
| 1 | `a_` | `r` |
| 2 | `a_r` | `e` |
| 3 | `a_re` | `d` |
| 4 | `a_red` | `_` |
| 5 | `a_red_` | `f` |

Part C: (1) `s = 9` (`y` is `text[10:16]`; `s = 10` would need a 17th character). (2) `N - T = 16 - 6 =` **10** valid starts (0 to 9); `torch.randint(10, (B,))`. (3) 8 x 6 = **48**. (4) 32 x 64 = **2,048**. (5) train 6,274 - 64 = **6,210**; validation 698 - 64 = **634**.

Part D: the program's output above. `y` is `x` moved one place because `y` starts at `s + 1`. For `s = 9`: `x = _ran_u`, `y = ran_up` (`x` has a space first). At `s = 10` the `y` slice `text[11:17]` has only 5 characters, so the rows no longer stack (program E).

### Page 17.2

Part A:

| True | p | `-ln p` |
|:--:|---|:--:|
| `e` | 0.6 | **0.511** |
| `a` | 0.2 | **1.609** |
| `u` | (1 - 0.9) / 25 = 0.004 | **5.521** |

Second friend, true `s`: p = (1 - 0.9) / 27 = **0.0037**, score **5.598**. Third friend: `-ln 0` is **infinite** (as `p` shrinks, `-ln p` grows without limit); a model that said it was impossible would be infinitely wrong the first time it was not. The mean of the five scores in `check172.py` is 2.669. *Common errors:* forgetting the leftover is shared among the letters **not** listed (25 after three, 27 after one); using log base 10.

Part C: the hidden letters are **p**, **l**, **o**, **i**. Scoring is the student's own; any mean is acceptable provided each line shows the probability given to the true letter and `-ln p` to three decimals. A guess of 0.9 on the true letter scores 0.105; 0.1 scores 2.303. The counting models sit at 3.332, 2.855 and 2.033. After page 17.5 the TinyGPT rung is **about 1.44** (validation loss, seed 0).

Part D: (1) nobody knows. Four cards are a small sample; one bad card moves the mean a lot. (2) Card 1 (`made ro_`, `rope`) usually: a person who sees `rope maker made ro` has the word. (3) Card 4 or card 3, where several letters are plausible (`no_`: `noon`, `nothing`, `nobody`). What to draw out: a person who sees the whole phrase can beat a model that sees one letter.

### Page 17.3

Part A:

| Part | Working | Count |
|---|---|:--:|
| character table | 28 x 128 | **3,584** |
| place table | 64 x 128 | **8,192** |
| one block | 12 x 128^2 + 10 x 128 = 196,608 + 1,280 | **197,888** |
| four blocks | 4 x 197,888 | **791,552** |
| final norm | 2 x 128 | **256** |
| output layer | 128 x 28 + 28 | **3,612** |
| **all** | | **807,196** |

Part B (`d = 32`, 3 blocks): 28 x 32 = **896** · 64 x 32 = **2,048** · one block 12 x 1,024 + 320 = **12,608** · three blocks **37,824** · final norm **64** · output layer 32 x 28 + 28 = **924** · all **41,756**. `check173.py` printed `match: True`.

Part C: the true count is 807,196.

| Friend | Count | Gap | Slip |
|---|:--:|:--:|---|
| Ana | 808,732 | +1,536 = 3 x 128 x 4 | gave `q`, `k` and `v` a bias (they have none: `bias=False`) in four blocks |
| Ben | 806,044 | -1,152 = 9 x 128 | counted each of the 9 layer norms as `d` instead of `2 d` (a layer norm has a scale **and** a shift) |
| Cy | 15,644 | -791,552 | the blocks sat in a plain list, so PyTorch did not see them: only `tok` + `pos` + `ln_f` + `head` = 3,584 + 8,192 + 256 + 3,612 |

Part D: (1) `T = 32`: the place table is 32 x 128 = 4,096, so **803,100** (checked by building it). Only the place table changes; nothing in a block depends on `T`. (2) `V = 40`: the character table (40 x 128 = 5,120) and the output layer (128 x 40 + 40 = 5,160); total **810,280** (checked). The mask does **not** count.

### Page 17.4

Part A: `ln 50` = **3.912**.

Part B and C: the table below is from `check174.py` (seed 0, a 32 x 64 batch, `d = 64`, 2 blocks). Yours will be close; the ordering and the verdicts should match.

| | Our run | Verdict |
|---|:--:|:--:|
| `calm_head=False` | 3.5636 (distance 0.2314) | **FAIL** |
| `calm_head=True` | 3.3479 (distance 0.0157) | **PASS** |
| `calm_head=True`, `y = x` | 3.3368 (distance 0.0046) | **PASS** |

Part D: (1) **0.23 here.** A `FAIL` of this size says the model *starts a little over-confident* (the untouched output layer gives bigger scores than the calm one). It does **not** say the model is broken or cannot train; in class a `FAIL` of 0.17 trained fine. (2) The check looks only at the loss when the model has seen nothing. A wrong `y` changes which answer the loss is compared with, not how confident the model is, so a model that can see its answer still starts at `ln(V)`. The check **cannot** catch a wrong `y`. (3) *A first loss far below `ln(V)` is suspicious, because a brand-new model knows nothing: check that you are really scoring an untrained model. A leak in `y` is invisible at step 0 (blanks: `y`, invisible); far above means the output layer starts too confident, or the targets are wrong (ids out of order).* What to draw out: a check that is off tells you to look; a check that passes is not a proof.

### Page 17.5

What a complete report contains (our run, seed 0, one thread; yours uses your own):

| Item | Our run | Acceptable to expect |
|---|---|---|
| Knobs | 807,196 | exactly 807,196 |
| First loss (step 0): train / val | 3.349 / 3.351 | within 0.05 of 3.332 |
| Distance of train from `ln 28` | 0.017 | under 0.05 |
| Step time | 53 ms (60 ms on another run) | 30-150 ms at one thread |
| Final train / val | 0.907 / 1.447 | train 0.8-1.0, val 1.35-1.55 (our judgement of what is normal, from one seed) |
| Gap | 0.540 | positive and clearly above 0.3 |
| Passes over the text | 490 | 490 |
| Real words at step 0 / 300 / 1499 | 0% / 17% / 60% | rising |

Samples: step 0 is random characters; step 300 has `the`, `and`, `an` but no sentences (`the man adid ing sa theand and the fowit ...`); step 1499 has lines that start with `the` and end with a full stop, made of real words joined with near-words (`the old man mem menthy witer.`). Evidence for order: the share of real words rises, full stops and line breaks appear, spaces fall between short words. The share counts words that are copied from the training text; it says **nothing** about meaning. *If a number is outside the range:* `STEPS`, `lr`, a missing shift, a different model size.

Optional 600-step run (ours, seed 0): the final gap is **0.043**, **smaller** than 0.540. Train 1.757, val 1.800, 59 ms a step, 196 passes.

### Page 17.6

Part A:

| Step | Gap |
|:--:|:--:|
| 0 | 0.002 |
| 250 | -0.024 |
| 300 | 0.009 |
| 500 | 0.027 |
| 599 | 0.031 |
| FINAL | 0.043 |

1. **No.** Its validation loss is 1.800, against about 1.447 for the 1,500-step run: the gap is small because the model has not learned much, not because it learned well. 2. A gap measures the *difference* between two scores; both can be bad. (A model that knows nothing has a gap of about 0.002.) 3. No: at step 250 the difference is inside the noise of estimating each loss from 20 random batches, and the model is still bad at everything. (We did not measure that noise.)

Part B, model answer: *"The gap is validation loss minus training loss (1.447 - 0.907 = 0.540). It means the model does much better on characters it was trained on than on characters it has not seen, which is what memorising the training text looks like. It was about zero at step 300 and grew at each later checkpoint. It does not mean the model is useless, and it does not prove why; we did not run a version with more text, less training or dropout, which would be the test."* Mark scheme (5): the gap as a number with its direction · validation is the fairer number for unseen text · linked to fitting the text it saw, using the growth across checkpoints · what was **not** tested · one concrete next experiment.

### Page 17.7

- **A.** Runs? **No.** Last line: `RuntimeError: Expected target size [4, 28], got [4, 6]`. `cross_entropy` wants the scores as `(rows, 28)` and the targets as `(rows,)`. Fix: `F.cross_entropy(scores.reshape(4 * 6, 28), targets.reshape(4 * 6))` (the `reshape` TinyGPT uses).
- **B (SILENT).** It runs. PyTorch sees **476**; I meant **10,172**. 476 is only the output layer (16 x 28 + 28): the blocks are in a plain list. Fix: `nn.ModuleList([...])`. It is also why the optimizer would never move the blocks.
- **C.** It stops after the history passes 8 characters, when the position table (8 rows) is asked for place 8. Last line: `IndexError: index out of range in self`. Fix: pass `idx[:, -model.T:]` to the model (the class `generate` does: `idx[:, -self.T:]`). It made 8 characters without error; the ninth call fails.
- **D (SILENT).** Training loss at step 299 is **0.044** (the model learned to copy the character it sees, no prediction at all); on honest targets, **6.585**, far worse than `ln 28 = 3.332`, since it has learned to repeat its input. Report the honest one; a training loss of 0.04 in 300 steps is the bug alarm. The first-loss check cannot catch it (page 17.4).
- **E.** Runs? **No.** The starts are printed (`[4, 3, 0, 2, 1, 2, 6, 3, 4, 5, 2, 0]`) and one of them is 6; the last line is `RuntimeError: stack expects each tensor to be equal size, but got [4] at entry 0 and [3] at entry 6`. Fix: `torch.randint(len(text) - T, (12,))`. Note it only fails if a batch happens to draw the top start; with a big text and a small batch it can go unseen for many steps, which is why the top is worth computing by hand.

### Bug Log and Self-Check

Model entries for the Bug Log: `cross_entropy` shape (Program A), `AttributeError: cannot assign module before Module.__init__() call` (from the student guide's `bad_init.py`), `IndexError: index out of range in self` (Program C), `RuntimeError: stack expects each tensor to be equal size` (Program E).

Self-Check, short answers: (1) one question = "what comes after this prefix?"; `y` is `x` moved one place left; 32 x 64 = 2,048. (2) `y` runs to `s + T`, so `s` can be at most `N - T - 1`, and `randint` leaves the top out. (3) Character table, place table, four blocks, final norm, output layer; `TinyGPT` holds `Block`s (module inside a module). (4) `ln 28 = 3.332`, each character gets 1/28; a 0.17 `FAIL` says it starts over-confident, not broken; it can never catch a wrong `y`. (5) "On text it studied 0.9, on text it did not 1.4; consistent with memorising, not proven." Not: "it's good" or "it's overfitting so it's bad". (6) "Its samples have mostly real words (60%) and some near-words; it learned the shape of sentences a character at a time from 6,972 characters; it has not read anything." (7) Open: more than one seed, more text, controls.
