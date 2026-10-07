# Week 6 — Where Did This Data Come From?

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Week 7 ➡](week-07.md) · [Student Guide](../student-guide/week-06.md) · [Workbook](../workbook/week-06.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (works in 60, stretches to 75) |
| **Type** | 🟩 lab — hands on a keyboard from minute 26 |
| **Big idea** | Thirty rows about you are a **sample**, not the world — and a **data card** is how you stay honest about that. |
| **New vocabulary** | provenance · sample · population · data card · outlier |
| **Materials** | The student's own table from Weeks 4–5 (aim: 21+ rows) · the printed workbook (Week 6), whose Build It section holds the blank "My data card" table · a board or big sheet of paper · a pen |
| **Tech needed** | A browser and **one** of: Google Sheets (free account), Excel, or LibreOffice Calc. All three behave identically for everything we do. Nothing to install if you use Sheets. Plus **one web page with a statistic on it**, chosen by you in advance. |
| **Prep time** | 20 minutes the night before — 5 of them spent actually typing `=AVERAGE` yourself |

> **⚠️ Watch out:** This is the first lesson with a screen in it, and screens eat time. The
> spreadsheet is a **tool**, not the subject. If the login fails, do the whole lesson on paper and
> lose nothing that matters. The paper fallback is written out in full below.

---

## 🎯 Lesson Objectives

By the end of this lesson the student can:

1. **Tell the population from the sample** for their own dataset — say out loud "the thing I want to be true about is ___, the thing I actually measured is ___" — and explain why the two are not the same.
2. **Ask the five provenance questions** of any dataset put in front of them, and write **"unknown"** without embarrassment when the source will not say.
3. **Write a seven-line data card** covering what the data is, how much of it there is, who collected it, who it is about, what permission was given, what is missing, and what it must not be used for.
4. **State three specific things their own dataset does not prove**, each beginning "This does not show that…", each naming the exact thing that is missing.

Objective 4 is the one that matters most, and it is the one an 11-year-old finds hardest, because it asks them to argue against their own work. A student who can do it has learned something most adults never learn.

---

## 🧑‍🏫 What YOU Need to Know First

**Read this once, slowly. About 15 minutes. It is complete — you need nothing else, including no prior spreadsheet skill.**

### The one-sentence version

A number is never just a number: it carries an invisible label saying *who was measured, by whom, when and how* — and if you cannot read that label, you cannot know what the number means.

### Part 1 — Provenance: every dataset has an origin story

> **Provenance** — the origin story of a dataset: who collected it, from whom, when, how, and with whose permission.

The word comes from the art world. When a museum buys a painting, it demands the provenance: who painted it, who owned it, where it has been. Not because the paint changes, but because a painting with no history is probably stolen or fake.

**🍕 The analogy to use with the student: the unlabelled tin.**

You would not eat from a tin with no label. You want to know what is in it, who made it, when, and whether it has expired. A dataset with no provenance is exactly that tin — and people feed them to models every single day.

**Here is the example that will do the heavy lifting in your lesson.** Two datasets. Both real. Both 1,000 rows. Both answering "how many hours do teenagers sleep?"

| | Dataset A | Dataset B |
|---|---|---|
| Rows | 1,000 | 1,000 |
| Collected from | Visitors to a **sleep-problems clinic** | Every student in **4 randomly chosen schools** |
| Average sleep | **5.9 hours** | **7.8 hours** |

Nobody cheated. Nobody mis-measured. Every row in both tables is a correctly recorded, honest number. And they disagree by nearly two hours — which, if you were writing a newspaper headline about teenage sleep, is the difference between "crisis" and "fine".

The reason is not in the numbers. It is in the sentence *"visitors to a sleep-problems clinic"*. Everyone in Dataset A is there **because they already had a sleep problem**. That is the entry ticket. So Dataset A honestly answers a *different question*: "how much do teenagers with sleep problems sleep?"

**Read this next line twice, because it is the whole lesson:** nothing about the numbers reveals this. You could stare at the 1,000 rows of Dataset A forever, compute every average, draw every chart, and never discover the problem. Only the provenance tells you. That is why every dataset needs a card.

**The five questions.** Memorise these five. They take about a minute to ask and they are the most useful minute in data work.

| # | Question | Weak answer | Good answer |
|---|---|---|---|
| 1 | **Who collected it?** | "It was on the internet" | "Me, by hand, in a notebook" |
| 2 | **From whom?** | "People" | "One person, age 11" |
| 3 | **When?** | "Recently" | "3 to 28 August 2026" |
| 4 | **How, exactly?** | "Somehow" | "Written down at 21:00 each night" |
| 5 | **With whose permission?** | *(silence)* | "My own data, a parent checked it" |

![The five provenance questions](../figures/fig-w06-5-five-questions.svg)
*Figure 6.1 — The five questions, and what a real answer sounds like. Print this one if you print nothing else.*

**On question 5 — permission — three rules, because it involves other people.** Ask first, every time: *"Can I write down your bedtime for a school project?"* Use initials or codes, never full names: `S3`, not `Sanjay Rao`. And never record home addresses, phone numbers, or photographs of faces without a parent's explicit yes. Week 31 and Week 32 go deep on privacy. For now the habit is enough: **if a row is about a person, that person gets a say.**

![The provenance chain, with one link broken](../figures/fig-w06-3-provenance-chain.svg)
*Figure 6.2 — Break any link and every box to the right of it inherits the mystery.*

The chain in Figure 6.2 is worth ten minutes of your own thinking before class. Data starts as a **person** who did something. Someone **wrote it down**. Someone **typed it up**. A **model learned** from it. Then a **decision** got made about somebody's real life — a loan, a school place, a medical scan. If the first link is unknown, the model is not broken; it works perfectly. You simply cannot say who its answers are about. That is a different and much worse problem, because it looks like nothing is wrong.

### Part 2 — Sample and population: your thirty rows are not the world

> **Population** — every single thing you would like your answer to be true about.
>
> **Sample** — the smaller set you actually managed to measure.

**🍕 The analogy: tasting the soup.**

You stir the pot, take one spoonful, and decide the whole pot needs salt. That works — *because you stirred*. Take your spoonful off the top without stirring and you get the oily layer, and your verdict on the pot is wrong.

The key insight, and say it exactly like this: **stirring matters more than spoon size.** A well-stirred teaspoon beats an unstirred ladle. This is the single most counter-intuitive fact in the lesson, and it is why "just get more data" is not the answer people think it is.

**The worked example that lands it.** You want to know the favourite sport at your school. Population: all 800 students. You ask 30 of them:

| Sport | Votes | Percent |
|---|---|---|
| Cricket | 22 | 73% |
| Football | 5 | 17% |
| Badminton | 3 | 10% |

Confident conclusion: cricket wins by a mile, 73%. Now the provenance: **you asked 30 people at cricket practice.**

The true school-wide answer might be cricket 40%, football 35%, badminton 25%. Your survey is not just wrong, it is *confidently* wrong, and here is the sting: **your 30 rows cannot detect their own error.** Inside your sample everything is perfectly consistent. There is no clean cell, no impossible value, nothing for last week's four checks to find. Week 5's tools are blind to this. That is precisely why this week exists.

**Three ways a sample goes wrong:**

| Problem | What happens | Example |
|---|---|---|
| **Wrong place** | You only reach one kind of person | Surveying at cricket practice |
| **Self-selection** | Only people who care bother to answer | An online poll about school food — only the furious vote |
| **Too small** | Luck dominates | Asking 3 people and reporting a percentage |

![Thirty measured, eight hundred hoped for](../figures/fig-w06-1-sample-vs-population.svg)
*Figure 6.3 — You measured 30. You are talking about 800. Every claim has to survive that gap.*

**The one-line fix you can always apply.** You usually cannot make your sample perfect — a real 11-year-old cannot survey 800 students. But you can *always* write down who is in it and who is missing. "This is 30 students from cricket practice; it under-represents students who do not play sport" turns a lie into an **honest limited finding**. Those two words are the goal of the whole lesson.

**Why this matters for AI specifically**, and this is the thread that runs to June: a model learns whatever its sample contains, and then gets used on the whole population. A face-unlock model trained mostly on adult faces is worse at children's faces — not because anyone was cruel, but because children were a thin layer of the sample. In Week 31 the student will measure exactly this gap on their own model, with their own numbers. Today they build the vocabulary for it.

### Part 3 — The data card

> **Data card** — a short honest note describing a dataset and its limits.

Seven lines. That is all. The first five are bookkeeping that anybody can do. **The last two are the professional part**, and if you emphasise one thing today, emphasise this:

| Line | What goes on it |
|---|---|
| What it is | One sentence a stranger could understand |
| How much | Rows × columns, dates covered, and what one row is |
| Who collected it | A person, and how they did it |
| Who it is about | Which people or things. If people, how many and who |
| Permission | Whose data, who agreed, what was left out on purpose |
| **Known gaps** | Blanks, deletions, faults found — **from last week's log** |
| **Do NOT use for** | The claims this data cannot support |

![A finished data card, all seven lines](../figures/fig-w06-2-data-card.svg)
*Figure 6.4 — Anybody can count rows. Saying what you cannot claim is the skill.*

The card in Figure 6.4 belongs to a student who tracked sleep, bag weight and screen time for thirty school days — the same *idea* as last week's Crime Scene Table, carried out properly to thirty rows. Notice that its "known gaps" line is just last week's fault log, written in plain English: two nights blank, one 88-hour sleep reading deleted as impossible. **The clean-up work from Week 5 becomes line 6 of the card.** Say that out loud; it makes last week's homework feel like it was going somewhere, because it was.

> **🧑‍🏫 If a student asks:** *"Is that the same table we fixed last week?"* — No. Same idea, thirty
> days instead of twelve, so the faults it lists are its own. A different collection would list
> different gaps. That is the point: the card describes *this* dataset and no other.

### Part 4 — Outlier, formally

The student met this last week as the trap. This week it gets its glossary card.

> **Outlier** — a value that is legal but sits far away from all the others.

The distinction they already fought over is worth one sentence of revision and no more: an **impossible value** sits outside the legal range and gets blanked; an **outlier** sits inside the legal range, just far from the crowd, and gets **kept and annotated**. New this week is only where the outlier goes: **on the data card, line 6**. "One day of 480 screen-minutes; I was home sick" is provenance. It belongs in writing, next to the data, forever.

### Part 5 — What you need to know about spreadsheets (if you have never used one)

You need four facts. That is genuinely all.

**Fact 1 — a spreadsheet is graph paper with names.** Columns are lettered A, B, C. Rows are numbered 1, 2, 3. So every box has a name: `A1` is top-left, `D5` is the fourth column, fifth row. Say the name out loud when you point; the naming *is* the skill.

**Fact 2 — the header row is row 1.** Put your column names in row 1 and your data starts in row 2. If you have 30 rows of data, they occupy rows 2 to 31. This trips up every beginner and it is worth saying twice.

**Fact 3 — typing `=` means "compute something".** Click an empty cell, type `=AVERAGE(D2:D31)`, press Enter. The cell shows a number. The colon means "everything from here to there". `D2:D31` is thirty boxes.

**Fact 4 — blanks are skipped, and this is the one dangerous fact.** `AVERAGE` ignores empty cells. If two of your thirty boxes are blank, it quietly divides by 28, not 30, and tells you nothing about having done so. That is *correct* behaviour and it is also exactly why last week's rule — never fill a blank with 0 — matters. A 0 would have been included and would have dragged the average down. A blank is honestly skipped.

![Two averages in a spreadsheet](../figures/fig-w06-6-sheets-average.svg)
*Figure 6.5 — The whole spreadsheet skill for this course, in one picture.*

That is the entire technical content of the lab. Google Sheets, Excel and LibreOffice Calc are identical for all four facts and for `=AVERAGE`. If you can do Figure 6.5, you can teach today.

### The three misconceptions you will meet today

**Misconception 1: "A bigger sample fixes a biased sample."** This is the big one, and adults hold it as firmly as children. Asking 300 people at cricket practice instead of 30 does not move the answer one inch closer to the truth — it just makes the wrong answer look more scientific. The unstirred ladle is not better than the unstirred teaspoon. The question that unpicks it: *"If I ask 300 people at cricket practice, does cricket stop winning?"*

**Misconception 2: "The average is the answer."** A student computes 16.4 and treats it as a fact about meals in general. It is a fact about *thirty specific meals eaten by one person over ten days in September*. The fix is a sentence shape you will drill today: "The average of my sample is 16.4 minutes" — legal. "Meals take 16.4 minutes" — not legal.

**Misconception 3: "Writing 'unknown' means I failed."** Students hate leaving blanks and will invent an answer to avoid one — exactly the instinct that fills a missing cell with 0. Praise "unknown" loudly and early. It is a finding, not a gap in their effort. When a web page will not say who collected its numbers, **the page failed, not the student.**

### How deep to go — and where to stop

**Go this deep:** the five questions; population vs sample with the soup; the cricket survey; the seven-line card; three "does not show that" sentences; `=AVERAGE`; blanks are skipped.

**Stop before:**

| Do not raise today | Because |
|---|---|
| Margin of error, confidence intervals, "±3%" | Real, and years away. If asked: "there is a way to measure how much luck is in a number, and it needs maths you will meet later" |
| Random sampling procedures, stratification | Beyond Level 1. "Stirred" is the whole idea and it is enough |
| Median, mode, standard deviation | We use one summary number this year: the mean. Mentioning the median is fine; teaching it is not |
| Measuring bias with numbers | That is Week 31, with their own model, and it needs the accuracy tools from Weeks 19–22 |
| Any formula except `=AVERAGE` | `=SUM` and `=COUNT` are fine if the student asks. Nothing else. This is not a spreadsheet course |
| Where ChatGPT's training data came from, in detail | Answer honestly and briefly — see the Questions section — then park it. Week 28 does language properly |

**One thing you may say plainly without naming it:** two things happening together does not mean one caused the other. Heavy-bag days were also test days; the table cannot separate them. Say it in exactly those concrete words. Do **not** introduce the phrase "correlation is not causation" — the words add nothing an 11-year-old can use, and Week 7's pattern work is where this gets its proper treatment.

### If you have five spare minutes before class

Open any news story with a statistic in it and ask the five questions out loud, writing your answers down. Most stories will leave you with three or four "unknown"s. Do this once and you will teach this lesson with genuine conviction instead of borrowed conviction — and you will have a second live example in your pocket if the first web page disappoints.

---

### 🧭 The Growing Map — Week 6's frame

Last week on this tile. The picture is the same as Weeks 4 and 5 — THE TABLE tinted and badged — and
this is the frame where you can say the tile is finished and tell them where the map moves next.

![The course map after Week 6: the table tile is finished](../figures/fig-w06-0-where-this-fits.svg)

*Figure 6.0 — Week 6's version. Third and final week on THE TABLE, its full run being "wk 4-6", with
**data** and **impact** lit along the bottom.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it, then ask** *"which bit did we do today?"* THE TABLE, for the third time — the two averages,
   the five provenance questions, the card they wrote. Then ask the better version: *"what were the
   three weeks on this one tile about?"* Row, mess, origin. That is the tile, complete.
2. **Then ask** *"what's still dashed?"* Seven tiles, and the nearest is FEATURES in Week 11. Tell them
   plainly that next week the map changes on the **left** side of the fork for the first time since
   Week 1 — the person's room finally subdivides. A promised change is a reason to come back.
3. **Have them finish the tile on their own map** — colour it and write "wk 4-6" under it. First tile
   they have watched fill over more than one week, and it is worth pausing on for ten seconds.

> **🧑‍🏫 Why this is worth two minutes.** Weeks 4 to 6 are the driest stretch in Level 1, and this is
> the frame where the learner gets to see them add up to one finished box. Closing a tile out loud is
> what stops three weeks of spreadsheets feeling like an unexplained detour.

**The six threads** along the bottom: **data · representation · model · learning signal · evaluation
· impact.** Two lit — **data** (where the rows came from) and **impact** (who is missing from them).
Orientation, not assessment: no marks, no quiz.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Print the whole Workbook Week 6** (Warm-Up, Practice Sets A and B, Puzzle, Think Deeper, Build It, Draw It, Self-Check; the Answers section at the end is the student's own check, so print without it or fold it under). The **Build It** page is the one that must exist on paper, because it holds the blank "My data card" table; writing a card in a text box on a screen kills it.
- [ ] **Get a spreadsheet working, and type `=AVERAGE` yourself.** Five minutes. Open [sheets.google.com](https://sheets.google.com) (or Excel, or LibreOffice), make a blank sheet, type the numbers 2, 4, 6 down cells A1, A2, A3, click A5 and type `=AVERAGE(A1:A3)`, press Enter. It must show **4**. If it shows `=AVERAGE(A1:A3)` as text, you missed the `=`. **Do not skip this step.** Reading about it is not the same as your fingers having done it.
- [ ] **Check the student can get in.** If they need a Google account they do not have, decide tonight: use your account, use Excel/LibreOffice, or use the paper fallback. Do not discover this at minute 26.
- [ ] **Pick your web page and open it in a tab.** Any page with a statistic: a news article with a percentage, a sports statistics page, a Wikipedia table, a product review score. **Choose one that will frustrate you slightly.** A page that answers all five questions makes for a lovely dataset and a dead lesson. A page that answers two is perfect.
- [ ] **Ask the five questions of that page yourself and write your answers on a sticky note.** Ten minutes, and it is the difference between running the activity and watching it. Count your "unknown"s so you know what is coming.
- [ ] **Check the student's table.** They should have 21+ rows. If they have 8, read the fallback table now and decide your plan before class rather than during it.

### 5 minutes on the day

- [ ] Board: write the two sleep averages, `5.9` and `7.8`, and nothing else. Cover them or turn the board round.
- [ ] Laptop open, blank spreadsheet on screen, web page in a second tab, screen brightness up.
- [ ] Workbook open to Build It, "My data card" table, face down on the desk.
- [ ] The student's own table on the desk, next to the laptop.
- [ ] Their Week 5 fault log where you can both see it — it becomes line 6 of the card.

### If something fails

| If this fails | Do this instead |
|---|---|
| **No internet** | Do the whole lesson on paper. Compute the two averages by hand — that is 30 additions and one division, it takes six minutes, and it makes "blanks are skipped" concrete because *they* have to decide what to divide by. For the provenance half, use the two sleep datasets from the Hook plus any statistic printed on a food packet, a shampoo bottle ("93% of women agreed") or a schoolbook. Packaging statistics are magnificently unprovenanced. |
| **No Google account** | Excel or LibreOffice Calc, identical steps. Or `sheet.new` on an existing account of yours. Or paper. Nothing in this lesson depends on Google. |
| **The spreadsheet eats the time** | Hard stop at minute 40 regardless of how many rows are typed in. Ten rows entered and a data card written beats thirty rows entered and no card. The card is the objective; the typing is not. |
| **Your chosen web page answers all five questions** | Congratulations, that is a genuinely well-documented source and it happens. Say so out loud, praise it, then open any second page — a social media statistic, a "9 out of 10 dentists" advertisement — and compare. The contrast teaches better than the failure would have. |
| **The student has only 8–10 rows** | Run the lab on the rows they have and say the honest thing: "your sample just got smaller, so your card has to say so." Change nothing else. A card that reads "10 rows, 3 days" is completely valid and slightly more interesting than a tidy 30. |
| **The student refuses to write "do NOT use for"** | Do it as a game: you make three deliberately outrageous claims from their table ("so all children eat rice for lunch") and they have to shoot each one down. Their rebuttals *are* line 7. Write them down as they speak. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | 🪝 **Hook** — two true numbers, two hours apart | Both datasets are honest. They still disagree. |
| 8–26 | 🧠 **Concept** — soup, samples, and the five questions | Population vs sample, the cricket survey, the five questions on the board. |
| 26–40 | 🔍 **Worked Example Together** — the spreadsheet half | Type the table, compute two averages, then say what they are *not*. |
| 40–60 | 🎲 **Activity** — the interrogation and the card | Five questions on a real web page, then the seven-line card, read aloud. |
| 60–70 | 🔑 **Wrap & Assign** | Three "does not show that" sentences, takeaways, homework. |

**Running 60 minutes?** Cut the Worked Example to 8 minutes by entering only 10 rows, and the Wrap to 6. Do **not** cut the card or the reading-aloud.
**Running 75?** Take the extension questions from Differentiation, or interrogate a second web page of the student's own choosing.

---

### 🪝 Hook — Two true numbers, two hours apart (0–8)

**Do this:** reveal the board. It says only:

```
Dataset A:  average sleep = 5.9 hours
Dataset B:  average sleep = 7.8 hours
```

**Say this:**

> "Two research teams both wanted to know the same thing: how many hours do teenagers sleep? Both of them did it properly. A thousand rows each. One row per teenager. Nobody made anything up, nobody typed 88 by mistake, and I have checked both tables with all four of last week's checks. No blanks. No duplicates. No impossible values. No four spellings of Monday. Both tables are **clean**.
>
> Team A got five point nine hours. Team B got seven point eight hours. That is a gap of nearly two hours a night. If you were writing a newspaper headline, one of these says 'teenagers are exhausted, this is a crisis' and the other says 'teenagers are basically fine.'
>
> Here is my question, and I want you to think before you answer. **Which team made the mistake?**"

**Ask this:** *"Which team got it wrong?"*

- **Hoping for:** hesitation, then "you can't tell from that." Perfect. Say so: "Right. You cannot tell. So what would you need to know?"
- **If they say "the small one is wrong":** they are both a thousand rows. Say it and watch the theory collapse. That collapse is useful.
- **If they say "average them, so about 6.8":** brilliant wrong answer, take it seriously. Ask: "If I measured a giraffe and a mouse, is the average a useful animal?" Averaging two answers to two different questions gives you an answer to no question at all.
- **If they say "neither, they measured different people":** you have a strong student. Do not skip ahead — make them tell you *which* different people, and let them discover they cannot know from the board.

**Do this:** now reveal the provenance. Write under each number:

```
Dataset A:  average sleep = 5.9 hours   <-  1,000 visitors to a SLEEP-PROBLEMS CLINIC
Dataset B:  average sleep = 7.8 hours   <-  every student in 4 RANDOMLY CHOSEN SCHOOLS
```

**Say this:**

> "Nobody made a mistake. Every single row in both tables is correct.
>
> But look at who is in Dataset A. To get into that table you had to walk into a sleep clinic — and you only walk into a sleep clinic if you already have a sleep problem. That is the ticket to get in. So Dataset A honestly answers a different question: *how much do teenagers with sleep problems sleep?* Five point nine hours. Probably true. Completely useless for the question that was asked.
>
> And here is the part I want you to feel slightly annoyed about. **Nothing in the numbers told us that.** You could stare at those thousand rows all week. You could check every cell, average every column, draw every graph. The problem is not in the table. The problem is in one sentence *about* the table — a sentence somebody nearly forgot to write down.
>
> That sentence has a name. It is called **provenance**: who collected the data, from whom, when, how, and with whose permission. Today we learn to ask for it, and to write it for our own data. And by the end of the lesson you will have said, in writing, three things your own thirty rows do **not** prove."

---

### 🧠 Concept — Soup, samples, and the five questions (8–26)

**Say this:**

> "Start with soup. You are cooking a big pot of soup and you want to know if the whole pot needs salt. You do not drink the pot. You stir it, take one spoonful, taste it, and decide.
>
> That works. And it works for one specific reason: **you stirred**. If you skim your spoonful off the top without stirring, you get the oily layer floating on top, and you tell everyone the soup is greasy — and you are wrong about the pot even though you were completely right about your spoonful.
>
> So here is the sentence I want you to remember all year: **stirring matters more than spoon size.** A well-stirred teaspoon beats an unstirred ladle. Every time."

**Do this:** draw the two-word diagram on the board — this is the core board work of the lesson and everything else hangs off it.

```
  POPULATION  =  everything I want my answer to be true about
                 (the whole pot)

      SAMPLE  =  what I actually measured
                 (my one spoonful)
```

**Say this:**

> "Two words, and they are the two most useful words in the whole term.
>
> The **population** is everything you wish your answer covered. The **sample** is the little bit you actually got your hands on. They are almost never the same, and the gap between them is where nearly every wrong number in the world lives.
>
> Let me show you a survey that lies, and lies without a single mistake in it."

**Do this:** write the cricket survey on the board, **without** the provenance line at first.

```
Question:  favourite sport at my school?     School = 800 students

Asked 30 students:      cricket   22   (73%)
                        football    5   (17%)
                        badminton   3   (10%)
```

**Ask this:** *"Do you believe cricket wins, 73%?"*

- **Hoping for:** "yes" or "probably" — good, let them commit. Commitment makes the reveal land.
- **If they immediately say "depends who you asked":** excellent. Say "Ask me, then." Let them ask, and reveal it as their discovery rather than yours.

**Do this:** now add one line.

```
I asked 30 people ...  AT CRICKET PRACTICE.
```

**Say this:**

> "Everything in that table is honest. Thirty real students, thirty real answers, arithmetic correct. And the answer is rubbish, because I dipped my spoon in the one part of the pot where the cricket had collected.
>
> Now here is the cruel bit. Run last week's four checks on my thirty rows. Any blanks? No. Any duplicates? No. Anything impossible? No — every answer is a real sport. Any inconsistent spellings? No, I used a controlled vocabulary like a good student. **My table passes every single check from last week and it is still lying.** That is why we needed a new lesson. Clean is not the same as trustworthy."

**Ask this:** *"If I ask 300 people at cricket practice instead of 30, does cricket stop winning?"*

- **Hoping for:** "no." Then push: "Why not?" You want "because they are all still cricket people." That is the whole idea of bias, in their own words, and it will come back in Week 31.
- **If they say "yes, 300 is more accurate":** go back to the soup. "Is an unstirred ladle better than an unstirred teaspoon?" Then: "More data makes a wrong answer look *more* convincing. That is worse, not better."

**Say this:**

> "So how do you fix it? Honestly — often you cannot. You are eleven. You are not going to survey eight hundred students, and you should not pretend otherwise.
>
> But there is something you can always do, and it costs one sentence: **write down who is in your sample and who is missing.** 'This is thirty students from cricket practice; it under-represents students who do not play sport.' The moment you write that, you have not fixed your data — you have turned a lie into an **honest limited finding**. Those two words are what I want from you today. Not a perfect finding. An honest limited one."

**Do this:** write the five questions on the board, numbered, leaving room to the right of each for answers. This list stays up for the rest of the lesson.

```
1. Who collected it?
2. From whom?
3. When?
4. How, exactly?
5. With whose permission?
```

**Say this:**

> "These five questions are your whole toolkit. They take about a minute to ask and they will save you from believing rubbish for the rest of your life.
>
> And there is a sixth rule that goes with them: **if you cannot find the answer, you write the word 'unknown'.** Not a guess. Not 'probably scientists'. The word unknown. Writing unknown is not failing — it is a finding, and it is a finding about the *source*, not about you. When a web page will not tell you who collected its numbers, **the page failed the test, not you.**"

**Ask this:** *"Which of the five questions would have caught the sleep-clinic problem?"*

- **Hoping for:** number 2, "from whom". Exactly right. Point at it on the board.
- **If they say "how":** defensible and worth a nod — "how, exactly" would surface "we surveyed patients at a clinic". Accept it, then ask which single word in the question is doing the work, and steer to "from whom".

---

### 🔍 Worked Example Together — The spreadsheet half (26–40)

This is the first half of the lab. **You drive for the first two minutes; the student's hands are on the keyboard after that.**

**Say this:**

> "Right. Laptop. We are going to move your table into a spreadsheet, and then we are going to compute two averages — and then, immediately, before we get too pleased with ourselves, we are going to write down what those averages are **not** evidence for.
>
> Four facts about a spreadsheet and then we start. One: columns have letters, rows have numbers, so every box has a name. That box is A1. That one is D5. Two: your column names go in row one, so your data starts in row two. Three: if you type an equals sign, the spreadsheet computes something for you. Four — and this is the one that matters — it **skips empty boxes**, and it does not tell you when it does. Hold on to that one."

**Do this:** open a blank sheet. Type the student's four or five column headers into row 1 as they dictate them. Then hand over the keyboard. They type their own rows.

Set the target out loud: **as many rows as exist, and stop at minute 36 no matter what.** If they have 21 rows, that is 21 rows. Typing is not the objective.

> **💡 Try this:** if typing is slow or handwriting is bad, split it — you read the values aloud from
> the paper table and they type. Twice as fast, and it forces them to say every value, which catches
> faults last week's homework missed.

**Do this:** at minute 36, stop the typing. Click an empty cell three rows below the data. Say the cell's name aloud as you click it: "I am in D34."

**Say this:**

> "Now the formula. Equals, then A-V-E-R-A-G-E, then a bracket, then the first box of the column, then a colon, then the last box, then close the bracket. The colon means 'everything from here to there'. Enter."

Type it together: `=AVERAGE(D2:D31)`.

![Two averages in a spreadsheet](../figures/fig-w06-6-sheets-average.svg)
*Figure 6.5, again — exactly what the screen should look like. Note that the formula goes in an empty cell **below** the data, never inside it.*

**Say this:**

> "Sixteen point four. It did thirty additions and one division in less time than it took me to say 'average'. That is genuinely worth being impressed by.
>
> Now do the same for the other number column."

Do the second average — for the meals table, `=AVERAGE(E2:E31)` → **2.9**.

**Ask this:** *"How many numbers did it add up to get that?"*

- **Hoping for:** "thirty." Then spring it: *"You had two blank boxes. Did it add thirty, or twenty-eight?"* The answer is twenty-eight, and the spreadsheet said nothing.
- **If they say "I don't know":** good, that is the honest answer. Show them: type `=COUNT(D2:D31)` in the next cell. It reports how many boxes actually held a number. If it says 28, the machine has just quietly told you something it would never have volunteered.
- **If they have no blanks:** say what *would* have happened, and then praise them properly. Thirty rows with no blanks is real discipline.

**Say this:**

> "So it divided by twenty-eight, not thirty, and it never mentioned it. That is not a bug — it is the right thing to do with a blank. But now remember last week's rule: **never fill a blank with a zero.** If you had typed 0 in those two boxes, the spreadsheet would have counted them, and your average would have dropped for a reason that never happened. A blank gets honestly skipped. A fake zero gets honestly believed. Same-looking table, opposite outcomes."

**Do this:** now the important two minutes. Turn away from the screen. On paper, write two sentence-starters and fill them in together, out loud.

```
This average IS evidence that ....................
This average is NOT evidence that ................
```

**Say this:**

> "Sixteen point four minutes. Say it back to me in a sentence that is definitely true."

**Ask this:** *"What is this average actually evidence of?"*

- **Hoping for:** something like "my thirty meals took 16.4 minutes on average, in September." Full marks for any version that names *whose* meals and *when*.
- **If they say "meals take 16.4 minutes":** stop, gently, and ask: "Whose meals? Which meals? When?" Then have them say it again with those three things in it. Do this every single time; it is the sentence habit the whole lesson is trying to build.
- **If they say "nothing, it's just my data":** too modest, and worth correcting. It is real evidence about a real sample. "Your data proves something small and true. Small and true is exactly what we are aiming at."

---

### 🎲 Activity — The interrogation and the card (40–60)

Full instructions in the next section. In brief: **eight minutes** interrogating a real web page with the five questions, then **ten minutes** writing the seven-line data card, then **two minutes** reading it aloud, standing up.

**Say this to launch it:**

> "Two jobs. First we are detectives on somebody else's data. Then we are the ones being investigated.
>
> I have a web page here with a number on it. We are going to ask it all five questions, out loud, in order, and I am going to write your answers on the board. And every time the page will not tell us, we write **unknown** — cheerfully, in big letters. I want to see how many unknowns we can collect. My guess is three."

Do not skip the reading-aloud. Two minutes, standing, out loud, to you. It converts a worksheet into a claim the student is willing to defend, and that shift is the entire point of the exercise.

---

### 🔑 Wrap & Assign (60–70)

**Do this:** show or draw the three-sentence warning panel.

![What this data cannot tell you](../figures/fig-w06-4-cannot-tell-you.svg)
*Figure 6.6 — Three worked examples. Copy the shape of the sentence, not the numbers — these come from a couple of different sleep tables, not from yours.*

**Say this:**

> "Last job of the day, and it is the one I will read first in your homework. Three sentences, each one starting **'This does not show that…'**
>
> Look at how the ones on the panel work. It is not 'my data might be wrong'. That sentence is worth nothing — anything might be wrong. Every good one names *the exact thing that is missing*. 'This does not show that other children sleep the same amount, because my sample is one person.' 'This does not show that a heavy bag makes me sleep badly, because heavy-bag days were also test days and I never separated the two.' 'This does not show anything about weekends, because Saturday is not in the table.'
>
> Each one names a hole. That is the difference between being vague and being honest."

**Ask this:** *"Give me one right now, about your own table."*

Take whatever comes and improve it together on the spot. If they produce "this does not show that everyone eats like me", accept it and then sharpen it: "everyone — who is everyone? And why not? Say the reason." Push until the reason names something specific and missing.

**Do this:** the takeaways, on the board or read aloud.

> **🔑 Takeaways**
> 1. **Provenance is part of the data.** Who collected it, from whom, when, how, and with what permission changes what the numbers mean — and nothing in the numbers reveals it.
> 2. **Your sample is not the population.** You usually cannot fix that. You can always write down who is missing.
> 3. **Stirring beats spoon size.** More data does not fix a badly chosen sample; it just makes a wrong answer look more convincing.
> 4. **A data card turns a spreadsheet into something trustworthy** — especially line 7, the line saying what it must not be used for.
> 5. **"Unknown" is an honest answer**, and a common one. Guessing is not.

Then assign the homework using the words in the Homework section, and check the fault log is stapled to the card.

---

## 🎲 The Activity, In Full

### Data Card Workshop

**What it is:** a two-part lab. Part 1 (already done in the Worked Example segment) puts the table into a spreadsheet and computes two averages. Part 2 interrogates somebody else's data, then turns the interrogation around on their own.

**Time:** 20 minutes — 8 for the interrogation, 10 for the card, 2 for reading it aloud.

### Materials

- The web page you chose, open in a tab
- Board or big paper with the five questions already numbered down the left
- Workbook Week 6, Build It, the blank "My data card" table, **on paper**
- The student's Week 5 fault log
- The completed averages from the first half

### Setup (1 minute)

Five questions numbered on the board with space to their right. Web page on screen, scrolled to the top. Blank data card face down until the interrogation is finished — do not let them start writing their own card while still thinking about somebody else's.

### Part 2a — The provenance interrogation (8 minutes)

**Rules:**

1. **The student asks the question out loud.** Not you. They read question 1 off the board and say it.
2. **You hunt on the page together.** Scroll, look for a "methods" or "about" or "sources" link, check the small print at the bottom, check the date at the top.
3. **You write the answer on the board.** In their words, not yours.
4. **Ninety seconds per question, maximum.** Then you write what you have got and move on.
5. **"Unknown" is written in full and out loud.** Not a dash, not a shrug. The word.
6. **No guessing.** "Probably scientists" becomes "unknown". Say why: a guess written down looks exactly like a fact three weeks later.

**What a finished interrogation looks like.** For a typical news article about screen time:

| # | Question | What the page said |
|---|---|---|
| 1 | Who collected it? | "A university survey" — no name, no link → **half answered** |
| 2 | From whom? | **Unknown.** It says "teenagers". Which teenagers? Where? |
| 3 | When? | Article dated this year; the data's date → **unknown** |
| 4 | How, exactly? | "Survey" — online? paper? asked at school? → **unknown** |
| 5 | With whose permission? | **Unknown.** Not mentioned at all. |

Three or four unknowns out of five is the normal result. When you get it, say the line that matters:

> "This number is on a real news site, in a real article, and we cannot answer four of the five
> questions about it. That does not make it false. It makes it **unchecked**. And now you know the
> difference, which most adults do not."

> **⚠️ Watch out:** do not let this curdle into "everything on the internet is lies." That is a
> different and lazier lesson. The point is not that sources are bad; it is that a number with
> provenance can be checked and a number without it can only be believed or not believed. Say that
> out loud if the mood tips towards cynicism.

### Part 2b — Writing the card (10 minutes)

Hand over the Build It page. Seven lines, the rows of the "My data card" table, in order. Read each line's prompt aloud, give them a minute, move on. Do not let them polish line 1 for four minutes — the last two lines are worth more than the first five put together.

Timing inside the ten minutes:

| Line | Time | The thing to watch for |
|---|---|---|
| 1. What it is | 60 s | Must include what one row is |
| 2. How much | 60 s | Rows × columns, and real dates |
| 3. Who collected it | 60 s | "Me" is not enough — *how* did they do it? |
| 4. Who it is about | 60 s | If any other person appears, this must say so |
| 5. Permission | 60 s | For a solo dataset: "my own data, a parent checked it" |
| 6. **Known gaps** | 3 min | **Copy from the Week 5 fault log.** Blanks, deletions, the outlier |
| 7. **Do NOT use for** | 3 min | At least two claims. This is the graded line |

The completed example to hold up if they stall is Figure 6.4. Let them read it for thirty seconds, then take it away — a visible model gets copied word for word, and a card in somebody else's words is worthless.

### Part 2c — Reading it aloud (2 minutes)

Standing up, facing you, all seven lines, no apologising. Then one question from you and one only:

> *"Would you be happy for someone to make a decision using this data, after hearing that card?"*

Any answer is fine. The question is the point. It is the first time this year the student is asked to take responsibility for a dataset rather than just produce one, and it is a moment they tend to remember.

### What "finished" looks like

- [ ] The table is in a spreadsheet, with headers in row 1 and data from row 2 down
- [ ] Two averages computed with `=AVERAGE`, and both written on paper as well as on screen
- [ ] One sentence saying what each average **is** evidence for, naming whose data and when
- [ ] The five questions asked of a real web page, with every answer written down, including the unknowns
- [ ] All seven lines of the card filled in, on paper, in their own words
- [ ] Line 6 traceable to the Week 5 fault log
- [ ] Line 7 naming at least two claims the data cannot support
- [ ] The card read aloud, standing

### Variation — easier

Cut the spreadsheet entirely and do the averages on paper — 30 additions is not beyond a Grade 6 student and it makes "what do I divide by?" a real question they have to answer themselves. For the interrogation, use a shampoo bottle or a cereal packet instead of a web page: "93% of women agreed" has beautifully absent provenance and needs no scrolling. Give the card as a fill-in-the-gaps version where lines 1 to 5 are half-written and they complete lines 6 and 7 only. Those are the two that matter.

### Variation — harder

Three extensions, in increasing order of difficulty:

1. **Two pages, one number.** Find the same statistic on two different pages. Do they cite the same source? Usually they cite each other, in a circle, and the original never appears. Ask them to draw the circle.
2. **Design the stirred sample.** "You want the real favourite sport of all 800 students, and you get one hour and no help. Write the plan." Then the sting: *"Name one thing that is still wrong with your plan."* Every plan has something. A student who finds their own plan's flaw has arrived somewhere real.
3. **Write the card for the data you did not collect.** What would a card look like for the *missing* thirty rows — the weekend meals, the days they forgot? Naming the shape of an absence is genuinely hard and genuinely useful.

---

## ❓ Questions Students Ask This Week

**"If my data is only about me, is it useless?"**
No — it is the opposite. It is the only dataset in the world where you know the answers to all five provenance questions. That makes it more trustworthy than almost anything you will find online. It is just *narrow*: it is evidence about you, in September, doing your usual routine. Narrow and honest beats broad and unchecked. Every professional dataset started as somebody's narrow one.

**"How many rows do I need before it counts?"**
**Nobody knows for sure, and here is why.** There is no fixed number, because the answer depends on how varied the thing you are measuring is. If every meal you eat takes exactly 15 minutes, three rows tell the whole story. If your meals swing from 4 minutes to 40, even a hundred rows will wobble. Statisticians have real maths for estimating how much luck is left in a number, and even with that maths they argue about the answer, because it depends on how wrong you can afford to be. The honest working rule for this year: **more rows shrink the luck, but no number of rows fixes a badly chosen sample.** Thirty is enough to see a pattern and not enough to prove one — which is exactly why your card says so.

**"Why can't the computer just check whether data is trustworthy?"**
Because trustworthiness is not in the data. Go back to the two sleep tables: both clean, both correct, two hours apart. The difference lived in one sentence *about* the table — a sentence written by a person who chose to write it. A computer can check for blanks, duplicates, impossible values and inconsistent spellings, all four of last week's checks, in a fraction of a second. It cannot check who walked into the clinic. Only a human who was there can tell you that, and only if they bothered to write it down.

**"Where does ChatGPT's data come from?"**
Mostly enormous amounts of text collected from the internet — web pages, books, forums, code — plus a lot of human writing and rating done afterwards to shape the answers. But here is the honest part: for most of the big systems, the full list is **not published**. So if you ask the five provenance questions about ChatGPT's training data, several honest answers are "unknown", and that is not you failing to research it — it is genuinely not public. Some researchers think that is a serious problem for exactly the reason we learned today: you cannot say who a model's answers are about if you cannot say who its data came from. We will build our own tiny language machine in Week 28, and you will know its provenance completely, because you will be it.

**"Is it stealing to use somebody's data?"**
Sometimes, and the honest answer is that the world has not settled this. Some things are clearly wrong: taking a friend's data after they said no, or publishing someone's name and address. Some are clearly fine: your own numbers. In between there is a huge argued-about middle — photos posted publicly years ago and later used to train models, artwork used without asking, medical records shared for research. Courts and governments are working through it right now, and different countries have landed in different places. Our rules for this course are strict and simple: **ask first, use initials, never addresses or faces.** Week 32 goes properly into this.

**"If I ask everyone in my class, is that the whole population?"**
It depends entirely on the question. If your question is "what is my class's favourite sport?", then yes — you measured every single member of the population, which is a wonderful position to be in. If your question is "what is my school's favourite sport?", your class is a sample of 30 out of 800, and probably an unstirred one, because friends tend to like the same things. **The same thirty rows are a whole population for one question and a biased sample for another.** The rows did not change. The question did.

**"Can I delete the weird row so my average looks nicer?"**
No, and you already know why from last week. If it is *impossible* — a negative weight, an 88-hour night — blank it and note it. If it is legal but far from the others, it is an **outlier**, and it stays. Then it goes on line 6 of your card: "one day of 480 screen-minutes, I was home sick." Deleting it to make an average tidier is choosing your answer first and picking the data to match, which is the one thing a person working with data is never allowed to do.

**"Does writing 'unknown' five times mean I did the homework badly?"**
No. It means the source documented itself badly, and you found that out — which is a result. A card with three honest unknowns is worth far more than a card with three confident guesses, because a guess written down looks exactly like a fact three weeks later. Nobody, including you, will remember which lines were guessed.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The spreadsheet eats 25 minutes** and there is no time for the card | Typing is visible progress and feels productive; the card feels like homework | Hard stop at minute 40 with however many rows exist. Say it out loud: "Ten rows and a card beats thirty rows and no card." The card is the objective |
| **The student treats the average as a fact about the world** — "meals take 16.4 minutes" | Averages sound official. A single number feels more true than thirty messy ones | Every time, ask the three questions: "Whose meals? Which meals? When?" Then make them say the sentence again with all three inside it. Repetition is the whole fix |
| **"More data would fix it"** survives the whole lesson | It is a deeply held belief and it is sometimes true, which makes it sticky | Return to the soup, hard: "Is an unstirred ladle better than an unstirred teaspoon?" Then the killer question: "Does asking 300 cricket players change the answer?" |
| **They guess rather than write "unknown"** | Blanks feel like failure. This is the same instinct that fills a missing cell with 0 | Praise the first unknown loudly and visibly. Write it in big letters yourself. Add: "This tells us about the website, not about you" |
| **Line 7 comes out as "do not use for anything"** | It is technically safe and requires no thinking | Reject it kindly: "That is a cop-out and you know it. Your data proves something small and real. Tell me the smallest true thing it proves — and then what it does not" |
| **They can't tell population from sample and the words start swapping** | Two new abstract nouns arriving in the same eighteen minutes | Drop the words for five minutes. Use "the whole pot" and "my spoonful" only. Reattach the formal words at the very end, one at a time |
| **Cynicism sets in — "so all statistics are lies"** | The interrogation produces four unknowns and that feels like a verdict on everything | Correct it immediately: a number with provenance can be *checked*; a number without it can only be believed or not. The goal is checking, not disbelieving. Then show a well-documented source — a census page, a school's own attendance figures — so they have seen a good one |
| **The Week 4–5 homework barely exists** | Three weeks of daily collection is genuinely hard | Run the lab on 8 rows without complaint and make the small sample *the finding*: "Your card is going to say 8 rows, 3 days, and that is an honest card." Then set a realistic new target |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** the spreadsheet (do averages by hand), the second average (one is enough), and the web page interrogation (use a shampoo bottle or cereal box instead — the five questions still work and there is no scrolling).

**Reteach with this and nothing else:** the soup. Get an actual bowl or mug of something if you can. Stir it, taste, then skim the top without stirring and taste again. Two tastes, ninety seconds, and the abstraction disappears.

**Reduce the card** to three lines: What it is / What is missing / Do not use for. Those three carry most of the value. Add the other four next week if you like; nothing downstream breaks.

**Accept spoken answers for line 7.** Let them talk and you write. The thinking is the objective; the handwriting is not.

### If they are flying

Extension questions, in order of difficulty:

1. "Your card says thirty rows. Write the card for the thirty rows you *did not* collect — the weekends, the days you forgot. What would be in it?"
2. "Design a stirred sample of our school in one hour with no help. Then name one thing still wrong with your plan." *(Every plan has one. Finding your own is the skill.)*
3. "Find the same statistic on two web pages. Do they cite the same original source, or each other?" *(Usually each other, in a circle, with the original nowhere.)*
4. "Dataset A was collected at a sleep clinic. Invent a question for which Dataset A is the **better** dataset." *(A good answer: 'how well do treatments at this clinic work?' Biased for one question is perfect for another — that is a genuinely sophisticated idea and it is available to a strong 11-year-old.)*
5. "Your average is 16.4 minutes. If I deleted your single longest meal, what happens to it — and what does that tell you about how solid the 16.4 is?" *(It moves noticeably, because thirty rows is small. That felt fragility is the beginning of statistics.)*

### If they won't engage today

Do the interrogation only, and make it a game. **You** defend the web page; **they** attack it. You play the smug journalist who insists the number is fine; they have to make you admit you cannot answer question 2. Ten minutes, and it delivers objective 2 on its own.

If even that fails, fall back to the smallest real version: ask the five questions about **something in the room**. A food packet. A shoe's size label. A school notice claiming "attendance is up". Five questions, three minutes, written down. That is a complete, honest lesson and it needs no worksheet, no screen and no enthusiasm.

Whatever happens, do not spend the session arguing about the missing homework rows. Rows can be collected next week. The habit of asking where a number came from is what today was for.

---

## ✅ Assessing Understanding

Three checks, last five minutes, about four minutes total.

### Check 1 — Population and sample (60 seconds)

Ask, in exactly these words:

> "Point at your table. What is the population, and what is the sample?"

**A good answer** names both and keeps them straight: *"The population is all the meals I will ever eat. The sample is these thirty meals, from ten days in September."*

**A weaker answer** describes the sample twice: *"The population is my thirty meals and the sample is the table."* Prompt once: "Do you only care about those thirty meals, or about your meals in general?" That question usually fixes it.

### Check 2 — The unknown (45 seconds)

> "Which of the five questions could you not answer about that web page, and what did you write?"

**A good answer** names a specific question and the word: *"Question two, from whom. I wrote unknown, because it only said 'teenagers'."* You are checking two things: that they remember which question failed, and that they are not embarrassed by having written unknown.

### Check 3 — The sentence that must not be said (90 seconds)

> "I am going to say a sentence about your data. Tell me whether it is allowed, and why."
>
> *"Meals take sixteen point four minutes."*

**A good answer** rejects it and repairs it: *"Not allowed — that is about all meals everywhere. Mine took 16.4 on average, over ten days in September."* The repair is what you are marking.

**A weaker answer** accepts it. Then ask: "Whose meals? Measured when?" and have them try again. If they still accept it, that is a level 2 and the sentence drill is where the next session should start.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Uses "population" and "sample" interchangeably. Treats the average as a fact about everyone. Guesses rather than writing unknown |
| **2 — Emerging** | Can define sample and population when asked, but slips back into over-claiming in the very next sentence. Card lines 1–5 filled in, 6 and 7 thin or missing |
| **3 — Secure** | Names the population and sample for their own table correctly and unprompted. All seven card lines written. Asks all five questions and writes unknown without discomfort. Produces one solid "does not show that" sentence |
| **4 — Strong** | Three specific "does not show that" sentences, each naming exactly what is missing. Explains why 300 cricket players do not fix the survey. Line 6 of the card traceable to the fault log |
| **5 — Exceptional** | Argues that a biased dataset can be the *right* dataset for a different question, with an example. Spots that their own thirty rows are a whole population for one question and a biased sample for another. Names a flaw in their own improved sampling plan |

Write the level in your own notes. Week 9's Term 1 Checkpoint asks for it, and Week 31 revisits this exact ground with the student's own model.

---

## 📤 Homework to Assign

**Workbook Week 6, all sections — Warm-Up, Practice Set A, Practice Set B, Puzzle of the Week, Think Deeper, Build It (finish "Your Life In 30 Rows" plus the data card), Draw It, Self-Check.**
**Time: 45–60 minutes across the week.**

The workbook is meant to be done in its printed order, about 45–60 minutes across the week; **Build It takes about 20 of those**. In class the student only drafts the "My data card" table (Part 2b of the activity); everything else in the workbook is home work, and the card is finished there. Tell the student that the Warm-Up and Practice Sets are quick, and that **Build It is the part you will read first.**

**Say this:**

> "This is the last instalment. After this week, the table is finished and it is yours — and in Week 7 we use it to hunt for patterns, so it is about to earn its keep.
>
> **One. Finish the rows.** Get to thirty. If you cannot get to thirty, get as close as you honestly can and then **write the real number on your card**. Do not invent rows to reach a round number. An invented row is worse than a missing one, because a missing one is visible.
>
> **Two. Both averages, written on paper.** Not just on the screen. Write the number, and next to it write what it is the average *of* — how many rows went into it. If two boxes were blank, the average came from twenty-eight, and your paper should say twenty-eight.
>
> **Three. The seven-line card, finished properly.** Line six comes straight from your fault log — every blank, every deletion, every outlier you kept. Line seven needs at least two things your data must not be used for.
>
> **Four, and this is the one I will read first. Three sentences, each starting 'This does not show that…'** Each one has to name the exact thing that is missing. 'This does not show that other people eat like me, because my sample is one person.' That works. 'This might be wrong' does not work — anything might be wrong. That sentence tells me nothing and it costs you nothing to write, which is how I know it is empty.
>
> **Five. Get one of those three sentences checked by an adult.** Read it to them and ask one question: 'Does this make sense to you?' If they look confused, your sentence is not finished. Write down what they said, even if what they said was 'I don't get it.' Especially then."

The five spoken instructions below are the Build It page ("My two averages", "My data card", "My three sentences", "The adult check"). Say them after the sections above are on the table.

**What to check when it comes in:** the row count on the card matches the actual number of rows; both averages appear on paper with the count they were computed from; line 7 names at least two forbidden claims; and each of the three sentences names something specific and missing rather than just expressing doubt. Then mark the other sections from the Answer Key below, which follows the workbook's own order; the answers are also printed at the end of the workbook, so a student can self-check Warm-Up through Think Deeper.

---

## 🔑 Answer Key

Complete answers to everything asked in this lesson and in Workbook Week 6.

### Lesson questions

**Hook — "Which team made the mistake?"**
Neither. Both tables are correctly measured and internally clean. They disagree because they sampled different populations: Dataset A sampled teenagers *who already had sleep problems* (that is the entry condition for being at the clinic), so it honestly answers a different question. The full-credit answer is "you cannot tell from the numbers alone — you need to know who was measured."

**Hook follow-up — "Should we average the two, so about 6.8 hours?"**
No. Averaging answers to two different questions produces an answer to no question. 6.85 hours describes neither the clinic population nor the school population. If a student proposes it, take it seriously and use the giraffe-and-mouse line: the average of a giraffe and a mouse is not a useful animal.

**Concept — "Do you believe cricket wins, 73%?"**
Not once you know the thirty people were at cricket practice. The sample was drawn from one part of the population, so the result describes cricket players, not the school. Note carefully: the table itself contains no error. It passes all four of Week 5's checks. That is the point of the example.

**Concept — "If I ask 300 people at cricket practice, does cricket stop winning?"**
No. All 300 are still cricket people. Increasing the size of a badly chosen sample does not move the answer towards the truth; it narrows the *luck* while leaving the *lean* exactly where it was. It makes a wrong answer look more convincing, which is worse than a small wrong answer. Full credit for any answer containing the idea "they are all still cricket players."

**Concept — "Which of the five questions would have caught the sleep-clinic problem?"**
**Question 2, "from whom?"** — the answer "visitors to a sleep-problems clinic" gives the whole game away instantly. Question 4, "how, exactly?", is a defensible second answer, since a proper description of the method would have mentioned recruiting at a clinic. Questions 1, 3 and 5 would not have caught it: an honest, recent, fully consented study can still sample the wrong people.

**Worked Example — "How many numbers did it add up to get that average?"**
As many as were non-blank, not necessarily thirty. `AVERAGE` silently ignores empty cells. With two blanks in thirty rows it divides by 28. `=COUNT(D2:D31)` reveals the true count. This is correct behaviour, and it is also the reason a blank must never be replaced with 0 — a 0 *would* have been counted, dragging the average down for a reason that never happened.

**Worked Example — "What is this average actually evidence of?"**
Full credit requires three things: whose data, which subset, and when. Model answer: *"My thirty meals, recorded over ten days in September, took 16.4 minutes on average."* Not acceptable: *"Meals take 16.4 minutes."* Watch for the middle case — *"I take 16.4 minutes to eat"* — which drops the *when* and quietly claims it is true all year. Ask for the dates back.

**Wrap — "Give me one 'does not show that' sentence about your own table."**
See the marking rules under Workbook Build It, "My three sentences", below. In class, accept a rough version and sharpen it on the spot: every "everyone" must be replaced by a specific group, and every sentence must end with a *because* naming something absent from the table.

**Activity — "Would you be happy for someone to make a decision using this data, after hearing that card?"**
No single correct answer; both answers can be excellent. Strong "no": *"No — it is one person and ten days, and line 7 says not to use it for anyone else."* Strong "yes": *"Yes, for one kind of decision — a decision about my own routine. Nothing bigger."* What you are marking is whether the answer is *scoped*. An unscoped "yes, it's my data, it's fine" is a level 2.

### Activity — the provenance interrogation

Answers depend on your chosen page, so what follows are the marking rules and a fully worked example.

**Marking rules.** All five questions asked, in order, out loud. Every answer written down, including unknowns. No guess dressed up as an answer — "probably a university" is **unknown**. Three or four unknowns out of five is the expected result for a typical news page and should be praised, not fixed.

**Worked example — a news article reading "42% of teenagers say they lose sleep because of their phones."**

| # | Question | Answer found | Verdict |
|---|---|---|---|
| 1 | Who collected it? | "A survey by a children's charity" — named, but no link to the report | **Half.** A name with no document cannot be checked |
| 2 | From whom? | "Teenagers" — no age range, no country, no numbers | **Unknown**, and this is the dangerous one. 42% of *whom*? |
| 3 | When? | The article is dated this month; the survey's date is not given | **Unknown.** An article's date is not its data's date |
| 4 | How, exactly? | "Survey" only. Online? At school? Self-reported? | **Unknown.** "Do you lose sleep because of your phone?" and "what time did you fall asleep?" produce very different 42%s |
| 5 | With whose permission? | Not mentioned | **Unknown** |

**The conclusion to write on the board:** four unknowns out of five. The number is not proven false — it may well be right. It is **unchecked**, and now we can say precisely which four things we would need in order to check it. That sentence is the deliverable.

**The one-line verdict.** The student closes with *"This number is unchecked because I cannot answer questions ___ and ___."* A verdict of "this number is a lie" is **not** full credit: it claims more than the interrogation showed. Being unable to check a number is not the same as knowing it is false, and that distinction is worth a mark of its own. (The interrogation is done in class; it is not a workbook section.)

### Activity — the data card

Marking criteria rather than a single answer:

- [ ] Line 1 says what **one row** is
- [ ] Line 2 has rows × columns **and** real dates
- [ ] Line 3 says *how* it was collected, not just "me"
- [ ] Line 4 names every person who appears — for a solo dataset, "one person: me, age 11"
- [ ] Line 5 covers permission — for a solo dataset, "my own data, a parent checked it, no names or address"
- [ ] Line 6 matches the Week 5 fault log: blanks, deletions, kept outliers
- [ ] Line 7 names **at least two** claims the data cannot support, and is not "anything"

**A full-credit card for the meals dataset:**

> **DATA CARD — My Meals & Sleepiness, September 2026**
> **What it is:** 30 meals I ate, with what I ate, how long I took, and how sleepy I felt one hour later. One row = one meal.
> **How much:** 30 rows × 5 columns, 3 to 12 September 2026.
> **Who collected it:** Me, by hand, in a notebook, writing the time at the first bite and the last bite, and the sleepiness exactly one hour later with a phone timer.
> **Who it is about:** One person: me, age 11. Nobody else appears.
> **Permission:** My own data. A parent read it before I shared it. No names, no address, no photos.
> **Known gaps:** 2 meals blank (forgot to record). 1 sleepiness value of 9 deleted as impossible on a 1–5 scale. 1 meal of 47 minutes kept — it was a birthday lunch, not an error. No weekend meals at all.
> **Do NOT use for:** Guessing anyone else's eating or sleepiness. Any claim about children in general. Deciding what anybody should eat.

### Workbook Week 6 — Warm-Up (W1–W5)

Recap of Week 5. Mark quickly; if more than two are wrong, spend two minutes on Week 5's type test before moving on.

- **W1.** The one-question test: *"If I **add** two of these values together, does the answer **mean anything**?"* Yes means number; no means category, however many digits it has.
- **W2. CATEGORY.** ID 1001 + ID 1002 = 2003, which is a different person or nobody. The digits are a **name**, not an amount. *(Watch for: NUMBER, "because it has digits". Send them back to the W1 test.)*
- **W3. Do:** leave it visibly blank and write a note saying why. **Never:** put a 0 in it. A blank says *I don't know*; a 0 says *I know, and it was zero.* *(This is the same idea that matters again in B5(d).)*
- **W4.** `sleep_h` = 88 is **IMPOSSIBLE** (outside 0–16): blank it and note `was 88, impossible, original lost`; do **not** guess 8 or 8.8. `screen_min` = 480 is an **OUTLIER** (inside 0–1440, so legal): **keep it** and note why that day was different. The common swap is treating the 480 as an error and deleting it.
- **W5.** A closed, short list, for example `ALLOWED VALUES for day: Mon · Wed · Fri`, with nothing else allowed. It has to be a **list**, **short** and **closed**. "Be consistent" fails: it is not a list and cannot be checked.

### Workbook Week 6 — Practice Set A, Understand It (A1–A6)

- **A1.** **population**, **sample**, **provenance**, **data card**, **seven**, **unknown**. Accept "dataset" or "table" for *population* only with a prompt: "everything you would like your answer to be true about".
- **A2. (b) Question 2, "From whom?"** The answer "visitors to a sleep-problems clinic" gives the whole game away. **Second best: (d) question 4, "How, exactly?"**, because a proper description of the method would have had to mention recruiting at a clinic. Questions 1, 3 and 5 would **not** have caught it: an honest, recent, fully consented study can still measure the wrong people. *(This is the same item as the "Which of the five questions would have caught the sleep-clinic problem?" lesson question above.)*
- **A3. FALSE.** All 300 are still cricket people. A bigger badly chosen sample narrows the **luck** and leaves the **lean** exactly where it was. In soup words: **an unstirred ladle is not better than an unstirred teaspoon; stirring matters more than spoon size.**
- **A4.** 1 → **C** · 2 → **D** · 3 → **A** · 4 → **E** · 5 → **B**.
- **A5.** 1. **population** · 2. **sample** · 3. **bias** (also accept "the gap between what I measured and what I am talking about") · 4. **the things I never measured**, the rest of the population. **Fraction: 8 / 46.** The denominator is the **whole** population, the 8 filled dots **plus** the 38 hollow ones. **8/38 is the common slip** (measured versus unmeasured, not measured versus everything). 8 out of 46 is about 17%, so 83% was never looked at.
- **A6.** Numbering, top to bottom of the jumbled list: Who it is about **4** · Do NOT use for **7** · What it is **1** · Permission **5** · Known gaps **6** · How much **2** · Who collected it **3**. **The two that matter: lines 6 and 7.** Anybody can count rows and write a date; saying what is missing and what you may not claim is the skill, and it is the part a careless person would leave off.

### Workbook Week 6 — Practice Set B, Use It (B1–B5)

**B1.**

| Dataset | The question it honestly answers |
|---|---|
| **A** (sleep clinic) | *"How much sleep do teenagers **who already have a sleep problem** get?"* The entry ticket to the clinic is having one |
| **B** (4 random schools) | *"How much sleep do teenagers in these four schools get?"* Much closer to the question asked, though still not "all teenagers everywhere" |

**Averaging them to about 6.85: NO.** It answers two different questions and so answers none. Use the giraffe-and-mouse line (see the lesson question "Should we average the two" above).

**B2. Face unlock.** It will work **noticeably worse on children's faces** (failing, or taking several tries) and fine for adults, while nothing in the table looks broken: Week 5's four checks all pass. **Clean is not the same as trustworthy.** The word is **sample** (accept **bias**): the sample does not match the population it is used on. **20,000 more adult faces: NO.** More unstirred ladle; it adds not a single child. The fix is more of the *missing kind* of data, not more data.

**B3. The volunteer survey.** Population: **all 30 students in the class.** Sample: **the 11 who chose to walk up to the desk.** The failure is **self-selection**. The people who volunteer tend to feel strongly, often the ones who dislike maths and want to say so; the 19 who thought it was "fine" did not bother, and "fine" is the answer that never gets recorded. So 2.1 out of 5 is the opinion of the people who cared enough to walk over. Honest sentence to add, for example: *"This is 11 students out of 30 who chose to answer. It under-represents students who feel neutral about maths, because neutral people do not usually volunteer."*

**B4. Repairing the sentences.** Marking rule: every good sentence names **a specific claim** and ends with a **because** pointing at something **absent from the table**.

| The bad sentence | Why it fails | A repaired version |
|---|---|---|
| "This might be wrong." | **Anything** might be wrong. It names nothing, costs nothing, and tells a reader zero | *"This does not show that my sleepiness comes from the food, because I never recorded how much homework I had that night."* |
| "This does not prove anything." | An **over-correction**. It does prove something small and true: that these 30 meals took this long | *"This does prove that my own 30 meals in September took about 16 minutes. It does not show that anyone else's do, because my sample is one person."* |
| "This does not show that everyone eats like me." | Right **idea**, but "everyone" does no work and no reason is attached | *"This does not show that other children in my class eat for 16 minutes, because I measured one person, me, and one person tells you nothing about anyone else, however many meals I record."* |

Further repairs you may need at the desk:

| Not accepted | Why | The repair |
|---|---|---|
| "This does not show that I am healthy." | True but unconnected: health was never measured or claimed | "Pick a claim somebody might actually make from your numbers" |
| "This does not prove anything." (unrepaired) | Over-correction | "What is the smallest true thing it does prove? Start there, then say where it stops" |

**B5. The average that quietly divided by 28.**

| Part | Answer |
|---|---|
| (a) | 492 ÷ **30** = **16.4** minutes |
| (b) | 461 ÷ **28** = 16.4642... = **16.46** minutes. `AVERAGE` did this **silently** and never mentioned the 28 |
| (c) | **`=COUNT(D2:D31)`**. If it says 28, the machine has told you something it would never have volunteered |
| (d) | 461 ÷ **30** = 15.3666... = **15.37** minutes: a drop of more than a minute for a reason that never happened. **A blank gets honestly skipped; a fake zero gets honestly believed** |
| (e) | `16.46 minutes — average of 28 values, 2 rows blank` |

"16.5, average of 30" records something that did not happen. Accept 16.5 in (b) only if the student shows 16.46 first, but the (e) line must say 28 and 2 blank.

### Workbook Week 6 — Puzzle of the Week, Four Surveys, One School

1. **Order, most trustworthy first: D → B → C → A.** D measured **all 800**, so there is no sampling error. B is only 30 but **stirred** (a lottery pick of 5 from each of 6 year groups), and its 34% is within 4 points of the true 38%. C is 120 but **self-selected**, off by 24 points. A is 400 but every one stood **in the pizza queue**, off by 43 points.
2. **Survey A.** 400 people, but all from the one place in the school where pizza-lovers had collected. Being in the queue was the entry ticket, exactly like walking into the sleep clinic. More rows from the wrong place is a wrong answer that looks scientific.
3. Because **B was stirred and A and C were not.** A well-stirred teaspoon beats an unstirred ladle. B used about 13 times less data than A and landed 39 points closer to the truth.
4. **Survey D:** population = **all 800 students**; sample = **all 800 students**. The unusual thing is that **they are the same set**. When the sample is the whole population the result is a fact, not an estimate. (It is a fact only about *that* question: ask about students in the whole town and the same 800 rows become a sample again.)
5. **A: wrong place** · **B: nothing wrong** (accept "too small" as a fair worry, but B landed closest of the three samples) · **C: self-selection** · **D: nothing wrong**.

### Workbook Week 6 — Think Deeper (T1–T2)

**T1. Invent a question for which Dataset A is the better dataset.** Full credit needs a question where the clinic's entry condition is a **feature, not a flaw**. Model answers: *"How well are the treatments at this clinic working? Dataset A is the only one that can answer that, because everyone in it is a patient there."* Or *"How little sleep do teenagers with sleep problems actually get? That is exactly what Dataset A measures, and Dataset B would mostly measure people who sleep fine."* The big idea: the dataset was never bad, it was **matched to the wrong question**. A student who reaches this is at level 5.

**T2. Designing a stirred sample.** Marked on (a) some mechanism for **stirring** and (b) finding their **own** flaw. A strong plan: *"I'd go to six registration classes, one per year group, on the same morning. In each, the teacher reads out five names from a list I shuffled beforehand, and only those five answer. That is 30 people across every year, and I never choose who."* Full-credit flaws include: one class per year is not a fair slice (classes are often grouped by ability or language); anyone absent is invisible; the student standing at the front may be told what they want to hear; one morning is one day (if it is chips day, chips wins). The most common weak answer is *"nothing is wrong with my plan."* Something always is; push until they find it.

### Workbook Week 6 — Build It, Finish Your Life In 30 Rows

Eight checklist steps, then four fill-in parts: **My two averages**, **My data card**, **My three sentences**, **The adult check**. No single answer; mark against the points below.

**My two averages.** Numbers depend on the student's own data. The worked example used throughout this file: `minutes` sums to **492**, and 492 ÷ 30 = **16.4 minutes**; `sleepy_1to5` sums to **87**, and 87 ÷ 30 = **2.9**. If two cells are blank the arithmetic changes and the paper must say so: for example, 28 remaining `minutes` values summing to 461 give 461 ÷ 28 = **16.46**, written as "average of 28 rows, 2 blank". Check the table's *Average*, *How many values it came from* and *Rows blank* columns agree with each other and with the student's `=COUNT` result (step 4).

**The full sentence, with *whose* and *when*.** Model: *"My own thirty meals, recorded over ten days in September, took 16.4 minutes on average."* Not acceptable: *"Meals take 16.4 minutes."* Watch for the middle case, *"I take 16.4 minutes to eat"*, which drops the *when* and quietly claims it is true all year; ask for the dates back. Model IS / IS NOT pair if a student asks for the contrast:

| | |
|---|---|
| **IS** evidence that | "My own meals, over these ten days in September, took about 16 minutes on average." |
| **is NOT** evidence that | "Meals in general take 16 minutes. My sample is one person, ten days, one routine, no weekends." |

**My data card.** Marked with the seven criteria in "Activity — the data card" above, against the seven numbered rows of the *My data card* table. Two notes. **A card with honest unknowns scores full marks:** "Who collected it: unknown, my little brother wrote three of the rows and cannot remember how he measured them" is an excellent line 3, specific and honest, and it tells a reader which rows to distrust. **A card that contradicts the table loses marks:** if line 2 says 30 rows and the table has 22, that is the fault the card exists to prevent. Check this first; it takes five seconds and is the most common failure.

**My three sentences.** Every sentence must (a) start "This does not show that…", (b) name a specific claim, and (c) give a *because* that names something **absent from the table**. Three full-credit answers for the meals dataset:

> **1.** "This does not show that other children eat for 16 minutes. My sample is one person, me, and one person tells you nothing about anyone else, however many meals I record."

> **2.** "This does not show that big meals make me sleepy. Every big meal in my table was also a rice meal, so I cannot tell whether it is the size or the rice. I would need a big meal that was not rice, and I do not have one."

> **3.** "This does not show anything about weekends. I only recorded school days, so Saturday and Sunday are not in the table at all, and those are the days I eat most differently."

Sentences that do not earn credit are in the B4 repair tables above; use the same repairs here.

**The adult check.** Full credit is the adult's actual words written down, whatever they were. "My dad said he didn't understand the second one" is a genuine result and should be praised loudly: the student tested their sentence instead of assuming it worked. A suspiciously perfect "my mum said it was very good" with no detail earns a gentle question: "What exactly did she say?"

### Workbook Week 6 — Draw It

Marked on four things, not artistic skill: the population drawn **much bigger** than the sample and labelled with a real number or description; the sample patch **shaded** and labelled with the actual rows and dates; the **missing** part labelled, ideally with a count; and one "This does not show that…" sentence naming something **specific and absent**. **The single most common mistake** is drawing the sample as a neat patch in the **middle**, evenly spread, which quietly claims the spoonful was stirred. For a one-person, ten-school-day table it was not, so **draw it in a corner**; where the patch goes is an honest claim about how it was sampled. The workbook's own example (about 1,100 meals a year; a corner patch of 30 meals, 3–12 September; "about 1,070 meals never measured") is a full-credit answer.

### Workbook Week 6 — Self-Check

Five "I can…" rows with 😀 / 🙂 / 😕 boxes, and a free "one thing I still want to ask about" line. Nothing to mark. Read the 😕 ticks and the question; they tell you where to start Week 7's recap. A student who ticks 😀 on all five but wrote an unscoped "everyone" sentence in Build It is over-rating themselves; show them the sentence.

### The three claims for the "won't engage" fallback

If you used the game where you make outrageous claims and the student shoots them down, here are three to use, with the rebuttal you are fishing for:

| Your claim | The rebuttal you want |
|---|---|
| "So all children eat rice for lunch." | "You measured one child. Me." |
| "So eating slowly makes you sleepy." | "The table shows them happening together. It cannot show which one caused the other — and my big meals were all rice anyway." |
| "So this proves people should eat faster." | "It does not show that eating faster helps anything at all. I never tried eating faster on purpose, so there is nothing in the table about it." |

Write their rebuttals down verbatim. They are line 7 of the card and the "My three sentences" part of Build It, already written in the student's own voice.

---

## 🔮 Next Week Preview

Next week the table finally pays off. Having built it, cleaned it and written its card, the student goes looking for **patterns** — the things in their own data that repeat often enough to bet on. Week 7 asks what a pattern actually is, how many repeats it takes before you would risk something on it, and why "it happened twice" is a story while "it happened twenty-six times out of thirty" is a rule. Their thirty rows are the raw material for the whole lesson, which is why chasing the row count this week matters more than it looks.

**Prep early:** nothing to buy and nothing to install — Week 7 is paper and pens again. Two things to do, though. First, **read the student's finished table before Week 7 and find one repeat in it yourself.** Anything: rice at lunch four times, sleepiness always higher after dinner, no meals recorded on Sundays. Having one in your pocket means the lesson starts with their data instead of an invented example, and that is worth ten minutes of your evening. Second, **keep the data card where you can both see it**, because Week 7's most important moment is the one where a genuinely exciting pattern collides with line 7 of their own card.

---

[⬅ Week 5](week-05.md) · [Course Home](../README.md) · [Week 7 ➡](week-07.md) · [Student Guide](../student-guide/week-06.md) · [Workbook](../workbook/week-06.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
