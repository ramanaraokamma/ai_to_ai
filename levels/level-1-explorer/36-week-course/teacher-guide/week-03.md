# Week 3 — AI Detective: Find 15 in Your Own Day

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Week 4 ➡](week-04.md) · [Student Guide](../student-guide/week-03.md) · [Workbook](../workbook/week-03.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (60- and 75-minute versions in §The Lesson) |
| **Type** | **Lab** — the first one. Hands on a keyboard, evidence written down. |
| **Big idea** | Almost every AI you meet is narrow — brilliant at one job and completely blank at everything else — and some of it *generates* instead of *choosing*. |
| **New vocabulary** | generative AI · narrow AI · general AI (AGI) · confidence score |
| **Materials** | Laptop with speakers · 15 sticky notes (or torn scraps) · a large sheet or the table top for the board · the student's Week 1 Spotter's Log (8 rows) · pencil · printed score card |
| **Tech needed** | A browser and internet. `quickdraw.withgoogle.com` and **one** chatbot that an adult has approved. **You drive the chatbot keyboard, not the student.** |
| **Prep time** | 10 minutes the night before (test both sites) + 20 minutes reading this file |
| **Source module** | [`module-01-what-ai-is-and-isnt.md`](../../module-01-what-ai-is-and-isnt.md) §4, §5 |

> **🔒 Safety, before anything else.** Two rules from
> [`00-orientation.md`](00-orientation.md) §8 apply hard today:
> **(1)** An adult is at the keyboard for every chatbot session. Not beside it — *at* it. Never as
> homework, never solo.
> **(2)** Quick, Draw! **sends every drawing to Google** and adds it to a public open dataset. That
> is fine — you're drawing shapes, not names or faces — but **tell the student out loud before they
> draw.** It takes fifteen seconds and it teaches a Week 32 lesson for free.

---

## 🎯 Lesson Objectives

By the end of this lesson the student can:

1. **Distinguish a system that picks a label from one that generates new content**, using one test:
   count the possible outputs. A short fixed list = picking. A blank page = generating.
2. **Prove a system is narrow** by designing a task one small step sideways from its job, running it,
   and recording the failure as evidence.
3. **Read a confidence score as a preference strength**, not a promise — and say why "94%" does not
   mean "right 94 times out of 100".
4. **Classify fifteen real systems from their own day** into rules / learned / generating, and defend
   three genuinely hard calls in writing.

Objective 2 is the lab skill: they must *design* the sideways task themselves. Doing your sideways
task for them costs the whole objective.

---

## 🧑‍🏫 What YOU Need to Know First

*About thirteen minutes. Complete — you need nothing else.*

### Where we are

Week 1: a person writes if-then rules. Week 2: nobody writes the rule; a machine finds it from
labelled examples. Today adds the third box and then puts a hard limit around all three.

### Box three: generating instead of choosing

Last week's spam filter produces one of exactly two words: `spam` or `not spam`. That answer is a
**label** — a choice from a fixed menu.

Some systems don't choose from a menu. They *build* something, piece by piece, that never existed
before.

> **Generative AI** — a system that produces new content (text, images, sound, video) rather than
> choosing a label from a fixed list.

**The analogy that works:** a multiple-choice question gives you four boxes and you tick one. That's
labelling. An essay question gives you a blank page and you write three hundred words that have never
been written in that order before. That's generating. Same student, same brain, two completely
different kinds of output.

![Picking from a menu versus writing a new dish](../figures/fig-w03-4-menu-vs-blank-page.svg)

*Figure 3.1 — The test is countable: how many different things could come out?*

**The test, and it is exact:** count the possible outputs.

| System | Possible outputs | How many? | Kind |
|---|---|:--:|---|
| Spam filter | `spam`, `not spam` | 2 | picking a label |
| Photo animal tagger | `cat`, `dog`, `bird`, `horse`, `fish` | 5 | picking a label |
| Handwriting digit reader | `0`–`9` | 10 | picking a label |
| Chatbot writing a paragraph | any sequence of words | effectively unlimited | **generating** |
| Image maker | any picture | effectively unlimited | **generating** |

**The bit that matters and that people get wrong:** generative AI is *inside* machine learning, not
beside it. A chatbot learned from examples exactly like a spam filter did. It is a kind of machine
learning, not a fourth family.

```
   ┌──────────────────────── ARTIFICIAL INTELLIGENCE ────────────────────────┐
   │                                                                         │
   │   ┌──────────────────┐        ┌──────────────────────────────────────┐  │
   │   │   RULE-BASED     │        │        MACHINE LEARNING              │  │
   │   │                  │        │                                      │  │
   │   │ a human writes   │        │  spam filter · face unlock           │  │
   │   │ the if-then      │        │  recommendations · translation       │  │
   │   │ steps            │        │                                      │  │
   │   │                  │        │   ┌──────────────────────────────┐   │  │
   │   │ thermostat       │        │   │      GENERATIVE AI           │   │  │
   │   │ vending machine  │        │   │  makes new content           │   │  │
   │   │ alarm clock      │        │   │  chatbot · image maker       │   │  │
   │   │                  │        │   └──────────────────────────────┘   │  │
   │   └──────────────────┘        └──────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────────────────────┘
```

So when you sort a system, ask two questions **in this order**:

1. Did a human write the rules, or did the machine find them from examples?
2. If it found them — does it output a label from a menu, or new content from a blank page?

### Narrow, and why every real system is

Here is the thing films get wrong.

> **Narrow AI** — a system that can do exactly one job and is completely blank outside it.
>
> **General AI (AGI)** — a hypothetical system that could learn and do *any* job a person can,
> switching between them the way you do. **It does not exist.**

**The analogy:** imagine a chef who makes the finest samosa on Earth. Crisper than yours, perfect
every time. Now ask her to fix a bicycle. She can't. Teach algebra? Can't. Make a *pizza* — also
dough, also folded, also baked? Can't, because she only ever learned samosas.

Every real AI system today is that chef.

![Narrow AI versus general AI](../figures/fig-w03-2-narrow-vs-general.svg)

*Figure 3.2 — One blade out, and nothing else in the handle.*

| System | Number of jobs it can do |
|---|:--:|
| AlphaGo | 1 (play Go) |
| Face unlock | 1 (is this the owner's face?) |
| Spam filter | 1 (spam or not) |
| Google Translate | 1 (turn text in language A into language B) |
| A modern chatbot | **Looks like many — but it is 1:** guess the next chunk of text |
| **Your student** | effectively unlimited |

That last row is why "narrow" matters. Your student is reading this, and could stop and make toast,
comfort a friend, learn to juggle, and argue about a cricket match. No machine can do that set.

**The chatbot row is the one to think about before class**, because it is the row that will be
challenged. A chatbot appears to do a hundred jobs: it writes poems, explains photosynthesis,
translates Spanish, plans a party. But it is doing one job over and over — *guess what text comes
next* — and the hundred jobs are what that one job looks like from outside. Week 28 has the student
tally this by hand with no magic at all. Today you only need to say the sentence and mean it.

### Confidence is not correctness

> **Confidence score** — how strongly the model prefers one answer over the others. A number, not a
> promise.

When a model classifies something, it doesn't produce one answer. It produces a number for every
option and they add up to 100%.

![A confidence score is a preference, not a promise](../figures/fig-w03-5-confidence-not-correctness.svg)

*Figure 3.3 — 94% sure. Still a fox.*

Say this sentence to yourself until it is automatic, because you will need it in about eight
different weeks this year:

> **A confidence score is how strongly the model prefers a class. It is not the probability that the
> model is right.**

A model can be 99% confident and completely wrong. It happens most often on inputs unlike anything it
trained on — which is exactly when you most need it to hesitate, and exactly when it doesn't.

**The concrete version for today:** Quick, Draw! doesn't show you numbers, but it does something
better — it calls out its guesses **in order**. *"Is it a circle? … is it a wheel? … it's a clock!"*
That order **is** the confidence ranking, spoken out loud. The first thing it says is the thing it
prefers most. And it is often wrong twice before it's right, at high confidence each time.

### The thing today's AI genuinely cannot do

Today's AI **cannot reliably know when it doesn't know.**

A person who has never seen a Pomeranian says *"I'm not sure what that is."* A model trained on cats
and dogs, shown a Pomeranian, says *"dog — 94%"*. Shown a **chair**, it still says *"dog — 71%"*,
because *chair* is not on its menu. There is no option for "that's outside my world".

This surprises people because the confident tone reads like understanding. It is not. It is a number
coming out of a machine that was only ever built to pick from a menu.

The generative version of the same problem has a name: a **hallucination** — a confident, fluent,
completely invented answer. You'll produce one live today. Have this sentence ready:

> *"It's not lying. Lying needs you to know the truth and choose to say something else. It's guessing
> what a good answer would look like, and sometimes a good-looking answer isn't a true one."*

### The two misconceptions you will meet today

**Misconception 1: "AI means chatbots."**

Chatbots got all the news coverage, so for most people "AI" now means "AI that talks". Your student
will over-sort into *generating*. The fix is the counting test: how many possible outputs? Face
unlock has two. Spam has two. YouTube's feed picks from a list of existing videos it did not create.
None of those generate anything.

**Misconception 2: "AGI is nearly here / it's already here."**

Not a silly belief — some serious people expect it eventually — but it is not true today. The honest
line: *"There is not one system anywhere that can do a second job it wasn't built for. Not one. And
whether there ever will be is genuinely argued about by people who know far more than I do."*

### How deep to go — and where to stop

**Go this deep today:** the three families, the counting test, the narrowness proof as a *method*,
and confidence-as-preference.

**Stop before:**
- **How a chatbot actually predicts text.** Week 28–29. One sentence today: *"it guesses the next
  chunk of text, over and over."*
- **Why the same prompt gives different answers.** Week 29, with a die. If asked today:
  *"it picks its next word a bit randomly. You'll do it with a die in Week 29."*
- **Measuring accuracy.** Weeks 19–22. No percentages of your own today.
- **Bias and who's missing.** Week 31. If the student notices Quick, Draw! is worse at things drawn
  differently in different countries — and some do — that is a superb observation. Write it on the
  Questions We Owe page and tell them it has a whole week.

---

## 🧰 Prep Checklist

### 10 minutes the night before

- [ ] **Open `quickdraw.withgoogle.com` on the laptop you'll actually use.** Click *Let's Draw!* and
      do one drawing. Check the sound works — the spoken guesses are half the value.
- [ ] **Open your chosen chatbot and check you can log in.** Do not test the fake-film prompt in
      advance on the same account — you want a fresh conversation tomorrow.
- [ ] **Decide which chatbot.** Any one an adult has approved. Have a second one available as a
      backup; behaviour varies a lot between them and between weeks.
- [ ] **Print the score card** (Figure 3.4) or rule up six rows on paper.
- [ ] **Count out 15 sticky notes.** Put them where you can reach them without leaving the table.
- [ ] **Find the student's Week 1 Spotter's Log.** They wrote eight rows. Today they get to fifteen.
- [ ] **Read the fallback table below.** Labs fail; the ones that fail well have a paper version.

### 5 minutes before class

- [ ] Both tabs already open, logged in, ready. Do not spend lesson time on a login screen.
- [ ] Every other camera or drawing app quit.
- [ ] 15 sticky notes, pencil, score card, Week 1 log on the table.
- [ ] Board space cleared, or a large sheet, marked into three columns: **RULES · LEARNED ·
      GENERATING**, with a narrow fourth column headed **DEFEND THESE**.
- [ ] The sentence *"a confidence score is a preference, not a promise"* somewhere you can see it.

### If something fails

| Problem | Fallback |
|---|---|
| **Quick, Draw! won't load** | Play **20 questions** with you as the machine. You may only answer from a fixed menu of five animals. Then they ask you something outside the menu and you must still answer one of the five. That is the narrowness proof, unplugged, and it works. |
| **No sound** | The guesses also appear as text on screen. Read them aloud yourself. |
| **The chatbot refuses the fake-film question** | **Excellent — say so out loud and praise it.** Then run Backup B below, which always works. |
| **No internet at all** | Run the whole lesson on paper. Round 1 → the 20-questions game above. Round 2 → read the pre-written invented paragraph in §The Activity aloud and have the student mark which details are checkable. Round 3 → the sticky-note board needs no internet at all and is the biggest chunk anyway. |
| **Only 45 minutes** | Hook (5) + Concept parts A and B (12) + Round 1 Quick, Draw! (13) + Round 3 board (15). Move Round 2 (the chatbot) into a five-minute demo at the start of Week 4. |

---

## ⏱️ The Lesson, Minute by Minute

| Time | Minutes | Segment | What happens |
|---|---|---|---|
| 0:00–0:08 | 8 | 🪝 **Hook** | The samosa chef. The AlphaGo callback. "Name one thing it can't do." |
| 0:08–0:26 | 18 | 🧠 **Concept** | Generating vs picking · narrow vs general · confidence as preference |
| 0:26–0:40 | 14 | 🔍 **Worked Example Together** | **Round 1** — Quick, Draw!: six drawings, score card filled in, then the narrowness proof |
| 0:40–1:00 | 20 | 🎲 **Activity** | **Round 2** — catch the chatbot inventing (8 min) · **Round 3** — build the 15-note board (12 min) |
| 1:00–1:10 | 10 | 🔑 **Wrap & Assign** | Three hardest calls into the defend column · vocabulary · homework, step one |
| | **70** | | |

**For 60 minutes:** cut Round 2 to a four-minute demo (you type, one prompt, one follow-up, no
discussion) and cut the concept block's confidence section to the single sentence plus Figure 3.3.

**For 75 minutes:** run the *Three-Test Narrowness Proof* in §Differentiation — a proper little
experiment with a written conclusion.

---

### 🪝 Segment 1 — Hook (0:00–0:08)

**Do this:** Laptop closed. Nothing on the table but the samosa story.

**Say this:**

> "Imagine a chef. Not a good chef — the *best* chef. She makes the finest samosa on Earth. Crisper
> than yours, better than mine, perfect every single time, a thousand a day, never a bad one.
>
> Now ask her to fix a bicycle.
>
> She can't. Not badly — at all. She has no idea what a spanner is.
>
> Okay, ask her to teach algebra. Can't. Ask her to make a **pizza** — which is also dough, also
> flattened, also baked, also has stuff on it. She cannot make a pizza. She only ever learned
> samosas.
>
> Right. Now remember AlphaGo from two weeks ago — the program that beat the best human in the world
> at Go? It couldn't play checkers. Couldn't tell you what a Go board is made of. Ask it 'are you
> tired?' and it would reply with a Go move, because a Go move is the only thing it can produce.
>
> **Every single AI system that exists today is that chef.** Superb at one thing. Blank at everything
> else. Not one exception, anywhere in the world, right now.
>
> And today you're not going to take my word for it. You're going to prove it, on a real system, with
> your own hands, in about twenty minutes."

**Ask this:**

> **"You use YouTube. Name one thing YouTube's recommendation system cannot do."**

- **Hoping for:** anything outside picking videos — *"it can't tell me what the video's about"*,
  *"it can't make a video"*, *"it can't answer a question"*.
- **If they say "it can't recommend good videos":** funny, and worth a laugh, then push:
  *"That's it doing its job badly. I want something it can't do **at all**."*
- **If they say "nothing, it can do anything":** perfect setup. *"Can it tell you what 7 times 8 is?
  Can it make you a sandwich? Can it tell you whether your homework is finished?"* Then:
  *"So it does exactly one job and it's blank everywhere else. That has a name, and we're doing it
  in four minutes."*

---

### 🧠 Segment 2 — Concept (0:08–0:26)

#### Part A — picking versus generating (0:08–0:14)

**Say this:**

> "Last week's spam filter — how many different things could ever come out of it?"

Wait for it. The answer is **two**.

> "Two. `spam` or `not spam`. That's the whole menu. It could run for a hundred years and it would
> never produce a third thing.
>
> When a system picks from a fixed menu like that, we say it produces a **label**.
>
> Now — a chatbot writing a poem. How many different things could come out of *that*?"

- **Hoping for:** *"loads"* / *"infinite"* / *"anything"*.
- **If they try to count:** *"Could it write a poem nobody has ever written before?"* Yes. *"Then
  there's no list."*

> "Right. No menu. A blank page. That's a different kind of machine and it has a name: **generative
> AI** — a system that makes new content instead of picking a label off a list.
>
> Think of a school test. Multiple choice: four boxes, tick one. That's labelling. Essay question:
> blank page, write three hundred words nobody has ever written in that order. That's generating.
> Same you, same brain, two completely different kinds of answer."

**Do this:** Show Figure 3.1 and write the test on the board:

```
   COUNT THE POSSIBLE OUTPUTS
     short fixed list  →  picking a label
     blank page        →  generating
```

**Say this — and do not skip this bit, it is the correction people never get:**

> "One thing people get wrong constantly. Generative AI is not a *separate* thing from machine
> learning. It's **inside** it. A chatbot learned from examples in exactly the same way the spam
> filter did — it just produces a blank page instead of a menu. Same family. Different output shape."

#### Part B — narrow and general (0:14–0:20)

**Say this:**

> "Two more words, and one of them describes something that doesn't exist.
>
> **Narrow AI** is a system that does exactly one job and is completely blank outside it. That's the
> samosa chef. That's every system you have ever touched.
>
> **General AI**, or **AGI**, would be a system that could learn and do *any* job a person can,
> switching between them the way you do. Making toast, then comforting a friend, then learning to
> juggle, then arguing about cricket.
>
> **It does not exist.** Not a prototype, not a secret one, not nearly. Zero."

**Do this:** Show Figure 3.2. Point at the dashed knife.

![Narrow AI versus general AI](../figures/fig-w03-2-narrow-vs-general.svg)

*Figure 3.2 — I drew the right-hand one dashed on purpose. You can't draw a solid picture of a thing
that isn't there.*

**Ask this — the objection you want them to raise:**

> **"But a chatbot writes poems AND explains science AND translates Spanish. Isn't that lots of jobs?"**

If they don't raise it, raise it yourself and then answer it:

> "It looks like a hundred jobs. It's one. The job is: **guess what chunk of text comes next.** A poem
> is text. An explanation is text. A translation is text. It's doing one thing over and over, and
> those hundred jobs are what that one thing looks like from the outside.
>
> I'm not asking you to believe me. In Week 28 you're going to build one by hand with tally marks and
> no computer, and you'll see the whole engine. For now: write down that you're not sure, and hold
> me to it."

#### Part C — confidence is not correctness (0:20–0:26)

**Say this:**

> "Last idea, and it's the one I'd keep if I could only keep one thing from today.
>
> When a model gives an answer, it doesn't just say 'dog'. It gives a number for every option, and
> they add up to a hundred. Like this."

**Do this:** Show Figure 3.3.

![A confidence score is a preference, not a promise](../figures/fig-w03-5-confidence-not-correctness.svg)

*Figure 3.3 — Dog 94, fox 4, cat 2. The photo was a fox.*

**Say this:**

> "Dog, ninety-four percent. Fox, four. Cat, two. Ninety-four plus four plus two is a hundred. They
> always add to a hundred.
>
> That number is called a **confidence score**. And here's the trap.
>
> Ninety-four percent does **not** mean 'right ninety-four times out of a hundred'. It means 'dog is
> the one I'm leaning towards hardest'. That's all. Leaning hard and being right are two completely
> separate things.
>
> That photo was a fox."

**Ask this:**

> **"If a model says 'dog, 99%', how sure should you be that it's a dog?"**

- **Hoping for:** *"not that sure"* / *"you can't tell from that number"*.
- **If they say "99% sure":** the exact trap, and it's the right mistake to make. Don't say wrong.
  Ask: *"How would you check?"* → you'd have to look at the photo. *"So what did the number tell
  you?"* → how much the machine liked its own answer. Nothing more.
- **The line to leave them with:** *"There's a place this goes badly wrong, and you'll see it in
  twenty minutes when a computer tells us about a film that does not exist, in complete sentences,
  without blinking."*

---

### 🔍 Segment 3 — Worked Example Together: Round 1 (0:26–0:40)

**Do this:** Before you open the laptop, say the privacy line. Out loud. Every time.

**Say this:**

> "One thing before we start, and I'm telling you because you're allowed to know. Everything you draw
> in this game gets sent to Google and added to a big public pile of drawings that anyone can
> download. That's fine — we're drawing clocks and ladders, not names and not faces — but you should
> know it, and you should ask that question about every tool anyone ever hands you. Deal?"

**Do this:** Open `quickdraw.withgoogle.com`. Put the score card in front of the student. **They
draw; you write.** Swapping that round wastes time and they'll draw better if their hands are free.

![A Quick, Draw! score card for six rounds](../figures/fig-w03-1-quickdraw-scorecard.svg)

*Figure 3.4 — A filled-in score card. Yours will look different; the shape is what matters.*

**Say this:**

> "Six drawings, twenty seconds each. Draw as well as you can. And listen — it talks while you draw.
> It calls out its guesses out loud, in order, as your lines appear. **The order is the important
> bit.** The first thing it says is the thing it likes most. That's the confidence score, spoken."

**Do this:** For each round, write down: what it asked for · every guess it called out, **in order**
· did it get it · roughly how many seconds. Six rounds takes about six minutes including the
between-round screens.

**Ask this after round 3, mid-game:**

> **"It said 'circle' and then 'wheel' before it said 'clock'. Was it wrong twice?"**

- **Hoping for:** *"Sort of — it changed its mind"* or *"it was guessing."*
- **The point:** *"It wasn't hedging. At the moment it said 'circle', circle was its top answer — it
  was confident about circle. Then more lines appeared and its top answer changed. Confidence moves
  around, and at every single moment it sounds certain."*

**Do this — now the narrowness proof. This is the objective, so do it properly.**

**Say this:**

> "Right. Six rounds, and it did pretty well. So here's the real experiment.
>
> I don't want to know what it's *good* at. I want to find the edge. I want you to design a task that
> is **one small step sideways** from its job — not something ridiculous like asking it to do maths,
> but something a person would find easy and obviously related.
>
> You design it. Not me. What are you going to try?"

Give them thirty seconds. If they're stuck, offer these as a menu but make them choose:

| Sideways task | What actually happens | What it proves |
|---|---|---|
| Draw **two things at once** (a cat *and* a hat) | It only ever scores against the one prompt it gave. It ignores the other thing entirely. | It isn't looking at your picture. It's matching against one target word. |
| Draw the prompt **upside down** | Usually fails completely, even on a good drawing | It learned what people's *strokes* look like, not what the object is |
| Asked for "dog", draw a **cat** | It guesses "dog" wrongly for a while, then goes silent. **It never says "cat".** | It cannot volunteer what it actually sees. It only checks against the one prompt. |
| Asked for "house", **write the word** H-O-U-S-E | "zigzag", "squiggle" | Meaning is completely outside its world |
| Asked for "sun", draw a **perfect circle** | "circle", "clock", "donut" — no sun until you add rays | It knows what people's sun *drawings* look like, not what a sun is |

**Ask this after the failure:**

> **"So what is this thing's actual job? Not what the website says — what your evidence says."**

- **Hoping for** something in the direction of: *"it checks whether my lines look like other people's
  lines for one particular word."*
- **The model answer to build towards, and it is worth writing down:**

> **"Quick, Draw! does one job: given some pen strokes and one target word, it scores how closely
> those strokes match the strokes other people drew for that same word. It is not recognising
> objects."**

- **If they say "it's just bad at kangaroos":** the best wrong answer available, and worth taking
  seriously. *"Maybe. How would we tell the difference between 'bad at kangaroos' and 'only matching
  strokes'?"* → the cat test settles it: a system that recognises objects would say *"that's a cat"*.
  This one says nothing at all, because *cat* isn't the word it was checking.

---

### 🎲 Segment 4 — Activity: Rounds 2 and 3 (0:40–1:00)

Full instructions in the next section. The minute-by-minute:

#### Round 2 — catch it inventing (0:40–0:48)

**Do this:** **You type.** Student watches and writes. Say so explicitly — it's a rule, not a slight.

**Say this:**

> "I'm at the keyboard for this one — that's a rule in this course for anything that talks back.
> Your job is to watch and write down what happens.
>
> I'm going to ask it about a film. The film does not exist. I made it up. Watch what it does."

**Type this, exactly:**

```
Tell me about the 1987 Australian film "The Glass Kangaroo of Wollongong",
including its director and how it was received.
```

**Then read the answer aloud** and have the student fill in the four-row table in the workbook.

**Ask this:**

> **"How many things in that paragraph could we go and check?"**

Count them together and point at each: the director's name, the year, the studio, the awards, the
review quote. Four or five checkable claims, all invented, all in complete confident sentences.

**Then type this follow-up:**

```
Was that film real? Answer with just yes or no.
```

**Ask this:**

> **"It just changed its story. What does that tell you?"**

- **The answer:** it never knew in the first place. It produced text that *looked like* the right kind
  of text. When challenged, it produced different text that also looked right. Neither answer came
  from knowing anything.

**Say this:**

> "That has a name — a **hallucination**. And here's the sentence I want you to remember:
>
> *It isn't lying. Lying means you know the truth and you choose to say something else. It doesn't
> know the truth. It's guessing what a good answer would look like, and sometimes a good-looking
> answer isn't a true one.*
>
> And notice — it didn't hedge. It didn't sound unsure. It sounded exactly as confident as when it's
> right. Which is why 'it sounded confident' is worth **nothing**."

**If it refuses and says the film doesn't exist:** genuinely good behaviour. Say so out loud —
*"That's the honest answer and it's better than what I expected"* — then run **Backup B**:

```
(in one tab)  Explain in 100 words why the sky is blue.
(new tab, fresh chat, same question)  Explain in 100 words why the sky is blue.
```

The two answers will differ, often a lot. **Ask:** *"If it were looking the answer up, would it come
back different every time?"* No. Different every time is the signature of **generating**, and that
proves the point just as well.

#### Round 3 — build the board (0:48–1:00)

**Do this:** Laptop closed. Sticky notes out. Three columns on the table or wall.

**Say this:**

> "Fifteen systems. Real ones, from your actual life, that you actually touched. You've already got
> eight from two weeks ago — get them out, they count.
>
> One system per sticky note. Be specific: not 'my phone', but 'my phone's keyboard suggestion bar'.
> Then stick it in a column: **rules**, **learned**, or **generating**.
>
> Say the reason out loud as you stick it. Every one."

Give them ten minutes. Your job is to ask *"what made you put that there?"* about five times, and to
say nothing else.

![A finished AI Spotter's Log board](../figures/fig-w03-3-spotters-log-board.svg)

*Figure 3.5 — What a finished board looks like. Fifteen notes, three columns, three pinned for
defending.*

---

### 🔑 Segment 5 — Wrap & Assign (1:00–1:10)

**Do this:** Add the fourth column: **DEFEND THESE**.

**Say this:**

> "Now the most valuable two minutes of the lesson. Pick the **three notes you were least sure
> about** and move them into this column.
>
> Least sure. Not most interesting, not most impressive. The three where you thought 'hmm' and
> stuck it down anyway. Those three are your homework."

**Ask this — the wrap question:**

> **"Give me today's big idea in one sentence, your own words."**

- **Hoping for:** *"Every AI does one job and is useless just outside it, and some of them make new
  stuff instead of picking from a list."*
- **If they only say the narrow half:** *"And the other new thing today?"*
- **If they say "AI isn't as good as people think":** true-ish, but too vague. *"Say it so a
  seven-year-old could use it tomorrow."*

**Do this:** Vocabulary into the notebook, their words.

| Term | The one-line meaning |
|---|---|
| **generative AI** | a system that makes new content instead of picking an answer off a fixed list |
| **narrow AI** | a system that does exactly one job and is blank outside it — this is all of them |
| **general AI (AGI)** | an imaginary system that could do any job a person can. It does not exist. |
| **confidence score** | how strongly the model prefers its answer — a number, not a promise it's right |

**Do this:** Read the homework aloud. Check step one only: they can name the three notes in the
DEFEND column without looking.

**Say this:**

> "Next week everything changes. For three weeks we've asked *who wrote the rule?* From now on we ask
> a different question: **where did the examples come from?** Because everything a machine knows
> arrived as a table — rows and columns, like a register — and once you can see the table, you can
> see what's missing from it."

---

## 🎲 The Activity, In Full

### AI Detective — three rounds

**What it is:** an evidence-gathering lab. Round 1 finds the edge of a learned system. Round 2
catches a generative system inventing. Round 3 turns the student's own day into sorted, defensible
data.

**Time:** 34 minutes total in class (14 + 8 + 12). Comfortably fills 50 if you have it.

**Materials:** laptop with sound · score card · 15 sticky notes · Week 1 Spotter's Log · pencil ·
three columns marked out on a table, wall or large sheet · a fourth narrow column headed DEFEND
THESE.

### Round 1 — Quick, Draw! and the narrowness proof (14 min)

**Setup**
1. Say the privacy line **before** opening the site. Every time. It is fifteen seconds.
2. Student at the trackpad, you with the pencil.
3. Score card in front of you both.

**Rules**
- Six drawings, twenty seconds each, drawn as well as they can.
- You record **every guess it calls out, in order** — this is the data, not just whether it won.
- After six rounds, the student **designs their own sideways task**. Do not design it for them; offer
  the menu only if they're stuck after thirty seconds.
- The failure gets written down as evidence, in the same table.

**What "finished" looks like:** six rows filled in, at least one wrong guess recorded before a right
one, one designed sideways task with its outcome, and a written one-sentence statement of what the
system's real job is — based on their evidence, not the marketing.

### Round 2 — catch it inventing (8 min)

**Setup**
1. **You are at the keyboard.** State it as a rule.
2. Fresh conversation, not one you tested last night.
3. Student has the four-row table ready.

**The prompt**

```
Tell me about the 1987 Australian film "The Glass Kangaroo of Wollongong",
including its director and how it was received.
```

**The follow-up**

```
Was that film real? Answer with just yes or no.
```

**The four rows the student fills in**

| Question | Their answer |
|---|---|
| Did it invent details? | |
| How confident did it sound, 1–5? | |
| Did it warn you at all? | |
| Would you have believed it if you didn't already know? | |

**Backup B — if it refuses** (this one always works and teaches the same point):
same question, twice, in two fresh chats. Compare. Different answers = it is generating, not
retrieving.

**Backup C — no internet.** Read this aloud yourself, deadpan, and have them mark every checkable
claim:

> *"The Glass Kangaroo of Wollongong (1987) is a quietly regarded Australian drama directed by
> Marion Hollis, her second feature after the well-received Coast Road. Shot over eleven weeks in New
> South Wales, it follows a glassblower's daughter returning to her home town. It won the Silver
> Boomerang at the Adelaide Film Festival and holds a warm reputation among Australian critics, with
> The Age calling it 'small, salt-worn and completely honest'."*

Every proper noun in that paragraph is invented. Ask them to circle every claim they could check, then
say: *"That's what a machine that has never heard of a thing sounds like."*

**What "finished" looks like:** the four rows filled in, at least three specific invented details
named out loud, and the student able to say why *"it sounded confident"* is not evidence of anything.

### Round 3 — the fifteen-note board (12 min)

**Setup**
1. Three columns marked: **RULES · LEARNED · GENERATING**.
2. Fifteen sticky notes, pencil.
3. Week 1's eight rows in front of them — those transfer straight across.

**Rules**
- One system per note.
- **Specific or it doesn't count.** "My phone" is rejected; "my phone's keyboard suggestion bar" is
  accepted.
- Reason spoken aloud before the note is stuck down.
- Aim for a spread across four zones so they don't end up with fifteen phone apps:

| Zone | Where to look |
|---|---|
| 🏠 Home | TV recommendations, smart speaker, washing machine cycles, thermostat, microwave, doorbell |
| 📱 Phone | keyboard, photo search, face unlock, maps, spam folder, video feed, music shuffle, translate |
| 🏫 School | attendance system, library scanner, plagiarism checker, timetable, school bell |
| 🛣️ Street | traffic lights, self-checkout, ATM, automatic doors, number-plate cameras, bus arrival board |

**What "finished" looks like:** fifteen notes placed, **at least two in each column**, and three notes
moved into DEFEND THESE.

> **💡 Try this:** if they can't find a single *generating* system, that is a real and interesting
> result, not a failure. Say so: *"Then write that down — 'I met no generative AI today.' That's an
> honest finding and it's true for a lot of people. Generative AI is the loudest kind and not the
> most common kind."*

### Variation — easier

- **Ten notes instead of fifteen**, and drop the four-zone requirement.
- **Two columns instead of three** (rules / learned), then introduce *generating* with a single
  example — the chatbot from Round 2 — and let them add just one note to it.
- **Give them the sideways task** in Round 1 rather than making them design it. You lose part of
  objective 2 but you keep the whole demonstration.
- **Skip Round 2 entirely** and use Backup C, the read-aloud paragraph. It is shorter, calmer, and
  makes the same point.

### Variation — harder

- **The Three-Test Narrowness Proof.** A real little experiment, written up properly:

  | Request | What I expected | What it actually did |
  |---|---|---|

  Three rows, three genuinely different sideways tasks, then one sentence stating the system's real
  job *based only on the evidence in the table*. This is the Module 1 stretch exercise and it is
  excellent Grade 6 work.
- **Split a product across two columns.** Take one note — the video doorbell, or autocorrect — and
  make them physically tear it in half and put each half in a different column with its own reason.
  Genuinely sophisticated.
- **The confidence hunt.** Find a real system that shows you a number: a weather app's "70% chance of
  rain", a photo app's face-match suggestions, a spam folder's "probably spam" banner. Then ask:
  **"70% chance of rain — is that a confidence score or a probability? How could you tell?"**
  (Genuinely subtle. Weather forecasts are actually *calibrated* — over many days, it really does rain
  on about 70% of the 70% days. Model confidence scores usually are not calibrated at all. That is a
  distinction most adults have never drawn.)

### If you have 2–6 learners

Round 1: one drawer, everyone else records — then rotate. Round 2: each learner writes a prediction
of what the chatbot will do **before** you press enter, folded and face down. Round 3: each learner
builds their own board, then swaps and plays **official sceptic** on someone else's, challenging any
note they'd have placed differently. Independent challenge is the real skill and it is more fun than
sorting your own.

---

## ❓ Questions Students Ask This Week

**1. "Is ChatGPT the same thing as AI?"**

No — it's one kind, the way a labrador is one kind of animal. The spam filter on your email is AI.
The thing that picks your next video is AI. Face unlock is AI. Chatbots are the loudest kind right
now, not the only kind and not the most common kind. Most of the AI you touched today didn't say a
word to you.

**2. "Can it lie?"**

Lying means knowing the truth and choosing to say something else. It doesn't know the truth, so no.
But it will absolutely say false things with total confidence, which can hurt you just as much. We
call that a hallucination. And the important bit: it sounds *exactly* the same when it's right.

**3. "Why did it make up a director's name instead of saying it didn't know?"**

Because "I don't know" is not the kind of thing it was built to produce. Its whole job is to make
text that looks like the right kind of text. A paragraph about a film has a director's name in it, so
it produced a director's name. That's not it being sneaky — that is the machine working exactly as
designed on a question where the plausible answer and the true answer are different things.

**4. "So is it actually intelligent, or not?"**

Depends entirely on what you mean, and that's not a dodge — it's the real answer. Can it do a job
that used to need a person's judgement? Yes, often brilliantly. Does it understand what it's doing?
There is nothing in there having a time. Does it know when it's out of its depth? No, and that's the
dangerous bit. Pick your definition and the answer follows.

**5. "When will AGI exist?"**

**Nobody knows for sure, and here's why that's an honest answer rather than me dodging.** Serious,
well-informed people give answers ranging from five years to never, and they are all looking at the
same evidence. We can't predict it because we don't actually know what's missing — if we knew what
was missing, someone would build it. What I can tell you for certain is what's true *today*: there is
not one system anywhere that can do a second job it wasn't built for. Anyone who tells you they know
the date is guessing, including the confident ones. Especially the confident ones.

**6. "If it says 99%, is it right 99 times out of 100?"**

No, and this is one of the most useful things in the whole year. That number is how strongly the
model *prefers* that answer — it's the biggest number in a list that adds up to 100. It is not a
prediction about how often it's correct. Models are most confidently wrong on things unlike anything
they trained on, which is exactly when you'd most want them to hesitate.

**7. "Could someone build a general AI in secret?"**

Extremely unlikely, and here's the reasoning rather than just the answer: these systems need
enormous amounts of electricity, thousands of specialised chips, and hundreds of people. That leaves
tracks — power bills, chip orders, job adverts, people leaving. And the companies building the
biggest systems have every commercial reason to *announce* progress, not hide it. It's a fun idea and
the evidence points the other way.

**8. "Is Quick, Draw! cheating by knowing the word already?"**

That is a *superb* question and the answer is essentially yes — and noticing it is the whole point of
the round. It isn't looking at your drawing and working out what it is. It's checking how well your
strokes match other people's strokes **for one word it already picked**. That's a much smaller job
than "recognise this drawing", and the cat test proves it: draw a cat when it asked for a dog and it
never once says "cat". It can't. Cat isn't the question it's answering.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The chatbot answers honestly and refuses the fake film | Newer models handle obvious fake-entity prompts better than they used to | **Praise it out loud** — honest refusal is the behaviour we want and the student should see an adult approve of it. Then run Backup B (same question, two fresh chats). Different answers prove *generating* just as well. |
| The student wants to keep chatting to the bot | It's the most engaging thing on the table by a distance | Name it and time-box it: *"Fair. Two minutes, my hands on the keyboard, and then we're closing it."* Then close it. Curiosity is not the enemy but the board is the objective. |
| Everything ends up in the *generating* column | "AI" now means "chatbot" for most people | Take one wrong note — face unlock. *"What are the possible answers face unlock can give?"* → two. *"Is two a blank page?"* One note re-sorted properly resets the whole board. |
| They can't find fifteen and stall at nine | They're only looking at phones | Read the four-zone table aloud. *"Did you walk through a door today? Did a bell ring? Was there a traffic light?"* Six more arrive in ninety seconds. |
| Round 1 goes brilliantly and eats 25 minutes | Quick, Draw! is genuinely fun | Set a visible timer before you open it. When it goes, close the laptop mid-round if you must. **The board is the objective; the game is the demo.** |
| "It got the kangaroo wrong so it's rubbish" | Judging a system by whether it wins | Redirect from *good/bad* to *what does the failure tell us*: *"It got five out of six. It's not rubbish. The question isn't whether it's good — it's what it's actually doing. What did the kangaroo failure show you that the clock success didn't?"* |
| The student is upset or unsettled by the hallucination | Discovering that a confident adult-sounding thing invents facts is genuinely disorienting at 11 | Take it seriously; don't jolly it along. *"You're right to find that unsettling. That's why we're learning to check instead of learning to trust. That reflex — 'how would I check that?' — is the most useful thing you'll get out of this whole year."* |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** Part C of the concept block. Teach confidence *inside* Round 1 instead, using the spoken
guess order — *"the first thing it says is what it likes most"* — which is more concrete than any
bar chart.

**Cut:** Round 2 down to Backup C, the read-aloud paragraph. It is calmer, needs no internet, and
makes the identical point in three minutes.

**Reteach like this:** if picking-vs-generating isn't landing, drop AI completely for three minutes
and use a restaurant. *"Here's a menu with four things on it. Point at one."* — that's picking.
*"Now invent a new dish that isn't on the menu."* — that's generating. Then: *"Face unlock has a
menu with two things on it. A chatbot has no menu."*

**Simplify the board:** ten notes, two columns, no zone requirement. Ten sorted notes with real
reasons beats fifteen guessed ones every time.

### If they are flying

- **The Three-Test Narrowness Proof** written up as a proper table with a conclusion sentence.
- **"Find a system that's in two columns at once."** Then physically tear the note in half. (Best
  answers: the keyboard suggestion bar — it learned from examples *and* it generates text; a video
  doorbell — rules for motion, learned for "that's a person"; a self-checkout — rules for the
  barcode, possibly learned for the camera.)
- **The calibration question**, in §Variation — harder. Genuinely university-level and completely
  reachable with a weather app.
- **The hardest question available this week:** *"AlphaGo could only play Go. A chatbot can write
  about Go, and cricket, and photosynthesis. Is a chatbot still narrow?"* There is no clean answer
  and that is the point. The strongest position: it's one job (predict text) done so broadly that the
  word "narrow" strains — but it still cannot learn to ride a bicycle, cannot check whether it's
  right, and cannot do anything that isn't producing text. Push them to argue both sides and pick
  one. This is real thinking and it deserves real time.

### If they won't engage today

- **Open the laptop first.** No hook, no concept. *"Draw six things. I'll write."* Play. Teach the
  ideas afterwards out of what happened — you'll have real data to teach from and they'll have had
  fun first.
- **Let them break it.** Reframe the whole lesson as *"your job today is to make the computer look
  stupid, and you have to write down how you did it."* That is genuinely what the narrowness proof
  is, and 11-year-olds find it irresistible.
- **Shrink to one target.** If nothing else happens, land this: *every AI does one job and is blank
  one step sideways.* One demonstrated failure with the student's own hands is enough. The board can
  become homework.
- **Skip the chatbot** if they're dysregulated. Round 2 involves discovering that a confident thing
  invents facts, and that lands badly on a bad day. Do it in Week 4 instead.

---

## ✅ Assessing Understanding

### Check 1 — picking vs generating (objective 1)

> **"Face unlock, or a chatbot writing a poem. Which one is generating, and how do you know?"**

Good answer: the chatbot, **because you can count face unlock's answers (two) and you can't count
the chatbot's**. The *counting* is what you're marking. "Because the chatbot is cleverer" is a ✗ —
reteach with the menu.

### Check 2 — the narrowness proof (objective 2)

> **"Design me a test — right now, out loud — that would prove Google Translate is narrow."**

Good answers: ask it what the sentence *means*; ask it whether the sentence is true; ask it to
translate a picture; ask it whether the sentence is polite. Any task **one step sideways from
translating text**. A weak answer ("ask it to make a sandwich") shows they've got *narrow* but not
*one step sideways* — the sideways-ness is the skill, because it rules out "well it just wasn't
designed for that".

### Check 3 — confidence (objective 3)

> **"A model says 'this is a wolf, 96%'. Finish this sentence: that means the model…"**

Good answer: *"…prefers wolf more strongly than anything else"* or *"…is leaning hardest towards
wolf."* Not-yet answer: *"…is nearly certain it's right"* or *"…will be right 96% of the time."*

### Mastery scale for this week

| | Level | What it looks like |
|:--:|---|---|
| **1** | Not yet | Thinks AI means chatbots. Cannot say what narrow means. Sorts by vibe. |
| **2** | Emerging | Repeats "narrow means one job" but can't design a test for it. Puts most notes in *generating*. |
| **3** | Developing | Uses the counting test on clear cases. Ran a sideways task you suggested and recorded the failure. Board sorted with 2+ notes in each column. |
| **4** | **Secure — this is the target** | Designed their own sideways task and stated the system's real job from their own evidence. Fifteen notes sorted with reasons. Says a confidence score is a preference, not a promise. |
| **5** | Extending | Splits one product across two columns with reasons. Names what evidence would change their mind on a hard call. Argues the "is a chatbot really narrow?" question from both sides before picking one. |

---

## 📤 Homework to Assign

**Workbook pages: Week 3, sections W3.1 – W3.3.** About 55 minutes. This is the biggest homework of
the term so far — say that out loud so it isn't a surprise.

**Say this:**

> "Three things.
>
> **One — finish the Spotter's Log.** Fifteen rows in the workbook, one per system, each sorted into
> rules, learned or generating. You've got them all on sticky notes already, so this is mostly
> copying — except each row also needs a **one-line reason**. Every reason has to mention either 'a
> person wrote the steps' or 'it must have learned it from examples'.
>
> **Two — defend your three hard calls.** These are the three you moved into the DEFEND column. One
> paragraph each, at least five sentences, and every paragraph must contain all four of these:
>
> 1. What made it hard to classify.
> 2. The evidence **for** your answer.
> 3. The evidence **against** your answer — the honest case for the other side.
> 4. What **one fact** you'd need to look up to be certain.
>
> Number four is the one everyone skips and it's the most valuable. 'I'd need to know whether the
> doorbell can tell a person from a cat' is a real, answerable question. Write real ones.
>
> There's a model defence in the workbook. Read it before you start. Copy its shape, not its words.
>
> **Three — go and interview an adult.** Ask any adult: *what is AI?* Write down **exactly** what they
> said, word for word, even if it's short, even if it's wrong. Then rewrite it honestly underneath —
> same rules as last week, no magic words.
>
> Step one, now: name your three DEFEND notes out loud without looking at the board."

**Marking notes:** the defences are the whole assignment. Mark them and be relaxed about the fifteen
rows. A defence missing point 4 is incomplete — hand it back and ask only for point 4. On the adult
interview, be gentle: most adults say something with "robots" or "smart" in it, and the student
noticing that is the entire exercise. Do not let it become "the adult was stupid" — the honest frame
is *"this is what almost everyone thinks, including me three weeks ago."*

---

## 🔑 Answer Key

### Round 1 — Quick, Draw!

Exact results vary every time, so what follows is a **typical** run and the reasoning that must
appear, not a set of answers to match.

| Round | Prompt | Typical guesses, in order | Got it? | Why |
|:--:|---|---|:--:|---|
| 1 | clock | circle … wheel … clock | ✅ ~3s | Almost everyone draws a clock as a circle with two hands. Thousands of near-identical examples. |
| 2 | sun | circle … donut … sun | ✅ ~5s | Only lands once rays appear — rays are what people's sun *drawings* have. |
| 3 | ladder | zigzag … ladder | ✅ ~2s | Very consistent shape across drawers. |
| 4 | shoe | shoe | ✅ ~2s | Strong, distinctive silhouette. |
| 5 | tree | broccoli … bush … tree | ✅ ~6s | Broccoli and bushes genuinely look like trees when drawn in twenty seconds. |
| 6 | kangaroo | dog … horse … bear … *(nothing)* | ❌ ran out | Nobody agrees how to draw a kangaroo, so its examples are all over the place. |

**"It said 'circle' then 'wheel' before 'clock' — was it wrong twice?"**
Yes, and at each of those moments that guess was its **top** answer — it was confident about
*circle*. More strokes appeared and the top answer changed. Confidence moves, and at every single
moment it sounds certain.

**The sideways tasks and what each proves**

| Task | What happens | What it proves |
|---|---|---|
| Draw two things at once | It scores only against its one prompt and ignores the other object entirely | It is not looking at your picture; it is matching against one target word |
| Draw the prompt upside down | Usually fails on an otherwise good drawing | It learned stroke patterns, not objects |
| Draw a cat when it asked for a dog | Guesses "dog" wrongly, then goes quiet. **Never says "cat".** | It cannot volunteer what it sees. Strongest single piece of evidence in the round. |
| Write the word instead of drawing it | "zigzag", "squiggle" | Meaning is entirely outside its world |
| Perfect circle for "sun" | circle, clock, donut — no sun until rays | It knows drawings of suns, not suns |

**"What is this thing's actual job, based on your evidence?"**

> **Model answer:** *"Quick, Draw! does one job: given a set of pen strokes and one target word, it
> outputs how closely those strokes match the strokes other people drew for that same word. It is not
> recognising objects — it is matching stroke patterns against one stored prompt."*

Why that matters: the marketing calls it *"a neural network learning to recognise doodles"*. Test 3
disproves *recognising*. A system that recognised objects would say "that's a cat". This one says
nothing, because *cat* is not the question it is answering. The student got a truer description than
the marketing by pushing three inches past the edge of the demo — and that is the whole method of
this course.

### Round 2 — the chatbot

**Expected outcome (most likely):** a fluent, confident paragraph containing an invented director, an
invented plot, an invented festival or award, and possibly an invented review quote. No hedging, no
warning.

**"How many things could we check?"** Typically four or five: director's name · year · studio or
festival · award · quoted review. All invented. Count them out loud and point at each — the counting
is what makes it concrete.

**"It just changed its story. What does that tell you?"**
That it never knew in the first place. It produced text that looked like the right kind of text; when
challenged it produced different text that also looked right. Neither answer came from knowing
anything. *(If it does **not** change its story and sticks to "it was real" — even better. Then say:
"So now it's confidently wrong twice. Which of the two answers should we believe?" Neither.)*

**The four rows — model answers**

| Question | Model answer |
|---|---|
| Did it invent details? | Yes — a director's name, a festival award, and a quote from a newspaper, none of which exist. |
| How confident did it sound, 1–5? | 5. It didn't hedge once. |
| Did it warn you at all? | No. Not a word. |
| Would you have believed it? | Yes — and that's the frightening bit. It read exactly like a real film summary. |

**If it refuses instead:** that is honest behaviour and worth naming. The four rows become: *no /
n-a / yes, it told me it couldn't find the film / no.* Then run Backup B and record: *"the same
question gave two different answers in two tabs, so it is producing text rather than looking
something up."*

**"Why did it invent a name instead of saying it didn't know?"** Because a paragraph about a film has
a director's name in it, and its job is to produce text of the right shape. It is the machine working
normally on a question where the plausible answer and the true answer differ.

### Round 3 — the fifteen-note board

A model board. Yours will differ; **the reasons are what you mark, not the notes.**

**RULES — a person wrote the steps (5)**

| # | System | Reason |
|:--:|---|---|
| 1 | Alarm clock, 07:00 | `IF time = 07:00 THEN ring`. Same every day, never surprises anyone. |
| 2 | Microwave 90-second timer | Counting down is not a decision. |
| 3 | Traffic light on a timer | `IF 30 seconds passed THEN amber`. Fixed sequence. |
| 4 | Automatic shop doors | `IF something moves THEN open`. It opens for a stray cat, which is how you know it isn't judging. |
| 5 | Calculator app | One right answer, one exact method. Not even judgement. |

**LEARNED — found the rule from examples (7)**

| # | System | Reason |
|:--:|---|---|
| 6 | Phone face unlock | Nobody could write if-then rules over two million coloured dots. |
| 7 | Email spam folder | It catches new wording nobody could have listed in advance. |
| 8 | YouTube home feed | The pairings came from what billions of people watched, not from a person's list. |
| 9 | Maps arrival time | It uses how long cars actually took on that road just now — learned from data, not a fixed speed limit sum. |
| 10 | Photo app "dog" search | Trained on millions of already-tagged photos. |
| 11 | Spotify autoplay | Learned which song people don't skip after which song. |
| 12 | Voice dictation | Nobody can write rules over sound waves. |

**GENERATING — makes new content (3)**

| # | System | Reason |
|:--:|---|---|
| 13 | Chatbot writing a poem | Blank page. No menu. The poem never existed before. |
| 14 | AI image maker | Unlimited possible pictures. |
| 15 | Keyboard next-word bar | It produces words rather than picking a label — a small blank page, but a blank page. |

**Not-AI notes are fine and expected.** A light switch, a kettle, a bicycle bell. If a student
includes one, don't reject it — write NOT AI beside it and say *"good, that's a correct answer to a
question I didn't ask."*

**"If you found no generative AI at all"** — a legitimate finding. Write it down as a sentence.

### The three defences — full model answers

The student must include all four required points. Here is the standard, on the hardest of the three:

> ⭐ **Note 15 — my phone's keyboard suggestion bar.**
>
> **(1) What made it hard.** I couldn't decide between *learned* and *generating*, and I ended up
> thinking it's genuinely both, which felt like cheating until I wrote it out.
>
> **(2) Evidence for *generating*.** It produces words. Words are content. And there's no fixed menu
> — over a week it has suggested hundreds of different words to me, including names and slang I'm
> fairly sure aren't in any standard list. If I count the possible outputs the way we did in class,
> I can't. That's the blank-page test and it passes it.
>
> **(3) Evidence against — the honest case for *learned*.** It only ever shows me **three** options at
> a time. Three is a menu. And it definitely learned: it started suggesting my friend's name after I
> typed it about five times, so it's picking up patterns from examples, which is exactly what
> *learned* means. Also, everything in the *generating* column is also in the *learned* column, since
> generative AI is a kind of machine learning — so "learned" isn't even wrong.
>
> **(4) The one fact I'd need.** I'd need to know whether the three words come from a fixed list the
> phone keeps, or whether it builds each word up letter by letter as it goes. If it's a list, it's
> picking. If it builds them, it's generating. I could test this myself: type a made-up word ten
> times and see if the bar ever suggests it. If it can suggest a word that didn't exist before I
> invented it, it isn't reading off a list.
>
> **My call: generating** — but I've written it in the *learned* column too, with an arrow, because
> generative AI lives inside machine learning and both are true.

**The other two hard calls, answered**

| Note | The call | Reasoning |
|---|---|---|
| **4 — Automatic shop doors** | **Rules** — and arguably **not AI at all** | `IF motion detected THEN open` is a rule someone wrote. But the deciding question is whether the job needs judgement, and "did something move?" doesn't — the sensor fires for a stray cat, a blown crisp packet, anything warm and moving. No case-by-case decision, so no judgement, so probably not AI. **The fact that would settle it:** does the door ever *decline* to open for something that moved? If it never declines, there's no decision in there. |
| **9 — Maps arrival time** | **Learned** | A rule-based version is easy to imagine: distance ÷ speed limit. But the estimate changes minute by minute and gets rush hour right, which means it's using how long real cars actually took on that road just now. Nobody hand-wrote a rule for "Tuesday, 8:40am, raining, roadworks". **Evidence against:** part of it genuinely is arithmetic — the distance is just measured. **The fact that would settle it:** does the estimate change if I ask twice, ten minutes apart, on the same route? If yes, it's using live data, and turning live data into a time estimate is learned. |

### In-lesson questions

**Hook — "Name one thing YouTube's recommender cannot do."**
Anything that isn't ranking videos: tell you what a video is about, answer a question, make a video,
know whether you enjoyed it (it only knows whether you kept watching), tell you 7 × 8.

**Concept — "How many things could come out of a spam filter?"** Two. **"Out of a chatbot?"**
Effectively unlimited — no menu, a blank page.

**Concept — "But a chatbot writes poems AND explains science AND translates. Isn't that lots of
jobs?"** It looks like many and it is one: guess the next chunk of text. A poem, an explanation and a
translation are all text. Week 28 builds one by hand.

**Concept — "If a model says 'dog, 99%', how sure should you be?"**
Not sure at all, on that number alone. It tells you how strongly the model prefers *dog* over its
other options. It says nothing about whether *dog* is correct. Models are most confidently wrong on
inputs unlike anything they trained on.

**Round 1 — "So what's this thing's actual job?"** See the model answer above.

**Round 2 — "How many things could we check?"** Four or five, all invented. **"It changed its story —
what does that tell you?"** It never knew; it was producing plausible-shaped text both times.

**Wrap — "Today's big idea in one sentence."**
Model answers: *"Every AI does exactly one job and is blank one step sideways, and some of them make
new stuff instead of picking from a list."* · *"AI is narrow — brilliant at one thing, useless just
outside it — and being confident is not the same as being right."*

### Workbook answers

**W3.1 — The fifteen-row Spotter's Log**

Marked against six criteria. Tick each:

- [ ] Fifteen rows, no blanks
- [ ] Every system **specific** ("my phone's keyboard bar", not "my phone")
- [ ] At least three rows from each of the four zones
- [ ] At least two rows in each of rules / learned / generating — **or** a written sentence explaining
      why a column is empty
- [ ] Every reason mentions either *a person wrote the steps* or *it learned from examples*
- [ ] Three rows starred as hard calls

See the model board above for the standard.

**W3.2 — The three defences**

See the model defence above. Every paragraph must contain all four points; a missing point 4 means
hand it back and ask only for point 4. Five sentences minimum. The best defences use the system's
**failures** as evidence — "it opens for a cat, so it isn't judging" is worth more than any amount of
confident assertion.

**W3.3 — Interview an adult**

There is no wrong answer to record — the student writes down exactly what was said. What you're
marking is the honest rewrite underneath.

Typical adult answers and their honest rewrites:

| What the adult said | The honest rewrite |
|---|---|
| "AI is computers that can think for themselves." | "AI is machines doing jobs that used to need a person's judgement. They don't think — they find patterns in examples or follow rules someone wrote." |
| "It's robots, basically." | "Robots are about having a body. AI is about a kind of decision. Most AI has no body at all — the spam filter is AI and it's just software." |
| "It's ChatGPT and all that." | "ChatGPT is one kind of AI. Spam filters, face unlock and video recommendations are all AI too, and they're older and used by more people." |
| "It's a computer that learns." | "Some AI learns from examples. Some AI is if-then rules a person wrote. Learning is one way of doing AI, not the definition of it." |
| "Honestly, I don't really know." | **The most honest answer on this list.** Write it down exactly, and say so. Then write the definition underneath as a gift. |

**The thing to notice, and to say out loud:** most adults reach for *robots*, *thinking* or
*ChatGPT*. Those are the three misconceptions the student has now personally worked past in three
weeks. Frame it generously — *"that's what nearly everyone thinks, including me before I read this"*
— never as the adult being stupid.

---

## 🔮 Next Week Preview

Term 1 pivots next week. For three weeks the question has been **"who wrote the rule?"** From Week 4
it becomes **"where did the examples come from?"** — because everything a machine knows arrived as
**data**, and almost always in the shape of a table: one row per example, one column per thing
measured. The student builds their own honest table from a week of real life and discovers the
hardest question in the whole topic, which is not a vocabulary question at all: **what is one row?**
A day? A meal? An hour? All three are valid and they produce completely different tables.

**Prep early:**
- Nothing to install. Week 4 runs on paper, or on Google Sheets if you'd rather.
- Ask the student to start noticing one measurable thing about their days this week — bedtime, screen
  minutes, how far they walked, how many times the dog barked. They'll turn it into a table.
- Keep the fifteen-note board up on the wall. It is the first thing on the artefact wall and it stays
  there all year.
- Check the Questions We Owe page and clear anything on it before Week 4 starts. If *"when will AGI
  exist?"* landed there, the honest answer is in §Questions above — read it back to them and then
  close it.

---

[⬅ Week 2](week-02.md) · [Course Home](../README.md) · [Week 4 ➡](week-04.md) · [Student Guide](../student-guide/week-03.md) · [Workbook](../workbook/week-03.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
