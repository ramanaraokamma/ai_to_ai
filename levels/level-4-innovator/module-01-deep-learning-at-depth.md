# Module 1 — Deep Learning at Depth: Optimizers, Regularization, and Debugging Training

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 4 Home](README.md) · [Next ➡](module-02-sequence-models.md)

**Level 4 · Module 1 · ~6 hours · Prereqs: Level 3 (PyTorch tensors, `nn.Module`, autograd, a training loop you wrote yourself), comfort with derivatives, means, and standard deviations**

---

## 🎯 What You'll Be Able To Do

- **Explain momentum and Adam as improvements on plain SGD**, and pick between them for a given job with a stated reason — not a superstition.
- **Diagnose a training run from its loss curves alone**: learning rate too high, underfitting, overfitting, dead training, or data leakage.
- **Apply dropout, weight decay, early stopping, augmentation, and normalization**, and measure the effect of each one *in isolation* with a controlled experiment.
- **Explain why residual connections let networks get deep** without their gradients dying on the way back.
- **Write your own one-page tuning playbook** that turns a symptom into an action.

---

## 🪝 The Hook

Two students hand in the same assignment: train a network to separate two interleaved spirals. Same laptop, same dataset, same architecture — a 4-layer MLP with 64 hidden units. Byte-for-byte identical model code.

Student A's model reaches 98.9% accuracy in a few seconds.

Student B's model sits at 52.8% — barely better than flipping a coin — for the entire run, and its loss line is as flat as a table.

The difference between them is one number: Student A used `lr=0.003` with AdamW, Student B used `lr=0.03` with plain SGD. That is it. No architecture change, no extra data, no clever trick.

Those numbers are not hypothetical — they are the real output of the script you will run later in this module. Almost everything people call "deep learning intuition" is actually this: knowing which of about ten knobs is causing the shape you are looking at. This module hands you all ten.

---

## 🧠 The Concept

### 1. The optimizer: from SGD to momentum to Adam

#### The plain version you already know

You already wrote this loop in Level 3:

```
for each batch:
    loss = f(model(x), y)
    gradients = d(loss)/d(weights)
    weights = weights - learning_rate * gradients
```

That last line is **stochastic gradient descent (SGD)** — *update every weight by stepping a fixed fraction of the way down its own gradient, using one small batch of data at a time*. "Stochastic" just means "using a random batch instead of the whole dataset."

SGD has exactly one problem, and it is a big one: **it treats every weight the same and it has no memory.**

#### 🍕 Analogy: pushing a shopping trolley down a narrow aisle

Imagine you are pushing a shopping trolley down a long, narrow aisle that slopes gently towards the checkout at the far end. The aisle walls are steep; the floor slope is gentle.

- **Plain SGD** looks at the ground under its wheels and pushes in the steepest downhill direction. But the steepest direction is *sideways into the wall*, not forwards. So the trolley zig-zags wall-to-wall, making tiny progress towards the checkout. If you push harder (bigger learning rate), you just slam into the walls faster.
- **Momentum** lets the trolley keep rolling. The sideways pushes cancel out (left, right, left, right → net zero), but the forward pushes all point the same way and *accumulate*. The trolley stops zig-zagging and starts rolling straight towards the checkout.

This shape — steep in one direction, shallow in another — is called a **ravine**, and it is the normal shape of a neural network's loss surface, not the exception.

#### Momentum, formally

Keep a running "velocity" vector `v` that remembers past gradients:

```
v = β · v + g            (β is typically 0.9)
w = w − lr · v
```

With β = 0.9, `v` is roughly a running average of the last 10 gradients (because 1/(1−0.9) = 10). Consistent directions add up; noisy back-and-forth directions cancel.

**Tiny example.** Gradient is `+2.0` for three steps in a row, β = 0.9:

| step | g | v = 0.9·v + g |
|------|-----|----------------|
| 1 | 2.0 | 0.9·0 + 2.0 = **2.00** |
| 2 | 2.0 | 0.9·2.00 + 2.0 = **3.80** |
| 3 | 2.0 | 0.9·3.80 + 2.0 = **5.42** |

The effective step grows from 2.0 to 5.42 — momentum accelerates along consistent slopes. Now the same thing with a gradient that flips sign: `+2.0, −2.0, +2.0`:

| step | g | v |
|------|-----|-----|
| 1 | +2.0 | +2.00 |
| 2 | −2.0 | 0.9·2.00 − 2.0 = **−0.20** |
| 3 | +2.0 | 0.9·(−0.20) + 2.0 = **+1.82** |

The flip-flopping shrinks. That is the wall-cancelling effect, in numbers.

#### RMSProp: give every weight its own learning rate

Momentum fixes *direction*. It does not fix *scale*. Some weights in a network get gradients around 0.0001; others get gradients around 10. One global learning rate cannot be right for both.

**RMSProp** — *divide each weight's step by the recent typical size of that weight's gradient* — fixes this:

```
s = β₂ · s + (1 − β₂) · g²        (β₂ typically 0.999)
w = w − lr · g / (√s + ε)
```

`s` is a running average of the *squared* gradient, so `√s` is roughly "how big this weight's gradients usually are". Dividing by it means a weight with tiny gradients still gets a decently sized step, and a weight with huge gradients gets reined in.

#### 🍕 Analogy: grading on a curve

A teacher marks two exams. One was brutal (top score 30/100), one was easy (top score 98/100). Comparing raw marks is meaningless. So the teacher divides each student's score by the typical score for that exam. RMSProp does exactly this to gradients: it grades each weight's gradient *on that weight's own curve*.

#### Adam = momentum + RMSProp (+ a bias fix)

**Adam** — *Adaptive Moment Estimation; keep a running average of the gradient (like momentum) and of the squared gradient (like RMSProp), correct both for startup bias, and divide one by the other*:

```
m = β₁·m + (1 − β₁)·g          # 1st moment: direction   (β₁ = 0.9)
s = β₂·s + (1 − β₂)·g²         # 2nd moment: scale       (β₂ = 0.999)
m̂ = m / (1 − β₁^t)             # bias correction, t = step number
ŝ = s / (1 − β₂^t)
w = w − lr · m̂ / (√ŝ + ε)      # ε = 1e-8
```

The bias correction matters because `m` and `s` start at zero, so without it the first few steps would be far too small. With it, **Adam's very first step has size almost exactly `lr`**, no matter how big the gradient is. You will verify that by hand in the worked example.

#### AdamW: the weight-decay bug fix

**Weight decay** is *shrinking every weight slightly towards zero on every step, to discourage the model from relying on any one large weight*. The classic way to do it was to add `λ·w²` to the loss, which adds `2λ·w` to the gradient.

That works fine with SGD. With Adam it breaks, because Adam then *divides the decay term by √ŝ too* — so weights with noisy gradients get decayed less than weights with clean gradients. Nobody wanted that.

**AdamW** — *Adam with weight decay applied directly to the weights, outside the adaptive-scaling machinery*:

```
w = w − lr · m̂ / (√ŝ + ε) − lr · λ · w      # decay term kept separate
```

> **Rule of thumb:** use `torch.optim.AdamW` by default. Use `SGD(momentum=0.9)` when you are training a convolutional vision model for many epochs and you have time to tune the learning rate, because well-tuned SGD often generalizes slightly better there.

| Optimizer | Remembers direction? | Per-weight scale? | Typical LR | Best for |
|---|---|---|---|---|
| SGD | no | no | 0.1 – 1.0 | simple convex-ish problems, teaching |
| SGD + momentum | yes | no | 0.01 – 0.5 | CNNs, long vision training runs |
| RMSProp | no | yes | 1e-3 | RNNs (historically) |
| Adam | yes | yes | 1e-4 – 3e-3 | almost everything, fast baseline |
| AdamW | yes | yes | 1e-4 – 3e-3 | **default for transformers** |

---

### 2. Learning-rate schedules: warmup and cosine decay

The learning rate is not one number. It is a *function of time*.

#### Why decay at all?

Early in training you are far from a good solution, so big steps are useful — you want to cross the map quickly. Late in training you are near a good solution, and big steps just bounce you around it. The loss curve stalls at a plateau that is above what the model can actually reach.

#### 🍕 Analogy: parallel parking

You start with big steering inputs to swing the car roughly into the space. Then you make smaller and smaller corrections. If you kept using the big inputs, you would oscillate forever and never actually park. Learning rate decay is the "smaller corrections as you get closer" rule.

#### Cosine decay

**Cosine decay** — *smoothly reduce the learning rate from its peak to (nearly) zero following the first half of a cosine curve*:

```
lr(t) = lr_peak · 0.5 · (1 + cos(π · t / T))
```

where `t` is the current step and `T` is the total number of steps.

Check the endpoints: at `t = 0`, `cos(0) = 1`, so `lr = lr_peak·0.5·2 = lr_peak`. At `t = T`, `cos(π) = −1`, so `lr = 0`. At the halfway point `t = T/2`, `cos(π/2) = 0`, so `lr = 0.5·lr_peak`. Smooth, no cliffs, no extra hyperparameters.

**Tiny example**, `lr_peak = 0.003`, `T = 1000` steps:

| step t | t/T | cos(π·t/T) | lr |
|---|---|---|---|
| 0 | 0.00 | 1.000 | 0.00300 |
| 250 | 0.25 | 0.707 | 0.00256 |
| 500 | 0.50 | 0.000 | 0.00150 |
| 750 | 0.75 | −0.707 | 0.00044 |
| 1000 | 1.00 | −1.000 | 0.00000 |

#### Warmup

**Warmup** — *start at a near-zero learning rate and ramp linearly up to the peak over the first few percent of training*.

Why? At step 0 the weights are random and Adam's `s` (the running squared-gradient average) is based on almost no data, so its per-weight scaling is garbage. Taking a full-size step on garbage scaling can blow the model into a bad region it never recovers from. Warmup gives Adam a hundred or so steps to build a reliable estimate before you trust it.

```
lr
 ▲
 │        ╭──────────╮
 │       ╱            ╲
 │      ╱               ╲
 │     ╱                  ╲
 │    ╱                      ╲___
 └───┴────────────────────────────▶ step
     warmup        cosine decay
     (2–5%)
```

Rule of thumb: warmup for 2–5% of total steps. It is nearly free and it is the difference between "trains" and "NaN at step 40" for transformers.

---

### 3. Batch size, gradient noise, and the effective learning rate

#### What a batch actually does

A gradient computed on 4 examples is a noisy estimate of the "true" gradient over the whole dataset. A gradient computed on 512 examples is a much cleaner estimate. Specifically, the noise in the gradient shrinks like `1/√B` where `B` is batch size.

Go from batch 16 to batch 64 (4× bigger) and the gradient noise halves (`√4 = 2`).

#### 🍕 Analogy: polling for the school captain election

Ask 4 students who they will vote for and you get a wild estimate. Ask 400 and you get a stable one. Quadrupling your sample halves your margin of error — the same `1/√n` law. A batch is a poll of your dataset.

#### The trade-off nobody tells you: noise is partly *useful*

Small batches are not just "worse big batches". The noise acts like a mild regularizer — it shakes the model out of narrow, brittle minima. In the experiments you will run:

| batch size | final train loss | final val loss | val accuracy |
|---|---|---|---|
| 8 | 0.026 | 0.027 | 99.2% |
| 64 | 0.007 | 0.037 | 98.9% |
| 512 | 0.027 | 0.079 | 97.8% |

(CPU, seed 0, 60 epochs, AdamW lr 3e-3.) Batch 8 fits the training set *worse* (0.026 vs 0.007) but has a tiny train-to-validation gap and the best validation loss. Batch 512 takes far fewer optimizer steps *and* loses the helpful noise, so it does worst on validation here. This is one seed on one small problem: treat the ordering as a pattern to test, not a law.

#### The linear scaling rule

If you double the batch size, the gradient is cleaner, so you can safely take bigger steps. The practical rule:

> **Double the batch size → double the learning rate.**

The quantity `learning_rate / batch_size` is roughly what controls the amount of "shaking" per example. People call `lr × steps` or `lr / B` the **effective learning rate** — *the amount of weight change the model actually experiences per training example, not per step*.

**Tiny example.** You tuned `lr=1e-3` at `batch=32` and it works. You move to a bigger machine and use `batch=128` (4×). Start from `lr=4e-3`, not `1e-3`. If you forget, your model will look like it "got worse on better hardware," which is a genuinely confusing bug to hit.

---

### 4. Regularization: four ways to stop memorizing

**Overfitting** is *the model getting better on data it has seen while getting worse on data it has not*. On a loss plot it is unmistakable: train loss keeps falling, validation loss bottoms out and then climbs.

Here is a real run from the code in this module, with only 120 training points:

```
loss
 ▲
 │ ╲
 │  ╲          val loss ...........•••••••••••  ← climbing = memorizing
 │   ╲.....••••
 │    •••
 │      ╲___________________________  train loss (still falling)
 └─────────┴─────────────────────────▶ epoch
          ~85
       best val = 0.199       final val = 0.495
```

The validation loss reaches 0.199 at epoch 85 and then rises about 2.5x to 0.495 by epoch 250, while train loss keeps dropping to 0.023. The model spent 165 epochs getting worse and never told you.

#### (a) Early stopping

**Early stopping** — *keep a copy of the weights from the best validation epoch, and stop when validation has not improved for `patience` epochs*.

It is the cheapest regularizer in existence and it is the one people most often forget. In the run above it would have saved you 0.296 of validation loss for zero extra compute.

#### (b) Dropout

**Dropout** — *during training only, randomly zero out a fraction `p` of the activations in a layer and scale the rest up by 1/(1−p)*.

#### 🍕 Analogy: the group project where anyone might be absent

If you know exactly one teammate always does the graphs, you will lean entirely on that teammate. Now imagine the teacher randomly sends 30% of the group home each day. Suddenly everyone has to be able to do the graphs. The group becomes robust because no single member is load-bearing.

Dropout does that to neurons: no single neuron can become the one thing the answer depends on.

The 1/(1−p) scaling keeps the *average* activation the same, so the network's outputs don't shrink when you switch to eval mode. **This is why `model.eval()` matters** — it turns dropout off. Forgetting it is the single most common PyTorch bug in existence.

Real numbers from this module's experiments (full dataset, 60 epochs):

| dropout p | train loss | val loss |
|---|---|---|
| 0.0 | 0.007 | **0.037** |
| 0.2 | 0.036 | 0.051 |
| 0.5 | 0.060 | 0.058 |

(CPU, seed 0.) On the full 840-example set, dropout did **not** help: validation loss got slightly *worse* as dropout grew (0.037, 0.051, 0.058), while training loss rose. This model had nothing to fix, because it was not overfitting. Dropout earns its keep when it *is* overfitting: in the 120-example experiment in the Hands-On, dropout 0.3 cut final validation loss from 0.495 to 0.355. Regularization is a medicine, not a vitamin: it only helps when there is a disease.

#### (c) Weight decay

**Weight decay** — *pull every weight a tiny bit towards zero every step*, controlled by `λ` (`weight_decay=` in PyTorch).

#### 🍕 Analogy: a monthly subscription fee for every weight

Every weight pays rent proportional to its size. A weight that is not earning its keep — not reducing loss — gets shrunk out of existence. Only weights that keep pulling the loss down survive at large values. The model ends up simpler.

Typical values: `0.01`–`0.1` for AdamW on transformers, `1e-4`–`5e-4` for SGD on CNNs.

#### (d) Data augmentation

**Data augmentation** — *make new training examples by applying label-preserving changes to the ones you have*.

A flipped photo of a cat is still a cat. A slightly rotated handwritten "7" is still a 7. Adding Gaussian noise to a tabular row is usually still the same class. Augmentation is the only regularizer that adds genuine information about what the model *should* ignore.

⚠️ Label-preserving is the whole game. Horizontally flipping a "b" gives you a "d". Flipping a chest X-ray moves the heart to the wrong side. Always ask "is the label still true?" before adding an augmentation.

| Regularizer | What it costs | When to reach for it |
|---|---|---|
| Early stopping | nothing | always — do this first |
| Weight decay | one hyperparameter | always for AdamW; start at 0.01 |
| Dropout | slower convergence | when train/val gap is large and you can't get more data |
| Augmentation | domain knowledge | images, audio, and any input with known invariances |
| More data | money and time | the best fix, when available |

---

### 5. Batch norm vs layer norm — and why transformers chose layer norm

Both are **normalization** — *rescale a layer's numbers so they have roughly mean 0 and standard deviation 1, then let the model learn a scale `γ` and shift `β` to undo it if it wants*.

Why bother? Because if one layer's outputs drift to a mean of 300 and a standard deviation of 0.001, the next layer's gradients become useless. Normalization keeps every layer operating in a numerically sane range, which lets you use larger learning rates and train deeper stacks.

The two differ **only in what they average over**. Picture a batch of activations as a table, rows = examples in the batch, columns = features:

```
                    feature₁  feature₂  feature₃  feature₄
   example₁    │      1.2      -0.4      3.3      0.1     │
   example₂    │      0.8       2.1     -1.0      0.5     │  ← LayerNorm
   example₃    │     -0.3       0.7      2.2     -0.9     │     normalizes
   example₄    │      1.9      -1.1      0.4      1.4     │     ACROSS a row
                     ▲
                     │ BatchNorm normalizes DOWN a column
```

- **Batch norm** — *normalize each feature using the mean and variance of that feature across the batch* (down a column).
- **Layer norm** — *normalize each example using the mean and variance across that example's own features* (across a row).

#### Why that difference is decisive

| | Batch norm | Layer norm |
|---|---|---|
| Depends on other examples in the batch? | **Yes** | No |
| Works with batch size 1? | No (variance undefined) | Yes |
| Works with variable-length sequences? | Awkward — padding pollutes the stats | Yes, naturally |
| Train and eval behave identically? | No — eval uses stored running averages | Yes, identical |
| Needs syncing across multiple GPUs? | Yes | No |
| Standard in | CNNs / vision | **Transformers / NLP** |

The killer issue for language: sequences have different lengths. Batch norm would compute "the mean value of feature 7 at position 40 across the batch," but half your batch might be shorter than 40 tokens and only contain padding there. The statistic is garbage. Layer norm never looks outside a single token's own vector, so length does not matter at all.

Second killer issue: batch norm makes your model's prediction for one example *depend on the other examples that happened to be in the same batch*. During generation you often run a batch of 1. Batch norm then has to switch to stored running averages, creating a train/inference mismatch that is a classic source of "it worked in training and broke in production."

**RMSNorm** (used in Llama-family models) is layer norm with the mean-subtraction step removed — just divide by the root-mean-square. Slightly cheaper, works about as well.

In the module experiments on this (fully-connected, fixed-length) problem, batch norm actually gave the best validation loss (0.019 vs 0.064 for layer norm) — which is the honest result for a vision-style setup. The transformer preference is about sequences and batch independence, not about raw accuracy on tabular data.

---

### 6. Residual connections, gradient clipping, and reading loss curves

#### Residual connections

Stack 30 layers and something bad happens on the backward pass. The chain rule multiplies a Jacobian for every layer. If each layer's contribution scales the gradient by, say, 0.8, then after 30 layers the gradient is scaled by 0.8³⁰ ≈ **0.00124** — the early layers effectively get no learning signal. This is the **vanishing gradient problem**.

**Residual connection** (or *skip connection*) — *make each block compute `x + f(x)` instead of `f(x)`, so the input passes through untouched alongside the transformation*.

```
        ┌─────────────────────────────────┐
        │                                 │  identity path
   x ───┤                                 ├──▶ (+) ──▶ out
        │                                 │     ▲
        └──▶ [ Norm → Linear → GELU ] ────┘─────┘
                    f(x)
```

Why it fixes things: differentiate `out = x + f(x)` with respect to `x` and you get `1 + f'(x)`. The **1** is a gradient highway. Even if `f'(x)` is tiny, the gradient still flows back through the `+1` at full strength. Thirty stacked residual blocks give `(1 + f'₁)(1 + f'₂)...` which stays near 1 rather than collapsing to 0.001.

#### 🍕 Analogy: the express lane

A 30-stop bus route where each stop loses a few passengers ends up empty. A 30-stop route with an *express lane running alongside it* delivers everyone, and the local stops are optional improvements. Residual blocks make the transformation optional: if a block has nothing useful to add, it can learn `f(x) ≈ 0` and become a pass-through, which is much easier than learning to reproduce the identity function exactly.

This one idea is why 2015's ResNet could be 152 layers deep and why every transformer block on earth is written as `x = x + attention(norm(x))` and `x = x + mlp(norm(x))`.

#### Gradient clipping

Sometimes a single weird batch produces a colossal gradient and one update destroys the model. **Gradient clipping** — *if the total size (norm) of the gradient vector exceeds a threshold, rescale the whole vector down to that threshold, keeping its direction*:

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

Note it preserves *direction* and only limits *length*. `max_norm=1.0` is the near-universal default for language models. It is cheap insurance: it costs nothing when gradients are normal, and it saves the run when they are not.

#### Reading loss curves as diagnostics

This is the skill. Learn these six shapes and you can debug almost anything.

```
(A) HEALTHY                   (B) LR TOO HIGH               (C) DEAD / LR TOO LOW
 │╲                            │  ╱╲  ╱╲                     │
 │ ╲___                        │ ╱  ╲╱  ╲  spiky, or NaN     │────────────────  flat
 │     ╲______                 │╱          rises             │
 └────────────▶                └────────────▶                └────────────▶

(D) OVERFITTING               (E) UNDERFITTING              (F) VAL BELOW TRAIN
 │╲   val ..••••••             │╲                            │╲  train
 │ ╲..••                       │ ╲______  both flatten       │ ╲____
 │  ╲______ train              │          high & together    │ ╲___  val (lower!)
 └────────────▶                └────────────▶                └────────────▶
```

| Shape | Name | Most likely cause | First thing to try |
|---|---|---|---|
| A | Healthy | — | keep going; train longer |
| B | Loss spikes, oscillates, or → NaN | learning rate too high | divide LR by 10; add warmup; clip grads at 1.0 |
| C | Perfectly flat from step 0 | LR too low, LR = 0, dead ReLUs, or `optimizer.step()` never called | print the LR; check `loss.backward()` is called; check `zero_grad()` position |
| D | Train ↓, val ↑ | overfitting | early stop; add dropout/weight decay; get more data |
| E | Both plateau high | underfitting — model or budget too small | bigger model, longer training, higher LR, less regularization |
| F | Val loss *below* train loss | usually **not** a bug: dropout is on during training and off during eval. If the gap is huge, suspect a leak or a too-easy val split | compare train loss recomputed in `eval()` mode |

⚠️ **The single best sanity check in deep learning:** before a real run, take 8 training examples and try to drive the loss to ~0 on just those 8. If your model cannot memorize 8 examples, the bug is in your code, not your hyperparameters. This takes 30 seconds and saves entire afternoons.

---

## 🔍 Worked Example

**Task:** minimize `f(w) = w²` starting from `w = 1.0` with learning rate `0.1`. The gradient is `f'(w) = 2w`. We will run SGD, momentum, and Adam side by side for three steps, showing every number.

The true minimum is at `w = 0`.

### Optimizer 1 — plain SGD

Rule: `w ← w − 0.1 · g`

| step | w before | g = 2w | step size = 0.1·g | w after |
|---|---|---|---|---|
| 1 | 1.0000 | 2.0000 | 0.2000 | **0.8000** |
| 2 | 0.8000 | 1.6000 | 0.1600 | **0.6400** |
| 3 | 0.6400 | 1.2800 | 0.1280 | **0.5120** |

Notice: each step is *smaller* than the last, because the gradient shrinks as we approach zero. SGD slows down exactly when it is close — it never quite arrives. After 3 steps: `w = 0.512`.

### Optimizer 2 — SGD with momentum (β = 0.9)

Rule: `v ← 0.9·v + g`, then `w ← w − 0.1·v`. Start `v = 0`.

| step | w before | g = 2w | v = 0.9·v + g | step = 0.1·v | w after |
|---|---|---|---|---|---|
| 1 | 1.0000 | 2.0000 | 0.9(0) + 2.0 = 2.0000 | 0.2000 | **0.8000** |
| 2 | 0.8000 | 1.6000 | 0.9(2.0) + 1.6 = 3.4000 | 0.3400 | **0.4600** |
| 3 | 0.4600 | 0.9200 | 0.9(3.4) + 0.92 = 3.9800 | 0.3980 | **0.0620** |

After 3 steps: `w = 0.062`. Momentum is **8× closer to the minimum** than SGD.

But watch what happens if we continue:

| step | w before | g = 2w | v | step | w after |
|---|---|---|---|---|---|
| 4 | 0.0620 | 0.1240 | 0.9(3.98) + 0.124 = 3.7060 | 0.3706 | **−0.3086** |

It overshot past zero. That is momentum's cost: it can sail past the target and has to come back. On real, noisy loss surfaces that overshoot is usually worth it — but this is exactly why momentum runs sometimes look bumpier than SGD runs.

### Optimizer 3 — Adam (β₁ = 0.9, β₂ = 0.999, ε = 1e-8)

Start `m = 0`, `s = 0`.

**Step 1** (`w = 1.0`, `g = 2.0`, `t = 1`):
- `m = 0.9(0) + 0.1(2.0) = 0.2`
- `s = 0.999(0) + 0.001(2.0²) = 0.001 × 4 = 0.004`
- `m̂ = 0.2 / (1 − 0.9¹) = 0.2 / 0.1 = 2.0`
- `ŝ = 0.004 / (1 − 0.999¹) = 0.004 / 0.001 = 4.0`, so `√ŝ = 2.0`
- update `= 0.1 × 2.0 / (2.0 + 1e-8) = 0.1 × 1.0 = 0.1`
- `w = 1.0 − 0.1 = ` **0.9000**

👉 **The first step is exactly the learning rate.** The gradient was 2.0, but `m̂/√ŝ` = 1.0 exactly, so the step size is `lr`. This is why Adam's learning rate is so much easier to pick than SGD's: `lr` literally means "how far a weight moves per step," independent of gradient magnitude.

**Step 2** (`w = 0.9`, `g = 1.8`, `t = 2`):
- `m = 0.9(0.2) + 0.1(1.8) = 0.18 + 0.18 = 0.36`
- `s = 0.999(0.004) + 0.001(1.8²) = 0.003996 + 0.003240 = 0.007236`
- `m̂ = 0.36 / (1 − 0.81) = 0.36 / 0.19 = 1.8947`
- `ŝ = 0.007236 / (1 − 0.998001) = 0.007236 / 0.001999 = 3.6198`, `√ŝ = 1.9026`
- update `= 0.1 × 1.8947 / 1.9026 = 0.09958`
- `w = 0.9 − 0.09958 = ` **0.8004**

**Step 3** (`w = 0.8004`, `g = 1.6008`, `t = 3`):
- `m = 0.9(0.36) + 0.1(1.6008) = 0.324 + 0.16008 = 0.48408`
- `s = 0.999(0.007236) + 0.001(2.5626) = 0.0072288 + 0.0025626 = 0.0097914`
- `m̂ = 0.48408 / (1 − 0.729) = 0.48408 / 0.271 = 1.7863`
- `ŝ = 0.0097914 / (1 − 0.997003) = 0.0097914 / 0.002997 = 3.2671`, `√ŝ = 1.8075`
- update `= 0.1 × 1.7863 / 1.8075 = 0.09883`
- `w = 0.8004 − 0.09883 = ` **0.7016**

### Side-by-side

| after step | SGD | Momentum | Adam |
|---|---|---|---|
| 1 | 0.8000 | 0.8000 | 0.9000 |
| 2 | 0.6400 | 0.4600 | 0.8004 |
| 3 | 0.5120 | 0.0620 | 0.7016 |
| step sizes | 0.200, 0.160, 0.128 | 0.200, 0.340, 0.398 | 0.100, 0.0996, 0.0988 |

**Read the last row. It is the whole lesson.**

- SGD's steps **shrink** with the gradient — it is a slave to gradient magnitude.
- Momentum's steps **grow** while the direction is consistent — it accelerates.
- Adam's steps stay **almost exactly `lr`** — it has normalized the gradient away entirely.

On this toy problem Adam looks slowest. On a real network where different weights have gradients differing by a factor of 10,000, Adam's magnitude-independence is exactly what makes it work out of the box while SGD needs careful per-problem tuning.

---

## 💻 Hands-On

### Setup

Everything below runs offline, on CPU only, with torch + numpy + matplotlib already installed. Nothing is downloaded and no accelerator is used: the whole lab takes a few seconds.

### The controlled-experiment harness

Save this as `diagnostics_lab.py`. It generates its own data, defines one network, and gives you a single `run(...)` function where every knob is a keyword argument. **One function, one knob per experiment** — that discipline is the entire point of the module.

```python
"""Module 1 Hands-On: one dataset, one network, one knob at a time."""
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

DEVICE = "cpu"   # this course is CPU-only; do not switch it
print("device:", DEVICE)


# ---------------------------------------------------------------- 1. data
def make_spirals(n_per_class=600, noise=0.22, seed=0):
    """Two interleaved spirals. Hard enough that tuning actually matters."""
    rng = np.random.default_rng(seed)
    xs, ys = [], []
    for c in range(2):
        t = np.linspace(0.35, 3.4, n_per_class)      # radius grows along the arm
        theta = 2.1 * t + c * np.pi                  # class 1 is a half-turn behind
        x1 = t * np.cos(theta) + rng.normal(0, noise, n_per_class)
        x2 = t * np.sin(theta) + rng.normal(0, noise, n_per_class)
        xs.append(np.stack([x1, x2], axis=1))
        ys.append(np.full(n_per_class, c))
    X = np.concatenate(xs).astype(np.float32)
    y = np.concatenate(ys).astype(np.int64)
    p = rng.permutation(len(X))                      # shuffle before splitting
    return X[p], y[p]


X, y = make_spirals()
n_train = int(0.7 * len(X))
Xtr = torch.tensor(X[:n_train], device=DEVICE)
ytr = torch.tensor(y[:n_train], device=DEVICE)
Xva = torch.tensor(X[n_train:], device=DEVICE)
yva = torch.tensor(y[n_train:], device=DEVICE)

# Standardize using TRAIN statistics only. Using val stats here would be a leak.
mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True)
Xtr = (Xtr - mu) / sd
Xva = (Xva - mu) / sd
print("train", tuple(Xtr.shape), "val", tuple(Xva.shape))


# ------------------------------------------------------------- 2. network
class Block(nn.Module):
    """Pre-norm block: norm -> linear -> activation -> dropout, optional residual."""
    def __init__(self, width, norm="none", dropout=0.0, residual=False):
        super().__init__()
        self.fc = nn.Linear(width, width)
        self.act = nn.GELU()
        self.drop = nn.Dropout(dropout)
        self.residual = residual
        if norm == "batch":
            self.norm = nn.BatchNorm1d(width)
        elif norm == "layer":
            self.norm = nn.LayerNorm(width)
        else:
            self.norm = nn.Identity()          # a no-op, so shapes stay identical

    def forward(self, x):
        h = self.drop(self.act(self.fc(self.norm(x))))
        return x + h if self.residual else h   # the gradient highway


class MLP(nn.Module):
    def __init__(self, width=64, depth=4, norm="none", dropout=0.0, residual=False):
        super().__init__()
        self.stem = nn.Linear(2, width)
        self.blocks = nn.Sequential(*[
            Block(width, norm, dropout, residual) for _ in range(depth)])
        self.head = nn.Linear(width, 2)

    def forward(self, x):
        return self.head(self.blocks(self.stem(x)))


# ------------------------------------------------------------ 3. one run
def run(tag, *, lr=3e-3, batch_size=64, epochs=60, optimizer="adamw",
        weight_decay=0.0, dropout=0.0, norm="none", residual=False,
        schedule="none", warmup_frac=0.0, clip=None, seed=0):
    torch.manual_seed(seed)                    # same init for every experiment
    model = MLP(norm=norm, dropout=dropout, residual=residual).to(DEVICE)

    if optimizer == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay)
    elif optimizer == "momentum":
        opt = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9,
                              weight_decay=weight_decay)
    elif optimizer == "adam":
        opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)

    steps_per_epoch = max(1, len(Xtr) // batch_size)
    total_steps = steps_per_epoch * epochs
    warmup_steps = int(warmup_frac * total_steps)

    def lr_mult(step):
        """Returns a MULTIPLIER on the base lr, applied by LambdaLR."""
        if warmup_steps > 0 and step < warmup_steps:
            return (step + 1) / warmup_steps                     # linear ramp up
        if schedule == "cosine":
            prog = (step - warmup_steps) / max(1, total_steps - warmup_steps)
            return 0.5 * (1 + np.cos(np.pi * min(1.0, prog)))    # 1 -> 0 smoothly
        if schedule == "step":
            return 0.1 ** (step // max(1, total_steps // 3))     # /10 every third
        return 1.0                                               # constant lr

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_mult)
    lossf = nn.CrossEntropyLoss()
    hist = {"train": [], "val": [], "acc": [], "lr": [], "gnorm": []}
    g = torch.Generator(device="cpu").manual_seed(seed)

    for ep in range(epochs):
        model.train()                          # dropout ON, batchnorm uses batch stats
        perm = torch.randperm(len(Xtr), generator=g).to(DEVICE)
        running, nb = 0.0, 0
        for i in range(steps_per_epoch):
            idx = perm[i * batch_size:(i + 1) * batch_size]
            loss = lossf(model(Xtr[idx]), ytr[idx])
            opt.zero_grad(set_to_none=True)    # clear last step's gradients
            loss.backward()                    # accumulate this step's gradients
            gn = torch.nn.utils.clip_grad_norm_(   # returns the PRE-clip norm
                model.parameters(), clip if clip else float("inf"))
            opt.step()                         # apply the update
            sched.step()                       # advance the lr schedule
            running += loss.item()
            nb += 1

        model.eval()                           # dropout OFF, batchnorm uses running stats
        with torch.no_grad():
            vlogits = model(Xva)
            vloss = lossf(vlogits, yva).item()
            vacc = (vlogits.argmax(1) == yva).float().mean().item()

        hist["train"].append(running / nb)
        hist["val"].append(vloss)
        hist["acc"].append(vacc)
        hist["lr"].append(opt.param_groups[0]["lr"])
        hist["gnorm"].append(float(gn))

    print(f"{tag:<28} train {hist['train'][-1]:.3f}  "
          f"val {hist['val'][-1]:.3f}  acc {hist['acc'][-1]*100:5.1f}%")
    return hist


# --------------------------------------------------- 4. six controlled runs
results = {}
results["sgd lr=0.03"]            = run("sgd lr=0.03", optimizer="sgd", lr=0.03)
results["momentum lr=0.03"]       = run("momentum lr=0.03", optimizer="momentum", lr=0.03)
results["adamw lr=0.003"]         = run("adamw lr=0.003", lr=3e-3)
results["adamw lr=0.3 (too big)"] = run("adamw lr=0.3 (too big)", lr=0.3)
results["adamw + cosine"]         = run("adamw + cosine", schedule="cosine",
                                        warmup_frac=0.05)
results["adamw + ln + residual"]  = run("adamw + ln + res", norm="layer", residual=True)

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for k, h in results.items():
    ax[0].plot(h["train"], label=k)
    ax[1].plot(h["val"], label=k)
ax[0].set_title("train loss")
ax[1].set_title("val loss")
for a in ax:
    a.set_xlabel("epoch"); a.set_ylabel("cross-entropy"); a.set_yscale("log")
ax[1].legend(fontsize=7)
plt.tight_layout()
plt.savefig("optimizer_comparison.png", dpi=110)
print("saved optimizer_comparison.png")
```

**Expected output** (real CPU run, torch 2.2.1, seed 0; your digits may differ in the last place with another PyTorch version):

```
device: cpu
train (840, 2) val (360, 2)
sgd lr=0.03                  train 0.690  val 0.690  acc  52.8%
momentum lr=0.03             train 0.018  val 0.034  acc  98.6%
adamw lr=0.003               train 0.007  val 0.037  acc  98.9%
adamw lr=0.3 (too big)       train 0.701  val 0.723  acc  46.9%
adamw + cosine               train 0.007  val 0.045  acc  98.9%
adamw + ln + res             train 0.011  val 0.022  acc  99.4%
saved optimizer_comparison.png
```

### Reading that output like an engineer

- **`sgd lr=0.03` → loss 0.690, accuracy 52.8%.** Note that `ln(2) = 0.693` is the loss of a model that outputs 50/50 for a 2-class problem. A loss pinned at 0.69 means *the model has learned literally nothing*. Diagnosis: shape (C), and the cause is that SGD without momentum needs about 10× more learning rate here. Run `run("sgd lr=0.3", optimizer="sgd", lr=0.3)` and you get **train 0.016, val 0.041, acc 98.9%** — same optimizer, same everything, one number changed.
- **`adamw lr=0.3` → loss 0.701, accuracy 46.9%.** Also stuck near `ln(2)`, but for the opposite reason: the steps are so large the model bounces around and never settles. Two very different diseases, one identical-looking flat line. **This is why you never diagnose from the final number alone — you look at the shape of the curve.** Plot them and the difference is obvious: SGD's curve is a flat line, AdamW-at-0.3's is a jagged mess.
- **`momentum` fixed SGD without touching the learning rate.** That is the whole argument for momentum in one line of output.

### Second experiment: manufacture overfitting on purpose

Add this at the bottom. It keeps everything identical but starves the model of training data.

```python
# ------------------------------------------- 5. deliberately overfit
X2, y2 = make_spirals(n_per_class=600, noise=0.35, seed=1)
n2 = int(0.7 * len(X2))
Xtr_full = torch.tensor(X2[:n2], device=DEVICE)
ytr_full = torch.tensor(y2[:n2], device=DEVICE)
mu2, sd2 = Xtr_full.mean(0, keepdim=True), Xtr_full.std(0, keepdim=True)

Xtr, ytr = ((Xtr_full - mu2) / sd2)[:120], ytr_full[:120]   # only 120 examples!
Xva = (torch.tensor(X2[n2:], device=DEVICE) - mu2) / sd2
yva = torch.tensor(y2[n2:], device=DEVICE)

over = {
    "no regularization": run("no regularization", epochs=250),
    "dropout 0.3":       run("dropout 0.3", epochs=250, dropout=0.3),
    "weight decay 0.3":  run("weight decay 0.3", epochs=250, weight_decay=0.3),
}
for name, h in over.items():
    best = int(np.argmin(h["val"]))
    print(f"{name:<20} best val {min(h['val']):.3f} @ epoch {best:>3}"
          f"   final val {h['val'][-1]:.3f}")

plt.figure(figsize=(7, 4.5))
for name, h in over.items():
    line, = plt.plot(h["val"], label=f"{name} (val)")
    plt.plot(h["train"], "--", color=line.get_color(), alpha=0.5)
plt.xlabel("epoch"); plt.ylabel("loss"); plt.legend(fontsize=8)
plt.title("solid = val, dashed = train")
plt.tight_layout(); plt.savefig("overfitting.png", dpi=110)
```

**Expected output:**

```
no regularization    train 0.023  val 0.495  acc  93.3%
dropout 0.3          train 0.127  val 0.355  acc  93.6%
weight decay 0.3     train 0.047  val 0.269  acc  92.5%
no regularization    best val 0.199 @ epoch  85   final val 0.495
dropout 0.3          best val 0.199 @ epoch 177   final val 0.355
weight decay 0.3     best val 0.174 @ epoch 161   final val 0.269
```

Three things to notice, and they are worth more than the plot:

1. **No-regularization and dropout reach the same *best* validation loss (0.199); weight decay is a little better (0.174).** Regularization mostly did not improve the peak. It moved the peak later (epoch 85 vs 177 vs 161).
2. **They differ in the *final* loss** (0.495 vs 0.355 vs 0.269). Regularization slows down the *decay* after the peak, and here weight decay slows it most; dropout and weight decay are not tied.
3. **Early stopping at epoch 85 beats the final result of every regularizer.** 0.199 with no regularization at all is better than 0.355 with dropout and 0.269 with weight decay run to the end. Do the free thing first.

### Adding early stopping properly

```python
import copy

def run_with_early_stopping(patience=25, **kw):
    """Wrap run(): track the best val epoch and report what you would have kept."""
    h = run("early-stop probe", **kw)
    best_ep, best_val = int(np.argmin(h["val"])), float(min(h["val"]))
    # simulate the patience rule on the recorded history
    stop_ep = len(h["val"]) - 1
    for ep in range(len(h["val"])):
        if ep - int(np.argmin(h["val"][:ep + 1])) >= patience:
            stop_ep = ep
            break
    print(f"  would stop at epoch {stop_ep}, keeping weights from {best_ep} "
          f"(val {best_val:.3f}) instead of {h['val'][-1]:.3f}")
    return h

_ = run_with_early_stopping(patience=25, epochs=250)
```

Real output on the 120-example overfitting set:

```
  would stop at epoch 110, keeping weights from 85 (val 0.199) instead of 0.495
```

In a real training loop you save the state dict, not just the number. Here is the pattern as a complete, runnable helper:

```python
import copy

def early_stopping_state():
    return {"best_val": float("inf"), "best_state": None, "bad_epochs": 0}


def early_stopping_update(st, model, vloss, patience=25, min_delta=1e-4):
    """Call once per epoch. Returns True when you should stop."""
    if vloss < st["best_val"] - min_delta:
        st["best_val"], st["bad_epochs"] = vloss, 0
        # deepcopy, or the saved tensors alias the live model and keep changing
        st["best_state"] = copy.deepcopy(model.state_dict())
        return False
    st["bad_epochs"] += 1
    return st["bad_epochs"] >= patience


# usage inside your epoch loop:
#     if early_stopping_update(st, model, vloss, patience=25):
#         break
# and after the loop:
#     model.load_state_dict(st["best_state"])
```

⚠️ `copy.deepcopy` is not optional. `model.state_dict()` returns tensors that share storage with the live model, so without the copy your "saved best" silently changes as training continues.

---

## ✍️ Practice

### 1. [Warm-up] Find the learning-rate cliff

Using `run()` from the hands-on script, sweep AdamW over `lr ∈ {1e-5, 1e-4, 1e-3, 1e-2, 1e-1}` with everything else at its default. Record final train loss, final val loss, and val accuracy for each in a table.

**Done looks like:** a 5-row table plus one sentence naming the smallest LR that is clearly *too small* and the smallest LR that is clearly *too large*, with the loss value you used as evidence for each.

### 2. [Warm-up] Predict the curve shape

For each of these five descriptions, name which diagnostic shape (A–F from the table) you expect, *before* running anything. Then run each and check.

1. `run(lr=1e-6, epochs=60)`
2. `run(lr=0.5, epochs=60)`
3. `run(dropout=0.8, epochs=60)`
4. `run(epochs=400)` with the 120-example training set
5. `run(lr=3e-3, epochs=5)`

**Done looks like:** a table with columns `config | predicted shape | actual shape | was I right?` and one sentence for each miss explaining what you got wrong.

### 3. [Build] Test the linear scaling rule

Run this grid and fill in the table:

| batch | lr | final val loss |
|---|---|---|
| 32 | 1e-3 | ? |
| 64 | 1e-3 | ? |
| 64 | 2e-3 | ? |
| 128 | 1e-3 | ? |
| 128 | 4e-3 | ? |
| 256 | 1e-3 | ? |
| 256 | 8e-3 | ? |

**Done looks like:** the filled table, plus a written verdict on whether scaling the LR with the batch size recovered the batch-32 performance. Note that all runs use the same number of *epochs*, so bigger batches take fewer *steps* — mention whether that confounds your conclusion.

### 4. [Build] Instrument the gradient norm

The `run()` function already records `hist["gnorm"]` (the pre-clip gradient norm from the last step of each epoch). Plot it on a log y-axis for three configs: `lr=3e-3` (healthy), `lr=0.3` (too high), and a 12-block-deep model with `residual=False` versus `residual=True`. To get a deeper model, call `MLP(depth=12)` — you will need to add a `depth` argument to `run()`.

**Done looks like:** two plots (LR effect, depth+residual effect) and two sentences: what the gradient norm does when the LR is too high, and what the residual connection does to the gradient norm at depth 12.

### 5. [Stretch] Build an LR range test

Implement the **LR range test**: train for ~200 steps while multiplying the learning rate by a constant factor each step so it sweeps from 1e-7 up to 1.0 exponentially. Record the loss at each step and plot loss versus log(LR).

The plot has a characteristic shape: flat (LR too small to matter), then a steep descent (the useful zone), then an explosion. The rule of thumb is to pick the LR about one order of magnitude *below* the minimum of the curve.

**Done looks like:** the plot, the LR you would pick from it, and a comparison run at that LR against `lr=3e-3` showing which wins.

### 6. [Stretch] Break normalization on purpose

Design and run an experiment that makes **batch norm fail** where **layer norm succeeds**, using only the code in this module. Hint: batch norm's weakness is dependence on the other examples in the batch — think about batch size 2, or a validation set whose feature distribution differs from training.

**Done looks like:** a reproducible config where `norm="batch"` gives a clearly worse validation loss than `norm="layer"` (a gap of at least 2×), plus a paragraph explaining the mechanism, not just the number.

---

## 🤔 Think Deeper

### 1. Adam is the default almost everywhere, yet carefully tuned SGD+momentum still wins some vision benchmarks. If Adam is "smarter," why does the dumber method sometimes generalize better?

*How to reason about it:* Adam normalizes away gradient magnitude. That means it takes equally large steps for weights whose gradients are confidently large and weights whose gradients are tiny noise. Ask yourself: does the *size* of a gradient carry information that is worth keeping? Consider what kind of minimum each optimizer ends up in — a narrow spike where the loss is low but the surrounding region is bad, or a wide flat basin. Then ask which of those two survives a slightly different test distribution. There is no settled answer in the research literature, which is itself worth noticing.

### 2. Early stopping uses the validation set to decide when to stop. Does that count as training on the validation set? What is the honest way to report your final number?

*How to reason about it:* Count the decisions. If you try 40 configurations and pick the best validation score, how many "bits" of the validation set have you consumed? Think about what happens if you repeat this 500 times on a 300-example validation set — you will eventually find a config that looks great by luck alone. Then think about what a *third* split would buy you, and why Kaggle competitions have a private leaderboard that nobody can see until the end.

### 3. Suppose you tune a model to 99% accuracy on a medical dataset using dropout, weight decay, and 200 experiments guided by validation loss. A hospital wants to deploy it. What have your loss curves *not* told you, and what should you insist on measuring first?

*How to reason about it:* A loss curve is an average over the validation set. Averages hide subgroups. Ask: what is the accuracy on the smallest group in the data? What is the accuracy on cases that arrived from a different scanner, a different year, a different hospital? What is the cost of a false negative versus a false positive here, and is cross-entropy loss even the right thing to minimize when those costs differ by 100×? Consider that the most dangerous model is not one that is wrong, but one that is wrong *and confident*, and note that nothing in this module measured confidence calibration at all.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Forgetting `model.eval()` before validation | Dropout and batch norm change behaviour between modes, and the mode is invisible in the code that calls the model | Call `model.eval()` before every validation pass and `model.train()` at the top of every training epoch. Wrap validation in `with torch.no_grad():` too |
| Forgetting `optimizer.zero_grad()` | PyTorch *accumulates* gradients by design (useful for gradient accumulation across micro-batches) — so it feels like it should reset itself, and it doesn't | Call `opt.zero_grad(set_to_none=True)` immediately before `loss.backward()`, every step, no exceptions |
| Changing two knobs in one experiment | It feels efficient — "I'll just try the new LR *and* dropout together" | Change exactly one thing per run and log every setting. If two things change and it improves, you have learned nothing about which one helped |
| Comparing runs with different random seeds | Seeds are invisible, so run-to-run variation looks like a real effect | Fix `torch.manual_seed(seed)` for every run. For any close call, run 3 seeds and compare means. A 0.005 difference on one seed is noise |
| Normalizing with statistics computed over the whole dataset | `X = (X - X.mean()) / X.std()` before splitting is one clean-looking line | Compute `mu` and `sd` from the **training split only**, then apply them to val and test. Otherwise validation information leaks into training and your scores are fake |
| Using a very high learning rate and blaming the architecture | The failure looks like the model "can't learn this problem," which points suspicion at the model | Before touching the architecture, sweep the LR over 5 orders of magnitude and try to overfit 8 examples. Fix the optimization before you fix the model |
| Using `weight_decay` in `torch.optim.Adam` and expecting AdamW behaviour | The argument exists on both, with the same name, and does a different thing | Use `torch.optim.AdamW` when you want decoupled weight decay. `Adam(weight_decay=λ)` is L2-in-the-loss, which interacts badly with the adaptive scaling |
| Saving "best weights" without `deepcopy` | `state_dict()` returns tensors that share memory with the live model | `best_state = copy.deepcopy(model.state_dict())` |

---

## 🛠️ Mini-Project: Training Diagnostics Lab

**Time:** ~6 hours (including the writing, which is the point)

### Goal

Run six controlled experiments on **one fixed network and one fixed dataset**, each isolating exactly one knob. Plot all the curves on shared axes. Then distil what you learned into a one-page tuning playbook that another person could actually follow.

### Starter steps

1. **Freeze the baseline.** Copy `diagnostics_lab.py`. Write down every default in a comment block at the top: network width 64, depth 4, AdamW, lr 3e-3, batch 64, 60 epochs, no dropout, no weight decay, no norm, no residual, no schedule, seed 0. This is your control. Run it once and record its numbers.

2. **Run the six experiments.** Each one changes **one** argument from the baseline:

   | # | Knob | Values to try |
   |---|---|---|
   | 1 | `lr` | 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 |
   | 2 | `batch_size` | 8, 32, 128, 512 |
   | 3 | `dropout` | 0.0, 0.1, 0.3, 0.5 |
   | 4 | `weight_decay` | 0.0, 0.01, 0.1, 1.0 |
   | 5 | `norm` | "none", "batch", "layer" |
   | 6 | `schedule` | "none", "cosine", "cosine"+`warmup_frac=0.05`, "step" |

3. **Repeat every config on 3 seeds** (0, 1, 2) and report the mean and the spread. If the spread across seeds is bigger than the difference you are claiming, you have not found an effect.

4. **Plot.** One figure per knob, all values of that knob on shared axes, train as dashed lines and val as solid. Log-scale the y axis — loss differences that matter are multiplicative.

5. **Build a results table:**

   | Experiment | Value | Train loss (mean ± spread) | Val loss | Val acc | Curve shape |
   |---|---|---|---|---|---|

6. **Write the playbook.** One page, structured strictly as `SYMPTOM → CHECK → ACTION`. Every entry must come from something *you observed in your own runs*, with the numbers cited. For example:

   > **Symptom:** loss frozen at 0.693 from epoch 0.
   > **Check:** print `opt.param_groups[0]["lr"]` and the gradient norm.
   > **Action:** if grad norm is normal but nothing moves, the LR is too small — multiply by 10 until something happens. In my run, SGD at lr=0.03 gave loss 0.690 for 60 epochs; lr=0.3 gave 0.018.

### Success criteria checklist

- [ ] Exactly one variable changes per run — verified by diffing the kwargs
- [ ] Every run uses the same seed set (0, 1, 2) and the same data split
- [ ] Six figures, each with a caption stating what the reader should notice
- [ ] A results table with mean ± spread across seeds
- [ ] A one-page playbook with **at least six** `SYMPTOM → CHECK → ACTION` rules
- [ ] At least one rule where your data **contradicted** your prior expectation, and you say so
- [ ] Every claim in the playbook cites a number from your own table

### Level it up

Add a **seventh experiment on depth**: run `depth ∈ {2, 4, 8, 16, 32}` with `residual=False`, then the same sweep with `residual=True`. Plot final validation loss versus depth for both. You should see the plain network get *worse* past some depth while the residual network keeps improving or holds flat. Record the gradient norm of the **first** block in each case and show it collapsing in the plain deep network. That plot is the single most convincing piece of evidence for residual connections you can make yourself, and it is the direct bridge to Module 3, where every transformer block is residual.

---

## 🔑 Key Takeaways

- **The optimizer is three ideas stacked:** step downhill (SGD), remember your direction (momentum), and give every weight its own scale (RMSProp). Adam is momentum + RMSProp + a bias fix; AdamW just applies weight decay outside that machinery. Default to AdamW.
- **Adam's first step has size exactly `lr`.** That magnitude-independence is why its learning rate transfers across problems and SGD's does not.
- **The learning rate is a schedule, not a number.** Warm up over 2–5% of steps, then cosine decay to near zero. Free performance, two lines of code.
- **Regularization has a sweet spot, and early stopping is free.** In the module's own runs, no-regularization-plus-early-stopping (val 0.199) beat dropout-run-to-the-end (val 0.355) and weight-decay-run-to-the-end (val 0.269).
- **Batch norm looks at other examples; layer norm does not.** That single difference is why transformers use layer norm: sequences vary in length, and inference batches can be size 1.
- **Residual connections turn multiplication into addition on the backward pass.** `d(x + f(x))/dx = 1 + f'(x)` — the `1` is the gradient highway that makes 100-layer networks trainable.
- **Diagnose from the curve's shape, not its final number.** A loss stuck at `ln(2)` can mean "LR too small" or "LR too large" — two opposite fixes, one identical-looking result.

---

## 📓 Vocabulary

| Term | Plain definition | Example |
|---|---|---|
| **SGD** | Step every weight downhill by a fixed fraction of its gradient, using one small random batch at a time | `torch.optim.SGD(params, lr=0.1)` |
| **Momentum** | Keep a running average of past gradients so consistent directions accelerate and zig-zags cancel | `SGD(..., momentum=0.9)`; three `+2.0` gradients give velocity 2.0 → 3.8 → 5.42 |
| **RMSProp** | Divide each weight's step by the recent typical size of that weight's gradient | Lets a weight with 1e-5 gradients still move meaningfully |
| **Adam** | Momentum + RMSProp + bias correction; steps are roughly `lr`-sized regardless of gradient magnitude | First step from `w=1.0` with `lr=0.1` lands exactly on 0.9 |
| **AdamW** | Adam with weight decay applied straight to the weights instead of through the loss | `AdamW(params, lr=3e-4, weight_decay=0.01)` — the transformer default |
| **Learning-rate schedule** | A rule that changes the learning rate over the course of training | Cosine: `lr·0.5·(1+cos(π·t/T))`, from `lr` down to 0 |
| **Warmup** | Ramp the LR linearly from ~0 up to peak over the first few percent of steps | 5% warmup stops Adam from taking a huge step on a garbage variance estimate |
| **Effective learning rate** | How much weight change happens per training *example*, roughly `lr/batch_size` | Quadruple the batch → quadruple the LR to keep it constant |
| **Overfitting** | Getting better on seen data while getting worse on unseen data | Train loss 0.023, val loss climbing from 0.199 to 0.495 |
| **Early stopping** | Keep the weights from the best validation epoch and stop when it stops improving | Saved 0.296 of val loss for free in this module's run (0.199 instead of 0.495) |
| **Dropout** | Randomly zero a fraction of activations during training so no neuron is indispensable | `nn.Dropout(0.2)`; turned off automatically by `model.eval()` |
| **Weight decay** | Shrink every weight slightly towards zero each step | `weight_decay=0.01`; a "rent" that unhelpful weights cannot pay |
| **Data augmentation** | Create new training examples by label-preserving transformations | Flipping a cat photo; ⚠️ not flipping a letter "b" |
| **Batch norm** | Normalize each feature using statistics across the batch (down a column) | Standard in CNNs; needs batch size > 1 |
| **Layer norm** | Normalize each example using statistics across its own features (across a row) | Standard in transformers; batch-size-independent |
| **Residual connection** | Compute `x + f(x)` so the input flows past the block untouched | Makes the backward gradient `1 + f'(x)` — never vanishes to zero |
| **Gradient clipping** | Rescale the gradient vector down if its length exceeds a threshold, keeping direction | `clip_grad_norm_(params, 1.0)` — the LM default |
| **Vanishing gradient** | Gradients shrinking towards zero as they propagate back through many layers | 0.8 per layer × 30 layers ≈ 0.0012 of the original signal |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Find the learning-rate cliff

```python
for lr in [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]:
    run(f"adamw lr={lr}", lr=lr)
```

Real results (CPU, seed 0, 60 epochs, batch 64):

| lr | train loss | val loss | val acc | shape |
|---|---|---|---|---|
| 1e-5 | 0.683 | 0.679 | 55.3% | (C) nearly dead — barely moves off ln(2) |
| 1e-4 | 0.077 | 0.063 | 98.1% | (A) healthy — slower, but it gets there |
| 1e-3 | 0.018 | 0.026 | 99.4% | (A) healthy |
| 1e-2 | 0.013 | 0.059 | 99.2% | (A) healthy but noisier (val higher) |
| 1e-1 | 0.693 | 0.702 | 46.9% | (B) too high — never converges |

**Answer sentence:** `1e-5` is clearly too small — its loss stays at 0.683, almost `ln(2) = 0.693`, meaning almost no learning in 60 epochs (`1e-4` is *not* too small: it reaches 98.1%). `1e-1` is clearly too large — its loss is *also* near 0.693 but the curve is jagged rather than flat, and a run at `lr=0.3` is worse still (0.701). The usable band is roughly `1e-4` to `1e-2`, about two orders of magnitude wide, which is why "try powers of ten" is the standard first sweep.

The key discriminator between too-small and too-large is the *shape*: too-small is a smooth flat line or a slow smooth descent; too-large is spiky.

### 2. [Warm-up] Predict the curve shape

| config | predicted | actual | reasoning |
|---|---|---|---|
| `lr=1e-6` | (C) dead | (C) — flat at 0.693 (val 0.692, acc 53.1%) | Steps are ~1e-6 in size; 780 steps moves each weight by at most ~0.0008 total |
| `lr=0.5` | (B) LR too high | (B) — train 0.648, val 0.712, acc 46.9%: no better than chance on validation | Every step overshoots; the model random-walks |
| `dropout=0.8` | (E) underfitting | **Not (E)**: train 0.376, val 0.182, acc 93.6% — val is *below* train, shape (F) | Zeroing 80% of a 64-unit layer leaves ~13 active units during training, so train loss is inflated; at eval time all units are on. The model is handicapped, not broken — and the prediction "underfits" was wrong, which is the lesson |
| 400 epochs on 120 examples | (D) overfitting | (D) — val bottoms at 0.199 near epoch 85, then climbs to 0.525 by epoch 400 (train 0.009, acc 92.5%) | 120 examples, thousands of parameters: memorization is the easiest way to reduce loss |
| `lr=3e-3, epochs=5` | (E) underfitting | Mild (E): train 0.133, val 0.145, acc 95.0% | Nothing wrong with the setup, just few steps; already 95% — a budget limit, not a capacity limit. It is far better than most people predict |

**Important distinction to write down:** case 3 turned out *not* to be underfitting at all (val below train, shape F: dropout is on while the train loss is measured and off for validation). Case 5 is the genuine budget-limited case and needs *more time*. If a curve is still visibly descending at the end, train longer; if it is flat and high, suspect capacity or too much regularization. Do not trust a predicted shape over a measured one.

### 3. [Build] Test the linear scaling rule

```python
for bs, lr in [(32,1e-3),(64,1e-3),(64,2e-3),(128,1e-3),
               (128,4e-3),(256,1e-3),(256,8e-3)]:
    run(f"bs={bs} lr={lr}", batch_size=bs, lr=lr)
```

Representative results:

| batch | lr | final val loss | note |
|---|---|---|---|
| 32 | 1e-3 | 0.056 | reference (the worst of the 1e-3 runs) |
| 64 | 1e-3 | 0.026 | best of all |
| 64 | 2e-3 | 0.058 | doubling lr did not help |
| 128 | 1e-3 | 0.033 | fine without scaling |
| 128 | 4e-3 | 0.050 | scaling did not help |
| 256 | 1e-3 | 0.028 | fine without scaling |
| 256 | 8e-3 | 0.031 | fine |

**Verdict:** **this task does not reproduce the textbook pattern.** Large batches at an unscaled lr of 1e-3 are *not* worse than batch 32 (256 gives 0.028 vs 0.056), and scaling the lr did not systematically help. Differences of 0.02–0.03 in val loss between runs are within what one seed can do, so the honest conclusion is "no batch-size effect detectable here, at one seed". The linear scaling rule is a published finding about much larger problems with a "critical batch size" far above 256; it is *not* reproduced in this 840-example toy, and a toy this small cannot confirm or refute it.

**The confound, stated honestly:** all runs use 60 *epochs*, so batch 256 takes far fewer optimizer steps than batch 32 (3 × 60 = 180 versus 26 × 60 = 1560; 840 training examples). Fewer steps would be expected to hurt, and here it does not, which tells you this problem is easy enough that either number of steps suffices. A cleaner experiment fixes the number of *steps* instead of epochs:

```python
for bs in [32, 64, 128, 256]:
    epochs = int(60 * bs / 64)      # constant total step count
    run(f"bs={bs} fixed-steps", batch_size=bs, lr=1e-3 * bs / 64, epochs=epochs)
```

Real fixed-steps result: bs=32 val 0.041, bs=64 0.026, bs=128 0.070, bs=256 0.044. Again no monotone trend (bs=128 is the worst, bs=64 the best). Being able to spot a confound, fix it, and then report that the effect still did not show up is the actual skill being tested.

### 4. [Build] Instrument the gradient norm

First add `depth` to `run()`:

```python
def run(tag, *, depth=4, **kw):     # add depth to the signature
    ...
    model = MLP(depth=depth, norm=norm, dropout=dropout,
                residual=residual).to(DEVICE)
```

Then:

```python
h_ok   = run("lr ok",   lr=3e-3)
h_high = run("lr high", lr=0.3)

plt.figure(figsize=(7,4))
plt.plot(h_ok["gnorm"],   label="lr=3e-3")
plt.plot(h_high["gnorm"], label="lr=0.3")
plt.yscale("log"); plt.xlabel("epoch"); plt.ylabel("grad norm")
plt.legend(); plt.savefig("gnorm_lr.png", dpi=110)

h_plain = run("depth12 plain", depth=12, residual=False, epochs=40)
h_res   = run("depth12 res",   depth=12, residual=True,  epochs=40)
```

**What you should see and write:**

1. **LR too high:** the gradient norm is enormous at the start: 229 at the first epoch versus 0.168 for the healthy run (about 1,360x). Unlike the textbook story it then *does* come down (to 0.077 by the last epoch; the healthy run ends at 0.026), because with lr=0.3 the weights are flung to a region where the logits are huge and the loss surface is flat there; the model is stuck at 46.9% accuracy anyway. Lesson: **a gradient norm that is orders of magnitude larger than a healthy run's in the first epochs is the warning sign; a gradient norm that has fallen is not proof of health** — look at the loss and accuracy too.

2. **Residual at depth 12:** the plain 12-block model's gradient norm *is* smaller at the start (0.074 at the first epoch, versus 0.465 for the residual model), but it is **not** stuck: its gradient norm rises to 0.95, its train loss goes from 0.695 to 0.031, and it reaches 98.9% accuracy, the same as the residual model (train 0.772 to 0.010, 98.9%, gradient norm 0.465 to 0.032). **This did not reproduce the "plain deep net stalls" story**: at depth 12 and width 64 with AdamW (which rescales each weight's step, so a small gradient does not mean a small step), the plain network trains fine. The residual identity `d(x + f(x))/dx = 1 + f'(x)` still gives a healthier early gradient (0.465 vs 0.074), and the stalling the literature reports appears at much greater depth and with plain SGD; neither was run here. The first-block weight gradient norm of the residual model at the end of training is 0.0126.

To measure a specific block's gradient rather than the global norm:

```python
first_block_norm = model.blocks[0].fc.weight.grad.norm().item()
```

### 5. [Stretch] Build an LR range test

```python
import math

def lr_range_test(min_lr=1e-7, max_lr=1.0, steps=200, batch_size=64, seed=0):
    torch.manual_seed(seed)
    model = MLP().to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=min_lr)
    lossf = nn.CrossEntropyLoss()
    gamma = (max_lr / min_lr) ** (1 / steps)      # multiply lr by this each step
    lrs, losses, smooth = [], [], None
    g = torch.Generator(device="cpu").manual_seed(seed)

    for s in range(steps):
        idx = torch.randint(0, len(Xtr), (batch_size,), generator=g).to(DEVICE)
        loss = lossf(model(Xtr[idx]), ytr[idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        cur = min_lr * (gamma ** s)
        # exponential smoothing so the curve is readable
        smooth = loss.item() if smooth is None else 0.9 * smooth + 0.1 * loss.item()
        lrs.append(cur); losses.append(smooth)
        for pg in opt.param_groups:
            pg["lr"] = min_lr * (gamma ** (s + 1))
        if smooth > 4 * min(losses):              # diverged; stop early
            break

    plt.figure(figsize=(7, 4))
    plt.plot(lrs, losses)
    plt.xscale("log"); plt.xlabel("learning rate"); plt.ylabel("smoothed loss")
    plt.title("LR range test"); plt.tight_layout()
    plt.savefig("lr_range_test.png", dpi=110)
    best = lrs[int(np.argmin(losses))]
    print(f"loss minimum at lr={best:.2e}  ->  suggested lr={best/10:.2e}")
    return best / 10

suggested = lr_range_test()
run("suggested", lr=suggested)
run("default 3e-3", lr=3e-3)
```

**What you should see:** flat from 1e-7 to about 1e-5 (steps too small to matter), a steep descent from about 1e-4 to 1e-2, a minimum near 1e-2, then a sharp explosion. Real run: the minimum is at lr=1.29e-02, so the suggested lr is 1.29e-03. Training with it gives train 0.012, val 0.049, acc 98.9%; the default 3e-3 gives train 0.007, val 0.037, acc 98.9%. **The default wins slightly** (the suggested value is a safe choice, not the best one), and the hands-on default sits close to that range.

**Why divide by 10:** the loss minimum in the range test is the point at which the model is descending *fastest right now*, which is already close to the unstable edge. Training for thousands of steps at that value will blow up. One order of magnitude below is the standard safety margin.

### 6. [Stretch] Break normalization on purpose

Two configurations reliably do it.

**Approach A — tiny batches.** Batch norm estimates a mean and variance from the batch. At batch size 2, those estimates are almost pure noise, and the *running averages* it stores for eval time are correspondingly bad.

```python
run("bn bs=2", norm="batch", batch_size=2, epochs=30)
run("ln bs=2", norm="layer", batch_size=2, epochs=30)
```

**Approach B — train/eval distribution mismatch.** Shift the validation inputs. Batch norm's stored running statistics were computed on the training distribution and are now wrong; the question is whether layer norm is any better here — the data says it is not (see the table below).

```python
Xva_shift = Xva + 1.5        # every validation feature shifted by 1.5 sd

def eval_on(model, Xv, yv):
    model.eval()
    with torch.no_grad():
        logits = model(Xv)
        return (nn.CrossEntropyLoss()(logits, yv).item(),
                (logits.argmax(1) == yv).float().mean().item())
```

(Train each model normally, then evaluate on `Xva_shift`.)

**The mechanism, in words:** batch norm stores a single fixed `running_mean` and `running_var` per feature, learned during training, and subtracts them at eval time. If eval inputs are shifted, those subtractions are wrong for every example and the error propagates through the whole stack. Layer norm computes its statistics from the example currently in front of it, so it is invariant to a constant added to the *inputs of the layer norm*. But in this model the shift enters at the raw input, **before** the first linear layer, and the first linear layer mixes the shifted features with fixed weights *before* any norm sees them. So layer norm does **not** rescue the shifted data here (real results below). The prediction "layer norm adapts" was wrong for this architecture; it would hold only if the shift were applied directly to a layer norm's input.

This is not a contrived scenario. It is the mechanism behind "my model degraded after we changed the camera," "it worked on the dev set and failed in production," and — most relevantly for Module 3 — "batch statistics are meaningless when half the batch is padding tokens."

**Real results** (2x2, 60 epochs unless noted; validation shifted by +1.5):

| | matched val | shifted val |
|---|---|---|
| batch norm | loss 0.019, acc 99.4% | loss 4.480, acc 46.7% |
| layer norm | loss 0.064, acc 98.9% | loss 4.523, acc 48.3% |

Approach A at batch size 2, 30 epochs: batch norm train 0.688, val 0.677, acc 56.4% (fails); layer norm train 0.105, val 0.034, acc 98.6% (fine). So tiny batches *do* separate the two; the +1.5 shift breaks both equally.

**Report requirement:** show the numbers for both norms and both conditions in a 2×2 table, so the reader can see that batch norm is *fine* in the matched condition and only fails in the mismatched one. A regularizer that fails everywhere is a bug; a regularizer that fails under a specific, nameable condition is knowledge.

</details>

---

## 🧾 Patch log (offline redesign, 2026-10)

Ground truth: `36-week-course/_ledger/ledger-m01-04.md` (real CPU runs, torch 2.2.1, seed 0) plus three extra seeded CPU runs marked (*extra*) below.

- Hook "99.2% in twenty seconds" → "98.9% in a few seconds" → matches the real adamw lr=0.003 line.
- Batch-size table (8 / 64 / 512) → real values (*extra* run): batch 8 now best val 0.027, batch 64 0.007/0.037/98.9% → the old 0.075/0.045, 0.005/0.035 did not reproduce; added a one-seed caveat.
- Dropout-p table → 0.0/0.2/0.5 now 0.037/0.051/0.058 val (*extra* run) → the claim "dropout 0.2 halves val loss" was false on the full data; prose now says dropout helps only when overfitting (120-example run).
- Overfitting diagram and prose: best 0.216 @ 41, final 0.591 → best 0.199 @ 85, final 0.495; "saved 0.375" → "saved 0.296".
- batch vs layer norm quote 0.061 → 0.064 for layer norm (ledger 6B matched run).
- Setup: removed `pip install`; removed CUDA/MPS branch, `DEVICE = "cpu"`; "bigger GPU" → "bigger machine".
- Lab expected output: device mps → cpu; momentum, adamw, cosine, ln+res lines replaced with ledger values; `sgd lr=0.3` result 0.018 → 0.016 (*extra* run).
- Overfit experiment output and the three "notice" bullets rewritten (weight decay best 0.174; epochs 85/177/161; early stop beats final of all regularizers, still true); added early-stopping probe output (stops at 110, keeps epoch 85).
- Key takeaways and glossary numbers updated to match.
- Answer key 1: lr table replaced with real values; "1e-4 underfitting (~85%)" → healthy 98.1%; usable band 1e-4 to 1e-2; 1e-5 is "nearly dead" (55.3%).
- Answer key 2: `dropout=0.8` "underfits" → measured val 0.182 < train 0.376, 93.6% (not underfitting); 400-epoch run "climbs past 0.6" → best 0.199 @ 85, final 0.525; `lr=3e-3, epochs=5` "0.3-0.5" → 0.133/0.145/95.0%; closing paragraph rewritten.
- Answer key 3: scaling table replaced with measured values; "breaks at 256" → not reproduced; "195 steps" → 180; added fixed-steps results.
- Answer key 4: "LR too high gradient norm does not decay" → 229 → 0.077; "plain depth-12 stalls" → trains to 98.9%, did not reproduce; added numbers.
- Answer key 5: suggested lr 1.29e-3 vs default 3e-3 (default wins slightly).
- Answer key 6: "layer norm adapts to shift" → false for this architecture (LN shifted 48.3% vs BN 46.7%); added 2x2 and bs=2 results.

---

[⬅ Previous](../../CURRICULUM_MAP.md) · [Level 4 Home](README.md) · [Next ➡](module-02-sequence-models.md)
