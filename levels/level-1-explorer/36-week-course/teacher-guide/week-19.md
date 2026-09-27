# Week 19 — The Test You Can't Study For

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Student Guide](../student-guide/week-19.md) · [Workbook](../workbook/week-19.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (comfortable in 65; the 60-minute cut is in §Differentiation) |
| **Type** | 🟦 teach — new idea, worked arithmetic, one unplugged activity |
| **Big idea** | Testing a model on the examples it trained on is cheating. You must hide examples **before** training and never let the model see them. |
| **New vocabulary** | training set · test set · hold out · split ratio |
| **Materials** | **30 index cards** · **1 sealable envelope** · a **pen** (not a pencil) · Handout 19A (split arithmetic) · Handout 19B (the four cheat cards, cut out) · a calendar or diary · a highlighter |
| **Tech needed** | **None.** This is the one week in Term 3 that needs no computer at all. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the envelope the student seals today does not get opened until **Week 22**. That is
> three weeks of it sitting somewhere. Decide *now* where it lives — taped inside the front cover of
> their notebook is the answer that has never gone wrong — and write the opening date on it in front
> of them.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can, observably:

1. **Split a set of examples into a training set and a test set at a stated ratio**, showing the
   multiplication and the check that the two parts add back to the total.
2. **Explain why the split has to happen before training and not after**, in their own words, without
   using the word "cheating" as the whole explanation.
3. **Spot four different ways of cheating on a split** and say, for each, what specifically leaked and
   which direction the reported score will be wrong in.
4. **Physically seal and sign a held-out test set**, and state who is allowed to open it and when.

---

## 🧑‍🏫 What YOU Need to Know First

*Read this once — about twelve minutes. Sections 1, 3 and 6 are the ones you cannot teach without.*

### 1. The one sentence the whole week rests on

**A score only means something if the thing being scored had never seen the questions.**

Everything else today — the card deal, the arithmetic, the envelope, the signature — is machinery for
making that sentence concrete enough that an 11-year-old cannot wriggle out of it.

Here is the situation it protects against. Your student trained a model in Week 17. It works. They
have shown it a spoon and it said "spoon". If you now ask *"how good is it?"* the natural thing to do
is show it some photos and count how many it gets right. And the natural photos to reach for are the
ones already sitting on the laptop — **the ones it trained on.**

That measurement will produce a lovely number. It will also measure nothing whatsoever.

### 2. The exam analogy, which is the whole lesson

Your teacher gives you 60 practice questions with the answers on the back. You work through them
until you can do every one. Then exam day arrives and the paper has **15 questions you have never
seen before.** Your mark on that paper tells everybody — including you — something real.

Now imagine a different teacher, who sets an exam made of the exact same 60 practice questions.
Everyone gets full marks. Everyone is delighted. And **not one person in the room knows whether
anybody learned any maths.** That exam measured nothing, and — this is the part that matters — it
*felt exactly like a successful exam.*

Testing a model on its training photos is that second exam. It always produces a good number, and it
always tells you nothing.

![The honest path and the cheat path](../figures/fig-w19-1-honest-path-vs-cheat-path.svg)
*Figure 19.1 — The same 30 photos, two orders of operations. Only the top row produces a number you
can believe.*

### 3. The four words, in plain language

> **Training set** — the examples the model is allowed to study.
>
> **Test set** — examples you hide *before* training, and look at once, at the very end, to find out
> how good the model really is.
>
> **Hold out** — to deliberately put examples aside before training. "I held out five photos per
> class."
>
> **Split ratio** — how you divided the examples, written as train / test. "80 / 20."

And one rule, which you should write on the board and point at repeatedly:

> **The golden rule — a test example is NEVER trained on. Not once. Not "just to top it up".**

### 4. The arithmetic, which is genuinely easy

With 30 examples and an 80 / 20 split:

```
   test  = 0.20 × 30 = 6
   train = 30 − 6     = 24
   check: 24 + 6 = 30  ✓
```

That check line is not padding. It is the habit that catches every mistake the student will make in
Week 22, and it costs four seconds.

**One refinement that matters more than the ratio: split each class separately.** If you shuffle all
75 photos together and grab 15, you can end up holding out 12 combs and 1 spoon. Then your "test set"
measures how good the model is at combs and barely mentions spoons. So:

```
   per class:  0.20 × 25 = 5 test,  25 − 5 = 20 train
   × 3 classes: 15 test, 60 train
   check: 15 + 60 = 75  ✓
```

### 5. Choosing the ratio — and being honest that there is no right answer

| Ratio | Train (of 75) | Test | Good because | Bad because |
|---|:--:|:--:|---|---|
| 90 / 10 | 67 | 8 | the model gets nearly all the data | 8 test photos is a shaky measurement — one photo is worth 12.5 points |
| **80 / 20** | **60** | **15** | **sensible middle; the usual default** | **nothing much. A good starting choice** |
| 70 / 30 | 52 | 23 | a much more trustworthy score | the model has fewer photos to learn from, so it is genuinely worse |
| 50 / 50 | 37 | 38 | a very reliable score | ...of a badly trained model. You measured the wrong thing very precisely |

The rule of thumb to teach: **80 / 20 unless you have a reason.** And the trade-off to say out loud,
because it is the honest heart of it: **every test photo is a training photo you gave up.** There is
no way round that with a fixed pile of photos — only ways to be clear about it.

### 6. The four cheats — and why number 4 is the one to spend time on

These are the four you will put in front of the student. All four report a score that is **too
high**. They are not equally obvious.

| # | The cheat | What leaks | Why it fools people |
|:--:|---|---|---|
| 1 | **Split after training** — train on all 30, then pick 6 and call them the test | The model already studied all six | It feels like a fair random pick, because the *picking* was random |
| 2 | **Same burst** — 30 frames from one 3-second video clip, 6 held out | Near-identical twins. Frame 14 and frame 17 differ by nothing | The folders really are separate, and it really was one shuffle |
| 3 | **Peek, then retrain** — open the envelope, see 4/6, add photos, retrain, get 6/6 | The *decision* about what to change came from the test set — it leaked through your brain | Each individual step looks harmless and helpful |
| 4 | **Same object in both** — the same blue bottle photographed for training *and* for testing | You are measuring "can it recognise **this** bottle", not "can it recognise bottles" | Different day, different room, different photos, separate folders. Everything looks right |

**Number 4 deserves the most discussion time, and here is the precise reason.** Cheats 1, 2 and 3 are
all fixable by being more careful with the same objects. Cheat 4 cannot be fixed by care at all — you
need *a different bottle*. The question the test set is supposed to answer is "will this work on a
bottle it has never met?" and a test set built from the same physical object can never answer it, no
matter how good your photography discipline is.

This is not a made-up school worry. It is exactly how a famous real failure worked: in 2020–21 dozens
of research teams built systems to spot COVID from chest X-rays and reported superb accuracy. When
other researchers checked, several of the models turned out to be keying on things like the position
of the patient or **text markers printed on the image by one particular hospital's machine** — because
the sick scans came from one hospital and the healthy ones from another. The models had learned *which
hospital*, not *which disease*. Every one of them had been tested. Just not on anything new.

### 7. The two misconceptions you will meet today

**Misconception 1 — "I'll just remember not to train on those."**
No. This is the big one, and it is not a character problem, it is a memory problem. Three weeks from
now the student will not remember which six photos were the test set, and the six will be sitting in
the same folder as the others looking identical. The envelope is not theatre; it is the only mechanism
that survives three weeks. **Sealing beats intending.**

**Misconception 2 — "20% is a rule, so 20% must be right."**
There is no correct ratio. 80/20 is a convention, and a good one, but a student who says "I chose
70/30 because I only have 12 photos per class and I wanted my score to mean something" has understood
this better than a student who says "80/20 because that's the rule." Reward the reason, not the
number.

### 8. Why the signature specifically

You could just put the photos in a drawer. The signature across the flap does something a drawer
cannot: **it makes reopening an event.** You cannot open it accidentally, you cannot open it and
un-know it, and you cannot open it and pretend you didn't. A drawer lets you have a quick look. A
signature does not.

This is a real technique, not a school game. Tamper-evident seals are used on ballot boxes, evidence
bags, and — genuinely — on the data used in some medical trials.

### 9. How deep to go, and where to stop

| Go this deep | Stop before |
|---|---|
| Training set, test set, hold out, split ratio | The word **validation set** — that is Level 2 |
| Split before training; split per class | Cross-validation, k-folds, stratified sampling by name |
| Four ways to cheat, and which direction the error goes | Any of the accuracy arithmetic — that is next week |
| "Every test photo is a training photo you gave up" | Learning curves, sample-size formulas |

> **⚠️ Watch out:** do not compute any accuracy today. The temptation is enormous, because a test set
> is obviously *for* scoring. But today is about the split and the seal — and Week 20 is entirely
> about the arithmetic. If you spend today on percentages you will arrive at Week 20 with nothing left
> to teach and a student who never physically sealed anything.

---

### 🧭 The Growing Map

The tinted box **moves** today, for the first time since Week 15. TRAINING turns plain white and gets its
finished label, `wk 15-18`, and **HONEST TESTING** lights up as the new box. Point at that move; it is
visible from across the room and it marks the start of Term 3.

![The course map in Week 19: honest testing is the new box, filled in by sealing examples away before training](../figures/fig-w19-0-where-this-fits.svg)

*Figure 19.0 — Week 19's version. TRAINING now white and finished, HONEST TESTING newly tinted and
badged, with **data** and **evaluation** lit along the bottom.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask:** *"which bit did we do today — and notice the shaded box has jumped. Why?"* The
   answer you want is that they did not train anything at all today; they **split the photos and sealed
   an envelope**. Splitting happens *before* training, so the new box had to open before the next model
   is ever built.
2. **Then the better question:** *"why is TRAINING white now, and why is it behind us?"* Because a model
   you cannot score is just a toy. Then ask the sharper one: *"we didn't work out a single percentage
   today — why not?"* Because the split is the thing that makes a percentage worth having, and Week 20
   is where the arithmetic lives.
3. **Have them copy the move onto their own map:** shade HONEST TESTING, write `wk 15-18` under TRAINING,
   and draw a small envelope with the seal date and the number of photos inside it. They will need both
   of those figures in Week 22.

> **🧑‍🏫 Why this is worth two minutes.** Today's idea is completely unglamorous — you put photos in an
> envelope — and it is the single most important habit in the whole level. Seeing the map's shaded box
> physically move because of an envelope is the strongest argument available that this counts as real
> work. It also quietly warns them that three more weeks sit inside this box, so they should not expect
> to be finished with testing by Friday.

**The six threads** along the bottom are the spine of all four levels. **Data** and **evaluation** are
lit this week. Do not quiz them on the threads; the map is orientation, never assessment.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Count out 30 index cards** and number them 1 to 30 in pen, one number per card. Yes, all
      thirty, and yes, by hand — it takes four minutes and the numbers are what make the deal
      checkable afterwards.
- [ ] **Find one sealable envelope.** A standard letter envelope is perfect. Check the flap actually
      sticks; a flap that won't stay down wrecks the moment.
- [ ] **Print Handout 19A** (the split arithmetic sheet — five problems, blank working space) and
      **Handout 19B** (the four cheat cards). Cut 19B into four separate cards before class. Loose
      cards are handled and re-read; a list on one page is skimmed once.
- [ ] **Read §6 above until you can say cheat 4 in your own words.** It is the one you will have to
      explain twice, and the difference between "the same bottle" and "a different bottle of the same
      kind" is the whole idea.
- [ ] **Open a calendar and pick the two photo days**, in ink, before the lesson. You need day 1 and
      day 2 to be genuinely different days — ideally with different weather or different light. If the
      only option is morning and evening of the same day, that is acceptable; say so honestly.
- [ ] **Decide where the envelope will live for three weeks.** Taped inside the front cover of the
      student's notebook is the answer.

### 5 minutes on the day

- [ ] 30 numbered cards, shuffled and face down in one stack
- [ ] The envelope, a pen, the highlighter
- [ ] Handout 19A on the table, the four 19B cards face down in a small pile
- [ ] Calendar open at the right page
- [ ] Board or big sheet, wiped clean, with room for six lines of arithmetic

### If something fails

| What fails | Fallback |
|---|---|
| **No index cards** | Tear a sheet of A4 into 30 rough rectangles and number them. Scruffy is fine — the point is that they are countable and shuffleable. |
| **No envelope** | Fold one sheet of paper around the six cards, tape it shut on all three open edges, and sign across every piece of tape. It works identically. |
| **You have no printer** | Handout 19A is five lines you can write on paper in two minutes (the five problems are in §Answer Key K1). Handout 19B is four sentences — write each on a card by hand, which is arguably better. |
| **The student has already lost their Week 17 photos** | Today does not need them. Today's homework starts a fresh collection anyway. Say so and move on; nothing is lost. |
| **No calendar, no diary** | Write the two dates on the envelope and on the top of Handout 19A. The envelope is the calendar. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0 – 8 | 🪝 **Hook** — the exam made of the practice questions | A fake test, marked, and the question it leaves |
| 8 – 26 | 🧠 **Concept** — hide some before you start | The four words, the golden rule, the arithmetic, per-class splitting |
| 26 – 40 | 🔍 **Worked Example** — three splits on paper, together | 30 cards, 75 photos, and one that doesn't divide neatly |
| 40 – 60 | 🎲 **Activity** — The Split, Unplugged · then the four cheats | Deal 24/6, seal, sign · then find the flaw in four splits |
| 60 – 70 | 🔑 **Wrap & Assign** — the timeline, the two dates, the homework | Two photo sessions booked into a real calendar |

---

### 🪝 Hook — 8 minutes

**Do this first, before you say anything about AI.** Write these three questions on the board and ask
the student to answer them on paper:

```
   1.  7 × 8 = ?
   2.  What is the capital of France?
   3.  Spell "rhythm".
```

Let them answer. Mark it out loud. Presumably 3 out of 3. Make a small fuss.

**Say this:**

> "Three out of three. Excellent. Now — how good are you at maths, geography and spelling?"
>
> *(Let them answer. Then:)*
>
> "Here's my problem. I wrote those three questions on the board, and I watched you look at them, and
> then I asked you those exact three questions. What if I'd asked you three questions you'd never
> seen? Would you still have got three out of three?"
>
> "Maybe! Probably, those were easy. But — and this is the whole lesson — **I cannot tell.** My test
> didn't measure whether you're good at maths. It measured whether you can read a board."
>
> *(Pause here. Then bring it round.)*
>
> "Now think about your model. Last term you trained it on about a hundred and twenty photos. Suppose
> I want to know how good it is, so I take some of those photos and show them to it and count how many
> it gets right. What have I just measured?"
>
> "You have a model that studied a hundred and twenty photos, and I tested it on... photos it studied.
> I have written the questions on the board and then asked those questions."
>
> "So today: how do you build a test that a machine **cannot** study for?"

**Ask this:**

> **1. "Was my three-question test fair?"**
> - *Hoping for:* no, because you'd already shown them the questions.
> - *If they say "yes, I did get them right":* agree completely — they *did* get them right, honestly.
>   "You definitely got 3 out of 3. My question is different: does my 3 out of 3 tell me how good you
>   are at spelling? What if the next word was 'onomatopoeia'?"
> - *If they're stuck:* "What would have made it a harder test?" Any answer that involves *new*
>   questions is the right one.

> **2. "How would you make it a real test?"**
> - *Hoping for:* ask questions I haven't seen / cover the board / use different questions.
> - Whatever they say, name it: "You just invented today's method. You said: hide some questions."
> - Write their own sentence on the board and leave it there for the whole lesson.

---

### 🧠 Concept — 18 minutes

**Say this (part 1 — the two piles):**

> "Here is what professionals do, and it takes five minutes and almost nobody does it the first
> time."
>
> "Before you train anything — before you touch the laptop — you take your pile of examples and you
> split it into two piles. The big pile is the **training set**. That is the pile the model is allowed
> to study. The small pile is the **test set**. Those are the examples you hide, and the model never,
> ever sees them until the very end."
>
> "The word for putting them aside is **hold out**. You say: 'I held out five photos per class.'"
>
> "And there is one rule, and it is the whole subject: **a test example is never trained on. Not once.
> Not 'just to top it up because I was short of photos.'** The moment a test photo gets trained on, it
> stops being a test photo — it becomes a question you already showed the machine."

**Say this (part 2 — the ratio and the arithmetic):**

> "How big should the two piles be? The usual answer is **80 / 20**. Eighty percent to study from,
> twenty percent hidden. That pair of numbers is called the **split ratio**."
>
> "Let's do it on thirty cards, which is what we've got on the table. Twenty percent of thirty."
>
> *(Do it on the board, out loud, slowly.)*
>
> "0.20 times 30 is 6. So six cards get hidden. And the training pile is 30 minus 6, which is 24. Then
> — always, every time, no exceptions — **check**: 24 plus 6 is 30. ✓ Good. Nothing lost, nothing
> invented."

**Say this (part 3 — split each class separately, and the honest trade-off):**

> "One extra thing that matters more than the ratio does. Imagine you've got 75 photos — 25 spoons, 25
> toothbrushes, 25 combs — and you shuffle the whole lot together and grab 15 for your test set. What
> could go wrong?"
>
> *(Wait. Let them find it.)*
>
> "You might grab 12 combs and 1 spoon. And then your test set is basically a comb test. So you split
> **each class separately**: 20 percent of 25 is 5, so 5 combs, 5 spoons, 5 toothbrushes hidden. Same
> total, much better spread."
>
> "And one last honest bit. Every photo you hide is a photo the model doesn't get to learn from. So
> hiding more photos gives you a **better measurement** of a **worse model**. That trade is real and
> there's no way round it. It's why 80/20 is popular — it's a compromise, not a law."

**Do this:**

Build the board as you talk, in this order, and leave every line of it up:

![Week 19 finished board](../figures/fig-w19-6-board-plan.svg)
*Figure 19.2 — What the board should look like at minute 26. You will point at the RULE line four more
times today.*

Then put up the picture of the deal itself, because the arithmetic and the piles need to be the same
thing in the student's head:

![An 80 20 split dealt as two unequal piles](../figures/fig-w19-2-deal-24-and-6.svg)
*Figure 19.3 — Shuffle first. An unshuffled deal can hand you six cards that are all the same class.*

**Ask this:**

> **1. "Why does the split have to happen BEFORE training, not after?"**
> - *Hoping for:* because if you train first, the model has already studied all of them, so there's
>   nothing left to hide.
> - *If they say "because that's the rule":* refuse it, kindly. "Suppose I train on all 30 cards, then
>   pick 6 and call them my test set. What's wrong with those 6?" Push until they say *it has already
>   seen them*.
> - *If they get it fast:* extension — "could I fix it by training again from scratch on just the 24?"
>   *(Yes — and that is exactly what the honest order is. Good spot.)*

> **2. "If I hide 6 out of 30, what's my split ratio?"**
> - *Hoping for:* 80/20, and ideally the working: 6 ÷ 30 = 0.2 = 20%.
> - *If they say "24 to 6":* accept it as true and then push for the percentage. "That's the counts.
>   What's that as a ratio out of a hundred?"
> - *If they can't do 6 ÷ 30:* do it together — 3 ÷ 30 would be a tenth, so 6 ÷ 30 is two tenths, so
>   20%.

> **3. "What could go wrong if I shuffle all 75 photos together and grab 15?"**
> - *Hoping for:* you might get too many of one class and none of another.
> - *If they say "nothing, it's random":* "Random is exactly the problem. Random doesn't mean even.
>   What's the worst possible 15 you could pull out?" *(All 15 combs.)*

> **4. "I'm short of training photos. Can I use one of the hidden ones — just one?"**
> - This is a trap question and you should ask it in a friendly, reasonable voice, as if it were a
>   sensible suggestion.
> - *Hoping for:* no, because then it isn't hidden any more.
> - *If they say yes:* do not correct. Just ask: "and then what does my score at the end measure?"
>   Let them get there.

---

### 🔍 Worked Example Together — 14 minutes

**Three splits on paper.** You hold the pen for the first, they hold it for the second and third.
Handout 19A has all three plus two more for homework.

**Split A — 30 cards, 80/20 (4 min).** You write, saying each line out loud.

```
   total = 30
   ratio = 80 / 20

   test  = 0.20 × 30 = 6
   train = 30 − 6     = 24

   check: 24 + 6 = 30  ✓
```

Then the sentence that turns it into a habit: *"Six hidden, twenty-four to study from, and the parts
add back to the whole."*

**Split B — 75 photos, 25 per class, 80/20, split per class (5 min).** They write. You only ask
questions.

```
   per class:  test  = 0.20 × 25 = 5
               train = 25 − 5     = 20

   × 3 classes: test  = 5 × 3  = 15
                train = 20 × 3 = 60

   check: 15 + 60 = 75  ✓
```

> **💡 Try this:** make them write the words *spoon / toothbrush / comb* next to the "5, 5, 5". Naming
> the classes stops per-class splitting from turning into a multiplication trick.

**Split C — the one that doesn't divide neatly (5 min).** This is the interesting one. Four classes,
with 50, 50, 50 and **18** photos.

```
   class 1:  0.20 × 50 = 10 test,  40 train
   class 2:  0.20 × 50 = 10 test,  40 train
   class 3:  0.20 × 50 = 10 test,  40 train
   class 4:  0.20 × 18 = 3.6  →  ???
```

Stop at the 3.6 and ask the question below. Then finish it:

```
   class 4:  round UP to 4 test,  18 − 4 = 14 train

   totals: test = 10 + 10 + 10 + 4 = 34
           train = 40 + 40 + 40 + 14 = 134
   check:  34 + 134 = 168  ✓
```

**Ask this:**

> **1. "You can't hide 3.6 photos. Up to 4, or down to 3?"**
> - *Hoping for:* **up to 4**, with a reason like "3 is too few to measure anything".
> - The full reason, which you should supply if they don't: with only 3 test photos in a class, one
>   photo is worth a third of that class's score. Getting one wrong drops it by 33 points. That is too
>   coarse to mean anything. The extra training photo you give up matters less than being able to
>   measure the class at all.
> - *If they say down to 3 "because 3.6 is nearer 4... I mean 3":* let them do the "what's one photo
>   worth?" sum out loud. 1 ÷ 3 = 33%. 1 ÷ 4 = 25%. That usually settles it.

> **2. "Something else is wrong with class 4. What?"**
> - *Hoping for:* it has 18 photos and the others have 50 — it is unbalanced. (Week 16.)
> - Confirm and be precise: the *split* arithmetic here is correct; it is the *collection* that needs
>   fixing. Two different problems, and it is worth separating them out loud.

> **3. "Give me the check line for Split B without looking."**
> - *Hoping for:* 15 + 60 = 75.
> - If they can produce the check unprompted, that habit is now in place, and it is the single most
>   useful thing they take from today into Week 22.

---

### 🎲 Activity — 20 minutes

**Part 1: The Split, Unplugged (8 min).** Shuffle, deal 24 and 6, seal, sign.
**Part 2: The Four Cheats (12 min).** Four cards, find the flaw in each.

Full instructions in the next section.

---

### 🔑 Wrap & Assign — 10 minutes

**Do this:** put up the timeline and walk it left to right with your finger, naming each step.

![Timeline from collect to score with the seal step highlighted](../figures/fig-w19-5-seal-timeline.svg)
*Figure 19.4 — Move the seal to after step 4 and the whole timeline stops measuring anything.*

**Say this:**

> "Six steps. Collect, split, seal, train, open, score. The order is the entire lesson. Steps four,
> five and six are only honest **because step three actually happened.**"
>
> "Now — your model already exists, from Week 17. So your homework is to build the test set it never
> had. And you're going to do it in the world, not in a folder, because that's the only way to make
> sure the test photos are genuinely new."

**Do this:** open the calendar. Write in two dates, in ink, in front of them.

```
   SESSION 1  —  ____________   20 photos per class   →  folder: TRAIN
   SESSION 2  —  ____________    5 photos per class   →  the ENVELOPE
```

**Say this:**

> "Two different days. Not two hours apart — two days. Different light, different room if you can,
> different surface underneath. Session one is the training half. Session two is the test half, and it
> goes in the envelope and gets signed, exactly like the cards did today."
>
> "And the envelope does not get opened until Week 22. Not by you, not by me, not to check it worked.
> If either of us opens it, we have to write that down and admit it, and the number we get at the end
> will be worth less. That's not me being strict — that is literally the rule that stops everyone in
> this field from fooling themselves."

**Ask this:**

> **1. "Who is allowed to open this envelope, and when?"**
> - *Hoping for:* nobody, until Week 22.
> - *If they say "you can, if you're careful":* "There's no careful. Once I've seen them, I can't
>   un-see them. What would I have to write on your report?"

> **2. "Why two different days? Why not just take all 25 in one go and put 5 aside?"**
> - *Hoping for:* because photos from the same session are near-twins — that's cheat number 2.
> - If they name cheat 2 by number, that is a full-marks answer at minute 68.

Finally, write the opening date on the envelope in big numbers and tape it inside the notebook cover
while they watch.

---

## 🎲 The Activity, In Full

### Part 1 — The Split, Unplugged

**Time:** 8 minutes · **Materials:** 30 numbered index cards · 1 envelope · a pen

**Setup:** the 30 cards in one stack, face down. Envelope and pen beside them. Nothing else on the
table.

**Steps:**

1. **Shuffle properly.** Not two flicks — spread them face down, swirl them around with both hands
   for a good ten seconds, gather them up. Say why: *"if these were photos in the order you took them,
   the first six would all be from the same minute."*
2. **Deal 24 into the left pile**, face down, counting out loud. This is the **training set**.
3. **Deal the remaining 6 into the right pile**, face down, counting out loud. This is the **test
   set**. Do not turn them over. Nobody looks at the numbers.
4. **Check the arithmetic on the table**, not just on paper: 24 + 6 = 30, and 6 ÷ 30 = 0.2 = 20%.
5. **Put the 6 straight into the envelope.** Seal it.
6. **The student signs across the flap** — the signature must cross from the flap onto the envelope
   body, so it breaks if it is opened.
7. **Write the date and `TEST SET — DO NOT OPEN` on the front.**

![A signed and sealed test envelope](../figures/fig-w19-3-signed-sealed-envelope.svg)
*Figure 19.5 — The signature has to cross the flap. That is the only part that does any work.*

**Say this, at step 6, while they are signing:**

> "Sign it so the line runs across the flap and onto the envelope. Here's why that specific thing
> matters. If I put these six cards in a drawer, I could have a quick look and put them back and
> nobody would ever know — including me, ten minutes later. With your name written across the flap, I
> **cannot** open it without it being obvious. It stops being a decision I could make quietly and
> becomes an event."
>
> "This is not a school game. Ballot boxes and evidence bags get sealed the same way, and for the same
> reason."

**Then the deliberate mistake, if you have 90 seconds spare.** Take the 24-card pile, put it back in
order 1 to 30 in your hand, and deal the "first six" without shuffling. You get cards 1, 2, 3, 4, 5,
6. Ask: *"if these thirty were photos taken in order, what would those six have in common?"* Answer:
they were all taken in the same minute, in the same place, with the same light. Shuffling is not a
ritual — it is what stops the test set from being one narrow slice.

### Part 2 — The Four Cheats

**Time:** 12 minutes · **Materials:** the four Handout 19B cards, face down

**How it runs:** turn over one card at a time. The student reads it out loud. Then they have to say
**three things**:

```
   1.  WHAT LEAKED?          what did the model effectively already see?
   2.  WHICH DIRECTION?      will the reported score be too high or too low?
   3.  WHAT'S THE FIX?       one sentence, something you could actually do
```

All four are "too high". Do not tell them that in advance — let them work out that it is always the
same direction, because that realisation is worth having.

![Four cheating splits](../figures/fig-w19-4-four-cheating-splits.svg)
*Figure 19.6 — All four report a score that is too high. Number 4 is the sneakiest, because the
folders really are separate.*

**Card 1 — Split AFTER training.**
> *"I trained my model on all 30 photos. Then I picked 6 of them at random and used them as my test
> set. I got 6 out of 6."*

Timing: 2 minutes. This one is usually spotted immediately, and it is a good confidence builder. The
answer: all six were already studied. Fix: split first, then train on the 24 only.

**Card 2 — Same burst of photos.**
> *"I took a 3-second video of each object and pulled 30 frames out of it. I shuffled the frames
> properly and held out 6. I got 6 out of 6."*

Timing: 3 minutes. Harder. The student will often defend it, because the shuffle *was* fair. The point
to draw out: frame 14 and frame 17 are a twentieth of a second apart — same angle, same shadow, same
smudge on the spoon. They are the same photo wearing different names. Fix: split by *session*, not by
frame. Shoot two clips in two places and use one entirely for testing.

**Card 3 — Peek, then retrain.**
> *"I opened my envelope, scored 4 out of 6, saw it was bad at combs, took 20 more comb photos,
> retrained, tested again and got 6 out of 6. I'm reporting 6 out of 6."*

Timing: 3 minutes. The subtle bit: nothing was uploaded that shouldn't have been. The leak went
through the *person*. Every change was chosen **because of** what the test set said, so the test set
helped train the model — via the student's brain. Fix: the honest report is "4 out of 6 on the first
attempt; then I changed things and I no longer have a hidden test set." A fresh envelope, sealed
before the changes, is the real fix.

**Card 4 — Same object in both.  ⭐ *spend the most time here***
> *"For training I took 24 photos of my blue water bottle. For testing I took 6 more photos of my blue
> water bottle — different day, different room, different light, and I kept them in a separate sealed
> folder. I got 6 out of 6."*

Timing: 4 minutes, and let it run over if it is going well.

**How to run it.** Read the card. Then say, genuinely and without a hint of a trap in your voice:
*"This one looks fine to me. Different day, different room, sealed folder. Everything we said. Is it
fine?"*

Sit with the silence. Then, whichever way they answer, ask this:

> **"What question is the test set supposed to answer?"**

Push until you get something like *"will it work on a bottle it has never seen?"* Then:

> **"And can six photos of the same bottle answer that?"**

The answer lands hard: no. Never. Not with any amount of care. You have measured "does it recognise
**this** bottle", which is a real question but a much smaller one than the one you were claiming to
answer.

**Then the extension that makes it concrete:**

> **"How would you fix it? And you're not allowed to say 'take better photos'."**
> - *Hoping for:* borrow a different bottle. Use somebody else's. Test on three bottles you've never
>   photographed.
> - *If they say "take the test photos further away":* honest and wrong, and worth naming: "That
>   changes the *photo*. The problem is the *bottle*."

**Why this one is worth the most time:** cheats 1, 2 and 3 are cured by discipline. Cheat 4 is cured
only by *getting hold of a different object* — and that is a real cost, which is exactly why people
skip it and why it keeps happening in professional work.

### What "finished" looks like

- [ ] Six cards sealed in an envelope, signature crossing the flap, date written on the front
- [ ] The split arithmetic written down twice: on Handout 19A and out loud at the table
- [ ] Four cheat cards, each with a leak named, a direction (all "too high"), and a fix
- [ ] The student noticing, unprompted, that all four are wrong in the same direction
- [ ] Two dates in the calendar for the photo sessions

### Variation — easier

Use **20 cards instead of 30** (0.20 × 20 = 4 test, 16 train — much easier arithmetic, same idea).
Run cheats **1 and 4 only** — 1 to build confidence, 4 because it is the lesson. Skip the
unshuffled-deal demonstration. You write on Handout 19A while they talk.

### Variation — harder

1. **The 12-photo problem.** "You have 12 photos per class. 0.20 × 12 = 2.4. What do you do, and what
   is your *real* split ratio once you've rounded?" *(Round up to 3, so the real ratio is 3/12 = 25%
   — write 75/25, not 80/20. Honesty about the label is the point.)*
2. **Invent a fifth cheat** that isn't on the cards, and say what leaks. Real ones students have
   found: *the test photos are all of my left hand and so are the training ones*; *I asked my brother
   to take the test photos but he used my phone in my kitchen*; *my test photos are of the same three
   objects but I'd already shown the model those objects last term*.
3. **The impossible case.** "A doctor has 12 recorded cases of a rare illness. Hiding 20% means hiding
   2. A test of 2 measures nothing. What should they do?" There is no clean answer, and that is the
   answer: reuse the examples cleverly, or report a very wide range of uncertainty, or refuse to
   deploy. The wrong move is to build it and let people assume.

---

## ❓ Questions Students Ask This Week

**1. "Why can't I just remember which photos not to train on?"**
Because in three weeks you won't. They'll be sitting in the same folder as all the others, looking
exactly like them. This isn't about being trustworthy — it's about being human. The envelope survives
three weeks; your memory of six photo filenames does not. Sealing beats intending, every time.

**2. "What if my test set is really easy by accident?"**
It might be, and that's a real problem — it's why you shuffle before you split, and why you split each
class separately. But it's also why you write the *fraction* down and not just the percentage. "6 out
of 6" tells the reader there were only six, and any honest reader will then know not to be too
impressed.

**3. "Can I test it twice?"**
Once, properly. Every time you look at the test set and then change something, you've used it to make
a decision, which means it helped train the model — just through you instead of through the upload
button. If you want to test again after changing things, you need a *new* set of photos, sealed before
the changes.

**4. "What's the right split ratio?"**
**Nobody knows for sure, and here's why.** It depends on how many examples you have, how varied they
are, how similar your classes look, and what you plan to do with the number. There is no formula
anybody can give you — 80/20 is a *convention* that works reasonably well most of the time, not a law
of nature. What you *can* do is state your ratio and your reason, so a reader can judge for
themselves. "70/30 because I only had 12 per class and I wanted my score to mean something" is a
better answer than "80/20 because that's the rule."

**5. "If the hidden photos would make the model better, isn't hiding them a waste?"**
That's a genuinely good objection and the answer is: yes, it costs you something real. Every test
photo is a training photo you gave up, so your model is slightly worse than it could have been.
You're paying that price to buy something you can't get any other way — knowing how good it actually
is. A slightly worse model you understand beats a slightly better model you're guessing about.

**6. "The COVID X-ray thing — were the doctors cheating?"**
Almost certainly not. Nobody set out to build a hospital-detector. They collected the data they could
get, which came from different hospitals for sick and healthy patients, and they tested carefully — on
data with the same flaw. That's what makes this worth learning: it's not a story about dishonest
people, it's a story about a mistake you can make while trying hard and being careful.

**7. "Could I just take a photo of my photo, and use that as a test photo?"**
Lovely, sneaky idea, and no. A photo of a photo of your bottle is still *that* bottle, that angle,
that shadow. It's cheat 4 with an extra step. It would look like a new file and behave like an old
one.

**8. "What if I open the envelope by accident?"**
Then you write it down. Honestly, on the sheet, in the words "the envelope was opened early". Nobody
will be cross with you. What matters is that the person reading your result knows how much to trust
it. Hiding it would be the actual problem, and it would only ever fool one person: you.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The student turns over the six test cards "just to see"** | They are cards. Cards get looked at. | Let it happen once and use it: "Those six are spoiled now — we can't un-see them. Deal six new ones." Dealing again from a re-shuffled deck takes 30 seconds and makes the rule real in a way no explanation does. |
| **The lesson slides into computing accuracy** | A test set is obviously *for* scoring, and 6 out of 6 is right there. | Stop and say: "That's next week's whole lesson and I'm not spending it today." Today ends at *sealed*, not at *scored*. Write "how many did it get right?" on the board and leave it unanswered on purpose. |
| **Cheat 2 gets defended, hard** | The shuffle genuinely was fair, so the student is right about the thing they're defending. | Agree with the bit they're right about first: "your shuffle was perfect." Then move the argument to the photos: "How different is frame 14 from frame 17?" Hold up two fingers a centimetre apart. |
| **Cheat 4 gets waved through as fine** | Every visible rule was followed. It looks like the model answer. | Do not correct. Ask the two questions in order: *"what question is the test set supposed to answer?"* then *"can six photos of the same bottle answer it?"* They will get there themselves, and it sticks better. |
| **The signature is a tiny squiggle in one corner** | Signing is a formality, so it gets done like a formality. | Make them redo it, warmly. "It has to cross the flap. If I can open this without breaking your name, it isn't sealed." Ten seconds, and the point is the whole activity. |
| **"20%" becomes a magic number** | It was on the board all lesson. | Ask the harder version: "You've got 12 photos per class. 20% is 2.4. Now what?" Any student who can talk sensibly about rounding up and relabelling the ratio has understood that the number was a choice. |
| **The two photo sessions collapse into one afternoon** | Two days is inconvenient, and the student is keen to finish. | Hold the line, but negotiate the *gap*, not the *number of sessions*: morning and evening of the same day is a weak-but-honest fallback. Then make them write "same day, 8 hours apart" in the log — labelling the weakness is the skill. |
| **The envelope goes in a school bag and vanishes** | It is a loose piece of paper in the life of an 11-year-old. | Tape it inside the front cover of the notebook before they leave the table. Do not defer this. Week 22 does not work without it. |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** Split C (the 3.6 rounding problem); cheats 2 and 3; the unshuffled-deal demonstration.

**Reteach with the exam analogy, physically.** Write five spelling words on paper. Let them study it
for thirty seconds. Then test them on those exact five — full marks. Then test them on five *different*
words. The gap between the two scores is the entire lesson, in ninety seconds, with no arithmetic.

**Use 20 cards, not 30.** 0.20 × 20 = 4 and 20 − 4 = 16. The idea is identical and the sums stop being
in the way.

**The 60-minute version:** Hook 6 · Concept 15 · Worked example 10 (Splits A and B only) · Activity 19
(the deal, plus cheats 1 and 4) · Wrap 10. Do not cut the wrap — the two dates in the calendar are
what makes the homework happen.

**Keep, whatever else goes:** the deal, the signature, cheat 4, and the two dates.

### If they are flying

1. **The 12-photo problem** (§Variation — harder, item 1). The interesting part is not the rounding,
   it is realising you must relabel the ratio as 75/25 and say so.
2. **Invent a fifth cheat and try to fool you with it.** Give them two minutes to write one that
   *looks* completely legitimate. Genuinely try to be fooled. If they manage it, say so loudly.
3. **The whose-photos question.** "Your test photos are your hands, your kitchen, your light. Your
   model will be used by other people in other kitchens. Is your test set honest?" *(Partly. It
   predicts your house well and other houses poorly.)* This is Week 31 and Week 33 arriving early —
   don't resolve it, just let them sit with it.
4. **Design the split for a task with time in it.** "You're predicting which pupils need extra maths
   help next year, and you have three years of data. How do you split?" *(By year: train on the older
   years, test on the most recent one, because that mimics how it will actually be used.)*

### If they won't engage today

**Plan A — make it a game with a prize.** You are the cheat-designer; they are the inspector. You read
out four splits (three cheating, one honest — invent a clean one) and they have to catch the cheats.
Score it. Being the one who catches the adult out is powerful fuel.

**Plan B — just do the envelope.** Deal, seal, sign, date, tape it in. Four minutes. That single act
carries the whole week and makes Week 22 possible. Everything else can be reteaching at the start of
Week 20.

**Plan C — the deliberate disaster.** Announce that you are going to test your own "model" (you) on
the three board questions again, and predict loudly that you'll get 3 out of 3 and that this proves
you are excellent at geography. Then ask them to design a test you can't cheat on. Hand them the pen.
Let them catch you.

---

## ✅ Assessing Understanding

### Check 1 — the order of operations

> **"I've got 50 photos. Tell me the order I do things in, from photos to score."**

- **Good:** split, seal, train, then open and score. Bonus for "and the split happens before training".
- **Partial:** "train it then test it" — right words, wrong order. Ask: "when does the hiding happen?"
- **Not good enough:** "you test it at the end." Reteach with the six-step timeline (Figure 19.4),
  pointing at each circle. Sixty seconds.

### Check 2 — the arithmetic, cold

> **"40 photos, 80/20 split. How many hidden, how many to study from, and prove it adds up."**

- **Good:** 0.20 × 40 = 8 hidden, 40 − 8 = 32, check 32 + 8 = 40.
- **Partial:** gets 8 and 32 but doesn't produce the check without being asked. Ask for it. If it
  comes, that's fine — the habit is new.
- **Not good enough:** can't get 8. Do it as "a fifth of 40" and then move on; the concept matters
  more than the multiplication today, and Week 20 drills the arithmetic properly.

### Check 3 — the sneaky one

> **"I trained on 24 photos of my blue bottle and tested on 6 more photos of the same blue bottle,
> taken a week later in a different room. Is that a fair test?"**

- **Good:** no — it only tells you about *that* bottle. Full marks if they say what it *does* measure,
  not just that it's wrong.
- **Partial:** "no, because it's the same object" — correct but thin. Ask: "so what would a fair test
  need?" You want *a different bottle*.
- **Not good enough:** "yes, it's a different day." Re-run the two questions from cheat 4 and let them
  get there. Note it and re-ask it as the Week 20 warm-up.

### Mastery scale for this week

| Level | What it looks like |
|:--:|---|
| **1** | Deals the cards when told. Cannot say why six are being hidden. |
| **2** | Does the split arithmetic with help. Says "you shouldn't test on training photos" but can't say what goes wrong if you do. |
| **3** | Splits at a stated ratio with the check line, unprompted. Explains that the split must come first because otherwise the model has already studied everything. Spots cheats 1 and 2. |
| **4** | All of the above, plus spots cheat 3 (the peek) and can say the leak went through the person. States a ratio *with a reason*. Seals and signs without being reminded why. |
| **5** | Spots cheat 4 unaided and can say what the test set was supposed to answer and why the same object can't answer it. Handles the 2.4-photo rounding case and relabels the ratio honestly. Invents a fifth cheat that genuinely fools you. |

**Aim for 3.** Level 4 is a strong outcome for the first week of Term 3.

---

## 📤 Homework to Assign

**Workbook:** Week 19, pages 1–3. **Time: about 55 minutes**, plus the two photo sessions (about 15
minutes each, on two different days).

**Say this, word for word:**

> "Three things, and the third one is the real one."
>
> "First: page 1, five splitting problems. Show the multiplication and show the check every time. If
> the answer isn't a whole number, tell me which way you rounded **and why** — that's the bit I'm
> marking, not the number."
>
> "Second: page 2. Write up the four cheats — what leaked, too high or too low, and the fix in one
> sentence. Then invent a fifth one of your own and try to make it sound completely reasonable."
>
> "Third, and this is the one that actually matters: **photos, on two different days.** Session one,
> on ______: twenty photos of each of your three objects. That's the training half — put it in a
> folder called TRAIN. Session two, on ______: five photos of each. Different room if you can,
> different light, different surface underneath. Those fifteen photos go in the envelope, you sign
> across the flap, you write the date on it, and it does not get opened until Week 22."
>
> "Session two does not touch the laptop. Not to look at, not to check, not 'just to see if they came
> out okay'. If you want to check a photo came out okay, do that during session two while you're
> taking them."

**Check before they leave:** ask them to say the two dates out loud, and point at where the envelope
is taped.

| Page | Task | Approx. time |
|---|---|---|
| 1 | Five splitting problems, multiplication + check shown | 20 min |
| 2 | The four cheats written up, plus a fifth of your own | 20 min |
| 3 | The photo plan and the envelope log: two dates, counts, ticked change-list, signature | 15 min |

> **🧑‍🏫 If a student asks** whether they can put the Session 1 photos into Teachable Machine and
> retrain their Week 17 model: yes, that is allowed and it is a good instinct. Two conditions. They
> must write down the new training accuracy from **Advanced → Under the hood**, because Week 22 needs
> it. And Session 2 must not go anywhere near the training panel. If they would rather leave the Week
> 17 model exactly as it is, that is equally fine — Week 22 works either way.

**If there is no printer for the photos:** the envelope can hold a signed index card instead of prints.
On the card: the date, the count (15), the three class names with 5 each, and the *filenames*. Then
move the fifteen files into a folder called `DO_NOT_TRAIN` and do not open it. The prints are nicer;
the commitment is what does the work.

---

## 🔑 Answer Key

### K1 — Workbook page 1: the five splitting problems

**(a) 3 classes, 30 photos each (90 total), 80/20.**
```
   per class:  test  = 0.20 × 30 = 6
               train = 30 − 6     = 24
   totals:     test  = 6 × 3  = 18
               train = 24 × 3 = 72
   check:      18 + 72 = 90  ✓
```
No rounding needed.

**(b) 3 classes, 25 photos each (75 total), 80/20.**
```
   per class:  test  = 0.20 × 25 = 5
               train = 25 − 5     = 20
   totals:     test = 15,  train = 60
   check:      15 + 60 = 75  ✓
```

**(c) 4 classes with 50, 50, 50 and 18 photos (168 total), 80/20.**
```
   class 1:  0.20 × 50 = 10 test,  40 train
   class 2:  0.20 × 50 = 10 test,  40 train
   class 3:  0.20 × 50 = 10 test,  40 train
   class 4:  0.20 × 18 = 3.6  →  round UP to 4 test,  14 train

   totals:   test = 10 + 10 + 10 + 4 = 34
             train = 40 + 40 + 40 + 14 = 134
   check:    34 + 134 = 168  ✓
```
**Rounding note (this is the marked part):** round 3.6 **up** to 4, not down to 3. With only 3 test
photos in a class, one photo is worth a third of that class's score — too coarse to mean anything. The
one training photo you give up matters less than being able to measure the class at all.

**Also worth flagging:** class 4 has 18 photos against the others' 50. That is a class-imbalance
problem (Week 16) and it will hurt this model however the split is done. The split arithmetic is
right; the *collection* needs fixing.

**(d) 2 classes, 200 photos each (400 total).**
```
   80/20:  per class  test = 0.20 × 200 = 40,  train = 160
           totals     test = 80,  train = 320
   check:  80 + 320 = 400  ✓
```
**Would you use 80/20 here?** A good answer argues either way and gives a reason. The strongest
version: with 400 photos, 90/10 is also fine — 20 test per class, 40 in total, so one photo is worth
2.5 points, which is plenty precise, and the 40 extra training photos per class are worth more. But if
you intend to *compare several models*, keep 80/20, because 80 test photos separates a 90% model from
an 87% model far more reliably than 40 does. **The right ratio depends on the question, not on a
rule.**

**(e) 3 classes, 12 photos each (36 total), 80/20.**
```
   per class:  0.20 × 12 = 2.4  →  round UP to 3 test,  9 train
   totals:     test = 9,  train = 27
   check:      9 + 27 = 36  ✓
```
**The honest part:** 3 out of 12 is not 20% — it is 3 ÷ 12 = 0.25 = **25%**. So the real ratio is
**75 / 25** and that is what you should write in your notes. Do not label it 80/20 because that is
what you set out to do. A student who spots this gets full marks even if the rest is shaky.

**Bonus, if they attempted it:** with 3 test photos per class, one photo is worth 1 ÷ 3 = 33 points of
that class's score. That is a warning label, not a disaster — you just have to say it when you report
the number.

### K2 — Workbook page 2: the four cheats

Every one of the four reports a score that is **too high**. If the student noticed that pattern
themselves, say so out loud — it is the most valuable single observation of the week.

**Cheat 1 — split after training.**
- *What leaked:* everything. The model studied all 30, so all 6 "test" photos are ones it has already
  seen. There is no hidden set at all; there is a hidden *label*.
- *Direction:* far too high. Expect something near 100%.
- *Fix:* split first, then train on the 24 only. If you have already trained, you must start again
  from scratch — you cannot un-train a photo.

**Cheat 2 — same burst of photos.**
- *What leaked:* near-duplicates. Frames a twentieth of a second apart share the angle, the shadow,
  the background and the smudge on the object. Each held-out frame has an almost-identical twin in the
  training pile, so the model has effectively seen it.
- *Direction:* far too high — often 95–100% for a model that fails on any genuinely new photo.
- *Fix:* split by **session**, not by frame. Shoot two clips, in two places, on two days, and use one
  entirely for testing. Random splitting only works when the examples are genuinely independent of
  each other, and video frames are not.

**Cheat 3 — peek, then retrain.**
- *What leaked:* the *decision*. Nothing was uploaded that shouldn't have been, but the choice of what
  to change was made by looking at the test set — so the test set trained the model, through the
  person. Reporting 6/6 means reporting the best of two attempts at the same exam.
- *Direction:* too high, and it gets worse with every extra round. Ten rounds of "tweak until the
  score goes up" can inflate a number enormously.
- *Fix:* collect a fresh set of photos, sealed before any changes, and report the score on that. At
  minimum, report it honestly as what it is: *"4 out of 6 on the first attempt; 6 out of 6 on the
  second, after adding photos because of the first result."*

**Cheat 4 — the same object in both.**
- *What leaked:* the object itself. The test set answers "does it recognise **this** blue bottle",
  which is not the question anybody was asking. It cannot answer "does it recognise bottles" because a
  bottle it has never met never appears anywhere in the experiment.
- *Direction:* too high — and unfixable by care, which is what makes it the sneakiest. Every visible
  rule was obeyed: different day, different room, sealed folder.
- *Fix:* get a **different bottle**. Borrow one, use a sibling's, use three you have never
  photographed. If you genuinely only own one bottle, then say so in your report: *"tested on new
  photos of the same object, so this number does not tell you how it behaves on a bottle it has never
  seen."*

**The thread through all four, and the sentence to look for on page 2:** a test set is only honest if
it differs from the training set **in the same ways the real world will differ.** Frames, sessions,
tweaking rounds and single objects are four different ways that quietly fails.

**The invented fifth cheat.** There is no single right answer. Full credit needs three things: a
scenario that sounds plausible, a named leak, and a fix. Strong examples students actually produce:

- *"My friend took the test photos — on my phone, in my kitchen, on my table."* Leak: everything
  except the hands. Fix: change the room and the light too, and report exactly which one thing was
  tested.
- *"The test photos are of the same three objects, but I'd already trained on those objects last
  term."* Leak: the objects. This is cheat 4 wearing a hat.
- *"I took a photo of my training photo."* Leak: the photo. Same object, same angle, same shadow, one
  extra step.
- *"I held out 6 photos but they were all of the class I knew it was good at."* Leak: the choice of
  which to hide. Fix: shuffle, and split each class separately.

### K3 — Workbook page 3: the photo plan and the envelope log

Model answer:

```
   SESSION 1  —  Saturday 14th, 3pm, kitchen table, afternoon daylight
                 spoon 20 · toothbrush 20 · comb 20      total 60   → folder TRAIN

   SESSION 2  —  Monday 16th, 7pm, bedroom desk, lamp only
                 spoon 5 · toothbrush 5 · comb 5         total 15   → ENVELOPE

   What I changed for session 2:
     ☑ different room      ☑ different light     ☑ different surface
     ☑ different day       ☑ different hand      ☐ different distance (forgot)

   split ratio: 60 / 15  →  15 ÷ 75 = 0.20 = 20%   →  80 / 20   ✓
   check: 60 + 15 = 75  ✓

   Sealed and signed: Monday 16th.   Do not open until Week 22.
```

**Two written sentences, model answers:**

> **Why must the split happen before training and not after?**
> Because after training the model has already studied every photo, so there is nothing left that
> counts as hidden. Picking six of them afterwards and calling them a test set only changes what I
> call them — it does not change what the model has seen.

> **What would you say to somebody who asked to open the envelope early?**
> No, because once we've seen them we can't un-see them, and then any change we make would be a change
> we chose using the answers. If it does get opened I have to write that on my results, so the person
> reading them knows how much to trust the number.

**Marking note:** accept any answer that gets *"it has already seen them"* into the first one. Refuse
"because that's cheating" as a complete answer — push for what specifically goes wrong.

### K4 — Every question posed in the lesson

| Segment | Question | Answer |
|---|---|---|
| Hook | Was my three-question test fair? | No — the questions were on the board. It measured reading, not knowing. |
| Hook | How would you make it a real test? | Ask questions they haven't seen. Hide some questions. (This is the lesson.) |
| Concept | Why must the split happen before training? | Because after training the model has studied everything, so nothing is hidden any more. |
| Concept | Hide 6 of 30 — what's the split ratio? | 6 ÷ 30 = 0.2 = 20%, so 80 / 20. |
| Concept | What goes wrong shuffling all 75 and grabbing 15? | You can get 12 combs and 1 spoon. The test set becomes a comb test. Split each class separately. |
| Concept | Can I use one hidden photo for training, just one? | No. Then it isn't hidden, and your final score stops measuring anything new. |
| Worked ex. | 3.6 photos — round up or down? | Up, to 4. With 3, one photo is worth 33 points of that class's score — too coarse. |
| Worked ex. | What else is wrong with class 4? | It has 18 photos against 50 — a class imbalance. Different problem from the split; fix the collection. |
| Worked ex. | Give me the check line for Split B. | 15 + 60 = 75. |
| Activity | Cheat 1 — what leaked? | All six were already studied. Too high. Fix: split first, retrain from scratch. |
| Activity | Cheat 2 — how different is frame 14 from frame 17? | Almost identical — same angle, shadow, background. Near-twins count as already seen. |
| Activity | Cheat 3 — nothing was uploaded, so what leaked? | The decision. The test set trained the model through the person. |
| Activity | Cheat 4 — what question is the test set for? | "Will it work on a bottle it has never seen?" Six photos of the same bottle cannot answer that. |
| Activity | Cheat 4 — how would you fix it, without "take better photos"? | Get a different bottle. Borrow one. Test on objects never photographed. |
| Activity | Which direction are all four wrong in? | Too high. Every one of them. |
| Wrap | Who may open the envelope, and when? | Nobody, until Week 22. If it is opened early, that gets written down. |
| Wrap | Why two different days? | Photos from one session are near-twins — that is cheat 2. Two days buys real difference. |

### K5 — The 20-card version (for the easier variation)

```
   test  = 0.20 × 20 = 4
   train = 20 − 4     = 16
   check: 16 + 4 = 20  ✓
```

### K6 — Handout 19B, the four cheat cards (text to copy if you are writing them by hand)

1. *"I trained my model on all 30 photos. Then I picked 6 of them at random and used them as my test
   set. I got 6 out of 6."*
2. *"I took a 3-second video of each object and pulled 30 frames out of it. I shuffled the frames
   properly and held out 6. I got 6 out of 6."*
3. *"I opened my envelope, scored 4 out of 6, saw it was bad at combs, took 20 more comb photos,
   retrained, tested again and got 6 out of 6. I'm reporting 6 out of 6."*
4. *"For training I took 24 photos of my blue water bottle. For testing I took 6 more photos of my
   blue water bottle — different day, different room, different light, and I kept them in a separate
   sealed folder. I got 6 out of 6."*

---

## 🔮 Next Week Preview

Next week is **Week 20 — Accuracy, Three Ways — and the Number That Lies**, and it is marked as the
single most important lesson in the course. The student finally gets to score something: a completed
fifteen-row test sheet, by hand, one row at a time, with the long division written out. It comes to
11/15, then 0.7333, then 73.3%. Then the sheet gets split up by class and the discovery arrives — 100%,
80% and **40%**. One number was hiding a class that barely beats a coin toss. No computer needed again.

**Prep early:**

- **Print the fifteen-row scoring sheet** (Workbook page W20.1) or rule it by hand. You need it filled
  in already, with the results in the Week 20 answer key — the student's job is to *score* it, not to
  collect it.
- **A coloured pen or highlighter** for splitting the sheet by class. It is on the Week 0 list for
  weeks 5, 20, 21 and 25.
- **No calculator on the table.** The whole point of Week 20 is that the division gets written down.
  Put the calculator in a drawer before the student arrives; it can come out at the very end to check.
- **Check the envelope is still sealed and still taped in.** Ten seconds, every week, until Week 22.

---

[⬅ Week 18](week-18.md) · [Course Home](../README.md) · [Week 20 ➡](week-20.md) · [Student Guide](../student-guide/week-19.md) · [Workbook](../workbook/week-19.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
