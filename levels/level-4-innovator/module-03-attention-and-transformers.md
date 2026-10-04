# Module 3 — Attention and Transformers: Build a Tiny GPT

[⬅ Previous](module-02-sequence-models.md) · [Level 4 Home](README.md) · [Next ➡](module-04-how-llms-are-trained.md)

**Level 4 · Module 3 · ~8 hours · Prereqs: Module 1 (residual connections, layer norm, AdamW, warmup+cosine), Module 2 (hidden state, vanishing gradients, teacher forcing, temperature and top-k sampling), matrix multiplication and softmax**

---

## 🎯 What You'll Be Able To Do

- **Compute scaled dot-product attention by hand** for a 3-token sequence, producing every score, every softmax weight, and every output number.
- **Explain query, key, and value as roles**, and say precisely why the scores are divided by the square root of the head dimension — with a numeric demonstration of what goes wrong if you skip it.
- **Implement causal masking, multi-head attention, and a complete transformer block** in PyTorch, from `nn.Linear` upwards.
- **Train a character-level GPT from scratch** until it writes readable English, show it learning at three checkpoints, and explain every single line of the code.
- **Read an attention heatmap** and say what a specific head has learned to look at.

---

## 🪝 The Hook

In Module 2 you measured the exact failure of recurrent memory. The gradient reaching back 40 steps was `3.28 × 10⁻¹²` — one four-hundred-billionth of the signal at the last step. You watched an LSTM improve that to `1.6 × 10⁻²`, and then you worked out that `0.95⁴⁰⁰ ≈ 4 × 10⁻⁹`, so even the LSTM's memory dies out somewhere in the hundreds of steps.

Now consider *why* that happens. It happens because information from step 1 has to be **carried** to step 400, and carrying means passing through 399 multiplications.

So here is the idea that ended the debate, in one sentence:

> **Stop carrying. Let step 400 reach back and read step 1 directly.**

No hidden state. No chain of 399 multiplications. One matrix multiply, and every position can see every earlier position at a distance of exactly **one** operation. This is called attention, the paper that introduced it was called *Attention Is All You Need*, and by the end of this module you will have built the entire thing and trained it to write sentences.

---

## 🧠 The Concept

### 1. Attention as soft, differentiable lookup

#### Start with something you already know: a dictionary

```python
prices = {"bread": 2.50, "fish": 6.00, "rope": 4.25}
prices["fish"]      # -> 6.00
```

A lookup has three parts:

- the thing you are asking for — `"fish"` — the **query**
- the labels you compare it against — `"bread"`, `"fish"`, `"rope"` — the **keys**
- the things you get back — `2.50`, `6.00`, `4.25` — the **values**

Python's dictionary is a **hard** lookup: the query either matches a key exactly or it fails. And "matches exactly" has no derivative, so you cannot train it with gradient descent.

#### Make it soft

**Attention** is *a lookup where the query is compared to every key, the comparisons become weights that sum to 1, and the answer is the weighted average of all the values*.

```
hard lookup:  answer = values[ index of the one matching key ]
soft lookup:  answer = Σ  weight(query, key_i) × value_i      with Σ weights = 1
```

Nothing is a hard yes or no, so everything has a gradient, so the whole thing can be learned.

#### 🍕 Analogy: asking a class a question

You ask a class: *"who knows about the river?"* That is the **query**. Every student has a mental label for what they know — "bread", "the river", "rope" — those are the **keys**. What each student could actually tell you is their **value**.

A hard lookup picks one student and hears only them. Attention lets every student answer at a volume proportional to how well their label matched your question: the river expert at 70%, the fisherman at 25%, the rope maker at 5%. You hear the blend, and nobody is silenced by a tie-breaker.

#### Tiny example with numbers

Three keys with these match scores against your query: `bread: 0.1`, `river: 2.0`, `rope: 0.3`. Their values are the numbers `10`, `50`, `30`.

Softmax the scores: `exp(0.1) = 1.105`, `exp(2.0) = 7.389`, `exp(0.3) = 1.350`; sum = 9.844.

- weight(bread) = 1.105/9.844 = 0.112
- weight(river) = 7.389/9.844 = 0.751
- weight(rope) = 1.350/9.844 = 0.137

Output = 0.112(10) + 0.751(50) + 0.137(30) = 1.12 + 37.55 + 4.11 = **42.78**

Mostly the river's answer, with a trace of the other two. And every one of those numbers is differentiable, so if 42.78 was the wrong answer, gradient descent can adjust the keys, the query, and the values to fix it.

---

### 2. Query, key, value; scores; softmax; and why we divide by √d

#### Where Q, K, V come from

In a transformer the queries, keys, and values are not given to you — they are **computed from the tokens themselves by three learned linear layers**. This is called **self-attention**: *every token produces its own query, its own key, and its own value, and attends over the same sequence it belongs to*.

```
X   : (T, d_model)     the token vectors coming into this layer
Q = X · W_Q            (T, d_k)   "what am I looking for?"
K = X · W_K            (T, d_k)   "what do I have to offer?"
V = X · W_V            (T, d_v)   "what do I actually contribute?"
```

The **only** learned parameters in a head are `W_Q`, `W_K`, `W_V` (plus an output projection). The attention operation itself has no parameters at all.

#### The formula

```
                    ⎛  Q Kᵀ  ⎞
Attention(Q,K,V) = softmax⎜ ────── ⎟ V
                    ⎝   √d_k ⎠
```

Read it as four steps:

1. `Q Kᵀ` — every query dotted with every key. Result: a `(T, T)` matrix of raw **scores**. Entry `(i, j)` is "how much does token i want to hear from token j?"
2. `/ √d_k` — the **scaling**, explained in a moment.
3. `softmax(·, dim=-1)` — each row becomes a probability distribution over all positions. Rows sum to 1.
4. `... V` — multiply by the values. Each output row is a weighted average of value vectors.

```
   ┌──────┐ W_Q  ┌───┐
   │      ├─────▶│ Q │──┐
   │      │      └───┘  │   ┌──────────┐   ┌─────────┐   ┌────────┐
   │  X   │ W_K  ┌───┐  ├──▶│ Q Kᵀ/√dk │──▶│ softmax │──▶│  × V   │──▶ out
   │(T,d) ├─────▶│ K │──┘   └──────────┘   └─────────┘   └────────┘
   │      │      └───┘         (T,T)         (T,T)          (T,dv)
   │      │ W_V  ┌───┐                                        ▲
   │      ├─────▶│ V │────────────────────────────────────────┘
   └──────┘      └───┘
```

#### 🍕 Analogy: a dating app for tokens

Your **query** is your "looking for" profile, your **key** is your "about me" profile, and your **value** is what you actually bring. Every token writes all three; the score matrix is everyone rating everyone else's compatibility. Crucially, "looking for" and "about me" are **separate** — a verb can look for its subject while advertising itself as a verb. Collapsing Q and K into one vector would force "what I want" to equal "what I am", a much weaker model.

#### Why divide by √d_k — the demonstration

Suppose the entries of `q` and `k` are independent with mean 0 and variance 1. Their dot product is `Σᵢ qᵢkᵢ`, a sum of `d_k` independent terms each with variance 1. So:

```
Var(q · k) = d_k        →      standard deviation = √d_k
```

With `d_k = 64`, the raw scores have a standard deviation of **8**. So typical scores swing between roughly −16 and +16, and the largest in a row can easily be 20 higher than the smallest.

Feed that to a softmax and see what happens. Take three raw scores `[8, −2, 1]`:

- `exp(8) = 2980.96`, `exp(−2) = 0.135`, `exp(1) = 2.718`; sum = 2983.81
- weights = **[0.99904, 0.000045, 0.000911]**

That is a hard one-hot lookup. It has thrown away the softness that made attention trainable in the first place — and worse, the gradient of softmax through a near-one-hot output is nearly zero, so this head has stopped learning.

Now divide by `√64 = 8` first, giving `[1.0, −0.25, 0.125]`:

- `exp(1.0) = 2.718`, `exp(−0.25) = 0.779`, `exp(0.125) = 1.133`; sum = 4.630
- weights = **[0.587, 0.168, 0.245]**

Soft. Informative. Differentiable.

Top-to-bottom weight ratio: **22,000 : 1** unscaled versus **3.5 : 1** scaled.

> **The scaling is not cosmetic.** Dividing by `√d_k` normalizes the score variance back to 1 regardless of head size, so a 64-dimensional head and a 128-dimensional head both start with usefully soft attention. Remove that one division and large models stop training.

---

### 3. Causal masking: hiding the future

#### The problem

A language model predicts the next token: position 5 must predict token 6. But attention as described lets position 5 look at *every* position — including 6, 7, and 8. If position 5 can see token 6, predicting it is trivial: copy it. The loss goes to near zero, the model learns nothing, and generation produces garbage because the future genuinely does not exist yet. This is **label leakage** — the easiest way to build a language model that looks perfect and is worthless.

🍕 It is an exam with the answer sheet on the desk. You score 100%, you learn nothing, and you fail the moment nobody hands you the answers. Causal masking is taking the answer sheet off the desk.

#### The fix

**Causal masking** (also called *autoregressive masking*) — *before the softmax, set every score where the key position is later than the query position to −∞, so those positions get exactly zero weight*.

Why −∞ and not 0? Because the masking happens **before** the softmax, and `exp(−∞) = 0`. Setting the score to 0 would instead give `exp(0) = 1`, a perfectly respectable weight. The mask must be applied in score space, not in weight space.

In practice you use a large negative number like `-1e9`, or PyTorch's `float("-inf")` with `masked_fill`.

#### What the mask looks like

For a 4-token sequence, `allowed[i][j] = 1` means "query i may attend to key j":

```
        key: t1   t2   t3   t4
 query t1  [  1    0    0    0  ]   t1 sees only itself
 query t2  [  1    1    0    0  ]   t2 sees t1, t2
 query t3  [  1    1    1    0  ]   t3 sees t1, t2, t3
 query t4  [  1    1    1    1  ]   t4 sees everything so far
```

A lower-triangular matrix. In PyTorch: `torch.tril(torch.ones(T, T))`.

```python
att = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5     # (T, T) scores
att = att.masked_fill(tril[:T, :T] == 0, float("-inf")) # hide the future
att = F.softmax(att, dim=-1)                            # rows sum to 1
```

Note that row 1 has exactly one allowed entry, so after softmax it is `[1, 0, 0, 0]` — the first token can only attend to itself, no matter what the scores say. That is correct and unavoidable.

#### The beautiful side effect

Because of the mask, **one forward pass computes a legitimate next-token prediction for every position at once** — a 64-token sequence gives 64 training signals from one pass. That is 64× more supervision per forward pass than an RNN gets, and it is a bigger part of why transformers train faster than the parallel hardware use is. (Encoder models like BERT drop the mask entirely, because they fill in blanks rather than predict the next token. **Causal masking is what makes a transformer generative.**)

---

### 4. Multi-head attention: parallel subspaces of meaning

#### One head is not enough

At position 33 of `the baker made bread every morning`, several questions matter at once: which characters are in the word I am inside? where was the last word boundary? is a `.` likely here? A single head produces **one** distribution over positions, so it must pick one blend — it cannot attend hard to position 32 (previous character) *and* position 4 (start of the word).

🍕 Give one document to four experts. The grammarian tracks structure, the fact-checker tracks names, the editor tracks tone, the proofreader tracks the last three words. Four short specialist reports beat one general report of the same total length.

**Multi-head attention** — *split the model dimension into `h` chunks, run an independent attention head on each chunk, then concatenate the outputs and pass them through one more linear layer*.

#### The arithmetic

With `d_model = 128` and `n_head = 4`, each head gets `d_k = 128/4 = 32` dimensions.

```
head 0:  Q,K,V of size (T, 32)  →  out (T, 32)
head 1:  Q,K,V of size (T, 32)  →  out (T, 32)
head 2:  Q,K,V of size (T, 32)  →  out (T, 32)
head 3:  Q,K,V of size (T, 32)  →  out (T, 32)
                                     │
concat along the feature axis ───────┘  →  (T, 128)
                                     │
output projection W_O (128 → 128) ───┘  →  (T, 128)
```

The parameter count is unchanged from one big 128-dimensional head: `4 × 3 × (128×32) = 49,152`, exactly `3 × (128×128)`. **Multi-head attention is free** — you are not adding parameters, you are partitioning the ones you have so they can specialize. The output projection `W_O` matters too: without it the four heads' outputs would be stacked side by side with no mixing, and later layers would have to untangle them.

#### Real measurements from the model you will train

Here is the mean **look-back distance** — how many characters back a head puts its attention weight, on average — for all 16 heads of the 4-layer GPT you will build:

| Layer | H0 | H1 | H2 | H3 | layer mean |
|---|---|---|---|---|---|
| 0 | 3.67 | 3.72 | 3.63 | 3.52 | **3.64** |
| 1 | 6.06 | 6.78 | 7.25 | 6.92 | **6.75** |
| 2 | 6.58 | 7.21 | 7.93 | 7.10 | **7.21** |
| 3 | 6.48 | 6.93 | 8.41 | 7.59 | **7.35** |

(Real CPU run, seed 1337, 2,500 steps. Your digits will differ slightly.) Read the last column. **Depth buys range**, though not evenly: layer 0 looks ~3.6 characters back ("the current word so far"); layers 1-3 look ~6.8-7.4 back, and the last layer is only slightly above the middle ones. Nobody programmed this. Early layers assemble letters into word-fragments, later layers assemble fragments into phrases — exactly the hierarchy you would design by hand.

---

### 5. Positional encodings: giving a permutation-blind model a sense of order

#### The problem, stated exactly

`Q Kᵀ` is a dot product between token vectors, and dot products do not know where their operands came from. Shuffle the input tokens and you get the same set of outputs, shuffled identically.

> **Attention is permutation-equivariant** — *permute the inputs and the outputs permute identically; nothing about the computation depends on position.*

So a transformer without positional information sees no difference between *the dog bit the postman* and *the postman bit the dog*. That is Module 2's bag-of-words problem again. The RNN got order for free by processing tokens in order; the transformer processes them all at once, so **order has to be put in by hand.**

#### The fix: add a position vector to every token vector

```
x_t = token_embedding[token_id]  +  position_embedding[t]
```

Just addition, at the very bottom of the network, once. Everything above it operates on vectors that already know where they are.

#### Two ways to make the position vectors

**Learned positional embeddings** — *an ordinary `nn.Embedding(max_len, d_model)` whose rows train like any other parameter*. GPT-2 used these, and so will you: `x = self.tok_emb(idx) + self.pos_emb(torch.arange(T))`. Simple, and the model learns whatever notion of position helps. The cost: it cannot handle a sequence longer than `block_size`, because row 65 of a 64-row table does not exist.

**Sinusoidal positional encodings** — *a fixed, non-learned pattern of sines and cosines at geometrically spaced frequencies*:

```
PE(pos, 2i)   = sin( pos / 10000^(2i/d) )
PE(pos, 2i+1) = cos( pos / 10000^(2i/d) )
```

**Worked out for `d = 4`.** Dimension pair `i = 0` has divisor `10000^0 = 1`; pair `i = 1` has divisor `10000^(2/4) = 100`.

| pos | sin(pos/1) | cos(pos/1) | sin(pos/100) | cos(pos/100) |
|---|---|---|---|---|
| 0 | 0.0000 | 1.0000 | 0.0000 | 1.0000 |
| 1 | 0.8415 | 0.5403 | 0.0100 | 1.0000 |
| 2 | 0.9093 | −0.4161 | 0.0200 | 0.9998 |
| 3 | 0.1411 | −0.9900 | 0.0300 | 0.9996 |

#### 🍕 Analogy: the hands of a clock

The second hand spins fast — it separates *this second from the next* but repeats every minute. The hour hand barely moves — it cannot separate adjacent seconds but never repeats in a day. Read all the hands together and the position is unambiguous. Sinusoidal encoding is a clock with `d/2` hands, geometrically spaced from very fast to very slow: fast dimensions say "one token along or two?", slow dimensions say "near the start or the end?"

The clever property: `PE(pos + k)` is a fixed linear function of `PE(pos)` for any offset `k`, so the model can detect *relative* offsets with one learned matrix. And being a formula rather than a table, it extends past any length seen in training.

| | Learned | Sinusoidal |
|---|---|---|
| Parameters | `max_len × d_model` | 0 |
| Beyond training length | impossible | works (degrades) |
| Encodes relative position | must be learned | built in |
| Used by | GPT-2, BERT | original transformer |

Modern models mostly use **RoPE (rotary positional embeddings)**, which *rotates* the query and key vectors by an angle proportional to position, so the dot product between them depends only on their *relative* distance. Same clock idea, applied inside the attention score rather than added at the bottom.

---

### 6. The transformer block, and parallelism versus recurrence

#### Attention alone is not enough

Attention **moves information between positions**, but it does not do much *thinking* about it — each output is just a weighted average of value vectors, a linear operation once the weights are fixed. So every transformer block pairs attention with a small per-position network:

**Feed-forward network (FFN / MLP)** — *a two-layer MLP applied independently and identically to every position, expanding to 4× the model width and back*: `Linear(128, 512) → GELU → Linear(512, 128)`.

It has **no** cross-position mixing at all — position 7's FFN never sees position 8. That is the division of labour:

> **Attention gathers; the MLP thinks.**

The 4× expansion is a convention that has survived every scaling study since 2017, and it is where most of the parameters live: in your tiny GPT the MLPs hold **131,712** parameters per block versus **65,664** for attention.

#### The full block

```
             x  (T, d_model)
             │
     ┌───────┴────────┐
     │           ┌────▼────┐
     │           │ LayerNorm│
     │           └────┬────┘
     │        ┌───────▼────────┐
     │        │ Multi-Head     │
     │        │ Causal Attn    │
     │        └───────┬────────┘
     └──────▶ (+) ◀───┘                 ← residual connection
             │
     ┌───────┴────────┐
     │           ┌────▼────┐
     │           │ LayerNorm│
     │           └────┬────┘
     │        ┌───────▼────────┐
     │        │  MLP  4x       │
     │        └───────┬────────┘
     └──────▶ (+) ◀───┘                 ← residual connection
             │
             ▼  out (T, d_model)
```

In code that is exactly two lines:

```python
x = x + self.attn(self.ln1(x))
x = x + self.ff(self.ln2(x))
```

Every piece comes from Module 1. **Residual connections:** `d(x + f(x))/dx = 1 + f'(x)`, so stacking 96 blocks (GPT-3) still gets gradient to the bottom; without them 6 layers is about the limit. **Layer norm, not batch norm:** sequences vary in length and inference batches can be size 1, so you normalize across each token's own features. **Pre-norm placement:** the norm sits *inside* the residual branch (`x + attn(ln(x))`), not after the addition (`ln(x + attn(x))`). The 2017 paper used post-norm and needed heroic warmup; pre-norm keeps a clean identity path and trains far more reliably. Every modern model uses pre-norm.

#### Parallelism versus recurrence — the trade that decided everything

| | RNN / LSTM | Transformer |
|---|---|---|
| Path length from token 1 to token T | **T** sequential steps | **1** attention operation |
| Training: can positions be computed in parallel? | No — `h_t` needs `h_(t−1)` | **Yes** — one matmul does all T |
| Time per layer (sequence length T, width d) | O(T · d²) but **serial in T** | O(T² · d) and **fully parallel** |
| Memory for the attention weights | O(d) | **O(T²)** |
| Generation (one token at a time) | O(1) state, fast | must re-read all T previous tokens |
| Long-range gradient | dies (measured: 10⁻¹² at 40 steps) | constant — one hop |

Read the first row. **That is the whole revolution.** In an RNN the gradient from token 400 to token 1 crosses 399 multiplications. In a transformer it crosses one. Nothing to vanish.

Read the fifth row too, because it is the price: attention costs `O(T²)`. Double the context and you quadruple the compute and the memory. At `T = 1024` the attention matrix has a million entries per head per layer. Everything you have heard about "context windows" and their cost comes from this one quadratic.

⚠️ Note the honest asymmetry: transformers win enormously at *training* (parallel) and only partly at *generation* (still one token at a time, and now with an `O(T)` re-read per token, mitigated by caching the keys and values). The revolution was mostly about being able to train on far more data in the same wall-clock time — which is exactly the setup for Module 4.

---

## 🔍 Worked Example

**Task:** compute a full causal self-attention layer by hand for a 3-token sequence. Every number shown. No steps skipped.

### The setup

Three tokens: `the`, `cat`, `sat`. Model dimension `d_model = 2`, head dimension `d_k = 2`.

Input matrix `X` (rows = tokens, after positional information has already been added):

```
        x₁ = [1, 0]        "the"
   X =  x₂ = [0, 1]        "cat"
        x₃ = [1, 1]        "sat"
```

Weight matrices (chosen to be readable, not realistic):

```
W_Q = [[1, 0],      W_K = [[1, 0],      W_V = [[0, 1],
       [0, 1]]             [0, 1]]             [1, 0]]
     (identity)          (identity)          (swap)
```

### Step 1 — project to Q, K, V

`W_Q` and `W_K` are the identity, so `Q = X` and `K = X`. `W_V` swaps the two components, so each `v = [x₂, x₁]`:

```
      q₁ = [1, 0]        k₁ = [1, 0]        v₁ = [0, 1]
Q  =  q₂ = [0, 1]   K  = k₂ = [0, 1]   V  = v₂ = [1, 0]
      q₃ = [1, 1]        k₃ = [1, 1]        v₃ = [1, 1]
```

### Step 2 — raw scores `Q Kᵀ`, then scale by `√d_k = √2 = 1.4142`

Nine dot products, each shown as `raw → scaled`:

| | k₁ = [1,0] | k₂ = [0,1] | k₃ = [1,1] |
|---|---|---|---|
| **q₁ = [1,0]** | 1(1)+0(0) = 1 → 0.7071 | 1(0)+0(1) = 0 → 0.0000 | 1(1)+0(1) = 1 → 0.7071 |
| **q₂ = [0,1]** | 0(1)+1(0) = 0 → 0.0000 | 0(0)+1(1) = 1 → 0.7071 | 0(1)+1(1) = 1 → 0.7071 |
| **q₃ = [1,1]** | 1(1)+1(0) = 1 → 0.7071 | 1(0)+1(1) = 1 → 0.7071 | 1(1)+1(1) = 2 → 1.4142 |

### Step 3 — apply the causal mask

Everything strictly above the diagonal becomes −∞:

| | k₁ | k₂ | k₃ |
|---|---|---|---|
| **q₁** | 0.7071 | −∞ | −∞ |
| **q₂** | 0.0000 | 0.7071 | −∞ |
| **q₃** | 0.7071 | 0.7071 | 1.4142 |

### Step 4 — softmax each row

**Row 1:** only one live entry, so no arithmetic needed.
`exp(0.7071) = 2.0281`, and `exp(−∞) = 0`. Sum = 2.0281.
weights = `[2.0281/2.0281, 0, 0]` = **[1.0000, 0, 0]**

*Token 1 attends 100% to itself. Unavoidable — it has no past.*

**Row 2:** `exp(0.0000) = 1.0000`, `exp(0.7071) = 2.0281`. Sum = 3.0281.
- 1.0000 / 3.0281 = **0.3302**
- 2.0281 / 3.0281 = **0.6698**

weights = **[0.3302, 0.6698, 0]** (check: 0.3302 + 0.6698 = 1.0000 ✓)

**Row 3:** `exp(0.7071) = 2.0281`, `exp(0.7071) = 2.0281`, `exp(1.4142) = 4.1133`. Sum = 8.1695.
- 2.0281 / 8.1695 = **0.2483**
- 2.0281 / 8.1695 = **0.2483**
- 4.1133 / 8.1695 = **0.5035**

weights = **[0.2483, 0.2483, 0.5035]** (check: sum = 1.0001, rounding ✓)

The full attention weight matrix:

```
           the     cat     sat
 the   [ 1.0000  0.0000  0.0000 ]
 cat   [ 0.3302  0.6698  0.0000 ]
 sat   [ 0.2483  0.2483  0.5035 ]
```

Every row sums to 1. Every entry above the diagonal is exactly 0. **This is the picture you will see in the heatmap you plot later** — a lower-triangular block of colour with black above the diagonal.

### Step 5 — multiply by V

`V = [[0,1], [1,0], [1,1]]`

**Output row 1:** `1.0000·[0,1] + 0·[1,0] + 0·[1,1]` = **[0.0000, 1.0000]**

**Output row 2:** `0.3302·[0,1] + 0.6698·[1,0]`
- first component: `0.3302(0) + 0.6698(1) = 0.6698`
- second component: `0.3302(1) + 0.6698(0) = 0.3302`
- = **[0.6698, 0.3302]**

**Output row 3:** `0.2483·[0,1] + 0.2483·[1,0] + 0.5035·[1,1]`
- first: `0.2483(0) + 0.2483(1) + 0.5035(1) = 0 + 0.2483 + 0.5035 = 0.7518`
- second: `0.2483(1) + 0.2483(0) + 0.5035(1) = 0.2483 + 0 + 0.5035 = 0.7518`
- = **[0.7518, 0.7518]**

### The final answer

```
             input X          →   attention output
 the        [1, 0]                [0.0000, 1.0000]
 cat        [0, 1]                [0.6698, 0.3302]
 sat        [1, 1]                [0.7518, 0.7518]
```

### What just happened, in words

Token `sat` produced a blend of all three value vectors, weighted 25% / 25% / 50%. It **read from the past directly** — not through a hidden state squashed twice on the way, but through a single weighted sum. At 400 tokens, token 400 would read token 1 through the same single weighted sum, with the same gradient path. That is the whole idea; everything else in a transformer is engineering around this one operation.

**Four sanity checks to run every time.** (1) Rows sum to 1: 1.0000, 1.0000, 1.0001 ✓. (2) Upper triangle exactly zero ✓ — if not, your mask is broken and the model will "learn" by cheating. (3) Row 1 is one-hot on position 1 ✓ — there is nothing else it can be. (4) Every output lies inside the convex hull of the value vectors: `[0.7518, 0.7518]` sits between `[0,1]`, `[1,0]`, `[1,1]` ✓; outside means you multiplied by the wrong matrix.

---

## 💻 Hands-On

### Setup

Everything runs offline on CPU only (torch + numpy + matplotlib, already installed). The whole script takes about 2 minutes on 2 CPU threads (133 s measured for 2,500 steps). The dataset is ~7,000 characters typed directly into the file: no downloads.

### The complete Tiny GPT

Save as `tiny_gpt.py`.

```python
"""Module 3 Hands-On — a character-level GPT, built from scratch."""
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

torch.manual_seed(1337)
DEVICE = "cpu"   # this course is CPU-only; do not switch it

# ------------------------------------------------------------------ 1. data
CORPUS = """
the sun rose over the quiet town and the baker opened her door.
the baker made bread every morning before the sun rose.
the boy walked to school with a book under his arm.
the girl walked to school with a kite under her arm.
the teacher asked a question and the class went quiet.
a question is a small door and an answer is a room behind it.
the river ran past the town and the town grew beside the river.
in the morning the river was quiet and in the evening it was loud.
the old man fed the birds by the river every single morning.
the birds knew the old man and the old man knew the birds.
a bridge crossed the river and the children crossed the bridge.
under the bridge the water was cold and dark and slow.
the market opened at noon and closed when the sun went down.
at the market you could buy bread and fish and rope and salt.
the fisherman sold fish and the baker sold bread and both were happy.
the rope maker made rope and nobody asked how the rope was made.
a cat slept on the wall beside the market every afternoon.
the cat did not care about bread or fish or rope or salt.
the cat cared about the sun on the wall and nothing else.
when it rained the market closed and the cat found a dry door.
the rain fell on the roofs and ran down into the river.
the river rose and the bridge held and the town slept.
in the winter the river froze and the children walked on it.
the old man told them not to walk on the river in the winter.
the children listened to the old man because the old man was right.
a story is a road and a road goes somewhere if you follow it.
the teacher said that a question is better than a guess.
the boy said that a guess is better than nothing at all.
the girl said that both of them were right and both were wrong.
the class laughed and the teacher wrote the question on the board.
every morning the baker counted her loaves before she opened.
every evening the fisherman counted his fish before he went home.
counting is a quiet thing and it makes the world hold still.
the old man did not count the birds because the birds moved too much.
the sun rose over the quiet town and the day began again.
a town is a machine made of people and roads and small kindnesses.
the baker gave bread to the old man and the old man fed the birds.
the birds sang over the river and the children heard them sing.
the teacher opened a window so the class could hear the birds.
a window is a door for sound and light but not for people.
the boy drew a bird in his book and the girl drew a river.
the teacher drew a bridge between the bird and the river.
that is how a lesson works said the teacher and the class went quiet.
in the spring the ice broke and the river ran fast and brown.
the fisherman waited because the fish would come back in time.
waiting is work even when it does not look like work.
the rope maker made a long rope and gave it to the fisherman.
the fisherman tied his boat to the bridge with the long rope.
the boat held and the river ran and the town went on.
the cat watched the boat from the wall and did not move.
the sun went down behind the roofs and the market closed.
the baker swept her floor and the teacher closed her window.
the old man walked home along the river in the last of the light.
the children ran ahead of him and he did not try to keep up.
a town at night is a quiet machine and it still runs.
in the morning the baker opened her door before the sun rose.
the boy asked the old man why the birds came back every year.
the old man said that the birds remember the shape of the river.
the girl asked whether a river has a shape at all.
the old man said that everything has a shape if you watch it long enough.
the teacher wrote the word shape on the board and drew a river beside it.
the class copied the word and nobody copied the river.
the boy copied the river and left the word out.
the teacher said that both of those are notes and neither one is wrong.
a note is a rope you throw to the person you will be tomorrow.
the rope maker liked that line and asked the teacher to write it down.
the teacher wrote it on a small card and gave it to the rope maker.
the rope maker kept the card in his pocket for the rest of the winter.
the fisherman found a broken oar under the bridge one cold morning.
he carried the oar to the rope maker and the rope maker mended it.
mending is quieter than making and it is often harder.
the baker mended a torn sack with thread and did not tell anyone.
the teacher mended a broken chair and told the whole class about it.
the old man mended nothing because the old man threw nothing away.
the cat mended nothing and the cat was not ashamed.
in the summer the market stayed open until the light was gone.
the children ran between the stalls and nobody stopped them.
the fisherman gave a small fish to the cat and the cat took it.
the cat did not thank the fisherman because cats do not do that.
the fisherman did not mind because he had not asked for thanks.
a gift with a price on it is a trade and both of them are fine.
the baker traded bread for fish and the fisherman traded fish for bread.
the rope maker traded rope for both and everyone went home full.
the teacher traded questions for answers and the class grew.
the old man traded nothing and the town gave him bread anyway.
in the autumn the leaves fell into the river and floated to the sea.
the boy asked where the sea was and the girl said far past the bridge.
the old man said the sea is where the river stops explaining itself.
the teacher wrote that on the board and did not explain it.
the class thought about it for a long time and then went home.
some questions are meant to be carried and not answered.
the boy carried that one all winter and asked about it in the spring.
the old man had forgotten saying it and laughed a long time.
the girl remembered every word and told him what he had said.
the old man said that is why we need more than one person in a town.
the baker heard the story and put it in her bread song.
she sang the bread song every morning while the loaves rose.
the loaves did not care about the song but the baker did.
a song is a way of counting that does not feel like counting.
the fisherman sang nothing and counted his fish in his head.
the rope maker hummed and lost count and started over every time.
the teacher sang badly and the class loved her for it.
the children sang the bread song walking home over the bridge.
the old man heard them from the river and fed the birds and smiled.
the birds did not sing back because the birds were eating.
in the last week of winter the ice broke with a sound like a door.
the whole town heard it and everybody knew what it meant.
the fisherman untied his boat and the rope maker checked the rope.
the baker made extra bread and the teacher opened the window.
the old man walked to the bridge and watched the brown water go.
the children came running and the cat stayed on the wall.
the sun rose over the quiet town and the day began again.
"""

text = CORPUS.strip()
chars = sorted(set(text))              # every distinct character, sorted
V = len(chars)                         # vocabulary size
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join(itos[i] for i in l)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]
print(f"{len(text)} chars | vocab {V} | train {len(train_data)} "
      f"val {len(val_data)} | device {DEVICE}")

BLOCK = 64        # context length: how far back the model can see
BATCH = 32
N_EMBD = 128      # d_model
N_HEAD = 4        # so each head gets 128/4 = 32 dimensions
N_LAYER = 4
DROPOUT = 0.1


def get_batch(split):
    """Grab BATCH random windows of length BLOCK; y is x shifted one right."""
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - BLOCK - 1, (BATCH,))
    x = torch.stack([d[i:i + BLOCK] for i in ix])
    y = torch.stack([d[i + 1:i + BLOCK + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


# --------------------------------------------------------- 2. one attention head
class Head(nn.Module):
    def __init__(self, n_embd, head_size, block, dropout):
        super().__init__()
        # no bias: the bias would be absorbed by layer norm anyway
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        # a buffer moves with .to(device) but is not a trainable parameter
        self.register_buffer("tril", torch.tril(torch.ones(block, block)))
        self.drop = nn.Dropout(dropout)
        self.last_attn = None                       # stashed for the heatmap

    def forward(self, x):
        B, T, C = x.shape
        k, q, v = self.key(x), self.query(x), self.value(x)   # each (B,T,hs)
        # (B,T,hs) @ (B,hs,T) -> (B,T,T);  the *hs**-0.5 is the 1/sqrt(d_k) scaling
        att = q @ k.transpose(-2, -1) * k.shape[-1] ** -0.5
        att = att.masked_fill(self.tril[:T, :T] == 0, float("-inf"))  # causal
        att = F.softmax(att, dim=-1)                # rows now sum to 1
        self.last_attn = att.detach()
        return self.drop(att) @ v                   # (B,T,T) @ (B,T,hs) -> (B,T,hs)


# ------------------------------------------------------ 3. multi-head attention
class MultiHeadAttention(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        hs = n_embd // n_head                       # 128 // 4 = 32
        self.heads = nn.ModuleList([Head(n_embd, hs, block, dropout)
                                    for _ in range(n_head)])
        self.proj = nn.Linear(n_embd, n_embd)       # W_O: blends the heads
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)   # (B,T,n_embd)
        return self.drop(self.proj(out))


# ------------------------------------------------------------ 4. the MLP
class FeedForward(nn.Module):
    """Applied to each position independently. Attention gathers, this thinks."""
    def __init__(self, n_embd, dropout):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd), nn.GELU(),
            nn.Linear(4 * n_embd, n_embd), nn.Dropout(dropout))

    def forward(self, x):
        return self.net(x)


# --------------------------------------------------- 5. the transformer block
class Block(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        self.ln1 = nn.LayerNorm(n_embd)
        self.attn = MultiHeadAttention(n_embd, n_head, block, dropout)
        self.ln2 = nn.LayerNorm(n_embd)
        self.ff = FeedForward(n_embd, dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))   # pre-norm + residual (Module 1)
        x = x + self.ff(self.ln2(x))
        return x


# --------------------------------------------------------------- 6. the GPT
class TinyGPT(nn.Module):
    def __init__(self, vocab, n_embd=N_EMBD, n_head=N_HEAD, n_layer=N_LAYER,
                 block=BLOCK, dropout=DROPOUT):
        super().__init__()
        self.block_size = block
        self.tok_emb = nn.Embedding(vocab, n_embd)   # what the token is
        self.pos_emb = nn.Embedding(block, n_embd)   # where the token is
        self.blocks = nn.ModuleList([Block(n_embd, n_head, block, dropout)
                                     for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)             # final norm before the head
        self.head = nn.Linear(n_embd, vocab)         # project to vocab logits
        self.apply(self._init)

    def _init(self, m):
        """GPT-2's initialization: small normal weights, zero biases."""
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)    # token + position
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.ln_f(x))             # (B, T, vocab)
        loss = None
        if targets is not None:
            # every one of the T positions is a training example
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                   targets.reshape(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        """Autoregressive sampling — Module 2's loop, new engine."""
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]     # never exceed the context
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature  # only the last position
            if top_k is not None:
                v = torch.topk(logits, top_k).values
                logits[logits < v[:, [-1]]] = -float("inf")
            probs = F.softmax(logits, dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        self.train()
        return idx


model = TinyGPT(V).to(DEVICE)
print(f"parameters: {sum(p.numel() for p in model.parameters()):,}")

# ------------------------------------------------------------- 7. training
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
MAX_STEPS = 2500
WARMUP = 100
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (      # Module 1
    (s + 1) / WARMUP if s < WARMUP else
    0.5 * (1 + math.cos(math.pi * (s - WARMUP) / (MAX_STEPS - WARMUP)))))


@torch.no_grad()
def estimate_loss(iters=20):
    """Average over several batches — a single batch is far too noisy."""
    model.eval()
    out = {}
    for split in ["train", "val"]:
        losses = torch.zeros(iters)
        for k in range(iters):
            x, y = get_batch(split)
            _, l = model(x, y)
            losses[k] = l.item()
        out[split] = losses.mean().item()
    model.train()
    return out


history = []
CHECKPOINTS = [0, 300, 1200, 2499]
for step in range(MAX_STEPS):
    if step in CHECKPOINTS:                      # watch it learn
        ctx = torch.tensor([[stoi["t"]]], device=DEVICE)
        torch.manual_seed(0)
        s = decode(model.generate(ctx, 220, temperature=0.8)[0].tolist())
        lo = estimate_loss()
        print(f"\n--- step {step} | train {lo['train']:.3f} "
              f"val {lo['val']:.3f} ---")
        print(repr(s))
    x, y = get_batch("train")
    _, loss = model(x, y)
    opt.zero_grad(set_to_none=True)
    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    sched.step()
    history.append(loss.item())
    if step % 500 == 0:
        lo = estimate_loss()
        print(f"step {step:4d} train {lo['train']:.3f} val {lo['val']:.3f}")

lo = estimate_loss()
print(f"\nFINAL train {lo['train']:.3f} val {lo['val']:.3f}")
ctx = torch.tensor([[stoi["t"]]], device=DEVICE)
torch.manual_seed(0)
print(decode(model.generate(ctx, 400, temperature=0.8)[0].tolist()))

# ------------------------------------------------- 8. look inside the heads
prompt = "the baker made bread every morning"
idx = torch.tensor([encode(prompt)], device=DEVICE)
model.eval()
with torch.no_grad():
    model(idx)                                   # populates every last_attn

print("\n=== what does each head look at? ===")
for li in range(N_LAYER):
    for hi in range(N_HEAD):
        a = model.blocks[li].attn.heads[hi].last_attn[0]      # (T, T)
        T = a.shape[0]
        pos = torch.arange(T, device=a.device).float()
        dist = ((pos.unsqueeze(0) - pos.unsqueeze(1)).abs() * a).sum(-1)
        print(f"L{li} H{hi}: mean look-back {dist[5:].mean():.2f} chars, "
              f"self-weight {a.diagonal().mean().item():.2f}")

q = len(prompt) - 1
a = model.blocks[1].attn.heads[0].last_attn[0][q]
top = torch.topk(a, 5)
print(f"\nquery = last char {prompt[q]!r} (pos {q}), top-5 attended:")
for w, i in zip(top.values.tolist(), top.indices.tolist()):
    print(f"   pos {i:2d} {prompt[i]!r}  weight {w:.3f}")

att = model.blocks[1].attn.heads[0].last_attn[0].cpu().numpy()
plt.figure(figsize=(7, 6))
plt.imshow(att, cmap="viridis")
plt.xticks(range(len(prompt)), list(prompt), fontsize=6)
plt.yticks(range(len(prompt)), list(prompt), fontsize=6)
plt.xlabel("key position (attended TO)")
plt.ylabel("query position (attending FROM)")
plt.colorbar(); plt.title("layer 1, head 0 — causal attention")
plt.tight_layout(); plt.savefig("attention_heatmap.png", dpi=110)

plt.figure(figsize=(7, 4))
plt.plot(history, alpha=0.3, label="per-step")
k = 50
plt.plot(np.arange(k - 1, len(history)),
         np.convolve(history, np.ones(k) / k, mode="valid"),
         label="50-step moving average")
plt.xlabel("step"); plt.ylabel("train loss"); plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("loss_curve.png", dpi=110)
print("\nsaved attention_heatmap.png and loss_curve.png")
```

### Expected output

```
6972 chars | vocab 28 | train 6274 val 698 | device cpu
parameters: 807,196

--- step 0 | train 3.346 val 3.339 ---
'tur.gah\nczcw\nqkhooe\nog wazh\ncyxgkiqknwekxueqwafgrqvltzoafncsphdyafpn\nynhfkrhbcuwyxcdbmegigzifshlq
 ezfuwpafo\nfwofhgtrf\nnzwfufptlxncwm.eyxyfdlafzdlhf...'
step    0 train 3.340 val 3.335

--- step 300 | train 1.722 val 1.779 ---
'the.\naher cat thoold s wan thean is wa ithe is are ndooa nd nd thepn the br wean.\nas macisund sl
 thefow rd the foger san fopeald com end id arorl theof t the ntrd brale thean rd doto meake man...'
step  500 train 1.226 val 1.410
step 1000 train 0.445 val 1.328

--- step 1200 | train 0.301 val 1.451 ---
'the cat cared about is on the board and drew a river from and the bnothing he birds.\na girl kiver
 the witer thas gone with and lough.\nthe teacher wrote that on the board and drew begar one the
 river beside it.\nthe boy cop...'
step 1500 train 0.212 val 1.589
step 2000 train 0.159 val 1.664

--- step 2499 | train 0.148 val 1.682 ---
'the cat was not askt about it in the spring.\nthe old man had forgotten saying it and laughed a
 long time.\nthe girl remembered every word and told him what he had said.\nthe old man said that
 is why we need more than one pe...'

FINAL train 0.150 val 1.669

=== what does each head look at? ===
L0 H0: mean look-back 3.67 chars, self-weight 0.15
L0 H1: mean look-back 3.72 chars, self-weight 0.14
   ... (all 16 heads; the full numbers are the table in sub-concept 4) ...
L3 H2: mean look-back 8.41 chars, self-weight 0.15
L3 H3: mean look-back 7.59 chars, self-weight 0.10

query = last char 'g' (pos 33), top-5 attended:
   pos 28 'o'  weight 0.204
   pos 29 'r'  weight 0.162
   pos 31 'i'  weight 0.156
   pos 33 'g'  weight 0.076
   pos 26 ' '  weight 0.062

saved attention_heatmap.png and loss_curve.png
```

### Reading the output like an engineer

**Step 0 — `tur.gah\nczcw\nqkhooe...`** Pure noise, loss 3.346. A uniform guess over 28 characters costs `ln(28) = 3.332`. **Your model at step 0 should always be within a hair of `ln(vocab_size)`** — far above means broken initialization, below means a leak.

**Step 300 — `the.\naher cat thoold s wan thean...`** Loss 1.722. Character statistics learned: `the` everywhere, words 3–6 characters, spaces and newlines in plausible places. Roughly a bigram model.

**Step 1200 — `the cat cared about is on the board and drew a river from and the bnothing he birds.`** Train 0.301, val 1.451. Mostly real words and fragments of real grammar, plus invented non-words (`bnothing`, `kiver`, `witer`) and **sentences that are not in the corpus**. Semantically nonsense, but English-shaped text assembled from learned pieces. That is the generalizing regime (and it is not clean: some of it is garbage).

**Step 2499 — `the cat was not askt about it in the spring. the old man had forgotten saying it...`** Train 0.148, and after the first sentence (a near-miss with the typo `askt`), the sentences are **verbatim quotations** of the corpus. The model has stopped generalizing and started reciting.

**Now read the validation column: 3.339 → 1.779 → 1.328 → 1.451 → 1.664 → 1.682.** That is Module 1's overfitting U-curve, live, in a transformer. Best validation is near step 1000; everything after is memorization. With 807,196 parameters and 6,972 characters — **115 parameters per character** — that is not surprising, it is inevitable. ⚠️ The fix is not a cleverer architecture, it is more data. GPT-2 had 124M parameters and 8B training tokens: roughly **64 tokens per parameter**, not 0.009. That ratio is the subject of Module 4.

**The head statistics.** Mean look-back by layer: 3.64 → 6.75 → 7.21 → 7.35 characters — a monotonic increase in range with depth (steep from layer 0 to layer 1, then slow), learned from nothing but next-character prediction. And the top-5 for the final `g` of `morning` are positions 28 (`o`), 29 (`r`), 31 (`i`): the letters of `morning` itself. That head does within-word tracking.

**The heatmap.** Expect a hard black triangle above the diagonal (the mask working), a bright first column (the "attention sink" — many queries park weight on position 0), and bright bands near the diagonal (local context).

---

## ✍️ Practice

### 1. [Warm-up] Attention by hand, again

Repeat the worked example with the **same** `X`, `W_Q`, `W_K` but a different value matrix:

```
W_V = [[2, 0],
       [0, 3]]
```

Compute `V`, then all three output rows. The attention weights do not change (they depend only on Q and K), so you can reuse them.

**Done looks like:** the `V` matrix, the three output rows to 4 decimal places, and one sentence explaining why the weight matrix was unchanged.

### 2. [Warm-up] Break the mask on purpose

In `Head.forward`, comment out the `masked_fill` line and retrain for 500 steps. Report the train and validation loss, then generate 200 characters.

**Done looks like:** the loss numbers, the generated sample, and a paragraph explaining precisely how a loss *lower* than the masked model's is evidence of a bug rather than an improvement. Include what the generated text looks like and why it is bad despite the good loss.

### 3. [Build] Ablate every component

Run six configurations for 1500 steps each and report best validation loss: (1) no positional embedding — delete `+ self.pos_emb(pos)`; (2) `N_HEAD = 1`; (3) no MLP — `Block.forward` becomes just `x = x + self.attn(self.ln1(x))`; (4) no residuals — `x = self.attn(self.ln1(x))` then `x = self.ff(self.ln2(x))`; (5) no scaling — remove `* k.shape[-1] ** -0.5`; (6) `N_LAYER = 1`.

**Done looks like:** a table sorted by best validation loss, one sentence per ablation explaining the mechanism behind the damage, and a statement of which single removal hurts most and whether that matched your prediction.

### 4. [Build] Make attention efficient with batched heads

The shipped `MultiHeadAttention` loops over heads in Python. Real implementations do all heads in one batched matmul. Write `MultiHeadAttentionFast` that uses **one** `nn.Linear(n_embd, 3 * n_embd)` for Q, K, V together (then `.split(n_embd, dim=2)`), reshapes each to `(B, n_head, T, head_size)` via `.view(B, T, n_head, hs).transpose(1, 2)`, runs scale-mask-softmax-`@v` on the 4-D tensors, and reshapes back to `(B, T, n_embd)`. Verify equivalence by copying the loop version's weights across, then time both.

**Done looks like:** a passing `torch.allclose` test at `atol=1e-5`, and a timing comparison over 100 forward passes.

### 5. [Stretch] Sinusoidal versus learned positions, and extrapolation

Implement sinusoidal positional encodings as a non-trainable buffer. Train two models — one learned, one sinusoidal — at `BLOCK = 32`, then evaluate both at lengths 32, 48, and 64. The learned model has only 32 embedding rows, so report exactly what happens beyond 32: crash, or forced truncation?

**Done looks like:** a table of validation loss versus evaluation length for both models, the exact failure mode of the learned version, and a sentence on whether the sinusoidal model at length 64 was actually usable or merely non-crashing.

### 6. [Stretch] Find and name a head

For each of the 16 heads, compute over a held-out passage: (a) mean look-back distance, (b) weight on the immediately previous position, (c) weight on position 0, (d) weight on the most recent space character. Build a 16-row table. Then take the head with the most extreme value in any column, plot its attention matrix on a 40-character prompt, and write a "head card": a name, a claim, three pieces of supporting evidence, and one prompt on which your claim fails.

**Done looks like:** the 16-row table, one heatmap, and the head card including the honest failure case.

---

## 🤔 Think Deeper

### 1. Attention costs `O(T²)`. Doubling the context quadruples the compute. Every year models ship with longer contexts anyway. What is actually being traded, and where does it stop?

*How to reason about it:* Put numbers on it. At `T = 1,000,000` the attention matrix has 10¹² entries — per head, per layer. That does not fit in any memory that exists. So something must be giving. Look up what one of these does and work out what it gives up: sliding-window attention, sparse attention, linear attention, or the KV cache. Each one buys speed by refusing to compute some attention weights. Then ask the sharper question: if a model can only actually *use* information from a few thousand tokens back, is a million-token context window a capability or a marketing number? Design an experiment that could tell the difference.

### 2. You trained a model on 7,000 characters and it ended up reciting them verbatim. A frontier model trained on trillions of tokens sometimes reproduces long passages from its training data too. Is that the same phenomenon, and does the scale change the ethics?

*How to reason about it:* Separate the mechanism from the consequence. Mechanically, memorization happens when a sequence is rare enough and repeated enough that reproducing it is the lowest-loss option — you can watch that happen in your own model between step 1000 and step 2500. Consequentially, ask: does it matter whether the memorized text was a public-domain nursery rhyme, a copyrighted novel, or someone's leaked medical record? Consider that "the model rarely does this" is a statistical claim, and a one-in-a-million event happens constantly at a billion queries a day. Then ask what a *test* for this would look like, since you now know how to write one.

### 3. The transformer replaced recurrence largely because it parallelizes across the sequence during training. That is an argument about hardware, not about intelligence. What does that suggest about which architecture "wins" next?

*How to reason about it:* Notice that the 1997 LSTM and the 2017 transformer solve almost the same problem, and the transformer's decisive advantage was that it maps onto a GPU. Ask what the *current* hardware constraint is — is it FLOPs, or memory bandwidth, or interconnect between chips? Then ask which architectural choices would look good under a different constraint. Look at what state-space models (Mamba) optimize for, and note that they are recurrent. The uncomfortable implication is that architecture research is partly a search over what current silicon happens to be fast at, which means good ideas can be temporarily wrong.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Masking after the softmax | Zeroing out the future feels like the natural thing to do to a probability matrix | Mask **before** softmax by setting scores to `-inf`. Masking after leaves rows that no longer sum to 1, silently rescaling every prediction |
| Forgetting the `1/√d_k` scaling | The model still trains at small `d_k`, so the bug hides until you scale up | `att = q @ k.transpose(-2,-1) * k.shape[-1]**-0.5`. Without it, at `d_k = 64` scores have σ = 8 and the softmax saturates to one-hot |
| Using `0` instead of `-inf` for the mask | 0 looks like "no contribution" | `exp(0) = 1`, which is a perfectly ordinary weight. The masked positions would get *more* weight than genuinely low-scoring ones |
| Forgetting positional embeddings | The model still trains and the loss still falls, just to a worse floor | Without positions the model is permutation-blind — it can learn character frequencies but not word order. Compare against a baseline; the gap is large and obvious |
| Transposing the wrong dimensions | `k.transpose(-2,-1)` vs `k.T` vs `k.transpose(0,1)` all look plausible | Always use negative indices (`-2, -1`) so the code works with or without a batch dimension. Print `.shape` after every line the first time you write it |
| Post-norm instead of pre-norm | The 2017 paper says post-norm, and lots of diagrams copy it | Use `x = x + attn(ln(x))`, not `x = ln(x + attn(x))`. Pre-norm keeps a clean identity path and trains without heroic warmup schedules |
| Generating past the context window | `generate` happily concatenates forever until the position embedding table runs out | Slice: `idx_cond = idx[:, -self.block_size:]`. Otherwise you get an index error at token `block_size + 1` |
| Leaving dropout on during generation | Sampling is a separate function and the mode switch is easy to forget | `self.eval()` at the top of `generate`, `self.train()` at the end. With dropout 0.1 left on, every generated character is computed with a randomly damaged network |
| Judging the model on train loss | Train loss falls smoothly and looks great all the way to 0.15 | Track validation loss. In this run train went 1.71 → 0.15 while validation went 1.76 → 1.37 → **1.66**. The model got worse for 1,500 steps while its train loss looked wonderful |

---

## 🛠️ Mini-Project: Tiny GPT

**Time:** ~8 hours

### Goal

Build attention, multi-head attention, a transformer block, and a complete GPT in PyTorch — from `nn.Linear` upwards, no `nn.MultiheadAttention`, no `nn.TransformerEncoder`. Train it on a corpus you type yourself, show three checkpoints of it learning, and produce an attention heatmap you can actually interpret.

### Starter steps

1. **Write your own corpus.** 5,000–15,000 characters, lowercase, minimal punctuation, typed by you. Pick something with strong internal repetition — recipes, a rulebook, match commentary, a made-up mythology, two-character dialogue. Repetition is what makes a corpus this small learnable. **Do not download a file.**

2. **Build it bottom-up, asserting at each stage** (do not write the whole thing then debug): `Head` on `(1,5,128)` random input → output `(1,5,32)`, `last_attn` rows sum to 1, upper triangle exactly 0. `MultiHeadAttention` → `(1,5,128)`. `Block` → output shape equals input shape. `TinyGPT` untrained → loss within 0.05 of `ln(vocab_size)`. Finally, **overfit 8 examples** (the Module 1 sanity check); if the loss will not go near 0 on a batch you repeat, stop and find the bug.

3. **Train with the Module 1 recipe.** AdamW, `lr = 3e-4`, `weight_decay = 0.1`, 100 warmup steps then cosine decay, `clip_grad_norm_(1.0)`. Track train and validation loss every 100 steps and **save the best-validation checkpoint**.

4. **Capture three checkpoints of learning.** Generate 200 characters at step 0, at roughly one-eighth of training, and at the best-validation step. Paste all three verbatim; the reader should see noise → word-shaped → sentence-shaped without being told.

5. **Plot the loss curve.** Train and validation on shared axes, best-validation step marked with a vertical line, and a sentence on what happens after that line.

6. **Visualize and interpret one head.** Use a 30–40 character prompt from your domain, with your characters as tick labels. Write three sentences: what the black triangle proves, what the bright first column means, and what your head appears to track — backing the last claim with top-5 attended positions for two different query positions.

7. **Report the head statistics table** for all `n_layer × n_head` heads (mean look-back, self-weight) and state whether look-back increases with depth in *your* model.

### Success criteria checklist

- [ ] Attention implemented from scratch — no PyTorch attention modules anywhere
- [ ] All five build-stage assertions pass, and you can show them (including untrained loss within 0.05 of `ln(vocab_size)`)
- [ ] Three generated samples showing clear progression, pasted verbatim
- [ ] Generated text at the best checkpoint is **readable**: recognizable words, plausible grammar, sentence boundaries
- [ ] A loss curve with both train and validation, and the best step marked
- [ ] An attention heatmap with character tick labels and a black upper triangle
- [ ] A written interpretation of one head backed by top-5 numbers, not vibes, plus the head statistics table for every head
- [ ] An honest paragraph on memorization: your parameter count, your character count, their ratio, and evidence for or against verbatim recall

### Level it up

Pick one. **(a) KV caching** — generation currently re-runs the whole context per token (`O(T²)` for a full generation). Cache each layer's keys and values, appending one column per step. Measure tokens/second before and after at `T = 64`, and confirm the output is **identical** with a fixed seed; if it is not, your cache is wrong. **(b) Weight tying** — set `self.head.weight = self.tok_emb.weight` so the input embedding and output projection share one matrix (standard in GPT-2). Report parameter count and validation loss before and after, and explain why one matrix can sensibly serve both roles. **(c) Scaling study** — train `n_layer ∈ {1, 2, 4, 8}` at fixed everything else and plot best validation loss against parameter count on log-log axes. That is your own miniature scaling law, which is precisely where Module 4 begins.

---

## 🔑 Key Takeaways

- **Attention is a soft dictionary lookup.** Compare a query to every key, softmax the comparisons into weights, return the weighted average of the values. Every step is differentiable, which is why it can be learned.
- **Q, K, V are three different learned projections of the same tokens.** Keeping "what I am looking for" separate from "what I have to offer" is what makes self-attention expressive.
- **Divide by `√d_k` or the softmax saturates.** At `d_k = 64` the raw score standard deviation is 8; scores like `[8, −2, 1]` give weights `[0.999, 0.00005, 0.0009]` and the gradient dies.
- **Causal masking sets future scores to −∞ *before* the softmax.** It prevents label leakage and it is what makes a transformer generative — and it gives you T training signals per forward pass.
- **Multi-head attention is free.** Splitting `d_model` into `h` chunks costs the same parameters as one big head and lets each head specialize. Measured in the trained model: look-back grows 3.64 → 7.35 characters from layer 0 to layer 3.
- **Attention is permutation-blind**, so position must be added explicitly — a learned table or a sinusoidal clock.
- **A transformer block is `x = x + attn(ln(x))` then `x = x + mlp(ln(x))`.** Attention gathers information across positions; the MLP thinks about it within a position. Residual + pre-norm from Module 1 are what let you stack 96 of them.
- **The path from token 1 to token T is one operation, not T.** That is the entire difference from Module 2, and the price is `O(T²)` compute and memory.
- **807,196 parameters on 6,972 characters memorizes.** Validation loss bottomed at 1.328 and rose to 1.682 while train loss fell to 0.148. The fix is data, and that is Module 4.

---

## 📓 Vocabulary

| Term | Plain definition | Example |
|---|---|---|
| **Attention** | A soft lookup: compare a query to all keys, softmax into weights, return the weighted average of values | Scores `[0.1, 2.0, 0.3]` → weights `[0.112, 0.751, 0.137]` |
| **Query / Key / Value** | Three learned projections of a token: what it wants, what it advertises, what it contributes | `Q = X·W_Q`, `K = X·W_K`, `V = X·W_V` |
| **Self-attention** | Attention where the queries, keys, and values all come from the same sequence | Every token attends over its own sentence |
| **Attention scores** | The `(T, T)` matrix of query·key dot products before softmax | Entry (3,1) = how much token 3 wants token 1 |
| **Scaling by √d_k** | Dividing scores by the square root of head dimension to keep score variance at 1 | `√64 = 8`; without it softmax saturates |
| **Causal mask** | Setting scores for future positions to −∞ before the softmax | `torch.tril(torch.ones(T,T))`, then `masked_fill(..., -inf)` |
| **Label leakage** | Letting the model see the answer it is supposed to predict | Unmasked attention gives near-zero loss and useless generation |
| **Multi-head attention** | Split `d_model` into h chunks, attend independently in each, concatenate, project | 128 dims / 4 heads = 32 dims per head; same parameter count |
| **Output projection (W_O)** | The linear layer after concatenating heads, which blends their outputs | `nn.Linear(n_embd, n_embd)` |
| **Positional encoding** | Information about position added to every token vector | `x = tok_emb(idx) + pos_emb(arange(T))` |
| **Learned positional embedding** | A trainable table with one row per position | `nn.Embedding(block_size, n_embd)`; cannot exceed `block_size` |
| **Sinusoidal encoding** | A fixed pattern of sines and cosines at geometric frequencies | `sin(pos/10000^(2i/d))`; extends past training length |
| **Feed-forward network (FFN)** | A per-position 2-layer MLP with 4× expansion; holds most of the parameters | `Linear(128,512) → GELU → Linear(512,128)` |
| **Transformer block** | Attention + MLP, each wrapped in pre-norm and a residual connection | `x = x + attn(ln1(x)); x = x + ff(ln2(x))` |
| **Pre-norm** | Applying layer norm inside the residual branch rather than after the addition | `x + attn(ln(x))`, not `ln(x + attn(x))` |
| **Permutation equivariance** | Shuffling the inputs shuffles the outputs identically — no position awareness | Why a transformer needs positional encodings and an RNN does not |
| **Context window / block size** | The maximum number of tokens the model can attend over | `BLOCK = 64` here; `idx[:, -block_size:]` enforces it |
| **Attention sink** | Many queries putting weight on position 0 regardless of content | Shows up as a bright first column in the heatmap |
| **KV cache** | Storing past keys and values so generation does not recompute the whole context | Turns `O(T²)` generation into `O(T)` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Attention by hand, again

**Why the weights are unchanged:** the attention weight matrix is `softmax(QKᵀ/√d_k)` with the causal mask. It depends only on `Q` and `K`, which depend only on `X`, `W_Q`, `W_K`. `W_V` appears nowhere in that expression — it only affects what gets averaged, not how the averaging is weighted. So we reuse:

```
           the     cat     sat
 the   [ 1.0000  0.0000  0.0000 ]
 cat   [ 0.3302  0.6698  0.0000 ]
 sat   [ 0.2483  0.2483  0.5035 ]
```

**Compute the new V.** `W_V = [[2,0],[0,3]]` scales the first component by 2 and the second by 3.

- `v₁ = [1,0]·W_V = [1(2)+0(0), 1(0)+0(3)] = [2, 0]`
- `v₂ = [0,1]·W_V = [0(2)+1(0), 0(0)+1(3)] = [0, 3]`
- `v₃ = [1,1]·W_V = [1(2)+1(0), 1(0)+1(3)] = [2, 3]`

**Output row 1:** `1.0000·[2,0]` = **[2.0000, 0.0000]**

**Output row 2:** `0.3302·[2,0] + 0.6698·[0,3]`
- first: `0.3302(2) + 0.6698(0) = 0.6604`
- second: `0.3302(0) + 0.6698(3) = 2.0094`
- = **[0.6604, 2.0094]**

**Output row 3:** `0.2483·[2,0] + 0.2483·[0,3] + 0.5035·[2,3]`
- first: `0.4966 + 0 + 1.0070 = 1.5036`
- second: `0 + 0.7449 + 1.5105 = 2.2554`
- = **[1.5036, 2.2554]**

Sanity check: every output should lie inside the convex hull of `[2,0]`, `[0,3]`, `[2,3]`. First components are all in [0, 2] ✓; second components all in [0, 3] ✓.

### 2. [Warm-up] Break the mask on purpose

Comment out `att = att.masked_fill(...)` and train 500 steps.

**What you will see:** train and validation loss both collapse to something very small. Real run (500 steps): validation 0.166 at step 250 and **0.066 at step 499** (train 0.067). That is far below the masked model's 1.226 at step 500, and far below the true entropy of English text.

**Generated output:** garbage. In the real run it was `tttttttttttttttt...`, one repeated character, no words, nothing resembling the corpus.

**The explanation paragraph:**

The loss is low because the task became trivial, not because the model became good. Position `t` must predict `targets[t]`, which is `data[t+1]`. Without the mask, position `t` attends over the *entire* input window — and `inputs[t+1]` **is** `data[t+1]`. The answer sits in the input at a fixed offset of one, so the model only has to learn "copy the token one to my right," which a single head expresses perfectly with a positional-offset pattern.

This is **label leakage**: the target is recoverable from the input. It produces the classic dangerous signature — excellent on every metric you track, useless in deployment. Generation exposes it immediately, because at generation time there *is* no token to the right; the copy strategy has nothing to copy, so the model emits noise.

The general lesson: **any time your loss drops far below what you expected, suspect leakage before you celebrate.** Compute the theoretical floor for your task first (character-level English is roughly 1.0–1.5 nats/char) and treat anything well below it as a bug report.

### 3. [Build] Ablate every component

```python
# run each config for 1500 steps, tracking BEST validation loss
```

Real results (CPU, 1,500 steps each, best validation loss checked every 50 steps, one seed; the mask-break probe ran 500 steps). Treat differences under about 0.05 as noise: we did not run multiple seeds.

| # | Config | best val loss | Δ vs baseline |
|---|---|---|---|
| baseline | full model | **1.278** (step 750) | — |
| 2 | 1 head | 1.269 (step 700) | -0.009 (no change) |
| 6 | 1 layer | 1.271 (step 1450) | -0.007 (no change) |
| 3 | no MLP | 1.452 (step 1250) | +0.174 |
| 1 | no positional embedding | 1.632 (step 600) | +0.354 |
| 5 | no √d_k scaling | **1.245** (step 600) | -0.033 (no change, nominally the best) |
| 4 | no residuals | 2.848 (step 850) | +1.570 |

**Mechanisms, one per ablation:**

- **No positional embedding (+0.354).** The model becomes permutation-blind — it learns character frequencies but cannot distinguish `the` from `teh`. It does not collapse completely, because the causal mask leaks a little positional information (position `t` has exactly `t+1` visible keys). That partial leak is a genuinely interesting finding.
- **One head (-0.009: no measurable damage).** With a 28-character vocabulary and 32-character context, one head (`d_k = 128`) does as well as four. Multi-head attention is a capacity and specialization argument that this tiny task does not test. Whether the gap widens on a larger vocabulary and longer context is untested here.
- **No MLP (+0.174).** Attention barely computes; it averages. Removing the MLP also removes about two-thirds of the parameters, so part of this gap is capacity rather than architecture.
- **No residuals (+1.570).** Final train 2.843 and val 2.849: the model barely learned (the unigram-like regime) and never got going. Without the gradient highway four blocks was enough to stall it, and pre-norm without a residual is worse than useless. This is Module 1's `1 + f'(x)` argument, and it is by far the most damaging of the six. (Caveat from Module 1: a plain 12-block *MLP* trained fine with AdamW, so depth alone is not the cause; the transformer's attention path appears to need the residual.)
- **No scaling (-0.033: did not reproduce the predicted damage).** Theory says that at `d_k = 32` the score standard deviation is `√32 ≈ 5.7`, so the softmax can run near-saturated. In this run, removing the scaling gave the *lowest* best validation loss of all (1.245), with a slightly earlier overfit (final train 0.278, final val 1.352 vs baseline 1.336). With weights initialized at std 0.02 the raw scores start tiny, so the saturation story is not supported at this size; we did not measure softmax saturation directly and did not run several seeds, so the claim that scaling matters is **not shown here** (it is argued from the literature at larger `d_k`).
- **One layer (-0.007: no measurable damage).** Here the compositional hierarchy did not matter for the score; the one-layer model's best val (1.271) matched the baseline (1.278), although it fit the training set less (final train 0.869 vs 0.411). The look-back grew — look-back grew from 3.64 to 7.35 characters across the four layers in the baseline, which shows the layers *use* different ranges, not that the range is needed for this score.

**Biggest damage:** removing residual connections (+1.570), then positional embeddings (+0.354), then the MLP (+0.174). Most people predict positional embeddings, because that ablation is more conceptually dramatic. The residual result is a reminder that **optimization failures usually beat representational failures**. And the three "no change" rows (1 head, 1 layer, no scaling) are the honest part of the lesson: on a tiny task, components that matter at scale may not show up, so an ablation that finds nothing is a result about the task, not proof the component is useless.

### 4. [Build] Batched multi-head attention

```python
class MultiHeadAttentionFast(nn.Module):
    def __init__(self, n_embd, n_head, block, dropout):
        super().__init__()
        assert n_embd % n_head == 0
        self.n_head, self.n_embd = n_head, n_embd
        self.qkv = nn.Linear(n_embd, 3 * n_embd, bias=False)
        self.proj = nn.Linear(n_embd, n_embd)
        self.attn_drop = nn.Dropout(dropout)
        self.resid_drop = nn.Dropout(dropout)
        self.register_buffer("tril", torch.tril(torch.ones(block, block))
                                          .view(1, 1, block, block))

    def forward(self, x):
        B, T, C = x.shape
        hs = C // self.n_head
        q, k, v = self.qkv(x).split(C, dim=2)                    # 3 x (B,T,C)
        q = q.view(B, T, self.n_head, hs).transpose(1, 2)        # (B,nh,T,hs)
        k = k.view(B, T, self.n_head, hs).transpose(1, 2)
        v = v.view(B, T, self.n_head, hs).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * hs ** -0.5             # (B,nh,T,T)
        att = att.masked_fill(self.tril[:, :, :T, :T] == 0, float("-inf"))
        att = self.attn_drop(F.softmax(att, dim=-1))
        y = att @ v                                              # (B,nh,T,hs)
        y = y.transpose(1, 2).contiguous().view(B, T, C)         # re-merge heads
        return self.resid_drop(self.proj(y))
```

**Equivalence test.** The loop version has one `key`/`query`/`value` linear per head, each `(hs, n_embd)`. The fast version has one `(3*n_embd, n_embd)`. Stack the per-head weights in the order q-all-heads, k-all-heads, v-all-heads:

```python
torch.manual_seed(0)
slow = MultiHeadAttention(128, 4, 64, 0.0).eval()
fast = MultiHeadAttentionFast(128, 4, 64, 0.0).eval()
with torch.no_grad():
    qw = torch.cat([h.query.weight for h in slow.heads], dim=0)   # (128,128)
    kw = torch.cat([h.key.weight   for h in slow.heads], dim=0)
    vw = torch.cat([h.value.weight for h in slow.heads], dim=0)
    fast.qkv.weight.copy_(torch.cat([qw, kw, vw], dim=0))         # (384,128)
    fast.proj.weight.copy_(slow.proj.weight)
    fast.proj.bias.copy_(slow.proj.bias)

x = torch.randn(2, 40, 128)
with torch.no_grad():
    a, b = slow(x), fast(x)
print("max abs diff:", (a - b).abs().max().item())
assert torch.allclose(a, b, atol=1e-5)
print("equivalent")
```

Expected: a difference around 1e-6 or smaller (real run: exactly `0.0`), and the assertion passes.

**Timing.** Warm up once, then time 100 forward passes of each on `torch.randn(32, 64, 128)` with `time.perf_counter()`.

**Real result on 2 CPU threads, shape (32, 64, 128):** the batched version was *slower*, not faster: loop 0.162 s vs batched 0.207 s per 100 forward passes, a speedup of **0.78x** (three runs: 0.78x, 0.78x, 0.81x; one run under load showed 1.07x). Both do the same FLOPs. The textbook argument is that batching removes kernel-launch overhead and improves memory locality, but on this CPU, with this size, the extra `transpose`/`contiguous` copies cost more than the launches saved. The speed advantage of batching is a GPU effect we could not measure here; do not expect it on a CPU. Time your own machine before believing either story.

Two things that catch people out: the `.contiguous()` before `.view()` is required because `.transpose()` produces a non-contiguous tensor; and the mask buffer needs the two leading singleton dimensions (`view(1,1,block,block)`) to broadcast against `(B, nh, T, T)`.

### 5. [Stretch] Sinusoidal versus learned positions

```python
def sinusoidal(max_len, d):
    pe = torch.zeros(max_len, d)
    pos = torch.arange(max_len).unsqueeze(1).float()
    div = torch.exp(torch.arange(0, d, 2).float() * (-math.log(10000.0) / d))
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe

class SinGPT(TinyGPT):
    def __init__(self, vocab, **kw):
        super().__init__(vocab, **kw)
        del self.pos_emb
        self.register_buffer("pe", sinusoidal(4096, self.tok_emb.embedding_dim))
        # FIX: each Head built a (block x block) causal mask, so any input longer
        # than BLOCK fails with a shape error. Enlarge the masks (cheap: 128 x 128).
        for b in self.blocks:
            for h in b.attn.heads:
                h.tril = torch.tril(torch.ones(128, 128))

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pe[:T].to(idx.device)
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                   targets.reshape(-1))
        return logits, loss
```

Note the buffer is built for 4096 positions even though training uses 32 — free, since it is a formula rather than parameters.

**Real results** after training both for 1,500 steps at `BLOCK = 32` (loss on validation windows of the stated length):

| eval length | learned | sinusoidal |
|---|---|---|
| 32 | 1.228 | 1.383 |
| 48 | **IndexError** | 1.866 (with the mask fix above) |
| 64 | **IndexError** | 2.220 (with the mask fix above) |

**Without the mask fix, `SinGPT` also crashes** at length 48 and 64: `RuntimeError: The size of tensor a (32) must match the size of tensor b (48) at non-singleton dimension 2`, because each `Head.tril` is only 32 x 32. The first draft of this exercise did not have that fix and could not have produced the numbers it quoted.

**The exact failure mode of the learned version:** `self.pos_emb` is `nn.Embedding(32, 128)`, so `torch.arange(48)` produces index 32, which is out of range for a 32-row table. On CPU you get `IndexError: index out of range in self`; a crash is the good outcome (some accelerator back ends fail silently instead). The `TinyGPT.generate` method dodges this entirely with `idx[:, -self.block_size:]`, but that is a truncation, not an extension: the model still sees only 32 tokens no matter how long the prompt is.

**Is the sinusoidal model's length-64 result usable?** Mostly no — loss rises from 1.383 at length 32 to 1.866 at 48 and 2.220 at 64. The model never *trained* on positions 32–63, so while those encodings are well-defined and distinct, no head has learned what to do with them. **Sinusoidal encodings give graceful degradation, not free extrapolation.** That distinction is why so much effort goes into schemes (RoPE with interpolation, ALiBi) that extend cleanly rather than merely not crashing. Honest caveat: with 698 validation characters the length-64 measurement has few independent windows, so the error bars are large — say so.

### 6. [Stretch] Find and name a head

```python
def head_stats(model, text_sample):
    idx = torch.tensor([encode(text_sample)], device=DEVICE)
    model.eval()
    with torch.no_grad():
        model(idx)
    T = len(text_sample)
    space_pos = [i for i, c in enumerate(text_sample) if c == " "]
    rows = []
    for li in range(N_LAYER):
        for hi in range(N_HEAD):
            a = model.blocks[li].attn.heads[hi].last_attn[0]      # (T,T)
            pos = torch.arange(T, device=a.device).float()
            look = (((pos.unsqueeze(0) - pos.unsqueeze(1)).abs() * a)
                    .sum(-1)[5:].mean().item())
            prev = a.diagonal(-1).mean().item()                   # weight on t-1
            first = a[:, 0].mean().item()                         # weight on pos 0
            sp = 0.0
            for qi in range(5, T):
                prior = [s for s in space_pos if s < qi]
                if prior:
                    sp += a[qi, prior[-1]].item()
            sp /= max(1, T - 5)
            rows.append((f"L{li}H{hi}", look, prev, first, sp))
    print(f"{'head':6s} {'lookback':>9s} {'prev':>7s} {'pos0':>7s} {'lastspace':>10s}")
    for r in rows:
        print(f"{r[0]:6s} {r[1]:9.2f} {r[2]:7.3f} {r[3]:7.3f} {r[4]:10.3f}")
    return rows

rows = head_stats(model, "the old man walked home along the river tonight")
```

**A head card** whose evidence numbers (Evidence 1 and 2) are measured from the real model on the sentence `the old man walked home along the river tonight`; Evidence 3 and the failure case below are **illustrative, not measured**. Yours will name a different head — that is fine, the format is what is being graded:

> ### Head card — `L0H3`, "the previous-character head"
>
> **Claim:** this head puts most of its weight on the immediately preceding character, acting as a one-step delay line that lets the layer above see bigrams.
>
> **Evidence 1.** Lowest mean look-back of all 16 heads: **3.48 characters** versus a model-wide mean of 7.57.
> **Evidence 2.** Mean weight on the diagonal-minus-one (position `t−1`) is **0.268**, the highest of all 16 heads and roughly 4× what uniform attention over a 17-character visible prefix would give (1/17 = 0.06).
> **Evidence 3 (illustrative, not measured).** Top-5 for query position 20 in `the old man walked home along the river`: positions 19, 18, 20, 17, 0 — a contiguous local window plus the attention sink.
>
> **Where the claim fails (illustrative, not measured).** On a query that lands immediately after a newline, the previous-character weight collapses to about 0.08 and weight shifts to position 0. At a sentence boundary the "previous character" is a newline, which carries almost no information about the next word, so the head abandons its usual strategy. So the accurate claim is narrower: *this head tracks the previous character **within** a line*, not unconditionally.

**Grading yourself:** a head card without a failure case is not finished — interpretability claims that cite only supporting examples are how people convince themselves a head does something it does not. Also note that 16 heads × 4 statistics is 64 numbers, so *something* will look extreme by chance. Before naming a head, check the pattern survives on a second, different prompt. If it does not, you found noise.

</details>

## 🧾 Patch log (offline redesign, 2026-10)

Ground truth: `36-week-course/_ledger/ledger-m01-04.md` and its `out/` files (CPU, `manual_seed(1337)`). The model structure (807,196 parameters, 6972 chars, overfit U-curve) matched and is unchanged.

- Setup: removed `pip install`; removed CUDA/MPS branch (`DEVICE = "cpu"`); "faster with CUDA or MPS" removed; "device mps" in expected output → cpu; "roughly 2 minutes" → measured 133 s on 2 threads.
- Expected output: every loss line (step 300 1.705/1.761 → 1.722/1.779; 500 → 1.226/1.410; 1000 → 0.445/1.328; 1200 → 0.301/1.451; 1500 → 0.212/1.589; 2000 → 0.159/1.664; 2499 → 0.148/1.682; FINAL 0.146/1.644 → 0.150/1.669) and all four samples replaced by the real ones; reading-the-output prose re-quoted (step 2499 is verbatim corpus after the first near-miss sentence); validation series → 3.339, 1.779, 1.328, 1.451, 1.664, 1.682.
- Head statistics: look-back table 3.66/6.94/7.26/8.26 → 3.64/6.75/7.21/7.35 (all 16 cells replaced from the real run); "L3 is 8.3" prose → 7.35; top-5 for `g` → real weights (0.204/0.162/0.156/0.076/0.062); L0H0..L3H3 sample lines updated; Key Takeaway and ablation text updated.
- Mask-break probe: "under 0.1, often under 0.05" → 0.166 at step 250, 0.066 at step 499; masked baseline 1.206 → 1.226; generated output → `tttt...`.
- Ablation table: 1 head 1.34 → 1.269; 1 layer 1.52 → 1.271; no MLP 1.58 → 1.452; no pos 1.85 → 1.632; no scaling "1.9-2.4 unstable" → 1.245 (best of all); no residuals 2.3 → 2.848. Mechanism bullets rewritten: 1 head, 1 layer, no scaling are "no measurable damage / did not reproduce"; "scaling saturates the softmax and diverges" is now marked not shown by this run; biggest damage (residuals) kept and reinforced; single seed caveat added.
- Batched attention: "2-4x faster on CPU" → 0.78-0.81x (slower) with real timings; equivalence diff `0.0`.
- Sinusoidal: code crashed at length 48/64 (mask buffer 32x32) → added a mask-enlarging fix to `SinGPT.__init__`; table 1.40/1.42/1.55/1.68 → learned 1.228, sinusoidal 1.383 / 1.866 / 2.220; CUDA remark removed.
- Head card: representative L0H2 (3.44, 6.5, 0.31) → measured L0H3 (3.48, 7.57, 0.268); Evidence 3 and the failure case are labelled illustrative, not measured.
- Not reproduced / unverified: the heatmap description (attention sink etc.) and the GPT-2 tokens-per-parameter figures are literature or illustrative and were not run here.

---

[⬅ Previous](module-02-sequence-models.md) · [Level 4 Home](README.md) · [Next ➡](module-04-how-llms-are-trained.md)
