# Week 5 — Numbers, Names, and Broken Boxes

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Week 6 ➡](week-06.md) · [Student Guide](../student-guide/week-05.md) · [Workbook](../workbook/week-05.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (works in 60, stretches to 75) |
| **Type** | Teach |
| **Big idea** | Every column has a type, and the four kinds of mess — missing, duplicate, impossible and inconsistent — are all findable if you actually look. |
| **New vocabulary** | data type · missing value · duplicate · impossible value · controlled vocabulary |
| **Materials** | **Four coloured pens or highlighters, four different colours** · the printed Crime Scene Table (Workbook Week 5, page 2) · the student's own homework table from Week 4 · a board or big sheet of paper · a calculator or a phone calculator |
| **Tech needed** | **None.** Paper and pens only. A calculator is convenient but mental arithmetic works. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

---

## 🎯 Lesson Objectives

By the end of this lesson the student can:

1. **Decide a column's data type** by asking whether averaging its values would mean anything — and correctly catch at least one column that is made of digits but is not a number.
2. **Find and name all four kinds of mess** in a wrecked table: missing value, duplicate, impossible value, inconsistent category.
3. **Explain the difference between an impossible value and an outlier**, and say exactly what you do with each — blank the first, keep and annotate the second.
4. **Write a controlled vocabulary** that would have prevented an inconsistency they personally found.

Objective 3 is the hard one and the one worth the most. A student who deletes the outlier has failed the lesson even if they found all nine faults.

---

## 🧑‍🏫 What YOU Need to Know First

**Read this once, slowly. About 12 minutes. It is complete — you need nothing else.**

### The one-sentence version

Real data is always broken in a small number of very specific ways, and each way has a different correct repair — so the skill is not "tidying up", it is *diagnosis*.

### Part 1 — Columns have types, and the test is arithmetic

Last week every column was just a column. This week we notice that they behave differently.

> **Data type** — what kind of value lives in a column, which decides what you are allowed to do with it.

Four types matter today:

| Type | Looks like | Average it? | Sort it? | Example |
|---|---|---|---|---|
| **Number** | `7.5`, `340`, `-2` | ✅ yes | ✅ yes | `sleep_hours` |
| **Category** | `beagle`, `main`, `6A` | ❌ no | ⚠️ only if there is a natural order | `pocket` |
| **Text** | `"was ill, stayed home"` | ❌ no | ⚠️ alphabetically, which rarely helps | `note` |
| **Time** | `2026-08-24`, `21:30` | ⚠️ carefully | ✅ yes | `bedtime` |

**The test is one question: if I add two of these together, does the answer mean anything?**

![How to decide a column's data type](../figures/fig-w05-2-column-type-tree.svg)
*Figure 5.1 — Start at the top. Ask about the meaning of the values, never about how they look.*

Try it:

- 3 hours of sleep + 8 hours of sleep = 11 hours of sleep. Meaningful. **Number.**
- Bus route 7 + bus route 12 = route 19. Meaningless — route 19 is a different bus, or no bus. **Category.**
- Class 6A + class 6B = ? Does not even compute. **Category.**
- Postcode 560001 + postcode 110001 = 670002. Perfectly valid arithmetic, complete nonsense. **Category.**

**This is the single most valuable idea in the section, so let me make it concrete.** Take three friends with postcodes 560001, 110001 and 400001. Average them: 1,070,003 ÷ 3 = **356,667.67**. Postcode 356667 is a real place — a village none of the three has ever visited. The maths is perfect. The answer is garbage. The column was a category wearing number clothes.

Student ID numbers, shirt numbers, phone numbers, house numbers, bus routes, postcodes, room numbers: all categories. Spreadsheets will happily average every one of them and will never warn you.

**Ordered categories** are the honest grey area. A mood rating of 1–5 is a category — but 5 really is happier than 4, so it has an order. You can sort it and find the middle value. Whether you can *average* it is genuinely debated by scientists, because the gap from 1 to 2 might not feel the same size as the gap from 4 to 5. In practice everyone averages it and adds a footnote. Tell the student exactly that: **we do it, it's slightly fake, and knowing it's slightly fake is the professional part.**

### Part 2 — The four kinds of mess

![The four kinds of mess](../figures/fig-w05-1-four-kinds-of-mess.svg)
*Figure 5.2 — Four different problems. Four different fixes. Naming which one you found is half the job.*

**Mess 1 — Missing value.** A box where a measurement should be, and isn't.

> **Missing value** — an empty box where a measurement should be.

What to do: **leave it visibly blank, and write a note saying why.** That's it. At Level 1 that is almost always the right answer.

What *not* to do, and this is the one that matters: **never fill it with 0.** A blank says "I don't know." A zero says "I know, and it was zero." Those are opposite statements, and no machine on Earth can tell them apart afterwards. If a student fills three blank sleep cells with 0, their average sleep drops by hours and nothing on the page records that it happened.

There is a second distinction that trips up adults constantly: **no data is not the same as no event.** A shop that was closed on Sunday genuinely sold 0 items — that's a real measurement of zero. A Sunday you forgot to check is blank. Both look like an absent row. Only a note tells them apart.

**Mess 2 — Duplicate.** The same example recorded more than once.

> **Duplicate** — the same example written down twice.

Why it matters: the duplicated row gets double voting power. Everything computed from the table is now slightly skewed towards that one example, and with a twelve-row table, "slightly" is generous.

**But check before you delete.** Two rows can be identical and be genuinely different examples: two different pencils that both weigh 6 grams and are both 18 cm long are not a duplicate, they are a coincidence. The way professionals tell them apart is to give every row a unique ID at collection time. Then duplicates are visible and coincidences are safe.

**Mess 3 — Impossible value.** A value reality does not allow.

> **Impossible value** — a value outside what reality permits.

88 hours of sleep. A bag weighing −3.2 kg. An age of 45 for a dog. A mood of 9 on a 1-to-5 scale.

How you catch them: **write down the legal range for every number column before you collect anything.** `sleep_hours: 0 to 16`. `bag_kg: 0.1 to 12`. `screen_min: 0 to 1440` (there are 1440 minutes in a day). Then anything outside the range is flagged automatically.

What to do with one: **blank it, and write the note `was 88, impossible, original lost`.** Do *not* guess. You genuinely do not know whether 88 was a mis-typed 8.8 or a mis-typed 8 or something else entirely. Guessing replaces a known gap with an invented fact, which is strictly worse. You have lost one measurement. You have not lost your credibility.

**Mess 4 — Inconsistent category.** The same thing written several different ways.

> **Controlled vocabulary** — the written-down list of allowed values for a category column.

`Monday`, `monday`, `MON`, `Mon.` — to you, obviously one day. To a machine, four unrelated categories, as different from each other as `dog` and `Tuesday`. This is, genuinely, the most common data error in the world.

The fix is not to be more careful. Being more careful does not work; people are not careful over three weeks at 9pm. The fix is a **controlled vocabulary**: decide the allowed values in advance, write them at the top of the sheet, and never type anything else. In a spreadsheet you can enforce it with a dropdown (Week 6). On paper you enforce it by having the list where you can see it.

### Part 3 — The trap: outliers are not faults

This is the most important paragraph in the file.

> **Outlier** — a value that is legal but sits far away from all the others.

480 screen-minutes in a week where everything else is 95–150. That is 8 hours. It is not impossible; there are 1440 minutes in a day. It is not a typo, necessarily. It might be completely real: a sick day at home.

![Impossible value versus outlier](../figures/fig-w05-5-outlier-vs-impossible.svg)
*Figure 5.3 — Impossible sits outside the legal range. An outlier sits inside it, just far from the crowd. Completely different diagnoses.*

**Never delete an outlier because it is inconvenient.** It is very often the most informative row in the entire table. In the Crime Scene Table, the 480-minute row is also the row with the lowest sleep — that pair of facts is the only interesting thing in the whole dataset, and a student who deletes it has thrown away the finding.

The professional move: **investigate and annotate.** Add a note: `home sick, watched films all day`. Keep the value.

And here is the honest hard part you should be ready to say out loud: **sometimes you genuinely cannot tell an outlier from an error.** If the note-writing didn't happen at the time, 480 might be a real sick day or might be a mis-typed 48. There is no procedure that recovers the truth. That is why writing notes *at the moment of collection* matters so much — it is the only defence against a question you cannot answer later.

### The two misconceptions you will meet today

**Misconception 1: "Anything weird is an error."** Students find 480 and cross it out with enormous confidence, usually within ten seconds of finding it. This is the single most common failure in the lesson and you should expect it, welcome it, and then spend five minutes on it. The question that unpicks it: *"What number would have made you suspicious? Now — is 480 outside what's physically possible, or just outside what's usual?"*

**Misconception 2: "The computer will work out that Monday and monday are the same."** It will not. Not by being clever, not by being modern. A spreadsheet counting distinct values will report 4 where you see 1. Demonstrate it if you can, but even just saying it plainly with total confidence usually lands.

A third, smaller one: **"a blank is a zero."** Attack this every single time you see it. It is the error with the biggest consequences per second of effort.

### How deep to go — and where to stop

**Go this deep:** the averaging test; the four kinds of mess with their names; the outlier distinction; controlled vocabulary; and the fact that one bad cell can destroy an average.

**Stop before:**

| Do not raise today | Because |
|---|---|
| Where the data came from, who collected it, permission | That is Week 6, entirely |
| Sample vs population | Week 6 |
| Spreadsheets, `=AVERAGE`, dropdowns | Week 6 is the first time we open Sheets |
| Median, standard deviation, "robust statistics" | Beyond Level 1. You may *mention* the median if a strong student notices it barely moves — see the extension questions — but do not teach it |
| Filling gaps with the column average ("imputation") | Real technique, wrong level. Mention that big datasets sometimes do it, and say we never will |
| Bias in data | Week 31 |

If a student asks "but where did this table come from and can we trust the person who made it?" — that is a wonderful question and it is *next week's entire lesson*. Write it on the parking lot and move on.

### If you have five spare minutes before class

Take your own phone's screen-time numbers for the last seven days and compute the average. Then look for the day that is furthest from the rest, and ask yourself honestly whether you can now, days later, remember *why* it was high. You almost certainly cannot. That is the outlier problem in your own hands, and it makes you very convincing at minute 55.

---

### 🧭 The Growing Map — Week 5's frame

Nothing moves on the map this week, and that is the teaching point. Same band, same nine tiles, same
badge on THE TABLE — week two of a three-week tile.

![The course map after Week 5: still the table tile, now checked for mess](../figures/fig-w05-0-where-this-fits.svg)

*Figure 5.0 — Week 5's version. Geometrically identical to Week 4. The only differences are the
thread strip — **data** alone this week — and the line at the bottom.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Put it up next to last week's and ask** *"what's different?"* Let them hunt. The honest answer
   is *"almost nothing"*, and a learner who gets there has understood that the map tracks the
   *course*, not the *lesson*.
2. **Then ask** *"which bit did we do today, then?"* They will point at THE TABLE again — the crime
   scene table, the nine faults, the fifteen-hour sleeper. Follow with *"and what does dashed still
   mean?"* Same answer as always: not yet.
3. **No redraw this week.** Have them look at the copy they already have and say one sentence out
   loud: *"same tile, second of three, and this time it was the four kinds of mess."* Saying it is
   the whole exercise.

> **🧑‍🏫 Why this is worth two minutes.** "We didn't move" is reassuring in a way that is easy to
> underestimate. A learner who cannot see the map reads a second week on the same material as *"I must
> be behind"*. One glance at an unchanged picture kills that idea for free.

**The six threads** along the bottom: **data · representation · model · learning signal · evaluation
· impact.** Only **data** is lit — one thread, because the whole lesson was about the stuff going in.
If they cannot remember which thread it was, that costs nothing.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print Workbook Week 5, pages 1–4.** Page 2 is the Crime Scene Table — the student's copy has **no shading and no numbered pins**. Check that before you hand it over; handing them the teacher copy ends the lesson instantly.
- [ ] **Find four coloured pens or highlighters in four clearly different colours.** This is the one unusual material. If you only have two, see the fallback table.
- [ ] **Write the colour legend** on a scrap of paper or the board:

  | Colour | Fault type |
  |---|---|
  | Colour 1 (e.g. blue) | MISSING — an empty box |
  | Colour 2 (e.g. red) | IMPOSSIBLE — reality says no |
  | Colour 3 (e.g. green) | DUPLICATE — same example twice |
  | Colour 4 (e.g. orange) | INCONSISTENT — same thing, different spellings |

- [ ] **Do the activity yourself, on the teacher copy, with the pens.** Ten minutes. You will find out which faults are hard to spot (the duplicate is hardest; the blanks are easiest) and you will be ready for the 480 argument.
- [ ] **Chase the Week 4 homework.** The student needs their own table in class today for the homework brief, and they need at least 14 rows in it by Week 6. If nothing has been collected, decide now whether you're going to spend five minutes of the wrap restarting it.
- [ ] **Read the Answer Key.** It contains all nine faults, the outlier argument, and every arithmetic result. Ten minutes.

### 5 minutes on the day

- [ ] Board: write `average sleep = 15.0 hours per night` and nothing else. Cover it or turn the board round.
- [ ] Four pens laid out in a row, legend beside them.
- [ ] Crime Scene Table (student copy) face down.
- [ ] Calculator to hand.
- [ ] Student's Week 4 homework table on the desk.

### If something fails

| If this fails | Do this instead |
|---|---|
| **Only two coloured pens** | Two colours plus two *shapes*: circle it in colour 1 for missing, box it in colour 1 for duplicate, circle in colour 2 for impossible, box in colour 2 for inconsistent. Write the key at the top. Shape-plus-colour is exactly what a colour-blind reader needs anyway, so this is arguably the better version. |
| **One pen only** | Circle every fault in that pen and write the fault's initial letter beside it: M, D, I, C. Works perfectly. |
| **No printer** | Read the twelve rows aloud, slowly, twice, while the student copies them onto ruled paper. Costs 6 minutes — take them from the Worked Example. There is a real bonus: copying by hand introduces *their own* transcription errors, which is a beautiful, if slightly cruel, extra lesson. |
| **No calculator** | The arithmetic is deliberately small. Every sum in the answer key is doable on paper in under a minute, and doing it by hand makes the "one bad cell" moment hit harder. |
| **The Week 4 homework never happened** | Do the lesson exactly as written. For the homework, have them start the table this week and give them the Week 6 target of 21 rows instead of 30. Say the reduced number out loud so it feels like a plan, not a failure. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | 🪝 **Hook** — "This person sleeps fifteen hours a night" | An impossible average, from a table they haven't seen yet. |
| 8–26 | 🧠 **Concept** — Types, and the four kinds of mess | The averaging test, then the four faults, then the trap. |
| 26–40 | 🔍 **Worked Example Together** — Six dogs, six faults | Clean a small table together and watch the average move. |
| 40–60 | 🎲 **Activity** — Crime Scene Table | Twelve rows, nine faults, four pens, one trap. |
| 60–70 | 🔑 **Wrap & Assign** | Controlled vocabulary, takeaways, homework. |

**Running 60 minutes?** Cut the Worked Example to 8 minutes (do the dog table's duplicate and impossible value only) and the Wrap to 6. Do not cut the activity — the outlier argument lives there.
**Running 75?** Add the extension questions from Differentiation, or have the student plant faults in a fresh table for *you* to find.

---

### 🪝 Hook — "This person sleeps fifteen hours a night" (0–8)

**Do this:** reveal the board. It says, and only says:

```
average sleep = 15.0 hours per night
```

**Say this:**

> "I've been given a table. Somebody tracked their sleep, their school bag weight and their screen time for twelve school days. I've done the arithmetic, and here's what it says. This person sleeps fifteen hours a night. Every night.
>
> Don't tell me yet whether you believe it. Tell me something else first: **is fifteen hours even possible?**"

Let them answer. It is possible — a very ill person, or a teenager after an exhausting week, could sleep fifteen hours once. As an *average across twelve days*, it means going to bed at 8pm and getting up at 11am every single day, which for a school student is not credible.

**Say this:**

> "Right. Not impossible for one night. Completely unbelievable as an average. So one of two things is true: either this person has a very unusual life, or **there is something wrong with the table**.
>
> Here's the part I find genuinely alarming. The arithmetic is correct. I didn't make a mistake. I added up the sleep column and divided by how many numbers there were, and the answer really is 15.0. The table produced a lie, using perfect maths, and it didn't warn me.
>
> By the end of today you'll be able to find out why in about ninety seconds, and you'll know the name of the problem."

**Do this:** write these two numbers under the first one:

```
average sleep      = 15.0 hours per night
average bag weight = 3.42 kg
```

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "3.42 kg for a school bag — believable?" | "Yes, that sounds normal." | If they say no, ask what a normal bag weighs. Most guess 3–5 kg, which is right. The point stands: *this one looks fine.* |
| "So the bag number is safe?" | Ideally hesitation, or "…is it?" | Most students will say yes. Let them. Then: "Hold that thought. That number is wrong too, and it's wrong in a way you can't see at all. That's the scary one." |
| "What could make an average come out too high?" | "One really big number" / "someone typed it wrong" | If they're stuck: "How many numbers do you think it takes to wreck an average of twelve?" Steer to **one**. |

**Say this:**

> "One number. One box on one row, and the whole answer moves by seven hours. That's what we're hunting today. There are nine faults planted in that table, and one thing that looks exactly like a fault and absolutely is not — and telling those apart is the actual skill."

---

### 🧠 Concept — Types, and the four kinds of mess (8–26)

#### Part A — the averaging test (6 minutes)

**Say this:**

> "Before we hunt faults, one quick idea, because it stops a whole category of mistake.
>
> Last week every column was just a column. That was a useful lie. Actually columns come in different **types**, and the type decides what you're allowed to do with the column.
>
> Here's the test, and it's just one question. **If I add two of these values together, does the answer mean anything?**"

**Do this:** work through these on the board, out loud, one at a time. Make them answer before you do.

| Column | The addition | Verdict |
|---|---|---|
| `sleep_hours` | 3 hours + 8 hours = 11 hours | Means something. **Number.** |
| `bus_route` | route 7 + route 12 = route 19 | Route 19 is a different bus, or no bus. **Category.** |
| `weight_g` | 200 g + 340 g = 540 g | Means something. **Number.** |
| `student_id` | ID 1001 + ID 1002 = student 2003 | A different person, or nobody. **Category.** |
| `postcode` | 560001 + 110001 = 670002 | Perfect maths, total nonsense. **Category.** |

**Say this:**

> "Look at the pattern. Half of those were made entirely of digits, and half of *those* were not numbers. Bus route seven is not a quantity of anything. It's a **name** that happens to be written with a digit.
>
> Here's why I'm bothering you with this. A spreadsheet will happily average your student ID column. It will not warn you. It will give you a confident, precise, completely meaningless answer, and it will look exactly as trustworthy as the average sleep number sitting next to it."

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "Is `shirt_number` a number or a category?" | "Category." | If they say number: "What's the average shirt number of your team? Is there a player who *is* that?" |
| "Is `mood_1to5` a number or a category?" | Hesitation, then "…sort of both?" | **This is the right answer and worth praising hard.** Explain: it's an ordered category. 5 really is happier than 4, so you can sort it. Averaging it is standard practice and slightly fake, because the gap 1→2 might not feel the same as 4→5. We do it and we footnote it. |

#### Part B — the four kinds of mess (8 minutes)

**Do this:** draw four boxes on the board, or hold up Figure 5.2. Name them one at a time, and give the fix immediately after the name — never let a fault float without its repair.

![The four kinds of mess](../figures/fig-w05-1-four-kinds-of-mess.svg)
*Figure 5.4 — The four faults, and how differently they look.*

**Say this:**

> "**Number one: missing.** A box that should have a measurement in it, and doesn't. You forgot. You were asleep. The scale was flat.
>
> The fix is easy and everyone gets it wrong. The fix is: **leave it blank, and write a note saying why.** That's it.
>
> What you must never do — and I want you to remember this one specifically — is put a zero in it. A blank says 'I don't know.' A zero says 'I know, and it was zero.' Those are opposite sentences. Put a zero in your sleep column and you've claimed you didn't sleep at all that night, and nothing on the page will ever tell anyone that you made it up.
>
> **Number two: duplicate.** The same example written down twice. Same night, same day, entered twice.
>
> Why it matters: that night now votes twice. Everything you work out from the table leans towards it.
>
> But careful — check before you delete. Two rows can be identical and both be real. Two different pencils that both weigh 6 grams and are both 18 cm long aren't a duplicate, they're a coincidence. The way grown-ups avoid this is to give every row its own ID number when they collect it.
>
> **Number three: impossible.** A value reality doesn't allow. Eighty-eight hours of sleep. A bag that weighs minus three kilograms. A dog that's forty-five years old.
>
> How you catch them: before you collect anything, write down the legal range for every number column. Sleep, nought to sixteen. Bag, nought point one to twelve. Screen minutes, nought to one thousand four hundred and forty, because that's how many minutes are in a day. Then anything outside the range puts its hand up.
>
> What you do: blank it, and write the note 'was 88, impossible, original lost'. **Don't guess.** You genuinely don't know if 88 was meant to be 8.8 or 8. If you guess, you've replaced a hole you knew about with a made-up fact you'll forget was made up.
>
> **Number four: inconsistent.** The same thing written four different ways. Monday, monday, MON, Mon-full-stop.
>
> You see one day. A computer sees four completely different categories — as different from each other as 'dog' and 'Thursday'. This is the most common data error in the world, and I mean that literally.
>
> The fix isn't 'be more careful'. Being careful doesn't work at nine o'clock at night in week three. The fix is a **controlled vocabulary** — you write down the allowed answers before you start and you never type anything else."

#### Part C — the trap (4 minutes)

**Say this:**

> "Now the one that separates people who tidy tables from people who understand them.
>
> Suppose your screen-time column reads: ninety-five, a hundred and twenty, a hundred and ten, a hundred and five, a hundred and fifty… and then **four hundred and eighty**.
>
> Is that a fault?"

Let them answer. Most say yes, immediately and confidently. Do not correct yet.

**Say this:**

> "Four hundred and eighty minutes is eight hours. Is eight hours of screen time *impossible*? There are twenty-four hours in a day. So — no. It's completely possible. Unusual, but possible.
>
> That's not a fault. That's an **outlier**: a value that's legal, but sits a long way from all the others."

![Impossible value versus outlier](../figures/fig-w05-5-outlier-vs-impossible.svg)
*Figure 5.5 — Impossible sits outside the legal range. An outlier sits inside it, just far from the crowd.*

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "What could make a real day come out at 480?" | "Sick day" / "holiday" / "the internet was down at school so I was home" | If they can't think of one, offer: "What if you'd been ill in bed?" Once they can name one real cause, the deletion instinct dies. |
| "So what do we do with it?" | "Keep it and write a note." | If they say delete: "If you delete it, and it was real, what have you thrown away?" Steer to: *the most interesting day in the whole table.* |
| "Here's the hard one. Can you always tell an outlier from a mistake?" | "No." | **Sit with this.** The honest answer is no. If nobody wrote a note at the time, 480 might be a real sick day or a mis-typed 48, and no amount of cleverness recovers the truth. That is why notes get written *at the moment*, not later. |

---

### 🔍 Worked Example Together — Six dogs, six faults (26–40)

**Do this:** write this table on the board or a sheet of paper between you. Say it is from an animal shelter.

| id | name | age_years | weight_kg | breed |
|---|---|---|---|---|
| 1 | Bruno | 3 | 22 | labrador |
| 2 | Coco | 2 | 8 | Beagle |
| 3 | Bruno | 3 | 22 | labrador |
| 4 | Rex | 45 | 30 | german shepherd |
| 5 | Milo | 1 | | beagle |
| 6 | Zara | 4 | -5 | Labrador |

**Say this:**

> "Six dogs. Six faults. You've got three minutes and you may not write anything yet — just find them and tell me. Go."

Let them hunt in silence. Then take answers one at a time and, for each, ask two follow-up questions: **which of the four kinds is it?** and **what's the fix?**

The full diagnosis, in the order most students find them:

| Found | Kind | Fix |
|---|---|---|
| Row 5's `weight_kg` is empty | **Missing** | Leave blank. Note: `never weighed`. Absolutely not 0 — a 0 kg dog would wreck the average. |
| Row 4: Rex is 45 | **Impossible** | The oldest dog ever recorded lived to 29. Blank it, note `was 45, impossible`. Do not guess 4 or 5. |
| Row 6: Zara weighs −5 kg | **Impossible** | Negative mass doesn't exist. Blank it, note `was -5, impossible`. |
| Row 3 is identical to row 1 | **Duplicate** | Delete row 3. Bruno was counted twice. |
| `Beagle` (row 2) vs `beagle` (row 5) | **Inconsistent** | Standardise to `beagle`. |
| `labrador` (rows 1, 3) vs `Labrador` (row 6) | **Inconsistent** | Standardise to `labrador`. |

> **🧑‍🏫 If a student says the duplicate might be two different dogs both called Bruno:** that is a genuinely excellent objection, and you should say so out loud. Two Bruno labradors, both 3, both 22 kg, is *possible*. The reason we call it a duplicate here is that everything matches exactly, which is much more likely to be a copy-paste than a coincidence — and the reason we can't be certain is that nobody gave the rows unique IDs at collection time. That uncertainty is real and permanent. Praise it.

**Do this — the payoff.** Compute the average weight before and after, out loud, together.

> **Before** (all the numbers as written, skipping the blank):
> 22 + 8 + 22 + 30 + (−5) = **77**, over 5 numbers → **15.4 kg**
>
> **After** (duplicate deleted, both impossibles blanked):
> 22 + 8 + 30 = **60**, over 3 numbers → **20.0 kg**

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "How much did the average move?" | "4.6 kg" / "about 30%" | If they struggle with the percentage, just take the difference. The size is the point, not the arithmetic. |
| "Which single fault moved it most?" | "The minus five." | Check it together: without only the −5 it would be (22+8+22+30)/4 = 20.5. Yes — the negative did most of the damage. |
| "How many different breeds does a computer see in the dirty table?" | "Five." | Count them: `labrador`, `Beagle`, `beagle`, `german shepherd`, `Labrador` = **5**. After cleaning: **3**. |
| "So what did cleaning actually do to the breed column?" | "Made three real groups instead of five fake ones" | Land it: with 5 groups of one or two dogs each, there is nothing to learn. With 3 groups there is. **Cleaning didn't tidy the table; it created the information.** |

---

### 🎲 Activity — Crime Scene Table (40–60)

Full instructions below. In brief: the student gets a printed twelve-row table with nine planted faults and one outlier, and hunts all of it with four coloured pens, naming each fault in the margin and proposing a fix. Then they write the controlled vocabulary that would have prevented the Monday problem.

**Do this at minute 40:** lay out the four pens, point at the legend, and hand over the student copy of the table face down.

**Say this:**

> "Twelve rows. Nine faults. One thing that looks like a fault and isn't — and if you cross that one out, you've made the worst mistake in the lesson, so think before you cross.
>
> Four pens, one per fault type. Circle it, then write in the margin what kind it is and what you'd do about it. Twelve minutes. Turn it over. Go."

---

### 🔑 Wrap & Assign (60–70)

**Do this:** put the marked-up Crime Scene Table where you can both see it.

**Say this:**

> "Three things.
>
> One. **Every column has a type, and the test is arithmetic.** If adding two of them doesn't mean anything, it's a category, no matter how many digits it's made of.
>
> Two. **There are four kinds of mess and they have different fixes.** Missing: leave blank and note. Duplicate: check, then delete one. Impossible: blank and note, never guess. Inconsistent: write the allowed list.
>
> Three, and this is the one I care most about. **Weird is not the same as wrong.** An impossible value is outside what reality allows, and you remove it. An outlier is inside what reality allows and just far from the rest, and you keep it and write a note. Four hundred and eighty minutes was the most interesting row in that table and you nearly crossed it out."

**Do this:** the controlled vocabulary, written properly. Have them write, at the top of their own Week 4 homework table, the allowed values for their category column. Actual example, actual list. It should look like:

```
ALLOWED VALUES for meal_type:  breakfast · lunch · dinner · snack
Nothing else goes in this column. Ever.
```

**Do this:** fill in the vocabulary box together — five words, in their own words.

| Word | The definition you're steering to |
|---|---|
| **data type** | What kind of value a column holds, which decides what you can do with it |
| **missing value** | An empty box where a measurement should be |
| **duplicate** | The same example written down twice |
| **impossible value** | A value reality doesn't allow |
| **controlled vocabulary** | The written list of allowed answers for a category column |

Then assign the homework as written below.

---

## 🎲 The Activity, In Full

### Crime Scene Table

**Time:** 20 minutes (12 hunting, 5 discussing, 3 writing the vocabulary)
**Group size:** 1 student, or pairs with one sheet each and a shared discussion
**The point:** diagnosis, not tidying

![The Crime Scene Table with all nine faults marked](../figures/fig-w05-3-crime-scene-table.svg)
*Figure 5.6 — The teacher copy, with every fault pinned. The student's sheet is identical but has no pins and no shading.*

### Materials

- Workbook Week 5, page 2: the Crime Scene Table, **student version** (no pins, no shading)
- Four coloured pens or highlighters
- The colour legend, visible
- This teacher guide's Answer Key, in your hand, not theirs

### The table they get

One row = one school day. Twelve rows, Mondays, Wednesdays and Fridays through August 2026.

| day | date | sleep_h | bag_kg | screen_min |
|---|---|---|---|---|
| Monday | Aug 3 | 7.5 | 4.1 | 95 |
| Wed | Aug 5 | 8.0 | 3.8 | 120 |
| Fri | Aug 7 | 6.5 | 4.0 | 480 |
| monday | Aug 10 | 7.0 | 4.2 | 110 |
| Wed | Aug 12 | | 3.9 | 105 |
| Fri | Aug 14 | 8.5 | −3.2 | 150 |
| MON | Aug 17 | 7.5 | 4.4 | 130 |
| Wed | Aug 19 | 88 | 4.0 | 140 |
| Fri | Aug 21 | 9.0 | 4.1 | |
| Mon. | Aug 24 | 7.0 | 4.3 | 115 |
| Wed | Aug 26 | 8.0 | 3.7 | 125 |
| Wed | Aug 26 | 8.0 | 3.7 | 125 |

### Setup (1 minute)

Legal ranges, written on the board before they start — they need these to judge "impossible":

```
sleep_h     0 to 16
bag_kg      0.1 to 12
screen_min  0 to 1440
```

### Rules

1. **One colour per fault type.** No mixing.
2. **Circle the fault, then write in the margin two things: what kind it is, and what you'd do.** A circle with no words scores nothing.
3. **You may not change any number on the sheet.** You propose fixes; you do not apply them. (This keeps the original readable and models what real data cleaning does — you log changes, you don't silently overwrite.)
4. **Say out loud before you cross anything out.** Especially anything that surprises you.

### Timing inside the activity

- **Minutes 0–12:** hunting, in silence, alone. Do not help. Do not hover. If they stall at six faults, say only: "There are nine. Two of them are the same *kind*."
- **Minutes 12–17:** the discussion. This is the best five minutes of the term — see below.
- **Minutes 17–20:** they write the controlled vocabulary for the `day` column.

### The five-minute discussion — how to run it

Go through the faults in the order *they* found them, not in your order. For each one, ask two questions: **which kind?** and **what's the fix?**

Then, whether or not they circled 480, do this:

**Say this:**

> "Right. One left. Look at the screen-minutes column and tell me the number that doesn't belong."

They will say 480.

**Say this:**

> "Cross it out then."

**Wait.** Do not say anything else. Give it a full five seconds of silence.

If they cross it out, let them, and then ask: *"What's the legal range for screen minutes?"* They wrote it down: 0 to 1440. *"Is 480 inside that range?"* Yes. *"So what rule did you just break?"*

If they hesitate or refuse — praise it immediately and hard. That hesitation is the single best thing that will happen in this lesson.

**Then say this:**

> "480 minutes is eight hours. It's inside what's possible. It's not a fault — it's an **outlier**, and it's the most interesting row on the page. Look across that row: that's also the night with the *lowest* sleep in the whole table, six and a half hours. The one weird value and the one low value are on the same line.
>
> If you'd crossed it out, you'd have deleted the only interesting thing in this dataset, and the table would have looked *tidier*, and you'd never have known.
>
> So the rule is: an impossible value gets blanked. An outlier gets **kept and annotated**. Write in the margin: 'outlier, not a fault — investigate'."

### Writing the controlled vocabulary (3 minutes)

**Say this:**

> "Last job. The Monday problem. Write me the thing that would have stopped it from ever happening."

They should write, at the top of the sheet:

```
ALLOWED VALUES for day:  Mon · Wed · Fri
Nothing else goes in this column.
```

Marking points: it must be an explicit written list, it must be short, and it must state that nothing else is allowed. `"be consistent"` fails. `"use short forms"` fails — it isn't a list.

> **🧑‍🏫 If a student asks whether it should be `Mon` or `Monday`:** it genuinely does not matter, and say so. What matters is that one is chosen and written down. Offer them the choice and make them commit. That moment — realising the *choice* is arbitrary but *making* the choice is not — is worth a lot.

### What "finished" looks like

- Nine faults circled, each in the right colour
- Nine margin notes, each naming the kind and the fix
- The 480 either uncircled, or circled and annotated `outlier — keep`
- A written controlled vocabulary for the `day` column at the top of the sheet

### Variation — easier

- **Tell them the count per type up front:** "two missing, one duplicate, two impossible, four spellings." Removes the searching load and keeps the diagnosis.
- **Do the first two faults together**, out loud, then hand over.
- **Cut to eight rows** (delete Aug 21, Aug 24, Aug 26, Aug 26 — but then you lose the duplicate, so instead delete Aug 5, Aug 12, Aug 17 and keep the rest). Six faults in nine rows is a fair reduced target.
- Skip the controlled vocabulary writing and just *say* it together.

### Variation — harder

- **Don't give them the legal ranges.** Make them write the ranges first, from scratch, and defend each one. "Why 16 and not 12?" is a genuinely hard question with no single right answer.
- **Add the arithmetic:** have them compute average sleep before and after cleaning themselves. Before is 15.00; after is 7.67. Then ask which single fault caused the biggest movement.
- **The forgery task:** hand them a clean eight-row table and 4 minutes to plant five faults in it, one of each kind plus one fake outlier. Then you hunt. Planting faults requires understanding them completely, and watching you work is genuinely engaging.
- **The impossible question:** "Row 9 has no screen time. Is that a missing value, or did they genuinely have zero screen time?" There is no way to tell from the table. The correct answer is that only a note written on the day could distinguish them — and that is why data collection sheets have a notes column.

---

## ❓ Questions Students Ask This Week

**"Why can't we just fill the blank with the average? It's the closest we can get."**
It is a real technique and professionals do use it on very large datasets. We don't, for two reasons. First, on a twelve-row table you'd be inventing a meaningful fraction of your own data. Second, and worse, once it's filled in nothing on the page marks it as invented — three weeks later it looks exactly as real as the measured numbers. A visible blank keeps you honest. If you ever do fill a gap, the rule is: log it, and mark it.

**"Was the 88 a typo for 8.8 or for 8?"**
**Nobody knows, and nobody ever will.** That's not me being coy — the information is genuinely gone. Both are plausible: `8.8` is a slipped decimal point, `8` is a doubled keypress. There is no clever method that recovers it. That's precisely why we blank it and write "was 88, original lost" rather than picking one. And it is the strongest possible argument for writing notes at the moment you collect, because the person who typed 88 knew, for about four seconds, what they meant.

**"Isn't deleting the duplicate row also losing data?"**
Sharp question. Yes — if it was a genuine coincidence rather than a copy-paste, you've just deleted a real example. That's why we say *check before you delete*. Here the whole row matches exactly, including the date, and there was only one 26th of August, so it's a copy. If the dates had differed, we'd keep both. The permanent fix is to give every row a unique ID when you collect it, so a real duplicate is obvious and a coincidence is safe.

**"What if I find a fault in my own table from last week?"**
Then the homework has already worked. That's the job. Log it, fix it, and note what you did. Finding faults in your own work isn't embarrassing — it's the only evidence that you actually looked.

**"How does a big company clean billions of rows? They can't use coloured pens."**
They write programs that do the four checks automatically: count the blanks, count the distinct values in each category column, flag anything outside a legal range, look for identical rows. Exactly the four things you did, just executed millions of times a second. The interesting part is that the *judgements* don't automate. A program can flag 480 as unusual; only a person can decide whether it's a sick day or a typo. That's still true at every company in the world.

**"If a table has faults in it, does that mean the AI trained on it is wrong?"**
Not automatically, and this is worth being careful about. A few bad rows in a million might make no measurable difference. A few bad rows in twelve will wreck everything. And some faults are much more dangerous than others: an impossible value that's obviously silly often gets caught, while an inconsistent category quietly splits one group into four and nobody notices at all. The honest answer is that it depends on how many, which kind, and how big the table is — and this is why every serious project has somebody whose actual job is this.

**"Is there a way to make data that has no faults at all?"**
No. Not at any scale that matters. Anything collected by humans over time drifts, gets forgotten, gets typed wrong. The goal was never perfect data — it's *data whose faults you know about and have written down*. That's next week's lesson, and it's the difference between a spreadsheet and something you can trust.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The student crosses out the 480 in three seconds flat and moves on | It looks weird, and crossing things out feels productive | Don't stop them mid-hunt. Save it for the discussion and run the "cross it out then" silence. The mistake is far more useful once they've committed to it. |
| They fill blank cells with 0 during the activity | A blank feels unfinished; 0 feels like an answer | Stop immediately, this one is worth interrupting for. Recompute the average sleep with their 0 in it, out loud. Then ask: "Did this person sleep zero hours, or did we not write it down?" |
| They find the four Mondays but count them as one fault | It *is* one problem — they're being logical | Accept the logic and then reframe: "One problem, four broken cells. Circle all four, because each one needs fixing." Do not mark them down; they were right. |
| They can't find the duplicate at all | It's the hardest one — the row looks completely normal | Nudge without giving it: "Read the dates out loud, top to bottom." Hearing "Aug 26… Aug 26" finds it every time. |
| They start *fixing* the table instead of diagnosing it | Fixing feels like the real work | Point at rule 3. Say: "Real data cleaning logs the change; it never silently overwrites. If you rub it out, nobody can ever check you." |
| Ten minutes in and they've found three faults | Nine is a lot for twelve rows | Give a structural hint, not the answers: "Go column by column instead of row by row. Do the whole `day` column first." Column-wise scanning finds inconsistencies immediately. |
| They insist −3.2 kg is possible "if the scale was broken" | It's a reasonable thought | Agree, then separate the two questions: "You might be right about *why* it happened. But is the value itself possible? Can a bag weigh less than nothing?" A broken scale is an explanation for an impossible value, not a reason to keep it. |
| They argue the 88 should be changed to 8.8 | It's the obvious repair | "Show me how you know it was 8.8 and not 8." They can't. Land it: a guess that looks like a measurement is worse than a hole. |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** the data-type section down to one example (bus routes), and the worked example down to two faults. Keep the whole activity — the hunt is the lesson.

**Reteach like this:** do one fault type at a time, with a separate pass over the table for each. Pass 1: "find every empty box." Pass 2: "find every number that's impossible." Pass 3: "read the day column out loud." Pass 4: "read the dates out loud." Four short passes beats one long hunt for almost every struggling student, and it teaches a real method — professionals check one thing at a time too.

**Reduce the load:** give them the count per type before they start ("two missing, two impossible, one duplicate, four spellings"). This converts an open search into a checklist, which is a completely legitimate scaffold.

**The minimum acceptable outcome for today:** they can find the two blanks and the 88, they can say a blank must not be filled with 0, and they can say that 480 is not a fault. Those three are the whole lesson in miniature.

### If they are flying

1. **"The average sleep before cleaning is 15.0. After cleaning it's 7.67. Now find the middle value of the sleep column before cleaning — sort them and take the one in the middle."** Sorted: 6.5, 7, 7, 7.5, 7.5, 8, 8, 8, 8.5, 9, 88 → the middle one is the sixth, which is **8.0**. So the middle value barely moved while the average exploded. Ask why. *(Because the middle value doesn't care how big the biggest number is — only where it sits in the order.)* This is the median, and it is a genuine, real idea; you can name it, but don't teach a procedure around it.
2. **"Which of the nine faults would have done the most damage if a machine had trained on this table, and why?"** Strong answers argue for the four Mondays: the impossible values are loud and get caught, but splitting one day into four categories is silent and permanent. Accept a well-argued case for the 88 too.
3. **"Design a collection sheet that makes each of the four faults physically impossible to commit."** Real answers: a printed dropdown list for `day`; a box that prints the legal range next to each number column; a pre-printed row ID; a mandatory "why is this blank?" line. This is professional-level thinking from an 11-year-old and worth taking seriously.
4. **"Row 9 has no screen time. Missing, or a genuine zero?"** Unanswerable from the table. The point of the question is to make them say "you can't tell" — and then to see what would have made it tellable.
5. **The forgery task** from the harder variation.

### If they won't engage today

**Make it a game with a score.** "Nine faults hidden. I'll tell you how many you've got, not which ones. How few guesses can you do it in?" The scoring turns a worksheet into a puzzle and it works on almost everyone.

**Make it about you.** Show them a real messy list of your own — a shopping list, a contacts list with three versions of the same name, an old spreadsheet. "Find my mistakes." Hunting an adult's errors is dramatically more motivating than hunting an anonymous table's.

**Or shrink it hard.** Take just the `day` column, twelve values, and nothing else. "How many different days are in this list?" They'll say 3. "A computer says 6. Why?" That is a complete, honest, ninety-second lesson, and if that's all you get today, take it and move on.

**Do not skip:** the 480 discussion. If you only get five minutes of engagement all lesson, spend it there.

---

## ✅ Assessing Understanding

Do these in the last five minutes. Exact wording below.

### Check 1 — The averaging test (45 seconds)

> "I've got a column called `bus_route` full of numbers, and a column called `journey_minutes` full of numbers. I average both. Which answer is meaningless, and why?"

**A good answer looks like:** "`bus_route` — because route 7 plus route 12 isn't route 19, it's a different bus. The numbers are names, not amounts."
**A weak answer looks like:** "The bus one because buses aren't numbers." Push once: "But it *is* written as a number. What's the actual test?" You want them to reach for addition.

### Check 2 — Name the fault and the fix (90 seconds)

Read these four aloud, one at a time. For each: **what kind of fault, and what do you do?**

1. "A dog's age is listed as 45." → **Impossible.** Blank it, note `was 45, impossible`. Don't guess.
2. "Two rows are identical, same date and everything." → **Duplicate.** Check the date is genuinely the same day, then delete one.
3. "The breed column has `Beagle` and `beagle`." → **Inconsistent.** Standardise to one, and write the allowed list.
4. "The weight box for row 5 is empty." → **Missing.** Leave blank, add a note. **Never 0.**

**A good answer:** three or four correct, with the fix, not just the name.
**A weak answer:** naming the fault but not the fix, or saying "delete the row" for the missing value.

### Check 3 — The trap (60 seconds)

> "Your screen-time column reads 95, 120, 110, 105, 150, and 480. Is the 480 a fault? Tell me why or why not, and tell me what you'd do."

**A good answer looks like:** "Not a fault — 480 minutes is eight hours, which is possible. It's an outlier. Keep it and write a note saying what happened that day."
**A weak answer looks like:** "Yes, delete it." Ask: "What's the legal range for screen minutes?" Then: "Is 480 inside it?" Let them get there.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Fills blanks with 0. Cannot name the fault types. Deletes the outlier and can't say why it was wrong. |
| **2 — Emerging** | Finds the loud faults (blanks, 88) with prompting. Names them if given the list of four. Still treats "weird" as "wrong". |
| **3 — Secure** | Finds 7+ of the 9 unprompted, names each kind, gives the right fix. Leaves the 480 alone after discussion. **Target for Week 5.** |
| **4 — Strong** | Finds all 9 including the duplicate. Leaves the 480 alone *without* discussion, and can justify it with the legal range. Writes a usable controlled vocabulary unprompted. |
| **5 — Exceptional** | Argues which fault is most dangerous and why, using the idea that silent faults beat loud ones. Notices that the outlier row is also the lowest-sleep row. Proposes a collection sheet that prevents the faults at source. |

---

## 📤 Homework to Assign

**Workbook Week 5, pages 3 and 4 — the Fault Log, run on their own table.**
**Time: 45–60 minutes across the week, including continued data collection.**

**Say this:**

> "Three jobs.
>
> **One. Keep collecting.** You should be at fourteen rows by now. Get to twenty-one by next week. Next week we finish at thirty and turn it into a real dataset.
>
> **Two. Run all four checks on the rows you already have** — the same four you did today. Blanks. Duplicates. Impossible values. Inconsistent spellings. Do it as four separate passes, one check at a time, one column at a time. It's faster and it finds more.
>
> Every fault you find goes in the fault log table on page 4, with four things: which row, which column, what kind of fault, and what you did about it. **Every single change gets logged.** If you change a value and don't log it, you've destroyed your own record of what actually happened — and you will not remember in three weeks. I promise you that.
>
> Before you start, write your legal ranges at the top: what's the smallest and biggest each of your number columns is allowed to be. You can't spot an impossible value if you never said what's possible.
>
> **Three. The last question on page 4, and it's the one I'll be reading first.** Of all the faults you found, which one would have been the most *dangerous* if a machine had trained on your table — and why? Two or three sentences. There's more than one good answer; I want the reasoning, not the answer.
>
> And a warning, because it will happen: **you might find zero faults.** If so, don't invent one. Write 'no faults found' and then write down what checks you ran, so I can see you actually looked. Finding nothing after four real checks is a completely respectable result."

**What to check when it comes in:** the legal ranges are written down; the log has a row per change (not a summary); no blanks were filled with 0; and the "most dangerous" answer gives a *reason*, not just a fault.

---

## 🔑 Answer Key

### Lesson questions

**Hook — "Is 15.0 hours a night possible?"**
Possible for a single night, not credible as a twelve-day average — it would mean 8pm to 11am every day. So the table, not the person, is the problem.

**Hook — "What could make an average come out too high?"**
One value that is far too large. With only twelve rows, a single bad cell dominates.

**Concept Part A — the averaging test.**

| Column | Type | Why |
|---|---|---|
| `sleep_hours` | Number | 3 h + 8 h = 11 h, meaningful |
| `bus_route` | Category | Route 7 + route 12 ≠ route 19 |
| `weight_g` | Number | 200 g + 340 g = 540 g, meaningful |
| `student_id` | Category | ID 1001 + ID 1002 = a different person, or nobody |
| `postcode` | Category | Valid arithmetic, meaningless result |
| `shirt_number` | Category | No player *is* the average shirt number |
| `mood_1to5` | Ordered category | 5 really is more than 4, so it sorts. Averaging is standard and slightly fake |

**Concept Part C — "What could make a real day come out at 480 screen-minutes?"**
Home ill; a school holiday; travelling all day; the day a long film was watched; a power cut at school sending everyone home. Any concrete cause is a correct answer — the point is that a cause exists.

**Concept Part C — "Can you always tell an outlier from a mistake?"**
No. Without a note written at the time, 480 could be a real day or a mis-typed 48, and nothing recovers the truth.

### Worked Example — the six dogs

**All six faults:**

| # | Row | Column | Kind | Fix |
|---|---|---|---|---|
| 1 | 5 | `weight_kg` | Missing | Leave blank, note `never weighed`. Not 0. |
| 2 | 4 | `age_years` | Impossible | Oldest recorded dog was 29. Blank, note `was 45, impossible`. |
| 3 | 6 | `weight_kg` | Impossible | Negative mass. Blank, note `was -5, impossible`. |
| 4 | 3 | whole row | Duplicate | Identical to row 1 in every column but `id`. Delete row 3. |
| 5 | 2, 5 | `breed` | Inconsistent | `Beagle` vs `beagle` → standardise to `beagle`. |
| 6 | 1, 3, 6 | `breed` | Inconsistent | `labrador` vs `Labrador` → standardise to `labrador`. |

*(A seventh, if the student spots it: `german shepherd` contains a space, which causes trouble in many tools. `german_shepherd` is safer. Accept it as a bonus, not a required find.)*

**The cleaned table:**

| id | name | age_years | weight_kg | breed | note |
|---|---|---|---|---|---|
| 1 | Bruno | 3 | 22 | labrador | |
| 2 | Coco | 2 | 8 | beagle | |
| 4 | Rex | | 30 | german_shepherd | age was 45, impossible |
| 5 | Milo | 1 | | beagle | never weighed |
| 6 | Zara | 4 | | labrador | weight was −5, impossible |

**Average weight:** before = (22 + 8 + 22 + 30 − 5) ÷ 5 = 77 ÷ 5 = **15.4 kg**. After = (22 + 8 + 30) ÷ 3 = 60 ÷ 3 = **20.0 kg**. Movement: **4.6 kg, about 30%.**

**Distinct breeds:** before **5** (`labrador`, `Beagle`, `beagle`, `german shepherd`, `Labrador`); after **3** (`labrador`, `beagle`, `german_shepherd`).

### Activity — the Crime Scene Table: all nine faults

Numbered in reading order, matching the pins in Figure 5.6.

| Pin | Row | Column | Kind | What's wrong | Fix |
|---|---|---|---|---|---|
| **1** | Aug 3 | `day` | Inconsistent | `Monday` | Standardise to `Mon` |
| **2** | Aug 10 | `day` | Inconsistent | `monday` | Standardise to `Mon` |
| **3** | Aug 12 | `sleep_h` | Missing | Empty box | Leave blank, note `forgot to record`. **Not 0.** |
| **4** | Aug 14 | `bag_kg` | Impossible | −3.2 kg | Blank it, note `was -3.2, impossible` |
| **5** | Aug 17 | `day` | Inconsistent | `MON` | Standardise to `Mon` |
| **6** | Aug 19 | `sleep_h` | Impossible | 88 h = 3.7 days | Blank it, note `was 88, impossible, original lost`. Do not guess 8 or 8.8. |
| **7** | Aug 21 | `screen_min` | Missing | Empty box | Leave blank, note. **Not 0.** |
| **8** | Aug 24 | `day` | Inconsistent | `Mon.` | Standardise to `Mon` |
| **9** | Aug 26 (second) | whole row | Duplicate | Identical to the row above, same date | Delete one. Only one 26 August existed. |

**Pin 10 — the trap.** Aug 7, `screen_min` = **480**. **Not a fault.** It is inside the legal range 0–1440, so it is legal. It is an **outlier**: 8 hours, far from the 95–150 cluster. Keep it, and write a note (`why was this day different?`). Bonus observation for strong students: this row also has the lowest sleep in the table, 6.5 h — the two facts sit on the same line, which is the only genuinely interesting thing in the whole dataset.

**Fault counting.** Nine faults, but only **four kinds**, and the four Monday spellings are one *problem* in four *places*. Students who report "six faults" because they counted the Mondays as one are reasoning correctly; mark it right and ask them to circle all four cells anyway.

### Activity — the arithmetic

![The wrecked table before and after cleaning](../figures/fig-w05-4-before-after-clean.svg)
*Figure 5.7 — Every number in this figure is worked below.*

**Average `sleep_h` before cleaning.** Eleven non-blank values: 7.5, 8.0, 6.5, 7.0, 8.5, 7.5, 88, 9.0, 7.0, 8.0, 8.0.
Sum = 7.5 + 8.0 = 15.5; + 6.5 = 22.0; + 7.0 = 29.0; + 8.5 = 37.5; + 7.5 = 45.0; + 88 = 133.0; + 9.0 = 142.0; + 7.0 = 149.0; + 8.0 = 157.0; + 8.0 = **165.0**.
165.0 ÷ 11 = **15.00 hours**.

**Average `sleep_h` after cleaning.** Duplicate row deleted (removes one 8.0), the 88 blanked, the Aug 12 blank stays blank. Nine values: 7.5, 8.0, 6.5, 7.0, 8.5, 7.5, 9.0, 7.0, 8.0.
Sum = **69.0**. 69.0 ÷ 9 = **7.666… = 7.67 hours**.

**Movement: 15.00 → 7.67, a drop of 7.33 hours, caused overwhelmingly by one cell.**

**Average `bag_kg` before.** Twelve values: 4.1, 3.8, 4.0, 4.2, 3.9, −3.2, 4.4, 4.0, 4.1, 4.3, 3.7, 3.7. Sum = **41.0**. 41.0 ÷ 12 = **3.4166… = 3.42 kg**.

**Average `bag_kg` after.** Duplicate deleted (removes one 3.7), the −3.2 blanked. Ten values: 4.1, 3.8, 4.0, 4.2, 3.9, 4.4, 4.0, 4.1, 4.3, 3.7. Sum = **40.5**. 40.5 ÷ 10 = **4.05 kg**.

**This is the important one.** The bag average looked completely believable at 3.42 kg. Nothing about it raised a flag. It was still wrong by 0.63 kg — about 16%. **A wrong number that looks reasonable is far more dangerous than one that looks silly.**

**Average `screen_min` before.** Eleven non-blank values. Sum = 95 + 120 + 480 + 110 + 105 + 150 + 130 + 140 + 115 + 125 + 125 = **1695**. 1695 ÷ 11 = **154.09 minutes**.

**Average `screen_min` after.** Duplicate deleted, the 480 **kept**. Ten values, sum = **1570**. 1570 ÷ 10 = **157.0 minutes**.

Note what happened: cleaning moved the screen average *up* slightly, and the outlier stayed. Cleaning is not the same as making numbers smaller or tidier.

**Distinct `day` values:** before **6** (`Monday`, `Wed`, `Fri`, `monday`, `MON`, `Mon.`); after **3** (`Mon`, `Wed`, `Fri`).

**Row count:** before **12**; after **11**.

### Activity — the controlled vocabulary

Full credit:

```
ALLOWED VALUES for day:  Mon · Wed · Fri
Nothing else may be typed in this column.
```

Also full credit with `Monday · Wednesday · Friday`, as long as it is an explicit closed list. **Not** full credit: "be consistent", "use three letters", "write it the same each time" — none of those is a list, and none can be checked.

### Workbook Week 5, page 1 — Type the column

*Label each as number, category, text or time, and say whether averaging makes sense.*

| Column | Type | Average it? | Why |
|---|---|---|---|
| `shoe_size` | Number (ordered) | ⚠️ Sort of | Evenly spaced and ordered, so "average 7.4" is usable — but mixing UK, US and EU scales ruins it |
| `favourite_colour` | Category | ❌ No | Red + blue isn't a colour, and blue isn't "more" than green |
| `bus_route_number` | **Category** | ❌ No | A name printed with digits |
| `temperature_celsius` | Number | ✅ Yes | Real measurement on a real scale |
| `text_message_body` | Text | ❌ No | You can't average sentences. You *can* count the characters — but that's a new number column you created |
| `date_of_birth` | Time | ⚠️ Technically | The average of two birthdays is a real date. Usually convert to `age_years` first |
| `student_id` | **Category** | ❌ No | The classic trap: ID 1001 + ID 1002 means nothing |
| `race_finish_seconds` | Number | ✅ Yes | Real measurement; the average is a real time |
| `house_number` | **Category** | ❌ No | Number 12 plus number 40 is not number 52 |
| `mood_1to5` | Ordered category | ⚠️ Commonly done | 5 is genuinely happier than 4. Averaging is standard and slightly fake |

**The three number-looking categories are `bus_route_number`, `student_id` and `house_number`.** Accept `shoe_size` as a fourth if argued well — sizes are a manufacturing scale, not a physical measurement.

### Workbook Week 5, page 2 — the Crime Scene Table

See the nine-fault table above, plus the outlier at Aug 7, plus the arithmetic.

**Extra question on the page: "How many faults are there really — nine or six?"**
Both answers are defensible and both get full credit if reasoned. **Nine broken cells** (or, more precisely, eight broken cells plus one duplicated row). **Four kinds of problem.** **Six distinct incidents** if you treat the four Mondays as a single inconsistency. The best answer says all of that and notes that the count depends on whether you're counting *cells to fix* or *problems to prevent* — and that the two counts lead to different actions: nine corrections, but only four rules needed to stop it happening again.

### Workbook Week 5, page 3 — Write the controlled vocabulary

*Three columns are given; write the allowed list for each.*

1. **`day`** (from the Crime Scene Table) → `Mon · Wed · Fri`
2. **`meal_type`** (for a food tracker) → `breakfast · lunch · dinner · snack`. Marking point: it must be closed. "Anything I eat" fails.
3. **`weather`** (for a weather tracker) → `sunny · cloudy · rain · storm`. Any short closed list is correct. The extra credit is noticing the hard case — what do you write on a day that is sunny *then* rains? A full-credit answer either adds a rule ("whatever it was at 8am") or adds a value (`mixed`). Naming the ambiguity is worth more than the list.

**General marking rule for this page:** a controlled vocabulary must be (a) a list, (b) short, (c) closed — with an explicit statement that nothing else is allowed, and (d) accompanied by a rule for the awkward case.

### Workbook Week 5, page 4 — the Fault Log, on their own table

No single answer; the marking criteria are:

- [ ] Legal ranges written for every number column *before* the checks
- [ ] All four checks visibly run (four passes, not one glance)
- [ ] One log line per change: `row | column | kind of fault | what I did`
- [ ] Zero blanks filled with 0
- [ ] Any outlier is kept and annotated, not deleted
- [ ] "No faults found" is accepted **only** if the four checks are listed

**The final question — "which fault would have been most dangerous if a model had trained on it?"**

There is no single right answer. Three answers that earn full credit:

> **The inconsistent spellings.** "The impossible values are loud — 88 hours makes you stop and look. The four Mondays are silent. Nothing warns you, the table looks perfectly fine, and the machine quietly thinks there are four different days that each happened once. It would never learn anything about Mondays, and I'd never find out why."

> **The blank filled with a zero** *(if they did it, or nearly did)*. "If I'd put 0 in the empty sleep box, I'd have claimed I didn't sleep at all that night. The average would drop and nothing on the page would say it was made up. It's the only fault that actively lies rather than just being absent."

> **The duplicate.** "It's the only fault that doesn't look like a fault at all. Every value in it is legal and sensible. It just makes one day count twice, and none of the checks except a specific duplicate check would ever see it."

**What does not earn full credit:** "the 88, because it's the biggest." Size isn't danger. Push back with: *which fault is hardest to notice?* Danger lives in silence, not size.

---

## 🔮 Next Week Preview

Next week is a lab, and we open a computer for the first time. The student finishes their thirty-row table in Google Sheets, computes two averages with a real formula, and then immediately has to write down what those averages *are not* evidence for. Then we interrogate a real dataset off a real web page with five questions — who collected it, from whom, when, how, and with whose permission — writing "unknown" every time the page won't say, which will be more often than they expect. They finish by writing a seven-line data card for their own dataset and reading it out loud.

**Prep early:** you need a **working browser and a Google account** (or Excel, or LibreOffice — all three work identically for everything we do). Test that you can create a blank spreadsheet and type `=AVERAGE(B2:B10)` into a cell before the lesson. Also, **pick your web page now** — any page with a statistic on it: a news article with a percentage, a sports stats page, a Wikipedia table. Choose one that will frustrate you slightly, because a page that answers all five questions makes for a very boring lesson.

And chase the row count. The student needs 21 rows by next week and 30 by the end of it.

---

[⬅ Week 4](week-04.md) · [Course Home](../README.md) · [Week 6 ➡](week-06.md) · [Student Guide](../student-guide/week-05.md) · [Workbook](../workbook/week-05.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
