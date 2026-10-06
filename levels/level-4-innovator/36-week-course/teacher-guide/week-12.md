# Week 12 — Teach a Network to Invent Names

[⬅ Week 11](week-11.md) · [Course Home](../README.md) · [Week 13 ➡](week-13.md) · [Student Guide](../student-guide/week-12.md) · [Workbook](../workbook/week-12.md)

---

![Map of the 36 weeks with Week 12, Teach a Network to Invent Names, highlighted in Term 2](../figures/fig-w12-0-where-this-fits.svg)
*Figure 12.0 — Week 12 trains a gated loop on real names, the first sequence model that writes.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~60-75 min, of which about 25 seconds is the computer training) |
| **Type** | 🟩 Lab — the student turns 231 typed names into numbers, builds the shifted input that **teacher forcing** needs, trains a character model with a loss that **skips the padding**, holds 31 names back to see train against validation, generates names one letter at a time, and **counts how many already exist** |
| **Big idea** | **Training** hands the model the *true* previous letter at every step, so every input is known before the model runs and nothing is sampled inside the loop. **Generating** hands the model *its own* previous guess, so the next input does not exist until the last answer does: the steps of one name must run in order, no shortcut. The same weights do both jobs, and the two jobs are not the same test. A model that scores well on the first can be a copying machine on the second: here, 80% of what it "invents" is a name it was trained on. |
| **New vocabulary** | **teacher forcing** · **shift right** / start token · **padding** and **padding mask** (`ignore_index`) · **train loss** / **validation loss** (met in Week 5, used now on text) · **generate** / **autoregressive** · **novelty rate** (the share of generated names that are not in the list). (**Overfitting**, **dropout**, **embedding**, **LSTM cell**, **cross-entropy** and **softmax** are *already theirs*: Weeks 5, 8, 11, Level 3 Weeks 14 and 26. Say so, and use them.) |
| **New maths** | *(none)*. One old idea gets a new job: **average surprise** (`-ln p`, Level 3 Week 14) is the loss, and the question of the day is *which positions get averaged*. See the 🔢 section. |
| **New syntax** | `F.cross_entropy(..., ignore_index=)` · `torch.cat` (already met in Level 3 Week 27; used here to shift the input) · `torch.full` · `import torch.nn.functional as F`. That is the ladder's list: three constructs and the import. **One off-ladder helper** (`rng.random()` inside the received function `draw`) is declared in section 4. |
| **Dataset** | The 231 typed names in `l4lib.names` (lowercase, letters only, all distinct; longest 7 letters). 200 train / 31 held back for validation, by a seeded shuffle. **Nothing downloads. No internet.** |
| **Model** | A **real, small LSTM character model** (`NameLSTM`: an embedding of 24 numbers, an `nn.LSTMCell` of 64, dropout 0.3, a linear layer to 28 scores; **25,532 numbers**), trained for real for 800 full-batch steps. **There is no scripted backend and no stand-in anywhere in this week.** It is a toy: it has read 200 names. |
| **Materials** | Laptop with Python 3 and torch (nothing new to install) · the folder that contains `l4lib/` · a calculator with an `ln` key (a phone in calculator mode is fine; **airplane mode on**) · the printed **name quiz** (Hook) · workbook pages 12.1-12.6 · a timer |
| **Prep time** | 30 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | The student's whole file (`week12.py`, seven blocks) runs in **about 6 seconds** (three trainings: 800 steps on 200 names, 100 steps, and 800 steps on all 231). The teacher-only blocks add about **9 seconds**. Anything over **60 seconds** means something is wrong (see Fallback). |

> **⚠️ Watch out:** two things go wrong this week. **First, "new" gets heard as "creative" or "good".** The model trained for 800 steps reproduces a training name **four times out of five** (159 of 200), and the ones that are not in the list are mostly near-copies. The same recipe stopped at step 100 has *almost no* names from the list (1 of 200) and the names are mostly not names (`dareltl`, `gmana`). "Not in the list" is a count a loop can make; "a name" is a judgement a person makes by reading. The quiz in the Hook is there so that the student makes the judgement **before** they see the count. **Second, the validation loss will look like a bug.** It gets *worse* after step 80 and ends at `3.417`, which is above the `3.332` of a model that knows nothing. It is not a bug; it is Week 5's memorising, on letters, and the Clinic (mistakes 5 and 6) shows the two ways to get a validation number that *is* wrong.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Build the shift-right input** with `torch.full` and `torch.cat`, and say in one sentence why it exists: "at each step the model is shown the letter *before* the one it must predict".
2. **Say what teacher forcing is**: "training feeds the true previous letter, so the inputs are all known in advance"; and the contrast: "generating feeds the model's own pick, so each input waits for the last answer".
3. **Use `F.cross_entropy(..., ignore_index=PAD)`** and say what it changes: the padding positions leave the average. Give the number that shows it (`0.5857` against `1.1513` on the toy, `444` of `1,848` positions in the real data).
4. **Report train loss and validation loss** for the same model and read the gap: `0.906` against `3.417` at step 800.
5. **Measure novelty**: generate 200 names with a seeded generator, count how many are already in the training list, and say what the count does and does not show.

Observable evidence: the hand tables on workbook pages 12.1-12.3, the loss table on 12.4, the novelty table on 12.5 (two models, counts copied in full), and a short report on 12.6 in which **every number was printed by the student's own run**.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** (the seven student blocks, the teacher-only blocks `T1`, `T2`, `T3` and `K1`) and in the **🐞 Debugging Clinic** was run, in order, in **one shared session** on a CPU with one thread and the seeds shown. The seven student blocks are the pieces of **one file, `week12.py`**, pasted one under the other with no gap: each later block uses names defined by an earlier one. The Clinic blocks are *deliberate mistakes*, each marked, each run in a copy of the session as it stood after block 7; their tracebacks are real. **Timing is the only thing that varies run to run; every other number repeated exactly on a second full run on the same machine** (torch `2.2.1`, Python 3.10). A different CPU or PyTorch build can move the last digit of a loss, and a count of generated names can move by a name or two; the shape of every table does not move. Tracebacks show `/home/you/l4/...` for the path, and the long middle of a torch traceback is replaced by `... frames inside torch (elided) ...`; **the last line is always the real, complete last line.**

### 1. What the student is doing today, in one paragraph

Last week an LSTM was never trained. Today it reads names. They first turn names into numbers (`aarav` becomes `[2, 2, 19, 2, 23, 1, 0, 0]`: letters, an end-of-name marker, then padding) and build the second tensor that teacher forcing needs, the same names **shifted one place right** with a start token in front. They do a loss **by hand** on four steps, and see that counting padding steps the model finds easy would halve the number without the model having learned anything (`1.1513` against `0.5857`). They build the model, see that an untrained one scores `3.3455` (about `ln 28 = 3.3322`), and train one on **200** names, printing train and validation loss as it goes: train falls to `0.906`, validation reaches `2.308` at step 100 and then **climbs** to `3.417`. They write nothing new to generate: they receive a short `draw` function (a seeded dice-roll weighted by the model's probabilities; Week 13 opens it), run the generator, and count: of 200 names, **159 are names from the training list**. They then stop the same recipe at step 100 and count again: **1**. The last block trains on all 231 names, for Week 13.

### 2. 🔢 The maths you need — taught to you first

**No new idea.** One old idea gets a new job. Do each of these yourself, once, with a calculator, before class.

**(a) The loss is an average of surprises (Level 3 Week 14).** For each step the model gives a probability to the *true* next letter `p`; the surprise is `-ln p`; the loss is the average. Four steps with `p = 0.5, 0.25, 0.8, 0.1`:

| Step | `p` on the true letter | surprise `-ln p` |
|:--:|:--:|:--:|
| 1 | 0.5 | 0.6931 |
| 2 | 0.25 | 1.3863 |
| 3 | 0.8 | 0.2231 |
| 4 | 0.1 | 2.3026 |

Average `= 4.6051 / 4 =` **`1.1513`**. (Block 2 prints each line.) `F.cross_entropy` is the same arithmetic in one call: it is Level 3 Week 26's `nn.CrossEntropyLoss` under its function name, and it applies the softmax itself, so it takes **scores**, not probabilities. Block 2 feeds it `ln p` as scores so that the softmax hands back exactly our `p`.

**(b) Padding is a free answer, and counting it flatters you.** Every name is padded to 8 steps. `uma` has 4 real targets (`u`, `m`, `a`, EOS) and 4 padding targets. A model that has learned nothing about names can still learn "after EOS comes padding, with 98% certainty", which costs `-ln 0.98 = 0.0202` per step. Put four of those under our four real steps and divide by 8:

`(4.6051 + 4 x 0.0202) / 8 =` **`0.5857`**, half the honest `1.1513` with no better guess at a single letter. `ignore_index=PAD` removes those rows from **both** the top and the bottom of the average (the top is the sum, the bottom is the count), so the honest number is `4.6051 / 4`. In the real data `444` of the `1,848` positions (`24.0%`) are padding, and the number of real targets is `1,404` (5.08 letters per name, plus one EOS).

**(c) Reading a loss as a number of letters (teacher-only reading; the student has `exp` from Level 3).** `e ** loss` is "how many equally likely letters the model behaves as if it were choosing between". `K1` prints it: a model that knows nothing, `28.0`; the letter-frequency baseline on validation, `15.4`; the model at step 100 on validation, `10.1`; at step 800 on train, `2.5`; at step 800 on validation, **`30.5`**. The last one says: on names it has not seen, the 800-step model is **worse than a model that knows nothing**, because it is confident and wrong. It is a reading aid, not a result; do not put `e ** loss` on the student's page.

**(d) Train minus validation is Week 5's gap.** Week 5 found the best validation epoch, the best validation loss and the final validation loss, and said *the column that tells the truth is validation*. Nothing new: `0.906` train against `3.417` validation is a gap of 2.5, and the lowest validation (`T1`) is `2.301` at step 80.

> **🚫 What you must NOT do with the maths.** (1) **Do not say "perplexity".** It is not on the ladder; `e ** loss` stays in your pocket (c). (2) **Do not derive the loss from probability or write a likelihood.** "The average surprise at the true letter" is the whole definition. (3) **Do not call a validation loss above `3.332` "impossible".** It is possible when a model is confident and wrong, and today's model does it. (4) **Do not compare `0.906` with Week 13's `1.026`** as if one were a better model: `0.906` is the *train* loss with dropout off, `1.026` is the last *training step* of a different run (all 231 names) with dropout on. Block 7 prints both numbers for the same run.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Status |
|---|---|
| The 231 names | **Typed** by the course author (`l4lib.names`), in the Level 4 reference module. All distinct, lowercase, no real person's data. They are not a sample of any population. |
| `NameLSTM`, the training, every loss, every generated name, every count | **Real.** PyTorch on the CPU, seed 0 (training) and the generator seeds shown. **Nothing is scripted.** |
| The 200 / 31 split | **Ours**: a seeded shuffle, 200 train, 31 validation. 31 names is about 200 letters; the validation number is **noisy** (it moves from `3.417` to `3.668` to `3.490` across three training seeds, `T2`). |
| `draw` | **Plain Python**: a running total walked until it passes a seeded random number. It does what `torch.multinomial` does in Week 13. Received, not typed. |
| "Novel" | **Ours**, and narrow: *the string is not in the list the model was trained on.* It says nothing about whether a human would call it a name (`amira`, `erich` are names in the world; `gmana` is not), or whether it is good. |
| The letter-frequency baseline (`T1`) | **A measurement, not a model**: predict every letter from how often it appears, ignoring context. It is there so that `2.3` has something to be compared with. |

> **🚫 What you must NOT claim about today's numbers.**
> 1. **"The model invents names."** At 800 steps **79.5%** of 200 draws (159) are names from the training list, and the 200 contain only **147 distinct** strings. The honest sentence is: *"it mostly reproduces its training list, and a fifth of the time it makes a string that is not in it."* Three training seeds, 200 draws each (`T2`): `80.5%`, `86.0%`, `86.5%` in the list.
> 2. **"Stopping at step 100 is better."** It is *more novel* (`0.5%` in the list, `199` distinct) and the lowest validation loss is near there (`2.301` at step 80), but its names are mostly not names, and the validation loss `2.308` is still only a little below the letter-frequency baseline (`2.735`). We did not rate the names; the student reads twenty and judges, and that judgement is theirs, not a number.
> 3. **"Validation loss above `ln 28` means something is broken."** It means the model is confident and wrong on names it has not seen. The bug version is mistake 5 in the Clinic, where validation is near **zero**.
> 4. **"Teacher forcing makes training parallel in time."** It makes every input *known in advance*, so the loss needs no sampling inside the loop (`T3`: the step-by-step scores and the whole-batch scores agree exactly, gap `0.0e+00`). **The 8 time steps are still a loop inside the LSTM**, in training as in generation. What generation lacks is not the loop or the batch (generation can also run many names side by side); it is that step t+1's input is step t's sample, so the steps of one name cannot be known ahead of time. (Week 14's attention is what removes the loop in time.) `T3` times it: scoring 200 known names takes about 1.3 ms, generating 200 new ones about 29 ms, roughly **20 times** longer; this compares one batch of 200 with 200 batches of 1, so it is mostly a batching effect, and the ratio moves with the machine.
> 5. **Setting the reference module's numbers beside ours.** The module trains on all 231 names and samples with `torch.multinomial` at temperature 1.0 and finds 12 of 60 new; our generator and seeds are different and we count 33 of 200 new for the 231-name model (`16.5%`). The *shape* agrees (most of what it writes is in its list); the numbers are not a reproduction. The module's "`dira`" and "`arjav`" are its samples, not ours.
> 6. **Anything about a real language model.** A real model trains on billions of characters and does not memorise one list of 231. Today is the same two loops (train with the truth, generate on your own output) at a size where you can read every output.

### 4. The three new constructs and the import, for somebody who has never seen them

**(a) `F.cross_entropy(scores, labels, ignore_index=PAD)` — loss that skips rows.** (The snippets in this section are excerpts of the blocks below, shown for reading, not blocks to run.)

```text
import torch.nn.functional as F
loss = F.cross_entropy(scores.reshape(-1, 28), targets.reshape(-1), ignore_index=0)
```

Read as: *"for every row of 28 scores, take the softmax, find the probability of the true id, take `-ln`, and average over the rows **whose label is not 0**."* Two shapes must be right: `scores` is `(rows, 28)` and `labels` is `(rows,)` with one whole number per row. Our model returns `(231, 8, 28)` and the targets are `(231, 8)`, so **both are flattened**: `scores.reshape(-1, 28)` (`-1` means "work out this number": 1,848) and `targets.reshape(-1)`. Forgetting it is Clinic 3; a wrong shift is Clinic 2. `ignore_index=0` works because PAD is id 0 and no real letter has id 0. **`import torch.nn.functional as F`** is the convention: `F.` is the namespace of functions that have no knobs of their own (a loss, a softmax); Level 3 used the `nn.CrossEntropyLoss()` class to avoid it, and Week 13 uses `F.softmax`.

**(b) `torch.full(shape, value)` — a tensor filled with one number.**

```text
start = torch.full((231, 1), 0)      # 231 rows, 1 column, every entry 0 (the start token)
```

Read as: *"make a grid of this shape and write this number in every cell."* The shape is a **tuple**: `torch.full(231, 0)` is Clinic 1. The start token is the id of PAD (0) on purpose: nothing real is ever 0, so "0 in the input" can only mean "nothing has been said yet" (or, after the name ends, "nothing more to say").

**(c) `torch.cat([a, b], dim=1)` — glue along an axis that already exists.** (Known from Level 3 Week 27; the student has used it for `dim=0`.)

```text
inputs = torch.cat([start, data[:, :-1]], dim=1)     # (231, 1) next to (231, 7)  ->  (231, 8)
```

Read as: *"put the column of start tokens on the left of the names with their last column removed."* `data[:, :-1]` is "every row, every column except the last" (slices are Level 2). After it, column `t` of `inputs` is column `t - 1` of the targets. That **is** the shift. Drop the `[:, :-1]` and the result is `(231, 9)`, which is Clinic 2. For the name `anika` the student should be able to read the table from block 1: at step 2 the input is `15` (`n`), the letter just said, and the target is `10` (`i`), the letter to come.

**(d) The one off-ladder helper, `draw`.** The student **receives** it (a pasted block, not something to type or to be examined on). Inside it: `torch.softmax(scores, dim=0)` (Level 3 Week 26's function, on a 1-D list of 28 scores, so `dim=0`), `.tolist()`, a plain `for` loop with a running total, and **`rng.random()`**: a float between 0 and 1 from the seeded `np.random.default_rng` the student has used since Level 3 (the same family as `rng.normal`, Week 5). That one method is not on the ladder. Say it in one sentence: *"the dice-roll; a number between 0 and 1. The loop walks along the probabilities, adding them up, until the total passes the roll."* Week 13 replaces the whole function with `torch.multinomial`, and only then does the student *write* a chooser.

### 5. The other code the student types — nothing new, but note these

All old: `class` with `__init__` / `super().__init__()` / `forward` (Level 3 Week 23; Week 5 already used one), `nn.Embedding` (Week 8), `nn.LSTMCell` and the **pair** `(h, c)` (Week 11; the state as a pair is still the commonest error), `nn.Dropout` and `model.train()` / `model.eval()` (Week 5, Level 3), `torch.stack` (Week 10), `torch.randperm(n, generator=g)` (Week 5), `AdamW` with `weight_decay=` (Week 3), `clip_grad_norm_` (Week 6), `set_to_none=True` (Week 2), `with torch.no_grad():`, `.item()`, `.tolist()`, `sum(p.numel() for p in model.parameters())` (Level 3 Week 22), `zip`, f-strings with `:.3f` and `:.1%`, `in` on a `set`, list comprehensions, `range`, `math.log` and `math.exp` (Level 3), `np.random.default_rng(seed)` (Level 3), and the two imports from `l4lib.names`. **Two patterns to point at.** (i) `tensor != PAD` gives a grid of True/False and `.sum()` counts the Trues (block 3 uses it once to count real positions). (ii) `inputs[rows]` with `rows` a tensor or a list of row numbers picks those rows (a copy, in that order).

**Not used today, on purpose**, because they are later rungs: `F.softmax` and `torch.multinomial` (Week 13), temperature, top-k, top-p (Week 13), attention (Week 14), `torch.arange` (Week 16), `nn.LSTM` as the main layer of a model (the student has it from Week 11 but today's model uses the cell so that *one step* exists for generation). **The teacher-only blocks use a few things the student never sees** (`torch.bincount`, `min(..., key=lambda ...)`, `time.perf_counter`, a hand-written optimizer loop with underscore names) and are marked. Do not paste them into the student's file.

### 6. What the numbers will say

Read these before class so nothing surprises you. **Every number is printed by the blocks below.**

- **The data** (block 1): 231 names, vocabulary 28 (26 letters, PAD, EOS), longest name 7 letters plus EOS so 8 steps. `anika` is `[2, 15, 10, 12, 2, 1, 0, 0]`. `inputs`, `targets`, `data` all `(231, 8)`; `start` `(231, 1)`.
- **The toy loss** (block 2): `0.6931, 1.3863, 0.2231, 2.3026`, average `1.1513`; padding counted `0.5857`, padding ignored `1.1513` (equal to the by-hand average).
- **The untrained model** (block 3): 25,532 numbers; scores `(231, 8, 28)`; 1,848 positions, **1,404 real, 444 padding**; loss with padding counted `3.3629`, ignored `3.3455`; `ln 28 = 3.3322`. (All three are within half a per cent: an untrained model is a near-uniform guess.)
- **The training** (block 4), 200 names, 800 steps, seed 0:

| step | train | validation |
|:--:|:--:|:--:|
| 0 | 3.346 | 3.349 |
| 100 | 1.960 | 2.308 |
| 200 | 1.431 | 2.544 |
| 300 | 1.103 | 2.880 |
| 400 | 0.984 | 3.077 |
| 600 | 0.921 | 3.314 |
| 800 | 0.906 | 3.417 |

  The last training step (dropout on) is `1.001`, not `0.906`: the printed table is measured with dropout **off** (`model.eval()`), the training loop's own number is with it **on**. The validation curve has its lowest point at step 80 (`T1`: `2.301`).
- **Twenty names** (block 5): `olen, vito, tatiana, felix, naya, oona, leena, maren, deepak, alina, alina, pavel, willem, yash, serge, rusha, yash, katya, juno, argek`. Count by eye: **17 of these 20 are in the list** (`alina` and `yash` each come up twice); `naya`, `rusha` and `argek` are not.
- **The audit** (block 6, generator seed 1): 800 steps: **159 of 200 in the training list** (79.5%), 0 in the held-back list, 41 in neither; 147 distinct. Stopped at step 100 (train `1.960`, validation `2.308`): **1** in the list, 0 held back, 199 in neither, 199 distinct.
- **The keeper** (block 7), all 231 names, generator seed 2: loss on all names `0.934` (dropout off); last training step `1.026` (dropout on; this is the number Week 13's `namelm.py` prints as its check). 167 of 200 in the list (83.5%), 33 new, 156 distinct.
- **Seeds** (`T2`, three training seeds, generator seeds 10-12):

| training seed | steps | train | validation | in train list | distinct of 200 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0 | 100 | 1.960 | 2.308 | 1 (0.5%) | 197 |
| 0 | 800 | 0.906 | 3.417 | 161 (80.5%) | 146 |
| 1 | 100 | 1.919 | 2.331 | 4 (2.0%) | 200 |
| 1 | 800 | 0.906 | 3.668 | 172 (86.0%) | 148 |
| 2 | 100 | 1.942 | 2.269 | 3 (1.5%) | 200 |
| 2 | 800 | 0.907 | 3.490 | 173 (86.5%) | 142 |

  Spread across seeds: train loss to the third digit, **validation to 0.25**, in-list share by 6 points. The 100-step versus 800-step difference (under 2% against over 80%) is far bigger than any spread; the exact validation number is not something to quote beyond one decimal.
- **The baseline** (`T1`): letter frequencies only, train `2.789`, validation `2.735`. The 100-step model (`2.308`) beats it by 0.4; the 800-step model (`3.417`) loses to it by 0.7.
- **Step by step against whole batch** (`T3`): biggest gap `0.0e+00`.

![Two rows of eight cells for the name anika: the input row starts with START then a n i k a EOS PAD, the target row is a n i k a EOS PAD PAD, with arrows from each target to the next input](../figures/fig-w12-1-shift-right-names.svg)
*Figure 12.1 — Shift right: every step is asked for the letter that comes next, and each answer becomes the following question.*

![Bars of surprise for the eight positions of uma, four real and four tiny padding ones, and two bars of average loss, 1.1513 with padding ignored and 0.5857 with it counted](../figures/fig-w12-2-padding-flatters-loss.svg)
*Figure 12.2 — Counting the padding halves the loss without the model learning anything; ignore it.*

### 7. The honest limits of today

1. **One list of 231 names, one architecture, 25,532 numbers, one learning rate.** The results are about *this* recipe on *this* list. Not tested: a bigger list, a smaller model, more dropout.
2. **A validation set of 31 names is tiny.** Its loss moves by a quarter across three training seeds (`T2`). It says "much worse than train", not "exactly 3.4".
3. **We did not rate the quality of the names.** The student reads twenty and judges; we count. Do not invent a quality score for the student's page.
4. **The 800 steps are not tuned.** The lowest validation is at step 80; the course recipe keeps 800 because Week 13 and the reference module use it. Say this out loud: *"800 steps is the recipe we carry to next week, not the best stopping point."*
5. **The generator uses plain sampling at the model's own probabilities** (no temperature, no top-k). What greedy, a flatter or a sharper draw would do is Week 13's question; **do not pre-empt it**. If asked, say "next week, with numbers".
6. **The `0.5%` at step 100 is partly luck of the draw and partly the weak model.** Across seeds it is `0.5%` to `2.0%`. The quantity measured, "in the training list", can only be large when the model has memorised.
7. **"In the held-back list: 0."** Zero of 200 draws equal any of 31 held-back names. That is what you would expect from a model that is copying its *training* list; it is not evidence that the model cannot generalise, and the 31 names are too few to be a test of generalisation by matching. Do not build a story on it.
8. **The dropout 0.3 and weight decay 0.1 are the reference module's.** Weeks 3 and 5 taught both; the student is not asked to tune them today.

### 8. The three misconceptions you will actually meet

1. **"The model made those names up."** It has 25,532 numbers and has seen 200 names 800 times. Fix: block 6, the count. Then: *"What would a model that really understood how names work do with `amara`, which it never saw?"* (Give `amara` a good score. It does not: validation is `3.417`.)
2. **"Teacher forcing is cheating."** It is the standard way to train autoregressive language models like this one, and it is not cheating because at test time the answers are not available; what the model *is* graded on in generation is its own pick. Fix: the driving-lesson analogy in the Concept, and then block 5's loop against block 3's forward.
3. **"Padding is harmless because it's just blanks."** It is 24% of the positions, and the model gets credit for every one it predicts easily. Fix: block 2's `0.5857` against `1.1513`, done by hand.

### 9. How deep to go, and where to stop

Stop at: *"training hands the model the true previous letter, so all inputs are known and nothing is sampled inside the loop; generating hands it its own pick, so each letter waits for the one before; the padding is skipped so it cannot flatter the loss; train loss and validation loss are two numbers and the second is the honest one; and the count of names already in the list shows how much of 'inventing' is remembering."* Do **not** go into: scheduled sampling, beam search, perplexity, embeddings as meaning, why letter 12 is `n`, bidirectional models, or what the hidden state "stores". If the student asks *"so how do I make it invent more?"*: *"Two things change the answer: stop earlier, and choose the next letter differently. Next week is the second."*

### 10. 🧭 Where Week 12 sits

```text
   W5   overfitting: train loss keeps falling, validation turns round
   W8   an embedding and a recurrent cell read a sequence in order
   W10  the loop's slopes compound
   W11  an LSTM cell: a memory track updated by adding; the dial starts near 1/2
   W12  (today) the LSTM meets 231 names. TRAIN: true previous letter in,
        all inputs known, padding skipped. GENERATE: own pick in, one letter at
        a time. The count: 80% of what it "invents" was in its training list.
   W13  choosing the next letter: greedy, temperature, top-k, top-p; exposure bias
   W14  attention: skip the loop altogether
```

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Confirm the stack and the folder.** The lesson imports `l4lib.names`, so run everything from the folder that contains `l4lib/` (`36-week-course/`):

```bash
python3 -c "import torch; print(torch.__version__); from l4lib.names import NAMES; print(len(NAMES))"
```

You should see a version (the numbers in this guide came from torch `2.2.1`) and the count:

```text
2.2.1
231
```

`pip` returning 403 is expected and not an error; **nothing this week installs anything.**

- [ ] **Make a working folder and one file, `week12.py`.** Paste the seven blocks below into it **one under the other, with no gap**, running the file after each. Each block uses names defined by the ones above (`torch`, `F`, `math`, `np`, `inputs`, `targets`, `model`, `train`, `loss_of`, `make_name`). The output printed under each block is what **that block** prints (the whole file prints all seven in order). Total runtime: about 6 seconds.

**Block 1 — the names as numbers, and the shifted input** (`torch.full`, `torch.cat`)

```python
# names.py - Week 12 block 1: the names as numbers, and the shift-right input that teacher forcing needs.
import torch
from l4lib.names import NAMES, PAD, EOS, STOI, VOCAB_SIZE, MAXLEN, encode, decode
torch.set_num_threads(1)

print(len(NAMES), "names | vocabulary", VOCAB_SIZE, "| longest name + EOS", MAXLEN)
print("aarav ->", encode("aarav"))
print("anika ->", encode("anika"))

data = torch.tensor([encode(n) for n in NAMES])                 # (231, 8): letters, then EOS, then PAD
start = torch.full((len(NAMES), 1), PAD)                        # a column of 231 "start" tokens (the id of PAD)
inputs = torch.cat([start, data[:, :-1]], dim=1)                # shift right: START, then every true letter but the last
targets = data
print("data", tuple(data.shape), "| start", tuple(start.shape), "| inputs", tuple(inputs.shape), "| targets", tuple(targets.shape))

print("step  input  target      (the name anika)")
row = NAMES.index("anika")
for t in range(MAXLEN):
    print(f"  {t}    {int(inputs[row, t]):2d}     {int(targets[row, t]):2d}")
print("decode(targets[row]) =", decode(targets[row]))
```

```text
231 names | vocabulary 28 | longest name + EOS 8
aarav -> [2, 2, 19, 2, 23, 1, 0, 0]
anika -> [2, 15, 10, 12, 2, 1, 0, 0]
data (231, 8) | start (231, 1) | inputs (231, 8) | targets (231, 8)
step  input  target      (the name anika)
  0     0      2
  1     2     15
  2    15     10
  3    10     12
  4    12      2
  5     2      1
  6     1      0
  7     0      0
decode(targets[row]) = anika
```

`0` is PAD, `1` is EOS, `2` is `a`. The two tables to read aloud: **targets** `2, 15, 10, 12, 2, 1, 0, 0` (a-n-i-k-a, end, blank, blank) and **inputs** `0, 2, 15, 10, 12, 2, 1, 0`. Row by row the input is the previous row's target: that is the whole idea of shifting. The last column of `data` is never an input (nothing follows a padding), which is why it is removed before the glue. Step 6: the target is `0` (padding) and the input is `1` (EOS): the model will be shown "the name has ended" and asked for "nothing", and we will ask the loss not to care.

**Block 2 — the padding, by hand and with `F.cross_entropy`** (`F.cross_entropy(..., ignore_index=)`)

```python
# pad.py - Week 12 block 2: what the loss does with padding, by hand and then with F.cross_entropy.
import math
import torch.nn.functional as F

# One name "uma" -> 3 letters + EOS = 4 real targets, then 4 PAD targets (MAXLEN is 8).
# Pretend the model gave these probabilities to the TRUE next letter at each real step (invented, to do by hand):
p_true = [0.5, 0.25, 0.8, 0.1]
surprise = [-math.log(p) for p in p_true]
print("surprise per real step :", [round(s, 4) for s in surprise])
print("average over 4 real    :", round(sum(surprise) / 4, 4))

# Now let F.cross_entropy do the same job. A toy world of 3 ids: 0 and 1 are letters, 2 is PAD.
# Scores that make softmax equal our probabilities: scores = ln(p). The two wrong ids share what is left.
true_ids = [0, 1, 0, 1]                                  # which id was the true next letter at each real step
rows, labels = [], []
for p, true_id in zip(p_true, true_ids):
    row = [math.log((1 - p) / 2)] * 3
    row[true_id] = math.log(p)
    rows.append(row)
    labels.append(true_id)
for _ in range(4):                                       # four padding steps: the model is "sure" of PAD
    rows.append([math.log(0.01), math.log(0.01), math.log(0.98)])
    labels.append(2)
scores = torch.tensor(rows)
labels = torch.tensor(labels)
print("scores", tuple(scores.shape), "labels", labels.tolist())
print("padding counted    :", round(F.cross_entropy(scores, labels).item(), 4))
print("padding ignored    :", round(F.cross_entropy(scores, labels, ignore_index=2).item(), 4))
```

```text
surprise per real step : [0.6931, 1.3863, 0.2231, 2.3026]
average over 4 real    : 1.1513
scores (8, 3) labels [0, 1, 0, 1, 2, 2, 2, 2]
padding counted    : 0.5857
padding ignored    : 1.1513
```

The by-hand average equals `padding ignored` to four places: that is the check. `padding counted` is `0.5857`: four steps that the toy model finds easy (`-ln 0.98` each) have been averaged in. `ignore_index=2` means "rows whose label is 2 are dropped from the top and the bottom". (Three ids in the toy, with 2 as the padding id, so that the real labels `0` and `1` are not touched.)

**Block 3 — the model, untrained**

```python
# model.py - Week 12 block 3: the model. An embedding, an LSTM cell, a dropout, a linear layer to 28 scores.
import torch.nn as nn

class NameLSTM(nn.Module):
    def __init__(self, vocab=VOCAB_SIZE, emb=24, hidden=64, p_drop=0.3):
        super().__init__()
        self.hidden = hidden
        self.emb = nn.Embedding(vocab, emb)          # letter id -> 24 numbers (Week 8)
        self.cell = nn.LSTMCell(emb, hidden)         # one LSTM step (Week 11)
        self.drop = nn.Dropout(p_drop)               # off in eval mode (Week 5)
        self.out = nn.Linear(hidden, vocab)          # 64 numbers -> one score per id

    def init_state(self, B):
        return torch.zeros(B, self.hidden), torch.zeros(B, self.hidden)      # the PAIR (h, c)

    def step(self, tok, state):
        """ONE step: a batch of letter ids in, scores for the next letter out, and the new (h, c)."""
        state = self.cell(self.emb(tok), state)
        return self.out(self.drop(state[0])), state

    def forward(self, x):
        """A whole batch of names at once. Every input letter is already known: x is the shift-right tensor."""
        state, rows = self.init_state(x.shape[0]), []
        for t in range(x.shape[1]):
            scores, state = self.step(x[:, t], state)
            rows.append(scores)
        return torch.stack(rows, 1)                  # (names, steps, 28)

torch.manual_seed(0)
model = NameLSTM()
print("numbers in the model:", sum(p.numel() for p in model.parameters()))
scores = model(inputs)
print("scores", tuple(scores.shape), "(231 names, 8 steps, 28 scores each)")

flat_scores = scores.reshape(-1, VOCAB_SIZE)        # (1848, 28): one row per (name, step)
flat_targets = targets.reshape(-1)                  # (1848,)
real = int((flat_targets != PAD).sum())
print("positions:", flat_targets.numel(), "| real:", real, "| padding:", flat_targets.numel() - real)
print("loss, padding counted :", round(F.cross_entropy(flat_scores, flat_targets).item(), 4))
print("loss, padding ignored :", round(F.cross_entropy(flat_scores, flat_targets, ignore_index=PAD).item(), 4))
print("a model that knows nothing scores ln(28) =", round(math.log(VOCAB_SIZE), 4))
```

```text
numbers in the model: 25532
scores (231, 8, 28) (231 names, 8 steps, 28 scores each)
positions: 1848 | real: 1404 | padding: 444
loss, padding counted : 3.3629
loss, padding ignored : 3.3455
a model that knows nothing scores ln(28) = 3.3322
```

Read: **25,532** numbers (the embedding `28 x 24 = 672`, the LSTM cell `4 x 64 x (24 + 64 + 2) = 23,040` and the output layer `64 x 28 + 28 = 1,820`); `1,404` of the `1,848` positions are real, `444` padding (24.0%). An untrained model gives the right id about one time in 28, so its loss is about `ln 28 = 3.3322`; counting padding moves the number from `3.3455` to `3.3629`. **The model's `forward` is a loop of 8 steps over a batch of 231**, every input taken from the tensor `x` that already exists. That line (`self.step(x[:, t], state)`) is what "teacher forcing" means in code; block 5's loop takes its input from the previous answer.

**Block 4 — hold out 31 names, train, print train against validation** (about 2.5 seconds)

```python
# train.py - Week 12 block 4: hold some names back, train on the rest, report train loss and validation loss.
g = torch.Generator().manual_seed(0)
order = torch.randperm(len(NAMES), generator=g)             # a seeded shuffle of 0..230 (Week 5)
train_rows, val_rows = order[:200], order[200:]
train_names = [NAMES[i] for i in train_rows.tolist()]
val_names = [NAMES[i] for i in val_rows.tolist()]
print("train", len(train_names), "| validation", len(val_names), "| first three held back:", val_names[:3])

def loss_of(model, rows):
    """Average loss per real letter on the chosen rows, with dropout OFF and no learning."""
    model.eval()
    with torch.no_grad():
        scores = model(inputs[rows])
        return F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets[rows].reshape(-1), ignore_index=PAD).item()

def train(rows, steps=800, seed=0, report=()):
    torch.manual_seed(seed)
    model = NameLSTM()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.1)
    for step in range(steps + 1):
        if step in report:
            print(f"  step {step:4d}  train {loss_of(model, train_rows):.3f}  validation {loss_of(model, val_rows):.3f}")
        if step == steps:
            break
        model.train()                                       # dropout ON while learning
        scores = model(inputs[rows])                        # the whole batch of names at once
        loss = F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets[rows].reshape(-1), ignore_index=PAD)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    model.eval()
    return model, loss.item()                                # the model, and the last training-step loss (dropout on)

print("training on 200 names, 800 full-batch steps:")
model, last = train(train_rows, report=(0, 100, 200, 300, 400, 600, 800))
print("final   train", round(loss_of(model, train_rows), 3), "| validation", round(loss_of(model, val_rows), 3), "| last training step (dropout on)", round(last, 3))
```

```text
train 200 | validation 31 | first three held back: ['amara', 'rhea', 'rafael']
training on 200 names, 800 full-batch steps:
  step    0  train 3.346  validation 3.349
  step  100  train 1.960  validation 2.308
  step  200  train 1.431  validation 2.544
  step  300  train 1.103  validation 2.880
  step  400  train 0.984  validation 3.077
  step  600  train 0.921  validation 3.314
  step  800  train 0.906  validation 3.417
final   train 0.906 | validation 3.417 | last training step (dropout on) 1.001
```

The shuffle is seeded (`Generator().manual_seed(0)`): the same 31 names every run. The function `loss_of` turns dropout off and does not learn; `train` turns it on while learning (**two** modes, Week 5). The last column is new in its position: `1.001` is the last *training* step with dropout on, `0.906` is the same model measured with dropout off. The two curves are the whole lesson of the week: **train keeps falling; validation turns round after step 100 and ends at `3.417`, above the `3.332` of knowing nothing.**

**Block 5 — generate: the model's own pick is fed back in** (`draw` is received, not typed)

```python
# generate.py - Week 12 block 5: generating. The model's OWN pick is fed back in, one letter at a time.
import numpy as np

def draw(scores, rng):
    """RECEIVED, not typed (Week 13 opens this box): pick one id at random, in proportion to the model's probabilities."""
    probs = torch.softmax(scores, dim=0).tolist()           # 28 numbers that add to 1
    r, running = rng.random(), 0.0                          # r: a seeded float in [0, 1)
    for i, p in enumerate(probs):
        running += p
        if r < running:
            return i
    return len(probs) - 1

def make_name(model, rng):
    model.eval()                                            # dropout OFF
    state, tok, ids = model.init_state(1), torch.full((1,), PAD), []   # START token, empty memory
    with torch.no_grad():
        for _ in range(MAXLEN):
            scores, state = model.step(tok, state)          # ONE letter at a time
            scores = scores[0]                              # (1, 28) -> (28,)
            scores[PAD] = -1e9                              # padding is never an answer
            i = draw(scores, rng)
            if i == EOS:
                break
            ids.append(i)
            tok = torch.tensor([i])                         # the model's OWN pick is the next input
    return decode(ids)

rng = np.random.default_rng(0)
twenty = [make_name(model, rng) for _ in range(20)]
print(twenty)
```

```text
['olen', 'vito', 'tatiana', 'felix', 'naya', 'oona', 'leena', 'maren', 'deepak', 'alina', 'alina', 'pavel', 'willem', 'yash', 'serge', 'rusha', 'yash', 'katya', 'juno', 'argek']
```

Read `make_name` against `forward` from block 3: there, step `t`'s input is `x[:, t]`, a column that already exists; here it is `tok`, which is set from `i`, the last answer. **That is the difference the whole week is about.** Twenty draws with seed 0: 17 are names from the training list (`alina` and `yash` twice each). `scores[PAD] = -1e9` is a score so low that its probability is zero; it is insurance (Clinic 8: this trained model never asks for padding), and it is what Week 13's `next_scores` does too.

**Block 6 — the audit: how many generated names are in the training list?** (two generations of 200, one short training)

```python
# novelty.py - Week 12 block 6: count how many generated names already exist in the training list.
def count_new(generated, train_list, val_list):
    in_train = sum(n in train_list for n in generated)
    in_val = sum(n in val_list for n in generated)
    neither = len(generated) - in_train - in_val
    return in_train, in_val, neither

rng = np.random.default_rng(1)
generated = [make_name(model, rng) for _ in range(200)]
in_train, in_val, neither = count_new(generated, set(train_names), set(val_names))
print(f"200 names | already in the TRAINING list: {in_train} ({in_train / 200:.1%}) | in the held-back list: {in_val} | in neither: {neither}")
print("distinct among the 200:", len(set(generated)))
print("a few that are in neither list:", [n for n in generated if n not in set(train_names) and n not in set(val_names)][:8])

early, _ = train(train_rows, steps=100)                        # the same recipe, stopped at step 100
rng = np.random.default_rng(1)
generated_early = [make_name(early, rng) for _ in range(200)]
in_train, in_val, neither = count_new(generated_early, set(train_names), set(val_names))
print(f"stopped at step 100: train {loss_of(early, train_rows):.3f}, validation {loss_of(early, val_rows):.3f}")
print(f"200 names | in the TRAINING list: {in_train} ({in_train / 200:.1%}) | in the held-back list: {in_val} | in neither: {neither}")
print("distinct among the 200:", len(set(generated_early)))
print("a few that are in neither list:", [n for n in generated_early if n not in set(train_names) and n not in set(val_names)][:8])
```

```text
200 names | already in the TRAINING list: 159 (79.5%) | in the held-back list: 0 | in neither: 41
distinct among the 200: 147
a few that are in neither list: ['gmeo', 'koori', 'nunia', 'jekori', 'gemra', 'ferix', 'domitana', 'sagna']
stopped at step 100: train 1.960, validation 2.308
200 names | in the TRAINING list: 1 (0.5%) | in the held-back list: 0 | in neither: 199
distinct among the 200: 199
a few that are in neither list: ['luesa', 'taran', 'gmana', 'dareltl', 'lagun', 'nios', 'leanpa', 'teno']
```

159 of 200 at step 800 (`79.5%`), only 147 different strings among the 200 (names drawn more than once), and `gmeo`, `koori`, `nunia`, `jekori`, `gemra`, `ferix` as examples of the rest; at step 100 only **1** of 200 is in the list, but `luesa`, `taran`, `gmana`, `dareltl`, `nios` are mostly not names. **Have the student read the 8 printed strings in each group and say which could be names, before you say anything.** Zero are in the held-back list in both cases: see section 7, item 7.

**Block 7 — the keeper: train on all 231 names, for Week 13** (about 2.5 seconds)

```python
# keeper.py - Week 12 block 7: the model for next week. Train on ALL 231 names, same recipe, and count again.
all_rows = list(range(len(NAMES)))
keeper, last = train(all_rows)
print("keeper: loss on all 231 names =", round(loss_of(keeper, all_rows), 3), "| last training step (dropout on) =", round(last, 3))

rng = np.random.default_rng(2)
generated_all = [make_name(keeper, rng) for _ in range(200)]
known = sum(n in set(NAMES) for n in generated_all)
print(f"200 names | already in the 231-name list: {known} ({known / 200:.1%}) | new: {200 - known} | distinct: {len(set(generated_all))}")
print("the new ones:", sorted(set(n for n in generated_all if n not in set(NAMES)))[:12])
```

```text
keeper: loss on all 231 names = 0.934 | last training step (dropout on) = 1.026
200 names | already in the 231-name list: 167 (83.5%) | new: 33 | distinct: 156
the new ones: ['amira', 'andira', 'andriia', 'arnata', 'arnay', 'asme', 'belia', 'camendid', 'clala', 'elma', 'erich', 'fakori']
```

`0.934` is the honest loss (dropout off); `1.026` is the training step's own number (dropout on), and **is the check Week 13's `namelm.py` prints**: if yours prints `1.026`, the recipe is the course's. `amira` and `erich` are names in the world and not in the list; `andriia`, `camendid` and `fakori` are not names. 33 of 200 (16.5%) are new strings; 156 distinct.

**Teacher-only block T1 — the baseline and the validation curve, step by step** (about 3 seconds; uses `torch.bincount`, `min(..., key=lambda ...)`; the student never sees it)

```python
# TEACHER-ONLY T1: (a) the know-nothing-about-context baseline (letter frequencies only), and (b) the validation curve step by step.
# (Uses torch.bincount, a boolean mask and a list of steps; the student never sees this block. A measurement, not a model.)
def unigram_loss(train_rows, eval_rows):
    counts = torch.bincount(targets[train_rows][targets[train_rows] != PAD], minlength=VOCAB_SIZE).float()
    probs = (counts + 1) / (counts + 1).sum()                      # add one so no id has probability 0
    t = targets[eval_rows]
    t = t[t != PAD]
    return -torch.log(probs[t]).mean().item()

print("letter-frequency baseline: train", round(unigram_loss(train_rows, train_rows), 3), "| validation", round(unigram_loss(train_rows, val_rows), 3))

curve = {}
steps_to_show = list(range(0, 301, 20))
_m = None
torch.manual_seed(0)
_m = NameLSTM()
_opt = torch.optim.AdamW(_m.parameters(), lr=3e-3, weight_decay=0.1)
for step in range(301):
    if step in steps_to_show:
        curve[step] = (loss_of(_m, train_rows), loss_of(_m, val_rows))
    _m.train()
    _s = _m(inputs[train_rows])
    _l = F.cross_entropy(_s.reshape(-1, VOCAB_SIZE), targets[train_rows].reshape(-1), ignore_index=PAD)
    _opt.zero_grad(set_to_none=True)
    _l.backward()
    torch.nn.utils.clip_grad_norm_(_m.parameters(), 1.0)
    _opt.step()
best = min(curve, key=lambda s: curve[s][1])
print("step  train  validation")
for s in steps_to_show:
    print(f"{s:4d}  {curve[s][0]:.3f}  {curve[s][1]:.3f}" + ("   <- lowest validation" if s == best else ""))
```

```text
letter-frequency baseline: train 2.789 | validation 2.735
step  train  validation
   0  3.346  3.349
  20  2.613  2.607
  40  2.336  2.388
  60  2.178  2.313
  80  2.065  2.301   <- lowest validation
 100  1.960  2.308
 120  1.853  2.340
 140  1.745  2.369
 160  1.636  2.424
 180  1.530  2.483
 200  1.431  2.544
 220  1.343  2.596
 240  1.267  2.675
 260  1.201  2.739
 280  1.146  2.809
 300  1.103  2.880
```

Read this before class, because it changes what "the validation loss" means. **The letter-frequency baseline is `2.735`**: a model that looks at no context at all, only how often each letter occurs. The real model beats it only in the window of steps 20 to about 250 (it is already below `2.735` at step 20, `2.607`, and back above it by step 260, `2.739`) and never by much (best `2.301` at step 80). Everything after that is worse than counting letters. The recipe's `800` is the number from the reference module, not a tuned stopping point.

**Teacher-only block T2 — three training seeds, two stopping points** (about 6 seconds)

```python
# TEACHER-ONLY T2: three training seeds on the SAME split: train, validation and the share of 200 generated names already in the training list.
print("seed  steps  train  validation  in-train/200  distinct")
for seed in [0, 1, 2]:
    for steps in [100, 800]:
        m, _ = train(train_rows, steps=steps, seed=seed)
        r = np.random.default_rng(10 + seed)
        gen = [make_name(m, r) for _ in range(200)]
        hit = sum(n in set(train_names) for n in gen)
        print(f"  {seed}   {steps:4d}  {loss_of(m, train_rows):.3f}   {loss_of(m, val_rows):.3f}      {hit:3d} ({hit / 200:5.1%})   {len(set(gen))}")
```

```text
seed  steps  train  validation  in-train/200  distinct
  0    100  1.960   2.308        1 ( 0.5%)   197
  0    800  0.906   3.417      161 (80.5%)   146
  1    100  1.919   2.331        4 ( 2.0%)   200
  1    800  0.906   3.668      172 (86.0%)   148
  2    100  1.942   2.269        3 ( 1.5%)   200
  2    800  0.907   3.490      173 (86.5%)   142
```

Spread across seeds: the train loss agrees to the third digit (`0.906, 0.906, 0.907`), the validation loss moves by about 0.25 (`3.417, 3.668, 3.490`), and the share of the 200 names that are in the training list is `80.5%` to `86.5%` at 800 steps and `0.5%` to `2.0%` at 100. **The difference between the two stopping points is far bigger than the spread between seeds.** Do not quote the validation figure beyond one decimal.

**Teacher-only block T3 — whole batch against one step at a time, and the clock** (under 1 second)

```python
# TEACHER-ONLY T3: (a) teacher forcing gives the SAME scores whether you run the whole batch at once or feed the true letters one step at a time,
# (b) the clock: scoring 200 known names against generating 200 new ones. (Timing varies run to run; the ratio does not change sign.)
import time
model.eval()
with torch.no_grad():
    whole = model(inputs[train_rows])
    state = model.init_state(len(train_rows))
    stepwise = []
    for t in range(MAXLEN):
        s, state = model.step(inputs[train_rows][:, t], state)
        stepwise.append(s)
    stepwise = torch.stack(stepwise, 1)
print("whole batch vs step by step, biggest gap:", f"{(whole - stepwise).abs().max().item():.1e}")

t0 = time.perf_counter()
with torch.no_grad():
    for _ in range(20):
        model(inputs[train_rows])
t_tf = (time.perf_counter() - t0) / 20
rng = np.random.default_rng(3)
t0 = time.perf_counter()
_ = [make_name(model, rng) for _ in range(200)]
t_gen = time.perf_counter() - t0
print(f"teacher-forced pass over 200 names: {t_tf * 1000:.1f} ms | generating 200 names, one letter at a time: {t_gen * 1000:.1f} ms | ratio {t_gen / t_tf:.0f}x")
```

```text
whole batch vs step by step, biggest gap: 0.0e+00
teacher-forced pass over 200 names: 1.3 ms | generating 200 names, one letter at a time: 28.9 ms | ratio 21x
```

The gap `0.0e+00` says: feeding the true letters one step at a time gives **exactly** the scores the whole-batch pass gives, so teacher forcing is a scheduling fact (all the inputs exist) and not a different computation. The 20x ratio below is therefore mostly batch size 1 against batch 200, not forcing against no forcing; The two timings vary from run to run and machine to machine; the ratio was `18x` to `21x` in our three runs on this machine. the 200 generated names cost many more cell calls than one batch of 200 (one call per name per letter, with a batch of 1).

**Teacher-only block K1 — `key.py`: every hand answer in the workbook, computed** (under 1 second)

```python
# TEACHER-ONLY key.py - Week 12: every hand-arithmetic answer in the workbook, computed.
# 12.1 encode and shift by hand: three names.
for name in ["uma", "bex", "kaia"]:
    ids = encode(name)
    shifted = [PAD] + ids[:-1]
    print(f"{name:5s} targets {ids}  inputs {shifted}")

# 12.2 how much of a batch is padding: four names, then all 231.
four = ["uma", "bex", "wren", "kajsa"]
real4 = sum(len(n) + 1 for n in four)
print("four names: real", real4, "| total", 4 * MAXLEN, "| padding", 4 * MAXLEN - real4, f"| share {(4 * MAXLEN - real4) / (4 * MAXLEN):.1%}")
print("all names : real", real, "| total", len(NAMES) * MAXLEN, "| padding", len(NAMES) * MAXLEN - real, f"| share {(len(NAMES) * MAXLEN - real) / (len(NAMES) * MAXLEN):.1%}", "| mean letters per name", round(sum(len(n) for n in NAMES) / len(NAMES), 2))

# 12.3 loss of one name by hand: the four real steps got these probabilities on the true letter.
p4 = [0.4, 0.5, 0.25, 0.9]
each = [-math.log(p) for p in p4]
print("12.3 surprise per step:", [round(s, 4) for s in each], "| average:", round(sum(each) / 4, 4))
print("12.3 the same four steps plus four padding steps the model is 99% sure of:",
      round((sum(each) + 4 * -math.log(0.99)) / 8, 4), "<- padding counted, the number looks better")

# 12.4 reading a loss as 'how many equally likely letters': e ** loss.
for label, value in [("know nothing", math.log(VOCAB_SIZE)), ("letter frequencies, validation", unigram_loss(train_rows, val_rows)), ("step 100 validation", loss_of(early, val_rows)), ("step 800 train", loss_of(model, train_rows)), ("step 800 validation", loss_of(model, val_rows))]:
    print(f"{label:32s} loss {value:.3f}  ->  e ** loss = {math.exp(value):5.1f}")
```

```text
uma   targets [22, 14, 2, 1, 0, 0, 0, 0]  inputs [0, 22, 14, 2, 1, 0, 0, 0]
bex   targets [3, 6, 25, 1, 0, 0, 0, 0]  inputs [0, 3, 6, 25, 1, 0, 0, 0]
kaia  targets [12, 2, 10, 2, 1, 0, 0, 0]  inputs [0, 12, 2, 10, 2, 1, 0, 0]
four names: real 19 | total 32 | padding 13 | share 40.6%
all names : real 1404 | total 1848 | padding 444 | share 24.0% | mean letters per name 5.08
12.3 surprise per step: [0.9163, 0.6931, 1.3863, 0.1054] | average: 0.7753
12.3 the same four steps plus four padding steps the model is 99% sure of: 0.3927 <- padding counted, the number looks better
know nothing                     loss 3.332  ->  e ** loss =  28.0
letter frequencies, validation   loss 2.735  ->  e ** loss =  15.4
step 100 validation              loss 2.308  ->  e ** loss =  10.1
step 800 train                   loss 0.906  ->  e ** loss =   2.5
step 800 validation              loss 3.417  ->  e ** loss =  30.5
```

Use this to mark pages 12.1-12.3. Do **not** hand it over or paste it into the student's folder.

- [ ] **Print the name quiz** (Hook): twelve names in a shuffled order on a card, six from the training list and six from block 7's "new ones" (list below). Keep the answer line for yourself.
- [ ] **Print the workbook pages** 12.1-12.6 and read the Answer Key below.
- [ ] **Read the Debugging Clinic** and copy the eight snippets to a scratch file so they are ready to plant; each starts with a `# DELIBERATE MISTAKE n` comment.

### 3 minutes on the day

- [ ] Open `week12.py` as an **empty file** for typing. Check `l4lib/` is in the same folder.
- [ ] Calculator, timer, name quiz and workbook pages on the desk; a pen in two colours.

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Blocks 1 and 2 are still worth reading from the guide; pages 12.1-12.3 need only paper and the calculator. Run the rest from the printed outputs and say so. |
| `ModuleNotFoundError: No module named 'l4lib'` | You are in the wrong folder. Run `python3 week12.py` from the folder that contains `l4lib/`. |
| `NameError: name 'F' is not defined` (or `model`, `train`, `loss_of`, `make_name`, `np`, `math`) | The earlier block was not pasted above. The seven blocks are one file; `F` and `math` come from block 2, `np` from block 5. |
| `TypeError: full(): argument 'size' (position 1) must be tuple of ints, not int` | Clinic 1: the shape is a tuple. `(231, 1)`. |
| `ValueError: Expected input batch_size (2079) to match target batch_size (1848).` | Clinic 2: the shifted input kept all 8 columns of `data`; use `data[:, :-1]`. |
| `RuntimeError: Expected target size [231, 28], got [231, 8]` | Clinic 3: flatten the scores and the targets. |
| A table differs in the second or third digit | Different PyTorch build or CPU. Compare the shape: train falls to about `0.9`, validation falls then climbs above `3`, the in-list share is 70-90% at step 800 and under 5% at step 100. Use the numbers on your screen. |
| Train loss at step 800 is not `0.906` | `torch.set_num_threads(1)` is at the top of block 1; check it ran. Check `ignore_index=PAD` is in both the training line and `loss_of`. |
| Block 4 takes more than 20 seconds | Not normal (2.5 s here). Missing `torch.set_num_threads(1)` is the usual cause on a laptop with many cores. |
| Student's generated names are all the same | Clinic 7: the generator is being re-created inside the loop. |
| No laptop at all | Do the Hook, the Concept, and pages 12.1-12.3 with pencil and calculator. Read the tables in section 6 as "data from my laptop at home". Say so out loud. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 8 | The name quiz: 12 names on a card, which are real? Then the count that says what "real" meant |
| 🧠 Concept | 14 | A name as numbers; the shifted input; training with the answers in sight, generating on your own words; padding and the loss |
| 💻 Live-code | 20 | Blocks 1-3 (names as numbers and the shift, the padding by hand, the model) |
| 🎲 Their turn | 23 | Predict, then block 4 (train against validation); block 5 (generate); block 6 (the audit, twice) |
| 🔑 Wrap & assign | 5 | What was shown, what was not; the homework |

### 🪝 Hook — Real or Invented? (8 minutes)

**(3 min) The card.** Hand over the printed **name quiz**: twelve names in a fixed shuffled order. Say: *"Six of these are from a list of 231 names somebody typed. Six were written by a computer program that has read that list. Mark the ones you think the program wrote. Do not look at the computer."* Write their guesses on a card before you say anything. The twelve, with the key for you:

| On the card | Who wrote it |
|---|---|
| `tamara` · `dmitri` · `sigrid` · `kavya` · `heidi` · `noor` | from the typed list (`NAMES`) |
| `amira` · `arnata` · `clala` · `camendid` · `fakori` · `andriia` | **written by the model trained on all 231 names** (from block 7's generator; none of the six is in the list) |

Shuffle them on the card (for example: `fakori, tamara, amira, dmitri, camendid, noor, clala, sigrid, andriia, kavya, arnata, heidi`). Expect disagreement, and expect `amira` to be marked "real" (it is a name in the world: *it is not in our list, but it is in the world*) while `camendid` or `fakori` are marked "computer". **That is the point of the quiz:** "invented" and "not in the list" are two different questions. Do not tell them yet how many of the program's names are *in* the list.

**(3 min) What the program does.** Say: *"Here is how the program is built. Training: I show it one name at a time, one letter at a time, and after each letter I ask 'what comes next?'. It guesses. I tell it the real answer. It adjusts. Then I move to the next letter, and I give it the real letter, not its guess. After thousands of rounds, it is good at the game 'what comes next after `an`?'."* Write on the board: **TRAIN: the true previous letter goes in.** Then: *"Now the program has to write a name. There is no real previous letter. What does it have?"* (Its own last pick.) Write: **GENERATE: its own last pick goes in.** *"Which of these two is easier to get wrong?"* (Generate.) Leave it there.

**(2 min) A number to guess.** Say: *"Suppose a program reads 200 of these names and then writes 200 names of its own. How many of its 200 do you think are names it was *given*?"* Write their guess on the card (a number from 0 to 200). *"The real number is one run of code away. We will get it before the hour is up."*

**Bridge:** *"To find out, we have to get names into the program as numbers, give it the right thing to look at, and give it a score that is fair."*

### 🧠 Concept — The Answers in Sight, and Then on Your Own (14 minutes)

**(3 min) A name is a list of numbers.** On the board: `a=2, b=3, ...`, `EOS = 1` (the name has ended), `PAD = 0` (nothing; filler to make every name the same length). Write `anika -> [2, 15, 10, 12, 2, 1, 0, 0]`. Say: *"Every name is padded to the same length so the computer can hold 231 of them in one grid. The 0s are not part of the name."* Ask: *"what is the longest name in the list?"* (Seven letters, plus EOS, so eight columns.)

**(4 min) The shift.** Draw the two rows from block 1:

```text
input :  START  a   n   i   k   a   EOS  PAD
target:    a    n   i   k   a  EOS  PAD  PAD
```

Say: *"At every step the program sees the column above and must say the column below. The input row is the target row moved one place to the right, with a START in front."* Point at the arrow: *"Every input is a letter I already have."* Ask: *"could I work out the input for step 5 before the program has done step 2?"* (Yes.) *"Then I can put the whole grid of names through together."* That is **teacher forcing**. The analogy, if the student likes one: the driving lesson from the reference module, where the instructor has a second steering wheel and corrects every drift before the next decision. *"You learn a lot and fast. But the test has no second wheel."*

**(4 min) Padding and the fair score.** On the board, the four steps of `uma` and four blanks. Say: *"The score for one step is how surprised the program was by the right letter: `-ln p`. The score for the name is the average. `uma`: four real steps and four blanks. The program will very quickly learn that after END comes a blank. How surprised is it by a blank it is 98% sure of?"* (`-ln 0.98 = 0.02`.) *"If I average the four real steps with the four blanks, what happens to my score?"* They should compute it in a minute: `(4.6051 + 4 x 0.0202) / 8 = 0.5857`, which is block 2's number. *"Did the program get better at names?"* (No.) **`ignore_index` says: do not average the blanks.**

**(3 min) Two numbers for one model.** Say: *"We will hold back 31 names. The program never trains on them. After each stretch of training we ask it for its score on the names it trained on, and on the 31."* Ask them to predict the shape (Week 5): *"the first keeps falling; the second..."* (Falls, then turns round. If they do not remember, say "Week 5's second curve".) *"If the second gets bad, what has the program done to the first 200?"* (Memorised them. Say the word.) Write **train loss / validation loss** on the board.

> **Check for understanding (do not skip).** *"What goes in at each step during training? During writing? Which one has all its inputs known up front? Why is the blank left out of the score?"* (The true previous letter; its own pick; training, because every input is known up front; so blanks cannot flatter it.) If they say "writing is slower because it's harder", go back: it is slower because the next input *does not exist* until the last answer does.

### 💻 Live-Code Together — blocks 1-3 (20 minutes)

The student types; you narrate **after** they have predicted. Keep `week12.py` open and add each block under the last.

1. **Block 1 (8 min)**: introduce **`torch.full`** (section 4b) and **`torch.cat`** (4c). Make them say the shape of `start` before they run (`(231, 1)`), of `data[:, :-1]` (`(231, 7)`), and of the glued result (`(231, 8)`). Run. Read the `anika` table: the input at each step is the previous step's target. Ask: *"what is the input at step 6 and why?"* (`1`, EOS: the last thing said.) Keep Clinic 1 and 2 in your pocket: this is where they happen.
2. **Block 2 (6 min)**: introduce **`F.cross_entropy(..., ignore_index=)`** (section 4a). They do the four surprises on a calculator **first** (`0.6931, 1.3863, 0.2231, 2.3026`) and the average (`1.1513`). Run. Point at the two lines: *"the function and the hand agree only when we tell it to skip the blanks"*. Say what `0.5857` is.
3. **Block 3 (6 min)**: read `NameLSTM` aloud as a sentence, part by part (an embedding: Week 8; an LSTM cell and a **pair** state: Week 11; dropout: Week 5; a linear layer to 28 scores). Point at `forward`: *"the input at step `t` is `x[:, t]`: a column that was there before we started."* Run. Compare the `3.3455` with `ln 28`. Ask *"what should an untrained program score?"* (About `ln 28`: one guess in 28.) Ask *"how much of the grid is blank?"* (`444` of `1,848`.)

### 🎲 Their Turn — The Name Audit (23 minutes)

**(3 min) Predict first.** Show workbook page 12.4 and 12.5 and ask for three written predictions, in pen, **before block 4**: (i) *"after 800 steps, is the validation loss going to be bigger or smaller than the train loss?"* (ii) *"at step 100, 200, 400, 800, does the validation loss go up, down, or down-then-up?"* (iii) the number out of 200 for the Hook. **Do not say if they are right.**

**(6 min) Block 4.** They type it and run it (2.5 seconds). They copy the seven rows into the table on 12.4 **with every digit**. Ask: *"when was the validation loss lowest, from this table?"* (Step 100 among the rows shown; `T1` finds it at 80, not in the student's table.) *"At step 800 the program scores `3.417` on the 31 names and `0.906` on the 200. What is `ln 28`?"* (`3.332`.) *"So on names it has not seen, it is doing worse than guessing one in 28."* Let that sit for ten seconds. *"What did it learn?"* (The 200 names.)

**(6 min) Block 5, the generator.** Introduce `draw` as a received helper in one sentence: *"the dice-roll; a number between 0 and 1 picks a letter in proportion to the program's probabilities"* (section 4d). Make them read `make_name` aloud against `forward`: *"where does the input come from, here? and there?"* Run. Twenty names appear. *"Mark the ones you think are from the list, before the computer says."* They mark; then they run `sum(n in train_names for n in twenty)` (one line; or you tell them: **17 of 20**).

**(6 min) Block 6, the audit.** They run it. First reaction: *"79.5%?"* Read line by line: 159 of 200 were in the training list; **0** of the held-back list; 41 in neither; only 147 distinct strings. Then the second half: stop at step 100: **1** of 200 in the list, 199 new, 199 distinct, and `luesa, taran, gmana, dareltl, lagun, nios, leanpa, teno`. Ask: *"which model is better at inventing names?"* (The question has no answer until you say what 'better' is: the 800-step one copies its list; the 100-step one makes new strings, most of which are not names. Both facts, in a sentence each.) Fill 12.5.

**(2 min) The Hook's number.** Return to the card: their guess for "how many of the 200 are names it was given?". Read the real one aloud and compare: **159**.

### 🔑 Wrap & Assign (5 minutes)

**(3 min) Three sentences.** The student says, from memory: *(1) what goes in at each step during training and during generation, (2) what `ignore_index` is for, (3) what the gap between `0.906` and `3.417` means and what the count `159 of 200` shows.* Write nothing for them. If they cannot do (3), go back to block 4's last line and block 6's first.

**(2 min) What we did not do, said out loud.** *"We looked at one recipe on one list. We did not test whether the names were good. We used the simplest dice-roll there is. Next week we open the dice: choosing the next letter in a different way changes how many names are new and how many are nonsense, and I will ask you to predict it first."* Hand out the homework.

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code, in a copy of the shared session as it stood after block 7. **Paths and the line numbers inside the snippet depend on how it was pasted** (here each snippet is its own file, with the `# DELIBERATE MISTAKE` comment on line 1). Each mistake is deliberate: you plant it, the student reads the traceback aloud (or, for the silent ones, the numbers), and you refuse to fix it until they have said what it means. Three are loud; **four are silent and one is a mistake that does not bite**, and the silent ones teach more.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (For the silent ones: *"Read me the number. Does it look right?"*)
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the shape of `torch.full` is not a tuple (loud)

```python
# DELIBERATE MISTAKE 1: torch.full wants a SHAPE (a tuple), and was given a bare number.
start = torch.full(len(NAMES), PAD)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad1.py", line 2, in <module>
    start = torch.full(len(NAMES), PAD)
TypeError: full(): argument 'size' (position 1) must be tuple of ints, not int
```

**Read it:** `torch.full` wants the *shape* as a tuple, `(231, 1)`; it was given the number 231. **Fix:** `torch.full((len(NAMES), 1), PAD)`. The hint in the message is `tuple of ints, not int`.

### Mistake 2 — the shift forgot to drop a column (loud)

```python
# DELIBERATE MISTAKE 2: the shift-right forgot to drop the last column, so inputs is one step too long.
bad_inputs = torch.cat([torch.full((len(NAMES), 1), PAD), data], dim=1)
print("inputs", tuple(bad_inputs.shape), "targets", tuple(targets.shape))
scores = model(bad_inputs)
loss = F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets.reshape(-1), ignore_index=PAD)
```

```text
inputs (231, 9) targets (231, 8)
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 5, in <module>
    loss = F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets.reshape(-1), ignore_index=PAD)
  ... frames inside torch (elided) ...
ValueError: Expected input batch_size (2079) to match target batch_size (1848).
```

**Read it:** the inputs are `(231, 9)`: a START column glued onto all 8 columns of `data`. The model happily returns 9 steps per name (`231 x 9 = 2,079` rows after flattening), and the loss finds 2,079 score-rows against 1,848 labels. **Fix:** `data[:, :-1]`. The numbers in the message (`2079`, `1848`) are the clue; the student should divide them by 231.

### Mistake 3 — the 3-D scores were not flattened (loud)

```python
# DELIBERATE MISTAKE 3: F.cross_entropy wants one ROW per (name, step); the 3-D scores were not flattened.
scores = model(inputs)
print("scores", tuple(scores.shape), "targets", tuple(targets.shape))
loss = F.cross_entropy(scores, targets, ignore_index=PAD)
```

```text
scores (231, 8, 28) targets (231, 8)
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 4, in <module>
    loss = F.cross_entropy(scores, targets, ignore_index=PAD)
  ... frames inside torch (elided) ...
RuntimeError: Expected target size [231, 28], got [231, 8]
```

**Read it:** for a 3-D input, `F.cross_entropy` reads the **middle** axis as the classes. Ours is `(231, 8, 28)`, so it saw 8 classes and asked for a target of shape `[231, 28]`. **Fix:** `scores.reshape(-1, VOCAB_SIZE)` and `targets.reshape(-1)`. The student should notice the target it wants, `[231, 28]`, and find the `28` in their own scores.

### Mistake 4 — padding counted in training (SILENT)

```python
# DELIBERATE MISTAKE 4 (SILENT): training with padding counted (no ignore_index). The reported number looks healthier.
torch.manual_seed(0)
bad = NameLSTM()
opt = torch.optim.AdamW(bad.parameters(), lr=3e-3, weight_decay=0.1)
for step in range(801):
    bad.train()
    scores = bad(inputs[train_rows])
    loss = F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets[train_rows].reshape(-1))     # <- no ignore_index
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(bad.parameters(), 1.0)
    opt.step()
    if step in (0, 100, 800):
        print(f"  step {step:3d}  loss as this loop reports it: {loss.item():.3f}")
print("the honest number for letters only (padding ignored):", round(loss_of(bad, train_rows), 3), "| validation:", round(loss_of(bad, val_rows), 3))
print("the correct recipe, same steps:                        ", round(loss_of(model, train_rows), 3), "| validation:", round(loss_of(model, val_rows), 3))
```

```text
  step   0  loss as this loop reports it: 3.364
  step 100  loss as this loop reports it: 1.615
  step 800  loss as this loop reports it: 0.772
the honest number for letters only (padding ignored): 0.913 | validation: 3.376
the correct recipe, same steps:                         0.906 | validation: 3.417
```

**Read it:** the loop reports `0.772` and the honest letters-only number is `0.913`: **the printed loss flatters the model by about 15%**, and nothing else is different. The model is as good as the correct recipe (`0.913` against `0.906` train; `3.376` against `3.417` validation, which is within a seed's noise, `T2`). Nothing crashes. **The harm is to the reader:** a number printed with padding counted cannot be compared with one printed without. The rule: *before you compare two losses, check they average the same positions.*

### Mistake 5 — no shift: the answer is the input (SILENT)

```python
# DELIBERATE MISTAKE 5 (SILENT): no shift. The input at each step is the answer for that step.
peek = targets                                   # should have been the shifted tensor
torch.manual_seed(0)
bad = NameLSTM()
opt = torch.optim.AdamW(bad.parameters(), lr=3e-3, weight_decay=0.1)
for step in range(801):
    bad.train()
    scores = bad(peek[train_rows])
    loss = F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets[train_rows].reshape(-1), ignore_index=PAD)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(bad.parameters(), 1.0)
    opt.step()
bad.eval()
with torch.no_grad():
    val_loss = F.cross_entropy(bad(peek[val_rows]).reshape(-1, VOCAB_SIZE), targets[val_rows].reshape(-1), ignore_index=PAD).item()
print("train loss", round(loss.item(), 4), "| validation loss", round(val_loss, 4), "   <- both near zero!")
rng = np.random.default_rng(0)
print("generated:", [make_name(bad, rng) for _ in range(8)])
```

```text
train loss 0.0027 | validation loss 0.001    <- both near zero!
generated: ['llllllll', 'iiiiiiii', 'tttttttt', 'llllllll', 'eeeeeeee', 'iiiiiiii', 'dddddddd', 'iiiiiiii']
```

**Read it:** train loss `0.0027` and validation loss `0.001`: both near zero, after the full 800 steps on a problem where the honest number is `3.4`. The model has learned to **copy its input**, which is the answer. Validation is also near zero because *validation peeks too*. Generation then reads the START token and its own letters, has never practised that, and writes `llllllll`. **The alarm is the number:** a validation loss of `0.001` on names is not a success, it is a leak. **Fix:** feed the shifted tensor (`inputs`), not `targets`. Ask: *"what should the validation loss be able to tell you that train cannot?"* (How the model does on data it was not shown; here it was shown the answers.)

### Mistake 6 — validation with dropout still on (SILENT)

```python
# DELIBERATE MISTAKE 6 (SILENT): validation loss measured with dropout still ON (model.train() was the last mode set).
for attempt in range(3):
    model.train()
    with torch.no_grad():
        s = model(inputs[val_rows]).reshape(-1, VOCAB_SIZE)
    print("dropout on :", round(F.cross_entropy(s, targets[val_rows].reshape(-1), ignore_index=PAD).item(), 3))
model.eval()
with torch.no_grad():
    s = model(inputs[val_rows]).reshape(-1, VOCAB_SIZE)
print("dropout off:", round(F.cross_entropy(s, targets[val_rows].reshape(-1), ignore_index=PAD).item(), 3))
```

```text
dropout on : 3.629
dropout on : 3.543
dropout on : 3.659
dropout off: 3.417
```

**Read it:** three calls, three different numbers (`3.629, 3.543, 3.659`), all above the honest `3.417`. Dropout zeroes a random share of the 64 numbers (`h`) going into the output layer on every call (not the memory `c`, and not the loop itself). **Two tells:** the number is different each time with nothing else changed, and all three are above the eval-mode number. **Fix:** `model.eval()` before measuring (`loss_of` does it; a hand-written measurement forgets it). This is Week 5's silent mistake on new ground.

### Mistake 7 — the generator is re-created inside the loop (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): the generator is re-seeded INSIDE the loop, so every name starts from the same random number.
names = []
for _ in range(200):
    rng = np.random.default_rng(0)
    names.append(make_name(model, rng))
print("200 names, distinct:", len(set(names)), "|", names[:4])
```

```text
200 names, distinct: 1 | ['olen', 'olen', 'olen', 'olen']
```

**Read it:** 200 names, **1** distinct: the same seed gives the same random numbers, so every name is `olen`. Nothing crashes; the *count of distinct names* is the alarm. **Fix:** make the generator **once**, outside the loop, and let it run on. The new-name rate of a run like this is a measurement of nothing. (This is Level 3 Week 1's seed rule, read in the other direction: a seed makes a run repeatable, so it must be set once per run and not once per draw.)

### Mistake 8 — the padding switch left out (a mistake that does not bite here)

```python
# DELIBERATE MISTAKE 8 (SILENT): the line scores[PAD] = -1e9 is left out of the generator. How often does the model ask for padding?
asked = 0
rng = np.random.default_rng(0)
with torch.no_grad():
    for _ in range(200):
        state, tok = model.init_state(1), torch.full((1,), PAD)
        for _ in range(MAXLEN):
            scores, state = model.step(tok, state)
            i = draw(scores[0], rng)
            if i == PAD:
                asked += 1
                break
            if i == EOS:
                break
            tok = torch.tensor([i])
print("names in which the model asked for padding before it said EOS:", asked, "of 200")
```

```text
names in which the model asked for padding before it said EOS: 0 of 200
```

**Read it:** zero of 200 names asked for padding. The model was trained with padding **ignored**, so the padding score is only ever pushed down (it is never the right answer in a row that counts); in this trained model the padding probability is small enough never to be drawn in 200 names. **Keep the line anyway:** it costs nothing, and a differently trained model (a different seed, a different size) could draw padding, which would end a name at once and feed the model a start token in the middle of a word. This mistake is in the Clinic to teach one sentence: *"it did not go wrong this time"* is not *"it is right"*. We did not test other seeds.

---

## 🎲 The Activity, In Full

### The Name Audit

**What it is:** a prediction, a measurement and a judgement, done in that order, on workbook pages 12.4 and 12.5. The judgement is the student reading twenty strings and marking which could be a name.

### Setup (2 minutes, during the live-code segment)

Page 12.4 has a blank table (steps 0, 100, 200, 400, 800; columns *train* and *validation*) and a second blank line for *predicted*. Page 12.5 has two columns: *the recipe stopped at step 800* and *stopped at step 100*, and three rows: *in the training list*, *in the held-back list*, *in neither*, with a fourth row *distinct of 200*. Two pens of different colours: predictions in one, measurements in the other.

### The rules, read out loud before the first cell

1. **Write your three predictions before you run block 4.** (Bigger or smaller validation loss at step 800; up, down or down-then-up; a number out of 200.)
2. **Copy each measured number in full, with every digit.** `0.906` is not `0.9`; `3.417` is not `3.4`.
3. **Read before you count.** Before block 6's numbers appear, mark twenty of the printed names *could be a name / could not*. Then count.
4. **Every number in your report must have been printed by your own run, with its seed, today.**

### The measured tables

The student's tables, so you can check them (blocks 4 and 6; seed 0 for the training, generator seed 1):

| step | train | validation |
|:--:|:--:|:--:|
| 0 | 3.346 | 3.349 |
| 100 | 1.960 | 2.308 |
| 200 | 1.431 | 2.544 |
| 400 | 0.984 | 3.077 |
| 800 | 0.906 | 3.417 |

| 200 generated names | stopped at 800 | stopped at 100 |
|---|:--:|:--:|
| in the training list | 159 (79.5%) | 1 (0.5%) |
| in the held-back list | 0 | 0 |
| in neither | 41 | 199 |
| distinct strings | 147 | 199 |

(Different training seeds and generator seeds give counts that differ by a few names: `T2` shows the 800-step in-list share at `80.5%`, `86.0%`, `86.5%` and the 100-step share at `0.5%` to `2.0%`. **The honest teaching line:** *"read the gap between the two columns, not the last digit."*)

### What "finished" looks like

Three predictions written; the loss table copied with every digit; twenty names marked by eye before the counts; the two-column table filled; and the student answers the question that makes the activity: *"the program wrote 200 names; how many were new?"* with *"for the 800-step model, about a fifth, and most of those are near-copies; for the 100-step model, nearly all, and most are not names"*.

### Variation — a shorter slot (55 minutes)

Skip the 100-step half of block 6 (keep the first, 159 of 200), and skip block 7. Keep the Hook, blocks 1-3 and the train/validation table whole. The student still answers "what does `159 of 200` show?".

### Variation — an anxious or slow student

Fill the loss table for **three** rows only (steps 0, 100, 800) and read the gap in one sentence: *"train goes down, validation goes down then up."* Skip the hand work on page 12.3's second half (padding counted). Say the padding idea as *"the blank pages at the end of a test shouldn't count towards the mark"*.

### Variation — harder (a student who finishes early)

1. **Find the stopping point.** *"Change `report=` in block 4 to print every 20 steps up to 300. Where is the lowest validation loss?"* (`T1` found step 80, `2.301`.) Let them report what they measure.
2. **Length and letters.** *"What is the mean length of the 159 copies and of the 41 new names?"* (Not run here; let them find out.)
3. **A different split.** *"Change the seed in block 4's `manual_seed(0)` shuffle and report how much the validation loss moves."* (`T2` moved three training seeds by 0.25; a new split was not measured.)
4. **The bigger question.** *"If I make the model bigger, does the in-list share go up or down? Predict, then test."* (Not run here; the student's result is the data.)

---

## ❓ Questions Students Ask This Week

**"Why does the input start with 0?"** 0 is PAD, used here as the START token: at the first step the model has not yet seen a letter. Nothing real is 0, so a 0 input can only mean "nothing yet".

**"Why not use the real previous letter when generating?"** There isn't one: the name does not exist yet. We only have what the model wrote.

**"Why does training have all the real letters but generating doesn't?"** Because in training we are grading the model on names we already have, and in generating we are asking it to make one.

**"Why is validation worse than random?"** The model is confident and wrong: after reading `am` it puts most of its probability on the letters that followed `am` in its training names, and the held-back names are different. A random guess gives every letter `1/28`, so it never loses by much.

**"Then why not stop at step 80?"** You could; it is the better validation number (`T1`). The course carries the 800-step recipe into Week 13 because the names it generates give the sampling experiments something to work on. Say it plainly.

**"Is `amira` a new name?"** It is a string that is not in our list and a name in the world. The program did not know that; it got there by letters. "Novel" in this course means *not in the list*.

**"Why do we not count the padding?"** It is not part of the name. If we counted it, the program would score well for predicting blanks.

**"Why `dim=1` in `torch.cat`?"** The `dim` is which axis to glue along. `dim=1` joins columns, so a `(231, 1)` and a `(231, 7)` make `(231, 8)`. `dim=0` would stack rows and need matching columns.

**"Can I use `nn.LSTM` instead of the cell?"** Yes; the student has it from Week 11. The cell is used today so that there is one step to call during generation. (We did not time the two.)

**"Does a real language model do this?"** Yes, with letters replaced by pieces of words and the LSTM replaced by attention (Week 14): train on the true previous tokens, generate on its own. The size is the difference.

**"Will my numbers match yours?"** The calculator numbers (`1.1513`, `0.5857`) match exactly. The tables should match on the same machine with the same seeds; on another build the third digit of a loss and a count of names may move. The shape will not.

---

## ⚠️ Where This Lesson Goes Wrong

1. **"The model invents names."** Ask: *"what did block 6 say at step 800?"* (159 of 200 in the list.) *"What did it say at step 100, and were those names?"*
2. **The student reads a low validation loss as a success.** It is only a success if the honest recipe produced it (Clinic 5). Ask what was fed in.
3. **Validation above `3.332` is "a bug".** It is memorising; Clinics 5 and 6 are the real bugs.
4. **The student fixes Clinic 2 by trimming `targets`.** Both tensors are then 7 steps and the loss works, and the model never sees the last letter's turn to speak (no EOS target). Point out the lost EOS. (We did not run this variant.)
5. **The exponent and digits are dropped.** `0.906` copied as `0.9`. Say it in words.
6. **Timing is quoted as a result.** "Generating is 20 times slower" is a measurement on this laptop. It is in `T3`, not in the student's page.
7. **The student compares `0.906` with Week 13's `1.026`.** Different runs, different dropout state. Block 7 prints both for one run.
8. **The quiz result gets gamified.** The point is that "real" and "in the list" are different questions. Do not score the Hook.
9. **`T1` gets mentioned in class as "the right number of steps".** It is one validation curve of one seed on 31 names. It is why we say "800 steps is the recipe", not "800 steps is best".

---

## 🧭 Differentiation

### If the student is struggling

- Do **only** blocks 1, 2 and 4. Skip the model's code (give them block 3 to paste and read, not to type) and the generation.
- Hand table 12.4 with three rows (0, 100, 800) and the sentence *"train goes down, validation goes down then up."*
- Replace page 12.5 with one line: *"of 200 names written by the 800-step program, about 160 were in the list."*
- The idea in three lines: *the right letter goes in while learning; its own letter goes in while writing; the blanks are not marked.*

### If the student is flying

- **The stopping point.** Find the lowest validation loss on their own split (`T1` found step 80 on this one).
- **The baseline.** *"What would a program that only knows how often each letter occurs score on the 31 held-back names?"* (`2.735`, `T1`. They can work it out with counts, a dictionary and `math.log`; do not give them `bincount`.)
- **Teacher forcing by hand.** `T3`'s check: feed the true letters one at a time with `model.step` and compare to the whole-batch pass. (Gap `0.0e+00`.)
- **The reference module's exposure-bias exercise.** It asks for the model's loss on its own generated names fed back through with teacher forcing. That is **Week 13's** measurement; point them at it, and do not let them finish it today.

### If the student won't engage today

Play the quiz again with their own name list: five names of people they know, and five that a friend invents. Ask which are which. Then the count: *"the program copied four out of five of the names it had been given."* That is the Hook, and the one idea worth keeping. The code can be blocks 1 and 6 printed and read aloud.

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"What goes into the model at each step during training, and what during generation?"** *Pass:* training, the true previous letter (shifted right, with a start token); generation, the model's own last pick.
2. **"Why does training need no sampling inside the loop but generation does?"** *Pass:* in training all inputs exist up front; in generation the next input is the last answer.
3. **"What does `ignore_index=PAD` do, and what would happen without it?"** *Pass:* it leaves padding positions out of the average; without it the number is flattered by easy blanks (`0.5857` against `1.1513` on the toy).
4. **"Train loss `0.906`, validation loss `3.417`: what has happened?"** *Pass:* the model has memorised its 200 names and is confident and wrong on the 31 it has not seen (Week 5's gap).
5. **"159 of 200 generated names are in the training list. What does that show, and what doesn't it show?"** *Pass:* it shows most of the output is remembered; it doesn't say the rest are good names, and it is one recipe on 231 names. (Bonus: the 100-step model has almost none in the list and almost none are names.)

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Predicts validation turning round before running; explains "known inputs" as the reason training needs no sampling in the loop and generation does; reports both the 159 and the 1 and says the second set of names were mostly not names; spots that `0.001` validation in Clinic 5 is a leak. |
| **3 — Secure** | Builds the shift with `torch.full` and `torch.cat`; explains `ignore_index`; reads the train/validation gap; counts novelty and says what it means. |
| **2 — Developing** | Gets the shift and the loss; thinks "new" means "invented" or "good"; needs help flattening the scores. |
| **1 — Not yet** | Cannot say what goes into the model at each step. Repeat the Hook at the start of Week 13, before sampling. |

---

## 📤 Homework to Assign

The workbook has six pages (12.1-12.6). The student does them in order, and **writes predictions before running anything**.

1. **12.1 Encode and shift by hand** — three names (`uma`, `bex`, `kaia`): target rows and input rows, ids from the table the student prints.
2. **12.2 How much of a batch is padding** — four names by hand, then the real `1,404` and `444`.
3. **12.3 A loss by hand** — four steps with given probabilities: four surprises, the average, and the same four steps with padding counted.
4. **12.4 Train against validation** — the measured table from their own run (seed 0), one sentence on the gap, and where they would stop.
5. **12.5 The name audit** — the two-column table, twenty names marked by eye, one sentence on what the count shows and doesn't.
6. **12.6 The report** — a short paragraph, every number from their own run in the last 24 hours with the seed stated, and the **Bug Log**: any real error they met, with its last line copied and the fix.

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated. Estimated time: 60-75 minutes.

---

## 🔑 Answer Key

### Page 12.1 — Encode and shift by hand (from `K1`)

| Name | targets | inputs (shift right, START = 0) |
|---|---|---|
| `uma` | `22, 14, 2, 1, 0, 0, 0, 0` | `0, 22, 14, 2, 1, 0, 0, 0` |
| `bex` | `3, 6, 25, 1, 0, 0, 0, 0` | `0, 3, 6, 25, 1, 0, 0, 0` |
| `kaia` | `12, 2, 10, 2, 1, 0, 0, 0` | `0, 12, 2, 10, 2, 1, 0, 0` |

*Marking:* each name is 2 marks (targets right, inputs right). *Common errors:* forgetting EOS (a `1` after the last letter); the START token put in the targets; the inputs **not** shifted (the targets copied). The letters' ids are read from the student's printed `aarav`/`anika` table in block 1 and extended with `encode` or `STOI` (block 1 imports both): accept any ids the student checked with code.

### Page 12.2 — How much of a batch is padding (from `K1`)

| | Real targets | Total | Padding | Share padding |
|---|:--:|:--:|:--:|:--:|
| `uma, bex, wren, kajsa` | 19 (4 + 4 + 5 + 6) | 32 | 13 | 40.6% |
| all 231 names | 1,404 | 1,848 | 444 | 24.0% |

Mean letters per name: `5.08`. *Marking:* the first row by hand (3 marks); the second copied from block 3 (1 mark). *Common error:* forgetting the EOS as a real target (`3+3+4+5 = 15` instead of `19`).

### Page 12.3 — A loss by hand (from `K1`)

Probabilities `0.4, 0.5, 0.25, 0.9`:

| Step | `p` | surprise `-ln p` |
|:--:|:--:|:--:|
| 1 | 0.4 | 0.9163 |
| 2 | 0.5 | 0.6931 |
| 3 | 0.25 | 1.3863 |
| 4 | 0.9 | 0.1054 |

Average over the four real steps: **`0.7753`**. With four padding steps the model is 99% sure of, averaged in as well: **`0.3927`**. *What to draw out:* the second number is about half of the first and the model learned nothing more about names. *Marking:* four surprises (2 marks), the average (1), the padding-counted number (1), one sentence (1). Accept any value within `0.001`.

### Page 12.4 — Train against validation (from block 4)

| step | train | validation |
|:--:|:--:|:--:|
| 0 | 3.346 | 3.349 |
| 100 | 1.960 | 2.308 |
| 200 | 1.431 | 2.544 |
| 300 | 1.103 | 2.880 |
| 400 | 0.984 | 3.077 |
| 600 | 0.921 | 3.314 |
| 800 | 0.906 | 3.417 |

Model sentences: *"Train fell from 3.346 to 0.906 while validation fell to 2.308 at step 100 and then rose to 3.417, above the 3.332 of a model that knows nothing. The program has memorised the 200 names."* *Where to stop:* "around step 100" is the answer the table supports; **step 80 (`2.301`) is the right answer if they printed more rows** (`T1`). *Marking:* 5 marks for the table (digits in full), 1 for the sentence with two numbers, 1 for a stopping point with a reason. *Do not score the predictions;* look for a student who predicted "validation keeps falling" and said what surprised them.

### Page 12.5 — The name audit (from block 6)

The table is in 🎲. Model sentences: *"At 800 steps 159 of 200 generated names are in the training list (79.5%) and only 147 are different; at 100 steps 1 of 200 is in the list, 199 are different, and most are not names (`gmana`, `dareltl`). Counting 'not in the list' does not tell me whether a name is good."* *Judgement (twenty strings marked by eye):* **not keyed**. Look for a student who marks `naya`, `rusha` as "could be" and `argek` as "could not" and can say why in letters, or who says the 100-step names are mostly not names. *Marking:* the table (4 marks), the eye-marks done (1), the sentence (2).

### Page 12.6 — The report (model answer and rubric)

Model: *"With seed 0, the model trained on 200 names reached a train loss of 0.906 and a validation loss of 3.417 after 800 steps; its validation loss was lowest, 2.308, at step 100 among the steps I printed. Of 200 names it generated at 800 steps, 159 (79.5%) were already in the training list; at step 100, 1 was. The gap is Week 5's memorising. The names in neither list at step 100 were mostly not names, so 'new' doesn't mean good. This is one recipe on 231 typed names."*

| Criterion | Marks |
|---|:--:|
| Two numbers **with every digit**, from their own run, seed stated: one loss, one count | 2 |
| States the cause of the gap (memorising the 200 names) in one sentence | 1 |
| States what the count shows **and** what it doesn't (new is not good) | 2 |
| States one limit (one recipe, 231 names, 31 validation names, seed) | 1 |

A write-up that says "the model invents names" loses the last three marks regardless of the rest. **Bug Log:** any real entries are fine if the **last line** of the traceback (not the whole) was copied and the fix works.

### Teacher-only: the Clinic, at a glance

| # | Loud / silent | Last line (or tell) | One-line fix |
|:--:|:--:|---|---|
| 1 | loud | `TypeError: full(): argument 'size' (position 1) must be tuple of ints, not int` | `torch.full((231, 1), PAD)` |
| 2 | loud | `ValueError: Expected input batch_size (2079) to match target batch_size (1848).` | `data[:, :-1]` in the glue |
| 3 | loud | `RuntimeError: Expected target size [231, 28], got [231, 8]` | `.reshape(-1, VOCAB_SIZE)` and `.reshape(-1)` |
| 4 | **silent** | loop reports `0.772`; honest letters-only `0.913` | `ignore_index=PAD` everywhere |
| 5 | **silent** | train `0.0027`, validation `0.001`; names `llllllll` | feed `inputs`, not `targets` |
| 6 | **silent** | `3.629, 3.543, 3.659` vs `3.417` | `model.eval()` before measuring |
| 7 | **silent** | 200 names, 1 distinct | create `rng` once, outside the loop |
| 8 | does not bite | 0 of 200 asked for padding | keep the line as insurance |

### Answers to every question posed in the lesson

| Question | Answer |
|---|---|
| Which names on the card are from the list? | `tamara, dmitri, sigrid, kavya, heidi, noor`. The program wrote `amira, arnata, clala, camendid, fakori, andriia`. |
| Is `amira` an invented name? | Not in the list; a name in the world. "Not in the list" is the only definition of new today. |
| How many of the program's 200 are names it was given? | 159 at 800 steps (seed 0 training, generator seed 1); 1 at 100 steps. |
| What is the longest name, in steps? | 7 letters plus EOS: 8 columns. |
| What is `anika` as numbers? | `[2, 15, 10, 12, 2, 1, 0, 0]`. |
| What is the input at step 0, and why? | `0`, the START token: nothing has been said. |
| What is the input at step 6 for `anika`? | `1`, EOS, the last thing said. |
| Could you work out the input at step 5 before step 2 has run? | Yes: it is a letter of the name. That is teacher forcing. |
| What goes in at each step when generating? | The model's own last pick. |
| Which of training and generating has every input known before the model runs? | Training. |
| How surprised is a model by a blank it is 98% sure of? | `-ln 0.98 = 0.0202`. |
| What happens to the toy loss if you count the blanks? | `1.1513` falls to `0.5857`. |
| What should an untrained model score? | About `ln 28 = 3.3322`; ours gives `3.3455`. |
| How much of the real grid is padding? | `444` of `1,848` (24.0%). |
| Validation above 3.332: a bug? | No, memorising: confident and wrong on unseen names. |
| When was validation lowest (student's rows)? | Step 100 (`2.308`); step 80 (`2.301`) if more rows are printed. |
| Which model is better at inventing names? | Neither, until "better" is defined: the 800-step copies; the 100-step makes mostly non-names. |
| What is `1.026` and what is `0.934`? | The last training step with dropout on, and the same model measured with dropout off (all 231 names). |
| Does the count show the names are good? | No. It shows how many are in the list. |
| What did we **not** do today? | Rate the quality of names, try other sizes or seeds (beyond `T2`), or choose letters any way but the plain draw. |

---

## 🔮 Next Week Preview

**Week 13 — Choosing the Next Letter: Sampling and Exposure Bias** (🟦 teach). Today's generator used the simplest dice-roll there is, at the model's own probabilities, and it mostly gave back the training list. Next week the student opens the roll: **greedy** (always the top score), **temperature**, **top-k** and **top-p**, predicted on a 5-letter distribution before each is run, then plugged into the generator they wrote today, and the novelty counts repeated. The new syntax is `F.softmax(dim=-1)`, `torch.multinomial`, `torch.topk`, and top-p via `torch.sort` + `torch.cumsum`. The last ten minutes measure something new: the model scores its *own* names worse than real ones, and a model trained on the truth drifts when it reads its own words.

**What from today carries over:** `NameLSTM` and its `step` / `init_state` (Week 13 re-types them as a module, `namelm.py`, whose `train()` takes no rows and trains on all 231 names; it prints **`final loss 1.026`**, the number block 7 printed for the same recipe, which is the check that yours and the course's agree), `make_name` (Week 13 takes a `pick` function in place of `draw`), `F.cross_entropy(..., ignore_index=PAD)`, and the counting habit: *count, do not eyeball.* **If page 12.4 or 12.5 is blank, do it before Week 13**; the student needs the numbers from the 800-step and the 100-step runs.
