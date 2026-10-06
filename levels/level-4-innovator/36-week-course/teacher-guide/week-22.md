# Week 22 — After Pretraining: SFT, Reward Model, DPO

[⬅ Week 21](week-21.md) · [Course Home](../README.md) · [Week 23 ➡](week-23.md) · [Student Guide](../student-guide/week-22.md) · [Workbook](../workbook/week-22.md)

---

![Map of the 36 weeks with Week 22, After Pretraining: SFT, Reward Model, DPO, highlighted in Term 3](../figures/fig-w22-0-where-this-fits.svg)
*Figure 22.0 — Week 22 is the fourth lesson of Term 3: what is done to a model after pretraining.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~60-75 min) |
| **Type** | 🟦 Teach — **one new maths idea, four new constructs, and the most crowded hour of Term 3.** Three ideas from Module 4 (masked SFT loss, a reward model, DPO) in one sitting. Each is a toy small enough to run in about a second, and each has a number the student can predict on paper first. |
| **Big idea** | A pretrained model continues text; it does not answer. Three cheap steps turn "continues" into "answers the way people prefer". **(1) SFT:** keep training on prompt-and-answer pairs, but score the model **only on the answer** (the prompt is masked out of the loss). **(2) Reward model:** people find it easier to say *which of two answers is better* than to write a perfect one, so learn a scoring function from pairs, with `-ln sigmoid(reward of winner - reward of loser)`. **(3) DPO:** skip the reward model and move the model's own chances directly, measured **against a frozen copy of where it started**. The leash on how far it may travel is a number called `beta`, and the distance travelled is a number called **KL divergence**. |
| **New vocabulary** | **SFT** (supervised fine-tuning) · **demonstration** · **loss mask** (`-100`) · **preference pair** (chosen, rejected) · **reward model** · **Bradley-Terry loss** · **reward hacking** · **reference model** (frozen) · **DPO** · **`beta`** · **KL divergence**. (**Cross-entropy, sigmoid, `ignore_index`, Adam and "the log-chance of the right answer" are already theirs**: Level 3 Weeks 13-14, Week 3, Week 12. Say so and use them.) |
| **New maths** | **KL divergence**: the average of `ln(p/q)` over the outcomes, each weighted by `p`'s own chance. "How far did the leash let you move." Met **on two 4-outcome tables, by arithmetic only**: `0.1733` and `0.4458`. See the 🔢 box. |
| **New syntax** | `F.logsigmoid` · `F.log_softmax` · `torch.gather` · `tensor.detach()`. That is all four. |
| **Dataset** | None downloaded. Random "scores" for nine positions of a pretend 12-token vocabulary (`torch.manual_seed(0)`); a 42-character prompt-and-answer typed by you; **six candidate answers written as five 0/1 features each** and **ten typed preferences**; a **four-answer toy policy** with four starting scores. **Nothing downloads. No internet.** |
| **Model** | Real PyTorch on the CPU, but **no language model is trained or run today.** The "reward model" is five weights; the "policy" is four numbers; the "SFT model's output" is random. **There is no scripted backend and no stand-in LLM anywhere in this week** — but see the "Real vs stand-in" table: every toy here is a toy, and nothing it does says anything about a real assistant. |
| **Materials** | Laptop with Python 3 and torch (nothing new to install) · a working folder (**nothing today imports `l4lib`**) · workbook pages 22.1-22.6 printed · a calculator with `ln` and `e^x` keys (a phone is fine; **airplane mode on**) · scrap paper · a timer |
| **Prep time** | 35 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | Every file below finishes in **about a second**; the full set of nine files, run in one Python session, takes **1.7 seconds** on the author's CPU (the slowest, the 3,000-step sweep, is 0.8 s). **Nothing in this lesson takes over 10 seconds**; if anything does, something is wrong (see Fallback). |

> **⚠️ Watch out:** the sentence the student will want to leave with is *"a low loss means the model is good."* **Today's numbers contradict it twice.** The DPO run with `beta = 5` ends with a loss of `0.0020`, far smaller than the `0.2560` of `beta = 0.1`, **and it moved the model much less** (`A = 0.589` against `0.997`). And the masked SFT loss (`4.0407`) is *higher* than the unmasked (`3.8008`) — it is a different, more honest number, not a worse model. A loss is only comparable with another loss **from the same setup**. The second thing that goes wrong is **believing the toys**. The reward model has five weights and ten judgements; the policy is four numbers. They show the *mechanism*; they do not show what happens to a real assistant. The third is the module's phrase "**small `beta` = long leash**". It is **true only once the run is long enough**, and at the module's own fixed 300 steps the data say otherwise (see section 6 and `sweep.py`). Teach what was measured.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say why SFT masks the prompt, and do it**: the guess at place `t` is for place `t+1`, so with a 5-token prompt the first **4** guesses are set to `-100`; show `3.8008` (all 8 guesses) against `4.0407` (the last 4) on the same numbers, and say which one is SFT.
2. **Train a reward model from pairs**: write the Bradley-Terry loss with `F.logsigmoid`, watch it start at `0.6931` (`ln 2`, "no idea which is better") and fall to `0.0017`, and read five weights as "what the raters liked".
3. **Find the hacked feature**: `has_numbered_steps` has the largest weight (`+5.047`), so an answer that is **only** numbered steps and says nothing (`r9`) outscores a short direct one (`+5.047` against `+4.578`). And say why a feature that never differs **inside a pair** gets weight exactly `0`.
4. **Compute a KL divergence on paper**: two 4-outcome tables against a uniform reference, `0.1733` and `0.4458`; say it is `0` only when the two are equal, and that it depends on which table goes first (`0.4458` against `0.4298`).
5. **Run DPO at two values of `beta`** and explain, with the KL number beside it, what `beta` did: at 300 steps `beta = 0.1` reaches `A = 0.997` with KL `1.760`, `beta = 5.0` reaches `A = 0.589` with KL `0.566`; and say why the smaller *loss* belongs to the model that moved less.

Observable evidence: `sftmask.py` printing `3.8008` and `4.0407`; the student's hand KL on workbook page 22.3 matching `0.1733` / `0.4458`; `reward.py` printing `train-pair agreement: 10/10` and the student circling `has_numbered_steps`; `dpo.py` printing the two `beta` rows; and the student's spoken answer to *"why is the loss smaller at `beta = 5` when the model moved less?"*

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** was run, **in order, in one Python session (one shared namespace)**, on a CPU with `torch.set_num_threads(1)` and the seeds shown; the outputs printed below are the real printed output, and **the whole set was run twice with every printed line identical** (apart from the `seconds:` line). Blocks in the **🐞 Debugging Clinic** are **deliberate mistakes**, each marked, each run on its own, and their tracebacks and odd numbers are real. Different CPU or PyTorch build: the last digit of a loss can move; nothing in the lesson depends on a last digit. **Numbers that come from the module or the ground-truth ledger rather than from a block run for this guide are labelled "ledger" or "module"**; the rest were printed by the blocks here. The author ran the whole set on PyTorch 2.2.1.

### 1. What the student is doing today, in one paragraph

Last week the student fitted a straight line through four training runs and saw that pretraining is "the Week 17 loss, at a scale". Today the model is *finished pretraining* and the question is what to do next. A pretrained model, asked "q: what runs past the town?", carries on the text; it does not answer. Three toy versions of the three fixes. **One:** SFT. The student scores a model's guesses on an 8-position example twice, once over every guess and once over the last four only, and sees `3.8008` against `4.0407`; they build the mask by hand with `log_softmax` and `gather`, and check it against `F.cross_entropy(..., ignore_index=-100)` from Week 12. **Two:** a reward model. Ten typed judgements between six answers, five weights, the loss `-logsigmoid(winner - loser)`, and the uncomfortable finding that the biggest weight is for *formatting*. **Three:** DPO. A four-answer policy starts where the SFT model is, is told six preferences, and is trained for 300 steps at two values of `beta`. On paper, before any of it, they compute a KL divergence on two small tables of chances. Everything is real PyTorch, everything is a toy, and the lesson is honest about both.

### 2. 🔢 The maths you need — taught to you first

**One new idea: KL divergence.** Do all of this yourself, with a calculator, before class.

**(a) The log-ratio.** The student already has `ln` as a *surprise meter* (Level 3 Week 14): `-ln(chance)` is how surprised you are by something that had that chance. Now take **two** tables of chances for the same four outcomes: `q`, the **reference** (where we started) and `p`, the **policy** (where we are now). The **log-ratio** of one outcome is `ln(p / q)`. It is `0` if the outcome has the same chance in both tables, positive if it has become *more* likely, negative if *less*. Nothing else.

**(b) KL divergence is the average of the log-ratio, where "average" means weighted by `p`.** For outcomes with chances `p1..p4` and `q1..q4`:

`KL(p || q) = p1 x ln(p1/q1) + p2 x ln(p2/q2) + p3 x ln(p3/q3) + p4 x ln(p4/q4)`

Read it aloud as: *"go through the outcomes; for each, how much more likely did it get, in logs; weight that by how often the new table actually picks it; add up."* **Worked, table 1.** `q = [0.25, 0.25, 0.25, 0.25]`, `p1 = [0.50, 0.25, 0.125, 0.125]`.

| Outcome | `q` | `p` | `p / q` | `ln(p/q)` | `p x ln(p/q)` |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | 0.25 | 0.50 | 2 | `+0.6931` | `0.5 x 0.6931 = +0.3466` |
| 2 | 0.25 | 0.25 | 1 | `0.0000` | `0` |
| 3 | 0.25 | 0.125 | 0.5 | `-0.6931` | `0.125 x -0.6931 = -0.0866` |
| 4 | 0.25 | 0.125 | 0.5 | `-0.6931` | `-0.0866` |

Sum: `0.3466 - 0.0866 - 0.0866 =` **`0.1733`** (as a shortcut, `0.5 ln 2 - 0.25 ln 2 = 0.25 ln 2 = 0.1733`). **Worked, table 2.** `p2 = [0.70, 0.10, 0.10, 0.10]` against the same `q`: `0.7 x ln(2.8) + 3 x 0.1 x ln(0.4) = 0.7 x 1.0296 + 0.3 x (-0.9163) = 0.7207 - 0.2749 =` **`0.4458`**. The more the table has moved, the bigger the number.

**(c) Four facts about it, all of which `kl.py` prints.**
- **`KL = 0` exactly when `p = q`** (every log-ratio is `0`). It is never negative. That is the reason it works as "distance moved".
- **It is weighted by `p`, not plain-averaged.** The plain average of `ln(p1/q)` over the four outcomes is `-0.1733`, a *negative* number: it is not KL. The weighting by `p` is what makes it not negative.
- **It is not symmetric.** `KL(p2 || q) = 0.4458` but `KL(q || p2) = 0.4298`. So "distance" is a loose word; say "how far `p` has moved from `q`", and always say which is first. In every KL below, the **policy is first and the reference is second**.
- **It is unbounded if `p` gives a chance to something `q` says is impossible** (we do not need this today), and `0 x ln 0` must be treated as `0` (Mistake 8 is what happens if you do not).

**(d) Bradley-Terry by hand (Level 3's sigmoid and `ln`, nothing new).** The chance that answer `w` beats answer `l` is `sigmoid(r(w) - r(l))`, and the loss is `-ln` of that. Module numbers, checked by `key.py`: rewards `a = 2.1, b = 1.4, c = -0.3, d = 2.6` give `P(a beats b) = 0.6682`, `P(d beats a) = 0.6225`, `P(a beats c) = 0.9168`. A judge who says *c beats d* gives a gap of `-2.9`, `sigmoid(-2.9) = 0.05215`, loss **`2.954`**: a confident mistake costs `34` times what a confident success costs (`a` beats `c`: `0.0868`). Add `100` to every reward and nothing changes: **only differences matter**, so a reward has no "zero". With both rewards equal (all weights `0`) the chance is `0.5` and the loss is `-ln 0.5 = 0.6931`, which is why **step 1 of `reward.py` prints `0.6931`**. *Module note:* the module's hand-worked `c > d` lines read `0.05213` and `0.0869`; the exact values are `0.05215` and `0.0868` (fourth-decimal rounding, ledger `m04_11`).

**(e) DPO on one pair, by hand (the only new "formula" in the hour).** Keep four numbers: how much the policy's log-chance of the **chosen** answer has moved from the frozen reference, how much the **rejected** one has moved, and `beta`. The *margin* is `beta x (moved_chosen - moved_rejected)` and the loss is `-ln sigmoid(margin)`. Module example: reference log-chances `(-20.0, -18.0)` for (chosen, rejected), policy now `(-19.0, -19.5)`. Chosen moved `+1.0`, rejected moved `-1.5`. At `beta = 0.1` the margin is `0.1 x 2.5 = 0.25`, `sigmoid(0.25) = 0.5622`, loss **`0.5759`** (the module prints `0.5757` from rounding `0.5622`; `key.py` and torch both give `0.5759`). At `beta = 5` the same movement gives margin `12.5`, `sigmoid = 0.999996` and loss **`0.000004`**. **Same movement, a loss that is more than 100,000 times smaller.** The loss stops caring. That is the whole of what `beta` does, and it is why Mistake 9 exists.

> **Say to yourself:** KL is a *measurement* we take afterwards (`dpo.py` reports it; the loss never contains it). `beta` is a *dial inside the loss*. The link is: a big `beta` makes the loss satisfied by a small movement, so the model stops early, so the KL stays small. The toy has **no explicit KL penalty term**; the real RLHF objective does (the module's `r - beta x KL`), and we describe that and never run it.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| PyTorch, `F.log_softmax`, `gather`, `logsigmoid`, Adam, every printed loss, chance and KL | **Real.** Computed on the CPU. |
| The "model output" in `sftmask.py` (9 positions x 12 tokens) | **Random numbers** (`torch.manual_seed(0)`), **not a model**. That the response positions score higher (`4.0407`) than the whole (`3.8008`) is an accident of the random numbers. `ln 12 = 2.4849` is what a model that knew nothing would score; these random scores are *worse* than that. |
| The 42-character SFT example in `pairs.py` | **Typed by us.** No model reads it; it only shows how the mask is built. |
| The five features, six candidate answers and ten preferences in `reward.py` | **Invented by the course author** ("ten hand-made human judgements"). **There are no raters and no real preference data in this course.** The reward model is five weights, not a transformer. |
| The four-answer policy in `dpo.py` | **A toy**: four scores, where the "SFT model" is just the four starting numbers `[0.4, 0.6, 1.2, 0.8]`. The six preferences are invented (A beats everything, D loses to everything). It has no words and no prompt. |
| "Mode collapse" (`A = 0.997`, everything else `~0`) | **A property of this toy under these pairs**, not a measurement of any assistant. Say "the toy collapsed onto one answer", not "DPO collapses models". |
| PPO / RLHF, the "four models in memory" table, the `0.0003%` SFT-to-pretraining ratio, "reward hacking seen in real systems" | **Background from the reference module. Not run, not measured here.** Describe, never demonstrate, and do not quote as a result. |
| Any language model | **Not present today.** No scripted backend, no stand-in LLM. (From Week 23 the course uses a labelled scripted stand-in, `l4lib.fakellm`; today does not.) |

> **Say to the student, out loud:** *"Everything today is a toy on purpose: four numbers, five weights, random scores. It shows the machinery clearly. It does not tell you what happens to a real assistant, and nobody has shown you one."*

> **🚫 What you must NOT claim.**
> 1. **"SFT teaches the model new facts."** The module says it *selects a behaviour the base model could already produce*; that is background, and our toy neither shows nor refutes it. Say: "SFT shows it what an answer looks like."
> 2. **"The reward model knows what is good."** It knows what the ten judgements agreed on. The feature `is_factually_correct` gets weight `+0.000` not because facts don't matter but because **the data never asked** (`hack.py`).
> 3. **"Lower DPO loss = better."** Mistake 9. Compare the chance of the preferred answer and the KL, never the loss across different `beta`.
> 4. **"`beta` is the KL penalty."** In DPO it is the scale on the margin; the KL is only the thing we report. Say "`beta` sets how early the loss is satisfied".
> 5. **"Small `beta` always means a longer leash."** True at 3,000 steps in this toy, **false at the 300 steps the module uses** (KL `1.213` at `beta = 0.02`, which is *less* than `1.760` at `beta = 0.1`). The sweep mixes "how far it wants to go" with "how fast it gets there".
> 6. **"A reward model trained on preferences is unbiased / aligned / safe."** Nothing here measures bias. The hack is on the **features we invented**; a real reward model is a transformer and its blind spots were not studied.
> 7. **"DPO is better than RLHF."** Not tested. The module's table (DPO cannot exceed the pairs you give it; PPO can explore) is a description.

### 4. The four new constructs, for somebody who has never seen them

**(a) `F.logsigmoid(x)` — `ln(sigmoid(x))`, computed so that it does not break.** `torch.log(torch.sigmoid(x))` gives `-inf` when `x` is very negative, because the sigmoid rounds to exactly `0`; `F.logsigmoid` stays correct. `constructs.py` shows it: at `x = -200` the first gives `-inf`, the second `-200.0`. The student has `F` since Week 12. **Every Bradley-Terry and DPO loss today is `-F.logsigmoid(something).mean()`.** The minus sign is required (Mistake 5).

**(b) `F.log_softmax(scores, dim=-1)` — the log of the chances, straight from the scores.** It is Week 13's `F.softmax` followed by `ln`, in one safe step. `dim=-1` means "across the tokens, one row at a time" (Mistake 4 is `dim=0`). It gives you the **log-chance of every token**; the next construct picks one.

**(c) `logp.gather(1, index)` — in each row, pick the column named by the index.** `logp` has shape `(8, 12)`; `index` must have the same number of dimensions, `(8, 1)` (a column of column-numbers), not `(8,)` (Mistake 3), and every number in it must be a real column, so **`-100` cannot go in** (Mistake 2). The result is `(8, 1)`: the log-chance of the *right* token at each place. In `dpo.py` the same word on a 1-D tensor is `moved_up.gather(0, chosen)`: "from this list of four, take the ones named by `chosen`". *It is the same as fancy indexing* (`logp[0, 2]`), and `constructs.py` shows the two agreeing; the reason to learn `gather` is that it is the form that works on a whole batch of rows at once.

**(d) `tensor.detach()` — the same numbers, cut off from the graph.** `c = b.detach()` has `c.requires_grad == False`: a gradient will never flow *through* it. In DPO this is **the frozen reference model**: `ref_logp = F.log_softmax(policy_logits, dim=-1).detach()` is taken **once, before training**, so it stays at where the policy started while the policy itself moves. Forget it and you get Mistake 6 (a loud error); recompute it every step and you get Mistake 7 (a silent one). (Earlier teacher-only snippets in this course used `.detach()` quietly; it is **new to the student today**.)

> **Order to introduce them:** `log_softmax` (the student types it in `sftmask.py`), `gather` (same file), `logsigmoid` (`reward.py`), `detach` (`dpo.py`). One per step, each with a prediction first.

### 5. The other code the student types — nothing new, but note these

- **`F.cross_entropy(..., ignore_index=-100)`** (Week 12 used `PAD`; here the ignored label is `-100`, PyTorch's default — it is the same mechanism as the padding mask, and worth saying so).
- **`x[:, :4] = -100`** slice assignment on a `.clone()` (Week 3 for `.clone()`; slice assignment Level 3); **`.reshape(-1, V)`** (Level 3), `.tolist()`, `torch.allclose` (Week 8).
- **`X[a] @ w`** (a dot product; Level 3 Week 16), `torch.stack([...]).mean()` (Week 10), **`torch.tensor(v, dtype=torch.float32)`**, `torch.zeros(5, requires_grad=True)` (Week 2), Adam (Week 3), the loop `zero_grad / backward / step`.
- **`zip`, `sorted(..., key=lambda kv: -kv[1])`, dict comprehension, f-strings with `:+.3f`**: all Weeks 1-18.
- **`torch.tensor(START, requires_grad=True)`** as "the policy": a bare tensor of knobs with no `nn.Module`. (**`nn.Parameter` is Week 31**, so today's `dpo.py` deliberately builds the policy this way; the module used `nn.Parameter(ref_logits.clone())`.)
- **`torch.log`** (Week 12), **`math.exp`/`math.log`** (teacher-only `key.py`).

**`key.py` is teacher-only** (it uses `math` on purpose, to check torch). Everything else the student types, except that the student types the **mask** lines of `sftmask.py` and the **loop** of `dpo.py` and is *given* the rest.

**Not used today, on purpose:** `nn.Parameter` (Week 31), `torch.where` (Week 24: it would have fixed Mistake 8), `F.kl_div` and `F.binary_cross_entropy_with_logits` (two shortcuts for what we write by hand), `reduction="none"`, anything about PPO.

### 6. What the numbers will say

These are all printed by the files below. Read them before class so nothing surprises you.

- **The constructs (`constructs.py`).** `torch.log(torch.sigmoid(x))` at `x = -200` is `-inf`; `F.logsigmoid` gives `-200.0`. Rows of `log_softmax` exponentiate to chances adding to `1.0`. `gather` and indexing agree. `b.detach()` has `requires_grad` False and the same numbers.
- **The masked loss (`sftmask.py`).** `targets_sft: [[-100, -100, -100, -100, 4, 4, 1, 6]]`; loss over all 8 = **3.8008**; over the last 4 = **4.0407**. The by-hand route agrees with `cross_entropy` (`True True`), with per-position surprises `4.574, 1.972, 2.968, 4.729 | 4.111, 4.044, 3.102, 4.907`. (The sum of the last four, three-decimal rounded, is `16.164`, `4.041` after dividing: a rounding shadow of `4.0407`.)
- **The mask by characters (`pairs.py`).** 42 characters, prompt 30, answer 12; **12 of 41** guesses count. Not 12 of 42 (one fewer guess than characters) and not 13 (the first answer character is guessed from the last prompt character, so **that** guess counts). The last line is a **deliberate slip** shown for comparison: a mask one place too long leaves `11`.
- **KL on paper (`kl.py`).** `0.1733` and `0.4458`; `0.0000` for the reference against itself; `KL(p2||q) = 0.4458`, `KL(q||p2) = 0.4298`; the plain average `-0.1733`.
- **The reward model (`reward.py`).** Loss `0.6931`, `0.0135`, `0.0017` at steps 1, 100, 500. Weights `+5.047, +4.578, -2.794, -2.534, -6.091`. Ranking `r1 +9.625, r6 +7.091, r2 +4.578, r3 -0.750, r4 -2.794, r5 -6.091`; `10/10` pairs agree. The invented `r9` (only numbered steps) gets `+5.047` and **beats** `r2` (`+4.578`). All of these reproduced the module's printed numbers exactly (ledger `m04_05`).
- **The blind spot (`hack.py`).** `is_factually_correct` stays **`+0.000`**; the other five weights are identical to `reward.py`'s; `r7` (correct) and `r8` (wrong) both get `+9.625`. Ledger `m04_09` agrees.
- **DPO (`dpo.py`).** Reference `A=0.168 B=0.206 C=0.375 D=0.251`. At `beta = 0.2`: step 1 loss `0.6931`, step 50 `0.4529`, step 150 `0.2526`, step 300 `0.1424`, finishing at `A = 0.997`. Two leashes at 300 steps: `beta 0.10` -> `A=0.997`, KL `1.760`, loss `0.2560`; `beta 5.00` -> `A=0.589 B=0.236 C=0.144 D=0.032`, KL `0.566`, loss `0.0020`. **All of these reproduced the module's printed numbers exactly** (ledger `m04_06`).
- **The sweep (`sweep.py`, workbook only).** At 300 steps the KL is `1.213, 1.760, 1.709, 1.557, 0.566` for `beta = 0.02, 0.1, 0.5, 1.0, 5.0` — **not monotone**. At 3,000 steps it is `1.782, 1.782, 1.781, 1.772, 1.095`: smaller `beta` goes further, and the top of the range is `-ln(0.16839) = 1.7815`, the most KL the toy can reach (all the chance on A). This 3,000-step table is **this guide's own run; it is not in the module or the ledger.**
- **Hand numbers (`key.py`).** Bradley-Terry `0.9741`, `0.1269`; `0.6682, 0.6225, 0.9168`; `0.05215` / loss `2.954`; `0.0868`. DPO one pair `0.5759` at `beta 0.1`, `0.000004` at `beta 5`.

![Nine tokens in a row, five prompt and four answer, with eight guesses beneath them: the first four dashed and marked minus 100, the last four counted, and the two means 3.8008 and 4.0407](../figures/fig-w22-1-sft-loss-mask.svg)
*Figure 22.1 — SFT averages only the guesses whose right answer is in the answer, so its mean (4.0407) is over different guesses than the full mean (3.8008).*

![Two bars per outcome A to D for the reference q and the policy p1, the log-ratio and the weighted product under each, adding up to KL 0.1733](../figures/fig-w22-2-kl-by-hand.svg)
*Figure 22.2 — KL is the log-ratio of each outcome weighted by the new table's own chances; for p1 it adds to 0.1733.*

### 7. The honest limits of today

1. **No language model was involved.** Not one token of generated text. The masked loss is on random scores; the reward model on five typed features; DPO on four numbers. Each shows a mechanism and no more.
2. **The preference data is invented and perfectly consistent.** Real raters disagree. The module's Practice 6 (contradictions and cycles) shows what then happens: a contradiction reverts to the reference's own preference (`A=0.450 B=0.550`, loss `0.3395`); a perfect cycle leaves the policy **unmoved** at the reference, loss stuck at `0.6931` (ledger `m04_10`, not run today; a stretch item). **A DPO loss that sits at `0.6931` is telling you about your labels, not your optimizer.**
3. **One seed, one toy.** The reward model's weights and the DPO numbers do not depend on a random draw (they are deterministic given the start), but we did not vary the start scores or the pairs.
4. **"Mode collapse" is a toy fact** (section 3). We did not measure diversity of a real model.
5. **The `beta` story is subtle and partly contradicts the module.** The module says "at `beta = 5` the gradient dies and the policy barely moves; at `beta = 0.02` the loss keeps pushing." At 300 steps `beta = 0.02` has *not yet* collapsed (`A = 0.782`) and its KL is lower than `beta = 0.1`'s. At 3,000 steps the picture matches the module's intuition. We did not test beyond 3,000 steps, other learning rates, or other preference sets.
6. **A full DPO run uses the summed log-chance of a whole reply**, and the reference model is a second copy of the whole network. We did neither. The four-answer toy has one "sequence" per answer. (Background.)
7. **We did not run PPO or RLHF.** The PPO objective is in the README's "deliberately not in this level" list. Describe it in two sentences and stop.
8. **The SFT "instruction following" claim is not shown.** We show the *loss mask*, the single detail that makes SFT SFT; we did not fine-tune anything.
9. **Seeds and the `-100` convention.** `-100` is PyTorch's default `ignore_index`; we pass it explicitly.

### 8. The misconceptions you will actually meet

1. **"The mask removes the prompt from the input."** No: the model still *reads* the prompt (it is all in the input). The mask removes the **scoring** of the prompt's own tokens. Point at `targets_sft`: the inputs are unchanged, only the right answers were blanked.
2. **"Masked loss is lower, because it's cleaner."** Here it is higher. There is no rule; it is the average over a different set of guesses.
3. **"The reward model gives each answer a grade out of 10."** It gives a number whose **differences** mean something (`add 100` changes nothing). Compare two answers, never read one alone.
4. **"The biggest weight is the most important feature."** It is the feature the ten judgements most reliably agreed on. `has_numbered_steps` is `+5.047` because the winners mostly had steps. That is also exactly the property an optimizer would exploit (`r9`).
5. **"`logsigmoid` is just `log` of `sigmoid`, so why bother?"** Run `constructs.py`'s first lines: `-inf`.
6. **"DPO needs no data of the model's own."** It needs a frozen copy of itself; it needs no *reward model* and no sampling while training.
7. **"KL is a distance."** It is not symmetric (`0.4458` against `0.4298`). Also "KL = 0 means the models are identical": true, but KL is small and the models can still differ on a rare outcome.
8. **"The policy that moved further is the better one."** Nothing in the KL says better. `A = 0.997` is "very sure", not "right".
9. **"Smaller loss means the leash is working."** Mistake 9.

### 9. How deep to go, and where to stop

Stop at: *"SFT is next-token training that only scores the answer. A reward model learns a score from pairs, and the score can be gamed. DPO moves the model's own chances toward the chosen answers, measured against a frozen copy of where it started; KL says how far it moved, and `beta` says how soon the loss stops caring."* Do **not** go into PPO's clipping or value network, the derivation that DPO's loss is the optimal policy of the KL-penalised objective (the module states it; we do not prove it, and the README excludes proofs), the Bradley-Terry model's assumptions, inter-rater statistics (Week 30), length bias, constitutional methods, or how real raters are paid. If the student asks *"so is this how ChatGPT was made?"*: *"The reference module says the real recipe has these three stages, at a vastly bigger scale. We built the smallest version of each stage that fits on a laptop. We did not check how any product was made."* If they ask *"why does the reference model have to be frozen?"*: Mistake 7.

### 10. 🧭 Where Week 22 sits

```text
   W12  padding mask (ignore_index)       W22  after pretraining (today)
   W13  softmax, sampling                 -------------------------------------------------------------
   W17  TinyGPT: next-token loss          SFT: next-token loss, only on the answer   (-100 mask, gather)
   W21  pretraining, the scaling line     reward model: -ln sigmoid(r_win - r_lose)   (logsigmoid)
                                          DPO: move the model's own chances, leash beta, KL measured
                                                                              |
                                          W23  Prompting as engineering: a prompt is a test suite
                                          W24  learning in context (a small transformer you train)
                                          W27  Review and Assessment 3 (weeks 19-26)
                                          W30  do two raters (or a judge and a person) agree?  Cohen's kappa
                                          W31  fine-tuning cheaply: LoRA
```

---

## 🧰 Prep Checklist

### 35 minutes the night before

- [ ] **Confirm the stack.** Run from the folder you will work in:

```bash
python3 -c "import torch; print(torch.__version__)"
python3 -c "import torch, torch.nn.functional as F; print(F.logsigmoid(torch.tensor(-200.0)).item())"
```

You must see (the first line's digits may differ on another PyTorch version):

```text
2.2.1
-200.0
```

`pip` returning 403 is expected and not an error; **nothing this week installs anything.** Nothing this week imports `l4lib`.

- [ ] **Type the files below into one working folder.** Each begins with a `#` comment naming it. **The files are meant to be run in one session, in order** (`exec` them one after another, or run `python3 -i`), because `hack.py`, `sweep.py` and `key.py` use names made by the files before them; that is noted in each. `for f in ...; do python3 $f.py` also works for every file **except those three**. A ready one-liner is at the end of this list.

**File 1 — `constructs.py`** (the four new constructs, on numbers small enough to read)

```python
# constructs.py - Week 22: the four new constructs, each on numbers small enough to read.
import torch
import torch.nn.functional as F

torch.set_num_threads(1)

# (a) F.logsigmoid: the log of a sigmoid, kept safe when the sigmoid is tiny
x = torch.tensor([2.0, 0.0, -2.0, -50.0, -200.0])
print("torch.log(torch.sigmoid(x)):", [round(v, 3) for v in torch.log(torch.sigmoid(x)).tolist()])
print("F.logsigmoid(x)            :", [round(v, 3) for v in F.logsigmoid(x).tolist()])

# (b) F.log_softmax: log-chances over the last axis (one row per position)
scores = torch.tensor([[1.0, 2.0, 3.0],
                       [0.0, 0.0, 0.0]])
logp = F.log_softmax(scores, dim=-1)
print("\nlog-chances, row 0:", [round(v, 4) for v in logp[0].tolist()])
print("log-chances, row 1:", [round(v, 4) for v in logp[1].tolist()])
print("chances add to 1 per row:", F.softmax(scores, dim=-1).sum(dim=1).tolist())

# (c) torch.gather: in each row, pick the column named by the index
pick = torch.tensor([[2], [0]])                 # row 0: column 2, row 1: column 0
print("\ngather:", [round(v, 4) for v in logp.gather(1, pick).reshape(-1).tolist()], " (row 0 col 2, row 1 col 0)")
print("same by indexing:", [round(logp[0, 2].item(), 4), round(logp[1, 0].item(), 4)])

# (d) .detach(): the same numbers, cut off from the graph
a = torch.tensor([1.0, 2.0], requires_grad=True)
b = a * 2
c = b.detach()
print("\nb needs a gradient:", b.requires_grad, "  c = b.detach() needs one:", c.requires_grad, "  same numbers:", c.tolist())
```

```text
torch.log(torch.sigmoid(x)): [-0.127, -0.693, -2.127, -50.0, -inf]
F.logsigmoid(x)            : [-0.127, -0.693, -2.127, -50.0, -200.0]

log-chances, row 0: [-2.4076, -1.4076, -0.4076]
log-chances, row 1: [-1.0986, -1.0986, -1.0986]
chances add to 1 per row: [1.0, 1.0]

gather: [-0.4076, -1.0986]  (row 0 col 2, row 1 col 0)
same by indexing: [-0.4076, -1.0986]

b needs a gradient: True   c = b.detach() needs one: False   same numbers: [2.0, 4.0]
```

**File 2 — `sftmask.py`** (the same scores, scored two ways; then by hand with `gather`)

```python
# sftmask.py - Week 22: the same model output, scored two ways. Only the second is SFT.
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
torch.manual_seed(0)

V = 12                                     # pretend vocabulary size
logits = torch.randn(1, 9, V)              # pretend model output for 9 positions (random, NOT a model)
tokens = torch.tensor([[3, 7, 2, 9, 11, 4, 4, 1, 6]])
PROMPT_LEN = 5                             # the first 5 tokens are the prompt

preds = logits[:, :-1, :]                  # the answer at position t is a guess for token t+1
targets_all = tokens[:, 1:].clone()        # what each position should have guessed

# Route 1: F.cross_entropy, as in Week 12 (ignore_index skips rows)
loss_all = F.cross_entropy(preds.reshape(-1, V), targets_all.reshape(-1))

targets_sft = targets_all.clone()
targets_sft[:, :PROMPT_LEN - 1] = -100     # -100 means "skip this row"
loss_sft = F.cross_entropy(preds.reshape(-1, V), targets_sft.reshape(-1), ignore_index=-100)

print("targets_all:", targets_all.tolist())
print("targets_sft:", targets_sft.tolist())
print(f"loss over all 8 predictions   : {loss_all.item():.4f}")
print(f"loss over 4 response positions: {loss_sft.item():.4f}")

# Route 2: by hand, with log_softmax and gather.
rows = preds.reshape(-1, V)                       # (8, 12): one row of scores per position
logp = F.log_softmax(rows, dim=-1)                # each row becomes log-chances (they sum to 1 after exp)
want = targets_all.reshape(-1, 1)                 # (8, 1): the column we want in each row
picked = logp.gather(1, want)                     # (8, 1): log-chance of the right token, one per row
per_position = -picked.reshape(-1)                # (8,): the surprise at each position
print("\nper-position surprise:", [round(x, 3) for x in per_position.tolist()])
print("mean of all 8          :", round(per_position.mean().item(), 4))
print("mean of the last 4     :", round(per_position[PROMPT_LEN - 1:].mean().item(), 4))
print("same as cross_entropy? :", torch.allclose(per_position.mean(), loss_all),
      torch.allclose(per_position[PROMPT_LEN - 1:].mean(), loss_sft))
print("shapes:", tuple(logp.shape), tuple(want.shape), tuple(picked.shape))
```

```text
targets_all: [[7, 2, 9, 11, 4, 4, 1, 6]]
targets_sft: [[-100, -100, -100, -100, 4, 4, 1, 6]]
loss over all 8 predictions   : 3.8008
loss over 4 response positions: 4.0407

per-position surprise: [4.574, 1.972, 2.968, 4.729, 4.111, 4.044, 3.102, 4.907]
mean of all 8          : 3.8008
mean of the last 4     : 4.0407
same as cross_entropy? : True True
shapes: (8, 12) (8, 1) (8, 1)
```

The target lists are the ones the module prints. `logits` is `torch.randn`: **random, not a model.** That the last 4 average `4.0407` and all 8 average `3.8008` says nothing about SFT working.

**File 3 — `pairs.py`** (an SFT example made of characters, with its mask)

```python
# pairs.py - Week 22: an SFT example made of characters, with its mask. The prompt is typed by us, not a model.
import torch

PROMPT = "q: what runs past the town?\na:"      # what the user said
ANSWER = " the river.\n"                        # the ideal reply, typed by a person
text = PROMPT + ANSWER
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
ids = torch.tensor([stoi[c] for c in text])

targets = ids[1:].clone()                       # the guess at place t is for place t+1
targets[:len(PROMPT) - 1] = -100                # skip every guess whose right answer is still inside the prompt
print("characters:", len(text), " prompt:", len(PROMPT), " answer:", len(ANSWER))
print("guesses that count:", int((targets != -100).sum()), "of", len(targets))
print("the first guess that counts is for the character:", repr(text[len(PROMPT)]))
kept = [text[i + 1] for i in range(len(targets)) if targets[i] != -100]
print("the characters it is scored on:", "".join(kept).replace("\n", "\\n"))

late = ids[1:].clone()
late[:len(PROMPT)] = -100                       # DELIBERATE slip, for comparison: the mask one place too long
print("if the mask started one place late:", int((late != -100).sum()), "guesses would count")
```

```text
characters: 42  prompt: 30  answer: 12
guesses that count: 12 of 41
the first guess that counts is for the character: ' '
the characters it is scored on:  the river.\n
if the mask started one place late: 11 guesses would count
```

**File 4 — `kl.py`** (KL divergence is arithmetic on two tables)

```python
# kl.py - Week 22: KL divergence is arithmetic on two tables of chances. No training.
import torch

torch.set_num_threads(1)


def kl(p, q):
    """How far p has moved from q: the average of ln(p/q), averaged with p's own chances."""
    return (p * (torch.log(p) - torch.log(q))).sum().item()


q = torch.tensor([0.25, 0.25, 0.25, 0.25])     # the reference: four outcomes, all equally likely
p1 = torch.tensor([0.50, 0.25, 0.125, 0.125])  # a policy that has moved a little
p2 = torch.tensor([0.70, 0.10, 0.10, 0.10])    # a policy that has moved a lot

for name, p in [("p1", p1), ("p2", p2), ("q itself", q)]:
    logratio = (torch.log(p) - torch.log(q)).tolist()
    print(f"{name:9s} ln(p/q) per outcome: {[round(x, 4) for x in logratio]}   KL = {kl(p, q):.4f}")

# Two things to notice.
print("\nKL(p2 || q) =", round(kl(p2, q), 4), "   KL(q || p2) =", round(kl(q, p2), 4), "  (not the same number)")
unweighted = (torch.log(p1) - torch.log(q)).mean().item()
print("the plain average of ln(p1/q) (NOT weighted by p1):", round(unweighted, 4), " <- can be zero or negative; it is not KL")
```

```text
p1        ln(p/q) per outcome: [0.6931, 0.0, -0.6931, -0.6931]   KL = 0.1733
p2        ln(p/q) per outcome: [1.0296, -0.9163, -0.9163, -0.9163]   KL = 0.4458
q itself  ln(p/q) per outcome: [0.0, 0.0, 0.0, 0.0]   KL = 0.0000

KL(p2 || q) = 0.4458    KL(q || p2) = 0.4298   (not the same number)
the plain average of ln(p1/q) (NOT weighted by p1): -0.1733  <- can be zero or negative; it is not KL
```

**File 5 — `reward.py`** (a five-weight reward model from ten judgements, and the hack)

```python
# reward.py - Week 22: teach a tiny reward model from ten judgements. Five features, five knobs.
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
torch.manual_seed(1)

FEATS = ["has_numbered_steps", "gives_direct_answer", "hedges_a_lot", "over_400_chars", "refuses"]

POOL = {                        # six candidate answers, each written as five 0/1 features
    "r1": [1, 1, 0, 0, 0],      # numbered steps, direct, short
    "r2": [0, 1, 0, 0, 0],      # direct and short, no structure
    "r3": [0, 1, 1, 1, 0],      # direct but hedgy and long
    "r4": [0, 0, 1, 0, 0],      # hedgy and evasive
    "r5": [0, 0, 0, 0, 1],      # refuses a harmless question
    "r6": [1, 1, 0, 1, 0],      # numbered steps, direct, but long
}

# Ten hand-made judgements: (winner, loser)
PAIRS = [("r1", "r4"), ("r1", "r5"), ("r2", "r4"), ("r6", "r3"), ("r1", "r3"),
         ("r2", "r5"), ("r1", "r2"), ("r6", "r4"), ("r2", "r3"), ("r3", "r5")]

X = {name: torch.tensor(v, dtype=torch.float32) for name, v in POOL.items()}
w = torch.zeros(5, requires_grad=True)             # the reward model: one weight per feature
opt = torch.optim.Adam([w], lr=0.1)

for step in range(1, 501):
    # Bradley-Terry: -log sigmoid( reward(winner) - reward(loser) ), averaged over the pairs
    losses = [-F.logsigmoid(X[a] @ w - X[b] @ w) for a, b in PAIRS]
    loss = torch.stack(losses).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step in (1, 100, 500):
        print(f"step {step:4d}  BT loss {loss.item():.4f}")

print("\nlearned reward weights:")
for f, wi in zip(FEATS, w.detach()):
    print(f"  {f:22s} {wi:+.3f}")

scores = {k: (X[k] @ w).item() for k in POOL}
print("\nranking of every candidate:")
for k, v in sorted(scores.items(), key=lambda kv: -kv[1]):
    print(f"  {k}  reward {v:+.3f}   {POOL[k]}")
agree = sum(scores[a] > scores[b] for a, b in PAIRS)
print(f"\ntrain-pair agreement: {agree}/{len(PAIRS)}")

# The hack: an answer that is ONLY numbered steps (no direct answer at all).
POOL["r9"] = [1, 0, 0, 0, 0]
X["r9"] = torch.tensor(POOL["r9"], dtype=torch.float32)
scores["r9"] = (X["r9"] @ w).item()
print(f"\nr9 numbered steps, answers nothing: reward {scores['r9']:+.3f}  vs r2 direct and short: {scores['r2']:+.3f}")
print("r9 beats r2?", scores["r9"] > scores["r2"])
```

```text
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

r9 numbered steps, answers nothing: reward +5.047  vs r2 direct and short: +4.578
r9 beats r2? True
```

**File 6 — `hack.py`** (a feature the data never varies gets weight exactly zero) — *uses `POOL` and `PAIRS` from `reward.py`*

```python
# hack.py - Week 22: a feature that never varies inside a pair cannot be learned. (Needs reward.py's names: run it in the same session, or paste it below reward.py.)
import torch
import torch.nn.functional as F

torch.set_num_threads(1)
torch.manual_seed(1)

FEATS6 = ["has_numbered_steps", "gives_direct_answer", "hedges_a_lot", "over_400_chars", "refuses", "is_factually_correct"]
POOL6 = {name: v + [1] for name, v in POOL.items() if name != "r9"}   # every rated answer happened to be correct
POOL6["r7"] = [1, 1, 0, 0, 0, 1]      # same as r1, and correct
POOL6["r8"] = [1, 1, 0, 0, 0, 0]      # same as r1, and WRONG
X6 = {name: torch.tensor(v, dtype=torch.float32) for name, v in POOL6.items()}

w6 = torch.zeros(6, requires_grad=True)
opt6 = torch.optim.Adam([w6], lr=0.1)
for step in range(500):
    loss6 = torch.stack([-F.logsigmoid(X6[a] @ w6 - X6[b] @ w6) for a, b in PAIRS]).mean()
    opt6.zero_grad()
    loss6.backward()
    opt6.step()

for f, wi in zip(FEATS6, w6.detach()):
    print(f"  {f:22s} {wi:+.3f}")
print(f"\nr7 (correct)   reward {(X6['r7'] @ w6).item():+.3f}")
print(f"r8 (incorrect) reward {(X6['r8'] @ w6).item():+.3f}")
```

```text
  has_numbered_steps     +5.047
  gives_direct_answer    +4.578
  hedges_a_lot           -2.794
  over_400_chars         -2.534
  refuses                -6.091
  is_factually_correct   +0.000

r7 (correct)   reward +9.625
r8 (incorrect) reward +9.625
```

**File 7 — `dpo.py`** (DPO on a four-answer policy; `detach` and `gather`)

```python
# dpo.py - Week 22: DPO on a four-outcome toy policy. The "model" is four scores; nothing else.
import torch
import torch.nn.functional as F

torch.set_num_threads(1)

RESPONSES = ["A: numbered recipe, 6 lines, no filler",
             "B: correct recipe buried in 3 paragraphs of preamble",
             "C: vague answer that never lists ingredients",
             "D: refuses a harmless cooking question"]
START = [0.4, 0.6, 1.2, 0.8]                       # the SFT model's four scores
DPAIRS = [(0, 3), (0, 2), (0, 1), (1, 2), (1, 3), (2, 3)]   # (chosen, rejected), as answer numbers
chosen = torch.tensor([a for a, b in DPAIRS])
rejected = torch.tensor([b for a, b in DPAIRS])


def run_dpo(beta, steps, lr=0.05, trace=False):
    policy_logits = torch.tensor(START, requires_grad=True)          # the policy starts AS the reference
    ref_logp = F.log_softmax(policy_logits, dim=-1).detach()         # freeze a copy: no graph, no gradient
    opt = torch.optim.Adam([policy_logits], lr=lr)
    for s in range(1, steps + 1):
        logp = F.log_softmax(policy_logits, dim=-1)                  # log-chances of all four answers
        moved_up = logp - ref_logp                                   # how far each answer has moved from the reference
        margin = beta * (moved_up.gather(0, chosen) - moved_up.gather(0, rejected))
        loss = -F.logsigmoid(margin).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if trace and s in (1, 50, 150, 300):
            p = F.softmax(policy_logits, dim=-1).detach()
            print(f"  step {s:4d}  loss {loss.item():.4f}   probs " +
                  " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)))
    p = F.softmax(policy_logits, dim=-1).detach()
    logp = F.log_softmax(policy_logits, dim=-1).detach()
    kl = (p * (logp - ref_logp)).sum().item()                        # the same KL as kl.py, policy against reference
    return p, kl, loss.item()


ref_p = F.softmax(torch.tensor(START), dim=-1)
print("reference policy:", " ".join(f"{RESPONSES[i][0]}={ref_p[i]:.3f}" for i in range(4)))
print("\nbeta = 0.2, 300 steps:")
run_dpo(0.2, 300, trace=True)

print("\ntwo leashes, 300 steps each:")
for b in [0.1, 5.0]:
    p, k, l = run_dpo(b, 300)
    print(f"  beta {b:4.2f}  " + " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)) +
          f"   KL(pi||ref)={k:.3f}  loss={l:.4f}")
```

```text
reference policy: A=0.168 B=0.206 C=0.375 D=0.251

beta = 0.2, 300 steps:
  step    1  loss 0.6931   probs A=0.179 B=0.219 C=0.361 D=0.242
  step   50  loss 0.4529   probs A=0.519 B=0.461 C=0.013 D=0.006
  step  150  loss 0.2526   probs A=0.946 B=0.054 C=0.000 D=0.000
  step  300  loss 0.1424   probs A=0.997 B=0.003 C=0.000 D=0.000

two leashes, 300 steps each:
  beta 0.10  A=0.997 B=0.003 C=0.000 D=0.000   KL(pi||ref)=1.760  loss=0.2560
  beta 5.00  A=0.589 B=0.236 C=0.144 D=0.032   KL(pi||ref)=0.566  loss=0.0020
```

**File 8 — `sweep.py`** (workbook / fast student: the `beta` sweep at 300 steps and at 3,000) — *uses `run_dpo` and `RESPONSES` from `dpo.py`*

```python
# sweep.py - Week 22 (workbook / fast student): the beta sweep, then the same sweep run 10 times longer.
# Needs dpo.py's run_dpo in the same session.
import time
t0 = time.time()
print("300 steps:")
for b in [0.02, 0.1, 0.5, 1.0, 5.0]:
    p, k, l = run_dpo(b, 300)
    print(f"  beta {b:4.2f}  " + " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)) + f"   KL={k:.3f}  loss={l:.4f}")
print("3000 steps:")
for b in [0.02, 0.1, 0.5, 1.0, 5.0]:
    p, k, l = run_dpo(b, 3000)
    print(f"  beta {b:4.2f}  " + " ".join(f"{RESPONSES[i][0]}={p[i]:.3f}" for i in range(4)) + f"   KL={k:.3f}  loss={l:.4f}")
print(f"seconds: {time.time() - t0:.1f}")
```

```text
300 steps:
  beta 0.02  A=0.782 B=0.218 C=0.000 D=0.000   KL=1.213  loss=0.5317
  beta 0.10  A=0.997 B=0.003 C=0.000 D=0.000   KL=1.760  loss=0.2560
  beta 0.50  A=0.987 B=0.013 C=0.000 D=0.000   KL=1.709  loss=0.0513
  beta 1.00  A=0.950 B=0.047 C=0.003 D=0.000   KL=1.557  loss=0.0204
  beta 5.00  A=0.589 B=0.236 C=0.144 D=0.032   KL=0.566  loss=0.0020
3000 steps:
  beta 0.02  A=1.000 B=0.000 C=0.000 D=0.000   KL=1.782  loss=0.1310
  beta 0.10  A=1.000 B=0.000 C=0.000 D=0.000   KL=1.782  loss=0.0160
  beta 0.50  A=1.000 B=0.000 C=0.000 D=0.000   KL=1.781  loss=0.0014
  beta 1.00  A=0.999 B=0.001 C=0.000 D=0.000   KL=1.772  loss=0.0005
  beta 5.00  A=0.802 B=0.150 C=0.043 D=0.004   KL=1.095  loss=0.0000
seconds: 0.8
```

The 300-step rows are the module's sweep, reproduced exactly. **The 3,000-step rows are this guide's own extra run** (the `seconds:` line varies).

**File 9 — `key.py`** (teacher-only: every hand-arithmetic answer, computed) — *uses `kl`, `START`, `F` and `torch` from the files above*

```python
# key.py - Week 22: every hand-arithmetic answer in the workbook, computed. Nothing here is new teaching.
# Needs kl.py's kl, dpo.py's names (START, F, torch) in the same session.
import math

# ---- Page 22.2 (Bradley-Terry by hand): sigmoid of a reward gap, then -ln of it
def sig(x):
    return 1 / (1 + math.exp(-x))

print("BT: r(chosen)=0.3, r(rejected)=0.8 -> gap -0.5: sigmoid", round(sig(-0.5), 4), " loss", round(-math.log(sig(-0.5)), 4))
print("BT: gap +2.0: sigmoid", round(sig(2.0), 4), " loss", round(-math.log(sig(2.0)), 4))
R = {"a": 2.1, "b": 1.4, "c": -0.3, "d": 2.6}
print("P(a>b) =", round(sig(R["a"] - R["b"]), 4), " P(d>a) =", round(sig(R["d"] - R["a"]), 4), " P(a>c) =", round(sig(R["a"] - R["c"]), 4))
print("c>d: sigmoid(-2.9) =", round(sig(R["c"] - R["d"]), 5), " loss", round(-math.log(sig(R["c"] - R["d"])), 3),
      "  a>c loss", round(-math.log(sig(R["a"] - R["c"])), 4))
print("add 100 to every reward: P(a>b) =", round(sig((R["a"] + 100) - (R["b"] + 100)), 4))

# ---- Page 22.3: DPO on ONE pair, by hand. log pi_ref (chosen, rejected) = (-20, -18); log pi now = (-19, -19.5)
moved_w, moved_l = -19.0 - (-20.0), -19.5 - (-18.0)
print("\nDPO one pair: chosen moved", moved_w, " rejected moved", moved_l)
for beta in (0.1, 5.0):
    m = beta * (moved_w - moved_l)
    print(f"  beta {beta}: margin {m}   sigmoid {sig(m):.4f}   loss {-math.log(sig(m)):.4f}   torch: {-F.logsigmoid(torch.tensor(m)).item():.4f}  (six places: {-F.logsigmoid(torch.tensor(m)).item():.6f})")

# ---- Page 22.4: KL on paper
q = torch.tensor([0.25, 0.25, 0.25, 0.25])
p1 = torch.tensor([0.50, 0.25, 0.125, 0.125])
p2 = torch.tensor([0.70, 0.10, 0.10, 0.10])
print("\nKL(p1||q) by hand: 0.5*ln2 + 0 + 2*0.125*ln(0.5) =", round(0.5 * math.log(2) - 0.25 * math.log(2), 4), " code:", round(kl(p1, q), 4))
print("KL(p2||q) by hand: 0.7*ln(2.8) + 3*0.1*ln(0.4)   =", round(0.7 * math.log(2.8) + 0.3 * math.log(0.4), 4), " code:", round(kl(p2, q), 4))
print("pieces: ln(2.8) =", round(math.log(2.8), 4), " ln(0.4) =", round(math.log(0.4), 4), " ln(2) =", round(math.log(2), 4))
ref = F.softmax(torch.tensor(START), dim=-1)
print("\nreference chance of A, 5 places:", round(ref[0].item(), 5), " -ln of it (the most KL this toy can reach):", round(-math.log(ref[0].item()), 4))

# ---- Page 22.1: the masked loss, counted
print("\nmasked loss: 8 positions, 4 skipped. Sum of the last 4 =", round(sum([4.111, 4.044, 3.102, 4.907]), 3), " /4 =", round(sum([4.111, 4.044, 3.102, 4.907]) / 4, 4))
print("ln(12), the loss of a model that knows nothing about 12 tokens:", round(math.log(12), 4))
```

```text
BT: r(chosen)=0.3, r(rejected)=0.8 -> gap -0.5: sigmoid 0.3775  loss 0.9741
BT: gap +2.0: sigmoid 0.8808  loss 0.1269
P(a>b) = 0.6682  P(d>a) = 0.6225  P(a>c) = 0.9168
c>d: sigmoid(-2.9) = 0.05215  loss 2.954   a>c loss 0.0868
add 100 to every reward: P(a>b) = 0.6682

DPO one pair: chosen moved 1.0  rejected moved -1.5
  beta 0.1: margin 0.25   sigmoid 0.5622   loss 0.5759   torch: 0.5759  (six places: 0.575939)
  beta 5.0: margin 12.5   sigmoid 1.0000   loss 0.0000   torch: 0.0000  (six places: 0.000004)

KL(p1||q) by hand: 0.5*ln2 + 0 + 2*0.125*ln(0.5) = 0.1733  code: 0.1733
KL(p2||q) by hand: 0.7*ln(2.8) + 3*0.1*ln(0.4)   = 0.4458  code: 0.4458
pieces: ln(2.8) = 1.0296  ln(0.4) = -0.9163  ln(2) = 0.6931

reference chance of A, 5 places: 0.16839  -ln of it (the most KL this toy can reach): 1.7815

masked loss: 8 positions, 4 skipped. Sum of the last 4 = 16.164  /4 = 4.041
ln(12), the loss of a model that knows nothing about 12 tokens: 2.4849
```

- [ ] **Run the whole set in one session** and check nothing fails (about 1.7 seconds):

```bash
python3 -c "
import time
t0 = time.time()
for name in ['constructs', 'sftmask', 'pairs', 'kl', 'reward', 'hack', 'dpo', 'sweep', 'key']:
    exec(open(name + '.py').read())
print('all nine ran; total seconds:', round(time.time() - t0, 1))
" > /dev/null && echo OK
```

- [ ] **Print** workbook pages 22.1-22.6. Have a calculator with `ln` and `e^x` (a phone works; **airplane mode on**).
- [ ] **Do the two KL tables yourself**, once, on paper (section 2b), so you hold `0.1733` and `0.4458`; and the DPO one-pair arithmetic (section 2e), so you hold `0.25` and `12.5`.
- [ ] **Read the Debugging Clinic** and copy the nine `bad*.py` files to a scratch folder so they are ready to plant.

### 3 minutes on the day

- [ ] Open `sftmask.py` and `dpo.py` in the editor as **empty files**, for typing together. Have the others open in another tab.
- [ ] Put the calculator and the timer on the desk; write the five lesson-objective numbers (`3.8008`, `4.0407`, `+5.047`, `0.1733`, `0.997`) on a sheet **face down** for the wrap-up.

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Fall back to the paper work: the two KL tables (page 22.3) and the one-pair DPO arithmetic (page 22.3) need only a calculator; read the printed outputs in this guide for the rest. |
| `sftmask.py` prints different numbers from `3.8008` / `4.0407` | `torch.manual_seed(0)` must come **before** `torch.randn`, and `torch.set_num_threads(1)` is in the file. A different PyTorch build can move the last digit; the *shape* of the finding (two different numbers from one set of scores) is unchanged. |
| `reward.py` stops at a loss other than `0.0017` | A wrong seed (`manual_seed(1)` — though the model starts at zero so the seed barely matters), a sign slip (Mistake 5) or `lr` not `0.1`. Compare line by line with File 5. |
| `dpo.py`: `Trying to backward through the graph a second time` | `.detach()` is missing on `ref_logp` (Mistake 6). |
| `dpo.py` moves, but ends at `A=0.450 B=0.550` | The reference is being recomputed inside the loop (Mistake 7). |
| `KL(pi||ref)=nan` | You used `torch.log(p)` and some chance is exactly `0` (Mistake 8); use `F.log_softmax` as `dpo.py` does. |
| Different low digits on another machine | Expected. Use the `True`/`False` lines, the shapes, the ranking order and the pattern (bigger `beta` -> smaller KL at 300 steps), not the fourth decimal. |
| No laptop at all | Run the lesson from the printed outputs here, with the two paper tables and the one-pair DPO sum. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 6 | Ask the base model a question; it carries on instead of answering. Three fixes, three predictions. |
| 🧠 Concept | 12 | Mask the prompt (3) · a judge from pairs (4) · DPO, the frozen copy and KL on a napkin (5) |
| 💻 Live-code | 22 | `sftmask.py` (6) · `pairs.py` (3) · `reward.py` (7) · `dpo.py` (6) |
| 🎲 Their turn | 25 | The Leash: KL on paper (8), one DPO pair on paper (6), run two `beta` values (8), the question (3) |
| 🔑 Wrap & assign | 5 | What was shown and what was not; homework |

> **Timing note.** The hour is deliberately tight; Module 4 is compressed into three weeks and this is the crowded one. **The `beta` sweep (`sweep.py`) is not in class**: it goes to workbook page 22.4. If the hour is running long, drop `pairs.py` (the mask-by-characters, 3 min; it is page 22.1's second question) and `hack.py` (the student runs it as homework). **Never drop the KL arithmetic or the two-`beta` comparison**: they are the week.

### 🪝 Hook — A Model That Carries On (6 minutes)

**Do not open the laptop yet.**

1. **(2 min) The problem.** *"Imagine you have the best model we could build, pretrained like Week 21. You type: `q: what runs past the town?` and the next line is `a:`. What does a model trained only to guess the next character do?"* Draw it out: **it carries on in the style of the text**, maybe another question, maybe a list of questions. It has read a lot of text; nobody has asked it to *answer*. (Say plainly that we do not have a big model to show; this is a reasoned statement from what next-token training does, not a demo.)
2. **(2 min) Three fixes, one line each, on the board.**

```text
   SFT      show it good answers, and score ONLY the answer
   REWARD   it is easier to say "A is better than B" than to write a perfect A: learn a judge from pairs
   DPO      skip the judge; nudge the model's own chances toward the winners, on a leash
```

3. **(2 min) Three predictions on a card.** (a) *"The model guesses 8 characters; the first 4 are the question, the last 4 are the answer. Scored on all 8, or only on the last 4, which number is bigger?"* (b) *"A judge learns from ten pairs which answers people liked. Which single property of an answer do you think it will love most?"* (c) *"A model is told to move toward the winners, and we tie a string to it, so it can only move so far. Ties it tightly, it moves... ?"* Collect guesses. **Do not reveal.** (Typically: masked bigger or "no idea"; "correct"; "less".)

*If the student says "but we never built a chatbot":* agree. The lesson builds the three mechanisms as four-number toys and says so out loud.

### 🧠 Concept — Mask, Judge, Leash (12 minutes)

**(3 min) The mask.** Put a 9-place line on the board: `q : h i ? a : y e s` (invented). *"Next-token training: at each place, guess the next character. Place 1 guesses place 2, and so on. In SFT we keep that; but we only grade the guesses whose right answer is in the reply."* Underline the last four. *"The model still reads the question. We just do not grade it for writing the question; we want it to learn to answer, not to ask."* Then the off-by-one, slowly: **the guess at place `t` is for place `t+1`**, so with a 5-character prompt the guess at place 5 (the last prompt character) is already for the first answer character. Four guesses are prompt-only; the rest count. Write `-100` and say "PyTorch's word for *skip this row*; you used the padding version in Week 12".

**(4 min) The judge.** *"Writing a perfect answer is hard. Picking the better of two is quick. So people make pairs: winner, loser."* Write:

```text
   reward(answer) = a number;   we want reward(winner) > reward(loser)
   chance the winner wins = sigmoid( reward(winner) - reward(loser) )      <- Level 3 Week 13
   loss = -ln of that                                                      <- Level 3 Week 14
```

*"If the judge knows nothing, both rewards are 0, the chance is 0.5, and the loss is -ln 0.5. What number is that?"* (`0.6931`; they have it from Week 1: "a coin".) *"If the judge is sure and right, the chance is near 1 and the loss near 0. If it's sure and wrong, the loss is huge."* Say: **the judge is five weights, one per yes/no feature of an answer** (steps? direct? hedging? long? refuses?). **Do not show the weights.** Ask again: *"which feature will be biggest?"*

**(5 min) DPO and the leash.** *"Skip the judge. Keep a frozen photocopy of the model (the reference). Train the real one so that, for each pair, it has moved the winner up **more** than it has moved the loser, measured against the photocopy. If it moves a lot, that is a big change from the photocopy."* Then the napkin: *"How do we say 'how much has it moved'? Here are two tables of chances for four answers."* Write `q = 0.25 0.25 0.25 0.25` and `p = 0.5 0.25 0.125 0.125`. *"For each answer, how many times more likely did it get? 2, 1, half, half. In surprise-meter units, take the ln: +0.69, 0, -0.69, -0.69. Now average, but weight each by how often the **new** table picks it."* Compute it with the student: `0.5 x 0.69 - 0.125 x 0.69 x 2 = 0.1733`. **Name it:** *"That is KL divergence. Zero means no movement. It gets bigger the further it moves."* Stop. (Do **not** mention asymmetry; it is on the paper later.) Then one sentence on `beta`: *"The loss has a dial inside it, beta. We will try a small one and a big one and watch what happens to the model and to the KL."*

### 💻 Live-Code Together — `sftmask.py`, `pairs.py`, `reward.py`, `dpo.py` (22 minutes)

The student types. You narrate. **Nobody pastes.** `constructs.py` is for **you** to run beforehand and for the student to read in homework (page 22.6); use it live only if a construct gets stuck.

**Step 1 (6 min) — `sftmask.py`.** Type down to the first two `print`s. **Before running, hold up the prediction card (a).** Run: `3.8008` and `4.0407`. *"Two numbers from the same scores. Only one is SFT: which?"* (The second.) Make a point of it: **the masked one is higher, and that is fine** (section 8, 2). Then type the by-hand half: `log_softmax`, `want`, `gather`, `per_position`. Narrate **each shape** aloud and print them (`(8, 12) (8, 1) (8, 1)`). *"What would `gather(1, ...)` do if I told it column -100?"* (Crash: Mistake 2; show it now, it is 20 seconds.) The two `True`s at the end: *"the by-hand way and `cross_entropy` are the same thing."*

**Step 2 (3 min) — `pairs.py`.** Type the first ten lines; **predict** before the print: *"how many of the 41 guesses will count?"* (`12`: the answer is 12 characters, and each is guessed once.) *"Why 41 and not 42?"* (The last character has no next one.) Run. Point at `the first guess that counts is for the character: ' '` — the guess made from `:`, the last prompt character.

**Step 3 (7 min) — `reward.py`.** Give the student the data block (`FEATS`, `POOL`, `PAIRS`) already typed; they type the training loop (they know Adam loops) and **only one new line**: `-F.logsigmoid(X[a] @ w - X[b] @ w)`. **Predict step 1's loss** (`0.6931`; they argued why in the Concept). Run. Print the weights **slowly**. *"Which feature did the judge love most?"* (`has_numbered_steps`.) *"What is the shortest answer that gets that reward and nothing else?"* Type `r9 = [1, 0, 0, 0, 0]`: *numbered steps and no answer*. Run the last lines: `+5.047` beats `+4.578`. **Pause.** *"This is reward hacking. We did not program it; we found it by looking. Who has to look?"* Then run `hack.py` **only if time allows** (2 min): the sixth feature stays `+0.000`.

**Step 4 (6 min) — `dpo.py`.** Give the student `RESPONSES`, `START` and `DPAIRS` typed. They type **`ref_logp = ....detach()`** and the four lines of the loop body; you narrate `moved_up` and `gather`. **The key moment:** draw two boxes, `policy_logits` (with an arrow for the gradient) and `ref_logp` (no arrow). *"The reference is a snapshot taken once; `detach` cuts it off so nothing trains it."* Run the `beta = 0.2` trace: the probability of A climbs `0.179 -> 0.519 -> 0.946 -> 0.997`, C and D fall to zero. Ask: *"the photocopy preferred C (0.375), and nobody told the model A is correct. How did it find A?"* (Six pairwise preferences; A wins every pair it is in.)

### 🎲 Their Turn — The Leash (25 minutes)

The full rules are in *The Activity, In Full* below. The shape:

1. **(8 min) KL on paper** (page 22.3). The two tables of section 2b, with a calculator. They should get `0.1733` and `0.4458`; then the same table against itself (`0`); then a third table *of their own choice* for which they predict "bigger or smaller than 0.4458". Check with `kl.py`.
2. **(6 min) One DPO pair on paper.** The four numbers `-20, -18 | -19, -19.5`: chosen moved `+1.0`, rejected `-1.5`; at `beta = 0.1` margin `0.25`, loss `0.5759`; at `beta = 5` margin `12.5`, loss `0.000004`. *"Same movement. What did the loss do?"* (Fell to almost zero.) *"If the loss is almost zero, what does the gradient do?"* (Nearly nothing; the model stops being pushed.)
3. **(8 min) Run `run_dpo` at `beta = 0.1` and `5.0`** (they already have the function from the live-code; they type the two-line loop) and fill the table on page 22.4: `A`, KL, loss. They expect, from the paper work, that `beta = 5` moves less. It does: `A = 0.589`, KL `0.566`.
4. **(3 min) The question.** *"`beta = 5` has the smaller loss, `0.0020`, and the model moved less. Which model is better?"* No wrong answers to start; the lesson is that *the loss can't tell you*. Then: *"What would you look at instead?"* (The chance of the preferred answer, the KL, and most of all whether the preferences were right in the first place.)

**Stop at 25 minutes.** If the paper KL is unfinished, show `kl.py`'s output and move on. The student should leave having computed one KL by hand, seen one loss shrink while the model moved less, and found one hacked feature.

### 🔑 Wrap & Assign (5 minutes)

1. **(2 min)** Face-down sheet: *"Five numbers."* Turn it over: `3.8008 / 4.0407`, `+5.047`, `0.1733`, `0.997`. *"What was each?"* (All-8 and last-4 loss; the formatting weight; the KL on paper; the chance of A after DPO.) *"What did we **not** do?"* (Touch a language model; use real raters; run PPO.)
2. **(1 min)** *"Which of today's three toys could you break by giving it a bad dataset?"* (All of them; the point of Week 30.)
3. **(1 min)** Hand out the workbook.
4. **(1 min)** One sentence ahead: *"Next week the question changes: you are the user, and the model is a script. How do you test a prompt the way you test a function?"*

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code. **Paths will differ on your machine**; here they are shown as `/home/you/l4/`. Tracebacks from PyTorch run through several of its own files; the long middle of those is replaced by a line reading `... frames inside torch (elided) ...`, and **the last line is the real, complete last line**. Each mistake is deliberate: you plant it, the student reads the traceback (or the odd number) aloud, and you refuse to fix it until they have said what it means. Each block is **self-contained** so you can drop it in a scratch folder (none needs the Prep files). **Five of the nine are silent**, and the silent ones are the point.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (It says what went wrong; the lines above say where.) For a silent mistake: *"What did you expect this to print?"*
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the mask starts one place too late (SILENT)

```python
# DELIBERATE MISTAKE 1 (SILENT): the mask starts one place too late. The prompt is 5 tokens, but the
# guess at position t is for token t+1, so only the first 4 rows are prompt rows.
import torch
import torch.nn.functional as F

torch.manual_seed(0)
V = 12
logits = torch.randn(1, 9, V)
tokens = torch.tensor([[3, 7, 2, 9, 11, 4, 4, 1, 6]])
PROMPT_LEN = 5

preds = logits[:, :-1, :]
targets = tokens[:, 1:].clone()
targets[:, :PROMPT_LEN] = -100                     # <- should be :PROMPT_LEN - 1
loss = F.cross_entropy(preds.reshape(-1, V), targets.reshape(-1), ignore_index=-100)
print("targets:", targets.tolist())
print(f"loss: {loss.item():.4f}   (Week 22's masked loss is 4.0407)")
```

```text
targets: [[-100, -100, -100, -100, -100, 4, 1, 6]]
loss: 4.0174   (Week 22's masked loss is 4.0407)
```

**Read it:** no error, and `4.0174` is a believable loss. But look at `targets`: **five** `-100`s, and the first answer character (`4`) has gone. The prompt is 5 tokens, but the guess at place `t` is for token `t+1`, so the first **4** rows are prompt rows; masking 5 throws away the first guess at the answer. **Fix:** `targets[:, :PROMPT_LEN - 1]`. The clue is to *print the targets*, which the module's own code does. A good question: *"how many guesses should count?"* (4; it shows 4 only after the fix.)

### Mistake 2 — `gather` given a `-100` (loud)

```python
# DELIBERATE MISTAKE 2: gather with the masked targets. -100 is not a column of the table.
import torch
import torch.nn.functional as F

torch.manual_seed(0)
V = 12
rows = torch.randn(8, V)
targets = torch.tensor([-100, -100, -100, -100, 4, 4, 1, 6])     # already masked for cross_entropy
logp = F.log_softmax(rows, dim=-1)
picked = logp.gather(1, targets.reshape(-1, 1))                  # <- gather has no "ignore" option
print(picked.shape)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 10, in <module>
    picked = logp.gather(1, targets.reshape(-1, 1))                  # <- gather has no "ignore" option
RuntimeError: index -100 is out of bounds for dimension 1 with size 12
```

**Read it:** `gather` takes column numbers, and `-100` is not a column of a 12-column table. `cross_entropy(..., ignore_index=-100)` knows to skip those rows; `gather` does not. **Fix:** gather with the *unmasked* targets (`targets_all`, as `sftmask.py` does), then drop the prompt rows by slicing: `per_position[PROMPT_LEN - 1:]`. The clue is `out of bounds for dimension 1 with size 12`.

### Mistake 3 — `gather` given a flat list (loud)

```python
# DELIBERATE MISTAKE 3: gather with a wrong-shaped index (a flat list where gather wants a column).
import torch
import torch.nn.functional as F

torch.manual_seed(0)
V = 12
rows = torch.randn(8, V)
targets = torch.tensor([7, 2, 9, 11, 4, 4, 1, 6])
logp = F.log_softmax(rows, dim=-1)
picked = logp.gather(1, targets)                                 # <- should be targets.reshape(-1, 1)
print(picked.shape)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 10, in <module>
    picked = logp.gather(1, targets)                                 # <- should be targets.reshape(-1, 1)
RuntimeError: Index tensor must have the same number of dimensions as input tensor
```

**Read it:** `logp` has two axes `(8, 12)`; the index has one `(8,)`. `gather` wants the same number of axes: an `(8, 1)` column. **Fix:** `targets.reshape(-1, 1)`. The clue is `same number of dimensions`.

### Mistake 4 — `log_softmax` over the wrong axis (SILENT)

```python
# DELIBERATE MISTAKE 4 (SILENT): log_softmax over the wrong axis. Rows are positions, columns are tokens.
import torch
import torch.nn.functional as F

torch.manual_seed(0)
V = 12
rows = torch.randn(8, V)
targets = torch.tensor([7, 2, 9, 11, 4, 4, 1, 6])
good = F.log_softmax(rows, dim=-1)                               # each ROW sums to 1 once exponentiated
bad = F.log_softmax(rows, dim=0)                                 # <- each COLUMN sums to 1 instead
print("row sums of the chances, good:", [round(x, 3) for x in F.softmax(rows, dim=-1).sum(dim=1).tolist()][:4], "...")
print("row sums of the chances, bad :", [round(x, 3) for x in F.softmax(rows, dim=0).sum(dim=1).tolist()][:4], "...")
print("loss, good:", round(-good.gather(1, targets.reshape(-1, 1)).mean().item(), 4))
print("loss, bad :", round(-bad.gather(1, targets.reshape(-1, 1)).mean().item(), 4))
```

```text
row sums of the chances, good: [1.0, 1.0, 1.0, 1.0] ...
row sums of the chances, bad : [0.951, 1.608, 1.56, 1.53] ...
loss, good: 3.8142
loss, bad : 3.4502
```

**Read it:** both versions run and give loss-looking numbers. Only the row sums give it away: with `dim=-1` each **row** (one position) adds to 1 (`[1.0, 1.0, 1.0, 1.0]`); with `dim=0` each **column** (one token across all positions) does, and the rows add to `0.951, 1.608, ...`. The "loss" `3.4502` is lower than `3.8142` and is a number about nothing. **Fix:** `dim=-1`. The habit to teach: *after `softmax`, add up one row and see 1.*

### Mistake 5 — the minus sign on the reward loss is lost (SILENT)

```python
# DELIBERATE MISTAKE 5 (loud after a warning): the sign of the reward loss is lost. Winner and loser are the right way round.
import torch
import torch.nn.functional as F

torch.manual_seed(1)
X = {"win": torch.tensor([1.0, 1.0]), "lose": torch.tensor([0.0, 1.0])}
w = torch.zeros(2, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
for step in range(1, 201):
    loss = F.logsigmoid(X["win"] @ w - X["lose"] @ w)            # <- the minus sign is missing: -F.logsigmoid(...)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step in (1, 50, 200):
        print(f"step {step:4d}  loss {loss.item():+.4f}   reward(win) {(X['win'] @ w).item():+.3f}   reward(lose) {(X['lose'] @ w).item():+.3f}")
```

```text
step    1  loss -0.6931   reward(win) -0.100   reward(lose) +0.000
step   50  loss -5.2841   reward(win) -5.390   reward(lose) +0.000
step  200  loss -21.1251   reward(win) -21.228   reward(lose) +0.000
```

**Read it:** `loss` goes **negative** and keeps falling; `reward(win)` is pushed **down**, to `-21.228`, while `reward(lose)` stays at `0`. The loop is *maximising* the gap by making the loser's lead bigger. `-ln(sigmoid(gap))` is a positive number that we minimise; `ln(sigmoid(gap))` is negative and minimising it does the opposite. **Fix:** `-F.logsigmoid(...)`. The clue is `loss -0.6931` on step 1: *"a loss is never negative; what is `ln 2` with the wrong sign?"*

### Mistake 6 — the frozen reference kept its graph (loud)

```python
# DELIBERATE MISTAKE 6: the frozen reference kept its graph, and was computed once outside the loop.
import torch
import torch.nn.functional as F

policy_logits = torch.tensor([0.4, 0.6, 1.2, 0.8], requires_grad=True)
ref_logp = F.log_softmax(policy_logits, dim=-1)                  # <- missing .detach()
opt = torch.optim.Adam([policy_logits], lr=0.05)
chosen, rejected = torch.tensor([0, 0]), torch.tensor([3, 2])
for step in range(1, 4):
    logp = F.log_softmax(policy_logits, dim=-1)
    moved = logp - ref_logp
    loss = -F.logsigmoid(0.1 * (moved.gather(0, chosen) - moved.gather(0, rejected))).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
    print("step", step, "loss", round(loss.item(), 4))
```

```text
step 1 loss 0.6931
Traceback (most recent call last):
  File "/home/you/l4/bad6.py", line 14, in <module>
    loss.backward()
  ... frames inside torch (elided) ...
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.
```

**Read it:** step 1 worked; step 2's `backward()` fails: the reference `ref_logp` was built from `policy_logits` **with** a graph, and the first `backward()` freed that graph. (The message mentions `retain_graph=True`; **do not** take that advice: it would keep the reference connected to the policy and train it along with everything else, which is the opposite of frozen.) **Fix:** `.detach()` at the end of the line. The clue is `backward through the graph a second time`.

### Mistake 7 — the "frozen" reference recomputed every step (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): the "frozen" reference is recomputed from the policy every step.
import torch
import torch.nn.functional as F

policy_logits = torch.tensor([0.4, 0.6, 1.2, 0.8], requires_grad=True)
opt = torch.optim.Adam([policy_logits], lr=0.05)
chosen, rejected = torch.tensor([0, 0, 0, 1, 1, 2]), torch.tensor([3, 2, 1, 2, 3, 3])
for step in range(1, 301):
    logp = F.log_softmax(policy_logits, dim=-1)
    ref_logp = F.log_softmax(policy_logits, dim=-1).detach()     # <- the reference moves with the policy
    moved = logp - ref_logp
    loss = -F.logsigmoid(0.2 * (moved.gather(0, chosen) - moved.gather(0, rejected))).mean()
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step in (1, 300):
        p = F.softmax(policy_logits, dim=-1).detach()
        print(f"step {step:4d}  loss {loss.item():.4f}  probs", [round(x, 3) for x in p.tolist()])
```

```text
step    1  loss 0.6931  probs [0.179, 0.219, 0.361, 0.242]
step  300  loss 0.6931  probs [0.45, 0.55, 0.0, 0.0]
```

**Read it:** the first line is right: step 1, loss `0.6931`, probabilities `0.179 0.219 0.361 0.242` — the same as `dpo.py`. But the loss **never leaves `0.6931`**, and at step 300 the probabilities are `[0.45, 0.55, 0.0, 0.0]` — **B above A**, which the six preferences say is wrong (`dpo.py` ends at `A = 0.997`). Each step the "reference" is a photocopy of *now*, so `moved` is exactly `0`, the margin is `0`, and `sigmoid(0) = 0.5` forever; the gradient never shrinks because the loss never gets satisfied. There is no leash because there is no fixed thing to be far from. **Fix:** compute `ref_logp` **once, before the loop**. The clue: *a loss that is exactly `ln 2` at step 300 while the probabilities have moved.*

### Mistake 8 — KL with `torch.log(p)` and a chance of exactly zero (loud, in its own way)

```python
# DELIBERATE MISTAKE 8: KL with torch.log(p) when a chance has fallen to exactly zero.
import torch
import torch.nn.functional as F

logits = torch.tensor([0.0, 0.0, -200.0, 0.0])                   # one answer is now impossible to 32-bit precision
ref = F.softmax(torch.tensor([0.0, 0.0, 0.0, 0.0]), dim=-1)
p = F.softmax(logits, dim=-1)
print("p:", p.tolist())
print("ln(p):", torch.log(p).tolist())
print("KL =", (p * (torch.log(p) - torch.log(ref))).sum().item())
```

```text
p: [0.3333333432674408, 0.3333333432674408, 0.0, 0.3333333432674408]
ln(p): [-1.0986123085021973, -1.0986123085021973, -inf, -1.0986123085021973]
KL = nan
```

**Read it:** `ln(0)` is `-inf`, and `0 x -inf` is `nan`, and one `nan` makes the whole sum `nan`. No error: a `nan`. (We met it for real: our own first `dpo.py` printed `KL=nan` for `beta = 0.02` at 3,000 steps, when the losing answers' chances reached exactly `0`.) **Fix:** take the log-chances from `F.log_softmax` (a large negative number, never `-inf`), as `dpo.py` does: `(p * (logp - ref_logp)).sum()`. The honest maths is "`0 x ln 0` counts as `0`"; the code trick is to never form `ln 0`.

### Mistake 9 — judging the leash by the loss (SILENT)

```python
# DELIBERATE MISTAKE 9 (SILENT): judging a leash by the loss. Same ten-fold more steps, two betas: whose loss is smaller?
import torch
import torch.nn.functional as F

def run(beta, steps):
    logits = torch.tensor([0.4, 0.6, 1.2, 0.8], requires_grad=True)
    ref = F.log_softmax(logits, dim=-1).detach()
    opt = torch.optim.Adam([logits], lr=0.05)
    chosen, rejected = torch.tensor([0, 0, 0, 1, 1, 2]), torch.tensor([3, 2, 1, 2, 3, 3])
    for _ in range(steps):
        moved = F.log_softmax(logits, dim=-1) - ref
        loss = -F.logsigmoid(beta * (moved.gather(0, chosen) - moved.gather(0, rejected))).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    p = F.softmax(logits, dim=-1).detach()
    return loss.item(), p[0].item()

for beta in (0.1, 5.0):
    loss, pa = run(beta, 300)
    print(f"beta {beta}: final loss {loss:.4f}   chance of the best answer A: {pa:.3f}")
print("the smaller loss belongs to the model that moved LESS.")
```

```text
beta 0.1: final loss 0.2560   chance of the best answer A: 0.997
beta 5.0: final loss 0.0020   chance of the best answer A: 0.589
the smaller loss belongs to the model that moved LESS.
```

**Read it:** `beta = 5` has the smaller loss (`0.0020` against `0.2560`) and the model that is **further from done** (`A = 0.589` against `0.997`). The loss was *satisfied early* (section 2e: margin `12.5`), so the gradient went quiet. Different `beta`, different loss scale: **never compare losses across `beta`.** **Fix:** none needed in the code; the fix is in what you report: the chance of the preferred answer and the KL, beside the loss.

---

## 🎲 The Activity, In Full

### The Leash

**What it is:** the student does, by hand, the one piece of new maths (KL on two tables), then the one piece of DPO arithmetic (a single pair at two `beta`s), and only then runs the toy, so that the two numbers that come out (`0.997` and `0.589`) are *predictions confirmed*, not surprises.

### Setup (2 minutes, during the live-code segment)

- Page 22.3 (the four tables and the pair). A calculator with `ln`.
- A strip of paper with the rule written at the top: **KL = add up, over the four outcomes: (chance in `p`) x ln( chance in `p` / chance in `q` )**.
- Two 4-outcome tables (the student sees them as rows A-D):

```text
          A      B      C      D
   q   0.25   0.25   0.25   0.25      the reference
   p1  0.50   0.25   0.125  0.125     moved a little
   p2  0.70   0.10   0.10   0.10      moved a lot
```

### The rules, read out loud before round one

1. The **reference** `q` is always the second table; the policy is first.
2. Work in natural logs (`ln`, not `log10`), **4 decimals**.
3. Write the four log-ratios first, then multiply each by the policy's own chance, then add.
4. You may use the calculator for `ln` only.

### The five rounds

| Round | Policy | Reference | Answer | What to draw out |
|:--:|---|---|:--:|---|
| 1 | `p1` | `q` | **`0.1733`** | Log-ratios `+0.6931, 0, -0.6931, -0.6931`; products `+0.3466, 0, -0.0866, -0.0866`. The negatives are smaller because `p` weights them by their *new, smaller* chances. |
| 2 | `p2` | `q` | **`0.4458`** | Log-ratios `+1.0296, -0.9163 x 3`. *"Moved more, bigger number."* |
| 3 | `q` | `q` | **`0`** | Every log-ratio is `0`. *"No movement is zero."* |
| 4 | `q` | `p2` (swap!) | **`0.4298`** | Log-ratios are the *negatives* of round 2's, but weighted by `0.25`, not by `p2`'s. *"Not the same as 0.4458: it matters who goes first."* |
| 5 | **their own table** (four numbers that add to 1) | `q` | **check with `kl.py`** | Predict first: bigger or smaller than `0.4458`? **Compute the answer in `kl.py` first, with their numbers, so you can check them.** |

Then the DPO pair, with the same four numbers for both `beta`s (page 22.3, part B):

```text
   reference log-chance (chosen, rejected) = (-20.0, -18.0)
   policy now                               = (-19.0, -19.5)
   chosen moved +1.0   rejected moved -1.5   gap = 2.5
   beta 0.1:  margin 0.25   sigmoid 0.5622   loss 0.5759
   beta 5.0:  margin 12.5   sigmoid 1.0000   loss 0.000004
```

### The question that makes the activity

*"The movement is the same in both lines. Only `beta` changed. Which line still wants the model to move?"* (The first: a loss of `0.58` is far from satisfied; the second is already at `0.000004`.) *"So which model ends up further from the reference after the same number of steps?"* (The first; `0.997` and KL `1.760` against `0.589` and `0.566`.) And the honest second half: *"Is the further-moved model better?"* (We do not know. It is more sure of A. That is all the numbers say.)

### What "finished" looks like

Rounds 1-4 within `0.001` of the key; the one-pair loss at both `beta`s; a table with two `beta` rows filled from the student's own run; and the student saying "same movement, a bigger `beta` is satisfied sooner, so it stops sooner and the KL is smaller".

### Variation — easier

Do rounds 1 and 3 only (the first table and "no movement is zero"), and give the student the four log-ratios of round 2 so that they only weight and add. For the pair, do `beta = 0.1` only and read `beta = 5` from the key.

### Variation — harder

Round 6: the student constructs a table `p` whose KL from `q` is **as large as they can make it with no zero entries**, and says what happens as a chance goes to `0`, or to `1` (it tends to `-ln(0.25) = 1.386`, the most this `q` allows: all the chance on one outcome). **Compute their table's KL in `kl.py` before you tell them it is right.** Or run `sweep.py` and have them predict, before running, whether `beta = 0.02` beats `beta = 0.1` at 300 steps (it does not: `1.213` against `1.760`), and at 3,000 (they tie at `1.782`).

---

## ❓ Questions Students Ask This Week

**"Why mask the prompt? Doesn't the model learn from the questions too?"** It can, and in our toy nothing stops us; the reference module's reason is that we want it to learn to *produce the answer given the prompt*, not to imitate users, and that scoring the prompt would be wasted effort. We did not run a comparison of the two training regimes, so this is the module's reasoning, not our result.

**"Why is the masked loss bigger?"** Different set of guesses. Here it is only because the last four random guesses happened to score worse. It would be the other way with other random numbers.

**"Why `-100`?"** It is PyTorch's default for `ignore_index`. Any number that is not a real token id would do, and the padding mask of Week 12 is the same mechanism.

**"Why is a reward model trained on *pairs*, not scores out of 10?"** Module reasoning: people are more consistent at picking the better of two than at agreeing on a number. We did not test that; we have no raters.

**"Where do the ten judgements come from?"** We made them up. Say so. The point of the exercise is to see what a *fitted* judge looks like, not to claim these are real preferences.

**"Does the reward model really like numbered steps?"** This one does, because in our pairs the winners mostly had steps. The module notes that real reward models were observed to like certain openings and lengths; that is background from the module, not a measurement here. A fine question back: *"what pair would you add to teach it that steps alone are not enough?"* (Try one pair: `r9` loses to `r2`. **Train it in `reward.py` first and report what moves**; this guide did not run that variant.)

**"Why does `is_factually_correct` stay at zero?"** Every pair compares two answers with the same value for it, so the *difference* is 0 in all ten pairs, so the gradient for that weight is exactly 0, so Adam never moves it. The data never asked. Add one pair that differs **only** in that feature and it would move; we did not run that, but the module states it.

**"Is DPO the same as the reward model?"** The module says that if the reward model is Bradley-Terry and the objective is reward-minus-KL, the optimal policy has a closed form and the reward model can be skipped. We do not prove it. What you *see* in `dpo.py` is the same `logsigmoid` of a gap, but the gap is now measured in the policy's own log-chances, against a frozen copy.

**"Why does `beta` make the loss smaller?"** Because the loss is `-logsigmoid(beta x gap)`; bigger `beta`, bigger number inside, closer to `sigmoid = 1`, smaller loss. It does not mean a better model. (Mistake 9.)

**"What is `beta` in a real model?"** The module's value in its hand example is `0.1`. Typical values in practice were not checked here; do not say.

**"Why does KL depend on the order?"** The weights (`p`'s own chances) belong to the first table. `0.4458` against `0.4298`. In DPO the policy is first.

**"Can KL be negative?"** No (in exact arithmetic it is zero or more). A negative number means you forgot to weight by `p` (`kl.py`'s last line prints `-0.1733` for the plain average) or made an arithmetic slip.

**"So is this RLHF?"** No. RLHF (with PPO) would *sample* answers from the policy and score them with the reward model, every step. We did neither. The module describes it; we did not run it.

**"Can I try it on my TinyGPT?"** Yes, as homework for the flying student (see Differentiation), but **nothing in the lesson depends on it and nothing in this guide was run on TinyGPT**: a real SFT on the Week 17 model is a Week 24-style project and a slow one.

---

## ⚠️ Where This Lesson Goes Wrong

1. **The student thinks the mask changes the input.** Show `targets_sft` against `targets_all` and that `preds` is the same object in both calls.
2. **Off by one in the mask** (Mistake 1). The clinic is the cure. Make them say "the guess at place `t` is for place `t+1`" aloud.
3. **The student reads `0.6931` as "a bug".** It is `ln 2`: no idea which is better. The same number appears in Weeks 1 and 10; it is good to see it again. Bugs live in Mistakes 5 and 7, where it is *stuck* or has the wrong sign.
4. **KL arithmetic slips.** The usual ones: `log10` instead of `ln` (gives `0.0753` for round 1: `0.1733 / 2.3026`); forgetting to weight by `p` (plain average, `-0.1733`); weighting by `q` instead of `p` (swapped order, round 4's `0.4298`); using the ratio `p/q` instead of its `ln`.
5. **The student treats the hack as a joke.** `r9` scoring higher than `r2` is funny for ten seconds. Keep going: *"who would notice, in a thousand answers?"*
6. **Time.** The hour is too full. The first thing to drop is `pairs.py`, the second is `hack.py`. **Not** the KL, **not** the two `beta` values.
7. **The student runs `sweep.py` in class** because it is in the folder. It takes under 2 seconds; the reason not to is that the hour is full and the interesting bit (300 steps against 3,000) is a workbook question. If they do, use it.
8. **The student stops at "`beta = 5` has the lower loss, so it's better."** Mistake 9. Do not accept the first answer to the closing question.
9. **A hand-typed `nn.Parameter` or `nn.Module` policy.** That is Week 31. Keep the policy as `torch.tensor(START, requires_grad=True)`.
10. **The student says "the AI learned to prefer A".** The toy's four numbers moved. Nothing has preferences but the pairs we typed.

---

## 🧭 Differentiation

### If the student is struggling

- Do only **round 1** of the KL and the one-pair DPO at `beta = 0.1`. Run `dpo.py` once at `beta = 0.1`, and read `beta = 5` from the printed output.
- Skip `gather` by hand: use `cross_entropy(..., ignore_index=-100)` only, and show `pairs.py` so the mask is visible as characters. (The student has met `ignore_index`.)
- Demo Mistake 7 instead of explaining `detach` in words: the stuck `0.6931` teaches it faster.

### If the student is flying

- Run **`hack.py`** and `sweep.py`, then ask them to **add a pair that fixes the hack** to `reward.py` (`r9` loses to `r2`), train, and report what the weights become. **This guide did not run that variant; let them run it and report what they measure, and check it against the full-run pattern yourself.**
- Ask: *"Which `beta` gives the largest KL at 300 steps?"* (`0.1`: `1.760`.) *"At 3,000?"* (All of the small ones tie, near `1.78`.) *"Why can't KL go past `1.7815`?"* (It would need more than all the chance on A.) Have them derive `-ln(0.16839)`.
- Ask for the **contradiction and the cycle** (module Practice 6): a pair `(0,1)` and `(1,0)` -> `A=0.450 B=0.550`; a cycle -> unmoved at `0.6931`. **Ledger `m04_10`; not run in this lesson.** They should run it and compare with the ledger values.
- Optional, honest project: build an SFT batch from the student's **own Week 17 corpus** (prompt = a sentence start, answer = its end), mask it as in `pairs.py`, and compare the loss of TinyGPT scored over all characters against scored over the answer only. **Not run for this guide; nothing depends on it. If they do it, the model is a pretrained-on-a-tiny-corpus TinyGPT, not an assistant.**

### If the student won't engage today

Make the hack personal: give them a one-line list of five features of their own (*"has an emoji, is short, says sorry, uses capital letters, ends with a question"*), and ask which they think a reward model would most reward. **Then work out together how you would test it with ten made-up pairs, in `reward.py`.** Run the results as a class.

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"Why do we mask the prompt in SFT, and what is masked?"** *Pass:* the model still reads the prompt; only the scoring of the prompt's own tokens is skipped, so that it is trained to produce answers, not questions. The guesses whose right answer lies in the prompt get `-100`.
2. **"What does the reward model's loss say when it knows nothing, and why?"** *Pass:* `0.6931` (`ln 2`): both rewards equal, so the chance the winner wins is `0.5`.
3. **"What is reward hacking, and what did we see?"** *Pass:* an answer that scores high on the judge without being good; `r9`, just numbered steps, outscored a short direct answer because the biggest weight was formatting.
4. **"What does KL divergence measure and when is it zero?"** *Pass:* how far a policy's chances have moved from a reference's, as the `p`-weighted average of `ln(p/q)`; zero only when the two tables are equal.
5. **"What did `beta` change?"** *Pass:* a bigger `beta` makes the loss satisfied by less movement, so the model moves less (less KL) and the loss number is smaller; the loss is therefore not comparable across `beta`s.

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Builds the mask without the off-by-one; computes both KLs and the asymmetry; explains why the smaller-loss model is not better; names a hack and the mechanism (an unvaried feature gets weight 0); says "toy" without being prompted. |
| **3 — Secure** | Reproduces `3.8008` / `4.0407`; computes `0.1733` and `0.4458`; reads `has_numbered_steps` as the hacked feature; runs DPO at two `beta`s and says the bigger one moved less. |
| **2 — Developing** | Does the KL with help on the weighting; runs the code; says the lower loss is better; cannot say what `detach` is for. |
| **1 — Not yet** | Cannot say why the prompt is masked or what `-100` does. Repeat `pairs.py` and round 1 of the Leash at the start of Week 23 and do not build on today's words until the student can say "the model reads the prompt, we just do not score it." |

---

## 📤 Homework to Assign

The workbook has six pages (22.1-22.6). The student does them in order, and writes **predictions before running anything**.

1. **22.1 Mask** — predict, then run, the two losses in `sftmask.py` with a *different* prompt length (their choice, 3 to 7); count the guesses that count by hand for the character example; say what changes if the mask starts one place late (the Mistake 1 number).
2. **22.2 Judge** — Bradley-Terry by hand: four rewards, three probabilities, one confident mistake (`2.954`), and "add 100 to every reward"; then one run of `reward.py` and the five weights copied out.
3. **22.3 Leash** — the KL rounds on paper (1 to 5) and the one-pair DPO at `beta = 0.1` and `5`, checked with `kl.py` and `key.py`.
4. **22.4 Two leashes** — the `beta` table: run `run_dpo` at `0.02, 0.1, 0.5, 1.0, 5.0` for 300 steps, fill `A`, KL and loss, say which column is **not** comparable across rows, then rerun at 3,000 steps and say what changed.
5. **22.5 Hack** — add a seventh candidate answer to `reward.py` that beats a short direct one while answering nothing; then run `hack.py` and say why `is_factually_correct` stays at zero.
6. **22.6 Write-up** — one page, "What a toy showed and what it did not": what the student measured today in each of the three toys, one sentence on each of **what it does not tell us about a real assistant**, and the four new constructs explained in their own words (with `constructs.py` run and its four outputs copied out).

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated.

Estimated time: 60-75 minutes.

---

## 🔑 Answer Key

> **The workbook pages 22.1-22.6 follow this order.** Where an answer is a number it comes from `sftmask.py`, `pairs.py`, `kl.py`, `reward.py`, `hack.py`, `dpo.py`, `sweep.py` or `key.py`, all run from the Prep Checklist.

### Page 22.1 — Mask (from `sftmask.py`, `pairs.py`)

| Question | Answer |
|---|---|
| In `sftmask.py`, how many guesses are there for 9 tokens? | 8 (the last token has no next one). |
| How many are prompt-only when the prompt is 5 tokens? | 4 (the fifth prompt token's guess is already for the first answer token). |
| Loss over all 8 / over the last 4 | `3.8008` / `4.0407`. |
| Which is the SFT loss? | The second. |
| Why is the second bigger? | Different set of guesses; random scores; no rule. |
| `pairs.py`: how many guesses count? | 12 of 41. |
| With the mask one place too long (the last line of `pairs.py`) | `11` guesses count; the first answer character is lost (Mistake 1). |
| What are the shapes of `logp`, `want`, `picked`? | `(8, 12)`, `(8, 1)`, `(8, 1)`. |
| Why can `gather` not take `-100`? | It is not a column number (Mistake 2). |

### Page 22.2 — Judge (from `key.py`, `reward.py`)

| Question | Answer |
|---|---|
| Gap `-0.5` (chosen `0.3`, rejected `0.8`): chance, loss | `0.3775`, `0.9741`. |
| Gap `+2.0`: chance, loss | `0.8808`, `0.1269`. |
| `P(a beats b)`, `P(d beats a)`, `P(a beats c)` | `0.6682`, `0.6225`, `0.9168`. |
| Loss when `c` beats `d` is the verdict | `sigmoid(-2.9) = 0.05215`; loss `2.954`. |
| Loss when `a` beats `c` | `0.0868`. The ratio is about 34. |
| Add 100 to every reward | All three chances unchanged (`0.6682` etc.): only differences matter. |
| `reward.py`: loss at steps 1, 100, 500 | `0.6931`, `0.0135`, `0.0017`. |
| The five weights | `+5.047, +4.578, -2.794, -2.534, -6.091`. |
| Which features raise reward / lower it? | Steps and direct answer raise; hedging, length and refusing lower. |
| Agreement with the ten pairs | `10/10`. |
| The ranking | `r1 +9.625`, `r6 +7.091`, `r2 +4.578`, `r3 -0.750`, `r4 -2.794`, `r5 -6.091`. |

### Page 22.3 — Leash (from `kl.py`, `key.py`)

| Question | Answer |
|---|---|
| KL `p1` against `q` | `0.1733` (`0.25 ln 2`). |
| KL `p2` against `q` | `0.4458` (`0.7 ln 2.8 + 0.3 ln 0.4`). |
| KL `q` against `q` | `0`. |
| KL `q` against `p2` | `0.4298`. |
| Plain average of `ln(p1/q)` | `-0.1733` (not KL). |
| The maximum KL from this `q` | tends to `-ln(0.25) = 1.3863` (all the chance on one outcome). |
| Chosen / rejected moved | `+1.0`, `-1.5`. |
| Margin, loss at `beta = 0.1` | `0.25`, `0.5759` (the module prints `0.5757`; rounding). |
| Margin, loss at `beta = 5` | `12.5`, `0.000004`. |
| What happened to the loss with the same movement? | Fell to almost zero: the loss is satisfied, so the gradient is almost zero. |

### Page 22.4 — Two leashes (from `dpo.py`, `sweep.py`)

| `beta` | A (300 steps) | KL (300) | loss (300) | A (3000) | KL (3000) |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.02 | 0.782 | 1.213 | 0.5317 | 1.000 | 1.782 |
| 0.1 | 0.997 | 1.760 | 0.2560 | 1.000 | 1.782 |
| 0.5 | 0.987 | 1.709 | 0.0513 | 1.000 | 1.781 |
| 1.0 | 0.950 | 1.557 | 0.0204 | 0.999 | 1.772 |
| 5.0 | 0.589 | 0.566 | 0.0020 | 0.802 | 1.095 |

- The column that is **not** comparable across rows: the **loss** (the scale of the number inside `logsigmoid` depends on `beta`).
- Reference: `A=0.168 B=0.206 C=0.375 D=0.251`. At `beta = 0.2`, 300 steps: `A=0.997`, loss `0.1424`.
- *"What changed at 3,000 steps?"* Small `beta`s now all sit near `1.78`, the top of the range; `beta = 5` is still climbing. The 300-step row is a snapshot of a race, not a result about `beta`.
- *"Which answer did the reference prefer, and which does the policy pick?"* `C` (`0.375`) against `A`.
- The 3,000-step columns are this guide's own run; the 300-step columns are the module's, reproduced.

### Page 22.5 — Hack (from `reward.py`, `hack.py`)

| Question | Answer |
|---|---|
| `r9 = [1, 0, 0, 0, 0]` reward | `+5.047`. |
| Compare with `r2` (`+4.578`) | `r9` wins. |
| Why is that a hack? | It has only the biggest-weight feature, and answers nothing. |
| `is_factually_correct` weight after training | `+0.000`. |
| `r7` and `r8` rewards | both `+9.625`. |
| Why zero? | Every pair compares two answers that are both correct, so the feature's difference is 0 in all ten pairs and its gradient is exactly 0. |
| How would you fix it? | Add a pair that differs **only** in correctness. (Module statement; not run here.) |

Model answers to the open questions on this page are judged against the rubric below; there is no single right second hack.

### Page 22.6 — Write-up (rubric)

Full marks need: (1) the student's own four numbers from today, each with a seed; (2) one sentence per toy saying what it shows **and what it does not** (no real model, invented preferences, four numbers for a policy); (3) the loss-across-`beta` trap in their own words; (4) the four constructs explained correctly (`logsigmoid` stays finite where `log(sigmoid)` gives `-inf`; `log_softmax` gives log-chances along `dim=-1`; `gather` picks one column per row and needs a column index; `detach` cuts the graph, used for the frozen reference). Deduct for: "DPO is better than RLHF" (not tested), "the model learned to prefer" (four numbers moved), "lower loss is better".

### Teacher-only: the map of wrong answers on the KL rounds

| Wrong answer | Likely cause |
|---|---|
| `0.0753` (round 1) | `log10` instead of `ln` (`0.1733 / 2.3026`). |
| `-0.1733` (round 1) | Plain average of the four log-ratios, not weighted by `p`. |
| `0.4298` for round 2 | The two tables swapped (that is round 4's answer). |
| `0.6931` or `1.0296` | Stopped after the first row, or forgot to add. |
| `+0.4458` but `-0.4458` shown | Sign of `ln(0.4)` dropped. |
| A KL of `nan` in code | `torch.log` of an exact zero (Mistake 8). |

### Answers to every question posed in the lesson

| Question | Answer |
|---|---|
| Scored on all 8, or only the last 4, which is bigger? | Here the last 4 (`4.0407` against `3.8008`); nothing general. |
| Which number is SFT? | The masked one. |
| Why 41 guesses for 42 characters? | The last character has no next. |
| What does a judge that knows nothing score? | `0.6931` (`ln 2`). |
| Which feature did the judge love most? | `has_numbered_steps` (`+5.047`). |
| What stops the reference moving? | `.detach()`. |
| How did the policy find A, which nobody named? | A wins every pair it is in. |
| Same movement, bigger `beta`: what happens to the loss? | Nearly zero; the gradient dies. |
| Which model is better? | The loss cannot say. Look at the chance of the preferred answer, the KL, and whether the pairs were right. |
| What did we not do? | Use a language model, real raters, or PPO. |

---

## 🔮 Next Week Preview

**Week 23 — Prompting as Engineering: The Harness.** The student stops training models and starts *testing* them. A prompt loop is a test suite: a frozen set of cases, a versioned prompt, a call, a parse, a score and a regression report. The rung gets steeper in syntax: `@dataclass`, a class with `__init__`, `try` / `except` with a custom exception, and `re.search(..., re.S)`. **No new maths.** The "model" in Week 23 is a **scripted stand-in from the shared kit (`l4lib.fakellm`)**, labelled "stand-in, not a model" wherever it appears; what the harness measures says nothing about a real model. (Week 24 then trains a real, small one.) The baseline is a constant answer (the Week 1 lesson that `0.693` is a coin, applied to a test set). **For the student:** finish the workbook, especially 22.4 (the `beta` table) and 22.6, and bring the one sentence from the Wrap: *"the loss cannot tell you which model is better."* **For you:** Week 23 opens with "freeze the eight cases **before** you write the prompt", and today's reward model is the cautionary tale for why.
