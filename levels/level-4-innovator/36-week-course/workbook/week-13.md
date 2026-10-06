# Workbook — Week 13: Choosing the Next Letter (Sampling and Exposure Bias)

**Name:** ________________________________  **Date:** ______________

[⬅ Week 12](week-12.md) · [📖 Read the chapter first](../student-guide/week-13.md) · [Course Home](../README.md) · [Next ➡](week-14.md)

---

> **Rules for this workbook.** Pages 13.1 to 13.5 are the week's homework (about 60-75 minutes, of which about 40 seconds is the computer working on page 13.4). Page 13.6 (break it on purpose) and page 13.7 (the Bug Log) are the extra pages that make the week stick; do them in the same sitting if you can.
>
> **Pen first, then run.** Write your answer **before** you open the check file. The numbers in the worked examples and in the answers came from real CPU runs (PyTorch, `torch.manual_seed(0)` wherever anything is random). By-hand numbers are plain arithmetic and will match exactly. Different CPU or PyTorch build: the **last digit** of a chance can move, and a count of "new names" can move by a name or two.
>
> **The model is real and small.** `namelm.py` is your Week 12 name model, trained on the 231 typed names and nothing else. There is **no scripted stand-in** anywhere in this workbook. The scores on pages 13.2, 13.3 and 13.6 are **invented by us** to make the arithmetic readable; they are not from any model.
>
> **Nothing new to install, no internet.** Run every check file from the folder that contains `l4lib/`. Files that use the name model also need `namelm.py` and `samplers.py` next to them. Carry **three decimals** by hand unless a page says otherwise.
>
> **Only this week's four tools are used:** `F.softmax(x, dim=-1)`, `torch.multinomial`, `torch.topk`, and `torch.sort` with `torch.cumsum`.

![Map of the 36 weeks in four term lanes with week 13, Choosing the Next Letter, highlighted in term 2 and weeks 1 to 12 solid behind it](../figures/fig-w13-0-where-this-fits.svg)
*Figure 13.0 — Where this week fits: week 13 of 36, in term 2 (memory, then attention).*

---

## ✅ Warm-Up (5 min, before anything else)

**W1.** A model gives five letters the scores `3, 1, 0, 0, 0`. The model's **output** is: (circle one) **one letter / one score per letter / one probability of being right**.

**W2.** In `F.softmax(x, dim=-1)`, the `-1` means softmax runs along the ____________ axis.

**W3.** You divide every score by `T`. For a **flatter** set of chances you make `T` **bigger / smaller** (circle one).

**W4.** Greedy picks the letter with the ____________ score, and uses ____________ (how much?) randomness.

**W5.** Write one sentence on what a **recurrent cell carries along** from one step to the next: ___________________________________________

---

## 🎲 Page 13.1 — Greedy, and the Sampler Table (15 min)

**Part A. Before you read anything else, write your guess.** A name model always picks the most likely next letter. You ask it for 200 names. Roughly how many **different** names do you get? ____________ . Why? ___________________________________________

**Part B. Predict the shape.** Cover the counts. For each sampler, write **more** or **fewer** compared with `T = 1.0` for (i) distinct names out of 200 and (ii) new names out of 200 (a name is **new** if it is not in the 231 training names).

| Sampler | (i) distinct: more / fewer? | (ii) new: more / fewer? |
|---|:--:|:--:|
| greedy | | |
| `T = 0.5` | | |
| `T = 1.5` | | |
| top-k, `k = 5` | | |
| top-p, `p = 0.9` | | |

**Part C. The measured table.** Run `namegen.py` from class and fill in the numbers, then one word from **repeats · recites · balanced · rambles · narrow · careful**.

| Sampler | distinct / 200 | new / 200 | One word |
|---|:--:|:--:|---|
| greedy | | | |
| `T = 0.5` | | | |
| `T = 1.0` | | | |
| `T = 1.5` | | | |
| top-k 5 | | | |
| top-p 0.9 | | | |
| `T = 1.5` + top-p 0.9 | | | |

**Part D.** Which row of the table makes the **best** names? Circle one row above and write what you mean by *best*, in one sentence. ___________________________________________

Did your Part B directions match? Count the matches: ______ / 10. **A new string is not a new *name*.** Hold on to that for page 13.3.

---

## 🧮 Page 13.2 — Scores to Chances: by Hand, then Predict, then Measure (25 min)

**A note on the method.** Softmax has three steps: (1) `exp` of each score, (2) add them up, (3) divide each by the total. Temperature is one step **before** those: divide every score by `T`. Use `exp(0) = 1.000`, `exp(1) = 2.718`, `exp(2) = 7.389`, `exp(-1) = 0.368`, `exp(0.5) = 1.649`, `exp(0.25) = 1.284`, `exp(-0.5) = 0.607`.

**Worked example (done for you).** Three letters `m o p` with the invented scores `2.0, 0.0, 1.0`, at `T = 1`.

| Letter | score | `exp(score)` | ÷ total |
|:--:|:--:|:--:|:--:|
| m | 2.0 | 7.389 | 7.389 / 11.107 = **0.665** |
| o | 0.0 | 1.000 | 1.000 / 11.107 = **0.090** |
| p | 1.0 | 2.718 | 2.718 / 11.107 = **0.245** |

Total = 7.389 + 1.000 + 2.718 = **11.107**. The three chances add to 1.

### Part A. Your turn, by hand (`a b c d e`, scores `0, 2, -1, 1, 0.5`)

The scores are from the chapter. **At `T = 2` first divide each score by 2**, then follow the same three steps.

| Letter | score | `T = 1`: exp | `T = 1`: ÷ 13.124 | score ÷ 2 | `T = 2`: exp | `T = 2`: ÷ total |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| a | 0.0 | | | | | |
| b | 2.0 | | | | | |
| c | -1.0 | | | | | |
| d | 1.0 | | | | | |
| e | 0.5 | | | | | |
| **total** | | **13.124** | **1.000** | | | **1.000** |

The `T = 2` total is ____________ . Which letter is best at both `T`? ______ . Did its chance go **up** or **down** when `T` went from 1 to 2? ____________

### Part B. Predict, **then** measure (the assigned task)

Five letters `s t a r e` with the invented scores **`1.5, 1.0, 0.0, -0.5, 2.5`**. **Before you run anything**, fill in the two prediction columns for `T = 0.3`, `T = 1` and `T = 2`.

| T | Most likely letter (predict) | Its share vs `T = 1`: **up** or **down**? (predict) |
|:--:|:--:|:--:|
| 0.3 | | |
| 1 | | *(the reference)* |
| 2 | | |

Now write `check132.py`, built from `five.py`, that prints `F.softmax(scores / T, dim=-1)` for each `T`, and fill in the measured chances to three decimals.

| T | s | t | a | r | e | best letter's share |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.3 | | | | | | |
| 1.0 | | | | | | |
| 2.0 | | | | | | |

Was each prediction right? T = 0.3 ☐ right ☐ wrong · T = 2 ☐ right ☐ wrong. If wrong, what did you expect, and what did the table say? ___________________________________________

### Part C. Does the wheel match the table? (`torch.multinomial`)

Add to the file: draw **10,000** letters from the `T = 1` chances with `torch.manual_seed(0)` and `torch.multinomial(p, 10000, replacement=True)`, and print the share of each letter. Write the shares, next to the table's `T = 1` row:

| | s | t | a | r | e |
|---|:--:|:--:|:--:|:--:|:--:|
| drawn (10,000) | | | | | |
| table, `T = 1` | | | | | |

Are the two rows the same to the third decimal? ☐ yes ☐ no. Why should they be *close*, but not *identical*? ___________________________________________

### Part D. The extension (if you are flying)

The biggest score is 2.5 and the smallest is -0.5: a gap of **3.0**. At each `T`, divide the biggest chance by the smallest (with a calculator, from your unrounded program output, not from the three-decimal table). Then compare with `e^(3.0 / T)`. What do you notice? ___________________________________________

![Three bar charts of the chances of the letters a to e from the same five scores, at T = 0.3, 1 and 2; the bar for b is highlighted and falls from 0.958 to 0.375](../figures/fig-w13-1-temperature-dial.svg)
*Figure 13.1 — Temperature does not change which letter is best, only how much it wins by.*

---

## ✂️ Page 13.3 — Top-k and Top-p, by Hand, and the Name Tasting (25 min)

### Part A. The two cutting rules in words

**Top-k** keeps the ____________ letters with the ____________ scores, then re-shares the chances so they add to 1.

**Top-p** sorts the chances big to small, takes a running total, and keeps a letter if the total of the letters **above it** is **less than / more than** (circle one) `p`.

### Part B. Worked example (done for you, on scores **not in order**)

Letters `w x y z`, scores `0, 1, 3, 2`, `T = 1`. The chances, in the order `w x y z`, are **0.032, 0.087, 0.644, 0.237**.

- **Top-2:** the two biggest scores are at `y` and `z`. Re-share: 0.644 / 0.881 = **0.731** and 0.237 / 0.881 = **0.269**. (`0.881 = 0.644 + 0.237`.)
- **Top-p with `p = 0.8`:** sorted, the order is `y z x w` with chances `0.644, 0.237, 0.087, 0.032`. The running total is `0.644, 0.881, 0.968, 1.000`. The total **above** each is `0, 0.644, 0.881, 0.968`. Keep a letter if that is below 0.8: `y` (0) yes, `z` (0.644) yes, `x` (0.881) **no**. Kept: `y z`, re-shared `0.731, 0.269`.
- **Top-p with `p = 0.5`:** nothing is above `y` (0 < 0.5, kept); above `z` is 0.644, which is not below 0.5. Kept: `y` alone. **The top letter always passes.**

### Part C. Your turn (the assigned task)

Scores `[2, 1, 0.5, 0]` for four letters, `T = 1`. Use `exp(2) = 7.389`, `exp(1) = 2.718`, `exp(0.5) = 1.649`, `exp(0) = 1`.

Total of the four `exp` values: ____________ .

| Letter | 1st | 2nd | 3rd | 4th |
|---|:--:|:--:|:--:|:--:|
| chance | | | | |
| running total | | | | |
| total **above** this letter | | | | |

1. **Top-2.** Keep the first two. Their re-shared chances are ____________ and ____________ .
2. **Top-p, `p = 0.9`.** Letters kept: ____________ . Their re-shared chances: ____________ .
3. **Top-p, `p = 0.5`.** Letters kept: ____________ . Why not two? ___________________________________________
4. If `p` is tiny, such as 0.01, how many letters survive? ____________ . Why? ___________________________________________

Now check your hand numbers. Type `check133.py` **after** your hand work is done (it uses only this week's tools: `torch.topk`, `torch.sort`, `torch.cumsum`), run it, and write the number of hand slips: ______ .

```python
# check133.py - Week 13 workbook page 13.3: check the hand top-k and top-p.
import torch
import torch.nn.functional as F

def show(name, scores, letters, cuts):
    p = F.softmax(torch.tensor(scores), dim=-1)
    print(name, "probs :", [round(float(x), 3) for x in p])
    top_v, top_i = torch.topk(p, 2)                      # the two biggest chances and where they sit
    kept = top_v / top_v.sum()                           # re-share so they add to 1
    print("  top-2 at :", [letters[int(i)] for i in top_i], " kept:", [round(float(x), 3) for x in kept])
    sorted_p, order = torch.sort(p, descending=True)
    running = torch.cumsum(sorted_p, dim=-1)
    before = running - sorted_p                          # the total of the letters ABOVE each one
    print("  sorted   :", [round(float(x), 3) for x in sorted_p], [letters[int(i)] for i in order])
    print("  running  :", [round(float(x), 3) for x in running])
    print("  before   :", [round(float(x), 3) for x in before])
    for cut in cuts:
        keep = sorted_p * (before < cut)
        keep = keep / keep.sum()
        print("  top-p", cut, ":", [round(float(x), 3) for x in keep])

show("worked", [0.0, 1.0, 3.0, 2.0], "wxyz", [0.8, 0.5])
show("yours ", [2.0, 1.0, 0.5, 0.0], "1234", [0.9, 0.5, 0.01])
```

### Part D. The Name Tasting (in class, with your teacher's sheet)

Forty unlabelled names, ten from each of four samplers. Mark **R** (I could imagine meeting someone with this name) or **X** (I could not). One second each, and no talking until all forty are marked.

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| | | | | | | | | | |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| | | | | | | | | | |

| 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| | | | | | | | | | |

| 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| | | | | | | | | | |

After your teacher reads the reveal, fill in (your `R` count comes from your marks; the "in the 231" count comes from the reveal):

| Sampler | My `R` count (of 10) | Names in the 231 (of 10) | Boring, balanced or rambling? |
|---|:--:|:--:|---|
| A `T = 0.5` | | | |
| B `T = 1.0` | | | |
| C `T = 1.5` | | | |
| D top-p 0.9 | | | |

Which sampler got the most `R`s? ____________ . Which gave the most names that are **not** in the 231? ____________ . Are those the same sampler? ☐ yes ☐ no. **Ten names a sampler is a sample, not a finding.** One sentence on what you would need to be sure: ___________________________________________

---

## 🧭 Page 13.4 — How Far Can the Memory Reach? and the Model Grading Itself (20 min)

### Part A. The copy-task delay sweep (the assigned task)

The task: five symbols out of eight are shown, then **D** filler steps, then the model must write the same five symbols again. To get them right across the gap, the model has to **carry** them. **Chance** is guessing one symbol out of eight each time.

1. Chance is ____________ (a decimal to three places).
2. **Predict first.** Which one, `nn.RNN` or `nn.LSTM`, will stay above chance across a longer gap? ____________ . At what gap do you think it falls to chance? ____________

Now run `copytask.py` (about **33 seconds**, ten short training runs; read the table, not the clock). Write what it prints. Each number is the share of copied symbols that came out right.

| Gap D | 1 | 5 | 10 | 20 | 40 |
|---|:--:|:--:|:--:|:--:|:--:|
| `nn.RNN` | | | | | |
| `nn.LSTM` | | | | | |

3. The RNN falls to chance (within about 0.01 or 0.02 of your Part 1 answer) at D = ____________ . The LSTM falls to chance at D = ____________ .
4. The RNN scored ____________ at D = 1. Is "the RNN cannot remember at all" a fair sentence? ☐ yes ☐ no. Why? ___________________________________________
5. This was **one seed** and **1,500 training steps** at hidden size 64. Write one sentence of caution about reading a cliff off these ten numbers: ___________________________________________

### Part B. Predict before `exposure.py`

The model is given a name and the **true** previous letters, and asked how surprised it is by each next letter (the loss per letter; lower means less surprised).

**Which scores worse on average: the 231 real names, or 200 names the model made itself at `T = 1`?** Circle: **real names · its own names · the same**. Your reason, in one sentence: ___________________________________________

Run `exposure.py` and fill in:

| | mean loss per letter | share of names above 1.5 |
|---|:--:|:--:|
| 231 real names | | |
| 200 own names, `T = 1.0` | | |
| 200 own names, `T = 0.5` | | |

Was your prediction right? ☐ yes ☐ no. The `T = 1` gap (own minus real) is ____________ . The `T = 0.5` gap is ____________ .

![Two rows of letter boxes, one fed the true letters and one fed its own unlikely letter, above three bars of loss per letter: 0.954 for real names, 1.122 and 0.920 for the model's own](../figures/fig-w13-2-exposure-bias.svg)
*Figure 13.2 — The model is more surprised by its own names than by real ones; that fits exposure bias but does not prove it.*

---

## 🪞 Page 13.5 — Exposure Bias in Two Sentences, and a Temperature of Zero (10 min)

### Part A. Exposure bias

Write it in **two sentences**. The first says **what the mechanism is** (what is the model fed in training, and what is it fed when it generates?). The second quotes **today's measurement with its numbers and one honest caution** (what else could make its own names score worse?).

Sentence 1: ___________________________________________

___________________________________________

Sentence 2: ___________________________________________

___________________________________________

**Check your wording.** Did you write "consistent with" or "suggests", and not "proves"? ☐ yes ☐ no. The `T = 0.5` line closed the gap. Name **two** stories that fit that one number: (1) ___________________________________________ (2) ___________________________________________

### Part B. A temperature of zero (on paper, then run `check135.py`)

A friend sets `T = 0.0` "to make it greedy". The scores are `2, 1, 0`.

1. By hand: `2 / 0.0 =` ____________ , `1 / 0.0 =` ____________ , `0 / 0.0 =` ____________ (write **a number**, **infinity**, or **not a number**).
2. Softmax of a row that holds those values will give: ___________________________________________

Type and run `check135.py` (**deliberately broken**: it divides by zero on purpose, and only prints) and copy the two lines:

```python
# check135.py - DELIBERATE: a temperature of zero.
import torch
import torch.nn.functional as F

scores = torch.tensor([2.0, 1.0, 0.0])
print(scores / 0.0)
print(F.softmax(scores / 0.0, dim=-1))
```


```text
line 1:
line 2:
```

3. What should your friend write instead, to get greedy without dividing by zero? ___________________________________________

---

## 🐞 Page 13.6 — Break It on Purpose (15 min)

Three programs, **each deliberately broken**. Do **not** run them first. For each: write **(i)** the bug, **(ii)** what you think will happen when it runs (loud error, or quietly wrong?), **(iii)** the fixed line. *Then* run it.

**The reading method:** for a loud bug, read the **last line** of the error, then find **your own file's** line just above it. For a **silent** bug, there is no error: you must check a property that has to be true (rows add to 1; changing `T` changes the answer).

**Bug 13.6-A (SILENT).** Three rows of scores, one row per next-letter choice. Predict **what the row sums are**.

```python
# DELIBERATE BUG 13.6-A (SILENT): softmax over the wrong axis on a batch of three score rows.
import torch
import torch.nn.functional as F

scores = torch.tensor([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 2.0, 0.0, 0.0],
                       [0.0, 0.0, 0.0, 0.0]])       # three rows: three different next-letter choices
p = F.softmax(scores, dim=0)
print(p)
print("row sums:", p.sum(dim=-1))
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 13.6-B (SILENT).** The programmer wants `T = 0.2` to be sharp and `T = 5.0` to be flat. The code prints **two lines**. Predict both before you run.

```python
# DELIBERATE BUG 13.6-B (SILENT): temperature applied AFTER the softmax.
import torch
import torch.nn.functional as F

scores = torch.tensor([3.0, 1.0, 0.0])
def shares(T, n=10000):
    torch.manual_seed(0)
    p = F.softmax(scores, dim=-1) / T
    draws = torch.multinomial(p, n, replacement=True)
    return [round(float((draws == i).float().mean()), 3) for i in range(3)]
print("T=0.2 :", shares(0.2))
print("T=5.0 :", shares(5.0))
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 13.6-C (loud).** Top-p with `p = 0.7` on scores `4, 1, 0`. Predict **how many letters** are kept.

```python
# DELIBERATE BUG 13.6-C (loud): top-p with "running total < p" instead of "total ABOVE this letter < p".
import torch
import torch.nn.functional as F

p = F.softmax(torch.tensor([4.0, 1.0, 0.0]), dim=-1)
sorted_p, order = torch.sort(p, descending=True)
print("sorted:", [round(float(x), 3) for x in sorted_p])
kept = sorted_p * (torch.cumsum(sorted_p, dim=-1) < 0.7)
print("kept  :", kept)
print(order[torch.multinomial(kept, 1)])
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**After running all three:** for the two silent ones, write the **one check** that would have told you something was wrong, *without* reading the code: ___________________________________________

---

## 📓 Page 13.7 — The Bug Log

**Entry 1: the prediction I got most wrong this week.** *"I thought ______________, but ______________."* (Candidates: greedy's name count, the exposure gap, the LSTM's gap, top-p 0.5.)

_______________________________________________________________________________

**Entry 2: a slip, not a gap.** Find one place where you **knew** the method and lost the answer to arithmetic (a swapped letter, `T` divided too late, a total that did not add to 1). The **one habit** that would have saved it: ___________________________________________

**Entry 3: the silent ones.** Bugs 13.6-A and 13.6-B **ran without an error**. In your own words, why is a silent bug more dangerous than a loud one, and what two cheap checks did this week give you? ___________________________________________

**Entry 4: "new" is not "good".** Write the one sentence you would say to a friend who says "the sampler with the most new names is the best name maker": ___________________________________________

**Entry 5: the rule I will follow next week.** One sentence about a habit, not a topic: ___________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (do this last, from memory)

Tick only if you could do it **now**, without scrolling up.

- ☐ Say what the model outputs, and how a program turns it into one letter.
- ☐ Write the line that turns scores at temperature `T` into chances, with the right axis.
- ☐ Say what happens to the best letter's chance as `T` grows, and what happens at `T` very close to 0.
- ☐ Do top-k and top-p by hand on four scores, and say why the top letter always survives top-p.
- ☐ Say why 200 copies of one name is not a name generator, and why 118 "new" names is not a good one either.
- ☐ Explain exposure bias in two sentences and say what the measurement does **not** prove.
- ☐ Say which of `nn.RNN` and `nn.LSTM` reached further on the copy task, with the word "here" (one seed, one budget).

**Ticks:** ______ / 7 . **The one I could not tick, and when I will redo it:** ___________________________________________

**Next week.** Week 14 is **Attention by Hand**. The `F.softmax` you typed today comes back with a different job: deciding how much each earlier word counts. The one new idea is a weighted average, where the weights add to 1. **Bring a pen and a calculator.**

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact to three decimals. Last digits may differ on another CPU or PyTorch build; a count of new names can move by a name or two. Only mark the *reasoning* as wrong if the number is far off.

### Warm-Up

**W1.** **One score per letter.** **W2.** **Last** axis. **W3.** **Bigger** (a bigger `T` makes the scores closer together). **W4.** **Highest** score, **no** randomness. **W5.** A fixed-size summary (the "note", the hidden state) of everything read so far; any honest sentence that says it is passed from step to step.

### Page 13.1

**A.** One name is the answer the model gives: 1 distinct out of 200, because greedy has no randomness and the same scores give the same choice every time. (The model's name is `andrei`.) A guess of "lots" is the common wrong guess; mark the reason, not the number.

**B.** Expected directions against `T = 1.0`: greedy, **fewer** distinct, **fewer** new. `T = 0.5`: fewer, fewer. `T = 1.5`: **more**, **more**. Top-k 5: fewer, fewer. Top-p 0.9: fewer, fewer.

**C.** From `namegen.py` (seed 0, 200 names each; the model's final loss prints `1.026`):

| Sampler | distinct / 200 | new / 200 | One word (accept others with a number) |
|---|:--:|:--:|---|
| greedy | 1 | 0 | repeats (`andrei` 200 times) |
| `T = 0.5` | 111 | 2 | recites |
| `T = 1.0` | 155 | 32 | balanced |
| `T = 1.5` | 192 | 118 | rambles |
| top-k 5 | 73 | 18 | narrow |
| top-p 0.9 | 128 | 7 | careful |
| `T = 1.5` + top-p 0.9 | 159 | 50 | hot, with the tail cut |

**The direction is what matters:** more temperature, more distinct and more new; cutting the tail at the same temperature brings both down (`T = 1.5` gives 192 and 118; adding top-p 0.9 brings them to 159 and 50).

**D.** Any row, with a stated meaning of "best". A good answer notes that *new* is a count and *best* is a judgement you make by reading.

### Page 13.2

**Worked example check:** the `m o p` table above was run: `T=1.0: m=0.6652 o=0.0900 p=0.2447`. At `T = 0.5` it gives `m=0.8668 o=0.0159 p=0.1173`, and at `T = 4.0`, `m=0.4192 o=0.2543 p=0.3265`.

**Part A.**

| Letter | score | `T=1` exp | `T=1` chance | score ÷ 2 | `T=2` exp | `T=2` chance |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| a | 0.0 | 1.000 | 0.076 | 0.0 | 1.000 | 0.138 |
| b | 2.0 | 7.389 | 0.563 | 1.0 | 2.718 | 0.375 |
| c | -1.0 | 0.368 | 0.028 | -0.5 | 0.607 | 0.084 |
| d | 1.0 | 2.718 | 0.207 | 0.5 | 1.649 | 0.227 |
| e | 0.5 | 1.649 | 0.126 | 0.25 | 1.284 | 0.177 |

The `T = 2` total is **7.258** (1.000 + 2.718 + 0.607 + 1.649 + 1.284 = 7.258). The best letter is `b` at both; its chance went **down** (0.563 to 0.375). A value within 0.001 of these is fine; small rounding differences come from using three-digit `exp` values.

**Part B.** The best letter is `e` at every `T` (temperature changes how much it wins by, not who wins). Up or down against `T = 1`: `T = 0.3` **up**; `T = 2` **down**. Measured:

| T | s | t | a | r | e | best letter's share |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.3 | 0.034 | 0.006 | 0.000 | 0.000 | 0.959 | 0.959 |
| 1.0 | 0.214 | 0.130 | 0.048 | 0.029 | 0.580 | 0.580 |
| 2.0 | 0.234 | 0.182 | 0.111 | 0.086 | 0.386 | 0.386 |

(The `exp` values at `T = 1` are `4.4817, 2.7183, 1.0, 0.6065, 12.1825`, total `20.989`; `12.1825 / 20.989 = 0.580`.) A wrong prediction that is honestly recorded and corrected is a good answer to this page.

**Part C.** With `torch.manual_seed(0)` and 10,000 draws from the `T = 1` chances the printed shares are `s=0.208 t=0.131 a=0.048 r=0.030 e=0.583`, against the table's `0.214 0.130 0.048 0.029 0.580`. **Close, not identical:** a draw is random, and 10,000 draws land near the chances but not exactly on them. A different seed gives slightly different shares.

**Part D.** The ratio of best to worst is `22026.5` at `T = 0.3`, `20.1` at `T = 1`, and `4.5` at `T = 2`. Each equals `e^(3.0 / T)`. The gap between the biggest and smallest score, divided by `T`, is all that decides how lopsided the chances are between those two letters: dividing the scores by `T` scales the gap by the same amount.

### Page 13.3

**Part A.** Top-k keeps the **k** letters with the **highest** scores. Top-p keeps a letter if the total of the letters above it is **less than** `p`.

**Part C.** `exp` total: 7.389 + 2.718 + 1.649 + 1.000 = **12.756**.

| Letter | 1st | 2nd | 3rd | 4th |
|---|:--:|:--:|:--:|:--:|
| chance | 0.579 | 0.213 | 0.129 | 0.078 |
| running total | 0.579 | 0.792 | 0.922 | 1.000 |
| total above | 0.000 | 0.579 | 0.792 | 0.922 |

1. **Top-2:** `0.579 / 0.792 = 0.731` and `0.213 / 0.792 = 0.269`.
2. **Top-p 0.9:** the first **three** (the total above the third is 0.792, which is below 0.9; above the fourth it is 0.922, which is not). Re-shared: `0.629, 0.231, 0.140`.
3. **Top-p 0.5:** the **first letter only**. Above the first there is nothing (0 is below 0.5); above the second the total is 0.579, which is not below 0.5. **A student who wrote two letters used the total *including* the letter, which is the bug on page 13.6-C.**
4. **One letter.** The top letter has nothing above it, so its test is always "0 is less than `p`", which is true for any `p` above 0.

**Check-file output** (`check133.py`; the first `probs` list is in the letters' own order, and the `top-p` lists are in sorted order):

```text
worked probs : [0.032, 0.087, 0.644, 0.237]
  top-2 at : ['y', 'z']  kept: [0.731, 0.269]
  sorted   : [0.644, 0.237, 0.087, 0.032] ['y', 'z', 'x', 'w']
  running  : [0.644, 0.881, 0.968, 1.0]
  before   : [0.0, 0.644, 0.881, 0.968]
  top-p 0.8 : [0.731, 0.269, 0.0, 0.0]
  top-p 0.5 : [1.0, 0.0, 0.0, 0.0]
yours  probs : [0.579, 0.213, 0.129, 0.078]
  top-2 at : ['1', '2']  kept: [0.731, 0.269]
  sorted   : [0.579, 0.213, 0.129, 0.078] ['1', '2', '3', '4']
  running  : [0.579, 0.792, 0.922, 1.0]
  before   : [0.0, 0.579, 0.792, 0.922]
  top-p 0.9 : [0.629, 0.231, 0.14, 0.0]
  top-p 0.5 : [1.0, 0.0, 0.0, 0.0]
  top-p 0.01 : [1.0, 0.0, 0.0, 0.0]
```

**Part D.** No fixed answer: your marks. The pattern to expect: the lowest-temperature sampler gets nearly all `R`s and the fewest new names (it is also the most boring); the hottest one gets several `X`s (strings like `inditrr` and `nnanvir`) and the most new names; top-p 0.9 often gets nearly as many `R`s as `T = 0.5`, and it is **not** the same ten names repeated. "Most `R`s" and "most new" are usually **different** samplers: that is the lesson. To be sure of a difference, you would need many more than ten names per sampler, and more than one judge.

### Page 13.4

**Part A.** 1. Chance = **0.125** (one in eight). 2. Any honest prediction. The LSTM is designed to protect what it carries; the point of the page is to measure it.

The printed sweep (seed 0, 1,500 steps, hidden size 64):

```text
rnn D=1 1.000  D=5 0.384  D=10 0.129  D=20 0.127  D=40 0.127
lstm D=1 0.996  D=5 0.987  D=10 0.959  D=20 0.130  D=40 0.130
```

| Gap D | 1 | 5 | 10 | 20 | 40 |
|---|:--:|:--:|:--:|:--:|:--:|
| `nn.RNN` | 1.000 | 0.384 | 0.129 | 0.127 | 0.127 |
| `nn.LSTM` | 0.996 | 0.987 | 0.959 | 0.130 | 0.130 |

3. The RNN falls to chance by **D = 10**; the LSTM holds to D = 10 and is at chance by **D = 20**, *at this training budget and size*. Accept the same pattern with each cell up to about 0.05 away (that is noise, not a different result). 4. **No.** The RNN is perfect at D = 1; it fails on longer gaps. "The RNN cannot remember at all" and "the LSTM remembers 40 steps" are both wrong readings. 5. Full marks for a sentence such as: *one seed and 1,500 steps only; a longer training run or a bigger hidden size might move the cliff; the cliff location on ten numbers is approximate.*

**Part B.** Most students predict **its own names**. The measured answer is the opposite. Printed by `exposure.py`:

```text
real names     n=231  mean 0.954  median 0.936
own, T=1.0     n=200  mean 1.122  median 0.957  gap +0.167  worst 2.74  share above 1.5: 0.175
own, T=0.5     n=200  mean 0.920  median 0.908  gap -0.035  worst 2.44  share above 1.5: 0.010
real above 1.5: 0.000
```

The `T = 1` gap is **+0.167** (1.122 against 0.954); the `T = 0.5` gap is **-0.035**. Real names: 0.000 above 1.5; own, `T = 1`: 0.175; own, `T = 0.5`: 0.010. Note the **median** moves very little (0.957 against 0.936): the extra surprise is concentrated in a minority of bad names. Remember the real names are the model's own training names, so this compares a training-set score with the model's score on its own samples.

### Page 13.5

**Part A. Model answer.** *"The model is trained only on true previous letters, but when it generates it is fed its own letters, which it never practised on. Measured: it scores its own `T = 1` names at 1.122 per letter against 0.954 for real names, with 17.5% of its own names above 1.5 and none of the real ones, which is consistent with drift, though sampling unlikely letters on purpose and reciting memorised names at low temperature also move the number."* Mark sentence 1 for the mechanism and sentence 2 for the numbers and the caution. **Do not give full marks to "proves".**

The two stories that fit the closed gap at `T = 0.5`: (1) at low temperature it makes fewer wrong turns, so there is less drift; (2) at low temperature it is simply **reciting names it has seen** (only 2 of 200 names were new), and those score well. One number, two stories: we say what we measured.

**Part B.** 1. `2 / 0.0 =` **infinity**, `1 / 0.0 =` **infinity**, `0 / 0.0 =` **not a number**. 2. A row with infinity and not-a-number in it gives a row of **not-a-number** (there is no meaningful answer). Printed by `check135.py`:

```text
tensor([inf, inf, nan])
tensor([nan, nan, nan])
```

3. Use the **greedy** picker (`scores.argmax()`), or a tiny `T` such as 0.01 if you want to keep the same code. A temperature must be above zero: that is the Bug Log lesson. (With `T = 0.01` on these scores the chances are 1, then something below 1e-40, then 0: effectively greedy.)

### Page 13.6

**13.6-A (silent).** The bug: `dim=0` runs **down the columns**; we wanted `dim=-1`. It runs without an error. The printed output:

```text
tensor([[0.5761, 0.1065, 0.3333, 0.3333],
        [0.2119, 0.7870, 0.3333, 0.3333],
        [0.2119, 0.1065, 0.3333, 0.3333]])
row sums: tensor([1.3493, 1.6656, 0.9851])
```

Each **column** adds to 1, but each **row** does not (1.3493, 1.6656, 0.9851). Every number is a good probability, just over the wrong thing. Fix: `F.softmax(scores, dim=-1)`. The check: `p.sum(dim=-1)` must be all ones.

**13.6-B (silent).** The bug: `/ T` is applied to the **probabilities**, not the scores. Dividing every probability by the same number changes none of their *relative* sizes, and `multinomial` only cares about relative sizes (it does not need them to add to 1, which is why it runs without a murmur).

```text
T=0.2 : [0.836, 0.121, 0.043]
T=5.0 : [0.836, 0.121, 0.043]
```

Identical output for two very different `T`, and both are (up to random draw noise) the `T = 1` chances (`0.844, 0.114, 0.042`; the draws gave `0.836, 0.121, 0.043`), not a sharp set. Fix: `F.softmax(scores / T, dim=-1)`. The check: **change `T` and see that the output changes.** (For comparison, the right answer at `T = 0.2` is `[1.0, 0.0, 0.0]` to three decimals.)

**13.6-C (loud).** The bug: the test is "the total *including* this letter is below 0.7", and the top letter alone already holds 0.936. Nothing passes, so there is nothing to draw from.

```text
sorted: [0.936, 0.047, 0.017]
kept  : tensor([0., 0., 0.])
Traceback (most recent call last):
  File "/private/tmp/wb13/b3.py", line 10, in <module>
    print(order[torch.multinomial(kept, 1)])
RuntimeError: invalid multinomial distribution (sum of probabilities <= 0)
```

(The path on your machine will differ.) Fix: compare the total of the letters **above**: `before = torch.cumsum(sorted_p, dim=-1) - sorted_p`, then `kept = sorted_p * (before < 0.7)`. Then `before` is `[0.0, 0.936, 0.983]` and `kept` is `[0.9362, 0.0, 0.0]`: one letter kept, as predicted by the page 13.3 rule (the top letter always passes).

**The checks for the two silent bugs:** rows must add to 1 (`sum(dim=-1)`); and changing `T` must change the answer.

### Page 13.7 and Self-Check

Your own words. A good **Entry 3** says: a silent bug **runs**, prints plausible numbers, and gets reported; so the checks are *properties that must hold* (each row adds to 1; a different `T` gives a different answer). A good **Entry 4** says *new* is a count of strings not in the training list, *good* is a judgement by reading, and the two can point in opposite directions (118 new at `T = 1.5`, many of them not names). A good **Entry 5** is short and about a habit ("change the dial and check the output moves").

**Self-Check:** if you could tick fewer than five, redo pages 13.2 and 13.3 first; they are the two every later week leans on (Week 14 reuses the softmax).
