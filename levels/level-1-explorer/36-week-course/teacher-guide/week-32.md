# Week 32 — Your Data, Fakes, and Trusting Too Much

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Student Guide](../student-guide/week-32.md) · [Workbook](../workbook/week-32.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 teach |
| **Big idea** | A photo carries more than a picture, a confident answer is not a correct one, and something that looks completely real can be made in ten minutes. |
| **New vocabulary** | personal data · metadata · deepfake · over-trust · automation bias |
| **Materials** | Printed fact cards for Round 1 (five slips), printed AI-answer cards for Round 3 (three slips), a real reference book or a trusted reference website, pen and paper |
| **Tech needed** | One computer with **one photo taken on a phone** already copied onto it. A browser for Round 3. |
| **Prep time** | 20 minutes, and **10 of those must happen the night before** — the photo transfer is the one step that cannot be improvised |

> **⚠️ Watch out:** Do not run Round 1 using a real classmate's real details. Use the fictional
> person supplied below. The point lands just as hard and nobody goes home upset.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can, and you will have seen them do it:

1. **Narrow a group of 800 people down to one** using five "anonymous" facts, and say which single
   fact did the most work and why that is surprising.
2. **Name three things a photo file carries besides the image**, and point to them on a real file.
3. **List the four provenance checks** — who posted it first, when, who else has it, what was around
   it — and state in one sentence why staring at the pixels does not work.
4. **Define automation bias** with a concrete example, and name one habit that defends against it.
5. **Fact-check three confident statements** against a real independent source and correctly
   identify the invented one *without guessing from tone*.

---

## 🧑‍🏫 What YOU Need to Know First

*About twelve minutes. Everything the lesson needs is here.*

### The three ideas, and how they hang together

Week 31 was about a gap in the data. This week is about three different ways an AI system can hurt
someone even when its accuracy is fine:

1. **It knows more about you than you gave it.**
2. **It can manufacture things that never happened.**
3. **You believe it, because it sounds sure.**

They belong in one lesson because they share a single root: **the confident surface hides the
machinery underneath.** A photo looks like a picture. A generated video looks like a recording. A
fluent sentence looks like a fact. In all three cases the surface is the thing that fools you.

### Idea 1 — Personal data is much wider than your name

> **Personal data** — any information that is about an identifiable person, **or that could be
> combined with other information to identify them.**

That second half is the whole lesson. Sort information into three columns and the middle one is
where the danger lives:

| Clearly personal | Personal **in combination** | Usually not personal |
|---|---|---|
| Full name, face photo | Postcode + birthday + school year | Yesterday's temperature |
| Home address, phone number | "the only left-handed goalkeeper in Year 7" | The rules of cricket |
| Voice recording, fingerprint | Your exact route to school | A photo of an empty street |
| School ID number | The times of day you are online | The plot of a novel |

No single item in the middle column identifies anybody. Put three together and there is exactly one
person in the country they can refer to. This is called **re-identification**, and it is why *"we
removed the names, so it's anonymous"* is one of the most commonly repeated false statements in
technology.

You will demonstrate this live in Round 1. It usually takes under ninety seconds, and the part that
lands hardest is not that it works — it is **which** facts did the work. The boring administrative
ones ("Year 7") delete hundreds of people at a stroke. The dramatic-sounding private one ("allergic
to peanuts") often deletes just one. Nobody protects the boring facts, because nobody thinks of them
as private.

### Idea 1b — Metadata: the notes a file keeps about itself

> **Metadata** — the hidden information a file carries about itself: when it was made, on what
> device, and often exactly where.

![What a photo file carries besides the picture](../figures/fig-w32-3-photo-metadata.svg)
*Figure 32.1 — You shared one thing. You gave away six.*

The analogy that works with an eleven-year-old: you post a photo of yourself in your garden. You are
thinking about your face. The photo also contains your house number on the gate, your school
uniform, a neighbour's number plate, a reflection in the window, and — attached invisibly to the
file — the exact GPS coordinates and the time. **You shared one thing and gave away nine.**

**What about models — do they remember?** Two honest answers, and the student will ask, so have both:

- **Your Teachable Machine classifier does not store your photos.** It stores numbers learned from
  them. You cannot open it and get a photo back. That is genuinely reassuring. It is not *total*
  reassurance: a model trained on 30 photos of your bedroom has learned quite a lot about your
  bedroom, and researchers can sometimes tell whether a specific example was in a training set.
- **A language model is different, and more alarming.** Because it was trained to reproduce likely
  text, text that appeared many times in its training data can come back out **word for word** —
  including things like phone numbers that happened to sit on a webpage. Nobody programmed that in.
  It is a side effect of "learn to continue text really well".

> **The rule: data you put into a system is data you may not be able to take back out.** Once it is
> inside a trained model, "please delete it" is a far harder request than it sounds.

### Idea 2 — Deepfakes, and why you must check provenance not pixels

> **Deepfake** — a photo, video or voice recording of a real person doing or saying something they
> never did, made by an AI.

Fakes are as old as photography. Three things changed, and it is the three together that matter:

| Before | Now |
|---|---|
| Took an expert days | Takes anyone minutes |
| Cost money | Costs nothing |
| One at a time | Thousands, automatically, each slightly different |
| Voice was hard to fake | A few seconds of audio is enough |

**The second harm is the sneakier one and most adults miss it.** Once everybody knows convincing
fakes exist, a person caught on *genuine* video can simply say "that's a deepfake" — and plenty of
people will believe them. So the technology damages truth twice: it makes false things believable,
**and it makes true things deniable.** The second harm reaches you even if you never see a single
fake.

**Do not teach fake-spotting by looking.** Weird hands, blurry teeth, wrong number of fingers —
generators fix those every few months, and "I can tell" is precisely how people get fooled. Teach
the four provenance checks instead, because they do not decay:

![Real or fake: check the provenance, not the pixels](../figures/fig-w32-4-provenance-checks.svg)
*Figure 32.2 — Two identical-looking photos. Staring harder will not help.*

1. **Who posted it FIRST?** Not who sent it to you. Scroll back to the original. An account created
   last week is a red flag.
2. **When was it posted?** Eleven minutes ago, with 90,000 shares, from 40 followers, is not organic.
3. **Who else has it?** A real event has multiple independent witnesses. One video and silence
   everywhere else is the shape of a fake.
4. **What was around it?** Reverse-search a frame. Old real footage relabelled as something new is
   the most common fake of all — and it needs no AI at all.

Then the fifth question, which is about you rather than the file: **who benefits if I believe this
and pass it on — and does it happen to confirm something I already wanted to be true?** A fake that
annoys you gets checked. A fake that delights you gets forwarded.

### Idea 3 — Over-trust and automation bias

> **Over-trust** — accepting an AI answer without checking, because it sounded sure.
> **Automation bias** — the human habit of trusting a machine's answer more than our own judgement,
> especially when we are tired, rushed, or unsure.

Notice that this is a fact about **people**, not about machines. It is why a mediocre AI can do more
harm than a terrible one: a terrible one gets ignored, and a usually-right one gets trusted on the
day it is wrong.

![Automation bias: the satnav and the river](../figures/fig-w32-5-satnav-river.svg)
*Figure 32.3 — The driver had eyes, headlights, and a lifetime of knowing roads do not go underwater.*

The student already has the technical half of this from Week 16 and Week 29: a confidence score
means "best of my options", not "probability I am right", and a text generator produces true and
invented sentences in the same smooth voice because there is no wobble channel. **A confident wrong
answer and a confident right answer are made by the same machinery and look identical.**

Here are the three situations to memorise, and the figure to show:

![Three times not to trust an AI answer](../figures/fig-w32-1-when-not-to-trust.svg)
*Figure 32.4 — Print this one and stick it somewhere. It is the most reusable thing in the week.*

And the fourth, which is about the human: **when you are in a hurry and the answer is what you were
hoping for.** That combination defeats more people than any technical flaw.

**What good use looks like** — say this out loud at some point, because otherwise the week reads as
"AI bad". Use AI where a wrong answer is cheap and checkable: brainstorming, first drafts,
explaining something you will then verify, rewriting your own words, making practice questions.
**Push the AI toward drafting and keep the deciding for yourself.**

### The three misconceptions you will meet

| Misconception | What to say |
|---|---|
| **"I could tell if something was fake."** Near-universal, and confidently held. | Show Figure 32.2 and let them try. Then: "generators get better every few months and your eyes do not. That is why we check where it came from, which does not go out of date." |
| **"It's anonymous, the names are gone."** | Run Round 1. Do not explain it — demonstrate it. Ninety seconds and the argument is over. |
| **"An AI wouldn't just make something up."** | It absolutely would, and not because it is lying. It was built to produce *likely-looking* text, and an invented page number looks exactly as likely as a real one. Week 29 already showed the machinery. |

### How deep to go — and where to stop

**Go this deep:** three ideas, one live demonstration each, and the four provenance checks written
down somewhere they will survive.

**Stop before:** how deepfakes are technically generated (interesting, not needed, and it drifts
toward "how would I make one"); any real distressing deepfake material — do not show one, describe
them; specific privacy law; and anything that turns into "the internet is dangerous, be scared".
The tone you want is **competent, not frightened**. A student who leaves able to run four checks is
in a better place than one who leaves anxious.

---

### 🧭 The Growing Map

Nothing moves on the map this week, and saying so out loud is worth ten seconds. **WHO IT FAILS** stays
shaded, because metadata, deepfakes and over-trust are not a fourth topic bolted on the end — they are
the same tile as bias, seen from the side where the person is the one being got wrong.

![The course map in Week 32: the same who it fails tile, now asking where a file came from and who gains if you pass it on](../figures/fig-w32-0-where-this-fits.svg)

*Figure 32.0 — Week 32's version. The same tinted, badged tile as last week, one dashed tile left, and
only **impact** lit along the bottom.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask:** *"which bit did we do today?"* They will look for a new box, not find one, and
   that hesitation is the teaching moment. Then ask the question that lands it: *"we opened a photo
   file, re-identified three classmates from boring facts, and spotted an invented video — why is that
   the same box as last week?"* Because all four things end with a real person believing something
   false about themselves or the world.
2. **Then the better question:** *"why is the other box still dashed?"* Because you have not built
   anything yet. YOUR OWN AI is weeks 34 to 36, and it is now the only thing on the map marked *not
   yet* — which is a quietly motivating thing for a student to notice in early summer.
3. **Have them copy it** and write their own four provenance checks — who posted it first, when, who
   else has it, what was around it — down the side of the WHO IT FAILS box, in their own words.

> **🧑‍🏫 Why this is worth two minutes.** This is the week most likely to be remembered as "the scary
> internet lesson". The map refuses that framing: the tile sits on the same branch as THE TABLE and
> HONEST TESTING, which says these are checkable, countable habits, not fears. Competent, not
> frightened — and the picture does half that work for you.

**The six threads** along the bottom are the spine of all four levels. Only **impact** is lit this week,
and deliberately so: nothing today improved a model. If a student asks why *model* is dark, that is the
best question of the wrap. Do not quiz them on the threads; the map is orientation, never assessment.

---

## 🧰 Prep Checklist

**10 minutes, the night before — this is the part that cannot be improvised**

- [ ] Take a photo on a phone **with location services switched on for the camera**, outdoors is best.
- [ ] Copy it to the computer **as a file** — USB cable, or email it to yourself as an *attachment*.
      **Do not send it through a chat app.** Most messaging apps strip metadata on the way through,
      which is genuinely good for your privacy and completely ruins this demonstration.
- [ ] Check you can see the details. **Mac:** open in Preview → Tools → Show Inspector → the "i" tab,
      then the GPS tab. **Windows:** right-click the file → Properties → Details.
- [ ] If no location shows up, that is fine and it is still worth showing — the time, the device and
      the camera settings are enough. Say honestly: "this one has no location, which means either
      the setting was off or something stripped it. Many photos do have it."

**10 minutes, on the day**

- [ ] Print or hand-write the **five fact slips** for Round 1 (text in the Activity section).
- [ ] Print or hand-write the **three AI-answer cards** for Round 3 (text in the Activity section).
      Do not let the student see them early.
- [ ] Put a real reference source on the table: an atlas, an encyclopedia, or a browser open at a
      reference site you trust. Round 3 does not work if the only available source is another AI.
- [ ] Read Figure 32.4 once so the three no-trust situations are in your head in order.

**If the internet or the photo fails**

| If | Then |
|---|---|
| The photo has no metadata at all | Use Figure 32.1 as the exhibit. It is a drawn version of exactly the same panel. The demonstration is weaker but the idea is intact. |
| No internet for Round 3 | Use a printed encyclopedia, an atlas, or a textbook. Round 3 is *better* against a paper source, because there is no temptation to search for the AI's own words. |
| No printer | All slips are five lines each. Hand-write them on scrap paper; the student never keeps them. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | 🪝 **Hook** — The garden photo | One posted photo, nine things given away |
| 8–26 | 🧠 **Concept** — Three ways a surface fools you | Personal data and metadata · fakes and provenance · over-trust |
| 26–40 | 🔍 **Worked Example** — The athlete video | Run all four provenance checks out loud on one scenario |
| 40–60 | 🎲 **Activity** — Three rounds | Re-identification · metadata · fact-check three answers |
| 60–70 | 🔑 **Wrap & Assign** | Four checks on a card, three takeaways, homework |

---

### 🪝 Hook — 8 minutes

**Say this:**

> "You take a photo of yourself in your garden and you post it. What did you just share?
>
> You are thinking: my face. Fine. Here is what actually went out.
>
> Your face. The house number on the gate behind you. Your school uniform, so now somebody knows
> which school. Your neighbour's car number plate. A reflection in the window, which sometimes shows
> the inside of the room. The plants, which tell somebody roughly what country and what season. The
> shadow, which gives the time of day.
>
> And then, attached to the file — not in the picture, *attached to the file* — the exact latitude
> and longitude to about five metres, the exact date and time, the make and model of the phone, and
> often the name of the account the phone is signed in to.
>
> You shared one thing. You gave away nine."

**Do this:** write the number **9** on the board and circle it. Nothing else.

**Ask this:** *"Which of those nine did you agree to share?"*

- **Hoped-for answer:** only the face. Say: "Right. One out of nine. And the other eight are the
  interesting ones."
- **If they say "well, everyone knows photos have that stuff":** press gently. "Do they? Show me how
  to look at it." Almost nobody can. That is the gap between knowing something abstractly and being
  able to use it.
- **If they get uneasy:** good, briefly — then steer to competence straight away. "We are not going
  to be scared of this. We are going to learn to open the file and look, which most adults cannot
  do, and then decide for ourselves what to send."

---

### 🧠 Concept — 18 minutes

Three blocks, six minutes each. Do not let block 1 eat block 3.

**Block 1 — Personal data (6 min).**

> "Here is the definition, and the second half is the one that matters. **Personal data** is any
> information about an identifiable person, **or that could be combined with other information to
> identify them.**
>
> So: your name is personal data, obviously. But 'Year 7' is not personal data on its own — there
> are a hundred and twenty of you. 'Lives in postcode area 3' is not personal data on its own.
> 'Left-handed' is not personal data on its own.
>
> Put those three together and there is one person. That is called **re-identification**, and it is
> why the sentence 'we removed the names so it's anonymous' is one of the most common false
> statements in the whole of technology."

**Do this:** draw the three-column table from the teacher notes on the board — clearly personal /
personal in combination / not personal — and fill in two examples each with the student's help.

**Ask this:** *"Give me something about you that isn't personal at all."*

- Whatever they offer ("I like cricket"), accept it, then add two more of their own facts out loud
  and ask how many people in the school are left. The point makes itself.
- **If they offer something genuinely non-identifying** (like "I have two arms") — that is a good
  answer and worth saying so. The truly non-personal facts are the ones that are true of everybody,
  which is also why they are useless in a dataset.

**Block 2 — Metadata and fakes (6 min).**

Show Figure 32.1. Read three lines out of it. Then move to fakes:

> "Same idea, other direction. A photo can carry more than you meant to send — **and** a photo can
> carry less truth than you assume. This is a **deepfake**: a picture, video or voice of a real
> person doing something they never did, made by an AI.
>
> Fakes are not new. Three things changed. It used to take an expert days and cost money; now it
> takes anyone minutes and costs nothing. It used to be one at a time; now it is thousands,
> automatically. And voices used to be hard; now a few seconds of audio is enough.
>
> And there is a second problem that is sneakier than the first. Once everyone knows fakes exist,
> anyone caught on a *real* video can just say 'that's a deepfake' — and people will believe them.
> So it makes false things believable **and** true things deniable. That second one reaches you even
> if you never see a fake in your life."

**Ask this:** *"How would you tell a fake photo from a real one?"*

- **Almost certain answer:** look at the hands / the teeth / it looks weird. This is the answer you
  want, because you get to demolish it. Show Figure 32.2 and say: *"Which of these two is real?
  You cannot tell, and neither can I, and that is not because we are bad at looking. Generators fix
  their visible flaws every few months. Your eyes do not get an upgrade every few months."*
- Then land it: *"So we stop checking the picture and start checking where it came from."*

**Block 3 — Over-trust (6 min).**

> "Last idea, and this one is about us, not about the machine. **Automation bias** is the habit of
> trusting a machine's answer more than our own judgement — especially when we are tired, rushed,
> or unsure.
>
> There is an entire genre of news story where a driver follows a satnav down a boat ramp into a
> river. They could see the water. They had eyes and headlights and a whole lifetime of knowing that
> roads do not usually go underwater. The screen was so confident, and had been right so many times
> before, that it beat the evidence in the windscreen.
>
> That is why a usually-right machine is more dangerous than a useless one. A useless one gets
> ignored."

Show Figure 32.3, then Figure 32.4, and read the three situations aloud.

**Ask this:** *"Give me a question where it would be fine to trust an AI, and one where it wouldn't."*

- **Hoped-for:** fine = a limerick, a brainstorm, a summary of something they can also read. Not
  fine = a medicine dose, a page number, last Tuesday's school match.
- **If both their examples are "not fine":** supply the other side yourself. This week must not
  land as "AI bad". The rule is *push it toward drafting, keep the deciding for yourself.*

---

### 🔍 Worked Example Together — 14 minutes

**Say this:**

> "A video reaches you. A famous athlete, at what looks like a press conference, saying they are
> quitting. It was posted eleven minutes ago. The account that posted it has forty followers and was
> created last week. It already has ninety thousand shares.
>
> We are going to run four checks. Watch how far we get **without looking at the video even once.**"

**Do this:** write the four checks down the board as you work through them, leaving space for the
findings beside each.

> **1. SOURCE — who posted this FIRST?**
> "Not who sent it to me. I tap the account. Join date: last week. Post count: nine. Has it ever
> posted about this sport before? No. Then I go to the athlete's own verified account and their
> club's account. If somebody is retiring, it is there. **It is not there.** That is a very loud
> silence."
>
> **2. WHEN — is the timing plausible?**
> "Eleven minutes old. Ninety thousand shares from a forty-follower account. Think about what that
> requires: each of forty people would have to have produced two thousand two hundred and fifty
> shares. That is not how things spread. Either somebody is pushing it deliberately or it was
> engineered to be maximally shareable. Both are reasons to slow down."
>
> **3. WHO ELSE HAS IT — corroboration.**
> "I search the athlete's name in a news app, sorted by newest. A real retirement from a famous
> athlete is covered by several independent news organisations within minutes. I check at least two
> that are not owned by the same company. **Nothing.**"
>
> **4. WHAT WAS AROUND IT — reverse search.**
> "I screenshot one clear frame and reverse-image-search it. What I am looking for is whether this
> footage exists somewhere else, with different audio, from an older press conference on a totally
> different subject. Relabelled real footage is the most common fake there is, and it takes no AI
> at all."

**Ask this:** *"We have found no other source anywhere. Does that prove it is fake?"*

- **Hoped-for answer:** no — strong evidence, not proof. If a student gets this unprompted, stop and
  make a fuss of it, because it is the hardest idea in the week.
- **Likely answer:** "yes, it's definitely fake." Reply: *"Careful. Absence of evidence is not
  evidence of absence. It is possible, rarely, to genuinely be first. So what do we actually do?"*
- **The answer you are steering to:** you do not declare it fake. **You do not share it, and you
  wait.** Waiting an hour costs you nothing. Sharing a fake costs you your credibility and helps it
  reach the next ninety thousand people.

**Say this to close:**

> "The right output of a verification check is very often 'I don't know yet'. Being comfortable
> sitting in that state, instead of picking a side so the discomfort stops, is the actual skill.
>
> And here is the last one, the check people skip. **Who benefits if I believe this and pass it on?**
> Then the harder version: *does this happen to confirm something I already wanted to be true?* A
> fake that annoys you gets checked. A fake that delights you gets forwarded."

---

### 🎲 Activity — 20 minutes

Full instructions below. Three rounds: re-identification (7), metadata (5), fact-check (8).

---

### 🔑 Wrap & Assign — 10 minutes

**Do this:** have the student write the four provenance checks on a small card, in their own words,
and put it somewhere they will see it. Not in the workbook — somewhere real.

**Say this:**

> "Three things.
>
> One: **'anonymous' usually is not.** It took us about a minute to get from eight hundred people to
> one, using facts nobody would think of as private. Assume the boring facts identify you, because
> they do.
>
> Two: **check where it came from, not what it looks like.** Your eyes will not keep up with the
> generators. The four checks will still work in ten years.
>
> Three: **a confident answer and a correct answer are different things**, and they are produced by
> the same machinery and sound exactly alike. The habit that protects you is small and boring: when
> it is a specific fact that matters, look it up somewhere that is not the thing that told you."

**Ask this (exit question):** *"You get a message that is exactly the thing you were hoping was
true. What do you do differently?"*

- **Hoped-for answer:** check it harder, precisely because I want it to be true.
- **If they say "nothing, I'd just check it normally":** press. "Would you though? Be honest. Which
  do you check more carefully — a message saying your team lost, or one saying your team won?"

---

## 🎲 The Activity, In Full

### **Three Rounds**

**Time:** 20 minutes (7 + 5 + 8) · **Group size:** 1 (notes for 2–6 at the end)

---

### Round 1 — The re-identification game (7 minutes)

**Materials:** five slips of paper, face down, in this order.

**Setup.** Say: *"There are eight hundred people in this town. I am thinking of one of them. There
are no names in what I am about to read you — this is a fully anonymous record. Tell me when you
know who it is."* Then turn over one slip at a time and, after each, ask the student to say roughly
**how many people are left.**

| Slip | What it says | People left | Removed |
|---|---|---:|---:|
| 1 | Year 7 | 120 | 680 |
| 2 | Lives in postcode area 3 | 28 | 92 |
| 3 | Plays cricket | 9 | 19 |
| 4 | Left-handed | 2 | 7 |
| 5 | Allergic to peanuts | **1** | 1 |

![Eight hundred people narrowed down to one](../figures/fig-w32-2-eight-hundred-to-one.svg)
*Figure 32.5 — No name. Five facts. One person.*

The student will not be able to compute the exact counts and does not need to; you supply them.
What they must do is watch the number collapse.

**Then the two questions that are the actual lesson:**

**Ask this:** *"Which single fact did the most work?"*

- **The answer:** slip 1, "Year 7". It removed 680 people out of 800 by itself.
- **Most students say slip 5**, the allergy, because it sounds the most private. Correct them with
  the number: the allergy removed **one** person. The school year removed six hundred and eighty.

**Ask this:** *"So which fact would you have thought to protect?"*

- Everybody protects the allergy. Nobody protects the school year. **The facts that identify you are
  not the facts that feel private**, and that mismatch is why anonymising data properly is so much
  harder than it looks.

**Finish with the trade-off**, which has no clean answer and should not be given one: *"Now make
this dataset genuinely anonymous. What do you delete?"* Whatever they delete, ask what the dataset
was for and whether it can still do that job. Bucket the ages, blur the postcode, drop the
handedness — and you have a dataset that can no longer answer the question it was collected to
answer. **That trade is permanent and unresolved, and noticing it is the achievement.**

---

### Round 2 — Open up a photo (5 minutes)

**Setup:** the phone photo you prepared, already on the computer.

**Do this:** open the file's details in front of the student and read the fields out loud, slowly.

- **Mac:** Preview → Tools → Show Inspector → the "i" tab, then the GPS tab.
- **Windows:** right-click → Properties → Details.

Read out: the **date and time** to the minute. The **device**. The **camera settings**. And if it is
there, the **latitude and longitude** — then paste those coordinates into a map and let the map show
where you were standing.

**Ask this:** *"Where did you think that information was stored?"*

- Most students assume it is held by the app or the phone, not carried around inside the file
  itself. The moment worth building is: **this travels with the file. If you send the file, you send
  all of it.**

**Ask this:** *"When would you want this switched on?"*

Do not let this become one-sided. Metadata is genuinely useful: it is how your photos sort by date,
how a map of your holiday gets built, how a photographer proves a picture is theirs, and how the
time on a photo can prove where somebody was. **The skill is choosing, not avoiding.**

> **🧑‍🏫 If a student asks:** *"Can I remove it?"* — Yes. Most phones have a "remove location" option
> when sharing, and most chat apps strip it automatically. Worth knowing: the fact that chat apps
> strip metadata is why the photo for this lesson had to be transferred by cable or as an email
> attachment.

---

### Round 3 — Two true, one invented (8 minutes)

**Materials:** three cards, and one **real, independent** source — an atlas, an encyclopedia, or a
reference site. Not another AI.

**Do this:** put all three cards on the table at once. Read them aloud in the same confident voice.

> **CARD A.** "The Great Barrier Reef lies off the coast of Queensland in Australia. It is the
> largest coral reef system in the world and stretches for more than 2,000 kilometres."
>
> **CARD B.** "The blue whale is the largest animal that has ever lived. The longest ones reliably
> measured are about 30 metres and they can weigh over 100 tonnes."
>
> **CARD C.** "The first people to reach the summit of Mount Everest were Sir Edmund Hillary and a
> Sherpa named Nawang Gombu, in 1948."

**The rule, stated before anyone speaks:** *"Two of these are true and one is invented. You are not
allowed to guess. You are not allowed to say which one 'sounds off'. You have to check all three
against a real source and show me where you looked."*

**What happens:** the student almost always wants to nominate one immediately, on tone. Do not let
them. Make them check A first — the true one — because checking a true statement and finding it
confirmed is what teaches the procedure. Checking only the suspicious one teaches nothing.

**The answers, with what the check should turn up:**

| Card | Verdict | What a real source says |
|---|---|---|
| **A** | **True** | Off Queensland, Australia; the world's largest coral reef system; roughly 2,300 km long. |
| **B** | **True** | Largest animal known to have ever lived; reliably measured lengths up to about 30 m; heaviest individuals well over 100 tonnes. |
| **C** | **INVENTED** | The first ascent was **29 May 1953**, by Edmund Hillary and **Tenzing Norgay**. |

**The debrief, which is the point of the round:**

Card C is a beautiful specimen. Look at what it got *right*: Edmund Hillary is the right person.
"Sherpa" is the right word. **Nawang Gombu was a real Everest climber** — Tenzing Norgay's nephew,
who summited in 1963. Every ingredient is real. They have just been assembled wrongly, into a
sentence with exactly the same confident shape as the two true ones.

**Ask this:** *"How would you have known, without looking it up?"*

- **The honest answer is: you wouldn't.** Say so plainly. That is the whole lesson. There is no tell.
  There is no wobble in the voice. There is no "hmm, I'm not sure about this one" — because the
  machinery that produces a true sentence and the machinery that produces that sentence are the
  same machinery.
- **If the student claims they could tell** (some will, especially if they happen to know the date),
  accept it and then move the target: *"Fine — you knew that one. Now do it for the price of a
  train ticket in a city you have never been to. What's your tell then?"*

**"Finished" for Round 3 looks like:** three verdicts, and for each one a named source the student
actually opened.

---

### Variation — easier

Run Round 1 with three facts instead of five (Year 7 → postcode → left-handed gets you to two
people, which is close enough to make the point). Skip Round 2's map step. In Round 3, tell the
student which card is false and make the task "find the proof and write down where you found it" —
the procedure is what is being taught, not the detective work.

### Variation — harder

- **Round 1:** give the student the dataset and ask them to make it genuinely anonymous, then state
  in writing which question it can no longer answer.
- **Round 3:** add a fourth card that is **half** true — "Mount Everest is 8,848 metres high and lies
  entirely within Nepal" (the height is right; the summit is on the **border between Nepal and
  China**, so "entirely within Nepal" is false). Half-true statements are the hardest kind and the
  most common.

### If you have 2–6 students

Round 1 works better with a group — call out the running count together. For Round 3, split the
three cards between pairs, then have each pair *present its evidence* rather than its verdict; the
rest of the group decides whether the evidence is good enough. That "show your source" step is the
habit you are actually installing.

---

## ❓ Questions Students Ask This Week

**1. "If I delete a photo, is it gone?"**

From your phone, yes. From everywhere, almost never. If you posted it, somebody may have saved it,
a service may keep backups for months, and if it was ever used to train a model, the model has
already learned from it and cannot un-learn it on request. The useful mental model: **posting is
not like saying something, it is like printing something.** Deleting takes back your copy, not
theirs.

**2. "Does my model have my photos inside it?"**

Not as photos, no. Your Teachable Machine classifier stores numbers learned from your photos, and
you cannot open it and get a picture back out. But it is not nothing: a model trained on thirty
photos of your bedroom has learned a fair amount about your bedroom, and a language model trained on
text can sometimes reproduce that text word for word. So the honest answer is "not the way you're
imagining, but more than you'd like."

**3. "Why don't they just make a computer program that detects deepfakes?"**

**Nobody knows whether that can be made to work in the long run, and here is why it is a genuinely
open question.** People do build detectors, and they do work — for a while. But the moment a
detector exists it can be used to *train* the next generator: make a fake, run it through the
detector, adjust until the detector is fooled, repeat. The detector is a scoring machine for the
thing it was built to stop. Some people think signing and tracking authentic files at the point of
capture will win instead, some think detection will keep up, and some think we simply move to a
world where video is not treated as proof on its own. It has not been settled. That is exactly why
the four provenance checks matter: they do not depend on winning that race.

**4. "If a fake is obviously a joke, is it fine?"**

The joke is fine right up until the clip leaves the room, and clips always leave the room. Once it
is forwarded twice, nobody attached to it knows it was a joke; they just have a recording of a real
person saying something. The rule that costs you nothing: **do not make a fake of a real person
without asking them**, even when nobody would find out. It is their face and their voice.

**5. "Everyone already has my data, so why bother?"**

Two answers. The small one: it is not all-or-nothing. Some things are out there and plenty is not,
and the next ten years of your data have not happened yet. The bigger one: "I have nothing to hide"
quietly assumes you know what will matter later, and you do not. A school attendance record, a
medical note, a location history — none of those look dangerous today, and any of them can matter a
lot in five years to somebody you have not met.

**6. "Isn't it rude to fact-check somebody?"**

Fact-check the *claim*, not the person, and say it that way. "I couldn't find another source for
this yet" is a completely different sentence from "you're wrong". And here is the practical bit:
people who feel corrected get defensive and dig in; people who feel included in the investigation
help you. Aim for "let's check" rather than "that's fake".

**7. "So should I just not trust AI at all?"**

No, and that would be a bad outcome from this lesson. Use it where a wrong answer is cheap and you
can check it yourself in seconds — brainstorming, first drafts, explaining a concept, rewriting your
own words, making practice questions. Avoid it where a wrong answer is expensive and you *cannot*
check it easily. **Push it toward drafting; keep the deciding for yourself. You are the last
checkpoint, and the last checkpoint is not allowed to be asleep.**

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The room gets frightened | Three ideas about being watched, faked and fooled, all in one hour | Every idea must end with an action, not a warning. "Here is how to open the file." "Here are four checks." "Here is when it is fine to trust it." Competence, not fear |
| The student insists they could spot a fake | Everyone believes this, and it feels like a skill | Do not argue. Show Figure 32.2, let them pick, then tell them the two images are drawn identically on purpose. Then: "your eyes don't get an upgrade every few months; the generators do" |
| Round 3 gets solved by vibes | Guessing is faster than checking, and one card *does* sound slightly off | Enforce the rule: **check card A first**, the true one. Nobody gets to name a verdict before all three have a named source |
| Round 1 uses a real student's details | It seems more vivid | Use the supplied fictional person. Real details in this exercise land as an accusation and the lesson is lost |
| The photo has no metadata | A chat app stripped it in transit, or location was off | Say what happened — it is a genuine finding. "This app removed it, which is good for me and bad for my demo." Then fall back to Figure 32.1 |
| It turns into "AI is bad" | The whole week is failure modes | Spend a full minute on good use: drafting, brainstorming, explaining, rewriting. The rule is *drafting yes, deciding no*, not *never* |
| The student fact-checks by asking an AI | It is right there and it sounds authoritative | Name the trap: it will confirm itself in the same confident voice. Two independent sources that do not copy each other, or it does not count |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** Round 2's map step, the "make it genuinely anonymous" trade-off discussion, and the
half-true fourth card. Cut the model-memory material entirely — it is background for you, not
required content for them.

**Keep, non-negotiably:** Round 1 (it is ninety seconds and it is the best thing in the week), the
four provenance checks written on a card, and one round of "check it against a real source".

**Reteach like this:** do Round 1 about a fictional person and then, gently and with permission, half
of it about the student — two facts only, and stop before it gets uncomfortable. Feeling the number
shrink is worth more than any definition. For the fakes half, drop deepfakes and use the older,
commoner version: a real photo from a real event, reposted with a false caption. No AI involved, the
same four checks catch it, and it is much easier to picture.

### If the student is flying

1. "You must publish the class dataset for a genuinely good reason — planning school lunches. Make
   it actually anonymous, then write down what question it can no longer answer."
2. Take the half-true Everest card and write the *correct* version of the sentence.
3. "Name something that is impossible to fact-check, and explain why." (Predictions, opinions, and
   claims about someone's private intentions. Worth noticing that these are exactly the claims that
   spread fastest.)
4. The hard one: "The technology makes false things believable and true things deniable. Which of
   those two do you think does more damage, and what evidence would change your mind?"

### If the student won't engage today

Do Round 1 and stop. It takes ninety seconds, it is a game, it needs nothing printed, and it works
even in a bad mood. Then read the four provenance checks aloud, have them copy the four onto a card,
and end the lesson. You will have delivered the two most durable things in the week, and the rest
moves to Week 33's warm-up.

---

## ✅ Assessing Understanding

**Check 1 — re-identification.**
> Say: *"Give me three facts about a person, none of which is their name, that together would
> identify exactly one person in this town."*

- **Excellent:** three ordinary-sounding facts that intersect to one person, and an explanation of
  *why* the intersection is small.
- **Good enough:** three facts that would plausibly do it.
- **Not yet:** offers a name, an address or a phone number — that is the easy case. Re-ask: "now do
  it with facts that all sound harmless."

**Check 2 — provenance.**
> Say: *"Name the four checks, in any order."*

- **Excellent:** first source, when, who else has it, what was around it — plus "and who benefits".
- **Good enough:** three of the four, in their own words.
- **Not yet:** "look at the hands." Redirect to the card they wrote, and ask why looking fails.

**Check 3 — automation bias.**
> Say: *"Define automation bias, and give me one habit that protects you from it."*

- **Excellent:** a definition that puts the flaw in the *person*, plus a specific habit ("check a
  specific fact against a source that isn't the AI").
- **Good enough:** the satnav-and-the-river story plus any checking habit.
- **Not yet:** "it means the AI is wrong." Correct it directly: it means *we* over-trust it. The
  machine's error rate is a separate thing.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1** | Thinks "anonymous" means "no name attached". Believes fakes can be spotted by looking. |
| **2** | Can repeat that combinations identify people, and can name one or two provenance checks with prompting. Still fact-checks by asking whether it "sounds right". |
| **3** | Re-identifies from three facts unaided, names three or four provenance checks, finds metadata on a real file, and checks a claim against a named independent source. |
| **4** | All of level 3, plus explains **why** pixel-spotting is a losing strategy, and knows the boring facts do the most identifying. Can state one legitimate good use of AI without prompting. |
| **5** | All the above, plus grasps that "no other source" is strong evidence and not proof, and that the right answer is often *"I don't know yet, so I'm not sharing it."* Notices the fourth trap — that they check content they dislike more carefully than content they like. |

**Target for a typical student: 3, with the "I don't know yet" idea arriving later in the term.**

---

## 📤 Homework to Assign

**Say this:**

> "The workbook is about fifty minutes, and it starts with five quick questions from last week, no
> notes. The big job is in Practice Set B. First, pick one AI product you actually use — not one
> you've heard of, one you use — and answer five questions about what it collects and whether you
> could say no. Guess where you have to, but mark every guess with a question mark. **An honest
> guess clearly labelled is worth far more than a confident invention.** That sentence is basically
> the whole course.
>
> Second, three more confident statements. Same rules as in class: check all three against a real
> source, write down which source, and no guessing from tone. Every verdict needs a named source —
> 'I checked' scores zero.
>
> Then there is a puzzle, two big questions, and a photo investigation. Those are the stretch —
> do as many as you like. And last: write the four checks on a real card and put it somewhere you
> will see it."

**What the student needs at home:** a pen, one real reference source that is **not** an AI (an atlas,
an encyclopedia, a textbook or a reference site you trust) for B2, and three of their own photo files
for Build It.

**Workbook sections.** The workbook states about 50 minutes for the core; the per-section
times below are my own estimates, so adjust them to your student.

| Workbook section | Task | Core or stretch | Est. time |
|---|---|---|---|
| ✅ **Warm-Up** | Five recall questions from Week 31 (bias, the gap, the chain, the accuracy question, predicting first) | Core | 5 min |
| ✍️ **A1** | Fill in the blanks: personal data, metadata, re-identification | Core | 3 min |
| ✍️ **A2** | Multiple choice: the shocking video, then say what is wrong with the three not ticked | Core | 4 min |
| ✍️ **A3** | Three true/false statements, each with a reason | Core | 4 min |
| ✍️ **A4** | Match five terms to their meanings | Core | 2 min |
| ✍️ **A5** | Label the photo-file diagram with five different hidden things (Figure W32.1) | Core | 3 min |
| ✍️ **A6** | Vocabulary: five words, one sentence each | Core | 5 min |
| ✍️ **B1** | Data map of a real product you use: five questions | Core | 15 min |
| ✍️ **B2** | Fact-check three confident answers; name the source for each | Core | 15 min |
| ✍️ **B3** | Sort twelve school-app data items into three columns, break the "names removed" claim, name three misuses, name two forbidden columns | Core | 10 min |
| ✍️ **B4** | The athlete video: four checks as actions, two signals with no pixels, the "no other source" question, the message to a friend | Core | 8 min |
| ✍️ **B5** | What would go wrong: the nurse's dose, and the "joke" deepfake of a teacher | Core | 5 min |
| 🧩 **Puzzle of the Week** | Eight students, four harmless columns: who is identified by which pair (Figure W32.2) | Stretch | 10 min |
| 🤔 **Think Deeper** | Two paragraph questions: genuinely anonymous data; which harm is worse | Stretch | 10 min |
| 🛠️ **Build It** | Metadata investigation of three real photos, then the provenance card | Stretch, but the card is expected | 15 min |
| 🎨 **Draw It** | One photo you might post, nine things given away (Figure W32.3) | Stretch | 10 min |
| 📊 **Self-Check** | Tick seven "I can…" rows | Core | 2 min |

B1 and B2 are the two heaviest pieces, so if time is short, protect those and the card.

---

## 🔑 Answer Key

Answers follow the workbook's own order: Warm-Up, Practice Set A (A1–A6), Practice Set B (B1–B5),
Puzzle of the Week, Think Deeper, Build It, Draw It, Self-Check. The student's workbook has its own
Answers section at the end; **never hand over this teacher guide** — it also names the mistakes to
expect.

### Warm-Up

**1.** A **count**. The model saw far fewer examples of one group; nobody had to be unkind.

**2.** 74 − 41 = **33 percentage points.** Not 33%, because "33% of what?" has no answer.

**3.** Who got photographed → the training data is lopsided → the model learns what it saw → somebody
real gets bad answers. **The fix is at link 1.**

**4.** **"93% — for whom?"** A single accuracy number is an average, and every average hides somebody.

**5.** Because a guess made afterwards is worthless — you could pick whichever group made you look
right, or quietly drop the batch that came out badly. Writing it first turns a demonstration into a
test.

*Watch for:* "33%" in item 2 (the percent versus percentage-points slip), and "the model is biased
against them" in item 1 (an attitude, not a count). Any fuzzy answer here is a Week 31 gap, and
Week 33 is built on it.

---

### A1 — Fill in the blanks

Personal data: *identifiable* … *combined*. Metadata: *hidden* … *itself* … *device* … *where*. The
word for working out who an "anonymous" record belongs to is **re-identification**.

---

### A2 — Multiple choice

**(c)** is correct.

- **(a)** fails because generators fix their visible flaws every few months and your eyes do not get an
  upgrade. "I can tell" is exactly how people get fooled.
- **(b)** fails because it will answer in the same confident voice using the same machinery. You need a
  source that does not come from the thing you are checking.
- **(d)** fails because sharing it *is* spreading it. Adding "is this real?" does not undo the reach —
  plenty of people will only read the video.

*Watch for:* a student who ticks (c) but writes "the others are just worse" — they need a reason for
each, not a ranking.

---

### A3 — True or false, and explain

**(i) FALSE.** Names are the easy part. Year group + postcode area + bus route took us from 600
students to one, with no name anywhere. Combinations identify people.

**(ii) FALSE.** It is stored **inside the file**. Which is exactly why it matters: send the file, send
all of it. (Many chat apps strip it on the way through — which is good for you and is also why the demo
photo has to be transferred by cable or as an email attachment.)

**(iii) FALSE.** Automation bias is a fact about **people** — our habit of believing a screen over our
own judgement, especially when tired or rushed. The machine's error rate is a completely separate
thing. Which is why a *usually-right* machine is more dangerous than a useless one: the useless one
gets ignored.

---

### A4 — Match the pairs

**1 → C** · **2 → E** · **3 → B** · **4 → D** · **5 → A**

---

### A5 — Label the diagram

Five different kinds of hidden thing: **(1)** the date and time, to the minute · **(2)** the device —
make and model of the phone · **(3)** the camera settings — exposure, flash, which lens · **(4)** the
location, latitude and longitude, often to about five metres · **(5)** the edit history — whether it was
cropped, filtered or rotated.

Also acceptable in place of one of those: the account the phone was signed in to, or the file's
original filename.

*Watch for:* "GPS", "address", "map place" and "city" as five lines — that is one kind of thing five
times, which the workbook warns against.

---

### A6 — Vocabulary

| Word | A correct student answer looks like |
|---|---|
| **personal data** | Information about a person you can identify — including facts that only identify them when several are put together. |
| **metadata** | The hidden notes a file keeps about itself: when it was made, on what device, and often exactly where. |
| **deepfake** | A photo, video or voice of a real person doing or saying something they never did, made by an AI. |
| **over-trust** | Accepting an AI's answer without checking, because it sounded sure. |
| **automation bias** | The human habit of believing the machine over your own judgement — like following the satnav into a river. |

---

### B1 — Audit a real product's data map

Marked on **structure and honesty**, not on being right — the student cannot know most of this for
certain, which is itself the finding. Worked example for a short-video app:

| Question | A full-marks answer |
|---|---|
| **1. What does it collect from you?** | Every video I watch and for how long, what I skip, what I re-watch, what I search, what I like and comment, my rough location `?`, my device and screen size, and the times of day I am on it. |
| **2. What does it collect from other people, about you?** | Who I message, and therefore who my friends are; anything my friends' contact lists say about me `?`; other people's videos that I appear in. |
| **3. Could you opt out and still use it?** | Some of it — I can turn off precise location. **Not the core of it:** watch history *is* the product, so opting out of that means the app cannot work. `?` |
| **4. Who is affected but was never asked?** | Everyone who appears in the background of a video. Everyone whose video was used to work out what people like me watch. My friends, whose contact details reached the app through me. |
| **5. What happens when it is wrong?** | Small harm: I get shown something boring. Big harm: it learns I linger on something upsetting and shows me more of it, and nobody notices because from the outside that just looks like engagement. **Who finds out? Usually nobody.** |

**Give full marks for `?` marks.** A student who writes "I think it collects location but I'm not
sure" has done better work than one who states it flatly. Question 4 is the one that teaches most:
**most AI systems affect far more people than use them, and those people had no say at all.**

---

### B2 — Fact-check three confident answers

The three statements, presented in the workbook in the same confident voice:

> **1.** "A hexagon has six sides, and its interior angles add up to 720 degrees."
> **2.** "Sachin Tendulkar scored 100 international centuries. His first came in 1990 and his
> hundredth in 2012."
> **3.** "Mount Kilimanjaro is the highest mountain in Africa, at 6,895 metres, and it stands in
> Kenya."

| # | Verdict | The check |
|---|---|---|
| **1** | **True** | Checkable with arithmetic, no source needed: a polygon's interior angles total (n − 2) × 180. For n = 6 that is 4 × 180 = **720**. ✓ |
| **2** | **True** | An encyclopedia or cricket reference confirms 100 international centuries; the first in 1990 and the hundredth in March 2012. |
| **3** | **FALSE — twice over** | Kilimanjaro *is* the highest mountain in Africa, but it is **5,895 metres**, not 6,895, and it is in **Tanzania**, not Kenya. An atlas settles both in about twenty seconds. |

**Full marks require a named source per statement**, not just a verdict. "I checked" scores zero;
"I checked in the atlas on page 44" scores full.

**The debrief question — "what did the false one have in common with the true ones?"**

Everything except the truth. It is the same length, the same confident tone, it contains a genuinely
correct claim (Kilimanjaro *is* Africa's highest), a specific-looking number, and a country that is
right next door to the correct one. **Specific facts are exactly where invention happens most
freely, because a specific fact is rare in the training text and its *shape* is trivially easy to
fake.**

**"Why couldn't you just ask the AI if it was sure?"** — because it will confirm itself in the same
confident voice, using the same machinery that produced the error. You need a source that does not
come from the thing you are checking.

---

### B3 — Sort the data, then break the claim

A school app collects: *full name · student ID · date of birth · home postcode · photo of face ·
daily arrival time · lunch choice · test scores · medical allergies · parent phone number · bus
route · favourite colour.*

**(a) The three-way sort.**

| Clearly personal | Personal in combination | Not personal on its own |
|---|---|---|
| Full name | Home postcode | Favourite colour |
| Student ID | Daily arrival time | Lunch choice |
| Date of birth | Bus route | |
| Photo of face | Test scores | |
| Medical allergies | | |
| Parent phone number | | |

Two placements worth defending out loud. **Test scores** are in the middle column because a score
alone identifies nobody, but "the student who got 98% in Year 7 maths" usually identifies exactly
one. **Lunch choice** looks harmless and mostly is — until you notice that a consistent halal,
kosher or vegetarian choice can reveal religion. Almost nothing stays in column three once you
combine it with something else.

**(b) Break the claim "we removed the names, so it's anonymous".**

Take **postcode + date of birth**. In a school of 600, maybe 40 students live in one small postcode
area; of those, the number born on one exact date is nearly always zero or one. Add bus route to
confirm. No name required — and both of those look like harmless background columns to whoever
published the file.

**(c) Three most sensitive, with a specific misuse each.**

1. **Medical allergies.** Leaked school data reaching an insurer or a future employer turns a
   childhood allergy into a reason to charge more or hire someone else — and the person is never
   told that was the reason.
2. **Face photo + daily arrival time.** Together they tell somebody what a child looks like and
   exactly when and where they will be. Either alone is general information; together they are an
   opportunity.
3. **Parent phone number + student name.** A scammer calls saying "there has been an incident with
   [correct name] and we need a payment now". The correct name is what makes it work; the number is
   what delivers it.

**(d) Which columns should a "who will be late tomorrow" model be forbidden from using?**

| Forbidden | Why |
|---|---|
| Medical allergies | Nothing to do with lateness. Health data repurposed into a discipline-adjacent prediction starts shaping how a child is treated for reasons nobody can see |
| Home postcode | A strong stand-in for family income. The model learns "children from poorer areas are late" and flags them in advance — punishing a child for where they live, dressed as a prediction |
| Photo of face | Not needed for the task at all. **If a column is not needed, collecting it is the harm** |
| Test scores | Links lateness to academic performance and quietly builds a "problem student" profile that follows a child around |

The principle worth memorising: **use the smallest number of columns that does the job.** Bus route
and past arrival times are enough.

---

### B4 — The athlete video

**(a) The four checks, as actions rather than principles.**

1. **Source.** Tap the posting account: join date, post count, whether it has ever posted about this
   sport. Then check the athlete's own verified account and their club's. A retirement is announced
   there or it is not happening.
2. **When.** Eleven minutes old, 90,000 shares, 40 followers. That is 2,250 shares per follower.
   Not organic.
3. **Who else has it.** Search the athlete's name in a news app sorted by newest; check two outlets
   that are not owned by the same company.
4. **What was around it.** Screenshot a frame and reverse-image-search it. Look for the same footage
   with different audio, or from an older press conference about something else entirely.

**(b) Two signals of a fake that need no pixels.**

1. **A week-old account with 40 followers.** Real news about a famous person breaks from the person,
   their club, or a journalist with a reputation to lose — not from an account with no history.
2. **90,000 shares in eleven minutes from 40 followers.** The spread is wildly out of proportion to
   the source, which means either coordinated pushing or content engineered to be maximally
   shareable. Both are reasons to slow down.

*(A third, if wanted: nobody else is reporting it.)*

**(c) Does "no other source" prove it is fake?**

**No — strong evidence, not proof, and the distinction is the hardest idea in the week.**

What it *does* tell you: for an event this big about a famous person, silence everywhere else after
eleven minutes is very hard to explain if the video is real. Real news propagates fast and from
several directions at once.

What it does *not* tell you: absence of evidence is not evidence of absence. It is possible, rarely,
to be genuinely first.

So the correct action is not "declare it fake". It is **"do not share it, and wait."** Waiting an
hour costs nothing. Sharing a fake costs your credibility and helps it reach the next 90,000 people.

**(d) The message to your friend who already forwarded it to thirty people.**

> Hey — I looked into that clip and I can't find it anywhere except one account that was made last
> week, and none of the sports sites have it, which is strange for news this big. I'm not saying
> it's definitely fake, but I'd wait an hour before believing it. Might be worth putting a "not
> confirmed yet" on the group chat, since a lot of people have it now.

Why it is worded that way: no accusation, no *"I can't believe you fell for that"*, an actual reason
instead of an assertion, an admission of uncertainty, and an easy face-saving next step. **People
who feel corrected dig in. People who feel included in the investigation help you.**

---

### B5 — What would go wrong

**(a)** Two things at once. **Over-trust:** the answer is accepted because it sounded sure, and a
specific number is exactly the kind of thing that gets invented most freely. **Automation bias:** she is
busy and tired, which is precisely when a screen beats a person's own judgement. And the stakes are
high and hard to undo — situation 1 on the card.

The habit: **when it is a specific fact that matters, look it up somewhere that is not the thing that
told you.** In a hospital that means the official dosing reference, every time, no exceptions for being
in a hurry.

**(b)** The joke is fine right up until the clip leaves the room — and clips always leave the room.
After two forwards, nobody attached to it knows it was a joke; they just have a recording of a real
person saying something. It is also the teacher's face and voice, being used without asking.

**The rule that costs you nothing: do not make a fake of a real person without asking them**, even when
you are certain nobody would find out.

---

### Puzzle of the Week — Eight students, four harmless columns

**(a)** No single column works.

```text
   Year = 8        →  4 people left  (S4, S5, S6, S8)
   Bus = B         →  3 people left  (S3, S5, S6)
   Lunch = non-veg →  3 people left  (S2, S5, S7)
   Hand = L        →  3 people left  (S4, S5, S7)
```

**(b) Two columns.**

**(c)** Three pairs work:

- **Year + Lunch** — Year 8 gives S4, S5, S6, S8; of those only S5 is non-veg.
- **Bus + Lunch** — Bus B gives S3, S5, S6; of those only S5 is non-veg.
- **Bus + Hand** — Bus B gives S3, S5, S6; of those only S5 is left-handed.

**(d)** Any of these, with the leftovers named:

- **Year + Bus** leaves S5 **and S6**.
- **Year + Hand** leaves S5 **and S4**.
- **Lunch + Hand** leaves S5 **and S7**.

**(e)** Because **Year only has two possible values here** (7 or 8), so knowing it can at best halve the
table. Bus has three values, and Lunch and Hand split the table unevenly, so each of those cuts harder.

In the town of 800 there were *five* year groups plus adults, so "Year 7" removed 680 people. Same
column, completely different power.

> **The rule: how much a fact narrows things down depends on how many different values it can take, and
> how unevenly they are spread.** Which is exactly why you cannot judge whether a column is "safe to
> publish" just by looking at how private it *feels*.

*Watch for:* a student who answers (b) with "one" because Year = 8 "feels" rare, or who lists only the
pairs that include S5's Bus. Have them cross out the rows on the table rather than argue.

---

### Think Deeper

**1. Genuinely anonymous.** There is no single right answer; a full-marks paragraph names a specific
change **and** the specific question that is now unanswerable.

A strong answer: *"I would replace exact dates of birth with just the year, replace the postcode with
'north of the river / south of the river', delete handedness and lunch choice entirely, and round the
lateness column to 'none / some / a lot'. Now the file cannot identify anybody. It also cannot answer
the question it was collected for — 'how many vegetarian lunches do we need on Tuesdays in Year 7?' —
because I deleted the lunch column. So the school has to choose: know the answer, or protect the
students. I would keep the lunch column but publish only totals per year group, never row by row,
because a total answers the question and a row identifies a person."*

That last sentence is the professional move: **publish the answer, not the data.**

**2. Which harm is worse.** Both answers can earn full marks. What is being marked is whether the
student names a **specific person** in each case and offers something that could change their mind.

- **"False things believable" is worse:** name somebody who loses their job, or is threatened, over a
  video of something they never did. It reaches people who have no way to check.
- **"True things deniable" is worse:** name somebody caught on genuine video doing real harm, who simply
  says "deepfake" and walks away — and now every real recording of anything is arguable. This harm
  **grows over time** and reaches people who never see a fake at all.

**What would change your mind** is the important part. A good answer: *"if it turned out that most
people, when shown proof a video was genuine, still believed the 'deepfake' claim, I'd switch to the
second answer — because that means evidence has stopped working, and everything else depends on
evidence working."*

---

### Build It — The metadata investigation and the card

There is no fixed answer, but a correct investigation looks like this:

- **Photo 1 (outdoors, from your own camera roll):** date and time to the minute, phone make and model,
  camera settings, **and usually latitude and longitude**. The map will show a street, a park, or your
  own house.
- **Photo 2 (indoors):** the same, but the location may be less exact or missing — phones often struggle
  for a fix indoors.
- **Photo 3 (via a chat app):** usually **almost nothing.** Often the location is gone, sometimes the
  device too, and the filename has been replaced.

**Which carried the least, and why:** the one that came through the chat app. Most messaging apps strip
metadata as the photo passes through. **Say the honest double-edged thing about that:** it is genuinely
good for your privacy, and it is also why the photo for this lesson had to be moved by cable or as an
email attachment. "None" written in a cell is a result, not a blank, and should be marked as one.

**"One thing you now know about yourself that you did not put in the picture on purpose"** — full marks
for anything specific: *"it says I was in the park at 16:42 on 14 March"*, *"it names my phone model"*,
*"it shows I cropped it"*.

**The card.** Full marks for four checks in your own words, plus the fifth question:

1. Who posted it **first**? (Not who sent it to me.)
2. **When**, and how fast did it spread?
3. **Who else** has it — two sources that do not copy each other?
4. **What was around it** — does this footage exist elsewhere, with different audio?
5. **Who benefits if I believe this and pass it on** — and does it happen to be something I wanted to be
   true?

Check it is a real card somewhere real, not words copied into the workbook page.

---

### Draw It

Marked on three things:

- [ ] At least seven labels **inside** the picture, all of them specific things (a house number, a badge,
  a number plate, a reflection, a shadow) rather than "background"
- [ ] The metadata in a **separate** box with a dashed arrow, clearly marked as invisible and attached to
  the file
- [ ] At least one label naming **somebody else** who did not agree to be in it — a neighbour's car, a
  passer-by, a window

If everything is inside the picture, the student has drawn the hook and missed the twist: the most
revealing part of that photo is the part you cannot see. Aim for nine labels in all.

---

### Self-Check

Not marked. Read the "not yet" column: each one points back to a section above (re-identification to the
Puzzle and B3, metadata to A5 and Build It, provenance checks to B4 and the card, automation bias to B5,
fact-checking to B2, "when it is fine to trust" to B5(a) and the Concept 3 row below).

---

### Answers to the questions posed during the lesson

| Where | Question | Answer to steer toward |
|---|---|---|
| Hook | "Which of those nine did you agree to share?" | One — the face. The other eight went with it. |
| Concept 1 | "Give me something about you that isn't personal at all." | Anything true of nearly everybody. Which is also why it is useless in a dataset. |
| Concept 2 | "How would you tell a fake photo from a real one?" | You cannot, reliably, by looking. Check where it came from instead. |
| Concept 3 | "One question it's fine to trust an AI on, one it isn't." | Fine: a limerick, a brainstorm, a summary of text you also have. Not fine: a dose, a page number, last Tuesday's local score. |
| Worked example | "No other source anywhere. Does that prove it's fake?" | No. Strong evidence, not proof. Do not share it, and wait. |
| Round 1 | "Which single fact did the most work?" | "Year 7" — it removed 680 of 800 by itself. The peanut allergy removed one. |
| Round 1 | "Which fact would you have thought to protect?" | The allergy. Which is the wrong one. The facts that identify you are not the facts that feel private. |
| Round 2 | "Where did you think that information was stored?" | Inside the file. It travels with the file — send the file, send all of it. |
| Round 2 | "When would you want it switched on?" | Sorting photos by date, holiday maps, proving a photo is yours. The skill is choosing, not avoiding. |
| Round 3 | "How would you have known, without looking it up?" | You would not. There is no tell. That is the entire lesson. |
| Wrap | "It's exactly what you hoped was true. What changes?" | You check it harder, precisely because you want it to be true. |

---

## 🔮 Next Week Preview

Week 33 is where all of this stops being about other people. The student runs the full fairness
audit on their **own** model: four batches of twelve photos in four deliberately different
conditions, every photo scored on paper, per-condition accuracy computed, the gap written in
percentage points — and then the Week 31 envelope comes out and the sealed prediction is compared
against what actually happened, and reported either way. Then the fix gets priced in actual
photographs, with the algebra shown, and the Fairness Audit Poster is started.

**Prep early, and this genuinely matters:** the four batches of twelve photos take about 25 minutes
to collect and the lesson does not work without them. **Ask the student to shoot them before class
day** — same three objects every time, twelve photos in bright daylight, twelve by lamplight, twelve
held in a hand, twelve on a busy patterned background. And **find the sealed envelope now**, not at
minute 55 next week.

---

[⬅ Week 31](week-31.md) · [Course Home](../README.md) · [Week 33 ➡](week-33.md) · [Student Guide](../student-guide/week-32.md) · [Workbook](../workbook/week-32.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
