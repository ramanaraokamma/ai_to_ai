# Week 27 — Review and Assessment 3: What Did Term 3 Leave Behind?

[⬅ Week 26](week-26.md) · [Course Home](../README.md) · [Week 28 ➡](week-28.md) · [Student Guide](../student-guide/week-27.md) · [Workbook](../workbook/week-27.md)

![Level 4 map: Week 27 highlighted among 36 week tiles in four term lanes](../figures/fig-w27-0-where-this-fits.svg)
*Figure 27.0 — Week 27 is the assessment tile that closes the third lane: an X-ray of Weeks 19 to 26 before the agents of Term 4.*


---

## 📋 At a Glance

This table gives the shape of the week in one place: timing, what is assessed, what is deliberately absent, and what you need to print.

| | |
|---|---|
| **Duration** | 75 minutes in class (2 to settle, 70 for the paper, 3 to hand in), then the marking homework (~45 min) |
| **Type** | 🟥 Assessment — **no new material at all.** Weeks 19-26 on paper, no computer. |
| **Big idea** | Same as Weeks 9 and 18, one term later: the paper is not a grade; it is a **map**. It finds, week by week, what stuck and what did not, so that the per-week remediation table tells the student which page to redo *before* Term 4 builds on it. **Weeks 28-29 (agents) lean directly on Week 23 (the harness, the floor, the budget guard), Week 26 (chunks, citations, the gate, "retrieved text is data") and, through them, on Week 25 (cosine) and Week 20 (counting tokens).** |
| **New vocabulary** | **None.** (If you catch yourself teaching a word today, stop: it is not on the paper.) |
| **New maths** | **None.** The paper *tests* the hand-calculable ideas of Term 3: cosine (W25), KL divergence and the Bradley-Terry loss (W22), the log-log slope and `C = 6ND` (W21), bytes per token (W20) and counting against a floor (W23, W26). Each is in the 🔢 section below, worked for you first. |
| **New syntax** | **None.** Every line of code on the paper uses a construct from Weeks 1-26, listed in section 4. |
| **The paper** | 75 marks. **A** 20 multiple choice (1 each) · **B** 8 "what does this print" (2 each) · **C** 4 "find the bug" (3 each) · **D** 3 arithmetic (5 each) · **E** 1 extended question on two real tables (12). Printed in full in [The Paper, in Full](#-the-paper-in-full) below; the key is at the bottom. |
| **Dataset** | None run by the student. Section E prints two real tables as numbers: Week 19's five-way ablation of the TinyGPT (800 steps) and Week 26's recall table on the 15-note notebook. **Nothing downloads. No internet.** |
| **Model** | Real PyTorch and numpy on the CPU, used by *you* in the prep to confirm the numbers the paper quotes from Weeks 22 and 26. **The Week 23 scripted client (`FakeClient`) and Week 26's sentence-copier appear on the paper only as named stand-ins, in words ("stand-in, not a model"). Nothing scored against them says anything about a real model, and the paper says so.** |
| **Materials** | The printed paper (one copy, single-sided) · the printed **marking sheet** (Marking Sheet 1, the one page you may hand over afterwards) · a pen · a calculator with `ln`, `e^x`, `log` (base 10) and a power key (a phone in calculator mode is fine; **airplane mode on**) · scrap paper · a timer · the per-week grid and remediation table (pages 27.2, 27.3) |
| **Prep time** | 30 minutes the night before (printing, reading the key, one 2-second prep run) · 3 minutes on the day |
| **Expected runtime of the code** | The **whole** prep (every block in the Prep Checklist, one session) runs in about **2 seconds** of wall time (measured 1.8 s, most of it importing torch). **No block takes over 10 seconds**, so nothing needs a recorded time; Week 19's 3.6-minute ablation table is deliberately **not** re-run (see section 3). Anything over **1 minute** means something is wrong (see Fallback). The *student* runs no code today. |

> **⚠️ Watch out:** four things go wrong this week.
>
> - **The teacher rescuing the student mid-paper** (as in Weeks 9 and 18). A frown at question 7 changes a right answer. Your job for 70 minutes is to be a quiet adult in a chair.
> - **Reading Term 3's toys as more than they are.** Section E invites the student to say that a recall of 1.00 means the system "works", or that a no-mask loss of 0.077 means the mask was a mistake. The key gives credit for the *opposite* reading. The honest reading is narrower than either: the first is a number about questions written in the notebook's own words, the second is a model reading its own answer.
> - **Marking by the final number only** (see the marking rules).
> - **Thin cover on Weeks 20, 21 and 24** (4 to 8 marks each), so a low fraction there is one or two questions. Read it as a prompt to ask, not a verdict (section 6, item 2).

---

## 🎯 Lesson Objectives

By the end of the lesson the student has, **with no computer and no notes:**

1. **Read an ablation table honestly**: say why the no-mask row is a leak, why "deleting it made it better" is one small model on two seeds, and what a switch-off test adds to a head's name. *(Week 19)*
2. **Say what a tokenizer does and compute what it saves**: a byte-level BPE merges the most common neighbouring pair; bytes per token rises as merges are learned. *(Week 20)*
3. **Use a log-log line and the `6ND` rule** without pretending an extrapolation is a measurement. *(Week 21)*
4. **Read the three fine-tuning toys**: the masked loss is a different number, not a worse model; a reward model's differences carry the meaning; `beta` is a leash and KL is how far you went. *(Week 22)*
5. **Treat a harness as an instrument**: a floor, a frozen set, a guard that stops one call late, and a stand-in that proves nothing about real models. *(Week 23)*
6. **Say what in-context examples and a logit mask do and do not do** (weights do not change; shape is guaranteed, sense is not). *(Week 24)*
7. **Do a cosine by hand, pick the top k, and read recall@k with the question "who wrote the questions?"**, and know that a valid citation only proves the writer named a note it was handed. *(Weeks 25-26)*

Observable evidence: a scored paper; a filled **per-week mark grid** (Marking Sheet 2); and, most important, **a remediation table with at most two weeks circled** for the student to redo during the following fortnight — and, as the README asks, the **recall table re-run with a changed chunk size** (homework, section "Homework to Assign").

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist**, in the **🐞 Debugging Clinic** and in **The Paper** was run, in order, in one Python session with one thread and the seeds shown; the outputs below are the real printed output. The Clinic blocks that are *deliberate mistakes* are marked and their tracebacks are real. The code inside the paper is the very same text that the key runs. **Every number repeated exactly on a second run on the same machine** (the only seeded randomness is `torch.manual_seed` inside the Week 22 toy, which is deterministic). Different CPU or PyTorch build: the last digit of a loss can move. **The Section E tables that go on the paper are printed numbers, so they do not depend on your laptop at all** — print them, do not re-generate them on the day.

### 1. What the student is doing today, in one paragraph

Nothing new. For 70 minutes the student answers a paper about the last eight weeks: twenty multiple-choice questions (one each), eight short programs whose output they must say, four short programs with a bug they must find and fix, three pieces of arithmetic (a cosine by hand, a KL divergence, a tokenizer-and-scaling triple) and one longer question built on **two real tables printed from this course's own runs**. They may use a calculator. They may not use a computer, notes, or you. Afterwards they are handed the *marking sheet*, mark their own paper in a different colour of pen as homework, fill the per-week grid, circle the (at most two) weeks to redo, and re-run Week 26's recall table at a chunk size it did not use.

Why on paper? Because the standard of the whole year — *you can say what a program will print before you run it* — is best tested with the laptop closed. Why self-marking? Because comparing their own working to the sheet is the best 45 minutes of review on offer, which is why the sheet shows working and not just answers.

### 2. 🔢 The maths you need — taught to you first

**There is no new idea.** But you will mark five hand-calculations and a dozen printed numbers, so do each of these yourself, once, with a calculator, *before* class. Block P5 computes all of them.

**(a) Cosine by hand (Week 25), Question D1.** Three invented 3-number vectors: `u = [2, 1, 2]`, `v = [1, 2, 2]`, `w = [2, -1, 0]`. The dot product multiplies place by place and adds: `u·v = 2·1 + 1·2 + 2·2 = 8`, `u·w = 2·2 + 1·(-1) + 2·0 = 3`. The lengths are `sqrt(4+1+4) = 3`, `sqrt(1+4+4) = 3`, `sqrt(4+1+0) = 2.236`. The cosine is dot over product of lengths: `cos(u, v) = 8 / (3 × 3) = 0.889`, `cos(u, w) = 3 / (3 × 2.236) = 0.447`. So `v` is nearer to `u` than `w` is. (Week 25's warning stands: a cosine ranks; it does not say "89% similar".)

**(b) KL divergence (Week 22), Question D2.** Two tables of chances over three outcomes: `p = [0.6, 0.3, 0.1]`, `q = [0.3, 0.3, 0.4]`. The KL of `p` from `q` is the sum over outcomes of `p × ln(p / q)`: `0.6 × ln 2 = 0.4159`, `0.3 × ln 1 = 0`, `0.1 × ln 0.25 = -0.1386`; the sum is **0.2773**. Against itself every ratio is 1, `ln 1 = 0`, so **KL(p‖p) = 0**. Swapped, `q × ln(q / p)`: `0.3 × ln 0.5 = -0.2079`, `0`, `0.4 × ln 4 = 0.5545`; the sum is **0.3466**, **not the same** (KL is not symmetric; Week 22's `0.4458` against `0.4298`). Note that single terms can be negative; the *sum* cannot.

**(c) Bytes per token, the log-log slope, and `6ND` (Weeks 20-21), Question D3.** (a) A text of 2,400 bytes that becomes 800 tokens gives `2400 / 800 = 3.0` bytes per token; more merges make the same text fewer tokens, so the number **rises**. (b) Three models: `N = 10^4, 10^5, 10^6` knobs with losses `9.0, 3.0, 1.0`. On log-log paper the x-steps are `4, 5, 6` and the y-values are `log10 9 = 0.954`, `log10 3 = 0.477`, `log10 1 = 0`. Each step up loses `0.477`: the slope is **-0.477**, and the three points are exactly on a line. (c) One more step (`N = 10^7`) multiplies the loss by `10^-0.477 = 1/3`: a predicted **0.333**. (d) `C ≈ 6ND = 6 × 10^6 × 2×10^7 = 1.2×10^14` FLOPs.

**(d) Counting against a floor (Weeks 23, 26), Questions A12, A20, E.** 50.0% of 32 fields is 16; 43.8% is 14; so 2 fields better. With ten questions one question is `0.10`, so `0.90` against `1.00` is **one question**.

**(e) The Bradley-Terry loss (Week 22), Question B4.** `-ln sigmoid(0) = ln 2 = 0.6931` (two equal rewards), and for a winner 2 ahead, `sigmoid(2) = 0.8808`, `-ln 0.8808 = 0.1269`. (B4 prints the first as a `logsigmoid`, which is the *negative* of the loss: `-0.6931`.)

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| Every number in the Week 26 half of Section E (the recall rows and the chunking table) | **Real and re-run tonight.** Block P2 re-executes Week 26's own blocks from its guide and prints the same lines. |
| The Week 22 numbers quoted in A9 and A11 (`3.8008`, `4.0407`, the two `beta` rows) | **Real and re-run tonight** (Block P4). |
| The Week 19 table in Section E (five ablations at 800 steps, two seeds) | **Real, quoted from the Week 19 guide, NOT re-run.** The full table is a 3.6-minute run and is a single-seed number that would be printed on the paper anyway; re-running it would only risk a last-digit difference. The paper prints it. |
| The Week 23 figures in A12 and A14 (`50.0%`, `43.8%`, `14 of 32`) | **Real, quoted from the Week 23 guide; the arithmetic is checked in Block P6.** The Week 23 guide's own block cannot be re-executed by a line-based extractor (one of its strings contains a code fence), so it was not re-run here. |
| Every "what does this print" output (Section B) and every error (Section C, Clinic) | **Real.** Produced by running the code below. |
| The hand-arithmetic answers (Section D) | **Computed twice:** by hand in section 2, and by numpy in Block P5. They agree. |
| The vectors and tables in D1-D3 | **Chosen by us** so the arithmetic is easy. Not learned, not measured. |
| `FakeClient`, the sentence-copier writer, and anything "scored" by them (A14, A19, E(c)) | **Stand-ins, not models.** The paper labels them. Results against them say nothing about a real model. |
| The pass mark (45 of 75) | **A proposal**, the same as Weeks 9 and 18. The README leaves the pass mark to the owner (Open Questions). Nothing in this file depends on 45. |

> **Say to the student, out loud, before they start:** *"Everything on this paper is something you have already done with your own hands. It is not a race and it is not a grade. It is an X-ray. If a question looks strange, read it twice, write down what you do know, and move on."*

> **🚫 What you must NOT claim about Section E.** (1) **Not** "removing the mask made the model 20 times better": `0.077` against `1.673` is a model reading the answer it is asked to predict (its sample is `tatatattt...`); the leak test in Week 19 made it a measurement. (2) **Not** "layer norm is useless": the no-norm model scored *better* on validation at both seeds (`1.478`, `1.453` against `1.673`, `1.643`), with a much larger train-to-validation gap, and **the Week 19 guide says plainly that we did not find out why.** (3) **Not** "RAG recall is 1.00": it is `1.00` on ten questions written after reading the notes and `0.20` on the same ten facts in a stranger's words. (4) **Not** "the 250-word chunks are best because recall is 1.00 at every k": they send 718 words, 104% of the notebook, so the retriever has stopped choosing.

### 4. The constructs the paper uses — all old, none new

Nothing is new this week. For your reference, here is **every** construct the paper leans on and the week it came from, so you can check "nothing is used before its week" at a glance:

| Week | Construct on the paper | Where |
|:--:|---|---|
| 1-8 | `for ... in range(...)` · `print` · `round` · `.item()` · `torch.tensor` · `torch.zeros` · `torch.optim.SGD` · `requires_grad=True` · `.backward()` | B1, B4, C1 |
| 6 | `x + f if residual else f` (a conditional expression; Level 2) and the residual road, in words | B1 |
| 12-13 | `F.softmax(x, dim=-1)` · `.argmax()` | B6 |
| 20 | `collections.Counter` · `.most_common` · slicing `s[i:i+2]` · a list comprehension · `str.replace` *(Counter is Week 20; the list comprehension is Level 2)* | B2 |
| 21 | `np.polyfit(x, y, 1)` · `np.log10` | B3, D3 |
| 22 | `F.logsigmoid` · `.detach()` *(described, not called)* | B4, C1 |
| 23 | a class with `__init__` and `self` · `try` / `except MyError` with `raise` · `re.search(..., re.S)` | B5, C2 |
| 24 | `torch.where(cond, a, b)` | B6 |
| 25 | `@` on arrays · `np.sqrt` · `np.argsort(-s)[:k]` *(written by the student in Week 26; met in Week 25)* · `axis=1, keepdims=True` *(Level 3 Week 32's normalise)* | B7, C3 |
| 26 | `np.argsort(-s)[:k]` · `re.findall(r"\[(\d+)\]", t)` · set operations `-` and `<=` | B7, B8, C4 |

**Teacher-only code.** The prep blocks use `re`, `exec`, `contextlib.redirect_stdout`, `io.StringIO`, `tempfile` and `os.chdir` to re-run earlier guides' own code and print only the lines the paper quotes. They are plumbing for *you*, **flagged `TEACHER-ONLY` where they appear,** and are not on the student's ladder. The paper's own code uses none of them.

Not on the paper, on purpose, because they are later rungs: tools and the agent loop (Week 28), traces and `k(k+1)/2` (Week 29), anything from Weeks 28 onwards. **If a student writes "agent", "tool call" or "injection defence" anywhere, do not mark it wrong and do not mark it extra; it is from next term.** ("Injection" itself appeared lightly in Week 26 and is fair game in A19.)

### 5. What the numbers will say

These are printed by the prep blocks. Read them before class so nothing surprises you.

- **Section B.** B1 `1.331 0.001` · B2 `[('aa', 4), ('ab', 2)]` and `XabdXabac` · B3 `-0.301 64` · B4 `-0.6931 0.1269` · B5 `stopped at call 3 spent 1.2` · B6 `3 0 0.0` · B7 `0.96` and `[1 2]` · B8 `['2', '7'] False {'7'}`.
- **Section C.** C1 ends `-18.64 -17.64` (the loser is 18.64 *ahead*, and the loss is **negative**); C2 raises `AttributeError: 'NoneType' object has no attribute 'group'`; C3 prints `[3. 1.] [0]` (note 0 wins by length); C4 prints `[2 0 4] [0.   0.05 0.12]` (the three *lowest*).
- **Section D.** D1 `0.889`, `0.447`. D2 `0.2773`, `0.0`, `0.3466`. D3 `3.0`, `-0.477`, `0.333`, `1.2e+14`.
- **Section E, the ablation (Week 19, 800 steps, validation):** full `1.673`, no mask `0.077`, no positions `1.739`, no residual `2.679`, no norm `1.478`; seed 1: `1.643`, `0.085`, `1.717`, `2.711`, `1.453`.
- **Section E, recall (Week 26):** your wording `1.00 / 1.00 / 1.00`, stranger `0.20 / 0.50 / 0.60`; chunking rows as in the paper. **The homework sweep** (Block P3): 20 words/5 overlap `0.60 / 0.90 / 1.00` sending 9% of the notebook; 45/10 `0.90 / 1.00 / 1.00` at 20%; 90/20 `1.00 / 1.00 / 1.00` at 39%.
- **Week 22 numbers quoted on the paper:** masked loss `4.0407` against unmasked `3.8008`; `beta 0.10`: `A = 0.997`, KL `1.760`, loss `0.2560`; `beta 5.00`: `A = 0.589`, KL `0.566`, loss `0.0020`.

### 6. The honest limits of today

1. **One paper is one sample.** A student who is ill, hungry or anxious scores lower than they know. Treat 45 as a prompt for a conversation, never a verdict. The *pattern across weeks* carries the information; the total barely does.
2. **Three weeks are thin.** The marks per week are `19:10 · 20:6 · 21:8 · 22:13 · 23:8 · 24:4 · 25:12 · 26:14` (sum 75). Week 24 has **four** marks (two multiple-choice and one output) and Week 20 **six**: one question is 17-25% of the week. A "redo" flag on either of those means *ask the spoken check first*, not *redo the whole page*.
3. **Multiple choice can be guessed.** Twenty 4-option questions guessed at random average 5 marks. That is why there are only 20 of 75 marks there, and why every wrong option was built from a real wrong answer or a real tempting half-truth from Weeks 19-26, so a wrong choice *means* something (the key names what).
4. **Weeks 20, 21 and 24 are quoted from the plan, not from a written guide.** When this file was written, `teacher-guide/week-20.md`, `week-21.md` and `week-24.md` (and the student guides and workbooks for Weeks 19-21 and 24) **were not on disk**. The questions on those weeks (A4-A8, A15-A16, B2, B3, B6, D3) therefore use only what the README's row for each week and the patched Module 4 say — byte-level BPE merging the most common pair, a straight line on log-log paper, `C ≈ 6ND`, learning from examples in the prompt, a schema guarantees shape not sense, `torch.where` as a logit mask — and every number in them is **chosen or computed here**, not quoted from a Week 20/21/24 run. **Status update (audit, Term 3 numbers check):** all three guides and their student guides and workbooks now exist, and each of the six words on the paper (*merge*, *bytes per token*, *power law*, *log-log*, *in-context*, *logit mask*) does appear in the matching lesson (Week 20: merge, bytes per token; Week 21: power law, log-log; Week 24: in-context, logit mask). **Before you print:** still skim those three guides; if the paper's words ever drift from the lessons', change the paper and the key **together**. The arithmetic will not change.
5. **Every quoted number is one run.** The Week 19 table is one seed plus one repeat; Week 26's recall is ten questions; Week 22's toys are deterministic but tiny. The paper's claims are about the *shape*.
6. **The self-marking is honest only if the sheet gives working.** A sheet that shows only answers invites a student to "correct" their paper to match. Marking Sheet 1 shows working for every arithmetic question for that reason.
7. **The stand-ins.** A14, A19 and E(c) mention `FakeClient` and the sentence-copier. They are labelled on the paper. If a student writes that "the model" chose a sentence, mark the sentence for what it says, but write on the sheet: *stand-in, not a model*.

### 7. The misconceptions you will actually see, and where

| On the paper | A student writes | What it tells you |
|---|---|---|
| A2 | "the mask was holding it back" | Reads a loss as a score; has not met the leak. Week 19. |
| A3 | "a bright stripe proves what the head does" | Takes a name for a result. Week 19. |
| A5 | "deletes the most common letter" | Thinks of compression as deletion. Week 20. |
| A6 | "the loss drops by the same amount" | Confuses log-log with a plain line. Week 21. |
| A7 | "a measurement" | Treats a fitted line as data. Week 21. |
| A9 | "masking broke the model" | Cannot compare two averages over different guesses. Week 22. |
| A11 | "beta 5 is better: lower loss" | Compares losses across setups. Week 22. |
| A12 | "6" | Took 50.0 − 43.8 as fields. Week 23. |
| A14 | "examples help real models" | Reads a stand-in's script as a finding. Week 23. |
| A15 | "the weights are updated per example" | Confuses prompt-time learning with training. Week 24. |
| A18 | "dense beats sparse" | The headline the week was built to prevent. Week 25. |
| A19 | "the answer is right" | A valid citation is not a true answer. Week 26. |
| B2 | `[('aa', 2), ...]` and `Xabd...` | Counts non-overlapping pairs; Counter counts every neighbouring pair. |
| B5 | "stopped at call 2" | Stops at the last call under the limit; the guard trips one call late. |
| B8 | `['2', '5', '9']` for the first list | Confuses `cited` with `served`. |
| C1 | "it is fine, the loss falls" | Misses that it is **negative** and the winner is behind. |
| C3 | "the search works, note 0 is first" | Never asked whether the vectors are the same length. |
| D1 | `8 / 9` with no name, or `8 / 3` | Forgot one length. Week 25. |
| D2 | `0.2773` for KL(q‖p) as well | Thinks KL is symmetric. Week 22. |
| D3(b) | `-0.954` or `0.477` | Lost the sign, or used one step of `log10` only. Week 21. |
| E(c) | "1.00 is excellent" | The lesson of Week 26 in one line. |

### 8. How deep to go, and where to stop

Today you teach **nothing**. If, while they work, the student asks a question, the only legal answers are *"read it again"*, *"write what you know"*, and *"I can't help with that one, move on."* Afterwards, in the wrap, explain **no** wrong answers; promise to go through the pattern next time. Real explaining happens in the remediation fortnight, where it will stick because the student has just discovered the gap for themselves.

### 9. 🧭 Where Week 27 sits

```text
   TERM 3 — HOW IT IS MADE, HOW IT IS ASKED                         TERM 4 — AGENTS, SAFETY, THE CAPSTONE
   W19 open the GPT   W20 BPE   W21 scaling   W22 SFT/RM/DPO        W28 tools and the loop (needs W23, W26)
   W23 the harness    W24 in-context + schemas                      W29 attacks + the cost of history (needs W26, W23)
   W25 embeddings     W26 RAG: retrieve, cite, refuse               W30-33 fine-tune, evals, safety (need W23, W22)
                          ┌───────────────┐
                          │  W27  PAPER   │  one week to find out what to redo BEFORE the model gets hands
                          └───────────────┘
```
Three weeks are load-bearing for Term 4: **Week 23** (the floor, the frozen set, the budget guard that stops one call late — Week 28's six fences and Week 29's cost arithmetic reuse all three), **Week 26** (chunks, the gate, citations verified in code, and "retrieved text is data, not orders" — Week 29 is that sentence made into an attack) and **Week 22** (the leash and KL return when Week 31 fine-tunes). If the grid shows Weeks 23, 26 or 22 under 60%, those are the ones to redo first; see the remediation table.

---

## 🧰 Prep Checklist

Work through this list the night before. It confirms the numbers the paper quotes and gets the printed pages ready.

### 30 minutes the night before

**☐ 1. Smoke test and folder check (1 minute).** Open a terminal **in the `36-week-course/` folder** — the folder that *contains* both `l4lib/` and `teacher-guide/` — and run the first block in a Python session (`python3`; **one session for the whole prep**, because the blocks share names). If it says `ModuleNotFoundError: No module named 'l4lib'` you are in the wrong folder (the commonest error of the whole year). If it says `FileNotFoundError: .../teacher-guide/week-26.md` you are in the wrong folder too. `pip` returning **403** is the proxy, and it is **not an error**: nothing is installed this year. The block moves the session into a fresh temporary folder, so Week 26's `notes/` folder is written there and **not** into your course folder.

**Block P1 — set-up, and a loader for earlier guides (TEACHER-ONLY plumbing)**

```python
# week27.py - Week 27 prep. Run the blocks below in order, in ONE session, from the folder that contains l4lib/ and teacher-guide/.
import contextlib
import io
import math
import os
import re
import sys
import tempfile
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
torch.set_num_threads(1)
COURSE = os.getcwd()                                   # the 36-week-course/ folder
sys.path.insert(0, COURSE)
from l4lib import rag


def guide_blocks(week):
    """Every fenced python block of one teacher guide, in order (TEACHER-ONLY plumbing, not on the student's ladder)."""
    text = open(f"{COURSE}/teacher-guide/week-{week}.md", encoding="utf-8").read()
    fence = "`" * 3                                        # three backticks, spelled so this block does not contain a fence
    return re.findall(fence + r"python\n(.*?)" + fence, text, flags=re.S)


def block_named(blocks, first_line):
    found = [b for b in blocks if b.startswith(first_line)]
    assert len(found) == 1, (first_line, len(found))
    return found[0]


os.chdir(tempfile.mkdtemp(prefix="w27_"))              # Week 26's blocks write notes/ into the current folder; keep it out of the course folder
print("l4lib loaded; Week 26 guide blocks found:", len(guide_blocks("26")) > 20)
```
```text
l4lib loaded; Week 26 guide blocks found: True
```

**☐ 2. Confirm the Week 26 numbers that go on the paper (1 minute).** Block P2 re-executes Week 26's own set-up, question, retrieval and chunking blocks from the Week 26 guide, in one namespace, and prints only the recall rows and the chunking table. If your numbers differ, **stop**: the paper quotes them.

**Block P2 — `rerun26.py` (TEACHER-ONLY plumbing)**

```python
# rerun26.py - Week 27 prep (TEACHER-ONLY). Re-runs Week 26's own blocks, in one namespace, and prints only the lines the paper quotes.
g26 = {}
b26 = guide_blocks("26")
quiet = io.StringIO()
with contextlib.redirect_stdout(quiet):                 # Week 26's blocks print a lot; we want only a few lines
    for first in ["# week26.py", "# questions.py", "# retrieve.py", "# chunking.py"]:
        exec(block_named(b26, first), g26)
for line in quiet.getvalue().splitlines():
    if ("recall@1/3/5" in line) or line.startswith(("by note", "fixed ", "cut ")):
        print(line)
```
```text
literal (the questions you wrote)      recall@1/3/5 = 1.00 / 1.00 / 1.00
stranger (same facts, other words)     recall@1/3/5 = 0.20 / 0.50 / 0.60
cut                            n  avg w   r@1   r@3   r@5  words @k=3  % of notebook
by note (the files)           15   45.3  1.00  1.00  1.00         146            21%
fixed 30 words, overlap 8     31   29.9  0.80  0.90  1.00          90            13%
fixed 60 words, overlap 15    15   59.9  0.90  1.00  1.00         180            26%
fixed 120 words, overlap 0     6  114.7  0.90  1.00  1.00         354            51%
fixed 250 words, overlap 50    4  209.5  1.00  1.00  1.00         718           104%
```

**☐ 3. The homework key: the same table at three chunk sizes Week 26 did not use (1 minute).** The README's homework is *"rerun the recall table with a changed chunk size"*. Week 26 cut at 30, 60, 120 and 250 words. Block P3 adds 20, 45 and 90, with the same ten questions and the same scoring (the phrase must appear in the text of the top-k chunks).

**Block P3 — `sweep.py` (uses P2's names)**

```python
# sweep.py - Week 27 homework key: Week 26's chunking table at three chunk sizes it did not use.
rp, chunk_fixed, Tf = g26["recall_phrase"], rag.chunk_fixed, rag.TfidfEmbedder
total_words = len(rag.NOTEBOOK.split())
print(f"{'cut':28s}{'n':>4s}{'r@1':>6s}{'r@3':>6s}{'r@5':>6s}{'% of notebook @k=3':>20s}")
for size, over in [(20, 5), (45, 10), (90, 20)]:
    cs = chunk_fixed(rag.NOTEBOOK, size, over)
    cix = rag.VectorIndex(cs, Tf())
    sent = sum(sum(len(h.text.split()) for h in cix.search(qq, 3)) for qq, _, _ in g26["QUESTIONS"]) / len(g26["QUESTIONS"])
    r = [rp(cix, k) for k in (1, 3, 5)]
    print(f"fixed {size} words, overlap {over:<3d}   {len(cs):4d}{r[0]:6.2f}{r[1]:6.2f}{r[2]:6.2f}{sent / total_words * 100:19.0f}%")
```
```text
cut                            n   r@1   r@3   r@5  % of notebook @k=3
fixed 20 words, overlap 5       46  0.60  0.90  1.00                  9%
fixed 45 words, overlap 10      20  0.90  1.00  1.00                 20%
fixed 90 words, overlap 20      10  1.00  1.00  1.00                 39%
```

Read it with the Week 26 table: recall@1 climbs with window size (`0.60`, `0.80`, `0.90`, `0.90`, `1.00`) while the share of the notebook sent at k = 3 climbs faster (`9%`, `13%`, `26%`, `51%`, `104%`). **One question is `0.10`**, so `0.90` against `1.00` is one question. The honest sentence for the student's write-up: *"on these ten questions, bigger windows gave me higher recall and cost me more words; I cannot tell 0.90 from 1.00 with ten questions."*

**☐ 4. Confirm the Week 22 numbers the paper quotes (1 minute).** Block P4 re-executes Week 22's masked-loss and DPO blocks.

**Block P4 — `rerun22.py` (TEACHER-ONLY plumbing)**

```python
# rerun22.py - Week 27 prep (TEACHER-ONLY). Re-runs Week 22's masked-loss and DPO blocks from the Week 22 guide (about 2 seconds) and prints the lines the paper quotes.
g22 = {}
buf = io.StringIO()
b22 = guide_blocks("22")
with contextlib.redirect_stdout(buf):
    for first in ["# sftmask.py", "# dpo.py"]:
        exec(block_named(b22, first), g22)
for line in buf.getvalue().splitlines():
    if line.startswith(("loss over", "  beta 0.10", "  beta 5.00")):
        print(line)
```
```text
loss over all 8 predictions   : 3.8008
loss over 4 response positions: 4.0407
  beta 0.10  A=0.997 B=0.003 C=0.000 D=0.000   KL(pi||ref)=1.760  loss=0.2560
  beta 5.00  A=0.589 B=0.236 C=0.144 D=0.032   KL(pi||ref)=0.566  loss=0.0020
```

**☐ 5. Compute the key (2 minutes).** Every hand-arithmetic answer on the paper, from code. This file teaches nothing new; it is there so that **you** can see the hand answers and the computer agree.

**Block P5 — `key.py`: Section D, every number**

```python
# key.py - Week 27: every hand-arithmetic answer on the paper (Section D), computed.
u, v, w = np.array([2.0, 1.0, 2.0]), np.array([1.0, 2.0, 2.0]), np.array([2.0, -1.0, 0.0])


def cos(a, b):
    return float(a @ b / (np.sqrt(a @ a) * np.sqrt(b @ b)))


print("D1 lengths:", np.sqrt(u @ u), np.sqrt(v @ v), round(float(np.sqrt(w @ w)), 3))
print("D1 dots   :", u @ v, u @ w)
print("D1 cosines:", round(cos(u, v), 3), round(cos(u, w), 3))
p, q = np.array([0.6, 0.3, 0.1]), np.array([0.3, 0.3, 0.4])
print("D2 terms p||q:", (p * np.log(p / q)).round(4), " KL", round(float((p * np.log(p / q)).sum()), 4))
print("D2 KL(p||p)  :", float((p * np.log(p / p)).sum()))
print("D2 terms q||p:", (q * np.log(q / p)).round(4), " KL", round(float((q * np.log(q / p)).sum()), 4))
print("D3 (a) bytes per token:", 2400 / 800)
slope = np.log10(1.0 / 9.0) / (np.log10(1e6) - np.log10(1e4))
print("D3 (b) slope:", round(float(slope), 3), " (c) loss at 1e7:", round(float(1.0 * 10 ** (slope * (7 - 6))), 3))
print("D3 polyfit  :", np.polyfit(np.log10([1e4, 1e5, 1e6]), np.log10([9.0, 3.0, 1.0]), 1).round(3))
print("D3 (d) C = 6ND:", "%.1e" % (6 * 1e6 * 2e7))
```
```text
D1 lengths: 3.0 3.0 2.236
D1 dots   : 8.0 3.0
D1 cosines: 0.889 0.447
D2 terms p||q: [ 0.4159  0.     -0.1386]  KL 0.2773
D2 KL(p||p)  : 0.0
D2 terms q||p: [-0.2079  0.      0.5545]  KL 0.3466
D3 (a) bytes per token: 3.0
D3 (b) slope: -0.477  (c) loss at 1e7: 0.333
D3 polyfit  : [-0.477  2.863]
D3 (d) C = 6ND: 1.2e+14
```

**☐ 6. Check the grid adds up, and the quoted sums (1 minute).** Block P6 lists every question with its week and marks, totals by week, prints the "redo if marks at or below" line (60% rounded down) and checks the arithmetic the paper leans on from Weeks 22 and 23.

**Block P6 — `grid.py` (TEACHER-ONLY: dictionaries and a loop)**

```python
# grid.py - Week 27: check the per-week grid (Marking Sheet 2) adds up to the paper's 75 marks, and the quoted sums.
items = []                                                       # (label, week, marks)
weeks_A = [19, 19, 19, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 25, 25, 26, 26]
for i, wk in enumerate(weeks_A):
    items.append((f"A{i + 1}", wk, 1))
for i, wk in enumerate([19, 20, 21, 22, 23, 24, 25, 26]):
    items.append((f"B{i + 1}", wk, 2))
items += [("C1", 22, 3), ("C2", 23, 3), ("C3", 25, 3), ("C4", 26, 3)]
items += [("D1", 25, 5), ("D2", 22, 5), ("D3(a)", 20, 2), ("D3(b-d)", 21, 3)]
items += [("E(a,b)", 19, 5), ("E(c,d)", 26, 7)]
per_week = {}
for label, wk, marks in items:
    per_week[wk] = per_week.get(wk, 0) + marks
for wk in sorted(per_week):
    print(f"week {wk}: {per_week[wk]:2d} marks, redo if marks <= {int(per_week[wk] * 0.6)}")
print("total:", sum(per_week.values()), "| section A:", sum(m for l, _, m in items if l.startswith("A")),
      "| B:", sum(m for l, _, m in items if l.startswith("B")), "| C:", sum(m for l, _, m in items if l.startswith("C")),
      "| D:", sum(m for l, _, m in items if l.startswith("D")), "| E:", sum(m for l, _, m in items if l.startswith("E")))
print("A12: fields at 50.0% and 43.8% of 32:", round(0.50 * 32), round(0.438 * 32), "| difference", round(0.50 * 32) - round(0.438 * 32))
print("A9 : masked minus unmasked loss:", round(4.0407 - 3.8008, 4))
print("B4 : -ln(sigmoid(2)):", round(float(-np.log(1 / (1 + np.exp(-2)))), 4), "| ln 2:", round(math.log(2), 4))
```
```text
week 19: 10 marks, redo if marks <= 6
week 20:  6 marks, redo if marks <= 3
week 21:  8 marks, redo if marks <= 4
week 22: 13 marks, redo if marks <= 7
week 23:  8 marks, redo if marks <= 4
week 24:  4 marks, redo if marks <= 2
week 25: 12 marks, redo if marks <= 7
week 26: 14 marks, redo if marks <= 8
total: 75 | section A: 20 | B: 16 | C: 12 | D: 15 | E: 12
A12: fields at 50.0% and 43.8% of 32: 16 14 | difference 2
A9 : masked minus unmasked loss: 0.2399
B4 : -ln(sigmoid(2)): 0.1269 | ln 2: 0.6931
```

**☐ 7. Run the paper's code (3 minutes).** Every program on the paper is in [The Paper, in Full](#-the-paper-in-full); run the preamble and B1-B8 in one session, then run C1-C4 *as given* (each is deliberately broken, and the **Debugging Clinic** has the real output). The outputs are in the key (Marking Sheet 1). **Do not skip this step**: it is the only way you will recognise a student's wrong answer at a glance.

**☐ 8. Read the key once (10 minutes).** Section A's wrong-option map, the D follow-through notes and the E(a)-(d) exemplars. Then decide, honestly, what *you* would write for E(c) (the reply to the classmate).

**☐ 9. Print.** Print **one** copy of [The Paper](#-the-paper-in-full) single-sided (so there is room to work), and **one** copy of the **marking sheet** (Marking Sheet 1 — *only* the block between the two "✂ PRINT" lines). Print the **per-week grid** (Marking Sheet 2) and the **remediation table** (Marking Sheet 3) on one page. **Do not print the rest of this file.** Never hand the student any page of this guide except those three.

**☐ 10. Check the student-guide wording (5 minutes).** See "Honest limits", item 4. Open the Week 22, 23, 25 and 26 student guides (they exist) and check the words *masked loss*, *leash*, *floor*, *frozen set*, *recall@k*, *stranger*, *citation*. For Weeks 19, 20, 21 and 24, open whatever exists. If one differs, edit the paper and the key **together**.

**☐ 11. Decide the remediation slots.** The remediation table gives each weak week a 20-minute redo. Find two slots in the coming fortnight *now* and write them on the table. A remediation plan with no time attached does not happen.

### 3 minutes on the day

**☐ 12.** Clear the desk: pen, calculator (airplane mode **on**), scrap paper, water. **The laptop is shut and out of reach**, because this paper's whole point is "no computer". Put the timer where you can both see it. Put the paper face down.

### Fallback if the laptops fail

**Nothing about the lesson needs a laptop.** The student's paper is printed numbers. If *your* laptop fails the night before, the Section E tables are already printed and the key's numbers are in this file: the prep only confirms them. Do the lesson from the printed pages. If Block P2 or P4 runs for more than a minute, stop it (Ctrl-C): nothing downstream needs it. If `exec` of an earlier guide fails with a `SyntaxError`, the extractor has met a code fence inside a string (this is what stops Week 23's `bench.py` from being re-run); skip that block, the numbers are quoted.

---

## ⏱️ The Lesson, Minute by Minute

This week's lesson has the usual five-part shape, but four of the five parts are deliberately **empty**. That is the design: nothing is taught, so nothing can be "rescued".

| Segment | Minutes | Clock | What happens |
|---|:--:|:--:|---|
| 🪝 Hook — The Promise | 2 | 0:00-0:02 | Desk cleared, laptop away. You read the three rules and the X-ray sentence. |
| 🧠 Concept & Maths | 0 | — | **None.** There is nothing to explain. |
| 💻 Live-Code Together | 0 | — | **None.** No computer today. |
| 🎲 Their Turn — The Paper | 70 | 0:02-1:12 | Sections A to E, with five time-checks. You say the *time*, nothing else. |
| 🔑 Wrap & Assign | 3 | 1:12-1:15 | Paper in. Marking sheet out. Say what the homework is. Nothing about right or wrong answers. |

### 🪝 Hook — The Promise (2 minutes)

Say, slowly, *from the page, not from memory*:

> *"This is not a test you pass or fail. It is an X-ray of the last eight weeks. You have 70 minutes, a calculator and a pen. No computer, no notes, and I can't help, because the X-ray only works if I don't. If a question looks strange, write down what you do know and move on: partial working earns marks. When it is over you will mark it yourself, and the marks will tell us which two weeks to go back to before the model gets hands and tools."*

Then: *"Questions?"* Answer **only** about logistics (where to write, the calculator, the toilet). Turn the paper over. Start the timer.

![One bar split into five blocks A to E sized by marks, with minutes beneath each and Section E highlighted](../figures/fig-w27-1-the-paper-in-marks.svg)
*Figure 27.1 — The paper is 75 marks in five sections (20 + 16 + 12 + 15 + 12), and the biggest single question is last.*


### 🎲 Their Turn — The Paper (70 minutes)

Sit **to the side and a little behind**. Do something quiet and boring: read, mark something else. Do not watch the page: a student who feels watched writes the answer they think you want.

**The five time-checks.** At each time below say *only* the sentence on the right, in a normal voice:

| Clock | Say | What it is for |
|:--:|---|---|
| **0:17** | *"Seventeen minutes. Section A is usually done by now."* | A is 20 one-mark questions; a student still on A at 0:17 will starve E. |
| **0:32** | *"Thirty-two minutes. Moving on from B is fine."* | B is 8 short programs, about 2 minutes each. |
| **0:44** | *"Forty-four minutes. Section C should be finished."* | C is 4 bugs, about 3 minutes each. |
| **0:59** | *"An hour. You have thirteen minutes for E. Start it now."* | E is 12 marks, **the largest single question on the paper**, and D is the slowest section; a student who is still on D at 0:59 should leave D3 for last and go to E. |
| **1:10** | *"Two minutes. Finish the sentence you are on."* | Stops the half-finished answer. |

**If they ask you something during the paper.** Three legal replies: *"Read it again."* / *"Write what you do know."* / *"I can't help with that one — move on."* Never a fourth. **If they say "I don't get it":** *"That is useful. Write 'did not get it' next to it and go on. It is the most useful thing you can write."* (Marking rule 4: an honest *"don't know"* is recorded on the grid and is worth more than a lucky guess.)

**If they finish early.** With more than 10 minutes left: *"Go back through, starting from the end, and check each one against your own working."* **Do not** let them leave; do not let them start the next week. If they finish with more than 20 minutes left something is wrong (blank sections? tell them to try every question, even by guessing in A).

**If they are visibly upset.** Stop the clock if you must. *"This is the X-ray, not the grade. Nobody here is keeping score but you."* A calm minute costs a mark or two and is worth it. If the student cannot continue, write the time on the paper, collect it, and mark only what is there; add the missing-section marks to the grid as *"not attempted — rest of paper"* (do not score it zero in the remediation table, see "Assessing Understanding").

![Eight boxes for Weeks 19 to 26 joined by lines to four boxes for Weeks 28, 29, 30 and later; Weeks 22, 23 and 26 are drawn heavier and tagged redo first](../figures/fig-w27-2-term-3-feeds-term-4.svg)
*Figure 27.2 — Weeks 22, 23 and 26 are the ones Term 4 leans on hardest, so they are the first redos.*


### 🔑 Wrap & Assign (3 minutes)

1. **At 1:12: "Pens down."** Take the paper. Do not read it in front of them.
2. **Hand over the marking sheet** (the printed Marking Sheet 1 and the grid, Sheet 2) and a pen of a *different colour* from the one used on the paper.
3. **Say the homework once:** *"Mark your own paper tonight against this sheet, in the other colour. Give yourself marks for working, not just answers: the sheet tells you how. Then fill in the grid, and circle at most two weeks. Then one small job at the computer, which the sheet explains. Bring it next time."*
4. **Say one true thing about the paper**, whatever the result: *"Whatever you got, the thing I care about is whether you can tell me, on the grid, where the marks went."*
5. Do **not** discuss any question. If they ask, *"Tonight, with the sheet. Then we'll talk about the pattern."*

---

## 🐞 The Debugging Clinic

This week the clinic is **short and different**: the four bugs the paper asks the student to find (C1-C4), produced by running them, with the real output you will want to hold in your head while you mark Section C — plus four more mistakes from Weeks 22-26 (M5-M8) for the remediation fortnight. There is nothing to *plant* in class: the student has already met each of these. Use this clinic **in the remediation fortnight**, on whichever bug the student missed. **Four of the eight are silent** (nothing is raised; the output is just wrong): those are the ones that cost the most marks.

Every error below was produced by running the code. **Paths will differ on your machine**; they are shown as `/home/you/l4/`. Each block marked `DELIBERATE` is a mistake on purpose.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (It says what went wrong; the lines above say where.)
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What would you change, and what do you predict will happen?"* — and let them run it.

For a **silent** bug there is no last line to read, so the first question changes: *"What should be true of this output, and is it?"* (A loss is never negative? The winner is ahead? The best match is the most similar, not the longest? The top three are the three highest?)

### Bug C1 — the reward loss missing its minus (SILENT, Week 22)

```python
# DELIBERATE BUG C1 (SILENT): the reward loss is missing its minus sign.
import torch
import torch.nn.functional as F
r = torch.zeros(2, requires_grad=True)              # r[0] = reward of the winner, r[1] = reward of the loser
opt = torch.optim.SGD([r], lr=0.5)
for step in range(20):
    loss = F.logsigmoid(r[0] - r[1])
    opt.zero_grad()
    loss.backward()
    opt.step()
print(round((r[0] - r[1]).item(), 2), round(loss.item(), 2))
```
```text
-18.64 -17.64
```

**Read it:** nothing is raised, the loop runs, the number printed is tidy. But the first number is the winner's reward **minus** the loser's, and it is **-18.64**: the winner has been pushed 18.6 *behind*. And the loss printed is **negative**, which a loss built from `-ln(a chance)` never is. `F.logsigmoid` is the *log* of a chance, which is zero or below; the loss is its negative. Minimising the log-chance drives it to minus infinity by pushing the gap the wrong way. **Fix:** the minus. **The checks** are the two Week 22 taught: *a loss is not negative*, and *after training the winner must be ahead*. Marking: 1 for "the sign of the loss / missing minus / it trains the wrong way", 1 for the consequence (the winner ends behind, or the loss is negative), 1 for the fix `-F.logsigmoid(...)`.

```python
import torch
import torch.nn.functional as F
r = torch.zeros(2, requires_grad=True)
opt = torch.optim.SGD([r], lr=0.5)
for step in range(20):
    loss = -F.logsigmoid(r[0] - r[1])               # the minus: a small loss means the winner is ahead
    opt.zero_grad()
    loss.backward()
    opt.step()
print(round((r[0] - r[1]).item(), 2), round(loss.item(), 2))
```
```text
2.96 0.05
```

### Bug C2 — a pattern that cannot see across a line break (loud, Week 23)

```python
# DELIBERATE BUG C2 (loud): the pattern cannot see across a line break.
import re
reply = 'Sure, here you go:\n{\n  "category": "billing",\n  "urgency": 2\n}'
match = re.search(r"\{.*\}", reply)
print(match.group())
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad_c2.py", line 5, in <module>
    print(match.group())
AttributeError: 'NoneType' object has no attribute 'group'
```

**Read it:** the error is on the **`print` line**, but the mistake is on the line above. `re.search` found nothing and returned `None`; `None` has no `.group`. The dot in `\{.*\}` matches any character **except a line break**, and this record spans four lines. **Fix:** `re.S` as the third argument (Week 23's fourth construct). Marking: 1 for "`match` is `None` / the search found nothing", 1 for "`.` does not match the line break / the record is on several lines", 1 for `re.S`. *(Had the reply been on one line there would have been no error at all: the bug only shows when the stand-in, or a real model, decides to lay out its JSON over several lines.)*

```python
import re
reply = 'Sure, here you go:\n{\n  "category": "billing",\n  "urgency": 2\n}'
match = re.search(r"\{.*\}", reply, re.S)
print(match.group())
```
```text
{
  "category": "billing",
  "urgency": 2
}
```

### Bug C3 — the index rows are not normalised (SILENT, Week 25)

```python
# DELIBERATE BUG C3 (SILENT): the index rows are not normalised, so a long row beats a close one.
import numpy as np
index = np.array([[3.0, 3.0],       # note 0: points up and to the right, and is LONG
                  [0.0, 1.0]])      # note 1: points exactly the way the question does
query = np.array([0.0, 1.0])
scores = index @ query
print(scores, np.argsort(-scores)[:1])
```
```text
[3. 1.] [0]
```

**Read it:** nothing is raised, the ranking code is right (`np.argsort(-scores)[:1]` is the Week 26 top-1), and the answer is wrong: note 1 points *exactly* the way the question does (cosine 1.0) and loses to note 0, which points 45 degrees away (cosine 0.707) but is longer. A plain dot product rewards **length**. **Fix:** normalise every row to length 1 **once**, and the query too; then the dot product *is* the cosine (Week 25). **The check:** the lengths of the rows (`np.sqrt((index * index).sum(axis=1))`); if they are not all 1 the scores are not cosines. Marking: 1 for "the dot product rewards long vectors / the rows are not normalised", 1 for the consequence (note 1 is the better match and ranks second; or scores `3` and `1` are not cosines), 1 for "divide each row by its length once".

```python
import numpy as np
index = np.array([[3.0, 3.0], [0.0, 1.0]])
query = np.array([0.0, 1.0])
index = index / np.sqrt((index * index).sum(axis=1, keepdims=True))     # normalise every row ONCE
query = query / np.sqrt(query @ query)
scores = index @ query
print(scores.round(3), np.argsort(-scores)[:1])
```
```text
[0.707 1.   ] [1]
```

### Bug C4 — the top three, picked without the minus (SILENT, Week 26)

```python
# DELIBERATE BUG C4 (SILENT): the top three, picked without the minus.
import numpy as np
scores = np.array([0.05, 0.60, 0.00, 0.31, 0.12, 0.44])
def top_k(scores, k):
    return np.argsort(scores)[:k]
print(top_k(scores, 3), scores[top_k(scores, 3)])
```
```text
[2 0 4] [0.   0.05 0.12]
```

**Read it:** nothing is raised, three ids come back, and they are the three **lowest**. `np.argsort` sorts smallest first; the minus flips it (Week 26's own comment). In a RAG pipeline this would serve the three *least* similar notes and the system would answer confidently from them. **The check** is Week 26's: print the scores of the ids you picked next to the best score. Marking: 1 for "`argsort` sorts smallest first", 1 for the consequence ("picks the three lowest scores / least similar"), 1 for `np.argsort(-scores)[:k]`.

```python
import numpy as np
scores = np.array([0.05, 0.60, 0.00, 0.31, 0.12, 0.44])
def top_k(scores, k):
    return np.argsort(-scores)[:k]
print(top_k(scores, 3), scores[top_k(scores, 3)])
```
```text
[1 5 3] [0.6  0.44 0.31]
```

### Four more, for the remediation fortnight

```python
# DELIBERATE MISTAKE M5 (loud): F.logsigmoid given a plain Python number, not a tensor.
import torch.nn.functional as F
print(F.logsigmoid(2.0))
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad_m5.py", line 3, in <module>
    print(F.logsigmoid(2.0))
TypeError: log_sigmoid(): argument 'input' (position 1) must be Tensor, not float
```

**Read it:** the last line names the function and the type it wanted. **Fix:** `F.logsigmoid(torch.tensor(2.0))`. (The Week 22 construct takes tensors, not numbers.)

```python
# DELIBERATE MISTAKE M6 (warns, then wrong): the cosine of a note with no words at all.
import numpy as np
a = np.array([0.0, 0.0, 0.0])
b = np.array([1.0, 2.0, 2.0])
print(a @ b / (np.sqrt(a @ a) * np.sqrt(b @ b)))
```
```text
nan
```

**Read it:** the real run also prints, **above** the `nan`, a warning on `stderr`: `RuntimeWarning: invalid value encountered in scalar divide`. The length of an all-zero vector is `0`, and `0 / 0` is `nan`. Nothing is raised, and a `nan` then **wins or loses every comparison by accident** (`np.argsort` puts it last; `nan > 0.5` is `False`). In Week 25's pipeline this is a note or a question with no known letter pieces. **Fix:** test the length first and treat zero as "no score" (Week 26's gate does this by refusing).

```python
# DELIBERATE MISTAKE M7 (SILENT): comparing citation ids typed as numbers with served ids typed as text.
import re
cited = set(re.findall(r"\[(\d+)\]", "The answer is in [2]."))
served = {2, 5, 9}
print(cited, cited <= served)
```
```text
{'2'} False
```

**Read it:** `re.findall` returns **strings**; `served` was built from integers, so `'2'` is not in it and a correct citation is rejected. (Week 26's own `check_citations` converts to `int` first.) The same mistake the other way round would **accept nothing** or, with a different pair, nothing visible. **Fix:** `{int(c) for c in cited}`.

```python
# DELIBERATE MISTAKE M8 (loud): a guard that catches the wrong exception.
class OverBudget(Exception):
    pass
def charge(spent, cost, limit):
    if spent + cost > limit:
        raise OverBudget("over the limit")
    return spent + cost
try:
    charge(0.9, 0.4, 1.0)
except ValueError:
    print("caught")
```
```text
Traceback (most recent call last):
  File "/home/you/l4/bad_m8.py", line 9, in <module>
    charge(0.9, 0.4, 1.0)
  File "/home/you/l4/bad_m8.py", line 6, in charge
    raise OverBudget("over the limit")
__main__.OverBudget: over the limit
```

**Read it:** the `except` names `ValueError`, the function raised `OverBudget`, so nothing catches it and the program dies with the custom error: this is **exactly** the failure a budget guard is meant to prevent from being a crash. (On your machine the last line may read `OverBudget: over the limit` without `__main__.`.) **Fix:** `except OverBudget:` (Week 23).

---

## 🎲 The Activity, In Full

### The Paper, in Full

> **How to use this section.** Everything between the two lines marked `✂ PAPER STARTS` and `✂ PAPER ENDS` is what the student sees. Print exactly that. Everything *outside* them is for you. The code on the paper is the same text that the key runs (the preamble and B1-B8 below; C1-C4 are the Clinic's), and the Section E tables are printed numbers from the Week 19 and Week 26 guides (confirmed, for Week 26, by Blocks P2 and P3).

✂ PAPER STARTS

#### Term 3 Checkpoint — Review and Assessment 3

**Name: ____________________   Date: ______________   Time allowed: 70 minutes   Total: 75 marks**

**Rules.** Calculator allowed. No computer. No notes. Write on the paper. **Show your working** in Sections B-E: a wrong number with the right working still earns marks. If you do not know, write *"don't know"*: that is useful information and costs nothing extra. Every question is about something you have already done with your own hands. In the code, the lines below have already been run.

```python
import re
import numpy as np
import torch
import torch.nn.functional as F
from collections import Counter
```

| Section | What | Marks | Suggested time |
|:--:|---|:--:|:--:|
| **A** | 20 multiple choice (circle one letter) | 20 | 15 min |
| **B** | 8 "what does this print?" | 16 | 15 min |
| **C** | 4 "find the bug" (the programs are *deliberately* broken) | 12 | 10 min |
| **D** | 3 arithmetic | 15 | 15 min |
| **E** | 1 longer question on two real tables | 12 | 13 min |

---

## Section A — Multiple choice (20 marks, 1 each). Circle ONE letter.

**A1.** An **ablation** is

A. training the same model for more steps with a smaller learning rate
B. deleting one part, retraining with everything else the same, and comparing the validation loss
C. timing how long each part of the model takes to run
D. adding a new part and seeing whether the training loss falls

**A2.** In a table of five retrained models, the one with **no mask** has validation loss `0.077`, far the best (the full model has `1.673`). The best reading is

A. the mask was holding the model back
B. masks should always be removed
C. the model can read the answer it is being asked to predict, so the number is a leak and says nothing about whether a mask is worth having
D. `0.077` must be a mistake, because no loss can be below 1

**A3.** On the **copy** task, switching off any *one* head leaves the accuracy at `1.00`. On the **lookup** task, switching off layer-0 head 0 drops it from `1.00` to `0.48`. The best reading is

A. on copy the heads are redundant (another does the same job); on lookup that head does a job no other head covers
B. the lookup model is broken
C. on copy the heads do nothing
D. a bright stripe in a heatmap proves what a head's job is

**A4.** Why is the tokenizer built on **bytes** (UTF-8) and not on letters?

A. bytes make each token carry more meaning
B. computers cannot store letters
C. bytes make the vocabulary bigger than a word-level one
D. every possible text, including emoji, Devanagari and the empty string, is a list of numbers from 0 to 255, so decoding gives the original text back exactly

**A5.** One **merge step** of BPE

A. finds the most common single letter and deletes it
B. finds the most common pair of neighbouring tokens and gives that pair a new token number
C. joins the two longest words into one token
D. picks a random pair so the vocabulary is varied

**A6.** On log-log paper the loss against the number of knobs is a straight line. That means each time the number of knobs is multiplied by 10,

A. the loss drops by the same amount
B. the loss reaches zero at some size
C. the loss is multiplied by (about) the same factor
D. doubling the knobs always halves the loss

**A7.** You fit the line on four small models and read off the loss for a model 100 times bigger. The number you read off is best called

A. a prediction, to be checked by training that model
B. a measurement
C. a guarantee, because the line passed through all four points
D. wrong, because a straight line cannot be extended

**A8.** Using `C ≈ 6ND`, the *same* model (same `N`) is trained on *twice as many* tokens `D`. The compute

A. stays the same
B. goes up about four times
C. halves
D. doubles

**A9.** On the same model scores, the **masked** SFT loss (answer positions only) is `4.0407` and the **unmasked** loss (every position) is `3.8008`. The reason is

A. masked training has broken the model
B. they are averages over different sets of guesses, so they are different numbers, not evidence that one model is worse
C. the prompt tokens were deleted from the model's input
D. masking always raises the loss by 0.24

**A10.** A reward model gives answer 1 a reward of `9.6` and answer 2 a reward of `4.6`. Which statement is safe?

A. answer 1 scores 9.6 out of 10
B. answer 2 is a wrong answer
C. adding 100 to every reward would change nothing it has learned; only the difference between two answers matters
D. the model is 96% confident in answer 1

**A11.** After 300 steps of a DPO toy: `beta = 0.10` ends with `A = 0.997`, KL `1.760`, loss `0.2560`; `beta = 5.00` ends with `A = 0.589`, KL `0.566`, loss `0.0020`. The right reading is

A. `beta = 5` kept the policy much closer to where it started (a short leash), even though its loss is smaller
B. `beta = 5` is better because its loss is lower
C. `beta = 0.10` broke the model
D. a bigger KL means the run failed

**A12.** On a frozen set of 32 fields a prompt scores `50.0%`; the best **constant answer** (the floor, which ignores the message) scores `43.8%`. The prompt is better than the floor by

A. 0 fields
B. 1 field
C. 6 fields
D. 2 fields

**A13.** Why **freeze** the eight test cases *before* writing the prompt?

A. so the model memorises them
B. so the cases cannot be chosen or edited to flatter the prompt, and a change in score means the prompt changed
C. so the budget guard works
D. so the parser runs faster

**A14.** The scripted client `FakeClient` (**stand-in, not a model**) scores version 3 of a prompt above version 1. The claim this supports is

A. examples help real models
B. version 3 is better for any model
C. the script behind the stand-in gives more credit to a prompt with rules and examples; it says nothing about a real model
D. the harness is broken

**A15.** A small transformer you trained learns to follow examples placed in its prompt. At the moment you put new examples into the prompt, its weights

A. do not change: the behaviour comes from what it already learned in training
B. are updated once for each example
C. are copied into the prompt
D. are reset

**A16.** A logit mask forces 100% of a model's outputs to be valid JSON. What can still be wrong?

A. nothing
B. the brackets
C. the braces may be unbalanced
D. the values inside: a well-formed record can carry the wrong category

**A17.** The word table scores `0.000` for the query `optimiser` on the note that says `optimizer`. Why?

A. the note is not in the notebook
B. the two spellings are different columns in the word table, and it has no sense of nearness between columns
C. cosine is undefined for words
D. SVD has not been run

**A18.** Recall@1 on 15 questions: word table `0.67`, LSA `0.73`, trained tier `0.63` on average (range `0.47` to `0.73` over five seeds). The supported claim is

A. dense embedders beat word tables
B. training is worse than no training
C. at recall@1 the three are within a question or two of each other; the word table's hard zero on `optimiser` is a clearer failure than any embedder's win
D. LSA is the best embedder

**A19.** A citation `[8]` passes the code check because note 8 was among the sources served (the writer is a sentence-copying **stand-in, not a model**). This proves

A. the answer is right
B. the note is true
C. the note is safe to obey
D. the writer named a note it was handed; nothing more

**A20.** Recall@1 is `1.00` on questions you wrote after reading the notes, and `0.20` on the same facts in a stranger's words. Which number tells you how it will do for other people?

A. the stranger one, `0.20`, saying who wrote the questions
B. `1.00`
C. the average, `0.60`
D. neither; recall cannot be measured

---

## Section B — What does this print? (16 marks, 2 each)

Write exactly what the last line(s) print. Where a number is rounded, give it as printed.

**B1.**
```python
def run(x, residual):
    for _ in range(3):
        f = 0.1 * x
        x = x + f if residual else f
    return x
print(round(run(1.0, True), 3), round(run(1.0, False), 3))
```

**B2.**
```python
s = "aaabdaaabac"
pairs = Counter([s[i:i + 2] for i in range(len(s) - 1)])
print(pairs.most_common(2))
print(s.replace("aa", "X"))
```

**B3.**
```python
N = np.array([1e3, 1e4, 1e5])
L = np.array([8.0, 4.0, 2.0])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
print(round(slope, 3), round(10 ** intercept))
```

**B4.**
```python
print(round(F.logsigmoid(torch.tensor(0.0)).item(), 4), round(-F.logsigmoid(torch.tensor(2.0)).item(), 4))
```

**B5.**
```python
class OverBudget(Exception):
    pass
class Guard:
    def __init__(self, limit):
        self.limit = limit
        self.spent = 0.0
    def charge(self, cost):
        self.spent += cost
        if self.spent > self.limit:
            raise OverBudget("stop")
guard = Guard(1.0)
calls = 0
try:
    for _ in range(10):
        calls += 1
        guard.charge(0.4)
except OverBudget:
    print("stopped at call", calls, "spent", round(guard.spent, 1))
```

**B6.**
```python
scores = torch.tensor([2.0, 1.0, 0.5, 3.0])
allowed = torch.tensor([True, True, True, False])
masked = torch.where(allowed, scores, torch.tensor(float("-inf")))
print(scores.argmax().item(), masked.argmax().item(), F.softmax(masked, dim=-1)[3].item())
```

**B7.**
```python
a = np.array([3.0, 4.0])
b = np.array([4.0, 3.0])
print(round(float(a @ b / (np.sqrt(a @ a) * np.sqrt(b @ b))), 2))
sc = np.array([0.2, 0.9, 0.5])
print(np.argsort(-sc)[:2])
```

**B8.**
```python
cited = set(re.findall(r"\[(\d+)\]", "see [2] and [7] and [2]"))
served = {"2", "5", "9"}
print(sorted(cited), cited <= served, cited - served)
```

---

## Section C — Find the bug (12 marks, 3 each)

Each program is **deliberately** broken. For each: (1) say what is wrong, (2) say what happens because of it (the error, or what is wrong with the output), (3) write the fix. 1 mark each.

**C1.** The programmer wants the winner's reward to end up *ahead* of the loser's. `F` and `torch` are imported.
```python
r = torch.zeros(2, requires_grad=True)              # r[0] = winner, r[1] = loser
opt = torch.optim.SGD([r], lr=0.5)
for step in range(20):
    loss = F.logsigmoid(r[0] - r[1])
    opt.zero_grad()
    loss.backward()
    opt.step()
print(round((r[0] - r[1]).item(), 2), round(loss.item(), 2))     # prints -18.64 -17.64
```

**C2.** The programmer wants the JSON record out of a reply that is laid out over several lines.
```python
reply = 'Sure, here you go:\n{\n  "category": "billing",\n  "urgency": 2\n}'
match = re.search(r"\{.*\}", reply)
print(match.group())
```

**C3.** The question points exactly the way note 1 does. The search returns note 0.
```python
index = np.array([[3.0, 3.0],
                  [0.0, 1.0]])
query = np.array([0.0, 1.0])
scores = index @ query
print(scores, np.argsort(-scores)[:1])               # prints [3. 1.] [0]
```

**C4.** The programmer wants the ids of the **three best** notes.
```python
scores = np.array([0.05, 0.60, 0.00, 0.31, 0.12, 0.44])
def top_k(scores, k):
    return np.argsort(scores)[:k]
print(top_k(scores, 3), scores[top_k(scores, 3)])     # prints [2 0 4] [0.   0.05 0.12]
```

---

## Section D — Arithmetic (15 marks, 5 each)

Show every step. A calculator with `ln`, `log` and a power key is allowed.

**D1. Cosine by hand (5).** `u = [2, 1, 2]`, `v = [1, 2, 2]`, `w = [2, -1, 0]`.
(a) Find `u·v` and the lengths of `u` and `v`, and so `cos(u, v)` to three decimals. *(3)*
(b) Find `cos(u, w)` to three decimals. *(2)*
(c) Which of `v` and `w` is nearer in direction to `u`? *(no mark; it is the point)*

**D2. KL divergence (5).** Two tables of chances over three outcomes: `p = [0.6, 0.3, 0.1]`, `q = [0.3, 0.3, 0.4]`. KL of `p` from `q` is the sum over outcomes of `p × ln(p / q)`.
(a) Write the three terms and their sum, to four decimals. *(3)*
(b) What is KL of `p` from `p` itself? *(1)*
(c) Work out KL of `q` from `p` (the same sum with the roles swapped). Is it the same as (a)? *(1)*

**D3. Tokens and scaling (5).**
(a) A text of 2,400 bytes becomes 800 tokens after the merges are learned. How many bytes per token? If more merges are learned, does the number go up or down? *(2)*
(b) Three models have `N = 10,000`, `100,000` and `1,000,000` knobs, and losses `9.0`, `3.0` and `1.0`. On log-log paper (`log10` of the loss against `log10` of `N`) these lie on a straight line. What is its slope? *(1)*
(c) Use the line to predict the loss for `N = 10,000,000`. Is this a measurement? *(1)*
(d) The million-knob model is trained on `D = 20,000,000` tokens. Estimate the compute `C ≈ 6ND`. *(1)*

---

## Section E — Reading two real tables (12 marks)

**Table 1. Week 19: the TinyGPT with one part deleted, 800 steps, one thread, seed 0** (the same text and the same scoring batches for every row).

| Model | Train loss | Validation loss | Gap | Validation, repeated with seed 1 |
|---|:--:|:--:|:--:|:--:|
| full | 1.597 | 1.673 | 0.076 | 1.643 |
| no mask | 0.070 | 0.077 | 0.007 | 0.085 |
| no positions | 1.451 | 1.739 | 0.288 | 1.717 |
| no residual | 2.664 | 2.679 | 0.015 | 2.711 |
| no norm | 1.150 | 1.478 | 0.327 | 1.453 |

The sample from the no-mask model begins `tatatattt`.

**Table 2. Week 26: the 15-note notebook, retrieval by word table.** Recall@1/3/5 = the share of ten questions whose right note is the top 1/3/5 result.

| Questions | recall@1 | recall@3 | recall@5 |
|---|:--:|:--:|:--:|
| written after reading the notes (your wording) | 1.00 | 1.00 | 1.00 |
| the same ten facts in a stranger's words | 0.20 | 0.50 | 0.60 |

**Table 3. Week 26: cutting the same notebook into chunks of different sizes** (does the right phrase appear in the text of the top-k chunks?)

| Cut | Chunks | recall@1 | recall@3 | recall@5 | Share of the notebook sent at k = 3 |
|---|:--:|:--:|:--:|:--:|:--:|
| 30 words, overlap 8 | 31 | 0.80 | 0.90 | 1.00 | 13% |
| 60 words, overlap 15 | 15 | 0.90 | 1.00 | 1.00 | 26% |
| 250 words, overlap 50 | 4 | 1.00 | 1.00 | 1.00 | 104% |

**E(a)** *(3 marks)* Put the four deleted models in order from **least to most harmful**, using the validation loss, **but say which row you have not ranked and why its number cannot be read that way.**

**E(b)** *(2 marks)* A classmate says: *"Deleting the layer norm made the model better: 1.673 down to 1.478. Layer norm is useless."* Give **two** reasons, from the table, to be careful.

**E(c)** *(3 marks)* Another classmate says: *"Recall@3 is 1.00, so our search works."* Reply in three sentences: what Table 2 shows, which number you would quote for how it will do for other people and why, and the one question you would ask before trusting any recall number.

**E(d)** *(4 marks)* Using Table 3, a classmate wants to use the 250-word chunks "because recall is 1.00 at every k". Give **two** reasons the 60-word row may be the better choice, say how big a difference of `0.10` is with ten questions, and say one thing you would do to decide properly.

✂ PAPER ENDS

### Setup (2 minutes)

Nothing to set up beyond the desk. The paper is the entire activity.

### What "finished" looks like

Every section has *something* written in it, and at least two of the questions say *"don't know"* or show crossed-out working, which is a **good** sign: it means the student was honest. A paper with no crossed-out working and no "don't know" at all is either an excellent student or one who guessed everything and wrote it down cleanly — look at the Section D working to tell which.

### Variation — shorter (a 60-minute slot)

Sit **A, B, C, D** in class in 52 minutes (63 marks: 20 + 16 + 12 + 15; the 60% line scales to **38 of 63**), and give **E** as a *closed-book take-home*, timed by the student at **13 minutes**, within 24 hours, on the honour system. Say the rules aloud. The E marks (12) then join the grid on the usual rows (Weeks 19 and 26). This is the only variation the grid supports without recomputing.

### Variation — an anxious or slow student

Split the paper into two 40-minute sittings on different days (A-C then D-E). **Not** more time on one day: fatigue is itself a distortion, and a long paper makes it worse.

### Variation — harder (a student who finishes in 40 minutes with 70+ marks)

Add **one** optional question afterwards, *not* on the paper, and said aloud: *"In D3(b) the three points lie exactly on a line. If the loss at 100,000 had been 2.0 instead of 3.0, would the three still be on a line, and what would you do before predicting the loss at ten million?"* (Answer in the key's *Answers to every question posed in the lesson*; it uses only Week 21.)

---

## ❓ Questions Students Ask This Week

Use this table for questions during or after the paper. Each row gives an honest answer and a note on how to handle it.

| They ask | Honest answer | Notes |
|---|---|---|
| "Why no computer?" | "Because the paper is asking what is in *your* head, not what the computer knows. Everything on it, you have done by hand at least once." | If they say "but nobody works without a computer" — *"True. And nobody can debug one who can't predict what it will print."* |
| "Is this for a grade?" | "No. It's an X-ray. The only person it reports to is you, and then me." | Mean it. Do not record a mark anywhere except the grid. |
| "Can I use my notes / the workbook?" | "Not today. The marking sheet tonight is your notes." | |
| "What if I get under 45?" | "Then we go back to the two weeks that need it, for 20 minutes each. It's a plan, not a punishment." | The 45 is a proposal (section 3). Never use the word "fail". |
| "Can I do it again?" | "After the fortnight there is a *new* paper of the same shape, not the same one: the fourth paper, in Week 36, re-tests the key ideas." | Do not write a re-sit paper. Weeks 28-29 recycle W23 and W26 anyway. |
| "Why is `10 ** intercept` in B3?" *(afterwards)* | "The line is `log10 L = slope × log10 N + intercept`. At `N = 1` the log of `N` is 0, so `10 ** intercept` is the loss at `N = 1`: 64." | Week 21's second number. Give the mark for `-0.301` and the mark for `64`. |
| "Why does `.replace` give `XabdXabac` and not something with four X's?" *(afterwards)* | "`Counter` counts every neighbouring pair, so the three a's in a row make **two** `aa` pairs that overlap. `replace` can only use each letter once, left to right." | B2. The honest 'count the overlap' trap. |
| "Why did `stopped at call 3`, not 2?" *(afterwards)* | "After call 2 you have spent 0.8, which is under the limit of 1.0. Call 3 is the one that crosses it, and the guard only notices after it has made the call." | Week 23's 'one call late'. |
| "Can I write `-inf` as a big negative number?" | "In a fix, yes: `-1e9` does the same job as long as it is set before the softmax." | Give the mark. |
| "What's `ln 2`?" | "0.693. You have a calculator." | A student without a `log` key: tell them to write `log10 3` and what they would do; give that step's mark if the setup is right. |

---

## ⚠️ Where This Lesson Goes Wrong

Read this before class. It lists the failures most likely to spoil the paper or its marking.

1. **You help.** The commonest failure. A raised eyebrow changes an answer. Sit to the side.
2. **You hand over the wrong page.** The student must get only Marking Sheets 1, 2 and 3. The rest of this file contains every answer *and the mistakes the student is expected to make*.
3. **The paper runs over.** Seventy minutes is *tight*; Section D is the slowest. The five time-checks exist so E is not left in the last four minutes. If E is not attempted at all, mark A-D and treat E as a take-home (see "Variation — shorter").
4. **Marking by the final number.** The marks are in the *working*. D1 (5 marks) has a dot product, two lengths and a divide; a student who gets a length wrong and then divides *correctly from their own length* loses the length mark, not the divide mark. Follow the key's "follow-through" notes.
5. **Treating 45 as pass/fail.** The only decision the total drives is how many weeks to redo (at most two). A 70 with a 1/4 on Week 24 means **ask the spoken check**, whatever the total.
6. **Scoring the self-marking as the real mark.** Students mark generously or harshly. The teacher **re-marks D and E only** (about 10 minutes), because those are the judgment sections. A disagreement of more than 3 marks in total is a conversation, not an accusation.
7. **Teaching in the wrap.** Resist. The wrap is three minutes, and none of them is for a right answer.
8. **Student-guide wording drift** (Honest limits, item 4). Three of the eight weeks had no written guide when this paper was made. If a guide says it differently, the student will lose a mark to *your* wording, not their own error.
9. **The tables differ on your laptop.** They do not matter: the paper's tables are printed. It would matter only if you re-generated them on the day instead of printing them.
10. **Marking E for "right conclusion".** The marks are for the parts named in each question, not for whether the student agrees with the classmate. A student who writes "layer norm might still be useful" with no reason earns none of E(b); one who says "the gap is bigger and we only ran two seeds" earns both marks even if they still think it is useless.
11. **Counting a stand-in's result as a finding.** A14, A19 and E(c) mention stand-ins. A student who writes that "the model picked the wrong sentence" has the right observation and the wrong noun: give the mark, write *stand-in, not a model* on the sheet.

---

## 🧭 Differentiation

This section covers adjusting the day for a student who is struggling, one who finishes early, and one who will not engage.

### If the student is struggling

- **Same paper, two sittings** (A-C, then D-E), on different days. Not extra time on one day.
- **Read Section E aloud** if reading, not maths, is the barrier. Do not paraphrase; read the words.
- **Calculators for everything** (already allowed). A student who spends 5 minutes on `ln 4` by hand has been unfairly treated by the paper.
- **After the paper**, the remediation table is for *at most two* weeks, even if five are low. Pick the one that Term 4 needs most (priority order: **Week 23 → Week 26 → Week 22**), then the lowest remaining.
- **Do not repeat the paper.** Redo the *page* that went wrong (Marking Sheet 3 names it) and ask the **teacher check question** from the table out loud afterwards. A spoken correct answer, in your own words, is the exit ticket.
- **If Weeks 19-21 are the low ones**, do not panic: nothing in Term 4 leans on them directly. Week 20's token counts return in Week 29's cost arithmetic (the student's own tokenizer, or the `ceil(words × 1.3)` fallback), and Week 21's `6ND` is used once more at the capstone.

### If the student is flying

- **70+ in under 55 minutes:** give the "harder" question from the Activity (D3(b) with a changed loss), orally, afterwards.
- **Have them write two new Section C questions** — one *loud* bug and one *silent* one — for the **next** student, with the real output for the loud one, produced by running it. It is the best test of whether they understand the bug and the cheapest way to test whether the paper is any good. (Do not add them to this paper; they are a candidate for the Week 36 paper's bank.)
- **Have them do the homework sweep at a fourth chunk size** without being asked, and predict the row before running it.
- **Not** more content from Week 28. Today is a review.

### If the student won't engage today

- A flat "I don't care" on the day usually means **one** of: tired, afraid, or "this isn't for a mark so why". Do not argue. Use the X-ray sentence again, shorter: *"Nobody sees this but us. Do the sections you like first."* **They may do the sections in any order.** Take Section D first if that is where the confidence is.
- If they sit 15 minutes with nothing on the page, stop. *"Today is not the day. We'll do it on Thursday."* A paper written under protest produces a map of the protest.
- **Never bribe.** Never threaten. A single "yes, but you can't unlearn what you learned" is enough.

---

## ✅ Assessing Understanding

This section says how to mark the paper, how to read the pattern across weeks, and what to do with each result.

### The marking rules

1. **Working earns marks.** Sections B-E are marked for *method first, number second*. A right number with no working: **half marks** on 2- and 3-mark questions, **at most 3** on a 5-mark question. (This is the rule that makes "show your working" real. Say it in the key, and mean it.)
2. **Follow-through.** If an early number is wrong, mark later lines *from the student's own number*. The key's "follow-through" notes say where it matters (D1, D2, D3, E(a)).
3. **Rounding.** In Section B, numbers are as printed, so `0.96` is 1 mark and `0.9` is **0**. In Section D, accept any answer within **0.002** of the key for D1, within **0.0005** for D2 (a) and (c), and within **0.005** for D3 (b).
4. **"Don't know"** scores 0 *on that question* but is recorded as **"honest"** on the grid, and a paper with several honest "don't knows" and no wild guesses gets **a tick** (see "Reading the pattern").
5. **Vocabulary from next term** is neither penalised nor rewarded (section 4).

### Reading the pattern

- **The total** is the *least* informative number.
- **The per-week fraction** (Marking Sheet 2) tells you what to redo. **Under 60% of the marks in a week** goes in the "redo" column; **80% or over** is "secure". Weeks 20 and 24 are too thin for percentages: see section 6, item 2.
- **Pairs that matter.** Weeks 23 and 26 together low means *the floor and the frozen set* and *the citation and the gate* have not landed, and those are what Week 28's six fences and Week 29's attacks stand on; redo both before Week 28. Weeks 25 and 26 together low means *cosine and recall* have not landed; that is the only idea they share, and it returns in Week 29's mini RAG.
- **When the total and the pattern disagree, the pattern wins.** A made-up student, to practise the arithmetic (this is an illustration, **not** data from anyone): marks by week `W19 8/10, W20 5/6, W21 7/8, W22 7/13, W23 3/8, W24 3/4, W25 9/12, W26 8/14` for a total of **50**, which the scale below calls "Secure". The grid says otherwise: Week 23 is 38%, Week 22 is 54% and Week 26 is 57%, three weeks at or under their "redo" line (3 ≤ 4, 7 ≤ 7, 8 ≤ 8). The rule is **circle at most two**, with the priority order Week 23 → Week 26 → Week 22: so **circle Weeks 23 and 26**, and write Week 22 on the "if there is time" line.
- **Section C versus Section B.** A student who can say what a program prints (B) but cannot find a bug in it (C) knows the *rule* but has not yet learned to ask what should be true of the output: a different remediation (do "a loss is never negative", "the best match is the most similar, not the longest" and "print the scores of the ids you picked" aloud on two programs) from not knowing the rule.
- **Section A high, D low.** Knows the words; cannot do the sums. Redo the by-hand pages. **A low, D high:** does the sums and cannot name them — the vocabulary list from each week's guide.

### Mastery scale for this paper

| Level | Marks (of 75) | Looks like | What you do |
|---|:--:|---|---|
| **Flying** | 60-75 | Section D almost clean; E(c) and E(d) each name a reason and a check; at most one week under 80% | Offer the harder question; ask for two new bug questions; offer a fourth chunk size. |
| **Secure** | 45-59 | At most two weeks under 60%; D mostly right | Redo the circled weeks (20 min each), then move on. |
| **Getting there** | 30-44 | Three or four weeks under 60% | Redo **two** (priority order Week 23 → Week 26 → Week 22), spoken check, and **slow** Week 28 down by one session if needed. Tell the owner before Term 4 builds on shaky ground. |
| **Needs a conversation** | under 30 | Many blanks, or the paper was not attempted seriously | **Do not mark it as a result.** Talk first: tired? afraid? bored? A paper written under protest is a map of the protest. Then see "If the student won't engage". |

*(The 45 line is the proposal from section 3; it is 60% of 75. The scale is a guide, not a ruling.)*

### Teacher re-mark: only D and E

Self-marking covers A, B and C well: those answers are *checkable*. D and E need judgment (is D1(b) done with the student's own length? does the E(c) reply really say who wrote the questions?). Re-mark D (15) and E (12) yourself, in about 10 minutes, **in front of the student if they are willing**. If your total for D+E differs from theirs by more than 3, talk about *why*.

---

## 📤 Homework to Assign

Five tasks for the week after the paper, with time estimates.

1. **Mark your own paper** against the printed sheet (Marking Sheet 1), in the *other colour*. For D and E, mark the **working**, not only the answer. *(Estimated 30 minutes.)*
2. **Fill the per-week grid** (Marking Sheet 2): the marks you got, out of the marks available, for each of the eight weeks, and the percentage. *(5 minutes.)*
3. **Circle at most two weeks** in the remediation table (Marking Sheet 3): the lowest, but with the priority order Week 23, Week 26, Week 22 breaking ties. Write a day and time for each redo next to the circle. *(5 minutes.)*
4. **The README's small job at the computer: rerun the recall table with a changed chunk size.** Week 26's table cut at 30, 60, 120 and 250 words. Cut at **20, 45 and 90** words (overlaps of 5, 10 and 20 words), using your Week 26 files, and **predict each row before you run it**: will recall@1 rise or fall, and will the share of the notebook sent at k = 3 rise or fall? Then write two sentences: what the table shows, and what ten questions cannot tell you. *(Estimated 15 minutes.)*
5. **One sentence in the Bug Log**: *"The answer I was most surprised to get wrong was ___, because I thought ___."* *(5 minutes.)*

**Next time you bring:** the marked paper, the grid, the circled table, the new chunk table. If a student comes back having *redone* a week's page already, that is a lovely surprise; do not insist on it.

---

## 🔑 Answer Key

> **How this key is laid out.** **Marking Sheet 1** is the student's marking sheet: *print only the block between the two ✂ lines*. **Marking Sheet 2** is the per-week grid. **Marking Sheet 3** is the remediation table. Then comes everything for **you**: the wrong-option map for Section A, the marking notes for B-E, the model answers, and the answers to every question posed in the lesson. The B outputs come from running the preamble and B1-B8 (Block P7 below); the C outputs from the Clinic; the D numbers from Block P5; the E numbers from the Week 19 guide and Blocks P2-P3.

The B programs, run exactly as printed on the paper (the preamble first), produce the outputs on Marking Sheet 1. **Block P7** is that run, with the outputs in order, so that you have the real text in front of you:

**Block P7 — the paper's B1-B8, run in one session (the same text as the paper)**

```python
# b_all.py - Week 27: Section B as printed on the paper, in order (preamble first).
import re
import numpy as np
import torch
import torch.nn.functional as F
from collections import Counter


def run(x, residual):
    for _ in range(3):
        f = 0.1 * x
        x = x + f if residual else f
    return x
print("B1:", round(run(1.0, True), 3), round(run(1.0, False), 3))

s = "aaabdaaabac"
pairs = Counter([s[i:i + 2] for i in range(len(s) - 1)])
print("B2:", pairs.most_common(2))
print("B2:", s.replace("aa", "X"))

N = np.array([1e3, 1e4, 1e5])
L = np.array([8.0, 4.0, 2.0])
slope, intercept = np.polyfit(np.log10(N), np.log10(L), 1)
print("B3:", round(slope, 3), round(10 ** intercept))

print("B4:", round(F.logsigmoid(torch.tensor(0.0)).item(), 4), round(-F.logsigmoid(torch.tensor(2.0)).item(), 4))


class OverBudget(Exception):
    pass


class Guard:
    def __init__(self, limit):
        self.limit = limit
        self.spent = 0.0

    def charge(self, cost):
        self.spent += cost
        if self.spent > self.limit:
            raise OverBudget("stop")


guard = Guard(1.0)
calls = 0
try:
    for _ in range(10):
        calls += 1
        guard.charge(0.4)
except OverBudget:
    print("B5:", "stopped at call", calls, "spent", round(guard.spent, 1))

scores = torch.tensor([2.0, 1.0, 0.5, 3.0])
allowed = torch.tensor([True, True, True, False])
masked = torch.where(allowed, scores, torch.tensor(float("-inf")))
print("B6:", scores.argmax().item(), masked.argmax().item(), F.softmax(masked, dim=-1)[3].item())

a = np.array([3.0, 4.0])
b = np.array([4.0, 3.0])
print("B7:", round(float(a @ b / (np.sqrt(a @ a) * np.sqrt(b @ b))), 2))
sc = np.array([0.2, 0.9, 0.5])
print("B7:", np.argsort(-sc)[:2])

cited = set(re.findall(r"\[(\d+)\]", "see [2] and [7] and [2]"))
served = {"2", "5", "9"}
print("B8:", sorted(cited), cited <= served, cited - served)
```
```text
B1: 1.331 0.001
B2: [('aa', 4), ('ab', 2)]
B2: XabdXabac
B3: -0.301 64
B4: -0.6931 0.1269
B5: stopped at call 3 spent 1.2
B6: 3 0 0.0
B7: 0.96
B7: [1 2]
B8: ['2', '7'] False {'7'}
```

### Marking Sheet 1 — The marking sheet (the one page the student may keep)

✂ PRINT FROM HERE

**Marking sheet — Term 3 Checkpoint.** Use a different colour. For every question, put the marks you earned in the margin. For B-E, mark the *working* too: the sheet says how many marks each step is worth.

**Section A (1 mark each).**

| Q | Ans | Why |
|:--:|:--:|---|
| A1 | **B** | An ablation deletes one part, retrains with everything else the same, and compares validation loss. |
| A2 | **C** | With no mask the model can read the answer it must predict: a leak. The loss says nothing about the mask's value. |
| A3 | **A** | On copy another head covers for the one switched off (redundant); on lookup nothing covers for that head. |
| A4 | **D** | Every text is a list of bytes 0-255, so decode(encode(text)) returns the text exactly, emoji and empty string included. |
| A5 | **B** | A merge step takes the most common neighbouring pair and gives it a new token number. |
| A6 | **C** | A straight line on log-log paper means multiplying `N` by a fixed factor multiplies the loss by a fixed factor (a power law). |
| A7 | **A** | An extrapolation is a prediction; you check it by training that model. |
| A8 | **D** | `C ≈ 6ND`: same `N`, double `D`, double `C`. |
| A9 | **B** | Different sets of guesses, different averages; `4.0407` vs `3.8008` is not evidence one model is worse. |
| A10 | **C** | Only differences matter; adding 100 to all rewards changes nothing. |
| A11 | **A** | At `beta = 5` the policy stayed near the start (KL `0.566`, `A = 0.589`); its small loss is a different scale. |
| A12 | **D** | 50.0% of 32 = 16 fields; 43.8% = 14; two fields. |
| A13 | **B** | So nobody can tune the cases to the prompt; a score change then means the prompt changed. |
| A14 | **C** | The script gives more credit to rules and examples. Stand-in, not a model. |
| A15 | **A** | Weights are fixed at prompt time; the behaviour comes from training. |
| A16 | **D** | A mask guarantees the shape, not the sense: the values can still be wrong. |
| A17 | **B** | Different spellings are different columns; the word table has no geometry. |
| A18 | **C** | Within a question or two at recall@1; the hard zero is the clear failure. |
| A19 | **D** | The writer named a note it was handed. That is all a passing check proves. |
| A20 | **A** | Quote the stranger number and say who wrote the questions. |

**Section B (2 marks each; 1 mark per correct printed item unless noted).**

| Q | Output | Working |
|:--:|---|---|
| B1 | `1.331 0.001` | With the residual road each step multiplies by 1.1: `1.1³ = 1.331`. Without it, each step replaces `x` by `0.1 x`: `0.1³ = 0.001`. [1 each] |
| B2 | `[('aa', 4), ('ab', 2)]` then `XabdXabac` | `Counter` counts every neighbouring pair, so `aaab` holds `aa, aa, ab`: in all four `aa` and two `ab`. `replace` is left to right without overlap: `aaab` → `Xab`. [1 for each line] |
| B3 | `-0.301 64` | Losses halve each time `N` is ×10: slope `log10(0.5) = -0.301`. `10 ** intercept` is the loss at `N = 1`: `8 × 10^(0.301 × 3) = 64`. [1 each] |
| B4 | `-0.6931 0.1269` | `logsigmoid(0) = ln 0.5 = -0.6931` (negative of the loss). `-ln sigmoid(2) = -ln 0.8808 = 0.1269`. [1 each] |
| B5 | `stopped at call 3 spent 1.2` | After call 2: 0.8, under 1.0. Call 3 reaches 1.2 and trips the guard: it stops one call late. [1 for `3`, 1 for `1.2`] |
| B6 | `3 0 0.0` | Raw argmax is the 3.0 at place 3. The mask sets place 3 to `-inf`, so the best allowed is place 0 (2.0), and the softmax gives place 3 exactly 0. [1 for `3 0`, 1 for `0.0`] |
| B7 | `0.96` then `[1 2]` | `a·b = 24`, both lengths 5: `24 / 25 = 0.96`. The two best of `[0.2, 0.9, 0.5]` are places 1 and 2. [1 each] |
| B8 | `['2', '7'] False {'7'}` | Cited is `{'2', '7'}` (a set: the repeated 2 counts once). Not inside served; `7` was never served. [1 for the sorted list, 1 for `False {'7'}`] |

**Section C (3 marks each: 1 what is wrong, 1 what happens, 1 the fix).**

| Q | What is wrong | What happens | Fix |
|:--:|---|---|---|
| C1 | The loss is `logsigmoid(gap)` with no minus; it is the log of a chance, so it is zero or below | Minimising it pushes the winner *behind*: the gap is `-18.64` and the loss is negative | `loss = -F.logsigmoid(r[0] - r[1])` |
| C2 | `.` does not match a line break and the record spans lines | `re.search` returns `None`; `.group` on `None` raises `AttributeError` | add `re.S` |
| C3 | The index rows are not normalised: a dot product rewards length | Note 0 (score 3) beats note 1 (score 1) though note 1 points exactly at the question | divide every row (and the query) by its length once |
| C4 | `np.argsort` sorts smallest first | It returns the three *lowest* scores (ids `2 0 4`) | `np.argsort(-scores)[:k]` |

**Section D.**

*D1 (5):* **[1]** `u·v = 8`; **[1]** the two lengths `3` and `3`; **[1]** `cos(u, v) = 8 / 9 = 0.889`; **[1]** `u·w = 3` and `|w| = sqrt 5 = 2.236`; **[1]** `cos(u, w) = 3 / (3 × 2.236) = 0.447`. (c) `v`. *Follow-through:* a wrong length used correctly loses the length mark only.

*D2 (5):* **[2]** three terms `0.4159`, `0`, `-0.1386` (one mark if one term is wrong); **[1]** sum `0.2773`; **[1]** `KL(p‖p) = 0` (every ratio is 1, `ln 1 = 0`); **[1]** `KL(q‖p) = 0.3466`, and it is **not** the same as 0.2773. *Follow-through:* (c) is marked from the student's own working.

*D3 (5):* **[1]** `2400 / 800 = 3.0`, **[1]** goes **up** (fewer tokens for the same bytes); **[1]** slope `-0.477` (each step of ×10 multiplies the loss by `1/3`; `log10 3 = 0.477`); **[1]** predicted `0.333`, and it is **not** a measurement (a prediction to check by training that model); **[1]** `6 × 10^6 × 2×10^7 = 1.2×10^14`.

*E (12):* **E(a) [3]** the order by validation loss is no norm `1.478` (below the full model's `1.673`, so "harmless here"), then no positions `1.739` (+0.066), then no residual `2.679` (+1.006). **[1]** puts no norm first (or says it did not hurt), **[1]** puts positions before residual (residual is the worst), **[1]** says the no-mask row is **not ranked** because its `0.077` is a leak (the model reads the answer; the sample is `tatatattt`). *(Accept no norm placed differently provided the student says what they are doing with it.)* **E(b) [2]** any two of: one model, one dataset and only two seeds; the gap is larger (`0.327` against `0.076`), so the train number is doing something the validation number does not show; the validation gain is small compared with how far it is from understanding why (the Week 19 guide says we did not find out); the full model's two seeds differ by `0.030`. **E(c) [3]** **[1]** Table 2 shows `1.00` on ten questions written in the notebook's own words but `0.20` / `0.50` / `0.60` on a stranger's; **[1]** quote the stranger row (or both, with who wrote them); **[1]** "who wrote the questions?" (or "how many questions? one question is `0.10`"). **E(d) [4]** **[1]** 250-word chunks send 718 words, 104% of the notebook, so the retriever has stopped choosing (and a model would be told everything); **[1]** 60-word chunks send 26% and reach 1.00 at k = 3; **[1]** `0.10` is one question of ten, so `0.90` against `1.00` cannot be told apart; **[1]** one check: more questions, written by other people, in other words.

✂ PRINT TO HERE

### Marking Sheet 2 — The per-week grid (print this, with Sheet 3)

| Week | Topic | Questions | Marks available | Marks earned | % | Redo if marks ≤ | Circle? |
|:--:|---|---|:--:|:--:|:--:|:--:|:--:|
| 19 | Ablations; the mask leak; heads and the switch-off test | A1-A3, B1, E(a), E(b) | **10** | | | 6 | |
| 20 | BPE: bytes, merges, bytes per token | A4, A5, B2, D3(a) | **6** | | | 3 | |
| 21 | The log-log line; extrapolation; `6ND` | A6-A8, B3, D3(b-d) | **8** | | | 4 | |
| 22 | Masked loss; Bradley-Terry; KL; the leash | A9-A11, B4, C1, D2 | **13** | | | 7 | |
| 23 | The harness: floor, frozen set, stand-in, guard | A12-A14, B5, C2 | **8** | | | 4 | |
| 24 | In-context examples; logit mask; schemas | A15, A16, B6 | **4** | | | 2 | |
| 25 | Embeddings: cosine; recall; what dense does and does not show | A17, A18, B7, C3, D1 | **12** | | | 7 | |
| 26 | RAG: top k, citations, recall on strangers, chunk size | A19, A20, B8, C4, E(c), E(d) | **14** | | | 8 | |
| | **Total** | | **75** | | | | |

*(10 + 6 + 8 + 13 + 8 + 4 + 12 + 14 = 75; Block P6 checks this. "Redo if marks ≤" is 60% of the week's marks, rounded down. Weeks 20 and 24 are thin: a flag there means "ask the spoken check first".)*

### Marking Sheet 3 — The remediation table (print with Sheet 2)

Circle at most **two** weeks. Priority order if there is a tie: **Week 23, Week 26, Week 22**. Each redo is 20 minutes plus the spoken check. **Weeks 19, 20, 21 and 24 point at their own workbook pages below.**

| Week | Redo this (20 min) | The teacher's spoken check (the student answers aloud, no paper) | Why Term 4 needs it |
|:--:|---|---|---|
| 19 | Workbook **Page 19.3** (the leak, by hand) and **Page 19.6** (switch it off) | "The no-mask model scores 0.077. Is the mask a bad idea?" → *no: it reads the answer; a leak* | The leak and the switch-off test are how Week 31 decides a fine-tune "worked". |
| 20 | Workbook **Page 20.2** (merge by hand) and **Page 20.5** (bytes per token as the text grows) | "What does one merge do, and what happens to bytes per token as merges are learned?" → *joins the most common neighbouring pair; it rises* | Week 29's cost arithmetic counts tokens. |
| 21 | Workbook **Page 21.1** (the straight-line trick) and **Page 21.3** (predict, then check) | "Loss 9, 3, 1 at ×10 steps: what is the line, and is a prediction a measurement?" → *slope -0.477; no, a prediction to check* | The capstone's cost budget uses `6ND`. |
| 22 | Workbook **Page 22.1** (the mask) and **Page 22.3** (KL on paper, and DPO on one pair) | "Masked loss is higher than unmasked. Is that worse?" → *no: a different set of guesses* | Week 31 fine-tunes with a leash and watches a regression. |
| 23 | Workbook **Page 23.2** (the floor, by hand) and **Page 23.5** (the guard that stops one call late) | "A prompt scores 50% and the constant answer 43.8%: what have you shown, and why does the guard stop one call late?" → *two fields, not much; it checks the bill after each call* | **Week 28's six fences and Week 29's cost both reuse the guard; Week 30's evals reuse the frozen set.** |
| 24 | Workbook **Page 24.1** (the ceiling) and **Page 24.4** (the mask, hand softmax first) | "A mask forces valid JSON. What is still wrong?" → *the values; shape, not sense* | Week 28's `validate_args` makes the same promise and the same mistake possible. |
| 25 | Workbook **Page 25.1** (cosine cards) and **Page 25.4** (recall, the control, and what the table does not show) | "Why does a long vector beat a close one on a plain dot product, and what fixes it?" → *length; normalise once* | Week 29's mini RAG uses cosine. |
| 26 | Workbook **Page 26.1** (Citation Court) and **Page 26.3** (recall on your own questions) and **Page 26.4** (chunking) | "Recall is 1.00. What is your first question?" → *who wrote the questions? Then: a valid citation proves what?* → *the writer named a note it was handed* | **Week 29 is Week 26's "retrieved text is data" turned into an attack.** |

### The workbook's own practice pages (Workbook Pages 27.1-27.6 are not the marking sheets above)

The workbook pages are practice on numbers that are not the paper's; every figure below was re-run from the workbook's own check files. **Workbook 27.1:** cosines `1.000`, `0.596`, `-1.000` for cards A, B, C; `KL(p from r) = 0.1838` against `KL(r from p) = 0.1920` (not equal, so say "from which"); `KL(p from p) = 0`; pair losses `0.0486`, `0.6931`, `3.0486` at gaps `+3`, `0`, `-3`; bytes per token `2.0` then `3.0`; slope `-0.452` and a prediction of `0.283` at 10,000,000 (a prediction, not a measurement); `6ND = 1.2 x 10^14`; field score `65.6%` against a floor of `53.1%` (4 fields); top three ids `[3, 0, 2]`. **Workbook 27.2:** gaps `0.10, 0.02, 0.30, 0.30` (full, no mask, no positions, no norm); no mask is a leak; one question is `0.10` of ten and `0.125` of eight. **Workbook 27.3:** the practice marks `[8, 2, 5, 6, 7, 3, 10, 9]` total 50 of 75 and flag Week 20 (33%) and Week 22 (46%); its grid has the same 10, 6, 8, 13, 8, 4, 12, 14 marks as Marking Sheet 2. **Workbook 27.4:** 688 notebook words; windows of 20 / 5, 45 / 10 and 90 / 20 give `46, 20, 10` windows, `913, 878, 868` words stored (`1.33, 1.28, 1.26` times the notebook), and at most `60, 135, 270` words sent at k = 3. **Workbook 27.5:** **A** swapped roles in KL print `0.192` for a value that should be `0.1838`, and `KL(p from p)` still prints `0.0`, so that test cannot fail; **B** `ZeroDivisionError: division by zero` on an empty text; **C** mixing `ln` and `log10` gives a slope of `-1.04` and a prediction of `0.073` instead of `-0.452` and `0.283`.

### Teacher-only: the map of wrong answers in Section A

| Q | Wrong option | It usually means |
|:--:|---|---|
| A1 | A / C / D | Thinks of training-time knobs, speed, or adding; has not got "delete and compare". |
| A2 | A / B | Reads a loss as a score. D: thinks a loss has a floor at 1. |
| A3 | B / D | B: reads a drop as a bug. D: takes a stripe for a proof. |
| A4 | A / B / C | Does not see that bytes make every text representable. |
| A5 | A / C / D | Thinks of compression as deletion or randomness. |
| A6 | A | Semi-log by mistake (constant *amount* per step). D: assumes exponent 1. |
| A7 | B / C / D | B/C: a fit is not a measurement. D: too timid; prediction is allowed. |
| A8 | B / C | B: squares; C: inverts. |
| A9 | A / C / D | A: a bigger number is worse. D: invents a rule. |
| A10 | A / B / D | Reads a reward as a grade, a label or a confidence. |
| A11 | B / C / D | B: compares losses across setups. C/D: confuses movement with failure. |
| A12 | A / B / C | C: subtracts percentages (`6.2`) and rounds. |
| A13 | A / C / D | Has not met leakage of the test into the design. |
| A14 | A / B / D | Treats the stand-in as a finding. D: distrusts the tool. |
| A15 | B / C / D | Confuses prompt time with training time. |
| A16 | A / B / C | Believes a format guarantee is a correctness guarantee. |
| A17 | A / C / D | Does not see the column picture. |
| A18 | A / B / D | A: the headline the week was built to prevent. |
| A19 | A / B / C | A/B: a citation as proof of truth. C: 'safe to obey' is Week 29. |
| A20 | B / C / D | B: quotes the flattering number. C: averages the un-averageable. D: gives up. |

### Teacher-only: marking notes for B, C

- **B2 is the trap.** A student who writes `[('aa', 2), ('ab', 2)]` has counted non-overlapping pairs; `[('aa', 4), ('ab', 2)]` is right. Give one mark for the second line alone if the first is wrong. `XabdXabac` wrongly written as `XXbdXXbac` means they replaced every `a`.
- **B3.** Accept `64.0` as well as `64`. A student who writes `-0.301` and leaves the second blank earns 1.
- **B5.** The number 1.2 may appear as `1.2000000000000002` only if they forget `round`; the printed answer is `1.2`.
- **B6.** The third value is `0.0` (not `0`, not `0.00`); give it if the student writes `0`.
- **C1 is the one most often marked 1/3.** The student says "the loss isn't going down" (true, but it does go down: to -17). Give the first mark only if they say the sign is wrong or the direction is reversed.
- **C2.** A student who proposes `re.DOTALL` has found the long name for `re.S`: give the mark.
- **C3.** A fix that only reverses the ranking ("take the smallest") earns the first two marks but not the third.
- **C4.** A fix `sorted(range(len(scores)), key=lambda i: -scores[i])[:k]` earns full marks.

### Teacher-only: follow-through and exemplars for E

**E(a), a full-mark answer.** *"Least to most harmful: no norm (1.478, actually better than full), no positions (1.739, a bit worse), no residual (2.679, much worse). I haven't ranked no mask because 0.077 is a leak: with no mask it can look at the next letter, which is the answer it has to predict, and its sample is tatatattt."* Credit the ranking even if 'no norm' is placed last as 'least harmful' in a different wording.

**E(b), a full-mark answer.** *"It's one small model and only two seeds (1.478 and 1.453 against 1.673 and 1.643, so it is consistent but small). And the gap between train and validation is much bigger without the norm (0.327 against 0.076), so it may be fitting the training text harder; it might get worse with more steps (a guess to test, not something the table shows)."*

**E(c), a full-mark answer.** *"Table 2 shows 1.00 only for questions written in the notebook's own words; for a stranger's it is 0.20 at k = 1 and 0.60 at k = 5. I would quote the stranger's row because it is nearer to real users. Before trusting any recall number I'd ask who wrote the questions, and how many there were, since one question is 0.10."* **A 2/3 answer.** *"It doesn't work for strangers, 0.20."* (One fact, no quote-choice reason or question.) **A 1/3 answer.** *"1.00 is good."*

**E(d), a full-mark answer.** *"250-word chunks send 718 words, more than the whole notebook, so recall is 1.00 because nothing is left out, not because the search is choosing. 60-word chunks get 1.00 at k = 3 and send 26%. 0.10 is one question in ten, so 0.90 against 1.00 doesn't tell them apart. I'd write twenty more questions in other words and re-run the table."*

### Answers to every question posed in the lesson

| In the lesson | Answer |
|---|---|
| *"Questions?"* (Hook) | Logistics only. |
| *"Read it again" / "Write what you do know"* | The only legal prompts; nothing else. |
| **Harder variation:** D3(b) with 2.0 instead of 3.0 at `N = 100,000` | The three points `9, 2, 1` are **not** on a line (`log10` of the losses: `0.954, 0.301, 0`: the steps are `-0.653` and `-0.301`). Before predicting the loss at ten million you would check the line: train another model, or several seeds, and see whether the middle point was noise. A prediction from two points is an anecdote. |
| **Homework 4:** the chunk-size sweep | Block P3's rows: 20/5 `0.60 / 0.90 / 1.00` (9% of the notebook); 45/10 `0.90 / 1.00 / 1.00` (20%); 90/20 `1.00 / 1.00 / 1.00` (39%). Recall@1 rises with window size; so does the words sent. Ten questions cannot tell `0.90` from `1.00`. |

---

## 🔮 Next Week Preview

This section shows what the next week builds on, so you can see which of today's results matter most.

**Week 28 — Tools and the Loop** (🟦 teach). A tool is a function plus a contract; the model only asks and your code acts. The loop is perceive, decide, act, observe, stop, with six fences that fire with no model present. The new ideas are a safe calculator built on `ast.parse` and an `operator` whitelist, a sandbox test with `Path.resolve()` and `is_relative_to`, `isinstance` checks before a tool runs, and `ThreadPoolExecutor` so a timeout can be enforced. There is no new maths. The "model" in Week 28 is again a **stand-in, not a model** (a scripted agent); the student has met that honesty rule in Week 23 and Week 26.

The first fence, the safe calculator, starts from this one line (teacher-only; `ast` is a Week 28 construct and is not on today's paper):

```python
# preview28.py - Week 27 (preview of Week 28, TEACHER-ONLY): what ast.parse makes of a sum. Week 28 walks this tree and refuses anything that is not a number or an operator.
import ast
print(ast.dump(ast.parse("2 + 3 * 4", mode="eval").body))
```
```text
BinOp(left=Constant(value=2), op=Add(), right=BinOp(left=Constant(value=3), op=Mult(), right=Constant(value=4)))
```

**What from today carries over:** the floor and the frozen set (Week 23) become the agent's scorecard; the budget guard that stops one call late (Week 23) becomes a fence; the citation check in code (Week 26) is the model for "verify in code, do not trust the model"; and "retrieved text is data" (Week 26) is the sentence Week 29 attacks. **If the grid shows Weeks 23, 26 or 22 under 60%, those are the redos to do before Week 28.** Nothing else from Term 3 is on the critical path.
