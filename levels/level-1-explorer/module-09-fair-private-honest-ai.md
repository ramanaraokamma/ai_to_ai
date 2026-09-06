# Module 9 — Fair, Private, and Honest: The Human Side of AI

**Level 1 · Module 9 · ~3 hours · Prereqs: Module 2 (data cards, provenance, sample vs population), Module 5 (your trained model), Module 6 (test sets, accuracy, per-class scores), Module 7 (pixels and backgrounds), Module 8 (fluency vs truth)**

[⬅ Previous](module-08-how-computers-read-and-chat.md) · [Level 1 Home](README.md) · [Next ➡](capstone.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** trace a biased prediction backwards to a specific, countable gap in the training data — and show the two numbers side by side.
2. **You will be able to** identify the personal data in any dataset and say concretely what could go wrong if it leaked, to whom.
3. **You will be able to** run a fairness test on your own model, compute an accuracy gap in percentage points, and report the bad result honestly.
4. **You will be able to** state three situations where you should not trust an AI's answer, and say exactly what to do instead in each.
5. **You will be able to** decide whether a piece of media you have been sent is likely generated, using a repeatable checking procedure rather than a gut feeling.

---

## 🪝 The Hook

In 2017 a researcher named Joy Buolamwini was building an art project that needed a computer to notice a human face. The software worked fine for her lab-mates. It would not see her at all — until she held a white plastic mask in front of her own face. Then, instantly, it found a face.

She did not shrug and move on. She built a test set: 1,270 faces of parliamentarians from three African and three European countries, sorted by skin tone and by gender. Then she measured three commercial face-analysis products that were already being sold to real customers.

The best of them got lighter-skinned men wrong about **0.8%** of the time. The same product got darker-skinned women wrong **34.7%** of the time. One error in 125, versus one error in three. Every one of those products had been tested before shipping. Every one had a headline accuracy number that looked good. The gap was invisible because nobody had split the score by group.

Here is the part that should stay with you. **Nothing was broken.** No bug, no crash, no sabotage. Somebody assembled a set of training faces, that set contained far more of some people than others, the model learned what it was shown, and the testing was done the same way — as one average. That is all it takes.

Your Module 5 model has the same problem right now. You just haven't measured it yet. Today you will.

---

## 🧠 The Concept

Five ideas. Each with an anchor, and each with numbers, because "be fair" is a slogan and a measured gap is a fact.

---

### 1️⃣ Bias comes from who is missing in the training data

> **Bias**, in machine learning — when a model works noticeably worse for some group of inputs than for others, in a way that matters.

This is not the everyday meaning of "biased" (holding an unfair opinion). A model has no opinions. It has counts. It gets good at whatever it saw a lot of, and stays bad at whatever it barely saw. That is not a character flaw, it is the definition of learning from examples — which means **bias is the default outcome, not an unlucky one.** You have to work to avoid it.

🍕 **Analogy — studying for the wrong exam.** You spend three weeks on fractions and skip decimals entirely. On exam day you score 95% on the fractions questions and 30% on the decimals questions, for an average of 78%. Nobody would say you are "biased against decimals". You simply studied one and not the other. Now imagine the exam is 90% fractions: you score 88% overall, look brilliant, and nobody discovers the hole — until the day a decimals question actually matters.

**The chain is always the same, and it always has four links:**

```
   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
   │  WHO/WHAT    │    │  TRAINING    │    │   MODEL      │    │  WHO GETS    │
   │  GOT         │───►│  DATA        │───►│  LEARNS      │───►│  BAD         │
   │  COLLECTED   │    │  IS SKEWED   │    │  THE SKEW    │    │  PREDICTIONS │
   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
    photos taken        520 daylight        excellent in        anyone using
    by one person       8 lamp-light        daylight, poor      it at night
    in one kitchen      0 in the dark       at night
    in the afternoon

   The fix is almost never at the model. It is almost always at link 1.
```

**Tiny concrete example with real numbers.** Suppose a voice assistant was trained on 10,000 recordings:

| Speaker group | Training recordings | Share | Word error rate when tested |
|---|---:|---:|---:|
| Adults, standard accent | 8,500 | 85% | 5% |
| Adults, regional accent | 1,200 | 12% | 14% |
| Children under 12 | 300 | 3% | 31% |

The headline number, if the test set matched the training mix:

```
   (0.85 × 0.95) + (0.12 × 0.86) + (0.03 × 0.69)
   =  0.8075   +   0.1032   +   0.0207
   =  0.9314   →  93.1% of words correct
```

**93% sounds excellent.** And a child using it gets nearly a third of their words wrong — every third word, all day, in a product advertised as working for everyone. The average did not lie. It just answered a question nobody should have asked on its own.

> **The rule: a single accuracy number is a summary, and every summary hides something. Always ask "for whom?"**

**Where the gaps come from.** In practice, almost always one of these five:

| Source of the gap | What it looks like |
|---|---|
| Convenience sampling | You photographed what was nearby — your kitchen, your hands, your accent |
| Historical data | You trained on past decisions that were themselves unfair, so the model copies them |
| One collector | One person, one phone, one time of day, one height, one handedness |
| A group that is genuinely rarer | Fewer examples exist, so fewer get collected, so the model stays bad, so they use it less, so even fewer get collected |
| Unmeasured groups | You cannot find a gap in a group you never wrote a column for |

That last one is the sneakiest. **You can only measure a gap you thought to look for.** Which is why the first step of a fairness audit is always: *list the groups*, before you look at any results.

---

### 2️⃣ Privacy: what is yours, and what a model remembers

> **Personal data** — any information that is about an identifiable person, or that could be combined with other information to identify them.

That definition is wider than most people expect. It is not only your name.

| Clearly personal | Personal in combination | Usually not personal |
|---|---|---|
| Full name, photo of your face | Postcode + birthday + school year | The temperature yesterday |
| Home address, phone number | "The only left-handed goalkeeper in Year 7" | The rules of cricket |
| Voice recording, fingerprint | Your exact walking route to school | A photo of an empty street |
| School ID number | Timestamps of when you're online | The plot of a novel |

**The combination column is the dangerous one.** No single item there identifies you. Put three together and there is exactly one person in the country they could refer to. This is called **re-identification**, and it is the reason "we removed the names, so it's anonymous" is one of the most common false statements in technology.

🍕 **Analogy — the group photo.** You post a photo of yourself in your garden. You are thinking about your face. The photo also contains: your house number on the gate, your school uniform, your neighbour's car number plate, a reflection in the window, and — invisibly attached to the file — the exact GPS coordinates and the time it was taken. You shared one thing. You gave away nine.

> **Metadata** — the hidden information a file carries about itself: when it was made, on what device, and often exactly where.

**Now the AI-specific part: what does a model remember?**

Two honest answers, depending on the kind of model.

*Your Teachable Machine classifier* does not store your photos. It stores a set of numbers learned from them. You cannot open the model and get your photo back out. That is genuinely reassuring — but not total: models can leak whether a specific example was in the training set, and a model trained on 30 photos of your bedroom has learned quite a lot about your bedroom.

*A language model* is different, and more alarming. Because it was trained to reproduce likely text, if some text appeared many times in its training data it can reproduce it **word for word**. Researchers have shown that models can be prompted into emitting exact passages from their training data, including things like phone numbers and addresses that happened to appear on a webpage. Nobody programmed that in. It is a side effect of "learn to continue text really well".

> **The rule: data you put into a system is data you may not be able to take back out.** Once it is in a training set, "please delete it" is a much harder request than it sounds — the training run has already happened, and the information is spread across millions of numbers.

**Four questions worth asking before you hand over anything:**

1. Who can see this — the company, its staff, its partners, a future buyer of the company?
2. How long is it kept? "Forever" is the default unless someone says otherwise.
3. Is it used to train a model? If so, it may resurface in an answer given to a stranger.
4. What happens to it if this company is sold, hacked, or shuts down?

**And a rule for your own projects, starting today:** if a photo has another person's face in it, you ask them before you train on it. Not because a law says so at your age, but because it is their face. This is the smallest possible version of the biggest ethical rule in the field, and practising it on 20 photos is how you get good at it before it is 20 million.

---

### 3️⃣ Deepfakes and misinformation: generated content that looks real

Module 8 showed you a text generator. The same idea builds image, voice, and video generators — and they got good, quickly.

> **Deepfake** — a photo, video, or voice recording of a real person doing or saying something they never did, made by an AI.
> **Misinformation** — false information spreading, whether or not anyone meant to deceive. **Disinformation** — false information spread deliberately.

**Why this is different from old-fashioned faking.** Fakes have existed as long as photographs. Three things changed:

| Before | Now |
|---|---|
| Took an expert days | Takes anyone minutes |
| Cost money | Costs nothing |
| One at a time | Thousands, automatically, each slightly different |
| Voice was hard to fake | A few seconds of audio is enough |

🍕 **Analogy — the counterfeit note.** One good forger with a printing press was a police problem. A machine on every phone that prints perfect notes in seconds is not a police problem — it is a problem with the whole idea of trusting notes. That is what has happened to photographs and recordings as *evidence*.

**The second, sneakier harm.** Once everyone knows convincing fakes exist, a person caught on genuine video can simply say *"that's a deepfake"* — and a lot of people will believe them. So the technology damages truth twice: it makes false things believable, **and** it makes true things deniable. Notice that the second harm hurts you even if you never see a single deepfake.

**A checking procedure you can actually run.** Do not rely on spotting weird hands or blurry teeth — generators fix those flaws every few months, and "I can tell" is exactly how people get fooled. Check the *provenance*, not the pixels:

```
   THE FOUR-STEP CHECK

   1. SOURCE      Who posted this first? Not who sent it to you —
                  who posted it FIRST. Scroll back to the original.
                  An account made last week is a red flag.

   2. CORROBORATE Is anyone else reporting it? A real event with a real
                  video has multiple independent witnesses. One video and
                  silence everywhere else is the shape of a fake.

   3. REVERSE     Reverse image search a frame. Old photos from other
                  events get relabelled constantly — that is the most
                  common fake of all, and it needs no AI at all.

   4. MOTIVE      Who benefits if you believe this and pass it on?
                  Then ask the harder one: does it happen to confirm
                  something I already wanted to be true?
```

Step 4 is the one people skip and the one that matters most. **The content most likely to get past your defences is the content you were hoping was true.** A fake that annoys you gets checked. A fake that delights you gets forwarded.

---

### 4️⃣ Attribution: someone made the data

Every dataset is made of somebody's work, somebody's writing, somebody's face, or somebody's life.

> **Attribution** — saying where something came from and who made it.

Your Module 2 data card already had "where did this come from". Now add the harder question: **were they asked, and would they have said yes?**

**The three cases you will actually meet:**

| Case | Example | What you owe |
|---|---|---|
| **You made it** | Your own 60 photos of your own comb | Nothing to anyone else. Still write the data card |
| **Someone gave permission** | 20 photos your friend agreed to let you use | Name them, use it only for what you agreed, delete it when asked |
| **You just took it** | 300 images downloaded off a search engine | This is the hard case, and "it was on the internet" is not an answer |

**Why the third case is genuinely hard.** A human artist who studies 500 paintings and develops a style owes nobody a payment — that is how art has always worked. An AI system trained on 500 paintings can produce work "in the style of" that artist, thousands of times an hour, competing directly with them, without ever naming them. Is that the same activity at a bigger scale, or a different activity altogether?

Reasonable people disagree, lawsuits are running right now, and you are not required to have the final answer at eleven. You **are** required to notice that there is a question. The trap is not getting it wrong. The trap is not seeing that anyone is there.

**Three habits that cost you nothing and put you ahead of most adults:**

1. **Label generated work.** If an AI wrote it, drew it, or helped substantially, say so. Every time. This is about honesty with your reader, not about the AI's feelings.
2. **Name your sources in the data card.** "20 photos from my brother, with permission, 4 March" takes ten seconds and makes your project auditable.
3. **Ask before you use someone's face, voice, or writing.** Even when nobody would find out.

---

### 5️⃣ Over-trust: when the confident answer is the dangerous one

> **Automation bias** — the human habit of trusting a machine's answer more than our own judgement, especially when we are tired, rushed, or unsure.

This is a fact about *people*, not about machines, and it is the reason a mediocre AI can cause more harm than a terrible one. A terrible AI gets ignored. A usually-right AI gets trusted on the day it is wrong.

🍕 **Analogy — the satnav and the lake.** There is a whole genre of news story where a driver follows their satnav down a boat ramp and into a river. The driver could see the water. They had eyes, headlights, and a lifetime of knowing that roads do not usually go underwater. The screen was so confident, and had been right so many times, that it beat the evidence in the windscreen. That is automation bias in its purest form.

**Why confidence is not accuracy.** You already met this in Module 5: your classifier says **97%** while looking at a fork it has never seen, because 97% means "of my three classes, this one fits best" — not "I am 97% likely to be right". Module 8 sharpened it: a text generator produces true and invented sentences in the same smooth voice, because there is no wobble channel. **A confident wrong answer and a confident right answer are produced by the same machinery and look identical.**

**Three situations where you should not trust an AI's answer — memorise these:**

| # | Situation | Why | What to do instead |
|---|---|---|---|
| **1** | **High stakes and hard to undo** — health, money, safety, legal, anything about a real person's reputation | Being wrong once is not recoverable, and you may not find out you were wrong until it is too late | Treat the AI answer as a *question to research*, never as an answer. Confirm with a qualified human or an authoritative source before acting |
| **2** | **A specific checkable fact** — a name, date, number, quote, price, page reference, URL, medical dose | This is exactly where generation invents most freely, because specific facts are rare in the training text and the *shape* is easy to fake | Verify against two independent sources that don't copy each other. Never ask the same AI "are you sure?" — it will confirm itself |
| **3** | **The input is unusual, or about you specifically** — something rare, local, recent, or outside what the model saw | Models are worst exactly where they have the fewest examples, and they give no warning when they leave familiar ground | Ask "would there have been much data about this?" If your situation is rare, downgrade your trust hard and find a person who knows |

A fourth one worth adding, though it is about you rather than the model: **when you are in a hurry and the answer is what you were hoping for.** That combination defeats more people than any technical flaw.

**What good use looks like.** None of this means don't use AI. It means: use it where a wrong answer is cheap and checkable. Brainstorming, first drafts, explaining a concept you will then verify, rewriting your own words more clearly, generating practice questions, summarising something you can also read yourself. Push the AI toward *drafting* and keep *deciding* for yourself. **You are always the last checkpoint, and the last checkpoint is not allowed to be asleep.**

---

## 🔍 Worked Example

**Goal:** run a complete fairness audit on the classifier from Modules 5 and 6, trace every gap back to the training data, and write the honest report. Every number shown.

### Step 1 — The model and its training data, counted honestly

The model: a three-class Teachable Machine classifier — **comb**, **spoon**, **toothbrush** — trained on 60 photos, 20 per class.

Before testing anything, we count the training set along every dimension we can think of. This is the step almost everyone skips, and it is where the answer already is.

| Dimension | Breakdown of the 60 training photos |
|---|---|
| Lighting | daylight from a window **52** · kitchen lamp **8** · dark or torch **0** |
| Background | white counter **55** · wooden table **5** · anything patterned **0** |
| Object position | flat on a surface **60** · held in a hand **0** |
| Distance | roughly 30 cm **58** · further **2** |
| Photographer | one person, one phone, right hand, all between 3pm and 5pm |

Read that table and you can predict the results before running the test. **That is the point of the table.**

### Step 2 — List the groups BEFORE looking at results

We will test four conditions, 12 held-out photos each (4 per class), 48 photos total. Every photo is of the *same three objects* — only the surrounding conditions change.

| Batch | Condition | Why we chose it |
|---|---|---|
| **A** | Daylight, white counter | The **control** — matches training exactly |
| **B** | Kitchen lamp at night | Training had only 8 lamp photos and 0 dark ones |
| **C** | Held in a hand | Training had **zero** |
| **D** | Patterned cloth background | Training had **zero** |

Writing this table before collecting results is what makes it an audit rather than a fishing trip. It also stops you quietly dropping the batch that looks bad.

### Step 3 — Score all 48 photos

| Batch | Correct | Total | Fraction | Decimal | Percentage |
|---|---:|---:|---|---|---:|
| A — daylight, counter | 11 | 12 | 11/12 | 0.9167 | **91.7%** |
| B — lamp at night | 7 | 12 | 7/12 | 0.5833 | **58.3%** |
| C — held in hand | 5 | 12 | 5/12 | 0.4167 | **41.7%** |
| D — patterned cloth | 6 | 12 | 6/12 | 0.5000 | **50.0%** |

The arithmetic, written out:

```
   11 ÷ 12 = 0.916666...  →  ×100 = 91.66...  →  91.7%
    7 ÷ 12 = 0.583333...  →  ×100 = 58.33...  →  58.3%
    5 ÷ 12 = 0.416666...  →  ×100 = 41.66...  →  41.7%
    6 ÷ 12 = 0.500000     →  ×100 = 50.00     →  50.0%
```

### Step 4 — The overall number, and why it is nearly useless

```
   total correct = 11 + 7 + 5 + 6 = 29
   total photos  = 12 × 4 = 48

   29 ÷ 48 = 0.604166...  →  60.4%
```

**Overall accuracy: 60.4%.**

Now notice something uncomfortable: **that number is an artefact of how many photos I put in each batch.** I chose 12 each. If I had taken 30 daylight photos and 6 of each other condition, the overall would have been:

```
   daylight:  30 × 0.917 = 27.5 correct
   lamp:       6 × 0.583 =  3.5
   hand:       6 × 0.417 =  2.5
   cloth:      6 × 0.500 =  3.0
   ─────────────────────────────────
   total:     36.5 correct out of 48  →  76.0%
```

Same model. Same weaknesses. Same objects. **60.4% or 76.0%, purely by choosing how many photos of each kind to take.** If a single number can be moved 16 points by a decision the tester makes, that number is not a property of the model. Report the per-group table or report nothing.

### Step 5 — The accuracy gap

> **Accuracy gap** — best group's accuracy minus worst group's accuracy, measured in **percentage points**.

```
   best  = Batch A = 91.7%
   worst = Batch C = 41.7%

   gap = 91.7 − 41.7 = 50.0 percentage points
```

**A word about units, because it is a real distinction.** Going from 41.7% to 91.7% is a rise of **50 percentage points**. It is *also* a rise of about **120 percent** of the original value (50 ÷ 41.7 ≈ 1.20). Both are true and they are different sentences. Use "percentage points" when subtracting two percentages, and you will never be accused of exaggerating.

### Step 6 — Trace each gap back to the data

Now put the two tables next to each other. This is the whole module in one grid.

| Condition | Training photos | Test accuracy | Verdict |
|---|---:|---:|---|
| Daylight, white counter | 52 of 60 (87%) | 91.7% | Well covered → works |
| Lamp / low light | 8 of 60 (13%) | 58.3% | Barely covered → shaky |
| Held in hand | **0 of 60 (0%)** | 41.7% | Never seen → fails |
| Patterned background | **0 of 60 (0%)** | 50.0% | Never seen → fails |

The pattern is not subtle. **Accuracy tracks training coverage almost perfectly.** Nothing mysterious happened inside the model. It learned what it was shown and it did not learn what it was not shown.

Adding the Module 7 lens makes it sharper still. When a photo is held in a hand, the pixels now contain fingers — a big region of skin-toned pixels with strong edges wrapping around the object, and half the object hidden. None of those edges were ever associated with the label "comb". And on patterned cloth, the background produces hundreds of strong edges that on the plain white counter did not exist, so the object's own outline is no longer the most obvious thing in the edge map.

### Step 7 — Which class breaks first

The 12 photos per batch break down as 4 comb, 4 spoon, 4 toothbrush. Per-class results:

| | comb | spoon | toothbrush | batch total |
|---|---:|---:|---:|---:|
| A — daylight | 4/4 | 4/4 | 3/4 | 11/12 |
| B — lamp | 2/4 | 3/4 | 2/4 | 7/12 |
| C — hand | 1/4 | 3/4 | 1/4 | 5/12 |
| D — cloth | 1/4 | 3/4 | 2/4 | 6/12 |
| **class total** | **8/16 = 50.0%** | **13/16 = 81.3%** | **8/16 = 50.0%** | 29/48 |

Check the arithmetic: 8 + 13 + 8 = 29 ✓ and 16 × 3 = 48 ✓.

Something interesting fell out that we were not looking for. **Spoon holds up everywhere** (81.3%), while comb and toothbrush both collapse. Why? Because a spoon has a distinctive bright reflective bowl and a chunky silhouette, whereas a comb and a toothbrush are both thin, long, dark, plastic and roughly the same shape — so as soon as conditions get hard, the model falls back on "long thin thing" and cannot separate them.

**This is why an audit uses a grid, not a list.** The condition table alone would never have shown you this.

### Step 8 — Who is affected, in the real world

Suppose this were shipped as a real feature — a phone app that names household objects for someone with low vision.

| Group | What happens to them | Severity |
|---|---|---|
| Someone in a bright modern kitchen | Works well, they trust it | fine |
| Someone whose home is dimly lit | Wrong 4 times in 10 | bad |
| **Anyone using it while holding the object** | Wrong 6 times in 10 | **worst — and this is how a person actually uses an object-naming app** |
| Someone with patterned surfaces | Wrong half the time | bad |

Look at that third row. The condition with **zero training examples** is the condition that describes **the normal way the product would be used.** The training set was built by a person putting objects down and photographing them, because that was convenient. Nobody was being careless and nobody was being unkind. **The gap was created by convenience, and convenience is the most common cause of bias there is.**

### Step 9 — The fix, with numbers

Vague fixes ("get more data") are not fixes. Here is a countable one.

```
   Current training set: 60 photos
      held-in-hand: 0

   Target: at least 25% of training photos show the object held in a hand,
           spread evenly across the three classes.

   Let x = photos to add.
        x / (60 + x) = 0.25
              x = 0.25 × (60 + x)
              x = 15 + 0.25x
          0.75x = 15
              x = 20

   So: add 20 held-in-hand photos — 7, 7, 6 across the three classes
       (as close to even as 20 divides).
   New training set: 80 photos, 20 of them held-in-hand = 25%.
```

Do the same for the other two gaps, one after another, each time using the *new* total:

```
   LOW LIGHT.  We already have 8. Let y = low-light photos to add.
      (8 + y) / (80 + y) = 0.25
            8 + y = 20 + 0.25y
            0.75y = 12
                y = 16        →  new total 96, low light 24, 24/96 = 25% ✓

   PATTERNED BACKGROUND.  We have 0. Let z = photos to add.
            z / (96 + z) = 0.25
                        z = 24 + 0.25z
                    0.75z = 24
                        z = 32    →  new total 128, patterned 32, 32/128 = 25% ✓
```

| Gap | Photos to add | Running total |
|---|---:|---:|
| Held in hand → 25% | 20 | 80 |
| Low light → 25% | 16 | 96 |
| Patterned background → 25% | 32 | 128 |
| **Total new photos to collect** | **68** | |

Sixty-eight extra photos to close three gaps in a 60-photo model. That number is the honest price of the shortcut taken at collection time, and it is worth noticing that shooting the original 60 photos across varied conditions in the first place would have cost nothing extra at all.

Then — and this is the part people forget — **retest with the same four batches** and report both the old and new numbers side by side. A fix you did not measure is a hope, not a fix.

### Step 10 — Write the honest report

> **Model:** household object classifier — comb, spoon, toothbrush. Trained on 60 photos (20 per class) in Teachable Machine.
>
> **Overall accuracy on 48 held-out photos: 60.4%.** That number should not be quoted on its own, because it depends entirely on how many photos of each condition I chose to take.
>
> **Per-condition accuracy:** daylight on a white counter 91.7%; kitchen lamp at night 58.3%; **held in a hand 41.7%**; patterned cloth background 50.0%. **Accuracy gap: 50.0 percentage points.**
>
> **Group handled worst:** objects held in a hand. **Cause:** 0 of 60 training photos showed an object being held. The gap in the results is the same size as the gap in the data.
>
> **Secondary finding:** comb and toothbrush both score 50.0% across all conditions while spoon scores 81.3%. The two thin dark plastic objects are being confused with each other whenever conditions get difficult.
>
> **Fix:** add 20 held-in-hand photos to reach 25% coverage, 12 low-light, and 23 patterned-background, then retest with the identical four batches and publish both sets of numbers.
>
> **Do not use this model** to name objects for anyone who would rely on the answer, in any lighting other than bright daylight, on a plain surface, with the object put down. That is a laboratory, not a kitchen.

Read that last line again. **The most valuable thing an honest audit produces is a clear statement of where the model must not be used.** Anyone can report a good number. Reporting the boundary is the skill.

---

## 💻 Hands-On

Four activities, about 70 minutes.

### Activity A — The re-identification game (10 min, unplugged)

Someone publishes a "fully anonymous" dataset about your class. Names removed. Here are three rows:

```
   row 12:  age 11 · Year 7 · lives in postcode area 3 · plays cricket ·
            left-handed · absent 14 days · allergic to peanuts

   row 27:  age 12 · Year 7 · lives in postcode area 1 · plays no sport ·
            right-handed · absent 2 days · no allergies

   row 41:  age 11 · Year 7 · lives in postcode area 3 · plays cricket ·
            right-handed · absent 3 days · allergic to peanuts
```

Answer in writing:

1. There are no names. Can you work out who row 12 is? What is the smallest number of columns you need?
2. Which single column narrows it down the most? Which narrows it down least?
3. Row 12 reveals a medical fact and a poor attendance record. Name one specific person who could misuse each, and how.
4. You must publish this dataset for a genuinely useful reason (planning school lunches). Change it so it is actually anonymous. What did you delete, blur, or bucket — and what did the dataset lose in usefulness as a result?

*The point:* you will find that two or three columns are enough, and that making it truly anonymous costs you most of what made it interesting. **That trade is not a puzzle with a clean answer — it is the permanent, unresolved tension at the centre of data privacy.**

### Activity B — Audit your own model (30 min)

This is the heart of the module. Use your Module 5/6 classifier.

**Step 1 — Count your training data first.** Before you touch the model, fill this in from memory and from looking at your photos:

| Dimension | Count |
|---|---|
| Lighting: daylight / lamp / dark | ___ / ___ / ___ |
| Background: surface 1 / surface 2 / other | ___ / ___ / ___ |
| Held in hand / put down | ___ / ___ |
| Photographed by: how many different people? | ___ |
| Distance: close / far | ___ / ___ |

**Step 2 — Predict, in writing, before testing.** Write one sentence: *"I predict the model will be worst at ___ because my training data has only ___ examples of it."* Seal it (fold the paper, or write it at the top of the page and don't change it).

Predicting first is not a game. It is the difference between a test and a story you tell afterwards.

**Step 3 — Collect four batches of 8–12 photos each.** Same objects every time; change only the conditions. Suggested batches: **control** (matches training), **new lighting**, **held in your hand**, **new background**. If your model is not about objects, adapt: for a hand-gesture model use different hands, sleeves, and distances.

**Step 4 — Score them on paper.** One row per photo, filled in *as you go*, before you look at the totals:

| # | Batch | True label | Predicted | Confidence | Correct? |
|---|---|---|---|---:|---|

**Step 5 — Compute.** For each batch: fraction, decimal, percentage. Then overall accuracy. Then the accuracy gap in percentage points.

**Step 6 — Build the grid.** Batches down the side, classes across the top, like Step 7 of the Worked Example. Look for the surprise you were not testing for. There is almost always one.

**Step 7 — Open your prediction.** Were you right? Write one sentence either way. Being wrong here is more interesting than being right, and you should write that down too.

### Activity C — Confidence is not correctness, measured (15 min)

Take the photos your model got **wrong** in Activity B and write down the confidence it reported for each.

| Wrong photo | Confidence it gave | | Right photo | Confidence it gave |
|---|---:|---|---|---:|
| | | | | |

Compute two averages:

```
   average confidence when RIGHT  = ______
   average confidence when WRONG  = ______
```

Then answer:

1. Is the wrong-average much lower than the right-average? By how many points?
2. What was the **highest** confidence on a photo it got wrong? If that number is above 90%, write it in large letters somewhere you will see it.
3. If you built an app that only spoke when confidence was above 90%, how many of your wrong answers would it still have spoken aloud? How many correct ones would it have stayed silent on?

*What you should find:* confidence is usually a bit lower on mistakes, but there will be at least one confidently wrong answer, and often several. **That single number — the highest confidence on a wrong answer — is the most useful thing in your whole audit**, because it is the exact reason you cannot use a confidence threshold as a safety net.

### Activity D — Audit a real product's data map (15 min)

Pick one AI product you actually use: a video recommender, a photo app that sorts by face, a spam filter, a keyboard, a music shuffle, a homework helper.

Fill in this map. Guess where you must, and mark guesses with a `?` — an honest guess clearly labelled is worth far more than a confident invention.

```
   ┌────────────────────────────────────────────────────────────────────┐
   │  PRODUCT: ______________________________                           │
   │                                                                    │
   │  1. WHAT DATA GOES IN                                              │
   │     From me:        ______________________________________         │
   │     From others:    ______________________________________         │
   │     Collected how:  ______________________________________         │
   │     Did anyone agree? ____________________________________         │
   │                             │                                      │
   │                             ▼                                      │
   │  2. WHAT IT PREDICTS                                               │
   │     Input  → ____________________________________________          │
   │     Output → ____________________________________________          │
   │     Family (Module 1): rules / learned / generative ______         │
   │                             │                                      │
   │                             ▼                                      │
   │  3. WHO IS AFFECTED                                                │
   │     Helped most:    ______________________________________         │
   │     Helped least:   ______________________________________         │
   │     Affected but never asked: ____________________________         │
   │                             │                                      │
   │                             ▼                                      │
   │  4. WHAT GOES WRONG WHEN IT IS WRONG                               │
   │     Small harm:     ______________________________________         │
   │     Big harm:       ______________________________________         │
   │     Who finds out?  ______________________________________         │
   └────────────────────────────────────────────────────────────────────┘
```

The row that teaches the most is **"affected but never asked"**. For a spam filter, that is everyone who sends you email. For a face-sorting photo app, that is every person who happens to be in your photos. **Most AI systems affect far more people than use them**, and those people had no say at all.

---

## ✍️ Practice

Six exercises. Show the arithmetic; the answer key shows it too.

---

**1. [Warm-up] Sort the data, name the harm.**

A school app collects the following about each student:

```
   full name · student ID · date of birth · home postcode · photo of face ·
   daily arrival time · lunch choice · test scores · medical allergies ·
   parent phone number · which bus route they take · favourite colour
```

(a) Sort all twelve into three groups: **clearly personal**, **personal in combination**, **not personal**.
(b) Pick the three you think are most sensitive and, for each, write one specific sentence about who could misuse it and how.
(c) The school says "we removed the names, so the data is anonymous." Give a concrete counter-example using two or three of the remaining columns.
(d) The app wants to train a model to predict which students will be late tomorrow. Which columns should it be *forbidden* from using, and why? Give a reason for each.

*Done looks like:* a three-way sort of all twelve items, three misuse sentences, one re-identification counter-example, and at least two forbidden columns with reasons.

---

**2. [Warm-up] Compute a fairness gap.**

A "is this person smiling?" classifier was tested on four groups:

| Group | Correct | Total |
|---|---:|---:|
| A — wearing glasses | 18 | 20 |
| B — no glasses | 47 | 50 |
| C — with a beard | 9 | 25 |
| D — wearing a face mask | 6 | 15 |

(a) Overall accuracy as a fraction, a decimal, and a percentage. Show the addition and the division.
(b) Per-group accuracy as percentages, to one decimal place.
(c) The accuracy gap in percentage points. Name the best and worst groups.
(d) The company's website says "94% accurate". Which number are they quoting, and what does it hide?
(e) In real use the population is 45% group A, 45% group B, 5% group C, 5% group D. Compute the expected overall accuracy for that mix. Then explain the trap: has the model got better?

*Done looks like:* five answers with arithmetic shown, and a written explanation for (d) and (e).

---

**3. [Build] Trace a bias back to the data, then price the fix.**

A school built a "hand raised / hand not raised" detector for online classes.

**Training data (200 photos):**

| Clothing | Photos |
|---|---:|
| Short sleeves | 180 |
| Long sleeves | 20 |
| Jacket or blazer | 0 |

**Test results (50 held-out photos per group):**

| Clothing | Correct | Total |
|---|---:|---:|
| Short sleeves | 47 | 50 |
| Long sleeves | 31 | 50 |
| Jacket or blazer | 18 | 50 |

(a) Compute the three accuracies as percentages and the accuracy gap in percentage points.
(b) Put training share and test accuracy side by side in one table. Describe the relationship in one sentence.
(c) Write the causal chain in four steps, from how the data was collected to who gets hurt. Be specific about *who*.
(d) **Price the fix.** How many jacket photos must be added so that jackets make up 20% of the training set? Show the algebra.
(e) Now suppose the school is in a cold country where most students wear jackets for five months of the year. Explain in two sentences why the fix in (d) is still not enough, and say what you would do instead.
(f) Name one harm here that is not about accuracy at all.

*Done looks like:* three percentages and a gap, a two-column comparison table, a four-step chain naming real people, algebra with a whole-number answer, and two written answers.

---

**4. [Build] Design and run a fairness test on your own model.**

Using your Module 5/6 classifier and the results from Hands-On Activity B.

(a) List **four groups or conditions** you will test, and for each, one sentence saying why you suspect it might be weak — referring to a specific count in your training data.
(b) Write your prediction of the worst group **before** you look at any results.
(c) Report the scoring table: at least 8 photos per condition, with true label, prediction, confidence and correct/incorrect for each.
(d) Compute per-condition accuracy (fraction, decimal, percentage), overall accuracy, and the accuracy gap in percentage points.
(e) Build the condition × class grid and name one thing it shows that the condition table alone did not.
(f) Write the six-line honest report, in the format of Worked Example Step 10, **including the "do not use this model for…" line**.

*Done looks like:* four justified conditions, a sealed prediction, a scoring table of 32+ photos, four computed percentages plus a gap, a grid, and a report that ends with a usage boundary.

---

**5. [Stretch] Should your school use face recognition for attendance?**

A company offers your school a camera at the gate that recognises faces and marks attendance automatically. Their claim: **"98% accurate."**

An independent test finds the system fails to recognise a student who *is* present (a **false reject**, marking them absent) at these rates:

| Group | False reject rate |
|---|---:|
| Overall average | 2% |
| Students wearing a headscarf | 8% |
| Students wearing glasses | 3% |
| Students who recently changed hairstyle | 6% |

(a) A school year is **180 days**. For a student in the overall-average group and a student who wears a headscarf, compute the expected number of days each is wrongly marked absent in one year. Show both multiplications.
(b) Compute the difference, and then the totals over **four years** of school.
(c) The school has 600 students. At the overall 2% rate, how many wrong absence marks happen **per day** across the whole school? If a staff member needs 4 minutes to fix each one, how many minutes per day is that? Convert to hours and minutes.
(d) List three harms of a wrongly recorded absence that are **not** about the number itself. Think about who receives the message and what happens next.
(e) The company says the gap is "only 6 percentage points". Write a two-sentence reply using your numbers from (a) and (b).
(f) Write a recommendation to the head teacher: adopt, adopt with conditions, or reject. State your decision, give three reasons, and name one piece of evidence that would change your mind.

*Done looks like:* four computed numbers in (a) and (b), a per-day figure converted to hours and minutes, three non-numeric harms, a two-sentence reply, and a recommendation with three reasons and a falsifier.

---

**6. [Stretch] Fakes, credit, and the confident answer.**

**Part 1 — Verification.** A video reaches you showing a well-known athlete apparently saying they are quitting. It was posted eleven minutes ago by an account with 40 followers, created last week. It has 90,000 shares.

(a) Apply the four-step check from section 3. Write what you would actually do at each step — the specific action, not the principle.
(b) Give two signals here that point to a fake **without examining a single pixel**.
(c) You check and cannot find any other source. Does "no other source" prove it is fake? Explain what it does and does not tell you.
(d) Your friend has already forwarded it to 30 people. Write the message you would send them — three sentences, and do not make them feel stupid, because people who feel stupid stop listening.

**Part 2 — Attribution.** Rate each scenario as **fine**, **needs a credit line**, or **should not do it**, with a one-sentence reason:

```
   1. You use an AI to fix the grammar in an essay you wrote and hand it in.
   2. You ask an AI to write the essay and hand it in as your own.
   3. You train a model on 200 of your own drawings and post the output.
   4. You train a model on 200 drawings by a living artist you found online,
      then sell prints "in their style".
   5. You use an AI to make a poster for the school fair and put it on the wall.
   6. You use an AI voice of a classmate saying something they never said, as a joke.
```

**Part 3 — Over-trust.** For each situation, say whether you should trust the AI answer, which of the three warning situations from section 5 it matches, and exactly what you would do instead:

```
   A. "Write me a limerick about a goat."
   B. "What is the correct dose of this medicine for a 30 kg child?"
   C. "Summarise the three paragraphs I just pasted."
   D. "What was the score of my school's cricket match last Tuesday?"
   E. "Is my friend angry with me? Here is what she texted."
   F. "Give me five sources about the Chola dynasty, with page numbers."
```

*Done looks like:* four verification answers, six attribution ratings with reasons, and six over-trust answers each naming a warning situation and an alternative action.

---

## 🤔 Think Deeper

**1. Can a model be fair to everyone at once?**
Suppose a model is used to pick which students get a free tutoring place. "Fair" could mean: equal accuracy for every group; or equal numbers of places per group; or places going to whoever the model scores highest regardless of group; or equal *error* rates rather than equal *success* rates. Mathematicians have proved that in realistic conditions you cannot satisfy all of these at the same time. So who chooses which fairness you optimise for?

*How to reason about it:* pick two definitions and construct a small numerical example — twenty students, two groups — where satisfying one definition clearly violates the other. Once you have built that example the abstract argument becomes concrete and you will never lose it. Then ask the question underneath: this is a choice about *values*, so should an engineer be making it alone at a keyboard, and if not, who should be in the room? Notice too that "we'll just use the raw scores and not think about groups" is not a neutral option — it is one of the choices, with its own winners and losers.

**2. Is it better to have a biased AI or no AI at all?**
A medical scanning tool works well for 85% of patients and poorly for 15%. Withdrawing it helps nobody: the 85% lose a real benefit. Deploying it means the 15% get worse care than everyone else and may not be told. Which is worse — an unequal benefit, or no benefit?

*How to reason about it:* the fake version of this question compares the tool against perfection. The real version compares it against **what those patients get today**, which is often nothing, or a long wait, or a tired human. Work out the actual baseline before you judge. Then separate the deployment question from the honesty question: much of the harm here comes not from using the tool but from using it *silently* — a tool that announces "this scan is outside my reliable range, escalate to a specialist" is a completely different product from the same model shipped without that line. Ask what changes if the 15% are told, given a choice, and prioritised for the fix.

**3. If you were never asked, were you harmed?**
Your photos, your writing, your voice notes and your search history may already sit inside training data. You did not agree to it in any meaningful sense — you clicked a box. Nothing bad has visibly happened to you. Is that a harm?

*How to reason about it:* try distinguishing three different things people mean by harm. **Concrete harm:** something measurable happened to you. **Risk:** the chance of concrete harm went up, even though nothing has happened yet. **Dignity:** something of yours was taken and used without asking, and that is wrong regardless of consequences. Decide which of these you find persuasive, and test your view by swapping the subject: does your answer change if the data is your face rather than your search history? A stranger's rather than yours? A dead person's? If your answer shifts, work out which feature made it shift — that feature is the thing you actually care about, and now you can say it out loud.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reporting one overall accuracy number | It is the number the tool shows you, and it is usually the flattering one | Always split by group and report the **gap** in percentage points. A single number is a summary, and every summary hides someone |
| Choosing test groups after seeing results | You spot a bad batch and quietly drop it, or you go hunting for a group that looks good | List your groups and write your prediction **before** collecting any results. Fold the paper |
| Thinking "I'm not biased, so my model isn't" | Bias feels like an accusation about your character | Bias here is about **counts, not intentions**. Point at the training data table. Nobody has to have done anything wrong for a 50-point gap to exist |
| "We removed the names, so it's anonymous" | Names feel like the identifying part | Two or three ordinary columns usually identify one person. Test it: try to find yourself in your own dataset |
| Confusing percent with percentage points | They both have a % sign nearby | 41.7% → 91.7% is **50 percentage points**, and about **120 percent** of the original. Subtracting percentages always gives points |
| Trusting a high confidence score | 97% looks like a promise | Confidence means "best of my options", not "probability I'm right". Find your highest confidence on a wrong answer and remember that number |
| Judging a fake by looking harder at it | "I can spot a fake" feels like a skill | Generators outrun your eye every few months. Check **provenance** — first source, corroboration, reverse search, motive |
| Only fact-checking things you dislike | Content you agree with does not trigger suspicion | Run the same four steps on the things that delight you. Especially those. They are the ones you will forward |
| Asking the same AI to verify its own answer | It is right there, and it sounds authoritative | It will confirm itself in the same confident voice. Use two independent sources that do not copy each other |
| Saying "the algorithm decided" | It sounds neutral and removes the awkwardness | People chose the data, the classes, the threshold, and the deployment. Naming a human is not blame — it is where the fix lives |

---

## 🛠️ Mini-Project — Fairness Audit Poster

**Time:** 75–90 minutes · **You need:** your Module 5 model, a phone camera, one large sheet of paper (or a single slide), coloured pens

### 🎯 Goal

One poster that does two things at once: maps a real AI product from data to consequences, and publishes a measured, honest bias test of your own model — including the number that makes you look bad.

### 📋 Starter steps

**Part 1 — The product data map (20 min)**

Pick a real AI product you personally use. Fill in all four blocks from Hands-On Activity D. Mark every guess with a `?`.

Draw it on the left half of your poster as a flow, not a list:

```
   DATA IN  ──►  WHAT IT PREDICTS  ──►  WHO IS AFFECTED  ──►  WHAT GOES WRONG
```

Under "who is affected", you must fill three boxes: **helped most**, **helped least**, and **affected but never asked**. That third box is the one adults skip and the one that makes the poster worth reading.

**Part 2 — The bias test on your own model (35 min)**

**Step 1 — Count your training data** across at least three dimensions (lighting, background, held/not held, distance, who took the photos). Put the counts on the poster. This is your evidence, not decoration.

**Step 2 — Write your prediction** of the worst condition, with the training count that justifies it, before you collect anything. Put the prediction on the poster whether or not it turns out right.

**Step 3 — Collect four batches** of 8–12 photos each. Suggested: control (matches training), **new lighting**, **new hands** (get someone else to hold the object — different hand size, skin tone, sleeve, nail polish, jewellery), **new background**. Same objects throughout.

**Step 4 — Score every photo on paper** as you go: true label, prediction, confidence, correct or not. No editing afterwards.

**Step 5 — Compute:** per-condition accuracy (fraction → decimal → percentage), overall accuracy, and the **accuracy gap in percentage points**. Show at least one full division on the poster so a reader can see it is real arithmetic.

**Step 6 — Build the condition × class grid** and circle the worst cell.

**Step 7 — Note the highest confidence the model gave on a photo it got wrong.** Put that number on the poster in large text with the caption "the model said this, and was wrong".

**Part 3 — The fix, priced (10 min)**

Not "collect more data". A specific, countable plan:

- Which condition you would fix first, and why that one.
- **How many photos**, worked out with the algebra from Worked Example Step 9.
- How you would know it worked — name the retest and the number you would want to see.
- One thing you would put in the product itself: a warning, a refusal to answer below some confidence, a limitation stated in the instructions.

**Part 4 — Assemble the poster (15 min)**

Required elements:

```
   ┌───────────────────────────────┬───────────────────────────────┐
   │  DATA MAP                     │  MY MODEL'S BIAS TEST         │
   │  (real product)               │                               │
   │                               │  training data counts         │
   │  data in                      │  my prediction (sealed)       │
   │      ↓                        │  results table, 4 conditions  │
   │  what it predicts             │  ACCURACY GAP: ___ pts        │
   │      ↓                        │  condition × class grid       │
   │  who is affected              │  highest confidence           │
   │   • helped most               │    while WRONG: ___%          │
   │   • helped least              │                               │
   │   • never asked ★             │                               │
   │      ↓                        ├───────────────────────────────┤
   │  what goes wrong              │  MY FIX: ___ more photos of   │
   │                               │  ___, then retest and publish │
   ├───────────────────────────────┴───────────────────────────────┤
   │  DO NOT USE THIS MODEL FOR: _________________________________ │
   └───────────────────────────────────────────────────────────────┘
```

That bottom strip is compulsory and should be the boldest thing on the poster.

### ✅ Success criteria checklist

- [ ] A four-block data map of a real product, with guesses marked `?`
- [ ] The "affected but never asked" box filled in with real people
- [ ] Training data counted across at least three dimensions, on the poster
- [ ] A written prediction made **before** testing, shown whether right or wrong
- [ ] Four test conditions, 8+ photos each, scored on paper as you went
- [ ] Per-condition accuracy as fraction, decimal and percentage, with one division shown
- [ ] An **accuracy gap in percentage points**, clearly labelled
- [ ] A condition × class grid with the worst cell circled
- [ ] The highest confidence on a wrong answer, displayed large
- [ ] A fix with a **specific number of photos**, backed by algebra
- [ ] A "do not use this model for…" line in the boldest text on the poster
- [ ] You presented it to someone and answered one hard question without saying "magic"

### 🚀 Level it up

Pick one:

- **Fix it and prove it.** Actually collect the photos your plan calls for, retrain, and rerun the **identical** four test batches. Add a second results column labelled "after". Report both numbers, including the possibility that your control batch got slightly *worse* — which often happens, and is itself a real finding worth explaining. A before-and-after table you measured yourself is the single most persuasive thing you can put in front of an adult.
- **Audit somebody else's model.** Swap models with a friend. Neither of you may see the other's training data. Each writes a prediction, runs four conditions, and reports a gap. Then reveal the training-data counts and see whether the auditor correctly guessed the hole from the outside. This is exactly what real independent auditors do, and finding out how hard it is without access to the data is the lesson.

---

## 🔑 Key Takeaways

- **Bias is the default, not an accident.** A model gets good at whatever it saw a lot of. If a group is missing from the training data, the model will be bad at that group, and nobody has to have done anything wrong for it to happen.
- **A single accuracy number hides people.** Split by group, report the **accuracy gap in percentage points**, and remember that the overall number can be moved 16 points just by choosing how many photos of each kind to test.
- **Trace failures backwards to the data, not the model.** Put training coverage and test accuracy side by side. The gap in the results is usually the same shape as the gap in the data.
- **Personal data is wider than names.** Two or three ordinary columns usually identify one person, and what you put into a system may not be removable later.
- **Check provenance, not pixels.** First source, independent corroboration, reverse search, and who benefits — especially when the content is something you were hoping was true.
- **Three no-trust situations:** high stakes and hard to undo; a specific checkable fact; an input that is rare, recent, local, or about you. In all three, the AI answer is a question to research, not an answer.
- **Reporting the boundary is the skill.** Anyone can publish a good number. "Do not use this model for ___" is what makes you trustworthy.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Bias** | When a model works noticeably worse for some group than others | 91.7% in daylight, 41.7% held in a hand |
| **Accuracy gap** | Best group's accuracy minus worst group's, in percentage points | 91.7 − 41.7 = 50.0 percentage points |
| **Percentage points** | The unit you get when you subtract two percentages | 41.7% → 91.7% is a rise of 50 points |
| **Fairness audit** | Deliberately testing a model group by group to find who it fails | Four batches of 12 photos, scored separately |
| **Personal data** | Information about an identifiable person | A face photo, a phone number, a home postcode |
| **Re-identification** | Working out who someone is from "anonymous" data | Year 7 + postcode 3 + left-handed = one person |
| **Metadata** | Hidden information a file carries about itself | The GPS location and time stored inside a photo |
| **Deepfake** | A fake photo, video or voice of a real person, made by AI | A video of an athlete saying something they never said |
| **Misinformation** | False information spreading, whether or not on purpose | An old photo reposted as if it happened today |
| **Disinformation** | False information spread deliberately to deceive | A fake video made and posted to swing an election |
| **Provenance** | Where something came from and how it got to you | "First posted by this account, eleven minutes ago" |
| **Attribution** | Saying who made something and where it came from | "20 photos from my brother, with permission, 4 March" |
| **Automation bias** | Trusting the machine over your own judgement | Following the satnav into a river |
| **Over-trust** | Accepting an AI answer without checking, because it sounded sure | Copying a book title the AI invented into your homework |
| **False reject** | The system fails to recognise someone who really is there | A present student marked absent by the face scanner |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Sort the data, name the harm

**(a) The three-way sort.**

| Clearly personal | Personal in combination | Not personal on its own |
|---|---|---|
| Full name | Home postcode | Favourite colour |
| Student ID | Daily arrival time | Lunch choice |
| Date of birth | Which bus route | |
| Photo of face | Test scores | |
| Medical allergies | | |
| Parent phone number | | |

Two judgement calls worth defending. **Test scores** are placed in the middle column because a score by itself identifies nobody, but "the student who scored 98% in Year 7 maths" often identifies exactly one person in a school. **Lunch choice** looks harmless, and mostly is — until you notice that a consistent halal, kosher or vegetarian choice can reveal religion, which is sensitive. Almost nothing is truly in column three once you combine it with something else.

**(b) Three most sensitive, with a specific misuse each.**

1. **Medical allergies.** An insurance company or a future employer buying leaked school data could use a childhood allergy record as a reason to charge more or hire someone else, and the student would never be told that was the reason.
2. **Photo of face plus daily arrival time.** Someone who wanted to find a specific child in person would know what they look like and exactly when and where they will be — the two pieces that turn general information into an opportunity.
3. **Parent phone number plus student name.** A scammer can phone a parent saying "there has been an incident with [correct child's name] at school, we need a payment now". The correct name is what makes the scam work; the number is what delivers it.

**(c) Re-identification counter-example.**

Take **postcode + date of birth + bus route**. In a school of 600, the number of students living in one small postcode area is maybe 40; of those, the number born on one exact date is usually zero or one; and the bus route confirms it. No name needed. In practice **postcode + date of birth alone** identifies a single student the overwhelming majority of the time, and both look like harmless "background" columns to whoever published the file.

**(d) Columns the lateness model should be forbidden from using.**

| Forbidden | Why |
|---|---|
| **Medical allergies** | Nothing to do with lateness. Health data must never be repurposed for a discipline-adjacent prediction, because the moment it is in the model it starts influencing how a child is treated for reasons no one can see |
| **Home postcode** | It is a strong stand-in for family income and neighbourhood. The model would learn "children from poorer areas are late" and start flagging them in advance — punishing children for where they live, dressed up as a prediction |
| **Photo of face** | Completely unnecessary for the task, and the biggest privacy risk in the dataset. If a column is not needed, collecting it is the harm |
| **Test scores** | Would link lateness to academic performance and quietly build a "problem student" profile that follows a child around |

The general principle, worth memorising: **use the smallest number of columns that does the job.** Bus route and past arrival times are enough to predict lateness. Everything else adds risk and adds nothing.

---

### Exercise 2 — Compute a fairness gap

**(a) Overall accuracy.**

```
   correct = 18 + 47 + 9 + 6  = 80
   total   = 20 + 50 + 25 + 15 = 110

   fraction:    80/110  =  8/11
   decimal:     80 ÷ 110 = 0.727272...
   percentage:  ×100 = 72.7%
```

**(b) Per-group accuracy.**

```
   A:  18 ÷ 20 = 0.90    →  90.0%
   B:  47 ÷ 50 = 0.94    →  94.0%
   C:   9 ÷ 25 = 0.36    →  36.0%
   D:   6 ÷ 15 = 0.40    →  40.0%
```

**(c) Accuracy gap.**

```
   best  = group B (no glasses)  = 94.0%
   worst = group C (with a beard) = 36.0%

   gap = 94.0 − 36.0 = 58.0 percentage points
```

Fifty-eight points. Group C is wrong nearly two times in three.

**(d) The "94% accurate" claim.**

They are quoting **group B's score only** — their single best group — and presenting it as the product's accuracy. That is not a rounding difference or an honest simplification; the overall figure on the same test was 72.7%, and one group scored 36.0%.

What it hides: that a bearded person using this product gets a wrong answer 64% of the time, and a masked person 60% of the time. Anyone reading "94% accurate" would reasonably conclude they had roughly a 1-in-17 chance of a wrong answer. For group C the real figure is closer to 2 in 3 — about eleven times worse than advertised.

**(e) Expected accuracy on the realistic mix.**

```
   0.45 × 0.90 = 0.4050
   0.45 × 0.94 = 0.4230
   0.05 × 0.36 = 0.0180
   0.05 × 0.40 = 0.0200
   ───────────────────────
   total       = 0.8660  →  86.6%
```

**The trap.** The headline number jumped from 72.7% to 86.6% — a rise of nearly 14 points — and **the model did not change at all.** Not one number inside it moved. All that changed was the *mix of people in the test*.

This is the most important idea in the exercise, so it is worth being blunt: **making your test set match the real population makes the headline number look better precisely by giving the failing groups less weight.** Group C is still wrong 64% of the time. There are simply fewer of them in the average now.

That does not mean a realistic test mix is wrong — you need one to predict how the product performs overall. It means **the realistic mix is the wrong tool for finding harm**, because a small group can be catastrophically failed and barely move the average. You need both: a population-weighted number to describe the product, and a **per-group table** to find who it hurts. Report only the first and you have hidden group C behind arithmetic.

---

### Exercise 3 — Trace a bias back to the data, then price the fix

**(a) Accuracies and gap.**

```
   short sleeves:  47 ÷ 50 = 0.94  →  94.0%
   long sleeves:   31 ÷ 50 = 0.62  →  62.0%
   jacket:         18 ÷ 50 = 0.36  →  36.0%

   gap = 94.0 − 36.0 = 58.0 percentage points
```

**(b) Side by side.**

| Clothing | Training photos | Training share | Test accuracy |
|---|---:|---:|---:|
| Short sleeves | 180 | 90.0% | 94.0% |
| Long sleeves | 20 | 10.0% | 62.0% |
| Jacket / blazer | 0 | 0.0% | 36.0% |

**One sentence:** test accuracy rises and falls with training share almost perfectly — 90% coverage gives 94% accuracy, 10% coverage gives 62%, and zero coverage gives 36%, which is barely better than guessing between two options.

**(c) The four-step causal chain.**

1. **Collection.** Someone recorded training clips over a few sessions in a warm room — or asked volunteers who happened to be in short sleeves — so 180 of 200 photos show bare forearms and none show a jacket.
2. **Data.** The training set now contains a hidden assumption it was never asked about: *a raised hand is attached to a bare arm*. The model has no examples that separate "arm shape" from "hand raised".
3. **Model.** The model learns edges and shapes that include the bare forearm — the long light-coloured region below the hand. A jacket sleeve covers that region, changes its colour and its edges, and shortens the visible arm, so the pattern the model relies on is gone.
4. **Who gets hurt.** *Students who wear a blazer, a school jacket, or long sleeves for warmth, for religious reasons, or because they are cold.* Their raised hands are missed 64% of the time. They are not called on, they appear disengaged in the teacher's dashboard, and they are quietly marked down for participation — for wearing a coat.

Note the last step carefully: the harm is not "the model is 36% accurate". The harm is **a specific child being marked as not participating, repeatedly, and never being told why.**

**(d) Pricing the fix.**

Let `x` = jacket photos to add. Currently 200 photos with 0 jackets. Target: jackets = 20% of the new total.

```
        x / (200 + x)  = 0.20
                    x  = 0.20 × (200 + x)
                    x  = 40 + 0.20x
             x − 0.20x = 40
                 0.80x = 40
                     x = 40 ÷ 0.80
                     x = 50
```

**Add 50 jacket photos.** Check: new total = 250, jackets = 50, and 50 ÷ 250 = 0.20 ✓.

**(e) Why 20% is still not enough in a cold country.**

If most students wear jackets for five of the ten school months, then jackets are not a minority case at all — they are roughly **half of real use**, so a training set that is 20% jackets still under-represents the actual conditions by a factor of about two and a half.

What I would do instead: match the training mix to the *deployment* mix, not to some generic idea of "enough". Collect until jackets are about 45–50% of the training set — around 180 more jacket photos, giving roughly 180 short-sleeve, 20 long-sleeve and 180 jacket — and then split the test set the same way so the winter case has enough photos to give a trustworthy number. And I would test again in *January*, not in the same warm week I collected everything else, because clothing is not the only thing that changes with the season (light levels change too).

**(f) A harm that is not about accuracy.**

Several are valid:

- **Surveillance.** The system requires a camera watching every child continuously in their own home during online classes, and it records their clothing, their room, and everyone who walks behind them. That harm exists at 100% accuracy.
- **Chilling effect.** Students who know they are being scored by a camera behave differently — some stop raising their hands at all rather than risk being missed, which is the exact opposite of what the system was for.
- **Shifted burden of proof.** When the machine says a child did not participate, the child now has to prove they did. A child arguing with a dashboard usually loses.
- **The wrong metric became the goal.** "Hand raised" is a proxy for engagement, and it is a poor one — a student who is listening intently and thinking hard scores zero. Once you can measure something, it starts being what people optimise for.

---

### Exercise 4 — Design and run a fairness test on your own model

This is your own data, so here is a full worked example in the required format. Yours will differ; the **structure** is what is being marked.

**(a) Four conditions, each justified by a count.**

| Condition | Why I suspect it | Training count |
|---|---|---|
| Control: daylight, kitchen counter | Matches training exactly; establishes the ceiling | 48 of 60 |
| Lamp light at night | I took almost nothing in artificial light | 6 of 60 |
| Held in someone else's hand | I never held anything, and never involved another person | **0 of 60** |
| Patterned tea-towel background | Every photo was on the same plain surface | **0 of 60** |

**(b) Prediction, written before testing.**

> "I predict the model will be worst at objects **held in someone else's hand**, because 0 of my 60 training photos show a hand at all, and a hand adds a large area of skin-coloured pixels with strong edges that also hides part of the object."

**(c) Scoring table** (extract — the full sheet has 40 rows, 10 per condition):

| # | Batch | True | Predicted | Conf. | ✓/✗ |
|---:|---|---|---|---:|---|
| 1 | control | comb | comb | 96% | ✓ |
| 2 | control | spoon | spoon | 99% | ✓ |
| 3 | control | toothbrush | toothbrush | 88% | ✓ |
| … | | | | | |
| 21 | hand | comb | toothbrush | **93%** | ✗ |
| 22 | hand | toothbrush | comb | 71% | ✗ |
| 23 | hand | spoon | spoon | 84% | ✓ |
| … | | | | | |

**(d) The numbers.**

```
   control:   9/10  = 0.90  →  90.0%
   lamp:      6/10  = 0.60  →  60.0%
   hand:      4/10  = 0.40  →  40.0%
   pattern:   5/10  = 0.50  →  50.0%

   overall = (9 + 6 + 4 + 5) ÷ 40 = 24 ÷ 40 = 0.60 → 60.0%

   accuracy gap = 90.0 − 40.0 = 50.0 percentage points
```

**(e) The condition × class grid.**

| | comb | spoon | toothbrush | total |
|---|---:|---:|---:|---:|
| control | 3/3 | 3/3 | 3/4 | 9/10 |
| lamp | 2/3 | 3/3 | 1/4 | 6/10 |
| hand | 1/3 | 3/3 | 0/4 | 4/10 |
| pattern | 1/3 | 3/3 | 1/4 | 5/10 |
| **total** | **7/12 = 58.3%** | **12/12 = 100%** | **5/16 = 31.3%** | 24/40 |

Check the arithmetic: 7 + 12 + 5 = 24 ✓, and 12 + 12 + 16 = 40 ✓ (each batch had 3 combs, 3 spoons, 4 toothbrushes).

**What the grid shows that the condition table did not:** spoon is perfect in every single condition (12/12) while toothbrush is at 31.3% and scored **0/4** in the hand batch. The condition table blamed the conditions; the grid shows the real story is that one class is carrying the model and one class is broken almost everywhere. Averaging across classes hid a class that fails outright.

**(f) The honest report.**

> **Model:** three-class household object classifier (comb, spoon, toothbrush), 60 training photos in Teachable Machine.
>
> **Overall accuracy on 40 held-out photos: 60.0%** — do not quote this alone; it depends on how many photos of each condition I chose to take.
>
> **Per condition:** control 90.0%, lamp light 60.0%, **held in another person's hand 40.0%**, patterned background 50.0%. **Accuracy gap: 50.0 percentage points.**
>
> **Worst group:** objects held in another person's hand. **Cause:** 0 of 60 training photos contained a hand.
>
> **Second finding, which I was not testing for:** toothbrush scores 31.3% across all conditions and 0/4 when held, while spoon scores 100%. The model is not really a three-class classifier — it is a reliable spoon detector attached to a coin flip between comb and toothbrush.
>
> **Highest confidence on a wrong answer: 93%** (a comb confidently called a toothbrush). A 90% confidence threshold would not have caught it.
>
> **Fix:** add 20 held-in-hand photos (25% of a new 80-photo set), weighted toward toothbrush and comb, then rerun these identical four batches and publish both columns.
>
> **Do not use this model** to tell a comb from a toothbrush, in anything other than bright daylight, on a plain surface, with the object put down and nobody's hand in shot — and never in a situation where somebody would act on the answer.

---

### Exercise 5 — Should your school use face recognition for attendance?

**(a) Wrongly marked absent in one 180-day year.**

```
   overall-average student:   0.02 × 180 = 3.6 days
   headscarf-wearing student: 0.08 × 180 = 14.4 days
```

**(b) Difference, and four-year totals.**

```
   difference in one year:  14.4 − 3.6 = 10.8 days

   over four years:
      average student:   3.6 × 4  = 14.4 days
      headscarf student: 14.4 × 4 = 57.6 days
      difference:        57.6 − 14.4 = 43.2 days
```

Put that in human terms before moving on. **57.6 days is more than eleven school weeks** of being marked absent while sitting in the classroom. And a student in the average group racks up 14.4 wrong marks over the same period, which is itself not nothing.

**(c) School-wide load.**

```
   600 students × 2% = 600 × 0.02 = 12 wrong marks per day

   12 × 4 minutes = 48 minutes per day
```

**48 minutes per day = 0 hours 48 minutes.** Over a 180-day year:

```
   48 × 180 = 8,640 minutes
   8,640 ÷ 60 = 144 hours   →  about 18 full working days of staff time per year
```

So the system that was sold as saving administration time creates **144 hours a year of new administration** — and that is only if every wrong mark is actually noticed and corrected, which it will not be.

**(d) Three harms that are not the number itself.**

1. **An automatic message goes to a parent** saying their child was absent. The child says they were there. The parent now has to choose between believing their child and believing the school's computer, and that argument happens in someone's kitchen, repeatedly, with no way to settle it.
2. **The record follows the student.** Attendance figures feed into reports, references, and sometimes legal thresholds for prosecuting parents over truancy. A 57.6-day error over four years is not a spreadsheet inconvenience; it is a number that could appear in a formal letter.
3. **The burden of proof inverts.** Normally a school must show a child was absent. Now the child must prove they were present, against a machine that "is 98% accurate", to a busy adult who has seen the system be right many times. **Automation bias means the child usually loses.** And a child who has to argue every week eventually stops arguing.

A fourth, worth adding: the students affected are disproportionately those wearing a headscarf, so a system that is technically neutral produces an outcome that lands on one religious group. Even with no ill intent anywhere, the effect is discriminatory.

**(e) Two-sentence reply to "only 6 percentage points".**

> Six percentage points means a headscarf-wearing student is wrongly marked absent **14.4 days a year against 3.6** — four times as often, and 57.6 days across four years of school. A difference that lands on one identifiable group, four times over, and generates a letter to their parents every time, is not "only" anything.

**(f) Recommendation.**

**Reject — or at most, adopt with strict conditions that the company is unlikely to accept.**

Three reasons:

1. **The error is not evenly distributed and it is not small.** 8% against 2% means one identifiable group of students carries four times the burden, for four years, generating parent letters and permanent records. A system that is unequal in exactly this way should not be installed on children who cannot opt out.
2. **The claimed benefit is not real.** The system was justified by saving staff time, and my calculation in (c) shows it creates roughly 144 hours a year of correction work — and only if every error is caught. Measured against its own goal it fails before fairness is even discussed.
3. **The cost of the alternative is low.** A teacher reading a register takes about two minutes, has an error rate near zero, involves no biometric database of 600 children's faces, and cannot be hacked or sold. When the low-tech option is this cheap and this good, the bar for replacing it should be very high.

**Evidence that would change my mind:** an independent audit — not the company's own — on a group of students matched to ours, showing false-reject rates below 1% **for every measured group**, with the group breakdown published; plus a written commitment that a student's verbal statement overrides the machine without needing an adult's approval, that faces are stored on school premises and deleted at the end of each year, and that families can opt out and use a register instead with no penalty. If all of that were true and independently verified, the calculation genuinely changes and I would revisit it.

---

### Exercise 6 — Fakes, credit, and the confident answer

**Part 1 — Verification**

**(a) The four steps, as actions.**

1. **Source.** Tap the account that posted it. Check the join date, total post count, and whether it has ever posted anything else about this sport. Then search the athlete's own verified account and their club's account — if they are retiring, it will be there, and if it is not there, that is a very loud silence.
2. **Corroborate.** Search the athlete's name in a news app and sort by newest. A genuine retirement announcement from a well-known athlete is covered by multiple independent news organisations within minutes. Check at least two that are not owned by the same company.
3. **Reverse.** Screenshot a clear frame and run a reverse image search. Look for whether this footage exists elsewhere with different audio, or is from an older press conference on a different topic. Relabelled real footage is the most common fake there is.
4. **Motive.** Ask who gains. A 40-follower account that has just collected 90,000 shares has gained enormously — attention is the payment. Then the harder question: *am I inclined to believe this because I follow this sport and would find it dramatic?*

**(b) Two signals without examining a single pixel.**

1. **The account is a week old with 40 followers.** A real scoop about a famous athlete does not break from an account with no history; it breaks from the athlete, their club, or a journalist with a reputation to lose.
2. **The share count is wildly out of proportion to the account's size, eleven minutes in.** 90,000 shares from a 40-follower account in eleven minutes is not organic spread — it indicates either coordinated pushing or that the content was engineered to be maximally shareable, and both are reasons for suspicion.

A third, if you want it: nobody else is reporting it (see (c)).

**(c) Does "no other source" prove it is fake?**

**No.** It is strong evidence, not proof, and the distinction matters.

What it *does* tell you: for an event this big, involving a famous person, silence everywhere else eleven minutes in is very hard to explain if the video is real. Real news about famous people propagates fast and from multiple directions. So the absence of corroboration should move your belief a long way toward "fake".

What it does *not* tell you: absence of evidence is not evidence of absence. It is possible — rarely — to be genuinely first. Perhaps the video was filmed by one person at a small event, and reporting will catch up in an hour.

The correct action is therefore not "declare it fake" but **"do not share it, and wait"**. Waiting an hour costs you nothing. Sharing a fake costs you your credibility, and helps it reach the next 90,000 people. The right output of a verification check is often *"I don't know yet"* — and being comfortable sitting in that state is the actual skill.

**(d) The message to your friend.**

> Hey — I looked into that clip and I can't find it anywhere except one account that was made last week, and none of the sports sites have it, which is strange for news this big. I'm not saying it's definitely fake, but I'd wait an hour before believing it. Might be worth sticking a "not confirmed yet" on the group chat, since a lot of people have it now.

Why it is worded that way: no accusation, no "I can't believe you fell for that", an actual reason rather than an assertion, an admission of uncertainty ("not saying it's definitely fake"), and a concrete, easy, face-saving next step. **People who feel corrected get defensive and dig in. People who feel included in the investigation help you.**

**Part 2 — Attribution**

| # | Scenario | Rating | Reason |
|---|---|---|---|
| 1 | AI fixes grammar in your own essay | **Fine** *(usually — check your school's rule)* | The ideas, structure and argument are yours; a grammar fix is the same category of help as a spellchecker or a parent proofreading |
| 2 | AI writes the essay, handed in as yours | **Should not do it** | The assignment is asking what *you* can do. Submitting someone else's work as your own is dishonest regardless of whether that someone is a person or a machine — and you also lose the practice, which was the actual point |
| 3 | Model trained on your own 200 drawings | **Fine** | Your work, your model, your output, nobody else involved. Saying "made with a model I trained" is still good practice for your audience |
| 4 | Model trained on a living artist's work, prints sold "in their style" | **Should not do it** | You are using their work as the raw material, competing directly with them, and profiting from their name and reputation without asking or paying. The scale and the direct competition are what separate this from a human being influenced by an artist |
| 5 | AI-made poster for the school fair | **Needs a credit line** | Nothing wrong with it, but write "poster made with AI" on it — people are entitled to know whether a human drew it, and the habit of labelling is what you are building |
| 6 | AI voice of a classmate saying something they never said | **Should not do it** | It is their voice and their reputation, and you cannot control where a clip travels after you make it. "It was a joke" does not survive the clip being forwarded to someone who does not know that. Nobody may use another person's likeness without permission |

**Part 3 — Over-trust**

| | Trust it? | Warning situation | What to do instead |
|---|---|---|---|
| **A** limerick about a goat | **Yes** | None — no fact can be wrong, and you can judge the result yourself | Just use it. Read it first to make sure it's actually funny |
| **B** medicine dose for a 30 kg child | **No** | **#1 high stakes and irreversible**, and **#2 a specific checkable number** | Ask a pharmacist or doctor, or read the printed leaflet in the box. Never act on a dose from a chatbot, not even to double-check one you already have |
| **C** summarise three pasted paragraphs | **Mostly yes** | Mild #2 — it can drop or distort a detail | Read the summary against the original. Because you have the source right there, checking costs ten seconds — this is the ideal shape of AI use |
| **D** your school's cricket score last Tuesday | **No** | **#3 rare, recent and local** — almost certainly no data about it | Ask someone who was there, or check the school's own page. If the AI answers with a confident score, that is invention, and its confidence tells you nothing |
| **E** "is my friend angry with me?" | **No** | **#3 about specific real people the model knows nothing about**, plus a private message you should think twice about pasting anywhere | Ask your friend. An AI is guessing from text with none of the history, tone or context, and acting on its guess can damage a real relationship. Also note you have just shared someone else's private message with a company |
| **F** five sources with page numbers | **No** | **#2 in its purest form** — titles, authors and page numbers are the single most commonly invented category | Use a library catalogue or an academic search engine to find real sources. If you use AI at all here, use it to suggest *search terms*, then find the sources yourself and cite only what you have actually opened |

**The pattern across all six.** The safe ones (A, C) share two features: a wrong answer is cheap, and **you can check it yourself in seconds**. The dangerous ones (B, D, F) share the opposite: they are specific, they are checkable *in principle* but not by glancing, and being wrong costs something real. E is its own category — the model has no access to the one thing that would make an answer meaningful, which is the actual person.

**The one-line rule to carry out of Level 1:** *push the AI toward drafting, and keep deciding for yourself.*

---

</details>

---

[⬅ Previous](module-08-how-computers-read-and-chat.md) · [Level 1 Home](README.md) · [Next ➡](capstone.md)

*You have finished the nine modules of Level 1. You can tell a rulebook from a learned model, build an honest dataset, train a classifier, test it without cheating, explain how a machine sees a photo and guesses a word, and find out who your model fails. One thing is left: put all of it into a single build that a stranger can walk up to and question. The capstone is the AI Fair Booth — and the rule is that you answer every question without using the word "magic".*
