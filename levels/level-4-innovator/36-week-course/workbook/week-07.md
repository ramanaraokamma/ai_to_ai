# Workbook — Week 7: The Symptom-Check-Action Playbook

**Name:** ________________________________  **Date:** ______________

[⬅ Course Home](../README.md) · [📖 Read the chapter first](../student-guide/week-07.md) · [Course Home](../README.md) · [Next ➡](week-08.md)

---

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the worked examples came from real CPU runs (one thread, seeds 0, 1, 2, 60 epochs). If your third decimal differs, that is fine. If a *verdict* differs, tell your teacher.
>
> Run everything from inside `36-week-course/` so that `from l4lib.spirals import run` works, with `knobs.py` from the chapter saved next to your files. **Import `l4lib`. Never copy it.**
>
> **No real statistics this week.** "Twice the spread" is a habit for not fooling yourself. It is not a proof. Everything here is about *this network on the two spirals*.

---

![Map of the 36 weeks with Week 7, the Symptom-Check-Action Playbook project, highlighted in Term 1](../figures/fig-w07-0-where-this-fits.svg)
*Figure 7.0 — Week 7 is the project that closes the stretch on training on purpose: the sweep, the table and the playbook.*

## ✅ Warm-Up (5 min)

**W1.** You train the same network three times and only `seed` changes. The three final validation losses are different. Name **one** thing that the seed changes. ____________

**W2.** Three runs ended at 0.10, 0.12, 0.14. What is the **mean**? ____________ Roughly how far do they wobble around it (the **spread**)? ____________

**W3.** Dropout and weight decay are tools against one problem. Which? ____________

**W4.** A loss of 0.693 is what a two-class model scores when it is doing what? ____________ (Week 1.)

**W5.** `for a, b in zip(xs, ys):` walks two lists together. Write what `for x in xs:` walks. ____________

![Three bars of final validation loss for the identical baseline run: 0.0367, 0.0499 and 0.0301 for seeds 0, 1 and 2](../figures/fig-w07-1-same-code-three-seeds.svg)
*Figure 7.1 — The seed alone moves the result: same code and data, and 0.0499 is about 66% bigger than 0.0301.*

---

## 🔮 Page 7.1 — Predict Before the Sweep

**Do this page before you run `sweep.py`.** Nothing here has a right answer. It is a calibration card: at the end you find out how well you know this network.

The sweep changes **one knob at a time** from the baseline (`lr 3e-3`, batch 64, no dropout, no weight decay, no norm, no schedule). There are 24 rows besides the baseline (page 7.2 counts them).

**P1.** How many of the 24 rows do you think will be **WORSE** than the baseline (gap bigger than twice the spread)? ____________

**P2.** How many **better**? ____________ How many **inside noise**? ____________

**P3.** Circle the **one knob** you think matters most:  `lr`   `batch_size`   `dropout`   `weight_decay`   `norm`   `schedule`

**P4.** For each of these, write **better / worse / no difference** and your confidence (1 to 5):

| Row | My guess | Confidence |
|---|:--:|:--:|
| `dropout 0.3` | __________ | ____ |
| `weight_decay 0.1` | __________ | ____ |
| `batch_size 512` | __________ | ____ |
| `norm layer` | __________ | ____ |
| `schedule cosine` | __________ | ____ |
| `lr 1e-2` | __________ | ____ |

**P5.** One sentence: *the result I would be most surprised by is* ________________________________

________________________________________________________________

**After the sweep.** Fill in with your own table:

| | My guess | What the table said |
|---|:--:|:--:|
| WORSE rows | ____ | ____ |
| better rows | ____ | ____ |
| inside noise | ____ | ____ |

Which guess surprised you most? ________________________________________

---

## 🔢 Page 7.2 — Count the Runs (by hand; no code for C1-C4)

**There is no new maths this week.** The only arithmetic is multiplying to count combinations. Then you check one line with `itertools.product`.

The knob lists in `knobs.py` are:

| Knob | Values | How many |
|---|---|:--:|
| `lr` | 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 | ____ |
| `batch_size` | 8, 32, 128, 512 | ____ |
| `dropout` | 0.0, 0.1, 0.3, 0.5 | ____ |
| `weight_decay` | 0.0, 0.01, 0.1, 1.0 | ____ |
| `norm` | none, batch, layer | ____ |
| `schedule` | none, cosine, cosine+warmup, step | ____ |

**C1.** Total values (add): ____ + ____ + ____ + ____ + ____ + ____ = ____________

**C2.** One knob at a time, 3 seeds (0, 1, 2): ____ x 3 = ____________ runs. Plus the baseline under 3 seeds: ____________ runs in total. (`sweep.py` should report this number.)

**C3.** Every combination of **all six** knobs (multiply, not add): ____ x ____ x ____ x ____ x ____ x ____ = ____________ configurations. Times 3 seeds: ____________ runs.

**C4.** Our 75 runs took about 30 seconds, so about 0.4 seconds per run. Estimate the time for the full grid: ____________ seconds, which is about ____________ minutes. *(Write "estimate" next to your answer. You did not run it.)*

**C5.** How many pairs does `itertools.product([1e-3, 1e-2], [0, 1, 2])` make? Predict: ____________ . Then write the six pairs you expect, in order:

________________________________________________________________

**C6.** Now run it (`grid.py` from the chapter) and compare. Did the order match? ____________

**C7.** Steps per epoch. There are 840 training points and only whole batches count (`840 // batch_size`, floor division). Fill in:

| `batch_size` | steps per epoch | steps in 60 epochs |
|:--:|:--:|:--:|
| 8 | ________ | ________ |
| 64 | ________ | ________ |
| 512 | ________ | ________ |

**C8.** What do we give up by changing one knob at a time? Finish: *we cannot see two knobs* ________________________________

---

## 🧮 Page 7.3 — Is It Noise? (by hand, then check)

**The rule.** For each row:

```text
gap     = (row's mean val loss) - (baseline's mean val loss)
spread  = the larger of the row's spread and the baseline's spread
verdict = "inside noise"      if |gap| < 2 x spread
          "WORSE" / "better"  otherwise   (WORSE if the loss went up)
```

Use **three decimals** and a calculator. The baseline is **0.039 +/- 0.008**. The spread here is `std` dividing by 3 (`ddof=0`), as in Level 3 Week 11.

**Worked example (done for you).** `lr 1e-4` is 0.079 +/- 0.012. Gap = 0.079 - 0.039 = **0.040**. Spread = max(0.012, 0.008) = 0.012, so 2 x spread = **0.024**. 0.040 is more than 0.024: **WORSE**.

**Now you.**

| Row | Mean +/- spread | gap | 2 x spread | Verdict |
|---|:--:|:--:|:--:|---|
| `dropout 0.3` | 0.043 +/- 0.013 | ________ | ________ | ______________ |
| `norm batch` | 0.024 +/- 0.005 | ________ | ________ | ______________ |
| `schedule step` | 0.033 +/- 0.001 | ________ | ________ | ______________ |

**H1.** One of these three is **close to the line**. Which, and by how much? ________________________________

**H2.** `norm batch` has the lowest mean in the whole table. Is it the winner? Write one sentence that uses the words *gap* and *twice the spread*.

________________________________________________________________

**H3.** `schedule step` has a tiny spread (0.001) against the baseline's 0.008. What is a **spread** finding? Write what you can and cannot say, with "on the spirals" and "3 seeds".

________________________________________________________________

________________________________________________________________

**H4 - the baseline's own seeds.** The three baseline validation losses are 0.0367, 0.0499, 0.0301.

```
mean   = (0.0367 + 0.0499 + 0.0301) / 3 = ____________
largest / smallest = 0.0499 / 0.0301 = ____________   (that is a ____ % swing with nothing changed)
```

**H5 - stretch.** `lr 1e-2` has seeds 0.059, 0.090, 0.139. Mean = ____________ . Spread (`std`, divide by 3) is about 0.033. The baseline is 0.039 +/- 0.008.
gap = ____________ ; 2 x spread = ____________ ; verdict: ____________ .
Its mean is about ____ times the baseline's. Yet the verdict is not "WORSE". What is the honest line for the playbook?

________________________________________________________________

**H6 - check with code.** Run `table.py`. Did your three verdicts in the table above match it? ____________ If not, which digits did you round? ____________

![Two rows each with a gap bar and a twice-the-spread bar: dropout 0.3 is inside noise, learning rate 1e-4 is WORSE](../figures/fig-w07-2-gap-versus-twice-spread.svg)
*Figure 7.2 — A difference counts only when the gap is longer than twice the larger spread.*

---

## 📈 Page 7.4 — Read Four Curves

Each of these is a real run (seed 0, 60 epochs), read off at epochs 0, 10, 30 and 59. `gnorm59` is the gradient length on the last mini-batch only, so treat it as rough.

```text
run                  train ep0    ep10    ep30    ep59  val ep59  gnorm59    lr59
healthy (defaults)       0.675   0.028   0.030   0.007     0.037    0.026   3e-03
lr = 1e-5                0.694   0.693   0.691   0.683     0.679    0.049   1e-05
lr = 0.1                12.786   0.612   0.698   0.693     0.702    0.025   1e-01
batch_size = 512         0.694   0.629   0.239   0.027     0.079    0.163   3e-03
norm = batch             0.423   0.187   0.065   0.117     0.019    1.111   3e-03
```

The six shapes:

- **A** healthy: falls fast, flattens low.
- **B** a huge number at epoch 0.
- **C** flat near 0.693 the whole time.
- **D** training loss far below validation loss (fits the training points, not new ones).
- **E** still falling when the epochs run out.
- **F** validation loss *below* training loss.

**R1.** Label each run with the letter (or letters) that fit. Then write **the one number** that proves it.

| Run | Letter(s) | The number that proves it |
|---|:--:|---|
| defaults | ____ | ______________________ |
| `lr = 1e-5` | ____ | ______________________ |
| `lr = 0.1` | ____ | ______________________ |
| `batch_size = 512` | ____ | ______________________ |
| `norm = batch` | ____ | ______________________ |

**R2.** Two runs end with almost the same loss (about 0.69). Which two? ____________ and ____________ . The number that separates them: ____________

**R3.** For `batch_size = 512`, the gradient length is biggest (0.163). Does that prove anything? (Hint: how many update steps did it get? See C7.)

________________________________________________________________

**R4.** For `norm = batch`, validation (0.019) is well below training (0.117). Write **a guess** why, and **one check** that would test the guess. *Do not state the guess as a fact.*

Guess: ________________________________________________________________

Check: ________________________________________________________________

**R5.** Run `snap.py` yourself. Did your rows agree with the printed ones to about 0.005? ____________ Which row differed most? ____________

---

## 📊 Page 7.5 — Reading the Sweep

Use **your own** `table.py` output. Write your digits, not mine.

**S1.** The three baseline validation losses (seeds 0, 1, 2): ____________ , ____________ , ____________ . Nothing changed between them except the seed. By what percentage do the largest and smallest differ? ____________

**S2.** Four rows are the baseline wearing a different hat. Write their names:

____________ , ____________ , ____________ , ____________

**S3.** `seeds.py` printed `1` for each seed when it counted distinct values. What does that prove about the harness? Finish: *the noise is* ____________ *not* ____________ .

**S4.** Count the verdicts in your table (24 rows):  WORSE ____ ;  better ____ ;  inside noise ____ . Which rows are WORSE? ________________________________

**S5.** Dropout and weight decay have eight rows between them. How many **beat** the baseline? ____________ Write one sentence with the words "on the spirals" saying what you can and cannot claim.

________________________________________________________________

**S6.** The row with the lowest mean is ____________ . Is its gap bigger than twice the spread? ____________

**S7.** Which knob had the smallest effect? Give your answer **with a spread**: ________________________________

**S8.** Write **one claim the table does not support** (something people often believe about these knobs). Say which row shows it.

________________________________________________________________

**S9.** *The epoch budget.* The chapter re-ran the sweep at 30 epochs. The baseline's spread went from 0.008 to 0.055, and `batch_size 512` went from inside noise to WORSE. In one sentence, why must every playbook claim state its epoch count?

________________________________________________________________

---

## 📝 Page 7.6 — Your Playbook

Rule the page into four columns and fill **at least six rules.** Each rule uses this frame:

> *When I see ___ , I check ___ , and if ___ I will ___ . In my run, ___ gave ___ +/- ___ and the baseline gave ___ +/- ___ , at 60 epochs, 3 seeds, on the spirals.*

| # | SYMPTOM (a number I can see) | CHECK (one cheap thing) | ACTION (one change) | EVIDENCE (row, mean +/- spread, epochs) | Gap > 2 x spread? |
|:--:|---|---|---|---|:--:|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

(Add more on your own page.)

**The three questions from the court.** Before you hand a rule in, tick:

- [ ] Which row, how many seeds, at how many epochs? (answered in EVIDENCE)
- [ ] Is the gap bigger than twice the spread? (answered in the last column)
- [ ] Did I check, or did I guess the cause? (if I guessed, the CHECK column says how to test it)

**The contradiction rule.** Write **one rule the table contradicted** - something you predicted on page 7.1 that was wrong - and say so in the first words.

________________________________________________________________

**The limitations line** (required, at the top of your playbook). Finish each:

- One knob at a time, so I cannot see ____________________________________
- Only ____ seeds, so my spread is ____________________________________
- Seeds change the weights and batch order but not ____________________, so the real wobble is probably ____________________
- Only this network on the two spirals, so I say nothing about ____________________

**Mark yourself** (out of 7; 5 or more is a pass):

| # | Criterion | ✓ |
|:--:|---|:--:|
| 1 | At least six rules in SYMPTOM, CHECK, ACTION form | |
| 2 | Every rule cites a row of **my own** table, with spread and epoch count | |
| 3 | Every rule says whether the gap beats twice the spread | |
| 4 | At least one rule the data contradicted, and it says so | |
| 5 | No cause stated as a fact where the check was never run | |
| 6 | My sweep table is attached, from my own `sweep.py` | |
| 7 | The limitations line is present | |

---

## 🐞 Page 7.7 — Break It on Purpose

These are **deliberate** mistakes. Predict the error (or the silence!) before you run each. Save each as its own file next to `knobs.py`.

**Mistake 1.**

```python
# DELIBERATE MISTAKE 1: look at what product() hands back.
import itertools
from knobs import SEEDS

grid = itertools.product([1e-3, 1e-2], SEEDS)
print(len(grid))
```

Prediction: ____________ . Last line of the real error: ________________________________

Fix: ________________________________

**Mistake 2.**

```python
# DELIBERATE MISTAKE 2: a number where a list should be.
import itertools

grid = list(itertools.product([1e-3, 1e-2], 3))
```

Last line of the real error: ________________________________ . What did I mean to write? ____________

**Mistake 3 (silent).**

```python
# DELIBERATE MISTAKE 3: walk the same product twice.
import itertools
from knobs import SEEDS

grid = itertools.product([1e-3, 1e-2], SEEDS)
print(len(list(grid)))
print(len(list(grid)))
```

Predict the two numbers: ____________ and ____________ . What did it print? ____________ and ____________ . Why? (Hint: product makes pairs *on demand*, one at a time.)

________________________________________________________________

**Mistake 4 (silent).**

```python
# DELIBERATE MISTAKE 4: s = BASE is not a copy.
from knobs import BASE, settings
s = BASE
s["lr"] = 0.1
print(BASE["lr"])
```

Predict `BASE["lr"]` : ____________ . Printed: ____________ . In your own words, what is the difference between `s = BASE` and `s = copy_of(BASE)`?

________________________________________________________________

**Mistake 5 (silent).** In `sweep.py`, change the line that loops over seeds so that `seed` is always `0`. The sweep still runs. Which number in `table.py` gives it away? ____________ What value is it? ____________

---

## 📓 Page 7.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Keep this page; you will use it in Week 9's assessment.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more): write the one I made, or nearly made, this week. ________________________________________

Write this sentence in your own handwriting:

> **"One change, three seeds, a spread, and a number in the sentence."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **What are the three columns of a playbook rule, and what goes in each?**

________________________________________________________________

2. **What does `itertools.product(a, b)` give you, and why can you not call `len()` on it?**

________________________________________________________________

3. **Your friend says "dropout 0.3 scored 0.043, so dropout helps." What two questions do you ask?**

________________________________________________________________

4. *Parking Lot.* `batch_size 512` is fine at 60 epochs and bad at 30. Do **not** answer it with certainty. Write your best guess and the one thing you would count.

________________________________________________________________

**Mark yourself.** Tick the first line you can honestly say.

- [ ] **Not yet:** I can read a mean but not the spread.
- [ ] **Getting there:** I run the gap-versus-twice-spread rule by hand, but my playbook has rules with no numbers.
- [ ] **Secure:** six rules, each with a row, a spread, an epoch count, and a verdict; I say "on the spirals".
- [ ] **Beyond:** I noticed `lr 1e-2` (big mean, huge spread) cannot be called worse, and I wrote "add more seeds".

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-07.md) · [Next ➡](week-08.md)

---
---

# ✂️ ANSWERS - keep this page folded until you have finished

*Numbers come from real runs: CPU, one thread, seeds 0, 1, 2, 60 epochs, `l4lib.spirals.run`. Within +/-0.005 on a loss is a match; the **verdicts** must agree.*

### Warm-Up

- **W1.** The starting weights (and the order of the batches). The data stays the same.
- **W2.** Mean 0.12. Spread about 0.016 (`std` dividing by 3); "about 0.02" or "between 0.10 and 0.14" is fine.
- **W3.** Overfitting.
- **W4.** Guessing (probability one half each class, so `ln 2`).
- **W5.** One item at a time from `xs`.

### Page 7.1

No right answers. The reveal: of 24 rows, **20 inside noise** (4 are the baseline repeated), **4 WORSE** (`lr 1e-5`, `lr 1e-4`, `lr 0.1`, `dropout 0.5`), **0 better**. The knob that matters most is `lr`. Common wrong guesses: "dropout and weight decay help" (none beat the baseline); "a bigger batch is fine" (inside noise at 60 epochs, WORSE at 30).

### Page 7.2

| Knob | Count |
|---|:--:|
| `lr` 5, `batch_size` 4, `dropout` 4, `weight_decay` 4, `norm` 3, `schedule` 4 | |

- **C1.** 5 + 4 + 4 + 4 + 3 + 4 = **24**.
- **C2.** 24 x 3 = **72**; plus 3 baseline runs = **75**.
- **C3.** 5 x 4 x 4 x 4 x 3 x 4 = **3,840**; x 3 seeds = **11,520** runs.
- **C4.** 11,520 x 0.4 = about 4,600 seconds, about **77 minutes** (estimate; not run).
- **C5/C6.** 2 x 3 = **6** pairs, in this order: (0.001, 0), (0.001, 1), (0.001, 2), (0.01, 0), (0.01, 1), (0.01, 2). The first list changes slowest.
- **C7.** 840 // 8 = **105** steps per epoch, 6,300 in 60 epochs. 840 // 64 = **13**, 780 total. 840 // 512 = **1**, **60** total.
- **C8.** ...two knobs *interacting* (for example a big learning rate behaving differently with a big batch).

### Page 7.3

| Row | gap | 2 x spread | Verdict |
|---|:--:|:--:|---|
| `dropout 0.3` | 0.043 - 0.039 = 0.004 | 2 x 0.013 = 0.026 | inside noise |
| `norm batch` | 0.024 - 0.039 = -0.015 | 2 x 0.008 = 0.016 | inside noise, **borderline** |
| `schedule step` | 0.033 - 0.039 = -0.006 | 2 x 0.008 = 0.016 | inside noise |

- **H1.** `norm batch`: |gap| 0.015 is just under 0.016, short of the line by 0.001.
- **H2.** No. Its gap (0.015) is below twice the spread (0.016), so the rule calls it inside noise; the lowest of 24 noisy numbers is not a winner.
- **H3.** The spread (0.001) is the smallest in the table, against 0.008. You may say: on the spirals, with 3 seeds, a decaying schedule looked *steadier*, not lower. You may not say it is better, or that it will hold on another dataset.
- **H4.** Mean = **0.0389**. 0.0499 / 0.0301 = **1.66**, a **66%** swing with nothing changed.
- **H5.** Mean = **0.096**. gap = 0.096 - 0.039 = 0.057; 2 x spread = 2 x 0.033 = 0.066; **inside noise**. The mean is about **2.5** times the baseline's. Honest playbook line: "add more seeds before concluding".
- **H6.** These hand sums use rounded figures; the code uses unrounded ones. The verdicts agree.

### Page 7.4

| Run | Letter | Proving number |
|---|:--:|---|
| defaults | **A** | train 0.675 to 0.028 to 0.007; val 0.037 |
| `lr = 1e-5` | **C** | 0.694 at epoch 0, 0.683 at epoch 59; gradient length 0.049 |
| `lr = 0.1` | **B** (start) and **C** (end) | epoch 0 train 12.786, then 0.693 flat |
| `batch_size = 512` | **E** | 0.629 at epoch 10, 0.239 at epoch 30, 0.027 at epoch 59 |
| `norm = batch` | **F** | val 0.019 below train 0.117 |

(D is not used by any of these five runs.)

- **R2.** `lr = 1e-5` (0.683) and `lr = 0.1` (0.693). The epoch-0 loss: 0.694 against 12.786.
- **R3.** No. It is one mini-batch's reading, and it is simply still falling: 512 gives 1 step per epoch, 60 steps in all, against 780 for batch 64. The honest check is to count steps.
- **R4.** Any honest guess earns credit if it is labelled as a guess. Our guess (**untested**): the logged training loss is an average taken in train mode while the model was changing, and validation is scored in `eval()` mode. Check: recompute the training loss in `eval()` mode. Do not "fix" anything first.
- **R5.** Your digits should match to about 0.005.

### Page 7.5

- **S1.** 0.0367, 0.0499, 0.0301; about **66%**.
- **S2.** `dropout 0.0`, `weight_decay 0.0`, `norm none`, `schedule none`.
- **S3.** The harness is deterministic, so the noise is **the seed**, not **the code**.
- **S4.** WORSE **4**, better **0**, inside noise **20**. The four WORSE rows: `lr 1e-5`, `lr 1e-4`, `lr 0.1`, `dropout 0.5`.
- **S5.** **Zero** of eight beat the baseline. Sample sentence: "On the spirals, with 3 seeds and 60 epochs, I found no detectable gain from dropout or weight decay; I cannot say they do nothing, and I cannot say anything about other data."
- **S6.** `norm batch` (0.024). No: 0.015 is under 0.016.
- **S7.** Accept any answer that cites a spread. The best-supported is `schedule`: all three non-baseline values are inside noise, with smaller spreads (0.003, 0.007, 0.001) than the baseline (0.008).
- **S8.** For example: "layer norm is better than no norm" (0.057 +/- 0.031 against 0.039 +/- 0.008: the mean is *higher* and the spread huge). Or "dropout 0.3 helps" (inside noise).
- **S9.** Because a run that is still learning when the budget runs out can look worse (or better) than it would at another budget; the conclusion changes with the epoch count.

### Page 7.6

A model playbook is in the teacher guide; your wording will differ. Judge yourself against the marking table on the page. Reminders: a cause is a guess until a check has been run (rule 5 of the marking); "cosine is best (0.034)" cannot be said when `step` is 0.033, since three seeds cannot rank them; "batch 8 is best because its train loss is low" is false here: its train loss (0.018) is **higher** than the baseline's (0.007).

Limitations line: one knob at a time, so I cannot see interactions; only 3 seeds, so the spread is very rough; seeds do not change the **data**, so the real wobble is probably bigger; only this network on the spirals, so I say nothing about other models or data.

### Page 7.7

- **Mistake 1.** `TypeError: object of type 'itertools.product' has no len()`. Fix: `list(itertools.product(...))`.
- **Mistake 2.** `TypeError: 'int' object is not iterable`. Meant `[3]`, `range(3)` or `SEEDS`.
- **Mistake 3.** Predicted 6 and 6; it prints **6** then **0**. The first `list(grid)` used the iterator up. Fix: build the list once, `grid = list(...)`.
- **Mistake 4.** Predicted 0.003; it prints **0.1**. `s = BASE` gives the same dict a second name, so changing `s` changes `BASE` and every later run inherits it. `copy_of(BASE)` builds a new dict with the same entries.
- **Mistake 5.** The three seeds come out identical, so the spread is exactly **0**. A spread of exactly zero is a sign of identical runs, probably a hard-typed seed.

### Bug Log and Self-Check

Bug Log: any real entries are fine if the **last line** (not the whole traceback) was copied and the fix works.

1. SYMPTOM: what I see (a number); CHECK: one cheap thing to look at; ACTION: one change, with the number that backs it.
2. It gives every combination of its lists, one at a time, on demand; it never builds the list, so it does not know its own length. Wrap it in `list(...)` to count.
3. "What is the baseline's number and spread?" and "Is the gap bigger than twice the spread?" Here 0.043 - 0.039 = 0.004, inside noise.
4. Reading, not proof: batch 512 gets only 60 update steps in 60 epochs (780 for batch 64), so it may be still learning when time stops; at 30 epochs that shows. One thing to count: steps = `840 // batch_size` x epochs.

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-07.md) · [Next ➡](week-08.md)
