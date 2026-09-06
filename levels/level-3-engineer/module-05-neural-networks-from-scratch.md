# Module 5 — Neural Networks From Scratch: Neurons, Layers, and Backprop

**Level 3 · Module 5 · ~6 hours · Prereqs: Module 4 (sigmoid, log loss, gradients, the update rule) and Module 2 (StandardScaler, train/test discipline).**

[⬅ Previous](module-04-logistic-regression-gradient-descent.md) · [Level 3 Home](README.md) · [Next ➡](module-06-pytorch-deep-learning.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to compute a single neuron's output by hand from weights, inputs, a bias, and an activation function — for ReLU, sigmoid, and tanh.
2. You will be able to trace a full forward pass through a 2-layer network with real numbers, showing every intermediate matrix.
3. You will be able to derive backpropagation for that network using the chain rule, and compute all four gradient arrays by hand.
4. You will be able to verify your analytic gradients against a numerical gradient to a relative error below `1e-6`.
5. You will be able to explain why weight initialization matters, and demonstrate a network failing because of a bad one.
6. You will be able to explain the dead-ReLU problem and show it happening in a training run you cause on purpose.

---

## 🪝 The Hook

Last module you built logistic regression from nothing and matched scikit-learn. But there's a wall you can't climb: logistic regression predicts class 1 when `w·x + b ≥ 0`, which is the equation of a **straight line**. That's all it can ever draw.

Now picture two interlocking crescent moons of dots, like a yin-yang symbol. Orange on one crescent, purple on the other. A five-year-old with a crayon separates them in two seconds with a curved squiggle. Logistic regression gets **90.4%** — it slices a straight line through the middle and gives up.

Here is the strange part. Take that same logistic regression unit — weighted sum, bias, squash — and make sixteen copies of it. Feed the two coordinates into all sixteen. Then feed those sixteen outputs into one final logistic regression unit. Nothing new has been invented. It is the same little unit, just stacked and wired.

That thing gets **99.2%**, and the boundary it draws curves.

This module is why that works, and how to train it — with your own hands, on paper first and then in NumPy, checking every gradient against a number you cannot argue with.

---

## 🧠 The Concept

### 1. The neuron: weighted sum + bias + activation

> **Neuron (unit):** takes several numbers in, multiplies each by a weight, adds them up, adds a bias, and passes the result through an **activation function**.

That is exactly the logistic regression from Module 4, except the final squash doesn't have to be a sigmoid.

```
   x₁ ──w₁──┐
            ├──▶ [  Σ  ] ──▶ z ──▶ [ activation ] ──▶ a
   x₂ ──w₂──┤        ▲
            │        │
   x₃ ──w₃──┘        b
```

```
z = w₁x₁ + w₂x₂ + w₃x₃ + b        (the "pre-activation")
a = f(z)                          (the "activation" / the unit's output)
```

🍕 **Analogy.** A neuron is a single judge on a talent-show panel with a very simple brain. She scores each act by weighing three things: singing (weight 0.4), dancing (weight −0.7 — she hates dancing), and stage presence (weight 1.2). She also starts out grumpy, so she subtracts 0.5 from everything. Then she converts her internal grumbling into a public verdict: thumbs up if positive, nothing if negative. That last conversion is her activation function.

🔢 **Tiny concrete example.** `w = [0.4, −0.7, 1.2]`, `b = −0.5`, act = ReLU.

Act A scores `x = [2, 1, 0.5]`:
```
z = 0.4(2) + (−0.7)(1) + 1.2(0.5) + (−0.5)
  = 0.8 − 0.7 + 0.6 − 0.5
  = 0.2
a = ReLU(0.2) = max(0, 0.2) = 0.2      ← faint thumbs up
```

Act B scores `x = [−1, 2, 0]`:
```
z = 0.4(−1) + (−0.7)(2) + 1.2(0) + (−0.5)
  = −0.4 − 1.4 + 0 − 0.5
  = −2.3
a = ReLU(−2.3) = max(0, −2.3) = 0      ← silence
```

**The bias is what lets a neuron be picky.** With `b = −0.5`, an act needs to earn at least +0.5 from the weighted features before the judge says anything at all. Without a bias, the threshold would always be exactly zero.

---

### 2. Layers, hidden units, and why depth adds expressive power

> **Layer:** a row of neurons that all see the same inputs but have their own weights and biases.
> **Hidden layer:** a layer whose outputs you never look at directly — they only feed the next layer.
> **Multi-layer perceptron (MLP):** input layer → one or more hidden layers → output layer, everything fully connected.

```
       INPUT            HIDDEN (ReLU)          OUTPUT (sigmoid)
                        ┌──────┐
   x₁ ───────┬─────────▶│  h₁  │──────┐
             │      ┌──▶│      │      │
             │      │   └──────┘      │      ┌──────┐
             │      │   ┌──────┐      ├─────▶│  ŷ   │──▶ p
   x₂ ───────┼──────┼──▶│  h₂  │──────┤      └──────┘
             │      │   └──────┘      │
             │      │   ┌──────┐      │
             └──────┴──▶│  h₃  │──────┘
                        └──────┘
        2 inputs      3 hidden units      1 output
      W1: 2×3, b1: 1×3       W2: 3×1, b2: 1×1
```

🍕 **Analogy.** One judge can only enforce one rule: "score above the line, you pass." Three judges with different tastes can each enforce a different rule, and the head judge can then combine their three verdicts into a decision that no single judge could have reached — "pass if judge 1 likes you AND judge 3 doesn't hate you." The head judge is still doing a plain weighted sum, but she is summing *opinions*, not raw features, and opinions are already curved.

**Why the activation function is non-negotiable.** Suppose you stack two layers with no activation, just weighted sums:

```
h  = X·W1 + b1
ŷ  = h·W2 + b2
   = (X·W1 + b1)·W2 + b2
   = X·(W1·W2) + (b1·W2 + b2)
   = X·W_combined + b_combined
```

Two layers collapsed into one. Ten layers would collapse into one. Without a non-linear activation between them, depth buys you **exactly nothing** — you have an expensive way to write a straight line. The activation is what makes stacking meaningful.

🔢 **Real numbers from the Hands-On** (make_moons, 250 test rows, trained identically):

| Hidden units | Final training loss | Test accuracy |
|---|---|---|
| 1 | 0.3052 | 0.9040 |
| 2 | 0.3052 | 0.9040 |
| 4 | 0.2558 | 0.9440 |
| 8 | 0.0695 | **0.9920** |
| 16 | 0.0669 | 0.9920 |
| 64 | 0.0645 | 0.9920 |

Look at 1 and 2 hidden units: **90.40%**, identical to plain logistic regression. With one or two ReLU units the network essentially cannot bend. At 8 units it jumps nine points and then plateaus — the crescents are fully separated and more units add nothing. Capacity is real, and it is also finite in usefulness.

---

### 3. Activations: ReLU, sigmoid, softmax, and the dead-ReLU problem

| Activation | Formula | Output range | Use it for | Watch out for |
|---|---|---|---|---|
| **ReLU** | `max(0, z)` | `[0, ∞)` | Hidden layers — the default | Dead units |
| **Sigmoid** | `1/(1+e^(−z))` | `(0, 1)` | Binary output layer | Saturation kills gradients |
| **Tanh** | `(e^z − e^(−z))/(e^z + e^(−z))` | `(−1, 1)` | Older hidden layers | Also saturates |
| **Softmax** | `e^(z_k) / Σ_j e^(z_j)` | `(0, 1)`, sums to 1 | Multi-class output layer | Only for the last layer |

```
   ReLU                    Sigmoid                  Tanh
    ▲                        ▲                        ▲
  3 |        /             1 |      ....___          1|      ...___
  2 |      /                 |    ..                  |    ..
  1 |    /                 .5|---•                   0|---•
  0 |__ /                    | ..                     |  ..
    +------------▶         0 |____....         ▶    -1|__...          ▶
   -3   0    3              -6   0    6              -6   0    6
```

**Why ReLU won.** It is `max(0, z)` — one comparison, no exponentials, so it's fast. And crucially its derivative is exactly **1** for all positive inputs. Sigmoid's derivative maxes out at 0.25 and collapses toward zero at both ends; multiply five of those together while backpropagating through five layers and your gradient is `0.25⁵ ≈ 0.001` of its original size. That's the **vanishing gradient problem**, and it is why deep networks did not work before ReLU.

🍕 **Analogy for ReLU.** A one-way valve. Push forward, water flows exactly as hard as you pushed. Push backward, nothing — sealed shut.

> **Dead ReLU:** a hidden unit whose pre-activation `z` is negative for *every* training row. Its output is always 0, so its gradient is always 0, so its weights never change, so it stays dead forever. The unit is a wasted parameter for the rest of training.

🔢 **Real numbers — killing your own units on purpose** (16 hidden units, 2000 epochs):

| Learning rate | Final loss | Test accuracy | Dead hidden units |
|---|---|---|---|
| 0.5 | 0.0692 | 0.9920 | 0 / 16 |
| 5.0 | 0.0607 | 0.9880 | 0 / 16 |
| 20.0 | 0.3169 | 0.8920 | **10 / 16** |
| 100.0 | 13.8155 | 0.4960 | **16 / 16** |

At `lr = 20` a single oversized update pushes ten units' biases so far negative that they never fire again. The network limps along with six working units. At `lr = 100` every unit dies and the network outputs a constant — 49.6% accuracy is a coin flip. The learning rate lesson from Module 4 comes back, with a new failure mode attached.

**Softmax, in one paragraph.** For 3 classes the output layer has 3 units and their raw scores are `[2.0, 1.0, 0.1]`. Softmax exponentiates and normalises:
```
e^2.0 = 7.389,  e^1.0 = 2.718,  e^0.1 = 1.105     sum = 11.212
p = [7.389/11.212, 2.718/11.212, 1.105/11.212]
  = [0.6590, 0.2424, 0.0986]                       ← sums to 1.0000
```
Those are proper probabilities across mutually exclusive classes. Paired with **categorical cross-entropy** (`L = −Σ y_k ln p_k`), the gradient at the output is `p − y` — the *exact same clean form* as sigmoid + log loss from Module 4. That cancellation is not a coincidence; it happens for the whole family of these pairings.

---

### 4. The forward pass as matrix multiplication

Doing sixteen neurons one at a time with Python loops would be unbearably slow. Matrices fix this.

Stack your inputs as a matrix `X` with **one row per example** and one column per feature. Stack layer 1's weights as `W1` with **one column per hidden unit**. Then a single `@` computes every neuron for every example at once.

```
  X        @      W1       +   b1     =     Z1        →  A1 = ReLU(Z1)
(n × 2)        (2 × 16)      (1 × 16)     (n × 16)        (n × 16)

  A1       @      W2       +   b2     =     Z2        →  A2 = σ(Z2)
(n × 16)       (16 × 1)      (1 × 1)      (n × 1)         (n × 1)
```

> **Shape rule:** for `A @ B` to work, `A`'s column count must equal `B`'s row count. The result has `A`'s rows and `B`'s columns. 90% of neural network bugs are shape bugs; check them out loud.

> **Broadcasting:** `b1` has shape `(1, 16)` but `X @ W1` has shape `(n, 16)`. NumPy silently copies `b1` down all `n` rows. This is intended and is why biases are stored as row vectors.

🔢 **Shape trace for a batch of 750 training rows, 2 features, 16 hidden units:**

```
X      (750, 2)
W1     (2, 16)     →  X @ W1     (750, 16)
b1     (1, 16)     →  Z1         (750, 16)   [broadcast]
A1     (750, 16)
W2     (16, 1)     →  A1 @ W2    (750, 1)
b2     (1, 1)      →  Z2         (750, 1)
A2     (750, 1)                              one probability per row ✅
```

The whole forward pass for 750 examples is four lines of NumPy and takes microseconds.

---

### 5. The chain rule and backpropagation

Here is the only genuinely new idea in this module, and it is a rule you already know from Module 4 — applied more than once.

> **Chain rule:** if `a` affects `b` and `b` affects `c`, then `dc/da = (dc/db) × (db/da)`. Slopes multiply along a path.

🍕 **Analogy.** Rain affects traffic; traffic affects your arrival time. If one extra mm of rain adds 3 cars per minute to the road, and each extra car per minute adds 0.5 minutes to your trip, then one extra mm of rain costs you `3 × 0.5 = 1.5` minutes. You never had to model "rain → minutes" directly. You chained two local facts.

> **Backpropagation:** computing the gradient of the loss with respect to every weight by starting at the loss and applying the chain rule backwards, layer by layer, reusing the work from each layer in the one before it.

**The five backward rules.** These are all you need, and you can derive each in one line.

| Forward operation | Backward rule | Why |
|---|---|---|
| `Z2 = A1 @ W2 + b2`, `A2 = σ(Z2)`, log loss | `dZ2 = A2 − y` | The Module 4 cancellation, unchanged |
| `Z = A @ W` | `dW = A.T @ dZ` | Each weight's blame = its input times the downstream error |
| `Z = A @ W + b` | `db = dZ.sum(axis=0)` | The bias is added to every row, so its blame is the sum over rows |
| `Z = A @ W` | `dA = dZ @ W.T` | Send the error backwards through the same weights |
| `A = ReLU(Z)` | `dZ = dA * (Z > 0)` | Slope is 1 where `Z > 0`, else 0 — the valve |

Read the last one carefully. `(Z > 0)` is a boolean array of 1s and 0s. Multiplying by it **zeroes out the gradient for every unit that didn't fire on that row.** That's the ReLU valve working in reverse: no signal went forward, so no blame comes back.

```
FORWARD  ────────────────────────────────────────────────────────▶
  X ──▶ Z1 ──ReLU──▶ A1 ──▶ Z2 ──σ──▶ A2 ──▶ loss
        │            │      │         │
        │            │      │         │
  ◀─────┴────────────┴──────┴─────────┴──────────── BACKWARD
      dZ1          dA1     dZ2      (A2 − y)
       │            │       │
      dW1          dW2     db2
      db1
```

**The complete backward pass, five lines:**

```
dZ2 = (A2 − y) / n            # average over the batch, as in Module 4
dW2 = A1.T @ dZ2
db2 = dZ2.sum(axis=0)
dA1 = dZ2 @ W2.T
dZ1 = dA1 * (Z1 > 0)
dW1 = X.T @ dZ1
db1 = dZ1.sum(axis=0)
```

Then the same update rule as Module 4, applied to all four arrays:
```
W1 ← W1 − lr·dW1     b1 ← b1 − lr·db1
W2 ← W2 − lr·dW2     b2 ← b2 − lr·db2
```

That's a neural network. Everything from here — CNNs, transformers, all of it — is these same seven lines with more interesting layers in the middle.

**How do you know your derivation is right?** You check it against a number that cannot lie.

> **Numerical gradient check:** nudge one weight by a tiny `ε` in both directions, recompute the loss both times, and use `(L(w+ε) − L(w−ε)) / (2ε)`. Compare against your analytic gradient. The **relative error** `|num − ana| / (|num| + |ana|)` should be below `1e-6`.

This is agonisingly slow — one full forward pass per weight per direction — so you only ever run it on a handful of weights and a handful of rows. But it turns "I think my calculus is right" into "I verified my calculus is right", and you should never skip it when writing backprop by hand.

---

### 6. Weight initialization, epochs, and the training loop

In Module 4 you started every weight at zero and it worked fine. **Do that in a neural network and it will never learn anything.**

> **Symmetry breaking:** if every hidden unit starts with identical weights, every unit computes the same output, receives the same gradient, and updates identically. They stay clones forever. Sixteen hidden units behave as one.

With ReLU, all-zeros is even worse: every `Z1` is exactly 0, `ReLU(0) = 0`, and `(Z1 > 0)` is `False` everywhere, so `dZ1` is zero and **no hidden weight ever moves at all**.

> **He initialization:** draw each weight from a normal distribution with mean 0 and standard deviation `sqrt(2 / n_inputs_to_this_layer)`. The standard choice for ReLU networks. Biases start at 0 — they don't cause symmetry problems because the weights already differ.

Why that formula? Each unit sums `n_in` products. If the weights had a fixed spread regardless of `n_in`, the sums would get bigger and bigger as layers got wider, and the sigmoid at the end would saturate. Dividing the variance by `n_in` keeps the typical size of `z` roughly constant no matter how wide the layer is. The factor of 2 compensates for ReLU throwing away half the values.

🔢 **Real numbers — four initializations, 16 hidden units, 3000 epochs, `lr = 0.5`:**

| Init scheme | Loss at epoch 0 | Final loss | Test accuracy | Dead units |
|---|---|---|---|---|
| All zeros | 0.6931 | **0.6931** | **0.5000** | 16 / 16 |
| Tiny (σ = 0.0001) | 0.6931 | 0.3051 | 0.9040 | 0 / 16 |
| **He (σ = √(2/n_in))** | 0.7967 | **0.0669** | **0.9920** | 0 / 16 |
| Huge (σ = 50) | 10.3524 | 0.2843 | 0.9680 | 0 / 16 |

Read every row:

- **All zeros:** loss never moves off `ln 2 = 0.6931`. Every unit is dead. Accuracy 50% — literally a coin.
- **Tiny:** it does learn, but it lands on 0.3051 and 90.4% — exactly the logistic regression numbers. The units started so close together that they never differentiated; the network is behaving like a single linear model.
- **He:** starts slightly worse than random (0.7967 > 0.6931 — the initial predictions are confidently random) but ends at 0.0669 and 99.2%.
- **Huge:** starts catastrophically at 10.35 because every sigmoid is pinned at 0 or 1, and though it eventually claws back to 96.8%, it wasted thousands of epochs and never fully recovered.

**The training loop skeleton.** Memorise this shape; Module 6 uses the identical structure with PyTorch doing the middle bits:

```
initialize parameters (He)
repeat for each epoch:
    cache = forward(params, X)                  # 1. predict
    loss  = loss_fn(cache["A2"], y)             # 2. score
    grads = backward(params, cache, X, y)       # 3. blame
    for each parameter:                         # 4. step
        param -= learning_rate * grads[param]
    occasionally: evaluate on validation data
```

> **Epoch:** one full pass over the training set. In this module every epoch is one full-batch update, so epochs and steps are the same thing. In Module 6 they will not be.

---

## 🔍 Worked Example

We are going to trace **one forward pass and one complete backward pass** through a tiny 2-layer network, entirely by hand. Every number is checkable.

### The network

Two inputs, two hidden units with ReLU, one output with sigmoid.

```
W1 = [ 0.5  -0.3 ]      b1 = [ 0.1   0.05 ]
     [ 0.8   0.2 ]

W2 = [  1.0 ]           b2 = [ 0.3 ]
     [ -2.0 ]
```

`W1` is 2×2: **row `i` = input `i`, column `j` = hidden unit `j`.** So `W1[0][1] = −0.3` is the weight from input 1 to hidden unit 2.

One training example: `x = [1.0, 2.0]`, true label `y = 1`.

---

### Forward pass

**Step 1 — hidden pre-activations `Z1 = x·W1 + b1`.**

```
Hidden unit 1 (column 0 of W1):
  z₁ = (1.0)(0.5) + (2.0)(0.8) + 0.1
     = 0.5 + 1.6 + 0.1
     = 2.20

Hidden unit 2 (column 1 of W1):
  z₂ = (1.0)(−0.3) + (2.0)(0.2) + 0.05
     = −0.3 + 0.4 + 0.05
     = 0.15

Z1 = [ 2.20 , 0.15 ]
```

**Step 2 — hidden activations `A1 = ReLU(Z1)`.**

```
A1 = [ max(0, 2.20) , max(0, 0.15) ] = [ 2.20 , 0.15 ]
```

Both positive, so both units fire and ReLU passes them through unchanged. Keep `Z1` around — we need its signs on the way back.

**Step 3 — output pre-activation `Z2 = A1·W2 + b2`.**

```
Z2 = (2.20)(1.0) + (0.15)(−2.0) + 0.3
   = 2.20 − 0.30 + 0.30
   = 2.20
```

**Step 4 — output `A2 = σ(Z2)`.**

```
e^(−2.2) = 0.110803
A2 = 1 / (1 + 0.110803) = 1 / 1.110803 = 0.900250
```

The network says **90.03% chance of class 1**.

**Step 5 — loss.** `y = 1`, so:

```
L = −ln(0.900250) = 0.105083
```

Not bad already. Now let's make it better.

---

### Backward pass

**Step 6 — the output error.** By the Module 4 cancellation, `dL/dZ2 = A2 − y`:

```
dZ2 = 0.900250 − 1 = −0.099750
```

Negative, meaning: *increasing `Z2` would decrease the loss.* Correct — the true label is 1, and a bigger `Z2` means a bigger probability.

**Step 7 — gradients for the output layer.** `dW2 = A1.T @ dZ2`, and `A1` has shape (1, 2) so `A1.T` is (2, 1) and the result is (2, 1) — matching `W2`. ✅

```
dW2[0] = (2.20)(−0.099750) = −0.219451
dW2[1] = (0.15)(−0.099750) = −0.014963

db2    = dZ2 = −0.099750
```

Interpretation: hidden unit 1 was loud (2.20), so its weight gets a big correction. Hidden unit 2 was quiet (0.15), so its weight barely moves. **Loud units get blamed most.**

**Step 8 — push the error back to the hidden activations.** `dA1 = dZ2 @ W2.T`:

```
dA1[0] = (−0.099750)(1.0)  = −0.099750
dA1[1] = (−0.099750)(−2.0) = +0.199501

dA1 = [ −0.099750 , +0.199501 ]
```

Notice the sign flip on the second one. Hidden unit 2's weight into the output is negative, so *increasing* unit 2's output *decreases* `Z2` — and since we want `Z2` bigger, we want unit 2's output smaller. The gradient's positive sign says exactly that.

**Step 9 — through the ReLU valve.** `dZ1 = dA1 * (Z1 > 0)`:

```
Z1 = [2.20, 0.15], both > 0, so the mask is [1, 1]

dZ1 = [ −0.099750 × 1 , +0.199501 × 1 ] = [ −0.099750 , +0.199501 ]
```

Both gates open, so nothing is blocked. (If `z₂` had been `−0.15` instead, the mask would be `[1, 0]` and `dZ1[1]` would be **exactly zero** — that unit contributed nothing forward, so it receives no blame backward.)

**Step 10 — gradients for the hidden layer.** `dW1 = x.T @ dZ1`, an outer product of a (2,1) and a (1,2):

```
dW1[0][0] = x₁ · dZ1[0] = (1.0)(−0.099750) = −0.099750
dW1[0][1] = x₁ · dZ1[1] = (1.0)(+0.199501) = +0.199501
dW1[1][0] = x₂ · dZ1[0] = (2.0)(−0.099750) = −0.199501
dW1[1][1] = x₂ · dZ1[1] = (2.0)(+0.199501) = +0.399002

dW1 = [ −0.099750   +0.199501 ]
      [ −0.199501   +0.399002 ]

db1 = dZ1 = [ −0.099750 , +0.199501 ]
```

Every entry is **input value × downstream error**, exactly the same shape of rule as logistic regression. Input 2 was twice as large as input 1, so its weights get exactly twice the correction.

---

### Verify one gradient numerically

Let's check `dW1[0][0] = −0.099750` by brute force. Nudge that one weight by `ε = 1e-6` and recompute the loss twice.

**With `W1[0][0] = 0.500001`:**
```
z₁ = (1.0)(0.500001) + (2.0)(0.8) + 0.1 = 2.200001
Z2 = (2.200001)(1.0) + (0.15)(−2.0) + 0.3 = 2.200001
A2 = σ(2.200001) = 0.9002496
L₊ = −ln(0.9002496) = 0.10508322
```

**With `W1[0][0] = 0.499999`:**
```
z₁ = 2.199999  →  Z2 = 2.199999  →  A2 = 0.9002494
L₋ = −ln(0.9002494) = 0.10508342
```

**Numerical gradient:**
```
(L₊ − L₋) / (2ε) = (0.10508322 − 0.10508342) / (0.000002) = −0.0997505
```

Analytic said **−0.099750**. Numerical says **−0.0997505**. Relative error is about `4e-8`. Your calculus is correct. ✅

---

### Take one step and confirm the loss dropped

Apply the update rule with `lr = 0.5`:

```
W1 ← [0.5, −0.3; 0.8, 0.2] − 0.5·[−0.09975, 0.19950; −0.19950, 0.39900]
   = [ 0.549875  −0.399750 ]
     [ 0.899750   0.000499 ]

b1 ← [0.1, 0.05] − 0.5·[−0.09975, 0.19950] = [ 0.149875 , −0.049750 ]

W2 ← [1.0; −2.0] − 0.5·[−0.219451; −0.014963] = [ 1.109726 ; −1.992519 ]

b2 ← 0.3 − 0.5·(−0.099750) = 0.349875
```

**New forward pass with the updated weights:**
```
z₁ = (1.0)(0.549875) + (2.0)(0.899750) + 0.149875 = 2.499250
z₂ = (1.0)(−0.399750) + (2.0)(0.000499) + (−0.049750) = −0.448502
A1 = [2.499250, 0]                    ← unit 2 just died on this example
Z2 = (2.499250)(1.109726) + 0 + 0.349875 = 3.123434
A2 = σ(3.123434) = 0.957846
L  = −ln(0.957846) = 0.043068
```

**Loss went from 0.105083 to 0.043068.** One step, 59% of the loss gone. And notice something: hidden unit 2's pre-activation flipped negative, so on this example it is now off. On a full dataset, other rows would still be lighting it up — but if *every* row pushed it negative, that would be a dead unit.

That is a complete, honest, arithmetic-visible training step for a neural network. Everything else in deep learning is this, repeated.

---

## 💻 Hands-On

```bash
pip install numpy scikit-learn matplotlib
```

---

### Step 1 — Reproduce the hand-traced forward and backward pass

Create `trace_by_hand.py`:

```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)

W1 = np.array([[0.5, -0.3],
               [0.8,  0.2]])
b1 = np.array([[0.1, 0.05]])
W2 = np.array([[ 1.0],
               [-2.0]])
b2 = np.array([[0.3]])

x = np.array([[1.0, 2.0]])     # one example, shape (1, 2)
y = np.array([[1.0]])          # its label,   shape (1, 1)

sigmoid = lambda z: 1.0 / (1.0 + np.exp(-z))

# ---------- forward ----------
Z1 = x @ W1 + b1
A1 = np.maximum(0.0, Z1)
Z2 = A1 @ W2 + b2
A2 = sigmoid(Z2)
L = float(-(y * np.log(A2) + (1 - y) * np.log(1 - A2))[0, 0])

print("Z1 =", Z1, " A1 =", A1)
print("Z2 =", Z2, " A2 =", A2)
print("loss =", round(L, 6))

# ---------- backward ----------
dZ2 = A2 - y
dW2 = A1.T @ dZ2
db2 = dZ2
dA1 = dZ2 @ W2.T
dZ1 = dA1 * (Z1 > 0)
dW1 = x.T @ dZ1
db1 = dZ1

print("\ndZ2 =", dZ2)
print("dW2 =", dW2.ravel())
print("db2 =", db2.ravel())
print("dA1 =", dA1)
print("dZ1 =", dZ1)
print("dW1 =\n", dW1)
print("db1 =", db1)

# ---------- numerical check on W1[0,0] ----------
eps = 1e-6


def loss_now():
    Z1 = x @ W1 + b1
    A1 = np.maximum(0.0, Z1)
    A2 = sigmoid(A1 @ W2 + b2)
    return float(-(y * np.log(A2) + (1 - y) * np.log(1 - A2))[0, 0])


orig = W1[0, 0]
W1[0, 0] = orig + eps; Lp = loss_now()
W1[0, 0] = orig - eps; Lm = loss_now()
W1[0, 0] = orig
print("\nnumerical dW1[0,0] =", (Lp - Lm) / (2 * eps))
print("analytic  dW1[0,0] =", dW1[0, 0])
```

Expected output:

```
Z1 = [[2.2  0.15]]  A1 = [[2.2  0.15]]
Z2 = [[2.2]]  A2 = [[0.90025]]
loss = 0.105083

dZ2 = [[-0.09975]]
dW2 = [-0.219451 -0.014963]
db2 = [-0.09975]
dA1 = [[-0.09975   0.199501]]
dZ1 = [[-0.09975   0.199501]]
dW1 =
 [[-0.09975   0.199501]
 [-0.199501  0.399002]]
db1 = [[-0.09975   0.199501]]

numerical dW1[0,0] = -0.09975048908400508
analytic  dW1[0,0] = -0.0997504891196852
```

Every number matches the Worked Example. The numerical and analytic gradients agree to eight decimal places.

---

### Step 2 — Build the full NumPy Brain

Create `numpy_brain.py`. This is your mini-project's engine.

```python
"""A 2-layer MLP in pure NumPy: forward, backprop, gradient check, training."""
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def relu(z):
    return np.maximum(0.0, z)


def sigmoid(z):
    """Stable logistic, same trick as Module 4."""
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def init_params(n_in, n_hidden, seed=0):
    """He initialization: std = sqrt(2 / fan_in). Biases start at zero."""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, np.sqrt(2.0 / n_in), size=(n_in, n_hidden)),
        "b1": np.zeros((1, n_hidden)),
        "W2": rng.normal(0, np.sqrt(2.0 / n_hidden), size=(n_hidden, 1)),
        "b2": np.zeros((1, 1)),
    }


def forward(P, X):
    Z1 = X @ P["W1"] + P["b1"]
    A1 = relu(Z1)
    Z2 = A1 @ P["W2"] + P["b2"]
    A2 = sigmoid(Z2)
    return {"Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2}


def loss_fn(A2, y, eps=1e-12):
    p = np.clip(A2, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def backward(P, cache, X, y):
    n = X.shape[0]
    dZ2 = (cache["A2"] - y) / n            # divide once, here, for the mean
    dW2 = cache["A1"].T @ dZ2
    db2 = dZ2.sum(axis=0, keepdims=True)
    dA1 = dZ2 @ P["W2"].T
    dZ1 = dA1 * (cache["Z1"] > 0)          # the ReLU valve, in reverse
    dW1 = X.T @ dZ1
    db1 = dZ1.sum(axis=0, keepdims=True)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


def gradient_check(P, X, y, eps=1e-6, seed=0):
    """Worst relative error over 20 random entries of each parameter array."""
    grads = backward(P, forward(P, X), X, y)
    rng = np.random.default_rng(seed)
    worst = 0.0
    for name in ["W1", "b1", "W2", "b2"]:
        A = P[name]
        for _ in range(20):
            idx = tuple(rng.integers(0, s) for s in A.shape)
            orig = A[idx]
            A[idx] = orig + eps
            lp = loss_fn(forward(P, X)["A2"], y)
            A[idx] = orig - eps
            lm = loss_fn(forward(P, X)["A2"], y)
            A[idx] = orig                    # ALWAYS restore
            num = (lp - lm) / (2 * eps)
            ana = grads[name][idx]
            denom = max(1e-12, abs(num) + abs(ana))
            worst = max(worst, abs(num - ana) / denom)
    return worst


def train(P, X, y, lr=0.5, epochs=3000, Xv=None, yv=None, log_every=500):
    hist = []
    for e in range(epochs + 1):
        cache = forward(P, X)
        L = loss_fn(cache["A2"], y)
        hist.append(L)
        if e % log_every == 0:
            msg = f"epoch {e:>5}  train loss {L:.4f}"
            if Xv is not None:
                cv = forward(P, Xv)
                acc = float(((cv["A2"] >= 0.5).astype(int) == yv).mean())
                msg += f"  val loss {loss_fn(cv['A2'], yv):.4f}  val acc {acc:.4f}"
            print(msg)
        if e == epochs:
            break
        g = backward(P, cache, X, y)
        for k in P:
            P[k] -= lr * g[k]
    return hist


if __name__ == "__main__":
    X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
    y = y.reshape(-1, 1).astype(float)          # shape (n, 1), not (n,)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                          stratify=y, random_state=42)
    sc = StandardScaler().fit(Xtr)
    Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)

    P = init_params(2, 16, seed=0)
    print("gradient check (relative error):",
          f"{gradient_check(P, Xtr[:20], ytr[:20]):.3e}")
    print()
    train(P, Xtr, ytr, lr=0.5, epochs=3000, Xv=Xte, yv=yte, log_every=500)
    acc = float(((forward(P, Xte)["A2"] >= 0.5).astype(int) == yte).mean())
    print(f"\nfinal test accuracy: {acc:.4f}")

    from sklearn.linear_model import LogisticRegression
    lin = LogisticRegression().fit(Xtr, ytr.ravel())
    print("logistic regression test accuracy:",
          round(float(lin.score(Xte, yte.ravel())), 4))
```

Expected output:

```
gradient check (relative error): 3.651e-08

epoch     0  train loss 0.7967  val loss 0.7977  val acc 0.6200
epoch   500  train loss 0.0883  val loss 0.0535  val acc 0.9920
epoch  1000  train loss 0.0754  val loss 0.0414  val acc 0.9920
epoch  1500  train loss 0.0714  val loss 0.0374  val acc 0.9920
epoch  2000  train loss 0.0692  val loss 0.0352  val acc 0.9920
epoch  2500  train loss 0.0678  val loss 0.0337  val acc 0.9920
epoch  3000  train loss 0.0669  val loss 0.0326  val acc 0.9920

final test accuracy: 0.9920
logistic regression test accuracy: 0.904
```

**Three things to notice.**

1. **Gradient check: 3.651e-08.** Well under `1e-6`. Your backprop derivation is verified, not hoped for.
2. **99.2% versus 90.4%.** The stacked-and-wired version of the same unit gains nearly nine points on data a straight line cannot handle.
3. **Validation loss is *lower* than training loss** (0.0326 vs 0.0669). That looks backwards, and here it is fine — `make_moons` scatters noise randomly, and this particular 250-row test split happened to get slightly cleaner points. On real data you should be suspicious of that pattern and go hunting for leakage (Module 2).

---

### Step 3 — Plot the curved decision boundary

Create `plot_boundary.py`:

```python
import numpy as np
import matplotlib
matplotlib.use("Agg")               # write to a file, no window needed
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from numpy_brain import init_params, forward, train

X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
y = y.reshape(-1, 1).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                      stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)

P = init_params(2, 16, seed=0)
train(P, Xtr, ytr, lr=0.5, epochs=3000, log_every=10 ** 9)   # near-silent
lin = LogisticRegression().fit(Xtr, ytr.ravel())

# grid covering the data
pad = 0.6
gx = np.linspace(Xtr[:, 0].min() - pad, Xtr[:, 0].max() + pad, 300)
gy = np.linspace(Xtr[:, 1].min() - pad, Xtr[:, 1].max() + pad, 300)
GX, GY = np.meshgrid(gx, gy)
grid = np.c_[GX.ravel(), GY.ravel()]

mlp_p = forward(P, grid)["A2"].reshape(GX.shape)
lin_p = lin.predict_proba(grid)[:, 1].reshape(GX.shape)

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, probs, title in [(axes[0], lin_p, "Logistic regression — 90.4%"),
                         (axes[1], mlp_p, "2-layer MLP, 16 hidden — 99.2%")]:
    ax.contourf(GX, GY, probs, levels=25, cmap="coolwarm", alpha=0.65)
    ax.contour(GX, GY, probs, levels=[0.5], colors="black", linewidths=2)
    ax.scatter(Xtr[ytr.ravel() == 0, 0], Xtr[ytr.ravel() == 0, 1],
               s=10, c="tab:blue", edgecolor="k", linewidth=0.2, label="class 0")
    ax.scatter(Xtr[ytr.ravel() == 1, 0], Xtr[ytr.ravel() == 1, 1],
               s=10, c="tab:red", edgecolor="k", linewidth=0.2, label="class 1")
    ax.set_title(title)
    ax.set_xlabel("feature 1 (standardised)")
    ax.set_ylabel("feature 2 (standardised)")
    ax.legend(loc="upper right", fontsize=8)

plt.tight_layout()
plt.savefig("boundary.png", dpi=130)
print("wrote boundary.png")
```

Expected: one log line (`epoch 0 train loss 0.7967` — epoch 0 always logs) and then `boundary.png`, two panels. Left is a straight black line slicing diagonally through both crescents, misclassifying the tips. Right is a black line that **bends** — it curls between the two moons, following the gap. That bend is what sixteen ReLU units bought you, and it is the visual proof that stacking works.

If you look closely at the MLP boundary you can see it is made of short straight segments joined at kinks. Each kink is one ReLU unit switching on or off. The network is not drawing a smooth curve; it is drawing a **piecewise-linear** curve out of sixteen hinges. More hidden units, more hinges, smoother-looking curve.

---

### Step 4 — Break it on purpose: initialization and dead ReLUs

Create `break_it.py`:

```python
import io
import contextlib
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from numpy_brain import forward, train

X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
y = y.reshape(-1, 1).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                      stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)


def init_custom(n_in, h, mode, seed=0):
    rng = np.random.default_rng(seed)
    if mode == "zeros":
        W1, W2 = np.zeros((n_in, h)), np.zeros((h, 1))
    elif mode == "tiny":
        W1 = rng.normal(0, 0.0001, (n_in, h)); W2 = rng.normal(0, 0.0001, (h, 1))
    elif mode == "he":
        W1 = rng.normal(0, np.sqrt(2 / n_in), (n_in, h))
        W2 = rng.normal(0, np.sqrt(2 / h), (h, 1))
    elif mode == "huge":
        W1 = rng.normal(0, 50, (n_in, h)); W2 = rng.normal(0, 50, (h, 1))
    return {"W1": W1, "b1": np.zeros((1, h)), "W2": W2, "b2": np.zeros((1, 1))}


def run(P, lr, epochs):
    with contextlib.redirect_stdout(io.StringIO()):
        hist = train(P, Xtr, ytr, lr=lr, epochs=epochs, log_every=10 ** 9)
    A1 = forward(P, Xtr)["A1"]
    dead = int(np.sum(np.all(A1 <= 0, axis=0)))     # never fires on ANY row
    acc = float(((forward(P, Xte)["A2"] >= 0.5).astype(int) == yte).mean())
    return hist[0], hist[-1], acc, dead


print("=== initialization (lr = 0.5, 3000 epochs) ===")
print(f"{'scheme':>8} {'loss@0':>9} {'final':>9} {'test acc':>9} {'dead':>7}")
for mode in ("zeros", "tiny", "he", "huge"):
    s, f, a, d = run(init_custom(2, 16, mode), 0.5, 3000)
    print(f"{mode:>8} {s:>9.4f} {f:>9.4f} {a:>9.4f} {str(d) + '/16':>7}")

print("\n=== dead ReLUs from too-large learning rates (2000 epochs, He init) ===")
print(f"{'lr':>7} {'final':>9} {'test acc':>9} {'dead':>7}")
for lr in (0.5, 5.0, 20.0, 100.0):
    s, f, a, d = run(init_custom(2, 16, "he"), lr, 2000)
    print(f"{lr:>7} {f:>9.4f} {a:>9.4f} {str(d) + '/16':>7}")
```

Expected output:

```
=== initialization (lr = 0.5, 3000 epochs) ===
  scheme    loss@0     final  test acc    dead
   zeros    0.6931    0.6931    0.5000   16/16
    tiny    0.6931    0.3051    0.9040    0/16
      he    0.7967    0.0669    0.9920    0/16
    huge   10.3524    0.2843    0.9680    0/16

=== dead ReLUs from too-large learning rates (2000 epochs, He init) ===
     lr     final  test acc    dead
    0.5    0.0692    0.9920    0/16
    5.0    0.0607    0.9880    0/16
   20.0    0.3169    0.8920   10/16
  100.0   13.8155    0.4960   16/16
```

You just caused two classic deep-learning failures on demand and measured both. When someone tells you their network "isn't learning," these two tables are the first things to check.

---

## ✍️ Practice

### [Warm-up] 1 — One neuron, three activations

A neuron has `w = [0.4, −0.7, 1.2]` and `b = −0.5`.

(a) For `x = [2, 1, 0.5]`, compute `z` by hand, then `ReLU(z)`, `sigmoid(z)`, and `tanh(z)`.
(b) Do the same for `x = [−1, 2, 0]`.
(c) Which of the three activations gives a *different sign* of information for input (b), and why might that matter downstream?
(d) Verify all six numbers in Python.

**Done looks like:** a 2×4 table (`z`, ReLU, sigmoid, tanh for both inputs) to 6 decimals, matching a Python printout.

---

### [Warm-up] 2 — Forward pass on a new input

Use the Worked Example's network exactly: `W1 = [[0.5, −0.3], [0.8, 0.2]]`, `b1 = [0.1, 0.05]`, `W2 = [[1.0], [−2.0]]`, `b2 = [0.3]`.

New example: `x = [2.0, −1.0]`, true label `y = 0`.

(a) Compute `Z1`, `A1`, `Z2`, `A2`, and the loss, showing each multiplication.
(b) One hidden unit does not fire. Which one, and what is its `A1` value?
(c) State what the network predicts and whether it is right at a 0.5 threshold.

**Done looks like:** all five quantities to 6 decimals, plus the answers to (b) and (c).

---

### [Build] 3 — Backprop on that new input, verified numerically

Continue from exercise 2.

(a) Compute `dZ2`, `dW2`, `db2`, `dA1`, `dZ1`, `dW1`, `db1` by hand.
(b) Two entries of `dW1` are exactly zero. Explain why in one sentence — do not just say "because the mask."
(c) Verify `dW1[0][0]`, `dW1[1][0]`, `dW1[0][1]`, `dW2[0][0]`, and `dW2[1][0]` with a numerical gradient at `ε = 1e-6`. Report each pair.
(d) Take one step with `lr = 0.5` and confirm the loss decreased.

**Done looks like:** all seven gradient arrays, five numeric/analytic pairs agreeing to at least 6 significant figures, and two loss values with the second smaller.

---

### [Build] 4 — Capacity sweep

Using `numpy_brain.py` on `make_moons(n_samples=1000, noise=0.20, random_state=42)`:

(a) Train with `n_hidden ∈ {1, 2, 4, 8, 16, 64}`, `lr = 0.5`, 3000 epochs, seed 0. Report final training loss and test accuracy for each.
(b) Two of those settings give exactly the same test accuracy as plain `LogisticRegression`. Which, and why?
(c) Identify the smallest `n_hidden` that reaches at least 99% test accuracy.
(d) Count the parameters in the 64-unit network and in the 8-unit one. Was the extra capacity worth it here?

**Done looks like:** a six-row table, a stated minimum sufficient width, and two parameter counts with a one-sentence verdict.

---

### [Stretch] 5 — Add a second hidden layer

Extend the network to `2 → 16 → 8 → 1`, with ReLU on both hidden layers.

(a) Write down the forward pass and the backward pass for the three-layer version. You need two new lines in `backward`.
(b) Implement `init3`, `forward3`, `backward3`, and extend `gradient_check` to cover all six parameter arrays.
(c) Run the gradient check. It must come in below `1e-6`.
(d) Train for 3000 epochs at `lr = 0.5` and compare test accuracy to the 2-layer version. Comment honestly on whether depth helped on this problem.

**Done looks like:** a passing gradient check on all six arrays, a test accuracy number, and an honest one-paragraph comparison.

---

### [Stretch] 6 — Softmax for three classes

Rebuild the network for multi-class output: `2 → 16 → 3`, ReLU hidden, **softmax** output, categorical cross-entropy loss.

(a) Implement a numerically stable softmax (subtract the row max before exponentiating — explain in one line why that is safe).
(b) One-hot encode the labels and implement the loss `L = −(1/n)·Σ_i Σ_k y_ik · ln p_ik`.
(c) Show that the output gradient is still `dZ2 = (A2 − Y)/n`, and confirm with a gradient check below `1e-6`.
(d) Train on `make_blobs(n_samples=900, centers=3, cluster_std=1.8, random_state=3)` (standardised, 75/25 stratified split, `lr = 0.5`, 2000 epochs) and report test accuracy. Print one test row's three probabilities and confirm they sum to 1.

**Done looks like:** a passing gradient check, a test accuracy, and one probability triple that sums to 1.000000.

---

## 🤔 Think Deeper

**1. Your MLP got 99.2% on `make_moons`. But `make_moons` is a synthetic dataset generated by a formula you could write down in three lines. Does a great score on it tell you anything at all about whether your network will work on real data?**

*How to reason about it:* separate two claims — "my backprop implementation is correct" and "neural networks are good at this class of problem." Ask which of those a synthetic benchmark can actually test. Then think about what real data has that `make_moons` does not: missing values, categorical columns, label noise that isn't uniform, a distribution that shifts over time, and features that are correlated with each other in structured ways. Which of those would break your code, and which would break your *model*?

**2. A hospital deploys a 3-layer network that predicts sepsis risk. A doctor asks: "why did it flag this patient?" You can print all 449 weights. Is that an answer?**

*How to reason about it:* try writing out what a single weight actually means in a network with a hidden layer — `W1[3][7] = 0.42` is the influence of feature 3 on hidden unit 7, but hidden unit 7 has no name and no meaning anyone agreed on. Compare that with logistic regression, where a weight of 0.42 on "heart rate" is a sentence in English. Then ask a harder question: if the network is more accurate but unexplainable and the logistic regression is less accurate but explainable, who should get to choose, and does the answer change between "which film to recommend" and "which patient to escalate"?

**3. The dead-ReLU experiment showed 10 of 16 units permanently switched off, and the network still got 89.2%. Suppose a model in production quietly loses half its units this way after a bad training run. What would tell you?**

*How to reason about it:* list the things you would normally monitor — accuracy, loss, latency — and ask whether any of them would flag a network running at reduced capacity but still roughly working. Then think about what *would* catch it: a count of dead units logged at the end of every training run, a comparison of this run's final loss against the last ten runs, a held-out canary set. This is the kind of check that belongs in the model card and monitoring plan you will write at the end of this level.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ValueError: matmul: Input operand 1 has a mismatch` | Weight matrix built as `(n_hidden, n_in)` instead of `(n_in, n_hidden)` | Write the shapes as a comment above every layer and read them left to right: `(n, 2) @ (2, 16) -> (n, 16)` |
| Loss stuck at exactly 0.6931 forever | Weights initialised to zeros — no symmetry breaking, and with ReLU no gradient at all | Use He init: `rng.normal(0, sqrt(2/n_in), (n_in, n_hidden))` |
| Network gets exactly the logistic-regression accuracy, no better | Either no activation between layers (two linear layers collapse to one) or initial weights so tiny the units never differentiate | Confirm `relu` is actually applied to `Z1`; check `P["W1"].std()` is around `sqrt(2/n_in)`, not `1e-4` |
| Gradient check gives ~0.5 relative error on `b1` or `b2` | Forgot `keepdims=True` on the bias sum, so the shape collapsed and broadcasting silently did the wrong thing | `db1 = dZ1.sum(axis=0, keepdims=True)` |
| Gradient check gives errors around `1e-3`, not `1e-6` | `ε` too small (floating-point cancellation) or too large (the one-sided approximation error dominates) | Use `ε = 1e-6` with a **two-sided** difference `(L₊ − L₋)/(2ε)`, and float64 throughout |
| Gradient check passes but training does nothing afterwards | The check perturbed a weight and forgot to restore it, corrupting the model | Always restore with `A[idx] = orig` in the same block, before the next iteration |
| Gradients are `n` times too big; loss explodes | Forgot to divide by the batch size — `dZ2 = A2 − y` instead of `(A2 − y)/n` | Divide once at the top of `backward` and let it flow through everything downstream |
| Labels shaped `(n,)` cause silent garbage | `A2` is `(n, 1)`, so `A2 - y` broadcasts to `(n, n)` and NumPy raises no error | Always `y = y.reshape(-1, 1)` and assert `A2.shape == y.shape` |
| Half the hidden units are dead after training | Learning rate too large; one oversized step drove biases far negative | Lower `lr`, and log `np.sum(np.all(A1 <= 0, axis=0))` at the end of every run |

---

## 🛠️ Mini-Project — NumPy Brain

**Goal.** A 2-layer MLP in pure NumPy that learns `make_moons` to >90% test accuracy, with a numerical gradient check that agrees with your analytic gradients to `1e-6`, and a plotted decision boundary that visibly curves.

**Time.** 90 minutes.

### Starter steps

1. **Data.** `make_moons(n_samples=1000, noise=0.20, random_state=42)`. Reshape `y` to `(n, 1)`. Split 75/25 stratified with `random_state=42`. `StandardScaler` fit on **train only**.

2. **Parameters.** Write `init_params(n_in, n_hidden, seed)` using He initialization for both weight matrices and zeros for both biases. Store them in a dict so you can loop over them in the update step.

3. **Forward.** Write `forward(P, X)` returning a cache dict with `Z1`, `A1`, `Z2`, `A2`. Above each line, write the shape as a comment.

4. **Loss.** Write `loss_fn(A2, y)` with clipping. Verify that a freshly initialised network gives a loss somewhere near `ln 2 = 0.693` (He init on this data gives 0.7967 — close, and the small excess is real).

5. **Backward.** Write `backward(P, cache, X, y)` returning a dict with the same four keys as `P`. Derive each of the seven lines yourself before you look back at the Concept section.

6. **Gradient check — the gate.** Write `gradient_check` that perturbs 20 random entries of each of the four arrays with `ε = 1e-6` and returns the worst relative error `|num − ana| / (|num| + |ana|)`. Run it on 20 rows **before you train anything**. If it is above `1e-6`, stop and fix backprop. Do not train a network whose gradients you have not verified.

7. **Train.** Full-batch, `lr = 0.5`, 3000 epochs, printing train loss, validation loss, and validation accuracy every 500 epochs.

8. **Compare.** Fit `LogisticRegression` on the identical arrays and print both test accuracies side by side.

9. **Plot.** Produce `boundary.png` with two panels — logistic regression's straight boundary and your MLP's curved one — over a 300×300 probability grid, with the 0.5 contour drawn in black.

10. **Report.** Five lines: gradient-check value, MLP test accuracy, logistic regression test accuracy, number of hidden units, and one sentence on what the boundary looks like.

### Success criteria checklist

- [ ] Gradient check prints a relative error **below 1e-6** (you should see roughly `3.7e-08`), and it is run *before* training.
- [ ] All four parameter arrays are covered by the check, not just `W1`.
- [ ] Test accuracy is **above 90%** (you should see about 99.2%).
- [ ] Your MLP beats `LogisticRegression` on the same split by at least 5 percentage points.
- [ ] `boundary.png` exists, has two labelled panels, and the MLP's 0.5 contour is **visibly non-linear** — not a straight line.
- [ ] `backward()` contains no calls to any autodiff library. Every gradient is one you derived.
- [ ] The scaler is fit on the training split only.
- [ ] You print the number of dead hidden units at the end of training, and it is 0.

### Level it up

Make the hidden layer's job visible. Add a third panel to your figure showing, for four individual hidden units, the region of input space where that unit is **on** (`Z1[:, j] > 0`) — draw its boundary line, which is exactly `W1[0,j]·x₀ + W1[1,j]·x₁ + b1[j] = 0`.

You will see that each hidden unit contributes one straight hinge line, and the final curved boundary is assembled from those hinges. Then answer with evidence: **how many of the 16 hinge lines actually pass through the region where the data lives?** Units whose hinge sits far outside the data are effectively constant and are wasted capacity. Report the count, and connect it to your capacity-sweep result from Practice 4.

---

## 🔑 Key Takeaways

- **A neuron is logistic regression with a swappable squash**: weighted sum, plus bias, through an activation. A network is those units stacked in layers and wired together.
- **The activation function is what makes depth mean anything.** Two linear layers with no activation between them collapse algebraically into one linear layer — you would have an expensive straight line.
- **The forward pass is two matrix multiplies.** `Z1 = X@W1 + b1`, `A1 = ReLU(Z1)`, `Z2 = A1@W2 + b2`, `A2 = σ(Z2)`. Most bugs are shape bugs; write the shapes down.
- **Backprop is the chain rule applied backwards, and it is five rules**: `dZ2 = A2 − y`, `dW = A.T @ dZ`, `db = dZ.sum(axis=0)`, `dA_prev = dZ @ W.T`, `dZ = dA * (Z > 0)`. Everything else is bookkeeping.
- **Always gradient-check before you train.** Two-sided nudge at `ε = 1e-6`, relative error below `1e-6`. It converts hope into verification and costs you five minutes.
- **Initialization decides whether learning happens at all.** Zeros gives you a dead network at exactly `ln 2`. Tiny gives you a disguised linear model. He initialization — `std = sqrt(2/n_in)` — works.
- **Dead ReLUs are a real, measurable failure.** A too-large learning rate killed 10 of 16 units and cost 10 accuracy points. Count them at the end of every run.
- **Capacity has a ceiling.** 1 or 2 hidden units matched logistic regression exactly; 8 units hit 99.2%; 64 units added nothing but parameters.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Neuron / unit** | Multiplies its inputs by weights, adds a bias, squashes the result | `a = ReLU(0.4x₁ − 0.7x₂ − 0.5)` |
| **Activation function** | The squash at the end of a neuron; what makes stacking useful | ReLU, sigmoid, tanh, softmax |
| **Pre-activation (`z`)** | The weighted sum *before* the squash | `z = 2.20` |
| **Activation (`a`)** | The neuron's output, after the squash | `a = ReLU(2.20) = 2.20` |
| **Layer** | A row of neurons that all see the same inputs | 16 hidden units |
| **Hidden layer** | A layer whose outputs you never read directly | The 16 units between input and output |
| **MLP** | Multi-layer perceptron: fully connected layers stacked | `2 → 16 → 1` |
| **ReLU** | `max(0, z)`. A one-way valve. The default hidden activation | `ReLU(−2.3) = 0` |
| **Softmax** | Turns several raw scores into probabilities that sum to 1 | `[2, 1, 0.1] → [0.659, 0.242, 0.099]` |
| **Dead ReLU** | A unit that is negative for every row, so it never fires and never learns | 10 of 16 units after `lr = 20` |
| **Vanishing gradient** | Gradients shrinking toward zero as they pass back through many saturating layers | `0.25⁵ ≈ 0.001` |
| **Chain rule** | Slopes multiply along a path: `dc/da = (dc/db)(db/da)` | rain → traffic → arrival time |
| **Backpropagation** | Using the chain rule backwards to get every weight's gradient in one sweep | Five lines of NumPy |
| **Gradient check** | Nudging a weight and dividing, to verify your calculus | `(L₊ − L₋)/(2ε)` |
| **Relative error** | `|a − b| / (|a| + |b|)`. Fair comparison regardless of scale | `3.7e-08` — passes |
| **He initialization** | Random weights with `std = sqrt(2/n_in)`; the ReLU default | `std = sqrt(2/2) = 1.0` for the first layer |
| **Symmetry breaking** | Making units start different so they learn different things | Random init instead of zeros |
| **Broadcasting** | NumPy copying a small array across a bigger one automatically | `(n,16) + (1,16)` |
| **Piecewise-linear** | A curve built out of straight segments joined at kinks | The MLP's boundary; one kink per ReLU |
| **Capacity** | How complicated a shape a model can represent | 1 hidden unit ≈ a line; 16 ≈ a curve |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — One neuron, three activations

**(a) `x = [2, 1, 0.5]`:**

```
z = (0.4)(2) + (−0.7)(1) + (1.2)(0.5) + (−0.5)
  = 0.8 − 0.7 + 0.6 − 0.5
  = 0.200000

ReLU(0.2)    = max(0, 0.2)                    = 0.200000
sigmoid(0.2) = 1 / (1 + e^(−0.2))
             = 1 / (1 + 0.818731) = 1/1.818731 = 0.549834
tanh(0.2)    = (e^0.2 − e^(−0.2)) / (e^0.2 + e^(−0.2))
             = (1.221403 − 0.818731) / (1.221403 + 0.818731)
             = 0.402672 / 2.040134                = 0.197375
```

**(b) `x = [−1, 2, 0]`:**

```
z = (0.4)(−1) + (−0.7)(2) + (1.2)(0) + (−0.5)
  = −0.4 − 1.4 + 0 − 0.5
  = −2.300000

ReLU(−2.3)    = max(0, −2.3)   = 0.000000
sigmoid(−2.3) = e^(−2.3)/(1 + e^(−2.3)) = 0.100259/1.100259 = 0.091123
tanh(−2.3)    = −0.980096
```

**Summary table:**

| input | `z` | ReLU | sigmoid | tanh |
|---|---|---|---|---|
| `[2, 1, 0.5]` | 0.200000 | 0.200000 | 0.549834 | 0.197375 |
| `[−1, 2, 0]` | −2.300000 | 0.000000 | 0.091123 | −0.980096 |

**(c)** Only **tanh** returns a negative number (−0.980096) for input (b). ReLU returns exactly 0 and sigmoid returns a small positive 0.091. That matters downstream because tanh can send a *negative* signal to the next layer — "strongly not this" — whereas ReLU can only send "nothing" and sigmoid can only send "a little bit of yes." A tanh unit is zero-centred, so the next layer's weighted sums stay balanced around zero; a layer of ReLUs feeds only non-negative values forward, which biases the next layer's pre-activations positive. (That is one of the reasons tanh was popular before ReLU's speed and non-vanishing gradient won out.)

**(d) Verification:**

```python
import numpy as np
w, b = np.array([0.4, -0.7, 1.2]), -0.5
for x in ([2, 1, 0.5], [-1, 2, 0]):
    z = float(np.dot(w, x) + b)
    print(f"x={x}  z={z:.6f}  relu={max(0.0, z):.6f}  "
          f"sig={1/(1+np.exp(-z)):.6f}  tanh={np.tanh(z):.6f}")
```

```
x=[2, 1, 0.5]  z=0.200000  relu=0.200000  sig=0.549834  tanh=0.197375
x=[-1, 2, 0]  z=-2.300000  relu=0.000000  sig=0.091123  tanh=-0.980096
```

---

### 2 — Forward pass on a new input

`x = [2.0, −1.0]`, `y = 0`.

**(a)**

```
Hidden unit 1:  z₁ = (2.0)(0.5) + (−1.0)(0.8) + 0.1
                   = 1.0 − 0.8 + 0.1
                   = 0.300000

Hidden unit 2:  z₂ = (2.0)(−0.3) + (−1.0)(0.2) + 0.05
                   = −0.6 − 0.2 + 0.05
                   = −0.750000

Z1 = [ 0.300000 , −0.750000 ]
A1 = [ max(0, 0.3) , max(0, −0.75) ] = [ 0.300000 , 0.000000 ]

Z2 = (0.300000)(1.0) + (0.000000)(−2.0) + 0.3
   = 0.3 + 0 + 0.3
   = 0.600000

A2 = σ(0.6) = 1 / (1 + e^(−0.6)) = 1 / (1 + 0.548812) = 1/1.548812 = 0.645656

y = 0, so  L = −ln(1 − 0.645656) = −ln(0.354344) = 1.037488
```

**(b)** **Hidden unit 2** does not fire. Its pre-activation is `z₂ = −0.750000`, and `ReLU(−0.75) = 0`, so `A1[1] = 0.000000`. Its weight into the output (`−2.0`) is therefore multiplied by zero and contributes nothing to `Z2` on this example.

**(c)** The network predicts **p = 0.645656**, which is `≥ 0.5`, so it predicts **class 1**. The true label is **0**, so this prediction is **wrong** — which is why the loss (1.037) is so much larger than the Worked Example's (0.105).

---

### 3 — Backprop on that new input, verified numerically

**(a)**

```
dZ2 = A2 − y = 0.645656 − 0 = 0.645656          (positive: shrink Z2)

dW2 = A1.T @ dZ2
    = [ 0.300000 ; 0.000000 ] × 0.645656
    = [ 0.193697 ; 0.000000 ]

db2 = dZ2 = 0.645656

dA1 = dZ2 @ W2.T
    = 0.645656 × [ 1.0 , −2.0 ]
    = [ 0.645656 , −1.291313 ]

mask = (Z1 > 0) = (  [0.30, −0.75] > 0  ) = [ 1 , 0 ]

dZ1 = dA1 * mask = [ 0.645656 × 1 , −1.291313 × 0 ]
                 = [ 0.645656 , 0.000000 ]

dW1 = x.T @ dZ1 = outer([2.0, −1.0], [0.645656, 0.000000])
    = [  1.291313    0.000000 ]
      [ −0.645656    0.000000 ]

db1 = dZ1 = [ 0.645656 , 0.000000 ]
```

**(b) Why `dW1[0][1]` and `dW1[1][1]` are exactly zero.**

Those two entries are the weights *into hidden unit 2*. On this example, hidden unit 2's pre-activation was −0.75, so ReLU clamped its output to 0 and it contributed nothing to `Z2`. Nudging either of those weights by a hair would change `z₂` from −0.75 to −0.749999 — still negative, still clamped to 0, so `A1[1]` stays exactly 0, `Z2` is unchanged, and the loss is unchanged. A weight that provably cannot change the loss has a derivative of exactly zero. (This is the flat left half of ReLU, and it is also the mechanism behind dead units: if *every* row does this, the weight never moves again.)

**(c) Numerical verification at `ε = 1e-6`:**

| Entry | Analytic | Numerical | Agrees? |
|---|---|---|---|
| `dW1[0][0]` | 1.291313 | 1.2913126123947904 | ✅ |
| `dW1[1][0]` | −0.645656 | −0.6456563061973952 | ✅ |
| `dW1[0][1]` | 0.000000 | 0.0 | ✅ |
| `dW2[0][0]` | 0.193697 | 0.19369689185921857 | ✅ |
| `dW2[1][0]` | 0.000000 | 0.0 | ✅ |

```python
import numpy as np
sig = lambda z: 1 / (1 + np.exp(-z))
W1 = np.array([[0.5, -0.3], [0.8, 0.2]]); b1 = np.array([[0.1, 0.05]])
W2 = np.array([[1.0], [-2.0]]);           b2 = np.array([[0.3]])
x = np.array([[2.0, -1.0]]);              y = np.array([[0.0]])

def loss_now():
    Z1 = x @ W1 + b1; A1 = np.maximum(0, Z1); A2 = sig(A1 @ W2 + b2)
    return float((-(y * np.log(A2) + (1 - y) * np.log(1 - A2)))[0, 0])

eps = 1e-6
for name, M, idx in [("dW1[0,0]", W1, (0, 0)), ("dW1[1,0]", W1, (1, 0)),
                     ("dW1[0,1]", W1, (0, 1)), ("dW2[0,0]", W2, (0, 0)),
                     ("dW2[1,0]", W2, (1, 0))]:
    o = M[idx]
    M[idx] = o + eps; lp = loss_now()
    M[idx] = o - eps; lm = loss_now()
    M[idx] = o
    print(name, (lp - lm) / (2 * eps))
```

**(d) One step with `lr = 0.5`:**

```
W1 ← [0.5, −0.3; 0.8, 0.2] − 0.5·[1.291313, 0; −0.645656, 0]
   = [ −0.145656   −0.300000 ]
     [  1.122828    0.200000 ]

b1 ← [0.1, 0.05] − 0.5·[0.645656, 0] = [ −0.222828 , 0.050000 ]

W2 ← [1.0; −2.0] − 0.5·[0.193697; 0] = [ 0.903152 ; −2.000000 ]

b2 ← 0.3 − 0.5·(0.645656) = −0.022828

New forward pass:
  z₁ = (2.0)(−0.145656) + (−1.0)(1.122828) + (−0.222828) = −1.636969
  z₂ = (2.0)(−0.300000) + (−1.0)(0.200000) + 0.050000    = −0.750000
  A1 = [0, 0]                       ← both units off on this example now
  Z2 = 0 + 0 + (−0.022828) = −0.022828
  A2 = σ(−0.022828) = 0.494293
  L  = −ln(1 − 0.494294) = −ln(0.505707) = 0.681798
```

**Loss fell from 1.037488 to 0.681798.** ✅ And the prediction flipped from 0.6457 (wrong side) to 0.4943 (correct side of the 0.5 threshold). Note that after this single aggressive step both hidden units are off *for this input* — a real training run averages over hundreds of rows, so no single row can shove the weights around like this.

---

### 4 — Capacity sweep

```python
import io, contextlib
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from numpy_brain import init_params, forward, train

X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
y = y.reshape(-1, 1).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr)
Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)

for h in (1, 2, 4, 8, 16, 64):
    P = init_params(2, h, seed=0)
    with contextlib.redirect_stdout(io.StringIO()):
        hist = train(P, Xtr, ytr, lr=0.5, epochs=3000, log_every=10 ** 9)
    acc = float(((forward(P, Xte)["A2"] >= 0.5).astype(int) == yte).mean())
    print(f"hidden={h:<3} train loss {hist[-1]:.4f}  test acc {acc:.4f}")

print("logreg:", round(float(LogisticRegression()
                            .fit(Xtr, ytr.ravel()).score(Xte, yte.ravel())), 4))
```

**(a)**

```
hidden=1   train loss 0.3052  test acc 0.9040
hidden=2   train loss 0.3052  test acc 0.9040
hidden=4   train loss 0.2558  test acc 0.9440
hidden=8   train loss 0.0695  test acc 0.9920
hidden=16  train loss 0.0669  test acc 0.9920
hidden=64  train loss 0.0645  test acc 0.9920
logreg: 0.904
```

**(b)** `n_hidden = 1` and `n_hidden = 2` both give **0.9040**, exactly `LogisticRegression`'s score.

For `n_hidden = 1`: the network is `p = σ(w₂·ReLU(w₁·x + b₁) + b₂)`. Wherever the single unit is on, `ReLU` is the identity, so the whole thing reduces to `σ(w₂w₁·x + w₂b₁ + b₂)` — algebraically a logistic regression with rescaled weights. Wherever the unit is off, the output is a constant. The only shape available is a straight line plus one flat region, which on this data is no better than a straight line.

For `n_hidden = 2`, more capacity exists in principle, but gradient descent from this seed converged to the same 0.3052 loss — the second unit's hinge landed somewhere that added nothing. Two hinges is simply not enough to trace a crescent.

**(c)** The smallest `n_hidden` reaching ≥99% is **8** (0.9920).

**(d) Parameter counts.** For `2 → h → 1`: `W1` is `2h`, `b1` is `h`, `W2` is `h`, `b2` is `1`. Total = `4h + 1`.

```
h = 8  →  4(8) + 1  = 33 parameters   → 0.9920
h = 64 →  4(64) + 1 = 257 parameters  → 0.9920
```

**Verdict:** the extra capacity was not worth it. 257 parameters bought exactly the same test accuracy as 33 — an 8× increase in model size for zero measurable gain, plus more memory, slower training, and more room to overfit on a harder dataset. Pick the smallest architecture that reaches your target, then stop.

---

### 5 — Add a second hidden layer

**(a) Forward and backward for `2 → 16 → 8 → 1`.**

Forward:
```
Z1 = X  @ W1 + b1     A1 = ReLU(Z1)      (n,2)@(2,16) -> (n,16)
Z2 = A1 @ W2 + b2     A2 = ReLU(Z2)      (n,16)@(16,8) -> (n,8)
Z3 = A2 @ W3 + b3     A3 = σ(Z3)         (n,8)@(8,1)  -> (n,1)
```

Backward — the same five rules, applied one extra time:
```
dZ3 = (A3 − y) / n
dW3 = A2.T @ dZ3                 db3 = dZ3.sum(axis=0, keepdims=True)
dZ2 = (dZ3 @ W3.T) * (Z2 > 0)    ← NEW LINE 1
dW2 = A1.T @ dZ2                 db2 = dZ2.sum(axis=0, keepdims=True)
dZ1 = (dZ2 @ W2.T) * (Z1 > 0)    ← NEW LINE 2
dW1 = X.T  @ dZ1                 db1 = dZ1.sum(axis=0, keepdims=True)
```

The pattern is completely mechanical: `dA_prev = dZ @ W.T`, then apply the previous layer's ReLU mask, then `dW = A_prev.T @ dZ`. Twenty layers would be the same two lines twenty times. That mechanical repetition is exactly what PyTorch automates in Module 6.

**(b)+(c)+(d) Implementation:**

```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from numpy_brain import relu, sigmoid, loss_fn


def init3(n_in, h1, h2, seed=0):
    r = np.random.default_rng(seed)
    return {"W1": r.normal(0, np.sqrt(2 / n_in), (n_in, h1)), "b1": np.zeros((1, h1)),
            "W2": r.normal(0, np.sqrt(2 / h1), (h1, h2)),     "b2": np.zeros((1, h2)),
            "W3": r.normal(0, np.sqrt(2 / h2), (h2, 1)),      "b3": np.zeros((1, 1))}


def forward3(P, X):
    Z1 = X @ P["W1"] + P["b1"]; A1 = relu(Z1)
    Z2 = A1 @ P["W2"] + P["b2"]; A2 = relu(Z2)
    Z3 = A2 @ P["W3"] + P["b3"]; A3 = sigmoid(Z3)
    return dict(Z1=Z1, A1=A1, Z2=Z2, A2=A2, Z3=Z3, A3=A3)


def backward3(P, c, X, y):
    n = len(X)
    dZ3 = (c["A3"] - y) / n
    dW3 = c["A2"].T @ dZ3; db3 = dZ3.sum(0, keepdims=True)
    dZ2 = (dZ3 @ P["W3"].T) * (c["Z2"] > 0)
    dW2 = c["A1"].T @ dZ2; db2 = dZ2.sum(0, keepdims=True)
    dZ1 = (dZ2 @ P["W2"].T) * (c["Z1"] > 0)
    dW1 = X.T @ dZ1;       db1 = dZ1.sum(0, keepdims=True)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2, "W3": dW3, "b3": db3}


def gcheck(P, fwd, lossf, bwd, X, y, keys, eps=1e-6, seed=0):
    g = bwd(P, fwd(P, X), X, y)
    r = np.random.default_rng(seed)
    worst = 0.0
    for k in keys:
        A = P[k]
        for _ in range(20):
            i = tuple(r.integers(0, s) for s in A.shape)
            o = A[i]
            A[i] = o + eps; lp = lossf(fwd(P, X), y)
            A[i] = o - eps; lm = lossf(fwd(P, X), y)
            A[i] = o
            num = (lp - lm) / (2 * eps)
            worst = max(worst, abs(num - g[k][i]) / max(1e-12, abs(num) + abs(g[k][i])))
    return worst


X, y = make_moons(n_samples=1000, noise=0.20, random_state=42)
y = y.reshape(-1, 1).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)

P = init3(2, 16, 8, seed=0)
keys = ["W1", "b1", "W2", "b2", "W3", "b3"]
print("gradient check:", f"{gcheck(P, forward3, lambda c, y: loss_fn(c['A3'], y), backward3, Xtr[:20], ytr[:20], keys):.3e}")

for _ in range(3001):
    g = backward3(P, forward3(P, Xtr), Xtr, ytr)
    for k in P:
        P[k] -= 0.5 * g[k]

print("train loss", round(loss_fn(forward3(P, Xtr)["A3"], ytr), 4))
print("test acc  ", round(float(((forward3(P, Xte)["A3"] >= 0.5).astype(int) == yte).mean()), 4))
```

Output:

```
gradient check: 7.107e-08
train loss 0.0607
test acc   0.988
```

**(c)** `7.107e-08` — comfortably below `1e-6`. ✅ All six arrays checked.

**(d) Honest comparison.**

| Model | Parameters | Train loss | Test accuracy |
|---|---|---|---|
| 2 → 16 → 1 | 65 | 0.0669 | **0.9920** |
| 2 → 16 → 8 → 1 | 193 | 0.0607 | 0.9880 |

Depth **did not help**. The deeper network reached a slightly lower *training* loss (0.0607 vs 0.0669) but a slightly *worse* test accuracy (98.8% vs 99.2%) with three times the parameters. That gap — better on train, worse on test — is the signature of mild overfitting, and it is exactly what you should expect when you add capacity to a problem that already had enough.

This is a useful and slightly deflating result to sit with. `make_moons` is a two-dimensional problem whose boundary is one smooth curve; sixteen hinges cover it completely. Depth pays off when the function you are learning is *compositional* — edges make textures make parts make objects — which is the situation in Module 7's image data, not here. Adding layers because "deep is better" is cargo cult; add them when the problem has structure that layers can mirror.

---

### 6 — Softmax for three classes

**(a) Stable softmax.**

```python
def softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)     # shift each row
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)
```

**Why subtracting the row max is safe:** softmax is `e^(z_k) / Σ e^(z_j)`. Subtract a constant `c` from every entry in the row and you get `e^(z_k − c) / Σ e^(z_j − c) = (e^(−c)·e^(z_k)) / (e^(−c)·Σ e^(z_j))` — the `e^(−c)` cancels top and bottom, so the result is mathematically identical. Choosing `c = max(z)` makes the largest exponent exactly `e^0 = 1`, so nothing can overflow.

**(b) One-hot labels and categorical cross-entropy.**

```python
Y = np.eye(3)[y_train]        # (n, 3): row i is 1 in column y_train[i]

def loss_s(c, Y, eps=1e-12):
    return float(-np.mean(np.sum(Y * np.log(np.clip(c["A2"], eps, 1)), axis=1)))
```

Because `Y` is one-hot, `Σ_k y_ik·ln p_ik` picks out exactly the log-probability the model assigned to the *correct* class. Binary log loss is this formula with `k = 2`.

**(c) Why `dZ2 = (A2 − Y)/n`.**

For row `i` with true class `t`, `L_i = −ln p_t`. Differentiating softmax-plus-cross-entropy with respect to `z_k`:

```
∂L_i/∂z_k = p_k − y_k          (y_k is 1 if k == t, else 0)
```

The softmax Jacobian (`∂p_k/∂z_j = p_k(δ_kj − p_j)`) collapses against the `1/p_t` from the log, in exactly the same way the sigmoid's `p(1−p)` cancelled in Module 4. Divide by `n` for the mean and you get `dZ2 = (A2 − Y)/n`. **Nothing else in `backward` changes.**

**(d) Full implementation and results:**

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from numpy_brain import relu


def softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)


def init_s(n_in, h, k, seed=0):
    r = np.random.default_rng(seed)
    return {"W1": r.normal(0, np.sqrt(2 / n_in), (n_in, h)), "b1": np.zeros((1, h)),
            "W2": r.normal(0, np.sqrt(2 / h), (h, k)),       "b2": np.zeros((1, k))}


def fwd_s(P, X):
    Z1 = X @ P["W1"] + P["b1"]; A1 = relu(Z1)
    Z2 = A1 @ P["W2"] + P["b2"]; A2 = softmax(Z2)
    return dict(Z1=Z1, A1=A1, Z2=Z2, A2=A2)


def loss_s(c, Y, eps=1e-12):
    return float(-np.mean(np.sum(Y * np.log(np.clip(c["A2"], eps, 1)), axis=1)))


def bwd_s(P, c, X, Y):
    n = len(X)
    dZ2 = (c["A2"] - Y) / n
    dW2 = c["A1"].T @ dZ2; db2 = dZ2.sum(0, keepdims=True)
    dZ1 = (dZ2 @ P["W2"].T) * (c["Z1"] > 0)
    return {"W1": X.T @ dZ1, "b1": dZ1.sum(0, keepdims=True), "W2": dW2, "b2": db2}


Xb, yb = make_blobs(n_samples=900, centers=3, cluster_std=1.8, random_state=3)
Xtr, Xte, ytr, yte = train_test_split(Xb, yb, test_size=0.25, stratify=yb, random_state=3)
sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
Y = np.eye(3)[ytr]

P = init_s(2, 16, 3, seed=0)
# (reuse gcheck from exercise 5)
print("gradient check:", f"{gcheck(P, fwd_s, loss_s, bwd_s, Xtr[:20], Y[:20], ['W1','b1','W2','b2']):.3e}")

for _ in range(2001):
    g = bwd_s(P, fwd_s(P, Xtr), Xtr, Y)
    for k in P:
        P[k] -= 0.5 * g[k]

probs = fwd_s(P, Xte)["A2"]
print("train loss", round(loss_s(fwd_s(P, Xtr), Y), 4))
print("test acc  ", round(float((probs.argmax(1) == yte).mean()), 4))
print("row 0 probs", np.round(probs[0], 4), "sum =", round(float(probs[0].sum()), 6))
```

Output:

```
gradient check: 1.689e-07
train loss 0.0859
test acc   0.9333
row 0 probs [0.0012 0.     0.9988] sum = 1.000000
```

Gradient check `1.689e-07` — passes. ✅ Test accuracy **93.33%** on three overlapping blobs (`cluster_std=1.8` makes them genuinely bleed into each other, so ~93% is close to the ceiling). The probability triple sums to exactly 1.000000, as softmax guarantees.

Note that `predict` here is `probs.argmax(axis=1)` — pick the class with the highest probability — rather than a 0.5 threshold. Threshold tuning from Module 3 still applies in the multi-class case, but it becomes a per-class decision rather than a single dial.

</details>

---

[⬅ Previous](module-04-logistic-regression-gradient-descent.md) · [Level 3 Home](README.md) · [Next ➡](module-06-pytorch-deep-learning.md)
