# Module 4 — How LLMs Are Actually Trained: Pretraining, SFT, and RLHF

[⬅ Previous](module-03-attention-and-transformers.md) · [Level 4 Home](README.md) · [Next ➡](module-05-prompt-engineering.md)

**Level 4 · Module 4 · ~6 hours · Prereqs: Module 3 (transformer block, causal masking, next-token cross-entropy, sampling), Module 1 (AdamW, warmup+cosine, loss curves), comfort with logs, softmax, and scientific notation**

---

## 🎯 What You'll Be Able To Do

- **Implement byte-pair encoding from scratch** — training, encoding, and decoding — and prove your tokenizer round-trips arbitrary text exactly.
- **Explain in concrete numbers why subword tokens beat both words and characters**, and compute how vocabulary size trades off against sequence length and embedding parameters.
- **Describe the pretraining objective, the data pipeline, and the compute budget** of a real model using the `C ≈ 6ND` rule and the Chinchilla token-to-parameter ratio.
- **Explain supervised fine-tuning, reward modelling, and RLHF/DPO as three genuinely different learning signals**, and implement a working reward model and a working DPO update.
- **Distinguish a base model from an instruct model from a reasoning model** by behaviour alone, and name the training stage responsible for the difference.

---

## 🪝 The Hook

At the end of Module 3 your tiny GPT wrote things like `the man walked home along the river`. It has maybe 200,000 parameters and it saw maybe 100,000 characters of text. A frontier model has on the order of 10¹¹ parameters and has seen on the order of 10¹³ tokens.

That is a factor of about 500,000× in parameters and 100,000,000× in data. Big, but boring — it is the same architecture, the same loss, the same AdamW.

Here is the interesting part. If you *only* scaled up your Module 3 GPT, you would get something that **cannot follow an instruction**. Ask it "What is the capital of France?" and a pure scaled-up next-token predictor is entirely likely to answer:

```
What is the capital of France?
What is the capital of Germany?
What is the largest country in Europe?
```

Because that is what documents containing quiz questions look like. It is not being unhelpful. It is doing exactly what it was trained to do — continue the text.

Turning that into something that answers takes **three more training stages** after pretraining, each using a different kind of learning signal. This module is those four stages, in order, with the arithmetic and the code.

---

## 🧠 The Concept

Here is the whole module in one picture. Keep coming back to it.

```
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STAGE 0 · TOKENIZATION   (not learning — but it decides everything)  │
  │  raw bytes  ──BPE──▶  integer token ids                               │
  └───────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STAGE 1 · PRETRAINING            signal: the next token in the text  │
  │  ~10¹³ tokens of web text · months of GPU time · ~99% of total compute│
  │  RESULT: a BASE MODEL — knows the world, obeys nobody                 │
  └───────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STAGE 2 · SUPERVISED FINE-TUNING  signal: a human-written ideal reply│
  │  10³–10⁶ (prompt, response) demonstrations · hours to days            │
  │  RESULT: a model that answers instead of continuing                   │
  └───────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STAGE 3 · PREFERENCE MODELLING    signal: A is better than B         │
  │  10⁴–10⁶ human comparisons ──▶ a REWARD MODEL that scores any reply   │
  └───────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │  STAGE 4 · PREFERENCE OPTIMIZATION  signal: raise reward, stay near   │
  │  RLHF (PPO) or DPO · pushes probability toward preferred behaviour    │
  │  RESULT: an INSTRUCT MODEL — the thing you actually talk to           │
  └───────────────────────────────────────────────────────────────────────┘
```

---

### 1. Tokenizers: byte-pair encoding, vocabulary size, and token arithmetic

#### The problem

Your Module 3 GPT used **characters** as its unit. A frontier model does not. Why not? And why not whole words either?

Line them up on the sentence `The cricket team practised on Tuesday.` (38 characters):

| Unit | Vocabulary size | Tokens in this sentence | What breaks |
|---|---|---|---|
| **Characters** | ~100 | 38 | Sequences are 4× longer than they need to be. Attention costs O(T²), so 4× longer = 16× the attention compute. The model wastes layers relearning that `t`+`h`+`e` = "the". |
| **Words** | 170,000+ and still not enough | 7 | `practised` is not in the American-English vocab → `<UNK>`. Typos, code, URLs, Hindi, emoji → `<UNK>`. You cannot spell, so you cannot do arithmetic or reverse a string. |
| **Subwords (BPE)** | 32,000 – 200,000 | ~9 | Nothing. Common words are one token, rare words split into pieces, and *anything* can be represented. |

> **Tokenizer** — the piece of software that turns text into a list of integers (and back). It is not part of the neural network. It is trained separately, before pretraining, and then frozen forever.

#### 🍕 Analogy

Think about how you'd write down a takeaway order in shorthand. You would not spell out every letter (`p-i-z-z-a`) — too slow. You would not invent a symbol for every possible dish either — you'd run out of symbols the first time someone ordered something weird. You'd have short codes for the common things (`PZ` for pizza, `GB` for garlic bread) and you'd fall back to spelling for the unusual ones (`s-h-a-k-s-h-u-k-a`). That is exactly BPE: **frequent things get their own symbol; rare things get spelled out from pieces.**

#### How BPE works

> **Byte-pair encoding (BPE)** — start with an alphabet of the 256 possible bytes, then repeatedly find the most frequent adjacent pair of symbols in your corpus and glue it into a single new symbol. Each glue operation is called a **merge**. The list of merges, in order, *is* the tokenizer.

The algorithm in five lines:

```
vocabulary  = the 256 byte values
repeat (vocab_size - 256) times:
    count every adjacent symbol pair in the corpus
    pick the most frequent pair (a, b)
    create a new symbol ab, give it the next free id
    replace every occurrence of (a, b) with ab
```

Two properties matter enormously:

1. **It starts from bytes, so it can never fail.** Any text — Tamil, an emoji, a corrupted PDF, a base64 blob — is a sequence of bytes, so it always encodes. There is no `<UNK>`. Ever.
2. **It is deterministic and reversible.** Encode then decode returns the original text, byte for byte. You will prove this in the Hands-On.

#### Vocabulary size is a real engineering trade-off

Bigger vocabulary → fewer tokens per document → shorter sequences → cheaper attention. But bigger vocabulary → a bigger embedding table and a bigger output softmax.

Concrete numbers, for a model with `d_model = 768`:

| Vocab size `V` | Embedding params `V × d_model` | Output layer params `d_model × V` | Total tied to `V` |
|---|---|---|---|
| 8,192 | 6.3 M | 6.3 M | 12.6 M |
| 50,257 (GPT-2) | 38.6 M | 38.6 M | 77.2 M |
| 128,000 | 98.3 M | 98.3 M | 196.6 M |

`50257 × 768 = 38,597,376`. For a 124M-parameter model, the embedding table alone is 31% of the parameters. Push `V` to 128,000 and the embeddings would be larger than the transformer.

#### Token arithmetic — memorize these

For ordinary English prose:

```
1 token  ≈  4 characters  ≈  0.75 words
1,000 tokens  ≈  750 words  ≈  1.5 pages
```

Tiny worked example. A 2,400-word essay:

```
2,400 words ÷ 0.75 words/token = 3,200 tokens
```

At Claude Sonnet 5's input price of $2.00 per million tokens:

```
3,200 / 1,000,000 × $2.00 = $0.0064   (about two-thirds of a cent)
```

Non-English text and code are *worse* per character, because the tokenizer's merges were learned mostly on English. The same sentence in Hindi or Telugu can cost 2–4× the tokens. That is a real fairness issue and a real billing issue, and you will measure it yourself in the practice section.

---

### 2. Pretraining: next-token prediction at web scale

#### The objective has not changed at all

This is the same loss you wrote in Module 3:

```
loss = cross_entropy( model(tokens[:-1]) , tokens[1:] )
```

Average negative log-probability of the true next token. Nothing more. Every fact a base model "knows" is a side effect of the fact that knowing things helps you predict the next token.

#### 🍕 Analogy

Imagine reading every book in a library with the last word of every sentence covered, guessing it, then uncovering it to check. Do this a trillion times. To get good, you are *forced* to learn grammar, then facts, then arithmetic, then reasoning — not because anyone asked you to, but because each one lowers your guessing error. **Capability is a by-product of compression.**

#### The data pipeline is where most of the real work happens

Raw web crawl is mostly garbage. A realistic pipeline:

```
  ~100 TB raw Common-Crawl HTML
        │  1. extract text from HTML, drop boilerplate/nav/ads
        ▼  ~30 TB
        │  2. language ID — keep the languages you want
        ▼  ~12 TB
        │  3. quality filters — perplexity*, symbol ratio, line length,
        │                       "does this look like a real page?"
        ▼  ~5 TB
        │  4. DEDUPLICATION — exact + near-duplicate (MinHash)
        ▼  ~2 TB          ← often removes 50-70%
        │  5. safety / PII filtering
        ▼  ~1.8 TB
        │  6. MIXING — upweight books, code, Wikipedia, papers;
        │              downweight low-quality web
        ▼  the final training mixture, ~10-15 trillion tokens
```

> \* **Perplexity** — a score for how *surprised* a small reference language model is by a piece of text. Roughly, "how many equally-likely words was it choosing between at each step." Ordinary prose scores low; keyboard-mash, navigation menus and machine-generated spam score very high. Filtering on it is a cheap, fully automatic way to throw out pages no human wrote.

**Why deduplication is not optional.** Suppose one page is duplicated 1,000 times in your corpus. Three bad things happen at once:

1. The model memorizes it verbatim instead of generalizing — this is how training data gets regurgitated.
2. It silently eats your compute budget: those are 1,000 gradient steps spent learning one page.
3. If that page also appears in your evaluation set, your benchmark score is a lie. This is called **contamination**, and you will meet it again in Module 8.

Tiny concrete example. Take a 10-billion-token corpus in which 40% is near-duplicate. After dedup you have 6B unique tokens. If you train on the un-deduped 10B, roughly 4B of your gradient steps are re-teaching things the model has already seen — and the measured effect in published studies is *worse* held-out loss, not better. More data made the model worse. That is the whole argument for the dedup stage in one sentence.

#### The mixture matters as much as the size

Adding source code to the mixture measurably improves *non-code* reasoning. Nobody fully knows why; the leading guess is that code is long-range-structured text where a single wrong token breaks everything, so predicting it forces precise state tracking. Whatever the reason, mixture design is now a first-class research problem, not an afterthought.

---

### 3. Scaling laws, parameters, tokens, and compute budgets

#### The two numbers that define a training run

- **`N`** = number of parameters
- **`D`** = number of training tokens

And the rule of thumb that connects them to cost:

> **`C ≈ 6 N D`** — the total floating-point operations to train a transformer is about six times parameters times tokens.

Where does 6 come from? A forward pass costs about `2ND` (one multiply and one add per parameter per token). The backward pass costs about twice the forward pass, `4ND`. Total: `6ND`.

#### Worked compute budget

Train a 7-billion-parameter model on 1.4 trillion tokens:

```
C = 6 × 7×10⁹ × 1.4×10¹²
  = 6 × 9.8×10²¹
  = 5.88×10²²  FLOPs
```

An H100 GPU peaks around 10¹⁵ bf16 FLOP/s, but real training achieves roughly 40% of peak — call it `4×10¹⁴ FLOP/s` sustained.

```
time on ONE GPU = 5.88×10²² / 4×10¹⁴ = 1.47×10⁸ s
                = 1,701 days  ≈  4.7 years
on 1,024 GPUs   = 1.66 days
GPU-hours       = 1.47×10⁸ / 3600 = 40,830 GPU-hours
at $2/GPU-hour  ≈ $81,700
```

That is a *small* modern model. Multiply `N` by 50 and `D` by 10 and you are at 500× the cost. This is why there are not very many people training frontier models.

#### Scaling laws: how to spend a fixed budget

You have a fixed `C`. Do you train a big model on little data, or a small model on lots of data? **Scaling laws** answer this empirically: train many small models, measure loss as a function of `N` and `D`, fit a curve, extrapolate.

> **The Chinchilla result** — for a fixed compute budget, loss is minimized at roughly **`D ≈ 20 N`**: about 20 training tokens per parameter.

Check it against our example: `N = 7×10⁹`, so compute-optimal `D = 1.4×10¹²`. That is exactly the 1.4 trillion tokens above. Not a coincidence — that is where the number came from.

#### But nobody trains compute-optimally any more, and here is why

Chinchilla optimizes **training** cost. Real models get *served* billions of times. A smaller model trained on far more than 20 tokens/parameter costs more to train but is permanently cheaper and faster to run. So modern open models routinely use 100–300 tokens per parameter — deliberately "over-training" past the Chinchilla point to buy cheaper inference forever.

| Model style | `N` | `D` | tokens/param | Why |
|---|---|---|---|---|
| Chinchilla-optimal 7B | 7 B | 140 B | 20 | Cheapest possible training |
| Modern 8B open model | 8 B | 15 T | ~1,875 | Cheap inference matters more |
| Frontier 400B+ | 4×10¹¹ | 15 T | ~37 | Both matter; capability is the goal |

The lesson generalizes far beyond LLMs: **"optimal" is only meaningful once you say optimal *for what*.**

---

### 4. Stage 2 — Supervised fine-tuning on demonstration data

After pretraining you have a base model. It completes text. It does not answer.

**Supervised fine-tuning (SFT)** fixes this with the least clever idea imaginable: *show it thousands of examples of the behaviour you want, and keep using the same next-token loss.*

> **Supervised fine-tuning (SFT)** — continued next-token training on a curated dataset of (prompt, ideal response) pairs written or vetted by humans, where the loss is computed **only on the response tokens**.

#### The data looks like this

```json
{"prompt": "Explain photosynthesis to a 10-year-old.",
 "response": "Plants are tiny solar-powered kitchens. Their leaves catch sunlight..."}
{"prompt": "Write a Python function that reverses a list without using reverse().",
 "response": "def reverse_list(items):\n    return items[::-1]\n\n..."}
{"prompt": "What's the capital of France?",
 "response": "Paris."}
```

Wrapped in a **chat template** so the model can tell whose turn it is:

```
<|user|>
What's the capital of France?
<|assistant|>
Paris.<|end|>
```

Those `<|user|>` markers are ordinary tokens added to the vocabulary. This is the entire mechanism by which a model "knows" it is in a conversation. There is no conversation object. There is a string with special tokens in it.

#### The one non-obvious detail: loss masking

You compute loss **only on the assistant's tokens**. The prompt tokens are set to a label of `-100`, which PyTorch's `cross_entropy` skips.

Why? Because you are not trying to teach the model to *generate user questions*. You are teaching it: given this prompt, produce this response. Training on the prompt tokens wastes capacity and, worse, teaches it to imitate users — which is precisely the base-model failure from the Hook.

#### 🍕 Analogy and the numbers

SFT is teaching by worked example. Pretraining was reading the entire library; SFT is a tutor sitting down with 50,000 solved problems and saying "do it like this."

And it is *tiny* in comparison:

```
pretraining : ~1.5×10¹³ tokens
SFT         : ~5×10⁷ tokens   (50,000 examples × ~1,000 tokens)

ratio: SFT is 0.0003% of pretraining
```

Three ten-thousandths of one percent of the data changes the model from "text continuer" to "assistant". That tells you something important: **SFT is not teaching new knowledge. It is selecting a behaviour the base model could already produce.** The capability was already in there; SFT just makes it the default.

#### Where SFT stops working

To write an SFT example, a human has to produce the *ideal* answer. For "summarize this legal contract in 200 words," writing an excellent answer takes 40 minutes. But *judging* which of two summaries is better takes 30 seconds.

That gap — hard to produce, easy to judge — is the entire reason the next two stages exist.

---

### 5. Stages 3 and 4 — Preference data, reward models, RLHF, and DPO

#### Stage 3: turn comparisons into a scoring function

Show a human one prompt and two model responses. They pick the better one. You now have a **preference pair** `(prompt, chosen, rejected)`.

> **Reward model (RM)** — a model that takes a (prompt, response) and outputs a single number: how much a human would like this response. It is trained *only* from comparisons, never from absolute scores.

The trick that makes comparisons trainable is the **Bradley–Terry model**: assume the probability a human prefers response `w` over response `l` is

```
P(w ≻ l) = σ( r(w) − r(l) )        where σ(x) = 1 / (1 + e^(−x))
```

So the loss to minimize is

```
L_RM = − log σ( r(chosen) − r(rejected) )
```

**Tiny worked example.** Suppose your untrained RM scores `r(chosen) = 0.3` and `r(rejected) = 0.8` — backwards.

```
difference = 0.3 − 0.8 = −0.5
σ(−0.5)    = 1 / (1 + e^0.5) = 1 / (1 + 1.6487) = 0.3775
loss       = −log(0.3775) = 0.9741
```

After training pushes the gap to `+2.0`:

```
σ(2.0) = 1 / (1 + e^(−2.0)) = 1 / 1.1353 = 0.8808
loss   = −log(0.8808) = 0.1269
```

Loss dropped from 0.974 to 0.127. Notice the RM never learns "response X deserves a 7/10". It only ever learns *ordering*. The absolute scale is arbitrary — add 1000 to every reward and the loss is identical.

#### Stage 4a: RLHF with PPO

Now you have a scoring function, so you can generate *new* responses and score them. That is reinforcement learning.

```
      ┌──────────────┐  prompt   ┌───────────────┐
      │  prompt pool │──────────▶│  policy (LLM) │
      └──────────────┘           └───────┬───────┘
                                         │ sampled response
                                         ▼
                                 ┌───────────────┐
                                 │ reward model  │──▶ r
                                 └───────────────┘
                                         │
                          ┌──────────────┴─────────────┐
                          │  objective:                │
                          │  maximize  r − β·KL(π‖π_ref)│
                          └──────────────┬─────────────┘
                                         ▼
                                  PPO gradient step
```

> **RLHF (reinforcement learning from human feedback)** — sample responses from the model, score them with the reward model, and update the model to make high-scoring responses more likely, while a KL penalty keeps it from drifting far from the SFT model it started as.

**Why the KL penalty is mandatory.** Without it, the policy finds the reward model's blind spots — a phenomenon called **reward hacking**. Real observed failures: responses that always open with "Great question!" because that correlated with human approval; responses padded to 3× the useful length because longer answers won more comparisons; responses that agree with whatever the user asserted, because agreement felt good to raters. The reward model is a *proxy* for human preference, and any proxy optimized hard enough stops tracking the thing it proxies for. You will meet this again by its proper name — specification gaming — in Module 9.

The KL term `β·KL(π‖π_ref)` says: "you may improve, but you may not become a different model." `β` is the leash length.

#### Stage 4b: DPO, the same thing without the RL

PPO is genuinely painful: four models in memory (policy, reference, reward, value), unstable, hyperparameter-sensitive.

**Direct preference optimization (DPO)** is the observation that if your reward model is Bradley–Terry and your objective is reward-minus-KL, then the optimal policy has a closed form — and you can substitute it back in and *skip the reward model entirely*.

> **DPO** — train directly on preference pairs with a plain supervised loss that raises the log-probability of the chosen response and lowers the log-probability of the rejected one, measured **relative to a frozen reference model**.

```
L_DPO = − log σ( β · [ (log π(y_w|x) − log π_ref(y_w|x))
                     − (log π(y_l|x) − log π_ref(y_l|x)) ] )
```

Read it in plain words: *"the amount by which I have raised the winner above the reference should exceed the amount by which I have raised the loser, by a healthy margin."*

**Tiny worked example.** One preference pair, `β = 0.1`:

| | chosen `y_w` | rejected `y_l` |
|---|---|---|
| `log π_ref` | −20.0 | −18.0 |
| `log π` (current) | −19.0 | −19.5 |

```
chosen shift   = −19.0 − (−20.0) = +1.0
rejected shift = −19.5 − (−18.0) = −1.5
margin         = 0.1 × (1.0 − (−1.5)) = 0.1 × 2.5 = 0.25
loss           = −log σ(0.25) = −log(0.5622) = 0.5757
```

The reference model started out *preferring* the rejected response (−18.0 beats −20.0). DPO does not care about the absolute probabilities at all — it only cares that you moved the winner up relative to where the reference had it. That relative framing is exactly what replaces the KL penalty.

| | RLHF (PPO) | DPO |
|---|---|---|
| Reward model needed | Yes, trained separately | No |
| Models in memory | 4 | 2 (policy + frozen reference) |
| Needs on-policy sampling | Yes, every step | No — offline dataset |
| Stability | Fiddly | Behaves like ordinary supervised training |
| Can exceed the preference data | Yes (explores new responses) | No (bounded by the pairs you have) |

That last row is the real trade-off. PPO can discover responses no human wrote. DPO can only rank the ones you gave it.

---

### 6. Base vs instruct vs reasoning models, and what "emergent" really means

#### The three things people call "a model"

| | **Base** | **Instruct / chat** | **Reasoning** |
|---|---|---|---|
| Training stages | 1 | 1 + 2 + (3,4) | 1 + 2 + (3,4) + RL on verifiable tasks |
| Behaviour on "What is 17 × 23?" | may continue with more maths problems | "391." | thinks internally, then "391." |
| Refuses harmful requests | rarely | usually | usually |
| Good for | further fine-tuning, raw completion, research | almost everything | maths, code, multi-step planning |
| Cost per answer | lowest | low | higher (pays for hidden thinking tokens) |

A **reasoning model** is trained with an extra RL stage on tasks where correctness can be checked automatically — maths with known answers, code with unit tests. The reward is not a human preference model, it is `1 if the tests pass else 0`. That verifiable signal is what lets the model be trained to produce long internal reasoning before answering. This is why current Claude models expose adaptive thinking as an API feature rather than a prompt trick — you will use it in Module 5.

#### "Emergent abilities" — be careful with this phrase

The claim: some capabilities appear suddenly at a certain scale, absent below it, present above it.

The careful version: **the sharpness usually comes from the metric, not the model.** If you score multi-step arithmetic with exact match, a model that goes from getting 2 of 5 digits right to 5 of 5 looks like it jumped from 0% to 100%. Score it with per-digit accuracy instead and you see a smooth climb the whole way.

So:

- ✅ Fair to say: "at this scale the model crosses the threshold where this task becomes usable."
- ❌ Not fair to say: "capabilities appear from nowhere, so we cannot predict what a bigger model will do."

The second is a strong claim, it is used to justify both hype and doom, and the evidence for it is much weaker than the phrase suggests. When you read "emergent", ask what metric was used.

---

## 🔍 Worked Example

**Train a BPE tokenizer by hand, then use it.**

Corpus (10 words):

```
low low low low low lower lower widest widest widest
```

**Step 0 — pre-tokenize and count.** Split into runs of whitespace and runs of non-whitespace. Whitespace runs here are single spaces and have no internal pairs, so they contribute nothing.

| chunk | frequency | initial symbols (bytes) |
|---|---|---|
| `low` | 5 | `l` `o` `w` |
| `lower` | 2 | `l` `o` `w` `e` `r` |
| `widest` | 3 | `w` `i` `d` `e` `s` `t` |
| `" "` | 9 | (single symbol — no pairs) |

Byte values we will need: `d`=100, `e`=101, `i`=105, `l`=108, `o`=111, `r`=114, `s`=115, `t`=116, `w`=119.

**Step 1 — count every adjacent pair, weighted by chunk frequency.**

| pair | from `low`×5 | from `lower`×2 | from `widest`×3 | total |
|---|---|---|---|---|
| (`l`,`o`) | 5 | 2 | — | **7** |
| (`o`,`w`) | 5 | 2 | — | **7** |
| (`w`,`e`) | — | 2 | — | 2 |
| (`e`,`r`) | — | 2 | — | 2 |
| (`w`,`i`) | — | — | 3 | 3 |
| (`i`,`d`) | — | — | 3 | 3 |
| (`d`,`e`) | — | — | 3 | 3 |
| (`e`,`s`) | — | — | 3 | 3 |
| (`s`,`t`) | — | — | 3 | 3 |

Two pairs tie at 7. We need a deterministic tie-break, so use "smaller first byte wins": `l`=108 < `o`=111, so **(`l`,`o`) wins**.

**Merge 1: (108, 111) → id 256 = `lo`**

Corpus now: `lo w` ×5, `lo w e r` ×2, `w i d e s t` ×3.

**Step 2 — recount.**

| pair | total |
|---|---|
| (`lo`,`w`) | 5 + 2 = **7** |
| (`w`,`e`) | 2 |
| (`e`,`r`) | 2 |
| (`w`,`i`), (`i`,`d`), (`d`,`e`), (`e`,`s`), (`s`,`t`) | 3 each |

**Merge 2: (256, 119) → id 257 = `low`**

Corpus: `low` ×5, `low e r` ×2, `w i d e s t` ×3.

**Step 3 — recount.** Now the maximum is 3, tied five ways: (`w`,`i`)=(119,105), (`i`,`d`)=(105,100), (`d`,`e`)=(100,101), (`e`,`s`)=(101,115), (`s`,`t`)=(115,116). Smallest first byte is 100.

**Merge 3: (100, 101) → id 258 = `de`**

Corpus: `low` ×5, `low e r` ×2, `w i de s t` ×3.

**Step 4.** Pairs at count 3: (`w`,`i`)=(119,105), (`i`,`de`)=(105,258), (`de`,`s`)=(258,115), (`s`,`t`)=(115,116). Smallest first byte: 105.

**Merge 4: (105, 258) → id 259 = `ide`**

Corpus: `low` ×5, `low e r` ×2, `w ide s t` ×3.

**Step 5.** Pairs at 3: (`w`,`ide`)=(119,259), (`ide`,`s`)=(259,115), (`s`,`t`)=(115,116). Smallest first: 115.

**Merge 5: (115, 116) → id 260 = `st`**

Corpus: `low` ×5, `low e r` ×2, `w ide st` ×3.

**Step 6.** Pairs at 3: (`w`,`ide`)=(119,259), (`ide`,`st`)=(259,260). Smallest first: 119.

**Merge 6: (119, 259) → id 261 = `wide`**

**Step 7.** (`wide`,`st`) = 3.

**Merge 7: (261, 260) → id 262 = `widest`**

**Step 8.** Remaining pairs with count ≥ 2: (`low`,`e`)=2, (`e`,`r`)=2. Tie; `e`=101 < `low`=257.

**Merge 8: (101, 114) → id 263 = `er`**

**The finished merge list:**

| # | pair | new id | new symbol |
|---|---|---|---|
| 1 | (108, 111) | 256 | `lo` |
| 2 | (256, 119) | 257 | `low` |
| 3 | (100, 101) | 258 | `de` |
| 4 | (105, 258) | 259 | `ide` |
| 5 | (115, 116) | 260 | `st` |
| 6 | (119, 259) | 261 | `wide` |
| 7 | (261, 260) | 262 | `widest` |
| 8 | (101, 114) | 263 | `er` |

**Now encode a word the tokenizer has never seen: `lowest`.**

Encoding applies merges **in the order they were learned**, always taking the lowest-numbered applicable merge:

```
start:            l  o  w  e  s  t          (108 111 119 101 115 116)
merge 1 applies:  lo w  e  s  t             (256 119 101 115 116)
merge 2 applies:  low e  s  t               (257 101 115 116)
merge 3? (d,e) not present.
merge 4? (i,de) not present.
merge 5 applies:  low e  st                 (257 101 260)
merge 6? (w,ide) not present.
merge 7? no.  merge 8? (e,r) not present.
STOP.
```

**Result: `[257, 101, 260]` → `low` + `e` + `st` — three tokens for a word never seen in training.** This is the whole point of subwords. No `<UNK>`, and the pieces are meaningful ones the model has representations for.

**And decoding is trivial:** look up each id's bytes and concatenate. `b"low" + b"e" + b"st"` = `b"lowest"`. Exact.

---

## 💻 Hands-On

Everything here runs on CPU in under a minute. You need `torch` for parts C–E.

```bash
pip install torch
```

### Part A — Byte-pair encoding from scratch

Save as `bpe.py`.

```python
"""A complete, correct byte-level BPE tokenizer in about 60 lines."""
import re
from collections import Counter

# Split text into runs of whitespace and runs of non-whitespace.
# Key property: "".join(pretokenize(text)) == text, for ANY text.
# Pre-tokenizing stops merges from ever crossing a word boundary.
PRETOKEN_RE = re.compile(r"\s+|\S+")


def pretokenize(text):
    return PRETOKEN_RE.findall(text)


def merge_pair(ids, pair, new_id):
    """Replace every adjacent occurrence of `pair` in `ids` with `new_id`."""
    out, i = [], 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


class BPETokenizer:
    def __init__(self):
        self.merges = {}                                  # (id, id) -> new id
        self.vocab = {i: bytes([i]) for i in range(256)}   # id -> raw bytes

    def train(self, text, vocab_size, verbose=False):
        assert vocab_size >= 256, "vocab must include the 256 byte tokens"
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}

        # Work on UNIQUE chunks with counts — far faster than the raw stream.
        counts = Counter(pretokenize(text))
        words = [list(chunk.encode("utf-8")) for chunk in counts]
        freqs = list(counts.values())

        for m in range(vocab_size - 256):
            pair_counts = Counter()
            for word, f in zip(words, freqs):
                for p in zip(word, word[1:]):
                    pair_counts[p] += f
            if not pair_counts:
                break
            # Tie-break on smaller ids so training is fully deterministic.
            best, cnt = max(pair_counts.items(),
                            key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))
            if cnt < 2:
                break                                     # nothing left worth merging
            new_id = 256 + m
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            words = [merge_pair(w, best, new_id) for w in words]
            if verbose:
                print(f"merge {m + 1:3d}: {best} -> {new_id:4d}  "
                      f"{self.vocab[new_id]!r:14s} count={cnt}")
        return self

    def _encode_chunk(self, chunk):
        ids = list(chunk.encode("utf-8"))
        while len(ids) >= 2:
            pairs = set(zip(ids, ids[1:]))
            # Apply the EARLIEST-learned applicable merge, always.
            cand = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
            if cand not in self.merges:
                break
            ids = merge_pair(ids, cand, self.merges[cand])
        return ids

    def encode(self, text):
        out = []
        for chunk in pretokenize(text):
            out.extend(self._encode_chunk(chunk))
        return out

    def decode(self, ids):
        return b"".join(self.vocab[i] for i in ids).decode("utf-8", errors="replace")
```

Reproduce the worked example exactly:

```python
if __name__ == "__main__":
    tiny = "low low low low low lower lower widest widest widest"
    t = BPETokenizer().train(tiny, vocab_size=256 + 8, verbose=True)
    ids = t.encode("lowest")
    print(ids, [t.vocab[i] for i in ids])
```

**Expected output — identical to the hand trace above:**

```
merge   1: (108, 111) ->  256  b'lo'          count=7
merge   2: (256, 119) ->  257  b'low'         count=7
merge   3: (100, 101) ->  258  b'de'          count=3
merge   4: (105, 258) ->  259  b'ide'         count=3
merge   5: (115, 116) ->  260  b'st'          count=3
merge   6: (119, 259) ->  261  b'wide'        count=3
merge   7: (261, 260) ->  262  b'widest'      count=3
merge   8: (101, 114) ->  263  b'er'          count=2
[257, 101, 260] [b'low', b'e', b'st']
```

### Part B — Train on a real (small) corpus and measure compression

Save as `corpus.py`:

```python
CORPUS = """The cricket team practised on Tuesday. The cricket team practised again on Thursday.
Practice makes the team faster, and the team plays better when the team practises together.
The school library opened a new reading room. The reading room has thirty chairs and eight tables.
Students borrow books from the library every morning and return the books before evening.
Reading every day makes reading easier, and easier reading makes students read more.
The science club built a small weather station. The weather station measures temperature and rainfall.
Every morning a student records the temperature, and every evening a student records the rainfall.
The recorded temperature and the recorded rainfall go into a shared spreadsheet.
The spreadsheet shows that rainfall increased in June and temperature decreased in July.
The music room needs new speakers. The old speakers stopped working during the school concert.
The concert still happened because the choir sang without speakers, and the choir sang beautifully.
Teachers said the concert was the best concert of the year, and students agreed with the teachers.
"""
```

Then:

```python
from bpe import BPETokenizer, pretokenize
from corpus import CORPUS

print("characters:", len(CORPUS),
      " bytes:", len(CORPUS.encode("utf-8")),
      " pretokens:", len(pretokenize(CORPUS)))

tok = BPETokenizer().train(CORPUS, vocab_size=256 + 40, verbose=True)
ids = tok.encode(CORPUS)
print("token count:", len(ids),
      "  bytes/token:", round(len(CORPUS.encode("utf-8")) / len(ids), 3))
print("round-trip exact:", tok.decode(ids) == CORPUS)

for vs in [256, 306, 356, 456, 656]:
    t = BPETokenizer().train(CORPUS, vocab_size=vs)
    n = len(t.encode(CORPUS))
    print(f"vocab {vs:5d}  merges {len(t.merges):4d}  tokens {n:5d}  "
          f"bytes/token {len(CORPUS.encode('utf-8')) / n:.2f}")
```

**Expected output** (first 15 merges shown; the rest follow the same pattern):

```
characters: 1117  bytes: 1117  pretokens: 348
merge   1: (104, 101) ->  256  b'he'          count=34
merge   2: (101, 97) ->  257  b'ea'          count=27
merge   3: (105, 110) ->  258  b'in'          count=20
merge   4: (101, 114) ->  259  b'er'          count=19
merge   5: (116, 256) ->  260  b'the'         count=18
merge   6: (114, 101) ->  261  b're'          count=14
merge   7: (97, 110) ->  262  b'an'          count=12
merge   8: (84, 256) ->  263  b'The'         count=11
merge   9: (101, 100) ->  264  b'ed'          count=11
merge  10: (258, 103) ->  265  b'ing'         count=11
merge  11: (101, 110) ->  266  b'en'          count=10
merge  12: (114, 97) ->  267  b'ra'          count=10
merge  13: (115, 116) ->  268  b'st'          count=10
merge  14: (262, 100) ->  269  b'and'         count=10
merge  15: (114, 257) ->  270  b'rea'         count=9
...
merge  32: (277, 109) ->  287  b'team'        count=5
merge  33: (286, 116) ->  288  b'udent'       count=5
...
token count: 760   bytes/token: 1.47
round-trip exact: True

vocab   256  merges    0  tokens  1117  bytes/token 1.00
vocab   306  merges   50  tokens   720  bytes/token 1.55
vocab   356  merges  100  tokens   580  bytes/token 1.93
vocab   456  merges  138  tokens   504  bytes/token 2.22
vocab   656  merges  138  tokens   504  bytes/token 2.22
```

**Read those numbers carefully — three lessons are hiding in them.**

1. **The merges are not random; they are English.** `he`, `ea`, `in`, `er`, `the`, `ing`, `and`, `team`, `udent`. Nobody told the algorithm about morphemes. Counting adjacent pairs found them.
2. **Compression saturates.** At 138 merges training stops on its own, because no remaining pair appears twice. Asking for a 656-token vocabulary on a 1,117-byte corpus gets you the same 138 merges. **A tokenizer's vocabulary is limited by its training corpus, not by what you request.** Real tokenizers are trained on hundreds of gigabytes.
3. **2.22 bytes/token is bad.** GPT-2's tokenizer on this same text gets roughly 4.5 bytes/token — twice as good — because it was trained on 40 GB, not 1 KB.

#### Compare against a production tokenizer

```python
# pip install transformers
from transformers import AutoTokenizer
from bpe import BPETokenizer
from corpus import CORPUS

hf = AutoTokenizer.from_pretrained("gpt2")   # downloads ~1 MB the first time
mine = BPETokenizer().train(CORPUS, vocab_size=256 + 200)

for name, n in [("mine (138 merges)", len(mine.encode(CORPUS))),
                ("gpt2  (50k vocab)", len(hf.encode(CORPUS)))]:
    print(f"{name}: {n:4d} tokens   {len(CORPUS.encode('utf-8')) / n:.2f} bytes/token")

s = "Photosynthesis converts sunlight into chemical energy."
print("mine:", [mine.decode([i]) for i in mine.encode(s)])
print("gpt2:", [hf.decode([i]) for i in hf.encode(s)])
```

**Approximate expected output** (exact counts vary slightly by `transformers` version):

```
mine (138 merges):  760 tokens   1.47 bytes/token
gpt2  (50k vocab):  ~250 tokens  ~4.5 bytes/token

mine: ['P', 'h', 'o', 't', 'o', 's', 'y', 'n', 'the', 's', 'is', ' ', 'con', 'v', ...]
gpt2: ['Phot', 'osynthesis', ' converts', ' sunlight', ' into', ' chemical', ' energy', '.']
```

Note the difference in the *unseen* sentence: your tokenizer, which never saw the word "photosynthesis" or anything like it, falls apart into near-characters. GPT-2 handles it in two pieces. **Tokenizer quality on out-of-domain text is entirely a function of training-corpus breadth.**

Also notice `' converts'` — GPT-2 attaches the leading space to the word. Your `\s+|\S+` pre-tokenizer emits spaces as separate tokens instead. Both round-trip perfectly; GPT-2's choice is more compact because a leading space is so predictable.

#### Token arithmetic and a spending limit

```python
PRICE_IN_PER_MTOK = 2.00     # Claude Sonnet 5, USD per 1M input tokens
PRICE_OUT_PER_MTOK = 10.00   # USD per 1M output tokens

def cost(input_tokens, output_tokens):
    return (input_tokens / 1e6) * PRICE_IN_PER_MTOK + \
           (output_tokens / 1e6) * PRICE_OUT_PER_MTOK

print(f"one call  (12,000 in / 800 out): ${cost(12_000, 800):.4f}")
print(f"1,000 such calls               : ${cost(12_000, 800) * 1000:.2f}")

BUDGET = 5.00
print(f"calls affordable on ${BUDGET:.2f}: {int(BUDGET / cost(12_000, 800))}")
```

**Expected output:**

```
one call  (12,000 in / 800 out): $0.0320
1,000 such calls               : $32.00
calls affordable on $5.00: 156
```

Do this arithmetic *before* you write the loop, every single time. You will formalize it in Module 5.

### Part C — SFT loss masking, demonstrated

```python
import torch
import torch.nn.functional as F
torch.manual_seed(0)

V = 12                                    # pretend vocabulary size
logits = torch.randn(1, 9, V)             # pretend model output for 9 positions
tokens = torch.tensor([[3, 7, 2, 9, 11, 4, 4, 1, 6]])
PROMPT_LEN = 5                            # first 5 tokens are the prompt

preds = logits[:, :-1, :]                 # position t predicts token t+1
targets_all = tokens[:, 1:].clone()

loss_all = F.cross_entropy(preds.reshape(-1, V), targets_all.reshape(-1))

targets_sft = targets_all.clone()
targets_sft[:, :PROMPT_LEN - 1] = -100    # -100 == "ignore me"
loss_sft = F.cross_entropy(preds.reshape(-1, V),
                           targets_sft.reshape(-1), ignore_index=-100)

print("targets_all:", targets_all.tolist())
print("targets_sft:", targets_sft.tolist())
print(f"loss over all 8 predictions   : {loss_all.item():.4f}")
print(f"loss over 4 response positions: {loss_sft.item():.4f}")
```

**Expected output:**

```
targets_all: [[7, 2, 9, 11, 4, 4, 1, 6]]
targets_sft: [[-100, -100, -100, -100, 4, 4, 1, 6]]
loss over all 8 predictions   : 3.8008
loss over 4 response positions: 4.0407
```

Two different numbers from the same model on the same sequence. Only the second one is SFT. Getting this wrong is one of the most common fine-tuning bugs — see Module 8.

### Part D — Train a reward model with the Bradley–Terry loss

Real reward models are transformers with a scalar head. To see the *learning signal* clearly, we use a linear model over five hand-designed features. The loss is exactly the one used in production.

```python
import torch
import torch.nn.functional as F
torch.manual_seed(1)

FEATS = ["has_numbered_steps", "gives_direct_answer",
         "hedges_a_lot", "over_400_chars", "refuses"]

POOL = {                       # candidate responses as feature vectors
    "r1": [1, 1, 0, 0, 0],     # numbered steps, direct, concise
    "r2": [0, 1, 0, 0, 0],     # direct and concise, no structure
    "r3": [0, 1, 1, 1, 0],     # direct but hedgy and long
    "r4": [0, 0, 1, 0, 0],     # hedgy and evasive
    "r5": [0, 0, 0, 0, 1],     # refuses a harmless question
    "r6": [1, 1, 0, 1, 0],     # numbered steps, direct, but long
}

# Ten hand-made human judgements: (winner, loser)
PAIRS = [("r1", "r4"), ("r1", "r5"), ("r2", "r4"), ("r6", "r3"), ("r1", "r3"),
         ("r2", "r5"), ("r1", "r2"), ("r6", "r4"), ("r2", "r3"), ("r3", "r5")]

X = {k: torch.tensor(v, dtype=torch.float32) for k, v in POOL.items()}
w = torch.zeros(5, requires_grad=True)              # the reward model
opt = torch.optim.Adam([w], lr=0.1)

for step in range(1, 501):
    # Bradley-Terry: -log sigmoid( r(winner) - r(loser) )
    losses = [-F.logsigmoid(X[a] @ w - X[b] @ w) for a, b in PAIRS]
    loss = torch.stack(losses).mean()
    opt.zero_grad(); loss.backward(); opt.step()
    if step in (1, 100, 500):
        print(f"step {step:4d}  BT loss {loss.item():.4f}")

print("\nlearned reward weights:")
for f, wi in zip(FEATS, w.detach()):
    print(f"  {f:22s} {wi:+.3f}")

print("\nranking of every candidate:")
scores = {k: (X[k] @ w).item() for k in POOL}
for k, v in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {k}  reward {v:+.3f}   {POOL[k]}")

agree = sum(scores[a] > scores[b] for a, b in PAIRS)
print(f"\ntrain-pair agreement: {agree}/{len(PAIRS)}")
```

**Expected output:**

```
step    1  BT loss 0.6931
step  100  BT loss 0.0135
step  500  BT loss 0.0017

learned reward weights:
  has_numbered_steps     +5.047
  gives_direct_answer    +4.578
  hedges_a_lot           -2.794
  over_400_chars         -2.534
  refuses                -6.091

ranking of every candidate:
  r1  reward +9.625   [1, 1, 0, 0, 0]
  r6  reward +7.091   [1, 1, 0, 1, 0]
  r2  reward +4.578   [0, 1, 0, 0, 0]
  r3  reward -0.750   [0, 1, 1, 1, 0]
  r4  reward -2.794   [0, 0, 1, 0, 0]
  r5  reward -6.091   [0, 0, 0, 0, 1]

train-pair agreement: 10/10
```

Step 1's loss is `0.6931` = `−log(0.5)` = `log 2`, exactly as it must be when all rewards are zero.

**Now look at the weights as an attacker would.** `has_numbered_steps` is worth `+5.047`. So the single cheapest way to raise your reward is to *number everything*, regardless of whether the content is any good. Your feature set contains no term for correctness — because nobody could rate correctness in 30 seconds — so the reward model literally cannot tell truth from confident nonsense. Optimize hard against this and you get a model that writes beautifully formatted wrong answers. **That is reward hacking, and you just built it in 25 lines.**

### Part E — DPO on a toy policy

A full DPO run needs a language model. But DPO's *update rule* is visible in a four-outcome policy, which trains in a second.

```python
import torch
import torch.nn.functional as F

RESPONSES = ["A: numbered recipe, 6 lines, no filler",
             "B: correct recipe buried in 3 paragraphs of preamble",
             "C: vague answer that never lists ingredients",
             "D: refuses a harmless cooking question"]

# The frozen reference model (this is our "SFT model").
ref_logits = torch.tensor([0.4, 0.6, 1.2, 0.8])
ref_logp = F.log_softmax(ref_logits, dim=-1)

PAIRS = [(0, 3), (0, 2), (0, 1), (1, 2), (1, 3), (2, 3)]   # (chosen, rejected)


def run_dpo(beta, steps, lr=0.05, trace=False):
    policy_logits = torch.nn.Parameter(ref_logits.clone())
    opt = torch.optim.Adam([policy_logits], lr=lr)
    for s in range(1, steps + 1):
        logp = F.log_softmax(policy_logits, dim=-1)
        margins = torch.stack([
            beta * ((logp[w] - ref_logp[w]) - (logp[l] - ref_logp[l]))
            for w, l in PAIRS])
        loss = -F.logsigmoid(margins).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if trace and s in (1, 50, 150, 300):
            p = F.softmax(policy_logits, -1).detach()
            print(f"  step {s:4d}  loss {loss.item():.4f}   probs " +
                  " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)))
    p = F.softmax(policy_logits, -1).detach()
    kl = (p * (torch.log(p) - ref_logp)).sum()          # KL(policy || reference)
    return p, kl.item(), loss.item()


ref_p = torch.softmax(ref_logits, -1)
print("reference policy:", " ".join(f"{RESPONSES[i][0]}={ref_p[i]:.3f}" for i in range(4)))
print("\nbeta = 0.2, 300 steps:")
run_dpo(0.2, 300, trace=True)

print("\nbeta sweep, all at 300 steps:")
for b in [0.02, 0.1, 0.5, 1.0, 5.0]:
    p, kl, l = run_dpo(b, 300)
    print(f"  beta {b:4.2f}  " +
          " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)) +
          f"   KL(pi||ref)={kl:.3f}  loss={l:.4f}")
```

**Expected output:**

```
reference policy: A=0.168 B=0.206 C=0.375 D=0.251

beta = 0.2, 300 steps:
  step    1  loss 0.6931   probs A=0.179 B=0.219 C=0.361 D=0.242
  step   50  loss 0.4529   probs A=0.519 B=0.461 C=0.013 D=0.006
  step  150  loss 0.2526   probs A=0.946 B=0.054 C=0.000 D=0.000
  step  300  loss 0.1424   probs A=0.997 B=0.003 C=0.000 D=0.000

beta sweep, all at 300 steps:
  beta 0.02  A=0.782 B=0.218 C=0.000 D=0.000   KL(pi||ref)=1.213  loss=0.5317
  beta 0.10  A=0.997 B=0.003 C=0.000 D=0.000   KL(pi||ref)=1.760  loss=0.2560
  beta 0.50  A=0.987 B=0.013 C=0.000 D=0.000   KL(pi||ref)=1.709  loss=0.0513
  beta 1.00  A=0.950 B=0.047 C=0.003 D=0.000   KL(pi||ref)=1.557  loss=0.0204
  beta 5.00  A=0.589 B=0.236 C=0.144 D=0.032   KL(pi||ref)=0.566  loss=0.0020
```

**Three things to take away.**

1. **The reference model preferred C** (0.375) — the worst response. After DPO the policy puts essentially all its mass on A. Nobody ever told the model "A is correct"; it only ever saw six pairwise comparisons.
2. **Mode collapse is real.** At β=0.2 after 300 steps, B, C and D have probability ~0.000. A model that can only produce one response is not a good model. In a real DPO run this is what shows up as loss of diversity — every answer starts sounding the same.
3. **β controls how hard the loss pushes.** At β=5.0 a small logit gap already makes the margin large, `logsigmoid` saturates, the gradient dies, and the policy barely moves (KL 0.566). At β=0.02 the same logit gap barely registers, so the loss keeps pushing. Small β = long leash. This sweep holds *steps* fixed, so it mixes "how far DPO wants to go" with "how fast it gets there" — a good reminder that in preference tuning, when you stop is as much a hyperparameter as β is.

---

## ✍️ Practice

### [Warm-up] 1 — Token arithmetic on your own text

Take any 500+ word piece of writing you have (an essay, a README, a chat log). Encode it with your `BPETokenizer` trained on `CORPUS` from Part B, and with GPT-2's tokenizer. Report characters, your tokens, GPT-2 tokens, and bytes/token for each. Then compute what one Claude Sonnet 5 call containing this text as input would cost at $2.00 per million input tokens.

**Done looks like:** a five-row table and a dollar figure to four decimal places, plus one sentence explaining why the two token counts differ by the factor they do.

### [Warm-up] 2 — Bradley–Terry by hand

A reward model scores four responses: `r(a)=2.1`, `r(b)=1.4`, `r(c)=-0.3`, `r(d)=2.6`.

(a) Compute `P(a ≻ b)`, `P(d ≻ a)`, and `P(a ≻ c)` using `σ(r_w − r_l)`.
(b) Compute the Bradley–Terry loss for a human judgement that says `c ≻ d`.
(c) Add 100 to every reward and recompute all of (a). Explain the result in one sentence.

**Done looks like:** six probabilities, one loss value, all to three decimals, and the one-sentence explanation.

### [Build] 3 — Vocabulary-size curve

Train your BPE tokenizer on `CORPUS` at vocab sizes 256, 276, 306, 356, 406, 456, and 556. Plot bytes-per-token against vocabulary size with matplotlib. Mark on the plot the point where training stops early because no pair repeats.

**Done looks like:** a saved PNG with labelled axes, plus a written answer to: "if you had 100× more text, would the curve keep going up? Why?"

### [Build] 4 — Multilingual token tax

Take the same three sentences in English and in one other language you know (or use a translation you trust). Encode both with GPT-2's tokenizer. Report tokens-per-character for each language.

**Done looks like:** a table of tokens, characters, and tokens/character for both languages, and a short paragraph on what that ratio means for (a) cost per user and (b) how much of a 200k-token context window each user actually gets.

### [Stretch] 5 — Break your reward model

Extend Part D's reward model with a sixth feature, `is_factually_correct`, but do **not** include it in any preference pair (simulating raters who could not check facts). Add two new candidates: `r7 = [1,1,0,0,0]` plus correct, and `r8 = [1,1,0,0,0]` plus incorrect. Score both.

**Done looks like:** the printed rewards for `r7` and `r8`, an explanation of why they are identical, and a 150-word note titled "What my reward model cannot see" listing three real behaviours it would fail to penalize.

### [Stretch] 6 — DPO with contradictory preferences

Modify Part E so that the preference list contains a contradiction: add both `(0, 1)` and `(1, 0)`. Run at β = 0.1 for 300 steps. Report the final probabilities and the loss. Then remove the contradiction and add instead a *cycle*: `(0,1), (1,2), (2,0)`. Run again.

**Done looks like:** two sets of final probabilities and losses, plus an explanation of what the loss floor tells you. (Hint: what is the minimum achievable value of `−log σ(m)` averaged over `m` and `−m`?)

---

## 🤔 Think Deeper

**1. The preference data is the values.**
A reward model is trained on the judgements of a specific pool of human raters, working from a specific rubric, paid a specific rate, under time pressure. Every value judgement in the final model traces back to that pool. Who *should* be in it for a model used by 500 million people across 100 countries? Is a globally representative sample even the right target, or does that just average away every strong position into mush?

*How to reason about it:* pick one concrete disagreement where reasonable people differ across cultures — how direct criticism should be, how much a model should defer to authority, whether it should give medical advice. Now try to write a rubric line that satisfies both sides. Notice whether your rubric ends up saying something, or ends up saying nothing. Then ask who should be allowed to break the tie, and by what authority.

**2. Deduplication versus memory.**
Aggressive deduplication improves held-out loss. But some things *should* be memorized verbatim — the text of a constitution, the standard library API, a mathematical constant. Dedup removes exactly the repetition that would have cemented them. How would you decide what is worth memorizing, and how would you protect it through the pipeline?

*How to reason about it:* separate "the model can recite it" from "the model can find it" — Module 6's RAG makes the second one cheap. Then ask which category each of your examples belongs in, and what the cost of a wrong recitation is versus a failed lookup. Consider also who gets to declare something canonical.

**3. The judge is not the goal.**
Your Part D reward model gives `+5.047` for numbered steps and has no term for truth. Frontier reward models are far more sophisticated, but they are still proxies fitted to finite human judgements. Is there any way out of this — some signal that is not a proxy? Or is "the metric is not the goal" simply permanent?

*How to reason about it:* look for domains where the signal is *verifiable* rather than preferred — unit tests, formal proofs, physical measurements — and ask what fraction of what you want from an assistant falls into that category. Then ask what happens when you optimize hard on the verifiable part and leave the rest to a proxy. Does the unverifiable part get better, stay put, or quietly rot?

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Applying BPE merges in frequency order instead of learned order at encode time | It feels equivalent, and on short words it often is | Encoding must replay merges in the exact order learned. Use `min(pairs, key=lambda p: merges.get(p, inf))` — earliest merge id first, always |
| Letting merges cross word boundaries (skipping pre-tokenization) | Simpler code; you just run BPE on the whole string | You get tokens like `" the"`+`"cat"` glued into `" thecat"`, wasting vocabulary on accidents of phrasing. Always pre-tokenize first |
| Training BPE on characters instead of bytes | Characters are easier to print and debug | Any character outside your training corpus becomes `<UNK>` and round-trip breaks. Start from the 256 byte values — then nothing can ever fail to encode |
| Computing SFT loss over prompt tokens too | `cross_entropy(logits, labels)` on the whole sequence is the obvious call | Set prompt-position labels to `-100` and pass `ignore_index=-100`. Otherwise you are training the model to write user turns |
| Believing the reward model's absolute numbers | They are floats, floats look like measurements | Bradley–Terry fixes only *differences*. `r=7.2` means nothing on its own; only `r(a) − r(b)` is meaningful. Never threshold on a raw reward |
| Running DPO or PPO to convergence | Low loss is good, right? | Both over-optimize into mode collapse. Monitor KL to the reference and response diversity, and stop on those — not on training loss |
| Quoting "emergent abilities" as evidence of unpredictability | The phrase is vivid and widely repeated | Check what metric produced the jump. Discontinuous metrics manufacture discontinuous curves out of smooth improvement |
| Assuming a bigger vocabulary is always better | Fewer tokens per document sounds strictly good | Embedding and output layers scale linearly with `V`. At `d_model=768`, going from 50k to 128k vocab adds ~120M parameters to a 124M model |

---

## 🛠️ Mini-Project — Tokenizer + Life-of-an-LLM

**Time: ~2.5 hours**

### Goal

Two deliverables that together prove you understand the full pipeline: a **working BPE tokenizer with a round-trip proof**, and a **four-stage training-story explainer** that would teach something new to a smart adult who is not an engineer.

### Starter steps

**Part 1 — The tokenizer (~60 min)**

1. Implement `BPETokenizer` yourself, from the algorithm description, without copying Part A. Then diff against Part A.
2. Write a round-trip test that must pass on all of these:
   ```python
   TESTS = [
       "",                                     # empty
       "a",                                    # single byte
       "The cricket team practised on Tuesday.",
       "Ramana works at Apple Inc.",
       "naïve café — résumé",                  # multi-byte UTF-8
       "नमस्ते दुनिया",                            # non-Latin script
       "🍕🍕 pizza time 🍕",                    # 4-byte emoji
       "def f(x):\n\treturn x**2  # tab + newline",
       "   \n\n   ",                           # whitespace only
       "aaaaaaaaaaaaaaaaaaaaaaaa",             # pathological repetition
   ]
   for t in TESTS:
       assert tok.decode(tok.encode(t)) == t, repr(t)
   print(f"all {len(TESTS)} round-trip tests passed")
   ```
3. Save your merge list to JSON and load it back in a fresh process. The round-trip test must still pass. (Watch out: JSON keys must be strings — you will need to serialize the `(int, int)` tuples.)
4. Produce the comparison table: your tokenizer vs GPT-2 on (a) the training corpus, (b) a paragraph of unseen English, (c) a snippet of Python code.

**Part 2 — Build a preference dataset by hand (~40 min)**

5. Pick one task: "explain a technical concept to a beginner."
6. Write 10 prompts. For each, write two candidate responses yourself — one deliberately better, one deliberately worse, and **vary what makes it worse**: too long, too hedgy, factually wrong, ignores the audience, no example, wrong format.
7. Record them as JSONL:
   ```json
   {"prompt": "...", "chosen": "...", "rejected": "...", "why": "rejected buries the answer in preamble"}
   ```
8. Now the important part: **hand your 10 pairs to another person and have them label them without seeing your labels.** Compute agreement.

**Part 3 — The explainer (~50 min)**

9. Write "The Life of an LLM" — four stages, one section each, aimed at a smart adult with no ML background.
10. Each section must contain: what goes in, what the learning signal is, what comes out, one real number, and one concrete example of what goes wrong if you skip that stage.
11. Include at least one diagram you drew yourself (ASCII is fine).
12. End with a section titled **"What I got wrong before I did this module"**, listing at least two things.

### Success criteria checklist

- [ ] All 10 round-trip tests pass, including emoji, Devanagari, and the empty string
- [ ] Merge list survives a save/load cycle in a fresh Python process
- [ ] Comparison table shows your bytes/token and GPT-2's on three different text types
- [ ] Preference dataset has 10 pairs with **at least four distinct failure reasons** recorded in `why`
- [ ] Inter-rater agreement is computed and reported honestly, including any pair you disagreed on
- [ ] Explainer covers all four stages with a real number in each
- [ ] Explainer contains at least one thing a smart adult would not have guessed
- [ ] "What I got wrong" section is specific, not "I didn't know how it worked"

### Level it up

**Train your tokenizer on two corpora and measure the domain penalty.** Train tokenizer A on 50 KB of English prose and tokenizer B on 50 KB of Python source. Then cross-evaluate all four combinations and fill in this table:

| | eval on prose | eval on code |
|---|---|---|
| **tokenizer A (prose-trained)** | ? bytes/token | ? bytes/token |
| **tokenizer B (code-trained)** | ? bytes/token | ? bytes/token |

Then answer: if you must ship *one* tokenizer for a model that will see 70% prose and 30% code, how would you build its training corpus? What is the cost, in bytes/token, of getting the mix wrong by 20 percentage points? Measure it — do not guess.

---

## 🔑 Key Takeaways

- **Tokenization is a frozen decision made before training starts, and it constrains everything after.** Byte-level BPE never fails, always round-trips, and turns "most frequent adjacent pair" into a vocabulary that discovers English morphemes without being told they exist.
- **Pretraining is next-token prediction and nothing else.** All the engineering is in the data pipeline — extraction, filtering, deduplication, and mixture — and deduplication is the step where more data can make a model worse.
- **`C ≈ 6ND` and `D ≈ 20N` let you budget a training run on the back of an envelope**, and knowing why nobody follows the second rule any more teaches you that "optimal" is meaningless until you say optimal for what.
- **The four stages use four different learning signals:** the next token, a human-written ideal answer, a human comparison, and a scalar reward with a leash. SFT is 0.0003% of the data and changes the model's entire character, because it selects behaviour rather than installing knowledge.
- **Reward models only learn orderings, and any proxy optimized hard enough stops tracking the thing it proxies for.** You built a reward model that pays `+5` for numbered steps and `0` for truth in 25 lines of code.
- **A base model completes, an instruct model answers, a reasoning model thinks first** — and each difference is a specific training stage, not magic. Be sceptical of the word "emergent": check the metric before you believe the cliff.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Tokenizer** | The translator that turns text into numbers the model can read, and back again | `"lowest"` → `[257, 101, 260]` → `"lowest"` |
| **Byte-pair encoding (BPE)** | Repeatedly glue the most common neighbouring pair of symbols into one new symbol | `l`+`o` → `lo`, then `lo`+`w` → `low` |
| **Merge** | One glue operation, stored with an order number so encoding can replay it exactly | Merge #5 was `(115,116) → st` |
| **Vocabulary size** | How many distinct tokens exist; the tokenizer's whole alphabet | GPT-2 has 50,257 |
| **Pretraining** | Reading a huge pile of text and guessing the next token, trillions of times | 15 trillion tokens, months of GPUs |
| **Deduplication** | Deleting repeated documents before training | Removes 50–70% of a raw web crawl |
| **Contamination** | When test questions accidentally appear in the training data, so scores lie | A benchmark answer key that got crawled |
| **Scaling law** | A fitted curve predicting loss from model size and data size | Chinchilla: about 20 tokens per parameter |
| **`C ≈ 6ND`** | Training compute ≈ 6 × parameters × tokens | 7B params × 1.4T tokens ≈ 5.9×10²² FLOPs |
| **Base model** | A model that has only been pretrained; it continues text, it does not obey | Asks more questions back at you |
| **Supervised fine-tuning (SFT)** | Showing thousands of ideal answers and training only on the answer tokens | 50,000 (prompt, response) pairs |
| **Loss masking** | Setting prompt-token labels to `-100` so they are excluded from the loss | `targets[:, :prompt_len-1] = -100` |
| **Chat template** | Special tokens that mark whose turn it is in a conversation | `<\|user\|> ... <\|assistant\|> ...` |
| **Preference pair** | One prompt plus two responses, with a human saying which is better | `(prompt, chosen, rejected)` |
| **Reward model** | A model that scores how much a human would like a response, trained only on comparisons | `r(response) = 9.625` |
| **Bradley–Terry loss** | `−log σ(r(winner) − r(loser))` — the loss that turns comparisons into scores | Gap of 2.0 gives loss 0.127 |
| **RLHF** | Sample responses, score them with the reward model, push probability toward high scores | PPO with a KL leash |
| **KL penalty** | The leash stopping the tuned model from drifting far from where it started | `β · KL(π ‖ π_ref)` |
| **Reward hacking** | Getting a high score by exploiting the scorer instead of doing the task | Numbering everything because numbering scores `+5` |
| **DPO** | Preference training with no reward model and no RL, using a frozen reference for comparison | Two models in memory instead of four |
| **Instruct model** | A base model put through SFT and preference tuning; the thing you actually chat with | Answers "Paris." |
| **Reasoning model** | An instruct model additionally trained with RL on tasks whose answers can be checked automatically | Thinks internally, then answers |
| **Emergent ability** | A capability that looks like it appears suddenly at a certain scale — often a metric artifact | Multi-digit arithmetic under exact-match scoring |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1 — Token arithmetic on your own text

Solution script (works on any text file you point it at):

```python
from transformers import AutoTokenizer
from bpe import BPETokenizer
from corpus import CORPUS

with open("my_essay.txt", encoding="utf-8") as f:
    text = f.read()

mine = BPETokenizer().train(CORPUS, vocab_size=256 + 200)
hf = AutoTokenizer.from_pretrained("gpt2")

nb = len(text.encode("utf-8"))
n_mine = len(mine.encode(text))
n_gpt2 = len(hf.encode(text))

rows = [
    ("characters",        len(text)),
    ("bytes",             nb),
    ("my tokens",         n_mine),
    ("gpt2 tokens",       n_gpt2),
]
for k, v in rows:
    print(f"{k:14s} {v:7d}")
print(f"{'my b/tok':14s} {nb / n_mine:7.2f}")
print(f"{'gpt2 b/tok':14s} {nb / n_gpt2:7.2f}")
print(f"input cost @ $2/Mtok (gpt2 count as proxy): ${n_gpt2 / 1e6 * 2.00:.4f}")

assert mine.decode(mine.encode(text)) == text     # round-trip still holds
```

Representative result for a 3,100-character essay:

| quantity | value |
|---|---|
| characters | 3,100 |
| bytes | 3,104 |
| my tokens | 1,890 |
| gpt2 tokens | 702 |
| my bytes/token | 1.64 |
| gpt2 bytes/token | 4.42 |
| input cost | $0.0014 |

**Why the gap is ~2.7×:** your tokenizer learned 138 merges from 1,117 bytes of text about a school. GPT-2 learned 50,000 merges from 40 GB of the internet. Every word in your essay that did not appear in `CORPUS` — which is most of them — falls back toward per-character tokens in your tokenizer, while GPT-2 has a merge for it. The gap is a measure of corpus coverage, not of algorithm quality: the algorithm is identical.

Note also that the cost figure uses the GPT-2 count as a stand-in. Claude uses a different tokenizer, so for real budgeting you must call `client.messages.count_tokens` — which you will do in Module 5.

---

### 2 — Bradley–Terry by hand

**(a)** `σ(x) = 1/(1+e^(−x))`.

```
P(a ≻ b) = σ(2.1 − 1.4)  = σ(0.7)
         = 1/(1 + e^(−0.7)) = 1/(1 + 0.4966) = 0.6682

P(d ≻ a) = σ(2.6 − 2.1)  = σ(0.5)
         = 1/(1 + 0.6065) = 0.6225

P(a ≻ c) = σ(2.1 − (−0.3)) = σ(2.4)
         = 1/(1 + 0.0907) = 0.9168
```

**(b)** The human said `c ≻ d`, so the winner is `c` and the loser is `d`:

```
r(c) − r(d) = −0.3 − 2.6 = −2.9
σ(−2.9)     = 1/(1 + e^2.9) = 1/(1 + 18.174) = 0.05213
loss        = −log(0.05213) = 2.954
```

A large loss, correctly — the model was confidently wrong about this pair. Compare with the loss it would incur on a pair it gets right, e.g. `a ≻ c`: `−log(0.9168) = 0.0869`. The Bradley–Terry loss punishes confident errors roughly 34× harder here.

**(c)** Adding 100 to every reward: `r(a)=102.1`, `r(b)=101.4`, `r(c)=99.7`, `r(d)=102.6`. Every *difference* is unchanged, so `P(a≻b)=0.6682`, `P(d≻a)=0.6225`, `P(a≻c)=0.9168` — **identical**.

**One-sentence explanation:** the Bradley–Terry model depends only on reward *differences*, so a reward model is defined only up to an additive constant — which is exactly why you may never threshold on a raw reward value or compare rewards across two separately trained reward models.

---

### 3 — Vocabulary-size curve

```python
import matplotlib.pyplot as plt
from bpe import BPETokenizer
from corpus import CORPUS

sizes = [256, 276, 306, 356, 406, 456, 556]
nbytes = len(CORPUS.encode("utf-8"))
xs, ys, merges = [], [], []

for vs in sizes:
    t = BPETokenizer().train(CORPUS, vocab_size=vs)
    n = len(t.encode(CORPUS))
    xs.append(vs); ys.append(nbytes / n); merges.append(len(t.merges))
    print(f"vocab {vs:4d}  merges {len(t.merges):4d}  tokens {n:5d}  b/tok {nbytes/n:.2f}")

sat = next(i for i in range(1, len(merges)) if merges[i] == merges[i - 1])

plt.figure(figsize=(7, 4))
plt.plot(xs, ys, "o-", label="bytes per token")
plt.axvline(256 + merges[sat], ls="--", c="crimson",
            label=f"training saturates at {merges[sat]} merges")
plt.xlabel("requested vocabulary size")
plt.ylabel("bytes per token (higher = better compression)")
plt.title("BPE compression vs vocabulary size on a 1,117-byte corpus")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig("vocab_curve.png", dpi=150)
print("saved vocab_curve.png")
```

Printed values:

```
vocab  256  merges    0  tokens  1117  b/tok 1.00
vocab  276  merges   20  tokens   855  b/tok 1.31
vocab  306  merges   50  tokens   720  b/tok 1.55
vocab  356  merges  100  tokens   580  b/tok 1.93
vocab  406  merges  138  tokens   504  b/tok 2.22
vocab  456  merges  138  tokens   504  b/tok 2.22
vocab  556  merges  138  tokens   504  b/tok 2.22
```

The curve rises steeply, then goes flat at 138 merges. Training stops early because the `if cnt < 2: break` guard fires — every remaining adjacent pair occurs exactly once, so merging it would create a token used exactly once. That is a pure waste of vocabulary.

**Would the curve keep going with 100× more text? Yes, for a long way.** With 100 KB instead of 1 KB you would get thousands of pairs occurring ≥2 times, so `cnt < 2` would not fire until far later, and each new merge would still be removing a real, repeated pattern. But the curve is concave and will eventually flatten anyway, for a different reason: merges are added in decreasing frequency order, so the *k*-th merge saves less than the (*k*−1)-th. Real tokenizers show bytes/token climbing quickly to ~3.5 by 8k vocab, ~4.2 by 32k, and ~4.6 by 100k — big gains early, diminishing returns after. That diminishing-returns shape is exactly why 32k–128k is the range everyone settles in: past that, you pay `d_model` parameters per new token for almost no compression.

---

### 4 — Multilingual token tax

```python
from transformers import AutoTokenizer
hf = AutoTokenizer.from_pretrained("gpt2")

SAMPLES = {
    "English": ("The library opened a new reading room this morning. "
                "Students borrow books every day and return them before evening. "
                "Reading every day makes reading easier."),
    "Hindi":   ("पुस्तकालय ने आज सुबह एक नया पठन कक्ष खोला। "
                "छात्र हर दिन किताबें उधार लेते हैं और शाम से पहले लौटा देते हैं। "
                "हर दिन पढ़ने से पढ़ना आसान हो जाता है।"),
}

print(f"{'language':9s} {'chars':>6s} {'bytes':>6s} {'tokens':>7s} {'tok/char':>9s}")
for lang, s in SAMPLES.items():
    n = len(hf.encode(s))
    print(f"{lang:9s} {len(s):6d} {len(s.encode('utf-8')):6d} {n:7d} {n/len(s):9.3f}")
```

Representative output:

```
language   chars  bytes  tokens  tok/char
English      183    183      36     0.197
Hindi        168    452     171     1.018
```

**The table says: Hindi costs about 5.2× more tokens per character than English.**

Two causes, and they compound. First, GPT-2's merge list was learned on overwhelmingly English text, so Devanagari sequences have almost no merges — they fall back to near-byte tokens. Second, Devanagari characters are 3 bytes each in UTF-8, so even at the byte level there is 3× more to encode before any merges apply.

**(a) Cost per user.** At $2.00 per million input tokens, the same 183-character message costs $0.000072 in English and $0.000342 in Hindi. Across ten million messages that is $720 versus $3,420. A Hindi-speaking user is charged roughly 5× as much for the identical request. Nobody designed that; it fell out of the training-corpus mixture.

**(b) Usable context.** A 200,000-token context holds roughly 1,015,000 English characters but only about 196,000 Hindi characters. The Hindi user gets about one-fifth of the effective window. That means shorter documents in RAG, fewer conversation turns retained, and earlier truncation — a capability gap, not just a billing gap.

This is why modern tokenizers deliberately over-sample non-English text when learning merges. It costs vocabulary slots that could have gone to English, and that is exactly the trade-off being made on purpose.

---

### 5 — Break your reward model

```python
import torch
import torch.nn.functional as F
torch.manual_seed(1)

FEATS = ["has_numbered_steps", "gives_direct_answer", "hedges_a_lot",
         "over_400_chars", "refuses", "is_factually_correct"]

POOL = {
    "r1": [1, 1, 0, 0, 0, 1],
    "r2": [0, 1, 0, 0, 0, 1],
    "r3": [0, 1, 1, 1, 0, 1],
    "r4": [0, 0, 1, 0, 0, 1],
    "r5": [0, 0, 0, 0, 1, 1],
    "r6": [1, 1, 0, 1, 0, 1],
    "r7": [1, 1, 0, 0, 0, 1],   # identical to r1 but CORRECT
    "r8": [1, 1, 0, 0, 0, 0],   # identical to r1 but WRONG
}
# Everything the raters actually compared happened to be factually correct,
# so r7/r8 never appear in any pair and the feature never varies within one.
PAIRS = [("r1", "r4"), ("r1", "r5"), ("r2", "r4"), ("r6", "r3"), ("r1", "r3"),
         ("r2", "r5"), ("r1", "r2"), ("r6", "r4"), ("r2", "r3"), ("r3", "r5")]

X = {k: torch.tensor(v, dtype=torch.float32) for k, v in POOL.items()}
w = torch.zeros(6, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
for _ in range(500):
    loss = torch.stack([-F.logsigmoid(X[a] @ w - X[b] @ w) for a, b in PAIRS]).mean()
    opt.zero_grad(); loss.backward(); opt.step()

for f, wi in zip(FEATS, w.detach()):
    print(f"  {f:22s} {wi:+.3f}")
print(f"\nr7 (correct)   reward {(X['r7'] @ w).item():+.3f}")
print(f"r8 (incorrect) reward {(X['r8'] @ w).item():+.3f}")
```

Output — the weight on `is_factually_correct` stays exactly at its initialization of zero, and the other five weights are bit-for-bit identical to Part D:

```
  has_numbered_steps     +5.047
  gives_direct_answer    +4.578
  hedges_a_lot           -2.794
  over_400_chars         -2.534
  refuses                -6.091
  is_factually_correct   +0.000

r7 (correct)   reward +9.625
r8 (incorrect) reward +9.625
```

**Why they are identical.** Look at what the loss actually depends on: `X[a] @ w − X[b] @ w = (X[a] − X[b]) @ w`. Only the *difference* between the two feature vectors enters. Every pair in `PAIRS` compares two responses that both have `is_factually_correct = 1`, so that coordinate of the difference is `1 − 1 = 0` in all ten pairs. Its gradient is therefore exactly zero at every step, and Adam leaves it at its initial value forever.

It is not that the model decided facts do not matter, and it is not a numerical accident. **The data never contained the question**, so the parameter that would answer it received no signal at all. Add one single pair that differs only in that feature and the weight moves immediately.

> ### What my reward model cannot see
>
> This reward model was fitted to ten judgements about presentation, made by a rater who read each response for thirty seconds. Anything that takes longer than thirty seconds to check is invisible to it, and invisibility is not neutrality — an invisible property gets weight zero, which means the optimizer is free to destroy it for free.
>
> Three concrete behaviours it would not penalize:
>
> 1. **A confidently wrong citation.** "According to the 2019 WHO report, ..." with a report that does not exist scores exactly as well as a real one, because `is_factually_correct` carries no weight. Fluency is rewarded; accuracy is not measured.
> 2. **Numbered steps that are numbered nonsense.** `has_numbered_steps` is worth `+5.047` — nearly as much as everything else combined. Wrapping a bad answer in "1. 2. 3." is the single cheapest reward increase available, and an optimizer will find it.
> 3. **Silent scope reduction.** Answering an easier version of the question — "how do I sort a list" when asked "how do I sort a list of dicts by two keys" — is direct, concise, and unhedged, so it scores near the top. Nothing in the feature set checks that the answer addresses the question that was actually asked.
>
> The fix is not a better optimizer. It is preference data that contains pairs differing *only* in the property you care about, collected from raters given enough time and enough tooling to actually check. That is expensive, which is precisely why it often does not happen.

---

### 6 — DPO with contradictory preferences

```python
import torch
import torch.nn.functional as F

ref_logits = torch.tensor([0.4, 0.6, 1.2, 0.8])
ref_logp = F.log_softmax(ref_logits, dim=-1)

def run(pairs, beta=0.1, steps=300, lr=0.05):
    pl = torch.nn.Parameter(ref_logits.clone())
    opt = torch.optim.Adam([pl], lr=lr)
    for _ in range(steps):
        logp = F.log_softmax(pl, dim=-1)
        m = torch.stack([beta * ((logp[w] - ref_logp[w]) - (logp[l] - ref_logp[l]))
                         for w, l in pairs])
        loss = -F.logsigmoid(m).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    return F.softmax(pl, -1).detach(), loss.item()

BASE = [(0, 3), (0, 2), (1, 2), (1, 3), (2, 3)]

p, l = run(BASE + [(0, 1), (1, 0)])
print("contradiction:", " ".join(f"{c}={p[i]:.3f}" for i, c in enumerate("ABCD")),
      f" loss={l:.4f}")

p, l = run([(0, 1), (1, 2), (2, 0)])
print("cycle        :", " ".join(f"{c}={p[i]:.3f}" for i, c in enumerate("ABCD")),
      f" loss={l:.4f}")
```

Actual output:

```
contradiction: A=0.450 B=0.550 C=0.000 D=0.000  loss=0.3395
cycle        : A=0.168 B=0.206 C=0.375 D=0.251  loss=0.6931
```

**Reading the contradiction case.** The pair `(0,1)` pushes A above B; the pair `(1,0)` pushes B above A with exactly equal force. They cancel — but notice they do *not* settle at 0.500/0.500. They settle at 0.450/0.550, and the reference model's probabilities restricted to {A, B} were `0.168/(0.168+0.206) = 0.449` and `0.206/(0.168+0.206) = 0.551`. **The contradicted pair reverts precisely to the reference model's own preference.** That is DPO's KL term doing its job without there being an explicit KL term: the loss only measures movement *relative to the reference*, so when the preference data says nothing net, the reference wins by default. Meanwhile C and D still collapse to zero, because every pair involving them agrees they lose. Contradictory data does not break DPO — it produces deference to the reference on the contradicted options while the uncontested part of the ranking trains normally.

**Reading the cycle case.** A ≻ B ≻ C ≻ A has no consistent ordering. The result is the strongest possible version of the same phenomenon: the final probabilities are `0.168, 0.206, 0.375, 0.251` — **exactly the reference model, unchanged to three decimals** — and the loss sits at `0.6931`. In a perfect cycle every option wins exactly once and loses exactly once, so the three gradient contributions cancel to zero at the starting point, and the starting point is the reference. The model never moves at all. 300 steps of training accomplished literally nothing.

**The hint, worked out.** For a matched pair of opposite margins `m` and `−m`, the average loss is

```
½[ −log σ(m) − log σ(−m) ]
```

Using `σ(−m) = 1 − σ(m)` and writing `s = σ(m)`, this is `−½[log s + log(1−s)]`, which is minimized at `s = 0.5`, giving `−log 0.5 = 0.6931`. So **`log 2` is the loss floor for perfectly contradictory data** — and the cycle run sits exactly on that floor, which is how you know it is not learning. The contradiction run's `0.3395` is lower only because five of its seven pairs are consistent and drive C and D down.

**Why this matters in practice.** A DPO training loss that plateaus near `0.693` is not telling you your model is bad. It is telling you your *labels* are inconsistent — either your raters disagree with each other, or the same rater is inconsistent, or your pairs are genuinely ties that a human coin-flipped. Before you touch β or the learning rate, go and measure inter-rater agreement. If it is near chance, no optimizer can help you, because there is nothing in the data to learn.

</details>

---

[⬅ Previous](module-03-attention-and-transformers.md) · [Level 4 Home](README.md) · [Next ➡](module-05-prompt-engineering.md)
