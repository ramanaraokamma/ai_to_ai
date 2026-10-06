# Workbook — Week 25: Embeddings: Geometry for Meaning

**Name:** ________________________________  **Date:** ______________

[⬅ Week 24](week-24.md) · [📖 Read the chapter first](../student-guide/week-25.md) · [Course Home](../README.md) · [Next ➡](week-26.md)

---

> **Rules for this workbook.** Five pages, a Break-It page and a Bug Log. **Write your prediction or your hand answer first, then run.** A guess written after the run is not a guess. Every number in your write-up (page 25.4) must have been printed by **your own** run, with the seed stated.
>
> **There is no language model and no stand-in anywhere in this workbook.** The two "dense" embedders are real but tiny: one is an SVD of a table (no training at all), one is a small PyTorch model trained on **15 notes**. They show a *mechanism*. They say **nothing** about how a pretrained sentence encoder behaves, and none is run here.
>
> **Real numbers.** Every printed number below came from a real CPU run (one thread, the seeds shown). By-hand numbers are plain arithmetic and match exactly. On another scikit-learn or PyTorch build the **last digit** of a score can move, and a recall figure can move by one question (`0.07`). Numbers marked **PRACTICE** are invented for this workbook so they are not the class numbers.
>
> **Files you need.** The files you typed in class: `week25.py`, `hook.py` (for `QA`), `lsa.py` (for `fit_embedder`, `encode`, `search`), `recall.py`, `seeds.py`. Run them in **one Python session**, from the folder that contains `l4lib/`. Pages 25.3 and 25.6 use only the functions in `lsa.py` and four short typed notes of their own. They write one small file, `wb_index.npy`, into your folder: it is yours to delete.
>
> **Calculator.** A square-root key (a phone is fine, airplane mode on). Three decimals; round only the answer.

![Level 4 map: Week 25 highlighted among 36 week tiles in four term lanes](../figures/fig-w25-0-where-this-fits.svg)
*Figure W25.0 — Week 25 sits in the third lane, the term on how models are made and asked; it is the first of the retrieval weeks.*


---

## ✅ Warm-Up (5 min, before anything else)

**W1.** Two vectors point exactly the same way, one twice as long. Their cosine is ____________ (three decimals).

**W2.** A cosine ignores ____________ and keeps only ____________.

**W3.** Circle one. The word table (`TfidfVectorizer()`) scores `optimiser` against `optimizer` as: `1.0` / `0.359` / `0.0` / `-1.0`.

**W4.** An index has 15 notes and you keep 14 directions. Its shape is (____ , ____).

**W5.** Circle one. `fit_transform` is for: the **notes, once** / **every question**.

---

## 📐 Page 25.1 — Cosine Cards, Your Own Numbers (10 min · pen and calculator, no computer)

Four vectors on three axes (**PRACTICE**): `P = [2, 1, 2]`  `Q = [4, 2, 4]`  `R = [1, 2, 2]`  `S = [0, 3, 4]`.

**A.** Dot product `P . R` = (2 x 1) + (1 x 2) + (2 x 2) = ____________

**B.** Lengths: `|P|` = square root of (4 + 1 + 4) = ____________   `|R|` = ____________   `|S|` = ____________

**C.** `cos(P, R)` = ____________ / ( ____________ x ____________ ) = ____________ (three decimals)

**D.** `Q` is `P` doubled. **Without arithmetic**, `cos(P, Q)` = ____________. Why? ______________________________________________

**E.** `cos(R, S)` = ____________ (write the working: dot, both lengths, divide)

**F.** `cos(P, S)` = ____________

**G.** Which of `R` and `S` points nearer to `P` by **cosine**? ________   Which has the bigger **raw dot** with `P`? ________   Did they agree? Yes / No. In one sentence, why not? ______________________________________________

**H.** Now check on the machine, after the `cosine.py` from class has been run in your session (its `length` and `cosine` functions):

```python
# check251.py - needs length() and cosine() from cosine.py, and numpy as np
P = np.array([2.0, 1.0, 2.0]); Q = np.array([4.0, 2.0, 4.0])
R = np.array([1.0, 2.0, 2.0]); S = np.array([0.0, 3.0, 4.0])
print("P.R =", (P * R).sum(), " P.S =", (P * S).sum())
print(f"cos(P,R) = {cosine(P, R):.3f}   cos(P,Q) = {cosine(P, Q):.3f}")
print(f"cos(R,S) = {cosine(R, S):.3f}   cos(P,S) = {cosine(P, S):.3f}")
```

Copy what printed: ______________________________________________

Did every one of your hand answers match? Yes / No. Where did you lose a digit? ______________________________________________

![Three three-number vectors A, B and C with their shapes, the dot product worked out, and a bar for each pair's cosine: 1.000, 0.283 and 0.283](../figures/fig-w25-1-cosine-ignores-length.svg)
*Figure W25.1 — A cosine compares direction and ignores length. B is 2 × A, so cos(A, B) = 1.000; cos(A, C) = 4 ÷ (3.162 × 4.472) = 0.283.*


---

## 🧮 Page 25.2 — Four Notes and a Question (15 min · pen and calculator)

Three axes: `(optimizers, text, money)`. The question is `q = [2, 1, 2]`, length `3`. Four notes (**PRACTICE**):

| note | vector | raw dot with `q` | length | cosine = dot / (length x 3) |
|:--:|:--:|:--:|:--:|:--:|
| D0 | `[6, 8, 0]` | | | |
| D1 | `[0, 5, 12]` | | | |
| D2 | `[4, 4, 2]` | | | |
| D3 | `[1, 0, 1]` | | | |

(Lengths: `D0` is a 6-8-10 triangle. Work out the others; `D3`'s is a square root, three decimals.)

**A.** Winner by **raw dot**: ______   Winner by **cosine**: ______

**B.** Rank all four by raw dot (best first): ______________   by cosine: ______________

**C.** Which note is the **shortest**? ______ Where did it finish in the raw-dot ranking? ______ in the cosine ranking? ______

**D.** One sentence. If a search engine sorted notes by raw dot, which kind of note would it keep putting first? ______________________________________________

**E. Normalise once.** Divide every note by its own length and write the new vector of `D3` (three decimals): `[ ______ , ______ , ______ ]`. Its length is now ______. Predict: the dot of this new `D3` with the raw `q = [2, 1, 2]` is ______ (hint: it is the cosine times `|q|`).

**F.** Why is it fine to leave the **question** un-normalised when you only want the order? ______________________________________________

---

## 🔤 Page 25.3 — Letter Pieces, Then Your Own Index (25 min · pen, then computer)

### Part 1 — Pieces by hand (10 min)

`analyzer="char_wb"` cuts each word into pieces of letters, with a space added at each end of the word. Today use **pieces of exactly 3 letters**. The word `cat` becomes ` ca`, `cat`, `at ` (three pieces; a space counts as a letter).

**A.** The pieces of `cats`: ____________________________  (how many? ____ )

**B.** Pieces that `cat` and `cats` **share**: ____________________________ (how many? ____ )

**C.** Give each word a vector with a `1` for each of its pieces and `0` otherwise, then take the cosine: shared pieces / (square root of pieces in `cat` x square root of pieces in `cats`). `cos(cat, cats)` = ____ / ( ____ x ____ ) = ____________ (three decimals)

**D. PRACTICE.** `colour` and `color`.

| word | its 3-letter pieces | how many |
|:--:|---|:--:|
| `colour` | | |
| `color` | | |

Shared: ____________________________  (____ )   `cos(colour, color)` = ____________

**E.** `banana` shares no piece with `color`. Its cosine with `color` is ____________.

**F.** Check it (this is an experiment on three words, not the class run; `use_idf=False` switches off the "rare words count more" weighting so your by-hand method is exactly right):

```python
# pieces.py - needs numpy as np and TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
words = ["colour", "color", "banana"]
v = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 3), use_idf=False)
X = v.fit_transform(words)
print(list(v.get_feature_names_out()))
print((X @ X.T).toarray().round(3))
```

Copy the matrix row for `colour`: ______________________   Does the `colour`/`color` entry equal your Part 1 D? Yes / No. (If not, did you forget the spaces at the ends?)

**G.** The same words through the plain word table give `colour`/`color` = ____________ because ______________________________________________

### Part 2 — Your own four-note index (15 min)

Type `lsa.py`'s three functions if they are not already in your session, then run this **PRACTICE** block (the notes are invented; yours come next).

```python
# mynotes.py - PRACTICE notes; needs fit_embedder, encode, search from lsa.py
notes = ["the small optimizer kept the loss low after one hundred steps",
         "dropout switched off some units and the loss rose a little",
         "a bigger batch made each step slower but less noisy",
         "the tokeniser split the emoji into four strange pieces"]
vec, svd, M = fit_embedder(notes, 3)
print("index shape:", M.shape)
print("each row against itself:", [round(float(r @ r), 3) for r in M])
for question in ["which optimiser kept the loss low", "what happened to the tokenizer and emoji", "banana bread recipe"]:
    print(question, "->", [(i, round(s, 3)) for i, s in search(vec, svd, M, question, 4)])
np.save("wb_index.npy", M)
M2 = np.load("wb_index.npy")
print("loaded:", M2.shape, " identical:", bool(np.array_equal(M, M2)))
```

```text
index shape: (4, 3)
each row against itself: [1.0, 1.0, 1.0, 1.0]
which optimiser kept the loss low -> [(0, 0.992), (1, 0.694), (3, 0.519), (2, 0.294)]
what happened to the tokenizer and emoji -> [(3, 0.944), (0, 0.671), (1, 0.228), (2, -0.022)]
banana bread recipe -> [(2, 0.999), (0, 0.294), (3, -0.078), (1, -0.154)]
loaded: (4, 3)  identical: True
```

**H.** Why is the second argument `3` and not `4` for four notes? (Say the rule used here: ____ directions for ____ notes, one fewer than the number of notes.) ______________________________________________

**I.** In the first query the word is spelt `optimiser` and the note says `optimizer`. Which note won, and with what score? ______________________________________________

**J.** The nonsense query `banana bread recipe` scored note 2 at `0.999`. Note 2 is about batch size. Is `0.999` a sign the index understood the question? Yes / No. What does this tell you about trusting a top score with **nothing to compare it to**? ______________________________________________

**K. Your own notes.** Write **four notes of your own** (about 3 sentences each) in a `notes` list, run `fit_embedder(notes, 3)`, and write two questions whose answers are in the notes.

| Your question | Note it should find | Where it ranked (1 to 4) | Score |
|---|:--:|:--:|:--:|
| | | | |
| | | | |

One question your index **cannot** answer (no shared letter pieces with any note): ______________________________________________ What did you expect it to return? ______________ What did it return? ______________

Save it with `np.save`, load it back, and print `identical`: ____________

---

## 📏 Page 25.4 — Recall, the Control, and What the Table Does Not Show (20 min)

### Part 1 — Counting recall by hand (5 min)

A system answered ten questions (**PRACTICE**). The right note was at these ranks (1 means first): `1, 3, 2, 1, 5, 1, 4, 2, 1, 9`.

recall@1 = ____ of 10 = ____________   recall@3 = ____ of 10 = ____________

Pure chance with 20 notes: recall@1 = 1 / 20 = ____________; recall@3 = 3 / 20 = ____________.

### Part 2 — Five seeds (**PRACTICE**, by hand)

A trained embedder had recall@1 of `0.60, 0.73, 0.47, 0.67, 0.53` for seeds 0 to 4 (invented). Mean = ____________ (sum first); range = ____________ to ____________. A second embedder scored `0.70` on one run. Is it better than the trained one? Yes / No / Cannot tell. Why? ______________________________________________

### Part 3 — Your table (10 min)

Fill from **your own** `recall.py`, `seeds.py` and `untrained.py` runs (the 15 class notes and `QA`).

| embedder | recall@1 | recall@3 |
|---|:--:|:--:|
| word tf-idf | | |
| LSA dim 2 | | |
| LSA dim 4 | | |
| LSA dim 8 | | |
| LSA dim 14 | | |
| contrastive, seed 0 | | |
| contrastive, mean of 5 seeds | | |
| contrastive after 1 step (control), mean of 5 | | |
| chance (1/15 and 3/15) | | |

Range of the contrastive recall@1 over the five seeds: ________ to ________

**The hook query.** From `headline.py`, for the query `optimiser`: the word table gave the right note a score of ________ and ________ notes shared exactly that score.

### Part 4 — Three sentences

1. About the word table (use the hook query): ______________________________________________
2. Using the word **control** correctly (what did the one-step embedder show about the letter pieces and about the training?): ______________________________________________
3. What the table does **not** show (say how many notes and questions, how many seeds, or which model was never run): ______________________________________________

Rule: a sentence that says one embedder "wins" earns nothing unless it quotes the seed range.

![Paired bars of recall at 1 and at 3 for chance, word table, one-step control, trained embedder and LSA, with the seed range marked](../figures/fig-w25-2-recall-beside-its-control.svg)
*Figure W25.2 — A recall number needs its control. One training step already reaches recall@3 0.73; 150 steps reach 0.89, so training added 0.63 − 0.48 = 0.15 at recall@1.*


---

## 🧩 Page 25.5 — Homework Check: Two More Cosines (5 min)

With `A = [1, 0, 3]`, `C = [4, 2, 0]` and a new `D = [3, 1, 0]`:

`A . D` = ____  `|A|` = ____  `|D|` = ____  `cos(A, D)` = ____________

`C . D` = ____  `|C|` = ____  `cos(C, D)` = ____________

Nearest pair: ____ and ____ .

Check both with `cosine(A, D)` and `cosine(C, D)` from `cosine.py` (define `A`, `C`, `D` first): I got ____________ and ____________.

**Extension (for the fast).** Run `pairs.py`. Six typed pairs did not raise the recall. Write **one** thing you would test to find out why (not what you think the answer is): ______________________________________________

---

## 🐞 Page 25.6 — Break It on Purpose (three bugs · 25 min)

**Each block below is DELIBERATELY broken.** Run it after Page 25.3's `mynotes.py` in the same session. For each bug: **(i)** write what you expect to see, **(ii)** run, **(iii)** name the bug in one line, **(iv)** write the fix and a check that would catch it.

### 25.6-A (SILENT) — the rows were never made length 1

```python
# DELIBERATE BUG 25.6-A (SILENT): the rows are the SVD's raw output, never divided by their own length.
raw = svd.transform(vec.transform(notes))
print("a note against itself (should be 1.000):", [round(float(r @ r), 2) for r in raw])
question = "which optimiser kept the loss low"
qv = svd.transform(vec.transform([question]))[0]
print("raw scores :", np.round(raw @ qv, 3))
print("best note  :", int(np.argmax(raw @ qv)))
```

(i) I expect: ______________________________________________
(ii) The best note is right. So what is wrong? ______________________________________________
(iii) Bug: ______________________________________________
(iv) Fix and a one-line check: ______________________________________________

### 25.6-B (loud) — the question given to `fit_transform`

```python
# DELIBERATE BUG 25.6-B (loud): the question is given to fit_transform, which re-learns the columns from one sentence.
q_bad = vec.fit_transform([question])
print("columns now:", q_bad.shape[1])
print(svd.transform(q_bad))
```

(i) I expect: ______________________________________________
(ii) Last line of the error, copied: ______________________________________________
(iii) Bug: ______________________________________________
(iv) Fix: ______________________________________________  **Side effect:** this block replaced `vec` in your session. What must you run to put it back? ______________________________________________

### 25.6-C (SILENT) — an index from one set of notes, an encoder fitted on another

```python
# DELIBERATE BUG 25.6-C (SILENT): the index was built from the notes; the encoder was re-fitted on an edited copy.
vec, svd, M = fit_embedder(notes, 3)
exam = [("which optimiser kept the loss low", 0), ("what happened to the tokenizer and emoji", 3),
        ("why did dropout change the loss", 1), ("is a big batch noisy", 2)]
def right_count(v, s, index):
    return sum(int(np.argmax(index @ encode(v, s, [qq])[0])) == g for qq, g in exam)
print("matched encoder   :", right_count(vec, svd, M), "of 4")
edited = [n.replace("the ", "") for n in notes]
vec_e, svd_e, _ = fit_embedder(edited, 3)
print("mismatched encoder:", right_count(vec_e, svd_e, M), "of 4")
```

(i) I expect: ______________________________________________
(ii) Did any line of the run complain? Yes / No. Why do the shapes still fit? ______________________________________________
(iii) Bug: ______________________________________________
(iv) Fix, and the check you would run after any rebuild: ______________________________________________

---

## 📓 Page 25.7 — The Bug Log

Add **at least two** entries to your running Bug Log (one must be a SILENT one). Use the usual columns.

| # | File / page | What I saw | What it meant | The fix | How I would catch it next time |
|:--:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Bug Log Entry 3** should name the self-cosine (`0.48`, `0.77`, `0.94`, `0.93`) or the `4 of 4` against `2 of 4`.

---

## 🧠 Self-Check (from memory, no notes)

1. Why does a raw dot product favour long vectors, and what one step stops it? ______________________________________________
2. Why are `optimiser` and `optimizer` unrelated to the word table, and what cut makes them related? ______________________________________________
3. What does `np.save` save, and what does it **not** save that you need to search? ______________________________________________
4. What does `nn.EmbeddingBag` do that `nn.Embedding` does not, and what is the "starts" list for? ______________________________________________
5. In one sentence: the idea of contrastive training. ______________________________________________
6. Why is a single training run not a result? ______________________________________________

---

# ✂️ ANSWERS - keep this page folded until you have finished

### Warm-Up

W1. `1.000`. W2. **length**; **direction**. W3. `0.0`. W4. `(15, 14)`. W5. the **notes, once**: a question only ever gets `transform`.

### Page 25.1

A. `8`. B. `3`; `3`; `5`. C. `8 / (3 x 3) = 0.889`. D. `1.000`: `Q` is `P` doubled, it points the same way, the lengths cancel. E. `R . S = 0 + 6 + 8 = 14`; `14 / (3 x 5) = 0.933`. F. `P . S = 0 + 3 + 8 = 11`; `11 / (3 x 5) = 0.733`.
G. By **cosine** `R` is nearer to `P` (`0.889` against `0.733`). By **raw dot** `S` is bigger (`11` against `8`). They disagree: `S` is longer (5 against 3), and the raw dot rewards length.
H. **Output:**

```text
P.R = 8.0  P.S = 11.0
cos(P,R) = 0.889   cos(P,Q) = 1.000
cos(R,S) = 0.933   cos(P,S) = 0.733
```

### Page 25.2

| note | vector | raw dot | length | cosine |
|:--:|:--:|:--:|:--:|:--:|
| D0 | `[6, 8, 0]` | `20` | `10` | `0.667` |
| D1 | `[0, 5, 12]` | `29` | `13` | `0.744` |
| D2 | `[4, 4, 2]` | `16` | `6` | `0.889` |
| D3 | `[1, 0, 1]` | `4` | `1.414` | `0.943` |

A. Raw dot: **D1** (`29`). Cosine: **D3** (`0.943`). B. Raw dot: D1, D0, D2, D3. Cosine: D3, D2, D1, D0. C. `D3`; **last** by raw dot, **first** by cosine. D. **Long** notes (any sentence that names length). E. `D3 / 1.414 = [0.707, 0, 0.707]`, length `1.000`; its dot with `q` is `0.943 x 3 = 2.828`. F. Every score is the cosine multiplied by the same number, `|q|`, so the **order** is unchanged (the scores are not cosines any more, so do not compare them with a threshold).

### Page 25.3

**Part 1.** A. ` ca`, `cat`, `ats`, `ts ` (4). B. ` ca`, `cat` (2). C. `2 / (sqrt(3) x sqrt(4)) = 2 / 3.464 = 0.577`. D. `colour`: ` co`, `col`, `olo`, `lou`, `our`, `ur ` (6). `color`: ` co`, `col`, `olo`, `lor`, `or ` (5). Shared: ` co`, `col`, `olo` (3). `3 / sqrt(30) = 3 / 5.477 = 0.548`. E. `0.000`.
F. **Output:**

```text
[' ba', ' co', 'ana', 'ban', 'col', 'lor', 'lou', 'na ', 'nan', 'olo', 'or ', 'our', 'ur ']
[[1.    0.548 0.   ]
 [0.548 1.    0.   ]
 [0.    0.    1.   ]]
```

G. `0.0`: `colour` and `color` are two different whole words, two different columns, with nothing in common (for the class words the plain table gave `optimizer`/`optimiser` `0.0`, and the letter-piece table `0.359`).

**Part 2.** H. The rule used here is **14** directions for **15** notes, so for four notes `3` (`N - 1`). (Asking for all `4` also runs and keeps everything, `1.000` of the spread, so nothing is squeezed; `N - 1` makes sure at least one direction is dropped.) I. Note `0`, the optimizer note, at `0.992`: it shares most letter pieces even with the different spelling. J. **No.** A top score of `0.999` for `banana bread recipe` means the query happened to land near note 2 in a space with only 3 directions; it tells you nothing about understanding. A top score needs something to compare it to (a threshold tested on questions you know have no answer, which is Week 26). K. No fixed answer: check the rank is reported, the failing question is honestly named, and `identical` is `True`.

### Page 25.4

**Part 1.** recall@1 = `4` of 10 = `0.40` (ranks of 1: four of them). recall@3 = `7` of 10 = `0.70` (ranks `1, 3, 2, 1, 1, 2, 1`). Chance: `0.05`; `0.15`.
**Part 2.** Sum `3.00`, mean `0.60`; range `0.47` to `0.73`. **Cannot tell**: `0.70` is inside the range of the trained one over five seeds, and one run is one seed.
**Part 3** (your run should match to within one question; these are the class numbers):

| embedder | recall@1 | recall@3 |
|---|:--:|:--:|
| word tf-idf | `0.67` | `0.73` |
| LSA dim 2 | `0.13` | `0.27` |
| LSA dim 4 | `0.53` | `0.73` |
| LSA dim 8 | `0.67` | `0.87` |
| LSA dim 14 | `0.73` | `1.00` |
| contrastive, seed 0 | `0.67` | `0.87` |
| contrastive, mean of 5 seeds | `0.63` | `0.89` |
| contrastive after 1 step (control), mean of 5 | `0.48` | `0.73` |
| chance | `0.07` | `0.20` |

Seed range of recall@1: `0.47` to `0.73`. Hook query `optimiser`: the word table gave the right note `0.000` and **15** notes shared exactly that score (so "rank 1" is only the list order).
**Part 4.** Full marks if: (1) says the word table scores `0.000` on the hook query (or has no geometry); (2) uses *control* correctly, for example "the one-step control already gets recall@3 of `0.73`, so most of the gain is the letter pieces; training adds about `0.15`"; (3) says the table is for 15 notes and 15 questions, or one seed is not a result, or no pretrained encoder was run. Any claim that one embedder wins needs the seed range.

### Page 25.5

`A . D = 3`, `|A| = 3.162`, `|D| = 3.162`, `cos(A, D) = 3 / 10 = 0.300`. `C . D = 14`, `|C| = 4.472`, `cos(C, D) = 14 / 14.142 = 0.990`. Nearest pair: **C and D**. Machine: `0.300` and `0.990`. Extension: any test, not a conclusion (for example, type twenty pairs, or use different pair phrases, and run five seeds each).

### Page 25.6

**25.6-A.** (i) Anything; the honest answer is "I expect it to work, the best note is right". (ii) The best note is right, but the scores are not cosines. (iii) The rows were never made length 1 (no `normalize`), so `M @ q` is a dot product, not a cosine, and short rows score low for no reason. (iv) `normalize(svd.fit_transform(X))`, in one place; the check is that every row against itself is `1.000`. **Output:**

```text
a note against itself (should be 1.000): [0.48, 0.77, 0.94, 0.93]
raw scores : [0.32  0.285 0.134 0.234]
best note  : 0
```

The catch: a raw score of `0.32` for the right note would fail any threshold like `0.5`, though the cosine is `0.992`.

**25.6-B.** (ii) `ValueError: X has 65 features, but TruncatedSVD is expecting 387 features as input.` (iii) `fit_transform` on the question forgot the 387 columns learned from the notes and learned 65 new ones. (iv) `vec.transform([question])`. **Side effect:** `vec` is now fitted on one sentence; re-run `vec, svd, M = fit_embedder(notes, 3)`. **Output:**

```text
columns now: 65
ValueError: X has 65 features, but TruncatedSVD is expecting 387 features as input.
```

(The real traceback has several lines above the last one.) The catch: `fit` is for the notes, once; a question only gets `transform`.

**25.6-C.** (ii) No line complained: the index has 3 numbers per note and the encoder makes 3 numbers per question, so the shapes fit; but the two encoders learned different letter pieces from different text, so the 3 numbers mean different things. (iii) The saved index and the encoder came from different versions of the notes. (iv) Rebuild everything (vectorizer, SVD, matrix) from the same list in one function, every time; after any rebuild, re-run a sanity question and compare with the result it gave before. **Output:**

```text
matched encoder   : 4 of 4
mismatched encoder: 2 of 4
```

On four questions the drop is big; on real notes it was from `0.73` to `0.07` (class `recall@1`). The catch: nothing complains, so only a before-and-after score tells you.

### Page 25.7 and Self-Check

**Bug Log Entry 3:** the self-cosines `0.48`, `0.77`, `0.94`, `0.93` (25.6-A) or `4 of 4` against `2 of 4` (25.6-C). **Self-Check:** 1. A long vector gets a big dot just by being long; dividing every row by its own length once (**normalise once**). 2. They are two different columns (different whole words); cutting into letter pieces, which they largely share. 3. The matrix of numbers; **not** the vectorizer or the SVD (you need those to encode a question). 4. It looks up rows **and** averages them in one call; the starts say where each document begins in the one long list of ids. 5. Two halves of the same note should land nearer than halves of different notes. 6. One seed is an anecdote: the recall moved from `0.47` to `0.73` across five seeds of the same code.
