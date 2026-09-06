# Module 4 — How Learning Actually Happens: Loss and Gradient Descent

**Level 3 · Module 4 · ~5.5 hours · Prereqs: Module 1 (splits, baselines, Pipeline), Module 2 (scaling, ColumnTransformer), Module 3 (probabilities, thresholds, log loss mentioned).**

[⬅ Previous](module-03-evaluation-metrics.md) · [Level 3 Home](README.md) · [Next ➡](module-05-neural-networks-from-scratch.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to explain the **sigmoid** function, convert a model's raw score into a probability by hand, and convert a probability back into a raw score.
2. You will be able to compute **log loss** for a small set of predictions with arithmetic you show, and explain in one sentence why squared error is the wrong loss for classification.
3. You will be able to state the gradient descent update rule `w ← w − lr × gradient` and apply it for three iterations on paper, showing every intermediate number.
4. You will be able to implement logistic regression trained by your own NumPy gradient descent and match scikit-learn's weights to three decimal places.
5. You will be able to diagnose a training run from its loss curve alone — too-small learning rate, too-large learning rate, converged, stuck — and name the fix for each.
6. You will be able to explain the difference between batch, mini-batch, and stochastic gradient descent in terms of weight updates per epoch.

---

## 🪝 The Hook

You have called `.fit()` maybe forty times in this level already. Every time, the same thing happened: a second of silence, and then an object came back that could predict.

Here is what actually happened in that second, for `LogisticRegression`:

The model started with every weight set to zero — meaning it predicted 50% for everything, like a coin. Then it computed **one number** that summarised how badly wrong all its predictions were. Then it asked a question with a surprisingly simple answer: *"If I nudge this weight up by a hair, does that one number get bigger or smaller?"* It nudged every weight in the direction that made the number smaller. Then it did that again. And again. A few hundred times, in under a second.

That is the entire secret. A number that measures wrongness, and a rule for stepping downhill. Every model in the rest of this level and all of Level 4 — neural networks, CNNs, the language models behind Claude — is trained by exactly this loop, at enormous scale. Today you build it yourself, in about forty lines of NumPy, and you check your answer against scikit-learn.

---

## 🧠 The Concept

### 1. From a weighted sum to a probability: the sigmoid

In Module 1 you built models but treated them as boxes. Let's open the smallest interesting box.

A **linear model** does exactly one arithmetic operation: it multiplies each feature by a weight, adds them up, and adds a constant.

> **Weight (`w`):** a number saying how much one feature pushes the answer up or down.
> **Bias (`b`):** a constant added to every prediction; it shifts the whole model up or down.
> **Logit / raw score (`z`):** the output of the weighted sum, before it is turned into a probability.

For two features:

```
z = w₁·x₁ + w₂·x₂ + b
```

🍕 **Analogy.** You are deciding whether a pizza order will be late. You have two facts: how many orders are already in the oven (`x₁`) and how far the house is in km (`x₂`). Experience says each pending order adds 0.6 to your worry, each km adds 0.4, and you start out at −3 worry because most orders are fine. That's `z = 0.6·x₁ + 0.4·x₂ − 3`. With 4 orders pending and 5 km to drive: `z = 2.4 + 2.0 − 3 = 1.4`.

But `z = 1.4` is not a probability. Probabilities live between 0 and 1, and `z` can be anything from −∞ to +∞. We need a squashing function.

> **Sigmoid (logistic function):** `σ(z) = 1 / (1 + e^(−z))`. It takes any real number and returns a number strictly between 0 and 1.

Three properties make it the right choice:

| Property | What it means |
|---|---|
| `σ(0) = 0.5` | A raw score of zero means "totally unsure" |
| `σ(z) → 1` as `z → +∞` | Big positive score means confidently class 1 |
| `σ(z) → 0` as `z → −∞` | Big negative score means confidently class 0 |
| It is smooth (differentiable) everywhere | We can compute slopes on it, which we will need |

Here is the S-curve, drawn in text:

```
 p
1.0 |                                    ...........•••••••
    |                              ....•••
0.8 |                          ..••
    |                       .••
0.6 |                    .••
0.5 |- - - - - - - - - -•- - - - - - - - - - - - - - - - -
0.4 |                .••
    |             ••.
0.2 |         ..••
    |  •••••••...
0.0 |•••.................................................
    +-----|-----|-----|-----|-----|-----|-----|-----|----
        -6    -4    -2     0     2     4     6     8   z
```

🔢 **Tiny concrete example.** Continuing the pizza: `z = 1.4`, so

```
e^(−1.4) = 0.246597
σ(1.4)   = 1 / (1 + 0.246597) = 1 / 1.246597 = 0.802184
```

**80.2% chance this order is late.** That number is now something you can threshold with everything you learned in Module 3.

**Going backwards.** Sometimes you have a probability and want the score. Invert the sigmoid:

```
z = ln( p / (1 − p) )
```

The quantity `p / (1 − p)` is the **odds**, and `ln(odds)` is the **log-odds** — which is exactly what `z` is. That's why `z` is called the logit. For `p = 0.9`: odds = 0.9/0.1 = 9, and `z = ln(9) = 2.197`.

⚠️ **A practical wrinkle.** Computing `e^(−z)` for `z = −1000` gives `e^1000`, which overflows to infinity in floating point. The fix is to branch: for `z ≥ 0` use `1/(1+e^(−z))`; for `z < 0` use `e^z/(1+e^z)`. Both are algebraically identical, but each avoids the exponential blowing up. You will write this in the Hands-On.

---

### 2. Loss functions: why squared error is wrong for classification

A **loss function** is one number that says how wrong the model currently is. Lower is better. Zero is perfect.

> **Loss function:** a formula that turns (true labels, predicted values) into a single non-negative number measuring wrongness.

Your instinct from any maths class is to use squared error: `(y − p)²`. Average it over all rows and you get mean squared error. It is simple and it is what regression uses. For classification it is a bad choice, for two separate reasons.

**Reason A: it barely punishes confident disasters.**

Say the truth is `y = 1` and the model says `p = 0.02`. That is a catastrophic prediction — the model is 98% sure of the wrong answer. Squared error says the damage is `(1 − 0.02)² = 0.9604`. Now say the model says `p = 0.4` — mildly wrong, still on the wrong side. Squared error says `(1 − 0.4)² = 0.36`. So the catastrophe is rated as only 2.7× worse than a near-miss. That is not how a fraud team, a hospital, or a spam filter experiences the difference.

**Reason B (the deep one): its gradients vanish exactly when you need them.**

We'll prove this properly in sub-concept 3, but the headline: when the model is confidently wrong, `σ` is flat there, and squaring makes the slope flat too. The model gets almost no signal telling it to fix itself. It just sits, confidently wrong, learning nothing.

The right loss is **log loss**, also called binary cross-entropy.

> **Log loss (binary cross-entropy):** for one row, `L = −[ y·ln(p) + (1 − y)·ln(1 − p) ]`. Average over all rows for the dataset loss.

Read it as an if-statement, because that is what it is:

- If `y = 1`, the second term dies and `L = −ln(p)`. The higher `p` is, the smaller the loss.
- If `y = 0`, the first term dies and `L = −ln(1 − p)`. The lower `p` is, the smaller the loss.

🍕 **Analogy.** Log loss is the "surprise" you feel. You said there was a 5% chance of rain and it poured. Your surprise is `−ln(0.05) = 3.00`. You said 90% chance of rain and it poured — surprise `−ln(0.90) = 0.105`. A weather forecaster's total surprise over the year is a fair way to score them, and it punishes confident wrongness brutally, which is precisely the behaviour we want.

🔢 **Tiny concrete example.** Same two predictions as before, `y = 1`:

| Prediction | Squared error | Log loss |
|---|---|---|
| `p = 0.40` (mildly wrong) | `0.360` | `−ln(0.40) = 0.916` |
| `p = 0.02` (confidently wrong) | `0.960` | `−ln(0.02) = 3.912` |
| Ratio, disaster vs near-miss | **2.7×** | **4.3×** |
| `p = 0.001` (catastrophic) | `0.998` | `−ln(0.001) = 6.908` |

Squared error tops out at 1.0 no matter how insane the prediction. Log loss goes to infinity. That unboundedness is a feature, not a bug: it means the model can *always* be made to care about a confidently-wrong row.

⚠️ **Numerical guard.** If the model ever outputs exactly `p = 0` when `y = 1`, `ln(0) = −∞` and your loss becomes `inf` or `nan`. Every real implementation clips probabilities into `[1e-12, 1 − 1e-12]` first. You will do the same.

---

### 3. Slope, derivative, and the gradient

To go downhill you need to know which way is downhill. That is what a derivative tells you.

> **Derivative:** the slope of a function at a point — how much the output changes when you nudge the input by a tiny amount. Written `dL/dw`, read "the derivative of L with respect to w."

🍕 **Analogy.** You are standing on a foggy hillside and you cannot see the valley. You can still feel the ground under your feet. Step your left foot 10 cm north: it goes down 3 cm. Step 10 cm east: it goes up 1 cm. So north-ish is downhill, east is uphill. The **gradient** is the arrow pointing in the steepest *uphill* direction. Its negative points steepest *downhill*. You do not need a map; you only need the ground right under you.

> **Gradient:** the collection of all the partial derivatives, one per weight, packed into a vector. It points in the direction of steepest **increase** of the loss.

🔢 **Feeling a derivative with numbers, no calculus needed.** Take `f(w) = w²`. What is the slope at `w = 3`?

```
f(3.001) = 9.006001
f(2.999) = 8.994001
slope ≈ (9.006001 − 8.994001) / (3.001 − 2.999)
       = 0.012 / 0.002
       = 6.0
```

And the calculus rule says the derivative of `w²` is `2w = 6`. They agree. That "nudge it and divide" trick is called a **numerical gradient**, and it is how you will check your work in Module 5. It's slow but it never lies.

**The gradient of log loss for logistic regression.** Here is the punchline, and it is unreasonably clean. For a dataset of `n` rows, with `p_i = σ(w·x_i + b)`:

```
∂L/∂w_j = (1/n) · Σ_i (p_i − y_i) · x_ij

∂L/∂b   = (1/n) · Σ_i (p_i − y_i)
```

That's it. **Error times feature, averaged.** No sigmoid derivative left over, no messy fractions. The ugly `σ'(z) = σ(z)(1 − σ(z))` term that appears midway through the derivation cancels exactly against a term from the log. This cancellation is *the* reason log loss is paired with sigmoid — they are built for each other.

<details>
<summary>Optional: the two-line derivation (chain rule)</summary>

For one row with `z = w·x + b`, `p = σ(z)`, `L = −[y ln p + (1−y) ln(1−p)]`:

```
dL/dp = −y/p + (1−y)/(1−p) = (p − y) / (p(1 − p))
dp/dz = σ(z)(1 − σ(z)) = p(1 − p)

dL/dz = dL/dp · dp/dz = (p − y)/(p(1−p)) · p(1−p) = p − y      ← the cancellation
dz/dw_j = x_j

dL/dw_j = (p − y) · x_j
```
The `p(1 − p)` cancels. Average over rows and you have the formula above. You will use this exact chain-rule move again in Module 5, on more layers.

</details>

🔢 **What the formula means, in words.** If the model predicted `p = 0.9` and the truth was `y = 1`, then `p − y = −0.1` — small error, small push. If it predicted `p = 0.9` and the truth was `y = 0`, then `p − y = +0.9` — huge error, huge push. And that push gets multiplied by the feature value, so features that were large on that row get corrected the most. It is a blame-assignment rule, and it is intuitive.

---

### 4. The update rule

Once you have the gradient, the algorithm is one line.

> **Gradient descent update rule:** `w ← w − lr · ∂L/∂w`, for every weight, repeated until the loss stops improving.

> **Learning rate (`lr`):** how big a step to take. A small positive number, typically between 0.0001 and 1.

The minus sign is the whole idea: the gradient points uphill, so you step the *opposite* way.

🍕 **Analogy.** Foggy hillside again. The gradient tells you which way is up. You turn 180° and take a step. The learning rate is your stride length. Take baby steps and you'll be out there all night. Take giant leaps and you'll bound straight across the valley and up the far slope.

🔢 **One update, fully numeric.** Suppose `w = 0.5` and the gradient at that point is `∂L/∂w = 0.265122`, with `lr = 1.0`:

```
w_new = 0.5 − 1.0 × 0.265122 = 0.234878
```

The gradient was positive (increasing `w` would increase the loss), so we decreased `w`. Correct.

Here's the loop as a diagram:

```
   ┌──────────────────────────────────────────────────────┐
   │                                                      │
   ▼                                                      │
┌─────────────┐   ┌──────────┐   ┌───────────┐   ┌────────┴────────┐
│ z = Xw + b  │──▶│ p = σ(z) │──▶│ loss(p,y) │──▶│  gradient       │
│ forward     │   │          │   │           │   │  (1/n)Xᵀ(p − y) │
└─────────────┘   └──────────┘   └───────────┘   └────────┬────────┘
                                                          │
                                              ┌───────────▼───────────┐
                                              │ w ← w − lr·grad_w     │
                                              │ b ← b − lr·grad_b     │
                                              └───────────────────────┘
```

Loop that a few hundred times and the box marked `fit()` is no longer a box.

---

### 5. Learning rate: too small, too large, divergence

The learning rate is the single most consequential number you choose. Here is what each regime looks like on a loss curve.

```
 TOO SMALL (lr=0.005)      JUST RIGHT (lr=0.5)      TOO LARGE (lr=800)
 loss                       loss                     loss
 0.7|••                     0.7|•                    18 |    •
    |  •••                     |  •                     |   • •
 0.5|     ••••                 | •                    9 |  •   •  •
    |         ••••          0.4| •                      | •     ••  •
 0.3|             ••••         |  ••                  0 |•         ••••
    +-------------------       +•••••••••••••          +-----------------
    0            500 ep        0          500 ep       0        500 ep
 still falling at the end   flat and low by ep 100  chaos; may end worse
```

**Real numbers from the dataset you'll use in the Hands-On** (400 rows, 2 standardised features, 500 full-batch epochs):

| Learning rate | Loss at epoch 0 | Epoch 100 | Epoch 500 | Worst loss seen | Monotone? | Test accuracy |
|---|---|---|---|---|---|---|
| 0.005 | 0.6931 | 0.5748 | 0.3774 | 0.6931 | yes | 0.9300 |
| 0.5 | 0.6931 | 0.2189 | 0.2157 | 0.6931 | yes | 0.9500 |
| 800 | 0.6931 | 10.6483 | 2.9062 | **17.9656** | **no** | 0.7800 |

Read the table like a doctor reads a chart:

- **lr = 0.005** — nothing is broken, it's just slow. The loss is still falling at epoch 500; it never got to the bottom. Fix: increase lr, or run more epochs.
- **lr = 0.5** — the loss flattened by epoch ~100 and stayed. This is convergence. Extra epochs cost time and buy nothing.
- **lr = 800** — the loss shot from 0.69 to nearly 18. The steps are so large the model leaps over the valley to a worse spot each time, then leaps back. Accuracy fell 17 points. Fix: divide lr by 10 until the curve behaves.

> **Divergence:** when the loss increases instead of decreasing, because the steps are too big. Cure: smaller learning rate.

**The diagnostic rule you should memorise:** *for full-batch gradient descent on a convex loss, with a good learning rate the loss decreases every single epoch.* Not "mostly". Every epoch. If your loss curve wiggles upward on full-batch training, your learning rate is too big — full stop. (Mini-batch and stochastic curves *do* wiggle, for a different and harmless reason; see the next sub-concept.)

**Feature scaling matters enormously here.** If one feature ranges 0–1 and another ranges 0–100000, the loss surface is a long thin canyon. Any learning rate small enough to be stable in the steep direction is hopelessly slow in the shallow direction. This is why Module 2's `StandardScaler` is not cosmetic — it is what makes gradient descent tractable. On unscaled data, `lr = 1.0` on this same problem sends the loss from 0.693 to 1.658 in fifty epochs and then it gets *stuck there forever*, because the sigmoid has saturated and the gradients are effectively zero.

---

### 6. Batch, mini-batch, and stochastic gradient descent

So far, every gradient used all `n` rows. That's one flavour.

> **Batch (full-batch) gradient descent:** compute the gradient using every training row, then take one step. One step per epoch.
>
> **Stochastic gradient descent (SGD):** compute the gradient from one row, step, move to the next row. `n` steps per epoch.
>
> **Mini-batch gradient descent:** compute the gradient from a small chunk (32, 64, 256 rows), step, next chunk. `n/batch_size` steps per epoch.

> **Epoch:** one complete pass over the training data. **Step (or iteration):** one weight update.

🍕 **Analogy.** You're adjusting a huge pot of curry. Full-batch is: taste a spoonful blended from the whole pot, then add salt once. Perfectly informed, but slow — you have to blend the whole pot every time. SGD is: taste one grain of rice, add a pinch of salt, taste the next grain. Fast and noisy; one weird grain sends you the wrong way, but over hundreds of grains it averages out. Mini-batch is: taste a small bowl. Almost as informed as the whole pot, almost as fast as one grain. Everyone uses mini-batch.

🔢 **Real numbers, same dataset, 100 epochs each, `lr = 0.5`:**

| Method | Weight updates in 100 epochs | Final train loss | Test accuracy |
|---|---|---|---|
| Full batch | 100 | 0.2189 | 0.9400 |
| Mini-batch (32) | 1,000 | 0.2157 | 0.9500 |
| Stochastic (1) | 30,000 | 0.2195 | 0.9500 |

Mini-batch got further in the same number of epochs because it took ten times as many steps. That's the whole appeal. Stochastic took 300× the steps and landed in the same place — the extra steps were noisy and partly cancelled out, and each one cost a Python loop iteration, so it was much slower in wall-clock time.

**Why the noise is sometimes good.** A mini-batch gradient is a noisy estimate of the true gradient. In Module 5 and beyond, where the loss surface has many local dips instead of one clean valley, that noise helps the model rattle out of shallow bad dips. For logistic regression the loss is **convex** — one bowl, one bottom — so the noise buys you nothing but speed.

> **Convex loss:** a bowl shape with exactly one lowest point. Log loss for logistic regression is convex, so gradient descent with a sane learning rate always finds *the* answer, not *an* answer. Neural network losses (Module 5) are not convex.

**When do you stop?** Three standard **convergence criteria**:

| Criterion | Rule | When to use it |
|---|---|---|
| Fixed epochs | Run exactly 1,000 epochs | Simple, predictable; wastes time or stops early |
| Loss change | Stop when `|loss_t − loss_{t−1}| < 1e-6` | Good default for full-batch |
| Gradient norm | Stop when `‖gradient‖ < 1e-5` | Most principled — at the bottom, the slope is zero |
| Validation stall | Stop when validation loss stops improving | The one that matters for real models (Module 6) |

---

## 🔍 Worked Example

Let's train a logistic regression **entirely by hand** for three iterations. Every number below is arithmetic you can check on a calculator.

### The setup

Four students. One feature: hours of past-paper practice, `x`. One label: did they pass, `y`.

| Student | `x` (hours) | `y` (passed) |
|---|---|---|
| A | 1 | 0 |
| B | 2 | 0 |
| C | 3 | 1 |
| D | 4 | 1 |

Model: `z = w·x + b`, `p = σ(z)`. Start at `w = 0`, `b = 0`. Learning rate `lr = 1.0`. Full batch (all four rows per step).

Gradient formulas we derived:

```
∂L/∂w = (1/4) · Σ (p_i − y_i)·x_i
∂L/∂b = (1/4) · Σ (p_i − y_i)
```

---

### Iteration 0 → 1

**Forward pass.** `w = 0, b = 0`, so `z = 0` for everyone, so `p = σ(0) = 0.5` for everyone.

**Loss.**
```
Student A (y=0): −ln(1 − 0.5) = −ln(0.5) = 0.693147
Student B (y=0): −ln(0.5)              = 0.693147
Student C (y=1): −ln(0.5)              = 0.693147
Student D (y=1): −ln(0.5)              = 0.693147
Mean loss = (0.693147 × 4) / 4 = 0.693147
```
Sanity check: 0.693147 is `ln 2`. A model that says 50% to everything always has log loss `ln 2`. That is the "I know nothing" baseline. Memorise it — if your training loss sits at 0.693 forever, your model is learning nothing at all.

**Errors `p − y`.**
```
A: 0.5 − 0 = +0.5
B: 0.5 − 0 = +0.5
C: 0.5 − 1 = −0.5
D: 0.5 − 1 = −0.5
```

**Gradients.**
```
∂L/∂w = (1/4)[ (0.5)(1) + (0.5)(2) + (−0.5)(3) + (−0.5)(4) ]
      = (1/4)[ 0.5 + 1.0 − 1.5 − 2.0 ]
      = (1/4)(−2.0)
      = −0.500000

∂L/∂b = (1/4)[ 0.5 + 0.5 − 0.5 − 0.5 ] = (1/4)(0) = 0.000000
```

**Update.**
```
w ← 0 − 1.0 × (−0.500000) = +0.500000
b ← 0 − 1.0 × ( 0.000000) =  0.000000
```

Notice: the bias gradient was exactly zero because the classes are perfectly balanced (2 and 2) and every prediction was 0.5. The bias only moves when the average prediction is off from the average label.

---

### Iteration 1 → 2

**Forward pass.** `w = 0.5, b = 0`.

| Student | `x` | `z = 0.5x` | `p = σ(z)` | `y` |
|---|---|---|---|---|
| A | 1 | 0.5 | 0.622459 | 0 |
| B | 2 | 1.0 | 0.731059 | 0 |
| C | 3 | 1.5 | 0.817574 | 1 |
| D | 4 | 2.0 | 0.880797 | 1 |

**Loss.**
```
A: −ln(1 − 0.622459) = −ln(0.377541) = 0.974077
B: −ln(1 − 0.731059) = −ln(0.268941) = 1.313262
C: −ln(0.817574)                     = 0.201413
D: −ln(0.880797)                     = 0.126928
Sum = 2.615680;  Mean loss = 0.653920
```
Down from 0.693147. ✅

Look at student B: the model now says 73% pass, and B failed. That single row contributes 1.313 — more than half the total loss. Log loss is telling you exactly where to look.

**Errors `p − y`.**
```
A: +0.622459
B: +0.731059
C: −0.182426
D: −0.119203
```

**Gradients.**
```
∂L/∂w = (1/4)[ (0.622459)(1) + (0.731059)(2) + (−0.182426)(3) + (−0.119203)(4) ]
      = (1/4)[ 0.622459 + 1.462118 − 0.547278 − 0.476812 ]
      = (1/4)(1.060487)
      = 0.265122

∂L/∂b = (1/4)[ 0.622459 + 0.731059 − 0.182426 − 0.119203 ]
      = (1/4)(1.051889)
      = 0.262972
```

**Update.**
```
w ← 0.500000 − 1.0 × 0.265122 = 0.234878
b ← 0.000000 − 1.0 × 0.262972 = −0.262972
```

Interesting: `w` went *down*. Iteration 1 overshot — a stride of 1.0 pushed `w` past where it wanted to be, and now the model is correcting. That's a mild overshoot, not divergence: the loss is still falling.

---

### Iteration 2 → 3

**Forward pass.** `w = 0.234878, b = −0.262972`.

| Student | `x` | `z = 0.234878x − 0.262972` | `p = σ(z)` | `y` |
|---|---|---|---|---|
| A | 1 | −0.028094 | 0.492977 | 0 |
| B | 2 | 0.206784 | 0.551512 | 0 |
| C | 3 | 0.441662 | 0.608655 | 1 |
| D | 4 | 0.676540 | 0.662966 | 1 |

**Loss.**
```
A: −ln(1 − 0.492977) = −ln(0.507023) = 0.679172
B: −ln(1 − 0.551512) = −ln(0.448488) = 0.801811
C: −ln(0.608655)                     = 0.496541
D: −ln(0.662966)                     = 0.411005
Sum = 2.388529;  Mean loss = 0.597152
```
Down again: 0.693147 → 0.653920 → 0.597152. ✅

**Errors `p − y`.**
```
A: +0.492977
B: +0.551512
C: −0.391345
D: −0.337034
```

**Gradients.**
```
∂L/∂w = (1/4)[ 0.492977 + 1.103024 − 1.174035 − 1.348136 ]
      = (1/4)(−0.926170)
      = −0.231543

∂L/∂b = (1/4)[ 0.492977 + 0.551512 − 0.391345 − 0.337034 ]
      = (1/4)(0.316110)
      = 0.079028
```

**Update.**
```
w ← 0.234878 − 1.0 × (−0.231543) = 0.466420
b ← (−0.262972) − 1.0 × (0.079028) = −0.342000
```

---

### Where we are after three iterations

| Iteration | `w` | `b` | Loss |
|---|---|---|---|
| 0 (start) | 0.000000 | 0.000000 | 0.693147 |
| 1 | 0.500000 | 0.000000 | 0.653920 |
| 2 | 0.234878 | −0.262972 | 0.597152 |
| 3 | 0.466420 | −0.342000 | 0.571048 |

The loss dropped every step. The weight is oscillating a little (0.5 → 0.23 → 0.47) because `lr = 1.0` is on the large side for this problem — but it is oscillating *downhill*, which is fine. Run this loop 2,000 more times and it lands near `w ≈ 2.0, b ≈ −5.0`, at which point the model says student A has a 4% chance and student D has a 95% chance. Which is exactly what the data says.

**What you just did is what `fit()` does.** The only differences at scale are: more features, more rows, and someone else's C code doing the arithmetic.

---

## 💻 Hands-On

Everything below runs on Python 3.11+ with `numpy`, `scikit-learn`, and `matplotlib`.

```bash
pip install numpy scikit-learn matplotlib
```

---

### Step 1 — A numerically safe sigmoid

Create `sigmoid_demo.py`:

```python
import numpy as np


def sigmoid(z):
    """Numerically stable logistic function. Works on scalars and arrays."""
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    # For z >= 0 : 1 / (1 + e^-z)   -> e^-z is at most 1, never overflows.
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    # For z <  0 : e^z / (1 + e^z)  -> e^z is at most 1, never overflows.
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


print("z        sigmoid(z)")
for z in [-6, -3, -1, -0.5, 0, 0.5, 1, 3, 6]:
    print(f"{z:>5}    {float(sigmoid(z)):.6f}")

print()
print(f"sigmoid(1000)  = {float(sigmoid(1000)):.6f}")
print(f"sigmoid(-1000) = {float(sigmoid(-1000)):.6f}")
```

Expected output:

```
z        sigmoid(z)
   -6    0.002473
   -3    0.047426
   -1    0.268941
 -0.5    0.377541
    0    0.500000
  0.5    0.622459
    1    0.731059
    3    0.952574
    6    0.997527

sigmoid(1000)  = 1.000000
sigmoid(-1000) = 0.000000
```

Try replacing the function body with the naive `1/(1+np.exp(-z))` and passing `-1000`. You get a `RuntimeWarning: overflow encountered in exp`. The branching version never does.

---

### Step 2 — Log loss with the arithmetic exposed

Create `logloss_demo.py`:

```python
import numpy as np
from sklearn.metrics import log_loss


def log_loss_manual(y, p, eps=1e-12):
    """Per-row loss and the mean. Clipping stops ln(0) = -inf."""
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    per_row = -(y * np.log(p) + (1 - y) * np.log(1 - p))
    return per_row, per_row.mean()


y = np.array([1, 1, 0, 0, 1])
p = np.array([0.90, 0.60, 0.20, 0.70, 0.05])

per_row, mean = log_loss_manual(y, p)
print(" y     p      loss")
for yi, pi, li in zip(y, p, per_row):
    print(f" {yi}   {pi:.2f}   {li:.6f}")

print(f"\nmean log loss      = {mean:.6f}")
print(f"sklearn log_loss   = {log_loss(y, p):.6f}")
print(f"mean squared error = {np.mean((y - p) ** 2):.6f}")
```

Expected output:

```
 y     p      loss
 1   0.90   0.105361
 1   0.60   0.510826
 0   0.20   0.223144
 0   0.70   1.203973
 1   0.05   2.995732

mean log loss      = 1.007807
sklearn log_loss   = 1.007807
mean squared error = 0.320500
```

Look at row 5: `y = 1` but the model said 5%. It contributes **2.995732** — nearly three times the next worst row, and 60% of the whole loss on its own. Under squared error, that same row contributes `(1 − 0.05)² = 0.9025` out of 1.6025 total, so it is only 56% — and it would be capped at 1.0 no matter how wrong the model got. That difference in *how loudly the loss screams* is what drives the gradient.

---

### Step 3 — Reproduce the hand-worked three iterations

Create `three_steps.py`:

```python
import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))     # safe here: |z| stays small


x = np.array([1.0, 2.0, 3.0, 4.0])   # hours of practice
y = np.array([0.0, 0.0, 1.0, 1.0])   # passed?

w, b, lr = 0.0, 0.0, 1.0

for it in range(4):
    p = sigmoid(w * x + b)
    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    grad_w = np.mean((p - y) * x)
    grad_b = np.mean(p - y)
    print(f"iter {it}:  w={w:>9.6f}  b={b:>9.6f}  loss={loss:.6f}  "
          f"gw={grad_w:>9.6f}  gb={grad_b:>9.6f}")
    print(f"          p = {np.round(p, 6)}")
    w -= lr * grad_w
    b -= lr * grad_b

print(f"\nafter 3 updates: w={w:.6f}  b={b:.6f}")
```

Expected output:

```
iter 0:  w= 0.000000  b= 0.000000  loss=0.693147  gw=-0.500000  gb= 0.000000
          p = [0.5 0.5 0.5 0.5]
iter 1:  w= 0.500000  b= 0.000000  loss=0.653920  gw= 0.265122  gb= 0.262972
          p = [0.622459 0.731059 0.817574 0.880797]
iter 2:  w= 0.234878  b=-0.262972  loss=0.597152  gw=-0.231543  gb= 0.079028
          p = [0.492977 0.551512 0.608655 0.662966]
iter 3:  w= 0.466420  b=-0.342000  loss=0.571048  gw= 0.082251  gb= 0.184468
          p = [0.531065 0.643558 0.742167 0.82108 ]

after 3 updates: w=0.384170  b=-0.526467
```

Every number matches the Worked Example. Your hand arithmetic and the machine agree — that is the whole point of this step. If they had not matched, one of you would be wrong, and you'd know to go find out which.

---

### Step 4 — A real gradient-descent logistic regression class

Create `gd_logreg.py`. This is the file your mini-project builds on.

```python
"""Logistic regression trained by hand-written gradient descent."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def log_loss_mean(y, p, eps=1e-12):
    p = np.clip(p, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class MyLogisticRegression:
    """batch_size=None -> full batch; 1 -> stochastic; 32 -> mini-batch."""

    def __init__(self, lr=0.5, n_epochs=300, batch_size=None, tol=1e-7, seed=0):
        self.lr = lr
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.tol = tol
        self.seed = seed

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n, d = X.shape

        self.w_ = np.zeros(d)          # start at "I know nothing"
        self.b_ = 0.0
        self.loss_history_ = []
        self.w_history_ = []

        rng = np.random.default_rng(self.seed)
        bs = n if self.batch_size is None else self.batch_size
        prev = None

        for epoch in range(self.n_epochs):
            loss = log_loss_mean(y, sigmoid(X @ self.w_ + self.b_))
            self.loss_history_.append(loss)
            self.w_history_.append((self.w_.copy(), self.b_))

            if prev is not None and abs(prev - loss) < self.tol:
                self.n_epochs_run_ = epoch
                break
            prev = loss

            order = rng.permutation(n) if bs < n else np.arange(n)
            for start in range(0, n, bs):
                idx = order[start:start + bs]
                Xb, yb = X[idx], y[idx]
                p = sigmoid(Xb @ self.w_ + self.b_)
                err = p - yb                          # the (p - y) term
                grad_w = (Xb.T @ err) / len(idx)      # error x feature, averaged
                grad_b = float(err.mean())
                self.w_ -= self.lr * grad_w           # THE update rule
                self.b_ -= self.lr * grad_b
        else:
            self.n_epochs_run_ = self.n_epochs

        # record the state after the final update too
        self.loss_history_.append(log_loss_mean(y, sigmoid(X @ self.w_ + self.b_)))
        self.w_history_.append((self.w_.copy(), self.b_))
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, dtype=float) @ self.w_ + self.b_)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

    def score(self, X, y):
        return float((self.predict(X) == np.asarray(y)).mean())


if __name__ == "__main__":
    X, y = make_classification(n_samples=400, n_features=2, n_redundant=0,
                               n_informative=2, n_clusters_per_class=1,
                               class_sep=1.0, flip_y=0.05, random_state=7)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=7)
    scaler = StandardScaler().fit(Xtr)          # fit on TRAIN only (Module 2!)
    Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)

    print("=== three learning rates, 500 full-batch epochs ===")
    print(f"{'lr':>8} {'start':>8} {'ep100':>9} {'final':>9} "
          f"{'worst':>9} {'monotone':>9} {'test acc':>9}")
    for lr in (0.005, 0.5, 800.0):
        m = MyLogisticRegression(lr=lr, n_epochs=500, tol=0.0).fit(Xtr_s, ytr)
        h = np.array(m.loss_history_)
        mono = bool(np.all(np.diff(h) <= 1e-12))
        print(f"{lr:>8} {h[0]:>8.4f} {h[100]:>9.4f} {h[-1]:>9.4f} "
              f"{h.max():>9.4f} {str(mono):>9} {m.score(Xte_s, yte):>9.4f}")

    print("\n=== my model (lr=0.5, 5000 epochs) vs sklearn ===")
    mine = MyLogisticRegression(lr=0.5, n_epochs=5000, tol=0.0).fit(Xtr_s, ytr)
    sk = LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000).fit(Xtr_s, ytr)
    print("mine    w =", np.round(mine.w_, 4), " b =", round(mine.b_, 4),
          " test acc =", round(mine.score(Xte_s, yte), 4))
    print("sklearn w =", np.round(sk.coef_[0], 4), " b =", round(float(sk.intercept_[0]), 4),
          " test acc =", round(float(sk.score(Xte_s, yte)), 4))
    print("max |weight difference| =",
          round(float(np.max(np.abs(mine.w_ - sk.coef_[0]))), 4))
    print("accuracy gap (points)   =",
          round(abs(mine.score(Xte_s, yte) - sk.score(Xte_s, yte)) * 100, 2))

    print("\n=== batch vs mini-batch vs stochastic (100 epochs, lr=0.5) ===")
    for name, bs in [("full batch", None), ("mini-batch 32", 32), ("stochastic (1)", 1)]:
        m = MyLogisticRegression(lr=0.5, n_epochs=100, batch_size=bs,
                                 tol=0.0, seed=1).fit(Xtr_s, ytr)
        updates = 100 * (1 if bs is None else int(np.ceil(len(Xtr_s) / bs)))
        print(f"{name:>15}: final train loss {m.loss_history_[-1]:.4f}  "
              f"test acc {m.score(Xte_s, yte):.4f}  weight updates {updates}")
```

Expected output:

```
=== three learning rates, 500 full-batch epochs ===
      lr    start     ep100     final     worst  monotone  test acc
   0.005   0.6931    0.5748    0.3774    0.6931      True    0.9300
     0.5   0.6931    0.2189    0.2157    0.6931      True    0.9500
   800.0   0.6931   10.6483    2.9062   17.9656     False    0.7800

=== my model (lr=0.5, 5000 epochs) vs sklearn ===
mine    w = [ 1.093  -2.9487]  b = 0.8309  test acc = 0.95
sklearn w = [ 1.0963 -2.9479]  b = 0.8331  test acc = 0.95
max |weight difference| = 0.0033
accuracy gap (points)   = 0.0

=== batch vs mini-batch vs stochastic (100 epochs, lr=0.5) ===
     full batch: final train loss 0.2189  test acc 0.9400  weight updates 100
  mini-batch 32: final train loss 0.2157  test acc 0.9500  weight updates 1000
 stochastic (1): final train loss 0.2195  test acc 0.9500  weight updates 30000
```

**Read that middle block again.** Your forty lines of NumPy found `w = [1.0930, −2.9487]`. scikit-learn's professionally-tuned L-BFGS optimiser found `w = [1.0963, −2.9479]`. They agree to three decimal places, and both score 95% on the test set. This is not luck — the loss is convex, so there is exactly one right answer and any correct method must find it.

> ⚠️ **A note on `penalty=None`.** By default, `LogisticRegression` applies L2 **regularisation** (`penalty="l2", C=1.0`) — deliberately handicapping the model by adding a penalty for large weights, so it cannot overfit by leaning hard on one feature — which shrinks weights toward zero and would *not* match your unregularised implementation. You must pass `penalty=None` for a fair comparison. On scikit-learn ≤ 1.1 the spelling was `penalty="none"` (a string); from 1.2 onward use the Python `None`. Practice exercise 5 has you add the regularisation term to your own code.

---

### Step 5 — Plot the loss curves and the moving decision boundary

Create `plot_descent.py`:

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from gd_logreg import MyLogisticRegression

X, y = make_classification(n_samples=400, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1,
                           class_sep=1.0, flip_y=0.05, random_state=7)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                      stratify=y, random_state=7)
scaler = StandardScaler().fit(Xtr)
Xtr_s = scaler.transform(Xtr)

fig, (ax_loss, ax_bnd) = plt.subplots(1, 2, figsize=(13, 5))

# --- left panel: three loss curves on a log y-axis -------------------------
for lr, colour in [(0.005, "tab:blue"), (0.5, "tab:green"), (800.0, "tab:red")]:
    m = MyLogisticRegression(lr=lr, n_epochs=500, tol=0.0).fit(Xtr_s, ytr)
    ax_loss.plot(m.loss_history_, color=colour, label=f"lr = {lr}")
ax_loss.axhline(np.log(2), ls="--", c="grey", lw=1, label="ln 2 = know-nothing")
ax_loss.set_yscale("log")
ax_loss.set_xlabel("epoch")
ax_loss.set_ylabel("training log loss (log scale)")
ax_loss.set_title("Learning rate decides everything")
ax_loss.legend()

# --- right panel: the boundary moving during training ----------------------
good = MyLogisticRegression(lr=0.5, n_epochs=500, tol=0.0).fit(Xtr_s, ytr)
ax_bnd.scatter(Xtr_s[ytr == 0, 0], Xtr_s[ytr == 0, 1], s=14, c="tab:orange",
               label="class 0", alpha=0.6)
ax_bnd.scatter(Xtr_s[ytr == 1, 0], Xtr_s[ytr == 1, 1], s=14, c="tab:purple",
               label="class 1", alpha=0.6)

# Boundary is where z = 0, i.e. w0*x0 + w1*x1 + b = 0  ->  x1 = -(w0*x0 + b)/w1
xs = np.linspace(Xtr_s[:, 0].min() - 0.3, Xtr_s[:, 0].max() + 0.3, 100)
snapshots = [1, 3, 10, 40, 200, 500]
for k, epoch in enumerate(snapshots):
    w, b = good.w_history_[epoch]
    if abs(w[1]) < 1e-9:
        continue
    ys = -(w[0] * xs + b) / w[1]
    shade = 0.85 - 0.85 * k / (len(snapshots) - 1)   # light -> black
    ax_bnd.plot(xs, ys, color=str(shade), lw=1.6,
                label=f"epoch {epoch}" if epoch in (1, 500) else None)

ax_bnd.set_ylim(Xtr_s[:, 1].min() - 0.5, Xtr_s[:, 1].max() + 0.5)
ax_bnd.set_xlabel("feature 1 (standardised)")
ax_bnd.set_ylabel("feature 2 (standardised)")
ax_bnd.set_title("Decision boundary walking into place")
ax_bnd.legend(loc="best", fontsize=8)

plt.tight_layout()
plt.savefig("descent.png", dpi=130)
print("wrote descent.png")
```

Expected: a file `descent.png`. In the left panel the green curve (`lr = 0.5`) plunges and flattens near 0.21; the blue curve (`lr = 0.005`) is still sloping down at epoch 500; the red curve (`lr = 800`) spikes above the grey `ln 2` line and thrashes. In the right panel you see six lines from pale grey to black, sweeping from a near-random starting angle to the final separating line.

**Why the boundary is a straight line:** the model predicts class 1 when `p ≥ 0.5`, which happens exactly when `z ≥ 0`, which is `w₀x₀ + w₁x₁ + b ≥ 0` — the equation of a straight line. Logistic regression can only ever draw a straight line. That limitation is the entire reason Module 5 exists.

---

## ✍️ Practice

### [Warm-up] 1 — Sigmoid by hand, both directions

A trained model has `w = [0.8, −1.5]` and `b = 0.2`.

(a) Compute `z` and `p` by hand for `x = [2, 1]`. Show the multiplication and the exponential.
(b) Do the same for `x = [0, 3]`.
(c) What raw score `z` would produce `p = 0.9`? Use the inverse formula.
(d) Verify all three with a two-line Python check.

**Done looks like:** three probabilities to 6 decimal places and a Python printout that matches them.

---

### [Warm-up] 2 — Log loss versus squared error

Four predictions: `y = [1, 0, 1, 0]`, `p = [0.80, 0.30, 0.40, 0.95]`.

(a) Compute the per-row log loss and the mean, by hand.
(b) Compute the per-row squared error and the mean, by hand.
(c) Which row is the worst under each measure? Give the share of total loss that row is responsible for under each.
(d) Write one sentence explaining what the difference in shares implies about which errors each loss will push the model to fix first.

**Done looks like:** two tables of four numbers plus two means, and a one-sentence conclusion.

---

### [Build] 3 — Three iterations on paper, then verified

New dataset: `x = [0, 1, 2, 3]`, `y = [0, 0, 1, 1]`. Start at `w = 0, b = 0`. Use `lr = 2.0`, full batch.

(a) Do three complete iterations by hand. For each, show `p` for all four rows, the loss, both gradients, and the updated `w` and `b`.
(b) Write a short script that reproduces your numbers.
(c) The bias gradient is 0 on iteration 0 but not afterwards. Explain why in one sentence.

**Done looks like:** a table with columns `iter | w | b | loss | grad_w | grad_b` for iterations 0–3, matching your script to 6 decimal places.

---

### [Build] 4 — Find the largest stable learning rate

Using `MyLogisticRegression` on the Hands-On dataset (standardised, 300 epochs, full batch), sweep `lr` over `[0.01, 0.1, 1, 3, 10, 30, 100, 300, 1000]`.

(a) For each, report the final loss, the worst loss seen, whether the curve was monotone decreasing, and the test accuracy.
(b) Identify the **largest** learning rate that is still monotone.
(c) Show that the largest monotone learning rate reaches a lower loss in 300 epochs than `lr = 0.1` does.
(d) Re-run the sweep on **unstandardised** data and report what changes.

**Done looks like:** two results tables and a stated "largest stable lr" value with evidence.

---

### [Stretch] 5 — Add L2 regularisation and match sklearn's `C`

scikit-learn's `LogisticRegression(C=...)` minimises `n·C·(log loss) + ½‖w‖²`, which is equivalent to minimising `log loss + (λ/2)‖w‖²` with `λ = 1/(n·C)`.

(a) Add an `l2` parameter to `MyLogisticRegression` so the weight gradient becomes `grad_w + l2 * w`. Do **not** regularise the bias — explain in one line why not.
(b) For `λ ∈ {0, 0.01, 0.1, 1.0}`, train your model and compare its weights against `LogisticRegression(C=1/(λ·n))`.
(c) Report the maximum absolute weight difference for each λ. Aim for < 0.01.
(d) Describe in one sentence what happens to the weights as λ grows, and why.

**Done looks like:** a four-row comparison table (λ, your weights, sklearn's weights, max diff) with all differences under 0.01.

---

### [Stretch] 6 — Prove that squared error stalls

Show numerically that squared-error-plus-sigmoid has vanishing gradients when the model is confidently wrong, and log-loss-plus-sigmoid does not.

(a) Derive `dL/dz` for `L = (y − p)²` with `p = σ(z)`. (Hint: chain rule, and `dp/dz = p(1 − p)`.)
(b) For `y = 1` and `z ∈ {−6, −3, 0, 3, 6}`, tabulate `p`, `dL/dz` under log loss, `dL/dz` under squared error, and the ratio.
(c) Train two versions of `MyLogisticRegression` — one with the log-loss gradient, one with the squared-error gradient — for 500 epochs at `lr = 0.5` from a *deliberately bad* start of `w = [-6.0, 6.0], b = 0.0`. Report the training accuracy of each.
(d) Write two sentences connecting your table in (b) to your result in (c).

**Done looks like:** a five-row gradient table, two accuracy numbers, and the written connection.

---

## 🤔 Think Deeper

**1. Gradient descent only guarantees you find *a* bottom, not *the* bottom — unless the loss is convex. Logistic regression's loss is convex; a neural network's is not. So why does anyone bother with neural networks?**

*How to reason about it:* separate two questions — "can I reliably find the best settings of this model?" and "how good is the best setting of this model?" Logistic regression wins the first question outright and can only ever draw straight lines. A neural network loses the first question and can draw almost anything. Think about which one limits you more on a problem like handwriting recognition. Then consider a third possibility: maybe for very large networks the local bottoms are all roughly as good as each other, so the first question stops mattering.

**2. Your gradient descent implementation minimises log loss. But in Module 3 you learned that the metric that matters might be recall at a fixed precision, or expected cost with a 50:1 penalty. Why don't we just do gradient descent directly on the metric we care about?**

*How to reason about it:* ask what the gradient of "recall" is. Recall counts things — it changes in jumps as predictions cross the threshold, and is perfectly flat in between. What does gradient descent do on a function that is flat everywhere except at jumps? Then think about the two-step workaround you already know from Module 3 (optimise a smooth **surrogate** loss, then tune the threshold against the real metric), and ask what that workaround might be leaving on the table.

**3. A hiring-screening model is trained with gradient descent on ten years of a company's past hires. The loss goes down beautifully and the model matches historical decisions with 94% accuracy. Is a lower loss always a better model?**

*How to reason about it:* write out exactly what the loss function is measuring — "agreement with the labels we were given." Then ask where those labels came from and what a *perfect* score would mean in that light. Consider whether there is any term in log loss that could possibly notice a pattern of unfair past decisions. If the answer is no, ask where in the pipeline from Modules 1–3 that check would have to live instead — and who has to decide to put it there.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Loss becomes `nan` after a few epochs | `ln(0)` when a probability is clipped-free and hits exactly 0 or 1, or an overflow in `exp` | Clip `p` to `[1e-12, 1 − 1e-12]` before the log, and use the branching stable sigmoid |
| Loss goes *up* and never recovers | Learning rate too large; the steps leap over the valley | Divide `lr` by 10 until the full-batch curve is monotone decreasing, then use the largest stable one |
| Loss falls fast then stops at 0.6931 | 0.6931 is `ln 2` — the model is predicting 0.5 for everything. Usually the features are all zeros after a bad scaler, or the learning rate is so small nothing has moved | Print `w` and `b`; print `X.mean()` and `X.std()` per column; check that the scaler was actually applied |
| Your weights don't match sklearn's | You forgot `penalty=None`; sklearn regularises by default | Pass `penalty=None`, or add the matching L2 term to your own gradient |
| Model works on train data, useless on new data, and it seemed fine | Fitting `StandardScaler` on the full dataset before splitting — Module 2's preprocessing leakage | Fit the scaler on train only, then `transform` train and test separately |
| Gradient descent takes 50,000 epochs and still crawls | Features on wildly different scales create a long thin loss canyon | Standardise every numeric feature; re-tune `lr` afterwards |
| Sign error: loss increases even at tiny `lr` | Wrote `w += lr * grad` instead of `w -= lr * grad` | The gradient points *uphill*. Always subtract. Test on the 4-row worked example — you know the right answers |
| Comparing mini-batch and full-batch by "epochs" and concluding mini-batch is magic | An epoch of mini-batch is many more weight updates than an epoch of full-batch | Compare by weight updates or by wall-clock time, not by epochs |

---

## 🛠️ Mini-Project — Descent From Scratch

**Goal.** Build, tune, visualise, and validate your own gradient-descent logistic regression, and prove it matches scikit-learn.

**Time.** 60–90 minutes.

### Starter steps

1. **Data.** Use `make_classification(n_samples=400, n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1, class_sep=1.0, flip_y=0.05, random_state=7)`. Split 75/25 stratified. Standardise with a scaler fit on **train only**.

2. **Implement.** Write `MyLogisticRegression` yourself — do not copy the Hands-On file, type it. It must record `loss_history_` and `w_history_` every epoch. Use the numerically stable sigmoid and clipped log loss.

3. **Three learning rates.** Train with `lr ∈ {0.005, 0.5, 800}` for 500 full-batch epochs. For each, record: starting loss, loss at epoch 100, final loss, worst loss seen, whether the curve is monotone (`np.all(np.diff(history) <= 0)`), and test accuracy.

4. **Loss-curve figure.** Plot all three curves on one axes with a log y-scale and a dashed horizontal line at `ln 2`. Label them.

5. **Moving-boundary figure.** For the good learning rate, plot the training points and overlay the decision boundary at epochs 1, 3, 10, 40, 200, 500, shading from pale grey to black. Remember the boundary is `x₁ = −(w₀x₀ + b) / w₁`.

6. **Match sklearn.** Train your model at `lr = 0.5` for 5,000 epochs. Fit `LogisticRegression(penalty=None, solver="lbfgs", max_iter=5000)` on the identical arrays. Print both weight vectors, both biases, both test accuracies, and `max|w_mine − w_sk|`.

7. **Batch size comparison.** Run 100 epochs at `lr = 0.5` with `batch_size ∈ {None, 32, 1}`. Report final train loss, test accuracy, and number of weight updates for each.

8. **Write a five-line README** stating: your chosen learning rate and why, your accuracy gap versus sklearn, and one sentence on what the `lr = 800` curve looked like.

### Success criteria checklist

- [ ] Loss decreases **monotonically** for `lr = 0.5` — verified with `np.all(np.diff(loss_history) <= 1e-12)`, printed as `True`, not eyeballed.
- [ ] `lr = 0.005` is monotone but clearly has not converged (final loss well above the `lr = 0.5` final loss).
- [ ] `lr = 800` produces a non-monotone curve whose worst loss exceeds `ln 2 = 0.6931`.
- [ ] Your test accuracy is within **2 percentage points** of sklearn's.
- [ ] `max|w_mine − w_sk| < 0.01`.
- [ ] `descent.png` contains both panels with axis labels, a title, and a legend.
- [ ] The moving-boundary panel shows at least six boundary lines and the last one visibly separates the classes.
- [ ] The batch-size table reports weight updates, not just epochs.
- [ ] Nothing in your gradient code imports `sklearn.linear_model` — sklearn appears only in the comparison.

### Level it up

Add **momentum** to your optimiser. Instead of `w ← w − lr·g`, keep a running velocity:

```
v ← β·v + (1 − β)·g          # β = 0.9 is standard
w ← w − lr·v
```

Momentum lets the optimiser build speed along the consistent downhill direction and cancel out the side-to-side oscillation. Re-run all three learning rates with and without momentum and report how many epochs each needs to reach a loss of 0.25. You should find momentum reaches it in far fewer epochs at small `lr`, and — more interestingly — that it makes the *large* learning rate worse, not better. Explain why in two sentences. (You will meet this again in Module 6 as `torch.optim.SGD(..., momentum=0.9)`.)

---

## 🔑 Key Takeaways

- **The sigmoid turns any real number into a probability**: `σ(z) = 1/(1 + e^(−z))`, with `σ(0) = 0.5`. Its inverse is the log-odds, `z = ln(p/(1−p))`.
- **Log loss, not squared error, is the right loss for classification.** It is unbounded above, so confidently-wrong predictions dominate the loss and get fixed first. A know-nothing model scores exactly `ln 2 = 0.6931`.
- **The gradient of log loss for logistic regression is `(1/n)·Xᵀ(p − y)` — error times feature, averaged.** The messy sigmoid derivative cancels out. That cancellation is why sigmoid and log loss are always paired.
- **The update rule is one line: `w ← w − lr·gradient`.** The minus sign is the whole algorithm; the gradient points uphill and you go the other way.
- **The learning rate is the highest-leverage number you choose.** Too small = slow but safe. Too large = the loss climbs and the model gets worse. For full-batch on a convex loss, a good learning rate gives a monotonically decreasing curve, every epoch.
- **Mini-batch is the default in practice** because it takes many more weight updates per pass over the data, at almost no cost in gradient quality.
- **Forty lines of NumPy matches scikit-learn to three decimals** on a convex problem, because there is exactly one right answer and both methods find it. `fit()` is not magic; it is this loop, optimised.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Weight** | How strongly one input pushes the answer up or down | `w = −1.5` on "days late" means being late pushes the prediction down hard |
| **Bias** | A constant added to every prediction; slides the whole model up or down | `b = 0.2` makes every prediction slightly more positive |
| **Logit / raw score (z)** | The weighted sum, before it becomes a probability. Can be any number | `z = 1.4` |
| **Sigmoid** | The S-shaped squasher that turns any number into a probability between 0 and 1 | `σ(1.4) = 0.802` |
| **Odds** | Probability of yes divided by probability of no | `p = 0.9` → odds = 9, "9 to 1 on" |
| **Log-odds** | The natural log of the odds; exactly the same thing as `z` | `ln(9) = 2.197` |
| **Loss function** | One number that says how wrong the model is right now. Lower is better | Log loss = 0.21 |
| **Log loss (cross-entropy)** | A loss that measures your surprise; punishes confident wrongness enormously | Saying 5% when the truth was yes costs 2.996 |
| **Squared error** | `(truth − prediction)²`. Right for regression, wrong for classification | `(1 − 0.4)² = 0.36` |
| **Derivative** | The slope: how much the output moves when you nudge the input a hair | Slope of `w²` at `w = 3` is 6 |
| **Gradient** | All the slopes at once, one per weight, packed in a vector. Points uphill | `[0.265, −0.081]` |
| **Gradient descent** | Repeatedly step in the opposite direction of the gradient | `w ← w − 0.5 × 0.265` |
| **Learning rate** | Your stride length when stepping downhill | `lr = 0.5` |
| **Divergence** | When the loss climbs instead of falling because the steps are too big | Loss 0.69 → 17.97 at `lr = 800` |
| **Epoch** | One full pass over all the training data | 500 epochs |
| **Step / iteration** | One weight update | 400 rows, batch 32 → 13 steps per epoch |
| **Batch GD** | Use every row to compute one gradient, then step once | 1 update per epoch |
| **Mini-batch GD** | Use a chunk of 32 or 64 rows per step | 13 updates per epoch |
| **Stochastic GD (SGD)** | Use one row per step | 400 updates per epoch |
| **Convex** | Bowl-shaped: one bottom, no traps. Logistic regression's loss is convex | Any sane `lr` finds the same answer |
| **Convergence criterion** | The rule that tells you to stop training | Stop when loss changes by less than `1e-6` |
| **Numerical gradient** | Estimating a slope by nudging the input and dividing | `(f(w+ε) − f(w−ε)) / 2ε` |
| **Momentum** | Letting the optimiser build speed in a consistent downhill direction | `v ← 0.9v + 0.1g` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Sigmoid by hand, both directions

**(a) `x = [2, 1]`, `w = [0.8, −1.5]`, `b = 0.2`.**

```
z = 0.8 × 2 + (−1.5) × 1 + 0.2
  = 1.6 − 1.5 + 0.2
  = 0.3

e^(−0.3) = 0.740818
p = 1 / (1 + 0.740818) = 1 / 1.740818 = 0.574443
```

**p = 0.574443.** Barely above a coin flip — the two features nearly cancelled.

**(b) `x = [0, 3]`.**

```
z = 0.8 × 0 + (−1.5) × 3 + 0.2
  = 0 − 4.5 + 0.2
  = −4.3

e^(4.3) = 73.699794
p = 1 / (1 + 73.699794) = 1 / 74.699794 = 0.013387
```

**p = 0.013387.** Very confidently class 0.

**(c) What `z` gives `p = 0.9`?**

```
z = ln( 0.9 / 0.1 ) = ln(9) = 2.197225
```

Check: `e^(−2.197225) = 0.111111`, `1/(1.111111) = 0.900000`. ✅

**(d) Verification:**

```python
import numpy as np
sig = lambda z: 1 / (1 + np.exp(-z))
w, b = np.array([0.8, -1.5]), 0.2
for x in ([2, 1], [0, 3]):
    z = float(np.dot(w, x) + b)
    print(f"x={x}  z={z:.6f}  p={sig(z):.6f}")
print("z for p=0.9:", np.log(0.9 / 0.1))
```

```
x=[2, 1]  z=0.300000  p=0.574443
x=[0, 3]  z=-4.300000  p=0.013387
z for p=0.9: 2.1972245773362196
```

---

### 2 — Log loss versus squared error

**(a) Log loss per row.** `y = [1, 0, 1, 0]`, `p = [0.80, 0.30, 0.40, 0.95]`.

| Row | `y` | `p` | Formula | Value |
|---|---|---|---|---|
| 1 | 1 | 0.80 | `−ln(0.80)` | 0.223144 |
| 2 | 0 | 0.30 | `−ln(1 − 0.30) = −ln(0.70)` | 0.356675 |
| 3 | 1 | 0.40 | `−ln(0.40)` | 0.916291 |
| 4 | 0 | 0.95 | `−ln(1 − 0.95) = −ln(0.05)` | 2.995732 |

```
Sum  = 0.223144 + 0.356675 + 0.916291 + 2.995732 = 4.491842
Mean = 4.491842 / 4 = 1.122960
```

**(b) Squared error per row.**

| Row | Formula | Value |
|---|---|---|
| 1 | `(1 − 0.80)² = 0.20²` | 0.0400 |
| 2 | `(0 − 0.30)² = 0.30²` | 0.0900 |
| 3 | `(1 − 0.40)² = 0.60²` | 0.3600 |
| 4 | `(0 − 0.95)² = 0.95²` | 0.9025 |

```
Sum  = 0.0400 + 0.0900 + 0.3600 + 0.9025 = 1.3925
Mean = 1.3925 / 4 = 0.348125
```

**(c) Worst row and its share.**

Row 4 is worst under both — the model said 95% and the answer was no.

```
Log loss share    : 2.995732 / 4.491842 = 0.6669  →  66.7% of the total
Squared error share: 0.9025 / 1.3925    = 0.6481  →  64.8% of the total
```

They look similar here, but push the prediction further: at `p = 0.999` for `y = 0`, log loss for that row is 6.908 (share would climb above 82%) while squared error is capped at 0.998 — its share can never exceed a bounded fraction, no matter how absurd the prediction.

**(d) One sentence.**

Log loss gives an unbounded penalty for confident wrongness, so its gradient is largest exactly on the rows where the model is most catastrophically wrong; squared error caps out at 1.0 per row, so a confidently-wrong row and a merely-wrong row look similar to it and the model has little incentive to prioritise the disaster.

Verification:

```python
import numpy as np
y = np.array([1, 0, 1, 0.]); p = np.array([0.8, 0.3, 0.4, 0.95])
ll = -(y * np.log(p) + (1 - y) * np.log(1 - p))
print(np.round(ll, 6), ll.mean())          # [0.223144 0.356675 0.916291 2.995732] 1.1229603751702717
print(np.round((y - p) ** 2, 6), np.mean((y - p) ** 2))   # [0.04 0.09 0.36 0.9025] 0.348125
```

---

### 3 — Three iterations on paper, then verified

`x = [0, 1, 2, 3]`, `y = [0, 0, 1, 1]`, `w = 0`, `b = 0`, `lr = 2.0`, full batch.

**Iteration 0.** `z = 0` everywhere → `p = [0.5, 0.5, 0.5, 0.5]`.

```
loss = −(1/4)[ ln(0.5) + ln(0.5) + ln(0.5) + ln(0.5) ] = 0.693147

p − y = [ +0.5, +0.5, −0.5, −0.5 ]

grad_w = (1/4)[ (0.5)(0) + (0.5)(1) + (−0.5)(2) + (−0.5)(3) ]
       = (1/4)[ 0 + 0.5 − 1.0 − 1.5 ] = (1/4)(−2.0) = −0.500000
grad_b = (1/4)[ 0.5 + 0.5 − 0.5 − 0.5 ] = 0.000000

w ← 0 − 2.0(−0.5) = 1.000000
b ← 0 − 2.0(0)    = 0.000000
```

**Iteration 1.** `w = 1.0`, `b = 0`, so `z = [0, 1, 2, 3]`.

```
p = [ σ(0), σ(1), σ(2), σ(3) ] = [0.500000, 0.731059, 0.880797, 0.952574]

loss = −(1/4)[ ln(0.5) + ln(1−0.731059) + ln(0.880797) + ln(0.952574) ]
     = −(1/4)[ −0.693147 − 1.313262 − 0.126928 − 0.048587 ]
     = (1/4)(2.181924) = 0.545481

p − y = [ +0.500000, +0.731059, −0.119203, −0.047426 ]

grad_w = (1/4)[ (0.5)(0) + (0.731059)(1) + (−0.119203)(2) + (−0.047426)(3) ]
       = (1/4)[ 0 + 0.731059 − 0.238406 − 0.142278 ]
       = (1/4)(0.350375) = 0.087594
grad_b = (1/4)[ 0.5 + 0.731059 − 0.119203 − 0.047426 ] = (1/4)(1.064430) = 0.266107

w ← 1.000000 − 2.0(0.087594) = 0.824812
b ← 0.000000 − 2.0(0.266107) = −0.532215
```

**Iteration 2.** `w = 0.824812`, `b = −0.532215`.

```
z = [ −0.532215, 0.292597, 1.117409, 1.942221 ]
p = [  0.370000, 0.572632, 0.753508, 0.874596 ]

loss = −(1/4)[ ln(0.630000) + ln(0.427368) + ln(0.753508) + ln(0.874596) ]
     = −(1/4)[ −0.462035 − 0.850072 − 0.283117 − 0.133993 ]
     = (1/4)(1.729217) = 0.432289

p − y = [ +0.370000, +0.572632, −0.246492, −0.125404 ]

grad_w = (1/4)[ 0 + 0.572632 − 0.492984 − 0.376212 ] = (1/4)(−0.296564) = −0.074141
grad_b = (1/4)[ 0.370000 + 0.572632 − 0.246492 − 0.125404 ] = (1/4)(0.570736) = 0.142684

w ← 0.824812 − 2.0(−0.074141) = 0.973094
b ← −0.532215 − 2.0(0.142684) = −0.817583
```

**Iteration 3 state.** `w = 0.973094`, `b = −0.817583` → `p = [0.306277, 0.538800, 0.755581, 0.891068]`, loss **0.383802**.

**Summary table.**

| iter | `w` | `b` | loss | `grad_w` | `grad_b` |
|---|---|---|---|---|---|
| 0 | 0.000000 | 0.000000 | 0.693147 | −0.500000 | 0.000000 |
| 1 | 1.000000 | 0.000000 | 0.545481 | 0.087594 | 0.266107 |
| 2 | 0.824812 | −0.532215 | 0.432289 | −0.074141 | 0.142684 |
| 3 | 0.973094 | −0.817583 | 0.383802 | −0.069208 | 0.122932 |

**(b) Script:**

```python
import numpy as np
sig = lambda z: 1 / (1 + np.exp(-z))
x = np.array([0., 1., 2., 3.]); y = np.array([0., 0., 1., 1.])
w = b = 0.0; lr = 2.0
for t in range(4):
    p = sig(w * x + b)
    loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    gw = np.mean((p - y) * x); gb = np.mean(p - y)
    print(f"iter {t}: w={w:.6f} b={b:.6f} loss={loss:.6f} gw={gw:.6f} gb={gb:.6f}")
    print(f"        p={np.round(p, 6)}")
    w -= lr * gw; b -= lr * gb
```

```
iter 0: w=0.000000 b=0.000000 loss=0.693147 gw=-0.500000 gb=0.000000
        p=[0.5 0.5 0.5 0.5]
iter 1: w=1.000000 b=0.000000 loss=0.545481 gw=0.087594 gb=0.266107
        p=[0.5      0.731059 0.880797 0.952574]
iter 2: w=0.824812 b=-0.532215 loss=0.432289 gw=-0.074141 gb=0.142684
        p=[0.37     0.572632 0.753508 0.874596]
iter 3: w=0.973094 b=-0.817583 loss=0.383802 gw=-0.069208 gb=0.122932
        p=[0.306277 0.5388   0.755581 0.891068]
```

Matches. ✅

**(c) Why `grad_b = 0` on iteration 0 only.**

`grad_b` is the mean of `p − y`, i.e. `mean(p) − mean(y)`. On iteration 0 every `p = 0.5` and the labels are two 0s and two 1s, so `mean(y) = 0.5` too, and the difference is exactly zero. Once the weights move, the predictions are no longer all 0.5 and their average drifts away from 0.5, so the bias gradient becomes non-zero.

---

### 4 — Find the largest stable learning rate

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from gd_logreg import MyLogisticRegression

X, y = make_classification(n_samples=400, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1,
                           class_sep=1.0, flip_y=0.05, random_state=7)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=7)
sc = StandardScaler().fit(Xtr)
A, B = sc.transform(Xtr), sc.transform(Xte)

def sweep(A, B, label):
    print(f"--- {label} ---")
    for lr in [0.01, 0.1, 1, 3, 10, 30, 100, 300, 1000]:
        m = MyLogisticRegression(lr=lr, n_epochs=300, tol=0.0).fit(A, ytr)
        h = np.array(m.loss_history_)
        mono = bool(np.all(np.diff(h) <= 1e-12))
        print(f"  lr={lr:<6} final={h[-1]:8.4f} worst={h.max():9.4f} "
              f"monotone={str(mono):5} acc={m.score(B, yte):.4f}")

sweep(A, B, "standardised")
sweep(Xtr, Xte, "raw (unstandardised)")
```

**(a) Standardised results:**

```
--- standardised ---
  lr=0.01   final=  0.3557 worst=   0.6931 monotone=True  acc=0.9300
  lr=0.1    final=  0.2251 worst=   0.6931 monotone=True  acc=0.9400
  lr=1      final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=3      final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=10     final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=30     final=  0.2468 worst=   0.9087 monotone=False acc=0.9400
  lr=100    final=  1.0409 worst=   4.2884 monotone=False acc=0.9300
  lr=300    final=  0.5194 worst=  13.4879 monotone=False acc=0.9500
  lr=1000   final=  1.3224 worst=  13.7870 monotone=False acc=0.9400
```

**(b) Largest monotone learning rate: `lr = 10`.** At `lr = 30` the worst loss rises to 0.9087, above the starting `ln 2 = 0.6931`, so the curve climbed at some point — not monotone.

**(c) Comparison at 300 epochs:**

```
lr = 0.1 : final loss 0.2251
lr = 10  : final loss 0.2157   ← lower by 0.0094
```

`lr = 10` also reaches 0.2157 — the converged value — while `lr = 0.1` is still 0.009 above it and still creeping down. The 100× bigger step gets to the bottom; the small one is still walking.

**(d) Unstandardised.**

```
--- raw (unstandardised) ---
  lr=0.01   final=  0.3241 worst=   0.6931 monotone=True  acc=0.9200
  lr=0.1    final=  0.2235 worst=   0.6931 monotone=True  acc=0.9400
  lr=1      final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=3      final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=10     final=  0.2157 worst=   0.6931 monotone=True  acc=0.9500
  lr=30     final=  0.5878 worst=   1.2587 monotone=False acc=0.8600
  lr=100    final=  0.5720 worst=   3.7232 monotone=False acc=0.9300
  lr=300    final=  1.6795 worst=   8.7137 monotone=False acc=0.8600
  lr=1000   final=  1.5943 worst=  14.8035 monotone=False acc=0.9400
```

The honest answer for *this* dataset: **not much changes.** `make_classification` already produces columns with standard deviations of 1.319 and 1.108 and means near zero, so it is nearly standardised out of the box. The largest monotone rate is still 10, and the breakdown at `lr = 30` is a little more violent (worst loss 1.2587 rather than 0.9087) — that is all.

That is a genuinely useful finding, and you should say so in your write-up rather than pretending to see a dramatic effect. To see the real damage, exaggerate the problem deliberately: multiply column 1 by 1000 before training. Then at `lr = 1.0` the loss jumps from 0.6931 to **1.6579 within 50 epochs and stays at 1.6579 forever**. The sigmoid has saturated — every `|z|` is in the hundreds, so every `p` is pinned at 0 or 1, every gradient is effectively zero, and the model is frozen in a terrible place with no way out. *That* is the argument for standardising before gradient descent, and it is worth reproducing yourself:

```python
Xbad = Xtr.copy(); Xbad[:, 1] *= 1000.0
m = MyLogisticRegression(lr=1.0, n_epochs=200, tol=0.0).fit(Xbad, ytr)
print([round(v, 4) for v in m.loss_history_[::50]])   # [0.6931, 1.6579, 1.6579, 1.6579, 1.6579]
```

---

### 5 — Add L2 regularisation and match sklearn's `C`

**(a) The change is one term.** Inside the update, use:

```python
grad_w = (Xb.T @ err) / len(idx) + self.l2 * self.w_   # <-- added
grad_b = float(err.mean())                             # bias NOT regularised
```

Add `l2=0.0` to `__init__` and store it as `self.l2`.

**Why not regularise the bias:** the bias sets the model's baseline rate — how often it predicts class 1 when all features are at their average. Shrinking it toward zero forces the baseline toward `σ(0) = 50%`, which is simply wrong if the true base rate is, say, 5%. Regularisation exists to stop the model over-reacting to *features*; the bias carries no feature information, so penalising it only adds bias in the statistical sense.

**(b)+(c) Comparison:**

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from gd_logreg import sigmoid   # reuse

def fit_l2(X, y, lr=0.5, n_epochs=3000, lam=0.0):
    n, d = X.shape
    w = np.zeros(d); b = 0.0
    for _ in range(n_epochs):
        p = sigmoid(X @ w + b)
        err = p - y
        w -= lr * ((X.T @ err) / n + lam * w)
        b -= lr * err.mean()
    return w, b

n = len(A)
print(f"{'lambda':>7} {'my w':>22} {'my b':>8} {'sk w':>22} {'sk b':>8} {'maxdiff':>8}")
for lam in [0.0, 0.01, 0.1, 1.0]:
    w, b = fit_l2(A, ytr.astype(float), lam=lam)
    if lam == 0:
        sk = LogisticRegression(penalty=None, solver="lbfgs", max_iter=10000).fit(A, ytr)
    else:
        sk = LogisticRegression(C=1.0 / (lam * n), solver="lbfgs", max_iter=10000).fit(A, ytr)
    diff = float(np.max(np.abs(w - sk.coef_[0])))
    print(f"{lam:>7} {str(np.round(w,4)):>22} {b:>8.4f} "
          f"{str(np.round(sk.coef_[0],4)):>22} {float(sk.intercept_[0]):>8.4f} {diff:>8.4f}")
```

| λ | sklearn `C = 1/(λn)` | My weights | My bias | sklearn weights | sklearn bias | max diff |
|---|---|---|---|---|---|---|
| 0.00 | `penalty=None` | `[1.0930, −2.9487]` | 0.8309 | `[1.0963, −2.9479]` | 0.8331 | **0.0033** |
| 0.01 | 0.3333 | `[1.0405, −2.2099]` | 0.5806 | `[1.0422, −2.2099]` | 0.5816 | **0.0017** |
| 0.10 | 0.03333 | `[0.7144, −1.0928]` | 0.1858 | `[0.7147, −1.0926]` | 0.1862 | **0.0003** |
| 1.00 | 0.003333 | `[0.2380, −0.2959]` | 0.0337 | `[0.2380, −0.2959]` | 0.0337 | **0.0000** |

All differences are far under 0.01. ✅

**(d) One sentence.** As λ grows the weights shrink toward zero — from `[1.09, −2.95]` down to `[0.24, −0.30]`, a factor of about ten — because the `λ·w` term in the gradient is a constant pull toward the origin that eventually balances the data's pull outward; the model becomes less confident and its decision boundary flattens.

---

### 6 — Prove that squared error stalls

**(a) Derivation.** For `L = (y − p)²` with `p = σ(z)`:

```
dL/dp = 2(p − y)                        (chain rule on the square)
dp/dz = p(1 − p)                        (derivative of sigmoid)

dL/dz = 2(p − y) · p(1 − p)
```

Compare with log loss, where `dL/dz = (p − y)` — the `p(1 − p)` factor is **not** there because it cancelled. Squared error keeps it, and `p(1 − p)` is ~0 whenever `p` is near 0 or 1.

**(b) Table for `y = 1`:**

| `z` | `p = σ(z)` | `dL/dz` (log loss) | `dL/dz` (squared error) | ratio SE / LL |
|---|---|---|---|---|
| −6 | 0.002473 | −0.997527 | −0.004921 | **0.004933** |
| −3 | 0.047426 | −0.952574 | −0.086068 | 0.090353 |
| 0 | 0.500000 | −0.500000 | −0.250000 | 0.500000 |
| +3 | 0.952574 | −0.047426 | −0.004285 | 0.090353 |
| +6 | 0.997527 | −0.002473 | −0.000012 | 0.004933 |

Read row 1. The model says there is a 0.2% chance and the truth is yes — the worst possible mistake. Log loss produces a gradient of magnitude 0.998, essentially the maximum. Squared error produces 0.0049 — **203 times smaller**. The loss that should be screaming is whispering.

**(c) Training from a deliberately bad start:**

```python
import numpy as np
from gd_logreg import sigmoid, log_loss_mean

def train(A, y, use_log_loss, lr=0.5, n_epochs=500):
    w = np.array([-6.0, 6.0]); b = 0.0
    n = len(A)
    for _ in range(n_epochs):
        p = sigmoid(A @ w + b)
        if use_log_loss:
            dz = (p - y)
        else:
            dz = 2 * (p - y) * p * (1 - p)
        w -= lr * (A.T @ dz) / n
        b -= lr * dz.mean()
    acc = float(((sigmoid(A @ w + b) >= 0.5).astype(int) == y).mean())
    return w, b, acc

yf = ytr.astype(float)
for name, flag in [("log loss", True), ("squared error", False)]:
    w, b, acc = train(A, yf, flag)
    print(f"{name:>14}: w={np.round(w,4)}  b={b:.4f}  train acc={acc:.4f}")
```

Output:

```
      log loss: w=[ 1.0988 -2.936 ]  b=0.8297  train acc=0.9467
 squared error: w=[-4.696   3.1559]  b=5.2671  train acc=0.2200
```

The log-loss run escapes the bad initialisation completely and reaches **94.67%** training accuracy — it lands essentially on top of the answer the well-initialised model found (`[1.093, −2.949]`). The squared-error run has barely moved: after 500 epochs its weights are still near the terrible starting point `[−6, 6]`, and its training accuracy is **22%** — far *worse* than a coin, because it is still confidently predicting the opposite of the truth and has no gradient strong enough to escape.

**(d) The connection, in two sentences.**

The bad initialisation puts almost every row at a large `|z|`, where `p(1 − p)` is nearly zero; squared error multiplies its gradient by exactly that factor, so every gradient it produces is two or three orders of magnitude too small to move the weights within 500 epochs. Log loss has that factor cancelled out of its gradient, so its signal stays at full strength `(p − y)` no matter how saturated the sigmoid is — which is precisely why classification uses log loss and why the sigmoid/cross-entropy pairing is not an accident.

</details>

---

[⬅ Previous](module-03-evaluation-metrics.md) · [Level 3 Home](README.md) · [Next ➡](module-05-neural-networks-from-scratch.md)
