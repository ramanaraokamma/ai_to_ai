# Week 19 — Open the GPT: Heads, Ablations, Synthetic Tasks

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Workbook](../workbook/week-19.md)

---

> ### This week in one sentence
> **You take your own TinyGPT apart, deleting the mask, the places, the residual road and the layer norms one at a time, you learn to spot a model that is cheating, and you look inside three tiny models to name what one attention head does, and then test the name.**
>
> **By the end of this chapter you will be able to:**
> - **Say what an ablation is** and what makes one fair: delete one thing, change nothing else, compare on text the model never trained on
> - **Fill a five-row ablation table** (full, no mask, no positions, no residual, no norm) and write one honest sentence per row
> - **Explain a leak**: why the best number in the table is a cheat, and the test that catches it
> - **Train a tiny GPT on three made-up tasks** (copy, reverse, lookup) and say what score pure guessing would get on each
> - **Name one head from its picture**, and write down what evidence would prove the name wrong
>
> **New maths:** **none.** You take differences of two losses, work out a share, and use `ln` of a number of choices (Week 17).
>
> **New syntax:** **none.** Everything you type is from earlier weeks: `if` switches, keyword arguments with defaults, `nn.Identity()`, `nn.ModuleList`, `torch.randint`, and `imshow` from Level 2.
>
> **New words:** ablation · leak · synthetic task · attention weights (as a picture) · head card · redundant
>
> **Reading time:** about 35 minutes. **In class:** about 70 minutes (one 3.6-minute run sits inside it). **Homework (the workbook):** about 60-75 minutes.

> **📌 About the code blocks.** Each block is a whole file, with its name in the first line. Type the files into **one folder, next to `l4lib/`** (and next to your Week 17 `tinygpt.py`, which you will copy from), and run them from that folder. Every output shown was printed by a real run on a CPU, one thread, with the seeds you see in the files. The losses, scores and samples matched on repeat runs here; a different PyTorch version can change the digits, and **the times in brackets will differ**. **Everything this week is really trained**: the longest file, `text_ablate.py`, runs for about **3.6 minutes**. There is **no scripted backend and no stand-in anywhere this week**, and nothing needs the internet. Blocks marked **DELIBERATE** go wrong on purpose.

![Growing map of all 36 weeks in four term lanes: weeks 1 to 18 are solid, week 19 is tinted pink with a pointer, weeks 20 to 36 are dashed](../figures/fig-w19-0-where-this-fits.svg)

*Figure 19.0 — Week 19, Open the GPT, sits in term 2 on the road from memory to attention. Everything before it is built; everything after it is still ahead.*

---

## 🪝 Start Here

Last week you built the TinyGPT and trusted every part of it: the mask, the place table, the residual road, the layer norms. Did anybody *test* any of them? Somebody proved that some of them helped, somewhere, on something. Today you check on your own model, on your own text.

Before you type anything, take a card and do two things.

1. **Rank** the four parts from "deleting it hurts the model most" to "hurts least": **the mask, the place table, the residual road, the layer norms.**
2. Underneath, write **one part you think will not matter at all.**

Keep the card. We come back to it when the table is full.

---

## 🧠 The Big Idea

### 1. Ablation: delete one thing, change nothing else

A claim like *"every part of the GPT is needed"* can be tested. Take the part out, train again, and compare. The word for this is **ablation**: training a model with **one part deleted** and measuring what changes. A test is only worth reading if it is **fair**. Three rules:

```text
1. Same seed, same steps, same data, same scoring batches.   (Only the deleted part changes.)
2. Compare on text the model was NOT trained on.             (Validation, not training.)
3. If a result is too good, check for a leak before you cheer.
```

Rule 1 is why the script below resets the random dice to the same state before scoring every model: five models scored on five *different* sets of windows could differ by 0.03 for no reason that is about the model.

Rule 3 needs an idea. A **leak** is when the model can see the answer it is being scored on. Its loss comes out very low and means nothing, because the model is not predicting, it is reading. Hold that thought; the table will give you a chance to meet one.

### 2. Made-up tasks: so you know what the right answer looks like

On English text nobody can say what an attention head is *supposed* to do. So we also make **synthetic tasks**: tasks made of numbers, generated on the spot, where we know the right mechanism. Three of them:

```text
copy     3 1 7 7 0 5 | 3 1 7 7 0 5          six symbols, a separator, the same six
reverse  3 1 7 7 0 5 | 5 0 7 7 1 3          the same six, backwards
lookup   a 4 c 9 e 1 b 6 | c  ->  9         four key-and-value pairs, then one key: say its value
```

How often would a model that only guesses be right? On copy and reverse the symbols are drawn from 8 symbols, so a guess is right **1 time in 8 = 0.125**, and the loss on one answer is `ln(8) =` **2.079** (Week 17: `ln` of the number of choices). On lookup the answer is a digit 0 to 9, so a guess is right **1 in 10 = 0.1**. A trained model that scores **1.00** is not guessing.

### 3. One row of a picture

Every place in the window, as it works out its answer, spreads a total of 1.0 of **attention** over the places it is allowed to look at (Week 15). Those spread-out numbers are the **attention weights**. Draw them as a grid and you get a picture: **one row is one place's answer to "where did I look?"**, and one column is a place that was looked at. The mask means nothing is lit above the main diagonal.

> **A picture shows where a head looked. It does not show whether the model needed that look.** That is a second test, and you will run it before the end of the chapter.

---

## 🏗️ Build It

### 4. Four switches in your TinyGPT

Copy your Week 17 `tinygpt.py` to a new file `ablate_model.py`, and add four switches, one for each part: `mask_on`, `pos_on`, `res_on`, `ln_on`. Each one is a keyword argument with a default (Week 1), so `TinyGPT(..., pos_on=False)` reads like English. Say what the model will do **before** you add each:

- `mask_on` around the `masked_fill`: with no mask, every place can see every other place.
- `pos_on` in `forward`: with no place table, the model only knows *which* character, not *where*.
- `res_on`: without the residual road, each sub-layer's output *replaces* `x` instead of being added to it (Week 6: the road the gradient travels on).
- `ln_on`: replace each `nn.LayerNorm` by `nn.Identity()`, a layer that hands its input back unchanged (Week 6).

Two more lines are for **looking**, not for training: `last_weights` keeps the latest attention weights, and `silence` is a list of heads to switch off *after* training to see what they were worth. They do nothing until you use them. One line in the given code is from the future: `weights.detach()` hands back the same numbers, cut loose from training, so keeping them for a picture does not keep the whole training history alive. Copy it; you will meet `.detach()` properly in Week 22.

**`ablate_model.py`** (prints nothing)

```python
# ablate_model.py - Week 19: Week 17's TinyGPT with four switches. Each switch deletes one component.
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)


class Block(nn.Module):
    def __init__(self, d, H, T, mask_on=True, res_on=True, ln_on=True):
        super().__init__()
        self.H = H
        self.mask_on = mask_on
        self.res_on = res_on
        self.ln1 = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d)
        self.register_buffer("mask", torch.tril(torch.ones(T, T)))
        self.ln2 = nn.LayerNorm(d)
        self.up = nn.Linear(d, 4 * d)
        self.act = nn.GELU()
        self.down = nn.Linear(4 * d, d)
        self.last_weights = None                                        # the latest attention weights, kept for looking at
        self.silence = []                                               # heads to switch off (used for testing, not training)
        if not ln_on:
            self.ln1 = nn.Identity()
            self.ln2 = nn.Identity()

    def forward(self, x):
        B, T, d = x.shape
        dh = d // self.H
        h = self.ln1(x)
        q = self.q(h).view(B, T, self.H, dh).transpose(1, 2)
        k = self.k(h).view(B, T, self.H, dh).transpose(1, 2)
        v = self.v(h).view(B, T, self.H, dh).transpose(1, 2)
        scores = q @ k.transpose(-2, -1) / dh ** 0.5
        if self.mask_on:
            scores = scores.masked_fill(self.mask[:T, :T] == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1)
        for h_off in self.silence:
            weights[:, h_off] = 0.0                                    # this head now mixes in nothing
        self.last_weights = weights.detach()
        mixed = (weights @ v).transpose(1, 2).reshape(B, T, d)
        if self.res_on:
            x = x + self.proj(mixed)
            x = x + self.down(self.act(self.up(self.ln2(x))))
        else:
            x = self.proj(mixed)
            x = self.down(self.act(self.up(self.ln2(x))))
        return x


class TinyGPT(nn.Module):
    def __init__(self, V, d, H, L, T, mask_on=True, pos_on=True, res_on=True, ln_on=True):
        super().__init__()
        self.T = T
        self.pos_on = pos_on
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)
        self.blocks = nn.ModuleList([Block(d, H, T, mask_on, res_on, ln_on) for _ in range(L)])
        self.ln_f = nn.LayerNorm(d) if ln_on else nn.Identity()
        self.head = nn.Linear(d, V)
        with torch.no_grad():
            self.head.weight *= 0.1

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok(idx)
        if self.pos_on:
            x = x + self.pos(torch.arange(T))
        for blk in self.blocks:
            x = blk(x)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(B * T, -1), targets.reshape(B * T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, n_new, temperature=1.0):
        for _ in range(n_new):
            logits, _ = self(idx[:, -self.T:])
            probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        return idx
```

### 5. The five-model run on your text

`text_ablate.py` is Week 17's `train.py` wrapped in a function `run(name, mask_on=True, ...)`, called five times: once with everything on, then once with each part off. It uses **800 steps** per model, not Week 17's 1,500, so the whole table takes about 3.6 minutes. It prints one line of numbers and a 70-character sample per model. Two things to notice in the file: `SEED = 0` (rule 1, same seed), and `estimate` resetting the dice (rule 1, same scoring batches).

**Before you press Enter, write down which of the five you think will have the lowest validation loss.**

**`text_ablate.py`** (about 3.6 minutes)

```python
# text_ablate.py - Week 19: train the TinyGPT five times on the typed corpus, each time with one thing deleted. 800 steps each.
import math
import time
import torch
from ablate_model import TinyGPT
from l4lib.corpus import TEXT

SEED = 0
chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]

d, H, L, T, B = 128, 4, 4, 64, 32
STEPS, WARMUP = 800, 50


def get_batch(split):
    src = train_data if split == "train" else val_data
    starts = torch.randint(len(src) - T, (B,))
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + 1:s + T + 1] for s in starts])
    return x, y


@torch.no_grad()
def estimate(model, split, batches=20):
    saved = torch.get_rng_state()                        # the same 20 batches for every model, then put the dice back
    torch.manual_seed(123)
    total = 0.0
    for _ in range(batches):
        x, y = get_batch(split)
        _, loss = model(x, y)
        total += loss.item()
    torch.set_rng_state(saved)
    return total / batches


def run(name, mask_on=True, pos_on=True, res_on=True, ln_on=True):
    torch.manual_seed(SEED)
    model = TinyGPT(V, d, H, L, T, mask_on=mask_on, pos_on=pos_on, res_on=res_on, ln_on=ln_on)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / WARMUP if s < WARMUP
                                              else 0.5 * (1 + math.cos(math.pi * (s - WARMUP) / (STEPS - WARMUP))))
    t0 = time.perf_counter()
    for step in range(STEPS):
        x, y = get_batch("train")
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
    seconds = time.perf_counter() - t0
    train_loss, val_loss = estimate(model, "train"), estimate(model, "val")
    torch.manual_seed(1)
    out = model.generate(torch.tensor([[stoi["t"]]]), 100, 0.8)[0].tolist()
    text = "".join(itos[i] for i in out).replace("\n", " / ")
    print(f"{name:<9} train {train_loss:.3f}  val {val_loss:.3f}  gap {val_loss - train_loss:.3f}  ({seconds:.0f} s)")
    print(f"          {text[:70]}")


run("full")
run("no mask", mask_on=False)
run("no pos", pos_on=False)
run("no res", res_on=False)
run("no norm", ln_on=False)
```
```text
full      train 1.597  val 1.673  gap 0.076  (44 s)
          the caros river the oxxunted bean the feewon as tolle the cacherd rsth
no mask   train 0.070  val 0.077  gap 0.007  (44 s)
          tatattttttttttattttaatttattattttttttatatttottatttaatattatataattattasat
no pos    train 1.451  val 1.739  gap 0.288  (47 s)
          t the wther saken thod wat do the wak feeron t did thery beacot thes w
no res    train 2.664  val 2.679  gap 0.015  (45 s)
          t te te cbr urot thdo iwaardobt gt ah leeeot as td ae tamteir t t rs w
no norm   train 1.150  val 1.478  gap 0.327  (41 s)
          the cast brout. / the old marked on the lepeor and dre thad cared did 
```

The `(N s)` figures change from run to run; nothing else did. Compare your table with your card, then read it row by row.

| Model | Train | Validation | Gap | What to say |
|---|:--:|:--:|:--:|---|
| full | 1.597 | **1.673** | 0.076 | The baseline: Week 17's model at 800 steps (Week 17 reached 0.907 and 1.447 at 1,500). |
| no mask | 0.070 | **0.077** | 0.007 | The best number in the table, and **a leak** (next section). |
| no positions | 1.451 | **1.739** | 0.288 | Fits its training text *better* than the full model, scores *worse* on unseen text, and the gap is nearly four times as big. |
| no residual | 2.664 | **2.679** | 0.015 | **Wrecked.** It has hardly learned anything, which is why train and validation agree. |
| no norm | 1.150 | **1.478** | 0.327 | *Better* than the full model on validation, with a much larger gap. |

Compare each row with the full model by subtraction on **validation** loss: no positions `1.739 - 1.673 = +0.066` (a little worse), no residual `2.679 - 1.673 = +1.006` (much worse), no norm `1.478 - 1.673 = -0.195` (better), no mask `0.077 - 1.673 = -1.596` ("better", and we are about to see why that is not a compliment).

![Five horizontal bars of validation loss, one per TinyGPT with a part deleted, with a dashed line at the full model's 1.673 and crosses on the two that fail](../figures/fig-w19-1-ablation-bars.svg)

*Figure 19.1 — Deleting a part can make the score look better; a very low number needs a leak check before it is believed.*

### 6. The leak

The no-mask sample is `tatattttttt...`, a line of `t` and `a`. That is not writing; it is a model that found a shortcut. With no mask, a place that must predict the next character can look one place ahead, and the place ahead **holds** that very character, which is the answer. Its loss is low because it reads, not because it predicts.

There is a test that catches this, and it does not need a trained model. **Change one later character and see whether the scores at earlier places move.** If the model only looks backwards, they cannot.

**`leak_test.py`**

```python
# leak_test.py - Week 19: change ONE later token. Do the scores at EARLIER places move?
import torch
from ablate_model import TinyGPT

torch.manual_seed(0)
x = torch.randint(0, 28, (4, 64))                     # 4 windows of 64 characters
x2 = x.clone()
x2[:, 40] = (x2[:, 40] + 1) % 28                      # change the character at place 40, and nothing else
for mask_on in (True, False):
    torch.manual_seed(0)
    model = TinyGPT(28, 128, 4, 4, 64, mask_on=mask_on)
    with torch.no_grad():
        a, _ = model(x)
        b, _ = model(x2)
    moved = (a[:, :40] - b[:, :40]).abs().max().item()
    print(f"mask_on={mask_on}: largest change in the scores at places 0-39 = {moved:.6f}")
```
```text
mask_on=True: largest change in the scores at places 0-39 = 0.000000
mask_on=False: largest change in the scores at places 0-39 = 0.001437
```

With the mask, changing the character at place 40 moved the scores at places 0 to 39 by exactly `0.000000`. Without it, they moved by `0.001437`. The second number is tiny because this model is untrained; what matters is **zero against not zero**. Write the sentence in your Bug Log:

> **"A loss is not a score if the model can see the answer."**

### 7. Three made-up tasks, one trainer

While the five-model run is going (if you have a second window), type `tasks.py`. It defines the three tasks as functions that make a batch of numbers, a function `accuracy` that gives the share of answer tokens a model gets right on 1,000 fresh sequences, and `train_task` that trains a small GPT (width 64, 2 heads, 2 blocks). It has no `if __name__ == "__main__"`; it only defines things. Two decisions are worth a look:

- `logits[:, -k:, :]` scores **only the answer places**, not every place. The six symbols before the separator are random and nobody can predict them. If they counted, the loss could not go below `5 x ln(8) / 12 = 0.866`, and a perfect model would look bad.
- `lookup_batch` uses `torch.randperm(6)[:P]` to draw **four different keys**. `torch.randint` could draw the same key twice with two different values, and then no model could know the answer.

**`tasks.py`** (prints nothing)

```python
# tasks.py - Week 19: three made-up tasks, one trainer. Every token is a number; nothing here is text.
import time
import torch
import torch.nn.functional as F
from ablate_model import TinyGPT

N = 6                       # symbols to copy or reverse
SEP = 8                     # the separator token for copy and reverse (symbols are 0..7)


def copy_batch(B, reverse=False):
    s = torch.randint(0, 8, (B, N))
    tail = s.flip(1) if reverse else s
    return torch.cat([s, torch.full((B, 1), SEP), tail], dim=1)          # 6 symbols, SEP, 6 answers = 13 tokens


def lookup_batch(B, P=4):
    keys = torch.stack([torch.randperm(6)[:P] for _ in range(B)]) + 10    # P different keys from 10..15
    vals = torch.randint(0, 10, (B, P))
    pairs = torch.stack([keys, vals], dim=2).reshape(B, 2 * P)            # k v k v k v k v
    pick = torch.randint(0, P, (B,))
    rows = torch.arange(B)
    return torch.cat([pairs, torch.full((B, 1), 16), keys[rows, pick][:, None], vals[rows, pick][:, None]], dim=1)


TASKS = {
    "copy": (lambda B: copy_batch(B), 9, 13, N),            # (batch maker, vocab, length, how many answers at the end)
    "reverse": (lambda B: copy_batch(B, reverse=True), 9, 13, N),
    "lookup": (lookup_batch, 17, 11, 1),
}


def accuracy(model, task, B=1000):
    make, V, length, k = TASKS[task]
    seq = make(B)
    with torch.no_grad():
        logits, _ = model(seq[:, :-1])
    guess = logits[:, -k:, :].argmax(dim=-1)
    return (guess == seq[:, -k:]).float().mean().item()               # share of answer tokens that are right


def train_task(task, steps=600, seed=0, L=2, H=2, mask_on=True, pos_on=True, res_on=True, ln_on=True):
    make, V, length, k = TASKS[task]
    torch.manual_seed(seed)
    model = TinyGPT(V, 64, H, L, length - 1, mask_on=mask_on, pos_on=pos_on, res_on=res_on, ln_on=ln_on)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.0)
    for step in range(steps):
        seq = make(64)
        logits, _ = model(seq[:, :-1])
        loss = F.cross_entropy(logits[:, -k:, :].reshape(-1, V), seq[:, -k:].reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return model, loss.item()
```

Before you trust it, print one batch of each and read the first row out loud (*"that is six symbols, the separator 8, and six answers"*). Add two lines to a scratch file to do it: `print(copy_batch(2))` and `print(lookup_batch(2))`, after `from tasks import copy_batch, lookup_batch`.

### 8. The task table

`task_table.py` trains five models on each task (full, then one part deleted), 600 steps each, and prints the share of answers right. It takes about 50 seconds.

**`task_table.py`**

```python
# task_table.py - Week 19: three tasks, five models each (full, then one thing deleted). 600 steps each. Prints the share of answers right.
import time
from tasks import TASKS, train_task, accuracy

t0 = time.perf_counter()
print(f"{'task':<9}{'full':>7}{'no mask':>9}{'no pos':>8}{'no res':>8}{'no norm':>9}")
for task in TASKS:
    row = [accuracy(train_task(task)[0], task),
           accuracy(train_task(task, mask_on=False)[0], task),
           accuracy(train_task(task, pos_on=False)[0], task),
           accuracy(train_task(task, res_on=False)[0], task),
           accuracy(train_task(task, ln_on=False)[0], task)]
    print(f"{task:<9}" + "".join(f"{a:>{w}.2f}" for a, w in zip(row, (7, 9, 8, 8, 9))))
print(f"{time.perf_counter() - t0:.0f} s for the whole table")
```
```text
task        full  no mask  no pos  no res  no norm
copy        1.00     1.00    0.95    1.00     1.00
reverse     1.00     1.00    0.92    1.00     1.00
lookup      1.00     0.37    1.00    1.00     0.33
48 s for the whole table
```

The chance levels are **0.125** on copy and reverse and **0.1** on lookup. Read the grid in this order.

1. **Full model:** 1.00 on all three. Not guessing.
2. **No mask on copy and reverse: 1.00, for the wrong reason.** The input contains the answer one place ahead. It is the leak again.
3. **No positions costs a few points on copy and reverse (0.95 and 0.92) and nothing on lookup (1.00).** A masked model still has a weak sense of place: place 1 sees one character, place 6 sees six (Week 16, `masked.py`). It does *not* say "positions do nothing".
4. **The lookup column is where things show up.** No mask: **0.37**. This is *not* a leak: the window stops before the answer. No norm: **0.33**.

Read the lookup column with care. This is one seed and one length of training. Whether no-norm's 0.33 is *broken* or just *slow or unlucky* is something this one table cannot say, and you have not tested why no-mask breaks lookup either. Write both down as **open questions**, not findings.

![A grid of share of answers right: three tasks by five models plus a chance column, with ticks on 1.00, crosses on 0.37 and 0.33, and ringed numbers 1 and 2](../figures/fig-w19-2-task-table.svg)

*Figure 19.2 — A perfect score can be a leak; the lookup column is where deleting a part shows up, and its cause is still an open question.*

---

## 👁️ Open the Heads

### 9. Where does each head look?

`heads.py` trains the copy model and prints, for each of its four heads (2 layers, 2 heads each), the place each answer place looks at most, averaged over 500 fresh sequences. It also saves the picture `copy_heads.png`. The window has 12 places: six symbols (0-5), the separator (6), and the answers (positions 6 to 11 are the ones that must produce an answer).

**`heads.py`** (about 4 seconds)

```python
# heads.py - Week 19: train the copy model, then look at what each head looks at.
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tasks import N, copy_batch, train_task, accuracy

model, loss = train_task("copy", L=2, H=2, steps=600)
print(f"copy model: final loss {loss:.4f}   accuracy {accuracy(model, 'copy'):.2f}")

seq = copy_batch(500)
x = seq[:, :-1]                                           # 12 tokens: 6 symbols, SEP, 5 answers
with torch.no_grad():
    model(x)

print("\nwhere does each head look? (average over 500 sequences; rows are the positions that must produce an answer)")
for layer in range(2):
    for head in range(2):
        w = model.blocks[layer].last_weights[:, head].mean(dim=0)      # (12, 12), averaged over the 500 sequences
        print(f"layer {layer} head {head}")
        for q in range(N, 2 * N):                                      # positions 6..11 each produce one answer
            src = int(w[q].argmax())
            print(f"   position {q:2d} looks mostly at position {src:2d}  (weight {w[q, src]:.2f}, that is {q - src} back)")

one = model.blocks[0].last_weights[0]                                   # (heads, 12, 12) for the first sequence
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, (layer, head) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
    w = model.blocks[layer].last_weights[0, head]
    axes[i].imshow(w, cmap="viridis")
    axes[i].set_title(f"layer {layer} head {head}")
    axes[i].set_xlabel("looked at")
    axes[i].set_ylabel("looking")
plt.tight_layout()
plt.savefig("copy_heads.png", dpi=100)
print("\nsaved copy_heads.png")
```
```text
copy model: final loss 0.0016   accuracy 1.00

where does each head look? (average over 500 sequences; rows are the positions that must produce an answer)
layer 0 head 0
   position  6 looks mostly at position  0  (weight 0.99, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.96, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.95, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.96, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.99, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.98, that is 6 back)
layer 0 head 1
   position  6 looks mostly at position  0  (weight 0.97, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.96, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.97, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.98, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.96, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.99, that is 6 back)
layer 1 head 0
   position  6 looks mostly at position  0  (weight 0.88, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.76, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.82, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.86, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.90, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.71, that is 6 back)
layer 1 head 1
   position  6 looks mostly at position  0  (weight 0.86, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.78, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.72, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.92, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.90, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.68, that is 6 back)

saved copy_heads.png
```

Open `copy_heads.png`: four small grids, one per head. Each row is a "looking" place, each column a "looked at" place. The answer rows (6 to 11) have one bright square each, in columns 0 to 5: a stripe running parallel to the main diagonal, six columns to its left. That is the "6 back" of the printout, and it is in all four panels. Nothing is lit above the main diagonal (the mask). The upper rows show a fainter pattern that we did not investigate; say "I do not know what the symbol places are doing" rather than guessing.

### 10. Two more models, and the test that can prove a name wrong

`heads_more.py` does the same for the **reverse** and **lookup** models, and adds the second test. `silence_test` uses the `silence` list from `ablate_model.py` to switch a **trained** head off (it stops mixing in anything) and measures accuracy again, for each head alone and for both heads of a layer.

**`heads_more.py`** (about 7 seconds)

```python
# heads_more.py - Week 19: two more models, two more head cards, and the test that can prove a name wrong.
import torch
from tasks import copy_batch, lookup_batch, train_task, accuracy


def table(model, seq, queries):
    with torch.no_grad():
        model(seq[:, :-1])
    for layer in range(2):
        for head in range(2):
            w = model.blocks[layer].last_weights[:, head].mean(dim=0)
            cells = [f"{q}->{int(w[q].argmax())} ({w[q].max():.2f})" for q in queries]
            print(f"  layer {layer} head {head}:  " + "   ".join(cells))


def silence_test(model, task):
    print(f"  nothing switched off: {accuracy(model, task):.2f}")
    for layer in range(2):
        for head in range(2):
            model.blocks[layer].silence = [head]
            print(f"  only layer {layer} head {head} off: {accuracy(model, task):.2f}")
            model.blocks[layer].silence = []
        model.blocks[layer].silence = [0, 1]
        print(f"  both heads of layer {layer} off: {accuracy(model, task):.2f}")
        model.blocks[layer].silence = []


print("REVERSE  (query position -> the position it looks at most, and its weight)")
rev, _ = train_task("reverse")
table(rev, copy_batch(500, reverse=True), range(6, 12))
silence_test(rev, "reverse")

print("\nLOOKUP   (odd positions hold a value; position 9 holds the asked-for key)")
lk, _ = train_task("lookup")
seq = lookup_batch(500)
table(lk, seq, [1, 3, 5, 7, 9])
silence_test(lk, "lookup")

with torch.no_grad():
    lk(seq[:, :-1])
w = lk.blocks[1].last_weights                                     # (500, 2, 10, 10)
pick_pos = (seq[:, 0:8:2] == seq[:, 9:10]).float().argmax(dim=1)   # which pair held the asked-for key: 0..3
answer_pos = 2 * pick_pos + 1                                       # where that pair's value sits
for head in range(2):
    hit = (w[:, head, 9, :].argmax(dim=-1) == answer_pos).float().mean().item()
    print(f"\n  layer 1 head {head}: at position 9 it looks at the right value in {100 * hit:.0f}% of sequences")
```
```text
REVERSE  (query position -> the position it looks at most, and its weight)
  layer 0 head 0:  6->5 (0.99)   7->4 (0.96)   8->3 (0.97)   9->2 (0.97)   10->1 (0.98)   11->0 (0.96)
  layer 0 head 1:  6->5 (1.00)   7->4 (0.95)   8->3 (0.98)   9->2 (0.98)   10->1 (1.00)   11->0 (0.96)
  layer 1 head 0:  6->5 (0.74)   7->4 (0.78)   8->3 (0.46)   9->2 (0.73)   10->1 (0.53)   11->0 (0.73)
  layer 1 head 1:  6->5 (0.76)   7->4 (0.83)   8->3 (0.65)   9->2 (0.74)   10->1 (0.61)   11->0 (0.81)
  nothing switched off: 1.00
  only layer 0 head 0 off: 1.00
  only layer 0 head 1 off: 1.00
  both heads of layer 0 off: 0.57
  only layer 1 head 0 off: 1.00
  only layer 1 head 1 off: 1.00
  both heads of layer 1 off: 1.00

LOOKUP   (odd positions hold a value; position 9 holds the asked-for key)
  layer 0 head 0:  1->0 (0.97)   3->2 (0.98)   5->4 (0.98)   7->6 (0.98)   9->7 (0.18)
  layer 0 head 1:  1->0 (0.60)   3->3 (0.32)   5->4 (0.44)   7->6 (0.56)   9->6 (0.15)
  layer 1 head 0:  1->0 (0.60)   3->0 (0.29)   5->0 (0.25)   7->3 (0.18)   9->5 (0.27)
  layer 1 head 1:  1->0 (0.64)   3->2 (0.32)   5->0 (0.23)   7->3 (0.17)   9->5 (0.26)
  nothing switched off: 1.00
  only layer 0 head 0 off: 0.48
  only layer 0 head 1 off: 1.00
  both heads of layer 0 off: 0.35
  only layer 1 head 0 off: 0.80
  only layer 1 head 1 off: 1.00
  both heads of layer 1 off: 0.19

  layer 1 head 0: at position 9 it looks at the right value in 100% of sequences

  layer 1 head 1: at position 9 it looks at the right value in 100% of sequences
```

The lines of a head card read like this: `9->7 (0.18)` means "the place 9 looks most at place 7, and the weight is 0.18". In lookup, the odd places hold values, place 8 is the separator, and place 9 holds the asked-for key. The last two lines check, over 500 sequences, whether a layer-1 head at place 9 looks at the value that belongs to the asked-for key.

The copy model has the same test, in its own file (about 4 seconds), so you can write your predictions for the copy heads before you read the lookup numbers.

**`copy_off.py`**

```python
# copy_off.py - Week 19: the switch-off test on the copy model. Each head alone, then both heads of a layer.
from tasks import train_task, accuracy

model, _ = train_task("copy", L=2, H=2, steps=600)
print(f"  nothing switched off: {accuracy(model, 'copy'):.2f}")
for layer in range(2):
    for head in range(2):
        model.blocks[layer].silence = [head]
        print(f"  only layer {layer} head {head} off: {accuracy(model, 'copy'):.2f}")
        model.blocks[layer].silence = []
    model.blocks[layer].silence = [0, 1]
    print(f"  both heads of layer {layer} off: {accuracy(model, 'copy'):.2f}")
    model.blocks[layer].silence = []
```
```text
  nothing switched off: 1.00
  only layer 0 head 0 off: 1.00
  only layer 0 head 1 off: 1.00
  both heads of layer 0 off: 0.75
  only layer 1 head 0 off: 1.00
  only layer 1 head 1 off: 1.00
  both heads of layer 1 off: 1.00
```

---

## 🎲 Your Turn

### Match the Samples

Your teacher cuts the five samples from your table down to 70 characters, shuffles them and labels them A to E. Match each to its model (full, no mask, no positions, no residual, no norm) and write **one piece of evidence** per card. Use the train, validation and gap columns as well as the text. Two of them will be hard to tell apart. If you cannot tell two apart, say so: a sample is one draw, and the loss can rank close models when a sample cannot.

### Head Detective

Four cards, made from the printouts above (your teacher may give you the lines on paper):

| Card | Task and head | What to use |
|:--:|---|---|
| A | **Copy**, layer 0 head 0 | its lines in the `heads.py` printout |
| B | **Reverse**, layer 0 head 0 | its line in the `heads_more.py` printout |
| C | **Lookup**, layer 0 head 0 (places 0-7 pairs, 8 is the separator, 9 is the asked-for key) | its line in the `heads_more.py` printout |
| D | **Lookup**, layer 1 head 0, looking from place 9 | the last check in `heads_more.py` |

For each card write:

1. **In one sentence, what is this head doing?**
2. **A name, three words or fewer.**
3. **One test that would show your name wrong.**

Three questions to ask yourself while you work. *Does this head's job depend on the input, or is it the same on every input?* *If I gave the copy model different symbols, where would card A look?* *If I took this head out, what do I expect?* **Write your prediction for the last one before you read the switch-off lines** in `copy_off.py` and `heads_more.py`. Then read them.

**The sentence to end on.** A stripe of light in a picture tells you where a head looked. In the copy and reverse models, four heads light the same stripe, and the switch-off numbers for one head alone are the same as with nothing switched off. In the lookup model, switching off a single head can change accuracy a lot. **What does that do to a head's name?**

### Predict, then run

In `text_ablate.py`, change `STEPS, WARMUP = 800, 50` to `STEPS, WARMUP = 400, 50`. **Before you run it**, write down whether the order of the five rows will stay the same. Report what you measure. Do not borrow anybody else's number.

---

## 🔬 Break It On Purpose

Three mistakes that stop the program with an error message. Write down what you expect before you run each.

**DELIBERATE 1: a typo in a switch name.**

```python
# bad_typo.py - DELIBERATE: a typo in a switch name.
from tasks import train_task

model, loss = train_task("copy", steps=10, pos_off=True)
```
```text
Traceback (most recent call last):
  File "bad_typo.py", line 4, in <module>
    model, loss = train_task("copy", steps=10, pos_off=True)
TypeError: train_task() got an unexpected keyword argument 'pos_off'
```

The last line names the exact word that is wrong. Keyword arguments with defaults turn a typo into an error. In your Bug Log: what would have happened if `train_task` took a plain dictionary of settings instead?

**DELIBERATE 2: a picture of too many axes.**

```python
# bad_imshow.py - DELIBERATE: imshow handed all of last_weights, which has four axes.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tasks import copy_batch, train_task

model, _ = train_task("copy", steps=50)
model(copy_batch(8)[:, :-1])
plt.imshow(model.blocks[0].last_weights)
```
```text
Traceback (most recent call last):
  File "bad_imshow.py", line 9, in <module>
    plt.imshow(model.blocks[0].last_weights)
    ... frames inside matplotlib (elided) ...
TypeError: Invalid shape (8, 2, 12, 12) for image data
```

`(8, 2, 12, 12)`: say the four axes in words before you fix anything (sequence, head, looking, looked at). `imshow` draws a grid, and a grid has two axes. What index gives you one sequence and one head?

**DELIBERATE 3: a head switched off before training.**

```python
# bad_silence.py - DELIBERATE: a head switched off BEFORE training. The switch is for testing a trained model.
import torch
from ablate_model import TinyGPT
from tasks import copy_batch

torch.manual_seed(0)
model = TinyGPT(9, 64, 2, 2, 12)
model.blocks[0].silence = [0]                          # head 0 of layer 0 off, then we train
seq = copy_batch(64)
_, loss = model(seq[:, :-1], seq[:, 1:])
loss.backward()
```
```text
Traceback (most recent call last):
  File "bad_silence.py", line 13, in <module>
    loss.backward()
    ... frames inside torch (elided) ...
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation: [torch.FloatTensor [64, 2, 12, 12]], which is output 0 of SoftmaxBackward0, is at version 1; expected version 0 instead. Hint: enable anomaly detection to find the operation that failed to compute its gradient, with torch.autograd.set_detect_anomaly(True).
```

The shape `[64, 2, 12, 12]` is a batch of 64, 2 heads, and 12 by 12 attention weights. The switch writes zeros *into* the weights, which the backward pass still needs. Where in this chapter did we set `silence`, and when? (Hint: the switch is for testing a trained model.)

---

## 🧭 What was shown, and what was not

**Shown:**
- In this small model, on this text, at 800 steps, with one seed: deleting the **residual road** wrecked it (validation 2.679 against 1.673); deleting the **positions** cost a little (1.739); deleting the **layer norms** made it *better* on validation (1.478); deleting the **mask** gave the best number of all (0.077) and it is a **leak**.
- A loss is not a score when the model can see the answer; the future-change test catches it (0.000000 with the mask, not zero without).
- On three made-up tasks the full tiny GPT scores 1.00, and chance is 0.125, 0.125 and 0.1.
- In the copy model all four heads look exactly six places back at the answer places, and switching off any one of them changes nothing; in the lookup model two heads do matter, and the printout says so.

**Not shown:**
- **That the layer norm is useless.** We saw that it was *better without it*, at 800 steps, in this small model. We did **not** find out why. The larger gap (0.327) is a reason not to prefer it.
- **That positions do not matter.** No positions was 1.00 on lookup and worse on copy and reverse. It is one effect on one task.
- **That no mask breaks lookup for a known reason.** We saw 0.37 and did not find out why.
- **That the ordering of the table would survive 1,500 steps, dropout or another seed.** One seed and 800 steps. The smallest effect (positions, +0.066) is the one to trust least.
- **That attention weights explain the model.** They show where a head looked. Only the switch-off test touches whether the head was needed, and it switches a head off *after* training, so it does not say what the model would have learned if the head never existed.
- **That any of this is how a large model works.** We looked inside models of about 100,000 knobs on made-up numbers. We did not look at a large one.

---

## 🔑 Wrap Up

1. What is an ablation? Write the three rules of a fair one.
2. The no-mask row has the lowest validation loss of all five. Why is that not a result about the mask? What test shows it?
3. What is a leak? How is it different from a model that is simply good?
4. The copy model has four heads that all look six places back. Switch any one off and nothing changes. What does the bright stripe prove, and what does it not prove?
5. Go back to your ranking card. Which part did you put first, and which did you put as "will not matter"? What surprised you?

Then write this sentence in your Bug Log in your own handwriting:

> **"I delete one thing and change nothing else; I compare on text the model never saw; I check for a leak when a number looks too good; and a head's name is a claim that needs a test that could prove it wrong."**

**A look ahead.** Next week the characters go away. The model will see pieces of words, and you build the piece-maker yourself, by counting the most common pair.

---

## 📤 Homework

Complete workbook pages 19.1 to 19.6. **Write your predictions before you run anything**: a guess written after the run is not a guess. Every number you write must have come from your own run in the last 24 hours, with the seed stated.

**Optional.** Change `SEED = 0` to `SEED = 1` in `text_ablate.py` and run the table again (another 3.6 minutes). Which signs of the differences in section 5 survived? Which were smaller than the change between the two seeds?

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **ablation** | training a model with one part deleted, everything else the same, and comparing the scores |
| **leak** | the model can see the answer it is scored on, so a low loss means nothing |
| **synthetic task** | a task made of generated numbers, chosen so that the right mechanism is known |
| **attention weights** | the numbers a head spreads over the places it may look at; drawn as a grid, one row per looking place |
| **head card** | the printed table of "place looks at place (weight)" for one head |
| **redundant** | a part that can be removed with no loss because another part does the same job |
| **switch-off test** | set a trained head's weights to zero and measure accuracy again; the test that can prove a head's name wrong |

---

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Workbook](../workbook/week-19.md)
