# Week 10 — The Rule Explosion: Why Nobody Writes 258 Rules

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (works in 60 if you cut the Worked Example to the 258 count only) |
| **Type** | 🟨 Project week — the concept is short, the build is long |
| **Big idea** | Adding rules to cover exceptions grows faster than the exceptions do, and that wall is exactly why machine learning had to be invented. |
| **New vocabulary** | check · rule explosion · exponential growth · the machine learning trade |
| **Materials** | 4 sheets of ordinary A4 paper · a calculator (phone is fine) · the student's Rulebook vs Reality folder from Weeks 7–9 · the sealed envelope of 10 fresh messages · pencil · ruler |
| **Tech needed** | **None required.** A spreadsheet (Google Sheets or Excel) is a nice-to-have for the extension only. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Before you read any further:** the student must still have the **sealed envelope of 10 fresh messages** from Week 9, unopened. If it has been opened, read the fallback in the Prep Checklist. This is the one thing that can quietly ruin the lesson.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Show by doubling** that *n* yes/no checks produce 2 to the power *n* situations, having filled in the table from 1 to 30 themselves.
2. **Explain rule explosion in their own words**, using a number they calculated themselves — not one you told them.
3. **State the machine learning trade**: you give up writing rules, and instead you supply labelled examples.
4. **Name one task they personally cannot write rules for**, and say precisely where the rules fall apart.

Observable evidence: a completed 1-to-30 doubling table in the workbook, a scored 10-message table with a fraction and a percentage, and a spoken sentence beginning "I stopped adding rules because…".

---

## 🧑‍🏫 What YOU Need to Know First

You do not need to know anything about AI to teach this. You need to know one piece of arithmetic and one idea. Both are below, in full.

### 1. The arithmetic: doubling

A computer program that follows instructions is built from **checks**. A check is a question with a yes/no answer:

- Does this message contain the word "free"?
- Does it have a link in it?
- Is the sender in my contacts?

Each check has 2 possible answers. Two checks together have 2 × 2 = 4 possible combinations. Three checks have 2 × 2 × 2 = 8. Write out all eight if it helps — the student will:

| # | free? | link? | known sender? |
|---|---|---|---|
| 1 | no | no | no |
| 2 | no | no | yes |
| 3 | no | yes | no |
| 4 | no | yes | yes |
| 5 | yes | no | no |
| 6 | yes | no | yes |
| 7 | yes | yes | no |
| 8 | yes | yes | yes |

That is the whole mathematics of this lesson: **each new check doubles the number of situations.** Written compactly, *n* checks give **2ⁿ** situations. Say "two to the power n" out loud; the student has met powers in maths.

Here is what doubling does when you keep going.

![The doubling staircase](../figures/fig-w10-1-doubling-staircase.svg)
*Figure 10.1 — Eight even-looking steps and you are already at 256. Thirty steps is over a billion.*

The figure is drawn with **even steps on purpose**. That is the trap in your own head: doubling *feels* like steady progress and it is not. From 3 checks to 30 checks you multiplied the questions by ten and the situations went from 8 to 1,073,741,824.

**The single most striking fact in this lesson — memorise it, it wins the room:**

> Going from 29 checks to 30 checks adds **536,870,912** brand-new situations.
> Every single one of checks 1 to 29, added up together, only ever created **536,870,911** situations.
>
> **Check 30 on its own creates more new situations than all twenty-nine checks before it, combined. By exactly one.**

Check the arithmetic yourself so you can say it with confidence: after 29 checks you have 2²⁹ = 536,870,912 situations. Before check 1 you had exactly 1 situation ("no questions asked"). So checks 1 to 29 created 536,870,912 − 1 = 536,870,911 situations between them. Check 30 doubles 536,870,912 to 1,073,741,824, adding 536,870,912. One more than all its predecessors put together. That is not a coincidence or a trick — it is true at every step of any doubling sequence, and it is the cleanest possible statement of why you cannot win this race.

### 2. Why the title says 258

Because the number is absurd, and because it is real. Here is where it comes from, and you should show this working to the student:

```
8 yes/no checks                    ->  2^8 = 256 situations
a rulebook that covers all of them ->  256 rules
plus one DEFAULT line ("otherwise...")     +1
plus one line saying which rule wins first +1
                                       -----
                                        258 lines
```

Eight checks is *nothing*. A person can hold eight questions in their head. And it already needs a document longer than this teacher guide's answer key. The load-bearing number is **256 = 2⁸**; the extra two lines are the housekeeping every rulebook needs. Be honest with the student about that — "256 is the maths, 258 is the maths plus the two boring lines."

### 3. Why the count is not even the worst part

If counting were the only problem, a determined person with a big enough team could grind through it. Three other things make it hopeless, and the third is the killer.

| # | The problem | What it looks like |
|---|---|---|
| 1 | **You cannot write them all** | See the table. 20 checks is 17.5 working years at 2 minutes a rule. |
| 2 | **They start contradicting each other** | Rule 12 says spam, rule 40 says ham. Now you need a second rulebook about which rule wins. |
| 3 | **The world changes underneath you** | You block "FREE", they write "FR33". You block "FR33", they write "F R E E". |

> **A rulebook is frozen the moment you finish it, and the world is not.**

There is a fourth problem the student will discover for themselves during the activity: **the rules stop paying.** Rules 1 to 5 buy you a lot of accuracy. Rules 200 to 258 buy you almost nothing.

![The rulebook gets fatter, the score does not](../figures/fig-w10-2-rulebook-vs-accuracy.svg)
*Figure 10.2 — Rules 9 to 258 bought four percentage points between them. That is the wall.*

### 4. The idea: the machine learning trade

Here is the whole of machine learning in one sentence, and it is genuinely all you need for Level 1:

> **The machine learning trade** — you stop writing the rules, and instead you collect examples with the correct answers attached. The machine finds the rule.

The everyday version: imagine teaching someone to pick a ripe watermelon.

- **Option A — write instructions.** "Knock it; if it sounds hollow it's ripe. Check the yellow patch. Check the stem." You will write ten instructions and they will still pick badly, because the real skill lives in combinations nobody can put into words.
- **Option B — walk them through a market.** Point at sixty watermelons and say "ripe… not ripe… ripe… not ripe". Say nothing else. They will get good at it, and they will still not be able to explain how.

**Option B is machine learning.** Notice both halves of the trade. You gained something that works on watermelons nobody described. You lost the ability to point at the reason.

![The machine learning trade](../figures/fig-w10-3-machine-learning-trade.svg)
*Figure 10.3 — You give up writing rules. You take on collecting labelled examples. That is the whole trade.*

Both sides of the trade cost something. Put the honest version on the board:

| | Writing rules yourself | The machine learning trade |
|---|---|---|
| You provide | The rules | **Labelled examples** |
| Effort grows… | **by doubling** (with the checks) | **by adding** (one example at a time) |
| Can you explain a decision? | Yes — point at the rule | Usually not |
| World changes? | Rewrite by hand | Add new examples, retrain |
| Things it can look at | About 10 before you drown | Thousands, easily |
| Needs lots of data? | No | **Yes. This is the price.** |
| Will it be perfect? | No | No |

That "effort grows by adding" row is the one that decides the whole argument. Collecting example number 5,000 costs the same as collecting example number 5. Writing rule number 5,000 does not.

![Doubling versus adding](../figures/fig-w10-5-effort-curves.svg)
*Figure 10.4 — Red squares: writing rules. Green triangles: collecting examples. Both go up; only one of them explodes.*

### 5. The two misconceptions you will meet, and what to say

**Misconception 1 — "A clever programmer would just write fewer, smarter rules."**

This is a *good* objection and it is partly right. A single rule can cover a whole block of situations at once: `IF contains "free" THEN spam` settles four of the eight three-check situations in one line. So the real rulebook is smaller than 2ⁿ.

But — and this is the reply to give — **the shortcut buys you a bigger n, not a different shape.** It helps enormously at 10 checks and not at all at 20,000. A real spam filter looks at every word in the language; that is tens of thousands of checks. Shortcuts move the wall further away. They do not remove it. Say exactly this: *"Yes, and that's why rules got us to about ten checks instead of about five. We need twenty thousand."*

**Misconception 2 — "So machine learning means nobody has to do any work."**

No. **You swapped thinking for collecting.** Collecting 5,000 correctly-labelled messages is many hours of dull, careful human work, and every mistake in it is learned by the machine with perfect loyalty. Rule-based systems fail because humans cannot think of everything. Learned systems fail because humans cannot collect everything. Neither is magic; they fail in different places.

### 6. How deep to go, and where to stop

**Go this far:**
- 2ⁿ, computed by hand and by doubling.
- The word *exponential* meaning "doubles each step" — nothing more.
- The trade, stated in the student's own words.

**Stop before:**
- Logarithms. Do not mention log scales even if the student uses a spreadsheet chart. Say "the curve becomes a straight line, which is what doubling always looks like on this kind of chart" and move on.
- *How* a machine finds the rule. That is Week 15. If asked, say "we'll build one in seven weeks and you'll see it happen." Do not improvise an explanation of training now — it will be wrong and you will have to unteach it.
- Neural networks, ChatGPT, anything with a brand name. Not this week.

If you genuinely understood the sentence *"each new check doubles the situations, and doubling always beats a human"*, you understand this lesson well enough to teach it confidently.

---

## 🧰 Prep Checklist

**15 minutes the night before**

- [ ] **Find the envelope.** Confirm with the student that the sealed envelope of 10 fresh messages from Week 9 exists and is unopened. Do not open it yourself.
- [ ] **Print** workbook pages 10.1–10.6 (or have the workbook open at page 10.1).
- [ ] **Fold a sheet of A4 in half yourself, as many times as you can.** Do it now, in private. You will get 6 folds, possibly 7 with real effort, and you will not get 8. Knowing this in your hands makes the Hook work.
- [ ] **Read Figure 10.1 and the "check 30" fact** in section 4 above until you can say it without notes.
- [ ] **Write the two board panels** (Figure 10.5 below) if you have a whiteboard you can prepare in advance.

**5 minutes on the day**

- [ ] Four sheets of A4 on the table (one to fold, three spare).
- [ ] Calculator within reach.
- [ ] The student's Rulebook vs Reality folder: the 20 training messages, the tally table, the 5 rules.
- [ ] The sealed envelope, on the table, still sealed, in plain sight. It is a prop. Let it sit there.

**Fallback if something fails**

| If this fails | Do this instead |
|---|---|
| No internet / no spreadsheet | **Nothing changes.** This lesson is fully unplugged by design. The spreadsheet is an optional extension only. |
| The envelope was opened early | Do not pretend. Say: "That's a real problem and it's worth understanding why." Then generate 10 brand-new messages together in 5 minutes (5 obvious spam, 5 ordinary), **with the student's rulebook face-down on the table**, and use those. Losing the honesty of a test set is itself the lesson — Week 19 is about exactly this. |
| The student never finished the 5 rules in Week 9 | Spend the first 6 minutes of the Activity segment writing them, using the tally table. Cut the extension. Five rules plus a default is the minimum; do not accept four. |
| No paper to fold | Use a paper napkin, a receipt, or a page from a magazine. Any thin sheet works. Do not skip the fold — it is the physical anchor for the whole lesson. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Fold It Seven Times | 8 | 8 | The student fails to fold paper 8 times and finds out why |
| 🧠 Concept — Doubling, and the Wall | 18 | 26 | 2ⁿ, the 258 count, the three ways rules die |
| 🔍 Worked Example Together — Count the Explosion | 14 | 40 | Fill the doubling table 1→30 together; convert to hours |
| 🎲 Activity — The Trade, then Finish the Project | 20 | 60 | Write the trade; open the envelope; score 10 fresh messages |
| 🔑 Wrap & Assign | 10 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — Fold It Seven Times (8 minutes)

**Do this:** Put one sheet of A4 in front of the student. Say nothing about maths. Do not mention doubling.

**Say this:**

> "Simple challenge. Fold this sheet of paper in half. Then fold it in half again. Keep going. I want eight folds. You have two minutes. Go."

Let them go. Watch. Around fold 5 it gets stiff, at fold 6 it needs both hands and a table edge, and at fold 7 it becomes a small hard brick that will not bend. They will not reach 8. Nobody reaches 8 with A4.

> "Stop. How many did you get?"
>
> "Right — six. Almost everybody gets six, some people get seven with a table edge and a lot of anger, and basically nobody gets eight. Now here's my question, and I want you to think before you answer. **The paper didn't get thicker because you added anything to it.** No glue, no extra sheets. Same one sheet. So why did it get impossible?"

Let them answer. Then:

> "Every time you folded it, you doubled the number of layers. One sheet, then two, then four, then eight. Count with me: after six folds, how many layers?"

Count it out loud together on fingers: 1, 2, 4, 8, 16, 32, 64. Then:

> "Sixty-four layers. Fold it once more and it's a hundred and twenty-eight. That's why your hands failed. **Not because the job got a little bit harder each time — because it doubled each time.** Hold on to that feeling in your fingers, because the whole lesson today is that exact feeling, applied to writing rules."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Why did it get impossible?" | "The layers doubled every fold." | If they say "the paper got thicker" — good, push once: "It did. But nothing was added. Where did the thickness come from?" Then count layers together. |
| "How many layers after 7 folds?" | 128 | If they guess 14 (7 × 2), that is the *exact* misconception this lesson fixes. Say: "That's the natural guess and it's the mistake everyone makes. Let's count." Then count 1, 2, 4, 8, 16, 32, 64, 128 out loud. |
| "How thick is 128 sheets?" | About 12.8 mm — a finger's width | If unsure, give them the number: one sheet is about 0.1 mm. 128 × 0.1 = 12.8 mm. |

---

### 🧠 Concept — Doubling, and the Wall (18 minutes)

**Do this:** Draw the left-hand panel of Figure 10.5 on the board: a two-column table headed `checks | situations`. Leave the right-hand panel blank for now — you fill it in during the Wrap.

![The Week 10 board at the end of the concept segment](../figures/fig-w10-6-board-doubling-table.svg)
*Figure 10.5 — What the board should look like by minute 26. Leave it up all lesson.*

**Say this:**

> "Back in Week 8 you found out that every rule you write has edge cases — examples it gets wrong. And the obvious fix is obvious: add another rule. That genuinely works. It works for about five rules. Then something ugly happens, and today we're going to measure exactly how ugly.
>
> A computer program that follows instructions is built out of **checks**. A check is a question with a yes/no answer. Does this message contain the word 'free'? Yes or no. Does it have a link? Yes or no. Is the sender someone in my contacts? Yes or no.
>
> One check gives you two situations: yes, and no. Write that on the board — one check, two situations.
>
> Now add a second check. Every one of my two situations splits in two, because the new question can be answered either way. Two becomes four. Add a third: four becomes eight. Each new check **doubles** the number of situations, exactly like your paper.
>
> There's a name for this shape, and you should use it because it's the real word: **exponential growth**. It just means the thing doubles every step. It's the same word whether you're folding paper, splitting cells, or adding checks to a rulebook."

Write the definition where it stays visible:

> **Exponential growth** — when a quantity doubles at every step. It starts slow, looks harmless, and then defeats you.

> "Let's fill in a few rows. Three checks: two times two times two, which is eight. Five checks: thirty-two. Ten checks: one thousand and twenty-four. Twenty checks: over a million. Thirty checks: over a *billion*.
>
> Read that again with me. You went from three things to thirty things. You multiplied the number of questions by ten. And the number of situations went from eight to more than a billion.
>
> That has a name too, and it's the phrase for this week: **rule explosion**."

Write it up:

> **Rule explosion** — the number of rules you need grows far faster than the number of cases you are trying to handle, until the rulebook becomes impossible for a human to maintain.

> "And here is the sentence I want you to remember for the rest of your life. Going from twenty-nine checks to thirty checks adds five hundred and thirty-six million, eight hundred and seventy thousand, nine hundred and twelve brand new situations. All twenty-nine checks before it, added up together, only ever created five hundred and thirty-six million, eight hundred and seventy thousand, nine hundred and *eleven*.
>
> **The thirtieth check, on its own, creates more new work than every single check before it, put together. By exactly one.** And that's not special about thirty. It's true at every step. Check 10 creates more work than checks 1 to 9 combined. Check 5 creates more than checks 1 to 4 combined. You are always, at every moment, only halfway."

Pause here. This lands.

> "Now — three things kill the rule-writer, and the counting is only the first one.
>
> One: **you cannot write them all.** We'll put actual hours on that in a minute.
>
> Two: **the rules start fighting each other.** Rule 12 says spam. Rule 40 says not spam. Same message. Now you need rules about which rule wins — a second rulebook sitting on top of the first one.
>
> Three, and this is the one that actually finishes you off: **the world changes underneath you.** Scammers read your rules by testing them. You block 'FREE'? They write 'FR33'. You block 'FR33'? They write 'F R E E' with spaces. Every rule you write starts going stale the day you write it. A rulebook is frozen the moment you finish it, and the world isn't."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Four checks — how many situations?" | 16 | If they say 8, they doubled once instead of twice. Walk the split: "8 situations, each splits in two." |
| "Why does adding one check double it, instead of adding one?" | "Because every situation I already had can now go two ways." | If stuck, draw two boxes, then split each into two, then split those four into two. Physically drawing the split is what makes it click. |
| "Which of the three killers is worst, and why?" | Number three — because you can hire more people to write rules, but you cannot stop the world changing. | Any reasoned answer is fine. Push for the *reason*, not the choice. If they pick number one, ask "what if you had a hundred people writing rules?" |
| "Is 'exponential' just a fancy word for 'fast'?" | No — it means *doubling*. Something can be fast without doubling. | This is worth correcting properly. "A car going 200 km/h is fast. It isn't exponential. Exponential means the next step is as big as everything so far." |

---

### 🔍 Worked Example Together — Count the Explosion (14 minutes)

This segment is arithmetic done out loud, together, with the student holding the pencil. **You do not write the numbers. They do.** The objective says "a number you calculated yourself" and that is not decoration.

**Do this:** Open workbook page 10.1. It has a blank table, `checks` 1 to 30 down the left and `situations` blank on the right. Hand them the pencil.

**Say this:**

> "You're going to fill this in. And you're going to do it the lazy way, which is also the correct way: you never multiply anything. You just **double the row above**.
>
> Row 1: two. Row 2: double it, four. Row 3: eight. Row 4: sixteen. Keep going. Call the numbers out as you write them. When it gets hard, use the calculator — press two, times, two, then just keep pressing equals."

Let them work. This takes about 6 minutes and it should. Do not rush it. The physical act of writing 1,073,741,824 by hand is the lesson.

Checkpoints to call out as they pass them, so they notice the shape:

- **Row 8 (256):** "Stop. Eight checks. 256 situations. So a rulebook covering all of them is 256 rules, plus one line saying 'otherwise, do this', plus one line saying which rule wins if two fire. **258 lines.** That's the title of today's lesson, and eight checks is nothing at all."
- **Row 10 (1,024):** "Ten questions. A thousand situations. Could you hold ten questions in your head? Easily. Could you write a thousand rules? No."
- **Row 20 (1,048,576):** "Over a million."
- **Row 30 (1,073,741,824):** "Over a billion. Say the number out loud. One billion, seventy-three million, seven hundred and forty-one thousand, eight hundred and twenty-four."

Now the two conversions. Do these together on the calculator.

**Conversion 1 — hours.** Assume you are fast: one carefully-thought-out rule every 2 minutes, 8 hours a day, 250 working days a year.

```
20 checks            = 1,048,576 situations
1,048,576 x 2 min    = 2,097,152 minutes
2,097,152 / 60       = 34,952.5 hours
34,952.5 / 8         = 4,369 working days
4,369 / 250          = 17.5 working YEARS
```

> "Seventeen and a half years of solid work, no holidays, no sick days, for a system that checks twenty things. And a real spam filter doesn't check twenty things. It checks every word in the language — tens of thousands of them."

**Conversion 2 — the check-30 fact.** Have them look at rows 29 and 30 of their own table.

```
after 29 checks:  536,870,912 situations
after 30 checks: 1,073,741,824 situations
check 30 added:  1,073,741,824 - 536,870,912 = 536,870,912

everything checks 1-29 ever added: 536,870,912 - 1 = 536,870,911
```

> "Look at those two numbers on your own page. Check thirty added more than checks one to twenty-nine put together. By one. Write that in the margin."

**Do this:** Point back at Figure 10.2 (the fat rulebook, flat score) and give them ten seconds to look at it.

**Say this:**

> "Here's what this actually feels like when you're the one writing the rules. The first three rules take you from guessing to seventy percent. Rules four to eight take you to seventy-eight. And then rules nine through two hundred and fifty-eight — two hundred and fifty more rules — buy you four points. Four. That flat blue line next to that fat yellow book is the thing you're about to feel for yourself in the next twenty minutes."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Where did the 258 come from?" | 2⁸ = 256, plus a default line, plus a line about rule order. | If they say "you made it up" — half fair. Show the working. Say "256 is the maths. The other two are the boring lines every rulebook needs." |
| "17.5 years for 20 checks. How long for 21?" | 35 years. It doubles. | If they say "18 years" or "a bit more", that is the fold-the-paper mistake again. Point at row 21 of their own table. |
| "Does a real programmer write all 2ⁿ rules?" | No — one rule can cover a whole block at once. | Correct and important. Follow with: "So does that save them?" Answer: it moves the wall from about 5 checks to about 10. It does not remove it. |

---

### 🎲 Activity — The Trade, then Finish the Project (20 minutes)

Full instructions are in the next section. In the lesson flow it runs like this:

**Minutes 0–5 — Write the trade down.** Workbook page 10.3. They write, in their own handwriting, what they give up and what they supply instead. You fill in the right-hand panel of the board (Figure 10.5) at the same time so they can check themselves against it.

**Say this:**

> "So the rule-writer has hit a wall. Here's the deal that's on the table instead, and it's a genuine trade — both sides give something up.
>
> You stop writing the rules. Completely. You write none. Instead you collect **labelled examples** — a message with the word 'spam' written next to it, a message with 'ham' written next to it, a few thousand times — and the machine finds the rule.
>
> Now, what did you just give up? Two things, and the second one hurts. You gave up the *work* of writing rules, which is great. And you gave up the ability to *read* the rule and know why it decided. When your rulebook marks a message as spam you can point at rule 3. When a learned model does it, usually nobody on earth can tell you why. Write both of those down.
>
> And here's the price. How many labelled examples would you need? Not five. Not fifty. Thousands. Somebody has to sit and label them, and every mistake they make gets learned perfectly. **You swapped thinking for collecting. Thinking doesn't scale. Collecting does.**"

**Minutes 5–20 — Open the envelope.** This is the part they have been waiting three weeks for. See the full protocol below.

---

## 🎲 The Activity, In Full

### Part A — Count the Explosion (already done in the Worked Example)

Kept here for reference: workbook page 10.1, the 1-to-30 doubling table, plus page 10.2, the paper-fold arithmetic.

![Seven folds of paper](../figures/fig-w10-4-paper-folds.svg)
*Figure 10.6 — Seven folds. The same doubling as seven yes/no checks.*

Page 10.2 asks the student to write the fold table and answer: *how thick would the paper be after 30 folds?* The answer is 2³⁰ × 0.1 mm = 107,374,182.4 mm = **107 kilometres**. It is worth doing this one out loud; it is the single most memorable number available to you.

### Part B — Rulebook vs Reality: the reckoning

**What you need**

- The 20 labelled training messages (from Week 8)
- The 5 rules plus a default (from Week 9)
- The **sealed envelope** with 10 fresh messages, 5 spam and 5 ham
- Workbook page 10.4 (the scoring table) and page 10.5 (the write-up)
- A pen the student cannot erase with. This matters. See the rules.

**Setup (2 minutes)**

1. Lay the 5 rules face-up where both of you can read them.
2. Confirm out loud what the convention is: **first match wins, checked top to bottom.** If the student never wrote a convention, write it now.
3. Put the envelope in the student's hands. Do not open it yet.

**The rules of the scoring, said out loud before opening (1 minute)**

Read these to the student verbatim. They are not fussiness; the whole value of the exercise is here.

> "Three rules for the next ten minutes.
>
> **One: you are the computer, not the judge.** You run the rules exactly as written. If a rule gives an answer you know is wrong, you write the wrong answer down. No fixing it in your head.
>
> **Two: you may not change a rule.** Not one word, not until every message is scored. If you spot a fix, write it in the margin and keep going.
>
> **Three: you write which rule fired.** Not just the verdict. The rule number. Because a rule that gets the right answer for a stupid reason is not a good rule, and the only way to catch that is to look at which one fired."

**The scoring (10 minutes)**

Open the envelope. Score all ten, in order, in this table (workbook page 10.4):

| # | Message | First rule to fire | Verdict | Truth | ✓/✗ | Error type |
|---|---|---|---|---|---|---|
| 21 | | | | | | false alarm / miss / — |
| … | | | | | | |
| 30 | | | | | | |

*False alarm* = a real message marked spam. *Miss* = spam that got through.

**The arithmetic (3 minutes)** — workbook page 10.4, bottom:

```
Training accuracy = ____ correct out of 20 = ____ = ____%
Fresh accuracy    = ____ correct out of 10 = ____ = ____%
The gap           = training% - fresh%     = ____ percentage points
False alarms      = ____
Misses            = ____
```

**What "finished" looks like**

- All ten rows filled, including the rule number that fired.
- No rule was edited during scoring. (Margin notes are encouraged.)
- Both accuracies written as **a fraction and a percentage**.
- The gap computed, in percentage points.
- False alarms and misses counted **separately**.
- The student can point at one specific row and say "this is where it broke first."

**Expected result — tell the student this afterwards, not before:** the fresh score is almost always 10 to 30 percentage points below the training score, and the rule that breaks first is almost always their *strongest* rule. That is not bad luck. Their strongest rule is strongest because it fit the training messages hardest.

### Variation — easier

If the student is struggling to run the rules mechanically, or is emotionally attached to a good score:

- Score only **6** messages instead of 10 (3 spam, 3 ham). The gap still shows.
- **You** read each message aloud and run the rules with them for the first two, thinking out loud: "Rule 1 — does it contain 'free'? No. Rule 2 — …". Then hand over.
- Drop the "which rule fired" column for the first three rows, then add it back.

### Variation — harder

If the student finishes early and is enjoying it:

**The adversary round (10 minutes).** Show them the rules — they wrote them, so they already know them — and challenge them:

> "Write five messages that any human would instantly call spam, but that your own rulebook marks as ham."

Give them 6 minutes. They will succeed on all five, and quickly. Then ask the three questions:

1. How long did that take you?
2. Real spammers do exactly this, constantly, at industrial scale. What does that mean for how long your rulebook stays useful?
3. If your rules had been *learned* from 5,000 examples instead of written by you, would it have been harder to break?

The honest answer to 3 is *yes, harder — but not impossible*. You can still probe a learned system with test messages and find its gaps. Learning raises the cost of attacking. It does not make attacking impossible.

---

## ❓ Questions Students Ask This Week

**"If rules are so bad, why does anything still use them?"**

Because for a lot of jobs they are exactly right, and machine learning would be *worse*. Tax calculations, chess legality, drug dosage limits, speed limits. The test: **did a human write the correct answer down somewhere already?** A parliament wrote the tax bands. FIDE wrote the chess rules. A pharmacologist established the safe dose. If the answer already exists in written form, implement it as rules — learning can only make a fuzzy copy of something already exact. Learning is for jobs where the answer lives only in people's ability to recognise something without explaining it.

**"Couldn't a computer write the rules for us? It's fast."**

It can write them fast, but it cannot know which ones are *right*. Someone still has to decide that "contains FREE" means spam, and that decision comes from looking at examples. And notice what you've just invented: a system that looks at examples and produces rules. That is machine learning. You reasoned your way to it.

**"How many examples does a machine actually need?"**

It depends enormously, and there's no formula. For the tiny model you'll build in Week 17, about 40 photos per category is enough to see it work. For a real spam filter, hundreds of thousands. For a system that recognises faces, millions. The honest rule of thumb: the harder it is for a human to explain the task, the more examples you need.

**"Does the machine actually understand what spam is?"**

No. It counts patterns in the examples you gave it. If every spam message you showed it happened to be typed in capitals, it will learn "capitals means spam" and it will be delighted with itself, and it will be wrong the first time your grandmother sends a message in capitals. It has no idea what a scam is, or what money is, or what you are.

**"Why don't they just make the rules secret so scammers can't test them?"**

They do try. It doesn't work well, because a scammer doesn't need to *read* your rules — they just send test messages and see which ones get through. That's called probing. Within a few hundred test messages you can map out most of a rulebook without ever seeing it. This is also, incidentally, why "security by keeping it secret" is treated as a weak defence by people who do this professionally.

**"Which is better overall — rules or learning?"** *(This one has no clean answer, and you should say so.)*

**Nobody knows for sure, and here's why:** it depends on the job, and the people who build these systems genuinely argue about it. Rules are predictable, explainable, and fail in ways you can see. Learned systems handle jobs no human could write rules for, and fail in ways nobody can explain, sometimes badly. Most real systems in the world today are a mix — a learned model with hand-written rules bolted on top for the cases where being wrong is unacceptable. There is no formula that tells you the right mix. It is a judgement call made by humans, and reasonable experts disagree about it every day.

**"Is 258 a real number that someone had to write?"**

258 is our example. But yes, real rule-based systems got genuinely enormous before people gave up on them. Some medical and tax systems from the 1980s ran to tens of thousands of hand-written rules and needed full-time teams just to keep them from contradicting each other. That period is roughly why machine learning took over.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The student edits a rule halfway through scoring the fresh messages | It feels obviously wrong to write down an answer you know is wrong | Stop them mid-sentence. "Write it in the margin, don't change the rule." Then say why: "If you fix it now, you'll end up with a rulebook that scores brilliantly on these ten and we'll have learned nothing." |
| The envelope was opened before today | Curiosity, or it got shuffled into other papers | Do not paper over it. Use the fallback in the Prep Checklist, and name what was lost: "You can't un-see them, so this score won't mean what it should. That's exactly why professionals seal their test data." Week 19 comes back to it. |
| They guess 2 × 30 = 60 for thirty checks | Doubling genuinely feels like adding — this is a universal human bug, not a weakness of this student | Never say "no". Go back to the paper: "How many layers after 6 folds? 64. So is 7 folds 66, or 128?" Let them correct themselves. |
| The score on the fresh messages is high (9 or 10 out of 10) | Their 10 fresh messages were too similar to the training 20 — usually all from the same source | Do not deflate them. Say: "Good. Now let's find out if that's real." Write three brand-new messages yourself, on the spot, deliberately unlike theirs: a delivery scam, a message from a sibling with no punctuation, a school notice. Score those. The gap will appear. |
| "This is just maths, not AI" | It genuinely looks like a maths lesson | Agree, then land it: "It is maths. It's the *specific* piece of maths that made people stop writing rules and start collecting examples. Without this number, machine learning never gets invented." |
| They finish the doubling table in 90 seconds using a formula and learn nothing | A quick student will spot 2ⁿ immediately | Excellent — do not slow them down. Instead give the harder question straight away: "Prove to me that check 30 adds more than checks 1 to 29 put together." That is a genuinely satisfying problem. |
| The write-up becomes "rules are bad, machine learning is good" | It's the obvious summary and it is wrong | Push back once, hard: "Name three jobs where I'd be an idiot to use machine learning." Do not accept the page until they can. |
| The lesson runs 15 minutes over | The scoring always takes longer than you think | Protect the Wrap. If you are at minute 62 and only 6 messages are scored, stop scoring, do the three checks, and send the last four home as homework. The reflection matters more than the last four rows. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** the 1-to-30 table becomes a 1-to-12 table. Twelve rows (4,096) makes the point perfectly well and does not exhaust them. Skip the hours conversion entirely. Skip the adversary round.

**Reteach:** go back to the paper and build the situations physically. Take three small cards labelled `free?`, `link?`, `caps?`. Lay out the two situations for card 1 as two rows on the table. Add card 2 — physically split each row into two. Add card 3 — split again into eight. Seeing eight actual rows appear on the table from three cards does what no explanation can.

**Reduce the project:** score 6 fresh messages, not 10. Accept a five-sentence write-up rather than a page, as long as it names one specific rule and one specific message.

### If the student is flying

Extension questions, in increasing difficulty:

1. "A real spam filter checks about 20,000 things — every word it knows. How many situations is that?" *(2²⁰⁰⁰⁰. The honest answer is that the number is larger than the number of atoms in the observable universe, which is about 10⁸⁰. Let them sit with that.)*
2. "Prove that check *n* always adds more than checks 1 to *n*−1 combined." *(After n−1 checks you have 2ⁿ⁻¹ situations. You started with 1, so those checks added 2ⁿ⁻¹ − 1. Check n adds 2ⁿ − 2ⁿ⁻¹ = 2ⁿ⁻¹. Which is exactly one more.)*
3. "Build the table in a spreadsheet. Type `=2^A2` and drag it down. Then chart it. Then find the row where 'years to write' first goes above 1 — and answer: if you'd started writing rules the day you were born, would you be finished?"
4. "Find three jobs where hand-written rules are clearly better than machine learning, and say what they have in common." *(Answer key below.)*

### If the student won't engage today

Project weeks are long and this one has a lot of arithmetic. If they are done, do this instead — it is a genuine 15-minute lesson and it costs you nothing:

Do **only** the fold and the argument. Fold the paper. Count the layers to 128. Ask one question: *"How thick after 30 folds?"* Work it out together: 107 kilometres. Then ask them to defend the rule-writer for two minutes — "Convince me that writing rules is fine and I'm being dramatic." Argue back. That conversation hits the objective, and you can move the table and the scoring to a 20-minute session tomorrow.

If they are frustrated specifically because their rulebook did badly on the fresh messages, name it out loud: *"Your rulebook scoring badly is the successful outcome of this project. If it had scored ten out of ten I'd be worried you'd peeked."*

---

## ✅ Assessing Understanding

Three checks, five minutes, in the last segment. Use the exact wording.

**Check 1 — the arithmetic (spoken)**

> "I've got a rulebook that checks 12 things. I add one more check. How many extra situations did I just create?"

*A good answer:* "4,096" — or, better, "the same as all twelve checks made before, plus one." Either is full marks. A weaker but acceptable answer: "It doubles, so 4,096 more." **A wrong answer to catch:** "one more" or "twelve more" — that is the additive misconception; go back to the paper.

**Check 2 — the concept, in their words (spoken)**

> "Finish this sentence for me: I stopped adding rules because…"

*A good answer* contains a number they computed and a reason that is not "it got boring". For example: "…because rule twenty would only fix one message, and I'd already found four more it got wrong" or "…because I'd need 258 rules for eight checks and I've only got five." **What you're listening for:** evidence, not vibes.

**Check 3 — the trade (spoken)**

> "Tell me the deal. What do you give up, and what do you have to supply instead?"

*A good answer:* "I give up writing the rules, and I give up being able to explain why it decided. I supply labelled examples instead, and I need a lot of them." Two out of three of those is a solid pass. If they only say "I supply examples", prompt once: "And what do you lose?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks adding a check adds one situation. Cannot complete the doubling table without being told each value. |
| **2 — Emerging** | Completes the table with prompting. Can say "it doubles" but cannot use it to argue anything. Write-up is "rules are bad". |
| **3 — Secure** | Completes the table independently. States rule explosion in own words with a number they computed. Names both halves of the trade. **This is the target.** |
| **4 — Strong** | Also names a job where rules are clearly the right choice, and says why. Identifies which of their own rules broke first and why it was their strongest one. |
| **5 — Exceptional** | Can prove that check *n* adds more than all previous checks combined. Argues that shortcuts (one rule covering many situations) delay the wall without removing it. Distinguishes "I can't write the rule" from "the information isn't in the input at all." |

---

## 📤 Homework to Assign

**Say this:**

> "Two things, and about fifty minutes total.
>
> **First, finish the project.** That's workbook pages 10.4 and 10.5. Page 10.4 is the scoring you started today — the ten rows, and the numbers at the bottom. I want the fresh score written **both** ways: as a fraction, like eight out of ten, and as a percentage, eighty percent. Then page 10.5 is one page, in your own words, called *Why I stopped adding rules*. It has to contain three things: which rule broke first and on which exact message, whether that rule was one of your strongest ones on the training messages, and what you would do next if you were actually building this for real — and 'add more rules' is not an allowed answer.
>
> **Second, the unwritable rule.** That's page 10.6. Try to write if-then rules for 'is this a photo of a cat'. Take it seriously — write five real rules, not silly ones. Then, for each one, find a real thing it gets wrong. And write down which rule broke first. You are supposed to fail at this. Failing carefully is the homework."

**Workbook pages:** 10.1 and 10.2 finished in class; **10.3, 10.4, 10.5, 10.6** at home.

**Expected time:** 15 min finishing page 10.4 · 20 min for page 10.5 · 20 min for page 10.6. About 55 minutes.

---

## 🔑 Answer Key

### Page 10.1 — The doubling table

| checks | situations | | checks | situations | | checks | situations |
|---|---|---|---|---|---|---|---|
| 1 | 2 | | 11 | 2,048 | | 21 | 2,097,152 |
| 2 | 4 | | 12 | 4,096 | | 22 | 4,194,304 |
| 3 | 8 | | 13 | 8,192 | | 23 | 8,388,608 |
| 4 | 16 | | 14 | 16,384 | | 24 | 16,777,216 |
| 5 | 32 | | 15 | 32,768 | | 25 | 33,554,432 |
| 6 | 64 | | 16 | 65,536 | | 26 | 67,108,864 |
| 7 | 128 | | 17 | 131,072 | | 27 | 134,217,728 |
| 8 | 256 | | 18 | 262,144 | | 28 | 268,435,456 |
| 9 | 512 | | 19 | 524,288 | | 29 | 536,870,912 |
| 10 | 1,024 | | 20 | 1,048,576 | | 30 | 1,073,741,824 |

**10.1(a) How many situations does check 30 add on its own?**
1,073,741,824 − 536,870,912 = **536,870,912**.

**10.1(b) How many did checks 1 to 29 add between them?**
You start with 1 situation before any checks. After 29 checks you have 536,870,912. So they added 536,870,912 − 1 = **536,870,911**.

**10.1(c) Which is bigger?**
Check 30 alone, by exactly **1**.

**10.1(d) At 2 minutes per rule, how long to write the rules for 20 checks?**
1,048,576 × 2 = 2,097,152 minutes ÷ 60 = 34,952.5 hours ÷ 8 = 4,369 working days ÷ 250 = **17.5 working years**.

**10.1(e) Why does the real rulebook need fewer than 2ⁿ rules? Does that save the rule-writer?**
One rule can cover a whole block of situations at once — `IF contains "free" THEN spam` settles half of all situations involving that check in a single line, whatever the other checks say. So the real number is much smaller than 2ⁿ. It does **not** save the rule-writer: shortcuts move the wall from about five checks to about ten, and a real language task needs tens of thousands. The shortcut buys a bigger *n*; it does not change the shape of the curve.

### Page 10.2 — The paper fold

| folds | layers | thickness (0.1 mm a sheet) |
|---|---|---|
| 0 | 1 | 0.1 mm |
| 1 | 2 | 0.2 mm |
| 2 | 4 | 0.4 mm |
| 3 | 8 | 0.8 mm |
| 4 | 16 | 1.6 mm |
| 5 | 32 | 3.2 mm |
| 6 | 64 | 6.4 mm |
| 7 | 128 | 12.8 mm |

**10.2(a) Why couldn't you fold it eight times?**
Because 8 folds is 256 layers, about 25.6 mm of paper — you are trying to bend a block thicker than your thumb, and the outer layers have to travel further round the fold than the inner ones, so the paper has to stretch. It cannot.

**10.2(b) How thick after 30 folds?**
2³⁰ = 1,073,741,824 layers × 0.1 mm = 107,374,182.4 mm = 107,374.18 metres = **about 107 kilometres**. Higher than the edge of space (usually put at 100 km).

**10.2(c) What does the fold have to do with rules?**
Each fold doubles the layers; each check doubles the situations. Same arithmetic, and the same reason it beats you: it is not that each step is a bit harder than the last, it is that each step is as big as everything before it.

### Page 10.3 — The trade

Accept any wording that carries these five points. Model answer:

> **What I give up:** writing the rules myself, and the ability to read the rule and see why it decided.
> **What I supply instead:** labelled examples — a message with the right answer written next to it.
> **How many I would need:** for spam, thousands. Not five, not fifty.
> **The price:** labelling is slow, boring human work, and any mistake I make gets learned perfectly by the machine.
> **What I gain:** it can look at every word in the language instead of the ten things I could hold in my head, and when the world changes I add new examples instead of rewriting by hand.

**10.3(a) Write the trade as one sentence.**
"You swap thinking for collecting — because thinking doesn't scale and collecting does."

**10.3(b) Name one thing that is worse about the machine learning way.**
Any of: you cannot explain a decision · you need lots of data · it can surprise you · it learns your labelling mistakes exactly · it can be confidently wrong on something no human would get wrong.

### Page 10.4 — Rulebook vs Reality: the scored table

The student's own messages are their own, so here is a **complete worked model** to mark against. If your student's structure matches this and their arithmetic is right, it is correct.

**Model rulebook** (first match wins, top to bottom):

```
RULE 1: IF the message contains "free" (any capitalisation)   THEN spam
RULE 2: IF it contains "win", "won" or "prize"                THEN spam
RULE 3: IF it contains [LINK]                                 THEN spam
RULE 4: IF it contains a question mark                        THEN ham
RULE 5: IF it has 2 or more ALL-CAPS words of 3+ letters      THEN spam
DEFAULT: OTHERWISE                                            THEN ham
```

Training accuracy on the 20 messages: **19/20 = 95%.**

| # | Message | Rule that fired | Verdict | Truth | ✓/✗ | Error type |
|---|---|---|---|---|---|---|
| 21 | Congratulations! You have WON a FREE holiday. Claim at [LINK] | 1 | spam | spam | ✓ | — |
| 22 | Your parcel could not be delivered. Update your address here [LINK] | 3 | spam | spam | ✓ | — |
| 23 | Are you free after school? | 1 | spam | ham | ✗ | false alarm |
| 24 | URGENT: your bank account is LOCKED. Verify now. | 5 | spam | spam | ✓ | — |
| 25 | Can you bring my maths book tomorrow? | 4 | ham | ham | ✓ | — |
| 26 | Dinner at 7 | DEFAULT | ham | ham | ✓ | — |
| 27 | You have been selected for a cash reward. Reply YES to claim. | DEFAULT | ham | spam | ✗ | miss |
| 28 | Match is cancelled, pitch flooded | DEFAULT | ham | ham | ✓ | — |
| 29 | WIN an iPhone! Just tap [LINK] before midnight | 2 | spam | spam | ✓ | — |
| 30 | Did you finish the science poster? I'm stuck on question 3 | 4 | ham | ham | ✓ | — |

```
Training accuracy = 19/20 = 0.95 = 95%
Fresh accuracy    =  8/10 = 0.80 = 80%
The gap           = 95 - 80 = 15 percentage points
False alarms      = 1   (message 23)
Misses            = 1   (message 27)
```

**Right for the wrong reason — worth marking:** message 21 was scored by Rule 1 ("free"), but it would also have been caught by Rules 2, 3 and 5. It looks like a triumph for Rule 1 and it is really a triumph for the message being obvious spam four times over.

### Page 10.5 — "Why I stopped adding rules"

A full-credit write-up contains all three required points. Model answer:

> **Which rule broke first, and where.** Rule 1 — `IF contains "free" THEN spam` — broke on message 23, "Are you free after school?". The word "free" was doing two completely different jobs and my rule could only see the letters.
>
> **Was it one of my strongest?** Yes, it was my strongest. On my 20 training messages, "free" appeared in 7 of the 10 spam and 0 of the 10 ham — a gap of 7, the biggest gap in my whole tally table. That is exactly why I put it first. Being the rule that fit my training messages best is *why* it broke first: it was tuned hardest to the messages I happened to have.
>
> **Which error type I had more of, and why it matters.** I had one of each, so they tied, but the false alarm worries me more. A miss means one scam message reaches me and I can just ignore it. A false alarm means a real message from a friend is hidden in a junk folder I never open. On a real phone, filtering out a message from your mum is a much worse failure than letting a scam through.
>
> **One message no rule of mine could catch.** Message 27, "You have been selected for a cash reward. Reply YES to claim." There is no unusual word in it. No link. No exclamation marks. One capitalised word. Every single thing that makes it a scam lives in the *meaning* — that strangers do not give people money — and no rule that counts words can reach meaning.
>
> **What the gap tells me.** Fifteen points of gap tells me my rules were fitted to the exact 20 messages I had, not to spam in general. I did not discover how spam works. I discovered how *my twenty messages* work.
>
> **What I would do next.** Not add more rules. I would collect a few thousand labelled messages from lots of different phones, not just mine, and let a machine find the rule — accepting that I would then not be able to explain any single decision it made.

**Marking guidance:** if the write-up says "rules are bad and machine learning is good", it is a level 2. Send it back with one question: *"Name three jobs where I'd be an idiot to use machine learning."*

### Page 10.6 — The unwritable rule: is this a photo of a cat?

Model answer:

| # | Rule | A real case it gets wrong |
|---|---|---|
| 1 | `IF it has pointed triangular ears THEN cat` | A German Shepherd. A fox. A bat. |
| 2 | `IF it has whiskers THEN cat` | Dogs have whiskers. So do rats, seals and walruses. |
| 3 | `IF it is furry AND smaller than a shoebox THEN cat` | A Chihuahua is smaller. A Maine Coon is much bigger. A guinea pig is both. |
| 4 | `IF the pupils are vertical slits THEN cat` | The same cat in a dark room has round pupils. And a photo of the cat's back has no eyes at all. |
| 5 | `IF it has a long tail with a curl at the tip THEN cat` | A Manx cat has no tail. A photo cropped at the shoulders has no tail. A squirrel has a much better one. |

**Which rule broke first?** Usually rule 1, because the very first non-cat photo anyone tries is a dog, and a lot of dogs have pointed ears.

**The closing paragraph — what information is missing:**

> Every one of my rules failed for the same reason, and it is not that I chose bad rules. It is that **none of the things my rules talk about are actually in the photo.** A photo is a grid of coloured dots. "Pointed ear" is not in that grid; it is something my eyes assemble out of the grid without telling me how. To write rule 1 as a real instruction a computer could run, I would first have to write a rule for "is this shape an ear", which needs a rule for "where does this shape end", which needs a rule for "is this dot part of an edge" — and that regress never bottoms out into anything I can write down.
>
> So more rules cannot help me. More rules can only look harder at what is already there. They cannot fetch what is not there. And what is not there is the enormous amount of recognising that my own eyes do in about a twentieth of a second without ever reporting to me how they did it.
>
> That is the sharpest test I know for when to stop writing rules: **if you can do the task instantly but cannot explain how, rules will fail and learning will work.** I know a cat when I see one. I cannot say how. So I should stop writing and start collecting.

### Extension answers (for the flying path)

**"20,000 checks — how many situations?"**
2²⁰⁰⁰⁰. Writing it out would take roughly 6,000 digits. For scale, the number of atoms in the observable universe is about 10⁸⁰, an 81-digit number. There is no useful way to describe 2²⁰⁰⁰⁰ except "vastly beyond anything physical".

**"Prove check *n* adds more than checks 1 to *n*−1 combined."**
Before any checks there is exactly 1 situation. After *n*−1 checks there are 2ⁿ⁻¹, so those checks added 2ⁿ⁻¹ − 1 between them. Check *n* takes 2ⁿ⁻¹ to 2ⁿ, so it adds 2ⁿ − 2ⁿ⁻¹ = 2ⁿ⁻¹. And 2ⁿ⁻¹ is exactly one more than 2ⁿ⁻¹ − 1. True for every *n*.

**"Three jobs where hand-written rules clearly win, and what they have in common."**

1. **Income tax.** `IF income is between 300,000 and 600,000 THEN tax = 5% of (income − 300,000)`. The bands were decided by a parliament; there is nothing to discover, and two people with identical incomes must get identical bills.
2. **A hospital drug-dosage cut-off.** `IF dose > max_safe_dose_for_weight THEN block and alert the pharmacist`. The limit comes from controlled trials, not from data. A 99.9% accurate model kills one person per thousand; a comparison against a published number is right by construction.
3. **Whether a chess move is legal.** The rules are complete, finite and published on two pages. A learned system could only ever produce a fuzzy copy, occasionally allowing an illegal move or rejecting a rare legal one like en passant.

**What they have in common:** in all three, *the correct answer already exists in written form* — a law, a published safety limit, a game's rulebook. Learning can only make an approximate copy of something already exact. Use rules when the answer was written down by someone. Use learning when the answer lives only in people's ability to recognise it without explaining it.

### Lesson questions posed in the Say-this scripts

- *"How many layers after 7 folds?"* → **128.**
- *"How thick is 128 sheets?"* → **12.8 mm**, about a finger's width.
- *"Four checks — how many situations?"* → **16.**
- *"Why does one more check double it?"* → Because every situation you already had can now go two ways.
- *"Where did 258 come from?"* → 2⁸ = 256 situations, +1 default line, +1 line stating which rule wins.
- *"17.5 years for 20 checks — how long for 21?"* → **35 years.** It doubles.
- *"I check 12 things and add one more — how many extra situations?"* → **4,096**, which is more than all twelve earlier checks created between them.

---

## 🔮 Next Week Preview

Week 11 changes the subject completely, and on purpose. Having spent three weeks discovering that you cannot *tell* a machine the rule, we start on the only other option: showing it examples. But an example is not a photo or an object — it is a **row of measurements**, and next week is about building one. The student will hide an object behind a book and describe it down an imaginary phone using only things you can measure, then measure three real household objects into three real rows. The single hardest and most important part is writing a *measuring instruction* precise enough that a different person gets the same number.

**Prep early:** for Week 11 you will need three household objects that are genuinely easy to confuse — three spoons of different sizes is a much better exercise than a spoon, a sofa and a cat. You will also need a ruler and a kitchen scale (a phone scale app is fine; if you have neither, "heavier or lighter than a full water bottle" works as a three-level category). Put them in a box now so they are not a scramble on the day. And bring an apple, or any single piece of fruit — you will need it for the opening.

---

[⬅ Week 9](week-09.md) · [Course Home](../README.md) · [Week 11 ➡](week-11.md) · [Student Guide](../student-guide/week-10.md) · [Workbook](../workbook/week-10.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
