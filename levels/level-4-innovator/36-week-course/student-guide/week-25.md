# Week 25 — Embeddings: Geometry for Meaning

[⬅ Week 24](week-24.md) · [Course Home](../README.md) · [Week 26 ➡](week-26.md) · [Workbook](../workbook/week-25.md)

---

> ### This week in one sentence
> **A word table has no idea that two spellings of one word are "near", so you cut words into letter pieces, squeeze the table with SVD or train a tiny model so that similar notes land close together, build a search that is one matrix multiply, and measure how much of the gain is the training and how much is just the letter pieces.**
>
> **By the end of this chapter you will be able to:**
> - **Compute a cosine by hand** for three 3-number arrows and say what a cosine ignores
> - **Show why a word table has no geometry** (`optimiser` scores `0.000` against a note titled `Optimizer`) and how letter pieces fix it
> - **Build a whole search index in a dozen lines**: letter pieces, `TruncatedSVD`, normalise once, one matrix multiply, `np.argsort`
> - **Save the index with `np.save`**, load it back identical, and say what the file does *not* contain
> - **Say what `nn.EmbeddingBag` is**, and say the one idea of contrastive training in a sentence
> - **Fill a recall table and write a sentence with the word "control" in it**
>
> **New maths:** **none.** Cosine is Level 3 Week 32; SVD is Level 3 Week 29's PCA idea applied to Week 32's TF-IDF. You re-do a cosine by hand so that you can see it.
>
> **New syntax:** `TruncatedSVD(n_components=...)` · `TfidfVectorizer(analyzer="char_wb")` · `np.save` / `np.load` · `nn.EmbeddingBag`
>
> **New words:** embedding · dense / sparse · character n-gram (letter piece) · SVD / latent dimension · LSA · index · normalise once · contrastive training · positive pair · recall@k
>
> **Reading time:** about 35 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 55 minutes (25 with a pen and calculator, 30 at the computer).

> **📌 About the code blocks.** Twelve small files, each a whole file with its name in the first line. **Run them in order, in one Python session, from the folder that contains `l4lib/`** (`python3 -i`, or `exec(open("name.py").read())` one after another), because later files use names made by earlier ones. If you see `ModuleNotFoundError: No module named 'l4lib'`, you are in the wrong folder. `week25.py` imports `l4lib`'s `rag` module: **import it, never copy it.** Every output shown was printed by a real run on a CPU, with the seeds in the files, so your numbers should match (a different scikit-learn or PyTorch build can move the last digit of a score, and a recall figure by one question, `0.07`; `seconds` lines vary). `np.save` writes one small file, `notebook_index.npy`, into your folder. **Nothing needs the internet. There is no language model and no stand-in anywhere this week.** The two "dense" embedders are real but tiny: one is an SVD of a table (no training at all), one is a small PyTorch model trained for 150 steps on **15 notes**. They show a *mechanism*; **they say nothing about how a pretrained sentence encoder behaves**, and none is run here.

![Level 4 map: Week 25 highlighted among 36 week tiles in four term lanes](../figures/fig-w25-0-where-this-fits.svg)
*Figure 25.0 — Week 25 sits in the third lane, the term on how models are made and asked; it is the first of the retrieval weeks.*


---

## 🪝 Start Here

You have a lab notebook of 15 notes (it ships inside `l4lib`, and it is written as if by you, about this course's own experiments). Note 0 is called *Optimizer bake-off*. You will ask it twice.

Before you type anything, write three guesses on a card.

1. Ask for `optimizer` and the right note scores a little above zero. Ask for `optimiser` (the other spelling). Will the right note score **higher**, **lower**, or **the same**?
2. You cut `optimizer` and `optimiser` into pieces of 3 to 5 letters. Out of `0` (nothing in common) to `1` (identical), what cosine do you expect between the two words? Write a number.
3. An embedder is trained for 150 steps and looks better than the word table. What is the one experiment you would run before saying "training made it better"?

Keep the card. We come back to it at the end.

### The notebook that cannot spell

Type this file and run it. It defines the 15 questions that the rest of the week measures against, and it builds the word table you already know from Level 3 Week 32.

**`week25.py`**

```python
# week25.py - Week 25. Run every block in order, in ONE session, from the folder that contains l4lib/.
import time
import numpy as np
import torch
import torch.nn as nn
torch.set_num_threads(1)
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from l4lib import rag

chunks = rag.notebook_chunks()
titles = rag.notebook_titles(chunks)
print(len(chunks), "notes")
print("note 0:", titles[0])
print("note 11:", titles[11])
```

```text
15 notes
note 0: 2026-01-14 - Optimizer bake-off
note 11: 2026-06-25 - Reward model toy
```

**`hook.py`**

```python
# hook.py - the notebook, 15 questions with their answers, and the word-table index (Level 3's TF-IDF, behind l4lib's one interface)
QA = [("which optimiser should I start with", 0),
      ("what made the loss blow up to not-a-number", 1),
      ("does randomly switching off units help", 2),
      ("why do names come out as junk when sampling hot", 3),
      ("which gated recurrent net was quicker to train", 4),
      ("why divide the scores by a square root", 5),
      ("how many layers did the small transformer have", 6),
      ("what happens if the model has no idea of order", 7),
      ("does a bigger batch hurt generalisation", 8),
      ("where should normalisation go in a block", 9),
      ("does the tokeniser handle emoji", 10),
      ("what is the cheapest way to raise the reward", 11),
      ("why did the policy collapse", 12),
      ("why did the constant guess matter", 13),
      ("how much does a call cost in dollars", 14)]

tfidf_ix = rag.VectorIndex(chunks, rag.TfidfEmbedder())
print("word columns:", tfidf_ix.M.shape[1], " (so each note is a row of", tfidf_ix.M.shape[1], "numbers)")
for query in ["optimizer", "optimiser"]:
    hits = tfidf_ix.search(query, k=3)
    print(f"query {query!r}:", [(h.id, round(h.score, 3)) for h in hits])
```

```text
word columns: 288  (so each note is a row of 288 numbers)
query 'optimizer': [(0, 0.131), (1, 0.0), (2, 0.0)]
query 'optimiser': [(0, 0.0), (1, 0.0), (2, 0.0)]
```

Look at the last line. **`optimiser` scores `0.0` on the right note.** It also scores `0.0` on all 14 others. To the word table `optimiser` and `optimizer` are two different columns, exactly as different as `optimiser` and `banana`. There is no idea of *near*. Today you build one.

> **near = similar.** That is the whole week.

---

## 🧠 The Big Idea

A note is a row of numbers, so a note is an arrow. Two arrows that point roughly the same way should be two notes about roughly the same thing. That needs three things:

1. **Numbers for a note where near-spellings share something.** Cut each word into **letter pieces** (a **character n-gram**: a run of 3, 4 or 5 letters inside a word). `optimizer` and `optimiser` share most of their pieces.
2. **A squeeze.** The piece table is huge and mostly empty (**sparse**). An **SVD** keeps the best few directions and gives every note a short row of numbers (**dense**). Doing this to a text table is called **LSA**. The short row is an **embedding**. Or, instead of squeezing, you can **train** a small model to make the embedding (contrastive training, section 4).
3. **A way to search.** Make every row length 1 **once**, and then searching is one matrix multiply. The finished table of rows is an **index**.

And one rule for the whole week: **a number is only a result if you ran a control.** Section 5 is the control.

### Cosine, by hand

The **cosine** of two arrows is **what they share, divided by how long they are**. Take `A = [1, 0, 3]`, `B = [2, 0, 6]`, `C = [4, 2, 0]`.

- What they share: multiply the matching numbers and add. `A · C = 1x4 + 0x2 + 3x0 = 4`.
- How long: `|A| = sqrt(1 + 0 + 9)`, `|C| = sqrt(16 + 4 + 0)`.
- Divide: `cos(A, C) = 4 / (|A| x |C|)`.

Do the two square roots and the division on your calculator before you run anything. Then also guess `cos(A, B)` without any arithmetic (look at `B` and `A` side by side). Then type this.

**`cosine.py`**

```python
# cosine.py
A = np.array([1.0, 0.0, 3.0])
B = np.array([2.0, 0.0, 6.0])
C = np.array([4.0, 2.0, 0.0])

def length(v):
    return float(np.sqrt((v * v).sum()))

def cosine(x, y):
    return float((x * y).sum() / (length(x) * length(y)))

print("A.C =", (A * C).sum(), "  |A| =", round(length(A), 3), "  |C| =", round(length(C), 3))
print(f"cos(A,B) = {cosine(A, B):.3f}")
print(f"cos(A,C) = {cosine(A, C):.3f}")
print(f"cos(B,C) = {cosine(B, C):.3f}")

V = np.array([A, B, C])
U = normalize(V)
print("lengths after normalise:", [round(length(u), 3) for u in U])
G = U @ U.T
for row in G:
    print("  ".join(f"{x:.3f}" for x in row))
```

```text
A.C = 4.0   |A| = 3.162   |C| = 4.472
cos(A,B) = 1.000
cos(A,C) = 0.283
cos(B,C) = 0.283
lengths after normalise: [1.0, 1.0, 1.0]
1.000  1.000  0.283
1.000  1.000  0.283
0.283  0.283  1.000
```

A cosine of `1.000` means the arrows point exactly the same way. `0` would be a right angle. **A cosine ignores length**, which is what you want for text: a long note and a short note on one topic should score alike.

The last three lines use `normalize` (from `sklearn.preprocessing`, Level 3 Week 32): every row divided by its own length. Then `U @ U.T` is every pair's cosine in one matrix multiply. **That is the trick the whole index uses.**

> **The trap of the raw dot product.** If you skip the division and only multiply and add, a long arrow can beat a short one that points better. You will see it with your own pen on workbook page 25.2.

![Three three-number vectors A, B and C with their shapes, the dot product worked out, and a bar for each pair's cosine: 1.000, 0.283 and 0.283](../figures/fig-w25-1-cosine-ignores-length.svg)
*Figure 25.1 — A cosine compares direction and ignores length. B is 2 × A, so cos(A, B) = 1.000; cos(A, C) = 4 ÷ (3.162 × 4.472) = 0.283.*


---

## 🔤 Letter Pieces

Here is the first new construct. You know `TfidfVectorizer()`: one column per whole word. `analyzer="char_wb"` changes what a column *is*: a run of letters inside a word, with a space added at each end of the word (`wb` is "word boundary"). So `opt` inside a word and ` opt` at the start of a word are different columns. `ngram_range=(3, 5)` means pieces of 3, 4 and 5 letters.

**Predict first:** what cosine will the letter-piece table give `optimizer` and `optimiser`? Most people say `0.9`. Write your number, then run.

**`spelling.py`**

```python
# spelling.py
words = ["optimizer", "optimiser", "optimise", "banana"]

word_vec = TfidfVectorizer()                       # Level 3's: one column per whole word
W = word_vec.fit_transform(words)
print("word columns:", list(word_vec.get_feature_names_out()))
print("word-level cosine, optimizer vs optimiser:", round(float((W[0] @ W[1].T).toarray()[0, 0]), 3))

char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))     # NEW: columns are letter pieces
Cc = char_vec.fit_transform(words)
print("char columns:", len(char_vec.get_feature_names_out()))
print("some pieces of 'optimiser':", [g for g in char_vec.get_feature_names_out() if g.strip() in ("opt", "opti", "optim", "iser", "ser")])
Cn = normalize(Cc)
S = (Cn @ Cn.T).toarray()
for a, row in zip(words, S):
    print(f"{a:>10}", "  ".join(f"{x:.3f}" for x in row))
```

```text
word columns: ['banana', 'optimise', 'optimiser', 'optimizer']
word-level cosine, optimizer vs optimiser: 0.0
char columns: 52
some pieces of 'optimiser': [' opt', ' opti', 'iser', 'iser ', 'opt', 'opti', 'optim', 'ser', 'ser ']
 optimizer 1.000  0.359  0.353  0.000
 optimiser 0.359  1.000  0.670  0.000
  optimise 0.353  0.670  1.000  0.000
    banana 0.000  0.000  0.000  1.000
```

`0.0` against `0.359`. The two spellings now share columns. It is not bigger because the pieces around the `z` and the `s` differ and there are many pieces. `optimise` and `optimiser` share far more (`0.670`). And `banana` stays at `0.000`: the geometry is real, not just everything being nudged together.

---

## 🧱 The Index: Fit, Encode, Search

Now the main file. Three small functions and a search. Read `fit_embedder` slowly: it is the whole idea.

- `vec.fit_transform(docs)` learns the columns **and** gives the big table.
- `TruncatedSVD(n_components=dim)` is the second new construct. Level 3 Week 29's PCA found the direction in which data is most spread out. `TruncatedSVD(n)` does the same job on a big mostly-empty table and **keeps the best `n` directions**. `random_state=0` is a seed, because the algorithm starts from random numbers.
- `normalize(...)` makes every row length 1, **once**, here.
- A query only gets `transform`, never `fit_transform`. **`fit` is for the notes, once. A query only ever gets `transform`.**
- `np.argsort(-sims)[:k]` (Level 3 Week 33) gives the positions of the `k` biggest scores. The minus turns "smallest first" into "biggest first".

**`lsa.py`**

```python
# lsa.py
def fit_embedder(docs, dim):
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)
    X = vec.fit_transform(docs)
    svd = TruncatedSVD(n_components=dim, random_state=0)
    M = normalize(svd.fit_transform(X))            # normalise ONCE, here
    return vec, svd, M

def encode(vec, svd, texts):
    return normalize(svd.transform(vec.transform(texts)))

def search(vec, svd, M, query, k=3):
    q = encode(vec, svd, [query])[0]
    sims = M @ q
    order = np.argsort(-sims)[:k]
    return [(int(i), float(sims[i])) for i in order]

t0 = time.time()
vec, svd, M = fit_embedder(chunks, 14)
print("tf-idf matrix:", vec.transform(chunks).shape, " index:", M.shape, " seconds:", round(time.time() - t0, 2))
print("share of the spread kept:", round(float(svd.explained_variance_ratio_.sum()), 3))

q = "which optimiser was best"
print("query:", q)
for i, s in search(vec, svd, M, q):
    print(f"  {s:.3f}  [{i}] {titles[i]}")
```

```text
tf-idf matrix: (15, 3906)  index: (15, 14)  seconds: 0.04
share of the spread kept: 0.941
query: which optimiser was best
  0.565  [1] 2026-01-21 - Learning rate sweep
  0.525  [0] 2026-01-14 - Optimizer bake-off
  0.482  [2] 2026-02-03 - Dropout and weight decay
```

The table went from `(15, 3906)` to `(15, 14)` and kept `0.941` of the spread. **The right note (`[0]`) came second.** The first was "Learning rate sweep", which also contains the word `best`. Do not fix it: a ranking error is a reason to ask *what was shared*, not evidence of a bug. The rest of the week measures how often this happens.

> **Why 14 and not 15?** A table of 15 notes has at most 15 directions, and asking for all 15 keeps everything (`1.000` of the spread), so nothing is squeezed. `l4lib` stops at one fewer than the number of notes (14), so at least one direction is dropped. "14 numbers per note" is not much compression; it is mostly a change of axes.

### Save it, and load it back

The third construct: `np.save("name.npy", array)` writes **one array** to one file, and `np.load("name.npy")` brings it back exactly. Predict before you run: what will `np.save` *not* contain that you need to search the file later?

**`index.py`**

```python
# index.py - the hand-built index against the library's, then save and load
lib = rag.VectorIndex(chunks, rag.TinyDenseEmbedder("lsa", dim=14))
mine = [i for i, s in search(vec, svd, M, q, k=15)]
theirs = [h.id for h in lib.search(q, k=15)]
print("same ranking as l4lib's lsa tier:", mine == theirs)
print("same matrix:", bool(np.allclose(M, lib.M)))

np.save("notebook_index.npy", M)
M2 = np.load("notebook_index.npy")
print("loaded back:", M2.shape, M2.dtype, M2.nbytes, "bytes of numbers; identical:", bool(np.array_equal(M, M2)))
print("the 15 x 3906 letter-piece table, stored densely, would be", 15 * 3906 * 8, "bytes")
print("search with the loaded matrix:", [i for i, s in search(vec, svd, M2, q)])
```

```text
same ranking as l4lib's lsa tier: True
same matrix: True
loaded back: (15, 14) float64 1680 bytes of numbers; identical: True
the 15 x 3906 letter-piece table, stored densely, would be 468720 bytes
search with the loaded matrix: [1, 0, 2]
```

The hand-built index matches `l4lib`'s. The saved file is 1,680 bytes of numbers. **It holds only the numbers.** It does not hold the vectorizer or the SVD that made them, so a question must still go through the *same fitted* `vec` and `svd` that built the matrix.

---

## 🏋️ The Trained Embedder

The fourth construct. You know `nn.Embedding` (Week 8): an id goes in, a row of numbers comes out. **`nn.EmbeddingBag`** takes a *bag* of ids and returns the **mean** of their rows in one call. A batch of documents is handed over as one long list of ids, plus a list of **starts** saying where each document begins. The ids `[0, 1, 2, 3, 4]` with starts `[0, 3]` are the two documents `[0, 1, 2]` and `[3, 4]`. Predict the output shape before you run.

**`bag.py`**

```python
# bag.py - nn.EmbeddingBag: a lookup table that also averages
torch.manual_seed(0)
bag = nn.EmbeddingBag(6, 3, mode="mean")          # 6 piece ids, 3 numbers each; the mean of the rows asked for
ids = torch.tensor([0, 1, 2,   3, 4])             # two documents laid end to end: [0, 1, 2] and [3, 4]
starts = torch.tensor([0, 3])                     # where each document begins in that long list
out = bag(ids, starts)
print("shape:", tuple(out.shape), "  (one row per document)")

by_hand = torch.stack([bag.weight[torch.tensor([0, 1, 2])].mean(dim=0),
                       bag.weight[torch.tensor([3, 4])].mean(dim=0)])      # pick the rows, then average them yourself
print("same as picking the rows and averaging:", bool(torch.allclose(out, by_hand)))
print(np.round(out.detach().numpy(), 3))
```

```text
shape: (2, 3)   (one row per document)
same as picking the rows and averaging: True
[[-0.225  0.433 -0.173]
 [ 0.616  0.706  0.565]]
```

In the trained embedder each document is a bag of letter pieces, and the row for the note is built from the rows for its pieces. What gets trained is those rows.

### The one idea of contrastive training

Open `l4lib/rag.py` with your teacher at the `TinyDenseEmbedder` class and read the training loop. Do not type it. In three sentences:

> Make two halves of every note. Embed all the first halves and all the second halves. Push each first half's cosine with **its own** second half up, and with every other note's second half down. That is the whole loss.

Two halves of the same note are a **positive pair**. The loss is small when a half finds its own other half among all 15 notes. If a model knew nothing, it would give every note a `1/15` chance, and the first-step loss would be about `ln 15 = 2.708`.

**`contrastive.py`**

```python
# contrastive.py - the trained tier, from l4lib (the loop is in l4lib/rag.py; you read it with your teacher)
t0 = time.time()
cem = rag.TinyDenseEmbedder("contrastive", dim=32, seed=0)
cix = rag.VectorIndex(chunks, cem)
print("seconds to train on the 15 notes:", round(time.time() - t0, 1))
print("steps:", len(cem.loss_history), " loss at step 0, 10, 50, 149:",
      [round(cem.loss_history[i], 3) for i in (0, 10, 50, 149)])
print("first-step loss if it knew nothing (ln of 15 notes):", round(float(np.log(15)), 3))
print(f"recall@1 {rag.recall_at_k(cix, QA, 1):.2f}   recall@3 {rag.recall_at_k(cix, QA, 3):.2f}")
```

```text
seconds to train on the 15 notes: 0.9
steps: 150  loss at step 0, 10, 50, 149: [1.755, 0.004, 0.002, 0.002]
first-step loss if it knew nothing (ln of 15 notes): 2.708
recall@1 0.67   recall@3 0.87
```

The loss went from `1.755` to `0.004` by step 10 and barely moved after. **Did it learn English?** Look at step 10 against step 149: it was already finished at step 10. It learned to tell these 15 notes from their own halves. A loss of `0.002` says nothing about text it has never seen.

---

## 📏 Measuring: recall@k

**recall@k** is the share of questions whose right note is in the top `k`. You have 15 questions in `QA`, each with its one right note. Chance for recall@1 is `1/15 = 0.07`; for recall@3 it is `3/15 = 0.20`. **One question is worth `0.067`**, so a gap of one question is not a result.

**`recall.py`**

```python
# recall.py - recall@1 and recall@3 of every embedder on the 15 questions in hook.py

def recall_with(embedder, M_, k):
    # the same measurement as rag.recall_at_k, for an embedder and a matrix you already have
    hit = 0
    for question, gold in QA:
        sims = M_ @ embedder.encode([question])[0]
        hit += gold in list(np.argsort(-sims)[:k])
    return hit / len(QA)

print(f"{'embedder':<22}{'recall@1':>9}{'recall@3':>9}")
print(f"{'word tf-idf':<22}{rag.recall_at_k(tfidf_ix, QA, 1):>9.2f}{rag.recall_at_k(tfidf_ix, QA, 3):>9.2f}")
for d in (2, 4, 8, 14):
    ix = rag.VectorIndex(chunks, rag.TinyDenseEmbedder("lsa", dim=d))
    print(f"{'lsa, dim ' + str(d):<22}{rag.recall_at_k(ix, QA, 1):>9.2f}{rag.recall_at_k(ix, QA, 3):>9.2f}")
```

```text
embedder               recall@1 recall@3
word tf-idf                0.67     0.73
lsa, dim 2                 0.13     0.27
lsa, dim 4                 0.53     0.73
lsa, dim 8                 0.67     0.87
lsa, dim 14                0.73     1.00
```

Read the table aloud, row by row. Dimension 2 squeezes hardest, and it is the worst.

### The query the word table cannot hear

**`headline.py`**

```python
# headline.py - the query the word table cannot hear, and where each embedder puts the right note
lsa_ix = rag.VectorIndex(chunks, rag.TinyDenseEmbedder("lsa", dim=14))
for query in ["optimiser", "which optimiser was best"]:
    print("query:", query)
    for name, ix in [("word tf-idf", tfidf_ix), ("lsa (14 numbers)", lsa_ix), ("contrastive (seed 0)", cix)]:
        hits = ix.search(query, k=len(chunks))                 # all 15, best first
        right = [h for h in hits if h.id == 0][0]              # note 0, the optimizer note
        tied = sum(h.score == right.score for h in hits)       # how many notes share exactly its score
        rank = [h.id for h in hits].index(0) + 1
        print(f"  {name:<22} right note scores {right.score:.3f}; rank {rank:>2}; notes with exactly that score: {tied}")
```

```text
query: optimiser
  word tf-idf            right note scores 0.000; rank  1; notes with exactly that score: 15
  lsa (14 numbers)       right note scores 0.799; rank  1; notes with exactly that score: 1
  contrastive (seed 0)   right note scores 0.429; rank  1; notes with exactly that score: 1
query: which optimiser was best
  word tf-idf            right note scores 0.000; rank  2; notes with exactly that score: 14
  lsa (14 numbers)       right note scores 0.525; rank  2; notes with exactly that score: 1
  contrastive (seed 0)   right note scores 0.377; rank  1; notes with exactly that score: 1
```

**Read the tie carefully.** For `optimiser` the word table gives the right note `0.000` *and gives the same `0.000` to all 14 others*. Its "rank 1" is only list order (ties go to the earlier note). It is not a success. The last column is the sentence that matters: **15 notes share exactly that score.**

### One seed is an anecdote

The trained tier starts from random numbers. Before you run the next file, predict the range of recall@1 across five seeds.

**`seeds.py`**

```python
# seeds.py - one seed is an anecdote: five seeds of the contrastive tier, and the lsa tier beside them
print(f"{'seed':<6}{'loss@0':>8}{'loss@149':>10}{'recall@1':>10}{'recall@3':>10}")
r1s, r3s = [], []
for s in range(5):
    e = rag.TinyDenseEmbedder("contrastive", dim=32, seed=s)
    ix = rag.VectorIndex(chunks, e)
    r1, r3 = rag.recall_at_k(ix, QA, 1), rag.recall_at_k(ix, QA, 3)
    r1s.append(r1); r3s.append(r3)
    print(f"{s:<6}{e.loss_history[0]:>8.2f}{e.loss_history[-1]:>10.3f}{r1:>10.2f}{r3:>10.2f}")
print(f"mean  {'':>18}{np.mean(r1s):>10.2f}{np.mean(r3s):>10.2f}   (range of recall@1: {min(r1s):.2f} to {max(r1s):.2f})")
```

```text
seed    loss@0  loss@149  recall@1  recall@3
0         1.75     0.002      0.67      0.87
1         3.54     0.001      0.73      0.87
2         2.29     0.001      0.60      0.93
3         3.16     0.001      0.67      0.93
4         1.57     0.001      0.47      0.87
mean                          0.63      0.89   (range of recall@1: 0.47 to 0.73)
```

The loss ends near `0.001` or `0.002` for *every* seed, including the one with recall@1 `0.47`. **A low loss is not a good embedder.**

### The control

The trained tier looks better than the word table at recall@3. But how much of that is the training, and how much is just the letter pieces? Run the same embedder after **one** training step: nearly random numbers for the same letter pieces. That is a **control**.

**`untrained.py`**

```python
# untrained.py - the control: the same embedder after ONE training step, so it is almost a random squashing of the letter pieces
r1c, r3c = [], []
for s in range(5):
    e = rag.TinyDenseEmbedder("contrastive", dim=32, seed=s, steps=1)
    ix = rag.VectorIndex(chunks, e)
    r1c.append(rag.recall_at_k(ix, QA, 1)); r3c.append(rag.recall_at_k(ix, QA, 3))
print(f"1 step  : mean recall@1 {np.mean(r1c):.2f}  recall@3 {np.mean(r3c):.2f}   (recall@1 by seed: {[round(x, 2) for x in r1c]})")
print(f"150 steps: mean recall@1 {np.mean(r1s):.2f}  recall@3 {np.mean(r3s):.2f}   (from seeds.py)")
print(f"pure chance: recall@1 {1/15:.2f}  recall@3 {3/15:.2f}")
```

```text
1 step  : mean recall@1 0.48  recall@3 0.73   (recall@1 by seed: [0.6, 0.4, 0.53, 0.33, 0.53])
150 steps: mean recall@1 0.63  recall@3 0.89   (from seeds.py)
pure chance: recall@1 0.07  recall@3 0.20
```

After one step the embedder already reaches recall@3 `0.73`, which equals the word table. Training adds about `0.15` on both recall@1 and recall@3 over almost-random numbers for the same pieces. That is about two of the 15 questions, over five seeds, and the seed ranges overlap (recall@1 after one step `0.33` to `0.60`; after 150 steps `0.47` to `0.73`), so read it as "modest", not as a precise `0.15`; it also measures this 150-step recipe, not training in general. **The sentence to keep: on these 15 questions, the trained tier scored about 0.15 higher on average than a one-step model built from the same letter pieces.**

![Paired bars of recall at 1 and at 3 for chance, word table, one-step control, trained embedder and LSA, with the seed range marked](../figures/fig-w25-2-recall-beside-its-control.svg)
*Figure 25.2 — A recall number needs its control. One training step already reaches recall@3 0.73; 150 steps reach 0.89, so training added 0.63 − 0.48 = 0.15 at recall@1.*


---

## 🎲 Your Turn

**The Cosine Cards (pen and calculator, no computer).** Workbook page 25.1 has `A`, `B`, `C` from above: the dot product, both lengths, the cosine, and one sentence on what a cosine ignores. Page 25.2 has four notes and a question `q = [1, 2, 2]`. Work out the **raw dot** of each note with `q`, then the **cosine**. Write the winner by raw dot, the winner by cosine, and which note points exactly the way the question points. Then one sentence: *why did the winner change?* Use three decimals, write your working, and if a number looks odd, say so in words.

**At the computer.** Type four short notes of your own (three sentences each) and run `fit_embedder(notes, 3)` on them. Write two questions whose answers are in your notes, and report where the right note ranks. Then write one question that **cannot** be answered by shared letter pieces, and write down what you expect the index to do with it *before* you run it.

---

## 🔬 Break It On Purpose

**DELIBERATE.** `TruncatedSVD` keeps `n_components` directions. What if you ask for more than there are? Write down what you expect, and run this after `lsa.py` in the same session.

**`break3.py`**

```python
# break3.py - DELIBERATE: more directions asked for than the table has columns.
X_ = vec.transform(chunks)
print("table shape:", X_.shape)
TruncatedSVD(n_components=5000, random_state=0).fit(X_)
```

```text
table shape: (15, 3906)
Traceback (most recent call last):
  File "/home/you/l4/break3.py", line 4, in <module>
    TruncatedSVD(n_components=5000, random_state=0).fit(X_)
  File "/home/you/venv/lib/python3.x/site-packages/sklearn/decomposition/_truncated_svd.py", line 206, in fit
    self.fit_transform(X)
  ...
ValueError: n_components(5000) must be <= n_features(3906).
```

Did the message tell you what to do? It names both numbers. Write in your Bug Log the largest sensible `n_components` for 15 notes, and why asking for all `15` would squeeze nothing (it keeps every direction).

---

## 🧭 What was shown, and what was not

**Shown:**
- The word table scores `optimiser` at `0.000` against every one of the 15 notes. Letter pieces give `optimizer` and `optimiser` a cosine of `0.359`, `optimise` and `optimiser` `0.670`, and `banana` `0.000`.
- The hand-built index (letter pieces, SVD to 14 numbers, normalise once, matrix multiply) gives exactly `l4lib`'s matrix and ranking, and `np.save` / `np.load` keeps it identical.
- On these 15 questions: word table recall@1 `0.67`, recall@3 `0.73`; SVD tier `0.73` and `1.00` (14 numbers); the contrastive tier averages `0.63` and `0.89` over five seeds (recall@1 from `0.47` to `0.73`).
- The control: one training step already gives recall@3 `0.73`. Training added about `0.15` on average (about two questions; the seed ranges overlap).

**Not shown:**
- **That "dense beats sparse".** At recall@1 the word table is level with the trained tier. At recall@3 the dense tiers are ahead, by small margins.
- **Anything about a real sentence encoder.** None is present and none was run. Would a pretrained one be better? Almost certainly, and we cannot measure it offline.
- **That the embedder knows what words mean.** It knows which letter pieces go together in 15 notes. `big` against `large` share no pieces, so there is no reason for it to put them near.
- **Anything general.** These numbers belong to this notebook and these 15 questions.
- **That a score such as `0.525` means "52% relevant".** It is a cosine. It ranks; it does not measure.

---

## 🔑 Wrap Up

1. What does a cosine ignore, and why is that what you want for text?
2. Why does `optimiser` get `0.000` from the word table, and what is in the last column of `headline.py` that shows the "rank 1" is not a success?
3. Where does `normalize` appear in `fit_embedder`, and why only once?
4. What does `np.save` not save?
5. What is `nn.EmbeddingBag`, and what does the `starts` list say?
6. Write one sentence that uses the word *control*. Then go back to your three cards from Start Here. What did you get right? What surprised you?

Then write this sentence in your Bug Log in your own handwriting:

> **"The embedder puts notes with shared letter pieces near each other; training helps by a modest amount on 15 notes; and I can say how much because I ran a control."**

**A look ahead.** Next week the index gets a job: it hands the right notes to an answer-writer that must say which note it used, and say "not in notes" when nothing is close. From Week 26 the answer-writer is a scripted stand-in, always labelled "stand-in, not a model". Today has none.

---

## 📤 Homework

Complete workbook pages 25.1 to 25.5. Write your **predictions before you run anything**: a guess written after the run is not a guess. Every number you write must come from your own calculator or your own run.

1. **Cosines by hand.** With `A = [1, 0, 3]` and a new vector `D = [3, 1, 0]`, compute `cos(A, D)` by hand, then `cos(C, D)` with `C = [4, 2, 0]`. Say which pair points nearest to the same way, then check both with `cosine` from `cosine.py`.
2. **Your own notes.** The four-note index from Your Turn. Save the matrix with `np.save`, reload it, and check that it is identical.
3. **The recall table.** Fill it from `recall.py` and `seeds.py`, then write **three sentences**: one about the word table, one that uses the word *control*, and one that says what the table does *not* show.

**Optional (fast students).** Six typed pairs (a short phrase and the note it should land near). Do they help? Predict, then type this in the same session as the others.

**`pairs.py`**

```python
# pairs.py - EXTENSION: six typed pairs (a short phrase and the note it should land near). Do they help?
pairs = [("optimiser comparison", chunks[0]), ("learning rate experiments", chunks[1]),
         ("regularisation and dropout", chunks[2]), ("normalisation layer placement", chunks[9]),
         ("tokeniser for emoji text", chunks[10]), ("cost per call", chunks[14])]
plain, paired = [], []
for s in range(5):
    for store, extra in ((plain, None), (paired, pairs)):
        e = rag.TinyDenseEmbedder("contrastive", dim=32, seed=s)
        M_ = e.fit_encode(chunks, pairs=extra)
        store.append((recall_with(e, M_, 1), recall_with(e, M_, 3)))
print("no typed pairs : mean recall@1 %.2f  recall@3 %.2f" % tuple(np.mean(plain, axis=0)))
print("six typed pairs: mean recall@1 %.2f  recall@3 %.2f" % tuple(np.mean(paired, axis=0)))
```

```text
no typed pairs : mean recall@1 0.63  recall@3 0.89
six typed pairs: mean recall@1 0.59  recall@3 0.83
```

Six typed pairs did not help here. Write what you would test to find out *why*.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **embedding** | The row of numbers that stands for a note |
| **sparse / dense** | Mostly zeros and very wide, or short with every number used |
| **character n-gram (letter piece)** | A run of 3 to 5 letters inside a word, with a space at each end of the word |
| **SVD / latent dimension** | A squeeze that keeps the best `n` directions of a table; each kept direction is a latent dimension |
| **LSA** | An SVD applied to a text table |
| **index** | The table of length-1 rows, searched by one matrix multiply |
| **normalise once** | Divide each row by its length when the index is built, so a dot product is a cosine |
| **contrastive training** | Train so that two halves of one note land nearer than halves of different notes |
| **positive pair** | Two halves of the same note |
| **recall@k** | The share of questions whose right note is in the top `k` |

---

[⬅ Week 24](week-24.md) · [Course Home](../README.md) · [Week 26 ➡](week-26.md) · [Workbook](../workbook/week-25.md)
