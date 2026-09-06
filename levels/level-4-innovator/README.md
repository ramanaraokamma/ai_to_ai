```
  ██╗     ███████╗██╗   ██╗███████╗██╗       ██╗  ██╗
  ██║     ██╔════╝██║   ██║██╔════╝██║       ██║  ██║
  ██║     █████╗  ██║   ██║█████╗  ██║       ███████║
  ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║       ╚════██║
  ███████╗███████╗ ╚████╔╝ ███████╗███████╗       ██║
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝       ╚═╝

  ██╗███╗   ██╗███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗
  ██║████╗  ██║████╗  ██║██╔═══██╗██║   ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
  ██║██╔██╗ ██║██╔██╗ ██║██║   ██║██║   ██║███████║   ██║   ██║   ██║██████╔╝
  ██║██║╚██╗██║██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║   ██║   ██║   ██║██╔══██╗
  ██║██║ ╚████║██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║   ██║   ╚██████╔╝██║  ██║
  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

# 🚀 Level 4 — Innovator

### *Modern AI is attention plus scale plus a learning signal from humans — and you can build every piece.*

**Grade band:** 11–12 (ages ~16–18) · **Coding required:** fluent PyTorch — you can write a training loop from a blank file · **Math required:** matrices, dot products, derivatives, and basic probability
**Duration:** ~28 weeks · 9 modules (~6–8 h each) + a ~20 h capstone · **~79 hours total**

[⬅ Level 3](../level-3-engineer/) · [Back to AI Academy](../../README.md) · [Full curriculum map](../../CURRICULUM_MAP.md) · [Glossary](glossary.md) · [Assessment](assessment.md) · [Capstone](capstone.md)

---

## 🪝 Why This Level Exists

There is a sentence you have probably heard, and it is a lie: *"Nobody really knows how these things work."*

People say it because a frontier language model has hundreds of billions of parameters and nobody can read them. That part is true. But the *machine* is not mysterious. It is a stack of one repeated block. That block does two things: every token looks at the other tokens it needs, and then every token passes through a small two-layer network. That is it. Wrap that stack in a training objective — guess the next token — pour in trillions of tokens, then shape the result with a few thousand human judgements about which of two answers is better.

Nine modules from now you will have written every one of those pieces yourself.

```
   Modules 1–3  ·  THE MACHINE.
                   Get training under control. Meet the memory problem
                   that recurrence cannot solve. Then build attention,
                   multi-head attention, a transformer block, and a GPT
                   that generates readable English — from a blank file.

   Modules 4–5  ·  THE PIPELINE AND THE INTERFACE.
                   How a tiny GPT becomes a frontier model: tokenizers,
                   pretraining, scaling laws, SFT, reward models, RLHF,
                   DPO. Then how you talk to one on purpose, with a
                   frozen test set and a scorer instead of vibes.

   Modules 6–8  ·  THE PRODUCT.
                   Give the model your documents (RAG). Give it hands
                   (agents). Change its weights and prove the change
                   helped — and find the thing it broke.

   Module  9    ·  THE PART WHERE YOU ATTACK YOUR OWN WORK.
                   Alignment, injection, PII, red-teaming, system cards.
```

Here is the honest shape of the level. **Modules 1–4 are about how the machine is built. Modules 5–9 are about how a system around it is engineered.** Both halves matter, and most people only ever learn one. Somebody who can implement attention but ships an agent with no iteration cap is dangerous. Somebody who can wire an API but thinks the model is a wizard cannot debug it when it fails.

You are going to be neither.

---

## 🎯 Level Outcomes

When you finish Level 4 you will be able to:

1. **Diagnose and tune deep-network training from its loss curves**, choosing optimizers, schedules, and regularization deliberately rather than by superstition.
2. **Implement scaled dot-product attention, multi-head attention, and a full transformer block from scratch**, and train a character-level GPT until it generates readable text.
3. **Explain pretraining, supervised fine-tuning, reward models, and RLHF/DPO precisely**, and implement a byte-pair-encoding tokenizer that round-trips text exactly.
4. **Treat prompting as engineering** — versioned prompts, structured outputs, a frozen test set, and a measured eval harness.
5. **Build a complete RAG system** with chunking, embeddings, vector search, citations, and a refusal path that fires when retrieval fails.
6. **Build a tool-using agent** with real tool schemas, a bounded loop, a full trace log, and guardrails that refuse even when the model insists.
7. **Fine-tune a small model and prove both the win and the regression** with an evaluation suite you froze before you started.
8. **Red-team your own system**, document each exploit, ship mitigations, re-test, and publish a system card.

> **The one-line test of whether you finished this level:** someone shows you a chatbot that gave a wrong answer, and you can tell them — with evidence — whether it was a retrieval failure, a generation failure, a prompt failure, a tokenizer artefact, or a person who trusted a suggestion that was clearly labelled as one.

---

## 🎒 What You Need Before Starting

### Prerequisites — the honest list

| You need | Why | If you don't have it |
|---|---|---|
| **Level 3 finished** — including the capstone | Module 1 opens by assuming you can write a PyTorch training loop and read a loss curve | Do [Level 3](../level-3-engineer/). Module 1 here starts at Level 3 Module 6's finishing speed. |
| A PyTorch training loop **from memory** — `zero_grad → forward → loss → backward → step` | You will type it about forty times in this level, with variations | [L3 M6](../level-3-engineer/module-06-pytorch-deep-learning.md). If you have to look it up, drill it for a week first. |
| Tensor shapes: `(batch, seq, features)`, `reshape`, `transpose`, `@` | Module 3 is 80% shape arithmetic. A wrong `transpose` there is invisible and fatal. | [L3 M6](../level-3-engineer/module-06-pytorch-deep-learning.md). Habit: print `.shape` after every line for a week. |
| **Matrix multiplication by hand**, including which dimensions have to match | You will compute a 3×2 attention matrix with a pen in Module 3 before you code it | Any algebra text. `(3,4) @ (4,2) → (3,2)`; the inner numbers vanish and must agree. |
| What a **derivative** is, and the chain rule as "multiply the local slopes" | Modules 1 and 2 are about gradients getting too big, too small, or too noisy | [L3 M4–M5](../level-3-engineer/module-04-logistic-regression-gradient-descent.md). You do not need to *compute* derivatives here — you need to reason about them. |
| **softmax** and **cross-entropy**, and why they are always paired | Every model in this level ends in a softmax over a vocabulary | [L3 M5](../level-3-engineer/module-05-neural-networks-from-scratch.md) |
| **Cosine similarity** and **TF-IDF** | Module 6 opens with them and immediately shows where they break | [L3 M9](../level-3-engineer/module-09-classic-nlp.md) |
| Precision, recall, thresholds, and the idea of a **cost of errors** | Modules 6, 8, and 9 all report scores by subgroup and by category | [L3 M3](../level-3-engineer/module-03-evaluation-metrics.md) |
| A **credit card belonging to an adult who has agreed**, or a school-provided API key | Modules 5–9 and the capstone call the Claude API. This costs real money. | See the money box below. There is a free path for Modules 1–4 and for large parts of 6 and 8. |
| Comfort with being wrong **in writing** | Module 9 makes you publish a list of ways you broke your own system | This is the level where "I don't know" stops being an admission and becomes a feature you implement |

### The kit

```
   ┌──────────────────────────────────────────────────────────────────┐
   │  THE LEVEL 4 KIT                                                 │
   ├──────────────────────────────────────────────────────────────────┤
   │  □  A laptop — macOS / Windows / Linux. Apple Silicon (MPS) or   │
   │     an NVIDIA GPU is a nice-to-have, never a requirement.        │
   │  □  ~12 GB free disk. torch is ~2.5 GB, transformers +           │
   │     sentence-transformers pull ~1 GB of model weights.           │
   │  □  An Anthropic API key, and a spending limit set on the        │
   │     console BEFORE your first call. Non-negotiable.              │
   │  □  A folder ~/ai-academy/level4 you never delete                │
   │  □  A notebook and pen. Module 3 makes you compute a full        │
   │     attention pass by hand before you are allowed to code it.    │
   │  □  A free Google account for Colab — the GPU fallback for       │
   │     Modules 3 and 8 if your laptop is slow                       │
   │  □  journal.md, one dated entry per session, carried over        │
   │     from Level 3                                                 │
   └──────────────────────────────────────────────────────────────────┘
```

### 💳 The money conversation — read this with an adult

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  WHAT THIS LEVEL COSTS, HONESTLY                                     │
   ├──────────────────────────────────────────────────────────────────────┤
   │                                                                      │
   │  Modules 1, 2, 3, 4     $0.00   — all local, all CPU, no accounts    │
   │  Module 5 (Prompt Bench) ~$1.50 — 3 versions × 20 cases × ~15 runs   │
   │  Module 6 (RAG)          ~$1.00 — Parts A–E are offline and free     │
   │  Module 7 (Agents)       ~$2.00 — loops cost more than single calls  │
   │  Module 8 (Fine-tune)    ~$2.00 — the judge and baselines only       │
   │  Module 9 (Red-team)     ~$2.00                                      │
   │  Capstone                ~$5.00                                      │
   │  ───────────────────────────────                                     │
   │  Expected total          ~$14    Budget $25 and you will be fine.    │
   │                                                                      │
   │  ⚠️  A single runaway loop can spend $50 in four minutes.            │
   │      Set a hard monthly limit in the Anthropic console TODAY,        │
   │      before your first call. Then set a second, smaller limit        │
   │      in your own code — Module 5 gives you the BudgetGuard class     │
   │      and every later module reuses it.                               │
   │                                                                      │
   │  Claude Sonnet 5 pricing used throughout:                            │
   │      $2.00 per million input tokens                                  │
   │     $10.00 per million output tokens                                 │
   │  Output costs 5× input. "Make it stop explaining itself" is a        │
   │  cost lever, not just a style preference.                            │
   └──────────────────────────────────────────────────────────────────────┘
```

> ⚠️ **A grown-up should read this bit.** Modules 1–4 run entirely on the learner's own machine with no accounts and no network beyond `pip install`. From Module 5 onwards the learner sends text to Anthropic's API over the internet. **Nothing personal should ever go into a prompt** — the course's example data is invented customer-support tickets and the learner's own lab notes about optimizers. Module 9 covers PII, logging, and retention explicitly and makes the learner write down what their own system stores. Set a spending cap on the API console before handing over the key.

> ⚠️ **No GPU? Genuinely fine.** Module 3's Tiny GPT trains in about 2 minutes on a laptop CPU. Module 8's DistilBERT fine-tune takes 2–4 minutes. Everything in this level is deliberately sized so that waiting is never the bottleneck — thinking is.

---

## 🗺️ The Roadmap

```
        LEVEL 4 · INNOVATOR — from "fit() is a loop" to "here is the system card"

   PART ONE — THE MACHINE
   ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
   │  1. DEEP LEARNING  │      │  2. SEQUENCE       │      │  3. ATTENTION &    │
   │     AT DEPTH       │─────►│     MODELS         │─────►│     TRANSFORMERS   │
   │                    │      │                    │      │                    │
   │  SGD → momentum    │      │  hidden state      │      │  Q · K · V         │
   │  → Adam → AdamW    │      │  unrolling · BPTT  │      │  scores/√d_k       │
   │  warmup · cosine   │      │  vanishing grads   │      │  CAUSAL MASK       │
   │  dropout · decay   │      │  LSTM/GRU gates    │      │  multi-head        │
   │  batch vs layer    │      │  teacher forcing   │      │  positions         │
   │  norm · residuals  │      │  temp · top-k      │      │  🏗️ A REAL GPT     │
   └────────────────────┘      └─────────┬──────────┘      └─────────┬──────────┘
     "the ten knobs                       │ "memory in ONE            │
      nobody explained"                   │  vector fails —           │ you built
                                          │  measured: 3.28e-12"      │ the thing.
                                          └──────────────────────────►│ now: how is
                                                                      │ the real one
   PART TWO — THE PIPELINE AND THE INTERFACE                          │ made?
   ┌────────────────────┐      ┌────────────────────┐                 ▼
   │  5. PROMPT         │◄─────│  4. HOW LLMs ARE   │◄────────────────┘
   │     ENGINEERING    │      │     ACTUALLY       │
   │                    │      │     TRAINED        │
   │  messages API      │      │                    │
   │  few-shot examples │      │  BPE from scratch  │
   │  delimiters        │      │  pretraining       │
   │  JSON + validate   │      │  scaling · C≈6ND   │
   │  FROZEN test set   │      │  SFT · reward model│
   │  cost per call     │      │  RLHF · DPO        │
   └─────────┬──────────┘      └────────────────────┘
             │ you can talk to it
             │ and MEASURE the talking
             ▼
   PART THREE — THE PRODUCT
   ┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
   │  6. EMBEDDINGS,    │      │  7. TOOL-USING     │      │  8. FINE-TUNING &  │
   │     VECTORS, RAG   │─────►│     AGENTS         │─────►│     EVALUATING     │
   │                    │      │                    │      │                    │
   │  dense vs TF-IDF   │      │  tool schemas      │      │  prompt/retrieve/  │
   │  cosine · top-k    │      │  perceive→decide→  │      │    fine-tune       │
   │  chunk size/overlap│      │    act→observe     │      │  LoRA · PEFT       │
   │  cite every claim  │      │  iteration budget  │      │  exact/rubric/judge│
   │  REFUSE below τ    │      │  sandbox · trace   │      │  kappa · position  │
   │  recall@k          │      │  ⚠️ INJECTION      │      │  ⚠️ THE REGRESSION │
   └────────────────────┘      └─────────┬──────────┘      └─────────┬──────────┘
                                          │  the agent you            │
                                          │  are about to attack      │
                                          ▼                           │
                               ┌────────────────────┐                 │
                               │  9. RESPONSIBLE &  │◄────────────────┘
                               │     SAFE AI        │
                               │                    │
                               │  alignment         │
                               │  hallucination vs  │
                               │    miscalibration  │
                               │  RED-TEAM YOUR OWN │
                               │  PII · copyright   │
                               │  bias in generation│
                               │  📄 SYSTEM CARD    │
                               └─────────┬──────────┘
                                         │
                    ╔════════════════════▼═════════════════════════════════╗
                    ║   🚀  CAPSTONE — BUILD AN AI PRODUCT  (~20 h)        ║
                    ║                                                      ║
                    ║   a design doc · at least two of {RAG, agent,        ║
                    ║   fine-tuned model} · an eval harness of 25+ cases   ║
                    ║   that runs on demand · a MEASURED cost and latency  ║
                    ║   budget · guardrails with a documented red-team     ║
                    ║   pass · a 5-minute demo · a system card · and the   ║
                    ║   honest section: what it fails at, and who should   ║
                    ║   not rely on it.                                    ║
                    ╚══════════════════════════════════════════════════════╝
```

**Read the arrows as "you need this before that."** Module 1's AdamW, warmup, layer norm, and residuals are literally the settings Module 3's GPT trains with. Module 2's vanishing-gradient measurement is the *reason* attention exists — do not skip it, the punchline lands nowhere else. Module 3's model is the thing Module 4 explains the industrial version of. Module 6's vector index becomes Module 7's `search_notes` tool. Module 7's agent is the target Module 9 attacks. Nothing here is decoration.

> 🔍 **Notice where the pen appears.** Module 3 makes you compute a full three-token attention pass by hand — every dot product, the `/√2`, the mask, the softmax, the weighted sum — *before* you write a line of PyTorch. Then the code prints the same numbers. That moment, when `0.751` shows up on the screen because you already knew it would, is when attention stops being a diagram and becomes arithmetic you own.

---

## 📚 The Nine Modules

| # | Module | You'll build | Time |
|:--:|---|---|:--:|
| 1 | [**Deep Learning at Depth: Optimizers, Regularization, and Debugging Training**](module-01-deep-learning-at-depth.md) | 🔬 **Training Diagnostics Lab** — six controlled runs on one fixed network, each isolating exactly one knob (LR, batch size, dropout, weight decay, normalization, schedule), all curves on shared axes, distilled into your own one-page if-you-see-this-do-that tuning playbook | ~6 h |
| 2 | [**Sequence Models: RNNs, LSTMs, and the Memory Problem**](module-02-sequence-models.md) | 🔤 **Name Generator** — a char-level RNN trained on 231 typed-in names that invents pronounceable new ones, sampled at three temperatures, plus a plot of gradient magnitude against sequence position showing decay to `3.28e-12` and a written explanation of why | ~6 h |
| 3 | [**Attention and Transformers: Build a Tiny GPT**](module-03-attention-and-transformers.md) | 🧲 **Tiny GPT** — attention, multi-head attention, a transformer block, and a full GPT written from scratch in PyTorch, trained on ~7,000 typed-in characters, with samples at three checkpoints, a loss curve, and an interpretable attention heatmap | ~8 h |
| 4 | [**How LLMs Are Actually Trained: Pretraining, SFT, and RLHF**](module-04-how-llms-are-trained.md) | 🧬 **Tokenizer + Life-of-an-LLM** — byte-pair encoding implemented from scratch that round-trips text exactly, benchmarked against a Hugging Face tokenizer, plus 10 hand-scored preference pairs, a Bradley–Terry reward model, a DPO demo, and the four-stage training-story explainer | ~6 h |
| 5 | [**Prompt Engineering as a Real Engineering Skill**](module-05-prompt-engineering.md) | 📊 **Prompt Bench** — a 20-case frozen test set, a programmatic scorer, three prompt versions (zero-shot / few-shot / structured-with-rules) run through the Claude API, and a results table with score, token cost, and latency per version | ~6 h |
| 6 | [**Embeddings, Vector Search, and RAG**](module-06-embeddings-vector-search-rag.md) | 🔎 **Ask My Notes** — a full RAG system over your own AI Academy lab notebook: chunking, embeddings, a vector index, top-k retrieval, cited generation, a similarity threshold τ, and a refusal path — tested on 10 questions of which 2 are deliberately unanswerable | ~7 h |
| 7 | [**Tool-Using AI Agents: The Loop That Does Things**](module-07-ai-agents.md) | 🤖 **Three-Tool Agent** — calculator + search-my-notes + write-file-to-sandbox, a bounded loop with `MAX_ITERATIONS = 10` and a dollar cap, full `trace.jsonl` logging, path-traversal guards, and five multi-step tasks that all complete or fail gracefully | ~7 h |
| 8 | [**Fine-Tuning and Evaluating LLMs**](module-08-finetuning-and-evaluating-llms.md) | 🎯 **Eval Suite + Fine-Tune** — a 30-case eval suite frozen *before* training, a deduplicated SFT set, a DistilBERT fine-tune, LoRA in fifteen lines, an LLM judge checked with Cohen's κ and a position-bias flip test, and a per-category report that names a real regression | ~7 h |
| 9 | [**Responsible and Safe AI: Alignment, Red-Teaming, and Shipping Without Harm**](module-09-responsible-and-safe-ai.md) | 🛡️ **Red-Team Report** — a structured attack campaign against your own Module 7 agent across five categories (injection via a retrieved document, sandbox escape, PII extraction, budget exhaustion, confident wrongness), every successful exploit logged, a mitigation shipped for each, all re-tested, and a published system card | ~6 h |
| 🚀 | [**CAPSTONE — Build an AI Product**](capstone.md) | 📦 Something a stranger would actually use: design doc, a system combining at least two of {RAG, agent, fine-tuned model}, a 25+ case eval harness, a measured cost and latency budget, guardrails with a red-team pass, a 5-minute demo, a system card, and the honest section | ~20 h |

**Also in this folder:**

| File | What it's for | When to use it |
|---|---|---|
| [`assessment.md`](assessment.md) | 20 multiple-choice + 8 short-answer + 4 debug problems, spanning all nine modules, with an explained answer key for every single item | Week 22 — after Module 9, before the capstone |
| [`glossary.md`](glossary.md) | Every term introduced in this level — 212 of them — alphabetized, with a plain definition, the actual example from the course, and the module tag | Any time a word stops making sense |
| [`capstone.md`](capstone.md) | The final build: brief, milestones, scaffold, a worked solution for the hardest milestone, rubric, demo script | Weeks 23–28 |

---

## 🧭 How This Level Fits the Whole Journey

### What Level 3 gave you

Level 3 taught you to build and ship *one model*. Level 4 makes that model a component inside a system. Here is the exact mapping:

```
   ┌───────────────────────────────────────────────────────────────────────────┐
   │  LEVEL 3 (you built it)           ─►   LEVEL 4 (it becomes...)      Mod   │
   ├───────────────────────────────────────────────────────────────────────────┤
   │  loss.backward(); opt.step()      ─►   momentum, Adam, AdamW,        M1   │
   │                                        warmup, cosine decay, and          │
   │                                        knowing WHICH to reach for         │
   │  "the model overfit"              ─►   six controlled experiments,   M1   │
   │                                        one knob each, on shared axes      │
   │  a hidden layer                   ─►   a transformer block:          M3   │
   │                                        attention + MLP + residual        │
   │                                        + pre-norm, stacked                │
   │  TF-IDF + cosine similarity       ─►   dense embeddings, a vector    M6   │
   │                                        index, and recall@k                │
   │  "bag-of-words threw away order"  ─►   the exact failure that        M2   │
   │                                        motivated recurrence, then         │
   │                                        the failure that killed it    M3   │
   │  softmax over 10 classes          ─►   softmax over a 50,257-token   M4   │
   │                                        vocabulary, once per position      │
   │  a train/val/test split           ─►   a FROZEN eval set, written    M5   │
   │                                        before the first prompt exists M8  │
   │  precision, recall, thresholds    ─►   recall@k, exact match,        M6   │
   │                                        rubric scoring, LLM-as-judge, M8   │
   │                                        Cohen's κ, position bias           │
   │  a model card with subgroups      ─►   a SYSTEM card: intended use,  M9   │
   │                                        evals, limits, out-of-scope        │
   │  logging every prediction         ─►   a full agent trace: every     M7   │
   │                                        decision, tool call, and result    │
   │  "bind to 127.0.0.1, know why"    ─►   sandboxes, allowlists,        M7   │
   │                                        iteration caps, spend caps,   M9   │
   │                                        and prompt injection               │
   └───────────────────────────────────────────────────────────────────────────┘
```

If you did Level 3 properly, nothing in the right-hand column is *alien* — it is the same instinct pointed at a bigger machine. That is why Module 1 can open at speed: it is tuning a car you already know how to drive.

If you skipped Level 3: Module 3 will end you. Not because attention is hard — it is a dot product, a divide, a softmax and a weighted average — but because you will be debugging tensor shapes while also learning what a tensor shape is. Go do [Level 3 Modules 4, 5, 6 and 9](../level-3-engineer/) at minimum.

### What comes after — and there is no Level 5

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │                                                                     │
   │   Level 1 gave you the concepts with your hands.                    │
   │   Level 2 gave you the keyboard.                                    │
   │   Level 3 gave you the maths under the hood and the discipline      │
   │           to ship.                                                  │
   │   Level 4 gives you the frontier.                                   │
   │                                                                     │
   │   There is no Level 5, because Level 5 is the part nobody           │
   │   writes a curriculum for. It is a real problem, a real user,       │
   │   and nobody checking your answer key.                              │
   │                                                                     │
   └─────────────────────────────────────────────────────────────────────┘
```

That said, "no Level 5" does not mean "nothing after." It means the next thing is chosen by you rather than handed to you. Here is what this level deliberately prepares you for, and what it deliberately does not:

| What you'll be able to walk into | What Level 4 gave you | What is still missing, honestly |
|---|---|---|
| **A university ML course** | Attention derived, backprop understood, optimizers compared, PyTorch fluency | Measure-theoretic probability, convex optimization proofs, the linear algebra behind why `√d_k` is the right scale |
| **An open-source contribution** | You can read a transformer implementation and know what every line does | Git at team scale, code review, tests, CI, someone else's abstractions |
| **A research paper (reading one)** | You know the vocabulary: ablation, scaling law, PEFT, RLHF, contamination, κ | Reading a paper's *claims* against its *evidence* — a skill that takes about thirty papers |
| **Your own product** | The whole capstone: design doc, evals, budget, guardrails, system card | Users. Real users, who will do things you did not imagine. |
| **A conversation with an ML engineer** | You can ask "what's your eval set, and was it frozen before you tuned?" and mean it | Nothing. That question alone will get you taken seriously. |

> **The honest limit of this course.** You have trained a model with about 200,000 parameters on 7,000 characters. Frontier models are a million times bigger and trained on a trillion times more text. Scale changes things this course cannot show you — behaviours that appear only at size, failure modes that are statistical rather than mechanical, and costs measured in megawatts. What does *not* change is the machine. The block you wrote is the block they use. Hold on to that, and be suspicious of anyone who tells you the difference is magic.

---

## 🔧 Environment Setup

Budget **50 minutes**. Do it in **week 0 — before Module 1**. Run every smoke test. A half-installed environment costs a whole evening in week 5 and you will blame the wrong thing.

### Step 1 — Check your Python (5 min)

```bash
python3 --version
```

| What you see | What to do |
|---|---|
| `Python 3.11.x` or `3.12.x` | ✅ Ideal. Every output in this level was checked on 3.11 and 3.12. |
| `Python 3.10.x` | ✅ Fine. |
| `Python 3.13.x` | ⚠️ Usually fine now, but check a `torch` wheel exists before committing. If `pip install torch` fails, install 3.12 alongside. |
| `Python 3.9` or older | ❌ `anthropic` 1.x requires 3.10+. Install 3.11 from [python.org](https://www.python.org/downloads/). |

### Step 2 — A fresh environment for this level (10 min)

Do **not** reuse Level 3's venv. `transformers` pins `tokenizers`, `sentence-transformers` pins `torch`, and one bad resolution will break a level you already finished.

```bash
# 1) One folder for the whole level. Never delete this.
mkdir -p ~/ai-academy/level4
cd ~/ai-academy/level4

# 2) Create the private box
python3 -m venv .venv

# 3) Step INTO the box
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows PowerShell
```

Your prompt must now start with `(.venv)`. It does not persist between terminal sessions — run the activate line every time.

### Step 3 — Install the stack (20 min, ~4 GB download)

Install in two waves. Wave 1 gets you through Modules 1–4 with no account and no API key. Wave 2 is only needed from Module 5 onwards, but installing it now means you find the problems now.

```bash
python -m pip install --upgrade pip

# ---- WAVE 1: Modules 1-4. Local only. No accounts, no keys. ----
python -m pip install torch numpy matplotlib scikit-learn

# ---- WAVE 2: Modules 4-9. Needed from Module 4's tokenizer comparison on. ----
python -m pip install transformers tokenizers datasets
python -m pip install sentence-transformers
python -m pip install anthropic pydantic
```

> ⚠️ **Windows + NVIDIA GPU?** Plain `pip install torch` may give you a CPU-only build. **That is fine for this whole level.** If you want CUDA, get the exact command for your CUDA version from [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/). Do not guess it.

> ⚠️ **Apple Silicon (M1/M2/M3/M4)?** MPS ships in the default install. Nothing extra to do. Modules 1–3 auto-detect it.

What you just installed, and where it first appears:

| Package | What it does | First used |
|---|---|---|
| `torch` | Tensors, autograd, `nn.Module`, optimizers | M1 |
| `numpy` | Array maths, the hand-checks | M1 |
| `matplotlib` | Loss curves, gradient-decay plots, attention heatmaps | M1 |
| `scikit-learn` | `TfidfVectorizer`, cosine similarity, the offline embedder fallback | M6 |
| `transformers` | GPT-2's tokenizer (M4), DistilBERT (M8) | M4 |
| `tokenizers` | The fast Rust BPE you benchmark your own against | M4 |
| `datasets` | Hugging Face dataset loading for M8 | M8 |
| `sentence-transformers` | `all-MiniLM-L6-v2`, the 384-dimension dense embedder for RAG | M6 |
| `anthropic` | The Claude SDK: `client.messages.create(...)` | M5 |
| `pydantic` | Validating the JSON the model gives back | M5 |

Minimum versions this level's outputs were checked against: `torch 2.2+`, `numpy 1.26+` (2.x fine), `matplotlib 3.7+`, `scikit-learn 1.4+`, `transformers 4.40+`, `sentence-transformers 3.0+`, `anthropic 1.0+`, `pydantic 2.0+`.

### Step 4 — Your API key and your spending cap (10 min, do it in this order)

**Cap first. Key second.** Every year somebody does it the other way round and learns about runaway loops the expensive way.

1. Go to the Anthropic console with the adult who owns the card.
2. **Set a hard monthly spend limit.** $25 is generous for this whole level.
3. Create an API key. Copy it once — you cannot see it again.
4. Put it in your environment, **never in a file you commit**:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."       # macOS / Linux, this terminal only
setx ANTHROPIC_API_KEY "sk-ant-..."         # Windows, permanent (reopen the terminal)
```

To make it stick on macOS/Linux, add the `export` line to `~/.zshrc` or `~/.bashrc`.

> 🔑 **The rule you will break exactly once.** Never paste a key into a `.py` file, a notebook cell, or a screenshot. Keys leak through screen-shares, through git history, and through "I'll take it out later." If you think a key leaked, revoke it on the console immediately — that takes ten seconds and costs nothing.

### Step 5 — The 3-line smoke test (2 min)

Create `smoke.py` in `~/ai-academy/level4`:

```python
import torch, transformers, sentence_transformers, anthropic
device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
print("L4 ready · torch", torch.__version__, "· device:", device,
      "· attn shape:", (torch.randn(1, 4, 8) @ torch.randn(1, 8, 4)).shape,
      "· key set:", bool(__import__("os").environ.get("ANTHROPIC_API_KEY")))
```

```bash
python smoke.py
```

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  🚀 LEVEL 4 SMOKE TEST                                              │
   ├─────────────────────────────────────────────────────────────────────┤
   │                                                                     │
   │  ✅ PASS looks like:                                                │
   │      L4 ready · torch 2.5.1 · device: mps                           │
   │        · attn shape: torch.Size([1, 4, 4]) · key set: True          │
   │      (your versions will differ; `device: cpu` is a PASS too)       │
   │                                                                     │
   │  ❌ FAIL looks like:                                                │
   │      ModuleNotFoundError: No module named 'anthropic'               │
   │      → troubleshooting row 1                                        │
   │                                                                     │
   │      key set: False                                                 │
   │      → troubleshooting row 2 (not fatal until Module 5)             │
   └─────────────────────────────────────────────────────────────────────┘
```

That `torch.Size([1, 4, 4])` is not decoration. It is `(1,4,8) @ (1,8,4) → (1,4,4)` — a batch of one, four tokens, each scoring against four tokens. **That is literally the shape of an attention score matrix.** If it printed, your tensor library can do the central operation of this entire level.

### Step 6 — Prove the API works, for one twentieth of a cent (3 min)

Create `smoke_api.py`:

```python
import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from the environment

# FREE: count tokens before you spend anything.
count = client.messages.count_tokens(
    model="claude-sonnet-5",
    system="You are terse.",
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
)
print("input tokens (free to check):", count.input_tokens)

# COSTS MONEY: about $0.00006. Six thousandths of a cent.
resp = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=16,
    system="You are terse.",
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
)
print("reply      :", resp.content[0].text.strip())
print("stop_reason:", resp.stop_reason)
print("usage      :", resp.usage.input_tokens, "in /", resp.usage.output_tokens, "out")
print("cost       : $%.6f" % (resp.usage.input_tokens/1e6*2.00 + resp.usage.output_tokens/1e6*10.00))
```

```
input tokens (free to check): 21
reply      : ready
stop_reason: end_turn
usage      : 21 in / 2 out
cost       : $0.000062
```

Three habits are being installed here and all three carry through to the capstone: **count before you send** (`count_tokens` is free), **read `stop_reason` every time** (`max_tokens` means you got truncated), and **price every call** from `response.usage`, not from a guess.

### Step 7 — Prove the embedder downloads (5 min, needed by Module 6)

`sentence-transformers` pulls ~90 MB of model weights on first use. School networks block this surprisingly often, so find out in week 0, not week 13. Create `smoke_embed.py`:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")     # ~90 MB on first run only
v = model.encode(["the optimizer diverged", "training blew up"],
                 normalize_embeddings=True)
print("shape:", v.shape)
print("cosine('the optimizer diverged', 'training blew up') =", float(v[0] @ v[1]))
```

```
shape: (2, 384)
cosine('the optimizer diverged', 'training blew up') = 0.6431
```

Those two sentences share **zero words**. TF-IDF would score them 0.000. A dense embedder scores them 0.64. That one number is the entire argument of Module 6, and you just ran it. (Your value may differ in the third decimal across versions — anything above ~0.55 is a pass.)

### Step 8 — Editor and the Colab fallback (5 min)

| Option | Get it | Best for |
|---|---|---|
| **VS Code** ✅ recommended | [code.visualstudio.com](https://code.visualstudio.com/) + the Microsoft **Python** extension | Everything. `Ctrl+Shift+P` → *Python: Select Interpreter* → the one with `.venv` in the path. |
| **JupyterLab** | `pip install jupyterlab`, then `jupyter lab` | Module 3's attention heatmaps, capstone write-up |
| **Google Colab** | [colab.research.google.com](https://colab.research.google.com) | GPU fallback for M3 and M8. `torch` and `transformers` are pre-installed. **Never paste your API key into a Colab cell** — use Colab's Secrets panel. |

### ✅ Setup complete checklist

- [ ] `python3 --version` prints 3.10 or higher
- [ ] `~/ai-academy/level4` exists with a `.venv` folder inside
- [ ] My prompt shows `(.venv)` after I run the activate line
- [ ] `python smoke.py` prints a torch version and `torch.Size([1, 4, 4])`
- [ ] A **hard monthly spend limit** is set on the Anthropic console
- [ ] `python smoke_api.py` prints `ready` and a cost under $0.001
- [ ] `python smoke_embed.py` prints `(2, 384)` and a cosine above 0.55
- [ ] My key is in an environment variable, **not** in any file
- [ ] I know my device string (`cpu` / `mps` / `cuda`) and I wrote it down
- [ ] `journal.md` exists with one entry: *"Week 0. Setup done. Device is ___."*

---

## 🚑 Troubleshooting — the five things that actually go wrong

| # | Symptom | Most likely cause | Fix |
|:--:|---|---|---|
| 1 | `ModuleNotFoundError: No module named 'anthropic'` (or `torch`, or `sentence_transformers`) immediately after a "successful" install. Or `pip install` succeeds but the import fails in VS Code only. | You installed into one Python and are running another. The venv wasn't active, or VS Code is using the system interpreter while your terminal uses the venv. This is the single most common setup failure in every level of this course. | Prove which Python is running: `python -c "import sys; print(sys.executable)"`. The path **must** contain `.venv`. If it doesn't: re-run the activate line and reinstall with `python -m pip install ...` (never bare `pip`). In VS Code, `Ctrl+Shift+P` → *Python: Select Interpreter* → pick the `.venv` one, then **restart the terminal inside VS Code**. If the path is right and it still fails, `python -m pip list \| grep anthropic` will tell you whether it is actually there. |
| 2 | `anthropic.AuthenticationError: invalid x-api-key`, or `TypeError: Could not resolve authentication method. Expected the ANTHROPIC_API_KEY environment variable to be set` | Four separate causes that look identical: the key isn't exported in *this* terminal; you exported it with quotes or a trailing space; you're on Windows where `setx` only affects **new** terminals; or the key was revoked/rotated. | Check it exists and looks right: `echo $ANTHROPIC_API_KEY \| cut -c1-10` should print `sk-ant-api`. On Windows, close and reopen the terminal after `setx`. Watch for a trailing space — `export KEY="sk-... "` fails with a message that never mentions whitespace. If all that is fine, the key is dead: make a new one on the console. **Never** hardcode it as a fallback in your script "just to test" — that is how keys end up in git. |
| 3 | `BadRequestError: 400 ... temperature: Extra inputs are not permitted` — or the same for `top_p`, `top_k`, or an assistant prefill message | You copied a snippet written for an older model. On `claude-sonnet-5` the sampling parameters have been **removed** and assistant-turn prefills are rejected. Your training instinct and half the internet are out of date here. | Delete `temperature`, `top_p`, and `top_k` from the call. You get consistency three other ways, all of which are better engineering: a precise prompt, `output_config={"format": SCHEMA}` structured output, and measuring over a 20-case set instead of eyeballing one sample. For format control, use the system prompt or a JSON schema — not a prefilled assistant turn. Module 5 §1 covers this in full. |
| 4 | `sentence-transformers` hangs, or dies with `OSError: We couldn't connect to https://huggingface.co`, `SSLCertVerificationError`, or `LocalEntryNotFoundError` on the second run | A school/office network blocking the Hugging Face CDN, or an interrupted first download leaving a corrupt file in the cache that the library then trusts forever. | **First, delete the cache and retry** — `rm -rf ~/.cache/huggingface` (Windows: `%USERPROFILE%\.cache\huggingface`). A half-download is the most common version of this and nothing will fix it for you. If it's the network: do the one download on a phone hotspot (~90 MB, once, kept forever). On macOS an SSL error is often fixed by running `/Applications/Python 3.x/Install Certificates.command`. **If your network blocks it outright, you are not stuck** — Module 6 ships a `TfidfEmbedder` with the identical interface, so every part of the RAG pipeline still runs; you just lose the semantic-similarity demo, which you can watch in Colab instead. |
| 5 | Training in Module 3 or 8 crashes with `RuntimeError: MPS backend out of memory` / `CUDA out of memory`, or produces `nan` loss after a few hundred steps, or runs 20× slower than the module says | Three different problems that arrive together. **OOM:** batch size or block size too big for your device. **NaN:** learning rate too high, or a missing `clip_grad_norm_`, or fp16 on a device that shouldn't use it. **Slow:** you're on MPS with an operation that silently falls back to CPU, or you're on CPU with `num_workers>0` thrashing. | For OOM, halve `BATCH_SIZE` first, then halve `BLOCK`; both are single constants at the top of every script in this level. For NaN, drop the LR by 10× and confirm `torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)` is in your loop — Module 1 explains why this is mandatory and Module 2 shows the explosion it prevents (`9.38e+06`). For slow, set `device = "cpu"` and compare honestly: **CPU is often faster than MPS for models this small**, because the transfer overhead beats the compute saving. Every script here is sized for CPU on purpose. |

**Three more, less common but maddening:**

| # | Symptom | Fix |
|:--:|---|---|
| 6 | `RateLimitError: 429` in Module 7, or your agent burns $4 in ninety seconds | Two different alarms with the same root: an unbounded loop. Every agent in this level must have `MAX_ITERATIONS` **and** a `BudgetGuard` that raises before the call, not after. If you hit a 429, that's the API being kind to you. Add the caps before you retry, not after. Module 7's guardrails section is not optional reading. |
| 7 | `ValueError: numpy.dtype size changed`, or `ImportError: cannot import name ... from 'tokenizers'`, or `transformers` and `torch` disagree about a version | A dependency clash, usually numpy 2.x vs a package built against 1.x, or `transformers` pinning a `tokenizers` version. Reinstall the clashing set together so pip can resolve them: `python -m pip install --upgrade --force-reinstall numpy torch transformers tokenizers`. If it persists, pin `python -m pip install "numpy<2"`. The nuclear option always works: delete `.venv`, redo Steps 2–3. That is *why* you made a venv. |
| 8 | Your Tiny GPT trains, the loss falls beautifully to near zero, and the generated text is perfect English copied word-for-word from the training data | Not a bug — two things happening at once. (a) With ~7,000 characters and 200k parameters, memorisation is the *expected* outcome and the module says so; check your **validation** loss, which will have turned upward. (b) If train loss is near zero within 200 steps, you probably broke the causal mask and the model can see the answer. Module 3's Practice 2 makes you break it on purpose so you recognise the signature. |

---

## 📅 Weekly Pacing

Twenty-eight weeks at about **2.8 hours a week**, in three sittings. Level 4 modules are the longest in the course, so most get two weeks and Module 3 gets three. Two checkpoint weeks with no new material are built in, and they are the two weeks most likely to be skipped and most damaging to skip.

### The weekly rhythm

```
   ┌──────┬──────────┬────────────────────────────────────────────────────┐
   │ DAY  │  TIME    │  WHAT YOU DO                                       │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ TUE  │  ~50 min │  🪝 Hook + 🧠 Concept                              │
   │      │          │  Away from the keyboard, with paper. In Modules    │
   │      │          │  1–4 the pen comes BEFORE the terminal, always.    │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ THU  │  ~60 min │  🔍 Worked Example + 💻 Hands-On                   │
   │      │          │  Do the worked example's arithmetic by hand, THEN  │
   │      │          │  run the code and check the numbers match. From    │
   │      │          │  Module 5 on: run the offline stubs before you     │
   │      │          │  spend a single cent on the API.                   │
   ├──────┼──────────┼────────────────────────────────────────────────────┤
   │ SAT  │  ~60 min │  ✍️ Practice + ⚠️ Mistakes + 🛠️ Mini-Project      │
   │      │          │  Struggle 20 minutes before the answer key. Then   │
   │      │          │  one journal paragraph: what broke, what you now   │
   │      │          │  believe, and what it cost in dollars.             │
   └──────┴──────────┴────────────────────────────────────────────────────┘
```

> 📓 **Your journal is now also a ledger.** From Module 5 onwards, every entry gets a cost line: *"Thursday: prompt v2 eval, 60 calls, $0.09, score 0.71 → 0.84."* By the capstone you will have a real sense of what things cost, which is a skill almost nobody your age has and quite a few professionals lack.

> 🔁 **And your journal is also Module 6's corpus.** Module 6's RAG system is built over *your own lab notes*. If you have been writing them since week 1, that module becomes personal instead of abstract. If you haven't, you will be typing a fake notebook. Write the notes.

### The twenty-eight weeks

| Week | Focus | Hand in at the end of the week |
|:--:|---|---|
| **0** | 🔧 **Setup** (above) | All three smoke tests pass; spend cap set; device string written down |
| **1** | [M1](module-01-deep-learning-at-depth.md) part 1 — SGD → momentum → Adam → AdamW, schedules, warmup | Three Adam steps computed **by hand** on paper, matched against the module's table |
| **2** | [M1](module-01-deep-learning-at-depth.md) part 2 — regularization, normalization, residuals, curve-reading | 🔬 **Diagnostics Lab**: six runs, one knob each, one shared plot, your own tuning playbook |
| **3** | [M2](module-02-sequence-models.md) part 1 — hidden state, unrolling, BPTT, vanishing gradients | A 4-step RNN unrolled by hand; the gradient product written as a chain |
| **4** | [M2](module-02-sequence-models.md) part 2 — LSTM/GRU gates, teacher forcing, temperature, top-k | 🔤 **Name Generator**: pronounceable names at three temperatures + the decay plot |
| **5** | [M3](module-03-attention-and-transformers.md) part 1 — attention as soft lookup, Q/K/V, scores, √d_k | **The full 3-token attention pass computed by hand.** No code this week. None. |
| **6** | [M3](module-03-attention-and-transformers.md) part 2 — masking, multi-head, positions, the block | Your hand numbers matched against PyTorch to 4 decimal places |
| **7** | [M3](module-03-attention-and-transformers.md) part 3 — training the GPT, sampling, the heatmap | 🧲 **Tiny GPT**: readable text, a loss curve, and an attention heatmap you can interpret |
| **8** | [M4](module-04-how-llms-are-trained.md) part 1 — BPE from scratch, vocabulary size, token arithmetic | A BPE that round-trips 100% of your own text, compared to GPT-2's tokenizer |
| **9** | [M4](module-04-how-llms-are-trained.md) part 2 — pretraining, scaling, SFT, reward models, RLHF, DPO | 🧬 **Life-of-an-LLM**: 10 hand-scored preference pairs + the four-stage explainer |
| **10** | 🧱 **Checkpoint 1 — the machine** (no new module) | **Rebuild a single attention head and a transformer block from a blank file, from memory.** Sit assessment Q1–Q9 and D1–D2. |
| **11** | [M5](module-05-prompt-engineering.md) part 1 — messages API, few-shot, delimiters, structured JSON | A frozen 20-case test set and a scorer, both written before any prompt exists |
| **12** | [M5](module-05-prompt-engineering.md) part 2 — versioning, evals, tokens, cost, the budget guard | 📊 **Prompt Bench**: three versions, one table, score + cost + latency, winner chosen by numbers |
| **13** | [M6](module-06-embeddings-vector-search-rag.md) part 1 — dense vs sparse, cosine, the index, chunking | A cosine similarity computed by hand; one query keyword search provably misses |
| **14** | [M6](module-06-embeddings-vector-search-rag.md) part 2 — the pipeline, citations, τ, recall@k | 🔎 **Ask My Notes**: 10 questions, every answer cited, both unanswerables refused |
| **15** | [M7](module-07-ai-agents.md) part 1 — tool schemas, the loop, planning, state | A tool description rewritten until the model routes to it correctly, with the before/after |
| **16** | [M7](module-07-ai-agents.md) part 2 — failure handling, guardrails, injection | 🤖 **Three-Tool Agent**: 5 tasks, 10-iteration cap, full trace, no sandbox escape |
| **17** | 🧱 **Checkpoint 2 — the system** (no new module) | Draw the RAG pipeline and the agent loop on one page from memory, with every guardrail marked. Sit assessment Q10–Q17 and D3. |
| **18** | [M8](module-08-finetuning-and-evaluating-llms.md) part 1 — the decision table, SFT data, dedup, LoRA | A 30-case eval suite **frozen and committed before** you look at a training example |
| **19** | [M8](module-08-finetuning-and-evaluating-llms.md) part 2 — judges, κ, position bias, regressions | 🎯 **Eval Suite + Fine-Tune**: before/after by category, with one honest regression named |
| **20** | [M9](module-09-responsible-and-safe-ai.md) part 1 — alignment, specification gaming, hallucination vs calibration, abstention | Your own system's specification-gaming example, written up with the mechanism |
| **21** | [M9](module-09-responsible-and-safe-ai.md) part 2 — red-teaming, PII, bias, oversight, system cards | 🛡️ **Red-Team Report**: 3+ exploits found, all mitigated, all re-tested, system card published |
| **22** | 📝 **[Assessment](assessment.md)** | All 20 MCQ + 8 short answer + 4 debug, then read **every** explanation, including the ones you got right |
| **23** | 🚀 [Capstone](capstone.md) M1 — the design doc | Problem, users, why AI, what could go wrong — signed off before any code |
| **24** | 🚀 [Capstone](capstone.md) M2 — the eval harness, written first | 25+ cases and a scorer that runs on demand and prints a number |
| **25** | 🚀 [Capstone](capstone.md) M3–M4 — the two components wired together | RAG + agent (or your chosen pair) answering end to end |
| **26** | 🚀 [Capstone](capstone.md) M5 — cost, latency, and the budget | p50/p95 latency, dollars per task, all measured from logs |
| **27** | 🚀 [Capstone](capstone.md) M6 — guardrails and the red-team pass | Every attack category run; mitigations shipped; re-tested |
| **28** | 🚀 [Capstone](capstone.md) M7 + 🎤 **demo** | System card, the honest section, and a live 5-minute demo to a human |

### Pacing variations

| If you have... | Do this |
|---|---|
| **~1.5 h/week** | Take 40 weeks. Give Modules 3, 7 and 8 an extra week each. Never drop the checkpoints and never drop the mini-projects — the capstone is built from Modules 6, 7 and 8's outputs. |
| **~8 h/week (a summer)** | 12 weeks: roughly a module a week, capstone in the last three. But **keep Module 2 and Module 3 at least four days apart.** The vanishing-gradient result in M2 is the setup; attention in M3 is the punchline; the joke does not work if you rush the pause. |
| **A study partner** | Add a Sunday call and make it adversarial. From Module 5 on: attack each other's prompts. From Module 7 on: attack each other's agents. Give your partner *only* the interface, never the code, and see what they can make it do. This is the single highest-value drill in the level and it is exactly what Module 9 formalises. |
| **A school term structure** | Weeks 1–21 as lessons, 22 as the assessment, 23–28 as a project block ending in a **demo day**. Invite people who are not in the class — the capstone's whole test is whether a stranger can use it. |
| **You already use LLM APIs a lot** | Sit the assessment's Q10–Q17 and debug problem D3 **first**. Score 100% and you may compress Module 5 to its mini-project only. You may **not** skip Module 6 or 7 on that basis; almost everyone who "knows prompting" has never frozen a test set, measured recall@k, or capped an agent loop. |
| **You want to go into research** | Do every [Stretch] exercise and every "level it up." Then take Module 3's model and scale one axis at a time — layers, heads, `d_model`, data — and fit your own tiny scaling curve. That is an actual research skill and it fits in a weekend. |

### ⚠️ Five pacing rules that matter more than the schedule

1. **Pen before terminal in Modules 1–4.** Module 3's worked example exists so that when PyTorch prints `0.751`, you already knew it would. Run the code first and you get the answer while losing the lesson. This is the same rule as Level 3 and it matters more here, not less.
2. **Offline stubs before the API in Modules 5–9.** Every API-using module in this level has a free offline path for the harness. Your bugs are in the parsing, scoring and reporting — none of which needs the model. Get the harness right for $0.00, *then* point it at Claude.
3. **Never skip the checkpoint weeks (10 and 17).** Week 10 is where attention stops being something you copied and becomes something you can write. Week 17 is where the RAG pipeline and the agent loop become one picture in your head rather than two folders on disk. Skip week 10 and Module 8's LoRA will feel like magic again.
4. **Freeze the eval set before you build the thing it measures.** Modules 5, 8 and the capstone all enforce this, and it is the single most transferable habit in the level. A test set you edited after seeing your score is not a test set; it is a mirror.
5. **If you fall behind, drop [Stretch] exercises and "level it up" extensions — never the mini-projects, and never Module 9.** Module 6, 7 and 8's projects are the capstone's raw material. Module 9 is the one that decides whether what you build is safe to hand to somebody.

---

## 🧾 The Level 4 Promise

Twenty-eight weeks from now, somebody will show you a chatbot and say it is intelligent.

You will not argue. You will ask what it was trained on, and whether the benchmark it scored well on was in that data. You will ask what its eval set looks like and whether anyone froze it before tuning. You will ask what happens when it doesn't know — whether there is an abstention path, or whether it just produces the most probable-sounding sentence. You will ask what the retrieved documents are allowed to make it do.

And when it is *your* system, you will hand over a design doc, an eval harness that runs on demand and prints a number, a measured cost per task and a p95 latency, a trace log of every decision it made, a red-team report listing the three ways you broke it and the mitigation you shipped for each, and a system card whose last section is titled *"What this fails at, and who should not rely on it."*

Anyone can wire an API to a text box. The difference between that and what you are about to build is written down, measured, and signed.

---

## ▶️ Start Here

> ### 👉 **[Module 1 — Deep Learning at Depth](module-01-deep-learning-at-depth.md)**
>
> It opens with the same network, the same data, and the same code — trained twice, with one number changed, ending at 91% accuracy and at random guessing. The number is not the architecture.

---

[⬅ Level 3](../level-3-engineer/) · [Back to AI Academy](../../README.md) · [Curriculum map](../../CURRICULUM_MAP.md) · [Glossary](glossary.md) · [Assessment](assessment.md) · [Capstone](capstone.md)
