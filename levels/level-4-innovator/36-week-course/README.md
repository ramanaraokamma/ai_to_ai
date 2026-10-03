```
   █████╗ ██╗    ██████╗  █████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗
  ██╔══██╗██║   ██╔════╝ ██╔══██╗██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝
  ███████║██║   ██║      ███████║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝
  ██╔══██║██║   ██║      ██╔══██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝
  ██║  ██║██║   ╚██████╗ ██║  ██║██████╔╝███████╗██║ ╚═╝ ██║   ██║
  ╚═╝  ╚═╝╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │        L E V E L   4   ·   I N N O V A T O R                      │
  │        ────────────────────────────────────────                  │
  │        T H E   3 6 - W E E K   C O U R S E                        │
  │                                                                  │
  │        One class a week. 60-75 minutes. Everything offline.       │
  │        You build a GPT, the pipeline around it, and then          │
  │        you attack your own work and publish what broke.           │
  │                                                                  │
  │        loss.backward()  ─────►  "here is the system card"         │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
```

# 🚀 Level 4 Innovator — The 36-Week Course

### *One school year. One class a week. From "I can train a network" to "I built a small GPT, the retrieval, agent and evaluation machinery around it, broke it on purpose, and wrote down how."*

**Status:** PLAN (this file is the planner's output; no weekly file exists yet) · **Derived from:** the nine reference modules in [`../`](../README.md) · **Books:** 3 x 36 weeks
**Rhythm:** 36 weeks x one 60-75 minute class + ~60-75 min of workbook homework

[Back to Level 4 modules](../README.md) · [Level 3 course](../../level-3-engineer/36-week-course/README.md) · [Level 4 capstone (reference)](../capstone.md)

---

## 🪝 What This Is

Level 3 ended with a student who could write this, and prove every number in it:

```python
for epoch in range(60):
    opt.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    opt.step()
```

Level 4 asks the next question: **what are the ten decisions hiding inside that loop, what is the
machine that turns it into language, and how do you build a product on top of it that you can defend?**

The nine Level 4 modules next door are a book for one motivated reader with six free hours. They are
**not a course**, and three of them currently assume things this programme does not allow: a credit
card and an API key (Modules 5-9), a 90 MB embedding download (Module 6), a pretrained DistilBERT and
a pretrained GPT-2 tokenizer (Modules 4 and 8), and an Apple/CUDA GPU whose numbers are pasted as if
anyone's laptop would match them (Modules 1 and 3). This folder turns the modules into **36 sittings**
*and* redesigns every network dependency so that the whole level runs **offline, on a CPU, with no
account**. The redesign is described honestly in [Offline by Design](#-offline-by-design-for-level-4).

> **The design constraint, inherited from Level 3 and unchanged:**
> **The teacher opens the week's file 20 minutes before class, and that is all the preparation they
> get. They do not know AI. They have never heard of an LSTM. They must be able to teach a confident,
> correct 70-minute lesson from that one file.**

Level 4 raises that bar in three places, and the teacher files are written to meet it:

1. **The maths is still taught to the adult first, numerically.** The new ideas are small (a running
   average, a square root used as a "typical size", a weighted average, variances adding, a straight
   line on log-log paper, a log-ratio) and each is worked on real numbers *before* it is named.
2. **The teacher is told, every week, which thing is a real model and which thing is a stand-in.**
   From Week 23 on, parts of the course run against a scripted "model" (see
   [the Shared Kit](#-the-shared-kit-l4lib)). That is a deliberate, labelled simplification. A teacher
   who does not know this will tell the student something false.
3. **Every week has a "what you must NOT claim" box.** Toy results demonstrate a mechanism, not a
   rate. A scripted agent that obeys an injected instruction 7 times in 10 says nothing about Claude.

Six things are true of every week in this folder (five are Level 3's, one is new):

1. **Every code block was actually run before it was pasted**, on a CPU, with a seed set, and every
   output shown is the real output. The reference modules' numbers came from MPS/GPU and a live API
   and are **not trusted** - see the ledger in [Risks](#-risks-and-open-questions).
2. **Every new mathematical idea is computed numerically before it is named.**
3. **At most ONE new mathematical idea per week**, and 23 of the 36 weeks add none.
4. **Every week shows at least one real error**, copied from a real failed run and read line by line.
5. **Nothing downloads.** No API, no pretrained weights, no `torchvision`, no `pip`.
6. **(New) Every number quoted from the literature is labelled "quoted, not reproduced here".**
   GPT-2's 124M parameters, Chinchilla's 20 tokens per parameter, "ResNet-152 wins" - all usable as
   context, none ever an exercise.

### What the student walks out with in June

- 📈 **A playbook** - SYMPTOM, CHECK, ACTION - for reading a loss curve, backed by a three-seed sweep
  over the six knobs, with mean and spread, not one lucky run
- ⚙️ **Adam, momentum and a cosine schedule rebuilt by hand** and checked against `torch.optim` to
  the last printed digit
- 🔁 **A measured vanishing gradient** (a number, not a diagram) and the gate that fixes it
- 🔤 **A character-level name generator** with four samplers and a measured novelty rate
- 🧠 **TinyGPT** - a decoder-only transformer written from `nn.Linear` up, trained on CPU on a text
  they typed, with an attention heatmap, a named head, and an ablation table that deleted each
  component in turn
- 🧩 **A byte-level BPE tokenizer** (about 60 lines, their own) that round-trips emoji and Devanagari,
  and a measured "token tax" by language
- 📉 **A measured scaling curve** - four small models, a straight line on log-log paper, and a
  compute estimate built from a FLOP/s rate they timed on their own CPU
- 🎯 **SFT loss-masking, a Bradley-Terry reward model and DPO** on toy data, with reward hacking seen
  happening
- 🧪 **A prompt-engineering bench**: frozen test set, versioned prompts, a scorer, a regression gate,
  a budget guard, all run against a local backend
- 🔎 **A RAG system with citations and a refusal path**, with recall@k measured and every citation
  verified by code
- 🤖 **A tool-using agent** with six guardrails that fire *without any model involved*
- 🏷️ **A fine-tune (full and LoRA) with a frozen eval that caught the regression**
- 🛡️ **A red-team report** of their own agent, with before/after fractions over seeded runs, and a
  **system card** in which every claim carries a number and a sample size
- And the reflex Level 4 exists to install: **when a chatbot is wrong, say whether it was retrieval,
  generation, the prompt, the tokenizer, or a person who over-trusted it - and show the evidence.**

---

## 👤 Who This Is For

| | |
|---|---|
| **The learner** | One student, around 15-16, **who has finished Level 3** - including Weeks 34-36 (shipped artifact). Writes PyTorch's five-line loop from memory, has derived backprop by hand for a 2-layer net and watched PyTorch agree to 8 decimals, trained a digits CNN, built a bag-of-words sentiment engine and seen it fail on word order. **Has never seen an optimizer other than SGD and Adam-as-a-name, an RNN, attention, a tokenizer, or an LLM API.** |
| **The teacher** | You. **You are not expected to know AI.** Read [`teacher-guide/00-orientation.md`](teacher-guide/00-orientation.md) once (to be written: the Level 3 maths course extended by the thirteen Level 4 ideas, a "real vs stand-in" glossary, the 16 errors this level actually produces) and you are ready for 36 weeks. |
| **The setting** | One laptop with about 2.5 GB free (Level 3's install is enough; **Level 4 installs nothing new**). No GPU. No internet during lessons. |
| **Group size** | Written for one learner. Every activity has a "if you have 2-6 students" note. |
| **Honest caveat** | The reference [`README.md`](../README.md) says ages 16-18 and lists a credit card and an API key as prerequisites. **Both statements are superseded by this file** for the taught course (see Risks, item 1). |

### What Level 3 gave them - and the gaps this course closes

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │  THEY ALREADY DO THIS             ─►  THIS YEAR THEY SEE WHAT'S UNDER IT   │
   ├────────────────────────────────────────────────────────────────────────────┤
   │  w -= lr * grad   (w15, w21)      ─►  momentum, Adam, AdamW, schedules     │
   │                                       W2-W4 - the same line, ten variants  │
   │  model.eval() / train() (w22-23)  ─►  dropout, batch norm, layer norm      │
   │                                       - what the switch actually flips  W6 │
   │  slopes multiply along a chain    ─►  40 of them shrink to 3e-12,         │
   │  (w18)                                and a gate fixes it        W10-W11  │
   │  bag-of-words loses order (w33)   ─►  a network that reads in order   W8   │
   │  (A @ B) and shapes (w17)         ─►  (batch, seq, heads, dim) and the    │
   │                                       causal mask                  W14-W17 │
   │  cosine similarity (w32)          ─►  Q.K as a similarity score; later     │
   │                                       a dense embedding search     W14,W25 │
   │  train/val/test, leakage (w2,w6)  ─►  a frozen eval set and a         W23 │
   │                                       contamination check             W30  │
   │  precision/recall/threshold       ─►  abstention: "I don't know" as    W32 │
   │  (w8-w11)                             a measured feature                   │
   │  logging + model card (w35)       ─►  JSONL traces, a system card      W29 │
   │                                                                     W34-36 │
   └────────────────────────────────────────────────────────────────────────────┘
```

**Seven things Level 3 did not teach that the reference modules silently assume.** Each is scheduled
by hand in a specific week; none may appear earlier:

| Gap | Where the module assumes it | Introduced in |
|---|---|---|
| Exponential moving average | Module 1 (momentum, Adam), Module 2 (gates as blends) | W2, by hand on five numbers |
| `sqrt` and epsilon as a "typical size" | Module 1 (RMSProp, Adam) | W3 |
| `lambda` | `LambdaLR`, `key=` functions in Modules 4, 6 | W4 |
| `nn.Embedding`, `nn.Dropout`, `nn.LayerNorm`, `clip_grad_norm_` | Modules 1-3 | W8, W5, W6 |
| `nn.LSTM` / `nn.GRU` (Level 3 lists them as *deliberately not taught*) | Module 2 | W11 |
| KL divergence, Brier score, binomial SD, Cohen's kappa | Modules 4, 8, 9 | W22, W32, W33, W30 |
| `@dataclass`, custom exceptions, classes with `__init__` | Modules 5-9 harness code | W23 |

---

## 📚 The Three Books

Identical in role to Level 3. Using the wrong one is the most common way a course goes wrong.

```
   ┌─────────────────────────┬──────────────────────────┬──────────────────────────┐
   │  📕 TEACHER GUIDE       │  📗 STUDENT GUIDE        │  📘 WORKBOOK             │
   │  teacher-guide/week-NN  │  student-guide/week-NN   │  workbook/week-NN.md     │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  Read alone, 20 min     │  Read at the keyboard,   │  Done alone after class, │
   │  before class           │  in and after class      │  ~60-75 min              │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  · 20-minute prep       │  · The hook (a real,     │  · 6-10 exercises        │
   │  · 🔢 THE MATHS YOU     │    measured number)      │  · Predict-the-output    │
   │    NEED, TAUGHT TO YOU  │  · The concept for a     │    before you run it     │
   │    FIRST                │    15-year-old           │  · Do-it-by-hand, then   │
   │  · 🧭 REAL vs STAND-IN  │  · 🔢 maths, numbers     │    the code that checks  │
   │    box: what is a real  │    before names          │    it                    │
   │    model, what is a     │  · Complete runnable     │  · The week's build      │
   │    scripted one, what   │    code; real output in  │  · A self-check          │
   │    you must NOT claim   │    a separate block      │  · Answer key at the     │
   │  · Minute-by-minute     │  · 🐞 this week's error, │    bottom, sealed behind │
   │    script               │    read and fixed        │    a "struggle 15 min    │
   │  · Exact code + its     │  · 💡 optional "when you │    first" note           │
   │    real CPU output      │    have internet"        │                          │
   │  · Mistakes they'll make│    callout (max one)     │                          │
   │  · Marking guidance     │                          │                          │
   └─────────────────────────┴──────────────────────────┴──────────────────────────┘
```

**The rules** (Level 3's five, plus two):

1. The student never opens the teacher guide.
2. The teacher does not skip the teacher guide - especially on the 13 weeks that carry a new maths idea.
3. The workbook answer key sits at the bottom of the workbook.
4. Nobody pastes code. (Level 4 raises this: a typed-in `bpe.py` is the point.)
5. Every hand calculation gets checked by code, every code result by hand at least once.
6. **(New) Any number a student writes in a report must have been printed by their own run, with a
   seed, in the last 24 hours.** The module's pasted numbers are never a substitute.
7. **(New) Weeks that use the scripted backend open with its label: "This is a stand-in for a model,
   not a model."** The student says it out loud.

### And the folders that are not weekly

| Folder | What is in it | When you open it |
|---|---|---|
| 📝 `assessments/` | Four papers, 75 minutes, 75 marks, no computer: 20 multiple choice, 8 "what does this print / what number", 4 "find the bug", 3 "do the arithmetic", 1 extended | Weeks 9, 18, 27, 36 |
| 🛠️ `projects/` | 30 offline project ideas, one worked capstone taken end to end, the capstone scaffold | Any time from Week 12; Weeks 34-36 for the capstone |
| 🧰 `l4lib/` | The [Shared Kit](#-the-shared-kit-l4lib): one tested Python package used by weeks 1-19 (`spirals`, `names`, `corpus`) and 20-36 (the rest) | Built once, before any week is authored |

---

## 🧰 The Shared Kit (`l4lib/`)

Five of the nine modules (5, 6, 7, 8, 9) and the capstone need "a model to talk to". The reference
modules each invent one from the Claude API. Offline, that would mean five incompatible fakes.
**Decision: one package, written and unit-tested once, that all weeks import.** It is the single
largest piece of new engineering in this plan.

| File | What it is | Used in weeks |
|---|---|---|
| `spirals.py` | `make_spirals(n, noise, seed)` and the `run(*, lr, ..., depth=4)` harness (the Module 1 harness, CPU-pinned, `depth` argument shipped rather than left as homework) | 1-7, 19 |
| `names.py`, `corpus.py` | The 231 typed names; the ~7,000-character TinyGPT corpus; a seeded toy-grammar sentence generator | 8-19 |
| `tinytok.py` | Local token counter: the student's own BPE from W20, falling back to `len(text.split())*1.3`. **Never `tiktoken.get_encoding`** (downloads its ranks) | 20, 23-36 |
| `fakellm.py` | `FakeClient` exposing `messages.create(model, max_tokens, system, messages)` returning `.content[0].text`, `.stop_reason`, `.usage`; a rule-based policy whose competence is a *documented function of prompt features*; seeded error rates; truncation by `max_tokens`; `stop_sequences`; prefix-cache accounting; injectable `RateLimit` / `BadRequest` faults | 23-36 |
| `rag.py` | `TinyDenseEmbedder` (LSA tier and contrastive tier behind one `fit_encode`/`encode` interface), `VectorIndex`, chunkers, the 15-note notebook, and the extractive generator with `cite_wrong_id` / `no_citation` / `ignore_sources` fault switches | 25-26, 28-29, 33-36 |
| `toyagent.py` | `run_agent(question, registry, specs)`; `ScriptedModel`, `GullibleModel` (obeys imperative sentences found in tool results, with a `gullibility` dial), `FlakyBackend`; ToolRegistry; sandbox | 28-29, 33-36 |

**The honesty rule for the kit, stated in every README it touches:**

> *A scripted backend teaches the scaffolding - the loop, the contracts, the fences, the traces, the
> cost shape. It does not teach what a real model does. Rates measured against it are properties of
> the stand-in. We model the mechanism, not the rate.*

Where a lesson needs a *real* learned behaviour (few-shot beating zero-shot, chain of thought
helping, grounding vs guessing, a judge that is biased) it is **re-earned on a model the student
trains from scratch in minutes** - not asserted, and not scripted. See W24.

---

## 🗓️ The Four Terms

Nine weeks each. Each term answers one question the student can answer out loud at the end, while
showing a file that runs and a number they can reproduce.

```
   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 1  ·  WEEKS 1-9  ·  TRAIN IT ON PURPOSE                             ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  Your loss curve is wrong. Which of ten knobs do you       ║
   ║                 turn - and how do you know, before you turn it?           ║
   ║                                                                           ║
   ║  Ends with: 📈 a SYMPTOM-CHECK-ACTION playbook backed by a 3-seed sweep,   ║
   ║  Adam/AdamW/cosine rebuilt by hand and matching torch.optim, residuals    ║
   ║  shown to rescue a 32-block net, and the first recurrent cell (W8)        ║
   ║  unrolled on paper. Assessment 1.                                         ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 2  ·  WEEKS 10-18  ·  MEMORY, THEN ATTENTION                        ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  Why can a network not remember forty steps back - and     ║
   ║                 what did people build instead of making it remember?      ║
   ║                                                                           ║
   ║  Ends with: 🔁 a measured gradient of ~1e-12 and the gate that fixes it,   ║
   ║  🔤 a name generator, 🧠 TinyGPT built from nn.Linear and trained on CPU,   ║
   ║  a three-token attention pass computed with a pen BEFORE any PyTorch.      ║
   ║  Assessment 2.                                                            ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 3  ·  WEEKS 19-27  ·  HOW IT IS MADE, HOW IT IS ASKED               ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  Where does a language model's behaviour come from -       ║
   ║                 and how do you test what you ask it, and what you         ║
   ║                 retrieve for it, like an engineer?                        ║
   ║                                                                           ║
   ║  Ends with: 🔬 a TinyGPT ablation table, 🧩 a tokenizer, 📉 a measured     ║
   ║  scaling line, 🎯 a reward model and DPO on toy preferences, 🧪 a frozen   ║
   ║  prompt-eval bench, 🔎 a RAG system that cites and refuses. Assessment 3. ║
   ╚═══════════════════════════════════════════════════════════════════════════╝

   ╔═══════════════════════════════════════════════════════════════════════════╗
   ║  TERM 4  ·  WEEKS 28-36  ·  AGENTS, EVIDENCE, AND THE SYSTEM CARD         ║
   ║  ───────────────────────────────────────────────────────────────────────  ║
   ║  BIG QUESTION:  You have built the parts. Can you build a product out of  ║
   ║                 them, prove it works, attack it yourself, and tell        ║
   ║                 a stranger honestly where it breaks?                      ║
   ║                                                                           ║
   ║  Ends with: 🤖 an agent whose six guardrails fire with no model present,   ║
   ║  🏷️ a fine-tune whose regression a frozen eval caught, 🛡️ a red-team        ║
   ║  report, and 🚀 a capstone with a design doc, an eval harness, a measured  ║
   ║  cost budget, a demo and a system card.                                   ║
   ╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 🧭 Module Map - which reference module feeds which weeks

| Ref. module | Weeks | Lines in the reference | Audit verdict | Redesign needed |
|---|:--:|:--:|---|---|
| 1 Deep learning at depth | 1-7 | 1,192 | Already offline | Pin CPU, re-run, propagate numbers, bridge EMA/sqrt |
| 2 Sequence models | 8, 10-13 | 1,270 | Already offline | Import check, top-p sampler, dialect bridge, re-time sweeps |
| 3 Attention and transformers | 14-17, 19 | 1,350 | Already offline | Pin CPU, re-time, numpy-first attention step, synthetic tasks |
| 4 How LLMs are trained | 20-22 | 1,543 | ~90% offline | **GPT-2 tokenizer replaced** by local `tokenizers` BPE and a growing corpus |
| 5 Prompt engineering | 23-24 | 1,617 | API-bound | **Rebuilt on `FakeClient`** + from-scratch in-context model |
| 6 Embeddings and RAG | 25-26 | 1,641 | MiniLM + API | **LSA and contrastive encoder**; extractive generator |
| 7 AI agents | 28-29 | 1,725 | API-bound | **Scripted / gullible policies**; own `notes.py` and mini RAG |
| 8 Fine-tuning and evaluating | 30-31 | 1,662 | DistilBERT + API | **Pretrain-then-fine-tune a tiny encoder**; rule-based and planted-bias judges |
| 9 Responsible and safe AI | 32-33 | 1,233 | Agent + API | **Toy agent as target**; local classifier for calibration and bias |
| Capstone | 34-36 | - | API-bound | Two components from {RAG, agent, fine-tune} on the local backend |

Review and assessment weeks (9, 18, 27) belong to no module.

---

## 📋 All 36 Weeks

**Type key:** 🟦 teach · 🟩 lab · 🟨 project · 🟪 review · 🟥 assessment · 🎪 capstone

| Week | Term | Title | Big idea | New maths | New syntax | Type | Homework |
|:--:|:--:|---|---|---|---|:--:|---|
| 1 | 1 | One Loop, Ten Knobs | The `w -= lr * grad` loop has ten knobs nobody named. This year each is turned alone, on data you generate, with a loss curve as the witness - and 0.693 is the number that says "no better than a coin". | *(none)* | `torch.set_num_threads(1)` · keyword-only `*` in `def run(*, lr, ...)` · `nn.GELU()` | 🟦 teach | Run the harness at six learning rates, label each curve A-F, and write down the loss at which a two-class model is guessing (and why `ln 2`) |
| 2 | 1 | Momentum: A Running Average of Where You Were Going | A step that remembers the last few steps rolls through bumps that stop plain SGD. The memory is a running average. | **exponential moving average** - by hand on five numbers, with the "half-life" of 0.9 | `SGD(momentum=0.9)` · `zero_grad(set_to_none=True)` · `tensor.norm()` | 🟦 teach | Do three steps of SGD and of momentum on `f(w)=w^2` by hand, then check against `torch.optim`; find a `lr` where momentum helps and one where it hurts |
| 3 | 1 | Adam: Every Knob Gets Its Own Step Size | Divide each knob's step by a running "typical size" of its own gradient and the first step is `lr` (to within epsilon) - whatever the scale. AdamW fixes a quiet bug in weight decay. | **root-mean-square** - the "typical size" of numbers, with a tiny epsilon to stop dividing by zero | `torch.optim.Adam` · `torch.optim.AdamW` · `weight_decay=` · `torch.sqrt` | 🟦 teach | Fill the three-optimizer table (SGD, momentum, Adam) for four steps by hand and match `torch.optim`; then show Adam's first step size is `lr` for gradients of 1 and 1000 |
| 4 | 1 | Schedules and Batch Size | The right step size changes during a run (warm up, then decay), and the batch you average over changes both the noise and how many steps you get. | *(none)* | `lambda` · `LambdaLR` · `scheduler.step()` · `scheduler.get_last_lr()` | 🟦 teach | Plot cosine and warmup-plus-cosine with numpy, verify against `LambdaLR`, then run the batch-size grid and state why "bigger batch, better" is confounded by fewer steps |
| 5 | 1 | Four Ways to Stop Memorising | Early stopping, dropout, weight decay and augmentation all land near the same best validation loss - and early stopping is free. | *(none)* | `nn.Dropout(p)` · `copy.deepcopy(model.state_dict())` · `rng.normal(0, s, size=...)` · `torch.randperm(n, generator=g)` | 🟩 lab | Overfit 120 points on purpose, then run the four cures and fill a table of best-val-epoch, best-val-loss and final-val-loss; say which column tells the truth |
| 6 | 1 | Norms, Residuals, and the Gradient Highway | Batch norm leans on other examples and breaks at batch size 1; layer norm does not. `x + f(x)` gives the gradient a road of slope exactly 1 to walk down. | **slope of a sum** - nudge `x` in `x + f(x)` and see `1 + f'(x)` emerge | `nn.LayerNorm` · `nn.BatchNorm1d` · `nn.Identity` · `clip_grad_norm_` | 🟦 teach | Break batch norm on purpose at batch size 2, then plot the first-block gradient norm at depth 2, 8, 16, 32 with and without residuals |
| 7 | 1 | Project: The Symptom-Check-Action Playbook | A loss curve is a symptom; a playbook maps each symptom to one cheap check and one action. One knob per run, three seeds, mean and spread. | *(none)* | `itertools.product` | 🟨 project | Sweep six knobs x about four values x 3 seeds (with the stated `epochs` cut-down), and hand in the one-page playbook plus the sweep table |
| 8 | 1 | Order Matters: A Cell That Remembers | Bag-of-words cannot tell "dog bit postman" from "postman bit dog". A recurrent cell reads in order and carries a summary: one small net, reused at every step. | *(none)* | `nn.Embedding` · `nn.RNN(batch_first=True)` · `out, h_n = rnn(x)` | 🟦 teach | Unroll a 4-step RNN by hand with the worked weights, check it against `nn.RNN`, and show two sentences with identical bags get different final states |
| 9 | 1 | Review and Assessment 1 | Weeks 1-8 on paper: read a curve, do an optimizer step, name the norm that fails, unroll a cell. | *(none)* | *(none - review)* | 🟥 assessment | Mark the paper against the key; fill the per-week remediation table |
| 10 | 2 | Forty Multiplications: Why Memory Fades | Backprop through time multiplies the same slope over and over. A number below 1 shrinks to nothing, above 1 blows up - and clipping only cures the second. | **compounding** - a number multiplied by itself T times (`0.9526^40 = 0.143`), by hand | `h.retain_grad()` · `torch.stack` · `torch.randn(T, ...)` | 🟩 lab | Measure the gradient at position 1 against sequence length T = 10, 20, 40, 80, and force an explosion with and without `clip_grad_norm_` |
| 11 | 2 | Gates: Memory That Adds Instead of Multiplies | An LSTM updates its memory by adding, so the slope back through it is the forget gate. A gate near 1 is the residual highway of Week 6 in a loop. | *(none)* | `nn.LSTMCell` · `nn.LSTM` / `nn.GRU` · in-place `fill_()` on a bias slice | 🟦 teach | Code an LSTM cell from scratch, check against `nn.LSTMCell`, then compare RNN, GRU and LSTM over 3 seeds and the forget-bias 0 vs 2 probe |
| 12 | 2 | Teach a Network to Invent Names | Training feeds the true previous letter (teacher forcing) and runs in parallel; generating feeds back its own guess and runs one letter at a time. | *(none)* | `F.cross_entropy(..., ignore_index=)` · `torch.cat` · `torch.full` | 🟩 lab | Train the character model on 231 typed names, report train vs val loss, and measure what fraction of generated names already exist in the training list |
| 13 | 2 | Choosing the Next Letter: Sampling and Exposure Bias | Greedy repeats itself, temperature reshapes the odds, top-k and top-p cut the tail. A model trained on truth can still drift once it reads its own output. | *(none)* | `F.softmax(dim=-1)` · `torch.multinomial` · `torch.topk` · top-p via `sort` + `cumsum` | 🟦 teach | Predict then measure what T = 0.3, 1, 2 does to a 5-letter distribution; run the copy-task delay sweep at the stated CPU-sized defaults |
| 14 | 2 | Attention by Hand | A soft dictionary lookup: compare the question to every key, turn the scores into weights, blend the values. One three-token pass, done entirely with a pen and then with numpy. | **weighted average** - weights that sum to 1, applied to values | `k.transpose(-2, -1)` · `nn.Linear(d, d, bias=False)` · `unsqueeze` | 🟦 teach | Hand-compute the module's 3-token attention pass to three decimals, then reproduce it in numpy and in torch and show all three agree |
| 15 | 2 | Scale, Mask, and Many Heads | Big dot products saturate softmax, so divide by the square root of the width. Hiding the future turns one sentence into T training signals. | **variances add** - the spread of a sum of `d` independent terms grows like `d`, so divide by `sqrt(d)`; measured, not proved | `masked_fill(mask, float("-inf"))` · `torch.tril` · `.view(B,T,H,dh).transpose(1,2)` | 🟦 teach | Show the softmax of raw vs scaled scores at `d_k` = 4, 16, 64; then prove the mask is set before the softmax (and show what 0 instead of `-inf` does) |
| 16 | 2 | Where Am I? Positions and the Transformer Block | Attention cannot tell order, so add a position vector. Attention plus a 4x MLP, wrapped in residuals and layer norm, is one block - and a GPT is a stack of them. | *(none)* | `nn.ModuleList` · `register_buffer` · `torch.arange` | 🟦 teach | Permute a sequence and show attention without positions returns the same (shuffled) answer; add positions and show it changes; count the parameters of one block by hand |
| 17 | 2 | Build TinyGPT | A decoder-only transformer, from `nn.Linear` up, trained on 7,000 typed characters. Initial loss should be within 0.05 of `ln(vocab)` - a check, not a hope. | *(none)* | `torch.randint` batching · `@torch.no_grad()` · nested `nn.Module` | 🟩 lab | Train the CPU-sized configuration, report the measured step time, the three checkpoint samples, and train vs val loss - and say what the gap means |
| 18 | 2 | Review and Assessment 2 | Weeks 9-17: gradient compounding, gates, sampling, the attention arithmetic, the block. | *(none)* | *(none - review)* | 🟥 assessment | Mark the paper; redo the 3-token pass on a new set of numbers |
| 19 | 3 | Open the GPT: Heads, Ablations, Synthetic Tasks | Delete each component in turn (mask, positions, residual, layer norm) and watch what breaks. Synthetic copy, reverse and lookup tasks make heads easy to name. | *(none)* | *(none - reuses)* | 🟩 lab | Fill the ablation table at the stated reduced step count; name one head on the copy task from its heatmap and say what evidence would prove the name wrong |
| 20 | 3 | Tokenizers: BPE From Scratch | Words are too many, letters too few. Repeatedly merge the most common adjacent pair and you get subwords that round-trip any text, including emoji and Devanagari. | *(none)* | `collections.Counter` · `str.encode("utf-8")` · `re.compile(...).findall` · `tokenizers` `BpeTrainer` | 🟩 lab | Write `bpe.py`, pass the round-trip tests (emoji, Devanagari, empty string), then diff it against a locally trained `tokenizers` BPE and chart bytes-per-token as the corpus grows |
| 21 | 3 | Pretraining and the Scaling Arithmetic | Pretraining is the same next-token loss as Week 17, at a scale where data pipeline and compute budget matter. Loss falls as a power law - a straight line on log-log paper. | **log-log straight line** - a power law is a line once you take logs of both axes | `np.polyfit` · `np.log10` · `hashlib.md5` (for dedup) | 🟦 teach | Train four model widths, fit loss vs parameters, extrapolate one point and check it; time your CPU's FLOP/s and estimate `C = 6ND` for your own model |
| 22 | 3 | After Pretraining: SFT, Reward Model, DPO | Fine-tune on prompt-and-answer pairs but mask the prompt; teach a reward model from preferences; or skip the reward model and apply DPO directly. All three fit on a laptop as toys. | **KL divergence** - average log-ratio of two distributions; "how far did the leash let you move" | `F.logsigmoid` · `F.log_softmax` · `torch.gather` · `.detach()` | 🟦 teach | Show masked vs unmasked SFT loss on the same logits; train the 5-feature reward model and find one hacked feature; run DPO at two `beta` values and explain the difference |
| 23 | 3 | Prompting as Engineering: The Harness | A prompt loop is a test suite: a frozen set, a versioned prompt, a call, a parse, a score, a regression report. A constant-answer baseline sets the floor. | *(none)* | `@dataclass` · a class with `__init__` · `try`/`except` with a custom exception · `re.search(..., re.S)` | 🟦 teach | Freeze an 8-case set before writing a prompt; compute the brute-force constant baseline over 30 constants; add a `BudgetGuard` that trips one call late and say why |
| 24 | 3 | Examples, Scratchpads, and Schemas - Learned in Context | A small transformer that you train yourself can learn to follow examples in its prompt, or to show its working. A schema guarantees shape, never sense. | *(none)* | `random.Random(seed)` · `hashlib.sha256` · `torch.where` | 🟩 lab | Plot copy accuracy at 0, 1, 3, 8 in-context examples; train direct-answer vs scratchpad addition; add a logit mask that forces 100% valid JSON and show the semantic errors that survive |
| 25 | 3 | Embeddings: Geometry for Meaning | TF-IDF has no geometry: "optimiser" and "optimizer" share nothing. Character n-grams plus SVD, or a contrastive model you train, put similar things near each other. | *(none - SVD is Level 3 Week 29's PCA idea applied to Level 3 Week 32's TF-IDF)* | `TruncatedSVD` · `TfidfVectorizer(analyzer="char_wb")` · `np.save` / `np.load` · `nn.EmbeddingBag` | 🟦 teach | Hand-compute cosine for three 3-vectors (1.000 and 0.283), build the normalise-once matrix-multiply index, and measure a query that TF-IDF scores 0.000 and your embedder does not |
| 26 | 3 | RAG: Retrieve, Cite, Refuse | Chunk, embed, retrieve, number the sources, demand the id back, verify it in code, refuse below a threshold. Diagnose a wrong answer as retrieval or generation by reading the chunks. | *(none)* | `np.argsort(-s)[:k]` · `re.findall` for citations · set operations · `Path.glob` | 🟩 lab | Build the 15-note index with structural chunking; report recall@1/3/5 on 10 questions you wrote first; sweep the threshold; poison one note and show the injection |
| 27 | 3 | Review and Assessment 3 | Weeks 19-26: ablation reasoning, BPE, scaling, SFT and DPO, the eval harness, cosine, recall@k. | *(none)* | *(none - review)* | 🟥 assessment | Mark the paper; rerun the recall table with a changed chunk size |
| 28 | 4 | Tools and the Loop | A tool is a function plus a contract; the model only asks, your code acts. Perceive, decide, act, observe, stop - with six fences that work with the model unplugged. | *(none)* | `ast.parse` safe calculator · `operator` whitelist · `Path.resolve()` + `is_relative_to` · `ThreadPoolExecutor` | 🟦 teach | Fire all six guardrails from plain Python with no model, then run the scripted agent on the worked five-turn plan and paste the real trace |
| 29 | 4 | Agents Under Attack and Under Budget | Tool results are data, not orders, and only capability limits truly stop an injection. Every turn re-sends history, so cost grows faster than steps. | **triangular sum** - `1+2+...+k = k(k+1)/2`, so re-sent history grows like `k^2` | JSONL trace with `json.dumps` · `future.result(timeout=)` · `time.sleep` (simulated latency, default 0) | 🟩 lab | Run the gullible model through the three injection layers and show which one holds; fit cost against steps and predict step 30 |
| 30 | 4 | Evaluating LLM Systems: The Frozen Suite and the Judge | Freeze the eval before you build. Beat the cheap baseline first. Then test the judge itself: a judge with a planted bias is one you can catch. | **Cohen's kappa** - agreement beyond chance, by hand on 20 ratings | `cohen_kappa_score` · set intersection and union for Jaccard · `rng.choice` | 🟦 teach | Build the 30-case 5-class set, score a rules baseline, run a dedup and contamination check, and recover the planted position bias in the scripted pairwise judge |
| 31 | 4 | Fine-Tuning, LoRA, and the Regression | Pretrain a tiny encoder once, fine-tune it on 64 tickets, and freeze most of it with a low-rank patch. The average rises while one category collapses. | **low-rank** - a big grid as the product of two thin ones; `r x in + out x r` parameters | `nn.Parameter` · `requires_grad_(False)` · `nn.init.zeros_` / `normal_` · `copy.deepcopy(model)` | 🟩 lab | Compute the LoRA parameter percentage for your model by hand, then show step 0 equals the base model, and report the per-category table that exposes the regression |
| 32 | 4 | The Proxy Is Not the Goal: Calibration and Abstention | The score you optimise is not the thing you wanted. A model can be wrong and sure. Saying "I don't know" is a measured feature. | **calibration gap** - Brier score (mean squared gap between probability and 0/1) and expected calibration error (average gap between "said 80%" and "was right 80%"), by hand on 10 results | `np.digitize` · `brier_score_loss` · `np.bincount` | 🟦 teach | Build the reliability table (5 buckets, about 8 of the 40 results each) and ECE, add an abstain threshold, draw the coverage-vs-accuracy curve, and find a category that fell while the average rose |
| 33 | 4 | Attack Your Own System | Red-teaming is a discipline: attack, evidence, mechanism, fix, re-test (including the happy path), residual risk. Redact PII twice, log less, delete on schedule, and ask whether 20 runs can see a gap. | **binomial standard deviation** - `sqrt(n p (1-p))`, "how wobbly is a count" | `re.sub` with ordered patterns · `Path.stat().st_mtime` | 🟩 lab | Run attacks A1-A5 against the toy agent over 50 seeded runs each, patch one, re-test, and report before/after fractions with a noise bound |
| 34 | 4 | Capstone 1: Design and the Frozen Eval | Decide what you are building, write down what it will NOT do, and freeze 25 eval cases before any component exists. | *(none)* | *(none)* | 🟨 project | Design doc (seven headings), 25 frozen cases with a committed hash, and a stated cost-and-latency budget |
| 35 | 4 | Capstone 2: Build, Measure, Attack | Two components from {RAG, agent, fine-tuned model}, the harness running on demand, one red-team pass, one documented regression caught by the suite. | *(none)* | *(none)* | 🟨 project | Eval report with per-category table, measured tokens and latency, and a red-team log with one fixed and one accepted risk |
| 36 | 4 | Capstone 3: Demo, System Card, Final Assessment | Five minutes to show it, one page to say honestly where it fails and who should not rely on it. Then the paper. | *(none)* | *(none)* | 🎪 capstone | System card with a number and a sample size behind every claim; final paper (Assessment 4) |

**Count check:** 36 rows. Labs fall on weeks 5, 10, 12, 17, 19, 20, 24, 26, 29, 31, 33; projects on 7, 34, 35; reviews/assessments on 9, 18, 27; the capstone on 36.

### Year at a glance

```
   Wk  1  2  3  4  5  6  7  8  9 |10 11 12 13 14 15 16 17 18 |19 20 21 22 23 24 25 26 27 |28 29 30 31 32 33 34 35 36
   M1  ■  ■  ■  ■  ■  ■  ■        |                            |                            |
   M2                    ■        |■  ■  ■  ■                  |                            |
   M3                             |            ■  ■  ■  ■      |■                           |
   M4                             |                            |   ■  ■  ■                  |
   M5                             |                            |            ■  ■            |
   M6                             |                            |                  ■  ■      |
   M7                             |                            |                            |■  ■
   M8                             |                            |                            |      ■  ■
   M9                             |                            |                            |            ■  ■
   Cap                            |                            |                            |                  ■  ■  ■
   ✔                           A1 |                         A2 |                         A3 |                        A4
```

Three weeks are structurally the heaviest and are flagged in [Risks](#-risks-and-open-questions):
**W22** (three ideas from Module 4 in one sitting), **W24** (three from-scratch toy models) and **W33**
(red-team, PII and bias probe).

---

## 🪜 The Maths Ladder

**Every mathematical idea in Level 4, in the week it first appears. At most one per week; 23 of 36
weeks add none.** The ladder is enforced the same way as Level 3: search the table before using a
word.

### Already theirs, from Levels 1-3 - assumed, never re-taught

Mean/median/mode; standard deviation and z-score (L3 W4); variance (L3 W29); a slope by rise over run
and a slope *at a point* by nudging (L3 W12); the gradient as one slope per knob (L3 W15); slopes
multiplying along a chain (L3 W18); `exp`, the sigmoid and softmax (L3 W13); `ln` as a surprise meter
and log loss (L3 W14); shapes and `A @ B` (L3 W16-17); `tanh` and ReLU (L3 W16); cosine similarity
(L3 W32); PCA as "the best few directions" (L3 W29); precision, recall, thresholds, cost of mistakes
(L3 W8-11); mean and spread across repeats (L3 W11).

### New in Level 4, in order

| Week | Idea | Plain meaning | How it is met first |
|:--:|---|---|---|
| 2 | **Exponential moving average** | New average = 0.9 x old average + 0.1 x new value | Five numbers on paper; watch an old value fade by a fixed share each step |
| 3 | **Root-mean-square** (and epsilon) | The "typical size" of a list, ignoring sign; add a tiny number so you never divide by zero | Square, average, root, on `[3, -4]`; then `[300, -400]` |
| 6 | **Slope of a sum** | Nudge `x`; `x + f(x)` moves by 1 plus whatever `f` does | Numerically with a tiny step, before `1 + f'(x)` is written |
| 10 | **Compounding** | Multiply by the same number T times | `0.9526` forty times is `0.143`; `0.95` forty times; `1.05` forty times |
| 14 | **Weighted average** | A mean where some values count more; the weights add to 1 | Three values, weights `[0.7, 0.2, 0.1]` |
| 15 | **Variances add** | A sum of `d` independent spreads grows like `d`, its size like `sqrt(d)` | Simulated with a seeded generator at `d` = 4, 16, 64 |
| 21 | **Log-log straight line** | A power law `y = a x^-b` becomes a straight line when both axes are logged | Plot four points on both axes; fit the line with `np.polyfit` |
| 22 | **KL divergence** | Average log-ratio of two distributions: how far one has moved from the other | Two 4-outcome tables, arithmetic only |
| 29 | **Triangular sum** | `1+2+...+k = k(k+1)/2` | Add 1 to 10 by pairing ends; so re-sent history grows like `k^2` |
| 30 | **Cohen's kappa** | Agreement with the chance agreement removed | Twenty paired ratings on a grid |
| 31 | **Low-rank** | A big grid as a thin times a thin, needing far fewer numbers | A 4x4 grid of rank 1, then `r x in + out x r` |
| 32 | **Calibration gap (Brier, ECE)** | How far a stated probability is from how often it came true | Ten results on paper: square each gap for Brier; bucket by stated confidence for ECE |
| 33 | **Binomial standard deviation** | How much a count wobbles when every try is a weighted coin | `sqrt(20 x 0.3 x 0.7)`, then 200 runs |

### Deliberately NOT in this level - so you can say "not yet" with confidence

Proofs of any kind; limits; the chain rule written as symbols; the backward pass of attention by hand
(the forward pass is by hand; backward is checked against autograd only); the Jacobian (the per-step
factor is the *measured* slope of `tanh` times a weight); information theory beyond cross-entropy and
one KL; statistics beyond mean, SD, kappa, calibration gap and one binomial SD; the PPO objective (described, never
derived or run).

---

## 🪜 The Syntax Ladder

Every construct, in the week it first appears. **Nothing is used before its week. Maximum four per
week.** Everything in the [Level 3 ladder](../../level-3-engineer/36-week-course/README.md#-the-syntax-ladder)
(and therefore Level 2's) is assumed, with these Level 3 "not yet" items **now unlocked** only where
they appear below: `lambda` (W4), `nn.LSTM` / `nn.GRU` (W11), classes with `__init__` (W23).

| Week | New construct | What it does in one line |
|:--:|---|---|
| 1 | `torch.set_num_threads(1)` | Makes CPU results reproducible run to run |
| 1 | keyword-only `*` in `def run(*, lr, ...)` | Forces named arguments so a sweep can never pass them in the wrong order |
| 1 | `nn.GELU()` | A smooth cousin of ReLU, used from Week 16 on |
| 2 | `torch.optim.SGD(..., momentum=0.9)` | SGD with a running average of past gradients |
| 2 | `optimizer.zero_grad(set_to_none=True)` | Clears gradients by removing them (cheaper, and a `None` is easier to spot) |
| 2 | `tensor.norm()` | The length of a tensor - used for gradient size |
| 3 | `torch.optim.Adam` | Momentum plus a per-knob step size |
| 3 | `torch.optim.AdamW` | Adam with weight decay applied the right way |
| 3 | `weight_decay=` | Shrinks every weight a little each step |
| 3 | `torch.sqrt` | Square root of every element |
| 4 | `lambda step: ...` | A function written in one line |
| 4 | `torch.optim.lr_scheduler.LambdaLR` | Multiplies the base `lr` by your function of the step |
| 4 | `scheduler.step()` | Advances the schedule once per optimizer step |
| 4 | `scheduler.get_last_lr()` | Reads the current `lr` back |
| 5 | `nn.Dropout(p)` | Randomly zeroes a share of activations in train mode only |
| 5 | `copy.deepcopy(model.state_dict())` | A snapshot that later training cannot overwrite |
| 5 | `rng.normal(0, s, size=...)` | Gaussian jitter, from the seeded generator of Week 1 (L3) |
| 5 | `torch.randperm(n, generator=g)` | A seeded shuffle of `0..n-1` |
| 6 | `nn.LayerNorm(d)` | Normalises each example across its own features |
| 6 | `nn.BatchNorm1d(d)` | Normalises each feature across the batch (has running stats) |
| 6 | `nn.Identity()` | A layer that does nothing - the skip path |
| 6 | `torch.nn.utils.clip_grad_norm_` | Rescales gradients if their total length is too large; returns the pre-clip size |
| 7 | `itertools.product` | Every combination of several lists - the sweep grid |
| 8 | `nn.Embedding(V, d)` | A lookup table from token id to vector |
| 8 | `nn.RNN(..., batch_first=True)` | A recurrent layer on a `(batch, time, features)` tensor |
| 8 | `out, h_n = rnn(x)` | Unpacking every hidden state and the last one |
| 9 | *(review)* | - |
| 10 | `h.retain_grad()` | Keeps the gradient of a non-leaf tensor so you can read it |
| 10 | `torch.stack` | Joins a list of tensors into one along a new axis |
| 10 | `torch.randn(T, ...)` | Seeded random inputs of chosen shape |
| 11 | `nn.LSTMCell` | One LSTM step, so you can write the gates yourself and compare |
| 11 | `nn.LSTM` / `nn.GRU` | The whole-sequence layers |
| 11 | `tensor.fill_(x)` | In-place fill, used on a bias slice under `no_grad` |
| 12 | `F.cross_entropy(..., ignore_index=)` | Loss that skips padding positions |
| 12 | `torch.cat` | Joins tensors along an existing axis (shift-right inputs) |
| 12 | `torch.full` | A tensor filled with one value (the start token) |
| 12 | `import torch.nn.functional as F` | The functional namespace, which Level 3 deliberately avoided; needed for `F.cross_entropy` here and `F.softmax` in W13 |
| 13 | `F.softmax(x, dim=-1)` | Probabilities over the last axis |
| 13 | `torch.multinomial` | Draws an index according to given probabilities |
| 13 | `torch.topk` | The k largest values and their positions |
| 13 | `torch.sort` + `torch.cumsum` | The pair that implements top-p (counted as one) |
| 14 | `k.transpose(-2, -1)` | Swaps the last two axes, whatever comes before them |
| 14 | `nn.Linear(d, d, bias=False)` | A pure matrix multiply, used for Q, K and V |
| 14 | `tensor.unsqueeze(dim)` | Adds a length-1 axis so shapes line up |
| 15 | `masked_fill(mask, float("-inf"))` | Hides positions from softmax |
| 15 | `torch.tril` | The lower-triangle matrix that encodes "no looking ahead" |
| 15 | `.view(B,T,H,dh).transpose(1,2)` | Splits channels into heads |
| 16 | `nn.ModuleList` | A list of sub-modules PyTorch can see |
| 16 | `register_buffer` | A tensor that moves with the model but is not trained |
| 16 | `torch.arange` | Integers `0..n-1` as a tensor (positions) |
| 17 | `torch.randint` batching | Random window starts for training batches |
| 17 | `@torch.no_grad()` | Decorator form of Level 3 Week 21's `with torch.no_grad()` (used, not written; writing decorators stays out of scope) |
| 17 | nested `nn.Module` | Modules containing modules (Block in GPT) |
| 18 | *(review)* | - |
| 19 | *(none - reuses)* | - |
| 20 | `collections.Counter` | Counts how often each item appears |
| 20 | `str.encode("utf-8")` | Turns text into bytes, so any script round-trips |
| 20 | `re.compile(...).findall` | A reusable pattern applied to text |
| 20 | `tokenizers` `BpeTrainer` | The production BPE trainer, used **locally** on local text |
| 21 | `np.polyfit(x, y, 1)` | Best straight line through points |
| 21 | `np.log10` | Base-10 log (log-log axes) |
| 21 | `hashlib.md5` | A fingerprint for exact-duplicate detection |
| 22 | `F.logsigmoid` | `log(sigmoid(x))` without numerical trouble |
| 22 | `F.log_softmax` | Log-probabilities over the last axis |
| 22 | `torch.gather` | Picks one entry per row by index (the chosen token's log-prob) |
| 22 | `tensor.detach()` | Cuts a tensor off from the graph (the frozen reference model) |
| 23 | `@dataclass` | A class that is just named fields |
| 23 | class with `__init__` | Your own object with state and methods |
| 23 | `try` / `except MyError` | Catches a specific failure; `raise MyError(...)` to signal one |
| 23 | `re.search(..., re.S)` | Matches across line breaks |
| 24 | `random.Random(seed)` | A seeded generator local to one object |
| 24 | `hashlib.sha256` | Fingerprint of a prompt prefix (cache key) |
| 24 | `torch.where(cond, a, b)` | Element-wise choose (the logit mask) |
| 25 | `TruncatedSVD(n)` | Keeps the best `n` directions of a sparse matrix |
| 25 | `TfidfVectorizer(analyzer="char_wb")` | Character n-grams, so near-spellings overlap |
| 25 | `np.save` / `np.load` | Persists an index to disk |
| 25 | `nn.EmbeddingBag` | Mean of embeddings in one call |
| 26 | `np.argsort(-s)[:k]` | Positions of the k largest scores |
| 26 | `re.findall(r"\[(\d+)\]", t)` | Pulls citation ids out of text |
| 26 | set operations | Checks cited ids are a subset of served ids |
| 26 | `Path.glob` | Lists files matching a pattern |
| 27 | *(review)* | - |
| 28 | `ast.parse` + `operator` whitelist | A calculator that cannot run arbitrary code |
| 28 | `Path.resolve()` + `is_relative_to` | The sandbox test: did this path escape? |
| 28 | `ThreadPoolExecutor` | Runs a tool in another thread so a timeout can be enforced |
| 28 | `isinstance` checks in `validate_args` | Type-checks arguments before a tool runs |
| 29 | `json.dumps` one line per event | JSONL tracing |
| 29 | `future.result(timeout=)` | Stops waiting on a hung tool |
| 29 | `time.sleep` | A simulated round-trip delay, default 0, labelled simulated |
| 30 | `cohen_kappa_score` | Kappa, after you have done it by hand |
| 30 | set intersection / union | Jaccard overlap for near-duplicate detection |
| 30 | `rng.choice` | Seeded sampling for the planted biased judge |
| 31 | `nn.Parameter` | A tensor PyTorch will train |
| 31 | `requires_grad_(False)` | Freezes a module in place |
| 31 | `nn.init.zeros_` / `normal_` | Sets LoRA's `B` to zero and `A` to small random |
| 31 | `copy.deepcopy(model)` | A pristine copy of the base to compare against |
| 32 | `np.digitize` | Puts each probability into a bucket |
| 32 | `brier_score_loss` | Mean squared gap between probability and outcome |
| 32 | `np.bincount` | Counts per bucket |
| 33 | `re.sub` with ordered patterns | Redaction: longest pattern first |
| 33 | `Path.stat().st_mtime` | File age, for the retention sweep |
| 34-36 | *(none)* | Capstone uses only earlier constructs |

Not in Level 4 at all: decorators you write yourself, metaclasses, `asyncio`, type hints as a
required practice, `pytest`, `transformers` (optionally `GPT2Config` with random weights to count
parameters, flagged optional), `torchvision`.

---

## 🔌 Offline by Design for Level 4

**Read this before Week 1.** Level 3's rule carries over verbatim:

> **Every dataset in all 36 weeks is typed by the student, generated by numpy or Python in front of
> them, or ships inside scikit-learn. Nothing downloads. There is no API key, no account and no
> credit card. Ever.**

Level 4 cannot stop there, because its subject matter is defined by things that *are* downloaded:
pretrained tokenizers, pretrained embedders, hosted LLMs. So this section makes the **substitutions
explicit, and says what is lost**.

### What stands in for what

| The reference module uses | This course uses instead | What is honestly lost |
|---|---|---|
| `pip install torch numpy matplotlib` (M1, M2, M3, M4) | A 3-line smoke test; "nothing to install" | Nothing |
| CUDA / MPS auto-detect; numbers pasted from MPS (M1, M3) | `DEVICE = "cpu"`, `torch.set_num_threads(1)`, numbers re-run on CPU | Absolute speed; results now match on the student's machine |
| GPT-2 tokenizer via `from_pretrained` (M4) | The student's BPE; a locally trained `tokenizers` BPE; **bytes-per-token measured climbing as the corpus grows** | The number 4.5 is quoted as "measured elsewhere", not reproduced |
| Claude API: `messages.create`, `count_tokens`, `thinking`, `effort`, structured output (M5) | `FakeClient` with the same surface; local token counter; a logit-mask JSON decoder | Real prompt sensitivity. **The module's 59.4 to 90.6% few-shot story is dropped** and re-earned on a model trained from scratch (W24) |
| "Temperature removed, HTTP 400" and other vendor rules (M5) | A one-line vendor note; `FakeClient` can simulate it, labelled as simulating one vendor | Vendor-specific facts |
| `all-MiniLM-L6-v2` (M6, M8, M9) | LSA (char n-grams + SVD) and a contrastive bi-encoder trained in under two minutes | Semantic quality - **the "0.62" figure does not survive and is not replaced by a bigger number** |
| Claude as generator and as query-rewriter (M6) | Extractive generator with faulty-mode switches; rule-based rewriter with pseudo-relevance feedback | Fluent answers |
| The agent's model (M7, M9) | `ScriptedModel`, `GullibleModel`, `FlakyBackend` | Everything a real model does. Rates are the stand-in's, not the world's |
| DistilBERT fine-tuning + LoRA (M8) | A 2-4 layer encoder pretrained for 1-3 min on a generated corpus, then fine-tuned and LoRA'd | The 0.900 / 0.867 / 1.11% results (recomputed for the tiny model; the regression story rewritten around what is actually observed) |
| Claude as judge (M8) | Rule-based rubric judge + a judge with a planted, known bias | Real judge behaviour; gained: a bias you can recover |
| Dollar costs of a live API (M5-M9) | Tokens sent/received, locally counted, times an explicit **`PRICE_TABLE` labelled illustrative** | Real bills |
| Real-time latency of a network call (M7) | `time.perf_counter` on the local backend; optional labelled-simulated `sleep` | - |

### 🚫 What this course never does

- **Never calls or wraps a hosted model** in any assessed activity.
- **Never uses `tiktoken.get_encoding`, `AutoTokenizer.from_pretrained`, `SentenceTransformer`,
  `fetch_20newsgroups`, Hugging Face datasets, or pretrained `sentencepiece` models** - all download.
  (`tokenizers` and `sentencepiece` *training* on local text works offline and is allowed.)
- **Never imports `torchvision`.** Image work is `load_digits()` and numpy images; the W5 augmentation
  cell uses jitter and `np.roll`.
- **Never needs a GPU.** Every training run states its expected CPU time; the three slowest are given
  a reduced default (W17, W19, W24) and a "full" setting marked optional.
- **Never presents a scripted result as evidence about a real model.**
- **Never presents a literature number as something the student measured.** It is marked
  *quoted, not reproduced here*.

### The datasets, all 36 weeks

| Weeks | Dataset | Where it comes from |
|:--:|---|---|
| 1-7 | Two interleaved spirals, 840 train / 360 val | **Generated by numpy** (`make_spirals`, seeded) |
| 5 | Augmentation | Gaussian jitter on spiral points; optional `np.roll` on `load_digits()` |
| 8-13 | Toy grammar sentences; 231 typed names | **Generated by Python**, seeded · typed by the student |
| 10-11 | Synthetic sequences of length 10-80 | `torch.randn`, seeded |
| 14-17, 19 | ~7,000-character corpus; copy / reverse / lookup tasks | **Typed**, inline · **generated by numpy** |
| 20 | Growing text: the course's own markdown, Python stdlib source | **On disk already** - read with plain `open(...).read()` (Level 2); `Path.glob` first appears in W26 |
| 21-22 | Width-sweep models on `load_digits()` or numpy data; 5-feature preferences; 4-outcome toy policy | ships in sklearn · **generated** |
| 23-24 | 8-case and 20-case prompt sets; in-context key-to-value and addition sequences | **Typed** · **generated** |
| 25-26 | 15-note notebook; auto-generated paraphrase pairs | **Typed** · template generator |
| 28-29 | Notes folder, task sentences for the tool router | **Typed** (about 60 sentences) |
| 30-31 | 30 labelled support tickets, 64 training tickets; template pretraining corpus | **Typed / generated** |
| 32-33 | 40 typed results; probe sets; L3 W33 sentiment pipeline | **Typed** · the student's own |
| 34-36 | Whatever the capstone needs from the above | Their own |

> **💡 When you have internet:** each of these weeks may carry **at most one** clearly marked optional
> callout - e.g. W20 *"compare your BPE with the GPT-2 vocabulary"*, W25 *"swap in a pretrained
> sentence encoder in three lines"*, W23/W28/W30/W33 *"point the same code at a hosted model"*. **It is
> always optional. No exercise, activity, workbook answer or assessment depends on it,** and a student
> who never once has internet finishes the level having missed nothing that is assessed. Each
> callout keeps the original reference-module code so nothing is lost for a student who can use it.

### The install

There is none. Level 3's five libraries (`numpy`, `pandas`, `matplotlib`, `scikit-learn`, `torch`) are
the whole stack. `tokenizers` is already present; W20 states that if `import tokenizers` fails, the
week still works without it (the student's own BPE is the deliverable). A `pip` failure (403) is
expected behind the proxy and is **not an error** - Week 1 says so, and shows the smoke test:

```python
import numpy, pandas, matplotlib, sklearn, torch
print(torch.__version__)
```

---

## 🚀 Capstone Outline (Weeks 34-36)

Derived from [`../capstone.md`](../capstone.md), rebuilt on the Shared Kit.

**The brief:** build an "Ask My Notes" style product using **at least two of three components**:
A. **RAG** over a notebook the student wrote (W25-26), B. **a tool-using agent** with guardrails
(W28-29), C. **a fine-tuned small model** with LoRA and a frozen eval (W30-31). The model behind A and B
is the local backend; behind C it is the student's own tiny encoder.

| Week | Milestone | Deliverable | Gate |
|:--:|---|---|---|
| 34 | **M1 Design** · **M2 Frozen eval** | `DESIGN.md` under seven headings: problem, user, why not a script, the two components, what could go wrong (ranked by **severity**, not likelihood), the budget committed *before* knowing if it can be met, what it will NOT do · `eval/cases.py` with 25 or more cases, committed with a hash before any `src/` exists | Cases are frozen; the design lists at least three failure modes |
| 35 | **M3 Baseline** · **M4 Spine** · **M5 Red-team pass** | A cheap baseline score; the two-component spine running end to end; `eval/run_eval.py` printing a per-category table on demand; tokens and latency measured locally; one attack per category A1-A5 run and logged; one regression caught by the suite | The suite runs in one command and matches the committed numbers; at least one attack fixed and re-tested, one accepted and documented |
| 36 | **M6 Demo** · **M7 System card** · **Assessment 4** | Five-minute demo on the real machine; `SYSTEM_CARD.md` (intended use, out of scope, measured numbers with sample sizes, failure modes, guardrails, retention, staged release, incident response, contact) · the final paper | Every claim in the card has a number and an n |

**Rubric weights (to be finalised by the owner):** eval design 25, measured evidence 25, guardrails
and red-team 20, honesty of the card 20, demo 10. The honest section - *what it fails at and who
should not rely on it* - is marked as heavily as the working code.

The one-line test from the reference README is kept as the final oral question: *"Here is a wrong
answer. Was it retrieval, generation, the prompt, the tokenizer, or a person over-trusting it? Show
me the evidence."*

---

## 🧰 Materials and If Something Goes Wrong

**The box:** a laptop, a notebook and pen (every week has a by-hand step), a ruler is still useful for
the log-log line in W21, and a printed copy of the week's hand-worked table.

**If something goes wrong** (full table in `HOW-TO-USE.md`): a run takes over a few minutes, use the
stated reduced defaults, never skip the seed · a number does not match the student guide to the last
digit, check `torch.set_num_threads(1)` and the seed first, then compare to the stated tolerance ·
`pip` returns 403, that is expected, close the terminal, nothing needs installing · a scripted result
seems "too clean", that is the point; restate the label aloud · a student reaches for `tiktoken`,
`from_pretrained` or an API key, the honest answer is "it would download; here is what we use".

---

## ⚠️ Risks and Open Questions

### Decisions the owner must make before authoring starts

1. **Fix the Level 4 reference README and modules first, or treat the course as authoritative?** The
   reference README still lists a credit card, an API key, `pip install` of `anthropic` and
   `sentence-transformers`, a 90 MB download, and ages 16-18. Modules 1-9 carry MPS numbers, API
   numbers, a `pip` line each, and the GPT-2 tokenizer. The repo rule is that the course must stay
   consistent with the modules. *Recommendation:* one **offline-patch pass over the nine modules
   before block 1**, in the spirit of L3's divergence from the CIFAR-10 CNN module, with each patch
   logged. The alternative (course diverges, modules keep the API path as "reference only") is cheaper
   and is a known source of drift.
2. **Learner age and the "16-18" claim.** The repo is one learner growing from 6th grade over two to
   three years; Level 3 was a 9th grader of about 14. Confirm Level 4's learner (this plan assumes
   15-16 and the same maths ceiling as Level 3).
3. **Is `tokenizers` allowed?** Level 3 bans `transformers`. The audit found `tokenizers` installed
   and able to train locally. This plan allows it for one week (W20) and one comparison. Confirm, or
   drop the comparison and keep only the student's own BPE.
4. **Depth of the FakeLLM.** The Shared Kit gives it *documented* competence functions. A richer fake
   is more fun and more misleading. *Recommendation:* keep it a transparent function of prompt
   features, and put all real learned behaviour in from-scratch models.
5. **Module 5's headline is lost.** The 59.4% to 78.1% to 90.6% zero-shot to few-shot story cannot be
   regenerated offline and is dropped as a measured claim. W24 re-earns the *idea* on a 2-layer
   transformer. Accept the change in tone: "watch examples in context help a model you trained".
6. **Course-wide scripted-label policy.** The plan requires the "stand-in, not a model" label
   (W23 onward). Confirm it also appears on the website pages (a banner in the generated HTML).
7. **Site integration.** Add an `ALL_LEVELS` entry for L4 (key `l4`, accent colour, term names).
   The plan table above keeps Level 3's exact column order, so `parse_weeks()` (which locates the type
   column) should work without change; the author should confirm the type words
   (`teach lab project review assessment capstone`) all exist in `TYPE_ICON`. `_level_is_complete()`
   will hold L4 back until all 108 weekly files exist, as designed.

### Content risks

| Risk | Where | Mitigation |
|---|---|---|
| **W22 is overloaded**: SFT masking, a reward model, and DPO with KL in one sitting | Module 4 compressed to 3 weeks | If authoring shows it does not fit, split into W22a/W22b by dropping W19 (lab) to a homework. Alternative: move DPO's `beta` sweep to a workbook-only exercise |
| **W24 is three toy models** (in-context, scratchpad, logit mask) | Module 5 compressed to 2 weeks | Time each on CPU in the ledger first; the logit-mask decoder can be homework |
| **W33 bundles** red-team, PII, retention and the bias probe | Module 9 compressed to 2 weeks | PII and retention can move to the capstone system-card week |
| **TinyGPT CPU time** | W17, W19 | Module 3's 2,500-step, 807k-parameter run was timed on MPS. Reference fallback: `d_model=64`, 2 layers, 1,500 steps. Decide by measurement |
| **Depth vs the ladder**: W11 unlocks `nn.LSTM`, which Level 3 banned | Syntax ladder | Allowed only after the student writes the cell by hand (W11 order of events) |
| **Numbers already in the modules that will drift**: 99.2% / 52.8%, 0.216, 0.413 (M1); 3.28e-12, 9.38e+06, 0.9526^40 (M2); 807,196 params and head tables (M3); 138 merges, 760 tokens, 702 GPT-2 tokens (M4) | All | **Ground-truth ledger** (see phasing, stage 0): execute every reference script on CPU, seed 0, torch 2.2, and store the real stdout. No block author may invent or copy a number |
| **Prerequisite chain between modules** | M5 to M9 share `FakeClient` and `rag.py` | Shared Kit written and unit-tested before block 7 is authored |
| **Module 3's Mamba/GPT-2/GPT-3 figures** | W16, W21 | Printed only inside *quoted, not reproduced* boxes |
| **Known defect class: stale output** | Everywhere | Each block authored with its real output in the same stage (the Level 3 rule) and audited by execution |
| **Weeks 34-35 reuse** all upstream modules | Capstone | Build the capstone starter last, using the finished kit |

### Open questions not decided here

- Whether Assessment 4 is a paper, a demo, or both (plan: both; paper is the Level 3 format).
- Whether the ladder may be relaxed in W22 (a fourth new idea) if the split is rejected.
- Whether a stretch "Level 4.5" week for PPO is wanted. (Plan: no; PPO is described only.)
- Pass mark and remediation table content for the four assessments.

---

## 💰 Cost and Phasing

Based on the recorded costs of Levels 1-3: **$900-1,200 per taught level**, bounded by **$300/day** and
**160 requests per 4 minutes**, with the lessons that teacher files are 1,500-1,800 lines (~100 KB),
that **three** authoring stages beat two, and that twelve concurrent agents die mid-write.

Level 4 is costlier per week than Level 3 for three reasons: every reference number must be
regenerated, the code is heavier (training runs to time), and the Shared Kit is new engineering.
**Estimate: about $1,400-2,150 all-in** (the stage ranges below sum to that; about five to seven days at the cap), broken down below.

| Stage | Work | Concurrency | Rough share |
|---|---|:--:|:--:|
| **0a** | Planner fixes (this file) · design-system agent writes `figures/STYLE.md` | 1-2 | $40-80 |
| **0b** | **Ground-truth ledger**: execute every script in the nine reference modules on CPU with torch 2.2 and store the real stdout and timings | 2 | $60-120 |
| **0c** | **Shared Kit**: write `l4lib/` with unit tests (FakeClient, rag, toyagent, tinytok, spirals) | 2 | $120-220 |
| **0d** | Offline patch of the nine reference modules (owner decision 1) | 3 | $150-250 |
| **1-4** | Twelve 3-week blocks, authored in **four waves of three concurrent blocks**. Each block: teacher guide, then student guides, then workbooks (three stages; downstream stages `grep` and offset-read the teacher file, never read it whole) | 3 | $800-1,100 |
| **5** | Extras: `HOW-TO-USE.md`, orientation, four assessments, projects, figures | 2 | $120-200 |
| **6** | **Audit as its own workflow on a fresh day**: execute every block, validate SVGs (`_gen_audit.py` must print `0 finding(s)`), crawl links, check both ladders | 2 | $100-180 |

**The twelve blocks and their waves:**

| Wave | Blocks (weeks) | Depends on | Notes |
|:--:|---|---|---|
| A | 1 (1-3) · 2 (4-6) · 3 (7-9) | Ledger (M1, M2 cell) | Pure spiral harness; cheapest wave |
| B | 4 (10-12) · 5 (13-15) · 6 (16-18) | Ledger (M2, M3) | Hand arithmetic for attention is the risk; keep teacher-file maths verified by code |
| C | 7 (19-21) · 8 (22-24) · 9 (25-27) | Ledger (M3, M4, M5, M6); **Shared Kit: `tinytok`, `fakellm`, `rag`** | Heaviest wave; consider running as two days |
| D | 10 (28-30) · 11 (31-33) · 12 (34-36) | **Shared Kit: `toyagent`**; Ledger (M7-M9) | Capstone block authored last, against the finished kit |

Rule carried over: each wave is a separate day's budget; never start wave C and D on the same day. Run
the audit (stage 6) only after all four waves, on a fresh day, as its own workflow, because as the last
phase of a build it was starved by the budget on every Level 3 run.

---

## ▶️ Start Here

1. **Owner:** settle the seven decisions in [Risks](#-risks-and-open-questions) above.
2. **Author:** run stages 0a to 0d. Nothing in blocks 1-12 may begin until the ground-truth ledger
   exists, because every number a block prints must be a number the ledger reproduced.
3. **Teacher (later):** read `teacher-guide/00-orientation.md`, then `teacher-guide/week-01.md`.
4. **Student (later):** `student-guide/week-01.md`, type every line, and run the smoke test first.

---

## 🧾 The Promise

By the end of Week 36 the student will have trained a network on purpose, built a GPT and a tokenizer
and the machinery that surrounds them, and attacked their own work. They will be able to tell a stranger
exactly which parts were real models, which were stand-ins, which numbers they measured, and which they
only quote. They will have done it with no account, no key and no download - and they will know, because
they built it, that **a number you cannot reproduce is not a result.**
