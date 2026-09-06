# 📕 Teacher Orientation — Everything You Need, Before You Teach Anything

### *Read this once, cover to cover. About 45 minutes. Then you can teach all 36 weeks.*

[⬅ Back to the course](../README.md) · [Week 1 student guide](../student-guide/week-01.md) · [Figure style guide](../figures/STYLE.md)

---

## 🪝 You Do Not Need to Know AI to Teach This

Let me say that again, because you probably did not believe it the first time.

**You do not need to know anything about artificial intelligence to teach this course.** Not a
course, not a book, not a background in computing. Nothing.

Here is why that is true and not just encouraging noise:

1. **The subject is smaller than it sounds.** Almost all of practical AI rests on about six ideas.
   Data. Features and labels. Learning a pattern from examples instead of being told the rule.
   Testing on things you hid. Measuring honestly. Noticing who got left out. That is the whole
   spine of this course, and you will understand all six by the end of Section 2 of this file,
   which takes about twenty minutes.

2. **Every lesson is fully scripted.** The teacher file for each week gives you the exact words for
   the hard explanations, the exact numbers for the worked examples, a minute-by-minute plan, and
   the answer to every question a student can reasonably ask. You are not improvising.

3. **This course is not about AI facts.** It is about a habit of mind: *"how do you actually know
   that?"* You already have that habit. You use it on adverts, on news stories, on your child's
   claim that everyone else is allowed to stay up until eleven. Teaching it here is the same move
   pointed at a computer.

4. **Saying "I don't know" is part of the syllabus.** Section 8 of this file makes that concrete.
   A teacher who says "I don't know — here's how we'd find out" is teaching better science than one
   who bluffs. Your student will remember the honesty far longer than the fact.

### What is actually being asked of you

| You need to | You do NOT need to |
|---|---|
| Read the week's teacher file for 20 minutes before class | Read anything else, ever |
| Be able to count, divide, and turn a fraction into a percentage | Know any maths beyond that |
| Click a button in a browser | Install, configure, or code anything |
| Be willing to be wrong in front of a child | Be an expert |
| Care whether a number is honest | Care about the history of AI |

### One warning, and it is the important one

There is exactly one way to teach this course badly, and it is this: **teaching AI as a set of
impressive facts instead of a set of things you can check.**

If your student leaves this year able to say "a neural network has layers of neurons" but unable to
ask "out of how many photos?", the year was wasted. The whole point is the second question. Every
time you are choosing between covering more and checking more carefully, choose checking.

---

# 📖 Section 1 — The Whole of AI, in Twelve Short Chapters

This is your own mini-course. Read it straight through. Nothing here is beyond a careful adult, and
you will not need anything outside it for the entire year.

---

## 1.1 — What AI actually is

Forget robots. Forget brains. Here is the definition this course uses, and it is a good one:

> **Artificial intelligence** is a machine doing a job that used to need a person's **judgement**.

The load-bearing word is *judgement*. Judgement means a choice where reasonable people could
disagree, and the right answer depends on the specific case.

- Adding 47 and 88 is not judgement. There is one answer and no argument. A calculator is not AI.
- Deciding whether a photo is blurry enough to delete **is** judgement. Two people would draw the
  line differently. A phone that does this is doing AI.
- Deciding whether a text message is spam is judgement. Deciding whether a light is red is not.

This definition is useful because it is about **the job**, not about the technology. It stops you
having to know how something was built to decide whether it counts.

**What AI is not:**

| It is not | Because |
|---|---|
| A brain | It has no beliefs, no desires, no experience. It maps inputs to outputs. |
| Alive | It does not want anything, including to stay switched on. |
| Magic | Every step can be written down, and this course writes them all down. |
| One thing | "AI" covers spam filters, chess programs, photo taggers and chatbots. They share almost no machinery. |
| Conscious | Nothing in a current AI system has an inside. There is no view from in there. |

---

## 1.2 — The two ways a computer can get an answer

This is the most important distinction in the first third of the course, so make sure it is solid
in your own head.

**Way 1 — a rule-based system.** A human works out the rule and writes it down as if-then steps.
The computer follows them, exactly, forever.

```
   HUMAN thinks hard  ──►  writes IF-THEN rules  ──►  COMPUTER follows them  ──►  answer
```

A thermostat: `IF temperature < 20 THEN turn on the heat`. A spell-checker's underline:
`IF word is not in the dictionary THEN underline it`. A traffic light on a timer.

Rule-based systems are wonderful. They are predictable, explainable, and you can fix them by editing
one line. Most of the software in the world is rule-based, and that is correct.

**Way 2 — machine learning.** Nobody writes the rule. A human collects many **examples with the
correct answer attached**, and a program works out the rule for itself by studying them.

```
   HUMAN collects labelled examples  ──►  TRAINING  ──►  a MODEL  ──►  answer
```

Show a program 5,000 messages, each marked *spam* or *not spam*, and it will work out for itself
that "FREE" and five exclamation marks are suspicious. Nobody typed that rule. It fell out of the
counting.

**Why anyone bothers with way 2.** Rules work beautifully until the thing you are describing is
messy. Try writing if-then rules for "is this a photo of a cat". Pointy ears — so are foxes. Whiskers
— you cannot see them at that resolution. Fur — so is a rug. Every rule you add breaks two others.
The course spends four weeks (7–10) making the student feel this wall personally, because
understanding *why* machine learning exists is worth more than knowing that it does.

> **🧑‍🏫 The one-line version to say out loud:** "In the first kind, a person figures out the rule.
> In the second kind, the machine figures out the rule from examples. That's the whole difference."

---

## 1.3 — Data: everything a machine knows arrived as a table

Whatever an AI system knows, it arrived as **data** — recorded observations — and almost always in
the shape of a **table**.

```
   ┌────────────┬───────────┬──────────────┬─────────┐
   │ name       │ weight_g  │ colour       │ fruit   │  ← HEADER: names each column
   ├────────────┼───────────┼──────────────┼─────────┤
   │ item_01    │  150      │ red          │ apple   │  ← ROW: one example
   │ item_02    │  118      │ orange       │ orange  │
   │ item_03    │  205      │ yellow       │ banana  │
   └────────────┴───────────┴──────────────┴─────────┘
        ↑             ↑           ↑            ↑
      COLUMN: one thing measured for every example
```

Three words your student will use all year:

- **Row** — one example. One student, one photo, one message, one day.
- **Column** — one thing measured about every example.
- **Header** — the top row that names the columns.

The hardest bit for an 11-year-old is not the vocabulary. It is deciding **what one row is**. If
your table is about a week of your life, is one row a day? A meal? An hour? All three are valid and
they produce completely different tables. Week 4 spends most of its time here, and it should.

**Data is always a bit broken.** There are exactly four kinds of mess, and the course teaches all
four as findable, fixable things rather than as a vague warning:

| Mess | Looks like | Fix |
|---|---|---|
| **Missing** | An empty cell where a measurement should be | Record it as blank, honestly. Never invent a number. |
| **Duplicate** | The same example recorded twice | Delete one. Check whether it was a real repeat first. |
| **Impossible** | `sleep_hours = 88`, `weight_kg = -5` | Reality does not allow it. Find the typo or delete the row. |
| **Inconsistent** | `Mon`, `monday`, `MONDAY`, `M` all in one column | Write a **controlled vocabulary** — the list of allowed values — and enforce it. |

There is a fifth thing that looks like mess and is not: an **outlier**, a real value that sits far
from the others. 480 screen-minutes in a week of 150s might be a typo, or might be the day they were
ill on the sofa. You investigate outliers; you do not automatically delete them.

**And data comes from somewhere.** **Provenance** is the origin story — who collected it, from whom,
when, how, with whose permission. A dataset with no provenance is a rumour. Week 6 turns this into a
7-line *data card* the student writes themselves, and it is the single most professional habit in
the course.

---

## 1.4 — Features and labels

Here is the machine's-eye view of the world, and it is narrower than you think.

- A **feature** is one measured description of one example. One column. `weight_g = 150`.
- A **label** is the answer you want the machine to produce. Also a column — the one you cover up
  and try to predict. `fruit = apple`.

That is it. A machine learning problem is: *here are the features, here is the label, learn the
connection.*

**Not every feature is worth having.** Three kinds, and the middle one is the one adults miss:

| Kind | Definition | Example |
|---|---|---|
| **Useful** | Knowing it makes your guess better than guessing blind | `colour` for fruit — gets it right 91.7% of the time versus 33.3% blind |
| **Useless** | Knowing it changes nothing | `which quadrant of the bowl it sat in` — scores exactly the blind rate |
| **Leaky** | It already contains the answer, and it will not be there when you actually need it | `sticker_says = APPLE` |

Leaky features are the great embarrassment of real machine learning. A model that predicts whether a
patient has a disease using the column "was referred to the cancer ward" will score 99% in testing
and be worthless in a clinic. The student meets a toy version of this in Week 12 and it lands hard.

**Baseline** is the other idea to lock down. The baseline is the score you would get by always
guessing the most common label. Three equally common fruits? The baseline is 33.3%. If your model
gets 35%, it has learned essentially nothing, no matter how impressive 35% sounds. **Every accuracy
number in this course is reported next to its baseline, every time.**

**Two kinds of prediction:**

- **Classification** — "which one?" — from a short fixed list. Apple / orange / banana. Spam / not
  spam. This is what the student builds.
- **Regression** — "how much?" — a number on a sliding scale. "This orange weighs 197.5 g."

The same table does either. Cover the `fruit` column and it is classification. Cover the `weight_g`
column and it is regression. That flip, in Week 13, is one of the nicest moments in the year.

---

## 1.5 — Training, and what a model actually is

**Training** is a one-time process. You feed a program many labelled examples. It adjusts itself,
repeatedly, until its guesses on those examples are mostly right. Then it stops.

What comes out is a **model**: a guessing machine. Feed it a new input, get a guess out.

Three things about a model that adults get wrong and 11-year-olds get right once told:

1. **The examples are not inside it.** After training, the photos are gone. The model is a big pile
   of numbers that happen to work. It is not a database you can search.
2. **It cannot explain itself.** Ask a model why it said "cat" and there is no reason in there to
   report. Making models explain themselves is an active research problem, not a setting.
3. **It only knows what was in the examples.** All of a model's competence, and all of its blind
   spots, are inherited from its training data. Every single time.

An **epoch** is one complete pass over all the training examples. Teachable Machine defaults to 50
epochs — it looks at every photo fifty times. That is worth mentioning once; it demystifies the
progress bar.

**Confidence scores.** When a model classifies something, it does not output one answer. It outputs a
number for every class, and they add to 100%:

```
   spoon        ████████████████████████████░░░░░░░░░░░░░░░░  62%
   toothbrush   █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  21%
   comb         ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  17%
                                                       total = 100%
```

Say this sentence to yourself until it is automatic, because you will need it in about eight
different weeks:

> **A confidence score is how strongly the model prefers a class. It is not the probability that
> the model is right.**

A model can be 99% confident and wrong. This happens constantly, particularly on inputs unlike
anything it trained on. The **margin** — top score minus second score — is often more informative
than the top score alone: 62/21/17 is a comfortable win; 45/44/11 is a coin flip that happens to
have landed.

**Class balance.** If you train on 200 spoons, 200 toothbrushes and 8 combs, the model learns that
comb is a bad bet and mostly stops saying it. Roughly equal counts per class, or you are teaching
the model a prejudice by accident.

**Data quality beats data quantity.** Forty photos taken across five backgrounds, three lighting
conditions and eight angles will beat four hundred photos taken in one sitting on one table. This is
counter-intuitive and the course proves it experimentally in Week 18.

---

## 1.6 — Train, test, and the reason this course exists

This is the heart. If your student takes one thing from thirty-six weeks, make it this.

**Testing a model on the examples it trained on is cheating.** It is giving a student the exam paper
to revise from and then being impressed by their mark.

So: before you train anything, you hide some examples. Set aside about 20% — the **test set** — and
do not let the model near them. Train on the other 80% — the **training set**. Then, once, at the
end, you unseal the test set and score.

```
   100 photos
        │
        ├──────► 80 photos ─── TRAINING SET ───► training ───► MODEL
        │                                                        │
        └──────► 20 photos ─── TEST SET ────────────────────────►│
                 🔒 sealed, untouched, unseen              score them
```

The course makes this physical: the student puts printed photos in an envelope and **signs across
the flap**. Eleven-year-olds take sealed envelopes seriously in a way they do not take instructions
seriously.

**Accuracy** is just:

```
                 number of correct guesses          11
   accuracy  =  ───────────────────────────  =  ──────  =  0.733  =  73.3%
                    total number of guesses          15
```

The course always writes it three ways — fraction, decimal, percentage — and always shows the
division. The fraction matters most: `11/15` tells you there were fifteen tests, and `73.3%` hides
that. "95% accurate" out of twenty attempts is a very different claim from 95% out of twenty
thousand.

**Generalizing vs memorizing.**

| | Training accuracy | Test accuracy | Verdict |
|---|---|---|---|
| Generalizing | 88% | 84% | Learned the thing. Good. |
| Memorizing | 100% | 40% | Learned the photos, not the object. |

That second row is **overfitting**. The name sounds technical; the meaning is homely. The model
fitted the training examples so closely that it stopped working on anything else. The classic
schoolroom version: a model trained entirely on photos taken on a wooden table learns "wooden table",
scores 95% on the wooden table, and collapses to 34% at the kitchen sink.

**The gap** — training accuracy minus test accuracy — measures how much memorising happened. Small
gap, good. Twenty-plus points, worry.

**One number can hide a corpse.** Overall accuracy of 73% might be three classes at 100%, 80%, 40%.
The average looks acceptable while one class is broken. So you also compute **per-class accuracy**,
and you build a **confusion matrix**: a grid with the true class down the side and the predicted
class across the top.

```
                    PREDICTED
                 spoon  tbrush  comb
              ┌───────┬───────┬───────┐
   T  spoon   │   5   │   0   │   0   │   5/5 = 100%
   R          ├───────┼───────┼───────┤
   U  tbrush  │   0   │   4   │   1   │   4/5 = 80%
   E          ├───────┼───────┼───────┤
      comb    │   1   │   2   │   2   │   2/5 = 40%   ← the corpse
              └───────┴───────┴───────┘
   The diagonal (5 + 4 + 2 = 11) is everything it got right.
   Every off-diagonal cell is a specific, nameable mistake:
   "two combs were called toothbrush" — now go and look at those photos.
```

The confusion matrix is the single most useful object in the course, because it converts "it's a bit
rubbish" into "it confuses combs with toothbrushes, specifically, and here is why".

**Percentage points.** 73.3% minus 33.3% is **40 percentage points**, not "40 percent". The student
will get this wrong and so will most adults. Worth being fussy about; it recurs in the bias weeks.

---

## 1.7 — Why models make mistakes

There are only about six reasons, and every failure your student meets this year is one of them.

| # | Reason | What it looks like | Fix |
|:--:|---|---|---|
| 1 | **Not enough examples** | Wobbly, low confidence, changes its mind as you move | More examples |
| 2 | **Not enough variety** | Great on your desk, useless anywhere else | Same number of examples, more conditions |
| 3 | **Class imbalance** | One class almost never predicted | Even up the counts |
| 4 | **A leaky or spurious feature** | Suspiciously brilliant in testing, useless in real use | Find what it is really keying on and remove it |
| 5 | **The input is unlike anything it trained on** | Very confident and very wrong | Add an `other` class; set a confidence threshold |
| 6 | **The task is genuinely ambiguous** | Even humans disagree on the answer | Accept a ceiling below 100% and say so |

Notice something about that table: **five of the six are data problems, not model problems.** That
ratio is roughly right in professional practice too, and it is why this course spends far more time
on data than on models. When a student's model misbehaves, your first question is always the same:
*"Show me the photos."*

---

## 1.8 — What a neural network is (enough, and no more)

The course does not teach neural networks — that is Level 3 — but Teachable Machine uses one and
your student will ask. Here is the honest, sufficient answer.

A **neural network** is a big pile of very simple maths steps, arranged in layers, with thousands of
adjustable numbers called **weights**. That's the whole architecture.

The picture that works for an 11-year-old:

> Imagine ten thousand tiny switches wired up between the photo and the answer. At the start every
> switch is set randomly, so the answer is nonsense. Training shows the network a photo, sees how
> wrong the answer was, and nudges every switch a tiny bit in the direction that would have made it
> less wrong. Then it does that again with the next photo. Do it a few million times and the switches
> settle into positions that mostly give the right answer.

Three things to be careful about:

1. **The word "neuron" is a metaphor and a bad one.** A unit in a neural network is a weighted sum
   followed by a simple threshold. Real neurons are cells with chemistry, timing and history. The
   name is a historical accident from the 1940s. Say "it was named after brain cells, but it is not
   one" and move on.
2. **"Deep" just means "many layers."** Not profound. Not deep thinking. Deep as in a deep stack of
   pancakes.
3. **Nobody can read out the rule it found.** The knowledge is spread across thousands of numbers
   with no individual meaning. This is not laziness; it is the honest state of the field.

> **🧑‍🏫 If a student asks "is that how brains work?":** "We genuinely don't know how brains work.
> Neural networks were loosely inspired by a 1940s guess about brain cells, and they've drifted a
> long way since. Calling it a brain is like calling a plane a metal bird — it borrowed one idea
> and then went somewhere else."

---

## 1.9 — How a computer sees

A digital photo is a grid of numbers. There is nothing else in the file.

For a black-and-white image, each **pixel** — each tiny square — is one number from **0 to 255**.
0 is black, 255 is white, 128 is mid-grey.

```
       a 5×5 patch of an image, as stored:

       255  255  255  255  255          █ = 255 white
       255    0    0    0  255          ░ = 128 grey
       255    0  255    0  255          ▓ =   0 black
       255    0    0    0  255
       255  255  255  255  255     ← this is a hollow black square
```

For a colour image it is **three grids stacked**: one for red, one for green, one for blue. Each
pixel is three numbers. `(255, 255, 0)` is yellow, because red light plus green light makes yellow.
Each of the three grids is a **channel**.

**Resolution** is how many pixels: 224 × 224 is 50,176 pixels. Shrinking an image
(**downsampling**) averages blocks of pixels together, and the thrown-away detail is gone for good —
"enhance!" is a lie television tells.

**Filters** are the good bit. A filter (or kernel) is a tiny grid of numbers you slide over the
image. At each position you multiply the filter's numbers by the pixel numbers underneath and add up
the result. One number out, per position. Change the filter's numbers and you change what gets
highlighted.

```
   this filter                 ...highlights vertical edges,
   ┌────┬────┬────┐            because it computes
   │ -1 │  0 │ +1 │            (stuff on the right) − (stuff on the left).
   ├────┼────┼────┤
   │ -1 │  0 │ +1 │            Flat area  →  right ≈ left  →  answer ≈ 0
   ├────┼────┼────┤            Sharp edge →  right ≫ left  →  big number
   │ -1 │  0 │ +1 │
   └────┴────┴────┘
```

An **edge** is a place where brightness changes suddenly. Edges are the first genuinely useful thing
you can extract from a photo, and here is why they matter more than brightness: **turn on a lamp and
every brightness number changes, but the edges stay exactly where they were.** A vision system built
on edges survives a change of lighting. One built on raw brightness does not. Week 26 has the student
prove this with two lamps and a spreadsheet.

Real image models learn their own filters during training rather than being given them, and they
stack many layers of them. But the machinery is the one above, repeated. Nothing else appears.

---

## 1.10 — How a computer reads and chats, and what an LLM is

Text becomes numbers too, just less obviously.

First you **tokenize**: chop text into pieces. Roughly words, though real systems use word-fragments
so they can handle "unbelievability" and "Ramanujan".

```
   "I love pizza!"   →   [ i ] [ love ] [ pizza ] [ ! ]
```

Then — and this genuinely is the engine — you count **which token tends to follow which**. Take a
pile of text (a **corpus**) and tally every adjacent pair (a **bigram**):

```
   after "the" came:     cat  ×3     dog  ×2     mat  ×1
```

Now you can generate. Start with a word. Look up what usually follows. Pick one. Repeat.

If you always pick the most common option, that is **greedy** — and it is boring and loops. If you
pick randomly, weighted by the counts, that is **sampling**, and it is why the same prompt gives you
a different answer each time. Your student will find this genuinely surprising and it explains a lot
of chatbot behaviour in one stroke.

**A large language model (LLM) — ChatGPT, Claude, Gemini — is this, scaled up almost
unbelievably far.** The differences that matter:

| Your tally sheet | A large language model |
|---|---|
| A 40-word corpus | Trillions of words |
| Looks at the previous 1 word | Looks at thousands of previous words (**context**) |
| A tally table you can read | Billions of weights in a neural network, unreadable |
| Counts pairs | Learns deep statistical structure across whole documents |
| Also: guesses the next token | Also: guesses the next token |

That last row is the point. Scale changes what a next-token guesser can do to an astonishing degree —
it produces fluent argument, working code, decent translation. But the mechanism the student
tallied by hand in Week 28 is genuinely the mechanism. That is not a simplification for children;
it is the actual training objective.

**The consequence you must teach: fluency is not truth.** A next-word guesser optimises for
*plausible*, not *correct*. When it produces something confident and false — an invented book title,
a non-existent law, a wrong date — that is called a **hallucination**, and it is not a bug that will
be patched away. It is the same machinery working normally on a question where the plausible answer
and the true answer differ.

> **🧑‍🏫 The sentence to have ready:** "It's not lying. Lying needs you to know the truth and choose
> to say something else. It's guessing what a good answer would look like, and sometimes a good-looking
> answer isn't a true one."

Modern assistants add layers on top — human feedback training, safety filters, sometimes the ability
to look things up — which help a lot and do not change the underlying picture.

---

## 1.11 — Bias, in the only sense that matters here

Drop the word "bias" as a feeling. In this course it means one measurable thing:

> **Bias** is when a model works noticeably worse for some group than for others.

And it has, overwhelmingly, one cause: **who was missing from the training data.**

Worked example, and this is the exact one the student meets:

```
   TRAINING DATA, counted honestly
     photos taken in daylight, on a table    ............ 183
     photos taken under a lamp               .............  17
                                                          ────
                                                           200

   TEST RESULTS, by group
     daylight, on a table    11/12  =  91.7%
     under a lamp             5/12  =  41.7%
                                       ──────
     ACCURACY GAP  =  91.7 − 41.7  =  50.0 percentage points
```

Nobody was malicious. Nobody wrote a rule against lamps. Someone took photos in the afternoon
because that is when they had time, and the model inherited it. That is how nearly all real-world AI
bias happens: not through malice, through a gap in the data that nobody counted.

**A fairness audit** is the fix-finder. You decide the groups **before** you look at any results
(this matters — deciding afterwards lets you pick the flattering split), you test each group
separately with a decent number of examples, you compute per-group accuracy, and you report the gap
in percentage points. Then you trace each gap back to a count in the training data, and you price the
fix: *"about ninety more lamplight photos."*

Two more things worth having in your head:

- **False rejects and false accepts hurt different people.** A face-recognition attendance system
  that fails to recognise a present student (a false reject) marks a child absent. Which error you
  minimise is an ethical choice, not a technical one.
- **Fixing one group often costs another slightly.** Retrain with more lamplight photos and daylight
  accuracy typically dips a point or two. That is a real trade-off, and being able to show it as a
  before-and-after table is genuinely impressive work for Grade 6.

---

## 1.12 — Privacy, fakes, and trusting too much

Four ideas, all of which land better as stories than as rules. The course supplies the stories.

**1. "Anonymous" often isn't.** Take away the name and you have not necessarily hidden the person.
*Year 7 + postcode + left-handed + plays the trombone* narrows eight hundred students to one. This is
**re-identification**, and Week 32 runs it as a game the student wins in about ninety seconds, which
is the point.

**2. Files carry hidden information.** A photo from a phone usually stores **metadata** — the time,
the camera, often the GPS coordinates. Sharing a photo can share your address without you sharing
your address.

**3. Fakes are cheap now.** A **deepfake** — a fabricated photo, video or voice of a real person — no
longer requires a studio. The defence taught here is not "spot the pixels", which stops working every
few months. It is **provenance**: who first posted this, when, and does any independent source have
it? That defence does not expire.

**4. Over-trust is the biggest everyday risk.** Not robot uprisings. People copying a confident wrong
answer into their homework, or following the satnav into a river. There is a name for it:
**automation bias** — trusting the machine over your own judgement. The antidote taught all year is a
reflex: *how would I check that?*

---

# ❓ Section 2 — The 20 Questions Students Will Ask

These come up. Not "might" — do. Here is a short, honest, correct answer for each. You can read
these aloud verbatim.

**1. "Is it alive?"**
No. Being alive means growing, using energy to stay organised, and eventually dying. A model does
none of those. When you switch it off nothing is lost, because there was nothing in there having a
time.

**2. "Does it think?"**
Not in the way you do. It does something that produces useful answers, but there is no inner voice,
no daydreaming, nothing happening between your questions. It is only doing anything while it is
answering.

**3. "Is ChatGPT the same as AI?"**
No — ChatGPT is one kind of AI, the same way a labrador is one kind of animal. The spam filter on
your email is AI. The thing that recommends videos is AI. Chatbots are the loudest kind right now,
not the only kind.

**4. "Will it take my job?"**
Some jobs, yes — that has happened before with other machines, and it was hard for the people
involved. It usually changes jobs more than it deletes them: fewer people typing things up, more
people checking whether the machine got it right. The safest skill is being the person who can tell
when the answer is wrong. That is literally what this course teaches.

**5. "Can it lie?"**
Lying means knowing the truth and choosing to say something else. It does not know the truth, so no.
But it will absolutely say false things with total confidence, which can hurt you just as much. We
call that a hallucination.

**6. "Is it smarter than me?"**
It is better than you at exactly one narrow thing, and completely blank outside it. AlphaGo beat the
best Go player alive and cannot play checkers, or tie a shoelace, or know it won. You can learn
checkers this afternoon.

**7. "Could it become evil / take over?"**
Nothing today is remotely close to that, and the systems we build have no wants at all. The real
present-day harms are less dramatic and much more likely: a system that works worse for some group of
people, a fake video that fools someone, a person trusting a confident wrong answer.

**8. "How does it know what a cat is?"**
It doesn't, in your sense. Somebody showed it many thousands of pictures with "cat" written next to
them, and it found patterns of light and dark that reliably go with that word. Show it something odd
enough and it will confidently call a cushion a cat.

**9. "Who taught it?"**
Nobody sat down and taught it. People collected examples with the answers attached, and a program
adjusted itself until it got most of them right. The people chose the examples — which is exactly why
what is missing from the examples matters so much.

**10. "Does it remember me?"**
Depends entirely on the system, and you are allowed to demand a straight answer. Teachable Machine
in your browser: no, it keeps nothing. A chatbot with an account: often yes, and it may use your
conversations. Read what it says, and assume anything you type could be seen by a person.

**11. "Can it feel sad?"**
No. It can produce the words a sad person would write, because it learned from text written by
people who felt things. That is imitation of the output, not the feeling. There is nobody in there
to be sad.

**12. "Why is it wrong sometimes?"**
Almost always because of the examples. Not enough of them, or all too similar, or missing the
situation you're in now. When a model is wrong, the first place to look is the photos — not the
program.

**13. "Is my photo going to Google?"**
In Teachable Machine, no — training happens inside your browser on this laptop, and photos are not
uploaded unless you deliberately click "upload my model". Other tools are different, and it is a
completely fair question to ask about every single one.

**14. "Why does it give a different answer each time?"**
Because it picks its next word randomly, weighted by what usually comes next, instead of always
choosing the most likely one. You will build exactly that with a die in Week 29.

**15. "Can AI make art / is it stealing?"**
It makes new combinations from patterns in millions of existing images, most of which were made by
people who were not asked and are not paid. Whether that is theft is genuinely argued about right
now, by artists and lawyers, and it is not settled. You are allowed to have an opinion and you should
be able to say why.

**16. "Is it always right if it says 99%?"**
No, and this is one of the most useful things in the whole course. That number is how strongly it
prefers that answer, not how likely it is to be correct. Models are most confidently wrong on things
unlike anything they trained on.

**17. "Do robots have AI?"**
Some do, some don't. A factory arm repeating the same weld follows rules and is not AI. A robot
vacuum working out a room's shape is doing a bit of AI. "Robot" is about a body; "AI" is about a
kind of decision. They are separate questions.

**18. "Could I make one?"**
You will make one, in Week 17, and you will measure how good it actually is in Week 22. That second
part is the bit most adults never do.

**19. "Is AI in my phone right now?"**
Yes, in a dozen places you don't notice: face unlock, autocorrect, the photo app sorting pictures of
your dog, noise reduction on calls, which notifications get shown first. Week 3 has you find fifteen
of them.

**20. "What can't AI do?"**
Anything it has no examples of. Anything needing to actually understand what happens to a real
person. Anything needing to say "I don't know" honestly — most systems will produce a confident
answer rather than admit they are stuck, which is why your job is to check.

---

# ⚠️ Section 3 — The 15 Things Teachers Most Often Get Wrong

Not criticism. These are the standard misconceptions in the general adult population, and you may
hold several. Correcting them before you teach is worth an hour of anything else.

**1. Wrong: "AI = robots."**
Right: AI is a kind of decision-making, not a kind of body. Almost all AI has no body. The robot arm
on a car production line is usually pure if-then rules.

**2. Wrong: "AI = ChatGPT."**
Right: chatbots are one loud recent branch. Spam filters, recommendation feeds, face unlock, fraud
detection, and photo sorting are all AI, all older, and all more widely used.

**3. Wrong: "The computer programmed itself / nobody understands it at all."**
Right: humans chose the examples, the labels, the architecture and the success measure. What we
cannot read is the specific pattern it settled on. Everything else was a human decision, and every
human decision is a place responsibility lives.

**4. Wrong: "It searches the internet for the answer."**
Right: a trained model does not look anything up. It applies a fixed pile of numbers to your input.
(Some products bolt a search step on top, and when they do, they usually tell you — that is a
different feature, not how the model works.)

**5. Wrong: "More data always makes it better."**
Right: more *varied* data makes it better. Four hundred near-identical photos taken in one sitting
are worth less than forty taken across different backgrounds and lighting. Week 18 measures this.

**6. Wrong: "95% accurate means it's good."**
Right: 95% is meaningless without two other numbers — out of how many, and what is the baseline?
95% on a task where always guessing "no" gets 94% is a model that has learned nothing.

**7. Wrong: "Confidence score = probability of being correct."**
Right: it is how strongly the model prefers that class. Models are routinely 99% confident and
wrong. This one is worth being genuinely fussy about, all year.

**8. Wrong: "Bias means someone was prejudiced."**
Right: in this course bias is a measured accuracy gap between groups, and its usual cause is a
counting gap in the training data. No villain required. Which is exactly why counting is the fix.

**9. Wrong: "You test it by trying it out a few times."**
Right: you hold out examples *before* training, you score every one of them on paper, and you write
the fraction down. "I tried it and it worked" is the thing this course exists to eliminate.

**10. Wrong: "Neural networks work like the human brain."**
Right: they were loosely inspired by a 1940s guess about brain cells and are now nothing like one.
We do not understand brains well enough for the comparison to mean anything.

**11. Wrong: "It understands what it's saying."**
Right: it produces text that patterns like understanding. Whether that ever amounts to
understanding is a genuine open argument among serious people — but for anything you will do this
year, assume not, and check the facts.

**12. Wrong: "AI is new."**
Right: the term dates from 1956. Machine learning has been in commercial use since the 1990s — your
bank has been using it on fraud for decades. What changed recently is scale and public visibility.

**13. Wrong: "It can't be creative / it's just copying."**
Right: it is genuinely producing combinations that did not previously exist, and calling that
"copying" is too easy. It is also true that it can only recombine what it was shown, and that the
people who made the training material mostly were not asked. Both halves are true; teach both.

**14. Wrong: "If it's wrong, the program is broken."**
Right: a model being wrong is normal operation, not a fault. Every model has an accuracy below 100%.
The engineering question is never "is it wrong?" but "how often, on what, and does that matter here?"

**15. Wrong: "I need to understand the maths to teach this."**
Right: you need to understand counting, division, and percentages. Everything in Level 1 is built
from those three. The maths under the hood is Level 3, and skipping it now costs the student
absolutely nothing.

---

# 🕐 Section 4 — How to Run a Lesson

Every week uses the same five-part shape. Same order, same timings, thirty-six times. The
predictability is deliberate — it means neither of you spends any energy wondering what happens next.

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │  THE STANDARD 70-MINUTE LESSON                                             │
   ├──────┬─────────────────────────────────────────────────────────────────────┤
   │      │                                                                     │
   │ 0:00 │  🪝  HOOK  (5 min)                                                  │
   │      │  One story, one surprising object, or one question with a wrong      │
   │      │  obvious answer. Never start with a definition. The teacher file     │
   │      │  gives you the exact hook — read it or tell it, don't improvise.     │
   │      │  Ends with the student wanting to know something.                    │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:05 │  🧠  CONCEPT  (12 min — HARD CEILING)                               │
   │      │  The new idea. Concrete example first, formal name second. Always    │
   │      │  in that order. Bold the new word, give the one-line definition,     │
   │      │  move on. Two or three new terms maximum.                            │
   │      │  ⏰ If you are still talking at 12 minutes, stop mid-sentence and    │
   │      │     go to the activity. You can finish the point afterwards, and     │
   │      │     it will land better because they'll have done it by then.        │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:17 │  🔍  WORKED EXAMPLE  (13 min)                                       │
   │      │  You do one, out loud, showing every step including the arithmetic.  │
   │      │  Then the student does the next one while you sit on your hands.     │
   │      │  ⚠️ Never do the arithmetic for them. Wait. Count to fifteen in      │
   │      │     your head. The silence is doing the work.                        │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 0:30 │  🎲  ACTIVITY  (30 min)  ← the heart of the lesson                  │
   │      │  Hands on cards, on the keyboard, on graph paper. This is where      │
   │      │  the learning actually happens. Protect this block at all costs.     │
   │      │  If the lesson is running late, cut anything else — never this.      │
   │      │                                                                     │
   ├──────┼─────────────────────────────────────────────────────────────────────┤
   │ 1:00 │  🔑  LAND IT  (10 min)                                              │
   │      │  Three things, in this order:                                        │
   │      │   1. "Tell me the big idea in one sentence, in your own words."      │
   │      │      (Their words, not yours. Wait for it. Don't accept the file's   │
   │      │       sentence recited back.)                                        │
   │      │   2. Write the week's vocabulary into the notebook — the term and    │
   │      │      the student's own definition.                                   │
   │      │   3. Read the homework aloud together and check they know the first  │
   │      │      step. Not the whole thing — just step one.                      │
   │      │                                                                     │
   │ 1:10 │  ✅ DONE                                                            │
   └──────┴─────────────────────────────────────────────────────────────────────┘
```

### Squeezing it into 60 minutes

Cut in exactly this order and no other:

1. The second worked example (student does it in the workbook instead) — saves 6 min
2. The vocabulary write-up (moves to homework) — saves 4 min
3. The last third of the activity (finish it next week as a warm-up) — saves up to 10 min

**Never cut the hook** (five minutes buys you sixty-five minutes of attention) and **never cut the
one-sentence summary** (it is your only real evidence anything landed).

### Stretching to 75+ minutes

Add the ✍️ practice questions in class instead of setting them as homework, or run the
*"level it up"* extension in the teacher file.

### Six rules of thumb that work every week

1. **Concrete first, name second.** Always. "You know how your phone suggests the next word? That's
   called next-word prediction." Never the other way round.
2. **Never say a term without defining it in the same breath.** One line, plain, first time.
3. **Ask before you tell.** "What do you think will happen?" costs eight seconds and doubles what
   they remember when they find out.
4. **Let the wrong answer live for a minute.** Don't correct instantly. "Interesting — how could we
   check?" is almost always the better next sentence.
5. **Make it fail on purpose.** Every lab has a break-it step. Watching your own model fail is the
   fastest route to understanding it, and students love it.
6. **End with them talking, not you.** If your voice is the last one in the room, you don't know what
   they learned.

---

# 🤷 Section 5 — How to Say "I Don't Know" Well

You will not know some things. Good. Here is how to make that an asset.

### The four-part move

```
   1. SAY IT PLAINLY        "I don't know."
                            Not "well, sort of…", not a bluff, not a topic change.
                            Kids detect bluffing instantly and it costs you more
                            than the gap in knowledge ever would.

   2. SAY WHAT KIND         "Is that a fact we could look up, or is it something
      OF QUESTION IT IS      nobody knows yet?"  This is genuinely one of the most
                             valuable distinctions you can teach. "Do LLMs
                             understand?" is nobody-knows. "How many photos does
                             Teachable Machine need?" is lookup-able.

   3. WRITE IT DOWN         Keep a "Questions We Owe Answers To" page in the front
                             of the notebook. Nothing says a question mattered like
                             writing it down in front of the person who asked it.

   4. COME BACK TO IT       Open the next lesson with it. Every time. This is the
                             single most trust-building thing you can do all year.
```

### Looking things up safely — a method you can teach

| Step | Do | Don't |
|---|---|---|
| 1 | Say what you're trying to find out, in one sentence, before searching | Type a vague phrase and skim |
| 2 | Prefer the source closest to the thing (Teachable Machine's own FAQ for Teachable Machine questions) | Take a random blog's word for it |
| 3 | Get a second, independent source | Count three sites quoting the same one source as three sources |
| 4 | Notice the date. AI facts from 2019 are frequently wrong now | Assume a page is current |
| 5 | If you use a chatbot, treat it as a lead, not an answer. Ask it, then verify | Paste its answer into the lesson |

> **⚠️ Watch out:** Asking a chatbot "is this true?" is close to useless — it will usually agree with
> whatever you suggested. Ask it *"what's the evidence for and against this?"* and then go and check
> the evidence yourself. Model this out loud for your student at least once. It is a Week 32 skill
> that you get to demonstrate in Week 4.

### Three things it is fine to simply say

- **"Nobody knows that yet."** True of consciousness, of understanding, of most of what's inside a
  large model.
- **"That's an argument, not a fact."** True of whether AI art is theft, whether AGI is close,
  whether schools should use face recognition. Say which side you're on and why, and say that
  reasonable people disagree.
- **"That's above this course, and here's the one-line version."** Backpropagation, transformers,
  gradient descent. One honest sentence, then move on. There is a Level 3 and it has their name on
  it.

---

# 👥 Section 6 — Classroom Management

### With one learner (the default this course is written for)

**The advantage:** you can go at exactly the right speed, and nobody can hide.
**The risk:** no peer to argue with, and it is very easy for you to do the thinking out loud and for
them to nod along.

Five habits that fix the risk:

1. **You be the wrong one.** Deliberately propose a bad rule, a leaky feature, a dishonest test.
   Make them catch you. Aim for one planted error per lesson; the teacher files suggest good ones.
2. **The 15-second silence.** After you ask something, count to fifteen. It will feel like a
   minute. Do not rescue them. Most of the time the answer arrives at second eleven.
3. **Recruit a second human.** Weeks 14, 30, 33, 35 and 36 are much better with an audience.
   A sibling, a grandparent, a neighbour, a video call. Book them a week ahead.
4. **Swap chairs for the explanation.** Once a lesson, they teach the last five minutes back to you.
   Physically move seats. It changes what their brain does.
5. **Keep a visible artefact wall.** Pin up the Spotter's Log, the data card, the confusion matrix,
   the audit poster. Over 36 weeks a solo learner needs to see the pile growing.

### With 2–6 learners

- **Pair the activity, individual the workbook.** Everyone builds their own model; discussion is
  shared.
- **Swap and test.** From Week 14 onwards, the best activity is always testing someone else's work:
  their card deck, their rulebook, their model, their bias claims. Independent testing is a real
  professional skill and it is more fun than doing your own.
- **Give the quiet one a job with a name.** Scorekeeper, timekeeper, official sceptic. The official
  sceptic role — whose job is to say "how do you know?" — is worth rotating every week.
- **Add 10 minutes to every activity.** Everything takes longer with more people. Cut the practice
  block, not the activity.

### With 7+ learners

Run it as pairs and treat the pair as the unit. Double all the activity timings, and split labs
across two weeks rather than rushing them. Weeks 17, 22, 26, 30 and 33 will each need two sessions.
That turns 36 weeks into roughly 41 — plan for it up front rather than discovering it in April.

### When motivation dips (it will, around weeks 12 and 24)

| Symptom | Almost always caused by | Do this |
|---|---|---|
| "This is boring" | Too much talking, not enough hands | Cut the concept block to 6 minutes. Start the activity. |
| "I don't get it" | A gap two or three weeks back, not today | Ask them to explain last week's big idea. Find the actual gap. Fix that. |
| "Why do I have to write it down?" | Fair question, badly answered | "Because in Week 22 you'll need this number and you won't remember it." Then be right. |
| Refusing the arithmetic | It feels like maths homework | Do the division on the calculator, but they write the fraction. The fraction is the honest bit. |
| Wants to skip to the chatbot | Genuine curiosity | Let them. Go and play with a chatbot for ten minutes and come back with three questions. Curiosity is not the enemy. |

---

# ✏️ Section 7 — Marking the Workbook

### How strict to be

Strict about **exactly three things**. Relaxed about everything else.

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  BE STRICT ABOUT                                                    │
   │                                                                     │
   │   1. THE ARITHMETIC IS SHOWN.                                       │
   │      Not just "73.3%". You want to see  11 ÷ 15 = 0.733 = 73.3%.    │
   │      An answer without the division is not an answer.               │
   │                                                                     │
   │   2. THE FRACTION IS THERE.                                         │
   │      "80%" without "4 out of 5" hides how small the test was.       │
   │      This is a professional habit and it starts now.                │
   │                                                                     │
   │   3. NO "MAGIC" WORDS.                                              │
   │      Banned all year: magic · it just knows · the AI figured it out │
   │      it's smart · it thinks · it understands · obviously            │
   │      Circle it. Ask for the sentence again. Every single time.      │
   └─────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────┐
   │  BE RELAXED ABOUT                                                   │
   │   · Spelling and handwriting (unless you literally cannot read it)  │
   │   · Using their own words instead of the book's — actively prefer   │
   │     their words                                                     │
   │   · A wrong answer with good reasoning — that's most of the marks   │
   │   · Neatness of drawings, as long as they're labelled               │
   │   · Getting there by an unexpected route                            │
   └─────────────────────────────────────────────────────────────────────┘
```

### The four-tick scheme

Use this on every workbook exercise. It takes ten minutes a week.

| Mark | Means | Say |
|:--:|---|---|
| ✓✓ | Right, and the reasoning is visible | "This is the reasoning I wanted — say it back to me in one sentence." |
| ✓ | Right answer, reasoning missing or thin | "Correct. Now show me how you got there." Do not give full credit for a bare answer. |
| ~ | Wrong answer, good reasoning | **This is worth more than a bare ✓.** "Your thinking is right, one step slipped — find it." |
| ✗ | Wrong, and the reasoning shows a misconception | Do not correct in writing. Find the misconception and reteach it in three minutes at the start of next class. |

### Giving feedback

- **Ask, don't tell.** "How did you get 40%?" surfaces the misconception. "That should be 60%" hides
  it.
- **Two ticks, one question.** Per page: name two things that are genuinely good, ask one question
  that makes them go back. More than one question and they stop reading.
- **Praise the process, not the child.** "You wrote down the fraction as well as the percentage —
  that's the thing" beats "you're so clever". This matters more than it sounds; praising the habit
  makes the habit repeat.
- **Praise the honest failure loudest of all.** A student who writes *"my model got 6/15 and I think
  it's because all my photos were on the same table"* has done better work than one who got 14/15
  and cannot say why. Say so, out loud, in those words.

### Marking the term checkpoints (weeks 9, 18, 27)

Mark these together, out loud, right after the quiz — not later, alone, in red pen. For each wrong
answer ask: *"which week does this belong to?"* Then put the week number in the margin. At the end
you have a list of weeks to revisit, which is the entire point of a checkpoint.

There is no grade. Do not give a grade. The output of a checkpoint is a list of weeks, not a number.

### Marking the capstone (weeks 34–36)

Use the eight-row rubric in [`../../capstone.md`](../../capstone.md). Score each row 1–4 with the
student sitting next to you, and make them argue for their own score on at least two rows. Then:
27–32 exceptional, 21–26 proficient, 15–20 developing, 9–14 beginning.

The row that matters most is row 6, *Honesty & limits*. A booth with a modest model and a brutally
honest warning sign is a better piece of work than a flashy one that over-claims. Grade accordingly
and say why.

---

# 🔒 Section 8 — Safety and Privacy Rules

Non-negotiable. Read this section twice. It concerns a real child using real internet tools.

### The five rules

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │  1.  NO REAL NAME ANYWHERE ONLINE                                      │
   │      Scratch username, project titles, sprite names, model names.      │
   │      Pick something in Week 0. Week 32 explains why; do it first.      │
   │                                                                        │
   │  2.  NO FACES IN THE TRAINING DATA, unless it is the learner's own     │
   │      face AND the model never leaves the laptop.                       │
   │      Objects work just as well and raise none of the questions.        │
   │      Never photograph another child, ever, for any activity here.      │
   │                                                                        │
   │  3.  NO BACKGROUNDS THAT IDENTIFY A PLACE                              │
   │      School badges, house numbers, name labels, street signs, the      │
   │      view out of a recognisable window. Check before you photograph,   │
   │      not after.                                                        │
   │                                                                        │
   │  4.  DEFAULT TO NOT UPLOADING                                          │
   │      Teachable Machine can save to your computer as a .tm file         │
   │      instead of publishing to a cloud link. Do that. The capstone      │
   │      documents a full "Route B" that never uploads anything.           │
   │                                                                        │
   │  5.  AN ADULT IS PRESENT FOR EVERY CHATBOT SESSION                     │
   │      Weeks 1, 29 and 32 involve a generative AI. The adult drives      │
   │      the keyboard or sits beside it. Never a solo session, never as    │
   │      homework.                                                         │
   └────────────────────────────────────────────────────────────────────────┘
```

### Which tools do what — check this yourself before Week 1

| Tool | Where does the data go? | Account? | Verdict |
|---|---|---|---|
| **Teachable Machine** | Training runs **inside the browser tab** on your laptop. Photos are not uploaded unless you click "upload my model". | Only for Drive saving | ✅ Safest. Download the `.tm` file locally and nothing leaves the machine. |
| **Quick, Draw!** | Drawings **are** sent to Google and added to a public open dataset. | No | ⚠️ Fine — draw shapes, not names or faces. Tell the student their drawing is being donated; it's a Week 32 lesson in advance. |
| **Scratch** | Saved projects live on Scratch's servers and can be public. | Yes | ⚠️ Non-identifying username. Keep projects unshared. Also File → Save to your computer as a backup. |
| **Google Sheets** | Google's servers, on your account. | Yes | ✅ Fine for a table of sleep hours. Not for anything about other people. |
| **A chatbot (ChatGPT/Claude/Gemini)** | Servers; conversations may be stored and may be used for training depending on account settings. | Usually | ⚠️ Adult present. Never type a real name, school, address, or anything about another person. |

### The consent rule for other people's data

Weeks 2, 6 and the capstone can involve data about family members. Before recording anything about
another person, the student asks — out loud, in words — and writes the answer in the data card:
*"12 photos from my brother, with permission, 4 March."*

This is not bureaucracy. Attribution and consent are Week 32 content, and doing it a term early
means it is a habit by the time it is a lesson.

### If something goes wrong

| Situation | Do |
|---|---|
| A chatbot says something upsetting or inappropriate | Close the tab immediately. Talk about it plainly — it produced text from patterns, it was not aimed at them. Report it in the tool if there's a button. |
| A real name or face got uploaded | Delete the project/model at the source. Scratch: unshare then delete. Teachable Machine: delete the Drive file and the shareable link. |
| The student wants to share their model publicly | Only with an adult reviewing exactly what is in it, and only with the "DO NOT USE THIS FOR…" sign attached. Week 33 writes that sign. |
| A stranger contacts them on Scratch | Do not reply. Report and block. Scratch has good moderation; use it. |

---

# ✅ Section 9 — Pre-Flight Checklist

Run this every week. It takes four minutes and prevents about 90% of lessons that go wrong.

```
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  ⏱️  BEFORE EVERY CLASS — 4 MINUTES                                     │
   ├─────────────────────────────────────────────────────────────────────────┤
   │                                                                         │
   │  20 MINUTES BEFORE                                                      │
   │   □  Read this week's teacher-guide file, all of it                     │
   │   □  Read the "What you need to understand first" section twice         │
   │   □  Do the worked example yourself, on paper, with the arithmetic      │
   │      (if you can't do it cold, the student definitely can't)            │
   │   □  Say the week's big idea out loud in one sentence, in your words    │
   │                                                                         │
   │  5 MINUTES BEFORE                                                       │
   │   □  Materials for THIS week are on the table (check the week's list)   │
   │   □  Laptop charged; browser open; other camera apps quit               │
   │   □  On lab weeks: run the smoke test — webcam shows a picture          │
   │   □  Last week's homework is here, and you have looked at it            │
   │   □  One thing from last week you'll open with (a good answer, a        │
   │      mistake worth revisiting, or a question you owed them)             │
   │   □  Phone on silent and face down. Yours, too.                         │
   │                                                                         │
   │  AS YOU START                                                           │
   │   □  Notebook and pencil out                                            │
   │   □  Water within reach                                                 │
   │   □  60–75 minutes genuinely protected — no doorbell, no "quick call"   │
   │                                                                         │
   ├─────────────────────────────────────────────────────────────────────────┤
   │  THE TWO QUESTIONS TO ASK YOURSELF FIRST                                │
   │                                                                         │
   │   1. "What is the ONE sentence I want them saying at 1:10?"             │
   │   2. "What are they going to DO with their hands today?"                │
   │                                                                         │
   │  If you can answer both, the lesson will be fine.                       │
   │  If you can't answer either, re-read the teacher file.                  │
   └─────────────────────────────────────────────────────────────────────────┘
```

### The end-of-class 60-second review (for you, not them)

Write one line in the back of your own notebook:

```
   Week ___  ·  Landed: ____________________  ·  Didn't: ____________________
             ·  Owed them an answer to: _______________________________
```

Thirty-six of those lines is a genuinely useful record, and the "owed them" column is how you build
a student who trusts that questions get answered.

---

# 🧾 Last Thing

You are going to spend a school year teaching a child that the right response to a confident claim
is *"out of how many?"*

That is a better education in thinking than most people get at university, and it happens to be
delivered through a subject that will shape their entire adult life. You do not need to be an expert
to hand that over. You need to be honest, to protect the activity block, and to refuse the word
"magic" thirty-six weeks running.

Everything else is in the files.

> ### 👉 Next: **[Week 1 — Is It Smart, or Is It Just Following Orders?](../student-guide/week-01.md)**

---

[⬅ Course home](../README.md) · [Week 1 student guide](../student-guide/week-01.md) · [Week 1 workbook](../workbook/week-01.md) · [Level 1 glossary](../../glossary.md) · [Capstone](../../capstone.md) · [Assessment pack](../../assessment.md) · [Figure style guide](../figures/STYLE.md)
