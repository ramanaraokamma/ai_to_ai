# Week 31 — Words Into Columns

[⬅ Week 30](week-30.md) · [Course Home](../README.md) · [Week 32 ➡](week-32.md) · [Student Guide](../student-guide/week-31.md) · [Workbook](../workbook/week-31.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — the first week of text, and the week a sentence becomes a row |
| **Big idea** | A model only eats numbers, so a review becomes a row of **word counts**. And the moment you do that, **word order is gone** — `"the dog bit the man"` and `"the man bit the dog"` come out as the identical row. |
| **New vocabulary** | token · tokenization · normalization · stopword · bag-of-words · document-term matrix · sparse matrix |
| **New maths** | **None.** This week is counting and checking. It practises Weeks 1, 3 and 4 — a table of numbers, a fitted transformer, and a decision you have to justify. |
| **New syntax** | `re.findall(r"\b\w\w+\b", text)` · `text.lower()` · `CountVectorizer()` · `vec.get_feature_names_out()` |
| **Dataset** | **Four reviews written on the whiteboard**, then a **60-review corpus the student typed themselves.** Nothing downloads. No internet needed. Every character of data in this week was typed by a human. |
| **Materials** | The printed workbook (all of it; the numbered pages 31.4–31.7 are the marked homework) · **a big wall sheet headed THE VOCABULARY, with 8 blank columns ruled on it** · squared paper (the 4×8 grid gets drawn by hand) · two colours of pen · the Bug Log · a printed copy of Figure 31.2 for the activity |
| **Tech needed** | Laptop with Python 3, numpy, pandas, scikit-learn. **No new installs. No torch this week.** |
| **Prep time** | 25 minutes the night before · 5 minutes on the day |
| **Expected runtime of the code** | `bag.py` runs in **about 1 second**. There is no training in this lesson at all. **The slow part of this week is the human being, counting 32 cells by hand, and that is deliberate.** |

> **⚠️ Watch out:** the temptation this week is to skip the hand-built grid because `CountVectorizer` does it in one line. **Do not skip it.** The whole of Weeks 32 and 33 rests on the student believing, from having checked it themselves, that the library is doing exactly the counting they did on paper. Thirty-two cells takes eight minutes and buys the rest of the term.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Tokenize and normalize a piece of text** by hand and with `re.findall(r"\b\w\w+\b", text.lower())`, and **list every place the two disagree** — including the three real ones in `"The pizza was GREAT!!  But the service wasn't."`
2. **Build a 4×8 document-term matrix by hand** for four short reviews and **verify every one of the 32 cells** against `CountVectorizer`.
3. **Demonstrate that `"the dog bit the man"` and `"the man bit the dog"` produce identical rows**, and say in one sentence what that costs.
4. **Justify one normalization choice against a concrete case where it would be wrong** — starting with dropping the word `not`, and using a sentence pair they wrote themselves as the proof.

Observable evidence: the notebook page with all 32 cells filled in in pen and ticked against the printout; the printed line `are the two rows identical? True`; a written sentence pair where a normalization choice destroys the difference between them; and the corpus numbers `92` words, `5,520` cells, `363` stored.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not whole files** — each one carries on from the one above. **The complete runnable file is in the Prep Checklist and the Answer Key.**

**There is no new mathematics this week, and you should feel relieved about that.** After eighteen weeks of slopes, matrices and backpropagation, this week is counting. The difficulty has moved somewhere else: this week is about a **decision**, and about being honest with a fourteen-year-old that the decision throws information away on purpose.

### 1. Why text is a problem at all

Every model in this course so far has been handed numbers. The pizza-delivery table was numbers. `load_digits()` was numbers — 64 pixel brightnesses per picture. `load_wine()` was thirteen chemical measurements. Even the "categories" in Week 4 became numbers the moment `OneHotEncoder` touched them.

Text is not numbers. `"the pizza was cold"` is a string of characters, and **there is no obvious column to put it in.** You cannot average it, you cannot scale it, you cannot subtract one review from another.

So somebody had to invent a way to turn a sentence into a row of a spreadsheet, and the first answer — from the 1950s, still in daily use — is almost rude in its simplicity:

> **Count the words.**

Forget grammar. Forget word order. Forget everything an English teacher ever told you about how a sentence works. Just count. `"the pizza was cold"` becomes a row that says `the=1, pizza=1, was=1, cold=1`, and every other word in the English language `=0`.

**This should not work.** It cannot tell `"the dog bit the man"` from `"the man bit the dog"`. And yet it ran the world's spam filters and search engines for thirty years, and on a small problem it is still a sensible first attempt today: it trains in a second, needs no internet, and can be read word by word. **Both of those sentences are true, and holding both at once is the intellectual content of this week.**

### 2. Tokenization: chopping the string into pieces

> **Token** — one unit of text. Usually a word; sometimes a punctuation mark or a piece of a word.
>
> **Tokenization** — splitting a string into tokens.

The obvious first move is Python's `.split()`, which cuts at every space. Here is what that actually gives you, run for real:

```text
raw text          : The pizza was GREAT!!  But the service wasn't.
raw.split()   ( 8): ['The', 'pizza', 'was', 'GREAT!!', 'But', 'the', 'service', "wasn't."]
```

**Look at that list as a computer would.** `'GREAT!!'` is a different token from `'GREAT!'`, which is different from `'great'`, which is different from `'Great'`. **Four spellings of one word, four separate columns, each with a quarter of the evidence.** And `'the'` appears as both `'The'` and `'the'`, so your commonest word has been split in two.

That is why you **normalize**.

> **Normalization** — tidying tokens so that different spellings of the same thing become the same token.

The cheapest normalization is `text.lower()` — one method call, every capital letter becomes lower case:

```text
lower + split ( 8): ['the', 'pizza', 'was', 'great!!', 'but', 'the', 'service', "wasn't."]
```

`The` and `the` are now the same token. But `great!!` still carries its exclamation marks. So the second move is to stop cutting at spaces and instead **pick out the runs of letters and digits**, which is what the regular expression does:

```text
lower + regex ( 8): ['the', 'pizza', 'was', 'great', 'but', 'the', 'service', 'wasn']
```

Clean. **And look at the last token.** `wasn't` has become `wasn`. The `'` broke the word in two and the leftover `t` was thrown away because it is only one letter long.

![One sentence, four ways to chop it up](../figures/fig-w31-1-sentence-chopped-into-tokens.svg)
*Figure 31.1 — One sentence, four ways to chop it up. 8 tokens, then 8, then 8, then 4 once the stopwords go. And `wasn` is not a word at all.*

### 3. The regular expression, explained character by character

This is the single line of this week that will scare a teacher, so here it is taken apart. **You do not need to know regular expressions to teach this. You need to know what these five pieces do.**

```python
re.findall(r"\b\w\w+\b", text)
```

| Piece | What it means, in plain English |
|---|---|
| `re` | a toolbox that comes with Python for finding patterns in text. Nothing to install. |
| `findall` | "give me a list of every place this pattern matches" |
| `r"..."` | **a raw string.** The `r` tells Python "do not interpret the backslashes, hand them to the pattern as they are." |
| `\w` | one **w**ord character: a letter, a digit, or an underscore. **Not** a space and **not** punctuation. |
| `\w\w+` | one word character, then **one or more** more. So: **two characters or longer.** |
| `\b` | a **b**oundary — the edge of a word. It stops the pattern grabbing half of a longer word. |

Read the whole thing out loud as: **"find me every run of two or more letters or digits."**

> **⚠️ Watch out:** `\w\w+` means **two or more**, so **every single-letter token is silently thrown away.** In the corpus your student types this week, `i` and `a` both vanish. `print("is 'i' in the vocabulary?", "i" in set(vocab))` prints `False`. This is not a bug in scikit-learn; it is `CountVectorizer`'s documented default, and it is usually harmless and occasionally catastrophic. **Say it out loud in class, because a student who discovers it alone in the homework will think they have broken something.**

> **🐞 If you see this error:** nothing at all, and an empty list. If you forget the `r` — `re.findall("\b\w\w+\b", text)` — Python reads `\b` as the **backspace character**, the pattern looks for a literal backspace, and you get `[]` back with no error, no warning, and no hint. **This is deliberate mistake number two in the live-code segment, and it is the highest-value sixty seconds of the lesson.**

### 4. Normalization is a set of decisions, and every one can be wrong

This is the part of the week to spend your prep time on, because **objective 4 is the one that separates a level-3 student from a level-5 one.**

| Normalization | What it does | When it is right | When it is **wrong** |
|---|---|---|---|
| **Lowercasing** | `Great → great` | almost always, for topic or sentiment | `US` the country versus `us` the pronoun; `Apple` the company versus `apple` the fruit; ALL-CAPS SHOUTING is real evidence in abuse detection |
| **Strip punctuation** | `great!! → great` | most classification jobs | `!!!` and `?!` carry feeling; `$4.99` becomes `4` and `99`; `:-(` disappears completely, and on a sentiment job that was the clearest signal in the sentence |
| **Remove stopwords** | drop `the, is, a, of` | topic classification, search | **negation.** Dropping `not` is a disaster. Also authorship: the little words *are* the fingerprint. |
| **Stemming** | `running, runs → run` | when you have very little data | a keen stemmer turns `university` and `universe` both into `univers`, and `news` into `new`. (Mapping `ran → run` or `better → good` needs a *lemmatizer*, which uses a dictionary and is a different, heavier tool.) |

> **Stopword** — an extremely common word (`the`, `is`, `and`) that carries almost no information about the topic on its own.

**The killer case, and the one to put on the board.** Take a stopword list that contains `the`, `was` and `not` — a completely ordinary list; `not` is on most of them. Now normalize these two reviews:

```text
'the pizza was not cold' -> ['pizza', 'cold']
'the pizza was cold'     -> ['pizza', 'cold']
```

**Identical.** A happy customer and an unhappy customer, and after your tidying they are the same row: `( pizza 1, cold 1 )`.

![Drop the word not and the meaning flips](../figures/fig-w31-5-dropping-not-flips-the-meaning.svg)
*Figure 31.5 — Drop the word `not` and the meaning flips. Two opposite reviews, one identical row, because the stopword list deleted the only word that carried the meaning.*

🍕 **The analogy that works with fourteen-year-olds:** normalizing is **tidying a room before you count what is in it.** Putting all the pens in one drawer (lowercasing) genuinely makes counting easier. Throwing out everything small (stopword removal) makes it easier still — right up to the moment you realise you have thrown out the house keys. **`not` is a house key.**

### 5. The document-term matrix, and how to count it by hand

> **Bag-of-words** — representing a document as a list of word counts, ignoring order entirely. A *bag* because you tipped all the words in and shook it.
>
> **Document-term matrix** — a table with **one row per document** and **one column per vocabulary word**. The cell at row *i*, column *j* is how many times word *j* appears in document *i*.

The four whiteboard reviews for this week:

```text
d1: "The pizza was great!"
d2: "The pizza was cold."
d3: "Great pizza, great service."
d4: "Cold service and cold food."
```

**Step one: the vocabulary.** Tokenize every review, gather every different token, sort them alphabetically. That gives **eight** terms:

```text
and, cold, food, great, pizza, service, the, was
```

**Step two: fill in the grid**, one cell at a time. Eight columns, four rows, 32 cells:

| | and | cold | food | great | pizza | service | the | was |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **d1** | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 |
| **d2** | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| **d3** | 0 | 0 | 0 | **2** | 1 | 1 | 0 | 0 |
| **d4** | 1 | **2** | 1 | 0 | 0 | 1 | 0 | 0 |

**The two cells that are not 1 or 0 are the two cells to point at.** d3 is `"Great pizza, great service."` and the word `great` is in it **twice**, so that cell is 2. d4 has `cold` twice. **Everything else is a 1 where the word is present and a 0 where it is not**, which is what makes this grid checkable by a class in eight minutes.

![Four reviews become one grid of counts](../figures/fig-w31-2-four-documents-into-a-count-matrix.svg)
*Figure 31.2 — Four reviews become one grid of counts. 4 documents × 8 words = 32 cells, and every one is a count you can check by eye.*

**And that grid is now an ordinary numeric feature matrix.** It has a shape — `(4, 8)` — exactly like Week 1's `X`. `LogisticRegression` will eat it without complaint. That is the whole trick, and it is why this week exists.

### 6. Sparsity: the property that makes text different

Count the zeros in that table. **There are 17 of them, out of 32 cells.** More than half the grid is empty, on a four-document corpus with an eight-word vocabulary.

Now scale up. Your student's own 60-review corpus, run for real:

```text
documents        : 60
vocabulary size  : 92
cells in the grid: 5520
non-zero cells   : 363
zero cells       : 5157 = 93.4% of the grid
```

**Ninety-three per cent empty.** And it gets worse, not better, as you add documents: a real corpus of 20,000 news articles with a 50,000-word vocabulary has a billion cells of which perhaps one in a thousand holds a number.

> **Sparse matrix** — a grid stored as a list of *(row, column, value)* triples for the non-zero cells only. Scikit-learn's vectorizers hand you one of these by default, which is why `print(X)` shows coordinates instead of a table.

This is what `print(counts)` actually shows — the first four of the fifteen things it keeps:

```text
  (0, 6)	1
  (0, 4)	1
  (0, 7)	1
  (0, 3)	1
```

Read `(0, 6) 1` as: **"row 0, column 6, holds 1."** Row 0 is d1, column 6 is `the`, and d1 contains `the` once. **Nowhere in that list is there an entry saying "row 0 column 0 holds 0", because storing a zero would be storing nothing.**

![A sparse matrix stores only the numbers that are there](../figures/fig-w31-4-sparse-matrix-only-the-nonzeros-stored.svg)
*Figure 31.4 — A sparse matrix stores only the numbers that are there. 32 − 15 = 17 empty cells on the toy corpus; 5,520 cells and 363 stored on the student's own 60.*

🍕 **The analogy:** a bag-of-words row is **a supermarket receipt with a line for every product the shop sells.** Yours says `milk: 2, bread: 1`, and forty thousand other lines all say zero. **Obviously you do not print those.** You print the two lines that matter. That is a sparse matrix.

**The one practical consequence for the lesson:** to see a grid you must call `.toarray()`, and `pd.DataFrame(counts, ...)` without it produces a confusing `ValueError`. That error is in the Debugging Clinic and you will meet it in class.

### 7. What bag-of-words throws away, listed honestly

Keep this list. Week 32 tries to fix the first problem with it and fails; Week 33 measures exactly how much it costs.

| Thrown away | Example | Why the row cannot tell |
|---|---|---|
| **Word order** | `"the dog bit the man"` vs `"the man bit the dog"` | identical rows, cell for cell |
| **Negation scope** | `"good"` vs `"not good"` | both rows contain `good` |
| **Which word modifies which** | `"cheap phone, great camera"` vs `"great phone, cheap camera"` | identical rows |
| **Grammar entirely** | — | there is no place in a row of counts to put it |

The first row of that table is the one you demonstrate live, because it takes eleven seconds and it is unarguable:

```text
vocabulary: ['bit' 'dog' 'man' 'the']
             bit  dog  man  the
dog bit man    1    1    1    2
man bit dog    1    1    1    2
are the two rows identical? True
```

![Two different sentences, one identical row](../figures/fig-w31-3-same-row-two-different-sentences.svg)
*Figure 31.3 — Two different sentences, one identical row. Subtract them and every column gives 0, so nothing anywhere in the row records the order.*

**Say the honest thing about this out loud, in these words or close to them:** *"This is not a bug. Nobody is going to fix it in a later version. It is the price of the method, and you pay it every single time you use it. The skill is knowing what you paid."*

### 8. Every new line of this week's code, explained to somebody who has never programmed

Four new things.

**New thing 1 — making text lower case.**

```python
text.lower()
```

`text` is a string — a run of characters. `.lower()` is a **method**: a small job the string knows how to do to itself. It hands back a **new** string with every capital letter turned into a small one. It does not change the original. `"GREAT".lower()` gives `"great"`.

**New thing 2 — pulling the words out with a pattern.**

```python
import re
re.findall(r"\b\w\w+\b", text.lower())
```

Taken apart in §3 above. In one sentence: **find me every run of two or more letters or digits, in the lower-cased text, and give me them as a list.** The `r` before the quote is not decoration — leave it off and you get an empty list with no error.

**New thing 3 — the counter.**

```python
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
counts = cv.fit_transform(docs)
```

`CountVectorizer` is **a transformer, exactly like Week 4's `StandardScaler`** — and saying so out loud is worth thirty seconds, because it means the student already knows how it behaves.

- `.fit(docs)` **reads** the documents and decides the vocabulary. That is the learned thing.
- `.transform(docs)` **turns documents into rows** using the vocabulary it already has.
- `.fit_transform(docs)` does both, and **you only ever call it on your training documents.**

**Its defaults are decisions somebody else made.** `lowercase=True` is on, and `token_pattern` is the very regex from §3. So `CountVectorizer()` with no arguments has already lower-cased your text and thrown away every single-letter word, before you did anything.

> **⚠️ Watch out:** `fit_transform` wants **an iterable of documents**, not one document. Hand it a bare string and every *character* looks like a document to it — except scikit-learn now catches that and says `ValueError: Iterable over raw text documents expected, string object received.` That is the first deliberate mistake in the live-code segment.

**New thing 4 — asking what the columns are called.**

```python
cv.get_feature_names_out()
```

Hands back the vocabulary, in column order, as an array of strings. **This is the only way to know what column 6 means**, and every single time you put a count matrix into a DataFrame you will use it for the column names. Call it before `.fit()` and you get `NotFittedError: Vocabulary not fitted or provided`, which is a perfectly clear message and worth reading aloud.

### 9. The three misconceptions you will actually meet

**Misconception 1 — "so the computer understands the review now."**
It does not. It has a row of counts. **Cure:** the order demo. `"the dog bit the man"` and `"the man bit the dog"`, identical rows, eleven seconds. *"Does something that cannot tell those apart understand English?"*

**Misconception 2 — "removing stopwords is just tidying up, so it is always good."**
**Cure:** `the pizza was not cold` and `the pizza was cold`, both reduced to `( pizza 1, cold 1 )`. Ask what the shop should do about each of those two customers, and then point out that the model cannot tell which is which.

**Misconception 3 — "a zero in the grid means the word is not in the language."**
It means the word is not in **this document**, but it *is* in the vocabulary, which came from the whole corpus. **Cure:** point at d1's `cold` cell. `cold` has a column because d2 and d4 used it. d1's cell is 0 because d1 did not. **The column exists; the count is zero.** This matters enormously in Week 33, where a word with no column at all is silently dropped and a word with a column and a zero is not the same thing.

### 10. How deep to go, and where to stop

**Go this far:** the four tokenizers and the three places they disagree; the regex read out in English; lowercasing; stopwords and the `not` case; the vocabulary; the 4×8 grid built by hand and checked cell by cell; sparsity with real numbers; the order demo.

**Stop before:**

| Do not teach today | Where it lives |
|---|---|
| **TF-IDF, idf, weighting** | **Week 32.** If a student says "but `the` is in everything and tells you nothing" — and somebody will — write their sentence on the wall sheet with their name on it and say *"that is next week's entire lesson, and you just wrote the title."* |
| **Cosine similarity** | **Week 32.** Today two rows are compared by looking at them. |
| **Training a classifier on text** | **Week 33.** Today nothing is fitted except the vocabulary. |
| **n-grams / bigrams** | **Week 33.** If asked how you would fix word order, say *"there is a patch, we measure it in two weeks, and it works less well than you would hope."* Do not demonstrate it today. |
| **Stemming and lemmatizing** | Not in this level. They need a library we do not have offline. One sentence if asked: *"there are tools that cut `running` down to `run`; they help when you have very little data and they make mistakes like turning `universe` into `univers`."* |
| **Regular expressions as a subject** | Not in this level. **One pattern, read out in English, and that is the lot.** A student who wants more should be pointed at it as a hobby, not a syllabus. |
| **Word embeddings** | **Week 33's last ten minutes, and then Level 4.** |

The line to hold in your head all lesson: **today the student turns words into columns, checks the library's arithmetic by hand, and finds out what the method costs.**

---

### 11. 🧭 The Growing Map — the same box, and the "words" half of it finally arrives

The student guide carries a figure called **Where This Fits**: the same picture every week with one more
piece filled in. The tile does not move this week, but the second word on it comes into play for the
first time.

![The Level 3 pipeline in Week 31: still the no labels and words tile, now words turned into columns](../figures/fig-w31-0-where-this-fits.svg)

*Figure 31.0 — Week 31's version. Fourth week inside the gold `no labels · words` tile. The ↻ on stage
three is black, as it has been since Week 12.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Ask "which box did we do today?" and then "which word on it?"** Same gold tile — but point at the
   word **words**, which has been sitting unused on that map since Week 1. *"Weeks 28 to 30 were the no
   labels half. From today it is the words half, and Weeks 32 and 33 finish it."*
2. **Anchor it on the thirty-two cells and on `True`.** Hold up the completed 32-cell notebook page. *"This box turned
   four sentences into thirty-two numbers, and every one of them was checked against the library by
   hand."* Then the printed line `are the two rows identical? True` for `"the dog bit the man"` and
   `"the man bit the dog"`. **The cost is the lesson, not the method** — ask them to say in one sentence
   what the box threw away, and insist on the word *order*.
3. **Point at stage one, twice.** Once for `Pipeline`: the vectorizer is a **fitted transformer**, so the
   vocabulary is learned on the training reviews only, and a vocabulary built on everything is leakage
   wearing a friendly face. And once for the decisions: dropping `not` is a preprocessing choice, exactly
   the kind Week 1 made them write down in pen. *"Which box does 'we decided to lowercase everything'
   belong to?"* — the answer is stage one, not stage five.

> **🧑‍🏫 Why this is worth two minutes.** After eighteen weeks of gradients and tensors, a lesson spent
> counting words by hand can feel like a step backwards, and the map is the cheapest correction: **this
> is the fourth week of the final stage.** Nothing has regressed; the data changed shape, and the
> pipeline did not have to. That is the actual point of having had a fixed picture since Week 1.

**One thing to notice, so you can answer if asked.** No thread for "language" ever appears on that
strip, and a sharp student may ask why text does not get its own. It is the right question and the answer
is the best thing you can tell them this week: **text is not a new kind of problem, it is a new
representation of an old one.** `92` words, `5,520` cells, `363` stored — that is a table, and every box
to the left of the gold one already knows what to do with a table.

---

## 🧰 Prep Checklist

Use this section to get the room, the files and the fallback ready before the lesson.

### 25 minutes the night before

- [ ] **Type and run `reviews.py` first.** It is just data, but everything else imports it, and the student will have typed their own version. **Twelve minutes to type, and it is the student's homework from last week's preview, so check yours matches theirs in shape: two lists, `POS` and `NEG`, thirty strings each.**

```python
"""reviews.py - the corpus, typed by hand. No downloads, no data files."""

POS = [
    "the pizza arrived hot and the base was perfect",
    "quick delivery and a friendly driver",
    "delicious food and a generous portion",
    "the salad was fresh and crisp",
    "great value and a lovely warm welcome",
    "excellent service from a polite driver",
    "the chips were hot and crisp",
    "a tasty curry and a generous helping of rice",
    "fresh bread and a delicious dip",
    "the delivery was quick and the food was hot",
    "lovely staff and a perfect order",
    "friendly, polite and on time",
    "the sauce was tasty and the cheese was lovely",
    "generous portions and excellent prices",
    "the burger was hot and the salad was fresh",
    "delicious dessert and a friendly note in the bag",
    "a perfect meal and a quick refund on the drink",
    "great chips, crisp and properly salted",
    "the coffee was hot and the cake was fresh",
    "polite driver and a warm, tasty pizza",
    "excellent noodles with fresh vegetables",
    "a lovely evening and a delicious meal",
    "quick, friendly and generous",
    "the fish was fresh and the batter was crisp",
    "perfect timing and a hot bag",
    "tasty wrap, generous salad and a great price",
    "the naan was warm and lovely",
    "friendly manager and a quick, fair refund",
    "a delicious pizza, hot and perfect",
    "excellent, fresh food and a polite driver",
]

NEG = [
    "the pizza arrived cold and the base was soggy",
    "slow delivery and a rude driver",
    "awful food and a mean portion",
    "the salad was stale and limp",
    "poor value and a cold, rude welcome",
    "terrible service from a rude driver",
    "the chips were cold and soggy",
    "an awful curry and a mean helping of rice",
    "stale bread and a greasy dip",
    "the delivery was slow and the food was cold",
    "rude staff and a wrong order",
    "rude, slow and very late",
    "the sauce was bitter and the cheese was greasy",
    "mean portions and terrible prices",
    "the burger was cold and the salad was limp",
    "awful dessert and a rude note in the bag",
    "a wrong meal and a slow refund on the drink",
    "soggy chips, cold and completely unsalted",
    "the coffee was cold and the cake was stale",
    "rude driver and a cold, greasy pizza",
    "terrible noodles with limp vegetables",
    "i would not order from here again",
    "slow, rude and mean",
    "the fish was stale and the batter was soggy",
    "late again and a cold bag",
    "greasy wrap, limp salad and a terrible price",
    "the naan was cold and stale",
    "rude manager and a slow, unfair refund",
    "an awful pizza, cold and soggy",
    "terrible, stale food and a rude driver",
]

CORPUS_60 = POS + NEG
LABELS_60 = [1] * 30 + [0] * 30
```

- [ ] **Type and run `bag.py` yourself, in the same folder.** The whole file:

```python
"""bag.py - Week 31: a sentence becomes a row of numbers."""
import re

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from reviews import CORPUS_60

# ---------- 1. four ways to chop up one sentence ----------
raw = "The pizza was GREAT!!  But the service wasn't."

print("--- one sentence, four tokenizers ---")
print("raw text          :", raw)
naive = raw.split()
print("raw.split()   (%2d):" % len(naive), naive)
lowered = raw.lower().split()
print("lower + split (%2d):" % len(lowered), lowered)
regex = re.findall(r"\b\w\w+\b", raw.lower())
print("lower + regex (%2d):" % len(regex), regex)
STOP = {"the", "but", "was", "and", "of", "to", "is"}
kept = [t for t in regex if t not in STOP]
print("minus stopwords(%2d):" % len(kept), kept)

# ---------- 2. the four whiteboard reviews ----------
docs = ["The pizza was great!",
        "The pizza was cold.",
        "Great pizza, great service.",
        "Cold service and cold food."]

cv = CountVectorizer()
counts = cv.fit_transform(docs)
terms = cv.get_feature_names_out()

print()
print("--- the document-term matrix ---")
print("vocabulary :", terms)
print("shape      :", counts.shape, "=", counts.shape[0], "documents x",
      counts.shape[1], "words")
print("matrix type:", type(counts).__name__)
print("stored     :", counts.nnz, "non-zero cells of",
      counts.shape[0] * counts.shape[1])
print()
print(pd.DataFrame(counts.toarray(), index=["d1", "d2", "d3", "d4"],
                   columns=terms))

# ---------- 3. what a sparse matrix actually holds ----------
print()
print("--- the first four things the sparse matrix stores ---")
for line in str(counts).splitlines()[:4]:
    print(line)
print("   ... 11 more, and NOT ONE of the 17 zeros")

# ---------- 4. the order demo ----------
pair = ["the dog bit the man", "the man bit the dog"]
cv2 = CountVectorizer()
P = cv2.fit_transform(pair).toarray()
print()
print("--- the order demo ---")
print("vocabulary:", cv2.get_feature_names_out())
print(pd.DataFrame(P, index=["dog bit man", "man bit dog"],
                   columns=cv2.get_feature_names_out()))
print("are the two rows identical?", bool((P[0] == P[1]).all()))

# ---------- 5. the sixty reviews you typed ----------
cv3 = CountVectorizer()
X = cv3.fit_transform(CORPUS_60)
vocab = cv3.get_feature_names_out()
cells = X.shape[0] * X.shape[1]
print()
print("--- your 60-review corpus ---")
print("documents        :", X.shape[0])
print("vocabulary size  :", X.shape[1])
print("cells in the grid:", cells)
print("non-zero cells   :", X.nnz)
print("zero cells       :", cells - X.nnz,
      "= %.1f%% of the grid" % (100 * (cells - X.nnz) / cells))

total = np.asarray(X.sum(axis=0)).ravel()
order = np.argsort(total)[::-1]
print()
print("the ten commonest words in the corpus:")
for i in order[:10]:
    print("   %-10s %d" % (vocab[i], total[i]))

print()
print("is 'i' in the vocabulary?  ", "i" in set(vocab))
print("is 'a' in the vocabulary?  ", "a" in set(vocab))
print("words of one letter kept:  ",
      sum(1 for w in vocab if len(w) == 1))
```

Run `python3 bag.py`. You must see **exactly** this:

```text
--- one sentence, four tokenizers ---
raw text          : The pizza was GREAT!!  But the service wasn't.
raw.split()   ( 8): ['The', 'pizza', 'was', 'GREAT!!', 'But', 'the', 'service', "wasn't."]
lower + split ( 8): ['the', 'pizza', 'was', 'great!!', 'but', 'the', 'service', "wasn't."]
lower + regex ( 8): ['the', 'pizza', 'was', 'great', 'but', 'the', 'service', 'wasn']
minus stopwords( 4): ['pizza', 'great', 'service', 'wasn']

--- the document-term matrix ---
vocabulary : ['and' 'cold' 'food' 'great' 'pizza' 'service' 'the' 'was']
shape      : (4, 8) = 4 documents x 8 words
matrix type: csr_matrix
stored     : 15 non-zero cells of 32

    and  cold  food  great  pizza  service  the  was
d1    0     0     0      1      1        0    1    1
d2    0     1     0      0      1        0    1    1
d3    0     0     0      2      1        1    0    0
d4    1     2     1      0      0        1    0    0

--- the first four things the sparse matrix stores ---
  (0, 6)	1
  (0, 4)	1
  (0, 7)	1
  (0, 3)	1
   ... 11 more, and NOT ONE of the 17 zeros

--- the order demo ---
vocabulary: ['bit' 'dog' 'man' 'the']
             bit  dog  man  the
dog bit man    1    1    1    2
man bit dog    1    1    1    2
are the two rows identical? True

--- your 60-review corpus ---
documents        : 60
vocabulary size  : 92
cells in the grid: 5520
non-zero cells   : 363
zero cells       : 5157 = 93.4% of the grid

the ten commonest words in the corpus:
   and        55
   the        34
   was        26
   cold       11
   rude       10
   driver     8
   fresh      7
   hot        7
   pizza      6
   food       6

is 'i' in the vocabulary?   False
is 'a' in the vocabulary?   False
words of one letter kept:   0
```

**Expected runtime: about 1 second.** There is no training in this lesson. If it takes longer than five seconds, something is wrong with the install, not with the file.

- [ ] **Break the `r` on purpose, once.** Change `re.findall(r"\b\w\w+\b", ...)` to `re.findall("\b\w\w+\b", ...)` and run it. You get:

```text
lower + regex ( 0): []
```

**No error. No warning. An empty list.** Sit with that for ten seconds, because it is the exact feeling your students will have in the homework. This is deliberate mistake two.

- [ ] **Count the 32 cells yourself, on paper, before class.** Genuinely do it. It takes four minutes and it tells you which cell your class will argue about. (It is d3's `great`, and the argument will be whether a repeated word counts twice. It does.)
- [ ] **Print the whole workbook** (Warm-Up through Self-Check; the numbered Build It pages are 31.4–31.7).
- [ ] **Rule up the wall sheet headed THE VOCABULARY** — eight blank columns, four blank rows, with `d1 d2 d3 d4` down the side. It gets filled in live in the activity and it stays up for Weeks 32 and 33.
- [ ] **Have the student's own 60 reviews on disk and check they run.** They typed them for homework. **If they have not, the last five minutes of the lesson has nothing to bite on** — so check tonight, not at minute 60.

### 5 minutes on the day

- [ ] Editor open, terminal ready, `reviews.py` and `bag.py` in the same folder.
- [ ] THE VOCABULARY wall sheet up, blank.
- [ ] Squared paper or a notebook page out for the by-hand tokenizing (workbook P2 and A5 revisit it afterwards). **The by-hand tokenizing done in pen before any code runs.**
- [ ] Two colours of pen per student — one for their hand-built grid, one for ticking it against the printout. **The ticks are the evidence for objective 2 and they must be visibly a second pass.**
- [ ] Bug Log out.
- [ ] Squared paper for the 4×8 grid.

### Fallback if the laptops fail

**This is the most paper-friendly week of the entire term, and you lose almost nothing.**

1. **Objectives 1, 2 and 4 are all pencil work.** Tokenizing by hand, building the 32-cell grid, and arguing about `not` need no electricity at all.
2. **Objective 3, the order demo, works on the board in ninety seconds.** Write the two sentences, write the vocabulary `bit dog man the`, and have two students each count one sentence. **They will produce `1 1 1 2` twice and the room will go quiet. It is better on the board than on a screen.**
3. **The only genuine casualty is the *verification* half of objective 2** — checking your grid against `CountVectorizer`'s. Print this file's output and have them check against the printout instead. **Say what you are doing:** *"today you are checking against my printout; I am asking you to trust me for one week, which is the last time this year I will ask that."*
4. **The corpus numbers** — 92 words, 5,520 cells, 93.4% empty — can be read off this file and put on the wall sheet. The arithmetic `60 × 92 = 5,520` is worth doing on paper anyway.

| If this fails | Do this instead |
|---|---|
| `ModuleNotFoundError: No module named 'reviews'` | `reviews.py` is in a different folder from `bag.py`. **Same folder, and run `python3` from that folder.** |
| `lower + regex ( 0): []` | The `r` is missing before the pattern. **This is the whole point of deliberate mistake two — if it happens by accident, celebrate it.** |
| The student's 60 reviews were never typed | Use this file's corpus for the last five minutes and **set the typing as part of the homework.** Weeks 32 and 33 both need it, so it cannot be skipped, only moved. |
| A student's vocabulary size is not 92 | Theirs is different from mine and that is correct — they typed different reviews. **Ask for the number, not for 92.** What must be true is `60 × their vocabulary size = their cell count`. |
| The class argues about whether `great` in d3 is 1 or 2 | **Let it run for ninety seconds.** Then read the definition off the board: *how many times the word appears*. Twice. **That argument is the single best thing that will happen today.** |
| Somebody asks about `the` being useless | Write their sentence on the wall sheet with their name on it. **It is next week's title.** |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — What Number Is "Cold"? | 7 | 7 | A model eats numbers; here is a sentence; the count trick |
| 🧠 Concept — Chop, Tidy, Count | 18 | 25 | Tokens, the regex in English, normalization as a decision, the grid |
| 💻 Live-Code Together — `bag.py` | 18 | 43 | Four tokenizers, the grid, sparsity. **Two deliberate mistakes.** |
| 🎲 Their Turn — The 32 Cells, and the Order Demo | 20 | 63 | Hand-build, check every cell, then the dog and the man |
| 🔑 Wrap & Assign | 7 | 70 | The three losses, 93.4%, homework |

---

### 🪝 Hook — What Number Is "Cold"? (7 minutes)

**Do this:** Nothing on the screen. Write one review on the board, big:

```text
the pizza was cold
```

**Say this:**

> "Thirty weeks ago you started this course with a table. Rows were pizza deliveries, columns were numbers — distance, minutes, how many items. Everything since then has eaten numbers. The scaler ate numbers. The decision tree ate numbers. Last term's network ate 64 pixel brightnesses. Last week `KMeans` ate thirteen chemical measurements of a wine.
>
> Here is a review. **I want to feed it to a model. What number is it?**"

**Ask this:** "What number is `cold`?"

*Let this be uncomfortable for a few seconds. You will get: "1 for bad?" "minus 5?" "you can't."*

> "Every one of those answers is interesting and the last one is nearly right. **You cannot.** There is no number that `cold` *is*. So somebody had to invent one, and the answer they invented in the 1950s is so simple it is almost insulting."

**Do this:** Write under the review:

```text
the = 1     pizza = 1     was = 1     cold = 1
... and every other word in English = 0
```

**Say this:**

> "**Count the words.** That is it. That is the whole idea. Forget grammar. Forget which word came first. Forget everything your English teacher ever told you about how a sentence works. **Just count.**
>
> And now it is a row of numbers, so `LogisticRegression` will eat it, and you are away."

**Ask this:** "Give me one reason this is a terrible idea."

*Take answers. Somebody will get close to word order; somebody will say "but the word `the` is in everything".*

> "Hold both of those. You have just named the two things that go wrong, and they are the next two weeks of this course.
>
> But before we complain about it, I want you to know what it did. **This idea — counting the words — ran the world's spam filters and search engines for thirty years.** It is not a toy. On a small problem, today, with a hundred reviews and no internet, it can still be a sensible first attempt that trains in a second, needs no internet, and can be read word by word, which a system with a hundred billion numbers cannot offer.
>
> So today you build one. **By hand first, and then you check that the library agrees with you, cell by cell.** And at minute sixty I am going to show you the one sentence it cannot cope with, and it will annoy you."

---

### 🧠 Concept — Chop, Tidy, Count (18 minutes)

**Do this:** Write the raw sentence on the board, exactly as it is, punctuation and all:

```text
The pizza was GREAT!!  But the service wasn't.
```

**Say this:**

> "Before you can count words you have to decide what a word *is*, and that is not as obvious as it looks. **Chopping a string into pieces has a name: tokenization.** Each piece is a **token**."

**Do this:** Write on the board and box it:

> **Token** — one unit of text, usually a word.
> **Tokenization** — chopping a string into tokens.

**Ask this:** "Easiest possible rule. Cut at every space. How many pieces?"

*Eight.*

**Do this:** Write the eight, with their punctuation kept exactly:

```text
The | pizza | was | GREAT!! | But | the | service | wasn't.
```

**Ask this:** "Now think like a computer, which has no idea that letters have meanings. **How many different tokens for the word `the` are in that list?**"

*Two — `The` and `the`.*

> "**Two.** And to the computer they are as unrelated as `the` and `hydraulics`. So your commonest word has been split in half, and each half has half the evidence.
>
> Same problem with `GREAT!!`. That is a different token from `GREAT!`, and from `Great`, and from `great`. **Four spellings of one word, four columns, a quarter of the evidence each.** So we tidy up. That has a name too."

**Do this:** Write and box:

> **Normalization** — tidying tokens so different spellings of the same thing become the same token.

**Say this:**

> "Cheapest fix first: make everything small. In Python that is `.lower()` — one method on a string, and every capital becomes lower case."

**Do this:** Write row two under row one:

```text
the | pizza | was | great!! | but | the | service | wasn't.
```

**Ask this:** "Better. What is still wrong?"

*`great!!` still has its exclamation marks.*

> "Right. So stop cutting at spaces, and instead go and **fetch the runs of letters**. That is the one line of pattern-matching you learn this year, and I am going to read it to you in English rather than in symbols."

**Do this:** Write the pattern on the board and then, underneath, the English. **Write both. The English is the bit they keep.**

```text
re.findall(r"\b\w\w+\b", text)
```

```text
"find me every run of TWO OR MORE letters or digits"
```

**Say this, slowly, pointing at each piece:**

> "`re` is a toolbox that comes with Python for finding patterns in text. `findall` means give me a list of every match. The `r` in front of the quote marks means *do not mess with the backslashes, hand them straight to the pattern* — and if you forget that `r`, you get an empty list and no error message at all, which I will do to you on purpose in about ten minutes.
>
> `\w` is one word character — a letter or a digit. `\w\w+` is one, and then one or more. **So: two characters or longer.** And `\b` is a word boundary, so it does not grab half of a longer word."

**Do this:** Write row three:

```text
the | pizza | was | great | but | the | service | wasn
```

**Ask this:** "Two things changed. One is good. What is the other one?"

*`wasn't` has become `wasn`.*

> "**`wasn`.** That is not a word. The apostrophe broke `wasn't` in two, and the leftover `t` was thrown away because it is only one letter long and our pattern wants two or more.
>
> **And notice what has just happened to the meaning.** `wasn't` was a negative. It was the word that made the second half of that review a complaint. It is now a nonsense token called `wasn`, and the negation is gone. **That is not a bug. That is the default behaviour of the most-used text tool in the world, and it is one reason carelessly-built sentiment models get negation wrong.**"

**Do this:** Now the decision table. Write four rows on the board with two columns headed **when it helps** and **when it hurts**:

| | helps | hurts |
|---|---|---|
| make it lower case | `The`/`the` become one | `US` the country / `us` the pronoun |
| throw away punctuation | `great!!` → `great` | `$4.99` → `4` and `99`; `:-(` vanishes |
| drop the common words | fewer useless columns | **`not`** |

**Ask this:** "The last one. I have a list of common words to throw away — `the`, `is`, `a`, `of`, `was`, `not`. Perfectly normal list. Now: `the pizza was not cold`. What survives?"

*`pizza`, `cold`.*

**Ask this:** "And `the pizza was cold`?"

*`pizza`, `cold`.*

**Do this:** Say nothing for three seconds. Then write both results on the board, one under the other, and draw a box round them.

```text
the pizza was not cold   ->   pizza  cold
the pizza was cold       ->   pizza  cold
```

**Say this:**

> "**Same row. One customer is happy and one customer is furious, and after my tidying they are the same row of numbers.**
>
> Here is the way to think about all of this. **Normalizing is tidying a room before you count what is in it.** Putting all the pens in one drawer genuinely helps. Throwing out everything small helps even more — right up until you notice you have thrown out the house keys.
>
> **`not` is a house key.** And nobody can give you a list of which words are house keys, because it depends on what you are doing. For finding out what a review is *about*, `not` is noise. For finding out how the writer *felt*, `not` is the whole thing."

**Do this:** Now the grid. Write the four whiteboard reviews:

```text
d1: The pizza was great!
d2: The pizza was cold.
d3: Great pizza, great service.
d4: Cold service and cold food.
```

**Ask this:** "Tokenize all four in your head. How many *different* words are there altogether?"

*Take guesses, then build the list on the wall sheet in alphabetical order:* `and, cold, food, great, pizza, service, the, was` — **eight.**

**Do this:** Write and box:

> **Bag-of-words** — a document as a list of word counts, order ignored. A *bag*, because you tipped the words in and shook it.
> **Document-term matrix** — one row per document, one column per vocabulary word, and the cell is a count.

**Say this:**

> "Four reviews, eight words. **Four rows by eight columns is thirty-two cells, and you are about to fill in every single one of them by hand.** Then we will ask the computer and check all thirty-two. That is the next forty minutes, and it is not busywork — it is the reason you will trust everything in Weeks 32 and 33."

---

### 💻 Live-Code Together — `bag.py` (18 minutes)

**You never touch their keyboard.** They type; you narrate.

**Step 1 (4 min) — the four tokenizers.**

```python
import re

raw = "The pizza was GREAT!!  But the service wasn't."
print("raw.split()   :", raw.split())
print("lower + split :", raw.lower().split())
print("lower + regex :", re.findall(r"\b\w\w+\b", raw.lower()))
```

```text
raw.split()   : ['The', 'pizza', 'was', 'GREAT!!', 'But', 'the', 'service', "wasn't."]
lower + split : ['the', 'pizza', 'was', 'great!!', 'but', 'the', 'service', "wasn't."]
lower + regex : ['the', 'pizza', 'was', 'great', 'but', 'the', 'service', 'wasn']
```

> **Say this:** "Three lines, three policies, and every one of them is a decision you are making on behalf of every review you will ever process. **Read the last token of each line: `wasn't.`, then `wasn't.`, then `wasn`.** By line three the negation has become a nonsense word."

**Step 2 (3 min) — 🐞 DELIBERATE MISTAKE ONE: one document or many?**

> **Say this:** "Right, the counter. It works like `StandardScaler` — you `fit` it and it learns something, then you `transform`. Let me just count one sentence."

```python
from sklearn.feature_extraction.text import CountVectorizer
CountVectorizer().fit_transform("the pizza was great")
```

Real output, last line:

```text
ValueError: Iterable over raw text documents expected, string object received.
```

**Do this:** Read the message out loud, slowly, twice. Point at the two halves.

**Ask this:** "It wanted one thing and got another. What did it want, and what did I give it?"

*Hoped-for answer:* it wanted a list of documents; I gave it one document.

> **Say this:** "**It wanted a collection of documents and I handed it one string.** And think about why that even matters: to this thing, a document is 'one row of the answer'. If I give it one string, does it make one row, or does it make one row per letter? **It refuses to guess, and it is right to refuse.** So: always a list, even for one document. `["the pizza was great"]`, with the brackets."

Fix it live, with the four reviews:

```python
docs = ["The pizza was great!",
        "The pizza was cold.",
        "Great pizza, great service.",
        "Cold service and cold food."]
cv = CountVectorizer()
counts = cv.fit_transform(docs)
print("vocabulary :", cv.get_feature_names_out())
print("shape      :", counts.shape)
print("matrix type:", type(counts).__name__)
print("stored     :", counts.nnz, "non-zero cells of", 4 * 8)
```

```text
vocabulary : ['and' 'cold' 'food' 'great' 'pizza' 'service' 'the' 'was']
shape      : (4, 8)
matrix type: csr_matrix
stored     : 15 non-zero cells of 32
```

**Ask this:** "The vocabulary is the same eight words we put on the wall sheet, in the same order. **Who decided that order?**"

*Alphabetical, and `CountVectorizer` chose it.*

> **Say this:** "Alphabetical, and it chose it, not us. Which means **column 3 means `great` and nothing else**, for the whole of the rest of this term. Write that on the wall sheet. And `get_feature_names_out()` is how you ever find that out — a matrix of numbers does not remember what its columns were called unless you ask."

**Step 3 (4 min) — the grid, and why `.toarray()` exists.**

```python
import pandas as pd
print(pd.DataFrame(counts, index=["d1", "d2", "d3", "d4"],
                   columns=cv.get_feature_names_out()))
```

```text
ValueError: Shape of passed values is (4, 1), indices imply (4, 8)
```

**Ask this:** "It thinks I handed it a grid four rows by **one** column. Why one?"

*Take answers. Steer to: the sparse matrix is not a grid; pandas sees it as a single object per row.*

> **Say this:** "Because `counts` is not a grid. It is a `csr_matrix` — a **sparse matrix** — and it is not holding thirty-two numbers. It is holding fifteen. **It stores only the cells that have something in them.**"

```python
for line in str(counts).splitlines()[:4]:
    print(line)
```

```text
  (0, 6)	1
  (0, 4)	1
  (0, 7)	1
  (0, 3)	1
```

> **Say this:** "Read the first line as **'row 0, column 6, holds 1'**. Row 0 is d1. Column 6 is `the`. And d1 contains `the` once.
>
> **Now the important thing: there is no line anywhere in that list that says row 0 column 0 holds 0.** Storing a zero would be storing nothing. Fifteen lines for thirty-two cells, and the other seventeen simply do not exist as far as the computer is concerned.
>
> To see an actual grid you have to ask for one, and the word is `.toarray()`."

```python
print(pd.DataFrame(counts.toarray(), index=["d1", "d2", "d3", "d4"],
                   columns=cv.get_feature_names_out()))
```

```text
    and  cold  food  great  pizza  service  the  was
d1    0     0     0      1      1        0    1    1
d2    0     1     0      0      1        0    1    1
d3    0     0     0      2      1        1    0    0
d4    1     2     1      0      0        1    0    0
```

**Do this:** Leave that on the screen. **The class is about to check every cell of it by hand and they will need it up.**

**Step 4 (4 min) — 🐞 DELIBERATE MISTAKE TWO: the missing `r`.**

> **Say this:** "One more. I keep typing that `r` in front of the pattern and I have never been sure it matters. Let me find out."

```python
print("lower + regex :", re.findall("\b\w\w+\b", raw.lower()))
```

```text
lower + regex : []
```

**Do this:** Say nothing. Point at the empty brackets. Wait.

**Ask this:** "What went wrong?"

*Hoped-for answer:* nothing crashed; it just found nothing.

> **Say this:** "**Nothing went wrong. That is the problem.** No error. No warning. No red. An empty list, and if this were line 4 of a two-hundred-line program you would spend an hour looking in the wrong place.
>
> Here is what happened. Without the `r`, Python looks at `\b` and says *'ah, that is the backspace character'* — the thing the backspace key sends. So the pattern went hunting for a literal backspace character in the review, found none, and honestly reported none.
>
> **`r` means 'raw': do not touch my backslashes, hand them to the pattern exactly as I typed them.** One letter. No error if you leave it out. **Bug Log.**"

**Do this:** Bug Log entry. Message: *"no message — an empty list"*. Meaning: *"the pattern never matched anything"*. Cause: *"missing `r` before the quotes, so `\b` became a backspace character"*. Fix: *`r"\b\w\w+\b"`*. **Alarm: an empty list from a pattern is almost always a raw-string problem.**

**Step 5 (3 min) — their own sixty reviews.**

```python
from reviews import CORPUS_60
X = CountVectorizer().fit_transform(CORPUS_60)
cells = X.shape[0] * X.shape[1]
print("documents        :", X.shape[0])
print("vocabulary size  :", X.shape[1])
print("cells in the grid:", cells)
print("non-zero cells   :", X.nnz)
print("zero cells       :", cells - X.nnz,
      "= %.1f%% of the grid" % (100 * (cells - X.nnz) / cells))
```

```text
documents        : 60
vocabulary size  : 92
cells in the grid: 5520
non-zero cells   : 363
zero cells       : 5157 = 93.4% of the grid
```

**Ask this before running:** "Sixty reviews, and let us say ninety-something different words. **How many cells?**"

*60 × 92 = 5,520.*

**Ask this:** "And how many of those 5,520 do you think have a number in them?"

*Take guesses. They will guess far too many.*

> **Say this:** "**Three hundred and sixty-three.** Ninety-three point four per cent of that grid is empty, and here is the part that should bother you: **it tends to get emptier as you add reviews, not fuller.** Most new reviews bring a few new words, and every new word adds a whole column of zeros for all the reviews that came before.
>
> A real corpus — twenty thousand news articles, fifty thousand different words — is a billion cells with maybe a million numbers in it. **Stored as a grid that is eight gigabytes. Stored as a list of the non-zeros it is about eight megabytes.** That is the difference between 'runs on your laptop' and 'does not run at all', and it is why every text tool in Python hands you a sparse matrix whether you asked for one or not."

---

### 🎲 Their Turn — The 32 Cells, and the Order Demo (20 minutes)

Full instructions in **🎲 The Activity, In Full** below. In outline: **twelve minutes** filling in all thirty-two cells of the 4×8 grid by hand on squared paper, in pen, then a second pass in a different colour ticking each one against the printout on screen; then **eight minutes** on the Order Demo — the two dog-and-man sentences, predicted in pen first, then typed.

---

### 🔑 Wrap & Assign (7 minutes)

**Do this:** Stand at THE VOCABULARY wall sheet with all thirty-two cells now filled in and ticked.

**Say this:**

> "Thirty-two cells. You filled in every one by hand and then you checked every one against the computer. **You now know, because you checked, that `CountVectorizer` is doing exactly the counting you did on paper.** That matters more than it sounds like it does, because from next week the numbers get harder and you will not be able to check them by feel. You will have to check them by arithmetic. Today you proved to yourself that it is worth doing."

**Do this:** Type the order demo result again and leave it up.

```text
             bit  dog  man  the
dog bit man    1    1    1    2
man bit dog    1    1    1    2
are the two rows identical? True
```

**Ask this:** "Somebody tell me what is wrong with that."

*One sentence is about a dog biting a man; the other is a man biting a dog; the rows are identical.*

**Say this:**

> "**Identical. Cell for cell.** Subtract one row from the other and you get zero in every column. **There is no number left anywhere in that row that records which animal did the biting.**
>
> And I want to be precise about what kind of problem this is. **It is not a bug.** Nobody is going to fix it in the next version. It is not a limitation of `CountVectorizer`; it is a limitation of *counting words*, and it applies to every bag-of-words model that has ever been built. **It is the price of the method, and you pay it every single time.**
>
> The skill — the actual engineering skill, the thing that makes you different from somebody who just imports things — **is knowing exactly what you paid.** So here is the bill, and I want it in your workbook."

**Do this:** Write the bill on the board:

```text
WHAT COUNTING WORDS THROWS AWAY
  1. word order        "dog bit man" = "man bit dog"
  2. negation          "good" and "not good" both contain good
  3. what modifies what  "cheap phone, great camera" = "great phone, cheap camera"
```

**Ask this:** "One of those three you can nearly patch, and we do it in two weeks. Which one do you think, and how?"

*Take answers. Somebody will suggest counting pairs of words instead of single words.*

> "**That is exactly the patch, and it is called n-grams, and you have just invented it.** Hold that thought until Week 33, because we are going to measure whether it works, and the answer is going to be more interesting than yes."

**Do this:** Three quick checks — exact wording in **✅ Assessing Understanding**.

**Say this, to close:**

> "One last number. **93.4 per cent.** That is how much of your own 60-review grid is empty, and next week that number becomes useful rather than just surprising.
>
> Because look at your ten commonest words. `and` fifty-five times. `the` thirty-four. `was` twenty-six. **Then `cold` eleven and `rude` ten.** Right now the grid treats `and` and `rude` exactly the same way: a number in a column. **And `and` tells you absolutely nothing about a review, while `rude` tells you everything.**
>
> Next week you learn how to make the computer notice that difference. It takes one multiplication and one division, and it is the single most useful piece of arithmetic in the whole of classic text processing."

**Do this:** Hand out the homework and read the third part out loud, slowly.

---

## 🐞 The Debugging Clinic

Every message below came from running a broken version of this week's actual code.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Iterable over raw text documents expected, string object received.` | "You gave me one document. I wanted a collection of them." | `cv.fit_transform("the pizza was great")` — no brackets. | Wrap it in a list: `cv.fit_transform(["the pizza was great"])`. **Even for a single review. Always a list.** |
| `sklearn.exceptions.NotFittedError: Vocabulary not fitted or provided` | "I do not know what the columns are called yet." | `cv.get_feature_names_out()` before any `fit`. | `cv.fit(docs)` or `cv.fit_transform(docs)` first. **The vocabulary is the learned thing; there is nothing to report before it is learned.** |
| `AttributeError: 'CountVectorizer' object has no attribute 'get_feature_names'` | "That method used to exist and does not any more." | Copied from an old tutorial. The name gained `_out` in scikit-learn 1.0. | `get_feature_names_out()`. **And a general lesson: a tutorial from 2019 will do this to you about four times.** |
| `AttributeError: 'list' object has no attribute 'lower'` | "One of the things you called a document is a list." | `cv.fit_transform([d.lower().split() for d in docs])` — tokenizing *before* handing it over. | Hand `CountVectorizer` the **raw strings**. It does its own lowercasing and its own tokenizing. **Doing the job twice breaks it.** |
| `ValueError: Shape of passed values is (4, 1), indices imply (4, 8)` | "I see four rows and one column; you promised eight columns." | `pd.DataFrame(counts, ...)` on a sparse matrix. | `pd.DataFrame(counts.toarray(), ...)`. **A sparse matrix is not a grid until you ask it to become one.** |
| `ValueError: Shape of passed values is (4, 8), indices imply (4, 7)` | "You gave me eight columns of numbers and seven column names." | The `columns=` list was typed out by hand and a word was missed. | `columns=cv.get_feature_names_out()`. **Never type the vocabulary by hand. Ask for it.** |
| `TypeError: expected string or bytes-like object` | "That is not text." | `re.findall(r"\b\w\w+\b", 12.5)` — a number, or a `NaN` from a spreadsheet column. | `str(x)` first, or clean the column. **A missing value in a text column arrives as a float, and this is the message it produces.** |
| `IndexError: Index dimension must be 1 or 2` | "You indexed a matrix with a word." | `counts[0, "great"]` — a count matrix has **numbered** columns, not named ones. | Find the number first: `j = list(cv.get_feature_names_out()).index("great")`, then `counts[0, j]`. |
| `NotImplementedError: adding a nonzero scalar to a sparse array is not supported` | "Adding 1 to every cell would fill in all the zeros, and then it would not be sparse any more." | `counts + 1`. | `counts.toarray() + 1` if you really mean it. **And notice the error is telling you something true: the whole saving is that the zeros are not there.** |
| **No error. `re.findall` returns `[]`.** | Nothing crashed. The pattern matched nothing at all. | The `r` is missing: `re.findall("\b\w\w+\b", text)`. Python read `\b` as a backspace character. | `r"\b\w\w+\b"`. **An empty list out of a pattern is almost always a missing `r`.** |
| **No error. The vocabulary changes size between two runs.** | Nothing crashed, and every column now means something different. | `fit_transform` was called a second time, on different documents. It **refits**, so the old vocabulary is thrown away. | `fit_transform` on the training documents **once**; `transform` on everything else. Real proof: fit on `["cold pizza", "great pizza"]` gives `['cold' 'great' 'pizza']`; then `fit_transform(["cold chips"])` gives `['chips' 'cold']` and shape `(1, 2)`, while `transform(["cold chips"])` gives `[[1 0 0]]` and shape `(1, 3)`. **One of those two is a bug and neither of them says so.** |
| **No error. The word `i` is missing from the vocabulary.** | Nothing crashed. Every one-letter word has gone. | `\w\w+` means **two or more characters**, and that is `CountVectorizer`'s default pattern. | Nothing, usually. If you need single letters, `token_pattern=r"\b\w+\b"`. **But know that it happened, because on maths text it deletes every `x`.** |

### How to teach debugging without giving the answer

All the old moves stand. This week adds three, and the first one is the most transferable thing in the lesson.

26. **"What did it give you back, and how long is it?"** For text work, `len()` of the thing you just made is the check. Zero tokens, zero documents, or a vocabulary of size 1 are all silent disasters and all visible in one `print(len(...))`.

27. **"Is that one document, or a list of documents?"** Half of this week's errors are this question. **A string is one document. A list of strings is a corpus. Getting them mixed up is the week's signature bug.**

28. **"Did you `fit` twice?"** If two matrices have different numbers of columns, or the same column number means two different words, somebody called `fit_transform` when they meant `transform`. **This is Week 6's leakage discipline wearing a new hat, and it comes back with teeth in Week 33.**

And the sentence for this week:

> **"Text code fails quietly. A shape error shouts; an empty token list just sits there looking normal. So print three numbers every time you vectorize anything: how many documents, how many words in the vocabulary, and how many non-zero cells. If any of the three surprises you, stop."**

---

## 🎲 The Activity, In Full

This section gives the full set-up and steps for the two hands-on parts of the lesson.

### Part A — The Thirty-Two Cells (12 minutes)

**What it is.** Every student fills in all thirty-two cells of the 4×8 document-term matrix by hand, in pen, on squared paper. Then, in a **different colour**, they tick each cell against the printout on screen. Thirty-two ticks.

**Why it is worth twelve minutes of a seventy-minute lesson.** Because Weeks 32 and 33 ask the student to trust numbers they cannot check by eye — a TF-IDF weight of `0.841002`, a coefficient of `−3.0641`. **The only reason to trust those is that the last time you could check the library by hand, you did, and it agreed with you.** This is that time. It never comes again this year.

### Setup

- Squared paper, one sheet each. **Landscape.**
- Two pens of different colours.
- Workbook A4 ("Label the count matrix") shows this same 4×8 grid with four cells left blank — use it afterwards to check, not instead of the squared paper.
- The four reviews on the board, and THE VOCABULARY wall sheet with the eight words on it.
- **The screen showing the printout, but covered or scrolled away** until step 3.

### Step 1 — rule the grid (2 minutes)

Eight columns, four rows. Column headings from the wall sheet, in the order `CountVectorizer` chose:

```text
        and  cold  food  great  pizza  service  the  was
  d1
  d2
  d3
  d4
```

**Say this:** *"Alphabetical, because that is what the library does. Column 3 is `great` for the rest of this term."*

### Step 2 — fill in all thirty-two, in pen (6 minutes)

One rule, said out loud before they start, and written on the board:

> **Every cell is: how many times does this word appear in this review? If it does not appear, write 0. Do not leave it blank.**

**Do this:** Walk the room. Two things to watch for and both are worth stopping the room over:

1. **Blanks instead of zeros.** *"A blank is not a number. The computer does not have blanks."* Every cell gets a digit.
2. **The `great` cell in d3.** Somebody will write 1. The review is `"Great pizza, great service."` **Let the argument happen** — it is the best ninety seconds available today — then read the definition off the board: *how many times the word appears*. **Twice.**

**Expected finish:** most students in five minutes. The row totals are a good self-check and worth putting on the board: d1 = 4, d2 = 4, d3 = 4, d4 = 5.

### Step 3 — the second pass, in the other colour (4 minutes)

**Do this:** Now reveal the printout.

```text
    and  cold  food  great  pizza  service  the  was
d1    0     0     0      1      1        0    1    1
d2    0     1     0      0      1        0    1    1
d3    0     0     0      2      1        1    0    0
d4    1     2     1      0      0        1    0    0
```

> **Say this:** "Second colour. **Thirty-two ticks, one per cell.** Do not just glance at it and decide it looks right — a cell at a time, left to right, top to bottom. If one disagrees, do not change your number yet. **Circle it and put your hand up**, because there are two possible explanations and one of them is that I am wrong."

**Ask this, once the room is quiet:** "Hands up if all thirty-two agreed. Hands up if one did not."

**What "finished" looks like:**

- A grid of thirty-two digits in pen, with thirty-two ticks over them in a second colour.
- Anybody who disagreed has circled the cell and found out why.
- The student can answer, unprompted: *"the library counted exactly what I counted."*
- **The row totals 4, 4, 4, 5 written down the side and checked against the number of tokens in each review.**

### Variation — easier

**Cut the grid to 4 columns.** Use only `cold`, `great`, `pizza`, `service` — sixteen cells, and the two interesting cells (d3's `great` = 2, d4's `cold` = 2) are both still in it. **Objective 2 survives completely; only the arithmetic gets shorter.**

**And give them the tokenized reviews already written out**, one line each, so the only job is counting:

```text
d1: the pizza was great
d2: the pizza was cold
d3: great pizza great service
d4: cold service and cold food
```

**One scaffold that works very well:** do d1 together on the board, all eight cells, out loud, and leave it on the board as the worked row. Then they do d2, d3 and d4 alone.

### Variation — harder

1. **Predict the vocabulary before running.** Write the eight words down, in the order they think `CountVectorizer` will use, *before* it is printed. **Getting alphabetical order right is the point.**
2. **Add a fifth review and predict what happens to the shape.** `"The service was great!"` adds no new words, so the shape becomes `(5, 8)` and not `(5, 9)`. **Predicting that correctly is a real piece of understanding.**
3. **Find a five-word review that produces a row of all zeros.** It has to be five words none of which are in the vocabulary, e.g. `"nobody answered my phone calls"` → all eight cells 0. **Then the question that matters: what would a model predict for that review?** Nothing useful, and it would not tell you.
4. **Count the zeros and predict the percentage before dividing.** 32 − 15 = 17, and 17 ÷ 32 = 53%. Then predict whether adding a fifth review makes the percentage go up or down. **Up, if the review brings new words.**

### Part B — The Order Demo (8 minutes)

**What it is.** Two sentences, predicted in pen, then typed. Eight minutes, and six of them are talking.

### Step 1 — predict, in pen (3 minutes)

**Do this:** Write on the board:

```text
the dog bit the man
the man bit the dog
```

> **Say this:** "Next page of the notebook. **In pen.** Vocabulary first — how many different words are in those two sentences altogether? Then write out both rows."

*The vocabulary is four: `bit`, `dog`, `man`, `the`.*

**Ask this:** "Before you write the rows — **will they be the same or different?** Commit, in pen."

*Most students say different, because the sentences obviously mean different things. Collect the vote on the board.*

### Step 2 — type it (2 minutes)

```python
pair = ["the dog bit the man", "the man bit the dog"]
cv2 = CountVectorizer()
P = cv2.fit_transform(pair).toarray()
print("vocabulary:", cv2.get_feature_names_out())
print(pd.DataFrame(P, index=["dog bit man", "man bit dog"],
                   columns=cv2.get_feature_names_out()))
print("are the two rows identical?", bool((P[0] == P[1]).all()))
```

```text
vocabulary: ['bit' 'dog' 'man' 'the']
             bit  dog  man  the
dog bit man    1    1    1    2
man bit dog    1    1    1    2
are the two rows identical? True
```

**Do this:** Say nothing for five seconds.

### Step 3 — the conversation (3 minutes)

**Ask this:** "Why is `the` a 2?"

*It appears twice in each sentence.*

**Ask this:** "Subtract one row from the other. What do you get?"

*Zero in all four columns.*

**Ask this:** "So where, in either of those rows, is the information about who did the biting?"

*Nowhere.*

> **Say this:** "**Nowhere. It is not stored anywhere. It is gone.** And it did not get lost by accident — we threw it away on purpose the moment we decided to count words instead of reading them.
>
> Now the honest question, and it is the one I want in your workbook. **Does that matter?** If I am sorting reviews into 'about the food' and 'about the delivery', it does not matter at all — both sentences are about a biting incident. **If I am working out who to prosecute, it matters completely.**
>
> **There is no general answer.** There is only: *what is this for?*"

**What "finished" looks like:** the order-demo notebook page (workbook B4 and the Puzzle continue it at home) with a prediction in pen, the two identical rows, and one sentence in the student's own words saying what was lost and one situation where it would matter.

---

## ❓ Questions Students Ask This Week

Use this section for the questions students ask this week, with an answer for each.

**"Why does it throw away `i` and `a`? Those are real words."**

Because the default pattern is `\w\w+` — **two or more characters** — and nobody changed it. It is not a considered decision about the English language; it is a default that was reasonable for the job somebody had in 1990 and has been inherited ever since.

**Usually it is harmless.** `i` and `a` are among the least informative words in English, and you were probably going to drop them as stopwords anyway.

**Occasionally it is a catastrophe**, and the example to give is maths text: every `x`, every `y`, every `n` disappears, so `"solve for x"` and `"solve for y"` become the identical row. Also chemistry, also anything with initials in it.

**The honest lesson is bigger than the pattern:** *a default is a decision somebody else made for a different problem.* You should know what every default in your pipeline is doing. `CountVectorizer()` with empty brackets has already made **four** decisions for you — lower-case everything, split on that pattern, drop single letters, keep every word however rare.

**"Couldn't we just keep the punctuation? `!!!` obviously means something."**

You could, and for some jobs you absolutely should. **On abuse detection and sentiment, `!!!`, `?!` and `:-(` are real evidence**, and a serious sentiment system keeps them, sometimes as their own tokens.

The reasons people usually drop them are worth knowing, because they are practical rather than principled: punctuation multiplies your vocabulary (`great`, `great!`, `great!!`, `great!!!` are four columns for one word), it varies enormously between writers for reasons that have nothing to do with meaning, and it is very unevenly used across a corpus so you get thousands of columns each appearing once.

**The decision, stated properly:** keeping punctuation costs you columns and buys you feeling. On a topic task, do not pay. On a sentiment task, think hard. **And either way, write down which you chose, because in three months you will not remember.**

**"What happens to a review whose words are all missing from the vocabulary?"**

You get a row of zeros, and **nothing whatsoever will warn you.**

It is worth doing live if there is time: `transform(["nobody answered my phone calls"])` against our eight-word vocabulary gives eight zeros. The model will then predict something — whatever its default lean is — and it will attach a confidence to it, and the confidence will be a lie, because the model saw literally nothing.

**This is one of the genuinely dangerous things about text models** and there is a cheap defence: after transforming, check how many non-zero entries each row has, and refuse to predict on a row with none. `X.getnnz(axis=1)` gives you that in one line. **Almost nobody does it.**

**"Isn't there a better way? This seems primitive."**

**Yes, and it is Level 4, and you should know that "primitive" is not the same as "worse for your problem".**

The better way replaces a column-per-word with a short list of numbers per word, arranged so that words with similar meanings get similar numbers — so `film` and `movie` end up almost on top of each other instead of being as unrelated as `film` and `hydraulics`. You meet the idea at the end of Week 33 and you build on it for a year.

**But be clear about the trade.** Counting words needs sixty typed reviews, one second, and no internet, and you can read the finished model's mind word by word. The better way needs a great deal more data, a great deal more computation, and hands you three hundred numbers per word that mean nothing to a human. **On a problem the size of yours, the primitive one often wins, and it always explains itself.**

**"Why alphabetical? Wouldn't commonest-first be more useful?"**

**It would be more useful to look at, and it would be a disaster to rely on.** Think about what "commonest" depends on: the documents you happened to fit on. Add one review and the order changes, so column 3 stops meaning `great` and starts meaning `pizza` — and nothing in your code would notice.

**Alphabetical order depends only on the words themselves.** Fit on the same vocabulary twice and you get the same column order twice, on any machine, in any version. **That is worth much more than being nice to read**, and `get_feature_names_out()` exists precisely so that you never have to care what the order is.

**"If word order is so important, why did anyone use this for thirty years?"**

Because **for the jobs they were doing, word order mostly did not matter, and they measured that rather than assuming it.**

Sorting news articles into sport, politics and finance: an article about politics contains the word `election` whatever order it puts it in. Catching spam: the presence of certain words is nearly the whole signal. Search: you type three words and you want documents containing those three words.

**Word order matters most for exactly one family of tasks — the ones where the *relations* between words carry the meaning.** Sentiment is the obvious one, because `not` is a relation. Question answering is another. **And that is why Week 33 is a sentiment lab: it is the task that breaks this method, so it is the task that teaches you what the method is.**

**"How do you decide which words are stopwords?"** *(Nobody fully agrees, and here is why.)*

**There is no settled answer, and the disagreement is real and old.**

**Camp one uses a fixed published list.** There are standard lists — scikit-learn ships one — and they are convenient, reproducible and quotable. Their problem is that they were written for general English and your corpus is not general English. Scikit-learn's own documentation warns against its own list, which tells you something.

**Camp two uses frequency.** Drop the words that appear in more than, say, half your documents, because a word in half your documents cannot separate them. This has the great virtue of being about *your* data. Its problem is that on a small corpus it is unstable: with sixty reviews, the cutoff is decided by a handful of documents.

**Camp three says do not drop stopwords at all** — let the weighting scheme handle it. A word in every document gets a low weight automatically, so why make an irreversible decision when you can make a reversible one? **This is close to the modern consensus for text classification, and it is what Week 32 does.**

**And camp four says the question is wrong**, because "words that carry no information" is not a property of words, it is a property of words *for a task*. `the` is noise for topic classification and evidence for authorship attribution — how often somebody writes `the` is genuinely a fingerprint. The same word, the same corpus, opposite verdicts.

What to tell a fourteen-year-old, out loud: **"Do not drop a word because a list told you to. Drop it because you can say what it would have told you, and you have decided you do not need that. And write down what you dropped, because the word you drop is always the one that mattered."**

---

## ⚠️ Where This Lesson Goes Wrong

Use this section to spot what usually goes wrong, and what to do right now.

| What happens | Why | What to do right now |
|---|---|---|
| **The hand-built grid gets skipped or rushed** | `CountVectorizer` does it in one line and the lesson is running late | **Cut something else.** Cut the sparse-matrix coordinates, cut the 60-review numbers, cut a question from the wrap. **Do not cut the thirty-two cells and do not cut the second-colour ticks**, because the ticks are the evidence for objective 2 and the trust they buy is spent in Weeks 32 and 33. |
| The regex turns into a lesson on regular expressions | It is genuinely interesting and a keen student will pull you in | **One pattern, read out in English, and stop.** *"Find me every run of two or more letters or digits."* If somebody wants more, tell them it is a big and useful subject and point them at it as a hobby. **Ten minutes on `\d{2,4}` costs you the hand-built grid.** |
| The `not` example gets described but not demonstrated | It is quicker to assert it | **Write both reduced rows on the board yourself.** `pizza cold` and `pizza cold`. The silence when the class sees two identical rows for two opposite reviews is the whole of objective 4, and you cannot get it by saying it. |
| Students write blanks instead of zeros | A blank feels like "nothing here", which feels right | **Stop the room the first time you see it.** *"A blank is not a number. There is no blank in a matrix. Every cell has a value and that value is zero."* This misconception returns in Week 33 as the difference between *a column with a zero in it* and *no column at all*, and that difference matters enormously there. |
| The d3 `great` cell gets settled by you instead of by them | It is faster | **Let the argument run for ninety seconds.** Then read the definition off the board rather than giving the answer. **A class that argued its way to 2 will never forget that counts are counts and not ticks.** |
| Somebody concludes the method is stupid | The order demo is genuinely damning | **Give them the thirty years.** Spam filters, search engines, document sorters. Then: *"and in two weeks you will measure what it can and cannot do on your sixty reviews."* **A method with a known price is not stupid. A method whose price you cannot state is.** |
| The lesson drifts into TF-IDF | It is the obvious next thought and a good student will get there | **Write their sentence on the wall sheet with their name on it** and say it is next week's title. **Do not start explaining idf at minute 55.** It needs the full eighteen-minute concept slot it gets next week, and a rushed version is worse than none. |
| The empty-list bug is explained rather than performed | It looks like a trivial typo | **Type it and run it in front of them.** The teaching moment is not "you need an `r`", it is **"nothing went red and the answer was wrong"**, and that only lands if they watch an empty list appear on a screen. |
| The 60-review corpus does not exist | It was homework and homework happens to other people | **Use this file's corpus for the last five minutes**, and set the typing tonight. **Weeks 32 and 33 both need it.** It can be moved; it cannot be dropped. |
| Everybody's vocabulary size is different and it feels like an error | They typed different reviews | **Ask for the arithmetic, not the number.** `their documents × their vocabulary = their cell count` must hold exactly. **That check works for everyone and 92 works only for me.** |

---

## 🧭 Differentiation

Use this section to adjust the lesson for a student who is struggling, flying or not engaging.

### If the student is struggling

**Cut:** the four-tokenizer comparison down to **two** — `.split()` and the regex. The middle two rows make the point sharper but they are not load-bearing.

**Cut:** the sparse-matrix coordinate listing. **Keep the count of zeros** — 17 of 32 — because that is the idea; the `(0, 6) 1` notation is decoration today.

**Cut:** the 60-review corpus numbers entirely if time is short. It is a scale-up of something already shown.

**Give them the tokenized reviews already written out** so the only job is counting:

```text
d1: the pizza was great
d2: the pizza was cold
d3: great pizza great service
d4: cold service and cold food
```

**The version that skips everything hard.** No code and no regex. **One 4×4 grid, sixteen cells**, columns `cold great pizza service`, and three questions:

| | cold | great | pizza | service |
|---|---:|---:|---:|---:|
| d1 `The pizza was great!` | | | | |
| d2 `The pizza was cold.` | | | | |
| d3 `Great pizza, great service.` | | | | |
| d4 `Cold service and cold food.` | | | | |

> **"Fill in all sixteen. Which two cells are not 0 or 1, and why? And which two rows are most alike?"**

The answers are d3's `great` = 2 and d4's `cold` = 2, both because the word is in the review twice; and d1 and d2 are most alike, sharing `pizza`. **That last answer is objective 2 complete, and it also sets up the surprise of Week 32 — that the two most similar reviews are a happy one and an unhappy one.**

**The copy-this-exactly scaffold.** Eight lines and it runs on its own:

```python
from sklearn.feature_extraction.text import CountVectorizer

docs = ["the pizza was great", "the pizza was cold"]
cv = CountVectorizer()
counts = cv.fit_transform(docs)
print(cv.get_feature_names_out())
print(counts.toarray())
```

```text
['cold' 'great' 'pizza' 'the' 'was']
[[0 1 1 1 1]
 [1 0 1 1 1]]
```

Then two questions and nothing else: **"which column is `cold`, and why is it 0 in the first row?"** It is column 0, and it is 0 because the first review does not contain the word `cold` — **but the column still exists, because the second review does.** Let them find that themselves; it is the misconception worth killing early.

**One thing you must not cut:** the order demo. If the whole lesson collapses to one sentence, make it *"counting words cannot tell `the dog bit the man` from `the man bit the dog`, and that is the price of the method."*

### If the student is flying

None of these need syntax from a later week.

1. **Predict the vocabulary, in order, before running.** Alphabetical, eight words. Then predict what a fifth review of `"The service was great!"` does to the shape — `(5, 8)`, not `(5, 9)`, because it brings no new words.
2. **Find the all-zero row.** Write a five-word review none of whose words are in the vocabulary, transform it, and get eight zeros. **Then the real question: what would a model predict, and how confident would it claim to be?** This is genuinely dangerous behaviour and very few people check for it.
3. **Count how many one-letter words their own corpus lost.** In the corpus in this file, `i` appears in several reviews and is in the vocabulary **zero** times. Then: how many rows did that change? **And is there any task where it would have mattered?**
4. **Write a pair of sentences that are opposite in meaning and identical as rows.** Harder than it sounds and a genuinely good exercise. Beyond word order, the easy route is negation plus a stopword list. **The pair they invent goes on page 31.6.**
5. **Work out the storage arithmetic for a real corpus.** 20,000 documents, a 50,000-word vocabulary: 1,000,000,000 cells. At 8 bytes each that is 8 gigabytes. If one cell in a thousand is non-zero, storing the non-zeros costs about 8 megabytes plus the coordinates. **A factor of a thousand, from one design decision.**
6. **Tokenize a sentence containing a price, an email address and an emoticon**, and list everything the default pattern destroyed. Real output: `"Call me on 555-0134 or email me@example.com!!"` becomes `['call', 'me', 'on', '555', '0134', 'or', 'email', 'me', 'example', 'com']` — the phone number is two numbers, the email is three words, and `me` now appears twice. **Then: for which task is each of those losses fatal?**

### If the student won't engage today

**Close the laptop. Four reviews on paper and a pen.**

Write the four reviews out. Then three instructions and nothing else:

> **"Underline every different word you can find in all four reviews. How many are there?"**
>
> **"Now write them out in alphabetical order across the top of the page."**
>
> **"Under `cold`, write how many times `cold` appears in each review, one number per review."**

Eight words; `and cold food great pizza service the was`; the `cold` column is `0, 1, 0, 2`. **That is objective 2's whole understanding with no machine and no code**, and the 2 at the bottom of the column is the interesting bit — ask why it is not 1.

If they will take one more, go straight to the order demo on paper:

> **"Write out `the dog bit the man`. Now write out `the man bit the dog`. How many different words in total?"**
>
> **"Count each word in each sentence. Write the two rows."**
>
> **"Are they the same?"**

Four words; both rows `1 1 1 2`; **yes, identical.** Then the question that lands: **"so which sentence did the dog do the biting in?"** They cannot tell from the rows. **That is the best moment in the lesson and it needs nothing but a pencil.**

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the two cells that are not 1 or 0 (spoken, 45 seconds)**

> "In our 4×8 grid, **thirty of the cells are 0 or 1 and two of them are 2.** Name one of the twos and tell me why it is a two."

*Good answer:* "d3's `great` cell. d3 is `Great pizza, great service.` and the word `great` is in it twice, so the count is 2. Or d4's `cold`, same reason."

**What to catch:** "because `great` is important" or "because it's a strong word". **Push once:** *"how many times does the word appear?"* **Full marks needs the word "twice".** A cell is a count, not a judgement, and a student who has not got that will not follow Week 32's `tf` at all.

**Check 2 — the order demo (spoken, 60 seconds)**

> "`the dog bit the man` and `the man bit the dog` come out as the identical row. **Is that a bug in `CountVectorizer`?**"

*Good answer:* "No. It's what counting words means. The row records which words are there and how many times, and there's nowhere in it to put the order, so the order is gone. Nobody's going to fix it — it's the price of the method."

**What to catch:** "yes, it's broken" and also "no, because it's a library so it must be right". **Neither is the point.** The correct answer names the *design decision*, not the software. A student who says *"we threw the order away on purpose when we decided to count"* is at level 4.

**Check 3 — the normalization that would be wrong (written, 90 seconds)**

> "Give me **one** normalization choice, and **one sentence from your own corpus** where that choice would destroy the meaning. Both, on paper."

*Good answer:* "Dropping stopwords, if `not` is on the list. `the pizza was not cold` and `the pizza was cold` both become `pizza cold` — one is a happy customer, one is not, and after tidying they are the same row." **Or:** "lowercasing, because I have a review saying `THE FOOD WAS COLD` and shouting is evidence, and `.lower()` deletes it."

**What to catch:** a choice with no sentence attached, or a sentence with no choice attached. **The pairing is the objective.** *"Stopwords are bad"* scores nothing; *"stopwords are bad because of this exact sentence"* scores full marks. **This is the check that predicts whether Week 33's post-mortem will be any good.**

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot say what a token is. Leaves cells blank instead of writing 0. Thinks a cell is a tick rather than a count. Cannot say what the vocabulary is or where it came from. |
| **2 — Emerging** | Fills in the grid with help and gets most of the thirty-two cells right. Can point at the repeated word once it is pointed out. Knows `CountVectorizer` makes the grid but not that it also chose the vocabulary. |
| **3 — Secure** | Builds all thirty-two cells unaided and checks every one. Explains both 2s. Says what the vocabulary is, where it came from, and that it is alphabetical. Demonstrates the order demo and states what it costs. Names one normalization choice with a sentence that breaks it. **This is the target.** |
| **4 — Strong** | Predicts the vocabulary in alphabetical order before running. Spots that a fifth review with no new words leaves the shape at `(5, 8)`. Says out loud that the order was thrown away *on purpose*, not lost. Notices that a zero in a column and no column at all are different situations. Invents their own opposite-meaning identical-row pair. |
| **5 — Exceptional** | Asks about the single-letter words before being told, and finds a task where dropping them would be fatal. Works out the sparse-storage arithmetic and says why sparsity gets worse as the corpus grows. Says unprompted that `the` is getting the same treatment as `rude` and that this must be wrong — i.e. invents Week 32. Proposes counting pairs of words to recover order — i.e. invents Week 33's n-grams — and can say why it would only half work. |

---

## 📤 Homework to Assign

Use this section to set the homework: what to say, and what the student receives.

**Say this:**

> "About an hour, three pages, and the third one is the one I mark hardest.
>
> **First, page 31.4 — six sentences, twice each.** Tokenize each one **by hand**, the way a person would say the words are, and then with `re.findall(r"\b\w\w+\b", s.lower())`. Two lists per sentence. **Then list every single place they disagree, and put a verdict next to each disagreement: which one is right, and for what task.** Not 'the regex is wrong' — *'the regex turned `$12.50` into 12 and 50, which is wrong if I care about price and fine if I only care about topic.'*
>
> **Second, page 31.5 — five reviews, fifty cells, by hand.** Same drill as today: rule the grid, fill in every cell in pen, then check every cell against `CountVectorizer` in a second colour. **And give me the row totals and the column totals**, because those are the two checks that catch a miscount.
>
> **Third, page 31.6 — and this is the page I care about.** Find **one** normalization choice that would be **wrong for your own sixty reviews**, and prove it with a sentence pair out of your own corpus. **Two reviews that mean opposite things and come out as the same row.** Write both reviews, write both token lists, write both rows, and write one sentence saying what was lost. **A page that says 'stopwords can be bad' with no sentence attached scores nothing**, and I will hand it back once.
>
> Page 31.7 is a stretch: it asks what happens to a review made entirely of words your vocabulary has never seen. **The answer is quietly alarming and I want to know whether it alarms you.**"

**Workbook pages:** the 32 cells and the order demo are done in class on squared paper (notebook, not workbook) · **Build It pages 31.4, 31.5, 31.6** at home · 31.7 optional. The remaining workbook sections (Warm-Up, Maths by Hand, Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle, Think Deeper, Draw It, Self-Check) are not numbered pages; set them as the week's extra practice as time allows. The Answer Key has a section for every one.

**Expected time:** 20 min on the six sentences · 25 min on the fifty cells · 15 min on the normalization case · **about 60 minutes**, plus 15 more for the stretch.

> **🧑‍🏫 What to look for when you mark it:** three things, and the third is the real one. **One — are there fifty digits on page 31.5, and fifty ticks?** No blanks. A blank cell is the misconception, not a slip. **Two — do the row totals match the token counts?** e1 has 4 tokens and its row must sum to 4; e2 has 5 and sums to 5; e5 has 5 and sums to 5. **A grid whose row totals do not match the token counts has a miscount in it and the student can find it themselves** — hand it back with only that check circled. **Three — does page 31.6 contain an actual sentence pair from their own corpus?** The bar is: *two reviews, written out in full, that mean opposite things and produce the same row.* Generic statements about stopwords score nothing. **And praise loudly anybody whose pair does not use `not`** — negation is the obvious route and finding a second one (shouting, a price, a hyphenated word, `US` versus `us`) is genuinely harder and shows they understood the principle rather than memorising the example.

---

## 🔑 Answer Key

Every workbook section and item is restated below in the **workbook's own order**, so you can mark from this page alone. The workbook has no pages 31.1–31.3 — its only numbered pages are the four Build It pages, **31.4–31.7**. The three in-class exercises that used to be called 31.1–31.3 are **notebook pages** (squared paper, in pen), and they come first.

| Where the student writes | Answered under |
|---|---|
| Notebook, in class: tokenize by hand · the 32 cells · the order demo | **In-class notebook pages 1–3** (first three sections below) |
| Workbook **✅ Warm-Up** W1–W5 | Workbook sections, Warm-Up |
| Workbook **🔢 Do the Maths by Hand** M1–M4 | Workbook sections, Maths |
| Workbook **🔎 Predict the Output** P1–P4 | Workbook sections, Predict |
| Workbook **✍️ Practice Set A** A1–A6 (A4 is the labelled figure) | Workbook sections, Set A |
| Workbook **✍️ Practice Set B** B1–B5 | Workbook sections, Set B |
| Workbook **🐞 Fix the Broken Program** Bugs 1–3 | Workbook sections, Fix |
| Workbook **🧩 Puzzle of the Week** (a)–(f) | Workbook sections, Puzzle |
| Workbook **🤔 Think Deeper** T1, T2 | Workbook sections, Think Deeper |
| Workbook **🛠️ Build It** pages **31.4, 31.5, 31.6, 31.7** (the marked homework) | **Pages 31.4–31.7** below |
| Workbook **🎨 Draw It** and **📊 Self-Check** | After page 31.7 |

### In-class notebook page 1 — Tokenize by hand, in pen, before running (in class)

*The sentence:* `The pizza was GREAT!!  But the service wasn't.`

*(a) Cut it at every space. How many pieces, and what are they?*

**Eight:**

```text
['The', 'pizza', 'was', 'GREAT!!', 'But', 'the', 'service', "wasn't."]
```

> **Note for you:** there are two spaces between `GREAT!!` and `But`, and `.split()` treats a run of spaces as one break. **A student who writes nine pieces because they counted the double space has done something reasonable and should be told so before being corrected.** Python prints 8.

*(b) How many different tokens are there for the word `the`?*

**Two:** `The` and `the`. And to the computer they are as unrelated as `the` and `hydraulics`.

*(c) Now lower-case first. What changes?*

`The` becomes `the`, and `But` becomes `but`. **The count is still 8; the number of *different* tokens drops from 8 to 7**, because `the` now appears twice.

*(d) Now predict what `re.findall(r"\b\w\w+\b", s.lower())` gives.*

```text
['the', 'pizza', 'was', 'great', 'but', 'the', 'service', 'wasn']
```

**Three things changed and all three are worth a sentence:** `great!!` lost its exclamation marks; `wasn't.` became `wasn`; and the stray `t` was dropped because it is one letter long and the pattern wants two or more.

**Marking notes.** **Present or absent, not right or wrong** — this page is a prediction made in pen. **What earns credit is spotting `wasn`.** A student who predicts `wasn't` for (d) has made a completely sensible prediction and gets full credit for having made it; the lesson happens when the real output appears.

### In-class notebook page 2 — The thirty-two cells (in class)

| | and | cold | food | great | pizza | service | the | was | row total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **d1** | 0 | 0 | 0 | **1** | **1** | 0 | **1** | **1** | **4** |
| **d2** | 0 | **1** | 0 | 0 | **1** | 0 | **1** | **1** | **4** |
| **d3** | 0 | 0 | 0 | **2** | **1** | **1** | 0 | 0 | **4** |
| **d4** | **1** | **2** | **1** | 0 | 0 | **1** | 0 | 0 | **5** |
| **column total** | 1 | 3 | 1 | 3 | 3 | 2 | 2 | 2 | **17** |

**The two cells that are not 0 or 1:** d3's `great` = 2, because `"Great pizza, great service."` contains `great` twice. d4's `cold` = 2, because `"Cold service and cold food."` contains `cold` twice.

**The checks that catch a miscount, and both should be on the page:**

- **Row totals** must equal the number of tokens in that review: 4, 4, 4, 5. ✅
- **All the totals must agree:** 4 + 4 + 4 + 5 = 17, and 1 + 3 + 1 + 3 + 3 + 2 + 2 + 2 = 17. ✅
- **Non-zero cells:** 15 of 32, which is what `counts.nnz` printed. 32 − 15 = 17 empty cells, and 17 ÷ 32 = 53%.

> **⚠️ Watch out:** the total of all the counts (17) and the number of non-zero cells (15) are **both 17 and 15 and it is easy to muddle them.** They differ by exactly 2 — the two cells holding a 2 rather than a 1. **That is a lovely check and worth pointing out: total counts − non-zero cells = the number of repeats in the whole corpus.**

**Marking notes.** **Thirty-two digits and thirty-two ticks in a second colour.** No blanks. The two 2s must be there. **A student whose row totals are written down and match has checked their own work, which is the habit being taught** — say so.

### In-class notebook page 3 — The order demo (in class)

*(a) Vocabulary of the two sentences.* **Four words:** `bit`, `dog`, `man`, `the`.

*(b) Both rows.*

| | bit | dog | man | the |
|---|---:|---:|---:|---:|
| `the dog bit the man` | 1 | 1 | 1 | 2 |
| `the man bit the dog` | 1 | 1 | 1 | 2 |

*(c) Same or different?* **Identical, cell for cell.** Subtract them and every column gives 0.

*(d) What was lost, and one situation where it would matter.*

**Full marks:**

> *"The rows record which words are in the sentence and how many times each one appears. They do not record the order, so there is nowhere in either row that says which animal did the biting — subtract the rows and you get zero in all four columns. For sorting these into 'about animals' it does not matter at all, because both are about animals. For working out who to prosecute it matters completely, because the two sentences accuse different parties."*

**Marking notes.** **Prediction in pen is the point of the page.** Most students predict "different" and that is the correct thing to have predicted from a human reading. **What earns credit is part (d) naming a task where it matters and a task where it does not** — the answer "it always matters" is wrong, and so is "it never matters".

## Workbook sections, in workbook order

*Values below are the ones in the workbook's own Answers section, re-run for this guide: the corpus is `CORPUS_60` from the Prep Checklist, and every count, shape, percentage and variance was recomputed and agrees.*

### ✅ Warm-Up (last week's material)

- **W1.** `s = (6.0 − 2.0) ÷ 6.0 = 4.0 ÷ 6.0 = 0.6667`. The bigger of the two is `b`, so divide by 6, not 2. **Yes, in the right cluster** — three times further from the other cluster than from its own.
- **W2.** `381.1 ÷ 97.2 = 3.9`, **so k = 3.**
- **W3.** It licenses **averaging the per-point scores inside one cluster** to find the weakest cluster; a per-cluster mean is comparable with the whole-set number only because the two are the same average.
- **W4.** `0.2849 ÷ 0.0776 = 3.7` times the floor, so the clustering is finding real structure, not what any random cloud would give.
- **W5.** (a) the raw one, `0.5711`. (b) the standardised one, ARI `0.8975`. (c) The silhouette measures how cleanly separated the clusters are in whatever space you clustered in; it does not measure whether they correspond to anything real.

> **Marking tip:** W2 and W4 want an actual division written out. An arrow on a chart is not a vote; a division is.

### 🔢 Do the Maths by Hand

**M1.** Vocabulary (seven): `and, chips, cold, hot, pizza, the, was` — eight means a repeat was counted.

| | and | chips | cold | hot | pizza | the | was | **row total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **t1** | 1 | 1 | **2** | 0 | 1 | 0 | 0 | **5** |
| **t2** | 1 | 1 | 0 | **2** | 1 | 0 | 0 | **5** |
| **t3** | 0 | 0 | 1 | 0 | 1 | 1 | 1 | **4** |
| **column total** | 2 | 2 | 3 | 2 | 3 | 1 | 1 | **14** |

(c) Row totals 5, 5, 4 (each the token count); `5 + 5 + 4 = 14`; column totals also 14. (d) shape `(3, 7)` · cells `3 × 7 = 21` · non-zero 12 · empty 9 · `9 ÷ 21 = 42.86%`. (e) **Two** columns, `cold` and `hot`.

**M2.** (a) `60 × 92 = 5,520`; `5,520 − 363 = 5,157`; `5157 ÷ 5520 = 0.9342` → **93.42%**. (b) `20,000 × 50,000 = 1,000,000,000`; non-zero ≈ `20,000 × 120 = 2,400,000`; empty `= 99.76%`. (c) `1,000,000,000 ÷ 2,400,000 = 416.67` → about **417 times**. (d) No — that is what text looks like, and it gets emptier as data is added, because each new word adds a whole column of zeros for every earlier review.

**M3.** (a) `17 − 15 = 2`. (b) **The number of repeats** — the extra counts in cells holding more than 1 (d3's `great`, d4's `cold`). (c) `22 − 19 = 3`: e2's `cold`, e3's `great`, e5's `again`. (d) `385 − 363 = 22` cells hold more than 1, and the biggest number anywhere is **2** (the run prints 22 cells equal to 2, none of 3 or more).

**M4.** (a) `(55 + 34 + 26 + 11 + 10) ÷ 5 = 136 ÷ 5 = 27.2`. (b) distances `+27.8, +6.8, −1.2, −16.2, −17.2`; squares `772.84, 46.24, 1.44, 262.44, 295.84`. (c) sum of squares **1,378.80** · `÷ 4 = 344.70` · `sd = √344.70 = 18.5661`. (d) mean `81 ÷ 4 = 20.25` · variance `412.75 ÷ 3 = 137.5833` · sd `11.7296`. (e) `and` is an outlier: dropping it cut the sd from 18.57 to 11.73. That is next week's problem in Week 29's language.

### 🔎 Predict the Output

**P1.**

```text
vocab: ['chips' 'cold' 'pizza' 'the' 'was' 'zebra']
shape: (2, 6)
type : csr_matrix
nnz  : 7 of 12
[[1 0 1 0 0 2]
 [0 1 1 1 1 0]]
```

`Zebra` is last because the column order is **alphabetical**, not the order typed. Its cell is 2 (said twice, and lowercasing made `Zebra` and `zebra` one token). `7 = 3 + 4` stored cells.

**P2.**

```text
split  : ['I', 'paid', '$12.50', 'for', 'a', '9/10', 'pizza']
regex  : ['paid', '12', '50', 'for', '10', 'pizza']
no r   : []
```

Without the `r`, Python reads `\b` as the **backspace character**, the pattern matches nothing, and `[]` comes back with no error. An empty list from a pattern is almost always a missing `r`. (`$12.50` became `12` and `50`; `9/10` became `10`.)

**P3.**

```text
vocabulary: ['cold' 'great' 'pizza']
[[1 0 0]
 [0 0 0]]
getnnz: [1 0]
```

`chips` is not in the vocabulary, so `transform` silently drops it. **No error was raised for the second review**, and a model given that row will still predict confidently from nothing.

**P4.**

```text
X.shape             : (60, 92)
type(total).__name__: matrix
total.shape         : (1, 92)
after ravel         : (92,)
first five          : [ 2  2 55  2  4]
```

The missing `1` is a **row**: `X.sum(axis=0)` returns a one-row grid, not a flat list. `.ravel()` flattens it to `(92,)` before `np.argsort` or `total[i]`. The first five are `again 2, an 2, and 55, arrived 2, awful 4`.

### ✍️ Practice Set A

**A1.** token **(iii)** · tokenization **(iv)** · normalization **(vii)** · stopword **(v)** · bag-of-words **(vi)** · document-term matrix **(i)** · sparse matrix **(ii)**.

**A2.** (a) **s2's `summer`** — `"Summer nights, summer days"`. (b) Three cells hold 1, 1 and 2, which add to 4. (c) s1 gives 5 (`dancing, in, the, summer, rain`), s2 adds 2 (`nights, days`), s3 adds 3 (`on, empty, street`): `5 + 2 + 3 = 10`. (d) Today `summer` (3); with a thousand more titles, **`the`**. (e) `(30 − 13) ÷ 30 = 17 ÷ 30 = 56.67%` empty.

**A3.** (1) Missing `r`: `\b` is a backspace, so it prints `[]` with no error. (2) `counts` is sparse, so pandas sees four rows and one column; fix `counts.toarray()`. (3) The vocabulary was fitted on all sixty, including the held-out fifteen: Week 3's leak. **Crashes: (2). Still wrong in six months: (3).**

**A4 (labelled figure).** Missing cells: **d1 `great` = 1 · d2 `cold` = 1 · d3 `great` = 2 · d4 `cold` = 2**. Row totals **4, 4, 4, 5**. shape `(4, 8)` · cells 32 · stored (`nnz`) 15 · empty `17 ÷ 32 = 53%`. The two 2s are d3's `great` and d4's `cold`, each because the word appears twice in that review.

**A5.** `raw.split()` **(ii)** · `raw.lower().split()` **(iv)** · the regex **(i)** · the stopword filter **(iii)**. The non-word token is **`wasn`**, in lists **(i)** and **(iii)** (the two regex ones).

**A6.** (a) After: documents **61** · vocabulary **97** · cells **5917** · non-zero **368** · empty **93.78**. (b) Each new word adds a whole column (61 cells) with only one number in it, so the grid grew by 397 cells and only 5 got a number. (c) `rude` — and the grid does nothing about that preference; `and` simply has 5.5 times as much of it.

### ✍️ Practice Set B

Expected results; students' code will differ. Full reference programs are in the workbook's Answers section.

- **B1.** `vocabulary size: 92`.
- **B2.** Four lines of lengths **9, 9, 9, 5**; the nonsense token is **`weren`** (lines 3 and 4). The last line, `['delivery', 'late', 'chips', 'weren', 'hot']`, sounds like a good review of a complaint.
- **B3.** Corner cell **22** (twice over: rows and columns agree), then `cells: 50  stored: 19  empty: 62%`. TOTAL column `4 5 4 4 5`; TOTAL row `2 2 3 4 2 2 3 2 1 1`. Watch out for `pd.DataFrame(counts, ...)` without `.toarray()`.
- **B4.** Any pair with the same words in a different order and a different meaning. Difference all zeros, last line `True`. (Reference: `"the driver was rude and the food was cold"` versus `"the food was rude and the driver was cold"`.)
- **B5.** Two report lines:

```text
first 50: 50 documents, 87 words, 4350 cells, 305 stored, 93.0% empty
all 60: 60 documents, 92 words, 5520 cells, 363 stored, 93.4% empty
```

Top five both times: `and 47/55, the 31/34, was 23/26, cold 8/11, rude 7/10`. Then **a refusal for `"nobody answered my telephone"`** and `4 of its words have a column` for `"the chips were cold"`. Vocabulary growing from 87 to 92 is the evidence for M2(b).

### 🐞 Fix the Broken Program

- **Bug 1 (`NotFittedError`).** The vectorizer has not learned a vocabulary yet. **Fix:** move the `print` after `fit_transform` and print `len(terms)`.
- **Bug 2 (`(4, 1)` versus `(4, 92)`).** `(4, 1)` is what pandas sees in a sparse matrix (four opaque row objects); `(4, 92)` is what the index and the 92 column names promise. **Fix:** `counts[:4].toarray()`.
- **Bug 3 (the silent one).** (a) `counts = cv.fit_transform(CORPUS_60)` (vocabulary saw all sixty) and the "10 held-out reviews never seen: 0" line cannot both be honest — the zero is a definition, not a measurement; `train` is declared and never used. (b) `CORPUS_60` → `train` in the `fit_transform` line. (c) vocabulary size **87**, unknown words **6** (`would, not, here, again` from `"i would not order from here again"`; `again` from `"late again and a cold bag"`; `unfair`). (d) **`not`** — two weeks on, a sentiment model will answer `"not fresh and not hot"` as positive because `not` has no column.

> **Marking tip:** a student who says "the fix is to print the number" has missed Bug 3. The point is which rows the vocabulary was fitted on.

### 🧩 Puzzle of the Week

(a) **Five** tokens (`the dog bit the man`). (b) `120 ÷ 2 = 60` orderings. (c) Readable ones: `the dog bit the man`, `the man bit the dog`, `the dog the man bit` (borderline grammatical), `the man the dog bit` (as in "the man the dog bit is in hospital"); only a handful of the sixty are English at all. (d) `the dog bit the man` and `the man bit the dog`. (e) `720 ÷ (2 × 2) = 180` orderings. (f) The model has been given one row standing for all N sentences equally; what distinguishes them is information it does not have — **absent, not damaged.**

### 🤔 Think Deeper

**T1 (same loss as flattening in Week 24).** A strong answer has four moves. **Same shape of loss:** flattening 8×8 to 64 numbers lost "next to"; counting words lost "neighbouring words", and nothing warns you in either case. **Week 24's repair:** a convolution, which looks at each pixel with its neighbours. **Text equivalent:** n-grams (`not fresh` as a token), Week 33's first experiment. **Why harder:** a 3×3 kernel has the same nine neighbours everywhere, whereas 92 words have `92² = 8,464` possible pairs (50,000 words give two and a half billion), and a pair needs to have occurred in training to have a column. A convolution generalises across positions; an n-gram does not generalise across words.

**T2 (who owns `CountVectorizer`'s silent defaults).** Full credit for resisting both easy positions ("the default is wrong"; "read the documentation") and for landing on a design with its cost named. The answer worth arguing for is **visibility** (a one-line note of what was lowercased and dropped), with the counter-argument that warnings which fire on every correct use get silenced. Whatever the library does, printing your own vocabulary and reading it is what actually protects you.

### 🛠️ Build It — pages 31.4 to 31.7

These are the four numbered workbook pages and the marked homework. Their answers follow, and they match the workbook's own Answers section.

### Page 31.4 — Six sentences, by hand and by regex

*The six:*

```text
s1 = "It wasn't GREAT, but it wasn't bad :-)"
s2 = "Call me on 555-0134 or email me@example.com!!"
s3 = "The US economy vs. us as consumers"
s4 = "I paid $12.50 for a 9/10 pizza"
s5 = "Don't order the so-called deep-pan"
s6 = "A+ service, 5 stars, 100% would order again"
```

**By hand — what a person would say the words are** (this is `.split()`, which is the honest stand-in for "how a human chunks it"):

```text
s1: ['It', "wasn't", 'GREAT,', 'but', 'it', "wasn't", 'bad', ':-)']
s2: ['Call', 'me', 'on', '555-0134', 'or', 'email', 'me@example.com!!']
s3: ['The', 'US', 'economy', 'vs.', 'us', 'as', 'consumers']
s4: ['I', 'paid', '$12.50', 'for', 'a', '9/10', 'pizza']
s5: ["Don't", 'order', 'the', 'so-called', 'deep-pan']
s6: ['A+', 'service,', '5', 'stars,', '100%', 'would', 'order', 'again']
```

**By regex —** `re.findall(r"\b\w\w+\b", s.lower())`, real output:

```text
s1 ( 7): ['it', 'wasn', 'great', 'but', 'it', 'wasn', 'bad']
s2 (10): ['call', 'me', 'on', '555', '0134', 'or', 'email', 'me', 'example', 'com']
s3 ( 7): ['the', 'us', 'economy', 'vs', 'us', 'as', 'consumers']
s4 ( 6): ['paid', '12', '50', 'for', '10', 'pizza']
s5 ( 7): ['don', 'order', 'the', 'so', 'called', 'deep', 'pan']
s6 ( 6): ['service', 'stars', '100', 'would', 'order', 'again']
```

**Every disagreement, with a verdict. A full-marks page has all of these or most of them:**

| # | The disagreement | Verdict |
|---|---|---|
| s1 | `wasn't` → `wasn`, twice, and both `t`s dropped | **The regex is wrong for sentiment.** `wasn't` is a negation and `wasn` is a nonsense token. It is fine for topic classification, where the negation is irrelevant. |
| s1 | `:-)` disappears completely | **Wrong for sentiment, badly.** That emoticon is the clearest signal in the sentence and it is now not in the data at all. |
| s1 | `GREAT,` → `great`, so the shouting is gone | **Wrong for abuse detection**, where capitals are evidence. Fine for topic. |
| s2 | `555-0134` → `555` and `0134` | **Wrong for anything that cares about the number.** A phone number has become two meaningless integers. |
| s2 | `me@example.com` → `me`, `example`, `com`, and now `me` appears **twice** | **Wrong, and sneakily so.** The token `me` has been double-counted, so the count for `me` is 2 when the person said it once. |
| s3 | `US` → `us`, identical to the pronoun `us`, which is also in the sentence | **Wrong, and this is the best one on the page.** The country and the pronoun are now the same token, and the regex reports `us` twice. The whole sentence was built on that distinction. |
| s4 | `$12.50` → `12` and `50` | **Wrong if price matters.** The currency, the decimal point and the amount are all gone. |
| s4 | `9/10` → `10`, and the `9` is dropped | **Wrong, and worse than it looks.** A rating of nine out of ten has become the single number 10. |
| s4 | `I` and `a` vanish | **Usually fine** — both are near-useless for topic and sentiment. **Fatal on maths text**, where every `x` disappears. |
| s5 | `Don't` → `don` | **Wrong for sentiment**, same reason as s1. |
| s5 | `so-called` → `so` + `called`, `deep-pan` → `deep` + `pan` | **Debatable, and the honest answer is "it depends".** `deep` and `pan` are arguably useful separately. `so-called` carries scorn that `so` and `called` do not, so that one is a loss. |
| s6 | `A+` → nothing at all | **Wrong.** `A+` was a rating and it has been deleted, because `A` is one letter and `+` is not a word character. |
| s6 | `5` dropped, `100%` → `100` | **`5` dropped is wrong** if it was "5 stars"; `100%` → `100` is harmless here. |

**Marking notes.** **The verdicts are the objective, not the token lists.** Full marks needs, for each disagreement, *which one is right* **and** *for what task*. **"The regex is wrong" scores nothing; "the regex is wrong for sentiment and fine for topic" scores everything.** The three that must be spotted: `wasn't → wasn`, the `US`/`us` collision, and `$12.50 → 12, 50`. **A student who spots that `me@example.com` makes `me` appear twice has noticed something most adults miss — say so.**

### Page 31.5 — Five reviews, fifty cells

*The five:*

```text
e1: "The chips were cold."
e2: "Cold pizza and cold chips."
e3: "Great chips, great pizza!"
e4: "The pizza was late."
e5: "Late again, and cold again."
```

**Vocabulary — ten terms, alphabetical:** `again, and, chips, cold, great, late, pizza, the, was, were`

**The full matrix, real output:**

| | again | and | chips | cold | great | late | pizza | the | was | were | row total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **e1** | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | **4** |
| **e2** | 0 | 1 | 1 | **2** | 0 | 0 | 1 | 0 | 0 | 0 | **5** |
| **e3** | 0 | 0 | 1 | 0 | **2** | 0 | 1 | 0 | 0 | 0 | **4** |
| **e4** | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | **4** |
| **e5** | **2** | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | **5** |
| **column total** | 2 | 2 | 3 | 4 | 2 | 2 | 3 | 2 | 1 | 1 | **22** |

**The checks:**

- Row totals: 4, 5, 4, 4, 5 — and each matches the number of tokens in that review. ✅
- 4 + 5 + 4 + 4 + 5 = 22, and the column totals also sum to 22. ✅
- Cells: 5 × 10 = **50**. Non-zero: **19**. Empty: 50 − 19 = **31**, and 31 ÷ 50 = **62%**.

**Three cells hold a 2:** e2's `cold`, e3's `great`, e5's `again`. All for the same reason — the word is in the review twice.

**Marking notes.** **Fifty digits, fifty ticks, and the two total rows.** If the row totals do not match the token counts, **hand it back with only the mismatched row circled and no other comment** — the student can and should find it themselves, and finding your own arithmetic mistake is the skill. The 62% is worth asking about: **it is higher than the four-review grid's 53%, and that is the point — more documents means emptier, not fuller.**

### Page 31.6 — One normalization choice that would be wrong

*Find one normalization choice that would be wrong for your own sixty reviews, and prove it with a sentence pair from your corpus.*

**Full marks, version one — the negation case:**

> *"The choice: dropping stopwords, with `not` on the list. Most published stopword lists have `not` on them.*
>
> *The pair, both from my own corpus:*
>
> ```text
> "the pizza was not cold"   <- a happy customer
> "the pizza was cold"       <- an unhappy customer
> ```
>
> *Tokenized: `['the','pizza','was','not','cold']` and `['the','pizza','was','cold']`. After dropping `the`, `was` and `not`, both become `['pizza','cold']`, so both rows are `( pizza 1, cold 1 )` — identical.*
>
> *What was lost: the only word that told the two reviews apart. The model now cannot tell a happy customer from an angry one, and nothing anywhere will warn me. For working out what the review is **about** the loss is harmless — both are about a cold pizza. For working out how the writer **felt** it destroys the task completely, which is exactly the task I am doing in Week 33."*

**Full marks, version two — and praise this one louder, because it is harder to find:**

> *"The choice: lowercasing. My corpus has `"THE FOOD WAS COLD"` in it, typed in capitals because the customer was furious, and `"the food was cold"` from somebody just reporting a fact. After `.lower()` they are the identical row. The shouting was evidence about how angry the writer was, and `.lower()` deleted it. For topic classification I do not care. For deciding which complaints to escalate, the capitals were the whole signal."*

**Other acceptable pairs:** a price (`"a £12 pizza"` and `"a £120 pizza"` both become `['12']` and `['120']`, which survives — but `"$12.50"` and `"$1250"` both become `12`/`50` and `1250`, and the first is now indistinguishable from a review about 12 pizzas and 50 minutes); a hyphen (`"deep-pan"` and `"deep pan"` become the same two tokens, which is usually fine); an emoticon (`"the food was cold :-)"` — sarcasm — and `"the food was cold"` become identical rows).

**Marking notes.** **The bar is one sentence pair, written out in full, from their own corpus.**

- ✅ Full marks: two reviews, both token lists, both rows, and one sentence naming what was lost **and** one task where it matters and one where it does not.
- ✅ Level 5: a pair that does **not** use `not`. Negation is the example from the lesson; finding a second route shows the principle landed.
- ✅ Also level 5: noticing that the loss is task-dependent and saying so explicitly — *"harmless for topic, fatal for sentiment"*.
- ❌ Zero on this page: *"stopwords can be bad"*, *"lowercasing loses information"*, or any general statement with no sentence attached. **Hand it back once with one question written on it: "show me the two reviews."**

### Page 31.7 — Stretch: a review made of unknown words

*What happens when you transform a review none of whose words are in the vocabulary?*

```python
from sklearn.feature_extraction.text import CountVectorizer

train = ["cold pizza", "great pizza"]
cv = CountVectorizer()
cv.fit(train)
print("vocabulary:", cv.get_feature_names_out())
print("a review made of known words   :", cv.transform(["cold chips"]).toarray())
print("a review made of unknown words :",
      cv.transform(["nobody answered my phone"]).toarray())
print("non-zero entries in each row   :",
      cv.transform(["cold chips", "nobody answered my phone"]).getnnz(axis=1))
```

**Real output:**

```text
vocabulary: ['cold' 'great' 'pizza']
a review made of known words   : [[1 0 0]]
a review made of unknown words : [[0 0 0]]
non-zero entries in each row   : [1 0]
```

**The full answer:**

**Nothing happens. That is the alarming part.** You get a row of zeros, no error, no warning. A model handed that row will still produce a prediction — whatever its default lean is — and it will still report a confidence, and the confidence will be meaningless, because the model saw nothing at all.

**Notice also that `"cold chips"` gave `[[1 0 0]]`.** The word `chips` is not in the vocabulary either, so it was silently dropped; only `cold` survived. **So a half-unknown review is quietly half-ignored and there is no line in the output that says so.**

**The defence is one line and almost nobody writes it:**

```python
if X.getnnz(axis=1)[0] == 0:
    print("refusing to predict: none of these words is in the vocabulary")
```

**Marking notes.** Full marks is the row of zeros **plus** the sentence *"and it will still predict something, with a confidence, and the confidence is a lie."* **A student who proposes the `getnnz` check, or any check, before being shown it is at level 5** — this is a real production failure mode and refusing to predict is a genuinely mature engineering instinct.

### 🎨 Draw It

A full-marks drawing has **two arrows meeting at one row**: two opposite sentences (`the pizza was not cold` and `the pizza was cold`, or the student's own) pointing into a single `pizza 1, cold 1`. Around it: the bill of three lost things, each with an example (word order with `dog bit man = man bit dog`; negation with `good` and `not good`; what-modifies-what with `cheap phone, great camera = great phone, cheap camera`); the sparsity as a rectangle with a small shaded corner labelled `363 stored of 5,520 cells = 93.4% empty`; and **a column with a `0` beside a word with no column at all**, labelled as two different situations. A drawing that shows only the conversion diagrams a function; one that shows what fell out diagrams an idea.

### 📊 Self-Check

Self-assessed, no marks. For any 😕, send the student back as follows.

| Row | Go to |
|---|---|
| tokenizing, the regex, the missing `r` | the chapter's Step 1 and Break 3, then P2 |
| building the matrix, checking cells | the chapter's Part A, then M1 and page 31.5 |
| shapes, `nnz`, `.toarray()` | the chapter's Steps 2–4, then P4 and Bug 2 |
| sparsity and why it grows | the chapter's Trick 4, then M2 and A6 |
| word order, and what it costs | the chapter's Part B, then the Puzzle and B4 |
| a zero versus no column | the chapter's Trick 1, then P3 and page 31.7 |
| a vocabulary fitted on the test rows | Bug 3, then Week 3's pipeline |

### Answers to every question posed in the lesson

**Hook — "what number is `cold`?"** **There isn't one.** There is no number that `cold` *is*, which is why somebody had to invent a way to make one — and the way they invented is to count.

**Hook — "give me one reason this is a terrible idea."** The two best answers are **word order** (`"the dog bit the man"`) and **`the` is in everything and tells you nothing**. The first is this week's wrap; the second is next week's title.

**Concept — "cut at every space. How many pieces?"** **Eight.** And the two spaces before `But` count as one break.

**Concept — "how many different tokens for the word `the`?"** **Two:** `The` and `the`. Half the evidence each.

**Concept — "better. What is still wrong?"** `great!!` still carries its exclamation marks, so it is a different token from `great`.

**Concept — "two things changed. One is good. What is the other one?"** **`wasn't` became `wasn`**, and the negation has become a nonsense token.

**Concept — "`the pizza was not cold`. What survives the stopword list?"** `pizza`, `cold`. **"And `the pizza was cold`?"** `pizza`, `cold`. **Identical rows for two opposite reviews.**

**Concept — "how many different words in the four reviews?"** **Eight:** `and, cold, food, great, pizza, service, the, was`.

**Live-code step 2 — "it wanted one thing and got another. What did it want?"** **A collection of documents.** It was given one string. `ValueError: Iterable over raw text documents expected, string object received.` The fix is brackets.

**Live-code step 2 — "who decided the column order?"** **`CountVectorizer` did, alphabetically.** So column 3 is `great` for the rest of the term, and `get_feature_names_out()` is the only way to find that out.

**Live-code step 3 — "it thinks I handed it four rows and one column. Why one?"** Because a sparse matrix is not a grid. It holds **fifteen** numbers, not thirty-two, and pandas cannot unpack it without `.toarray()`.

**Live-code step 4 — "what went wrong?"** **Nothing crashed**, which is the problem. Without the `r`, Python read `\b` as a backspace character, the pattern matched nothing, and `re.findall` honestly reported `[]`.

**Live-code step 5 — "sixty reviews, ninety-two words. How many cells?"** **5,520.** **"And how many have a number in them?"** **363** — so 5,157 are empty, which is **93.4%**.

**Wrap — "somebody tell me what is wrong with that."** The two rows are identical although the sentences mean opposite things. **Subtract them and every column is 0.**

**Wrap — "where is the information about who did the biting?"** **Nowhere.** It is not stored. It was thrown away on purpose the moment we decided to count words.

**Wrap — "one of those three you can nearly patch. Which, and how?"** **Word order**, by counting **pairs** of adjacent words as well as single words. That is an n-gram, it arrives in Week 33, and it works less well than anybody expects.

**Activity — "which two rows are most alike?"** **d1 and d2** — `"The pizza was great!"` and `"The pizza was cold."` — because they share `the`, `pizza` and `was`, three of their four words. **Hold on to that answer: those two reviews are a happy customer and an unhappy one, and next week you measure exactly how similar the method thinks they are.**

---

## 🔮 Next Week Preview

This section previews next week and what to prepare early.

Next week fixes the complaint somebody made in the first ten minutes of today: **`and` appeared 55 times in the corpus and `rude` appeared 10, and the grid treats them exactly the same way.** The repair is one multiplication and one division, and it is called **TF-IDF** — how often a word appears **here**, multiplied by how rare it is **everywhere else**. The student computes one weight all the way by hand — `tf` of 2, times an `idf` of `ln(5 ÷ 3) + 1 = 1.510826`, giving `3.021651`, then divided by the row's length of `3.592917` to give `0.841002` — and then `TfidfVectorizer` prints `0.841002` and nobody is allowed to move on until the two agree to four decimal places. Then the week's one new piece of maths: **cosine similarity**, the dot product of two lists divided by both their lengths, worked by hand on two three-number lists and read as an **angle** rather than a score. And then the result that should annoy them: the two most similar reviews in their own corpus turn out to be `"the coffee was hot and the cake was fresh"` and `"the coffee was cold and the cake was stale"` — one happy, one furious, 37.1 degrees apart, and the two words that carry all the meaning contribute exactly nothing.

**To prep early:** three things. **One — THE VOCABULARY wall sheet stays up**, and a second one goes beside it headed **IDF**, with the eight words down the side and three blank columns: `df`, `ln(...)`, `idf`. It gets filled in live. **Two — every student needs a calculator that does natural logarithms**, a phone calculator is fine, and **check tonight that yours gives `ln(5 ÷ 3) = 0.510826`** — a calculator set to `log` base 10 gives `0.221849` and a student using one will conclude the lesson is wrong. **Three — check the student's own sixty reviews are on disk and run**, because next week's last ten minutes finds the closest pair in their corpus and it is the best moment of the week.
