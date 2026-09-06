# 📓 Level 4 Glossary — Every Word, Alphabetized

**Level 4 · Reference · Prereqs: none — use this any time a word stops making sense**

[Level 4 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Level 3 Glossary](../level-3-engineer/glossary.md) · [Level 2 Glossary](../level-2-builder/glossary.md)

---

## How to use this page

Every technical term introduced anywhere in Level 4 is here — **212 of them** — with a plain-English definition and the actual example from the course. The **Module** column tells you where to go for the full explanation:

| Tag | Where |
|---|---|
| `M1`–`M9` | That module file, e.g. [`module-03-attention-and-transformers.md`](module-03-attention-and-transformers.md) |
| `SET` | The environment-setup section of the [level README](README.md) |
| `CAP` | The [capstone](capstone.md) |

**Jump to a letter:**
[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [Z](#z)

> ⚠️ **A word on `code font`.** Terms written like `this` are things you literally type. Terms written like *this* are ideas. If you can type it, it is a spelling; if you cannot, it is a concept.

> 🔑 **The words that carry the most weight in this level** are not the mathematical ones. They are **frozen test set**, **grounding**, **refusal path**, **guardrail**, **regression**, and **who should not rely on this**. If you only own six terms from Level 4, own those.

---

## A

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Ablation** | Removing one component and re-measuring, to find out what that component was actually contributing | Removing the residual connections from Tiny GPT and watching validation loss get worse | M3 |
| **Abstention** | Designing a permitted, deliberate way for a system to decline to answer instead of guessing | `NOT_IN_SOURCES`, returned when the passages do not contain the answer | M6, M9 |
| **Adam** | An optimizer combining momentum and RMSProp with bias correction, so each step is roughly `lr`-sized regardless of gradient magnitude | From `w = 1.0` with `lr = 0.1`, Adam's first step lands exactly on `0.9` | M1 |
| **AdamW** | Adam with weight decay applied straight to the weights instead of through the loss — the transformer default | `AdamW(params, lr=3e-4, weight_decay=0.01)` | M1 |
| **Adaptive thinking** | An API feature letting the model reason internally before it answers | `thinking={"type": "adaptive"}` | M5 |
| **Agent** | A model in a loop that can request actions, see the results, and decide what to do next | search → calculate → write → answer | M7 |
| **Agent loop** | Repeating perceive → decide → act → observe until a stop condition fires | The bounded `for` loop in `run_agent` | M7 |
| **Alignment** | Making a system pursue what people actually want, rather than the measurable proxy you trained it on | A reward model that rewards numbered lists produces a model that numbers everything | M9 |
| **Allowlist** | The explicit set of permitted things; everything not on it is refused by default | The `ToolRegistry` dict — a tool that is not registered does not exist | M7 |
| **`ANTHROPIC_API_KEY`** | The environment variable the SDK reads to authenticate. Never put it in a file. | `export ANTHROPIC_API_KEY="sk-ant-..."` | SET |
| **Answer contract** | One dataclass defining every field an answer carries, used by the CLI, the eval harness, the logger and the demo | `Answer(question, route, text, refused, citations, cost_usd, latency_s, ...)` | CAP |
| **Approximate nearest neighbour (ANN)** | Trading a little retrieval accuracy for a lot of speed once you have millions of vectors | FAISS, hnswlib — unnecessary at 15 chunks, essential at 15 million | M6 |
| **Attention** | A soft, differentiable lookup: compare a query to every key, softmax the scores into weights, return the weighted average of the values | Scores `[0.1, 2.0, 0.3]` → weights `[0.112, 0.751, 0.137]` | M3 |
| **Attention scores** | The `(T, T)` matrix of query·key dot products, before scaling and softmax | Entry `(3, 1)` = how much token 3 wants token 1 | M3 |
| **Attention sink** | Many queries dumping weight on position 0 regardless of content, because softmax must sum to 1 somewhere | The bright first column in your attention heatmap | M3 |
| **Autoregressive generation** | Feeding the model's own output back in as the next input, one token at a time | `<START>→d→i→r→a→<EOS>` gives "dira" | M2 |
| **Automation bias** | People trusting a machine's answer more than their own judgement, especially when it is fluent | Accepting a cited-looking answer without ever opening the citation | M9 |

---

## B

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Bag of words** | A text representation that keeps word counts and throws away order | "dog bit postman" and "postman bit dog" give the identical vector | M2 |
| **Base model** | A model that has only been pretrained. It continues text; it does not obey. | Ask it a question and it writes more questions | M4 |
| **Baseline** | The score of the laziest thing that could possibly work, which your system must beat before its number means anything | Keyword search only: 0.37 on the 27-case capstone eval | M5, CAP |
| **Batch norm** | Normalize each feature using statistics computed **across the batch** (down a column) | Standard in CNNs; undefined at batch size 1 | M1 |
| **Batch size** | How many examples are averaged into one optimizer step | 32 → 128 quadruples the gradients per step and quarters the steps per epoch | M1 |
| **Benchmark contamination** | A public test set that has already been swallowed by the pretraining crawl, so scores on it are meaningless | Why MMLU cannot decide your release | M4, M8 |
| **Blast radius** | How much damage one wrong action can do | One sandboxed file, versus your entire home directory | M7 |
| **Block size** | See **Context window** | `BLOCK = 64` in Tiny GPT | M3 |
| **BPTT (backpropagation through time)** | Backpropagation applied to a recurrent network unrolled into a chain | The gradient at step 1 of a 40-step sequence passes through 39 chained Jacobians | M2 |
| **Bradley–Terry loss** | `−log σ(r(winner) − r(loser))` — the loss that turns pairwise comparisons into a single score per item | A reward gap of 2.0 gives a loss of 0.127 | M4 |
| **Brier score** | The mean squared error of probabilities: average of `(confidence − outcome)²`. One number for "how wrong were the probabilities", lower is better | 0.2150 on the 40-question calibration run | M9 |
| **Budget guard** | Code that tracks spend and **raises before** a call that would exceed the cap | `BudgetGuard(limit_usd=0.50).check(projected_usd=0.01)` | M5, CAP |
| **Byte-pair encoding (BPE)** | Repeatedly glue the most common neighbouring pair of symbols into one new symbol, building a subword vocabulary from bytes upward | `l`+`o` → `lo`, then `lo`+`w` → `low` | M4 |

---

## C

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`C ≈ 6ND`** | Training compute ≈ 6 × parameters × tokens | 7B params × 1.4T tokens ≈ 5.9×10²² FLOPs | M4 |
| **Calibration** | Whether a model's expressed confidence matches how often it is actually right | Saying "definitely" on a class of question it gets right 60% of the time is *mis*calibration | M9 |
| **Catastrophic forgetting** | Losing an ability you already had while learning a new task | `out_of_scope` accuracy 0.80 → 0.40 after fine-tuning | M8 |
| **Causal mask** | Setting the attention scores for future positions to `−inf` **before** the softmax, so a token cannot see its own answer | `torch.tril(torch.ones(T, T))`, then `masked_fill(mask == 0, -inf)` | M3 |
| **Cell state** | The LSTM's additive memory track, kept separate from the hidden state | `c_t = f_t ⊙ c_(t−1) + i_t ⊙ g_t` | M2 |
| **Chain-of-thought** | Making the model write its working out before its answer | "315, then 500 − 315 = 185, then…" | M5 |
| **Chat template** | Special tokens marking whose turn it is in a conversation | `<\|user\|> ... <\|assistant\|> ...` | M4 |
| **Chinchilla ratio** | The rough scaling-law finding that a compute-optimal model wants about **20 tokens per parameter** | A 7B model wants ~140B tokens | M4 |
| **Chunk** | One piece of a document that gets its own embedding and its own id | One `##` entry from your lab notebook | M6 |
| **Citation** | A marker tying a sentence back to the exact source it came from | `[9]` at the end of a factual sentence | M6, CAP |
| **Class balance** | How many training examples each label gets | 14 / 14 / 14 / 14 / **8** — the last class is the one that breaks | M8 |
| **Cohen's kappa (κ)** | Agreement between two raters, corrected for the agreement you would get by chance | 0.4118 = "moderate". 74% raw agreement on skewed data can be κ ≈ 0.04. | M8 |
| **Cold start** | The one-off cost of loading everything before the first request — reported separately from per-request cost, always | 38 ms to load the model; 1.6 ms per prediction | CAP |
| **Compute budget** | The total FLOPs you can afford, which then has to be split between model size and data size | Given `C`, scaling laws tell you the best `N` and `D` | M4 |
| **Consent** | Whether the people whose text you are using agreed to it | The `SOURCES.md` file naming whose documents are in your corpus | M9, CAP |
| **Constant baseline** | The score you get by ignoring the input and always answering the same thing | 37.5% on the Module 5 extraction suite | M5 |
| **Contamination** | Test data leaking into training data, so the score lies | A Jaccard 1.000 duplicate between the eval set and the SFT set | M4, M8 |
| **Context window** | The maximum number of tokens the model can attend over at once | `BLOCK = 64` in Tiny GPT; `idx[:, -block_size:]` enforces it | M3 |
| **Copyright and attribution** | Whose work the training data or the corpus is, and whether you are allowed to use it and must credit it | Scraping a syllabus you did not write, into a product you show people | M9 |
| **Cosine similarity** | How closely two vectors point in the same direction, ignoring their lengths | `1.0` identical, `0.0` unrelated; `0.64` for two sentences sharing zero words | M6 |
| **Cost per task** | Dollars spent per completed user request, measured from `response.usage`, reported as a mean **and** a p95 | mean $0.00488, p95 $0.01820 — the p95 is the agent path | M5, CAP |
| **`count_tokens`** | A free endpoint that tells you the input size **before** you pay for it | `client.messages.count_tokens(...).input_tokens` | M5 |

---

## D

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Data augmentation** | Creating new training examples with label-preserving transformations | Flipping a cat photo; ⚠️ **not** flipping a letter "b" | M1 |
| **Data fencing** | Wrapping untrusted retrieved text in a labelled container so it cannot pass as an instruction | `<retrieved_document trust="untrusted">…</retrieved_document>` | M9 |
| **Data minimization** | Collecting and keeping the least data that does the job | Truncating the logged question to 400 characters and redacting PII first | M9, CAP |
| **Decomposition** | Splitting a task into ordered steps with dependencies | look up the number → multiply it → save the result | M7 |
| **Deduplication** | Removing repeated or near-repeated rows — from a training corpus, or from training data that is too close to your eval set | Removes 50–70% of a raw web crawl; removed 2 of 66 SFT rows in M8 | M4, M8 |
| **Delimiter** | A marker separating your instructions from somebody else's data | `<message> ... </message>`, `<sources> ... </sources>` | M5 |
| **Dense embedding** | A list of a few hundred numbers that captures what a piece of text *means* | 384 numbers per note from `all-MiniLM-L6-v2` | M6 |
| **Design doc** | A written statement of the problem, the user, why AI, and what could go wrong — produced **before** any code | `DESIGN.md`, dated and committed first | CAP |
| **DPO (direct preference optimization)** | Preference training with no reward model and no reinforcement learning, using a frozen reference model for comparison | Two models in memory instead of four | M4 |
| **Dropout** | Randomly zeroing a fraction of activations during training, so no single neuron becomes indispensable | `nn.Dropout(0.2)`; turned off automatically by `model.eval()` | M1 |

---

## E

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Early stopping** | Keeping the weights from the best validation epoch and stopping when it stops improving | Saved 0.375 of validation loss for free in Module 1's run | M1 |
| **ECE (expected calibration error)** | The size of the gap between stated confidence and actual hit rate, averaged over buckets and weighted by bucket size | 0.1075 — nearly all of it in the "definitely" bucket | M9 |
| **Effective learning rate** | How much weight change happens per training *example*, roughly `lr / batch_size` | Quadruple the batch → quadruple the LR to hold it constant | M1 |
| **Effort** | How much internal work the model puts into a response | `output_config={"effort": "low"}` for classification | M5 |
| **Emergent ability** | A capability that appears to switch on suddenly at a certain scale — often an artefact of an all-or-nothing metric | Multi-digit arithmetic looks emergent under exact match and gradual under per-digit accuracy | M4 |
| **Enum** | A schema rule saying "only these exact values are permitted" | `"enum": ["billing", "shipping", "technical", "account", "other"]` | M5 |
| **Eval harness** | Code that runs every version over the frozen test set and prints a score | `python eval/run_eval.py` → one headline number | M5, CAP |
| **Exact match** | Score 1 if the prediction equals the gold answer, 0 otherwise | `pred == "refund"` | M8 |
| **Exploding gradient** | The BPTT product growing without bound instead of shrinking | Measured `9.38e+06` with `W_hh` scaled by 8 | M2 |
| **Exposure bias** | Training only on perfect histories, then generating from imperfect ones | A small early error compounds because nothing ever corrects it | M2 |

---

## F

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Feed-forward network (FFN)** | The per-position two-layer MLP inside a transformer block, usually with 4× expansion; it holds most of the parameters | `Linear(128, 512) → GELU → Linear(512, 128)` | M3 |
| **Few-shot** | Showing 2–8 completed examples before the real input | Three `<example>` blocks in the prompt | M5 |
| **Field-level score** | Fraction of individual fields correct, rather than all-or-nothing per case | 3 of 4 fields right = 0.75 | M5 |
| **Fine-tuning** | Continuing to train a model's weights on your own examples | DistilBERT on 64 support tickets | M8 |
| **Flip rate** | How often a pairwise judge's winner changes when you swap the order of the two answers | 8 of 30 = 26.7% — a direct measure of position bias | M8 |
| **Forget gate bias** | The initial bias on an LSTM's forget gate, set to +2 so the cell starts in "remember" mode | σ(2) = 0.881 instead of σ(0) = 0.5 | M2 |
| **Frozen test set** | Cases and gold answers written **before** any tuning, and never edited to flatter a result | 20 committed JSON cases in M5; 30 in M8; 25+ in the capstone | M5, M8, CAP |

---

## G

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Gate** | A 0–1 vector produced by a sigmoid that scales how much information passes through | A forget gate at 0.95 keeps 95% of the memory each step | M2 |
| **Generation failure** | The answer *was* in the retrieved context and the model still got it wrong | Fix the prompt, reduce `k`, or reorder the context | M6 |
| **Golden test** | Two or three inputs whose exact answers you assert, run after every change | `tests.py` — the cheapest regression test in existence | CAP |
| **Graceful failure** | Stopping with a partial answer and an honest explanation, rather than crashing or inventing | "I could not write the file because the path escaped the sandbox." | M7 |
| **Gradient clipping** | Rescaling the gradient vector down if its length exceeds a threshold, keeping its direction | `clip_grad_norm_(params, 1.0)` — mandatory for RNNs | M1, M2 |
| **Gradient noise** | The randomness in a gradient estimate from using a small batch instead of the whole dataset | Small batches are noisier, which regularizes but destabilizes | M1 |
| **Greedy decoding** | Always taking the highest-probability token | Deterministic, and reliably boring | M2 |
| **Grounding** | Requiring the answer to come **only** from provided sources | "Using ONLY the passages in `<sources>`, answer…" | M5, M6 |
| **GRU** | A simpler gated recurrent cell: one update gate, one reset gate, no separate cell state | `h_t = (1−z) ⊙ h_(t−1) + z ⊙ h̃_t` | M2 |
| **Guardrail** | A check **in your code** that can refuse regardless of what the model asked for | The sandbox path check — a system prompt is a request, this is a guarantee | M7, M9 |

---

## H

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Hallucination** | Content that is not supported by the source or by fact, produced fluently | "The week-11 experiment found…" when there is no week 11 | M9 |
| **Head dimension (`d_k`)** | How many dimensions each attention head works in | 128 model dims ÷ 4 heads = 32 per head | M3 |
| **Hidden state** | The fixed-size vector holding everything a recurrent network remembers so far | The one sticky note you are allowed while reading a novel | M2 |
| **Human-in-the-loop** | A person must approve before a risky action runs | `approve? [y/N]` before a file write | M7, M9 |
| **Hybrid search** | Combining dense-embedding and keyword scores into one ranking | `0.6 × dense + 0.4 × tfidf` | M6 |

---

## I

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Incident response** | The written plan for what you do when your deployed system causes a problem | Who is told, how it is switched off, and what gets logged | M9 |
| **Injection marker** | A phrase your scanner looks for in untrusted text, as one layer of defence | `"ignore previous instructions"`, `"you are now"`, `"system:"` | M7 |
| **Instruct model** | A base model put through SFT and preference tuning — the thing you actually chat with | Answers "Paris." instead of writing more questions | M4 |
| **Iteration budget** | The hard maximum number of passes an agent loop may take | `MAX_ITERATIONS = 10` | M7 |

---

## J

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Jaccard similarity** | Shared words ÷ total distinct words — a cheap near-duplicate detector | 7/9 = 0.778 between a training row and an eval row | M8 |
| **Jailbreak** | A prompt crafted to talk a model out of its own guidelines | Distinct from injection, which hides orders inside *data* | M9 |
| **JSON Lines (JSONL)** | A log format: one complete JSON object per line, append-only, human-readable and script-parseable | `logs/trace.jsonl` | M7, CAP |

---

## K

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **KL penalty** | The leash stopping a preference-tuned model from drifting far from where it started | `β · KL(π ‖ π_ref)` in RLHF; folded into the loss in DPO | M4 |
| **KV cache** | Storing past keys and values so generation does not recompute the whole context each step | Turns `O(T²)` generation into `O(T)` | M3 |

---

## L

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Label leakage** | Letting the model see the answer it is supposed to predict | A missing causal mask: train loss near zero, generation useless | M3 |
| **Latency (p50 / p95)** | The median and 95th-percentile time per request. Report both; the mean hides the tail. | p50 2.41 s (retrieval), p95 9.88 s (the agent path) | CAP |
| **Layer norm** | Normalize each example using statistics across **its own features** (across a row) | The transformer standard; batch-size-independent and identical at train and inference | M1 |
| **Learned positional embedding** | A trainable table with one row per position | `nn.Embedding(block_size, n_embd)`; cannot exceed `block_size` | M3 |
| **Learning-rate schedule** | A rule that changes the learning rate over the course of training | Cosine: `lr · 0.5 · (1 + cos(π·t/T))`, from `lr` down to 0 | M1 |
| **Linear scaling rule** | Multiply the batch size by `n`, multiply the learning rate by `n` | batch 32 → 128 means `3e-4` → `1.2e-3` | M1 |
| **LLM-as-judge** | Using a model to grade another model's free-text output | `claude-sonnet-5` scoring answers against a numbered rubric | M8 |
| **Logits** | Raw unnormalized scores, one per vocabulary item, before the softmax | `[2.0, 1.0, 0.5, 0.0]` | M2 |
| **Long context** | Pasting the whole corpus into every prompt instead of retrieving from it | $4,000/month versus $20 for the same questions | M6 |
| **LoRA** | Freeze the big weight matrix `W` and learn a small low-rank correction `B·A` instead | 12,288 trainable parameters instead of 589,824 | M8 |
| **Loss masking** | Setting prompt-token labels to `-100` so they are excluded from the SFT loss | `targets[:, :prompt_len-1] = -100` — you train on the answer, not the question | M4 |
| **LR range test** | Sweeping the learning rate upward over a few hundred steps to find where the loss starts diverging | The cheapest way to find your usable LR band | M1 |
| **LSTM** | A recurrent cell with an additive cell state and three gates (forget, input, output), designed to keep gradients alive | Published 1997; dominant from ~2014 | M2 |

---

## M

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **`max_tokens`** | The hard ceiling on how much the model may write. Required on every call. | 300 for extraction, 4000 for essays | M5 |
| **Merge** | One BPE glue operation, stored with an order number so encoding can replay it exactly | Merge #5 was `(115, 116) → st` | M4 |
| **Messages API** | The endpoint you send a conversation to and get a reply from | `client.messages.create(model="claude-sonnet-5", ...)` | M5 |
| **Miscalibration** | Expressed confidence that does not match the actual hit rate — distinct from hallucination | Right this time, but stating certainty it has not earned | M9 |
| **Momentum** | Keeping a running average of past gradients, so consistent directions accelerate and zig-zags cancel | Three `+2.0` gradients give velocity 2.0 → 3.8 → 5.42 | M1 |
| **MPS** | Apple's GPU backend for PyTorch on Apple Silicon | `torch.backends.mps.is_available()`; often *slower* than CPU for tiny models | SET |
| **Multi-head attention** | Split `d_model` into `h` chunks, attend independently in each, concatenate, project | 128 dims / 4 heads = 32 per head, at essentially the same parameter count | M3 |

---

## N

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Normalisation (of predictions)** | Cleaning up a prediction before comparing it to the gold answer | `"Technical Support"` → `technical` | M8 |
| **`NOT_IN_SOURCES`** | The exact string your grounded prompt permits the model to return when the passages do not contain the answer | The refusal escape hatch, and the reason the model does not have to invent | M6, CAP |

---

## O

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Out-of-scope use** | A thing a reasonable person might try that you are telling them not to | "Do not use this for anything that affects another person" | M9, CAP |
| **Out-of-vocabulary (OOV)** | A word the tokenizer or vectorizer has never seen | A fatal problem for word-level tokenizers; structurally impossible for BPE | M4 |
| **Output projection (`W_O`)** | The linear layer applied after concatenating the attention heads, which blends their outputs | `nn.Linear(n_embd, n_embd)` | M3 |
| **Overfitting** | Getting better on data you have seen while getting worse on data you have not | Train loss 0.013 while validation loss climbs 0.216 → 0.591 | M1 |
| **Overlap** | Shared text between neighbouring chunks, so a fact straddling a boundary appears whole somewhere | 8 words of a 30-word chunk | M6 |
| **Over-trust** | Acting on an AI answer without the checking you would apply to a human's | Accepting a citation without opening it | M9 |

---

## P

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Pairwise preference** | Asking which of two outputs is better, rather than scoring each alone | A vs B, then B vs A, to catch position bias | M4, M8 |
| **Parameter** | One learned number in the model | Tiny GPT has ~200,000; a frontier model has hundreds of billions | M3, M4 |
| **Path traversal** | Using `..` or an absolute path to escape a directory you were meant to stay inside | `sandbox/../../etc/passwd` | M7 |
| **PEFT** | Parameter-efficient fine-tuning — the family LoRA belongs to | 1.11% of parameters trainable | M8 |
| **Per-category breakdown** | Scores reported per class, with `n` on every row — never just an average | The table that catches the regression the average hides | M8, CAP |
| **Per-chunk floor** | The similarity score below which a chunk is dropped from the assembled context, even if it made the top-k | `0.10` | M6 |
| **Permutation equivariance** | Shuffling the inputs shuffles the outputs identically — no built-in sense of position | Why a transformer needs positional encodings and an RNN does not | M3 |
| **Perplexity** | How *surprised* a reference language model is by a piece of text — roughly, how many equally-likely words it was choosing between at each step. Low for real prose, very high for keyboard-mash | Used as an automatic quality filter in pretraining-corpus cleaning | M4 |
| **PII (personally identifiable information)** | Data that identifies a specific person — names, emails, phone numbers, addresses | Redacted from retrieved text **before** context assembly and **before** logging | M9 |
| **Position bias** | A judge preferring whichever answer it was shown first | 60% first-position win rate on a set that should be near 50/50 | M8 |
| **Positional encoding** | Information about a token's position, added to its vector | `x = tok_emb(idx) + pos_emb(arange(T))` | M3 |
| **Pre-norm** | Applying layer norm **inside** the residual branch rather than after the addition | `x + attn(ln(x))`, not `ln(x + attn(x))` | M3 |
| **Preference pair** | One prompt plus two responses, with a human saying which is better | `(prompt, chosen, rejected)` | M4 |
| **Pretraining** | Reading a huge pile of text and guessing the next token, trillions of times | 15 trillion tokens, months of GPUs, no human judgement anywhere | M4 |
| **Prompt caching** | Reusing a long unchanged prefix at roughly a tenth the price | `cache_control={"type": "ephemeral"}`; verify with `usage.cache_read_input_tokens` | M5 |
| **Prompt injection** | Hostile instructions hidden inside content the model reads as data | `IGNORE ALL PREVIOUS INSTRUCTIONS` planted in a retrieved note | M5, M7, M9 |
| **Prompt versioning** | Treating each prompt as a numbered artifact you can score, compare, and roll back | v1 zero-shot, v2 few-shot, v3 structured-with-rules | M5 |

---

## Q

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Query / Key / Value** | Three learned projections of a token: what it is looking for, what it advertises, and what it contributes | `Q = X·W_Q`, `K = X·W_K`, `V = X·W_V` | M3 |

---

## R

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **RAG (retrieval-augmented generation)** | Find the relevant passages first, then answer only from them | retrieve → assemble → generate → cite | M6 |
| **Rank (`r`)** | How wide the LoRA bottleneck is | `r = 8` | M8 |
| **Reasoning model** | An instruct model additionally trained with RL on tasks whose answers can be checked automatically | Thinks internally, then answers | M4 |
| **recall@k** | The fraction of questions whose answer appeared somewhere in the top `k` retrieved chunks | 8/10 = 0.80 at k = 3 | M6 |
| **Recurrent neural network (RNN)** | One small function applied once per item in a sequence, passing a summary vector forward | `h_t = tanh(W_xh·x_t + W_hh·h_(t−1) + b)` | M2 |
| **Red-teaming** | Structured, adversarial testing of your own system, with every attempt logged | 22 attempts across 5 categories, 5 hits, all mitigated and re-tested | M9, CAP |
| **Refusal path** | The permitted, designed way for the system to say it does not know | `NOT_IN_SOURCES`, fired below τ — and it costs $0.00000 | M6, CAP |
| **Regression** | A change that improves the average while breaking something that used to work | Urgency +2 but order_id −3; `out_of_scope` 0.80 → 0.40 | M5, M8 |
| **Residual connection** | Compute `x + f(x)` so the input flows past the block untouched | Makes the backward derivative `1 + f'(x)` — a gradient highway | M1 |
| **Residual risk** | What is still broken after you have fixed everything you could, written down on purpose | "Polite injections still pass; detector recall 0.75" | M9 |
| **Retention** | How long you keep logged data before deleting it, decided and written down in advance | "Traces are truncated to 400 characters and deleted after 30 days" | M9, CAP |
| **Retrieval failure** | The answer was never in the retrieved context | Fix chunking, overlap, `k`, or the embedder | M6 |
| **Retry path** | A capped second attempt that feeds the validation errors back into the prompt | 2 attempts, then raise loudly | M5 |
| **Reward hacking** | Getting a high score by exploiting the scorer instead of doing the task | Numbering everything, because numbering scores `+5` | M4, M9 |
| **Reward model** | A model that scores how much a human would like a response, trained only on comparisons | `r(response) = 9.625` | M4 |
| **RLHF** | Sample responses, score them with the reward model, push probability toward high scores — with a KL leash | PPO over four models in memory | M4 |
| **RMSProp** | Divide each weight's step by the recent typical size of that weight's own gradient | Lets a weight with `1e-5` gradients still move meaningfully | M1 |
| **Router** | The code that decides which component of your system handles a request, and logs why | `top < τ → refuse`; `NEEDS_MATH → agent`; otherwise `retrieve` | CAP |
| **Rubric** | A written checklist a grader applies, human or model | Four numbered pass conditions | M8 |

---

## S

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Sandbox** | The one directory an agent is permitted to write to | `agent_sandbox/`, enforced by `resolve()` then `is_relative_to()` | M7 |
| **Scaling by `√d_k`** | Dividing attention scores by the square root of the head dimension, to hold score variance at 1 | `√64 = 8`; without it the softmax saturates and gradients die | M3 |
| **Scaling law** | A fitted curve predicting loss from model size and data size | Chinchilla: about 20 tokens per parameter | M4 |
| **Self-attention** | Attention where the queries, keys and values all come from the same sequence | Every token attends over its own sentence | M3 |
| **Sequence** | An ordered list where the order carries meaning | "dog bit postman" ≠ "postman bit dog" | M2 |
| **SFT dataset** | Pairs of (input, desired output) demonstrating the behaviour you want | `("hi there", "greeting")` × 64 | M8 |
| **SGD** | Step every weight downhill by a fixed fraction of its gradient, one small random batch at a time | `torch.optim.SGD(params, lr=0.1)` | M1 |
| **Similarity threshold (τ)** | The retrieval score below which you refuse **without calling the model** | `τ = 0.25`, chosen from the gap between 0.19 and 0.31 | M6, CAP |
| **Sinusoidal encoding** | A fixed pattern of sines and cosines at geometric frequencies, added to token vectors | `sin(pos / 10000^(2i/d))`; extends past the training length | M3 |
| **Smoke test** | Three lines that prove the environment works before you rely on it | `python smoke.py` printing `torch.Size([1, 4, 4])` | SET |
| **Softmax saturation** | The region where one logit dominates so completely that the softmax's gradient is nearly zero | What `/√d_k` exists to prevent | M3 |
| **Sparse vector** | A vector that is mostly zeros, one slot per vocabulary word | TF-IDF over 30,000 words | M6 |
| **Specification gaming** | Optimizing the measurable proxy rather than the intended goal | The proxy was a faithful description of your data; the goal was not | M9 |
| **Spend budget** | A dollar ceiling checked **before** each API call | `budget_usd = 0.05` per agent run | M7, CAP |
| **Spine** | The single function in a system that turns a request into an answer, called by every interface | `answer(question) -> Answer` in `src/spine.py` | CAP |
| **Staged release** | Shipping to a small, informed group first, watching, then widening | The alternative to launching to everyone and finding out | M9 |
| **Stateless** | The API remembers nothing; you resend the whole history every call | Turn 5 sends all of turns 1–4 | M5 |
| **Stop condition** | Any rule that ends an agent run | `end_turn`, iteration cap, budget cap, too many tool errors | M7 |
| **`stop_reason`** | Why generation stopped this turn | `end_turn`, `tool_use`, `max_tokens`, `refusal` | M5, M7 |
| **Structured output** | Forcing the response to match a JSON schema at the API level | `output_config={"format": SCHEMA}` | M5 |
| **Supervised fine-tuning (SFT)** | Showing thousands of ideal answers and training only on the answer tokens | 50,000 (prompt, response) pairs | M4 |
| **System card** | The document describing a whole system's intended use, evaluation, limitations and out-of-scope uses | `SYSTEM_CARD.md`, ending with who should not rely on it | M9, CAP |
| **System prompt** | The standing instructions for the whole conversation, sent separately from the messages | "You answer questions using ONLY the passages provided." | M5 |

---

## T

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Teacher forcing** | Feeding the true previous token during training, regardless of what the model predicted | Training on "anika": step 3 always sees the real `n` | M2 |
| **Temperature** | Divide the logits by `T` before the softmax; low sharpens, high flattens | At `T = 0.5` the top token's probability rose from 0.579 to 0.831 | M2 |
| **TF-IDF** | Word counting, with common words downweighted | Scores 0.000 for two sentences that share no words but mean the same thing | M6 |
| **Token** | One unit the model actually reads — usually a subword piece, not a word | `"lowest"` → `[257, 101, 260]` | M4 |
| **Tokenizer** | The translator turning text into numbers the model can read, and back again | GPT-2's, with a 50,257-token vocabulary | M4 |
| **Tool** | A function the model may ask you to run, described in words and a JSON schema | `calculate`, `search_notes`, `write_file` | M7 |
| **Tool schema** | The JSON Schema saying which arguments are legal for a tool | `{"expression": {"type": "string"}}` | M7 |
| **`tool_result` block** | Your reply to a tool request, tagged with the same id. **All results for one turn go in one user message.** | `{"type": "tool_result", "tool_use_id": "toolu_01A", "content": ...}` | M7 |
| **`tool_use` block** | The model's request: this tool, these arguments, this id | `toolu_01A / calculate` | M7 |
| **top-k (retrieval)** | The `k` highest-scoring chunks returned by a search | `k = 3` | M6 |
| **Top-k sampling** | Keep only the `k` best tokens, renormalize, then sample | `k = 2` turned `[0.579, 0.213, 0.129, 0.078]` into `[0.731, 0.269, 0, 0]` | M2 |
| **Trace** | The append-only log of every decision, tool call and result, replayable after the fact | `trace.jsonl` | M7, CAP |
| **Transformer block** | Attention + MLP, each wrapped in pre-norm and a residual connection | `x = x + attn(ln1(x)); x = x + ff(ln2(x))` | M3 |

---

## U

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Unit vector** | A vector scaled so its length is exactly 1, which makes cosine similarity a plain dot product | `E /= np.linalg.norm(E, axis=1, keepdims=True)` | M6 |
| **Unrolling** | Drawing a recurrent loop as a chain of identical copies | A 40-step sequence becomes a 40-layer network | M2 |
| **Untrusted data** | Any content that came from outside your code — retrieved documents, tool output, user text — which is never an instruction | Wrapped in `<untrusted_data>` tags before it reaches the model | M7, M9 |

---

## V

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Validator** | Your own code checking that valid-*shaped* output also makes *sense* | Rejecting `order_id: "the customer did not give one"` | M5 |
| **Vanishing gradient** | The learning signal shrinking toward zero as it propagates back through many steps or layers | Measured `3.28e-12` at step 1 of a 40-step RNN | M1, M2 |
| **Vector database** | A dedicated store that holds embeddings and returns the nearest ones for you | FAISS, Chroma, pgvector — none of which you need until numpy is measurably too slow | M6 |
| **Vector index** | The stored matrix of chunk embeddings, plus the search code over it | A `15 × 384` matrix and one matrix multiply | M6 |
| **Virtual environment (venv)** | A private folder holding one project's packages, so one level's install cannot break another's | `python3 -m venv .venv` in `~/ai-academy/level4` | SET |
| **Vocabulary size** | How many distinct tokens exist — the tokenizer's whole alphabet | GPT-2: 50,257 | M4 |

---

## W

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Warmup** | Ramping the learning rate linearly from ~0 up to peak over the first few percent of steps | 5% warmup stops Adam taking a huge step on a garbage variance estimate | M1 |
| **Weight decay** | Shrinking every weight slightly toward zero each step | `weight_decay=0.01` — a "rent" unhelpful weights cannot pay | M1 |
| **Weight sharing** | Using the same parameters at every time step of a recurrence | Why an RNN handles any length with a fixed parameter count — and why its gradients are a power | M2 |

---

## Z

| Term | Plain-English definition | Example from this course | Module |
|---|---|---|:--:|
| **Zero-shot** | Describing the task in words with no examples | "Classify this ticket." | M5 |
| **`zero_grad()`** | Clearing the accumulated gradients before computing new ones. PyTorch never does this for you. | `opt.zero_grad(set_to_none=True)` — forgetting it is the loudest silent bug in the level | M1 |

---

## 🔗 Terms carried in from earlier levels

These are assumed, not re-taught. If any of them is fuzzy, follow the link before Module 1.

| Term | Where it was taught |
|---|---|
| accuracy, precision, recall, F1, threshold, cost of errors | [L3 M3](../level-3-engineer/module-03-evaluation-metrics.md) |
| train / validation / test split, leakage, baseline | [L3 M1–M2](../level-3-engineer/module-01-the-supervised-pipeline.md) |
| gradient descent, loss function, learning rate, the chain rule | [L3 M4](../level-3-engineer/module-04-logistic-regression-gradient-descent.md) |
| forward pass, backpropagation, softmax, cross-entropy, ReLU | [L3 M5](../level-3-engineer/module-05-neural-networks-from-scratch.md) |
| tensor, `shape`, `dtype`, device, autograd, `model.eval()`, `state_dict` | [L3 M6](../level-3-engineer/module-06-pytorch-deep-learning.md) |
| convolution, transfer learning, freezing a backbone | [L3 M7](../level-3-engineer/module-07-cnns-for-images.md) |
| PCA, clustering, explained variance | [L3 M8](../level-3-engineer/module-08-unsupervised-kmeans-pca.md) |
| tokens (naive), bag-of-words, TF-IDF, cosine similarity, embeddings | [L3 M9](../level-3-engineer/module-09-classic-nlp.md) |
| artifact, versioning, prediction log, latency, model card, monitoring | [L3 Capstone](../level-3-engineer/capstone.md) |
| DataFrame, `groupby`, numpy broadcasting, `axis=0` vs `axis=1` | [L2 M5–M6](../level-2-builder/module-05-numpy-arrays.md) |

---

## 📌 The twelve terms that matter most

If you forget everything else on this page, keep these. They are the ones that change how you work rather than what you know.

| Term | Why it matters more than the others |
|---|---|
| **Frozen test set** | Every claim you will ever make about a system depends on whether this was written first. |
| **Grounding** | The difference between an answer and a plausible sentence. |
| **Refusal path** | A system that cannot say "I don't know" will always invent. Abstention is a feature you build. |
| **Guardrail** | Code that refuses. Not a prompt that asks. This distinction is the whole of Module 7 and half of Module 9. |
| **Untrusted data** | Retrieved text and tool output are data. Treating them as instructions is the vulnerability. |
| **Regression** | The average can go up while the product gets worse. Per-category breakdowns exist for this. |
| **Causal mask** | One tensor operation between a working GPT and label leakage — and it fails silently. |
| **Vanishing gradient** | The reason LSTMs exist, and then the reason attention exists. Two eras of architecture, one problem. |
| **Scaling by `√d_k`** | Proof that the transformer's details are derived, not guessed. |
| **Cohen's κ** | The number that stops you mistaking agreement for correctness. |
| **Specification gaming** | Your system optimizes what you measured, not what you meant. Always. |
| **"Who should not rely on this"** | The last section of a system card, and the sentence that separates an engineer from a salesperson. |

---

[Level 4 Home](README.md) · [Assessment](assessment.md) · [Capstone](capstone.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Level 3 Glossary](../level-3-engineer/glossary.md)
