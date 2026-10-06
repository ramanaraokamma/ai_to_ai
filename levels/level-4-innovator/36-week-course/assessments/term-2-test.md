# 📝 Term 2 Test — Weeks 10–17: Memory, Then Attention

[⬅ Course home](../README.md) · [⬅ Term 1 test](term-1-test.md) · Term 2 of 4 · covers Weeks 10–17 (Week 18 is the review week)

---

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │   AI ACADEMY · LEVEL 4 INNOVATOR                                     │
   │   TERM 2 TEST — Memory, Then Attention                               │
   │   Covers Weeks 10–17. Nothing later appears anywhere on this test.   │
   │                                                                      │
   │   PART 1 · THE PAPER           70 minutes      75 marks              │
   │   PART 2 · THE DEMO            15 minutes      15 marks              │
   │                                                                      │
   │   Section A   20 multiple choice          1 mark each     20 marks   │
   │   Section B    8 "what does this print"   2 marks each    16 marks   │
   │   Section C    4 "find the bug"           3 marks each    12 marks   │
   │   Section D    3 "do the arithmetic"      5 marks each    15 marks   │
   │   Section E    1 longer question on real tables           12 marks   │
   │                                                                      │
   │   PART 1:  ⛔ NO COMPUTER.   ✅ A CALCULATOR, YES.                  │
   │   PART 2:  ✅ A COMPUTER AND YOUR OWN WEEK 10–17 FILES. NO NETWORK. │
   │                                                                      │
   │      This is the term of exponents and tables of weights. Check     │
   │      NOW that your calculator has an e^x key and a y^x key (a       │
   │      "power" key). A missing button costs real marks.               │
   │                                                                      │
   │   SUGGESTED TIME   A 15 · B 15 · C 12 · D 15 · E 13 minutes         │
   │                                                                      │
   │   INSTRUCTIONS FOR THE PAPER                                         │
   │   · Pencil. Answer every question. "Don't know" is allowed and       │
   │     costs nothing extra; a blank tells nobody anything.              │
   │   · Section A: circle ONE letter. If you guessed, write "not sure".  │
   │   · Section B: write EVERY line the program prints, in order.        │
   │     Shapes are written with brackets: (4, 3).                        │
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
> **What this file is.** The Week 18 review week already contains a paper (in that week's own guide).
> **This is a second paper of the same shape with every number and every question different**, a fresh
> item on each topic, no question repeated. Use it as the formal Term 2 test, as the re-sit after the
> remediation fortnight, or as practice. It is **not** a replacement: the Week 18 paper is the one the
> student self-marks. Week 18 is the review week, so this test covers Weeks 10–17.
>
> **You do not need to know Python, calculus or machine learning to run or mark this.** The answer key
> at the bottom gives every answer, every piece of working, and the *real printed output* of every code
> block. Compare, do not work out.
>
> **What "real" means here.** Every code block on this file, on the paper and in the key, was run from a
> scratch folder on a CPU, one thread (`torch.set_num_threads(1)`), Python 3.10.10, torch 2.2.1,
> numpy 1.26.4, with the seeds shown, and the output pasted in unedited (tracebacks only have the file
> path shortened). Weeks 14–17 code came from the course's own student guides (Week 17's `tinygpt.py`
> was extracted from the guide and run unchanged), with the course's `l4lib/` folder on the path. **The
> two tables in Section E are printed numbers: print them, do not regenerate them on the day.** On a
> different CPU or torch build the last digit of a loss, or the second digit of a very small gradient
> like `2.5e-06`, can move; the size of every number will not.
>
> **There is no language model, no scripted backend and no stand-in anywhere on this test.** Nothing
> here is a "stand-in, not a model", because Term 2 never uses one; the first scripted backend arrives in
> Week 23. Every network on this test is real PyTorch. The layers in Section E Table 2 are *untrained*
> (seeded random numbers), and the paper says so. The Section E Table 1 model is a real, small TinyGPT
> trained for 700 steps.
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

**A1.** [W10] Fifty people stand in a line. Each one passes on 98% of what they heard and loses 2%. About how much of the original message reaches the fiftieth person?

- (a) None: fifty losses of 2% add up to all of it
- (b) About 0.36, just over a third
- (c) About 0.98
- (d) About 0.02

---

**A2.** [W10] You measure the gradient at position 1 for a cell whose recurrent weights are made 8 times bigger, on five seeds. Four seeds give huge numbers (`4.4e+03`, `8.8e+04`, `9.7e+05`, `1.1e+05`). One seed gives `5.5e-07`. The most honest reading is:

- (a) The fifth seed has a bug in the probe
- (b) Bigger recurrent weights always explode
- (c) On these five seeds, bigger weights usually explode but not always, so "bigger recurrent weights explode" is a tendency, not a law
- (d) Clipping made the fifth seed vanish

---

**A3.** [W10] What does `h.retain_grad()` do, and where does it go?

- (a) It keeps the gradient of the in-between value `h`, so `h.grad` is filled in after `backward()`; it goes before `backward()`
- (b) It turns `h` into a knob that the optimizer updates
- (c) It clips `h`'s gradient to length 1
- (d) It stops the gradient flowing through `h`

---

**A4.** [W11] In an LSTM the memory is updated as `c = f * c_old + i * g`. Suppose the forget dial is exactly `f = 1.0` and the input dial is exactly `i = 0.0` at every one of 40 steps. After 40 steps `c` is:

- (a) Zero
- (b) Half of its starting value
- (c) Replaced by the candidate `g`
- (d) Exactly what it was at the start

---

**A5.** [W11] You write `out, last = nn.LSTM(4, 16)(x)` for an input `x` of shape `(5, 4)`. What is `last`?

- (a) One tensor, the final note `h_n`
- (b) A pair: the final note `h_n` and the final memory `c_n`
- (c) The memory `c_n` only
- (d) The last row of `out`

---

**A6.** [W11] Week 11 compared untrained layers and found that an LSTM with forget bias 2 keeps far more of the first word's pull at `T = 40` than the same LSTM with bias 0, on three seeds. Which sentence is **not** supported by that table?

- (a) The bias-2 and bias-0 rows are many orders of magnitude apart
- (b) With bias 0 the forget dial starts at `0.5`
- (c) A trained LSTM that starts from bias 2 will remember the first word of a sentence
- (d) Three seeds show the bias matters far more than the seed does

---

**A7.** [W12] Training a name model can push every letter of a name through at once, but generating a name must go one letter at a time. Why?

- (a) In training every input letter is the true previous letter, so it exists before the model runs; in generating, the next input is the model's own last pick, which does not exist until it is made
- (b) Generating uses a bigger model
- (c) Dropout is on during generating and off during training
- (d) The model has no memory during training

---

**A8.** [W12] What happens to a name model's printed loss if the padding targets are **counted** in the average instead of ignored?

- (a) The model becomes better at names
- (b) The printed loss looks lower, because padding is an easy guess, although the model has not learned one more letter
- (c) The printed loss goes up
- (d) Nothing; padding has no targets

---

**A9.** [W12] A name model writes 200 names. None of the 200 is in the held-back list of 31 names. Which conclusion is fair?

- (a) The model never copies
- (b) The model is inventing completely new names
- (c) The model is broken
- (d) 31 held-back names is too few to build a story on; a model that copies its *training* list would also show zero

---

**A10.** [W13] A programmer sets the temperature to exactly `T = 0.0` "to make the sampler greedy". What happens?

- (a) It becomes exactly greedy
- (b) It behaves like `T = 1`
- (c) Dividing by zero makes the scores `inf` or `nan`, and `torch.multinomial` stops with a `RuntimeError`
- (d) It always picks the last letter

---

**A11.** [W13] The sorted chances are `0.8, 0.1, 0.06, 0.04` and `p = 0.5`. With the correct top-p test ("keep a letter if the total of the letters ranked **above** it is still below `p`"), which letters are kept?

- (a) All four
- (b) Only the top letter
- (c) The top two
- (d) None: the top letter alone is already above `0.5`

---

**A12.** [W13] A name model scores `0.954` per letter on the real names and `1.122` on the names it generated itself at `T = 1`. A classmate says "this proves exposure bias". The best reply is:

- (a) Yes, the gap is exactly exposure bias
- (b) No, the numbers are too close to tell apart
- (c) No, because a model cannot score its own names
- (d) It fits exposure bias, but plain sampling of unlikely letters and reciting the training list fit the same number, so it is evidence, not proof

---

**A13.** [W12] In `F.cross_entropy(scores.reshape(-1, VOCAB_SIZE), targets.reshape(-1))`, what does the `-1` do?

- (a) It tells PyTorch to work that number out itself, here names × steps
- (b) It counts from the end of the tensor
- (c) It flips the sign of the loss
- (d) It tells the loss to ignore padding

---

**A14.** [W14] A soft lookup gives weights that are never negative and add up to 1, and blends the values `10, 50, 30`. Which answer is **impossible**?

- (a) `20`
- (b) `42.77`
- (c) `55`
- (d) `10`

---

**A15.** [W14] A programmer turns a `3 x 3` table of scores into weights with `e = np.exp(scores)` and `weights = e / e.sum()`. What is wrong?

- (a) Nothing; that is the softmax
- (b) Every row now adds to 3
- (c) It raises an error
- (d) The nine weights together add to 1, so no single row does; each row needs its own total

---

**A16.** [W15] Two independent wobbles have spreads `6` and `8`. The spread of their sum is:

- (a) `10`
- (b) `14`
- (c) `7`
- (d) `48`

---

**A17.** [W15] The river question had scores `0.1, 2.0, 0.3`. Shout it ten times louder (`1, 20, 3`) and take the softmax. The weights are now:

- (a) Still about `0.112, 0.751, 0.137`
- (b) `0.000000, 1.000000, 0.000000`: the soft lookup has frozen into the hard lookup
- (c) All equal
- (d) Negative

---

**A18.** [W15] To hide the future, a programmer fills the hidden scores with `0.0` **before** the softmax (not `-inf`). What happens?

- (a) The hidden words get exactly weight `0`
- (b) The rows no longer add to 1
- (c) The hidden words still get a real share of the weight, because `e` to the power `0` is `1`
- (d) The program raises an error

---

**A19.** [W16] A module holds `nn.Linear(3, 3)` and a registered buffer `mask` of shape `(3, 3)`. How many knobs does `sum(p.numel() for p in model.parameters())` count?

- (a) 21
- (b) 12
- (c) 9
- (d) 3

---

**A20.** [W17] A text has 100 characters and a window is `T = 10` long. The target window is the input window moved one place right, so a start `s` needs `text[s + 1 : s + T + 1]` to exist. What goes in `torch.randint(?, (B,))` for the starts?

- (a) `90`
- (b) `100`
- (c) `89`
- (d) `91`

---

# 🅱️ Section B — What Does This Print?

*8 questions · 2 marks each · write EVERY line the program prints, exactly. Rounding is done inside the code. Each snippet is separate and imports what it needs.*

---

**B1.** [W10]

```py
rate = 1.5
value, k = 1.0, 0
while value < 10:
    value = value * rate
    k = k + 1
print(k, round(value, 2))
```

---

**B2.** [W12]

```py
import torch
data = torch.zeros(6, 9, dtype=torch.long)
start = torch.full((6, 1), 27)
inputs = torch.cat([start, data[:, :-1]], dim=1)
print(tuple(start.shape), tuple(data[:, :-1].shape), tuple(inputs.shape))
print(inputs[0, 0].item(), inputs[0, 1].item())
```

---

**B3.** [W11] Three lines are printed.

```py
f, i, g = 0.9, 0.2, 0.5
c = 2.0
for _ in range(3):
    c = f * c + i * g
    print(round(c, 3))
```

---

**B4.** [W11] Two lines are printed. (The second is a count: `4 x (7x3 + 7x7 + 7 + 7)`.)

```py
import torch
import torch.nn as nn
torch.manual_seed(0)
layer = nn.LSTM(3, 7)
out, (h_n, c_n) = layer(torch.randn(6, 3))
print(tuple(out.shape), tuple(h_n.shape), tuple(c_n.shape))
print(sum(p.numel() for p in layer.parameters()))
```

---

**B5.** [W17]

```py
import torch
text = torch.arange(100, 110)
s = 6
x = text[s:s + 4]
y = text[s + 1:s + 5]
print(x.tolist())
print(y.tolist())
```

---

**B6.** [W13] Two lines are printed.

```py
import torch
import torch.nn.functional as F
scores = torch.tensor([4.0, 0.0])
for T in [1.0, 2.0]:
    print(round(F.softmax(scores / T, dim=-1)[0].item(), 2))
```

---

**B7.** [W15] You may round the numbers in the tensors to 2 decimal places.

```py
import torch
import torch.nn.functional as F
s = torch.tensor([[1.0, 5.0], [2.0, 2.0]])
v = torch.tensor([[10.0], [20.0]])
mask = torch.tril(torch.ones(2, 2))
w = F.softmax(s.masked_fill(mask == 0, float("-inf")), dim=-1)
print(w)
print(w @ v)
```

---

**B8.** [W16] Three lines are printed.

```py
import torch
import torch.nn as nn
x = torch.zeros(3, 10, 12)
print(tuple(x.view(3, 10, 4, 3).transpose(1, 2).shape))
print(torch.arange(2, 6).tolist())
pos = nn.Embedding(10, 12)
print(tuple((x + pos(torch.arange(10))).shape))
```

---

# 🅲 Section C — Find and Fix the Bug

*4 questions · 3 marks each · for each: **(i)** what is wrong · **(ii)** what happens when it runs (an error, with what its last line means in plain words, or a silent wrong result) · **(iii)** the fixed line. The programs are **deliberately** broken.*

---

**C1.** [W10] The programmer wants the recurrent gradient's length to be **at most 1.0** before the step. The program prints one number. (You cannot work out the exact number from the code; say what is wrong.)

```py
# DELIBERATE: this program has a bug. Find it.
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Linear(2, 1)
x = torch.tensor([[1000.0, 1000.0]])
nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
model(x).sum().backward()
print(round(model.weight.grad.norm().item(), 1))
```

The program prints:

```text
1414.2
```

---

**C2.** [W11] The programmer wants the forget-bias group of an `nn.LSTM` set to 2 before any training.

```py
# DELIBERATE: this program has a bug. Find it.
import torch.nn as nn
H = 16
lstm = nn.LSTM(4, H)
lstm.bias_ih_l0[H:2 * H].fill_(2.0)
print("forget bias set")
```

The program prints:

```text
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 5, in <module>
    lstm.bias_ih_l0[H:2 * H].fill_(2.0)
RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.
```

---

**C3.** [W13] The programmer wants to draw ONE letter, then EIGHT letters, from five chances.

```py
# DELIBERATE: this program has a bug. Find it.
import torch
torch.manual_seed(0)
p = torch.tensor([0.5, 0.3, 0.1, 0.06, 0.04])
print(torch.multinomial(p, 1).item())
print(torch.multinomial(p, 8).tolist())
```

The program prints:

```text
1
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 6, in <module>
    print(torch.multinomial(p, 8).tolist())
RuntimeError: cannot sample n_sample > prob_dist.size(-1) samples without replacement
```

---

**C4.** [W15] The programmer wants the first row of the weights to be exactly `[1, 0, 0]` (the first word may read only itself), and the first row's hidden entries to add to zero. The program prints:

```py
# DELIBERATE: this program has a bug. Find it.
import torch
import torch.nn.functional as F
scores = torch.tensor([[2.0, 0.0, 1.0],
                       [0.0, 2.0, 1.0],
                       [1.0, 1.0, 1.0]])
future = torch.tril(torch.ones(3, 3)) == 0
weights = F.softmax(scores.masked_fill(future, 0.0), dim=-1)
print(weights)
print(weights[0, 1:].sum().item() == 0.0)
```

```text
tensor([[0.7870, 0.1065, 0.1065],
        [0.1065, 0.7870, 0.1065],
        [0.3333, 0.3333, 0.3333]])
False
```

---

# 🅳 Section D — Do the Arithmetic

*3 questions · 5 marks each · a calculator is expected · show every line of working · carry FOUR decimal places and round only at the end.*

---

**D1.** [W14, W15] One pass of attention on three words, with invented numbers. Nothing is learned here.

```text
   p = [ 1,  0]        Wq = identity         Wk = identity         Wv = [[2, 0],
   q = [ 0,  1]                                                         [0, 1]]
   r = [ 1, -1]

   Use:  e^1 = 2.7183   e^-1 = 0.3679   e^2 = 7.3891      (for parts b and c)
         e^0.7071 = 2.0281   1 / sqrt(2) = 0.7071         (for part e)
```

**(a)** Write `V`, the three value rows. *(1)*
**(b)** Write the three scores for the word **r** (its question against each word's label, no divide, no mask). *(1)*
**(c)** Turn the three scores into weights (show the exponentials and their total). The weights must add to 1. *(1)*
**(d)** Write the blended output for **r**, to four places. *(1)*
**(e)** Now switch **both** dials on for the word **q** only: divide the scores by `sqrt(2)`, and hide the future (q may read only p and q). Write the two weights, and the words q gives weight to. *(1)*

---

**D2.** [W10, W11] An LSTM's forget *score* is `2.5`. Use `e^-2.5 = 0.0821`.

**(a)** Write the forget dial `f = 1 / (1 + e^-2.5)`. *(1)*
**(b)** The slope back through the memory track is `f` at every step. By how much is the signal multiplied over **25** steps back? Show the working. *(1)*
**(c)** A dial of `0.5` (score 0) over 25 steps? Write it in `e` notation. *(1)*
**(d)** How many times more signal survives 25 steps with the dial from (a) than with `0.5`? *(1)*
**(e)** With the dial from (a), after how many multiplications does the signal first fall below one half? *(1)*

---

**D3.** [W16, W17] A tiny GPT: vocabulary `20`, width `d = 10`, `2` heads, room for `16` places, `3` blocks. Count the knobs. Use the Week 16 rules: `Linear(a, b)` is `a x b + b` (no `+ b` if `bias=False`), `LayerNorm(d)` is `2 x d`, `Embedding(V, d)` is `V x d`, `GELU` is nothing. In one block: two `LayerNorm(10)`; `q`, `k`, `v` each `Linear(10, 10, bias=False)`; `proj = Linear(10, 10)`; `up = Linear(10, 40)`; `down = Linear(40, 10)`. The causal mask is a buffer and is not counted.

**(a)** The two layer norms *(1)*. **(b)** Attention: `q`, `k`, `v` and `proj` *(1)*. **(c)** The MLP: `up` and `down` *(1)*. **(d)** One whole block *(1)*. **(e)** The whole model: `tok` (one row per character), `pos` (one row per place), the 3 blocks, one final `LayerNorm(10)`, and a `head = Linear(10, 20)` *(1)*.

---

# 🅴 Section E — Reading Real Tables

*1 question with three parts · 12 marks · the numbers are real · quote them.*

**Loss** here is the average surprise (`-ln` of the chance given to the true next letter). A model that knows nothing about 28 characters scores `ln 28 = 3.332`.

**Table 1 (Week 17).** A **reduced** TinyGPT, built from Week 17's `tinygpt.py` with width 64 and 2 blocks: 107,420 knobs. It was trained for 700 steps on the same 6,972 typed characters. The last tenth (698 characters) is held back for validation. Each loss is an average of 20 random windows. "Real words" is the share of words in a 1,000-character sample that appear in the typed text.

```text
step            0     100     200     300     400     500     600     699
train       3.331   2.157   1.980   1.870   1.791   1.743   1.719   1.728
val         3.334   2.118   1.978   1.899   1.832   1.761   1.767   1.772

real words at step 699: 26%          training characters: 6,274
107,420 knobs                        about 15 ms per training step

Three models that only count, scored on the same validation text:
    knows nothing (uniform)    3.332
    knows letter frequencies   2.855
    knows the previous letter  2.033

For comparison, Week 17's full-size run (807,196 knobs, 1,500 steps):
    train 0.894   val 1.437   gap 0.543   real words 60%
```

**E(a)** *(4 marks, 1 each)*
**(i)** Work out the gap (val minus train) at step 699, and say at which printed step the validation loss is lowest.
**(ii)** At step 100 the validation loss is *lower* than the train loss. Is that a bug? Give a reason in one sentence.
**(iii)** By how much does the step-699 validation loss beat the "previous letter" counter?
**(iv)** Week 17's full-size run has a gap of `0.543`; this run has a much smaller one. A classmate says "fewer knobs per character is why". Work out the knobs per training character for both runs (Week 17's run has `807,196` knobs) and say one thing this comparison does **not** let you claim.

**Table 2 (Week 11).** **Untrained** layers (seeded random numbers), width 16, inputs of 4 random numbers per step. For each layer: how much does the end of a 30-step sequence care about the **first** word, as a fraction of how much it cares about the **last** word? Seeds 3, 4 and 5. The "forget bias" is a number written into the LSTM before any training. The dial is `1 / (1 + e^-bias)`.

```text
T = 30, first word / last word, seeds 3, 4, 5:
  rnn                   ['9.7e-08', '4.8e-11', '1.3e-08']
  gru                   ['8.5e-07', '3.5e-06', '2.1e-07']
  lstm, forget bias 0   ['2.5e-06', '1.4e-07', '1.7e-06']
  lstm, forget bias 1   ['4.9e-03', '2.0e-03', '1.6e-03']
  lstm, forget bias 3   ['3.8e-01', '2.3e-01', '4.5e-01']

the dial for bias 0, 1, 3:  0.500, 0.731, 0.953

one more: lstm with forget bias 3, seed 3, at T = 30 and T = 60:
                        ['3.8e-01', '1.7e-01']
```

**E(b)** *(4 marks, 1 each)*
**(i)** For seed 3, about how many **powers of ten** apart are the bias-0 and bias-3 LSTM rows?
**(ii)** Which rows' ranges (smallest to largest of the three seeds) **overlap**: `rnn` and `lstm, forget bias 0`, or `gru` and `lstm, forget bias 0`? What does that let you say, and not say, about which is better?
**(iii)** The dial for bias 3 is `0.953`. Work out `0.953` multiplied by itself 30 times, and say whether the three bias-3 numbers at `T = 30` are in the same neighbourhood.
**(iv)** For the last line, write how many times smaller the number got when the sequence went from 30 to 60 steps, and say whether that is "level" or "falling".

**E(c)** *(4 marks)* A classmate says: *"Table 2 proves an LSTM remembers the first word of a 60-word sentence, so we don't need to worry about forgetting."* Write a reply of three or four sentences that (1) says one thing the table **does** support, with a number; (2) says what the numbers in the table measure and what they do **not** (think about what was trained, what the inputs were, what the score was); (3) says what the three seeds tell you about whether the bias or the seed matters more; and (4) names one more run you would want before saying more.

---

# 💻 PART 2 — THE DEMO

**15 minutes · 15 marks · a computer, your own Week 10–17 files, and the `l4lib` folder. No network, no chatbot.**
*Teacher: sit beside the student. The marks are for what you **watch** and **hear**, so keep the checklist in the marking scheme next to you.*

Open a terminal in the `36-week-course/` folder. Run `export PYTHONPATH="$PWD"` once. Copy your Week 17 `tinygpt.py` next to the demo files. Each demo is a new file. **Say your prediction out loud before you run anything.** A prediction you make after seeing the output does not count.

**Demo 1 — "Check my hand arithmetic" · 5 marks · Weeks 10 and 11**
Write `demo1.py`. **(i)** With a loop and `math.exp`, print the dial `f` for a forget score of `2.5`, `f ** 25`, and `0.5 ** 25`; then, with a `while` loop, the number of multiplications before the signal first falls below one half. These must match your **D2**. **(ii)** Print the three values of `c` from **B3** (`f, i, g = 0.9, 0.2, 0.5`, start `c = 2.0`). **(iii)** Build an `nn.LSTMCell(4, 16)`, set the forget group of its two biases to `2.0` and `0.0` (the right way, inside `torch.no_grad()`), and print the forget dial of the first three units from the **biases alone**, and that dial multiplied 40 times. Say in one sentence what this shows **and does not show**.

**Demo 2 — "The same pass, three ways, two dials" · 5 marks · Weeks 14 and 15**
Write `demo2.py`. **(i)** Compute **D1** for all three words with numpy, and again with torch (`F.softmax`, `transpose(-2, -1)`). Print the row for **r** from each, and whether the two agree. They must match your **D1 (d)**. **(ii)** Switch both dials on in torch (divide by `sqrt(2)`, `masked_fill` with `-inf` before the softmax). Print the weights and output for **q**: they must match **D1 (e)**. **(iii)** Change **only the last word** to `[5, -3]` and print, for each of the three rows, whether its output moved. Predict all three answers first, and say what the result tells you about the mask.

**Demo 3 — "Count it, then let the machine count it" · 5 marks · Weeks 16 and 17**
Write `demo3.py`. Build your own `TinyGPT(20, 10, 2, 3, 16)` (vocabulary 20, width 10, 2 heads, 3 blocks, 16 places) with `torch.manual_seed(0)` set **first**. Print the knobs of `tok`, `pos`, `blocks`, `ln_f` and `head`, and the total. The total must match your **D3 (e)**. Then draw a batch of random ids with `torch.randint`, score it, and print `ln(20)`, the first loss, and the distance between them. Finally print whether any parameter has shape `(16, 16)`, and which entries of `state_dict()` end in `mask`. Say out loud what the distance check is for, and why the mask is in the second list but not the first.

*End of Part 2.*

---

# 📊 MARKING SCHEME

**Paper: 75 marks. Demo: 15 marks. Report them separately.** The paper is "can you run code and arithmetic in your head", the demo is "can you prove it on a machine, in front of someone". A student who is strong on one and weak on the other has told you something that one sum would hide.

> **Mark Section A first.** It is fast, and the pattern of wrong answers tells you where to look in the rest.
> Below each answer in the key is a sentence on why the wrong options were tempting.

## Section A — 20 marks

| Q | Ans | Week | | Q | Ans | Week |
|:--:|:--:|:--:|---|:--:|:--:|:--:|
| A1 | **b** | W10 | | A11 | **b** | W13 |
| A2 | **c** | W10 | | A12 | **d** | W13 |
| A3 | **a** | W10 | | A13 | **a** | W12 |
| A4 | **d** | W11 | | A14 | **c** | W14 |
| A5 | **b** | W11 | | A15 | **d** | W14 |
| A6 | **c** | W11 | | A16 | **a** | W15 |
| A7 | **a** | W12 | | A17 | **b** | W15 |
| A8 | **b** | W12 | | A18 | **c** | W15 |
| A9 | **d** | W12 | | A19 | **b** | W16 |
| A10 | **c** | W13 | | A20 | **a** | W17 |

No half marks. Two letters circled scores 0. A guess marked "not sure" that is right still scores 1; count the "not sure" ones separately, because a student who is right and knows they are unsure needs a different conversation from one who is wrong and sure.

## Section B — 16 marks

**2 marks for every snippet exactly right. 1 mark if the idea is right and one digit, bracket or sign is wrong. 0 otherwise.** Count lines: a correct first line and a missing second line is 1. Tensors may be rounded to 2 places and written with or without the word `tensor`.

| Q | Exact output | The trap |
|:--:|---|---|
| B1 | `6 11.39` | Stopping at `5` (`1.5^5 = 7.59` is still below 10, so the loop goes round once more), or writing `10`. The loop stops after it has gone **past** the target. |
| B2 | `(6, 1) (6, 8) (6, 9)` · `27 0` | `(6, 9)` for the middle one (forgetting that `[:, :-1]` drops the last column). Writing `0 0` for the second line: the first input of every row is the start token `27`, and the second is the first true letter, here `0`. |
| B3 | `1.9` · `1.81` · `1.729` | Writing `1.900` (Python prints `1.9`). Writing `2.0` three times, or `1.9, 1.8, 1.7` (subtracting instead of multiplying). The fixed amount `i * g = 0.1` is added **after** the keep. |
| B4 | `(6, 7) (1, 7) (1, 7)` · `336` | `h_n` as `(7,)` or `(6, 7)` (it is one final note, with the leading `1`). `c_n` missing. For `336`: using 3 groups (a GRU, `252`) or 1 (an RNN, `84`). It is four groups of `7x3 + 7x7 + 7 + 7 = 84`. |
| B5 | `[106, 107, 108, 109]` · `[107, 108, 109]` | Writing four numbers for `y`. The start `6` is one too high, because `text` only has indices up to `109`; the slice stops quietly at the end, so `y` is **short**, with no error. |
| B6 | `0.98` · `0.88` | `0.98` and `0.98` (forgetting to divide by `T`), or `0.98` and `0.5`. `softmax([4, 0])` is `0.9820`; `softmax([2, 0])` is `0.8808`. |
| B7 | `[[1.00, 0.00], [0.50, 0.50]]` · `[[10.], [15.]]` | Giving row 1 of the weights as `[0.05, 0.95]` (the score `5` is in the **hidden** place, so it is gone). Row 2 has equal scores, so equal weights. The output is `0.5 x 10 + 0.5 x 20 = 15`. |
| B8 | `(3, 4, 10, 3)` · `[2, 3, 4, 5]` · `(3, 10, 12)` | `(3, 10, 4, 3)` (forgetting `transpose(1, 2)` brings the head axis forward). `[2, 3, 4, 5, 6]` (the stop is **not** included). Writing the third as `(10, 12)`: the position rows stretch across the batch. |

## Section C — 12 marks

**3 marks each: (i) the bug named = 1 · (ii) what happens = 1 · (iii) a correct fix = 1.**

| Q | (i) The bug | (ii) What happens | (iii) The fix |
|:--:|---|---|---|
| C1 | `clip_grad_norm_` runs **before** `backward()`, so there is no gradient yet to clip | **Silent.** Nothing errors; the printed length is `1414.2`, not at most `1.0` | Move it: `backward()`, then `clip_grad_norm_`, then (in a real loop) `step()` |
| C2 | `fill_` on a slice of a tracked knob, outside `torch.no_grad()` | **Loud.** `RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation.` | Wrap it: `with torch.no_grad():` then the `fill_` line |
| C3 | `torch.multinomial(p, 8)` asks for 8 draws from 5 letters **without replacement** | **Loud.** `RuntimeError: cannot sample n_sample > prob_dist.size(-1) samples without replacement` | `torch.multinomial(p, 8, replacement=True)` |
| C4 | The hidden scores were filled with `0.0`, not `-inf`; `e^0 = 1`, so hidden words still get weight | **Silent.** Row 0 is `[0.7870, 0.1065, 0.1065]` and the check prints `False` | `masked_fill(future, float("-inf"))` |

For C1 and C4, a student who says "it crashes" has not understood the bug. Accept "it prints something wrong" for (ii). For C3, the first line `1` is a real draw from the seeded generator and not part of the bug. Accept any fix that produces the expected result; the key fixes above were run (see the key).

## Section D — 15 marks

| Part | Marks | What earns them |
|---|:--:|---|
| D1(a) | 1 | `V` = `[2, 0]` · `[0, 1]` · `[2, -1]`. 0 if two rows are wrong. |
| D1(b) | 1 | `[1, -1, 2]`. The dot products of `r = [1, -1]` with `p`, `q`, `r`: `1`, `-1`, `2`. |
| D1(c) | 1 | Exps `2.7183`, `0.3679`, `7.3891` · total `10.4753` · weights `0.2595`, `0.0351`, `0.7054` (add to 1.0000). |
| D1(d) | 1 | `[1.9298, -0.6703]`. Accept `1.930`, `-0.670`. |
| D1(e) | 1 | Scores `[0, 0.7071]` (q·p = 0, q·q = 1, divided by `sqrt 2`) · exps `1`, `2.0281` · weights `0.3302` on **p**, `0.6698` on **q**. The third word gets `0`, hidden. |
| D2(a) | 1 | `1 / 1.0821 = 0.9241`. |
| D2(b) | 1 | `0.9241 ^ 25 = 0.1391` (about `0.14`). The method is the point: a calculator power key, not 25 multiplications by hand. |
| D2(c) | 1 | `0.5 ^ 25 = 2.98e-08` (about `3.0e-08`). |
| D2(d) | 1 | `0.1391 / 2.98e-08 = 4.67e+06`, about four and a half to five million. Accept "about 5 million". |
| D2(e) | 1 | **9** (`0.9241^8 = 0.5320`, `0.9241^9 = 0.4916`). 0 for `8`. |
| D3(a) | 1 | `2 x (2 x 10) = 40`. |
| D3(b) | 1 | `3 x 100 + 110 = 410`. |
| D3(c) | 1 | `up` `10x40 + 40 = 440`; `down` `40x10 + 10 = 410`; total `850`. |
| D3(d) | 1 | `40 + 410 + 850 = 1300` (and `12 x 10 x 10 + 10 x 10 = 1300`). |
| D3(e) | 1 | `200 + 160 + 3 x 1300 + 20 + 220 = 4500`. |

## Section E — 12 marks

| Part | Marks | What earns them |
|---|:--:|---|
| E(a)(i) | 1 | **gap** `1.772 - 1.728 = 0.044`, **and** lowest val at **step 500** (`1.761`). Both needed. |
| E(a)(ii) | 1 | **Not a bug.** Any one of: both numbers are averages of only 20 random windows and the model has barely started; the difference (`0.039`) is small and goes the other way later; validation text is only 698 characters. "The model is cheating" scores 0. |
| E(a)(iii) | 1 | `2.033 - 1.772 = 0.261`. |
| E(a)(iv) | 1 | Knobs per character: **17.1** (`107,420 / 6,274`) and **128.7** (`807,196 / 6,274`). And one limit: the two runs also differ in width, blocks, steps, learning rate and seed, so nothing was changed alone; "consistent with, not proved". |
| E(b)(i) | 1 | **Five** powers of ten (`3.8e-01` against `2.5e-06`: about `1.5e+05`). Accept "about 5 or 6". |
| E(b)(ii) | 1 | `gru` [2.1e-07, 3.5e-06] and `lstm bias 0` [1.4e-07, 2.5e-06] **overlap**, so with three seeds you cannot rank them. `rnn` tops out at `9.7e-08`, just under the smallest LSTM number, so it is lowest, but only barely and on three seeds. |
| E(b)(iii) | 1 | `0.953 ^ 30 = 0.236` (about `0.24`); the table's `0.38, 0.23, 0.45` is in the same neighbourhood (within a factor of about 2). |
| E(b)(iv) | 1 | `0.38 / 0.17 = 2.2` times smaller: **falling, slowly** (a factor of a few in 30 more steps), nowhere near the `10^5` a bias-0 row loses. (The bias-0 row at `T = 60` is not printed, so only compare the sizes of the drops loosely.) |
| E(c) | 4 | One mark each: a supported statement **with a number** (e.g. "bias 3 keeps `0.38` of the last word's pull at `T = 30` and `0.17` at `T = 60`, against `2.5e-06` for bias 0") · says the layers were **untrained**, fed **random inputs**, with a **toy score** (the sum of the last output), and the numbers are gradient sizes, not memory · says the bias moves the number by about 5 powers of ten while the seeds move it by a factor of about 2, so the bias matters far more · names a run: **train** the RNN and the LSTM (bias 0 and bias 3) on the Week 13 copy task over at least three seeds. "Run more seeds" alone scores 0 for this mark: it must be something **trained**. |

## Part 2 — the demo, 15 marks

| | Marks | The teacher watches for |
|---|:--:|---|
| **Demo 1** | 5 | prediction said first (1) · `dial f = 0.9241`, `f ** 25 = 0.1391`, `0.5 ** 25 = 2.98e-08`, `first below one half after 9 multiplications` (1) · `c = 1.900, 1.810, 1.729` (1) · forget dial `0.8808` from the biases alone, built with `fill_` **inside** `torch.no_grad()`; the 40-step value `6.238e-03` (1) · the sentence: *"a dial of 0.88 still loses 99.4% in 40 steps; this is the starting point of an untrained cell, and nothing was trained"* (1) |
| **Demo 2** | 5 | prediction said first (1) · numpy and torch rows for **r** both `[1.9298, -0.6703]` and `True` for agreement (1) · q with both dials: weights `[0.3302, 0.6698, 0.0]`, output `[0.6605, 0.6698]` (1) · `[False, False, True]` for the three rows (1) · the sentence: *"with the mask, the first two rows do not move when the last word changes, because they cannot read it; without it they would"* (1) |
| **Demo 3** | 5 | prediction said first (1) · the five parts `200, 160, 3900, 20, 220` and the total `4500`, with `match: True` against the paper (2) · the distance check: `ln(20) = 2.9957`, first loss near `3.01`, distance about `0.015`, and the student says it is a **flag to look**, not proof (1) · `False` for a `(16, 16)` knob, and three `mask` entries in `state_dict`: *"the mask is saved with the model but never trained"* (1) |

> **Reference output of the three demos** (what a correct `demo1.py`, `demo2.py` and `demo3.py` print) is in the key. If the student's numbers differ in the last digit on your machine, that is the CPU; a difference in the first digit is a bug, so ask them to find it (the Debugging Clinic habit of Week 9). In Demo 3 the first loss depends on the **order** of `manual_seed`, model and `randint`; the order above gives `3.0107`. Another order may give a different number; it should still be within about `0.05` of `ln(20)`, and if it is not, that is the moment to talk about why.

## How to read the score

These thresholds are suggestions; nothing in the course depends on them.

| Paper | What it probably means |
|:--:|---|
| 60–75 | Term 3 can start as planned. |
| 45–59 | Fine to start Term 3. Redo the one or two weeks in the grid below that scored under 60%. |
| under 45 | Do **not** read this as a verdict. Check Section A against the demo first: a student who knew it at the machine and lost it on paper needs a different plan from one who lost it on both. Redo at most two weeks, then re-sit the Week 18 paper. |

### The per-week grid

Add up the marks the student earned on these questions, and divide by the total shown.

| Week | Questions | Marks available | Redo this week if under |
|:--:|---|:--:|:--:|
| [10](../student-guide/week-10.md) | A1–A3, B1, C1, D2 | 13 | 8 |
| [11](../student-guide/week-11.md) | A4–A6, B3, B4, C2, E(b), E(c) | 18 | 11 |
| [12](../student-guide/week-12.md) | A7–A9, A13, B2 | 6 | 4 |
| [13](../student-guide/week-13.md) | A10–A12, B6, C3 | 8 | 5 |
| [14](../student-guide/week-14.md) | A14–A15, D1(a)–(d) | 6 | 4 |
| [15](../student-guide/week-15.md) | A16–A18, B7, C4, D1(e) | 9 | 5 |
| [16](../student-guide/week-16.md) | A19, B8, D3 | 8 | 5 |
| [17](../student-guide/week-17.md) | A20, B5, E(a) | 7 | 4 |
| **Total** | | **75** | |

Three weeks carry Term 3: **Week 14** (the three-token attention pass is what Week 19's ablations take apart), **Week 16** (the block and its knob count) and **Week 17** (TinyGPT itself, which Week 19 opens). If any of those is under the threshold, redo it first. **Week 11** is the heaviest single week on this paper (18 marks); a low score there with high scores elsewhere usually means the forget dial, not the whole term.

---

# ✅ ANSWER KEY

> **🧑‍🏫 Do not show this to the student until after the test is marked.** It contains every answer and names the mistakes the student is expected to make. **Every code block in this key was run, and the real output is pasted in unedited.**

## Section A — why each answer, and why the wrong ones were tempting

<details>
<summary><b>A1 – A3 · Week 10</b></summary>

**A1 — (b) about 0.36.** `0.98 ** 50`. (a) is the linear guess, `50 x 2% = 100%`: compounding loses 2% of **what is left**, not of the start. (c) and (d) ignore fifty multiplications or overdo them.

**A2 — (c).** Block 6 of Week 10 showed exactly this kind of row: four huge, one vanished. (b) is "always", which five seeds cannot say. (a) blames the probe. (d) has clipping, which cannot create a vanishing.

**A3 — (a).** It goes before `backward()`. (b) and (d) confuse "keep this gradient" with "train this" or "block this"; (c) is `clip_grad_norm_`'s job.

</details>

<details>
<summary><b>A4 – A6 · Week 11</b></summary>

**A4 — (d) exactly what it was.** `c = 1.0 * c + 0.0 * g`. The run below confirms it. Tempting: (a), from "a gate forgets".

**A5 — (b) a pair.** `nn.LSTM` returns `(out, (h_n, c_n))`: its second answer is itself a pair. (a) is what `nn.RNN` and `nn.GRU` do.

**A6 — (c).** Nothing was trained. The table is about the *starting point* of untrained layers on random numbers, with a toy loss. (a), (b) and (d) are all read straight off the table.

</details>

<details>
<summary><b>A7 – A9, A13 · Week 12</b></summary>

**A7 — (a).** It is the `x[:, t]` line versus `tok = torch.tensor([i])`. (c) and (d) are tempting because they sound like a real difference between training and generating; dropout is a mode, not the reason.

**A8 — (b).** Padding is an easy guess ("after EOS comes PAD"), so counting it lowers the printed number without the model learning a letter. Week 12's block 2 showed exactly this: `0.5857` with padding counted against `1.1513` with it ignored.

**A9 — (d).** 31 names is too few, and zero is also what a model that copies its training list would show. (a) and (b) are the story the number tempts you to tell.

**A13 — (a).** The `-1` means "work this number out for me": `231 x 8 = 1,848`. (b) is slicing's `-1`; (d) is `ignore_index`.

</details>

<details>
<summary><b>A10 – A12 · Week 13</b></summary>

**A10 — (c).** `scores / 0.0` is `inf` (and `0 / 0` is `nan`), so the softmax is `nan` and `torch.multinomial` stops. The run below prints the message. (a) is the hope; greedy is `argmax`, not a temperature.

**A11 — (b) only the top letter.** The letters ranked above the top letter add to `0`, which is below `0.5`, so it is kept; the letters ranked above the second add to `0.8`, so it is not. (d) is what you get from the **wrong** test ("total including this letter is below `p`"), and it leaves nothing to choose from. The run below prints both.

**A12 — (d).** The gap fits exposure bias, but plain sampling and reciting the training list fit the same number. (a) is the story; (b) and (c) are wrong on the facts.

</details>

<details>
<summary><b>A14 – A15 · Week 14</b></summary>

**A14 — (c) 55.** A weighted average with non-negative weights that add to 1 lands between the smallest and the biggest value (`10` and `50`). (d) `10` is possible: all the weight on the first value.

**A15 — (d).** `e.sum()` with no `axis` is one **grand** total. The run below prints the rows adding to `0.25`, `0.25`, `0.5`. (a) is tempting because the line looks like a softmax and the table as a whole does add to 1.

</details>

<details>
<summary><b>A16 – A18 · Week 15</b></summary>

**A16 — (a) 10.** Variances add: `36 + 64 = 100`, and the square root is `10`. (b) adds the spreads; (d) multiplies.

**A17 — (b).** Scores times 10 saturate the softmax. The run below prints `0.000000, 1.000000, 0.000000`.

**A18 — (c).** `e^0 = 1`: a score of `0` is not "nothing". The run below prints the first row as `0.5761, 0.2119, 0.2119`. (a) is the hope; (b) is the "mask **after** the softmax" bug.

</details>

<details>
<summary><b>A19 – A20 · Weeks 16 and 17</b></summary>

**A19 — (b) 12.** The `Linear` has `3 x 3 + 3 = 12`; the mask is a buffer: saved with the model (it is one of the `state_dict` keys) but never trained. (a) adds the mask's 9.

**A20 — (a) 90.** `randint` stops **before** its top number, so `90` gives starts `0` to `89`, and the last start has `y` ending at index `99`. (c) is the last valid **start**; `randint` wants one more than that. (b) is the deliberate bug of the Week 17 guide: the last windows run off the end.

</details>

### The Section A facts, run

```py
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
torch.set_num_threads(1)
# A1 (W10): 2% lost per step, 50 steps
print("A1  0.98 ** 50 =", round(0.98 ** 50, 4), "  the linear guess 1 - 50 * 0.02 =", round(1 - 50 * 0.02, 1))
# A4 (W11): f = 1, i = 0 leaves the memory exactly as it was
c = 0.7321
for _ in range(40):
    c = 1.0 * c + 0.0 * 0.9
print("A4  c after 40 steps with f = 1, i = 0:", c)
# A11 (W13): top-p with the right test and the wrong test
p = torch.tensor([0.8, 0.1, 0.06, 0.04])
running = torch.cumsum(p, dim=0)
before = running - p
print("A11 total ranked above:", [round(v, 2) for v in before.tolist()])
print("    right test  (before < 0.5):", (before < 0.5).tolist())
print("    wrong test  (running < 0.5):", (running < 0.5).tolist())
# A14 (W14): a weighted average lies between the smallest and largest value
w = torch.tensor([0.112, 0.751, 0.137])
print("A14 soft lookup of [10, 50, 30]:", round((w * torch.tensor([10.0, 50.0, 30.0])).sum().item(), 2), "  largest possible: 50")
# A17 (W15): shouting the scores
s = torch.tensor([0.1, 2.0, 0.3])
print("A17 calm:", [round(v, 3) for v in F.softmax(s, dim=-1).tolist()], " loud (x10):", [round(v, 6) for v in F.softmax(s * 10, dim=-1).tolist()])
# A18 (W15): hide with 0.0 instead of -inf
sc = torch.tensor([[1.0, 1.0, 1.0]] * 3)
future = torch.tril(torch.ones(3, 3)) == 0
print("A18 hidden with 0.0 then softmax, row 0:", [round(v, 4) for v in F.softmax(sc.masked_fill(future, 0.0), dim=-1)[0].tolist()])
print("    hidden with -inf then softmax, row 0:", [round(v, 4) for v in F.softmax(sc.masked_fill(future, float('-inf')), dim=-1)[0].tolist()])
# A19 (W16): a 3x3 linear plus a registered 3x3 mask buffer
class M(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(3, 3)
        self.register_buffer("mask", torch.tril(torch.ones(3, 3)))
print("A19 knobs:", sum(q.numel() for q in M().parameters()), " saved entries:", list(M().state_dict().keys()))
# A20 (W17): the top number of torch.randint
text_len, T = 100, 10
torch.manual_seed(0)
starts = torch.randint(text_len - T, (5000,))
print("A20 largest start drawn:", int(starts.max()), "  its y ends at index", int(starts.max()) + T, "of", text_len - 1)
# A15 (W14): row totals against grand total
sc2 = torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]])
e = torch.exp(sc2)
wrong = e / e.sum()
print("A15 row sums with the grand total:", [round(v, 3) for v in wrong.sum(dim=1).tolist()], " with row totals:", (e / e.sum(dim=1, keepdim=True)).sum(dim=1).tolist())
# A10 (W13): temperature zero
try:
    torch.multinomial(F.softmax(torch.tensor([0.0, 2.0, 1.0]) / 0.0, dim=-1), 1)
except RuntimeError as err:
    print("A10", err)
```

```text
A1  0.98 ** 50 = 0.3642   the linear guess 1 - 50 * 0.02 = 0.0
A4  c after 40 steps with f = 1, i = 0: 0.7321
A11 total ranked above: [0.0, 0.8, 0.9, 0.96]
    right test  (before < 0.5): [True, False, False, False]
    wrong test  (running < 0.5): [False, False, False, False]
A14 soft lookup of [10, 50, 30]: 42.78   largest possible: 50
A17 calm: [0.112, 0.751, 0.137]  loud (x10): [0.0, 1.0, 0.0]
A18 hidden with 0.0 then softmax, row 0: [0.5761, 0.2119, 0.2119]
    hidden with -inf then softmax, row 0: [1.0, 0.0, 0.0]
A19 knobs: 12  saved entries: ['mask', 'lin.weight', 'lin.bias']
A20 largest start drawn: 89   its y ends at index 99 of 99
A15 row sums with the grand total: [0.25, 0.25, 0.499]  with row totals: [1.0, 1.0, 1.0]
A10 probability tensor contains either `inf`, `nan` or element < 0
```

(`A14` prints `42.78` because the weights are rounded to three places; Week 14's `42.77` keeps every digit. `A8`'s numbers come from Week 12's own block 2, in the student guide.)

---

## Section B — outputs, run

Every snippet on the paper, run exactly as printed on the paper (B4 with `torch.manual_seed(0)` as shown), one after another. The output of each is below it.

**B1**
```text
6 11.39
```
`1.5^5 = 7.59` is still below 10, so the loop goes round a sixth time: `1.5^6 = 11.39`.

**B2**
```text
(6, 1) (6, 8) (6, 9)
27 0
```

**B3**
```text
1.9
1.81
1.729
```
`0.9 x 2.0 + 0.1 = 1.9`, then `0.9 x 1.9 + 0.1 = 1.81`, then `0.9 x 1.81 + 0.1 = 1.729`.

**B4**
```text
(6, 7) (1, 7) (1, 7)
336
```
`out` has one row per step (6) of 7 numbers; `h_n` and `c_n` are each one final `(1, 7)`. `336 = 4 x 84`.

**B5**
```text
[106, 107, 108, 109]
[107, 108, 109]
```
`text` has indices `0` to `9`, so `text[6:10]` is four long but `text[7:11]` stops at the end and is three long. No error: this is the quiet half of Week 17's deliberate `randint` bug.

**B6**
```text
0.98
0.88
```

**B7**
```text
tensor([[1.0000, 0.0000],
        [0.5000, 0.5000]])
tensor([[10.],
        [15.]])
```

**B8**
```text
(3, 4, 10, 3)
[2, 3, 4, 5]
(3, 10, 12)
```

## Section C — bugs, run

Each program below was run first as printed on the paper (the output is on the paper and in the table above), then with its fix.

**C1 fixed** (`backward()`, then clip, with the clip's own return value printed):
```py
import torch
import torch.nn as nn
torch.manual_seed(0)
model = nn.Linear(2, 1)
x = torch.tensor([[1000.0, 1000.0]])
model(x).sum().backward()
before = nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
print(round(before.item(), 1), round(model.weight.grad.norm().item(), 1))
```
```text
1414.2 1.0
```
The first number is the length **before** clipping (what `clip_grad_norm_` returns); the second is the weight gradient's length after. In the buggy version `clip_grad_norm_` saw no gradients at all, so it did nothing.

**C2 fixed:**
```py
import torch
import torch.nn as nn
H = 16
lstm = nn.LSTM(4, H)
with torch.no_grad():
    lstm.bias_ih_l0[H:2 * H].fill_(2.0)
print("forget bias set", lstm.bias_ih_l0[H:2 * H][:3].tolist(), lstm.bias_ih_l0[0].item() != 2.0)
```
```text
forget bias set [2.0, 2.0, 2.0] True
```
(The last `True` says only the forget group was touched.)

**C3 fixed:**
```py
import torch
torch.manual_seed(0)
p = torch.tensor([0.5, 0.3, 0.1, 0.06, 0.04])
print(torch.multinomial(p, 1).item())
print(torch.multinomial(p, 8, replacement=True).tolist())
```
```text
1
[1, 0, 0, 1, 0, 0, 0, 0]
```
Eight draws from five chances must be **with** replacement: the same letter will come up again.

**C4 fixed:**
```py
import torch
import torch.nn.functional as F
scores = torch.tensor([[2.0, 0.0, 1.0],
                       [0.0, 2.0, 1.0],
                       [1.0, 1.0, 1.0]])
future = torch.tril(torch.ones(3, 3)) == 0
weights = F.softmax(scores.masked_fill(future, float("-inf")), dim=-1)
print(weights)
print(weights[0, 1:].sum().item() == 0.0)
```
```text
tensor([[1.0000, 0.0000, 0.0000],
        [0.1192, 0.8808, 0.0000],
        [0.3333, 0.3333, 0.3333]])
True
```

## Section D — worked answers

### D1 (attention, 5 marks)

```text
(a) V = X Wv:   p -> [2, 0]     q -> [0, 1]     r -> [2, -1]
(b) scores for r:   r.p = 1    r.q = -1    r.r = 2       ->  [1, -1, 2]
(c) exps 2.7183  0.3679  7.3891     total 10.4753
    weights 2.7183/10.4753 = 0.2595    0.3679/10.4753 = 0.0351    7.3891/10.4753 = 0.7054
    (0.2595 + 0.0351 + 0.7054 = 1.0000)
(d) output for r = 0.2595 x [2, 0] + 0.0351 x [0, 1] + 0.7054 x [2, -1]
                 = [0.5190 + 0 + 1.4108,  0 + 0.0351 - 0.7054]  =  [1.9298, -0.6703]
(e) q, both dials.  q may read p and q.  scores q.p = 0, q.q = 1
    divide by sqrt(2):  0 and 0.7071     exps 1 and 2.0281    total 3.0281
    weights  1/3.0281 = 0.3302 on p,   2.0281/3.0281 = 0.6698 on q,   0 on r (hidden)
```

A quick check by machine (the same arithmetic, in numpy):

```py
import numpy as np, math
X = np.array([[1., 0.], [0., 1.], [1., -1.]])   # p q r
Wv = np.array([[2., 0.], [0., 1.]])
V = X @ Wv
S = X @ X.T
print("V\n", V); print("S\n", S)
def sm(s):
    e = np.exp(s)
    print(" exps", np.round(e, 4), "total", round(e.sum(), 4))
    return e / e.sum()
w = sm(S[2]); print("row r weights", np.round(w, 4), w.sum().round(4)); print("out r", np.round(w @ V, 4))
s2 = S / math.sqrt(2)
w3 = sm(s2[1][:2]); print("row q, both dials", np.round(w3, 4)); print("out", np.round(w3 @ V[:2], 4))
```
```text
V
 [[ 2.  0.]
 [ 0.  1.]
 [ 2. -1.]]
S
 [[ 1.  0.  1.]
 [ 0.  1. -1.]
 [ 1. -1.  2.]]
 exps [2.7183 0.3679 7.3891] total 10.4752
row r weights [0.2595 0.0351 0.7054] 1.0
out r [ 1.9298 -0.6703]
 exps [1.     2.0281] total 3.0281
row q, both dials [0.3302 0.6698]
out [0.6605 0.6698]
```

(The machine totals `10.4752`; the hand total `10.4753` adds the four-place exps. Both give the same weights to four places. In (e) the hand sum gives `0.6604`; the machine's unrounded weights give `0.6605`. Accept either.)

### D2 (the dial, 5 marks)

```text
(a) f = 1 / (1 + 0.0821) = 1 / 1.0821 = 0.9241
(b) 0.9241 ^ 25 = 0.1391          (about 14% of the signal is left after 25 steps back)
(c) 0.5 ^ 25 = 2.98e-08            (about three parts in a hundred million)
(d) 0.1391 / 2.98e-08 = 4.67e+06   (about four and a half million times more)
(e) 0.9241^8 = 0.532, 0.9241^9 = 0.4916  ->  after 9 multiplications
```

```py
import math
f = 1 / (1 + math.exp(-2.5))
print("f", round(f, 4), " f**25", round(f ** 25, 4), " 0.5**25", f"{0.5 ** 25:.2e}", " ratio", f"{f ** 25 / 0.5 ** 25:.2e}")
value, k = 1.0, 0
while value >= 0.5:
    value = value * f
    k = k + 1
    if k in (8, 9):
        print(k, round(value, 4))
```
```text
f 0.9241  f**25 0.1391  0.5**25 2.98e-08  ratio 4.67e+06
8 0.532
9 0.4916
```

Common slips: `0.9241 x 25` (multiplying instead of raising to the power, `23.1`); `f = 0.0821` (forgetting the `1 /`); `8` for (e), the number where the value is still `0.532`.

### D3 (the knob count, 5 marks)

```text
(a) two LayerNorm(10):            2 x (2 x 10)                 =   40
(b) attention:  q, k, v           3 x (10 x 10)                =  300
                proj              10 x 10 + 10                 =  110        -> 410
(c) MLP:        up                10 x 40 + 40                 =  440
                down              40 x 10 + 10                 =  410        -> 850
(d) one block:  40 + 410 + 850                                 = 1300        (12 x 10 x 10 + 10 x 10)
(e) whole model: tok 20 x 10                                   =  200
                 pos 16 x 10                                   =  160
                 3 blocks   3 x 1300                           = 3900
                 final LayerNorm(10)  2 x 10                   =   20
                 head Linear(10, 20)  10 x 20 + 20             =  220
                                                       total   = 4500
```

The 2 heads and the mask cost nothing: the count has no `H` and no `T x T` in it. That is the Week 16 result, and students who put `2 x 100` or a mask term into (b) have not absorbed it. The Demo 3 program below prints the same `4500` from the real model.

## Section E — worked answers

### How the two tables were made

**Table 1** (`e1.py`): Week 17's `tinygpt.py` (extracted from the guide and run unchanged) and Week 17's own training loop, with the model built at `d = 64, H = 4, L = 2`, `lr = 1e-3`, 700 steps, 50 warm-up steps, seed 1. The counters are Week 18's `baselines.py` recipe.

```py
# e1.py - Term 2 test, Table 1: a reduced TinyGPT (width 64, 2 blocks), 700 steps, seed 1. Uses tinygpt.py from Week 17.
import math, time
import numpy as np
import torch
from tinygpt import TinyGPT
from l4lib.corpus import TEXT
torch.manual_seed(1)
chars = sorted(set(TEXT)); V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}; itos = {i: c for c, i in stoi.items()}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data)); train_data, val_data = data[:n], data[n:]
d, H, L, T, B = 64, 4, 2, 64, 32
STEPS, WARMUP = 700, 50
def get_batch(split):
    src = train_data if split == "train" else val_data
    starts = torch.randint(len(src) - T, (B,))
    return torch.stack([src[s:s+T] for s in starts]), torch.stack([src[s+1:s+T+1] for s in starts])
@torch.no_grad()
def estimate(split, batches=20):
    return sum(model(*get_batch(split))[1].item() for _ in range(batches)) / batches
model = TinyGPT(V, d, H, L, T)
print("knobs:", sum(p.numel() for p in model.parameters()))
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.1)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s+1)/WARMUP if s < WARMUP else 0.5*(1+math.cos(math.pi*(s-WARMUP)/(STEPS-WARMUP))))
t_all = 0.0
print("step   train    val")
for step in range(STEPS):
    if step in (0, 100, 200, 300, 400, 500, 600):
        print(f"{step:4d}  {estimate('train'):.3f}  {estimate('val'):.3f}")
    t0 = time.perf_counter()
    x, y = get_batch("train"); _, loss = model(x, y)
    opt.zero_grad(set_to_none=True); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step()
    t_all += time.perf_counter() - t0
print(f" 699  {estimate('train'):.3f}  {estimate('val'):.3f}")
print(f"step time {1000*t_all/STEPS:.0f} ms, total {t_all:.0f} s")
ids = data.tolist(); tr, va = ids[:n], ids[n:]
print("knows nothing (uniform)   :", round(math.log(V), 3))
one = np.ones(V)
for c in tr: one[c] += 1
p1 = one / one.sum()
print("knows letter frequencies  :", round(float(np.mean([-math.log(p1[c]) for c in va[1:]])), 3))
two = np.ones((V, V))
for a, b in zip(tr[:-1], tr[1:]): two[a, b] += 1
p2 = two / two.sum(axis=1, keepdims=True)
print("knows the previous letter :", round(float(np.mean([-math.log(p2[a, b]) for a, b in zip(va[:-1], va[1:])])), 3))
known = set(TEXT.split())
idx = torch.tensor([[stoi["t"]]])
out = model.generate(idx, 1000, 0.8)[0].tolist()
s = "".join(itos[i] for i in out)
w = s.split()
print("real words in a 1,000-character sample:", f"{100*sum(x in known for x in w)/len(w):.0f}%")
print(s[:200].replace("\n", " / "))
```
```text
knobs: 107420
step   train    val
   0  3.331  3.334
 100  2.157  2.118
 200  1.980  1.978
 300  1.870  1.899
 400  1.791  1.832
 500  1.743  1.761
 600  1.719  1.767
 699  1.728  1.772
step time 15 ms, total 10 s
knows nothing (uniform)   : 3.332
knows letter frequencies  : 2.855
knows the previous letter : 2.033
real words in a 1,000-character sample: 26%
t thas bre ba uther sand rornd and mave wad theand bedin re che heane wig. / ald ther gis a laus ished and ris. / theang the as. / thes a lil bring diklt the theter stid the poa thild. / the wer. / the on san s
```

(`step time` depends on the machine; print the table on the paper, do not regenerate it.)

**Table 2** (`e2.py`): the `make_layer` and `reach` functions are Week 11's blocks 6 and 7, unchanged, run on seeds 3, 4, 5 at `T = 30`.

```py
# e2.py - Term 2 test, Table 2: how much the end of a 30-step sequence cares about the first word (untrained layers, seeds 3-5).
import math
import torch
import torch.nn as nn
torch.set_num_threads(1)
D, H = 4, 16
def make_layer(kind, seed=0, forget_bias=None):
    torch.manual_seed(seed)
    layer = {"rnn": nn.RNN, "gru": nn.GRU, "lstm": nn.LSTM}[kind](D, H)
    if forget_bias is not None:
        with torch.no_grad():
            layer.bias_ih_l0[H:2 * H].fill_(forget_bias)
            layer.bias_hh_l0[H:2 * H].fill_(0.0)
    return layer
def reach(layer, T, seed=0):
    torch.manual_seed(100 + seed)
    x = torch.randn(T, D, requires_grad=True)
    out, last = layer(x)
    out[-1].sum().backward()
    return [row.norm().item() for row in x.grad]
def ratio(kind, T, seed, forget_bias=None):
    sizes = reach(make_layer(kind, seed, forget_bias), T, seed)
    return sizes[0] / sizes[-1]
print("T = 30, first word / last word, seeds 3, 4, 5:")
for label, kind, fb in [("rnn", "rnn", None), ("gru", "gru", None), ("lstm, forget bias 0", "lstm", 0.0), ("lstm, forget bias 1", "lstm", 1.0), ("lstm, forget bias 3", "lstm", 3.0)]:
    print(f"  {label:20s}", [f"{ratio(kind, 30, seed, fb):.1e}" for seed in (3, 4, 5)])
print("the dial for each bias:", [round(1 / (1 + math.exp(-b)), 3) for b in (0, 1, 3)])
print("T = 30 against T = 60, seed 3, lstm with forget bias 3:", [f"{ratio('lstm', T, 3, 3.0):.1e}" for T in (30, 60)])
```
```text
T = 30, first word / last word, seeds 3, 4, 5:
  rnn                  ['9.7e-08', '4.8e-11', '1.3e-08']
  gru                  ['8.5e-07', '3.5e-06', '2.1e-07']
  lstm, forget bias 0  ['2.5e-06', '1.4e-07', '1.7e-06']
  lstm, forget bias 1  ['4.9e-03', '2.0e-03', '1.6e-03']
  lstm, forget bias 3  ['3.8e-01', '2.3e-01', '4.5e-01']
the dial for each bias: [0.5, 0.731, 0.953]
T = 30 against T = 60, seed 3, lstm with forget bias 3: ['3.8e-01', '1.7e-01']
```

### E(a) — Table 1 (4 marks)

**(i)** Gap at step 699: `1.772 - 1.728 =` **0.044**. The validation loss is lowest at **step 500** (`1.761`); steps 600 and 699 (`1.767`, `1.772`) are within `0.011` of it, which is inside the noise of an average of 20 windows, so "flat since step 500" is the fair reading.

**(ii)** **Not a bug.** At step 100 the gap is `2.118 - 2.157 = -0.039`. Both numbers are averages of 20 random windows, the validation text is only 698 characters, and the model has barely started; a difference of `0.04` in either direction is noise at this size. It is the same reason Week 17's step-0 gap was `0.002`.

**(iii)** `2.033 - 1.772 =` **0.261**. The model is better than one that reads only the previous letter, but not by a huge margin; and 26% real words at step 699 (against 60% for the full-size run) agrees.

**(iv)** Knobs per training character: `107,420 / 6,274 =` **17.1**; Week 17's run is `807,196 / 6,274 =` **128.7**. The gaps are `0.044` and `0.543`. It fits the "fewer knobs per character, less room to memorise" story (Week 5's memorising, on letters), and it is a story to test, not a result: the two runs also differ in width, number of blocks, learning rate, number of steps and seed, so nothing was changed alone. To test it you would change only the width, with everything else fixed, and look at three seeds.

### E(b) — Table 2 (4 marks)

**(i)** Seed 3: `3.8e-01` against `2.5e-06` is about `1.5 x 10^5`: **five** powers of ten (the ratio is `150,000`; accept 5 or 6).

**(ii)** Ranges: `rnn` runs from `4.8e-11` to `9.7e-08`; `gru` from `2.1e-07` to `3.5e-06`; `lstm, bias 0` from `1.4e-07` to `2.5e-06`. **`gru` and `lstm, bias 0` overlap** (both cover roughly `2e-07` to `2.5e-06`), so on three seeds you cannot say which is better; the numbers are of the same kind. `rnn` tops out at `9.7e-08`, just below the smallest LSTM number `1.4e-07`, so it is lowest, but that is a gap of a factor of 1.4 on three seeds, so hold it loosely.

**(iii)** `0.953 ^ 30 =` **0.236** (a calculator). The three measured numbers `0.38, 0.23, 0.45` are in the same neighbourhood (within a factor of about two). This is Week 11's "the main path is `f`": in a real cell the dials also read the old note, so the main path is not the whole story, and the match is loose on purpose.

**(iv)** `0.38 / 0.17 =` about **2.2 times smaller**: **falling, slowly**. Thirty more steps cost a factor of about two, not the factor of `10^5` or more that bias 0 loses over twenty or so steps in the Week 11 table. (The bias-0 row at `T = 60` is not printed on the paper, so this is a comparison of the sizes of the drops, not of two cells.)

### E(c) — exemplars (4 marks)

**A full-marks reply:** *"The table shows that with forget bias 3, the first word still has `0.38` of the last word's pull at 30 steps and `0.17` at 60, against `2.5e-06` for the default bias at 30. But these layers were never trained, the inputs were random numbers, and the score was 'add up the last output', so the numbers are gradient sizes at the starting point and not evidence that a trained LSTM remembers a word. The bias moves the number by five powers of ten, while the seeds only move it by a factor of two or so, so the bias matters much more than luck here. Before saying more I would train an RNN and an LSTM (bias 0 and bias 3) on the Week 13 copy task over three seeds and compare how far back each can copy."*

**A reply scoring 2:** *"The table shows the LSTM with bias 3 is much better. It is untrained, though. I'd run more."* (A number is missing; "more" is not a trained run.)

**A reply scoring 0:** *"LSTMs fix forgetting, as the table proves."* Repeats the claim and uses no number.

## Part 2 — the demo, reference output

**Demo 1** — what a correct `demo1.py` prints:

```py
import math
import torch
import torch.nn as nn

# Part (i): the dial from D2, by hand-style arithmetic
f = 1 / (1 + math.exp(-2.5))
print(f"dial f = {f:.4f}   f ** 25 = {f ** 25:.4f}   0.5 ** 25 = {0.5 ** 25:.2e}")
value, k = 1.0, 0
while value >= 0.5:
    value = value * f
    k = k + 1
print(f"first below one half after {k} multiplications ({value:.4f})")

# Part (ii): B3, the memory line, three steps
f3, i3, g3 = 0.9, 0.2, 0.5
c = 2.0
for step in range(3):
    c = f3 * c + i3 * g3
    print(f"step {step + 1}: c = {c:.3f}")

# Part (iii): set the forget bias of a real LSTMCell to 2 and read the dial back
H = 16
torch.manual_seed(0)
cell = nn.LSTMCell(4, H)
with torch.no_grad():
    cell.bias_ih[H:2 * H].fill_(2.0)
    cell.bias_hh[H:2 * H].fill_(0.0)
z = cell.bias_ih[H:2 * H] + cell.bias_hh[H:2 * H]
dial = torch.sigmoid(z)
print("forget dial from the bias alone, first three units:", [round(v, 4) for v in dial[:3].tolist()])
print("that dial multiplied 40 times:", f"{dial[0].item() ** 40:.3e}")
```
```text
dial f = 0.9241   f ** 25 = 0.1391   0.5 ** 25 = 2.98e-08
first below one half after 9 multiplications (0.4916)
step 1: c = 1.900
step 2: c = 1.810
step 3: c = 1.729
forget dial from the bias alone, first three units: [0.8808, 0.8808, 0.8808]
that dial multiplied 40 times: 6.238e-03
```

`0.8808 ** 40 = 0.00624`, so 99.4% of the signal is gone, on the main path, at the **starting point** of an untrained cell. Bias 2 is a better start than bias 0 (`0.5 ** 40 = 9e-13`), not a solved problem. **The sentence to listen for:** the dial is a setting we wrote, not something learned.

**Demo 2** — what a correct `demo2.py` prints:

```py
import numpy as np
import torch
import torch.nn.functional as F

X = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, -1.0]])                     # p, q, r
Wq = np.eye(2)
Wk = np.eye(2)
Wv = np.array([[2.0, 0.0],
               [0.0, 1.0]])

def softmax_rows(s):
    e = np.exp(s)
    return e / e.sum(axis=1).reshape(-1, 1)

# Part (i): D1 in numpy, then in torch
Q, K, V = X @ Wq, X @ Wk, X @ Wv
w_np = softmax_rows(Q @ K.T)
out_np = w_np @ V
xt = torch.tensor(X.tolist())
qt, kt, vt = xt @ torch.tensor(Wq.tolist()), xt @ torch.tensor(Wk.tolist()), xt @ torch.tensor(Wv.tolist())
out_t = F.softmax(qt @ kt.transpose(-2, -1), dim=-1) @ vt
print("row r, numpy:", np.round(out_np[2], 4), " torch:", np.round(out_t[2].tolist(), 4))
print("numpy vs torch, biggest gap below 1e-5:", np.abs(out_np - np.array(out_t.tolist())).max() < 1e-5)

# Part (ii): both dials
mask = torch.tril(torch.ones(3, 3))
def attend(x):
    q, k, v = x @ torch.tensor(Wq.tolist()), x @ torch.tensor(Wk.tolist()), x @ torch.tensor(Wv.tolist())
    s = (q @ k.transpose(-2, -1)) / 2 ** 0.5
    s = s.masked_fill(mask == 0, float("-inf"))
    w = F.softmax(s, dim=-1)
    return w, w @ v
w, out = attend(xt)
print("weights of q with both dials:", [round(v, 4) for v in w[1].tolist()])
print("output of q with both dials: ", [round(v, 4) for v in out[1].tolist()])
x2 = torch.tensor([[1.0, 0.0], [0.0, 1.0], [5.0, -3.0]])    # change ONLY the last word
_, out2 = attend(x2)
print("rows that moved when the last word changed:", [bool((out[i] - out2[i]).abs().max() > 1e-6) for i in range(3)])
```
```text
row r, numpy: [ 1.9298 -0.6703]  torch: [ 1.9298 -0.6703]
numpy vs torch, biggest gap below 1e-5: True
weights of q with both dials: [0.3302, 0.6698, 0.0]
output of q with both dials:  [0.6605, 0.6698]
rows that moved when the last word changed: [False, False, True]
```

The last line is the point: with the mask, words 1 and 2 cannot read word 3, so changing word 3 moves only word 3's own row. Without the mask all three rows would move (Week 15's `dials.py` printed `[True, True, True]`).

**Demo 3** — what a correct `demo3.py` prints (with `tinygpt.py` from Week 17 beside it):

```py
import math
import torch
from tinygpt import TinyGPT, Block
torch.manual_seed(0)
V, d, H, L, T = 20, 10, 2, 3, 16
model = TinyGPT(V, d, H, L, T)
parts = {"tok": model.tok, "pos": model.pos, "blocks": model.blocks, "ln_f": model.ln_f, "head": model.head}
for name, part in parts.items():
    print(f"  {name:<6}", sum(p.numel() for p in part.parameters()))
total = sum(p.numel() for p in model.parameters())
print("knobs:", total, " my hand count (D3):", 4500, " match:", total == 4500)
x = torch.randint(V, (8, T))
y = torch.randint(V, (8, T))
with torch.no_grad():
    _, loss = model(x, y)
print(f"ln({V}) = {math.log(V):.4f}   first loss = {loss.item():.4f}   distance = {abs(loss.item() - math.log(V)):.4f}")
print("mask counted as a knob?", any(p.shape == (T, T) for p in model.parameters()))
print("mask entries in the saved state:", [k for k in model.state_dict() if k.endswith("mask")])
```
```text
  tok    200
  pos    160
  blocks 3900
  ln_f   20
  head   220
knobs: 4500  my hand count (D3): 4500  match: True
ln(20) = 2.9957   first loss = 3.0107   distance = 0.0149
mask counted as a knob? False
mask entries in the saved state: ['blocks.0.mask', 'blocks.1.mask', 'blocks.2.mask']
```

The five parts and the total match D3 line for line. The first loss is `0.0149` from `ln(20)`: inside the Week 17 bar of `0.05`. The sentence to listen for: *"a model that knows nothing must start at `ln(vocab)`; if it does not, look before you trust it. It is a flag, not a proof."* The mask is in `state_dict` (saved with the model) but not in `parameters()` (never trained): one `mask` per block, three in all.

---

## 🧭 What this test does and does not show

1. **It is one sample.** A student who was ill, hungry or anxious scores lower than they know. Treat the pattern across weeks as the information and the total as almost none.
2. **Multiple choice can be guessed.** Twenty 4-option questions guessed at random average 5 marks. That is why only 20 of the 75 marks are there and why every wrong option was built from a real mistake.
3. **The two Section E tables are small samples.** Table 1 is one reduced network on one seed; Table 2 is untrained layers on three seeds. They show *symptoms*, not laws. Nothing on this test claims the reduced model's small gap would hold at other widths, or that a trained LSTM remembers 60 steps back.
4. **Section E is a reading test, and the hardest mark is the fourth of E(c).** Students who name "more seeds" have learned Term 1's lesson and not yet Term 2's: the natural next step for an untrained measurement is a **trained** one.
5. **The demo marks a conversation.** The student's own words at the machine are the evidence; do not help, and do not mark a sentence the student was handed.
6. **Not on this test, on purpose:** anything from Week 19 onwards. If a student writes "ablation", "tokenizer", "BPE", "pretraining" or "DPO" anywhere, do not mark it wrong and do not mark it extra; it comes from next term. Say so kindly on the sheet.

**Nothing on the ladder is used before its week.** The constructs on this test are, by week: W10 `h.retain_grad()`, `torch.stack`, `torch.randn`, `clip_grad_norm_` (Week 6); W11 `nn.LSTM`, `nn.LSTMCell`, `fill_` on a slice of a bias; W12 `torch.full`, `torch.cat`, `reshape(-1, V)`, `ignore_index`; W13 `F.softmax(dim=)`, `torch.multinomial`, top-p by `cumsum`, temperature; W14 `transpose(-2, -1)`, the row-by-row softmax; W15 `masked_fill`, `torch.tril`, `.view(B, T, H, dh).transpose(1, 2)`; W16 `torch.arange`, `nn.ModuleList`-held blocks, `register_buffer`, the knob count; W17 `torch.randint`, the nested `TinyGPT` and the first-loss check. Section D's "compounding" is Week 10's maths, the "variances add" question (A16) is Week 15's, and the "weighted average" (A14) is Week 14's. `nn.Embedding` (B8) is Week 8's, `AdamW`, `LambdaLR` (Table 1's training recipe) are Weeks 3 and 4's. Weeks 19–36 appear nowhere on this test.
