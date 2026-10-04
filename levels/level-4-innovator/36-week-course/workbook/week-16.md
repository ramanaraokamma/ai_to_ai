# Workbook — Week 16: Where Am I? Positions and the Transformer Block

**Name:** ________________________________  **Date:** ______________

[⬅ Week 15](week-15.md) · [📖 Read the chapter first](../student-guide/week-16.md) · [Course Home](../README.md) · [Next ➡](week-17.md)

---

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the worked examples and in the answers came from real CPU runs (PyTorch 2.2.1, `torch.manual_seed(0)` where anything is random). The by-hand numbers (`1.8509 ...`) are plain arithmetic and will match exactly to four decimals. The random tables inside a run may differ on another PyTorch build; the `True`/`False` lines, the **shapes** and the **counts** will not.
>
> **Predict first, then run.** On pages 16.1, 16.3, 16.4 and 16.7 you write your guess *before* you run anything. A wrong guess is useful. A guess written after the run is not a guess.
>
> **Nothing is trained this week.** Every weight you meet is a seeded random number, or a number you type in. So a result here can say *"this machinery can or cannot tell the order"*. It cannot say *"the network understands the sentence"*. **There is no language model and no stand-in anywhere in this workbook.**
>
> Run everything from the folder that contains `l4lib/`. This week needs nothing new installed, and no file here downloads anything.
>
> Use a **calculator with an `e^x` key** (a phone will do, in airplane mode) and carry **four decimals** all the way. Rounding each `e^x` to 2 decimals in the middle is the usual reason a fourth decimal is off.

---

## ✅ Warm-Up (5 min)

Five quick questions about **last week** (scale, mask, heads).

**W1.** Why do we divide the attention scores by `sqrt(d_k)` before the softmax? Finish the sentence: *big dot products make the softmax ...* ________________________________

**W2.** A head is 64 numbers wide. What number do you divide the scores by? ____________

**W3.** The mask is applied **before / after** (circle one) the softmax, and the number that goes into the hidden places is ____________ .

**W4.** Somebody puts `0` in the hidden places instead. Does the future get weight 0 after the softmax? ____________ Why? ________________________________

**W5.** `x` is `(B, T, d)`. After `.view(B, T, H, dh).transpose(1, 2)` its shape is ( ____ , ____ , ____ , ____ ).

---

## 🙈 Page 16.1 — The Blind Reader (predict, then run)

Attention builds each answer from *that word's own vector* and from *the set of all the vectors*. It never looks at the seating. Today you test that claim on a **new sentence pair** that is not in the chapter.

The words have these ids: `the` = 0, `cat` = 1, `chased` = 2, `mouse` = 3, `big` = 4.

```text
a = the cat chased the mouse   ->  [0, 1, 2, 0, 3]
b = the mouse chased the cat   ->  [0, 3, 2, 0, 1]
perm = [3, 0, 4, 2, 1]         (a way to shuffle five words)
```

**Predict** `True` or `False` for each line. Fill in the "Guess" column **now**.

| # | The line says... | Guess, words only | Guess, with places |
|:--:|---|:--:|:--:|
| 1 | the first `the` and the second `the` get the same answer row | ________ | ________ |
| 2 | `cat` in sentence `a` (row 1) and `cat` in sentence `b` (row 4) get the same answer row | ________ | ________ |
| 3 | shuffle the words then attend equals attend then shuffle the answers | ________ | ________ |

One sentence: *why* do you expect line 1 to behave that way in the "words only" column? ________________________________________________

Now type and run `check161.py`. It defines everything it uses, so nothing has to be imported from an earlier file.

```python
# check161.py - Week 16 workbook page 16.1: is attention blind to order? A NEW sentence pair, with and without places.
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
d = 4
emb = nn.Embedding(5, d)                # ids: the = 0, cat = 1, chased = 2, mouse = 3, big = 4
pos_table = nn.Embedding(8, d)
Wq = nn.Linear(d, d, bias=False)
Wk = nn.Linear(d, d, bias=False)
Wv = nn.Linear(d, d, bias=False)


def attend(x):
    scores = Wq(x) @ Wk(x).transpose(-2, -1) / d ** 0.5
    return F.softmax(scores, dim=-1) @ Wv(x)


def words_only(ids):
    return emb(ids)


def with_places(ids):
    return emb(ids) + pos_table(torch.arange(len(ids)))


a = torch.tensor([0, 1, 2, 0, 3])       # the cat chased the mouse
b = torch.tensor([0, 3, 2, 0, 1])       # the mouse chased the cat
perm = torch.tensor([3, 0, 4, 2, 1])

for name, make in [("words only ", words_only), ("with places", with_places)]:
    out_a = attend(make(a))
    out_b = attend(make(b))
    print(name, "| 1st 'the' == 2nd 'the':", torch.allclose(out_a[0], out_a[3], atol=1e-6),
          "| 'cat' in a == 'cat' in b:", torch.allclose(out_a[1], out_b[4], atol=1e-6),
          "| shuffle-then-attend == attend-then-shuffle:",
          torch.allclose(attend(make(a[perm])), attend(make(a))[perm], atol=1e-6))

same = torch.tensor([0, 1, 2, 0, 3])
print("control: the same sentence twice, with places, equal:", torch.allclose(attend(with_places(same)), attend(with_places(a)), atol=1e-6))
print("identity shuffle, with places, True ?", torch.allclose(attend(with_places(a[torch.arange(5)])), attend(with_places(a))[torch.arange(5)], atol=1e-6))
```

```text
words only  | 1st 'the' == 2nd 'the': True | 'cat' in a == 'cat' in b: True | shuffle-then-attend == attend-then-shuffle: True
with places | 1st 'the' == 2nd 'the': False | 'cat' in a == 'cat' in b: False | shuffle-then-attend == attend-then-shuffle: False
control: the same sentence twice, with places, equal: True
identity shuffle, with places, True ? True
```

**Score your guesses:** ______ of 6 right.

The last two lines are **controls**. Say in a few words why each is `True` and why that is *not* a contradiction of the line above it: ________________________________________________

**Careful what you claim.** Write which of these is fully supported by this page. Circle it.

- (a) *"A transformer cannot tell order without positions."*
- (b) *"Attention with no mask and no positions cannot tell order, and here is the line that shows it."*

Why is the other one too big? (Hint: Week 15 added a mask.) ________________________________________________

---

## 🃏 Page 16.2 — The Seat Swap (by hand; you are the attention)

**Rules, as in class.** Three cards. Each card is its own query, key and value (`q = k = v = the number on the card`). The width is 1, so there is nothing to divide by.

- score = (my card) x (their card)
- weight = `e^score` / (the sum of the three `e^score` values)
- answer = the sum of (weight x their card)

Follow **only the card `2`**. In rounds 3 and 4 add the seat **stamp** (**0, 0.5, 1.0**, left to right) to each card *first*. The stamp belongs to the **seat**, not to the card.

**Worked example (done for you): the scores of round 1.** Cards `2, 1, 0`, card `2` at seat 1. Scores: `2 x 2 = 4`, `2 x 1 = 2`, `2 x 0 = 0`. So the scores are **4, 2, 0**.

Fill in the rest. **Four decimals.**

| Round | Seating | Cards after stamping | Scores (card `2` times each) | `e^score` | Weights (add to 1) | Answer |
|:--:|---|---|---|---|---|:--:|
| 1 | `2, 1, 0` | `2, 1, 0` | 4, 2, 0 | ______, ______, ______ | ______, ______, ______ | ________ |
| 2 | `0, 1, 2` | ______________ | ______________ | ______, ______, ______ | ______, ______, ______ | ________ |
| 3 | `2, 1, 0` | ______________ | ______________ | ______, ______, ______ | ______, ______, ______ | ________ |
| 4 | `0, 1, 2` | ______________ | ______________ | ______, ______, ______ | ______, ______, ______ | ________ |

*(In round 3 and 4, "the card `2`" has a stamp on it now. Follow the **seat** that held the card `2`, and use its stamped value as "my card".)*

**Check that the weights add to 1 before you compute the answer:** round 1 ______ round 2 ______ round 3 ______ round 4 ______

**Questions.**

**S1.** Rounds 1 and 2 use the same three cards. Did the answer change? ____________ Where did the card `2` sit in each? ________________________

**S2.** If I had told you *only* the three numbers on the cards, and not the order, could you have given a different answer for round 1 and round 2? ____________ What does that say about what attention used? ________________________________

**S3.** In round 4 the answer is close to the stamped value of the last card. Is your answer "the right answer"? Think about who chose the stamps and whether anything was trained. ________________________________________________

**S4.** Write the one thing that changed between round 2 and round 4, and the one thing that changed between round 1 and round 3: ________________________________

### Practice cards (not from class)

New cards: **`1, 2, 0`** and **`0, 2, 1`**. This time follow **the card `1`**. Same stamps `0, 0.5, 1.0`.

| Round | Seating | Seat you follow | Cards after stamping | Scores | Answer |
|:--:|---|:--:|---|---|:--:|
| P1 | `1, 2, 0` | ____ | ______________ | ______________ | ________ |
| P2 | `0, 2, 1` | ____ | ______________ | ______________ | ________ |
| P3 | `1, 2, 0` + stamps | ____ | ______________ | ______________ | ________ |
| P4 | `0, 2, 1` + stamps | ____ | ______________ | ______________ | ________ |

Check with the file below **after** you have written your answers.

```python
# check162.py - Week 16 workbook page 16.2: the Seat Swap, on PRACTICE cards (1, 2, 0 - not the class cards).
import torch
import torch.nn.functional as F


def seat_swap(cards, who, stamps=None, masked=False):
    """Follow the card at seat `who` (0 is the first seat). Returns scores, weights, answer."""
    x = torch.tensor(cards)
    if stamps is not None:
        x = x + torch.tensor(stamps)
    scores = x[who] * x
    if masked:
        seats = torch.arange(len(cards))
        scores = scores.masked_fill(seats > who, float("-inf"))
    w = F.softmax(scores, dim=0)
    return x.tolist(), scores.tolist(), [round(v, 4) for v in w.tolist()], round((w * x).sum().item(), 4)


stamps = [0.0, 0.5, 1.0]
rounds = [
    ("1", [1.0, 2.0, 0.0], None),
    ("2", [0.0, 2.0, 1.0], None),
    ("3", [1.0, 2.0, 0.0], stamps),
    ("4", [0.0, 2.0, 1.0], stamps),
]
for name, cards, st in rounds:
    who = cards.index(1.0)
    x, scores, w, ans = seat_swap(cards, who, st)
    print(f"round {name}: cards {cards} follow seat {who + 1}: cards used {x} scores {scores} weights {w} answer {ans}")

print("--- the mask: class cards, no stamps, follow the card 2 ---")
for name, cards in [("A  2, 1, 0", [2.0, 1.0, 0.0]), ("B  0, 1, 2", [0.0, 1.0, 2.0])]:
    who = cards.index(2.0)
    x, scores, w, ans = seat_swap(cards, who, masked=True)
    print(f"masked {name}: follow seat {who + 1}: scores {scores} weights {w} answer {ans}")
```

```text
round 1: cards [1.0, 2.0, 0.0] follow seat 1: cards used [1.0, 2.0, 0.0] scores [1.0, 2.0, 0.0] weights [0.2447, 0.6652, 0.09] answer 1.5752
round 2: cards [0.0, 2.0, 1.0] follow seat 3: cards used [0.0, 2.0, 1.0] scores [0.0, 2.0, 1.0] weights [0.09, 0.6652, 0.2447] answer 1.5752
round 3: cards [1.0, 2.0, 0.0] follow seat 1: cards used [1.0, 2.5, 1.0] scores [1.0, 2.5, 1.0] weights [0.1543, 0.6914, 0.1543] answer 2.0372
round 4: cards [0.0, 2.0, 1.0] follow seat 3: cards used [0.0, 2.5, 2.0] scores [0.0, 5.0, 4.0] weights [0.0049, 0.7275, 0.2676] answer 2.3539
--- the mask: class cards, no stamps, follow the card 2 ---
masked A  2, 1, 0: follow seat 1: scores [4.0, -inf, -inf] weights [1.0, 0.0, 0.0] answer 2.0
masked B  0, 1, 2: follow seat 3: scores [0.0, 2.0, 4.0] weights [0.0159, 0.1173, 0.8668] answer 1.8509
```

A match is **within 0.001**. Any line that differs is a calculator slip: find which step.

### Stretch: the mask leaks a little order (optional)

The last two lines above follow the card `2` with **the mask on** (a seat may look only at itself and the seats to its left) and **no stamps**.

Compare them with your round 1 and round 2 answers. In the mask version, do the two seatings give the same answer? ____________ Why not? (Think about what seat 1 is allowed to see.) ________________________________________________

Write one careful sentence that uses the word **"a little"**: ________________________________________________

---

## 📍 Page 16.3 — Places and `torch.arange`

A position table has **one row per place**. `torch.arange(T)` makes the place numbers `0, 1, ..., T-1`, and the table turns each number into a row of `d` numbers, which is **added** to the word's row.

**Predict** (no running yet).

| Expression | My prediction |
|---|---|
| `torch.arange(4)` prints | ________________________ |
| `torch.arange(3, 7)` prints | ________________________ |
| `torch.arange(3.0)` prints (look at the dots) | ________________________ |
| `nn.Embedding(10, 6)` holds how many numbers? | ____________ |
| shape of `pos_table(torch.arange(7))` with `pos_table = nn.Embedding(10, 6)` | ( ____ , ____ ) |
| shape of `pos_table(torch.arange(3, 7))` | ( ____ , ____ ) |
| the longest sentence this 10-row table can serve | ____________ words |
| In `emb(ids) + pos_table(torch.arange(4))`, if `ids = [0, 1, 2, 0]`, are rows 0 and 3 equal? | ____________ |
| the same, but **without** the position table | ____________ |

Now type and run `check163.py`.

```python
# check163.py - Week 16 workbook page 16.3: places, torch.arange, and the size of a position table.
import torch
import torch.nn as nn

torch.manual_seed(0)
print("torch.arange(4)      :", torch.arange(4).tolist())
print("torch.arange(3, 7)   :", torch.arange(3, 7).tolist())
print("torch.arange(3)      :", torch.arange(3))
print("torch.arange(3.0)    :", torch.arange(3.0))

pos_table = nn.Embedding(10, 6)
print("table shape          :", tuple(pos_table.weight.shape), " numbers:", pos_table.weight.numel())
print("pos_table(torch.arange(7)) shape:", tuple(pos_table(torch.arange(7)).shape))
print("pos_table(torch.arange(3, 7)) shape:", tuple(pos_table(torch.arange(3, 7)).shape))
print("longest sentence this table can serve:", pos_table.num_embeddings)

emb = nn.Embedding(5, 6)
ids = torch.tensor([0, 1, 2, 0])             # the id 0 appears twice
plain = emb(ids)
placed = emb(ids) + pos_table(torch.arange(4))
print("no places : row 0 == row 3 ?", torch.allclose(plain[0], plain[3]))
print("with places: row 0 == row 3 ?", torch.allclose(placed[0], placed[3]))
print("width of the big model table: 64 places x 128 =", 64 * 128)
```

```text
torch.arange(4)      : [0, 1, 2, 3]
torch.arange(3, 7)   : [3, 4, 5, 6]
torch.arange(3)      : tensor([0, 1, 2])
torch.arange(3.0)    : tensor([0., 1., 2.])
table shape          : (10, 6)  numbers: 60
pos_table(torch.arange(7)) shape: (7, 6)
pos_table(torch.arange(3, 7)) shape: (4, 6)
longest sentence this table can serve: 10
no places : row 0 == row 3 ? True
with places: row 0 == row 3 ? False
width of the big model table: 64 places x 128 = 8192
```

**P1.** How many of the nine predictions were right? ______ Which one surprised you most, and why? ________________________________________________

**P2.** Why does the position table need **one row per place** and not one row per word in the vocabulary? ________________________________________________

**P3.** A position table has 32 rows. A sentence is 40 words long. What happens, and in which week did you meet that kind of message? ________________________________________________

**P4.** Why does the model **add** the position row to the word row instead of sticking it on the end? (Think about the width of the vectors going into the next layer.) ________________________________________________

---

## 🔢 Page 16.4 — Count the Knobs of One Block

A block has **six** parts, in this order: layer norm, attention, residual add, layer norm, MLP, residual add. The knobs are in the layers with weights. The `GELU` has none. The **mask is not a knob** (it is a buffer).

### Part A — the class width, `d = 8` (fill in before you run anything)

Rules for counting: a `Linear(a, b)` has `a x b` weights **plus `b` biases** unless it says *no bias*. A `LayerNorm(d)` has `d` scales **and** `d` shifts.

**Worked example (done for you): `ln1`.** `LayerNorm(8)`: 8 scales + 8 shifts = 2 x 8 = **16**.

| Part | What it is | How to count | Knobs |
|---|---|---|:--:|
| `ln1` | `LayerNorm(d)` | 2 x d | 16 |
| `q` | `Linear(d, d)`, no bias | ______ | ______ |
| `k` | `Linear(d, d)`, no bias | ______ | ______ |
| `v` | `Linear(d, d)`, no bias | ______ | ______ |
| `proj` | `Linear(d, d)` with bias | ______ | ______ |
| `ln2` | `LayerNorm(d)` | ______ | ______ |
| `up` | `Linear(d, 4d)` with bias | ______ | ______ |
| `act` | `GELU()` | nothing to learn | ______ |
| `down` | `Linear(4d, d)` with bias | ______ | ______ |
| | | **total** | ______ |

Compare your total with your teacher's **before** you run anything.

### Part B — a new width, `d = 10` (not from class)

The formula is `12 x d x d + 10 x d`. Use it, then fill in the nine rows the long way and see whether they agree.

| Part | Knobs at `d = 10` |
|---|:--:|
| `ln1` | ______ |
| `q` | ______ |
| `k` | ______ |
| `v` | ______ |
| `proj` | ______ |
| `ln2` | ______ |
| `up` | ______ |
| `act` | ______ |
| `down` | ______ |
| **total, the long way** | ______ |
| **total, the formula** `12 x 10 x 10 + 10 x 10` | ______ |

Do the two totals agree? ____________

**More widths, using the formula only.** `d = 6`: ____________  `d = 12`: ____________  `d = 20`: ____________

**Does the number of heads change the count?** Try `H = 2` and `H = 5` at `d = 10`: ____________ . Explain in one sentence: ________________________________________________

**A width that cannot have 3 heads.** At `d = 10`, `d // 3 = ____`, and `3 x (d // 3) = ____` , which is not ____ . So the heads would not fill the width. (You will see this as an error on page 16.7.)

Now type and run `check164.py`.

```python
# check164.py - Week 16 workbook page 16.4: count the knobs of one block, on a PRACTICE width (d = 10).
import torch.nn as nn

d = 10
parts = [
    ("ln1   LayerNorm(d)          ", nn.LayerNorm(d)),
    ("q     Linear(d, d), no bias ", nn.Linear(d, d, bias=False)),
    ("k     Linear(d, d), no bias ", nn.Linear(d, d, bias=False)),
    ("v     Linear(d, d), no bias ", nn.Linear(d, d, bias=False)),
    ("proj  Linear(d, d)          ", nn.Linear(d, d)),
    ("ln2   LayerNorm(d)          ", nn.LayerNorm(d)),
    ("up    Linear(d, 4d)         ", nn.Linear(d, 4 * d)),
    ("act   GELU()                ", nn.GELU()),
    ("down  Linear(4d, d)         ", nn.Linear(4 * d, d)),
]
total = 0
for name, layer in parts:
    n = sum(p.numel() for p in layer.parameters())
    total = total + n
    print(f"{name} {n:5d}")
print("total at d = 10:", total)

for width in [6, 10, 12, 20]:
    print(f"d = {width:2d}:  12 x d x d + 10 x d =", 12 * width * width + 10 * width)

d = 10
print("d // H for H = 2:", d // 2, " for H = 5:", d // 5, " for H = 3:", d // 3, " and 3 x (d // 3) =", 3 * (d // 3))

print("--- a stack of blocks at d = 10 ---")
one = 12 * d * d + 10 * d
print("one block :", one)
print("three blocks:", 3 * one)
print("MLP part of one block (up + down):", (d * 4 * d + 4 * d) + (4 * d * d + d))
print("attention part (q, k, v, proj)   :", 4 * d * d + d)
print("two norms                        :", 4 * d)
print("MLP share of the block:", round(((d * 4 * d + 4 * d) + (4 * d * d + d)) / one, 3))
print("mask for T = 7 has", 7 * 7, "numbers, and they are not knobs")
```

```text
ln1   LayerNorm(d)              20
q     Linear(d, d), no bias    100
k     Linear(d, d), no bias    100
v     Linear(d, d), no bias    100
proj  Linear(d, d)             110
ln2   LayerNorm(d)              20
up    Linear(d, 4d)            440
act   GELU()                     0
down  Linear(4d, d)            410
total at d = 10: 1300
d =  6:  12 x d x d + 10 x d = 492
d = 10:  12 x d x d + 10 x d = 1300
d = 12:  12 x d x d + 10 x d = 1848
d = 20:  12 x d x d + 10 x d = 5000
d // H for H = 2: 5  for H = 5: 2  for H = 3: 3  and 3 x (d // 3) = 9
--- a stack of blocks at d = 10 ---
one block : 1300
three blocks: 3900
MLP part of one block (up + down): 850
attention part (q, k, v, proj)   : 410
two norms                        : 40
MLP share of the block: 0.654
mask for T = 7 has 49 numbers, and they are not knobs
```

### Part C — whose count is wrong? (`d = 8`, true answer from Part A)

Four classmates each made one slip at `d = 8`. For each wrong total, say what the slip must have been. **Work it out from your Part A table**; do not guess.

| Classmate's total | The slip (what did they add or leave out?) |
|:--:|---|
| 872 | ________________________________ |
| 832 | ________________________________ |
| 816 | ________________________________ |
| 840 | ________________________________ |
| 800 | ________________________________ (hint: three things left out) |

**Part D.** At `d = 10` the `up` layer has 440 knobs and the `down` layer 410. Both are "about `4 x d x d`". Why do they differ by 30? ________________________________________________

---

## 🧱 Page 16.5 — The Block, the Stack, and Where the Knobs Live

### The six parts in order

Number them 1 to 6 in the order a word's vector meets them. Then write, in a few words, what each one is **for**.

| Order | Part | What it is for |
|:--:|---|---|
| ____ | attention | ____________________________ |
| ____ | second residual add | ____________________________ |
| ____ | first layer norm | ____________________________ |
| ____ | the 4x MLP | ____________________________ |
| ____ | first residual add | ____________________________ |
| ____ | second layer norm | ____________________________ |

**Fill in:** *attention _____________ , the MLP _____________ , the adds keep the _____________ open.*

**Who talks to whom?** In the block, the nudge test changed places 3, 4 and 5 when place 3 was nudged, and the MLP alone changed only place 3. Which part lets a word hear about **other** words? ____________ Which works on each place **alone**? ____________

### A stack

A GPT is a stack of blocks. The output of one is the input of the next, so each block's output must have the **same shape** as its input. The blocks live in an `nn.ModuleList`, not in a plain list.

At `d = 10`: one block is ______ knobs, so three blocks are ______ knobs. (You have both numbers from page 16.4.)

**Where the knobs live at `d = 10`.** From the output of `check164.py`:

| | Knobs | Share of the block |
|---|:--:|:--:|
| attention (q, k, v, proj) | ______ | ______ |
| MLP (up + down) | ______ | ______ |
| two norms | ______ | ______ |
| **block** | ______ | 1.000 |

Which part has the most knobs? ____________ Is that the part most people call "the transformer"? ____________

### The whole TinyGPT of Week 17, by arithmetic only

Next week's model has **28 characters**, room for **64 places**, width `d = 128`, **4 blocks**, a final layer norm and an output layer `Linear(128, 28)`. One block at `d = 128` is `12 x 128 x 128 + 10 x 128`.

| Piece | How to count | Knobs |
|---|---|:--:|
| token table `Embedding(28, 128)` | 28 x 128 | ______ |
| position table `Embedding(64, 128)` | 64 x 128 | ______ |
| one block | `12 x 128 x 128 + 10 x 128` | ______ |
| four blocks | 4 x one block | ______ |
| final `LayerNorm(128)` | 2 x 128 | ______ |
| output `Linear(128, 28)` | 128 x 28 + 28 | ______ |
| **whole model** | add the pieces that are there | ______ |

Now type and run `check165.py` and compare.

```python
# check165.py - Week 16 workbook page 16.5: the whole TinyGPT of Week 17, by arithmetic only, then one real block to check.
import torch.nn as nn

D = 128
tok = 28 * D                       # one row of 128 numbers for each of 28 characters
pos = 64 * D                       # one row of 128 numbers for each of 64 places
block = 12 * D * D + 10 * D
final_norm = 2 * D
head = D * 28 + 28
print("token table     :", tok)
print("position table  :", pos)
print("one block       :", block)
print("four blocks     :", 4 * block)
print("final layer norm:", final_norm)
print("output layer    :", head)
print("whole model     :", tok + pos + 4 * block + final_norm + head)

# a real layer-by-layer check of the pieces that are not a block
print("check: Embedding(28, 128)  :", nn.Embedding(28, 128).weight.numel())
print("check: Embedding(64, 128)  :", nn.Embedding(64, 128).weight.numel())
print("check: LayerNorm(128)      :", sum(p.numel() for p in nn.LayerNorm(128).parameters()))
print("check: Linear(128, 28)     :", sum(p.numel() for p in nn.Linear(128, 28).parameters()))

print("--- the same model with 2 blocks and room for 32 places ---")
print("whole model     :", tok + 32 * D + 2 * block + final_norm + head)
```

```text
token table     : 3584
position table  : 8192
one block       : 197888
four blocks     : 791552
final layer norm: 256
output layer    : 3612
whole model     : 807196
check: Embedding(28, 128)  : 3584
check: Embedding(64, 128)  : 8192
check: LayerNorm(128)      : 256
check: Linear(128, 28)     : 3612
--- the same model with 2 blocks and room for 32 places ---
whole model     : 407324
```

**Write it as a promise.** *"Next week I will build a model and `sum(p.numel() for p in model.parameters())` will print ____________ ."* If it prints something else, the first place to look is ________________________________ .

**Honest limit.** This count tells you how many knobs there are. It tells you nothing about whether a model with that many is any good. Write one thing it does **not** tell you: ________________________________________________

---

## 🏗️ Page 16.6 — The Build: `my_shuffle.py`

Write a file that runs the shuffle test on **your own sentence**, without places and with places. You may start from `check161.py`, but the sentence, the vocabulary and the shuffle must be yours.

**Plan (fill in before you type).**

Vocabulary (one id per different word; ids must start at 0): ________________________________________________

My sentence (six or more words, at least one word twice): ________________________________________________

Its ids: [ ______________________ ]  Largest id: ______  So the word table needs at least ______ rows.

Number of words: ______ . The places I need are `0` to ______ , so the position table needs at least ______ rows. I will make it ______ rows.

My `perm` (the same length as the sentence; each place number once): [ ______________________ ]

**Your file must print, with `torch.manual_seed(0)` at the top:**

1. the number of words, the largest id, and the number of rows in each table,
2. shuffle-then-attend equals attend-then-shuffle, **words only**,
3. the same line **with places**,
4. a shuffle that gives `True` *even with places* (which one is it?),
5. the number of knobs in the two tables.

**Predict the three `True`/`False` answers (lines 2, 3, 4) for your sentence:** ______ , ______ , ______ .

After you run it: did any guess fail? ____________ If so, which, and what did you learn? ________________________________________________

**A line to add.** Print the knobs of `Wq`, `Wk` and `Wv` together with `sum(p.numel() for p in [...])`, or write "left for Week 17". Mine: ________________________________

**Marking yourself (one mark each).**

| Criterion | Mark |
|---|:--:|
| A sentence of six or more words, with a repeated word | ☐ |
| The word table has enough rows for the largest id, and the place table enough rows for the sentence | ☐ |
| Words only prints `True` for the shuffle test | ☐ |
| With places prints `False`, and a shuffle that moves nothing prints `True` | ☐ |
| A sentence that says **"attention on its own is blind to order; positions tell it the order on purpose"** (or equivalent), not "the model understands" | ☐ ☐ |

Total: ______ / 6.

---

## 🐞 Page 16.7 — Break It on Purpose

Every program below is **deliberately broken**. Do not fix it until you have done the "Predict" line. Then copy it, run it, read the **last line** (or the odd number), and fix it. Each program is self-contained. **Four of the nine are silent**: they run, and the only sign is a number you must check.

**Program 1 (deliberate).**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)


class Stack(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.layers = [nn.Linear(2, 2) for _ in range(n)]

    def forward(self, x):
        for layer in self.layers:
            x = torch.tanh(layer(x))
        return x


model = Stack(3)
print("output shape:", tuple(model(torch.ones(4, 2)).shape))
opt = torch.optim.AdamW(model.parameters(), lr=0.01)
```

Predict: runs or error? ____________ Does the first `print` line appear? ____________ Last line: ________________________________ Fix: ________________________

**Program 2 (deliberate, SILENT).**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)


class Stack(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.layers = [nn.Linear(2, 2) for _ in range(n)]
        self.out = nn.Linear(2, 1)

    def forward(self, x):
        for layer in self.layers:
            x = torch.tanh(layer(x))
        return self.out(x)


model = Stack(3)
print("knobs PyTorch can see:", sum(p.numel() for p in model.parameters()))
print("knobs I meant        :", 3 * (2 * 2 + 2) + (2 + 1))
```

Predict the two numbers: ______ and ______ . Printed: ______ and ______ . Why is there **no error** this time, when Program 1 had one? ________________________________ Fix: ________________________

**Program 3 (deliberate).**

```python
import torch
import torch.nn as nn

pos_table = nn.Embedding(6, 3)
places = torch.arange(4.0)
print(places)
print(pos_table(places).shape)
```

Predict: ________________ What does the first `print` already show you? ________________ Last line: ________________________________ Fix: ________________

**Program 4 (deliberate).**

```python
import torch
import torch.nn as nn

pos_table = nn.Embedding(6, 3)
sentence_length = 9
print(pos_table(torch.arange(sentence_length)).shape)
```

Predict: ________________ Last line: ________________________________ The largest sentence this table can take: ______ words. Two different fixes: ________________________________

**Program 5 (deliberate, SILENT).**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
d = 4
emb = nn.Embedding(4, d)
pos_table = nn.Embedding(8, d)


def with_places(ids):                     # ids is (B, T): B sentences, T words each
    B, T = ids.shape
    return emb(ids) + pos_table(torch.arange(B))


ids = torch.tensor([[0, 1, 2, 0, 3]])     # one sentence of five words
x = with_places(ids)
print("shape:", tuple(x.shape))
print("word 0 and word 3 are both the id 0; same input row?", torch.allclose(x[0, 0], x[0, 3]))
```

Predict the second line (`True` or `False`) **if the places were working**: ____________ . Printed: ____________ . Shapes are fine. What tells you something is wrong? ________________________________ Which letter should `torch.arange(...)` get, `B` or `T`? ____________ Fix: ________________________

**Program 6 (deliberate, SILENT).** The MLP's last layer is set to zeros, as in the chapter's "switch the add-on off" test. The block *should* hand its input back.

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
d = 6
ln = nn.LayerNorm(d)
up = nn.Linear(d, 4 * d)
act = nn.GELU()
down = nn.Linear(4 * d, d)
with torch.no_grad():
    down.weight.fill_(0.0)
    down.bias.fill_(0.0)

x = torch.randn(1, 5, d)
y = down(act(up(ln(x))))
print("MLP switched off, output equals input:", torch.allclose(y, x))
print("largest number in the output:", y.abs().max().item())
```

Predict the first line, **if the residual were there**: ____________ . Printed: ____________ . What is missing from the line `y = ...`? ________________ Fix: ________________________

**Program 7 (deliberate).**

```python
import torch
import torch.nn as nn

d = 6
norm_after_up = nn.LayerNorm(d)
up = nn.Linear(d, 4 * d)
x = torch.ones(1, 5, d)
print(norm_after_up(up(x)).shape)
```

Predict: ________________ Last line: ________________________________ The two numbers that tell the story: ______ and ______ . Fix: ________________

**Program 8 (deliberate).**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
d, H = 10, 4
q = nn.Linear(d, d, bias=False)
x = torch.randn(1, 5, d)
B, T, _ = x.shape
heads = q(x).view(B, T, H, d // H)
print(heads.shape)
```

Predict: ________________ Last line: ________________________________ Work it out: `1 x 5 x 4 x (10 // 4)` is ______ , but there are ______ numbers. Give two pairs `(d, H)` that would work: ________________

**Program 9 (deliberate, SILENT on a CPU).**

```python
import torch
import torch.nn as nn


class Masked(nn.Module):
    def __init__(self, T):
        super().__init__()
        self.lin = nn.Linear(3, 3)
        self.mask = torch.tril(torch.ones(T, T))


m = Masked(4)
print("the mask is there:", tuple(m.mask.shape))
print("saved entries   :", list(m.state_dict().keys()))
```

Predict the second line: ________________________________ Is the mask in it? ____________ Printed: ________________________________ Fix: ________________________

**The habit each silent program teaches.**

| Program | The check I run before I trust the model |
|:--:|---|
| 2 | ________________________________ |
| 5 | ________________________________ |
| 6 | ________________________________ |
| 9 | ________________________________ |

---

## 📓 Page 16.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Add a row for every real error you hit this week, not only the deliberate ones.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more; this week there were four): write the one I made, or nearly made. ________________________________________________

**The habit for silent mistakes.** Fill in the blanks: *after I write a model, I count the* ____________ *and compare with my* ____________ *count; after I add positions, I run the* ____________ *test; after I write a block, I switch the add-ons off and check that the output* ____________ *the input.*

Write this sentence in your own handwriting:

> **"Count the knobs, shuffle the words, and never say the block understands."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **Why can attention not tell "the cat chased the mouse" from "the mouse chased the cat"?**

________________________________________________________________

2. **What does adding a position vector do? Why does the table have one row per place?**

________________________________________________________________

3. **Name the parts of one block in order, and say which part lets words talk to each other.**

________________________________________________________________

4. **What is `nn.ModuleList` for? What goes wrong with a plain list, and why is it worse when the model also has one ordinary layer?**

________________________________________________________________

5. **What is `register_buffer` for? Is the mask one of the knobs?**

________________________________________________________________

6. **Your friend says "a transformer cannot tell order without positions, so a GPT with no positions is broken".** What do you say? Use "attention on its own" and "a little" in your answer.

________________________________________________________________

7. *Parking Lot.* The chapter adds the position vector instead of joining it on the end. Do **not** claim that adding is better. Write one experiment you could run to compare them, and what you would have to count: ________________________________

**Mark yourself.** Tick the first line you can honestly say.

- [ ] **Not yet:** I cannot say why shuffling the words does not change attention's answers.
- [ ] **Developing:** I get the Seat Swap with help, and I can list the parts of the block, but my count is off by a bias or two.
- [ ] **Secure:** I get the four Seat Swap answers, see `True` become `False` when places are added, get 848 by hand at `d = 8`, and name the six parts in order.
- [ ] **Fluent:** I counted a block at a width I chose using `12 d^2 + 10 d`, explained why the mask still leaks a little, predicted every `True`/`False` on page 16.1, and wrote "attention on its own" rather than "a transformer".

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-16.md) · [Next ➡](week-17.md)

---
---

# ✂️ ANSWERS - keep this page folded until you have finished

*Numbers come from real runs: CPU, PyTorch 2.2.1, `torch.manual_seed(0)` wherever anything is random. The by-hand numbers are plain arithmetic and should match to four decimals (within 0.0001 of rounding). Random tables may differ on another build; the `True`/`False` lines, the shapes and the counts should not.*

### Warm-Up

- **W1.** ...saturate: one weight near 1 and the rest near 0. Dividing by `sqrt(d_k)` keeps the scores' spread about the same whatever the width.
- **W2.** `sqrt(64)` = **8**.
- **W3.** **Before**; `-inf` (`float("-inf")`).
- **W4.** No. `e^0 = 1`, so the hidden places still get weight: the future leaks in.
- **W5.** `(B, H, T, dh)`.

### Page 16.1

| # | Words only | With places |
|:--:|:--:|:--:|
| 1 | True | False |
| 2 | True | False |
| 3 | True | False |

- *Why line 1 is `True` without places:* both `the`s have the same vector, and each answer is built from that word's own vector and the whole set of vectors, which is the same room for both. The seating never enters.
- *Controls.* The same sentence twice gives the same answer (same input, same weights). A shuffle that moves nothing (the identity) obviously gives `True` even with places. Neither contradicts the line above: the line above is about a shuffle that **does** move words.
- **Careful what you claim.** Circle **(b)**. (a) is too big: a GPT hides the future with a mask (Week 15), and a mask is itself a weak clue about position (the first word sees only itself). The chapter's `masked.py` shows the shuffle test is `False` even with no positions. The honest sentence is *"attention on its own is blind to order, and positions are how a GPT is told the order on purpose."*

### Page 16.2

Class cards, follow the card `2`:

| Round | Cards after stamping | Scores | `e^score` | Weights | Answer |
|:--:|---|---|---|---|:--:|
| 1 | `2, 1, 0` | 4, 2, 0 | 54.5982, 7.3891, 1.0000 | 0.8668, 0.1173, 0.0159 | **1.8509** |
| 2 | `0, 1, 2` | 0, 2, 4 | 1.0000, 7.3891, 54.5982 | 0.0159, 0.1173, 0.8668 | **1.8509** |
| 3 | `2.0, 1.5, 1.0` | 4.0, 3.0, 2.0 | 54.5982, 20.0855, 7.3891 | 0.6652, 0.2447, 0.0900 | **1.7876** |
| 4 | `0.0, 1.5, 3.0` | 0.0, 4.5, 9.0 | 1.0000, 90.0171, 8103.0839 | 0.0001, 0.0110, 0.9889 | **2.9832** |

(The `e^score` column is arithmetic; the weights, answers and stamped cards are also printed by the course's own check run. Within 0.001 is a match.)

- *Round 3 and 4 detail.* In round 3 the card `2` is at seat 1 with stamp 0, so "my card" is 2.0. In round 4 the card `2` is at seat 3 with stamp 1.0, so "my card" is **3.0** (not 2) and the scores are 3 x [0, 1.5, 3] = 0, 4.5, 9. A common slip is to keep using 2 as "my card".
- **S1.** No, the answer did not change: **1.8509** both times. The card `2` sat at the left end in round 1 and the right end in round 2.
- **S2.** No. It is the same answer, so attention used only the cards and *which cards are in the room*, never the order.
- **S3.** No "right" answer exists. We chose the stamps, and nothing has been trained. It just **depends on the seat** now.
- **S4.** Between round 1 and round 3 (and between round 2 and round 4) the only change is the seat stamps added to the cards. Same cards, same seats: `1.8509` becomes `1.7876` (round 3) and `1.8509` becomes `2.9832` (round 4).

**Practice cards** (follow the card `1`):

| Round | Seat followed | Cards after stamping | Scores | Answer |
|:--:|:--:|---|---|:--:|
| P1 | 1 | `1, 2, 0` | 1, 2, 0 | **1.5752** |
| P2 | 3 | `0, 2, 1` | 0, 2, 1 | **1.5752** |
| P3 | 1 | `1.0, 2.5, 1.0` | 1.0, 2.5, 1.0 | **2.0372** |
| P4 | 3 | `0.0, 2.5, 2.0` | 0.0, 5.0, 4.0 | **2.3539** |

Weights: P1 `0.2447, 0.6652, 0.0900`; P2 `0.0900, 0.6652, 0.2447`; P3 `0.1543, 0.6914, 0.1543`; P4 `0.0049, 0.7275, 0.2676`. In P4 the card `1` is at seat 3 with stamp 1.0, so "my card" is **2.0**.

**Stretch (mask).** Masked, no stamps: seatings A and B give **2.0000** and **1.8509**. Not the same. In seating A the card `2` is at seat 1, which may look only at itself, so its weights are `1, 0, 0` and its answer is its own value. In seating B the card is at seat 3 and sees all three cards. So the mask gives the seats **different jobs**, which tells the model something about place. A careful sentence: *"The mask leaks a little order even with no places, because the first seat can see only itself."* Not shown: that this is enough to read order well (the chapter notes a GPT without positions is worse, not broken, in the course's own ablation; one seed).

### Page 16.3

| Expression | Answer |
|---|---|
| `torch.arange(4)` | `tensor([0, 1, 2, 3])` (`[0, 1, 2, 3]` with `.tolist()`) |
| `torch.arange(3, 7)` | 3, 4, 5, 6 (four numbers; the end is **not** included) |
| `torch.arange(3.0)` | `tensor([0., 1., 2.])` (the dots show it is a float tensor) |
| `nn.Embedding(10, 6)` | 10 x 6 = **60** |
| `pos_table(torch.arange(7))` | **(7, 6)** |
| `pos_table(torch.arange(3, 7))` | **(4, 6)** |
| longest sentence | **10** words (places 0 to 9) |
| rows 0 and 3 with the position table | **False** |
| without it | **True** |

- **P2.** A place is a *number along the sentence* (0, 1, 2 ...), not a word. The table is indexed by place, so it needs as many rows as the longest sentence the model will be asked to read, whatever the vocabulary size.
- **P3.** An `IndexError: index out of range in self`. Same kind of message as Week 8 (an id beyond the table). The table's number of rows is the model's **context length**.
- **P4.** Adding keeps the width at `d`, so every later layer keeps the same shape. Joining the two would make the vectors wider. (Honest note: joining was not tested in this course, so neither is claimed to be better.)
- Common slip: `torch.arange(3, 7)` answered as 3 to 7 inclusive (five numbers).

### Page 16.4

**Part A, `d = 8`.**

| Part | How to count | Knobs |
|---|---|:--:|
| `ln1` | 2 x 8 | 16 |
| `q` | 8 x 8 | 64 |
| `k` | 8 x 8 | 64 |
| `v` | 8 x 8 | 64 |
| `proj` | 8 x 8 + 8 | 72 |
| `ln2` | 2 x 8 | 16 |
| `up` | 8 x 32 + 32 | 288 |
| `act` | nothing to learn | 0 |
| `down` | 32 x 8 + 8 | 264 |
| | **total** | **848** |

**Part B, `d = 10`.** `ln1` 20, `q` 100, `k` 100, `v` 100, `proj` 110, `ln2` 20, `up` 440, `act` 0, `down` 410. Total **1300**; formula `12 x 100 + 100` = **1300**. They agree.

More widths: `d = 6` **492**; `d = 12` **1848**; `d = 20` **5000**.

Heads: **no** change; the formula has no `H` in it, because the heads share the same `d x d` matrices between them (they are slices of one wide matrix). At `d = 10`: `d // 3 = 3`, `3 x 3 = 9`, which is not **10**.

**Part C.**

| Total | The slip |
|:--:|---|
| 872 | A bias added on `q`, `k` and `v` (3 x 8 = 24 extra). |
| 832 | Each layer norm counted as `d` instead of `2d` (two norms, 8 fewer each: 16 fewer). |
| 816 | The bias of `up` forgotten (32 fewer). |
| 840 | The bias of `proj` forgotten (8 fewer). `down`'s bias forgotten also gives 840; either is fine. |
| 800 | All three biases forgotten: `proj` (8), `up` (32), `down` (8) = 48 fewer. |

**Part D.** `up` is `10 x 40 + 40` (weights plus 40 biases, one per output); `down` is `40 x 10 + 10` (weights plus 10 biases). Same weights, 400 each; the biases differ: 40 against 10, a difference of **30**. A bias belongs to the **output** of a layer.

Common errors: forgetting a bias; counting `LayerNorm` as `d`; counting the mask (36 or 49 numbers) as knobs; counting `GELU` as non-zero.

### Page 16.5

Order: **1** first layer norm, **2** attention, **3** first residual add, **4** second layer norm, **5** the 4x MLP, **6** second residual add.

- Layer norm: steadies the numbers before the layer sees them. Attention: lets each word gather from the words it is allowed to see. Residual add: hands the input along, so the road stays open and the layer's result is an add-on. MLP: works on each place by itself, thinks about what was gathered.
- *Fill in:* attention **gathers** (words talk), the MLP **thinks** (each word alone), the adds keep the **road** open.
- **Who talks to whom?** Attention; the MLP.

**Stack.** At `d = 10`: one block **1300**, three blocks **3900**. Attention **410**, MLP **850**, norms **40**; shares `410 / 1300 = 0.315`, `850 / 1300 = 0.654`, `40 / 1300 = 0.031`; the shares sum to 1.000 (within rounding). The MLP has the most knobs. No: people call the whole thing "attention", but about two thirds of a block's knobs are in the MLP.

**TinyGPT.** Token table **3584**; position table **8192**; one block **197888**; four blocks **791552**; final norm **256**; output layer **3612**; whole model **807196** (3584 + 8192 + 791552 + 256 + 3612). *Promise:* it will print **807196**; if not, check first the sizes you gave the tables, the block's width, or whether a list was used where `nn.ModuleList` belongs (page 16.7, Programs 1 and 2). The 2-block, 32-place variant is 407324.

Honest limit (any one): whether the model is any good; whether 4 blocks is a good number; whether the knobs are useful; how well it reads text.

### Page 16.6

Any sentence of six or more words with a repeated word. The sample answer (sentence `the big cat chased the mouse`, ids `[0, 4, 1, 2, 0, 3]`, `perm = [5, 3, 0, 1, 4, 2]`, seed 0) printed:

```text
words: 6  largest id: 4  rows in emb: 5
places needed: 0 to 5  rows in pos_table: 8
words only  shuffle-then-attend == attend-then-shuffle: True
with places shuffle-then-attend == attend-then-shuffle: False
with places, perm = 0,1,2,3,4,5 (nothing moves): True
knobs in the two tables: 20 + 32 = 52
```

Required: the word table needs at least `largest id + 1` rows; the position table needs at least as many rows as words; `perm` is a shuffle of `0..n-1`, each number once. Guesses: **True, False, True**. The identity shuffle must give `True` with places. A write-up that says "the model understands the sentence" loses the last two marks.

| Criterion | Marks |
|---|:--:|
| Six or more words, with a repeated word | 1 |
| Table sizes large enough | 1 |
| Words only `True` | 1 |
| With places `False`, and nothing-moves shuffle `True` | 1 |
| The sentence "attention on its own is blind to order; positions tell it the order on purpose" (or equivalent) | 2 |

### Page 16.7

- **Program 1.** Error. The first `print` **does** appear (`output shape: (4, 2)`): the model runs. Last line: `ValueError: optimizer got an empty parameter list`. The layers are in a plain list, so PyTorch cannot see them: no knobs. Fix: `self.layers = nn.ModuleList([...])`.
- **Program 2.** Prints `knobs PyTorch can see: 3` and `knobs I meant        : 21`. No error because the model also has one real layer (`self.out`, 2 + 1 = 3 knobs), so the optimizer always finds something; the three listed layers would never train. Fix: `nn.ModuleList`. Habit: count the knobs and compare with your hand count before training.
- **Program 3.** Error. The first `print` shows `tensor([0., 1., 2., 3.])`, the dots mean floats. Last line: `RuntimeError: Expected tensor for argument #1 'indices' to have one of the following scalar types: Long, Int; but got torch.FloatTensor instead (while checking arguments for embedding)`. Fix: `torch.arange(4)`.
- **Program 4.** Error. `IndexError: index out of range in self`. Six rows means places 0 to 5, so **6** words at most; a sentence of 9 asks for places 6, 7 and 8. Fixes: a bigger table (`nn.Embedding(9, 3)` or more), or a shorter sentence.
- **Program 5.** Prints `shape: (1, 5, 4)` and `... same input row? True`. If places were working: **False**. The `True` tells you the two `the`s are still the same input. `B` is the number of **sentences** (1); the places must be `torch.arange(T)`, the number of **words** (5). With `arange(B)` the single row for place 0 is added to every word. Habit: run the shuffle test (or this two-`the` test) after writing position code.
- **Program 6.** Prints `MLP switched off, output equals input: False` and `largest number in the output: 0.0`. With the residual it would be **True**. Missing: the `x +`. Fix: `y = x + down(act(up(ln(x))))`. Habit: switch the add-ons off and check the block hands its input back.
- **Program 7.** Error. Last line: `RuntimeError: Given normalized_shape=[6], expected input with shape [*, 6], but got input of size[1, 5, 24]`. The two numbers: **6** and **24**. The layer norm was placed after `up`, where the width is `4d = 24`. Fix: norm the width-`d` stream (`nn.LayerNorm(d)` applied to `x` before `up`), or `nn.LayerNorm(4 * d)` if the norm really goes after `up`.
- **Program 8.** Error. Last line: `RuntimeError: shape '[1, 5, 4, 2]' is invalid for input of size 50`. `1 x 5 x 4 x 2` = **40**, but there are **50**. Pairs that work: `(d, H) = (8, 2)`, `(8, 4)`, `(12, 3)`, `(10, 5)`, `(10, 2)`. Habit: check `H x (d // H) = d`.
- **Program 9.** Prints `the mask is there: (4, 4)` and `saved entries   : ['lin.weight', 'lin.bias']`. The mask is **not** in the list. Nothing is wrong on a CPU, but the mask is not saved with the model. Fix: `self.register_buffer("mask", torch.tril(torch.ones(T, T)))`. Habit: print `list(m.state_dict().keys())` and read it.

| Program | The check |
|:--:|---|
| 2 | Count the knobs and compare with the hand count. |
| 5 | The shuffle test: it must print `False` once places are added. |
| 6 | Switch the add-ons off; the block must hand `x` straight back (`True`). |
| 9 | Print `list(m.state_dict().keys())` and look for the mask. |

(Tracebacks on your machine will show your own file paths and a few lines inside `torch`. The **last line** is the one that matters.)

### Bug Log and Self-Check

Bug Log: any real entries are fine if the **last line** (not the whole traceback) was copied and the fix works. The four no-traceback mistakes of the week are Programs 2, 5, 6 and 9. Habit blanks: **knobs**, **hand**, **shuffle**, **equals**.

1. Each answer is built from that word's own vector and the set of all the vectors; the seating never enters. Shuffle the words and you only shuffle the answers (and two copies of one word get identical answers).
2. It makes each word's vector depend on where the word sits, so the same word in two places is no longer the same input. The table is indexed by place, so it has one row per place up to the longest sentence allowed (the context length).
3. Layer norm, attention, residual add, layer norm, MLP, residual add. Attention lets words talk to each other; the MLP works on each place alone.
4. `nn.ModuleList` is a list PyTorch can look inside, so the optimizer finds the knobs of the stack. With a plain list and no other layer you get an error (`empty parameter list`). With one ordinary layer beside it there is **no** error: the optimizer sees only that layer, and the rest never train.
5. A buffer is a tensor that belongs to the model (saved, moved with it) without being a knob. No: the mask has `T x T` numbers and none is counted.
6. "Attention on its own is blind to order. A GPT also hides the future with a mask, and that leaks **a little** order, so a GPT with no positions is worse (in this course's own test that took the positions out, best validation loss 1.632 against 1.278, one seed), not broken."
7. Reading, not proof. Experiment: build two position schemes, one adding and one joining with `torch.cat`, train each with the same seed and the same data, and compare the validation loss over several seeds (counting the extra knobs in the next layer, since joining makes the vectors wider). Do not claim either is better without the comparison.

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-16.md) · [Next ➡](week-17.md)
