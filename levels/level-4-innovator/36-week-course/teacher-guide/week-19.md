# Week 19 — Open the GPT: Heads, Ablations, Synthetic Tasks

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Student Guide](../student-guide/week-19.md) · [Workbook](../workbook/week-19.md)

![Growing map of all 36 weeks in four term lanes: weeks 1 to 18 are solid, week 19 is tinted pink with a pointer, weeks 20 to 36 are dashed](../figures/fig-w19-0-where-this-fits.svg)

*Figure 19.0 — Week 19, Open the GPT, sits in term 2 on the road from memory to attention. Everything before it is built; everything after it is still ahead.*

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class (one 3.5-minute run of five models sits inside it), then the workbook (~60-75 min) |
| **Type** | 🟩 Lab — the student **takes the Week 17 TinyGPT apart**: deletes the mask, the positions, the residual road and the layer norm one at a time, retrains each, and fills a table; then trains tiny models on three made-up tasks (copy, reverse, lookup) and **names a head from its attention picture** |
| **Big idea** | "Every part of the GPT is needed" is a claim, and a claim can be tested: delete one part, retrain with everything else the same, and compare the **validation** loss. Today's table says four different things. Taking out the **residual road** wrecks the model (validation 2.68 against 1.67). Taking out the **positions** costs a little (1.74). Taking out the **layer norm** makes this small model *better* (1.48). Taking out the **mask** gives the best number of all (0.077) and is the one that proves nothing: the model is reading the answer. Then, on tasks small enough to see inside, the heads turn out to have simple jobs ("look six back", "look at the mirror place", "read the key just before me"), and a head's name is worth something only if a test could have shown it wrong. |
| **New vocabulary** | ablation · leak · synthetic task · attention weights (as a picture) · head card · redundant |
| **New maths** | **None.** The only arithmetic is `ln(8)`, a share (5 of 12 places), and differences of two losses. See the 🔢 box. |
| **New syntax** | **None** (the ladder row for Week 19 is empty). Everything typed is from earlier weeks: `if` switches, `nn.Identity()` (Week 6), keyword arguments with defaults, `nn.ModuleList`, `torch.randint`, `matplotlib` `imshow` (Level 2). See section 4 for the few things to watch. |
| **Dataset** | Two kinds. **Text:** the shared kit's typed corpus `l4lib.corpus.TEXT` (6,972 characters, 28 distinct; train 6,274 / validation 698), exactly as in Week 17. **Made-up tasks:** numbers generated on the spot by `torch.randint` and `torch.randperm`; nothing is stored. **Nothing downloads. No internet.** |
| **Model** | **Real models, really trained, no stand-ins.** Text: the Week 17 TinyGPT (807,196 knobs; width 128, 4 heads, 4 blocks, 64 places) trained five times for **800 steps** each (Week 17 used 1,500). Tasks: a small GPT of **101,641 knobs** (copy, reverse) or **102,545** (lookup): width 64, 2 heads, 2 blocks. **There is no scripted backend anywhere in this week.** |
| **Materials** | Laptop with Python 3, torch and matplotlib (all already installed) · the folder containing `l4lib/` and the student's Week 17 `tinygpt.py` · four printed **Head Detective** cards and five shuffled sample cards (Activity) · workbook pages 19.1-19.6 · a timer |
| **Prep time** | 30 minutes the night before (the longest run is 3.6 minutes) · 3 minutes on the day |
| **Expected runtime of the code** | `text_ablate.py` **about 3.6 minutes** (measured 216 s on the author's CPU, one thread: 39-43 s per model) · `task_table.py` **about 46 s** · `heads.py` 4 s · `heads_more.py` 7 s · `key.py` 7 s. Teacher-only `key_seed.py` ~3.7 minutes and `key_lookup.py` ~2.6 minutes. If `text_ablate.py` takes over **8 minutes**, something is wrong (see Fallback). |

> **⚠️ Watch out:** three things go wrong this week. **First, the mask row looks like a triumph.** Validation 0.077 against 1.673 is the best number in the table and the model is cheating: with no mask, place 5 can read place 6, which *is* its answer. Its sample is `tatattttttt...`. A student who writes "removing the mask makes it 20 times better" has read a loss as a score. The leak test in section 6 turns the suspicion into a measurement. **Second, "we deleted it and nothing broke" is not "it is not needed".** The no-norm text model is *better* than the full one (1.478 against 1.673), and on the lookup task the no-position model scores 1.00. Both are results about one small model on one small task, at 800 or 600 steps, on one or two seeds. We do not know *why* no-norm is better (section 7, limit 6). **Third, the head names are stories until tested.** All four heads of the copy model look exactly six places back, and switching off any *one* of them changes nothing: a camera pointed at a head tells you where it looks, not whether the model needed it. The "switch it off" test is the evidence, and it is the part the student must not skip.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say what an ablation is and what makes one fair**: delete one thing, change nothing else (same seed, same steps, same data), and compare on text the model was *not* trained on.
2. **Fill the ablation table** at 800 steps (five rows: full, no mask, no positions, no residual, no norm) and write one honest sentence per row, including the row where a *loss* is not a *score*.
3. **Explain a leak**: why the no-mask model's 0.077 is a cheat, using the sample (`tatat...`) and the future-change test (change one later token; do earlier scores move?).
4. **Train a model on copy, reverse and lookup** and say what score chance would get (copy and reverse: 1 in 8 = 0.125; lookup: 1 in 10 = 0.1) and what the trained model gets (1.00).
5. **Name one head from its picture** (e.g. "layer 0 head 0 of the copy model looks six places back") and write **what evidence would prove the name wrong**: switch it off and see whether accuracy falls; or find an input where it looks somewhere else.

Observable evidence: `text_ablate.py` printing five rows; `task_table.py` printing a three-by-five grid; `heads.py` saving `copy_heads.png`; the **Head Detective** cards named and each given a kill-test; and the workbook's written answer to *"what would prove your name wrong?"*

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist** is a *whole file* and every one was run, from one folder next to `l4lib/`, on a CPU with `torch.set_num_threads(1)` and the seeds shown. Blocks in the **🐞 Debugging Clinic** are *deliberate mistakes* and each is marked; their tracebacks are real. Outputs are real. Everything is seeded, and the losses, accuracies and samples printed here were identical on a second run of each file; **only the `(N s)` timings change**. The numbers labelled **ledger** come from the course author's reference run of Module 3 (1,500 steps, dropout 0.1, a different implementation) and were **not** run for this lesson; they are a comparison in *direction*, not a target.

### 1. What the student is doing today, in one paragraph

Last week they built and trained the TinyGPT and found a gap between what it does on text it studied and text it did not. Today they take it apart. They copy their Week 17 model and add four on/off switches, one for each of the mask, the place table, the residual road and the layer norms. They train the model five times on the typed text (all switches on, then each one off in turn) and write down train loss, validation loss and a 70-character sample for each. While that runs (3.6 minutes) they build three made-up tasks whose right answers they know: **copy** (say back the six symbols you were given), **reverse** (say them backwards), and **lookup** (four key-value pairs, then a key: say its value). On these the whole model is tiny enough to look inside: they draw the attention weights of each head as a picture, name what one head does, and then test the name by switching that head off. **Nothing in the lesson is a chatbot and nothing is a stand-in: the models are real and small, and what they do on made-up numbers tells you about those models and nothing about larger ones.**

### 2. 🔢 The maths you need — taught to you first

**There is no new mathematical idea this week.** Four pieces of arithmetic; do them before class.

**(a) Chance on the made-up tasks.** The copy and reverse symbols are drawn from 8 symbols (0-7), so a model that guesses the answer place by place is right **1 time in 8 = 0.125**. Its loss on one answer is `ln(8) =` **2.079** (Week 17: `ln` of the number of choices). The lookup answer is a digit 0-9: a guess is right **1 in 10 = 0.1**; a model that worked out that the answer must be one of the four values on the page would get `1/4 + 3/4 x 1/10 =` 0.325, not 0.25, because two pairs can hold the same digit (workbook 19.4). A trained model that scores 1.00 is not guessing.

**(b) A loss floor you can calculate.** If the copy model is scored on *every* place and not only the six answers (Clinic 2), five of the twelve places are random symbols nobody can predict (places 1-5 of the window; the first symbol is never predicted because it is an input), each worth `ln(8)`. The best possible average is `5 x ln(8) / 12 =` **0.866**. The run gets 0.872. This is why a "loss that will not go below 0.87" is a correct result, not a bug.

**(c) Differences of two losses.** Each row of the ablation table is compared with the full model by subtraction, on validation loss: no positions 1.739 - 1.673 = **+0.066** (worse), no residual 2.679 - 1.673 = **+1.006** (much worse), no norm 1.478 - 1.673 = **-0.195** (better), no mask 0.077 - 1.673 = **-1.596** ("better", and a leak). A difference is only worth reading if it is bigger than the run-to-run wobble; the second seed (section 6) moves each validation loss by 0.01-0.03 and leaves every sign unchanged.

**(d) The size of the task models**, by Week 16's formula with the vocabulary and places of the task: copy and reverse (vocabulary 9, 12 places, width 64, 2 blocks) = **101,641** knobs; lookup (vocabulary 17, 10 places) = **102,545** (both printed by `key.py`). You will not be asked for these; they tell you that the task models are one eighth the size of the text model.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| In the lesson | Status |
|---|---|
| Every model, every loss, every accuracy, every attention picture | **Real**: PyTorch models trained on your CPU this session. |
| Any scripted stand-in (`FakeClient` or similar) | **None used this week.** |
| The corpus | The author's own typed text (6,972 characters), as in Week 17. |
| The copy, reverse and lookup tasks | **Generated numbers**, not language. They are chosen because the right mechanism is known, so a head's job can be checked. |
| The "ledger" figures (no residual +1.570, no positions +0.354) | **Reference-run figures, not run today**: 1,500 steps, dropout 0.1, a different implementation of the same model. Same ordering of the two biggest effects as today; different sizes. |
| "Attention explains the model" | **Do not claim it.** The weights show where a head looked. Whether the model *needed* the look is a separate test (switch the head off). On the copy task, a head that looks exactly where it should can be removed with no loss, because another head does the same job. |
| "This is how GPT-whatever works" | **Do not claim it.** We looked inside 100,000-knob models on made-up numbers. |

### 4. The constructs, for somebody who has never seen them

Week 19's ladder row is empty, so **nothing is taught**; these are the places where a new-looking line uses an old idea, so you can answer without searching.

- **`nn.Identity()`** (Week 6: the skip path). Used here to make "no layer norm" by replacing each `nn.LayerNorm` with a layer that hands its input back untouched.
- **A keyword argument with a default** (`mask_on=True`), the Week 1 pattern (`def run(*, lr, ...)`). Each switch is one of these; `TinyGPT(..., pos_on=False)` reads like English.
- **`torch.randperm(6)[:4]`** (Week 5 used `torch.randperm(n, generator=g)`): a shuffle of 0-5 and the first four. Here it makes **four different keys**; `torch.randint` would allow repeats (Clinic 3).
- **`weights[:, h] = 0.0`** (item assignment on a tensor, Level 2/3 indexing): the head switch inside `Block.forward`. It is for **testing a trained model** and would break training (Clinic 5).
- **`plt.imshow(w)`** (Level 2 matplotlib): a grid of numbers drawn as colours. Needs a **2-D** grid (Clinic 6).
- **`weights.detach()` in `Block.forward` (ahead of the ladder, flagged, not counted):** it is Week 22's `.detach()`. It stores the attention weights as plain numbers, cut off from the training graph, so `imshow` can draw them and training does not keep the graph alive. The given code uses it and the student text says "copy it; you meet it properly in Week 22". Do not teach it today.
- **Teacher-only, flagged:** `**sw` in `key_lookup.py` (unpack a dictionary into keyword arguments; it appears in the student Weeks 4-6 harness as `**kw`) and `exec(source)` in `key_seed.py`. Neither is in any student file.

### 5. The other code the student types — nothing new, but note these

- `ablate_model.py` is **Week 17's `tinygpt.py` with four `if`s**. The student types the four `if`s; `last_weights` and `silence` are given (you say "these two are for looking, not for training").
- `text_ablate.py` is **Week 17's `train.py` wrapped in a function `run(name, mask_on=True, ...)`** and called five times. It does not print the three checkpoints; it prints one line of numbers and a 70-character sample per model. The `estimate` function **resets the random dice to the same state for every model** (`torch.manual_seed(123)`, then puts the old state back), so all five models are scored on the same 20 batches. Without that, a difference of 0.03 could be a different draw of windows.
- `tasks.py` has **no `if __name__ == "__main__"`** (not in the ladder for student files): it defines functions and that is all. The table lives in `task_table.py`.
- `train_task` scores **only the answer places** (`logits[:, -k:, :]`), not every place. This is a real decision, and Clinic 2 shows what happens without it.

### 6. What the numbers will say

**The text table (800 steps, seed 0, one thread).** Printed by `text_ablate.py`:

| Model | Train | Validation | Gap | What to say |
|---|:--:|:--:|:--:|---|
| full | 1.597 | **1.673** | 0.076 | The baseline. Week 17's model at 800 steps instead of 1,500 (Week 17 reached 0.907 / 1.447). |
| no mask | 0.070 | **0.077** | 0.007 | **A leak.** The sample is `tatatattt...`. Not a result about the mask's value. |
| no positions | 1.451 | **1.739** | 0.288 | Fits the training text *better* (1.451 against 1.597), does *worse* on unseen text, and the gap is four times the baseline's. |
| no residual | 2.664 | **2.679** | 0.015 | **Wrecked**: it barely learns at all (the full model has 1.673). Train and validation agree because it has learned almost nothing to memorise. |
| no norm | 1.150 | **1.478** | 0.327 | *Better* than the full model on validation, with a much larger gap. **We did not find out why** (limit 6). |

**Is it luck?** `key_seed.py` repeats the whole table with seed 1. Every sign holds: full 1.643; no mask 0.085; no positions 1.717 (+0.074); no residual 2.711 (+1.068); no norm 1.453 (-0.190). The differences between the two seeds (0.01 to 0.03 on validation) are smaller than the effects of the three real ablations. The no-positions effect (+0.066 and +0.074) is the smallest: about twice the seed-to-seed difference of the full model (1.673 against 1.643, 0.030), so **say "small, and probably real; two seeds"**, not "proved". **Two seeds is all we ran.**

**Against the ledger (direction only).** The reference run at 1,500 steps (one seed) has the residual as the biggest damage (+1.570) and the positions second (+0.354). Today's run agrees that the residual is the worst and that removing positions hurts, but the positions effect is much smaller (+0.066) at 800 steps. The reference model also had dropout; ours does not. **We did not run 1,500 steps today**, so we do not know whether more training would widen the positions gap toward 0.354.

**The task table (600 steps, seed 0)**, printed by `task_table.py`; the entry is the share of answer tokens right on 1,000 fresh sequences:

| Task | full | no mask | no positions | no residual | no norm |
|---|:--:|:--:|:--:|:--:|:--:|
| copy | 1.00 | 1.00 | 0.95 | 1.00 | 1.00 |
| reverse | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 |
| lookup | 1.00 | **0.37** | 1.00 | 1.00 | **0.33** |

Three things to read, in this order. **(i) No mask on copy and reverse is 1.00 because of the leak again** (the input contains the answer one place ahead). **(ii) No positions costs 0.05-0.08 on copy and reverse, and nothing on lookup.** A causal model still has a weak sense of place (place 1 sees one token, place 6 sees six; Week 16, `masked.py`). **(iii) The lookup column is where the things that matter show up**: no mask 0.37 (not a leak: the window stops *before* the answer), and no norm 0.33 at 600 steps. `key_lookup.py` ran it over three seeds and two training lengths: **no mask stays at 0.35-0.37 at 600 and 1,500 steps on all three seeds**; **no norm is 0.33 on seed 0 at 600 steps and 1.00 everywhere else** (so it is *slower or unlucky*, not broken); no positions and no residual are 1.00 everywhere. **A one-layer lookup model gets 0.40 at 1,500 steps**, where the two-layer model gets 1.00: lookup needs two layers at this size, which is a result about the task (and we did not vary the width). **We did not find out why no mask breaks lookup.**

**The heads.** From `heads.py` and `heads_more.py` (model trained for 600 steps; 500 fresh sequences):

| Task | What the heads do | Switch-off test |
|---|---|---|
| copy | **All four heads** look exactly **6 places back** at the answer places (weights 0.99 in layer 0, 0.68-0.92 in layer 1) | One head off: 1.00 each. Both layer-0 heads off: **0.75**. Both layer-1 heads off: **1.00**. |
| reverse | All four heads look at the **mirror place** (answer place 6 looks at 5, 7 at 4, ... 11 at 0) | One head off: 1.00 each. Both layer-0 off: **0.57**. Both layer-1 off: **1.00**. |
| lookup | **L0 H0** looks one place back from each value place (1->0, 3->2, 5->4, 7->6, weight 0.97-0.98): each value reads the key just before it. **L1 H0 and L1 H1** at the asked-for key place look at the **right value** in **100%** of 500 sequences. | L0 H0 off: **0.48** · L0 H1 off: 1.00 · both layer-0 off: 0.35 · L1 H0 off: **0.80** · L1 H1 off: 1.00 · both layer-1 off: **0.19** |

The copy and reverse heads are **redundant**: look at the switch-off column. The lookup heads are **not**: L0 H0 off drops accuracy from 1.00 to 0.48. **Same picture (a bright stripe), different importance**; that is the entire argument for testing a name.

![Five horizontal bars of validation loss, one per TinyGPT with a part deleted, with a dashed line at the full model's 1.673 and crosses on the two that fail](../figures/fig-w19-1-ablation-bars.svg)

*Figure 19.1 — Deleting a part can make the score look better; a very low number needs a leak check before it is believed.*

![A grid of share of answers right: three tasks by five models plus a chance column, with ticks on 1.00, crosses on 0.37 and 0.33, and ringed numbers 1 and 2](../figures/fig-w19-2-task-table.svg)

*Figure 19.2 — A perfect score can be a leak; the lookup column is where deleting a part shows up, and its cause is still an open question.*

### 7. The honest limits of today

1. **One seed for almost everything**; two for the text table; three for the lookup column. No spread was measured on the heads.
2. **Small models, made-up numbers.** The heads of a 101,641-knob copy model say nothing about the heads of any other model.
3. **A loss is not a score when the model can see the answer.** The no-mask rows are leaks, not findings about the mask.
4. **"No damage" is a statement about one task.** No positions is 1.00 on lookup and worse on copy. Do not say "positions are not needed".
5. **800 steps, not 1,500.** Chosen so the table takes 3.6 minutes. The ledger's effect sizes (at 1,500) are different; today's are smaller for positions.
6. **We did not find out why the no-norm text model is better than the full one** (1.478 against 1.673 on seed 0, 1.453 against 1.643 on seed 1). Candidate stories (the model learns faster without the norms at this size; the norms interact with the small learning rate) were **not tested**. Say "better at 800 steps, in this small model, and we do not know why". The larger gap (0.327) is a reason not to prefer it: it fits the training text more and generalises relatively less.
7. **We did not find out why no-mask breaks lookup** (0.35-0.37) when it cannot see the answer.
8. **Attention weights are where a head looked, not what it did** with what it found. Only the switch-off test touches that.
9. **The silence test switches a head off after training.** It does not say what the model would have learned if the head never existed.

### 8. The misconceptions you will actually meet

- **"No mask is the best model."** The leak. Ask: *"what is in `x` at place 6, and what is the answer at place 6?"* (The answer is in `x` at place 7.)
- **"Positions do nothing" (because the no-position lookup model scored 1.00).** One task. Return to copy: 0.95 and 0.92.
- **"The head that looks six back is the head that copies."** All four look six back, and any one of them can go. *"Is a head that can be removed doing the work?"*
- **"If I remove the norm and it gets better, norms are useless."** Limit 6.
- **"The brighter the stripe, the more important the head."** The weights of L1 H0 and L1 H1 on the copy task are 0.68-0.92 and the layer can be removed entirely with no loss.
- **"The ablation table proves which part is most important."** One seed pair, one model, 800 steps.

### 9. How deep to go, and where to stop

Stop at: *"each row is one deletion; compare on validation; a loss that is too good is a leak; and a head's name is a claim with a test."* Do **not** go into why layer norm is or is not needed, into circuits, or into induction heads as a named mechanism (the lookup model finds the key, then the value: say that, and leave the name for the student who asks). Do not tell the student that heads in big models look like these. **We did not look at any.**

### 10. 🧭 Where Week 19 sits

| Week | What it gave | Used today |
|---|---|---|
| 6 | Residual road, layer norm, `nn.Identity` | Two of the four deletions; the Identity trick |
| 15 | The mask and the divide | Deleting the mask |
| 16 | Positions; `masked.py` (the mask leaks a little order) | Deleting the positions; copy no-pos 0.95 |
| 17 | TinyGPT, the first-loss check, the gap | The baseline; "train vs validation" is read from the table |
| **19** | **Deleting parts; synthetic tasks; naming a head** | |
| 20 | Pieces instead of characters (BPE); the only use of `tokenizers` | The text model is characters; the next week changes that |

---

## 🧰 Prep Checklist

### 30 minutes the night before

- [ ] **Confirm the stack.** Run from the folder that contains `l4lib/`:

```bash
python3 -c "import torch, matplotlib; print(torch.__version__, matplotlib.__version__)"
python3 -c "from l4lib.corpus import TEXT; print(len(TEXT), len(set(TEXT)))"
```

You should see (the digits may differ on another machine):

```text
2.2.1 3.7.1
6972 28
```

`pip` returning 403 is expected; **nothing this week installs anything.**

- [ ] **Type the files below into one working folder** (next to `l4lib/`). Each begins with a `#` comment naming it. Run each in order and compare with the output printed here.

**File 1 — `ablate_model.py`** (Week 17's `tinygpt.py` with four switches, plus two lines for looking inside). Prints nothing. The student types the four `if`s (`mask_on`, `res_on`, `ln_on`, `pos_on`); you give them `last_weights` and `silence`.

```python
# ablate_model.py - Week 19: Week 17's TinyGPT with four switches. Each switch deletes one component.
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)


class Block(nn.Module):
    def __init__(self, d, H, T, mask_on=True, res_on=True, ln_on=True):
        super().__init__()
        self.H = H
        self.mask_on = mask_on
        self.res_on = res_on
        self.ln1 = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d)
        self.register_buffer("mask", torch.tril(torch.ones(T, T)))
        self.ln2 = nn.LayerNorm(d)
        self.up = nn.Linear(d, 4 * d)
        self.act = nn.GELU()
        self.down = nn.Linear(4 * d, d)
        self.last_weights = None                                        # the latest attention weights, kept for looking at
        self.silence = []                                               # heads to switch off (used for testing, not training)
        if not ln_on:
            self.ln1 = nn.Identity()
            self.ln2 = nn.Identity()

    def forward(self, x):
        B, T, d = x.shape
        dh = d // self.H
        h = self.ln1(x)
        q = self.q(h).view(B, T, self.H, dh).transpose(1, 2)
        k = self.k(h).view(B, T, self.H, dh).transpose(1, 2)
        v = self.v(h).view(B, T, self.H, dh).transpose(1, 2)
        scores = q @ k.transpose(-2, -1) / dh ** 0.5
        if self.mask_on:
            scores = scores.masked_fill(self.mask[:T, :T] == 0, float("-inf"))
        weights = F.softmax(scores, dim=-1)
        for h_off in self.silence:
            weights[:, h_off] = 0.0                                    # this head now mixes in nothing
        self.last_weights = weights.detach()
        mixed = (weights @ v).transpose(1, 2).reshape(B, T, d)
        if self.res_on:
            x = x + self.proj(mixed)
            x = x + self.down(self.act(self.up(self.ln2(x))))
        else:
            x = self.proj(mixed)
            x = self.down(self.act(self.up(self.ln2(x))))
        return x


class TinyGPT(nn.Module):
    def __init__(self, V, d, H, L, T, mask_on=True, pos_on=True, res_on=True, ln_on=True):
        super().__init__()
        self.T = T
        self.pos_on = pos_on
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)
        self.blocks = nn.ModuleList([Block(d, H, T, mask_on, res_on, ln_on) for _ in range(L)])
        self.ln_f = nn.LayerNorm(d) if ln_on else nn.Identity()
        self.head = nn.Linear(d, V)
        with torch.no_grad():
            self.head.weight *= 0.1

    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok(idx)
        if self.pos_on:
            x = x + self.pos(torch.arange(T))
        for blk in self.blocks:
            x = blk(x)
        logits = self.head(self.ln_f(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(B * T, -1), targets.reshape(B * T))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, n_new, temperature=1.0):
        for _ in range(n_new):
            logits, _ = self(idx[:, -self.T:])
            probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)
            idx = torch.cat([idx, torch.multinomial(probs, 1)], dim=1)
        return idx
```

**File 2 — `text_ablate.py`** (five models, 800 steps each; **about 3.6 minutes**, 216 s measured)

```python
# text_ablate.py - Week 19: train the TinyGPT five times on the typed corpus, each time with one thing deleted. 800 steps each.
import math
import time
import torch
from ablate_model import TinyGPT
from l4lib.corpus import TEXT

SEED = 0
chars = sorted(set(TEXT))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in TEXT])
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]

d, H, L, T, B = 128, 4, 4, 64, 32
STEPS, WARMUP = 800, 50


def get_batch(split):
    src = train_data if split == "train" else val_data
    starts = torch.randint(len(src) - T, (B,))
    x = torch.stack([src[s:s + T] for s in starts])
    y = torch.stack([src[s + 1:s + T + 1] for s in starts])
    return x, y


@torch.no_grad()
def estimate(model, split, batches=20):
    saved = torch.get_rng_state()                        # the same 20 batches for every model, then put the dice back
    torch.manual_seed(123)
    total = 0.0
    for _ in range(batches):
        x, y = get_batch(split)
        _, loss = model(x, y)
        total += loss.item()
    torch.set_rng_state(saved)
    return total / batches


def run(name, mask_on=True, pos_on=True, res_on=True, ln_on=True):
    torch.manual_seed(SEED)
    model = TinyGPT(V, d, H, L, T, mask_on=mask_on, pos_on=pos_on, res_on=res_on, ln_on=ln_on)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: (s + 1) / WARMUP if s < WARMUP
                                              else 0.5 * (1 + math.cos(math.pi * (s - WARMUP) / (STEPS - WARMUP))))
    t0 = time.perf_counter()
    for step in range(STEPS):
        x, y = get_batch("train")
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
    seconds = time.perf_counter() - t0
    train_loss, val_loss = estimate(model, "train"), estimate(model, "val")
    torch.manual_seed(1)
    out = model.generate(torch.tensor([[stoi["t"]]]), 100, 0.8)[0].tolist()
    text = "".join(itos[i] for i in out).replace("\n", " / ")
    print(f"{name:<9} train {train_loss:.3f}  val {val_loss:.3f}  gap {val_loss - train_loss:.3f}  ({seconds:.0f} s)")
    print(f"          {text[:70]}")


run("full")
run("no mask", mask_on=False)
run("no pos", pos_on=False)
run("no res", res_on=False)
run("no norm", ln_on=False)
```

```text
full      train 1.597  val 1.673  gap 0.076  (43 s)
          the caros river the oxxunted bean the feewon as tolle the cacherd rsth
no mask   train 0.070  val 0.077  gap 0.007  (39 s)
          tatattttttttttattttaatttattattttttttatatttottatttaatattatataattattasat
no pos    train 1.451  val 1.739  gap 0.288  (43 s)
          t the wther saken thod wat do the wak feeron t did thery beacot thes w
no res    train 2.664  val 2.679  gap 0.015  (43 s)
          t te te cbr urot thdo iwaardobt gt ah leeeot as td ae tamteir t t rs w
no norm   train 1.150  val 1.478  gap 0.327  (41 s)
          the cast brout. / the old marked on the lepeor and dre thad cared did 
```

`estimate` scores every model on the **same** 20 batches (the dice are reset inside it and put back). The `(N s)` figures change from run to run; nothing else did. The samples are from `generate` with temperature 0.8 and a fixed seed. The `no mask` sample is a line of `t` and `a`: the model is not writing, it is reading.

**File 3 — `tasks.py`** (three made-up tasks and one trainer; prints nothing)

```python
# tasks.py - Week 19: three made-up tasks, one trainer. Every token is a number; nothing here is text.
import time
import torch
import torch.nn.functional as F
from ablate_model import TinyGPT

N = 6                       # symbols to copy or reverse
SEP = 8                     # the separator token for copy and reverse (symbols are 0..7)


def copy_batch(B, reverse=False):
    s = torch.randint(0, 8, (B, N))
    tail = s.flip(1) if reverse else s
    return torch.cat([s, torch.full((B, 1), SEP), tail], dim=1)          # 6 symbols, SEP, 6 answers = 13 tokens


def lookup_batch(B, P=4):
    keys = torch.stack([torch.randperm(6)[:P] for _ in range(B)]) + 10    # P different keys from 10..15
    vals = torch.randint(0, 10, (B, P))
    pairs = torch.stack([keys, vals], dim=2).reshape(B, 2 * P)            # k v k v k v k v
    pick = torch.randint(0, P, (B,))
    rows = torch.arange(B)
    return torch.cat([pairs, torch.full((B, 1), 16), keys[rows, pick][:, None], vals[rows, pick][:, None]], dim=1)


TASKS = {
    "copy": (lambda B: copy_batch(B), 9, 13, N),            # (batch maker, vocab, length, how many answers at the end)
    "reverse": (lambda B: copy_batch(B, reverse=True), 9, 13, N),
    "lookup": (lookup_batch, 17, 11, 1),
}


def accuracy(model, task, B=1000):
    make, V, length, k = TASKS[task]
    seq = make(B)
    with torch.no_grad():
        logits, _ = model(seq[:, :-1])
    guess = logits[:, -k:, :].argmax(dim=-1)
    return (guess == seq[:, -k:]).float().mean().item()               # share of answer tokens that are right


def train_task(task, steps=600, seed=0, L=2, H=2, mask_on=True, pos_on=True, res_on=True, ln_on=True):
    make, V, length, k = TASKS[task]
    torch.manual_seed(seed)
    model = TinyGPT(V, 64, H, L, length - 1, mask_on=mask_on, pos_on=pos_on, res_on=res_on, ln_on=ln_on)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.0)
    for step in range(steps):
        seq = make(64)
        logits, _ = model(seq[:, :-1])
        loss = F.cross_entropy(logits[:, -k:, :].reshape(-1, V), seq[:, -k:].reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return model, loss.item()
```

**File 4 — `task_table.py`** (three tasks, five models each; **46 s**)

```python
# task_table.py - Week 19: three tasks, five models each (full, then one thing deleted). 600 steps each. Prints the share of answers right.
import time
from tasks import TASKS, train_task, accuracy

t0 = time.perf_counter()
print(f"{'task':<9}{'full':>7}{'no mask':>9}{'no pos':>8}{'no res':>8}{'no norm':>9}")
for task in TASKS:
    row = [accuracy(train_task(task)[0], task),
           accuracy(train_task(task, mask_on=False)[0], task),
           accuracy(train_task(task, pos_on=False)[0], task),
           accuracy(train_task(task, res_on=False)[0], task),
           accuracy(train_task(task, ln_on=False)[0], task)]
    print(f"{task:<9}" + "".join(f"{a:>{w}.2f}" for a, w in zip(row, (7, 9, 8, 8, 9))))
print(f"{time.perf_counter() - t0:.0f} s for the whole table")
```

```text
task        full  no mask  no pos  no res  no norm
copy        1.00     1.00    0.95    1.00     1.00
reverse     1.00     1.00    0.92    1.00     1.00
lookup      1.00     0.37    1.00    1.00     0.33
45 s for the whole table
```

**File 5 — `heads.py`** (train the copy model; print where each head looks; save the picture `copy_heads.png`; 4 s)

```python
# heads.py - Week 19: train the copy model, then look at what each head looks at.
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tasks import N, copy_batch, train_task, accuracy

model, loss = train_task("copy", L=2, H=2, steps=600)
print(f"copy model: final loss {loss:.4f}   accuracy {accuracy(model, 'copy'):.2f}")

seq = copy_batch(500)
x = seq[:, :-1]                                           # 12 tokens: 6 symbols, SEP, 5 answers
with torch.no_grad():
    model(x)

print("\nwhere does each head look? (average over 500 sequences; rows are the positions that must produce an answer)")
for layer in range(2):
    for head in range(2):
        w = model.blocks[layer].last_weights[:, head].mean(dim=0)      # (12, 12), averaged over the 500 sequences
        print(f"layer {layer} head {head}")
        for q in range(N, 2 * N):                                      # positions 6..11 each produce one answer
            src = int(w[q].argmax())
            print(f"   position {q:2d} looks mostly at position {src:2d}  (weight {w[q, src]:.2f}, that is {q - src} back)")

one = model.blocks[0].last_weights[0]                                   # (heads, 12, 12) for the first sequence
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, (layer, head) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
    w = model.blocks[layer].last_weights[0, head]
    axes[i].imshow(w, cmap="viridis")
    axes[i].set_title(f"layer {layer} head {head}")
    axes[i].set_xlabel("looked at")
    axes[i].set_ylabel("looking")
plt.tight_layout()
plt.savefig("copy_heads.png", dpi=100)
print("\nsaved copy_heads.png")
```

```text
copy model: final loss 0.0016   accuracy 1.00

where does each head look? (average over 500 sequences; rows are the positions that must produce an answer)
layer 0 head 0
   position  6 looks mostly at position  0  (weight 0.99, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.96, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.95, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.96, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.99, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.98, that is 6 back)
layer 0 head 1
   position  6 looks mostly at position  0  (weight 0.97, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.96, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.97, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.98, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.96, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.99, that is 6 back)
layer 1 head 0
   position  6 looks mostly at position  0  (weight 0.88, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.76, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.82, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.86, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.90, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.71, that is 6 back)
layer 1 head 1
   position  6 looks mostly at position  0  (weight 0.86, that is 6 back)
   position  7 looks mostly at position  1  (weight 0.78, that is 6 back)
   position  8 looks mostly at position  2  (weight 0.72, that is 6 back)
   position  9 looks mostly at position  3  (weight 0.92, that is 6 back)
   position 10 looks mostly at position  4  (weight 0.90, that is 6 back)
   position 11 looks mostly at position  5  (weight 0.68, that is 6 back)

saved copy_heads.png
```

Open `copy_heads.png`: four small grids, each row one "looking" place, each column one "looked at" place. Three things to see. **Rows 6-11 (the answer places)** have one bright square each, in columns 0-5: a stripe running parallel to the main diagonal, six columns to its left. That is the "6 back" of the printout, and it is in all four panels. **Rows 0-5 (the six symbols)** show a fainter pattern, mostly each place looking at itself and a few near it (one example sequence; we did not investigate what the symbol places are doing). **Nothing is lit above the main diagonal** (the mask). (We produced the file and looked at it; it is not shipped in the course.)

**File 6 — `heads_more.py`** (reverse and lookup heads, the switch-off test, 7 s)

```python
# heads_more.py - Week 19: two more models, two more head cards, and the test that can prove a name wrong.
import torch
from tasks import copy_batch, lookup_batch, train_task, accuracy


def table(model, seq, queries):
    with torch.no_grad():
        model(seq[:, :-1])
    for layer in range(2):
        for head in range(2):
            w = model.blocks[layer].last_weights[:, head].mean(dim=0)
            cells = [f"{q}->{int(w[q].argmax())} ({w[q].max():.2f})" for q in queries]
            print(f"  layer {layer} head {head}:  " + "   ".join(cells))


def silence_test(model, task):
    print(f"  nothing switched off: {accuracy(model, task):.2f}")
    for layer in range(2):
        for head in range(2):
            model.blocks[layer].silence = [head]
            print(f"  only layer {layer} head {head} off: {accuracy(model, task):.2f}")
            model.blocks[layer].silence = []
        model.blocks[layer].silence = [0, 1]
        print(f"  both heads of layer {layer} off: {accuracy(model, task):.2f}")
        model.blocks[layer].silence = []


print("REVERSE  (query position -> the position it looks at most, and its weight)")
rev, _ = train_task("reverse")
table(rev, copy_batch(500, reverse=True), range(6, 12))
silence_test(rev, "reverse")

print("\nLOOKUP   (odd positions hold a value; position 9 holds the asked-for key)")
lk, _ = train_task("lookup")
seq = lookup_batch(500)
table(lk, seq, [1, 3, 5, 7, 9])
silence_test(lk, "lookup")

with torch.no_grad():
    lk(seq[:, :-1])
w = lk.blocks[1].last_weights                                     # (500, 2, 10, 10)
pick_pos = (seq[:, 0:8:2] == seq[:, 9:10]).float().argmax(dim=1)   # which pair held the asked-for key: 0..3
answer_pos = 2 * pick_pos + 1                                       # where that pair's value sits
for head in range(2):
    hit = (w[:, head, 9, :].argmax(dim=-1) == answer_pos).float().mean().item()
    print(f"\n  layer 1 head {head}: at position 9 it looks at the right value in {100 * hit:.0f}% of sequences")
```

```text
REVERSE  (query position -> the position it looks at most, and its weight)
  layer 0 head 0:  6->5 (0.99)   7->4 (0.96)   8->3 (0.97)   9->2 (0.97)   10->1 (0.98)   11->0 (0.96)
  layer 0 head 1:  6->5 (1.00)   7->4 (0.95)   8->3 (0.98)   9->2 (0.98)   10->1 (1.00)   11->0 (0.96)
  layer 1 head 0:  6->5 (0.74)   7->4 (0.78)   8->3 (0.46)   9->2 (0.73)   10->1 (0.53)   11->0 (0.73)
  layer 1 head 1:  6->5 (0.76)   7->4 (0.83)   8->3 (0.65)   9->2 (0.74)   10->1 (0.61)   11->0 (0.81)
  nothing switched off: 1.00
  only layer 0 head 0 off: 1.00
  only layer 0 head 1 off: 1.00
  both heads of layer 0 off: 0.57
  only layer 1 head 0 off: 1.00
  only layer 1 head 1 off: 1.00
  both heads of layer 1 off: 1.00

LOOKUP   (odd positions hold a value; position 9 holds the asked-for key)
  layer 0 head 0:  1->0 (0.97)   3->2 (0.98)   5->4 (0.98)   7->6 (0.98)   9->7 (0.18)
  layer 0 head 1:  1->0 (0.60)   3->3 (0.32)   5->4 (0.44)   7->6 (0.56)   9->6 (0.15)
  layer 1 head 0:  1->0 (0.60)   3->0 (0.29)   5->0 (0.25)   7->3 (0.18)   9->5 (0.27)
  layer 1 head 1:  1->0 (0.64)   3->2 (0.32)   5->0 (0.23)   7->3 (0.17)   9->5 (0.26)
  nothing switched off: 1.00
  only layer 0 head 0 off: 0.48
  only layer 0 head 1 off: 1.00
  both heads of layer 0 off: 0.35
  only layer 1 head 0 off: 0.80
  only layer 1 head 1 off: 1.00
  both heads of layer 1 off: 0.19

  layer 1 head 0: at position 9 it looks at the right value in 100% of sequences

  layer 1 head 1: at position 9 it looks at the right value in 100% of sequences
```

The last two lines are a check over 500 sequences: at the place that holds the asked-for key, does the head look at the value that belongs to that key? For both layer-1 heads, 100%. Its line is a measurement; the names in the Answer Key are built on it.

**File 7 — `key.py`** (**TEACHER ONLY.** The leak test, deleting the mask from a trained model, the hand numbers, the lookup cards.) **Never show this to the student.**

```python
# key.py - Week 19 (TEACHER ONLY): the leak test, deletion from a trained model, the hand numbers, and the lookup cards for the activity.
import math
import torch
from ablate_model import TinyGPT
from tasks import copy_batch, lookup_batch, train_task, accuracy

# ---- The leak test: change ONE later token; do the logits at EARLIER places move?
torch.manual_seed(0)
x = torch.randint(0, 28, (4, 64))
x2 = x.clone()
x2[:, 40] = (x2[:, 40] + 1) % 28                                   # change the token at place 40
for mask_on in (True, False):
    torch.manual_seed(0)
    model = TinyGPT(28, 128, 4, 4, 64, mask_on=mask_on)
    with torch.no_grad():
        a, _ = model(x)
        b, _ = model(x2)
    moved = (a[:, :40] - b[:, :40]).abs().max().item()
    print(f"mask_on={mask_on}: largest change in the scores at places 0-39 when place 40 changes = {moved:.6f}")

# ---- Deleting the mask from a model that was TRAINED with it (test-time, no retraining)
m, _ = train_task("copy")
print("\ncopy model, trained with the mask:")
print("  tested with the mask    :", round(accuracy(m, "copy"), 2))
for blk in m.blocks:
    blk.mask_on = False
print("  tested without the mask :", round(accuracy(m, "copy"), 2))

# ---- Hand numbers
print(f"\nln(8) = {math.log(8):.3f}   5*ln(8)/12 = {5 * math.log(8) / 12:.3f}   chance on a copy answer = {1 / 8:.3f}")
print("chance on a lookup answer: 1/10 =", 1 / 10, " (picking one of the four values on the page at random: 1/4 + 3/4 x 1/10 =", 1 / 4 + 3 / 4 * 1 / 10, ")")
for name, args in (("copy/reverse", (9, 64, 2, 2, 12)), ("lookup", (17, 64, 2, 2, 10))):
    print(f"knobs, {name}:", sum(p.numel() for p in TinyGPT(*args).parameters()))

# ---- The lookup cards: which value does layer 1 head 0 look at, position 9, for five different sequences?
lk, _ = train_task("lookup")
torch.manual_seed(3)
seq = lookup_batch(5)
with torch.no_grad():
    lk(seq[:, :-1])
w = lk.blocks[1].last_weights[:, 0, 9, :]
names = {10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f", 16: "|"}
print("\nlookup cards (layer 1 head 0, looking from position 9):")
for i in range(5):
    text = " ".join(names.get(int(t), str(int(t))) for t in seq[i, :10])
    best = int(w[i].argmax())
    print(f"  {text}   -> looks at position {best} (weight {w[i, best]:.2f}),  true answer {int(seq[i, 10])}")
```

```text
mask_on=True: largest change in the scores at places 0-39 when place 40 changes = 0.000000
mask_on=False: largest change in the scores at places 0-39 when place 40 changes = 0.001437

copy model, trained with the mask:
  tested with the mask    : 1.0
  tested without the mask : 1.0

ln(8) = 2.079   5*ln(8)/12 = 0.866   chance on a copy answer = 0.125
chance on a lookup answer: 1/10 = 0.1  (picking one of the four values on the page at random: 1/4 + 3/4 x 1/10 = 0.325 )
knobs, copy/reverse: 101641
knobs, lookup: 102545

lookup cards (layer 1 head 0, looking from position 9):
  e 8 a 7 d 4 c 4 | c   -> looks at position 7 (weight 0.97),  true answer 4
  a 0 b 0 d 1 e 4 | a   -> looks at position 1 (weight 1.00),  true answer 0
  e 3 c 9 d 2 f 3 | f   -> looks at position 7 (weight 0.99),  true answer 3
  b 0 a 2 e 1 f 3 | a   -> looks at position 3 (weight 1.00),  true answer 2
  a 4 f 6 b 5 e 4 | e   -> looks at position 7 (weight 0.97),  true answer 4
```

Read the first two lines: **with the mask, changing the token at place 40 moves the scores at places 0-39 by exactly 0.000000; without it, by 0.001437.** The second number is small because the model is untrained; the test is *zero against not zero*. Also: deleting the mask from a copy model **trained with** it changed nothing (1.0 and 1.0): that model's answers come from earlier places, so letting it look ahead costs it nothing. Deleting the mask **and retraining** is what produces the leak.

**File 8 — `key_seed.py`** (**TEACHER ONLY.** The text table again with seed 1; **about 3.7 minutes**; it uses `exec`, which is not in any student file.)

```python
# key_seed.py - Week 19 (TEACHER ONLY): the same five text runs, with seed 1 instead of 0. How much of the table is luck?
source = open("text_ablate.py").read().replace("SEED = 0", "SEED = 1")
exec(source)
```

```text
full      train 1.576  val 1.643  gap 0.067  (43 s)
          the cat chrid ot the boung as. / the are andot the doun the car the ro
no mask   train 0.073  val 0.085  gap 0.012  (42 s)
          ttttttttttttttttttttttttttttttttttttttttttottttttttttttttttttttttttttt
no pos    train 1.424  val 1.717  gap 0.293  (45 s)
          the cat chrid oun tho the riy unte the werot the wrou the chiver trs w
no res    train 2.709  val 2.711  gap 0.001  (47 s)
          t te te chr urot thdod waordo t g kah leeeot as td ae t meeir t t rs w
no norm   train 1.106  val 1.453  gap 0.347  (45 s)
          t ank town is man the river. / the old man wotch at fle the birdge the
```

**File 9 — `key_lookup.py`** (**TEACHER ONLY.** Is the lookup column luck? Three seeds, two lengths; **about 2.6 minutes**; it uses `**sw`, not in any student file.)

```python
# key_lookup.py - Week 19 (TEACHER ONLY): is the lookup column of the task table luck? Three seeds, two lengths of training; and one layer instead of two.
from tasks import train_task, accuracy

switches = {"full": {}, "no mask": {"mask_on": False}, "no pos": {"pos_on": False}, "no res": {"res_on": False}, "no norm": {"ln_on": False}}
print(f"{'lookup':<9}{'seed 0':>14}{'seed 1':>14}{'seed 2':>14}      (600 steps / 1,500 steps)")
for name, sw in switches.items():
    cells = []
    for seed in (0, 1, 2):
        a600 = accuracy(train_task("lookup", steps=600, seed=seed, **sw)[0], "lookup")
        a1500 = accuracy(train_task("lookup", steps=1500, seed=seed, **sw)[0], "lookup")
        cells.append(f"{a600:.2f} / {a1500:.2f}")
    print(f"{name:<9}" + "".join(f"{c:>14}" for c in cells))
print("one layer, two heads:", f"{accuracy(train_task('lookup', steps=1500, L=1)[0], 'lookup'):.2f}")
```

```text
lookup           seed 0        seed 1        seed 2      (600 steps / 1,500 steps)
full        1.00 / 1.00   1.00 / 1.00   1.00 / 1.00
no mask     0.37 / 0.36   0.35 / 0.36   0.36 / 0.36
no pos      1.00 / 1.00   1.00 / 1.00   1.00 / 1.00
no res      1.00 / 1.00   1.00 / 1.00   1.00 / 1.00
no norm     0.33 / 1.00   1.00 / 1.00   1.00 / 1.00
one layer, two heads: 0.40
```

- [ ] **Run the files as a set** and check nothing fails: `for f in text_ablate task_table heads heads_more key; do python3 $f.py > /dev/null || echo FAIL $f; done`. It prints nothing and takes about 4.5 minutes.
- [ ] **Print** workbook pages 19.1-19.6, the four **Head Detective** cards (Activity) and the five sample cards. The five samples are the `text_ablate.py` lines, cut at 70 characters, **shuffled**, labelled A-E; your sheet says which is which. Card contents are in *The Activity, In Full*.
- [ ] **Have the student's own `tinygpt.py` from Week 17 open**, so the four switches are added to their file.
- [ ] **Read the Debugging Clinic** and copy the seven `bad*.py` files to a scratch folder so they are ready to plant. (`bad1` to `bad3` take 4-8 seconds each because they train.)
- [ ] **Decide where the five-model run goes.** The plan below starts it at about minute 29 and plays the second half of live-code while it runs.

### 3 minutes on the day

- [ ] Open `ablate_model.py` as a copy of the student's `tinygpt.py` ready to edit. Open `text_ablate.py` with `run(...)` **typed in advance** (the body is the Week 17 loop; see Live-Code). Laptop **plugged in** (on battery the times can double).
- [ ] Put the prediction cards, the sample cards and the timer on the desk.

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: l4lib` | You are in the wrong folder. Only `from l4lib.corpus import TEXT` needs it. |
| `ModuleNotFoundError: torch` / `matplotlib` | `pip` is blocked; use a machine that already has them. Without a laptop, run the lesson from this guide's printed tables and do the Head Detective cards on paper. |
| `text_ablate.py` takes over 8 minutes | Battery or a busy laptop. **Set `STEPS, WARMUP = 400, 50`**: about 22 s per model (110 s in all). With `sed 's/STEPS, WARMUP = 800, 50/STEPS, WARMUP = 400, 50/' text_ablate.py > text_ablate400.py` we measured the table below. **The order changes**: at 400 steps the no-positions model (1.876) and the no-norm model (1.818) are both *ahead* of the full one (1.950), the no-mask model is 1.619 and not yet 0.077 (the leak takes longer to learn), and only the residual is still clearly worst (2.852). Do not quote the 800-step reading on this table; the lesson about rules (same steps, validation, check for a leak) is unchanged. |
| `RuntimeError` naming an in-place operation | A `silence` list is not empty before training (Clinic 5). Reset `silence = []`. |
| Different random numbers on another machine | Expected (other PyTorch builds). The structure holds: the residual is the worst, the mask is a leak, every head on copy looks six back. Nothing depends on a digit. |

The 400-step table (measured; same script, `STEPS = 400`):

```text
full      train 1.942  val 1.950  gap 0.008  (23 s)
          the can chris ot thdo indord be g ola anewot as t fie the carot thrs w
no mask   train 1.607  val 1.619  gap 0.012  (22 s)
          tatatattatratatattadotatatrat tot tat atewottas tatat tateawatatttasat
no pos    train 1.819  val 1.876  gap 0.056  (23 s)
          the cat chras ot the bowat as the oll andeot as the che me wandrdirs w
no res    train 2.841  val 2.852  gap 0.011  (23 s)
          t ewe e shr eeotn hdo  waordo t g  ah  eewot  s  dn e ta eewr trttrs w
no norm   train 1.752  val 1.818  gap 0.066  (22 s)
          the cat chris oth ado indor ien t the anerot as id te the cacot thrs w
```

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 8 | "Which part would you delete to break it the most?" Each writes a ranking on a card. |
| 🧠 Concept | 12 | What an ablation is and what makes it fair; what a synthetic task buys; what one row of a heatmap is |
| 💻 Live-code | 25 | Add four switches; start the five-model run; type `tasks.py`; run `task_table.py` and `heads.py` |
| 🎲 Their turn | 20 | Read the table against the ranking; match the five samples; Head Detective; switch-off test |
| 🔑 Wrap & assign | 5 | What was shown, what was not; the leak; the name needs a test; homework |

### 🪝 Hook — Which Part Would You Delete? (8 minutes)

**Do not open the laptop yet.**

1. **(2 min) The frame.** *"A GPT has a lot of parts. Last week we built it and trusted every one. Today we test the trust. You get a card with four parts: the mask, the place table, the residual road, the layer norms. Rank them from 'deleting it hurts most' to 'hurts least'. Underneath, write one part you think will *not* matter."*
2. **(3 min) Why not just believe it?** *"Which of these four did we add because somebody proved it was needed? Which because it worked?"* (Let them argue; we did not test any of them in Weeks 15-17.) *"What would a test look like?"*
3. **(3 min) Hold up the cards, do not reveal.** *"We will fill the table in about half an hour. Keep the cards."* Write on the board: **"delete one thing, change nothing else, compare on text it has not seen."** This is the definition of **ablation**; say the word once and write it under the sentence.

### 🧠 Concept — Fair Deletions, Made-Up Tasks, One Row of a Picture (12 minutes)

**(4 min) Three rules of a fair ablation.** On the board:

```text
1. Same seed, same steps, same data, same scoring batches.   (Only the deleted part changes.)
2. Compare on text the model was NOT trained on.             (Validation, not training.)
3. If a result is too good, check for a leak before you cheer.
```

Ask about rule 3 with a question, do not lecture: *"Suppose a model had somehow been allowed to peek at the answer. What would its loss look like?"* (Very low.) *"Then how would we tell a model that is good from a model that peeks?"* Collect ideas; the test (change a later token and see whether earlier scores move) comes out of the room, or you give it.

**(3 min) Why made-up tasks?** *"On English text, we cannot say what a head is supposed to do. So we make a task where we know. Copy: six symbols, a separator, then the same six. If a model gets it right, something must carry each symbol across the gap. Reverse: the same, backwards. Lookup: four key-and-value pairs and then one key; say its value."* Draw one of each on the board, with numbers:

```text
copy     3 1 7 7 0 5 | 3 1 7 7 0 5
reverse  3 1 7 7 0 5 | 5 0 7 7 1 3
lookup   a 4 c 9 e 1 b 6 | c  ->  9
```

Ask: *"How often would a model that guesses the answer be right? Copy: one symbol out of eight. Lookup: a digit out of ten."* (0.125 and 0.1; the `ln(8)` version is section 2(a).)

**(3 min) One row of a heatmap.** Draw a 12 x 12 grid. *"Every place in the window, as it works out its answer, spreads 1.0 of attention over the places before it (the mask forbids the rest). One row is one place's answer to 'where did I look?'. If the copy model is working, which column do you expect the answer-place to light up?"* (The place where its symbol sits: 6 back. Let them predict; it is right for every head.)

**(2 min) The warning, in one sentence.** *"A picture shows where it looked. It does not show whether the model needed it. That is a second test, and we will do it."*

### 💻 Live-Code Together — Four Switches, Five Models, Three Tasks (25 minutes)

The student types. You narrate. **Nobody pastes, except `last_weights` and `silence` and the student's own `Block` and `TinyGPT` from `tinygpt.py`.**

**Step 1 (7 min) — `ablate_model.py`: four `if`s.** Start from the student's `tinygpt.py`. Add the four switches one at a time and **say, before each, what the model will do without it**:

- `if self.mask_on:` around `masked_fill`: *"every place can see every other place."*
- `pos_on` in `forward`: *"the model only knows which character, not where."*
- `res_on`: *"each sub-layer's output replaces the road instead of adding to it."* (Week 6: the gradient road.)
- `ln_on`: the Identity replacement for the three kinds of norm (`ln1`, `ln2`, `ln_f`).

Give the student the two looking-lines (`last_weights`, `silence`) and say: *"these are for looking and testing; they do nothing when training."* **Do not run anything yet.**

**Step 2 (6 min) — `text_ablate.py`, then press Enter.** The student copies their Week 17 `train.py` into a function `run(name, mask_on=True, ...)` (the body is the same loop, no checkpoints) and adds the five calls at the bottom. Two things to point at: `SEED = 0` (rule 1: same seed) and `estimate` resetting the dice (rule 1: same scoring batches). **Before pressing Enter:** *"Predict which of the five will have the lowest validation loss."* Collect. Press Enter. **It takes 3.6 minutes**; keep the step time in your head (about 53 ms per step).

**Step 3 (12 min) — `tasks.py` while it runs.** The student types `copy_batch` and `lookup_batch` and **prints one batch** of each, reading the first row aloud (*"that is six symbols, the separator 8, and six answers"*). Then `accuracy` and `train_task` (the loop is theirs: AdamW, no warm-up here; `logits[:, -k:, :]` picks the answer places only, say why). Run `task_table.py` (**46 s on an idle machine; a bit longer while the other run is going**). Read the grid together; ask only *"what is suspicious?"* (No mask on copy and reverse: 1.00 for the wrong reason, saved for the table discussion.) Then `heads.py` (4 s): open `copy_heads.png`.

**Timing note.** The five-model run should end at about minute 33 of the lesson. If it ends while they are typing `tasks.py`, leave the output on screen and go on.

### 🎲 Their Turn — Read the Table, Match the Samples, Detect the Heads (20 minutes)

Full rules in *The Activity, In Full*. The shape:

1. **(5 min) Read the ablation table.** Students compare it with their ranking card. Ask, one at a time: *"Which row is the best?"* (no mask, 0.077) *"Do you believe it?"* Read the sample. Run the **future-change test** from `key.py` **on the board** (not the code; the idea): change one later token, do earlier scores move? Then the sentence: **a loss is not a score if the model can see the answer.** Then the real ranking: residual (+1.006) ≫ positions (+0.066), and no norm *better* (-0.195). Ask: *"Does that mean norms are useless?"* (We do not know; limit 6.)
2. **(3 min) Match the samples.** Five cards A-E, five models. Students match and write one piece of evidence each (Activity, Part 1).
3. **(10 min) Head Detective.** Four cards; name each; write a kill-test (Activity, Part 2).
4. **(2 min) The switch-off results** from `heads_more.py`. Read the copy column: *"four heads look six back; switch off one: nothing. So what does the stripe prove?"*

**Stop at 20 minutes.** If Head Detective runs long, do cards A and C and leave B and D for the workbook.

### 🔑 Wrap & Assign (5 minutes)

1. **(2 min)** *"Three things we did. One: we deleted four parts and found one that wrecks the model, one that costs a little, one that helped, and one that lets the model cheat. Two: we made three tasks whose answers we know and read the pictures of the heads. Three: we found that a head's name is a claim and needs a test. What did we **not** do?"* (Find out why no-norm helped; run more seeds; try other sizes or other tasks; look inside any real large model.)
2. **(1 min)** *"What is a leak?"* (The model can see the answer. The loss is low and means nothing.)
3. **(1 min)** Hand out the workbook.
4. **(1 min)** One sentence ahead: *"Next week the characters go away. The model will see pieces of words; we build the piece-maker ourselves, by counting the most common pair."*

---

## 🐞 The Debugging Clinic

Every error below was produced by running the code. **Paths will differ on your machine**; here they appear as `/home/you/l4/`. Tracebacks from PyTorch and matplotlib run through several of their own files; the long middle is replaced by a line reading `... frames inside torch (elided) ...` (or `matplotlib`), and **the last line is the real, complete last line**. Each mistake is deliberate: you plant it, the student reads the traceback (or the odd number) aloud, and you refuse to fix it until they have said what it means. Each block imports the finished `ablate_model.py` or `tasks.py`. **Three of the seven are silent**, and the silent ones are the point.

### How to teach debugging without giving the answer

1. *"Read me the last line."* For a silent mistake: *"What did you expect this to print?"*
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

### Mistake 1 — the switch set on the wrong object (SILENT: nothing is deleted)

```python
# DELIBERATE MISTAKE 1 (SILENT): the "no mask" switch set on the GPT, not on its blocks. Nothing is deleted. Compare the two numbers.
import torch
from tasks import train_task, accuracy

full, _ = train_task("lookup", steps=300)
model, _ = train_task("lookup", steps=300)
model.mask_on = False                                      # <- sets a new attribute on the GPT; the Blocks never look at it
torch.manual_seed(5)
print("full model              :", round(accuracy(full, "lookup"), 3))
torch.manual_seed(5)                                       # the same 1,000 test sequences for both
print("'no mask' model, claimed:", round(accuracy(model, "lookup"), 3))
print("same answers everywhere? ", bool((full(torch.tensor([[11, 3, 12, 5, 13, 1, 14, 7, 16, 12]]))[0] ==
                                         model(torch.tensor([[11, 3, 12, 5, 13, 1, 14, 7, 16, 12]]))[0]).all()))
print("what the Blocks say     :", [b.mask_on for b in model.blocks])
```

```text
full model              : 0.907
'no mask' model, claimed: 0.907
same answers everywhere?  True
what the Blocks say     : [True, True]
```

**Read it:** the two accuracies are **identical to three decimals** and the scores from the two models are identical for a test input, because the "no mask" model still has the mask. `model.mask_on = False` created a new attribute on the *GPT*; each `Block` reads its *own* `mask_on` (the last line says `True`, `True`). **The lesson:** identical to the last digit is not a sign of robustness, it is a sign that nothing changed. Ask: *"the task table said no mask gave 0.37 on lookup. What does this file say? Which one did the deleting?"*

### Mistake 2 — the loss taken over every place (SILENT, and the number is right)

```python
# DELIBERATE MISTAKE 2 (SILENT): the loss is taken over EVERY position of the copy task, including the six random symbols nobody can predict.
import math
import torch
import torch.nn.functional as F
from ablate_model import TinyGPT
from tasks import copy_batch, accuracy

torch.manual_seed(0)
model = TinyGPT(9, 64, 2, 2, 12)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.0)
for step in range(600):
    seq = copy_batch(64)
    _, loss = model(seq[:, :-1], seq[:, 1:])               # <- targets for all 12 positions, not just the 6 answers
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
print(f"final loss {loss.item():.3f}   accuracy on the answers {accuracy(model, 'copy'):.2f}")
print(f"5 unpredictable symbols out of 12 places, each worth ln(8): 5 * ln(8) / 12 = {5 * math.log(8) / 12:.3f}")
```

```text
final loss 0.872   accuracy on the answers 1.00
5 unpredictable symbols out of 12 places, each worth ln(8): 5 * ln(8) / 12 = 0.866
```

**Read it:** accuracy on the answers is **1.00**, but the loss stays at **0.872**. It is not stuck: the loss includes five places that are random symbols nobody can predict, worth `ln(8)` each; the best possible average is `5 x ln(8) / 12 = 0.866`. **The lesson:** a loss that will not go to zero can be a correct result if part of the thing being scored is noise. The fix is to score only the answer places (`logits[:, -k:, :]` in `train_task`). Ask: *"where does 0.866 come from?"*

### Mistake 3 — the lookup keys with repeats (SILENT, and more training does not help)

```python
# DELIBERATE MISTAKE 3 (SILENT): the lookup keys drawn with torch.randint, so the same key can appear twice with two different values.
import torch
import torch.nn.functional as F
from ablate_model import TinyGPT


def bad_lookup_batch(B, P=4):
    keys = torch.randint(10, 16, (B, P))                   # <- repeats allowed
    vals = torch.randint(0, 10, (B, P))
    pairs = torch.stack([keys, vals], dim=2).reshape(B, 2 * P)
    pick = torch.randint(0, P, (B,))
    rows = torch.arange(B)
    return torch.cat([pairs, torch.full((B, 1), 16), keys[rows, pick][:, None], vals[rows, pick][:, None]], dim=1)


torch.manual_seed(0)
model = TinyGPT(17, 64, 2, 2, 10)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.0)
for step in range(1501):
    seq = bad_lookup_batch(64)
    logits, _ = model(seq[:, :-1])
    loss = F.cross_entropy(logits[:, -1, :], seq[:, -1])
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    if step % 500 == 0:
        with torch.no_grad():
            seq = bad_lookup_batch(2000)
            right = (model(seq[:, :-1])[0][:, -1].argmax(dim=-1) == seq[:, -1]).float().mean().item()
        print(f"step {step:4d}  loss {loss.item():.3f}  accuracy {right:.2f}")
seq = bad_lookup_batch(2000)
dup = torch.tensor([len(set(row[0:8:2].tolist())) < 4 for row in seq])
print(f"sequences with a repeated key: {100 * dup.float().mean().item():.0f}%")
```

```text
step    0  loss 2.826  accuracy 0.09
step  500  loss 0.515  accuracy 0.80
step 1000  loss 0.435  accuracy 0.80
step 1500  loss 0.514  accuracy 0.81
sequences with a repeated key: 70%
```

**Read it:** the accuracy sits at **0.80-0.81** from step 500 to 1,500 and the loss stops falling at about 0.4-0.5. **70% of the sequences have a repeated key**, so for those the question "what is this key's value?" has two right answers (the task as built picks one pair at random to ask about). The model cannot know which. `torch.randperm(6)[:4]` in `tasks.py` gives four different keys. **The lesson:** when accuracy will not pass a ceiling and more training does not move it, the task may have no single right answer. Count the repeats. (We did not work out the exact ceiling from the repeats; the measured 0.80-0.81 is what it did.)

### Mistake 4 — a typo in a switch name (loud)

```python
# DELIBERATE MISTAKE 4: a typo in a switch name.
from tasks import train_task

model, loss = train_task("copy", steps=10, pos_off=True)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad4.py", line 4, in <module>
    model, loss = train_task("copy", steps=10, pos_off=True)
TypeError: train_task() got an unexpected keyword argument 'pos_off'
```

**Read it:** last line names the exact word that is wrong: `pos_off` is not `pos_on`. Keyword arguments with defaults turn a typo into an error instead of a silent default. (Compare Mistake 1, where the typo was an *attribute*, which Python accepts.) Ask: *"why is this one loud and Mistake 1 silent?"*

### Mistake 5 — a head switched off before training (loud)

```python
# DELIBERATE MISTAKE 5: a head switched off BEFORE training. The switch is for testing a trained model.
import torch
import torch.nn.functional as F
from ablate_model import TinyGPT
from tasks import copy_batch

torch.manual_seed(0)
model = TinyGPT(9, 64, 2, 2, 12)
model.blocks[0].silence = [0]                              # <- head 0 of layer 0 off, then we train
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
seq = copy_batch(64)
_, loss = model(seq[:, :-1], seq[:, 1:])
opt.zero_grad(set_to_none=True)
loss.backward()
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad5.py", line 14, in <module>
    loss.backward()
    ... frames inside torch (elided) ...
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation: [torch.FloatTensor [64, 2, 12, 12]], which is output 0 of SoftmaxBackward0, is at version 1; expected version 0 instead. Hint: enable anomaly detection to find the operation that failed to compute its gradient, with torch.autograd.set_detect_anomaly(True).
```

**Read it:** "modified by an inplace operation" and the shape `[64, 2, 12, 12]`: that is the attention weights (batch 64, 2 heads, 12 x 12). `weights[:, h] = 0.0` writes into a tensor the backward pass still needs. **The lesson:** the `silence` switch is for testing a trained model under no gradient. Ask: *"where in the lesson did we train a model with `silence` set? Where did we use it?"*

### Mistake 6 — `imshow` handed four axes (loud)

```python
# DELIBERATE MISTAKE 6: imshow handed all of last_weights, which has four axes.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tasks import copy_batch, train_task

model, _ = train_task("copy", steps=50)
model(copy_batch(8)[:, :-1])
plt.imshow(model.blocks[0].last_weights)                   # <- shape (8, 2, 12, 12): sequence, head, looking, looked at
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad6.py", line 9, in <module>
    plt.imshow(model.blocks[0].last_weights)                   # <- shape (8, 2, 12, 12): sequence, head, looking, looked at
    ... frames inside matplotlib (elided) ...
TypeError: Invalid shape (8, 2, 12, 12) for image data
```

**Read it:** `(8, 2, 12, 12)` is sequence, head, looking, looked-at. `imshow` draws a grid, which has two axes. The fix is `last_weights[0, 0]` (first sequence, first head). Ask the student to say the four axes **in words** before fixing it.

### Mistake 7 — the model built for fewer places than it is fed (loud)

```python
# DELIBERATE MISTAKE 7: the model built for 10 places, fed 12.
import torch
from ablate_model import TinyGPT
from tasks import copy_batch

model = TinyGPT(9, 64, 2, 2, 10)                           # <- T = 10
model(copy_batch(4)[:, :-1])                               # 12 tokens
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad7.py", line 7, in <module>
    model(copy_batch(4)[:, :-1])                               # 12 tokens
    ... frames inside torch (elided) ...
  File "/home/you/l4/ablate_model.py", line 72, in forward
    x = x + self.pos(torch.arange(T))
    ... frames inside torch (elided) ...
IndexError: index out of range in self
```

**Read it:** `index out of range in self` on the line `self.pos(torch.arange(T))`: the window has 12 places, the place table has 10 rows. (Week 16's `IndexError` again.) The fix: `TinyGPT(..., T=12)`; in `tasks.py` that is `length - 1`.

---

## 🎲 The Activity, In Full

### Match the Samples, then Head Detective

**What it is:** two short games. The first makes the student connect a line of numbers to a line of text. The second makes them name a head and say what would prove the name wrong.

### Setup (2 minutes, during the live-code segment)

- **Part 1 cards.** Five samples, cut at 70 characters, shuffled, labelled A-E. On your sheet: 

| Model | Sample (first 70 characters, from `text_ablate.py`) |
|---|---|
| full | `the caros river the oxxunted bean the feewon as tolle the cacherd rsth` |
| no mask | `tatattttttttttattttaatttattattttttttatatttottatttaatattatataattattasat` |
| no pos | `t the wther saken thod wat do the wak feeron t did thery beacot thes w` |
| no res | `t te te cbr urot thdo iwaardobt gt ah leeeot as td ae tamteir t t rs w` |
| no norm | `the cast brout. / the old marked on the lepeor and dre thad cared did` |

- **Part 2 cards.** Four Head Detective cards (below). Give **only** the table and the task description. The names and the switch-off results are on your sheet.

### Part 1 — Match the Samples (3 minutes)

Students have the numbers table (train, validation, gap) and the five samples, and match them. The intended evidence: *no mask: only `t` and `a`, the train loss is 0.07 (the model found a shortcut); no residual: not a word in it and the loss is 2.7 (hardly learned); no norm and full: the only two with whole words (`the cast`, `the old marked`; `the river`); no pos: words run together, but a mix of `the`, `wat`, `did`.* **Two are hard to tell apart (full and no norm, or full and no pos).** Say so: *samples cannot rank close models; the loss can.* (A sample is one draw; limit 1.)

### Part 2 — Head Detective (the 10-minute core)

Each card has the task, a table of "query place -> place it looks at most (weight)", and three questions: **(1) In one sentence, what is this head doing? (2) Give it a name of three words or fewer. (3) Write one test that would show your name wrong.**

| Card | Task and head | Table |
|:--:|---|---|
| A | **Copy**, layer 0 head 0 (symbols 6, separator, answers) | `6->0 (0.99)  7->1 (0.96)  8->2 (0.95)  9->3 (0.96)  10->4 (0.99)  11->5 (0.98)` |
| B | **Reverse**, layer 0 head 0 | `6->5 (0.99)  7->4 (0.96)  8->3 (0.97)  9->2 (0.97)  10->1 (0.98)  11->0 (0.96)` |
| C | **Lookup**, layer 0 head 0 (places 0-7 pairs; 8 is `|`; 9 is the asked-for key) | `1->0 (0.97)  3->2 (0.98)  5->4 (0.98)  7->6 (0.98)  9->7 (0.18)` |
| D | **Lookup**, layer 1 head 0, looking from place 9, five sequences | `e 8 a 7 d 4 c 4 | c  -> looks at 7 (0.97)`<br>`a 0 b 0 d 1 e 4 | a  -> looks at 1 (1.00)`<br>`e 3 c 9 d 2 f 3 | f  -> looks at 7 (0.99)`<br>`b 0 a 2 e 1 f 3 | a  -> looks at 3 (1.00)`<br>`a 4 f 6 b 5 e 4 | e  -> looks at 7 (0.97)` |

(Cards A-C come from `heads.py` and `heads_more.py`; card D from `key.py`. Letters `a`-`f` stand for keys 10-15 and `|` for the separator, as in the `key.py` printout.)

**Walk the room with three questions.** *"Is this head's job the same on every input, or does it depend on the input?"* (A, B, C: fixed offsets. D: a different place each time, chosen by the content.) *"If I give you a copy of card A with different symbols, where does it look?"* (The same places: it looks by place, not by symbol.) *"If I take this head out, what do you expect?"* (Let them predict; then read them the result.)

### The switch-off results (read after the cards, not before)

| Card | Head | Switch it off | Both heads of its layer off |
|:--:|---|:--:|:--:|
| A copy | L0 H0 | 1.00 | 0.75 |
| B reverse | L0 H0 | 1.00 | 0.57 |
| C lookup | L0 H0 | **0.48** | 0.35 |
| D lookup | L1 H0 | **0.80** | 0.19 |

The sentence to draw out: **A and B look as important as C and D, and are not: another head does the same job.** *"Which name would you trust more, after seeing this?"*

### What "finished" looks like

The table filled, with the leak row flagged; the five samples matched with evidence; four cards each with a name and a kill-test; and the student saying one sentence like *"the head looks six back, and I know that from the picture, but I only know the model needs it if switching it off breaks something."*

### Variation — easier

Do cards A and D only. Give the names ("looks 6 back", "finds the value for the asked-for key") and ask only question 3.

### Variation — harder

Ask the student to **predict** the switch-off result for L0 H1 on lookup before you read it (it is 1.00: the head looks one back only weakly, 0.32-0.60, and at place 3 it looks at itself), and then to design a second kill-test that does not use `silence`: *"find an input on which it should fail"* (for a fixed-offset head: a copy task with 7 symbols; the model was built for 6, so it will be out of range. We did not run this; have them try it and report).

---

## ❓ Questions Students Ask This Week

**"Why is the no-mask model so good?"** It is not good; it is reading the answer. With no mask, place 5 can attend to place 6, and place 6 of `x` *is* the correct answer for place 5. The future-change test shows it: change one later token, and earlier scores move (0.001437 against exactly 0.000000, untrained; `key.py`).

**"Why did removing the layer norm help?"** We do not know. It is better at 800 steps on both seeds, by about 0.19, and its gap is larger. We did not test longer training, other learning rates or other sizes. (Limit 6.)

**"Why is removing the residual so bad?"** We measured that it is (validation 2.68 against 1.67, and about 2.7 on the second seed). The Week 6 story (the gradient has no straight road back, so the first blocks barely learn) is consistent with it, but **we did not measure gradients in this model**, so say "consistent with".

**"Why do all four heads do the same thing?"** We do not know. They are redundant on this task at this size; the switch-off column shows it. It may be that two heads is more than copying needs. We did not try one head.

**"Can I see a head in the big model?"** Not in this course; there are no large models here. The pictures and names are from a 101,641-knob model on made-up numbers.

**"Is the layer-1 head of lookup an 'induction head'?"** Some write-ups use that name for a two-step find-the-key-then-read-the-next-token pattern. We did not test anything to put that name on it; today's evidence is the hit rate (100%) and the switch-off result. If the student asks, say so.

**"Why does lookup need two layers?"** A one-layer lookup model got 0.40 and the two-layer one got 1.00 (`key_lookup.py`). One reading: the first layer attaches each key to its value; the second uses the asked-for key to find it. The switch-off numbers for L0 H0 are consistent with it. We did not test other sizes.

**"Why do the no-position copy models still work (0.95)?"** The mask gives each place a rough idea of how far along it is (place 1 sees one token, place 6 sees six). Week 16's `masked.py` shows the same. It gets worse, not to chance (0.125).

**"Why 800 steps?"** So five models fit in 3.6 minutes. Week 17 used 1,500. At 400 steps the no-positions model (1.876) is ahead of the full one (1.950), so the table depends on the training length; the lesson's rules (same steps for all) matter.

**"Will my numbers match yours?"** The sizes (101,641 and 102,545), the chance levels, the shapes, the `ln(8)` are exact. Losses, accuracies and samples come from `torch.manual_seed(0)` and matched on repeat on the same machine; another PyTorch build may give different digits. The timings will differ.

---

## ⚠️ Where This Lesson Goes Wrong

1. **The student writes "removing the mask improved it".** Return to the sample, then the future-change test.
2. **Running five models takes the whole segment.** It is 3.6 minutes of waiting. Keep typing `tasks.py` while it runs. If the laptop is slow, use the 400-step fallback.
3. **Two scripts at once on a one-core laptop.** `text_ablate.py` and `task_table.py` together slow each other. Wait for one.
4. **The student compares the 800-step table with Week 17's 1.447.** Different steps (800 against 1,500). Compare rows with rows.
5. **Treating a single row as settled** (no norm). Two seeds, same sign; still one model, one size.
6. **A head "name" offered with no test.** Hold the student to question 3.
7. **Stale `silence`.** If a student silences a head, tests, and does not reset `silence = []`, later numbers are for a model with a head missing (silent). The code in `heads_more.py` resets inside the loop; the student's own code may not.
8. **The heatmap PNG is not opened.** `copy_heads.png` is saved, not shown; the student must open the file.
9. **The lookup "no mask" result (0.37) is read as a leak.** It is not: the window stops before the answer. We do not know what it is.
10. **The task is scored over every place** (Mistake 2): a loss stuck at 0.87 is the floor, not a failure.

---

## 🧭 Differentiation

### If the student is struggling

- Drop to **three** rows: full, no residual, no mask. Keep the leak discussion; it is the lesson.
- Give `ablate_model.py` whole and have the student type only the `run(...)` calls and `copy_batch`. The reading of the table and the two cards is the same.
- For heads, use card A only and the sentence *"it looks six back"*. Skip the naming of layer and head.

### If the student is flying

- Ask them to **predict, then run**: one head instead of two in the copy model (`H=1`); 300 steps instead of 600; a 7-symbol copy with the model built for 6. **We ran none of these; do not quote numbers; let them report.**
- Ask them to find a second seed for one row of the text table (teacher: `key_seed.py` has the answer for all five) and to say whether the no-positions effect survives.
- Ask: *"you found a head that looks six back; make the model fail by changing the input, not by switching anything off"*, then write the result as a kill-test.
- Ask them to explain the **0.37** on lookup with no mask. **We do not know the answer. If they find one with a test, write it down; it is a better answer than ours.**

### If the student won't engage today

Play **Head Detective** with their own cards: run `heads.py`, give them the printout for one head, and ask them to tell you where it looks. Then show them that the copy model works with any one of the four heads removed. The point is the surprise.

---

## ✅ Assessing Understanding

Five questions, orally, during the activity. Not graded; they inform the mastery scale.

1. **"What is an ablation, and what makes it fair?"** *Pass:* delete one thing; same everything else (seed, steps, data, scoring batches); compare on validation.
2. **"The no-mask model's validation loss is 0.077. Is the mask useless?"** *Pass:* no; that is a leak; the model can see the answer; the sample is `tatat...`.
3. **"Which deletion hurt the most, and by how much?"** *Pass:* the residual road, validation 2.68 against 1.67 (+1.01); positions a little (+0.07).
4. **"What is the chance level on copy, and why does the trained model's 1.00 mean something?"** *Pass:* 1 in 8 = 0.125; it is far above guessing.
5. **"All four heads look six back on the copy task. Which one copies?"** *Pass:* we cannot say from the picture; switching one off changes nothing; two heads of a layer together matter; so the heads are redundant, and the name needs a test.

### Mastery scale for this week

| Level | What you see |
|---|---|
| **4 — Fluent** | Builds the switches with little help; spots the leak unprompted from the sample or the too-good loss; names a head *and* writes a test that could falsify it; says what was not tested. |
| **3 — Secure** | Types the switches with prompts; fills the table; explains the leak once prompted; names a head and writes a plausible kill-test. |
| **2 — Developing** | Fills the table; reads lower loss as better in every row; names a head from the picture without a test. |
| **1 — Not yet** | Cannot say what was deleted or what was compared. Repeat Week 17's "train against validation" picture at the start of Week 20. |

---

## 📤 Homework to Assign

The workbook has six pages (19.1-19.6). The student does them in order, and writes **predictions before running anything**.

1. **19.1 Predict before you delete** — rank the four deletions and guess which (if any) makes the model better; compare with the table.
2. **19.2 The ablation table** — `text_ablate.py` with their own seed stated; the table of train, validation and gap, and one sentence per row.
3. **19.3 The leak** — explain the no-mask row in their own words, with the future-change test described, the chance numbers for the tasks and the `5 x ln(8) / 12` floor worked by hand.
4. **19.4 The three tasks** — `task_table.py`; the grid, with the chance level and the leak row marked.
5. **19.5 Name a head** — the lab deliverable: one head of the copy model, its heatmap, its table, its name, and **what evidence would prove the name wrong**.
6. **19.6 Switch it off** — the switch-off test for that head, one head alone and both of its layer, and a sentence on whether the name survived.

**Every number in a write-up must have been printed by the student's own run in the last 24 hours**, with the seed stated. Estimated time: 60-75 minutes, of which about five minutes is the computer working.

---

## 🔑 Answer Key

> **The workbook pages 19.1-19.6 follow this order.** Where an answer is a number it comes from `text_ablate.py`, `task_table.py`, `heads.py`, `heads_more.py` or `key.py`, all run from the Prep Checklist. **A student's own run uses their own seed; only the structure of the answer is fixed.** (If the workbook author has reordered the pages, match by title.)

### Page 19.1 — Predict before you delete

No wrong ranking. Marks for a *reason*. The measured ranking by damage on validation (seed 0): **no residual (+1.006) > no positions (+0.066) > full > no norm (-0.195) > no mask (-1.596, a leak)**. Common predictions: the mask or the positions first. Draw out: *"the one thing we did not predict was that a deletion would help."*

### Page 19.2 — The ablation table

| | Train | Validation | Gap |
|---|:--:|:--:|:--:|
| full | 1.597 | 1.673 | 0.076 |
| no mask | 0.070 | 0.077 | 0.007 |
| no positions | 1.451 | 1.739 | 0.288 |
| no residual | 2.664 | 2.679 | 0.015 |
| no norm | 1.150 | 1.478 | 0.327 |

(Seed 0, 800 steps. Another seed moved each validation number by 0.01-0.03 and left the order (`key_seed.py`).) Model one-sentence answers: *full: "the baseline."* *No mask: "the model can see the answer; the number is a leak."* *No positions: "it fits the training text better and the unseen text worse; the gap is four times bigger."* *No residual: "it hardly learned anything."* *No norm: "better on validation at 800 steps, and we do not know why; the gap is larger."* A student who ranks "no mask" as the best model has missed the lesson.

### Page 19.3 — The leak

Model answer: *"With no mask, place 5 can look at place 6, and the token at place 6 of `x` is the character place 5 is supposed to predict. So the model reads the answer instead of guessing. The sample is `tatattt...`. The test: change one later token and see whether earlier scores move; with the mask they don't (0.000000), without they do (0.001437 in an untrained model)."* Hand numbers: `ln(8) = 2.079`; chance on a copy answer 0.125; floor `5 x ln(8) / 12 = 5 x 2.0794 / 12 = 0.866`.

| Marks | |
|---|:--:|
| Says the model can see the answer | 1 |
| Links it to the sample or the too-low loss | 1 |
| Describes the future-change test (change later, see if earlier moves) | 1 |
| Says it is not a finding about the mask | 1 |

### Page 19.4 — The three tasks

| Task | full | no mask | no positions | no residual | no norm |
|---|:--:|:--:|:--:|:--:|:--:|
| copy | 1.00 | 1.00 | 0.95 | 1.00 | 1.00 |
| reverse | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 |
| lookup | 1.00 | 0.37 | 1.00 | 1.00 | 0.33 |

Chance: copy and reverse **0.125**; lookup **0.1**. Flag the two leaks (copy and reverse no mask). The lookup no-norm 0.33 is not stable: on seed 0 it is 0.33 at 600 steps and 1.00 at 1,500, and 1.00 on seeds 1 and 2. A student's own seed may give 1.00 in that cell; accept it. **The lookup no-mask 0.37 is stable on all three seeds and both lengths.**

### Page 19.5 — Name a head (the lab deliverable)

A **head card** is four things on one page: the name, the claim in a sentence, the table or heatmap it rests on, and the test that could prove it wrong.

What a complete write-up contains, for **their own** run (seed stated):

| Item | Our run (copy model, seed 0, 600 steps) | Acceptable |
|---|---|---|
| Accuracy of the model | 1.00 | above 0.95 |
| The table for one head | layer 0 head 0: `6->0, 7->1, ..., 11->5`, weights 0.95-0.99 | each answer place looks 6 back |
| A heatmap of it, opened and looked at | `copy_heads.png` | in rows 6-11, one bright square per row, six columns left of the place; nothing above the main diagonal |
| A name | "looks 6 back" / "the copy-across head" / "6-back head" | any that says *what it looks at* |
| The kill-test | "switch it off (`blocks[0].silence = [0]`) and see whether accuracy falls" | a test that names what result would mean "wrong" |

**The accepted kill-tests:** (a) switch the head off and see whether accuracy falls; (b) run it on a different input and see whether it still looks six back; (c) look at the other heads for the same stripe. *Not accepted:* "look at the picture again". A test with no result that would count against the name is not a test.

### Page 19.6 — Switch it off

| Switch-off (copy, seed 0) | Accuracy |
|---|:--:|
| nothing | 1.00 |
| L0 H0 only | 1.00 |
| L0 H1 only | 1.00 |
| L1 H0 only | 1.00 |
| L1 H1 only | 1.00 |
| both layer-0 heads | **0.75** |
| both layer-1 heads | 1.00 |

Model answer: *"My name was 'looks 6 back' and that's still true: the picture shows it. But switching the head off changed nothing, because the other three do the same. So the head is not what the model needs; the pair of layer-0 heads is (0.75 with both off). The name survives as a description and fails as a claim about importance."* (Reverse: 1.00 for every single head, 0.57 with both layer-0 heads off. Lookup: L0 H0 off 0.48; L1 H0 off 0.80; L0 H1 and L1 H1 off 1.00.)

| Criterion | Marks |
|---|:--:|
| Reports the single-head result as a number | 1 |
| Reports a both-heads result | 1 |
| Says what the result does to the name (survives as description, not as "needed") | 1 |
| Says what was not tested (other seeds, other sizes) | 1 |

### Teacher-only: the map of wrong answers

| Their number | Likely cause |
|:--:|---|
| no-mask text model near 1.6-1.9 | the switch never reached the blocks (Mistake 1) |
| loss floor near 0.87 on copy | scored over every place (Mistake 2) |
| lookup accuracy stuck near 0.8 | repeated keys (Mistake 3) |
| copy heads look 7 or 5 back, not 6 | off-by-one in `copy_batch` (SEP missing) |
| every single-head switch-off is 1.00 on copy | correct here; redundancy |
| a model with one head off gets worse *everywhere later* | `silence` not reset (Where This Goes Wrong 7) |
| lookup no-norm 1.00 | fine; luck of the seed (`key_lookup.py`) |

Use these as a prompt for conversation, not a certainty.

### Answers to every question posed in the lesson

| In the lesson | Answer |
|---|---|
| Rank the four parts | No wrong ranking; measured: residual ≫ positions, no norm helped, no mask leaks |
| Which of the four was added because somebody proved it? | We tested none in Weeks 15-17 |
| What would a test look like? | Delete one thing, change nothing else, compare on unseen text |
| How would a good model differ from one that peeks? | A model that peeks fails the future-change test |
| Copy chance; lookup chance | 0.125; 0.1 |
| Which column does the answer-place light up on the copy heatmap? | 6 back |
| Predict the best validation | Measured: no mask (0.077), a leak; of the honest four, no norm (1.478) |
| What is suspicious in the task grid? | Copy and reverse no-mask 1.00 (leak); lookup no-mask 0.37 and no-norm 0.33 (not leaks) |
| What is in `x` at place 6, and what is the answer at place 6? | The answer is in `x` at place 7 |
| Does the no-norm result mean norms are useless? | We do not know (limit 6) |
| Four heads look 6 back; switch off one: nothing. What does the stripe prove? | Where it looks, not that it is needed |
| Which name would you trust more after seeing the switch-off? | One with a test behind it; cards C and D (L0 H0 off: 0.48; L1 H0 off: 0.80) |
| What did we not do? | Find why no-norm helped; find why no-mask breaks lookup; more seeds; other sizes; any real large model |
| What is a leak? | The model can see the answer |

---

## 🔮 Next Week Preview

**Week 20 — Tokenizers: BPE From Scratch** (🟩 lab). Words are too many and letters too few. The student writes byte-pair encoding themselves (repeatedly merge the most common adjacent pair), passes round-trip tests (emoji, Devanagari, the empty string), then (**the only place in Level 4**) diffs it against a `tokenizers` BPE trained **locally** on local text. New syntax (teacher-only until taught): `collections.Counter`, `str.encode("utf-8")`, `re.compile(...).findall`, and the `tokenizers` `BpeTrainer`. The TinyGPT from Weeks 17 and 19 is not retrained next week.

**What from today carries over:** the three fair-test rules, the leak test, and the habit of writing down what was not tested. **If Week 17 or Week 19's grid shows under 60% on "what does the gap mean?" or "what is a leak?", redo those first.**
