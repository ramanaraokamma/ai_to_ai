# 📕 Teacher Orientation — Level 4: Read This First

### *Read this once, with a pen, a calculator and a terminal open. About two and a half hours. Then you can teach all 36 weeks of Level 4, including the thirteen small pieces of maths, the scripted "models" you must never confuse with real ones, and the errors this level actually produces.*

[⬅ Course home](../README.md) · [Week 1 teacher guide](week-01.md) · [Week 1 student guide](../student-guide/week-01.md) · [Level 4 glossary](../../glossary.md)

---

## 🪝 You Do Not Need to Know AI to Teach This

Let me be direct about the thing you are probably worried about.

Level 4 has a transformer in it, a tokenizer, retrieval, an agent, a reward model and a fine-tune.
Those words are why adults quietly hand this material to somebody else. Here is the actual situation:

> **Everything the student is asked to compute is arithmetic you can do with a calculator, and
> everything the student is asked to build is small enough to read in one sitting. The hard part of
> this level is not the maths and not the code. It is knowing, at every moment, which thing on the
> screen is a real model and which thing is a short Python script dressed up as one.**

That last sentence is the reason this file is longer than the Level 3 maths warm-up would suggest, and
it is why §5 of this file is the one you must not skim.

Level 3 ended with a student who could write five lines of training loop and prove every number in
them. Level 4 asks: *what are the ten decisions hiding inside that loop, what machine turns it into
language, and how do you build something on top of it that you can defend?* The whole year is one
answer to that, in four terms of nine weeks.

### What is actually being asked of you

| You do NOT need to | You DO need to |
|---|---|
| Know what a transformer, an LSTM or a tokenizer is | Open the week's file 20 to 60 minutes before class and do the hand arithmetic in it, with a pencil |
| Know any calculus or linear algebra beyond Level 3 | Be able to multiply decimals, take a square root, and read a table of numbers |
| Have used an LLM, an API or a vector database | Say, out loud and often, *"this is a stand-in, not a model"* when it is one |
| Know Python beyond Level 3 | Read §4 of this file once; it covers the five pieces of Python that are new *in kind* |
| Get every answer right in class | Say *"I don't know. Let's measure it."* and then measure it in front of them |
| Be fast | Be willing to be slow in public, and to let a run finish while you say nothing |
| Trust a number because it is printed | Ask of every number: *which rows, how many, which seed, real or stand-in?* |

### Six things that are true of every week

These are the course's own promises (the [course README](../README.md) states them too). Knowing them
tells you what to check when something looks wrong.

1. **Every code block in every teacher guide was run before it was pasted**, on a CPU, with a seed
   set, and every output shown is the real output. The reference modules' numbers came from a GPU and
   a live API and are **not trusted**; only numbers in the week files and in `_ledger/` are.
2. **Every new mathematical idea is computed numerically before it is named.** Thirteen weeks carry
   one; twenty-three carry none.
3. **Every week shows at least one real error**, copied from a real failed run and read line by line.
4. **Nothing downloads.** No API, no account, no key, no pretrained weights, no `torchvision`, no `pip`.
5. **Toy results demonstrate a mechanism, not a rate.** Every week has a *What you must NOT claim* box.
6. **Any number quoted from the literature is labelled "quoted, not reproduced here"** and is never an
   exercise.

### One warning, and it is the important one

Every teacher file opens with **🧑‍🏫 What YOU Need to Know First**, which always contains a
**🧭 Real vs stand-in** table and a **🔢 maths taught to you first** section (the latter says
*"there is no new maths this week"* on 23 weeks). **Read the first; do the second with a pencil.**

A student can tell within ninety seconds the difference between an adult who has done the arithmetic
and one who has read about it, and what they conclude is *"this is the kind of thing you read about,
not the kind of thing you do."* That conclusion is the failure mode of the whole programme.

The second failure mode is new in Level 4. From Week 23 onward, parts of the course run against
scripted stand-ins. A teacher who does not know this will say *"the model obeyed the hidden
instruction 15 times in 50"* as though it were a fact about AI. It is a fact about a number somebody
typed into a Python file. §5 is how you avoid that sentence.

### How to read this file

| Part | What | Read it |
|---|---|---|
| §1 | What Level 4 is, and what the student arrives with | Now |
| §2 | The four terms, and what to listen for in each | Now |
| §3 | The thirteen small ideas of maths, done on real numbers | Now, with a pencil (45 min) |
| §4 | The Python that is new in kind | Now (15 min); again before Weeks 4, 16 and 23 |
| §5 | Real, invented, stand-in, quoted: the policy and the kit | Now, **slowly** (30 min) |
| §6 | How a lesson runs, pacing, and the heavy weeks | Now |
| §7 | Setup: the smoke test, the kit self-test, the timing check | Before Week 1, alone |
| §8 | The sixteen errors, and what to do when a run fails | Now; return to it when stuck |
| §9-§12 | Questions students ask; what adults get wrong; helping; marking | Now, lightly; return as needed |
| §13 | The pre-flight checklist and the cheat-sheet card | Print it |

> **If this file and a week file ever disagree, the week file wins.** The week file has the run
> output for that week. This file is the manual; the week files are the facts. Where this file quotes
> a number, it names the week it comes from.

---
---

# 🧭 Section 1 — What Level 4 Is

## 1.1 — The question changes

Last year's question was *"does it learn?"* and the answer was a loss that went down. This year's is
*"when it does not, which knob do I turn, and how do I know before I turn it?"* Week 1 opens with the
loop the student already owns and names the ten things in it that nobody named:

```python
import inspect
from l4lib.spirals import run
print(inspect.signature(run))
```
```text
(tag, *, depth=4, lr=0.003, batch_size=64, epochs=60, optimizer='adamw', weight_decay=0.0, dropout=0.0, norm='none', residual=False, schedule='none', warmup_frac=0.0, clip=None, seed=0, verbose=True)
```

Ten of those are **knobs** (they change *how it learns*); four are set-up (`depth`, `epochs`, `seed`,
`verbose`). The knobs, and the week each one is first turned alone:

| # | Knob | Plain meaning | Turned alone in |
|:--:|---|---|:--:|
| 1 | `lr` | How big a step each update takes | Week 1 |
| 2 | `batch_size` | How many examples are averaged before one step | Weeks 4 and 7 |
| 3 | `optimizer` | The rule that turns a gradient into a step (`sgd`, `momentum`, `adam`, `adamw`) | Weeks 2-3 |
| 4 | `weight_decay` | A small shrink applied to every weight each step | Week 3 |
| 5 | `schedule` | Whether `lr` changes over the run (`none`, `cosine`, `step`) | Week 4 |
| 6 | `warmup_frac` | The share of the run spent ramping `lr` up from nearly zero | Week 4 |
| 7 | `dropout` | The share of activations randomly zeroed while training | Week 5 |
| 8 | `norm` | Whether each block normalises its input (`none`, `batch`, `layer`) | Week 6 |
| 9 | `residual` | Whether each block adds its input back to its output | Week 6 |
| 10 | `clip` | A ceiling on how long a gradient may be | Week 6 |

The method is **one knob alone, so the loss curve is the witness**. From Week 7 it becomes the
playbook: *symptom, check, action*, with three seeds and a mean and a spread, not one lucky run.

The rest of the year uses that discipline on bigger things: a recurrent cell that forgets (Weeks
8-13), attention and a GPT built from `nn.Linear` up (Weeks 14-19), a tokenizer, scaling and
post-training (Weeks 20-22), then the engineering around a model (Weeks 23-33), then a capstone
(Weeks 34-36).

## 1.2 — Who the student is, and what they arrive with

One student, about 15 or 16, who has **finished Level 3 including Weeks 34-36** (the shipped
artifact). The honest profile:

| They can | They have never seen |
|---|---|
| Write the five-line training loop from memory | Any optimizer except SGD; Adam only as a name |
| Derive backprop by hand for a 2-layer net and watch PyTorch agree to 8 decimals | A recurrent network, attention, a tokenizer |
| Measure a slope by nudging by 0.001 and dividing | `lambda`, a class with `__init__` that is not an `nn.Module`, `@dataclass` |
| Train a digits CNN; build a bag-of-words sentiment engine and watch it fail on word order | An LLM API, a prompt harness, retrieval, an agent |
| Say "0.94 on which rows? what's the baseline?" | A frozen evaluation set, a judge, kappa, calibration |
| Keep a Bug Log and read a traceback bottom-up | Red-teaming |

**Seven things Level 3 did not teach that the reference modules silently assume.** Each is scheduled
by hand in one week, and none appears earlier:

| Gap | Introduced in |
|---|---|
| Exponential moving average | Week 2, by hand on five numbers |
| `sqrt` and epsilon as a "typical size" | Week 3 |
| `lambda` | Week 4 |
| `nn.Embedding`, `nn.Dropout`, `nn.LayerNorm`, `clip_grad_norm_` | Weeks 8, 5, 6 |
| `nn.LSTM` / `nn.GRU` (Level 3 lists them as *deliberately not taught*) | Week 11, only after the student has written the cell by hand |
| KL divergence, Brier score, binomial SD, Cohen's kappa | Weeks 22, 32, 33, 30 |
| `@dataclass`, custom exceptions, classes with `__init__` | Week 23 |

If the student used a word in Level 3 (gradient, variance, softmax, cosine similarity, train/test
leakage) you may use it. If it is not in Level 3 and not yet in the Level 4 ladders in the
[course README](../README.md#-the-maths-ladder), **do not use it.** The ladders are enforced, and the
commonest way a well-meaning adult breaks them is by saying "oh, it's just the KL" in Week 12.

## 1.3 — The three books, and the seven rules

```
   ┌─────────────────────────┬──────────────────────────┬──────────────────────────┐
   │  📕 TEACHER GUIDE       │  📗 STUDENT GUIDE        │  📘 WORKBOOK             │
   │  teacher-guide/week-NN  │  student-guide/week-NN   │  workbook/week-NN.md     │
   ├─────────────────────────┼──────────────────────────┼──────────────────────────┤
   │  You, alone, 20-60 min  │  The student, at the     │  The student, alone,     │
   │  before class           │  keyboard, in and after  │  after class, 55-75 min  │
   │  Every answer, every    │  class                   │  Answer key at the       │
   │  mistake, the real      │  Hook, concept, code,    │  bottom, behind a        │
   │  output                 │  one real error          │  "struggle first" note   │
   └─────────────────────────┴──────────────────────────┴──────────────────────────┘
```

1. **The student never opens the teacher guide.** It contains every answer and names the mistakes they
   are about to make.
2. **You do not skip the teacher guide**, especially on the 13 weeks that carry a new maths idea.
3. **The workbook answer key stays sealed** until they have struggled for 15 minutes.
4. **Nobody pastes code.** In Level 4 this matters more than it did: a typed-in `bpe.py` *is* the
   point of Week 20.
5. **Every hand calculation is checked by code, and every code result is checked by hand at least once.**
6. **Any number a student writes in a report must have been printed by their own run, with a seed,
   within the last 24 hours.** The guide's numbers are never a substitute. (This is the rule that
   makes the capstone work.)
7. **Weeks that use a scripted backend open with its label: "This is a stand-in for a model, not a
   model."** The student says it aloud. You say it first, the first time.

The course README also names separate `assessments/` and `projects/` folders. They are written as
extras, alongside this file, and may or may not be present when you read it. **No week depends on
them:** the four term papers (with their keys and marking sheets) live inside the teacher guides of
Weeks 9, 18, 27 and 36, and the capstone is taught from Weeks 34-36 plus the reference
[`capstone.md`](../../capstone.md).

## 1.4 — What the student walks out with

By June, if you have taught it as written, the student can show you **files that run and numbers
they can reproduce**:

| Term | Artifact | The number they can quote |
|:--:|---|---|
| 1 | A SYMPTOM-CHECK-ACTION playbook backed by a three-seed sweep over the six knobs | Mean and spread, not one run |
| 1 | Adam, momentum and a cosine schedule rebuilt by hand and matching `torch.optim` | To the last printed digit |
| 1-2 | A recurrent cell unrolled on paper and checked; a measured vanishing gradient and the gate that fixes it | A measured gradient at position 1, far below the last position's |
| 2 | A character-level name generator with four samplers | A measured novelty rate |
| 2 | **TinyGPT**, written from `nn.Linear` up, trained on CPU on 6,972 typed characters | Initial loss within 0.05 of `ln 28 = 3.332`; the train/validation gap |
| 3 | An ablation table (what breaks when each component is deleted); their own byte-level BPE; a four-point scaling line | Bytes per token; a slope near `-0.126` |
| 3 | SFT loss-masking, a reward model and DPO on toy data | A KL in nats |
| 3 | A prompt bench with a frozen set and a floor; a RAG system that cites and refuses | recall@k on questions they wrote first |
| 4 | An agent whose six fences fire with no model present; a fine-tune whose regression a frozen eval caught | Per-category table |
| 4 | A red-team report with before/after fractions, and a system card | Every claim carries a number and an *n* |

And the reflex the level exists to install, which is also the final oral question (Week 36):

> *"Here is a wrong answer. Was it retrieval, generation, the prompt, the tokenizer, or a person
> over-trusting it? Show me the evidence."*

---
---

# 🗓️ Section 2 — The Four Terms

Nine weeks each. Each term answers one question the student can say out loud at the end, while
showing a file that runs and a number they can reproduce.

```
   Wk  1  2  3  4  5  6  7  8  9 |10 11 12 13 14 15 16 17 18 |19 20 21 22 23 24 25 26 27 |28 29 30 31 32 33 34 35 36
   ty  T  T  T  T  L  T  P  T  A |L  T  L  T  T  T  T  L  A |L  L  T  T  T  L  T  L  A |T  L  T  L  T  L  P  P  C
   ∑   .  ∑  ∑  .  .  ∑  .  .  . |∑  .  .  .  ∑  ∑  .  .  . |.  .  ∑  ∑  .  .  .  .  . |.  ∑  ∑  ∑  ∑  ∑  .  .  .

   T teach · L lab · P project · A assessment (paper) · C capstone        ∑ = carries one new maths idea
```

That is 18 teach weeks, 11 labs, 3 projects, 3 review-and-assessment weeks and the capstone. Thirteen
weeks carry a new idea of maths: 2, 3, 6, 10, 14, 15, 21, 22, 29, 30, 31, 32, 33.

## Term 1 (Weeks 1-9) — Train it on purpose

**Question:** *Your loss curve is wrong. Which of ten knobs do you turn, and how do you know before
you turn it?*

| Weeks | What happens |
|---|---|
| 1 | The six-learning-rate sweep; `0.693` is a coin |
| 2-3 | Momentum (an exponential moving average) and Adam (a root-mean-square), both rebuilt by hand and matched to `torch.optim` |
| 4 | Schedules and batch size, and why "bigger batch, better" is confounded by fewer steps |
| 5 | Four ways to stop memorising, on 120 noisy points |
| 6 | Batch norm vs layer norm; residuals as a gradient highway |
| 7 | **Project:** the playbook, with a sweep over six knobs and three seeds |
| 8 | The first recurrent cell, unrolled on paper |
| 9 | **Assessment 1** (paper, 75 minutes, 75 marks) |

**Listen for:** *"That curve is flat, not dead; it might just be slow."* *"That change is confounded:
I changed the batch size and the number of steps at the same time."* **Red flag:** *"Adam is better
than SGD."* It is better at one setting on one network; Week 3's clinic shows what happens when you hand Adam the learning rate that was best for SGD.

## Term 2 (Weeks 10-18) — Memory, then attention

**Question:** *Why can a network not remember forty steps back, and what did people build instead of
making it remember?*

| Weeks | What happens |
|---|---|
| 10 | Forty multiplications: a measured gradient at position 1 that is a tiny fraction of the last one, and `0.9526^40 = 0.143` by hand |
| 11 | Gates: a cell that adds instead of multiplies; the cell written by hand, then `nn.LSTM` |
| 12-13 | A character model that invents names, four ways to sample, and exposure bias |
| 14 | **Attention by hand**: a three-token pass with a pen *before* any PyTorch |
| 15 | Scale by `sqrt(d)`, the mask, several heads |
| 16 | Positions and the transformer block |
| 17 | **Build TinyGPT**; its first loss is a check, not a hope |
| 18 | **Assessment 2** |

**Listen for:** *"The gradient at position 1 is tiny"* (not *"RNNs can't learn long things"*, which
Week 10 explicitly refuses to claim). *"That weight row adds to 1."* **Red flag:** *"the model pays
attention to the important word."* The weights are a softmax of dot products of numbers; "important"
is not in the arithmetic (Week 14, box 1).

## Term 3 (Weeks 19-27) — How it is made, how it is asked

**Question:** *Where does a language model's behaviour come from, and how do you test what you ask it,
and what you retrieve for it, like an engineer?*

| Weeks | What happens |
|---|---|
| 19 | Ablations: delete mask, positions, residual, layer norm in turn; name a head from its heatmap |
| 20 | **Tokenizers:** write BPE from scratch; it round-trips emoji and Devanagari |
| 21 | **Pretraining and scaling:** four model widths, a straight line on log-log paper, one extrapolated point |
| 22 | **SFT, a reward model and DPO** on toy data (the structurally heaviest teach week) |
| 23 | **Prompting as engineering:** the harness, the frozen set, the floor; **first stand-in** (`FakeClient`) |
| 24 | Learned-in-context behaviours, on models the student trains (**no stand-in in any number**) |
| 25-26 | Embeddings, then RAG that retrieves, cites, verifies the citation in code, and refuses |
| 27 | **Assessment 3** |

**Listen for:** *"That ablation went down when I removed the mask. That's a leak, not an
improvement."* (Week 19's table has exactly that trap: the no-mask model gets the best number of all,
`0.077`, because it reads the answer.) *"That's the stand-in's number, not a model's."*
**Red flag:** *"the scaling law says..."* They measured four points. They did not test any published law.

## Term 4 (Weeks 28-36) — Agents, evidence, and the system card

**Question:** *You have built the parts. Can you build a product out of them, prove it works, attack it
yourself, and tell a stranger honestly where it breaks?*

| Weeks | What happens |
|---|---|
| 28 | Tools and the loop: six fences that work with the model unplugged |
| 29 | Injection and budget: which defence actually holds; the cost of re-sent history grows like `k^2` |
| 30 | Evaluating LLM systems: freeze the eval, beat the cheap baseline, test the judge |
| 31 | Fine-tuning, LoRA, and the regression a frozen eval catches |
| 32 | Calibration and abstention: "I don't know" as a measured feature |
| 33 | Attack your own system: red-team, redact, retain, and ask whether 20 runs can see a gap |
| 34-36 | **Capstone:** design and freeze 25 cases (34); build, measure, attack (35); demo, system card, and the final paper (36) |

**Listen for:** *"That's 17 against 15 out of 50. That's inside the wobble."* *"My model's average went
up and one category fell."* **Red flag:** any sentence that ends *"...so RAG/agents/fine-tuning doesn't
work."* Every rate measured in Term 4 is a property of a stand-in or of a 30-ticket toy.

## Where the course can slip, honestly

| Week | Risk | What to do |
|---|---|---|
| **22** | Three ideas (SFT masking, a reward model, DPO with a KL) in one sitting | The week file says what to cut; the `beta` sweep can be homework. Do not add a fourth |
| **24** | Three from-scratch toy models, about four minutes of training inside the class | Start the long run before the hook; the logit-mask decoder can be homework |
| **33** | Red-team, PII, retention and a bias probe | PII and retention can move to the system-card week |
| **17, 19, 21, 24** | Runs of 85 s, 3.6 min, 2 x 90 s and about 4 minutes | See §6.3; never shorten the seed or the step count silently |
| **34-35** | Heaviest take-home of the year (about 90 and 150 minutes) | Tell the student on the day you set it, not two days before it is due; allow two and three sittings |
| **36** | Three things do not fit in one hour | **Two sittings**, the paper on a different day from the demo (§6.4) |

---
---

# 🔢 Section 3 — The Thirteen Ideas of Maths, on Real Numbers

Every one of these is arithmetic. **Do each on paper first, then run the block** (the block is the
check on your pencil, never the other way round). Each is the same worked example its week uses, so
when the week arrives you will have met the numbers already. The student has met none of them.

A rule for the whole section, and for the whole year:

> **Number first, name second, symbol third, and often skip the third.** Say "typical size" before
> "root-mean-square". Say "how far it has moved" before "KL divergence". If a symbol is not in the
> week file, it is not on your board.

## 3.1 — Week 2: the exponential moving average

*"New average = 0.9 x old average + 0.1 x new value."* A running average that forgets the old by a fixed
share each step. Feed it a single `10` followed by zeros and watch the ten fade:

```python
old = 0.0
for step, value in enumerate([10, 0, 0, 0, 0], start=1):
    old = 0.9 * old + 0.1 * value
    print(f"step {step}: value {value:>2}   average {old:.4f}")
```
```text
step 1: value 10   average 1.0000
step 2: value  0   average 0.9000
step 3: value  0   average 0.8100
step 4: value  0   average 0.7290
step 5: value  0   average 0.6561
```

Each line is exactly 0.9 times the one above. **That is the whole idea**, and momentum (Week 2) is a
step that uses this average instead of the latest gradient. How long until the first value counts for
half? Count by hand (0.9, 0.81, 0.729, ...). It crosses one half between step 6 and step 7; the exact
figure is `ln 0.5 / ln 0.9`:

```python
import math
share, n = 1.0, 0
while share > 0.5:
    share *= 0.9
    n += 1
print("first step at which the first value counts for less than half:", n)
print("exact crossing:", round(math.log(0.5) / math.log(0.9), 2))
```
```text
first step at which the first value counts for less than half: 7
exact crossing: 6.58
```

Say "half-life" once and move on. **Do not** quote a half-life for 0.99 unless you have run it.

## 3.2 — Week 3: the root-mean-square, and epsilon

*"Square every number, average the squares, take the root."* The typical size of a list, ignoring
sign. It is what Adam divides by.

```python
import numpy as np
g = np.array([3.0, -4.0])
print("plain mean      :", g.mean())
print("squares         :", (g ** 2).tolist())
print("mean of squares :", (g ** 2).mean())
print("root of that    :", round(float(np.sqrt((g ** 2).mean())), 4))
for scale in [1, 100, 1000]:
    big = g * scale
    rms = np.sqrt((big ** 2).mean())
    print(f"list {big.tolist()}  rms {rms:.4f}  list / rms {np.round(big / rms, 4).tolist()}")
```
```text
plain mean      : -0.5
squares         : [9.0, 16.0]
mean of squares : 12.5
root of that    : 3.5355
list [3.0, -4.0]  rms 3.5355  list / rms [0.8485, -1.1314]
list [300.0, -400.0]  rms 353.5534  list / rms [0.8485, -1.1314]
list [3000.0, -4000.0]  rms 3535.5339  list / rms [0.8485, -1.1314]
```

The sentence of the week is the last three lines: **divide a list by its typical size and the scale
disappears.** That is why Adam's first step is `lr` whatever the gradient's size (1 or 1000 in the
workbook). The epsilon is a tiny number added so you never divide by zero. It should be too small to
matter, and it stops being too small only when the gradient itself is as small as epsilon:

```python
eps, lr = 1e-8, 0.1
for g in [1000, 1, 1e-3, 1e-6, 1e-8, 1e-9]:
    print(f"gradient {g:>8g}   first step {lr * g / (g + eps):.6f}")
```
```text
gradient     1000   first step 0.100000
gradient        1   first step 0.100000
gradient    0.001   first step 0.099999
gradient    1e-06   first step 0.099010
gradient    1e-08   first step 0.050000
gradient    1e-09   first step 0.009091
```

(This is the rule `g / (|g| + eps)` applied to a single step with a fresh average; Week 3's Block P10
prints the same column. The student is asked to see the first row and the last.)

> **Do not** say "standard deviation" when you mean this. A standard deviation subtracts the mean
> first; the RMS does not. If the student says "that's standard deviation": *"close cousin: that one
> measures spread around the average; this one measures size around zero."* Stop there.

## 3.3 — Week 6: the slope of a sum

Nudge `x` in `y = x + f(x)` and see that the slope is **1 plus whatever `f` does**. This is what
makes a residual connection a "highway": the `1` is always there. The week's `f` is `0.05 x^2`:

```python
def f(x):
    return 0.05 * x * x

h = 0.001
x = 2.0
slope_f = (f(x + h) - f(x - h)) / (2 * h)
y = lambda x: x + f(x)
slope_y = (y(x + h) - y(x - h)) / (2 * h)
print("slope of f at 2        :", round(slope_f, 4))
print("slope of x by itself   :", 1.0)
print("slope of x + f(x) at 2 :", round(slope_y, 4))
```
```text
slope of f at 2        : 0.2
slope of x by itself   : 1.0
slope of x + f(x) at 2 : 1.2
```

**Say it in words:** *the slope of a sum is the sum of the slopes, and the slope of `x` by itself is
1.* (This block uses `lambda`, which the student meets in Week 4, so it is fair for Week 6.) **Do not
write `1 + f'(x)`** in Week 6; the symbol comes after the student has said it themselves.

## 3.4 — Week 10: compounding

A number multiplied by itself `T` times. The surprise is the whole lesson: 5% a step is **not** "about
the same" after forty steps.

```python
print(f"{'k':>3} {'0.9526**k':>10} {'0.95**k':>9} {'1.05**k':>9}")
for k in [1, 2, 5, 10, 20, 40]:
    print(f"{k:>3} {0.9526 ** k:>10.4f} {0.95 ** k:>9.4f} {1.05 ** k:>9.3f}")
print("0.5 ** 40 =", f"{0.5 ** 40:.1e}")
```
```text
  k  0.9526**k   0.95**k   1.05**k
  1     0.9526    0.9500     1.050
  2     0.9074    0.9025     1.103
  5     0.7844    0.7738     1.276
 10     0.6153    0.5987     1.629
 20     0.3786    0.3585     2.653
 40     0.1434    0.1285     7.040
0.5 ** 40 = 9.1e-13
```

The last line is the week: a recurrent cell whose typical slope is 0.5 hands the start of a
forty-step sentence `9e-13` of the signal. Have the student **commit to a guess in writing before
you run it**; the gap between the guess and the table is the lesson. **Do not** solve `r^k = 0.5`
with logarithms (that is Week 21); a `while` loop finds it (15 for 0.9526).

## 3.5 — Week 14: the weighted average, and a whole attention pass

A mean where some values count more; the weights are not negative and add to 1. Then attention is
nothing but this, three times:

```python
import numpy as np
vals = np.array([10, 50, 30])
for w in ([0.7, 0.2, 0.1], [1/3, 1/3, 1/3], [0, 1, 0]):
    print(np.round(w, 3).tolist(), "->", round(float(np.dot(w, vals)), 2))

X  = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)   # the, cat, sat: INVENTED vectors
Wq = np.eye(2)
Wk = np.eye(2)
Wv = np.array([[0, 1], [1, 0]], dtype=float)           # swap the two numbers
Q, K, V = X @ Wq, X @ Wk, X @ Wv
scores = Q @ K.T
weights = np.exp(scores) / np.exp(scores).sum(axis=1, keepdims=True)
print("scores\n", scores)
print("weights (each row adds to 1)\n", np.round(weights, 4))
print("row sums:", weights.sum(axis=1).tolist())
print("output\n", np.round(weights @ V, 3))
```
```text
[0.7, 0.2, 0.1] -> 20.0
[0.333, 0.333, 0.333] -> 30.0
[0, 1, 0] -> 50.0
scores
 [[1. 0. 1.]
 [0. 1. 1.]
 [1. 1. 2.]]
weights (each row adds to 1)
 [[0.4223 0.1554 0.4223]
 [0.1554 0.4223 0.4223]
 [0.2119 0.2119 0.5761]]
row sums: [1.0, 1.0, 1.0]
output
 [[0.578 0.845]
 [0.845 0.578]
 [0.788 0.788]]
```

Those three output rows (`[0.578, 0.845]`, `[0.845, 0.578]`, `[0.788, 0.788]`) are what the student
computes with a pen in Week 14. **Tell them to carry four places in the weights** and round only the
answer; a student who rounds weights to three places gets `[0.577, 0.844]` and is also right. The
vectors are **invented** so they are easy to multiply. Nobody trained them.

## 3.6 — Week 15: variances add

Spreads of independent wobbles combine as squares: `3` and `4` make `5`, not `7`. A dot product of two
random `d`-long vectors is a sum of `d` such wobbles, so its spread grows like `sqrt(d)`. **This is why
attention divides by `sqrt(d)`.** Measured, not proved:

```python
import numpy as np
rng = np.random.default_rng(0)
a, b = rng.normal(0, 3, 100000), rng.normal(0, 4, 100000)
print("spread of a + b:", round(float((a + b).std()), 2), "  (3 and 4 make 5, not 7)")
for d in (4, 16, 64):
    q = rng.normal(size=(100000, d))
    k = rng.normal(size=(100000, d))
    print(f"d = {d:>2}   spread of q . k = {(q * k).sum(axis=1).std():.2f}   after / sqrt(d) = {((q * k).sum(axis=1) / np.sqrt(d)).std():.2f}")
s = np.array([8.0, -2.0, 1.0])
soft = lambda v: np.round(np.exp(v) / np.exp(v).sum(), 5)
print("softmax of [8, -2, 1]        :", soft(s).tolist())
print("softmax of the same / sqrt(64):", soft(s / 8).tolist())
```
```text
spread of a + b: 5.01   (3 and 4 make 5, not 7)
d =  4   spread of q . k = 2.01   after / sqrt(d) = 1.01
d = 16   spread of q . k = 4.00   after / sqrt(d) = 1.00
d = 64   spread of q . k = 7.99   after / sqrt(d) = 1.00
softmax of [8, -2, 1]        : [0.99904, 5e-05, 0.00091]
softmax of the same / sqrt(64): [0.58707, 0.1682, 0.24473]
```

The honest limit (say it only if asked): the argument needs the terms to be independent and random,
which is true of untrained tables at the start of training and need not be true later. Week 15's
`key.py` shows 64 copies of one number giving a spread of 64, not 8.

## 3.7 — Week 21: the log-log straight line

A power law `y = a x^-b` becomes a straight line when both axes are logged, and the slope is the
exponent. Three points first (`y = 100 / x`), then the week's four small GPTs (Week 21's own
losses, quoted here as that week prints them):

```python
import numpy as np
x = np.array([10.0, 100.0, 1000.0])
print("y = 100/x  slope, intercept:", np.round(np.polyfit(np.log10(x), np.log10(100 / x), 1), 3).tolist())

knobs = np.array([14549, 41173, 131285, 458965])
loss = np.array([2.2760, 2.0878, 1.7127, 1.4991])
slope, intercept = np.polyfit(np.log10(knobs), np.log10(loss), 1)
print("four widths: slope", round(float(slope), 4), " intercept", round(float(intercept), 4))
print("ten times the knobs multiplies the loss by", round(float(10 ** slope), 3))
print("doubling the knobs multiplies the loss by  ", round(float(2 ** slope), 3))
pred = 10 ** (slope * np.log10(1704149) + intercept)
print("line's prediction for 1,704,149 knobs:", round(float(pred), 3))
```
```text
y = 100/x  slope, intercept: [-1.0, 2.0]
four widths: slope -0.1262  intercept 0.8886
ten times the knobs multiplies the loss by 0.748
doubling the knobs multiplies the loss by   0.916
line's prediction for 1,704,149 knobs: 1.265
```

Say "ratio", not "subtract": the thing that stays the same is a *ratio*. The week then trains the
fifth model and reports the miss (about 16%, which is the honest part: four points are a description,
not a law). The published scaling results are **quoted, not reproduced**.

## 3.8 — Week 22: KL divergence

The average log-ratio of two tables of chances, weighted by the new table: *how far has the policy
moved from the reference.* Always say which is first.

```python
import numpy as np
q = np.array([0.25, 0.25, 0.25, 0.25])      # the reference: where we started
def kl(p, q):
    p, q = np.asarray(p), np.asarray(q)
    mask = p > 0                             # 0 * ln 0 counts as 0
    return float(np.sum(p[mask] * np.log(p[mask] / q[mask])))

p1 = [0.50, 0.25, 0.125, 0.125]
p2 = [0.70, 0.10, 0.10, 0.10]
print("KL(p1 || q) =", round(kl(p1, q), 4))
print("KL(p2 || q) =", round(kl(p2, q), 4))
print("KL(q || p2) =", round(kl(q, p2), 4), " <- not symmetric")
print("KL(q || q)  =", kl(q, q))
print("plain average of ln(p1/q), NOT KL:", round(float(np.mean(np.log(np.array(p1) / q))), 4))
```
```text
KL(p1 || q) = 0.1733
KL(p2 || q) = 0.4458
KL(q || p2) = 0.4298  <- not symmetric
KL(q || q)  = 0.0
plain average of ln(p1/q), NOT KL: -0.1733
```

Three facts to own: it is `0` exactly when nothing moved; it is never negative; it is **not**
symmetric. The plain average in the last line is negative, which is why "weighted by `p`" is not
decoration. Bradley-Terry (the reward model's loss) reuses Level 3's sigmoid and `ln` and needs
nothing new.

## 3.9 — Week 29: the triangular sum

`1 + 2 + ... + k = k(k+1)/2`, and why the bill for an agent grows like `k x k`: every turn re-sends
everything said so far.

```python
print("pair the ends:", [(i, 11 - i) for i in range(1, 6)], "-> five pairs of 11 =", 5 * 11)
for k in (10, 20, 30):
    print(f"k = {k}:  sum(range(1, k+1)) = {sum(range(1, k + 1))}   k(k+1)/2 = {k * (k + 1) // 2}")
n0, grow = 223, 32.5     # Week 29's measured first-turn tokens and per-step growth
for k in (10, 30):
    print(f"k = {k}: total input tokens = {n0 * (k + 1) + grow * k * (k + 1) / 2:.1f}")
```
```text
pair the ends: [(1, 10), (2, 9), (3, 8), (4, 7), (5, 6)] -> five pairs of 11 = 55
k = 10:  sum(range(1, k+1)) = 55   k(k+1)/2 = 55
k = 20:  sum(range(1, k+1)) = 210   k(k+1)/2 = 210
k = 30:  sum(range(1, k+1)) = 465   k(k+1)/2 = 465
k = 10: total input tokens = 4240.5
k = 30: total input tokens = 22025.5
```

Week 29 measures `4238` and `22018` for the scripted agent and these formulas give `4240.5` and
`22025.5`. **The fit is to a scripted agent's token counter, not to a hosted model's bill.**

## 3.10 — Week 30: Cohen's kappa

Agreement with the agreement-by-luck removed. Two raters, 20 replies, one strict and one lenient:

```python
from sklearn.metrics import cohen_kappa_score
H = ["pass"] * 7 + ["fail"] * 13                        # strict rater H: 7 pass, 13 fail
J = ["pass"] * 7 + ["pass"] * 7 + ["fail"] * 6           # lenient rater J: 14 pass, 6 fail
# pairs: 7 both pass, 7 J-pass/H-fail, 6 both fail, 0 J-fail/H-pass
po = (7 + 6) / 20
pe = (14 / 20) * (7 / 20) + (6 / 20) * (13 / 20)
print("agree", po, " luck", round(pe, 2), " kappa", round((po - pe) / (1 - pe), 4), " library:", round(cohen_kappa_score(H, J), 4))
lazy_judge = ["pass"] * 20
human = ["pass"] * 18 + ["fail"] * 2
agree = sum(a == b for a, b in zip(lazy_judge, human)) / 20
print("lazy judge: agreement", agree, " kappa", cohen_kappa_score(lazy_judge, human))
```
```text
agree 0.65  luck 0.44  kappa 0.375  library: 0.375
lazy judge: agreement 0.9  kappa 0.0
```

The last line is the sentence to leave the student with: **ninety percent agreement, zero skill.**
Kappa is undefined when both raters only ever say one thing.

## 3.11 — Week 31: low-rank

A big grid as a thin column times a thin row needs far fewer numbers. LoRA stores two thin grids:

```python
import numpy as np
col = np.array([[1], [2], [0], [-1]])
row = np.array([[2, 1, 0, 3]])
grid = col @ row
print(grid)
print("16 cells from 4 + 4 = 8 numbers; rank:", np.linalg.matrix_rank(grid))
inn = out = 64
for r in (1, 4, 8):
    patch = r * inn + out * r
    print(f"r = {r}:  {patch} numbers instead of {inn * out}  ({patch / (inn * out):.3f} of the projection)")
```
```text
[[ 2  1  0  3]
 [ 4  2  0  6]
 [ 0  0  0  0]
 [-2 -1  0 -3]]
16 cells from 4 + 4 = 8 numbers; rank: 1
r = 1:  128 numbers instead of 4096  (0.031 of the projection)
r = 4:  512 numbers instead of 4096  (0.125 of the projection)
r = 8:  1024 numbers instead of 4096  (0.250 of the projection)
```

(`matrix_rank` is teacher-only; the student sees that every row is a multiple of one row.) The
percentage for the whole model belongs to **one model and one choice of `r`**; Week 31 computes it
for the student's own (`1.92%`).

## 3.12 — Week 32: Brier and the calibration gap

How far a stated confidence is from how often it came true. These ten results are **invented** by
the Week 32 author (every fourth row of a 40-row sheet); they are not measured from any model:

```python
import numpy as np
ten = [("greeting", .97, 1), ("greeting", .91, 1), ("refund", .93, 1), ("refund", .72, 0),
       ("technical", .81, 1), ("technical", .63, 0), ("billing", .96, 0), ("billing", .87, 1),
       ("out_of_scope", .91, 1), ("out_of_scope", .69, 0)]
p = np.array([r[1] for r in ten]); y = np.array([r[2] for r in ten], dtype=float)
print("Brier (mean squared gap):", round(float(np.mean((p - y) ** 2)), 4))
print("one sure-and-wrong costs", round((0.96 - 0) ** 2, 4), "; one sure-and-right costs", round((0.97 - 1) ** 2, 4))
hi = p >= 0.8
gap_hi = abs(p[hi].mean() - y[hi].mean()); gap_lo = abs(p[~hi].mean() - y[~hi].mean())
print("sure   n", hi.sum(), " stated", round(float(p[hi].mean()), 4), " actual", round(float(y[hi].mean()), 4))
print("unsure n", (~hi).sum(), " stated", round(float(p[~hi].mean()), 2), " actual", float(y[~hi].mean()))
print("ECE on these ten, two buckets:", round(float(hi.mean() * gap_hi + (~hi).mean() * gap_lo), 4))
```
```text
Brier (mean squared gap): 0.2388
one sure-and-wrong costs 0.9216 ; one sure-and-right costs 0.0009
sure   n 7  stated 0.9086  actual 0.8571
unsure n 3  stated 0.68  actual 0.0
ECE on these ten, two buckets: 0.24
```

ECE depends on the buckets and on which results you look at: Week 32 shows four different ECEs from
the four "every fourth row" sets of ten. **Ten results are for learning the arithmetic, not for
believing the answer.**

## 3.13 — Week 33: the binomial standard deviation ("how wobbly is a count")

A count of weighted coin flips wobbles by about `sqrt(n p (1 - p))`. Week 33 measures it on the toy
agent; this is the same arithmetic on a plain seeded coin, so you can see the idea without the agent:

```python
import numpy as np
rng = np.random.default_rng(0)
n, p = 20, 0.3
print("expected count", n * p, "  wobble sqrt(n p (1-p)) =", round(float(np.sqrt(n * p * (1 - p))), 2))
counts = (rng.random((200, n)) < p).sum(axis=1)          # 200 batches of 20 flips
print("first ten batches:", counts[:10].tolist())
print("smallest / largest in 200:", counts.min(), "/", counts.max())
print("mean", round(float(counts.mean()), 2), " measured wobble", round(float(counts.std()), 2))
w = np.sqrt(n * p * (1 - p))
print("within one wobble of 6:", np.mean(np.abs(counts - 6) <= w).round(2),
      "  within two:", np.mean(np.abs(counts - 6) <= 2 * w).round(2))
print("batches of 20 showing 9 or more:", int((counts >= 9).sum()), " | 3 or fewer:", int((counts <= 3).sum()))
```
```text
expected count 6.0   wobble sqrt(n p (1-p)) = 2.05
first ten batches: [7, 3, 7, 5, 3, 7, 6, 7, 2, 6]
smallest / largest in 200: 0 / 11
mean 5.99  measured wobble 1.96
within one wobble of 6: 0.78   within two: 0.98
batches of 20 showing 9 or more: 25  | 3 or fewer: 18
```

**This is the moment the formula stops being an incantation.** The identical coin gives counts from
2 to 7 in one line of ten. Week 33's agent gives `1` to `13` in 200 batches with a measured wobble of
`2.03` (formula `2.05`); the coin here gives its own numbers (above), and the shape is the same. The
consequence is the sentence to repeat: **twenty runs cannot see a small improvement.**

**Do not say** "68-95-99.7", "normal distribution", "standard error" or "confidence interval". Say:
*about four in five land within one wobble, nearly all within two.*

## 3.14 — And what is deliberately not here

So you can say "not yet" with confidence: **proofs of any kind; limits; the chain rule written as
symbols; the backward pass of attention by hand** (the forward pass is by hand; backward is checked
against autograd only); **the Jacobian** (the per-step factor is the *measured* slope of `tanh` times
a weight); **information theory beyond cross-entropy and one KL; statistics beyond mean, SD, kappa,
the calibration gap and one binomial SD; the PPO objective** (described, never derived or run).

---
---

# 🐍 Section 4 — The Python That Is New in Kind

Everything in the Level 3 syntax ladder is assumed. The [course README](../README.md#-the-syntax-ladder)
lists every new construct by week (never more than four a week). Most are one-liners you can read
cold. **Five of them are new in kind**, meaning they change how the student *thinks about a
program*, not just what they can type. Read these five; the rest you can take from the week file.

## 4.1 — The star in a signature (Week 1)

`def run(tag, *, lr, ...)` means: everything after the `*` must be passed **by name**. It exists so a
sweep can never pass `lr` where `batch_size` was meant. The student's first deliberate error is
breaking it:

```python
def run(tag, *, lr=0.003, batch_size=64):
    return f"{tag}: lr={lr} batch_size={batch_size}"

print(run("ok", lr=0.01))
print(run("oops", 64, 0.01))
```
```text
ok: lr=0.01 batch_size=64
Traceback (most recent call last):
  File "block.py", line 5, in <module>
    print(run("oops", 64, 0.01))
TypeError: run() takes 1 positional argument but 3 were given
```

The error says "takes 1 positional argument but 3 were given". That reads like a complaint about
the *count*, and the student will count their arguments. Teach the cure, not the message: **read the
signature; is there a star?**

## 4.2 — `lambda` and a schedule (Week 4)

A function written in one line, used because `LambdaLR` wants *a function of the step* that returns a
multiplier on the base learning rate.

```python
import math, torch
w = torch.nn.Parameter(torch.zeros(1))
opt = torch.optim.SGD([w], lr=0.1)
cosine = lambda step: 0.5 * (1 + math.cos(math.pi * step / 10))
sched = torch.optim.lr_scheduler.LambdaLR(opt, cosine)
for step in range(11):
    if step in (0, 5, 10):
        print(f"step {step:>2}   lr {sched.get_last_lr()[0]:.4f}")
    opt.step()
    sched.step()
```
```text
step  0   lr 0.1000
step  5   lr 0.0500
step 10   lr 0.0000
```

The order matters: `opt.step()` first, then `sched.step()`. The week also computes the same curve
with plain numpy and checks it against this, which is the real lesson: **the scheduler is a function
you could have written.**

## 4.3 — Classes that are not networks (Week 23)

Until Week 23 every class the student has seen was an `nn.Module` with `forward`. The harness needs
plain objects with *state*: a `@dataclass` (named fields), a class with `__init__` (a budget that
remembers what it has spent), and a custom error that the loop can catch **by name**:

```python
from dataclasses import dataclass

@dataclass
class Case:
    text: str
    gold: str

class BudgetExceeded(Exception):
    pass

class BudgetGuard:
    def __init__(self, limit):
        self.limit = limit
        self.spent = 0.0            # state lives on self
    def charge(self, cost):
        self.spent += cost
        if self.spent > self.limit:
            raise BudgetExceeded(f"spent {self.spent:.2f} of {self.limit:.2f}")

print(Case("I was charged twice", "billing"))
guard = BudgetGuard(limit=0.25)
for call in range(1, 5):
    try:
        guard.charge(0.10)
        print("call", call, "ok, spent", round(guard.spent, 2))
    except BudgetExceeded as err:
        print("call", call, "STOPPED:", err)
        break
```
```text
Case(text='I was charged twice', gold='billing')
call 1 ok, spent 0.1
call 2 ok, spent 0.2
call 3 STOPPED: spent 0.30 of 0.25
```

Notice that the third call has **already been charged** (`0.30`) before the guard stops it: a guard
that checks after spending trips one call late, and Week 23 asks the student to say why.
Two habits to teach here: **catch the error you expect, by name** (a bare `except Exception` hides a
budget alarm; §8, error 13) and **`self.spent`, not `spent`** (forgetting `self.` is the commonest
loud error of the week).

## 4.4 — Modules inside modules (Weeks 16-17)

A GPT is a tree: `TinyGPT` holds four `Block`s, each holds its own layers. Three things make the tree
work, and each has a silent failure:

```python
import torch, torch.nn as nn

class Block(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.ln = nn.LayerNorm(d)
        self.ff = nn.Linear(d, d)
        self.register_buffer("mask", torch.tril(torch.ones(3, 3)))   # moves with the model, not trained
    def forward(self, x):
        return x + self.ff(self.ln(x))

class Net(nn.Module):
    def __init__(self, d, n):
        super().__init__()
        self.blocks = nn.ModuleList([Block(d) for _ in range(n)])      # a plain list would hide them
    def forward(self, x):
        for b in self.blocks:
            x = b(x)
        return x

net = Net(d=8, n=4)
print("children:", [name for name, _ in net.named_children()])
print("parameters:", sum(p.numel() for p in net.parameters()), "  (4 x (8*8+8 + 2*8) = 4 x 88)")
print("mask in state_dict:", "blocks.0.mask" in net.state_dict(), "| mask among the trained parameters:", "blocks.0.mask" in [n for n, _ in net.named_parameters()])
```
```text
children: ['blocks']
parameters: 352   (4 x (8*8+8 + 2*8) = 4 x 88)
mask in state_dict: True | mask among the trained parameters: False
```

Week 17's first-loss check (`ln 28`) and its parameter count by hand are what let the student trust
this tree. **Count the knobs by hand before you train**; it is the quickest way to catch a block that
was built but never registered.

## 4.5 — The trailing underscore (Weeks 11, 31)

A method ending in `_` changes the object **in place** and returns nothing new: `fill_`,
`requires_grad_`, `nn.init.zeros_`. It is how the student freezes a base model and starts a LoRA
patch at exactly "no change".

```python
import torch, torch.nn as nn
layer = nn.Linear(4, 4)
print("trainable before:", sum(p.numel() for p in layer.parameters() if p.requires_grad))
layer.requires_grad_(False)
print("trainable after :", sum(p.numel() for p in layer.parameters() if p.requires_grad))
nn.init.zeros_(layer.bias)
print("bias:", layer.bias.tolist())
```
```text
trainable before: 20
trainable after : 0
bias: [0.0, 0.0, 0.0, 0.0]
```

## 4.6 — The rest, in one line each

| You will see | It is | The one thing to say |
|---|---|---|
| `@torch.no_grad()` above a `def` (Week 17) | A decorator | "Used, not written. It means *do not record gradients inside this function*." Writing decorators is out of scope all year |
| `tokenizers` `BpeTrainer` (Week 20) | A library already installed | "Trains on text you give it. Downloads nothing." If `import tokenizers` fails the week still works; the student's own BPE is the deliverable |
| `ast.parse` plus a whitelist (Week 28) | A calculator that cannot run arbitrary code | The alternative is `eval`, which Week 28's first mistake is |
| `ThreadPoolExecutor` with `future.result(timeout=)` (Week 28) | Run a tool elsewhere and wait a limited time | "So a hung tool cannot hang the agent." Counted as one construct |
| `Path.resolve()` and `is_relative_to` (Week 28) | The sandbox test | Resolve first, compare second (Week 28 mistake 5 is the reverse) |
| `json.dumps` one event per line (Week 29) | JSONL tracing | One pretty JSON document is not JSON Lines (Week 29 mistake 6) |

> **The teaching rule for all of it:** when a new construct appears, the student first *reads* a toy
> that uses it, then types it, then breaks it on purpose. The week files sequence it; your job is to
> not skip the breaking.

---
---

# 🧭 Section 5 — Real, Invented, Stand-In, Quoted

This is the section the Level 3 orientation did not need. Read it slowly.

## 5.1 — The policy, in four sentences

1. **Every model the student trains is real.** TinyGPT, the name generator, the tiny encoder, the
   reward model: real PyTorch, trained on a CPU in front of them, seeded.
2. **Every "model" the student *calls* is a stand-in.** There is no API, no key and no hosted model
   anywhere. Where a lesson needs something to talk to, it talks to a short Python script from the
   shared kit, and that script is labelled in its own output.
3. **A result against a stand-in teaches the scaffolding** (the loop, the contracts, the fences, the
   traces, the shape of the cost) **and nothing about what a real model does.** The kit's own
   docstring says it: *"We model the mechanism, not the rate."*
4. **Where a lesson needs a real learned behaviour** (examples in the prompt helping, showing the
   working helping) **it is re-earned on a model the student trains from scratch** (Week 24), never
   asserted and never scripted.

## 5.2 — Four kinds of number, and the words for each

Every number the student will see this year is exactly one of these. Teach them to ask which.

| Kind | What it is | Examples | The words to use |
|---|---|---|---|
| **Measured** | Printed by code that ran on the student's machine, seeded, today | Every TinyGPT loss; every recall@k; every token count | "I measured that, with seed 0, on these rows." |
| **Invented** | Typed by the course author to have a useful shape | Week 14's word vectors; Week 32's 40 results; Week 33's three planted notes with dummy personal data | "Nobody measured that. We wrote it so you could do the arithmetic." |
| **Stand-in** | Produced by a labelled script that imitates a model | `FakeClient`; `ScriptedModel`; `GullibleModel`; `ExtractiveGenerator`; Week 30's mystery judge | "**This is a stand-in, not a model.** The rate is a property of a number somebody typed." |
| **Quoted** | A literature figure the course does not reproduce | GPT-2's 124M parameters; Chinchilla's 20 tokens per parameter; "4.5 bytes per token"; "ResNet-152 wins" | "Quoted, not reproduced here." Never an exercise, never an answer |

> **The test you can run on any sentence the student writes:** *which of the four is that number?*
> If they cannot say, they have found a hole in the lesson, and it is worth more than the number.

## 5.3 — The label, and the ritual

The kit builds the label into the objects, so nobody can forget it: it appears in `repr(client)`,
in `repr(response)`, in `response.metadata["label"]` and in every `usage_log` row.

```python
from l4lib.fakellm import FakeClient
client = FakeClient(seed=0)
print(repr(client))
reply = client.messages.create(
    model="fake-small", max_tokens=80,
    system="Extract fields as JSON. Rules: category is one of billing, shipping, technical, account, other.",
    messages=[{"role": "user", "content": "<message>\nI was charged twice for order A-1234\n</message>"}])
print(repr(reply))
print(reply.metadata["label"], "|", reply.metadata["price_table"])
```
```text
<FakeClient [stand-in, not a model] seed=0 calls=0>
<Response [stand-in, not a model] stop=end_turn Usage(input_tokens=31, output_tokens=11, cache_read_input_tokens=0) cost=$0.000086>
stand-in, not a model | illustrative
```

**The ritual** (course rule 7), every week that uses a scripted backend:

1. **You** say it first, at the top of the lesson, before any code runs: *"Today's backend is a
   stand-in for a model, not a model."*
2. **The student** says it aloud before their first run.
3. **Whenever a number is quoted,** they add which kind it is. ("17 of 25, *against the stand-in*.")
4. **In every written report** the label is in the first lines and again beside any rate.

It feels like ceremony in Week 23. By Week 33 it is a reflex, and the reflex is the point: it is the
habit of saying *what the evidence is evidence of.*

### What "stand-in" really means: a look inside

A stand-in does not read English. Week 23's `FakeClient` looks for a handful of word-stems. Watch it
"understand" a sentence that says the opposite:

```python
import json
from l4lib.fakellm import FakeClient
SYSTEM = "Extract fields as JSON. Rules: category is one of billing, shipping, technical, account, other."
def category(message):
    c = FakeClient(seed=0)
    r = c.messages.create(model="fake-small", max_tokens=80, system=SYSTEM,
                          messages=[{"role": "user", "content": "<message>\n" + message + "\n</message>"}])
    return json.loads(r.content[0].text)["category"]

for m in ["I was charged twice for order A-1234, give me my money back",
          "Thanks! I was never charged twice for order A-1234 and I love it.",
          "Where is my package? Order B-77 has not arrived in 9 days",
          "The weather is lovely today"]:
    print(f"{category(m):<9} <- {m}")
```
```text
billing   <- I was charged twice for order A-1234, give me my money back
billing   <- Thanks! I was never charged twice for order A-1234 and I love it.
shipping  <- Where is my package? Order B-77 has not arrived in 9 days
billing   <- The weather is lovely today
```

Read the second line aloud with the student. *"Never charged"* gets the same category as *"charged
twice"*, and a sentence about the weather is filed under `billing` because that is the default. That
is not the stand-in failing; **that is the stand-in working as designed**, and it is why every
accuracy against it is a statement about regular expressions. A real model would do differently,
better in some ways and worse in others, and this course deliberately does not say which.

## 5.4 — Which weeks have what

The *ran-on-a-real-trained-model* weeks and the *stand-in* weeks, so you know in advance:

| Weeks | Status |
|---|---|
| 1-22 | **All real.** Every model trained by the student; invented numbers appear only in hand arithmetic (Week 14's word vectors, Week 22's random scores for nine positions and its ten typed preferences) |
| 23 | **First stand-in:** `FakeClient` is the backend of the prompt harness. The scorer, parser, floor and budget guard are real code |
| 24 | **Real, from scratch:** three small transformers trained in class. `FakeClient` appears once, in a 10-second cache-key demo, and no number comes from it |
| 25 | **Real:** char n-grams plus SVD, and a contrastive embedder trained for 150 steps. No stand-in. A pretrained encoder is **not** present, and the reference module's `0.62` is not reproduced |
| 26 | **Stand-in:** `ExtractiveGenerator` (copies the one best-matching sentence and appends its id). The index, recall@k and threshold sweep are real |
| 28 | **Stand-in:** `ScriptedModel` replays a typed plan. The loop, fences, trace and token counts are real as code |
| 29 | **Stand-in:** `GullibleModel` obeys a `call tool(key="value")` sentence with a typed probability. The three defence layers are real as code; the obey rates are not evidence about any real model |
| 30 | **Stand-in:** the mystery judge, which reads a rubric score (not language) and has a planted bias. The eval set (typed), the scorer and the fingerprint are real engineering |
| 31 | **Real:** a tiny encoder pretrained and fine-tuned on CPU. Its pretraining text is itself "a stand-in for lots of text": 5,672 generated sentences, only 1,480 distinct, which flatters the model (the week says so) |
| 32 | **Invented data:** the 40 results. Brier, ECE and the curves are real arithmetic on them |
| 33 | **Stand-in and invented:** `GullibleModel` and three planted notes with dummy personal data. The redactor, the retention sweep and the wobble arithmetic are real code |
| 34-36 | Mixed, and labelled in the capstone's own card: the real parts are the harness, the fences, the frozen eval and the committed numbers; the stand-in parts are the generator and the agent's plan. **All dollars and milliseconds are stand-in dollars and stand-in milliseconds** (Week 36) |

One small inconsistency you may notice: the Week 36 guide calls the extractive generator "Week 25's",
while Week 25 says it first appears in Week 26 (Week 26 is right). It changes no lesson.

## 5.5 — The twelve sentences you must not say

Each is a sentence an enthusiastic adult says, and each is false or unsupported. The right-hand
column is what to say.

| ❌ Do not say | ✅ Say |
|---|---|
| "The model obeyed the injection 15 times in 50." | "The **stand-in** obeyed a planted sentence 15 times in 50. Its obey rate is a number we typed (`0.3`)." |
| "RAG fails at multi-hop questions." | "Our copy-one-sentence writer scores 0 of 4 on multi-hop. One sentence cannot hold two facts. A different writer would do differently." (Week 35) |
| "RNNs cannot learn long-range dependencies." | "At the start, the signal from position 1 is tiny. A trained cell can still learn it; Week 10's teacher check trains one and it got `T = 40` right on 4 seeds of 5." |
| "Adam is better than SGD." | "At this learning rate, on this network, in this run." |
| "Layer norm hurts / helps." | "In Week 19's small model, at 800 steps, removing it made validation loss better. That is one small model." |
| "The scaling law says ..." | "Our four points lie near a line of slope `-0.126`. The published laws are quoted, not reproduced." |
| "This proves the attention head does X." | "Here is the name I gave it, and here is the evidence that would prove the name wrong." (Week 19) |
| "The DPO/SFT/reward model learned the human's values." | "On ten typed preferences the reward model found a feature; it also rewarded a feature it should not have." (Week 22) |
| "Fine-tuning works / LoRA matches full fine-tuning." | "`19/30` and `19/30` on seed 0; over six seeds `18.5` and `19.0`; the spread between seeds is about two tickets, so I cannot rank them." (Week 31) |
| "The system is 70% accurate." | "17 of 25, on these 25 frozen cases, against these scripted parts." (Week 36's card wants a number and an *n*, never a bare percentage) |
| "Zero of 50 attacks succeeded, so it is impossible." | "0 of 50 with a wobble near zero says *this attack, this fix*; it says nothing about other attacks." (Week 33) |
| "Pretraining understood language." | "The tiny model learned which words appear in the same templates." (Week 31) |

## 5.6 — "But would a real model do that?"

A sharp student will ask it, probably in Week 23, probably politely. The honest answer has three
parts, and you may say all three:

> *"I don't know, and we can't find out on this laptop. What we **can** test is the machinery around
> a model: whether the test set is frozen, whether the parse is strict, whether the fence fires. Those
> are properties of code, and they would be the same if the model behind them were real. The rates
> are not. If you ever get to a real model, the harness you built is what you would run it through.
> That is the point of building the harness first."*

Then, if they are keen: the optional **💡 When you have internet** callouts (at most one per week, for example Weeks 20, 23, 25, 28, 30 and 33) keep the original reference-module code for a
student who can use it. **No exercise, workbook answer or assessment depends on any of them.** A
student who never once has internet finishes the level having missed nothing that is assessed.

## 5.7 — The shared kit, in one table

The source files in `l4lib/`, written and unit-tested once, that every week imports. **The student
imports them; nobody copies them, including you.** To see what is inside: `grep -n "def \|class "
l4lib/<file>.py`.

| File | What it is | Weeks |
|---|---|---|
| `spirals.py` | `make_spirals`, `get_data`, `make_model`, and the `run(*, lr, ...)` harness (CPU-pinned; `depth` is an argument) | 1-7, 19 |
| `names.py`, `corpus.py` | The 231 typed names; the 6,972-character TinyGPT corpus (28 distinct characters) | 8-19 |
| `tinytok.py` | Local token counter: the student's own BPE from Week 20, falling back to `len(text.split()) * 1.3`. **Never `tiktoken.get_encoding`** (it downloads its ranks) | 20, 23-36 |
| `fakellm.py` | `FakeClient` with the chat-API *surface* (`messages.create`, `.content[0].text`, `.stop_reason`, `.usage`); seeded error rates; `max_tokens` truncation; `stop_sequences`; prefix-cache accounting; injectable `RateLimit` / `BadRequest` faults; an **illustrative** `PRICE_TABLE` | 23-36 |
| `rag.py` | `TinyDenseEmbedder`, `VectorIndex`, chunkers, the 15-note notebook, the extractive generator with `cite_wrong_id` / `no_citation` / `ignore_sources` fault switches | 25-26, 28-29, 33-36 |
| `toyagent.py` | `run_agent`, `ScriptedModel`, `GullibleModel`, `FlakyBackend`, the tool registry and the sandbox | 28-29, 33-36 |

The kit ships with six test files (`l4lib/tests/`). You will run them in §7; they take about six
seconds together, and they are the fastest way to find out that a laptop is not what you think it is.

---
---

# 🕐 Section 6 — How a Lesson Runs, and How the Year Paces

## 6.1 — The 70-minute shape

Every teach, lab and project week has the same five parts. The minutes shift a little from week to
week; the order never does.

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │  ⏱️  THE 70-MINUTE LESSON                                                 │
   ├───────────────┬──────────────────────┬───────────────────────────────────┤
   │  about        │  part                │  what happens                     │
   ├───────────────┼──────────────────────┼───────────────────────────────────┤
   │  6-7 min      │  🪝 HOOK             │  A real, measured number on the    │
   │               │                      │  board or screen. A question you   │
   │               │                      │  do not answer yet. No new word.   │
   ├───────────────┼──────────────────────┼───────────────────────────────────┤
   │  12-18 min    │  🧠 CONCEPT          │  Pencils. The week's hand          │
   │               │  (or Concept & Maths)│  arithmetic, on three to five real │
   │               │                      │  numbers. On a maths week the new  │
   │               │                      │  word is said only after the sums. │
   │               │                      │  Predictions written BEFORE code.  │
   ├───────────────┼──────────────────────┼───────────────────────────────────┤
   │  22-26 min    │  💻 LIVE-CODE        │  You type, they type, same file.   │
   │               │  TOGETHER            │  Nobody pastes. The code CHECKS    │
   │               │                      │  the arithmetic. Deliberate        │
   │               │                      │  mistakes happen here, with the    │
   │               │                      │  traceback read aloud.             │
   ├───────────────┼──────────────────────┼───────────────────────────────────┤
   │  14-25 min    │  🎲 THEIR TURN       │  They build, label, or break it    │
   │               │                      │  alone. You sit on your hands.     │
   ├───────────────┼──────────────────────┼───────────────────────────────────┤
   │  5-7 min      │  🔑 WRAP & ASSIGN    │  Three takeaways, said by THEM.    │
   │               │                      │  Homework read aloud. Bug Log.     │
   └───────────────┴──────────────────────┴───────────────────────────────────┘
```

Three real weeks, so you can see how much the parts move:

| Week | Hook | Concept | Live-code | Their turn | Wrap | Total |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 (One Loop, Ten Knobs) | 7 | 18 | 22 | 16 | 7 | 70 |
| 2 (Momentum) | 7 | 17 | 26 | 14 | 6 | 70 |
| 23 (The Harness) | 6 | 12 | 22 | 25 | 5 | 70 |

Each teacher file also has: a **Prep Checklist** (the blocks to run the night before, with the real
output to compare against, and a paper-only fallback if the laptop dies), **🐞 The Debugging Clinic**
(the week's deliberate mistakes), **❓ Questions Students Ask This Week**, **⚠️ Where This Lesson Goes
Wrong**, **🧭 Differentiation**, **✅ Assessing Understanding** (a mastery scale), **📤 Homework**, a
**🔑 Answer Key**, and **🔮 Next Week Preview**. On a 70-minute clock you will use the first and
last of those two or three times each; the rest is for when something goes sideways.

## 6.2 — The four rituals that make a Level 4 lesson work

1. **Pencils before keyboards.** Every week has a by-hand step (a table of three optimizer steps, a
   three-token attention pass, a kappa on 20 ratings). Paper first, code second; the code's job is to
   agree with the paper. On the 13 maths weeks this is the lesson.
2. **Predict before you run.** A sentence or a sketch in writing, before the code: six index cards
   labelled A-F in Week 1, a guess at `0.95^40` in Week 10, "what will temperature 0.3, 1 and 2 do to five letters?" in Week 13. The gap between prediction and result is the thing they learn from, and nobody can feel it if
   the prediction was not committed.
3. **Name the evidence.** Every number spoken aloud carries four tags: *which rows, how many, which
   seed, which kind* (§5.2). *"0.693 on the 360 validation points, seed 0, measured."* Model this from
   Week 1.
4. **The Bug Log entry, before the fix is forgotten.** Real message, what it meant in their words,
   the fix. Ninety seconds, every week. It compounds: by June it is thirty pages, and the capstone
   leans on it.

## 6.3 — Runs that take time

Most weeks nothing runs longer than about ten seconds. These are the exceptions. The times are the
week files' measurements (an 18-core Mac, one thread); **your laptop will differ, and that is fine.**

| Week | What runs | About | What you do |
|:--:|---|---|---|
| 12 | Train the name model | 25 s | Start it, then talk about `ignore_index` |
| 13 | The copy-task delay sweep at the stated CPU-sized defaults (homework) | 40 s | Set it running and do something else |
| 17 | `train.py`, the TinyGPT (53 ms per step) | 80-95 s | Start it as the student finishes typing; **do not** fill the silence |
| 19 | Five ablation models at the stated reduced step count | 3.5 min | Start it early in the live-code segment; use the gap for the hand table |
| 21 | Two width-sweep runs of about 90 s each (your prep: about 5 minutes) | 2 x 90 s | Run them while you talk; the week file says where |
| 24 | Three small transformers: 103 s, 105 s and 30 s | about 4 min | Start before the lesson; the logit mask can be homework |

A few rules for all of them:

- **Start the long run first, talk second.** The 85 seconds of silence while TinyGPT trains is
  exactly the right time for the question *"what do you think the loss will be before step 1?"*.
- **Never shorten a run silently.** The week files state a *reduced default* (W17, W19, W24) and an
  optional "full" setting. Use the stated default. If a laptop is far slower, lower `steps` by a
  **stated** amount and write the new number in the Bug Log; do not change the seed.
- **Never skip the seed.** A number you cannot reproduce is not a result, and rule 6 forbids writing
  one in a report.
- **A slower CPU moves times, not shapes.** If a run is twice as slow, the lesson is the same; if the
  *digits* differ by one in the third decimal, see §7.5.

## 6.4 — The weeks that are not 70 minutes

| Weeks | What is different |
|:--:|---|
| **9, 18, 27** | **Assessments.** 75 minutes: 2 to settle, 70 for the paper, 3 to hand in. **No computer.** Twenty multiple choice, 8 "what does this print" (2 marks each), 4 "find the bug" (3 each), 3 "do the arithmetic" (5 each), and one 12-mark section reading real tables: **75 marks** (Week 9's sections are 20 + 16 + 12 + 15 + 12). Then about 45 minutes of *marking homework*: the student marks their own paper against the key and fills a per-week remediation table. The paper is an **X-ray, not a grade**; your job for 70 minutes is to be a quiet adult in a chair. A frown at question 7 changes a right answer |
| **34** | 70 in class, then about 90 minutes at home. The design doc, 25 frozen cases with a committed fingerprint, and a budget. **Nothing in `src/` may exist yet** (Week 34's clinic D8 is the guard firing when a student starts coding first) |
| **35** | 70 in class, then about **150 minutes at home**: allow three sittings, and tell the student on the Monday, not the Thursday |
| **36** | **Two sittings on different days.** Sitting 1 (70 min, with the computer): demo and system card. Sitting 2 (75 min, no computer): Assessment 4, at least a day after the demo, so nobody sits a paper straight after being questioned about their own system. Never squeeze the paper into the end of Sitting 1 |

## 6.5 — Squeezing into 60, stretching to 75

**Squeezing.** Cut in this order: the workbook-style extension in the Activity, then minutes from
*Their Turn*, then the second half of live-code (set it as a take-home). **Never cut:** the hand
arithmetic, the seed, the label on a stand-in, or the deliberate mistake. The arithmetic is the
lesson, the seed is reproducibility, the label is honesty, and the mistake is where debugging
confidence comes from.

**Stretching.** Use the *If the student is flying* variation in the week file, or make them explain
the maths back while you write down what they say. That transcript is the best assessment evidence
you will get.

**Three weeks that may honestly take two sittings:** 22, 24, 33. Their week files say where to split.

## 6.6 — Order, and what you may not reorder

The maths and syntax ladders mean a week may use only what earlier weeks taught. So:

- **You may stretch a week into two sittings. You may not swap two weeks.** Week 14 (attention by
  hand) must come before Week 15 (scale and mask); Week 20's BPE before Week 21's pretraining; Week 30's
  frozen eval before Week 31's fine-tune and Week 34's capstone.
- The only weeks with no new content are **9, 18 and 27**. If you must lose time, those are the only
  three that can be shortened, and only by moving the paper to a home sitting. (That is a judgement
  call for you, not something the course prescribes; the paper loses its "quiet adult in a chair" and
  you should say so in the marking notes.)
- If the student is a week or two behind, **do not drop a lab**. Labs (5, 10, 12, 17, 19, 20, 24,
  26, 29, 31, 33) are where the measured numbers come from, and a later week quotes them.

## 6.7 — Six rules of thumb that work every week

- If they are quiet and typing, **say nothing.**
- If they are quiet and *not* typing, ask *"what does the last line say?"*
- If they are frustrated, go back to **three numbers on paper.**
- If they finish early, ask them to break it and predict what breaks.
- If *you* are lost, say *"I don't know. Let's measure it."* and nudge something.
- If the arithmetic and the code disagree, **stop everything.** That disagreement is the most valuable
  event of the week, and it is instructive whichever one turns out to be wrong.

---
---

# 🔧 Section 7 — Setup: Do This Alone, Before Week 1

**Level 4 installs nothing new.** Level 3's five libraries (`numpy`, `pandas`, `matplotlib`,
`scikit-learn`, `torch`) are the whole stack. `tokenizers` is already present and is used in one week
(and if `import tokenizers` fails, Week 20 still works: the student's own BPE is the deliverable).
About 25 minutes, with nobody watching.

## 7.1 — The right folder

Open a terminal **in the `36-week-course/` folder**: the folder that *contains* `l4lib/`, not the
folder inside it. Every import this year is `from l4lib... import ...`, so this is the single commonest
error of Week 1 (§8, error 1). `ls` should show `l4lib`, `README.md`, `teacher-guide`, `student-guide`
and `workbook`.

## 7.2 — The smoke test

```python
import numpy, pandas, matplotlib, sklearn, torch
print("numpy", numpy.__version__, "| sklearn", sklearn.__version__, "| torch", torch.__version__)
try:
    import tokenizers
    print("tokenizers", tokenizers.__version__, "(needed only in Week 20)")
except ImportError:
    print("tokenizers missing: Week 20 still works with the student's own BPE")
try:
    import torchvision
    print("torchvision present (unused, and nothing may depend on it)")
except ImportError:
    print("torchvision absent, as expected")
```
```text
numpy 1.26.4 | sklearn 1.7.1 | torch 2.2.1
tokenizers 0.21.1 (needed only in Week 20)
torchvision absent, as expected
```

Any `2.x` torch is fine; the guides were run on `2.2.1`. **If a `pip` command returns 403** at any
point this year, that is the corporate proxy and it is **not an error**: nothing needs installing;
close the terminal and carry on.

## 7.3 — The kit self-test (the one that catches a surprising laptop)

The shared kit ships with plain-assert tests. Run them from the `l4lib/` folder; each prints a
closing line, and together they take about six seconds:

```bash
for t in tests/test_fakellm.py tests/test_names_corpus.py tests/test_rag.py tests/test_spirals.py tests/test_tinytok.py tests/test_toyagent.py; do
  python3 $t 2>&1 | tail -1
done
```
```text
12 tests passed
names/corpus: all 4 tests passed
13 tests passed
spirals: all 7 tests passed
tinytok: all 10 tests passed
19 tests passed
```

Six closing lines, no traceback. If one fails, **do not debug the kit**: note which test, reinstall
nothing, and ask the course owner; the week files assume the kit is correct. (These are the owner's
tests, not the student's; they never see them.)

## 7.4 — The data fingerprint

Week 1's first block, run now, so you know what "right" looks like. **If any of these differ, stop:**
the generator or the seed has changed and every other number in the year will be wrong.

```python
import torch
torch.set_num_threads(1)
from l4lib.spirals import make_spirals, get_data
X, y = make_spirals(n=600, noise=0.22, seed=0)
print("X", X.shape, X.dtype, "  y", y.shape, y.dtype, "  first x-coordinate", round(float(X[0, 0]), 3))
Xtr, ytr, Xva, yva = get_data()
print("train", tuple(Xtr.shape), " val", tuple(Xva.shape))
print("train class counts:", ytr.bincount().tolist(), "  val class counts:", yva.bincount().tolist())
```
```text
X (1200, 2) float32   y (1200,) int64   first x-coordinate 2.734
train (840, 2)  val (360, 2)
train class counts: [431, 409]   val class counts: [169, 191]
```

## 7.5 — Same seed, same digits (and when they will not match)

```python
import torch
torch.set_num_threads(1)
from l4lib.spirals import run
a = run("first ", lr=1e-3, epochs=5)
b = run("second", lr=1e-3, epochs=5)
print("identical training curves:", a["train"] == b["train"])
```
```text
first                        train 0.494  val 0.420  acc  63.1%
second                       train 0.494  val 0.420  acc  63.1%
identical training curves: True
```

This is the reproducibility promise. **Two things to know about the digits in the guides:**

- They repeat exactly on *this* machine, with *CPU*, *one thread* and *PyTorch 2.2.1*. A different
  PyTorch version or CPU can move the **third decimal**. The *shapes* and the *counts* (parameter
  counts, class counts, row sums) will **not** move.
- The tolerance the week files use is **±0.005 on losses and ±0.5 percentage points on accuracy.**
  An exact match is not the test. If a student's digits differ in the third place, say so and
  continue. If they differ in the **first** place, something real is different (the seed, the folder,
  `set_num_threads(1)`), and that is a finding, not noise.

## 7.6 — The timing check

```python
import time, torch
torch.set_num_threads(1)
from l4lib.spirals import run
t = time.time()
for letter, lr in [("A", 1e-6), ("B", 1e-5), ("C", 1e-4), ("D", 1e-3), ("E", 1e-2), ("F", 1e-1)]:
    run(f"{letter}  lr={lr:g}", lr=lr, epochs=60, verbose=False)
print(f"the Week 1 sweep took {time.time() - t:.1f} seconds on this machine")
```
```text
the Week 1 sweep took 2.2 seconds on this machine
```

Week 1's guide measured about **3 seconds** for the six runs. Under about 15 seconds you will not
notice. Over a minute, something is wrong (another process; a laptop in power-saving mode), and the
longest runs of the year (§6.3) will take proportionally longer. Fix it now; do not discover it in
Week 19.

## 7.7 — The things that actually go wrong

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'l4lib'` | Wrong folder | `cd` to the folder that contains `l4lib/` (§8, error 1) |
| `pip` returns 403 | The proxy | Not an error. Close the terminal. Nothing needs installing |
| `import torchvision` fails | It is not installed and cannot be | Expected; nothing may depend on it |
| `import tokenizers` fails | Not installed | Week 20 still works; the student's BPE is the deliverable |
| A number differs in the third decimal | A different PyTorch or CPU | Within tolerance (§7.5); continue |
| A number differs in the first decimal | Seed, folder, or forgotten `set_num_threads(1)` | Find out why **now**; it is a finding |
| A run is far slower than the guide | Power saving; another process; many threads | Plug in; close things; `torch.set_num_threads(1)` |
| A chart window never appears | A headless backend | Save the figure with `fig.savefig("name.png")` and open the file; do not fight the window |
| The student asks to `pip install transformers` or set an API key | Reaching for a download | "It would download. Here is what we use." Then show the week's stand-in |
| A stand-in's result looks "too clean" | It is a script | That is the point. Restate the label aloud |
| The laptop sleeps mid-run | Power settings | Re-run with the same seed; the result is identical |

## 7.8 — The setup completion checklist

```
   ☐  Terminal is in the folder that contains l4lib/
   ☐  Smoke test printed versions (any torch 2.x), torchvision absent
   ☐  All six kit tests printed their closing line
   ☐  Week 1 fingerprint matched (840/360, [431, 409] / [169, 191])
   ☐  Same seed printed "identical training curves: True"
   ☐  Timing check under a minute (ideally under 15 s)
   ☐  A notebook for the Bug Log, and a pen
   ☐  You have read §5 of this file
```

---
---

# 🐞 Section 8 — Reading an Error, and the Sixteen This Level Produces

## 8.0 — The three-step rule, and the Level 4 wrinkle

The Level 3 rule is unchanged: **(1) read the last line, (2) find your own file and line in the
traceback, (3) ask what you expected.** Cheerful, slow, out loud, every time.

The Level 4 wrinkle is that **more than half of this year's mistakes are silent.** (Counting the Clinic headings in the teacher guides that follow the Mistake/Error pattern, 127 of 240 are marked SILENT or QUIET and 87 LOUD; the rest carry no label.) The code runs. A
number appears. It is wrong. Each week's Clinic marks its mistakes *loud* or *SILENT*, and the silent
ones are where the learning is, because the only defence against a silent error is a **check**:

| The check | What it catches | Taught |
|---|---|---|
| First loss is `ln(vocab)` (within 0.05) | A model that is built wrong before it trains | Weeks 1, 17 |
| Softmax rows add to 1 | A softmax over the wrong axis; weights that do not sum to 1 | Weeks 13-15 |
| Count the knobs by hand before training | A layer that was never registered | Weeks 16-17 |
| The constant-answer **floor** | A score that means nothing | Weeks 23, 30 |
| A **fingerprint** of the frozen eval | A test set edited after the fact | Weeks 30, 34 |
| **Mean and spread over three seeds** | One lucky run; a difference inside the noise | Weeks 7, 23, 33 |
| `state_dict` and gradient **shape** prints | A silent reshape or a `batch_first` slip | Weeks 8, 15 |

Teach the check *with* the error. "It ran" is never the end of the sentence.

The sixteen below are not the only errors; they are the **families** you will see most. Each has a
block you can run, and each block's output is real. The week it bites is in the heading.

### Error 1 — The wrong folder *(Week 1; loud; the commonest of the first fortnight)*

```python
from l4lib.spirals import run
```
```text
ModuleNotFoundError: No module named 'l4lib'
```
**Meaning:** Python looked in this folder and there is no `l4lib`. **Fix:** `cd` to the folder that
contains it. **Ask:** *"What does `ls` show?"*

### Error 2 — Positional arguments to a keyword-only function *(Week 1; loud)*

```python
from l4lib.spirals import run
run("A", 1e-3)
```
```text
TypeError: run() takes 1 positional argument but 2 were given
```
**Meaning:** the harness has a `*` in its signature (§4.1), so `lr` must be passed by name. The
message counts arguments, which is the wrong thing to look at. **Fix:** `run("A", lr=1e-3)`.
**Ask:** *"Is there a star in the signature?"*

### Error 3 — Reading a gradient that was removed *(Week 2; loud)*

```python
import torch
w = torch.tensor([1.0], requires_grad=True)
opt = torch.optim.SGD([w], lr=0.1)
(w * w).sum().backward()
opt.zero_grad(set_to_none=True)
print(w.grad.norm())
```
```text
AttributeError: 'NoneType' object has no attribute 'norm'
```
**Meaning:** `set_to_none=True` removes the gradient, so there is nothing to take the length of. That
is the *feature*: a `None` is easier to spot than a stale zero. **Fix:** read the norm *before*
clearing. **Ask:** *"When was this cleared?"*

### Error 4 — `s = BASE` is not a copy *(Week 7; SILENT, and the most instructive)*

```python
BASE = {"lr": 1e-3, "depth": 4}
for lr in [1e-4, 1e-2]:
    s = BASE                      # a second NAME for the same dictionary, not a copy
    s["lr"] = lr
print("BASE after a sweep that never touched BASE:", BASE)
fixed = dict(BASE)                # a real copy
fixed["lr"] = 0.5
print("BASE after editing the copy:", BASE)
```
```text
BASE after a sweep that never touched BASE: {'lr': 0.01, 'depth': 4}
BASE after editing the copy: {'lr': 0.01, 'depth': 4}
```
**Meaning:** every "setting" in the sweep shares one dictionary, so each run inherits the last run's
edits. The sweep table looks fine. **Caught by:** printing the base settings after the sweep.
**Ask:** *"Did BASE change? Should it have?"*

### Error 5 — Forgetting `batch_first=True` *(Week 8; SILENT)*

```python
import torch, torch.nn as nn
torch.manual_seed(0)
x = torch.randn(1, 5, 4)                       # 1 sentence, 5 words, 4 features each
right = nn.RNN(4, 16, batch_first=True)
wrong = nn.RNN(4, 16)                          # forgot batch_first
wrong.load_state_dict(right.state_dict())
out_r, h_r = right(x)
out_w, h_w = wrong(x)
print("final-state shape, right:", tuple(h_r.shape), "  wrong:", tuple(h_w.shape))
print("same numbers:", torch.allclose(out_r, out_w))
```
```text
final-state shape, right: (1, 1, 16)   wrong: (1, 5, 16)
same numbers: False
```
**Meaning:** without `batch_first`, the layer reads the first axis as *time*, so a one-sentence,
five-word batch becomes five one-word sentences. The output has the same shape as the right one, so
nothing complains. **Caught by:** printing the shape of the *final state*. **Ask:** *"What shape is it,
and what should it be?"*

### Error 6 — Word ids with a decimal point *(Weeks 8, 16; loud)*

```python
import torch, torch.nn as nn
table = nn.Embedding(5, 3)
print(table(torch.tensor([0.0, 1.0, 2.0])))
```
```text
RuntimeError: Expected tensor for argument #1 'indices' to have one of the following scalar types: Long, Int; but got torch.FloatTensor instead (while checking arguments for embedding)
```
**Meaning:** an embedding is a lookup by whole-number position; `1.0` is a float. **Fix:**
`torch.tensor([0, 1, 2])`. The Level 3 dtype lesson, in new clothes.

### Error 7 — Calling `backward()` twice *(Week 10; loud)*

```python
import torch
x = torch.tensor(3.0, requires_grad=True)
y = x * x
y.backward()
y.backward()
```
```text
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.
```
**Meaning:** the first `backward()` frees the recorded computation. **Fix:** rebuild the forward pass
before each backward, or (deliberately) `retain_graph=True`. This is Level 3's error 4, met again.

### Error 8 — Softmax over the wrong axis *(Week 13; SILENT)*

```python
import torch, torch.nn.functional as F
torch.manual_seed(0)
scores = torch.randn(3, 4)                      # 3 rows of scores, 4 choices each
right = F.softmax(scores, dim=-1)
wrong = F.softmax(scores, dim=0)
print("row sums, dim=-1:", [round(v, 4) for v in right.sum(dim=1).tolist()])
print("row sums, dim=0 :", [round(v, 4) for v in wrong.sum(dim=1).tolist()])
```
```text
row sums, dim=-1: [1.0, 1.0, 1.0]
row sums, dim=0 : [1.6858, 1.3411, 0.9731]
```
**Meaning:** each *row* must be a probability table. With `dim=0`, each *column* is normalised and the
rows add to anything. **Caught by:** the **row-sums-to-1 check**. Also the error of Week 14 mistake 8
and Week 22 mistake 4. **Ask:** *"Which numbers must add to 1?"*

### Error 9 — Asking for more than there is *(Week 13; loud)*

```python
import torch
print(torch.topk(torch.tensor([0.1, 0.9, 0.5]), k=5))
```
```text
RuntimeError: selected index k out of range
```
**Meaning:** `k` larger than the number of letters. **Fix:** `k = min(k, n)`. Easy, and worth doing
because top-k and top-p are the first places the student writes a *bounds check*.

### Error 10 — Hiding the future with `0`, not `-inf` *(Week 15; SILENT)*

```python
import torch, torch.nn.functional as F
scores = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
allowed = torch.tril(torch.ones(3, 3)).bool()
good = F.softmax(scores.masked_fill(~allowed, float("-inf")), dim=-1)
bad  = F.softmax(scores.masked_fill(~allowed, 0.0), dim=-1)
print("row 0, future hidden with -inf:", [round(v, 4) for v in good[0].tolist()])
print("row 0, future 'hidden' with 0 :", [round(v, 4) for v in bad[0].tolist()])
```
```text
row 0, future hidden with -inf: [1.0, 0.0, 0.0]
row 0, future 'hidden' with 0 : [0.5761, 0.2119, 0.2119]
```
**Meaning:** `exp(0) = 1` is a perfectly ordinary weight, so a score of `0` hides nothing; the first
word is still reading the words after it. **Why it matters:** this is the leak Week 19's ablation
rewards with the best number of the table. **Caught by:** the weights above the diagonal must be
exactly `0`.

### Error 11 — A plain list of layers *(Week 16; SILENT, and the most dangerous of its week)*

```python
import torch.nn as nn
class Bad(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [nn.Linear(4, 4), nn.Linear(4, 4)]            # a plain list
class Good(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([nn.Linear(4, 4), nn.Linear(4, 4)])
print("Bad  parameters:", sum(p.numel() for p in Bad().parameters()))
print("Good parameters:", sum(p.numel() for p in Good().parameters()), " (2 x (4*4 + 4))")
```
```text
Bad  parameters: 0
Good parameters: 40  (2 x (4*4 + 4))
```
**Meaning:** PyTorch cannot see layers hidden inside a plain list, so the optimiser trains **none** of
them, and the model runs and the loss sits still. **Caught by:** counting the knobs by hand before
training. **Ask:** *"How many knobs should it have?"*

### Error 12 — Parsing the whole reply as JSON *(Week 23; loud, then the fix)*

```python
import json, re
reply = 'Sure! Here is the JSON you asked for: {"category": "refund", "urgency": 2}'
try:
    json.loads(reply)
except json.JSONDecodeError as err:
    print("loud:", err)
found = re.search(r"\{.*\}", reply, re.S)
print("fixed:", json.loads(found.group(0)))
```
```text
loud: Expecting value: line 1 column 1 (char 0)
fixed: {'category': 'refund', 'urgency': 2}
```
**Meaning:** a reply with chatty words round the JSON is not JSON. **Fix:** find the braces first.
Note that `re.S` (so the dot crosses line breaks) is the Week 23 construct whose *absence* is a quiet
error: the parse works on a one-line reply and fails on a multi-line one.

### Error 13 — The catch-all that swallows the alarm *(Week 23; SILENT)*

```python
class BudgetExceeded(Exception):
    pass

def call(spent):
    if spent > 1.0:
        raise BudgetExceeded("over budget")
    return "answer"

def careless(spent):
    try:
        return call(spent)
    except Exception:                 # catches EVERYTHING, including the alarm
        return "answer"

print("careless, under budget:", careless(0.5))
print("careless, over budget :", careless(5.0), "   <- the alarm never rang")
try:
    call(5.0)
except BudgetExceeded as err:
    print("careful,  over budget : STOPPED:", err)
```
```text
careless, under budget: answer
careless, over budget : answer    <- the alarm never rang
careful,  over budget : STOPPED: over budget
```
**Meaning:** a guard you cannot hear is not a guard. **Fix:** catch the error you expect, **by name**.

### Error 14 — `argsort` without the minus *(Week 26; SILENT)*

```python
import numpy as np
scores = np.array([0.10, 0.90, 0.40])
print("top-1 with argsort(s)[:1]  :", np.argsort(scores)[:1].tolist(), "  <- the WORST score")
print("top-1 with argsort(-s)[:1] :", np.argsort(-scores)[:1].tolist())
```
```text
top-1 with argsort(s)[:1]  : [0]   <- the WORST score
top-1 with argsort(-s)[:1] : [1]
```
**Meaning:** `argsort` sorts ascending, so the first entries are the *lowest*. The retriever happily
returns the least relevant note, and a wrong-looking answer is blamed on the generator.
**Caught by:** reading the retrieved chunks (the Week 26 diagnosis: *retrieval or generation?*).

### Error 15 — One run, and a conclusion *(Weeks 7, 23, 25, 33; SILENT, the code is right)*

```python
import numpy as np
A = [int((np.random.default_rng(s).random(20) < 0.3).sum()) for s in range(5)]
B = [int((np.random.default_rng(100 + s).random(20) < 0.3).sum()) for s in range(5)]
print("system A, 5 seeds of 20 runs:", A)
print("system B, 5 seeds of 20 runs:", B)
print("fewer is better: A looks better on", sum(a < b for a, b in zip(A, B)), "seeds, B looks better on", sum(b < a for a, b in zip(A, B)), "; the two systems are identical")
```
```text
system A, 5 seeds of 20 runs: [7, 5, 8, 7, 3]
system B, 5 seeds of 20 runs: [4, 3, 5, 7, 5]
fewer is better: A looks better on 1 seeds, B looks better on 3 ; the two systems are identical
```
**Meaning:** identical systems produce different counts, and any single pair can be read as a winner.
**Caught by:** mean and spread over seeds (Week 7) and the wobble `sqrt(n p (1 - p))` (Week 33).
**Ask:** *"How much does that number move if I change the seed?"*

### Error 16 — The frozen eval, edited *(Weeks 30, 34; loud, when the guard is there)*

```python
import hashlib
EVAL = [("I was charged twice", "billing"), ("My app crashes on start", "technical"), ("Hello there", "greeting")]
def fingerprint(cases):
    return hashlib.md5("\n".join(f"{t}|{y}" for t, y in cases).encode("utf-8")).hexdigest()
FROZEN = fingerprint(EVAL)
print("frozen:", FROZEN)
EVAL[0] = ("I was charged twice.", "billing")           # one full stop, "to be fair"
print("now   :", fingerprint(EVAL))
assert fingerprint(EVAL) == FROZEN, "the eval set changed after it was frozen"
```
```text
frozen: 855dc152c1da65cad6caeb4989ee9155
now   : 846a9ee4cb78bf38b11ff0d556771067
Traceback (most recent call last):
  File "block.py", line 9, in <module>
    assert fingerprint(EVAL) == FROZEN, "the eval set changed after it was frozen"
AssertionError: the eval set changed after it was frozen
```
**Meaning:** one character changed the fingerprint entirely, which is the whole mechanism (the
output shows the two values, then the traceback's last lines). **Why it matters more than any other error of
Term 4:** a tempted student "fixes" a case because one prompt failed it; the eval is then measuring
the student, not the system. Week 30's clinic and Week 34's D1 and D2 are this error in a dozen
costumes. **The sentence:** *"We write the eval first and we do not edit it to make a number go up."*

### The summary table

| # | Error | Week | Loud? | The check that catches it | The question |
|:--:|---|:--:|:--:|---|---|
| 1 | Wrong folder | 1 | Loud | `ls` shows `l4lib` | "What does `ls` show?" |
| 2 | Positional args to a `*` function | 1 | Loud | Read the signature | "Is there a star?" |
| 3 | Reading a removed gradient | 2 | Loud | Read before clearing | "When was it cleared?" |
| 4 | `s = BASE` is not a copy | 7 | **Silent** | Print the base after the sweep | "Did BASE change?" |
| 5 | Missing `batch_first` | 8 | **Silent** | Print the final-state shape | "What shape, and what should it be?" |
| 6 | Float word ids | 8, 16 | Loud | `dtype` is `Long` | "Whole numbers only?" |
| 7 | `backward()` twice | 10 | Loud | Rebuild the forward pass | "Did you run forward again?" |
| 8 | Softmax over the wrong axis | 13-15 | **Silent** | Rows add to 1 | "Which numbers add to 1?" |
| 9 | `k` bigger than the choices | 13 | Loud | `min(k, n)` | "How many are there?" |
| 10 | Mask with `0`, not `-inf` | 15 | **Silent** | Weights above the diagonal are exactly 0 | "What does the first word see?" |
| 11 | Plain list of layers | 16 | **Silent** | Count the knobs by hand | "How many knobs should it have?" |
| 12 | `json.loads` on a chatty reply | 23 | Loud | Find the braces first | "Is the whole reply JSON?" |
| 13 | Catch-all `except` | 23 | **Silent** | Catch by name | "Can the alarm ring?" |
| 14 | `argsort` without the minus | 26 | **Silent** | Read the retrieved chunks | "Retrieval or generation?" |
| 15 | One run, one conclusion | 7, 23-33 | **Silent** | Mean and spread; the wobble | "How much does it move with the seed?" |
| 16 | Editing the frozen eval | 30, 34 | Loud (with guard) | The fingerprint | "Did the eval change?" |

## 8.17 — When a run fails: what to do, in order

```
   THE RUN CRASHED
     1. "Read me the last line."
     2. Is it one of errors 1-3, 6, 7, 9, 12, 16?  →  the table above has the fix
     3. Else: "Which was the last line that definitely worked?"  →  print the shape there
     4. Still stuck after 12 minutes of real attempts?  →  the teacher file's Clinic has it

   THE RUN FINISHED BUT THE NUMBER IS WRONG
     1. "Which rows, how many, which seed?"
     2. "What does the week file say it should be?"   Within tolerance (±0.005)?  →  fine
     3. First decimal different?  →  seed, folder, or set_num_threads(1)
     4. Suspiciously GOOD?  →  leakage, the mask (error 10), or a floor you did not compute
     5. Suspiciously CLEAN against a stand-in?  →  that is the point; restate the label

   THE RUN IS TOO SLOW
     1. Use the week's stated reduced default. Never skip the seed.
     2. Check power settings and set_num_threads(1).  Do not change the step count silently.

   THE RUN HANGS
     1. Does it wait on input()?  →  it should not; stop it and read the block
     2. A tool with no timeout (Week 29, mistake 10)?  →  that is the lesson; add the timeout
```

> **Rule:** when the arithmetic and the code disagree, **stop everything.** It is a finding.

---
---

# ❓ Section 9 — The 20 Questions Students Ask in This Level

Honest answers. Say the honest one, including "I don't know".

**1. "Is this how ChatGPT works?"**
Same recipe, at a scale that is not comparable. TinyGPT is a decoder-only transformer trained to guess
the next character, with 807,196 knobs and 6,972 characters of text. GPT-2 small is **quoted, not
reproduced**: about 124 million. The architecture ideas are the same (attention, a mask, positions,
residuals, layer norm, a next-token loss). What is different is scale, the data, a tokenizer, and the
post-training of Week 22 done at a vast scale. Nobody has a secret extra kind of maths. Say both halves.

**2. "Why is a coin's loss 0.693?"**
A two-class model that says 50-50 gives the right class probability one half, and the surprise of a
one-in-two event is `ln 2 = 0.693`. A **ten**-class guesser scores `2.303`; a 28-letter guesser scores
`3.332`. So 0.693 is not "a bad loss"; it is the loss of a model that knows nothing *about two classes*.

**3. "Why do we use a fake model? Why can't we just use the real one?"**
Because there is no network access, no account, and no key, and because a real model would make every
number depend on something we cannot see or repeat. What we *can* build is everything around a model:
the frozen test set, the parse, the fences, the trace, the budget. Those are properties of code, and
they would be the same in front of a real model. We call the fake one a **stand-in** so nobody forgets.

**4. "Is the stand-in dumb on purpose?"**
It is *transparent* on purpose. Its skill is a documented function of features of the prompt, written
in a file you can read. A real model's skill is hidden in billions of numbers. You can audit the first
and not the second, and the first lets you check that your measuring instrument works: a judge with a
planted bias is one you can catch (Week 30).

**5. "Would a real model fall for the injection?"**
Honest answer: some might, some wouldn't, and we have not tested one. What the week shows is that a
*capability limit* (the agent is not allowed to do the thing) holds whether the model is fooled or not,
and a *scan* or a *polite warning* only lowers a probability. That lesson transfers; the rate does not.

**6. "Why is Adam's first step always the learning rate?"**
Because it divides the gradient by its own typical size (Week 3). A gradient of 1 and a gradient of
1000 both become a step of about `lr`. Show them the table in §3.2. The one place it stops being true
is when the gradient is as small as epsilon.

**7. "Why does my number differ from the guide in the third decimal?"**
A different PyTorch, a different CPU, or the thread count. Within ±0.005 on losses, that is fine. In
the first decimal, something real is different. (§7.5.)

**8. "Why can't I `pip install` something?"**
The proxy blocks it (that is the 403), and nothing in the course needs it. Do not treat it as an
error.

**9. "Why do the attention by hand if numpy does it?"**
Because the number that comes out of PyTorch in Week 17 is this arithmetic, and until you have done
nine scores and three softmaxes with a pen, "attention" is a word. After you have, it is a recipe with
a weighted average at the end.

**10. "Why divide by the square root of `d`?"**
Because a dot product of two random `d`-long vectors has a spread of about `sqrt(d)`, and a softmax on
numbers that large freezes into "all the weight on one word". Dividing by `sqrt(d)` brings the spread
back to about 1. We measured it (§3.6). We did not prove it.

**11. "Does the model understand what it's writing?"**
Say what is true. It assigns probabilities to the next character and it has learned patterns in 6,972
characters of typed text. The samples look like writing; 60% of their words appear in the training
text (Week 17). Whether that is "understanding" depends on a definition nobody in the room has. What we
*can* do is measure what it gets right and what it gets wrong, on text it did not see.

**12. "My ablation got *better* when I removed something. Why?"**
Two different reasons, and Week 19 has both. Removing the **layer norm** made this small model
better: a measured fact about one small model, not a law. Removing the **mask** gave the best number
of the whole table (`0.077`) because the model can now read the answer: that number proves nothing.
Ask: *"Could it see the answer?"*

**13. "Why not just use a bigger network?"**
Sometimes that is the answer: Week 21's line says ten times the knobs takes about a quarter off the
loss. But the line is four points, the fifth model misses it by about 16%, and bigger models overfit
faster on 120 points (Week 5). A bigger model is one knob; it is not the only one.

**14. "Is my BPE what the real ones do?"**
Same family: start from bytes, merge the commonest pair, repeat. Real vocabularies are trained on far
more text and have far more merges. "About 4.5 bytes per token" for a real tokenizer is **quoted, not
reproduced**: the number you measure climbs with your corpus (Week 20).

**15. "Why did RAG cite the wrong note?"**
Then it is a retrieval problem or a generation problem, and the way to tell is to **read the chunks it
was given** (Week 26). If the right note was not retrieved, it is retrieval. If it was retrieved and
the answer still ignored it, it is generation. The citation check is code: the id must be among the ids
you served.

**16. "What is the difference between prompting and fine-tuning?"**
A prompt changes what the model is *asked*; fine-tuning changes the model's *knobs*. Week 24 shows the
first on a model they trained (examples in the prompt help), and Week 31 the second (and the
regression it caused in one category while the average rose).

**17. "Is 17 out of 25 good?"**
Compared with what? (The floor.) In which categories? (The per-category table.) How much would it
move with another seed? (The wobble.) Twenty-five cases cannot see a small difference. It is a fine
start and a poor conclusion.

**18. "Is red-teaming hacking? Can I try it on something else?"**
Week 33 is about attacking **your own** system, on data that is invented, in a sandbox. Attacking
somebody else's system is a different thing with different rules and real consequences, and this
course is not permission for it. Say so plainly.

**19. "Why is the data all typed or generated? Where is the real data?"**
So that nothing downloads and every number repeats. The cost is that nothing here resembles a real
support queue, and the course says so. Week 30's tickets, Week 32's results and Week 33's notes are
each labelled **typed** or **invented**. The habits are what transfer: write the eval first, report
every category, say what the number is a property of.

**20. "What could I actually build with this?"**
A small question-answering system over notes you wrote, with retrieval, a refusal path, a frozen test
set, a fence around any tool it uses, and an honest card that says where it fails. That is the
capstone, and it is a sensible shape for a real project. What you could *not* do yet is train a large
model; nothing in this course is evidence about how one behaves.

---
---

# ⚠️ Section 10 — The 15 Things Adults Get Wrong Teaching This Material

**1. Saying a stand-in's rate as a fact about AI.** *"The model falls for it 30% of the time."* It is a
number somebody typed (`0.3`). Say "the **stand-in**", every time, until the student says it before you.

**2. Making the stand-in smarter to make it more impressive.** It is transparent because it is
auditable. A cleverer fake is more fun and more misleading. Don't.

**3. Teaching the symbol before the number.** Writing `KL(p || q)` or `sqrt(d_k)` on the board before
anyone has done the arithmetic. Numbers first, name second, symbol third, often skip the third.

**4. Apologising for the maths.** *"Sorry, this bit is horrible."* You have told them it is reasonable
to give up. Say: *"This bit is multiplication and a square root. Watch."*

**5. Saying "just".** *"Just divide by sqrt(d)."* Nothing in this level is "just".

**6. Explaining for longer than fifteen minutes.** Every Concept segment is capped around 12-18
minutes. If they are bored, you are still talking. Get to the arithmetic.

**7. Taking the keyboard.** §11. It is the most damaging habit available to you, and it feels helpful.

**8. Skipping the hand step "because the code does it".** The code *checks* the paper. A student who has
only seen the code cannot tell when the code is wrong, and in this level it is wrong silently (§8).

**9. Being pleased by a good number.** When the ablation table says `0.077`, the correct facial
expression is suspicion, out loud. *"What could it see? What's the floor? Which rows?"* It is the most
transferable habit in the year.

**10. "Fixing" the eval set.** A case fails, it looks unfair, you reword it. You have just measured the
student instead of the system. Week 30 and Week 34's clinics are this mistake in costume; the
fingerprint exists so that you cannot do it quietly.

**11. Rushing Week 10, Week 14 or Week 17.** Week 10 (the gradient that fades) motivates everything in
Terms 2-3; Week 14 (attention by hand) is what makes a transformer not magic; Week 17 is where they
*build* the thing. If one needs two sittings, take two. Compress Week 9.

**12. Letting the guide's numbers into the student's report.** Rule 6: a number in a report must have
been printed by their own run, with a seed, in the last 24 hours. The guide's value is a check, never a
source.

**13. Skipping the deliberate mistake.** It is five minutes. It is where tracebacks stop being
frightening and where the *silent* errors (§8) get their names.

**14. Filling the silence while a run trains.** Eighty-five seconds of nobody talking is a fine thing.
It is the time to ask what loss they expect at step 1.

**15. "Let's just try it on a real chatbot."** Curiosity is good; a real reply has no seed, no *n* and no
label, and it will tempt the student to paste an anecdote into a table of measurements. If they want
to, do it after the lesson, not inside it, and never put its answer in a report.

---
---

# 🙌 Section 11 — How to Help Without Taking the Keyboard

## 11.1 — The rule

**Your hands do not touch their keyboard. Ever. All year.** If you must show something, use your own
machine, or paper. A student who watches an adult fix a shape error learns that shape errors are fixed
by adults; a student who watches an adult type the `-inf` learns that masks are something adults know.

## 11.2 — The escalation ladder

Work down it. Wait ten full seconds between rungs. Ten seconds is much longer than it feels, and it
is where most of the learning happens.

```
   1.  "Hm."                                            ← often enough
   2.  "Read me the last line."
   3.  "What did you expect it to do?"
   4.  "What shape is it?"                              ← from Week 8 on
   5.  "Print it. What actually came out?"
   6.  "Which line was the last one that definitely worked?"
   7.  "Which numbers have to add to 1?"                 ← attention, sampling, RAG weights
   8.  "What did we get on paper for this one?"          ← every maths mismatch
   9.  "Is that a real model or a stand-in?"             ← from Week 23
  10.  "Which rows? How many? Which seed?"
  11.  "What's the floor?"                               ← before any model score
  12.  "Look at the teacher file's version of this line — what differs?"
  13.  Point at the line. Do not say what is wrong with it.
  14.  Say what is wrong with it. Let THEM type the fix.
```

You will rarely get past rung 5. Rungs 13 and 14 are the last resort and are still not *you typing*.

## 11.3 — The ten sentences

Keep them on a card.

1. *"Read me the last line."*
2. *"What shape is it?"*
3. *"What did you expect?"*
4. *"Show me on paper first."*
5. *"Which numbers have to add to 1?"*
6. *"Real, invented, stand-in or quoted?"*
7. *"Which rows, how many, which seed?"*
8. *"What's the floor?"*
9. *"How much does that move if you change the seed?"*
10. *"I don't know. Let's measure it."*

Number 10 is the most important, and saying it honestly, with curiosity, and then actually measuring,
is the single best teaching moment available to you. **Modelling "I don't know, so I will measure" is
more of the syllabus than any individual fact.**

## 11.4 — When to actually intervene

Take over the *thinking* (never the keyboard) when:

- **Twelve minutes of genuine stuck**, with real attempts, and morale is going. Twelve, not three.
- **The blocker is a fact they cannot deduce**: that `F.softmax` wants `dim`, or that a `ModuleList`
  exists. Facts are gifts; give them freely. Reasoning is not.
- **It is an environment problem** (the folder, a 403, a slow laptop). Never make a student debug
  their setup. Fix it on your own time.
- **Tears, or the beginning of them.** Stop. Close the laptop. Do three numbers on paper. The lesson
  can lose fifteen minutes; it cannot lose the student.

## 11.5 — "I don't get the maths" — the most important page in this file

You will hear it, probably five times this year, most likely in Weeks 3, 10, 14, 15 and 22. **What you
do in the next sixty seconds decides whether the level works.**

**Do not** re-explain it (they did not fail to hear you). **Do not** say "it's easy really" or "we can
come back to it" (you can't; the ladder means next week stands on this one). **Do not** reach for a
fifth analogy. **Do** stop talking, pick up a pencil, and do the smallest version with numbers *they*
choose.

**The script for the moving average (Week 2):**

> **You:** *"Forget the word. Start with a running number that is 0. Here is the rule: take 0.9 of
> what you have, and add 0.1 of the new number. The new number is 10. What have you got?"*
> **Them:** *"One."* (0.9 x 0 + 0.1 x 10)
> **You:** *"Now the new number is 0. What have you got?"*
> **Them:** *"0.9."*
> **You:** *"And again, new number 0?"*
> **Them:** *"0.81."*
> **You:** *"That's it. The 10 is still in there, 0.9 of it per step. That is the thing you said you
> didn't get. The word for it is 'moving average'."*

**The script for a weighted average, which is attention's last step (Week 14):**

> **You:** *"Three numbers: 10, 50, 30. Count 70 percent of the first, 20 percent of the second, 10
> percent of the third. Add them."*
> **Them:** *"7, 10, 3... 20."*
> **You:** *"Now give it to a friend who wants only the second. What weights?"* **Them:** *"0, 1, 0."*
> **You:** *"50. A softmax is just a way to make the weights up from scores, so that they're positive
> and add to 1. The rest is this."*

**For any other idea in the year,** the move is the same: numbers *they* chose, a completed correct
calculation in their own handwriting, then the word.

| What they actually mean by "I don't get it" | What the pencil fixes |
|---|---|
| "I don't know what the symbols refer to" | Replaces every symbol with a number they chose |
| "I can't hold five things at once" | One thing at a time, written down |
| "I don't believe I'm the kind of person who does this" | A completed correct calculation, in their handwriting |
| "I lost the thread four minutes ago and was embarrassed to say" | Restarts from a place that cannot be lost |

**The follow-up, next lesson:** ask them to do the same three numbers again, cold, at the start.
If they can, it landed. If not, do it again, cheerfully, with different numbers, no comment on the
repeat. Two or three cycles fixes it. Re-explaining, however many times, does not.

> ### 🔑 The one-line version
> **When they say "I don't get the maths", the answer is never more words. It is three numbers and a
> pencil.**

---
---

# ✏️ Section 12 — How to Mark Code, Claims and Papers

## 12.1 — Marking code: four questions, in this order

1. **Does it run?** If not, is the error *understood*? A student who pastes the traceback and writes
   "the ids were floats, the table wants whole numbers, out of time" has shown more than one with code
   they cannot explain. Give real credit for it.
2. **Is the number right?** Compare against the week file. **With the seed set and the tolerance
   (±0.005), a difference in the first decimal is a finding, not rounding.**
3. **Was the arithmetic checked by hand anywhere?** A result with no hand check attached is half a
   result. Look for the paper.
4. **Is the evidence named?** Any reported figure says *which rows*, *how many*, *which seed*, and *real,
   invented, stand-in or quoted*.

## 12.2 — Be strict about exactly six things

Everything else, be generous. These six, be immovable:

| Be strict about | Why |
|---|---|
| **A seed in every file that prints a number** | A number you cannot reproduce is not a result |
| **An *n* beside every rate** | "17 of 25" means something; "68%" does not |
| **A floor before a model score** | Otherwise 0.94 is unanchored |
| **The label on every stand-in result** | The year's central honesty habit |
| **The frozen eval never edited** (check the fingerprint) | Otherwise you measure the student, not the system |
| **One Bug Log entry per real error** | The artifact that compounds all year |

Be relaxed about: variable names, comment density, loops versus comprehensions, chart prettiness,
file organisation.

## 12.3 — The four-tick scheme for a week's work

| Ticks | Means | Looks like |
|:--:|---|---|
| ✓✓✓✓ | Mastered | Runs, numbers match, hand check present and correct, evidence named, and they can explain *why* when asked a question not on the sheet |
| ✓✓✓ | Solid | Runs, numbers match, hand check present; the explanation is mostly recall |
| ✓✓ | Getting there | Runs with help, or numbers match but no hand check, or a slip they find when prompted |
| ✓ | Attempted | A real attempt, errors pasted, the stuck point identified in writing |

**A ✓ with a well-written stuck point is a genuinely good outcome and should be said out loud.** The
failure state is a blank page, not a wrong answer.

## 12.4 — Marking a written claim

From Week 7 on they write things like *"Adam at 1e-3 reached 0.013 train loss, mean of three seeds"* or
*"the mask-off model's 0.077 is a leak, not an improvement"*. Mark each against five questions:

| Question | A good answer | A weak answer |
|---|---|---|
| **Is there a number in it?** | "0.077 against 1.67 for the baseline" | "it was much better" |
| **Does it say which rows, how many, which seed?** | "on the 698 validation characters, seed 0" | "on the test set" |
| **Is the mechanism named, not just the effect?** | "with no mask the model reads the answer at the next position" | "it overfit" |
| **Is the kind of number labelled?** | "against the **stand-in**; a property of its script" | "the model got it wrong 30% of the time" |
| **Does it say what would change their mind?** | "a second seed, or a different corpus" | (nothing) |

Three of five is good work at 15. Five of five is what the capstone card asks for, and by Week 36 it
is reachable.

> **⚠️ Watch out:** the commonest weak explanation this year is **fluent and wrong**: a confident
> paragraph using "overfitting", "attention" and "grounded" almost correctly, with no number in it.
> Do not reward it. Ask *"which number in your own results tells me that?"* If there isn't one, the
> explanation is a guess wearing vocabulary.

## 12.5 — The term papers and the capstone

- **Weeks 9, 18, 27, 36** each have a 75-minute paper **with its key and marking sheet inside that
  week's teacher guide.** Mark the paper, then mark the *reflection* separately and more generously:
  it is for them, not for you. The paper is an X-ray, not a grade; the per-week remediation table tells
  you which earlier week to revisit.
- **Week 18** carries the attention arithmetic again on new numbers; if they get it, say clearly that
  it is a long piece of hand work and they have done it.
- **Weeks 34-36** are marked against the capstone. Draft weights in the course README (to be
  finalised by the course owner): eval design 25, measured evidence 25, guardrails and red-team 20,
  honesty of the card 20, demo 10. **The honest section, *what it fails at and who should not rely on
  it*, is marked as heavily as the working code.** A card that says only "may occasionally be
  inaccurate" (Week 36, Clinic D6) loses most of the honesty marks whatever the score: the section
  needs a real input, a real wrong output, a number with an *n*, and a named person.
- The final oral question: *"Here is a wrong answer. Was it retrieval, generation, the prompt, the
  tokenizer, or a person over-trusting it? Show me the evidence."*

---
---

# ✅ Section 13 — The Pre-Flight Checklist

Run this before every class. It takes about eight minutes and prevents most lesson disasters.

```
   ┌───────────────────────────────────────────────────────────────────────────┐
   │  ✈️  PRE-FLIGHT — BEFORE EVERY CLASS                                       │
   ├───────────────────────────────────────────────────────────────────────────┤
   │                                                                           │
   │  THE NIGHT BEFORE (20-60 min; the week file says)                          │
   │  ☐  Read the week's teacher file, start to finish                         │
   │  ☐  🔢 DO THE ARITHMETIC IN THE "MATHS YOU NEED" SECTION, ON PAPER.         │
   │     Done, not read. On a no-maths week, do the hand table in the Activity.  │
   │  ☐  Run every block in the Prep Checklist; check against the printed output │
   │  ☐  Cause the week's first deliberate mistake once, so you have seen it     │
   │  ☐  Read the 🧭 Real vs stand-in table and the 🚫 "must NOT claim" box      │
   │  ☐  Weeks 23-36: find which parts of the week are stand-ins (§5.4)           │
   │  ☐  Note the ONE sentence you want them to leave with                       │
   │                                                                           │
   │  ON THE DAY (3-5 min)                                                      │
   │  ☐  Terminal is in the folder that contains l4lib/                         │
   │  ☐  Last week's file still runs (30 seconds; catches a broken setup)       │
   │  ☐  Printed workbook page(s) on the table; pencils, eraser, calculator      │
   │  ☐  The Bug Log notebook open on the table                                 │
   │  ☐  Any long run started or queued (§6.3)                                   │
   │  ☐  Phone face-down and out of sight. Yours too                             │
   │                                                                           │
   │  IN THE FIRST 60 SECONDS                                                   │
   │  ☐  Ask them to tell YOU last week's number: which rows, how many, which   │
   │     seed, and what kind of number it was                                   │
   │                                                                           │
   ├───────────────────────────────────────────────────────────────────────────┤
   │  IF THE LAPTOP IS DEAD: every teacher file has a paper-only fallback in    │
   │  its Prep section. The maths was always the lesson, and it runs on paper.  │
   └───────────────────────────────────────────────────────────────────────────┘
```

### The end-of-class 60-second review, for you, not them

Four questions, in your own notebook, every week:

1. **Did they do arithmetic with their own pencil today?** (If no, the lesson did not happen.)
2. **Did the code check the arithmetic, and did they see it agree?**
3. **What did they say back to me in their own words that I did not say first?**
4. **What is the one thing I should re-ask at the start of next week?**

Question 3 is your real assessment. Everything else is bookkeeping.

### The one-page cheat-sheet to keep next to the laptop

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  LEVEL 4 · THE CARD                                                   │
   ├───────────────────────────────────────────────────────────────────────┤
   │  TWO-CLASS COIN     loss = ln 2 = 0.693.   28 LETTERS: ln 28 = 3.332   │
   │                     a model's FIRST loss must be within 0.05 of ln V   │
   │  ONE KNOB AT A TIME  three seeds, mean and spread, never one lucky run  │
   │  MOVING AVERAGE     new = 0.9 x old + 0.1 x value  (half-life ~ 7)      │
   │  TYPICAL SIZE       square, average, root.  g / rms kills the scale     │
   │  COMPOUNDING        0.9526^40 = 0.143.  0.5^40 = 9e-13                  │
   │  WEIGHTED AVERAGE   weights >= 0, add to 1.  Softmax rows add to 1      │
   │  SCALE              dot product of random d-vectors wobbles sqrt(d)     │
   │  TRIANGLE           1+2+...+k = k(k+1)/2  ->  bill grows like k x k      │
   │  KAPPA              (agree - luck) / (1 - luck).  90% agree can be zero  │
   │  WOBBLE OF A COUNT  sqrt(n p (1-p)).  20 runs cannot see a small gap    │
   ├───────────────────────────────────────────────────────────────────────┤
   │  BEFORE YOU BELIEVE A NUMBER:  real, invented, stand-in or quoted?      │
   │     which rows?  how many (n)?  which seed?  what is the floor?         │
   │  STAND-IN?  "This is a stand-in for a model, not a model."  Say it.     │
   │  NUMBERS CHANGE EACH RUN   forgot the seed.   FIRST DECIMAL OFF  wrong   │
   │                            folder, seed, or set_num_threads(1)          │
   │  SCORE TOO GOOD    a leak (mask? eval? contamination?)                  │
   │  NEVER             edit the frozen eval to make a number go up          │
   ├───────────────────────────────────────────────────────────────────────┤
   │  THE TEN SENTENCES                                                    │
   │  "Read me the last line."     "What shape is it?"                     │
   │  "What did you expect?"       "Show me on paper first."               │
   │  "Which numbers add to 1?"    "Real, invented, stand-in or quoted?"    │
   │  "Which rows, how many, which seed?"      "What's the floor?"          │
   │  "How much does it move with the seed?"                               │
   │  "I don't know. Let's measure it."                                    │
   ├───────────────────────────────────────────────────────────────────────┤
   │  "I DON'T GET THE MATHS"  ->  never more words. Three numbers and a     │
   │                              pencil. §11.5                            │
   └───────────────────────────────────────────────────────────────────────┘
```

---
---

# 🧾 Last Thing

You are about to teach a fifteen-year-old to turn a loss curve into a diagnosis, to build a small
transformer from `nn.Linear` up, to measure whether a test set has been tampered with, and to write one
honest page about where their own system fails. Some adults who will hear about this year could not do
the last of those.

You will not know every answer. That is not the job. The job is:

- **Do the week's arithmetic on paper, the night before.** Twenty minutes. This is the whole deal.
- **Say "stand-in, not a model" every time it is one**, and make the student say it before you do.
- **Keep your hands off their keyboard.**
- **Ask of every number: which rows, how many, which seed, and what kind?**
- **Say "I don't know. Let's measure it."** and then measure it in front of them.
- **When they say "I don't get the maths", reach for a pencil and three numbers, not for more words.**

If you remember one thing from these two and a half hours, make it the last of those, and then the
promise the course makes in its final line: by Week 36 the student will be able to tell a stranger
exactly which parts were real models, which were stand-ins, which numbers they measured and which they
only quote, and they will know, because they built it, that **a number you cannot reproduce is not a
result.**

Now go and do the §7 setup, alone, with nobody watching. Then open Week 1.

---

[⬅ Course home](../README.md) · [**Week 1 teacher guide ➡**](week-01.md) · [Week 1 student guide](../student-guide/week-01.md) · [Week 1 workbook](../workbook/week-01.md) · [Capstone brief (reference)](../../capstone.md) · [Level 4 glossary](../../glossary.md)
