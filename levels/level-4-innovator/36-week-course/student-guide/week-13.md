# Week 13 — Choosing the Next Letter: Sampling and Exposure Bias

[⬅ Week 12](week-12.md) · [Course Home](../README.md) · [Week 14 ➡](week-14.md) · [Workbook](../workbook/week-13.md)

---

> ### This week in one sentence
> **A language model never says a letter; it gives a score for every letter, and a rule that *you* write turns the scores into one choice. Change the rule and you change what comes out, without touching the model.**
>
> **By the end of this chapter you will be able to:**
> - **Say what the model outputs** (one score per letter) and turn scores into chances with `F.softmax(scores, dim=-1)`
> - **Predict, then measure,** what a temperature of 0.3, 1 and 2 does to the chances of five letters
> - **Draw a letter** with `torch.multinomial` and check with 10,000 draws that the shares match the chances
> - **Write top-k and top-p** with `torch.topk`, `torch.sort` and `torch.cumsum`, and say what each one cuts off
> - **Count, not eyeball,** how many names a sampler repeats and how many are new, and say why "new" is **not** "good"
> - **Explain exposure bias in two sentences** and quote today's one measurement with its limits
>
> **New maths:** **none.** Softmax is from Level 3. Temperature is one extra step in front of it: divide every score by a number first.
>
> **New syntax:** `F.softmax(x, dim=-1)` · `torch.multinomial` · `torch.topk` · `torch.sort` + `torch.cumsum` (top-p, counted as one)
>
> **New words:** greedy · temperature · top-k · top-p · sampling · novelty rate · exposure bias
>
> **Reading time:** about 35 minutes. **In class:** about 70 minutes. **Homework (the workbook):** about 60-75 minutes, of which about 30 seconds is the computer working.

> **📌 About the code blocks.** Each block is a whole file, with its name in the first line. Keep them in **one folder, next to `l4lib/`**, and run them from that folder. **`namelm.py` is your Week 12 name model kept as a module; your teacher gives it to you and you do not type it.** The rest you type. Every output shown was printed by a real run on a CPU with seeds set. Different PyTorch build: the last digit of a chance can move, and a count of new names can move by a name or two. Lines that report **seconds** depend on your machine. Blocks marked **DELIBERATE** are written on purpose to fail. Nothing this week needs the internet. **The model is real and small: it was trained on the 231 typed names, nothing else.** There is no scripted stand-in. The five scores in `five.py` are **invented by us** to make the arithmetic readable; they are not from any model.

---

## 🪝 Start Here

Last week your model made names such as `dira` and `arjav`. At every letter it had a choice. **How did it choose?**

Write your guess on workbook page 13.1 before you read on. Most people write "the most likely letter". So let us find out what happens if a model *always* does that.

A few words to keep in mind:

- The model's answer at each step is a list of **scores**, one per letter (and one for "stop").
- **Sampling** means choosing the next letter from those scores by some rule.
- **Greedy** means the rule "always take the highest score".

---

## 🧠 The Big Idea

### 1. The model gives scores. Something else has to choose.

```text
   letters so far:  a  n  d
                    |  |  |
                [ the model ]          28 scores, one per letter (and one for "stop")
                    |
      a: 0.4   b: -1.2   ...   r: 2.1   e: 1.9   ...  stop: -0.3
```

A bigger score means a likelier letter. To pick we need chances that add up to 1. You did this in Level 3: raise `e` to each score, divide by the total. That is **softmax**. In PyTorch:

```python
probs = F.softmax(scores, dim=-1)
```

The `dim=-1` means "along the **last** axis". A list of scores has one axis, so that is the whole list. A batch of 64 rows has the scores along the last axis, so the same line works for a batch too. **Always write `dim`.** Leave it out and PyTorch guesses (and prints a warning saying so). A *wrong* `dim` gives no warning at all.

### 2. Do the arithmetic once, by hand

Five letters `a b c d e` with the invented scores `0.0, 2.0, -1.0, 1.0, 0.5`. Use a calculator and fill in page 13.2:

| Letter | score | `exp(score)` | ÷ total |
|:--:|:--:|:--:|:--:|
| a | 0.0 | 1.000 | ? |
| b | 2.0 | 7.389 | ? |
| c | -1.0 | 0.368 | ? |
| d | 1.0 | 2.718 | ? |
| e | 0.5 | 1.649 | ? |

The total is `1.000 + 7.389 + 0.368 + 2.718 + 1.649 = 13.124`. Divide each row by it. The five chances must add up to 1.

### 3. The dial: temperature

**Temperature** `T` is one more step in front: **divide every score by `T` first**, then softmax. That is the whole idea. With `T = 1` you divide by one and nothing changes, so `T = 1` is "the model's own belief".

**Before you run anything,** write on page 13.2: for the best letter, does its chance go **up or down** as `T` goes 0.3, then 1, then 2? Commit to it. Then type `five.py` **in pieces**: the top down to the `for T` loop first, run it, then add a piece at a time.

```python
# five.py - Week 13: one set of scores for five letters, turned into probabilities five ways.
import torch
import torch.nn.functional as F

letters = "abcde"
scores = torch.tensor([0.0, 2.0, -1.0, 1.0, 0.5])      # the model's raw scores ("logits")

def show(name, p):
    print(f"{name:<12}", " ".join(f"{letters[i]}={float(p[i]):.3f}" for i in range(len(letters))), f"  sum={float(p.sum()):.3f}")

# 1. softmax: scores -> probabilities that add to 1. dim=-1 means "along the last axis".
show("T=1", F.softmax(scores, dim=-1))

# 2. temperature: divide the scores by T first.
for T in [0.3, 1.0, 2.0]:
    show(f"T={T}", F.softmax(scores / T, dim=-1))

# 3. multinomial: draw ONE index at random, in proportion to the probabilities.
torch.manual_seed(0)
p = F.softmax(scores, dim=-1)
print("ten draws :", [letters[i] for i in torch.multinomial(p, 10, replacement=True)])
draws = torch.multinomial(p, 10000, replacement=True)
print("10000 draws, share of each letter:", [round(float((draws == i).float().mean()), 3) for i in range(5)])

# 4. topk: the k biggest scores, and the places they came from.
vals, ids = torch.topk(scores, 3)
print("top 3 scores:", vals.tolist(), "at places", ids.tolist())
kept3 = F.softmax(vals, dim=-1)                          # softmax over the survivors only
print("top-3 kept  ", " ".join(f"{letters[int(ids[j])]}={float(kept3[j]):.3f}" for j in range(3)))

# 5. top-p: sort big to small, running total, stop once the letters ranked above already reach p.
sorted_p, order = torch.sort(p, descending=True)
running = torch.cumsum(sorted_p, dim=-1)
print("sorted probs :", [round(float(x), 3) for x in sorted_p])
print("running total:", [round(float(x), 3) for x in running])
print("order        :", [letters[i] for i in order])
before = running - sorted_p
print("kept at p=0.9:", [bool(b) for b in (before < 0.9)])
```

```text
T=1          a=0.076 b=0.563 c=0.028 d=0.207 e=0.126   sum=1.000
T=0.3        a=0.001 b=0.958 c=0.000 d=0.034 e=0.006   sum=1.000
T=1.0        a=0.076 b=0.563 c=0.028 d=0.207 e=0.126   sum=1.000
T=2.0        a=0.138 b=0.375 c=0.084 d=0.227 e=0.177   sum=1.000
ten draws : ['e', 'd', 'b', 'e', 'c', 'd', 'b', 'b', 'b', 'b']
10000 draws, share of each letter: [0.073, 0.563, 0.027, 0.204, 0.132]
top 3 scores: [2.0, 1.0, 0.5] at places [1, 3, 4]
top-3 kept   b=0.629 d=0.231 e=0.140
sorted probs : [0.563, 0.207, 0.126, 0.076, 0.028]
running total: [0.563, 0.77, 0.896, 0.972, 1.0]
order        : ['b', 'd', 'e', 'a', 'c']
kept at p=0.9: [True, True, True, True, False]
```

Read the output beside the page.

- **The three `T` rows.** `b` gets 0.958, then 0.563, then 0.375. Was your up-or-down right? Same scores, three sets of chances, and the model did not change. The `T=1` and `T=1.0` rows are identical: dividing by one changes nothing.
- **`torch.multinomial(p, n, replacement=True)`** is a spinning wheel in which letter `i` owns a share `p[i]` of the rim. It returns **positions** (0 to 4), so we look up the letter ourselves. `replacement=True` lets the same letter come up again, which you need when you draw 10,000 times from five letters.
- **The 10,000 draws** give the shares `0.073, 0.563, 0.027, 0.204, 0.132`, close to the table's `0.076, 0.563, 0.028, 0.207, 0.126`. That is the check that the wheel does what the table says.
- **`torch.topk(scores, 3)`** returns a **pair**: the three biggest scores, and the places they came from (`b`, `d`, `e`). It is another pair, like `out, h_n = rnn(x)` in Week 8. Softmax over only those three gives `0.629, 0.231, 0.140`: the dropped letters' share has been handed back out in proportion. That is **top-k**.
- **`torch.sort` and `torch.cumsum`.** `sort(..., descending=True)` also returns a pair: the values from big to small, and where each one was. `cumsum` is a running total: `0.563, 0.770, 0.896, ...`.

**Temperature does not change which letter is best. It changes how much the best one wins by.** Low `T` means a big win (sharp); `T = 1` is honest; high `T` means a small win (flat). Push `T` toward 0 and you get greedy; push it very high and you get a fair die.

### 4. Top-k and top-p, in words

- **Top-k:** keep the `k` best letters, forget the rest, share the chance out again among the survivors.
- **Top-p:** keep the *smallest* group of best letters whose chances add up to at least `p`.

Try top-p by hand with `p = 0.9` on the sorted chances `0.563, 0.207, 0.126, 0.076, 0.028`. The running total is `0.563, 0.770, 0.896, 0.972, 1.000`. You need to go down to the **fourth** letter to reach 0.9 (0.896 is just under, 0.972 is over), so four letters stay and only `c` goes. Write which letter goes on page 13.2 **before** your last `five.py` lines print `kept at p=0.9`.

**Top-p adapts; top-k does not.** When the model is sure (0.95 on one letter) top-p keeps one or two letters. When it is unsure it keeps many. Top-k with `k = 5` keeps five either way.

> **📌 The one place to be careful: which total do you test?** A letter is kept if the total of the letters **ranked above it** is still below `p`. It is *not* "the total including this letter is below `p`". That is why `five.py` computes `before = running - sorted_p`. With the wrong test, a top letter that alone holds 0.8 would be dropped when `p = 0.5`, and **nothing is left to choose from**.

Also: `kept = sorted_p * (before < p)`. The test `before < p` gives yes/no for every letter. Multiplying a number by a `True` keeps it (`True` counts as 1); by a `False` zeroes it (`False` counts as 0). Yes keeps the number, no zeroes it.

---

## 💻 The Four Pickers: `samplers.py`

Each picker takes the scores and returns a plain whole number: the id of the chosen letter. Type it one function at a time. (`int(...)` turns a one-number tensor into a plain number; without it a tensor would not work as a letter id.)

```python
# samplers.py - the four ways to turn scores into one choice. Each takes scores, returns an int id.
import torch
import torch.nn.functional as F


def greedy(scores):
    return int(scores.argmax())


def temperature(scores, T=1.0):
    probs = F.softmax(scores / T, dim=-1)
    return int(torch.multinomial(probs, 1))


def top_k(scores, k=5, T=1.0):
    vals, ids = torch.topk(scores, k)                 # the k best scores and where they were
    probs = F.softmax(vals / T, dim=-1)               # softmax over the survivors = renormalised
    return int(ids[torch.multinomial(probs, 1)])


def top_p(scores, p=0.9, T=1.0):
    probs = F.softmax(scores / T, dim=-1)
    sorted_p, order = torch.sort(probs, descending=True)
    before = torch.cumsum(sorted_p, dim=-1) - sorted_p     # total of the letters ranked above
    kept = sorted_p * (before < p)                         # keep a letter if the ones above it had not yet reached p
    return int(order[torch.multinomial(kept, 1)])          # multinomial does not need them to add to 1
```

It prints nothing; other files import it. Three things to notice:

- `greedy` uses `argmax`, which has no randomness at all. The same start gives the same scores and the same top letter, every time.
- `multinomial` **does not need its chances to add to 1**, only to be non-negative and not all zero. That is why `top_p` can hand it the `kept` list with zeroes in it and nothing is re-divided.
- **Tiny `p` is greedy:** the top letter always passes the test, because nothing is ranked above it. The same goes for `k = 1`. You will check this in the workbook.

### Where the choosing rule plugs in: `namegen.py`

`make_name(model, pick)` in `namelm.py` generates one name. It asks the model for scores, calls `pick(scores)`, and feeds the chosen letter back in as the next input. Think of `pick` as a socket. Greedy fits it. `lambda s: temperature(s, T=0.5)` is `temperature` with its setting fixed, so it fits too (a one-line function, Week 4). **The model is the same in every line. Only the plug changes.**

Type this file. It trains the model (about 4 seconds), then makes **200** names per rule, seeding each rule the same so the comparison is fair.

```python
# namegen.py - Week 13: the same trained model, five ways of choosing. Count, do not eyeball.
import torch
from namelm import train, make_name, NAMES
from samplers import greedy, temperature, top_k, top_p

model, final_loss = train()
print(f"trained: final loss {final_loss:.3f}")
real = set(NAMES)

def run(label, pick, n=200, seed=0):
    torch.manual_seed(seed)
    names = [make_name(model, pick) for _ in range(n)]
    new = [x for x in names if x not in real and x != ""]
    print(f"{label:<14} distinct {len(set(names)):>3}/{n}   new {len(new):>3}/{n}   first five: {names[:5]}")
    return names

run("greedy", greedy)
run("T=0.5", lambda s: temperature(s, T=0.5))
run("T=1.0", lambda s: temperature(s, T=1.0))
run("T=1.5", lambda s: temperature(s, T=1.5))
run("top-k 5", lambda s: top_k(s, k=5))
run("top-p 0.9", lambda s: top_p(s, p=0.9))
run("T=1.5 top-p .9", lambda s: top_p(s, p=0.9, T=1.5))
```

```text
trained: final loss 1.026
greedy         distinct   1/200   new   0/200   first five: ['andrei', 'andrei', 'andrei', 'andrei', 'andrei']
T=0.5          distinct 111/200   new   2/200   first five: ['sanna', 'anders', 'katya', 'rachna', 'aditi']
T=1.0          distinct 155/200   new  32/200   first five: ['serge', 'anzel', 'maren', 'arnav', 'zuri']
T=1.5          distinct 192/200   new 118/200   first five: ['ulaj', 'iris', 'wanda', 'olan', 'jadei']
top-k 5        distinct  73/200   new  18/200   first five: ['devika', 'renata', 'rachna', 'rustam', 'asha']
top-p 0.9      distinct 128/200   new   7/200   first five: ['esha', 'andrei', 'hilde', 'anders', 'kajsa']
T=1.5 top-p .9 distinct 159/200   new  50/200   first five: ['esran', 'amara', 'hilde', 'anders', 'kajsa']
```

Before you read the table, cover the `new` column and write on page 13.1 which row you think makes the **best** names. We will test that in a moment.

What the columns mean: **distinct** is how many different names there are out of 200. **new** is how many names are **not in the list of 231** the model trained on. That is the **novelty rate**.

- Greedy: 1 distinct. `andrei`, 200 times. There is no randomness to make it do anything else.
- `T=0.5`: 111 distinct but only **2** new. It mostly recites the training list.
- `T=1.5`: 192 distinct, **118** new. Lots of new strings. Are they names?
- Top-p 0.9 sits in between: 128 distinct, 7 new. Top-p with `T=1.5` cuts the wild tail off the hot sampler (new drops from 118 to 50).

**Why greedy repeats.** Look at the first letter. The model's top five first letters are `a 0.09`, `s 0.06`, `d 0.052`, `c 0.051`, `r 0.05`. It is not sure at all. Greedy takes that tiny edge for `a` every time, then `n`, `d`, `r`, `e`, `i`, and stops. There is only one road.

> **🚫 What today does not show.**
> 1. **Greedy is not "the best answer".** It is the best guess *one letter at a time*. We did not test whether it finds the best *name*, so we claim nothing either way.
> 2. **A low temperature does not make the model "more accurate".** It makes it repeat the commonest thing. At `T=0.5`, 198 of 200 names are copies of training names. That is recitation.
> 3. **"New" is not "good".** The new count includes every misspelling. And "new" is measured against a list of **231 typed names**, not against the world: `lora` is new to the list and is a perfectly real name.

---

## 🎲 Your Turn

### The Name Tasting

The 200-name table counts names. It cannot say which are *good*. So you judge first and see the counts after.

Below are **forty names**. Ten came from each of four samplers, shuffled, with no labels. Your teacher knows which is which and will reveal it at the end. For each name, write **R** if you could imagine meeting someone with that name, **X** if not. One second each. Go with your gut. Do not talk, and do not look at anything else until all forty are marked.

| | | | | |
|--|--|--|--|--|
| 1. vilma | 2. kasild | 3. marisol | 4. senna | 5. cato |
| 6. armun | 7. lora | 8. gemra | 9. celia | 10. zaid |
| 11. pavel | 12. deria | 13. tarek | 14. tatiana | 15. lakshmi |
| 16. urho | 17. inditrr | 18. olga | 19. nnanvir | 20. gustav |
| 21. magnus | 22. jarl | 23. gurgus | 24. anika | 25. valeria |
| 26. armin | 27. devika | 28. brenan | 29. pablo | 30. javier |
| 31. bela | 32. anders | 33. oorja | 34. felix | 35. jaden |
| 36. kavya | 37. klara | 38. dara | 39. rodea | 40. bianca |

Mark them on workbook page 13.3. After the reveal you will count your own **R**s per sampler and compare them with the **new** column above. The lesson is in the comparison: **new and good are different questions.** Ten names a sampler is a sample, not a finding.

### The model grades itself: `exposure.py`

Here is a different question. Give the model a name and the **true** previous letters, and ask: how surprised is it by each next letter? That is the loss per letter. Lower means less surprised.

**Predict first** (page 13.4): which scores worse on average, the 231 real names, or 200 names the model made itself? Write your answer and your reason.

```python
# exposure.py - Week 13: how does the model score its OWN names, compared with the real ones?
import torch
import torch.nn.functional as F
from namelm import train, make_name, NAMES, PAD, VOCAB_SIZE, MAXLEN, encode
from samplers import temperature

model, _ = train()

def per_letter_loss(words):
    """Average loss per letter for each word, with the TRUE previous letters fed in (teacher forcing)."""
    out = []
    with torch.no_grad():
        for w in words:
            ids = torch.tensor([encode(w[:MAXLEN - 1])])
            x = torch.cat([torch.full((1, 1), PAD), ids[:, :-1]], dim=1)
            loss = F.cross_entropy(model(x).reshape(-1, VOCAB_SIZE), ids.reshape(-1), ignore_index=PAD)
            out.append(loss.item())
    return torch.tensor(out)

def generate(T, n=200, seed=7):
    torch.manual_seed(seed)
    names = [make_name(model, lambda s: temperature(s, T=T)) for _ in range(n)]
    return [x for x in names if x != ""]

real = per_letter_loss(NAMES)
print(f"real names     n={len(real):>3}  mean {real.mean():.3f}  median {real.median():.3f}")
for T in [1.0, 0.5]:
    own = per_letter_loss(generate(T))
    print(f"own, T={T}     n={len(own):>3}  mean {own.mean():.3f}  median {own.median():.3f}"
          f"  gap {own.mean() - real.mean():+.3f}  worst {own.max():.2f}"
          f"  share above 1.5: {float((own > 1.5).float().mean()):.3f}")
print(f"real above 1.5: {float((real > 1.5).float().mean()):.3f}")
```

```text
real names     n=231  mean 0.954  median 0.936
own, T=1.0     n=200  mean 1.122  median 0.957  gap +0.167  worst 2.74  share above 1.5: 0.175
own, T=0.5     n=200  mean 0.920  median 0.908  gap -0.035  worst 2.44  share above 1.5: 0.010
real above 1.5: 0.000
```

Most people guess the model's own names score better, "because they are its own". The real names average **0.954** per letter and the model's own `T=1` names average **1.122**. The model is more surprised by its own names. And **17.5%** of its own names score above 1.5 per letter, against **0%** of the real names.

**Why might that be?** Draw it:

```text
   TRAINING                          GENERATING
   gets the TRUE previous letter     gets its OWN previous letter
        a n d r _                         a n d t _
        ^ ^ ^ ^                                  ^   one wrong letter...
        always on the road                        ...and now the prefix is one it never practised on
```

In training, someone always hands the model the right letters. In generating, nobody does. One unlikely letter and it is reading a prefix it has hardly seen. That is **exposure bias**: it was only ever *exposed* to the truth.

**Is it proved by 1.122 against 0.954?** No. Three things could all sit inside that gap:

1. **Drift,** as described above.
2. **Plain sampling.** At `T=1` the model picks letters it gave *low* chance on purpose. The same model then scores the finished name and sees those letters as unlikely.
3. **Memorising.** At `T=0.5` it recites names it has seen, and a name it has seen scores low.

Look at the `T=0.5` row: the gap closes to -0.035. That fits the drift story. It also fits "it is just reciting". **Two stories, one number.** Say what you measured: *the model is more surprised by its own names than by real ones, and a long right tail is where it is most surprised. This is consistent with exposure bias; it does not prove it.* We also did not feed the model its own prefix and the true prefix at the same spot to compare directly, and we did not repeat at other seeds.

---

## 🔬 Break It On Purpose

Temperature is a division, so what happens if someone wants to make the model greedy by setting `T = 0`? **DELIBERATE:** this file is written to fail.

```python
# DELIBERATE: a temperature of exactly zero, "to make it greedy".
import torch
from samplers import temperature

torch.manual_seed(0)
scores = torch.tensor([0.0, 2.0, -1.0, 1.0, 0.5])
print(temperature(scores, T=0.5))
print(temperature(scores, T=0.0))
```

```text
1
Traceback (most recent call last):
  File "/private/tmp/w13s/bad.py", line 8, in <module>
    print(temperature(scores, T=0.0))
  File "/private/tmp/w13s/samplers.py", line 12, in temperature
    return int(torch.multinomial(probs, 1))
RuntimeError: probability tensor contains either `inf`, `nan` or element < 0
```

The first line, with `T=0.5`, works. The second does not. Read the last line of the error, then work out on paper what the scores divided by `0.0` turn into (page 13.5). The lesson for the Bug Log: **`T` must be bigger than zero; for "as greedy as possible" use `greedy`, or a tiny `T`, or `k = 1`.**

---

## 🚀 Optional: Does the Memory Bridge a Gap? `copytask.py`

This is your homework file, and it closes the loop with Weeks 8 to 11. The task: the model sees 5 random symbols (out of 8), then a **gap** of `D` filler symbols, then must write the same 5 symbols again. To do it, the memory has to carry the 5 symbols across the gap. A model guessing has a chance of `1/8 = 0.125` per symbol. We score only the five copied symbols.

It trains ten small models (an `nn.RNN` and an `nn.LSTM`, each at five gaps), 1,500 steps each. **It takes about 30 seconds.** Nothing is wrong unless it takes more than 2 minutes. `out, _ = rnn(x)` keeps the first half of the pair; the underscore is a name meaning "I do not need this".

```python
# copytask.py - Week 13 homework + prep: how long a gap can the memory bridge? (5 symbols, a gap, the same 5 again)
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(1)
L, N_SYM = 5, 8                      # copy 5 symbols; 8 different symbols; id 8 = "filler"
FILL = N_SYM

def batch(B, D):
    core = torch.randint(0, N_SYM, (B, L))                      # the 5 symbols to remember
    seq = torch.cat([core, torch.full((B, D), FILL), core], dim=1)
    start = torch.full((B, 1), FILL)
    return torch.cat([start, seq[:, :-1]], dim=1), core         # shift right: teacher forcing

class Copier(nn.Module):
    def __init__(self, kind, hidden=64):
        super().__init__()
        self.emb = nn.Embedding(N_SYM + 1, 16)
        self.rnn = nn.RNN(16, hidden, batch_first=True) if kind == "rnn" else nn.LSTM(16, hidden, batch_first=True)
        self.out = nn.Linear(hidden, N_SYM + 1)

    def forward(self, x):
        h, _ = self.rnn(self.emb(x))
        return self.out(h)

def run(kind, D, steps=1500, seed=0):
    torch.manual_seed(seed)
    model = Copier(kind)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    for _ in range(steps):
        x, core = batch(64, D)
        loss = F.cross_entropy(model(x)[:, -L:].reshape(-1, N_SYM + 1), core.reshape(-1))   # score only the copy
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    torch.manual_seed(99)
    with torch.no_grad():
        x, core = batch(512, D)
        return float((model(x)[:, -L:].argmax(dim=-1) == core).float().mean())

for kind in ["rnn", "lstm"]:
    print(kind, "  ".join(f"D={D} {run(kind, D):.3f}" for D in [1, 5, 10, 20, 40]), flush=True)
```

```text
rnn D=1 1.000  D=5 0.384  D=10 0.129  D=20 0.127  D=40 0.127
lstm D=1 0.996  D=5 0.987  D=10 0.959  D=20 0.130  D=40 0.130
```

Read the table, not the clock. Each number is the share of copied symbols that came out right. On page 13.4 write, for each row, the gap at which it falls to chance (0.125, within a hundredth or two). This is **one seed at one training budget** (1,500 steps, 64 hidden units). We did not test longer training or other seeds, so we can say what happened here and nothing about what RNNs or LSTMs can do in general. Treat a difference of about 0.05 in a single cell as noise.

---

## 🔑 Wrap Up

Three things you built today:

1. **Scores to chances to a choice:** `F.softmax(..., dim=-1)`, then `torch.multinomial`.
2. **Three ways to shape the choice:** a dial (temperature), a count (top-k), a total (top-p).
3. **The model reads its own words,** and nobody hands it the truth.

What you did **not** do: change the model, fix exposure bias, or prove it. There is a trade between repeating and rambling, and the sampler is how you choose the point. Which sampler would you use for naming a baby, and which for a spelling checker? Give a reason for each.

**A look ahead.** The softmax you typed today comes back in Week 14 with a different job: deciding how much each earlier word matters. Same function, new reason.

---

## 📤 Homework

Complete workbook pages 13.1 to 13.5 (about 60-75 minutes):

1. **Predict, then measure (page 13.2).** Five new scores for the letters `s t a r e` are on the page. **Before** you run anything, write for `T = 0.3, 1, 2` which letter will be most likely and whether its share goes up or down. Then fill the table with `F.softmax(scores / T, dim=-1)` and check yourself.
2. **The copy-task sweep (page 13.4):** run `copytask.py` and report both rows, what chance is, and the gap at which each row falls to chance.
3. **Top-k and top-p by hand** on the page's scores, and the **sampler table** from class with one word for each row: *repeats*, *rambles*, or *in between*.

**Optional.** Run `namegen.py`'s `T=1.0` line with three different seeds and write down the three "new" counts. How big is the spread? Then say whether a gap of one or two names between two samplers means anything.

---

## 📖 Words from this week

| Word | Meaning |
|---|---|
| **scores** | the model's raw answer: one number per possible next letter |
| **softmax** | turns scores into chances that add to 1 |
| **sampling** | choosing the next letter from the scores by some rule |
| **greedy** | always take the highest score; no randomness |
| **temperature** (`T`) | divide the scores by `T` before softmax; low makes the best letter win by more, high by less |
| **top-k** | keep only the `k` best letters, share the chance out among them |
| **top-p** (nucleus) | keep the smallest set of best letters whose chances add up to at least `p` |
| **`dim=-1`** | "along the last axis" |
| **novelty rate** | how many generated names are not in the training list; **not** a quality score |
| **exposure bias** | trained on the true previous letters, but at generation time fed its own |

---

[⬅ Week 12](week-12.md) · [Course Home](../README.md) · [Week 14 ➡](week-14.md) · [Workbook](../workbook/week-13.md)
