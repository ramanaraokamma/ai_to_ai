# Week 11 — Gates: Memory That Adds Instead of Multiplies

[⬅ Week 10](week-10.md) · [Course Home](../README.md) · [Week 12 ➡](week-12.md) · [Student Guide](../student-guide/week-11.md) · [Workbook](../workbook/week-11.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~60-70 min) |
| **Type** | 🟦 Teach — the student builds one LSTM step out of `@`, slices and `torch.sigmoid`, checks it against PyTorch's own, *measures* why its memory track behaves like Week 6's residual highway, and then turns one dial (the forget bias) and watches a table change by seven orders of magnitude |
| **Big idea** | Last week the error going back through a loop was multiplied by one slope per step, and forty slopes below 1 left nothing. An LSTM keeps a second track, the **memory** `c`, and updates it by **adding**: `c = f * c_old + i * g`. The slope back through that track is **`f`**, the forget gate, a dial between 0 and 1. **A dial near 1 is Week 6's `x + f(x)` highway, written as a loop. A dial near one half is Week 10's disease all over again** — and at the start of training the dial *is* near one half. |
| **New vocabulary** | **gate** (a dial between 0 and 1 that multiplies something) · **cell state** / memory track (`c`) · **forget gate** · **input gate** · **output gate** · **candidate** · **GRU** · **forget bias** (the number that sets the forget dial before any training). (**Sigmoid**, **running average**, **residual** and **vanishing gradient** are *already theirs*: Level 3 Week 13, Week 2, Week 6, Week 10. Say so, and use them.) |
| **New maths** | *(none)*. Three old ideas return and are **used, not re-taught**: the sigmoid squasher, compounding (`f ** 40`, Week 10) and the slope of a sum (Week 6). See the 🔢 section. |
| **New syntax** | `nn.LSTMCell` · `nn.LSTM` / `nn.GRU` · `tensor.fill_(x)` (in place, on a whole tensor and on a bias slice, under `no_grad`). Three, under the ladder maximum of four. |
| **Dataset** | None. The inputs are **seeded random numbers** (`torch.randn`), as in Week 10. **Nothing downloads. No internet.** |
| **Model** | **Real PyTorch**, **untrained**: a hand-written LSTM step, `nn.LSTMCell`, `nn.RNN`, `nn.GRU` and `nn.LSTM` of 16 numbers of memory, all at seeded random weights. There is **no language model and no stand-in** in the student's lesson. **Nothing is trained by the student today.** (Teacher-only block `T2` trains 55 small layers on a toy task to check what the probe does and does not predict.) |
| **Materials** | Laptop with Python 3 and torch (nothing new to install) · a calculator with a power key and an `e^x` key (a phone in calculator mode is fine; **airplane mode on**) · workbook pages 11.1-11.6 · a timer. Nothing imports `l4lib` today. |
| **Prep time** | 25 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | The student's whole file (`week11.py`, seven blocks) runs in **about 1 second** (nearly all of it is importing torch). The teacher-only blocks add about **55 seconds** (`T2` is 55 short trainings). Anything over **2 minutes** means something is wrong (see Fallback). |

> **⚠️ Watch out:** the thing that goes wrong this week is **"the LSTM fixes vanishing gradients"** said as a fact. It is not what the numbers show. At default settings the LSTM and GRU rows of today's table are **just as tiny as the RNN's** (`2e-09` and `1e-08` against `2e-10` at `T = 40`). The gates only help once the forget dial is **set near 1 on purpose** (bias 2: `5.8e-02`). Even then (teacher-only `T2`) a healthy-looking number did **not** mean the layer could learn at `T = 80`. The second thing that goes wrong is reading today as a result about language models or names: nothing today is trained, and Week 12 is where a gated cell meets real text.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say what a gate is**: "a dial between 0 and 1, made by a sigmoid, that multiplies something to decide how much of it gets through".
2. **Say why the memory track survives**: "`c = f * c_old + i * g` *adds*; the slope back to `c_old` is `f`, so a dial near 1 is a highway and a dial near one half is the old disease".
3. **Write one LSTM step** with `@`, slices and `torch.sigmoid`/`torch.tanh`, and show it agrees with `nn.LSTMCell` to float rounding.
4. **Measure it**: print how much the end of a sequence cares about the first word, for RNN, GRU and LSTM, at `T` = 10, 20, 40, 80, over 3 seeds, and read the table honestly (at default settings all three vanish).
5. **Turn the forget dial** (`fill_` on the bias slice), predict the direction, and say in one sentence what it changed and what it did **not** show (nothing was trained).

Observable evidence: the hand table on workbook page 11.2, the `nn.LSTMCell` check on 11.3, the filled grid on 11.4, the seed and dial table on 11.5, and a short report on 11.6 in which **every number was printed by the student's own run**.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** (the seven student blocks, the teacher-only blocks `T1`, `T2`, `T3` and `K1`) and in the **🐞 Debugging Clinic** was run, in order, in **one shared session** on a CPU with one thread and the seeds shown. The seven student blocks are the pieces of **one file, `week11.py`**, pasted one under the other with no gap: each later block uses names defined by an earlier one. The Clinic blocks are *deliberate mistakes*, each marked, each run in a copy of the session as it stood after block 7; their tracebacks are real. **Timing never appears in the outputs; every number repeated exactly on a second full run on the same machine** (torch `2.2.1`, Python 3.10). A different CPU or PyTorch build can move the last digit, and for a quantity like `2.05e-09` the *second* digit; the orders of magnitude and the shape of every table do not move. Tracebacks show `/home/you/l4/...` for the path, and the long middle of a torch traceback is replaced by `... frames inside torch (elided) ...`; **the last line is always the real, complete last line.** The *line numbers* in a traceback depend on exactly how the blocks were pasted; the last line does not.

### 1. What the student is doing today, in one paragraph

Last week's lesson ended on a seatbelt and a promise: the *tiny* side needs a different design. Today is the design. They first meet the **dial** on a calculator (the sigmoid turns any score into a number between 0 and 1; a dial of `0.9526` applied forty times leaves `0.143`, a dial of `0.5` leaves `9e-13`). They run **one LSTM unit by hand-code** on Week 8's spike and watch the memory keep 86% of itself over three steps where Week 8's note kept 12%. Then they write **one LSTM step in PyTorch** out of `@` and slices and check it against `nn.LSTMCell`. They show, with the recurrent weights set to zero (`fill_`), that the slope back through the memory track **is** the forget dial. Then the honest part: the dial starts near one half, so at default settings the memory track vanishes too. They turn the dial up by writing `fill_` on the forget slice of the bias, and compare RNN, GRU and LSTM, at four lengths and over three seeds. **Nothing is trained.** Week 12 is where a gated cell meets real text.

### 2. 🔢 The maths you need — taught to you first

**No new idea this week.** Three old ones come back, and the lesson is that they are the *same* three. Do each yourself, with a calculator, before class.

**(a) The dial is the sigmoid they already own** (Level 3 Week 13: a squasher that maps any number to between 0 and 1). From block 1:

| Score `z` | `sigmoid(z)` | that dial multiplied 40 times |
|:--:|:--:|:--:|
| -2 | 0.1192 | 1.126e-37 |
| 0 | 0.5000 | 9.095e-13 |
| 1 | 0.7311 | 3.615e-06 |
| 2 | 0.8808 | 6.238e-03 |
| 3 | 0.9526 | 0.1432 |
| 4 | 0.9820 | 0.4838 |

Read the **shape**: a score of 0 (which is roughly what an untrained gate's score is) gives a dial of exactly one half, and one half forty times is `9e-13`, the number from Week 10's `0.5 ** 40`. To keep even half of a message over forty steps the dial must be at `0.9828` (`0.5 ** (1 / 40)`, teacher-only; the student finds it between `0.98` and `0.99` by trial in the Hook). **The dial has to be very close to 1, and sigmoid only gets close to 1 for a large positive score.** That is why a bias of 2 or 4 matters.

**(b) The slope of a sum (Week 6).** Week 6's residual: `x + f(x)` has slope `1 + f'(x)` with respect to `x`, so the path through the `+` has slope exactly 1 before anything else is added. The memory update is `c = f * c_old + i * g`. With respect to `c_old` the first term has slope `f` (a dial times `c_old`), and the second term does not contain `c_old` at all, if the dials only look at the input. So **the slope back one step is `f`**. In the real cell the dials *also* read the old note `h`, and `h` was made from `c_old`, so there are extra, smaller paths; block 4 kills them by setting the recurrent weights to zero and shows the slope **is** `f` to about `6e-08`. **Say that limit out loud**: it is exact for the stripped-down cell; for a real cell it is the main path, and we did not measure how much the extra paths add.

**(c) Compounding (Week 10).** The slope back `k` steps along the memory track is a product of `k` dials. If they are all `f`, it is `f ** k`: the table above. With `f = 0.9526` and `k = 40` it is `0.1432` (Week 10's `0.9526 ** 40 = 0.1434` is the same number; the small gap is rounding `0.95257` to `0.9526`). Week 10's parked cell got the same `0.9526` from `1 - 0.2177 ** 2`; **that was a coincidence of the number we picked, not a connection** — do not let the student link them.

**(d) The GRU is Week 2's running average with a dial.** PyTorch's GRU writes `new note = z * old note + (1 - z) * candidate` (`T1` checks which way `z` points: with its bias at `+10` and everything else zero, an old note of `0.5` stays `0.5`; at `-10` it becomes `0.0`). `z` and `1 - z` add to 1, so this is exactly Week 2's `average = keep * old + (1 - keep) * new`, with `keep` chosen by the network at every step. The LSTM's `f` and `i` are two separate dials that need **not** add to 1, so the LSTM is a looser cousin, not an exact running average.

> **🚫 What you must NOT do with the maths.** (1) **Do not write "derivative", "Jacobian", "eigenvalue" or "chain rule".** "The slope back through the memory track" is the whole phrase. (2) **Do not derive `dc/dc_old = f` with the product rule on the board.** The student has the two facts they need ("slope of a sum", "a dial times something has slope the dial") and block 4 is the evidence. (3) **Do not say "the gradient is exactly `f`" about a real cell.** It is exact only in block 4's stripped-down cell. (4) **Do not take logarithms to find the dial that keeps half.** The student finds `0.983` by trial; `0.5 ** (1 / 40)` is teacher-only and the student has not met a fractional power.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Status |
|---|---|
| Every number in the Hook and Concept tables | **Real arithmetic**, printed by blocks 1 and 2 and by `K1`. |
| The hand-coded unit of block 2 | **Designed**: the gate scores (`3.0`, `5x - 2.5`, `2x`, `1.0`) are chosen by hand so each dial is simple. It is the reference module's worked example; the module's rounding differs by one in the fourth place (`0.8908` against our `0.8909`) because it multiplies rounded numbers. |
| `lstm_step` (block 3) | **Real** LSTM arithmetic, checked against `nn.LSTMCell`. The weights are PyTorch's own seeded random ones, **untrained**. |
| The "loss" (`h.sum()` of the last note; `out[-1].sum()`) | **A toy.** One number made from the last output. A real model has a loss at every position. |
| "Pull of the first word as a fraction of the pull of the last" | **Ours.** `x.grad` is the gradient on the *input* at each position, from `out[-1].sum()`; the ratio is first position over last. It works for all three layers with no `retain_grad`, which is why we use it. **It is not Week 10's number**: Week 10 measured the gradient on the *note* `h`, with a differently-drawn random input (see the comparison below). |
| The forget bias `0`, `1`, `2`, `4` | **Ours.** A number we write into the bias before any training. Not something found in a trained model. |
| Teacher-only `T2` | **Real** training of 1-layer `nn.RNN`/`nn.GRU`/`nn.LSTM` of 16 units, 300 Adam steps (one line, 1000), on a toy task invented for this check ("report the sign of your first input"). **A stand-in task, not a model, and not in the student's lesson.** |
| Any language model, scripted client or `FakeClient` | **Not present.** |

> **🚫 What you must NOT claim about today's numbers.**
> 1. **"LSTMs fix vanishing gradients."** At default settings, `T = 40`, seeds 0-2: RNN `2.0e-10, 6.3e-11, 3.1e-10`; GRU `1.4e-08, 1.5e-09, 8.9e-10`; LSTM `2.0e-09, 7.1e-08, 6.8e-09`. All three are *tiny*; the gates buy one to two orders of magnitude, not the seven the dial buys. What fixes it is the dial **near 1**: forget bias 2 gives `5.8e-02, 1.3e-01, 2.2e-01`. The honest sentence: **"an LSTM has a highway; whether the highway is open at the start depends on where the dial is set."**
> 2. **"The dial setting is what made it learn."** Nothing is trained in the lesson. `T2` trains layers to report the sign of their first input: at `T = 40` the forget-bias-2 LSTM gets it on **5 of 5 seeds** (`0.993`-`0.999`), the default LSTM and GRU on **0 of 5** (all near `0.5`, chance), **and the plain RNN on 4 of 5** (`T2` reproduces Week 10's `T2` numbers exactly). So the dial helped against the default LSTM; it did **not** beat the RNN, and we did not explain why the default LSTM and GRU do worse than the RNN at this task.
> 3. **"A healthy ratio means it can learn."** At `T = 80` the forget-bias-2 LSTM's ratio is `3.4e-02` in block 7 (healthy) and `T2` gets **0 of 5** seeds (chance), and with 1000 steps instead of 300 still **0 of 5**. Forget bias 4 got one seed of five. **A healthy probe at the start is not a guarantee.** We did not find out why; say "I do not know yet".
> 4. **"The GRU has a forget gate."** It has an *update* gate `z`, and in PyTorch it points the **keep** way (`T1`). The reference module writes the GRU with `z` pointing the **replace** way (its `h = (1 - z) * old + z * new`). Do not let the student copy the module's equation into code; it is the opposite convention to the one they will run.
> 5. **Comparing with the reference module's table.** It reports `1.60e-02` for "LSTM, forget bias +2" on a 96-unit character model with an embedding; ours is a 16-unit layer on random numbers. The *direction* agrees (a large gain from bias 2); **the numbers must not be set side by side.**

**The comparison with Week 10's page 10.4** (Week 10 promised the student this). Week 10's scale-1 row is the gradient on the *note* at position 1, and the last position's was always `4.0`, so dividing by `4.0` gives a comparable ratio (arithmetic on Week 10's printed numbers; not a new run):

| | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| Week 10, scale 1, position 1 / `4.0` | 2.29e-03 | 2.53e-06 | 5.15e-11 | 1.17e-21 |
| Today's RNN row, first word / last word (block 6) | 6.72e-03 | 1.77e-05 | 1.99e-10 | 6.48e-20 |

Same shape: a huge fall at every step along the row; the numbers differ by a factor of 3 to 55 because one measures the note and the other the word (one step earlier), and the random inputs are different draws. **Say "same disease, measured a step earlier"**, never "the same number".

### 4. The three new constructs, for somebody who has never seen them

**(a) `nn.LSTMCell(D, H)` — one LSTM step, as an object.** (The snippets in this section are excerpts of blocks 3 and 6, shown for reading, not blocks to run.)

```text
cell = nn.LSTMCell(4, 16)                  # 4 numbers in, 16 numbers of memory
h, c = cell(x_t, (h, c))                   # ONE step: the state goes in as a PAIR and comes out as a PAIR
```

Read as: *"an RNN keeps one thing between steps, the note `h`. An LSTM keeps two, the note `h` and the memory track `c`, so the state is a **pair** `(h, c)`."* Its numbers are four stacked groups of 16: `weight_ih` has shape `(64, 4)`, `weight_hh` `(64, 16)`, and the biases 64 each. The groups are in the order **input, forget, candidate, output** (`i, f, g, o`); block 3's slices `z[0:16]`, `z[16:32]`, `z[32:48]`, `z[48:64]` rely on that, and the check against `nn.LSTMCell` is what tests it (a wrong order would not agree). The two commonest errors are Clinic 1 (handing over `h` alone) and Clinic 5 (filling the wrong group).

**(b) `nn.LSTM(D, H)` / `nn.GRU(D, H)` — the whole-sequence layers.** They do the loop for you, like `nn.RNN` in Week 8.

```text
out, last = layer(x)                       # x: (T, 4) for one sequence; out: (T, 16), the note at every step
```

Read as: *"give it the whole sequence; it runs the cell T times and hands back every note."* `nn.GRU` and `nn.RNN` return `(out, h_n)` with `h_n` one note; **`nn.LSTM` returns `(out, (h_n, c_n))`: its second answer is a pair** (Clinic 2). A `(T, 4)` input is one sequence; `(1, T, 4)` without `batch_first=True` is **not** (Clinic 6). The parameter counts, printed by block 6, are `352` (RNN), `1056` (GRU, three times) and `1408` (LSTM, four times): one score group per dial.

**(c) `tensor.fill_(x)` — overwrite every number in place.**

```text
with torch.no_grad():
    quiet.weight_hh.fill_(0.0)             # every recurrent weight becomes 0
    cell.bias_ih[16:32].fill_(2.0)         # only a SLICE: the forget group of the bias
```

Read as: *"the trailing underscore means 'change it where it stands' instead of returning a new tensor."* On a tensor that PyTorch is tracking (a layer's knob) it must be inside `with torch.no_grad():`, which the student has from Level 3 Week 21 (Clinic 3). On a **slice**, `bias[16:32]` is a *view* of the same numbers, so filling it changes the bias itself. There are two biases in a layer (`bias_ih` and `bias_hh`); the code sets the forget group of the first to the chosen value and of the second to `0`, so the two add to the value (block 5).

### 5. The other code the student types — nothing new, but note these

All old: `@`, `torch.sigmoid`, `torch.tanh` and element-wise `*` (Weeks 8-10, Level 3), slices `z[0:H]`, `torch.allclose` (Week 8), `.abs()`, `.max()`, `.item()` and `.tolist()` on tensors (Weeks 1-10), `h.retain_grad()` (Week 10; now used on `c`), `requires_grad=True` and `x.grad` (Level 3), `tensor.norm()` (Week 2), `torch.randn(T, D)` (Week 10), `with torch.no_grad():` (Level 3 Week 21), list comprehensions and f-strings with `:.2e` (Level 3, Week 6), `sum([...])` over a list of `p.numel()` (Week 8's "count them"), a function with a default argument (`make_lstm_cell(forget_bias, seed=0)`), and `math.exp` and `math.tanh` (Level 3). **One pattern to point at**: block 6's `{"rnn": nn.RNN, "gru": nn.GRU, "lstm": nn.LSTM}[kind](D, H)` is a dictionary (Level 3) whose *values are classes*; the student looks one up by name and then calls it. Read it in two halves: "the thing I get out is `nn.GRU`" and "then I call it with `(D, H)`".

**Not used today, on purpose**, because they are later rungs: `F.cross_entropy` (Week 12), `F.softmax` (Week 13), attention (Week 14), `nn.GRUCell` and `nn.RNNCell` (not on the ladder). **The teacher-only blocks use a few things the student never sees** (a fractional power `** (1 / 39)`, `binary_cross_entropy_with_logits`, `Adam`, `batch_first=True`, a 1-unit `nn.GRU`) and are marked. Do not paste them into the student's file.

### 6. What the numbers will say

Read these before class so nothing surprises you. **Every number is printed by the blocks below.**

- **Dials.** `sigmoid(0) = 0.5`, `sigmoid(3) = 0.9526`, `sigmoid(4) = 0.9820`; forty of them leave `9.1e-13`, `0.1432`, `0.4838`.
- **The hand unit** (block 2): memory as a share of step 1 is `100.0, 95.3, 90.7, 86.4` per cent; Week 8's RNN note was `100.0, 47.7, 23.6, 11.8`. The slope back three steps is `f ** 3 = 0.8644` (the RNN's was `0.1041`); forty steps `0.1432`.
- **The cell from scratch** (block 3): the biggest gap to `nn.LSTMCell` is `0.0` at step 1 and at most `3.0e-08` by step 5 (float rounding: the two add the same numbers in a different order). `allclose` says `True True`. The cell holds `1408` numbers.
- **The highway** (block 4): with the recurrent weights set to zero the slope of step `p+1` back to step `p` equals the forget dial to `6.0e-08`. But that cell still has a default dial of about `0.5`, so the memory-track gradient still falls: `1.82e+00` at position 40, `3.16e-03` at 30, `9.46e-06` at 20, `2.97e-08` at 10, `2.15e-10` at 1. **"The slope is `f`" and "`f` is about one half" are both true, and together they are Week 10 again.**
- **The dial** (block 5), a real-weight cell, forget bias 0, 1, 2, 4: average `f` at step 1 is `0.510, 0.732, 0.879, 0.981`; the gradient at position 1 over position 40 is `1.93e-09, 9.84e-04, 2.21e-01, 1.08e+00`. (At bias 4 the ratio is above 1: for this one random input the first step mattered more than the last. We did not look into why; it is not a bug.)
- **The three layers** (block 6), first word over last word, seed 0:

| | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| rnn | 6.72e-03 | 1.77e-05 | 1.99e-10 | 6.48e-20 |
| gru | 2.84e-02 | 1.49e-04 | 1.36e-08 | 6.71e-18 |
| lstm | 7.65e-03 | 2.53e-04 | 2.05e-09 | 6.64e-16 |

- **The dial again** (block 7), seed 0, first over last:

| forget bias (sigmoid) | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| 0.0 (0.500) | 7.20e-03 | 4.86e-05 | 9.83e-10 | 3.92e-17 |
| 1.0 (0.731) | 1.07e-01 | 2.95e-02 | 3.52e-04 | 1.44e-06 |
| 2.0 (0.881) | 3.54e-01 | 3.10e-01 | 5.77e-02 | 3.37e-02 |
| 4.0 (0.982) | 7.23e-01 | 8.46e-01 | 3.52e-01 | 1.61e-01 |

**Say the shape of each row.** Bias 0 falls at the same rate as the RNN. Bias 1 falls, more slowly. Bias 2 and 4 **stay within a factor of 30 (bias 2) or 6 (bias 4) of the last word's pull all the way to `T = 80`**. The dial does not stop the fall; it slows it from "a factor of 10,000 or more every twenty steps" to "a factor of a few".
- **Seeds** (block 7, `T = 40`): rnn `2.0e-10, 6.3e-11, 3.1e-10`; gru `1.4e-08, 1.5e-09, 8.9e-10`; lstm `2.0e-09, 7.1e-08, 6.8e-09`; lstm with bias 0 `9.8e-10, 4.3e-09, 4.2e-09`; lstm with bias 2 `5.8e-02, 1.3e-01, 2.2e-01`. Spread inside a row: one to two orders. Gap between the default rows and the bias-2 row: **seven**. The ordering RNN below GRU below LSTM holds in these three seeds but the gaps are small, and **three seeds is not enough to call it**.
- **Typical slope per step** (`T1`, `(first / last) ** (1 / 39)`, seeds 0-2): rnn `0.564, 0.548, 0.570` (Week 10 found `0.51`-`0.55` for the note); gru `0.628, 0.594, 0.586`; lstm `0.599, 0.656, 0.617`; bias 2 `0.929, 0.950, 0.962`; bias 4 `0.974, 0.971, 0.996`. Bias 2 sits above `sigmoid(2) = 0.881`; we did not look into why.
- **Trained check** (`T2`): see the 🧭 claims above and section 7.
- **The limit** (`T3`): at `T = 400`, bias 2 gives `5.4e-08, 2.3e-12, 1.7e-14` and bias 4 gives `1.3e-04, 1.2e-01, 1.2e-04`; the plain RNN is too small to store (`0.0`). `sigmoid(2) ** 400 = 8.9e-23`, `sigmoid(4) ** 400 = 7.0e-04`, `0.95 ** 400 = 1.229e-09`. (The reference module says `0.95 ** 400` is "about `4e-09`"; that is wrong by a factor of 3. Its other figure, `0.9526 ** 400 ≈ 3.7e-09`, is right: we print `3.666e-09`.)

### 7. The honest limits of today

1. **Untrained weights, random inputs, a toy loss.** All three are *probes*. Nothing in the student's lesson is trained. `T2` is the only training, it is a teacher check, and its task is a stand-in.
2. **One width (16), one input size (4), three seeds.** Not tested: other widths, other input sizes. Three seeds show the gap between the default rows and the bias-2 row is far bigger than the spread; they do not establish the ordering RNN < GRU < LSTM.
3. **`T2` disagrees with the probe in two places, and we did not explain either.** (i) Default GRU and default LSTM got `0 of 5` at `T = 40`, worse than the RNN's `4 of 5`, although their probe ratios are *larger*. (ii) At `T = 80`, bias 2 has a healthy ratio and `0 of 5` (also `0 of 5` with 1000 steps); bias 4 gets one seed. A reason worth testing (not tested): 300 Adam steps at `lr = 0.01` on 16 units may simply not be enough. **Say "I do not know yet", and do not give the student a story.**
4. **The GRU trick.** Clinic 7 prints one number (seed 0, `T = 40`) for a GRU whose `z`-group bias is `+2`: `3.8e-02`. Other seeds and lengths were not put in a block, so **do not quote a general figure**.
5. **The parked cell of Week 10 and the dial `0.9526` are two different things that happen to be the same number.** Do not link them.
6. **Rounding.** The hand unit (block 2) ends `h = 0.4889`; the module says `0.4888`. The module multiplied rounded intermediate numbers. Use ours.
7. **A wording note for you.** Week 10's teacher preview says the student "measures the same table again" and "page 10.4 is what it is compared with". Today's table measures the gradient on the *word* with a `(first / last)` ratio, not on the note; the comparison table in section 3 is how to honour the promise without pretending the numbers are the same. If page 10.4 is blank, the student can still do today; they just cannot do that comparison.

### 8. The three misconceptions you will actually meet

1. **"The LSTM remembers because it has more weights / four of everything."** More numbers did nothing by themselves: default LSTM `2e-09` against RNN `2e-10`. What matters is the **`+`** and the **dial value**. Fix: block 7's bias-0 row against the bias-2 row, with the same number of weights.
2. **"A gate decides what is important."** Tempting and unsupported today. A gate is a number between 0 and 1 that multiplies something; what it "decides" is a story about a trained network, and nothing is trained. Say: *"what the gate **does** is multiply; why it ends up where it does is Week 12 and later."*
3. **"If a bias of 2 is good, 10 is better."** On a calculator `sigmoid(10)` is `0.99995`: the memory would almost never forget, so it would also almost never clear old things. Block 7 shows bias 4 already at a ratio near 1 (the memory barely decays), and `T2` shows bias 4 is not a cure-all at `T = 80` (one seed in five). We did not test bias 10; say so.

### 9. How deep to go, and where to stop

Stop at: *"an LSTM keeps a second track and updates it by adding; the slope back along it is the forget dial; a dial near 1 is a highway; the dial starts near one half, so you set it; and setting it is not learning."* Do **not** go into peephole connections, `proj_size`, bidirectional layers, stacking layers, variational dropout, truncated backprop, why `T2` behaves as it does, or how real systems choose a forget bias in practice. If the student asks *"so is the problem solved?"*: *"Not at 400 steps: `0.95 ** 400` is `1.2e-09` again. Week 14 is the design that does not multiply at all."*

### 10. 🧭 Where Week 11 sits

```text
   W2   running average: average = keep*old + (1-keep)*new
   W6   residual: x + f(x) has slope 1 + f'(x): a highway
   W8   a loop: one cell reused; the note is REWRITTEN each step
   W10  the loop's slopes compound: forty of them are tiny or huge
   W11  (today) a second track, UPDATED BY ADDING: c = f*c_old + i*g
        the slope back is f; a dial near 1 is W6's highway in a loop;
        the dial starts near 1/2, so set it. Nothing trained yet.
   W12  the LSTM meets 231 names: teacher forcing, padding, generation
   W13  sampling; exposure bias
   W14  attention: skip the loop altogether (the design that does not multiply)
```

---

## 🧰 Prep Checklist

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

- [ ] **Make a working folder and one file, `week11.py`.** Paste the seven blocks below into it **one under the other, with no gap**, running the file after each. Each block uses names defined by the ones above. The output printed under each block is what **that block** prints (the whole file prints all seven in order). Total runtime: about 1 second.

**Block 1 — the dial** (a sigmoid, and what a dial does to forty steps; no torch)

```python
# dial.py - Week 11: a gate is a dial between 0 and 1. The squasher (sigmoid) turns any score into a dial setting. No torch yet.
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

print("score z -> dial f = sigmoid(z) -> what f multiplied by itself 40 times leaves")
for z in [-2, 0, 1, 2, 3, 4]:
    f = sigmoid(z)
    print(f"  z = {z:2d}   f = {f:.4f}   f ** 40 = {f ** 40:.3e}")
```

```text
score z -> dial f = sigmoid(z) -> what f multiplied by itself 40 times leaves
  z = -2   f = 0.1192   f ** 40 = 1.126e-37
  z =  0   f = 0.5000   f ** 40 = 9.095e-13
  z =  1   f = 0.7311   f ** 40 = 3.615e-06
  z =  2   f = 0.8808   f ** 40 = 6.238e-03
  z =  3   f = 0.9526   f ** 40 = 1.432e-01
  z =  4   f = 0.9820   f ** 40 = 4.838e-01
```

`sigmoid(0)` is exactly `0.5`: an untrained gate, whose score is near 0, is a half-closed dial. `1.126e-37` is a very small number that Python still holds. The last column is the whole story: only a dial of `0.95` or more keeps anything.

**Block 2 — one LSTM unit, by hand** (Week 8's spike, the reference module's worked example)

```python
# unit.py - Week 11: ONE LSTM unit by hand on Week 8's spike (1, 0, 0, 0). The dials are set by hand, as on the page.
f = sigmoid(3.0)                 # forget dial: stuck near "keep", whatever the input
o = sigmoid(1.0)                 # output dial
c = 0.0                          # the memory track starts empty
memory = []
print("step  x    i       g       c       h")
for t, x in enumerate([1, 0, 0, 0], start=1):
    i = sigmoid(5 * x - 2.5)     # input dial: wide open for a 1, nearly shut for a 0
    g = math.tanh(2 * x)         # the candidate: what COULD be written
    c = f * c + i * g            # THE line: keep some of the old memory, ADD some of the new
    h = o * math.tanh(c)
    memory.append(c)
    print(f"  {t}   {x}   {i:.4f}  {g:.4f}  {c:.4f}  {h:.4f}")

notes = [0.7616, 0.3634, 0.1797, 0.0896]          # Week 8's four notes (the RNN)
print("LSTM memory as % of step 1:", [round(100 * m / memory[0], 1) for m in memory])
print("RNN  note   as % of step 1:", [round(100 * n / notes[0], 1) for n in notes])
print("slope back through 3 steps of the memory track: f ** 3 =", round(f ** 3, 4), "   (the RNN's was 0.1041)")
print("slope back through 40 steps:                    f ** 40 =", round(f ** 40, 4))
```

```text
step  x    i       g       c       h
  1   1   0.9241  0.9640  0.8909  0.5204
  2   0   0.0759  0.0000  0.8486  0.5047
  3   0   0.0759  0.0000  0.8084  0.4889
  4   0   0.0759  0.0000  0.7701  0.4730
LSTM memory as % of step 1: [100.0, 95.3, 90.7, 86.4]
RNN  note   as % of step 1: [100.0, 47.7, 23.6, 11.8]
slope back through 3 steps of the memory track: f ** 3 = 0.8644    (the RNN's was 0.1041)
slope back through 40 steps:                    f ** 40 = 0.1432
```

Read the `c` column against Week 8's note column: `0.8909, 0.8486, 0.8084, 0.7701` (the memory loses about 5% a step) against `0.7616, 0.3634, 0.1797, 0.0896` (the note loses half). The line `c = f * c + i * g` has **no `tanh` around the old `c`**: the old memory is only multiplied by `f`. At `x = 0` the input dial `i = 0.0759` and `g = 0.0000`, so nothing new is written; that is why the memory just decays by `f`.

**Block 3 — one LSTM step from scratch, checked** (the first new construct, `nn.LSTMCell`)

```python
# cell.py - Week 11: one LSTM step written out with @ and slices, checked against nn.LSTMCell.
import torch
import torch.nn as nn
torch.set_num_threads(1)

D, H = 4, 16
torch.manual_seed(0)
cell = nn.LSTMCell(D, H)         # ONE step of an LSTM: 4 numbers in, 16 numbers of memory and 16 of note
print("weight_ih:", tuple(cell.weight_ih.shape), "  weight_hh:", tuple(cell.weight_hh.shape), "  bias_ih:", tuple(cell.bias_ih.shape))

def lstm_step(cell, x, h, c):
    z = cell.weight_ih @ x + cell.bias_ih + cell.weight_hh @ h + cell.bias_hh    # 64 scores: four groups of 16
    i = torch.sigmoid(z[0:H])              # input dial   (first 16)
    f = torch.sigmoid(z[H:2 * H])          # forget dial  (second 16)
    g = torch.tanh(z[2 * H:3 * H])         # candidate    (third 16)
    o = torch.sigmoid(z[3 * H:4 * H])      # output dial  (last 16)
    c_new = f * c + i * g
    h_new = o * torch.tanh(c_new)
    return h_new, c_new, f

x = torch.randn(5, D)                      # five steps of input
mine_h, mine_c = torch.zeros(H), torch.zeros(H)
ref_h, ref_c = torch.zeros(H), torch.zeros(H)
for t in range(5):
    mine_h, mine_c, f = lstm_step(cell, x[t], mine_h, mine_c)
    ref_h, ref_c = cell(x[t], (ref_h, ref_c))              # the state goes in, and comes out, as a PAIR
    print(f"step {t + 1}: biggest gap in h = {(mine_h - ref_h).abs().max().item():.1e}   in c = {(mine_c - ref_c).abs().max().item():.1e}")
print("same answer:", torch.allclose(mine_h, ref_h), torch.allclose(mine_c, ref_c))
print("numbers in the cell:", sum([p.numel() for p in cell.parameters()]), "= 4 x (16x4 + 16x16 + 16 + 16)")
```

```text
weight_ih: (64, 4)   weight_hh: (64, 16)   bias_ih: (64,)
step 1: biggest gap in h = 0.0e+00   in c = 0.0e+00
step 2: biggest gap in h = 7.5e-09   in c = 1.5e-08
step 3: biggest gap in h = 3.7e-09   in c = 7.5e-09
step 4: biggest gap in h = 3.7e-09   in c = 7.5e-09
step 5: biggest gap in h = 1.5e-08   in c = 3.0e-08
same answer: True True
numbers in the cell: 1408 = 4 x (16x4 + 16x16 + 16 + 16)
```

`(64, 4)` is four groups of 16 scores for the 4-number input; `(64, 16)` four groups for the 16-number note. The gaps are `0.0` at step 1 and at most `3.0e-08` after: not exactly zero because the two versions add the same numbers in a different order, which float32 (about seven digits) cannot tell apart. `True True` says the two agree. `1408 = 4 x (64 + 256 + 16 + 16)`, written in the print as `4 x (16x4 + 16x16 + 16 + 16)`. The function returns `f` as well as `h` and `c`; the next block needs it.

**Block 4 — the highway** (`fill_` on a whole tensor, and `retain_grad` on the memory track)

```python
# highway.py - Week 11: run the cell for 40 steps and ask the MEMORY track how much the end cares about each step.
def run_lstm(cell, x):
    h, c = torch.zeros(H), torch.zeros(H)
    cs, fs = [], []
    for t in range(len(x)):
        h, c, f = lstm_step(cell, x[t], h, c)
        c.retain_grad()                    # Week 10's line, now on the memory track c
        cs.append(c)
        fs.append(f)
    h.sum().backward()                     # the "loss": add up the 16 numbers of the LAST h
    return cs, fs

torch.manual_seed(1)
x40 = torch.randn(40, D)

# First a cell whose dials look ONLY at the input: every recurrent weight is set to 0.
torch.manual_seed(0)
quiet = nn.LSTMCell(D, H)
with torch.no_grad():
    quiet.weight_hh.fill_(0.0)             # fill_ (new): overwrite every number in the tensor, in place
cs, fs = run_lstm(quiet, x40)
gaps = [(cs[p].grad / cs[p + 1].grad - fs[p + 1]).abs().max().item() for p in range(39)]
print("slope of step p+1 back to step p, minus the forget dial f: biggest gap over 39 steps =", f"{max(gaps):.1e}")
print("so with no recurrent weights, the slope back through the memory track IS f:")
print("   step 31 -> 30, first three units: slope", [round(v, 4) for v in (cs[29].grad / cs[30].grad)[:3].tolist()], " f", [round(v, 4) for v in fs[30][:3].tolist()])
g = [c.grad.norm().item() for c in cs]
for p in [40, 30, 20, 10, 1]:
    print(f"   position {p:2d}: {g[p - 1]:.2e}")
```

```text
slope of step p+1 back to step p, minus the forget dial f: biggest gap over 39 steps = 6.0e-08
so with no recurrent weights, the slope back through the memory track IS f:
   step 31 -> 30, first three units: slope [0.6677, 0.5753, 0.6577]  f [0.6677, 0.5753, 0.6577]
   position 40: 1.82e+00
   position 30: 3.16e-03
   position 20: 9.46e-06
   position 10: 2.97e-08
   position  1: 2.15e-10
```

The first printed line says the slope from step `p + 1` back to step `p` (for every one of the 39 steps; the biggest gap is `6.0e-08`) **equals** the forget dial, when the dials look only at the input. Then the honest part: that cell's dial is about one half (the first three units at step 31 were `0.6677, 0.5753, 0.6577`), so forty of them still leave `2.15e-10` at position 1 against `1.82` at position 40. **"The slope is `f`" is a fact about the design; whether it helps depends on `f`.**

**Block 5 — turn the dial up** (`fill_` on a slice, in a real-weight cell)

```python
# dial.py - Week 11: turn the forget dial up BEFORE training. Only the forget group of the bias (the second 16 of 64) is touched.
def make_lstm_cell(forget_bias, seed=0):
    torch.manual_seed(seed)
    cell = nn.LSTMCell(D, H)
    with torch.no_grad():
        cell.bias_ih[H:2 * H].fill_(forget_bias)     # fill_ on a SLICE: 16 of the 64 bias numbers
        cell.bias_hh[H:2 * H].fill_(0.0)             # the layer has two biases; zero the other one's forget group
    return cell

print("forget bias | average f at step 1 | memory-track gradient at positions 40, 20, 1 | position 1 / position 40")
for fb in [0.0, 1.0, 2.0, 4.0]:
    cs, fs = run_lstm(make_lstm_cell(fb), x40)
    g = [c.grad.norm().item() for c in cs]
    print(f"   {fb:3.1f}      |       {fs[0].mean().item():.3f}         |   {g[39]:.2e}   {g[19]:.2e}   {g[0]:.2e}   |   {g[0] / g[39]:.2e}")
```

```text
forget bias | average f at step 1 | memory-track gradient at positions 40, 20, 1 | position 1 / position 40
   0.0      |       0.510         |   1.83e+00   6.89e-05   3.52e-09   |   1.93e-09
   1.0      |       0.732         |   1.74e+00   3.20e-02   1.71e-03   |   9.84e-04
   2.0      |       0.879         |   1.43e+00   3.26e-01   3.16e-01   |   2.21e-01
   4.0      |       0.981         |   5.59e-01   3.20e-01   6.05e-01   |   1.08e+00
```

At forget bias 0 the dial is about `0.51` and position 1 is `1.9e-09` of position 40 (Week 10's disease). At 2 it is `0.879` and position 1 keeps `0.22` of position 40. At 4 it is `0.981` and the ratio is `1.08`. (`make_lstm_cell` with bias `0.0` is not identical to the default cell, whose bias is small and random; block 4's cell was the default one.)

**Block 6 — the whole-sequence layers** (`nn.RNN`, `nn.GRU`, `nn.LSTM`, and a probe that works on all three)

```python
# layers.py - Week 11: the whole-sequence layers. nn.RNN, nn.GRU and nn.LSTM take the same input and give the same first answer.
def make_layer(kind, seed=0, forget_bias=None):
    torch.manual_seed(seed)
    layer = {"rnn": nn.RNN, "gru": nn.GRU, "lstm": nn.LSTM}[kind](D, H)
    if forget_bias is not None:              # only meaningful for the LSTM (see block 7)
        with torch.no_grad():
            layer.bias_ih_l0[H:2 * H].fill_(forget_bias)
            layer.bias_hh_l0[H:2 * H].fill_(0.0)
    return layer

for kind in ["rnn", "gru", "lstm"]:
    layer = make_layer(kind)
    out, last = layer(torch.randn(5, D))     # five steps in
    size = sum([p.numel() for p in layer.parameters()])
    print(f"{kind:4s}: numbers {size:5d}   out {tuple(out.shape)}")
out, h_n = make_layer("gru")(torch.randn(5, D))
print("the GRU's second answer is ONE note, h_n:", tuple(h_n.shape))
out, last = make_layer("lstm")(torch.randn(5, D))
h_n, c_n = last                              # the LSTM's second answer is a PAIR: the note AND the memory track
print("the LSTM's second answer is a pair: h_n", tuple(h_n.shape), " c_n", tuple(c_n.shape))

def reach(layer, T, seed=0):
    torch.manual_seed(100 + seed)
    x = torch.randn(T, D, requires_grad=True)        # the words themselves are tracked, so x.grad will exist
    out, last = layer(x)
    out[-1].sum().backward()                         # the "loss": the 16 numbers of the LAST output
    return [row.norm().item() for row in x.grad]     # how much the end cares about the word at each position

print("pull of the FIRST word as a fraction of the pull of the LAST (seed 0):")
print("kind          |     T=10      T=20      T=40      T=80")
for kind in ["rnn", "gru", "lstm"]:
    row = []
    for T in [10, 20, 40, 80]:
        sizes = reach(make_layer(kind), T)
        row.append(sizes[0] / sizes[-1])
    print(f"{kind:13s} |" + "".join(f"  {v:8.2e}" for v in row))
```

```text
rnn : numbers   352   out (5, 16)
gru : numbers  1056   out (5, 16)
lstm: numbers  1408   out (5, 16)
the GRU's second answer is ONE note, h_n: (1, 16)
the LSTM's second answer is a pair: h_n (1, 16)  c_n (1, 16)
pull of the FIRST word as a fraction of the pull of the LAST (seed 0):
kind          |     T=10      T=20      T=40      T=80
rnn           |  6.72e-03  1.77e-05  1.99e-10  6.48e-20
gru           |  2.84e-02  1.49e-04  1.36e-08  6.71e-18
lstm          |  7.65e-03  2.53e-04  2.05e-09  6.64e-16
```

`352, 1056, 1408` is `1x, 3x, 4x`: one group of scores for each dial. Read the table one row at a time: **all three fall by the same kind of amount; between `T = 20` and `T = 40` each loses a factor of 10,000 to 100,000.** At default settings, gates alone did not open the highway. The `(first / last)` ratio is used because the last word's own pull differs from layer to layer, and the ratio puts the three on one scale.

**Block 7 — three seeds, and the dial** (the comparison the week is about)

```python
# compare.py - Week 11: three seeds, and the forget dial. Same recipe as block 6, one seed at a time.
def ratio(kind, T, seed, forget_bias=None):
    sizes = reach(make_layer(kind, seed, forget_bias), T, seed)
    return sizes[0] / sizes[-1]

print("T = 40, first word / last word, seeds 0, 1, 2:")
for label, kind, fb in [("rnn", "rnn", None), ("gru", "gru", None), ("lstm", "lstm", None), ("lstm, forget bias 0", "lstm", 0.0), ("lstm, forget bias 2", "lstm", 2.0)]:
    print(f"  {label:20s}", [f"{ratio(kind, 40, seed, fb):.1e}" for seed in range(3)])

print("the forget dial, seed 0 (sigmoid of the bias in brackets):")
print("forget bias |     T=10      T=20      T=40      T=80")
for fb in [0.0, 1.0, 2.0, 4.0]:
    row = [ratio("lstm", T, 0, fb) for T in [10, 20, 40, 80]]
    print(f"  {fb:3.1f} ({sigmoid(fb):.3f}) |" + "".join(f"  {v:8.2e}" for v in row))
```

```text
T = 40, first word / last word, seeds 0, 1, 2:
  rnn                  ['2.0e-10', '6.3e-11', '3.1e-10']
  gru                  ['1.4e-08', '1.5e-09', '8.9e-10']
  lstm                 ['2.0e-09', '7.1e-08', '6.8e-09']
  lstm, forget bias 0  ['9.8e-10', '4.3e-09', '4.2e-09']
  lstm, forget bias 2  ['5.8e-02', '1.3e-01', '2.2e-01']
the forget dial, seed 0 (sigmoid of the bias in brackets):
forget bias |     T=10      T=20      T=40      T=80
  0.0 (0.500) |  7.20e-03  4.86e-05  9.83e-10  3.92e-17
  1.0 (0.731) |  1.07e-01  2.95e-02  3.52e-04  1.44e-06
  2.0 (0.881) |  3.54e-01  3.10e-01  5.77e-02  3.37e-02
  4.0 (0.982) |  7.23e-01  8.46e-01  3.52e-01  1.61e-01
```

Read the first five lines: the last two rows (`lstm, forget bias 0` against `lstm, forget bias 2`) are the same layer, same seeds, one number different in the bias, and they are **seven orders of magnitude apart**. Then the second table: a dial at `0.881` or `0.982` turns a fall of a factor of about `10` to the `16` (bias 0, `T = 80`) into a fall of a factor of 30 or 6.

- [ ] **Run the teacher-only blocks** (paste them *below* the seven, in a copy named `teacher11.py`). `T1` checks the GRU's convention and prints the typical slope per step; `T2` trains 55 small layers (about 55 seconds); `T3` is the honest limit at `T = 400`; `K1` is the workbook key.

**Block T1 — teacher only: the GRU's dial, and the typical slope per step**

```python
# TEACHER-ONLY T1: (a) which way does PyTorch's GRU dial point?  (b) the typical slope per step behind block 7's rows.
# (Uses a fractional power ** (1 / k); the student never sees this block.)
gru = nn.GRU(1, 1)
with torch.no_grad():
    for p in gru.parameters():
        p.fill_(0.0)
    gru.bias_ih_l0[1:2].fill_(10.0)        # GRU bias groups are r, z, n: index 1 is z
out, last = gru(torch.zeros(1, 1), torch.tensor([[0.5]]))
print("GRU, z bias +10, old note 0.5, input 0 -> new note", round(out.item(), 4), "(0.5 means z = KEEP)")
with torch.no_grad():
    gru.bias_ih_l0[1:2].fill_(-10.0)
out, last = gru(torch.zeros(1, 1), torch.tensor([[0.5]]))
print("GRU, z bias -10, old note 0.5, input 0 -> new note", round(out.item(), 4), "(0 means z = REPLACE)")

print("typical slope per step = (first / last) ** (1 / 39), T = 40, seeds 0-2:")
for label, kind, fb in [("rnn", "rnn", None), ("gru", "gru", None), ("lstm", "lstm", None), ("lstm, forget bias 2", "lstm", 2.0), ("lstm, forget bias 4", "lstm", 4.0)]:
    print(f"  {label:20s}", [f"{ratio(kind, 40, s, fb) ** (1 / 39):.3f}" for s in range(3)])
print("sigmoid(2) =", round(sigmoid(2), 3), "  sigmoid(4) =", round(sigmoid(4), 3))
```

```text
GRU, z bias +10, old note 0.5, input 0 -> new note 0.5 (0.5 means z = KEEP)
GRU, z bias -10, old note 0.5, input 0 -> new note 0.0 (0 means z = REPLACE)
typical slope per step = (first / last) ** (1 / 39), T = 40, seeds 0-2:
  rnn                  ['0.564', '0.548', '0.570']
  gru                  ['0.628', '0.594', '0.586']
  lstm                 ['0.599', '0.656', '0.617']
  lstm, forget bias 2  ['0.929', '0.950', '0.962']
  lstm, forget bias 4  ['0.974', '0.971', '0.996']
sigmoid(2) = 0.881   sigmoid(4) = 0.982
```

Lines 1 and 2 are the whole GRU convention check: a `z` bias of `+10` leaves the old note alone (`0.5`); `-10` replaces it (`0.0`). So in PyTorch, `z` near 1 means **keep**. The slopes per step are `(first / last) ** (1 / 39)`: the single number per step that would give the same total fall.

**Block T2 — teacher only: does the probe predict learning?**

```python
# TEACHER-ONLY T2: does a bigger ratio mean it can LEARN? Train each layer to report the sign of its FIRST input, 300 Adam steps.
# (Uses binary_cross_entropy_with_logits, Adam and batch_first; the student never sees this block. A stand-in task, not a model.)
def first_bit(kind, T, seed=0, forget_bias=None, steps=300):
    torch.manual_seed(seed)
    layer = {"rnn": nn.RNN, "gru": nn.GRU, "lstm": nn.LSTM}[kind](1, H, batch_first=True)
    if forget_bias is not None:
        with torch.no_grad():
            layer.bias_ih_l0[H:2 * H].fill_(forget_bias)
            layer.bias_hh_l0[H:2 * H].fill_(0.0)
    head = nn.Linear(H, 1)
    opt = torch.optim.Adam(list(layer.parameters()) + list(head.parameters()), lr=1e-2)
    def batch(n):
        x = torch.randn(n, T, 1) * 0.5
        y = (torch.rand(n) > 0.5).float()
        x[:, 0, 0] = y * 2 - 1                      # the first input carries the answer; the rest is noise
        return x, y
    for step in range(steps):
        x, y = batch(64)
        out, last = layer(x)
        loss = nn.functional.binary_cross_entropy_with_logits(head(out[:, -1]).squeeze(1), y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    x, y = batch(1000)
    with torch.no_grad():
        out, last = layer(x)
    return ((head(out[:, -1]).squeeze(1) > 0).float() == y).float().mean().item()

for T in [40, 80]:
    for label, kind, fb in [("rnn", "rnn", None), ("gru", "gru", None), ("lstm", "lstm", None), ("lstm, forget bias 2", "lstm", 2.0), ("lstm, forget bias 4", "lstm", 4.0)]:
        print(f"T = {T}  {label:20s} accuracy, seeds 0-4:", [round(first_bit(kind, T, s, fb), 3) for s in range(5)])
print("T = 80  lstm, forget bias 2, 1000 steps instead of 300, seeds 0-4:", [round(first_bit("lstm", 80, s, 2.0, 1000), 3) for s in range(5)])
```

```text
T = 40  rnn                  accuracy, seeds 0-4: [1.0, 1.0, 1.0, 1.0, 0.503]
T = 40  gru                  accuracy, seeds 0-4: [0.519, 0.525, 0.521, 0.483, 0.489]
T = 40  lstm                 accuracy, seeds 0-4: [0.507, 0.512, 0.489, 0.52, 0.516]
T = 40  lstm, forget bias 2  accuracy, seeds 0-4: [0.998, 0.993, 0.993, 0.999, 0.998]
T = 40  lstm, forget bias 4  accuracy, seeds 0-4: [0.998, 0.999, 0.996, 0.999, 0.998]
T = 80  rnn                  accuracy, seeds 0-4: [0.47, 0.484, 0.5, 0.497, 1.0]
T = 80  gru                  accuracy, seeds 0-4: [0.488, 0.521, 0.483, 0.495, 0.505]
T = 80  lstm                 accuracy, seeds 0-4: [0.473, 0.51, 0.488, 0.491, 0.514]
T = 80  lstm, forget bias 2  accuracy, seeds 0-4: [0.473, 0.508, 0.488, 0.505, 0.514]
T = 80  lstm, forget bias 4  accuracy, seeds 0-4: [0.992, 0.508, 0.509, 0.509, 0.514]
T = 80  lstm, forget bias 2, 1000 steps instead of 300, seeds 0-4: [0.5, 0.493, 0.474, 0.504, 0.514]
```

Chance is `0.5`. Every success is near `1.0` and every failure near `0.5`, **except** that default GRU and LSTM at `T = 40` fail where the RNN mostly succeeds, and bias 2 fails at `T = 80` although its probe is healthy. **This block is why the lesson says "the dial opens the highway at the start", never "the LSTM learns long memories".** The last line is the 1000-step run quoted in the 🧭 claims.

**Block T3 — teacher only: gates buy hundreds of steps, not unlimited**

```python
# TEACHER-ONLY T3: the honest limit. Gates buy hundreds of steps, not unlimited ones.
print("0.95 ** 400 =", f"{0.95 ** 400:.3e}", "  0.9526 ** 400 =", f"{0.9526 ** 400:.3e}", "  sigmoid(2) ** 400 =", f"{sigmoid(2) ** 400:.3e}", "  sigmoid(4) ** 400 =", f"{sigmoid(4) ** 400:.3e}")
for label, kind, fb in [("rnn", "rnn", None), ("lstm, forget bias 2", "lstm", 2.0), ("lstm, forget bias 4", "lstm", 4.0)]:
    print(f"T = 400  {label:20s} first / last, seeds 0-2:", [f"{ratio(kind, 400, s, fb):.1e}" for s in range(3)])
```

```text
0.95 ** 400 = 1.229e-09   0.9526 ** 400 = 3.666e-09   sigmoid(2) ** 400 = 8.920e-23   sigmoid(4) ** 400 = 7.031e-04
T = 400  rnn                  first / last, seeds 0-2: ['0.0e+00', '0.0e+00', '0.0e+00']
T = 400  lstm, forget bias 2  first / last, seeds 0-2: ['5.4e-08', '2.3e-12', '1.7e-14']
T = 400  lstm, forget bias 4  first / last, seeds 0-2: ['1.3e-04', '1.2e-01', '1.2e-04']
```

`0.0e+00` means the number was below what a 32-bit float can hold: the RNN's ratio at `T = 400` is **too small for the computer to store**, not exactly zero. Bias 2 at `T = 400` is back to `1e-08`-`1e-14`; bias 4 keeps `1e-04` to `1e-01`.

**Block K1 — teacher only: `key.py`, every workbook answer computed**

```python
# TEACHER-ONLY key.py - Week 11: every hand-arithmetic answer in the workbook, computed.
print("11.1 dials")
for z in [-2, 0, 1, 3, 5]:
    print(f"  sigmoid({z}) = {sigmoid(z):.4f}")
for f in [0.5, 0.88, 0.95, 0.99]:
    print(f"  {f} ** 40 = {f ** 40:.4g}")
count, value = 0, 1.0
while value > 0.5:
    value = value * 0.95
    count = count + 1
print(f"  0.95 first below one half after {count} multiplications ({value:.4f})")
print("11.2 one unit, f = sigmoid(2), spike (1, 0, 0)")
f, o, c = sigmoid(2.0), sigmoid(1.0), 0.0
cs = []
for t, x in enumerate([1, 0, 0], start=1):
    i, g = sigmoid(5 * x - 2.5), math.tanh(2 * x)
    c = f * c + i * g
    h = o * math.tanh(c)
    cs.append(c)
    print(f"  t = {t}: f = {f:.4f}  i = {i:.4f}  g = {g:.4f}  c = {c:.4f}  h = {h:.4f}  c as % of t=1: {100 * c / cs[0]:.1f}")
print(f"  slope back from step 3 to step 1: f ** 2 = {f ** 2:.4f}")
print("11.2 the same unit with f = sigmoid(0) = 0.5")
f, c = sigmoid(0.0), 0.0
cs = []
for t, x in enumerate([1, 0, 0], start=1):
    i, g = sigmoid(5 * x - 2.5), math.tanh(2 * x)
    c = f * c + i * g
    cs.append(c)
print("  c:", [round(v, 4) for v in cs], " % of t=1:", [round(100 * v / cs[0], 1) for v in cs])
print("hook: which constant dial leaves half after 40 people?")
for f in [0.98, 0.982, 0.983, 0.985, 0.99]:
    print(f"  {f} ** 40 = {f ** 40:.4f}")
print("half-way dial, exactly (teacher only): 0.5 ** (1 / 40) =", round(0.5 ** (1 / 40), 4))
```

```text
11.1 dials
  sigmoid(-2) = 0.1192
  sigmoid(0) = 0.5000
  sigmoid(1) = 0.7311
  sigmoid(3) = 0.9526
  sigmoid(5) = 0.9933
  0.5 ** 40 = 9.095e-13
  0.88 ** 40 = 0.006016
  0.95 ** 40 = 0.1285
  0.99 ** 40 = 0.669
  0.95 first below one half after 14 multiplications (0.4877)
11.2 one unit, f = sigmoid(2), spike (1, 0, 0)
  t = 1: f = 0.8808  i = 0.9241  g = 0.9640  c = 0.8909  h = 0.5204  c as % of t=1: 100.0
  t = 2: f = 0.8808  i = 0.0759  g = 0.0000  c = 0.7847  h = 0.4791  c as % of t=1: 88.1
  t = 3: f = 0.8808  i = 0.0759  g = 0.0000  c = 0.6912  h = 0.4377  c as % of t=1: 77.6
  slope back from step 3 to step 1: f ** 2 = 0.7758
11.2 the same unit with f = sigmoid(0) = 0.5
  c: [0.8909, 0.4454, 0.2227]  % of t=1: [100.0, 50.0, 25.0]
hook: which constant dial leaves half after 40 people?
  0.98 ** 40 = 0.4457
  0.982 ** 40 = 0.4836
  0.983 ** 40 = 0.5037
  0.985 ** 40 = 0.5463
  0.99 ** 40 = 0.6690
half-way dial, exactly (teacher only): 0.5 ** (1 / 40) = 0.9828
```

- [ ] **Print** workbook pages 11.1-11.6.
- [ ] **Read the Debugging Clinic**, and keep its seven blocks ready to paste under `week11.py` in a scratch file.
- [ ] **Put a calculator on the desk** that has a power key (`x^y`) and an `e^x` key.
- [ ] **Have page 10.4 (Week 10's grid) ready** if the student did it. If it is blank, say so now: the comparison is nice to have, not needed.

### 3 minutes on the day

- [ ] Open `week11.py` as an **empty file** for typing.
- [ ] Calculator, timer and workbook pages on the desk.

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Blocks 1 and 2 need only Python; pages 11.1 and 11.2 need only paper and the calculator. Run the rest from the printed outputs and say so. |
| `NameError: name 'sigmoid' is not defined` (or `lstm_step`, `make_layer`, `reach`, `D`, `H`) | The earlier block was not pasted above. The seven blocks are one file. |
| `ValueError: LSTMCell: Expected hx[0] to be 1D or 2D` | Clinic 1: the state must be a pair `(h, c)`. |
| `AttributeError: 'tuple' object has no attribute 'shape'` | Clinic 2: `nn.LSTM` returns `(out, (h_n, c_n))`. |
| `RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.` | Clinic 3: `fill_` needs `with torch.no_grad():`. |
| A table differs in the second digit | Different PyTorch build or CPU. Compare the **orders of magnitude** (`e-10`, `e-02`) and the shape (all three default rows fall by a huge factor; bias 2 and 4 stay within a few). Use the number on your screen. |
| Block 4's gap is not near `1e-08` | Check `quiet.weight_hh.fill_(0.0)` ran: if the recurrent weights are not zero the gap is large, because the extra paths are included. |
| Block 7 is slow | It is not (a fraction of a second). Over 10 seconds means `torch.set_num_threads(1)` is missing from block 3. |
| No laptop at all | Do pages 11.1 and 11.2 with the calculator and read the tables (section 6) from this guide as "data from my laptop at home". Say so out loud. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 8 | The Forty-Person Telephone, again - but each person has a KEEP dial; find the dial that keeps half |
| 🧠 Concept | 14 | Rewrite versus add; the four dials; the slope back is `f`; why a dial starts near one half; the GRU in one minute |
| 💻 Live-code | 20 | Blocks 1-4 (the dial, a hand unit, the cell from scratch, the highway) |
| 🎲 Their turn | 23 | Predict then print the dial grid; three seeds; the forget bias |
| 🔑 Wrap & assign | 5 | What was shown, what was not; the homework |

### 🪝 Hook — The Telephone With a Dial (8 minutes)

**(2 min) Last week in one line.** Say: *"Forty people. Each passes on 95% of what they heard. How much arrives?"* They should remember `0.1285` (if not, let them press `0.95 ^ 40` again; it costs ten seconds and it is the setup). *"That person was multiplying, by a fixed 95%."*

**(3 min) The dial.** Say: *"New rule. Every person has a KEEP dial from 0 to 1. They keep that share of what they were told and pass it on. All forty people have the same dial. I want the dial setting that leaves half of the message at the end. Find it on the calculator, by trial."* **Write the guess on a card first**: *"0.9? 0.95? 0.99?"* They will try `0.9` (`0.0148`), `0.95` (`0.1285`), `0.99` (`0.669`), and home in: `0.98 ** 40 = 0.4457`, `0.982 ** 40 = 0.4836`, **`0.983 ** 40 = 0.5037`**. (`0.985` gives `0.5463`.) The answer is about **`0.983`**. Ask: *"How close to 1 is that?"* (Within two in a hundred of 1.) Write it on the board: **the dial has to be nearly 1.**

**(3 min) And the other way.** Say: *"Suppose I do not set the dial. Suppose the dial starts in the middle: 0.5. What arrives?"* `0.5 ** 40 = 9.1e-13` (Week 10's number). *"That is the thing we were stuck with last week: a loop that keeps half each time."* Then: *"A network cannot have a dial fixed at 0.983 forever, because sometimes it needs to forget. So the dial must be a **number the network computes**, from what it is reading, between 0 and 1."* That number is a **gate**; write the word.

**Bridge:** *"Last week we saw what happens when a loop rewrites its note every step. Today the loop keeps a second track that is not rewritten, only scaled and added to. Will a dial near 1 be enough? Let us measure."*

### 🧠 Concept — Add, Do Not Rewrite (14 minutes)

**(3 min) Rewrite versus add.** On the board draw last week's four boxes (note 1 to note 4). Write under them: **note = tanh(W x + W note)**. Say: *"Every step throws the old note away and computes a new one from it. The old note has to go through a tanh and a weight matrix to get into the new one. That is the multiplication."* Now draw a second line above the boxes, a long arrow left to right, labelled **memory `c`**. Write on it: **c = f x c_old + i x g**. Say: *"The memory is not rewritten. It is scaled by `f` and something is **added**."* Point at `+`: *"We saw that `+` in Week 6: `x + f(x)` has slope `1 + f'(x)`."* (Let them say it.) *"Here the slope of the memory with respect to the old memory is... what?"* (`f`.)

**(4 min) The four dials.** Keep it to names and jobs, and the **whiteboard story** from the reference module if the student likes a picture: an **eraser** (`f`, forget: how much of the old board to keep), a **writer** (`g`, the candidate: what could go on the board), an **editor** (`i`, input: how much of the draft actually goes up), a **spokesperson** (`o`, output: how much of the board is read out as the note `h`). Write under them: **three dials from sigmoid (`f`, `i`, `o`), one candidate from tanh (`g`)**. Say: *"Every dial is a score squashed by the sigmoid you already know, and a score is weights times what the cell sees plus a bias. Four scores from the same input, so four times the weights: 1408 numbers against the RNN's 352."* Do **not** claim what any of them "decides" (section 8, #2).

**(4 min) The slope, and the catch.** Ask: *"If `f` is 0.9526 at every step, what is the slope back forty steps?"* They do `0.9526 ** 40` and get `0.143` (compare: Week 10's cell gave `2e-10`). Then: *"And what is `f` at the very start, before anything is trained?"* Let them reason: the score is weights times inputs plus a bias, the bias starts near 0, the weights are small, so the score is near 0 and `sigmoid(0) = 0.5`. *"Forty of them?"* `9.1e-13`. **Pause.** *"So an LSTM built with no care is the RNN's disease again. What would you change?"* (Someone will say: start the forget score high. That is the **forget bias**, and it is the end of the lesson.)

**(3 min) The GRU in one minute.** Say: *"A GRU has two dials instead of four. The one that matters is called `z`. In PyTorch, `new note = z x old note + (1 - z) x candidate`. Where have you seen that?"* (Week 2: `average = keep x old + (1 - keep) x new`.) *"It is the running average with a dial the network sets at every step."* **Do not write the module's equation** (section 3, #4): it has `z` the other way round.

> **Check for understanding (do not skip).** *"If every dial is 0.5, what is left after 10 steps? After 40?"* (`0.5 ** 10 = 0.000977`, by calculator; `9.1e-13`.) *"If every dial is 0.9526, after 40?"* (`0.143`.) *"What sets the dial at the start?"* (The bias and the weights; near 0, so a half.) *"Which is the thing to change?"* (The bias on the forget score.) If they get the direction right and the size wrong, fine; if they think the LSTM is better *because it has more weights*, go back to the first sentence of the Concept.

### 💻 Live-Code Together — blocks 1-4 (20 minutes)

The student types; you narrate **after** they have predicted. Keep `week11.py` open and add each block under the last.

1. **Block 1 (3 min)**: the dial table. Predict one cell before running (`f ** 40` for `z = 3`?). Ask *"what score gives a dial of 0.5?"* (0.) *"why does `-2` give something with 37 zeros?"* (A small dial multiplied forty times.)
2. **Block 2 (3 min)**: the hand unit on Week 8's spike. They have done a hand RNN; this is the same four steps with a second line. Point at `c = f * c + i * g` and say: *"this one line is the LSTM."* Compare the two percentage lines: **86.4** against **11.8** after four steps. Then the slope line: `0.8644` against Week 10's `0.1041`.
3. **Block 3 (7 min)**: introduce **`nn.LSTMCell`** (section 4a): *"PyTorch has this step ready-made. We write it out, then check it."* Make them say the shapes aloud before running: `weight_ih` is `(64, 4)` (why 64? four groups of 16). Point at the slicing: *"the first 16 scores are the input dial, the next 16 the forget dial, then the candidate, then the output."* Run. The gaps are at most `3.0e-08`: say *"float32 has about seven digits, so that is the same number."* Note the state is a **pair** going in and out (Clinic 1 is the commonest error of the week).
4. **Block 4 (7 min)**: introduce **`fill_`** (section 4c): *"this zeros every recurrent weight. Why? So the dials can only look at the input, and the only way the old memory reaches the new one is the `f *` term."* Run. Read the first line: the biggest gap between the slope and `f` is `6.0e-08`. *"So the slope back through the memory track **is** the forget dial."* Then the catch, the five position lines: `1.82` at 40 down to `2.15e-10` at 1. *"Vanishing or exploding?"* (Vanishing.) *"Why, if the slope is `f` and `f` can be near 1?"* (`f` is about a half here.) **Pause.** Leave it open: block 5 answers it.

### 🎲 Their Turn — The Dial Grid (23 minutes)

**(2 min) The task.** Show the empty grid on workbook page 11.4: rows = rnn, gru, lstm, lstm with forget bias 2; columns = `T = 10, 20, 40, 80`. Say: *"The number is how much the last output cares about the first word, as a fraction of how much it cares about the last word. Before you run anything, put one letter in each of the 16 cells: **T** (tiny, below `1e-6`), **S** (small, `1e-6` to `1e-2`) or **L** (level, above `1e-2`). I will not tell you if you are right."* Most will write T for the RNN at the long lengths; **watch the GRU and LSTM rows**: many will write L for them.

**(5 min) Block 5, the dial.** They run block 5 **first** (it only needs blocks 1-4), read the four lines, and say the pattern: *bias 0: dial 0.51, position 1 is `1.9e-09` of position 40; bias 2: dial 0.879, position 1 keeps `0.22`*. *"Same cell, same weights, one number different."*

**(6 min) Block 6.** They run it and compare with their predictions. By the cut-offs: rnn: S, S, T, T; gru: L, S, T, T; lstm: S, S, T, T. *"Did the gates help?"* The honest answer: *a bit, in the GRU at short lengths; not at long ones. At default settings all three vanish.* Colour in the misses: **expect most predictions for the GRU and LSTM rows to have been too hopeful.** Read the parameter counts too: `352, 1056, 1408`.

**(4 min) Block 7, seeds and dial.** Three seeds for five rows at `T = 40`, then the dial grid. Ask: *"Which difference is bigger: between seeds inside a row, or between the bias-0 row and the bias-2 row?"* (Inside a row, a factor of 10 to 100; between rows, ten million.) *"Can you tell the GRU from the LSTM with three seeds?"* (No.) Then fill the fourth row of page 11.4 from block 7's bias-2 line: `3.54e-01, 3.10e-01, 5.77e-02, 3.37e-02` (all L).

**(3 min) The question that makes the activity.** Say: *"We set the forget bias by hand. Did anything learn?"* They should say **no**, and why: *"nothing was trained; we only looked at the starting point."* If they say "yes, it remembers", ask *"what did we train?"* Then: *"If I made the dial 0.99995 (bias 10), would you trust it more?"* (Discuss, section 8 #3.)

### 🔑 Wrap & Assign (5 minutes)

**(3 min) Three sentences.** The student says, from memory, in their own words: *(1) what the LSTM adds that the RNN does not have (a memory track updated by adding), (2) what the forget dial does to the slope back, (3) why the LSTM at default settings is not better than the RNN.* Write nothing for them. If they cannot do (3), go back to block 6's `lstm` row and block 5's first row.

**(2 min) What we did not do, said out loud.** *"We looked at an untrained cell with random numbers. We did not train anything; we did not show that any of these remembers anything in a real sentence. Next week: a real LSTM reads 231 names and learns to invent new ones, and we will meet the problem of training it letter by letter."* Hand out the homework.

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code, in a copy of the shared session. **Paths and the line numbers inside `week11.py` depend on how the blocks were pasted.** Each mistake is deliberate: you plant it, the student reads the traceback aloud, and you refuse to fix it until they have said what the last line means. Four are loud; **three are silent**, and the silent ones teach more.

### How to teach debugging without giving the answer

1. *"Read me the last line."*
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the state is a pair (loud)

```python
# DELIBERATE MISTAKE 1: the LSTM's state is a PAIR (h, c). Only h was handed over.
cell = make_lstm_cell(2.0)
h = torch.zeros(H)
h = cell(x40[0], h)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad1.py", line 4, in <module>
    h = cell(x40[0], h)
  ... frames inside torch (elided) ...
ValueError: LSTMCell: Expected hx[0] to be 1D or 2D, got 0D instead
```

**Read it:** `nn.LSTMCell` opens its state as a pair `(h, c)`. It was handed a single tensor, so it tried to unpack `h` into two pieces and the first piece was a single number (a 0-D value), not a row of 16. **Fix:** `h, c = cell(x, (h, c))`, and start with `(torch.zeros(H), torch.zeros(H))`. The hint is `hx[0]`: the first thing in the state.

### Mistake 2 — `nn.LSTM` returns a pair as its second answer (loud)

```python
# DELIBERATE MISTAKE 2: nn.GRU and nn.RNN hand back h_n, but nn.LSTM hands back the PAIR (h_n, c_n).
lstm = make_layer("lstm")
out, h_n = lstm(torch.randn(5, D))
print("last note:", h_n.shape)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 4, in <module>
    print("last note:", h_n.shape)
AttributeError: 'tuple' object has no attribute 'shape'
```

**Read it:** `nn.RNN` and `nn.GRU` return `(out, h_n)` with `h_n` one tensor, and Week 8 taught `out, h_n = rnn(x)`. For `nn.LSTM` the second answer is **itself** a pair, `(h_n, c_n)`; unpacking into two names works, which is why nothing fails until `h_n.shape` is used on a tuple. **Fix:** `out, (h_n, c_n) = lstm(x)` (or `out, last = lstm(x)` then `h_n, c_n = last`, as block 6 does).

### Mistake 3 — `fill_` on a tracked knob (loud)

```python
# DELIBERATE MISTAKE 3: fill_ on a parameter without no_grad. PyTorch refuses to change a tracked knob behind its back.
lstm = nn.LSTM(D, H)
lstm.bias_ih_l0[H:2 * H].fill_(2.0)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 3, in <module>
    lstm.bias_ih_l0[H:2 * H].fill_(2.0)
RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.
```

**Read it:** the bias is a knob PyTorch is tracking, and `bias[16:32]` is a *view* of it. Changing a tracked tensor in place without telling PyTorch would corrupt the record of how the numbers were made, so it refuses. **Fix:** put the `fill_` lines inside `with torch.no_grad():`, as in blocks 4 and 5. (This is the same `no_grad` the student met for measuring in Level 3; here it means "I am editing, not learning".)

### Mistake 4 — the input was not tracked (loud)

```python
# DELIBERATE MISTAKE 4: the input was not marked requires_grad=True, so x.grad is None.
def reach_bad(layer, T, seed=0):
    torch.manual_seed(100 + seed)
    x = torch.randn(T, D)
    out, last = layer(x)
    out[-1].sum().backward()
    return [row.norm().item() for row in x.grad]

sizes = reach_bad(make_layer("lstm"), 40)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad4.py", line 9, in <module>
    sizes = reach_bad(make_layer("lstm"), 40)
  File "/home/you/l4/bad4.py", line 7, in reach_bad
    return [row.norm().item() for row in x.grad]
TypeError: 'NoneType' object is not iterable
```

**Read it:** `x.grad` is `None` because `x` was never marked `requires_grad=True`, so PyTorch kept no gradient for it, and the loop then tried to go through `None`. **Fix:** `x = torch.randn(T, D, requires_grad=True)` as in block 6. (Note the layer's *knobs* did get gradients; only the input did not. That is why `backward()` itself raised nothing.)

### Mistake 5 — the dial turned on the wrong group (SILENT)

```python
# DELIBERATE MISTAKE 5 (SILENT): the dial was turned on the WRONG GROUP. [0:H] is the INPUT gate, not the forget gate.
def make_layer_wrong(seed, value):
    torch.manual_seed(seed)
    layer = nn.LSTM(D, H)
    with torch.no_grad():
        layer.bias_ih_l0[0:H].fill_(value)               # should have been [H:2 * H]
        layer.bias_hh_l0[0:H].fill_(0.0)
    return layer

def first_over_last(layer, seed):
    sizes = reach(layer, 40, seed)
    return sizes[0] / sizes[-1]

print("T = 40, first word / last word, seeds 0, 1, 2:")
print("  wrong group [0:H]   ", [f"{first_over_last(make_layer_wrong(s, 2.0), s):.1e}" for s in range(3)])
print("  right group [H:2H]  ", [f"{first_over_last(make_layer('lstm', s, 2.0), s):.1e}" for s in range(3)])
print("  no dial at all      ", [f"{first_over_last(make_layer('lstm', s), s):.1e}" for s in range(3)])
```

```text
T = 40, first word / last word, seeds 0, 1, 2:
  wrong group [0:H]    ['1.2e-07', '4.3e-06', '1.9e-07']
  right group [H:2H]   ['5.8e-02', '1.3e-01', '2.2e-01']
  no dial at all       ['2.0e-09', '7.1e-08', '6.8e-09']
```

**Read it:** nothing failed. The bias has four groups of 16 in the order **input, forget, candidate, output**; `[0:16]` is the *input* gate. For seed 0 the wrong group gave `1.2e-07` (a little better than no dial at all, `2.0e-09`), the right group `5.8e-02`: **five orders short of the right answer, and it looks like "it did something"**. **The tell:** compare against the right group and the no-dial row before believing a change. **Fix:** `[H:2 * H]` for the forget group, and check the order against the block-3 slices, which `nn.LSTMCell` already agreed with.

### Mistake 6 — a batch axis that is not what it looks like (SILENT)

```python
# DELIBERATE MISTAKE 6 (SILENT): a batch axis added to x. nn.LSTM reads (1, 40, 4) as ONE step of 40 separate sequences.
torch.manual_seed(100)
x = torch.randn(1, 40, D, requires_grad=True)             # should be (40, 4)
out, last = make_layer("lstm")(x)
out[-1].sum().backward()
sizes = [row.norm().item() for row in x.grad]
print("out shape:", tuple(out.shape), "  x.grad shape:", tuple(x.grad.shape), "  number of 'positions' measured:", len(sizes))
print("first / last:", sizes[0] / sizes[-1])
```

```text
out shape: (1, 40, 16)   x.grad shape: (1, 40, 4)   number of 'positions' measured: 1
first / last: 1.0
```

**Read it:** `(1, 40, 4)` without `batch_first=True` is read as *1 step of 40 separate sequences*, not one sequence of 40 steps. Nothing fails; `out` has shape `(1, 40, 16)`, `x.grad` has one row, and the ratio of a row to itself is `1.0`. **The tell:** a ratio of exactly `1.0`, "no decay at all", is too good to be true, and the number of positions is `1` instead of 40. **Fix:** `torch.randn(40, D, requires_grad=True)` (shape `(T, 4)`), as in block 6.

### Mistake 7 — the forget-bias lines on a layer with no forget gate (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): the same two lines of forget_bias code on a GRU and on a plain RNN. Neither has a forget gate.
for kind in ["rnn", "gru", "lstm"]:
    layer = make_layer(kind, 0, 2.0)
    print(f"  {kind:4s} bias_ih_l0 has {layer.bias_ih_l0.numel()} numbers; the slice [16:32] has {layer.bias_ih_l0[H:2 * H].numel()};",
          "first/last at T = 40, seed 0:", f"{ratio(kind, 40, 0, 2.0):.1e}")
```

```text
  rnn  bias_ih_l0 has 16 numbers; the slice [16:32] has 0; first/last at T = 40, seed 0: 2.0e-10
  gru  bias_ih_l0 has 48 numbers; the slice [16:32] has 16; first/last at T = 40, seed 0: 3.8e-02
  lstm bias_ih_l0 has 64 numbers; the slice [16:32] has 16; first/last at T = 40, seed 0: 5.8e-02
```

**Read it:** `make_layer(kind, 0, 2.0)` runs for all three. For `rnn`, the bias has 16 numbers, so `[16:32]` is **empty**: `fill_` fills nothing and the ratio is the untouched `2.0e-10` (the same as block 7). For `gru`, the slice is the *update* group `z`, which in PyTorch points the *keep* way (`T1`), so it happens to help (`3.8e-02` for seed 0) — **by a different gate than the one we named**. For `lstm` it is the forget gate. **The tell:** `numel()` of the slice. A forget bias on an RNN is a no-op, and on a GRU it is a different dial; a student who reports "the GRU's forget bias" has used the wrong name. **Fix:** only call it a forget bias for the LSTM.

---

## 🎲 The Activity, In Full

### The Dial Grid

**What it is:** a prediction grid and a measurement grid, filled one after the other on workbook page 11.4, plus the seed and dial table on page 11.5. It is the whole experiment in three printed tables.

### Setup (2 minutes, during the live-code segment)

The grid on page 11.4 is blank (4 rows: rnn, gru, lstm, lstm with forget bias 2; 4 columns: `T` = 10, 20, 40, 80), with a second blank copy beside it for the *measured* values. Two pens of different colours: predictions in one, measurements in the other.

### The rules, read out loud before the first cell

1. **Predict all 16 cells before running anything.** One letter each: **T** (below `1e-6`), **S** (`1e-6` to `1e-2`), **L** (above `1e-2`).
2. **Copy each measured number in full, exponent included.** `2.05e-09` is `0.00000000205`; a dropped exponent changes the answer by a factor of a billion.
3. **Colour in which predictions were right.** The score is not the point; the *pattern* of the misses is.

### The measured grid

The student's second table, so you can check it (block 6 for the first three rows, block 7 for the fourth; the letter is what the cut-offs give):

| | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| rnn | 6.72e-03 (S) | 1.77e-05 (S) | 1.99e-10 (T) | 6.48e-20 (T) |
| gru | 2.84e-02 (L) | 1.49e-04 (S) | 1.36e-08 (T) | 6.71e-18 (T) |
| lstm | 7.65e-03 (S) | 2.53e-04 (S) | 2.05e-09 (T) | 6.64e-16 (T) |
| lstm, forget bias 2 | 3.54e-01 (L) | 3.10e-01 (L) | 5.77e-02 (L) | 3.37e-02 (L) |

(The cut-offs are ours, not nature's: `1.77e-05` is S although it is already small. **The honest teaching line:** *"read the trend along each row, not the letter"*: the first three rows fall by a huge factor along the row; the fourth row barely falls.)

### What "finished" looks like

Sixteen predictions written; sixteen measurements copied; one sentence per row; the seed and dial table (11.5) filled; and the student answers the question that makes the activity: *"did anything learn?"* with *"no, we only looked at the starting point"*.

### Variation — a shorter slot (55 minutes)

Do only the `T = 10` and `T = 40` columns, and **skip the seed lines of block 7** (keep the dial grid). Keep blocks 3 and 4 whole.

### Variation — an anxious or slow student

Fill in the letters for **the rnn row and the bias-2 row only** (the obvious ones); they predict the middle two. Say the rule as *"the number gets small, or stays level"*. For the dial use only bias 0 and bias 2 and the sentence "turning one number stopped the fall".

### Variation — harder (a student who finishes early)

1. **Bias 10.** *"Set the forget bias to 10. What is `sigmoid(10)`? Run the `T = 80` ratio."* (We did not run this; let them find out and report what they measure.)
2. **Find the dial that keeps half.** Section 2's `0.9828`: can they find it to three places with a loop like Week 10's block 1? (`K1` prints `0.983 ** 40 = 0.5037`.)
3. **The GRU's dial.** Which slice of a GRU's bias would they fill, and which sign? (The `z` group, index 1 of `r, z, n`, and `+`, from `T1`; Clinic 7 printed `3.8e-02` at `T = 40`, seed 0. Let them check other seeds themselves.)
4. **400 steps.** `reach(make_layer("lstm", 0, 2.0), 400)`: what does the ratio do? (`T3`: `5.4e-08` at seed 0.)

---

## ❓ Questions Students Ask This Week

**"Why four dials? Why not one?"** The GRU uses two; a simpler cell with one is possible. The LSTM's four were found to work well in the 1990s and 2000s, and the reasons are a design story, not something we tested today. Say that.

**"Why 64 in `(64, 4)`?"** Four groups of 16: the input, forget, candidate and output scores, 16 of each because the memory has 16 numbers.

**"Why does `tanh` appear on `g` and `c`, but `sigmoid` on the dials?"** The dials must be between 0 and 1 (they multiply); the candidate and the note may be positive or negative, between -1 and 1. The sigmoid is a squasher to between 0 and 1, tanh to between -1 and 1. (In the update, `tanh` is on the *candidate* and on the memory as it is read out to make `h`; the old memory is not squashed on its way to the new one.)

**"Why is there no `tanh` on the old memory in `c = f * c + i * g`?"** That is the design: the old memory goes through only a multiplication by `f`. A `tanh` in that path would bring back Week 10's `1 - note squared` factor at every step.

**"Is the forget bias cheating?"** It is a start setting. In real use it is set before training and then the weights can move it. We did not train, so we cannot say what happens next; `T2` (teacher only) shows it helped a default LSTM at `T = 40` and not at `T = 80`.

**"Why did the default LSTM do so badly?"** In `T2`, at `T = 40`, the default GRU and LSTM got `0 of 5` and the plain RNN `4 of 5`. We did not find out why. **Say so.**

**"Is the probe the same as training?"** No. The probe looks at the start of training; `T2` is the only training and it is a toy.

**"Why the ratio `first / last` and not just the first?"** The last word's own pull is different for each layer, so dividing by it puts the three layers on one scale. It is a choice we made.

**"Why is the ratio above 1 at bias 4?"** Block 5 shows `1.08`: the first word mattered slightly more than the last one for that one random input. We did not look into it further.

**"Why not bias 10?"** On a calculator `sigmoid(10)` is `0.99995`: the memory would almost never clear. A design question; we did not test it.

**"Is this why chat models use attention?"** It is part of the story. Attention does not multiply along the sequence at all, and `0.95 ** 400 = 1.2e-09` is why 400 steps is a problem even for a well-set dial. Week 14 makes the argument; today is not a result about chat models.

**"Will my numbers match yours?"** The calculator numbers (`0.1432`, `0.4838`, `0.5037`, `0.8644`) match exactly. The tables should match on the same machine with the same seeds; on another build the second digit of the small numbers may move. The **orders of magnitude** and the shapes will not.

---

## ⚠️ Where This Lesson Goes Wrong

1. **The student writes "LSTMs fix vanishing gradients".** Ask: *"What did the `lstm` row of block 6 say at T = 40?"* (`2.05e-09`, tiny.) *"What did we change in block 7 to get `5.77e-02`?"*
2. **The forget bias is "the trick that makes the LSTM learn".** Nothing was trained. The sentence is "the trick that opens the highway at the start".
3. **The student calls `fill_` without `no_grad`.** Clinic 3. Expect it in the first ten minutes.
4. **Slice indices are copied without thinking.** `[H:2 * H]` is the forget group because of the order *input, forget, candidate, output*. Make them say the four groups, in order, aloud. Clinic 5 is what happens otherwise.
5. **The exponent is dropped.** `2.05e-09` copied as `2.05`. Say it in words.
6. **The hand unit's `c` is read as the note.** The LSTM has *two* numbers per step: `c` (memory) and `h` (the output note). Block 2 prints both; make the student say which column is which.
7. **The student uses the module's GRU equation.** It has `z` the other way round (section 3). Point at `T1`'s first two lines.
8. **`T2` mentioned in class as "proof".** It is a teacher check with a different task, one width, one learning rate, 300 steps. Use it only to stop "the dial makes it learn".
9. **The RNN-versus-LSTM "who is better" argument.** At default settings the probe says they are the same kind of bad, and `T2` says the RNN did better at `T = 40`. Do not referee it; say what each number is.

---

## 🧭 Differentiation

### If the student is struggling

- Do **only the hand unit** (block 2): `0.8909, 0.8486, 0.8084, 0.7701` against `0.7616, 0.3634, 0.1797, 0.0896`, then `0.9526 ** 40 = 0.143` and `0.5 ** 40` on the calculator. The whole idea in three lines.
- Predict T/S/L for **two rows only** (rnn and the bias-2 row).
- Replace the 16-cell grid with a 2 by 2 (`T` = 10, 40; rnn, bias 2): `6.72e-03`, `1.99e-10`, `3.54e-01`, `5.77e-02`.
- For the dial: use block 5's two lines (bias 0 and 2) only. The sentence *"turning one number stopped the fall"* is enough.

### If the student is flying

- **`T1`'s typical slope.** Ask *"what single number per step would give the same fall from the last word to the first?"* (`(first / last) ** (1 / 39)`.) Give nothing beyond that; they can work it out with a calculator.
- **Bias 10 and the GRU slice.** See the harder variation above.
- **The reference module's practice 5.** It asks for `MyLSTMCell(nn.Module)` with one `nn.Linear` and `torch.chunk`; the student has neither `class` nor `chunk` yet (classes are Week 12). Let them wrap `lstm_step` in a function that loops over a sequence instead.
- **`T2`'s puzzle.** Why does the default LSTM fail at `T = 40` when the RNN succeeds? (We do not know; let them propose a test and run it, and report what they measure.)

### If the student won't engage today

Play the Telephone with a number they care about (a rumour, a video, a meme shared at 90% or 110%), then give them the dial: *"what dial leaves half after forty people?"* The Hook is what they need; the code can be block 1 and block 2 printed and read aloud. **Compute their numbers first** (`0.9 ** 40 = 0.0148`, `1.1 ** 40 = 45.26`, both printed by Week 10's `K1`).

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"What is a gate?"** *Pass:* a number between 0 and 1, made by a sigmoid, that multiplies something to say how much gets through. (Not "it decides what is important".)
2. **"Why can the memory track keep things that the RNN's note loses?"** *Pass:* it is updated by *adding*, so the old memory is only scaled by `f`, not pushed through a `tanh` and a weight matrix; the slope back is `f`.
3. **"What is the forget gate at the start, and why does it matter?"** *Pass:* about one half, because the score is near 0; so forty of them leave `9e-13`, like the RNN.
4. **"What does the forget bias do, and what did we show?"** *Pass:* it sets the dial near 1 before training; the ratio went from `1e-9` to `6e-2` at `T = 40`. We did **not** show it makes the model learn.
5. **"Is an LSTM better than an RNN?"** *Pass:* "at default settings, in this probe, no: they vanish the same way; the dial near 1 is what helps". (Bonus: "and I don't know why `T2` disagrees".)

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Says, before running, that default GRU and LSTM will still vanish; explains the dial starting at `0.5`; reports both the `T = 40` success and the `T = 80` failure of the dial without being prompted, and says what was not explained. |
| **3 — Secure** | Writes the step from the equation and checks it against `nn.LSTMCell`; says "add, not rewrite; slope is `f`"; reads the grid in a sentence per row; knows nothing was trained. |
| **2 — Developing** | Gets "the dial near 1 helps"; thinks the LSTM is better by default; needs help with the slice indices. |
| **1 — Not yet** | Thinks "gate" means "chooses what matters". Repeat the Hook (dial at `0.983`, dial at `0.5`) at the start of Week 12, before names. |

---

## 📤 Homework to Assign

The workbook has six pages (11.1-11.6). The student does them in order, and **writes predictions before running anything**.

1. **11.1 Dials by hand** — five sigmoids from the calculator, three `f ** 40` values, and the halving count.
2. **11.2 One unit, by hand** — the hand unit with a new forget dial (`sigmoid(2)`): three steps, memory as a share of step 1, a comparison with a dial of `sigmoid(0)`.
3. **11.3 The cell from scratch** — the `nn.LSTMCell` check: the biggest gap at each of five steps and the sentence "what does a gap of `1e-08` mean".
4. **11.4 The dial grid** — the 16 predictions and the 16 measurements, one sentence per row.
5. **11.5 Three seeds and the forget bias** — the seed table at `T = 40`, the bias sweep at four lengths, and the sentence about what was and was not shown.
6. **11.6 The report** — a short paragraph, every number from their own run in the last 24 hours with the seed stated, and the **Bug Log**: any real error they met, with its last line copied and the fix.

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated.

Estimated time: 60-70 minutes.

---

## 🔑 Answer Key

> **The workbook pages 11.1-11.6 follow this order.** Where an answer is a number it comes from `key.py` (block `K1`), blocks 1-7 of `week11.py`, or the grid above. All were run in the Prep Checklist.

### Page 11.1 — Dials by hand (from `key.py`)

| Part | Question | Answer |
|:--:|---|:--:|
| a | `sigmoid(-2)` | **0.1192** |
| b | `sigmoid(0)` | **0.5000** |
| c | `sigmoid(1)` | **0.7311** |
| d | `sigmoid(3)` | **0.9526** |
| e | `sigmoid(5)` | **0.9933** |
| f | `0.5 ** 40` | **9.095e-13** |
| g | `0.88 ** 40` | **0.0060** |
| h | `0.99 ** 40` | **0.669** |
| i | How many multiplications by `0.95` until the value is first below one half? | **14** (`0.4877`) |

*What to draw out:* **b and f together**: a dial of exactly one half leaves nothing after forty steps. **g and h**: the difference between a dial of `0.88` and `0.99` is `0.006` against `0.67`. *Common errors:* `sigmoid(0) = 0` (it is one half); `0.88 ** 40` rounded to `0.9`; using `e^z` instead of `e^-z` (gives the wrong way round).

### Page 11.2 — One unit, by hand (from `key.py`)

The hand unit of block 2 with the forget dial changed to `sigmoid(2) = 0.8808`, spike `[1, 0, 0]`, `i = sigmoid(5x - 2.5)`, `g = tanh(2x)`, `o = sigmoid(1)`:

| Step | `x` | `i` | `g` | `c` | `h` | `c` as % of step 1 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 1 | 0.9241 | 0.9640 | **0.8909** | 0.5204 | 100.0 |
| 2 | 0 | 0.0759 | 0.0000 | **0.7847** | 0.4791 | 88.1 |
| 3 | 0 | 0.0759 | 0.0000 | **0.6912** | 0.4377 | 77.6 |

Slope back from step 3 to step 1: `f ** 2 = ` **0.7758**. With `f = sigmoid(0) = 0.5` instead: `c = 0.8909, 0.4454, 0.2227`, which is `100.0, 50.0, 25.0` per cent of step 1: **exactly halving, like the RNN's note**. *What to draw out:* at `x = 0`, `i * g = 0.0759 x 0.0000 = 0`, so nothing is added and `c` just shrinks by `f`. *Common errors:* using `tanh` on the old `c` inside the update; adding `h` instead of `c`; using the step-1 `i` at step 2.

### Page 11.3 — The cell from scratch (from block 3)

| Step | biggest gap in `h` | biggest gap in `c` |
|:--:|:--:|:--:|
| 1 | 0.0e+00 | 0.0e+00 |
| 2 | 7.5e-09 | 1.5e-08 |
| 3 | 3.7e-09 | 7.5e-09 |
| 4 | 3.7e-09 | 7.5e-09 |
| 5 | 1.5e-08 | 3.0e-08 |

`allclose`: `True True`. The cell holds `1408` numbers. *Accept* any gap at or below `1e-06` (another CPU may differ in the last digit). *The sentence that earns full marks:* "a gap of about `1e-08` is float rounding, so my step and PyTorch's are the same calculation". *Common errors:* a gap of order `1` (the groups are in the wrong order, usually input and forget swapped; see Clinic 5); passing `h` alone (Clinic 1).

### Page 11.4 — The dial grid

The measured grid is the one in 🎲. The model **sentences**, one per row:

- **rnn:** falls by a huge factor along the row: `6.7e-03` at 10, `2.0e-10` at 40, `6.5e-20` at 80. Vanishing.
- **gru:** the same shape, a little higher at short lengths (`2.8e-02` at 10), still `6.7e-18` at 80. Vanishing.
- **lstm:** the same shape (`7.7e-03` at 10, `6.6e-16` at 80). At default settings, the gates alone did not open the highway.
- **lstm, forget bias 2:** `3.5e-01` at 10 and `3.4e-02` at 80: stays within a factor of 30 of the last word's pull. The dial near 1 is what helped.

*Marking:* full credit for a sentence that gives the **direction** and **one number copied with its exponent**. **Do not score the T/S/L predictions**; look for a student who predicted L for the GRU and LSTM rows and then said what surprised them. *The one sentence that must appear somewhere:* "the gates by themselves did not help at default settings".

### Page 11.5 — Three seeds and the forget bias (from block 7)

**Seeds, `T = 40`, first over last:**

| | seed 0 | seed 1 | seed 2 |
|---|:--:|:--:|:--:|
| rnn | 2.0e-10 | 6.3e-11 | 3.1e-10 |
| gru | 1.4e-08 | 1.5e-09 | 8.9e-10 |
| lstm | 2.0e-09 | 7.1e-08 | 6.8e-09 |
| lstm, forget bias 0 | 9.8e-10 | 4.3e-09 | 4.2e-09 |
| lstm, forget bias 2 | 5.8e-02 | 1.3e-01 | 2.2e-01 |

**The dial, seed 0:**

| forget bias (sigmoid) | `T = 10` | `T = 20` | `T = 40` | `T = 80` |
|---|:--:|:--:|:--:|:--:|
| 0.0 (0.500) | 7.20e-03 | 4.86e-05 | 9.83e-10 | 3.92e-17 |
| 1.0 (0.731) | 1.07e-01 | 2.95e-02 | 3.52e-04 | 1.44e-06 |
| 2.0 (0.881) | 3.54e-01 | 3.10e-01 | 5.77e-02 | 3.37e-02 |
| 4.0 (0.982) | 7.23e-01 | 8.46e-01 | 3.52e-01 | 1.61e-01 |

The sentence that earns full marks: *"With the same weights and seeds, moving the forget bias from 0 to 2 changed the T = 40 ratio from about `1e-09` to about `1e-01`, far more than the spread between seeds; I did not train anything, so this is about the starting point, not learning."* **Also accept** "the dial opens the highway at the start". *Common errors:* "the LSTM is better than the GRU" from three seeds (the gaps are small); "the LSTM learns longer sequences" (nothing was trained).

### Page 11.6 — The report (model answer and rubric)

Model: *"With seed 0 and T = 40, the pull of the first word as a fraction of the last word was 1.99e-10 for an RNN, 2.05e-09 for an LSTM at default settings, and 5.77e-02 for an LSTM with the forget bias set to 2. An LSTM adds to its memory, so the slope back is the forget gate, and the gate starts near one half; setting its bias to 2 makes it 0.88. I measured an untrained layer on random numbers, so this does not show that the LSTM learns long memories."*

| Criterion | Marks |
|---|:--:|
| Two numbers **with exponents**, from their own run, seed stated, one default and one with the forget bias | 2 |
| States the cause in one sentence (the memory is updated by adding; the slope is the forget gate) | 1 |
| States that at default settings the gates alone did not help, or that the dial starts near one half | 1 |
| States what was **not** shown: nothing was trained | 2 |

A write-up that says "the LSTM solves vanishing gradients" loses the last two marks regardless of the rest. **Bug Log:** any real entries are fine if the **last line** of the traceback (not the whole) was copied and the fix works.

### Teacher-only: the Clinic, at a glance

| # | Loud / silent | Last line (or tell) | One-line fix |
|:--:|:--:|---|---|
| 1 | loud | `ValueError: LSTMCell: Expected hx[0] to be 1D or 2D, got 0D instead` | `cell(x, (h, c))` |
| 2 | loud | `AttributeError: 'tuple' object has no attribute 'shape'` | `out, (h_n, c_n) = lstm(x)` |
| 3 | loud | `RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.` | `with torch.no_grad():` around `fill_` |
| 4 | loud | `TypeError: 'NoneType' object is not iterable` | `torch.randn(T, D, requires_grad=True)` |
| 5 | **silent** | wrong group gives `1.2e-07`, right group `5.8e-02` | `[H:2 * H]` |
| 6 | **silent** | `number of 'positions' measured: 1`, ratio `1.0` | input shape `(T, 4)` |
| 7 | **silent** | `rnn` slice has 0 numbers; `gru` slice is the update gate | only call it a forget bias for the LSTM |

### Answers to every question posed in the lesson

| Question | Answer |
|---|---|
| Forty people each pass on 95%: how much arrives? | `0.1285`, about 13% (Week 10). |
| Which constant dial leaves half after 40 people? | About `0.983` (`0.983 ** 40 = 0.5037`; `0.982` gives `0.4836`). |
| And a dial of 0.5? | `9.1e-13`. |
| What is `sigmoid(0)`? | `0.5`. |
| What does the memory update look like? | `c = f * c_old + i * g`: scale the old, add the new. |
| Slope of the memory with respect to the old memory? | `f` (when the dials look only at the input: block 4). |
| Slope back forty steps at `f = 0.9526`? | `0.1432` (`0.143`). |
| What sets `f` at the start of training? | The bias and the (small) weights: a score near 0, so `f` near `0.5`. |
| How many numbers in an LSTM with 4 inputs and 16 memory? | `1408` (against the RNN's `352`). |
| If every dial is 0.5, left after 10 steps? | `0.000977` (`0.5 ** 10`, by calculator). |
| Block 2: what share of step 1 is left after 4 steps, LSTM vs RNN? | `86.4%` against `11.8%`. |
| Block 3: what does a gap of `1e-08` mean? | Float rounding: the two steps are the same calculation. |
| Block 3: why is the shape `(64, 4)`? | Four groups of 16 scores for a 4-number input. |
| Block 4: is the slope back the forget dial? | Yes, to `6.0e-08`, when the recurrent weights are zero. |
| Block 4: vanishing or exploding? | Vanishing (`2.15e-10` against `1.82`): `f` was about one half. |
| Block 5: which bias made the ratio `0.22`? | Forget bias 2. |
| Block 6: did the gates help at default settings? | A little in the GRU at short lengths; at `T = 40` all three are tiny. |
| Block 6: why `352, 1056, 1408`? | One, three and four groups of scores. |
| Block 7: which difference is bigger, seeds or dial? | The dial (seven orders against one to two). |
| Did anything learn today? | No. Nothing was trained. |
| Does a bias of 2 make the LSTM learn at `T = 80`? | We do not know; the teacher check `T2` says no, `0 of 5`, and we did not explain why. |
| What did we **not** do today? | Train anything, or show a gated cell remembers in a real sentence. |

---

## 🔮 Next Week Preview

**Week 12 — Teach a Network to Invent Names** (🟩 lab). Today's LSTM was never trained. Next week it reads **231 typed names** and learns to write new ones. Two new ideas: training feeds the **true** previous letter (teacher forcing) and runs the whole name at once, while generating feeds back the layer's **own** guess and must run one letter at a time. The new syntax is `F.cross_entropy(..., ignore_index=)` (so padding is not counted), `torch.cat` (already met in Level 3) and `torch.full`. The student trains the character model, reports train against validation loss, and measures what fraction of generated names already exist in the training list.

**What from today carries over:** `nn.LSTMCell`/`nn.LSTM` and the pair `(h, c)` (the state as a pair, Clinics 1 and 2, is needed again when the cell is put inside a model), and the sentence **"an LSTM has a highway; whether it is open at the start depends on where the dial is set"**. **If page 11.4 is blank, do it before Week 12.**
