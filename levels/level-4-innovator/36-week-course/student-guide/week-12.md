# Week 12 — Teach a Network to Invent Names

[⬅ Week 11](week-11.md) · [Course Home](../README.md) · [Week 13 ➡](week-13.md) · [Workbook](../workbook/week-12.md)

---

> ### This week in one sentence
> **While training, the model is handed the true previous letter at every step, so a whole batch of names goes through together; while generating, it is handed its own last guess, so it writes one letter at a time, and when you count, most of what it "invents" turns out to be a name it was trained on.**
>
> **By the end of this chapter you will be able to:**
> - **Turn names into numbers** and build the shifted input that **teacher forcing** needs, with `torch.full` and `torch.cat`
> - **Say what padding does to a loss** and use `F.cross_entropy(..., ignore_index=)` so it does not count
> - **Train a character model** on 200 names and report **train loss** and **validation loss** for the same model, and say what the gap means
> - **Say the difference** between what goes in at each step when training and when generating
> - **Count** how many generated names are already in the training list, and say what the count does and does not show
>
> **New maths:** **none.** One old idea gets a new job: the loss is the **average surprise** (`-ln p`, Level 3 Week 14), and today's question is *which positions get averaged*.
>
> **New syntax:** `F.cross_entropy(..., ignore_index=)` · `torch.full` · `torch.cat` (met in Level 3 Week 27; used here to shift the input) · `import torch.nn.functional as F`. One helper, `draw`, is **given to you** in block 5 and opened next week.
>
> **New words:** **teacher forcing** · **shift right** / **start token** · **padding** and **padding mask** · **generate** (**autoregressive**) · **novelty rate**
>
> **Reading time:** about 35 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60-75 minutes, of which about 25 seconds is the computer training.

> **📌 About the code blocks.** Type the seven blocks below into **one file, `week12.py`**, one under the other with no gap, and run the file after adding each block. Later blocks use names defined by earlier ones. Run it from **the folder that contains `l4lib/`**, because block 1 imports the 231 names from `l4lib.names`. The output under each block is what **that block** prints. Every output shown was printed by a real run on a CPU, with the seeds shown. On a different CPU or PyTorch build the last digit of a loss can move, and a count of generated names can move by a name or two; the shape of every table will not. **The model is real:** a small LSTM with 25,532 numbers, trained for real for 800 steps. **Nothing is scripted and there is no stand-in anywhere.** The 231 names were typed by the course author; they are not from any real list of people. Nothing this week needs the internet.

---

## 🪝 Start Here

Here are twelve names. **Six** are from a list of 231 names somebody typed. **Six** were written by a computer program that read that list. On a piece of paper, before you read on, mark the ones you think the *program* wrote:

`fakori` · `tamara` · `amira` · `dmitri` · `camendid` · `noor` · `clala` · `sigrid` · `andriia` · `kavya` · `arnata` · `heidi`

Write down your six. Then write one more number, a guess: **a program reads 200 of these names and then writes 200 names of its own. How many of its 200 do you think are names it was *given*?** (A number from 0 to 200.)

Keep both papers. We get the real number before the end of the chapter, and the answer to the first paper comes with it. (There is a trap in the first one: "the program wrote it" and "it is not in the list" are two different questions.)

Words to keep in mind:

- **Loss** is the average surprise at the true answer (Level 3 Week 14): `-ln p` for each step, averaged.
- **Validation loss** is the loss on examples the model never trained on (Week 5). It is the column that tells the truth.
- An **LSTM cell** keeps a note `h` and a memory `c`, and its state is the **pair** `(h, c)` (Week 11).

---

## 🧠 The Big Idea

### 1. A name is a list of numbers, and training needs a second list

The model does not read letters. It reads **ids**. In this course `0` is **PAD** (filler, so every name is the same length), `1` is **EOS** (the name has ended), and `2` is `a`, `3` is `b`, and so on. Every name is padded to 8 steps, because the longest name has 7 letters plus the EOS. So `anika` becomes `[2, 15, 10, 12, 2, 1, 0, 0]`: five letters, EOS, two padding.

Here is the question the model is asked at every step: **"here is the letter just said; what comes next?"** So the model needs two grids. The **targets** are the names themselves. The **inputs** are the same names moved **one place to the right**, with a **start token** in front:

```text
input :  START  a   n   i   k   a   EOS  PAD
target:    a    n   i   k   a  EOS  PAD  PAD
```

Read down a column: at each step the model sees the top letter and must say the bottom one. That move is called **shift right**. We use the id of PAD (`0`) as the start token. Nothing real is ever `0`, so a `0` in the input can only mean "nothing has been said yet".

Two pieces of syntax do the shifting. **`torch.full(shape, value)`** makes a grid of that shape with `value` written in every cell; **the shape is a tuple**, like `(231, 1)`. **`torch.cat([a, b], dim=1)`** glues tensors side by side along an axis that already exists; you met it in Level 3 Week 27. And `data[:, :-1]` is "every row, every column except the last": the last column is never an input, because nothing follows it.

Before you run block 1, write down the shape you expect for `start`, for `data[:, :-1]`, and for the glued `inputs`. Then run it.

**Block 1 — the names as numbers, and the shifted input**

Type this into `week12.py`. New: `torch.full`, and `torch.cat` used for the shift.

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

Read the `anika` table down the columns. **Each input is the previous row's target.** That is the whole idea of shifting. At step 6 the input is `1` (EOS: the last thing said) and the target is `0` (padding): the model is shown "the name has ended" and asked for "nothing". Block 2 is about that step.

### 2. Padding is a free answer, and counting it flatters you

The score for one step is how surprised the model was by the right letter: `-ln p`, where `p` is the probability it gave to the true letter. The score for a name is the average of those surprises.

Take the name `uma`. It has **four** real targets (`u`, `m`, `a`, EOS) and **four** padding targets. Padding is easy: after EOS comes PAD, always. A model that has learned nothing about names can still learn "after EOS comes PAD, 98% sure", which costs only `-ln 0.98 = 0.0202` per step.

**Do this on your calculator before you run block 2.** Suppose the model gave the true letter the probabilities `0.5, 0.25, 0.8, 0.1` at the four real steps. Work out `-ln p` for each, and the average of the four. Then work out what the average becomes if you put the four easy padding steps (`0.0202` each) under them and divide by **8** instead of 4. Did the model get better at names?

The function that lets the loss skip the padding is `F.cross_entropy(..., ignore_index=)`. It needs `import torch.nn.functional as F`, where `F.` is the home of functions with no knobs of their own. It takes the **scores** (not probabilities; it applies the softmax itself), one row of scores per position, and the true id for each row. `ignore_index=2` means: **drop every row whose true id is 2**, from the top of the average and from the bottom.

**Block 2 — the padding, by hand and with F.cross_entropy**

New: `import torch.nn.functional as F` and `ignore_index=`. The toy world has three ids, with `2` as its padding id.

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

The by-hand average and `padding ignored` agree to four places: that is your check. `padding counted` is `0.5857`, about half of `1.1513`, and the model has not learned one more letter. **Counting padding makes the loss look better without making the model better.**

### 3. The model

Block 3 defines the model as a sentence: an **embedding** that turns an id into 24 numbers (Week 8), an **LSTM cell** of 64 (Week 11), a **dropout** (Week 5), and a **linear layer** that gives 28 scores, one per id. Read the class from top to bottom and find each part.

Look hard at `forward`. The line `self.step(x[:, t], state)` takes its input from `x[:, t]`, **a column that already exists** before the model runs. That is **teacher forcing**: training feeds the *true* previous letter, so every input is known in advance, and a whole batch of names goes through at once. Keep that line in your head for block 5.

`scores.reshape(-1, VOCAB_SIZE)` flattens the scores from `(231, 8, 28)` to one row per (name, step). The `-1` means "work out this number for me": 1,848. Then `F.cross_entropy` sees `1,848` rows of `28` scores and `1,848` labels.

**Block 3 — the model, untrained**

Add this below block 2. Nothing is trained yet.

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

The model has **25,532** numbers. Of the `1,848` positions, `1,404` are real and `444` are padding (24%). An untrained model gives each of 28 ids about an equal chance, so its loss should be about `ln 28 = 3.3322`, and it is (`3.3455`). Counting padding moves it a little, to `3.3629`.

---

## 🎲 Your Turn

### The Name Audit

Three steps, in this order: **predict, measure, judge.**

**Before you run block 4, write three predictions in pen on workbook page 12.4:**

1. After 800 steps, will the **validation** loss be bigger or smaller than the **train** loss?
2. At steps 100, 200, 400 and 800, will the validation loss go **up**, **down**, or **down and then up**?
3. The number from the first page: out of 200 names the program writes, how many are names it was given?

Do not change them afterwards. A wrong prediction, kept, is worth more than a right one you rewrote.

### Train and validate

We hold back **31** names. The model never trains on them. Every so often we ask for its loss on the 200 names it trained on (**train loss**) and on the 31 (**validation loss**). The function `loss_of` turns dropout off and does not learn; `train` turns dropout on while learning. Those are the two modes from Week 5.

**Block 4 — hold out 31 names, train, print train against validation**

About 2.5 seconds. Copy all seven rows into the table on workbook page 12.4 **with every digit**: `0.906` is not `0.9`.

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

Compare with your predictions. Then compare the last row with `ln 28 = 3.3322`. On names it has **not** seen, the model at step 800 scores *worse than a model that knows nothing*, because it is confident and wrong. Is that a bug? No. It is Week 5's memorising, this time on letters. Notice the shape: train kept falling, and validation fell and then turned round (look at the rows between step 100 and step 200).

One more detail. The last number, `1.001`, is the loss of the final training step with dropout **on**; `0.906` is the same model measured with dropout **off**. Two modes, two numbers.

### Generate

Now the model writes. Read `make_name` against `forward` and answer out loud: **where does the input come from in `forward`? And in `make_name`?** In `forward` it is `x[:, t]`, a column that was there before we started. In `make_name` it is `tok`, which is set from `i`, the last answer: **the model's own pick**. The next input does not exist until the last answer does, so this is one letter at a time. That is the difference the whole week is about.

`draw` is **given to you**; type it in, but you are not asked to explain it. It is a dice-roll: `rng.random()` gives a number between 0 and 1, and the loop adds up the model's probabilities until the total passes the roll, so a letter is picked in proportion to its probability. Next week you open it. The line `scores[PAD] = -1e9` sets the score of padding so low that it is never picked.

**Block 5 — generate: the model's own pick is fed back in**

Add this below block 4. `rng` is seeded, so you get the same twenty names.

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

**Before you count anything**, go down the twenty and mark each one *could be a name* or *could not*. Write the marks on page 12.4. Then find out how many are in the training list by running this one line at the end of `week12.py`:

```python
print(sum(n in train_names for n in twenty))
```

```text
17
```

**17 of the 20** are names from the training list (`alina` and `yash` each came up twice). The three that are not: `naya`, `rusha` and `argek`.

### The audit

Now the count that answers the first page. Block 6 generates 200 names, and asks for each one: *is it in the training list? in the held-back list? in neither?* Then it does the whole thing again for a model trained with the **same recipe but stopped at step 100**. Before you run it, read the printed strings in each group and say which could be names.

**Block 6 — how many generated names are in the training list?**

About 3 seconds. Fill page 12.5, both columns, with every number.

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

Look at the two halves side by side.

| 200 generated names | stopped at step 800 | stopped at step 100 |
|---|:--:|:--:|
| in the training list | 159 (79.5%) | 1 (0.5%) |
| in the held-back list | 0 | 0 |
| in neither | 41 | 199 |
| distinct strings | 147 | 199 |

Now return to the number you guessed on the first page. The real one, for the 800-step model, is **159**. The 800-step model mostly reproduces its list, and the 200 contain only 147 different strings because some are drawn more than once. The 100-step model writes almost nothing from the list, but look at what it writes: `gmana`, `dareltl`, `nios`. Most of those are not names.

**Which model is better at inventing names?** The question has no answer until you say what "better" means. "Not in the list" is a count that a loop can make. "A name" is a judgement that a person makes by reading. Write one sentence for each fact.

The honest sentence for the 800-step model is: *"It mostly reproduces its training list, and about a fifth of the time it makes a string that is not in it."* Do not write "the model invents names". Zero of the 200 are in the held-back list, which is what you would expect from a model that copies its *training* list; 31 names is too few to build a story on, so do not.

### The keeper

Block 7 trains one more model on **all 231** names with the same recipe, and counts again. Next week's code starts from this model. Nothing new is in it.

**Block 7 — the keeper: train on all 231 names, for Week 13**

About 2.5 seconds.

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

`0.934` is the loss with dropout off, and `1.026` is the last training step with dropout on. Next week's first program prints `1.026` as a check, so if yours matches, your recipe is the course's. Back to the first page: `amira`, `arnata`, `clala`, `camendid`, `fakori` and `andriia` were all written by **this** model, and none is in the list. `amira` is a real name in the world. `camendid` and `fakori` are not. "Invented" and "not in the list" are two different questions.

---

## 🔬 Break It On Purpose

Two blocks, both **DELIBERATE**. Add each below block 7 in a scratch copy of `week12.py`. Predict what each will do before you run it.

**1. The shape is not a number.** `torch.full` wants the shape of the grid. What happens if it is given a bare number?

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

Read the last line, slowly. What did `full` want in position 1, and what did it get? Fix it, and write the fix in your Bug Log.

**2. One column too many.** Here the shift was written without dropping the last column of `data`.

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

(Your file name and line numbers will differ, and the long middle of a torch traceback is replaced here by one line. The last line is the real, complete last line.) Read the first printed line, then the last line. Divide each of the two numbers in the last line by 231. What do you get? Which line of block 1 is the fix? Write it in your Bug Log.

---

## 🔑 Wrap Up

1. Say from memory, in your own words: (1) what goes in at each step **during training** and **during generating**, (2) what `ignore_index` is for, (3) what the gap between `0.906` and `3.417` means, and what the count `159 of 200` shows.
2. "Teacher forcing is cheating." What is wrong with that? (Hint: what is the model graded on when it generates?)
3. "Padding is harmless because it's just blanks." Which two numbers from block 2 answer that?
4. The 800-step model has a validation loss above `ln 28`. Someone says "so something is broken." What would you say?

**What we did not do.** We looked at one recipe on one list of 231 typed names, with one model size. We did not test whether the names are good: you read twenty and judged, and that judgement is yours, not a number. 31 held-back names is a small test, so the validation number moves by about a quarter from one training seed to the next; read "much worse than train", not "exactly 3.4". We stopped at step 800 because that is the recipe we carry to next week, not because it is the best place to stop. We used the simplest dice-roll there is. This is a toy that has read 200 names, not a result about real language models; those read billions of characters. What is the same is the two loops: train with the truth in sight, generate on your own output.

Then write this sentence in your Bug Log in your own handwriting:

> **"Training hands the model the true previous letter; generating hands it its own last guess; and when I count, most of what it 'invents' is a name it was trained on."**

---

## 📤 Homework

Complete workbook pages 12.1 to 12.6 in order, and **write predictions before running anything**. Every number in your write-up must have been printed by your own run today (or by your own calculator), with the seed stated.

---

## 📖 What carries into next week

Week 13 keeps the model from block 7 and changes only **how the next letter is chosen**: your dice-roll `draw` gets opened, and you will be asked to predict, before each run, how many names are new and how many are nonsense. Bring your `week12.py` (it must print `1.026` for the keeper) and your table from page 12.5.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **teacher forcing** | training with the *true* previous letter as the input at every step, so all inputs are known in advance and a whole batch goes through together |
| **shift right** | moving the names one place to the right, with a start token in front, to make the inputs |
| **start token** | the id put in front of the input; here it is `0`, the same id as PAD |
| **padding** (PAD) | filler id `0`, used to make every name the same length |
| **padding mask** / `ignore_index` | telling the loss to skip the rows whose true id is the padding id, from the sum and from the count |
| **train loss** / **validation loss** | the loss on names the model trained on, and on names it never saw (from Week 5) |
| **generate** (autoregressive) | writing by feeding the model's own last pick back in as the next input, one letter at a time |
| **novelty rate** | the share of generated names that are *not* in the list the model was trained on; it says nothing about whether they are good names |
| **cross-entropy** | (from Level 3) the average of `-ln p` at the true answer |

---

[⬅ Week 11](week-11.md) · [Course Home](../README.md) · [Week 13 ➡](week-13.md) · [Workbook](../workbook/week-12.md)
