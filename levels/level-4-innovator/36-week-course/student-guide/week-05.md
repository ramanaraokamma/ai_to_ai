# Week 5 — Four Ways to Stop Memorising

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Next ➡ Week 6](week-06.md) · [Workbook](../workbook/week-05.md)

---

> ### This week in one sentence
> **A network can get a perfect score on the points it practised on and get worse on every point it has not seen, so the number to trust is the validation loss, and four cheap cures (stop early, drop units, shrink weights, jiggle the inputs) all pull it back down.**
>
> **By the end of this chapter you will be able to:**
> - **Recognise overfitting from two numbers:** training loss near zero, validation loss far above it and rising
> - **Keep a snapshot of the best weights** with `copy.deepcopy(model.state_dict())`, and say why a plain `state_dict()` is not a snapshot
> - **Say what `nn.Dropout(p)` does** in `train()` mode and in `eval()` mode
> - **Draw fresh jitter every epoch** with `rng.normal(0, s, size=...)` and shuffle with `torch.randperm(n, generator=g)`
> - **Fill a four-column table** (best epoch, best validation loss, final validation loss, what you would ship) and say which column tells the truth
>
> **New maths:** **none.** The only arithmetic is one multiplication by a number just under 1: `1 − 0.003 × 0.3 = 0.9991`.
>
> **New syntax:** `nn.Dropout(p)` · `copy.deepcopy(model.state_dict())` · `rng.normal(0, s, size=...)` · `torch.randperm(n, generator=g)`
>
> **Reading time:** about 40 minutes. **Homework:** about 60–75 minutes.

> **📌 About the code blocks.** Each file is its own file; the ones that say `from lab import *` need the `lab.py` you build in Step 3, in the same folder. If you paste a block on its own and get `NameError` or `ModuleNotFoundError: No module named 'lab'`, that is why; nothing is broken. The blocks marked **DELIBERATE ERROR** are broken on purpose. Every output shown was printed by a real run on a CPU with a seed set. Your numbers should match to every digit shown, except that file paths inside an error message will be your own; if a single-seed loss differs in the third decimal, compare the five-seed means and the shape of the curve instead. Every training run this week is a **real** network trained for real. The jitter is real numpy noise: it is an *invented* extra training example, not new data. Nothing this week needs the internet, and nothing is a language model.
>
> **Before you start:** `l4lib` must be importable. From inside the `36-week-course` folder, once per terminal: `export PYTHONPATH="$PWD"`. If you see `ModuleNotFoundError: No module named 'l4lib'`, that is the fix.

---

## 🪝 Start Here

At the end of Week 4 you saw a training loss of `0.000` sitting beside a validation loss several times larger. This week we make that happen on purpose, in a smaller and noisier problem: the two spirals again, but with **only 120 training points** and 360 separate validation points. The network is the Week 1 network (16,962 parameters, which is 141 for every training point). Nothing is changed except that we do not stop it. Here is one run, seed 0, with no cure at all:

```text
 epoch   train    val
     0   0.691   0.688  ###########################
    25   0.217   0.220  ########
    50   0.155   0.196  #######
    75   0.123   0.214  ########
   100   0.021   0.320  ############
   125   0.032   0.507  ####################
   150   0.001   0.694  ###########################
   175   0.000   0.792  ###############################
   200   0.000   0.840  #################################
   225   0.000   0.877  ###################################
   249   0.000   0.906  ####################################

best val 0.179 at epoch 59
final val 0.906   final train 0.000
```

Before you read any further, write in your Bug Log:

1. Is the network getting *better* or *worse* between epoch 100 and epoch 249? Which column are you looking at when you decide?
2. The training loss reaches `0.000`. Does that prove the model is good? What is it compared with?
3. Which epoch would you have wanted to stop at? Could you know that epoch while the run was still going?
4. Guess: what could you do to the *network*, the *weights*, the *data* or the *run* to keep the validation column from climbing? Write down four ideas, however silly.

You will write the code that produced this table today, then test four cures on it. Your four ideas will probably turn out to be close to the four we test.

---

## 🧠 The Big Idea

### 1. Learned versus memorised

A model that has **learned** has found something true about *all* spiral points. A model that has **memorised** has found something true about *these 120 points*, including their accidents: a point that landed on the wrong arm because the noise pushed it there. You cannot tell the two apart from the training loss, because both score well on the points they practised on. You can tell them apart from **two numbers side by side**: the loss on points it trained on, and the loss on points it has never seen. The second is the **validation loss**.

The word for a model that has memorised is **overfitting**. We caused it on purpose, with only 120 points and a network big enough to remember them all. (In Week 7 you will meet the same network at 840 points, where there is little to memorise and some of today's cures do nothing. That is an honest result too.)

### 2. The four cures

They are four different answers to one question: *how do I stop the network fitting the accidents?*

| Cure | What it changes | In words |
|---|---|---|
| **Early stopping** | Nothing about the network or the data | Keep the best weights seen so far; stop when it has not improved for `patience` epochs |
| **Dropout** | How the network trains | While training, randomly zero a share of the numbers inside the network |
| **Weight decay** | How the weights are updated | Shrink every weight by a tiny fee at every step |
| **Augmentation (jitter)** | The data | Each epoch, show slightly shaken copies of the training points |

### 3. The only arithmetic this week

**Weight decay is a fee.** In `AdamW`, before anything else at each step, every weight is multiplied by `1 − lr × weight_decay`. With `lr = 0.003` and `weight_decay = 0.3`:

```text
1 − 0.003 × 0.3  =  1 − 0.0009  =  0.9991
```

A weight of 1.0 becomes 0.9991 after one step, and after two steps `0.9991 × 0.9991 = 0.9982` (four places). That is the whole mechanism: a tiny shrink on every weight whether or not the loss cares. Weights the loss needs push back; weights that only helped memorise an accident have nothing pushing back, so they drift towards zero. **Do the two steps on a calculator now.** Do not try many steps by hand; the program will do that below and you will just read it.

**Dropout keeps a share and scales the survivors.** With `p = 0.5` each number is zeroed with probability one half, and every survivor is multiplied by `1 / (1 − p) = 1 / 0.5 = 2`. So a row of ones becomes a mixture of zeros and twos, and *on average* it is still one: `0.5 × 2 + 0.5 × 0 = 1`. Check with `p = 0.3`: survivors are multiplied by `1 / 0.7`, which is `1.4286`.

**Patience is a counter.** The rule, said aloud: *keep the best value so far and the epoch it happened. After every epoch, if the best was `patience` or more epochs ago, stop.* You will do it with a pencil on ten numbers before the computer does.

### 4. "Label-preserving"

A jittered spiral point is a new training example **only if its class is still true**. Among your 120 points, the *median* distance from a point to the nearest point of the other class is about **0.57** (in the units the network sees; this was measured for you with a script you will not write until later). Noise of size `s` in each of two coordinates moves a point by about `s × 1.41`. So `s = 0.1` moves it about 0.14 and `s = 0.5` about 0.71. Hold both numbers in your head; Part 3 of Your Turn asks you to use them.

### 5. The four new lines of syntax

**`nn.Dropout(p)`.** A layer with no weights. In `train()` mode it zeroes each incoming number with probability `p` and multiplies the rest by `1 / (1 − p)`. In `eval()` mode it does nothing at all. `p` is a share between 0 and 1, not a percentage. You have seen `Dropout(p=0.0, inplace=False)` in the Week 1 printout of the network; today those lines wake up.

**`copy.deepcopy(model.state_dict())`.** Read it inside out. `model.state_dict()` is a dictionary from each layer's name to its tensor of weights. **It hands you the live tensors, not copies.** `copy.deepcopy(...)` makes a genuinely independent copy of the whole dictionary. So the result is a snapshot that later training cannot overwrite.

**`rng.normal(0, s, size=...)`.** Draw random numbers from a bell curve centred on 0 with typical size `s`, from the seeded generator `rng = np.random.default_rng(seed)` you have used since Level 3. `size=` takes a **shape**: `size=5` gives five numbers, `size=(2, 3)` a 2×3 grid, `size=Xs.shape` one number per coordinate of every training point. The result is **float64**, and the network's weights are float32, so it must be converted with `torch.tensor(noise, dtype=torch.float32)`.

**`torch.randperm(n, generator=g)`.** A shuffled list of the integers `0 … n−1`, drawn from a seeded generator `g = torch.Generator().manual_seed(seed)`. Write `generator=` as a keyword. With 120 points and batch 40, `order[0:40]` is batch 1, `order[40:80]` batch 2 and `order[80:120]` batch 3. Nothing is dropped, because `120 // 40 = 3` exactly (a Week 4 idea).

---

## 💻 Try It Yourself

### Step 1 — the four constructs, one at a time

Make a folder for this week's files. Type each of these as its own file and run it. Each takes under a second.

```python
# dropout_demo.py
import torch
import torch.nn as nn

torch.manual_seed(0)
drop = nn.Dropout(0.5)
x = torch.ones(10)

drop.train()
print("train mode:", drop(x))
print("train mode:", drop(x))
drop.eval()
print("eval mode: ", drop(x))

# the share that survives, over many draws
drop.train()
big = torch.ones(100000)
out = drop(big)
print("share kept:", (out != 0).float().mean().item())
print("value of a survivor:", out.max().item())
print("average of the output:", out.mean().item())
```

```text
train mode: tensor([0., 0., 2., 0., 0., 0., 2., 2., 0., 2.])
train mode: tensor([2., 2., 2., 0., 2., 2., 2., 2., 0., 0.])
eval mode:  tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
share kept: 0.49924999475479126
value of a survivor: 2.0
average of the output: 0.9984999895095825
```

The exact pattern of zeros and twos is seeded, so yours will match. Three facts matter: survivors are `2.0`, about half survive, and `eval()` passes every number through.

```python
# alias_demo.py
import copy
import torch
import torch.nn as nn

torch.manual_seed(0)
lin = nn.Linear(1, 1, bias=False)
alias = lin.state_dict()                   # NOT a copy
snap = copy.deepcopy(lin.state_dict())     # a real copy
print("before training:  alias", round(alias["weight"].item(), 4), "  snapshot", round(snap["weight"].item(), 4))

opt = torch.optim.SGD(lin.parameters(), lr=0.5)
loss = (lin(torch.tensor([[2.0]])) - 10.0) ** 2
loss.backward()
opt.step()
print("after one step:   alias", round(alias["weight"].item(), 4), "  snapshot", round(snap["weight"].item(), 4))
print("live weight now:", round(lin.weight.item(), 4))
```

```text
before training:  alias -0.0075   snapshot -0.0075
after one step:   alias 20.0225   snapshot -0.0075
live weight now: 20.0225
```

Both started equal. After one training step, one of them moved with the live weight and one did not. Which is which, and what does that tell you about why `deepcopy` is not optional? Write it in your Bug Log. (The step is huge because the squared error `(2w − 10)²` is steep at the start; the size is not the point.)

```python
# jitter_demo.py
import numpy as np
import torch

rng = np.random.default_rng(0)
print(rng.normal(0, 0.1, size=5))
print(rng.normal(0, 0.1, size=(2, 3)))

rng = np.random.default_rng(0)
noise = rng.normal(0, 0.3, size=100000)
print("mean", round(noise.mean(), 4), " spread", round(noise.std(), 4))

from lab import Xs
rng = np.random.default_rng(0)
jittered = Xs + torch.tensor(rng.normal(0, 0.1, size=Xs.shape), dtype=torch.float32)
print(Xs[:3])
print(jittered[:3])
print("biggest move of any coordinate:", (jittered - Xs).abs().max().item())
```

```text
[ 0.01257302 -0.01321049  0.06404227  0.01049001 -0.05356694]
[[ 0.03615951  0.1304      0.0947081 ]
 [-0.07037352 -0.12654215 -0.06232745]]
mean -0.0003  spread 0.3
tensor([[ 0.1602, -1.4562],
        [-0.8742,  0.0270],
        [ 1.8985, -0.9444]])
tensor([[ 0.1728, -1.4694],
        [-0.8102,  0.0375],
        [ 1.8450, -0.9082]])
biggest move of any coordinate: 0.31063368916511536
```

(This file does `from lab import Xs`, so make `lab.py` in Step 3 first, or come back to it.) The first two lines show what `size=` means. In the last block each coordinate moved by about a tenth, and the biggest move of any of the 240 coordinates was 0.31, about three times the noise size.

```python
# decay_demo.py
import torch
import torch.nn as nn

# One weight, a gradient of exactly zero, so ONLY the decay acts.
for wd in [0.0, 0.3]:
    w = nn.Parameter(torch.tensor([1.0]))
    opt = torch.optim.AdamW([w], lr=0.003, weight_decay=wd)
    for step in range(1, 751):
        w.grad = torch.zeros(1)
        opt.step()
        if step in (1, 2, 10, 750):
            print(f"wd {wd}  after {step:>3} steps: w = {w.item():.4f}")

fee = 1 - 0.003 * 0.3
print("by hand, one step:  1 - 0.003 * 0.3 =", round(fee, 4))
print("by hand, two steps: that times itself =", round(fee * fee, 4))
```

```text
wd 0.0  after   1 steps: w = 1.0000
wd 0.0  after   2 steps: w = 1.0000
wd 0.0  after  10 steps: w = 1.0000
wd 0.0  after 750 steps: w = 1.0000
wd 0.3  after   1 steps: w = 0.9991
wd 0.3  after   2 steps: w = 0.9982
wd 0.3  after  10 steps: w = 0.9910
wd 0.3  after 750 steps: w = 0.5090
by hand, one step:  1 - 0.003 * 0.3 = 0.9991
by hand, two steps: that times itself = 0.9982
```

The gradient here is set to exactly zero, so **only the fee acts**. Your hand arithmetic matches steps 1 and 2. What happens in the 750 steps is the program repeating the same multiplication; how to work that out by arithmetic is for Week 10, so just read the number: a weight of 1.0 has been squeezed to 0.5090.

### Step 2 — patience, by hand and then by machine

Take this made-up list of ten validation losses (it is **not** from a run; it is invented so you can do the rule with a pencil):

```text
epoch:  0     1     2     3     4     5     6     7     8     9
val:    0.70  0.40  0.30  0.25  0.26  0.24  0.27  0.28  0.29  0.30
```

On paper, with `patience = 3`: at each epoch write the best value so far, the epoch it happened, and "epochs since best". Stop the first time that last number reaches 3. Write down the epoch you stop at and the epoch of the best value you would keep. Do it again for `patience = 5` and `patience = 1`. **Only then** run this. (The second half of `stopping.py` imports `lab.py` from Step 3, so if you have not built it yet, do Step 3 first and come back.)

```python
# patience.py
def when_to_stop(val_losses, patience):
    """Return (best_epoch, stop_epoch). stop_epoch is None if the run never stops."""
    best_val, best_ep = float("inf"), -1
    for ep, v in enumerate(val_losses):
        if v < best_val:
            best_val, best_ep = v, ep
        if ep - best_ep >= patience:
            return best_ep, ep
    return best_ep, None
```

```python
# stopping.py
from patience import when_to_stop

made_up = [0.70, 0.40, 0.30, 0.25, 0.26, 0.24, 0.27, 0.28, 0.29, 0.30]
print(when_to_stop(made_up, patience=3))
print(when_to_stop(made_up, patience=5))
print(when_to_stop(made_up, patience=1))

from lab import *
h = fit(seed=0)
print(when_to_stop(h["val"], patience=25))
print(when_to_stop(h["val"], patience=10))
print(when_to_stop(h["val"], patience=5))
```

```text
(5, 8)
(5, None)
(3, 4)
(59, 84)
(24, 34)
(24, 29)
```

Each pair is `(best epoch, stop epoch)`; `None` means the list ended before the rule fired. The first three lines are the made-up list with patience 3, 5 and 1. The last three are the real seed-0 curve with patience 25, 10 and 5. Compare your paper answers with the first three. Then look at the last three: what do the best epochs have in common for patience 10 and 5, and what is different about the best epoch for patience 25? Write one sentence about what a small patience risks.

### Step 3 — build `lab.py`, in pieces

Everything from here on imports one function, `fit`, with four switches: `dropout`, `wd` (weight decay), `jitter` and `patience` (early stopping). Everything else is identical every time: the same 120 points, the same 360 validation points, the same network, the same optimizer (AdamW, `lr=0.003`), batch 40 (so 3 steps per epoch and 750 steps in a 250-epoch run), and the same seed. **One switch per run**, which is the Week 1 rule.

Your teacher will go through the loop with you in pieces. Type it into one file, `lab.py`, exactly as below. Read the comments.

```python
# lab.py
import copy
import numpy as np
import torch
import torch.nn as nn
from l4lib.spirals import get_data, make_model

torch.set_num_threads(1)

Xtr, ytr, Xva, yva = get_data(600, 0.35, 1)      # the noisier spirals, seed 1
Xs, ys = Xtr[:120], ytr[:120]                    # ONLY 120 training points

def fit(*, dropout=0.0, wd=0.0, jitter=0.0, epochs=250, patience=None, batch=40, seed=0):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    g = torch.Generator().manual_seed(seed)
    model = make_model(dropout=dropout)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=wd)
    lossf = nn.CrossEntropyLoss()
    train_hist, val_hist = [], []
    best_val, best_ep, best_state, stopped_at = float("inf"), -1, None, None
    for ep in range(epochs):
        model.train()
        order = torch.randperm(len(Xs), generator=g)
        X = Xs
        if jitter > 0:
            noise = rng.normal(0, jitter, size=Xs.shape)
            X = Xs + torch.tensor(noise, dtype=torch.float32)
        total = 0.0
        for i in range(len(Xs) // batch):
            idx = order[i * batch:(i + 1) * batch]
            loss = lossf(model(X[idx]), ys[idx])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            total += loss.item()
        model.eval()
        with torch.no_grad():
            val = lossf(model(Xva), yva).item()
        train_hist.append(total / (len(Xs) // batch))
        val_hist.append(val)
        if val < best_val:
            best_val, best_ep = val, ep
            best_state = copy.deepcopy(model.state_dict())
        if patience is not None and ep - best_ep >= patience:
            stopped_at = ep
            break
    return {"train": train_hist, "val": val_hist, "best_val": best_val, "best_ep": best_ep,
            "best_state": best_state, "stopped_at": stopped_at, "model": model}
```

Things to find in it before you run anything:

- The three lines at the top of `fit` that seed three different random things (torch's global generator, numpy's `rng`, and the shuffle generator `g`). Why are there three?
- Which line is the new `torch.randperm` and where `generator=` appears as a keyword.
- Where `model.train()` and `model.eval()` are, and what each does to dropout.
- The `if jitter > 0:` block. Is the noise drawn inside or outside the epoch loop? Is it added to `Xs` or to `Xva`?
- The one line that makes the snapshot, and the line that decides when to take one.
- What is `best_ep` used for in the stopping rule?

Now check that the pieces are right:

```python
# checks.py
from lab import *
print(Xs.shape, ys.shape, Xva.shape, yva.shape)
print("class balance in the 120:", ys.float().mean().item())
print("parameters:", sum(p.numel() for p in make_model().parameters()))
print("steps per epoch:", len(Xs) // 40, "  steps in 250 epochs:", 250 * (len(Xs) // 40))
import torch
print(torch.__version__, np.__version__)
```

```text
torch.Size([120, 2]) torch.Size([120]) torch.Size([360, 2]) torch.Size([360])
class balance in the 120: 0.550000011920929
parameters: 16962
steps per epoch: 3   steps in 250 epochs: 750
2.2.1 1.26.4
```

(Your torch and numpy versions may differ.) Read the lines: 55% of the 120 points are class 1, so a model that always says "class 1" scores 55% here; 16,962 parameters; 3 steps per epoch. Check `make_model(dropout=0.3).blocks[0].drop` prints `Dropout(p=0.3, inplace=False)`: that is the wake-up of the line you saw in Week 1.

Now reproduce the opening table. This is the file that printed it:

```python
# hook.py
from lab import *

h = fit(seed=0)                      # no cure at all
print(" epoch   train    val")
for ep in list(range(0, 250, 25)) + [249]:
    bar = "#" * int(40 * min(1.0, h["val"][ep]))
    print(f"{ep:>6}   {h['train'][ep]:.3f}   {h['val'][ep]:.3f}  {bar}")
print()
print(f"best val {h['best_val']:.3f} at epoch {h['best_ep']}")
print(f"final val {h['val'][-1]:.3f}   final train {h['train'][-1]:.3f}")
print(f"gap (val - train) at the best epoch: {h['val'][h['best_ep']] - h['train'][h['best_ep']]:.3f}")
print(f"gap (val - train) at the end:        {h['val'][-1] - h['train'][-1]:.3f}")
```

```text
 epoch   train    val
     0   0.691   0.688  ###########################
    25   0.217   0.220  ########
    50   0.155   0.196  #######
    75   0.123   0.214  ########
   100   0.021   0.320  ############
   125   0.032   0.507  ####################
   150   0.001   0.694  ###########################
   175   0.000   0.792  ###############################
   200   0.000   0.840  #################################
   225   0.000   0.877  ###################################
   249   0.000   0.906  ####################################

best val 0.179 at epoch 59
final val 0.906   final train 0.000
gap (val - train) at the best epoch: 0.089
gap (val - train) at the end:        0.906
```

The last bar is five times as long as the epoch-50 bar. Compare the two gap lines.

### Step 4 — two deliberate errors

Both of these are broken on purpose. Read the **last line** of each error and say what it is asking for before you fix anything.

```python
# err1.py
# DELIBERATE ERROR 1
import torch.nn as nn
drop = nn.Dropout(30)
```

```text
Traceback (most recent call last):
  File "err1.py", line 3, in <module>
    drop = nn.Dropout(30)
  File ".../torch/nn/modules/dropout.py", line 16, in __init__
    raise ValueError(f"dropout probability has to be between 0 and 1, but got {p}")
ValueError: dropout probability has to be between 0 and 1, but got 30
```

```python
# err2.py
# DELIBERATE ERROR 2
import numpy as np
import torch
from lab import Xs, make_model

rng = np.random.default_rng(0)
noisy = Xs + torch.tensor(rng.normal(0, 0.1, size=Xs.shape))
print(noisy.dtype)
model = make_model()
out = model(noisy)
```

```text
Traceback (most recent call last):
  File "err2.py", line 10, in <module>
    out = model(noisy)
  ... (torch's own frames, elided)
  File "l4lib/spirals.py", line 82, in forward
    return self.head(self.blocks(self.stem(x)))
  ... (torch's own frames, elided)
  File ".../torch/nn/modules/linear.py", line 116, in forward
    return F.linear(input, self.weight, self.bias)
RuntimeError: mat1 and mat2 must have the same dtype, but got Double and Float
```

Fix each, and write in your Bug Log what each error message told you. For the second one, note what `print(noisy.dtype)` already said, and how far (in lines) the error is from the line that caused it. A good habit: **print the `dtype` of anything you built from numpy.**

Two more, in the same style (read the message, then fix):

```python
# err3.py
# DELIBERATE ERROR 3
import torch
g = torch.Generator().manual_seed(0)
order = torch.randperm(120, g)
```

```text
Traceback (most recent call last):
  File "err3.py", line 4, in <module>
    order = torch.randperm(120, g)
TypeError: randperm() received an invalid combination of arguments - got (int, torch._C.Generator), but expected one of:
 * (int n, *, torch.Generator generator, Tensor out, torch.dtype dtype, torch.layout layout, torch.device device, bool pin_memory, bool requires_grad)
 * (int n, *, Tensor out, torch.dtype dtype, torch.layout layout, torch.device device, bool pin_memory, bool requires_grad)
```

(In that message, the `*` in the list of allowed arguments is the clue to what is allowed after `n`.)

```python
# err4.py
# DELIBERATE ERROR 4
import numpy as np
from lab import Xs
rng = np.random.default_rng(0)
noise = rng.normal(0, 0.1, size=Xs)
```

```text
Traceback (most recent call last):
  File "err4.py", line 5, in <module>
    noise = rng.normal(0, 0.1, size=Xs)
  File "numpy/random/_generator.pyx", line 1220, in numpy.random._generator.Generator.normal
  File "_common.pyx", line 636, in numpy.random._common.cont
TypeError: expected a sequence of integers or a single integer, got 'tensor([[ 0.1602, -1.4562],
        [-0.8742,  0.0270],
        [ 1.8985, -0.9444],
        [ 0.2605 ...'
```

---

## 🎲 Your Turn — The Four-Cure Table

Open the empty table on **Workbook page 5.4**. You will fill it from your own run.

### Part 1 — one seed (about 10 minutes)

Run this file (about 9 seconds in all). The first block is seed 0; the second runs five seeds, which Part 2 uses.

```python
# table.py
from lab import *

cures = [
    ("no cure",           lambda s: fit(seed=s)),
    ("early stop (p=25)", lambda s: fit(seed=s, patience=25)),
    ("dropout 0.3",       lambda s: fit(seed=s, dropout=0.3)),
    ("weight decay 0.3",  lambda s: fit(seed=s, wd=0.3)),
    ("jitter 0.1",        lambda s: fit(seed=s, jitter=0.1)),
]

print("SEED 0")
print(f"{'cure':<18} {'best epoch':>10} {'best val':>9} {'final val':>10} {'final train':>12}")
for name, go in cures:
    h = go(0)
    print(f"{name:<18} {h['best_ep']:>10} {h['best_val']:>9.3f} {h['val'][-1]:>10.3f} {h['train'][-1]:>12.3f}")

print()
print("FIVE SEEDS (0-4): mean +- spread (lowest .. highest)")
print(f"{'cure':<18} {'best val':>26} {'final val':>26}")
for name, go in cures:
    hs = [go(s) for s in range(5)]
    b = np.array([h["best_val"] for h in hs])
    f = np.array([h["val"][-1] for h in hs])
    print(f"{name:<18} {b.mean():>8.3f} ({b.min():.3f} .. {b.max():.3f})   {f.mean():>8.3f} ({f.min():.3f} .. {f.max():.3f})")
```

Seed 0, as printed on a real run:

```text
SEED 0
cure               best epoch  best val  final val  final train
no cure                    59     0.179      0.906        0.000
early stop (p=25)          59     0.179      0.227        0.053
dropout 0.3                70     0.201      0.634        0.100
weight decay 0.3           61     0.140      0.274        0.053
jitter 0.1                 81     0.130      0.318        0.061
```

Copy the five rows into your table. Then:

1. Which column is picked with hindsight, so you could not know it while training? (Hint: which would need you to see the whole curve first?)
2. The early-stop row repeats the control's `59` and `0.179`. Why? (Think about what the early-stop run *is*.)
3. The early-stop row has two different "final" numbers: `0.227` is the loss at the epoch it stopped. What is the validation loss of the model you would actually **ship**, and where does it live in the code?
4. Add a fifth column to your table called **what I would ship** and fill it for each row. For the no-cure row, what would you ship if you did nothing and just ran 250 epochs?

### Part 2 — five seeds (about 10 minutes)

The second half of `table.py` printed:

```text
FIVE SEEDS (0-4): mean +- spread (lowest .. highest)
cure                                 best val                  final val
no cure               0.204 (0.159 .. 0.264)      0.803 (0.435 .. 1.285)
early stop (p=25)     0.212 (0.159 .. 0.264)      0.351 (0.227 .. 0.589)
dropout 0.3           0.190 (0.122 .. 0.257)      0.575 (0.449 .. 0.732)
weight decay 0.3      0.185 (0.138 .. 0.246)      0.389 (0.274 .. 0.537)
jitter 0.1            0.149 (0.113 .. 0.180)      0.366 (0.197 .. 0.524)
```

Before writing any sentence about a winner, do this with a pencil: for the **best val** column, draw each row's range `(lowest .. highest)` as a bar on a number line from 0.10 to 0.30. Which bars overlap? Now do the same for the **final val** column. Which column separates the cures more? Compare with seed 0: did seed 0 tell you the same story as the five-seed means? Write one sentence about what seed 0 alone would have let you claim, and why you should not.

### Part 3 — how big can the jitter be? (about 8 minutes)

Use the numbers from section 4: the typical gap to the other class is about **0.57** and a typical move for noise `s` is about `s × 1.41`. **Before you run anything**, write a prediction: for which jitter size `s` in `0.05, 0.1, 0.2, 0.3, 0.5` do you expect the lowest validation loss, and for which does the noise start to "lie about the label"? Then run:

```python
# jitter_sweep.py
from lab import *

print(f"{'jitter s':>9} {'best val':>26} {'final val':>26}")
for s in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]:
    hs = [fit(seed=k, jitter=s) for k in range(5)]
    b = np.array([h["best_val"] for h in hs])
    f = np.array([h["val"][-1] for h in hs])
    print(f"{s:>9} {b.mean():>8.3f} ({b.min():.3f} .. {b.max():.3f})   {f.mean():>8.3f} ({f.min():.3f} .. {f.max():.3f})")
```

```text
 jitter s                   best val                  final val
      0.0    0.204 (0.159 .. 0.264)      0.803 (0.435 .. 1.285)
     0.05    0.187 (0.159 .. 0.214)      0.609 (0.324 .. 1.049)
      0.1    0.149 (0.113 .. 0.180)      0.366 (0.197 .. 0.524)
      0.2    0.139 (0.127 .. 0.147)      0.192 (0.130 .. 0.235)
      0.3    0.193 (0.181 .. 0.207)      0.249 (0.224 .. 0.295)
      0.5    0.337 (0.309 .. 0.361)      0.416 (0.337 .. 0.443)
```

How did your prediction do? Sketch the `final val` column as a curve against `s`. What shape is it? At `s = 0.5`, compare the typical move (0.71) with the typical gap (0.57), and with the row for `s = 0.0`.

### Part 4 — two measurements about dropout and the fee

```python
# twice.py
from lab import *
h = fit(dropout=0.3, seed=0, epochs=100)
model = h["model"]
lossf = nn.CrossEntropyLoss()
with torch.no_grad():
    model.train()
    print("train mode, same data, twice:", round(lossf(model(Xva), yva).item(), 4), round(lossf(model(Xva), yva).item(), 4))
    model.eval()
    print("eval mode,  same data, twice:", round(lossf(model(Xva), yva).item(), 4), round(lossf(model(Xva), yva).item(), 4))
```

```text
train mode, same data, twice: 0.3621 0.3263
eval mode,  same data, twice: 0.2807 0.2807
```

Same model, same 360 points, asked twice. Why does train mode give two answers? What would it mean for your reports if `model.eval()` were forgotten?

```python
# weightsize.py
from lab import *

def total_size(model):
    return sum(p.abs().sum().item() for p in model.parameters())

for name, kw in [("no cure", {}), ("weight decay 0.3", dict(wd=0.3))]:
    h = fit(seed=0, **kw)
    print(f"{name:<18} sum of |weights| = {total_size(h['model']):.1f}   final val {h['val'][-1]:.3f}")
```

```text
no cure            sum of |weights| = 1584.2   final val 0.906
weight decay 0.3   sum of |weights| = 1152.9   final val 0.274
```

Work out by what percentage the total size of the weights fell. Where do you see the fee from `0.9991` in this?

### Part 5 — the report

Write your report with this template, filling every blank from your own screen:

```text
On ___ points, with ___ seeds, I ran ___ cures, one at a time.
The best validation loss was within ___ for all of them. The final validation loss differed by ___.
What I would ship is ___ because ___.  One thing I did not test: ___.
```

---

## 🔑 Wrap Up

Answer these before you close the laptop:

1. Why is the training loss alone not enough to say a model is good? What two numbers do you compare?
2. In `fit`, what is the difference between `best_val` and `h["val"][-1]`? Which would you be allowed to brag about for a model you will deploy?
3. Why must the snapshot use `copy.deepcopy`? What does a plain `state_dict()` give you instead?
4. What does `nn.Dropout(0.3)` do in `train()` mode, and what does it do in `eval()` mode?
5. Which of the four cures changed the network or how it trains, which changed the data, and which changed neither?
6. What do you want to know about this next? Put it in your Parking Lot.

Then write this sentence in your Bug Log, in your own handwriting:

> **"A toy result shows a mechanism, not a rate. The ranges between seeds are bigger than most differences between cures, so I say how many seeds I ran."**

Four things you may read elsewhere are **not** shown by anything you measured this week: why dropout works (stories about units depending on each other are plausible but untested at this size), a Bayesian reading of weight decay, double descent, and cross-validation. Write them in the "later" column of your Bug Log. Also note: dropout 0.3 did **not** win here, so do not claim "dropout is the standard cure so it should be best". And `weight_decay=0.3` is a large value that works on this tiny problem; the lesson is the mechanism, not the number.

---

## 📝 Vocabulary

| Word | Meaning |
|---|---|
| **overfitting** | Training loss keeps falling while validation loss turns round and climbs. |
| **memorise / learn** | Memorising is fitting these exact points, accidents included; learning is finding something true about all points of the kind. |
| **validation loss** | The loss on points the model never trained on. The number to trust. |
| **best epoch** | The epoch where the validation loss was lowest. Only known afterwards. |
| **patience** | How many epochs with no new best the run waits before stopping. |
| **snapshot** | An independent copy of the weights, taken with `copy.deepcopy(model.state_dict())`. |
| **dropout** | In training only, randomly zero a share `p` of the numbers inside the network and scale the rest by `1 / (1 − p)`. |
| **weight decay** | A tiny shrink of every weight at every step, by a factor `1 − lr × weight_decay`. |
| **jitter** | Small random noise added to the training inputs, freshly drawn each epoch. |
| **augmentation** | Making extra training examples by changing the real ones in a way that keeps their label true. |
| **label-preserving** | A change after which the class is still the right answer. |

---

## 🏠 Homework

Workbook Week 5, pages 5.1 to 5.5 (about 60 to 75 minutes). Everything you write down must come from **your own run, printed on your own screen, with a seed set, in the last 24 hours**, not from this chapter.

1. **Finish your own `lab.py`** (the four cures, the snapshot and the seed) and run the five rows of `table.py` on **three fresh seeds**: `[5, 6, 7]`. Print the three-seed mean of best epoch, best validation loss and final validation loss for each row.
2. **Pick a jitter size by measurement.** For `s` in `[0.05, 0.1, 0.3]`, run seeds 5, 6 and 7 and print the mean best and final validation loss for each.
3. **Four sentences.** Using your table and the jitter result: (1) which cure had the lowest best validation loss on your seeds, (2) whether that difference is bigger than the spread between seeds, (3) which number you would ship for each row and why, and (4) one thing you did not test.
4. **Optional extension.** Take a label-preserving change that is *not* jitter, for example moving an 8×8 digit one pixel with `np.roll` on scikit-learn's bundled `load_digits()`, and decide **before** running it whether you expect it to help. Then measure with seeds. Whatever you find, ask: "label-preserving" and "useful" are different words, so what would make it useful?

**The one line to write in your Bug Log tonight:** *"Training loss told me how well it practised. Validation loss told me how well it learned."*

---

## 🔮 Next Week

Four cures changed the network, the data or the stopping time, but they all used the same shape of network. Week 6 asks what happens when you change the **inside** of the network: normalisation, residual connections and clipping, on a different kind of problem.

**Before then:** keep `lab.py` and `table.py` exactly as they are. Bring one sentence: *which of the four cures would you try first on a new problem, and which number would you look at to decide?*

---

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Next ➡ Week 6](week-06.md) · [Workbook](../workbook/week-05.md)
