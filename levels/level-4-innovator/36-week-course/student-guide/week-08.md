# Week 8 — Order Matters: A Cell That Remembers

[⬅ Week 7](week-07.md) · [Course Home](../README.md) · [Week 9 ➡](week-09.md) · [Workbook](../workbook/week-08.md)

---

> ### This week in one sentence
> **A bag of words throws the order away; a recurrent cell reads the words one at a time, in order, and rewrites a small summary after each one, using the same rule every time.**
>
> **By the end of this chapter you will be able to:**
> - **Show with counts** that "the dog bit the postman" and "the postman bit the dog" give a bag of words the same row
> - **Explain `nn.Embedding(V, d)`** as a table with one row per word, and say the shape of a lookup before you run it
> - **Unroll a 4-step recurrent cell by hand** and show that `nn.RNN` prints the same four numbers
> - **State the three shapes** of `x`, `out` and `h_n`, and say which one is the summary of the whole sentence
> - **Show two sentences with the same bag ending in different final summaries (the "hidden state", defined below)**, and say why the number of weights does not grow when the sentence does
>
> **New maths:** **none.** The cell is "multiply, add, squash with `tanh`", which you did in Level 3 (a neuron). The only new thinking is that the answer of one step is fed into the next.
>
> **New syntax:** `nn.Embedding(V, d)` · `nn.RNN(..., batch_first=True)` · `out, h_n = rnn(x)`
>
> **Reading time:** about 30 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60-75 minutes.

> **📌 About the code blocks.** Each block is a whole file, with its name in the first line. Type the files into **one folder, next to `l4lib/`**, and run them from that folder. Every output shown was printed by a real run on a CPU with seeds set. The by-hand numbers match to every digit. The random tables (from `torch.manual_seed(0)`) may differ on a different PyTorch version; the `True`/`False` lines and the shapes will not. Lines that report **seconds** depend on your machine. Blocks marked **DELIBERATE** are written on purpose to behave in a way you must notice. Nothing this week needs the internet. There is no language model and no stand-in anywhere: `nn.Embedding` and `nn.RNN` are real PyTorch layers, but **none of them has learned anything yet**. Their numbers are seeded random numbers, or numbers we type in.

---

![Map of the 36 weeks with Week 8, Order Matters, highlighted in Term 1](../figures/fig-w08-0-where-this-fits.svg)
*Figure 8.0 — Week 8 introduces the recurrent cell, the first model in the course that reads in order.*

## 🪝 Start Here

Last year your sentiment engine counted words. Here are two sentences:

> *The dog bit the postman.*
> *The postman bit the dog.*

Say them aloud. Same news? Which one would you rather be in?

**Before you open the laptop**, take workbook page 8.1. It gives you a grid with the columns `the`, `dog`, `bit`, `postman`. Tally both sentences into it. Write what you find in pen.

A few words to keep in mind:

- A **bag of words** is a count of how many times each word appears. Where the word sits is not recorded.
- A **sequence** is a list where position matters.
- A **model that reads in order** has to carry a summary of what it has read so far.

---

## 🧠 The Big Idea

### 1. What a bag keeps, and what it throws away

Check your tally on the computer. This file has no torch in it.

**`bag.py`**

```python
# bag.py - Week 8: what a bag of words keeps, and what it throws away. No torch yet.
a = "the dog bit the postman"
b = "the postman bit the dog"

vocab = ["the", "dog", "bit", "postman"]


def bag(sentence):
    words = sentence.split()
    return [words.count(w) for w in vocab]


print("vocab      ", vocab)
print("bag of a   ", bag(a))
print("bag of b   ", bag(b))
print("same bag?  ", bag(a) == bag(b))
print("same text? ", a == b)

# How many orderings share one bag? Five different words can be lined up 5 x 4 x 3 x 2 x 1 ways.
n = 1
for k in range(1, 6):
    n = n * k
print("orderings of 5 different words:", n)
```
```text
vocab       ['the', 'dog', 'bit', 'postman']
bag of a    [2, 1, 1, 1]
bag of b    [2, 1, 1, 1]
same bag?   True
same text?  False
orderings of 5 different words: 120
```

The computer sees the same row twice. However clever the classifier that comes next, it cannot tell these sentences apart, because the information is gone before the classifier starts. The last line is a side fact: five different words can be lined up in 120 ways, and all 120 give one bag.

> **✏️ Write in your Bug Log.** What would a reader have to do that a counter does not? Write one sentence. Then write one pair of sentences of your own, with the same words in a different order, where the two meanings really differ.

The answer we will build this week is:

> **A model that reads in order has to carry a summary, and it has to use the same rule for every word.**

![Two five-word sentences with the same words in a different order, both turned into the same bag row 2, 1, 1, 1](../figures/fig-w08-1-same-bag-different-order.svg)
*Figure 8.1 — Counting words throws the order away, so a classifier cannot tell these two sentences apart.*

### 2. The sticky note

You are reading a long book, and you may keep **one sticky note**. After every page you rewrite the note, using the page you just read and the old note. At the end, the note is all you remember.

```text
   note starts empty (all zeros)

   read "the"  -> rewrite the note
   read "dog"  -> rewrite the note    (uses the last note AND "dog")
   read "bit"  -> rewrite the note
   ...
   the LAST note is the summary of the whole sentence
```

That note has a name: the **hidden state**. The machine that rewrites it is a **recurrent cell**. In symbols:

```text
new note = tanh( W_xh * (this word) + W_hh * (old note) + b )
```

In words: multiply the word's numbers by a weight, multiply the old note by another weight, add a bias, squash with `tanh`. Every piece is a neuron from Level 3. The only new thing is that the answer goes **back in** at the next step.

Draw the loop **unrolled**, one box per step:

```text
          x1          x2          x3          x4
           |           |           |           |
           v           v           v           v
  h0 --> [CELL] -h1-> [CELL] -h2-> [CELL] -h3-> [CELL] --> h4
          ^            ^            ^            ^
          +---- SAME weights in all four boxes ---+
```

We draw four boxes so that we can see the steps. There is really **one** cell, used again and again. This is called **weight sharing**, and it is why one cell can read a sentence of any length.

### 3. Do it by hand first

Take the simplest case: one number per word. Set `W_xh = 1.0`, `W_hh = 0.5`, `b = 0`, and start with a note of `0`. The sentence is "a spike, then quiet": `x = [1, 0, 0, 0]`.

Step 1: `pre = 1.0 x 1 + 0.5 x 0 = 1.0000`, and the new note is `tanh(1.0000) = 0.7616`.

Now do step 2 yourself with a calculator (it has a `tanh` key, and so does a phone) **before** you read on. Use the note from step 1. Then steps 3 and 4. Write the four notes in a column.

Now let the computer check you. Type `hand.py` **in two halves**. First type only the top half, down to the `for` loop, and run it. Then add the `nn.RNN` lines.

**`hand.py`**

```python
# hand.py - Week 8: the four-step unroll from the page, by hand, then by nn.RNN.
import math
import torch
import torch.nn as nn

W_xh = 1.0
W_hh = 0.5
xs = [1.0, 0.0, 0.0, 0.0]

h = 0.0
by_hand = []
for x in xs:
    pre = W_xh * x + W_hh * h
    h = math.tanh(pre)
    by_hand.append(h)
    print(f"pre = {pre:.4f}   h = {h:.4f}")

# Now the same thing with PyTorch's layer: 1 number in, 1 number remembered.
rnn = nn.RNN(1, 1, batch_first=True)
print("parameters inside nn.RNN(1, 1):")
for p in rnn.parameters():
    print("  ", tuple(p.shape))

# Put OUR weights into it. nn.RNN has TWO bias numbers; our hand version has none, so both go to 0.
rnn.weight_ih_l0.data = torch.tensor([[W_xh]])
rnn.weight_hh_l0.data = torch.tensor([[W_hh]])
rnn.bias_ih_l0.data = torch.zeros(1)
rnn.bias_hh_l0.data = torch.zeros(1)

x = torch.tensor(xs).reshape(1, 4, 1)          # (batch 1, time 4, features 1)
out, h_n = rnn(x)
print("out shape:", tuple(out.shape), " h_n shape:", tuple(h_n.shape))
print("rnn says  :", [round(v, 4) for v in out[0, :, 0].tolist()])
print("by hand   :", [round(v, 4) for v in by_hand])
print("match     :", torch.allclose(out[0, :, 0], torch.tensor(by_hand), atol=1e-6))
print("last of out == h_n:", torch.allclose(out[0, -1], h_n[0, 0]))
```
```text
pre = 1.0000   h = 0.7616
pre = 0.3808   h = 0.3634
pre = 0.1817   h = 0.1797
pre = 0.0899   h = 0.0896
parameters inside nn.RNN(1, 1):
   (1, 1)
   (1, 1)
   (1,)
   (1,)
out shape: (1, 4, 1)  h_n shape: (1, 1, 1)
rnn says  : [0.7616, 0.3634, 0.1797, 0.0896]
by hand   : [0.7616, 0.3634, 0.1797, 0.0896]
match     : True
last of out == h_n: True
```

Things to notice:

- `nn.RNN(1, 1, batch_first=True)` means: a cell that takes **1** number per word and keeps a note of **1** number. (The construct is explained in section 5.)
- Inside it are **four** parameters, printed as `(1, 1) (1, 1) (1,) (1,)`. Two of them are our weights `W_xh` and `W_hh`. The other two are **biases**. `nn.RNN` has two bias numbers (only their sum matters; it is a quirk of the library). Our hand version has no bias, so both go to zero.
- `.data = ...` forces your own numbers into a layer, exactly as you did with `conv.weight.data` in Level 3.
- `torch.allclose` means "equal, allowing for the last few decimal places". We never use `==` on decimals.
- `out[0, :, 0]` reads: sentence 0, every word, feature 0.

The spike **fades**: about half of it is lost at each step. Is that forgetting? Yes. How fast a note fades is a question for Week 10, where you will measure it.

> **🔢 Order matters, in four numbers.** Do two steps by hand with the same weights. First `x = [1, 0]` (spike first), then `x = [0, 1]` (spike second). In both, the inputs add up to 1, so a bag would say "same". Compare the **final** notes. This is workbook page 8.3.

![A recurrent cell drawn four times with the same weights, passing notes 0.7616, 0.3634, 0.1797 and 0.0896 forward](../figures/fig-w08-2-unrolled-cell-four-steps.svg)
*Figure 8.2 — One cell with one set of weights is reused at every step, and the note it passes on fades.*

### 4. A note of many numbers: `nn.Embedding`

Words are not numbers, and a computer needs a short list of numbers for each word. First give every word a **token id**, a whole number used as a row label. Then use a **table** that has one row for each word. Give the table an id and it hands back that word's row.

A row number is a **label, not an amount**. `bit = 2` does not mean `bit` is bigger than `dog`.

Before you run `lookup.py`, answer on paper: there are 5 ids and each row has 3 numbers. What shape will `vecs` be?

**`lookup.py`**

```python
# lookup.py - Week 8: nn.Embedding is a table with one row per word. Nothing is "computed".
import torch
import torch.nn as nn

torch.manual_seed(0)

vocab = ["the", "dog", "bit", "postman"]
ids = {w: i for i, w in enumerate(vocab)}      # word -> row number
print("ids:", ids)

emb = nn.Embedding(4, 3)                       # 4 words, each row has 3 numbers
print("table shape:", tuple(emb.weight.shape))
print("table:")
print(emb.weight.data)

x = torch.tensor([ids["the"], ids["dog"], ids["bit"], ids["the"], ids["postman"]])
print("ids of 'the dog bit the postman':", x.tolist())

vecs = emb(x)
print("lookup shape:", tuple(vecs.shape))
print(vecs.data)

# The lookup IS just row-picking: row 0 twice, and it is the same row.
print("row 0 of table == first vector:", torch.allclose(emb.weight.data[0], vecs.data[0]))
print("'the' at position 0 == 'the' at position 3:", torch.allclose(vecs.data[0], vecs.data[3]))
print("learnable numbers in the table:", emb.weight.numel())
```
```text
ids: {'the': 0, 'dog': 1, 'bit': 2, 'postman': 3}
table shape: (4, 3)
table:
tensor([[ 1.5410, -0.2934, -2.1788],
        [ 0.5684, -1.0845, -1.3986],
        [ 0.4033,  0.8380, -0.7193],
        [-0.4033, -0.5966,  0.1820]])
ids of 'the dog bit the postman': [0, 1, 2, 0, 3]
lookup shape: (5, 3)
tensor([[ 1.5410, -0.2934, -2.1788],
        [ 0.5684, -1.0845, -1.3986],
        [ 0.4033,  0.8380, -0.7193],
        [ 1.5410, -0.2934, -2.1788],
        [-0.4033, -0.5966,  0.1820]])
row 0 of table == first vector: True
'the' at position 0 == 'the' at position 3: True
learnable numbers in the table: 12
```

Look at the first and fourth rows of the lookup. The word `the` is the first and fourth word of the sentence, and the numbers are identical. The table does no thinking; it picks rows. The twelve numbers in the table are **knobs** that training will adjust like any weight. For now they are random, so they mean nothing.

### 5. The three new constructs

Read these slowly. They are the whole syntax of the week.

**(a) `nn.Embedding(V, d)` is a grid with `V` rows and `d` columns.** You give it a tensor of row numbers and it returns those rows. The ids must be whole numbers, and each must be smaller than `V`.

```python
emb = nn.Embedding(4, 3)     # 4 words, each stored as 3 numbers
vecs = emb(torch.tensor([0, 1, 2, 0, 3]))
```

**(b) `nn.RNN(input_size, hidden_size, batch_first=True)` is the recurrent cell.** `nn.RNN(3, 4, batch_first=True)` means: 3 numbers in per word, a note of 4 numbers. Its parameters are named like this:

| Name in PyTorch | Shape for `nn.RNN(3, 4)` | What it is |
|---|:--:|---|
| `weight_ih_l0` | (4, 3) | `W_xh`: from the word to the note |
| `weight_hh_l0` | (4, 4) | `W_hh`: from the old note to the new note |
| `bias_ih_l0` | (4,) | a bias |
| `bias_hh_l0` | (4,) | a second bias |

(`l0` means layer zero. We use one layer this year.)

`batch_first=True` says the input is laid out as **(batch, time, features)**: how many sentences, how many words in each, how many numbers per word. PyTorch's own default is (time, batch, features). **Always write `batch_first=True`, and say the shape aloud.**

**(c) `out, h_n = rnn(x)` hands back two things.** `out` is the note after **every** word. `h_n` is the note after the **last** word.

```text
x    (B, T, F)      sentences, words, numbers per word
out  (B, T, H)      a note for every word of every sentence
h_n  (1, B, H)      the LAST note of every sentence  (the leading 1 means "one layer")
```

For "the summary of the whole sentence" you use `h_n[0]`, which drops the leading 1. Before you run `shapes.py`, say the three shapes aloud: `x` is `(2, 4, 3)`, so what are `out` and `h_n`?

**`shapes.py`**

```python
# shapes.py - Week 8: the three shapes to say out loud before you run anything.
import torch
import torch.nn as nn

torch.manual_seed(0)

rnn = nn.RNN(3, 5, batch_first=True)       # 3 numbers in per step, 5 numbers remembered
x = torch.tensor([float(i) for i in range(24)]).reshape(2, 4, 3) / 10 - 1                   # 2 sentences, 4 steps each, 3 features per step
print("x    (batch, time, features):", tuple(x.shape))

out, h_n = rnn(x)
print("out  (batch, time, hidden)  :", tuple(out.shape))
print("h_n  (1, batch, hidden)     :", tuple(h_n.shape))

print("out[:, -1] is the last step:", tuple(out[:, -1].shape))
print("h_n[0]  drops the leading 1 :", tuple(h_n[0].shape))
print("out[:, -1] == h_n[0]        :", torch.allclose(out[:, -1], h_n[0]))
print("first step out[:, 0] == h_n[0]?", torch.allclose(out[:, 0], h_n[0]))
```
```text
x    (batch, time, features): (2, 4, 3)
out  (batch, time, hidden)  : (2, 4, 5)
h_n  (1, batch, hidden)     : (1, 2, 5)
out[:, -1] is the last step: (2, 5)
h_n[0]  drops the leading 1 : (2, 5)
out[:, -1] == h_n[0]        : True
first step out[:, 0] == h_n[0]? False
```

The last line prints `False` on purpose. The note after the *first* word is not the note after the *last* one.

---

## 🎲 Your Turn

### The Sticky-Note Relay

Now you are the cell. Your teacher is the reader. You will need a calculator with `tanh`, index cards, and a strip of paper with the headings `word | x | pre | note`.

The cards hold the word numbers (chosen by us, a toy, not a model):

| Card | Number |
|---|:--:|
| the | 0.2 |
| dog | 1.0 |
| bit | -0.5 |
| postman | -1.0 |

The rule, written at the top of your strip:

```text
pre  = x + 0.5 * (old note)
note = tanh(pre)
the note starts at 0
```

The rules of the game:

1. The reader turns over one card at a time, in the sentence's order, and says the word.
2. You compute `pre`, then `note`, write both to **4 decimals**, and read the note aloud.
3. You may not look at any card except the one just turned over. That is the whole point: it is all the real cell can do.
4. After five cards, the final note is the summary.

Play **round 1**: *the dog bit the postman*. Then **round 2**: *the postman bit the dog*.

Add up the five word numbers for each sentence. What do you get? If someone had given you only the total, could you say which sentence it was? Now look at your two final notes. Are they the same?

Then run `sticky.py` and compare it to your strip. Any row that differs is a calculator slip: find it.

**`sticky.py`**

```python
# sticky.py - Week 8 activity: the Sticky-Note Relay with ONE number per word and ONE number on the note.
import math

table = {"the": 0.2, "dog": 1.0, "bit": -0.5, "postman": -1.0}
W_hh = 0.5                                         # how much of the old note is kept (before squashing)


def relay(sentence, show=False):
    note = 0.0
    for w in sentence.split():
        pre = table[w] + W_hh * note
        note = math.tanh(pre)
        if show:
            print(f"  read {w:8s} x = {table[w]:5.1f}   pre = {pre:7.4f}   note = {note:7.4f}")
    return note


for s in ["the dog bit the postman", "the postman bit the dog"]:
    print(s)
    final = relay(s, show=True)
    print("  final note:", round(final, 4))

bag_sum_a = sum(table[w] for w in "the dog bit the postman".split())
bag_sum_b = sum(table[w] for w in "the postman bit the dog".split())
print("sum of word numbers:", round(bag_sum_a, 4), round(bag_sum_b, 4))
```

The output is not printed here, on purpose: it is your answer to check, not a thing to copy.

### Same bag, different story: `order.py`

Now the real layers. Two sentences with the same bag go through an embedding and an RNN. Before you run it, predict two things: are the **bag views** (the average of the word vectors) equal or not? Are the **final states** equal or not?

**`order.py`**

```python
# order.py - Week 8: same bag, different story. Embedding -> RNN -> one summary vector per sentence.
import torch
import torch.nn as nn

torch.manual_seed(0)

vocab = ["the", "dog", "bit", "postman"]
ids = {w: i for i, w in enumerate(vocab)}

a = "the dog bit the postman"
b = "the postman bit the dog"


def to_ids(sentence):
    return [ids[w] for w in sentence.split()]


x_ids = torch.tensor([to_ids(a), to_ids(b)])        # (batch 2, time 5)
print("ids:")
print(x_ids)

emb = nn.Embedding(4, 3)
rnn = nn.RNN(3, 4, batch_first=True)

vecs = emb(x_ids)                                     # (2, 5, 3)
out, h_n = rnn(vecs)
final = h_n[0]                                        # (2, 4): one summary per sentence

# The "bag" view: average the word vectors. Order is thrown away, so the two sentences agree.
bag_view = vecs.mean(dim=1)
print("bag view of a:", [round(v, 4) for v in bag_view[0].tolist()])
print("bag view of b:", [round(v, 4) for v in bag_view[1].tolist()])
print("bag views equal:", torch.allclose(bag_view[0], bag_view[1], atol=1e-6))

# The recurrent view: the final hidden state remembers the order.
print("final state of a:", [round(v, 4) for v in final[0].tolist()])
print("final state of b:", [round(v, 4) for v in final[1].tolist()])
print("final states equal:", torch.allclose(final[0], final[1], atol=1e-6))
print("size of the difference:", round((final[0] - final[1]).norm().item(), 4))

# Control: the SAME sentence twice must give the SAME state (the net is not random at run time).
same = torch.tensor([to_ids(a), to_ids(a)])
_, h_same = rnn(emb(same))
print("same sentence twice, equal:", torch.allclose(h_same[0, 0], h_same[0, 1]))

# Look at the first two words of each: the states only part ways once the orders differ.
print("step-by-step distance between the two sentences:")
for t in range(5):
    gap = (out[0, t] - out[1, t]).norm().item()
    print(f"  after word {t + 1}: {gap:.4f}")
```
```text
ids:
tensor([[0, 1, 2, 0, 3],
        [0, 3, 2, 0, 1]])
bag view of a: [0.7301, -0.286, -1.2587]
bag view of b: [0.7301, -0.286, -1.2587]
bag views equal: True
final state of a: [0.5728, -0.0141, 0.3677, 0.1722]
final state of b: [-0.1963, -0.0411, 0.3475, 0.6072]
final states equal: False
size of the difference: 0.8842
same sentence twice, equal: True
step-by-step distance between the two sentences:
  after word 1: 0.0000
  after word 2: 0.9854
  after word 3: 0.6620
  after word 4: 0.2906
  after word 5: 0.8842
```

Read the step-by-step distances at the bottom. After word 1 the distance is `0.0000`. Why? What have the two sentences read so far? When do they part ways?

> **⚠️ What this shows, and what it does not.** The weights here are seeded random numbers. The two final states are *different*, but they **mean nothing yet**. We showed that a recurrent state **can depend on the order**. We did not show that it understands anything. Teaching the state to mean something is the job of Weeks 10-13.

**Your own pair.** Change the two sentences `a` and `b` in `order.py` to a pair of your own, with the same words in a different order. Use only the four words in `vocab`. Run it again. What do you get on the `final states equal` line? Then find a pair that gives `True`.

### What is inside `nn.RNN`? `loop.py`

Here is the same layer written as a plain loop. Notice that the **same** `W_ih`, `W_hh` and `b` are used at every one of the five steps.

**`loop.py`**

```python
# loop.py - Week 8: nn.RNN is just this loop. One set of weights, used at every step.
import torch
import torch.nn as nn

torch.manual_seed(0)

rnn = nn.RNN(3, 4, batch_first=True)
x = torch.tensor([float(i) for i in range(15)]).reshape(1, 5, 3) / 10 - 0.7       # 1 sentence, 5 steps, 3 features
out, h_n = rnn(x)

W_ih = rnn.weight_ih_l0.data          # (4, 3)
W_hh = rnn.weight_hh_l0.data          # (4, 4)
b = rnn.bias_ih_l0.data + rnn.bias_hh_l0.data

h = torch.zeros(4)
worst = 0.0
for t in range(5):
    h = torch.tanh(W_ih @ x[0, t] + W_hh @ h + b)      # the SAME W_ih, W_hh, b every time
    gap = (h - out[0, t]).abs().max().item()
    worst = max(worst, gap)
    print(f"step {t + 1}: my h = {[round(v, 3) for v in h.tolist()]}   nn.RNN says {[round(v, 3) for v in out[0, t].tolist()]}")

print("worst difference over all steps < 1e-6:", worst < 1e-6)

# The weights do not grow with the length of the sentence.
for T in [5, 50, 500]:
    xx = torch.tensor([float(i) for i in range(3 * T)]).reshape(1, T, 3) / (3 * T)
    o, _ = rnn(xx)
    print(f"T = {T:3d}  out shape {tuple(o.shape)}  parameters {sum(p.numel() for p in rnn.parameters())}")

# Count them: 4x3 + 4x4 + 4 + 4
print("by hand: 4*3 + 4*4 + 4 + 4 =", 4 * 3 + 4 * 4 + 4 + 4)
```
```text
step 1: my h = [-0.531, -0.051, -0.637, 0.011]   nn.RNN says [-0.531, -0.051, -0.637, 0.011]
step 2: my h = [-0.23, -0.085, -0.603, -0.271]   nn.RNN says [-0.23, -0.085, -0.603, -0.271]
step 3: my h = [-0.399, -0.114, -0.581, -0.191]   nn.RNN says [-0.399, -0.114, -0.581, -0.191]
step 4: my h = [-0.362, -0.3, -0.52, -0.238]   nn.RNN says [-0.362, -0.3, -0.52, -0.238]
step 5: my h = [-0.374, -0.459, -0.514, -0.237]   nn.RNN says [-0.374, -0.459, -0.514, -0.237]
worst difference over all steps < 1e-6: True
T =   5  out shape (1, 5, 4)  parameters 36
T =  50  out shape (1, 50, 4)  parameters 36
T = 500  out shape (1, 500, 4)  parameters 36
by hand: 4*3 + 4*4 + 4 + 4 = 36
```

`@` is the matrix-times-vector product from Level 3. The weights do not grow with the length of the sentence: 36 numbers whether it reads 5 words or 500. Count them: `4x3 + 4x4 + 4 + 4 = 36`. That is weight sharing, in numbers.

One more honest limit. Reading five words takes five steps, one after another: step 3 cannot start before step 2 has finished. Sharing the weights is a statement about **how many numbers there are**, not about speed.

---

## 🔬 Break It On Purpose

**DELIBERATE.** This file leaves out `batch_first=True`. Before you run it, write down what `h_n` *should* look like if it reads 2 sentences of 4 words, each word 3 numbers, with a note of 5 numbers. Then run it.

```python
# DELIBERATE: forgot batch_first=True.
import torch
import torch.nn as nn

torch.manual_seed(0)
rnn = nn.RNN(3, 5)                                           # <- no batch_first=True
x = torch.tensor([float(i) for i in range(24)]).reshape(2, 4, 3) / 10 - 1              # meant: 2 sentences, 4 words, 3 numbers
out, h_n = rnn(x)
print("out shape:", tuple(out.shape), "  h_n shape:", tuple(h_n.shape))
print("I asked for 2 summaries. I got", h_n.shape[1])
```
```text
out shape: (2, 4, 5)   h_n shape: (1, 4, 5)
I asked for 2 summaries. I got 4
```

Did Python complain? Compare your prediction with what was printed. Write in your Bug Log what PyTorch thought the first axis of `x` was, and what you should do before every run from now on.

---

## 🚀 Optional: Does Order Help a Real Task? `flyer.py`

Every sentence in this file has the dog exactly once, as either the biter or the bitten. A bag of words cannot know which, because the bag is the same. Order is the only clue. This file **really trains** two tiny models for 200 steps each, which takes a fraction of a second.

**`flyer.py`**

```python
# flyer.py - Week 8 (optional, for the fast student): is the dog the biter or the bitten?
# Every sentence has the dog exactly once, so a bag of words cannot know which. Order is the only clue.
import time
import torch
import torch.nn as nn

torch.set_num_threads(1)
torch.manual_seed(0)

nouns = ["dog", "cat", "baker", "postman", "girl", "boy", "teacher", "fisherman"]
verbs = ["bit", "saw", "chased", "helped", "found", "called"]
vocab = ["the"] + nouns + verbs
ids = {w: i for i, w in enumerate(vocab)}

sentences, labels = [], []
for other in nouns[1:]:
    for v in verbs:
        sentences.append(f"the dog {v} the {other}")
        labels.append(1.0)                      # 1 = the dog did it
        sentences.append(f"the {other} {v} the dog")
        labels.append(0.0)                      # 0 = it was done to the dog

X = torch.tensor([[ids[w] for w in s.split()] for s in sentences])      # (84, 5)
y = torch.tensor(labels)
print("sentences:", len(sentences), "  tensor shape:", tuple(X.shape), "  share with label 1:", y.mean().item())

g = torch.Generator()
g.manual_seed(0)
order = torch.randperm(len(sentences), generator=g)
train_i, val_i = order[:60], order[60:]
print("train", len(train_i), " val", len(val_i))

# Sentences 2k and 2k+1 are mirror images (same bag, opposite label). How many val sentences have their mirror in train?
train_set = set(train_i.tolist())
print("val sentences whose mirror is in train:", sum(1 for i in val_i.tolist() if (i + 1 if i % 2 == 0 else i - 1) in train_set))


def counts(batch):                               # the bag: how many of each word
    c = torch.zeros(len(batch), len(vocab))
    for r in range(len(batch)):
        for w in batch[r].tolist():
            c[r, w] = c[r, w] + 1
    return c


def accuracy(logits, target):
    return ((logits > 0).float() == target).float().mean().item()


loss_fn = nn.BCEWithLogitsLoss()

# ---- model 1: a bag of words -> one linear layer
bag_head = nn.Linear(len(vocab), 1)
opt = torch.optim.AdamW(bag_head.parameters(), lr=0.05)
t0 = time.perf_counter()
for epoch in range(200):
    opt.zero_grad()
    loss = loss_fn(bag_head(counts(X[train_i])).reshape(-1), y[train_i])
    loss.backward()
    opt.step()
bag_train = accuracy(bag_head(counts(X[train_i])).reshape(-1), y[train_i])
bag_val = accuracy(bag_head(counts(X[val_i])).reshape(-1), y[val_i])
print(f"bag of words : train {bag_train:.3f}  val {bag_val:.3f}   ({time.perf_counter() - t0:.1f} s)")

# ---- model 2: embedding -> RNN -> last state -> one linear layer
emb = nn.Embedding(len(vocab), 8)
rnn = nn.RNN(8, 16, batch_first=True)
head = nn.Linear(16, 1)
params = list(emb.parameters()) + list(rnn.parameters()) + list(head.parameters())
opt = torch.optim.AdamW(params, lr=0.01)


def predict(batch):
    out, h_n = rnn(emb(batch))
    return head(h_n[0]).reshape(-1)


t0 = time.perf_counter()
for epoch in range(200):
    opt.zero_grad()
    loss = loss_fn(predict(X[train_i]), y[train_i])
    loss.backward()
    opt.step()
rnn_train = accuracy(predict(X[train_i]), y[train_i])
rnn_val = accuracy(predict(X[val_i]), y[val_i])
print(f"embedding+RNN: train {rnn_train:.3f}  val {rnn_val:.3f}   ({time.perf_counter() - t0:.1f} s)")
```
```text
sentences: 84   tensor shape: (84, 5)   share with label 1: 0.5
train 60  val 24
val sentences whose mirror is in train: 18
bag of words : train 0.567  val 0.333   (0.2 s)
embedding+RNN: train 1.000  val 1.000   (0.0 s)
```

Read these numbers carefully, and do not over-read them.

- The bag model gets `0.333` on the held-out sentences, which is **below** a coin flip. The script prints why: the 84 sentences come in mirror-image pairs with the same bag but opposite labels, and for 18 of the 24 held-out sentences the mirror is in the training half. A bag must give both the same answer, so what it learned from the training half is wrong for the partner. A bag cannot beat chance here in principle.
- The RNN gets 24 out of 24 on 24 held-out sentences, with one seed. It shows that a model that reads in order *can* do this task. It is a toy: it is **not** a result about language.

---

## 🔑 Wrap Up

1. Three things we did. One: a bag of words cannot tell these sentences apart. Two: a recurrent cell reads them in order, with one set of weights, and keeps a note. Three: its note after the last word *can* depend on the order. What did we **not** do?
2. How many numbers does the cell have to learn if the sentence has five words? And fifty?
3. What does `h_n[0]` hold, and how is it related to `out`?
4. In the relay, your two final notes mostly reflect which word? What does that suggest about how well a plain cell remembers the start of a long sentence?

Then write this sentence in your Bug Log in your own handwriting:

> **"One small net, reused at every step, and I say the shapes before I run."**

**A look ahead.** Next week is the first paper: weeks one to eight, no computer, and one of the questions is to unroll a cell like today's. After that, you will train a recurrent net and see what goes wrong.

---

## 📤 Homework

Complete workbook pages 8.1 to 8.6. The by-hand unroll on page 8.3 is the one to do carefully: Week 9 will ask for it on paper. Every number you write must have come from your own calculator or your own run.

**Optional.** In `hand.py`, change `W_hh` and see how the fade changes, then write what you saw in the Bug Log. Check your prediction before running.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **bag of words** | a count of each word; the order is lost |
| **sequence** | a list in which position matters |
| **token id** | a whole number used as the row label of a word |
| **embedding** | a table with one row of numbers per word |
| **hidden state** | the small summary (the "note") a recurrent cell rewrites after every word |
| **recurrent cell** | one small net, used at every step; its output goes back in at the next step |
| **unrolling** | drawing the loop as one box per step |
| **weight sharing** | the same weights used at every step |
| **`batch_first`** | input laid out as (batch, time, features) |

---

[⬅ Week 7](week-07.md) · [Course Home](../README.md) · [Week 9 ➡](week-09.md) · [Workbook](../workbook/week-08.md)
