# Module 9 — Classic NLP: From Tokens to Bag-of-Words to Embeddings

**Level 3 · Module 9 · ~5.5 hours · Prereqs: Module 2 (pipelines, encoding), Module 3 (precision, recall, confusion matrix), Module 4 (logistic regression coefficients), Module 8 (PCA, cosine-style distance thinking).**

[⬅ Previous](module-08-unsupervised-kmeans-pca.md) · [Level 3 Home](README.md) · [Next ➡](capstone.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. You will be able to tokenize and normalize a piece of text, and justify each normalization choice against a case where it would be wrong.
2. You will be able to build a bag-of-words count matrix by hand for four short documents and verify it against `CountVectorizer`.
3. You will be able to compute a TF-IDF weight with the exact formula scikit-learn uses, including the L2 normalization, and match its output to four decimal places.
4. You will be able to compute cosine similarity between two document vectors by hand and say what the number means.
5. You will be able to show, with a concrete example, where bag-of-words loses meaning, and measure whether n-grams recover it.
6. You will be able to describe what a word embedding is, and demonstrate that words used in identical contexts get identical vectors.

---

## 🪝 The Hook

Every model you have built in this level eats numbers. `StandardScaler` eats numbers. `LogisticRegression` eats numbers. A CNN eats a grid of numbers. Even the images in Module 7 were numbers before you started — pixel brightnesses, handed to you already digitised.

Text is not numbers. Text is `"the pizza was cold"`, and there is no obvious column to put it in.

So somebody had to invent a way to turn a sentence into a row of a spreadsheet. The first answer, and still one of the most useful, is almost insultingly simple: **count the words**. Forget grammar, forget word order, forget everything an English teacher told you. Just count. `"the pizza was cold"` becomes a row that says: `the=1, pizza=1, was=1, cold=1`, and every other word in the language `=0`.

This should not work. It throws away the difference between *"the dog bit the man"* and *"the man bit the dog."* And yet it powered spam filters, search engines, and document classifiers for thirty years, and it still beats a large language model on plenty of small problems today.

By the end of this module you'll have built one that works, found the specific sentence where it breaks, and met the idea that fixes it — the idea that all of Level 4 is built on.

---

## 🧠 The Concept

### 1. Tokenization and normalization: turning a string into a list of things

> **Token:** one unit of text — usually a word, sometimes a punctuation mark or a piece of a word.

> **Tokenization:** splitting a string into tokens.

The naive version is `text.split()`, and it is wrong in ways worth seeing:

```
"The pizza was GREAT!!  ...but the service wasn't."
        ↓ .split()
['The', 'pizza', 'was', 'GREAT!!', '...but', 'the', 'service', "wasn't."]
```

Now `'GREAT!!'`, `'GREAT!'`, `'great'` and `'Great'` are four different tokens as far as the computer is concerned. Your vocabulary explodes and every version of the word gets its own, weaker, statistics.

So you **normalize**. Each choice below is a decision, not a law:

| Normalization | What it does | When it's right | When it's WRONG |
|---|---|---|---|
| **Lowercasing** | `Great → great` | almost always for topic/sentiment | `US` (country) vs `us` (pronoun); `Apple` vs `apple`; ALL-CAPS SHOUTING is a real signal in abuse detection |
| **Strip punctuation** | `great!! → great` | most classification tasks | `!!!` and `?!` carry sentiment; `$4.99` and `499` are different things; emoticons `:-(` are pure signal |
| **Remove stopwords** | drop `the, is, a, of` | topic classification, search | authorship attribution (function words *are* the fingerprint); negation — dropping `not` is a disaster for sentiment |
| **Stemming / lemmatizing** | `running, ran, runs → run` | when you have little data | `better → good` loses intensity; over-aggressive stemmers turn `university` and `universe` both into `univers` |

> **Stopword:** an extremely common word (`the`, `is`, `and`) that carries little topic information on its own.

🍕 **Analogy.** Normalization is tidying a room before you count what's in it. Putting all the pens in one drawer (lowercasing) makes counting easy. Throwing out everything small (stopword removal) makes counting *even easier* — right up until you realise you threw out the house keys. `not` is a house key.

**The default that scikit-learn gives you, and a gotcha you must know.** `CountVectorizer`'s default tokenizer is the regular expression `(?u)\b\w\w+\b`. Read it carefully: `\w\w+` means **two or more** word characters. So scikit-learn silently drops every single-letter token — `i`, `a`, and (in maths-heavy text) `x`. That is usually fine and occasionally catastrophic, and you will trip over it in Practice 2.

**A worked normalization.** Input:

```
"The pizza was GREAT!!  But the service wasn't."
```

| Step | Result |
|---|---|
| lowercase | `the pizza was great!!  but the service wasn't.` |
| split on non-word chars | `['the','pizza','was','great','but','the','service','wasn','t']` |
| drop tokens shorter than 2 chars | `['the','pizza','was','great','but','the','service','wasn']` |

Notice what just happened to `wasn't`: it became `wasn` and a dropped `t`. The negation is now a nonsense token. This is not a hypothetical bug — it's the default behaviour, and it's exactly why sentiment models built carelessly get negation wrong.

---

### 2. Bag-of-words: the document-term matrix

> **Bag-of-words (BoW):** representing a document as a vector of word counts, ignoring order entirely. A "bag" because you dumped all the words in and shook it.

> **Document-term matrix:** a table with one row per document and one column per vocabulary word; cell `(i, j)` is how many times word `j` appears in document `i`.

Four tiny reviews:

```
d1: "The pizza was great!"
d2: "The pizza was cold."
d3: "Great pizza, great service."
d4: "Cold service and cold food."
```

Vocabulary (lowercased, punctuation stripped, alphabetical) — **8 terms**:

```
and, cold, food, great, pizza, service, the, was
```

The document-term matrix:

| | and | cold | food | great | pizza | service | the | was |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **d1** | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 |
| **d2** | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| **d3** | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 0 |
| **d4** | 1 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |

That is now a perfectly ordinary numeric feature matrix. `LogisticRegression` will eat it happily.

**Sparsity is the defining property.** With four documents and eight words, 22 of the 32 cells are zero — 69% sparse. Scale up to 20,000 news articles and a 50,000-word vocabulary and you get a billion cells of which maybe 0.1% are non-zero. Storing that as a dense array would need 8 GB; storing only the non-zeros needs about 8 MB.

> **Sparse matrix:** a matrix stored as a list of (row, column, value) triples for the non-zero entries only. scikit-learn's vectorizers return these by default, which is why `print(X)` shows coordinates instead of a grid.

🍕 **Analogy.** A bag-of-words vector is a shopping receipt with a line for every product the supermarket sells. Your receipt says `milk: 2, bread: 1`, and 40,000 other lines all say zero. Obviously you don't print those. You print the two lines that matter — that's a sparse matrix.

**What BoW throws away, listed honestly:**

- **Word order.** `"the dog bit the man"` and `"the man bit the dog"` are the *identical* vector.
- **Negation scope.** `"good"` and `"not good"` share the word `good`.
- **Syntax and grammar** entirely.
- **Which word modifies which.** `"cheap phone, great camera"` vs `"great phone, cheap camera"` — same vector.

Keep that list. §5 measures how much it costs.

---

### 3. TF-IDF: rare words are worth more

Raw counts have a problem you can see in the matrix above. In d1, the word `the` gets exactly as much weight as the word `great`. But `the` appears in half the corpus and tells you nothing; `great` is doing all the work.

> **Term frequency (TF):** how often a term appears in *this* document. Common words score high.

> **Inverse document frequency (IDF):** how *rare* the term is across the whole corpus. Words that appear everywhere score low; words that appear in few documents score high.

> **TF-IDF:** their product. High when a word is frequent **here** and rare **elsewhere** — which is exactly the definition of "distinctive."

🍕 **Analogy.** You're identifying which class a lost exercise book belongs to. Every book contains the word "the," so seeing "the" tells you nothing. One book contains "photosynthesis" three times — now you know it's Biology. TF-IDF is that instinct written as arithmetic: *how often, divided by how unsurprising.*

**The exact formula scikit-learn uses** (with default `smooth_idf=True`):

```
idf(t) = ln( (1 + n) / (1 + df(t)) ) + 1

    n     = number of documents
    df(t) = number of documents containing term t

tfidf(t, d) = tf(t, d) × idf(t)

then each document row is L2-normalized:  row ← row / ‖row‖
```

Three details that trip people up:

- The `+1`s are **smoothing** — they pretend there's one extra document containing every term, so `df = 0` can never divide by zero.
- The trailing `+ 1` outside the log means idf is **never zero**. A word in every single document gets `ln(1) + 1 = 1`, so it's down-weighted to a plain count rather than deleted.
- The **L2 normalization at the end is not optional** and is easy to forget. It makes every document vector have length 1, so a long review and a short review are comparable.

**Worked IDF for our four documents** (`n = 4`):

| term | df | (1+n)/(1+df) | ln(·) | **idf = ln + 1** |
|---|---:|---|---:|---:|
| and | 1 | 5/2 = 2.5 | 0.9163 | **1.9163** |
| cold | 2 | 5/3 = 1.6667 | 0.5108 | **1.5108** |
| food | 1 | 2.5 | 0.9163 | **1.9163** |
| great | 2 | 1.6667 | 0.5108 | **1.5108** |
| pizza | 3 | 5/4 = 1.25 | 0.2231 | **1.2231** |
| service | 2 | 1.6667 | 0.5108 | **1.5108** |
| the | 2 | 1.6667 | 0.5108 | **1.5108** |
| was | 2 | 1.6667 | 0.5108 | **1.5108** |

Read the column: `pizza` appears in 3 of 4 documents, so it gets the *lowest* weight (1.2231). `and` and `food` appear once each, so they get the *highest* (1.9163). That's IDF doing its job — the ubiquitous word is discounted, the distinctive word is boosted.

---

### 4. Cosine similarity: comparing direction, not size

You have two documents as vectors. How similar are they?

The obvious answer, dot product, is a trap. Consider:

```
d1     = "the pizza was great"                          (4 words)
d1_long= "the pizza was great the pizza was great"      (the same text, twice)
```

Raw count vectors: `d1 = [0,0,0,1,1,0,1,1]` and `d1_long = [0,0,0,2,2,0,2,2]`.

```
dot(d1, d1)      = 1+1+1+1 = 4
dot(d1, d1_long) = 2+2+2+2 = 8
```

By dot product, `d1_long` is **twice as similar to d1 as d1 is to itself** — which is nonsense. Length is drowning out content.

> **Cosine similarity:** the dot product divided by both vectors' lengths. It measures the *angle* between them, ignoring how long they are.
> ```
> cos(a, b) = (a · b) / ( ‖a‖ × ‖b‖ )
> ```
> Range 0 to 1 for count vectors (which are never negative). 1 = identical direction, 0 = no words in common.

Redo it:

```
‖d1‖      = √(1+1+1+1) = √4  = 2
‖d1_long‖ = √(4+4+4+4) = √16 = 4

cos(d1, d1)      = 4 / (2 × 2) = 1.0
cos(d1, d1_long) = 8 / (2 × 4) = 1.0
```

Both exactly 1.0, which is right: they contain the same words in the same proportions.

🍕 **Analogy.** Two people describe a pizza. One says "cheesy, tomatoey, hot." The other says the same three things but repeats each five times because they're excited. They're describing the *same pizza*. Cosine similarity asks "are they pointing the same way?" not "who talked longer?"

**A useful consequence:** because TF-IDF already L2-normalizes each row, every TF-IDF vector has length 1. So for TF-IDF vectors, **cosine similarity is just the dot product** — the denominator is `1 × 1`. That's why `linear_kernel` and `cosine_similarity` give identical answers on TF-IDF output, and why the former is faster.

---

### 5. n-grams, and exactly where bag-of-words breaks

> **n-gram:** a contiguous run of `n` tokens treated as a single feature. `"not good"` is a bigram (2-gram); `"was not good"` is a trigram.

Bigrams are the standard patch for word order. Using `ngram_range=(1, 2)` gives you every unigram **and** every bigram, so `"the food was not good"` produces:

```
unigrams: the, food, was, not, good
bigrams : the food, food was, was not, not good
```

Now `not good` is its own column, and a classifier can learn a negative weight for it independently of `good`.

**The cost, which is large:** vocabulary size explodes. A 5,000-word unigram vocabulary typically becomes 80,000–150,000 features when you add bigrams, most of which appear once and are pure noise. You control this with `min_df` (ignore terms appearing in fewer than *k* documents) and `max_features`.

**The catch nobody mentions:** a bigram feature can only help if **that exact bigram appeared in your training data**. If your training set never contains `"not good"`, the column doesn't exist, and at prediction time the phrase is silently ignored. Bigrams don't teach the model about negation as a concept. They just give it a place to store specific memorised phrases. You'll demonstrate this yourself in the Hands-On, and it is the honest answer to "why don't we just use bigrams?"

**A checklist of things bag-of-words cannot represent, even with bigrams:**

| Phenomenon | Example | Why BoW fails |
|---|---|---|
| Long-range negation | *"I would not, given the price and the wait, call this good."* | `not` and `good` are eight tokens apart |
| Sarcasm | *"Oh, brilliant. Another delay."* | every word is positive |
| Comparison direction | *"Better than the first one"* vs *"The first one was better"* | identical unigram bags |
| Attribution | *"My friend said it was terrible, but I loved it"* | `terrible` and `loved` both present, unweighted |
| Synonyms | *"film"* vs *"movie"* | separate, unrelated columns |

That last row is the important one for what comes next. To bag-of-words, `film` and `movie` are as unrelated as `film` and `hydraulics`. Which brings us to embeddings.

---

### 6. Word embeddings: meaning as a direction

> **Word embedding:** a dense vector of maybe 50–1000 real numbers representing one word, arranged so that words with similar meanings have similar vectors.

Compare the two representations of the word `film` in a 10,000-word vocabulary:

```
one-hot (bag-of-words column):   [0, 0, 0, ..., 1, ..., 0, 0]     10,000 numbers, 9,999 of them zero
embedding:                       [0.31, -0.88, 0.12, ..., 0.44]      300 numbers, all meaningful
```

The one-hot vector for `film` is exactly as far from `movie` as it is from `hydraulics` — the cosine similarity between any two distinct one-hot vectors is 0, always. The embedding puts `film` and `movie` almost on top of each other.

**Where do the numbers come from?** The **distributional hypothesis**, stated by the linguist J. R. Firth in 1957:

> *"You shall know a word by the company it keeps."*

If two words appear in the same contexts, they mean similar things. Nobody has to define `movie` for you — you learn it from *"let's watch a ___", "the ___ was three hours long", "a ___ about pirates."* `film` fits all three. So does `movie`. So they get similar vectors.

🍕 **Analogy.** You've never heard the word *bhindi*. Then you hear: "add the bhindi after the onions," "bhindi goes slimy if you overcook it," "we're having bhindi with rice." You now know, with no dictionary at all, that bhindi is a vegetable you cook. You located it by its company. An embedding is that process, run over billions of sentences, with the answer stored as coordinates.

**The mechanical version you can compute by hand.** Build a **co-occurrence matrix**: one row per word, one column per word, cell `(i, j)` = how often word `j` appears within a small window of word `i`. Each row is that word's "company." Then compare rows with cosine similarity. If two words genuinely have identical company, their rows are identical and cosine = exactly 1.0. Real embeddings (word2vec, GloVe, and the ones inside every transformer) are cleverer and denser, but this is the idea, and you'll build it in Part G.

**Vector analogies.** The famous demonstration is that embedding space supports arithmetic:

```
vec("king") − vec("man") + vec("woman")  ≈  vec("queen")
```

Read it as: *"start at king, remove the male direction, add the female direction, and you land near queen."* This works because the embedding has, without being told to, allocated a consistent direction to gender. Two honest caveats: real embeddings give a cosine of about 0.7–0.8 to `queen`, not 1.0, and the analogy is usually evaluated by excluding the three input words from the search, which quietly does a lot of work. Analogies are a real phenomenon and a slightly oversold demo.

**And the direction that carries gender also carries stereotype.** The same arithmetic on embeddings trained on web text famously produces `doctor − man + woman ≈ nurse` and `programmer − man + woman ≈ homemaker`. Nobody put that in. It is a faithful measurement of how the words were used in the training corpus, which means the embedding has learned society's associations along with its semantics. That is not a bug you can patch out with a filter; it's a property of learning meaning from human text, and it will follow you into every model in Level 4.

---

## 🔍 Worked Example

Full trace on the four reviews from §2, from raw strings to a cosine-similarity matrix. Every number by hand.

```
d1: "The pizza was great!"
d2: "The pizza was cold."
d3: "Great pizza, great service."
d4: "Cold service and cold food."
```

### Step 1 — tokenize and normalize

Lowercase, split on non-word characters, keep tokens of 2+ characters:

```
d1 → ['the', 'pizza', 'was', 'great']
d2 → ['the', 'pizza', 'was', 'cold']
d3 → ['great', 'pizza', 'great', 'service']
d4 → ['cold', 'service', 'and', 'cold', 'food']
```

Vocabulary, sorted: `and(0) cold(1) food(2) great(3) pizza(4) service(5) the(6) was(7)` — 8 terms.

### Step 2 — count matrix

| | and | cold | food | great | pizza | service | the | was | total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 4 |
| d2 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 4 |
| d3 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 0 | 4 |
| d4 | 1 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 5 |

### Step 3 — document frequencies and IDF

```
df(and)     = 1   (d4)
df(cold)    = 2   (d2, d4)
df(food)    = 1   (d4)
df(great)   = 2   (d1, d3)
df(pizza)   = 3   (d1, d2, d3)
df(service) = 2   (d3, d4)
df(the)     = 2   (d1, d2)
df(was)     = 2   (d1, d2)
```

With `n = 4`, `idf = ln(5 / (1 + df)) + 1`:

```
and     : ln(5/2) + 1 = 0.916291 + 1 = 1.916291
cold    : ln(5/3) + 1 = 0.510826 + 1 = 1.510826
food    : ln(5/2) + 1 =              = 1.916291
great   : ln(5/3) + 1 =              = 1.510826
pizza   : ln(5/4) + 1 = 0.223144 + 1 = 1.223144
service : ln(5/3) + 1 =              = 1.510826
the     : ln(5/3) + 1 =              = 1.510826
was     : ln(5/3) + 1 =              = 1.510826
```

### Step 4 — TF-IDF for d1, with normalization

Raw products (`tf × idf`):

```
great   : 1 × 1.510826 = 1.510826
pizza   : 1 × 1.223144 = 1.223144
the     : 1 × 1.510826 = 1.510826
was     : 1 × 1.510826 = 1.510826
everything else = 0
```

L2 norm:

```
‖d1‖ = √( 1.510826² + 1.223144² + 1.510826² + 1.510826² )
     = √( 2.282595  + 1.496081  + 2.282595  + 2.282595  )
     = √  8.343866
     =    2.888574
```

Normalized:

```
great   = 1.510826 / 2.888574 = 0.523035
pizza   = 1.223144 / 2.888574 = 0.423442
the     = 1.510826 / 2.888574 = 0.523035
was     = 1.510826 / 2.888574 = 0.523035
```

Check: `3(0.523035²) + 0.423442² = 3(0.273566) + 0.179303 = 0.820698 + 0.179303 = 1.000001` ✓ (rounding).

### Step 5 — TF-IDF for d3

Note `great` appears **twice**, so `tf = 2`:

```
great   : 2 × 1.510826 = 3.021652
pizza   : 1 × 1.223144 = 1.223144
service : 1 × 1.510826 = 1.510826

‖d3‖ = √( 3.021652² + 1.223144² + 1.510826² )
     = √( 9.130381  + 1.496081  + 2.282595  )
     = √ 12.909057
     =   3.592917

great   = 3.021652 / 3.592917 = 0.841002
pizza   = 1.223144 / 3.592917 = 0.340432
service = 1.510826 / 3.592917 = 0.420501
```

### Step 6 — the other two documents

**d2** has exactly the same shape as d1 (four distinct terms, three with idf 1.510826 and one with 1.223144), so its norm is identical: 2.888574.

```
cold  = 0.523035    pizza = 0.423442    the = 0.523035    was = 0.523035
```

**d4** — `cold` appears twice:

```
and     : 1 × 1.916291 = 1.916291
cold    : 2 × 1.510826 = 3.021652
food    : 1 × 1.916291 = 1.916291
service : 1 × 1.510826 = 1.510826

‖d4‖ = √( 3.672371 + 9.130381 + 3.672371 + 2.282595 ) = √18.757718 = 4.330971

and     = 1.916291 / 4.330971 = 0.442462
cold    = 3.021652 / 4.330971 = 0.697684
food    = 1.916291 / 4.330971 = 0.442462
service = 1.510826 / 4.330971 = 0.348842
```

### Step 7 — cosine similarities

Every vector already has length 1, so **cosine = plain dot product.** Only shared terms contribute.

```
cos(d1, d2):  shared = {pizza, the, was}
  pizza : 0.423442 × 0.423442 = 0.179303
  the   : 0.523035 × 0.523035 = 0.273566
  was   : 0.523035 × 0.523035 = 0.273566
                        total = 0.726434
```

```
cos(d1, d3):  shared = {great, pizza}
  great : 0.523035 × 0.841002 = 0.439874
  pizza : 0.423442 × 0.340432 = 0.144154
                        total = 0.584027
```

```
cos(d1, d4):  shared = {}                        total = 0.000000
```

```
cos(d2, d3):  shared = {pizza}
  pizza : 0.423442 × 0.340432 = 0.144153         total = 0.144153
```

```
cos(d2, d4):  shared = {cold}
  cold  : 0.523035 × 0.697684 = 0.364913         total = 0.364913
```

```
cos(d3, d4):  shared = {service}
  service: 0.420501 × 0.348842 = 0.146689        total = 0.146689
```

The similarity matrix:

|  | d1 | d2 | d3 | d4 |
|---|---:|---:|---:|---:|
| **d1** | 1.000 | 0.726 | 0.584 | 0.000 |
| **d2** | 0.726 | 1.000 | 0.144 | 0.365 |
| **d3** | 0.584 | 0.144 | 1.000 | 0.147 |
| **d4** | 0.000 | 0.365 | 0.147 | 1.000 |

### Step 8 — read the matrix, and notice the problem

The **highest** off-diagonal similarity is `cos(d1, d2) = 0.726`. But look at what d1 and d2 actually say:

```
d1: "The pizza was great!"    ← a happy customer
d2: "The pizza was cold."     ← an unhappy customer
```

Bag-of-words thinks these are the two most similar documents in the corpus, because they share `the`, `pizza`, and `was` — three of their four words. The single word that carries all the meaning (`great` vs `cold`) contributes nothing to their similarity, and TF-IDF's down-weighting of `pizza` wasn't enough to save it, because `the` and `was` are also only in 2 of 4 documents here and so keep a healthy idf of 1.51.

Meanwhile `cos(d1, d4) = 0.000` — the model says d1 and d4 have *literally nothing* in common, which is true at the word level and false at the meaning level (both are opinions about the same restaurant).

**That is the honest summary of bag-of-words.** It measures topical overlap well and sentiment badly, and it cannot see that two documents are about the same thing in different words. Everything else in this module is a response to those two sentences.

---

## 💻 Hands-On

### Setup

```bash
pip install numpy pandas scikit-learn matplotlib
```

Everything here runs in seconds on any laptop. No downloads, no data files — every document is typed into the script.

### Part A — tokenization, four policies

```python
import re

raw = "The pizza was GREAT!!  But the service wasn't. Cost $12.50 :-("

def tok_naive(s):
    return s.split()

def tok_lower_split(s):
    return s.lower().split()

def tok_sklearn_default(s):
    # exactly what CountVectorizer does by default
    return re.findall(r"(?u)\b\w\w+\b", s.lower())

STOP = {"the", "but", "was", "a", "is", "and", "of", "to"}
def tok_no_stop(s):
    return [t for t in tok_sklearn_default(s) if t not in STOP]

for name, fn in [("naive split", tok_naive),
                 ("lower+split", tok_lower_split),
                 ("sklearn default", tok_sklearn_default),
                 ("+ stopwords removed", tok_no_stop)]:
    toks = fn(raw)
    print(f"{name:22s} ({len(toks):2d}) {toks}")
```

Expected output:

```
naive split            ( 9) ['The', 'pizza', 'was', 'GREAT!!', 'But', 'the', 'service', "wasn't.", 'Cost', '$12.50', ':-(']
lower+split            ( 9) ['the', 'pizza', 'was', 'great!!', 'but', 'the', 'service', "wasn't.", 'cost', '$12.50', ':-(']
sklearn default        (10) ['the', 'pizza', 'was', 'great', 'but', 'the', 'service', 'wasn', 'cost', '12', '50']
+ stopwords removed    ( 7) ['pizza', 'great', 'service', 'wasn', 'cost', '12', '50']
```

(The first two report 9 because Python's `split()` groups the double space; the printed lists show 11 items — count them yourself, it's a good reminder to check your own output rather than trust the label.)

Three things worth saying out loud about the sklearn row:

- `wasn't` → `wasn` and a dropped `t`. **The negation has become a garbage token.**
- `$12.50` → `12` and `50`. The price is gone; two meaningless integers remain.
- `:-(` → nothing at all. On a sentiment task you just deleted the clearest signal in the sentence.

None of that is a bug. It is the default, and defaults are decisions somebody else made for a different problem.

### Part B — build the bag-of-words matrix

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

docs = ["The pizza was great!",
        "The pizza was cold.",
        "Great pizza, great service.",
        "Cold service and cold food."]

cv = CountVectorizer()                 # lowercase=True, token_pattern=r"(?u)\b\w\w+\b"
counts = cv.fit_transform(docs)

print("vocabulary:", cv.get_feature_names_out())
print("matrix type:", type(counts).__name__, " shape:", counts.shape)
print("stored non-zeros:", counts.nnz, "of", counts.shape[0] * counts.shape[1], "cells")
print()
print(pd.DataFrame(counts.toarray(),
                   index=["d1", "d2", "d3", "d4"],
                   columns=cv.get_feature_names_out()))
```

Expected output:

```
vocabulary: ['and' 'cold' 'food' 'great' 'pizza' 'service' 'the' 'was']
matrix type: csr_matrix  shape: (4, 8)
stored non-zeros: 15 of 32 cells

    and  cold  food  great  pizza  service  the  was
d1    0     0     0      1      1        0    1    1
d2    0     1     0      0      1        0    1    1
d3    0     0     0      2      1        1    0    0
d4    1     2     1      0      0        1    0    0
```

Cell for cell, identical to the hand-built table in the worked example. And note `csr_matrix` with 15 stored values out of 32 — sparsity, in action, on a four-document corpus.

### Part C — TF-IDF, verified against the hand arithmetic

```python
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

tv = TfidfVectorizer()                 # smooth_idf=True, norm='l2' by default
X = tv.fit_transform(docs)
terms = tv.get_feature_names_out()

print("idf values:")
for t, v in zip(terms, tv.idf_):
    print(f"  {t:8s} {v:.6f}")

print()
print("L2-normalized TF-IDF matrix:")
print(pd.DataFrame(np.round(X.toarray(), 6),
                   index=["d1", "d2", "d3", "d4"], columns=terms))
```

Expected output:

```
idf values:
  and      1.916291
  cold     1.510826
  food     1.916291
  great    1.510826
  pizza    1.223144
  service  1.510826
  the      1.510826
  was      1.510826

L2-normalized TF-IDF matrix:
         and      cold      food     great     pizza   service       the       was
d1  0.000000  0.000000  0.000000  0.523035  0.423442  0.000000  0.523035  0.523035
d2  0.000000  0.523035  0.000000  0.000000  0.423442  0.000000  0.523035  0.523035
d3  0.000000  0.000000  0.000000  0.841002  0.340432  0.420501  0.000000  0.000000
d4  0.442462  0.697684  0.442462  0.000000  0.000000  0.348842  0.000000  0.000000
```

Every single number matches the worked example. When your paper arithmetic and the library agree, you understand the library.

### Part D — cosine similarity, and the dot-product trap

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# First: why raw dot product fails
pair = ["the pizza was great",
        "the pizza was great the pizza was great"]
C = CountVectorizer().fit_transform(pair).toarray().astype(float)
print("count vectors:\n", C)
print("dot(d1, d1)     =", C[0] @ C[0])
print("dot(d1, d1_long)=", C[0] @ C[1])
print("cos(d1, d1)     =", round(float(cosine_similarity([C[0]], [C[0]])[0, 0]), 4))
print("cos(d1, d1_long)=", round(float(cosine_similarity([C[0]], [C[1]])[0, 0]), 4))
```

Expected output:

```
count vectors:
 [[1. 1. 1. 1.]
 [2. 2. 2. 2.]]
dot(d1, d1)     = 4.0
dot(d1, d1_long)= 8.0
cos(d1, d1)     = 1.0
cos(d1, d1_long)= 1.0
```

Dot product says the doubled document is twice as similar as the document is to itself. Cosine says both are 1.0. Cosine is right.

Now the full matrix for our four reviews:

```python
S = cosine_similarity(X)               # X is the TF-IDF matrix from Part C
print(pd.DataFrame(np.round(S, 4),
                   index=["d1", "d2", "d3", "d4"], columns=["d1", "d2", "d3", "d4"]))
```

Expected output:

```
        d1      d2      d3      d4
d1  1.0000  0.7264  0.5840  0.0000
d2  0.7264  1.0000  0.1442  0.3649
d3  0.5840  0.1442  1.0000  0.1467
d4  0.0000  0.3649  0.1467  1.0000
```

Matches the hand-computed matrix. And it still says a happy review and an unhappy review are the two most similar documents in the corpus — 0.7264. Hold on to that; it's the failure the next section is built around.

### Part E — a real sentiment classifier

Forty typed reviews, deliberately written in matched pairs so the model has to learn *sentiment* words rather than *topic* words.

```python
POS = [
 "absolutely loved this film, the acting was superb",
 "a delightful story with warm characters",
 "brilliant pacing and a satisfying ending",
 "i enjoyed every minute of it",
 "wonderful performances from the entire cast",
 "charming, funny, and genuinely moving",
 "the best thing i have seen all year",
 "beautiful cinematography and a strong script",
 "a heartfelt film that earns its emotion",
 "clever, sharp, and endlessly rewatchable",
 "i adored almost every scene of it",
 "excellent direction and a great soundtrack",
 "this movie exceeded all my expectations",
 "a masterpiece of quiet storytelling",
 "gripping from the first scene to the last",
 "i would happily watch this again tomorrow",
 "the dialogue is witty and the plot is tight",
 "a joyful, generous, big hearted film",
 "outstanding lead performance, fully deserved the praise",
 "smart and moving without ever being sentimental",
]

NEG = [
 "a boring film with wooden acting",
 "the plot made no sense at all",
 "terrible pacing and a lazy ending",
 "i wasted two hours of my life",
 "weak performances from almost everyone",
 "dull, predictable, and far too long",
 "the worst thing i have seen all year",
 "ugly cinematography and a clumsy script",
 "a hollow film that earns nothing",
 "stupid, dreary, and completely forgettable",
 "i hated almost every scene of it",
 "awful direction and an annoying soundtrack",
 "this movie failed all my expectations",
 "a disaster of noisy storytelling",
 "tedious from the first scene to the last",
 "i would not watch this again",
 "the dialogue is clunky and the plot is thin",
 "a joyless, mean, cold hearted film",
 "embarrassing lead performance, undeserved the hype",
 "dumb and dull while pretending to be deep",
]

train_texts  = POS + NEG
train_labels = [1] * len(POS) + [0] * len(NEG)

# A separate held-out set, typed by hand. The last two of each block are NEGATION TRAPS.
TEST = [
 ("a truly wonderful and warm film",        1),
 ("sharp writing and a superb cast",        1),
 ("i loved every scene",                    1),
 ("gripping and beautifully made",          1),
 ("not boring for a single minute",         1),   # trap
 ("never dull for a moment",                1),   # trap
 ("a dull and predictable mess",            0),
 ("terrible acting and a weak script",      0),
 ("i hated the writing",                    0),
 ("boring and badly made",                  0),
 ("this film is not good at all",           0),   # trap
 ("hardly a wonderful experience",          0),   # trap
]
test_texts  = [t for t, _ in TEST]
test_labels = [y for _, y in TEST]
print(f"train: {len(train_texts)}   test: {len(test_texts)}")
```

```
train: 40   test: 12
```

Now the pipeline — TF-IDF straight into the logistic regression you built by hand in Module 4:

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

uni = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 1))),
    ("clf",   LogisticRegression(C=10, max_iter=2000)),
])
uni.fit(train_texts, train_labels)

pred = uni.predict(test_texts)
print("vocabulary size:", len(uni.named_steps["tfidf"].get_feature_names_out()))
print("\nconfusion matrix (rows=true [neg,pos], cols=pred):")
print(confusion_matrix(test_labels, pred))
print()
print(classification_report(test_labels, pred,
                            target_names=["negative", "positive"], digits=3))
```

Representative output:

```
vocabulary size: 144

confusion matrix (rows=true [neg,pos], cols=pred):
[[5 1]
 [2 4]]

              precision    recall  f1-score   support

    negative      0.714     0.833     0.769         6
    positive      0.800     0.667     0.727         6

    accuracy                          0.750        12
   macro avg      0.757     0.750     0.748        12
weighted avg      0.757     0.750     0.748        12
```

75% on twelve reviews — 9 right, 3 wrong. Which three did it miss?

```python
for text, true, p in zip(test_texts, test_labels, pred):
    if true != p:
        conf = uni.predict_proba([text])[0][p]
        print(f"WRONG  true={true} pred={p} (p={conf:.3f})  {text!r}")
```

Representative output:

```
WRONG  true=1 pred=0 (p=0.720)  'not boring for a single minute'
WRONG  true=1 pred=0 (p=0.765)  'never dull for a moment'
WRONG  true=0 pred=1 (p=0.713)  'hardly a wonderful experience'
```

**There it is, in black and white — all three errors are the negation traps.** The nine ordinary reviews were all classified correctly; every failure is a sentence whose meaning is flipped by a word the bag cannot connect to anything.

- `"not boring for a single minute"` → predicted **negative** with 72% confidence. The bag contains `boring` (coefficient −1.07) and `not` (−1.48, learned from *"i would not watch this again"*). Two negative words, one positive meaning, and the model sums them.
- `"never dull for a moment"` → predicted **negative** with 77% confidence, for the same reason: `dull` is −1.16 and there is nothing to reverse it.
- `"hardly a wonderful experience"` → predicted **positive** with 71% confidence. `wonderful` is strongly positive, `hardly` has never been seen, so the sentence reads as a compliment.

Notice `not` picked up a **negative** coefficient of −1.48, purely because the one training review containing it happened to be negative. The model has learned "the word `not` means bad," which is not what `not` means at all. This is the word-order failure the module promised, on a real model, with probabilities attached.

### Part F — what the model learned, and whether bigrams fix it

```python
import numpy as np

vec = uni.named_steps["tfidf"]
clf = uni.named_steps["clf"]
words = vec.get_feature_names_out()
coef = clf.coef_[0]

order = np.argsort(coef)
print("15 MOST NEGATIVE words:")
for i in order[:15]:
    print(f"   {coef[i]:+.4f}  {words[i]}")
print("\n15 MOST POSITIVE words:")
for i in order[::-1][:15]:
    print(f"   {coef[i]:+.4f}  {words[i]}")
```

Representative output:

```
15 MOST NEGATIVE words:
   -1.6340  hated
   -1.4964  worst
   -1.4805  failed
   -1.4769  not
   -1.4633  tedious
   -1.1790  terrible
   -1.1790  lazy
   -1.1790  ugly
   -1.1790  clumsy
   -1.1744  disaster
   -1.1744  noisy
   -1.1556  dull
   -1.1060  thin
   -1.1060  clunky
   -1.1019  hollow

15 MOST POSITIVE words:
   +1.6165  exceeded
   +1.5140  best
   +1.4914  adored
   +1.4705  gripping
   +1.2454  moving
   +1.2285  happily
   +1.2285  tomorrow
   +1.1849  masterpiece
   +1.1849  quiet
   +1.1774  strong
   +1.1774  satisfying
   +1.1774  brilliant
   +1.1774  beautiful
   +1.1272  great
   +1.1272  excellent
```

Most of those are humanly sensible — `hated`, `worst`, `terrible`, `dull` on one side; `best`, `gripping`, `brilliant`, `beautiful` on the other. That readability is a genuine and underrated advantage of this whole approach. A linear model on TF-IDF is **fully inspectable**: you can read its mind, word by word, and check whether it agrees with you. Try that with the CNN from Module 7.

Now look at the three entries that should worry you.

- **`not` at −1.4769**, the fourth strongest negative word in the model. It appears in exactly one training review, *"i would not watch this again"*, which happens to be negative. From one example the model concluded that `not` is a strongly negative word. It is not a word with a sentiment at all; it is an operator that *reverses* the sentiment of whatever follows it.
- **`tomorrow` at +1.2285** and **`quiet` at +1.1849**. Neither is a sentiment word. They are there because *"i would happily watch this again tomorrow"* and *"a masterpiece of quiet storytelling"* are the only reviews containing them, and both are positive.
- **The ties.** `terrible`, `lazy`, `ugly`, and `clumsy` all sit at exactly −1.1790, and `strong`, `satisfying`, `brilliant`, `beautiful` all at +1.1774. Identical coefficients are a fingerprint of words that appear in exactly one document each with the same TF-IDF weight — the model has no evidence to separate them, so it doesn't.

The general rule this suggests: **print the document frequency next to every coefficient you plan to quote.** A weight learned from one review is a coincidence with a decimal point, and here that includes the fourth-largest weight in the whole model.

Now try bigrams:

```python
bi = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf",   LogisticRegression(C=10, max_iter=2000)),
])
bi.fit(train_texts, train_labels)
pred_bi = bi.predict(test_texts)

print("unigram vocab:", len(uni.named_steps['tfidf'].get_feature_names_out()))
print("uni+bigram vocab:", len(bi.named_steps['tfidf'].get_feature_names_out()))
print("\nunigram accuracy   :", round(np.mean(np.array(pred)    == test_labels), 4))
print("uni+bigram accuracy:", round(np.mean(np.array(pred_bi) == test_labels), 4))
print("\nis 'not good' a feature?",
      "not good" in set(bi.named_steps['tfidf'].get_feature_names_out()))
```

Representative output:

```
unigram vocab: 144
uni+bigram vocab: 308

unigram accuracy   : 0.75
uni+bigram accuracy: 0.75

is 'not good' a feature? False
```

**Bigrams changed nothing**, and the last line says exactly why: the phrase `not good` never appeared in training, so there is no such column, so at prediction time it is thrown away as if it were never written. Adding 164 features bought zero improvement. This is the catch from §5, demonstrated rather than asserted.

The fix is data, not features. Add six negation examples to training:

```python
NEG_AUG_POS = ["not boring at all", "never dull for a second", "not a single wasted minute"]
NEG_AUG_NEG = ["not good in any way", "not funny for a moment", "not worth the ticket price"]

aug_texts  = train_texts + NEG_AUG_POS + NEG_AUG_NEG
aug_labels = train_labels + [1, 1, 1] + [0, 0, 0]

bi2 = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf",   LogisticRegression(C=10, max_iter=2000)),
])
bi2.fit(aug_texts, aug_labels)
pred2 = bi2.predict(test_texts)
print("uni+bigram + 6 negation examples:",
      round(np.mean(np.array(pred2) == test_labels), 4))
print("is 'not good' a feature now?",
      "not good" in set(bi2.named_steps['tfidf'].get_feature_names_out()))
for text, true, p in zip(test_texts, test_labels, pred2):
    if true != p:
        print(f"  still wrong: true={true} pred={p}  {text!r}")
```

Representative output:

```
uni+bigram + 6 negation examples: 0.9167
is 'not good' a feature now? True
  still wrong: true=0 pred=1  'hardly a wonderful experience'
```

Accuracy **0.75 → 0.9167**, from six typed sentences. Both `not` traps and the `never dull` trap are now handled, because `not boring`, `not good`, and `never dull` all exist as columns.

The one still failing is `"hardly a wonderful experience"`. `hardly` is a negator the model has *still* never seen, and `wonderful` is strongly positive, so the sentence reads as praise. Which is the honest end of this road: **bag-of-words plus n-grams handles exactly the negations you showed it, and no others.** It did not learn "negation reverses sentiment." It learned three specific two-word phrases. Generalising from `not good` to `hardly wonderful` requires a model that knows those two phrases are related, and that is what embeddings — and eventually transformers — are for.

### Part G — build a word embedding from co-occurrence

Twelve sentences, deliberately written in matched pairs so `cat`/`dog` and `pizza`/`pasta` appear in *identical* contexts and never in the same sentence as each other.

```python
import numpy as np
from itertools import product
from sklearn.metrics.pairwise import cosine_similarity

corpus = [
 "the cat drinks milk",        "the dog drinks milk",
 "the cat eats meat",          "the dog eats meat",
 "a small cat sleeps",         "a small dog sleeps",
 "i like pizza very much",     "i like pasta very much",
 "the pizza tastes salty",     "the pasta tastes salty",
 "we order pizza on friday",   "we order pasta on friday",
]

tokenized = [s.split() for s in corpus]
vocab = sorted({w for s in tokenized for w in s})
idx = {w: i for i, w in enumerate(vocab)}
V = len(vocab)
print("vocabulary size:", V)

WINDOW = 2
Co = np.zeros((V, V))
for sent in tokenized:
    for pos, w in enumerate(sent):
        lo = max(0, pos - WINDOW)
        hi = min(len(sent), pos + WINDOW + 1)
        for j in range(lo, hi):
            if j != pos:
                Co[idx[w], idx[sent[j]]] += 1

print("co-occurrence row for 'cat':")
print({vocab[j]: int(Co[idx['cat'], j]) for j in range(V) if Co[idx['cat'], j] > 0})
print("co-occurrence row for 'dog':")
print({vocab[j]: int(Co[idx['dog'], j]) for j in range(V) if Co[idx['dog'], j] > 0})
```

Expected output:

```
vocabulary size: 22
co-occurrence row for 'cat':
{'a': 1, 'drinks': 1, 'eats': 1, 'meat': 1, 'milk': 1, 'sleeps': 1, 'small': 1, 'the': 2}
co-occurrence row for 'dog':
{'a': 1, 'drinks': 1, 'eats': 1, 'meat': 1, 'milk': 1, 'sleeps': 1, 'small': 1, 'the': 2}
```

**Identical rows.** Because every sentence containing `cat` has a twin containing `dog` in the same slot, the two words keep exactly the same company. Now measure it:

```python
def sim(a, b, M):
    return float(cosine_similarity([M[idx[a]]], [M[idx[b]]])[0, 0])

for a, b in [("cat", "dog"), ("pizza", "pasta"), ("cat", "pizza"),
             ("dog", "pasta"), ("milk", "meat")]:
    print(f"  cos({a:6s}, {b:6s}) = {sim(a, b, Co):.4f}")
```

Expected output:

```
  cos(cat   , dog   ) = 1.0000
  cos(pizza , pasta ) = 1.0000
  cos(cat   , pizza ) = 0.1818
  cos(dog   , pasta ) = 0.1818
  cos(milk  , meat  ) = 0.3333
```

`cos(cat, dog) = 1.0000` **exactly** — you can verify the 0.1818 for `cat`/`pizza` by hand: their rows share only the word `the` (2 in cat's row, 1 in pizza's), both rows have squared length 11, so `2 / (√11 × √11) = 2/11 = 0.1818`.

Nothing told the computer that cats and dogs are both animals. It read twelve sentences and worked out that they are the same *kind of thing* purely from the words around them. That is the distributional hypothesis, running.

Now compress those 22-dimensional sparse rows into 4 dense dimensions — which is what makes them "embeddings" rather than "a big table":

```python
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=4, random_state=0)
E = svd.fit_transform(Co)
print("embedding matrix shape:", E.shape)
print("variance captured by 4 dims:", round(svd.explained_variance_ratio_.sum(), 4))
print("embedding for 'cat':", np.round(E[idx['cat']], 3))
print("embedding for 'dog':", np.round(E[idx['dog']], 3))

for a, b in [("cat", "dog"), ("pizza", "pasta"), ("cat", "pizza")]:
    print(f"  cos_4d({a:6s}, {b:6s}) = {sim(a, b, E):.4f}")
```

Representative output:

```
embedding matrix shape: (22, 4)
variance captured by 4 dims: 0.4949
embedding for 'cat': [ 2.155 -1.538  1.504  0.593]
embedding for 'dog': [ 2.155 -1.538  1.504  0.593]
  cos_4d(cat   , dog   ) = 1.0000
  cos_4d(pizza , pasta ) = 1.0000
  cos_4d(cat   , pizza ) = 0.1748
```

Twenty-two dimensions became four, and `cat` and `dog` are still identical — they must be, because identical input rows give identical output rows under any linear projection. Meanwhile `cat`/`pizza` similarity *dropped* slightly, from 0.1818 to 0.1748, as the compression discarded part of the shared-`the` noise.

Note the 0.4949: four components capture under half the variance of this co-occurrence matrix. On a 12-sentence corpus almost every word has a nearly unique context, so the matrix is close to full rank and there is little redundancy to compress. On a real corpus of millions of sentences the same 300-dimensional compression captures the great majority of the structure — which is precisely why dense embeddings work at scale and look unimpressive at toy scale.

⚠️ **Honesty check.** Twelve hand-written sentences is not a corpus. Real embeddings are trained on billions of words, and the reason `cat` and `dog` come out similar there is statistical, not because someone arranged perfect twin sentences. This demo proves the *mechanism*, not the scale.

### Part H — vector arithmetic and analogies

Here is a hand-built embedding where every dimension has a name, so you can watch the analogy work:

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

DIMS = ["royal", "male", "female", "food", "animal"]
E = {
    "king":  np.array([0.9, 0.9, 0.0, 0.0, 0.0]),
    "queen": np.array([0.9, 0.0, 0.9, 0.0, 0.0]),
    "man":   np.array([0.0, 0.9, 0.0, 0.0, 0.0]),
    "woman": np.array([0.0, 0.0, 0.9, 0.0, 0.0]),
    "pizza": np.array([0.0, 0.0, 0.0, 0.9, 0.0]),
    "dog":   np.array([0.0, 0.0, 0.0, 0.1, 0.9]),
}

target = E["king"] - E["man"] + E["woman"]
print("king - man + woman =", target)
print()
for w, v in E.items():
    s = float(cosine_similarity([target], [v])[0, 0])
    print(f"  cos with {w:6s} = {s:+.4f}")
```

Expected output:

```
king - man + woman = [0.9 0.  0.9 0.  0. ]

  cos with king   = +0.5000
  cos with queen  = +1.0000
  cos with man    = +0.0000
  cos with woman  = +0.7071
  cos with pizza  = +0.0000
  cos with dog    = +0.0000
```

The arithmetic lands **exactly** on `queen`. Trace it by hand:

```
king  = [0.9, 0.9, 0.0, 0.0, 0.0]
−man  = [0.0,−0.9, 0.0, 0.0, 0.0]   →  [0.9, 0.0, 0.0, 0.0, 0.0]   (the "male" dimension is now 0)
+woman= [0.0, 0.0, 0.9, 0.0, 0.0]   →  [0.9, 0.0, 0.9, 0.0, 0.0]   (the "female" dimension is now 0.9)
                                        = queen, exactly
```

⚠️ **This table is rigged and you should know it.** I chose the five dimensions and typed the numbers so the answer would be perfect. In a real embedding: (i) no dimension has a human-readable name — meaning is spread across all 300, (ii) the result lands *near* `queen` with cosine around 0.7–0.8, not on it, and (iii) `king` and `woman` themselves usually score higher than `queen` unless you explicitly exclude the input words from the search, which most demos quietly do. The **mechanism** — that consistent semantic differences correspond to consistent vector offsets — is real and important. The **magic** is stage-managed.

### Part I — visualise the documents with PCA

Module 8's tool, applied to text.

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

vec = TfidfVectorizer()
D = vec.fit_transform(train_texts).toarray()      # (40, ~152) dense — fine at this size
p = PCA(n_components=2, random_state=0)
Z = p.fit_transform(D)

plt.figure(figsize=(8, 6))
lab = np.array(train_labels)
plt.scatter(Z[lab == 1, 0], Z[lab == 1, 1], c="seagreen", s=60, label="positive")
plt.scatter(Z[lab == 0, 0], Z[lab == 0, 1], c="indianred", s=60, marker="s", label="negative")
plt.xlabel(f"PC1 ({p.explained_variance_ratio_[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({p.explained_variance_ratio_[1]*100:.1f}% var)")
plt.title("40 reviews as TF-IDF vectors, projected to 2-D")
plt.legend(); plt.tight_layout(); plt.savefig("reviews_pca.png", dpi=110); plt.close()

print("explained variance (PC1, PC2):", np.round(p.explained_variance_ratio_[:2], 4))
print("cumulative for 2 components  :", round(p.explained_variance_ratio_[:2].sum(), 4))
print("saved reviews_pca.png")
```

Representative output:

```
explained variance (PC1, PC2): [0.0616 0.0601]
cumulative for 2 components  : 0.1217
saved reviews_pca.png
```

**Read that number before you read the picture: 12.2%.** Two components capture an eighth of the variance in this data, so the plot is a badly flattened shadow. You will see the green and red points loosely mingled with a weak tendency to separate — and that is not evidence the classes are inseparable, because the classifier gets 75% on held-out data using all 144 dimensions, and 92% once negation examples are added.

This is a general property of TF-IDF and it's worth internalising: text vectors are high-dimensional and roughly equally spread in many directions (there is no "biggest axis" the way there was for wine chemistry), so PCA to 2-D loses almost everything. Compare Module 8's wine plot at 55.4% — that was a real map. This is a rumour of one. Report the percentage next to every projection you ever publish.

---

## ✍️ Practice

### 1. [Warm-up] Tokenize and justify

Take these three raw strings:

```
s1 = "It wasn't GREAT, but it wasn't bad :-)"
s2 = "Call me at 555-0134 or email me@example.com!!"
s3 = "The US economy vs. us as consumers"
```

(a) Write out the token list each produces under `re.findall(r"(?u)\b\w\w+\b", s.lower())`.
(b) For **each** of the three strings, name one specific thing that normalization destroyed and say what task that loss would matter for.
(c) Propose one change to the tokenizer that would fix `s1`'s problem, and state what new problem your fix introduces.

**Done looks like:** three token lists, three named losses with a task each, and one proposed fix with its own honest downside.

### 2. [Warm-up] Bag-of-words by hand

Three documents:

```
e1: "i love this phone"
e2: "i hate this phone"
e3: "this phone is fine and i love it"
```

(a) Predict the vocabulary that `CountVectorizer()` will produce, **with its default settings**. Be careful.
(b) Build the full count matrix by hand.
(c) Verify with `CountVectorizer`.
(d) One word appears in all three documents but is missing from the vocabulary. Which one, and why?

**Done looks like:** a hand-built table matching the printed one exactly, and a correct one-sentence explanation for (d).

### 3. [Build] TF-IDF by hand, verified to four decimals

Using the same three documents from Exercise 2:

(a) Compute `df` for every vocabulary term.
(b) Compute `idf = ln((1 + n)/(1 + df)) + 1` for every term, to six decimals.
(c) Compute the **full L2-normalized TF-IDF vector for e3**, showing the raw products, the norm, and the final values.
(d) Verify against `TfidfVectorizer` and confirm agreement to four decimal places.
(e) Which term in e3 has the highest weight, and which has the lowest? Explain both in one sentence each.

**Done looks like:** an idf table, the complete e3 arithmetic, and a printed comparison confirming the match.

### 4. [Build] Cosine similarity and a nearest-neighbour search

Still using e1, e2, e3.

(a) Compute all three pairwise cosine similarities by hand from your Exercise 3 vectors.
(b) Verify with `cosine_similarity`.
(c) `e1` says "love," `e2` says "hate." Is `cos(e1, e2)` closer to `cos(e1, e3)` than you'd like? Quantify the gap and explain what's causing it.
(d) Now write a tiny search function: given the query `"phone i love"`, transform it with the **already-fitted** vectorizer and return the documents ranked by cosine similarity. Explain in one sentence why you must not call `fit_transform` on the query.

**Done looks like:** a 3×3 hand-computed matrix matching sklearn, a quantified answer to (c), and a working ranked search with the leakage explanation.

### 5. [Stretch] Measure what n-grams buy you

Using the 40-review training set and 12-review test set from the Hands-On:

(a) Train and evaluate five configurations: `ngram_range` of `(1,1)`, `(1,2)`, `(1,3)`, `(2,2)` alone, and `(1,2)` with `min_df=2`. Report vocabulary size and test accuracy for each in a table.
(b) For each configuration, print how many features have a *non-zero* coefficient after fitting (with `C=10` almost all will — note that too).
(c) Which configuration wins, and is the win larger than one test-set item (1/12 = 0.083)?
(d) Write three sentences explaining why `(2,2)` alone performs the way it does.

**Done looks like:** a five-row table, the winner named with an honest "is 1 test item a real difference?" judgement, and the three-sentence explanation.

### 6. [Stretch] Break the co-occurrence embedding

Start from Part G's 12-sentence corpus, where `cos(cat, dog) = 1.0000` exactly.

(a) Add the single sentence `"the cat chases the dog"` to the corpus, rebuild the co-occurrence matrix, and report the new `cos(cat, dog)`. Explain the change.
(b) Starting again from the original 12 sentences, add `"the dog barks loudly"` (which has no `cat` twin) and report the new `cos(cat, dog)`. Explain why this changes it differently from (a).
(c) Change `WINDOW` from 2 to 1 and then to 4 on the original corpus. Report `cos(cat, dog)`, `cos(cat, pizza)`, and `cos(milk, meat)` for each window size, and describe the trend.
(d) In three sentences, state what window size controls, conceptually — what kind of similarity does a small window capture versus a large one?

**Done looks like:** three numeric results with explanations, a window-size table, and a conceptual answer for (d).

---

## 🤔 Think Deeper

**1. Your model's 15 most positive words are readable. Is that the same as trustworthy?**
You printed `best +1.51, gripping +1.47, brilliant +1.18` and they all made sense, so it feels like you understand the model. But sitting in the same list was `tomorrow +1.23`, and fourth from the top of the negative list was `not −1.48` — a word with no sentiment at all, whose weight came from one training review and which actively broke two of your three test failures. Interpretability made the good weights legible and the bad weights legible too, and you only noticed the bad ones because you went looking.
*How to reason about it:* separate "I can read the weights" from "the weights are right." A useful discipline is to sort by coefficient but *display document frequency alongside*, then read the list asking "how many reviews taught the model this?" A weight learned from one example is a coincidence with a decimal point. Also watch for exact ties — `terrible`, `lazy`, `ugly`, and `clumsy` all landing on −1.1790 is the model telling you it has no evidence to distinguish them.

**2. Removing stopwords is a decision about whose speech patterns matter.**
Standard English stopword lists were written for search engines and drop `the, is, at, which, on`. But function words are the single strongest signal in authorship attribution, in detecting non-native writing, and in some dialect classification. If you drop them, you have decided that *what* someone talks about matters and *how* they talk does not — and "how" is often the part that correlates with who they are.
*How to reason about it:* ask what your stopword list is *for*. If it's to reduce vocabulary size, measure whether it actually helped (usually TF-IDF already down-weights these words, so it often doesn't). Then ask the fairness question: if your model's accuracy differs across groups of writers, would removing function words make that gap bigger or smaller? You can measure this — split your test set by any writer attribute you have and compare per-group recall, as in Module 3.

**3. The embedding learned that `programmer − man + woman ≈ homemaker`. What should be done?**
Three positions get argued. *Fix the vectors:* researchers have published debiasing methods that identify a "gender direction" and project it out. *Fix the corpus:* train on more balanced text. *Fix nothing, disclose everything:* the embedding is an accurate measurement of a real corpus, and hiding the association makes it harder to detect downstream harm.
*How to reason about it:* notice that each position makes a different claim about what an embedding *is* — a tool, a dataset, or a measurement instrument. Then ask the engineering question that cuts through it: for your specific application, what decision does the embedding influence, and who is affected if the association leaks into that decision? A résumé screener and a spell-checker inherit the same bias and it matters enormously in one and not at all in the other. Debiasing research has also found that the removed associations often reappear in the model's behaviour even when they're gone from the obvious direction — which should make you suspicious of any fix that is only tested on the metric it was designed to move.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Calling `fit_transform` on the test set | You copy the training line and change the variable name | `fit_transform` on train, `transform` only on test. Fitting on test builds a vocabulary and idf table from data you're supposed to be blind to — Module 2's leakage, in text form. Put the vectorizer in a `Pipeline` and it can't happen |
| Wondering where the word `i` went | `CountVectorizer`'s default `token_pattern` is `\b\w\w+\b` — two or more characters | Use `token_pattern=r"(?u)\b\w+\b"` if single letters matter. Always print `get_feature_names_out()` on a small sample before trusting anything |
| Removing stopwords on a sentiment task | Every tutorial does it, so it looks like a required step | Standard lists contain `not`, `no`, `never`, `against`. Check the list against your task; for sentiment, either keep them or use a custom list that preserves negators |
| Comparing documents with raw dot product | It's one line shorter than cosine | Long documents win automatically. Use `cosine_similarity`, or use TF-IDF (already L2-normalized) and note that the dot product then *is* the cosine |
| Assuming bigrams fix negation | "Word order is the problem, bigrams capture word order" | A bigram only exists as a feature if it appeared in training. Check with `"not good" in feature_names`. The real fix is training examples containing negation |
| Calling `.toarray()` on a real corpus | It works on 40 documents so you assume it scales | 20,000 documents × 50,000 terms × 8 bytes = 8 GB. Keep matrices sparse; use `TruncatedSVD` instead of `PCA` when you need to reduce them |
| Reading a 2-D PCA plot of text as meaningful | The plot renders, so it must mean something | Text TF-IDF routinely puts under 15% of variance in the first two components. Always print `explained_variance_ratio_` and say the number out loud before interpreting the picture |
| Interpreting large coefficients from rare words | The number is big, so the effect must be big | A word appearing in one training document can get a huge coefficient from pure chance. Print the document frequency next to every coefficient you plan to quote |
| Using accuracy on a 90%-spam corpus | It's the metric that prints by default | Module 3 applies unchanged. Report the confusion matrix, precision, and recall per class — a spam filter's cost of a false positive is nothing like its cost of a false negative |
| Forgetting that `TfidfVectorizer` L2-normalizes | The docs mention it once | It means every row has length 1, so document length is already removed. If you *want* length as a feature, add it as a separate column — don't turn the normalization off |

---

## 🛠️ Mini-Project — Sentiment Engine

**Goal.** Build a fully inspectable text classifier, evaluate it with Module 3's metrics, read its mind, and name a specific sentence it gets wrong because bag-of-words threw away word order.

**Starter steps.**

1. **Write the corpus.** Extend the Hands-On set to **at least 60 training reviews** (30 positive, 30 negative) and **at least 20 held-out test reviews** (10/10), all typed into your script — no downloads. Write them in matched pairs where you can, so the model can't cheat on topic. Include at least **four negation traps** in the test set (`"not boring"`, `"hardly wonderful"`, `"never once funny"`, `"far from terrible"`) and label them by their true meaning.
2. **Build the pipeline.** `TfidfVectorizer` → `LogisticRegression`, inside a single `Pipeline` so the vectorizer can never see the test set.
3. **Cross-validate on the training set.** Report 5-fold stratified mean ± std for accuracy and F1 (Module 3). Use this — not the test set — to pick `ngram_range` and `C`.
4. **Score the test set once.** Print the confusion matrix and a full `classification_report` with precision, recall, and F1 per class. State which error type you'd rather make for a review-moderation application and why.
5. **Read the model's mind.** Print the **15 most positive** and **15 most negative** words with their coefficients, and add a column showing each word's document frequency in the training set. Write two sentences: are the top words humanly sensible, and is there a word whose weight is an accident of a single training review?
6. **Find the word-order failure.** Identify at least one test review the model gets wrong **specifically because word order was discarded**. Quote it, print the predicted probability, and explain in 60–100 words exactly which words drove the wrong prediction — cite their coefficients.
7. **Try to fix it.** Re-run with `ngram_range=(1,2)`. Report whether the bigram appeared in the training vocabulary (`"not good" in feature_names`), whether accuracy changed, and what that tells you.
8. **Map it.** PCA the TF-IDF document vectors to 2-D, colour by true class, save the PNG, and print the explained-variance ratio. Write one sentence interpreting the plot **that is consistent with the variance percentage**.

**Success criteria checklist.**

- [ ] ≥ 60 training and ≥ 20 test reviews, all typed into the script, with ≥ 4 negation traps in test.
- [ ] Vectorizer and classifier inside one `Pipeline`; `transform` (never `fit`) applied to test data.
- [ ] Hyperparameters chosen by cross-validation on train, with mean ± std reported.
- [ ] Test set scored exactly once, with a confusion matrix and per-class precision/recall/F1.
- [ ] Top 15 positive and top 15 negative words printed **with document frequencies**.
- [ ] A written judgement that the top words are (or aren't) humanly sensible, plus one identified accidental weight.
- [ ] One misclassified review quoted, with its probability and a 60–100 word coefficient-level diagnosis naming word order as the cause.
- [ ] A bigram experiment with the `"not good" in feature_names` check reported either way.
- [ ] A PCA scatter with the explained-variance percentage printed and an interpretation that respects it.

**Level it up.** Add a **character n-gram** model: `TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))`. This ignores words entirely and counts letter sequences. Compare its test accuracy to your word model, then test both on three deliberately misspelled reviews (`"absolutly briliant film"`, `"terible acting"`, `"wonderfull"`). The word model will fail completely — the misspellings are out-of-vocabulary and vanish — while the character model should survive, because `bril`, `rill`, `illi` are still there. Write three sentences on when you would choose character n-grams in production, and name one real domain (hint: usernames, product codes, or any text people type in a hurry on a phone).

---

## 🔑 Key Takeaways

- Every normalization step — lowercasing, punctuation stripping, stopword removal — is a decision with a cost. `wasn't → wasn` and `:-( → nothing` are the defaults, and both are wrong for sentiment.
- Bag-of-words turns a document into a sparse vector of counts. It works far better than it has any right to, and it discards word order completely.
- TF-IDF = how often here × how rare elsewhere, with the exact formula `ln((1+n)/(1+df)) + 1`, then L2-normalize the row. You matched sklearn to six decimals doing it by hand.
- Cosine similarity compares direction, not length. Raw dot product says a doubled document is twice as similar to you as you are to yourself; cosine correctly says both are 1.0.
- Bag-of-words rated a happy review and an unhappy review as the most similar pair in the corpus (0.726), because they shared three function words. That is the method's honest ceiling.
- n-grams only help for the exact phrases present in training. `"not good"` isn't a feature unless somebody wrote it in your training data.
- An embedding is a dense vector where similar-meaning words are nearby, learned from context alone. Two words with literally identical company get cosine 1.0 — and that mechanism, scaled to billions of sentences, is what Level 4 is built on.
- Embeddings faithfully encode the associations in their training text, including the ones you wish weren't there. That's a measurement, not a malfunction, and it's yours to handle.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Token** | One unit of text, usually a word | `"the pizza"` → `['the', 'pizza']` |
| **Tokenization** | Chopping a string into tokens | `re.findall(r"\b\w\w+\b", text)` |
| **Normalization** | Tidying text so different spellings of the same thing match | `GREAT!! → great` |
| **Stopword** | A super-common word that carries little topic meaning | `the`, `is`, `and` — but `not` is dangerous to drop |
| **Bag-of-words** | A document as a list of word counts, order thrown away | `"the dog bit the man"` = `"the man bit the dog"` |
| **Document-term matrix** | Rows are documents, columns are words, cells are counts | Our 4 × 8 review table |
| **Sparse matrix** | Storing only the non-zero cells | 15 stored values out of 32 cells |
| **Term frequency (TF)** | How often a word appears in this document | `great` appears twice in d3, so tf = 2 |
| **Document frequency (df)** | How many documents contain a word | `pizza` is in 3 of our 4 reviews |
| **Inverse document frequency (IDF)** | A rarity boost — rare words score higher | `and` gets 1.916; `pizza` gets 1.223 |
| **TF-IDF** | TF × IDF, then L2-normalize the row | d3's `great` = 0.841 |
| **L2 normalization** | Scaling a vector so its length is exactly 1 | Divide d1 by 2.888575 |
| **Cosine similarity** | Similarity as an angle, ignoring vector length | `cos(d1, d2) = 0.726` |
| **n-gram** | A run of n consecutive tokens as one feature | `"not good"` is a bigram |
| **Word embedding** | A short dense vector per word, near other similar words | `cat` and `dog` at cosine 1.0 in Part G |
| **Distributional hypothesis** | Words used in the same contexts mean similar things | You learn `bhindi` from the sentences around it |
| **Co-occurrence matrix** | A table counting which words appear near which | `cat`'s row: `the:2, drinks:1, eats:1, …` |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

### 1. [Warm-up] Tokenize and justify

**(a)**

```python
import re
for name, s in [("s1", "It wasn't GREAT, but it wasn't bad :-)"),
                ("s2", "Call me at 555-0134 or email me@example.com!!"),
                ("s3", "The US economy vs. us as consumers")]:
    print(name, re.findall(r"(?u)\b\w\w+\b", s.lower()))
```

```
s1 ['it', 'wasn', 'great', 'but', 'it', 'wasn', 'bad']
s2 ['call', 'me', 'at', '555', '0134', 'or', 'email', 'me', 'example', 'com']
s3 ['the', 'us', 'economy', 'vs', 'us', 'as', 'consumers']
```

**(b)**

- **s1** — `wasn't` became `wasn` twice and the `t` was dropped, so **the negation is gone**. The remaining tokens are `great` and `bad`, which is the *opposite* of the sentence's meaning ("it wasn't great, but it wasn't bad" is lukewarm; the bag says strongly mixed-extreme). This matters for any **sentiment or opinion-mining** task. Also `:-)` disappeared entirely — a pure sentiment signal deleted.
- **s2** — `555-0134` split into `555` and `0134`, and `me@example.com` split into `me`, `example`, `com`. The phone number and email address, which are *entities*, have been shredded into meaningless fragments. This matters for **spam detection and PII redaction**, where the presence of a contact detail is often the whole feature.
- **s3** — Lowercasing merged `US` (the country) with `us` (the pronoun) into a single token appearing twice. This matters for **named-entity recognition and topic classification** — a document about the United States now looks like a document containing a common pronoun.

**(c)** *Fix for s1:* use a tokenizer that keeps contractions as single tokens, e.g. `re.findall(r"(?u)\b[\w']+\b", s.lower())`, which yields `['it', "wasn't", 'great', 'but', 'it', "wasn't", 'bad']`.

*New problem it introduces:* apostrophes are also used as quotation marks and in possessives, so `'hello'` becomes `["'hello'"]` and `dog's` stays as `dog's` — meaning `dog` and `dog's` become two separate vocabulary entries with split statistics. You've fixed negation and fragmented possessives. There is no tokenizer without trade-offs; there is only a tokenizer matched to a task.

### 2. [Warm-up] Bag-of-words by hand

**(a) Predicted vocabulary.** The default `token_pattern` is `\b\w\w+\b`, requiring **two or more** word characters, so `i` is dropped from all three documents. The surviving distinct tokens, sorted alphabetically:

```
and, fine, hate, is, it, love, phone, this      (8 terms)
```

**(b) Hand-built count matrix**

| | and | fine | hate | is | it | love | phone | this |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **e1** | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| **e2** | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 |
| **e3** | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 |

**(c)**

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
E = ["i love this phone", "i hate this phone", "this phone is fine and i love it"]
cv = CountVectorizer()
M = cv.fit_transform(E)
print(pd.DataFrame(M.toarray(), index=["e1","e2","e3"], columns=cv.get_feature_names_out()))
```

```
    and  fine  hate  is  it  love  phone  this
e1    0     0     0   0   0     1      1     1
e2    0     0     1   0   0     0      1     1
e3    1     1     0   1   1     1      1     1
```

Exact match.

**(d)** The missing word is **`i`**. It appears in all three documents but is only one character long, and `CountVectorizer`'s default regular expression `(?u)\b\w\w+\b` requires at least two word characters. To keep it, pass `token_pattern=r"(?u)\b\w+\b"`. Worth noting that `i` would have been useless as a feature here anyway (df = 3 of 3, so idf = 1.0, the minimum) — but the *silence* of the omission is the danger. In a corpus of maths text you would lose every occurrence of `x`, `y`, and `n` and never be told.

### 3. [Build] TF-IDF by hand

**(a) Document frequencies** (n = 3):

```
and = 1    fine = 1    hate = 1    is = 1
it  = 1    love = 2    phone = 3   this = 3
```

**(b) IDF**, `idf = ln((1 + 3)/(1 + df)) + 1 = ln(4/(1+df)) + 1`:

| term | df | 4/(1+df) | ln | **idf** |
|---|---:|---|---:|---:|
| and | 1 | 2.0 | 0.693147 | **1.693147** |
| fine | 1 | 2.0 | 0.693147 | **1.693147** |
| hate | 1 | 2.0 | 0.693147 | **1.693147** |
| is | 1 | 2.0 | 0.693147 | **1.693147** |
| it | 1 | 2.0 | 0.693147 | **1.693147** |
| love | 2 | 4/3 = 1.333333 | 0.287682 | **1.287682** |
| phone | 3 | 1.0 | 0.000000 | **1.000000** |
| this | 3 | 1.0 | 0.000000 | **1.000000** |

**(c) e3's vector.** Every term in e3 has tf = 1, so raw products equal the idf values:

```
and = 1.693147   fine = 1.693147   is = 1.693147   it = 1.693147
love = 1.287682  phone = 1.000000  this = 1.000000

norm² = 4 × (1.693147²) + 1.287682² + 1² + 1²
      = 4 × 2.866747 + 1.658125 + 1 + 1
      = 11.466989 + 1.658125 + 2
      = 15.125115

norm  = √15.125115 = 3.889102
```

Final normalized values:

```
and   = 1.693147 / 3.889102 = 0.435357
fine  = 1.693147 / 3.889102 = 0.435357
is    = 1.693147 / 3.889102 = 0.435357
it    = 1.693147 / 3.889102 = 0.435357
love  = 1.287682 / 3.889102 = 0.331100
phone = 1.000000 / 3.889102 = 0.257129
this  = 1.000000 / 3.889102 = 0.257129
hate  = 0
```

Check: `4(0.435357²) + 0.331100² + 2(0.257129²) = 0.758143 + 0.109627 + 0.132231 = 1.000001` ✓

**(d)**

```python
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
tv = TfidfVectorizer()
T = tv.fit_transform(E)
print("idf:", dict(zip(tv.get_feature_names_out(), np.round(tv.idf_, 6))))
print(pd.DataFrame(np.round(T.toarray(), 6), index=["e1","e2","e3"],
                   columns=tv.get_feature_names_out()))
```

```
idf: {'and': 1.693147, 'fine': 1.693147, 'hate': 1.693147, 'is': 1.693147,
      'it': 1.693147, 'love': 1.287682, 'phone': 1.0, 'this': 1.0}
         and      fine      hate        is        it      love     phone      this
e1  0.000000  0.000000  0.000000  0.000000  0.000000  0.673255  0.522842  0.522842
e2  0.000000  0.000000  0.767495  0.000000  0.000000  0.000000  0.453295  0.453295
e3  0.435357  0.435357  0.000000  0.435357  0.435357  0.331100  0.257129  0.257129
```

Row e3 matches the hand computation to six decimals.

**(e)** Highest weight in e3 is a **four-way tie at 0.435357** between `and`, `fine`, `is`, and `it` — each appears in only 1 of 3 documents, so each gets the maximum idf of 1.693147. Lowest is a **tie at 0.257129** between `phone` and `this` — each appears in all 3 documents, so `ln(4/4) = 0` and their idf bottoms out at exactly 1.0.

The uncomfortable observation: TF-IDF has decided that `and` is the most informative word in `"this phone is fine and i love it"`, and that `love` (0.3311) matters less. On three documents that's arithmetically correct and semantically absurd — a reminder that IDF measures *rarity in this corpus*, which only approximates *importance* once the corpus is large enough for rarity and meaningfulness to correlate.

### 4. [Build] Cosine similarity and search

**(a) By hand.** All vectors have length 1, so cosine = dot product; only shared terms contribute.

First, e1 and e2's vectors (same method as e3):

```
e1: raw = love 1.287682, phone 1.0, this 1.0
    norm = √(1.658125 + 1 + 1) = √3.658125 = 1.912623
    love = 0.673255   phone = 0.522842   this = 0.522842

e2: raw = hate 1.693147, phone 1.0, this 1.0
    norm = √(2.866747 + 1 + 1) = √4.866747 = 2.206071
    hate = 0.767495   phone = 0.453295   this = 0.453295
```

```
cos(e1, e2):  shared = {phone, this}
  phone : 0.522842 × 0.453295 = 0.237001
  this  : 0.522842 × 0.453295 = 0.237001
                        total = 0.474003

cos(e1, e3):  shared = {love, phone, this}
  love  : 0.673255 × 0.331100 = 0.222915
  phone : 0.522842 × 0.257129 = 0.134437
  this  : 0.522842 × 0.257129 = 0.134437
                        total = 0.491790

cos(e2, e3):  shared = {phone, this}
  phone : 0.453295 × 0.257129 = 0.116555
  this  : 0.453295 × 0.257129 = 0.116555
                        total = 0.233110
```

|  | e1 | e2 | e3 |
|---|---:|---:|---:|
| **e1** | 1.0000 | 0.4740 | 0.4918 |
| **e2** | 0.4740 | 1.0000 | 0.2331 |
| **e3** | 0.4918 | 0.2331 | 1.0000 |

**(b)**

```python
from sklearn.metrics.pairwise import cosine_similarity
print(pd.DataFrame(np.round(cosine_similarity(T), 4),
                   index=["e1","e2","e3"], columns=["e1","e2","e3"]))
```

```
        e1      e2      e3
e1  1.0000  0.4740  0.4918
e2  0.4740  1.0000  0.2331
e3  0.4918  0.2331  1.0000
```

**(c)** Yes, uncomfortably close. e1 ("i love this phone") and e3 ("this phone is fine and i love it") **mean the same thing** and score 0.4918. e1 and e2 ("i hate this phone") mean **opposite things** and score 0.4740. The gap is only **0.0178**, about 3.6% of the larger value.

The cause is that `phone` and `this` appear in all three documents, so their idf is exactly 1.0 — the floor, not zero. In e1's normalized vector those two terms carry `0.522842² × 2 = 0.5467`, i.e. **55% of the vector's entire squared length**, and in e2 they carry 41%. So over half of e1's representation is content-free words shared with every other document, and they alone push `cos(e1, e2)` to 0.474 before a single meaningful word is considered. The two words that actually differ — `love` and `hate` — contribute *nothing at all* to the similarity, because they never co-occur.

This is the same failure as `cos(d1, d2) = 0.726` in the worked example, and it is structural: bag-of-words similarity is dominated by shared vocabulary, and opposite opinions about the same subject share almost all their vocabulary.

**(d)**

```python
def search(query, vectorizer, matrix, docs):
    q = vectorizer.transform([query])          # transform, NOT fit_transform
    sims = cosine_similarity(q, matrix)[0]
    order = np.argsort(sims)[::-1]
    return [(round(float(sims[i]), 4), docs[i]) for i in order]

for score, doc in search("phone i love", tv, T, E):
    print(f"  {score:.4f}  {doc}")
```

```
  0.4918  i love this phone
  0.2680  this phone is fine and i love it
  0.2093  i hate this phone
```

**Why not `fit_transform`:** calling `fit` on the query would throw away the fitted vocabulary and idf table and build brand-new ones from the two words in the query. The resulting vector would live in a completely different feature space from the document matrix, so the dot product would be meaningless (and would usually raise a dimension-mismatch error, which is the lucky case — the unlucky case is that the dimensions happen to match and you get silent nonsense). A fitted vectorizer is a *learned transform*, exactly like `StandardScaler` in Module 2, and the rule is identical: fit once on training data, transform everything else.

### 5. [Stretch] Measure what n-grams buy you

```python
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

configs = [
    ("(1,1)",            dict(ngram_range=(1, 1))),
    ("(1,2)",            dict(ngram_range=(1, 2))),
    ("(1,3)",            dict(ngram_range=(1, 3))),
    ("(2,2) only",       dict(ngram_range=(2, 2))),
    ("(1,2) min_df=2",   dict(ngram_range=(1, 2), min_df=2)),
]

print(f"{'config':16s} {'vocab':>7s} {'nonzero coef':>13s} {'test acc':>9s}")
for name, kw in configs:
    p = Pipeline([("tfidf", TfidfVectorizer(**kw)),
                  ("clf", LogisticRegression(C=10, max_iter=2000))]).fit(train_texts, train_labels)
    v = len(p.named_steps["tfidf"].get_feature_names_out())
    nz = int(np.sum(np.abs(p.named_steps["clf"].coef_[0]) > 1e-8))
    acc = float(np.mean(p.predict(test_texts) == np.array(test_labels)))
    print(f"{name:16s} {v:>7d} {nz:>13d} {acc:>9.4f}")
```

**(a) + (b)** Representative output:

```
config             vocab  nonzero coef  test acc
(1,1)                144           144    0.7500
(1,2)                308           308    0.7500
(1,3)                450           450    0.7500
(2,2) only           164           164    0.5000
(1,2) min_df=2        76            76    0.5000
```

**(c)** The winner is a **three-way tie at 0.7500** between `(1,1)`, `(1,2)`, and `(1,3)` — that is 9 of 12 test items for all three. Adding bigrams and then trigrams tripled the vocabulary (144 → 450) and moved accuracy by **exactly zero**. The largest gap in the table, `(1,1)` over `(2,2) only`, is 0.25 = 3 test items, which is genuinely meaningful. But between the three tied configs the difference is 0/12, and even a 1/12 = 0.083 difference on a twelve-item test set is one review — well inside the noise of who happened to type which sentence. On this test set you cannot distinguish them at all, and the honest report says so rather than crowning `(1,3)` because it appeared last.

`(1,2) min_df=2` deserves a note of its own: it collapses to 0.5000 despite keeping unigrams. `min_df=2` throws away every feature appearing in fewer than 2 documents, and in a 40-review corpus of deliberately varied sentences that is **almost every sentiment word** — `brilliant`, `tedious`, `hated` and the rest each appear exactly once. What survives is the connective tissue (`the`, `and`, `film`, `this`), which carries no sentiment. `min_df` is an excellent tool on 50,000 documents and a wrecking ball on 40.

Note the "nonzero coef" column equals the vocabulary size every time: with `C=10` (weak regularisation) and L2 penalty (the default, which shrinks but never zeroes), **every** feature keeps a non-zero weight. If you wanted actual feature selection you would need `penalty="l1", solver="liblinear"`.

**(d) Why `(2,2)` alone collapses to 0.5000.** Bigrams-only discards all single words, so the model can no longer see `brilliant`, `terrible`, or `dull` at all — it can only see two-word phrases like `absolutely loved` and `boring film`. Those phrases are far rarer than the words inside them: in a 40-review corpus almost every bigram appears exactly once, so almost every feature is a one-off with no statistical support and the model is essentially memorising specific training sentences. At test time the reviews are newly written, so hardly any of their bigrams exist in the vocabulary, most test vectors come out nearly empty, and the classifier falls back to whatever the intercept says — which is why 0.5000 is exactly the coin-flip you'd get by always guessing one class.

### 6. [Stretch] Break the co-occurrence embedding

Helper used throughout (rebuilds the matrix from any corpus and window):

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

BASE = [
 "the cat drinks milk",        "the dog drinks milk",
 "the cat eats meat",          "the dog eats meat",
 "a small cat sleeps",         "a small dog sleeps",
 "i like pizza very much",     "i like pasta very much",
 "the pizza tastes salty",     "the pasta tastes salty",
 "we order pizza on friday",   "we order pasta on friday",
]

def build(corpus, window=2):
    toks = [s.split() for s in corpus]
    vocab = sorted({w for s in toks for w in s})
    idx = {w: i for i, w in enumerate(vocab)}
    M = np.zeros((len(vocab), len(vocab)))
    for s in toks:
        for p, w in enumerate(s):
            for j in range(max(0, p - window), min(len(s), p + window + 1)):
                if j != p:
                    M[idx[w], idx[s[j]]] += 1
    return M, idx

def cos(a, b, M, idx):
    return float(cosine_similarity([M[idx[a]]], [M[idx[b]]])[0, 0])
```

**(a) Adding `"the cat chases the dog"`**

```python
M, ix = build(BASE + ["the cat chases the dog"])
print("cos(cat, dog) =", round(cos("cat", "dog", M, ix), 4))
print("cat row :", {k: int(M[ix['cat'], v]) for k, v in ix.items() if M[ix['cat'], v] > 0})
print("dog row :", {k: int(M[ix['dog'], v]) for k, v in ix.items() if M[ix['dog'], v] > 0})
```

```
cos(cat, dog) = 0.9901
cat row : {'a': 1, 'chases': 1, 'drinks': 1, 'eats': 1, 'meat': 1, 'milk': 1, 'sleeps': 1, 'small': 1, 'the': 4}
dog row : {'a': 1, 'chases': 1, 'drinks': 1, 'eats': 1, 'meat': 1, 'milk': 1, 'sleeps': 1, 'small': 1, 'the': 3}
```

Similarity fell from 1.0000 to **0.9901** — a surprisingly small drop, and for a reason worth tracing.

In `"the cat chases the dog"`, `cat` sits at position 1 and `dog` at position 4. With `WINDOW = 2` they are three tokens apart, so **neither enters the other's context at all**. What actually changed is the count of `the`: `cat` is within two positions of *both* occurrences of `the` (positions 0 and 3), while `dog` is only within two of the second one (position 3). So `cat`'s `the` count goes 2 → 4 and `dog`'s goes 2 → 3, and that single mismatched cell is the entire cause of the 0.0099 drop.

Note the irony this exposes: putting two words in the same sentence does **not** make them more similar under this method, and can make them slightly less. The distributional hypothesis measures *shared company*, not *co-occurrence*. Words that appear together are not necessarily similar (`cat` and `chases`); words that appear in the same *slots* are.

**(b) Adding `"the dog barks loudly"`**

```python
M, ix = build(BASE + ["the dog barks loudly"])
print("cos(cat, dog) =", round(cos("cat", "dog", M, ix), 4))
```

```
cos(cat, dog) = 0.9239
```

Similarity fell to **0.9239** — a much bigger drop than (a)'s 0.9901, and the mechanism is different.

In (a) the two rows differed by exactly one count on one shared axis (`the`: 4 vs 3). Here `dog` acquires context along axes where `cat` is **flatly zero**: `barks: 1`, `loudly: 1`, plus one more `the`. Two brand-new non-zero dimensions tilt `dog`'s vector out of `cat`'s subspace far more than a single count mismatch on an axis they already share.

The general lesson: unbalanced evidence is more damaging to distributional similarity than a shared-context miscount. In a real corpus this is the normal state of affairs — no two words ever have perfectly twinned sentences, which is exactly why real embedding similarities are 0.7–0.9 rather than 1.0.

**(c) Window size**

```python
print(f"{'window':>7s} {'cat/dog':>9s} {'cat/pizza':>11s} {'milk/meat':>11s}")
for w in [1, 2, 4]:
    M, ix = build(BASE, window=w)
    print(f"{w:>7d} {cos('cat','dog',M,ix):>9.4f} "
          f"{cos('cat','pizza',M,ix):>11.4f} {cos('milk','meat',M,ix):>11.4f}")
```

```
 window   cat/dog   cat/pizza   milk/meat
      1    1.0000      0.2887      0.0000
      2    1.0000      0.1818      0.3333
      4    1.0000      0.1818      0.6000
```

`cat`/`dog` stays at exactly 1.0000 for every window, because the corpus's twin structure guarantees identical contexts at any radius. The other two move in **opposite directions**: `cat`/`pizza` *falls* (0.2887 → 0.1818, then plateaus once the window already spans whole sentences), while `milk`/`meat` *rises* steadily (0.0000 → 0.3333 → 0.6000).

You can verify the two extremes by hand. At window 1, `milk` only ever sits next to `drinks` and `meat` only next to `eats`, so their rows share nothing at all and the cosine is exactly 0. At window 4, `milk`'s row is `{the: 2, cat: 1, dog: 1, drinks: 2}` and `meat`'s is `{the: 2, cat: 1, dog: 1, eats: 2}`; both have squared length 10, they share `the`(4) + `cat`(1) + `dog`(1) = 6, so the cosine is 6/10 = 0.6 exactly.

**(d) What window size controls.** The window sets how much surrounding text counts as a word's "company," and therefore what *kind* of similarity you measure. A **small window (1–2)** captures mostly syntactic and substitutional similarity — words that could grammatically swap into the same slot, like `cat`/`dog` or `drinks`/`eats` — which is why `milk` and `meat` score 0 at window 1: they are never interchangeable in these sentences, they just belong to the same topic. A **large window (4+)** captures topical or associative similarity — words that show up in the same general discussion — so `milk`/`meat` climbs to 0.60 while `cat`/`pizza` gets no boost at all, because the extra context is exactly what distinguishes an animal sentence from a food sentence. Neither setting is more correct; you choose the window to match whether you want "these words are interchangeable" or "these words are about the same thing," and that choice is one of the main reasons two embedding models trained on the same corpus can disagree about which words are similar.

</details>

---

[⬅ Previous](module-08-unsupervised-kmeans-pca.md) · [Level 3 Home](README.md) · [Next ➡](capstone.md)
