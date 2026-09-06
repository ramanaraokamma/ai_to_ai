# Module 3 — Patterns and Rules: When Writing Rules Stops Working

**Level 1 · Module 3 · ~2.5 hours · Prereqs: Module 1 (rule-based vs learned systems), Module 2 (rows, columns, and data types)**

[⬅ Previous](module-02-data-is-everywhere.md) · [Level 1 Home](README.md) · [Next ➡](module-04-features-and-labels.md)

---

## 🎯 What You'll Be Able To Do

By the end of this module:

1. **You will be able to** find a pattern in a small table and state it as a precise if-then rule.
2. **You will be able to** build a rulebook of 5 or more rules and apply it consistently to examples you've never seen.
3. **You will be able to** count how many rules a task needs as the cases pile up, and explain **rule explosion** with real numbers.
4. **You will be able to** explain in one paragraph why learning a rule from examples beats writing rules by hand for certain jobs.
5. **You will be able to** recognise the exact moment a rulebook stops being fixable — and say what to do instead.

---

## 🪝 The Hook

In the 1980s, some of the smartest programmers alive tried to build a machine that could read handwriting. Their plan was reasonable: write rules. A `7` is two lines meeting at the top. A `1` is one vertical stroke. An `8` is two stacked loops.

They wrote rules. Then exceptions to the rules. Then exceptions to the exceptions. Some systems ended up with **thousands** of hand-written rules, and they still failed on ordinary post — because a European `7` has a bar through it, a doctor's `1` has a serif that makes it a `7`, and a child's `8` is two circles that don't quite touch.

Then in 1989 a researcher tried something that felt like cheating. He wrote **no rules about digits at all**. He collected thousands of handwritten digits with the correct answer written next to each, and let a program find the pattern itself.

It beat the thousand-rule systems. Within a few years it was reading most of the cheques in the United States.

The rule-writers weren't stupid. They hit a wall that is built into the universe. In this module you're going to walk straight into that same wall yourself — deliberately — because feeling it is the only way to understand why machine learning had to be invented.

---

## 🧠 The Concept

Five ideas, each with a plain explanation, an everyday anchor, and a small example with real numbers.

---

### 1️⃣ A pattern is something that repeats often enough to bet on

You're at a bus stop. Over four weeks you notice the 9:05 bus arrives late almost every Monday and is on time most other days.

Have you found a pattern? Let's be precise about what "pattern" means.

> **Pattern** — something that repeats often enough that betting on it beats guessing.

That definition has a hidden bar in it: **beats guessing.** A pattern that's right 50% of the time on a two-way choice is not a pattern. It's a coin.

**🍕 Analogy — the biscuit tin.**
Your grandmother keeps biscuits in the blue tin. Not always — sometimes they're in the cupboard, sometimes there are none. But if you had to bet, you'd check the blue tin first, and you'd be right most of the time. That's a pattern: not a guarantee, just a bet worth making.

Almost nothing in the real world is a guarantee. Patterns are how you act sensibly anyway.

**🔢 Tiny example — is the Monday bus thing real?**

Twenty days of data:

| Day | Times observed | Times late | Late rate |
|---|---|---|---|
| Monday | 4 | 4 | 100% |
| Tuesday | 4 | 1 | 25% |
| Wednesday | 4 | 0 | 0% |
| Thursday | 4 | 1 | 25% |
| Friday | 4 | 2 | 50% |

Overall late rate: `(4 + 1 + 0 + 1 + 2) ÷ 20 = 8 ÷ 20 = 40%`

Now compare:

- **Guess "late" for every day:** right 8 times out of 20 = **40%**
- **Guess "on time" for every day:** right 12 out of 20 = **60%**
- **Use the Monday pattern** — say "late" on Monday, "on time" otherwise: right on all 4 Mondays, plus 3+4+3+2 = 12 of the other 16. Total 16 out of 20 = **80%**

**80% beats 60%.** The pattern earns its keep by 20 percentage points. That's a real pattern.

⚠️ **But be careful.** Four Mondays is four observations. If the roadworks that caused it finish next week, your pattern evaporates. **A pattern is a bet about the future based on the past, and the past can stop being a good guide at any moment.** Module 2's warning about small samples applies here with full force.

---

### 2️⃣ If-then rules: how humans normally program a computer

Once you've spotted a pattern, you turn it into an instruction a machine can follow.

> **If-then rule** — an instruction of the form: *IF this condition is true, THEN do that.*

The Monday pattern becomes:

```
IF day_of_week = "Monday"  THEN predict "late"
ELSE                        predict "on time"
```

**🍕 Analogy — the recipe card.**
A recipe doesn't say "cook it nicely". It says "IF the water is boiling, THEN add the pasta." Every step has a condition and an action, in order. A machine needs exactly that: no vagueness, no judgement calls left to the reader.

**What makes a rule good enough for a machine:**

| Requirement | ❌ Bad rule | ✅ Good rule |
|---|---|---|
| **Testable** — the machine can actually check it | `IF the message feels dodgy` | `IF the message contains the word "prize"` |
| **Unambiguous** — one clear answer, every time | `IF the message is long` | `IF the message has more than 100 characters` |
| **Uses available data** — the input actually contains it | `IF the sender is a scammer` | `IF the sender is not in my contacts` |

The middle row is the one people get wrong most. "Long" is not a condition — it's an opinion. "More than 100 characters" is a condition, because the machine can count characters and always gets the same answer.

**🔢 Tiny example — the same rule, three sharpnesses:**

| Version | Rule | Can a machine run it? |
|---|---|---|
| v1 | `IF the message is shouty THEN spam` | ❌ No. "Shouty" isn't measurable |
| v2 | `IF the message has lots of capitals THEN spam` | ❌ No. "Lots" isn't a number |
| v3 | `IF more than 50% of the letters are capitals THEN spam` | ✅ Yes |

Test v3 on `"WIN NOW"`: 6 letters, all capital. 6 ÷ 6 = 100%. 100% > 50%, so → **spam**. ✅

Test v3 on `"OK see you at 5"`: letters are `O K s e e y o u a t` = 10 letters, 2 capital. 2 ÷ 10 = 20%. 20% is not > 50%, so → **not spam**. ✅

The rule works, and it works because every word in it is countable.

**Rule order matters.** When multiple rules could fire, you need to know which wins. The standard convention — and the one you'll use all module — is **first match wins**: check rules top to bottom, and the first one that fires decides the answer. Change the order, change the answers.

---

### 3️⃣ Edge cases: the examples your rule gets wrong

Every rule is a generalisation, and every generalisation has victims.

> **Edge case** — an example that your rule handles wrongly, usually because it sits at the boundary of what you were imagining.

**🍕 Analogy — the height sign at the theme park.**
`IF height ≥ 140cm THEN allowed on the ride.` Clean, testable, fair-looking. Now meet the edge cases:

- A 138cm 14-year-old — turned away, though she's plenty strong enough.
- A 141cm 6-year-old who's terrified — allowed on, though she shouldn't be.
- Someone with thick-soled shoes — 139cm barefoot, 142cm in trainers.

The rule isn't broken. Height genuinely does correlate with safety. But height is a **stand-in** for what actually matters (can this person be held safely by the harness?), and stand-ins always fail at the edges.

**Every if-then rule you will ever write uses a stand-in.** That's why edge cases are guaranteed, not unlucky.

**🔢 Tiny example — the capitals rule meets reality.**

Rule: `IF more than 50% of letters are capitals THEN spam`

| Message | Letters | Capitals | Percent | Rule says | Truth | Correct? |
|---|---|---|---|---|---|---|
| `"WIN A FREE PHONE"` | 13 | 13 | 100% | spam | spam | ✅ |
| `"hey are you free"` | 13 | 0 | 0% | not spam | not spam | ✅ |
| `"OMG I PASSED!!!"` | 10 | 10 | 100% | spam | **not spam** | ❌ |
| `"claim your prize now"` | 17 | 0 | 0% | not spam | **spam** | ❌ |

Let's verify one of those counts. `"OMG I PASSED!!!"` — the letters are `O M G I P A S S E D` = 10... let me recount including all alphabetic characters: `O, M, G, I, P, A, S, S, E, D` = 10 letters, all capital. 10 ÷ 10 = 100%. The rule fires. It says spam. It's your best friend celebrating an exam. **Wrong.**

2 correct out of 4 = **50%**. On a two-way choice, that is exactly as good as flipping a coin. The rule that looked brilliant on the first two examples is worthless on the second two.

**Two kinds of wrong, and they are not the same:**

> **False alarm** — the rule says spam, but the message is fine. (You lose your friend's good news.)
>
> **Miss** — the rule says fine, but the message is spam. (Scam lands in your inbox.)

Which is worse depends entirely on the job:

| Job | False alarm costs | Miss costs | Which is worse |
|---|---|---|---|
| Spam filter | You lose a real message | You see one scam | **False alarm** — you can delete a scam, you can't recover a deleted message you never saw |
| Smoke detector | It shrieks while you make toast | The house burns down | **Miss**, obviously |
| Exam cheating detector | An innocent student is accused | A cheat gets away with it | **False alarm**, by a mile |

**You cannot make both go to zero.** Tighten the rule to stop false alarms and you cause more misses. Loosen it to stop misses and you cause more false alarms. This trade-off never goes away — not with better rules, not with machine learning, not ever. All you can do is choose which mistake you'd rather make.

---

### 4️⃣ Rule explosion: why "just add another rule" stops working

Every edge case has an obvious fix: add a rule. And that works — for about five rules. Then something ugly happens.

> **Rule explosion** — the number of rules you need grows far faster than the number of cases you're trying to handle, until the rulebook becomes impossible for a human to maintain.

**🍕 Analogy — the family pizza order.**
One person: one rule. "Dad gets pepperoni."

Now add Mum (vegetarian), your sister (no cheese), and your cousin (allergic to nuts). Four people, four rules? No — because they share pizzas. Now you need rules for *combinations*: what if Mum and your sister share? What if the nut-free base isn't available in the size that fits four? What if your cousin is only there on Saturdays?

Four people generated far more than four rules. That's the explosion.

**🔢 Tiny example — count it exactly.**

Suppose your spam rules can look at just 3 things, each yes/no:

- Does it contain "FREE"?
- Does it have a link?
- Is the sender in my contacts?

How many distinct situations exist? Each thing has 2 options, and they combine:

```
2 × 2 × 2 = 8 situations
```

Here they all are:

| # | FREE? | Link? | Known sender? |
|---|---|---|---|
| 1 | no | no | no |
| 2 | no | no | yes |
| 3 | no | yes | no |
| 4 | no | yes | yes |
| 5 | yes | no | no |
| 6 | yes | no | yes |
| 7 | yes | yes | no |
| 8 | yes | yes | yes |

Eight rules covers *everything*. Completely manageable.

Now add just a few more things to check:

| Things checked | Situations = 2 to that power | Calculation |
|---|---|---|
| 3 | **8** | 2×2×2 |
| 5 | **32** | 2×2×2×2×2 |
| 10 | **1,024** | 2¹⁰ |
| 15 | **32,768** | 2¹⁵ |
| 20 | **1,048,576** | 2²⁰ |
| 30 | **1,073,741,824** | 2³⁰ |

**Read that table again.** You went from 3 things to 30 things — you multiplied the *questions* by ten — and the *situations* went from 8 to over a **billion**.

```
   situations
       │
   1B  │                                              ●
       │
       │
 100M  │
       │
       │
  10M  │
       │                                     ●
   1M  │
       │                            ●
 100k  │
  10k  │                   ●
   1k  │          ●
   100 │
    10 │ ●   ●
     0 └────┴────┴────┴────┴────┴────┴────┴────┴────► things checked
       3    5   10   15   20   25   30

   Each new thing you check DOUBLES the number of situations.
   Doubling thirty times is a billion.
```

This shape has a name: **exponential growth**. It's what happens when a quantity doubles each step, and it defeats human effort every single time.

**Put it in hours.** Suppose you're fast — one carefully-considered rule every 2 minutes, working 8 hours a day with no breaks. That's 240 rules a day.

| Rules needed | Days of solid 8-hour work | In plain terms |
|---|---|---|
| 8 | 0.03 days | 16 minutes ☕ |
| 32 | 0.13 days | A lunch break |
| 1,024 | 4.3 days | A hard week |
| 32,768 | 137 days | **Over 6 months**, working every school day |
| 1,048,576 | 4,369 days | **Almost 12 years** |
| 1,073,741,824 | 4,473,924 days | **Over 12,000 years** |

And a real spam filter looks at far more than 30 things. It looks at every word — tens of thousands of them.

**Three ways rule explosion actually kills you** (the count is only the first):

1. **You cannot write them all.** See the table.
2. **They start contradicting each other.** Rule 12 says spam, rule 40 says not spam, and now you need rules about which rule wins — a whole second rulebook on top of the first.
3. **The world changes underneath you.** Scammers read your rules by testing them. You block "FREE", they write "FR33". You block "FR33", they write "F R E E". Every rule you write has a shelf life, and by the time you've written 32,768 of them the first 10,000 are obsolete.

Point 3 is the killer. **A rulebook is frozen the moment you finish it, and the world isn't.**

---

### 5️⃣ The machine learning trade: give up writing rules, give the machine labelled examples

Here's the deal on the table:

> **The machine learning trade** — you stop writing the rules, and instead collect examples with the correct answers attached. The machine finds the rule.

Both sides give something up. Look at it honestly:

| | Writing rules yourself | The machine learning trade |
|---|---|---|
| **You provide** | The rules | **Labelled examples** |
| **Effort** | Grows with the number of cases (exponentially) | Grows with the number of examples (linearly — collecting example 5,000 costs the same as example 5) |
| **Can you explain a decision?** | ✅ Yes — point at the rule | ❌ Usually not |
| **What happens when the world changes?** | You rewrite by hand | Add new examples, retrain |
| **How many "things checked"?** | ~10 max, before you drown | Thousands, easily |
| **Do you need lots of data?** | ❌ No | ✅ Yes — this is the price |
| **Will it be perfect?** | ❌ No | ❌ No |
| **Is it predictable?** | ✅ Completely | ❌ It can surprise you |

> **Labelled example** — one piece of data with the correct answer written next to it.

**🍕 Analogy — teaching someone to spot a ripe watermelon.**

Option A: write instructions. "Knock it — if it sounds hollow, it's ripe. Check the yellow patch. Check the stem." You'll write ten instructions and the person will still pick badly, because the real skill lives in combinations you can't put into words.

Option B: walk them through a market and say "ripe… not ripe… ripe… not ripe" over sixty watermelons. Say nothing else. They will get good at it, and they still won't be able to explain how.

**Option B is machine learning.** Notice what you gave up: you can no longer point at the reason. And notice what you gained: it works on watermelons nobody described to you.

**🔢 Tiny example — the same job, both ways.**

Task: label a message spam or not.

**Rule way** — a human stares at examples, thinks hard, and writes:

```
RULE 1: IF contains "FREE"          THEN spam
RULE 2: IF contains "prize"         THEN spam
RULE 3: IF contains "click here"    THEN spam
RULE 4: OTHERWISE                   THEN not spam
```

Time spent: 20 minutes of thinking. Things checked: 3. Updatable: only by hand.

**Learning way** — a human collects and labels messages, and does no thinking about spam at all:

```
"WIN a FREE phone now!!!"      → spam
"Are you coming to practice?"  → not spam
"FREE money click here!!!"     → spam
"Mum said dinner at 7"         → not spam
... 4,996 more ...
```

Time spent: many hours of labelling. Things checked: every word that appears — maybe 20,000. Updatable: add 500 new examples next month and re-run.

**The trade in one sentence:** you swap *thinking* for *collecting*. Thinking doesn't scale. Collecting does.

**⚠️ And here is the catch, which Module 2 already warned you about.**

The machine believes your examples completely. If your 5,000 messages came only from your own phone, the model learns *your* spam, not spam in general. If you mislabelled 300 of them, the model learns your mistakes with perfect loyalty. **Rule-based systems fail because humans can't think of everything. Learned systems fail because humans can't collect everything.** Neither is magic; they just fail in different places.

```
     ┌──────────────────────────────────────────────────────────┐
     │  WHEN TO WRITE RULES YOURSELF                            │
     ├──────────────────────────────────────────────────────────┤
     │  ✔ The rule is genuinely simple and you know it          │
     │  ✔ You must be able to explain every single decision     │
     │  ✔ You have almost no examples                           │
     │  ✔ Getting it wrong is unacceptable (medicine doses,     │
     │    tax rates, safety cut-offs)                           │
     │  ✔ The rule is a decision someone MADE, not a pattern    │
     │    in the world  (e.g. "the speed limit is 30")          │
     └──────────────────────────────────────────────────────────┘
                                │
                                │  but if...
                                ▼
     ┌──────────────────────────────────────────────────────────┐
     │  WHEN TO MAKE THE MACHINE LEARNING TRADE                 │
     ├──────────────────────────────────────────────────────────┤
     │  ✔ You keep adding rules and accuracy barely moves       │
     │  ✔ The rules start contradicting each other              │
     │  ✔ You can recognise the answer but can't explain it     │
     │    ("I just know that's a dog")                          │
     │  ✔ The input is pixels, sound, or free text              │
     │  ✔ You can get lots of correctly-labelled examples       │
     │  ✔ The world keeps changing and rules go stale           │
     └──────────────────────────────────────────────────────────┘
```

That third bullet in the bottom box is the sharpest test anyone has found. **If you can do the task instantly but cannot explain how, rules will fail and learning will work.** You recognise your mother's face in a hundredth of a second and cannot describe how. Write rules for that and you'll fail. Show 200 photos and a machine will manage it.

---

## 🔍 Worked Example

Let's do the whole cycle end to end: find patterns in labelled data, write a rulebook, score it on the data it came from, then score it on fresh data — and watch exactly what breaks.

**The job:** decide whether a text message is `spam` or `ham`. (*Ham* is the traditional word for "not spam". It's a joke that stuck.)

---

### Step 1 — The training messages (10 labelled examples)

| # | Message | Truth |
|---|---|---|
| 1 | `WIN a FREE iPhone! Click now!!!` | spam |
| 2 | `Hey, are we still on for 5pm?` | ham |
| 3 | `CONGRATULATIONS! You won a PRIZE!!` | spam |
| 4 | `Can you bring my charger tomorrow` | ham |
| 5 | `FREE entry to win CASH! Text YES` | spam |
| 6 | `Mum says dinner is at 7:30` | ham |
| 7 | `URGENT: claim your reward NOW!!!` | spam |
| 8 | `did you finish the science homework?` | ham |
| 9 | `You have been SELECTED! Click here` | spam |
| 10 | `see you at the bus stop` | ham |

Five spam, five ham. Balanced — which matters, and Module 5 will explain why.

---

### Step 2 — Count things (this is the pattern hunt)

Don't guess. Count. Go through all 10 messages for each clue:

| Clue | In spam (of 5) | In ham (of 5) | Gap |
|---|---|---|---|
| Contains `FREE` | 2 (#1, #5) | 0 | **2** |
| Contains at least one `!` | 5 (#1, #3, #5, #7, #9) | 0 | **5** ⭐ |
| Contains `!!` or `!!!` | 3 (#1, #3, #7) | 0 | **3** |
| Contains `click` (any case) | 2 (#1, #9) | 0 | **2** |
| Has 2+ fully-capital words | 4 (#1, #3, #5, #7) | 0 | **4** ⭐ |
| Contains `win` / `won` / `WIN` | 3 (#1, #3, #5) | 0 | **3** |
| Contains a `?` | 0 | 3 (#2, #4, #8) | **3** (backwards!) |
| Message is under 40 characters | 1 (#7 is 32) | 4 (#2, #6, #8, #10) | **3** (backwards!) |

Let me verify the second starred row by hand, because it's the one that needs care.

**"2+ fully-capital words"** means two or more words written entirely in capitals, at least 2 letters long.

| # | Fully-capital words | Count | 2 or more? |
|---|---|---|---|
| 1 | `WIN`, `FREE` | 2 | ✅ |
| 2 | none | 0 | ❌ |
| 3 | `CONGRATULATIONS`, `PRIZE` | 2 | ✅ |
| 4 | none | 0 | ❌ |
| 5 | `FREE`, `CASH`, `YES` | 3 | ✅ |
| 6 | none | 0 | ❌ |
| 7 | `URGENT`, `NOW` | 2 | ✅ |
| 8 | none | 0 | ❌ |
| 9 | `SELECTED` | 1 | ❌ |
| 10 | none | 0 | ❌ |

So it fires on 4 of 5 spam and 0 of 5 ham. Strong, not perfect — #9 slips through with only one capital word.

⚠️ **The biggest gap is not automatically the best rule.** "Contains at least one `!`" has a perfect gap of 5 in this data, but a single exclamation mark is one of the most common things in ordinary friendly messages — my sample of 5 ham messages just happens not to contain one. Five rows is far too few to conclude that friends never use `!`. I'll use the doubled `!!` instead, which is rarer in ordinary writing. **This is a judgement call I am making from outside the data**, and it's exactly the kind of call that separates a good rulebook from a lucky one.

**Two clues point the *other* way** — `?` and short messages both indicate ham. Those are just as useful. A rulebook needs reasons to say "not spam" too, or everything drifts towards spam.

---

### Step 3 — Write the rulebook

Five rules, applied **first-match-wins**, top to bottom:

```
RULE 1:  IF the message contains "FREE" (any case)        THEN spam
RULE 2:  IF the message contains "!!" or "!!!"            THEN spam
RULE 3:  IF the message contains "click" (any case)       THEN spam
RULE 4:  IF the message contains "win" or "won" (any case) THEN spam
RULE 5:  IF the message contains "?"                      THEN ham
RULE 6:  OTHERWISE                                        THEN ham
```

Rule 6 isn't really a rule — it's the **default**, the answer when nothing fires. Every rulebook needs one, or it will freeze on an input it has no opinion about.

⚠️ Note that Rule 4 as written will also match the letters `win` inside other words, like `window` or `winter`. Keep that in your pocket; it will matter shortly.

---

### Step 4 — Score the rulebook on the training messages

Trace each one honestly, stopping at the first rule that fires:

| # | Message | First rule to fire | Says | Truth | ✓/✗ |
|---|---|---|---|---|---|
| 1 | `WIN a FREE iPhone! Click now!!!` | R1 (`FREE`) | spam | spam | ✅ |
| 2 | `Hey, are we still on for 5pm?` | R5 (`?`) | ham | ham | ✅ |
| 3 | `CONGRATULATIONS! You won a PRIZE!!` | R2 (`!!`) | spam | spam | ✅ |
| 4 | `Can you bring my charger tomorrow` | R6 (default) | ham | ham | ✅ |
| 5 | `FREE entry to win CASH! Text YES` | R1 (`FREE`) | spam | spam | ✅ |
| 6 | `Mum says dinner is at 7:30` | R6 (default) | ham | ham | ✅ |
| 7 | `URGENT: claim your reward NOW!!!` | R2 (`!!!`) | spam | spam | ✅ |
| 8 | `did you finish the science homework?` | R5 (`?`) | ham | ham | ✅ |
| 9 | `You have been SELECTED! Click here` | R3 (`Click`) | spam | spam | ✅ |
| 10 | `see you at the bus stop` | R6 (default) | ham | ham | ✅ |

**Score: 10 out of 10. 100%.**

```
Accuracy = correct ÷ total = 10 ÷ 10 = 1.0 = 100%
```

Perfect. Ship it. 🎉

**No. Stop.** Something is wrong, and it's important.

You built these rules *by looking at these exact ten messages*. Of course they score 100% — you designed them to. That's like writing an exam after seeing the answer sheet.

This is such an important idea that Module 6 is devoted entirely to it. For now, hold the suspicion: **a score on the examples you learned from is not evidence of anything.** The only honest test is fresh messages.

---

### Step 5 — Ten fresh messages the rulebook has never seen

| # | Message | Truth |
|---|---|---|
| 11 | `Your parcel is delayed, track it here` | spam |
| 12 | `WINTER SALE! 70% off everything` | spam |
| 13 | `I won the match!! So happy` | ham |
| 14 | `Free period tomorrow, want to meet?` | ham |
| 15 | `Bank alert: verify your account now` | spam |
| 16 | `Click the link I sent for the group project` | ham |
| 17 | `Reminder: dentist at 4pm` | ham |
| 18 | `U have won 5000!! Reply CLAIM` | spam |
| 19 | `whats the answer to q7` | ham |
| 20 | `Congratulations on your exam results!` | ham |

These are deliberately nasty — but every single one is the kind of message a real phone actually receives.

---

### Step 6 — Score on the fresh messages

| # | Message | First rule | Says | Truth | ✓/✗ | What happened |
|---|---|---|---|---|---|---|
| 11 | `Your parcel is delayed, track it here` | R6 default | ham | **spam** | ❌ | **Miss.** No FREE, no `!!`, no click, no win. A polite scam sails straight through |
| 12 | `WINTER SALE! 70% off everything` | R4 (`win` inside `WINTER`) | spam | spam | ✅ | Right answer, **wrong reason** — see below |
| 13 | `I won the match!! So happy` | R2 (`!!`) | spam | **ham** | ❌ | **False alarm.** Your friend's good news, binned |
| 14 | `Free period tomorrow, want to meet?` | R1 (`Free`) | spam | **ham** | ❌ | **False alarm.** "Free period" is a school timetable, not a prize |
| 15 | `Bank alert: verify your account now` | R6 default | ham | **spam** | ❌ | **Miss.** A real, dangerous scam. Zero trigger words |
| 16 | `Click the link I sent for the group project` | R3 (`Click`) | spam | **ham** | ❌ | **False alarm.** Classmates say "click the link" constantly |
| 17 | `Reminder: dentist at 4pm` | R6 default | ham | ham | ✅ | Correct |
| 18 | `U have won 5000!! Reply CLAIM` | R2 (`!!`) | spam | spam | ✅ | Correct |
| 19 | `whats the answer to q7` | R6 default | ham | ham | ✅ | Correct |
| 20 | `Congratulations on your exam results!` | R6 default | ham | ham | ✅ | Correct — one `!` isn't `!!` |

**Score: 5 out of 10.**

```
Accuracy = 5 ÷ 10 = 0.5 = 50%
```

**From 100% to 50%.** On a two-way choice, 50% is coin-flip performance. Your rulebook has no value at all.

---

### Step 7 — Read the wreckage

Break the 5 errors into the two types:

| Type | Count | Which ones | Cost |
|---|---|---|---|
| **False alarms** (ham marked spam) | 3 | #13, #14, #16 | You lose three real messages from friends |
| **Misses** (spam marked ham) | 2 | #11, #15 | Two scams in your inbox, one of them a bank scam |

**Which rule broke first, and worst?**

Rule 1 (`FREE`) caused false alarm #14. Rule 2 (`!!`) caused false alarm #13. Rule 3 (`Click`) caused false alarm #16. **All three of your strongest rules produced false alarms on fresh data.** Every rule that looked brilliant on the **training set** — the examples you were allowed to study while writing your rules — is now hurting you.

**And #12 is the most instructive row in the table.** The rulebook said spam. The truth was spam. ✅ But it fired because `win` appears inside `WINTER`. It got the right answer through a coincidence of spelling. **A rule that is right for the wrong reason will betray you the moment the coincidence stops holding** — the very next message about `winter`, `window`, or `winning the science fair` will be wrongly flagged. When you score a rulebook, always check *why* it was right, not just *that* it was.

---

### Step 8 — Try to fix it (this is the point of the whole module)

Let's actually try. Patch each failure:

**Fix for #14** (`Free period` → ham): add an exception.
```
RULE 0: IF the message contains "free period" THEN ham   [before Rule 1]
```
✅ Fixes #14. But `free time`? `free lesson`? `free to talk`? `are you free`? Each needs its own exception. **1 fix, 5+ new holes.**

**Fix for #13** (`I won the match!!` → ham): require `!!` AND a capital word.
```
RULE 2 (v2): IF contains "!!" AND has 2+ fully-capital words THEN spam
```
Check #13: `I won the match!! So happy` — fully-capital words: `I` is one letter, doesn't count. So 0 capital words. Rule 2 no longer fires. It falls to R4 (`won`) → still says spam. ❌ **Fix failed.** Now patch R4 too… and R4 was catching real spam in #18. **Every patch weakens a rule that was doing useful work.**

**Fix for #16** (`Click the link` → ham): only flag `click` from unknown senders.
```
RULE 3 (v2): IF contains "click" AND sender not in contacts THEN spam
```
✅ Genuinely good fix. **But notice what just happened: you needed information that isn't in the message.** Your rulebook was reading text; now it needs your contact list too. The system just got bigger and more complicated, and you've only fixed one message.

**Fix for #11 and #15** (the polite scams): what rule would catch these?

```
`Your parcel is delayed, track it here`
`Bank alert: verify your account now`
```

Try to write it. Go on, genuinely try for two minutes.

- `IF contains "verify"` → also catches "can you verify the meeting time?"
- `IF contains "account"` → also catches "I forgot my school account password"
- `IF contains "bank"` → also catches "meet me by the river bank" and every message about actual banking
- `IF contains "track"` → also catches every real delivery notification you'll ever get

**There is no word in these messages that isn't also in ordinary messages.** That's precisely why the scams are written that way. The scammer's job is to sound normal, and they are better at it than your rulebook is at catching them.

---

### Step 9 — The scoreboard

Suppose you spend three hours patching. Realistically:

| Rulebook | Rules | Training accuracy | Fresh accuracy |
|---|---|---|---|
| v1 (5 rules) | 5 | 100% | 50% |
| v2 (after 3 patches) | 8 | 100% | 60% |
| v3 (after 10 patches) | 18 | 100% | 65% |
| v4 (after 40 patches) | 58 | 100% | 68% |
| v5 (after 200 patches) | 258 | 100% | 70% |

Look at the shape. Training accuracy is stuck at 100% and tells you nothing. Fresh accuracy climbs — **and then flattens**. Rules 58 through 258 bought you **two percentage points**. Meanwhile the rulebook is now 258 rules that contradict each other, that nobody can read, and that a scammer can defeat by changing one word.

**That flattening curve is the wall.** It's the same wall the handwriting researchers hit in the 1980s. You have now hit it yourself, with your own rulebook, in about twenty minutes.

**What a learned system would do instead:** collect 5,000 labelled messages. Never think about which words matter — the counting finds that. It would weigh thousands of words at once, notice that `verify` is 8× more common in spam *when combined with* `account`, and reach 97% or better. And when scammers change tactics, you don't rewrite 258 rules — you add 500 new labelled messages and re-run.

**That is the trade. You have now earned the right to make it.**

---

## 💻 Hands-On

No programming. Paper, pencil, and a spreadsheet.

---

### Activity A — Be the machine: run a rulebook by hand (20 min)

You will execute a rulebook exactly as a computer would: no judgement, no shortcuts, first-match-wins.

**The rulebook — a homework-priority sorter:**

```
RULE 1: IF due_in_days = 0                        THEN "DO NOW"
RULE 2: IF due_in_days = 1 AND minutes_needed > 60 THEN "DO NOW"
RULE 3: IF due_in_days = 1                        THEN "DO TODAY"
RULE 4: IF minutes_needed > 120                   THEN "START EARLY"
RULE 5: IF due_in_days > 5                        THEN "LATER"
RULE 6: OTHERWISE                                 THEN "THIS WEEK"
```

**The tasks:**

| # | Task | due_in_days | minutes_needed | First rule that fires | Verdict |
|---|---|---|---|---|---|
| 1 | Maths sheet | 0 | 30 | | |
| 2 | Science poster | 1 | 90 | | |
| 3 | Read chapter | 1 | 20 | | |
| 4 | History essay | 7 | 180 | | |
| 5 | Spellings | 3 | 15 | | |
| 6 | Art project | 10 | 240 | | |
| 7 | Book review | 4 | 130 | | |
| 8 | Vocab list | 0 | 200 | | |

Fill in the last two columns. **Follow the rules exactly, in order, even when you disagree with the result.**

**Answers** (check yourself after you've tried):

| # | First rule | Verdict | Sensible? |
|---|---|---|---|
| 1 | R1 | DO NOW | ✅ |
| 2 | R2 (1 day, 90 > 60) | DO NOW | ✅ |
| 3 | R3 (R2 fails: 20 is not > 60) | DO TODAY | ✅ |
| 4 | R4 (180 > 120) | START EARLY | ✅ |
| 5 | R6 default | THIS WEEK | ✅ |
| 6 | R4 (240 > 120) | START EARLY | ⚠️ It's 10 days away — R5 "LATER" never gets a chance because R4 is above it |
| 7 | R4 (130 > 120) | START EARLY | ✅ |
| 8 | R1 | DO NOW | ⚠️ 200 minutes due today. "DO NOW" is technically right and completely useless — you needed to start three days ago |

**Now answer these three:**

1. **Swap Rule 4 and Rule 5.** Re-run tasks 4, 6, and 7. What changes?
   *(Task 6 becomes LATER — arguably better. But task 4, the 7-day 180-minute essay, also becomes LATER, which is worse. **One reorder, one improvement, one regression.**)*
2. **Task 8** is impossible to do well. Write a Rule 0 that catches it. What should it even say?
3. Your Rule 0 probably says something like `IF due_in_days ≤ 1 AND minutes_needed > 150 THEN "TOO LATE — ASK FOR HELP"`. **Where exactly did the numbers 1 and 150 come from?** You invented them. Would a different student pick different numbers? What would happen if a task needed 149 minutes?

That last question is the whole game. **Every threshold in every hand-written rule is a number a human made up.** A learned system picks those numbers from data instead of from a hunch.

---

### Activity B — Rule explosion, measured on your own hand (15 min)

You'll build the explosion table yourself so the numbers are yours, not mine.

Open a spreadsheet.

**Step 1.** In `A1` type `things_checked`, in `B1` type `situations`, in `C1` type `hours_to_write`, in `D1` type `years_to_write`.

**Step 2.** In `A2` through `A21`, put the numbers 1 to 20. (Type `1`, then `2`, select both, and drag the little square down.)

**Step 3.** In `B2` type:

```
=2^A2
```

**Step 4.** In `C2` type — assuming 2 minutes per rule:

```
=B2*2/60
```

**Step 5.** In `D2` type — assuming an 8-hour working day and 250 working days a year:

```
=C2/8/250
```

**Step 6.** Select `B2:D2` and drag down to row 21.

**Expected output** (spot-check these against yours):

| things_checked | situations | hours_to_write | years_to_write |
|---|---|---|---|
| 1 | 2 | 0.07 | 0.00003 |
| 5 | 32 | 1.07 | 0.0005 |
| 10 | 1,024 | 34.1 | 0.017 |
| 15 | 32,768 | 1,092.3 | 0.546 |
| 20 | 1,048,576 | 34,952.5 | **17.5** |

**Step 7.** Make a chart. Select `A1:B21`, then Insert → Chart → Line chart.

Look at it. For the first ten rows it hugs the bottom axis and looks like *nothing is happening*. Then it goes vertical.

**Step 8.** Now switch the vertical axis to logarithmic (Chart editor → Customise → Vertical axis → tick "Log scale"). The curve becomes a **straight line**.

**That straight line is the signature of exponential growth.** Whenever you see a straight line on a log chart, something is doubling — and human effort cannot keep up with doubling.

**Step 9 — write down the answer to this.** Find the row where `years_to_write` first goes above 1. Then answer: *if a task needs you to check that many things, and you started writing rules the day you were born, would you be finished yet?*

**Step 10 — the honest counter-argument.** A real programmer wouldn't write all 2ⁿ rules — they'd write rules that cover many situations at once (`IF FREE THEN spam` covers 4 of the 8 three-question situations by itself). So the true number is smaller than 2ⁿ.

**Does that save the rule-writer?** Write two sentences. *(It helps a lot at n=10 and not at all at n=20,000, which is roughly how many distinct words appear in real text messages. The shortcut buys you a bigger n; it doesn't change the shape of the curve.)*

---

### Activity C — The two-column pattern hunt (15 min)

Here's a table of 12 students and whether they passed a test. Find the pattern by counting — don't eyeball it.

| id | hours_studied | slept_well | passed |
|---|---|---|---|
| 1 | 0.5 | no | no |
| 2 | 3.0 | yes | yes |
| 3 | 1.0 | yes | no |
| 4 | 4.0 | no | yes |
| 5 | 2.0 | yes | yes |
| 6 | 0.0 | yes | no |
| 7 | 5.0 | yes | yes |
| 8 | 1.5 | no | no |
| 9 | 2.5 | no | yes |
| 10 | 3.5 | yes | yes |
| 11 | 0.5 | yes | no |
| 12 | 6.0 | no | yes |

**Step 1 — split by the number column.** Sort mentally by `hours_studied` and mark where `passed` flips:

```
hours: 0.0  0.5  0.5  1.0  1.5 │ 2.0  2.5  3.0  3.5  4.0  5.0  6.0
pass:   no   no   no   no   no │ yes  yes  yes  yes  yes  yes  yes
                               ↑
                    the line is between 1.5 and 2.0
```

**A perfectly clean split.** Every student below 2.0 hours failed; every student at or above 2.0 hours passed. Rule:

```
IF hours_studied >= 2.0 THEN pass  ELSE fail
```

**Step 2 — score it.** Check all 12: rows 1,3,6,8,11 are below 2.0 and all failed ✅. Rows 2,4,5,7,9,10,12 are at/above 2.0 and all passed ✅. **12 out of 12 = 100%.**

**Step 3 — now check `slept_well` on its own.**

| slept_well | count | passed | rate |
|---|---|---|---|
| yes | 7 (rows 2,3,5,6,7,10,11) | 4 | 57% |
| no | 5 (rows 1,4,8,9,12) | 3 | 60% |

57% vs 60%. **Sleeping well is associated with passing slightly *less* often.** That is almost certainly noise from 12 rows, and it certainly isn't evidence that sleep is bad for you. **`slept_well` is a useless column here** — it carries no signal.

**Step 4 — the three questions that matter.**

1. **Would you bet money that `hours_studied >= 2.0` works on 100 new students?**
   No. A perfectly clean split in 12 rows is exactly what you'd expect if you had *lucked into* a clean split. With 100 students you'd see students who studied 4 hours and failed, and students who studied 1 hour and passed — because studying isn't the only thing that matters.

2. **Why is 2.0 the threshold and not 1.9 or 2.1?**
   Because your data has a gap between 1.5 and 2.0 and nothing in between. **Any number in that gap fits your data equally well.** You picked 2.0 because it's round. That's not evidence, it's aesthetics.

3. **What would make you trust this rule?**
   More rows, especially rows near the boundary. If you collected 50 students who studied between 1.5 and 2.5 hours and the split still held, that would be real evidence. **The most valuable new data always sits at the boundary, not at the extremes.**

---

## ✍️ Practice

**[Warm-up] 1 — Pattern to rule.**
For each mini-table, state the pattern in one sentence, then write it as an if-then rule using only testable conditions.

*(a)*
| fruit | colour | ripe |
|---|---|---|
| banana | green | no |
| banana | yellow | yes |
| banana | brown | yes |
| banana | green | no |

*(b)*
| message_length | has_link | spam |
|---|---|---|
| 15 | no | no |
| 140 | yes | yes |
| 22 | no | no |
| 160 | yes | yes |
| 18 | yes | no |

*Done looks like:* 2 sentences and 2 if-then rules. Every condition must be something a machine could check without judgement. For (b), state which of the two columns actually carries the pattern and give your evidence.

**[Warm-up] 2 — Sharpen the vague rules.**
Rewrite each of these so a machine could run it. Then state the exact value you chose and why.
(a) `IF the email looks suspicious THEN spam`
(b) `IF the student is struggling THEN offer help`
(c) `IF the photo is bad quality THEN reject it`
(d) `IF the weather is nice THEN go outside`
*Done looks like:* 4 rewritten rules, each with a specific number or a specific testable condition, plus one sentence per rule explaining where your number came from and who might reasonably disagree with it.

**[Build] 3 — Build and break a 5-rule book.**
Pick one job: (a) is this email from my school? (b) should I take an umbrella? (c) is this YouTube video suitable for a 6-year-old?
Write 5 rules plus a default. Then invent **8 test cases** — 4 you expect it to get right and 4 designed to break it. Score all 8.
*Done looks like:* 5 rules + default written out, an 8-row scored table with columns `case | first rule to fire | verdict | truth | correct?`, an accuracy as a fraction and a percentage, and one sentence naming which rule caused the most damage.

**[Build] 4 — Count the explosion.**
A school wants a rule-based system to decide whether a student can attend a trip. It checks: permission slip signed (yes/no), payment made (yes/no), no detentions (yes/no), medical form (yes/no), and year group (7, 8, or 9).
(a) How many distinct situations exist? Show the multiplication.
(b) Now add "allergy declared" (yes/no) and "swimming ability" (none/weak/strong). How many now?
(c) At 3 minutes of thought per situation, how many hours is that?
(d) Write one sentence explaining why the real system probably needs far fewer rules than your count — and one sentence on why the count still matters.
*Done looks like:* 3 numbers with the multiplications shown, an hours figure, and 2 sentences.

**[Stretch] 5 — The unwritable rule.**
Choose one: (a) is this joke funny? (b) is this drawing of a cat or a dog? (c) is this person's voice happy or sad?
Write **5 serious rules**. Then, for each, give a real case it gets wrong. Then answer the hard question: **what information would the rule need that isn't available in the input?**
*Done looks like:* 5 rules, 5 counterexamples, and a closing paragraph (5+ sentences) that names the missing information specifically and explains why more rules cannot manufacture it.

**[Stretch] 6 — Argue the other side.**
Everything in this module argues that rules break down. **Now argue against it.** Find **three real jobs** where a hand-written rulebook is clearly the *right* choice and machine learning would be a bad idea. For each, give the job, a sample rule, and two specific reasons rules win here.
*Done looks like:* 3 jobs from genuinely different areas, 3 sample rules, 6 reasons, and a closing sentence stating the general test you'd apply to decide "rules or learning?" on a new job.

---

## 🤔 Think Deeper

**1. If a rule is right 95% of the time, who should decide what happens to the other 5%?**
A school uses `IF a student is late 3 times THEN detention`. It's right most of the time. But one student is late because she takes her little brother to a different school first.
*How to reason about it:* separate three different questions — should the rule exist at all, should there be an appeal route, and who hears the appeal. Then think about scale: a rule with a human appeal works for 200 students and collapses for 200 million users. Does the *right* answer change when the numbers change, or does only the *affordable* answer change? That gap is where a lot of real-world unfairness lives.

**2. Is a machine-learned system just a rulebook you can't read?**
A learned model does end up with *some* internal rule. Is the only real difference that a human can't read it — and if so, is that difference important or merely inconvenient?
*How to reason about it:* find something a learned system does that a written rulebook genuinely cannot, no matter how long the rulebook is. Consider a model that weighs 20,000 words simultaneously with different strengths — could a human write that as if-then rules? Could a human *maintain* it? Then flip it: find something a rulebook can do that a learned system can't, like being changed instantly by a single person who disagrees with one decision.

**3. Should the person who writes the rules have to live under them?**
The people who write school rules are teachers. The people who write app rules are engineers. The people who write laws are politicians. In each case, someone writes rules that mostly govern other people.
*How to reason about it:* think about which failures a rule-writer will *notice*. A rule-writer who is subject to their own rule notices the edge cases immediately, because they hurt. A rule-writer who isn't subject to it only hears about failures if someone can complain and be heard. Now apply this to a machine learning system: the "rule-writer" is whoever chose the training examples. What happens if the people affected by the model are not in the training data at all? Hold this question — Module 9 comes back to it directly.

---

## ⚠️ Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Testing a rulebook on the examples you built it from | It's the data in front of you, and the 100% score feels great | You designed those rules to fit those cases. Always keep fresh examples aside and score on those. This is the whole of Module 6 |
| Writing conditions a machine can't check (`IF it looks dodgy`) | That's genuinely how you think about it | Replace every adjective with a count or a comparison. "Long" → "more than 100 characters". If you can't count it, you can't rule on it |
| Ignoring rule order | The rules feel like a list, not a sequence | State your convention (first-match-wins) at the top and trace order-sensitive cases by hand. Swapping two rules can change many answers |
| Forgetting the default | You only think about cases that fire a rule | Always write a final `OTHERWISE` rule. Without it the system has no answer for inputs nothing matches — which is most inputs |
| Patching each failure with a new exception | Each individual patch genuinely works | Notice when patch count grows faster than accuracy. Flat accuracy with a growing rulebook is the signal to switch to learning |
| Assuming a rule that got the right answer got it for the right reason | You only checked the verdict column | Check *which rule fired* and whether that reason makes sense. `WINTER` matching `win` is a right answer built on sand |
| Chasing one kind of error and creating the other | You fix the failures you happen to notice | Count false alarms and misses separately, every time. Decide in advance which one you'd rather have, based on the actual cost |
| Trusting a clean split found in 12 rows | Clean splits look like laws of nature | Ask "how many rows sit near the boundary?" If the answer is zero, your threshold is a guess dressed as a discovery |
| Believing machine learning removes the need for human choices | The machine "finds the rule itself" | Humans still choose the examples, the labels, and what counts as a correct answer. The choices moved; they didn't disappear |

---

## 🛠️ Mini-Project — Rulebook vs Reality

**Time: ~2.5 hours.**

### 🎯 Goal

Write a spam-detector rulebook from **20 labelled text messages**, then apply it to **10 fresh messages you never saw while writing the rules**. Tally the hits and misses, and write about which rule broke first.

This project makes you *feel* the gap between 100% on your own data and reality. That feeling is the thing you're actually here to acquire.

---

### 📋 Starter steps

**Step 1 — Build your labelled set of 20 (30 min).**

You need 20 messages: **10 spam, 10 ham.** Get them from:

- ✅ Your own phone's spam/junk folder (with a parent's permission)
- ✅ Real ordinary messages from friends and family — **change all names to initials**
- ✅ Write realistic ones yourself if you can't find enough

⚠️ **Privacy rules, non-negotiable:**
- Replace every name with an initial: `Priya` → `P`
- Remove every phone number, address, and link — write `[LINK]` and `[NUMBER]`
- Never include a message about someone's health, money, or family problems
- Ask before using anyone else's messages

Put them in a table:

| id | message | truth |
|---|---|---|
| 1 | | spam / ham |
| … | | |
| 20 | | |

**Step 2 — Set the 10 fresh messages aside NOW, before writing any rules (10 min).**

This is the most important instruction in the project.

Collect **10 more messages** (5 spam, 5 ham). Write them on a separate sheet. **Fold it, put it in an envelope, and do not look at it again until Step 5.**

If you peek, the whole project is worthless — you'll unconsciously write rules that fit those exact messages, get a great score, and learn nothing. Those hidden messages are your **test set** — examples you lock away before you start, and score yourself on exactly once at the end. Peeking is called *contaminating your test set*, and professional researchers ruin real studies this way. (Module 6 is all about doing this properly.)

**Step 3 — Hunt patterns by counting (25 min).**

Do not write rules yet. **Count first.** Make a tally table:

| Clue | In spam (of 10) | In ham (of 10) | Gap |
|---|---|---|---|
| contains "free" | | | |
| contains "win"/"won" | | | |
| contains "!!" | | | |
| contains "click" | | | |
| contains "?" | | | |
| has a [LINK] | | | |
| 2+ ALL-CAPS words | | | |
| under 40 characters | | | |
| *(add 4 of your own)* | | | |

**Only clues with a gap of 4 or more are worth a rule.** A clue that appears in 5 spam and 4 ham has a gap of 1 and is noise.

**Also look for reverse clues** — things that indicate *ham*. You need at least one.

**Step 4 — Write your rulebook (20 min).**

At least **5 rules plus a default**. Format:

```
CONVENTION: first match wins, checked top to bottom.

RULE 1: IF __________________________ THEN __________
RULE 2: IF __________________________ THEN __________
RULE 3: IF __________________________ THEN __________
RULE 4: IF __________________________ THEN __________
RULE 5: IF __________________________ THEN __________
DEFAULT: OTHERWISE                    THEN __________
```

Requirements:
- Every condition must be checkable by counting or exact matching. No adjectives.
- At least one rule must output `ham`.
- Write a one-line justification for each rule, quoting its gap from your tally table.

Then **score it on your 20 training messages** and record the accuracy. It'll be high. Note it down and don't be impressed by it.

**Step 5 — Open the envelope. Score the 10 fresh messages (25 min).**

Now you may look. Score every one, **rule by rule, in order**, with no cheating:

| # | Message | First rule to fire | Verdict | Truth | ✓/✗ | Error type |
|---|---|---|---|---|---|---|
| 21 | | | | | | false alarm / miss / — |
| … | | | | | | |
| 30 | | | | | | |

⚠️ **Apply the rules mechanically.** If a rule gives an answer you know is wrong, write the wrong answer down. You are the computer, not the judge. Being honest here is the entire point.

**Step 6 — Compute your numbers (10 min).**

```
Training accuracy = correct on 20    ÷ 20  = ____  = ____%
Fresh accuracy    = correct on 10    ÷ 10  = ____  = ____%
The gap           = training% − fresh%      = ____ percentage points

False alarms (ham marked spam) = ____
Misses      (spam marked ham)  = ____
```

Also check **which rule fired** on each correct answer. Mark any that were right for a coincidental reason.

**Step 7 — Write the analysis paragraph (20 min).**

At least 8 sentences, and it must contain all six of these:

1. Which rule broke first — the specific rule and the specific message.
2. Whether that rule was one of your *strongest* ones on the training data. (It usually is. Say so if it is.)
3. Which error type you had more of, and why that matters for a real phone.
4. One message you believe **no rule you could write** would catch. Explain why.
5. What your accuracy gap tells you about your training set.
6. What you'd do next if you were actually building this — and it should not be "add more rules".

---

### ✅ Success criteria checklist

- [ ] 20 labelled training messages, 10 spam and 10 ham
- [ ] All names replaced with initials, all numbers and links removed
- [ ] 10 fresh messages set aside **before** any rule was written, and genuinely not looked at
- [ ] A completed tally table with at least 12 clues, including gaps
- [ ] 5+ rules plus a default, all with countable conditions
- [ ] At least one rule that outputs `ham`
- [ ] A one-line justification per rule quoting its tally gap
- [ ] Training accuracy computed and recorded
- [ ] A 10-row scored table on the fresh messages, with the first-firing rule named for each
- [ ] Fresh accuracy shown as a fraction and a percentage
- [ ] False alarms and misses counted separately
- [ ] Any "right for the wrong reason" rows marked
- [ ] An analysis paragraph of 8+ sentences containing all six required points

---

### 🚀 Level it up

**The adversary round.**

Give your rulebook to a friend or sibling — let them read every rule. Then challenge them:

> *"Write 5 messages that are obviously spam to a human, but that my rulebook marks as ham."*

Give them 10 minutes. Score their 5 messages.

**Expect to score close to 0 out of 5.** Once someone can see the rules, defeating them is trivial — they just avoid your trigger words.

Then write half a page on this:

1. How long did it take them to beat you?
2. **Real spammers do exactly this, constantly, at industrial scale.** They send test messages, see which get through, and rewrite. What does that mean for a rulebook's shelf life?
3. If your rules had been *learned from 5,000 examples* instead of written by you, would your friend have found it harder to break? Why?
4. Here's the sting in the tail: **could a determined attacker still break a learned model?** (Yes — and they do. It's called an adversarial attack. You can't see the rules, but you can still probe the system with test messages and find the gaps. Learning raises the cost of attacking; it doesn't make attacking impossible.)

---

## 🔑 Key Takeaways

- **A pattern is something that repeats often enough to bet on** — and it only counts if betting on it beats guessing. Check that with actual numbers.
- **An if-then rule needs testable, unambiguous conditions built from data you actually have.** Every adjective must become a count or a comparison.
- **Every rule has edge cases**, because every rule uses a stand-in for what really matters. Edge cases are guaranteed, not unlucky.
- **There are two kinds of wrong — false alarms and misses — and you must choose which one you'd rather have.** You can't drive both to zero.
- **Rule explosion is exponential:** each new thing you check doubles the situations. Thirty yes/no questions is over a billion combinations. No human can keep up with doubling.
- **A rulebook is frozen the moment you finish it, and the world isn't.** Anyone who can see your rules can walk around them.
- **The machine learning trade:** stop writing rules, start collecting labelled examples. You give up explainability and you need lots of data. You gain the ability to handle jobs no human could write rules for.
- **Scoring your rulebook on the examples you built it from proves nothing.** Only fresh examples tell the truth.

---

## 📓 Vocabulary

| Term | Kid-friendly definition | Example |
|---|---|---|
| **Pattern** | Something that repeats often enough that betting on it beats guessing | The 9:05 bus is late on 4 out of 4 Mondays |
| **If-then rule** | An instruction: if this condition is true, do that | `IF day = Monday THEN predict "late"` |
| **Condition** | The testable part of a rule — the bit after IF | `more than 50% of letters are capitals` |
| **Rulebook** | An ordered list of rules, plus a default | The 5 spam rules in the Worked Example |
| **Default** | The answer when no rule fires | `OTHERWISE → ham` |
| **First match wins** | The convention that the first rule to fire decides the answer | Rule 1 beats Rule 4 even if both would fire |
| **Threshold** | The cut-off number inside a condition | The `2.0` in `IF hours_studied >= 2.0` |
| **Edge case** | An example your rule gets wrong, usually near a boundary | A 138cm teenager turned away from a 140cm ride |
| **False alarm** | The system says yes when the truth is no | A friend's message marked as spam |
| **Miss** | The system says no when the truth is yes | A bank scam landing in the inbox |
| **Rule explosion** | Rules needed grow far faster than the cases, until it's unmaintainable | 30 yes/no checks = over a billion situations |
| **Exponential growth** | A quantity that doubles at every step | 2, 4, 8, 16, 32… reaching a billion in 30 steps |
| **Labelled example** | A piece of data with the correct answer written next to it | `"FREE money!!!" → spam` |
| **Training examples** | The labelled examples you built your rules or model from | The 20 messages in the mini-project |
| **Fresh examples** | Examples the system has never seen, used for honest scoring | The 10 in the sealed envelope |
| **Accuracy** | Correct answers ÷ total answers | 5 out of 10 = 0.5 = 50% |
| **The machine learning trade** | Give up writing rules; give the machine labelled examples instead | 5,000 labelled messages instead of 258 rules |

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers</summary>

---

### Exercise 1 — Pattern to rule

**(a) Bananas**

**Pattern:** Green bananas are not ripe; yellow and brown ones are.

**Rule:**
```
RULE 1: IF colour = "green"  THEN not ripe
RULE 2: OTHERWISE            THEN ripe
```

Check all 4 rows: green→not ripe ✅, yellow→ripe ✅, brown→ripe ✅, green→not ripe ✅. **4 of 4.**

⚠️ **Worth noticing:** the table only ever shows three colours. A black banana would be called "ripe" by Rule 2, which is wrong — it's rotten. **Your rule is only defined over the colours you saw.** That's an edge case waiting to happen, and it's the same shape as every failure in this module.

**(b) Messages**

**Pattern:** Long messages are spam; short ones are not. `has_link` looks like it matters but doesn't.

**Rule:**
```
RULE 1: IF message_length > 100  THEN spam
RULE 2: OTHERWISE                 THEN not spam
```

Check all 5: 15→not spam ✅, 140→spam ✅, 22→not spam ✅, 160→spam ✅, 18→not spam ✅. **5 of 5.**

**Which column carries the pattern — the evidence:**

| has_link | count | spam | rate |
|---|---|---|---|
| yes | 3 (rows 2, 4, 5) | 2 | 67% |
| no | 2 (rows 1, 3) | 0 | 0% |

| length | rows | spam | rate |
|---|---|---|---|
| > 100 | 2 (rows 2, 4) | 2 | **100%** |
| ≤ 100 | 3 (rows 1, 3, 5) | 0 | **0%** |

`message_length` splits the data perfectly. `has_link` does not — **row 5 is the proof**: length 18, has a link, and is *not* spam. That single row breaks any rule based on links and leaves the length rule untouched.

**Row 5 is the most valuable row in the table**, because it's the only one where the two candidate clues disagree. Rows where clues agree tell you nothing about which clue is doing the work.

⚠️ **The honest caveat:** the threshold could be anything from 23 to 139 and fit this data equally well. `100` is a guess, chosen because it's round.

---

### Exercise 2 — Sharpen the vague rules

**(a)** `IF the email looks suspicious THEN spam`

> **Rewritten:** `IF the sender's address is not in my contacts AND the email contains 2 or more links AND the subject line contains "urgent", "verify", or "suspended" THEN spam`

**Where the values came from:** "2 or more links" because ordinary personal emails almost never contain two links, while phishing emails usually do. The three subject words come from urgency language, which is the one thing nearly all phishing shares. **Who'd disagree:** anyone in a workplace where colleagues genuinely send multi-link emails, and anyone whose bank genuinely uses the word "verify" — for them this rule would produce constant false alarms.

**(b)** `IF the student is struggling THEN offer help`

> **Rewritten:** `IF the average of the last 3 assignment scores is below 50% OR 2 or more assignments in the last month were submitted late THEN offer help`

**Where the values came from:** three assignments is enough to distinguish a bad day from a trend; 50% is the school's own pass mark, so it isn't arbitrary. **Who'd disagree:** a student who scores 88% when she normally scores 98% is genuinely struggling and this rule can't see her — it detects low absolute performance, not a personal drop. A rule based on *change* would catch a different, equally real group of students. Both rules are defensible; neither catches everyone.

**(c)** `IF the photo is bad quality THEN reject it`

> **Rewritten:** `IF the image is smaller than 400×400 pixels OR the file size is under 20 kilobytes OR more than 60% of pixels are pure black or pure white THEN reject it`

**Where the values came from:** 400×400 is roughly the smallest size a face is recognisable at on a screen; the black/white check catches photos taken with the lens covered or straight into a light. **Who'd disagree:** an artist submitting a deliberately high-contrast black-and-white photograph would be rejected by the third clause, and the photo could be excellent.

**(d)** `IF the weather is nice THEN go outside`

> **Rewritten:** `IF temperature is between 15°C and 30°C AND rainfall in the last hour is 0mm AND wind speed is under 25 km/h THEN go outside`

**Where the values came from:** 15–30°C is a comfort band for someone in light clothing; 25 km/h is roughly when loose objects start blowing about. **Who'd disagree:** basically everyone. Someone from a cold country finds 15°C pleasant; someone from a hot one finds it freezing. **"Nice weather" isn't a fact about the weather — it's a fact about the person**, which is exactly why no single threshold can be right.

**The pattern across all four:** every sharpened rule needed a number, every number was invented by a human, and in every case a reasonable person would pick a different one. This is the hidden human judgement inside every "objective" rule-based system.

---

### Exercise 3 — Build and break a 5-rule book

**Model answer: (b) Should I take an umbrella?**

**Rulebook** (first match wins):
```
RULE 1: IF rain_chance_percent >= 70                        THEN take umbrella
RULE 2: IF rain_chance_percent >= 40 AND minutes_outside > 30 THEN take umbrella
RULE 3: IF wind_speed_kmh > 40                              THEN leave it (it'll break)
RULE 4: IF rain_chance_percent < 20                         THEN leave it
RULE 5: IF I have a hood AND minutes_outside <= 15          THEN leave it
DEFAULT:                                                     THEN take umbrella
```

**Test cases:**

| # | Case | First rule | Verdict | Truth | ✓/✗ |
|---|---|---|---|---|---|
| 1 | 85% rain, 20 min walk, no wind | R1 | take | take | ✅ |
| 2 | 5% rain, 45 min out | R4 | leave | leave | ✅ |
| 3 | 50% rain, 60 min out | R2 | take | take | ✅ |
| 4 | 30% rain, 10 min, have a hood | R5 | leave | leave | ✅ |
| 5 | 90% rain **and** 60 km/h wind | R1 (fires before R3) | take | **leave** — it will invert and break | ❌ |
| 6 | 15% rain but a thunderstorm forecast for 4pm | R4 | leave | **take** | ❌ |
| 7 | 35% rain, 25 min out, no hood | DEFAULT | take | leave (that's a lot of carrying for a 1-in-3 chance) | ❌ |
| 8 | 75% rain, but I'm going by car door-to-door | R1 | take | **leave** — I'm never outside | ❌ |

**Accuracy: 4 ÷ 8 = 0.5 = 50%**

**Which rule caused the most damage: Rule 1.** It caused failures #5 and #8, and it caused them because it fires *first* and unconditionally. It looks at only one variable — rain chance — and once it fires, nothing below it ever gets a say. Rule 3 (the wind rule) is correct and useful and **can literally never run when rain chance is 70% or more**, because Rule 1 always beats it to the answer.

**The deeper lesson:** my most confident rule was my worst rule, precisely *because* I was confident enough to put it first. In a first-match-wins rulebook, the rules at the top do the most damage, and the ones at the bottom are often dead code.

*(Case #8 exposes something else: the real question was never "will it rain?" — it was "will I be outside while it rains?" My rulebook is measuring the wrong thing entirely. No amount of tuning the rain thresholds fixes that.)*

---

### Exercise 4 — Count the explosion

**(a) The original five checks**

Permission slip (2) × payment (2) × no detentions (2) × medical form (2) × year group (3):

```
2 × 2 × 2 × 2 × 3 = 48 situations
```

**(b) Adding allergy (2) and swimming ability (3)**

```
2 × 2 × 2 × 2 × 3 × 2 × 3 = 288 situations
```

Check: `48 × 2 × 3 = 48 × 6 = 288`. ✅

**Two more questions took it from 48 to 288 — six times bigger.**

**(c) Hours of thought**

```
288 situations × 3 minutes = 864 minutes
864 ÷ 60 = 14.4 hours
```

**14.4 hours** — nearly two full working days, to write rules for a school trip.

**(d) Two sentences**

> **Why the real system needs fewer rules:** most of the 288 situations collapse into one another, because a single rule can cover a whole block at once — `IF permission_slip = no THEN refuse` settles 144 situations (half of all of them) in one line, regardless of every other field.

> **Why the count still matters:** those shortcuts only work while the checks are *independent*, and the moment they interact — a weak swimmer with a medical form is fine for the museum but not the lake, unless a parent is coming — you're back to reasoning about specific combinations, and the number of combinations is what sets the ceiling on how complicated the system can ever get.

**Bonus insight:** notice that going from 48 to 288 needed just two extra questions. That's a factor of 6 for two questions. Add four more small questions and you're past 10,000. **The explosion doesn't need big numbers — it needs a few more small ones.**

---

### Exercise 5 — The unwritable rule

**Model answer: (a) Is this joke funny?**

| # | Rule | A real case it gets wrong |
|---|---|---|
| 1 | `IF the text ends with a punchline shorter than 8 words THEN funny` | "The house burned down." Short, final, not funny |
| 2 | `IF the text contains a pun (a word with two meanings) THEN funny` | "The bank charged me a fee at the river bank." Technically a pun. Nobody laughs |
| 3 | `IF the text has an unexpected final word THEN funny` | "I went to the shop and bought some xylophone." Unexpected, just confusing |
| 4 | `IF the text contains "knock knock" THEN funny` | A note reading "knock knock before entering, Dad is on a call." Not a joke at all |
| 5 | `IF the audience laughed within 2 seconds THEN funny` | A nervous laugh at a funeral. Or a laugh track on a bad sitcom |

**Closing paragraph:**

Every one of my rules fails for the same underlying reason: funniness is not a property of the text. It's a property of the relationship between the text, the listener, and the moment. The exact same sentence — "nice haircut" — is a joke between two friends who both know the haircut is a disaster, and it's cruelty from a stranger, and it's a simple compliment from a grandmother. Nothing in the words distinguishes those three, so no rule that reads only the words can ever separate them.

The information my rules would need, and which is not in the input, is: **who is saying it, to whom, what those two people already know, what just happened, and what has been funny between them before.** That's context, and context is not a longer version of the text — it's a different kind of thing entirely. I could add a thousand rules about wordplay and rhythm and timing and I would not have added a single bit of that information, because more rules can only look harder at what's already there; they cannot fetch what isn't.

And there's a second problem I noticed while writing rule 5. Even if I *had* the full context, I'd still be stuck, because different people find different things funny — so there isn't one correct answer to learn. This is the honest limit: machine learning would beat my rulebook here, because a model trained on thousands of jokes rated by thousands of people would at least learn what *most* people laugh at. But even that model would be predicting "would the average rater laugh?", which is a real and useful question and a completely different question from "is this funny?" **Sometimes the task itself doesn't have a single right answer, and pretending otherwise is the first mistake, before any rule gets written.**

---

### Exercise 6 — Argue the other side

**Three jobs where hand-written rules clearly win:**

---

**Job 1 — Calculating income tax owed.**

> Sample rule: `IF taxable_income > 300000 AND taxable_income <= 600000 THEN tax = 5% of (taxable_income − 300000)`

**Reason 1 — the rule isn't a pattern in the world, it's a decision somebody made.** There is nothing to discover. A parliament wrote the bands down. Training a model on past tax returns to "learn" the tax rate would be absurd: it would give you an approximation of a number that is already exactly known.

**Reason 2 — every single decision must be explainable and identical.** If two people with identical incomes get different tax bills, that's a scandal. A learned model can output 5.0001% for one and 4.9998% for another, and nobody could explain why. Here, "predictable and explainable" isn't a nice-to-have — it's the entire requirement.

---

**Job 2 — A hospital drug-dosage safety cut-off.**

> Sample rule: `IF prescribed_dose > max_safe_dose_for_weight THEN block the order and alert the pharmacist`

**Reason 1 — the cost of a rare failure is catastrophic and irreversible.** A model that is 99.9% accurate kills someone in one case per thousand. A rule derived from published safety limits is right every time by construction, because it's just an arithmetic comparison against a number a pharmacologist established.

**Reason 2 — the correct answer is already known from science, not from data.** The safe maximum came from controlled trials. Learning it from hospital records would learn *what doctors actually prescribed*, mistakes included — which is precisely the failure that happened to the asthma-pneumonia model in this level's Module 2 hook.

---

**Job 3 — Deciding whether a chess move is legal.**

> Sample rule: `IF the piece is a bishop AND the move is not along an unobstructed diagonal THEN illegal`

**Reason 1 — the rules are complete, finite, and published.** Chess has about a dozen movement rules plus castling, en passant, and promotion. All of them fit on two pages, and they cover every position that can ever occur. There is no edge case, because the rulebook *defines* the game rather than describing it.

**Reason 2 — a learned system would be worse in a way that can't be patched.** Train on a million games and the model learns "bishops usually move like this" — and will occasionally allow an illegal move it never saw, or reject a legal-but-rare one like en passant. **In a domain with a complete published rulebook, learning can only introduce errors that the rules didn't have.**

---

**The general test I'd apply to a new job:**

> **Ask: does the correct answer already exist somewhere in written form, or does it have to be discovered from examples?** If a human wrote the answer down — a law, a game rule, a published safety limit, a company policy — implement it as rules, because learning can only produce a fuzzy copy of something already exact. If the answer lives only in people's ability to recognise it without explaining it — spam, faces, ripe fruit, sarcasm — write no rules and collect examples, because there is nothing to copy.

**A useful second question when the first is unclear:** *what happens on the case nobody anticipated?* Rules go silent or give a confidently wrong answer, and a human notices only if someone complains. Learned systems give a confident answer too — but they at least stand a chance of having seen something similar. Choose based on which failure you can afford.

---

</details>

---

[⬅ Previous](module-02-data-is-everywhere.md) · [Level 1 Home](README.md) · [Next ➡](module-04-features-and-labels.md)

*Next up: you've decided to make the machine learning trade. But a machine can't read your text messages the way you do — it needs each example turned into a row of measurements, and one column marked as the answer. Module 4 is about **features** and **labels**: how a machine describes a thing.*
