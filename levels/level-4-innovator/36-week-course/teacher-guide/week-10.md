# Week 10 — Forty Multiplications: Why Memory Fades

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md)

---

![Map of the 36 weeks with Week 10, Forty Multiplications, highlighted in Term 2](../figures/fig-w10-0-where-this-fits.svg)
*Figure 10.0 — Week 10 is the first lesson of Term 2 on memory: why a loop forgets.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~60-70 min) |
| **Type** | 🟩 Lab — the student *measures* a disease (how far back a recurrent cell's learning signal reaches) at four sequence lengths and four settings, then forces the opposite disease and tests the one cure they already own |
| **Big idea** | Learning a recurrent cell means sending an error *backwards* through the unrolled loop of Week 8. At every step back it is multiplied by that step's slope. **The same kind of number, multiplied forty times, is not "a bit smaller"; it is gone (below 1) or enormous (above 1).** Clipping can turn the volume *down*; it cannot turn it up. |
| **New vocabulary** | **compounding** · backpropagation through time · position (in a sequence) · exploding gradient. (**Vanishing gradient** and **clipping** are *already theirs*, Week 6. Say so, and use them.) |
| **New maths** | **Compounding** — a number multiplied by itself `T` times. Met on paper first: `0.9526` forty times is `0.143`; `0.95` forty times is `0.1285`; `1.05` forty times is `7.04`. See the 🔢 section. |
| **New syntax** | `h.retain_grad()` · `torch.stack` · `torch.randn(T, ...)`. Three, under the ladder maximum of four. |
| **Dataset** | None. The inputs are **seeded random numbers** (`torch.randn`): `T` inputs of 4 features each. **Nothing downloads. No internet.** |
| **Model** | **Real PyTorch**, used as in Week 8: a 16-number recurrent cell written out as a loop (the student's own `unroll`), with **untrained, seeded random weights** (`nn.RNN` is borrowed only as a source of them). There is **no language model and no stand-in** in the student's lesson. The only "training" is **one** update of the knobs, in the explosion test. |
| **Materials** | Laptop with Python 3 and torch (nothing new to install) · a calculator with a power key (a phone in calculator mode is fine; **airplane mode on**) · workbook pages 10.1-10.6 · a timer. Nothing imports `l4lib` today. |
| **Prep time** | 25 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | The student's whole file (`week10.py`, seven blocks) runs in **under 1 second**. The teacher-only blocks add about **5 seconds** (the trained check is 15 short trainings). Anything over **30 seconds** means something is wrong (see Fallback). |

> **⚠️ Watch out:** the thing that goes wrong this week is **the numbers get over-read.** Everything measured today is an *untrained, random* cell and a *single* toy score (the last note's sum). It shows how the **learning signal** from the first position behaves at the **start**. It does **not** show that a trained recurrent net cannot remember forty steps (in the teacher-only block `T2` one *can*, 4 seeds in 5, and then fails at 80 for 4 seeds in 5). Say "the signal reaching the first word is `2e-10` against `4` at the last", never "RNNs cannot remember". The second thing that goes wrong is **calling any of it a result about language models.** It is not; Week 14 argues why attention was invented, and that is a design argument, not today's measurement.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Compound by hand**: compute `r ** k` on a calculator for `r` below and above 1, and say, *before* they press the key, whether the answer will be tiny, near 1, or large.
2. **Say why an error vanishes or explodes on its way back through a loop**: "at every step back it is multiplied by that step's slope; forty slopes below 1 multiply to almost nothing; forty above 1 to a huge number".
3. **Measure it**: print the size of the gradient at position 1 for `T` = 10, 20, 40, 80 and four recurrent-weight settings, and read the table in one sentence per row.
4. **Force an explosion and test the cure**: one update with and without `clip_grad_norm_`, reading the *weight size before and after*.
5. **Say what clipping does not do**: it rescales everything by one number, so it cannot bring back a signal that has already vanished.

Observable evidence: the filled grid on workbook page 10.4, the with/without table on page 10.5, and a short report on page 10.6 in which **every number was printed by the student's own run**.

---

## 🧑‍🏫 What YOU Need to Know First

This section is your background reading: the maths, what is real and what is not, the new code, and the numbers you should expect to see. Read it before class.

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** (the seven student blocks, the teacher-only blocks `T1`, `T2` and `K1`) and in the **🐞 Debugging Clinic** was run, in order, in **one shared session** on a CPU with one thread and the seeds shown. The seven student blocks are the pieces of **one file, `week10.py`**, pasted one under the other with no gap: each later block uses names defined by an earlier one. The Clinic blocks are *deliberate mistakes*, each marked, each run in a copy of that session; their tracebacks are real. **Timing lines vary run to run; every other number repeated exactly on a second full run on the same machine.** A different CPU or PyTorch build can move the last digit, and for a quantity like `2.06e-10` the *second* digit; the orders of magnitude and the shape of every table do not move. Tracebacks show `/home/you/l4/...` for the path, and the long middle of a torch traceback is replaced by `... frames inside torch (elided) ...`; **the last line is always the real, complete last line.** The *line numbers* in a traceback depend on exactly how the blocks were pasted; the last line does not.

### 1. What the student is doing today, in one paragraph

Last week the student wrote a hidden state down and watched a note fade. Today they ask the question Week 8 left open ("*how fast* does it fade?") in the form that matters for learning: **how much does the answer at the end care about the word at the start?** They first meet *compounding* on a calculator (a message passed through forty people; `0.95` forty times), then do the same multiplication with **slopes taken from last week's own four notes**. They build a **parked-note cell**, one number whose slope is the same at every step, and watch the gradient at each position be a power of `0.9526`. Then the real thing: a 16-number cell, forty to eighty steps long, and a table of the gradient at position 1. They *predict each cell of a 4 by 4 grid* (tiny, level or huge), print it, and find the same machine gives `9e-03`, `2e-10` or `7e+07` depending on one setting. Last they force an explosion and test clipping. **Nothing is trained, apart from the one update in that last test.** Fixing the vanishing side is Week 11.

### 2. 🔢 The maths you need — taught to you first

**One new idea: compounding.** *A number multiplied by itself `T` times is `r ** T`.* The student has met two seeds of it: `0.9 ** t` in the Week 2 half-life table, and last week's note losing about half of itself each step. Do **each of these yourself, with a calculator, before class**.

**(a) The same multiplication in three directions.** From block 1 (every number below is printed there):

| Multiplications `k` | `0.9526 ** k` | `0.95 ** k` | `1.05 ** k` |
|:--:|:--:|:--:|:--:|
| 1 | 0.9526 | 0.95 | 1.05 |
| 2 | 0.9074 | 0.9025 | 1.103 |
| 5 | 0.7844 | 0.7738 | 1.276 |
| 10 | 0.6153 | 0.5987 | 1.629 |
| 20 | 0.3786 | 0.3585 | 2.653 |
| 40 | **0.1434** | **0.1285** | **7.04** |

Read the **shape**, not the table. A number a *little* under 1 loses about 5% per step, and after forty steps you have about *one-eighth*. A number a *little* over 1 gains about 5% a step and after forty you have *seven times*. **Neither is "about the same".** The student's intuition says "5% is small, so I keep about 80%"; the true answer is nowhere near. That surprise is the lesson, so let them **commit to a guess in writing first**.

**(b) How long until it halves.** `0.9526` first drops below one half after **15** multiplications (`0.4827`); `0.95` after **14**; and `1.05` first passes **double** after **15** (`2.0789`). A good rule of thumb to offer: *"at 5% a step it halves (or doubles) in about 14 or 15 steps"*. Say "about"; it is a rule of thumb, not a formula.

**(c) The slope of one step.** Last week's cell is `new note = tanh(W_xh x + W_hh x old note)`. *How much does the new note move if you nudge the old one?* The student has the method (Level 3 Week 12): nudge by a tiny step, divide. For this cell the answer is `W_hh x (1 - new note squared)` (the tanh slope is `1 - note squared`; the student **checks** the shortcut by nudging, they are not asked to derive it, and you do **not** say "derivative"). Using last week's four notes (`0.7616, 0.3634, 0.1797, 0.0896`, with `W_hh = 0.5`), block 2 prints the slopes **into** notes 2, 3 and 4: `0.4340`, `0.4839`, `0.4960`. From note 1 to note 4 the error is multiplied by all three: `0.4340 x 0.4839 x 0.4960 =` **0.1041**. (The reference module prints `0.1042` because it multiplies the *rounded* slopes; ours multiplies the unrounded ones. Say "about a tenth".) **Three steps back, a tenth of the signal is left. Forty steps back, at a typical slope of `0.5`: `0.5 ** 40 =` `9.1e-13`.** The whole week is that sentence.

**(d) The "parked" cell: where `0.9526` comes from.** If the note sits still at `0.2177`, then `1 - 0.2177 ** 2 =` **0.9526**, the *same slope at every step*. Then, in a chain of 41 notes, the gradient at position `p` is `0.9526 ** (41 - p)`: position 41 (the last) is `1`, position 40 is `0.9526`, position 1 is `0.9526 ** 40 = 0.143`. Block 3 builds this cell. It is a **designed** cell, chosen so that one number repeats; it is *not* what a trained cell looks like. The measured gradient at position 1 is `0.1447`, not `0.1434`: the note drifts from `0.2177` to `0.217` by position 41 and the slope drifts with it. If the student asks why the two disagree in the third decimal, that is the answer.

**(e) Above 1 is the same arithmetic.** `1.05 ** 40 = 7.04`. At a slope of `1.2` per step (about where the scale-8 cell sits, section 6) forty steps multiply by about `1,470` (`1.2 ** 40`, printed in `K1`).

> **🚫 What you must NOT do with the maths.** (1) **Do not write "derivative", "Jacobian", "spectral radius" or "eigenvalue".** The reference module uses them; the student has none of them. The slope of one step is "how far the new note moves when the old one is nudged", and that is all. (2) **Do not use logarithms to solve `r ** k = 0.5`.** A loop (block 1's `while`) gets the answer; logs are Week 21. (3) **Do not say "the slopes are all the same"** about the *real* cell in `probe`; they are not (section 6 shows the *typical* slope wandering with `T`). The parked cell is the only place they are equal, and only because we built it. (4) **Do not let "compounding" slide into "interest" for more than a minute.** The bank analogy gets the idea in; the cell is the point.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Status |
|---|---|
| Every number in the Hook and Concept tables | **Real arithmetic**, printed by blocks 1 and 2. |
| The recurrent cell in `unroll` | **Real** `tanh(W_ih x + W_hh h + b)`, the same loop as Week 8's `loop.py`; the weights come from a seeded `nn.RNN(4, 16)` and are **untrained**. |
| The "scale" setting | **Ours.** `scale = 1` is PyTorch's own initial weights; `2`, `4`, `8` multiply the recurrent matrix by that number. It is *a knob we turn*, not something found in a model. |
| The "loss" (`states[-1].sum()`) | **A toy.** One number made from the last note. A real model has a loss at every position (see section 7). |
| The parked cell | **Designed** (weight `1.0`, bias `0.0035`, start `0.2177`), so that every slope is `0.9526`. |
| The clipping test | **Real** `torch.optim.SGD` and `clip_grad_norm_`, **one** update, learning rate `0.1`, `max_norm = 1.0`. One seed. |
| Any language model, scripted client or `FakeClient` | **Not present.** |
| Block `T2` (teacher only) | **Real** training of an `nn.RNN(1, 16)` for 300 Adam steps, 15 trainings, on a toy task invented for this check ("report the sign of your first input"). **A stand-in task, not a model, and not in the student's lesson.** |

> **🚫 What you must NOT claim about today's numbers.**
> 1. **"RNNs cannot learn long-range things."** Today's numbers are the gradient of an *untrained* cell. `T2` trains one: at `T = 40` it got the first input right on **4 seeds of 5**; at `T = 80` it failed on **4 of 5** (and succeeded on the fifth). So: "at the start the signal is tiny", not "it cannot".
> 2. **"The gradient is `10^-10`, so nothing learns."** The table's quantity is the gradient **at position 1**. The gradient on the **knobs** is a sum over all positions and the *last few* dominate it: at scale 1, `T = 40`, the recurrent knobs' gradient has size `7.22` in block 7 (not tiny at all) while the signal from position 1 is `2e-10`. **A healthy-looking total and a vanished beginning are the same run.**
> 3. **"Exploding always happens above scale 1."** In block 6, scale 8 explodes for **four** of five seeds and *vanishes* for seed 3 (`5.5e-07`). A likely reason, **not tested further**: seed 3's notes are pinned at +-1 more often (`0.655` of them against `0.444`-`0.495` for the other seeds, in `T1`), and a pinned `tanh` has a slope near 0.
> 4. **"Clipping fixes it."** It stops one update from wrecking the weights. It does **not** bring a vanished signal back (it only multiplies everything by one number), and block 7 shows that with `max_norm = 1.0` it also shrinks a *healthy* gradient (`7.22` to `0.51` at scale 1). The honest summary: **a seatbelt, not an engine**.

### 4. The three new constructs, for somebody who has never seen them

**(a) `h.retain_grad()` — keep the gradient of an in-between value.** (The snippets in this section are excerpts of block 4, shown for reading, not blocks to run.)

```text
h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
h.retain_grad()                       # ask PyTorch to keep h's gradient after backward()
```

Read as: *"`h` was made from other things, so it is an in-between value. PyTorch normally throws away the gradient of in-between values to save memory and keeps only the knobs'. This line says: keep this one."*

After `backward()`, `h.grad` is the slope of the final number with respect to that `h`: **how much the end cares about this note**.

Two rules, each with a Clinic entry:

1. It only works on a value PyTorch is *tracking*. If the weights were copied with `.data` (the Week 8 habit) there is nothing to track and it raises an error (Clinic 1).
2. It must be called **before** `backward()`. If it is left out, `h.grad` is `None` with a warning that explains why (Clinic 2).

**(b) `torch.stack(list_of_tensors)` — join a list into one new tensor.**

```text
states = torch.stack(hs)              # hs is a LIST of 40 tensors of 16 numbers  ->  one tensor, shape (40, 16)
```

Read as: *"a pile of sheets: forty sheets of 16 numbers become one pile of shape (40, 16)."* The result has a **new first axis**. It takes **one list**, not tensors one after another (Clinic 3). The student already knows `torch.cat` (Level 3 Week 27), which joins along an axis that *exists*; `stack` makes a new one. If they ask for the difference: two tensors of 2 numbers, `cat` gives 4 numbers, `stack` gives a 2-by-2 grid. (Say it; we did not run it.)

**(c) `torch.randn(T, 4)` — seeded random numbers of a chosen shape.**

```text
x = torch.randn(5, 4)                 # 5 inputs, 4 numbers each, bell-shaped around 0
```

Read as: *"random numbers, mostly between -2 and 2, in a grid of the shape you name."* They are seeded by `torch.manual_seed` (`make_cell` does this), so a run repeats. The shape matters: `torch.randn(5)` is five *single numbers* and the cell needs five *rows* (Clinic 4). The habit: say the shape aloud before pressing Enter.

### 5. The other code the student types — nothing new, but note these

All old: `nn.RNN(D, H)` and `rnn.weight_hh_l0.data = ...` (Week 8: assigning `.data` to *set* a weight; here to weight-times-scale), `@` and `torch.tanh` (Week 8's `loop.py`), `tensor.norm()` and `torch.optim.SGD` (Week 2), `clip_grad_norm_` (Week 6), `requires_grad=True` (Level 3), `.float().mean()` on a true/false mask (Week 1), `while` and `for` loops, f-strings with `.2e` (Week 6), a function with default arguments (`def probe(T, scale=1.0, seed=0)`), and `x[t]` for the `t`-th row.

**Not used today, on purpose**, because they are later rungs: `nn.LSTM`, `nn.GRU`, `nn.LSTMCell` (Week 11), `F.cross_entropy` (Week 12), `F.softmax` (Week 13), attention (Week 14). `nn.RNNCell` is not on the ladder: the loop *is* the cell. **The teacher-only blocks use a few things the student never sees** (a fractional power `** (1 / (T - 1))`, `nn.functional.binary_cross_entropy_with_logits`, an `Adam` optimizer on a head, `math.tanh` in a loop) and are marked. Do not paste them into the student's file.

### 6. What the numbers will say

Read these before class so nothing surprises you. **Every number is printed by the blocks below.**

- **Compounding.** `0.9526 ** 40 = 0.1434`, `0.95 ** 40 = 0.1285`, `1.05 ** 40 = 7.04`. Halving takes 15 and 14 steps; doubling at `1.05` takes 15.
- **Last week's slopes.** `0.4340, 0.4839, 0.4960`, product `0.1041`; the nudge check gives `0.4339` against the shortcut's `0.4340`.
- **The parked cell.** Position 1 gradient `0.1447` against `0.9526 ** 40 = 0.1434`; position 21 `0.3809` against `0.3786`.
- **The probe at scale 1, T = 40.** The gradient at position 40 is `4.0` (the loss is the sum of 16 numbers, each with slope 1, so the length is `sqrt(16) = 4`). Going back: position 30 `5.39e-03`, 20 `1.09e-05`, 10 `2.24e-08`, 1 `2.06e-10`. Each ten steps back costs a factor of roughly **500 to 740** (`742`, `494`, `487`; the last nine steps `109`).
- **The grid** (block 5), the gradient at position 1:

| scale | T = 10 | T = 20 | T = 40 | T = 80 |
|:--:|:--:|:--:|:--:|:--:|
| x1 | 9.15e-03 | 1.01e-05 | 2.06e-10 | 4.69e-21 |
| x2 | 5.63e-01 | 1.66e-02 | 2.25e-03 | 2.93e-06 |
| x4 | 1.08e+01 | 1.14e+01 | 2.09e+01 | 3.36e+03 |
| x8 | 3.49e+01 | 2.55e+02 | 4.38e+03 | 6.92e+07 |

**Say the shape of each row.** Scale 1: falls by orders of magnitude, in every row. Scale 2: falls, more slowly. **Scale 4: roughly level at 10 to 20 up to `T = 40`, then it climbs.** Scale 8: climbs every time, to `7e+07`. **No row stays near `4`, the value at the last position.** That is the point of the week: *none of the four settings we tried is a comfortable middle*, and the near-1 one is a knife-edge. `T1` prints the *typical slope per step* (`(gradient at 1 / gradient at last) ** (1 / (T - 1))`): `0.51`-`0.55` at scale 1, `0.75`-`0.84` at scale 2, `0.89`-`0.98` at scale 3, `1.04`-`1.12` at scale 4, `1.20`-`1.27` at scale 8. Near 1 is the knife-edge, and the typical slope *wanders* with `T`.
- **Seeds** (block 6, `T = 40`): scale 1 gives `2.1e-10, 8.4e-11, 9.8e-10, 4.7e-09, 1.9e-14`: all tiny, spanning five orders of magnitude. Scale 8 gives `4.4e+03, 8.8e+04, 9.7e+05, 5.5e-07, 1.1e+05`: four huge, one vanished.
- **One update** (block 7, `T = 40`, seed 0, `lr = 0.1`). Scale 8, no clip: the recurrent knobs' gradient has size `8.55e+04`, the weight matrix's size jumps `17.87` to **`8548.25`**, and the share of notes pinned at +-1 goes `0.484` to **`0.997`**. With clip: gradient rescaled to `0.878`, weights `17.87` to `17.87`, pinned `0.484` to `0.494`. **Clipping saved the weights; it did not make the cell healthy (about half the notes were already pinned before the update).** Scale 1: `7.22` becomes `0.514` when clipped, the weights go `2.23` to `2.40` plain and `2.24` clipped, nothing pinned either way.
- **Trained check (`T2`, teacher only).** `T = 10`: all five seeds `1.0`. `T = 40`: four at `1.0`, one at `0.503`. `T = 80`: `0.47, 0.484, 0.5, 0.497` and one at `1.0`. Chance is `0.5`.

![Two bar panels: 0.9526 multiplied in a row shrinks from 0.9526 to 0.1434 over forty steps, while 1.05 grows from 1.05 to 7.04](../figures/fig-w10-1-compounding-forty-steps.svg)
*Figure 10.1 — Multiplying by a number below 1 forty times leaves almost nothing, above 1 gives a big number; only exactly 1 stays put.*

![A four by four grid of measured gradients at position 1, from 9.15e-03 down to 4.69e-21 in the top row and up to 6.92e+07 in the bottom row, each cell labelled vanishing, level or exploding](../figures/fig-w10-2-gradient-grid-lengths-scales.svg)
*Figure 10.2 — No setting of the grid keeps the gradient near the 4.0 of the last position: it vanishes or explodes by orders of magnitude.*

### 7. The honest limits of today

1. **Untrained weights, random inputs, a toy loss.** All three are *probes*, not a model. The reference module's table (`3.28e-12`, `9.38e+06`, ...) comes from a different net (a character model with 96 units) and its numbers **do not match ours and should not**; do not quote one against the other.
2. **One width (16), one input size (4).** We did not test other widths. Five seeds only, and only at `T = 40`.
3. **The gradient at position 1 is not the whole learning signal.** The knobs are updated by a *sum* over positions, dominated by the last few. A cell can train fine and still ignore the first word, or (as `T2` shows) learn to use it although the early signal is tiny. We **did not explain** why `T2` succeeds at 40 and fails at 80. Adam rescales each knob's step (Week 3), a possible contributor we did not test. Say "I do not know why yet".
4. **Clipping was tested on one step, with one `max_norm` (`1.0`) and one learning rate (`0.1`)**; neither was tuned.
5. **The parked cell is a construction.** It teaches the arithmetic; it is not evidence about trained cells.
6. **A wording note for you.** The Week 9 teacher preview says the cell is "trained for real" today. It is **not**, apart from the single update in the clipping test: today measures the *start* of training. If the preview raised the expectation, say plainly: *"we measure whether learning can even start; Week 12 trains one properly."*

### 8. The three misconceptions you will actually meet

1. **"It's only 5% per step, so it only loses 5%."** The step is 5%; the forty steps compound. Fix: the calculator, `0.95 ** 40 = 0.1285`. Let them press the key themselves.
2. **"The gradient shrinks because the network is bad / the weights are small."** The same weights give `2e-10` or `7e+07` depending on a setting that changes only their size by a factor of 8. It is the arithmetic of repeated multiplication, not quality.
3. **"So clip it and it's fixed."** Block 7 shows what clipping does (a bounded weight update) and what it does not (a cell whose notes are half pinned stays that way; a vanished signal stays vanished). **A seatbelt is not an engine.**

### 9. How deep to go, and where to stop

Stop at: *"going back through a loop, the error is multiplied by one slope per step; forty slopes of about the same size make a number that is either almost zero or enormous, so there is no comfortable setting."* Do **not** go into LSTM gates or the forget gate (Week 11; the student will ask), the matrix mathematics of *why* the product behaves as it does, truncated backpropagation, or attention as the cure (Week 14). If the student asks *"so how do real models do it?"*: *"Next week is the first answer, gates. Week 14 is the second, and the one chat models use."*

### 10. 🧭 Where Week 10 sits

```text
   W6   a deep chain of layers: slopes multiply; residual road, norm
   W8   a loop: one cell reused; the note fades (said, not measured)
   W9   Review & Assessment 1
   W10  (today) the loop's slopes COMPOUND: forty multiplications
        tiny below 1, huge above 1; clipping fixes only the huge
   W11  gates: a note that ADDS instead of multiplies (the cure for tiny)
   W12-13  training the cell on real names; sampling
   W14  attention: skip the loop altogether
```

---

## 🧰 Prep Checklist

This section is for setting up: the environment check, the student's file with its seven blocks, and the teacher-only checks. Work through it the night before.

### 25 minutes the night before

- [ ] **Confirm the stack.** Nothing imports `l4lib` today, so the only check is torch:

```bash
python3 -c "import torch; print(torch.__version__)"
```

You should see a version (the numbers in this guide came from torch `2.2.1`):

```text
2.2.1
```

`pip` returning 403 is expected and not an error; **nothing this week installs anything.**

- [ ] **Make a working folder and one file, `week10.py`.** Paste the seven blocks below into it **one under the other, with no gap**, running the file after each. Each block uses names defined by the ones above. The output printed under each block is what **that block** prints (the whole file prints all seven in order). Total runtime: under 1 second.

**Block 1 — compounding** (the multiplication on its own)

```python
# compound.py - Week 10: a number multiplied by itself k times. No torch.
for rate in [0.9526, 0.95, 1.05]:
    print(f"rate {rate}")
    for k in [1, 2, 5, 10, 20, 40]:
        print(f"   {rate} ** {k:2d} = {rate ** k:.4g}")

# How many multiplications until it is below one half? (above double, for 1.05)
for rate in [0.9526, 0.95]:
    value, k = 1.0, 0
    while value > 0.5:
        value = value * rate
        k = k + 1
    print(f"{rate}: first below 0.5 after {k} multiplications ({value:.4f})")
value, k = 1.0, 0
while value < 2.0:
    value = value * 1.05
    k = k + 1
print(f"1.05: first above 2 after {k} multiplications ({value:.4f})")
```

```text
rate 0.9526
   0.9526 **  1 = 0.9526
   0.9526 **  2 = 0.9074
   0.9526 **  5 = 0.7844
   0.9526 ** 10 = 0.6153
   0.9526 ** 20 = 0.3786
   0.9526 ** 40 = 0.1434
rate 0.95
   0.95 **  1 = 0.95
   0.95 **  2 = 0.9025
   0.95 **  5 = 0.7738
   0.95 ** 10 = 0.5987
   0.95 ** 20 = 0.3585
   0.95 ** 40 = 0.1285
rate 1.05
   1.05 **  1 = 1.05
   1.05 **  2 = 1.103
   1.05 **  5 = 1.276
   1.05 ** 10 = 1.629
   1.05 ** 20 = 2.653
   1.05 ** 40 = 7.04
0.9526: first below 0.5 after 15 multiplications (0.4827)
0.95: first below 0.5 after 14 multiplications (0.4877)
1.05: first above 2 after 15 multiplications (2.0789)
```

The `while` loops are from Level 2; `value = value * rate` is written out on purpose so the student *sees* the multiplication that `**` hides. `0.9526` and `0.95` halve in 15 and 14 steps; `1.05` doubles in 15.

**Block 2 — last week's slopes** (the same four notes as Week 8's `hand.py`)

```python
# slopes.py - Week 10: Week 8's cell (W_xh = 1.0, W_hh = 0.5, no bias), and the slope from one note to the next.
import math
import torch
import torch.nn as nn
torch.set_num_threads(1)

W_hh = 0.5
notes = [0.7616, 0.3634, 0.1797, 0.0896]          # the four notes of Week 8, hand.py
slopes = []
for h in notes[1:]:                                # the slope INTO each later note
    s = W_hh * (1 - h * h)                         # shortcut: tanh's slope is 1 - note squared
    slopes.append(s)
    print(f"slope into note {h}: {s:.4f}")
print("note 1 -> note 4 is three multiplications:", round(slopes[0] * slopes[1] * slopes[2], 4))

# Check one slope the Level-3 way: nudge the old note, see how far the new note moves.
old, nudge = 0.7616, 0.001
new_a = math.tanh(0.5 * old)                      # x = 0 at step 2, so only the old note feeds in
new_b = math.tanh(0.5 * (old + nudge))
print("by nudging:", round((new_b - new_a) / nudge, 4), "  by the shortcut:", round(W_hh * (1 - new_a ** 2), 4))
```

```text
slope into note 0.3634: 0.4340
slope into note 0.1797: 0.4839
slope into note 0.0896: 0.4960
note 1 -> note 4 is three multiplications: 0.1041
by nudging: 0.4339   by the shortcut: 0.434
```

`s = W_hh * (1 - h * h)` is the slope *into* each later note. The nudge check at the bottom re-does one slope the Level 3 way (nudge `0.001`, divide) and gets `0.4339` against the shortcut's `0.4340`: they agree to rounding, so the shortcut is trusted.

**Block 3 — the parked cell** (one number, the same slope at every step)

```python
# parked.py - Week 10: a one-number cell with W_hh = 1.0 whose note is PARKED at 0.2177, so every slope is the same.
w = torch.tensor(1.0, requires_grad=True)        # the recurrent weight, tracked so a gradient can flow

def run_parked(T):
    h = torch.tensor(0.2177)
    notes = []
    for t in range(T):
        h = torch.tanh(w * h + 0.0035)           # x = 0 every step; 0.0035 keeps the note parked
        h.retain_grad()                          # keep the gradient of this in-between value
        notes.append(h)
    notes[-1].backward()                         # slopes of the LAST note with respect to every earlier note
    return notes

notes = run_parked(41)
print("the note, positions 1, 2, 41:", [round(notes[i].item(), 4) for i in (0, 1, 40)])
print("slope of one step: 1 - 0.2177**2 =", round(1 - 0.2177 ** 2, 4))
for p in [41, 40, 39, 31, 21, 11, 1]:
    print(f"position {p:2d}: gradient {notes[p - 1].grad.item():.4f}   0.9526 ** {41 - p:2d} = {0.9526 ** (41 - p):.4f}")
```

```text
the note, positions 1, 2, 41: [0.2177, 0.2176, 0.217]
slope of one step: 1 - 0.2177**2 = 0.9526
position 41: gradient 1.0000   0.9526 **  0 = 1.0000
position 40: gradient 0.9529   0.9526 **  1 = 0.9526
position 39: gradient 0.9080   0.9526 **  2 = 0.9074
position 31: gradient 0.6173   0.9526 ** 10 = 0.6153
position 21: gradient 0.3809   0.9526 ** 20 = 0.3786
position 11: gradient 0.2348   0.9526 ** 30 = 0.2330
position  1: gradient 0.1447   0.9526 ** 40 = 0.1434
```

**Block 4 — the probe** (the 16-number cell; all three new constructs are here)

```python
# probe.py - Week 10: a 16-number cell, built from Week 8's loop, and a probe of its gradients.
def make_cell(scale=1.0, seed=0, D=4, H=16):
    torch.manual_seed(seed)
    rnn = nn.RNN(D, H)                           # used only as a seeded source of random weights
    rnn.weight_hh_l0.data = rnn.weight_hh_l0.data * scale
    return rnn

def unroll(rnn, x):
    W_ih, W_hh = rnn.weight_ih_l0, rnn.weight_hh_l0
    b = rnn.bias_ih_l0 + rnn.bias_hh_l0
    h = torch.zeros(W_hh.shape[0])
    hs = []
    for t in range(len(x)):
        h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
        h.retain_grad()
        hs.append(h)
    return hs

def probe(T, scale=1.0, seed=0):
    rnn = make_cell(scale, seed)
    x = torch.randn(T, 4)                        # T random inputs, 4 features each, seeded by make_cell
    hs = unroll(rnn, x)
    states = torch.stack(hs)                     # one tensor, shape (T, 16)
    states[-1].sum().backward()                  # the "loss": add up the 16 numbers of the LAST note
    grads = torch.stack([h.grad for h in hs])    # shape (T, 16): how much the loss cares about each position
    return [row.norm().item() for row in grads]

x = torch.randn(5, 4)
print("randn(5, 4) shape:", tuple(x.shape), "  stacked states for T = 5:", tuple(torch.stack(unroll(make_cell(), x)).shape))
g = probe(40)
print("T = 40, scale 1: gradient at position 40 =", round(g[39], 4), "(16 ones, length 4)")
for p in [40, 30, 20, 10, 1]:
    print(f"   position {p:2d}: {g[p - 1]:.2e}")
```

```text
randn(5, 4) shape: (5, 4)   stacked states for T = 5: (5, 16)
T = 40, scale 1: gradient at position 40 = 4.0 (16 ones, length 4)
   position 40: 4.00e+00
   position 30: 5.39e-03
   position 20: 1.09e-05
   position 10: 2.24e-08
   position  1: 2.06e-10
```

`(5, 4)` is `randn(5, 4)`; `(5, 16)` is **five** notes stacked, 16 numbers each. The gradient at the last position is `4.0` every time (a *check*, not a result). Going back: `5.39e-03`, `1.09e-05`, `2.24e-08`, `2.06e-10`.

**Block 5 — the grid** (the main table)

```python
# grid.py - Week 10: the whole experiment. Gradient at position 1, for four lengths and four recurrent-weight scales.
print("gradient at position 1 (the last position's is always 4.0)")
print("scale |       T=10       T=20       T=40       T=80")
for scale in [1, 2, 4, 8]:
    row = [probe(T, scale)[0] for T in [10, 20, 40, 80]]
    print(f"  x{scale}  |" + "".join(f"  {v:9.2e}" for v in row))
```

```text
gradient at position 1 (the last position's is always 4.0)
scale |       T=10       T=20       T=40       T=80
  x1  |   9.15e-03   1.01e-05   2.06e-10   4.69e-21
  x2  |   5.63e-01   1.66e-02   2.25e-03   2.93e-06
  x4  |   1.08e+01   1.14e+01   2.09e+01   3.36e+03
  x8  |   3.49e+01   2.55e+02   4.38e+03   6.92e+07
```

**Block 6 — five seeds** (is that one lucky seed?)

```python
# seeds.py - Week 10: is that one seed's luck? T = 40, five seeds, scale 1 and scale 8.
for scale in [1, 8]:
    vals = [probe(40, scale, seed)[0] for seed in range(5)]
    print(f"scale {scale}: position-1 gradient over seeds 0-4:", [f"{v:.1e}" for v in vals])
```

```text
scale 1: position-1 gradient over seeds 0-4: ['2.1e-10', '8.4e-11', '9.8e-10', '4.7e-09', '1.9e-14']
scale 8: position-1 gradient over seeds 0-4: ['4.4e+03', '8.8e+04', '9.7e+05', '5.5e-07', '1.1e+05']
```

**Block 7 — force an explosion, with and without clipping**

```python
# explode.py - Week 10: one update of the knobs, with and without clipping. T = 40, learning rate 0.1.
def update(scale, clip, lr=0.1, T=40, seed=0):
    rnn = make_cell(scale, seed)
    x = torch.randn(T, 4)
    before = torch.stack(unroll(rnn, x))
    before[-1].sum().backward()
    size = rnn.weight_hh_l0.grad.norm().item()          # the gradient of the recurrent knobs, before any clipping
    if clip:
        nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
    size_after = rnn.weight_hh_l0.grad.norm().item()
    w_before = rnn.weight_hh_l0.norm().item()
    torch.optim.SGD(rnn.parameters(), lr=lr).step()
    w_after = rnn.weight_hh_l0.norm().item()
    after = torch.stack(unroll(rnn, x))
    pinned_before = (before.abs() > 0.99).float().mean().item()
    pinned_after = (after.abs() > 0.99).float().mean().item()
    return size, size_after, w_before, w_after, pinned_before, pinned_after

print("scale  run    | grad size -> after clip | weight size before -> after | notes pinned at +-1 before -> after")
for scale in [1, 8]:
    for clip in [False, True]:
        a, b, c, d, e, f = update(scale, clip)
        label = "clipped" if clip else "plain  "
        print(f"  x{scale}  {label} | {a:9.2e} -> {b:9.2e}      | {c:6.2f} -> {d:9.2f}         | {e:.3f} -> {f:.3f}")
```

```text
scale  run    | grad size -> after clip | weight size before -> after | notes pinned at +-1 before -> after
  x1  plain   |  7.22e+00 ->  7.22e+00      |   2.23 ->      2.40         | 0.000 -> 0.000
  x1  clipped |  7.22e+00 ->  5.14e-01      |   2.23 ->      2.24         | 0.000 -> 0.000
  x8  plain   |  8.55e+04 ->  8.55e+04      |  17.87 ->   8548.25         | 0.484 -> 0.997
  x8  clipped |  8.55e+04 ->  8.78e-01      |  17.87 ->     17.87         | 0.484 -> 0.494
```

Reading the columns: *grad size* is the length of the recurrent knobs' gradient before and after clipping (clipping looks at *all* the knobs and allows their total length `1.0`, so `0.878` is the recurrent share); *weight size* is the length of the recurrent weight matrix before and after one update; *notes pinned* is the share of the 40 x 16 notes whose size is above `0.99` (the flat part of `tanh`, the "capped by `tanh`" of Week 8, in numbers).

- [ ] **Run the teacher-only blocks** (paste them *below* the seven, in a copy named `teacher10.py`). `T1` is the typical slope per step and the pinned share; `T2` trains 15 small cells (about 5 seconds); `K1` is the workbook key.

**Block T1 — teacher only: the typical slope per step, and the pinned share**

```python
# TEACHER-ONLY (uses ** (1 / k), a fractional power; the student never sees this): the geometric-mean slope per step.
for scale in [1, 2, 3, 4, 8]:
    row = []
    for T in [10, 20, 40, 80]:
        g = probe(T, scale)
        row.append((g[0] / g[-1]) ** (1 / (T - 1)))
    print(f"scale x{scale}: typical slope per step at T = 10, 20, 40, 80:", ["%.3f" % r for r in row])
print("0.5 ** 40 =", f"{0.5 ** 40:.3e}", "  0.95 ** 400 =", f"{0.95 ** 400:.3e}", "  0.982 ** 40 =", round(0.982 ** 40, 4))
print("1.05 ** 80 =", round(1.05 ** 80, 2), "  0.9526 ** 80 =", round(0.9526 ** 80, 4), "  0.95 ** 80 =", round(0.95 ** 80, 4))

pinned = []
for seed in range(5):
    st = torch.stack(unroll(make_cell(8, seed), torch.randn(40, 4)))
    pinned.append(round((st.abs() > 0.99).float().mean().item(), 3))
print("scale 8, T = 40, share of notes pinned at +-1, seeds 0-4:", pinned)
```

```text
scale x1: typical slope per step at T = 10, 20, 40, 80: ['0.509', '0.508', '0.545', '0.543']
scale x2: typical slope per step at T = 10, 20, 40, 80: ['0.804', '0.749', '0.825', '0.836']
scale x3: typical slope per step at T = 10, 20, 40, 80: ['0.954', '0.895', '0.979', '0.947']
scale x4: typical slope per step at T = 10, 20, 40, 80: ['1.117', '1.057', '1.043', '1.089']
scale x8: typical slope per step at T = 10, 20, 40, 80: ['1.272', '1.244', '1.197', '1.235']
0.5 ** 40 = 9.095e-13   0.95 ** 400 = 1.229e-09   0.982 ** 40 = 0.4836
1.05 ** 80 = 49.56   0.9526 ** 80 = 0.0206   0.95 ** 80 = 0.0165
scale 8, T = 40, share of notes pinned at +-1, seeds 0-4: [0.484, 0.467, 0.495, 0.655, 0.444]
```

`0.95 ** 400 =` `1.229e-09`: the reference module's *original* text said "about `4 x 10^-9`", which was **wrong by a factor of 3**; the patched module now says `1.2 x 10^-9`, the same as ours. `0.982 ** 40 = 0.4836` (the patched module says `0.484`, rounded to three places).

**Block T2 — teacher only: does a tiny gradient at the start mean it cannot learn?**

```python
# TEACHER-ONLY: does a vanishing gradient at the start mean the cell cannot learn? Train nn.RNN to report the SIGN of its FIRST input.
# (Uses binary_cross_entropy_with_logits and Adam; the student never sees this block.)
def first_bit(T, seed=0, steps=300):
    torch.manual_seed(seed)
    rnn = nn.RNN(1, 16, batch_first=True)
    head = nn.Linear(16, 1)
    opt = torch.optim.Adam(list(rnn.parameters()) + list(head.parameters()), lr=1e-2)
    def batch(n):
        x = torch.randn(n, T, 1) * 0.5
        y = (torch.rand(n) > 0.5).float()
        x[:, 0, 0] = y * 2 - 1                    # the first input carries the answer; the rest is noise
        return x, y
    for step in range(steps):
        x, y = batch(64)
        out, h_n = rnn(x)
        loss = nn.functional.binary_cross_entropy_with_logits(head(h_n[0]).squeeze(1), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    x, y = batch(1000)
    with torch.no_grad():
        out, h_n = rnn(x)
    return ((head(h_n[0]).squeeze(1) > 0).float() == y).float().mean().item()

for T in [10, 40, 80]:
    print(f"T = {T:2d}: accuracy on 1000 fresh sequences, seeds 0-4:", [round(first_bit(T, seed), 3) for seed in range(5)])
```

```text
T = 10: accuracy on 1000 fresh sequences, seeds 0-4: [1.0, 1.0, 1.0, 1.0, 1.0]
T = 40: accuracy on 1000 fresh sequences, seeds 0-4: [1.0, 1.0, 1.0, 1.0, 0.503]
T = 80: accuracy on 1000 fresh sequences, seeds 0-4: [0.47, 0.484, 0.5, 0.497, 1.0]
```

Chance is `0.5`. **This block is why the lesson says "the signal is tiny at the start", never "it cannot learn".** Every failure sits at chance (`0.47`-`0.50`); every success at `1.0`.

**Block K1 — teacher only: `key.py`, every workbook answer computed**

```python
# TEACHER-ONLY key.py - Week 10: every hand-arithmetic answer in the workbook, computed.
print("10.1")
for label, rate, k in [("a", 0.9, 10), ("b", 0.9, 20), ("c", 1.1, 10), ("d", 1.1, 20), ("e", 0.99, 40), ("f", 1.01, 40), ("g", 0.95, 40)]:
    print(f"  {label}) {rate} ** {k} = {rate ** k:.4f}")
value, k = 1.0, 0
while value > 0.5:
    value = value * 0.9
    k = k + 1
print(f"  h) 0.9 first below 0.5 after {k} multiplications ({value:.4f})")

print("10.2  the Week 8 cell with W_hh = 1.0, a spike at step 1")
h, notes = 0.0, []
for x in [1.0, 0.0, 0.0, 0.0]:
    h = math.tanh(1.0 * x + 1.0 * h)
    notes.append(round(h, 4))
print("  notes:", notes)
slopes = [1.0 * (1 - h * h) for h in notes[1:]]      # the slope INTO each later note, as in slopes.py
print("  slopes into notes 2, 3, 4:", [round(s, 4) for s in slopes])
print("  note 1 -> note 4:", round(slopes[0] * slopes[1] * slopes[2], 4))
print("  the same three slopes for W_hh = 0.5 were 0.4340, 0.4839, 0.4960 -> 0.1041")
print("extras used in the guide")
value, k = 1.0, 0
while value > 0.5:
    value = value * 0.9991
    k = k + 1
print(f"  0.9991 first below 0.5 after {k} multiplications")
print(f"  0.9 ** 40 = {0.9 ** 40:.4f}   1.1 ** 40 = {1.1 ** 40:.2f}   1.2 ** 40 = {1.2 ** 40:.0f}")
```

```text
10.1
  a) 0.9 ** 10 = 0.3487
  b) 0.9 ** 20 = 0.1216
  c) 1.1 ** 10 = 2.5937
  d) 1.1 ** 20 = 6.7275
  e) 0.99 ** 40 = 0.6690
  f) 1.01 ** 40 = 1.4889
  g) 0.95 ** 40 = 0.1285
  h) 0.9 first below 0.5 after 7 multiplications (0.4783)
10.2  the Week 8 cell with W_hh = 1.0, a spike at step 1
  notes: [0.7616, 0.642, 0.5663, 0.5126]
  slopes into notes 2, 3, 4: [0.5878, 0.6793, 0.7372]
  note 1 -> note 4: 0.2944
  the same three slopes for W_hh = 0.5 were 0.4340, 0.4839, 0.4960 -> 0.1041
extras used in the guide
  0.9991 first below 0.5 after 770 multiplications
  0.9 ** 40 = 0.0148   1.1 ** 40 = 45.26   1.2 ** 40 = 1470
```

- [ ] **Print** workbook pages 10.1-10.6.
- [ ] **Read the Debugging Clinic**, and keep its seven blocks ready to paste under `week10.py` in a scratch file.
- [ ] **Put a calculator on the desk** that has a power key (`x^y`).

### 3 minutes on the day

- [ ] Open `week10.py` as an **empty file** for typing.
- [ ] Calculator, timer and workbook pages on the desk.

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Block 1 needs only Python; pages 10.1 and 10.2 need only paper and the calculator. Run the rest from the printed outputs and say so. |
| `NameError: name 'probe' is not defined` (or `unroll`, `make_cell`) | The earlier block was not pasted above. The seven blocks are one file. |
| `RuntimeError: can't retain_grad on Tensor that has requires_grad=False` | Clinic 1: the weights were copied with `.data` inside `unroll`. Use `rnn.weight_ih_l0` directly. |
| A table differs in the second digit | Different PyTorch build or CPU. Compare the **orders of magnitude** (`e-10`, `e+07`) and the shape (falls; falls slowly; level then climbs; climbs). Use the number on your screen. |
| Block 5 is slow | It is not (a fraction of a second). Over 10 seconds means `torch.set_num_threads(1)` is missing from block 2. |
| No laptop at all | Do pages 10.1 and 10.2 with the calculator and read the grid (section 6) from this guide as "data from my laptop at home". Say so out loud. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the running order of the lesson, with what to say, ask and watch for in each segment.

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 8 | The Forty-Person Telephone: guess, then compound it on the calculator |
| 🧠 Concept & maths | 14 | Backwards through the loop; the slopes of last week's own notes; tiny and huge; why there is no comfortable middle |
| 💻 Live-code | 20 | Blocks 1-4 (compound, slopes, parked cell, the probe) |
| 🎲 Their turn | 23 | Predict then print the 4 by 4 grid; five seeds; one explosion, with and without clipping |
| 🔑 Wrap & assign | 5 | What was shown, what was not; the homework |

### 🪝 Hook — The Forty-Person Telephone (8 minutes)

**(2 min) The question.** Say: *"Forty people stand in a line. The first whispers a message to the second. Each person is a little forgetful: each passes on 95% of what they heard and loses 5%. How much of the original message reaches the fortieth person?"* **Write the guess on a card first**, with a number: *"half? a third? nine tenths?"* Most guess 50% to 80%. Keep the card.

**(3 min) The calculator.** Hand it over: *"Press 1, then times 0.95, forty times. Say the number out loud at 5, 10, 20, 40."* (Or `0.95 ^ 40`.) They get `0.7738, 0.5987, 0.3585, 0.1285`. The message is **13%** of itself. **Do not explain.** Ask: *"How did that happen from a 5% loss?"* (Wait. The answer they reach is "it keeps losing 5% *of what is left*". That is compounding. Write the word on the board.)

**(3 min) And the other way.** *"The same line, but each person adds a little: passes on 105% of what they heard."* They predict; they press; `1.05 ** 40 = 7.04`. *"A one-in-twenty bump, seven times as loud."* Write the numbers in a column on the board: **below 1: tiny. Above 1: huge.** *"The only number that stays the same is exactly 1."* (If they push back that real cells are not exactly one number, good: that is the point of the next 60 minutes.)

**Bridge:** *"Last week your note faded: 0.7616, 0.3634, 0.1797, 0.0896. Today's question is what that fading does to **learning**. Learning sends an error backwards through that loop. What does the backwards trip look like?"*

### 🧠 Concept & Maths — Slopes That Multiply (14 minutes)

**(3 min) Backwards through the loop.** On the board, draw last week's unrolled cell as four boxes with arrows going **right** (forward): note 1, note 2, note 3, note 4. Now draw the error arrow going **left**, from the last note. Say: *"To learn, the last note has to ask 'how much did note 1 matter to me?'. That is a slope. We did this with chains of layers in Week 6: slopes multiply along a chain. A loop, unrolled, **is** a chain, with the same layer repeated."* Name it once: **backpropagation through time** ("backprop through the unrolled loop; 'time' just means the steps of the sentence"). Add the word **position**: *"position 1 is the first word, position 41 the forty-first."*

**(4 min) The slopes of last week's notes.** Ask: *"How much does note 2 move if I nudge note 1?"* They know how to find out (nudge, divide). Run block 2 live, or do one by hand: `0.5 x (1 - 0.3634 squared) = 0.4340`. Then the other two (`0.4839`, `0.4960`). *"Note 1 to note 4 is three steps, so three slopes multiplied: what?"* They do it: **0.1041**. *"Three steps back, a tenth of the signal is left. What about forty?"* Let them guess; then `0.5 ** 40` on the calculator: `9.1e-13`. *"A millionth of a millionth."*

**(3 min) The word for it.** Write the Week 6 words and make them say them: **vanishing gradient** (they have it: the error reaching the first layers is tiny). Then the new word, the opposite: **exploding gradient** (the same product with slopes above 1, a huge number). Link to the Hook column: **below 1: vanishing; above 1: exploding.**

**(4 min) Why there is no reliable comfortable middle.** Say: *"For the product to stay near 1, every slope would have to be within a hair of 1, forty times. Check how little a hair is."* They compute `0.99 ** 40 = 0.669` and `1.01 ** 40 = 1.489` (workbook 10.1 e and f; let them do it now). *"A hair either side of 1 and in forty steps you have moved by a third or a half. A real cell does not have forty slopes all equal and all near 1. What do you think the real table looks like?"* Do not answer. They see it in twenty-five minutes.

> **Check for understanding (do not skip).** *"If every slope is 0.9, what is left after 7 steps?"* (`0.4783`, under half.) *"After 20?"* (`0.1216`.) *"If every slope is 1.1, after 20?"* (`6.7275`.) If they get the direction right and the size wrong, fine; if they get the direction wrong, repeat the Hook column.

### 💻 Live-Code Together — blocks 1-4 (20 minutes)

The student types; you narrate **after** they have predicted. Keep `week10.py` open and add each block under the last.

1. **Block 1 (3 min)**: the compounding table. Predict one cell before running (`0.9526 ** 10`?). Ask *"why did we write `value = value * rate` instead of `**`?"* (So you can *see* the multiplication happen.)
2. **Block 2 (3 min)**: the slopes of last week's notes. They have done these by hand; the code prints the same three numbers and the product `0.1041`. Point at the nudge check: *"two ways to the same number; that is why we trust the shortcut."*
3. **Block 3 (6 min)**: the parked cell. Say: *"We cheat to make a case where every slope is the same: a cell that sits still at 0.2177. Its slope is 0.9526 at **every** step. If our theory is right, the gradient at position 1 should be 0.9526 forty times over. Prediction first: what is it?"* (`0.1434`.) Then introduce **`h.retain_grad()`** (section 4a): *"normally PyTorch throws away the gradient of in-between values. This line says keep this one."* Run. They see `0.1447` against `0.1434` and the column of gradients beside `0.9526 ** k`. *"Theory and machine agree to two places; the rest is the note drifting."*
4. **Block 4 (8 min)**: the probe. Introduce **`torch.randn`** (4c) and **`torch.stack`** (4b) as they come up. Make them say the shapes aloud: `x` is `(T, 4)`, `states` is `(T, 16)`, `grads` is `(T, 16)`. Run, and read the five lines together: *"position 40 is 4.0. Position 30 is five thousandths. Position 1: `2e-10`."* **Pause.** *"That is ten orders of magnitude lost across 40 steps, with no cheating this time."* Ask: *"vanishing or exploding?"*

### 🎲 Their Turn — The Forty-Multiplications Grid (23 minutes)

**(2 min) The task.** Show the empty grid on workbook page 10.4: rows = scale `1, 2, 4, 8`; columns = `T = 10, 20, 40, 80`. Say: *"Scale is how much I multiply the recurrent weights by. Before you run anything, put a V (vanishing, below 0.001), L (level, between 0.001 and 10) or E (exploding, above 10) in every one of the 16 cells. I will not tell you if you are right."* They will write **V** down scale 1 and **E** down scale 8 and guess the middle. **Do not correct predictions.**

**(5 min) Print it.** They run block 5 and compare. By those cut-offs the grid reads: scale 1: L, V, V, V (the `9.15e-03` is above `0.001`); scale 2: L, L, L, V; scale 4: E, E, E, E (even `T = 10` gives `10.8`); scale 8: E in all four. **Some predictions will "miss" only because of our cut-offs.** Say: *"Good. What does that tell us about the cut-offs?"* (They are ours, not nature's. Read the **trend** down each row: falls; falls slowly; level-ish then up; up.) One sentence per row on page 10.4.

**(3 min) Is it the seed?** Run block 6. At scale 1: all five tiny (`1.9e-14` to `4.7e-09`). At scale 8: four huge, one tiny. Ask: *"Which seed broke the rule? What would you print to find out why?"* (A student who suggests counting how many notes are stuck at +-1 has just proposed `T1`'s check: praise it. We did not test it in the lesson; say that the teacher check found seed 3 had the most pinned notes.)

**(10 min) Force an explosion.** Say: *"We can see the size of the signal. Now what happens if we **act** on a huge one? One step, learning rate 0.1."* They read block 7 **before** running it: what do the columns mean? Predict: *"at scale 8, what happens to the size of the weight matrix after one update, with and without clipping?"* They run it. Read the two scale-8 rows aloud together: `17.87` to **`8548.25`** against `17.87` to `17.87`. *"One update multiplied the size of the weights by almost 500."* Then the last column: pinned `0.484` to `0.997` (stuck at +-1 almost everywhere) against `0.484` to `0.494`.

**Say the second half, the one students miss:** *"Look at the clipped row. The weights were not wrecked. But about half the notes were already stuck at plus or minus 1 **before** the update. Did clipping fix that?"* (No.) *"What did it fix?"* (One update; it cannot throw the weights across the room.) Then scale 1: *"the gradient there was `7.22`, a healthy size, and clipping shrank it to `0.514`. Is that good?"* (Not obviously: at `max_norm = 1.0` it also throttles a gradient that was fine.) **"A seatbelt, not an engine."** Write it on the board.

**(3 min) The question that makes the activity.** Ask: *"Our table says the signal from position 1 is `2e-10` at scale 1. Clipping scales everything by one number. Can clipping ever bring that `2e-10` back?"* They should say no, and why: *"it multiplies everything by the same number, so position 1 stays about twenty billion times smaller than position 40"* (`4.0 / 2.06e-10` is about `1.9e10`; do not insist on the figure). If they say only "no", ask for the *why*.

### 🔑 Wrap & Assign (5 minutes)

**(3 min) Three sentences.** The student says, from memory, in their own words: *(1) what compounding is, (2) why a loop makes it matter, (3) what clipping does and does not do.* Write nothing for them. If they cannot do (2), redraw the four boxes with the arrows going left and ask *"how many slopes between the last note and the first?"*

**(2 min) What we did not do, said out loud.** *"We measured a random cell at the start. We did not train it. We did not show that a trained cell cannot remember. Next week: gates, which make a memory that adds instead of multiplies, and we measure the same table again."* Hand out the homework.

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code, in a copy of the shared session. **Paths and the line numbers inside `week10.py` depend on how the blocks were pasted.** Each mistake is deliberate: you plant it, the student reads the traceback aloud, and you refuse to fix it until they have said what the last line means. Five are loud; **two are silent**, and the silent ones teach more.

### How to teach debugging without giving the answer

1. *"Read me the last line."*
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the Week 8 habit: `.data` switches tracking off (loud)

```python
# DELIBERATE MISTAKE 1: the weights were copied the Week 8 way (.data), which switches tracking off.
def unroll_bad(rnn, x):
    W_ih, W_hh = rnn.weight_ih_l0.data, rnn.weight_hh_l0.data
    b = rnn.bias_ih_l0.data + rnn.bias_hh_l0.data
    h = torch.zeros(W_hh.shape[0])
    hs = []
    for t in range(len(x)):
        h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
        h.retain_grad()
        hs.append(h)
    return hs

hs = unroll_bad(make_cell(), torch.randn(5, 4))
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad1.py", line 13, in <module>
    hs = unroll_bad(make_cell(), torch.randn(5, 4))
  File "/home/you/l4/bad1.py", line 9, in unroll_bad
    h.retain_grad()
RuntimeError: can't retain_grad on Tensor that has requires_grad=False
```

**Read it:** `retain_grad` only works on a value PyTorch is **tracking**. Week 8's `loop.py` copied the weights with `.data`, which makes an *untracked copy*, so `h` has no history to keep a gradient for. **Fix:** use `rnn.weight_ih_l0` and `rnn.weight_hh_l0` directly. `.data` is fine for *setting* a weight (Week 8) and wrong for *using* it in a calculation you want gradients through.

### Mistake 2 — forgetting `retain_grad` (loud, with a warning first)

The first thing the student sees is a **warning**. Have them read it aloud; it names the fix:

```text
bad2.py:14: UserWarning: The .grad attribute of a Tensor that is not a leaf Tensor is being accessed. Its .grad attribute won't be ...
```

then the traceback:

```python
# DELIBERATE MISTAKE 2: the line h.retain_grad() was left out.
def unroll_forgot(rnn, x):
    W_ih, W_hh = rnn.weight_ih_l0, rnn.weight_hh_l0
    b = rnn.bias_ih_l0 + rnn.bias_hh_l0
    h = torch.zeros(W_hh.shape[0])
    hs = []
    for t in range(len(x)):
        h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
        hs.append(h)
    return hs

hs = unroll_forgot(make_cell(), torch.randn(5, 4))
torch.stack(hs)[-1].sum().backward()
grads = torch.stack([h.grad for h in hs])
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 14, in <module>
    grads = torch.stack([h.grad for h in hs])
TypeError: expected Tensor as element 0 in argument 0, but got NoneType
```

**Read it:** `h.grad` is `None` for an in-between value unless `retain_grad()` asked PyTorch to keep it, so the list holds `None` and `torch.stack` refuses a `NoneType`. **Fix:** put `h.retain_grad()` back, **before** `backward()`. Ask first: *"what does the warning say to use?"* (`.retain_grad()`.) The warning is the actual teacher.

### Mistake 3 — `torch.stack` takes one list (loud)

```python
# DELIBERATE MISTAKE 3: torch.stack wants ONE list of tensors, not the tensors one after another.
a = torch.tensor([1.0, 2.0])
b = torch.tensor([3.0, 4.0])
both = torch.stack(a, b)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 4, in <module>
    both = torch.stack(a, b)
TypeError: stack(): argument 'tensors' (position 1) must be tuple of Tensors, not Tensor
```

**Read it:** "must be tuple of Tensors, not Tensor": the first thing given was a single tensor, not a *list* of them. **Fix:** `torch.stack([a, b])`, with the square brackets.

### Mistake 4 — `randn(5)` is five numbers, not five inputs (loud)

```python
# DELIBERATE MISTAKE 4: torch.randn(T) is T numbers, not T inputs of 4 features each.
x = torch.randn(5)
hs = unroll(make_cell(), x)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad4.py", line 3, in <module>
    hs = unroll(make_cell(), x)
  File "/home/you/l4/week10.py", line 70, in unroll
    h = torch.tanh(W_ih @ x[t] + W_hh @ h + b)
RuntimeError: both arguments to matmul need to be at least 1D, but they are 2D and 0D
```

**Read it:** the cell expects each `x[t]` to be four numbers; with `randn(5)`, `x[t]` is a *single number* (the "0D" in the message), so the matrix product has nothing to multiply. **Fix:** `torch.randn(5, 4)`. Have the student **say the shape aloud before pressing Enter**; this is why.

### Mistake 5 — calling `backward()` twice (loud)

```python
# DELIBERATE MISTAKE 5: backward() called twice on the same unrolled loop.
rnn = make_cell()
hs = unroll(rnn, torch.randn(6, 4))
states = torch.stack(hs)
states[-1].sum().backward()
states[-1].sum().backward()
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad5.py", line 6, in <module>
    states[-1].sum().backward()
  ... frames inside torch (elided) ...
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.
```

**Read it:** after the first `backward()` PyTorch **frees** what it saved for it. **Fix:** rebuild the unrolled loop and the stack before another `backward()`, which is what `probe` does at every call. (The message offers `retain_graph=True`; do not teach it. The right habit is a fresh forward pass.)

### Mistake 6 — clipping *before* `backward()` (SILENT)

```python
# DELIBERATE MISTAKE 6 (SILENT): clip_grad_norm_ called BEFORE backward(). No error. Nothing is clipped.
rnn = make_cell(8.0)
x = torch.randn(40, 4)
states = torch.stack(unroll(rnn, x))
size = nn.utils.clip_grad_norm_(rnn.parameters(), max_norm=1.0)
print("clip_grad_norm_ returned:", size.item())
states[-1].sum().backward()
print("recurrent gradient size after the 'clip':", f"{rnn.weight_hh_l0.grad.norm().item():.3e}")
```

```text
clip_grad_norm_ returned: 0.0
recurrent gradient size after the 'clip': 8.548e+04
```

**Read it:** there is **no error**. When `clip_grad_norm_` runs there is no gradient yet, so it has nothing to clip: it returns `0.0` and does nothing; then `backward()` fills in the gradient at its full size, `8.5e+04`. The code *looks* protected, and the printed `0.0` looks like a tiny gradient. **Fix:** `backward()` first, **then** `clip_grad_norm_`, **then** `opt.step()`. Ask *"what should the returned number have been?"* (The size *before* clipping, about `8.5e+04`; `0.0` is the tell.)

### Mistake 7 — the loss taken from the first note (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): the loss was taken from the FIRST note, not the last.
rnn = make_cell(1.0)
hs = unroll(rnn, torch.randn(40, 4))
states = torch.stack(hs)
states[0].sum().backward()
grads = torch.stack([h.grad for h in hs])
print("position 1 gradient:", [round(r.norm().item(), 2) for r in grads][:1])
print("positions 2..5     :", [round(r.norm().item(), 2) for r in grads][1:5])
```

```text
position 1 gradient: [4.0]
positions 2..5     : [0.0, 0.0, 0.0, 0.0]
```

**Read it:** no error, and a printed `4.0`: "the gradient at position 1 is 4.0, it never vanished!" But the loss was taken from the **first** note, so position 1 is where the error *starts* and every later position has gradient zero. **The question being measured was changed by one index.** **Fix:** `states[-1]`, the *last* note. The real-world version of today's lesson: *what is the loss attached to?*

---

## 🎲 The Activity, In Full

This section gives the full setup, rules and expected results for the grid activity, so you can run and check it without the student guide.

### The Forty-Multiplications Grid

**What it is:** a prediction grid and a measurement grid, filled one after the other on workbook page 10.4, plus the with-and-without table on page 10.5. It is the whole experiment in two printed tables.

### Setup (2 minutes, during the live-code segment)

The grid on page 10.4 is blank (4 rows: scale 1, 2, 4, 8; 4 columns: `T` = 10, 20, 40, 80), with a second blank copy beside it for the *measured* values. Two pens of different colours: predictions in one, measurements in the other.

### The rules, read out loud before the first cell

1. **Predict all 16 cells before running anything.** One letter each: **V** (below `0.001`), **L** (between `0.001` and `10`), **E** (above `10`).
2. **Copy each measured number in full, exponent included.** `9.15e-03` is `0.00915`; a dropped exponent changes the answer by a factor of a hundred or more.
3. **Colour in which predictions were right.** The score is not the point; the *pattern* of the misses is.

### The measured grid

The student's second table, so you can check it (the same numbers as section 6, with the letter the cut-offs give):

| scale | T = 10 | T = 20 | T = 40 | T = 80 |
|:--:|:--:|:--:|:--:|:--:|
| x1 | 9.15e-03 (L) | 1.01e-05 (V) | 2.06e-10 (V) | 4.69e-21 (V) |
| x2 | 5.63e-01 (L) | 1.66e-02 (L) | 2.25e-03 (L) | 2.93e-06 (V) |
| x4 | 1.08e+01 (E) | 1.14e+01 (E) | 2.09e+01 (E) | 3.36e+03 (E) |
| x8 | 3.49e+01 (E) | 2.55e+02 (E) | 4.38e+03 (E) | 6.92e+07 (E) |

(`9.15e-03` is **L** because it is above `0.001`, although it is the start of a fall; the whole scale-4 row is **E** because even `T = 10` gives `10.8`. **Both will surprise a student who predicted V and L.** The honest teaching line: *"the cut-offs are ours; the trend down the rows is nature's."* Scale 4 is *E by our rule* but, compared with the others, it is the one row that stays within a factor of two of itself from `T = 10` to `T = 40`.)

### What "finished" looks like

Sixteen predictions written; sixteen measurements copied; one sentence per row; the with-and-without table (10.5) filled; and the student answers the question that makes the activity: *"can clipping bring `2e-10` back?"* with *"no, and here is why"*.

### Variation — a shorter slot (55 minutes)

Do only the `T = 10` and `T = 40` columns, and **skip block 6** (the seeds). Keep block 7 whole.

### Variation — an anxious or slow student

Fill in the V/L/E letters for **scale 1 and scale 8 only** (the obvious rows); they predict the middle two. Say the rule as *"the number gets smaller, or stays, or gets bigger."* For clipping use only the two scale-8 rows and the sentence "clipping stopped the weights from jumping".

### Variation — harder (a student who finishes early)

1. **Find the knife-edge.** *"Scale 3 is between 2 and 4. Run `probe` at `3.0` for several `T`: does it level off, or wander?"* (It wanders: typical slope per step `0.954, 0.895, 0.979, 0.947` for `T` = 10, 20, 40, 80, from `T1`: not stable, not monotone.)
2. **Wider.** *"What does a bigger cell do?"* (`H = 64` instead of 16: they change `make_cell` and report. We did not run this; let them find out and report what they measure.)
3. **Another compounding.** *"Week 5's weight decay multiplied a weight by `0.9991` each step: how many steps until it halves?"* (A loop like block 1's; `K1` prints it: **770**.)

---

## ❓ Questions Students Ask This Week

This section collects the questions you are likely to meet, each with an answer that stays within what today measured.

**"Why `0.9526`? It looks random."** It is. We *chose* a cell that sits still at the note `0.2177`, where the slope is `1 - 0.2177 squared = 0.9526`. It is a designed example so that one slope repeats; the real cell has a different slope at every step.

**"Why is the gradient at the last position `4.0`, not `1`?"** The "loss" is the sum of the 16 numbers of the last note. Each has slope 1 with respect to itself, so the gradient is a list of sixteen `1`s, whose length is `sqrt(16) = 4`. It is a check that the setup is right, not a result.

**"Is `4.69e-21` zero?"** No: it is a very small number that the computer still holds. (We did not test how many steps it takes to reach one it cannot hold; do not give a figure.)

**"Why did seed 3 at scale 8 vanish when the others exploded?"** We do not know for certain. Its notes were pinned at +-1 more often than the other seeds' (`0.655` against `0.444`-`0.495`), and a pinned `tanh` has a slope near zero, which would put a *small* factor in the product. A likely reason; **we did not test it further.**

**"Is this the same cell as last week?"** The same loop, with a note of 16 numbers instead of 1 and weights that are random instead of typed. Block 4's `unroll` is `loop.py` with `retain_grad` added.

**"Why use `nn.RNN` if we write the loop ourselves?"** Only as a source of seeded random weights, so every student's `make_cell(1.0, 0)` is the same cell, and the *scale 1* case is PyTorch's own default.

**"Why does clipping `7.22` down to `0.514` look bad?"** `max_norm = 1.0` is the length allowed for the *whole* gradient (every knob); `0.514` is the recurrent knobs' share of it. At scale 1 the gradient was not a problem, and clipping still shrank it. A real run picks a `max_norm` above the usual size so it only acts on rare spikes; we did not tune one today.

**"So the first words of a sentence are just forgotten?"** Not exactly. Today shows that *at the start of training* the learning signal from the first position is tiny, for the cells we tried. `T2` shows that a trained cell can still learn a first-input task at `T = 40`, most of the time. We do not yet know why.

**"Is this why ChatGPT uses attention?"** Attention was motivated mainly by the fixed-size-summary bottleneck (gates such as the LSTM were the answer to fading gradients), and Week 14 makes that case. Today's measurement is about a plain recurrent cell, not about attention or any chat model.

**"Real models have a loss at every word, not just the last."** Yes, and that is a real difference: with a loss at *every* position, position 1 also gets a short, strong signal from position 2. Our toy loss isolates the long path on purpose. It is one reason a real model can learn *something* about early words despite the table.

**"Can I just make the weights exactly the right size?"** The table says the right size depends on `T`: at scale 3 the typical slope wanders from `0.89` to `0.98`. A setting that is fine at one length is not at another. Gates (Week 11) are a way out that does not depend on a precise setting.

**"Will my numbers match yours?"** The calculator numbers (`0.1434`, `0.1285`, `7.04`, `0.1041`) match exactly. The tables should match on the same machine; on another build the second digit of the small numbers may move. The **orders of magnitude** and the shapes will not.

---

## ⚠️ Where This Lesson Goes Wrong

This section lists the usual failures in this lesson and the quickest way back from each.

1. **The student writes "RNNs forget" or "RNNs cannot remember".** Today measured a random cell's gradient. Ask: *"What did we measure, a trained cell or a random one?"*
2. **A predicted V/L/E is "wrong" only because of our cut-offs.** The `T = 10, x1` cell and the whole scale-4 row are the usual ones. Do not argue the cut-off; point at the trend.
3. **The exponent is dropped.** `2.06e-10` copied as `2.06`. Say it in words: *"two point oh six times ten to the minus ten: how many zeros after the point?"*
4. **The student cannot multiply forty times on a calculator.** Give them `0.95 ^ 40` on the power key, or run block 1. Pressing the key forty times is not the lesson.
5. **The hook's guess is waved away.** A student who says "I knew it would be small" afterwards: show the card with their written guess. The surprise is the lesson; **the card is the evidence**.
6. **Clipping is taught as "the fix".** Return to block 7: the clipped row still has half the notes pinned. *"What did it fix? What did it not?"*
7. **The student re-runs block 7 with a different learning rate "to see what happens"** and finds a combination where both rows look fine. Good science, and a different experiment. Ask what they changed and make them *write it down*; do not let it replace the one in the lesson.
8. **Block 3's `w.grad` accumulates** over repeated runs in one session (it is a knob and nothing clears it). It does not change the gradients printed (those are `h.grad`), but a student who prints `w.grad` after three runs sees it grow. Say: "it adds up each time because we never cleared it".
9. **`T2` mentioned in class as "proof".** It is a teacher check with a different task, one width and one learning rate. Use it only to stop "cannot learn".

---

## 🧭 Differentiation

This section adjusts the lesson for a struggling, a fast or a disengaged student.

### If the student is struggling

- Do **only the three-step version** (block 2): `0.4340 x 0.4839 x 0.4960 = 0.1041`, then `0.5 ** 40` on the calculator. The whole idea in two lines.
- Predict V/L/E for **two rows only** (scale 1 and 8).
- Replace the 16-cell grid with a 2 by 2 (`T` = 10, 40; scale 1, 8): `9.15e-03`, `2.06e-10`, `3.49e+01`, `4.38e+03`.
- For clipping: scale 8 only. The sentence *"the weights did not jump"* is enough.

### If the student is flying

- **`T1`'s typical slope.** Ask *"what single number per step would give the same drop from position 40 to position 1?"* (The ratio to the power `1 / 39`.) That is the inverse of compounding. They work it out with a calculator; do not give the formula.
- **Scale 3.** Run `probe` at `3.0` for several `T` and report whether it levels, with the numbers.
- **Seed 3.** Print how many notes are pinned for each seed and relate it to the vanished one. (`T1` does this; let the student find it first.)
- **Halving a weight.** The `0.9991` question above (**770** steps).

### If the student won't engage today

Play the Telephone with a number they care about (a rumour passed on at 90%; a video that each viewer shares with 1.1 friends). The *hook* is what they need; the code can be block 1 printed and read aloud. **Compute their numbers first** (`0.9 ** 40 = 0.0148`, `1.1 ** 40 = 45.26`, both printed by `K1`) so you can check theirs.

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"What is compounding?"** *Pass:* multiplying by the same number over and over, so a number below 1 shrinks towards zero and above 1 grows without limit. (Not "adding a bit each time".)
2. **"Why does it matter in a loop?"** *Pass:* the error going back is multiplied by one slope per step, so forty steps is forty multiplications.
3. **"Which way does scale 8 go, and why?"** *Pass:* it explodes, because the slopes are above 1. (Bonus: "but not for every seed".)
4. **"What does clipping fix, and what does it not?"** *Pass:* it stops a huge update wrecking the weights; it cannot bring back a signal that has vanished (it multiplies everything by one number).
5. **"Did we show that a trained RNN cannot remember 40 steps?"** *Pass:* no, we measured a random one at the start.

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Predicts the direction of every row before running; computes a halving time unprompted; explains seed 3 as "not every setting explodes", offering a reason and flagging it untested; says what clipping cannot do. |
| **3 — Secure** | Gets the compounding table; fills the grid and reads each row in a sentence; says "tiny below 1, huge above 1"; states clipping's limit. |
| **2 — Developing** | Gets the direction of vanishing; mixes up which of `0.95` and `1.05` explodes; needs help reading the exponent. |
| **1 — Not yet** | Thinks 5% per step is 5% overall. Repeat the Hook with the calculator at the start of Week 11, before gates. |

---

## 📤 Homework to Assign

The workbook has six pages (10.1-10.6). The student does them in order, and **writes predictions before running anything**.

1. **10.1 Compounding by hand** — eight calculator answers and the telephone.
2. **10.2 Slopes in a chain** — last week's cell with `W_hh = 1.0`: three slopes, their product, a comparison with `W_hh = 0.5`.
3. **10.3 The parked cell** — read block 3's output and fill the gradient by position beside `0.9526 ** k`.
4. **10.4 The grid** — the 16 predictions and the 16 measurements, one sentence per row.
5. **10.5 One explosion** — the with-and-without table and the sentence about what clipping does *not* fix.
6. **10.6 The report** — a short paragraph, every number from their own run in the last 24 hours with the seed stated, and the **Bug Log**: any real error they met, with its last line copied and the fix.

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated.

Estimated time: 60-70 minutes.

---

## 🔑 Answer Key

This section is for checking the workbook; it is teacher-only.

> **The workbook pages 10.1-10.6 follow this order.** Where an answer is a number it comes from `key.py` (block `K1`), blocks 1-7 of `week10.py`, or the grid above. All were run in the Prep Checklist.

### Page 10.1 — Compounding by hand (from `key.py`)

| Part | Question | Answer |
|:--:|---|:--:|
| a | `0.9 ** 10` | **0.3487** |
| b | `0.9 ** 20` | **0.1216** |
| c | `1.1 ** 10` | **2.5937** |
| d | `1.1 ** 20` | **6.7275** |
| e | `0.99 ** 40` | **0.6690** |
| f | `1.01 ** 40` | **1.4889** |
| g | The telephone: `0.95 ** 40` | **0.1285** (about 13%) |
| h | How many multiplications by `0.9` until the value is first below one half? | **7** (`0.4783`) |

*What to draw out:* **e and f together**: a hair under 1 and a hair over 1, forty steps, `0.669` and `1.4889`; neither is "about 1". **a and b**: doubling the exponent does not halve the answer; it *squares* it (`0.3487` then `0.1216`). *Common errors:* `0.9 x 10 = 9`; rounding `0.99 ** 40` to `1`; answering `g` as "5% of 40 is 200% lost".

### Page 10.2 — Slopes in a chain (from `key.py`)

The Week 8 cell with `W_hh = 1.0`, `W_xh = 1.0`, spike `[1, 0, 0, 0]`: notes **0.7616, 0.642, 0.5663, 0.5126**. Slope into each later note, `1.0 x (1 - note squared)`:

| Into note | Working | Slope |
|:--:|---|:--:|
| 2 | `1 - 0.642 squared` | **0.5878** |
| 3 | `1 - 0.5663 squared` | **0.6793** |
| 4 | `1 - 0.5126 squared` | **0.7372** |

Product, note 1 to note 4: **0.2944** (the empty boxes of the blank chain, workbook Figure W10.6, hold `0.5878`, `0.6793`, `0.7372` and this product). For `W_hh = 0.5` the three slopes were `0.4340, 0.4839, 0.4960`, product **0.1041**. *Reading:* the bigger recurrent weight loses far less in three steps (`0.2944` against `0.1041`), as Week 8's workbook part g showed (the note fades more slowly). *Common errors:* using the *old* note in `1 - h squared` instead of the new one; forgetting `W_hh` in the slope; rounding each slope to one decimal.

### Page 10.3 — The parked cell (from block 3)

| Position `p` | Measured gradient | `0.9526 ** (41 - p)` |
|:--:|:--:|:--:|
| 41 | 1.0000 | 1.0000 |
| 40 | 0.9529 | 0.9526 |
| 39 | 0.9080 | 0.9074 |
| 31 | 0.6173 | 0.6153 |
| 21 | 0.3809 | 0.3786 |
| 11 | 0.2348 | 0.2330 |
| 1 | 0.1447 | 0.1434 |

*What to draw out:* the two columns agree to two places and drift apart a little as the note drifts from `0.2177` to `0.217`. The sentence: *"the gradient at position `p` is the slope multiplied `41 - p` times"*. *Common error:* reading the exponent as `p`; it is the distance *from the last position*.

### Page 10.4 — The grid

The measured grid is the one in 🎲 (block 5). The model **sentences**, one per row:

- **x1:** falls by a large factor every few steps: `9e-03` at 10, `2e-10` at 40, `5e-21` at 80. Vanishing.
- **x2:** falls, but slower: `0.56` at 10 and `3e-06` at 80. Vanishing, later.
- **x4:** about `10`-`20` up to 40, then `3.4e+03` at 80: neither, then exploding.
- **x8:** rises every time: `35` at 10, `7e+07` at 80. Exploding.

*Marking:* full credit for a sentence that gives the **direction** and **one number copied with its exponent**. **Do not score the V/L/E predictions**; look for a student who changed their mind after seeing the scale-4 row. *The one sentence that must appear somewhere:* "no setting stays level for every `T`".

### Page 10.5 — One explosion (from block 7)

| scale | run | weight size before | after | notes pinned before | after |
|:--:|---|:--:|:--:|:--:|:--:|
| 1 | plain | 2.23 | 2.40 | 0.000 | 0.000 |
| 1 | clipped | 2.23 | 2.24 | 0.000 | 0.000 |
| 8 | plain | 17.87 | **8548.25** | 0.484 | **0.997** |
| 8 | clipped | 17.87 | **17.87** | 0.484 | 0.494 |

The sentence that earns full marks: *"Clipping stopped one update from sending the weights from 18 to 8,500, but about half the notes were already pinned before, and it did not change that; and at scale 1, where nothing was wrong, it still made the step smaller."* **Also accept** "it limits the damage of one huge step but does not cure the cause". *Common error:* "clipping fixed the explosion". The cause is in the weights and the cell; clipping limited this one step.

### Page 10.6 — The report (model answer and rubric)

Model: *"With seed 0 and T = 40, the gradient at position 1 was `2.06e-10` at scale 1 and `4.38e+03` at scale 8 (the last position's was `4.0`). A number below 1 multiplied forty times is almost zero, and above 1 it is huge; clipping only helps with the second. I measured a random cell at the start of training, so this does not show that a trained cell can't remember."*

| Criterion | Marks |
|---|:--:|
| Two numbers **with exponents**, one vanishing and one exploding, from their own run, seed stated | 2 |
| States the cause in one sentence (the same kind of number multiplied many times) | 1 |
| States what clipping does **not** do | 1 |
| States what was **not** shown: an untrained cell, not "RNNs can't remember" | 2 |

A write-up that says "RNNs can't remember long sequences" loses the last two marks regardless of the rest. **Bug Log:** any real entries are fine if the **last line** of the traceback (not the whole) was copied and the fix works.

### Teacher-only: the Clinic, at a glance

| # | Loud / silent | Last line (or tell) | One-line fix |
|:--:|:--:|---|---|
| 1 | loud | `RuntimeError: can't retain_grad on Tensor that has requires_grad=False` | Use the parameters directly, not `.data` |
| 2 | loud, after a warning | `TypeError: expected Tensor as element 0 in argument 0, but got NoneType` | Add `h.retain_grad()` before `backward()` |
| 3 | loud | `TypeError: stack(): argument 'tensors' (position 1) must be tuple of Tensors, not Tensor` | `torch.stack([a, b])` |
| 4 | loud | `RuntimeError: both arguments to matmul need to be at least 1D, but they are 2D and 0D` | `torch.randn(5, 4)` |
| 5 | loud | `RuntimeError: Trying to backward through the graph a second time ...` | A fresh forward pass before each `backward()` |
| 6 | **silent** | `clip_grad_norm_ returned: 0.0` | `backward()` first, then clip |
| 7 | **silent** | position 1 gradient `4.0`, later positions `0.0` | Take the loss from `states[-1]` |

### Answers to every question posed in the lesson

| Question | Answer |
|---|---|
| How much of the message reaches person 40, passing on 95%? | `0.1285`, about 13%. |
| And passing on 105%? | `7.04` times. |
| How did a 5% loss become 87%? | It is 5% of *what is left*, forty times: compounding. |
| Slope of note 2 with respect to note 1 (`W_hh = 0.5`)? | `0.4340`. |
| Note 1 to note 4, three slopes multiplied? | `0.1041`, about a tenth. |
| `0.5 ** 40`? | `9.1e-13`. |
| Below 1: vanishing or exploding? Above 1? | Vanishing; exploding. |
| `0.99 ** 40`? `1.01 ** 40`? | `0.669`; `1.489`. |
| Every slope 0.9: what is left after 7 steps? After 20? | `0.4783` (under half); `0.1216`. |
| Every slope 1.1, after 20 steps? | `6.7275`. |
| Why `value = value * rate` instead of `**` in block 1? | So the multiplication can be seen happening. |
| What is the gradient at position 1 of the parked cell? | About `0.14` (`0.9526 ** 40`; measured `0.1447`). |
| Block 4's output: vanishing or exploding? | Vanishing (`2e-10` against `4`). |
| Shapes of `x`, `states`, `grads` in block 4? | `(T, 4)`, `(T, 16)`, `(T, 16)`. |
| Which seed broke the rule at scale 8? | Seed 3 (`5.5e-07`). |
| The weight matrix after one unclipped update at scale 8? | Size `17.87` to `8548.25`. |
| Did clipping fix the cell? | No: it stopped the weights jumping; half the notes were already pinned. |
| Can clipping bring back `2e-10`? | No: it multiplies everything by one number. |
| What did we **not** do today? | Train a cell properly, or show that a trained one cannot remember. |

---

## 🔮 Next Week Preview

This section shows how next week builds on today, so you know what to carry over.

**Week 11 — Gates: Memory That Adds Instead of Multiplies** (🟦 teach). Today's cure for the *huge* side was a seatbelt; the *tiny* side needs a different design. An LSTM updates its memory by **adding**, so the slope back through it is the **forget gate**: a gate near 1 is Week 6's residual highway, written as a loop. The student codes an LSTM cell from scratch, checks it against `nn.LSTMCell`, compares RNN, GRU and LSTM over three seeds, and runs the forget-bias 0 against 2 probe. No new maths idea. Three new constructs: `nn.LSTMCell`, `nn.LSTM` / `nn.GRU`, and in-place `fill_()` on a bias slice.

**What from today carries over:** the `probe` idea (*the thing to measure is the gradient at position 1*), the grid on page 10.4 as the baseline Week 11 compares against, and the sentence **"a seatbelt, not an engine"**. **If the grid on page 10.4 is blank, do it before Week 11.**
