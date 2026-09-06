# Module 8 — How Computers Read and Chat: Words, Guesses, and Autocomplete

**Level 1 · Module 8 · ~3 hours · Prereqs: Module 2 (data as rows and columns), Module 3 (if-then rulebooks), Module 5 (models and confidence), Module 7 (turning a thing into numbers)**

[⬅ Previous](module-07-how-computers-see.md) · [Level 1 Home](README.md) · [Next ➡](module-09-fair-private-honest-ai.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** split any sentence into **tokens** and explain, with an example, why lowercase and punctuation change the count.
2. **You will be able to** build a next-word frequency table from a paragraph by hand and use it to generate brand-new sentences that were never in the paragraph.
3. **You will be able to** explain why a chatbot can be perfectly fluent and completely wrong at the same time — and demonstrate it with your own table.
4. **You will be able to** build a working Scratch chatbot driven by a lookup table you designed, and say honestly which family of AI it belongs to.
5. **You will be able to** explain why the same prompt can give a different answer twice, and control that behaviour deliberately.

---

## 🪝 The Hook

Open the messaging app on any phone. Type one word — say **"I"** — and stop. Above the keyboard, three suggestions appear.

Now do something slightly ridiculous: tap the middle suggestion. Then tap the middle suggestion again. And again. Twenty times, without thinking, without choosing. Read what you have written.

You will get something like: *"I am not sure if you want to go to the store and get a new one for me to be able to see you."*

Nobody wrote that sentence. You didn't — you tapped a key twenty times. The phone didn't understand it, mean it, or intend it. Yet it is grammatical English. It has subjects and verbs in the right places. Read aloud, it sounds like a person who has slightly lost their train of thought.

Here is the uncomfortable part. That is not a toy version of a chatbot. **That is the same idea as a chatbot**, running on a much smaller table. The gap between your keyboard and a modern chatbot is enormous in scale and tiny in concept. Today you build the concept — with a pencil, a tally sheet, and a bag of paper slips — so that the scale never fools you again.

---

## 🧠 The Concept

Five ideas, each with an anchor and small numbers you can check.

---

### 1️⃣ Text is data too — and tokens are the pieces we count

In Module 7 you turned a picture into numbers by chopping it into pixels. Text needs the same move: chop it into pieces you can count.

> **Corpus** — the collection of text you are learning from. (Plural: *corpora*. It just means "body of text".)
> **Token** — one piece of text after chopping. Usually a word, but punctuation marks count too.
> **Tokenize** — to chop text into tokens.

Chopping sounds trivial. It is not, and the decisions you make while chopping quietly change everything downstream.

**Decision 1: is punctuation a token?**

```
   "I love pizza!"

   punctuation glued on   →  [ I ]  [ love ]  [ pizza! ]           3 tokens
   punctuation separate   →  [ I ]  [ love ]  [ pizza ]  [ ! ]     4 tokens
```

If punctuation is glued on, then `pizza!` and `pizza?` and `pizza.` are three *completely different words* to the machine, with three separate counts. Your table gets bigger and every count gets smaller. Splitting punctuation off keeps `pizza` as one word — and gives you a bonus, because `.` becomes a token meaning **"a sentence ended here"**, which turns out to be enormously useful.

**Decision 2: does capital I mean the same as small i?**

To a computer, `Pizza` and `pizza` are as different as `Pizza` and `banana`. Different letters, different word. So most systems **lowercase everything first**.

```
   "Pizza is great. I love pizza."

   without lowercasing:  Pizza (1), pizza (1)   ← counted as two separate words
   with lowercasing:     pizza (2)              ← correctly counted as one word
```

But lowercasing loses real information. `Apple` the company and `apple` the fruit become identical. `Polish` (from Poland) and `polish` (for shoes) merge. You gain cleaner counts and pay in ambiguity. **There is no free choice here — only a trade you should make on purpose.**

**Decision 3: what about `don't`, `it's`, `New York`?**

`don't` could be one token, or two (`do` + `n't`), or three (`don` + `'` + `t`). `New York` is one place but two words. Real systems make these calls differently and it matters.

🍕 **Analogy — cutting a pizza.** The pizza is the same either way, but *how* you slice it decides what a "piece" is. Cut into 8 big slices and each piece has lots of toppings but you have few pieces. Cut into 40 squares and you have plenty of pieces but each one tells you almost nothing. Tokenizing is choosing your slice size for language.

**One more thing, so you are not surprised later.** Real chatbots do not slice into whole words. They slice into **sub-word pieces**: `unbelievable` might become `un` + `believ` + `able`, and `Ramanujan` might become `Ram` + `an` + `uj` + `an`. Why? Because that way a fixed list of about 50,000 pieces can spell *any* word ever written, including names and typos, without needing a word for each. A useful rule of thumb for English: **about 4 characters per token, so 100 tokens ≈ 75 words.**

For everything in this module, we use whole words plus punctuation. It is simpler and the idea is identical.

**Tiny concrete example — tokenize three sentences.** Rules: lowercase everything; `. ! ? ,` are their own tokens; keep contractions whole.

```
   "I love pizza!"          →  i / love / pizza / !            4 tokens
   "Do you love pizza?"     →  do / you / love / pizza / ?     5 tokens
   "I don't love olives."   →  i / don't / love / olives / .   5 tokens
                                                              ─────────
                                                              14 tokens total
```

Fourteen tokens, but only **10 unique** ones: `i, love, pizza, !, do, you, ?, don't, olives, .` — because `i`, `love` and `pizza` each appear twice. Tokens are what you count; unique tokens are what your table has rows for.

---

### 2️⃣ Counting words, then counting word pairs

Once text is tokens, you can do the thing you did in Module 2 with numbers: **count**.

> **Word frequency** — how many times each word appears in the corpus.

Frequency alone tells you something. In almost any English text, the most common words are `the`, `and`, `a`, `to`, `of` — words that carry almost no meaning by themselves. The interesting words are rarer. But frequency alone can never write a sentence, because it has no idea what goes *next to* what.

For that you count **pairs**.

> **Bigram** — a pair of tokens that appeared next to each other, in order. ("Bi" = two, "gram" = written thing.)
> **Trigram** — three in a row. **N-gram** — n in a row.

The order matters enormously. `hot dog` and `dog hot` are different bigrams. `ice cream` is common; `cream ice` is not.

**Tiny concrete example.** Corpus: `the big dog ate the big bone`  (7 tokens)

```
   word frequency                bigrams (6 of them)
   ──────────────                ────────────────────
   the   2                       the → big     (twice)
   big   2                       big → dog     (once)
   dog   1                       dog → ate     (once)
   ate   1                       ate → the     (once)
   bone  1                       big → bone    (once)
   ─────                         ────────────────────
   7 tokens                      6 pairs
```

Notice the count: **7 tokens make 6 pairs.** In general, *n* tokens make *n − 1* pairs, because every token except the last one has something after it. That is a good arithmetic check on your tally sheet.

Now turn the bigrams into a **next-word table** — one row per word, listing everything that ever followed it and how often:

| If the current word is… | it was followed by… | count | out of | chance |
|---|---|---:|---:|---:|
| **the** | big | 2 | 2 | 100% |
| **big** | dog | 1 | 2 | 50% |
| | bone | 1 | 2 | 50% |
| **dog** | ate | 1 | 1 | 100% |
| **ate** | the | 1 | 1 | 100% |
| **bone** | *(nothing — end of text)* | — | — | — |

🍕 **Analogy — the school corridor.** Stand at the door of the science lab every day for a month and write down where each person goes next. After a month you have a table: *from the science lab, 60% go to the canteen, 30% to the library, 10% outside.* You do not know why. You cannot read minds. But you can now make a very good guess about where the next person will go — and you built that ability out of nothing but tally marks.

---

### 3️⃣ Next-word prediction is the whole engine

Here is the trick that runs your keyboard, autocomplete, and every chatbot you have ever used:

> **Next-word prediction** — given the words so far, guess which word comes next. Then add that word to "the words so far", and guess again. Repeat.

That is it. There is no separate "understanding" step. Generating a paragraph is guessing the next word, four hundred times in a row, each guess feeding into the next.

```
   THE GENERATION LOOP

   ┌─────────────────────────────────────────────────────────────┐
   │                                                             │
   │   "the"  ──────►  look up "the" in the table                │
   │                       │                                     │
   │                       ▼                                     │
   │                  followers: cat 25%, dog 25%, mat 12.5%,    │
   │                             fish 12.5%, rug 12.5%,          │
   │                             bone 12.5%                      │
   │                       │                                     │
   │                       ▼                                     │
   │                  PICK ONE  ──────►  "dog"                   │
   │                       │                                     │
   │                       ▼                                     │
   │   "the dog"  ────►  look up "dog"  ────►  pick  ──►  "sat"  │
   │                       │                                     │
   │   "the dog sat" ──►  look up "sat"  ───►  pick  ──►  "on"   │
   │                       │                                     │
   │                       ▼                                     │
   │              ...until you hit "." or run out of patience    │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
```

**Where "prompt" comes in.** The words you type are simply the first few words of "the words so far". You are not giving the machine an instruction in the way you'd instruct a person — you are handing it the beginning of a text and asking it to continue. Everything a chatbot does, it does by continuing.

> **Prompt** — the text you give the model to start from.

**Two things a bigram table can do that feel impossible.**

*It can produce sentences that were never in the corpus.* From the mini-corpus in the Worked Example below — which contains only four sentences about a cat and a dog — you can generate `the dog sat on the mat`, a sentence that appears nowhere in the corpus. The table has *recombined* pieces. That is generation, not lookup, and it is the same reason a chatbot can answer a question nobody has ever asked before.

*It sounds like a person.* Not because it knows anything, but because it learned from a person's word choices, and word choices are most of what "sounding like a person" means.

**And one thing it definitely cannot do:** know whether what it said is true. Nothing in a tally sheet has any connection to the world.

---

### 4️⃣ Randomness: why the same prompt gives different answers

You have a table saying `the` is followed by `cat` 25%, `dog` 25%, `mat` 12.5%, `fish` 12.5%, `rug` 12.5%, `bone` 12.5%. Which do you pick?

There are two honest strategies, and they behave completely differently.

**Strategy A — greedy: always take the most likely.**

> **Greedy** — always pick the single highest-count follower.

Predictable, repeatable, and **it gets stuck**. Because if `the → cat` is the top choice, it is *always* the top choice, every single time you land on `the`. Watch what happens with the Worked Example corpus (ties broken by whichever appeared first):

```
   the → cat → sat → on → the → cat → sat → on → the → cat → ...
```

An infinite loop, forever. This is exactly why your phone's keyboard, if you tap the same suggestion long enough, often starts repeating a phrase in a circle. Greedy generation walks into ruts and cannot climb out.

**Strategy B — sampling: pick at random, weighted by the counts.**

> **Sampling** — pick randomly, but give each option a chance proportional to how often it actually occurred.

The cleanest way to do this by hand is a **bag of slips**. For the word `the`, write one slip for *every single time* a follower appeared:

```
   BAG FOR "the"   (8 slips, because "the" was followed by something 8 times)

     ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
     │ cat  │ │ cat  │ │ dog  │ │ dog  │       2 cat  → 2/8 = 25%
     └──────┘ └──────┘ └──────┘ └──────┘       2 dog  → 2/8 = 25%
     ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       1 mat  → 1/8 = 12.5%
     │ mat  │ │ fish │ │ rug  │ │ bone │       1 fish → 1/8 = 12.5%
     └──────┘ └──────┘ └──────┘ └──────┘       1 rug  → 1/8 = 12.5%
                                               1 bone → 1/8 = 12.5%
     shake, draw one without looking,          ───────────────────
     read it, PUT IT BACK                      8 slips = 100%
```

Drawing a slip gives you exactly the right probabilities, automatically, with no arithmetic. Put the slip back every time or the probabilities drift.

**This is the answer to "why does the same prompt give a different answer twice?"** Because the machine is *drawing slips*. Same bag, different draw. It is not being moody or thinking harder on Tuesdays. It is a weighted coin flip, made hundreds of times per reply.

🍕 **Analogy — the ice cream shop.** Greedy is a person who orders vanilla every single visit because vanilla is the most popular flavour: safe, boring, and they will never discover pistachio. Sampling is a person who spins a wheel weighted by how popular each flavour is: usually vanilla or chocolate, occasionally something surprising. Real chatbots have a dial between the two. Turned all the way toward greedy they become repetitive and dull; turned far the other way they become adventurous and start talking nonsense.

**Two practical rules you will need in the mini-project:**

- **Stop rule.** Stop when you draw `.` — or after 20 tokens, whichever comes first. Without a stop rule your generator runs until you die of boredom.
- **Dead-end rule.** If you land on a word that never had anything after it (the last word of the corpus), you must stop. It has an empty bag.

---

### 5️⃣ Fluency is not truth

Here is the most important idea in the module, and it is not a technical one.

Your bigram table can produce: **`the cat ate the bone .`**

Grammatically perfect. Every word in the right place. Sounds exactly like the other sentences. And it is not in the corpus, where the cat ate the *fish* and the dog ate the *bone*.

Nothing in your table objected. Nothing *could* object, because your table has no cats, no bones, and no world. It has counts.

> **Hallucination** — when an AI produces something that sounds right but isn't true. It is not lying (lying needs knowing the truth and choosing otherwise) and it is not a glitch. It is the system doing exactly what it was built to do: produce likely-sounding text.

**Why fluency and truth come apart.** The machine is optimising for one thing: *does this word plausibly follow those words?* Truth is a completely different question — *does this match the world?* — and there is no step anywhere in the process that checks it. A well-formed false sentence and a well-formed true sentence look identical to a next-word predictor, because they are both well-formed.

🍕 **Analogy — the confident tour guide.** Imagine a guide who has read thousands of tour scripts but has never visited the city. Ask about any building and out comes a fluent, well-paced, confident answer in perfect tour-guide rhythm. Most of it will be right, because most tour scripts are right. But when they don't know, they don't stop — they produce more tour-guide-shaped sentences, at the same confidence, in the same voice. **There is no wobble in their voice when they cross from true to false.** That missing wobble is the whole danger.

**What this means for you, concretely:**

| The AI says | Trust level | Why |
|---|---|---|
| "Here's a story about a dragon" | fine | there is no fact to get wrong |
| "Rewrite this paragraph more simply" | mostly fine | you can read the result and check it |
| "Water boils at 100°C at sea level" | probably fine | extremely common in the training text |
| "Your teacher's phone number is 555-0182" | **do not trust** | specific, checkable, about a real person |
| "This medicine is safe with that one" | **do not trust** | high stakes, and being wrong is irreversible |
| "The book *Silverfin Bridge* by Meera Rao says…" | **do not trust** | AI systems invent book titles, authors and page numbers extremely readily, because titles are just word patterns |

The pattern: **the more specific, checkable, and consequential a claim is, the less you should accept it without verifying.** Which is the opposite of how confidence feels to a reader — specific claims *sound* more trustworthy, not less.

---

## 🔍 Worked Example

**Goal:** take a four-sentence corpus all the way from raw text to three generated sentences, showing every tally mark and every draw.

### Step 1 — The corpus

```
   The cat sat on the mat. The cat ate the fish.
   The dog sat on the rug. The dog ate the bone.
```

### Step 2 — Tokenize

Rules: lowercase everything, `.` is its own token, no other punctuation present.

```
    1 the      8 the      15 the      21 the
    2 cat      9 cat      16 dog      22 dog
    3 sat     10 ate      17 sat      23 ate
    4 on      11 the      18 on       24 the
    5 the     12 fish     19 the      25 bone
    6 mat     13 .        20 rug      26 .
    7 .                   (then .)
```

Careful count: sentence 1 has 7 tokens, sentence 2 has 6, sentence 3 has 7, sentence 4 has 6.

```
   7 + 6 + 7 + 6 = 26 tokens
```

### Step 3 — Word frequency

| Token | Tally | Count |
|---|---|---:|
| the | ⦀⦀ ⦀⦀ ⦀⦀ ⦀⦀ | 8 |
| . | ⦀⦀⦀⦀ | 4 |
| cat | ⦀⦀ | 2 |
| dog | ⦀⦀ | 2 |
| sat | ⦀⦀ | 2 |
| on | ⦀⦀ | 2 |
| ate | ⦀⦀ | 2 |
| mat | ⦀ | 1 |
| fish | ⦀ | 1 |
| rug | ⦀ | 1 |
| bone | ⦀ | 1 |

Check: 8 + 4 + 2 + 2 + 2 + 2 + 2 + 1 + 1 + 1 + 1 = **26** ✓ (matches the token count)

**11 unique tokens** out of 26 total. Already interesting: `the` is 8 of 26 tokens — nearly a third of the whole text — and it means almost nothing on its own.

### Step 4 — Tally every bigram

Rule: we do **not** count a pair that crosses a `.`, because the word after a full stop starts a fresh sentence. So each sentence's pairs stay inside that sentence, and `.` is the last token of each.

```
   Sentence 1: the cat sat on the mat .
      the→cat   cat→sat   sat→on   on→the   the→mat   mat→.        6 pairs

   Sentence 2: the cat ate the fish .
      the→cat   cat→ate   ate→the   the→fish   fish→.              5 pairs

   Sentence 3: the dog sat on the rug .
      the→dog   dog→sat   sat→on   on→the   the→rug   rug→.        6 pairs

   Sentence 4: the dog ate the bone .
      the→dog   dog→ate   ate→the   the→bone   bone→.              5 pairs
                                                                   ────────
                                                                   22 pairs
```

Arithmetic check: 26 tokens − 4 sentences = 22 pairs. (Each sentence loses one pair at its end, and there are 4 sentences.) ✓

### Step 5 — The next-word table

| Current word | Next word | Tally | Count | Out of | Chance |
|---|---|---|---:|---:|---:|
| **the** | cat | ⦀⦀ | 2 | 8 | 25% |
| | dog | ⦀⦀ | 2 | 8 | 25% |
| | mat | ⦀ | 1 | 8 | 12.5% |
| | fish | ⦀ | 1 | 8 | 12.5% |
| | rug | ⦀ | 1 | 8 | 12.5% |
| | bone | ⦀ | 1 | 8 | 12.5% |
| **cat** | sat | ⦀ | 1 | 2 | 50% |
| | ate | ⦀ | 1 | 2 | 50% |
| **dog** | sat | ⦀ | 1 | 2 | 50% |
| | ate | ⦀ | 1 | 2 | 50% |
| **sat** | on | ⦀⦀ | 2 | 2 | 100% |
| **on** | the | ⦀⦀ | 2 | 2 | 100% |
| **ate** | the | ⦀⦀ | 2 | 2 | 100% |
| **mat** | . | ⦀ | 1 | 1 | 100% |
| **fish** | . | ⦀ | 1 | 1 | 100% |
| **rug** | . | ⦀ | 1 | 1 | 100% |
| **bone** | . | ⦀ | 1 | 1 | 100% |
| **.** | *(end)* | — | — | — | — |

Check the counts add to 22: the 8, cat 2, dog 2, sat 2, on 2, ate 2, mat 1, fish 1, rug 1, bone 1 = **22** ✓

Check the percentages within `the`: 25 + 25 + 12.5 + 12.5 + 12.5 + 12.5 = **100%** ✓

### Step 6 — Build the bags

One bag per word. For `the`, write eight slips: `cat`, `cat`, `dog`, `dog`, `mat`, `fish`, `rug`, `bone`. For `cat`, two slips: `sat`, `ate`. For `sat`, two slips both saying `on` — so drawing is pointless, the answer is always `on`. And so on.

### Step 7 — Generation run 1 (start word: `the`)

I will write out every draw. Yours will differ — that is the point of randomness.

| Step | Current word | Bag | Drew | Sentence so far |
|---:|---|---|---|---|
| 1 | the | 8 slips | **dog** | the dog |
| 2 | dog | sat, ate | **sat** | the dog sat |
| 3 | sat | on, on | **on** (forced) | the dog sat on |
| 4 | on | the, the | **the** (forced) | the dog sat on the |
| 5 | the | 8 slips | **mat** | the dog sat on the mat |
| 6 | mat | . | **.** (forced) | the dog sat on the mat . |

**Result: `the dog sat on the mat.`**

Is that sentence in the corpus? **No.** The corpus has *the cat sat on the mat* and *the dog sat on the rug*. Your table just built a new sentence by recombining pieces of two old ones. This is generation, and this is the moment worth stopping on: **a stack of tally marks produced a sentence that had never existed.**

### Step 8 — Generation run 2 (start word: `the`)

| Step | Current | Drew | Sentence so far |
|---:|---|---|---|
| 1 | the | **cat** | the cat |
| 2 | cat | **ate** | the cat ate |
| 3 | ate | **the** (forced) | the cat ate the |
| 4 | the | **bone** | the cat ate the bone |
| 5 | bone | **.** (forced) | the cat ate the bone . |

**Result: `the cat ate the bone.`**

Read it again. Perfect grammar. Correct rhythm. Same style as every training sentence. And **in the corpus, the cat ate the fish and the dog ate the bone** — this sentence is a confident statement of something the source text does not say.

Your tally sheet just hallucinated. On its second try. With eleven words of vocabulary.

### Step 9 — Generation run 3 (start word: `the`), with a warning attached

| Step | Current | Drew | Sentence so far |
|---:|---|---|---|
| 1 | the | **cat** | the cat |
| 2 | cat | **sat** | the cat sat |
| 3 | sat | **on** (forced) | the cat sat on |
| 4 | on | **the** (forced) | the cat sat on the |
| 5 | the | **cat** | the cat sat on the cat |
| 6 | cat | **sat** | the cat sat on the cat sat |
| 7 | sat | **on** (forced) | the cat sat on the cat sat on |
| 8 | on | **the** (forced) | ... on the |
| 9 | the | **rug** | the cat sat on the cat sat on the rug |
| 10 | rug | **.** (forced) | the cat sat on the cat sat on the rug . |

**Result: `the cat sat on the cat sat on the rug.`**

Grammatical nonsense. The generator went round the `the → cat → sat → on → the` circle once before escaping. It escaped only because sampling gave it a 6-in-8 chance of picking something other than a loop word each time it hit `the`. **Greedy generation would have gone round that circle forever** — you will prove this in Practice 5.

### Step 10 — Score the three runs

| Run | Output | Grammatical? | In the corpus? | True to the corpus? |
|---:|---|---|---|---|
| 1 | the dog sat on the mat. | ✅ yes | ❌ no | ✅ plausible — nothing contradicts it |
| 2 | the cat ate the bone. | ✅ yes | ❌ no | ❌ **no — the corpus says fish** |
| 3 | the cat sat on the cat sat on the rug. | ❌ no | ❌ no | ❌ meaningless |

### Step 11 — The verdict

Three sentences. **All three were fluent enough to read.** One was a genuinely useful new sentence, one was confidently false, one was garbage.

Notice that **the machine could not tell you which was which.** All three came out of the same bags by the same procedure with the same enthusiasm. If you want to know which is which, a human has to check — and that will still be true when the table has a trillion counts in it instead of twenty-two.

---

## 💻 Hands-On

Four activities. Budget about 75 minutes.

### Activity A — Interrogate your phone's keyboard (10 min)

1. Open any app you can type into. Clear the box.
2. Type `I` and stop.
3. Tap the **middle** suggestion 20 times. Do not choose, do not steer. Write the result down exactly.
4. Now start over with `The weather` and tap the middle suggestion 20 times. Write that down too.
5. One more, with your own name as the starting word.

Answer these in writing:

- Did the text ever start repeating a phrase in a loop? Write down the loop.
- Did any sentence come out true? Did any come out false but believable?
- The middle suggestion is roughly the "most likely next word". Which strategy from section 4 is that — greedy or sampling? What does that predict about loops?
- Your keyboard has learned from *your* messages too. Did anything appear that only you would say?

*What you should find:* loops appear almost every time, usually within 12 taps. That is greedy generation doing exactly what section 4 said it would.

### Activity B — Tally a paragraph by hand (20 min)

You need paper, a pencil, and a 60–80 word paragraph. Use a page from a book, song lyrics, or a paragraph you wrote yourself. Do **not** skip this and go straight to the spreadsheet — the tallying is where the idea lands.

**Step 1.** Copy the paragraph out, tokenized: lowercase, one token per line or separated by slashes, punctuation split off.

**Step 2.** Number your tokens. Write the total at the top. Then write down `total pairs = total tokens − number of sentences` and check it later.

**Step 3.** Rule up a tally sheet with three columns: **Current word · Next word · Tally**.

**Step 4.** Walk through your token list with a finger on each pair. For every pair, find that row (or add it) and make one tally mark. Do not batch, do not skip ahead — one pair, one mark.

**Step 5.** Add a **Count** column, then an **Out of** column (the row-group total), then a **Chance** column.

**Step 6.** Check your work three ways:
- Do all your counts add up to the pair count you predicted in Step 2?
- Within each current-word group, do the chances add to 100%?
- Find your most common word. Does it have the most followers? (It usually does.)

### Activity C — Do it again in a spreadsheet (20 min)

Now automate what you just did by hand, so you can trust it on a 200-word paragraph.

**Step 1 — Get tokens into a column.** Put one token per row in **A2 downward**. Fastest route: type your paragraph into a single cell somewhere out of the way, then use Find & Replace to turn every space into a line break — or honestly, for 60 tokens, just type them. Say your tokens end at **A61** (60 tokens).

**Step 2 — Make the "next word" column.** In **B2**, type:

```
=A3
```

Then fill B2 down to **B60**. (Stop at B60, not B61 — the last token has no next word.)

Column A is now "current word" and column B is "next word", lined up side by side. Every row is one bigram.

**Step 3 — List your unique words.** In **D2**, if you are in Google Sheets or Excel 365:

```
=UNIQUE(A2:A61)
```

That spills a list of every distinct token down column D. *(In LibreOffice Calc: copy A2:A61 into column D, then Data → More Filters → Standard Filter with "No duplications" ticked.)*

**Step 4 — Count how often each word appears.** In **E2**:

```
=COUNTIF($A$2:$A$61, D2)
```

Fill down as far as your unique list goes. Now you have a word frequency table, built in one formula.

**Step 5 — Count a specific pair.** Somewhere clear, say **G2** and **H2**, type a current word and a next word you want to check. Then in **I2**:

```
=COUNTIFS($A$2:$A$60, G2, $B$2:$B$60, H2)
```

Note the ranges stop at row 60, matching column B. `COUNTIFS` counts rows where **both** conditions hold — that is exactly "how many times did G2 come immediately before H2".

**Step 6 — Check it against your hand tally.** Pick three pairs you tallied by hand in Activity B and check that the spreadsheet agrees. If it doesn't, find out who is wrong before you go on. (In my experience the hand tally is wrong about a third of the time on the first pass, which is itself a useful lesson about human data entry.)

**Optional Step 7 — Let the spreadsheet draw the slips.** Suppose you want to sample a follower of `the` using the Worked Example counts. Lay out a small block: put the **cumulative starting number** in column K and the **follower word** in column L, sorted ascending by K.

```
        K        L
   2    0       cat
   3    2       dog
   4    4       mat
   5    5       fish
   6    6       rug
   7    7       bone
```

Each word's starting number is the running total of the counts before it (cat 2, dog 2, mat 1, fish 1, rug 1, bone 1 → starts at 0, 2, 4, 5, 6, 7; total 8). Now in **M2**:

```
=VLOOKUP(RAND()*8, $K$2:$L$7, 2, TRUE)
```

`RAND()*8` gives a random decimal from 0 up to 8. `VLOOKUP` with `TRUE` finds the largest K value that is less than or equal to it, and returns the word beside it. So a draw of 3.4 lands between 2 and 4 → **dog**, which is right, because dog owns the range 2 to 3.999. Press the recalculate key (F9 in Excel, or just edit any cell in Sheets) to draw again.

You have built a slip bag out of one formula. Copy M2 down ten rows and count how many `cat`s you get — with 25% odds, expect about 2 or 3 out of 10, and be unsurprised when you get 1 or 5, because ten draws is a tiny sample.

### Activity D — Build a Scratch chatbot (25 min)

Go to **scratch.mit.edu**, click **Create**. This bot answers questions using a lookup table you write.

**Step 1 — Make two lists.** In the **Variables** category, click **Make a List**. Create one called `triggers` and one called `replies`. Untick both checkboxes so they don't clutter the stage.

**Step 2 — Make two variables.** Create `i` (which row are we checking) and `matched` (did we find anything).

**Step 3 — Build the script.** Here it is in Scratch block notation. Every line is a real block you can find in the palette.

```
when green flag clicked

    delete all of [triggers v]
    delete all of [replies v]

    ┌─── the lookup table: 10 pairs, most specific FIRST ───┐

    add [pineapple]        to [triggers v]
    add [Pineapple on pizza is a war crime. Delicious, though.]  to [replies v]

    add [topping]          to [triggers v]
    add [We do cheese, mushroom, paneer, olive and corn.]        to [replies v]

    add [price]            to [triggers v]
    add [A medium is 250 rupees. A large is 400.]                to [replies v]

    add [how much]         to [triggers v]
    add [A medium is 250 rupees. A large is 400.]                to [replies v]

    add [deliver]          to [triggers v]
    add [We deliver within 5 km, usually in 30 minutes.]         to [replies v]

    add [open]             to [triggers v]
    add [We open at 11am and close at 11pm, every day.]          to [replies v]

    add [vegan]            to [triggers v]
    add [Yes! Ask for the vegan base and skip the cheese.]       to [replies v]

    add [thank]            to [triggers v]
    add [Any time. Come hungry.]                                 to [replies v]

    add [hello]            to [triggers v]
    add [Hello! Ask me about toppings, price, or delivery.]      to [replies v]

    add [bye]              to [triggers v]
    add [See you soon!]                                          to [replies v]

    └────────────────────────────────────────────────────────┘

    say [Hi, I am PizzaBot. Ask me something.] for (2) seconds

    forever
        ask [What would you like to know?] and wait

        set [i v] to (1)
        set [matched v] to (0)

        repeat until <<(i) > (length of [triggers v])> or <(matched) = (1)>>
            if <(answer) contains (item (i) of [triggers v]) ?> then
                say (item (i) of [replies v]) for (3) seconds
                set [matched v] to (1)
            end
            change [i v] by (1)
        end

        if <(matched) = (0)> then
            say [I don't know that one. Try asking about toppings, price, delivery, or opening time.] for (3) seconds
        end
    end
```

**Step 4 — Test it.** Click the green flag and try all of these:

| You type | Expected reply | Why |
|---|---|---|
| `hello` | Hello! Ask me about toppings… | matches trigger 9 |
| `What toppings do you have?` | We do cheese, mushroom… | `contains` finds "topping" inside "toppings" |
| `HOW MUCH IS A LARGE` | A medium is 250 rupees… | Scratch's `contains` ignores capitals |
| `Do you have pineapple as a topping?` | the pineapple joke | **pineapple is checked first**, so it wins |
| `what is the moon made of` | I don't know that one… | nothing matches, fallback fires |

**Step 5 — Three things to notice, and write down.**

1. **Order is a rule.** The loop stops at the first match, so `pineapple` beats `topping` only because it sits higher in the list. Move it to the bottom and the pineapple joke becomes unreachable. You have just rediscovered rule ordering from Module 3 — a rulebook where earlier rules win.

2. **`contains` is generous, sometimes too generous.** The trigger `open` also matches "how do I open the box" and "are you opening a new branch". Short triggers cause false matches. Find one embarrassing false match of your own and write it down.

3. **This is not machine learning.** Look back at Module 1's three families. You wrote every rule and every reply by hand — this is a **rule-based system**, and the bot learned nothing from anything. Your bigram table from Activity B *is* learned from examples. They feel similar to use and are built in completely different ways, and being able to tell them apart on sight is one of Level 1's whole objectives.

**Step 6 — Make it hybrid (optional, 5 min).** Add an eleventh entry: trigger `story`, and for the reply, paste in one of the sentences your bigram table generated in Activity B. Now the bot has a rule-based shell with one machine-generated line inside it. That mixture — hand-written scaffolding around a generated core — is how a surprising number of real products are actually built.

---

## ✍️ Practice

Six exercises. Show the tallies, not just the totals.

---

**1. [Warm-up] Tokenize carefully.**

Tokenizing rules: lowercase everything; `. , ! ?` each become their own token; contractions like `don't` stay whole.

```
   A:  "Wow! Pizza night!"
   B:  "Do you want pizza, or do you want pasta?"
   C:  "I don't want pasta."
```

(a) Write out the tokens for each sentence and give a token count for each.
(b) Give the total token count and the number of **unique** tokens across all three.
(c) If you had *glued* punctuation onto the previous word instead of splitting it, how many unique tokens would there be? Explain the difference in one sentence.
(d) If you had *not* lowercased, which token would have been split into two, and how would that change its count?

*Done looks like:* three token lists with counts, two totals, a recount for (c), and two written explanations.

---

**2. [Warm-up] Read a next-word table.**

Someone tallied a large corpus. Here is the row group for the word `the`:

| Next word | Count |
|---|---:|
| dog | 6 |
| cat | 3 |
| red | 2 |
| big | 1 |

(a) How many times was `the` followed by something? Show the addition.
(b) What is the chance the next word is `cat`? Give it as a fraction, a decimal, and a percentage.
(c) What is the chance the next word is **not** `dog`? Show two different ways of getting the answer.
(d) If you generate from `the` 60 times by sampling, roughly how many `red`s do you expect? Show the arithmetic, then explain in one sentence why you will probably not get exactly that number.
(e) Under **greedy** generation, how many different words could ever follow `the`? Answer in one sentence.

*Done looks like:* five answers with arithmetic shown, and (c) done two ways.

---

**3. [Build] Build a next-word table from scratch.**

Corpus:

```
   I like pizza. I like ice cream. You like pizza too.
   We eat pizza on Friday. We eat ice cream on Sunday.
```

Tokenizing rules: lowercase, `.` is its own token, no pairs cross a `.`.

(a) Tokenize and give the total token count.
(b) Predict the number of bigrams **before** you count them, using the token count and the sentence count. State the rule.
(c) Build the complete next-word table: current word, next word, count, out of, chance. Every word that has a follower needs a row group.
(d) Check your table two ways: do the counts add to your prediction from (b), and does each row group's chances add to 100%?
(e) Which word has the most different possible followers? What does that tell you about that word?

*Done looks like:* a token list with a count, a prediction with its rule, a full table, two checks, and one written answer.

---

**4. [Build] Generate three sentences with fixed dice rolls.**

Use your table from Exercise 3. Rules:

- When a word has only one possible follower, take it — no roll needed.
- When there is a choice, list the options in **alphabetical order** (`.` sorts before all letters), then roll one six-sided die:
  - **2 options:** rolls 1–3 → first option, rolls 4–6 → second option.
  - **3 options:** rolls 1–2 → first, 3–4 → second, 5–6 → third.
- Stop when you reach `.`.

Generate three sentences using exactly these rolls, in this order:

```
   Sentence 1, starting from "we":   rolls  5, 3, 2
   Sentence 2, starting from "i":    rolls  1, 6, 4
   Sentence 3, starting from "you":  rolls  6, 1
```

(a) Trace each sentence step by step in a table: current word, options in alphabetical order, roll used (or "forced"), word chosen.
(b) Write out the three sentences.
(c) For each one, say whether it appears in the original corpus.
(d) One of your sentences is brand new but perfectly sensible. Which, and why is that the interesting result?
(e) Invent a fourth sentence your table **could** produce that would be fluent but wrong about the world. Explain what makes it wrong.

*Done looks like:* three trace tables, three sentences, three yes/no answers, and two written explanations.

---

**5. [Stretch] Greedy versus sampling, proved.**

Use the **Worked Example** table (the cat/dog corpus, 22 pairs). Greedy rule: always pick the highest count; if two are tied, pick whichever appeared first in the corpus.

(a) Generate greedily starting from `the`, for 12 tokens. Write out the sequence. What happens?
(b) Explain in two sentences *why* it happens, referring to specific rows of the table.
(c) Prove that greedy can **never** produce the word `bone` from this table, no matter how long you run it. (Hint: work out which words greedy can ever reach.)
(d) Now sampling. Starting from `the`, what is the chance you get exactly `the dog ate the fish .`? Multiply the probabilities at each choice point and show them all. Give your answer as a fraction and a percentage.
(e) What is the chance of getting exactly `the cat sat on the mat .`? Compare it to (d) and explain the difference.
(f) One sentence: name a real situation where you would *want* greedy behaviour, and one where you would want sampling.

*Done looks like:* a 12-token greedy sequence, a proof for (c), two multiplied-out probabilities, and three written answers.

---

**6. [Stretch] Trigrams, and where hallucination actually comes from.**

**Part 1 — Build a trigram table.** Go back to the Worked Example corpus. A **trigram** table is keyed on the previous **two** words: given `(word1, word2)`, what came next?

(a) Build the trigram row groups for these five contexts: `(the, cat)`, `(cat, sat)`, `(sat, on)`, `(on, the)`, `(ate, the)`. Give counts and chances.
(b) **Prove** that the loop from Worked Example run 3 — `the cat sat on the cat sat on…` — is impossible under trigrams. Point at the exact row that makes it impossible.
(c) Show that the trigram table **still** allows `the cat ate the bone .`. Trace it. Then explain: how many words back would a model need to look to know that the cat should eat the fish?
(d) Real chatbots consider thousands of previous tokens, not one or two. Using your answer to (c), explain in three sentences why that helps enormously — and why it still cannot make hallucination impossible.

**Part 2 — Audit a fluent answer.** A chatbot is asked "Tell me about the Indian mathematician Srinivasa Ramanujan" and replies:

> "Srinivasa Ramanujan was born in 1887 in Erode, India. He had almost no formal training in mathematics but produced thousands of original results. He worked with G. H. Hardy at Cambridge. He published his most famous paper, *On the Partition of Whole Numbers*, in the *Journal of Applied Combinatorics* in 1917, on pages 44 to 61. He died in 1920 at the age of 32."

(e) Sort every claim into three buckets: **easy to check**, **hard to check**, and **suspiciously specific**. Explain what puts a claim in the third bucket.
(f) Describe exactly how you would verify the paper title, journal name, and page numbers — the actual steps, not "look it up".
(g) The reply is written in one confident voice throughout. Explain, using the next-word idea, why the true parts and any invented parts would sound *identical*.

*Done looks like:* five trigram row groups, a proof, a trace, a three-bucket sort of at least six claims, a verification procedure, and three written explanations.

---

## 🤔 Think Deeper

**1. Does a next-word predictor understand anything?**
Your tally sheet clearly does not understand cats. A modern chatbot can explain the plot of a book you just invented, translate a poem, and debug a program. At some point along that scale, does something we should call "understanding" appear — or is it "just" next-word prediction all the way up, and we are the ones fooled by the fluency?

*How to reason about it:* the trap is arguing about the word "understanding" instead of about behaviour. Try replacing the question with a **test**: name a specific thing that a system which understands could do, and a system that merely predicts could not. Then check whether your test is actually passable — many candidate tests ("it can be creative", "it can handle new situations") turn out to be things prediction handles fine, and other tests ("it knows when it doesn't know") turn out to be things many *humans* fail. Notice also that you cannot see inside a person's head either; you judge human understanding purely from behaviour too. Is that a fair reason to extend the same courtesy to a machine, or is it a reason to be suspicious of your own test?

**2. If it is fluent everywhere, where should we be allowed to use it?**
A chatbot writing a birthday poem, summarising your notes, and answering a question about a medicine all feel like the same activity from the outside — you type, it types back, in the same confident voice. But the cost of being wrong is wildly different. Should some uses be off-limits, and who decides?

*How to reason about it:* rank the uses along two separate axes rather than one. Axis 1: **how bad is a wrong answer** (mildly annoying → someone gets hurt). Axis 2: **how easily can the reader check it** (obvious immediately → requires an expert and a week). The dangerous corner is high harm *and* hard to check — and notice that is exactly where people most want help, because that is where they feel least confident. Then ask who bears the cost: is it the person who typed, the person written about, or someone who was never in the conversation?

**3. Whose words did the table learn from?**
Your bigram table came from a paragraph you chose. Real language models are built from enormous amounts of text scraped from the internet: books, forums, blogs, news, fan fiction, arguments. Almost none of those authors were asked. Is a model trained on someone's writing more like a student who read their book, or more like a copy of it?

*How to reason about it:* test the two analogies against details. When a student reads a book, they cannot reproduce it verbatim, they read a handful of books not a hundred million, and they don't compete commercially with the author. Which of those differences matters morally, and which is just a difference of scale? Then flip it: if we decided models may not learn from anything without permission, who could still afford to build one — and does that outcome make things fairer or less fair? You take this apart properly in Module 9.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Counting pairs across a full stop | You walk your finger along the token list mechanically and don't notice the `.` | Draw a physical line after every `.` on your token sheet before you start tallying. Then check: pairs = tokens − sentences |
| Forgetting to put the slip back | It feels natural to hold onto the slip you drew | Say "read it, put it back" out loud every draw. Not replacing it changes the odds on the very next draw |
| Getting the pair direction backwards | `dog → ate` and `ate → dog` look similar on a tally sheet | Label your columns **CURRENT** and **NEXT** in capitals and never write a pair without both headings visible |
| Thinking a fluent sentence must be a true one | Fluency is the only signal you get, so your brain uses it as evidence | Ask "is this checkable?" before "does this sound right?". Specific names, numbers and titles need verifying, always |
| Expecting the same prompt to give the same answer | It feels like a machine should be repeatable | Sampling means drawing a slip. Same bag, different draw. If you need repeatability you need greedy — and you will pay in loops |
| Using greedy and being surprised by loops | Greedy feels like "the best option every time" | Best-at-each-step is not best-overall. Trace 12 steps of greedy on any small table and you will usually find the circle |
| Making Scratch triggers too short | Short triggers match more, which feels efficient | `open` matches "opening", "opener" and "open the box". Use the longest trigger that still catches real questions, and test the embarrassing cases |
| Putting general Scratch triggers above specific ones | You add rules in the order you think of them | The loop stops at the first match, so specific triggers must go **above** general ones. Re-read Module 3 on rule ordering |
| Assuming a bigger table removes hallucination | More data feels like more truth | A bigger table makes text *more likely-sounding*, not more true. Nothing in the counting procedure checks reality — that is a missing step, not a small one |

---

## 🛠️ Mini-Project — The Human Language Model

**Time:** 70–90 minutes · **You need:** a 200-word paragraph, paper, pencil, a spreadsheet (optional), Scratch

### 🎯 Goal

Be the language model. Tally every word pair in a real 200-word paragraph, generate three new sentences by drawing from your own table, and then build a Scratch chatbot with a 10-entry response table — so that you have built one system that **learned** and one system that **was told**, and can explain the difference cold.

### 📋 Starter steps

**Part 1 — Choose and prepare your corpus (10 min)**

Pick a paragraph of about 200 words with a strong, consistent voice. Good choices: a chapter opening from a novel you like, the rules page of a board game, a sports report, song lyrics, a recipe, or a page of your own diary. Avoid anything with lots of numbers or names — they generate badly because each one appears exactly once.

Write your **tokenizing rules at the top of the page** before you start. For example:

```
   MY TOKENIZING RULES
   1. Lowercase everything.
   2. . ! ? are separate tokens and end a sentence.
   3. Commas are deleted entirely.
   4. Contractions (don't, it's) stay as one token.
   5. Numbers written as digits are kept as one token.
```

There are no correct rules. There are only rules you wrote down and followed consistently. Copy your paragraph out in tokenized form and number the tokens.

**Part 2 — Tally every pair (25 min)**

Rule up a sheet: **CURRENT · NEXT · TALLY · COUNT · OUT OF · CHANCE**.

Before you start, predict your pair count: `pairs = tokens − sentences`. Write the prediction at the top.

Now walk the list. One pair, one mark, no batching. This takes about 20 minutes for 200 tokens and it is the single most valuable 20 minutes in Level 1, because you will never again think a language model is doing something mysterious.

When done, fill in Count, then Out of (the group total), then Chance. Then run all three checks:

- [ ] Counts sum to your predicted pair count
- [ ] Each row group's chances sum to 100%
- [ ] Your most common word has the biggest row group

*Optional:* rebuild the whole thing with `COUNTIFS` from Activity C and compare. Finding your own hand-tally errors is a genuine result — write down how many you made.

**Part 3 — Generate three sentences (15 min)**

Make slip bags for the words you will need, or use the die method from Practice 4, or the `VLOOKUP(RAND()...)` formula. Whichever you pick, **write down which method you used** — that is part of the report.

Generate three sentences. Rules: start each from a word of your choice; stop at `.` or at 20 tokens, whichever comes first; **do not edit the output**, not even a little, not even when it is embarrassing.

For each sentence, record:

| # | Generated sentence | Length | Was it in the corpus? | Fluent? | True? |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Then write a short paragraph answering: **which sentence best shows that fluency and truth are different things, and why?** If none of your three happened to come out false, say so honestly and then construct one by hand from your table that *would* be false — that counts.

**Part 4 — Build the Scratch chatbot (25 min)**

Build the bot from Activity D, but with **your own topic** and **your own 10 trigger/reply pairs**. Good topics: your school, a game you play, a pet, a sports team, a hobby.

Requirements:

- Exactly 10 trigger/reply pairs
- Triggers ordered deliberately, with specific ones above general ones
- A fallback reply when nothing matches
- At least one reply that uses a **generated sentence** from Part 3

**Test it against a real human.** Hand the keyboard to someone who has not seen your table and ask them to have a 10-turn conversation. Record what they typed and what the bot answered. Count how many turns produced a sensible reply.

**Part 5 — The write-up (10 min)**

Half a page, answering these four:

1. Which of your two systems **learned from examples**, and which one **was told the rules**? Name the Module 1 family each belongs to.
2. Your bigram generator can produce sentences you never wrote. Your Scratch bot can only produce the 10 replies you typed. Which is more useful, and for what?
3. Give one specific example of your bigram generator sounding right and being wrong.
4. What would you need to add to *either* system to make it check whether what it says is true? Be specific — and notice whether your answer involves the counting procedure at all.

### ✅ Success criteria checklist

- [ ] Written tokenizing rules, followed consistently
- [ ] A 200-word paragraph tokenized and numbered
- [ ] A predicted pair count, written down before tallying
- [ ] A complete tally sheet with Current, Next, Tally, Count, Out of, Chance
- [ ] All three checks run, with any discrepancies found and explained
- [ ] Three generated sentences, unedited, in a scored table
- [ ] A paragraph on fluency versus truth citing one of your own sentences
- [ ] A running Scratch project with 10 trigger/reply pairs and a fallback
- [ ] A 10-turn transcript with a real human tester and a score
- [ ] The four-question write-up

### 🚀 Level it up

Pick one:

- **Go trigram.** Rebuild your table keyed on the previous **two** words instead of one. Generate three more sentences and compare them to your bigram sentences. They will be noticeably more fluent — and you will notice something else: many of your trigram contexts appear only once, so the "choice" is forced and the generator ends up quoting the original paragraph verbatim. That is a real phenomenon with a name you will meet in Level 2, and hitting it yourself is worth more than being told about it. Write down where the sweet spot seems to be for a 200-word corpus.
- **Two voices, one table format.** Tally a second 200-word paragraph in a completely different voice — a sports report and a fairy tale, say. Generate three sentences from each. Then give six unlabelled sentences to a friend and ask them to sort them into two piles. If they can, your tables captured *style* — using nothing but counts of which word follows which. Write down what specifically gave each voice away.

---

## 🔑 Key Takeaways

- **Text becomes data by tokenizing** — chopping it into countable pieces. Lowercasing and punctuation rules are choices with consequences, and you must write yours down.
- **A bigram table is just tallies of which word followed which.** *n* tokens produce *n − 1* pairs, which is your arithmetic check.
- **Next-word prediction is the entire engine**: guess a word, add it to the text, guess again. A prompt is just the beginning of the text you are asking it to continue.
- **Sampling versus greedy is a real dial.** Greedy is repeatable and gets stuck in loops; sampling gives variety and is why the same prompt gives different answers.
- **A tally sheet with 22 pairs can generate sentences nobody ever wrote** — recombination, not lookup. That is generation, and scale does not change the idea.
- **Fluency and truth are separate.** Nothing in the counting procedure checks reality, so a confident false sentence and a confident true one are produced by exactly the same process, in the same voice.
- **A rule-based chatbot and a learned generator feel similar and are built completely differently.** You built one of each today; be able to tell them apart on sight.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Corpus** | The pile of text you learn from | The four sentences about the cat and the dog |
| **Token** | One piece of chopped-up text — usually a word, sometimes punctuation | "I love pizza!" → `i`, `love`, `pizza`, `!` |
| **Tokenize** | To chop text into tokens | Splitting a paragraph into a numbered list of words |
| **Word frequency** | How many times each word appears | `the` appeared 8 times out of 26 tokens |
| **Bigram** | Two tokens that appeared next to each other, in order | `the → cat` is a bigram; `cat → the` is a different one |
| **Trigram** | Three tokens in a row | `(sat, on) → the` |
| **N-gram** | Any number of tokens in a row | A 5-gram uses the previous four words to guess the fifth |
| **Next-word prediction** | Guessing which word comes next, then repeating | The engine behind autocomplete and every chatbot |
| **Language model** | A system that predicts likely next words | Your tally sheet is one. So is a chatbot — just far bigger |
| **Prompt** | The text you give the model to start from | "Write me a poem about rain" |
| **Sampling** | Picking randomly, weighted by the counts | Drawing a slip from a bag of 8 |
| **Greedy** | Always picking the single most likely next word | Tapping the middle keyboard suggestion every time |
| **Context** | How many previous words the model gets to look at | A bigram sees 1 word; a chatbot sees thousands |
| **Hallucination** | When an AI says something that sounds right but isn't true | "The cat ate the bone" — fluent, and not what the corpus says |
| **Fallback** | The reply a rule-based bot gives when nothing matches | "I don't know that one. Try asking about toppings." |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Tokenize carefully

**(a) Token lists.**

```
   A:  "Wow! Pizza night!"
       → wow / ! / pizza / night / !                                   5 tokens

   B:  "Do you want pizza, or do you want pasta?"
       → do / you / want / pizza / , / or / do / you / want / pasta / ?  11 tokens

   C:  "I don't want pasta."
       → i / don't / want / pasta / .                                  5 tokens
```

**(b) Totals.**

```
   total tokens = 5 + 11 + 5 = 21
```

Unique tokens — list them and cross off repeats:

```
   wow, !, pizza, night, do, you, want, ",", or, pasta, ?, i, don't, .
```

That is **14 unique tokens**. (`!` appears twice in A, `do`/`you`/`want` appear twice in B, `want` and `pasta` reappear in C — 21 total, 14 distinct.)

**(c) With punctuation glued on.**

Retokenizing with punctuation attached to the previous word:

```
   A:  wow!  pizza  night!                                   3 tokens
   B:  do  you  want  pizza,  or  do  you  want  pasta?      9 tokens
   C:  i  don't  want  pasta.                                4 tokens
```

Unique tokens: `wow!`, `pizza`, `night!`, `do`, `you`, `want`, `pizza,`, `or`, `pasta?`, `i`, `don't`, `pasta.` = **12 unique**.

**The difference in one sentence:** gluing punctuation on gives a smaller total (16 tokens instead of 21) but splits real words into look-alike copies — `pizza`, `pizza,` and `pasta?` and `pasta.` are now four separate entries instead of two, so each one's count is smaller and the table learns less from the same text.

**(d) Without lowercasing.**

`Wow`, `Pizza`, `Do` and `I` would all keep their capitals. The one that genuinely splits is **`pizza`**: sentence A has `Pizza` (capital, sentence-start) and sentence B has `pizza` (lowercase, mid-sentence). Instead of one token with a count of 2, you get `Pizza` count 1 and `pizza` count 1.

Why that hurts: the model would build two separate row groups for what is obviously the same word, halving the evidence in each. With a big corpus this happens to every common word — `The` at the start of sentences versus `the` in the middle — and it is the single most common reason a beginner's frequency table looks strange.

---

### Exercise 2 — Read a next-word table

**(a) Total.**

```
   6 + 3 + 2 + 1 = 12
```

`the` was followed by something **12 times**.

**(b) Chance of `cat`.**

```
   fraction:    3/12  =  1/4
   decimal:     3 ÷ 12  =  0.25
   percentage:  0.25 × 100  =  25%
```

**(c) Chance the next word is not `dog`, two ways.**

*Way 1 — add up everything that isn't dog:*

```
   cat 3 + red 2 + big 1  =  6
   6 ÷ 12  =  0.5  =  50%
```

*Way 2 — subtract from 1:*

```
   P(dog) = 6/12 = 0.5
   P(not dog) = 1 − 0.5 = 0.5 = 50%
```

Both give **50%**. Doing it both ways is a genuine check: if they disagree, one of your counts is wrong.

**(d) Expected `red`s in 60 draws.**

```
   P(red) = 2/12 = 1/6 ≈ 0.1667
   60 × 1/6 = 10
```

Expect roughly **10**.

**Why not exactly 10:** each draw is an independent random event, not a schedule. 1/6 does not mean "one in every six" — it means "one sixth of the time, on average, in the long run". Over 60 draws you will very often see 7, 8, 12 or 13, and occasionally something further out. The more draws you make, the closer the proportion tends to get to 1/6, but the exact count is never guaranteed.

**(e) Greedy.**

Exactly **one**: `dog`, every single time, forever. Greedy always picks the highest count (6), so the other three followers can never be produced no matter how long you generate. Greedy discards 50% of the table's knowledge permanently.

---

### Exercise 3 — Build a next-word table from scratch

**(a) Tokenize.**

```
   S1: i / like / pizza / .                                 4 tokens
   S2: i / like / ice / cream / .                           5 tokens
   S3: you / like / pizza / too / .                         5 tokens
   S4: we / eat / pizza / on / friday / .                   6 tokens
   S5: we / eat / ice / cream / on / sunday / .             7 tokens
   ────────────────────────────────────────────────────────────────
   total = 4 + 5 + 5 + 6 + 7 = 27 tokens
```

**(b) Prediction.**

**Rule:** every token has a follower except the last token of each sentence, so

```
   pairs = tokens − sentences = 27 − 5 = 22 pairs
```

**(c) The complete next-word table.**

First, list the pairs sentence by sentence:

```
   S1:  i→like   like→pizza   pizza→.                                    3
   S2:  i→like   like→ice     ice→cream    cream→.                       4
   S3:  you→like like→pizza   pizza→too    too→.                         4
   S4:  we→eat   eat→pizza    pizza→on     on→friday    friday→.         5
   S5:  we→eat   eat→ice      ice→cream    cream→on     on→sunday
        sunday→.                                                          6
   ──────────────────────────────────────────────────────────────────────
                                                                         22
```

| Current | Next | Count | Out of | Chance |
|---|---|---:|---:|---:|
| **i** | like | 2 | 2 | 100% |
| **like** | pizza | 2 | 3 | 66.7% |
| | ice | 1 | 3 | 33.3% |
| **pizza** | . | 1 | 3 | 33.3% |
| | too | 1 | 3 | 33.3% |
| | on | 1 | 3 | 33.3% |
| **ice** | cream | 2 | 2 | 100% |
| **cream** | . | 1 | 2 | 50% |
| | on | 1 | 2 | 50% |
| **you** | like | 1 | 1 | 100% |
| **too** | . | 1 | 1 | 100% |
| **we** | eat | 2 | 2 | 100% |
| **eat** | pizza | 1 | 2 | 50% |
| | ice | 1 | 2 | 50% |
| **on** | friday | 1 | 2 | 50% |
| | sunday | 1 | 2 | 50% |
| **friday** | . | 1 | 1 | 100% |
| **sunday** | . | 1 | 1 | 100% |
| **.** | *(end)* | — | — | — |

**(d) Two checks.**

*Check 1 — counts add to 22:*

```
   i 2 + like 3 + pizza 3 + ice 2 + cream 2 + you 1 + too 1
   + we 2 + eat 2 + on 2 + friday 1 + sunday 1

   = 2+3+3+2+2+1+1+2+2+2+1+1 = 22   ✓  matches the prediction
```

*Check 2 — each group sums to 100%:*

```
   i:      100                       ✓
   like:   66.7 + 33.3 = 100         ✓
   pizza:  33.3 + 33.3 + 33.3 = 100  ✓ (rounding; exactly 3 × 1/3)
   ice:    100                       ✓
   cream:  50 + 50 = 100             ✓
   we:     100                       ✓
   eat:    50 + 50 = 100             ✓
   on:     50 + 50 = 100             ✓
   ...and the single-option groups are all 100%.
```

**(e) Most different followers.**

**`pizza`**, with three different followers (`.`, `too`, `on`). `like` also has a lot of *uses* (3 pairs) but only two distinct followers.

**What it tells you:** `pizza` is the most *versatile* word in this corpus — it turns up in the most different positions and contexts, so the generator has the most freedom right after it. Words with many different followers are the branch points of your generator; words with one follower are corridors you are forced down. If you want more variety in your output, you need more words like `pizza` — which really means you need a bigger, more varied corpus.

---

### Exercise 4 — Generate three sentences with fixed dice rolls

**(a) and (b) — the three traces.**

**Sentence 1, starting from `we`, rolls 5, 3, 2:**

| Step | Current | Options (alphabetical) | Roll | Chosen |
|---:|---|---|---|---|
| 1 | we | eat *(only option)* | forced | **eat** |
| 2 | eat | ice, pizza | **5** → 4–6 = second | **pizza** |
| 3 | pizza | ., on, too | **3** → 3–4 = second | **on** |
| 4 | on | friday, sunday | **2** → 1–3 = first | **friday** |
| 5 | friday | . *(only option)* | forced | **.** |

**Sentence 1: `we eat pizza on friday .`**

**Sentence 2, starting from `i`, rolls 1, 6, 4:**

| Step | Current | Options (alphabetical) | Roll | Chosen |
|---:|---|---|---|---|
| 1 | i | like *(only)* | forced | **like** |
| 2 | like | ice, pizza | **1** → 1–3 = first | **ice** |
| 3 | ice | cream *(only)* | forced | **cream** |
| 4 | cream | ., on | **6** → 4–6 = second | **on** |
| 5 | on | friday, sunday | **4** → 4–6 = second | **sunday** |
| 6 | sunday | . *(only)* | forced | **.** |

**Sentence 2: `i like ice cream on sunday .`**

**Sentence 3, starting from `you`, rolls 6, 1:**

| Step | Current | Options (alphabetical) | Roll | Chosen |
|---:|---|---|---|---|
| 1 | you | like *(only)* | forced | **like** |
| 2 | like | ice, pizza | **6** → 4–6 = second | **pizza** |
| 3 | pizza | ., on, too | **1** → 1–2 = first | **.** |

**Sentence 3: `you like pizza .`**

**(c) In the corpus?**

| # | Sentence | In corpus? |
|---:|---|---|
| 1 | we eat pizza on friday . | **Yes** — it is sentence 4, word for word |
| 2 | i like ice cream on sunday . | **No** — brand new |
| 3 | you like pizza . | **No** — the corpus says "you like pizza **too**." |

**(d) The brand-new sensible one.**

**Sentence 2: `i like ice cream on sunday .`**

Why it is the interesting result: the corpus never contains it, and it was assembled from pieces of three different source sentences — `i like ice cream` from sentence 2, `on sunday` from sentence 5, joined at the word `cream` which the two sentences happened to share. The generator found a shared word between two sentences and crossed from one to the other, like changing trains at a station that two lines both stop at.

And the output is not just novel, it is **sensible**: liking ice cream on Sunday is a perfectly reasonable thing to say. This is generation in miniature. The table did not memorise this sentence, it *constructed* it — and that is the entire reason a chatbot can answer a question nobody has ever typed before.

**(e) A fluent-but-wrong sentence.**

Several are available. `we eat pizza on sunday .` is a clean one:

```
   we → eat (forced)
   eat → pizza (a valid option)
   pizza → on (a valid option)
   on → sunday (a valid option)
   sunday → . (forced)
```

Perfectly legal under the table, perfectly grammatical. But the corpus says pizza is eaten on **Friday** and ice cream on **Sunday**. The table has separated `pizza` and `friday` by three steps, and a bigram table has no memory at all beyond one word, so by the time it reaches `on` it has completely forgotten that it said `pizza`.

Another good one: `i like pizza too .` — which sounds right, but "too" only ever appeared attached to `you`, implying agreement with someone else. The table cannot represent that, because meaning was never in it.

**The general lesson:** these outputs are wrong not because the table made an error but because **the table is working exactly as designed**. It stores which word may follow which. It stores nothing about what is true. Wrong answers are not a bug in the machinery, they are a consequence of what the machinery is.

---

### Exercise 5 — Greedy versus sampling, proved

**(a) Greedy from `the`, 12 tokens.**

Work through the Worked Example table, taking the highest count and breaking ties by first appearance in the corpus:

```
   the  → cat 2, dog 2 (tie) → cat appeared first (sentence 1) → cat
   cat  → sat 1, ate 1 (tie) → sat appeared first (sentence 1) → sat
   sat  → on 2 (only)                                          → on
   on   → the 2 (only)                                         → the
   the  → cat (same as before, the table never changes)        → cat
   ...
```

**The 12-token sequence:**

```
   the  cat  sat  on  the  cat  sat  on  the  cat  sat  on
```

It loops forever, in a cycle of length 4.

**(b) Why.**

Because the table is fixed and greedy is deterministic: every time the generator is at `the`, it consults exactly the same row and makes exactly the same choice. Four specific rows create the trap — `the→cat` (tie broken to cat), `cat→sat` (tie broken to sat), `sat→on` (forced, the only option), and `on→the` (forced, the only option) — so once you enter the cycle at `the`, there is no row anywhere in the table that could route you out of it.

**(c) Proof that greedy can never produce `bone`.**

Work out the set of words greedy can reach, starting from `the`:

```
   start:  the
   the  → cat        (deterministic)      reachable set: {the, cat}
   cat  → sat        (deterministic)      reachable set: {the, cat, sat}
   sat  → on         (deterministic)      reachable set: {the, cat, sat, on}
   on   → the        (deterministic)      reachable set: unchanged — we are back
                                          at a word we have already visited
```

Every word in the reachable set has now been expanded, and no new word appeared. **The complete set of words greedy can ever produce from `the` is `{the, cat, sat, on}`.** `bone` is not in it, so it can never be produced.

The deeper reason: greedy makes every decision the same way every time, so the sequence it produces is completely determined by the starting word. A deterministic walk on a finite table must eventually revisit a word, and the moment it does, it repeats the same cycle forever. It cannot reach anything outside that cycle. **`bone`, `mat`, `fish`, `rug`, `dog` and `ate` are all permanently unreachable** — that is 6 of the 11 vocabulary words, over half the table, thrown away.

**(d) Chance of exactly `the dog ate the fish .` under sampling.**

Start at `the`. List every point where a choice is made:

```
   the → dog     dog has 2 slips out of 8    P = 2/8  = 1/4
   dog → ate     ate has 1 slip out of 2     P = 1/2
   ate → the     forced (2 slips, both the)  P = 1
   the → fish    fish has 1 slip out of 8    P = 1/8
   fish → .      forced                      P = 1
```

Multiply:

```
   1/4 × 1/2 × 1 × 1/8 × 1  =  1/64
```

```
   1 ÷ 64 = 0.015625  →  1.5625%  ≈ 1.6%
```

**About 1.6%**, or once in every 64 attempts.

**(e) Chance of exactly `the cat sat on the mat .`**

```
   the → cat     2 slips of 8     P = 2/8 = 1/4
   cat → sat     1 slip of 2      P = 1/2
   sat → on      forced           P = 1
   on  → the     forced           P = 1
   the → mat     1 slip of 8      P = 1/8
   mat → .       forced           P = 1

   1/4 × 1/2 × 1 × 1 × 1/8 × 1  =  1/64  =  1.5625%
```

**Exactly the same: 1/64.**

**The comparison, and why it matters.** These two sentences are not equally good. `the cat sat on the mat .` is a **real sentence from the corpus**. `the dog ate the fish .` never appeared and is false with respect to the corpus (the dog ate the bone). Yet the generator produces them with **identical probability**.

That is the whole hallucination problem, expressed in arithmetic. The sampling procedure has no term anywhere for "was this actually in the source" or "is this true". It multiplies local probabilities, and a false sentence made of common local steps can easily be *more* likely than a true sentence made of rare local steps. Making the model bigger multiplies more numbers together; it does not add the missing term.

**(f) When you want each.**

*Greedy:* when you need the same input to give the same output every time and variety is worthless or harmful — a keyboard suggestion strip you want to build muscle memory for, a system converting a form into a standard sentence, or any situation where two people comparing their results must see the same thing.

*Sampling:* when you want variety and novelty — writing story ideas, brainstorming names, generating practice questions, or anything where the user might press "try again" and would be annoyed to get an identical answer.

---

### Exercise 6 — Trigrams, and where hallucination actually comes from

**Part 1**

**(a) The trigram row groups.**

First, list every trigram in the corpus (a context of two words, plus what followed):

```
   S1: the cat sat on the mat .
       (the,cat)→sat   (cat,sat)→on   (sat,on)→the   (on,the)→mat   (the,mat)→.

   S2: the cat ate the fish .
       (the,cat)→ate   (cat,ate)→the  (ate,the)→fish (the,fish)→.

   S3: the dog sat on the rug .
       (the,dog)→sat   (dog,sat)→on   (sat,on)→the   (on,the)→rug   (the,rug)→.

   S4: the dog ate the bone .
       (the,dog)→ate   (dog,ate)→the  (ate,the)→bone (the,bone)→.
```

The five requested groups:

| Context (previous two words) | Next | Count | Out of | Chance |
|---|---|---:|---:|---:|
| **(the, cat)** | sat | 1 | 2 | 50% |
| | ate | 1 | 2 | 50% |
| **(cat, sat)** | on | 1 | 1 | 100% |
| **(sat, on)** | the | 2 | 2 | 100% |
| **(on, the)** | mat | 1 | 2 | 50% |
| | rug | 1 | 2 | 50% |
| **(ate, the)** | fish | 1 | 2 | 50% |
| | bone | 1 | 2 | 50% |

**(b) Proof the loop is impossible.**

The bigram loop was `the → cat → sat → on → the → cat → …`. To go round again, the generator must produce `cat` immediately after `on the`.

Look at the row group for the context **`(on, the)`**. Its only possible next words are **`mat`** and **`rug`**. There is no `cat`, and there never can be, because in the corpus the words `on the` are followed by `mat` in sentence 1 and `rug` in sentence 3, and nowhere else.

So after `... sat on the`, the generator is forced to emit `mat` or `rug`, both of which are followed only by `.`, which ends the sentence. **The cycle is broken by the `(on, the)` row group, and the trigram generator physically cannot loop here.**

Why the extra word helped: the bigram generator standing at `the` had forgotten it just said `on`. The trigram generator remembers, and that single extra word of memory is enough to rule out the nonsense. **More context removes whole categories of error.**

**(c) `the cat ate the bone .` is still possible.**

Trace it:

```
   start:   the cat
   (the, cat) → ate      ✓ legal, 50% chance
   (cat, ate) → the      ✓ legal, forced (100%)
   (ate, the) → bone     ✓ legal, 50% chance
   (the, bone) → .       ✓ legal, forced (100%)

   output:  the cat ate the bone .
```

Every single step is legal. The overall chance is 1/2 × 1 × 1/2 × 1 = **1/4** — and note that is *higher* than the bigram version's chance was, because the trigram table is more confident about each step.

**Why the trigram cannot save us here.** At the moment of the critical decision, the generator's context is `(ate, the)`. The word `cat` is **three tokens back** — outside the two-word window. So the generator has no idea whether a cat or a dog is doing the eating, and both `fish` and `bone` look equally good.

**How far back would it need to look?** Count the positions in `the cat ate the ___`: the deciding word `cat` sits 3 tokens before the blank. So the model needs a context of at least **3 previous words** — a **4-gram** — for `(cat, ate, the)` to become its own row group, which would then contain only `fish` and would forbid `bone` entirely.

**(d) Why thousands of tokens of context helps enormously — and why it is not enough.**

Three sentences:

1. Every extra word of context turns a vague question ("what usually follows *the*?") into a much sharper one ("what follows *the* right here, in this specific situation, after all of that?"), which rules out enormous numbers of locally-plausible-but-globally-wrong continuations — exactly the way `(on, the)` ruled out the loop in part (b).
2. With thousands of tokens, a model can keep track of who is doing what, what it said three paragraphs ago, what you asked for, and what it already promised — so the crude errors your 2-word window produced simply do not survive.
3. But context can only enforce **consistency with the text in the window**; it can never enforce **agreement with the world**, because the world is not in the window — so if a false claim is consistent with everything said so far and consists of likely-sounding words, nothing anywhere in the procedure will flag it, and the model will state it in exactly the same confident voice as everything else.

The blunt version: more context fixes errors of *forgetting*. It does not fix errors of *not knowing*, because there is still no step that checks reality.

**Part 2**

**(e) Three-bucket sort.**

| Claim | Bucket | Why |
|---|---|---|
| Born in 1887 | **easy to check** | in every encyclopedia; a famous, widely repeated fact |
| Born in Erode, India | **easy to check** | same — widely published |
| Almost no formal training in mathematics | **easy to check** (roughly) | well documented, though "almost none" is fuzzy wording |
| Produced thousands of original results | **hard to check** | depends on what counts as a "result"; needs a real source and a definition |
| Worked with G. H. Hardy at Cambridge | **easy to check** | one of the most famous collaborations in mathematics |
| Paper titled *On the Partition of Whole Numbers* | **suspiciously specific** | a plausible-sounding title in exactly the right style for the era |
| Published in the *Journal of Applied Combinatorics* | **suspiciously specific** | a plausible-sounding journal name — and it is easy to make one up |
| In 1917, pages 44 to 61 | **suspiciously specific** | precise page numbers are almost never worth trusting from a generator |
| Died in 1920, aged 32 | **easy to check** | widely published |

**What puts a claim in the third bucket:** it is *precise*, it is *rare* in ordinary text, it has the *form* of a citation, and it would be *equally easy to generate whether or not it were true*. Titles, journal names, page numbers, dates of obscure events, URLs, quotes and statistics all share this shape. Common facts (born 1887) appear thousands of times in the training text and are heavily reinforced; a specific page range appears approximately never, so the model has nothing to reinforce and simply produces plausible-shaped numbers.

The cruel irony: **the specificity is what makes the sentence feel authoritative to a reader, and it is exactly what makes it least reliable.** Your instinct is inverted here and you have to override it deliberately.

**(f) How I would verify the paper, journal and pages.**

1. Search for the exact title in quotation marks in a library catalogue or an academic search engine. If nothing comes back with that exact phrasing, that is already a strong signal.
2. Separately, check whether the *Journal of Applied Combinatorics* existed in 1917 — search the journal name by itself. A journal that does not exist is the fastest possible disproof, and invented journal names are extremely common in generated text.
3. Look up an independent list of Ramanujan's publications — an encyclopedia entry, a university mathematics department page, or the collected papers — and see whether any 1917 paper matches.
4. If a real paper exists, find the actual page numbers from that independent source and compare. Do not compare against the chatbot's own answer, and do not ask the chatbot "are you sure?" — it will happily produce a confident confirmation drawn from the same process that produced the original claim.
5. Use **two independent sources** that do not copy from each other. Two websites that both copied the same wrong Wikipedia sentence are one source, not two.
6. Write down what you found for each part, including the parts that checked out. "Three of five claims verified, two could not be found" is a real, honest result and far more useful than "seems fine".

**(g) Why the true and invented parts sound identical.**

Because they were produced by the same process: at every single word, the system picked something that plausibly follows what came before. When it wrote "born in 1887" it was continuing a pattern it had seen thousands of times; when it wrote "pages 44 to 61" it was continuing the pattern of *what a citation looks like* — and a citation-shaped phrase with invented numbers is just as likely-sounding, word by word, as one with real numbers.

There is no separate confidence channel. A human writer who is unsure hedges — "I think", "around", "if I remember right" — because they have an internal sense of how sure they are and choose to express it. A next-word predictor has no such sense to express, so **there is no wobble in the voice at the exact moment it stops being right.** The style stays perfectly smooth across the boundary between true and invented, which means style tells you nothing at all, which means the only defence is checking.

---

</details>

---

[⬅ Previous](module-07-how-computers-see.md) · [Level 1 Home](README.md) · [Next ➡](module-09-fair-private-honest-ai.md)

*Next up: you have now built a model that sees, a model that guesses words, and a rulebook that pretends to chat. Every one of them learned from data that somebody chose. Module 9 asks the question that has been waiting since Module 2 — who is in that data, who is missing, and who gets hurt when the model is wrong.*
