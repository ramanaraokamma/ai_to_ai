# Week 34 — The AI Fair Booth, Part 1: Build It and Test It Honestly

[⬅ Week 33](week-33.md) · [Course Home](../README.md) · [Week 35 ➡](week-35.md) · [Student Guide](../student-guide/week-34.md) · [Workbook](../workbook/week-34.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (60 minimum, 75 if the scoring runs long) |
| **Type** | 🎪 Capstone — build session, part 1 of 2 |
| **Big idea** | A real AI project is not the model. It is the model **plus the honest paperwork** saying what it can and cannot do. |
| **New vocabulary** | None. This is a consolidation week. Everything used today was taught in Weeks 4, 15, 19, 20 and 22. |
| **Materials** | The student's photos (shot before class — see Prep), 1 large envelope, 1 marker pen, printed brief template, printed scoring sheet (40 rows), printed blank 4×4 grid, a visible clock or kitchen timer, the booth folder (a cardboard wallet or ring binder) |
| **Tech needed** | A laptop with a webcam, a browser, [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com). No installs. No account needed. |
| **Prep time** | 15 minutes the night before, **plus** one 40-minute photo shoot with the student earlier in the week |

> **🧑‍🏫 Read this box before anything else.** Today is not a lesson with an activity bolted on.
> Today is a **build session with a clock on the wall**. Your job is not to explain AI — the student
> already knows the AI. Your job is to be the person who says *"eleven minutes left on Milestone 3"*
> and refuses to let them skip the boring paperwork. That is genuinely the whole role, and it is
> harder than it sounds.

![The booth: all eleven artefacts](../figures/fig-w34-1-booth-layout.svg)
*Figure 34.1 — The finished booth. Only two of the eleven required things are software.*

---

## 🎯 Lesson Objectives

By the end of today the student can:

1. **Write a capstone brief** that names a real annoyance in their own home, four classes (three real ones plus `other`), the baseline, and a **success bar chosen before anything is trained**.
2. **Split their photos before training** — physically move 20% of every class into a sealed envelope, and explain in one sentence why doing it afterwards would be worthless.
3. **Train and save a model with a real filename** (`booth-v1.tm`) and then **point at the file on the actual disk** before moving on.
4. **Score every held-out photo on paper**, one attempt each, and report accuracy as a **fraction, a decimal and a percentage** next to the 25% baseline.
5. **Build a 4×4 confusion matrix by hand** and read one true sentence off it that the overall accuracy hid.

---

## 🧑‍🏫 What YOU Need to Know First

*Read this once. About twelve minutes. You will finish it understanding the whole point of today.*

### The one-paragraph version

Most people think an AI project *is* the model. It isn't. In a real company the model is roughly
20% of the work. The other 80% is: writing down what problem you are solving, writing down where
your data came from and who said yes, hiding some data before you train so you can measure
honestly, measuring honestly, finding out who your system fails, and being able to explain all of
that to a person who was not there. **Today the student builds the first half of that 80%.**

### Why the paperwork is not busywork

Here is the trap, and it catches adults constantly.

A student trains a model. They hold up a can. It says `RECYCLING 96%`. Everyone claps. The
student now believes the model works. But nothing has actually been *measured*. "It worked when I
tried it" is a story, not a number. There are three separate holes in it:

| The story | The hole |
|---|---|
| "It said recycling and it was recycling" | That is **one** photo. One photo tells you almost nothing. |
| "It's 96% confident" | Confidence is the model's guess *strength*. It is not a hit rate. It can be 96% confident and wrong. (Week 16.) |
| "I tested it and it works" | Tested on what? If those photos were in the training pile, the score measures memory, not learning. (Week 19.) |

The paperwork closes all three holes. The scoring sheet says *how many* photos. The held-out
envelope says *the model had never seen them*. The confusion matrix says *which class it is bad at*.
Without those three pieces of paper, a model is a rumour.

### The single irreversible step: split before you train

This is the one thing today that cannot be fixed afterwards, so it is the one thing you must
personally supervise.

![Three piles of photos, three different jobs](../figures/fig-w34-5-three-envelopes.svg)
*Figure 34.2 — Three piles, three jobs. Mixing the first two is unfixable.*

> **Held-out set** — photos you hide **before** training, which the model never sees, kept to
> measure it honestly afterwards.

The exam analogy is exact, and it is worth saying out loud to the student in these words:

- The **training photos** are the practice questions you study from.
- The **held-out photos** are the sealed exam paper.
- If you study the exam paper, your marks go up and they stop meaning anything.

The reason this cannot be undone is simple: **there is no way to make a model un-see a photo.**
Once a photo has been in the training pile, any score you get from it is contaminated forever. You
cannot repair it by promising to be fair. The only fix is to go and take new photos, which is an
hour of a Saturday. So: envelope first, laptop second. Always in that order.

### The second idea: the success bar goes on paper first

> **Pre-registration** — writing down what would count as success **before** you see the result.

This word is not on the vocabulary list and you do not need to teach it as a term. But the habit is
the point of Milestone 1, so here is why it matters.

Suppose the student trains the model and gets 62%. What do they say? Almost always: *"62%! That's
way better than guessing!"* Suppose they get 41%. What do they say? *"Well, 41% is still better
than 25%, so it works."* Notice that **every possible result was going to be declared a success.**
A test that cannot fail is not a test.

Writing "I will call it useful if it beats 50%" on a piece of paper before training removes the
wriggle room. If the model gets 41%, the honest sentence is *"it did not clear my bar, and here is
what I would change."* That sentence is worth more, educationally and professionally, than a model
that scores 95%.

### The third idea: three numbers, not one

The student must report accuracy three ways. This looks like a maths-teacher fussiness. It isn't.

```
   FRACTION      30 / 40      tells you the SIZE of the test.
                              "95%" out of 20 photos is 19/20. Out of 4 photos it is
                              cheating. The fraction is the honesty.

   DECIMAL       0.75         forces you to actually do the division, and it is the form
                              that stops you writing "133%" by dividing upside down.

   PERCENTAGE    75%          the form a stranger at a fair understands instantly.
```

And every percentage must be printed next to its **baseline**.

> **Baseline** — the score you would get by guessing without looking. With four roughly equal
> classes that is 1 in 4 = **25%**.

75% sounds good. But 75% against a baseline of 25% means the model earned **50 percentage points**
of real skill. If the baseline had been 70% (say, one class was 70% of the data), the same 75%
would be worth almost nothing. A number with no baseline is a boast, not a measurement.

> **⚠️ Units matter, and this is the most common slip in the whole course.** 75% − 25% = 50
> **percentage points**, not "50%". Subtracting two percentages gives points. Say "points" out
> loud every time and the student will copy you.

### The confusion matrix, in plain terms

A **confusion matrix** is a grid. Down the side: what the photo *actually was*. Across the top:
what the model *said*. Each photo puts one tick mark in one box.

![The finished board: accuracy three ways and the matrix](../figures/fig-w34-6-board-accuracy.svg)
*Figure 34.3 — What the board looks like at minute 68.*

Two things to read off it, and only two. That is all you need today:

1. **The diagonal is the correct ones.** Top-left to bottom-right: the boxes where "what it was"
   and "what it said" agree. Add them up, divide by the total, that is the accuracy.
2. **The off-diagonal boxes tell you the story.** In Figure 34.3, the landfill row reads 3, 1, 6, 0.
   The model got 6 of 10 landfill photos right, and it called **three of them recycling**. That is
   not "the model is a bit wrong". That is "shiny landfill things look like cans to it", which
   points straight at what photos to take next.

That second reading is the thing that makes a booth good. Anyone can say "75%". Almost nobody says
"and the 25% it gets wrong is nearly all landfill being called recycling."

### The two misconceptions you will meet today

**Misconception 1: "I can hold photos back after training — I just won't look at them."**

This confuses *the student* not looking with *the model* not looking. The held-out set is about
what the **model** saw during training, not about what the student remembers. If the photos were
in the upload, they trained the model, full stop. Watch for the student who uploads all 50 per
class and then says "I'll test on the last 10". Stop them. That is the unfixable one.

**Misconception 2: "A higher confidence number means it's more likely to be right."**

Week 16 covered this and it will come back today, because the model will produce a big confident
number on a photo it gets wrong, and it will feel like a betrayal. Confidence is how strongly the
model prefers one class over the others. It is calculated by the same machinery that produced the
answer, so it cannot check the answer. The only thing that measures correctness is the held-out
score they are computing today.

### How deep to go, and where to stop

**Go this deep:** the difference between training photos and held-out photos; accuracy as a
fraction; the baseline; reading a row of the confusion matrix.

**Stop here.** Do **not** get into: precision and recall, F1 scores, cross-validation, validation
sets as a third split, or how Teachable Machine works internally. If the student asks about any of
those, the correct answer is *"that's real, it's a Level 2 thing, and it is built on exactly what
you are doing today."* Say it warmly. It is true.

**If the student asks something you cannot answer:** say "I don't know — how could we check?" and
mean it. That sentence is on the syllabus.

---

## 🧰 Prep Checklist

### 🗓️ Earlier in the week — the photo shoot (40 minutes, with the student)

This is the only part of Milestone 2 that will not fit in the lesson, so it happens before.
**Do not skip it and do not do it for them.**

- [ ] Agree the problem and the four classes over dinner. Three real classes plus `other`.
      Good ones: recycling / compost / landfill / other · turmeric / chilli / coriander / other ·
      keys / wallet / glasses / other.
- [ ] **Never** classes about people — mood, age, "who looks friendly". Hard rule, taught in Week 31.
- [ ] Make four folders on the laptop named exactly as the classes, plus a fifth called `heldout`.
- [ ] Shoot **50 photos per class** = 200 photos. About 30 minutes at one photo every 9 seconds.
      Between every 10 photos, change something: the background, the light, the angle, who is
      holding it, near or far. Five or six photos per class should be deliberately awkward —
      half out of frame, blurry, half-hidden.
- [ ] The `other` class is 50 photos of *none of these*: the bare table, hands, a mug, a shoe,
      a TV remote. This class is what stops the booth from confidently calling a stranger's car
      keys "compost".
- [ ] Count the photos and write the four numbers on the fridge. You need them in class.

### 🌙 The night before (15 minutes)

- [ ] Print, from the workbook: the **brief template** (W34-1), the **40-row scoring sheet**
      (W34-4), and the **blank 4×4 grid** (W34-6). Print two spare scoring sheets.
- [ ] Find one large envelope and a marker pen. Write **DO NOT OPEN UNTIL MILESTONE 4** on it now.
- [ ] Find the booth folder: a cardboard wallet, a ring binder, or a labelled shoebox.
- [ ] Put a clock or a phone timer where the student can see it. This matters more than it sounds.
- [ ] **Test the tool yourself for four minutes.** Open teachablemachine.withgoogle.com →
      *Get Started* → *Image Project* → *Standard image model*. Click **Train Model** with nothing
      in it just to see where the button is. Then find **☰ (top left) → Download project as file**.
      Know where those two buttons are before class. That is the entire technical prep.
- [ ] Check your browser will let the page use the camera (a padlock icon in the address bar →
      Camera → Allow).

### 🛟 Fallbacks

| If this fails | Do this instead |
|---|---|
| **No internet at class time** | Do Milestones 1 and 4 on paper using the worked numbers in the Answer Key, and move Milestones 2–3 to the weekend. The arithmetic is the lesson; the website is a tool. |
| **Teachable Machine won't load** | Try a different browser. If still stuck, run the whole session as a paper simulation: the "model" is you, guessing from behind a book, and the student scores your guesses. This genuinely teaches the same thing and is a good lesson in disguise. |
| **The webcam is a black rectangle** | Another app has the camera — quit Zoom, Teams, FaceTime, and any other browser tab, then reload. |
| **The photos never got taken** | Shoot 20 per class in class (12 minutes), split 4 out of each 20, and adjust every denominator: held-out becomes 16, not 40. Say out loud that a 16-photo test is a weaker measurement, and write that in the data card. |
| **Training is spinning forever** | Reload, re-upload one class at a time. Photos over about 4000 pixels wide can choke it; use smaller ones if the laptop is old. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | 🪝 **Hook** | Two booths at the fair. One claps, one convinces. |
| 8–26 | 🧠 **Concept** | The eleven artefacts; the split rule; the success bar |
| 26–40 | 🔍 **Worked Example** | Fill Milestone 1 together, then do the accuracy arithmetic on my numbers |
| 40–60 | 🎲 **Activity** | The Build Sprint: Milestones 2, 3, 4 against the clock |
| 60–70 | 🔑 **Wrap & Assign** | Accuracy three ways on the board, the matrix, homework |

---

### 🪝 Hook — Two Booths (8 minutes)

**Say this:**

> "Picture the school hall in two weeks. There are twenty stalls. I'm going to describe two of them
> and you tell me which one you'd rather be standing at.
>
> Stall number one. A kid has trained a model to tell apples from bananas. They hold up an apple.
> The screen says APPLE, 99%. Everyone claps. It's genuinely a good moment. Then a dad reaches into
> his pocket, holds up his car keys, and the screen says BANANA, 91%. The kid says 'ah, it's not
> trained for that,' and the dad wanders off. Four minutes later nobody remembers the stall.
>
> Stall number two. A kid says: 'My mum puts the yoghurt pot in the wrong bin about four times a
> week. So I built this.' They show it working on three things. Then they say: 'It gets thirty out
> of forty right on photos it has never seen. Guessing would be twenty-five percent. Here's the
> sheet — every one of those forty is written down.' Then they say: 'It's terrible at landfill.
> Six out of ten. Watch this' — and they deliberately make it fail. Then they hand over a pen and
> say 'try to break it, I'll write down what you did.'
>
> Which one do you believe?"

Let them answer. They will say the second one. Then:

> "Right. And here is the thing that surprises everyone: stall two is not *better at AI*. Both
> models are about the same. Stall two just did the paperwork. That's the whole difference, and
> the paperwork is what we're building today."

**Do this:** Put the eleven-artefact figure (34.1) in front of them, printed or on screen. Let them
look at it for a slow ten seconds without saying anything. Then point at the laptop in the picture.

**Ask this:**

- *"How many of these eleven things are computer things?"*
  → **Hoping for:** two — the model file and the app.
  → **If they say more:** count with them, out loud, pointing. Brief, counts, envelope, data card,
    test sheet, matrix, bias report, sign, demo script — that is nine pieces of paper. "Nine to two.
    That ratio is the actual job."
- *"Which of the eleven do you think takes the longest?"*
  → **Hoping for:** any answer with a reason. The true answer is the app (75 minutes, next week)
    and the photos.
  → **If they shrug:** tell them: the app takes longest, and the test sheet is the one people skip.
    "Today we do the one people skip."

---

### 🧠 Concept — The Eleven Things and the One You Cannot Undo (18 minutes)

**Say this — part one, the shape of today:**

> "There are seven milestones in this project. We do the first four today and the last three next
> week. They have to happen in this order, and I want to tell you why the order isn't just tidiness.
>
> Milestone one is the brief — one page saying what problem you're solving and what would count as
> winning. Milestone two is collecting the photos and *splitting* them. Milestone three is training
> and saving the model. Milestone four is the honest test.
>
> You cannot swap two and three. You'll see why in about ninety seconds."

**Do this:** Show Figure 34.4 (the milestone map). Tick 1 to 4 with a pen as you name them.

![The seven milestones, with one to four ticked](../figures/fig-w34-2-milestone-map.svg)
*Figure 34.4 — Seven milestones. Four of them are today.*

**Say this — part two, the split:**

> "Here's the rule that matters more than everything else today. Before you train, you take twenty
> percent of your photos out and put them in an envelope. Ten out of every fifty. And you don't
> open the envelope until the model is finished.
>
> Why? Think about an exam. Your teacher gives you twenty practice questions. You study them all
> week. Then on exam day, the exam *is* those twenty questions. You get 100%. Did the exam measure
> anything?
>
> No. It measured whether you'd seen the paper.
>
> Same here. If we test the model on photos it trained on, of course it does well — it's seen them.
> A model that just memorised every photo would score 100% and be completely useless on your mum's
> yoghurt pot. The score can't tell the difference between memorising and learning. So it isn't a
> measurement at all.
>
> And here's the bit I need you to really hear: **this is the only mistake today that cannot be
> undone.** If you upload all fifty and then decide to hold ten back — too late. There is no way to
> make a model forget a photo. The only fix is going and taking new photos. So the envelope gets
> sealed before the laptop is even open."

**Do this:** Hold up the envelope. Write today's date on it in front of them. This tiny bit of
theatre is doing real work — it makes the split a physical, memorable event rather than a
folder-drag they forget.

**Say this — part three, the bar:**

> "One more thing before we build. Milestone one asks you to write down a number: 'I will call this
> useful if it beats blank percent.' You write it *before* you train.
>
> I know why that feels pointless. Let me show you why it isn't. Imagine you train it and get 62%.
> What are you going to say?"

Let them answer. They will say something like "that's good, better than guessing."

> "Right. Now imagine you get 41%. What would you say?"

They will say "well, it's still better than 25%."

> "Exactly. So whatever happened, you were going to call it a win. That means the test couldn't
> fail — and a test that can't fail isn't a test. If you write '50%' on the paper right now, then
> 41% means you missed, and you get to say *why*, and that sentence is the most impressive thing on
> the whole booth. Grown-up scientists do this. It's called pre-registering, and it exists because
> grown-ups move goalposts too."

**Ask this:**

- *"Why can't we hold photos back after we train?"*
  → **Hoping for:** because the model already saw them, so the score doesn't mean anything.
  → **If they say "because it's against the rules":** push once. "Who made the rule? What would
    actually go wrong?" Steer to: the score can no longer tell memorising from learning.
- *"With four classes, what score would you get by just guessing with your eyes shut?"*
  → **Hoping for:** 1 in 4, 25%.
  → **If they say 50%:** they are thinking of two classes. Draw four boxes on paper and ask which
    one a blindfolded guess lands in. One in four.
- *"If the model scores 30%, is that good?"*
  → **Hoping for:** barely — it's only 5 points above blind guessing.
  → **If they say yes because 30 > 25:** agree it's *above* baseline, then ask "by how much?"
    Five points. Then ask "would you trust it with your mum's recycling?" No.
- *"What's the difference between 'it worked when I tried it' and 'it got 30 out of 40'?"*
  → **Hoping for:** the second one is a number, and you can tell how many tries it was.
  → **If they can't answer:** "How many tries was 'it worked when I tried it'?" One. "How many was
    30 out of 40?" Forty. "Which would you bet on?"

---

### 🔍 Worked Example Together — Milestone 1, Then the Arithmetic (14 minutes)

This segment does two things back to back. Keep both moving.

#### Part A — Fill in the brief, out loud (7 minutes)

**Do this:** Put the printed brief template (workbook page W34-1) in front of the student and hold
the pen yourself for the first two lines, then hand it over. Read each prompt aloud, they answer,
they write.

![A filled-in capstone brief with the success bar circled](../figures/fig-w34-3-capstone-brief.svg)
*Figure 34.5 — What a finished brief looks like. The circled line is the point.*

**Say this:**

> "Line one. In my house, blank happens about blank times a week. Don't write something impressive.
> Write something that actually annoyed somebody. Last week. Who did it annoy?"

> "Now the four classes. Real names, not Class 1 and Class 2 — write `recycling`, not `Class A`.
> And the fourth one is always `other`. Why do you think `other` is compulsory?"

> "Now the baseline. Four classes, roughly equal, so blind guessing is one in four. Write it as a
> fraction and a percentage: 1/4 = 25%."

> "Now the line that matters. 'I will call it useful if it beats ___ percent.' Pick a number. Once
> it's written I'm going to draw a circle round it, and neither of us is allowed to change it later,
> including me."

**Ask this:**

- *"Why is `other` compulsory?"*
  → **Hoping for:** because strangers will hold up things that aren't any of my three classes.
  → **If they say "to make it four":** give them the concrete version — the confidences always add
    up to 100%, so *something* always wins. Without `other`, a car key has to be called compost.
- *"What number should the bar be?"*
  → **Hoping for:** anything they can justify. 50% and 60% are both sensible for four classes.
  → **If they say 95%:** don't forbid it, but ask "what happens if you get 80%? Do you tear the
    booth up?" Let them revise it themselves. Self-revision here is the learning.
  → **If they say 26%:** ask "would a machine that's one point better than a coin-flip be worth
    building?" Let them raise it.

#### Part B — The arithmetic, on my numbers (7 minutes)

Use *these* numbers, not their real ones, so nothing today depends on how their model performs.

**Do this:** Draw this on the board or a sheet of paper as you talk:

```
     30 correct out of 40 photos

     FRACTION     30 / 40
     DECIMAL      30 ÷ 40 = ?
     PERCENTAGE   ? × 100 = ?
```

**Say this:**

> "Pretend for a second this is your model. Thirty right out of forty. Do the division. Write it
> down even though there's a calculator here — I want to see the working.
>
> Forty times zero point seven is twenty-eight. That leaves two. Two divided by forty is nought
> point nought five. So nought point seven plus nought point nought five is nought point seven
> five. Times a hundred: seventy-five percent.
>
> Or the quick check: thirty over forty is the same as three over four. Three quarters. 0.75. 75%.
> Both roads, same place. Always take the second road as a check.
>
> Now — and this is the bit people forget — write the baseline next to it. Twenty-five percent.
> And then the gain: seventy-five take away twenty-five is fifty. Fifty **percentage points**. Not
> fifty percent. Points. When you subtract two percentages you get points."

**Ask this:**

- *"Compute 27 out of 36 as a decimal and a percentage."*
  → **Hoping for:** 0.75 and 75% (27/36 simplifies to 3/4).
  → **If they get 1.33:** they divided 36 by 27. Say: "accuracy can never be more than 1. If your
    decimal is bigger than 1, you flipped the division." Redo it together.
- *"A friend says their model is 95% accurate. What are your two questions?"*
  → **Hoping for:** out of how many? and what's the baseline?
  → **If they only get one:** give them the other and make them say both back. This exact reflex is
    point 6 of the Level 2 gate in two weeks.

---

### 🎲 The Activity — The Build Sprint (20 minutes)

Full instructions in the next section. In summary: a visible clock, three milestones, no talking
about anything else.

**Do this:** Start the timer where they can see it. Announce each milestone's deadline out loud as
you begin it. Do not help with the mouse unless something is actually broken.

**Say this at the start:**

> "Twenty minutes. Three milestones. I'm the clock, not the help desk. If something breaks I'll
> fix it; if something is just fiddly, that's yours. Milestone two — the split — you have three
> minutes and it happens before the browser opens. Go."

**Ask this, at the moment they finish training:**

- *"Before you click anything else — what's the file called and where is it?"*
  → **Hoping for:** `booth-v1.tm`, in the Downloads folder (or wherever they saved it).
  → **If they don't know:** stop everything and go and find it in the file browser together. Do not
    proceed to Milestone 4 until the file has been seen with human eyes. Teachable Machine has no
    autosave and closing the tab loses everything.

---

### 🔑 Wrap & Assign (10 minutes)

**Do this:** Take the completed scoring sheet. On the board, write the fraction, then the division,
then the percentage, then the baseline, then the gain — the left half of Figure 34.3. Then draw the
empty 4×4 grid and fill it together from the sheet, one photo at a time, reading aloud: *"true
recycling, said recycling — tick in the top-left."*

**Say this:**

> "Look at the diagonal. Those are the ones it got right — add them up, that's your top number.
> Now look off the diagonal. Find the biggest number that isn't on the diagonal. That box is your
> model's actual problem, and it has a name: it's the class it gets wrong and *what it says instead*.
>
> Tonight you're going to write one sentence: 'My model is worst at blank, and when it's wrong about
> blank it usually says blank.' That one sentence is worth more at the fair than the accuracy is."

**Say this to assign the homework:**

> "Homework is assembly, not new work. Everything you made today goes into the booth folder, neatly,
> so a stranger could pick it up and understand it. Six documents: the brief, the counts, the test
> sheet with the accuracy three ways, the confusion matrix drawn properly, the first draft of the
> data card, and the model file — which lives on the laptop, so write the filename and where it is
> on a card and put the card in the folder. About forty-five minutes. Don't rush the data card:
> box six, 'what's NOT in it', is the one adults actually read."

**Ask this — the exit question:**

- *"Tell me in one sentence why we sealed the envelope before we opened the laptop."*
  → **Hoping for:** so the model never saw those photos, so the score means something.
  → **If it's vague:** give them the exam sentence and have them say it back in their own words
    before they leave the table.

---

## 🎲 The Activity, In Full

### The Build Sprint — Milestones 2, 3 and 4 against a clock

**What it is.** Twenty minutes, three milestones, one visible clock. The student builds; you time,
supervise the split, and refuse to let anything be skipped.

**Materials:** the 200 photos in four class folders · one large envelope marked **DO NOT OPEN UNTIL
MILESTONE 4** · the printed 40-row scoring sheet and a pencil · a laptop with browser and webcam ·
a clock the student can see.

**Setup before the timer starts:** all four photo folders open on screen · an empty `heldout` folder
created · scoring sheet and pencil to the *right* of the laptop · envelope on the table with the
marker on top of it.

![Three piles of photos, three different jobs](../figures/fig-w34-5-three-envelopes.svg)
*Figure 34.6 — Envelope first. Browser second. That order is the activity.*

### The rules

1. **The envelope closes before the browser opens.** No "I'll just check something".
2. **One photo, one attempt.** No retakes because "the lighting was off" — if lighting matters, that
   *is* the finding, and it goes in the report.
3. **Write it down as it happens**, not from memory afterwards. Memory is where honesty leaks out.
4. **The clock is the boss.** If a milestone overruns, the next one gets shorter, and you say so.

### Timing, minute by minute

| Minutes | Milestone | What the student does | What you do |
|---|---|---|---|
| 0–3 | **M2 — the split** | Move 10 photos out of each class folder into `heldout`. Take them from all over the folder, not just the last ten. Count out loud: 10, 10, 10, 10. Print or note the filenames, put the note in the envelope, seal it. | Watch. Count with them. Sign the envelope flap with the date. |
| 3–9 | **M3 — train and save** | Teachable Machine → Image Project → Standard. Rename the four classes properly. Drag **only** the four training folders in — never `heldout`. Check each class shows 40 samples. Train Model. Then ☰ → Download project as file → save as `booth-v1.tm`. | At minute 8, ask "where is the file?" and make them show you. |
| 9–10 | **M3 check** | Open the file browser, find `booth-v1.tm`, read the name out loud. | Nod. This 60 seconds saves the whole project. |
| 10–19 | **M4 — score the envelope** | Open the envelope. Feed each held-out photo to the Preview panel one at a time. For each: write the true label, the prediction, the top confidence, and a ✓ or ✗. | Read the true label out loud from the folder name so they only have to record. This roughly doubles the speed. |
| 19–20 | **M4 tally** | Count the ticks. Circle the total at the bottom of the sheet. | Say the number out loud, whatever it is, with no reaction either way. |

### What "finished" looks like

The envelope is open and empty and every photo in it has a row · the sheet has 40 filled rows and a
circled total · `booth-v1.tm` exists on disk and the student can point at it · nothing was retaken
and no row was filled in from memory.

> **💡 Try this:** at minute 19, before any arithmetic, ask *"how do you feel about that number?"*
> and write the answer on the back of the sheet. Comparing the feeling with the computed percentage
> two minutes later is a small, sharp lesson in why we measure.

### Variation — easier

Score **20** photos (5 per class) and reseal the other 20 for homework. Change every denominator and
say out loud: *"a 20-photo test is a weaker measurement, and we're writing that down."* Honest and
smaller beats dishonest and complete. If the arithmetic is the sticking point rather than the time,
pre-fill the fraction and have them do only the division and the percentage.

### Variation — harder

1. **Per-class accuracy too.** Four extra divisions: 9/10, 8/10, 6/10, 7/10 — then check the average
   equals the overall (it does, when the classes are equal-sized). A satisfying arithmetic check.
2. **Predict before you score.** Before opening the envelope, write down which class will be worst
   and why, with a photo count as the reason. A free rehearsal of next week's bias prediction.
3. **The margin column.** Add top confidence minus second confidence, then find the smallest margin.
   That photo is the one the booth should say "not sure" about next week.

---

## ❓ Questions Students Ask This Week

**"Can't I just use more photos so I don't need to hold any back?"**

No — the held-out photos aren't wasted, they're *spent on measurement*. Ten per class buys the only
honest number in the project. And size never fixes contamination: a model trained on 10,000 photos
and tested on 10 of those same photos is still being tested on its own homework.

**"What if my accuracy is rubbish?"**

Then you have a real result, which is what we came for. What separates a good project from a bad one
is not the number — it's whether the number is honest and whether you can say what you'd change. A
booth that says "58%, here's the sheet, here's the class it fails on, here's what I'd collect next"
beats one that says "99%" with nothing behind it. Every time.

**"Why 20% held out? Why not 10% or half?"**

A trade-off, not a law. Hold out too little and the test is tiny and noisy — with 4 photos, one
mistake swings the score 25 points. Hold out too much and the model has less to learn from. About
20% is the usual compromise, and you will see that same 0.2 written into Level 2's Python next year.

**"The model said 97% and it was wrong. Is it broken?"**

No, and this matters. That 97% is *guess strength* — how strongly it prefers that class over the
other three. It comes out of the same machinery as the answer, so it cannot check the answer.
Nothing broke. Write that photo down: "the highest confidence my model reached while completely
wrong" is one of the most memorable things you can put on a poster.

**"Could I take the held-out photos on a different day?"**

Yes, and it makes the test *better* — different day, different surface, different light is a harder
and more honest exam. If the model still does well, you have learned something real. If it
collapses, you have learned something even more useful.

**"How do professionals know when a model is good enough to actually use?"**

**Nobody knows for sure, and here's why.** There is no universal threshold; it depends entirely on
what happens when it's wrong. A bin sorter at 75% is useful, because being wrong means a yoghurt pot
in the wrong bin. A model reading medical scans at 99% may be nowhere near good enough, because the
1% is a person. Real teams argue about this for weeks and sometimes get it wrong and people are
hurt. What everybody *does* agree on is: measure honestly, split the score by group, write down who
it fails. That part is not opinion — and it is exactly what you did today.

**"Why does it have to be a problem from my own house?"**

Practically: you can collect 200 photos of things you own, and go back for 50 more when the bias
report says so. You cannot do that with every dog breed on your street. Honestly: you know the
ground truth. If you can't be sure of the right answer yourself, your label column is noise and your
test sheet measures nothing.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The student uploads all 50 photos per class, then says "I'll test on the last ten" | Teachable Machine makes uploading everything feel natural, and holding photos back feels wasteful | Stop immediately. Delete the class, move 10 files into `heldout` in the file browser, re-upload. Costs three minutes now; costs the whole project if you let it slide. |
| The Teachable Machine tab gets closed before the file is downloaded | There is no autosave and no warning | Nothing can be recovered — retrain from the same folders (2 minutes) and download **first** this time. Then say out loud: "that's why Milestone 3 has a stop sign in it." |
| The student retakes a held-out photo because "the lighting was weird" | It feels like fairness | Gently: "That's the finding. Write it in the notes column." One photo, one attempt. If you allow one retake you have allowed all of them. |
| Scoring stalls around photo 15 — it's boring and slow | It genuinely is boring, and 40 is a lot | Take over the reading. You call out the true label and the file, they only record. Or switch to the easier variation: 20 photos now, 20 as homework, denominator changed. |
| The class counts are wildly unequal (60, 60, 60, 12) | The `other` class is the least fun to shoot, so it gets skipped | Compute the balance check with them: (60 − 12) ÷ 60 = 80%, target is under 20%. Then set the fix as part of tonight's homework: 40 more `other` photos before next week, retrain. This is a real finding, not a failure. |
| The accuracy comes out at 25–35% and the student deflates | Genuinely disappointing, and it usually means class imbalance or too-similar photos | Do not rescue it with praise. Go to the confusion matrix and find *which* class is dragging it down. Turning a bad number into a specific diagnosis is the actual skill, and it will visibly lift them. |
| The student wants to fiddle with settings and retrain "to get a better score" | Very natural, and it is the beginning of a real bad habit | Allow at most one retrain, and only if something was broken (wrong folder uploaded). Explain: every time you tweak based on the test score, you leak a bit of the test set. The envelope is not a scoreboard to farm. |
| You end up doing the clicking | Faster, and the clock is ticking | Sit on your hands. The one thing that must not happen today is a booth the adult built. Being slow is fine. Being not-theirs is not. |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** the confusion matrix in class (move it to homework with the Answer Key example beside
them), and 40 held-out photos down to 20 — saying why out loud, so the shortcut is itself honest.

**Reteach, in this order:** (1) the exam analogy, with a real pretend exam — ask five questions,
then ask the *same* five, then ask what the 100% proved; (2) fractions to percentages with easy
pairs first — 5/10, 3/4, 7/10, then 30/40; (3) the word "points" — write "75% − 25% = 50 points" and
read it aloud three times.

**Drop entirely if needed:** per-class accuracy, the margin column, the pre-scoring prediction.

### If they are flying

- *"Your held-out photos were shot the same day as the training photos. Why is that a weaker test
  than a different day, and what would you change?"*
- *"Look at the biggest off-diagonal number. Design the exact photos that would fix it — how many,
  of what, in what light. Give me a number."*
- *"Five more minutes of camera time: more training photos or more held-out photos? Defend it."*
  (No single right answer. More held-out = a more reliable measurement; more training = possibly a
  better model, measured less well. The defence is the point.)
- Add the margin column, find the least-sure photo, and predict whether next week's 70% threshold
  would catch it.

### If they won't engage today

Capstone weeks are a common time for this — the project feels big.

**Shrink it to one thing.** *"Fine. One thing today: sealing the envelope. Three minutes, then we
stop."* Do the split, seal it, sign it, put it away. That single act preserves the whole project,
because it is the only step that cannot be recovered later. If there is any appetite after that, do
Milestone 1 conversationally — you write, they talk. "What annoys you at home?" is a chat.

**Do not** run the sprint at gunpoint. A rushed, grumpy scoring sheet is a *dishonest* scoring
sheet, and the honesty is the entire lesson. Move the sprint to the weekend.

---

## ✅ Assessing Understanding

Three checks, five minutes, at the very end.

**Check 1 — the irreversible step.**
Ask exactly: *"Why did we seal the envelope before we opened the laptop, and what would have gone
wrong if we'd done it the other way round?"*
> **A good answer** names both halves: the model would have seen those photos, so the score would
> measure memory instead of learning — and there's no way to fix it afterwards except taking new
> photos. A weak answer says "because those are the rules."

**Check 2 — the number with its baseline.**
Point at their own result and ask: *"Say that number the way you'd say it at the fair."*
> **A good answer** contains all three parts: the fraction, the percentage, and the baseline —
> e.g. "30 out of 40, that's 75%, and guessing would be 25%." If they say only "75%", ask "out of
> how many?" and "compared to what?" until all three appear.

**Check 3 — reading the matrix.**
Point at the biggest off-diagonal number and ask: *"What is this box telling us?"*
> **A good answer** names both classes in the right order: "three landfill photos got called
> recycling." A weak answer says "it got three wrong" without saying *which way round*. The
> direction is the whole information.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks testing on training photos is fine. Reports accuracy as a bare percentage or not at all. |
| **2 — Emerging** | Splits when told to, but can't say why. Computes the percentage with help. Doesn't mention a baseline. |
| **3 — Developing** | Splits before training and can explain it with the exam analogy. Gives fraction and percentage. Mentions the baseline when prompted. |
| **4 — Secure** | Splits unprompted. Volunteers all three forms plus the baseline and the gain in points. Reads the diagonal correctly. Wrote the success bar before training and honours it. |
| **5 — Mastery** | All of level 4, plus: names the worst class *and what it is confused with*, prices a fix in photos, and points out that a same-day held-out set is a weaker test than a different-day one. |

---

## 📤 Homework to Assign

**Say this:**

> "No new thinking tonight — this is assembly. Everything we made today goes into the booth folder,
> laid out so a stranger who has never met you could pick it up and understand the project. Six
> things. About forty-five minutes.
>
> The one to take seriously is the data card, and inside the data card, box six: *what's NOT in it*.
> That's the box adults actually read. 'No photos taken after dark. No photos of squashed cans. All
> photos taken by me, on the kitchen table.' Uncomfortable and specific beats comfortable and vague."

**Workbook pages:** `../workbook/week-34.md`, pages **W34-1 to W34-8**.

| Page | What it is | Time |
|---|---|---|
| W34-1 | The brief (finish it neatly if it was scribbled in class) | 5 min |
| W34-2 | The counts table + the balance check | 5 min |
| W34-3 | Model file record card: filename, folder, date, size | 3 min |
| W34-4 | The 40-row scoring sheet (copy up neatly if needed) | 5 min |
| W34-5 | Accuracy three ways + baseline + gain, division shown | 7 min |
| W34-6 | The 4×4 confusion matrix, drawn by hand, plus the one-sentence finding | 10 min |
| W34-7 | Data card draft — all 8 boxes, especially attribution and permission | 12 min |
| W34-8 | Two reflection questions | 3 min |

**Total: about 50 minutes.**

> **⚠️ Watch out:** if the folder ends up as a loose pile of paper on a bedroom floor, next week's
> lesson loses its first fifteen minutes to a search party. Put the folder somewhere specific and
> agree where, out loud, tonight.

![Inside the booth folder: six documents](../figures/fig-w34-4-booth-folder.svg)
*Figure 34.7 — What the folder should look like when it comes back next week.*

---

## 🔑 Answer Key

### Lesson questions

| Question asked in the lesson | The worked answer |
|---|---|
| **Hook** — how many of the eleven are computer things? | Two: the model file `booth-v1.tm` and the Scratch app. The other nine are written or physical — brief, counts, sealed photos, data card, test sheet, matrix, bias report, sign, delivered demo. |
| **Hook** — which takes longest? | The Scratch app (75 min, next week) and the photo shoot (60 min). The test sheet takes 40 min and is the one people skip — which is exactly why it is worth the most. |
| **Concept** — why can't we hold photos back after training? | The model has already seen them, so their score measures memory, not learning, and the two cannot be told apart. There is no way to make a model un-see a photo; the only repair is new photos. |
| **Concept** — what would guessing score with four classes? | 1 in 4 = 1/4 = 0.25 = **25%**. (Three classes → 33.3%; two → 50%.) |
| **Concept** — is 30% good? | It is 5 percentage points above baseline: above guessing, practically useless. Compare 75%, which is 50 points above. The **gain** is what tells you anything was learned. |
| **Concept** — "it worked when I tried it" vs "30 out of 40"? | One attempt with no record, versus forty attempts written down as they happened. The fraction shows the size of the test; a bare percentage hides whether it came from 4 photos or 400. |
| **Worked example** — why is `other` compulsory? | The confidences always add to 100%, so something always wins. Without an `other` class the model *cannot* say "none of these", and a stranger's car keys get confidently labelled compost. |
| **Worked example** — what should the bar be? | Anything the student can justify; 50–60% is sensible for four classes. 26% makes success meaningless; 95% turns a genuinely good model into a failure. The reasoning matters more than the number. |

**Worked example — "27 out of 36 as a decimal and a percentage."**
```
   27 / 36  →  divide top and bottom by 9  →  3 / 4
   36 × 0.7 = 25.2 ; 27 − 25.2 = 1.8 ; 1.8 ÷ 36 = 0.05 ; 0.7 + 0.05 = 0.75
   0.75 × 100 = 75%
```
**0.75 and 75%.** A decimal accuracy is always between 0 and 1; if it comes out above 1 the division
was done upside down.

**Worked example — "A friend says 95% accurate. Your two questions?"**
**Out of how many?** (19/20 and 950/1000 are different claims.) **What's the baseline?** (95% is
impressive against 25% and worthless against 94%.)

**Activity — "Where is the file?"** `booth-v1.tm`, normally in Downloads. The student must *see* it
in the file browser, not assume it. Teachable Machine has no autosave.

**Wrap — "Why did we seal the envelope first?"** So the model never saw those photos — the only
thing that makes the score a measurement rather than a memory test.

---

### Workbook answers

#### W34-1 — The brief

Answers vary by student. A brief is **complete** when all seven of these are present:

| Must contain | Example of a good version |
|---|---|
| A specific annoyance with a frequency and a person | "The wrong bin gets used about 4 times a week. It annoys Mum most." |
| Four class names, real words | `recycling`, `compost`, `landfill`, `other` |
| `other` present | ✓ |
| The input named | "a webcam photo of one piece of rubbish" |
| Baseline stated as a fraction and a percentage | 1/4 = 25% |
| A success bar, written before training | "I will call it useful if it beats 50%" |
| Consequences both ways | Right: the correct bin is named. Wrong: a pot in the food bin — annoying, nobody hurt. |

**Common problems and the fix:** classes named `Class 1`/`Class 2` (rename them); no `other` (add
it, take 50 photos); a bar written after the score was known (that one cannot be fixed — write down
that it happened, which is itself honest, and pre-register properly next time).

#### W34-2 — The counts table and the balance check

```
   class        total  heldout(20%)  train        balance check:
   recycling      50        10         40         (biggest − smallest) ÷ biggest
   compost        50        10         40       = (50 − 50) ÷ 50 = 0%   ✓ under 20%
   landfill       50        10         40
   other          50        10         40         a REAL failing example:
   ──────────   ─────   ─────────    ─────        (60 − 12) ÷ 60 = 0.8 = 80%  ✗
   TOTAL         200        40        160         fix: 48 more `other`, retrain
```

#### W34-3 — Model file record card

```
   filename: booth-v1.tm     folder: Downloads/     saved: <today>
   trained on:     160 photos, 40 per class, 50 epochs, default settings
   NOT trained on: the 40 photos in the sealed envelope        ← the line that matters
```

#### W34-4 / W34-5 — The scoring sheet and accuracy three ways

The sheet has 40 rows of `# · true label · predicted · top % · ✓/✗`, e.g.
`2  recycling  landfill  61  ✗`. Ticks counted: **30**.

```
   FRACTION     30 / 40
   DECIMAL      30 ÷ 40 :  40 × 0.7 = 28 → remainder 2 ; 2 ÷ 40 = 0.05 ; 0.7 + 0.05 = 0.75
                check: 30/40 = 3/4 = 0.75  ✓
   PERCENTAGE   0.75 × 100 = 75%
   BASELINE     25%          GAIN  75 − 25 = 50 percentage points
```

**Per-class accuracy** (the harder variation):

| True class | Row of the matrix | Correct | Accuracy |
|---|---|---|---|
| recycling | 9 / 0 / 1 / 0 | 9 of 10 | **90%** |
| compost | 1 / 8 / 1 / 0 | 8 of 10 | **80%** |
| landfill | 3 / 1 / 6 / 0 | 6 of 10 | **60%** |
| other | 1 / 0 / 2 / 7 | 7 of 10 | **70%** |

Check: 9 + 8 + 6 + 7 = 30 ✓ and (90 + 80 + 60 + 70) ÷ 4 = 300 ÷ 4 = 75% ✓ — the average of the
per-class accuracies matches the overall **because all four classes have exactly 10 photos**. If the
classes were different sizes, it would not, and the overall would be the one to trust.

#### W34-6 — The confusion matrix and the finding

```
                        PREDICTED
                   rec   com   lan   oth
   TRUE  rec        9     0     1     0     = 10
         com        1     8     1     0     = 10
         lan        3     1     6     0     = 10
         oth        1     0     2     7     = 10
                   ──    ──    ──    ──
                   14     9    10     7     = 40
```

Checks the student does themselves: every row adds to 10 ✓ · all sixteen boxes add to 40 ✓ · the
diagonal 9 + 8 + 6 + 7 = 30 matches the tick count on the scoring sheet ✓

**The one-sentence finding:**

> "My model is worst at **landfill** — 6 out of 10 — and when it gets landfill wrong it usually says
> **recycling** (3 of the 4 mistakes)."

"75%" tells a visitor nothing they can act on. "It calls shiny landfill things recycling" tells them
what to hold up to break it, what photos would fix it, and that the student actually looked. *(If two
classes tie for worst, say so and name the biggest single off-diagonal box instead.)*

#### W34-7 — Data card draft

All eight boxes filled. Model answers for the two that get skipped:

> **Box 4, Permission.** "The rubbish is our household's. I asked Mum on Saturday 14th and she said
> yes. No faces appear in any photo — I checked all 200."
>
> **Box 6, What's NOT in it** *(the box adults read first)*. "No photos after dark — all 200 shot
> between 10am and 4pm. Nothing squashed or dirty. One kitchen, one table, one tablecloth, one
> person's hands. No glass at all."

Box 7 reads: *30/40 = 75% on held-out photos; baseline 25%; worst class landfill at 60%.*
Box 8 is a draft of next week's sign: *"DO NOT USE THIS FOR a real recycling bin, anything in a dark
kitchen, or glass — I have no glass photos at all."*

#### W34-8 — Reflection

**"Which step could not be undone, and why?"**
> Splitting before training. Once a photo has trained the model, no score from it can tell learning
> from memorising, and there is no repair except collecting new photos.

**"Write the sentence you'd say to a stranger at the fair."**
> Four parts — fraction, percentage, baseline, failure: *"It got 30 out of 40 photos right that it
> had never seen — 75%, against 25% for blind guessing. It's worst at landfill, six out of ten, and
> it usually calls those recycling."* Percentage only is incomplete; send them back for the rest.

---

## 🔮 Next Week Preview

Next week is the other half of the booth, and it contains the hardest milestone in the whole
project: the Scratch app. Four different behaviours, one per class, plus a **confidence threshold**
so the app says "not sure" instead of guessing — which is the single most grown-up thing the student
will build all year. After that comes the bias report (a measured gap, a named failing group, a
priced fix), the DO-NOT-USE sign, and the first rehearsal of the five-minute demo.

**Prep early, this week:**

1. **Decide Route A or Route B now.** Route A uploads the model to a public Google link; Route B
   keeps everything on the laptop and the student types the prediction in. **Default to Route B
   unless you have actively decided to allow the upload.** If you want Route A, open
   `stretch3.github.io` once this week and check it loads with a Teachable Machine extension —
   if it doesn't, that decides it.
2. **Shoot the four bias-test batches**, 10 photos each: `control` (same conditions as training),
   `new-lighting` (a lamp, after dark), `new-hands` (somebody else holding the items),
   `new-background` (a different room). About 25 minutes. New photos, taken *after* training, on
   purpose.
3. Find a sheet of poster paper and a thick marker. The DO-NOT-USE sign has to be the boldest thing
   on the booth, and that needs a real marker, not a biro.

---

[⬅ Week 33](week-33.md) · [Course Home](../README.md) · [Week 35 ➡](week-35.md) · [Student Guide](../student-guide/week-34.md) · [Workbook](../workbook/week-34.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
