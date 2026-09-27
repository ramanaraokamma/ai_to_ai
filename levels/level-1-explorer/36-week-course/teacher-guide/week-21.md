# Week 21 — Memorizing vs Generalizing

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Student Guide](../student-guide/week-21.md) · [Workbook](../workbook/week-21.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes (works in 60; the cut is in §Differentiation) |
| **Type** | 🟦 teach — one new word, one new tool, both built by hand |
| **Big idea** | A model that scores 100% on its own photos and 40% on new ones did not learn the object — it learned the photos. |
| **New vocabulary** | overfitting · confusion matrix · diagonal · off-diagonal cell |
| **Materials** | **Last week's marked Handout 20A** (the 15-row sheet) · a **ruler** · plain paper · a **green** pen or highlighter · a red pen · Handout 21A (the pen/pencil/marker sheet, for homework) |
| **Tech needed** | **None.** Third week running with no computer — and the last one for a while. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** you need **last week's sheet**, already marked, with the eleven Ys on it. Today
> starts from it and builds the grid out of it. If it has gone missing, the data is reprinted in
> §Answer Key K1 — but re-mark it before class, not during.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can, observably:

1. **Tell memorizing apart from generalizing** using the gap between training accuracy and test
   accuracy, and say which of the two they want.
2. **Define overfitting in plain words** — without using the word "fit" — and give an example.
3. **Build a three-by-three confusion matrix by hand** from a scoring sheet, and run the diagonal check
   against the correct count.
4. **Read an off-diagonal cell as a specific, nameable mistake** — "two combs were called toothbrush" —
   and trace it back to something about the data.

---

## 🧑‍🏫 What YOU Need to Know First

*Read this once — about fifteen minutes. Sections 2, 4 and 6 are the ones you cannot teach without.*

### 1. Where we are

- **Week 19** — the student hid fifteen photos in a signed envelope. It is still sealed.
- **Week 20** — they scored somebody else's fifteen-row sheet: 11/15 = 73.3%, against a 33.3% baseline,
  with per-class scores of 100%, 80% and **40%**. They also computed the gap: 100% − 73.3% = 26.7
  percentage points.
- **Today** — the two words behind that gap get their proper meaning, and the 40% gets turned into a
  grid that says *exactly* what went wrong.
- **Week 22** — the envelope opens and they do all of this on their own model.

So today is the last dress rehearsal. Everything the student does today, they will redo next week on
their own numbers, with their own feelings attached. That is exactly why today runs on somebody
else's data.

### 2. Memorizing versus generalizing, and how to tell in ten seconds

> **Generalizing** — the model works on examples it has never seen. This is the only thing you actually
> want.
>
> **Memorizing** — the model works on the exact examples it studied, and falls apart on anything else.

You cannot tell these apart by looking at the model. Nobody can. But you can tell in ten seconds by
comparing two numbers: **the score on the photos it trained on, and the score on the photos it had
never seen.**

| Training accuracy | Test accuracy | What it means |
|:--:|:--:|---|
| 100% | 95% | Generalizing well. It learned the object. ✅ |
| 100% | 73% | Learned something real, and memorised some of the photos too. 🟡 |
| 100% | 40% | Memorised hard. It learned your table, not your comb. ❌ |
| 55% | 52% | Barely learned anything — too few photos, or the task is too hard. 🟠 |

**Read that last row carefully, because it is the trap in the trap.** A *small* gap is not automatically
good news. A model at 55% and 52% has a tiny gap and is useless. You read the gap **and the level**
together, always. The gap tells you about memorising; the level tells you whether anything was learned
at all.

![Two students sitting the same exam](../figures/fig-w21-1-two-students-same-exam.svg)
*Figure 21.1 — Both worked hard. Both got 100% on the sheet they had already seen. Only the new
questions told them apart.*

**The analogy to use, and it is the best one in the module.** Two students both score 100% on the
practice sheet.

Aisha understood how the method works. In the exam, facing questions she has never seen, she scores
95%.

Ben learned that question 3's answer is "42" and question 7's answer is "blue". In the exam he scores
40% and he is genuinely bewildered, because he *did* know all the answers.

**Ben is not lazy. Ben worked extremely hard.** He learned the wrong thing very well. And the crucial
part, which you should say out loud: **on the practice sheet you could not tell them apart.** You
needed the exam.

### 3. The gap, as one subtraction

```
   training accuracy:  60/60 = 100.0%
   test accuracy:      11/15 =  73.3%
   ─────────────────────────────────────
   the gap:                    26.7 percentage points
```

![Training score against test score with the gap arrowed](../figures/fig-w21-2-train-test-gap-bars.svg)
*Figure 21.2 — 100% on its own study material is the boring number. Only the second bar is news.*

A 26.7-point gap says: this model is somewhere between Aisha and Ben, and closer to the middle than
you would like. It has learned something real — 73.3% against a 33.3% baseline is not luck — **and** it
has also memorised something about those specific photos.

### 4. Overfitting, in plain words — and why we avoid the word "fit"

> **Overfitting** — when a model learns its training examples so closely that it stops working on
> anything new. In plain words: **it learned the photos, not the object.**

The formal definitions of this word all lean on "fitting a curve to data", which is a Level 2 picture
and means nothing to an 11-year-old. The plain version above says almost everything the formal version
says, and it is memorable. **Insist on the plain version today.** If the student can say "it learned
the photos, not the object", they will recognise the formal definition instantly when it arrives next
year.

**The second analogy, for the students who need a non-school one — learning your way to school.**

- Version A: *"turn left at the postbox, right at the big tree, straight on past the shop."*
- Version B: *"school is north-east of home; head that way and follow the main road."*

Both get you to school every single morning. Then one day the big tree is cut down. Version A is lost
on a street they have walked four hundred times. Version B does not even notice.

Version A memorised the route. Version B generalised. **And on every normal day, both looked
identical.**

**Three things that make overfitting more likely** — and the student controls all three:

| Cause | Why it does it | The fix |
|---|---|---|
| Too few examples | there is not enough variety for a general pattern to be the easiest one to find | collect more, in more situations |
| Too little variety | the background *is* the easiest pattern, so it gets learned | change room, light, surface, hand, distance |
| Near-duplicate examples | 200 frames of one burst is one example wearing 200 hats | short bursts, and move between them |

And here is the thing to remind them of: **they already built an overfitted model, in Week 18**, before
they had the word. The one-background model scored 95% on the wooden table and collapsed at the sink.
Point at that row in their Week 18 table today. The word is new; the experience is three weeks old.

### 5. The confusion matrix — what it actually is

> **Confusion matrix** — a grid where each **row** is the true class, each **column** is what the model
> said, and each **cell** counts how many examples fell into that combination.

That is all. It is a tally chart with two labels.

```
                        ┌─────── WHAT THE MODEL SAID ───────┐
                        │  spoon    toothbrush     comb     │  total
   ┌────────────────────┼───────────────────────────────────┼───────
   │ TRUTH: spoon       │    5           0          0       │   5
   │ TRUTH: toothbrush  │    0           4          1       │   5
   │ TRUTH: comb        │    1           2          2       │   5
   └────────────────────┴───────────────────────────────────┴───────
     total said              6           6          3       │  15
```

> **Diagonal** — the cells where true equals predicted. The correct answers. Here: 5 + 4 + 2 = 11.
>
> **Off-diagonal cell** — any other cell. Each one is a specific mistake: *this* got called *that*, this
> many times.

**Two checks, and they are not optional:**

1. **The diagonal must equal the number of correct answers** you already counted on the sheet. 5 + 4 +
   2 = 11 ✓
2. **All nine cells must add to the number of test photos.** 15 ✓

These two checks take four seconds and they catch nearly every filling error a student makes. Make them
compulsory today, because next week the student fills a grid from their own sheet with no answer key to
compare against, and the checks will be the only safety net they have.

### 6. How to *read* it — the part that makes the grid worth drawing

**Along a row** — what happened to a class.
*"Of the five real combs: two were called comb, two were called toothbrush, one was called spoon."*
That is the model's weakness **on combs**.

**Down a column** — what the model was willing to say.
*"It said the word 'comb' only three times in fifteen tries, though five combs existed."* That is the
model being **reluctant** about comb — which is a different diagnosis from simply being bad at combs,
and it usually points at that class having too few or too samey training photos.

**And the single most useful number in the grid is the biggest one that is not on the diagonal.** Here
it is the **2** in "true comb, said toothbrush". That cell is a shopping list: it tells you exactly
which photos to go and take tomorrow.

Which, notice, is not surprising once you say it out loud: a comb and a toothbrush are both thin plastic
handles with bristly bits. The grid did not just say "the model is 73.3% accurate". It said *"combs and
toothbrushes look alike to this model"* — a sentence you can act on.

### 7. The two misconceptions you will meet today

**Misconception 1 — "the rows are what the model said."**
This will happen, probably more than once, and it produces a grid that is the *transpose* of the right
one. The fix is a phrase, not an explanation: **"truth down the side, said across the top."** Have them
write the words `TRUTH` down the left edge and `SAID` across the top *before* any numbers go in. If the
grid comes out wrong, the diagonal check will usually still pass (the diagonal is the same either way!),
so this error is genuinely hard to catch later — which is exactly why you catch it by labelling first.

**Misconception 2 — "a 26.7-point gap means the model is 26.7% bad."**
No. The gap is not a quality score. It is a measure of *how much of what it learned was specific to
those exact photos*. A model can have a small gap and be useless (the 55%/52% row) or a large gap and
still be useful (73.3% is a long way above a 33.3% baseline). Gap and level are two different
questions.

### 8. How deep to go, and where to stop

| Go this deep | Stop before |
|---|---|
| Memorizing vs generalizing, told apart by the gap | Bias and variance, learning curves |
| Overfitting = "it learned the photos, not the object" | Any graph with a curve on it; the word "fit" |
| A 3×3 matrix, both checks, rows and columns read out loud | Precision, recall, F1 — Level 2 |
| The biggest off-diagonal cell as a shot list | Regularisation, dropout, early stopping, augmentation |

> **⚠️ Watch out:** do **not** let today drift into fixing the model. The whole point of the shot list
> is that it is a plan for later. And absolutely do not open the Week 19 envelope — that is next week's
> lesson and it only happens once.

---

### 🧭 The Growing Map

**HONEST TESTING** for a third week, and **model** has joined **evaluation** in the strip. That pairing is
exactly today's content: the gap between two scores is a statement about what the model *became*, not just
about how well it did.

![The course map in Week 21: honest testing is this week's box, where two scores tell memorizing from generalizing](../figures/fig-w21-0-where-this-fits.svg)

*Figure 21.0 — Week 21's version. HONEST TESTING still tinted and badged, with **model** and
**evaluation** lit along the bottom.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask:** *"which bit did we do today — third week in the same box, so what did this week
   add?"* The answer you want: Week 19 hid the photos, Week 20 turned them into one number, and today we
   needed **two** numbers plus a grid, because one number could never have told Aisha from Ben.
2. **Then the better question:** *"why has model lit up as well as evaluation this week?"* Because the gap
   is telling you what kind of thing the model is — one that learned the objects, or one that learned the
   photographs. Follow it with the practical one: *"why is WHO IT FAILS still dashed, when the matrix is
   full of mistakes?"* Because a matrix counts mistakes; it does not ask **whose** they are. That is
   Week 31.
3. **Have them write their two scores on their own map** next to HONEST TESTING, with a minus sign between
   them and the answer circled. Label the circle **overfitting**. A word they can now compute is a word
   they will not misuse.

> **🧑‍🏫 Why this is worth two minutes.** This week's two ideas — the gap, and the matrix — are the ones
> most often remembered as unconnected: one is a subtraction and the other is a grid. The map holds them
> together by putting both in the same box, and it sets up next week honestly: Week 22 is where this whole
> box gets pointed at their own model, and the Week 19 envelope is finally opened. Say so, and say that it
> only happens once.

**The six threads** along the bottom are the spine of all four levels. **Model** and **evaluation** are
lit this week. Do not quiz them on the threads; the map is orientation, never assessment.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Find last week's marked Handout 20A.** Eleven Ys, four Ns. If it is gone, print it again from
      §K1 and mark it yourself before class so the student starts from a scored sheet.
- [ ] **Draw the empty 3×3 grid yourself, on paper, with a ruler.** Genuinely do it. You will be drawing
      it live and there is a knack to spacing four rows and four columns on a half-sheet. Two minutes
      now saves a wonky grid in front of the student.
- [ ] **Fill your own copy in from the sheet**, all fifteen tally marks, and check the diagonal comes to
      11. If you have done it once you will spot the student's mis-tally instantly.
- [ ] **Print Handout 21A** — the pen / pencil / marker fifteen-row sheet, with the "correct?" column
      blank. This is the homework. Data in §K4.
- [ ] **Find a green pen or highlighter** for the diagonal, and a red one for the worst cell. Two
      colours; that is all the lesson needs.
- [ ] **Have the Week 18 sabotage table on the table too.** You will point at the one-background row
      when you name overfitting, and it lands much harder as *their own* old result than as a story.

### 5 minutes on the day

- [ ] Handout 20A, marked, flat on the table
- [ ] Plain paper, ruler, pen, green pen, red pen
- [ ] Handout 21A face down (it goes home, not out in the lesson)
- [ ] Board or big sheet with room for the empty grid and four lines of arithmetic
- [ ] The Week 19 envelope in sight and untouched. One more week.

### If something fails

| What fails | Fallback |
|---|---|
| **Last week's sheet is lost** | Reprint from §K1 and mark it yourself before class. Losing the student's own marks costs about four minutes of ownership and nothing else. |
| **No ruler** | The edge of a book. A hand-drawn wobbly grid works exactly as well; the labels are what matter, not the straightness. |
| **The student cannot get the grid to balance** | Do it as a physical tally: fifteen small paper squares, one per sheet row, physically placed into nine drawn boxes. Then count the piles. It is slower and it never goes wrong. |
| **No printer for Handout 21A** | Read the fifteen rows out loud and have them write it down as a warm-up next week, or dictate it as the first five minutes of homework. The data is in §K4. |
| **You are short of time** | Cut the column reading and the prediction. Never cut the diagonal check or the sentence-out-loud step. |

---

## ⏱️ The Lesson, Minute by Minute

| Minutes | Segment | What happens |
|---|---|---|
| 0 – 8 | 🪝 **Hook** — Aisha and Ben | Two students, one exam, and a question you cannot answer from the practice sheet |
| 8 – 26 | 🧠 **Concept** — the gap, overfitting, and the grid | Two words defined, one word banned, the empty grid drawn |
| 26 – 40 | 🔍 **Worked Example** — fill the first six rows together | Tally marks, out loud, one sheet row at a time |
| 40 – 60 | 🎲 **Activity** — Build the Matrix | Finish it, shade the diagonal, check it, then say every mistake out loud |
| 60 – 70 | 🔑 **Wrap & Assign** — the prediction and the shot list | Which cell will be worst on *your* model next week? |

---

### 🪝 Hook — 8 minutes

**Say this:**

> "Two students. Aisha and Ben. Both of them get given the same practice sheet with sixty questions on
> it, and the answers on the back. Both of them work through it until they can do every single one.
> Both of them score **a hundred percent** on the practice sheet."
>
> *(Write `Aisha 100%` and `Ben 100%` on the board.)*
>
> "So: which one of them is better at maths?"
>
> *(Let them answer. Whatever they say — including "the same" — keep going.)*
>
> "Right. Exam day. The paper has fifteen questions on it that neither of them has ever seen."
>
> "Aisha gets 95%."
>
> *(Write it.)*
>
> "Ben gets 40%."
>
> *(Write it. Pause.)*
>
> "And Ben is genuinely upset, and genuinely confused, because — and this is the important bit — **Ben
> did know all the answers.** He knew that question 3 was 42 and question 7 was blue. He worked
> incredibly hard. He learned sixty answers perfectly."
>
> "He just learned the wrong thing. Extremely well."
>
> "Now the question that is actually today's lesson: **on the practice sheet, could you have told them
> apart?**"
>
> *(No. They both got 100%.)*
>
> "No. You couldn't. They looked identical. You needed the exam. And your model is exactly the same
> problem — it will happily tell you it got 100% on the photos it studied, and that tells you
> absolutely nothing about which of these two it is."

**Do this:** draw two stick students on the board with their two pairs of numbers, and write between
them the number that matters:

```
   Aisha:  practice 100%   exam 95%    gap  5 points
   Ben:    practice 100%   exam 40%    gap 60 points
```

**Ask this:**

> **1. "What's the one number that tells them apart?"**
> - *Hoping for:* the difference between the two scores — the gap.
> - *If they say "the exam score":* good and nearly right. Push: "Aisha got 95 and Ben got 40 — but what
>   if a third student got 40 on the practice sheet AND 40 on the exam?" *(Different problem: that one
>   learned nothing. So you need both numbers, not one.)*
> - *If they're stuck:* point at the two pairs and say "subtract".

> **2. "Is Ben stupid?"**
> - *Hoping for:* no — he learned the wrong thing / he memorised.
> - This question matters more than it looks. Students hear "memorising" as an insult, and it isn't one:
>   memorising is a real strategy that works brilliantly right up until the moment it doesn't. Say so.

> **3. "Which one is your model?"**
> - *Hoping for:* a guess, and "we don't know yet".
> - Write the guess down. Next week they find out for real.

---

### 🧠 Concept — 18 minutes

**Say this (part 1 — the two words):**

> "Two words for the two students, and you'll use both for the rest of your life."
>
> "**Generalizing** is what Aisha did. The model works on examples it has never seen. This is the only
> thing you actually want — always, every time, in every situation."
>
> "**Memorizing** is what Ben did. It works on the exact examples it studied and falls apart on
> anything else."
>
> "And you tell them apart with one subtraction. Score on the photos it studied, minus score on the
> photos it never saw. We did that sum last week — a hundred minus seventy-three point three."
>
> *(Let them produce 26.7.)*
>
> "Twenty-six point seven **percentage points** — good, you said points. That gap is how much
> memorising happened."

**Say this (part 2 — the word, in plain language):**

> "There's a proper name for what Ben's version does, and you will meet this word for the rest of your
> life if you go anywhere near this subject. It's **overfitting**."
>
> "And I want you to learn the plain version, not the fancy one, because the plain version is honestly
> most of what the fancy one says:"
>
> *(Write it on the board, in a box.)*
>
> **"Overfitting: it learned the photos, not the object."**
>
> "That's it. Not the object — the photos. The wooden table in the corner of every picture. Your left
> hand. The shadow. The smudge on the spoon."
>
> "And here's the thing — **you already built one of these.** Three weeks ago, in Week 18. Look at your
> table."
>
> *(Point at the one-background row: 95% on the wooden table, wrong at the sink.)*
>
> "That model scored *higher* than your good model where it was trained, and it fell over two metres
> away. You built a textbook overfitted model in about ten minutes and you didn't have a word for it.
> Now you do."

> **💡 Try this:** ask them to explain overfitting to you without using the words "fit", "fitting" or
> "overfit". If they can produce "it learned the photos, not the object" or their own version of it,
> objective 2 is met and you can move on.

**Say this (part 3 — why one number isn't enough, and the grid):**

> "Last week you found that the 73.3% was hiding a class at 40%. Per-class accuracy told you **which
> class** was broken. But it didn't tell you **what it was getting confused with** — and that's the
> thing you'd actually need to fix it."
>
> "So here's the tool. It's a grid, and it's honestly just a tally chart with two labels."
>
> *(Draw the empty grid on the board as you talk. Labels first, always labels first.)*
>
> "Down the side: **the truth.** True spoon, true toothbrush, true comb. Across the top: **what the
> model said.** Said spoon, said toothbrush, said comb."
>
> "Then you go down your scoring sheet, one row at a time, and put one mark in the box where the truth
> meets what it said. Fifteen rows on the sheet, fifteen marks in the grid. It's called a **confusion
> matrix**, because it shows you exactly what got confused with what."
>
> "And two special names. The boxes going diagonally from top-left to bottom-right — those are the ones
> where the truth and the guess **match.** That's the **diagonal**, and it's all your correct answers.
> Every other box is an **off-diagonal cell**, and every single one of them is a mistake you can say
> out loud in a sentence."

**Do this:** the board, in this order — labels, then grid, then the two definitions, then the empty grid
left up for the whole lesson.

![Week 21 finished board](../figures/fig-w21-3-board-plan.svg)
*Figure 21.3 — What the board should look like at minute 26. Leave the empty grid up; the student rules
their own copy in the activity.*

Then hand them the template so the shape is unambiguous before any numbers arrive:

![An empty three by three confusion matrix, ready to fill](../figures/fig-w21-4-empty-matrix-template.svg)
*Figure 21.4 — Rows are the truth. Columns are what the model said. Label both before you write a
single number.*

**Ask this:**

> **1. "Which way round do the labels go?"**
> - *Hoping for:* truth down the side, what it said across the top.
> - *If they get it backwards:* fix it immediately and give them the phrase to say: "truth down, said
>   across." Do not explain it twice — the phrase does more work than an explanation, and getting it
>   backwards is the single most common error in the week.

> **2. "How many marks will end up in the grid, and how do you know before you start?"**
> - *Hoping for:* fifteen, because there are fifteen rows on the sheet and each row goes in exactly one
>   box.
> - This is the second check, arriving before it is needed. If they can say it now they will use it
>   later.

> **3. "If the model got everything right, what would the grid look like?"**
> - *Hoping for:* 5, 5, 5 down the diagonal and zero everywhere else.
> - Lovely follow-up: *"and if it got everything wrong?"* **Nothing on the diagonal at all** — which is
>   a genuinely strange-looking grid and worth picturing.

> **4. "Explain overfitting without using the word 'fit'."**
> - *Hoping for:* it learned the photos, not the object.
> - *If they use "fit":* ban it playfully and make them go again. The constraint is the whole exercise.

---

### 🔍 Worked Example Together — 14 minutes

**Build the top half of the matrix together.** You hold the ruler; they hold the pen.

**Step 1 — rule the grid (3 min).** On plain paper, a four-by-four grid: three rows and three columns of
cells, plus a totals column on the right. Then — **before any numbers** — write:

- `true spoon`, `true toothbrush`, `true comb` down the left,
- `said spoon`, `said toothbrush`, `said comb` across the top.

Say it out loud while they write it: *"truth down the side, said across the top."*

**Step 2 — the first six sheet rows, out loud (6 min).** Take last week's marked Handout 20A. For each
row, the student says the sentence and then makes the mark. The sentence matters; do not let them skip
it into silent tallying.

| Sheet row | Say this out loud | Mark goes in |
|:--:|---|---|
| 1 | "true spoon, said spoon" | true spoon / said spoon |
| 2 | "true spoon, said spoon" | true spoon / said spoon |
| 3 | "true spoon, said spoon" | true spoon / said spoon |
| 4 | "true spoon, said spoon" | true spoon / said spoon |
| 5 | "true spoon, said spoon" | true spoon / said spoon |
| 6 | "true toothbrush, said toothbrush" | true toothbrush / said toothbrush |

After row 5, stop and point at it: the whole `true spoon` row has five marks in one box and nothing
anywhere else. **That is what a class the model has completely solved looks like.** It is worth naming
now, because it makes the comb row look shocking later.

**Step 3 — cross off as you go (1 min of habit-building).** Show them: put a small tick beside each
sheet row as its mark goes in. This is how you avoid the classic disaster of tallying row 9 twice and
row 10 never.

**Step 4 — the interesting one, together (4 min).** Row 10: *true toothbrush, said comb.*

Stop here and ask the questions below before the mark goes down. This is the first off-diagonal cell of
the lesson and it deserves ten seconds of ceremony.

**Ask this:**

> **1. "Row 10 — where does this one go, and why is it different from the last nine?"**
> - *Hoping for:* it goes in true toothbrush / said comb, and it is different because it is off the
>   diagonal — it is a mistake.
> - *If they put it in "true comb / said toothbrush":* the most common slip in the lesson. Go back to the
>   sheet and read the row out loud, slowly: "TRUE toothbrush. SAID comb." Then: "so which row of the
>   grid are we in?" The row is fixed by the truth, always.

> **2. "Say row 10 as a sentence about the world."**
> - *Hoping for:* "a toothbrush was called a comb."
> - This is the skill of the whole week in one line, and it is worth practising on an easy cell before
>   it matters.

> **3. "Before we do the last five rows — how many marks should be in the grid so far, and how many are
> there?"**
> - *Hoping for:* ten, and ten.
> - If it does not come to ten, find the missing or doubled row **now**, not at the end. This is a
>   thirty-second habit that saves five-minute disasters.

---

### 🎲 Activity — 20 minutes

**Build the Matrix.** They finish the grid alone, shade and check the diagonal, then turn every
off-diagonal cell into a spoken sentence and trace the biggest one back to the photos.

Full instructions in the next section.

---

### 🔑 Wrap & Assign — 10 minutes

**Do this:** put the two bars back up and connect the grid to the gap.

![Training score against test score with the gap arrowed](../figures/fig-w21-2-train-test-gap-bars.svg)
*Figure 21.2, again — the gap. Now you know what the 26.7 points were made of: four specific mistakes,
three of them combs.*

**Say this:**

> "Look at where the four mistakes ended up. Not spread evenly around the grid — **three of the four
> are in the comb row.** So that 26.7-point gap isn't a vague fog of 'it's a bit memorised'. It's four
> specific photos, and three of them were combs, and two of those got called toothbrush."
>
> "That's the difference between a number and a diagnosis. '73.3% accurate' is a number. 'Combs and
> toothbrushes look alike to this model, and here are the two photos where it happened' is something
> you can actually go and fix."

**Then the prediction, which is the real assignment (3 min).**

> "Next week we open your envelope. Fifteen of your own photos that your model has never seen. And
> you're going to build this same grid out of your own results."
>
> "So: **which cell of your grid do you think will be the worst?** Write it down. Which of your three
> classes will get confused with which, and why?"

Make them write a full sentence with a reason, then date it and initial it. Next week you read it out
before opening the envelope. This is the same prediction discipline they used in Week 18 and it is
worth more than the score.

**Ask this:**

> **1. "Which cell will be worst on your model, and why?"**
> - *Hoping for:* a named pair and a reason grounded in their photos — "toothbrush called comb, because
>   they're both thin with bristles and I photographed both on the same table."
> - *If they say "I don't know":* offer the scaffold: "which two of your three objects look most alike?"
>   Then: "and which one did you take the fewest photos of?" Either route gives a prediction.

> **2. "If your grid's diagonal doesn't match your correct count next week, what's happened?"**
> - *Hoping for:* a tally mark went in the wrong box, or a row got counted twice or missed.
> - This is the last thing you say about the matrix and it is the thing that will save next week's
>   lesson.

---

## 🎲 The Activity, In Full

### Build the Matrix

**Time:** 20 minutes · **Group size:** one student, one adult
**Materials:** last week's marked Handout 20A · the part-built grid from the worked example · ruler ·
pen · green pen · red pen

**What "finished" looks like:** a hand-drawn 3×3 grid with fifteen marks in it, the diagonal shaded
green and summed to 11, every off-diagonal cell spoken aloud as a sentence, the biggest one circled in
red, and a written prediction about their own model.

### Step 1 — Finish the grid (5 min)

Rows 11 to 15 of the sheet, one at a time, saying each as a sentence before marking it:

| Sheet row | Sentence | Cell |
|:--:|---|---|
| 11 | "true comb, said comb" | comb / comb |
| 12 | "true comb, said comb" | comb / comb |
| 13 | "true comb, said toothbrush" | comb / toothbrush |
| 14 | "true comb, said toothbrush" | comb / toothbrush |
| 15 | "true comb, said spoon" | comb / spoon |

Then convert the tally marks to numbers and write in the row totals. The finished grid:

| | **said spoon** | **said toothbrush** | **said comb** | row total |
|---|:--:|:--:|:--:|:--:|
| **true spoon** | **5** | 0 | 0 | 5 |
| **true toothbrush** | 0 | **4** | 1 | 5 |
| **true comb** | 1 | 2 | **2** | 5 |
| **total said** | 6 | 6 | 3 | **15** |

### Step 2 — Shade the diagonal and check it (3 min)

Green pen. Shade the three cells where the truth and the guess match: top-left, middle, bottom-right.
Then add them up and write the sum outside the grid.

```
   diagonal:  5 + 4 + 2  =  11
   correct count on the sheet:  11        ✓ they match
   all nine cells:  5+0+0 + 0+4+1 + 1+2+2  =  15   ✓ same as the number of photos
```

![A filled confusion matrix with the diagonal shaded and one mistake circled](../figures/fig-w21-5-filled-matrix-diagonal.svg)
*Figure 21.5 — The diagonal is what went right. Every cell off it is a sentence you can say out loud.*

**Say this:**

> "Those two checks are the whole reason this grid is safe to trust. If the diagonal doesn't match your
> correct count, a mark went in the wrong box. If the nine cells don't add up to fifteen, you missed a
> row or counted one twice. Four seconds, both of them, every time. Next week there'll be nobody to
> compare against, so these checks are all you'll have."

### Step 3 — Say every mistake out loud (6 min)

This is the part that makes the grid worth drawing. There are **four** off-diagonal cells with numbers
in them. Each one becomes a full sentence, said aloud, in the form *"N of X were called Y."*

```
   true toothbrush → said comb,   1   →  "one toothbrush was called a comb."
   true comb → said spoon,        1   →  "one comb was called a spoon."
   true comb → said toothbrush,   2   →  "TWO COMBS WERE CALLED TOOTHBRUSH."
```

Then read the empty cells too, because zeros are information:

```
   true spoon → said toothbrush,  0
   true spoon → said comb,        0   →  "no spoon was ever mistaken for anything."
   true toothbrush → said spoon,  0
   true comb → ... nothing is zero — every comb cell has something in it.
```

**Circle the 2 in red.** It is the biggest number that is not on the diagonal, and that makes it the
most useful single number in the grid.

**Then read down the columns (2 of the 6 minutes).** This is a second, different reading and it gives a
different answer.

```
   said spoon:      6 times, but only 5 spoons existed   →  slightly over-eager
   said toothbrush: 6 times, but only 5 toothbrushes     →  slightly over-eager
   said comb:       3 times, though 5 combs existed      →  RELUCTANT about comb
```

**Say this:**

> "That's a different diagnosis from 'it's bad at combs'. If it were just bad at combs, its comb guesses
> would be scattered about randomly. This model has partly stopped **believing in** combs — it only
> used the word three times in fifteen tries. That usually means the comb photos were too few, or all
> too similar to each other."

### Step 4 — Trace the biggest cell back to the photos (4 min)

Take the red-circled cell — two combs called toothbrush — and ask the question that turns a grid into a
plan.

**Ask this:**

> **1. "Why would a comb and a toothbrush look alike to a machine?"**
> - *Hoping for:* they're both thin, both plastic, both have a handle and bristly bits, both about the
>   same size.
> - *If they say "they don't look alike at all":* ask them to describe each one in five words without
>   using its name. The descriptions come out nearly identical, which is the point.

> **2. "The confusion runs one way more than the other. Check it."**
> - Two combs were called toothbrush; **one** toothbrush was called comb. So it is not quite symmetric —
>   combs suffer more.
> - The reasoning to draw out: if the two objects simply looked alike, you would expect roughly equal
>   confusion in both directions. Lopsided confusion points at the *class* — too few comb photos, or
>   comb photos that were all too similar — rather than at the resemblance.

> **3. "Name the ten photos you'd take tomorrow. Not 'more combs'."**
> - *Hoping for:* something specific. A full-credit answer looks like: *"five photos of the comb
>   standing up in a mug so it isn't lying flat, and five of the comb next to a toothbrush at the same
>   distance so size is the only difference."*
> - *If they say "more combs":* "How many, where, and doing what?" Push until it is a list you could
>   actually follow.

### Step 5 — The prediction (2 min)

Written, dated, initialled: which cell of *their* grid will be worst next week, and why. See §Wrap.

### Variation — easier

Use a **2×2 grid** instead of 3×3. Collapse the sheet to two classes: `comb` and `not comb` (so rows
1–10 are all "not comb"). The grid becomes:

| | said comb | said not comb | total |
|---|:--:|:--:|:--:|
| **true comb** | 2 | 3 | 5 |
| **true not comb** | 1 | 9 | 10 |
| **total** | 3 | 12 | **15** |

Diagonal 2 + 9 = 11 ✓, all cells = 15 ✓. Four boxes instead of nine, the same two checks, the same
sentences. Then, if there is time, show them the 3×3 version you filled in yourself and let them see
what the extra detail buys.

Skip the column reading and the prediction. Keep the sentences out loud.

### Variation — harder

1. **Predict the grid before filling it.** Cover the sheet. From the per-class numbers alone (100%, 80%,
   40%) sketch what the grid must look like. They can deduce the diagonal exactly — 5, 4, 2 — but *not*
   where the four mistakes went. Realising which part is deducible and which part needs the raw data is
   a genuinely sophisticated insight.
2. **The transpose trap.** Hand them a grid that has been filled in the wrong way round (truth across
   the top) and ask them to prove it is wrong. The diagonal still comes to 11, so the checks pass — the
   only way to catch it is to read a cell as a sentence and notice it says something that didn't happen.
   This is worth doing; it shows that checks are necessary but not sufficient.
3. **A 4×4 grid.** Add an `other` class (Week 16) with five photos of a fork. Where do those five land?
   Anywhere at all, probably scattered. That row is what a model does with something it has never been
   given a box for.
4. **Fifty photos, same percentages.** "If you tested on 50 photos per class instead of 5 and got the
   same per-class percentages, what would the grid look like?" *(50, 40, 20 on the diagonal, and the
   mistakes ten times bigger.)* Then: "which grid would you trust more, and why?" *(The big one — one
   photo is worth 0.7 points instead of 6.7.)*

---

## ❓ Questions Students Ask This Week

**1. "Is memorizing always bad?"**
For a model, in this situation, yes — because you want it to work on new photos and memorising
specifically doesn't do that. But be careful with the word: memorising is a perfectly good strategy for
some jobs. If you want to remember your own phone number, memorising is exactly right and generalising
would be ridiculous. It's bad here because of *what we're asking the model to do*.

**2. "How big a gap is too big?"**
**Nobody knows for sure, and here's why:** there's no threshold, because it depends on how much data you
had, how varied it was, how hard the task is, and what you need the model for. A 5-point gap on a
million photos and a 5-point gap on fifteen photos mean completely different things. What everyone
agrees on is the *direction*: smaller gap, better — as long as the test score itself is high. That last
clause is the whole trick, because 55% and 52% is a tiny gap and a useless model.

**3. "Why is it called a confusion matrix? That's a weird name."**
Because it shows you what the model got **confused** about — literally which thing it mixed up with
which. "Matrix" is just a maths word for a grid of numbers. So: a grid of confusions. It's one of the
few pieces of jargon in this whole field that means exactly what it says.

**4. "Can the diagonal ever be zero?"**
Yes, and it would mean the model got every single answer wrong, which is strange and interesting rather
than just bad. A model that is reliably wrong knows something — if it called every spoon a comb and
every comb a spoon, you could fix it by swapping two labels. Being wrong in a *pattern* is much more
useful than being wrong at random.

**5. "Does 100% on the training photos mean the model is good at least at those?"**
It means it can reproduce answers it has already been given, which is a much smaller achievement than
it sounds. Ben also knew all sixty practice answers perfectly. The uncomfortable truth is that 100% on
training tells you almost nothing at all — it's what you'd expect from a good model and a memorising
one equally.

**6. "My model might get 15 out of 15 next week. Is that suspicious?"**
It might be brilliant and it might be a warning. The question to ask is about the photos, not the score:
were the fifteen genuinely taken on a different day, in a different room, with different light? If yes —
excellent, and say so in your write-up. If they were from the same session as your training photos,
then 15/15 is what a lazy split looks like and the number doesn't mean anything. Also: fifteen photos is
a small sample. 15/15 is encouraging, not proof.

**7. "Can I fix the model now that I know it's bad at combs?"**
Not from this grid, and here's the trap: this grid came from somebody else's model. And next week, when
you have your *own* grid, the same rule applies — the moment you change something because the test set
told you to, the test set has helped train the model and it stops being hidden. The right move is a shot
list for a *fresh* round, sealed all over again.

**8. "Did the model know it was getting them wrong?"**
No — and you can see it on the sheet. Look at the confidences on the four wrong rows: 54%, 58%, 66%,
49%. They're lower than the right answers, so there's a hint there. But row 14 got 66% and was wrong,
while row 12 got 63% and was right. **They overlap.** There's no confidence number you could use as a
clean line between right and wrong. That was Week 16's lesson and it's still true.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| **The grid gets built the wrong way round** (truth across the top) | Both layouts look equally sensible, and the diagonal check *still passes*, so nothing catches it. | Prevent it: make them write `TRUTH` down the left and `SAID` across the top before any number goes in. If it has already happened, don't rub it out — read one cell aloud as a sentence and let them hear that it describes something that didn't happen. |
| **A sheet row gets tallied twice, or missed** | Fifteen rows, nine boxes, eyes going back and forth. | The tick-as-you-go habit from the worked example. If the total isn't 15, do not hunt cell by cell — recount the *sheet* against the ticks. |
| **The diagonal check gets skipped** | It feels like showing off; the grid looks finished. | Make it a written line, not a mental note: `5 + 4 + 2 = 11 = correct count ✓`. Written checks get done; remembered checks don't. |
| **"It got confused" is the whole reading** | Naming the specific mistake is much harder than seeing that there is one. | Give them the sentence frame and refuse anything else: *"___ of the ___s were called ___."* Fill in the first blank for them once, then wait. |
| **The student wants to fix the model right now** | The red-circled cell makes the fix look obvious and urgent. | Redirect the energy into the shot list: "Write down the exact ten photos. That's a real job and it's tomorrow's." Naming the photos scratches the itch without touching anything. |
| **"Memorizing" is heard as an insult** | At school, memorising is what you're told to do. | Say the Ben sentence out loud: "Ben worked really hard and learned the wrong thing extremely well." Nobody in this story is lazy or stupid. |
| **The gap gets treated as a grade** | It is a number with a percent sign near it. | Show them the 55%/52% row. Tiny gap, useless model. Gap and level are two separate questions and you always ask both. |
| **They want to open the envelope, today, now** | Three weeks of it sitting there and the lesson is *about* testing. | "Next week. And it only happens once, so it happens properly." Move the envelope out of sight for the rest of the lesson. |

---

## 🧭 Differentiation

### If they are struggling

**Cut:** the column reading; the zero cells; the prediction (do it verbally instead of in writing).

**Use the 2×2 grid** (§Variation — easier). Four boxes, comb versus not-comb. The two checks and the
sentences survive intact and the bookkeeping stops being the obstacle.

**Reteach the grid as physical sorting.** Draw nine big boxes on a sheet of A3 or on the table with
tape. Write each of the fifteen sheet rows on a scrap of paper. Then *place* each scrap into a box. Now
the grid is a physical sorting task and the tally error becomes impossible. Count the piles at the end.
It takes four minutes longer and it never goes wrong.

**Reteach memorizing versus generalizing with something they can act out.** Ask them to memorise a
five-word sentence, then ask them to say a *different* sentence about the same subject. First is
memorising; second is generalising. Ninety seconds, no numbers.

**The 60-minute version:** Hook 6 · Concept 15 · Worked example 12 (rows 1–6 only) · Activity 17 (finish
the grid, shade, check, say the three mistakes) · Wrap 10. Cut columns, zeros and the harder tracing.

**Keep, whatever else goes:** the sentence *"two combs were called toothbrush"*, said out loud, and the
diagonal check.

### If they are flying

1. **The transpose trap** (§Variation — harder, item 2). The insight — that a check can pass on a wrong
   answer — is the most grown-up idea available this week.
2. **Predict the grid from the per-class numbers alone** (item 1). Then discuss what was deducible and
   what wasn't.
3. **Trace it to the collection log.** Get out their Week 15 photo log. "You've got the counts per
   background. If you were the model, which class had the least variety to learn from?" Connecting a
   number in a grid back to a decision they made with a camera five weeks ago is the whole course in one
   move.
4. **The asymmetry question.** "Two combs called toothbrush, one toothbrush called comb. Why isn't
   confusion symmetric?" Real answers: fewer comb photos; less varied comb photos; the comb happens to
   look like a toothbrush from more angles than the reverse. All three are testable and they'd each need
   a different fix.

### If they won't engage today

**Plan A — they build the grid, you fill it in wrong.** Deliberately. Put row 13 in the wrong box and
let them catch you with the diagonal check. Being the person who catches the error is far more
appealing than being the person who avoids it.

**Plan B — do it as a bingo game.** Nine boxes, fifteen tokens (coins, buttons, torn paper). Call out
the sheet rows like a bingo caller — "true comb, said toothbrush!" — and they place a token. Same
activity, zero writing.

**Plan C — the four-minute floor.** One question: *"Two combs got called toothbrush. Why would a machine
mix those two up?"* Then: *"name two photos that would help."* That single exchange carries the week's
big idea, and the grid can be a Week 22 warm-up.

---

## ✅ Assessing Understanding

### Check 1 — the two words, cold

> **"A model gets 100% on the photos it studied and 45% on photos it had never seen. What's happened,
> and what's the gap?"**

- **Good:** it memorised the photos — it's overfitting. The gap is 55 percentage points.
- **Partial:** "it's bad" or "it's overfitting" with no gap computed. Ask for the subtraction and the
  unit.
- **Not good enough:** "it's 45% good." Go back to Aisha and Ben on the board, sixty seconds, then
  re-ask.

### Check 2 — overfitting, in their own words

> **"Explain overfitting to me without using the word 'fit'."**

- **Good:** "it learned the photos, not the object" — or their own version: "it learned my table", "it
  memorised the pictures instead of the thing in them".
- **Partial:** "it's when it does badly on new stuff." True but it's the *symptom*, not the mechanism.
  Ask: "why does it do badly?"
- **Not good enough:** repeats a definition with "fitting" in it. That's a recital, not understanding.
  Give them the Week 18 one-background row and ask what that model had learned.

### Check 3 — read a cell

> **"Point at any cell that isn't on the diagonal and say what it means, in a sentence about real
> objects."**

- **Good:** "two combs were called toothbrush." Any correct cell, said as a sentence with a number in
  it.
- **Partial:** "that's the comb-toothbrush one." Names the cell, doesn't say the sentence. Ask: "so what
  happened, with the number in it?"
- **Not good enough:** "that's where it got confused." Give the frame — *"___ of the ___s were called
  ___"* — and wait.

### Mastery scale for this week

| Level | What it looks like |
|:--:|---|
| **1** | Copies the grid. Puts marks in roughly the right places with help. Cannot say what the diagonal is. |
| **2** | Fills the grid with prompting. Knows the diagonal is the correct answers. Says "it got confused" without naming what with what. |
| **3** | Builds a labelled 3×3 grid from the sheet unaided, runs the diagonal check, and reads at least two off-diagonal cells as proper sentences. Computes the gap with the right unit. Defines overfitting in plain words. |
| **4** | All of the above plus the column reading — spots that the model said "comb" only three times in fifteen tries and calls that reluctance. Traces the biggest cell back to something specific about the photos. Names ten specific photos that would help. |
| **5** | Notices the confusion is asymmetric and reasons about why. Deduces the diagonal from the per-class percentages before filling the grid. Catches a transposed grid by reading a cell aloud, and can explain why the diagonal check couldn't catch it. |

**Aim for 3.** Level 4 is exactly the readiness you want for Week 22.

---

## 📤 Homework to Assign

**Workbook:** Week 21, pages 1–3. **Time: about 50 minutes.**

**Say this, word for word:**

> "This is somebody else's model again — the last time, I promise. It's a **pen, pencil and marker**
> classifier, and it's a fifteen-row sheet exactly like the one we did today. Handout 21A."
>
> "Page one: mark the fifteen rows, then overall accuracy three ways with the division shown, then
> per-class accuracy for all three classes. Exactly what you did last week — you should be quick at it
> now."
>
> "Page two: draw its confusion matrix. Ruler. Labels first — truth down the side, said across the top.
> Row totals, column totals, and **both checks written down**, not just done in your head."
>
> "Page three, and this is the marked bit: **three sentences naming what got confused with what.** In
> the shape 'two markers were called pen.' Then one sentence — one — saying what you'd go and look at
> first. Not 'more photos'. Which photos, of what, and why."
>
> "And write down your prediction for your own model. Which cell will be worst next week? You've got a
> week to think about it and you can't change it after Wednesday."

**Check before they leave:** ask them to say the labels out loud — "truth down the side, said across the
top." If that comes back without hesitation, page 2 will be fine.

| Page | Task | Approx. time |
|---|---|---|
| 1 | Mark Handout 21A; overall accuracy three ways; per-class accuracy | 20 min |
| 2 | The confusion matrix, ruled and labelled, with row totals, column totals and both checks | 15 min |
| 3 | Three "what got confused with what" sentences, one investigate-first sentence, and the prediction for their own model | 15 min |

---

## 🔑 Answer Key

### K1 — Handout 20A, reprinted (in case last week's sheet is lost)

| # | true class | predicted | top conf. | correct? |
|:--:|---|---|:--:|:--:|
| 1 | spoon | spoon | 94% | Y |
| 2 | spoon | spoon | 88% | Y |
| 3 | spoon | spoon | 91% | Y |
| 4 | spoon | spoon | 76% | Y |
| 5 | spoon | spoon | 82% | Y |
| 6 | toothbrush | toothbrush | 90% | Y |
| 7 | toothbrush | toothbrush | 85% | Y |
| 8 | toothbrush | toothbrush | 71% | Y |
| 9 | toothbrush | toothbrush | 68% | Y |
| 10 | toothbrush | **comb** | 54% | N |
| 11 | comb | comb | 79% | Y |
| 12 | comb | comb | 63% | Y |
| 13 | comb | **toothbrush** | 58% | N |
| 14 | comb | **toothbrush** | 66% | N |
| 15 | comb | **spoon** | 49% | N |

11 correct. 11/15 = 0.7333 = 73.3%. Per class: spoon 5/5 = 100%, toothbrush 4/5 = 80%, comb 2/5 = 40%.
Training accuracy 60/60 = 100%, so the gap is 26.7 percentage points.

### K2 — The in-class confusion matrix

| | **said spoon** | **said toothbrush** | **said comb** | row total |
|---|:--:|:--:|:--:|:--:|
| **true spoon** | **5** | 0 | 0 | 5 |
| **true toothbrush** | 0 | **4** | 1 | 5 |
| **true comb** | 1 | 2 | **2** | 5 |
| **total said** | 6 | 6 | 3 | **15** |

**Checks:** diagonal 5 + 4 + 2 = **11** = the correct count ✓ · all nine cells = **15** = the number of
photos ✓

**Reading along the rows:**
- Spoons: never confused with anything. A perfect row.
- Toothbrushes: one escaped into `comb`.
- Combs: scattered — 2 right, 2 called toothbrush, 1 called spoon.

**Reading down the columns:**
- Said `spoon` 6 times, but only 5 spoons existed → slightly over-eager.
- Said `toothbrush` 6 times, but only 5 existed → slightly over-eager.
- Said `comb` only **3** times, though 5 combs existed → **under-predicting comb.** The model is
  reluctant to use that word at all, which points at the comb class having too few or too samey
  training photos rather than at combs and toothbrushes merely resembling each other.

**The four off-diagonal cells, as sentences:**
1. "One toothbrush was called a comb." *(1)*
2. "One comb was called a spoon." *(1)*
3. **"Two combs were called toothbrush."** *(2 — the biggest, and the one to circle)*
4. And the zeros are information too: no spoon was ever mistaken for anything.

**Why cell 3 is the useful one:** it is the largest number not on the diagonal, so it names the single
confusion worth attacking — combs and toothbrushes look alike to this model. Which is not surprising:
both are thin plastic handles with bristly bits, at roughly the same size.

**The ten-photo shot list (model answer):**

> Five photos of the comb standing upright in a mug so it isn't lying flat like a toothbrush, and five
> of the comb next to a toothbrush at the same distance so that size and tooth-spacing are the only
> differences available.

### K3 — Every question posed in the lesson

| Segment | Question | Answer |
|---|---|---|
| Hook | Which student is better at maths? | You cannot tell from the practice sheet — both scored 100%. |
| Hook | What's the one number that tells them apart? | The gap between practice score and exam score: 5 points vs 60 points. |
| Hook | Is Ben stupid? | No. He worked hard and learned the wrong thing extremely well. |
| Hook | Which one is your model? | A written guess, checked in Week 22. |
| Concept | Which way round do the labels go? | Truth down the side, what it said across the top. |
| Concept | How many marks end up in the grid? | Fifteen — one per sheet row. Known before you start. |
| Concept | What would a perfect grid look like? | 5, 5, 5 on the diagonal and zero everywhere else. |
| Concept | Explain overfitting without "fit". | It learned the photos, not the object. |
| Worked ex. | Row 10 — where does it go? | true toothbrush / said comb. The row is fixed by the truth, always. |
| Worked ex. | Say row 10 as a sentence. | "A toothbrush was called a comb." |
| Worked ex. | How many marks so far? | Ten after ten rows. If not, find the error now. |
| Activity | Why would a comb and a toothbrush look alike to a machine? | Both thin, plastic, handle plus bristly bits, similar size. |
| Activity | Is the confusion symmetric? | No — 2 one way, 1 the other. Lopsided confusion points at the comb class itself, not at the resemblance. |
| Activity | Name the ten photos you'd take tomorrow. | Specific: comb upright in a mug ×5, comb beside a toothbrush at equal distance ×5. |
| Wrap | Which cell will be worst on your model, and why? | A written, dated prediction with a reason. |
| Wrap | If the diagonal doesn't match, what's happened? | A mark went in the wrong box, or a sheet row was doubled or missed. |

### K4 — Handout 21A: the homework sheet (the data to print, "correct?" blank)

A pen / pencil / marker classifier, 15 held-out photos, 5 per class.

| # | true | predicted | top conf. | correct? |
|:--:|---|---|:--:|:--:|
| 1 | pen | pen | 91% | Y |
| 2 | pen | pen | 84% | Y |
| 3 | pen | **marker** | 57% | N |
| 4 | pen | pen | 88% | Y |
| 5 | pen | pen | 72% | Y |
| 6 | pencil | pencil | 93% | Y |
| 7 | pencil | pencil | 81% | Y |
| 8 | pencil | pencil | 77% | Y |
| 9 | pencil | **pen** | 61% | N |
| 10 | pencil | pencil | 86% | Y |
| 11 | marker | marker | 89% | Y |
| 12 | marker | marker | 74% | Y |
| 13 | marker | **pen** | 55% | N |
| 14 | marker | marker | 68% | Y |
| 15 | marker | **pen** | 52% | N |

### K5 — Workbook page 1: scoring Handout 21A

**Correct rows:** 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 14 → **11 correct out of 15**.

```
   FRACTION:    11 / 15
   DECIMAL:     15 × 0.7 = 10.5;  11 − 10.5 = 0.5;  0.5 ÷ 15 = 0.0333
                0.7 + 0.0333 = 0.7333
   PERCENTAGE:  73.3%

   baseline (3 equal classes) = 33.3%
   beats baseline by 40 percentage points
```

**Per-class accuracy:**

| class | correct | total | fraction | decimal | percentage |
|---|:--:|:--:|---|---|---|
| pen | 4 | 5 | 4/5 | 0.800 | **80.0%** |
| pencil | 4 | 5 | 4/5 | 0.800 | **80.0%** |
| marker | 3 | 5 | 3/5 | 0.600 | **60.0%** |
| **overall** | **11** | **15** | **11/15** | **0.733** | **73.3%** |

Checks: 4 + 4 + 3 = 11 ✓ · 5 + 5 + 5 = 15 ✓

> **🧑‍🏫 Note the coincidence and use it.** This model also scores 11/15 = 73.3% overall, exactly like
> the one in class — but its per-class numbers are 80 / 80 / 60 instead of 100 / 80 / 40, and its
> mistakes land in completely different cells. **Same headline, different machine.** If the student
> notices this unprompted, it is the best possible answer on the page. If they don't, point it out when
> you mark it: it is the whole argument for per-class numbers in a single comparison.

### K6 — Workbook page 2: the confusion matrix for Handout 21A

| | **said pen** | **said pencil** | **said marker** | row total |
|---|:--:|:--:|:--:|:--:|
| **true pen** | **4** | 0 | 1 | 5 |
| **true pencil** | 1 | **4** | 0 | 5 |
| **true marker** | 2 | 0 | **3** | 5 |
| **total said** | 7 | 4 | 4 | **15** |

**Checks:** diagonal 4 + 4 + 3 = **11** ✓ matches the correct count · all cells = **15** ✓ · column
totals 7 + 4 + 4 = 15 ✓

**Reading down the columns:** it said `pen` **7** times when only 5 pens existed — the model is
over-eager about pen. It said `pencil` 4 times and `marker` 4 times against 5 of each.

### K7 — Workbook page 3: the sentences

**The three sentences (model answers):**

1. **"Two markers were called pen."** *(the biggest off-diagonal cell, and the one to circle)*
2. "One pencil was called a pen."
3. "One pen was called a marker."

Accept any three correct cells said in the right shape. Full credit requires a number, a true class and
a predicted class in each sentence. Refuse "it mixed up pens and markers" as a sentence — it has no
number and no direction.

**Bonus observation, worth extra credit if they get it:** the confusion is **not symmetric**. Two
markers were called pen, but only *one* pen was called a marker. And nothing at all was ever called a
pencil that wasn't one. The traffic runs towards `pen`.

**The one investigate-first sentence (model answers).** Any of these earns full marks:

> "I'd look at whether the marker photos were taken with the cap on, because a capped marker is
> basically a fat pen, and the model called two markers 'pen' but only one pen 'marker'."

> "I'd count the training photos per class first, and check whether `pen` had more than the others,
> because the model said 'pen' seven times when there were only five — it's over-eager about that
> class."

> "I'd look at the size of the objects in the photos, because if the marker and pen were photographed
> at different distances then size isn't a reliable clue and the model has nothing else to go on."

**Not enough:** "get more marker photos", "train it for longer", "make it better". Hand these back with
the question: *"look at what, exactly?"*

**The prediction for their own model.** No right answer. Full credit needs three things: a named pair
(true class X will get called Y), a reason grounded in their own photos, and a date. Strong examples:

> "I think toothbrush will get called comb, because they're the two thinnest objects and I took nearly
> all my toothbrush photos flat on the table where it looks most like a comb."

> "I think comb will be worst, because I know I took fewer comb photos than the others — I got bored by
> the third class."

That second one is a superb answer, because it traces a prediction about a grid back to a decision they
made with a camera. Say so.

---

## 🔮 Next Week Preview

Next week is **Week 22 — The Hidden Ten**, and it is the week all of this has been for. The Week 19
envelope comes out, the signature gets broken, and the student scores fifteen photos of their own that
their own model has never seen — in pen, one at a time, no re-shows, no second attempts. Then they
compute all four numbers, build the grid, and write a one-sentence verdict on their own work: number,
sample size, baseline, worst class, commonest mistake.

Everything today was a rehearsal for that, and it should feel like one.

**Prep early:**

- **Find the envelope and check the signature is intact. Do not open it.** Not to count the photos, not
  to check they came out. If you have already opened it, there is an honest repair in the Week 22 prep
  checklist and it starts with telling the student.
- **Get their model loading.** Open Teachable Machine, load their Week 17 model, test it once with any
  object, and check the webcam permission still works. Do this the night before, not in the lesson.
- **Find their training accuracy** — from their Week 17 notes or from **Advanced → Under the hood**. You
  need it for the gap.
- **A pen, not a pencil.** Week 22 is explicit about this: a pencil invites going back and "fixing" row
  4 after seeing row 12.
- **Keep today's grid and today's prediction.** Week 22 opens by reading the prediction out loud before
  anything is unsealed.

---

[⬅ Week 20](week-20.md) · [Course Home](../README.md) · [Week 22 ➡](week-22.md) · [Student Guide](../student-guide/week-21.md) · [Workbook](../workbook/week-21.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
