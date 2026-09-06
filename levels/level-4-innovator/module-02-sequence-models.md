# Module 2 — Sequence Models: RNNs, LSTMs, and the Memory Problem

[⬅ Previous](module-01-deep-learning-at-depth.md) · [Level 4 Home](README.md) · [Next ➡](module-03-attention-and-transformers.md)

**Level 4 · Module 2 · ~6 hours · Prereqs: Module 1 (optimizers, gradient clipping, loss-curve diagnostics), PyTorch `nn.Module` and autograd, the chain rule**

---

## 🎯 What You'll Be Able To Do

- **Explain a recurrent cell's hidden state** and unroll a 4-step sequence by hand, writing down every intermediate number.
- **Implement and train a character-level RNN in PyTorch** that generates plausible new names it has never seen.
- **Demonstrate vanishing gradients empirically** — produce a plot showing the learning signal decaying by 12 orders of magnitude over 40 time steps — and explain the exact cause.
- **Describe how LSTM and GRU gates preserve information**, and show numerically that a forget gate near 1 turns a multiplying-to-zero problem into an almost-lossless one.
- **Sample text three ways** — greedy, temperature, and top-k — and predict what each will do before you run it.

---

## 🪝 The Hook

Here are two sentences built from exactly the same words:

> *The dog bit the postman.*
> *The postman bit the dog.*

To a **bag-of-words** model — the kind you built in Level 3, which counts words and throws away their positions — these two sentences are **identical**. Same vector. Same prediction. One of them is a Tuesday; the other is a news story.

So you need a model with memory: something that reads left to right and carries what it has seen so far. That model exists, it is called a recurrent neural network, and for about twenty-five years it was how machines did language.

Then, in this module, you will measure exactly how its memory fails. You will find that the learning signal reaching back 40 steps is about **0.000000000006 times** as strong as the signal reaching back 1 step. That single measurement — that specific, embarrassing number — is why the entire field abandoned recurrence and invented attention. Understanding *this* failure is the only honest way to understand Module 3.

---

## 🧠 The Concept

### 1. Sequences, and what bag-of-words throws away

A **sequence** is *an ordered list of items where the order carries meaning*. Sentences, DNA, stock prices, keystrokes, the moves in a chess game, sensor readings from a phone.

In Level 3 you represented a sentence as a vector of word counts. That is a **bag of words** — *a representation that records which items appeared and how often, but not in what order*.

#### 🍕 Analogy: the ingredients list versus the recipe

A pizza's ingredient list says: flour, water, yeast, tomato, cheese, basil. Two chefs get the same list. Chef A makes a pizza. Chef B puts the cheese in the dough, bakes the basil for forty minutes, and pours water on top at the end. Same ingredients — completely different outcome.

The ingredients are the bag of words. **The recipe is the sequence.**

#### The concrete cost

Take the sentence pair above. Bag-of-words vector over the vocabulary `[the, dog, bit, postman]`:

| Sentence | the | dog | bit | postman |
|---|---|---|---|---|
| The dog bit the postman | 2 | 1 | 1 | 1 |
| The postman bit the dog | 2 | 1 | 1 | 1 |

Identical rows. No classifier on earth can separate them, no matter how deep. The information was destroyed before the model saw it.

How many orderings does a bag of words hide? A 10-word sentence with distinct words has 10! = **3,628,800** possible orderings that all collapse to the same bag. Bag-of-words is a lossy compression that throws away almost everything.

#### What a sequence model must do

Read the items **one at a time, in order**, and maintain a summary of everything read so far. That summary is the whole idea of this module.

---

### 2. The recurrent cell, the hidden state, and unrolling

A **recurrent neural network (RNN)** is *a network with one small function that it applies over and over, once per item in the sequence, passing a summary vector forward each time*.

The summary vector is the **hidden state** — *a fixed-size vector holding everything the network has decided is worth remembering about the sequence so far*.

The core equation, for the simplest ("vanilla" or "Elman") RNN:

```
h_t = tanh( W_xh · x_t  +  W_hh · h_(t-1)  +  b )
y_t = W_hy · h_t
```

Three matrices, one bias, applied identically at every step. That last point matters: **the same weights are reused at every time step.** A 100-step sequence uses the same `W_hh` a hundred times. This is called **weight sharing**, and it is why an RNN can handle sequences of any length with a fixed number of parameters — and, as you will see, it is also the direct cause of its downfall.

#### 🍕 Analogy: reading a book with one sticky note

You are reading a 400-page novel, and you are allowed **one** sticky note. After every page you may rewrite the note however you like, but you can never look back at earlier pages. By page 400 the note is your only memory of pages 1–399.

- The **note** is the hidden state.
- The **rule you use to rewrite it** is the recurrent cell — one fixed procedure, applied identically after every page.
- Whatever fits on the note survives. Everything else is gone forever.

The note has a fixed size. Page 400's details will crowd out page 1's, and you have no way to reach back.

#### Unrolling

**Unrolling** is *drawing the same cell repeated once per time step, so a loop becomes a very deep feed-forward network*.

```
   x₁          x₂          x₃          x₄
    │           │           │           │
    ▼           ▼           ▼           ▼
  ┌────┐      ┌────┐      ┌────┐      ┌────┐
h₀│CELL│──h₁─▶│CELL│──h₂─▶│CELL│──h₃─▶│CELL│──▶ h₄
  └────┘      └────┘      └────┘      └────┘
    │           │           │           │
    ▼           ▼           ▼           ▼
   y₁          y₂          y₃          y₄

    ↑ SAME WEIGHTS in all four boxes ↑
```

This picture is the key insight of the whole module: **an RNN on a 40-step sequence is a 40-layer-deep network whose 40 layers are all the same layer.** Everything Module 1 taught you about deep networks — vanishing gradients, gradient clipping, residual connections — applies here, but harder, because you cannot make the layers different to fix it.

#### Tiny example with real numbers

One hidden unit. `W_xh = 1.0`, `W_hh = 0.5`, `b = 0`, `h₀ = 0`. Feed the sequence `x = [1, 0, 0, 0]` — one spike, then silence. Watch how long the spike is remembered.

| t | x_t | pre-activation = 1.0·x_t + 0.5·h_(t−1) | h_t = tanh(·) |
|---|---|---|---|
| 1 | 1 | 1.0(1) + 0.5(0) = 1.0000 | tanh(1.0000) = **0.7616** |
| 2 | 0 | 1.0(0) + 0.5(0.7616) = 0.3808 | tanh(0.3808) = **0.3634** |
| 3 | 0 | 0.5(0.3634) = 0.1817 | tanh(0.1817) = **0.1797** |
| 4 | 0 | 0.5(0.1797) = 0.0899 | tanh(0.0899) = **0.0896** |

The memory of the spike falls to 12% of its original size in three steps. Extend that: after 10 silent steps it is about `0.5¹⁰ = 0.001`. After 20, about a millionth. **A vanilla RNN's memory has a half-life, and it is short.**

---

### 3. Backpropagation through time, and the two ways gradients die

**Backpropagation through time (BPTT)** is *ordinary backpropagation applied to the unrolled network — the gradient flows backwards from the final loss through every time step, and because the weights are shared, every step's contribution is summed into the same gradient*.

#### Where the trouble comes from

To know how the loss at step 40 depends on the hidden state at step 1, the chain rule makes you multiply 39 Jacobians together:

```
∂L₄₀        ∂L₄₀     ∂h₄₀     ∂h₃₉            ∂h₂
────  =  ──────── · ────── · ────── · ... · ──────
∂h₁         ∂h₄₀     ∂h₃₉     ∂h₃₈            ∂h₁
```

For the vanilla RNN each factor is:

```
∂h_t / ∂h_(t−1)  =  (1 − h_t²) · W_hh
```

Two things multiply together, and both are usually less than 1:

- `(1 − h_t²)` is the derivative of tanh. It is **at most 1** (at `h = 0`) and gets small fast — at `h = 0.9` it is `1 − 0.81 = 0.19`.
- `W_hh` is a weight matrix. What matters is its largest singular value (its "spectral radius"), which standard initialization keeps near or below 1.

Multiply 39 numbers that average, say, 0.5, and you get `0.5³⁹ ≈ 1.8 × 10⁻¹²`.

> **Vanishing gradient** — *the learning signal shrinking towards zero as it propagates backwards through many steps, so early steps receive no useful instruction on how to change.*

> **Exploding gradient** — *the same product growing without bound when the factors exceed 1, producing enormous updates that destroy the model in a single step.*

#### 🍕 Analogy: the compound-interest problem, backwards

A bank account earning **−50% per year** (halving annually) is worth 0.0000000009 of its starting value after 30 years. A bank account earning **+50% per year** is worth 191,751× its starting value after 30 years. The same formula, `rate^n`, gives either annihilation or explosion. **There is no setting where it politely stays the same** — you are always near one cliff or the other. That is exactly the RNN gradient's situation, and 40 time steps is 40 compounding periods.

#### The real measurements you will produce

These are the actual numbers from the script in the Hands-On section, measuring `‖∂L₄₀/∂h_t‖` — how strongly the loss at step 40 depends on the hidden state at step t:

| Cell | t = 40 | t = 20 | t = 1 | ratio t=1 : t=40 |
|---|---|---|---|---|
| RNN (default init) | 5.45e-01 | 6.54e-07 | **3.28e-12** | 6.0 × 10⁻¹² |
| RNN (`W_hh` × 8) | 5.69e-01 | 2.19e+03 | **9.38e+06** | 1.6 × 10⁺⁷ |
| LSTM (default init) | 6.29e-01 | 1.41e-05 | 6.69e-09 | 1.1 × 10⁻⁸ |
| **LSTM (forget bias = +2)** | 6.24e-01 | 2.16e-02 | **1.60e-02** | 2.6 × 10⁻² |
| GRU (default init) | 5.48e-01 | 2.36e-05 | 4.55e-09 | 8.3 × 10⁻⁹ |

Read row 1 and row 2 together. Same architecture. The only difference is that row 2's recurrent weights were multiplied by 8. One vanishes to `3 × 10⁻¹²`; the other explodes to `9 × 10⁶`. Nineteen orders of magnitude apart, from one scaling constant.

Then read row 4. With the forget-gate bias set to +2, the signal at t=1 is only **39× weaker** than at t=40, instead of 2 trillion times weaker. That is the entire point of gates.

#### Gradient clipping handles exactly one of these two problems

From Module 1:

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

This caps explosion. It does **nothing** for vanishing — you cannot un-multiply by 10⁻¹². Clipping is essential for RNNs (they explode constantly) but it is a seatbelt, not an engine. The vanishing side needs an architectural fix, which is the next sub-concept.

---

### 4. LSTM and GRU gates: building a highway for memory

#### The core trick

The vanilla RNN's problem is that the hidden state is *overwritten* at every step: `h_t = tanh(...)` throws away `h_(t−1)` and computes something new from scratch. Memory is destroyed by construction.

The **LSTM (Long Short-Term Memory)** adds a second state vector, the **cell state** `c_t` — *a memory track that is updated by addition rather than by replacement*.

```
c_t = f_t ⊙ c_(t−1)  +  i_t ⊙ g_t
       ↑                  ↑
   keep some of        add some new
   the old memory        information
```

`⊙` is elementwise multiplication. And now look at the derivative:

```
∂c_t / ∂c_(t−1)  =  f_t
```

That is it. No tanh derivative, no weight matrix. Just the forget gate. **If `f_t ≈ 1`, the gradient passes through completely unchanged.**

Compare over 30 steps:

| Path | per-step factor | after 30 steps |
|---|---|---|
| Vanilla RNN | ~0.5 | 0.5³⁰ = **9.3 × 10⁻¹⁰** |
| LSTM, forget gate 0.95 | 0.95 | 0.95³⁰ = **0.215** |
| LSTM, forget gate 0.99 | 0.99 | 0.99³⁰ = **0.740** |

This is the same trick as the residual connection from Module 1 (`x + f(x)` giving a gradient of `1 + f'(x)`), reinvented for time instead of depth. **Addition preserves gradients; repeated multiplication destroys them.** Remember that sentence — it explains ResNets, LSTMs, and transformers all at once.

#### The four gates

A **gate** is *a vector of numbers between 0 and 1, produced by a sigmoid, that multiplies another vector to decide how much of it passes through*. 0 = block completely, 1 = let everything through.

```
f_t = σ(W_f·[x_t, h_(t−1)] + b_f)     forget gate  — how much old memory to keep
i_t = σ(W_i·[x_t, h_(t−1)] + b_i)     input gate   — how much new info to write
g_t = tanh(W_g·[x_t, h_(t−1)] + b_g)  candidate    — WHAT the new info is
o_t = σ(W_o·[x_t, h_(t−1)] + b_o)     output gate  — how much of memory to reveal

c_t = f_t ⊙ c_(t−1) + i_t ⊙ g_t       update the memory track
h_t = o_t ⊙ tanh(c_t)                 the visible hidden state
```

```
             ┌────────────────────────────────────────────┐
  c_(t-1) ───┤  ×f_t  ──────▶ (+) ──────────────────────── ├──▶ c_t
             │                 ▲                     │     │
             │            i_t × g_t                  ▼     │
             │                                    tanh     │
             │                                      │      │
             │                                    × o_t    │
  h_(t-1) ───┤                                      │      ├──▶ h_t
             │  gates computed from [x_t, h_(t-1)]  │      │
  x_t     ───┤──────────────────────────────────────┘      │
             └────────────────────────────────────────────┘
                   the top line is the memory HIGHWAY
```

#### 🍕 Analogy: a whiteboard with a strict protocol

A team keeps a project whiteboard (the cell state). Every hour, three people act on it in order:

- **The Eraser** (`forget gate`) decides, for each region of the board, how much to rub out. Rub out nothing (`f = 1`) and last hour's notes survive perfectly.
- **The Writer** (`candidate` `g_t`) drafts what could be added. **The Editor** (`input gate` `i_t`) decides how much of that draft actually gets written.
- **The Spokesperson** (`output gate` `o_t`) decides how much of the board to read aloud to the rest of the company (that reading-aloud is `h_t`, the visible hidden state).

Crucially the board itself is never wiped and rewritten from scratch — it is selectively erased and selectively added to. That is why something written in hour 1 can still be there in hour 500.

#### Why "forget bias = +2" is a real trick

At initialization all the biases are near 0, so `f_t = σ(0) = 0.5` — the network starts by forgetting half its memory every single step. That is `0.5^T` decay, exactly the vanilla-RNN disease, which is why "LSTM (default init)" in the table above is barely better than the RNN.

Set `b_f = 2` and `f_t = σ(2) = 0.881` at initialization. Set `b_f = 4` and `f_t = σ(4) = 0.982`. The network *starts* in remembering mode and learns to forget only where forgetting helps. This is a standard, cheap, real trick, and you saw its effect in the table: `1.60e-02` versus `6.69e-09`, a factor of two million.

#### GRU: the same idea with fewer parts

The **GRU (Gated Recurrent Unit)** merges the forget and input gates into one **update gate** `z_t` and drops the separate cell state:

```
z_t = σ(...)                              update gate
r_t = σ(...)                              reset gate
h̃_t = tanh(W·[x_t, r_t ⊙ h_(t−1)])       candidate
h_t = (1 − z_t) ⊙ h_(t−1) + z_t ⊙ h̃_t    a weighted blend
```

Note `(1 − z_t)·h_(t−1) + z_t·h̃_t` — an interpolation between "keep the old state" and "take the new one". It is the same additive highway.

| | Vanilla RNN | LSTM | GRU |
|---|---|---|---|
| State vectors | 1 (`h`) | 2 (`h`, `c`) | 1 (`h`) |
| Gates | 0 | 4 | 3 |
| Parameters (hidden size H, input E) | ~H(H+E) | ~4H(H+E) | ~3H(H+E) |
| Long-range memory | poor | good | good |
| Speed | fastest | slowest | middle |
| Use when | teaching, very short sequences | you want the best recurrent result | you want ~LSTM quality, less compute |

---

### 5. Teacher forcing versus autoregressive generation

There is a genuinely confusing asymmetry between how you train a sequence model and how you use it.

#### Training: teacher forcing

**Teacher forcing** is *feeding the model the true previous token at every step during training, regardless of what it actually predicted*.

Training on the name `anika`:

| step | input the model sees | target |
|---|---|---|
| 1 | `<START>` | `a` |
| 2 | `a` (the true one) | `n` |
| 3 | `n` (the true one) | `i` |
| 4 | `i` (the true one) | `k` |
| 5 | `k` (the true one) | `a` |
| 6 | `a` (the true one) | `<EOS>` |

Every step gets the correct history handed to it. Two big wins: the model never spirals off into nonsense during training, and — critically — **all steps can be computed from a single input tensor**, which is what makes batching possible.

#### Inference: autoregressive generation

**Autoregressive generation** is *feeding the model its own previous output back in as the next input, one step at a time*.

```
<START> → model → "d"
"d"     → model → "i"
"i"     → model → "r"
"r"     → model → "a"
"a"     → model → <EOS>          result: "dira"
```

Nobody is checking. If step 2 produces a bad character, step 3 has to keep going from there.

#### 🍕 Analogy: the driving test

**Teacher forcing** is a driving lesson where the instructor has their own steering wheel. Drift towards the kerb and the instructor silently corrects you, so your next decision is always made from a perfectly centred position. You learn a lot, fast.

**Autoregressive generation** is the actual test, alone in the car. Drift towards the kerb and the *next* decision is made from a drifted position, which makes drifting further more likely. Small errors compound.

This gap has a name: **exposure bias** — *the model is only ever trained on perfect histories, but at generation time it must handle its own imperfect ones*. It is why a model can have a beautiful training loss and still produce degenerate repetitive text. Every language model has this problem, including the frontier ones.

#### The mechanical consequence in code

Training and generation use *different code paths*:

```python
# training: one call, whole sequence, fully parallel over the batch
logits, _ = model(inputs)          # inputs is (batch, T) of TRUE tokens

# generation: a Python loop, one token at a time, cannot be parallelized
for _ in range(max_len):
    logits, state = model.step(tok, state)
    tok = sample_from(logits)
```

Note that even in training, the RNN's *time* dimension is still a sequential loop — you cannot compute `h₅` without `h₄`. That sequential dependency is the second reason RNNs lost. Hold that thought for Module 3.

---

### 6. Sampling: greedy, temperature, and top-k

Your model outputs **logits** — *raw, unnormalized scores, one per vocabulary item*. Turning them into an actual character is a design choice with big consequences.

Work with a 4-token vocabulary and these logits: `[2.0, 1.0, 0.5, 0.0]` for tokens `[a, b, c, d]`.

#### Greedy decoding

**Greedy decoding** — *always pick the highest-scoring token*. Here: always `a`.

Deterministic and safe. Also, for a generative model, usually terrible: it produces the same output every time and falls into repetition loops (`the the the the`), because the single most likely next token given "the the" is often "the".

#### Softmax and temperature

**Softmax** converts logits to probabilities: `p_i = exp(z_i) / Σ exp(z_j)`.

**Temperature** — *divide the logits by T before the softmax, to make the distribution flatter (T > 1) or sharper (T < 1)*.

```
p_i = exp(z_i / T) / Σ exp(z_j / T)
```

Let's compute all three columns by hand.

**T = 1.0** (no change): `exp(2.0)=7.389, exp(1.0)=2.718, exp(0.5)=1.649, exp(0.0)=1.000`; sum = 12.756

**T = 0.5** (logits become `[4.0, 2.0, 1.0, 0.0]`): `exp = 54.598, 7.389, 2.718, 1.000`; sum = 65.705

**T = 2.0** (logits become `[1.0, 0.5, 0.25, 0.0]`): `exp = 2.718, 1.649, 1.284, 1.000`; sum = 6.651

| token | logit | p at T=0.5 | p at T=1.0 | p at T=2.0 |
|---|---|---|---|---|
| a | 2.0 | **0.831** | 0.579 | 0.409 |
| b | 1.0 | 0.112 | 0.213 | 0.248 |
| c | 0.5 | 0.041 | 0.129 | 0.193 |
| d | 0.0 | 0.015 | 0.078 | 0.150 |

Read across the rows:

- **Low T sharpens.** At T = 0.5, `a` takes 83% of the probability. As T → 0 this becomes greedy decoding.
- **High T flattens.** At T = 2.0, the worst token `d` has gone from 7.8% to 15%. As T → ∞ every token becomes equally likely and you get pure noise.

#### 🍕 Analogy: the confidence dial

Temperature is a dial from "boring and careful" to "reckless and creative."

- **T = 0.3** — the friend who only ever recommends the restaurant you have been to nine times. Safe. Repetitive.
- **T = 1.0** — the friend who suggests things roughly as often as they actually think they are good ideas.
- **T = 1.5** — the friend who suggests you try the fermented-shark place. Occasionally brilliant. Often a mistake.

The real measurements from this module's name generator, counting how many of 60 sampled names are **not** in the training set:

| Temperature | novel names out of 60 |
|---|---|
| 0.5 | 0 |
| 0.8 | 6 |
| 1.0 | 12 |
| 1.2 | 18 |

At T = 0.5 the model just recites its training data. At T = 1.2 nearly a third of the output is new. Novelty and quality trade off — that is the dial.

#### Top-k sampling

High temperature has a specific failure: it gives real probability to *genuinely terrible* tokens, and one bad character can derail the rest of the name.

**Top-k sampling** — *keep only the k highest-scoring tokens, set the rest to zero probability, renormalize, and sample from what remains*.

With `k = 2` on our example at T = 1.0: keep `a` (7.389) and `b` (2.718), drop `c` and `d`. New sum = 10.107.

- p(a) = 7.389 / 10.107 = **0.731**
- p(b) = 2.718 / 10.107 = **0.269**

You keep randomness (`b` still has a 27% chance) while making `c` and `d` strictly impossible. This is the standard fix: **use temperature for creativity and top-k as a floor on quality**.

There is also **top-p / nucleus sampling** — *keep the smallest set of tokens whose probabilities add to at least p (say 0.9)*. It adapts: when the model is confident, the set is small; when it is unsure, the set is large. You will meet it again when you call real LLM APIs in Module 5.

---

## 🔍 Worked Example

**Task:** unroll both a vanilla RNN and an LSTM for 4 steps by hand, on the input `x = [1, 0, 0, 0]` — one spike then silence — and compare how well each remembers the spike. Every number shown.

Both use a **single hidden unit**, so all the vectors are just numbers. Real models use vectors of size 64–4096; the arithmetic is identical, just elementwise.

### Part A — the vanilla RNN

Weights: `W_xh = 1.0`, `W_hh = 0.5`, `b = 0`. Start `h₀ = 0`.

Rule: `h_t = tanh(1.0·x_t + 0.5·h_(t−1))`

**t = 1:** `pre = 1.0(1) + 0.5(0) = 1.0000`, `h₁ = tanh(1.0000) = 0.7616`
**t = 2:** `pre = 1.0(0) + 0.5(0.7616) = 0.3808`, `h₂ = tanh(0.3808) = 0.3634`
**t = 3:** `pre = 0.5(0.3634) = 0.1817`, `h₃ = tanh(0.1817) = 0.1797`
**t = 4:** `pre = 0.5(0.1797) = 0.0899`, `h₄ = tanh(0.0899) = 0.0896`

| t | h_t | fraction of h₁ remaining |
|---|---|---|
| 1 | 0.7616 | 100% |
| 2 | 0.3634 | 48% |
| 3 | 0.1797 | 24% |
| 4 | 0.0896 | **12%** |

### Part B — the same RNN's gradients

`∂h_t/∂h_(t−1) = (1 − h_t²) · W_hh`

- `∂h₂/∂h₁ = (1 − 0.3634²)(0.5) = (1 − 0.1321)(0.5) = 0.8679 × 0.5 = 0.4340`
- `∂h₃/∂h₂ = (1 − 0.1797²)(0.5) = (1 − 0.0323)(0.5) = 0.9677 × 0.5 = 0.4839`
- `∂h₄/∂h₃ = (1 − 0.0896²)(0.5) = (1 − 0.0080)(0.5) = 0.9920 × 0.5 = 0.4960`

Chain them:

```
∂h₄/∂h₁ = 0.4340 × 0.4839 × 0.4960 = 0.1042
```

Three steps back, the gradient is at **10.4%** of full strength. Extrapolate the per-step factor of ≈ 0.47:

| steps back | gradient fraction |
|---|---|
| 3 | 0.104 |
| 10 | 0.47¹⁰ ≈ 5.2 × 10⁻⁴ |
| 20 | 0.47²⁰ ≈ 2.8 × 10⁻⁷ |
| 40 | 0.47⁴⁰ ≈ 7.5 × 10⁻¹⁴ |

That last number is not far off the `3.28 × 10⁻¹²` the real 96-unit RNN produces in the code. **The toy hand calculation predicts the measured result.**

### Part C — an LSTM on the same input

Now one LSTM unit. To keep the arithmetic readable, weights are chosen so each gate is simple:

| gate | formula | value at x=1 | value at x=0 |
|---|---|---|---|
| forget `f` | σ(0·x + 3.0) | σ(3.0) = 0.9526 | σ(3.0) = 0.9526 |
| input `i` | σ(5·x − 2.5) | σ(2.5) = 0.9241 | σ(−2.5) = 0.0759 |
| candidate `g` | tanh(2·x) | tanh(2) = 0.9640 | tanh(0) = 0.0000 |
| output `o` | σ(0·x + 1.0) | σ(1.0) = 0.7311 | σ(1.0) = 0.7311 |

The forget gate is biased to +3, so it is stuck near "keep everything". Start `c₀ = 0`.

**t = 1** (`x = 1`):
- `c₁ = f·c₀ + i·g = 0.9526(0) + 0.9241(0.9640) = 0 + 0.8908 = ` **0.8908**
- `h₁ = o·tanh(c₁) = 0.7311 × tanh(0.8908) = 0.7311 × 0.7118 = ` **0.5204**

**t = 2** (`x = 0`, so `i = 0.0759` and `g = 0`, meaning `i·g = 0` — nothing new is written):
- `c₂ = 0.9526(0.8908) + 0 = ` **0.8486**
- `h₂ = 0.7311 × tanh(0.8486) = 0.7311 × 0.6904 = ` **0.5047**

**t = 3** (`x = 0`):
- `c₃ = 0.9526(0.8486) = ` **0.8084**
- `h₃ = 0.7311 × tanh(0.8084) = 0.7311 × 0.6687 = ` **0.4888**

**t = 4** (`x = 0`):
- `c₄ = 0.9526(0.8084) = ` **0.7701**
- `h₄ = 0.7311 × tanh(0.7701) = 0.7311 × 0.6470 = ` **0.4730**

### Part D — the comparison that is the whole point

| t | RNN `h_t` | RNN % of t=1 | LSTM `c_t` | LSTM % of t=1 |
|---|---|---|---|---|
| 1 | 0.7616 | 100% | 0.8908 | 100% |
| 2 | 0.3634 | 48% | 0.8486 | 95% |
| 3 | 0.1797 | 24% | 0.8084 | 91% |
| 4 | 0.0896 | **12%** | 0.7701 | **86%** |

And the gradient path:

| | per-step factor | after 4 steps | after 40 steps |
|---|---|---|---|
| RNN: `(1 − h²)·W_hh` | ≈ 0.47 | 0.104 | 7.5 × 10⁻¹⁴ |
| LSTM: `f_t` | 0.9526 | 0.824 | 0.143 |

**After 40 steps the RNN's gradient is 7.5 × 10⁻¹⁴ and the LSTM's is 0.143.** The LSTM's memory path is nearly two trillion times stronger, and the only reason is that its recurrence is `c_t = f·c_(t−1) + something` — addition with a near-1 multiplier — rather than `h_t = tanh(W·h_(t−1) + ...)` — a fresh nonlinear squashing every step.

⚠️ Note what the LSTM did **not** fix: `0.9526⁴⁰ = 0.143` is still decay. Push to 400 steps and `0.9526⁴⁰⁰ ≈ 4 × 10⁻⁹` — vanished again. **The LSTM buys you roughly 100–500 steps of memory, not unlimited memory.** That remaining limit is the gap Module 3 closes, by letting step 400 look directly at step 1 with no intervening multiplications at all.

---

## 💻 Hands-On

### Setup

```bash
pip install torch numpy matplotlib
```

Everything runs on CPU in about 6 seconds. No downloads — the dataset is 231 names typed directly into the file.

### The full script

Save as `name_generator.py`.

```python
"""Module 2 Hands-On — char-level name generator + the vanishing-gradient probe."""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

torch.manual_seed(0)

# ------------------------------------------------------------------ 1. data
NAMES = """
aarav aditi adrian agnes ahmed aiko alina amara amelia anders andrei
anika anita ansel arjun armin arnav asha aslan astrid aurora
bashir beatrix bela bhavya bianca bjorn bodhi bruno cadence caleb
carla carmen cedric celia chandra chitra cira clara colette dagmar
dalia damian daria deepak delia devika dilan divya dmitri dorian
edith eleni elias elina elodie emil enzo esha eshan esme
fabio farah farhan felix fiona flora franka freya gabor gauri
gemma georgi gita greta gustav hana harini harsha havel heidi
helena hugo ilya imran indira ingrid irina iris isolde ivar
jaden jarek jasmin jatin javier jelena jonas joris juno kaia
kalinda karim kasper katya kavya kiran klara koen lakshmi lars
latika leena lena leonie liana linnea lucia lucas magnus maja
malik manav maren marek marisol matteo mila mira nadia nandini
natan nikhil niko nina noor nuria olen olga omkar oorja
orla oskar pablo paloma pavel petra pooja pranav priya quintus
rachna radek rafael rahul rasmus rekha renata rhea rosa rustam
saga sameer sanjay sanna sasha selma senna serge sigrid simone
sofia stefan svea tamara tanvi tarek tatiana thea tibor tomas
torsten trisha uday ujwal ulla ulrich uma vadim valeria varsha
veda vera viggo vikram vilma wanda willem yamini yara yash
ylva yuri zaid zara zenon zoltan zora zuri alma bex
cato dara eero fenna gero hilde ilma jarl kajsa lior
nael oona pim risto suvi timo urho vito wren xanthe
""".split()

PAD, EOS = 0, 1                       # id 0 = padding, id 1 = end-of-name
chars = sorted(set("".join(NAMES)))   # the 26 letters that actually occur
stoi = {c: i + 2 for i, c in enumerate(chars)}   # ids 2..27
itos = {i: c for c, i in stoi.items()}
V = len(stoi) + 2                     # vocabulary size including PAD and EOS
MAXLEN = max(len(n) for n in NAMES) + 1          # +1 leaves room for EOS
TRAIN_SET = set(NAMES)                # used later to measure novelty
print(f"{len(NAMES)} names | vocab {V} | max length with EOS {MAXLEN}")


def encode(name):
    """'aarav' -> [2, 2, 19, 2, 23, 1, 0, 0]  (letters, EOS, then padding)."""
    ids = [stoi[c] for c in name] + [EOS]
    return ids + [PAD] * (MAXLEN - len(ids))


data = torch.tensor([encode(n) for n in NAMES], dtype=torch.long)
# Teacher forcing: input at step t is the TRUE token from step t-1.
inputs = torch.full((len(NAMES), MAXLEN), PAD, dtype=torch.long)
inputs[:, 1:] = data[:, :-1]          # shift right; column 0 stays PAD = <START>
targets = data
print("inputs", tuple(inputs.shape), "targets", tuple(targets.shape))
print("example:", NAMES[0], "->", encode(NAMES[0]))


# --------------------------------------------------------------- 2. model
class CharRNN(nn.Module):
    def __init__(self, vocab, emb=24, hidden=64, cell="lstm", p_drop=0.3):
        super().__init__()
        self.emb = nn.Embedding(vocab, emb)
        self.hidden, self.cell_type = hidden, cell
        if cell == "rnn":
            self.cell = nn.RNNCell(emb, hidden, nonlinearity="tanh")
        elif cell == "gru":
            self.cell = nn.GRUCell(emb, hidden)
        elif cell == "lstm":
            self.cell = nn.LSTMCell(emb, hidden)
        else:
            raise ValueError(cell)
        self.drop = nn.Dropout(p_drop)      # regularization, from Module 1
        self.out = nn.Linear(hidden, vocab)

    def init_state(self, B):
        """LSTM carries (h, c); RNN and GRU carry only h."""
        h = torch.zeros(B, self.hidden)
        return (h, torch.zeros(B, self.hidden)) if self.cell_type == "lstm" else h

    def step(self, tok, state):
        """ONE time step. Used by the generation loop."""
        h_or_pair = self.cell(self.emb(tok), state)
        h = h_or_pair[0] if self.cell_type == "lstm" else h_or_pair
        return self.out(self.drop(h)), h_or_pair

    def forward(self, x, keep_hidden=False):
        """Whole sequence with teacher forcing. keep_hidden is for the probe."""
        B, T = x.shape
        state, logits, kept = self.init_state(B), [], []
        for t in range(T):                       # the unrolled loop
            state = self.cell(self.emb(x[:, t]), state)
            h = state[0] if self.cell_type == "lstm" else state
            if keep_hidden:
                h.retain_grad()                  # so we can read h.grad later
                kept.append(h)
            logits.append(self.out(self.drop(h)))
        return torch.stack(logits, 1), kept      # (B, T, V)


def train(cell="lstm", steps=800, lr=3e-3, wd=0.1, clip=1.0, verbose=True):
    torch.manual_seed(0)
    m = CharRNN(V, cell=cell)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=wd)
    losses = []
    for step in range(steps):
        m.train()
        logits, _ = m(inputs)                                # full batch: 231 names
        loss = F.cross_entropy(logits.reshape(-1, V), targets.reshape(-1),
                               ignore_index=PAD)             # padding must not count
        opt.zero_grad(set_to_none=True)
        loss.backward()
        gn = nn.utils.clip_grad_norm_(m.parameters(), clip)  # RNNs need this
        opt.step()
        losses.append(loss.item())
        if verbose and (step % 200 == 0 or step == steps - 1):
            print(f"  {cell:4s} step {step:4d}  loss {loss.item():.3f}  "
                  f"grad-norm {gn:.2f}")
    return m, losses


@torch.no_grad()
def sample(m, n=10, temperature=1.0, top_k=None, seed=0):
    """Autoregressive generation: the model's own output feeds the next step."""
    m.eval()                                     # turns dropout OFF (Module 1!)
    torch.manual_seed(seed)
    names = []
    for _ in range(n):
        state, tok, chs = m.init_state(1), torch.tensor([PAD]), []
        for _ in range(MAXLEN):
            logits, state = m.step(tok, state)
            logits = logits[0].clone()
            logits[PAD] = -1e9                   # never emit padding
            logits = logits / max(temperature, 1e-6)
            if top_k is not None:
                kth = torch.topk(logits, top_k).values[-1]
                logits[logits < kth] = -1e9      # everything outside top-k dies
            tok = torch.multinomial(F.softmax(logits, -1), 1).view(1)
            if tok.item() == EOS:
                break
            chs.append(itos[tok.item()])
        names.append("".join(chs))
    return names


print("\n=== training a plain RNN ===")
rnn, rnn_losses = train("rnn")
print("\n=== training an LSTM ===")
lstm, lstm_losses = train("lstm")

print("\n=== sampling from the LSTM ===")
for T in [0.5, 0.8, 1.2]:
    s = sample(lstm, 10, temperature=T, seed=1)
    novel = sum(x not in TRAIN_SET for x in s)
    print(f"T={T}: {novel}/10 novel  {s}")
s = sample(lstm, 10, temperature=1.0, top_k=5, seed=1)
print(f"top_k=5: {sum(x not in TRAIN_SET for x in s)}/10 novel  {s}")
for T in [0.5, 0.8, 1.0, 1.2]:
    s = sample(lstm, 60, temperature=T, seed=1)
    print(f"  novelty rate at T={T}: {sum(x not in TRAIN_SET for x in s)}/60")


# ------------------------------------------------- 3. vanishing gradients
def grad_by_position(cell="rnn", T=40, w_scale=1.0, forget_bias=None, seed=0):
    """Measure ||dLoss_T / dh_t|| for every t. Untrained net, random input."""
    torch.manual_seed(seed)
    m = CharRNN(V, hidden=96, cell=cell, p_drop=0.0)
    with torch.no_grad():
        if w_scale != 1.0:
            m.cell.weight_hh.mul_(w_scale)       # crank up to force explosion
        if forget_bias is not None:
            H = m.hidden
            # PyTorch LSTMCell bias layout is [input, forget, cell, output]
            m.cell.bias_ih[H:2 * H].fill_(forget_bias)
            m.cell.bias_hh[H:2 * H].fill_(0.0)
    x = torch.randint(2, V, (1, T))
    logits, kept = m(x, keep_hidden=True)
    F.cross_entropy(logits[:, -1], torch.tensor([2])).backward()  # loss at LAST step
    return [h.grad.norm().item() for h in kept]


probes = {
    "RNN (default init)":        grad_by_position("rnn"),
    "RNN (W_hh x 8, exploding)": grad_by_position("rnn", w_scale=8.0),
    "LSTM (default init)":       grad_by_position("lstm"),
    "LSTM (forget bias = +2)":   grad_by_position("lstm", forget_bias=2.0),
    "GRU (default init)":        grad_by_position("gru"),
}
print("\n=== ||dL_40/dh_t|| ===")
for k, g in probes.items():
    print(f"{k:28s} t=40 {g[-1]:.2e} | t=20 {g[19]:.2e} | t=1 {g[0]:.2e}"
          f" | ratio {g[0]/g[-1]:.2e}")

plt.figure(figsize=(8, 4.8))
for k, g in probes.items():
    plt.plot(range(1, len(g) + 1), g, marker="o", ms=3, label=k)
plt.yscale("log"); plt.xlabel("time step t"); plt.ylabel("|| dLoss_40 / dh_t ||")
plt.title("How far back does the learning signal reach?")
plt.legend(fontsize=8); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("vanishing_gradients.png", dpi=110)

plt.figure(figsize=(7, 4))
plt.plot(rnn_losses, label="RNN"); plt.plot(lstm_losses, label="LSTM")
plt.xlabel("step"); plt.ylabel("cross-entropy"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("rnn_vs_lstm_loss.png", dpi=110)
print("saved plots")
```

### Expected output

```
231 names | vocab 28 | max length with EOS 8
inputs (231, 8) targets (231, 8)
example: aarav -> [2, 2, 19, 2, 23, 1, 0, 0]

=== training a plain RNN ===
  rnn  step    0  loss 3.370  grad-norm 0.55
  rnn  step  200  loss 1.653  grad-norm 0.23
  rnn  step  400  loss 1.343  grad-norm 0.29
  rnn  step  600  loss 1.201  grad-norm 0.33
  rnn  step  799  loss 1.167  grad-norm 0.40

=== training an LSTM ===
  lstm step    0  loss 3.345  grad-norm 0.29
  lstm step  200  loss 1.596  grad-norm 0.16
  lstm step  400  loss 1.153  grad-norm 0.13
  lstm step  600  loss 1.052  grad-norm 0.12
  lstm step  799  loss 1.026  grad-norm 0.15

=== sampling from the LSTM ===
T=0.5: 0/10 novel  ['anika', 'tamara', 'olga', 'eshan', 'orla', 'sanna', 'indira', 'tatiana', 'lucas', 'carmen']
T=0.8: 1/10 novel  ['damian', 'dira', 'uma', 'tibor', 'amara', 'asha', 'klara', 'flora', 'selma', 'farhan']
T=1.2: 2/10 novel  ['matteo', 'dira', 'uma', 'tieo', 'xanthe', 'asha', 'klara', 'flora', 'selma', 'flora']
top_k=5: 3/10 novel  ['damian', 'dira', 'rosa', 'devika', 'arjav', 'chelaa', 'dagmar', 'asha', 'cadence', 'dara']
  novelty rate at T=0.5: 0/60
  novelty rate at T=0.8: 6/60
  novelty rate at T=1.0: 12/60
  novelty rate at T=1.2: 18/60

=== ||dL_40/dh_t|| ===
RNN (default init)           t=40 5.45e-01 | t=20 6.54e-07 | t=1 3.28e-12 | ratio 6.01e-12
RNN (W_hh x 8, exploding)    t=40 5.69e-01 | t=20 2.19e+03 | t=1 9.38e+06 | ratio 1.65e+07
LSTM (default init)          t=40 6.29e-01 | t=20 1.41e-05 | t=1 6.69e-09 | ratio 1.06e-08
LSTM (forget bias = +2)      t=40 6.24e-01 | t=20 2.16e-02 | t=1 1.60e-02 | ratio 2.56e-02
GRU (default init)           t=40 5.48e-01 | t=20 2.36e-05 | t=1 4.55e-09 | ratio 8.31e-09
saved plots
```

### Reading the output like an engineer

**The loss curves.** The LSTM ends at 1.026 and the RNN at 1.167 — the LSTM is meaningfully better even on 8-character names. Note the RNN's grad-norm *rising* (0.23 → 0.40) while the LSTM's falls (0.16 → 0.12). That is a real signature: the plain RNN is fighting instability while the LSTM settles.

**The samples.** `dira`, `tieo`, `arjav`, `chelaa` — pronounceable, name-shaped, and not in the training set. `arjav` is a particularly good one: the model learned the `arj-` opening from `arjun` and the `-av` ending from `aarav`, then recombined them. That recombination is exactly what "learning the structure rather than the list" looks like.

**Novelty versus temperature.** 0 → 6 → 12 → 18 out of 60. At T = 0.5 the model is a lookup table for its training set. The dial is real and you can measure it.

⚠️ **Be honest about the size of this experiment.** 231 names is a very small corpus, and the model largely memorizes it — which is exactly the overfitting picture from Module 1. Dropout 0.3 and weight decay 0.1 are what keep any novelty at all. A production name generator trains on ~30,000 names and produces novel output at T = 0.8. Small data, big model, obvious memorization: you can now name that failure.

**The gradient probe.** Look at the RNN row: `3.28e-12` at t=1. A gradient of 10⁻¹² multiplied by a learning rate of 10⁻³ moves a weight by 10⁻¹⁵ — smaller than float32 can even represent relative to a weight of size 0.1. **The first 20 steps are, numerically, not being trained at all.**

Then look at "LSTM (forget bias = +2)": `1.60e-02` at t=1, only 39× smaller than at t=40, and the curve is nearly flat after step 15. Two lines of initialization code bought six orders of magnitude of memory reach.

---

## ✍️ Practice

### 1. [Warm-up] Unroll a GRU by hand

Using the GRU equations from sub-concept 4, unroll a **one-unit** GRU for 3 steps on `x = [1, 0, 0]` with these simplified gates: `z_t = σ(2x_t − 1)`, `r_t = 1` always, `h̃_t = tanh(1.5·x_t + 0.5·h_(t−1))`, `h₀ = 0`.

Compute `z_t`, `h̃_t`, and `h_t` at every step. Show 4 decimal places.

**Done looks like:** a 3-row table with all three quantities per step, plus one sentence saying whether this GRU is in "remember" mode or "overwrite" mode at t = 2 and t = 3, and which gate value tells you.

### 2. [Warm-up] Predict the temperature effect

For logits `[3.0, 2.0, 1.0]`, compute the softmax probabilities by hand at T = 0.5, T = 1.0, and T = 4.0. Then compute what top-k = 2 gives at T = 1.0.

**Done looks like:** a 3-column probability table (rounded to 3 decimals, each column summing to 1.000), the top-k = 2 probabilities, and one sentence describing the trend in the probability of the *worst* token as T rises.

### 3. [Build] RNN vs GRU vs LSTM, controlled

Using `train()` from the script, train all three cell types with everything else identical. Then for each, sample 60 names at T = 1.0 and report: final loss, novelty rate, and how many samples you personally judge "pronounceable."

Then repeat the whole thing with `seed=1` and `seed=2` inside `train()` (you will need to make the seed a parameter). Report mean and spread — the Module 1 discipline applies here too.

**Done looks like:** a table `cell | final loss (mean ± spread over 3 seeds) | novelty/60 | pronounceable/60`, plus a verdict sentence on whether the LSTM's advantage exceeds the seed noise.

### 4. [Build] Make the memory problem visible with a real task

The name task is only 8 characters long, so the memory problem barely bites. Build a task where it does: the **copy task**.

Generate sequences of the form `[random 5 tokens] [delay of D filler tokens] [the same 5 tokens again]`. Train an RNN and an LSTM to predict the final 5 tokens. Sweep `D ∈ {1, 5, 10, 20, 40}` and plot final accuracy on the copied part against `D` for both cells.

```python
def make_copy_batch(B=64, L=5, D=10, n_sym=8):
    """tokens 0..n_sym-1 are symbols, n_sym is the filler/blank token."""
    core = torch.randint(0, n_sym, (B, L))
    filler = torch.full((B, D), n_sym)
    seq = torch.cat([core, filler, core], dim=1)
    return seq
```

**Done looks like:** one plot with two lines (RNN and LSTM), accuracy versus delay, and a written statement of the delay at which each model drops below 50% accuracy.

### 5. [Stretch] Implement an LSTM cell from scratch

Replace `nn.LSTMCell` with your own `MyLSTMCell(nn.Module)` using only `nn.Linear`, `torch.sigmoid`, and `torch.tanh`. Use one linear layer producing `4*hidden` outputs and split it with `torch.chunk`. Verify correctness by loading `nn.LSTMCell`'s weights into yours and checking the outputs match to within 1e-5.

Then add a `forget_bias` argument that initializes the forget-gate bias, and re-run `grad_by_position` with `forget_bias ∈ {0, 1, 2, 4}`.

**Done looks like:** a passing numerical equivalence test, plus a plot of gradient-versus-position for the four bias values and one sentence stating the bias value at which the gradient stops decaying meaningfully.

### 6. [Stretch] Quantify exposure bias

Measure the gap between teacher forcing and autoregressive generation directly.

1. Compute the model's average per-character loss on the training names **with** teacher forcing (this is just the training loss).
2. Generate 200 names autoregressively at T = 1.0. Feed each generated name *back through the model with teacher forcing* and record its average per-character loss.
3. Compare the two distributions.

If the model's own generations score much worse under its own scoring than the real names do, you have measured exposure bias: the model has walked itself into regions it does not understand.

**Done looks like:** two overlaid histograms with means marked, the numerical gap, and a paragraph explaining why a *higher* loss on the model's own output is evidence of compounding error rather than evidence the outputs are creative.

---

## 🤔 Think Deeper

### 1. The LSTM was published in 1997 and only became dominant around 2014. What has to be true about a good idea for it to sit unused for seventeen years?

*How to reason about it:* List what changed between 1997 and 2014 that had nothing to do with the idea itself — GPU compute, dataset size, autodiff frameworks, the availability of word embeddings, the number of people trying. Then ask the uncomfortable follow-up: which ideas published in the last two years are currently unusable for a reason that will look silly in a decade? Consider also that being *right* and being *demonstrable* are different properties, and only one of them gets you cited.

### 2. Your name generator produced `dira` and `arjav`. Suppose you train the same architecture on 30,000 real names scraped from a public records database and use it to name a product. Who, if anyone, has a claim on the output?

*How to reason about it:* Separate three questions that people usually mash together. (a) Was collecting the data permitted? (b) Does the model *memorize* individual training examples — and you can test this directly, since you measured a 0/60 novelty rate at T = 0.5? (c) Is a generated name that happens to match a real person's rare name a harm, and does it matter whether the model "meant" to produce it? Then consider that names are not copyrightable but *are* identifying, so the relevant law may be privacy rather than copyright. Look up your own novelty measurements before you answer — they are evidence.

### 3. An RNN processes tokens strictly one at a time, so it cannot be parallelized across the sequence during training. A transformer can. Does that mean recurrence is dead, or is there a setting where a sequential model still wins?

*How to reason about it:* Count the costs. An RNN uses O(1) memory per step regardless of sequence length; attention uses O(T²) time and memory for a length-T sequence. Ask what happens at T = 1,000,000 tokens, or on a microcontroller with 64 KB of RAM, or in a streaming setting where tokens arrive one per second forever and there is no "whole sequence" to attend over. Then look up what state-space models (Mamba, S4) are — they are recurrent, they are recent, and they exist precisely because someone asked this question seriously.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Counting padding tokens in the loss | `cross_entropy` happily averages over every position, including the PAD ones, and gives no warning | Pass `ignore_index=PAD`. Otherwise the model spends most of its capacity learning to predict "blank after the end", and your loss number is meaningless |
| Forgetting `model.eval()` before sampling | Sampling is a different function from training, so the mode switch is easy to skip | Call `m.eval()` at the top of the sampling function. With dropout 0.3 left on, ~30% of hidden units are randomly zeroed *during generation* and your names turn to mush |
| Not detaching the hidden state between batches | Carrying `h` forward across batches for statefulness is a legitimate technique, and detaching feels like it would break it | `h = h.detach()` between batches. Otherwise autograd tries to backprop through the entire history since step 0 and you get a "backward through the graph a second time" error, or a memory explosion |
| No gradient clipping | It works fine for the first few hundred steps, so it looks unnecessary | Always `clip_grad_norm_(params, 1.0)` for RNNs. The explosion, when it comes, arrives on one batch and turns every weight to NaN in one step |
| Reusing the training forward pass for generation | The training path takes a `(B, T)` tensor; generation has only one token at a time, and it is tempting to fake it | Write a separate `step()` method that takes one token and a state. Trying to reuse `forward()` by growing a tensor each step is slow and easy to get wrong |
| Assuming an LSTM fixes long-range memory completely | "LSTM solves vanishing gradients" is repeated everywhere without a number attached | The forget gate gives per-step factor `f`. `0.95⁴⁰⁰ ≈ 4 × 10⁻⁹`. LSTMs buy hundreds of steps, not thousands. Measure your own model's `grad_by_position` at the length you actually care about |
| Comparing sample quality at different temperatures | Two models sampled at different T look very different, and it feels like a model difference | Fix the temperature *and* the random seed when comparing models. Novelty rate at T = 0.5 (0/60) and T = 1.2 (18/60) differ by more than most architecture changes will |
| Training on names but sampling with `<START>` = a real character | The start token has to come from somewhere and PAD is sitting right there | Use a dedicated start symbol and be consistent between `inputs[:, 0]` in training and `tok` at the start of generation. In this script both are `PAD`, deliberately |

---

## 🛠️ Mini-Project: Name Generator + Vanishing-Gradient Report

**Time:** ~6 hours

### Goal

Train a character-level RNN on a typed-in list of names, generate new plausible ones, sample at three temperatures, and then produce the plot and the written explanation that show *why* recurrence hits a wall. This is the piece of evidence you will refer back to in Module 3.

### Starter steps

1. **Build your own name list.** Do not reuse the 231 in the script — pick a theme (fantasy characters, chemical elements, station names, dinosaur genera, football clubs) and type in **at least 200** entries, all lowercase, letters only. Type them; do not download a file.

2. **Train three cells.** RNN, GRU, LSTM, identical everything else, 3 seeds each. Record final loss as mean ± spread.

3. **Sample at three temperatures** (0.6, 1.0, 1.4) plus one top-k run. For each setting produce 60 samples and record:
   - novelty rate (fraction not in the training list)
   - your own pronounceability judgement (read them aloud; be strict)
   - the average length compared with the training average

4. **Run the gradient probe** at sequence lengths T = 10, 20, 40, 80 for RNN and for LSTM with forget bias 0 and 2. That is 8 curves. Put the RNN and LSTM curves on the same log-scale axes.

5. **Force an explosion.** Set `w_scale = 8.0` and train with `clip=None` (pass `float("inf")`). Record the step at which the loss becomes NaN. Then re-run with `clip=1.0` and show it survives. Report both.

6. **Write the explanation.** 400–600 words, and it must contain:
   - the per-step multiplication `(1 − h²)·W_hh` written out
   - your own measured numbers, not the ones in this module
   - the specific claim "the loss at step T depends on `h_1` by a factor of X, which means the first N steps receive effectively no gradient", with your X and N
   - one sentence naming what an LSTM fixes and one naming what it does **not** fix

### Success criteria checklist

- [ ] At least 200 hand-typed names in a single theme
- [ ] Generated samples are pronounceable — at least 30 of 60 at T = 1.0 pass your read-aloud test
- [ ] Novelty rate reported at all three temperatures, and it increases with temperature
- [ ] A gradient-magnitude-versus-position plot on a **log** y-axis with at least three labelled curves
- [ ] Measurable decay demonstrated: state the ratio between t = 1 and t = T explicitly
- [ ] An explosion reproduced *and* fixed with clipping, with the NaN step number recorded
- [ ] The written explanation cites your own numbers throughout
- [ ] Loss curves for all three cell types on shared axes

### Level it up

Add a **conditional** generator: prefix each name during training with a category token (for example `<nordic>` or `<sanskrit>`, whichever fits your theme), so the model learns `p(name | category)`. At generation time, seed the loop with the category token instead of `<START>` and see whether the styles actually separate.

Then measure it: generate 60 names per category and check whether a simple classifier — or just you, blind — can tell which category each came from at better than chance. If the categories do not separate, that is a finding too, and the interesting question is whether the model lacks capacity, data, or a long enough memory to keep the category token in mind eight characters later. That last hypothesis is directly testable with the gradient probe you already built, and it is the perfect bridge into Module 3.

---

## 🔑 Key Takeaways

- **Bag-of-words destroys order**, and order is where most of the meaning in language lives. A 10-word sentence has 3.6 million orderings that all collapse to the same bag.
- **An RNN is one small function applied repeatedly**, carrying a fixed-size hidden state. Unrolled, it is a very deep network whose layers all share the same weights.
- **Backpropagation through time multiplies one Jacobian per step.** The factor `(1 − h²)·W_hh` is almost never exactly 1, so the product either vanishes or explodes — measured here as `3.28e-12` and `9.38e+06` from the same architecture.
- **Clipping fixes explosion only.** Vanishing needs an architectural change, not a safety rail.
- **The LSTM's cell state updates by addition**, so `∂c_t/∂c_(t−1) = f_t`. A forget gate near 1 is a gradient highway — the same trick as the residual connection from Module 1.
- **Gates buy hundreds of steps, not unlimited memory.** `0.95⁴⁰⁰ ≈ 4 × 10⁻⁹`. The LSTM postpones the wall; it does not remove it.
- **Training uses teacher forcing; generation is autoregressive.** The mismatch is exposure bias, and it is why models can have great losses and bad outputs.
- **Sampling is a real design decision.** Greedy repeats, temperature trades quality for novelty (0/60 novel at T = 0.5, 18/60 at T = 1.2), and top-k puts a floor under quality.

---

## 📓 Vocabulary

| Term | Plain definition | Example |
|---|---|---|
| **Sequence** | An ordered list where the order carries meaning | "dog bit postman" ≠ "postman bit dog" |
| **Bag of words** | A representation that keeps counts and discards order | Both sentences above give the same count vector |
| **Recurrent neural network (RNN)** | One small function applied once per item, passing a summary vector forward | `h_t = tanh(W_xh·x_t + W_hh·h_(t−1) + b)` |
| **Hidden state** | The fixed-size vector holding everything remembered so far | The one sticky note you are allowed while reading a novel |
| **Unrolling** | Drawing the recurrent loop as a chain of identical copies | A 40-step sequence becomes a 40-layer network |
| **Weight sharing** | Using the same parameters at every time step | Why an RNN handles any length with fixed parameter count |
| **BPTT** | Backpropagation applied to the unrolled network | Gradient at step 1 requires 39 chained Jacobians for T = 40 |
| **Vanishing gradient** | The learning signal shrinking to nothing over many steps | Measured `3.28e-12` at t = 1 for a 40-step RNN |
| **Exploding gradient** | The same product growing without bound | Measured `9.38e+06` with `W_hh` scaled by 8 |
| **Gradient clipping** | Rescaling the gradient down if its norm exceeds a threshold | `clip_grad_norm_(params, 1.0)` — mandatory for RNNs |
| **Cell state** | The LSTM's additive memory track, separate from the hidden state | `c_t = f_t⊙c_(t−1) + i_t⊙g_t` |
| **Gate** | A 0–1 vector from a sigmoid that scales how much passes through | Forget gate 0.95 → keep 95% of memory each step |
| **Forget gate bias** | The initial bias on the forget gate; set to +2 to start in "remember" mode | σ(2) = 0.881 instead of σ(0) = 0.5 |
| **GRU** | A simpler gated cell: one update gate, one reset gate, no separate cell state | `h_t = (1−z)⊙h_(t−1) + z⊙h̃_t` |
| **Teacher forcing** | Feeding the true previous token during training regardless of the prediction | Training on "anika": step 3 always sees the real `n` |
| **Autoregressive generation** | Feeding the model's own output back as the next input | `<START>→d→i→r→a→<EOS>` gives "dira" |
| **Exposure bias** | Training only on perfect histories, then generating from imperfect ones | Small errors compound because nothing corrects them |
| **Logits** | Raw unnormalized scores, one per vocabulary item | `[2.0, 1.0, 0.5, 0.0]` before softmax |
| **Temperature** | Divide logits by T before softmax; low = sharp, high = flat | At T = 0.5 the top token's probability rose from 0.579 to 0.831 |
| **Top-k sampling** | Keep only the k best tokens, renormalize, then sample | k = 2 turned `[0.579, 0.213, 0.129, 0.078]` into `[0.731, 0.269, 0, 0]` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Unroll a GRU by hand

Gates: `z_t = σ(2x_t − 1)`, `r_t = 1`, `h̃_t = tanh(1.5x_t + 0.5h_(t−1))`, `h_t = (1−z_t)h_(t−1) + z_t h̃_t`, `h₀ = 0`.

**t = 1** (`x = 1`):
- `z₁ = σ(2(1) − 1) = σ(1) = 0.7311`
- `h̃₁ = tanh(1.5(1) + 0.5(0)) = tanh(1.5) = 0.9051`
- `h₁ = (1 − 0.7311)(0) + 0.7311(0.9051) = 0 + 0.6617 = ` **0.6617**

**t = 2** (`x = 0`):
- `z₂ = σ(2(0) − 1) = σ(−1) = 0.2689`
- `h̃₂ = tanh(0 + 0.5(0.6617)) = tanh(0.3309) = 0.3193`
- `h₂ = (1 − 0.2689)(0.6617) + 0.2689(0.3193) = 0.7311(0.6617) + 0.0859`
- `= 0.4838 + 0.0859 = ` **0.5697**

**t = 3** (`x = 0`):
- `z₃ = σ(−1) = 0.2689`
- `h̃₃ = tanh(0.5(0.5697)) = tanh(0.2849) = 0.2774`
- `h₃ = 0.7311(0.5697) + 0.2689(0.2774) = 0.4165 + 0.0746 = ` **0.4911**

| t | z_t | h̃_t | h_t |
|---|---|---|---|
| 1 | 0.7311 | 0.9051 | 0.6617 |
| 2 | 0.2689 | 0.3193 | 0.5697 |
| 3 | 0.2689 | 0.2774 | 0.4911 |

**Answer sentence:** at t = 2 and t = 3 the GRU is in **remember** mode. The update gate `z = 0.2689` means only 27% of the state is replaced by the new candidate, so 73% of the previous state is carried straight through. Compare with t = 1, where `z = 0.7311` and the state was mostly overwritten by new input — exactly what you want when the input actually contains something.

Note the decay: 0.6617 → 0.5697 → 0.4911, retaining 86% per step. Compare that to the vanilla RNN's 48% per step in the worked example. The gate did that.

### 2. [Warm-up] Predict the temperature effect

Logits `[3.0, 2.0, 1.0]`.

**T = 0.5** → scaled logits `[6.0, 4.0, 2.0]`
`exp = 403.429, 54.598, 7.389`; sum = 465.416
- 403.429/465.416 = **0.867**
- 54.598/465.416 = **0.117**
- 7.389/465.416 = **0.016**

**T = 1.0** → logits `[3.0, 2.0, 1.0]`
`exp = 20.086, 7.389, 2.718`; sum = 30.193
- 20.086/30.193 = **0.665**
- 7.389/30.193 = **0.245**
- 2.718/30.193 = **0.090**

**T = 4.0** → scaled logits `[0.75, 0.50, 0.25]`
`exp = 2.117, 1.649, 1.284`; sum = 5.050
- 2.117/5.050 = **0.419**
- 1.649/5.050 = **0.327**
- 1.284/5.050 = **0.254**

| token | logit | T=0.5 | T=1.0 | T=4.0 |
|---|---|---|---|---|
| A | 3.0 | 0.867 | 0.665 | 0.419 |
| B | 2.0 | 0.117 | 0.245 | 0.327 |
| C | 1.0 | 0.016 | 0.090 | 0.254 |
| **sum** | | **1.000** | **1.000** | **1.000** |

**Top-k = 2 at T = 1.0:** keep A and B; new sum = 20.086 + 7.389 = 27.475
- p(A) = 20.086/27.475 = **0.731**
- p(B) = 7.389/27.475 = **0.269**
- p(C) = **0.000**

**Trend sentence:** the worst token's probability rises steadily with temperature — 0.016 → 0.090 → 0.254, a 16× increase from T = 0.5 to T = 4.0. At T = 4.0 the three tokens are within a factor of 1.6 of each other, so the model's ranking has almost stopped mattering. As T → ∞ every probability converges to 1/3.

### 3. [Build] RNN vs GRU vs LSTM, controlled

Add a seed argument:

```python
def train(cell="lstm", steps=800, lr=3e-3, wd=0.1, clip=1.0,
          seed=0, verbose=False):
    torch.manual_seed(seed)
    ...
```

Then:

```python
import statistics
rows = []
for cell in ["rnn", "gru", "lstm"]:
    finals, novs = [], []
    for seed in [0, 1, 2]:
        m, losses = train(cell, seed=seed)
        finals.append(losses[-1])
        s = sample(m, 60, temperature=1.0, seed=1)
        novs.append(sum(x not in TRAIN_SET for x in s))
    rows.append((cell, statistics.mean(finals),
                 max(finals) - min(finals), statistics.mean(novs)))
for r in rows:
    print(f"{r[0]:5s} loss {r[1]:.3f} (spread {r[2]:.3f})  novel {r[3]:.1f}/60")
```

Representative results (seed 0 values are the ones printed by the module script):

| cell | final loss (mean, spread over 3 seeds) | novelty/60 at T=1.0 | pronounceable (judgement) |
|---|---|---|---|
| rnn | ≈ 1.17, spread ≈ 0.03 | ≈ 20 | ~60–70% of the novel ones |
| gru | ≈ 1.05, spread ≈ 0.03 | ≈ 14 | ~75% |
| lstm | ≈ 1.03, spread ≈ 0.02 | ≈ 12 | ~80% |

**Verdict:** the LSTM's advantage over the RNN (≈ 0.14 in loss) is roughly **5× the seed spread** (≈ 0.03), so it is a real effect, not noise. The LSTM's advantage over the GRU (≈ 0.02) is **the same size as the spread**, so on this task you cannot claim the LSTM beats the GRU — and the GRU is cheaper. That is the honest reading, and the whole reason for running three seeds.

Note the inverse relationship between loss and novelty: the RNN fits worse, so it wanders further from the training set, so it produces more novel names — but a larger share of them are junk. **Novelty alone is not a quality metric.** You need both numbers.

### 4. [Build] The copy task

```python
def make_copy_batch(B=64, L=5, D=10, n_sym=8, seed=None):
    if seed is not None:
        torch.manual_seed(seed)
    core = torch.randint(0, n_sym, (B, L))
    filler = torch.full((B, D), n_sym)
    return torch.cat([core, filler, core], dim=1), core


def run_copy(cell, D, L=5, n_sym=8, steps=1500, hidden=64):
    torch.manual_seed(0)
    vocab = n_sym + 1
    m = CharRNN(vocab, emb=16, hidden=hidden, cell=cell, p_drop=0.0)
    opt = torch.optim.AdamW(m.parameters(), lr=3e-3)
    for step in range(steps):
        seq, core = make_copy_batch(64, L, D, n_sym)
        inp = torch.cat([torch.full((64, 1), n_sym), seq[:, :-1]], dim=1)
        logits, _ = m(inp)
        # only score the final L positions -- the copied part
        loss = F.cross_entropy(logits[:, -L:].reshape(-1, vocab),
                               core.reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
    with torch.no_grad():
        seq, core = make_copy_batch(512, L, D, n_sym, seed=99)
        inp = torch.cat([torch.full((512, 1), n_sym), seq[:, :-1]], dim=1)
        logits, _ = m(inp)
        acc = (logits[:, -L:].argmax(-1) == core).float().mean().item()
    return acc


for cell in ["rnn", "lstm"]:
    for D in [1, 5, 10, 20, 40]:
        print(cell, D, f"{run_copy(cell, D):.3f}")
```

**What you should find:** both models are near 100% at D = 1. The RNN degrades sharply — typically dropping below 50% somewhere around D = 10–20 — while the LSTM holds high accuracy considerably longer, often to D = 40. Chance accuracy is 1/8 = 0.125, so "below 50%" is well above chance but far from useful.

**Why this task is the right diagnostic:** it requires *exact* recall of a specific symbol from exactly D+L steps ago, with no statistical shortcut. Name generation lets the model cheat with letter-frequency statistics; the copy task does not. The delay at which accuracy collapses is a direct measurement of the model's memory horizon in steps, and it should line up with where your gradient plot goes flat.

If your RNN does surprisingly well, check that `n_sym` is large enough — with only 2 symbols, guessing gets you 50% for free.

### 5. [Stretch] Implement an LSTM cell from scratch

```python
class MyLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size, forget_bias=0.0):
        super().__init__()
        self.hidden_size = hidden_size
        # one linear for all four gates: [i, f, g, o] stacked, matching PyTorch
        self.x2h = nn.Linear(input_size, 4 * hidden_size)
        self.h2h = nn.Linear(hidden_size, 4 * hidden_size)
        with torch.no_grad():
            H = hidden_size
            self.x2h.bias[H:2 * H].fill_(forget_bias)
            self.h2h.bias[H:2 * H].fill_(0.0)

    def forward(self, x, state):
        h_prev, c_prev = state
        gates = self.x2h(x) + self.h2h(h_prev)          # (B, 4H)
        i, f, g, o = gates.chunk(4, dim=1)              # PyTorch's ifgo order
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c = f * c_prev + i * g                          # the additive highway
        h = o * torch.tanh(c)
        return h, c


# ---- equivalence test against nn.LSTMCell ----
torch.manual_seed(0)
ref = nn.LSTMCell(16, 32)
mine = MyLSTMCell(16, 32)
with torch.no_grad():
    mine.x2h.weight.copy_(ref.weight_ih)
    mine.h2h.weight.copy_(ref.weight_hh)
    mine.x2h.bias.copy_(ref.bias_ih)
    mine.h2h.bias.copy_(ref.bias_hh)

x = torch.randn(4, 16)
s = (torch.zeros(4, 32), torch.zeros(4, 32))
hr, cr = ref(x, s)
hm, cm = mine(x, s)
print("max |h diff| =", (hr - hm).abs().max().item())
print("max |c diff| =", (cr - cm).abs().max().item())
assert torch.allclose(hr, hm, atol=1e-5) and torch.allclose(cr, cm, atol=1e-5)
print("equivalence OK")
```

Expected: both differences print as approximately `0.0` (typically under 1e-7) and the assertion passes.

**Two details that trip people up:**

1. **Gate order.** PyTorch stacks the gates as `[input, forget, cell, output]` (i, f, g, o). Many textbooks write them in a different order. If you chunk in the wrong order, the cell still trains — badly — and you will never find the bug by staring at the loss. This is why the equivalence test exists.
2. **Two biases.** `nn.LSTMCell` has both `bias_ih` and `bias_hh`, which are mathematically redundant (their sum is the only thing that matters) but present for CuDNN compatibility. Copy both, and when setting a forget bias, set one and zero the other so the effective bias is exactly what you intended.

**The forget-bias sweep.** With `forget_bias ∈ {0, 1, 2, 4}`, the gradient at t = 1 (from the module's own probe) goes roughly:

| forget bias | σ(bias) | grad at t = 1 |
|---|---|---|
| 0 | 0.500 | ~7e-09 |
| 1 | 0.731 | ~1e-04 |
| 2 | 0.881 | ~1.6e-02 |
| 4 | 0.982 | ~1.2e-01 |

**Answer sentence:** decay stops being meaningful somewhere between bias 2 and bias 4. At bias 4 the forget gate is σ(4) = 0.982, so `0.982⁴⁰ = 0.485` — the signal at t = 1 is within a factor of 2 of the signal at t = 40, and the curve is essentially flat. The cost is that the cell starts out unable to forget anything, which can slow early learning on tasks where forgetting is the right behaviour.

### 6. [Stretch] Quantify exposure bias

```python
@torch.no_grad()
def score(m, words):
    """Average per-character teacher-forced loss for each word."""
    m.eval()
    out = []
    for w in words:
        w = w[:MAXLEN - 1]
        ids = torch.tensor([encode(w)])
        inp = torch.full((1, MAXLEN), PAD, dtype=torch.long)
        inp[:, 1:] = ids[:, :-1]
        logits, _ = m(inp)
        loss = F.cross_entropy(logits.reshape(-1, V), ids.reshape(-1),
                               ignore_index=PAD)
        out.append(loss.item())
    return np.array(out)

real_scores = score(lstm, NAMES)
gen = [g for g in sample(lstm, 200, temperature=1.0, seed=7) if len(g) > 0]
gen_scores = score(lstm, gen)

print(f"real names   mean {real_scores.mean():.3f}  median "
      f"{np.median(real_scores):.3f}  n={len(real_scores)}")
print(f"generated    mean {gen_scores.mean():.3f}  median "
      f"{np.median(gen_scores):.3f}  n={len(gen_scores)}")
print(f"gap = {gen_scores.mean() - real_scores.mean():.3f} nats/char")

plt.figure(figsize=(7, 4))
bins = np.linspace(0, max(gen_scores.max(), real_scores.max()), 30)
plt.hist(real_scores, bins=bins, alpha=0.6, label="real names")
plt.hist(gen_scores, bins=bins, alpha=0.6, label="model's own samples")
plt.axvline(real_scores.mean(), ls="--")
plt.axvline(gen_scores.mean(), ls="--", color="C1")
plt.xlabel("per-character loss (nats)"); plt.ylabel("count"); plt.legend()
plt.tight_layout(); plt.savefig("exposure_bias.png", dpi=110)
```

**What you should see:** the real names sit around 0.9–1.1 nats/char. The model's own T = 1.0 samples score noticeably higher — typically 1.2–1.6 nats/char — with a long right tail of samples the model finds genuinely surprising.

**The explanation paragraph:**

A higher loss on the model's own output is not a paradox — it is compounding error made visible. During training the model is only ever asked "given a *real* prefix, what comes next?" Its parameters are fit to the distribution of real prefixes. When it generates, it samples from its own distribution, and a single low-probability character produces a prefix that is now *slightly off-distribution*. The model has less reliable knowledge about that prefix, so its next prediction is worse, which pushes the prefix further off-distribution. The right tail of the histogram is made of samples where this ran away.

Crucially, this is **not** evidence that the output is creative. A creative-but-good name would be one the model assigns *low* loss to despite it not being in the training set — the model recognizes it as well-formed. High self-loss means the model itself does not think its own output is name-like. You can separate the two by filtering: generate 500 names, keep only those with per-character loss below the real-name mean, and check whether the survivors read better. They usually do, and that filtering trick is a crude version of what "reranking" does in real generation systems.

One honest caveat: sampling at T = 1.0 from a model deliberately regularized to be uncertain will always produce some high-loss output; part of the gap is just sampling entropy, not compounding. To separate them, repeat the measurement at T = 0.5 (where output is nearly all memorized training names) and check that the gap shrinks to near zero. If it does, the temperature-1 gap is genuine drift.

</details>

---

[⬅ Previous](module-01-deep-learning-at-depth.md) · [Level 4 Home](README.md) · [Next ➡](module-03-attention-and-transformers.md)
