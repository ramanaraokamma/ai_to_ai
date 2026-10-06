# Workbook — Week 8: Order Matters, A Cell That Remembers

**Name:** ________________________________  **Date:** ______________

[⬅ Week 7](week-07.md) · [📖 Read the chapter first](../student-guide/week-08.md) · [Course Home](../README.md) · [Next ➡](week-09.md)

---

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed, with a seed, in the last 24 hours.** The digits in the worked examples and in the answers came from real CPU runs (PyTorch 2.2.1, `torch.manual_seed(0)` where anything is random). The by-hand numbers (`0.7616 ...`) are plain arithmetic and will match exactly; a random table may differ on another PyTorch build, but the `True`/`False` lines and the **shapes** will not.
>
> **Predict first, then run.** On pages 8.2, 8.4 and 8.7 you write your guess *before* you run anything. A wrong guess is useful. A guess written after the run is not a guess.
>
> **Nothing is trained this week** (except, if you choose, the optional extension in the chapter). The weights you meet are seeded random numbers, or numbers you type in. So a result here can say *"the state can depend on the order"*. It cannot say *"the network understands the sentence"*.
>
> Run everything from the folder that contains `l4lib/`. This week needs no `l4lib` code and installs nothing.
>
> Use a **calculator with a `tanh` key** (a phone will do) and carry **four decimals** all the way. Rounding in the middle is the usual reason a fourth decimal is off.

---

![Map of the 36 weeks with Week 8, Order Matters, highlighted in Term 1](../figures/fig-w08-0-where-this-fits.svg)
*Figure 8.0 — Week 8 introduces the recurrent cell, the first model in the course that reads in order.*

## ✅ Warm-Up (5 min)

Five quick questions about **last week** (the playbook).

**W1.** A friend says *"dropout 0.3 scored 0.043, so dropout helps."* Which two numbers do you need before you can say anything? ____________ and ____________

**W2.** The baseline is 0.039 +/- 0.008. A row has mean 0.043. Is the gap (0.004) bigger than twice the spread (0.016)? ____________

**W3.** `itertools.product` gave you a thing with no `len()`. What one word, wrapped around it, lets you count it? ____________

**W4.** Last week's rule for a cause: a cause is a ____________ until a ____________ has been run.

**W5.** Level 3 built a bag-of-words sentiment engine. Name one sentence pair it would get wrong because of word order. ________________________________________________________________

---

## 🧺 Page 8.1 — Bags (by hand; no code until the end)

A **bag of words** is a list of counts: for each word in a fixed vocabulary, *how many times does it appear?* It keeps **how many**. It throws away **where**.

**Worked example (done for you).** Vocabulary `[the, dog, bit, postman]`.

| Sentence | the | dog | bit | postman | bag |
|---|:--:|:--:|:--:|:--:|:--:|
| the dog bit the postman | 2 | 1 | 1 | 1 | `[2, 1, 1, 1]` |
| the postman bit the dog | 2 | 1 | 1 | 1 | `[2, 1, 1, 1]` |

Same bag, different sentence. The computer sees the same row twice.

**Now you.** Fill in each grid by counting. Write the bag as a list of four numbers.

**B1.** Vocabulary `[the, cat, chased, dog]`.

| Sentence | the | cat | chased | dog | bag |
|---|:--:|:--:|:--:|:--:|:--:|
| the cat chased the dog | ___ | ___ | ___ | ___ | `[___, ___, ___, ___]` |
| the dog chased the cat | ___ | ___ | ___ | ___ | `[___, ___, ___, ___]` |

Same bag? ____________ Same text? ____________

**B2.** Vocabulary `[the, dog, bit, postman]` again. This pair is **not** a re-ordering (one word changed).

| Sentence | the | dog | bit | postman | bag |
|---|:--:|:--:|:--:|:--:|:--:|
| the dog bit the postman | ___ | ___ | ___ | ___ | `[___, ___, ___, ___]` |
| the dog bit the dog | ___ | ___ | ___ | ___ | `[___, ___, ___, ___]` |

Same bag? ____________ What does that tell you about when a bag **can** tell two sentences apart?

________________________________________________________________

**B3.** Make up **your own pair**: five words each, the same words in a different order, and the two sentences must mean different things.

Sentence 1: ________________________________________________

Sentence 2: ________________________________________________

Write the vocabulary you need, then the two bags.

Vocabulary: ________________________________________________

Bag 1: ________________________________  Bag 2: ________________________________

**B4.** A line-up of **five different** words can be ordered in `5 x 4 x 3 x 2 x 1` ways. Work it out: ____________ . All of those orderings share one bag. (Then run `bag.py` from the chapter and compare. Did the last line match? ____________)

**B5.** One sentence, in your own words: *a bag of words cannot tell these apart because* ________________________________________________

________________________________________________________________

![Two five-word sentences with the same words in a different order, both turned into the same bag row 2, 1, 1, 1](../figures/fig-w08-1-same-bag-different-order.svg)
*Figure 8.1 — Counting words throws the order away, so a classifier cannot tell these two sentences apart.*

---

## 📇 Page 8.2 — The Embedding Is a Table

`nn.Embedding(V, d)` is a grid with **V rows** (one per word) and **d columns** (numbers per word). You give it a list of row numbers (**ids**); it gives back those rows. It does **no arithmetic**.

Shapes are read **before** you run. Say them out loud.

**E1.** `emb = nn.Embedding(4, 3)`. The table has shape ( ____ , ____ ) and holds ____________ learnable numbers.

**E2.** `ids = torch.tensor([0, 1, 2, 0, 3])`, so `emb(ids)` has shape ( ____ , ____ ). *Predict, then run `lookup.py` and tick:* ☐ I was right  ☐ I was wrong

**E3.** In that list, the id 0 appears twice. Will the first and fourth vectors be **equal**? ____________ Why? ________________________________

**E4.** Fill the blank. The ids `0, 1, 2, 0, 3` stand for *the, dog, bit, ____, ____* , so the sentence is "________________________".

**E5.** Is `bit = 2` a *bigger* word than `dog = 1`? ____________ What are ids? ________________________________

**E6.** `nn.Embedding(6, 2)`. (a) What is the biggest id it can take? ____________ (b) How many learnable numbers? ____________ (c) Shape of the lookup for ids of shape (4,)? ( ____ , ____ )

**E7.** Predict, for each line, **runs** or **error**. If error, name the kind in a word or two (you will meet these in page 8.7).

| Line, with `emb = nn.Embedding(4, 3)` | Runs or error? | If error, which? |
|---|:--:|---|
| `emb(torch.tensor([0, 1, 2]))` | ____________ | ____________ |
| `emb(torch.tensor([0.0, 1.0, 2.0]))` | ____________ | ____________ |
| `emb(torch.tensor([0, 1, 4]))` | ____________ | ____________ |

---

## 🧮 Page 8.3 — Unroll the Cell by Hand

The recurrent cell is one line:

```text
new note  =  tanh( W_xh * x  +  W_hh * (old note) )          (bias = 0 today)
```

In this page `W_xh = 1.0` and `W_hh = 0.5`. The note **starts at 0**. For each word you do two steps: the **pre** (the sum inside the brackets), then the **note** (`tanh` of the pre). The new note becomes the old note of the next step. Carry **four decimals**.

**Worked example (done for you): `x = [0, 1, 0, 0]`** (the spike comes second).

| Step | x | pre = 1.0 * x + 0.5 * (old note) | note = tanh(pre) |
|:--:|:--:|---|:--:|
| 1 | 0 | 1.0 x 0 + 0.5 x 0 = 0.0000 | 0.0000 |
| 2 | 1 | 1.0 x 1 + 0.5 x 0.0000 = 1.0000 | 0.7616 |
| 3 | 0 | 1.0 x 0 + 0.5 x 0.7616 = 0.3808 | 0.3634 |
| 4 | 0 | 1.0 x 0 + 0.5 x 0.3634 = 0.1817 | 0.1797 |

**Now you.** Fill each table. The first row of (a) is done to get you going.

**(a)  `x = [1, 0, 0, 0]`**

| Step | x | pre | note |
|:--:|:--:|:--:|:--:|
| 1 | 1 | 1.0 x 1 + 0.5 x 0 = 1.0000 | 0.7616 |
| 2 | 0 | ____________ | ____________ |
| 3 | 0 | ____________ | ____________ |
| 4 | 0 | ____________ | ____________ |

**(b)  `x = [0, 0, 1, 0]`**

| Step | x | pre | note |
|:--:|:--:|:--:|:--:|
| 1 | 0 | ____________ | ____________ |
| 2 | 0 | ____________ | ____________ |
| 3 | 1 | ____________ | ____________ |
| 4 | 0 | ____________ | ____________ |

**(c)  `x = [1, 1, 0, 0]`**

| Step | x | pre | note |
|:--:|:--:|:--:|:--:|
| 1 | 1 | ____________ | ____________ |
| 2 | 1 | ____________ | ____________ |
| 3 | 0 | ____________ | ____________ |
| 4 | 0 | ____________ | ____________ |

**(d) and (e): the order swap.** Only two steps each. The **sum** of the inputs is 1 both times.

| Part | x | note after step 1 | note after step 2 |
|:--:|:--:|:--:|:--:|
| d | `[1, 0]` | ____________ | ____________ |
| e | `[0, 1]` | ____________ | ____________ |

**d-e question.** A bag would add up the inputs. Both sums are ____. The two final notes are ____________ and ____________. Are they the same? ____________ In one sentence, what does that show? ________________________________________________________________

**(f)  `x = [1, 0, 0, 0]` with `W_hh = 0`** (the cell may not use the old note at all). The pre is now just `1.0 * x`.

| Step | 1 | 2 | 3 | 4 |
|:--:|:--:|:--:|:--:|:--:|
| note | ________ | ________ | ________ | ________ |

What has happened to the memory of the spike? ________________________________________________

**(g)  `x = [1, 0, 0, 0]` with `W_hh = 1.0`**

| Step | 1 | 2 | 3 | 4 |
|:--:|:--:|:--:|:--:|:--:|
| note | ________ | ________ | ________ | ________ |

Compare step 4 with part (a): ____________ against ____________ . Does the spike fade more slowly or more quickly with the bigger `W_hh`? ____________

**Careful.** You tried **one input** and **two** values of `W_hh`. In a sentence, what may you say, and what may you not?

________________________________________________________________

**Check with the code.** Run `hand.py` from the chapter. Tick: ☐ `match : True`. Then change the four lines of weights and the list `xs` to redo (c) and (g). ☐ My hand numbers agreed with the code to four decimals.

**A spike fades.** In (a), about how much of the note is left after each step, compared with the step before? ____________ (Divide step 2 by step 1 and step 3 by step 2.) Do **not** say why it fades yet; that is a later week. Just report what you see.

### The Sticky-Note Relay sheet (from class, and one more to try)

Word numbers: `the = 0.2`, `dog = 1.0`, `bit = -0.5`, `postman = -1.0`. Rule: **pre = x + 0.5 x (old note)**, **note = tanh(pre)**, the note starts at 0. The cell may look at **only the card just turned over** and its own note.

| Sentence 1: the dog bit the postman | x | pre | note |
|---|:--:|:--:|:--:|
| the | 0.2 | ________ | ________ |
| dog | 1.0 | ________ | ________ |
| bit | -0.5 | ________ | ________ |
| the | 0.2 | ________ | ________ |
| postman | -1.0 | ________ | ________ |

Final note: ____________

| Sentence 2: the postman bit the dog | x | pre | note |
|---|:--:|:--:|:--:|
| the | 0.2 | ________ | ________ |
| postman | -1.0 | ________ | ________ |
| bit | -0.5 | ________ | ________ |
| the | 0.2 | ________ | ________ |
| dog | 1.0 | ________ | ________ |

Final note: ____________

**R1.** Add the five word numbers for each sentence (`0.2 + 1.0 - 0.5 + 0.2 - 1.0`). Sentence 1: ________ Sentence 2: ________ . If I had only given you the total, could you say which sentence it was? ____________

**R2.** The final notes are mostly about **which word came last**. Which? ____________ Do they also tell you anything about the *first* word? ____________ (Both sentences start with `the`.)

**R3. Try one yourself.** Same rule, two **three-word** sentences: *dog bit postman* and *postman bit dog*. Final notes: ________________ and ________________ .

![A recurrent cell drawn four times with the same weights, passing notes 0.7616, 0.3634, 0.1797 and 0.0896 forward](../figures/fig-w08-2-unrolled-cell-four-steps.svg)
*Figure 8.2 — One cell with one set of weights is reused at every step, and the note it passes on fades.*

---

## 📐 Page 8.4 — Shapes (say them before you run)

Three shapes to learn:

```text
x    (B, T, F)   sentences, words, numbers per word
out  (B, T, H)   a note for EVERY word of every sentence
h_n  (1, B, H)   the LAST note of every sentence (the 1 = "one layer")
```

`B` is the batch (how many sentences), `T` the time (words per sentence), `F` the features per word, `H` the size of the note. `batch_first=True` is what tells PyTorch the first axis is `B`.

**S1.** `nn.Embedding(10, 4)` followed by `nn.RNN(4, 6, batch_first=True)`. The ids have shape (3, 6): 3 sentences of 6 words.

| Thing | Shape (write it) |
|---|---|
| ids | ( 3 , 6 ) |
| after the embedding | ( ____ , ____ , ____ ) |
| `out` | ( ____ , ____ , ____ ) |
| `h_n` | ( ____ , ____ , ____ ) |
| `out[:, -1]` | ( ____ , ____ ) |
| `h_n[0]` | ( ____ , ____ ) |

Is `out[:, -1]` equal to `h_n[0]`? ____________ In words: both are ________________________________

**S2.** Three sentences, a note of 7 numbers. The shape of `h_n` is ( ____ , ____ , ____ ).

**S3.** `nn.RNN(3, 5, batch_first=True)` on `x` of shape (2, 4, 3). `out`: ( ____ , ____ , ____ ). `h_n`: ( ____ , ____ , ____ ).

**S4. The silent one.** The same line **without** `batch_first=True`: `nn.RNN(3, 5)`, same `x` of shape (2, 4, 3), meaning *2 sentences of 4 words*. PyTorch now reads the first axis as **time**. Predict the shape of `h_n`: ( ____ , ____ , ____ ). How many summaries do you get? ____________ (You asked for ____.) Does PyTorch complain? ____________

**S5.** Why is `out[-1]` **not** the last word of each sentence? What does `out[-1]` pick instead, and what would you write to get the last word of every sentence?

________________________________________________________________

**S6.** The embedding's second number and the RNN's first number must be the **same**. Why? If they are not, what does the last line of the error say? ________________________________________________

Now run `shapes.py` from the chapter, then type the S1-S6 cases into a file of your own and run it. Tick: ☐ all my shapes were right  ☐ I fixed ____ of them

---

## 🔢 Page 8.5 — Count the Knobs

A **knob** is one learnable number. Count them by hand, then check with the code.

| Layer | Working (write it) | Count |
|---|---|:--:|
| `nn.Embedding(10, 4)` | 10 x 4 | ________ |
| `nn.RNN(4, 6)` | 6x4 + 6x6 + 6 + 6 | ________ |
| both together | ________ + ________ | ________ |

Hint for the RNN: `weight_ih_l0` is (H, F), `weight_hh_l0` is (H, H), and there are **two** bias vectors, each of length H.

**K1.** `nn.RNN(3, 4)`. (a) Working: ____ x ____ + ____ x ____ + ____ + ____ = ________ (b) Does the count change for a 5-word sentence? For a 500-word sentence? ____________

**K2.** `nn.RNN(2, 3)`: ________ knobs. `nn.Embedding(6, 2)`: ________ knobs.

**K3.** List the four parameter **shapes** inside `nn.RNN(1, 1)`: ________ , ________ , ________ , ________ . Which two are the ones we set to `1.0` and `0.5`? ________________________________ What do we do with the other two? ________________

**K4. The big idea in a sentence.** Why does the number of knobs stay the same for a longer sentence? Use the words **the same weights**.

________________________________________________________________

Check: run `loop.py` from the chapter, and count the same layers in a file of your own. ☐ my counts matched

---

## 🏗️ Page 8.6 — The Build: `my_order.py`

Write a file that shows **two sentences with the same words in a different order** ending in **different** summaries. You may start from `order.py`, but the sentences and the vocabulary must be yours.

**Plan (fill in before you type).**

Vocabulary (one id per different word): ________________________________________________

Sentence 1: ____________________________________  Sentence 2: ____________________________________

Same length? ____________ (They must be, or the tensor will not be a rectangle. That is page 8.7, mistake 8.)

The embedding is `nn.Embedding( ____ , 3)`. The RNN is `nn.RNN( ____ , 4, batch_first=True)`. Shape of the ids: ( ____ , ____ ). Expected `h_n`: ( ____ , ____ , ____ ).

**Your file must print, with `torch.manual_seed(0)` at the top:**

1. the two **bag views** (the mean of the word vectors) and whether they are equal,
2. the two **final states** and whether they are equal,
3. the **size of the difference**, `(final[0] - final[1]).norm().item()`,
4. the **control**: the *same* sentence twice must give the *same* state.

**Paste your real output here** (copy and paste what your run printed; do not retype from memory).

```text
(paste here)








```

**Fill in from your run.**

| | My value |
|---|---|
| bag views equal? | ____________ |
| final states equal? | ____________ |
| size of the difference | ____________ |
| control (same sentence twice) equal? | ____________ |
| distance after word 1 | ____________ |

**The sentence that gets the marks.** Finish it in your own words, and name one thing your run did **not** show:

*My run showed that the final state* ________________________________________________

________________________________________________________________

*It did not show* ________________________________________________

________________________________________________________________

**Check yourself.**
- ☐ five or more words in each sentence, same words, different order
- ☐ the bag views printed, and equal
- ☐ the final states printed, and different, with a distance
- ☐ the control printed, and equal
- ☐ my sentence says the state **can depend on order** and that the weights are untrained, so it **means nothing yet**

**Did your first word match?** If both of your sentences start with the same word, the distance after word 1 is exactly 0. Does that mean "no difference"? Look at the **last** step before you answer: ________________________________

---

## 🐞 Page 8.7 — Break It on Purpose

Every program below is **deliberately broken**. Do not fix it until you have done the "Predict" line. Then copy, run, read the **last line** of the error, and fix.

**Program 1 (deliberate).**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
rnn = nn.RNN(3, 5, batch_first=True)
x = torch.tensor([float(i) for i in range(24)]).reshape(2, 4, 3) / 10 - 1

out = rnn(x)
print(out.shape)
```

Predict: runs or error? ____________ What I ran saw as the last line: ________________________________

What `rnn(x)` returns (how many things?): ____________ Fix: ________________________________

**Program 2 (deliberate).**

```python
import torch
import torch.nn as nn

emb = nn.Embedding(4, 3)
ids = torch.tensor([0.0, 1.0, 2.0])
print(emb(ids))
```

Predict: ________________  Last line: ________________________________  Fix: ________________

**Program 3 (deliberate).**

```python
import torch
import torch.nn as nn

emb = nn.Embedding(4, 3)
ids = torch.tensor([0, 1, 2, 3, 4])
print(emb(ids))
```

Predict: ________________  Last line: ________________________________  What is the largest id a 4-row table can take? ________

**Program 4 (deliberate).** The embedding gives 3 numbers per word, the RNN is told to expect 4.

```python
import torch
import torch.nn as nn

emb = nn.Embedding(4, 3)
rnn = nn.RNN(4, 5, batch_first=True)
ids = torch.tensor([[0, 1, 2]])
out, h_n = rnn(emb(ids))
```

Predict: ________________  Last line: ________________________________  Fix: ________________

**Program 5 (deliberate, SILENT): nothing will complain.** You wrote `h_n` on page 8.4 S4. Now run it.

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
rnn = nn.RNN(3, 5)                                           # <- no batch_first=True
x = torch.tensor([float(i) for i in range(24)]).reshape(2, 4, 3) / 10 - 1
out, h_n = rnn(x)
print("out shape:", tuple(out.shape), "  h_n shape:", tuple(h_n.shape))
print("I asked for 2 summaries. I got", h_n.shape[1])
```

What it printed: ________________________________________________ Did it match your prediction in S4? ____________

**Program 6 (deliberate, SILENT): a forgotten bias.**

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
rnn = nn.RNN(1, 1, batch_first=True)
rnn.weight_ih_l0.data = torch.tensor([[1.0]])
rnn.weight_hh_l0.data = torch.tensor([[0.5]])
rnn.bias_ih_l0.data = torch.zeros(1)
# rnn.bias_hh_l0.data = torch.zeros(1)      <- forgotten

x = torch.tensor([1.0, 0.0, 0.0, 0.0]).reshape(1, 4, 1)
out, h_n = rnn(x)
print("rnn says  :", [round(v, 4) for v in out[0, :, 0].tolist()])
print("by hand   : [0.7616, 0.3634, 0.1797, 0.0896]")
print("leftover bias_hh_l0 is", round(rnn.bias_hh_l0.item(), 4))
```

Predict: do the two lists agree? ____________ What it printed for "rnn says": ________________________________

Which line do you add to fix it? ________________________________ What one habit would have caught this without reading the code? ________________________________

**Program 7 (deliberate).** Wrong axis for "last".

```python
import torch
import torch.nn as nn

torch.manual_seed(0)
rnn = nn.RNN(3, 5, batch_first=True)
x = torch.tensor([float(i) for i in range(24)]).reshape(2, 4, 3) / 10 - 1
out, h_n = rnn(x)

print(tuple(out[-1].shape), tuple(h_n.shape))
print(torch.allclose(out[-1], h_n))
```

The first line prints: ________________ . Last line of the error: ________________________________

Fix (two changes): ________________________________

**Program 8 (deliberate).** Two sentences of different lengths.

```python
a = "the dog bit the postman".split()
b = "dog bit postman".split()
ids = {"the": 0, "dog": 1, "bit": 2, "postman": 3}
import torch
x = torch.tensor([[ids[w] for w in a], [ids[w] for w in b]])
```

Predict: ________________ . Why can a tensor not hold these two? ________________________________ (The real fix is Week 12. Today: use sentences of the same length.)

---

## 📓 Page 8.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Keep this page; the Week 9 assessment has a reading-errors question.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more; this week there were two): write the one I made, or nearly made. ________________________________________

**The habit for silent mistakes.** Fill in the blank: *before I run an RNN, I say the expected shape of* ________ *out loud; after I type weights by hand, I check them against* ________________ .

Write this sentence in your own handwriting:

> **"Say the shape first, and never say the RNN understands."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **Why can a bag of words not tell "the dog bit the postman" from "the postman bit the dog"?**

________________________________________________________________

2. **What does `nn.Embedding` do, in one sentence? Does it compute anything?**

________________________________________________________________

3. **Why is a recurrent cell "one net reused"? Where does that show in the knob count?**

________________________________________________________________

4. **What are the shapes of `x`, `out` and `h_n`, and which one is the summary of the whole sentence?**

________________________________________________________________

5. **Your friend's random RNN gave two different final states for two re-ordered sentences, and says "it understands word order". What do you say?** Use "can depend on" in your answer.

________________________________________________________________

6. *Parking Lot.* In the unroll in (a) the note shrinks each step. Do **not** answer "why" with certainty. Write your best guess, and one experiment you could run (a different `W_hh`, say) to test it.

________________________________________________________________

**Mark yourself.** Tick the first line you can honestly say.

- [ ] **Not yet:** I cannot say what the note is, or why order matters.
- [ ] **Developing:** I get the hand numbers with help, but I mix up `out` and `h_n`.
- [ ] **Secure:** I get the four hand numbers, see `match : True`, state the three shapes, and show two same-bag sentences ending in different states.
- [ ] **Fluent:** I unrolled with a different `W_hh` without being asked, predicted the shapes before running, and wrote "can depend on order" rather than "understands".

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-08.md) · [Next ➡](week-09.md)

---
---

# ✂️ ANSWERS - keep this page folded until you have finished

*Numbers come from real runs: CPU, PyTorch 2.2.1, `torch.manual_seed(0)` wherever anything is random. The by-hand numbers are plain arithmetic and should match to four decimals (within 0.0001 of rounding). Random tables may differ on another build; the `True`/`False` lines and the shapes should not.*

### Warm-Up

- **W1.** The baseline's number **and** its spread (and the row's spread). Then ask whether the gap is bigger than twice the spread.
- **W2.** No. 0.004 is less than 0.016: inside noise.
- **W3.** `list` (as in `list(itertools.product(...))`).
- **W4.** A cause is a **guess** until a **check** has been run.
- **W5.** Any pair of re-orderings, e.g. "the dog bit the postman" / "the postman bit the dog", or a negation that depends on position. The bag is the same, the meaning is not.

### Page 8.1

- **B1.** Both bags are `[2, 1, 1, 1]` (the = 2, cat = 1, chased = 1, dog = 1). Same bag: **True**. Same text: **False**.
- **B2.** `[2, 1, 1, 1]` against `[2, 2, 1, 0]`. Not the same bag. A bag **can** tell two sentences apart when they have different words or different counts; it cannot when they are just a re-ordering.
- **B3.** Any pair that is a re-ordering has equal bags. Check the student's counts add up to the sentence length (5 each) and that the two bags are identical.
- **B4.** `5 x 4 x 3 x 2 x 1` = **120**. `bag.py` prints `orderings of 5 different words: 120`.
- **B5.** It keeps the counts of each word and throws the order away.
- *Common error:* writing the number of words in the sentence instead of the list of counts.

### Page 8.2

- **E1.** (4, 3); **12**.
- **E2.** (5, 3).
- **E3.** Yes. Same id, so the same row of the table (`lookup.py` prints `True`).
- **E4.** *the, dog, bit, **the**, **postman***: "the dog bit the postman".
- **E5.** No. Ids are **labels on rows**, not sizes.
- **E6.** (a) **5** (rows numbered 0 to 5 for 6 rows). (b) 6 x 2 = **12**. (c) (4, 2).
- **E7.** Runs (shape (3, 3)); error: float ids (`Expected tensor for argument #1 'indices' to have one of the following scalar types: Long, Int`); error: id 4 with a 4-row table (`IndexError: index out of range in self`).

### Page 8.3

With `W_xh = 1.0`, `W_hh = 0.5`, bias 0, note starts at 0.

| Part | x | pre, step by step | notes, step by step |
|:--:|---|---|---|
| a | `[1, 0, 0, 0]` | 1.0000, 0.3808, 0.1817, 0.0899 | 0.7616, 0.3634, 0.1797, 0.0896 |
| b | `[0, 0, 1, 0]` | 0, 0, 1.0000, 0.3808 | 0.0, 0.0, 0.7616, 0.3634 |
| c | `[1, 1, 0, 0]` | 1.0000, 1.3808, 0.4406, 0.2071 | 0.7616, 0.8811, 0.4141, 0.2041 |
| d | `[1, 0]` | 1.0000, 0.3808 | 0.7616, 0.3634 |
| e | `[0, 1]` | 0, 1.0000 | 0.0, 0.7616 |
| f | `[1, 0, 0, 0]`, `W_hh = 0` | | 0.7616, 0.0, 0.0, 0.0 |
| g | `[1, 0, 0, 0]`, `W_hh = 1.0` | | 0.7616, 0.642, 0.5663, 0.5126 |

- **d-e question.** Both sums are **1**. The final notes are **0.3634** and **0.7616**. Not the same: *the sum (what a bag sees) is identical, the note is not; the note depends on the order.*
- **(f).** The spike is gone after one step: with `W_hh = 0` the cell does not use the old note, so it has no memory.
- **(g).** 0.5126 against 0.0896: the note fades **more slowly** with the bigger `W_hh`. May say: for this one input and these two values, the spike lasted longer. May not: that a bigger `W_hh` is better, or anything about other inputs.
- **"How much is left".** About half: 0.3634 / 0.7616 = 0.48, 0.1797 / 0.3634 = 0.49, 0.0896 / 0.1797 = 0.50 (roughly). Report only; no "why" this week.
- *Common errors:* `tanh` applied twice; forgetting the old note at step 2; rounding to 2 decimals mid-way.

**Relay (from `sticky.py`).**

| Sentence 1 | pre | note |
|---|:--:|:--:|
| the | 0.2000 | 0.1974 |
| dog | 1.0987 | 0.8000 |
| bit | -0.1000 | -0.0997 |
| the | 0.1502 | 0.1491 |
| postman | -0.9255 | -0.7285 |

| Sentence 2 | pre | note |
|---|:--:|:--:|
| the | 0.2000 | 0.1974 |
| postman | -0.9013 | -0.7169 |
| bit | -0.8585 | -0.6955 |
| the | -0.1477 | -0.1467 |
| dog | 0.9267 | 0.7290 |

Final notes **-0.7285** and **0.7290** (within 0.001 is a match).

- **R1.** Both totals are **-0.1**. No, you could not say.
- **R2.** The last word (`postman` = -1.0 against `dog` = +1.0). A little or nothing about the first: `the` is the same in both, so we cannot tell here. Week 10 measures how long a note survives.
- **R3.** *dog bit postman*: notes 0.7616, -0.1186, -0.7854, final **-0.7854**. *postman bit dog*: notes -0.7616, -0.7068, 0.5694, final **0.5694**. (Pre values for the first: 1.0000, -0.1192, -1.0593; for the second: -1.0000, -0.8808, 0.6466.)

### Page 8.4

- **S1.** ids (3, 6); after the embedding **(3, 6, 4)**; `out` **(3, 6, 6)**; `h_n` **(1, 3, 6)**; `out[:, -1]` **(3, 6)**; `h_n[0]` **(3, 6)**. Equal: **yes**; both are the note after the last word of each sentence. *Common errors:* `h_n` as (3, 6) (that is `h_n[0]`), or `out` as (3, 4, 6) (confusing feature size 4 with time 6).
- **S2.** **(1, 3, 7)**. (If (3, 7): half marks, that is `h_n[0]`.)
- **S3.** `out` **(2, 4, 5)**, `h_n` **(1, 2, 5)**.
- **S4.** `h_n` **(1, 4, 5)**: 4 summaries, not 2. No error, nothing complains. Each summary is a 2-step read.
- **S5.** `out[-1]` is the last **sentence** (first axis) with shape (4, 5): 4 words by 5 numbers. The last word of each sentence is `out[:, -1]`, shape (2, 5), and you compare it with `h_n[0]`, not `h_n`.
- **S6.** The RNN takes in what the embedding hands over, one vector per word. The error's last line says `Expected 4, got 3` (`input.size(-1) must be equal to input_size`).

### Page 8.5

- `nn.Embedding(10, 4)`: 10 x 4 = **40**. `nn.RNN(4, 6)`: 6x4 + 6x6 + 6 + 6 = 24 + 36 + 12 = **72**. Both: **112**.
- **K1.** 4 x 3 + 4 x 4 + 4 + 4 = 12 + 16 + 8 = **36**. The count does **not** change for 5 or 500 words (`loop.py` prints 36 at T = 5, 50, 500).
- **K2.** `nn.RNN(2, 3)`: 3x2 + 3x3 + 3 + 3 = 6 + 9 + 6 = **21**. `nn.Embedding(6, 2)`: **12**. (Both checked by running `sum(p.numel() for p in rnn.parameters())`.)
- **K3.** (1, 1), (1, 1), (1,), (1,). The two `(1, 1)` are `W_xh` and `W_hh`. Set both biases to zero (our hand version has none). *Common error:* counting one bias, not two.
- **K4.** The same weights are applied at every step, so the number of weights does not depend on how many steps.

### Page 8.6

Any pair of same-length sentences with the same words re-ordered, five or more words each. Required in the output, with a stated seed: bag views equal (`True`), final states different (`False`), a distance, control equal (`True`). Our seed-0 run of `order.py`: final states `[0.5728, -0.0141, 0.3677, 0.1722]` against `[-0.1963, -0.0411, 0.3475, 0.6072]`, distance **0.8842**, distance after word 1 **0.0000**, then 0.9854, 0.6620, 0.2906, 0.8842. Your numbers will differ if your sentences differ.

| Criterion | Marks |
|---|:--:|
| Two sentences, same words, different order, five or more words each | 1 |
| Bag view equal, printed | 1 |
| Final states different, printed, with a distance | 1 |
| The control (same sentence twice, equal) | 1 |
| A sentence that says **"the state can depend on order; the weights are untrained, so it means nothing yet"** (or equivalent) | 2 |

Not shown: that a trained network would carry the right information, anything about meaning, anything beyond one seed and one pair. A write-up that says "the RNN understands the sentences" loses the last two marks. **First-word question:** a distance of 0 after word 1 only means the first word was the same; the last step shows the difference.

### Page 8.7

- **Program 1.** Error. `AttributeError: 'tuple' object has no attribute 'shape'`. `rnn(x)` returns **two** things. Fix: `out, h_n = rnn(x)`.
- **Program 2.** Error. The last line says the ids must be `Long` or `Int` and got `FloatTensor` (`RuntimeError: Expected tensor for argument #1 'indices' to have one of the following scalar types: Long, Int; but got torch.FloatTensor instead ...`). Fix: whole numbers, `[0, 1, 2]`, or `.long()`.
- **Program 3.** Error. `IndexError: index out of range in self`. A 4-row table takes ids up to **3**.
- **Program 4.** Error. `RuntimeError: input.size(-1) must be equal to input_size. Expected 4, got 3`. Fix: make the embedding's `d` and the RNN's first number equal (both 3, or both 4).
- **Program 5.** Prints `out shape: (2, 4, 5)   h_n shape: (1, 4, 5)` and `I asked for 2 summaries. I got 4`. Silent. Habit: say the expected `h_n` shape, (1, 2, 5), before running.
- **Program 6.** Prints `rnn says  : [0.2581, -0.5419, -0.7645, -0.8069]`, `by hand   : [0.7616, 0.3634, 0.1797, 0.0896]`, `leftover bias_hh_l0 is -0.7359`. The lists do **not** agree. Fix: add `rnn.bias_hh_l0.data = torch.zeros(1)`. Habit: after typing weights, check against the hand calculation with `torch.allclose`.
- **Program 7.** First line prints `(4, 5) (1, 2, 5)`. Last line: `RuntimeError: The size of tensor a (4) must match the size of tensor b (2) at non-singleton dimension 1`. Fix: `out[:, -1]` and compare with `h_n[0]`.
- **Program 8.** Error. `ValueError: expected sequence of length 5 at dim 1 (got 3)`. A tensor is a rectangle. Real fix (padding) is Week 12.

The "What it printed" lines may differ a little in path names and in the number of elided frames; the **last line** is the one that matters.

### Bug Log and Self-Check

Bug Log: any real entries are fine if the **last line** (not the whole traceback) was copied and the fix works. The two no-traceback mistakes of the week are `batch_first` forgotten (Program 5) and the forgotten second bias (Program 6). Habit: say the expected shape of **`h_n`** out loud; check typed weights against **the hand calculation**.

1. It keeps the counts of each word and throws the order away; the two sentences give the same row of counts.
2. It looks up a row of a table by the word's number. It does no arithmetic; the same id always gives the same row.
3. The same weights (`W_ih`, `W_hh`, the biases) are used at every step. The knob count (36 for `nn.RNN(3, 4)`) has no "number of words" in it.
4. `x` is (B, T, F), `out` is (B, T, H), `h_n` is (1, B, H). The summary of the whole sentence is `h_n` (that is, `h_n[0]`, equal to `out[:, -1]`).
5. "In this untrained network the final state **can depend on** the order, so two re-orderings give different states. But the weights are random, so the difference means nothing yet. Making it mean something is the job of training, weeks 10 to 13."
6. Reading, not proof: the note is rewritten each step, and in (a) about half is lost each step. Experiment: rerun (a) with `W_hh = 1.0` (0.5126 after four steps against 0.0896), as in (g). Do not generalise beyond that one input.

---

[⬅ Course Home](../README.md) · [📖 Chapter](../student-guide/week-08.md) · [Next ➡](week-09.md)
