# Module 2 — Data Is Everywhere: Turning the World Into Rows and Columns

**Level 1 · Module 2 · ~3 hours · Prereqs: Module 1 (you can sort a system into rule-based, machine learning, or generative)**

[⬅ Previous](module-01-what-ai-is-and-isnt.md) · [Level 1 Home](README.md) · [Next ➡](module-03-patterns-and-rules.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** turn any real-world collection of things into a table, with rows as examples and columns as attributes.
2. **You will be able to** classify a column as **number**, **category**, **text**, **image**, or **time** data — and say why the type changes what you can do with it.
3. **You will be able to** spot missing values, duplicates, typos, and impossible entries in a table, and decide what to do about each one.
4. **You will be able to** write a **data card**: a short honest note saying what your data is, how much there is, and where it came from.
5. **You will be able to** explain why 30 rows about you are not 30 rows about everybody.

---

## 🪝 The Hook

In 2015, a hospital in the United States built a system to predict which pneumonia patients were likely to die, so doctors could keep the risky ones in hospital and send the safe ones home. The system learned from thousands of real patient records. It worked well on the numbers.

Then someone checked its rules and found something horrifying. The system had learned: *patients with asthma are LOW risk — send them home.*

That is exactly backwards. Asthma makes pneumonia far more dangerous. But here is why the data said otherwise: for decades, hospitals had sent asthma patients with pneumonia **straight to intensive care**. They got the best treatment immediately. So in the records, they survived more often. The machine read the survival numbers and concluded asthma was protective.

The model wasn't broken. The learning wasn't broken. The **data** carried a hidden story that nobody had written down, and the machine believed it.

Everything an AI knows arrived as data. If you don't know how the data was made, you don't know what your model learned. This module is about making data you can actually trust.

---

## 🧠 The Concept

Five ideas. Each one gets a plain explanation, an everyday anchor, and a small example with real numbers.

---

### 1️⃣ Data is recorded observations — and the table is its universal shape

You look out the window. It's raining. You *know* it's raining. That knowledge is in your head, and a machine cannot use it.

Now you write in a notebook: `2026-09-02, rain, 18°C`. You just made **data**.

> **Data** — observations of the world that have been written down in a form a machine can read.

The magic word is *recorded*. Nothing counts as data until it leaves someone's head and lands somewhere countable.

**🍕 Analogy — the class register.**
Every school on Earth keeps a register. It has one line per student and one column per thing the school needs to know: name, roll number, class, attendance today. Nobody had to invent that shape. It just *is* the shape you get when you write down facts about a group of things.

That shape has a name and two precise halves.

> **Row** — one example. One single thing you observed.
>
> **Column** — one attribute. One thing you measured about every example.

```
                    ┌─── COLUMNS: things you measured ───┐
                    │                                    │
                    ▼          ▼          ▼          ▼

              ┌──────────┬──────────┬──────────┬──────────┐
              │  name    │   age    │  class   │ present  │  ← header row
              ├──────────┼──────────┼──────────┼──────────┤
   ROWS:  ──► │  Asha    │   11     │   6A     │   yes    │  ← one student
   one        ├──────────┼──────────┼──────────┼──────────┤
   example ─► │  Ben     │   12     │   6A     │   no     │  ← one student
   each       ├──────────┼──────────┼──────────┼──────────┤
          ──► │  Carlos  │   11     │   6B     │   yes    │  ← one student
              └──────────┴──────────┴──────────┴──────────┘
```

**The two golden rules of tables:**

1. **Every row is the same kind of thing.** All students, or all photos, or all days. Never a mix.
2. **Every column measures the same attribute for every row.** If column 3 is "age in years" it must be age in years in *every single row* — never "age in years" for Asha and "birth year" for Ben.

Break rule 1 or rule 2 and your table becomes garbage, quietly, in a way that's very hard to find later.

**🔢 Tiny example — same facts, right table and wrong table.**

You want to record three pizzas.

❌ **Wrong** (breaks both rules):

| thing | info |
|---|---|
| Pizza A | margherita, 12 inch, ₹250 |
| Pizza B | 14 inch |
| Tuesday | we sold 40 pizzas |

Row 3 isn't a pizza at all — it's a day. And the `info` column crams three different attributes into one box, differently in each row.

✅ **Right:**

| pizza_id | topping | size_inches | price_rupees |
|---|---|---|---|
| A | margherita | 12 | 250 |
| B | margherita | 14 | 320 |
| C | pepperoni | 12 | 290 |

Every row is a pizza. Every column is one attribute, measured the same way every time. Now a machine can count, sort, average, and compare. In the wrong table, it can do none of those things.

---

### 2️⃣ Data types: number, category, text, image, and time

Not all columns behave the same way. Look at what you can legally *do* with each one.

> **Data type** — what kind of value lives in a column, which determines what operations make sense on it.

Five types matter at Level 1:

| Type | What it looks like | Can you average it? | Can you sort it? | Example column |
|---|---|---|---|---|
| **Number** | `18`, `7.5`, `250` | ✅ yes | ✅ yes | `sleep_hours` |
| **Category** | `red`, `6A`, `yes` | ❌ no | ⚠️ only if ordered | `favourite_colour` |
| **Text** | `"Are you coming?"` | ❌ no | ⚠️ alphabetically only | `message_body` |
| **Image** | a photo file | ❌ no | ❌ no | `dog_photo.jpg` |
| **Time** | `2026-09-02`, `21:30` | ⚠️ carefully | ✅ yes | `bedtime` |

**🍕 Analogy — the sports day scoreboard.**
Runner numbers on bibs are printed as numbers: 7, 12, 23. But averaging them gives 14, which means nothing — there's no such thing as "the average runner". Bib numbers are *categories that happen to look like numbers*.

Meanwhile, finish times (11.4s, 12.9s, 13.1s) genuinely average to 12.47s, and that number is meaningful.

**This is the trap that catches everyone: looking like a number and being a number are different things.**

**🔢 Tiny example — the postcode disaster.**

Three friends live at postcodes `560001`, `110001`, and `400001`.

Average = (560001 + 110001 + 400001) ÷ 3 = 1070003 ÷ 3 = **356667.67**

Postcode 356667 is a real place — a village in Rajasthan that none of the three has ever visited. The arithmetic is perfect and the result is nonsense, because postcode is a **category** wearing number clothes.

**The test:** ask *"if I add two of these together, does the answer mean anything?"*

- 3 hours of sleep + 8 hours of sleep = 11 hours of sleep. ✅ Meaningful. It's a number.
- Postcode 560001 + postcode 110001 = 670002. ❌ Meaningless. It's a category.
- Class 6A + Class 6B = ? ❌ Doesn't even compute. Category.

**Two special cases worth knowing now:**

**Ordered categories.** Some categories have a real order even though they aren't numbers. Mood on a 1–5 scale is one: 5 is genuinely happier than 4. You can sort them and find the middle one. Whether you can *average* them is genuinely debated by scientists — "average mood 3.4" is useful in practice but slightly fake, because the gap from 1 to 2 might not feel the same as the gap from 4 to 5. Use it, but know it's approximate.

**Images.** An image column doesn't hold the picture — it holds a *reference* to a picture (a filename). Module 7 will show you that a picture is secretly a giant grid of numbers, which means an image is really thousands of number columns squashed into one box.

---

### 3️⃣ Messy data: missing, duplicated, typo'd, and impossible

Real data is never clean. Here's a real-looking table of a week of sleep tracking — with everything that goes wrong, going wrong:

| day | date | sleep_hours | mood_1to5 | screen_minutes |
|---|---|---|---|---|
| Mon | 2026-08-24 | 7.5 | 4 | 95 |
| Tue | 2026-08-25 | 8 | 4 | 110 |
| Wed | 2026-08-26 |  | 3 | 120 |
| Thu | 2026-08-27 | 6.5 | 2 | 480 |
| Fri | 2026-08-28 | 88 | 5 | 200 |
| Sat | 2026-08-29 | 9 | 5 | 210 |
| Sat | 2026-08-29 | 9 | 5 | 210 |
| Sun | 2026-08-30 | 9.5 | fine | 180 |

Eight rows. **Four separate problems.** Find them before you read on.

---

**Problem 1 — Missing value (Wednesday, `sleep_hours` is blank).**

> **Missing value** — a box where a measurement should be but isn't.

Your options, and when to use each:

| Option | What it means | When it's right | When it's wrong |
|---|---|---|---|
| Leave it blank + note why | Honest gap | Almost always at Level 1 | Never really wrong |
| Delete the whole row | Throw away Wednesday | When the row is mostly empty | When you lose real information — Wednesday's mood and screen time are fine! |
| Fill with the average (8.1) | Guess the value | Big datasets, few gaps | Small datasets — you're inventing data |
| Fill with 0 | ☠️ | **Never for this** | Always. `0` means "slept zero hours", which is a *claim*, not a gap |

**The unforgivable one is filling with 0.** A blank says "I don't know". A zero says "I know, and it was zero". Those are opposite statements, and a machine cannot tell them apart. If you write 0, your average sleep drops from 8.1 to 7.0 and you'll never know why.

**Rule: a blank must stay visibly blank, with a note.**

---

**Problem 2 — Duplicate (Saturday appears twice, identically).**

> **Duplicate** — the same example recorded more than once.

Why it matters: duplicates give one example double the voting power. If a machine learns from this table, Saturday counts twice as much as Monday. With 8 rows, that skews everything.

But careful — **check before you delete.** Two rows can look identical and be genuinely different examples: two different students both aged 11 in class 6A scoring 78. That's not a duplicate, it's a coincidence, and you'd need an ID column to tell.

Here, `date` is `2026-08-29` twice, and there was only one Saturday the 29th. That's a genuine duplicate. **Delete one.**

**Fix for next time:** give every row a unique ID column. Then duplicates are obvious and coincidences are safe.

---

**Problem 3 — Impossible value (Friday, `sleep_hours = 88`).**

> **Impossible value** — a value outside what reality allows.

88 hours is 3.7 days. Nobody slept 88 hours on Friday.

The likely cause: a typo for `8.8`, or `8` with a stray keypress. You cannot fix it by guessing — you don't know which. But you *can* catch it, with a **range check**: before entering data, write down the legal range for every number column.

| Column | Legal range | Why |
|---|---|---|
| `sleep_hours` | 0 to 16 | More than 16 is medically unusual and needs a note |
| `mood_1to5` | 1 to 5 | The scale is defined that way |
| `screen_minutes` | 0 to 1440 | There are 1440 minutes in a day |

Any value outside the range gets flagged. **What to do with 88:** mark it missing and note "was 88, impossible, original value lost". You have lost one measurement. You have *not* lost your credibility.

---

**Problem 4 — Wrong type (Sunday, `mood_1to5 = "fine"`).**

The column is defined as a number 1–5. `"fine"` is a word. One text value in a number column poisons the whole column — every average, every sort, every chart breaks.

**Fix:** decide the mapping *in advance and write it down*. If your rule is "fine = 3", then apply it and record the translation. Never translate silently, because in three weeks you won't remember whether "fine" was a 3 or a 4.

---

**And Problem 5, which almost nobody spots — Thursday's `screen_minutes = 480`.**

480 minutes is 8 hours. Not impossible. Not a typo. Possibly completely real (a sick day at home). It's an **outlier**.

> **Outlier** — a value that is legal but very far from the others.

Never delete an outlier just because it's inconvenient. Thursday might be the most interesting row in your entire table — notice its mood is 2, the lowest in the week. **Investigate outliers, don't erase them.** Add a note: `Thu: home sick, watched films all day`.

---

Here's the cleaned table, done honestly:

| id | day | date | sleep_hours | mood_1to5 | screen_minutes | note |
|---|---|---|---|---|---|---|
| 1 | Mon | 2026-08-24 | 7.5 | 4 | 95 | |
| 2 | Tue | 2026-08-25 | 8 | 4 | 110 | |
| 3 | Wed | 2026-08-26 | *(blank)* | 3 | 120 | forgot to record sleep |
| 4 | Thu | 2026-08-27 | 6.5 | 2 | 480 | home sick, watched films |
| 5 | Fri | 2026-08-28 | *(blank)* | 5 | 200 | was 88 — impossible, original lost |
| 6 | Sat | 2026-08-29 | 9 | 5 | 210 | |
| 7 | Sun | 2026-08-30 | 9.5 | 3 | 180 | mood was "fine", mapped fine→3 |

7 rows instead of 8. Two visible blanks. Three notes. **This table is worth ten times the original**, because you can see exactly what you know and what you don't.

---

### 4️⃣ Data provenance: who collected it, from whom, with what permission

> **Provenance** — the origin story of a dataset: who collected it, from whom, when, how, and with whose permission.

**🍕 Analogy — the food label.**
You wouldn't eat something from an unlabelled tin. You want to know what's inside, who made it, when, and whether it's expired. A dataset with no provenance is that unlabelled tin — and people feed them to models every day.

**The five provenance questions.** Ask them about every dataset you ever meet:

| Question | Bad answer | Good answer |
|---|---|---|
| **Who collected it?** | "It was on the internet" | "I did, by hand, in a notebook" |
| **From whom?** | "People" | "Me, one person, age 11" |
| **When?** | "Recently" | "24–30 August 2026" |
| **How?** | "Somehow" | "Written down each night at bedtime, phone Settings > Screen Time for minutes" |
| **With what permission?** | *(silence)* | "It's my own data. My classmates' rows were collected with their spoken agreement, and I use initials only" |

**🔢 Tiny example — why provenance changes the answer.**

Two datasets, both 1,000 rows, both "how many hours teenagers sleep".

| | Dataset A | Dataset B |
|---|---|---|
| Collected from | Visitors to a sleep-problems clinic | Every student in 4 randomly chosen schools |
| Average sleep | 5.9 hours | 7.8 hours |

Both numbers are real. Both were measured correctly. But Dataset A only contains teenagers who *already had a sleep problem* — that's why they were at the clinic. Using it to answer "how much do teenagers sleep?" gives an answer that is wrong by almost two hours.

**Nothing about the numbers reveals this.** Only the provenance does. This is why every dataset needs a card.

**The permission part matters, and it's about people.**

If your data includes other people, three rules:

1. **Ask first.** "Can I record your bedtime for a school project?" Always.
2. **Use initials or codes**, not full names. `S3` instead of `Sanjay Rao`.
3. **Never record home addresses, phone numbers, or photos of faces without a parent's explicit yes.**

Module 9 goes deep on privacy. For now, the habit: *if a row is about a person, that person gets a say.*

---

### 5️⃣ Sample vs population: your 30 rows are not the whole world

> **Population** — every single thing you'd like your answer to be true about.
>
> **Sample** — the smaller set you actually managed to measure.

**🍕 Analogy — tasting the soup.**
You stir the pot, take one spoonful, and decide the whole pot needs salt. That works — *because you stirred*. If you take your spoonful off the top without stirring, you get only the oily layer, and your judgement about the whole pot is wrong.

A **stirred** spoonful is a good sample. An **unstirred** one is a biased sample. The spoon size doesn't matter nearly as much as the stirring.

**🔢 Tiny example — the class survey that lied.**

You want to know: *what's the favourite sport of students at my school?* (Population: all 800 students.)

You ask 30 students. Result:

| Sport | Votes | Percent |
|---|---|---|
| Cricket | 22 | 73% |
| Football | 5 | 17% |
| Badminton | 3 | 10% |

Confident conclusion: cricket wins, 73%.

Now the provenance: **you asked 30 people at cricket practice.**

Your sample wasn't stirred. You sampled the oily layer. The true school-wide answer might be cricket 40%, football 35%, badminton 25% — and your survey cannot detect its own error, because within your 30 rows everything is perfectly consistent.

**Three ways a sample goes wrong:**

| Problem | What happens | Real example |
|---|---|---|
| **Wrong place** | You only reach one kind of person | Surveying at cricket practice |
| **Self-selection** | Only people who care bother to answer | An online poll about school food — only the angry ones vote |
| **Too small** | Random luck dominates | Asking 3 people and reporting a percentage |

**The one-line fix you can always apply:** you usually cannot make your sample perfect, but you can always **write down who is in it and who is missing**. "This is 30 students from cricket practice; it under-represents students who don't play sport" turns a lie into an honest limited finding.

**Why this matters for AI specifically.** A model learns whatever its sample contains, then gets used on the whole population. A face-unlock model trained mostly on adult faces will be worse at children's faces — not because anyone was cruel, but because children were a thin layer of the sample. Module 9 will have you measure exactly this on your own model.

---

## 🔍 Worked Example

Let's take a messy pile of real-world stuff and turn it into a trustworthy table, showing every step and every number.

**The situation:** you want to record every meal you ate over 3 days, so you could later predict whether a meal will make you feel sleepy.

---

### Step 1 — Decide what one row is

This is the single most important decision, and beginners rush it.

Candidates:

- One row = one **day**? Then you can't tell which meal caused sleepiness.
- One row = one **food item**? Then "rice" and "dal" from the same lunch become two disconnected rows.
- One row = one **meal**. ✅

**Decision: one row = one meal I ate.** Write it at the top of the sheet. Now every row must be a meal — never a day, never a snack you didn't eat, never a shopping list.

---

### Step 2 — Decide the columns

For every column ask: *can I measure this the same way every single time?*

| Proposed column | Can I measure it consistently? | Keep? |
|---|---|---|
| `meal_id` | Yes — just count 1, 2, 3… | ✅ |
| `date` | Yes | ✅ |
| `meal_type` (breakfast/lunch/dinner) | Yes | ✅ |
| `main_food` | Yes, if I name the biggest item | ✅ |
| `size_1to3` (small/medium/large) | Yes, if I define it: 1 = less than usual, 2 = usual, 3 = more than usual | ✅ |
| `minutes_eating` | Yes, with a clock | ✅ |
| `sleepy_after_1to5` | Yes, rated 1 hour after | ✅ |
| `tastiness` | ❌ No — my scale drifts. A 4 on Monday isn't a 4 on Wednesday | ❌ drop |
| `healthiness` | ❌ No — I'd be guessing, and guessing differently each time | ❌ drop |

**Seven columns kept, two dropped.** Dropping columns you can't measure consistently is a *skill*, not a failure. An inconsistent column is worse than no column, because it looks like information.

---

### Step 3 — Collect the raw data (as scribbled in a notebook)

```
Mon: breakfast - 2 idlis, small, ate fast maybe 8 min. felt fine after, like 2
Mon: lunch was rice and dal, big plate, took ages 25 min, SO sleepy after, 5
Mon: dinner - roti + sabzi, normal, 15 min, 2
Tue: breakfast - dosa, normal, 10 min, 2
Tue: lunch - rice dal again, big, 22 min, sleepy 4
Tue: skipped dinner (out late)
Wed: breakfast - dosa, normal, 10 min, 2
Wed: lunch - sandwich at school, small, 12 min, 1
Wed: dinner - rice + curry, big, 20min, 3
```

---

### Step 4 — First draft table

| meal_id | date | meal_type | main_food | size_1to3 | minutes_eating | sleepy_after_1to5 |
|---|---|---|---|---|---|---|
| 1 | 2026-08-24 | breakfast | idli | 1 | 8 | 2 |
| 2 | 2026-08-24 | lunch | rice and dal | 3 | 25 | 5 |
| 3 | 2026-08-24 | dinner | roti and sabzi | 2 | 15 | 2 |
| 4 | 2026-08-25 | breakfast | dosa | 2 | 10 | 2 |
| 5 | 2026-08-25 | lunch | rice dal | 3 | 22 | 4 |
| 6 | 2026-08-26 | breakfast | dosa | 2 | 10 | 2 |
| 7 | 2026-08-26 | lunch | sandwich | 1 | 12 | 1 |
| 8 | 2026-08-26 | dinner | rice and curry | 3 | 20 | 3 |

8 rows. Now audit it hard.

---

### Step 5 — Run the four checks

**Check A — Missing values.**

Tuesday dinner does not appear. Is that a missing value?

**No.** A missing value is a meal that happened but wasn't recorded. Tuesday dinner *did not happen* — you were out. There is no row because there is no example.

⚠️ But this needs a note, because someone reading the table later will see 3 meals on Monday, 2 on Tuesday, 3 on Wednesday and wonder if you forgot. **Note: "Tue dinner: skipped, not eaten. Not a recording error."**

**This distinction — no data vs no event — trips up adults constantly.** Zero sales on Sunday because the shop was shut is not the same as forgetting to check Sunday's sales.

**Check B — Duplicates.**

Rows 4 and 6 look nearly identical: `dosa, 2, 10, 2`. Duplicate?

Check the `date` column: row 4 is 2026-08-25, row 6 is 2026-08-26. **Two different meals on two different days that happened to be the same.** Not a duplicate — keep both. This is exactly why the `date` and `meal_id` columns earn their place.

**Check C — Impossible values.**

Define the legal ranges:

| Column | Legal range | All rows inside? |
|---|---|---|
| `size_1to3` | 1–3 | ✅ values seen: 1,3,2,2,3,2,1,3 |
| `minutes_eating` | 1–120 | ✅ values seen: 8,25,15,10,22,10,12,20 |
| `sleepy_after_1to5` | 1–5 | ✅ values seen: 2,5,2,2,4,2,1,3 |

All clean.

**Check D — Inconsistent categories.**

Row 2 says `rice and dal`. Row 5 says `rice dal`. Row 8 says `rice and curry`.

To a human these are obviously related. **To a machine, `rice and dal` and `rice dal` are two completely different categories** — as different as `dosa` and `sandwich`. It has no idea they refer to the same food.

This is the single most common data error in the world, and the fix is a **controlled vocabulary**: decide the allowed values in advance and never deviate.

Allowed `main_food` values: `idli`, `dosa`, `rice_dal`, `rice_curry`, `roti_sabzi`, `sandwich`.

Rewrite rows 2, 5, and 8 to use them.

---

### Step 6 — The clean table

| meal_id | date | meal_type | main_food | size_1to3 | minutes_eating | sleepy_after_1to5 |
|---|---|---|---|---|---|---|
| 1 | 2026-08-24 | breakfast | idli | 1 | 8 | 2 |
| 2 | 2026-08-24 | lunch | rice_dal | 3 | 25 | 5 |
| 3 | 2026-08-24 | dinner | roti_sabzi | 2 | 15 | 2 |
| 4 | 2026-08-25 | breakfast | dosa | 2 | 10 | 2 |
| 5 | 2026-08-25 | lunch | rice_dal | 3 | 22 | 4 |
| 6 | 2026-08-26 | breakfast | dosa | 2 | 10 | 2 |
| 7 | 2026-08-26 | lunch | sandwich | 1 | 12 | 1 |
| 8 | 2026-08-26 | dinner | rice_curry | 3 | 20 | 3 |

---

### Step 7 — Now do the arithmetic

**Average sleepiness across all 8 meals:**

```
2 + 5 + 2 + 2 + 4 + 2 + 1 + 3  =  21
21 ÷ 8  =  2.625
```

**Average sleepiness by size:**

- Size 1 (rows 1, 7): `(2 + 1) ÷ 2 = 3 ÷ 2 = 1.5`
- Size 2 (rows 3, 4, 6): `(2 + 2 + 2) ÷ 3 = 6 ÷ 3 = 2.0`
- Size 3 (rows 2, 5, 8): `(5 + 4 + 3) ÷ 3 = 12 ÷ 3 = 4.0`

| Meal size | Rows | Average sleepiness |
|---|---|---|
| 1 (small) | 2 | 1.5 |
| 2 (usual) | 3 | 2.0 |
| 3 (large) | 3 | 4.0 |

A pattern jumps out: bigger meals go with more sleepiness. Small → 1.5, usual → 2.0, large → 4.0.

---

### Step 8 — Be honest about what this does NOT prove

Four warnings, all of which come straight from what you've learned:

1. **8 rows is a tiny sample.** Move one number and the pattern shifts.
2. **The population is "all my meals forever"; the sample is "3 days".** Three days in one week, one season, one routine.
3. **Size and food type are tangled.** Every size-3 meal was rice-based. Is it the *size* or the *rice*? This table cannot tell you — you'd need a big non-rice meal, and you don't have one.
4. **`sleepy_after` is my own rating**, made by the same person who wanted to see a pattern. That's not neutral.

**None of these mean the work is bad.** They mean the finding is *provisional*, which is what all real findings are. Writing them down is the difference between a data scientist and someone with a spreadsheet.

---

### Step 9 — Write the data card

> ### 📇 Data Card: My Meals & Sleepiness
>
> **What it is:** 8 meals I ate, with the food, how big it was, how long I took, and how sleepy I felt one hour later.
> **How much:** 8 rows, 7 columns, covering 24–26 August 2026 (3 days).
> **Who collected it:** Me, by hand, writing in a notebook right after each meal and rating sleepiness exactly 1 hour later using a phone timer.
> **Who it's about:** One person — me, age 11. Nobody else appears in this data, so there are no permission issues.
> **Known gaps and problems:** Tuesday dinner is absent because I skipped the meal, not because I forgot to record it. Every large meal in this sample was rice-based, so I cannot separate "big meal" from "rice meal". The sleepiness rating is my own opinion, and I already suspected big meals made me sleepy, which may have nudged my ratings.
> **What it should NOT be used for:** Predicting anyone else's sleepiness. Deciding what people should eat. Any claim about food and health.

Seven lines. That card is what makes the table trustworthy. Without it, someone could take these 8 rows and write a headline about rice.

---

## 💻 Hands-On

**No programming.** You'll use a spreadsheet — Google Sheets (free, browser), Excel, or LibreOffice Calc. All three work identically for everything below.

---

### Activity A — Build a table from a pile of stuff (25 min)

Go and physically collect **10 books** from around your home. Real books, on a real table.

**Step 1.** Open a new spreadsheet. In row 1, type these headers, one per cell across:

```
A1: book_id
B1: title_short
C1: pages
D1: has_pictures
E1: genre
F1: my_rating_1to5
```

**Step 2.** Before entering anything, write your rules in a second sheet (or on paper):

| Column | Type | Legal values | How I measure it |
|---|---|---|---|
| `book_id` | category | 1–10 | Just counting |
| `title_short` | text | any | First 3 words of the title |
| `pages` | number | 1–2000 | Last numbered page |
| `has_pictures` | category | `yes` / `no` | `yes` if more than 5 pages have a picture |
| `genre` | category | `story`, `factual`, `school`, `comic` | Pick the closest one |
| `my_rating_1to5` | number (ordered) | 1–5 | 1 = hated, 5 = loved |

**Do not skip this step.** Deciding `has_pictures` means "more than 5 pages have a picture" *before* you start is the whole difference between clean and messy data. Otherwise book 3 gets a `yes` for one picture and book 9 gets a `no` for two, and you'll never know.

**Step 3.** Fill in rows 2 through 11, one book per row.

**Step 4.** Now run the four checks. In cell `H1` type `CHECKS`, and use these formulas:

```
H2:  =COUNTBLANK(A2:F11)
H3:  =COUNTIF(C2:C11,">2000")
H4:  =COUNTIF(F2:F11,">5")
H5:  =COUNTA(UNIQUE(E2:E11))
H6:  =AVERAGE(C2:C11)
H7:  =AVERAGE(F2:F11)
```

Put labels next to them in column I so you remember what they mean:

| Cell | Formula | What it tells you | What you want |
|---|---|---|---|
| H2 | `COUNTBLANK` | How many empty boxes | `0` |
| H3 | `COUNTIF pages > 2000` | Impossible page counts | `0` |
| H4 | `COUNTIF rating > 5` | Out-of-range ratings | `0` |
| H5 | `COUNTA(UNIQUE(genre))` | How many distinct genres you typed | `4` or fewer — if it says 6, you typed `Story` and `story` |
| H6 | `AVERAGE(pages)` | Mean page count | A sensible number |
| H7 | `AVERAGE(rating)` | Mean rating | Between 1 and 5 |

> 💡 **If `UNIQUE` isn't available** (older Excel), use `=SUMPRODUCT((E2:E11<>"")/COUNTIF(E2:E11,E2:E11&""))` — it counts distinct values the long way and gives the same answer.

**Expected output** for a clean 10-book table:

```
H2:  0        ← no blanks
H3:  0        ← no impossible page counts
H4:  0        ← no bad ratings
H5:  4        ← exactly the 4 genres you allowed
H6:  187.4    ← (your number will differ)
H7:  3.7      ← (your number will differ)
```

**If H5 comes out as 5 or 6, you have a real bug.** Sort column E alphabetically and look: you'll find `comic` and `Comic`, or `story` and `story ` with a trailing space. **To a spreadsheet these are different values.** Fix them and re-check. This will happen to you, and finding it yourself is the point of the exercise.

---

### Activity B — Break a table on purpose, then detect the damage (15 min)

Duplicate your sheet (right-click the tab → Duplicate). Name the copy `broken`.

Now sabotage it — make exactly these four changes:

1. Delete the `pages` value for book 4 → creates a **missing value**
2. Copy row 7 and paste it as a new row 12 → creates a **duplicate**
3. Change book 2's `pages` to `99999` → creates an **impossible value**
4. Change book 5's `genre` from `story` to `Story` (capital S) → creates a **typo**

Update the check formulas to cover 11 rows (`A2:F12`, `C2:C12`, and so on) and record what happens:

| Sabotage | Which check catches it? | Value before | Value after |
|---|---|---|---|
| Missing pages | `COUNTBLANK` | 0 | 1 |
| Duplicate row | ❓ | | |
| pages = 99999 | `COUNTIF >2000` | 0 | 1 |
| `Story` vs `story` | `COUNTA(UNIQUE)` | 4 | 5 |
| — | `AVERAGE(pages)` | 187.4 | ~9200 |

**The big discovery:** three of your four sabotages are caught by a check. **The duplicate is not.** `COUNTBLANK` says 0, the range checks say 0, `UNIQUE` says 4. Every alarm is silent, and your data is wrong.

Add a duplicate detector. In `H8`:

```
=COUNTA(B2:B12) - COUNTA(UNIQUE(B2:B12))
```

This counts the titles, counts the *distinct* titles, and subtracts. `0` means no duplicates; `1` means one extra copy. Run it — you should get `1`.

**Now look at `AVERAGE(pages)`.** One typo took it from 187.4 to about 9,200. **A single bad cell out of 66 destroyed the answer.** That's the lesson: bad data doesn't degrade your results gently, it detonates them.

---

### Activity C — Write your first data card (10 min)

At the bottom of your sheet, or on paper, write a card for your 10-book table using exactly this template:

```
📇 DATA CARD

Name:            _______________________________________________
What it is:      _______________________________________________
How much:        ___ rows × ___ columns, collected on ___________
Who collected:   _______________________________________________
About whom:      _______________________________________________
How measured:    _______________________________________________
Known gaps:      _______________________________________________
Do NOT use for:  _______________________________________________
```

**Worked example:**

```
📇 DATA CARD

Name:            My Home Bookshelf, Sept 2026
What it is:      10 books physically on my shelves, with length, genre,
                 pictures, and my personal rating.
How much:        10 rows × 6 columns, collected 2 September 2026.
Who collected:   Me, by hand, holding each book.
About whom:      Books, not people. My rating column is about me.
How measured:    pages = the last numbered page. has_pictures = yes if
                 more than 5 pages have a picture. Rating is my opinion
                 today, 1 to 5.
Known gaps:      Only books currently in my house — library books and
                 books I lent out are missing. All 10 are books I chose
                 or was given, so easy books I rejected years ago aren't
                 here. Ratings for books I read long ago are from memory.
Do NOT use for:  Deciding what other people like. Claiming anything about
                 books in general. 10 books from one shelf is not a
                 library.
```

Notice that the last two lines are the ones with real value. Anybody can count books. Stating what your data *cannot* do is the professional part.

---

## ✍️ Practice

**[Warm-up] 1 — Name the row.**
For each of these five projects, write one sentence: *"One row = one ___."* Then name three columns you'd need.
(a) Predicting whether it will rain tomorrow. (b) Deciding if an email is spam. (c) Predicting a house's price. (d) Recognising handwritten digits. (e) Recommending a film.
*Done looks like:* 5 sentences of the form "One row = one ___", each with 3 named columns. Every column must be something you could actually measure.

**[Warm-up] 2 — Type the column.**
Label each column `number`, `category`, `text`, `image`, or `time`. Then answer: does averaging it make sense?

`shoe_size` · `favourite_colour` · `bus_route_number` · `temperature_celsius` · `tweet_body` · `date_of_birth` · `student_id` · `race_finish_seconds` · `passport_photo` · `mood_1to5`
*Done looks like:* 10 labels plus 10 yes/no answers on averaging, each with a short reason. At least two of the number-looking ones must be marked as categories.

**[Build] 3 — Clean the wreck.**
Here is a table of 8 dogs at a shelter. Find every problem, list it by row and column, and write your fix for each.

| id | name | age_years | weight_kg | breed | adopted |
|---|---|---|---|---|---|
| 1 | Bruno | 3 | 22 | labrador | yes |
| 2 | Coco | 2 | 8 | Beagle | no |
| 3 | Bruno | 3 | 22 | labrador | yes |
| 4 | Rex | 45 | 30 | german shepherd | no |
| 5 | Milo | 1 |  | beagle | yes |
| 6 | Zara | 4 | -5 | labrador | no |
| 7 | Simba | 2 | 15 | Labrador | maybe |
| 8 | Nala | 6 | 25 | german shepard | no |

*Done looks like:* at least 6 distinct problems found, each with row number, column name, problem type (missing / duplicate / impossible / typo / inconsistent), and a specific fix. Then state how many genuinely distinct breeds there are.

**[Build] 4 — Provenance detective.**
For each headline, write the **one provenance question** whose answer would most change whether you believe it, and explain in 2 sentences why.
(a) "Study finds 90% of teenagers prefer video to reading." (b) "New AI detects skin cancer better than doctors." (c) "Survey: 70% of parents support later school start times."
*Done looks like:* 3 questions and 3 explanations. Each question must be answerable with a fact (who, when, how many, from where) — not an opinion.

**[Stretch] 5 — Design a table for a hard thing.**
Design a table to answer: **"Does the weather affect how well I sleep?"**
Give: what one row is, at least 6 columns with type and legal range for each, how you'd measure each one, and **two columns you deliberately rejected** with reasons.
*Done looks like:* a full column specification table, a stated row definition, 2 rejected columns with reasons, and a 3-sentence note on which of your columns will be hardest to measure honestly and why.

**[Stretch] 6 — Sample surgery.**
Someone wants to know the average daily screen time of students at your school (800 students). They post an online poll in the school gaming club's group chat and get 40 replies. Average: 6.2 hours.
Write: (a) the population, (b) the sample, (c) three specific reasons this number is probably too high, (d) a better sampling plan that a real 11-year-old could actually carry out, and (e) one thing that would *still* be wrong with your better plan.
*Done looks like:* all five parts answered, with part (c) giving three genuinely different reasons and part (e) showing you know no sample is perfect.

---

## 🤔 Think Deeper

**1. Is it ever right to delete data you don't like?**
You track your mood for a month. One day you were furious about something unrelated and rated a 1. It drags your average down and doesn't feel representative. Delete it?
*How to reason about it:* separate two different justifications — "this measurement was taken wrongly" (a broken scale, a mis-click) versus "this measurement is correct but inconvenient". Only the first is ever a reason to delete. Then ask a harder question: if you allow yourself to delete inconvenient points, what happens to *every* conclusion you ever draw from your own data? Consider what a rule like "I'll write it down and mark it unusual" gives you that deletion doesn't.

**2. Who owns the data about you?**
Your school records your attendance, grades, and library loans. Your phone records where you went. Your watch records your heartbeat. Who owns each one — you, or the organisation that recorded it?
*How to reason about it:* ownership isn't one thing. Break it into four separate powers: who can *see* it, who can *change* it, who can *sell* it, and who can *delete* it. Work through each of the three examples against all four powers — you'll find the answer differs. Then ask what changes if the data is *about* you but was *created* by someone else's equipment.

**3. Can a dataset ever be neutral?**
Every table required someone to choose what counts as a row, which columns exist, and which don't. Those choices are made by people with opinions. Is "neutral data" even possible?
*How to reason about it:* pick a dataset that feels maximally boring — daily rainfall, say — and try to find the human choices inside it. Where were the gauges placed? Who decided which places get gauges? What's recorded on a day the gauge broke? If you find choices even there, you have your answer. Then think about the useful version of the question: not "is it neutral?" but "are its choices *written down* so I can judge them?"

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Filling a missing value with `0` | The box looks empty and 0 feels like nothing | `0` is a claim ("it was zero"); blank is honesty ("I don't know"). Leave it blank and add a note. Check every average afterwards |
| Averaging ID numbers, postcodes, or route numbers | They're printed as digits, so they look like numbers | Apply the addition test: does adding two of them mean anything? Route 7 + route 12 ≠ route 19. It's a category |
| Mixing row types in one table | You start with meals, then add a "weekly total" row at the bottom | A summary is a *different* kind of thing. Put totals in a separate sheet or cell, never as a row in the data |
| Inconsistent category spelling (`Labrador` / `labrador` / `lab`) | Typing freehand, over several days, from memory | Write the allowed values down before you start, and use a dropdown (Data → Data validation) so wrong values can't be typed |
| Deleting outliers because they spoil the chart | They look "wrong" and make the graph ugly | Legal-but-extreme ≠ impossible. Investigate and annotate. The outlier is often the most informative row you have |
| Treating "no event" as "missing data" | Both show up as an absent row | Zero sales because the shop was shut is a real measurement of 0. A day you forgot to check is blank. Write a note saying which |
| Collecting first, deciding what columns mean later | Collecting feels productive; defining feels like admin | Write the column spec (type, legal range, how measured) before row 1. Half an hour of spec saves a week of confusion |
| Reporting a percentage from a tiny sample | Percentages sound scientific | With 8 people, one person = 12.5%. Always report the raw count next to the percentage: "6 of 8 (75%)" |
| Forgetting your sample isn't the world | Your data is all you can see, so it feels like everything | Every data card must name who is *missing*, not just who is included |

---

## 🛠️ Mini-Project — Your Life In 30 Rows

**Time: ~3 hours total — about 10 minutes a day for a week, plus 90 minutes of building and writing.**

### 🎯 Goal

Track something real about yourself for a week, build a **30-row spreadsheet with at least 4 columns**, clean it honestly, and write a data card.

Thirty rows is small. It is also the first dataset you have ever *owned*, and you'll use it again — Module 3 will look for patterns in it.

---

### 📋 Starter steps

**Step 1 — Choose your unit (10 min). Decide what one row is.**

You need 30 rows from about 7 days, so one row per day won't do it. Pick one:

| Option | One row = | Rows per day | Total in 7 days |
|---|---|---|---|
| **A: Meals** | one meal | 3–5 | 21–35 ✅ |
| **B: Screen sessions** | one time you picked up your phone (over 5 min) | 4–8 | 28–56 ✅ |
| **C: Homework blocks** | one sitting of homework | 2–4 | 14–28 ⚠️ tight |
| **D: Hourly check-ins** | one waking hour, 4 fixed times a day | 4 | 28 ⚠️ tight |
| **E: Journeys** | one trip from A to B | 4–6 | 28–42 ✅ |

If you truly want one row per day, extend to 30 days — that's a fine project, just a longer one.

**Step 2 — Write your column spec BEFORE collecting anything (20 min).**

Minimum 4 columns beyond the ID. Fill in this spec table completely:

| Column name | Type | Legal range / allowed values | Exactly how I measure it |
|---|---|---|---|
| `row_id` | category | 1–30 | Counting |
| `date` | time | this week | Calendar |
| | | | |
| | | | |
| | | | |
| | | | |

**Rules for your columns:**

- At least **2 must be numbers** you can average (minutes, hours, count).
- At least **1 must be a category** with a written list of allowed values.
- At least **1 must be something about how you felt** (a 1–5 scale — define what 1 and 5 mean!).
- Every "how I measure it" must be so precise that a stranger could do it the same way. `"screen time"` fails. `"the number in Settings → Screen Time for that app, checked at 21:00"` passes.

**Step 3 — Collect for 7 days (10 min/day).**

- **Record at the moment, not at the end of the week.** Memory invents data.
- If you miss one, **leave it blank and write the reason**. Missing rows with honest notes are worth more than invented rows.
- Do not change your column definitions mid-week. If you must, start a note called `CHANGES` and record the day and what changed.

**Step 4 — Build the spreadsheet (20 min).**

Headers in row 1. Rows 2–31. Then add this check block off to the side:

```
Total rows:        =COUNTA(A2:A31)
Blank cells:       =COUNTBLANK(A2:F31)
Duplicate check:   =COUNTA(B2:B31)-COUNTA(UNIQUE(B2:B31))
Distinct categories: =COUNTA(UNIQUE(E2:E31))
Average of col C:  =AVERAGE(C2:C31)
Min of col C:      =MIN(C2:C31)
Max of col C:      =MAX(C2:C31)
```

`MIN` and `MAX` are your impossible-value detectors — if your `sleep_hours` max is 88, you'll see it instantly.

**Step 5 — Clean it, keeping a log (20 min).**

Make a `cleaning_log` sheet with columns: `row | column | problem | what I did`. Every single change goes in the log. If you change a value and don't log it, you have destroyed your own data's provenance.

**Step 6 — Write the data card (20 min).** Use the Activity C template. At least 5 lines, and your "Known gaps" line must be real.

**Step 7 — Find one thing (20 min).**

Compute one comparison from your data. Group by your category column and average one of your number columns — like the meal-size table in the Worked Example.

Then write three sentences: what you found, one reason it might not be true, and what extra data would settle it.

---

### ✅ Success criteria checklist

- [ ] 30 rows (or 28+ with a written explanation)
- [ ] At least 5 columns including `row_id` and `date`
- [ ] Every column header is typed, lowercase, with underscores instead of spaces (`sleep_hours`, not `Sleep Hours`)
- [ ] A completed column spec table written **before** collection
- [ ] At least 2 averageable number columns
- [ ] At least 1 category column with a written list of allowed values
- [ ] Every gap has a note explaining it — zero silent blanks
- [ ] `MIN` and `MAX` checked on every number column; no impossible values remain
- [ ] Duplicate check run and result recorded
- [ ] A cleaning log with one line per change made
- [ ] A data card of at least 5 lines, including a real "known gaps" line and a "do not use for" line
- [ ] One grouped comparison computed, with three sentences of honest interpretation

---

### 🚀 Level it up

**Add a second person.**

Ask one friend or family member to track the *same* columns, using your *exact* spec, for the same week. Then:

1. Put their rows in the same sheet with a new `person` column (`me` / `P2`). Use a code, not a name.
2. Compute your averages and theirs separately.
3. Compute the difference.

Now the real question: **do the differences mean anything?**

You'll notice something uncomfortable. Even with the identical spec, you two measured differently — your "mood 3" is not their "mood 3", and you might have checked screen time at 21:00 while they checked at bedtime. This is called **measurement inconsistency**, and it's one of the hardest problems in all of data collection. Professional researchers spend enormous effort on it.

Write a paragraph on the biggest inconsistency you found and how you'd fix it if you ran the study again with 100 people.

⚠️ **Permission first.** Ask before you collect, use a code instead of their name, and show them the sheet when you're done. Their data, their say.

---

## 🔑 Key Takeaways

- **Data is recorded observations.** Nothing in your head is data until it's written down in a countable form.
- **The table is the universal shape: one row per example, one column per attribute** — and every row must be the same kind of thing.
- **Data types decide what's legal.** Numbers can be averaged; categories cannot, even when they're written with digits. Apply the addition test.
- **Real data is messy in five specific ways:** missing values, duplicates, impossible values, typos and inconsistent categories, and outliers. Each has its own fix, and `0` is never the fix for missing.
- **Provenance is part of the data.** Who collected it, from whom, when, how, and with what permission changes what the numbers mean — and nothing in the numbers reveals it.
- **Your sample is not the population.** You usually can't fix that, but you can always write down who is missing.
- **A data card turns a spreadsheet into something trustworthy** — especially the line saying what it should *not* be used for.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Data** | Observations written down so a machine can read them | `2026-09-02, rain, 18°C` |
| **Table** | Data arranged in rows and columns | A class register |
| **Row** | One example — one single thing you observed | One student, one meal, one photo |
| **Column** | One attribute measured for every example | `age_years`, measured for all 30 students |
| **Header** | The top row that names each column | The first row reading `name`, `age`, `class`, `present` |
| **Data type** | What kind of value a column holds, which decides what you can do with it | `sleep_hours` is a number; `favourite_colour` is a category |
| **Number** | A value you can meaningfully add and average | 7.5 hours of sleep |
| **Category** | A value that names a group; adding them is meaningless | `beagle`, `6A`, postcode 560001 |
| **Missing value** | An empty box where a measurement should be | Forgot to record Wednesday's sleep |
| **Duplicate** | The same example recorded more than once | Saturday listed twice with identical values |
| **Impossible value** | A value reality doesn't allow | `sleep_hours = 88`; `weight_kg = -5` |
| **Outlier** | A legal value that sits far from all the others | 480 screen-minutes in a week of ~150s |
| **Controlled vocabulary** | The written list of allowed values for a category column | `main_food` may only be one of six listed foods |
| **Provenance** | The origin story: who collected it, from whom, when, how, with what permission | "Me, by hand, 24–30 Aug 2026, in a notebook" |
| **Population** | Everything you want your answer to be true about | All 800 students in the school |
| **Sample** | The smaller set you actually measured | The 30 students you asked |
| **Data card** | A short honest note describing a dataset and its limits | The seven-line card in the Worked Example |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Name the row

**(a) Predicting whether it will rain tomorrow**
> One row = one **day** at one **place**.

Columns: `date`, `temperature_c_at_noon`, `humidity_percent`, `pressure_hpa`, `rained_tomorrow` (the answer).

⚠️ Notice the row must be a day *at a place*. "One row = one day" alone breaks if you record Mumbai and Delhi on the same date — you'd have two rows for one day, which violates the rule that rows are unique examples. Add a `city` column and the pair `(date, city)` identifies the row.

**(b) Deciding if an email is spam**
> One row = one **email**.

Columns: `sender_domain`, `subject_word_count`, `number_of_links`, `has_attachment`, `is_spam` (the answer).

**(c) Predicting a house's price**
> One row = one **house that was sold**.

Columns: `area_sqft`, `bedrooms`, `age_years`, `distance_to_station_km`, `sale_price` (the answer).

⚠️ "One row = one house" is slightly wrong — a house sold three times in ten years is three examples, at three prices. One row = one *sale*.

**(d) Recognising handwritten digits**
> One row = one **image of a single digit**.

Columns: at Level 1, `image_file` and `true_digit` (the answer). Module 7 will reveal that `image_file` is really hundreds of number columns in disguise — a 28×28 image is 784 brightness values, so the real table has 785 columns.

**(e) Recommending a film**
> One row = one **rating**: one person rating one film.

Columns: `user_id`, `film_id`, `rating_1to5`, `date_rated`, `minutes_watched`.

⚠️ The tempting wrong answers are "one row = one film" or "one row = one person". Neither works, because the thing you're predicting connects *a person to a film*. The row has to be the pair.

**The pattern across all five:** the row is whatever the thing you're predicting is *about*. Find the prediction first, then the row.

---

### Exercise 2 — Type the column

| Column | Type | Average it? | Reason |
|---|---|---|---|
| `shoe_size` | number (ordered) | ⚠️ Sort of | Sizes are ordered and evenly spaced, so "average size 7.4" is usable. But UK/US/EU scales differ, so mixing systems ruins it |
| `favourite_colour` | category | ❌ No | `red + blue` is not a colour. No order either — blue isn't "more" than green |
| `bus_route_number` | **category** | ❌ No | Route 7 + route 12 ≠ route 19. It's a name printed with digits |
| `temperature_celsius` | number | ✅ Yes | Real measurement, real scale, evenly spaced. Average temperature is meaningful |
| `tweet_body` | text | ❌ No | You can't average sentences. You *can* count characters — but that's a new number column you'd create |
| `date_of_birth` | time | ⚠️ Technically | The average of two birthdays is a real date, which can be useful ("average birth year 2014"). Usually you'd convert to `age_years` first |
| `student_id` | **category** | ❌ No | The classic trap. ID 1001 + ID 1002 means nothing. It's a label made of digits |
| `race_finish_seconds` | number | ✅ Yes | Real measurement on a real scale. Averaging gives a meaningful team time |
| `passport_photo` | image | ❌ No | It's a picture. You can measure things *about* it (brightness, size) — those are new columns |
| `mood_1to5` | category (ordered) | ⚠️ Commonly done | 5 is genuinely happier than 4, so you can sort and take the middle. Averaging is standard practice but slightly fake, because the gap 1→2 may not equal 4→5 |

**The two number-looking categories:** `bus_route_number` and `student_id`. If you also flagged `shoe_size`, that's a defensible third — sizes aren't a physical measurement, they're a manufacturing scale.

**The addition test, applied:**

```
shoe 6 + shoe 8       → "size 14"?  Nonsense as a shoe. But the average, 7, is a real size. ⚠️
route 7 + route 12    → "route 19"? Different bus entirely.                                ❌
18°C + 22°C           → 40°C total is odd, but the average 20°C is perfectly real.          ✅
ID 1001 + ID 1002     → "student 2003"? A different person, or nobody.                      ❌
11.4s + 12.9s         → 24.3s is a real relay time. The average 12.15s is real too.         ✅
```

---

### Exercise 3 — Clean the wreck

**Problems found — nine of them:**

| # | Row | Column | Type | Problem | Fix |
|---|---|---|---|---|---|
| 1 | 3 | all | **Duplicate** | Row 3 is identical to row 1 in every column except `id` | Delete row 3. Bruno was counted twice |
| 2 | 4 | `age_years` | **Impossible** | 45 years — the oldest dog ever recorded was 29 | Blank it, note "was 45, impossible". Possibly a typo for 4 or 5, but guessing is inventing data |
| 3 | 5 | `weight_kg` | **Missing** | Blank | Leave blank, note "not weighed". Do **not** put 0 — a 0 kg dog would wreck the average |
| 4 | 6 | `weight_kg` | **Impossible** | −5 kg — negative mass doesn't exist | Blank it, note "was −5, impossible" |
| 5 | 7 | `adopted` | **Wrong value** | `maybe` in a yes/no column | Either add `pending` to the allowed values (and write it down) or blank it. Don't silently pick yes or no |
| 6 | 2, 5 | `breed` | **Inconsistent case** | `Beagle` vs `beagle` | Standardise to lowercase `beagle` |
| 7 | 1, 3, 6, 7 | `breed` | **Inconsistent case** | `labrador` vs `Labrador` | Standardise to lowercase `labrador` |
| 8 | 8 | `breed` | **Typo** | `german shepard` — misspelling of `shepherd` | Correct to `german_shepherd` |
| 9 | 4, 8 | `breed` | **Formatting** | Spaces inside a category value cause errors in many tools | Use `german_shepherd` with an underscore |

**How many genuinely distinct breeds?**

Raw distinct values in the column: `labrador`, `Beagle`, `beagle`, `german shepherd`, `Labrador`, `german shepard` = **6 apparent breeds**.

After cleaning: `labrador`, `beagle`, `german_shepherd` = **3 real breeds**.

**This is the headline result.** Before cleaning, a machine would treat this as 6 breed categories with 1–2 dogs each — far too thin to learn anything. After cleaning, it's 3 breeds with a real spread. **Cleaning didn't just tidy the table; it doubled the usable information.**

**The cleaned table:**

| id | name | age_years | weight_kg | breed | adopted | note |
|---|---|---|---|---|---|---|
| 1 | Bruno | 3 | 22 | labrador | yes | |
| 2 | Coco | 2 | 8 | beagle | no | |
| 4 | Rex | | 30 | german_shepherd | no | age was 45, impossible |
| 5 | Milo | 1 | | beagle | yes | never weighed |
| 6 | Zara | 4 | | labrador | no | weight was −5, impossible |
| 7 | Simba | 2 | 15 | labrador | pending | was "maybe"; added `pending` to allowed values |
| 8 | Nala | 6 | 25 | german_shepherd | no | breed spelling corrected |

7 rows. Three blanks, all noted. Every change logged.

**Bonus — the average weight, before and after:**

Before (treating blank as skipped, keeping −5): `(22+8+22+30-5+15+25) ÷ 7 = 117 ÷ 7 = 16.71 kg`
After: `(22+8+30+15+25) ÷ 5 = 100 ÷ 5 = 20.0 kg`

**A 3.3 kg difference** — over 16% — caused entirely by one duplicate and one negative number.

---

### Exercise 4 — Provenance detective

**(a) "Study finds 90% of teenagers prefer video to reading."**

> **The question: Where were these teenagers found, and how were they recruited?**

If they were recruited through a video app's own newsletter, the study has answered "do people who use a video app prefer video?" — which was never in doubt. Ninety percent is a big, clean number, and big clean numbers usually mean the sample was pre-filtered rather than that the world is genuinely that lopsided.

**(b) "New AI detects skin cancer better than doctors."**

> **The question: Whose skin was in the training and test data?**

Most public skin-image datasets are dominated by light skin, so a model can score brilliantly overall and be much worse on darker skin — and the single headline number hides that completely. This one is not hypothetical: it is a documented, repeated finding in real medical AI, and it is exactly what Module 9 will have you test on your own model.

**(c) "Survey: 70% of parents support later school start times."**

> **The question: How were the parents contacted, and what fraction of those contacted replied?**

If it was an optional online form, the parents who felt strongly are enormously more likely to have filled it in, so 70% may measure intensity of feeling rather than breadth of opinion. The reply rate is the tell: 70% of a 5% reply rate is roughly 3.5% of all parents, which is a very different sentence from the headline.

**What makes each of these a good question:** all three are answerable with a fact you could look up in the study's methods section, and in all three cases the answer could plausibly flip your conclusion. "Is the study any good?" is not a provenance question — it's a request for someone else's opinion.

---

### Exercise 5 — Design a table for a hard thing

**Question: Does the weather affect how well I sleep?**

**One row = one night's sleep.** (Not one day — a night spans two dates, so I'll label each row by the *morning* I woke up and say so explicitly, because otherwise "Tuesday's sleep" is ambiguous.)

**Column spec:**

| Column | Type | Legal range | How I measure it |
|---|---|---|---|
| `night_id` | category | 1–30 | Counting |
| `wake_date` | time | the 30 dates | The date of the morning I woke up |
| `bedtime` | time | 19:00–02:00 | Clock time lights went off, checked on my phone |
| `wake_time` | time | 04:00–12:00 | Clock time I got out of bed |
| `sleep_hours` | number | 0–14 | `wake_time − bedtime`, computed by the spreadsheet, not estimated |
| `night_temp_c` | number | −10 to 45 | Weather app's overnight low for my city, checked the next morning |
| `rained_overnight` | category | `yes` / `no` | Weather app's overnight precipitation greater than 0 mm |
| `humidity_percent` | number | 0–100 | Weather app's overnight average |
| `sleep_quality_1to5` | category (ordered) | 1–5 | Rated within 10 minutes of waking. **1 = woke up several times and feel exhausted. 5 = slept straight through and feel fully rested.** |
| `woke_up_count` | number | 0–10 | How many times I remember waking, recorded in the morning |

**Two columns I deliberately rejected:**

1. **`dreams` (text).** I can't measure it consistently — some mornings I remember dreams vividly, most mornings I remember nothing, and "nothing remembered" is not the same as "no dreams". The column would mostly record my memory, not my sleep, and I'd have no way to tell those apart.

2. **`room_temperature_c`.** This one hurts, because it's probably *more* relevant than the outdoor temperature — it's the air I'm actually sleeping in. I rejected it because I don't own a thermometer, and estimating it by feel would give me a made-up number that *looks* as trustworthy as the real weather-app numbers next to it. **A fake number in a column of real numbers is worse than an empty column**, because nothing on the sheet marks it as fake. If I could borrow a thermometer, this becomes my best column and I'd add it immediately.

**Which column is hardest to measure honestly, and why:**

`sleep_quality_1to5`, by a long way. I'm rating it myself, minutes after waking, when I'm barely conscious — and my scale will drift over 30 days without me noticing. Worse, I already believe hot nights ruin my sleep, so on a hot morning I may unconsciously rate a 2 where I'd have said 3 in cool weather. That would manufacture the exact pattern I'm looking for, out of nothing. The partial defence is `woke_up_count`: it's a count of events rather than a feeling, so it drifts less, and if `sleep_quality` and `woke_up_count` disagree I'll know my ratings are unreliable.

---

### Exercise 6 — Sample surgery

**(a) The population**
All 800 students at the school. That's the group the claim is meant to describe.

**(b) The sample**
40 students who (i) are in the gaming club, (ii) read that group chat, and (iii) chose to reply. That's three filters stacked on top of each other, and the poll only reports the survivors of all three.

**(c) Three specific reasons 6.2 hours is probably too high**

1. **Wrong place.** The gaming club selects for students who spend time on screens by definition. Sampling gamers to measure screen time is like sampling a cricket practice to measure interest in cricket.
2. **Self-selection within the sample.** Even inside the club, the 40 who replied are the ones who saw the message and wanted to answer. Someone with 45 minutes of screen time has little reason to respond to a screen-time poll; someone with 9 hours might find it funny to. This filter operates *after* the club filter and pushes the same direction.
3. **Self-reporting with no definition and no verification.** Nobody defined whether "screen time" includes school laptops, TV, or a phone playing music in your pocket. Different students counted different things, and some inflated it for laughs. There is no measurement here at all — only 40 opinions about a number.

*(A fourth, if you want it: 40 out of 800 is 5% of the school, so one respondent equals 2.5 percentage points. The number is noisy as well as biased.)*

**(d) A better plan an 11-year-old could actually do**

> **The register method.** Ask a teacher for permission to survey **two whole class registers** — say one Year 7 class and one Year 9 class, about 60 students. Hand out a paper slip in class and ask everyone present to fill it in and put it face-down in a box. Include the definition on the slip: *"Screen time = the total minutes shown in your phone's Settings → Screen Time / Digital Wellbeing for yesterday. Copy the number. If you don't have a phone, write NONE."*

Why each piece helps:

| Change | Fixes which problem |
|---|---|
| Whole classes, not a club | Removes the gaming-club filter — you get students who hate screens too |
| Everyone present fills it in | Removes self-selection almost entirely |
| Anonymous, face-down in a box | Reduces exaggerating and reduces embarrassment |
| Copy a number from the phone | Turns an opinion into a measurement |
| An explicit `NONE` option | Stops students without phones from silently vanishing from the data |
| Two different year groups | Lets you check whether the answer even is one answer |

**(e) One thing that would still be wrong**

**It only covers phones, and only students who were in class that day.**

Screen time on a family TV, a shared computer, a school laptop, or a sibling's tablet is invisible to my method — so I'm not measuring screen time, I'm measuring *phone* screen time, and I should say so in the title. And students absent that day are missing entirely; if they were absent because they were ill at home, they may well be exactly the highest-screen-time students in the school.

**That's the honest ending.** My plan is far better than the group chat, and it is still not the truth. The right move isn't to keep hunting for a perfect sample — it's to write both limits into the data card and let the reader judge.

---

</details>

---

[⬅ Previous](module-01-what-ai-is-and-isnt.md) · [Level 1 Home](README.md) · [Next ➡](module-03-patterns-and-rules.md)

*Next up: you have data. Now you'll go hunting for the **patterns** inside it, write those patterns as if-then rules — and watch your rulebook collapse the moment it meets a message it has never seen. That collapse is the reason machine learning exists.*
