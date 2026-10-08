# Week 14 — Attention by Hand

[⬅ Week 13](week-13.md) · [Course Home](../README.md) · [Week 15 ➡](week-15.md) · [Student Guide](../student-guide/week-14.md) · [Workbook](../workbook/week-14.md)

---

## 📋 At a Glance

This table is the one-page summary of the week: timing, new ideas, materials and what is and is not real.

| | |
|---|---|
| **Duration** | 70 minutes in class, then the workbook (~60 min, almost all of it pen and calculator; the computer is used for about 10 minutes of checking) |
| **Type** | 🟦 Teach — one idea (a soft dictionary lookup), done once with a pen, then in numpy, then in torch, and shown to agree |
| **Big idea** | A **lookup** finds the best match and returns its value. **Attention** is a *soft* lookup: compare the question to **every** key, turn the scores into **weights** that add to 1, and return the **weighted average** of the values. Nothing is a hard yes or no, so everything can be nudged, so everything can be learned (Week 17). Today there is no learning at all: the student computes one three-word pass by hand, with numbers they can check. |
| **New vocabulary** | token · query · key · value · score · weight · weighted average · hard lookup / soft lookup · attention |
| **New maths** | **Weighted average** — a mean where some values count more; the weights are never negative and add to 1. Met first as `[0.7, 0.2, 0.1]` on three values (answer 20), *before* any softmax appears. See the 🔢 box. |
| **New syntax** | `k.transpose(-2, -1)` · `nn.Linear(d, d, bias=False)` · `tensor.unsqueeze(dim)`. That is all three (the ladder allows four). |
| **Dataset** | None. Three invented 2-number vectors for the words `the`, `cat`, `sat`, and three invented 2×2 tables. For one check, random numbers from a seeded generator. **Nothing downloads. No internet.** |
| **Model** | **No model.** Nothing is trained and nothing is learned. The three tables are chosen to be easy to multiply. Today is the *arithmetic* of attention; Week 17 is where the tables are learned. **There is no scripted backend and no stand-in anywhere in this week.** |
| **Materials** | Laptop with Python 3, numpy and torch (nothing new to install) · a pen and a calculator (phone in calculator mode is fine) · the printed **Pen Pass** sheet (Activity) · workbook pages 14.1-14.5 · a timer |
| **Prep time** | 25 minutes the night before · 3 minutes on the day |
| **Expected runtime of the code** | Everything below finishes in **about one second** in total. Anything over **30 seconds** means something is wrong (see Fallback). |

> **⚠️ Watch out:** two things go wrong this week. **First, the pen pass is long, and one wrong exponent ruins every number after it.** The student's final answer will often differ from the key in the third decimal because they rounded the weights to three places (see 🔢 and the key: `0.577` against `0.578` is correct working, not an error). Mark the *method* and the *row sums*, not the last digit. **Second, "attention" gets heard as "the model understands which words matter".** Today's weights come from invented 2-number vectors and two identity-ish tables. They show the arithmetic, and only that. They say nothing about what a trained model attends to; Week 19 measures that on a trained model and still says only what it measured.

![Map of the 36 weeks in four term lanes with week 14, Attention by Hand, highlighted in term 2 and weeks 1 to 13 solid behind it](../figures/fig-w14-0-where-this-fits.svg)
*Figure 14.0 — Where this week fits: week 14 of 36, in term 2 (memory, then attention).*

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Say what a soft lookup is** and how it differs from a hard one: every key is consulted, each answer is counted in proportion to how well its key matched, and the weights add to 1.
2. **Compute a weighted average by hand** — weights `[0.7, 0.2, 0.1]` on values `[10, 50, 30]` give 20 — and say why weights that add to 1.1 are *not* a weighted average (Mistake 7).
3. **Do the four steps of one attention pass on paper**, for three tokens with two numbers each: make questions, keys and values; score every question against every key; softmax each **row**; blend the values. Every weight row adds to 1.
4. **Reproduce the same pass in numpy and in torch** (`nn.Linear(d, d, bias=False)`, `k.transpose(-2, -1)`, `F.softmax(..., dim=-1)`) and **show that the pen, numpy and torch agree** to within rounding.
5. **Use `unsqueeze`** to add a length-1 axis, both to make a batch of one sentence and to stand a row of weights on end so it multiplies the values.
6. **Say why there are two different tables for questions and keys**: with one table the score of "cat asks sat" always equals "sat asks cat"; with two it need not.

Observable evidence: a filled **Pen Pass** sheet whose weight rows each add to 1; the printed line `all three agree to 0.002: True`; the short answer to "why two tables"; and, as homework, a second pass by hand with a changed question table.

---

## 🧑‍🏫 What YOU Need to Know First

This section gives you the background to teach the week without surprises: the maths, the three new constructs, what the numbers will print, and what not to claim.

> **📌 About the code blocks in this guide.** Every block in the **🧰 Prep Checklist**, in the **🐞 Debugging Clinic** and in the **🔑 Answer Key** was run on a CPU with one thread and the seeds shown; the outputs below are the real printed output. The Prep files `attention.py`, `twotables.py`, `anyweights.py` and `hw.py` are typed one after another **into the same file** (`attention.py`), so that later parts can use the names made by earlier parts, and they were run that way, top to bottom, in one namespace. `lookup.py` and `key.py` stand alone. The Clinic blocks that are *deliberate mistakes* are marked and their tracebacks are real. **Nothing printed below depends on timing. Every number repeated exactly on a second run.** The one line that can differ on another CPU or PyTorch build is `numpy vs torch, biggest gap` (about `4e-08`; anything below `1e-05` is fine). The tables of three decimals do not depend on your laptop.

### 1. What the student is doing today, in brief

Last week the model gave a *score for every letter* and the student used `F.softmax` to turn the scores into chances. Today the same softmax has a different job: deciding **how much each word should count**. They start with no code: three "experts" (bread, river, rope) hold three numbers; the question matches them with scores `0.1, 2.0, 0.3`; the student turns the scores into weights and takes the weighted average of what the experts know (`42.77`), and sees that a *hard* lookup would have returned only `50`.

Then they take one pass of attention through three words with a pen: make a question, a key and a value for each word, score every question against every key (nine dot products), softmax each row, and blend the values.

Only then do they type it: the same pass in numpy, line for line, then in torch with `nn.Linear(2, 2, bias=False)`, and they check that the three answers (pen, numpy, torch) agree. The last ten minutes ask one question — *why does every word get a question **and** a key?* — and answer it by changing one table and watching the scores stop being symmetric.

### 2. 🔢 The maths you need — taught to you first

**One new idea: the weighted average.** The student knows the ordinary mean (add up, divide by how many). A **weighted average** lets some values count more. The recipe has two rules for the **weights**: none is negative, and they **add up to 1**. Then: multiply each value by its own weight and add. Do these yourself before class, with a calculator.

| Values | Weights | Working | Answer |
|---|---|---|:--:|
| `10, 50, 30` | `0.7, 0.2, 0.1` | `7 + 10 + 3` | **20** |
| `10, 50, 30` | `1/3, 1/3, 1/3` | `3.33 + 16.67 + 10` | **30** (the ordinary mean: equal weights are the plain mean) |
| `10, 50, 30` | `0, 1, 0` | `0 + 50 + 0` | **50** (all the weight on one value: a *hard* lookup) |
| `10, 50, 30` | `0.7, 0.2, 0.2` | `7 + 10 + 6` | **23** — *not* a weighted average: the weights add to 1.1 (Mistake 7) |

Two facts to say out loud. **(i)** Because the weights are not negative and add to 1, the answer always lands **between the smallest and the biggest value** (20 is between 10 and 50). A result outside that range means the weights did not add to 1, or you multiplied by the wrong matrix. **(ii)** A hard lookup is just the special case where one weight is 1 and the rest are 0.

**Where the weights come from: the softmax the student already owns (Week 13).** Take scores `0.1, 2.0, 0.3` for bread, river, rope. Exponentiate: `exp(0.1) = 1.105`, `exp(2.0) = 7.389`, `exp(0.3) = 1.350`. The total is `9.844`. Divide: weights `0.112, 0.751, 0.137`. These add to 1 (0.112 + 0.751 + 0.137 = 1.000). The experts know `10, 50, 30`. The blend is `0.112 × 10 + 0.751 × 50 + 0.137 × 30`, which by hand at three decimals is `1.12 + 37.55 + 4.11 = 42.78`, and which the computer, carrying every digit, prints as **42.77**. (That one-hundredth is *rounding*; `lookup.py` prints both. Say so before the student finds it and worries.)

**The attention pass on three words.** The vectors and tables are the ones in the reference module's worked example:

```text
   the  = [1, 0]        Wq = identity         Wk = identity         Wv = swap the two numbers
   cat  = [0, 1]             [[1, 0],              [[1, 0],              [[0, 1],
   sat  = [1, 1]              [0, 1]]               [0, 1]]               [1, 0]]
```

1. **Make questions, keys, values.** Each word's row times each table. Because `Wq` and `Wk` are the identity, `Q = K = X`. `Wv` swaps the two numbers, so `V` is `[[0,1],[1,0],[1,1]]`.
2. **Score.** The score of word *i*'s question against word *j*'s key is the dot product of row *i* of `Q` with row *j* of `K` (multiply matching numbers, add: Level 3 Week 32). Nine of them: `[[1,0,1],[0,1,1],[1,1,2]]`.
3. **Softmax each row.** Row 1 is `[1, 0, 1]`: `exp` gives `2.718, 1, 2.718`, total `6.437`, weights `0.4223, 0.1554, 0.4223`. Row 2 is `[0, 1, 1]`: `0.1554, 0.4223, 0.4223`. Row 3 is `[1, 1, 2]`: `2.718, 2.718, 7.389`, total `12.826`, weights `0.2119, 0.2119, 0.5761`. **Each row adds to 1.** The columns do not, and should not (Mistake 8).
4. **Blend.** Row 1 of the output is `0.4223 × [0,1] + 0.1554 × [1,0] + 0.4223 × [1,1] = [0.5777, 0.8446]`, i.e. **`[0.578, 0.845]`**. Row 2: `[0.845, 0.578]`. Row 3: `0.2119 × [0,1] + 0.2119 × [1,0] + 0.5761 × [1,1] = [0.788, 0.788]`.

**The rounding trap, so you are not caught out.** A student who rounds the weights to **three** places before blending has `0.422 + 0.155 + 0.422 = 0.999` as a row sum and gets `[0.577, 0.844]` for row 1, out by one in the third decimal. That is correct working. Tell the student to **carry four places in the weights** and round only the answer. `key.py` prints all three routes (exact, 3-place weights, 4-place weights).

**The parts of the recipe that use each table.** The *weights* depend only on `Q` and `K`, which come from `Wq` and `Wk`. `Wv` appears **nowhere** in the weights: it only changes *what gets averaged*. `key.py` shows it: swap `Wv` for the identity and the weights are identical and the outputs are the rows of `X` blended instead. This is a fact worth saying once, because it is why there are three tables and not two.

> **🚫 What you must NOT claim about attention today.**
> 1. **Not "the model paid attention to the important word".** The weights are the softmax of dot products of invented vectors. "Important" is not in the arithmetic. Say "the weight on `sat` from `sat` is 0.576", never "the model cares about itself".
> 2. **Not "this is how a transformer works", full stop.** Today's pass has **no divide and no mask**. The reference module divides the scores by `√d_k` and hides the future; both come in Week 15. Today's numbers therefore differ from the module's (teacher reconciliation below).
> 3. **Not "attention is better than the recurrent cell".** The *argument* (an early word reaches a late word in one step, not through forty multiplications) is design reasoning, which Week 10's measurement motivates; today measures nothing about speed, accuracy or memory.

**Teacher-only: how today's numbers relate to the reference module's.** *(This box uses a divisor and a mask the student has not met; it is for you, and `key.py` marks it `TEACHER-ONLY`.)* The module runs this same `X`, `Wq`, `Wk`, `Wv`, but divides every score by `√2 = 1.4142` and sets the scores above the diagonal to `-∞` before the softmax (so a word cannot read a later one). With both, the weights are `[[1, 0, 0], [0.3302, 0.6698, 0], [0.2483, 0.2483, 0.5035]]` and the output `[[0, 1], [0.6698, 0.3302], [0.7517, 0.7517]]` (the module prints `0.7518` because it rounded the weights by hand). With only the divide the output is `[[0.599, 0.802], [0.802, 0.599], [0.752, 0.752]]`; with only the mask it is `[[0, 1], [0.731, 0.269], [0.788, 0.788]]`. Today's answer is neither, by design: **the ladder puts the divide and the mask in Week 15**, and today's unscaled, unmasked pass is the one with small whole-number scores that can be done with a pen. If the student has read the module, tell them the two dials are the next lesson.

![A table of bread, river and rope with scores, weight bars 0.112, 0.751 and 0.137, values 10, 50 and 30, and the soft answer 42.77 beside the hard answer 50.0](../figures/fig-w14-1-soft-lookup.svg)
*Figure 14.1 — A soft lookup is a weighted average: mostly the best match, with a trace of the others.*

### 3. 🧭 Real vs stand-in — and what you must NOT claim

| Thing | Real or stand-in? |
|---|---|
| The arithmetic: every score, weight and output | **Real.** numpy and torch, to the digits printed. The pen version is the same arithmetic. |
| The three word vectors (`the`, `cat`, `sat`) and the three tables | **Invented by us** (from the reference module's worked example) to be easy to multiply. Not learned, not from any model. |
| The names `the`, `cat`, `sat` | Labels on rows. The vectors do not encode what the words mean. |
| The bread / river / rope experts, their scores and values | **Invented.** The scores `0.1, 2.0, 0.3` and values `10, 50, 30` are the module's. |
| The random tables in `anyweights.py` | **Real random numbers** from `torch.manual_seed(0)`, used only to show that the row sums are 1 *whatever* the tables hold. Not trained. |
| Any trained model, any pretrained weights, any large language model | **Not present.** Week 17 is where these tables are learned. |

> **Say to the student, out loud:** *"Nobody taught these tables anything. We chose them so you could multiply them. The point is the recipe, which is the same recipe a real model uses with tables it learned."*

### 4. The three new constructs, for somebody who has never seen them

Each snippet below is complete; it runs on its own.

**(a) `k.transpose(-2, -1)` — swap the last two axes.**

```python
import torch

k = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])     # 3 labels, 2 numbers each: shape (3, 2)
print(k.shape, "->", k.transpose(-2, -1).shape)              # the last two axes swap places
print(k.transpose(-2, -1))

two = torch.stack([k, k])                                     # two sentences stacked: shape (2, 3, 2)
print(two.shape, "->", two.transpose(-2, -1).shape)           # same line, same meaning: only the LAST TWO swap
```

```text
torch.Size([3, 2]) -> torch.Size([2, 3])
tensor([[1., 0., 1.],
        [0., 1., 1.]])
torch.Size([2, 3, 2]) -> torch.Size([2, 2, 3])
```

Read as: *"turn the table on its side: rows become columns."* The student has met the transpose of a flat table as `K.T` in numpy. **What is new is the pair `-2, -1`:** it names the last two axes, so the same words work for one sentence `(3, 2)` and for a stack of sentences `(2, 3, 2)`, leaving the stack axis alone. Why we need it: the score table is `q @ k.transpose(-2, -1)`. `q` is `(3, 2)` (3 questions, 2 numbers). To dot every question with every key we need the keys as `(2, 3)`, which gives a `(3, 3)` table. Without the swap, `q @ k` is `(3, 2) @ (3, 2)`, and the shapes do not fit (Mistake 2). The student will also see `transpose(0, 1)` in the prep file; on a flat table that is the same swap, with the axes named by number. **Tell them `-2, -1` is the one to remember.**

**(b) `nn.Linear(d, d, bias=False)` — a table and nothing else.**

```python
import torch.nn as nn

lin = nn.Linear(2, 2, bias=False)        # bias=False: no extra number is added; it is a pure table
print(lin.weight.shape, lin.bias)        # the table has shape (2, 2); there is no bias at all
```

```text
torch.Size([2, 2]) None
```

Read as: *"a layer that multiplies by a `d`-by-`d` table, and adds nothing."* The student has built `nn.Linear` layers before (Level 3 and this term) and knows a layer multiplies and then adds a **bias**. `bias=False` leaves out the adding, which is exactly what `X @ Wq` on paper does. Three things to know:

1. It keeps the table in `lin.weight`.
2. It stores the table the other way round (it computes `x @ W.T`), so to make a layer that does `x @ table` on paper you give it the **transpose** of `table`. `linear_from` in `attention.py` does this with `.transpose(0, 1)`, and Mistake 4 is what happens if you do not. The class example's tables are their own transposes (identity and swap), which is why that mistake is invisible there; Mistake 4 uses a table that is not.
3. Leaving `bias=False` out means a hidden random bias is added to every output (Mistake 9).

The assignment `lin.weight.data = torch.tensor(...)` is Week 8's `rnn.weight_ih_l0.data = ...`.

**(c) `tensor.unsqueeze(dim)` — add a length-1 axis.**

```python
import torch

w = torch.tensor([0.5, 0.25, 0.25])      # three weights: shape (3,)
print(w.shape, w.unsqueeze(0).shape, w.unsqueeze(1).shape, w.unsqueeze(-1).shape)
print(w.unsqueeze(-1))                    # the same three numbers, stood on end: (3, 1)
```

```text
torch.Size([3]) torch.Size([1, 3]) torch.Size([3, 1]) torch.Size([3, 1])
tensor([[0.5000],
        [0.2500],
        [0.2500]])
```

Read as: *"insert an axis of length 1 at this position."* Use `-1` for "at the end", `0` for "at the front". Two uses today. **A batch of one sentence:** `x.unsqueeze(0)` turns `(3, 2)` into `(1, 3, 2)`, which is the shape a stack of sentences has, so the same `attend` function handles one sentence or many. **Standing the weights on end:** `w` is `(3,)` and `values` is `(3, 2)`; `w.unsqueeze(-1)` is `(3, 1)`, and `(3, 1) * (3, 2)` multiplies each row of `values` by its own weight (PyTorch stretches the length-1 axis to fit; the name for that is "broadcasting", and you can just call it "stretching"). Then `.sum(dim=0)` adds the rows. The wrong end, `unsqueeze(0)`, fails loudly with three tokens (Mistake 5) and **silently gives a wrong answer when the number of tokens equals the number of values** (Mistake 6). That is why the habit is `-1` and a check against `weights @ v`.

### 5. The other code the student types — nothing new, but note these

- `np.exp`, `.sum(axis=1).reshape(3, 1)`, `np.round`, `@` for a matrix product, `K.T`: Level 2 and 3. The `reshape(3, 1)` stands the row totals on end so each row is divided by its own total; without it `e.sum(axis=1)` divides down the wrong direction. **This is the numpy twin of `unsqueeze`.** (The alternative, `e / e.sum()`, divides by one grand total: Mistake 1.)
- `F.softmax(scores, dim=-1)` (Week 13). **Same function, new job**: last week it chose a letter; today it sets how much each word counts.
- `argmax` (Level 3): the position of the biggest score, for the hard lookup in `lookup.py`.
- `import torch.nn as nn`, `nn.Linear` with a table in `.weight` and `.weight.data = ...` (Week 8), `.tolist()` (Week 6), `torch.cat` and `torch.stack` (Weeks 10 and 12; Level 3 Week 27).
- `(a - b).abs().max().item()`: the biggest gap between two tables of numbers (Week 6 used the same kind of test). `.all()` turns a table of True/False into one True/False: "are all of them true?"
- `tuple(x.shape)`: the shape as a plain tuple, for a tidy print.
- `def` with a docstring (Level 2): `weights_of`, `attend`, `show`, `linear_from` are one-to-four-line functions. **`attend(x)` uses `lin_q`, `lin_k` and `lin_v` as global names on purpose:** that is how Week 16 reuses it, and `hw.py` works by re-assigning `lin_q` and calling `attend` again.

**Not used today, on purpose**, because they are later rungs: dividing the scores by `√d` (Week 15 — the student will ask), `masked_fill` and `torch.tril` (Week 15), `.view(...).transpose(1, 2)` heads (Week 15), position vectors and `register_buffer` (Week 16), any `nn.Module` class for attention (Week 17), `torch.where` (Week 24), and `.detach()` is avoided in favour of `.tolist()`. If the student asks *"how does it know the order of the words?"*: *"It does not — not yet. Week 16."*

### 6. What the numbers will say

All printed by the files below. Read them before class so nothing surprises you.

- **The soft lookup.** Hard: `river → 50`. Soft: weights `0.112, 0.751, 0.137`, answer **42.77** (42.78 if the three-place weights are used, as in the module). `[0.7, 0.2, 0.1]` gives **20.0**; equal weights give **30.0**, the ordinary mean.
- **The pass, by numpy.** Scores `[[1,0,1],[0,1,1],[1,1,2]]`. Weights `[[0.422, 0.155, 0.422], [0.155, 0.422, 0.422], [0.212, 0.212, 0.576]]`. Output `[[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]`.
- **Torch agrees.** The same three tables through `nn.Linear(2, 2, bias=False)` give the same weights and output; the biggest gap to numpy is about `4e-08` (float32 against float64).
- **A batch.** `(3, 2) → (1, 3, 2)` and `(2, 3, 2)`; the batch of one gives the same answer as the single pass **exactly** (`True`).
- **Pen against numpy.** The three-decimal pen table is within `0.0004` of numpy; the line `all three agree to 0.002` prints `True`.
- **Two tables.** With one table for questions and keys the score table is symmetric (`True`). With the question table `[[0,0],[1,0]]`, "cat asks sat" is `1.0` and "sat asks cat" is `0.0`; `the` asks nothing (its question is all zeros), gets equal weights `0.333` on every word, and its answer is the **plain mean** of the three values, `[0.667, 0.667]`.
- **Random tables, seed 0.** A 5-token, 4-number input with random `nn.Linear(4, 4, bias=False)` tables: the weights are a `5 × 5` table whose rows each add to **1.0**, every weight between 0 and 1. (`key.py` adds: every answer lies inside the range of its column of values, and the weights range from `0.084` to `0.361`.)

### 7. The honest limits of today

1. **The tables are invented and so are the vectors.** Nothing here says what a *trained* model's weights look like. The only general claim is the structural one: **each weight row is a softmax, so it adds to 1 and is never negative, whatever the tables hold.** That is what `anyweights.py` shows, on random tables.
2. **The pass has no divide and no mask**, so it is not the pass a GPT runs. It is the smallest pass that has all four steps. Week 15 adds the two dials and Week 17 trains the tables.
3. **Small whole-number scores hide what big scores do.** With scores of 0, 1, 2 the softmax is gentle: the biggest weight is `0.576`. With scores in the tens, one weight takes nearly everything and the others nearly nothing. The student will not see this today; Week 15 measures it.
4. **"Agreement" is to rounding, not exact.** numpy and torch agree to about `4e-08`, because torch keeps 32 bits and numpy 64. The pen agrees to the digits written down (`0.0004` here). A bigger gap is a bug or a transposed table (Mistake 4), not rounding.
5. **Attention weights are not an explanation.** That the weight from `sat` to `the` is `0.212` does not say *why* a model produced any output. Week 19 opens a trained model and looks at heads, and it says exactly what it finds and no more.
6. **This is "self-attention"**: the questions, keys and values all come from the *same* three words. There is a version where the questions come from one sequence and the keys from another; we do not build it.

### 8. The misconceptions you will actually meet

1. **"Attention picks the best word."** That is the *hard* lookup (one weight is 1). Attention gives every word a share. Run `lookup.py`: hard gives 50, soft gives 42.77.
2. **"The weights are the model's opinion of which word matters."** They are a softmax of dot products. See the three things you must not claim.
3. **"Q, K and V are three copies of the word."** They are three different *views* of it, each made by its own table. In the class example `Q` and `K` happen to be equal, which is a property of the identity tables and not of attention. Do the two-tables step so the student sees it.
4. **"Each row of weights should add to 1 in both directions."** Rows (one word deciding how to share its attention) add to 1. Columns need not (a popular word can collect more than 1). Mistake 8.
5. **"The output for `the` should look like `the`."** The output is a blend of *values*, and `Wv` here swaps the two numbers. The output is also a blend of all three words, not only the word itself.
6. **"torch and numpy disagreeing in the ninth decimal is a bug."** It is 32-bit against 64-bit arithmetic. The threshold is not zero.
7. **"`nn.Linear` does `x @ W`."** It does `x @ W.T + bias`. Mistakes 4 and 9.

### 9. How deep to go, and where to stop

Stop at: *"every word asks a question of every word; the answers are shared out by a softmax; what comes back is a weighted average of what the words had to say."* Do **not** go into why we divide the scores (Week 15 — if the student asks, *"good question, it is next week's whole lesson"*), masking, multiple heads, positions, the `O(T²)` cost, cross-attention, or how a trained model's tables are learned (Week 17). Do not say "transformer" as if the student has met one: it is Week 17. If the student asks *"is this ChatGPT?"*: *"This is the smallest piece of the recipe. There is a lot more around it, and we build the rest over the next three weeks."*

### 10. 🧭 Where Week 14 sits

```text
   W8   a cell that remembers          W13  scores -> chances (softmax); choose a letter
   W10  why memory fades               W14  scores -> weights; blend values (today)
   W11  gates keep it                        same softmax, new job: how much each word counts
   W12  teach it names
                                       W15  two dials: divide (big scores) and mask (no peeking); heads
   W9   Review & Assessment 1          W16  positions, the block     W17  TinyGPT: the tables are learned
                                       W18  Review 2 asks you to redo the 3-token pass on new numbers
```

---

## 🧰 Prep Checklist

This checklist gets you from an empty folder to tested files, a printed sheet and a plan for what to do if the laptops fail.

### 25 minutes the night before

- [ ] **Confirm the stack.** Run from any folder (this week needs no files from `l4lib/`):

```bash
python3 -c "import torch, numpy; print(torch.__version__, numpy.__version__)"
```

You must see (the digits may differ on another build):

```text
2.2.1 1.26.4
```

`pip` returning 403 is expected and not an error; **nothing this week installs anything.**

- [ ] **Type the files below into one working folder.** `lookup.py` and `key.py` stand alone. `attention.py` is typed in four pieces, one after another, **into the same file**: the first piece is the whole numpy and torch pass with the agreement check (Parts 1 to 3), and the next three (`twotables`, `anyweights`, `hw`) go at the bottom of it. Compare each output with what is printed here.

**File 1 — `lookup.py`** (the dictionary lookup, hard and soft; numpy only)

```python
# lookup.py - Week 14: a dictionary lookup, hard and then soft. Numpy only.
import numpy as np

names  = ["bread", "river", "rope"]
scores = np.array([0.1, 2.0, 0.3])        # how well each label matches the question (invented)
values = np.array([10.0, 50.0, 30.0])     # what each one could tell you (invented)

# HARD lookup: find the best match, hear only that one.
best = scores.argmax()
print("hard lookup:", names[best], "->", values[best])

# SOFT lookup, step 1: scores -> weights (the softmax you wrote in Week 13).
e = np.exp(scores)
weights = e / e.sum()
print("weights:", np.round(weights, 3), " add up to", round(weights.sum(), 3))

# SOFT lookup, step 2: the weighted average = each value times its weight, added up.
soft = (weights * values).sum()
print("soft lookup:", round(soft, 2))

# A weighted average with weights you choose yourself.
w = np.array([0.7, 0.2, 0.1])
print("weights [0.7, 0.2, 0.1]:", (w * values).sum())

# Equal weights give the ordinary mean.
equal = np.array([1/3, 1/3, 1/3])
print("equal weights:", round((equal * values).sum(), 2), " ordinary mean:", values.mean())
```

```text
hard lookup: river -> 50.0
weights: [0.112 0.751 0.137]  add up to 1.0
soft lookup: 42.77
weights [0.7, 0.2, 0.1]: 20.0
equal weights: 30.0  ordinary mean: 30.0
```

**File 2 — `attention.py`, Parts 1 to 3** (the pass in numpy, in torch, and the agreement check)

```python
# attention.py - Week 14. One pass of attention on three tokens, three ways: numpy, torch, and the pen.
# The three tokens are "the", "cat", "sat". Their 2-number vectors and the three tables are INVENTED to be easy.
# Nothing here is learned and nothing is a language model.
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)

# ======================== PART 1: numpy, one line per step of the pen version ========================
X  = np.array([[1.0, 0.0],
               [0.0, 1.0],
               [1.0, 1.0]])               # one row per token
Wq = np.array([[1.0, 0.0],
               [0.0, 1.0]])               # question table
Wk = np.array([[1.0, 0.0],
               [0.0, 1.0]])               # label table
Wv = np.array([[0.0, 1.0],
               [1.0, 0.0]])               # what-I-say table (swaps the two numbers)

Q = X @ Wq                                # step 1: every token makes a question...
K = X @ Wk                                # ...a label...
V = X @ Wv                                # ...and a value
print("Q =\n", Q)
print("K =\n", K)
print("V =\n", V)

scores = Q @ K.T                          # step 2: every question against every label (nine dot products)
print("scores =\n", scores)

e = np.exp(scores)                        # step 3: softmax, row by row
weights = e / e.sum(axis=1).reshape(3, 1)
print("weights =\n", np.round(weights, 3))
print("row sums:", weights.sum(axis=1))

out = weights @ V                         # step 4: blend the values
print("output =\n", np.round(out, 3))

# ======================== PART 2: the same pass in torch ========================
xt = torch.tensor(X.tolist())             # the same three rows, now a torch tensor
d = 2


def linear_from(table):
    """A layer that is ONLY a table (no bias). nn.Linear stores its table the other way round, so we transpose."""
    lin = nn.Linear(d, d, bias=False)
    lin.weight.data = torch.tensor(table).transpose(0, 1)
    return lin


lin_q = linear_from(Wq.tolist())
lin_k = linear_from(Wk.tolist())
lin_v = linear_from(Wv.tolist())


def weights_of(x):
    """x is (T, d) or (B, T, d). The weights: one row per token, each row adds to 1."""
    q, k = lin_q(x), lin_k(x)
    scores = q @ k.transpose(-2, -1)      # swap the LAST TWO axes, whatever comes before them
    return F.softmax(scores, dim=-1)


def attend(x):
    """One pass of attention: weights, then blend the values."""
    return weights_of(x) @ lin_v(x)


def show(t):
    """Print a tensor as plain numbers rounded to 3 places."""
    print(np.round(t.tolist(), 3))


w_t = weights_of(xt)
out_t = attend(xt)
print("torch weights =")
show(w_t)
print("torch output =")
show(out_t)

# ---- unsqueeze: add an axis of length 1 ----
print("xt shape:", tuple(xt.shape))
batch = xt.unsqueeze(0)                   # a batch of ONE sentence: (1, 3, 2)
print("batch shape:", tuple(batch.shape))
print("batch answer shape:", tuple(attend(batch).shape))
print("same answer as the single pass:", (attend(batch)[0] - out_t).abs().max().item() == 0.0)

# two sentences at once: the second is the first with "the" and "sat" swapped
xt2 = torch.tensor([[1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])
both = torch.cat([xt.unsqueeze(0), xt2.unsqueeze(0)], dim=0)
print("two sentences:", tuple(both.shape), "->", tuple(attend(both).shape))

# ---- the blend written out: the weights of ONE token, stood on end, times the values ----
w3 = w_t[2]                               # the weights of "sat"
v_t = lin_v(xt)
blend = (w3.unsqueeze(-1) * v_t).sum(dim=0)     # (3,1) * (3,2) -> (3,2), then add the three rows
print("w3 shape:", tuple(w3.shape), " w3.unsqueeze(-1) shape:", tuple(w3.unsqueeze(-1).shape))
print("blend of the three value rows:", np.round(blend.tolist(), 3), " equals row 3 of the output:",
      (blend - out_t[2]).abs().max().item() < 1e-6)

# ======================== PART 3: do the three agree? ========================
hand = np.array([[0.578, 0.845],
                 [0.845, 0.578],
                 [0.788, 0.788]])         # typed in from the pen, three decimals
out_from_torch = np.array(out_t.tolist())
print("numpy vs torch, biggest gap:", np.abs(out - out_from_torch).max())
print("pen vs numpy, biggest gap:  ", round(np.abs(hand - out).max(), 4))
print("all three agree to 0.002:", np.abs(hand - out).max() < 0.002 and np.abs(out - out_from_torch).max() < 0.002)
```

```text
Q =
 [[1. 0.]
 [0. 1.]
 [1. 1.]]
K =
 [[1. 0.]
 [0. 1.]
 [1. 1.]]
V =
 [[0. 1.]
 [1. 0.]
 [1. 1.]]
scores =
 [[1. 0. 1.]
 [0. 1. 1.]
 [1. 1. 2.]]
weights =
 [[0.422 0.155 0.422]
 [0.155 0.422 0.422]
 [0.212 0.212 0.576]]
row sums: [1. 1. 1.]
output =
 [[0.578 0.845]
 [0.845 0.578]
 [0.788 0.788]]
torch weights =
[[0.422 0.155 0.422]
 [0.155 0.422 0.422]
 [0.212 0.212 0.576]]
torch output =
[[0.578 0.845]
 [0.845 0.578]
 [0.788 0.788]]
xt shape: (3, 2)
batch shape: (1, 3, 2)
batch answer shape: (1, 3, 2)
same answer as the single pass: True
two sentences: (2, 3, 2) -> (2, 3, 2)
w3 shape: (3,)  w3.unsqueeze(-1) shape: (3, 1)
blend of the three value rows: [0.788 0.788]  equals row 3 of the output: True
numpy vs torch, biggest gap: 4.222880078952329e-08
pen vs numpy, biggest gap:   0.0004
all three agree to 0.002: True
```

**File 2, continued — `twotables.py`** (typed at the bottom of `attention.py`; uses `scores`, `X`, `Wk`, `V`)

```python
# twotables.py - Week 14: why a token gets a question AND a label. Needs attention.py run first (uses its names).
# With the SAME table for questions and labels, "cat asks about sat" equals "sat asks about cat".
# With DIFFERENT tables, it need not.
print("same table for both (attention.py):")
print(scores)                              # scores[1][2] and scores[2][1] are the same number

Wq2 = np.array([[0.0, 0.0],
                [1.0, 0.0]])               # a question built from the SECOND number of a token, put in the first slot
scores2 = (X @ Wq2) @ (X @ Wk).T
print("question table changed:")
print(scores2)
print("cat asks about sat:", scores2[1][2], "  sat asks about cat:", scores2[2][1])   # cat is row 1, sat is row 2

e2 = np.exp(scores2)
weights2 = e2 / e2.sum(axis=1).reshape(3, 1)
print("weights =\n", np.round(weights2, 3))
print("the's weights are all equal:", np.round(weights2[0], 3), "-> its answer is the plain mean of the values:",
      np.round(weights2[0] @ V, 3), np.round(V.mean(axis=0), 3))
print("first table is symmetric (score[i][j] equals score[j][i]):", bool((scores == scores.T).all()))
```

```text
same table for both (attention.py):
[[1. 0. 1.]
 [0. 1. 1.]
 [1. 1. 2.]]
question table changed:
[[0. 0. 0.]
 [1. 0. 1.]
 [1. 0. 1.]]
cat asks about sat: 1.0   sat asks about cat: 0.0
weights =
 [[0.333 0.333 0.333]
 [0.422 0.155 0.422]
 [0.422 0.155 0.422]]
the's weights are all equal: [0.333 0.333 0.333] -> its answer is the plain mean of the values: [0.667 0.667] [0.667 0.667]
first table is symmetric (score[i][j] equals score[j][i]): True
```

**File 2, continued — `anyweights.py`** (seeded random tables; the row sums are always 1)

```python
# anyweights.py - Week 14: whatever the three tables hold, the weights always add to 1 (random tables, seed 0).
torch.manual_seed(0)
x4 = torch.randn(5, 4)                     # 5 tokens, 4 numbers each (random, invented)
r_q = nn.Linear(4, 4, bias=False)          # two random tables, nothing learned
r_k = nn.Linear(4, 4, bias=False)

w5 = F.softmax(r_q(x4) @ r_k(x4).transpose(-2, -1), dim=-1)
print("weights shape:", tuple(w5.shape))
print("row sums:", np.round(w5.sum(dim=-1).tolist(), 4))
print("every weight is between 0 and 1:", bool((w5 >= 0).all()) and bool((w5 <= 1).all()))
```

```text
weights shape: (5, 5)
row sums: [1. 1. 1. 1. 1.]
every weight is between 0 and 1: True
```

**File 2, continued — `hw.py`** (the homework check; it re-assigns `lin_q` and calls `attend` again)

```python
# hw.py - Week 14 homework check, run after attention.py: swap the question table and ask again.
lin_q = linear_from([[0.0, 0.0], [1.0, 0.0]])     # the H2 question table; lin_k and lin_v stay as they were
print("weights =")
show(weights_of(xt))
print("output =")
show(attend(xt))
```

```text
weights =
[[0.333 0.333 0.333]
 [0.422 0.155 0.422]
 [0.422 0.155 0.422]]
output =
[[0.667 0.667]
 [0.578 0.845]
 [0.578 0.845]]
```

- [ ] **Run them as a set.** From the working folder: `cat attention.py twotables.py anyweights.py hw.py > whole.py && python3 whole.py > /dev/null && python3 lookup.py > /dev/null && python3 key.py > /dev/null && echo fine`. It should print `fine` and take about a second. (`whole.py` is a scratch file: delete it afterwards.)
- [ ] **Do the Pen Pass yourself, once, on the printed sheet,** with a calculator, before class. If your weights come out at `0.422 0.155 0.422` and you have three places, you now know the rounding trap.
- [ ] **Read `key.py`'s output** (below, in the Answer Key) and keep it face down. It is **teacher-only**: never give the student this file.
- [ ] **Print** the Pen Pass sheet (Activity, below), one copy per attempt (print two), and workbook pages 14.1-14.5.
- [ ] **Read the Debugging Clinic** and copy the nine `bad*.py` files to a scratch folder so they are ready to plant.

### 3 minutes on the day

- [ ] Open `lookup.py` and `attention.py` in the editor as **empty files**, for typing together.
- [ ] Put the Pen Pass sheet, a pen, a calculator and the timer on the desk. **Keep the key face down.**

### Fallback if the laptops fail

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: torch` | `python3 -m pip` is blocked; use a machine that already has torch. Without torch, do the Hook, the Concept, the Pen Pass and `lookup.py` (numpy only) and run the torch part from the printed output here. |
| `numpy vs torch, biggest gap` is not about `4e-08` | A different build, or the tables differ. Anything under `1e-05` is fine; a gap near `0.1` or more means a table is transposed wrongly (Mistake 4). |
| The pen answer differs from numpy in the third decimal | Rounding the weights to three places before blending (🔢 box). Ask for four places. |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied` | `q @ k` without the transpose (Mistake 2) or `v @ weights` (Mistake 3). Read the shapes in the message aloud. |
| `NameError: name 'scores' is not defined` in `twotables.py` | It was run on its own. It uses the names made by `attention.py`; type it at the bottom of that file. |
| `weights_of` prints weights whose rows do not add to 1 | `dim=0` instead of `dim=-1` (Mistake 8). |
| No laptop at all | The Hook, the Concept, the Pen Pass and the agreement table (page 14.3) work on paper and calculator. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the running order of the lesson, with the words to say at each step.

| Segment | Minutes | What happens |
|---|:--:|---|
| 🪝 Hook | 6 | "Who knows about the river?" Three experts, one hard answer, one soft answer: 50 against 42.77 |
| 🧠 Concept | 10 | Query, key, value; the four steps on the board; the weighted average |
| 🎲 Pen Pass | 20 | The whole three-word pass with a pen and a calculator, no computer |
| 💻 Live-code | 24 | `lookup.py` (4) · `attention.py` Part 1, numpy (6) · Part 2, torch (10) · Part 3, do the three agree (4) |
| 🔬 Two tables | 6 | Why a question and a key? Change one table and watch |
| 🔑 Wrap & assign | 4 | What we built, what we did not, the homework |

### 🪝 Hook — Who Knows About the River? (6 minutes)

**Do not open the editor.** You are three people on three cards. Put three index cards face down: `bread`, `river`, `rope`. On the back of each is a number the person knows: `10`, `50`, `30`.

1. **(2 min) The hard lookup.** *"I ask: who knows about the river? Here is how well each of us matches your question."* Write `bread 0.1 · river 2.0 · rope 0.3`. *"You can only hear one of us. Who?"* (River: 2.0 is the biggest.) *"So the answer is..."* Turn over the river card: **50**. *"That is a lookup. One winner, everyone else silenced."*
2. **(2 min) The soft lookup.** *"But bread and rope matched a little. Why throw their answers away? What if every one of us answers, at a volume that matches how well we matched?"* Write on the board: **answer = weight × value, added up, for every expert.** *"We need the volumes. They should add up to 1, like a dial with a fixed total. Where have you seen scores turned into shares that add to 1?"* (Last week: softmax.) Have the student compute `exp(0.1), exp(2.0), exp(0.3)` on the calculator and the three weights `0.112, 0.751, 0.137` and check that they add to 1.
3. **(2 min) The blend.** *"Now multiply each weight by the number on the back of the card and add."* They get **42.78** (or near it: `1.12 + 37.55 + 4.11`). Write it beside the 50. *"The soft answer is mostly the river's answer, with a trace of the other two. And here is the useful thing: every one of these numbers can be nudged a little, so a machine could learn to make the answer better. A hard lookup cannot be nudged. That is why models use soft ones."* Then write on the board:

> **"Attention: ask every word a question; share the attention out by softmax; take the weighted average of what they said."**

*If the student says "but the real answer is 50":* there is no real answer here; the numbers are invented. The point is the *shape* of the recipe. Do not argue about which of 50 or 42.77 is better.

### 🧠 Concept — Question, Key, Value, and Four Steps (10 minutes)

**(3 min) Where the question, the label and the answer come from.** *"In the cards, someone handed us the scores. In a sentence, the words have to produce them. Every word makes three things from itself:"* Draw:

```text
   a word, as 2 numbers:  x = [1, 0]
        x times Wq  ->  q   "what am I looking for?"      (the QUESTION)
        x times Wk  ->  k   "what do I offer?"             (the KEY, a label)
        x times Wv  ->  v   "what do I actually say?"      (the VALUE)
```

*"Three tables of numbers, Wq, Wk, Wv. Every word goes through all three. A **token** is one piece of text the model reads; today a token is one word. This is the dictionary idea again: a question, a label on each entry, and what each entry says."* Use the module's class analogy once: *the question is "who knows about the river?", the key is each person's mental label, the value is what they could tell you.*

**(5 min) The four steps, on the board.** Write and leave up:

```text
   1. make     Q = X Wq      K = X Wk      V = X Wv                (each word's row times a table)
   2. score    scores = Q K^T                                       (every question against every key)
   3. share    weights = softmax of each ROW of scores              (each row adds to 1)
   4. blend    output = weights V                                   (weighted average of the values)
```

Take each step with the student, slowly, in words. *"Step 2 is nine dot products. The dot product of a question with a key is big when they point the same way. Row 1 is word 1's question against all three keys."* *"Step 3 is the Week 13 softmax, applied to each row separately."* Ask: *"Why each row and not the whole table?"* (One row is one word deciding how to share its attention; the shares must add to 1 for that word.) *"Step 4: each word's answer is a blend of all three values, weighted by its row."*

**(2 min) The weighted average.** Put `[10, 50, 30]` with weights `[0.7, 0.2, 0.1]` on the board and have the student compute **20** (and say what equal weights `1/3, 1/3, 1/3` give: the ordinary mean, 30). *"A mean where some count more. The weights must add to 1. That is the only new maths today."* Ask: *"Can the answer be bigger than 50?"* (No: not with non-negative weights that add to 1.) **Hold back the rounding trap and the `unsqueeze` story**; they come in the pen pass and the live code.

![Three small grids joined by arrows: scores for the, cat and sat, then rows of weights that each add to 1 with the largest ringed, then the output rows](../figures/fig-w14-2-one-pass-three-words.svg)
*Figure 14.2 — One pass of attention on three words: scores, then weights that add to 1 in every row, then the blended output.*

### 🎲 Their Turn — The Pen Pass (20 minutes)

Hand over the Pen Pass sheet (🎲 The Activity, In Full). **No laptop.** The class example is the module's: three words `the = [1, 0]`, `cat = [0, 1]`, `sat = [1, 1]`, with the three tables printed on the sheet. The student fills Q, K, V; the nine scores; the exps and row totals; the weights (**four places**); the output (**three places**). You sit quietly and check row sums as they appear. **Do not tell them a number is wrong; ask "does this row add to 1?"** When they finish, they turn the sheet over, write one sentence — *what did `sat` pay most attention to, and what number says so?* (itself: `0.576`) — and keep the sheet for the agreement check in the live code. **Stop at 20 minutes.** A student who is stuck on step 3 has the exps on the sheet; one who is stuck on step 2 needs the dot-product reminder, not the answer.

### 💻 Live-Code Together — `lookup.py` and `attention.py` (24 minutes)

The student types. You narrate. **Nobody pastes.**

**Step 1 (4 min) — `lookup.py`.** Type it. Before running: *"what will the hard lookup print? the soft?"* (`river → 50.0`; about 42.) Run. Point at `42.77` against the hand answer `42.78`: *"the computer kept every digit; you rounded the weights to three places. One hundredth. We will see this again."* Point at `weights [0.7, 0.2, 0.1]: 20.0` and `equal weights: 30.0  ordinary mean: 30.0`.

**Step 2 (6 min) — `attention.py` Part 1, the pass in numpy.** Type it line by line, **saying which step of the pen pass each line is.** Before running, the student reads their Pen Pass answers for the scores and the weights aloud. Run. *"Does numpy give your pen numbers?"* They compare row by row. If a row of theirs is off: ask for the row sum first. **Point at `row sums: [1. 1. 1.]`** and the reshape line: *"`e.sum(axis=1)` is three totals, one per row. `reshape(3, 1)` stands them on end so each row is divided by its own total."* If they ask why not `e / e.sum()`: *"try it"* (that is Mistake 1; plant it afterwards).

**Step 3 (10 min) — Part 2, the pass in torch.** Type `linear_from`, `weights_of`, `attend`, `show`. Draw the three new constructs on the board as they appear. **(a) `nn.Linear(d, d, bias=False)`:** *"a layer that is only a table."* **The transpose line in `linear_from`:** say it plainly: *"nn.Linear stores its table the other way round. We hand it ours turned over. Today's tables will not notice if we forget, because identity and swap are their own flip. Remember I said that."* **(b) `k.transpose(-2, -1)`:** *"turn the keys on their side so each question meets each key."* **Run.** The torch weights and output print the same as the numpy ones. **(c) `unsqueeze`:** type the batch lines; before running, ask the student to predict the shape after `xt.unsqueeze(0)` (`(1, 3, 2)`); run. Then the last block: *"this is step 4 for one word, with a pen: each value row times its own weight, added."* Have them say why `w3.unsqueeze(-1)` has shape `(3, 1)`.

**Step 4 (4 min) — Part 3, do the three agree?** Type the `hand = ...` table **from their own Pen Pass sheet**, not from the board. Run. `pen vs numpy, biggest gap` should be under `0.002`; `numpy vs torch` about `4e-08`; `all three agree to 0.002: True`. *"Three different ways: a pen, numpy, torch. One answer. That is how you know you understood the recipe and not just copied it."* If their pen table is off by `0.001` (three-place weights), that is still a pass: explain the row sum `0.999`.

### 🔬 Two Tables — Why a Question and a Key? (6 minutes)

Type `twotables.py` at the bottom of `attention.py`. Before running: *"In our example Wq and Wk are the same table. What do you expect about `cat asks sat` and `sat asks cat`?"* (They are equal.) Run: `first table is symmetric: True`. *"Now the question table changes."* Run the first part. Read: `cat asks about sat: 1.0 sat asks about cat: 0.0`. *"With two tables, what I look for and what I offer can be different. 'A verb looks for its subject while advertising itself as a verb.'"* Point at the printout for `the`: *"its question is all zeros, so every score is 0, every weight is 0.333, and its answer is just the plain average of the values. Attention with no preference is the ordinary mean."* Optional (2 min, if time): `anyweights.py` — *"random tables, nothing trained: do the rows still add to 1?"* They do, every time: the softmax guarantees it.

### 🔑 Wrap & Assign (4 minutes)

1. **(2 min)** *"What did we build? One: a soft lookup is a weighted average, weights that add to 1. Two: the four steps, made, scored, shared, blended. Three: pen, numpy and torch, all agreeing. What did we not do?"* (Learn the tables; divide the scores; hide the future; use positions.) *"Right. The first two are next week."*
2. **(1 min)** *"Why is the softmax applied to each row and not the whole table?"* (Each row is one word's shares; they must add to 1 for that word.) Accept any answer with "one word" and "adds to 1".
3. **(1 min)** Hand out the workbook: the weighted-average sheet, a second pass by hand with the question table changed, and the three-way check in code. *"Your pen numbers must agree with the computer's. If they do not, find out which of the two is wrong before you move on."* One sentence ahead: *"Next week two things break: what happens when the scores are big, and what stops a word from reading the future."*

---

## 🐞 The Debugging Clinic

This section lists nine mistakes to plant on purpose, each with its real output and the question that gets the student to read it.

Every error below was produced by running the code. **Paths will differ on your machine**; here they are shown as `/home/you/l4/`. Each mistake is deliberate: you plant it, the student reads the traceback (or the surprising output) aloud, and you refuse to fix it until they have said what it means. **Six are silent**: the program runs and prints something wrong. Those are the dangerous ones, and they are marked.

### How to teach debugging without giving the answer

1. *"Read me the last line."* (It says what went wrong; the lines above say where.)
2. *"Which of your files is on the line above it?"*
3. *"What did you expect that line to do?"*
4. Only then: *"What is different?"*

For the silent mistakes: *"Does anything look wrong?"* Make them check a property that must be true (each weight row adds to 1; an average of equal numbers is that number; torch agrees with numpy).

### Mistake 1 — one total for the whole table (SILENT)

```python
# DELIBERATE MISTAKE 1 (SILENT): softmax over the whole score table instead of row by row.
import numpy as np

scores = np.array([[1.0, 0.0, 1.0],
                   [0.0, 1.0, 1.0],
                   [1.0, 1.0, 2.0]])
e = np.exp(scores)
weights = e / e.sum()                      # ONE total for all nine numbers; we wanted one total per row
print(np.round(weights, 3))
print("row sums:", np.round(weights.sum(axis=1), 3))
print("whole table adds to:", round(weights.sum(), 3))
```

```text
[[0.106 0.039 0.106]
 [0.039 0.106 0.106]
 [0.106 0.106 0.288]]
row sums: [0.25  0.25  0.499]
whole table adds to: 1.0
```

**Read it:** every number is positive and the whole table adds to 1, but each *row* adds to `0.25`, `0.25`, `0.499`. The rows are the words; each should add to 1. **Fix:** `e / e.sum(axis=1).reshape(3, 1)`. **Why it is silent:** the numbers are perfectly good "chances", shared over the wrong thing (all nine entries at once). *The check:* `weights.sum(axis=1)` must be all ones.

### Mistake 2 — the keys not turned on their side (loud)

```python
# DELIBERATE MISTAKE 2 (loud): the labels were not turned on their side.
import torch

q = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])    # 3 questions, 2 numbers each
k = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])    # 3 labels, 2 numbers each
scores = q @ k
print(scores)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad2.py", line 6, in <module>
    scores = q @ k
RuntimeError: mat1 and mat2 shapes cannot be multiplied (3x2 and 3x2)
```

**Read it:** two tables of shape `3x2` cannot be multiplied: the inner numbers (2 and 3) do not match. We need `(3, 2) @ (2, 3)`. **Fix:** `q @ k.transpose(-2, -1)`. Ask: *"what shape would the answer have?"* (`3x3`: every question against every key.)

### Mistake 3 — the blend the wrong way round (loud)

```python
# DELIBERATE MISTAKE 3 (loud): the blend written the wrong way round (values times weights).
import torch

weights = torch.tensor([[0.422, 0.155, 0.422],
                        [0.155, 0.422, 0.422],
                        [0.212, 0.212, 0.576]])            # (3, 3)
v = torch.tensor([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])    # (3, 2)
print(v @ weights)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad3.py", line 8, in <module>
    print(v @ weights)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (3x2 and 3x3)
```

**Read it:** `v` is `3x2` and `weights` is `3x3`: inner numbers 2 and 3 again. The blend is **weights first**: `weights @ v` is `(3, 3) @ (3, 2)`, giving `(3, 2)`, one answer per word. **Fix:** `weights @ v`. Say: *"the weights are the shares; they come first because each row of weights picks a mix of the rows of `v`."* (Note that with three tokens and three values this fails loudly; with the same number of tokens as numbers it would not, which is why the row-sum and hull checks exist.)

### Mistake 4 — a table given to `nn.Linear` without turning it over (SILENT)

```python
# DELIBERATE MISTAKE 4 (SILENT): a table given to nn.Linear without turning it over. This one is NOT symmetric.
import numpy as np
import torch
import torch.nn as nn

table = [[1.0, 2.0],
         [0.0, 1.0]]
x = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
by_hand = x @ np.array(table)              # the pen answer: each row times the table

lin = nn.Linear(2, 2, bias=False)
lin.weight.data = torch.tensor(table)      # we forgot .transpose(0, 1)
print("pen answer:\n", by_hand)
print("nn.Linear answer:\n", np.round(lin(torch.tensor(x.tolist())).tolist(), 3))

# Why the Week 14 class example never showed it: its tables are their own transposes.
same = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
swap = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
print("identity equals its transpose:", bool((same == same.transpose(0, 1)).all()),
      " swap equals its transpose:", bool((swap == swap.transpose(0, 1)).all()))
```

```text
pen answer:
 [[1. 2.]
 [0. 1.]
 [1. 3.]]
nn.Linear answer:
 [[1. 0.]
 [2. 1.]
 [3. 1.]]
identity equals its transpose: True  swap equals its transpose: True
```

**Read it:** the pen answer and the `nn.Linear` answer are different, and only the first is what `x @ table` means. Row 2 `[0, 1]` times `[[1,2],[0,1]]` is `[0, 1]` on paper and `[2, 1]` from the layer. The last line shows why Week 14's class example never caught it: identity and swap are their own transposes. **Fix:** `lin.weight.data = torch.tensor(table).transpose(0, 1)`. **Why it is silent:** every number is a number, and the shape is right. *The check:* the three-way agreement test. Use a non-symmetric table whenever you compare pen with torch.

### Mistake 5 — `unsqueeze` on the wrong end (loud)

```python
# DELIBERATE MISTAKE 5 (loud): unsqueeze on the wrong end.
import torch

values = torch.tensor([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])    # 3 tokens, 2 numbers each
w = torch.tensor([0.5, 0.25, 0.25])                              # 3 weights, one per token

blend = (w.unsqueeze(0) * values).sum(dim=0)                     # we wanted w.unsqueeze(-1)
print(blend)
```

```text
Traceback (most recent call last):
  File "/home/you/l4/bad5.py", line 7, in <module>
    blend = (w.unsqueeze(0) * values).sum(dim=0)                     # we wanted w.unsqueeze(-1)
RuntimeError: The size of tensor a (3) must match the size of tensor b (2) at non-singleton dimension 1
```

**Read it:** the weights became `(1, 3)` and the values are `(3, 2)`. The 3 and the 2 sit under each other and cannot be stretched to match. **Fix:** `w.unsqueeze(-1)`, giving `(3, 1)`. *Ask:* "what does `(3, 1) * (3, 2)` do?" (Each row of `values` times its own weight.)

### Mistake 6 — the same wrong `unsqueeze`, with as many tokens as numbers (SILENT)

```python
# DELIBERATE MISTAKE 6 (SILENT): the same wrong unsqueeze, with as many tokens as numbers.
import numpy as np
import torch

values = torch.tensor([[0.0, 1.0], [1.0, 0.0]])    # 2 tokens, 2 numbers each
w = torch.tensor([0.9, 0.1])                       # 2 weights

right = (w.unsqueeze(-1) * values).sum(dim=0)      # each ROW times its own weight
wrong = (w.unsqueeze(0) * values).sum(dim=0)       # each COLUMN times a weight: shapes fit, meaning does not
print("right:", np.round(right.tolist(), 2))
print("wrong:", np.round(wrong.tolist(), 2), " <- runs, and is wrong")
```

```text
right: [0.1 0.9]
wrong: [0.9 0.1]  <- runs, and is wrong
```

**Read it:** the two answers are the same numbers in the opposite order. With two weights and two columns the shapes *do* fit, so nothing complains, but each **column** of `values` was multiplied by a weight instead of each **row**. **Fix:** `unsqueeze(-1)`. *The check:* `weights @ values` must equal it; make the student run it.

### Mistake 7 — weights that do not add to 1 (SILENT)

```python
# DELIBERATE MISTAKE 7 (SILENT): weights that do not add to 1 are not a weighted average.
import numpy as np

values  = np.array([10.0, 10.0, 10.0])     # three copies of the same number
weights = np.array([0.7, 0.2, 0.2])        # typed by hand; 0.7 + 0.2 + 0.2 is not 1
print("weights add to:", round(weights.sum(), 2))
print("'average' of three tens:", (weights * values).sum(), " <- an average of equal numbers must be that number")
```

```text
weights add to: 1.1
'average' of three tens: 11.0  <- an average of equal numbers must be that number
```

**Read it:** three tens, "averaged", give 11. An average of equal numbers must be that number. The weights add to 1.1. **Fix:** make them add to 1, or divide by their sum. This is the mistake behind every hand-typed weight; a softmax never makes it.

### Mistake 8 — softmax down the columns instead of along the rows (SILENT)

```python
# DELIBERATE MISTAKE 8 (SILENT): softmax down the columns (dim=0) instead of along each row.
import numpy as np
import torch
import torch.nn.functional as F

scores = torch.tensor([[1.0, 0.0, 1.0],
                       [0.0, 1.0, 1.0],
                       [1.0, 1.0, 2.0]])
weights = F.softmax(scores, dim=0)
print(np.round(weights.tolist(), 3))
print("row sums:   ", np.round(weights.sum(dim=-1).tolist(), 3))
print("column sums:", np.round(weights.sum(dim=0).tolist(), 3))
```

```text
[[0.422 0.155 0.212]
 [0.155 0.422 0.212]
 [0.422 0.422 0.576]]
row sums:    [0.79  0.79  1.421]
column sums: [1. 1. 1.]
```

**Read it:** each *column* adds to 1 and each *row* does not (`0.79`, `0.79`, `1.421`). This is Week 13's Mistake 1 again, in attention clothes. **Fix:** `dim=-1`. **Why it matters here:** with `dim=0` word 1 would be dividing its attention by what every other word thinks of each word, not by what it thinks. *The check:* `weights.sum(dim=-1)` must be all ones.

### Mistake 9 — a hidden random bias (SILENT)

```python
# DELIBERATE MISTAKE 9 (SILENT): nn.Linear left with its default bias when the pen version has none.
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0)
lin = nn.Linear(2, 2)                      # no bias=False: a bias is created, with random numbers
lin.weight.data = torch.tensor([[1.0, 0.0], [0.0, 1.0]])    # the identity table
x = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
print("should be x itself; got:")
print(np.round(lin(x).tolist(), 3))
print("the bias it added:", np.round(lin.bias.tolist(), 3))
```

```text
should be x itself; got:
[[ 0.728  0.19 ]
 [-0.272  1.19 ]
 [ 0.728  1.19 ]]
the bias it added: [-0.272  0.19 ]
```

**Read it:** the layer's table is the identity, so it should return `x` unchanged. It returned numbers near `x`, not equal. The two numbers in `lin.bias` were added to every row. **Fix:** `nn.Linear(2, 2, bias=False)`. **Why it is silent:** the shape is right and the numbers are close, which is the worst case. *The check:* compare with the pen answer, every time.

---

## 🎲 The Activity, In Full

This section holds everything for the Pen Pass: the printable sheet, the rules, the reveal and two variations.

### The Pen Pass

**Purpose.** To make the student *be* the attention layer for one pass, so that the numpy and torch lines they type later are something they have already done. Materials: the sheet (below), a pen, a calculator, your key.

### Setup (2 minutes before class)

Print the sheet. The exps are given so that nobody loses the lesson to a calculator key. Make two copies: the second is for a retry, or for the homework check.

```text
THE PEN PASS - three words, two numbers each.         Carry FOUR places in the weights. Round only the answer.

   the = [1, 0]     cat = [0, 1]     sat = [1, 1]          X = the rows above, in that order

   Wq = [[1, 0],    Wk = [[1, 0],    Wv = [[0, 1],
         [0, 1]]          [0, 1]]          [1, 0]]

   exp(0) = 1.000      exp(1) = 2.718      exp(2) = 7.389

STEP 1  make.    Q = X times Wq     K = X times Wk     V = X times Wv
        Q = [ __ , __ ]  [ __ , __ ]  [ __ , __ ]        (the, cat, sat)
        K = [ __ , __ ]  [ __ , __ ]  [ __ , __ ]
        V = [ __ , __ ]  [ __ , __ ]  [ __ , __ ]

STEP 2  score.   score(i, j) = (row i of Q) dot (row j of K)        (multiply matching numbers, add)
                  key:  the   cat   sat
        question the  [ __    __    __ ]
                 cat  [ __    __    __ ]
                 sat  [ __    __    __ ]

STEP 3  share.   For each ROW: exp of each score, the row total, each exp / total.
        row the:  exps __ __ __   total __     weights __ __ __     (they must add to 1)
        row cat:  exps __ __ __   total __     weights __ __ __
        row sat:  exps __ __ __   total __     weights __ __ __

STEP 4  blend.   output row = (weight 1) x (row 1 of V) + (weight 2) x (row 2 of V) + (weight 3) x (row 3 of V)
        the ->  [ ____ , ____ ]
        cat ->  [ ____ , ____ ]
        sat ->  [ ____ , ____ ]                 (three places)

CHECK   Did every weight row add to 1?  __    Is every output number between 0 and 1?  __
WRITE   What did "sat" pay most attention to, and which number says so?  ______________________
```

### The rules, read out loud before the first mark

1. *"This is one pass of attention, and you are the machine. Work in order. Carry four places in the weights."*
2. *"After step 3, stop and add each weight row. If a row does not add to 1, find out why before you go on."*
3. *"You may use the calculator. You may not ask me for an answer. You may ask me whether a row adds to 1 and I will tell you only that."*

### The reveal (the part with the learning in it)

1. **(2 min) Read the key together.** Scores: `[[1,0,1],[0,1,1],[1,1,2]]`. Weights to four places: `the [0.4223, 0.1554, 0.4223]`, `cat [0.1554, 0.4223, 0.4223]`, `sat [0.2119, 0.2119, 0.5761]`. Output: `[[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]`. The student marks their own sheet in another colour.
2. **(1 min) Ask three things.** *"Which word pays the most attention to itself?"* (`sat`, 0.5761.) *"Why does `sat` pay more to itself than `the` does?"* (Its score with itself is 2, the others 1; `sat` is `[1, 1]`, a longer vector than `[1, 0]`, so its dot product with itself is bigger: a dot product grows with length as well as with direction, and every vector points exactly along itself.) *"Which two words get the same weights from `sat`?"* (`the` and `cat`: `0.2119` each; `sat` matches both equally.)
3. **(1 min) The rounding trap.** If their output is `0.577`, `0.844`: *"Add your weights in row 1."* (0.999.) *"That gap is the whole difference. Carry four places."*

### The key

The filled sheet is the Answer Key page 14.1. Key facts: **scores `[[1,0,1],[0,1,1],[1,1,2]]`; row totals `6.437, 6.437, 12.826`; weights above; output `[[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]`.** All weight rows add to 1 at four places; `0.422 + 0.155 + 0.422` adds to 0.999 at three.

### What "finished" looks like

A filled sheet whose three weight rows add to 1, output within `0.001` of the key, and one written sentence: *"sat pays most attention to itself, weight 0.576."*

### Variation — easier

Give the student a completed Steps 1 and 2 and have them do only the row `sat` (one row of step 3 and one of step 4). Then show them that the other two rows are the same arithmetic.

### Variation — harder

Swap the question table for `[[0, 0], [1, 0]]` on a second sheet (the homework H2) and have the student predict which row's weights will be equal *before* calculating. Or ask: *"change only `Wv`; which of the steps change?"* (Only step 4; the weights do not move.)

---

## ❓ Questions Students Ask This Week

This section gives short answers to the questions you are likely to be asked.

**"Why three tables?"** The question says what a word is looking for, the key says what it offers, and the value says what it contributes. A word can look for one thing and offer another. Two tables make the scores able to be different in the two directions (the Two Tables step); the third decides what actually gets averaged, and the weights never depend on it.

**"Where do the tables come from?"** Today we chose them. In a real model they are learned by the same gradient-and-nudge loop as everything since Week 1; that is Week 17.

**"Why do we take the softmax of each row?"** Because row *i* is word *i* deciding how to share its attention across all the words. The shares for one word must add to 1. The columns (how much attention a word *receives*) need not.

**"What is a token?"** One piece of text the model reads. Today, one word. (Later weeks make it a piece of a word; Week 20.)

**"Why does the output for `the` not look like `the`?"** The output is a weighted blend of the *values*, and in this example `Wv` swaps the two numbers, and the blend includes all three words. It is not a copy.

**"Is the dot product the same as cosine similarity?"** Cosine similarity is a dot product after making each vector length 1 (Level 3 Week 32). Today we do not make them length 1, so bigger vectors give bigger scores.

**"Why does torch print `0.4220` and numpy `0.422`?"** Different print styles. We round to three places with `np.round` so they match.

**"Why `bias=False`?"** The pen version only multiplies. A bias adds a number on top, which is a real thing layers do, but attention's tables do not need it in this recipe (and leaving it on is Mistake 9).

**"Why is numpy slightly different from torch?"** torch keeps 32 bits per number, numpy 64. They agree to about 8 decimals.

**"Why can't I divide by the square root of something? The book does."** The reference module does, and so will we: it is Week 15, with its reason. Today's scores are small whole numbers, so nothing needs calming down.

**"Does the model read all the words at once?"** In this pass, yes: every word's question is scored against every word's key, in one matrix product. That is the idea that replaces the one-at-a-time recurrent cell; what it costs and what it needs (order, a mask) come in the next two weeks.

**"Is this what ChatGPT does?"** This is the smallest piece of the recipe. We add the rest over the next three weeks, and we never use a pretrained model.

**"Will my numbers match yours?"** The by-hand numbers and every printed table of three decimals are arithmetic and will match. The `4e-08` line can differ on another build. The random-table check uses seed 0 and should match on the same PyTorch version.

---

## ⚠️ Where This Lesson Goes Wrong

Use this table to match a symptom to its cause and a next move.

| Symptom | What is happening | What to do |
|---|---|---|
| The pen answer is off by `0.001` | Weights rounded to three places before blending; row sum 0.999 | Ask the student to add their weights; carry four places |
| A weight row does not add to 1 | An exp or the total is wrong, or the whole-table total was used | Ask for the row sum first; Mistake 1 |
| The student says "attention picks the important word" | They have heard the hard lookup | Run `lookup.py`: 50 against 42.77; point at the weights `0.112, 0.751, 0.137` |
| The student thinks `Q` and `K` are copies of `X` | In this example `Wq` and `Wk` are the identity | Do the Two Tables step; change `Wq` and print `K` and `Q` |
| `nn.Linear` output differs from numpy, by a lot | Table not transposed (symmetric tables hide it) or `bias=False` missing | Mistakes 4 and 9; test with a non-symmetric table |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied` | `q @ k` or `v @ weights` | Mistakes 2 and 3; say the shapes aloud |
| `twotables.py` says `NameError` | It was run alone | It uses names from `attention.py`; type it at the bottom of that file |
| The student asks about the divide and the mask and derails | The reference module has them | "Next week"; write it on the parking list |
| The lesson overruns | The Pen Pass is the longest piece | Give the completed Steps 1-2 (Variation — easier); never drop the three-way agreement |

---

## 🧭 Differentiation

This section says how to adjust the lesson for a student who is struggling, moving fast or not engaging.

### If the student is struggling

Stay with the river: hard lookup, soft lookup, weights, blend. Skip the matrix form. The minimum viable lesson: they can compute `[0.7, 0.2, 0.1]` on `[10, 50, 30]` (20), they can get from scores `0.1, 2.0, 0.3` to the weights and the blend (42.77), they have run `attention.py` Part 1 and can point to which line is "score", "share", "blend", and they say *"every word asks every word, and the answers are averaged by weights that add to 1."* Do the Pen Pass with the completed Steps 1 and 2 and only the row `sat`. Skip `unsqueeze` (show the shapes printed) and skip Two Tables.

### If the student is flying

Ask them to **predict, then run**: *"change `Wv` to the identity; which numbers change?"* (Only the outputs: `[[0.845, 0.578], [0.578, 0.845], [0.788, 0.788]]`; the weights are unchanged.) Then: *"make one key point exactly opposite to a question: what is the score, and what happens to the weight?"* (Score goes negative, `exp` is smaller than 1, weight is smaller than the rest but never negative.) Then the challenge: *"write `attend` so that it works on a stack of sentences with different tables in each"* — stop them at the shape wall: that is Week 15's heads. The teacher-only reconciliation with the reference module (divide by `√2`, hide the future) is a good aside: *"the module gets `0.6698, 0.3302` for `cat`; we get `0.845, 0.578`. Which two changes get you from ours to theirs?"* Do not give the answer: Week 15.

### If the student won't engage today

Run the Hook with the cards and no screen. Three index cards and a calculator need no typing. Then: *"you are the computer: give me the answer."* The Pen Pass on `sat` alone is one row of arithmetic and a result they can be proud of; the code can wait for the homework.

---

## ✅ Assessing Understanding

This section gives the questions to ask near the end and how to read the answers.

Ask these out loud near the end; do not rescue.

| Question | A good answer | A shaky answer |
|---|---|---|
| What is a soft lookup? | Compare the question to every key, turn the scores into weights that add to 1, and return the weighted average of the values | "It looks up the best match" |
| What is a weighted average? | A mean where some values count more; the weights are not negative and add to 1 | "An average" (no weights) |
| What must be true of each row of weights? | It adds to 1 (and no weight is negative) | "They are between 0 and 1" (only half) |
| Why does `the` get `0.333, 0.333, 0.333` in the Two Tables step? | Its question is all zeros, so every score is 0 and every exp is 1 | "Random" |
| What are the four steps of attention? | Make Q, K, V; score with Q against K; softmax each row; blend the values with the weights | Names some of the steps |
| Why are there separate tables for a question and a key? | What a word looks for can differ from what it offers; with one table the scores are symmetric | "They are different things" with no reason |
| What does `k.transpose(-2, -1)` do? | Swaps the last two axes so each question meets each key | "Transposes k" |
| How did you check that the pen, numpy and torch agree? | The biggest gap, under `0.002`; the pen within rounding, torch within about `1e-7` | "They looked the same" |
| Does a weight of 0.576 mean the model cares about that word? | No: it is the softmax of a dot product of invented vectors; it says nothing about meaning | "Yes, it pays attention to it" |

### Mastery scale for this week

| Level | Evidence |
|:--:|---|
| 🟥 Not yet | Cannot say what a weighted average is; weights not adding to 1 do not bother them. |
| 🟨 Emerging | Computes the river blend and the weighted average; runs `attention.py`; cannot do the pen pass without help. |
| 🟩 Secure | Completes the Pen Pass with row sums of 1; types Parts 1-3; says the four steps; shows the three agree. |
| 🟦 Strong | Also explains why two tables (symmetric scores), predicts what changing `Wv` does (weights fixed), and spots Mistake 4 or 6 unaided. |

---

## 📤 Homework to Assign

This section lists the three workbook tasks and the time they take.

~60 minutes, in the workbook, pages 14.1-14.5. The three tasks:

1. **Weighted averages (page 14.2).** For values `10, 50, 30`, compute the weighted average for weights `[0.5, 0.25, 0.25]` (25.0), `[0, 1, 0]` (50.0) and `[0.7, 0.2, 0.2]`; say which is **not** a weighted average and why (the weights add to 1.1), and fix it (divide each weight by 1.1, or by the total: `20.909`). The key is `key.py`'s H1 block.
2. **A second pass by hand (page 14.4).** Same `X`, `Wk`, `Wv` as the class, but the question table is `Wq = [[0, 0], [1, 0]]`. Compute `Q`, the scores, the weights (four places) and the output (three places) by hand. **Before** calculating, predict which row of weights will be equal across all three words (row `the`), and say why. The key is `key.py`'s H2 block.
3. **The three-way check (page 14.5).** With `hw.py`, run the same pass in torch (`lin_q = linear_from([[0.0, 0.0], [1.0, 0.0]])`), and report the biggest gap between the pen and the computer. If it is over `0.002`, find out which is wrong. The extension for the fast student: change only `Wv` to the identity and say which printed numbers change (the output) and which do not (the weights).

---

## 🔑 Answer Key

This section is teacher-only: every answer for the workbook, the full `key.py`, and the answers to the questions posed in the lesson.

Every number below comes from `key.py` (teacher-only) or from the files above.

### Page 14.1 — The Pen Pass (class example)

| | |
|---|---|
| **Q** (= **K**, identity tables) | the `[1, 0]`, cat `[0, 1]`, sat `[1, 1]` |
| **V** (`Wv` swaps) | the `[0, 1]`, cat `[1, 0]`, sat `[1, 1]` |
| **Scores** | `the [1, 0, 1]`, `cat [0, 1, 1]`, `sat [1, 1, 2]` |
| **Row totals of exps** | `6.437`, `6.437`, `12.826` (with `exp(0) = 1`, `exp(1) = 2.7183`, `exp(2) = 7.3891`) |
| **Weights, four places** | `the [0.4223, 0.1554, 0.4223]`, `cat [0.1554, 0.4223, 0.4223]`, `sat [0.2119, 0.2119, 0.5761]` |
| **Output, three places** | `the [0.578, 0.845]`, `cat [0.845, 0.578]`, `sat [0.788, 0.788]` |

Row totals of exps to four places: `6.4366`, `6.4366`, `12.8257`. Carrying **three** places in the weights gives `[[0.577, 0.844], [0.844, 0.577], [0.788, 0.788]]`: accept it (the `the` and `cat` row sums are 0.999). The written sentence: *"`sat` pays most attention to itself, 0.576."* Accept any sentence naming the word and the number. Check: every output number is between 0 and 1 (the values are 0s and 1s; a weighted average cannot leave that range).

**Workbook Part B (two words, `Wv = [[2, 0], [0, 4]]`):** scores `[[1, 0], [0, 1]]`, row totals `3.7183`, weights `a [0.7311, 0.2689]`, `b [0.2689, 0.7311]`, output `a [1.462, 1.076]`, `b [0.538, 2.924]`; word `a` leans towards its own value `[2, 0]`.

### Page 14.2 — The soft lookup and the weighted average (from `lookup.py` and `key.py`)

| Question | Answer |
|---|---|
| Hard lookup on the river scores | `river → 50.0` |
| Weights for `0.1, 2.0, 0.3` | `0.112, 0.751, 0.137` (exps `1.105, 7.389, 1.350`, total `9.844`) |
| Soft lookup | **42.77** by machine; **42.78** by hand with three-place weights (`1.12 + 37.55 + 4.11`) |
| `[0.7, 0.2, 0.1]` on `10, 50, 30` | **20.0** |
| Equal weights | **30.0**, the ordinary mean |
| H1: `[0.5, 0.25, 0.25]` | **25.0** |
| H1: `[0, 1, 0]` | **50.0** |
| H1: `[0.7, 0.2, 0.2]` | **23.0**; not a weighted average (adds to **1.1**); divided by the total: `23.0 / 1.1 = 20.909` |

**Workbook Part A** (new scores `1.0, 0.0, 2.0` for `bread, river, rope`): the hard lookup picks `rope` and returns **30**; exps `2.7183, 1.0000, 7.3891`, total `11.1073`; weights `0.245, 0.090, 0.665` (add to 1.000); soft lookup `(0.245 x 10) + (0.090 x 50) + (0.665 x 30) = 2.450 + 4.500 + 19.950 =` **26.90** by hand, **26.91** by machine, smaller than the hard 30 because the other two values pull it down in proportion to their weights.

### Page 14.3 — The agreement table (from `attention.py` Part 3)

| | the | cat | sat |
|---|:--:|:--:|:--:|
| Pen (four-place weights) | `[0.578, 0.845]` | `[0.845, 0.578]` | `[0.788, 0.788]` |
| numpy | `[0.578, 0.845]` | `[0.845, 0.578]` | `[0.788, 0.788]` |
| torch | `[0.578, 0.845]` | `[0.845, 0.578]` | `[0.788, 0.788]` |

Biggest gaps: pen vs numpy `0.0004` (rounding to three places); numpy vs torch about `4e-08` (32-bit against 64-bit). Full marks for: the three rows equal to 3 places, and the sentence *"they differ only by rounding"*. A gap near `0.1` or more: Mistake 4 or 9.

### Page 14.4 — Two tables and the second pass (from `twotables.py` and `key.py` H2)

With one table for questions and keys the score table is symmetric. With `Wq = [[0, 0], [1, 0]]`:

| | |
|---|---|
| `Q` | the `[0, 0]`, cat `[1, 0]`, sat `[1, 0]` |
| Scores | `the [0, 0, 0]`, `cat [1, 0, 1]`, `sat [1, 0, 1]` |
| Weights | `the [0.333, 0.333, 0.333]`, `cat [0.422, 0.155, 0.422]`, `sat [0.422, 0.155, 0.422]` |
| Output | `the [0.667, 0.667]`, `cat [0.578, 0.845]`, `sat [0.578, 0.845]` |
| cat asks sat / sat asks cat | `1.0` / `0.0` |

Prediction answer: row `the` has equal weights because its question is all zeros, so every score is 0 and every exp is 1. Its answer is the plain mean of the values, `[0.667, 0.667]`. Scores are **not** symmetric (`False`).

### Page 14.6 — Break it on purpose (workbook bugs A-E)

**A** (silent): `e.sum()` is one total for the whole table; printed weights `[[0.44, 0.06], [0.06, 0.44]]`, row sums `0.5, 0.5`; fix `e / e.sum(axis=1).reshape(2, 1)`. **B** (silent): `v @ weights` instead of `weights @ v`; prints `[[9, 2], [2, 16]]` then `[[9, 1], [4, 16]]`; the top-right entry must be `0.9 x 0 + 0.1 x 20 = 2`. **C** (loud): `w.unsqueeze(0)` gives shape `(1, 3)`; last line `RuntimeError: The size of tensor a (3) must match the size of tensor b (2) at non-singleton dimension 1`; fix `unsqueeze(-1)`, blend `[6.5, 6.5]`. **D** (silent): `nn.Linear(2, 2)` keeps its random bias; seed 1 prints `[[2.334, 4.424]]` instead of `[[3.0, 4.0]]`; fix `bias=False`. **E** (silent): `nn.Linear` stores the table turned over; prints `[[2.0, 1.0]]` against the pen's `[[0.0, 1.0]]`; fix `.transpose(0, 1)`; the class tables (identity, swap) are their own transposes, so they never showed it.

### Page 14.5 — The homework check (from `hw.py`)

`hw.py` prints the weights and output of page 14.4 (the same six rows). The extension: with `Wv` changed to the identity and `Wq`, `Wk` as the class example, the weights are unchanged and the output is `[[0.845, 0.578], [0.578, 0.845], [0.788, 0.788]]`; doubling `Wv` doubles the output and leaves the weights alone (`key.py`).

### The teacher-only key: every number, and the reconciliation with the module

```python
# key.py - Week 14 TEACHER ONLY: every number in the answer key, computed. Never give this file to the student.
# It uses np.tril, np.where and a square root as a divisor; none of those is on the student's ladder this week.
import numpy as np

# --- D1: the class pass with a calculator: exps, totals, weights at 4 places, output at 3 ---
print("exp(0), exp(1), exp(2):", np.round([np.exp(0), np.exp(1), np.exp(2)], 4))
row_tot = [1 + 2 * np.exp(1), 1 + 2 * np.exp(1), 2 * np.exp(1) + np.exp(2)]
print("row totals:", np.round(row_tot, 3))
for name, sc in [("the", [1, 0, 1]), ("cat", [0, 1, 1]), ("sat", [1, 1, 2])]:
    s = np.exp(np.array(sc, dtype=float))
    print(name, "weights (4 dp):", np.round(s / s.sum(), 4), " sum of the 3-dp weights:", round(float(np.round(s / s.sum(), 3).sum()), 3))

X  = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
V  = X @ np.array([[0.0, 1.0], [1.0, 0.0]])
def soft(sc):
    e = np.exp(sc)
    return e / e.sum(axis=1).reshape(-1, 1)
W = soft(X @ X.T)
print("exact output (3 dp):", np.round(W @ V, 3).tolist())
W3 = np.round(W, 3)
print("output from the 3-dp weights (what a hand pass carrying 3 places gets):", np.round(W3 @ V, 3).tolist())
W4 = np.round(W, 4)
print("output from the 4-dp weights:", np.round(W4 @ V, 3).tolist())

# --- the river example: 42.77 by machine, 42.78 by hand with 3-dp weights ---
sc = np.array([0.1, 2.0, 0.3]); val = np.array([10.0, 50.0, 30.0])
w = np.exp(sc) / np.exp(sc).sum()
print("river exact:", round(float((w * val).sum()), 4), " with 3-dp weights:", round(float((np.round(w, 3) * val).sum()), 3),
      " exps:", np.round(np.exp(sc), 3).tolist(), " total:", round(float(np.exp(sc).sum()), 3))

# --- H1 (homework): a weighted average with weights that do NOT add to 1, and the fix ---
vals = np.array([10.0, 50.0, 30.0])
bad = np.array([0.7, 0.2, 0.2])
print("H1 bad weights sum:", bad.sum(), " result:", (bad * vals).sum(), " divided by the sum:", round(float((bad * vals).sum() / bad.sum()), 3))
print("H1 [0.5, 0.25, 0.25]:", (np.array([0.5, 0.25, 0.25]) * vals).sum(), "  [0, 1, 0]:", (np.array([0.0, 1.0, 0.0]) * vals).sum())

# --- H2 (homework): the pass with the question table [[0,0],[1,0]] ---
Wq2 = np.array([[0.0, 0.0], [1.0, 0.0]])
sc2 = (X @ Wq2) @ X.T
W2 = soft(sc2)
print("H2 scores:", sc2.tolist())
print("H2 weights:", np.round(W2, 3).tolist())
print("H2 output:", np.round(W2 @ V, 3).tolist())
print("H2 scores symmetric?", bool((sc2 == sc2.T).all()))

# --- TEACHER-ONLY: how today's numbers relate to the reference module's pass (divide by sqrt 2, hide the future) ---
sc_m = (X @ X.T) / 2 ** 0.5
sc_m = np.where(np.tril(np.ones((3, 3))) == 1, sc_m, -np.inf)
Wm = soft(sc_m)
print("module weights:", np.round(Wm, 4).tolist())
print("module output :", np.round(Wm @ V, 4).tolist())
# only the divide, no mask; only the mask, no divide
Wd = soft((X @ X.T) / 2 ** 0.5)
print("divide only, output:", np.round(Wd @ V, 3).tolist())
Wk_ = soft(np.where(np.tril(np.ones((3, 3))) == 1, X @ X.T, -np.inf))
print("mask only, output  :", np.round(Wk_ @ V, 3).tolist())

# --- extension: the ratio of two weights in a row is e^(score gap), nothing else matters ---
print("ratio w[2][2] / w[2][0]:", round(float(W[2][2] / W[2][0]), 3), " e^(2-1):", round(float(np.exp(1)), 3))

# --- TEACHER-ONLY: random tables (seed 0, as anyweights.py), is every answer inside the range of the values? ---
import torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)
x4 = torch.randn(5, 4)
r_q = nn.Linear(4, 4, bias=False); r_k = nn.Linear(4, 4, bias=False); r_v = nn.Linear(4, 4, bias=False)
w5 = F.softmax(r_q(x4) @ r_k(x4).transpose(-2, -1), dim=-1)
v5 = r_v(x4); o5 = w5 @ v5
inside = bool((o5 >= v5.min(dim=0).values - 1e-6).all() and (o5 <= v5.max(dim=0).values + 1e-6).all())
print("random tables: every answer inside the range of its column of values:", inside)
print("largest single weight in the 5x5 table:", round(w5.max().item(), 3), " smallest:", round(w5.min().item(), 3))

# --- extension: change only Wv; the weights cannot move, because Wv is not in the recipe for the weights ---
Wv_id = np.array([[1.0, 0.0], [0.0, 1.0]])
print("Wv = identity, weights unchanged:", bool((soft(X @ X.T) == W).all()), " output:", np.round(W @ (X @ Wv_id), 3).tolist())
print("Wv doubled, output:", np.round(W @ (X @ (2 * np.array([[0.0, 1.0], [1.0, 0.0]]))), 3).tolist())
```

```text
exp(0), exp(1), exp(2): [1.     2.7183 7.3891]
row totals: [ 6.437  6.437 12.826]
the weights (4 dp): [0.4223 0.1554 0.4223]  sum of the 3-dp weights: 0.999
cat weights (4 dp): [0.1554 0.4223 0.4223]  sum of the 3-dp weights: 0.999
sat weights (4 dp): [0.2119 0.2119 0.5761]  sum of the 3-dp weights: 1.0
exact output (3 dp): [[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]
output from the 3-dp weights (what a hand pass carrying 3 places gets): [[0.577, 0.844], [0.844, 0.577], [0.788, 0.788]]
output from the 4-dp weights: [[0.578, 0.845], [0.845, 0.578], [0.788, 0.788]]
river exact: 42.7668  with 3-dp weights: 42.78  exps: [1.105, 7.389, 1.35]  total: 9.844
H1 bad weights sum: 1.0999999999999999  result: 23.0  divided by the sum: 20.909
H1 [0.5, 0.25, 0.25]: 25.0   [0, 1, 0]: 50.0
H2 scores: [[0.0, 0.0, 0.0], [1.0, 0.0, 1.0], [1.0, 0.0, 1.0]]
H2 weights: [[0.333, 0.333, 0.333], [0.422, 0.155, 0.422], [0.422, 0.155, 0.422]]
H2 output: [[0.667, 0.667], [0.578, 0.845], [0.578, 0.845]]
H2 scores symmetric? False
module weights: [[1.0, 0.0, 0.0], [0.3302, 0.6698, 0.0], [0.2483, 0.2483, 0.5035]]
module output : [[0.0, 1.0], [0.6698, 0.3302], [0.7517, 0.7517]]
divide only, output: [[0.599, 0.802], [0.802, 0.599], [0.752, 0.752]]
mask only, output  : [[0.0, 1.0], [0.731, 0.269], [0.788, 0.788]]
ratio w[2][2] / w[2][0]: 2.718  e^(2-1): 2.718
random tables: every answer inside the range of its column of values: True
largest single weight in the 5x5 table: 0.361  smallest: 0.084
Wv = identity, weights unchanged: True  output: [[0.845, 0.578], [0.578, 0.845], [0.788, 0.788]]
Wv doubled, output: [[1.155, 1.689], [1.689, 1.155], [1.576, 1.576]]
```

### Answers to every question posed in the lesson

- *Who do you hear, in a hard lookup?* The best match only: `river`, 50.
- *What is the answer in a soft lookup?* 42.77 (42.78 by hand): mostly the river, a trace of the others.
- *Where have you seen scores turned into shares that add to 1?* The softmax of Week 13.
- *Can a weighted average be bigger than the biggest value?* No, not with non-negative weights that add to 1.
- *Why each row and not the whole table?* One row is one word's shares, which must add to 1 for that word (Mistake 1).
- *What shape after `xt.unsqueeze(0)`?* `(1, 3, 2)`.
- *Why is `w3.unsqueeze(-1)` of shape `(3, 1)`?* `w3` is `(3,)`; a length-1 axis is added at the end so it can multiply the `(3, 2)` values row by row.
- *Does numpy give your pen numbers?* To three places, if the weights were carried to four.
- *What do you expect about "cat asks sat" and "sat asks cat" with one table?* They are equal (the score table is symmetric).
- *Why does `the` get equal weights in the second pass?* Its question is all zeros.
- *What did we not do?* Learn the tables; divide the scores; hide the future; use positions. Weeks 15-17.
- *Which word pays the most attention to itself in the Pen Pass?* `sat`, 0.5761.
- *If you change only `Wv`, which numbers change?* The output. The weights do not: `Wv` is not in the recipe for the weights.

---

## 🔮 Next Week Preview

This section tells you what the next week builds on, so you can set it up in the wrap-up.

**Week 15 — Scale, Mask, and Many Heads.** Today's scores were small whole numbers. Next week they get big, and the student will *see* the softmax collapse onto one word, measure how fast the raw dot product grows with the width `d` (a sum of `d` independent terms has a spread that grows like `√d`, the one new maths idea, measured, not proved), and fix it with one division: the `÷ √2` that the reference module quietly used. Then the mask: the student will hide the future with `masked_fill(..., float("-inf"))` and `torch.tril`, and show by experiment why the mask is applied **before** the softmax, and what happens if it is `0` instead. Then many heads, with `.view(B, T, H, dh).transpose(1, 2)`. **Bring Week 14's `attention.py` and the Pen Pass sheet.** By the end of Week 15 the student should be able to redo today's pass with the divide and the mask and land on the reference module's numbers (`0.6698, 0.3302` for `cat`).
