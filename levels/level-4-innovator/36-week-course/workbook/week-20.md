# Workbook — Week 20: Tokenizers, BPE From Scratch

**Name:** ________________________________  **Date:** ______________

[⬅ Week 19](week-19.md) · [📖 Read the chapter first](../student-guide/week-20.md) · [Course Home](../README.md) · [Next ➡](week-21.md)

---

> **Rules for this workbook.** Every number you write in a report this year must be one **your own run printed in the last 24 hours.** The digits in the worked examples and in the answers came from real CPU runs (Python 3, no GPU). **Nothing in this week is random**, so there is no seed to write down, and your numbers for the corpus files should match mine exactly. The one thing that can differ is the chart on page 20.5, because it reads Python's own source files and those change a little between Python versions. Timings differ on every machine. By-hand numbers are plain arithmetic.
>
> **Predict first, then run.** On pages 20.1, 20.4, 20.5 and 20.6 you write your guess *before* you run anything. A wrong guess is useful. A guess written after the run is not a guess.
>
> **Two kinds of page.** Pages **20.1 to 20.6 each have a PRACTICE part** (small, on text or strings I ran for you, so you can check your reading) **and a YOURS part** (what your own class files print). The practice parts are not your results and must not be pasted into your report.
>
> **Everything is real. There is no stand-in and no scripted backend anywhere in this workbook.** The tokenizer is your own `bpe.py`, trained on your CPU on text that is already on your computer. The `tokenizers` library appears **only** on pages 20.4 and 20.5, **only** as a trainer run locally on local text, and **only** through the given `make_theirs` and `their_tokenizer` functions from class. What a tokenizer trained on a 6,972-character corpus does says something about *that tokenizer* and nothing about any product's.
>
> **Keep your class files.** You need `bpe.py`, `samples.py`, `test_bpe.py`, `text_merges.py`, `compare.py`, `grow.py` and `cost.py` from class. The practice pages add **four** small files you type yourself (`check201.py`, `check203.py`, `check204.py`, `check205.py`, all in the answers section, for checking only) and three deliberate bugs on page 20.7. Run everything from the folder that contains `l4lib/`. The longest run is `grow.py` (about 20 to 25 seconds); everything else finishes in a few seconds. Nothing downloads anything.
>
> Use a **calculator** and carry **two decimals** unless a page says otherwise.

---

## ✅ Warm-Up (5 min)

Five quick questions about **Weeks 17 to 19**.

**W1.** Your corpus has 28 different characters. A model that knows nothing gives each one `1/28`. Its loss on one character is `ln 28` = ____________ (three decimals).

**W2.** In your TinyGPT, a "token" has been one **character** so far. Write what the model's list of possible tokens (its vocabulary) looked like for the corpus: ________________________________

**W3.** A model's loss on text it trained on is 1.0 and on text it did not train on is 1.4. What is the **gap**? ____________ Is the gap a property of the model alone, or of the model *and* the text? ________________________________

**W4.** Week 19's rule for a fair ablation: change ______ thing, keep the ______ , the ______ and the ______ the same.

**W5.** A result is "too good". Name the question Week 19 taught you to ask first: *can the model see* ________________________________

---

## 🔮 Page 20.1 — Three Ways to Cut (15 min, pen first)

Your TinyGPT cuts text into **characters**. Today there are two more ways: **words**, and **pieces** found by counting.

**Predict before you run `text_merges.py`.** Use the Week 17 corpus (6,972 characters).

| Guess | My number |
|---|:--:|
| How many **words** does the corpus have? | ________ |
| How many **different** words? | ________ |
| How many of those different words occur **only once**? | ________ |
| With 300 merges, will the corpus take **more** or **fewer** tokens than its 6,972 bytes? How many (a guess)? | ________ |

### Part A — PRACTICE (a sentence of 41 characters, by hand)

```text
the old man and the old dog and the river
```

**A1. Cut it three ways.** Count with a pencil.

| Cut | How many units | How many **different** units | How many units occur **once** |
|---|:--:|:--:|:--:|
| characters (spaces count as characters) | ________ | ________ | (skip) |
| words | ________ | ________ | ________ |

**A2.** `dog` and `river` and `man` each occur once. If a word model had been trained on *these ten words only* and then met `the old baker`, which word is a **hole**? ____________ Why can a *byte* model never have a hole? ________________________________

**A3.** I trained my own `bpe.py` for 300 merges on the **corpus** (not on this sentence) and cut the sentence. It came out as **20 tokens**, nine of them lone spaces (the check file is in the answers). Without looking at the answers: how many tokens would **words plus lone spaces** be (10 words and 9 spaces between them)? ________ How many does BPE save? ________

**A4.** The same tokenizer was asked to write `the old baker and the cricket`. `baker` came out as one token; `cricket` came out as `c`, `ri`, `c`, `ket`. Write the two sentences a word model and a byte-pair model would each have to say about `cricket`. Word model: ________________________________ BPE: ________________________________

### Part B — YOURS (`text_merges.py` from class)

Run `text_merges.py`. Copy what it printed.

| Quantity | My run printed |
|---|:--:|
| characters / distinct characters | ________ / ________ |
| words / distinct words / words that occur once | ________ / ________ / ________ |
| the commonest word and how often | ____________ |
| merges learned / vocabulary | ________ / ________ |
| tokens / bytes per token | ________ / ________ |
| lone spaces among the tokens (read it from section 9 of the chapter, or count them yourself with one line of code) | ________ |

**B1.** Compare with the guesses in the first table. Which was furthest out, and by how much? ________________________________

**B2.** Write the first **ten** merges: ________________________________________________ Circle the ones that are English words. Put a box around one that is **not** a word or a word-ending. Does BPE know any English? ________________________________

**B3. Size against merges.** Fill from your run:

| Merges asked for | 0 | 10 | 100 | 300 | 500 | 1000 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Merges learned | ____ | ____ | ____ | ____ | ____ | ____ |
| Bytes per token | ____ | ____ | ____ | ____ | ____ | ____ |

Why do 500 and 1000 give the **same** row? ________________________________________________

**B4. Vocabulary arithmetic.** A vocabulary is 256 + the number of merges **learned**. If you asked for 1000 and got fewer, the vocabulary is ________ . Vocabulary for 100 merges: ________ .

**B5. The weakness.** About 40% of the 3,227 tokens are lone spaces. What rule in the code makes every space its own token? ________________________________ What would you change, and what would you have to **measure** before saying it was better? ________________________________________________

---

## ✂️ Page 20.2 — Merge by Hand (25 min, pencil only, no code until the end)

Rules, every time:
- Count pairs of neighbouring letters **inside** each word, **weighted** by how often the word occurs. Never across a space.
- Glue the commonest pair into one new piece. **Recount** with the new piece in place.
- On a tie, the pair that comes first in the alphabet wins; **letters come before made-up pieces**.

### Part A — PRACTICE (a different card)

```text
sat x 4      sit x 2      said x 3      it x 1
```

**A1. First count table.** There are six different pairs. Fill them in (list each pair once and weight it).

| Pair | Where it occurs | Count |
|---|---|:--:|
| `s a` | sat 4, said 3 | ______ |
| `a t` | ____________ | ______ |
| `a i` | ____________ | ______ |
| `i d` | ____________ | ______ |
| `i t` | ____________ | ______ |
| `s i` | ____________ | ______ |

**A2.** Which pair wins? ____________ Glue it. Write the four words now: ________________________________

**A3. Merges 2 to 5.** Recount after each glue. Merge 3 has a tie: write which pairs tie and which you chose.

| Merge | Pair glued | Count | New piece | Words now |
|:--:|---|:--:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**A4.** Encode **`sits`** using your merges, earliest first: ________________________________ Encode **`dais`**: ________________________________ Why is `dais` so many pieces if `said` is one? ________________________________

### Part B — YOURS (the class card, from the chapter)

```text
the x 5      then x 2      than x 2      hat x 3
```

**B1. First count table.** (Pairs inside words, weighted.)

| Pair | `th` | `he` | `ha` | `at` | `en` | `an` |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Count | ____ | ____ | ____ | ____ | ____ | ____ |

**B2. Four merges.**

| Merge | Pair glued | Count when glued | New piece | The four words now |
|:--:|---|:--:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

**B3.** At merge 5 three pairs tie. Write them: ________________________________ Which did you take, and by what rule? ________________________________ Does your choice change the tokens of `then`? ________________________________

**B4.** Encode `thathen` with your **four** merges, earliest first: ________________________________ Does `hat` appear inside it? ____ Why is `that` not a piece? ________________________________

**B5. Now check with the code.** Only after the card is done, run `card_check.py` from the chapter. Which merge was the first where the code and your card differed? ______ What had you forgotten to do in that round? ________________________________

---

## 💻 Page 20.3 — Your `bpe.py` (25 min)

### Part A — PRACTICE (bytes by hand, then tokens)

**A1. Characters and bytes.** A character in the ASCII range is **1** byte; `é` and `ï` are **2**; a Devanagari or Japanese character is **3**; an emoji is **4**. Fill in the bytes by hand.

| String | Characters | Bytes (by hand) |
|---|:--:|:--:|
| `café` | 4 | ______ |
| `naïve café` | 10 | ______ |
| `日本語` | 3 | ______ |
| `🙂🙂` | 2 | ______ |
| `Tuesday` | 7 | ______ |

**A2.** The check file (`check203.py`, in the answers) printed these token counts for 300 merges trained on the corpus: `café` 5 · `naïve café` 12 · `日本語` 9 · `🙂🙂` 8 · `Tuesday` 4. For each, write bytes per token to two decimals, and say **which of them have nothing merged**.

| String | Bytes per token | Anything merged? |
|---|:--:|---|
| `café` | ______ | ______ |
| `naïve café` | ______ | ______ |
| `日本語` | ______ | ______ |
| `🙂🙂` | ______ | ______ |
| `Tuesday` | ______ | ______ |

**A3.** `Tuesday` is 7 bytes and 4 tokens. Could `decode` give back the 7 bytes from 4 ids? What does `decode` need to know? ________________________________

**A4. Vocabulary.** Asked for 100 merges on the corpus I got 100 learned; asked for 1000 I got 400. Write both vocabularies: ________ and ________ . Why did 1000 not give 1256? ________________________________

### Part B — YOURS (`bpe.py` and `test_bpe.py`)

Type `bpe.py` in the five pieces from the chapter, testing after each. Write down any error you hit in the **Bug Log** (page 20.8). Then run `test_bpe.py`.

**B1.** How many round trips passed? ______ of ______ .

| Text | Characters | Bytes | Tokens |
|---|:--:|:--:|:--:|
| `The cricket team practised on Tuesday.` | ______ | ______ | ______ |
| the Hindi greeting | ______ | ______ | ______ |
| `I love 🍕 and 🙂!` | ______ | ______ | ______ |
| the empty string | ______ | ______ | ______ |
| `😀😀😀` | ______ | ______ | ______ |
| the whole corpus | ______ | ______ | ______ |

**B2.** The Hindi greeting is 13 characters. Why 37 tokens? ________________________________ Why does the empty string give 0? ________________________________

**B3. The test that was missing.** `nomerges.py` made every round trip `True` with a tokenizer that learned nothing. Write **one extra test** you would add to `test_bpe.py` that a do-nothing tokenizer **fails**. Write it as a line of Python or as a sentence:

________________________________________________________________

Add it to the file and run it. It printed: ________________________________ Your test would have caught which tokenizer? ☐ one that learned zero merges ☐ one with the tie-break flipped ☐ one that applied the latest merge first (it would *not*, unless you compare with a trusted answer) . Explain your ticks: ________________________________

---

## 🔬 Page 20.4 — Does the Library Agree? (20 min)

**Predict first.** `make_theirs` builds the production BPE trainer, run locally on your corpus. Before you run `compare.py`, write: *will it give exactly your token count?* Yes / No / Only if ____________________ . My guess for its count with equal settings: ________ .

### Part A — PRACTICE (a smaller table that is not yours)

I ran the same three-way comparison (`check204.py`, in the answers) on the **first 3,000 characters** of the corpus with only **100 merges**. It printed:

```text
bytes: 3000
mine:                         1736 tokens
tokenizers, same chunk rule:  1736 tokens
tokenizers, its default cut:  1344 tokens
pieces that differ: 0
lone spaces among mine: 553
```

**A1. Fill in.**

| Tokenizer | Tokens | Bytes per token (3000 divided by tokens) |
|---|:--:|:--:|
| mine | 1736 | ______ |
| library, same chunk rule | 1736 | ______ |
| library, default cut | 1344 | ______ |

**A2.** The default cut uses `1344 / 1736` = ________ of my tokens, so it saves ________ % . (Two decimals, then a percentage.)

**A3.** Which row would you use to say "my code does what the library does"? ____________ Which row tells you the two **cutting rules** are different? ____________

**A4.** 553 of my 1,736 tokens are lone spaces. What fraction? ________ % Is it more or less than the 40% of the full corpus? ________

**A5.** One honest sentence about what the match shows **and** what it does not show. (Hint: it does not say which tokenizer is better, and it does not say a model trained on these tokens would do better.) ________________________________________________

### Part B — YOURS (`compare.py`)

| Tokenizer | Tokens on the corpus (300 merges) |
|---|:--:|
| mine | ________ |
| library, same chunk rule | ________ |
| library, default cut | ________ |
| pieces that differ (same chunk rule) | ________ |

**B1.** `'the baker'` with mine: ________________________________ with the library's default: ________________________________ What does the `Ġ` mean? ________________________________

**B2.** Write four sentences: the three numbers, the 0, the reason the fourth number is different, and one thing the match does not prove.

________________________________________________________________

________________________________________________________________

**B3.** Run the two lines at the bottom of `compare.py` for Hindi and emoji. Did the library round-trip them? ____ Why, in one clause? ________________________________

---

## 📈 Page 20.5 — Bytes per Token as the Text Grows (25 min)

**Predict.** As the training text grows from 2,000 to about 320,000 characters, bytes per token on **unseen** text will go: ☐ up ☐ down ☐ stay flat . It will start near ________ and end near ________ . Draw your predicted curve here (x axis: training characters, log scale; y axis: bytes per token):

```text
 bytes
 per
 token
   3 |
     |
   2 |
     |
   1 |
     +-----------------------------------------
       2k      10k      50k      300k   characters
```

### Part A — PRACTICE (a smaller experiment, not yours)

`check205.py` (in the answers) trains `bpe.py` on the first `n` characters of three of Python's own source files (`textwrap`, `string`, `heapq`: 53,214 characters in all), asks for **200 merges**, and measures on the first 10,000 characters of `difflib.py`, which was **not** in the training text. It printed:

```text
pool: 53214 characters   test: 10000 characters
train on   1000: merges 130  bytes per token 1.431
train on   3000: merges 200  bytes per token 1.574
train on  10000: merges 200  bytes per token 1.616
train on  30000: merges 200  bytes per token 1.665
train on  53214: merges 200  bytes per token 1.694
```

**A1.** Plot the five points on the grid below (x is log scale, so the points are roughly evenly spaced). Join them.

```text
 1.70 |
 1.65 |
 1.60 |
 1.55 |
 1.50 |
 1.45 |
 1.40 |
      +----------------------------------------------
        1k       3k       10k      30k      53k
```

**A2. Gains.** Fill the differences in bytes per token between neighbouring rows.

| From → to | 1,000 → 3,000 | 3,000 → 10,000 | 10,000 → 30,000 | 30,000 → 53,214 |
|---|:--:|:--:|:--:|:--:|
| Gain | ______ | ______ | ______ | ______ |

**A3.** The text grew by a factor of about 3 each time (and 1.8 at the end). Does each step give about the same gain? ________ Say in a sentence what shape the curve has. ________________________________

**A4.** The first row learned **130** merges, not 200. Why? ________________________________ Which rule in `train` stops it? ________________________________

**A5.** Name two things this small experiment does **not** tell you. ________________________________________________

### Part B — YOURS (`grow.py`, about 20 to 25 seconds)

Run `grow.py`. Copy the table:

| Trained on (characters) | Merges learned | Mine | `tokenizers` |
|--:|--:|:--:|:--:|
| 2,000 | ______ | ______ | ______ |
| 5,000 | ______ | ______ | ______ |
| 10,000 | ______ | ______ | ______ |
| 20,000 | ______ | ______ | ______ |
| 50,000 | ______ | ______ | ______ |
| 100,000 | ______ | ______ | ______ |
| all (about 324,000) | ______ | ______ | ______ |

**B1.** My timings at the biggest size: mine ______ s, library ______ s. The ratio is about ______ times. (A ratio, not a reason: we did not read the library, so any reason is a guess. Write one, and mark it **guess**.) ________________________________

**B2.** Open `bytes_per_token.png`. How many lines can you see? ______ Why? ________________________________ Change one thing in the plotting lines so that **both** lines are visible, and say what you changed: ________________________________

**B3.** Write the **reading** in two sentences: what the curve does, **with two of its numbers**; and one limit. ________________________________________________

**B4.** Did your prediction match: up or down, start, end? ________________________________ What would you change in `grow.py` to repeat the chart on a **different** unseen file? ________________________________

---

## 💸 Page 20.6 — Who Pays? (20 min)

**Predict before you run `cost.py`.** How many tokens will the Hindi greeting `नमस्ते दुनिया` (13 characters) take? ________ The three emoji `🍕🙂🍵`? ________ Will the English sentence take more or fewer tokens **per character** than the Hindi? ________

Two quantities, written out in full:

> **bytes per token** = (number of **bytes**) / (number of tokens)     **tokens per character** = (number of tokens) / (number of **characters**)

### Part A — PRACTICE (strings I ran for you)

Tokenizer: your `bpe.py`, 300 merges, trained on the corpus (the same one as `cost.py`). The numbers come from `check203.py`.

| String | Characters | Bytes | Tokens | Bytes per token | Tokens per character |
|---|:--:|:--:|:--:|:--:|:--:|
| `Tuesday` | 7 | 7 | 4 | ______ | ______ |
| `café` | 4 | 5 | 5 | ______ | ______ |
| `日本語` | 3 | 9 | 9 | ______ | ______ |
| `🙂🙂` | 2 | 8 | 8 | ______ | ______ |

**A1.** Which of these is **not** English and costs the **most** tokens per character? ________ By what factor is it more than `Tuesday`? ________ (divide the two tokens-per-character figures.)

**A2.** A friend says: *"`日本語` is hard for tokenizers."* Using only these numbers and what `cost.py` printed for the last line (Hindi, 37 tokens before, 3 after), write what is **wrong** with that sentence: ________________________________________________

**A3.** A different friend computes bytes per token for `日本語` as `3 / 9`. Which number did they use for the top: characters or bytes? ________ What should it be? ________

### Part B — YOURS (`cost.py`, with three strings of your own)

Run `cost.py` once as it is. Then add **three strings of your own** (a name, a sentence in another language you can read, a few emoji) to the list in the loop.

| String | Characters | Bytes | Tokens | Bytes per token | Tokens per character |
|---|:--:|:--:|:--:|:--:|:--:|
| English sentence | | | | | |
| Hindi greeting | | | | | |
| three emoji | | | | | |
| mixed sentence | | | | | |
| my string 1: ______ | | | | | |
| my string 2: ______ | | | | | |
| my string 3: ______ | | | | | |

**B1.** The last line of `cost.py` retrains with Hindi in the text. Hindi greeting: ______ tokens before, ______ after. Why did it change? ________________________________________________ Why must I not say "Hindi is cheap to fix"? ________________________________

**B2. Write the measured / not-measured sentence.** It must say: what tokenizer, trained on what, and one thing that is **not** a conclusion.

**Measured:** ________________________________________________

**Not measured:** ________________________________________________

---

## 🐞 Page 20.7 — Break It on Purpose (25 min)

Each file below is **deliberately broken**. Type it (or copy it), run it from the folder with your finished `bpe.py`, read what it prints, and answer **before** you look at the answers. Two of the three print no error at all.

### Bug A (SILENT): bytes per token worked out with the wrong length

```python
# DELIBERATE BUG 20.7-A (SILENT): bytes per token worked out with len(s), which counts CHARACTERS, not bytes.
from bpe import train, encode
from l4lib.corpus import TEXT
from samples import ENGLISH, HINDI

merges = train(TEXT, 300)
for name, s in [("English", ENGLISH), ("Hindi", HINDI)]:
    k = len(encode(s, merges))
    print(name.ljust(8), "tokens", k, " 'bytes' per token:", round(len(s) / k, 2))      # <- len(s) is characters
```

**A.1** It printed `English tokens 26 ... 1.46` and `Hindi tokens 37 ... 0.35`. Can a tokenizer that starts from bytes ever have **fewer than 1** byte per token? ____ Why is 0.35 a number you should distrust on sight? ________________________________

**A.2** The corrected Hindi figure is ________ . What do you write instead of `len(s)`? ________________________________

### Bug B (loud): one token of a character that is three bytes

```python
# DELIBERATE BUG 20.7-B (loud): decoding ONE token of a three-byte Devanagari letter.
from bpe import train, encode, decode
from l4lib.corpus import TEXT

merges = train(TEXT, 300)
ids = encode("च", merges)
print("ids:", ids)
print("all together:", decode(ids, merges))
print("the first token alone:", decode(ids[:1], merges))
```

**B.1** Copy the **last line** of the error: ________________________________________________

**B.2** In plain words, what does it mean, and why does `decode(ids)` work while `decode(ids[:1])` does not? ________________________________________________ How many ids did `च` give? ______ What would a tool that prints one token at a time have to be ready for? ________________________________

### Bug C (SILENT): the tie-break flipped

`train_flip` is your `train` with one thing changed: the tie-break line says `(pair_counts[p], p[0], p[1])` where the right line says `(pair_counts[p], -p[0], -p[1])`.

```python
# DELIBERATE BUG 20.7-C (SILENT): the tie-break is flipped, so on a tie the pair with the BIGGER numbers wins. Every round trip still passes.
from collections import Counter
from bpe import chunks, merge, encode, decode, make_vocab
from l4lib.corpus import TEXT
import bpe

def train_flip(text, n_merges):
    counts = Counter(chunks(text))
    words = [list(c.encode("utf-8")) for c in counts]
    freqs = list(counts.values())
    merges = {}
    for m in range(n_merges):
        pair_counts = Counter()
        for word, f in zip(words, freqs):
            for pair in zip(word, word[1:]):
                pair_counts[pair] += f
        if len(pair_counts) == 0:
            break
        best = max(pair_counts, key=lambda p: (pair_counts[p], p[0], p[1]))      # <- should be -p[0], -p[1]
        if pair_counts[best] < 2:
            break
        merges[best] = 256 + m
        words = [merge(w, best, 256 + m) for w in words]
    return merges

good = bpe.train(TEXT, 300)
bad = train_flip(TEXT, 300)
vg, vb = make_vocab(good), make_vocab(bad)
tg, tb = encode(TEXT, good), encode(TEXT, bad)
print("right: merges", len(good), " tokens", len(tg), " round trip", decode(tg, good) == TEXT)
print("wrong: merges", len(bad), " tokens", len(tb), " round trip", decode(tb, bad) == TEXT)
print("first six pieces, right:", [vg[i].decode() for i in list(good.values())[:6]])
print("first six pieces, wrong:", [vb[i].decode() for i in list(bad.values())[:6]])
pg = [vg[i].decode() for i in good.values()]
pb = [vb[i].decode() for i in bad.values()]
first = [k for k in range(300) if pg[k] != pb[k]][0]
print("first merge that differs: number", first + 1, " right", pg[first], " wrong", pb[first])
print("merges that differ in total:", sum([1 for a, b in zip(pg, pb) if a != b]))
```

**C.1** Copy the two token counts: right ______ , wrong ______ . Both round trips are `True`. Is the wrong tokenizer "broken"? Say what is true of it and what is not. ________________________________________________

**C.2** The first merge that differs is number ______ . Why did the first nine agree? ________________________________

**C.3** Which check from this week would have **shown** the difference, and what would it have printed? (Remember what `compare.py` printed for the **right** tokenizer.) ________________________________________________

**C.4** Why does the rule "on a tie, take the smaller numbers" matter at all if either choice gives a legal tokenizer? ________________________________________________

---

## 📓 Page 20.8 — The Bug Log

Copy the **last line** of each error, not the whole traceback. Add a row for every real error you hit this week, not only the deliberate ones.

| # | Date | What I typed (the line) | Last line of the error | What it means in plain words | Fix | Page I'll find this on again |
|:--:|---|---|---|---|---|:--:|
| 1 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 2 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 3 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 4 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |
| 5 | ______ | ______________ | ______________ | ______________ | ______________ | ____ |

**A mistake with no traceback** (these matter more; this week had three silent ones in the workbook): write the one I made, or nearly made. ________________________________________________

**The habit for silent mistakes.** Fill in the blanks: *when a tokenizer passes every round trip I also* ____________ *the tokens and* ____________ *against a known good one*; *when a number looks odd for a string in another script I check whether I divided by* ____________ *or by* ____________ .

Write this sentence in your own handwriting:

> **"A round trip tests that nothing was lost; counting the tokens and diffing against a known good tokenizer test whether it is any good."**

________________________________________________________________

---

## 🧠 Self-Check (do this last, from memory)

1. **What is the vocabulary of a tokenizer with 300 merges, and why? What if you asked for 1,000 on the corpus?**

________________________________________________________________

2. **Say the byte-pair rule in three short steps, including what you do after each glue.**

________________________________________________________________

3. **A tokenizer passes 13 of 13 round trips. Name two other checks, and the one tokenizer from this week that passes the round trips and fails both.**

________________________________________________________________

4. **Why does your tokenizer match the library only after you set the chunk rule?**

________________________________________________________________

5. **A tokenizer trained on English meets Hindi and spends 37 tokens on 13 characters. Say what was measured, and one thing it does not show.**

________________________________________________________________

6. **Name one thing today's results do not tell you about any real language model.**

________________________________________________________________

Tick what you can do without looking: ☐ run byte-pair merging by hand with a tie ☐ say characters from bytes from tokens ☐ compute bytes per token and tokens per character ☐ read a diff of two tokenizers ☐ say what a flat curve does and does not mean ☐ spot a silent bug that passes the round trip

---

# ✂️ ANSWERS - keep this page folded until you have finished

> Numbers below came from real runs (`/tmp` scratch folder, Python 3, nothing random). The check files are for checking your reading; the practice numbers are not your results.

### Warm-Up

**W1.** `ln 28` = **3.332**. **W2.** The 28 characters of the corpus (a list of 28 symbols, one per character). **W3.** Gap = 0.4; it depends on the model **and** the text (a different held-out text gives a different gap); it does not say the model is "good" or "bad". **W4.** change **one** thing, keep the **seed**, the **steps** and the **data** the same. **W5.** *can the model see the answer* (the thing it is asked to predict).

### Page 20.1

**Part A.** Characters: **41** units, **14** distinct (`t h e`, the space, `o l d m a n r i v g`); the "occur once" cell for characters is skipped. Words: **10** units, **6** distinct (`the old man and dog river`), **3** occur once (`man`, `dog`, `river`).

A2: `baker` is the hole (also accept `the old baker` has one hole). A byte model has no hole because every text, in any script, is a list of numbers from 0 to 255 and the 256 bytes are always in the vocabulary.

A3: words plus lone spaces = 10 + 9 = **19**; BPE gave 20, so it saves **nothing** here (it is one *more*), because `dog` came out as `do`, `g`: `dog` is not in the corpus as a word but `do` is common. The point is that the **tokens depend on the training text**, not on the sentence. Accept any student who reports 19 and 20 and says honestly that BPE did not win on this sentence. (Check file below.)

```python
# check201.py - Week 20 workbook page 20.1: three ways to cut a short sentence. PRACTICE numbers.
from bpe import train, encode, make_vocab
from l4lib.corpus import TEXT

S = "the old man and the old dog and the river"
words = S.split()
print("characters:", len(S), " distinct characters:", len(set(S)))
print("words:", len(words), " distinct words:", len(set(words)), " words that occur once:", sum([1 for w in set(words) if words.count(w) == 1]))
merges = train(TEXT, 300)
vocab = make_vocab(merges)
ids = encode(S, merges)
print("BPE tokens (300 merges trained on the corpus):", len(ids), " lone spaces among them:", sum([1 for i in ids if vocab[i] == b" "]))
print([vocab[i].decode() for i in ids])
new = "the old baker and the cricket"
print("words the corpus never contains:", [w for w in new.split() if w not in set(TEXT.split())])
print([vocab[i].decode() for i in encode(new, merges)])
```

```text
characters: 41  distinct characters: 14
words: 10  distinct words: 6  words that occur once: 3
BPE tokens (300 merges trained on the corpus): 20  lone spaces among them: 9
['the', ' ', 'old', ' ', 'man', ' ', 'and', ' ', 'the', ' ', 'old', ' ', 'do', 'g', ' ', 'and', ' ', 'the', ' ', 'river']
words the corpus never contains: ['cricket']
['the', ' ', 'old', ' ', 'baker', ' ', 'and', ' ', 'the', ' ', 'c', 'ri', 'c', 'ket']
```

A4 (model answers): *Word model: "`cricket` is not in my list, so I cannot write it at all (a hole)." BPE: "I write it from four pieces I already have; nothing is a hole, but it costs four tokens."*

**Part B.** From the class run: characters **6,972** / distinct **28**; words **1,389** / distinct **362** / once **189**; commonest `the` **234**; merges **300**, vocabulary **556**; tokens **3,227**, bytes per token **2.16**; lone spaces **1,277**. B3 table: asked 0, 10, 100, 300, 500, 1000 gives learned 0, 10, 100, 300, **400**, **400**; bytes per token 1.00, 1.20, 1.69, 2.16, 2.30, 2.30. The last two rows agree because **training stops by itself at 400 merges**: no pair is left that occurs twice. B4: 256 + 400 = **656**; 256 + 100 = **356**. B5: each run of spaces is its own chunk (`\s+|\S+`), so nothing glues to a space. A change such as ` ?\S+|\s+` (a space sticks to the next word) is possible, but the student must **count the tokens** before saying it is better, and even a smaller count does not show a model trained on it would do better. B2: the first ten are `he the an er and in ed ro is or`; `the`, `an`, `and`, `in`, `is`, `or` are words, `ed` and `er` are endings, `ro` is not. BPE finds **common pairs**, not English.

| Marks | |
|---|:--:|
| Part A table filled correctly (41, 10, 6, 3) | 1 |
| Says what a hole is and why bytes have none | 1 |
| Part B table copied from the student's own run | 1 |
| Says BPE found common pairs, not English | 1 |

### Page 20.2

**Part A.** First count table: `s a` **7** (sat 4, said 3) · `a t` **4** (sat) · `a i` **3** (said) · `i d` **3** (said) · `i t` **3** (sit 2, it 1) · `s i` **2** (sit). Merge 1: `s`+`a` (7), new piece `sa`: words `sa t`, `s i t`, `sa i d`, `i t`.

| Merge | Pair glued | Count | New piece | Words now |
|:--:|---|:--:|---|---|
| 1 | `s`+`a` | 7 | `sa` | sa t · s i t · sa i d · i t |
| 2 | `sa`+`t` | 4 | `sat` | sat · s i t · sa i d · i t |
| 3 | `i`+`d` (ties at 3 with `sa`+`i` and `i`+`t`; `i d` has a *letter* first and `d` comes before `t`) | 3 | `id` | sat · s i t · sa id · i t |
| 4 | `i`+`t` (ties at 3 with `sa`+`id`; letters before pieces) | 3 | `it` | sat · s it · sa id · it |
| 5 | `sa`+`id` | 3 | `said` | sat · s it · said · it |

(`a i` stopped existing at merge 1 because `sa` took the `a`. Merge 3: the tie at 3 is between `i d`, `i t` and `sa i`; the rule picks `i d`, because letters come before made-up pieces and `d` comes before `t`. Merge 4: `i t` and `sa id` tie at 3; the letter pair wins.) The code printed `sa`, `sat`, `id`, `it`, `said` with counts 7, 4, 3, 3, 3. A4: `sits` becomes **`s`, `it`, `s`**; `dais` becomes **`d`, `a`, `i`, `s`** (none of its neighbouring pairs `d a`, `a i`, `i s` was ever glued); `said` is one piece because *that exact word* was in the card. Check file:

```python
# check202.py - Week 20 workbook page 20.2: the practice card.
from bpe import train, encode, make_vocab
card = "sat sat sat sat sit sit said said said it"
m = train(card, 5, verbose=True)
v = make_vocab(m)
print([v[i].decode() for i in m.values()])
for w in ["said", "sits", "dais"]:
    print(w, [v[i].decode() for i in encode(w, m)])
```

```text
merge 1 (115, 97) -> 256 count 7
merge 2 (256, 116) -> 257 count 4
merge 3 (105, 100) -> 258 count 3
merge 4 (105, 116) -> 259 count 3
merge 5 (256, 258) -> 260 count 3
['sa', 'sat', 'id', 'it', 'said']
said ['said']
sits ['s', 'it', 's']
dais ['d', 'a', 'i', 's']
```

**Part B.** Same as the chapter's card; first count table: `th` **9** (the 5, then 2, than 2) · `he` **7** · `ha` **5** · `at` **5** · `en` **2** · `an` **2**.

| Merge | Pair glued | Count when glued | New piece | Words now |
|:--:|---|:--:|---|---|
| 1 | `t`+`h` | 9 | `th` | th e · th e n · th a n · h a t |
| 2 | `th`+`e` | 7 | `the` | the · the n · th a n · h a t |
| 3 | `a`+`t` (`h a` ties at 3; `a` comes before `h`) | 3 | `at` | the · the n · th a n · h at |
| 4 | `h`+`at` | 3 | `hat` | the · the n · th a n · hat |

B3: three pairs tie at 2: `a`+`n`, `th`+`a`, `the`+`n`. Whichever the student takes, `then` and `than` each end up as one piece by merge 7 (the code's merges: `th the at hat an than then`), so the choice changes the numbers, not the final pieces on this card. Accept any choice with a reason. B4: with four merges `thathen` is **`th`, `a`, `the`, `n`**; with all seven merges it is **`th`, `a`, `then`**. `hat` is not found: `th` is learned first and takes the `h` that `hat` needed, so `that` is never a piece. A student who writes `that`/`hen` applied merges by eye and not in learned order. B5: any honest answer (usually "I counted `hat` once, not three times", or "I forgot the `h` was gone after `th`").

| Marks | |
|---|:--:|
| First merge `th` with weighted count 9 | 1 |
| Merges 2-4 correct, with recounts | 1 |
| Says what a tie is and gives a rule | 1 |
| Encodes `thathen` in learned order and explains `hat` is not found | 1 |

### Page 20.3

**Part A.** A1 bytes: `café` **5**, `naïve café` **12**, `日本語` **9**, `🙂🙂` **8**, `Tuesday` **7**. A2 bytes per token: `café` 5/5 = **1.00** (nothing merged), `naïve café` 12/12 = **1.00** (nothing merged), `日本語` 9/9 = **1.00** (nothing), `🙂🙂` 8/8 = **1.00** (nothing), `Tuesday` 7/4 = **1.75** (merged: its letters were in the corpus). A3: yes, `decode` joins the bytes each id stands for (`vocab`, built from the merges), then decodes the bytes to text; it needs the **merges**. A4: **356** and **656**; training stopped by itself at 400 merges because no pair was left that occurs twice. Check file:

```python
# check203.py - Week 20 workbook page 20.3: characters, bytes and tokens for new strings. PRACTICE numbers.
from bpe import train, encode, decode
from l4lib.corpus import TEXT

merges = train(TEXT, 300)
for s in ["café", "naïve café", "日本語", "🙂🙂", "Tuesday", "the the the"]:
    ids = encode(s, merges)
    print(repr(s).ljust(14), len(s), "chars", len(s.encode("utf-8")), "bytes", len(ids), "tokens", "round trip:", decode(ids, merges) == s)
for n in [100, 1000]:
    m = train(TEXT, n)
    print("asked", n, "learned", len(m), "vocabulary", 256 + len(m))
```

```text
'café'         4 chars 5 bytes 5 tokens round trip: True
'naïve café'   10 chars 12 bytes 12 tokens round trip: True
'日本語'          3 chars 9 bytes 9 tokens round trip: True
'🙂🙂'           2 chars 8 bytes 8 tokens round trip: True
'Tuesday'      7 chars 7 bytes 4 tokens round trip: True
'the the the'  11 chars 11 bytes 5 tokens round trip: True
asked 100 learned 100 vocabulary 356
asked 1000 learned 400 vocabulary 656
```

**Part B.** 13 of 13 pass.

| Text | Characters | Bytes | Tokens |
|---|:--:|:--:|:--:|
| `The cricket team practised on Tuesday.` | 38 | 38 | 26 |
| Hindi greeting | 13 | 37 | 37 |
| `I love 🍕 and 🙂!` | 15 | 21 | 18 |
| empty string | 0 | 0 | **0** |
| `😀😀😀` | 3 | 12 | 12 |
| the whole corpus | 6,972 | 6,972 | 3,227 |

B2: 37 bytes (three per Devanagari letter, one per space) and no merge touches any of them, so 37 tokens; the empty string has nothing to encode. B3: any of these is accepted: tokens for the corpus must be **fewer than its bytes**; merges learned must be more than zero; bytes per token on the corpus must exceed 1.5; the result must equal a trusted implementation on a fixed text. A line such as

```python
print(len(encode(TEXT, merges)) < len(TEXT.encode("utf-8")))
print(len(merges) > 0)
print(len(TEXT.encode("utf-8")) / len(encode(TEXT, merges)) > 1.5)
```

prints `True`, `True`, `True` for a good tokenizer. *Not accepted:* "another round trip". Ticks: it catches the **zero-merges** tokenizer (it gives 6,972 tokens for 6,972 bytes). It does **not** catch a flipped tie-break (3,230 tokens, still fewer than 6,972, still above 1.5) or latest-merge-first (still fewer, still round-trips); only a comparison against a trusted answer catches those.

| Marks | |
|---|:--:|
| 13 of 13 pass, with the empty string giving 0 tokens | 1 |
| Explains 37 tokens for 13 Hindi characters | 1 |
| Adds a test that is not a round trip | 1 |
| Says which failure it would catch (and which not) | 1 |

### Page 20.4

**Part A.** A1: mine 3000/1736 = **1.73**; library same cut **1.73**; default 3000/1344 = **2.23**. A2: 1344/1736 = **0.77**, saves about **23%** (0.226). A3: row 2 (library, same chunk rule, with 0 pieces differing); row 3 is a different cutting rule. A4: 553/1736 = **31.9%**, which is **less** than 40% (a smaller text, fewer merges, a different mix). A5 model answer: *"With equal settings the library gives the same tokens as my code, so my code does what the library does; it does not show either is the best tokenizer, and nothing here says a model trained on these tokens would do better."* Check file:

```python
# check204.py - Week 20 workbook page 20.4: a SMALL diff (first 3,000 characters of the corpus, 100 merges). PRACTICE numbers.
from bpe import train, encode, make_vocab
from l4lib.corpus import TEXT
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, Regex

N = 100
small = TEXT[:3000]

def make_theirs(text, split_like_mine):
    tk = Tokenizer(models.BPE())
    if split_like_mine:
        tk.pre_tokenizer = pre_tokenizers.Sequence([
            pre_tokenizers.Split(Regex(r"\s+|\S+"), behavior="isolated"),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False)])
    else:
        tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tk.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=256 + N, min_frequency=2, show_progress=False,
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    tk.train_from_iterator([text], trainer)
    return tk

merges = train(small, N)
vocab = make_vocab(merges)
mine = encode(small, merges)
same_cut = make_theirs(small, True)
default_cut = make_theirs(small, False)
theirs = [same_cut.decoder.decode([t]).encode("utf-8") for t in same_cut.encode(small).tokens]
print("bytes:", len(small.encode("utf-8")))
print("mine:                        ", len(mine), "tokens")
print("tokenizers, same chunk rule: ", len(same_cut.encode(small).ids), "tokens")
print("tokenizers, its default cut: ", len(default_cut.encode(small).ids), "tokens")
print("pieces that differ:", sum([1 for a, b in zip([vocab[i] for i in mine], theirs) if a != b]))
print("lone spaces among mine:", sum([1 for i in mine if vocab[i] == b" "]))
```

**Part B.**

| Tokenizer | Tokens on the corpus (300 merges) |
|---|:--:|
| mine | 3,227 |
| library, same chunk rule | 3,227 (0 pieces differ) |
| library, default cut | 2,111 |

B1: `[b'the', b' ', b'baker']` against `['the', 'Ġbaker']`; `Ġ` is how the library writes a leading space. B2 model answer: *"Equal settings give equal tokens (3,227 and 3,227, 0 differ), so my code does what the library does. The default cut sticks a space to the next word, which saves about a third of the tokens (2,111). They are two tokenizers; neither is wrong. The match does not show my algorithm is best, or that a model would do better on these tokens."* Marks: three numbers (1), the 0 (1), the reason the fourth differs (1), one sentence saying the match does not prove the algorithm best (1). B3: both `True`; the starting alphabet is the 256 bytes. If a student's count with equal settings is not 3,227 while theirs is, the likely cause is a different tie-break (see page 20.7-C).

### Page 20.5

**Part A.** A2 gains: **0.143**, **0.042**, **0.049**, **0.029**. A3: gains are **not** equal; the first step is biggest and then they get smaller (the 10,000 to 30,000 step at 0.049 is a little larger than the one before it: one of the gains is not smaller than its predecessor, so the curve is *up, then flatter*, not perfectly smooth). Accept "climbs fast at first, then flattens", and a note that the steps are uneven. A4: the text had only 1,000 characters, and after 130 merges no pair was left that occurs twice: `if pair_counts[best] < 2: break`. A5: only one test file; only one set of sizes; only 200 merges; no model trained on the tokens; does not say anything about other kinds of text. Check file:

```python
# check205.py - Week 20 workbook page 20.5: bytes per token as the training text grows. SMALL version, 200 merges. PRACTICE numbers.
import textwrap, string, heapq, difflib
from bpe import train, encode

pool = ""
for module in [textwrap, string, heapq]:
    pool = pool + open(module.__file__, encoding="utf-8").read()
test = open(difflib.__file__, encoding="utf-8").read()[:10000]
print("pool:", len(pool), "characters   test:", len(test), "characters")
test_bytes = len(test.encode("utf-8"))
for n in [1000, 3000, 10000, 30000, len(pool)]:
    merges = train(pool[:n], 200)
    print(f"train on {n:6d}: merges {len(merges):3d}  bytes per token {test_bytes / len(encode(test, merges)):.3f}")
```

(The pool length depends on your Python version's `textwrap`, `string` and `heapq`; the shape should not.)

**Part B.** The class table:

| Trained on (characters) | Merges learned | Mine | `tokenizers` |
|--:|--:|:--:|:--:|
| 2,000 | 218 | 1.728 | 1.728 |
| 5,000 | 458 | 1.927 | 1.927 |
| 10,000 | 665 | 2.131 | 2.131 |
| 20,000 | 1,000 | 2.441 | 2.441 |
| 50,000 | 1,000 | 2.628 | 2.628 |
| 100,000 | 1,000 | 2.708 | 2.708 |
| 323,880 | 1,000 | 2.761 | 2.761 |

(The last row's length, and the middle rows' values, may differ with another Python version's standard library.) B1: the library is about 50 to 60 times faster at the largest size (about 12 s against 0.2 s on the reference machine); the reason is a **guess** (for example "it does not recount every pair every round"), because nobody read the library. B2: **one** line; the dashed line is under the solid one because the two columns are identical at every point. Change a marker or line style (`"o-"` and `"x--"`, or a thicker first line). B3 model answer: *"As the training text grew from 2,000 to 323,880 characters, bytes per token on text it had never seen climbed from 1.73 to 2.76; it climbed quickly at first and flattened (2.628 to 2.761 for a six-fold increase). The plot does not say a model trained on these tokens would do better, and it is one held-out file."* Marks: climbs (1), flattens with a number (1), both lines visible (1), a limit (1). B4: repeat on another unseen file means changing `argparse` to another module in `test`.

### Page 20.6

**Part A.** Table: `Tuesday` 7/4 = **1.75** bytes per token, 4/7 = **0.57** tokens per character; `café` 5/5 = **1.00**, 5/4 = **1.25**; `日本語` 9/9 = **1.00**, 9/3 = **3.00**; `🙂🙂` 8/8 = **1.00**, 8/2 = **4.00**. A1: `🙂🙂` (an emoji, 4.00; it is not "a language"), and among the *scripts of a language* `日本語` at 3.00; 3.00 / 0.57 = about **5.3** times `Tuesday`, 4.00 / 0.57 = **7.0** times. Accept either with its factor. A2: the numbers are about **this tokenizer** (trained on an English corpus) and the 13-Hindi-characters result shows that when the tokenizer *was* shown the text the cost dropped from 37 to 3; so the sentence confuses "this vocabulary never saw it" with "the script is hard". A3: they used **characters** (3) on top; it should be **9 bytes**, giving 1.00.

**Part B.** Reference figures (300 merges, trained on the corpus):

| String | Characters | Bytes | Tokens | Bytes per token | Tokens per character |
|---|:--:|:--:|:--:|:--:|:--:|
| English sentence | 38 | 38 | 26 | 1.46 | 0.68 |
| Hindi greeting | 13 | 37 | 37 | 1.00 | 2.85 |
| three emoji | 3 | 12 | 12 | 1.00 | 4.00 |
| mixed sentence | 15 | 21 | 18 | 1.17 | 1.20 |

A student's own strings give different numbers; accept any that match their own run and use the right columns (bytes on top for bytes per token, characters on the bottom for tokens per character). B1: **37** before, **3** after (the Hindi greeting repeated 60 times was added to the training text: a contrived case). It changed because the vocabulary is whatever the tokenizer was trained on. It does not mean Hindi is "cheap to fix": it says the vocabulary was decided by whoever chose the training text. B2 must say: a tokenizer trained on **English text only** (a 6,972-character corpus), **no production tokenizer measured**, and not a statement about any product or about any language's difficulty. Model: *"Measured: my own 300-merge tokenizer, trained on the 6,972-character story corpus, spent 37 tokens on a 13-character Hindi greeting and 26 on a 38-character English sentence. Not measured: any tokenizer anyone ships, any model trained on these tokens, or how hard any language is."*

### Page 20.7

**Bug A.** Printed `English tokens 26 ... 1.46` and `Hindi tokens 37 ... 0.35`. A.1: no: every token is at least one byte, so **bytes per token cannot be below 1**; 0.35 is `13 / 37`, characters over tokens. It is **silent**: no error, and the English figure is right because for ASCII characters equal bytes. A.2: `37 / 37 = 1.00`; use `len(s.encode("utf-8"))` instead of `len(s)`.

**Bug B.** Printed `ids: [224, 164, 154]`, `all together: च`, then a traceback ending:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe0 in position 0: unexpected end of data
```

B.2: `च` is **three bytes**, so three ids (nothing merged); one byte alone is not a character and cannot be turned into text; `decode` of the whole list works because the three bytes together are a complete character. A tool that prints one token at a time must be ready for a token that is only part of a character (decode the whole list, or handle the error; we did not use `errors="replace"` this week).

**Bug C.** Printed:

```text
right: merges 300  tokens 3227  round trip True
wrong: merges 300  tokens 3230  round trip True
first six pieces, right: ['he', 'the', 'an', 'er', 'and', 'in']
first six pieces, wrong: ['he', 'the', 'an', 'er', 'and', 'in']
first merge that differs: number 10  right or  wrong th
merges that differ in total: 277
```

C.1: **3,227** and **3,230**. It is **not broken**: it is a legal tokenizer, it round-trips, and it compresses almost the same; what is false is that it is "the same tokenizer". Two people using different tie rules get different tokenizers from the same text. C.2: the first nine merges each had a **unique** best pair; merge 10 was the first with a tie (`or` and `th` both had 45), and the flipped rule chose the other pair. After that the lists drift apart (277 of 300 merges differ). C.3: the diff against the library with equal settings: for the right tokenizer it printed 3,227 and **0** differing pieces, so the flipped one (3,230 tokens) would **not** match; the token count of 3,230 against 3,227 is a difference to investigate. The round trip would have said nothing. C.4: *"so that two people, or two programs, get the same tokenizer from the same text; any rule works, but there must be one, written down."*

### Page 20.8 and Self-Check

The Bug Log has no single right answer. The blanks: *when a tokenizer passes every round trip I also **count** the tokens and **diff** against a known good one*; *I check whether I divided by **characters** or by **bytes***. Self-Check model answers: (1) 556 for 300 merges (256 + 300); asked for 1,000 on the corpus, training stopped at 400 merges, so **656**; (2) start from the 256 bytes, find the commonest adjacent pair, glue it into a new piece with the next free number, and **recount** with the new piece in place, repeat; (3) count the tokens, and diff against a known good tokenizer; the do-nothing (zero-merge) tokenizer passes every round trip and fails both; (4) the library's default cut sticks a space to the next word; only with the same chunk rule (`\s+|\S+`) do both cut the same chunks; (5) a tokenizer trained on English only, 6,972 characters, spent 37 tokens on 13 characters of Hindi; it does not show that Hindi is hard, or anything about any shipped tokenizer; (6) any of: nobody trained a model on these tokens; one corpus and one held-out file; no other vocabulary size or chunk rule tried; no production tokenizer measured.

---

## 🔮 Next Week Preview

**Week 21 — Pretraining and the Scaling Arithmetic.** The model is trained on much more text with much more compute, and the first thing to count is **tokens**: how many tokens did the model see? Keep your `bpe.py`, your 556 and your 3,227, and the habit from this week: *check two different properties*, because a test that passes does not tell you the thing you did not test.
