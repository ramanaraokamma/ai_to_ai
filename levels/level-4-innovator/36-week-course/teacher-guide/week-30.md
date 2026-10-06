# Week 30 — Evaluating LLM Systems: The Frozen Suite and the Judge

[⬅ Week 29](week-29.md) · [Course Home](../README.md) · [Week 31 ➡](week-31.md) · [Student Guide](../student-guide/week-30.md) · [Workbook](../workbook/week-30.md)

---

![Thirty-six week tiles in four lanes, one per term; weeks 1 to 29 solid, week 30 tinted pink and pointed at in term 4, weeks 31 to 36 dashed](../figures/fig-w30-0-where-this-fits.svg)
*Figure 30.0 — Week 30 of 36, term 4: how we decide whether any of it worked, before the system card in the last weeks.*

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~55 min: 25 of pen and paper, 30 at the computer) |
| **Type** | 🟦 Teach — the student builds the **measuring instrument** before anything is measured with it: a 30-ticket, 5-label eval set that is **frozen** with a fingerprint; a scorer that reports every category, not just the average; two cheap baselines (a floor that always gives one answer, free keyword rules) and one small trained classifier; a **contamination scan** that keeps eval tickets out of training; and finally a test of the **judge** itself. The judge is a scripted stand-in with a planted habit of preferring whichever answer it sees first, and the student recovers that habit by asking every question twice in both orders. |
| **Big idea** | **Freeze the eval before you build. Beat the cheap baseline first. Then test the judge itself.** An eval written after the system is an eval written to flatter it. A system that cannot beat free rules has not earned its complexity (here a trained classifier scores `0.700` against the rules' `0.833`). A judge is a measuring instrument and instruments are calibrated: agreement between two raters means little until the **agreement expected by luck** has been taken out (**Cohen's kappa**), and a pairwise judge with a position habit will hand you a wrong verdict from a single run (`19` of `20` seeds say "v1 is better" when the rubric says v2 is better in `20` of `30` pairs). |
| **New vocabulary** | eval set · frozen (a fingerprint recorded at freeze time) · baseline (floor, free rules, trained) · per-category score · contamination · near-duplicate · Jaccard overlap · rubric · judge · rater · agreement · agreement by chance · Cohen's kappa · position bias · flip rate · consistent pair |
| **New maths** | **Cohen's kappa.** Agreement with the agreement-by-luck taken out: `κ = (p_o − p_e) / (1 − p_e)`, where `p_o` is how often two raters actually agree and `p_e` is how often they would agree if each kept their own habit of saying pass or fail but never looked at the item. Worked **by hand on 20 ratings** (`p_o = 0.65`, `p_e = 0.44`, `κ = 0.375`) before the library is allowed near it. Nothing else: no confidence intervals, no weighted kappa, no significance test, and the colour-band names ("fair", "moderate") are said once as a convention, not a law. |
| **New syntax** | `cohen_kappa_score(y1, y2)` from `sklearn.metrics`, called **after** the hand calculation · set intersection `A & B` and union `A | B` for the Jaccard overlap (the student has met `set` and subset checks in Week 26) · `rng.choice([...])` on the seeded `random.Random` of Week 24, to break ties. That is three, as the ladder says. **One mirror rides along and is flagged, not counted:** `rng.random()` (the same object; a float between 0 and 1, used once to decide whether the planted habit fires). **Old and used freely:** `hashlib.md5` and `.encode("utf-8")` (Week 21; the freeze), `re.findall` (Week 20; words), `Counter` (Week 20), f-strings, `lambda` as a `key=` (Week 4), dict and list comprehensions, `zip`, `enumerate`, the `score`/`compare` pair that Week 31 will reuse. **Deliberately not used:** `re.sub` (Week 33's construct: the reference module's scan and scorer used it; here `re.findall` does the same job) and `collections.defaultdict`. |
| **Dataset** | **30 eval tickets** typed by the student (`evalset.py`: 6 greeting, 7 refund, 7 technical, 5 billing, 5 out_of_scope) and **66 raw training tickets** handed over (`traindata.py`: 14, 15, 14, 15, 8), two of which are too close to eval tickets on purpose. **30 pairs of canned replies** (`replies.py`) built from fixed templates by Python, and a three-point rubric. Nothing downloads. **No internet.** |
| **Model** | **There is no language model today.** Four things are scripted or tiny: the floor (always one answer), the free keyword rules, a TF-IDF plus logistic regression classifier trained from scratch on 64 tickets, and the **mystery judge in `mystery.py`, which is a stand-in, not a model: it reads a rubric score, not language**, and has a number `BIAS` typed into it. Everything measured about the judge is a property of that number. Nothing says how often a real judge model shows a position habit. |
| **Materials** | Laptop with Python 3, numpy, scikit-learn (nothing new) · the eight files of Section "Prep Checklist" in one folder · printed **Pages 30.1-30.3** (Activity) · a timer · a pen |
| **Prep time** | 30 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | The **whole** guide (every Prep block, every Clinic block and every Key block, top to bottom, one session) ran in **about 1 second of wall time** (0.9 s measured), most of it importing scikit-learn and fitting the small classifier in Block P2 (**under 1 second**). **No block takes more than about a second, so nothing is over the 10-second mark and nothing needs a recorded time.** Anything over 1 minute means something is wrong (see Fallback). |

> **⚠️ Watch out:** six things go wrong this week. **First, the student (and you) will read a number about the stand-in judge as a number about judges.** The judge's habit is `BIAS = 0.5`, typed into a file. The lesson is *how to find out*, not *how biased judges are*. Say "stand-in, not a model" every time the flip rate is on the board. **Second, one run of the bias test is one draw.** Thirty pairs give an estimate of `0.27` on seed 0 for a true `0.5`; over twenty seeds the estimates run from `0.27` to `0.70` (Block P9) and over two hundred the spread (SD) is `0.087` (Key K2). The student should leave knowing that a small test gives a wobbly answer, and that ten times the pairs cuts the wobble to about a third (SD `0.031`). **Third, the free rules baseline is not a clean baseline.** Eight of its 32 keys (`hiya`, `afternoon`, `send them back`, `postage`, `blank`, `closes`, `rendering`, `inbox`) occur in eval tickets and in **no** training ticket (Key K7), so the course author wrote the rules with the eval in view. `0.833` is therefore a generous score for "free rules", and on ten brand-new tickets the same rules score `5/10` (Key K5). Tell the student when it comes up (Page 30.1 d); do not hide it, and do not change the rules, because Week 31's numbers (`25/30`) stand on them. **Fourth, "flagged" is not "removed"; a scan with a threshold is a dial.** At `0.70` it finds two tickets; at `0.30` it removes seven, including a harmless one; at `0.95` it leaves the near-copy in. And it cannot see a paraphrase at all (Block P4: five paraphrases, highest Jaccard `0.200`, scan caught `0`, score `+2` tickets). **Fifth, kappa needs both cells.** A high raw agreement with `κ = 0` (Block P7) and a middling `κ` with all the disagreement in one direction (Mistake 7) are the two ways to misread it. **Sixth, the consistent-pairs verdict is only safe for THIS flaw.** It gives the rubric's answer exactly here because the only flaw is "sometimes says A"; a real judge may be consistently wrong (prefers the longer answer in both orders), and then no amount of swapping shows it. Say so.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say why the eval is written and frozen first**, and show the freeze: a fingerprint of the 30 cases is recorded, and editing one ticket by a single character makes `assert fingerprint(EVAL) == FROZEN` fail (Mistake 1).
2. **Score three cheap systems on the same 30 tickets and say what each number means**: the floor `6/30 = 0.200`, the free rules `25/30 = 0.833`, the trained classifier `21/30 = 0.700`; and say why the trained one has to be compared with the *rules*, not with the floor.
3. **Read a per-category table**, not just the average: the rules against the classifier is `0.833 → 0.700` overall, with `out_of_scope` falling `1.000 → 0.200` (`−0.800` on `n = 5`), billing `−0.200` and greeting `−0.167` flagged.
4. **Compute a Jaccard overlap by hand with `&` and `|`** (`7 / 9 = 0.778` for the near-copy), run the scan, say what it removed (`2` tickets) and what it cannot see (five paraphrases at highest Jaccard `0.200`), and say that the score rose by `+1` ticket when the copy was left in (`22` against `21`) and by `+2` when paraphrases were.
5. **Compute Cohen's kappa by hand on 20 ratings** (`7 / 7 / 0 / 6`; `p_o = 0.65`, `p_e = 0.44`, `κ = 0.375`), check it against `cohen_kappa_score`, and say why a judge that says "pass" to everything gets raw agreement `0.90` and `κ = 0` on a set where 18 of 20 pass.
6. **Catch a judge with a position habit by swapping the order**: first-position wins `38` of `60` (`0.633`, against `0.500` for no habit), `8` flips in `30`, and estimate the planted bias from the flip rate; then say why the single-order verdict ("v1 wins `16` of `30`") is the wrong one when the rubric says v2 is better in `20`.
7. **Say what the test cannot show**: that one run of `30` pairs is a wobbly measurement (`0.27` to `0.70` over twenty seeds), that flips on tied pairs are not bias (Mistake 11), and that a judge which is consistently wrong in both orders passes the swap test.

Observable evidence: the printed fingerprint and `True`, the three-line baseline table (`0.200 / 0.833 / 0.700`), the line `Jaccard = 7/9 = 0.778`, the kappa line `kappa = (0.6500 - 0.4400) / (1 - 0.4400) = 0.3750` beside the library's `0.375`, the bias summary of Block P8, and filled Pages 30.1-30.3 (Activity).

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist**, in the **🐞 Debugging Clinic** and in the **🔑 Answer Key** was run, in document order, from one folder, in one Python session on a CPU; the outputs below are the real printed output. The eight **file blocks** (`evalset.py`, `traindata.py`, `dedup.py`, `scorer.py`, `compare.py`, `baselines.py`, `replies.py`, `mystery.py`) are saved as files first and imported by the blocks after them. The Clinic blocks that are *deliberate mistakes* are marked and their tracebacks are real (paths are shortened to `/home/you/l4/`, and Python's and scikit-learn's own files to `/usr/lib/python3.10/...`; the source line under each frame is the line that ran). **Nothing here depends on the clock or the network: every count repeated exactly on a second run**, because the stand-in judge draws from a seeded `random.Random`, the classifier has `random_state=0`, and the replies are built from fixed templates. Blocks marked **TEACHER-ONLY** use something the student does not type. **Clinic and Key blocks use names from the Prep blocks** (`EVAL`, `TRAIN`, `TRAIN_RAW`, `texts`, `score`, `r_rules`, `r_tfidf`, `r_raw`, `pairs`, `items`, `H`, `J`, `bias_test`, `judge_pair`, `v1_better`, …); **run the Prep blocks first, in one session, in order.**

### 1. What the student is doing today, in one paragraph

For twenty-nine weeks the student has built things and looked at whether they worked. Today they build the thing that decides *whether they worked*. They begin by typing a **frozen eval set** of 30 support tickets in five categories, and a one-line fingerprint of it that will shout if anyone edits a ticket. They score three cheap systems on it (a floor that always says one thing, a list of keyword rules, and a small classifier trained from scratch) and are surprised that the trained one **loses** to the free rules, and that the loss is almost all in one category. They then protect the eval from the training data: a Jaccard overlap worked by hand on two sets of words, a scan that removes two tickets, and a demonstration that five paraphrases sail through it and still raise the score by two tickets. The second half is about the **judge**. On paper and then in code they compute Cohen's kappa for two raters on 20 replies (`0.375`), see why raw agreement is a bad measure, and then face a sealed file: a scripted pairwise judge. They ask it every question twice, once in each order, and count how often the answer changes. It changes in `8` of `30`; by swapping they recover a habit nobody told them about. The finishing sentence: *"the eval was written first and fingerprinted, the free rules beat my model, my scan cannot see a paraphrase, kappa puts the lenient judge at only `0.375` on a scale where `0` is luck and `1` is perfect, and the pairwise judge changed its mind on `8` of `30` when I swapped the order, so I do not trust a single-order verdict."*

### 2. 🔢 The maths you need — taught to you first

**One idea: Cohen's kappa.** Do it by hand once before class. Two raters, `H` (strict) and `J` (lenient), each say *pass* or *fail* to 20 replies. Tally the four kinds of pair:

```text
                      H says pass    H says fail
   J says pass            7              7          -> J passes 14 of 20
   J says fail            0              6          -> J fails   6 of 20
                      H passes 7     H fails 13
```

**Step 1 — how often did they agree?** The agreeing cells are "both pass" `7` and "both fail" `6`: `p_o = (7 + 6) / 20 = 0.65`.

**Step 2 — how often would two raters agree by luck?** Suppose each kept their own *habit* (`J` says pass 14 times in 20, `H` says pass 7 times in 20) and neither looked at the reply. Both say pass with chance `0.70 × 0.35 = 0.245`; both say fail with chance `0.30 × 0.65 = 0.195`. Luck alone agrees `p_e = 0.245 + 0.195 = 0.44` of the time. **Say it like this:** *"We agreed 65 percent of the time. Two people who never read the replies and just stuck to their habits would have agreed 44 percent of the time. So the real agreement is the part above 44."*

**Step 3 — the part above luck, as a share of what was available.** Above luck we got `0.65 − 0.44 = 0.21`; the most that could be above luck is `1 − 0.44 = 0.56`. So `κ = 0.21 / 0.56 = 0.375`. `κ = 1` means perfect agreement; `κ = 0` means no better than luck; it can go negative (worse than luck). **The convention** (say it once, call it a convention): below `0.2` poor, `0.2-0.4` fair, `0.4-0.6` moderate, `0.6-0.8` substantial, above `0.8` almost perfect. `0.375` is "fair".

**Why not just report agreement?** Second worked case: the human passes 18 of 20 replies and a lazy judge says "pass" to all 20. Agreement `= 18 / 20 = 0.90`. Luck: the judge passes always (`1.0`), the human passes `0.90`: `p_e = 1.0 × 0.90 + 0.0 × 0.10 = 0.90`. So `κ = (0.90 − 0.90) / (1 − 0.90) = 0`. **Ninety percent agreement, zero skill.** This is the sentence to leave the student with: *"a raw agreement number rewards a judge that never looks, whenever almost everything passes."* The denominator fails if `p_e = 1`, which happens only when **both** raters say the same single thing every time (two lists of all 1s): kappa is then **undefined** and the library returns `nan` with a warning. A judge that says one thing while the human says both is *not* that case: `p_e < 1` and `κ = 0` (Block P7, Key K3).

**Direction matters.** The grid above has `7` in one off-diagonal cell and `0` in the other: the lenient judge *never* fails what the human passes and passes `7` replies the human fails. Kappa compresses that into one number; the two cells say which way to lean (Mistake 7).

**The other arithmetic on the page (not new maths).** *Jaccard overlap* is the number of words two tickets share divided by the number of different words in either: `7 / 9 = 0.778`. *Flip rate* is a count over a count: `8 / 30`. **A line for you only (not taught):** for this stand-in the chance that a pair flips is exactly the planted `BIAS`, because an honest answer never changes with the order and a pair flips exactly when the habit fires in a way that is not hidden by luck (Key K2 checks it: the flip rate and `2 × (first-position win rate) − 1` are **the same number on all 200 seeds**). Use only "the flip rate estimates the planted bias" with the student; the algebra is yours.

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| The 30 eval tickets, the 66 training tickets | **Typed by the course author.** Short, invented, in one voice; they look nothing like a real support queue. |
| Fingerprint, freeze check, scorer, `compare` | **Real engineering.** The habit (write the eval first, fingerprint it, report every category) is the thing that transfers. |
| Floor and free rules | **Real, trivial systems.** The rules were written **with the eval in view** (Key K7), so `0.833` is generous. |
| The TF-IDF classifier | **A real trained model, tiny.** It scores `0.700` on this eval. That number is a property of 64 tickets and these 30; it says nothing about larger systems. |
| The contamination scan | **Real, and limited.** It is a word-overlap test. It finds copies and near-copies, never paraphrases. |
| The 30 pairs of replies and the rubric | **Built by Python from five fixed templates.** No model wrote them. The rubric (`short`, `routed`, `no promise`) is a program, which is why it can act as the answer key for the judge test. |
| **The mystery judge** | **A stand-in, not a model.** It reads a rubric score, not language. With chance `BIAS` it answers "A" without looking; otherwise it compares scores. **Every number about its flip rate is a statement about the number `0.5` in `mystery.py`.** |
| "Rater H" and "rater J" | **Two programs.** `H` passes a reply only if it scores 3 of 3; `J` passes at 2 of 3. They stand in for "a careful person" and "a lenient judge". |
| Anything said about real LLM judges | **Nothing was measured.** You may say that *the test* (swap the order; count the flips) is the one practitioners use. Do not say how often real judges flip, or that they prefer the first answer. |

**What you must NOT claim:** *"LLM judges prefer the first answer"* (not shown); *"fine-tuning never beats rules"* (the classifier lost on 30 tickets); *"kappa above 0.6 means the judge is good"* (it means agreement with these labels, and only as good as the labels); *"the scan protects you from leakage"* (it protects you from copies).

### 4. The three new constructs, for somebody who has never seen them

**`cohen_kappa_score(y1, y2)`.** From `sklearn.metrics`. It takes **two lists of labels of the same length**, one per rater, in the same item order, and returns the kappa. Here the lists are 0/1 (fail/pass). It does the arithmetic of Section 2. The student types it only **after** the hand calculation, as a check (`0.375` both ways). **Trap:** lists of different lengths raise `ValueError: Found input variables with inconsistent numbers of samples: [20, 19]` (Mistake 9); if **both** raters say only the same one thing, the answer is `nan`; if only one does, `κ = 0` (Block P7, Key K3).

**Set intersection `A & B` and union `A | B`.** The student has met sets in Week 26 (checking that cited ids are a subset of served ids). A **set** holds each item once and forgets order: `set(["a", "b", "a"])` is `{"a", "b"}`. `A & B` is the items in both; `A | B` is the items in either. `len(A & B) / len(A | B)` is the Jaccard overlap. `words(s)` in `dedup.py` builds the set with `re.findall(r"[a-z0-9]+", s.lower())` (Week 20's tool), so `"doesn't"` becomes `doesn` and `t`: a real quirk, and Page 30.1 (a3) uses it. **Trap:** `&` and `|` are **not defined on lists** (`TypeError: unsupported operand type(s) for &: 'list' and 'list'`, Mistake 5). **Guard:** two tickets with no letters or digits give `len(A | B) = 0` and a `ZeroDivisionError` without the `if (A | B)` test (Mistake 6).

**`rng.choice([...])`.** On a `random.Random(seed)` (Week 24): it picks one item of a list, reproducibly. Here it breaks a tie, `rng.choice(["A", "B"])`, when the stand-in judge sees two replies with the same rubric score. **The mirror:** `rng.random()` on the same object gives a float in `[0, 1)`; `if rng.random() < bias` is "with chance `bias`". Say "same object, another method". **Trap:** one generator for the whole test. A new `random.Random(0)` inside the loop makes every call draw the same number (Mistake 10).

### 5. The other code the student types — nothing new, but note these

- **Typed by the student:** the first eight lines of `evalset.py` and the freeze lines (`fingerprint`, `FROZEN`, the two `assert`s); `dedup.py` (`words`, `jaccard`, `decontaminate`); the loops in Blocks P2 to P6 that print the tables; `bias_test`. **Handed over, read together:** `traindata.py`, `scorer.py`, `compare.py`, `baselines.py`, `replies.py`, and `mystery.py` **sealed**.
- `fingerprint(cases)` is `hashlib.md5("\n".join(f"{t}|{y}" for t, y in cases).encode("utf-8")).hexdigest()`: Week 21's fingerprint over the **data** (so a changed comment or a reformatted line does not trip it, and a changed ticket or label does). The `.hexdigest()` mirror was flagged in Week 21. **First time:** print `fingerprint(EVAL)`, paste the 32 characters into `FROZEN`.
- `sum(h == 1 and j == 1 for h, j in zip(H, J))` counts the `True`s; a generator inside `sum` is the same as the list comprehension of Level 2 without the brackets (Week 23 used `sum(... for ...)`; Week 26 used `any(...)` the same way).
- `naive_v1 += fwd == "A"` adds a `bool` to an int (Week 29 did this with `bool(...)`).
- `score(preds, name)` returns a **dict** with `overall`, `correct`, `n`, `per_category` (`{label: (right, total, share)}`) and `wrong`. Week 31 reads exactly these keys.

### 6. What the numbers will say

All printed by the blocks in the Prep Checklist. Read them before class.

- **The data (P1).** `30` eval tickets `{'greeting': 6, 'refund': 7, 'technical': 7, 'billing': 5, 'out_of_scope': 5}`; the fingerprint `73b33debbc8d8c4241051bc5670ef4dd`; `66` raw training tickets; the scan removes `2` (`EXACT` train#28 against eval#8 at Jaccard `1.000`; `NEAR` train#57 against eval#23 at `0.778`); kept `64`: `{'greeting': 14, 'refund': 14, 'technical': 14, 'billing': 14, 'out_of_scope': 8}`. **(The indices are zero-based, as Python prints them.)**
- **The baselines (P2).** Floor `6/30 = 0.200` (it says `greeting`, because four labels tie at 14 in training and the first one seen wins; the best any constant could do on this eval is `7/30 = 0.233`). Free rules `25/30 = 0.833`. TF-IDF classifier `21/30 = 0.700`. The rules' five misses: `is there a time limit on sending items back?` (said `out_of_scope`), `do I pay postage to return something?` (said `greeting`, because `"hi"` is inside `something`), and three technical tickets that the greeting rule grabs first (`"hi"` sits inside `nothing` and `everything`, and `afternoon` is a greeting key). **It is worth a minute to read these aloud.**
- **Jaccard (P3).** `7 / 9 = 0.778`. The paraphrase of the same question, `could you tell me my current monthly charge?`, scores `0.000` against it.
- **Leakage (P4).** Trained on all 66: `22/30 = 0.733` (the exact copy makes one ticket right). Trained on the 64 clean plus five paraphrases: `23/30 = 0.767`. The scan catches `0` of the five; the highest Jaccards are `0.200, 0.083, 0.143, 0.143, 0.077`.
- **The replies (P5).** The rubric says v1 is better in `10` of the `30` pairs and v2 in `20`; no ties.
- **Kappa (P6, P7).** The 20-row table; `7 / 7 / 0 / 6`; `p_o = 0.65`, `p_e = 0.44`, `κ = 0.375`; the library agrees. The lazy judge: agreement `0.9`, `κ = 0.0`.
- **The mystery judge (P8, P9).** Seed 0: first-position wins `38/60 = 0.633`, flips `8/30 = 0.267`, naive `16/30`, consistent pairs `22` (`v1 8`, `v2 14`, so v1 `0.364`), the rubric's `0.333`. Twenty seeds: estimates `0.27` to `0.70`, average `0.475`; the naive "v1 wins" counts `15` to `25` (above `15`, i.e. "v1 is better", on `19` of `20` seeds); the sealed file says `BIAS = 0.5`.
- **The table (P10).** Rules to classifier: overall `−0.133`; greeting `−0.167`, billing `−0.200`, out_of_scope `−0.800` flagged; refund and technical `+0.143` each. Three regressions and an average that fell by four tickets.

### 7. The honest limits of today

1. **The judge is a dial.** `BIAS = 0.5` is a number someone typed. The test finds the number; it does not say how real judges behave.
2. **Thirty pairs is a small test.** The spread of the estimate is about `0.09` (SD, 200 seeds); a planted `0.1` is found with estimates from `0.03` to `0.23` (Key K6). Ten times the pairs makes it about `0.03`.
3. **Swapping finds position habit only.** A judge that is consistently wrong (prefers the longer reply in both orders) has a flip rate of zero and passes the test. The honest companion is kappa against labels you trust.
4. **Ties flip even for an honest judge** (`15` of `30`, Mistake 11). Drop tied pairs, or count them separately.
5. **The labels are the ceiling.** `H` is a program with three checks; a kappa against a sloppy human is a kappa against a sloppy human. The course has not taught labelling agreement between people; do not teach it today.
6. **Word overlap cannot see meaning.** The scan is a floor, not a wall. A dense-embedding scan would catch some paraphrases and over-remove others; it is not built here, and nothing in this course measures how well it works.
7. **The free rules are not clean** (Key K7). The lesson's comparison "trained model vs rules" is honest about *direction* (the model lost) but the rules' `0.833` is optimistic.
8. **30 tickets, 5 per category in two categories.** One ticket is `0.033` overall and `0.200` in a five-ticket category. Every "regression" in a five-ticket category is one or two tickets (Week 31 says this again).
9. **The eval tickets are short and tidy.** A real queue has typos, two problems in one message, and other languages. The lesson is the method.

### 8. The misconceptions you will actually meet

1. **"A higher score on the eval means a better system."** Only if the eval was frozen first, kept out of training and not tuned against (Mistakes 1, 3, 12).
2. **"The trained model must beat the rules; something is wrong with the code."** Nothing is wrong. `21` against `25` is the measured result (P2), and it is the reason the baseline comes first.
3. **"80 percent agreement is good."** Against what? Luck can give 90 (Block P7).
4. **"Kappa tells me whether the judge is right."** It tells you how far the judge agrees with these labels, beyond luck. Which way it errs is in the off-diagonal (Mistake 7).
5. **"If I run the judge once, that is the verdict."** Nineteen seeds of twenty say v1 wins; the rubric says v2 (Mistake 8).
6. **"No flips means no bias."** It means no *position* bias found, by a test that worked only if the generator was shared (Mistake 10).
7. **"Flips mean bias."** On tied pairs an honest judge flips half the time (Mistake 11).
8. **"The scan removed the leaks."** It removed the copies. It cannot see a reworded ticket (Block P4).
9. **"I fixed the rules and now they score 30 out of 30."** You read the eval; the score is a training score (Mistake 12).

### 9. How deep to go, and where to stop

Stop at: *"write the eval first and fingerprint it; beat the cheap baseline before anything fancy; look at every category; keep eval tickets out of training and know that a scan only finds copies; a judge is an instrument: take luck out of its agreement with kappa, swap the order to find a position habit, and remember one small run is one draw."* Do **not** go into: inter-annotator agreement between humans, weighted or multi-class kappa, confidence intervals, significance tests, how real benchmarks get contaminated, embedding-based deduplication, prompt wording for real judges, chain-of-thought judging, reward models (Week 22 did those) or any claim about a real model's judging habits. If the student asks "do real judges do this?", the true sentence is *"people who test them report position effects, and the swap test is how; I have not measured one in this course."* If they ask what a good kappa is: *"by convention above 0.6 is called substantial, but the right number depends on what a wrong verdict costs."*

### 10. 🧭 Where Week 30 sits

```text
   W5   a held-out set used to stop early           W31  the thing being measured: a tiny encoder,
   W21  hashlib.md5 fingerprints; exact duplicates        fine-tuned and LoRA-patched; THIS week's
   W23  a frozen set; the constant-answer baseline        frozen eval and score/compare show the
   W26  recall@k on 10 questions written first            per-category regression
   W29  a stand-in with a dial; the layers table    W32  calibration and abstention: a model that
                                                          is sure and wrong; reuses "a category fell
   W30  the frozen 30-ticket suite, three baselines,      while the average rose"
        the contamination scan, kappa by hand,      W34  Capstone 1: freeze 25 cases BEFORE any
        a judge with a planted position habit            component exists, with a committed hash
```

![Paired bars per category for keyword rules and a trained classifier, with REGRESSION marked on greeting, billing, out_of_scope and overall](../figures/fig-w30-1-average-hides-regressions.svg)
*Figure 30.1 — The average fell 0.133, but one category fell 0.800: read every category before you ship.*

![A two by two grid of pass and fail counts 7, 7, 0 and 6 beside three numbered arithmetic steps ending at kappa 0.375](../figures/fig-w30-2-kappa-beyond-luck.svg)
*Figure 30.2 — Kappa is the agreement left over once luck is taken out: 0.65 raw becomes 0.375.*

---

## 🧰 Prep Checklist

### 30 minutes the night before

1. Make a scratch folder. Create the **eight files** of the blocks below, exactly as printed, each with the name in its first comment line: `evalset.py`, `traindata.py`, `dedup.py`, `scorer.py`, `compare.py`, `baselines.py`, `replies.py`, `mystery.py`. **Keep `mystery.py` out of the student's sight** until the end of Part 5.
2. Type Blocks P1 to P10 in order into **one Python session** (or one file per block, run with `exec`), from that folder. Block P1 prints the fingerprint; compare it with `FROZEN` in `evalset.py` (the file asserts it on import, so a mistyped ticket stops you at once).
3. Compare every printed number with this guide. **If the counts differ from `30`, `66`, `64`, `2` and `14 14 14 14 8`, stop:** the rest of the guide's numbers, and Week 31's, are for those files. Nothing in the first ten blocks takes more than about a second.
4. Read Key K7 (the free rules were written with the eval in view) and decide what you will say when the student asks why the rules are so good. Read Key K2 so that you know how wobbly a single run is.
5. Print **Pages 30.1 to 30.3** (Activity) and the workbook pages.
6. **Week 31 will ask the student for `evalset.py`, `traindata.py`, `dedup.py`, `scorer.py` and `compare.py`.** Make sure the student's folder has all five at the end of the lesson, and that `python -c "import evalset"` succeeds there (if the fingerprint assertion fires, a ticket was mistyped).

**File 1 of 8 — `evalset.py`.** The student types the first eight tickets and the five freeze lines at the bottom in class, *before* anything else is built, and pastes the other twenty-two from your copy (typing them adds nothing). The freeze lines are explained in Block P1 and Section 2 of "What YOU need to know".

```python
# evalset.py - the FROZEN eval set. Written 2026-09-01, before any training. Do not edit.
# Each case is (text, gold_label). Here the category is the label itself.
import hashlib

LABELS = ["greeting", "refund", "technical", "billing", "out_of_scope"]

EVAL = [
    # ---- greeting (6) ----
    ("hey! quick one for you",                                  "greeting"),
    ("good afternoon, are you there?",                          "greeting"),
    ("hiya",                                                    "greeting"),
    ("hello - first time using this",                           "greeting"),
    ("morning, got a sec?",                                     "greeting"),
    ("hi, hope this is the right place",                        "greeting"),
    # ---- refund (7) ----
    ("these shoes are the wrong colour, how do I send them back?", "refund"),
    ("I'd like my money returned for order 55301",              "refund"),
    ("is there a time limit on sending items back?",            "refund"),
    ("package never arrived, I want reimbursing",               "refund"),
    ("do I pay postage to return something?",                   "refund"),
    ("cancel order 7781 and put the money back on my card",     "refund"),
    ("opened it, hated it - can I still send it back?",         "refund"),
    # ---- technical (7) ----
    ("clicking save does absolutely nothing",                   "technical"),
    ("everything is blank after I sign in",                     "technical"),
    ("the android version force closes on launch",              "technical"),
    ("my csv download has headers but no rows",                 "technical"),
    ("reset email never turns up in my inbox",                  "technical"),
    ("charts stopped rendering yesterday afternoon",            "technical"),
    ("keeps saying 'network error' on a perfect connection",    "technical"),
    # ---- billing (5) ----
    ("took the money twice on the 3rd",                         "billing"),
    ("swap me onto the yearly plan",                            "billing"),
    ("need a proper tax invoice for accounting",                "billing"),
    ("what am I paying per month right now?",                   "billing"),
    ("card expired, where do I put the new one?",               "billing"),
    # ---- out_of_scope (5) ----
    ("what's a good recipe for dosa?",                          "out_of_scope"),
    ("how tall is Mount Kilimanjaro?",                          "out_of_scope"),
    ("write my sister a birthday message",                      "out_of_scope"),
    ("explain quantum entanglement",                            "out_of_scope"),
    ("should I buy bitcoin?",                                   "out_of_scope"),
]

assert len(EVAL) == 30



# ---- the freeze: a fingerprint of the 30 cases, written down the day they were written ----
def fingerprint(cases):
    return hashlib.md5("\n".join(f"{t}|{y}" for t, y in cases).encode("utf-8")).hexdigest()


FROZEN = "73b33debbc8d8c4241051bc5670ef4dd"
assert len(EVAL) == 30
assert fingerprint(EVAL) == FROZEN, "the frozen eval set was edited"
```

**File 2 of 8 — `traindata.py`.** Handed over as a file (it is data; typing 66 tickets is not the lesson). Do **not** point at the two marked rows; the scan will find them.

```python
# traindata.py - training tickets, written AFTER the eval set.
TRAIN_RAW = [
    # ---- greeting (14) ----
    ("hi there", "greeting"), ("hello", "greeting"),
    ("hey, anyone around?", "greeting"), ("good morning", "greeting"),
    ("hi, hope you're well", "greeting"), ("yo", "greeting"),
    ("hello, is this the support chat?", "greeting"), ("hey team", "greeting"),
    ("good evening", "greeting"), ("hi again", "greeting"),
    ("morning!", "greeting"), ("hello there, quick question coming", "greeting"),
    ("hey, thanks for picking up", "greeting"), ("greetings", "greeting"),
    # ---- refund (14 + 1 planted duplicate) ----
    ("I want my money back", "refund"),
    ("how do I return this order?", "refund"),
    ("the jacket doesn't fit, can I send it back?", "refund"),
    ("please refund order 41822", "refund"),
    ("I was charged for something I returned last week", "refund"),
    ("can I get a refund if I opened the box?", "refund"),
    ("I'd like to cancel and be reimbursed", "refund"),
    ("the item arrived broken, I want a refund", "refund"),
    ("return label please", "refund"),
    ("how long do refunds take to show up?", "refund"),
    ("I changed my mind, refund me", "refund"),
    ("sent the wrong size, want my money back", "refund"),
    ("can I exchange instead of a refund?", "refund"),
    ("refund status for order 90210", "refund"),
    ("is there a time limit on sending items back?", "refund"),   # <-- EXACT dup of eval#8
    # ---- technical (14) ----
    ("the app crashes when I open settings", "technical"),
    ("I can't log in, it says invalid token", "technical"),
    ("the page is stuck loading forever", "technical"),
    ("export to CSV produces an empty file", "technical"),
    ("notifications stopped working after the update", "technical"),
    ("getting a 500 error on checkout", "technical"),
    ("the mobile app won't sync", "technical"),
    ("my dashboard shows no data since Tuesday", "technical"),
    ("search returns nothing for any query", "technical"),
    ("two-factor codes are never arriving", "technical"),
    ("the site looks broken in Safari", "technical"),
    ("uploading a photo fails at 90 percent", "technical"),
    ("I keep getting logged out every few minutes", "technical"),
    ("dark mode toggle does nothing", "technical"),
    # ---- billing (14 + 1 planted near-duplicate) ----
    ("I was charged twice this month", "billing"),
    ("how do I update my credit card?", "billing"),
    ("what plan am I on?", "billing"),
    ("can I switch to annual billing?", "billing"),
    ("my invoice for March is missing", "billing"),
    ("why did my price go up?", "billing"),
    ("cancel my subscription please", "billing"),
    ("do you offer a student discount?", "billing"),
    ("I need a VAT receipt", "billing"),
    ("when is my next payment due?", "billing"),
    ("the payment failed but money left my account", "billing"),
    ("how much is the pro tier?", "billing"),
    ("add a second seat to my account", "billing"),
    ("change the billing email address", "billing"),
    ("what am I paying each month right now?", "billing"),        # <-- NEAR dup of eval#23
    # ---- out_of_scope (8 -- deliberately under-represented) ----
    ("what's the weather in Chennai tomorrow?", "out_of_scope"),
    ("write me a poem about cricket", "out_of_scope"),
    ("who won the world cup in 2018?", "out_of_scope"),
    ("can you do my maths homework?", "out_of_scope"),
    ("what is the capital of Peru?", "out_of_scope"),
    ("tell me a joke", "out_of_scope"),
    ("translate 'good night' into French", "out_of_scope"),
    ("what stocks should I buy?", "out_of_scope"),
]


```

**File 3 of 8 — `dedup.py`.** The contamination scan. The student types it in the lesson (Part 3); the function `decontaminate` is typed from your copy, line by line, with the explanation of `&` and `|` first.

```python
# dedup.py - run this BEFORE training, every single time.
import re
from evalset import EVAL
from traindata import TRAIN_RAW


def words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def jaccard(a, b):
    A, B = words(a), words(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def decontaminate(train, evalset, threshold=0.70, verbose=True):
    clean, removed = [], []
    for i, (t, y) in enumerate(train):
        worst = max(((jaccard(t, e), j, e) for j, (e, _) in enumerate(evalset)), key=lambda x: x[0])
        if worst[0] >= threshold:
            removed.append((i, t, worst))
        else:
            clean.append((t, y))
    if verbose:
        print(f"contamination scan: {len(train)} train x {len(evalset)} eval")
        for i, t, (sim, j, e) in removed:
            kind = "EXACT" if sim >= 0.999 else "NEAR "
            print(f"  {kind} train#{i:<3d} {t!r}\n        eval#{j:<3d} {e!r}   Jaccard {sim:.3f}")
        print(f"  removed {len(removed)}, kept {len(clean)}")
    return clean, removed
```

**File 4 of 8 — `scorer.py`.** Handed over; read it together, do not type it. Exact match after tidying the answer, and a per-category breakdown.

```python
# scorer.py - exact match after normalising, plus a per-category breakdown.
import re
from evalset import EVAL, LABELS

SYNONYMS = {                        # plausible phrasings mapped onto the canonical labels
    "tech": "technical", "technical support": "technical", "support": "technical",
    "return": "refund", "returns": "refund", "refunds": "refund",
    "payment": "billing", "payments": "billing", "invoice": "billing",
    "greetings": "greeting", "hello": "greeting", "smalltalk": "greeting",
    "other": "out_of_scope", "off-topic": "out_of_scope", "none": "out_of_scope",
    "out of scope": "out_of_scope", "unrelated": "out_of_scope",
}


def normalise(pred):
    p = "".join(re.findall(r"[a-z_ -]", str(pred).lower())).strip()
    p = SYNONYMS.get(p, p)
    return p if p in LABELS else "UNPARSEABLE"


def score(preds, name="system"):
    """preds: a list of 30 raw predictions, in the same order as EVAL."""
    assert len(preds) == len(EVAL), "prediction count must match the frozen eval set"
    per = {cat: [0, 0] for cat in LABELS}           # category -> [correct, total]
    wrong = []
    for (text, gold), raw in zip(EVAL, preds):
        p = normalise(raw)
        per[gold][1] += 1
        if p == gold:
            per[gold][0] += 1
        else:
            wrong.append((text, gold, p))
    total_ok = sum(c for c, t in per.values())
    return {"name": name, "overall": total_ok / len(EVAL), "correct": total_ok, "n": len(EVAL),
            "per_category": {k: (c, t, c / t) for k, (c, t) in per.items()},
            "wrong": wrong}


def report(res):
    print(f"\n=== {res['name']} ===  overall {res['correct']}/{res['n']} = {res['overall']:.3f}")
    for cat in LABELS:
        c, t, a = res["per_category"][cat]
        print(f"  {cat:14s} {c}/{t}  {a:.3f}  {'#' * round(a * 20)}")
    for text, gold, pred in res["wrong"]:
        print(f"    x {text[:48]:50s} gold={gold:13s} pred={pred}")
```

**File 5 of 8 — `compare.py`.** Handed over; read the table it prints rather than the code. The per-category before/after table. Week 31 uses it unchanged.

```python
# compare.py - the table that tells the truth: an average, then every category.
from evalset import LABELS


def compare(before, after, min_n=5, drop_threshold=0.10):
    print(f"\n{'category':14s} {'n':>3s} {'before':>8s} {'after':>8s} {'delta':>8s}")
    print("-" * 46)
    regressions = []
    for cat in LABELS:
        cb, n, ab = before["per_category"][cat]
        ca, _, aa = after["per_category"][cat]
        d = aa - ab
        flag = ""
        if n >= min_n and d <= -drop_threshold:
            flag = "  <-- REGRESSION"
            regressions.append((cat, n, ab, aa, d))
        print(f"{cat:14s} {n:3d} {ab:8.3f} {aa:8.3f} {d:+8.3f}{flag}")
    print("-" * 46)
    d_all = after["overall"] - before["overall"]
    print(f"{'OVERALL':14s} {before['n']:3d} {before['overall']:8.3f} "
          f"{after['overall']:8.3f} {d_all:+8.3f}")

    print("\ncontribution of each category to the overall delta:")
    for cat in LABELS:
        cb, n, ab = before["per_category"][cat]
        _, _, aa = after["per_category"][cat]
        print(f"  {cat:14s} (n/N = {n}/{before['n']}) x {aa - ab:+.3f} = {n / before['n'] * (aa - ab):+.4f}")

    if regressions:
        print(f"\n{len(regressions)} REGRESSION(S) - do not ship on the average alone:")
        for cat, n, ab, aa, d in regressions:
            print(f"   {cat}: {ab:.3f} -> {aa:.3f} ({d:+.1%} on n={n})")
    else:
        print("\nno category with n>=5 dropped by more than 10 points")
    return regressions
```

**File 6 of 8 — `baselines.py`.** Handed over. Three cheap systems, none of them a model of language. **Read Key K7 before you hand it over:** the `RULES` list was written by the course author *with the eval set in view* (eight of its keys appear in eval tickets and in no training ticket), so `0.833` is a generous score for "free rules". Week 31 also compares against it. Mistake 12 shows the same thing done on purpose.

```python
# baselines.py - the cheap systems a fancier system must beat. None of them understands language.
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

RULES = [
    ("greeting",  ["hi", "hiya", "hello", "hey", "morning", "afternoon", "evening"]),
    ("refund",    ["refund", "return", "send them back", "send it back", "money back",
                   "reimburs", "postage"]),
    ("billing",   ["invoice", "plan", "paying", "charge", "card", "billing",
                   "subscription", "twice"]),
    ("technical", ["error", "crash", "blank", "csv", "loading", "sync", "closes",
                   "rendering", "nothing", "inbox"]),
]


def rules_predict(text):
    low = text.lower()
    for label, keys in RULES:
        if any(k in low for k in keys):
            return label
    return "out_of_scope"


def majority_predict(train):
    """The dumbest baseline: always answer the commonest training label."""
    return Counter(y for _, y in train).most_common(1)[0][0]


def tfidf_fit_predict(train, texts):
    """A small classifier trained from scratch on the training tickets. Week 25's TF-IDF plus Level 2's logistic regression."""
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    X = vec.fit_transform([t for t, _ in train])
    clf = LogisticRegression(max_iter=1000, C=10, random_state=0).fit(X, [y for _, y in train])
    return list(clf.predict(vec.transform(texts)))
```

**File 7 of 8 — `replies.py`.** Handed over. Thirty tickets, each with two candidate replies from two "bots" (`v1` the old one, `v2` the new one), **built from fixed templates by Python, not by any model**, plus a rubric that is a short function the student can read. The rubric is the answer key for the judge test: it says which reply is better, with no opinion in it.

```python
# replies.py - canned replies for the 30 eval tickets, and a rubric a program can apply. NOT written by a model.
from evalset import EVAL, LABELS

ROUTE = {"greeting": "a greeting", "refund": "a refund request", "technical": "a technical fault",
         "billing": "a billing question", "out_of_scope": "something outside this shop"}
PROMISES = ["within", "guarantee", "definitely"]
PROMISE = " It will definitely be fixed within 24 hours."
FILLER = " We really do appreciate you getting in touch with us today and we hope your week is going well."
V1_KINDS = ["good", "promise", "bad", "promise", "good", "bad"]      # the old bot, repeating every 6 tickets
V2_KINDS = ["promise", "good", "good", "good", "long", "long"]       # the new bot


def make_reply(label, kind):
    other = LABELS[(LABELS.index(label) + 1) % len(LABELS)]
    good = f"This looks like {ROUTE[label]}, so I am passing it on."
    wrong = f"This looks like {ROUTE[other]}, so I am passing it on."
    return {"good": good, "promise": good + PROMISE, "wrong": wrong,
            "bad": wrong + PROMISE, "long": good + FILLER}[kind]


def rubric(reply, label):
    """Three checks, one point each: short (25 words or fewer), names the right route, makes no promise."""
    short = len(reply.split()) <= 25
    routed = ROUTE[label] in reply
    no_promise = not any(p in reply.lower() for p in PROMISES)
    return int(short) + int(routed) + int(no_promise)


def make_pairs():
    """One (ticket, label, v1 reply, v2 reply) per eval ticket."""
    return [(text, label, make_reply(label, V1_KINDS[i % 6]), make_reply(label, V2_KINDS[i % 6]))
            for i, (text, label) in enumerate(EVAL)]
```

**File 8 of 8 — `mystery.py`.** Handed over **as a sealed file: the student is told not to open it until the end of Part 5.** It holds the scripted pairwise judge. The number `BIAS` is the planted flaw.

```python
# mystery.py - a SCRIPTED pairwise judge with a planted flaw. STAND-IN, NOT A MODEL: it reads a rubric score, not language.
from replies import rubric

BIAS = 0.5          # the planted flaw: how often it answers "A" without looking at the replies


def judge_pair(label, a, b, rng, bias=BIAS):
    """Answer "A" or "B". With chance `bias` it says "A" without looking; otherwise it compares rubric scores."""
    if rng.random() < bias:
        return "A"
    sa, sb = rubric(a, label), rubric(b, label)
    if sa == sb:
        return rng.choice(["A", "B"])
    return "A" if sa > sb else "B"
```


**Block P1 — the freeze and the first run.** Run from the folder that holds the eight files.

```python
# p1_check.py - Week 30 block P1: what is in the frozen set, its fingerprint, and one run of the scan.
from collections import Counter
from evalset import EVAL, LABELS, FROZEN, fingerprint
from traindata import TRAIN_RAW
from dedup import decontaminate

print("eval cases:", len(EVAL), " per label:", dict(Counter(y for _, y in EVAL)))
print("fingerprint:", fingerprint(EVAL))
print("same as the one written down at freeze time:", fingerprint(EVAL) == FROZEN)
print("raw training tickets:", len(TRAIN_RAW), " per label:", dict(Counter(y for _, y in TRAIN_RAW)))
TRAIN, removed = decontaminate(TRAIN_RAW, EVAL)
print("kept per label:", dict(Counter(y for _, y in TRAIN)))
```

```text
eval cases: 30  per label: {'greeting': 6, 'refund': 7, 'technical': 7, 'billing': 5, 'out_of_scope': 5}
fingerprint: 73b33debbc8d8c4241051bc5670ef4dd
same as the one written down at freeze time: True
raw training tickets: 66  per label: {'greeting': 14, 'refund': 15, 'technical': 14, 'billing': 15, 'out_of_scope': 8}
contamination scan: 66 train x 30 eval
  EXACT train#28  'is there a time limit on sending items back?'
        eval#8   'is there a time limit on sending items back?'   Jaccard 1.000
  NEAR  train#57  'what am I paying each month right now?'
        eval#23  'what am I paying per month right now?'   Jaccard 0.778
  removed 2, kept 64
kept per label: {'greeting': 14, 'refund': 14, 'technical': 14, 'billing': 14, 'out_of_scope': 8}
```

**Block P2 — the floor, the free rules, and a model trained from scratch.** Three systems scored on the same 30 tickets.

```python
# p2_baselines.py - Week 30 block P2: three cheap systems on the frozen eval.
from scorer import score, report
from baselines import rules_predict, majority_predict, tfidf_fit_predict

texts = [t for t, _ in EVAL]
answer = majority_predict(TRAIN)
r_floor = score([answer] * 30, f"always say {answer!r}")
r_rules = score([rules_predict(t) for t in texts], "keyword rules (free)")
r_tfidf = score(tfidf_fit_predict(TRAIN, texts), "TF-IDF + logistic regression")
for r in (r_floor, r_rules, r_tfidf):
    print(f"{r['name']:32s} {r['correct']:2d}/30 = {r['overall']:.3f}")
best_constant = max(Counter(y for _, y in EVAL).values())
print(f"best possible constant answer on this eval: {best_constant}/30 = {best_constant / 30:.3f}")
report(r_rules)
```

```text
always say 'greeting'             6/30 = 0.200
keyword rules (free)             25/30 = 0.833
TF-IDF + logistic regression     21/30 = 0.700
best possible constant answer on this eval: 7/30 = 0.233

=== keyword rules (free) ===  overall 25/30 = 0.833
  greeting       6/6  1.000  ####################
  refund         5/7  0.714  ##############
  technical      4/7  0.571  ###########
  billing        5/5  1.000  ####################
  out_of_scope   5/5  1.000  ####################
    x is there a time limit on sending items back?       gold=refund        pred=out_of_scope
    x do I pay postage to return something?              gold=refund        pred=greeting
    x clicking save does absolutely nothing              gold=technical     pred=greeting
    x everything is blank after I sign in                gold=technical     pred=greeting
    x charts stopped rendering yesterday afternoon       gold=technical     pred=greeting
```

**Block P3 — the overlap number, by hand first.** `&` and `|` on two sets, then the function.

```python
# p3_jaccard.py - Week 30 block P3: Jaccard overlap, worked on the near-copy the scan found.
from dedup import words, jaccard

a = "what am I paying each month right now?"          # a training ticket
b = "what am I paying per month right now?"           # an eval ticket
A, B = words(a), words(b)
print("A:", sorted(A))
print("B:", sorted(B))
print("in both (A & B):", sorted(A & B), "->", len(A & B))
print("in either (A | B):", sorted(A | B), "->", len(A | B))
print(f"Jaccard = {len(A & B)}/{len(A | B)} = {len(A & B) / len(A | B):.3f}  (function says {jaccard(a, b):.3f})")
print("two tickets about the same thing, worded apart:",
      f"{jaccard('could you tell me my current monthly charge?', b):.3f}")
```

```text
A: ['am', 'each', 'i', 'month', 'now', 'paying', 'right', 'what']
B: ['am', 'i', 'month', 'now', 'paying', 'per', 'right', 'what']
in both (A & B): ['am', 'i', 'month', 'now', 'paying', 'right', 'what'] -> 7
in either (A | B): ['am', 'each', 'i', 'month', 'now', 'paying', 'per', 'right', 'what'] -> 9
Jaccard = 7/9 = 0.778  (function says 0.778)
two tickets about the same thing, worded apart: 0.000
```

**Block P4 — what the scan protected, and what it cannot see.**

```python
# p4_leak.py - Week 30 block P4: score the same classifier with and without the scan, then with five paraphrases the scan misses.
SNEAKY = [
    ("how many days do I have to post an unwanted product?",      "refund"),      # eval#8
    ("could you tell me my current monthly charge?",              "billing"),     # eval#23
    ("pressing the save button has no effect whatsoever",         "technical"),   # eval#13
    ("what is the elevation of Africa's highest peak?",           "out_of_scope"),# eval#26
    ("you debited my account two times earlier this month",       "billing"),     # eval#20
]
r_raw = score(tfidf_fit_predict(TRAIN_RAW, texts), "trained on all 66 (no scan)")
r_sneaky = score(tfidf_fit_predict(TRAIN + SNEAKY, texts), "trained on 64 + 5 paraphrases")
for r in (r_tfidf, r_raw, r_sneaky):
    print(f"{r['name']:32s} {r['correct']:2d}/30 = {r['overall']:.3f}")
_, caught = decontaminate(TRAIN + SNEAKY, EVAL, verbose=False)
print("paraphrases the scan caught:", len(caught))
for t, _ in SNEAKY:
    best = max(jaccard(t, e) for e, _ in EVAL)
    print(f"  highest Jaccard against any eval ticket: {best:.3f}   {t[:46]}")
```

```text
TF-IDF + logistic regression     21/30 = 0.700
trained on all 66 (no scan)      22/30 = 0.733
trained on 64 + 5 paraphrases    23/30 = 0.767
paraphrases the scan caught: 0
  highest Jaccard against any eval ticket: 0.200   how many days do I have to post an unwanted pr
  highest Jaccard against any eval ticket: 0.083   could you tell me my current monthly charge?
  highest Jaccard against any eval ticket: 0.143   pressing the save button has no effect whatsoe
  highest Jaccard against any eval ticket: 0.143   what is the elevation of Africa's highest peak
  highest Jaccard against any eval ticket: 0.077   you debited my account two times earlier this 
```

**Block P5 — the replies and the rubric.** Read three pairs aloud, then count how the rubric sorts all thirty.

```python
# p5_pairs.py - Week 30 block P5: 30 pairs of canned replies, and what the rubric says about them.
from replies import make_pairs, rubric

pairs = make_pairs()
for text, label, r1, r2 in pairs[:3]:
    print(f"ticket: {text!r} (gold {label})")
    print(f"  v1 [{rubric(r1, label)}/3] {r1}")
    print(f"  v2 [{rubric(r2, label)}/3] {r2}")
v1_better = sum(rubric(r1, l) > rubric(r2, l) for _, l, r1, r2 in pairs)
v2_better = sum(rubric(r1, l) < rubric(r2, l) for _, l, r1, r2 in pairs)
print("rubric says: v1 better in", v1_better, "pairs, v2 better in", v2_better, "pairs, tied in", 30 - v1_better - v2_better)
```

```text
ticket: 'hey! quick one for you' (gold greeting)
  v1 [3/3] This looks like a greeting, so I am passing it on.
  v2 [2/3] This looks like a greeting, so I am passing it on. It will definitely be fixed within 24 hours.
ticket: 'good afternoon, are you there?' (gold greeting)
  v1 [2/3] This looks like a greeting, so I am passing it on. It will definitely be fixed within 24 hours.
  v2 [3/3] This looks like a greeting, so I am passing it on.
ticket: 'hiya' (gold greeting)
  v1 [1/3] This looks like a refund request, so I am passing it on. It will definitely be fixed within 24 hours.
  v2 [3/3] This looks like a greeting, so I am passing it on.
rubric says: v1 better in 10 pairs, v2 better in 20 pairs, tied in 0
```

**Block P6 — kappa on 20 ratings: the table, the tally, the arithmetic by hand, then the library.** Rater **H** is the strict reader (passes a reply only if it gets 3 of 3); rater **J** is a lenient scripted judge (passes at 2 of 3). **Both are programs; neither is a model of language.**

```python
# p6_kappa.py - Week 30 block P6: Cohen's kappa, by hand first and then with the library.
items = [(text, label, r1) for text, label, r1, r2 in pairs[:20]]      # the old bot's reply to tickets 0-19
H = [1 if rubric(r, l) == 3 else 0 for _, l, r in items]               # strict: pass only with 3 of 3
J = [1 if rubric(r, l) >= 2 else 0 for _, l, r in items]               # lenient: pass with 2 of 3
print(" #  score  H  J   ticket")
for i, ((text, l, r), h, j) in enumerate(zip(items, H, J)):
    print(f"{i:2d}    {rubric(r, l)}    {h}  {j}   {text[:40]}")

both_pass = sum(h == 1 and j == 1 for h, j in zip(H, J))
j_pass_h_fail = sum(h == 0 and j == 1 for h, j in zip(H, J))
j_fail_h_pass = sum(h == 1 and j == 0 for h, j in zip(H, J))
both_fail = sum(h == 0 and j == 0 for h, j in zip(H, J))
print("\nboth pass", both_pass, "| J pass, H fail", j_pass_h_fail, "| J fail, H pass", j_fail_h_pass, "| both fail", both_fail)

n = 20
p_o = (both_pass + both_fail) / n                       # how often they agree
j_rate = (both_pass + j_pass_h_fail) / n                # how often J says pass
h_rate = (both_pass + j_fail_h_pass) / n                # how often H says pass
p_e = j_rate * h_rate + (1 - j_rate) * (1 - h_rate)     # how often they would agree by luck
kappa = (p_o - p_e) / (1 - p_e)
print(f"p_o = {p_o:.4f}   J passes {j_rate:.2f}, H passes {h_rate:.2f}   p_e = {p_e:.4f}")
print(f"kappa = ({p_o:.4f} - {p_e:.4f}) / (1 - {p_e:.4f}) = {kappa:.4f}")

from sklearn.metrics import cohen_kappa_score
print("library says:", round(cohen_kappa_score(H, J), 4))
```

```text
 #  score  H  J   ticket
 0    3    1  1   hey! quick one for you
 1    2    0  1   good afternoon, are you there?
 2    1    0  0   hiya
 3    2    0  1   hello - first time using this
 4    3    1  1   morning, got a sec?
 5    1    0  0   hi, hope this is the right place
 6    3    1  1   these shoes are the wrong colour, how do
 7    2    0  1   I'd like my money returned for order 553
 8    1    0  0   is there a time limit on sending items b
 9    2    0  1   package never arrived, I want reimbursin
10    3    1  1   do I pay postage to return something?
11    1    0  0   cancel order 7781 and put the money back
12    3    1  1   opened it, hated it - can I still send i
13    2    0  1   clicking save does absolutely nothing
14    1    0  0   everything is blank after I sign in
15    2    0  1   the android version force closes on laun
16    3    1  1   my csv download has headers but no rows
17    1    0  0   reset email never turns up in my inbox
18    3    1  1   charts stopped rendering yesterday after
19    2    0  1   keeps saying 'network error' on a perfec

both pass 7 | J pass, H fail 7 | J fail, H pass 0 | both fail 6
p_o = 0.6500   J passes 0.70, H passes 0.35   p_e = 0.4400
kappa = (0.6500 - 0.4400) / (1 - 0.4400) = 0.3750
library says: 0.375
```

**Block P7 — why not just report agreement.** A judge that says "pass" every time, on a set where almost everything passes.

```python
# p7_constant.py - Week 30 block P7: a judge that never looks, on a lopsided set.
H2 = [1] * 18 + [0] * 2                 # the human passes 18 of 20
Z = [1] * 20                            # the judge says pass to everything
agree = sum(h == z for h, z in zip(H2, Z)) / 20
print("raw agreement:", agree, "  kappa:", round(cohen_kappa_score(H2, Z), 4))
print("our lenient J against strict H:  raw agreement", p_o, "  kappa", round(cohen_kappa_score(H, J), 4))
```

```text
raw agreement: 0.9   kappa: 0.0
our lenient J against strict H:  raw agreement 0.65   kappa 0.375
```

**Block P8 — the mystery judge: run every comparison in both orders.** The student has not opened `mystery.py`.

```python
# p8_bias.py - Week 30 block P8: ask a pairwise judge each question twice, in both orders, and count what changes.
import random
from mystery import judge_pair


def bias_test(pairs, seed):
    rng = random.Random(seed)                  # ONE generator for the whole test (Mistake 10)
    first_wins = flips = v1_cons = v2_cons = naive_v1 = 0
    for text, label, r1, r2 in pairs:
        fwd = judge_pair(label, r1, r2, rng)   # v1 shown first (position A)
        rev = judge_pair(label, r2, r1, rng)   # v2 shown first
        naive_v1 += fwd == "A"
        first_wins += (fwd == "A") + (rev == "A")
        w_fwd = "v1" if fwd == "A" else "v2"
        w_rev = "v2" if rev == "A" else "v1"
        if w_fwd != w_rev:
            flips += 1
        elif w_fwd == "v1":
            v1_cons += 1
        else:
            v2_cons += 1
    return {"n": len(pairs), "first_wins": first_wins, "flips": flips, "v1_cons": v1_cons,
            "v2_cons": v2_cons, "naive_v1": naive_v1}


t = bias_test(pairs, 0)
n = t["n"]
print(f"first-position wins: {t['first_wins']}/{2 * n} = {t['first_wins'] / (2 * n):.3f}   (a judge with no position habit: 0.500)")
print(f"flips when the order is swapped: {t['flips']}/{n} = {t['flips'] / n:.3f}")
print(f"naive, v1 shown first only: v1 wins {t['naive_v1']}/{n} = {t['naive_v1'] / n:.3f}")
c = t["v1_cons"] + t["v2_cons"]
print(f"consistent pairs only: {c} pairs, v1 {t['v1_cons']}, v2 {t['v2_cons']}  ->  v1 wins {t['v1_cons'] / c:.3f}")
print(f"the rubric says v1 is better in {v1_better} of {n} = {v1_better / n:.3f}")
print(f"estimate of the planted bias (the flip rate): {t['flips'] / n:.3f}")
```

```text
first-position wins: 38/60 = 0.633   (a judge with no position habit: 0.500)
flips when the order is swapped: 8/30 = 0.267
naive, v1 shown first only: v1 wins 16/30 = 0.533
consistent pairs only: 22 pairs, v1 8, v2 14  ->  v1 wins 0.364
the rubric says v1 is better in 10 of 30 = 0.333
estimate of the planted bias (the flip rate): 0.267
```

**Block P9 — one run is one draw: thirty pairs, twenty seeds, then the sealed file.**

```python
# p9_seeds.py - Week 30 block P9: repeat the whole test with 20 different seeds, then open the sealed file.
import numpy as np
import mystery

est = [bias_test(pairs, s)["flips"] / 30 for s in range(20)]
print("20 estimates of the bias:", [round(e, 2) for e in est])
print(f"smallest {min(est):.2f}  largest {max(est):.2f}  average {np.mean(est):.3f}")
naive = [bias_test(pairs, s)["naive_v1"] for s in range(20)]
print("v1 'wins' in the naive run, out of 30, on each seed:", naive)
print(f"the sealed file says BIAS = {mystery.BIAS}")
```

```text
20 estimates of the bias: [0.27, 0.47, 0.4, 0.37, 0.4, 0.47, 0.47, 0.57, 0.6, 0.67, 0.4, 0.37, 0.5, 0.6, 0.37, 0.43, 0.7, 0.47, 0.5, 0.5]
smallest 0.27  largest 0.70  average 0.475
v1 'wins' in the naive run, out of 30, on each seed: [16, 19, 18, 15, 16, 19, 20, 20, 25, 23, 17, 18, 20, 22, 18, 17, 22, 20, 20, 21]
the sealed file says BIAS = 0.5
```

**Block P10 — the table that goes in the report: rules against the trained model, category by category.**

```python
# p10_compare.py - Week 30 block P10: Week 31's table, with Week 30's two baselines.
from compare import compare

compare(r_rules, r_tfidf)
```

```text

category         n   before    after    delta
----------------------------------------------
greeting         6    1.000    0.833   -0.167  <-- REGRESSION
refund           7    0.714    0.857   +0.143
technical        7    0.571    0.714   +0.143
billing          5    1.000    0.800   -0.200  <-- REGRESSION
out_of_scope     5    1.000    0.200   -0.800  <-- REGRESSION
----------------------------------------------
OVERALL         30    0.833    0.700   -0.133

contribution of each category to the overall delta:
  greeting       (n/N = 6/30) x -0.167 = -0.0333
  refund         (n/N = 7/30) x +0.143 = +0.0333
  technical      (n/N = 7/30) x +0.143 = +0.0333
  billing        (n/N = 5/30) x -0.200 = -0.0333
  out_of_scope   (n/N = 5/30) x -0.800 = -0.1333

3 REGRESSION(S) - do not ship on the average alone:
   greeting: 1.000 -> 0.833 (-16.7% on n=6)
   billing: 1.000 -> 0.800 (-20.0% on n=5)
   out_of_scope: 1.000 -> 0.200 (-80.0% on n=5)
```


### 3 minutes on the day

Start Python in the lesson folder and run Block P1 to be sure the eight files import. Confirm that `mystery.py` is not open on the student's screen and that the student's own `evalset.py` has **not yet** got a `FROZEN` value in it (they will add it in Part 1). Print **Pages 30.1-30.3**. Keep Key K4's table (pairs 11-20) within reach: it is Page 30.3's answer.

### Fallback if the laptops fail

The lesson is an argument, and the pages carry it on paper: the Jaccard of three pairs by hand (Page 30.1), the kappa of twenty printed ratings (Page 30.2), the flips in ten printed pairs (Page 30.3). If the laptop is dead, read the baseline table and the bias summary off this guide. If a block takes more than a minute, something is wrong: the usual cause is running from the wrong folder (an `ImportError` at once, not a slow run), a `FROZEN` value that does not match (an `AssertionError` on import), or a stray `time.sleep` from Week 29 pasted into the session.

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Clock | What happens |
|---|:--:|:--:|---|
| 🪝 Hook — A Score With No Context | 6 | 0:00-0:06 | "The bot scores 90 percent." Three questions. The report card nobody can check. |
| 🧠 Concept — The Instrument Before the Thing | 10 | 0:06-0:16 | Freeze first; baseline first; keep the eval out of training; a judge is an instrument; luck and kappa. |
| 🎲 Their Turn — Overlap and Agreement on Paper | 12 | 0:16-0:28 | Pen: Page 30.1 (Jaccard by hand, three pairs; a threshold) and Page 30.2 (kappa on 20 ratings). |
| 💻 Live-Code Together — `eval_suite.py` | 36 | 0:28-1:04 | Freeze; baselines; the scan and a leak it misses; replies and kappa with the library as a check; the sealed judge. |
| 🔑 Wrap & Assign | 6 | 1:04-1:10 | The sentence; what was and was not shown; homework; Week 31. |

### 🪝 Hook — A Score With No Context (6 minutes)

Write on the board: **"Our new bot scores 90 percent."** *"Would you ship it?"* Let them say yes, then ask the three questions and write each answer slot on the board: **"90 percent of what?"** (which tickets, how many, in which categories) · **"Compared with what?"** (a bot that always says one thing? a list of ten keywords?) · **"Who marked it?"** (the team that built it? a program? another model?). Then: *"Every one of these has a way to be quietly wrong, and the person who built the bot has every reason not to look. Today we build the thing that does the looking, before we build anything for it to look at."* Do **not** show a number yet. End with the honesty rule: *"There is no language model in this room today. There is a judge, but it is a script I wrote, and it has a flaw I have hidden on purpose."*

### 🧠 Concept — The Instrument Before the Thing (10 minutes)

1. **Freeze first (2 min).** *"An eval written after you have seen the outputs is written to make them look good."* Hold up a stapler: *"The fingerprint is a staple through the 30 tickets. If anyone changes a word, the staple pops."* Say what it does *not* do: it does not stop anyone editing, it makes editing **loud**.
2. **Baseline first (3 min).** Draw three rungs: **floor** (always say one thing), **free rules** (ten keywords and ten minutes), **trained** (a small model). *"A fancy system has to beat the rung below it, not the floor."* Ask: *"If the floor scores 20 percent, is 70 percent good?"* (Not until you know the rules score 83.) Do not give the numbers yet.
3. **Keep the test out of the lessons (2 min).** *"What happens if the exam questions are in the textbook?"* Draw two circles, TRAIN and EVAL; the overlap is contamination. *"The scan counts shared words. A copy shares all of them. A reworded question shares almost none."*
4. **A judge is an instrument (3 min).** When answers are sentences, something has to mark them: a program with a rubric, a person, or another model, which is called a **judge**. *"If the judge is a ruler, check the ruler."* Two checks: **do two raters agree beyond luck?** (kappa) and **does the judge change its answer when I only swap the order?** (position habit). Put the two raters' grid on the board (Section 2's `7 7 / 0 6`) and leave the arithmetic for the pen pages.

### 🎲 Their Turn — Overlap and Agreement on Paper (12 minutes)

Hand over the printed sheet (see **The Activity, In Full**). 6 minutes for Page 30.1: the Jaccard of three pairs of tickets as sets (a1-a3), the removal decision at two thresholds (b), one paraphrase against its eval ticket (c) and the rule-key question (d). 6 minutes for the start of Page 30.2: tally the 20 ratings into the 2 by 2 grid and compute `p_o` and the two pass rates; the rest, `p_e` and `κ`, finishes after the code. Sit back. At the end ask: *"Which of your three pairs is a near-copy, and which two are different questions that happen to share words?"* (a2 is the near-copy; a1 and a3 are different questions.) *"What would a threshold of 0.5 do to the one that is just about the same subject?"* (Remove it: a harmless loss of a training ticket. Thresholds trade copies caught against tickets lost.) Do not run the code for this.

### 💻 Live-Code Together — `eval_suite.py` (36 minutes)

The student types; you narrate. Blocks go in **one file**, `eval_suite.py`, in the order of P1-P10; the file blocks are saved as their own files first. Narration cues:

**Part 1 (7 min) — the freeze.** The student types the first eight tickets of `evalset.py` from the printed sheet and pastes the rest from your copy. Type `fingerprint`; run `print(fingerprint(EVAL))`; paste the 32 characters into `FROZEN` and add the two `assert`s. Then run P1. Read the per-label counts aloud (`6 7 7 5 5`) and ask *"which category can we say the least about?"* (billing, out_of_scope: five tickets each; one ticket is `0.2` there.) Point at the `EXACT` and `NEAR` lines of the scan: *"we have not written the scan yet; it came from the file I gave you, and we will read it in Part 3."* **Mistake 1 fits here** (one character; the staple pops).

**Part 2 (7 min) — three rungs.** Read `scorer.py` together (not typed). Run P2 with the three systems **after** the student predicts the order of the three scores on a sticky note. Then: *"the trained one scored `0.700`, the free rules `0.833`."* Let the silence sit. Ask *"which category does the gap come from?"* and run P10's `compare`: `out_of_scope` `1.000 → 0.200`. *"Why is the rules' out_of_scope perfect?"* (Because "out_of_scope" is what the rules say when nothing else fits: it is the default.) Read the five misses of the rules aloud (`"hi"` inside `nothing`). **Mistake 12 is for the homework slot**; do not run it here.

**Part 3 (8 min) — overlap and the leak.** The student types `words`, `jaccard` and `decontaminate` from your copy after P3's two sets are on the board. Run P3 (`7/9 = 0.778`, and `0.000` for the paraphrase). Run P4: *"the exact copy was worth one ticket (`22` against `21`); five rewordings were worth two more (`23`), and the scan saw none of them."* Ask: *"so is 23 better than 21?"* (No: it measures memory of the paraphrases.) **Mistake 4 and Mistake 5 fit here.**

**Part 4 (8 min) — replies and kappa.** Run P5 (three pairs read aloud; the rubric's own counts `10` and `20`). Then P6 with the hand calculation already on Page 30.2: the student types only the `cohen_kappa_score` line. Check `0.375` against the page. Run P7 (`0.9` and `0.0`). Ask: *"would you trust a judge that agrees with you 90 percent of the time?"* (Not before asking what it says to the easy cases.) **Mistake 7 fits here.**

**Part 5 (6 min) — the sealed judge.** Say: *"this file (`mystery.py`) holds a judge with a flaw. We do not open it. We ask it each question twice."* The student types `bias_test` (you narrate the two `judge_pair` calls: v1 first, then v2 first). Run it: `38` of `60`, `8` flips. **Ask them to say, before you tell them, what a judge with no habit would give for first-position wins** (30, i.e. `0.500`). Then the naive line (`v1 wins 16 of 30`) against the rubric (`10`), and the consistent pairs (`22`). Run P9 and show the twenty estimates (`0.27` to `0.70`): *"one run is one draw."* Open `mystery.py` last and read `BIAS = 0.5`. If time is short, show the P9 output printed and skip the second run. **Mistake 10 is the one to show if there is a minute.**

### 🔑 Wrap & Assign (6 minutes)

1. **One sentence each (3 min).** Ask for a sentence that says what the new instrument did. A good one: *"The eval was fixed before the model; the free rules beat the trained model; my judge changed its mind when I swapped the order, so I don't trust a single run."* A shaky one: "the judge was biased" (biased how, found how, how sure?).
2. **Say what was and was not shown (1 min).** *"We did not test a real judge. The flip rate is a fact about the number I typed. What we showed is a method: freeze, baseline, scan, kappa, swap. The rules being good was a fact about my rules."*
3. **Homework (1 min):** the three tasks below.
4. **Tease Week 31 (1 min):** *"Next week we build something to put under this ruler: a tiny model that read a pile of sentences once, fine-tuned on 64 tickets two ways. The average will go up by one ticket. We'll see what the table says."*

---

## 🐞 The Debugging Clinic

### How to teach debugging without giving the answer

Every error below was produced by running the code. **Paths will differ on your machine**; here they are shown as `/home/you/l4/` (the student's files) and `/usr/lib/python3.10/...` (library files). Each mistake is deliberate: you plant it, the student reads the traceback (or the surprising output) aloud, and you refuse to fix it until they have said what it means. **Eight are silent** (2, 3, 4, 7, 8, 10, 11, 12): the program runs and prints something plausible. Those are the dangerous ones. Four are loud (1, 5, 6, 9). Each block assumes the Prep blocks above were run in the same session, in order, and **a loud block stops the rest of its own block**, nothing else. Use the four questions: *What did the computer do? What did you ask it to do? Where do those two differ? What is the smallest change that closes the gap?* **Nothing here needs any text aimed at a real system: every attack-shaped thing today (the paraphrases in P4) is a reworded support ticket, run against a 64-ticket classifier on the student's own machine.**

### Mistake 1 — "the wording was unfair, so I fixed one ticket" (loud)

```python
# DELIBERATE MISTAKE 1 (loud): edit one frozen ticket "to be fair". The fingerprint written at freeze time notices.
edited = list(EVAL)
edited[2] = ("hiya!", "greeting")                        # ticket 2 was "hiya"; one character added
print("fingerprint of the edited set:", fingerprint(edited))
print("fingerprint written at freeze time:", FROZEN)
assert fingerprint(edited) == FROZEN, "the frozen eval set was edited"
```

```text
fingerprint of the edited set: e631aa8f7f9650e1a38f1510c8c6fdb3
fingerprint written at freeze time: 73b33debbc8d8c4241051bc5670ef4dd
Traceback (most recent call last):
  File "/home/you/l4/M1.py", line 6, in <module>
    assert fingerprint(edited) == FROZEN, "the frozen eval set was edited"
AssertionError: the frozen eval set was edited
```

**Read it:** `fingerprint(edited)` is `e631aa8f…`, not `73b33deb…`: adding one `!` to one ticket changed the whole 32-character fingerprint. The assertion fires with the message we wrote. The same assertion sits at the bottom of `evalset.py`, so **importing the file is enough to trip it**: nobody can run a score against an edited eval without seeing the message. **Fix:** do not edit the frozen ticket. If the wording was genuinely unfair, **add a new ticket to a new file** and leave the old one failing with a note (the Capstone's Milestone 2 says exactly this). **Say:** *"a frozen set you can edit is a set you will edit."*

### Mistake 2 — scoring the model on the tickets it learned from (SILENT)

```python
# DELIBERATE MISTAKE 2 (SILENT): score the model on its own training tickets. It will look superb.
train_texts = [t for t, _ in TRAIN]
guess = tfidf_fit_predict(TRAIN, train_texts)
right = sum(g == y for g, (_, y) in zip(guess, TRAIN))
print(f"'accuracy' on the 64 training tickets: {right}/{len(TRAIN)} = {right / len(TRAIN):.3f}")
print(f"accuracy on the frozen eval:           {r_tfidf['correct']}/30 = {r_tfidf['overall']:.3f}")
```

```text
'accuracy' on the 64 training tickets: 64/64 = 1.000
accuracy on the frozen eval:           21/30 = 0.700
```

**Read it:** the trained classifier is right on `64/64` of the tickets it was trained on and `21/30` on the frozen eval. Both numbers are honest; only one is a test. A model that has seen the answers scores well on them whatever it has learned. **Fix:** score only on tickets the model never trained on. **Say:** *"the training score tells me the model can remember; the eval tells me whether that is useful."* (This is Week 5's memorising, with a 64-ticket set.)

### Mistake 3 — skipping the scan, and liking the result (SILENT)

```python
# DELIBERATE MISTAKE 3 (SILENT): "22 is better than 21, so I will not run the scan." Which ticket made the difference?
before = {text for text, gold, pred in r_tfidf["wrong"]}
after = {text for text, gold, pred in r_raw["wrong"]}
print("scored 21/30 with the scan, 22/30 without it.")
print("wrong WITH the scan but right without it:", sorted(before - after))
print("wrong without the scan but right with it:", sorted(after - before))
print("the 'extra' ticket is the one whose exact copy sat in the training set:",
      ("is there a time limit on sending items back?", "refund") in TRAIN_RAW)
```

```text
scored 21/30 with the scan, 22/30 without it.
wrong WITH the scan but right without it: ['is there a time limit on sending items back?']
wrong without the scan but right with it: []
the 'extra' ticket is the one whose exact copy sat in the training set: True
```

**Read it:** the extra ticket is `'is there a time limit on sending items back?'`. Its exact copy sat in the training set with the label `refund`, so the classifier that saw it got it right, and the one that did not (the honest one) got it wrong. One ticket, `+0.033`. Nothing was learned; something was remembered. **Fix:** always run the scan, and report the score of the model trained on the *scanned* set. **Say:** *"the extra point was the exam question being in the textbook."*

### Mistake 4 — a threshold that only catches exact copies (SILENT)

```python
# DELIBERATE MISTAKE 4 (SILENT): threshold 0.95 removes the exact copy and leaves the near-copy. Nothing complains.
for threshold in (0.70, 0.95):
    kept, gone = decontaminate(TRAIN_RAW, EVAL, threshold=threshold, verbose=False)
    print(f"threshold {threshold:.2f}: removed {len(gone)}, kept {len(kept)}", [t for _, t, _ in gone])
```

```text
threshold 0.70: removed 2, kept 64 ['is there a time limit on sending items back?', 'what am I paying each month right now?']
threshold 0.95: removed 1, kept 65 ['is there a time limit on sending items back?']
```

**Read it:** at `0.95` only the exact copy goes, and the near-copy `'what am I paying each month right now?'` (`0.778`, one word different from an eval ticket) stays in. No error, no warning: a scan that *looks* like it ran. **Fix:** pick the threshold on purpose, look at what it removes (`verbose=True` prints each one), and expect it to be a dial (Key K1: `0.30` removes seven tickets and `0.50` removes a harmless one as well). **Say:** *"the threshold is a decision, not a default."*

### Mistake 5 — overlap on lists instead of sets (loud)

```python
# DELIBERATE MISTAKE 5 (loud): & and | are set operations. On lists they are not defined.
A = "what am I paying each month".lower().split()
B = "what am I paying per month".lower().split()
print(len(A & B) / len(A | B))
```

```text
Traceback (most recent call last):
  File "/home/you/l4/M5.py", line 4, in <module>
    print(len(A & B) / len(A | B))
TypeError: unsupported operand type(s) for &: 'list' and 'list'
```

**Read it:** `A` and `B` are lists (`.split()` returns a list), and `&`, `|` mean set operations. The error names both types: `'list' and 'list'`. **Fix:** `set(A) & set(B)`, or build the sets with `words`. (Note what `.split()` would have got wrong anyway: `'month?'` with its question mark is a different word from `'month'`. That is why `words` uses `re.findall`.) **Say:** *"a list keeps order and repeats; a set keeps only who is in it."*

### Mistake 6 — a ticket with no letters in it (loud)

```python
# DELIBERATE MISTAKE 6 (loud): the same formula without the guard. A ticket made only of an emoji has no words.
def jaccard_unguarded(a, b):
    A, B = words(a), words(b)
    return len(A & B) / len(A | B)


print(jaccard_unguarded("where is my order", "where is my parcel"))
print(jaccard_unguarded("\U0001F44D", "\U0001F44C"))
```

```text
0.6
Traceback (most recent call last):
  File "/home/you/l4/M6.py", line 8, in <module>
    print(jaccard_unguarded("\U0001F44D", "\U0001F44C"))
  File "/home/you/l4/M6.py", line 4, in jaccard_unguarded
    return len(A & B) / len(A | B)
ZeroDivisionError: division by zero
```

**Read it:** the first call works (`3 / 5 = 0.6`). A ticket that is only an emoji has **no** letters or digits, so `words` returns an empty set for both, the union has size zero and we divide by zero. The traceback points at the division. **Fix:** the guard in `jaccard`: `if (A | B) else 0.0`. (The guarded version calls two emoji tickets "no overlap", which is wrong in spirit and harmless here; mention it if the student is curious.) **Say:** *"before you divide, ask what happens when the bottom is empty."*

### Mistake 7 — reading kappa and not the direction (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): "kappa 0.375, so the judge is sometimes right, sometimes wrong, about equally." Look at the off-diagonal.
print("kappa:", round(cohen_kappa_score(H, J), 3))
print("judge passes a reply the human fails:", j_pass_h_fail, "times")
print("judge fails a reply the human passes:", j_fail_h_pass, "times")
```

```text
kappa: 0.375
judge passes a reply the human fails: 7 times
judge fails a reply the human passes: 0 times
```

**Read it:** `κ = 0.375` is "fair", but the two cells it hides are `7` and `0`. The judge is not wrong in both directions equally: it **never** fails what the human passes and passes seven replies the human fails. It is **lenient**, and lenient in the direction that makes your system look good. **Fix:** always print the off-diagonal cells beside the kappa. **Say:** *"kappa tells me how far; the two cells tell me which way."*

### Mistake 8 — trusting the single-order verdict (SILENT)

```python
# DELIBERATE MISTAKE 8 (SILENT): run the pairwise judge once, with v1 shown first, and read the winner.
said_v1 = [bias_test(pairs, s)["naive_v1"] for s in range(20)]
print("seeds where a single-order run says 'v1 is better' (more than 15 of 30):", sum(x > 15 for x in said_v1), "of 20")
print("what the rubric says: v1 better in", v1_better, "of 30; v2 better in", v2_better)
```

```text
seeds where a single-order run says 'v1 is better' (more than 15 of 30): 19 of 20
what the rubric says: v1 better in 10 of 30; v2 better in 20
```

**Read it:** on `19` of `20` seeds a single-order run (v1 shown first) says v1 wins more than half of the pairs, while the rubric says v1 is better in only `10` of `30`. The judge's habit of saying "A" turns a loss for v1 into a win. There is no error and the number looks like a result. **Fix:** ask every question twice in both orders and report the pairs where the judge agreed with itself (Block P8: `22` pairs, v1 `8`, v2 `14`). **Say:** *"a single order measures the position as much as the replies."*

### Mistake 9 — two lists of different lengths (loud)

```python
# DELIBERATE MISTAKE 9 (loud): the judge's list lost its last rating (a loop that stopped one early).
print(cohen_kappa_score(H, J[:19]))
```

```text
Traceback (most recent call last):
  File "/home/you/l4/M9.py", line 2, in <module>
    print(cohen_kappa_score(H, J[:19]))
  File "/usr/lib/python3.10/site-packages/sklearn/utils/_param_validation.py", line 218, in wrapper
    return func(*args, **kwargs)
  File "/usr/lib/python3.10/site-packages/sklearn/metrics/_classification.py", line 870, in cohen_kappa_score
    confusion = confusion_matrix(y1, y2, labels=labels, sample_weight=sample_weight)
  File "/usr/lib/python3.10/site-packages/sklearn/utils/_param_validation.py", line 191, in wrapper
    return func(*args, **kwargs)
  File "/usr/lib/python3.10/site-packages/sklearn/metrics/_classification.py", line 467, in confusion_matrix
    y_type, y_true, y_pred = _check_targets(y_true, y_pred)
  File "/usr/lib/python3.10/site-packages/sklearn/metrics/_classification.py", line 97, in _check_targets
    check_consistent_length(y_true, y_pred)
  File "/usr/lib/python3.10/site-packages/sklearn/utils/validation.py", line 473, in check_consistent_length
    raise ValueError(
ValueError: Found input variables with inconsistent numbers of samples: [20, 19]
```

**Read it:** the traceback runs through scikit-learn's own files and ends on the line that matters: `inconsistent numbers of samples: [20, 19]`. The lists are different lengths (`J[:19]` has one fewer), so the pairs do not line up. **Fix:** check `len(H) == len(J)` before scoring, and find out why one list is short (an off-by-one in a loop, a filtered row). **Say:** *"read the last line of a long traceback first."*

### Mistake 10 — a fresh generator for every call (SILENT)

```python
# DELIBERATE MISTAKE 10 (SILENT): a brand-new random.Random(0) inside the loop. Every call makes the same draw.
def bias_test_fresh(pairs):
    first_wins = flips = 0
    for text, label, r1, r2 in pairs:
        fwd = judge_pair(label, r1, r2, random.Random(0))
        rev = judge_pair(label, r2, r1, random.Random(0))
        first_wins += (fwd == "A") + (rev == "A")
        flips += (fwd == "A") == (rev == "A")
    return first_wins, flips


fw, fl = bias_test_fresh(pairs)
print(f"first-position wins {fw}/60, flips {fl}/30  ->  'no position bias found'")
print("the first number random.Random(0).random() gives:", round(random.Random(0).random(), 4), "(above 0.5, so the judge always looks)")
```

```text
first-position wins 30/60, flips 0/30  ->  'no position bias found'
the first number random.Random(0).random() gives: 0.8444 (above 0.5, so the judge always looks)
```

**Read it:** `random.Random(0).random()` is `0.8444` every time it is called, so `0.8444 < 0.5` is always false and the habit **never fires**; every judgement takes the honest path and the test reports no bias at all: `30/60`, `0/30`. The instrument has been wired so that it cannot see the thing it is for, and it prints a clean bill of health. **Fix:** make the generator **once**, outside the loop, and pass it in (`bias_test` does). **Say:** *"a test that cannot fail has not passed."* (Compare Week 29's Mistake 3.)

### Mistake 11 — counting flips on tied pairs as bias (SILENT)

```python
# DELIBERATE MISTAKE 11 (SILENT): an HONEST judge (bias 0.0) shown the same reply twice. It has to pick one; swapped, it "flips" half the time.
rng = random.Random(0)
flips = 0
for text, label, r1, r2 in pairs:
    fwd = judge_pair(label, r1, r1, rng, bias=0.0)
    rev = judge_pair(label, r1, r1, rng, bias=0.0)
    flips += (fwd == "A") == (rev == "A")
print(f"an honest judge, 30 identical pairs: {flips} flips out of 30")
```

```text
an honest judge, 30 identical pairs: 15 flips out of 30
```

**Read it:** both replies are identical, so the honest judge has nothing to go on and `rng.choice` decides; swapped, it decides again, independently; half the time the two coin flips land on the same letter and the "winner" changes. That is `15` flips of `30`, and none of it is bias. **Fix:** drop tied pairs before you count flips (the stand-in's 30 real pairs have no ties, by construction), or report ties on their own line. **Say:** *"a coin flip is not a habit."*

### Mistake 12 — tuning the rules on the frozen eval (SILENT)

```python
# DELIBERATE MISTAKE 12 (SILENT): read the five misses, fix the rules until they go away, and report the new score as the baseline.
TUNED = [
    ("refund",    ["refund", "return", "send them back", "send it back", "money back", "reimburs", "postage", "time limit"]),
    ("billing",   ["invoice", "plan", "paying", "charge", "card", "billing", "subscription", "twice"]),
    ("technical", ["error", "crash", "blank", "csv", "loading", "sync", "closes", "rendering", "nothing", "inbox"]),
    ("greeting",  ["hiya", "hello", "hey", "morning", "evening", "afternoon", "hi,", "hi "]),
]


def tuned_predict(text):
    low = text.lower()
    for label, keys in TUNED:
        if any(k in low for k in keys):
            return label
    return "out_of_scope"


r_tuned = score([tuned_predict(t) for t in texts], "rules, tuned on the eval")
print(f"{r_rules['name']}: {r_rules['correct']}/30   {r_tuned['name']}: {r_tuned['correct']}/30")
for text, gold, pred in r_tuned["wrong"]:
    print("  still wrong:", text, "| gold", gold, "| said", pred)
```

```text
keyword rules (free): 25/30   rules, tuned on the eval: 30/30
```

**Read it:** the tuned rules score `30/30` on the eval, and every edit was chosen by reading the eval misses: a key for `time limit`, the greeting rule moved last, `afternoon` added back. That is not a baseline any more; it is the eval written into the rules. **The honest check is a second set** of tickets written without looking at the rules (Key K5): the free rules score `5/10` on them and the tuned rules `7/10`. The gap between `30/30` and `7/10` is the optimism. **Fix:** tune on training tickets only, and keep the frozen eval for one score at the end. **Say:** *"the score went up because I taught the exam to the rules."* (The same thing is true, at a smaller scale, of the free rules in `baselines.py`; see Key K7.)

---

## 🎲 The Activity, In Full

### Overlap, Agreement and Flips on Paper

**Purpose.** To let the student *feel* what the code hides: that word overlap is a crude dial with no right setting, that agreement between two raters has a floor set by luck, and that a judge which answers differently when the order is swapped is telling you about its position and not about the replies.

### Setup (2 minutes before class)

Print the sheet below once, single-sided. A pen. No computer. **The tickets on Page 30.1 are the course's own; the ratings on Page 30.2 are the real output of Block P6 (two programs, `H` and `J`); the letters on Page 30.3 are the real output of the stand-in judge (Key K4, seed 0, pairs 11-20).** The scores on Page 30.2 are the rubric's.

### The sheet (print only the block between the two ✂ lines)

```text
✂ PRINT ------------------------------------------------------------------
Page 30.1  Overlap on Paper               Name: ____________   Date: ________

A ticket is turned into a SET of words: lower case, letters and digits only,
each word once. "doesn't" becomes two words, "doesn" and "t".
Jaccard = (words in BOTH sets) / (words in EITHER set).

(a) Fill in. Show the two sets.
    1.  "what stocks should I buy?"      and   "should I buy bitcoin?"
        in both: ____________________   in either: ____________________
        Jaccard = ___ / ___ = ______
    2.  "what am I paying each month right now?"  and  "what am I paying per
        month right now?"
        in both (count): ___    in either (count): ___     Jaccard = ______
    3.  "the jacket doesn't fit, can I send it back?"  and
        "opened it, hated it - can I still send it back?"
        in both: ____________________   in either (count): ___
        Jaccard = ___ / ___ = ______

(b) The scan removes a training ticket when its Jaccard against any eval
    ticket is at least the THRESHOLD.
    Threshold 0.70 removes pair(s): ______      Threshold 0.50 removes pair(s): ______
    Which removal at 0.50 do you think is a mistake, and what does it cost
    a category that has only 8 training tickets? ______________________________

(c) "could you tell me my current monthly charge?" and "what am I paying per
    month right now?"  Your eye says ____________________.
    Jaccard says ______.   Why? ______________________________________

(d) The free keyword rules contain the words "rendering" and "inbox".
    Find a ticket on your eval list that contains each: ____________________
    Neither word is in any training ticket. What does that suggest about
    WHEN the rules were written? __________________________________________
    Is 0.833 then a fair score for "free rules on tickets nobody has seen"?
    ____________________________________________________________________

Page 30.2  Agreement on Paper
Twenty replies by the old bot. Each has a rubric score out of 3.
Rater H passes a reply only if it scores 3.  Rater J passes if it scores 2 or 3.

  #  score  H  J   ticket                     #  score  H  J   ticket
  1    3    _  _   hey! quick one for you     11   3    _  _   do I pay postage to return...
  2    2    _  _   good afternoon, are you... 12   1    _  _   cancel order 7781 and put...
  3    1    _  _   hiya                       13   3    _  _   opened it, hated it - can...
  4    2    _  _   hello - first time using.. 14   2    _  _   clicking save does absolut...
  5    3    _  _   morning, got a sec?        15   1    _  _   everything is blank after...
  6    1    _  _   hi, hope this is the rig.. 16   2    _  _   the android version force...
  7    3    _  _   these shoes are the wrong.. 17   3    _  _   my csv download has header...
  8    2    _  _   I'd like my money returned 18   1    _  _   reset email never turns up..
  9    1    _  _   is there a time limit on.. 19   3    _  _   charts stopped rendering...
 10    2    _  _   package never arrived, I.. 20   2    _  _   keeps saying 'network erro...

(a) Write 1 for pass and 0 for fail under H and under J for every row.
(b) Tally:        H pass   H fail
        J pass     ____     ____
        J fail     ____     ____
(c) Agreement  p_o = (both pass + both fail) / 20 = ______
(d) J passes ___ of 20 = ____     H passes ___ of 20 = ____
(e) Luck: p_e = (J pass rate x H pass rate) + (J fail rate x H fail rate)
          = (____ x ____) + (____ x ____) = ______
(f) kappa = (p_o - p_e) / (1 - p_e) = (____ - ____) / (1 - ____) = ______
(g) Look at the two off-diagonal cells. Which way does J lean?  ____________
(h) A lazy judge says "pass" to all 20 replies, on a set where a person passes
    18 of 20.   p_o = ______   p_e = ______   kappa = ______
    Write one sentence about why raw agreement is a poor number. ____________

Page 30.3  Flips on Paper
A sealed judge is asked each question twice.  Column A: v1 was shown first.
Column B: v2 was shown first.  The judge answers "A" (the reply shown first) or
"B" (the reply shown second).

 pair  ticket                              A: said   B: said   winner    winner    same?
                                                              in A      in B
  11   do I pay postage to return somethi    A         B
  12   cancel order 7781 and put the mone    B         A
  13   opened it, hated it - can I still     A         A
  14   clicking save does absolutely noth    A         A
  15   everything is blank after I sign i    B         A
  16   the android version force closes o    A         A
  17   my csv download has headers but no    A         B
  18   reset email never turns up in my i    B         A
  19   charts stopped rendering yesterday    A         A
  20   keeps saying 'network error' on a     B         A

(a) In column A, "A" means the winner is v1 and "B" means v2. In column B,
    "A" means the winner is v2 (it was shown first) and "B" means v1.
    Fill the two "winner" columns and write yes/no under "same?".
(b) Flips (same? = no): ____ of 10.    Estimate of the bias = flips / 10 = ______
(c) How many of the 20 answers were "A"? ____  A judge with no habit would
    say "A" about ____ times in 20.
(d) Of the pairs that did NOT flip, how many had v1 as the winner? ____  v2? ____
(e) If you had only run column A, how many of the ten would say v1 wins? ____
    What would you have concluded? ____________________________________
(f) One sentence: why is one run of ten pairs a shaky measurement, and what
    would you do to make it steadier? ____________________________________
✂ END PRINT --------------------------------------------------------------
```

### What "finished" looks like

Page 30.1 with the three Jaccards (`3/6 = 0.500`, `7/9 = 0.778`, `5/13 = 0.385`), the two thresholds (`0.70`: pair 2 only; `0.50`: pairs 1 and 2) and the three sentences; Page 30.2 with the grid `7 7 / 0 6`, `0.65`, `0.44`, `0.375`; Page 30.3 with four flips and a sentence. The student keeps all three. **Marks:** 30.1 (a) three boxes; 30.2 (a) twenty rows, count a row right only if both H and J are right; 30.3 (a) ten rows.

### Variation — shorter (a 50-minute slot)

Give the student `evalset.py` already typed and `dedup.py` already saved. Run P1, P2 and P10 as one block; do Page 30.2 and P6 fully; give the P8 output printed and have them read it against Page 30.3. Drop P4, P9 and Mistake 12. The minimum viable lesson is: *the rules beat my model; kappa by hand; swap the order.*

### Variation — an anxious or slow student

Give the completed `evalset.py`, `dedup.py` and `bias_test`; have them type only the `cohen_kappa_score` line and the print loop of P6. The sentence that must survive: *"I ask the judge twice, in both orders, and count how often it changes its mind."* Skip Page 30.1 (c) and (d) and Page 30.3 (e) and (f).

### Variation — harder (a student who finishes early)

Homework 3's bias sweep, then: *"Write a second mystery judge whose flaw is "prefers the longer reply" and show that the swap test calls it clean."* (Key: a judge that always picks the longer reply gives the same winner in both orders, so it has a flip rate of `0` and a first-position rate of `0.5`, and it is still wrong whenever the shorter reply is the better one. The honest companion is kappa, or agreement with the rubric.) Keep it local: a function in the student's own folder.

---

## ❓ Questions Students Ask This Week

**"Why is the trained model worse than the rules? I thought the trained one was supposed to be smart."** It has 64 tickets, and some of its eval tickets contain words it never saw (`hiya` is in no training ticket). The rules were written by someone looking at the eval. Both facts are in the table. The right move is to say so and not to tune it until it wins.

**"Why is the rules' out_of_scope perfect?"** It is the default: whatever no key matches is called `out_of_scope`. A system that defaults to one label scores 100 percent on that label and pays for it elsewhere (the rules misread `nothing` as a greeting).

**"Is 0.833 a good score?"** Compared with what? With 0.200 for the floor, yes; with a model that fails on exactly the categories a real queue cares about, maybe not; and the rules were written with the eval in view. Compare on a second set (Homework 1).

**"Why fingerprint instead of just not touching the file?"** Because you will touch it, with good reasons, at 11 p.m. The fingerprint makes touching it loud.

**"Can't the scan just use a lower threshold and catch everything?"** At `0.20` it removes 25 of 66 tickets and still misses four of the five paraphrases (their highest Jaccards are `0.200`, `0.083`, `0.143`, `0.143`, `0.077`; only the first reaches `0.20`). The dial trades copies caught against tickets lost; it does not reach meaning.

**"What is a 'good' kappa?"** By convention above `0.6`. It depends on what a wrong verdict costs and on how good the labels are. Our `0.375` is "fair"; it would not let you use the judge without checking its passes by hand.

**"Why can't I just use agreement?"** Because a judge that always says pass gets `0.90` on a set where 18 of 20 pass, and `κ = 0`. Agreement rewards not looking.

**"Why do we need both orders? Isn't the judge just picking the better reply?"** It is picking the better reply *some* of the time. When it ignores the replies it says "A", so in one order it favours v1 and in the other v2. Only asking twice separates the habit from the judgement.

**"Does this mean real LLM judges prefer the first answer?"** I don't know; this judge is a script with a number in it. People who test real ones use this swap test, and report that they sometimes do. What we built is the test.

**"Why not just make the judge consistent?"** A judge that answers the same in both orders may still be wrong in both. Consistency is necessary, not enough.

**"Why 30 tickets? That seems few."** It is small enough to hand-write in an evening and freeze, and large enough to show the method. One ticket is `0.033`; a five-ticket category moves by `0.2` on one. Week 31 uses that.

**"Can I add more tickets to the eval later?"** Yes, in a new file with its own fingerprint. You do not edit the frozen one.

---

## ⚠️ Where This Lesson Goes Wrong

| Symptom | What is happening | What to do |
|---|---|---|
| `AssertionError: the frozen eval set was edited` on `import evalset` | A ticket or label was mistyped, or the student pasted `FROZEN` before finishing the file | Compare with the guide; the fingerprint is over the text and the label; fix the ticket, not `FROZEN` |
| The student says "the trained model is broken" | Rules `25` against classifier `21` | Section 8, item 2; Block P10 |
| Counts of removed tickets differ from `2` | Different `words` function (for instance `str.split`) | `words` must use `re.findall(r"[a-z0-9]+", ...)` on `.lower()` text |
| `TypeError: unsupported operand type(s) for &` | Lists, not sets | Mistake 5 |
| `ZeroDivisionError` in `jaccard` | A ticket with no letters and no guard | Mistake 6 |
| Kappa `nan` or a warning | Both raters say the same single thing on every item (`p_e = 1`) | Kappa is undefined; look at the data. One rater saying one thing gives `0.0`, not `nan` (Key K3) |
| The bias test says `0` flips | A fresh generator per call | Mistake 10 |
| The bias test says half the pairs flip | Tied pairs (identical replies) in the list | Mistake 11 |
| The student's flip rate is not `0.267` | A different seed, one generator per pair, or `judge_pair` called in a different order | The seeded sequence is fixed: fwd then rev, pair by pair, one `random.Random(0)` |
| The student opens `mystery.py` early | Curiosity | Fine; move to the "estimate from 10 pairs" and ask how wobbly it is |
| "Kappa 0.375 so the judge is fine" | Reading the number and not the cells | Mistake 7 |
| The lesson overruns | Part 1 (typing) and Part 3 (writing `dedup.py`) | Hand over `evalset.py` and `dedup.py`; keep P2, P6 and P8 |

---

## 🧭 Differentiation

### If the student is struggling

Stay with three ideas: *(1) the eval is written first and frozen, and the free rules are the rung to beat; (2) agreement needs luck taken out (`0.65` is not `0.375`); (3) ask a judge twice, in both orders.* Give the completed `evalset.py`, `dedup.py` and `bias_test`. The student runs P2, P6 and P8 and reads three numbers aloud: `0.833`, `0.375` and `8` of `30`. Skip P3, P4 and P9. The minimum viable lesson: the student says *"a judge that changes its answer when I swap the order is not reading the replies"* and does Page 30.2 (a) to (d).

### If the student is flying

Ask them to **predict, then run**: *"If I plant a bias of 0.25 instead of 0.5, what will the first-position win rate be?"* (`0.5 + 0.25/2 = 0.625`; Key K6 gives the flip rates.) Then the challenge: **build the fairest test you can for `judge_pair`**, using many more pairs of the same thirty tickets, and report the estimate with its spread. Extensions: show that the flip rate and `2 × first-position rate − 1` are equal on every seed (K2) and say why; design a second scorer for the replies that is *not* the rubric (for instance, word count alone) and compute kappa between the two.

### If the student won't engage today

Do the hook and Page 30.2 only. It is a pen lesson at heart: *"you are the strict reader and the lenient reader; count where you differ."* The code can wait for the homework.

---

## ✅ Assessing Understanding

Ask these out loud near the end; do not rescue.

| Question | A good answer | A shaky answer |
|---|---|---|
| Why is the eval written and frozen before the model? | Otherwise you can tune the eval to the outputs; the fingerprint makes an edit loud | "To keep it safe" |
| Why does the trained model have to beat the rules, not the floor? | The rules are the cheap thing a team would ship instead; beating a 20 percent floor says little | "The rules are worse" |
| What does the contamination scan do, and not do? | Removes training tickets that share most of their words with an eval ticket; cannot see a paraphrase, and the threshold is a trade | "It removes leaks" |
| Our paraphrases gave `+2` tickets. What does that tell you? | The score measures memory of the paraphrases; the scan missed them | "The model got better" |
| What is `p_e` in kappa, in words? | How often two raters would agree by luck if each kept their own pass rate and did not look | "The error" |
| Raw agreement `0.90`, kappa `0`. Explain. | Nearly everything passes; a judge that says pass to all gets 0.90 and has no skill | "It's a bug" |
| What does swapping the order show? | Whether the judge's answer follows the replies or the position; the flip rate estimates the habit | "Which reply is better" |
| Seed 0 says `0.267`, the truth is `0.5`. Is the test broken? | No: thirty pairs is a small sample; other seeds say `0.27` to `0.70`; more pairs steadies it | "Yes" |
| Name a judge the swap test would call clean and that is still wrong. | One that prefers the longer reply in both orders | "None" |
| What did today show about real LLM judges? | Nothing about how they behave; it showed the tests | "That they prefer the first answer" |

### Mastery scale for this week

| Level | Evidence |
|:--:|---|
| 🟥 Not yet | Reads scores as facts without asking "of what, compared with what"; treats kappa as "accuracy of the judge"; reads the flip rate as a fact about real judges. |
| 🟨 Emerging | Runs the code; computes `p_o` but not `p_e`; says the judge has a habit but not how they know; misses that the rules win. |
| 🟩 Secure | Completes Page 30.2 with `0.375`; says the trained model lost and by how many tickets; recovers roughly the right flip rate and says one run is one draw; says the scan does not catch paraphrases. |
| 🟦 Strong | Also predicts the first-position rate before it runs, spots that the rules were written with the eval in view, catches the fresh-generator mistake unprompted, and names a flaw the swap test cannot find. |

---

## 📤 Homework to Assign

~55 minutes, in the workbook, pages 30.1-30.3. The three tasks:

1. **A second set (page 30.1).** Write **ten** new support tickets, two per category, in your own words, *without* looking at `RULES` while you write. Save them in a new file `second_set.py` with its own fingerprint (do not touch `evalset.py`). Score the free rules on them, run the scan against the frozen eval, and compare with `25/30`. Write two sentences: what the gap says, and why ten tickets is a small set. (Key K5.)
2. **A lenient, a middle and a strict judge (page 30.2).** Rater `J` passes a reply at a score of 1, 2 or 3 (out of 3). For each, work out the agreement with `H` and the kappa (by hand for the 2 case; `cohen_kappa_score` for the others), and say which cases are degenerate and why. (Key K3.)
3. **How small a bias can thirty pairs see? (page 30.3).** `judge_pair` takes a `bias=` keyword. For `bias` of `0.1` and `0.25`, run the bias test for twenty seeds each, report the smallest, largest and average of the flip rates, and say which of the two you would be willing to call "found" from one run. Finish with three sentences: what the swap test shows, what it cannot, and what today says about a real judge. (Key K6.)

Extension for the fast student: the flying challenge, and the "prefers the longer reply" judge.

---

## 🔑 Answer Key

Every number below comes from the blocks above or from `K1` to `K7` (TEACHER-ONLY; below).

### Page 30.1 — Overlap on Paper

(a1) In both: `should, i, buy` (3); in either: `what, stocks, should, i, buy, bitcoin` (6). `3 / 6 = 0.500`.
(a2) In both `7` (`what, am, i, paying, month, right, now`); in either `9` (those seven plus `each` and `per`). `7 / 9 = 0.778`.
(a3) `the jacket doesn't fit, can I send it back?` gives `the, jacket, doesn, t, fit, can, i, send, it, back` (10); `opened it, hated it - can I still send it back?` gives `opened, it, hated, can, i, still, send, back` (8; `it` is written three times but counted once). In both: `can, i, send, it, back` (5). In either: `10 + 8 − 5 = 13`. `5 / 13 = 0.385`.
(b) At `0.70`: pair 2 only. At `0.50` (the scan removes at *at least* the threshold): pairs 1 and 2. The mistake at `0.50` is pair 1: a different question (`stocks` against `bitcoin`) and it costs one of the only **8** `out_of_scope` training tickets, an eighth of that category.
(c) The eye says *the same question*. Jaccard says `0.000`: no shared word. **The scan compares words, not meaning.** (A paraphrase stays in training; Block P4.)
(d) `rendering`: `charts stopped rendering yesterday afternoon`; `inbox`: `reset email never turns up in my inbox`. Neither is in a training ticket, which suggests the rules were written **after** the eval was seen. So `0.833` is generous: on ten unseen tickets the same rules score `5/10` (Key K5). Accept any answer that says "not a fair score for unseen tickets".

### Page 30.2 — Agreement on Paper

(a) `H`: pass (1) on rows `1, 5, 7, 11, 13, 17, 19` (score 3), else 0. `J`: pass on every row except `3, 6, 9, 12, 15, 18` (score 1).
(b) `H pass / J pass` `7`; `H fail / J pass` `7`; `H pass / J fail` `0`; `H fail / J fail` `6`.
(c) `p_o = (7 + 6) / 20 = 0.65`.
(d) `J` passes `14` of 20 (`0.70`); `H` passes `7` of 20 (`0.35`).
(e) `p_e = (0.70 × 0.35) + (0.30 × 0.65) = 0.245 + 0.195 = 0.44`.
(f) `κ = (0.65 − 0.44) / (1 − 0.44) = 0.21 / 0.56 = 0.375`. (Matches Block P6: `0.3750`, and the library's `0.375`.)
(g) `J` is **lenient**: it passes `7` replies `H` fails and never fails one `H` passes.
(h) `p_o = 18 / 20 = 0.90`; `p_e = 1.0 × 0.90 + 0.0 × 0.10 = 0.90`; `κ = 0`. Any sentence that says *raw agreement rewards a judge that never looks when almost everything passes*.

### Page 30.3 — Flips on Paper

(a) Winners in column A / column B / same?: `11`: v1 / v1 / yes · `12`: v2 / v2 / yes · `13`: v1 / v2 / **no** · `14`: v1 / v2 / **no** · `15`: v2 / v2 / yes · `16`: v1 / v2 / **no** · `17`: v1 / v1 / yes · `18`: v2 / v2 / yes · `19`: v1 / v2 / **no** · `20`: v2 / v2 / yes. (Key K4 prints the same table.)
(b) `4` of 10; estimate `0.40`. (The 30-pair run gave `0.267`; the planted value is `0.5`.)
(c) `14` of the 20 answers are "A"; a judge with no habit says "A" `10` times in 20.
(d) Of the six pairs that did not flip, v1 won `2` (pairs 11, 17) and v2 won `4` (12, 15, 18, 20) — and **the rubric agrees with all six**.
(e) Six of the ten (`11, 13, 14, 16, 17, 19`) say v1 wins. The rubric says v1 is better in `4` of these ten. A reader of column A alone would say v1 wins `6` of 10; a reader of column B alone (v2 shown first) would say v1 wins only `2` of 10. Each single order is pulled toward whichever reply it shows first; the truth (`4`) sits between them.
(f) Any sentence that says ten pairs is a small sample (4 flips could be 2 or 6 on another seed) and that more pairs, or the same pairs asked again with fresh draws, narrows the estimate (Key K2: ten times the pairs cuts the spread to about a third).

### The teacher-only key: every number

**K1 — the threshold is a dial**

```python
# k1_sweep.py (TEACHER-ONLY): how many of the 66 raw training tickets the scan removes at each threshold.
for th in (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00):
    kept, gone = decontaminate(TRAIN_RAW, EVAL, threshold=th, verbose=False)
    print(f"threshold {th:.2f}: removed {len(gone):2d}   e.g. {gone[-1][1]!r}" if gone else f"threshold {th:.2f}: removed  0")
kept, gone = decontaminate(TRAIN_RAW, EVAL, threshold=0.50, verbose=False)
print("the third ticket removed at 0.50:", [(t, round(w[0], 3), w[2]) for _, t, w in gone][-1])
```

```text
threshold 0.20: removed 25   e.g. 'what stocks should I buy?'
threshold 0.30: removed  7   e.g. 'what stocks should I buy?'
threshold 0.40: removed  3   e.g. 'what stocks should I buy?'
threshold 0.50: removed  3   e.g. 'what stocks should I buy?'
threshold 0.60: removed  2   e.g. 'what am I paying each month right now?'
threshold 0.70: removed  2   e.g. 'what am I paying each month right now?'
threshold 0.80: removed  1   e.g. 'is there a time limit on sending items back?'
threshold 0.90: removed  1   e.g. 'is there a time limit on sending items back?'
threshold 1.00: removed  1   e.g. 'is there a time limit on sending items back?'
the third ticket removed at 0.50: ('what stocks should I buy?', 0.5, 'should I buy bitcoin?')
```

**Read it:** `0.20` removes 25 of the 66 training tickets (far too many), `0.30` removes 7, `0.40` and `0.50` remove 3, `0.60` and `0.70` remove 2, and from `0.80` only the exact copy goes. The third ticket, which arrives at `0.50`, is `'what stocks should I buy?'` against `'should I buy bitcoin?'`: a different question on the same subject, and `out_of_scope` has only 8 training tickets to spare. **No usable threshold catches the paraphrases**: only one of the five reaches `0.200` (the rest are `0.143` or lower), and `0.20` already removes 25 of 66 tickets. That is the argument for a comparison that looks at meaning (Week 25's embeddings could, but nothing in this course measures how well; say so).

**K2 — the bias test, 200 seeds, a control, ten times the pairs**

```python
# k2_bias.py (TEACHER-ONLY): the bias test over 200 seeds, a control with no bias, and 10 times the pairs.
import numpy as np
runs = [bias_test(pairs, s) for s in range(200)]
est = np.array([2 * r["first_wins"] / 60 - 1 for r in runs])
flip_rate = np.array([r["flips"] / 30 for r in runs])
print("estimate from first-position wins  mean", round(est.mean(), 3), " SD", round(est.std(), 3), " min", round(est.min(), 2), " max", round(est.max(), 2))
print("the flip rate is the SAME number on every seed:", bool(np.allclose(est, flip_rate)))
print("seeds whose estimate is within 0.1 of the truth (0.5):", int((abs(est - 0.5) <= 0.1).sum()), "of 200")
naive = np.array([r["naive_v1"] for r in runs])
print("naive 'v1 wins' out of 30: mean", round(naive.mean(), 1), " seeds with more than 15:", int((naive > 15).sum()), "of 200")
cons_v1 = np.array([r["v1_cons"] for r in runs]); cons_n = np.array([r["v1_cons"] + r["v2_cons"] for r in runs])
print("consistent pairs: v1 share  mean", round((cons_v1 / cons_n).mean(), 3), "  (rubric: 0.333)")

# the control: a judge with NO planted bias
rng = random.Random(0)
fw = fl = 0
for text, label, r1, r2 in pairs:
    f = judge_pair(label, r1, r2, rng, bias=0.0); r = judge_pair(label, r2, r1, rng, bias=0.0)
    fw += (f == "A") + (r == "A"); fl += (f == "A") == (r == "A")
print("control, bias 0.0: first-position wins", fw, "/60, flips", fl, "/30")

# ten times the pairs: the same 30 tickets asked 10 times with fresh draws
def many(seed, times):
    rng = random.Random(seed); fw = 0
    for _ in range(times):
        for text, label, r1, r2 in pairs:
            fw += (judge_pair(label, r1, r2, rng) == "A") + (judge_pair(label, r2, r1, rng) == "A")
    return 2 * fw / (60 * times) - 1
big = np.array([many(s, 10) for s in range(30)])
print("300 pairs per run, 30 runs: mean", round(big.mean(), 3), " SD", round(big.std(), 3), " min", round(big.min(), 2), " max", round(big.max(), 2))
```

```text
estimate from first-position wins  mean 0.494  SD 0.087  min 0.23  max 0.73
the flip rate is the SAME number on every seed: True
seeds whose estimate is within 0.1 of the truth (0.5): 130 of 200
naive 'v1 wins' out of 30: mean 19.9  seeds with more than 15: 197 of 200
consistent pairs: v1 share  mean 0.332   (rubric: 0.333)
control, bias 0.0: first-position wins 30 /60, flips 0 /30
300 pairs per run, 30 runs: mean 0.501  SD 0.031  min 0.43  max 0.58
```

**Read it:** (1) the estimate from the 30 pairs has mean `0.494` and SD `0.087` over 200 seeds, from `0.23` to `0.73`; only `130` of `200` runs land within `0.1` of the truth. Seed 0's `0.267` is a low draw, not a mistake. (2) The two estimators are **the same number on every seed** (`True`): for this stand-in the flip rate equals `2 × (first-position win rate) − 1` exactly, because its only flaw is "sometimes says A" and there are no ties. (3) The naive single-order verdict "v1 wins more than half" appears on `197` of `200` seeds (mean `19.9` of `30`; the rubric: `10`). (4) The consistent pairs always carry the rubric's answer: v1's share has mean `0.332` against the rubric's `0.333`. (5) The control, with `bias=0.0`, gives exactly `30/60` and `0` flips: **the test can say "no bias"**, which is what makes it worth running. (6) Asking the same thirty tickets ten times (300 pairs per run) narrows the spread to SD `0.031` (`0.43` to `0.58`). **Why the flip rate is the planted bias, in words, for you only:** an honest answer depends on the pair and not the order, so it never flips; a pair flips when both answers are biased, or when exactly one is biased and the honest answer disagrees with the biased "A"; adding those cases up gives exactly `BIAS`.

**K3 — a lenient, a middle and a strict judge (Homework 2)**

```python
# k3_lenient.py (TEACHER-ONLY): kappa for a judge that passes at 1, 2 or 3 points out of 3, against the strict reader H. (Homework 2.)
for cut in (1, 2, 3):
    Jc = [1 if rubric(r, l) >= cut else 0 for _, l, r in items]
    agree = sum(h == j for h, j in zip(H, Jc)) / 20
    print(f"passes at {cut}+: J passes {sum(Jc)}/20   agreement {agree:.2f}   kappa", round(cohen_kappa_score(H, Jc), 4))
print("H against itself:", round(cohen_kappa_score(H, H), 4))
```

```text
passes at 1+: J passes 20/20   agreement 0.35   kappa 0.0
passes at 2+: J passes 14/20   agreement 0.65   kappa 0.375
passes at 3+: J passes 7/20   agreement 1.00   kappa 1.0
H against itself: 1.0
```

**Read it:** a judge that passes at `1+` passes everything (`20/20`): agreement `0.35`, equal to the human's pass rate, and `κ = 0.0` (`p_e = 1.0 × 0.35 + 0.0 × 0.65 = 0.35 = p_o`; it is `nan` only if H also said one thing only). At `2+` (our `J`) agreement `0.65` and `κ = 0.375`. At `3+` the judge *is* `H`, so agreement is `1.00` and `κ = 1.0`, which is trivial: `H` is defined as the `3+` rule. The lesson of the row at `1+` is the one of Block P7: **a judge that never looks can have respectable-looking agreement.**

**K4 — Page 30.3's answers**

```python
# k4_sheet.py (TEACHER-ONLY): pairs 11 to 20 of Page 30.3 (the same seed-0 run as Block P8, so the draws are the ones P8 made) - the mystery judge, seed 0, both orders.
rng = random.Random(0)
print("pair  ticket                           v1 first -> winner   v2 first -> winner   same?")
flips10 = first10 = 0
rows = []
for i, (text, label, r1, r2) in enumerate(pairs):
    f = judge_pair(label, r1, r2, rng); r = judge_pair(label, r2, r1, rng)
    rows.append((i, text, label, r1, r2, f, r))
for i, text, label, r1, r2, f, r in rows[10:20]:
    wf = "v1" if f == "A" else "v2"; wr = "v2" if r == "A" else "v1"
    flips10 += wf != wr; first10 += (f == "A") + (r == "A")
    print(f"{i + 1:3d}   {text[:30]:30s}   {f} ({wf})               {r} ({wr})               {'yes' if wf == wr else 'NO'}")
print("flips in pairs 11-20:", flips10, "| first-position wins in pairs 11-20:", first10, "of 20")
print("rubric winner of each:", ["v1" if rubric(a, l) > rubric(b, l) else "v2" for _, l, a, b in pairs[10:20]])
```

```text
pair  ticket                           v1 first -> winner   v2 first -> winner   same?
 11   do I pay postage to return som   A (v1)               B (v1)               yes
 12   cancel order 7781 and put the    B (v2)               A (v2)               yes
 13   opened it, hated it - can I st   A (v1)               A (v2)               NO
 14   clicking save does absolutely    A (v1)               A (v2)               NO
 15   everything is blank after I si   B (v2)               A (v2)               yes
 16   the android version force clos   A (v1)               A (v2)               NO
 17   my csv download has headers bu   A (v1)               B (v1)               yes
 18   reset email never turns up in    B (v2)               A (v2)               yes
 19   charts stopped rendering yeste   A (v1)               A (v2)               NO
 20   keeps saying 'network error' o   B (v2)               A (v2)               yes
flips in pairs 11-20: 4 | first-position wins in pairs 11-20: 14 of 20
rubric winner of each: ['v1', 'v2', 'v1', 'v2', 'v2', 'v2', 'v1', 'v2', 'v1', 'v2']
```

**Read it:** the student sees the two letters per pair; this block prints the winner behind each. Flips are pairs `13, 14, 16, 19` (**four of ten**, so the estimate from ten pairs is `0.40` against the true `0.5` and the 30-pair `0.267`); first-position wins `14` of `20` (`0.70`, against `0.50` for no habit); the six consistent pairs are `11, 12, 15, 17, 18, 20` with winners `v1, v2, v2, v1, v2, v2`, **which is exactly what the rubric says for each of them**. (The window is pairs 11 to 20 of the same seed-0 run as Block P8. Pairs 1 to 10 of that run contain only one flip, which makes a poorer page; say so if the student asks why the page starts at 11.)

**K5 — a second set (Homework 1)**

```python
# k5_second_set.py (TEACHER-ONLY key for Homework 1): ten NEW tickets written by the teacher, never used to build the rules. Rules before and after tuning.
SECOND = [
    ("hi - is anybody there?", "greeting"), ("good evening team", "greeting"),
    ("the kettle arrived cracked, can I get my money back?", "refund"), ("how do I post this parcel back to you?", "refund"),
    ("I can't open the app since the update", "technical"), ("the export button does nothing", "technical"),
    ("my subscription renewed and I want to cancel", "billing"), ("can you send me last month's receipt?", "billing"),
    ("who sings this song?", "out_of_scope"), ("what time does the cricket match start?", "out_of_scope"),
]
for name, fn in (("free rules", rules_predict), ("rules tuned on the eval", tuned_predict)):
    guess = [fn(t) for t, _ in SECOND]
    hit = sum(g == y for g, (_, y) in zip(guess, SECOND))
    print(f"{name:24s} {hit}/10   misses:", [(t[:28], g) for g, (t, y) in zip(guess, SECOND) if g != y])
print("overlap of the ten with the frozen eval (highest Jaccard):", round(max(jaccard(t, e) for t, _ in SECOND for e, _ in EVAL), 3))
```

```text
free rules               5/10   misses: [('how do I post this parcel ba', 'greeting'), ("I can't open the app since t", 'out_of_scope'), ('the export button does nothi', 'greeting'), ("can you send me last month's", 'out_of_scope'), ('who sings this song?', 'greeting')]
rules tuned on the eval  7/10   misses: [('how do I post this parcel ba', 'out_of_scope'), ("I can't open the app since t", 'out_of_scope'), ("can you send me last month's", 'out_of_scope')]
overlap of the ten with the frozen eval (highest Jaccard): 0.25
```

**Read it:** on ten new tickets written without the rules in view, the free rules score `5/10 = 0.500` (their misses: `post this parcel back` went to `greeting` because of `"hi"` in `this`; `since the update` found no key; `the export button does nothing` went to greeting through `"hi"` in `nothing`; `last month's receipt` found no key; `who sings this song?` went to greeting through `"hi"` in `this`), and the rules tuned on the eval score `7/10`. Against the `0.833` they got on the eval. **Ten tickets is a small set** (one ticket is `0.1`), so say the gap is big enough to notice and too small a sample to put a number on. The highest Jaccard of the ten against the frozen eval is `0.250`, so none of them is a copy.

**K6 — how small a bias can 30 pairs see? (Homework 3)**

```python
# k6_weak_bias.py (TEACHER-ONLY key for Homework 3): can 30 pairs see a weak bias? Planted bias 0.1, 0.25 and 0.5, twenty seeds each.
for b in (0.0, 0.1, 0.25, 0.5):
    ests = []
    for s in range(20):
        rng = random.Random(s); fw = 0
        for text, label, r1, r2 in pairs:
            fw += (judge_pair(label, r1, r2, rng, bias=b) == "A") + (judge_pair(label, r2, r1, rng, bias=b) == "A")
        ests.append(2 * fw / 60 - 1)
    print(f"planted {b:.2f}: estimates from {min(ests):.2f} to {max(ests):.2f}, average {np.mean(ests):.3f}, seeds that found 'zero bias': {sum(e == 0 for e in ests)} of 20")
```

```text
planted 0.00: estimates from 0.00 to 0.00, average 0.000, seeds that found 'zero bias': 20 of 20
planted 0.10: estimates from 0.03 to 0.23, average 0.110, seeds that found 'zero bias': 0 of 20
planted 0.25: estimates from 0.13 to 0.37, average 0.247, seeds that found 'zero bias': 0 of 20
planted 0.50: estimates from 0.27 to 0.70, average 0.475, seeds that found 'zero bias': 0 of 20
```

**Read it:** with no bias every seed gives exactly `0.00`. With a planted `0.10` the estimates run `0.03` to `0.23` (average `0.110`), with `0.25` from `0.13` to `0.37`, with `0.50` from `0.27` to `0.70`. No seed finds "zero" when the bias is there, so 30 pairs **can tell a biased judge from an honest one**, but it cannot tell `0.10` from `0.25` on one run with any confidence. The honest answer to "how small can it see?" is: *it can see that something is there; it cannot size it.* Ten times the pairs (K2) would.

**K7 — the free rules were written with the eval in view**

```python
# k7_rules_keys.py (TEACHER-ONLY): which RULES keys occur in an eval ticket but in NO training ticket?
from baselines import RULES
eval_text = " ".join(t.lower() for t, _ in EVAL)
train_text = " ".join(t.lower() for t, _ in TRAIN_RAW)
seen_in_eval_only = [(label, k) for label, keys in RULES for k in keys if k in eval_text and k not in train_text]
print(len(seen_in_eval_only), "of", sum(len(keys) for _, keys in RULES), "keys:", seen_in_eval_only)
for label, k in seen_in_eval_only:
    print(f"  {k!r:16s} <- {[t for t, _ in EVAL if k in t.lower()][0]!r}")
```

```text
8 of 32 keys: [('greeting', 'hiya'), ('greeting', 'afternoon'), ('refund', 'send them back'), ('refund', 'postage'), ('technical', 'blank'), ('technical', 'closes'), ('technical', 'rendering'), ('technical', 'inbox')]
  'hiya'           <- 'hiya'
  'afternoon'      <- 'good afternoon, are you there?'
  'send them back' <- 'these shoes are the wrong colour, how do I send them back?'
  'postage'        <- 'do I pay postage to return something?'
  'blank'          <- 'everything is blank after I sign in'
  'closes'         <- 'the android version force closes on launch'
  'rendering'      <- 'charts stopped rendering yesterday afternoon'
  'inbox'          <- 'reset email never turns up in my inbox'
```

**Read it:** eight of the 32 keys appear in an eval ticket and in **no** training ticket. Each of these eight is a word the eval contains and the training tickets do not: that is what you see when the rules were written looking at the eval. Nobody did this to cheat (the rules are a plain keyword list, and this is the course's first teaching of baselines), but it means `0.833` is optimistic for an unseen queue; K5 shows `0.500` on ten fresh tickets. **What to do with it:** say it once, plainly, when the student asks why the rules are so good; do not change `RULES`, because Week 31 compares against `25/30`; and use it as the live example of Mistake 12.



### Answers to every question posed in the lesson

| Where | Question | Answer |
|---|---|---|
| Hook | "90 percent of what? Compared with what? Who marked it?" | The tickets (which, how many, which categories), a baseline (floor, free rules), the marker (program, person or judge). |
| Concept | "If the floor scores 20 percent, is 70 percent good?" | Not until you know the rules score 83. |
| Their Turn | "Which pairs are near-copies, and which are different questions?" | a2 near-copy (`0.778`); a1 and a3 share words but are different questions. |
| Their Turn | "What would 0.5 do to pair 1?" | Remove a harmless out_of_scope training ticket. |
| Part 1 | "Which category can we say the least about?" | billing and out_of_scope (five tickets each). |
| Part 2 | "Why is the rules' out_of_scope perfect?" | It is the default answer when no key matches. |
| Part 3 | "Is 23 better than 21?" | No: it measures memory of five paraphrases, which the scan missed. |
| Part 4 | "Would you trust a judge that agrees 90 percent of the time?" | Not before asking what it says to the easy cases; `κ` can be `0`. |
| Part 5 | "What would a judge with no habit give for first-position wins?" | `30` of `60` (`0.500`). |
| Wrap | "What was and was not shown?" | A method and a dial. Not how real judges behave. |

### Reconciliation with the reference module (`module-08-finetuning-and-evaluating-llms.md`)

The patched module and this week agree where they overlap, and differ in six places that you should know about so that you are not surprised by the module.

1. **The rules baseline.** The module's patched text gives the measured `25/30 = 0.833` with the same five misses (its patch log #2 explains the `17/30` in its first draft). **Added here:** the rules were written with the eval in view (Key K7), which the module does not say.
2. **The trained baseline.** The module's Part C2 `21/30 = 0.700`, `out_of_scope` `1/5`, and the nine misses are reproduced exactly by Block P2; the module's `22/30` raw against `21/30` clean is Block P4. The module's `SNEAKY` paraphrases and their Jaccards (`0.200, 0.083, 0.143, 0.143, 0.077`) and the `21 → 23` inflation are reproduced exactly; **the module's indices `eval#8` and `eval#23` are zero-based**, as Python prints them.
3. **Code changes made for the ladder.** The module's `dedup.py` and `scorer.py` use `re.sub` (a Week 33 construct) and `collections.defaultdict`; here `re.findall` and a plain dict do the same job and give the same counts. The tokenisation is identical (`"doesn't"` gives `doesn` and `t`).
4. **Kappa.** The module's worked example (`16 / 6 / 2 / 6`, `κ = 0.4118`) is **illustrative** (its counts need an API judge); its arithmetic is exact. This week's grid (`7 / 7 / 0 / 6`, `κ = 0.375`) is measured, from two programs. The module's `cohen_kappa` and `kappa_label` are its own functions; here the student computes by hand and checks with `cohen_kappa_score`. The band names are the module's.
5. **Position bias.** The module's test uses an API judge and prints **illustrative** counts (`19/30` naive, `12/22` consistent, `36/60` first-position, flip rate `0.267`, stated as not reproduced). This week's test is the same **method** against a scripted stand-in with a planted `BIAS`, and all its numbers are measured (`16/30` naive, `8` v1 and `14` v2 among the `22` consistent pairs, `38/60` first-position wins, `8/30` flips: Block P8). The module's counts are **not** this week's counts and must not be mixed on the board.
6. **What was dropped.** The module's prompted-Claude baseline, the DistilBERT run and the LLM judge calls need an API or a checkpoint and are not built; nothing here depends on them. Its MiniLM-based contamination scan is not built either (the module marks its catch rate "not measured" and so do we).

Two ledger defects named in the plan do not touch this week (`build_registry` and the capstone routing belong to Weeks 28 and 34; the `redact_pii` ISO-date defect belongs to Week 33). This week's reference code had none; the one defect found is **the free rules being written with the eval in view** (Key K7), which is reported, not fixed.

---

## 🔮 Next Week Preview

**Week 31 — Fine-Tuning, LoRA, and the Regression** (🟩 lab). The student pretrains a tiny encoder once on a handed-out pile of template sentences, puts a five-label head on it, fine-tunes it on the **64 clean training tickets** two ways (every weight, or a **low-rank patch** beside frozen weights), and reads **this week's `score` and `compare`** on the **frozen eval**. The new maths is **low-rank** (a big grid as the product of two thin ones); the new syntax is `nn.Parameter`, `requires_grad_(False)`, `nn.init.zeros_` / `normal_` and `copy.deepcopy(model)`. **What from today carries over:** the five files (`evalset.py`, `traindata.py`, `dedup.py`, `scorer.py`, `compare.py`), the fingerprint, the scan (which will find no exact copy and 38 near-copies in the pretraining text), the rules baseline at `25/30`, and the habit of reading **a category that fell while the average rose**. **Prep for you:** before the lesson check that the student's folder still passes `python -c "import evalset"`; Week 31's first block prints the counts `30`, `66`, `64`, `2` and `14 14 14 14 8`, and nothing else in that week will make sense if they differ.
