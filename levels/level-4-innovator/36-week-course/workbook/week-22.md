# Workbook — Week 22: After Pretraining (SFT, Reward Model, DPO)

**Name:** ________________________________  **Date:** ______________

[⬅ Week 21](week-21.md) · [📖 Read the chapter first](../student-guide/week-22.md) · [Course Home](../README.md) · [Next ➡](week-23.md)

---

![Map of the 36 weeks with Week 22, After Pretraining: SFT, Reward Model, DPO, highlighted in Term 3](../figures/fig-w22-0-where-this-fits.svg)
*Figure 22.0 — Week 22 is the fourth lesson of Term 3: what is done to a model after pretraining.*

> **Rules for this workbook.** Seven pages and a Bug Log. **Write your prediction or your hand answer first, then run.** A guess written after the run is not a guess. Every number you write in the write-up (page 22.6) must have been printed by **your own** run, with the seed stated.
>
> **Everything today is a toy on purpose.** There is **no language model and no stand-in anywhere in this workbook.** The "scores" on page 22.1 are random numbers, the reward model on pages 22.2 and 22.5 is five weights fitted to ten invented judgements, and the "policy" on pages 22.3 and 22.4 is four numbers. They show a mechanism. They say **nothing** about what happens to a real assistant.
>
> **Real numbers.** Every printed number below came from a real CPU run (PyTorch, one thread, the seeds shown). By-hand numbers are plain arithmetic and will match exactly. On another PyTorch build the **last digit** of a loss can move; the story does not. Numbers marked **PRACTICE** are invented for this workbook so they are not the class numbers.
>
> **Files you need.** The files you typed in class: `sftmask.py`, `pairs.py`, `kl.py`, `reward.py`, `dpo.py` (and, for pages 22.4 and 22.5, `sweep.py` and `hack.py`). Run them in **one Python session** when a page says "needs": `reward.py` and `dpo.py` make names the later files use. Nothing today imports `l4lib`.
>
> **Calculator.** `ln` and `e^x` keys (a phone is fine, airplane mode on). Carry **four decimals** and round only the answer.

---

## ✅ Warm-Up (5 min, before anything else)

Five quick questions to settle the ideas you need before the pages start.

**W1.** A model that knows nothing about **12** tokens gives each one `1/12`. Its first loss should be `ln 12` = ____________ (three decimals).

**W2.** A judge who has no idea which of two answers is better says `0.5` for each. The loss `-ln 0.5` is ____________ (four decimals).

**W3.** In one sentence, what does **masking the prompt** stop the loss from doing? (Does the model still *read* the prompt?) _____________________________________________

**W4.** Circle one. KL divergence of a table from **itself** is: `0` / `1` / `ln 2` / can be negative.

**W5.** Circle one. In this course the **first** table in `KL(p || q)` is the: **policy** / **reference**.

---

## 🎭 Page 22.1 — The Mask (needs `sftmask.py` and `pairs.py` · 15 min)

This page is for practising how a prompt mask changes which guesses are scored. Predict each answer, then run `sftmask.py` and `pairs.py` to check.

**A. Count the guesses.** A sequence of 9 tokens gives ____ guesses (the last token has nothing after it). The guess at place `t` is for token `t + 1`.

**B. Predict the count.** With a prompt of length `L`, the number of guesses that **count** is `8 - (L - 1)`. Fill in before you run:

| Prompt length `L` | Rows set to `-100` | Guesses that count (predict) |
|:--:|:--:|:--:|
| 3 | | |
| 5 | | |
| 7 | | |

**C. Run it.** In `sftmask.py` change `PROMPT_LEN` to 3, run, then to 7, run. **Leave the `torch.manual_seed(0)` line where it is**; the scores must be the same random scores every time. Copy out the `targets_sft` line and the masked loss.

| `PROMPT_LEN` | `targets_sft` | Masked loss (4 decimals) | Loss over all 8 |
|:--:|---|:--:|:--:|
| 3 | | | |
| 5 | `[[-100, -100, -100, -100, 4, 4, 1, 6]]` | `4.0407` | `3.8008` |
| 7 | | | |

Did the "loss over all 8" change when you changed the prompt length? Yes / No. Why? _____________________________________________

**D. The mask by characters (hand first).** A new typed example, **PRACTICE**:

```text
PROMPT = "q: 2+2?\na:"      ANSWER = " four.\n"
```

Count the characters in the prompt (the `\n` is **one** character): ____ . In the answer: ____ . Total characters: ____ . Guesses in all: ____ . **Guesses that count: ____ .**

Now put this `PROMPT` and `ANSWER` into `pairs.py` and run it. Did your count match? ____ (If not, where did you lose one?) _____________________________________________

**E. Shapes.** In `sftmask.py` the by-hand route makes `logp`, `want` and `picked`. Write their shapes from memory, then print them to check: `logp` ________ `want` ________ `picked` ________

**F. Two sentences.** (1) Which of your two losses in part C is the *SFT* loss? ____________ (2) The masked loss was **higher** than the all-8 loss at `PROMPT_LEN = 5`. Does that mean masking made the model worse? Explain in one sentence, using the word *guesses*. _____________________________________________

---

## ⚖️ Page 22.2 — Judge: Bradley-Terry by Hand (15 min)

The chance that answer `w` beats answer `l` is `sigmoid(r(w) - r(l))`. The loss is `-ln` of that chance. Only the **gap** between the two rewards matters.

**A. Warm hands** (from class; check with your calculator). `sigmoid(x) = 1 / (1 + e^(-x))`.

| Chosen reward | Rejected reward | Gap | `sigmoid(gap)` | Loss `-ln sigmoid(gap)` |
|:--:|:--:|:--:|:--:|:--:|
| 0.3 | 0.8 | | | |
| 2.0 | 0.0 | | | |

**B. Four rewards (PRACTICE).** `e = 1.5`, `f = 0.5`, `g = -1.0`, `h = 2.0`.

1. `P(e beats f)` = ____________ (4 decimals)
2. `P(h beats e)` = ____________
3. `P(f beats g)` = ____________
4. A judge says **`g beats h`**. The gap is ____ , `sigmoid` of it is ____________ (5 decimals), and the loss is ____________ (3 decimals).
5. A judge says **`f beats g`** (the sensible verdict). The loss is ____________ (4 decimals).
6. How many times bigger is the loss in 4 than in 5? About ____ . In a sentence: what does the loss do to a confident mistake? _____________________________________________
7. Add 100 to every reward. `P(e beats f)` becomes ____________ . So a reward has no "____".

**C. The loss at the start.** With all five weights `0`, every reward is `0`. The gap is ____ , the chance is ____ , the loss is ____________ . Which line of `reward.py`'s output should show this? ____________

**D. Run `reward.py`.** Copy out:

| Step | 1 | 100 | 500 |
|---|:--:|:--:|:--:|
| BT loss | | | |

The five weights (write the sign):

| Feature | Weight |
|---|:--:|
| `has_numbered_steps` | |
| `gives_direct_answer` | |
| `hedges_a_lot` | |
| `over_400_chars` | |
| `refuses` | |

Train-pair agreement: ____ / 10 . Circle the features that **raise** the reward: steps · direct · hedges · over 400 · refuses .

**E. Predict, then check.** The ranking printed by `reward.py` lists `r1` first and `r5` last. Without looking, write the reward of `r2` (`[0, 1, 0, 0, 0]`) using your weights: ____________ . Then check against the printout: ____________ .

---

## 🪢 Page 22.3 — Leash: KL on Paper, and DPO on One Pair (25 min)

This page is for computing KL and a single DPO loss by hand, so the numbers on the next page are not a black box.

**Rule for every KL:** the **policy** `p` is first and the **reference** `q` is second. Natural logs (`ln`), four decimals. Write the four log-ratios first, multiply each by the policy's **own** chance, then add.

```text
          A      B      C      D
   q   0.25   0.25   0.25   0.25      the reference
   p1  0.50   0.25   0.125  0.125     moved a little
   p2  0.70   0.10   0.10   0.10      moved a lot
```

**A. Rounds from class.**

| Round | `p` against `q` | The four `ln(p/q)` | KL |
|:--:|---|---|:--:|
| 1 | `p1` against `q` | | |
| 2 | `p2` against `q` | | |
| 3 | `q` against `q` | | |
| 4 | `q` against `p2` (swapped!) | | |

Rounds 2 and 4 use the same two tables. Why are the answers different? _____________________________________________

**B. A table that is not from class (PRACTICE).** `p3 = [0.40, 0.40, 0.10, 0.10]` against the same `q`.

| Outcome | `p3` | `p3 / q` | `ln(p3/q)` | `p3 x ln(p3/q)` |
|:--:|:--:|:--:|:--:|:--:|
| A | 0.40 | | | |
| B | 0.40 | | | |
| C | 0.10 | | | |
| D | 0.10 | | | |

`KL(p3 || q)` = ____________ . **Before adding,** predict: bigger or smaller than `KL(p2 || q)`? ____________

**C. Your own table.** Write four chances that add to 1: `p = [ ____ , ____ , ____ , ____ ]`. Predict "bigger or smaller than 0.4458": ____________ . Put it into `kl.py` (`p = torch.tensor([...])`, then `print(kl(p, q))`) and write the result: ____________ . Right? Y / N

**D. The ceiling (stretch).** Keep `q` as it is. As one chance in `p` goes toward `1` and the rest toward `0`, the KL tends to `-ln(0.25)` = ____________ . Try `p = [0.97, 0.01, 0.01, 0.01]` in `kl.py` and write the KL: ____________ . Is it below the ceiling? Y / N

**E. The plain average.** For `p1`, the plain average of its four log-ratios (not weighted by `p1`) is ____________ . Is that KL? Y / N . Why not? _____________________________________________

**F. DPO on ONE pair, by hand.** The reference's log-chances for (chosen, rejected) are `(-20.0, -18.0)`. The policy's are now `(-19.0, -19.5)`.

- Chosen moved: ____ . Rejected moved: ____ . Gap (chosen minus rejected): ____ .
- The margin is `beta x gap`. At `beta = 0.1`: margin ____ , `sigmoid` ____ , loss ____________ (4 decimals).
- At `beta = 5`: margin ____ , `sigmoid` ____ , loss ____________ (it is tiny: write it as `0.00000_`).
- The movement is the **same** in both lines. Which `beta` still "wants" the model to move? ____________ . Why? _____________________________________________

**G. A second pair (PRACTICE).** Reference `(-15.0, -14.0)`, policy now `(-13.0, -15.0)`.

| `beta` | Chosen moved | Rejected moved | Margin | Loss |
|:--:|:--:|:--:|:--:|:--:|
| 0.1 | | | | |
| 0.5 | | | | |

The loss at `beta = 0.5` should equal the loss of a **Bradley-Terry** pair from page 22.2 with the same gap. Which one? Pair ____ beats ____ .

---

## 🎛️ Page 22.4 — Two Leashes (needs `dpo.py` · 20 min)

This page is for running `dpo.py` at several `beta` values and filling in the table from your own runs.

The reference policy (before any training) is `A=0.168 B=0.206 C=0.375 D=0.251`. Which answer does the *reference* like best? ____ . Which answer do the six preferences say is best? ____

**A. Predict.** From page 22.3 part F, write `beta = 5.0` or `beta = 0.1`: the one whose loss is satisfied **sooner** is ______ . So after the same 300 steps, the one that moved **less** is ______ .

**B. Run and fill.** In your `dpo.py` session, run `run_dpo(b, 300)` for the five `beta`s (`sweep.py` does exactly this; if you type it yourself the loop is two lines). Then run it again with **3000** steps.

| `beta` | A (300) | KL (300) | loss (300) | A (3000) | KL (3000) |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.02 | | | | | |
| 0.1 | | | | | |
| 0.5 | | | | | |
| 1.0 | | | | | |
| 5.0 | | | | | |

**C. Read the table.**

1. Which column **cannot** be compared across rows? ____________ . Why? (Say what `beta` does to the number inside `logsigmoid`.) _____________________________________________
2. At 300 steps, is the KL smallest at the smallest `beta` (0.02)? Y / N . Which `beta` has the **largest** KL at 300 steps? ____
3. At 3000 steps, what does `A` look like for `beta` from `0.02` to `1.0`? _____________________________________________
4. The most KL this toy can ever reach is `-ln(0.16839)` = ____________ (all the chance on A). Which rows at 3000 steps are at or almost at it? _____________________________________________
5. In your own words: "small `beta` means a long leash" is **true / false / only after enough steps** (circle one). Which row of your table is the evidence? _____________________________________________
6. `A = 0.997` is "very sure", not "right". Nothing in the KL says the model that moved further is *better*. Write one thing you would have to measure, that we did not, to say so. _____________________________________________

**D. The trap (one sentence to carry to Week 23).** "The loss cannot tell you ______________________ ." (Use your `beta = 0.1` and `beta = 5.0` rows.)

---

## 🕳️ Page 22.5 — Hack: What the Judge Cannot See (needs `reward.py`, then `hack.py` · 15 min)

This page is for working out, by hand and then with `hack.py`, what the trained reward model does and does not score.

**A. From `reward.py`.** `r9` is `[1, 0, 0, 0, 0]`: numbered steps and **nothing else**: it answers nothing. Its reward: ____________ . `r2` (short and direct) has ____________ . Does `r9` beat `r2`? Y / N . Which **weight** does the hacked answer use? ____________

**B. Find every hack.** Each answer is five 0/1 features, so there are `2 x 2 x 2 x 2 x 2 =` ____ possible answers. Using **your** five weights, work out by hand which of them score **above `r2`**. Start with the ones that have `has_numbered_steps = 1`. List them with their rewards:

_______________________________________________________________________________

_______________________________________________________________________________

Now cross out any that have `gives_direct_answer = 1`. What is left is the answers that **beat a short, direct answer while answering nothing**: ____________________

*(There are only 32 rows. Write them by hand, in order of `has_numbered_steps` first; no new code today.)*

**C. The blind spot.** Now run `hack.py` (needs `POOL` and `PAIRS` from `reward.py`). It adds a sixth feature, `is_factually_correct`, and two answers `r7` (correct) and `r8` (wrong) that are identical otherwise.

| | `r7` (correct) | `r8` (wrong) |
|---|:--:|:--:|
| Reward | | |

Weight of `is_factually_correct` after training: ____________ . Is it zero because facts do not matter? Y / N .

**D. Why exactly zero.** Look at `PAIRS`. In every pair, both answers are correct, so the feature's value in the winner minus its value in the loser is ____ in all ten pairs. A feature with a difference of 0 adds nothing to the gap, so its gradient is ____ , so its weight never moves from ____ . In one sentence, what would you add to `PAIRS` to fix this? _____________________________________________

**E. Claims.** Mark each **supported** or **not supported** by anything you ran today.

| Claim | Supported? |
|---|:--:|
| "The reward model learned that numbered steps are good." (in this toy) | |
| "Reward models know what is true." | |
| "Real assistants are reward-hacked in this way." | |
| "This toy's weights would be the same with ten different raters." | |

---

## ✍️ Page 22.6 — Write-Up: What a Toy Showed and What It Did Not (20 min)

Use the lines below, or a sheet of paper. **Every number must come from your own run**; next to each, write the seed or "no randomness".

**1. The mask (`sftmask.py`, seed ____ ).** I measured: all 8 guesses ____________ , the last 4 ____________ . It shows: _____________________________________________ . It does **not** tell us: _____________________________________________

**2. The judge (`reward.py`, seed ____ ).** I measured: loss at step 1 ____________ , step 500 ____________ ; biggest positive weight ____________ for ____________ ; `r9` reward ____________ . It shows: _____________________________________________ . It does **not** tell us: _____________________________________________

**3. The leash (`dpo.py`, no randomness).** I measured: `beta = 0.1` gives `A` = ______ , KL ______ , loss ______ ; `beta = 5.0` gives `A` = ______ , KL ______ , loss ______ . It shows: _____________________________________________ . It does **not** tell us: _____________________________________________

**4. The trap, in your own words.** Why is the smaller DPO loss not the better model? _____________________________________________

**5. The four new constructs**, each in one sentence, in **your own words**. Run `constructs.py` (from your teacher) and copy the four outputs beside them.

- `F.logsigmoid(x)`: ____________________________ Output: ____________________
- `F.log_softmax(scores, dim=-1)`: ____________________________ Output: ____________________
- `logp.gather(1, index)`: ____________________________ Output: ____________________
- `tensor.detach()`: ____________________________ Output: ____________________

**Check your sentences:** did you say *why* `logsigmoid` beats `torch.log(torch.sigmoid(x))` (the second gives `-inf` when the sigmoid is tiny)? Y / N . Did you say what `gather` needs (a column of column-numbers, none of them `-100`)? Y / N . Did you say what `detach` is **for** today (the frozen reference)? Y / N

---

## 🐞 Page 22.7 — Break It on Purpose (three bugs · 25 min)

**Each program is deliberately broken.** Do **not** run it first. For each, write **(i)** what the bug is, **(ii)** what you think the output says, **(iii)** the fixed line. *Then* run it.

**The reading method.** If there is an error, read the **last line**. If there is no error, ask what should be *true* of the output and check it: does one row of chances add to 1? Is a loss ever negative? How many guesses should count?

**Bug 22.7-A. (SILENT)** Six positions, five tokens. The programmer wants each **row** of chances to add to 1. Predict all four lines.

```python
# DELIBERATE BUG 22.7-A (SILENT): log_softmax is taken down the columns, not along each row.
import torch
import torch.nn.functional as F
torch.manual_seed(0)
rows = torch.randn(6, 5)
targets = torch.tensor([1, 4, 0, 2, 2, 3])
good = F.log_softmax(rows, dim=-1)
bad = F.log_softmax(rows, dim=0)
print("one row of chances adds to, good:", round(good[0].exp().sum().item(), 3))
print("one row of chances adds to, bad :", round(bad[0].exp().sum().item(), 3))
print("loss, good:", round(-good.gather(1, targets.reshape(-1, 1)).mean().item(), 4))
print("loss, bad :", round(-bad.gather(1, targets.reshape(-1, 1)).mean().item(), 4))
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 22.7-B. (SILENT)** A reward model with three features. `win` should end up with the **higher** reward. Predict the sign of the loss and which reward goes up.

```python
# DELIBERATE BUG 22.7-B (SILENT): the minus sign in front of logsigmoid is missing.
import torch
import torch.nn.functional as F
X = {"win": torch.tensor([1.0, 0.0, 1.0]), "lose": torch.tensor([0.0, 1.0, 1.0])}
w = torch.zeros(3, requires_grad=True)
opt = torch.optim.Adam([w], lr=0.1)
for step in range(1, 101):
    loss = F.logsigmoid(X["win"] @ w - X["lose"] @ w)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step in (1, 10, 100):
        print(f"step {step:3d}  loss {loss.item():+.4f}   reward(win) {(X['win'] @ w).item():+.3f}   reward(lose) {(X['lose'] @ w).item():+.3f}")
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Bug 22.7-C. (SILENT)** This is page 22.1 part D, with a mask that starts one place too late. You already counted the right answer by hand.

```python
# DELIBERATE BUG 22.7-C (SILENT): the mask starts one place too late (compare pairs.py).
import torch
PROMPT = "q: 2+2?\na:"
ANSWER = " four.\n"
text = PROMPT + ANSWER
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
ids = torch.tensor([stoi[c] for c in text])
targets = ids[1:].clone()
targets[:len(PROMPT)] = -100
print("guesses that count:", int((targets != -100).sum()), "of", len(targets))
kept = [text[i + 1] for i in range(len(targets)) if targets[i] != -100]
print("the characters it is scored on:", "".join(kept).replace("\n", "\\n"))
```

(i) The bug: ___________________ (ii) I predict: ___________________ (iii) Fix: ___________________

**Which one would you catch without printing a check, and which not?** Three bugs ran with **no error**. For each, write the one thing you would print to catch it: A: ____________ B: ____________ C: ____________

---

## 📓 Page 22.8 — The Bug Log

This page is for recording what went wrong today and the habit that would catch it next time.

Every entry needs a line from a **real** run of yours this week.

**Entry 1: a prediction I got wrong.** *"I predicted ______________, and the run printed ______________, because ____________________."*

_______________________________________________________________________________

**Entry 2: the one I was most tempted to believe.** The sentence *"a low loss means the model is good"* was contradicted twice today. Write the two pairs of numbers (yours, from pages 22.1 and 22.4) and a sentence of your own.

Pair 1: ____________ vs ____________ Pair 2: ____________ vs ____________

_______________________________________________________________________________

**Entry 3: a slip, not a gap.** A mark or a digit you lost that you knew how to get (an `ln` of the wrong thing, a swapped KL, `-100` where it does not belong). What was it, and what is the one habit that would have saved it?

Slip: ____________________ Habit: ___________________________________________

**Entry 4: the silent ones.** Name the habit you will use after each of these: `softmax` or `log_softmax` → ____________ . A loss that starts negative → ____________ . A mask → ____________ (hint: print something).

**Entry 5: the honest limits.** One thing today's toys *cannot* tell you about a real assistant, in your own words:

_______________________________________________________________________________

| Date | Where it happened | The symptom | What I thought it was | What it really was | The check that proved it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

---

## 🧠 Self-Check (from memory, no notes)

Six questions to answer without looking back at the pages.

1. The guess at place `t` is for token ____ . With a prompt of 5 tokens, the first ____ rows are set to ____ .
2. The Bradley-Terry loss is `-F.logsigmoid(` ____ `)` . At the start it is ____ .
3. `KL(p || q)` is ____ when `p = q`, and it is / is not (circle) the same as `KL(q || p)`.
4. `beta` is the ____ on the margin (the strength of the implicit KL leash), not a KL we compute. A bigger `beta` is satisfied ____ (sooner / later).
5. `ref_logp` ends in `.detach()` because ___________________________________ .
6. One sentence: a toy showed me ________________ but not ________________ .

---

## ✂️ ANSWERS - keep this page folded until you have finished

> Real printed outputs below. By-hand numbers are exact to the digits shown; where you carried fewer decimals, anything within `0.002` is fine. These answers are for the pages in **this workbook**.

### Warm-Up

**W1.** `ln 12 =` **2.485** (the random scores on page 22.1 are *worse* than this). **W2.** **0.6931**. **W3.** It stops the loss from **scoring the prompt's own tokens**. The model **still reads the prompt**; only the scoring is blanked. **W4.** **0**. **W5.** **policy**.

### Page 22.1

**A.** **8**. **B.**

| `L` | Rows set to `-100` | Count |
|:--:|:--:|:--:|
| 3 | 2 | 6 |
| 5 | 4 | 4 |
| 7 | 6 | 2 |

**C.**

| `PROMPT_LEN` | `targets_sft` | Masked loss | Loss over all 8 |
|:--:|---|:--:|:--:|
| 3 | `[[-100, -100, 9, 11, 4, 4, 1, 6]]` | `3.9767` | `3.8008` |
| 5 | `[[-100, -100, -100, -100, 4, 4, 1, 6]]` | `4.0407` | `3.8008` |
| 7 | `[[-100, -100, -100, -100, -100, -100, 1, 6]]` | `4.0043` | `3.8008` |

The all-8 loss does **not** change: it never looks at the mask. **D.** Prompt `q: 2+2?\na:` is **10** characters (`q`, `:`, space, `2`, `+`, `2`, `?`, newline, `a`, `:`), the answer ` four.\n` is **7**, total **17**, guesses **16**, **7 count** (the first answer character, the space, is guessed from the last prompt character, so it counts). The printed line is `guesses that count: 7 of 16` when you use the correct mask. **E.** `logp` `(8, 12)`, `want` `(8, 1)`, `picked` `(8, 1)`. **F.** (1) The **masked** one. (2) **No**: the two numbers are averages over **different sets of guesses**, and the scores are random; there is no rule that a masked loss is lower or higher.

### Page 22.2

**A.**

| Gap | `sigmoid` | Loss |
|:--:|:--:|:--:|
| `-0.5` | `0.3775` | `0.9741` |
| `+2.0` | `0.8808` | `0.1269` |

**B.** 1. `0.7311`. 2. `0.6225`. 3. `0.8176`. 4. gap `-3.0`, `sigmoid` `0.04743`, loss **`3.049`**. 5. Loss **`0.2014`**. 6. About **15** times (`3.049 / 0.2014 = 15.1`): a confident mistake costs far more than a confident success. 7. Still `0.7311`; a reward has no "**zero**" (only differences matter).

**C.** Gap `0`, chance `0.5`, loss **`0.6931`**: the step-1 line of `reward.py`.

**D.** Loss `0.6931`, `0.0135`, `0.0017`. Weights: `+5.047`, `+4.578`, `-2.794`, `-2.534`, `-6.091`. Agreement **10 / 10**. Raise the reward: **steps** and **direct**.

**E.** `r2` is `[0, 1, 0, 0, 0]`, so its reward is the direct-answer weight alone: **`+4.578`**.

### Page 22.3

**A.**

| Round | `ln(p/q)` | KL |
|:--:|---|:--:|
| 1 | `+0.6931, 0, -0.6931, -0.6931` | `0.1733` |
| 2 | `+1.0296, -0.9163, -0.9163, -0.9163` | `0.4458` |
| 3 | all `0` | `0` |
| 4 | `q` against `p2` | `0.4298` |

Rounds 2 and 4 differ because KL is **not symmetric**: in round 4 the log-ratios are weighted by `q`'s chances (`0.25` each), not `p2`'s. Always say which table goes first.

**B.** Log-ratios `+0.4700, +0.4700, -0.9163, -0.9163` (`0.4 / 0.25 = 1.6`, `ln 1.6 = 0.4700`; `0.1 / 0.25 = 0.4`, `ln 0.4 = -0.9163`). Products `+0.1880, +0.1880, -0.0916, -0.0916`. `KL(p3 || q)` = **`0.1927`**: **smaller** than `0.4458` (it moved less). For reference, the swapped order is `0.2231`.

**C.** Any four chances adding to 1. The nearer your table is to `[0.25, 0.25, 0.25, 0.25]`, the smaller the KL. Check with `kl.py`.

**D.** `-ln 0.25 =` **`1.3863`**. For `[0.97, 0.01, 0.01, 0.01]` the KL is **`1.2186`**, below the ceiling.

**E.** **`-0.1733`**. **No**: it is not weighted by `p1`, and KL is never negative.

**F.** Chosen moved **`+1.0`** (`-19.0 - (-20.0)`); rejected moved **`-1.5`** (`-19.5 - (-18.0)`); gap **`2.5`**. At `beta = 0.1`: margin **`0.25`**, `sigmoid` **`0.5622`**, loss **`0.5759`**. At `beta = 5`: margin **`12.5`**, `sigmoid` **`1.0000`**, loss **`0.000004`**. **`beta = 0.1`** still wants the model to move (a loss of `0.58` is far from satisfied); at `beta = 5` the loss is already almost zero, so its gradient is almost zero.

**G.** Chosen moved `-13.0 - (-15.0) =` **`+2.0`**; rejected moved `-15.0 - (-14.0) =` **`-1.0`**; gap **3.0**.

| `beta` | Margin | Loss |
|:--:|:--:|:--:|
| 0.1 | `0.3` | `0.5544` |
| 0.5 | `1.5` | `0.2014` |

(At `beta = 0.5`: `sigmoid(1.5) = 0.8176`.) That is page 22.2 part B item 5: **`f` beats `g`** (reward gap `1.5`). At `beta = 5` the margin is `15` and the loss is about `0.0000003`.

### Page 22.4

Reference likes **C** (`0.375`); the preferences say **A** is best. **A.** `beta = 5.0` is satisfied sooner, so it moved **less** after 300 steps.

**B.**

| `beta` | A (300) | KL (300) | loss (300) | A (3000) | KL (3000) |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 0.02 | 0.782 | 1.213 | 0.5317 | 1.000 | 1.782 |
| 0.1 | 0.997 | 1.760 | 0.2560 | 1.000 | 1.782 |
| 0.5 | 0.987 | 1.709 | 0.0513 | 1.000 | 1.781 |
| 1.0 | 0.950 | 1.557 | 0.0204 | 0.999 | 1.772 |
| 5.0 | 0.589 | 0.566 | 0.0020 | 0.802 | 1.095 |

(The 3,000-step columns are from the course's own run of `sweep.py`; they are not in the reference module. Your last digit may move.)

**C.** 1. The **loss**: `beta` scales the number inside `logsigmoid`, so losses from different `beta` are different units. 2. **No.** The KL at `beta = 0.02` (`1.213`) is *smaller* than at `beta = 0.1` (`1.760`), but the smallest of all is at `beta = 5.0` (`0.566`), so it is not simply "smaller `beta`, smaller KL". The **largest** at 300 steps is **`beta = 0.1`** (`1.760`). The sequence `1.213, 1.760, 1.709, 1.557, 0.566` is **not monotone**. 3. `A` is `1.000` (or `0.999` at `1.0`): all the chance has moved onto A. 4. `-ln(0.16839) =` **`1.7815`**. At 3000 steps, `beta` `0.02`, `0.1`, `0.5` (`1.782, 1.782, 1.781`) and `1.0` (`1.772`) are at or almost at it; `beta = 5` (`1.095`) is still climbing. 5. **Only after enough steps**: at 3,000 steps small `beta` goes furthest; at 300 steps the sweep mixes "how far it wants to go" with "how fast it gets there" (the `0.02` row has not arrived yet). 6. Any honest answer: for example, whether the answers are better by some measure other than the chance of A, judged by a person, or the quality of what it *says*; a toy with four numbers has no words to judge.

**D.** "The loss cannot tell you **which model is better**" (or "**how far the model moved**"): `beta = 5.0` has loss `0.0020` and `A = 0.589`; `beta = 0.1` has loss `0.2560` and `A = 0.997`.

### Page 22.5

**A.** `r9` is **`+5.047`**; `r2` is **`+4.578`**. **Yes**, `r9` wins. It uses the **`has_numbered_steps`** weight. **B.** `2^5 =` **32**. Above `r2`: `[1, 1, 0, 0, 0]` (`+9.625`), `[1, 1, 0, 1, 0]` (`+7.091`), `[1, 1, 1, 0, 0]` (`+6.831`), `[1, 0, 0, 0, 0]` (`+5.047`): **4 of 32**. Crossing out the ones with `gives_direct_answer = 1` leaves only **`[1, 0, 0, 0, 0]`**, which is `r9`. (Many other answers with steps lose because they also carry a negative weight.)

**C.** `r7` **`+9.625`**, `r8` **`+9.625`**. Weight of `is_factually_correct`: **`+0.000`**. **No**: it is zero because **the data never asked** (facts were never the thing that differed). **D.** The difference is **0** in all ten pairs, the gradient is **0**, the weight never moves from **0**. Fix: add a pair where the two answers differ **only** in correctness (the module's statement; not run here).

**E.** First claim: **supported** (the weight is `+5.047`; this is a statement about the toy). "Reward models know what is true": **not supported** (`hack.py` shows the opposite in this toy). "Real assistants are reward-hacked in this way": **not supported** (background from the module; we did not run or measure one). "Same weights with ten different raters": **not supported** (the ten preferences are invented and perfectly consistent; we never varied them).

### Page 22.6

Rubric (full marks need all four): (1) your own numbers, each with a seed (`sftmask.py` and `reward.py` seed `0` / `1`, `dpo.py` no randomness: for reference, `3.8008` and `4.0407`; `0.6931` and `0.0017`, `+5.047`, `r9` `+5.047`; `0.997`, `1.760`, `0.2560` and `0.589`, `0.566`, `0.0020`); (2) one sentence per toy saying what it shows **and what it does not** (no real model, invented preferences, four numbers for a policy); (3) the loss-across-`beta` trap in your own words; (4) the four constructs: `logsigmoid` stays finite where `log(sigmoid)` gives `-inf` (at `x = -200`: `-inf` against `-200.0`); `log_softmax` gives log-chances along the last axis; `gather` picks one column per row and needs an index of column numbers, never `-100`; `detach` cuts the graph, used for the frozen reference. Do not write "DPO is better than RLHF" (not tested), "the model learned to prefer" (four numbers moved), or "lower loss is better".

### Page 22.7

**22.7-A.** (i) `dim=0` normalises each **column**, not each row. (ii) Good row adds to `1.0`; bad row adds to something else; both losses look fine. (iii) `dim=-1`. **Output:**

```text
one row of chances adds to, good: 1.0
one row of chances adds to, bad : 0.507
loss, good: 2.1809
loss, bad : 2.3157
```

The bad loss is a believable number about nothing. The catch: add up **one row** after the softmax.

**22.7-B.** (i) `F.logsigmoid(...)` without the leading minus. (ii) The loss is **negative** at step 1 and keeps falling; `reward(win)` goes **down** and `reward(lose)` goes up. (iii) `loss = -F.logsigmoid(...)`. **Output:**

```text
step   1  loss -0.6931   reward(win) -0.100   reward(lose) +0.100
step  10  loss -1.9715   reward(win) -1.014   reward(lose) +1.014
step 100  loss -20.8173   reward(win) -10.512   reward(lose) +10.512
```

The catch: a loss is never negative; step 1 should print `+0.6931` (`ln 2`).

**22.7-C.** (i) `targets[:len(PROMPT)]` masks 10 rows; it should be `len(PROMPT) - 1` (9). (ii) `6 of 16`, and the scored characters begin at `f`, not at the space. (iii) `targets[:len(PROMPT) - 1] = -100`. **Output:**

```text
guesses that count: 6 of 16
the characters it is scored on: four.\n
```

The catch: compare the count with your hand count (7) and print the characters it is scored on.

Catches: A: one row after the softmax adds to 1; B: the sign of the step-1 loss (`+0.6931`); C: the guess count against your hand count.

### Page 22.8 and Self-Check

**Bug Log Entry 2** should name: masked `4.0407` against all-8 `3.8008` (page 22.1) and `beta = 5` loss `0.0020` against `beta = 0.1` loss `0.2560` (page 22.4). **Self-Check:** 1. `t + 1`; 4; `-100`. 2. the reward of the winner minus the reward of the loser; `0.6931`. 3. `0`; is **not**. 4. scale; sooner. 5. the reference must stay a frozen copy of where the policy started (no graph, no gradient); without it the "reference" moves with the policy or raises an error. 6. Any honest sentence; the usual answer: a toy showed a **mechanism** but not what happens to a real assistant.
