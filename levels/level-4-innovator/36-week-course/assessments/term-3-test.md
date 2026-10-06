# 📝 Term 3 Test — Weeks 19–26: How It Is Made, How It Is Asked

[⬅ Course home](../README.md) · [⬅ Term 2 test](term-2-test.md) · Term 3 of 4 · covers Weeks 19–26 (Week 27 is the review week)

---

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │   AI ACADEMY · LEVEL 4 INNOVATOR                                     │
   │   TERM 3 TEST — How It Is Made, How It Is Asked                      │
   │   Covers Weeks 19–26. Nothing later appears anywhere on this test.   │
   │                                                                      │
   │   PART 1 · THE PAPER           70 minutes      75 marks              │
   │   PART 2 · THE DEMO            15 minutes      15 marks              │
   │                                                                      │
   │   Section A   20 multiple choice          1 mark each     20 marks   │
   │   Section B    8 "what does this print"   2 marks each    16 marks   │
   │   Section C    4 "find the bug"           3 marks each    12 marks   │
   │   Section D    3 "do the arithmetic"      5 marks each    15 marks   │
   │   Section E    1 longer question on 3 real tables         12 marks   │
   │                                                                      │
   │   PART 1:  ⛔ NO COMPUTER.   ✅ A CALCULATOR, YES.                  │
   │   PART 2:  ✅ A COMPUTER AND YOUR OWN WEEK 19–26 FILES. NO NETWORK. │
   │                                                                      │
   │      This is the term of logs, sigmoids and cosines. Check NOW      │
   │      that your calculator has ln, log, e^x and a power key (y^x).   │
   │      A missing button costs real marks.                             │
   │                                                                      │
   │   SUGGESTED TIME   A 15 · B 15 · C 10 · D 17 · E 13 minutes         │
   │                                                                      │
   │   INSTRUCTIONS FOR THE PAPER                                         │
   │   · Pencil. Answer every question. "Don't know" is allowed and       │
   │     costs nothing extra; a blank tells nobody anything.              │
   │   · Section A: circle ONE letter. If you guessed, write "not sure".  │
   │   · Section B: write EVERY line the program prints, in order,        │
   │     exactly as Python prints it (brackets, quotes, trailing zeros).  │
   │   · Section C: say (i) what is wrong, (ii) what happens when it      │
   │     runs, (iii) the fixed line.                                      │
   │   · Section D: show every line of working. Carry FOUR decimal        │
   │     places through a chain and round only at the end.                │
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
> **What this file is.** The Week 27 review week already contains a paper (in that week's own guide).
> **This is a second paper of the same shape with every number and every question different**: a fresh
> item on each topic, no question repeated. Use it as the formal Term 3 test, as the re-sit after the
> remediation fortnight, or as practice. It is **not** a replacement: the Week 27 paper is the one the
> student self-marks. Week 27 is the review week, so this test covers Weeks 19–26.
>
> **You do not need to know Python, calculus or machine learning to run or mark this.** The answer key
> at the bottom gives every answer, every piece of working, and the *real printed output* of every code
> block. Compare, do not work out.
>
> **What "real" means here.** Every code block on this file, on the paper and in the key, was run from a
> scratch folder on a CPU, one thread (`torch.set_num_threads(1)` where torch is used), Python 3.10.10,
> torch 2.2.1, numpy 1.26.4, scikit-learn 1.7.1, with the seeds shown, and the output pasted in
> unedited (a traceback has its file path shortened; one warning is described, not pasted). The code
> came from the course's own student guides: Week 17's `tinygpt.py` (for Week 21's trainer), Week 19's `ablate_model.py` and
> `text_ablate.py`, Week 20's `bpe.py`, Week 21's `textpool.py` and `trainer.py`, Week 23's `bench.py`
> and `guard.py`, and the course's `l4lib/` folder on the path. **The three tables in Section E are
> printed numbers: print them, do not regenerate them on the day.** Two of them depend on the machine.
> Table 1 can move in its last digit on another CPU. **Table 2 depends on which text is in the Python
> install**: Week 21's pool is every `.py` file in the Python library folder, so on another computer the
> pool, the vocabulary size and therefore the knob counts and losses all differ. The tables in this
> file were made on a pool of 4,644,415 characters with 213 different characters.
>
> **Two things on this test are stand-ins, not models.** Wherever the paper meets `FakeClient` (Week
> 23) or the sentence-copying writer behind `rag.rag_answer` (Week 26), it says *"stand-in, not a
> model"*. Nothing scored against them says anything about a real model. Every network on this test
> is real PyTorch, built from the course's own files and trained on a CPU.
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

**A1.** [W19] In a table of five retrained TinyGPTs, the row "no residual" shows `train 2.84, validation 2.85, gap 0.01`. The best reading is:

- (a) It is the best model in the table, because its gap is the smallest
- (b) It has hardly learned anything: both numbers are bad, so they agree
- (c) It has memorised the training text, so the validation number is a fluke
- (d) Removing the residual road makes overfitting impossible, which is a good thing

---

**A2.** [W19] On a trained model, switching off layer-0 head 0 leaves the copy accuracy at `1.00`. Switching off layer-0 head 1 also leaves it at `1.00`. Switching off **both** drops it to `0.50`. The best reading is:

- (a) Neither head matters for the task
- (b) Head 0 is the copier and head 1 does nothing
- (c) Either head can do the job alone, so neither is necessary on its own, but the two together are
- (d) The switch-off test is broken, because switching off two things cannot give a different result from switching off one

---

**A3.** [W19] When should a head be switched off to find out what it was worth?

- (a) After training, on a model that learned with it in place
- (b) Before training, so the model never gets used to it
- (c) Half-way through training, so you can compare before and after in one run
- (d) At any time: the order makes no difference to what you learn

---

**A4.** [W20] You call `train(text, 1000)` and the tokenizer reports `400` merges learned. Why?

- (a) A bug: it should always learn what it is asked for
- (b) 400 is the biggest number of merges the function allows
- (c) The vocabulary of 556 pieces was full
- (d) Training stops by itself when no pair of neighbours occurs at least twice

---

**A5.** [W20] A tokenizer that learned **zero** merges passes every round-trip test (`decode(encode(s)) == s`). What does that show?

- (a) That it compresses text well
- (b) That nothing was lost, and nothing at all about whether the tokens are any good
- (c) That bytes are the wrong thing to start from
- (d) That the tests are too hard to be useful

---

**A6.** [W21] A line on log-log paper (loss against knobs) has slope `-0.30`. You make the model **100 times** bigger. By about what number is the loss multiplied?

- (a) 0.70, a loss of 30% less
- (b) 0.25
- (c) 0.30
- (d) 0.03

---

**A7.** [W21] A duplicate-line remover fingerprints each line with `md5` and drops any line whose fingerprint it has already seen. It keeps both `the river ran.` and `The river ran.`. Why?

- (a) `md5` is broken for capital letters
- (b) It is a bug in the loop, not in `md5`
- (c) `md5` only calls two lines the same when they are exactly the same text, so a near-copy gets a completely different fingerprint
- (d) Lines shorter than 20 characters cannot be fingerprinted

---

**A8.** [W21] Using `C = 6ND`: a model's knobs `N` are made **2 times** bigger and the number of characters it reads `D` is made **3 times** bigger. The compute is multiplied by:

- (a) 6
- (b) 5
- (c) 9
- (d) 36

---

**A9.** [W22] A reward model gives answer A a reward of `3` and answer B a reward of `1`. Someone adds `10` to **every** reward. What changes?

- (a) The chance that A is preferred to B
- (b) The pair loss for (A beats B)
- (c) Which of the two ranks first
- (d) Only the rewards themselves: every chance, loss and ranking is the same

---

**A10.** [W22] At the end of a DPO toy run the policy's KL from the reference is `0.0000`. You know that:

- (a) The policy has reached the best possible answer
- (b) The loss must also be 0
- (c) The policy's table of chances is the same as the reference's: nothing has moved
- (d) The leash `beta` was too small

---

**A11.** [W22] The same pair of answers has moved by the same amount in two DPO runs. One run has `beta = 0.1`, the other `beta = 1.0`. In the second run:

- (a) The margin is ten times bigger, the loss is smaller, and the gradient is quieter, so the model stops moving sooner
- (b) The margin is the same, because the movement is the same
- (c) The loss is bigger, so the model is pushed further
- (d) The model is forced to stay exactly at the reference

---

**A12.** [W23] On a frozen set of 8 messages (32 boxes) a prompt gets 20 boxes right. The best constant answer (the floor) gets 17. The best reading is:

- (a) The prompt is clearly better: it scores 62.5% against 53.1%
- (b) The prompt is ahead by three boxes of 32 on eight messages, which is too little to call a real difference
- (c) The prompt is worse, because a constant never makes a mistake
- (d) The floor does not matter once a prompt scores over 50%

---

**A13.** [W23] Why does `run_suite` start by calling `check_frozen(cases)`?

- (a) To make the loop run faster
- (b) To count how many cases there are
- (c) To remove duplicate cases
- (d) So that editing a gold label after seeing a score raises an error instead of quietly raising the score

---

**A14.** [W23] One call sends `500` tokens in and gets `80` tokens out. The price is `$2.00` per million tokens in and `$10.00` per million tokens out. The cost of one call is:

- (a) $0.018
- (b) $0.0010
- (c) $0.0018
- (d) $0.00018

---

**A15.** [W24] In the code game, `n` pairs are shown in the prompt and the best any player can score is `(n + 1) / 6`. A trained model with `n = 4` scores `0.86` on 500 test prompts, where a score wobbles by about two points either way. The best reading is:

- (a) It is `2.7` points over the ceiling of `0.833`, only a little more than the wobble, so this is not enough to say it beat the rules; test more prompts and more seeds
- (b) The formula for the ceiling must be wrong
- (c) The model must have leaked the answer: no score above the ceiling is ever noise
- (d) Bigger models can beat any ceiling

---

**A16.** [W24] Two models of the same size are trained for the same number of steps on five-digit addition. One writes the answer straight away; the other writes the working first. The one with the working usually scores far higher, because:

- (a) It has more knobs
- (b) It was trained for longer
- (c) It was shown more sums
- (d) Each step it writes is a small sum, and the earlier steps are on the page for the later ones to read, so it does not have to do everything at once

---

**A17.** [W25] A note's row of numbers is multiplied by 3 (the same direction, three times as long). Compared with a fixed query, what happens?

- (a) The dot product and the cosine both triple
- (b) The dot product triples and the cosine is unchanged
- (c) Both are unchanged
- (d) The cosine triples and the dot product is unchanged

---

**A18.** [W25] The trained embedder has recall@1 `0.63` after 150 steps. The same embedder after **one** step (almost random numbers for the same letter pieces) has `0.48`. Pure chance is `0.07`. The best reading is:

- (a) Training did nothing
- (b) The embedder is perfect after 150 steps
- (c) Most of the score came from the letter pieces; training added about `0.15` on top of almost-random numbers for the same pieces
- (d) The control run is not allowed to be compared with the trained one

---

**A19.** [W26] A notebook has 12 notes. A searcher picks 3 of them at random for each question. The recall@3 you would get by pure chance is:

- (a) 0.08
- (b) 0.25
- (c) 0.33
- (d) 0.50

---

**A20.** [W26] A refusal threshold `tau` was chosen by looking at questions the author wrote after reading the notes: it gave zero mistakes. What is wrong with trusting it?

- (a) Those were the easy questions: a stranger's wording scores lower, so the same `tau` will refuse many real questions
- (b) A threshold is not allowed to be chosen from data
- (c) Zero mistakes can never happen
- (d) Nothing is wrong: zero mistakes is the best result

---

# 🅱️ Section B — What Does This Print?

*8 questions · 2 marks each · write EVERY line the program prints, exactly. Rounding is done inside the code. Each snippet is separate and imports what it needs. `merge` and `chunks` in B1 are the Week 20 functions from your own `bpe.py`.*

---

**B1.** [W20] `merge(ids, pair, new_id)` replaces each adjacent `pair` by `new_id`, left to right, and never reuses a number it has already glued.

```py
from bpe import merge, chunks
print(merge([1, 2, 1, 2, 2], (1, 2), 7))
print(merge([5, 5, 5, 5, 5], (5, 5), 9))
print(chunks("a  b c"))
print(len("né 🙂"), len("né 🙂".encode("utf-8")))
```

---

**B2.** [W21] Three lines are printed.

```py
import numpy as np
N = np.array([1e2, 1e3, 1e4])
L = np.array([6.0, 3.0, 1.5])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
print(round(slope, 3), round(10 ** slope, 2))
print(round(10 ** intercept, 1))
print(round(float(10 ** (slope * np.log10(1e5) + intercept)), 2))
```

---

**B3.** [W22] Three lines are printed. (`log(1/3) = -1.0986`, `ln(11.107) = 2.4076`.)

```py
import torch
import torch.nn.functional as F
scores = torch.tensor([[0.0, 0.0, 0.0],
                       [2.0, 1.0, 0.0]])
logp = F.log_softmax(scores, dim=-1)
picked = logp.gather(1, torch.tensor([[1], [0]]))
print([round(v, 3) for v in picked.reshape(-1).tolist()])
targets = torch.tensor([-100, -100, 3, 1, 2])
print(int((targets != -100).sum()), len(targets))
print(tuple(picked.shape))
```

---

**B4.** [W23] Two lines are printed.

```py
class OverBudget(Exception):
    pass

class Guard:
    def __init__(self, limit):
        self.limit = limit
        self.spent = 0.0
    def charge(self, cost):
        self.spent += cost
        if self.spent > self.limit:
            raise OverBudget("stop")

guard = Guard(0.05)
calls = 0
try:
    for _ in range(10):
        guard.charge(0.02)
        calls += 1
    print("finished")
except OverBudget:
    print("stopped after", calls, "calls, spent", round(guard.spent, 2))
print("calls made in total:", calls + 1)
```

---

**B5.** [W24] Two lines are printed. (`e^2 = 7.389`, `e^1 = 2.718`, `e^0 = 1`.)

```py
import torch
import torch.nn.functional as F
scores = torch.tensor([2.0, 1.0, 0.0, 3.0])
allowed = torch.tensor([True, True, True, False])
masked = torch.where(allowed, scores, torch.tensor(float("-inf")))
print([round(v, 3) for v in F.softmax(masked, dim=-1).tolist()])
print(scores.argmax().item(), masked.argmax().item())
```

---

**B6.** [W25] Three lines are printed.

```py
import numpy as np
notes = np.array([[3.0, 4.0],
                  [4.0, 3.0],
                  [0.0, 5.0]])
q = np.array([0.0, 1.0])
dots = notes @ q
print(dots.tolist())
print(np.argsort(-dots)[:2].tolist())
print([round(float(n @ q / (np.sqrt(n @ n) * np.sqrt(q @ q))), 2) for n in notes])
```

---

**B7.** [W23] Four lines are printed.

```py
import re
from dataclasses import dataclass

@dataclass
class Run:
    name: str
    score: float

a = Run("v1", 0.5)
print(a)
print(a == Run("v1", 0.5), a.score)
reply = 'ok:\n{"urgency": 2,\n "id": null}'
print(re.search(r"\{.*\}", reply))
print(re.search(r"\{.*\}", reply, re.S) is not None)
```

---

**B8.** [W26] Four lines are printed.

```py
import re
answer = "Weight decay helped [2], and warmup helped [1]. Also [2]."
cited = set(re.findall(r"\[(\d+)\]", answer))
served = {"1", "2", "4"}
print(sorted(cited))
print(cited <= served, len(cited))
print(cited - {"1"})
print(sorted(["note-10.md", "note-9.md", "note-1.md"]))
```

---

# 🅲 Section C — Find and Fix the Bug

*4 questions · 3 marks each · for each: **(i)** what is wrong · **(ii)** what happens when it runs (an error, with what its last line means in plain words, or a silent wrong result) · **(iii)** the fixed line. The programs are **deliberately** broken.*

---

**C1.** [W21] The programmer wants to keep one copy of each distinct line.

```py
# DELIBERATE: this program has a bug. Find it.
import hashlib
lines = ["the river ran past the town", "a cold wind came", "the river ran past the town"]
seen = set()
kept = []
for line in lines:
    key = hashlib.md5(line).hexdigest()
    if key not in seen:
        seen.add(key)
        kept.append(line)
print(len(kept))
```

The program prints:

```text
Traceback (most recent call last):
  File "c1.py", line 7, in <module>
    key = hashlib.md5(line).hexdigest()
TypeError: Strings must be encoded before hashing
```

---

**C2.** [W22] The programmer wants, at every place of every window, the chances of the 5 characters to add up to 1. Python also prints a one-line warning that is not shown here.

```py
# DELIBERATE: this program has a bug. Find it.
import torch
import torch.nn.functional as F
torch.manual_seed(0)
logits = torch.randn(2, 3, 5)                 # 2 windows, 3 places, 5 characters
logp = F.log_softmax(logits)
chance_total = logp.exp().sum(dim=-1)         # for every place, the chances of the 5 characters added up
print(tuple(chance_total.shape), round(chance_total[0, 0].item(), 3))
print(torch.allclose(chance_total, torch.ones(2, 3)))
```

The program prints:

```text
(2, 3) 2.225
False
```

---

**C3.** [W24] The programmer wants five **different** rolls of one private dice, made so that the run can be repeated.

```py
# DELIBERATE: this program has a bug. Find it.
import random
rolls = []
for _ in range(5):
    dice = random.Random(7)
    rolls.append(dice.randint(1, 6))
print(rolls)
```

The program prints:

```text
[3, 3, 3, 3, 3]
```

---

**C4.** [W26] The programmer wants to accept an answer only if every id it cites is one of the notes that were served. The answer cites note 2, which was served.

```py
# DELIBERATE: this program has a bug. Find it.
import re
served = {1, 2, 4}                                   # ids of the notes handed to the writer, as numbers
answer = "Weight decay gave a steadier curve [2]."
cited = set(re.findall(r"\[(\d+)\]", answer))
print(cited, cited <= served)
print("refuse" if not cited <= served else "accept")
```

The program prints:

```text
{'2'} False
refuse
```

---

# 🅳 Section D — Do the Arithmetic

*3 questions · 5 marks each · a calculator is expected · show every line of working · carry FOUR decimal places and round only at the end.*

---

**D1.** [W20] Byte-pair encoding, by hand. The text is

```text
ab ab ab abc abc
```

The bytes are `a = 97`, `b = 98`, `c = 99`, and the first new piece gets the number `256`. Chunks are cut at spaces (each run of spaces is its own chunk), and a pair is never glued across a chunk. A pair that occurs **fewer than twice** is not glued. On a tie the pair with the smaller numbers would win (you will not need it).

**(a)** Count every pair of neighbours inside the chunks, counting a chunk as many times as it occurs. Write the counts. *(1)*
**(b)** Write the first merge: the pair, its new number, and its count. Then write the chunks `ab` and `abc` with the merge applied. *(1)*
**(c)** Write the second merge in the same way. Then say what happens on the third round and why. *(1)*
**(d)** Encode the text `abcab` with the two merges (earliest-learned first). Write the list of numbers, and the bytes per token. *(1)*
**(e)** Encode `cab` and `ba` the same way. Write both lists and say, for each, whether any merge applied. *(1)*

---

**D2.** [W22] Two tables of chances over three answers, and one preference pair. Use `ln 2 = 0.6931`, `ln 1.2 = 0.1823`, `ln 2.5 = 0.9163`, `e^-0.9 = 0.4066`, `e^-7.2 = 0.0007`.

```text
   policy  p = [0.5, 0.3, 0.2]          reference  q = [0.25, 0.25, 0.5]

   one pair: reference log-chances (chosen, rejected) = (-6.0, -4.0)
             policy now                                = (-5.0, -4.8)
```

**(a)** Write the three terms of KL of `p` from `q` (that is `p x ln(p / q)` for each answer) and add them, to four decimals. *(2: one for the terms, one for the sum)*
**(b)** What is the KL of `p` from `p` itself, before any arithmetic? Work out the KL of `q` from `p` (the roles swapped). Is it the same as (a)? *(1)*
**(c)** For the pair: how far did the chosen answer move, how far did the rejected one move, and what is the gap? At `beta = 0.5` write the margin, `sigmoid(margin)`, and the loss `-ln sigmoid(margin)`. *(1)*
**(d)** At `beta = 4` with the same movement, write the margin and the loss. Say in one sentence what the tiny loss means for how far the model will go. *(1)*

---

**D3.** [W21] A scaling line, `6ND`, and a prediction. Three models were trained the same way. Their knobs `N` and validation losses:

```text
   N =   2,000     20,000     200,000
   L =    10.0        4.0         1.6
```

**(a)** Write `log10` of all six numbers. *(1)*
**(b)** Work out the slope of the line on log-log paper between the first two points, and then between the last two, to three decimals. Do the three points lie on one line? *(1)*
**(c)** Say by what number the loss is multiplied when the knobs are multiplied by 10, and by what number when they are multiplied by 2. *(1)*
**(d)** Use the line to predict the loss for `N = 2,000,000`. Is that number a measurement? *(1)*
**(e)** The 200,000-knob model reads `D = 3,000,000` characters. Estimate `C = 6ND`. If a computer does `2 x 10^9` operations a second, how long is that, in minutes? *(1)*

---

# 🅴 Section E — Reading Real Tables

*1 question with three parts · 12 marks · the numbers are real · quote them.*

**Table 1 (Week 19).** The Week 19 five-model run, **shortened**: the same `text_ablate.py`, but with **400 steps** instead of 800 and **seed 2** instead of 0. Each model is a TinyGPT of width 128, 4 heads and 4 blocks, trained on the 6,972 typed characters, one thing deleted at a time, with the same scoring batches for every row. The sample is the first 70 characters of what the model writes.

```text
full      train 1.935  val 1.939  gap 0.004
          t the wther can thedo ind ris the tha ane ot as the che me want thas w
no mask   train 1.631  val 1.638  gap 0.007
          tatatttttttattottttdstttatttottttttttt tetotttsetettetttetewtttttttstt
no pos    train 1.798  val 1.854  gap 0.056
          the cat chris oth ado ind ris the the a beothe rid an therewr the rshe
no res    train 2.841  val 2.852  gap 0.011
          t ew  e chr eeotn hdo  waordo t g  ah  eewot  s  dn e ta eewr trttrs w
no norm   train 1.716  val 1.763  gap 0.047
          t the wachrker the do ownord be gerll anewot as the cloaned bot thes w

For comparison, Week 19's own run (800 steps, seed 0), validation only:
          full 1.673   no mask 0.077   no pos 1.739   no res 2.679   no norm 1.478
```

**E(a)** *(4 marks, 1 each)*
**(i)** For each of the four deleted models, work out its validation loss **minus the full model's**. Which of the four is the only one clearly **worse** than the full model?
**(ii)** The "no mask" row has a good number, and its sample begins `tatattt`. Say what you think happened and describe one test, needing no trained model, that would settle it.
**(iii)** In this run "no positions" (`1.854`) beats the full model (`1.939`). In Week 19's run it was worse (`1.739` against `1.673`). Say what this disagreement tells you about ranking "no pos" and "no norm" against the full model.
**(iv)** A classmate says: *"No residual has the smallest gap except the full model, `0.011`, so it generalises well."* Reply in one sentence, using two numbers from the table.

**Table 2 (Week 21).** Four widths of the same TinyGPT (2 heads, 2 blocks, only the width changes), each trained for **600 steps** of 32 windows of 64 characters, seed 1, scored on the same 640 validation windows. Then the straight line on log-log paper was fitted to the four rows and used to **predict** a fifth, bigger model, which was then really trained.

```text
width  12  knobs    9813  validation loss 2.5882
width  24  knobs   26325  validation loss 2.3950
width  48  knobs   80085  validation loss 2.2241
width  96  knobs  270549  validation loss 1.9187

the fitted line:  slope -0.0883   intercept 0.7695
width 192:  knobs 983,253   predicted loss 1.739   measured loss 1.7516
```

(`log10` of the knobs, first and last rows: `3.9918` and `5.4322`. `log10` of the losses: `0.4130` and `0.2830`.)

**E(b)** *(4 marks, 1 each)*
**(i)** Using **only the first and last rows**, work out the slope by hand and compare it with the printed `-0.0883`. Say in a few words why the two need not agree exactly.
**(ii)** Using `-0.0883`, by what number is the loss multiplied when the knobs are multiplied by 10? Write it as a ratio, and also say what a classmate who read `-0.0883` as "lose 8.8%" has got wrong.
**(iii)** Work out how far the measured `1.7516` is from the predicted `1.739`, and say what a prediction from the line is, and what the miss does and does **not** show.
**(iv)** The 192-wide run read `600 x 32 x 64` characters. Work out `D`, then `C = 6ND` for that run to two significant figures. Say one thing about the whole table that **stops it being a law**.

**Table 3 (Weeks 25 and 26).** The 15-note notebook. Eight questions the author wrote **after reading the notes** ("yours"), the same eight facts asked in words that are **not** the notebook's ("stranger"), and four questions whose answers are **not** in the notes. For each index, the best score of each question, and recall@k (the share of questions whose right note is in the top k). A question is **answered** if its best score is at least `tau`. "Errors" means answerable questions refused plus unanswerable questions answered. (The index is real; the writer behind it, where one is used, is a **stand-in, not a model**.)

```text
word table (Week 25's TF-IDF)
  answerable  : 0.225 0.349 0.366 0.459 0.496 0.541 0.543 0.565
  unanswerable: 0.000 0.000 0.138 0.138
  recall@1/3/5: [1.0, 1.0, 1.0]
  stranger    : 0.000 0.105 0.117 0.120 0.166 0.175 0.176 0.269
  stranger recall@1/3/5: [0.12, 0.38, 0.88]
  tau 0.10: answered 8/8, unanswerable refused 2/4, errors 2, stranger answered 7/8
  tau 0.20: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 1/8
  tau 0.30: answered 7/8, unanswerable refused 4/4, errors 1, stranger answered 0/8

LSA, 14 directions (Week 25's squeezed index)
  answerable  : 0.942 0.945 0.946 0.950 0.970 0.971 0.972 0.980
  unanswerable: 0.654 0.737 0.768 0.786
  recall@1/3/5: [1.0, 1.0, 1.0]
  stranger    : 0.553 0.621 0.622 0.652 0.670 0.702 0.732 0.763
  stranger recall@1/3/5: [0.38, 0.75, 0.75]
  tau 0.60: answered 8/8, unanswerable refused 0/4, errors 4, stranger answered 7/8
  tau 0.80: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 0/8
  tau 0.90: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 0/8
```

**E(c)** *(4 marks, 1 each)*
**(i)** At `tau = 0.20` the word table makes **zero** errors. Name the other number in that row that spoils the good news, and say in a sentence why it is lower.
**(ii)** The LSA index also makes zero errors, at `tau = 0.80`. A classmate says: *"So use `0.80` for the word table too."* Say what would happen, with one number from the table.
**(iii)** Work out the recall@3 you would get by pure chance on 15 notes. By how much does the word table's **stranger** recall@3 beat it, and what does one question here count for (there are 8)?
**(iv)** In two sentences: what does Table 3 support, and what can it **not** tell you? End with the first question you would ask before trusting any of these recall numbers.

---

# 💻 PART 2 — THE DEMO

**15 minutes · 15 marks · a computer, your own Week 19–26 files, and the `l4lib` folder. No network, no chatbot.**
*Teacher: sit beside the student. The marks are for what you **watch** and **hear**, so keep the checklist in the marking scheme next to you.*

Open a terminal in the `36-week-course/` folder. Run `export PYTHONPATH="$PWD"` once. Copy your Week 20 `bpe.py` and your Week 23 `bench.py` and `guard.py` next to the demo files. Each demo is a new file. **Say your prediction out loud before you run anything.** A prediction you make after seeing the output does not count.

**Demo 1 — "Check my hand arithmetic" · 5 marks · Weeks 20 and 22**
Write `demo1.py`. **(i)** Train your `bpe.py` on `"ab ab ab abc abc"` with up to 5 merges, `verbose=True`. Print how many merges were learned, then encode `abcab`, `cab` and `ba`, and print for each the list of numbers, whether it decodes back, and the bytes per token. These must match your **D1**. **(ii)** Print whether `"né 🙂"` survives a round trip with those two merges, and say what the answer does **not** tell you about the tokens. **(iii)** With `math.log`, print the KL of `p` from `q` and of `q` from `p` from **D2**. **(iv)** With `F.logsigmoid`, print the margin and the loss for the pair in **D2** at `beta = 0.5` and `beta = 4`. Say in one sentence why the loss with the bigger `beta` is not "the better model".

**Demo 2 — "The line, the floor and the guard" · 5 marks · Weeks 21 and 23**
Write `demo2.py`. **(i)** Fit the line of **D3** with `np.polyfit` and print the slope, the multiplier for 10 times the knobs and for 2 times, the prediction at `N = 2e6`, `C = 6ND`, and the seconds at `2e9` per second. Say out loud that the prediction is not a measurement. **(ii)** From your `bench.py`, print the floor (the best constant answer). Then copy the frozen cases, change **one** gold label in the copy, and show that the fingerprint no longer matches and that `check_frozen` refuses. **(iii)** Run your `BudgetGuard` with a limit of `$0.05` and calls of `$0.02`; print the call it stops on. Compare with **B4**. **(iv)** Print `FakeClient(seed=0)` and read the label aloud.

**Demo 3 — "Cosine, ceiling, gate, citation" · 5 marks · Weeks 24, 25 and 26**
Write `demo3.py`. **(i)** Print the ceiling `(n + 1) / 6` for `n = 0` to `5`, and the wobble `sqrt(c x (1 - c) / 500)` at `c = 0.833`. **(ii)** Write your own `cosine(x, y)` with numpy. Print the cosines and the dot products of the three notes in **B6** against the query, the top two by each, and the dot product and cosine of the first note when it is tripled. **(iii)** Build the word-table index over `rag.notebook_chunks()`. For the questions `"Which temperature was the sweet spot for names?"` and `"Which dataset was used for the vision experiments?"`, call `rag.rag_answer` at `threshold = 0.10` and at `0.20`, and print the best score, whether it refused, the cited ids and whether the citation check passed. (The writer is a stand-in, not a model.) **(iv)** With **sets**, check that `{"2"}` is inside `{"1", "2", "4"}` and that `{"2", "9"}` is not, and print what is missing. Say out loud what a passing citation check does and does not prove.

*End of Part 2.*

---

# 📊 MARKING SCHEME

**Paper: 75 marks. Demo: 15 marks. Report them separately.** The paper is "can you run code and arithmetic in your head", the demo is "can you prove it on a machine, in front of someone". A student who is strong on one and weak on the other has told you something that one sum would hide.

> **Mark Section A first.** It is fast, and the pattern of wrong answers tells you where to look in the rest.
> Below each answer in the key is a sentence on why the wrong options were tempting.

## Section A — 20 marks

| Q | Ans | Week | | Q | Ans | Week |
|:--:|:--:|:--:|---|:--:|:--:|:--:|
| A1 | **b** | W19 | | A11 | **a** | W22 |
| A2 | **c** | W19 | | A12 | **b** | W23 |
| A3 | **a** | W19 | | A13 | **d** | W23 |
| A4 | **d** | W20 | | A14 | **c** | W23 |
| A5 | **b** | W20 | | A15 | **a** | W24 |
| A6 | **b** | W21 | | A16 | **d** | W24 |
| A7 | **c** | W21 | | A17 | **b** | W25 |
| A8 | **a** | W21 | | A18 | **c** | W25 |
| A9 | **d** | W22 | | A19 | **b** | W26 |
| A10 | **c** | W22 | | A20 | **a** | W26 |

No half marks. Two letters circled scores 0. A guess marked "not sure" that is right still scores 1; count the "not sure" ones separately, because a student who is right and knows they are unsure needs a different conversation from one who is wrong and sure.

## Section B — 16 marks

**2 marks for every snippet exactly right. 1 mark if the idea is right and one digit, bracket or sign is wrong. 0 otherwise.** Count lines: a correct first line and a missing second line is 1. Sets are printed in braces and lists in square brackets; both must be right.

| Q | Exact output | The trap |
|:--:|---|---|
| B1 | `[7, 7, 2]` · `[9, 9, 5]` · `['a', '  ', 'b', ' ', 'c']` · `4 8` | Second line: gluing **overlapping** pairs (`[9, 9, 9]` or `[9, 9]`). Five fives hold two non-overlapping pairs and one left over. Third line: splitting the two spaces into two chunks (`'  '` is **one** chunk). Fourth line: `4 4` (counting a character as a byte): the `é` is two bytes and the emoji is four, `1 + 2 + 1 + 4 = 8`. |
| B2 | `-0.301 0.5` · `24.0` · `0.75` | `-0.3` (the rounding is to 3 places: `-0.301`). `0.5` is `10 ** slope`: every tenfold in knobs halves the loss (`6, 3, 1.5`). `24.0` is the loss at `N = 1` read off the line (a loss of 6 at `N = 100` is `24 / 100^0.301 = 6`). The last line continues the halving to `N = 1e5`: `1.5 x 0.5 = 0.75`. A student who writes `1.5` or `0.3` for the last line has forgotten the line is a straight line in logs, so each tenfold halves the loss. |
| B3 | `[-1.099, -0.408]` · `3 5` · `(2, 1)` | `-1.1` (Python prints `-1.099` at three places, not `-1.1`). `-0.408`: row 1 picks column 0 (score 2), whose log-chance is `2 - 2.4076`. `3 5`: three guesses count of five. `(2, 1)` not `(2,)`: `gather` wants, and returns, a column. |
| B4 | `stopped after 2 calls, spent 0.06` · `calls made in total: 3` | `stopped after 3 calls`: the counter went up **after** the charge that raised, so only two were counted, but **three were made and paid for**: the guard stops one call late. Writing `finished` on the first line. Writing `0.04`: the third charge has already been added (`0.06`) when the error is raised. |
| B5 | `[0.665, 0.245, 0.09, 0.0]` · `3 0` | `0.090` (Python prints `0.09`). The masked place gets exactly `0.0`, not a small number. The plain argmax is place 3 (score `3`); the masked argmax is place 0. `0.731` (`7.389 / 10.107`) is what you get by forgetting the third score: `e^0 = 1` counts too, so the total is `7.389 + 2.718 + 1 = 11.107` and the first chance is `0.665`. |
| B6 | `[4.0, 3.0, 5.0]` · `[2, 0]` · `[0.8, 0.6, 1.0]` | Writing the top two as `[1, 0]` (smallest first, no minus) or as the scores. The cosines are the dot divided by the two lengths: `4 / (5 x 1)`, `3 / 5`, `5 / 5`. Here the dot product and the cosine rank the notes the same way, because the notes all have the same length `5`; that is luck of the numbers, not a rule (see A17). |
| B7 | `Run(name='v1', score=0.5)` · `True 0.5` · `None` · `True` | Writing `Run('v1', 0.5)` (a dataclass prints the **field names**). `None` for the search **without** `re.S`: the dot does not cross the line break. Writing `False` on the last line. |
| B8 | `['1', '2']` · `True 2` · `{'2'}` · `['note-1.md', 'note-10.md', 'note-9.md']` | `['1', '2', '2']` (a set keeps each id once, so `len` is 2). `[1, 2]` with numbers (`findall` returns **text**). The last line: names sort as **text**, so `note-10` comes before `note-9` (the reason Week 26 zero-pads). |

## Section C — 12 marks

**3 marks each: (i) the bug named = 1 · (ii) what happens = 1 · (iii) a correct fix = 1.**

| Q | (i) The bug | (ii) What happens | (iii) The fix |
|:--:|---|---|---|
| C1 | `hashlib.md5` is handed a **string**, but it works on **bytes** | **Loud.** `TypeError: Strings must be encoded before hashing` | `hashlib.md5(line.encode("utf-8")).hexdigest()` (the program then prints `2`) |
| C2 | `F.log_softmax(logits)` has **no `dim=`**. On a three-axis tensor it picks the **first** axis (the windows), not the characters | **Silent**, apart from a one-line `UserWarning` that says "Implicit dimension choice ... has been deprecated". Nothing crashes: the chances over the characters add to `2.225`, not `1`, and the check prints `False` | `F.log_softmax(logits, dim=-1)` (then `(2, 3) 1.0` and `True`) |
| C3 | A **new** `random.Random(7)` is built **inside** the loop, so every roll comes from a fresh dice at the same starting point | **Silent.** The same number five times, `[3, 3, 3, 3, 3]` | Build the dice **once, before** the loop: `dice = random.Random(7)`, then roll five times from it |
| C4 | `findall` returns ids as **text** (`'2'`); `served` holds **numbers** (`2`). `'2'` is never in a set of numbers | **Silent.** A perfectly good citation is refused (`refuse`) | Make both the same kind: `served = {"1", "2", "4"}` (or `int(...)` the cited ids) |

For C2 and C3, a student who says "it crashes" has not understood the bug. Accept "it prints something wrong" for (ii). For C2 accept "the chances do not add to 1" or "it picks the wrong axis". For C3 the first number `3` is a real roll of `Random(7)` and is not part of the bug. Accept any fix that produces the expected result; the key fixes were run (see the key).

## Section D — 15 marks

| Part | Marks | What earns them |
|---|:--:|---|
| D1(a) | 1 | `(a, b)` = **5** (3 in `ab`, 2 in `abc`) and `(b, c)` = **2**. 0 if the chunk counts were not used (`(a, b) = 2`). |
| D1(b) | 1 | Merge 1: `(97, 98)` → `256`, count **5**. The chunks become `[256]` (x3) and `[256, 99]` (x2). |
| D1(c) | 1 | Merge 2: `(256, 99)` → `257`, count **2**; the chunk is now `[257]`. Third round: **no pair is left**, so training **stops** at 2 merges (every chunk is one piece). |
| D1(d) | 1 | `abcab` is the bytes `[97, 98, 99, 97, 98]`; `(a, b)` is the earliest merge → `[256, 99, 256]`; then `(256, 99)` → `[257, 256]`. **2 tokens** for 5 bytes: **2.5** bytes per token. |
| D1(e) | 1 | `cab` → `[99, 256]` (only the first merge applied, `(a, b)`); `ba` → `[98, 97]` (**no** merge applied: the pair `(b, a)` was never learned). Both written, and a "which applied" for each. |
| D2(a) | 2 | Terms: `0.5 ln 2 = 0.3466`, `0.3 ln 1.2 = 0.0547`, `0.2 ln 0.4 = -0.1833` (1). Sum **0.2180** (1). Accept `0.218`. |
| D2(b) | 1 | KL of `p` from `p` is **0** (all log-ratios are 0). KL of `q` from `p` = `0.25 x -0.6931 + 0.25 x -0.1823 + 0.5 x 0.9163 =` **0.2393**. **Not the same** as 0.2180: the order matters. Both parts needed. |
| D2(c) | 1 | Chosen moved `-5.0 - -6.0 = +1.0`; rejected `-4.8 - -4.0 = -0.8`; gap **1.8**. Margin `0.5 x 1.8 =` **0.9**; `sigmoid(0.9) = 1 / 1.4066 =` **0.7109**; loss `-ln 0.7109 =` **0.3412**. Accept `0.341`. |
| D2(d) | 1 | Margin `4 x 1.8 =` **7.2**; loss about **0.00075** (`1 / (1 + 0.0007)`, `-ln` of it). The sentence: the loss is already tiny, so there is almost no push left, and the model **stops moving early**: a bigger `beta` means a shorter leash. |
| D3(a) | 1 | `log10 N`: `3.3010, 4.3010, 5.3010`. `log10 L`: `1.0000, 0.6021, 0.2041`. 0 if two are wrong. |
| D3(b) | 1 | First two: `(0.6021 - 1.0) / 1 =` **-0.398**. Last two: `(0.2041 - 0.6021) / 1 =` **-0.398**. The same slope: the three points lie on **one line**. |
| D3(c) | 1 | `10 ^ -0.398 =` **0.4** for ten times the knobs; `2 ^ -0.398 =` **0.759** (about 0.76) for two times. As **ratios**, not "lose 0.398". |
| D3(d) | 1 | `1.6 x 0.4 =` **0.64**. **Not** a measurement: it is where the ruler says the next point would be; the only way to turn it into a measurement is to train that model. |
| D3(e) | 1 | `C = 6 x 200,000 x 3,000,000 =` **3.6 x 10^12**. `3.6e12 / 2e9 = 1,800` seconds = **30 minutes**. |

## Section E — 12 marks

| Part | Marks | What earns them |
|---|:--:|---|
| E(a)(i) | 1 | no mask `-0.301`, no pos `-0.085`, no res `+0.913`, no norm `-0.176`. **No residual** is the only clearly worse one. All four differences needed (accept one slip). |
| E(a)(ii) | 1 | A **leak**: with no mask each place can read the next character, which is the answer, so the low loss is reading and not predicting; the `tatatt` sample is the model repeating what it can see. The test: change **one later character** and see whether the scores at **earlier** places move (zero with a mask, not zero without). "It is just better" scores 0. |
| E(a)(iii) | 1 | Differences of about `0.1` to `0.2` on one seed and one shortened run **cannot be ranked**: the sign of "no pos" flips between two runs. It would need more seeds (and the full steps) before saying more. "The table is wrong" scores 0. |
| E(a)(iv) | 1 | A small gap is not good news here: **train `2.841` and validation `2.852` are both far worse than the full model's `1.935` and `1.939`**: it has barely learned anything, so there is nothing to overfit. (The gap is `0.011` only because both numbers are bad.) |
| E(b)(i) | 1 | `(0.2830 - 0.4130) / (5.4322 - 3.9918) = -0.1300 / 1.4404 =` **-0.0903**. Not the same as `-0.0883` because the fitted line uses **all four** rows; the two end rows are only two of the four points, and the four are not exactly on a line. |
| E(b)(ii) | 1 | `10 ^ -0.0883 =` **0.816**: ten times the knobs multiplies the loss by about 0.82 (about 18% less, not 8.8%). The mistake: the slope is an **exponent** on log-log paper; the ratio is `10 ^ slope`. Accept 0.82. |
| E(b)(iii) | 1 | Off by `1.7516 - 1.739 =` **0.0126** (about 0.7%, a little worse than predicted). A prediction is where a line fitted to **smaller** models says a bigger one will land, **not a measurement**. The miss shows the line was good **here, at this size, on one seed and 600 steps**; it does not show that the line goes on forever (a 4x step in knobs is not a thousand-fold step). |
| E(b)(iv) | 1 | `D = 600 x 32 x 64 =` **1,228,800** characters. `C = 6 x 983,253 x 1,228,800 =` **7.2 x 10^12** (accept 7.2e12 or 7.3e12). Anything that stops it being a law: one seed, only four small points, 600 steps, the largest model reads **the same** characters as the smallest, a text pool particular to this computer. Any **one** of these. |
| E(c)(i) | 1 | **Stranger answered: 1/8.** The questions the author wrote after reading the notes use the notebook's own words, so they score high; a stranger's wording shares fewer words, so its scores are low, and `tau = 0.20` refuses seven of eight real questions. |
| E(c)(ii) | 1 | The word table's **best** answerable score is `0.565`, below `0.80`, so **0 of 8** would be answered: every real question refused. A threshold belongs to **one** index. Any number from the table (`0.565`, `0/8`) earns the mark. |
| E(c)(iii) | 1 | Chance recall@3 = `3 / 15 =` **0.20**. `0.38 - 0.20 =` **0.18**. One question is worth `1/8 =` **0.125**, so a gap of 0.18 is **about one and a half questions**: not much to hang a claim on. |
| E(c)(iv) | 1 | Supports: on questions in the notebook's own words, retrieval and the gate work (recall 1.0, zero errors at one `tau`). Cannot tell: how it does for other people's wording (recall drops to `0.12` at k=1) or with only 8 and 4 questions; and **a valid citation or a recall number is not a proof that the answer is right**. The first question: **"who wrote the questions?"** (or equivalent). |

## Part 2 — the demo, 15 marks

| | Marks | The teacher watches for |
|---|:--:|---|
| **Demo 1** | 5 | prediction said first (1) · two merges `(97, 98) -> 256 count 5` and `(256, 99) -> 257 count 2`; `abcab` `[257, 256]` 2.5, `cab` `[99, 256]` 1.5, `ba` `[98, 97]` 1.0, all decode `True` (1) · the round trip of `"né 🙂"` is `True`, and the sentence: *"a round trip only shows nothing was lost, not that the tokens are good"* (1) · KL `0.218` and `0.2393` and the order matters (1) · margins `0.9` and `7.2`, losses `0.34115` and `0.00075`, and the sentence: *"the smaller loss belongs to the model that moves less; never compare losses across different beta"* (1) |
| **Demo 2** | 5 | prediction said first (1) · slope `-0.398`, `0.4`, `0.759`, prediction `0.64` and the words *"a prediction, not a measurement"*, `3.6e+12` and `1800.0` seconds (1) · floor `43.8 %` from the frozen cases; the edited copy has a different fingerprint and `check_frozen` raises `the test set changed since it was frozen` (1) · the guard stops at call 3, with `$0.0600` spent over a `$0.0500` limit, and the student says *"it stops one call late"* (1) · `<FakeClient [stand-in, not a model] seed=0 calls=0>` read aloud with the meaning: *"anything it scores tells me about my harness, not about a real model"* (1) |
| **Demo 3** | 5 | prediction said first (1) · ceiling `[0.167, 0.333, 0.5, 0.667, 0.833, 1.0]` and wobble `0.017` (1) · cosines `[0.8, 0.6, 1.0]`, dots `[4.0, 3.0, 5.0]`, both top two `[2, 0]`; tripled row: dot `12.0` but cosine still `0.8`, said as *"length changes the dot, not the cosine"* (1) · the temperature question answered at both thresholds with `[3]`; the vision question **answered** at `0.10` with `[2]` and a passing check but **refused** at `0.20` (best score `0.138`) (1) · the two set checks (`True` `[]`; `False` `['9']`) and the sentence: *"a passing check only says the ids were ones we handed over; it cannot say the answer is right, and the vision answer above passed and was wrong"* (1) |

> **Reference output of the three demos** is in the key. If the student's numbers differ in the last digit on your machine, that is the CPU; a difference in the first digit is a bug, so ask them to find it (the Debugging Clinic habit of Week 9). In Demo 3, `rag.rag_answer`'s refusal and citation behaviour depends on the writer being the sentence-copying stand-in; its answers are copies of note sentences, and nobody should call them "the model's answer".

## How to read the score

These thresholds are suggestions; nothing in the course depends on them.

| Paper | What it probably means |
|:--:|---|
| 60–75 | Term 4 can start as planned. |
| 45–59 | Fine to start Term 4. Redo the one or two weeks in the grid below that scored under 60%. |
| under 45 | Do **not** read this as a verdict. Check Section A against the demo first: a student who knew it at the machine and lost it on paper needs a different plan from one who lost it on both. Redo at most two weeks, then re-sit the Week 27 paper. |

### The per-week grid

Add up the marks the student earned on these questions, and divide by the total shown.

| Week | Questions | Marks available | Redo this week if under |
|:--:|---|:--:|:--:|
| [19](../student-guide/week-19.md) | A1–A3, E(a) | 7 | 4 |
| [20](../student-guide/week-20.md) | A4–A5, B1, D1 | 9 | 5 |
| [21](../student-guide/week-21.md) | A6–A8, B2, C1, D3, E(b) | 17 | 10 |
| [22](../student-guide/week-22.md) | A9–A11, B3, C2, D2 | 13 | 8 |
| [23](../student-guide/week-23.md) | A12–A14, B4, B7 | 7 | 4 |
| [24](../student-guide/week-24.md) | A15–A16, B5, C3 | 7 | 4 |
| [25](../student-guide/week-25.md) | A17–A18, B6, E(c)(ii) | 5 | 3 |
| [26](../student-guide/week-26.md) | A19–A20, B8, C4, E(c)(i), (iii), (iv) | 10 | 6 |
| **Total** | | **75** | |

Three weeks carry Term 4: **Week 23** (the guard and the frozen set are reused by the agent's fences in Week 28 and the cost sum of Week 29), **Week 26** ("retrieved text is data" becomes an attack in Week 29), and **Week 22** (a later week fine-tunes with a leash and watches for a regression). If any of those is under the threshold, redo it first. **Week 21** is the heaviest single week on this paper (17 marks); a low score there with high scores elsewhere usually means the log-log line, not the whole term. **Weeks 23, 24 and 25 have few marks each**, so a flag on one of them means "ask the spoken check first" before assigning a redo.

---

# ✅ ANSWER KEY

> **🧑‍🏫 Do not show this to the student until after the test is marked.** It contains every answer and names the mistakes the student is expected to make. **Every code block in this key was run, and the real output is pasted in unedited.**

## Section A — why each answer, and why the wrong ones were tempting

<details>
<summary><b>A1–A10 (Weeks 19–22)</b></summary>

- **A1 (b).** A model that has hardly learned has nothing to overfit, so train and validation agree: Week 19's no-residual row (`2.664` and `2.679`) showed the same shape. *(a) and (d) read a small gap as good news; (c) is the opposite of what a gap of 0.01 says.*
- **A2 (c).** Switching off one head at a time shows neither is **necessary**; switching off both shows they are **sufficient together**, so the job is shared. Do not name either head "the copier". *(b) names a head the evidence does not single out; (a) ignores the drop to 0.50.*
- **A3 (a).** The question is "what was this head worth to a model that **learned with it**". Switching it off before training (Week 19's `bad_silence.py`) lets the model learn around the gap, so you learn nothing. *(b) and (c) mix the question up with ablation; (d) is the trap of not having thought about the order.*
- **A4 (d).** The `if pair_counts[best] < 2: break` line: nothing left that happens twice, so nothing worth gluing (`train(TEXT, 1000)` really returns 400). The key ran it: see below. *(b) and (c) invent a limit; 400 is a fact about this text, not about the function.*
- **A5 (b).** A round trip tests whether anything was **lost**. Week 20's zero-merge tokenizer passed all of them with one token per byte. Quality is tested by counting tokens (3,227 against 6,972) or by comparing with a known good tokenizer. *(a) is the opposite: zero merges is no compression.*
- **A6 (b).** Multiply `x` by 100 and `y` by `10 ^ (2 x -0.30) = 10 ^ -0.6 = 0.251`. *(a) reads the slope as a percentage per step; (c) as the multiplier itself; (d) as `10 ^ -1.5`.*
- **A7 (c).** `md5` is a fingerprint of the **exact** text. Week 21: change one letter and all 32 characters change. The key printed the two fingerprints: they share nothing. *(a) and (d) invent faults; (b) blames the loop, but the loop is fine.*
- **A8 (a).** `C = 6ND`: `2 x 3 = 6`. *(b) adds instead of multiplying; (c) is `3 x 3`; (d) squares the 6.*
- **A9 (d).** Only differences matter: add 100 to every reward and no chance changes (Week 22). *(a), (b), (c) all depend only on `3 - 1 = 2`; a student who picks one has not taken in that a reward has no zero.*
- **A10 (c).** KL is `0` exactly when the two tables are the same, and never negative (Week 22's `q itself` row). *(a) mixes KL with "good"; (b) confuses the KL measurement with the loss, which is a different number; (d) is a guess.*
- **A11 (a).** The margin is `beta x (the gap)`: ten times as big at `beta = 1.0`; the loss at the larger margin is much smaller (`0.5759` at margin `0.25`, `0.0789` at `2.5`), the gradient is quiet, and the model stops sooner. *(b) forgets `beta` is inside the margin; (c) has the loss going the wrong way.*

</details>

<details>
<summary><b>A11–A20 (Weeks 22–26)</b></summary>

- **A12 (b).** `20/32 = 62.5%`, `17/32 = 53.1%`: three boxes, on eight messages. Not enough to separate a real difference from luck. *(a) reads the percentages as if they were precise; (c) is false: a constant is a floor, not a ceiling.*
- **A13 (d).** The fingerprint is taken when the set is frozen; edit one gold label and `check_frozen` raises `AssertionError`. The demo shows it. *(a), (b), (c) describe what the call is not.*
- **A14 (c).** `500 x 2 / 1,000,000 = $0.0010`; `80 x 10 / 1,000,000 = $0.0008`; total **$0.0018**. *(a) is 10 times too big, (b) forgets the output tokens, (d) is 10 times too small.*
- **A15 (a).** Ceiling `(4 + 1) / 6 = 0.833`; the score is `0.027` over it with a wobble of about `0.017`: about one and a half wobbles. Not conclusive either way. *(c) is too sure: noise exists; (b) and (d) throw out the rule rather than the doubt.*
- **A16 (d).** Same size, same steps: the difference is what is written on the page. Each step is a small sum and later steps read the earlier ones. *(a), (b), (c) are the three things Week 24 held equal.*
- **A17 (b).** The dot product is length times length times the cosine, so it triples; the cosine divides the lengths out. *(a) and (d) forget the division; (c) forgets the length.*
- **A18 (c).** The control (Week 25's `untrained.py`) says how much of a score is the letter pieces. Training added about `0.15` to recall@1 over almost-random numbers. *(a) and (b) are both too strong; (d) is the opposite of what a control is for.*
- **A19 (b).** `3 / 12 = 0.25`. *(a) is `1/12`, recall@1; (c) is `1/3`; (d) is a coin.*
- **A20 (a).** The questions you wrote after reading the notes use the notebook's words, so they score high and look separable; Table 3 shows the same `tau` answering `1/8` stranger questions. *(b) is false (choosing from data is fine, choosing from the easy data is not); (c) is false in Table 3 (a row with zero exists), but it will not hold for other wording.*

</details>

### The Section A facts, run

```py
# afacts.py - the numbers behind Section A. Run from the folder that holds bpe.py and l4lib/.
import hashlib
import math
import numpy as np
import torch
import torch.nn.functional as F

# A4 (W20): the pair must occur at least twice, so training stops by itself
from bpe import train
from l4lib.corpus import TEXT
print("A4: merges asked 1000, learned", len(train(TEXT, 1000)))

# A6 (W21): slope -0.30, knobs x 100
print("A6:", round(100 ** -0.30, 3))

# A7 (W21): md5 only calls exact copies the same
a, b = "the river ran.", "The river ran."
print("A7: same fingerprint?", hashlib.md5(a.encode("utf-8")).hexdigest() == hashlib.md5(b.encode("utf-8")).hexdigest(),
      hashlib.md5(a.encode("utf-8")).hexdigest()[:8], hashlib.md5(b.encode("utf-8")).hexdigest()[:8])

# A8 (W21): N x 2, D x 3 -> C = 6ND
print("A8:", (6 * (2 * 5e5) * (3 * 1e6)) / (6 * 5e5 * 1e6))

# A9 (W22): add 10 to every reward
for shift in (0, 10):
    ra, rb = 3.0 + shift, 1.0 + shift
    print("A9: shift", shift, "reward gap", ra - rb, "chance A wins", round(torch.sigmoid(torch.tensor(ra - rb)).item(), 4),
          "loss", round(-F.logsigmoid(torch.tensor(ra - rb)).item(), 4))

# A10 (W22): KL of a table from itself
p = [0.4, 0.35, 0.25]
print("A10:", sum(x * math.log(x / x) for x in p))

# A11 (W22): the same movement at two betas
gap = 2.5
for beta in (0.1, 1.0):
    print("A11: beta", beta, "margin", beta * gap, "loss", round(-F.logsigmoid(torch.tensor(beta * gap)).item(), 4))

# A12 (W23): the floor
print("A12:", round(20 / 32 * 100, 1), round(17 / 32 * 100, 1), 20 - 17, "boxes of 32")

# A14 (W23): cost of one call
print("A14:", 500 * 2 / 1e6 + 80 * 10 / 1e6)

# A15 (W24): ceiling and wobble
n = 4
c = (n + 1) / 6
print("A15:", round(c, 3), "wobble", round(float(np.sqrt(c * (1 - c) / 500)), 4), "gap", round(0.86 - c, 3))

# A17 (W25): row tripled
row = np.array([1.0, 2.0]); q = np.array([2.0, 1.0])
cos = lambda x, y: float(x @ y / (np.sqrt(x @ x) * np.sqrt(y @ y)))
print("A17: dot", float(row @ q), float((3 * row) @ q), "cosine", round(cos(row, q), 4), round(cos(3 * row, q), 4))

# A19 (W26): chance recall@3 over 12 notes
print("A19:", 3 / 12)
```

```text
A4: merges asked 1000, learned 400
A6: 0.251
A7: same fingerprint? False bb845926 6468a7ac
A8: 6.0
A9: shift 0 reward gap 2.0 chance A wins 0.8808 loss 0.1269
A9: shift 10 reward gap 2.0 chance A wins 0.8808 loss 0.1269
A10: 0.0
A11: beta 0.1 margin 0.25 loss 0.5759
A11: beta 1.0 margin 2.5 loss 0.0789
A12: 62.5 53.1 3 boxes of 32
A14: 0.0018
A15: 0.833 wobble 0.0167 gap 0.027
A17: dot 4.0 12.0 cosine 0.8 0.8
A19: 0.25
```

(`A9`: shift 0 and shift 10 print the same chance and the same loss. `A17` uses a `lambda`, Week 4's one-line function, in the key only.)

## Section B — outputs, run

Each snippet below is exactly the one on the paper, run as its own file.

**B1**

```text
[7, 7, 2]
[9, 9, 5]
['a', '  ', 'b', ' ', 'c']
4 8
```

**B2**

```text
-0.301 0.5
24.0
0.75
```

**B3**

```text
[-1.099, -0.408]
3 5
(2, 1)
```

**B4**

```text
stopped after 2 calls, spent 0.06
calls made in total: 3
```

**B5**

```text
[0.665, 0.245, 0.09, 0.0]
3 0
```

**B6**

```text
[4.0, 3.0, 5.0]
[2, 0]
[0.8, 0.6, 1.0]
```

**B7**

```text
Run(name='v1', score=0.5)
True 0.5
None
True
```

**B8**

```text
['1', '2']
True 2
{'2'}
['note-1.md', 'note-10.md', 'note-9.md']
```

## Section C — bugs, run

Each **fixed** program, run. The broken outputs are printed on the paper (and were produced by the programs shown there, run for real; C2 also prints the warning described in the mark scheme).

**C1, fixed**

```py
import hashlib
lines = ["the river ran past the town", "a cold wind came", "the river ran past the town"]
seen = set()
kept = []
for line in lines:
    key = hashlib.md5(line.encode("utf-8")).hexdigest()
    if key not in seen:
        seen.add(key)
        kept.append(line)
print(len(kept))
```

```text
2
```

**C2, fixed**

```py
import torch
import torch.nn.functional as F
torch.manual_seed(0)
logits = torch.randn(2, 3, 5)
logp = F.log_softmax(logits, dim=-1)
chance_total = logp.exp().sum(dim=-1)
print(tuple(chance_total.shape), round(chance_total[0, 0].item(), 3))
print(torch.allclose(chance_total, torch.ones(2, 3)))
```

```text
(2, 3) 1.0
True
```

**C3, fixed**

```py
import random
dice = random.Random(7)
rolls = [dice.randint(1, 6) for _ in range(5)]
print(rolls)
print(len(set(rolls)) > 1)
```

```text
[3, 2, 4, 6, 1]
True
```

**C4, fixed**

```py
import re
served = {"1", "2", "4"}                             # fix: the ids as text, like the ones findall returns
answer = "Weight decay gave a steadier curve [2]."
cited = set(re.findall(r"\[(\d+)\]", answer))
print(cited, cited <= served)
print("refuse" if not cited <= served else "accept")
```

```text
{'2'} True
accept
```

## Section D — worked answers

### D1 (BPE by hand, 5 marks)

The chunks are `ab`, `' '`, `ab`, `' '`, `ab`, `' '`, `abc`, `' '`, `abc`: `ab` three times, `abc` twice, the single space four times (a single space has no pair).

**(a)** `ab` x 3 gives `(97, 98)` x 3. `abc` x 2 gives `(97, 98)` x 2 and `(98, 99)` x 2. So `(97, 98) = 5` and `(98, 99) = 2`.
**(b)** The commonest pair is `(97, 98)`, count 5: merge 1 is `(97, 98) -> 256`. The chunks are now `[256]` (x 3) and `[256, 99]` (x 2).
**(c)** The only pair left is `(256, 99)`, count 2: merge 2 is `(256, 99) -> 257`. Now `ab` is `[256]` and `abc` is `[257]`: every chunk is a single piece, so on the third round **no pair is left** and training stops.
**(d)** `abcab` is `[97, 98, 99, 97, 98]`. The earliest-learned pair is `(97, 98)`: `[256, 99, 256]`. Then `(256, 99)`: `[257, 256]`. Two tokens for five bytes: `5 / 2 = 2.5` bytes per token.
**(e)** `cab` is `[99, 97, 98]` → `[99, 256]` (only merge 1 applies). `ba` is `[98, 97]`: the pair `(98, 97)` was never learned, so **no merge** applies.

The machine check (this is `bpe.py` from Week 20 on `"ab ab ab abc abc"`):

```py
from collections import Counter
from bpe import train, encode, decode, make_vocab, chunks
text = "ab ab ab abc abc"
print(chunks(text))
print(Counter(chunks(text)))
merges = train(text, 5, verbose=True)
print(merges)
vocab = make_vocab(merges)
ids = encode("abcab", merges)
print(ids, [vocab[i] for i in ids], decode(ids, merges))
print("bytes per token:", len("abcab".encode("utf-8")) / len(ids))
print(encode("abab", merges), encode("cab", merges), encode("ba", merges))
print("text tokens:", len(encode(text, merges)), "bytes:", len(text.encode("utf-8")))
```

```text
['ab', ' ', 'ab', ' ', 'ab', ' ', 'abc', ' ', 'abc']
Counter({' ': 4, 'ab': 3, 'abc': 2})
merge 1 (97, 98) -> 256 count 5
merge 2 (256, 99) -> 257 count 2
{(97, 98): 256, (256, 99): 257}
[257, 256] [b'abc', b'ab'] abcab
bytes per token: 2.5
[256, 256] [99, 256] [98, 97]
text tokens: 9 bytes: 16
```

### D2 (KL and the pair loss, 5 marks)

**(a)** `p x ln(p / q)`: `0.5 x ln 2 = 0.5 x 0.6931 = 0.3466`; `0.3 x ln(0.3 / 0.25) = 0.3 x ln 1.2 = 0.3 x 0.1823 = 0.0547`; `0.2 x ln(0.2 / 0.5) = 0.2 x ln 0.4 = 0.2 x -0.9163 = -0.1833`. Sum: `0.3466 + 0.0547 - 0.1833 =` **0.2180**.
**(b)** KL of `p` from `p` is **0** (every `ln(p / p) = ln 1 = 0`). KL of `q` from `p`: `0.25 x ln(0.25 / 0.5) = -0.1733`; `0.25 x ln(0.25 / 0.3) = -0.0456`; `0.5 x ln(0.5 / 0.2) = 0.5 x 0.9163 = 0.4581`; sum **0.2393**. Not the same as `0.2180`: always say which comes first.
**(c)** The chosen answer moved `-5.0 - (-6.0) = +1.0`; the rejected one `-4.8 - (-4.0) = -0.8`; the gap is `1.0 - (-0.8) = 1.8`. At `beta = 0.5`: margin `0.9`; `sigmoid(0.9) = 1 / (1 + 0.4066) = 0.7109`; loss `-ln 0.7109 =` **0.3412**.
**(d)** At `beta = 4`: margin `7.2`; `sigmoid = 1 / 1.0007`; loss about **0.00075**. The loss is almost zero, so there is almost no push left: the model **stops moving early**. The tiny loss belongs to a model that moved less, not to a better one.

```py
import math
import torch
import torch.nn.functional as F
p = [0.5, 0.3, 0.2]
q = [0.25, 0.25, 0.5]
terms = [x * math.log(x / y) for x, y in zip(p, q)]
print([round(t, 4) for t in terms], round(sum(terms), 4))
print(round(sum(y * math.log(y / x) for x, y in zip(p, q)), 4))
ref = (-6.0, -4.0)
now = (-5.0, -4.8)
moved_c = now[0] - ref[0]
moved_r = now[1] - ref[1]
print(moved_c, moved_r, moved_c - moved_r)
for beta in (0.5, 4.0):
    m = beta * (moved_c - moved_r)
    print(beta, m, round(torch.sigmoid(torch.tensor(m)).item(), 4), round(-F.logsigmoid(torch.tensor(m)).item(), 5))
print(round(-F.logsigmoid(torch.tensor(0.0)).item(), 4))
```

```text
[0.3466, 0.0547, -0.1833] 0.218
0.2393
1.0 -0.7999999999999998 1.7999999999999998
0.5 0.8999999999999999 0.7109 0.34115
4.0 7.199999999999999 0.9993 0.00075
0.6931
```

(The long tails such as `-0.7999999999999998` are how Python prints decimals it cannot hold exactly; the working above rounds them.)

### D3 (the scaling line, 5 marks)

**(a)** `log10 N`: `3.3010, 4.3010, 5.3010`. `log10 L`: `log10 10 = 1.0000`, `log10 4 = 0.6021`, `log10 1.6 = 0.2041`.
**(b)** First two: `(0.6021 - 1.0000) / (4.3010 - 3.3010) = -0.398`. Last two: `(0.2041 - 0.6021) / 1 = -0.398`. The same: one line.
**(c)** `10 ^ -0.398 = 0.4`; `2 ^ -0.398 = 0.759`.
**(d)** `1.6 x 0.4 = 0.64`. A prediction.
**(e)** `6 x 200,000 x 3,000,000 = 3.6 x 10^12`. `3.6 x 10^12 / 2 x 10^9 = 1,800` seconds, which is **30 minutes**.

```py
import numpy as np
N = np.array([2e3, 2e4, 2e5]); L = np.array([10.0, 4.0, 1.6])
s, b = np.polyfit(np.log10(N), np.log10(L), 1)
print(round(s, 3), round(10 ** s, 2), round(10 ** (s * np.log10(2e6) + b), 3))
print(f"{6 * 2e5 * 3e6:.1e}", 6 * 2e5 * 3e6 / 2e9, 6*2e5*6e6/2e9)
print(round(2 ** s, 3))
```

```text
-0.398 0.4 0.64
3.6e+12 1800.0 3600.0
0.759
```

(The second number on the second line, `3600.0`, is the same sum with `D` doubled: twice the data, twice the time.)

## Section E — worked answers

### How the three tables were made

**Table 1** is Week 19's `text_ablate.py`, **unchanged except for two lines**: `SEED = 2` and `STEPS, WARMUP = 400, 50`. Run with Week 19's `ablate_model.py` and `l4lib/corpus.py`. About 21 seconds a model on this machine.

```text
8c8
< SEED = 0
---
> SEED = 2
18c18
< STEPS, WARMUP = 800, 50
---
> STEPS, WARMUP = 400, 50
```

**Table 2** is this short file, with Week 21's `textpool.py` and `trainer.py` unchanged (and Week 17's `tinygpt.py`, which `trainer.py` imports):

```py
# e2.py - Term 3 test, Table 2: four widths at 600 steps, seed 1, then the line's prediction for a fifth.
import numpy as np
from trainer import train_one, knob_count
WIDTHS = [12, 24, 48, 96]
rows = []
for d in WIDTHS:
    knobs, loss, seconds = train_one(d, steps=600, seed=1)
    rows.append((d, knobs, loss))
    print(f"width {d:3d}  knobs {knobs:7d}  validation loss {loss:.4f}")
N = np.array([r[1] for r in rows], dtype=float)
L = np.array([r[2] for r in rows])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
print("slope", round(slope, 4), " intercept", round(intercept, 4))
big = knob_count(192)
print("width 192 knobs", big, " predicted loss", round(10 ** (slope * np.log10(big) + intercept), 4))
knobs, loss, seconds = train_one(192, steps=600, seed=1)
print(f"width 192 measured {loss:.4f}")
```

```text
width  12  knobs    9813  validation loss 2.5882
width  24  knobs   26325  validation loss 2.3950
width  48  knobs   80085  validation loss 2.2241
width  96  knobs  270549  validation loss 1.9187
slope -0.0883  intercept 0.7695
width 192 knobs 983253  predicted loss 1.739
width 192 measured 1.7516
```

The text pool on this machine was 4,644,415 characters with 213 distinct characters, so `V = 213`; the knob counts follow from `V` through Week 16's hand count.

**Table 3**:

```py
# e3.py - Term 3 test, Table 3: eight new answerable questions and four unanswerable ones, on the 15-note notebook, two indexes.
import numpy as np
from l4lib import rag
chunks = rag.notebook_chunks()
ANSWERABLE = [("How many epochs did plain SGD need to match AdamW?", 0),
              ("What warmup length removed the early spike?", 1),
              ("Which dropout rate hurt training loss badly?", 2),
              ("Which temperature was the sweet spot for names?", 3),
              ("Which gated net trained slightly faster per epoch?", 4),
              ("Which head looked at the previous character?", 6),
              ("Which batch size gave the smoother loss curve?", 8),
              ("How many output tokens does one call use?", 14)]
UNANSWERABLE = ["Which dataset was used for the vision experiments?",
                "Who reviewed my notebook?",
                "What is the speed of light?",
                "How many GPUs did the cluster have?"]
STRANGER = [("Which update rule needed far more passes over the data than the adaptive one?", 0),
            ("How many initial steps of gradually raised step size stopped the early blow-up?", 1),
            ("Which random-disabling rate damaged fitting badly?", 2),
            ("What randomness setting was the best compromise for the invented words?", 3),
            ("Which of the two gated recurrent designs was a little quicker per pass?", 4),
            ("Which attention unit mostly watched the preceding letter?", 6),
            ("Which group size made the loss trace less jumpy?", 8),
            ("How many generated pieces does a single request produce?", 14)]
word = rag.VectorIndex(chunks, rag.TfidfEmbedder())
lsa = rag.VectorIndex(chunks, rag.TinyDenseEmbedder("lsa", dim=14, seed=0))
for name, ix in [("word table", word), ("LSA, 14 directions", lsa)]:
    a = sorted(ix.search(q, 1)[0].score for q, _ in ANSWERABLE)
    u = sorted(ix.search(q, 1)[0].score for q in UNANSWERABLE)
    print(name)
    print("  answerable  :", " ".join(f"{s:.3f}" for s in a))
    print("  unanswerable:", " ".join(f"{s:.3f}" for s in u))
    print("  recall@1/3/5:", [round(rag.recall_at_k(ix, ANSWERABLE, k), 2) for k in (1, 3, 5)])
    st = sorted(ix.search(q, 1)[0].score for q, _ in STRANGER)
    print("  stranger    :", " ".join(f"{x:.3f}" for x in st))
    print("  stranger recall@1/3/5:", [round(rag.recall_at_k(ix, STRANGER, k), 2) for k in (1, 3, 5)])
    taus = [0.10, 0.20, 0.30] if name == "word table" else [0.60, 0.80, 0.90]
    for tau in taus:
        ans = sum(s >= tau for s in a)
        ref = sum(s < tau for s in u)
        sa = sum(x >= tau for x in st)
        print(f"  tau {tau:.2f}: answered {ans}/8, unanswerable refused {ref}/4, errors {(8 - ans) + (4 - ref)}, stranger answered {sa}/8")
```

```text
word table
  answerable  : 0.225 0.349 0.366 0.459 0.496 0.541 0.543 0.565
  unanswerable: 0.000 0.000 0.138 0.138
  recall@1/3/5: [1.0, 1.0, 1.0]
  stranger    : 0.000 0.105 0.117 0.120 0.166 0.175 0.176 0.269
  stranger recall@1/3/5: [0.12, 0.38, 0.88]
  tau 0.10: answered 8/8, unanswerable refused 2/4, errors 2, stranger answered 7/8
  tau 0.20: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 1/8
  tau 0.30: answered 7/8, unanswerable refused 4/4, errors 1, stranger answered 0/8
LSA, 14 directions
  answerable  : 0.942 0.945 0.946 0.950 0.970 0.971 0.972 0.980
  unanswerable: 0.654 0.737 0.768 0.786
  recall@1/3/5: [1.0, 1.0, 1.0]
  stranger    : 0.553 0.621 0.622 0.652 0.670 0.702 0.732 0.763
  stranger recall@1/3/5: [0.38, 0.75, 0.75]
  tau 0.60: answered 8/8, unanswerable refused 0/4, errors 4, stranger answered 7/8
  tau 0.80: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 0/8
  tau 0.90: answered 8/8, unanswerable refused 4/4, errors 0, stranger answered 0/8
```

These eight questions were **written by the test's author after reading the notes**, and the stranger set was written second, in words chosen to avoid the notebook's; both are small and neither is a measurement of how the system does for real users. That is part of what E(c)(iv) is asking.

### E(a) — Table 1 (4 marks)

**(i)** Validation minus full (`1.939`): no mask `1.638 - 1.939 = -0.301`; no pos `1.854 - 1.939 = -0.085`; no res `2.852 - 1.939 = +0.913`; no norm `1.763 - 1.939 = -0.176`. Only **no residual** is clearly worse (by `0.913`).
**(ii)** A **leak**. With no mask each place can read the character that comes next, which is the answer; the model is reading, not predicting, and its sample is the shape of that shortcut (`tatattt...`). Here the number (`1.638`) is not as dramatic as Week 19's `0.077` because only 400 steps were run, but the sample already shows it. The test: change **one later character** and see whether the scores at **earlier** places move; they cannot move with a mask, and they do without one (Week 19's `leak_test.py`: `0.000000` against `0.001437`).
**(iii)** The sign of "no pos" **flips** between two runs (better here, worse in Week 19), and "no norm" is better in both. A difference of `0.1` to `0.2` on one seed and a shortened run is not something to rank on; only "no residual" (+0.9, both runs) and "no mask" (a leak) are clear. It would take more seeds, and the full steps, to say anything about "no pos" and "no norm".
**(iv)** Both of its numbers (`2.841`, `2.852`) are far worse than the full model's (`1.935`, `1.939`): it has barely learned anything, so there is nothing to overfit and the two numbers agree. A small gap is only good news when both numbers are good.

### E(b) — Table 2 (4 marks)

**(i)** `(0.2830 - 0.4130) / (5.4322 - 3.9918) = -0.1300 / 1.4404 = -0.0903`. It is close to `-0.0883` but not equal: the printed slope is the best line through **all four** points, and the four are not exactly on a line (the end points are two of them).
**(ii)** `10 ^ -0.0883 = 0.816`. Ten times the knobs multiplies the loss by about `0.82`. "Lose 8.8%" is wrong: the slope is an exponent on log-log paper, and the ratio is `10 ^ slope`. (For two times the knobs: `2 ^ -0.0883 = 0.941`.)
**(iii)** `1.7516 - 1.739 = +0.0126`, about `0.7%` worse than the line said. A prediction is the place where a line fitted to **smaller** models says a bigger one will be. The miss shows the line was good **at this size, on one seed, at 600 steps**. It does not show the line will keep going: width 192 has `3.6` times the knobs of the biggest point, which is a short step.
**(iv)** `D = 600 x 32 x 64 = 1,228,800` characters. `C = 6 x 983,253 x 1,228,800 = 7.249 x 10^12`, about **7.2 x 10^12**. Anything that stops the table being a law: one seed, only four points, only 600 steps, every model reads the same number of characters (so the bigger models are not given more to read), a text pool particular to this computer.

### E(c) — Table 3 (4 marks)

**(i)** **Stranger answered: 1/8.** The questions written after reading the notes share the notebook's words and score `0.225` to `0.565`; the stranger's wording shares fewer, and scores `0.000` to `0.269`, so `tau = 0.20` refuses seven of the eight.
**(ii)** The word table's best answerable score is `0.565`, below `0.80`, so it would answer **0 of 8**. A threshold belongs to one index: the LSA scores sit between `0.55` and `0.99`, the word table's between `0.00` and `0.57`.
**(iii)** Chance recall@3 is `3 / 15 = 0.20`; the word table's stranger recall@3 is `0.38`, so it beats chance by `0.18`. One question is worth `1 / 8 = 0.125`, so that is about one and a half questions.
**(iv)** *Model answer (about 70 words):* "Table 3 supports that, on questions in the notebook's own words, retrieval finds the right note every time and one threshold separates the answerable from the unanswerable. It cannot tell me how it does for other people: in a stranger's words recall@1 is `0.12`, and eight and four questions are too few to rely on. And a recall number says nothing about whether an answer is right. My first question is: who wrote the questions?"

## Part 2 — the demo, reference output

Run each file from the folder that holds `l4lib/`, with `bpe.py`, `bench.py` and `guard.py` beside it. Nothing here is random except where seeded.

**`demo1.py`**

```py
# demo1.py - Term 3 test, Demo 1: check the hand work of D1 and D2 with the machine.
import math
import torch
import torch.nn.functional as F
from bpe import train, encode, decode, make_vocab

text = "ab ab ab abc abc"
merges = train(text, 5, verbose=True)
print("merges learned:", len(merges))
vocab = make_vocab(merges)
for s in ["abcab", "cab", "ba"]:
    ids = encode(s, merges)
    print(repr(s), ids, [vocab[i] for i in ids], decode(ids, merges) == s, len(s.encode("utf-8")) / len(ids))
print("round trip of a mixed string:", decode(encode("né 🙂", merges), merges) == "né 🙂")

p, q = [0.5, 0.3, 0.2], [0.25, 0.25, 0.5]
print("KL(p from q):", round(sum(x * math.log(x / y) for x, y in zip(p, q)), 4),
      " KL(q from p):", round(sum(y * math.log(y / x) for x, y in zip(p, q)), 4))
gap = (-5.0 - -6.0) - (-4.8 - -4.0)
for beta in (0.5, 4.0):
    m = torch.tensor(beta * gap)
    print(f"beta {beta}: margin {m.item():.1f}  loss {(-F.logsigmoid(m)).item():.5f}")
```

```text
merge 1 (97, 98) -> 256 count 5
merge 2 (256, 99) -> 257 count 2
merges learned: 2
'abcab' [257, 256] [b'abc', b'ab'] True 2.5
'cab' [99, 256] [b'c', b'ab'] True 1.5
'ba' [98, 97] [b'b', b'a'] True 1.0
round trip of a mixed string: True
KL(p from q): 0.218  KL(q from p): 0.2393
beta 0.5: margin 0.9  loss 0.34115
beta 4.0: margin 7.2  loss 0.00075
```

The sentence for (ii): *"every byte can be written, so nothing is lost; that says nothing about whether two merges make good tokens."* (The mixed string is mostly single bytes here, which is itself a sign.)

**`demo2.py`**

```py
# demo2.py - Term 3 test, Demo 2: the scaling line of D3, and the harness pieces of Week 23. Stand-in, not a model (FakeClient is scripted).
import copy
import numpy as np
from bench import TESTS, constant_baseline, check_frozen, FROZEN, fingerprint
from guard import BudgetGuard, BudgetExceeded
from l4lib.fakellm import FakeClient

N = np.array([2e3, 2e4, 2e5])
L = np.array([10.0, 4.0, 1.6])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
print("slope", round(slope, 3), " x10 knobs ->", round(10 ** slope, 3), " x2 knobs ->", round(2 ** slope, 3))
print("prediction at N = 2e6:", round(float(10 ** (slope * np.log10(2e6) + intercept)), 3), "(a prediction, not a measurement)")
print("C = 6ND:", f"{6 * 2e5 * 3e6:.1e}", " seconds at 2e9 per second:", 6 * 2e5 * 3e6 / 2e9)

best = constant_baseline()[0]
print("floor:", round(best[0] * 100, 1), "%")
edited = copy.deepcopy(TESTS)
edited[0]["gold"]["urgency"] = 2
print("same fingerprint after an edit:", fingerprint(edited) == FROZEN)
try:
    check_frozen(edited)
except AssertionError as e:
    print("refused:", e)

g = BudgetGuard(limit_usd=0.05)
for i in range(10):
    try:
        g.record(0.02)
    except BudgetExceeded as e:
        print("guard stopped at call", i + 1, "-", e)
        break
print(FakeClient(seed=0))
```

```text
slope -0.398  x10 knobs -> 0.4  x2 knobs -> 0.759
prediction at N = 2e6: 0.64 (a prediction, not a measurement)
C = 6ND: 3.6e+12  seconds at 2e9 per second: 1800.0
floor: 43.8 %
same fingerprint after an edit: False
refused: the test set changed since it was frozen
guard stopped at call 3 - spent $0.0600 over 3 calls, limit $0.0500
<FakeClient [stand-in, not a model] seed=0 calls=0>
```

`FakeClient` is a **stand-in, not a model**: its label is in its printout.

**`demo3.py`**

```py
# demo3.py - Term 3 test, Demo 3: the ceiling, the cosine, the gate and the citation check (writer: stand-in, not a model).
import numpy as np
from l4lib import rag

print("ceiling (n + 1) / 6 for n = 0..5:", [round((n + 1) / 6, 3) for n in range(6)])
print("wobble on 500 prompts at 0.833:", round(float(np.sqrt(0.833 * 0.167 / 500)), 3))

notes = np.array([[3.0, 4.0], [4.0, 3.0], [0.0, 5.0]])
query = np.array([0.0, 1.0])

def cosine(x, y):
    return float(x @ y / (np.sqrt(x @ x) * np.sqrt(y @ y)))

scores = np.array([cosine(n, query) for n in notes])
print("cosines:", [round(float(s), 2) for s in scores], " top 2:", np.argsort(-scores)[:2].tolist())
print("dots   :", (notes @ query).tolist(), " top 2:", np.argsort(-(notes @ query))[:2].tolist())
print("row 0 tripled: dot", float((3 * notes[0]) @ query), " cosine", round(cosine(3 * notes[0], query), 2))

chunks = rag.notebook_chunks()
word = rag.VectorIndex(chunks, rag.TfidfEmbedder())
for q in ["Which temperature was the sweet spot for names?", "Which dataset was used for the vision experiments?"]:
    for tau in (0.10, 0.20):
        r = rag.rag_answer(q, word, k=3, threshold=tau)
        print(f"tau {tau:.2f} | best score {r['hits'][0].score:.3f} | refused {r['refused']} | cited {r['cited']} | ok {r['citations_ok']} | {r['answer'][:50]!r}")

served = {"1", "2", "4"}
for cited in ({"2"}, {"2", "9"}):
    print(sorted(cited), "inside served:", cited <= served, " not served:", sorted(cited - served))
```

```text
ceiling (n + 1) / 6 for n = 0..5: [0.167, 0.333, 0.5, 0.667, 0.833, 1.0]
wobble on 500 prompts at 0.833: 0.017
cosines: [0.8, 0.6, 1.0]  top 2: [2, 0]
dots   : [4.0, 3.0, 5.0]  top 2: [2, 0]
row 0 tripled: dot 12.0  cosine 0.8
tau 0.10 | best score 0.496 | refused False | cited [3] | ok True | '0.8 was the sweet spot. [3]'
tau 0.20 | best score 0.496 | refused False | cited [3] | ok True | '0.8 was the sweet spot. [3]'
tau 0.10 | best score 0.138 | refused False | cited [2] | ok True | 'Dropout 0.5 hurt training loss badly and only help'
tau 0.20 | best score 0.138 | refused True | cited [] | ok None | 'NOT IN NOTES'
['2'] inside served: True  not served: []
['2', '9'] inside served: False  not served: ['9']
```

The vision question is **not in the notes** and is **answered** at `tau = 0.10` with a citation that passes the check: the passing check proves only that note 2 was one of the notes handed to the writer.

---

## 🧭 What this test does and does not show

**Shows:** whether the student can run code and arithmetic by hand for Weeks 19–26: delete one part and read the damage honestly (and spot a leak), merge pairs of bytes, read a straight line on log-log paper and use `6ND`, work a KL and a pair loss, treat a prompt loop as an instrument with a floor, a frozen set and a guard, and read a cosine, a recall number and a threshold with the question "who wrote the questions?" Then whether the student can **prove** it on a machine, aloud, in front of someone.

**Does not show:**

- **Anything about a real model.** The writer behind `rag.rag_answer` and `FakeClient` are **stand-ins, not models**; the TinyGPTs are real but tiny and run on text typed by the author. Nothing here says how a large language model behaves.
- **That the student knows the maths without the numbers.** Every number is small; the paper tests method, not stamina.
- **That the three tables are representative.** Table 1 is one seed and a shortened run; Table 2 is one seed on four small models and a text pool that belongs to the machine; Table 3 has eight questions written by the course author. A student who says exactly that has understood Term 3.
- **How a student will do on Term 4.** Weeks 28 to 36 build tools, attacks and a capstone on top of the guard, the frozen set, the sets and the retrieval of this term; the grid tells you which of those to repair first.

*Next: Week 27 is the review week, then Term 4 begins with tools and the loop.*
