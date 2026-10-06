# Week 18 — Review and Assessment 2: What Did Term 2 Leave Behind?

[⬅ Week 17](week-17.md) · [Course Home](../README.md) · [Week 19 ➡](week-19.md) · [Workbook](../workbook/week-18.md)

---

![The 36 week tiles in four term lanes; weeks 1 to 17 solid, week 18 tinted pink with a thick border and a pointer above it, weeks 19 to 36 dashed](../figures/fig-w18-0-where-this-fits.svg)
*Figure 18.0 — Week 18 of 36, the Term 2 review and paper, sits at the end of term 2; weeks 1 to 17 are done and weeks 19 to 36 are still ahead.*

> ### This week in one sentence
> **Today's paper is not a grade; it is an X-ray of Weeks 10 to 17. It shows, week by week, what stuck and what did not, so you can redo the right page before Week 19 takes your TinyGPT apart.**
>
> **By the end of this chapter you will be able to:**
> - **Compound a slope by hand** (a number multiplied by itself many times) and say which disease, fading or blowing up, the result is, and which of the two clipping can cure
> - **Turn scores into chances** at a temperature, and say what top-k and top-p keep
> - **Do the attention pass on a new set of numbers**: scores, divide by `sqrt(d)`, hide the future *before* the softmax, weighted average of the values
> - **Count the knobs of one block** and state the first loss a model that knows nothing should score
> - **Read two real tables** (a name model and a TinyGPT) and say what they show, what they do not, and what you would check next
> - **Mark your own paper honestly**, fill in the per-week grid, and circle **at most two weeks** to redo
>
> **New maths:** **none.** **New syntax:** **none.** **New words:** **none.** Everything on the paper is something you have already done with your own hands.
>
> **Reading time:** about 20 minutes (the night before). **In class:** 75 minutes (70 for the paper). **Homework:** about 45 minutes of marking.

> **📌 About the code blocks.** There are only four small files this week, and they are for **before** the paper. Each is a whole file with its name in the first line. Type them into **one folder** and run them from there. They do not need `l4lib/`. Every output shown was printed by a real run on a CPU; **none of them uses randomness**, so no seed is needed and your numbers should match. They use **practice numbers that are not the paper's numbers**, so they check your method without handing you the answers. **You run no code during the paper.** Nothing this week needs the internet. There is no language model, no scripted backend and no stand-in anywhere.

---

## 🪝 Start Here

For nine weeks you have built memory, gates, a name maker, a sampler, attention and a whole TinyGPT. Some of it is probably solid and some of it is probably soft. **You do not know which is which yet.** That is exactly what today finds out.

Three promises about the paper:

1. **It is on paper, with a calculator.** No computer, no notes, no internet.
2. **Every question is about something you did with your own hands.** There are no tricks and nothing from next term.
3. **"Don't know" is a good answer.** Write it. It tells you (and the grid) where to look. A lucky guess hides the problem; an honest "don't know" shows it.

Say this to yourself before you start: *"This is the X-ray, not the grade. Nobody is keeping score but me."*

Why bother before Term 3? Because **Week 19 deletes the parts of your TinyGPT one at a time** (the mask, the positions, the residual road, the layer norm) and watches what breaks. To read that, you need Weeks 15, 16 and 17 to be solid.

---

## 🗺️ What is on the paper

The paper is **75 marks** and you get **70 minutes**.

| Section | What it asks | Marks | About how long |
|:--:|---|:--:|:--:|
| **A** | 20 multiple choice, circle one letter | 20 | 15 min |
| **B** | 8 "what does this print?" (you write the exact output) | 16 | 15 min |
| **C** | 4 "find the bug" (say what the bug is, what happens, write the fix) | 12 | 10 min |
| **D** | 3 pieces of arithmetic (show every line of working) | 15 | 15 min |
| **E** | 1 longer question about two real tables | 12 | 13 min |

**Show your working** in B to E. A wrong number with the right working still earns marks. A right number with no working earns fewer.

**In Section C the programs are broken on purpose.** Your job is to say what the bug is, what the program does (an error, or a wrong answer), and to write the fix.

**Section E is the biggest single question** (12 marks) and the last one. Start it when you have about thirteen minutes left, not later. It uses **two real tables** printed from this course's own runs: the name model of Week 12 and the TinyGPT of Week 17. The tables are on the paper as numbers, so you do not need to remember them.

**Your teacher will say only five things during the paper** (the time-checks), and will answer questions with one of three sentences: *"Read it again."* / *"Write what you do know."* / *"I can't help with that one, move on."* That is not unkindness; it is what keeps the X-ray clean.

---

## 🧰 The night before: what to be able to do

Go down this list. For each line, ask: **could I do this right now with only a pen and a calculator?** Tick the ones you could. For any you could not, open the workbook page named and do it again, **for 20 minutes at most**. Do not try to learn everything the night before; just find out which lines are soft.

| Week | You should be able to... | Workbook pages to look at |
|:--:|---|---|
| 10 | Multiply a slope through a loop (`0.9` forty times) and say roughly what is left. Say which of the two diseases, fading or blowing up, **clipping** can cure, and which it cannot. | 10.1, 10.4 |
| 11 | Say what the slope back through the memory track is, and what number it starts near. Make a dial from a bias with the sigmoid, and say what setting the forget bias to a bigger number does. Say why an LSTM does **not** fix fading by itself. | 11.1, 11.5 |
| 12 | Say what **teacher forcing** is. Read a train-against-validation table and say when validation is worse than knowing nothing (`ln 28`). Say what `ignore_index` does. Build the shifted input for a name with `torch.cat`. | 12.4, 12.5 |
| 13 | Turn scores into chances at a temperature. Keep the top k, or the top-p set (the smallest set whose chances add to at least p). Say what greedy and **exposure bias** mean. | 13.2, 13.3 |
| 14 | Do the three-word attention pass with a pen. Say what each row of weights adds to. Say which of `Wq`, `Wk`, `Wv` does **not** change the weights. | 14.1, 14.4 |
| 15 | Say why the scores are divided by `sqrt(d)`. Build a causal mask, and say why the future is hidden with `-inf` **before** the softmax, not with 0 after. Give the shapes when a width is cut into heads. | 15.2, 15.3 |
| 16 | Say why attention alone cannot tell `dog bit man` from `man bit dog`, and what fixes it. Count the knobs in one block. | 16.2, 16.4 |
| 17 | Say what a model that knows nothing about 28 characters should score at step 0, and why. Say what the gap between train and validation loss does and does not tell you. | 17.3, 17.4, 17.6 |

> **Do not** stay up late. A tired head does the arithmetic worse than a rested one, and one night cannot teach you what nine weeks did not.

---

## 🔥 Warm-ups (optional, 25 minutes, the night before)

These four files check the *method* of four of the by-hand ideas on **practice numbers that are not on the paper**. The rule is the one you use for the paper: **do it by hand first, write your answer down, then run the file.** If you run it first you learn nothing about yourself.

### Warm-up 1 — compounding and a forget dial

On paper: what is `0.95` multiplied by itself 30 times, roughly? Is it closer to 0.2 or to 0.0002? And `1.10` multiplied by itself 30 times? Then: a forget dial is `1 / (1 + e^-bias)`. For a bias of `0`, `1` and `3`, write the dial, and guess how much signal survives **eight** steps. Then run:

```python
# warm1.py - Week 18 warm-up 1: compounding and a forget dial. PRACTICE numbers, not the paper's.
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

print("slope 0.95, 30 steps back:", round(0.95 ** 30, 4))
print("slope 1.10, 30 steps back:", round(1.10 ** 30, 2))
for bias in [0, 1, 3]:
    f = sigmoid(bias)
    print("forget bias", bias, "-> dial", round(f, 4), "-> left after 8 steps", round(f ** 8, 5))
```

```text
slope 0.95, 30 steps back: 0.2146
slope 1.10, 30 steps back: 17.45
forget bias 0 -> dial 0.5 -> left after 8 steps 0.00391
forget bias 1 -> dial 0.7311 -> left after 8 steps 0.08159
forget bias 3 -> dial 0.9526 -> left after 8 steps 0.67794
```

Two slopes very near 1, one on each side, end up in very different places. Which one is fading and which one is blowing up? If you wrote `0.95 x 30 = 28.5` you multiplied instead of compounding; look at the Week 10 chapter again.

![Left, two bars on a log scale: 0.95 compounded 30 times leaves 0.2146 (below the unchanged line), 1.10 leaves 17.45 (above it). Right, three bars for a forget dial: 0.00391, 0.08159 and 0.67794 left after 8 steps.](../figures/fig-w18-1-compounding-and-dials.svg)
*Figure 18.1 — Practice numbers, not the paper's: a slope near 1 fades or blows up when compounded, and a bigger forget bias keeps more signal.*

### Warm-up 2 — scores to chances, and top-p

On paper: scores `[3, 1, 0, -1]`. Dividing by a temperature of `0.5` gives `[6, 2, 0, -2]`. Which way does the top letter's chance move: up or down? Then run:

```python
# warm2.py - Week 18 warm-up 2: scores to chances, and top-p. PRACTICE numbers, not the paper's.
import torch
import torch.nn.functional as F

scores = torch.tensor([3.0, 1.0, 0.0, -1.0])
for temp in [1.0, 0.5, 2.0]:
    p = F.softmax(scores / temp, dim=-1)
    print("temperature", temp, "->", [round(x, 3) for x in p.tolist()])

p = F.softmax(scores, dim=-1)
sorted_p, ids = torch.sort(p, descending=True)
running = torch.cumsum(sorted_p, dim=-1)
print("running total:", [round(x, 3) for x in running.tolist()])
print("kept by top-p 0.9:", int((running < 0.9).sum().item()) + 1, "letters")
```

```text
temperature 1.0 -> [0.831, 0.112, 0.041, 0.015]
temperature 0.5 -> [0.979, 0.018, 0.002, 0.0]
temperature 2.0 -> [0.579, 0.213, 0.129, 0.078]
running total: [0.831, 0.943, 0.985, 1.0]
kept by top-p 0.9: 2 letters
```

Look at the last line. The first letter alone adds up to `0.831`, which is below `0.9`, so it is not enough. The second letter is the one that *crosses* the line, and it is kept too. That is why the code adds `1` after counting the entries below `0.9`.

### Warm-up 3 — the attention pass, with both dials

On paper: three words, `cat = [1, 2]`, `sat = [2, 1]`, `down = [1, 0]`. `Wq` and `Wk` are the identity, so `Q = K = X`. `Wv` doubles the first number. Write `V`, then the table of scores, then (for the **third** row only) divide by `sqrt(2)` and hide the future *before* the softmax. Which words does `down` look at? Then run:

```python
# warm3.py - Week 18 warm-up 3: a three-word attention pass with BOTH dials on. PRACTICE numbers, not the paper's.
# cat = [1, 2], sat = [2, 1], down = [1, 0]. Wq and Wk are the identity, Wv doubles the first number.
import math
import torch
import torch.nn.functional as F

X = torch.tensor([[1.0, 2.0], [2.0, 1.0], [1.0, 0.0]])
Wv = torch.tensor([[2.0, 0.0], [0.0, 1.0]])
V = X @ Wv
scores = X @ X.transpose(-2, -1)
print("scores:", scores.tolist())
scaled = scores / math.sqrt(2)                                   # dial 1: divide by sqrt(d), d = 2
future = torch.tril(torch.ones(3, 3)) == 0
hidden = scaled.masked_fill(future, float("-inf"))               # dial 2: hide the future BEFORE the softmax
weights = F.softmax(hidden, dim=-1)
print("weights:", [[round(x, 4) for x in row] for row in weights.tolist()])
print("row sums:", [round(x, 4) for x in weights.sum(dim=-1).tolist()])
print("output:", [[round(x, 3) for x in row] for row in (weights @ V).tolist()])
```

```text
scores: [[5.0, 4.0, 1.0], [4.0, 5.0, 2.0], [1.0, 2.0, 1.0]]
weights: [[1.0, 0.0, 0.0], [0.3302, 0.6698, 0.0], [0.2483, 0.5035, 0.2483]]
row sums: [1.0, 1.0, 1.0]
output: [[2.0, 2.0], [3.34, 1.33], [3.007, 1.0]]
```

Check the row sums first: if yours do not add to 1 the error is in the softmax step, not in the blend. The first word can see only itself, so its weight is exactly `1.0`. Carry four decimal places in the weights and round only the answer.

![Left, a 3 by 3 grid of attention weights for cat, sat, down with the hidden future struck through and each row summing to 1.0. Right, the down row blending three value rows with weights 0.2483, 0.5035, 0.2483 into the output 3.007, 1.0.](../figures/fig-w18-2-practice-attention-pass.svg)
*Figure 18.2 — Practice numbers, not the paper's: scores become weights that sum to 1, hide the future, and blend the value rows.*

### Warm-up 4 — count a block, and the first-loss number

On paper: one block at width `d = 12` has two layer norms (a scale and a shift each), `q`, `k`, `v` with **no** bias, a `proj` with a bias, and an `up`/`down` pair at four times the width, both with biases. Count each group, add them up, then try the Week 16 formula. Also: what should a model that knows nothing about a **10**-symbol alphabet score on its first try? Then run:

```python
# warm4.py - Week 18 warm-up 4: count a block, and the first-loss number. PRACTICE numbers, not the paper's.
import math
import torch.nn as nn

d = 12
pieces = {
    "two layer norms": [nn.LayerNorm(d), nn.LayerNorm(d)],
    "q, k, v (no bias)": [nn.Linear(d, d, bias=False) for _ in range(3)],
    "proj": [nn.Linear(d, d)],
    "up and down": [nn.Linear(d, 4 * d), nn.Linear(4 * d, d)],
}
total = 0
for name, layers in pieces.items():
    n = sum(p.numel() for layer in layers for p in layer.parameters())
    total += n
    print(f"{name:20s} {n}")
print("block at d = 12:", total, " formula 12d^2 + 10d:", 12 * d * d + 10 * d)
print("first loss for a 10-symbol alphabet, ln(10):", round(math.log(10), 3))
```

```text
two layer norms      48
q, k, v (no bias)    432
proj                 156
up and down          1212
block at d = 12: 1848  formula 12d^2 + 10d: 1848
first loss for a 10-symbol alphabet, ln(10): 2.303
```

The pieces are kept in a plain dictionary here only to add them up; this file is not a model, so the Week 16 warning about plain lists does not apply. If your total is `12 x 144 = 1,728`, you forgot the `10d` of biases and norms.

---

## 🎲 During the paper

A few habits, in order of how many marks they save.

1. **Do Section A first and fast.** It is 20 one-mark questions; do not spend five minutes on one of them. Circle your best guess and move on. A blank earns nothing.
2. **In Section B, work it out, don't "see" it.** Run the program in your head one line at a time and write each intermediate value beside the code. Write the number exactly as the program would print it, including a trailing zero.
3. **In Section C, answer all three parts.** (i) what the bug is, (ii) what happens when it runs (an error, and what its last line means, or a wrong result), (iii) the fixed line. Some bugs here print an answer without any error. Ask what should be *true* of the output, and check it.
4. **In Section D, write every line.** The marks are for the working. Four decimal places, as the paper says.
5. **In Section E, quote a number.** "It is bad" earns little. "The validation loss goes from 1.417 to 1.437" earns the mark. Name which table and which step you are describing. When a question asks what a score *measures and does not measure*, say both halves.
6. **If you finish early,** go back and check each answer against your own working, **starting from the end**. Do not leave, and do not start next week.
7. **If you get stuck,** write *"did not get it"* beside the question and go on. That is the most useful thing you can write.

> **If you feel panicky:** put the pen down, breathe for a minute, and say so. A calm minute costs a mark or two and gives them back.

---

## 📤 Homework: mark your own paper

You will be given the **marking sheet** (the short answers, with working) and a pen of a **different colour** from the one you used on the paper. Do this the same evening.

1. **Mark your paper in the other colour.** In A, B and C the answers are checkable, so be strict. In D and E, mark the **working**, not only the final answer: the sheet tells you how many marks each step earns. *(About 30 minutes.)*
2. **Fill in the per-week grid.** For each of the eight weeks (10 to 17), write the marks you earned, the marks available, and the percentage. The sheet tells you which questions belong to which week. *(About 5 minutes.)*
3. **Circle at most two weeks** in the remediation table below. Choose the **lowest percentages**. If there is a tie, go in this order: **Week 16, then Week 15, then Week 17** (those three are the ones Week 19 leans on directly). Write a day and a time for each redo next to the circle. *(About 5 minutes.)*
4. **One sentence in your Bug Log:** *"The answer I was most surprised to get wrong was ___, because I thought ___."* *(About 5 minutes.)*

**Why at most two?** Because a list of eight redos is a list nobody does. Two is a plan.

**A week needs a redo when you scored 60% or less of its marks.** The marking sheet says the exact number of marks for each week.

### The remediation table

Each redo is **20 minutes**, followed by your teacher asking you one question out loud (no paper) to check it landed. The question is in the third column; the answer is for you to say, not to read.

| Week | Redo this (20 min) | The spoken check | Why Term 3 needs it |
|:--:|---|---|---|
| 10 | Workbook **page 10.1** (compounding by hand) and **page 10.4** (the grid: read the shape of each row) | *A slope of 0.9 for forty steps: roughly what is left? Which of the two diseases can clipping cure?* | Week 21's scaling line and every "why does this train badly" question use compounding. |
| 11 | Workbook **page 11.1** (dials by hand) and **page 11.5** (three seeds and the forget bias) | *What is the slope back through the memory track, and roughly what number is it at the start of training?* | The gate is Week 6's residual road in a loop; Week 19 deletes the residual. |
| 12 | Workbook **page 12.4** (train against validation) and **page 12.5** (the name audit) | *Validation 3.417, `ln 28` 3.332. What does that mean?* | The train-against-validation reading returns in Weeks 17, 19 and 21. |
| 13 | Workbook **page 13.2** (scores to chances at three temperatures) and **page 13.3** (top-k and top-p by hand) | *What does a low temperature do to the top letter's chance? What does top-p 0.9 keep?* | Every generation from Week 17 on is a choice rule. |
| 14 | Workbook **page 14.1** (the pen pass) and **page 14.4** (a second pass by hand) | *Which of `Wq`, `Wk`, `Wv` does not change the weights, and why?* | **Week 19 reads head heatmaps**; those are these weights. |
| 15 | Workbook **page 15.2** (variances add; a softmax before and after) and **page 15.3** (the four settings; the mask built by hand) | *Mask before or after the softmax, and with `-inf` or with 0?* | **Two of the four parts Week 19 deletes.** |
| 16 | Workbook **page 16.2** (the seat swap) and **page 16.4** (count the knobs of one block) | *Why can attention alone not tell `dog bit man` from `man bit dog`, and what fixes it?* | **The other two parts Week 19 deletes** (positions and the block's layout). |
| 17 | Workbook **page 17.3** (count the model), **page 17.4** (the first-loss check), then **page 17.6** (what the gap means) | *What should the loss be at step 0 for 28 characters, and why?* | The first-loss check is how Week 19 decides that taking a part out of the GPT broke something. |

**One extra redo is always on offer** for Weeks 14, 15 or 16: the three-word attention pass on a **new** set of numbers, which your teacher has. Doing it once more, with a pen, is the fastest way to make it stick.

Bring to the next class: **the marked paper, the filled grid, and the circled table.** No new code. If you have already redone a page, lovely; nobody requires it.

> **A word on a low mark.** If the total is lower than you hoped, look at the *pattern*, not the number. One week with 30% and seven with 90% is a very different X-ray from eight weeks at 65%, and it is a much easier fix.
>
> **A word on words from later.** If you wrote "ablation" or "scaling law" in an answer because you have read ahead, that is not wrong and not extra; it is from next term. Your teacher will say so on the sheet.
>
> **A word on Section E.** Whatever you wrote, keep this in mind for later: a score for "real words" is a spelling check, not a test of understanding, and one run is one sample. That is why the question asks what you would check *next*.

---

## 📖 What carries into next week

**Week 19 opens the GPT you built in Week 17.** You delete each component in turn (the mask, the positions, the residual, the layer norm) and watch what breaks, then give it small made-up tasks (copy, reverse, lookup) so that a head is easy to name. It leans directly on three things from this paper: the mask and the divide (Week 15), positions and the block's layout (Week 16), and the first-loss check and the train-against-validation reading (Week 17). **If your grid shows Week 16, 15 or 17 under 60%, those are the redos to do first.** Nothing else from Term 2 is on the critical path.

---

## 📖 Words from this week

There are none. No word is new today. If you met a word on the paper that you did not recognise, write it in your Bug Log with the question number: that is a finding for the grid.

---

[⬅ Week 17](week-17.md) · [Course Home](../README.md) · [Week 19 ➡](week-19.md) · [Workbook](../workbook/week-18.md)
