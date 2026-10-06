# Week 29 — Nearest Neighbours, and the 20% You Must Hide

[⬅ Week 28](week-28.md) · [Course Home](../README.md) · [Week 30 ➡](week-30.md) · [Student Guide](../student-guide/week-29.md) · [Workbook](../workbook/week-29.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦⚡ Teach — **this is the week the student trains a real model.** Mark it in the diary. |
| **Big idea** | kNN guesses by letting the `k` closest examples vote — and the score only means anything on rows the model never saw. |
| **New vocabulary** | k-nearest neighbours · majority vote · fit · predict · train/test split |
| **New syntax** | `KNeighborsClassifier(n_neighbors=k)` · `model.fit(X_train, y_train)` · `model.predict(X_test)` · `train_test_split(X, y, test_size=0.2, random_state=42)` |
| **Materials** | The printed workbook (Predict the Output, Practice Sets A and B, Fix the Broken Program, Puzzle of the Week, Think Deeper, Build It) · **a real deck of playing cards** · **one envelope the student can sign across the flap** · a pen (not pencil) for the signature · last week's `x_and_y.py` and `iris_shapes.py` · the SHAPES sheet from Week 28 · a calculator |
| **Tech needed** | The Week 28 setup: Python 3 with numpy, pandas, matplotlib and scikit-learn. Nothing new to install. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** use a **real** deck of cards and a **real** envelope, and let the student sign the flap with a pen. This looks like decoration and it is not. The physical act of sealing 20% of the data away, with their own name across the seal, is the thing they will remember in Week 33 when the same idea has to catch a model cheating. A photocopied paper deck does not carry the same weight. Level 1 used a sealed envelope for exactly this and it is deliberately the same prop.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Explain kNN as a majority vote of the `k` nearest rows**, in their own words, without using the word "algorithm".
2. **Make, fit and use a model in three lines of code.**
3. **Split data with `train_test_split`** and say what `random_state` is for.
4. **Report the score on the training rows and on the held-back rows separately**, with the row count next to the second one.
5. **Explain in one sentence why the held-back score is the honest one.**

Observable evidence: a signed, sealed envelope on the table; a terminal showing two different scores printed one under the other; and a number written on the board labelled THE GAP that the student can explain without prompting.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

This is the most important section in the file. Read all of it. There is one genuinely hard idea in this week and it is not the code.

### 1. What kNN actually is — the whole algorithm, in four lines

You move to a new school and sit down in the canteen. You do not know anybody. You want to guess which club the person opposite you is in. You do not run a statistical analysis. You look at the **four people sitting nearest to them**. Three of the four are wearing chess-club badges. You guess: chess.

That is the entire algorithm. It has a name and a three-line implementation and it is used in production systems today.

> **k-nearest neighbours (kNN)** — to label something new, find the `k` known examples closest to it and take a vote.
> **majority vote** — whichever label appears most often among those `k` wins.

![The three nearest get a vote](../figures/fig-w29-1-knn-three-nearest-vote.svg)
*Figure 29.1 — Three neighbours inside the ring get a vote. The six outside get nothing. The tally always adds up to `k`.*

There is no equation to solve and nothing to work out. Here is the part that surprises people, and it is worth knowing before a student asks:

**kNN does not really "learn" anything.** When you call `fit`, it writes the training table down and stops. All the actual work happens later, at `predict` time, when it measures the distance from the new row to *every single row it wrote down*, sorts them, and counts the votes.

This has three consequences you should be able to state:

- **`fit` is instantaneous and `predict` is slow.** The opposite of most models. With 120 training rows nobody notices; with 14 million you would.
- **The model *is* the data.** There are no learned rules inside it. If you email somebody a trained kNN model, you have emailed them your training rows. (There is a privacy question hiding in there, and it is in the Questions section.)
- **The score on the training rows with `k = 1` is exactly 1.0 whenever no two training rows have identical measurements but different labels** (true for all four iris columns; not true for the two-sepal version in Part 3, where it is 0.9417). Every row's own nearest neighbour is itself, at distance zero. This is not a triumph. It is arithmetic.

### 2. What `k` does, and why it is not a detail

`k` is how many neighbours you ask. It is the size of the committee.

| `k` | Behaviour | How it fails |
|---|---|---|
| 1 | Copy whatever the single closest example says | One weird neighbour ruins the answer. Very jumpy. |
| 5–15 | A small committee. Sensible. | Usually where the good answers live. |
| = number of training rows | Everybody votes, so the answer is always the commonest class | It has stopped looking at the input at all |

Here is a real example the student built last week: six known flowers, using petal length and petal width, and one mystery flower at `(3.0, 1.0)`. The six distances, sorted nearest-first, are:

```
1.58  versicolor      <- closest
1.75  versicolor
1.79  setosa
1.79  setosa
1.88  setosa
1.96  versicolor
```

- **k = 1** → versicolor. **1 vote to 0.**
- **k = 3** → versicolor, versicolor, setosa → **2 to 1** → versicolor.
- **k = 5** → versicolor, versicolor, setosa, setosa, setosa → **3 to 2** → **setosa.**

**Same data. Same six distances. Not one number changed. Three different answers.** `k` is not a setting you tune at the end. It *is* the model.

![Change k, change the answer](../figures/fig-w29-5-k-changes-the-answer.svg)
*Figure 29.2 — Six known flowers, sorted nearest first. Take the top 1, the top 3 or the top 5, and the vote flips.*

> **💡 Try this:** use an **odd** `k` when there are two classes. With `k = 4` you can get a 2–2 tie, and sklearn breaks ties by picking whichever class comes first in sorted order — which is a rule, not a principle. With three classes ties are still possible; odd just makes them rarer.

### 3. The three verbs. Learn them once, use them for the rest of your life

Every one of the two hundred-odd models in scikit-learn speaks exactly the same three words.

| Verb | What it does | The code |
|---|---|---|
| **fit** | Learn from `X` and `y` | `model.fit(X_train, y_train)` |
| **predict** | Guess a label for every row of some new `X` | `model.predict(X_test)` |
| **score** | What fraction of those guesses were right | `model.score(X_test, y_test)` |

That is the whole interface. Swap `KNeighborsClassifier` for a decision tree in Week 31 or a straight line in Week 32 and **those three lines do not change one character.** Tell the student that. It is the single highest-value thing they will learn this year, and it is why the library is worth the trouble of installing.

![Three verbs, and that is the whole model](../figures/fig-w29-3-fit-predict-score.svg)
*Figure 29.3 — `fit` gets the answers. `predict` does not. `score` marks the guesses.*

Two details about the code that will trip somebody up:

```python
model = KNeighborsClassifier(n_neighbors=3)
```

This line **makes** a model; it does not train one. Nothing has happened yet. The model at this point is an empty machine with a dial set to 3. It is `n_neighbors` — American spelling, no `u`. A student who types `n_neighbours` gets a `TypeError`, and it is in the Clinic.

```python
model.predict([[3.0, 1.0]])
```

**Double brackets, even for one row.** `predict` always wants a *table* of rows, because it is built to answer thousands of questions at once and one question is just a table with one row in it. Single brackets give the most-quoted error message in this whole level: `ValueError: Expected 2D array, got 1D array instead`. You will meet it, so meet it on purpose.

### 4. The hard idea: a score on the training rows is not a score

This is the one thing in the week that matters more than everything else, and it is genuinely counter-intuitive.

🍕 **The analogy that works.** Your teacher hands you a hundred practice questions **with the answers printed underneath**. You study them until you can recite every one. Then the exam is… those exact hundred questions. You score 100%.

Did you learn the subject, or did you learn the answer sheet? **Nobody can tell. Including you.**

That is exactly what happens when you score a model on the rows it trained on. Here is the demonstration, and it is worth running in front of the student because the number is absurd:

```python
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X, y)                          # learn from ALL 150 flowers
print(model.score(X, y))                 # and then test on all 150
```

```text
1.0
```

**A hundred percent. Perfect. Ship it.** No. With `k = 1`, the nearest neighbour of every training flower is *that flower*, at distance nought. We asked the model to recite a list we had just given it. That number is worth exactly nothing — and versions of it appear in real press releases every month.

The fix is one rule, and it is worth more than every algorithm in this book:

> **Hide some of your rows before you start, and do not let the model see them until the very end.**

> **Training set** — the rows the model is allowed to learn from.
> **Test set** — rows you lock in a drawer and look at **once**, at the end, to find out how the model does on things it has never seen.
> **Train/test split** — the single cut that makes those two piles.

![One cut of the deck, then never mix them](../figures/fig-w29-2-deck-cut-80-20.svg)
*Figure 29.4 — One cut. 120 rows to study, 30 sealed. The counts have to add back up to 150.*

### 5. Every line of `train_test_split`, explained

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y,                 # the table and the answers, in that order
    test_size=0.2,        # 0.2 means 20% of the rows go into the test pile
    random_state=42,      # fixes the shuffle so we get the same cut every run
)
```

**Four names on the left, in that exact order.** `train_test_split` hands back four things, always, in the order X-train, X-test, y-train, y-test. Get the order wrong and nothing crashes — you just quietly train on your test set. Write the order on the SHAPES sheet.

> **⚠️ Watch out:** it is `X_train, X_test, y_train, y_test`. **Not** `X_train, y_train, X_test, y_test`, which is the order most people's brains want. Both X's first, then both y's.

**`test_size=0.2`** — a fraction, so 20%. `0.2` and `0.25` are the usual choices. There is nothing magic about 20%; it is a trade-off. A bigger test set gives you a more reliable score but leaves fewer rows to learn from.

**`random_state=42`** — this is the one worth understanding properly, because it looks like noise and it is not.

`train_test_split` **shuffles the rows before it cuts**, which it must do — the iris file is sorted by species, so cutting the last 20% without shuffling would hand you a test set of nothing but virginica. Shuffling needs randomness. And randomness means that **without** `random_state`, every single run gives you a different split and therefore a different score.

That is a disaster for learning anything. You change one thing, the score goes up, and you have no idea whether your change helped or whether you just got a friendlier shuffle. Setting `random_state` to any fixed whole number nails the shuffle down.

> **Reproducible** — running the same code again gives the same answer, so any difference you see was caused by your change and nothing else.

42 is traditional (it is a joke from a book). 0 and 7 and 31 are equally fine. **The number does not matter. Fixing it does.**

Here is how much it matters, measured. Same data, same model, only the seed changing — this is iris using just the two sepal columns:

```text
random_state=0   test score = 0.6667
random_state=1   test score = 0.8667
random_state=2   test score = 0.7333
random_state=3   test score = 0.7333
random_state=4   test score = 0.9000
random_state=5   test score = 0.8667
random_state=6   test score = 0.7333
random_state=7   test score = 0.6333
random_state=8   test score = 0.6333
random_state=9   test score = 0.8333

lowest : 0.6333
highest: 0.9
spread : 0.2667
```

**Twenty-seven percentage points of spread**, and nothing changed except where the deck was cut. If somebody quotes you a single accuracy with no test-set size and no seed, that table is what they are not telling you.

### 6. The gap, and the sentence to write on the board

When you score both piles you get two numbers, and the difference between them is the most informative thing on the screen.

```text
score on the TRAINING rows : 0.9417 on 120 rows
score on the HELD-BACK rows: 0.7333 on 30 rows

THE GAP: 0.2083
that is 20.83 percentage points
```

![Two scores. Only one of them is news.](../figures/fig-w29-4-two-scores-one-honest.svg)
*Figure 29.5 — The blue bar flatters. The pink bar is the one you are allowed to quote.*

**How to read a gap:**

| What you see | What it means |
|---|---|
| Both high, close together | Healthy. This is what you want. |
| Train high, test much lower | The model memorised. A big gap is the symptom. **Week 33's whole lesson.** |
| Both low | The model is not good enough, or the features do not carry the answer. |
| Test *higher* than train | It happens, especially on small test sets. It means the 30 rows you hid happened to be easy ones. It is not a triumph, it is a reminder that 30 rows is a short ruler. |

That last row will happen in this lesson. With all four iris columns and `k = 5`, the split at `random_state=42` gives train 0.9667 and test **1.0000** — the test score is *higher*. **Do not hide this. Explain it.** With 30 test flowers, each flower is worth 3.3 percentage points, so a gap of one or two flowers is noise, not evidence. Then switch to the two-sepal-column version, where the gap is a genuine 21 points, and put *that* number on the board.

### 7. The two misconceptions you will actually meet

**Misconception 1 — "the test set is a second thing to train on."**

Deeply common. The student sees four variables and assumes all four are used the same way. They are not. `X_train` and `y_train` go into `fit`. `X_test` goes into `predict`. **`y_test` is only ever used to mark the answers** — the model never sees it, not once, not ever. The envelope image is what fixes this: `y_test` is the answer sheet inside the sealed envelope.

**Misconception 2 — "hiding 20% of the data is wasteful."**

It sounds like throwing away learning material. Two answers. First, 120 rows and 150 rows produce almost identical models — the last 30 rows add very little. Second, and this is the real one: **a model whose accuracy you cannot honestly measure is worth nothing at all, however well it was trained.** You are not spending 30 rows on nothing. You are spending them on the only number anybody should believe.

### 8. How deep to go, and where to stop

**Go this far:** the vote, `k`, the three verbs, the split, `random_state`, two scores, the gap.

**Stop before:**
- **`stratify=y`.** Next week. If a student's test set comes out lopsided and they notice, that is excellent — write it on the wall and hold it for a week.
- **Scaling.** Next week, and it is next week's whole point. This week's iris model works fine unscaled, which is convenient and slightly lucky.
- **`accuracy_score` and the confusion matrix.** Next week. Use `model.score()` this week; it computes the same number.
- **Pipelines.** Not this year at all.
- **Choosing `k` by looking at the test scores.** Next week, and next week you will also teach why doing it is slightly dishonest.
- **Cross-validation.** Level 3.
- **Naming the failure.** The word for a big gap is *overfitting* and it belongs to Week 33. You can absolutely say "the model memorised". Do not hand over the word yet — Week 33 needs it to arrive as a name for something they have already felt.

---

### 9. 🧭 The Growing Map — two minutes on a box that does not move

Every week the student guide carries the same pipeline figure with one more piece filled in. It is the
only place either book shows the learner the shape of the year instead of the content of the lesson,
and this week the useful thing about it is precisely that **nothing on it changed.**

![The Level 2 pipeline in Week 29: still the X, y, kNN and trees tile, now splitting, fitting, predicting and scoring](../figures/fig-w29-0-where-this-fits.svg)

*Figure 29.0 — Week 29's version. Still the `X, y · kNN · trees` tile, weeks 28 to 31 — second week
inside it, and this is the one that earns the middle word. Two threads lit: model and evaluation.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and put a finger on the middle word of the gold tile.** Ask *"we did `kNN` today — so how
   many of the four steps happened before the model ever saw a single row?"* The answer is **one**, and
   it is the split. Make them say the four words in order, out loud, in the right order: *split, fit,
   predict, score.* If the order comes out wrong, that is the most useful thing you will learn all
   lesson, and it takes ten seconds to catch here.
2. **Then the question the picture is actually good for:** *"the box did not move this week — but you
   trained a model. Why has the map not changed?"* You are fishing for *because it is the same tile*
   or *because it takes four weeks*. Either is fine. What you are teaching is that this last stage is
   wide, not that the day was small.
3. **Have them copy the map and add THE GAP** in the space under the gold tile, with today's two
   scores on either side of it. Tell them to leave room: the same spot gets a second entry next week
   and a name in Week 33.

> **🧑‍🏫 Why this is worth two minutes.** The temptation this week is to treat training a model as the
> finish line, and the map quietly refuses to agree — three tiles of this stage are still ahead, and
> one whole box is still dashed. That framing is what keeps the held-back 20% feeling like a
> permanent habit rather than a one-off exercise. It also gives you somewhere physical to put the gap,
> which matters: Week 33 needs them to have *felt* a gap before it hands over the word overfitting.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Find a deck of cards and an envelope.** Any envelope the student can write across the flap. Any deck; it does not have to be 52 cards, it just has to be a real physical pile.
- [ ] **Check last week's files are still there:** `x_and_y.py` and `iris_shapes.py`. If they have gone, re-type `iris_shapes.py` tonight so you are not doing it in class.
- [ ] **Run the three-line model yourself.** Create `first_model.py`:

  ```python
  # first_model.py
  # Three lines of scikit-learn do what we just did by hand.

  import numpy as np
  from sklearn.neighbors import KNeighborsClassifier    # the model, imported

  six = np.array([[1.4, 0.2],
                  [1.4, 0.2],
                  [1.3, 0.2],
                  [4.7, 1.4],
                  [4.5, 1.5],
                  [4.9, 1.5]])
  names = np.array(["setosa", "setosa", "setosa",
                    "versicolor", "versicolor", "versicolor"])

  model = KNeighborsClassifier(n_neighbors=3)   # 1. make it. Committee of 3.
  model.fit(six, names)                         # 2. fit it. Show it the answers.
  guess = model.predict([[3.0, 1.0]])           # 3. predict. Note DOUBLE brackets.

  print("the model guesses:", guess)
  print()

  # Try the same mystery flower with three different committee sizes.
  for k in [1, 3, 5]:
      m = KNeighborsClassifier(n_neighbors=k)
      m.fit(six, names)
      print(f"k = {k}  ->", m.predict([[3.0, 1.0]]))
  ```

  Expected output, exactly:

  ```text
  the model guesses: ['versicolor']

  k = 1  -> ['versicolor']
  k = 3  -> ['versicolor']
  k = 5  -> ['setosa']
  ```

- [ ] **Run the full cycle yourself.** Create `full_cycle.py`:

  ```python
  # full_cycle.py
  # The whole thing: split, fit, predict, and TWO scores.

  from sklearn.datasets import load_iris
  from sklearn.model_selection import train_test_split
  from sklearn.neighbors import KNeighborsClassifier

  iris = load_iris()
  X = iris.data
  y = iris.target

  # 1. Cut the deck BEFORE the model sees anything.
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42
  )

  # 2. Make the model and fit it on the training pile only.
  model = KNeighborsClassifier(n_neighbors=5)
  model.fit(X_train, y_train)

  # 3. Predict the held-back rows.
  predictions = model.predict(X_test)

  print("first 10 predictions:", predictions[:10])
  print("first 10 real answers:", y_test[:10])
  print()

  train_score = model.score(X_train, y_train)   # score on rows it studied
  test_score = model.score(X_test, y_test)      # score on rows it never saw

  print("score on the TRAINING rows:", round(train_score, 4), " (", len(X_train), "rows )")
  print("score on the HELD-BACK rows:", round(test_score, 4), " (", len(X_test), "rows )")
  print()
  print("the gap:", round(train_score - test_score, 4))
  ```

  Expected output, exactly:

  ```text
  first 10 predictions: [1 0 2 1 1 0 1 2 1 1]
  first 10 real answers: [1 0 2 1 1 0 1 2 1 1]

  score on the TRAINING rows: 0.9667  ( 120 rows )
  score on the HELD-BACK rows: 1.0  ( 30 rows )

  the gap: -0.0333
  ```

  **Read that carefully now, before class.** The gap is *negative* — the held-back score came out higher. That is real, it is fine, and section 6 above tells you how to explain it. The lesson then switches to two columns instead of four, where the gap is a genuine 21 points.

- [ ] Print the whole Week 29 workbook (it has named sections, not numbered pages).
- [ ] Read section 4 (why a training score is not a score) twice. It is the whole week.
- [ ] Put the SHAPES sheet from Week 28 back on the wall.

### 5 minutes on the day

- [ ] Deck of cards, envelope and a **pen** on the table.
- [ ] Laptop on, terminal open, `first_model.py` and `full_cycle.py` **deleted or moved out of the way** — the student is going to type them, and having yesterday's copy sitting there is a temptation for both of you.
- [ ] Board or big sheet with room for one number, headed **THE GAP**. Leave it blank.
- [ ] Run `iris_shapes.py` once, now, to prove the install still works.

### Fallback if a laptop or an install fails

| If this fails | Do this instead |
|---|---|
| **No laptop today** | The deck, the envelope and the workbook's Puzzle of the Week (Part 1) give you a complete lesson. Puzzle Part 1 has twelve iris rows and one mystery flower printed; the student computes all twelve distances with a calculator, sorts them, and does the vote for `k = 1, 3, 5` by hand. That delivers objectives 1, 4 and 5 in full. Type the code next lesson — the concept is the hard part and it is entirely doable on paper. |
| **scikit-learn broke since last week** | Same as above. Do not spend class time on pip. |
| **No deck of cards** | Any pile of 20-ish identical objects: cut playing-card-sized rectangles from paper, use dominoes, use Lego bricks, use coins. **The envelope is the part you must not skip.** |
| **The student wants to skip the paper part and just type** | Do not let them. The whole point of this week is a discipline, and the discipline is physical before it is code. Say so, honestly: "The code takes four minutes. The habit takes twenty. We're here for the habit." |
| **The student read ahead and knows about scaling** | Superb. Write "SCALING — <their name>, <today's date>" on the wall and tell them Week 30 is theirs. Then, today, hand them the Differentiation → flying tasks. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — I Can Teach You a Real Model in One Sentence | 7 | 7 | The canteen, and then the 100% catch |
| 🧠 Concept — The Vote, and the Three Verbs | 16 | 23 | kNN by hand; `k` flips the answer; fit/predict/score |
| 💻 Live-Code Together — Three Lines, and Then the Lie | 18 | 41 | A working model; then 1.0 on purpose; two deliberate mistakes |
| 🎲 Their Turn — Cut the Deck, Sign the Envelope, Find the Gap | 20 | 61 | The physical split, then the same cut in code, then two scores |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the gap on the board, homework |

---

### 🪝 Hook — I Can Teach You a Real Model in One Sentence (7 minutes)

**Do this:** Laptop closed. Deck of cards visible but untouched on the table.

**Say this:**

> "I'm going to teach you a real machine learning model. Not a toy one — one that real companies actually run. And I'm going to do it in one sentence, and then we're done with the theory for the day.
>
> Here's the sentence. Picture your first day at a new school. You sit down in the canteen and you don't know a single person. You want to guess which club the girl opposite you is in. What do you do?"

Let them answer. Most people say something like "look at who she's sitting with".

> "Exactly. You look at the four people **nearest** to her. Three of the four have chess club badges on. You guess: chess.
>
> That's it. That is the whole model. It's called **k-nearest neighbours**, and the `k` is just how many neighbours you decided to ask. You asked four, so k was four.
>
> No equations. Nothing to solve. You find the closest examples you already know the answers for, and you let them vote."

Write on the board:

> **k-nearest neighbours** — to label something new, find the `k` closest examples you know the answer for, and take a vote.

> "And you already have everything you need to build it. Last week you learnt how to measure the distance between two rows. That was the hard part, and you've done it. This week it's three lines of code."

**Now the catch.** Change your tone.

> "But before we build anything, I want to show you how to break it, because that turns out to be the important half of today.
>
> Suppose I build this thing, and then I check how good it is by asking it about the **exact same** hundred and fifty flowers it learnt from. What do you reckon it scores?"

Let them guess. Let them be uncertain.

> "A hundred percent. Every single time. And here's why, and it's almost funny. If I ask it 'what's this flower?' and hand it a flower that's already in its notes — what's the nearest example to that flower?"

Wait for it. **It's itself.**

> "Itself. Distance zero. Nothing is closer to a thing than the thing. So it looks up the flower, finds the flower, reads off the answer, and gets it right. A hundred out of a hundred.
>
> Now — does that machine understand flowers?"

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Does a machine that scores 100% by looking itself up understand flowers?" | No. It memorised the list. | If they say "kind of", push: "What would it do with a flower that isn't in its notes? It has no idea, and the 100% didn't tell you that." |
| "Where have you met a perfect score that meant nothing before?" | Level 1, the wet umbrella / the sticker on the fruit. | If they don't get it, name it: "The sticker that said APPLE. Twelve out of twelve, and worthless." |
| "So how would you catch it out?" | Test it on flowers it has never seen. | This is the answer to the whole week. If they get there, stop and say so: "That's the rule this whole lesson is built on, and you just invented it." |
| "How much of the data would you hide?" | Anything sensible. 10%, 20%, a quarter. | Any argued number is right. Reply: "Twenty percent is what most people use. Why not ninety?" *(Because then there's nothing left to learn from.)* |

---

### 🧠 Concept — The Vote, and the Three Verbs (16 minutes)

**Do this:** The six-flower vote between you (the same six flowers as Practice Set B, B2; the six distances, already computed, are listed in the Answer Key under B2 — copy them onto a card).

**Say this — part 1, the vote, by hand:**

> "These are the six flowers you measured last week, and the mystery flower at (3.0, 1.0). And these are the six distances you worked out. I've sorted them, nearest at the top."

```
1.58  versicolor      <- closest
1.75  versicolor
1.79  setosa
1.79  setosa
1.88  setosa
1.96  versicolor
```

> "Right. If k is one — if I only ask the single closest neighbour — what's the answer?"

Versicolor.

> "If k is three — the top three vote. Read them to me."

Versicolor, versicolor, setosa. Two to one.

> "So k equals three says versicolor as well. Now k equals five. Top five. Count them for me."

Versicolor, versicolor, setosa, setosa, setosa. **Three setosa, two versicolor.**

> "**Setosa.** The answer just changed. And I want you to notice exactly what changed to make that happen. Did any distance change?"

No.

> "Did any flower move? Did I remeasure anything? Did I fix a bug?"

No, no, no.

> "I turned one dial. And the answer flipped. So `k` is not a little setting you fiddle with at the end. **`k` is the model.** Two people can run the same code on the same data with different k and get different answers, and neither of them is wrong."

**Say this — part 2, the three verbs:**

> "Now here's the bit that pays you back for the rest of your life. Every single model in this library — and there are about two hundred of them — speaks exactly three words. Three. And they never change.
>
> **fit.** You hand it `X` and `y` — the measurements and the answers — and it learns. For kNN, 'learns' literally means 'writes the table down'. That's all it does.
>
> **predict.** You hand it a new `X` with no answers, and it gives you a guess for every row.
>
> **score.** You hand it an `X` *and* the real `y`, and it tells you what fraction it got right.
>
> Write those three words down, because in Week 31 we swap kNN for a decision tree and in Week 32 we swap it for a straight line, and those three lines of code will not change by one character."

**Do this:** Write on the SHAPES sheet, under the shapes:

```
fit(X_train, y_train)     learn from these
predict(X_test)           guess these.  NO answers given
score(X_test, y_test)     mark the guesses
```

**Say this — part 3, the split, and the envelope:**

> "And now the rule that makes all of it mean something.
>
> Imagine I give you a hundred practice questions with the answers printed underneath. You study them until you can recite the lot. Then I set the exam — and the exam is those exact hundred questions. You get a hundred percent.
>
> Did you learn maths, or did you learn the answer sheet?"

Let them sit with it.

> "You can't tell. **I** can't tell. And *you* can't tell either, and that's the worst part.
>
> So: before we train anything, we cut the data in two. Eighty percent the model studies. Twenty percent we seal in an envelope and do not open until the very end.
>
> Two names, and they matter:
>
> The **training set** — the rows the model is allowed to learn from.
> The **test set** — the rows in the envelope. We look at them once. Once."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Why did k = 5 give a different answer from k = 3?" | Because two more setosa got votes and outnumbered the versicolors. | If they say "because 5 is bigger", push for the actual count: "Read me the top five and tally them." |
| "Which of the three verbs gets to see the answers?" | Only `fit`. And `score`, to do the marking. | **The one that matters.** If they say `predict` sees answers, go back to the envelope: "If it saw the answers, what would it be predicting?" |
| "Why not just train on all 150 and be done?" | Because then you have no honest way to check it. | If they say "it'd be better", agree partly: "Slightly better, yes. And completely unmeasurable. Which would you rather ship?" |
| "How many rows in the envelope if we have 150 and hide 20%?" | 30. And 120 to train on. | If they struggle, do it out loud: 10% of 150 is 15, so 20% is 30. |
| "What's `y_test` actually for?" | Marking. The model never sees it. | This is the check that separates secure from emerging. If they're unsure, hold up the sealed envelope: "It's the answer sheet in here." |

---

### 💻 Live-Code Together — Three Lines, and Then the Lie (18 minutes)

**Two chairs, one keyboard, and the student types.**

**Keystroke sequence — part 1, a working model (6 minutes).**

New file, `first_model.py`. Dictate the file exactly as printed in the Prep Checklist. Then, before running it, stop:

**Say this:**

> "Before we run this — three lines do the whole job and I want you to name them. Line one makes the model. What has it learnt at that point?"

Nothing.

> "Nothing. It's an empty machine with a dial set to 3. Line two is `fit`, and that's where it learns — which for kNN means it writes down the six flowers. Line three is `predict`, and that's where all the actual work happens: it measures six distances, sorts them, and counts three votes. Run it."

```text
the model guesses: ['versicolor']

k = 1  -> ['versicolor']
k = 3  -> ['versicolor']
k = 5  -> ['setosa']
```

**Say this, and take your time:**

> "Look at those three lines at the bottom, and then look at the page in front of you where you did it by hand.
>
> Versicolor. Versicolor. Setosa.
>
> **Identical.** The library and your pencil agree on all three. You didn't take my word for what kNN does — you did it yourself first, and then the machine confirmed you. That's the right order and I'd like you to keep doing it that way all year."

**Keystroke sequence — part 2, ⚠️ DELIBERATE MISTAKE NUMBER ONE (4 minutes).**

**Do this:** Change the predict line to single brackets, on purpose:

```python
guess = model.predict([3.0, 1.0])
```

**Say this:**

> "Now I'm going to make the single most common mistake in this entire library, deliberately, so you meet it here with me instead of alone tonight. I'm taking out one pair of brackets."

Run it. Long traceback, ending:

```text
  File "/Users/you/project/first_model.py", line 15, in <module>
    guess = model.predict([3.0, 1.0])
  ...
ValueError: Expected 2D array, got 1D array instead:
array=[3. 1.].
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
```

**Say this:**

> "Last line first — except this time the last three lines are all one message. `Expected 2D array, got 1D array instead.`
>
> **2D means a table.** Rows and columns. **1D means a single line.** I gave it a single line and it wanted a table.
>
> And why does it want a table for one flower? Because `predict` is built to answer thousands of questions in one go. It doesn't have a special mode for one. So one question is a table that happens to have one row in it. Hence two brackets: the outer ones say 'here is a table', the inner ones say 'here is the one row in it'.
>
> Ignore the advice about `reshape`. It's correct and it's for grown-up situations. Ours is: **put the brackets back.**"

Fix it. Run. It works.

**Keystroke sequence — part 3, the dishonest 100% (5 minutes).**

New file, `dishonest.py`:

```python
# dishonest.py
# The wrong thing, done on purpose, so you recognise it later.

from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data                            # all 150 rows, all 4 measurements
y = iris.target                          # all 150 answers

model = KNeighborsClassifier(n_neighbors=1)
model.fit(X, y)                          # learn from ALL 150 flowers

print("score on the very same 150 flowers:", model.score(X, y))
```

**Before running, ask them to predict the number and write it down.** Then run:

```text
score on the very same 150 flowers: 1.0
```

**Say this:**

> "One point nought. A hundred percent. Hundred and fifty out of a hundred and fifty.
>
> Now: put that in a press release. 'Our new flower identification system is one hundred percent accurate.' It's not a lie, is it? That is genuinely the number that came out.
>
> And it is completely worthless, and you can say exactly why in one sentence."

Let them say it. *Every flower's nearest neighbour is itself.*

> "So I want you to be suspicious of a number like that for the rest of your life. Level 1 taught you this with a sticker that said APPLE on it. Same shape of mistake, different clothes. **A perfect score is not a triumph. It's the first symptom that something has leaked.**"

**Keystroke sequence — part 4, ⚠️ DELIBERATE MISTAKE NUMBER TWO, and the split (3 minutes).**

New file, `split_it.py`. Type this, deliberately wrong — **two** names on the left instead of four:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X_train, X_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
```

Run:

```text
Traceback (most recent call last):
  File "/Users/you/project/split_it.py", line 5, in <module>
    X_train, X_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
ValueError: too many values to unpack (expected 2)
```

**Say this:**

> "`too many values to unpack (expected 2)`. Unpack is a nice word for it — imagine a parcel with four things in it and you've only put out two boxes to catch them.
>
> `train_test_split` always hands back **four** things, in one fixed order, and you have to catch all four:
>
> **X_train, X_test, y_train, y_test.**
>
> Both X's first, then both y's. And I'll be honest, that's not the order most brains want — most people want to pair them up, X-train-y-train. It isn't that. Learn the order, because if you get it wrong Python won't always tell you. Here it did, because we gave it two names. If you give it four names in the wrong order it will happily hand you your test set to train on and say nothing at all."

Fix it, and complete the file:

```python
# split_it.py
# Cut the deck: 80% to learn from, 20% locked away.

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split   # the new import

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y,                 # the table and the answers, in that order
    test_size=0.2,        # 0.2 means 20% of the rows go into the test pile
    random_state=42,      # fixes the shuffle so we get the same cut every run
)

print("whole table :", X.shape)
print("train pile  :", X_train.shape, " answers:", y_train.shape)
print("test pile   :", X_test.shape, " answers:", y_test.shape)
print()
print("len(X_train) =", len(X_train))
print("len(X_test)  =", len(X_test))
print("120 + 30 =", len(X_train) + len(X_test))
```

```text
whole table : (150, 4)
train pile  : (120, 4)  answers: (120,)
test pile   : (30, 4)  answers: (30,)

len(X_train) = 120
len(X_test)  = 30
120 + 30 = 150
```

**Do this:** Add all four shapes to the SHAPES sheet. Make the student read them out and confirm the row counts add up. **This addition is the check that catches most of their own mistakes for the rest of the year** — say so.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "2D array means what, in plain English?" | A table. Rows and columns. | If stuck: "How many directions does a table have? Two. That's the D." |
| "Why does `predict` want a table for one flower?" | Because it's built for thousands at once; one is just a table with one row. | If they say "because it's fussy", accept the frustration, then give the reason. |
| "Why did the 100% happen?" | Every flower's nearest neighbour is itself, distance 0. | Non-negotiable. If they can't say it, walk them to it with "what's the closest flower to flower number 7?" |
| "`train_test_split` gives back how many things, in what order?" | Four. X_train, X_test, y_train, y_test. | Drill it. Have them say it three times. Write it on the sheet. |
| "120 and 30. Should they add to 150?" | Yes, always. | If they say no, ask where the missing rows would have gone. Nowhere. Nothing is thrown away and nothing is in both piles. |

---

### 🎲 Their Turn — Cut the Deck, Sign the Envelope, Find the Gap (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–6:** the deck, the cut, the signature, the sealed envelope. Physical only. No laptop.
- **Minutes 6–13:** the full cycle in code — `full_cycle.py`, both scores printed.
- **Minutes 13–20:** the two-column version, `the_gap.py`, and the number goes on the board.

---

## 🐞 The Debugging Clinic

Every message below came out of a real run of a deliberately broken version of this week's code. Long middle sections are trimmed with `...` where they only show the library's own insides.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `ValueError: Expected 2D array, got 1D array instead:` `array=[3. 1.].` | "You gave me a single line and I need a table." | Single brackets: `model.predict([3.0, 1.0])`. | Double brackets: `model.predict([[3.0, 1.0]])`. One row is still a table. |
| `sklearn.exceptions.NotFittedError: This KNeighborsClassifier instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.` | "You asked me to guess before I'd been shown anything." | The `model.fit(...)` line is missing, misspelled, or below the `predict` line. | Put `model.fit(X_train, y_train)` in, above the `predict`. Order matters: make, fit, predict. |
| `ValueError: too many values to unpack (expected 2)` | "I handed you four things and you only put out two boxes." | `X_train, X_test = train_test_split(...)`. | Catch all four: `X_train, X_test, y_train, y_test = train_test_split(...)`. |
| `TypeError: KNeighborsClassifier.__init__() got an unexpected keyword argument 'n_neighbours'` | "There is no setting by that name." | British spelling. The library says `n_neighbors`, no `u`. | `KNeighborsClassifier(n_neighbors=5)`. Annoying, and permanent. |
| `ValueError: Found input variables with inconsistent numbers of samples: [120, 30]` | "You gave me 120 rows of measurements and 30 answers. Which 90 rows have no answer?" | `model.fit(X_train, y_test)` — the wrong `y`. Nearly always caused by the four-name order. | `model.fit(X_train, y_train)`. Then re-read the four names left to right and check they are in order. |
| `ValueError: Expected n_neighbors <= n_samples_fit, but n_neighbors = 10, n_samples_fit = 6, n_samples = 1` | "You asked ten neighbours to vote and I only know six examples." | `k` is bigger than the training set. Common on the six-flower toy example. | Make `k` smaller than the number of training rows. |
| `ImportError: cannot import name 'KNeighborsClassifier' from 'sklearn'` | "That name isn't in that room." | Import path too short: `from sklearn import KNeighborsClassifier`. | `from sklearn.neighbors import KNeighborsClassifier`. Models live in rooms: `.neighbors`, `.tree`, `.linear_model`. |
| `ImportError: cannot import name 'train_test_split' from 'sklearn.datasets'` | Right function, wrong room. | It is in `sklearn.model_selection`, not `sklearn.datasets`. | `from sklearn.model_selection import train_test_split`. |
| **No error at all**, and the accuracy changes every single time you run the file | Nothing is broken. The shuffle is different every run. | `random_state` is missing from `train_test_split`. | Add `random_state=42`. Any fixed whole number. |

### How to teach debugging without giving the answer

Same ladder as every week, but this week add one rung at the top, because sklearn's messages are unusually chatty:

0. **"Find the line with *your* filename on it."** Sklearn tracebacks are fifteen lines of library internals. Teach the student to scan for their own file first, then read the last line. Two lines out of fifteen are theirs.
1. **"Read me the last line."**
2. **"What was it expecting, and what did it get?"** Sklearn is unusually good at telling you both. `[120, 30]` is the whole bug, right there in the message.
3. **"What did you change since it last worked?"**
4. **Point at the line. Say nothing.**
5. **Point at the character.**
6. **Tell them — and name the family:** "that's a shapes-don't-match one", "that's a brackets one", "that's an order-of-the-four-names one."

> **🧑‍🏫 If a student asks:** *"Why doesn't it just fix the brackets for me? It clearly knows what I meant."* — Honest answer: it does not know. `[3.0, 1.0]` could sensibly mean one flower with two measurements, or two flowers with one measurement each. Both are real situations, and guessing wrong would give you a plausible answer that was silently wrong — which is far worse than an error. **A library that refuses to guess is doing you a favour**, and the `reshape(-1, 1)` / `reshape(1, -1)` advice in that message is it offering you both options rather than choosing.

---

## 🎲 The Activity, In Full

### Cut the Deck, Sign the Envelope, Find the Gap

Three parts, in this order, and the order is the point. Physical first, then code, then the number that makes it matter.

### Setup

**On the table:** the deck of cards, the envelope, a pen, the workbook open at Build It Part 1 and Practice Set A (A2), the laptop.

**On the board:** a blank space headed **THE GAP**.

### Part 1 — The deck and the envelope (6 minutes, no laptop)

1. **Count out 100 cards** — or however many the deck has; say the number out loud and write it down. If it is a standard 52-card deck, use 50 for easy arithmetic and put two aside.
2. **Shuffle properly.** Say why while you do it: *"The iris file is sorted — the first fifty rows are all setosa. If I cut it without shuffling, my test set is thirty virginica and nothing else, and my score tells me nothing about the other two species. Shuffling isn't tidiness. It's necessary."*
3. **Ask the student to work out 20% of the number of cards.** For 50, that is 10. Have them say it before you cut.
4. **Cut off that many cards.** Deal them into a small pile. Count them out loud, one at a time, into the pile. Then count the big pile.
5. **Write the two numbers on the envelope** — `TEST: 10 rows` — along with today's date.
6. **Put the small pile in the envelope. Seal it.**
7. **Hand the student the pen.** *"Sign across the flap. Right across it, so you'd be able to tell if it had been opened."*
8. Put the envelope in the middle of the table, where it stays, visible, for the rest of the lesson.

**Say this:**

> "Right. That envelope has ten rows in it and nobody knows what they are. Not you and not me. And from this second on there is exactly one thing we're allowed to do with it: at the very end, open it once, and check.
>
> Not open it, have a look, tweak the model, and check again. **Once.** Because the moment you look at it twice, and change something in between, it stops being data you've never seen — and it goes back to being a practice paper with the answers on it.
>
> That signature is you promising yourself. Level 1 did this with an envelope too, and it was the same promise then."

### Part 2 — The same cut, in one line (7 minutes)

**Do this:** The student types `full_cycle.py`, dictated as printed in the Prep Checklist. Run it.

```text
first 10 predictions: [1 0 2 1 1 0 1 2 1 1]
first 10 real answers: [1 0 2 1 1 0 1 2 1 1]

score on the TRAINING rows: 0.9667  ( 120 rows )
score on the HELD-BACK rows: 1.0  ( 30 rows )

the gap: -0.0333
```

**Say this:**

> "Two things to look at. First, the predictions and the real answers, side by side, and the first ten match exactly. That's a real model doing real work on flowers it has never seen — and you built it three minutes ago.
>
> Second — and this is the interesting one — look at the two scores. The held-back score is **higher** than the training score. It got everything right on the sealed pile.
>
> Now. Is that a triumph?"

Let them decide. Then:

> "No. And here's the honest reason. There are **thirty** flowers in that test pile. So each single flower is worth three point three percentage points. One flower being lucky or unlucky moves the number by three points. The gap here is one flower's worth.
>
> Which means: **the score didn't go up. It just didn't go anywhere, and thirty is too short a ruler to tell the difference.** That's why, from today, every accuracy you ever report gets its row count written next to it. Every single time. `1.0000 on 30 rows` is honest. `100%` on its own is showing off."

### Part 3 — Make it harder, and find the real gap (7 minutes)

**Say this:**

> "Iris with all four measurements is a bit too easy — it's the sort of problem where everything works and you learn nothing. So we're going to make it harder in the meanest possible way: we'll throw away the two best measurements and keep only the two worst.
>
> Last week you noticed the petals separate the species nicely. So: petals out. We'll use only the two **sepal** measurements, and we'll set k to 1, so the model just copies its nearest neighbour."

**Do this:** New file, `the_gap.py`:

```python
# the_gap.py
# The same cycle, but using only the two SEPAL columns, with k = 1.

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data[:, 0:2]                    # columns 0 and 1: the two sepal columns
y = iris.target

print("X shape now:", X.shape)           # 150 rows, only 2 columns

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=1)   # k = 1: copy the single closest
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print()
print("score on the TRAINING rows :", round(train_score, 4), "on", len(X_train), "rows")
print("score on the HELD-BACK rows:", round(test_score, 4), "on", len(X_test), "rows")
print()
print("THE GAP:", round(train_score - test_score, 4))
print("that is", round((train_score - test_score) * 100, 2), "percentage points")
```

```text
X shape now: (150, 2)

score on the TRAINING rows : 0.9417 on 120 rows
score on the HELD-BACK rows: 0.7333 on 30 rows

THE GAP: 0.2083
that is 20.83 percentage points
```

**Do this:** Write on the board, big, and **leave it there for the rest of the term**:

```
  THE GAP        0.9417  on the rows it studied
                 0.7333  on the rows it had never seen
                 --------
                 0.2083   =  21 percentage points of flattery
```

**Say this:**

> "There it is. Ninety-four percent on the homework it had the answers to. Seventy-three percent on the exam.
>
> Twenty-one points of that first number was **memory**. Not skill. Memory. And if I'd only ever shown you the ninety-four — which is exactly what a lot of people do — you'd have believed it, and so would I.
>
> That number stays on the board until the end of term. There's a lesson coming in a few weeks that is entirely about that gap, and when we get there I want you to be able to point at it and say 'we saw that in Week 29'."

### What "finished" looks like

- A sealed envelope on the table with a signature across the flap, a date, and a row count written on it.
- A terminal showing two scores printed one under the other, each with its row count.
- `0.2083` on the board, labelled, with both scores above it.
- The student able to answer, unprompted: **"which of those two numbers would you tell somebody, and why?"**

### Variation — easier

- **Do the whole thing on paper.** The workbook's Puzzle of the Week, Part 1, prints twelve iris rows and one mystery flower. The student computes twelve distances with a calculator, sorts them, and votes for `k = 1, 3, 5`. That is objectives 1, 4 and 5 completely, with no laptop.
- **Skip Part 3.** The envelope plus one working `full_cycle.py` is a complete and satisfying lesson. Put the gap from `full_cycle.py` on the board and be honest that it is small.
- **Give them `full_cycle.py` already typed** and have them change only `n_neighbors` and `random_state`, predicting each result before they run it. Reading and editing working code is a real skill and a legitimate substitute for typing it from scratch.
- **Drop the six-flower hand vote** and go straight to the code if the arithmetic is the blocker. The concept survives.

### Variation — harder

All of these use only syntax they already have.

1. **Three personalities of `k`.** Predict, in writing, what happens at `k = 1`, `k = 5` and `k = 120` (every training row voting), *before* running it. Then:

   ```python
   # three_personalities.py
   # Three sizes of committee, three completely different personalities.

   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   from sklearn.neighbors import KNeighborsClassifier

   iris = load_iris()
   X = iris.data
   y = iris.target

   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )

   for k in [1, 5, 120]:                    # 120 = every training row votes
       model = KNeighborsClassifier(n_neighbors=k)
       model.fit(X_train, y_train)
       train = model.score(X_train, y_train)
       test = model.score(X_test, y_test)
       print(f"k = {k:3d}   train = {train:.4f}   test = {test:.4f}")
   ```

   ```text
   k =   1   train = 1.0000   test = 1.0000
   k =   5   train = 0.9667   test = 1.0000
   k = 120   train = 0.3417   test = 0.3000
   ```

   Three questions worth asking about that: **Why is `k = 1`'s train score exactly 1.0000?** *(Every row is its own nearest neighbour.)* **Why did `k = 120` collapse to about a third?** *(Every training row votes on every prediction, so the answer is always the commonest class — and there are three roughly equal classes, so it is right about a third of the time. It has stopped looking at the flower entirely.)* **Which of the three is a healthy model?** *(k = 5: both scores high and close together.)*

2. **Does `random_state` change the story?** Loop the seed 0 to 9 on the two-sepal-column problem and collect the ten test scores:

   ```python
   # random_state_matters.py
   # Change where you cut the deck and the score changes. Same model, same data.

   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   from sklearn.neighbors import KNeighborsClassifier

   iris = load_iris()
   X = iris.data[:, 0:2]                    # the two sepal columns again
   y = iris.target

   scores = []                              # collect the ten test scores
   for seed in range(10):                   # ten different cuts of the same deck
       X_train, X_test, y_train, y_test = train_test_split(
           X, y, test_size=0.2, random_state=seed
       )
       model = KNeighborsClassifier(n_neighbors=5)
       model.fit(X_train, y_train)
       score = model.score(X_test, y_test)
       scores.append(score)
       print(f"random_state={seed}   test score = {score:.4f}")

   print()
   print("lowest :", round(min(scores), 4))
   print("highest:", round(max(scores), 4))
   print("spread :", round(max(scores) - min(scores), 4))
   ```

   ```text
   random_state=0   test score = 0.6667
   random_state=1   test score = 0.8667
   random_state=2   test score = 0.7333
   random_state=3   test score = 0.7333
   random_state=4   test score = 0.9000
   random_state=5   test score = 0.8667
   random_state=6   test score = 0.7333
   random_state=7   test score = 0.6333
   random_state=8   test score = 0.6333
   random_state=9   test score = 0.8333

   lowest : 0.6333
   highest: 0.9
   spread : 0.2667
   ```

   Then the question: **"If I picked which seed to report, what could I claim?"** *(Anything from 63% to 90%. Which is why you fix the seed before you look, not after — and why quoting one number without the test size is meaningless.)*

3. **Find a flower the model gets wrong**, and print its four measurements next to the true answer and the guess. Then say, in one sentence, why it is a hard flower. *(It will almost always be a versicolor/virginica near the boundary.)*
4. **Two columns of your choice.** Which *pair* of iris columns gives the best held-back score? There are six pairs. Try all six and rank them — then predict, before you look, which pair wins. *(The two petal columns. Last week's plot already showed why.)*

---

## ❓ Questions Students Ask This Week

**"Where is the model? What does it actually look like inside?"**

For kNN, genuinely: it is the training table. That is all. There are no rules and no learned numbers — `fit` copies `X_train` and `y_train` into the object and stops. That makes kNN unusual and a bit disappointing to look inside, and it also makes it the easiest model in the world to explain, which is why it is first. In Week 31 you will meet a decision tree, which throws the data away and keeps only a short list of yes/no questions, and you will be able to print those questions out and read them aloud.

**"Why 20%? Why not 10% or half?"**

It is a trade-off with no correct answer. A bigger test set gives you a more trustworthy score but leaves fewer rows to learn from; a smaller one leaves more to learn from but the score gets noisy — with only 15 test flowers, one flower is worth nearly 7 percentage points. Twenty percent and twenty-five percent are the common defaults because they sit in a reasonable middle for datasets of a few hundred rows. With a million rows people often hold back 1%, because 10,000 test examples is plenty. **The real answer is "enough test rows that one row doesn't move your number much" — and 30, which is what we have today, is honestly not enough.** Say that out loud.

**"Is 42 special?"**

No. It is a joke — it is "the answer to life, the universe and everything" from *The Hitchhiker's Guide to the Galaxy* — and it became a habit. `random_state=0`, `=1`, `=7`, `=31` are all exactly as good. What matters is that it is **fixed**, so your result is reproducible, and that you chose it **before** you looked at the scores rather than after. Choosing the seed after you have seen the scores has a name in the trade and the name is not polite.

**"Does the model get better if I run it again?"**

No, and this is a genuinely important thing to get straight early. Running the file again does exactly the same arithmetic and produces exactly the same model. There is no gradual improvement, no practising, nothing that accumulates. The model is a function of the training data and the settings, full stop. If the score *does* change between runs, something is unfixed — almost always a missing `random_state`. Some models in Level 3 do improve over repeated passes; kNN is not one of them, and neither are trees or straight lines.

**"kNN keeps every training row forever. Isn't that a privacy problem?"** *(This one deserves a real answer.)*

Yes, and it is not a small one. A decision tree throws the data away and keeps only rules. kNN keeps **the actual rows**. So if you train a kNN model on medical records and then send that trained model to a hospital, you have not sent them a summary — you have sent them the records. And it is worse than that: somebody who can only *query* the model, without seeing inside it, can feed it carefully chosen inputs and work backwards towards what the training rows must have been. Which raises a hard question that Level 1's privacy lesson set up: if a person asks you to delete their data, is deleting the row enough, when their row is baked into a model you have already given to fifty people? People do not agree on the answer, and the law in most countries has not caught up.

**"Can I look at the test set just once, then change something, then look again?"**

Technically yes; honestly no. The instant you *change something because of what you saw*, the test set has helped you make a decision — which means it has taught you something, which means it is no longer data your process has never seen. Your score becomes a little optimistic and you cannot tell by how much. **Next week you are going to break this rule on purpose**, by trying 25 values of `k` and picking the best, and the deal will be that you write a sentence admitting it. That is the honest way to break it. Doing it quietly is not.

**"What if the vote is a tie?"**

With two classes and an even `k` it happens easily — 2-2 with `k = 4`. Scikit-learn breaks the tie by choosing whichever class comes first in sorted order, which is a rule rather than a principle: nothing about your data made that choice. So use an odd `k` when you have two classes. With three classes you can still tie (1-1-1 with `k = 3`) and the same arbitrary rule applies. It is not a scandal, but you should know that a tied prediction is essentially a coin flip that Python is pretending was a decision.

**"Which is better, a high training score or a high test score?"** *(Careful — this is a trap question and worth walking into.)*

Only the test score is a *score*. The training score is not really a measure of quality at all; it is a measure of how much the model memorised. It is still worth printing, but only as a companion to the test score, because the **gap** between them is the diagnosis. Train 0.94 / test 0.73 says "memorised". Train 0.82 / test 0.80 says "healthy but limited". Train 0.34 / test 0.30 says "this model has given up". **One number tells you nothing; the pair tells you what kind of trouble you are in.**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The student trains on the test set by mistake, and nothing crashes | The four names came back in the wrong order, or `fit(X_train, y_test)` slipped through | This is the silent bug of the week. Build the habit now: **after every `train_test_split`, print all four shapes and read them out loud.** A wrong order shows up instantly as a shape that makes no sense. |
| The 100% from `dishonest.py` is taken as success | It genuinely looks like success and the hook was fifteen minutes ago | Do not explain. Ask the one question and wait in silence: *"What is the nearest flower to flower number 7?"* The realisation has to be theirs. |
| The held-back score comes out *higher* and the lesson seems to have failed | It does come out higher on this split, and it is real | Have the answer ready and treat it as a feature of the lesson, not an accident. One flower is 3.3 points. Then do Part 3, where the gap is real. **Never fudge a number to make a lesson tidier.** |
| The envelope gets opened "just to check" | Curiosity, and it is only cards | Stop everything and make it the lesson. *"You've just done exactly the thing this whole week is about. Now we can't use those cards as a test set again — and that is a real thing that happens to real projects."* Then reseal with fresh cards. It costs three minutes and it lands harder than any explanation. |
| `n_neighbours` typed with a `u`, three times running | It is the correct English spelling | Sympathise, do not correct silently. Write `n_neighbors` on the SHAPES sheet and point at it. It is a genuinely irritating wart in the library. |
| The score changes every run and confidence collapses | `random_state` was forgotten | Excellent teaching moment — do not just fix it. Run the file four times, write the four different numbers down, and *then* add the seed. Seeing the wobble is worth more than being told about it. |
| Twenty minutes vanish into "so how does it know which is closest?" | It is a fair question and last week's answer has faded | One sentence and a pointer: *"It does exactly what you did last week — subtract, square, add, root — once for every training row."* Then move on. If they want the detail, that is the Differentiation → flying route. |
| `predict` gets called before `fit` | The lines got typed in the order the student was thinking, not the order they run in | The `NotFittedError` message is unusually helpful — read it out loud together. Then write **make → fit → predict** on the sheet. |
| The student wants to "improve" the model by trying every `k` and keeping the best | It is the obvious next move, and it is next week's lab | Say yes, and say when: *"That's exactly what we do next week, and there's a catch in it that you'll spot before I tell you."* Do not let them do it today; the honesty lesson attached to it needs its own airtime. |
| "Memorising" gets called "overfitting" because they read it somewhere | Word is everywhere on the internet | Credit it and hold the line: *"That's the right word and it's Week 33's word. For now say 'it memorised' — and in Week 33 you get to be the one who already knew."* |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** Part 3 of the activity. The envelope and one working `full_cycle.py` is a complete lesson and hits four of the five objectives.

**Cut:** the six-flower hand vote if the arithmetic is the blocker. Give them the sorted distance list already computed (Answer Key, under B2) and have them do only the counting. **The counting is the concept; the subtracting is last week's homework.**

**Reteach the split physically, twice.** Do the deck-and-envelope with cards, and then do it again with the twelve paper strips from Week 28. Put ten strips in one pile, two in an envelope. Then ask, pointing at the envelope: *"To mark this model, what do I need out of here?"* — the answers. *"And does the model get to see them?"* — no. Repeat that exchange, out loud, three times over the lesson. It is the single hardest idea of the week and it is a two-sentence exchange.

**Copy-this-exactly scaffold.** Every line correct, every expected output written in as a comment:

```python
# my_first_model.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(X_train.shape)      # you should see (120, 4)
print(X_test.shape)       # you should see (30, 4)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

print(model.score(X_train, y_train))    # you should see 0.9666666666666667
print(model.score(X_test, y_test))      # you should see 1.0
print(len(X_test))                      # you should see 30
```

They fix the first line whose output disagrees, and no others.

**The one thing you must not cut:** the envelope, and the sentence that goes with it. If the whole lesson collapses to one idea, make it *"you only find out if something works by testing it on things it has never seen."*

### If the student is flying

1. **Three personalities of `k`** (Variation — harder, item 1), with the predictions written down first. The `k = 120` collapse to 0.30 is the best number in the week.
2. **The `random_state` sweep** (item 2), then the killer question: *"If I got to choose which seed to publish, what could I claim?"*
3. **Find a flower it gets wrong** (item 3) and print its measurements. Then: *"Look at the numbers. Would you have got that one right?"*
4. **All six pairs of columns** (item 4), ranked, with the winner predicted in advance.
5. **Write kNN yourself, with no library.** They have everything they need: broadcasting (Week 18), `axis=1` (Week 19), `sorted` (Week 12), loops and `if` (Weeks 5–7). Compute the distance from one test flower to all 120 training flowers, sort, take the top 5, count the votes, and check the answer against `model.predict`. **This is a genuinely impressive thing for a 12-year-old to have done**, and if they get it working, that is the achievement of the term so far.
6. **The honest question, in writing:** *"You have a model with a training score of 1.0000. Write me three sentences on what you would need to know before believing it is any good."*

### If the student won't engage today

Do the deck and the envelope, and nothing else.

Then play **"Would You Believe It?"** — you read out a claim, they say believe or don't-believe, and *why*. Best of ten, keep score, no writing.

> "My spam filter is 99% accurate." *(Don't believe — what fraction of email is spam? If 99% is not spam, a machine that says 'not spam' to everything scores 99% and has never read an email.)* · "My model got 100% on the data it was trained on." *(Don't believe — it memorised.)* · "My model got 88% on 4,000 examples it had never seen." *(Believe — the honest shape of a claim: a number, and how many rows.)* · "My model got 100% on 3 examples it had never seen." *(Don't believe — three rows is not a test.)* · "I tried 40 settings and I'm reporting the best score." *(Don't believe, or at least discount it — the test set helped choose.)* · "My model is better than last week's because the score went up 2%." *(Don't believe without knowing the test size and whether the split was the same.)* · "I hid 20% of the rows before I started and only looked at them once." *(Believe.)* · "The score is different every time I run it." *(Don't believe any single one of them — nothing is fixed.)* · "My model scored 51% on a two-choice question." *(Don't believe it's learnt anything — a coin does that.)* · "I fixed the random seed after seeing which one gave the best score." *(Don't believe — that is choosing your test.)*

That game delivers objectives 4 and 5 completely, takes twelve minutes, and is genuinely fun. The code survives to next lesson; Week 30 opens by re-typing the split anyway.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — the vote (spoken)**

> "Five nearest neighbours to a new song. Nearest first: hype, chill, chill, hype, chill. What does the model predict with k equal to 3? And with k equal to 5?"

*Good answer:* k = 3 → hype, chill, chill → **chill** (2–1). k = 5 → hype, chill, chill, hype, chill → **chill** (3–2). **What to catch:** taking the nearest one and stopping (that is k = 1), or counting all five when asked for three. Have them read out only the top three, aloud, and tally on fingers.

**Check 2 — the three verbs (spoken)**

> "Which of `fit`, `predict` and `score` are allowed to see the right answers? Say why for each one."

*Good answer:* `fit` sees them, because that is how it learns. `score` sees them, because it has to mark the guesses. **`predict` does not** — if it did, there would be nothing to predict. Full marks needs `predict` correctly excluded **with the reason**. This is the check that separates level 3 from level 2 on the mastery scale.

**Check 3 — the two scores (written, 60 seconds)**

> "A model scores 0.98 on the rows it trained on and 0.71 on 40 rows it had never seen. Write down which number you'd put in a report, the gap, and one sentence saying what the gap tells you."

*Good answer:* Report **0.71, on 40 rows**. The gap is **0.27**, or 27 percentage points. One sentence: *the model did much better on the rows it had already seen, which means a lot of that 0.98 was memory rather than skill, so it will do about 0.71 on new data.* **What to catch:** reporting 0.98 (the whole week has failed), or getting the gap right but reading it backwards as "the test rows were harder". They were not harder; they were unseen.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot do the vote by hand. Thinks a training score is a score. Cannot say what `fit` does. |
| **2 — Emerging** | Does the vote when the distances are pre-sorted. Types the three lines from a model. Splits the data when reminded, but reports whichever score is higher. |
| **3 — Secure** | Explains kNN as a vote of the `k` nearest. Writes make/fit/predict unaided. Splits with `train_test_split`, reports **both** scores with the test row count, and says why the held-back one is the honest one. **This is the target.** |
| **4 — Strong** | Says what `random_state` is for without prompting. Explains why `k = 1` gives a training score of exactly 1.0. Reads a gap as a diagnosis rather than as two facts. Excludes `predict` from seeing answers, with the reason. |
| **5 — Exceptional** | Works out unprompted that `k` = the number of training rows makes the model ignore its input, and can say what it will score. Notices that 30 test rows makes each row worth 3.3 points, and therefore that small gaps are noise. Sees that a kNN model *is* its training data, and asks what that means for privacy. |

---

## 📤 Homework to Assign

**Say this:**

> "One program and one paragraph, about an hour.
>
> **The program — Build It, Parts 2 and 3 in your workbook.** Run the full cycle on iris, start to finish, from a blank file: load it, split it 80/20 with `random_state=42`, make a kNN with k equal to 5, fit it, and then print **two** scores. The score on the training rows, and the score on the held-back rows. And next to the second one, print `len(X_test)`, so the number of rows is right there beside the accuracy. I want to see that on screen, not implied.
>
> **The paragraph — two sentences, and this is the bit I'm actually marking.** Look at your two scores. Write down the gap. Then two sentences: what the gap means, and which of the two numbers you would tell somebody if they asked how good your model is. Two sentences. Not four. Making it short is part of the work.
>
> And one thing extra for anyone who wants it: run the same file again with `random_state=7` instead of 42, and write down what happened. Don't change anything else. One line about what that tells you."

**Workbook sections:** the workbook has no numbered pages, only named sections. In class: **Warm-Up, Predict the Output (P1–P4), Practice Set A (A1–A6), Build It Part 1** (the deck and the envelope). At home: **Build It Parts 2–6** (the full cycle, the two sentences, the `random_state=7` extra, the short questions, the Bug Log). If there is time or the student wants more: **Practice Set B (B1–B5), Fix the Broken Program, Puzzle of the Week, Think Deeper (T1, T2), Draw It** and the **Self-Check**.

**Expected time:** 20 min for the program (Build It Part 2) · 15 min for the two sentences (Part 3 — they will rewrite them, and should) · 10 min for the `random_state` extra (Part 4) · 15 min for the short questions and the Bug Log (Parts 5 and 6). About 60 minutes. The other sections are extra; each of them runs 10–25 minutes.

---

## 🔑 Answer Key

Every code block was run before it was pasted, and every output is real. This key follows the workbook's own section order and item labels, so you can mark straight down the page. The values are those in the workbook's Answers section; the teacher-only notes (wrong-answer maps, marking tips) are added underneath.

| Workbook section | Items | Where in this key |
|---|---|---|
| ✅ Warm-Up | W1–W5 | Warm-Up |
| 🔎 Predict the Output | P1–P4 | Predict the Output |
| ✍️ Practice Set A — Read It | A1–A6 | Practice Set A |
| ✍️ Practice Set B — Write It | B1–B5 | Practice Set B |
| 🐞 Fix the Broken Program | Bugs 1–3 | Fix the Broken Program |
| 🧩 Puzzle of the Week | Parts 1–2, (a)–(k) | Puzzle of the Week |
| 🤔 Think Deeper | T1, T2 | Think Deeper |
| 🛠️ Build It | Parts 1–6 | Build It (the homework) |
| 🎨 Draw It | — | Draw It |
| 📊 Self-Check | 8 can-dos, 14 true/false | Self-Check |

### Warm-Up

**W1.** Because `X` has to come back as a **table** and `y` as a single **column**. The inner brackets are a *list of names*, and asking a table for a list of names gets a table back. One name gets one column.

**W2.** `X.shape` = `(40, 3)` and `y.shape` = `(40,)`. Rows first, columns second; the lonely comma means "there is no second number".

**W3.** Subtract, square, add up, square root.

**W4.** The **function itself**, not the data. `iris.data` on it gives `AttributeError: 'function' object has no attribute 'data'`. The round brackets are what run it.

**W5.** **`bpm`.** It is written in the hundreds while `minutes` is under six, and squaring turns that gap into an enormous one. Nothing about the songs made bpm important; the units did.

*Teacher note:* W5 is Week 28's homework coming back. A student who says "because bpm is more important" has not yet absorbed the lesson of Week 28; it is worth one more sentence before Week 30, which is entirely about this.

### Predict the Output

**P1** (three committee sizes on six songs; mystery song at bpm 112, 4.0 minutes):

```text
k = 1  -> ['chill']
k = 3  -> ['hype']
k = 5  -> ['chill']
```

Two of the three agree, and the middle one disagrees with both of its neighbours. The six distances:

| song | bpm | minutes | mood | distance |
|---|---|---|---|---|
| 0 | 68 | 4.2 | chill | 44.00 |
| 1 | 72 | 5.1 | chill | 40.02 |
| 2 | 76 | 4.6 | chill | 36.00 |
| 3 | 148 | 3.1 | hype | 36.01 |
| 4 | 152 | 3.4 | hype | 40.00 |
| 5 | 160 | 2.8 | hype | 48.01 |

Sorted nearest first: chill (36.00), hype (36.01), hype (40.00), chill (40.02), chill (44.00), hype (48.01). `k = 1`: chill, 1–0. `k = 3`: chill, hype, hype, so hype 2–1. `k = 5`: chill, hype, hype, chill, chill, so chill 3–2.

**The pattern:** the mystery song sits almost exactly between the two groups, so every vote is a hundredth of a beat from flipping. The honest answer is "this song is between the two and the model cannot tell."

**P2** (what `train_test_split` hands back):

```text
4
(120, 4)
(30, 4)
(120,)
(30,)
```

Line 1: it hands back **four** things, always in one fixed order (catch them with two names and you get `ValueError: too many values to unpack (expected 2)`). The two lonely commas belong to `parts[2]` and `parts[3]`, the two `y` piles. Order: `parts[0]` is `X_train`, `parts[1]` is `X_test`, `parts[2]` is `y_train`, `parts[3]` is `y_test`. Both X's first, then both y's.

**P3** (two scores, one model; `k = 1`, two sepal columns):

```text
0.9416666666666667
0.7333
30
```

Report **0.7333, on 30 rows**, because it is the only one measured on flowers the model had never seen; the other is a memory test. The gap is 0.9417 − 0.7333 = **0.2083**, about 21 percentage points.

*Why line 1 is not exactly 1.0:* two columns were thrown away, and sepal measurements alone cannot always tell the species apart. There are **15 pairs** of flowers in the whole table with identical sepals but different species (`(6.3, 2.5)` is both a versicolor and a virginica). A training flower whose zero-distance neighbour is its look-alike of the other species is marked wrong; on the full four columns `k = 1` scores exactly 1.0. Full credit is any answer that says "some flowers look identical on these two columns but have different species"; the counts (15 pairs, 16 training flowers involved, 7 wrong) are for your interest only. The workbook includes the confirming `clashing_sepals.py`, which prints `pairs of flowers with identical sepals but different species: 15`.

**P4** (names in the wrong order):

```text
X_train (120, 4)
y_train (30, 4)
X_test  (120,)
y_test  (30,)
```

It does **not** crash. The impossible shapes are `y_train` (`(30, 4)`, a table where `y` should be a single line) and `X_test` (`(120,)`, a line where `X` should be a table); the "train" pile now has 120 measurements and 30 answers. Python did not complain because four names is the right *number*; Python hands over its four things in its own fixed order and lets you call them anything. The line to add every time:

```python
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
```

*Scoring the "/ 4" line:* the student's own count. The usual miss is predicting a crash. Treat that as the useful mistake it is and ask why it would crash.

### Practice Set A

**A1 — the vote on paper.**

| # | Neighbours, nearest first | k = 1 | k = 3 | k = 5 |
|---|---|---|---|---|
| a | chess, chess, art, chess, art | chess | **chess** (2–1) | **chess** (3–2) |
| b | art, chess, chess, chess, art | art | **chess** (2–1) | **chess** (3–2) |
| c | hype, chill, chill, chill, hype | hype | **chill** (2–1) | **chill** (3–2) |
| d | setosa, versicolor, versicolor, setosa, setosa | setosa | **versicolor** (2–1) | **setosa** (3–2) |
| e | chill, chill, hype, hype, hype | chill | **chill** (2–1) | **hype** (3–2) |

**A1(f).** Rows (b), (c), (d) and (e) change; only (a) stays the same. In (b), (c) and (d) the closest neighbour is the odd one out, a single example of one class sitting nearest with the other class in the majority just behind it. **That is exactly the situation a bigger `k` exists to protect you from:** one strange near neighbour should not decide the answer alone. Row (e) is the reverse: the two nearest agree and going from `k = 3` to `k = 5` lets three farther neighbours outvote them, so a bigger `k` is not automatically wiser.

**A1(g).** **Setosa**, the `k = 5` answer, because three of the five nearest are setosa including the very closest. The fuller answer: the 2nd and 3rd nearest are both versicolor (which is why `k = 3` says versicolor), so 3–2 is a close call and the right conclusion is "this one is uncertain". A model that reports a confident answer here is overstating what it knows.

**A1(h).** A **2–2 tie.** Scikit-learn breaks it by taking whichever class name comes first in sorted order, `art` before `chess`, so it says art. Nothing about the data chose that. Use an odd `k` with two classes.

**A2 — four shapes that must add up.**

| # | `X_train.shape` | `X_test.shape` | `y_train.shape` | `y_test.shape` |
|---|---|---|---|---|
| a | `(120, 4)` | `(30, 4)` | `(120,)` | `(30,)` |
| b | `(142, 13)` | `(36, 13)` | `(142,)` | `(36,)` |
| c | `(8, 2)` | `(2, 2)` | `(8,)` | `(2,)` |
| d | `(455, 30)` | `(114, 30)` | `(455,)` | `(114,)` |
| e | `(30, 3)` | `(10, 3)` | `(30,)` | `(10,)` |

**A2(f).** `X_train` and `y_train` (both 120 in row a), and `X_test` and `y_test` (both 30), because every row of measurements needs exactly one answer. If those differ, `fit` refuses with `ValueError: Found input variables with inconsistent numbers of samples`.

**A2(g).** The number of columns. `y` has no columns; it is a single line of answers, which is what the lonely comma in `(120,)` says.

**A2(h).** Never trust your arithmetic; check with `len()`. 20% of 178 is 35.6 and sklearn rounds the test set **up** to 36; 20% of 569 is 113.8, rounded up to 114. A student who computed 35 or 113 is not bad at arithmetic; they assumed.

**A3 — which calls see `y`?**

| The call | Answer | The reason |
|---|---|---|
| `model.fit(X_train, y_train)` | sees `y` | That is how it learns; for kNN it copies both down |
| `model.predict(X_test)` | does not | If it saw the answers there would be nothing to predict |
| `model.score(X_test, y_test)` | sees `y` | It has to, to mark the guesses |
| `train_test_split(X, y, ...)` | sees `y` | It cuts `y` into the same two piles as `X`, in the same order |

**A3(e).** `predict`: the only one whose whole job disappears if it can see the answer. **A3(f).** Marking. `y_test` is the answer sheet inside the sealed envelope, used once at the end; the model never sees it.

**A4 — find the bug.**

| # | The fix |
|---|---|
| a | `n_neighbors=5`: American spelling, no `u` |
| b | `model.predict([[3.0, 1.0]])`: double brackets, one row is still a table |
| c | Catch all four: `X_train, X_test, y_train, y_test = ...` |
| d | `model.fit(X_train, y_train)`: the matching `y`, not the other one |
| e | `from sklearn.neighbors import KNeighborsClassifier`: models live in rooms |
| f | `from sklearn.model_selection import train_test_split`: right function, wrong room |
| g | Add `random_state=42` (any fixed whole number) |
| h | Split first, then `fit(X_train, y_train)` and `score(X_test, y_test)` |

**A4(i).** **(g) and (h)**, the two that run without an error. **A4(j).** (g): the accuracy changes every run, so you cannot tell whether your change or the shuffle moved it. (h): the score comes back suspiciously high (with `k = 1`, exactly 1.0, because every flower's nearest neighbour is itself at distance zero). The symptom of this bug is a perfect result, which is why it is the dangerous one.

**A5 — the three boxes.**

| Slot | Answer |
|---|---|
| Box 1 | `fit`: given `X` and `y`, gives nothing back |
| Box 2 | `predict`: given `X` only, gives one guess per row |
| Box 3 | `score`: given `X` and `y`, gives back one number |
| Sees the answers? | 1: yes · 2: no · 3: yes, to mark |

**A5(a).** make, then fit, then use. Call `predict` before `fit` and you get `sklearn.exceptions.NotFittedError: This KNeighborsClassifier instance is not fitted yet.` **A5(b).** `fit`: for kNN it writes the training table down and stops. All the work happens in `predict`, which is why `fit` is instant and `predict` is the slow part.

**A6 — reading the traceback** (`ValueError: Expected 2D array, got 1D array instead`).

- One sentence of error: **three** lines, from `ValueError: Expected 2D array` to the end of the `reshape` advice; sklearn's messages wrap.
- "2D" means a table (rows and columns); "1D" means a single line of numbers.
- Your own line is the one with your own filename, `File "/Users/you/project/first_model.py", line 18`: one line out of nine.
- Why insist on a table: `predict` is built to answer thousands of questions in one call, so one question is a table with a single row. Outer brackets say "here is a table", inner ones say "here is the one row".
- Why two `reshape` options: sklearn genuinely cannot know whether `[3.0, 1.0]` is one row of two measurements or two rows of one. A library that refuses to guess is doing you a favour.
- The fix: `guess = model.predict([[3.0, 1.0]])`

### Practice Set B

**B1.** `model = KNeighborsClassifier(n_neighbors=7)`. At this point it knows **nothing**: an empty machine with a dial set to 7.

**B2.** The three-line program (the class's six flowers and the mystery flower at `(3.0, 1.0)`, `k = 3`):

```python
# six_flowers.py
# Three lines of scikit-learn, and one mystery flower.

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

six = np.array([[1.4, 0.2],
                [1.4, 0.2],
                [1.3, 0.2],
                [4.7, 1.4],
                [4.5, 1.5],
                [4.9, 1.5]])
names = np.array(["setosa", "setosa", "setosa",
                  "versicolor", "versicolor", "versicolor"])

model = KNeighborsClassifier(n_neighbors=3)   # 1. make it
model.fit(six, names)                         # 2. fit it
guess = model.predict([[3.0, 1.0]])           # 3. predict it

print("the model guesses:", guess)
```

```text
the model guesses: ['versicolor']
```

The answer comes back in square brackets because `predict` gives one answer per row asked about; `guess[0]` gets the string out alone.

*Teacher-only, the lesson's hand vote on the same six flowers.* The distances from `(3.0, 1.0)`, nearest first, which is the list to hand over if the arithmetic is the blocker (see Differentiation):

```
1.58  versicolor
1.75  versicolor
1.79  setosa
1.79  setosa
1.88  setosa
1.96  versicolor
```

`k = 1, 3, 5` gives versicolor, versicolor, **setosa**. The model measures all **six** distances to answer one question; that is why `fit` is instant and `predict` is the slow part. The two 1.79s are two different flowers (rows 0 and 1 of iris have identical petal measurements `(1.4, 0.2)`): two rows can be the same point without being the same thing. Confirm it in code:

```python
# check_page_292.py
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

six = np.array([[1.4, 0.2], [1.4, 0.2], [1.3, 0.2],
                [4.7, 1.4], [4.5, 1.5], [4.9, 1.5]])
names = np.array(["setosa", "setosa", "setosa",
                  "versicolor", "versicolor", "versicolor"])

for k in [1, 3, 5]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(six, names)
    print(f"k = {k}  ->", model.predict([[3.0, 1.0]]))
```

```text
k = 1  -> ['versicolor']
k = 3  -> ['versicolor']
k = 5  -> ['setosa']
```

**B3.** Cut the deck and check the arithmetic:

```python
# split_it.py
# Cut the deck, and prove the row counts add back up.

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("whole table :", X.shape)
print("train pile  :", X_train.shape, " answers:", y_train.shape)
print("test pile   :", X_test.shape, " answers:", y_test.shape)
print()
print("len(X_train) =", len(X_train))
print("len(X_test)  =", len(X_test))
print("120 + 30 =", len(X_train) + len(X_test))
```

```text
whole table : (150, 4)
train pile  : (120, 4)  answers: (120,)
test pile   : (30, 4)  answers: (30,)

len(X_train) = 120
len(X_test)  = 30
120 + 30 = 150
```

Why compute the last line instead of typing 150? A typed 150 would still say 150 if the split had gone wrong. A check that cannot fail is not a check.

**B4.** The full cycle, both scores (also the model answer to Build It Part 2):

```python
# iris_full_cycle.py
# Load it, split it, fit it, and report BOTH scores honestly.

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data                            # (150, 4)
y = iris.target                          # (150,)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)              # only the training pile

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("train score:", round(train_score, 4), "on", len(X_train), "rows")
print("test  score:", round(test_score, 4), "on", len(X_test), "rows")
print("len(X_test) =", len(X_test))
print("the gap    :", round(train_score - test_score, 4))
```

```text
train score: 0.9667 on 120 rows
test  score: 1.0 on 30 rows
len(X_test) = 30
the gap    : -0.0333
```

The gap is negative: the held-back score came out higher. With thirty test flowers each is worth 3.3 percentage points, so that is one flower's worth of luck. **Mark for:** both scores printed, `len(X_test)` printed, `random_state=42` present, `fit` called on the training pile only. A student whose numbers differ has almost certainly forgotten `random_state`; check that first.

**B5.** Every odd `k` from 1 to 25 on the two sepal columns (`choose_k.py`: the same split as B4 but `X = iris.data[:, 0:2]`, looping `for k in range(1, 26, 2)` and keeping the best test score). Real output:

```text
k =  1   train = 0.9417   test = 0.7333   gap = +0.2083
k =  3   train = 0.8667   test = 0.7667   gap = +0.1000
k =  5   train = 0.8250   test = 0.8000   gap = +0.0250
k =  7   train = 0.8000   test = 0.7667   gap = +0.0333
k =  9   train = 0.8083   test = 0.8000   gap = +0.0083
k = 11   train = 0.8083   test = 0.7667   gap = +0.0417
k = 13   train = 0.7750   test = 0.7667   gap = +0.0083
k = 15   train = 0.7583   test = 0.8333   gap = -0.0750
k = 17   train = 0.7833   test = 0.8333   gap = -0.0500
k = 19   train = 0.7917   test = 0.8667   gap = -0.0750
k = 21   train = 0.7917   test = 0.8667   gap = -0.0750
k = 23   train = 0.7917   test = 0.8333   gap = -0.0417
k = 25   train = 0.8083   test = 0.8667   gap = -0.0583

best k on the held-back rows: 19 at 0.8667
test rows: 30
```

The gap shrinks as `k` grows and then goes negative. At `k = 1` it is +0.2083 (twenty-one points of memory); by `k = 9` it is +0.0083 (one flower). Bigger committees cannot memorise: at `k = 1` the model copies its single closest neighbour, which on training rows is itself, whereas at `k = 19` nineteen flowers vote and no one flower can be memorised. The negative gaps at the end are still noise (30 test rows, 3.3 points per flower). *Marking note:* "best k = 19" is this split's answer only; `19` and `21` tie at 0.8667 and the loop keeps the first. Do not accept "19 is the best `k` for iris" as the conclusion.

### Fix the Broken Program

**Bug 1, the syntax error.** Did any of it run? **No.** There is no `Traceback` and nothing was printed; Python never started because it could not finish reading the file. The fix is to close the bracket after `random_state=42`:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

**Bug 2, the runtime error.** "Unexpected keyword argument" means "there is no setting by that name": the class refuses a named option it has never heard of rather than silently ignoring it. The spelling is not wrong in English; `neighbours` is correct English, but scikit-learn uses American English and wants `neighbors`. It is not the student's fault and it is permanent. Fix: `model = KNeighborsClassifier(n_neighbors=1)`.

**Bug 3, the silent one.** The numbers (train 0.925, test 0.9, gap 0.025) look good because they came from a model that had already seen the test flowers. The line is `model.fit(X, y)`, which fits on all 150 rows, including the 30 in the envelope. The number that moved most is the **test** score: 0.9 (buggy) against 0.7333 (correct), which is 16.7 percentage points or five flowers. The train score barely moved (0.925 against 0.9417). One sentence for what the buggy version measured:

> It was measuring how well the model could look up flowers it had already been given the answers to. Because `fit` saw all 150 rows, the 30 "held-back" flowers were in the model's notes, so scoring on them was a memory test dressed up as an exam.

The fix: `model.fit(X_train, y_train)`. The general lesson: **`fit` gets the training pile and nothing else**, and a bug that raises your score gets shipped, while one that lowers it gets found.

### Puzzle of the Week

**Part 1, twelve flowers and one mystery** (petal length and width; mystery at 5.2, 1.7).

**(a)** The four setosa rows have petal lengths of 1.3 to 1.5 and widths of 0.2, nearly four units away in the length column alone, so none can get into a top seven of anything. Skipping them is noticing, not laziness.

**(b)** The eight that matter:

| row | species | gaps | squares | total | distance |
|---|---|---|---|---|---|
| 50 | versicolor | −0.5, −0.3 | 0.25, 0.09 | 0.34 | **0.58** |
| 51 | versicolor | −0.7, −0.2 | 0.49, 0.04 | 0.53 | **0.73** |
| 52 | versicolor | −0.3, −0.2 | 0.09, 0.04 | 0.13 | **0.36** |
| 65 | versicolor | −0.8, −0.3 | 0.64, 0.09 | 0.73 | **0.85** |
| 100 | virginica | +0.8, +0.8 | 0.64, 0.64 | 1.28 | **1.13** |
| 101 | virginica | −0.1, +0.2 | 0.01, 0.04 | 0.05 | **0.22** |
| 102 | virginica | +0.7, +0.4 | 0.49, 0.16 | 0.65 | **0.81** |
| 103 | virginica | +0.4, +0.1 | 0.16, 0.01 | 0.17 | **0.41** |

**(c)** Sorted: 0.22 virginica · 0.36 versicolor · 0.41 virginica · 0.58 versicolor · 0.73 versicolor · 0.81 virginica · 0.85 versicolor · 1.13 virginica.

**(d)** The votes:

| `k` | Who votes | Tally | Answer |
|---|---|---|---|
| 1 | virginica | 1–0 | **virginica** |
| 3 | virginica, versicolor, virginica | 2–1 | **virginica** |
| 5 | virginica, versicolor, virginica, versicolor, versicolor | 2–3 | **versicolor** |
| 7 | + virginica, versicolor | 3–4 | **versicolor** |

**(e)** At `k = 5`. **(f)** Something like: "Not confident. The nearest neighbour is virginica, the second is versicolor, and they are 0.22 and 0.36 away. The answer flips as soon as the committee grows past three and even at `k = 7` the vote is only 4–3. The honest output is 'versicolor, but only just'."

**(g)** Confirmed by code; all four match the hand vote:

```python
# puzzle_29.py
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

petals = np.array([[1.4, 0.2], [1.4, 0.2], [1.3, 0.2], [1.5, 0.2],
                   [4.7, 1.4], [4.5, 1.5], [4.9, 1.5], [4.4, 1.4],
                   [6.0, 2.5], [5.1, 1.9], [5.9, 2.1], [5.6, 1.8]])
species = np.array(["setosa"] * 4 + ["versicolor"] * 4 + ["virginica"] * 4)

for k in [1, 3, 5, 7]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(petals, species)
    print(f"k = {k}  ->", model.predict([[5.2, 1.7]]))
```

```text
k = 1  -> ['virginica']
k = 3  -> ['virginica']
k = 5  -> ['versicolor']
k = 7  -> ['versicolor']
```

**Part 2, build a tie on purpose.**

**(h)** Two chess and two art at `k = 4` is a 2–2 tie, broken by taking whichever class name comes first in sorted order (`art` before `chess`). That is a rule, not a reason; a tied prediction is a coin flip that Python is pretending was a decision. **(i)** Yes: with three classes `k = 3` can come out 1–1–1.

**(j)**

| Number of possible answers | Smallest `k > 1` that cannot tie |
|---|---|
| 2 | **3**: any odd `k` works, because two whole numbers adding to an odd number cannot be equal |
| 3 | **There is no such `k`.** `k = 3` gives 1–1–1, `k = 6` gives 2–2–2, `k = 9` gives 3–3–3; odd `k` rules out only two-way ties (5 could be 2–2–1) |

**(k)** Partial. Odd `k` fully solves it for two classes and only reduces it for three or more; the honest fixes then are to report how close the vote was, or have the model say "uncertain" when the top two are level.

### Think Deeper

**T1.** Model answer:

> *If I train a kNN model on 5,000 patients and email it to a hospital, I have emailed them **the 5,000 records**. Not a summary, not a set of rules: the actual rows. `fit` copies `X_train` and `y_train` into the object and does nothing else, so opening the trained model is opening the table.*
>
> *And it is worse than that, because you do not need to open it. Somebody who can only **ask** the model questions can still work backwards: feed it a row, nudge one measurement and see when the answer flips. Every flip tells you roughly where a training row must be sitting, because the answer only changes when you cross the halfway point between two stored patients. Do that a few thousand times, systematically, and you can reconstruct an approximate map of where the real patients are, and an unusual patient is out on their own and very easy to locate.*
>
> *So deleting the row is **not enough.** The row is baked into every copy I have already sent, and I cannot recall fifty hospitals' files. To honour the deletion I would have to retrain from the reduced table and get all fifty hospitals to replace what they have, and I cannot force that. This is a real gap between what the law asks for and what the technology can do, and nobody has a clean answer to it.*
>
> *A decision tree throws the data away and keeps only a short list of yes/no questions, so sending a tree is sending rules, not records. **That is safer, but not safe**: the questions were chosen by looking at the patients, so an unusual patient can still leave a fingerprint in a very specific threshold. Less exposure, not zero.*

**Marking note:** full marks needs (1) the literal answer stated plainly, (2) a concrete method for the query-only attack, (3) an explicit "no, deleting the row is not enough" with the reason, and (4) the tree comparison with the honest caveat.

**T2.** Model answer:

> *The score can move 27 points because `train_test_split` shuffles before it cuts, and with only 30 flowers in the test pile each flower is worth 3.3 percentage points. A different shuffle puts different flowers in the envelope, and 27 points is only about eight flowers being easier or harder. Nothing about the model changed. **The number was never that precise in the first place.***
>
> *What they did wrong is not lying. Every number is real. **What they did is choose their test after seeing the result**, picking the friendliest of ten splits, which turns "how it behaves on rows nobody has seen" into "the best case out of ten". The dishonesty is in the **selection**, invisible in the number itself.*
>
> *Two honest alternatives. **One: fix the seed before you look, and report that one number.** It costs you the chance to flatter yourself. **Two: run all ten and report the range (0.6333 to 0.9000) or the average.** It costs you a nice headline, because "somewhere between 63% and 90%" is a weaker claim than "90%", but it is the true one.*
>
> *What catches it in real life: ask them to run it on a fresh split, or better, on data collected after they finished. They cannot have shopped for a seed on data that did not exist yet.*

**Marking note:** full marks needs (1) the arithmetic of why 30 rows is a short ruler, (2) explicit rejection of "they lied" with selection named as the fault, (3) two alternatives each with its cost stated, and (4) the fresh-split test. Spot checks on the three printed seeds (0 gives 0.6667, 4 gives 0.9000, 7 gives 0.6333) were re-run and match.

### Build It (the homework)

**Part 1, the physical split.** For a 52-card deck 20% is 10.4, so expect the student to round (10 in the envelope, 42 in the big pile, 10 + 42 = 52); for a 50-card set it is 10 and 40. Accept any pair that adds back to the counted deck. *Why shuffle (iris-specific):* the iris file is sorted by species, the first fifty rows all setosa, the next fifty versicolor, the last fifty virginica. Cut the last 20% off *that* without shuffling and the test pile is thirty virginica and nothing else, so the score says nothing about the other two species. Shuffling is what makes the test pile representative. *What you may do with the envelope:* open it **once**, at the very end. Open, look, change the model and check again, and it stops being data your process has never seen. The signature across the flap is a promise to yourself; the person it protects you from is you. If someone opens it, changes the model and reseals it, they have lost the only honest number they had, and not just a correct one: they no longer know *how wrong* it is.

**Part 2, the full cycle.** Model answer is B4 above. The table filled in:

| | Value | Row count |
|---|---|---|
| Score on the rows it studied | 0.9667 | 120 |
| Score on the rows it had never seen | 1.0 | 30 |
| **THE GAP** | −0.0333 | — |
| One test flower is worth… | **3.3** percentage points | — |

**Part 3, the two sentences.** Full-credit model answer:

> The gap is −0.0333: the model actually scored *higher* on the thirty flowers it had never seen than on the hundred and twenty it studied, which sounds impossible but only means the thirty it was given happened to be easy ones. With only thirty test flowers each one is worth 3.3 percentage points, so a gap this size is one flower's worth of luck rather than evidence of anything.

And for "which number would you tell somebody":

> The test score, 1.0000 on 30 rows, and I would always say "on 30 rows" out loud, because 100% on thirty flowers is a much smaller claim than 100% on thirty thousand.

**Mark the row count hard.** A student who writes "100%" with no denominator has missed the point of the week. The three self-checks in the workbook should read: names a number (yes), says the row count (yes), avoids "accurate" with no denominator (yes).

**Part 4, the `random_state=7` extra.**

```python
# seed_change.py
# The same file, one number changed.

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()
X = iris.data
y = iris.target

for seed in [42, 7]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    print(f"random_state={seed}:  train {model.score(X_train, y_train):.4f}"
          f"   test {model.score(X_test, y_test):.4f}   on {len(X_test)} rows")
```

```text
random_state=42:  train 0.9667   test 1.0000   on 30 rows
random_state=7:  train 0.9833   test 0.9000   on 30 rows
```

| `random_state` | train score | test score | test rows |
|---|---|---|---|
| 42 | 0.9667 | 1.0000 | 30 |
| 7 | 0.9833 | 0.9000 | 30 |

Points moved: **10.0** percentage points; flowers: **three**. Expected one-liner:

> Changing nothing except where the deck was cut moved the test score from 1.0000 to 0.9000, ten percentage points or three flowers, so a single accuracy from a single split is a much shakier number than it looks.

**Part 5, short questions.**

| # | Question | Answer |
|---|---|---|
| i | What does `fit` do for a kNN model? | Writes the training table down. That is genuinely all; there is nothing else inside a fitted kNN. |
| ii | What does `predict` get given? | An `X` only. No answers. |
| iii | What is `y_test` used for? | Marking the guesses. The model never sees it. |
| iv | What does `random_state` do? | Fixes the shuffle, so the same cut happens every run and your result is reproducible. |
| v | Why is a training score of 1.0 with `k = 1` not impressive? | Every training row's nearest neighbour is itself, at distance zero. It is arithmetic, not skill. |
| vi | What happens if `k` equals the number of training rows? | Every row votes on every prediction, so the model always says the commonest class and has stopped looking at its input. On iris that scores about 0.30. |
| vii | Why print `len(X_test)` next to the accuracy? | Because 100% on 30 rows and 100% on 30,000 rows are different claims wearing the same clothes. |
| viii | The four names, in order. | `X_train, X_test, y_train, y_test`. Both X's, then both y's. |

**Part 6, the Bug Log.** No fixed answer; mark for honesty and specificity. A good entry names the error message (or "none", for the silent bugs), the fix, and a concrete thing to check next time, such as "print all four shapes after the split".

### Draw It

There is no single right drawing. A good one has numbers on both piles that add back up to the whole (120 + 30 = 150) and three labelled arrows saying which pile each verb may touch. The tell that it is right: the `predict` arrow points at the test pile's **X** with something crossing out its **y**, and `score` touches both halves of the envelope. If all three arrows point at the same place, it has drawn the split without drawing the point of it. The tell that it is *good*: a note that each of the thirty rows is worth 3.3 percentage points.

### Self-Check

The eight can-do rows are self-rated, with nothing to mark. True or false:

| Statement | Answer | Why |
|---|---|---|
| kNN works out rules while it is fitting | **FALSE** | `fit` writes the table down and stops; there are no rules inside it |
| For kNN, `fit` is fast and `predict` is slow | **TRUE** | The opposite of most models; `predict` measures the distance to every stored row |
| Bigger `k` is always better | **FALSE** | At `k` = the number of training rows it always says the commonest class and scores about 0.30 |
| `model.predict([3.0, 1.0])` works for one flower | **FALSE** | `ValueError: Expected 2D array, got 1D array instead`; one row is still a table |
| `train_test_split` hands back four things | **TRUE** | Always four, always in the same order |
| The order is `X_train, y_train, X_test, y_test` | **FALSE** | Both X's first: `X_train, X_test, y_train, y_test` |
| Running the file again makes the model better | **FALSE** | Same arithmetic, same model; if the score changes, `random_state` is missing |
| A training score of 1.0 means the model is excellent | **FALSE** | With `k = 1` every row is its own nearest neighbour |
| `predict` is allowed to see `y` | **FALSE** | If it could, there would be nothing to predict |
| Without `random_state` you get a different score every run | **TRUE** | Different shuffle, different cut, different score |
| A test score higher than the train score means something is broken | **FALSE** | On 30 test rows it is one flower's worth of luck |
| `n_neighbours` is the correct spelling for scikit-learn | **FALSE** | It wants `n_neighbors` |
| The test set is a second thing to train on | **FALSE** | `X_train` and `y_train` go into `fit`, `X_test` into `predict`, and `y_test` only ever marks |
| Hiding 20% of your rows is wasteful | **FALSE** | 120 rows and 150 rows make nearly identical models, and a model whose accuracy you cannot honestly measure is worth nothing |

### Lesson questions posed in the Say-this scripts

- *"Does a machine that scores 100% by looking itself up understand flowers?"* → No. It memorised the list, and the 100% is what memorising looks like.
- *"Where have you met a worthless perfect score before?"* → Level 1: the sticker that said APPLE, and the wet umbrella.
- *"So how would you catch it out?"* → Test it on rows it has never seen. That is the whole rule.
- *"How much would you hide?"* → 20% is the usual choice. Not 90%, because then there is nothing left to learn from.
- *"Why did k = 5 change the answer from k = 3?"* → Two more setosa got votes and outnumbered the versicolors, 3–2. No distance changed.
- *"Which of the three verbs sees the answers?"* → `fit` (to learn) and `score` (to mark). Never `predict`.
- *"Why not train on all 150?"* → Because you would then have no honest way of measuring it. Slightly better and completely unmeasurable.
- *"150 rows, hide 20% — how many each side?"* → 120 and 30.
- *"What is `y_test` for?"* → Marking. It is the answer sheet inside the sealed envelope.
- *"2D array means what?"* → A table: rows and columns. 1D means a single line.
- *"Why does `predict` want a table for one flower?"* → It is built to answer thousands at once; one question is a table with one row in it.
- *"Why did the 100% happen?"* → Every flower's nearest neighbour is itself, at distance 0.
- *"How many things does `train_test_split` give back, in what order?"* → Four: `X_train, X_test, y_train, y_test`.
- *"Should 120 and 30 add to 150?"* → Yes, always. Nothing is discarded and nothing is in both piles.
- *"The held-back score came out higher. Is that a triumph?"* → No. One flower out of thirty is worth 3.3 points, so a gap that small is noise. Thirty is a short ruler.
- *"Which of the two scores would you tell somebody?"* → The held-back one, always, with its row count attached.

---

## 🔮 Next Week Preview

Week 30 is a lab, and it opens with something that looks like a bug. The student runs kNN on a real table of 178 Italian wines with thirteen chemical measurements each, and it scores about **78%** — respectable, and much worse than iris. Then they change nothing about the model, put every column onto the same footing, and run it again: **94%**. Sixteen points, for free, with no new features and no tuning. The reason is the thing they may already have spotted in Week 28: one of those thirteen columns, `proline`, is measured in the high hundreds while `hue` sits under two, and in a distance calculation the big column drowns out all twelve others. They will see the arithmetic that proves it — one column contributing 99.999956% of a distance. Then two more tools: `accuracy_score`, and the **confusion matrix**, which is Level 1's grid of what-got-mistaken-for-what, printed by the library, and which will show that the wine model is fine at two of the three grape types and nearly blind to the third. And there is a planted bug waiting in the second half: fit the rescaler on *all* the data before splitting, and the score goes **up**. The student's job is to explain why a higher score is the bad news.

**Prep early:** three things. **One — run `wine_choose_k.py` yourself before the lesson.** It is the longest-running file of the term (it trains fifty models) and it takes a few seconds on a slow laptop; you want to know that before twenty-five lines of output arrive on the shared screen. **Two — leave `THE GAP 0.2083` on the board.** Week 30 adds a second number under it. **Three — check that saving a PNG still works** (`fig.savefig(...)` from Week 25); the lab produces a chart and a broken save at minute 55 is a bad way to end a lab.

---

[⬅ Week 28](week-28.md) · [Course Home](../README.md) · [Week 30 ➡](week-30.md) · [Student Guide](../student-guide/week-29.md) · [Workbook](../workbook/week-29.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
