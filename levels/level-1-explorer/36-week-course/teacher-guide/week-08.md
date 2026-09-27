# Week 8 — Where Rules Break: Edge Cases and False Alarms

[⬅ Week 7](week-07.md) · [Course Home](../README.md) · [Week 9 ➡](week-09.md) · [Student Guide](../student-guide/week-08.md) · [Workbook](../workbook/week-08.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (works in 60, stretches to 75) |
| **Type** | Teach |
| **Big idea** | Every rule has edge cases, and the two ways of being wrong — false alarms and misses — hurt completely different people. |
| **New vocabulary** | edge case · false alarm · miss · first match wins · labelled example |
| **Materials** | Printed Workbook Week 8 pages 1–4 · **the Breaker Card, cut off and kept in your pocket** · a plain sheet of paper and an envelope for the Week 9 seal · a pen you can both sign with · a board or big sheet · a ruler or tape measure if you have one |
| **Tech needed** | **None.** Paper and pencil only. |
| **Prep time** | 20 minutes the night before, 5 minutes on the day |

---

## 🎯 Lesson Objectives

By the end of this lesson the student can:

1. **Find an edge case for any rule** by taking its threshold and pushing a value right up against it from both sides.
2. **Tell a false alarm apart from a miss**, and name a specific person who is harmed by each.
3. **Fill a two-by-two grid** of what the rulebook predicted against what was true, and read the two error cells off it separately.
4. **Sharpen a vague rule** — "if it looks dodgy" — into a condition with a number in it that a computer could actually test.

Objective 2 is the one that carries the week. "It got it wrong" is not an acceptable answer by minute 60; the student should say *which kind* of wrong and *who pays*.

---

## 🧑‍🏫 What YOU Need to Know First

**Read this once, slowly. About 15 minutes. It is complete — you need nothing else, and no outside reading.**

### The one-sentence version

Rules do not fail because they were written badly; they fail because a rule always tests a **stand-in** for the thing you actually care about, and stand-ins break at the edges — so the real question is never "how do I stop being wrong?" but "which of the two ways of being wrong am I choosing?"

### Part 1 — First match wins, which is last week's cliffhanger

Last week ended with a question left deliberately unanswered: what happens on a rainy Monday, when Rule 1 and Rule 2 both fire?

> **First match wins** — the convention that you check rules from the top down, and the first rule that matches decides the answer. Every rule below it is skipped, even if it would have disagreed.

![First match wins: a rainy Monday never reaches rule 3](../figures/fig-w08-4-first-match-wins-ladder.svg)
*Figure 8.1 — Monday, 8 mm of rain. Rule 1 fires and everything below it never runs at all.*

Here is the thing to notice, and it is bigger than it looks. In that figure, **Rule 3 says "on time" and never gets a turn.** It is not outvoted. It is not overruled after consideration. It is simply never read.

So:

- **The order of the rules is part of the rulebook.** Two rulebooks with identical rules in a different order are different rulebooks and give different answers.
- **Rules near the top do the most damage**, because they fire before anything can moderate them.
- **Rules near the bottom can be dead** — never reachable, because something above always catches their cases first. In a fifty-rule book, several rules are usually dead and nobody knows which.
- **Who chose the order? A person. On a hunch.** That is the honest answer and the student should hear it.

There is one other convention worth knowing exists, so you aren't caught out: some systems collect *every* rule that fires and take a vote. That is a real design and it has its own problems (what do you do on a tie?). We use first-match-wins all year because it is simple, standard, and traceable — you can always point at the one rule that decided.

### Part 2 — Labelled examples, because you cannot score anything without them

> **Labelled example** — one piece of data with the correct answer written next to it.

`"WIN a FREE phone!!" → spam` is a labelled example. The message is the data; `spam` is the label.

The label is not free. Somebody had to read that message and decide. That person could be wrong, or tired, or could disagree with the next person — and every score you compute afterwards inherits their judgement. **A labelled example is a fact plus a human opinion, wearing the same coat.** Say that once, lightly, and move on; Week 15 comes back to it hard.

Today the student gets ten labelled messages and writes rules from them. That word "labelled" is doing real work: without the labels there is nothing to count and nothing to score.

### Part 3 — Edge cases are guaranteed, not unlucky

> **Edge case** — an example your rule gets wrong, usually because it sits right at the boundary of what you were imagining when you wrote the rule.

The clearest example in the world is a theme park height sign.

```
IF height_cm >= 140  THEN allow on the ride
```

It is testable, unambiguous, uses data you actually have, and looks completely fair. Now meet the edge cases:

- A 138 cm fourteen-year-old — turned away, though she is stronger than half the queue.
- A 141 cm six-year-old — allowed on, though the harness will not hold her, because she weighs very little.
- Someone measured in thick-soled trainers — 139 cm barefoot, 142 cm in shoes. Same child, two answers.

![A 138 cm child at a 140 cm ride](../figures/fig-w08-2-height-sign-138.svg)
*Figure 8.2 — Both arguments in that figure are correct. That is what makes it an edge case rather than a mistake.*

**Here is the mechanism, and it is the single most valuable idea in this file.** The ride operator does not care about height. They care about *whether the harness will hold this person safely*. They cannot measure that in a queue, so they measure something they can measure, that mostly goes along with it: height. Height is a **stand-in**.

Every rule you will ever write uses a stand-in:

| The rule measures | What you actually care about |
|---|---|
| height in centimetres | will the harness hold them |
| the word "FREE" in a message | is somebody trying to rob you |
| 3 or more absences | is this child in trouble at home |
| more than 30 characters | is this message from a stranger selling something |

**A stand-in agrees with the real thing in the middle and disagrees at the edges.** So edge cases are not bad luck and they are not evidence you wrote a sloppy rule. They are built into the arrangement. This is why "just fix the rule" never ends — and Week 10 is about what happens when you try.

**How to find an edge case on purpose**, which is the practical skill: take the threshold and step one unit either side of it. 139 and 141. 29 characters and 30 characters. 2.9 mm and 3.1 mm. Then ask whether the answer *should* flip there. It almost never should, and the two examples you just built are your edge cases.

![A rule boundary drawn on a number line](../figures/fig-w08-3-rule-boundary-number-line.svg)
*Figure 8.3 — Everybody far from the line is fine. Everybody near it is a coin toss with consequences.*

### Part 4 — The two ways of being wrong, and they are not equivalent

This is the heart of the lesson. "Wrong" is two different things wearing one word.

> **False alarm** — the rule raises the flag when it shouldn't have. It says *yes* and the truth was *no*.
>
> **Miss** — the rule fails to raise the flag when it should have. It says *no* and the truth was *yes*.

For a spam filter, the flag is "this is spam":

![The two ways of being wrong](../figures/fig-w08-1-false-alarm-miss-grid.svg)
*Figure 8.4 — Two cells right, two cells wrong, and the two wrong cells are nothing like each other.*

Read the grid out loud, cell by cell, because that is how it becomes usable:

|  | Rulebook said "spam" | Rulebook said "ham" |
|---|---|---|
| **Truly spam** | ✅ Caught it — the scam is blocked | ❌ **MISS** — a scam sits in your inbox looking normal |
| **Truly ham** | ❌ **FALSE ALARM** — your friend's good news goes in the junk bin | ✅ Left alone — the message arrives properly |

**Before you can use the words, you have to say which answer counts as raising the flag.** In spam filtering the flag is "spam". In a smoke detector the flag is "fire". At the ride the flag is "refuse — this person is unsafe". Get that backwards and false alarms and misses swap places, which is a genuine and very common confusion. Announce the flag out loud every single time. It takes four seconds and it prevents the most common error in the lesson.

**Now the part that matters more than the definitions: the two errors hurt different people.**

| The job | A false alarm costs | A miss costs | Which is worse |
|---|---|---|---|
| Spam filter | You lose a real message from a friend, and you never even know it existed | You see one scam and delete it | **The false alarm.** You can delete a scam. You cannot recover a message you never knew arrived. |
| Smoke detector | It shrieks while you make toast | The house burns down | **The miss**, obviously and enormously. |
| Exam cheating detector | An honest student is accused of cheating | One cheat gets away with it | **The false alarm**, by a mile. |
| Airport security scanner | Somebody's bag gets searched for nothing | A weapon gets on the plane | **The miss.** |

Notice that the answer changes completely from row to row. **There is no universal answer to "which error is worse", and anybody who gives you one is not thinking.** It depends on who is hurt and how badly, and that is a question about people, not about maths.

### Part 5 — You do not get to choose how many mistakes, only which kind

Take the spam rule `IF the message has 30 or more characters THEN spam` and start moving the number.

- **Loosen it** — 60 characters. Almost nothing gets flagged. False alarms nearly vanish. Misses pile up: every short scam sails through.
- **Tighten it** — 15 characters. Almost everything gets flagged. Misses nearly vanish. False alarms pile up: half your friends are in the junk bin.

![Tighten the rule and the errors move, they never vanish](../figures/fig-w08-5-tighten-loosen-tradeoff.svg)
*Figure 8.5 — Three settings of one rule. The total stays about the same; only the mix changes.*

**Every threshold in the world is a position on that slider, and somebody chose it.** They chose it by deciding which error they could live with — usually without writing down that they had decided anything at all.

This trade-off does not go away with better rules. It does not go away with machine learning. It does not go away with more data. It is a property of using a stand-in to guess something you cannot see, and it will still be true in Week 35 when the student is demonstrating a trained model at the AI fair. Say so today. It is one of the two or three ideas from this whole year that they will still be using at university.

### The three misconceptions you will meet today

**Misconception 1: "So we just need a better rule."** Overwhelmingly the most common response, and it is not stupid — it is the correct instinct applied to a problem that doesn't yield. Do not squash it. Let them try. When they patch the "!!" rule to fix the piano-exam message, ask them to re-check the scam that the "!!" rule was catching. Watching one patch open two holes is worth more than being told.

**Misconception 2: "wrong is wrong."** Students collapse false alarms and misses into a single count of mistakes. Break it with people, not logic: *"Your best friend messages you that she got into the team. It goes in the junk folder and you never see it. Now, separately: a scam text arrives and you read it and delete it. Same number of mistakes. Same day for you?"*

**Misconception 3: the grid gets filled in transposed.** They put the truth across the top and the prediction down the side, or they mix the two error cells up. The fix is mechanical and works every time: **write the flag word on the grid before filling anything in**, and read each row as a sentence — "truly spam, and the rulebook said ham: what do we call that?"

### How deep to go — and where to stop

**Go this deep:** first-match-wins and why order matters; labelled examples; edge cases and the stand-in mechanism; how to build an edge case from a threshold; false alarms versus misses with named victims; the grid; and the fact that you can only choose the mix, not the total.

**Stop before:**

| Do not raise today | Because |
|---|---|
| Accuracy as a formal number, training versus fresh scoring | **Week 9**, and it is the whole point of Week 9. Today you may count "1 out of 5" but do not turn it into a discussion about honest testing |
| The words *precision* and *recall* | Level 2. The ideas are here; the vocabulary is not. Your vocabulary budget this week is already five words |
| The phrase *confusion matrix* | You may say "grown-ups call this grid a confusion matrix" once if a student asks. Do not teach the term |
| Rule explosion, "why not just add more rules" as a *counting* argument | Week 10, deliberately. Today they should *feel* that patching fails. Week 10 puts numbers on it |
| Bias, and errors that fall unevenly on different groups of people | Week 31. If a student gets there on their own — "so the height rule is unfair to short adults" — praise it hard, write it on the parking lot, and say "that's Week 31, and you got there fourteen weeks early" |
| Probability, "60% likely to be spam" | Week 16 |

### If you have five spare minutes before class

Open your own spam or junk folder and look for a real message that shouldn't be there. Most people find one within ninety seconds, and it is often something that mattered. Then notice how long it had been sitting there unread. That is a false alarm, in your own life, with a real cost — and describing it out loud at minute 20 is worth more than any example I can print.

---

### 🧭 The Growing Map

Same figure, and this week the tinted tile has **not moved** — PATTERNS AND RULES is lit for the second
of its two weeks. Say that out loud, because it teaches them the map grows in chunks rather than weekly
hops, and because it is exactly what happened: Week 7 built the rule, Week 8 took it apart.

![The course map after Week 8: the same patterns and rules tile, now with its edges tested](../figures/fig-w08-0-where-this-fits.svg)

*Figure 8.0 — Week 8's version. Identical geometry to last week. What changed is the thread strip —
**model** and **evaluation** are both lit now — and the footer line underneath it.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask:** *"which bit of today is on this map?"* Expect *"we broke the rules"*, which is
   right. Then push once: *"and what did we do to the rulebook **before** we broke it?"* The answer is
   *we scored it* — and that is why a second thread lit up.
2. **Then the better question:** *"the box didn't move, so did we learn nothing today?"* Let somebody
   argue it out. The answer you want is that one tile can take two weeks, and that a rule you can
   write is not the same thing as a rule you can trust.
3. **Have them add nothing to their copy — have them say what changed instead**, in one sentence, while
   pointing at the bottom strip: *"same tile, week two, and evaluation lit up."* Then re-shade the same
   tile in pencil if they want it to look busier.

> **🧑‍🏫 Why this is worth two minutes.** False alarm and miss are two of the words this whole course
> hangs on, and today they arrive attached to a rule the learner wrote themselves. The map is what
> stops the lesson being filed away as "the day we argued about a ride queue".

**The six threads** along the bottom are the spine of all four levels. This week **model** and
**evaluation** are lit: the rulebook is the model, and counting the two kinds of wrong is evaluation.
They are shelves, not content — do not teach or test them.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Print Workbook Week 8, pages 1–4.**
  - Page 1: the ten labelled messages, the tally table, the rulebook frame.
  - Page 2: the Breaker scorecard and the empty two-by-two grid.
  - Page 3: the 138 cm homework.
  - Page 4: the five vague rules to sharpen.
- [ ] **Cut off the Breaker Card at the bottom of page 2 and put it in your pocket.** Same discipline as last week's Fresh Four. If the student reads the five breaker messages before writing their rules, the second half of the lesson is dead.
- [ ] **Read the five breaker messages out loud once, now, to yourself.** You have to deliver them one at a time with a straight face. Two of them are jokes at the rulebook's expense and you will smile — that's fine, but know which ones they are.
- [ ] **Write out the ten Week 9 envelope messages on a plain sheet of paper.** They are printed in the Answer Key at the bottom of this file under *The sealed ten*. Fold the sheet. **Do not seal it yet — you seal it in front of the student at the end of the lesson.** Put the folded sheet and an empty envelope in your bag.
- [ ] **Do the worked example yourself** — the eight ride queue riders, the grid, and the two threshold changes. Ten minutes with a pencil. The threshold-moving bit is the part you must have done by hand.
- [ ] **Read the Answer Key.** It contains the full tally, the expected rulebook, all fifteen traces and both grids.
- [ ] **Check the rainy-Monday question is still on the board** from last week. If it got wiped, write it back up before the lesson starts.

### 5 minutes on the day

- [ ] Board with room for a 2×2 grid drawn large.
- [ ] Workbook pages 1–4 out. **Breaker Card in your pocket.**
- [ ] Folded sheet of ten messages, plus the empty envelope and a signing pen, out of sight.
- [ ] Last week's rainy-Monday question visible.

### If something fails

| If this fails | Do this instead |
|---|---|
| **No printer** | Read the ten labelled messages aloud twice while the student writes them; they're short. Costs 6 minutes — take 4 from the worked example and 2 from the wrap. Keep the breakers oral anyway; they were always going to be read aloud. |
| **No envelope** | Fold the sheet in three, tape it shut along both edges, and both sign across the tape. The ceremony matters more than the stationery. A stapled paper bag works. |
| **The student writes rules you can't break with the five breakers** | Unlikely but possible if they invent a very narrow rule. Improvise: read their rule back and step one character either side of its threshold out loud. *"Your rule says 4 or more capitals. Here's a message with 3: 'HEY CALL ME'. Here's one with 4: 'OMG I WON'."* You can always build a breaker live from any threshold — that is the whole point of Part 3. |
| **They refuse to write down a wrong answer during the breaker round** | Say the line and mean it: "You are the computer right now, not the judge. The computer doesn't get to be embarrassed." If they still won't, you write it and they say it aloud. Do not let them silently correct the rulebook mid-round. |
| **You run out of time before the envelope** | Seal it anyway, even at the door, even in thirty seconds. Week 9 does not work without it. If the lesson has truly collapsed, seal it and both sign it before you leave the room — the *sealing*, witnessed, is the load-bearing part. |
| **No board** | The 2×2 grid works on a single sheet of A4 turned landscape, drawn with a ruler. Draw it large; you'll be pointing at cells for ten minutes. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | 🪝 **Hook** — "You're 138 centimetres. Argue with me." | The teacher plays the ride operator and refuses the student entry. |
| 8–26 | 🧠 **Concept** — Order, edges, and two kinds of wrong | First match wins · the stand-in · the two-by-two grid. |
| 26–40 | 🔍 **Worked Example Together** — The Ride Queue | Eight labelled riders, one grid, then move the threshold twice. |
| 40–60 | 🎲 **Activity** — Break My Rule | They build a three-rule spam book; you break it with five messages. |
| 60–70 | 🔑 **Wrap & Assign** | The "who pays" question, vocabulary, homework, and the sealing of the envelope. |

**Running 60 minutes?** Cut the worked example to 8 minutes — do the eight riders and the grid, and skip the two threshold moves (you can describe the result in one sentence). Cut the wrap to 6, but **do not cut the envelope**.
**Running 75?** Add extension question 2 or 4 from Differentiation, or let the student write five breakers aimed at *your* rulebook, which they will enjoy far too much.

---

### 🪝 Hook — "You're 138 centimetres. Argue with me." (0–8)

**Do this:** stand up. Hold out a flat hand at a bit above the student's head height, like a bouncer at a rope. Deliver this completely straight.

**Say this:**

> "Right. You've been queuing for forty minutes. It's the big ride, the one with the drop. You get to the front and I'm the person who checks.
>
> There's a sign next to me. It says: **you must be 140 centimetres tall to ride.** I measure you. You are 138.
>
> You're not getting on. Next, please."

**Do this:** wait. Do not soften it. Let the unfairness sit there for a few seconds.

**Say this:**

> "Now. Argue with me. Properly. Convince me I'm wrong."

Let them argue. Whatever they say, take it seriously and then hold your ground once. Common arguments and your reply:

- *"It's only two centimetres!"* → "Then where should I stop? 137? 130? Every centimetre is only one centimetre."
- *"I'm fourteen, I'm older than most of the queue!"* → "The sign doesn't say fourteen. It says 140."
- *"I'll stand on my toes."* → "Then the sign measures nothing at all and I might as well not have one."

**Say this:**

> "Here's the thing. **You're right, and so am I**, and that's not me being slippery — it's the actual situation.
>
> You're right that you're plenty strong enough and two centimetres is nothing. I'm right that the harness was tested at 140, and that if I bend the line for you I have to bend it for the next person, and the next, and then the line isn't anywhere.
>
> You are what's called an **edge case**. Not a mistake. Not a bug. You're a person standing right on the boundary of a rule, where the rule stops working and starts just hurting somebody."

**Do this:** write on the board:

```
THE RULE:      height >= 140  ->  allowed
THE EDGE CASE: 138 cm         ->  refused, and she was fine
```

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "Why does the sign measure height at all? What does the ride actually care about?" | "Whether the harness holds you" / "safety" | If they say "how old you are", push: "Would a very tall six-year-old be safe? Would a tiny adult?" You want them to arrive at *the harness*, i.e. something the sign can't measure. |
| "So can they measure 'will the harness hold you' in a queue?" | "No" | If they suggest a way (test the harness on everybody), take it seriously and cost it: forty minutes per rider. Land it: **you measure what you can, not what you want.** |
| "Give me a second edge case for the same rule. Somebody it lets on who shouldn't be." | "A really tall little kid" | If they're stuck, offer 141 cm and six years old. Then let them realise the rule is failing in *both* directions at once. |

**Say this:**

> "Two edge cases, opposite directions, one rule, thirty seconds of thinking. That's today. Every rule anyone has ever written has these, and today you're going to break your own on purpose."

---

### 🧠 Concept — Order, edges, and two kinds of wrong (8–26)

#### Part A — First match wins, and last week's cliffhanger (6 minutes)

**Do this:** point at the rainy-Monday question still on the board from last week.

**Say this:**

> "I owe you an answer. Last week you wrote a rulebook: Monday means late, three millimetres of rain or more means late, otherwise on time. And then a rainy Monday turned up and both rules fired at once, and I made you leave it.
>
> The answer is a convention, and it has a name: **first match wins.** You read top to bottom and the first rule that matches decides. Done. Stop reading.
>
> Now here's the part I actually care about."

**Do this:** draw a four-rung ladder on the board with an input falling in at the top. Fade or cross out rungs 2, 3 and the default, and write *never ran* beside each.

![First match wins: a rainy Monday never reaches rule 3](../figures/fig-w08-4-first-match-wins-ladder.svg)
*Figure 8.6 — The finished board. Three quarters of this rulebook did not run.*

**Say this:**

> "Look at rule 3. It says 'on time'. It *disagrees* with the answer we gave. And it never got a turn. Not outvoted — **never read.** The machine stopped three rungs above it.
>
> So three consequences, and they're all a bit unsettling.
>
> One: **the order is part of the rulebook.** Same rules, different order, different answers. Move rule 3 to the top and that exact same rainy Monday comes out 'on time' instead.
>
> Two: **the rules at the top do the most damage**, because nothing can moderate them. If your top rule is slightly wrong, it's wrong loudly and often.
>
> Three, and this is the strange one: **some rules are dead.** In a big rulebook there are always rules that can never fire, because something above them always catches those cases first. Fifty rules, and maybe six of them have never run in their lives, and nobody knows which six.
>
> And who decided the order? A person. Me, last week. I put Monday first because I found it first. That's the entire reason."

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "If I swap rules 1 and 2, does anything change for a rainy Monday?" | "The answer's the same, but rule 2 decided it" | If they say nothing changes at all, agree partly and sharpen: the *answer* is the same because both rules said "late". The *reason* changed. And when they disagree, the answer changes too. |
| "How could I find out if a rule in my book is dead?" | "Check if it ever fires" / "run all the data through and count" | This is a genuinely good, genuinely professional answer. Praise it: real engineers add a counter to each rule and look for the zeroes. |

#### Part B — Edge cases and the stand-in (6 minutes)

**Say this:**

> "Back to you at 138 centimetres. I want to name the machinery, because once you see it you'll see it everywhere.
>
> The sign measures height. The ride cares about whether the harness holds you. Those are **not the same thing** — height is a **stand-in**. It's the thing you can measure standing in for the thing you actually want to know.
>
> And here's the rule about stand-ins: **they agree with the real thing in the middle and disagree at the edges.** A 175 cm adult and a 95 cm toddler — height gets both of those completely right. It's the people between 130 and 150 where height starts lying.
>
> So edge cases aren't bad luck. They're not evidence I wrote a sloppy sign. **They are guaranteed, because every rule ever written uses a stand-in for something it can't see.**"

**Do this:** write these four on the board as two columns, and ask for the right-hand side each time before you write it.

| The rule measures | What we actually care about |
|---|---|
| height in centimetres | will the harness hold this person |
| the word "FREE" in a message | is somebody trying to rob me |
| 3 or more absences this month | is this child in trouble |
| more than 30 characters | is this a stranger selling something |

**Say this:**

> "Now the useful part — how to *find* an edge case on purpose, which is a skill, not a knack.
>
> **Take the threshold and step one unit either side of it.** That's it. My rule says 140. So look at 139 and 141. Your spam rule says thirty characters? Then find a message with 29 and one with 30. Rain of three millimetres? Look at 2.9 and 3.1.
>
> Then ask: **should the answer really flip between those two?** And the answer is almost always no — which means you've just built two edge cases in about fifteen seconds. That's what I'm going to do to your rulebook in half an hour, and now you know exactly how I'll do it."

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "Rule: `IF absences >= 3 THEN phone home`. Build me an edge case." | "A kid with 2 absences who's in real trouble" or "a kid with 3 absences because of a family holiday" | If they only give one side, ask for the other. Both directions exist for every threshold, always. |
| "Is there any threshold with no edge cases?" | "No" | If they propose one, take it seriously and step either side of it out loud. The genuine exception: a rule where the threshold *defines* the thing rather than standing in for it — "you must be 18 to vote" has no edge case about *voting age*, because the law simply is the number. Note it if a sharp student gets there; it's the seed of Week 10's "when rules are the right answer". |

#### Part C — Two ways of being wrong (6 minutes)

**Do this:** draw a big 2×2 grid on the board. Label the columns "rulebook said SPAM" and "rulebook said HAM". Label the rows "truly spam" and "truly ham". Then fill the cells one at a time as you talk.

![The two ways of being wrong](../figures/fig-w08-1-false-alarm-miss-grid.svg)
*Figure 8.7 — The finished board. Draw it big; you'll be pointing at it for ten minutes.*

**Say this:**

> "There are two ways a rule can be wrong and they are nothing like each other.
>
> A **false alarm** is when the rule shouts and it shouldn't have. It says yes, the truth was no. Your best friend messages you that she got into the team, your filter decides it's spam, and it goes into a folder you never open. You don't find out three weeks later. **You never find out at all.**
>
> A **miss** is when the rule stays quiet and it shouldn't have. It says no, the truth was yes. A message arrives saying your bank account has a problem, please verify. Polite. No capitals. No exclamation marks. It sails straight into your inbox looking exactly like a real message, because that's what the person who wrote it was trying to achieve.
>
> Now — one thing before you can use those words at all, and people get this wrong constantly. **You have to say which answer counts as raising the flag.** For a spam filter, the flag is 'spam'. For a smoke detector, the flag is 'fire'. At the ride, the flag is 'refuse this person'. Say the flag out loud *first*, every single time, or you'll swap false alarms and misses over and get everything backwards."

**Do this:** work the three jobs on the board as a table, asking for each verdict before you write it.

| Job | False alarm costs | Miss costs | Worse? |
|---|---|---|---|
| Spam filter | A real message, lost silently | One scam you delete | **false alarm** |
| Smoke detector | Shrieking during toast | House burns down | **miss** |
| Cheating detector | An honest student accused | One cheat gets away | **false alarm** |

**Say this:**

> "Look at the last column. It changes every row. **There is no answer to 'which mistake is worse' that works everywhere** — it depends entirely on who gets hurt and how badly, and that's a question about people, not maths.
>
> And here's the trap. You cannot get both errors to zero. Watch: I'll make my spam rule stricter to stop the scams getting through — and now half your friends are in the junk bin. So I loosen it to get your friends back — and the scams return. **You don't get to choose how many mistakes. You only get to choose which kind.**"

![Tighten the rule and the errors move, they never vanish](../figures/fig-w08-5-tighten-loosen-tradeoff.svg)
*Figure 8.8 — One rule, three settings. Ten mistakes, eight mistakes, ten mistakes. Only the mix moved.*

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "Airport bag scanner. Which error would you rather?" | "A false alarm — search the bag" | If they say miss, ask what a miss means here. Once "a weapon on the plane" is said out loud they change their mind unprompted. |
| "Your phone's face unlock. Which error would you rather?" | "A false alarm" — meaning it refuses *you* and you type your code | **This one is genuinely tricky and worth the time.** The flag here is "this is the owner". A miss means it fails to recognise you: annoying. A false alarm means it unlocks for your sibling: bad. So here you want to avoid the false alarm, which is the opposite of the spam answer. Same maths, opposite choice. |
| "Can a system have zero false alarms and zero misses?" | "No" | If they say yes: "Show me. Set the threshold anywhere you like and I'll find you a message on the other side of it." |

---

### 🔍 Worked Example Together — The Ride Queue (26–40)

**Do this:** write this table on the board. Explain the last column honestly: after the day ended, a safety engineer measured everyone properly — shoulder width, weight, the lot — and worked out who the harness would actually have held. That column is the **truth**. It is a set of **labelled examples**.

| # | rider | height_cm | rule says | truly safe? |
|---|---|---|---|---|
| 1 | A | 152 | allow | yes |
| 2 | B | 138 | refuse | **yes** |
| 3 | C | 141 | allow | **no** |
| 4 | D | 129 | refuse | no |
| 5 | E | 145 | allow | yes |
| 6 | F | 139 | refuse | no |
| 7 | G | 158 | allow | yes |
| 8 | H | 136 | refuse | **yes** |

**Say this:**

> "The rule is `IF height >= 140 THEN allow`, default refuse. And before we score anything: **what's the flag?** The sign's job is to catch people the harness won't hold. So the flag is **refuse**. Refusing somebody is the alarm going off."

**Do this:** fill the grid together, one rider at a time, out loud. Put the rider's letter in the cell.

|  | Rule refused (flag raised) | Rule allowed (no flag) |
|---|---|---|
| **Truly unsafe** | ✅ Caught: **D, F** (2) | ❌ **MISS: C** (1) |
| **Truly safe** | ❌ **FALSE ALARM: B, H** (2) | ✅ Fine: **A, E, G** (3) |

**Say this:**

> "Count it up. Right: two plus three, five. Wrong: three. Five out of eight.
>
> Now split the three wrong ones properly, because 'three wrong' tells you nothing about what happened to anybody.
>
> **Two false alarms — B and H.** Two people who were perfectly safe, sent away after forty minutes of queuing. B is your 138. H is 136.
>
> **One miss — C.** 141 centimetres, allowed on, and the harness wouldn't have held her. C is a six-year-old who is tall for her age and weighs very little.
>
> Which of those three would you rather the sign got wrong? Because B and H had a horrible afternoon, and C could have been hurt."

**Do this — the important part.** Now move the threshold twice and rebuild the counts. Do it on the board; do not just tell them.

**Threshold 130 — a loose rule:**

Everybody except D (129) gets on.

|  | Refused | Allowed |
|---|---|---|
| **Truly unsafe** | ✅ D (1) | ❌ **MISS: C, F** (2) |
| **Truly safe** | ❌ **FALSE ALARM: none** (0) | ✅ A, B, E, G, H (5) |

**Score 6 of 8. Zero false alarms, two misses.**

**Threshold 150 — a tight rule:**

Only A (152) and G (158) get on.

|  | Refused | Allowed |
|---|---|---|
| **Truly unsafe** | ✅ C, D, F (3) | ❌ **MISS: none** (0) |
| **Truly safe** | ❌ **FALSE ALARM: B, E, H** (3) | ✅ A, G (2) |

**Score 5 of 8. Three false alarms, zero misses.**

**Ask this:**

| Ask | Hoping for | If they say something else |
|---|---|---|
| "What happened to the mistakes as I moved the line?" | "They moved from one kind to the other" | If they focus on the total, that's fine and also true — the total barely moved (3, 2, 3). Praise it and then push: "And what changed a lot?" The *mix*. |
| "Which threshold should the park actually use?" | Ideally an argument, not a number | The honest answer is 150 or higher, because the park's worst outcome is a child getting hurt and three disappointed riders is survivable. Any answer with a *reason about who is hurt* gets full credit. A number with no reason gets none. |
| "Nobody at this park is 132 or 143. Does that matter?" | "You can't tell what happens there" | Excellent if they get it. Our data has gaps, so several thresholds are indistinguishable — the same discovery as last week, arriving in a place where somebody could get hurt. |

---

### 🎲 Activity — Break My Rule (40–60)

Full instructions in the next section. In brief: the student writes a three-rule spam rulebook from ten labelled messages and scores it. Then you read five messages built to defeat it, they run the rulebook mechanically, and everything goes into the grid.

**Do this at minute 40:** hand over Workbook page 1. Breaker Card stays in your pocket.

**Say this:**

> "Ten real-looking text messages, and next to each one, the truth — spam or ham. 'Ham' just means a normal message; it's an old joke that stuck.
>
> That's ten **labelled examples**: data with the right answer written next to it. Count the clues first — same as the bus — then write me three rules and a default. Eight minutes."

---

### 🔑 Wrap & Assign (60–70)

**Do this:** put the filled grid where you can both see it. Do not tidy it.

**Say this:**

> "Three things, and then a question I actually want you to think about.
>
> **One. Every rule has edge cases, and they're guaranteed.** Not because you wrote a bad rule — because every rule measures a stand-in for something it can't see. And you now know how to find them: take the threshold and step one either side.
>
> **Two. There are two ways of being wrong and they hurt different people.** A false alarm loses your friend's message and you never even know. A miss puts a scam in front of you looking completely normal. Your rulebook made three false alarms and one miss today.
>
> **Three. You don't get to choose how many mistakes, only which kind.** Every time you tightened a rule to stop one, you made more of the other."

**Ask this — the closing question, and give it real time:**

> "Last question, and there's no right answer. **Your email app has to choose.** It can be strict — it'll catch nearly every scam, and a few messages from your friends will vanish into the junk folder and you'll never see them. Or it can be relaxed — you'll never lose a real message, and a few scams will land in your inbox looking normal.
>
> Which one do you want? And here's the harder half: **who pays for your choice?**"

Take their answer seriously and then add the part they usually miss:

> "Whatever you pick — notice that *you* aren't the only person affected. If you choose relaxed, and one of those scams gets your grandmother's bank details because she's using the same app, she paid for your choice and she never got asked. **Somebody always chooses this, for a lot of people, and the people mostly don't know it happened.**"

**Do this — the envelope. Do not skip this, even if you are out of time.**

Take out the folded sheet. Hold it up. Say what it is without showing it.

> "Ten more messages. I wrote them last night. You have never seen them, and neither has your rulebook. They're going in here, and we're both signing across the flap, and we are not opening it until next week."

Seal it. Both sign across the flap. Put it somewhere visible for a week — on a shelf, on the fridge, not in a drawer.

> "Next week we open it. And you'll find out that the score you're proudest of is the one that doesn't count."

**Do this:** fill in the vocabulary box together.

| Word | The definition you're steering to |
|---|---|
| **edge case** | An example a rule gets wrong, usually right at its boundary |
| **false alarm** | The rule raises the flag when it shouldn't have — says yes, truth was no |
| **miss** | The rule stays quiet when it shouldn't have — says no, truth was yes |
| **first match wins** | Check rules top to bottom; the first one that matches decides |
| **labelled example** | A piece of data with the correct answer written next to it |

Then assign the homework as written below.

---

## 🎲 The Activity, In Full

### Break My Rule

**Time:** 20 minutes — 8 building, 7 breaking, 5 discussing
**Group size:** 1 student. With two, have one build the rulebook and the other write two extra breakers of their own; the rivalry does the motivating for you.
**The point:** to feel a rulebook that scores perfectly turn worthless in four minutes, and to count the two error types separately while it happens.

### Materials

- Workbook Week 8 page 1: ten labelled messages, the tally table, the rulebook frame
- Workbook Week 8 page 2: the Breaker scorecard and the empty 2×2 grid
- **The Breaker Card, cut off page 2, in your pocket**
- A pencil

### Part 1 — Build the rulebook (8 minutes)

The ten labelled examples they get:

| # | message | truth |
|---|---|---|
| 1 | `WIN a FREE phone!!` | spam |
| 2 | `CLAIM YOUR PRIZE NOW!!` | spam |
| 3 | `Free entry to win cash` | spam |
| 4 | `You have been selected for a reward, click the link` | spam |
| 5 | `URGENT: verify your bank account today` | spam |
| 6 | `see you at the bus stop` | ham |
| 7 | `Mum says dinner at 7:30` | ham |
| 8 | `did you finish maths?` | ham |
| 9 | `bring my charger back` | ham |
| 10 | `practice moved to 4pm` | ham |

**Step 1 — tally, don't guess.** Same discipline as last week. The table on their page has the clues listed and the counting left blank:

| clue | in spam (of 5) | in ham (of 5) | gap |
|---|---|---|---|
| contains `!!` | | | |
| contains `free` (any capitals) | | | |
| 30 or more characters | | | |
| contains `?` | | | |
| has an ALL-CAPS word | | | |

They must count characters for the third row. That is deliberate: it is fiddly, and it makes the threshold feel real.

**Step 2 — write three rules and a default.** Frame:

```
CONVENTION: first match wins, checked top to bottom.

RULE 1:  IF ______________________  THEN ________
RULE 2:  IF ______________________  THEN ________
RULE 3:  IF ______________________  THEN ________
DEFAULT: OTHERWISE                  THEN ________
```

Requirements said out loud: no adjectives, at least one rule with a number in it, and the default filled in.

The rulebook they will almost certainly write (and the one everything below assumes):

```
RULE 1:  IF the message contains "!!"                 THEN spam
RULE 2:  IF the message contains "free" (any capitals) THEN spam
RULE 3:  IF the message has 30 or more characters      THEN spam
DEFAULT: OTHERWISE                                     THEN ham
```

**Step 3 — score it on the ten.** It gets **10 out of 10.** Let them enjoy it for about fifteen seconds, then say:

> "Perfect score. And it means nothing at all, and I'll prove it in four minutes."

> **⚠️ Watch out:** if the student writes a *different* rulebook, that is completely fine and often better. The breakers still work, because every one of them attacks a general weakness — a real message that shouts, a scam that whispers, and a pair sitting either side of a length threshold. If their rules dodge one breaker, invent one live by stepping either side of their threshold, exactly as Concept Part B taught.

### Part 2 — The breaker round (7 minutes)

**Now take the card out of your pocket.** Read the messages **one at a time**, out loud. For each one:

1. The student writes down which rule fires first and what the rulebook says.
2. **They commit to it on paper before you say anything.**
3. Then you reveal the truth, and they mark it and write the error type.

| # | message | truth |
|---|---|---|
| B1 | `I PASSED MY PIANO EXAM!!` | ham |
| B2 | `Your parcel is delayed.` | spam |
| B3 | `Free period tomorrow?` | ham |
| B4 | `can you bring my charger today` | ham |
| B5 | `can you bring my charger back` | ham |

**The rule for this round, said before you start and enforced without mercy:**

> "You are the computer. Not the judge. If the rules give an answer you know is stupid, you write down the stupid answer. Being honest here is the entire point of the exercise."

![Five messages built to break the rulebook](../figures/fig-w08-6-breaker-scorecard.svg)
*Figure 8.9 — The finished scorecard. One right out of five.*

**Score: 1 out of 5.** Three false alarms, one miss, and **zero scams caught.**

**The pair to slow down on is B4 and B5.** Read them back to back:

```
"can you bring my charger today"   30 characters  ->  RULE 3 fires  ->  SPAM
"can you bring my charger back"    29 characters  ->  nothing fires ->  HAM
```

**Say this:**

> "Same person. Same charger. One word different. One character different. **One of those goes in the junk bin and one doesn't**, and there is no reason for it in the world except that I chose the number thirty and you happened to agree.
>
> That's an edge case, built on purpose, in about ten seconds. And I built it exactly the way I told you to: I found your threshold and I stepped one either side of it."

![A rule boundary drawn on a number line](../figures/fig-w08-3-rule-boundary-number-line.svg)
*Figure 8.10 — Messages as dots on a length line. Everybody far from the line is fine; the two marked with crosses are B4 at 30 and B2 at 23.*

### Part 3 — Fill the grid and count the two errors (5 minutes)

They fill the 2×2 grid on page 2 with the five breakers. **Announce the flag first: the flag is "spam".**

|  | Rulebook said spam | Rulebook said ham |
|---|---|---|
| **Truly spam** | ✅ caught: **none (0)** | ❌ **MISS: B2** (1) |
| **Truly ham** | ❌ **FALSE ALARM: B1, B3, B4** (3) | ✅ fine: **B5** (1) |

Then, out loud:

- **False alarms: 3.** Three real messages from real people, binned.
- **Misses: 1.** One scam, in the inbox, looking perfectly normal.
- **Scams caught: 0.** The rulebook's actual job, performed zero times.

**The closing discussion** (this is the part that matters, and it is the same question as the Wrap, asked smaller):

> "You've got three false alarms and one miss. Suppose you can only fix one kind. Which?"

Any answer is acceptable **if it names who is hurt**. Push once for the second half: *"And what does fixing it cost you in the other column?"*

### What "finished" looks like

- A tally table with both columns and a gap for every clue
- Three rules and a default, with no adjectives and at least one number
- 10 out of 10 written down on the training messages
- Five breakers scored **mechanically**, with the first-firing rule named for each
- A filled 2×2 grid with 3 false alarms and 1 miss counted separately
- One sentence naming which error they'd rather have and who pays

### Variation — easier

- **Give them the tally table already filled in.** They only choose which three clues become rules.
- **Two rules instead of three.** Drop the character-count rule; then B4 and B5 both come out ham, and the score is 2 of 5. The edge-case pair is lost, so build one live from their `!!` rule instead: `"OMG!!"` (fires, ham) against `"OMG!"` (doesn't fire, ham).
- **Do the first breaker together**, out loud, all the way through the grid, before handing over.
- **Skip the grid** and just tally false alarms and misses as two tally marks in the margin. The counting is the idea; the grid is the presentation.

### Variation — harder

- **Let them patch it.** Give four minutes. "Fix the piano-exam false alarm without losing message 1 or 2." The natural patch is `IF contains "!!" AND has an ALL-CAPS word THEN spam` — and it fails, because `I PASSED MY PIANO EXAM!!` is full of capitals. The next patch after that starts needing information the message doesn't contain. **This is Week 10's lesson, discovered early and honestly.**
- **They write the breakers, aimed at you.** Give them your own three-rule book, four minutes, and let them try. They will succeed, quickly, and enjoy it enormously. Then the real question: *"How long did that take you? Now — real scammers do exactly this, all day, professionally. What's a rulebook actually worth?"*
- **Order surgery.** Move Rule 3 to the top. Now `You have been selected for a reward, click the link` still fires (it's 51 characters) but so does `Free entry to win cash`? No — that's 22 characters, so it falls through to Rule 2. Have them find a message whose *answer* changes when the order changes, not just its reason. Answer in the key.
- **Count the harm, not the errors.** "Give a false alarm a cost in points and a miss a cost in points. Justify your numbers. Now re-score the five breakers in points instead of ticks." There is no right answer and the argument is the entire value.

---

## ❓ Questions Students Ask This Week

**"Why don't they just make the ride sign say 'must be 140cm OR over 12 years old'?"**
Real parks do exactly that sometimes, and it genuinely helps. But look at what you've done: you now need to know everyone's age, which means asking, which means being told the truth, which means someone checking. The rule got better *and* the system got bigger and slower — and it still has edge cases, they've just moved. Now it's the eleven-year-old who's 139 cm. **Every fix trades an edge case for a different edge case plus more complexity.** That trade is sometimes worth it. It is never free.

**"Can't we just write a rule for every edge case we find?"**
You can, and it works — for about five of them. Then two things happen. Your patches start contradicting each other, so you need rules about which rule wins. And the world moves: the scammer reads your rules by testing them, and writes the next message just outside them. Try the "harder" variation today and you'll feel it in four minutes. Week 10 does the arithmetic on exactly this, and the number is uncomfortable.

**"Is a false alarm always better than a miss?"**
No, and this is the question I most want you to get right. For your email, a false alarm is worse — you can delete a scam, but you can never read a message you didn't know arrived. For a smoke detector, a miss is catastrophically worse. For your phone's face unlock, a false unlock for your brother is worse than it failing to recognise you. **Same maths, three different answers**, because different people get hurt in different amounts. Anybody who tells you one of the two is always worse hasn't asked who's paying.

**"Who decides which mistake an app makes?"**
Somebody at the company, usually a small team, usually without telling anybody. It gets written into a threshold, and the threshold goes into an app used by millions of people who never got asked. That's not a conspiracy — it's just how software is built. But it does mean somebody chose, on your behalf, whether you'd rather lose your friend's message or see a scam. **When you build your booth in Week 34 you will be that somebody**, and I'm going to make you write down what you chose.

**"What's the best threshold for a spam filter?"**
**Nobody knows for sure, and here's why it isn't a cop-out.** There is no single best number, because "best" depends on how much you hate each error, and that's different for every person and every message. Real filters don't even use one fixed number any more — they learn from what you personally mark as spam, so your threshold and mine slowly drift apart. And here's the honest part: even the engineers who build these systems cannot tell you the right number. They pick one, measure what happens, and adjust. That's not a failure of cleverness; it's what the question is actually like.

**"If a rule got the right answer for a silly reason, does it still count?"**
It counts on the scoresheet and it should worry you. There's a message in next week's envelope that our rulebook marks as spam correctly — but only because it happens to be 31 characters long, not because of anything about the message. **A rule that's right for the wrong reason will betray you the moment the coincidence stops holding.** So when you score a rulebook, always check *which rule fired*, not just whether the answer was right. That habit is worth more than any single rule you'll write this year.

**"Do the rules in real apps look like ours?"**
The oldest ones did, almost exactly — lists of banned words and length checks, written by hand. Some parts of real systems still work that way, especially safety cut-offs where you must be able to explain every decision. But the part that actually catches spam now is learned from millions of labelled examples, and nobody can read it. Which means nobody can walk around it as easily as you walked around mine — and also that when it makes a mistake, nobody can point at the line that caused it. You traded one problem for another.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| During the breaker round they "correct" the rulebook's answer instead of writing what it says | Writing a wrong answer feels like being wrong | Say the line: "You're the computer, not the judge." Then make it concrete: "The computer doesn't know it's being silly. That's exactly what we're measuring." If it keeps happening, you hold the pen and they call out the rule number. |
| False alarms and misses get merged into "four mistakes" | It is genuinely simpler, and the word "wrong" covers both | Do not explain — dramatise. "Message one: your friend's piano news, gone forever, you never knew. Message two: a scam you read and deleted in two seconds. Same number of mistakes. Same day?" |
| The 2×2 grid is filled in transposed, or the two error cells are swapped | Four cells, two axes, and both axes use the same two words | Write the flag word on the grid first, then read each cell as a full sentence: "truly ham, and the rulebook said spam — that's the friend in the bin." Never let them fill a cell without saying the sentence. |
| They insist their rulebook is fine and the breakers are "unfair" | The breakers *are* unfair — that's the design | Agree completely and then turn it: "You're right, I cheated. I looked at your rules and worked around them. **Now: who else does that for a living?**" Land on spammers. The unfairness is the lesson. |
| They can't count the characters in a 30-character message reliably | It's genuinely fiddly, especially with spaces | Give them a rule for it: tap each character with a pencil tip and count in threes. Or just tell them the counts — the threshold idea matters, the counting doesn't. Both breaker messages' counts are in the key. |
| The lesson drifts into "spam filters are rubbish" | It's an easy and slightly satisfying conclusion | Correct it explicitly: real filters catch well over 99% of spam. **Our rulebook is bad; the idea isn't.** What makes real ones work is millions of labelled examples instead of ten, which is precisely the trade we make in Week 10. |
| The envelope gets forgotten | It's the last thing, and the wrap always runs late | Put it physically on top of your notes at minute 55 so you cannot miss it. If the lesson is dead and it's minute 69, seal and sign it at the door in twenty seconds. Week 9 does not work without it. |
| They ask, brilliantly, "isn't the height rule unfair to short people?" | Because it is, and they've spotted it | Praise it hard and hold the line: "That's Week 31, and you got there twenty-three weeks early." Write it on the parking lot where they can see you write it. Do not start that lesson today; you will not finish it. |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** the whole first-match-wins section down to one sentence and one traced input. Cut the threshold-moving half of the worked example. Keep the breaker round and the grid — that's the lesson.

**Reteach like this:** teach the two errors with *no table at all*, entirely as two stories about people, and get the student to tell the stories back. Story one: the friend's message in the junk bin. Story two: the polite scam in the inbox. Only when they can retell both, unprompted, draw the grid — and then fill it in as "which story is this?" Four cells, four stories.

**Reduce the load:** give the tally table pre-filled and the rulebook pre-written. Do the breaker round orally, with you writing. Their only job is to say the rule number and then say "false alarm" or "miss".

**The minimum acceptable outcome for today:** they can define an edge case in their own words, they can give one example of a false alarm and one of a miss with a person in each, and they can say that fixing one causes more of the other. That is the whole week in three sentences.

### If they are flying

1. **"Fix the piano-exam false alarm."** Four minutes, real attempt. Their patch will be `"!!" AND an ALL-CAPS word`, which fails on the very message it's meant to fix. Then: "What information would you need that isn't in the message?" (Who sent it. Whether they're in your contacts.) **That's the answer, and it means the rulebook has to get bigger, not smarter.**
2. **"Find a message whose answer changes if Rule 3 moves to the top."** Answer in the key: any 30+ character message that also contains `free` or `!!` in a *ham* context. `Are you free on Saturday afternoon?` (35 characters, contains "free") comes out spam either way — but the *reason* changes. To change the answer you need a rule that outputs ham, which their book doesn't have. **That discovery — "I can't change an answer because all my rules point the same way" — is a genuinely sophisticated finding.** Ask them to add a ham rule and try again.
3. **"Put a cost on each error."** Assign points to a false alarm and to a miss, justify the numbers, and re-score the five breakers as a total cost instead of a count. Then re-score with the costs swapped. There is no correct answer; the argument is the point, and it's the honest version of what a real engineering team does.
4. **"What's the smallest change to my threshold that makes B4 and B5 agree?"** Move it to 31 or above and both come out ham. Then the sting: what else did you just let through? Anything 30 characters long, which is most polite scams. **Every threshold move is paid for somewhere.**
5. **"Design a rule with no edge cases."** They can't, and the *attempt* is what teaches. The one honourable answer: a rule where the number *defines* the thing instead of standing in for it — "you may vote at 18" has no edge case about voting age, because the law is the number. Distinguishing "the rule describes the world" from "the rule is the world" is Week 10 thinking.

### If they won't engage today

**Play the villain properly.** The whole lesson works as a game where you are trying to beat them. Lean into it: "I'm going to break whatever you write. Bet you can't stop me." Adversarial framing engages students who will not do a worksheet, and it is *also* exactly what real spam is.

**Go straight to their own junk folder.** With permission, look at a real inbox — theirs, or yours. Find a real message that shouldn't be in the junk folder, and a real scam that shouldn't be in the inbox. Two real examples, ninety seconds, and no worksheet.

**Or shrink to two sentences.** "Your friend's message goes in the bin and you never see it. Or a scam turns up in your inbox and you delete it. Which would you rather?" Then: "Why can't we have neither?" That is a complete and honest version of this lesson in two minutes. Take it and go.

**Do not skip:** the B4/B5 pair, and the envelope.

---

## ✅ Assessing Understanding

Do these in the last five minutes. Exact wording below.

### Check 1 — Build an edge case (60 seconds)

> "Here's a rule: `IF a parcel weighs 5 kg or more THEN charge extra postage`. Give me an edge case, and tell me how you found it."

**A good answer looks like:** "A parcel that's 4.9 kg — it's basically the same as a 5 kg one but it's free. I found it by going just under the threshold."
**A weak answer looks like:** "A really heavy parcel." Push: *"Does the rule get that one wrong?"* No — it gets it right. Steer them to the boundary. The *method* is what you're assessing.

### Check 2 — Name the error and the victim (90 seconds)

Read these three aloud, one at a time. For each: **false alarm or miss, and who is harmed?**

1. "The smoke alarm goes off while you make toast." → **False alarm.** Harmed: everybody in the house, mildly, and worse — someone might take the battery out.
2. "A scam text lands in your grandmother's inbox looking like a real bank message." → **Miss.** Harmed: your grandmother, possibly badly.
3. "An honest student's essay is flagged as copied." → **False alarm.** Harmed: the student, seriously, and they may not be believed.

**A good answer:** all three named correctly with a specific person in each.
**A weak answer:** correct names but "the person" as the victim. Push for who *specifically*, because the whole idea lives in the specifics.

### Check 3 — The trade-off (45 seconds)

> "I've made my spam filter stricter so no scams get through. What have I just done to my friend's messages, and why?"

**A good answer looks like:** "More of them will end up in the junk folder. You can't stop the misses without causing false alarms."
**A weak answer looks like:** "Nothing — it's better now." Reteach with the slider: draw the three panels from Figure 8.8 and count with them.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Says "it got it wrong" without distinguishing the two kinds. Cannot build an edge case. Corrects the rulebook's answers during the breaker round. |
| **2 — Emerging** | Names false alarm and miss when the grid is in front of them, but swaps them about half the time. Finds an edge case with prompting. Fills the grid with help. |
| **3 — Secure** | Runs the rulebook mechanically and writes down wrong answers without flinching. Fills the grid unaided with the flag named first. Counts the two errors separately. Builds an edge case by stepping either side of a threshold. **Target for Week 8.** |
| **4 — Strong** | Also explains the stand-in idea — that the rule measures one thing and cares about another. Argues which error is worse for a specific job, with a named victim. Predicts what tightening a rule will cost. |
| **5 — Exceptional** | Notices that patching one rule damages another that was doing useful work. Says unprompted that somebody chose the threshold and the people affected weren't asked. Spots a right-answer-wrong-reason row and says why it should worry them. |

---

## 📤 Homework to Assign

**Workbook Week 8, pages 3 and 4.**
**Time: 45–60 minutes across the week.**

**Say this:**

> "Two jobs, and they're both writing jobs this week rather than counting jobs.
>
> **Page 3 — the 138 centimetre argument, both sides.** You were the one turned away today, so you've got the easy half. I want you to write the ride operator's side *properly* — not a straw man, not a cartoon villain. Their best possible argument, in their words. Then yours. Then one honest sentence: **is there any rule that would have been fair to both of you?**
>
> And then the question underneath: **who pays for each choice?** If the sign says 140, who pays? If it says 130, who pays? Name a person each time, not 'people'.
>
> **Page 4 — sharpen five vague rules.** Five rules that are useless as written. 'If it looks dodgy.' 'If the student is often late.' Rewrite each one so a computer could run it. Three requirements per rule, and I'll be checking all three:
>
> **One**, it must contain a number or an exact match — no adjectives, ever. **Two**, one sentence on where your number came from. 'I made it up, it seemed about right' is a completely honest and acceptable answer, and it's better than pretending. **Three** — and this is the new bit — **give me one edge case your new rule creates.** You know how to find them now: take your threshold and step one either side.
>
> That third requirement is the whole homework. Anyone can put a number in a rule. Knowing what your number just did to somebody standing next to it is the part that took us an hour today."

**What to check when it comes in:** the operator's argument is genuinely reasonable and not a caricature; both "who pays" answers name a specific person; all five sharpened rules contain a number or an exact match; every number has a stated origin; and every rule has an edge case built by stepping across its own threshold.

---

## 🔑 Answer Key

### Lesson questions

**Hook — "What does the ride actually care about?"**
Whether the harness will hold this person safely. Height is a stand-in for it, because you cannot test a harness on every rider in a queue.

**Hook — "Give me a second edge case."**
A 141 cm six-year-old who weighs very little: allowed on by the rule, and unsafe. The rule fails in both directions at once — that is normal, not a special disaster.

**Concept A — "If I swap rules 1 and 2, does anything change for a rainy Monday?"**
The answer stays "late", because both rules say late. The *reason* changes — rule 2 decides instead of rule 1. Order only changes the answer when the rules disagree; it always changes the explanation.

**Concept A — "How could I find out if a rule is dead?"**
Run all your data through and count how many times each rule fires. A rule with a count of zero has never decided anything. Real engineers do exactly this.

**Concept B — an edge case for `IF absences >= 3 THEN phone home`.**
Two directions, both valid: a child with 2 absences who is in serious trouble (missed, no call) and a child with 3 absences because of a family wedding (false alarm, call made for nothing).

**Concept B — "Is there any threshold with no edge cases?"**
Essentially no — except when the number *is* the thing rather than standing in for it. "You may vote at 18" has no edge case about voting age, because the law defines it. Every rule that *predicts* something has edge cases.

**Concept C — face unlock, which error would you rather?**
The flag is "this is the owner". A miss (it doesn't recognise you) is annoying: you type your code. A false alarm (it unlocks for your sibling) is a security failure. So here you avoid the **false alarm** — the opposite of the spam answer. Same structure, different victim, different choice.

**Concept C — "Can a system have zero of both?"**
No. Any threshold has examples sitting on both sides of it that are labelled the other way. Moving the line moves which ones.

### Worked Example — the Ride Queue

**The flag is "refuse".** The sign's job is to catch riders the harness won't hold.

**Threshold 140 (the actual rule):**

| # | height | rule says | truly safe | outcome |
|---|---|---|---|---|
| 1 | 152 | allow | yes | ✅ correctly allowed |
| 2 | 138 | refuse | yes | ❌ **false alarm** |
| 3 | 141 | allow | no | ❌ **miss** |
| 4 | 129 | refuse | no | ✅ correctly refused |
| 5 | 145 | allow | yes | ✅ correctly allowed |
| 6 | 139 | refuse | no | ✅ correctly refused |
| 7 | 158 | allow | yes | ✅ correctly allowed |
| 8 | 136 | refuse | yes | ❌ **false alarm** |

**Score 5 of 8. 2 false alarms (B, H), 1 miss (C).**

**Threshold 130:** only D (129) refused.
Correct: A, B, E, G, H allowed and safe (5) + D refused and unsafe (1) = **6 of 8.**
**0 false alarms, 2 misses (C at 141 and F at 139, both allowed and unsafe).**

**Threshold 150:** only A (152) and G (158) allowed.
Correct: A, G allowed and safe (2) + C, D, F refused and unsafe (3) = **5 of 8.**
**3 false alarms (B, E, H — all safe and refused), 0 misses.**

**The pattern, which is the whole point:**

| Threshold | False alarms | Misses | Total wrong | Score |
|---|---|---|---|---|
| 130 (loose) | 0 | 2 | 2 | 6 of 8 |
| 140 (middle) | 2 | 1 | 3 | 5 of 8 |
| 150 (tight) | 3 | 0 | 3 | 5 of 8 |

**The total barely moves — two, three, three — while the mix flips completely, from all-misses to all-false-alarms.** That is Figure 8.8 in real numbers.

And note the trap in that table, because a sharp student will find it: the *loose* rule scores best, 6 out of 8. On eight riders, with two of them near the boundary, the score is not stable enough to choose a safety threshold with. **A park that picked 130 because it scored best on eight riders would be choosing a policy about injured children on the basis of two rows of data.** That is a genuinely important thing to say out loud.

**Which threshold should the park use?** A defensible answer must argue about harm, not accuracy. The strongest case is for 150 or higher: three disappointed riders is recoverable, an injured six-year-old is not. Accept any answer with a named victim and a reason. Reject a bare number.

### Activity — the tally table

| clue | in spam (of 5) | in ham (of 5) | gap |
|---|---|---|---|
| contains `!!` | 2 (#1, #2) | 0 | **2** |
| contains `free` (any capitals) | 2 (#1, #3) | 0 | **2** |
| 30 or more characters | 2 (#4 = 51, #5 = 38) | 0 | **2** |
| contains `?` | 0 | 1 (#8) | 1 (backwards) |
| has an ALL-CAPS word | 3 (#1 `WIN`/`FREE`, #2 `CLAIM YOUR PRIZE NOW`, #5 `URGENT`) | 0 | **3** |

**Character counts** for the two long ones, in case a student challenges you: `You have been selected for a reward, click the link` = **51**. `URGENT: verify your bank account today` = **38**. Every ham message is 21–23 characters.

**Note for the teacher:** the ALL-CAPS clue has the biggest gap (3) and is *not* one of the three rules. That is deliberate and worth saying if the student notices — it overlaps almost entirely with `!!`, so adding it would catch nothing new. **The biggest gap is not automatically the best rule.** If your student chooses it instead of one of the three, their rulebook still scores 10 out of 10; check it with them.

### Activity — the rulebook scored on the ten training messages

```
RULE 1:  IF contains "!!"                   THEN spam
RULE 2:  IF contains "free" (any capitals)  THEN spam
RULE 3:  IF 30 or more characters           THEN spam
DEFAULT: OTHERWISE                          THEN ham
```

| # | message | chars | First rule to fire | Says | Truth | ✓/✗ |
|---|---|---|---|---|---|---|
| 1 | `WIN a FREE phone!!` | 18 | RULE 1 (`!!`) | spam | spam | ✅ |
| 2 | `CLAIM YOUR PRIZE NOW!!` | 22 | RULE 1 (`!!`) | spam | spam | ✅ |
| 3 | `Free entry to win cash` | 22 | RULE 2 (`Free`) | spam | spam | ✅ |
| 4 | `You have been selected for a reward, click the link` | 51 | RULE 3 (51 ≥ 30) | spam | spam | ✅ |
| 5 | `URGENT: verify your bank account today` | 38 | RULE 3 (38 ≥ 30) | spam | spam | ✅ |
| 6 | `see you at the bus stop` | 23 | DEFAULT | ham | ham | ✅ |
| 7 | `Mum says dinner at 7:30` | 23 | DEFAULT | ham | ham | ✅ |
| 8 | `did you finish maths?` | 21 | DEFAULT | ham | ham | ✅ |
| 9 | `bring my charger back` | 21 | DEFAULT | ham | ham | ✅ |
| 10 | `practice moved to 4pm` | 21 | DEFAULT | ham | ham | ✅ |

**Score: 10 out of 10 = 100%.**

**And it means nothing.** These are the ten messages the rules were written *from*. Do not explain why today — that is Week 9's entire job. Say only: "Perfect score, zero information. Next week you'll find out why."

### Activity — the five breakers

| # | message | chars | First rule | Says | Truth | Result |
|---|---|---|---|---|---|---|
| B1 | `I PASSED MY PIANO EXAM!!` | 24 | RULE 1 (`!!`) | spam | ham | ❌ **FALSE ALARM** |
| B2 | `Your parcel is delayed.` | 23 | DEFAULT | ham | spam | ❌ **MISS** |
| B3 | `Free period tomorrow?` | 21 | RULE 2 (`Free`) | spam | ham | ❌ **FALSE ALARM** |
| B4 | `can you bring my charger today` | **30** | RULE 3 (30 ≥ 30) | spam | ham | ❌ **FALSE ALARM** |
| B5 | `can you bring my charger back` | **29** | DEFAULT | ham | ham | ✅ correct |

**Score: 1 out of 5 = 0.2 = 20%.**
**3 false alarms · 1 miss · 0 scams caught.**

**The grid, with the flag = "spam":**

|  | Rulebook said spam | Rulebook said ham |
|---|---|---|
| **Truly spam** | 0 | **1** (B2) |
| **Truly ham** | **3** (B1, B3, B4) | 1 (B5) |

**Why each breaker breaks it — the design behind them:**

- **B1** is a real message that shouts. The `!!` rule assumed only spam gets excited. Eleven-year-olds get excited constantly.
- **B2** is a scam that whispers. No capitals, no exclamation marks, no trigger words, 23 characters. **This is what real scams look like, precisely because rulebooks like ours exist.** There is no word in it that isn't also in ordinary messages.
- **B3** is `free` in the school-timetable sense. The word carries two completely different meanings and the rule only knows one.
- **B4 and B5** are the pair. 30 characters and 29 characters. Same person, same charger, one word different, opposite verdicts. **Built in ten seconds by stepping either side of the threshold.**

### Activity — harder variation: moving Rule 3 to the top

Re-scoring the ten training messages with the order `RULE 3 → RULE 1 → RULE 2 → DEFAULT`:

Every answer stays the same. Message 4 and 5 already fired on Rule 3; messages 1, 2, 3 are all under 30 characters so Rule 3 doesn't touch them; all the hams are 21–23 characters. **Ten out of ten, again, with a different reason for two rows.**

The finding to lead a strong student to: **you cannot change an answer by reordering, because every rule in this book outputs the same verdict — spam.** Order only changes answers when rules disagree, and this rulebook contains no rule that says "ham". Ask them to add one — for example `IF contains "?" THEN ham` — and *then* reorder. Put the `?` rule at the top and B3 (`Free period tomorrow?`) flips from spam to ham, fixing a false alarm. Put it at the bottom and nothing changes at all. **Same rule, two positions, one useful and one dead.**

### Workbook Week 8, page 3 — the 138 cm write-up

**The ride operator's best argument** (full credit needs it to be genuinely reasonable):

> "The harness on this ride was tested and certified at 140 centimetres. I did not choose that number and I cannot change it. If I let a 138 cm rider on because she looks strong, then tomorrow I have to decide about 137, and 135, and a child whose parent insists she's nearly 140, and I will be making a safety judgement in four seconds with a queue of eighty people behind me. I am not qualified to do that and neither is anybody else at the gate. The line has to be somewhere, it has to be the same for everyone, and it has to be a number I can measure in three seconds. Two centimetres is exactly where I have to stop, and it is not personal."

**The 14-year-old's best argument:**

> "I am fourteen years old. I am stronger than most of the people you just let on, and I understand the safety instructions better than the eight-year-olds in front of me. The number 140 is not measuring whether I'm safe — it is measuring my height, and it is using my height to guess at my safety, and for me that guess is simply wrong. You can see with your own eyes that it is wrong. The rule was written for an average person and I am not average, and being punished for that is not the same thing as being kept safe."

**"Is there a rule fair to both?"** Full-credit answers accept that there isn't a perfect one and then propose something honest: a second route in ("140 cm **or** aged 12 and over"), a proper assessment on request, or a rule based on weight and shoulder width instead of height. Every one of these has its own edge case, and **saying so is required for full credit.** An answer that claims to have solved it has missed the lesson.

**"Who pays for each choice?"**

| The sign says | Who pays |
|---|---|
| 140 cm | The 138 cm fourteen-year-old — a ruined afternoon, in public, in front of a queue. Paid immediately and visibly. |
| 130 cm | The 141 cm six-year-old who gets on and is hurt. Paid rarely, terribly, and invisibly until it happens. |

**The marking point:** naming a *specific person* both times. "People who are too short" earns half credit. And the strongest answers notice the asymmetry — one cost is small, frequent and visible; the other is rare, severe and hidden. **That asymmetry is exactly why safety rules are set tight.**

### Workbook Week 8, page 4 — sharpen five vague rules

Each answer needs three parts: the sharpened rule, where the number came from, and one edge case.

**(a) `IF the email looks dodgy THEN spam`**

> **Sharpened:** `IF the sender is not in my contacts AND the message contains 2 or more links THEN spam`
> **Where the numbers came from:** ordinary personal messages almost never contain two links; scams usually do. Two is a guess in that gap.
> **Edge case:** a real message from a new classmate sending you two links for a group project. Not in contacts, two links, straight to the junk bin. **False alarm.**

**(b) `IF the student is often late THEN phone home`**

> **Sharpened:** `IF late 3 or more times in the last 20 school days THEN phone home`
> **Where the numbers came from:** three separates a bad week from a habit; twenty days is about a month of school, so the count can't accumulate forever.
> **Edge case:** a student late exactly twice, both times because she takes her little brother to a different school first. Nobody phones, nobody finds out, and she's the one who most needed the call. **Miss.**

**(c) `IF the photo is blurry THEN reject it`**

> **Sharpened:** `IF the image is smaller than 400 × 400 pixels OR more than 60% of pixels are pure black or pure white THEN reject it`
> **Where the numbers came from:** 400 × 400 is roughly the smallest size a face is recognisable at on a screen; the black/white check catches photos taken with the lens covered or straight into a light.
> **Edge case:** a deliberately high-contrast black-and-white photograph — an excellent photo, rejected by the second clause. **False alarm.**

**(d) `IF the parcel is heavy THEN charge extra`**

> **Sharpened:** `IF weight_kg >= 5 THEN charge extra`
> **Where the numbers came from:** the courier's own van-loading guidance says one person shouldn't repeatedly lift more than 5 kg. Not invented — looked up. Say so.
> **Edge case:** a 4.9 kg parcel goes free and a 5.0 kg parcel costs more. The two parcels are identical to anybody carrying them. **A pure boundary edge case, found by stepping either side.**

**(e) `IF the video is too long THEN don't watch it`**

> **Sharpened:** `IF duration_minutes > 20 AND minutes_until_bedtime < 40 THEN don't watch it`
> **Where the numbers came from:** both made up, honestly — 20 minutes is about one episode and 40 leaves time to clean your teeth. A different person would pick different numbers and would not be wrong.
> **Edge case:** a 21-minute video with 45 minutes until bedtime is allowed; a 19-minute video with 35 minutes left is also allowed; but a 21-minute video with 39 minutes left is banned. **Two thresholds means edge cases along two different edges**, and spotting that is the best possible answer on this page.

**General marking rule for page 4:** no adjectives anywhere; every rule contains a number or an exact match; every number has a stated origin (and "I made it up" is honest and acceptable); every edge case is built by crossing the rule's own threshold, not by inventing an unrelated weird case.

### The sealed ten

**These are the ten messages you write out, fold and seal in front of the student at the end of this lesson. Do not show them.** Week 9 opens the envelope and scores them.

| # | message | truth |
|---|---|---|
| 11 | `Reminder: dentist at 4pm` | ham |
| 12 | `WINTER SALE! 70% off everything` | spam |
| 13 | `I won the match!! So happy` | ham |
| 14 | `Are you free after school?` | ham |
| 15 | `Verify your account now` | spam |
| 16 | `Click the link I sent for the project` | ham |
| 17 | `U have won 5000!! Reply CLAIM` | spam |
| 18 | `whats the answer to q7` | ham |
| 19 | `Congratulations on your exam results!` | ham |
| 20 | `Your parcel could not be delivered, click here` | spam |

Write the messages **and the truths**, both, on the sheet. Five spam, five ham. Do not write anything else on it — no rules, no hints, no score. Fold it, seal it, and both sign across the flap.

**For your own confidence:** this rulebook will score **5 out of 10** on these, with 4 false alarms and 1 miss. The full trace is in Week 9's Answer Key. You do not need to look at it now, and it is slightly more fun if you don't.

---

## 🔮 Next Week Preview

Next week is the Term 1 checkpoint, and it opens with the envelope. The student scores their rulebook on the ten sealed messages, one row at a time with no skipping, and writes the result next to the 100% they got on their own ten. The gap is fifty points. We do not explain it away — we sit with it, compute accuracy three ways with the long division written out, and name the idea that makes the whole rest of the year work: **the only honest score comes from examples the rulebook has never seen.** Then a twelve-question closed-book quiz on everything since Week 1, marked together out loud, with the week number written beside every wrong answer so the output is a list of weeks to revisit rather than a grade.

**Prep early:** three things. **One** — the envelope must be somewhere visible and unopened. If it goes missing you can rewrite it from the list above, but say honestly that you rewrote it; the whole exercise runs on trust. **Two** — print the quiz (Workbook Week 9, page 3) but keep it face down; it is closed-book and it needs to feel like it. **Three** — have last week's and this week's workbook pages to hand, because the marking phase involves flipping back to find which week an answer came from.

---

[⬅ Week 7](week-07.md) · [Course Home](../README.md) · [Week 9 ➡](week-09.md) · [Student Guide](../student-guide/week-08.md) · [Workbook](../workbook/week-08.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
