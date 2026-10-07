# Week 7 — Doing It 100 Times Without Typing It 100 Times

[⬅ Week 6](week-06.md) · [Course Home](../README.md) · [Week 8 ➡](week-08.md) · [Student Guide](../student-guide/week-07.md) · [Workbook](../workbook/week-07.md)

---

## 📋 At a Glance

This table is the lesson on one page. Check it the night before.

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟩 Lab — two new shapes (`for` and the accumulator) built by hand, then broken on purpose |
| **Big idea** | A `for` loop repeats a block once per item, and an accumulator variable carries a running total across the repeats. |
| **New vocabulary** | loop · iteration · range · accumulator · off-by-one |
| **New syntax** | `for i in range(n):` · `range(start, stop, step)` · `total += x` · `"=" * 20` · `print(x, end=" ")` |
| **Materials** | The printed Week 7 workbook (all sections; Build It prints best in landscape) · pencil · notebook open at the **Bug Log** · **one index card with these twelve scores written large: 88 92 70 65 100 54 78 81 47 90 62 73** · a printed copy of the times-table grid (the paper fallback) |
| **Tech needed** | One laptop, Python 3, terminal in `~/ai-academy/level2`, editor with 4-space indent. Standard library only — **nothing to install**. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** the planted bug at the end of this lesson has **no error message**. The program asks for eleven scores instead of twelve. The only way to catch it is to **count the lines on the screen and compare them to the numbers on the card**.
>
> If you say "you're missing one" you have taken away the only thing this lesson is really teaching. Hand them the card, ask them to tick each number off as it goes in, and let them notice that they still have a number left over.

---

## 🎯 Lesson Objectives

These are the five things the student should be able to do when the lesson ends. The Assessing Understanding checks test them.

By the end of the lesson the student can:

1. **Write a `for` loop over `range()` and predict exactly how many times it runs**, before running it.
2. **Explain why `range(4)` gives 0, 1, 2, 3 and not 1, 2, 3, 4**, using the "stop minus start" argument.
3. **Build an accumulator** that totals a set of numbers, then divide by the count to get an average.
4. **Hand-check that average on paper**, showing the division, and match it to the program's answer.
5. **Find an off-by-one bug by counting output lines against input items** — twelve in, eleven out.

Observable evidence: a 9 × 9 times-table grid printed by two loops with aligned columns; a twelve-score totaller whose running total is printed on every pass; the division `900 ÷ 12 = 75` worked on paper next to the program's `75.00`; and a Bug Log entry for a bug that produced no error message at all.

---

## 🧑‍🏫 What YOU Need to Know First

This section is your own background reading, so you can teach loops without having programmed before. It comes before the lesson plan.

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to have programmed before to teach this.** Everything below is written for an adult who has never written a line of code, in the order you will need it. Read it once with the laptop open and type the six short programs as you go. About 25 minutes.

This is the week programs stop being the same length as the job they do. Everything so far has been one line of code per thing that happens. From today, **three lines of code can do a hundred things**, and that changes what a program *is*.

### 1. A loop is a block that runs more than once

Here is the whole idea, in five lines you can type right now. Make a file called `count_to_four.py`:

```python
# count_to_four.py - the smallest loop there is.

for i in range(4):          # i takes the values 0, 1, 2, 3 - one per pass
    print(i)                # indented, so this line belongs to the loop

print("done")               # NOT indented, so this runs once, after the loop
```

Run it with `python3 count_to_four.py`. The real output:

```text
0
1
2
3
done
```

> **loop** — a block of code that Python runs more than once.
>
> **iteration** — one single run through the block. Four numbers came out, so there were four iterations. Out loud, "iteration" and "pass" mean the same thing, and "pass" is the word to use with a 12-year-old.

**Four lines came out of one `print`.** That is the whole week. Look at the file again and count the `print(i)` lines: there is one. Look at the output and count the numbers: there are four.

### 2. Every part of `for i in range(4):`, explained

Six things are happening in that line. A student who can name all six can debug it; a student who has memorised its shape cannot.

| Part | What it is | What happens if you get it wrong |
|---|---|---|
| `for` | The keyword that starts this kind of loop. | Every `for` loop starts with it. There is no other spelling (`while`, a different keyword, is next week). |
| `i` | **A variable that Python fills in for you.** You choose the name; Python chooses the value, once per pass. | Any legal name works. `for n`, `for row`, `for score` — all fine, and usually better than `i`. |
| `in` | A keyword. It sits between the name and the values. | Leave it out and you get a `SyntaxError`. |
| `range(4)` | Where the values come from. `range(4)` hands out 0, 1, 2, 3 — one per pass. | Give it text instead of a number and you get a `TypeError`. |
| `:` | The colon. It means "the indented block below belongs to me." | Leave it out and you get `SyntaxError: expected ':'`. This will happen today. |
| the indent | Four spaces. **Indentation is how Python knows what to repeat.** | Get it wrong and either nothing repeats, or the wrong thing does. |

The two sentences worth saying out loud, both of which the student needs by minute 20:

- **"`i` is not a number you set. It is a box Python refills for you, once per pass."**
- **"The indent is not decoration. It is the loop's body. Move a line out of the indent and it stops being part of the loop."**

That second one is not a style rule in Python the way it is in most languages. It is the actual grammar. Type this to see the proof:

```python
total = 0
for n in range(1, 4):
    total += n
    print(f"inside : total is {total}")
print(f"outside: total is {total}")
```

```text
inside : total is 1
inside : total is 3
inside : total is 6
outside: total is 6
```

Three lines from the indented `print`, one line from the one at the margin. **Same two lines of code; the only difference is four spaces.**

### 3. Where the values come from: `range`, and the thing everybody gets wrong

> **range** — a value factory. You tell it where to start, where to stop, and how big a step to take, and it hands out one whole number per pass.

Here are the forms you will use, with what each one hands out:

| You write | You get | Read it as |
|---|---|---|
| `range(4)` | 0, 1, 2, 3 | "four values, starting at 0" |
| `range(1, 5)` | 1, 2, 3, 4 | "start at 1, **stop before** 5" |
| `range(0, 101, 10)` | 0, 10, 20 … 100 | "start at 0, stop before 101, in steps of 10" |
| `range(10, 0, -1)` | 10, 9, 8 … 1 | "count down" |

**`range(4)` gives you four values, and the last one is 3.** This catches every beginner alive, exactly once. It is worth spending three minutes on rather than thirty seconds.

Type this file, `steps.py`, to see the real output of the step forms:

```python
# steps.py - range with a third number: the step.

print("Counting in tens:")
for n in range(0, 101, 10):        # start 0, stop before 101, step 10
    print(n, end=" ")              # end=" " puts a space instead of a new line
print()                            # a bare print() ends the line

print("Counting in threes:")
for n in range(3, 31, 3):          # 3, 6, 9 ... 30
    print(n, end=" ")
print()

print("Counting backwards:")
for n in range(10, 0, -1):         # a negative step counts DOWN
    print(n, end=" ")
print()
```

```text
Counting in tens:
0 10 20 30 40 50 60 70 80 90 100 
Counting in threes:
3 6 9 12 15 18 21 24 27 30 
Counting backwards:
10 9 8 7 6 5 4 3 2 1 
```

**Why does it stop early? Give the student the honest reason, because there is one.** It is not a quirk and it is not an accident.

**Because then the count is a subtraction.** When the stop is above the start, `range(a, b)` hands out exactly `b - a` values. `range(1, 5)` → 5 − 1 = 4 values.

With a step the count changes: `range(0, 101, 10)` → eleven values (0, 10 … 100), so count those rather than subtracting. If `range` included the stop number, every count would be "the difference, plus one", and *that* plus-one would be the thing everybody got wrong instead.

![The stop number is a fence post, not a value](../figures/fig-w07-2-range-starts-at-zero.svg)
*Figure 7.1 — The stop number is a fence post you count up to, not a value you get handed. That is what makes the count a clean subtraction.*

The sentence to say, and to make them repeat: **"range stops *before* the number you give it."**

Two special cases look like bugs and are not. Know them before a student finds them:

```python
for n in range(3, 3):      # start equals stop
    print(n)
for n in range(10, 1):     # stop is BELOW start, with no negative step
    print(n)
```

Both print **nothing at all**. Zero passes, no error.

`3 - 3 = 0` values, and `1 - 10` is below zero, which also means none (you cannot hand out fewer than nothing). If a student's loop produces no output whatsoever, check this first.

### 4. The counter is a box Python refills

![One value per trip round the loop](../figures/fig-w07-1-loop-circular-counter.svg)
*Figure 7.2 — The hub is the counter. Each trip round, it holds exactly one of the values `range` handed out. Passes 1 and 2 are done; pass 3 is happening; passes 4 to 10 have not happened yet.*

**This is the figure to teach the concept from, and it is aimed at you as much as at the student.** Point at the hub and say "this is `n`". Point at the ring and say "this is one pass". Point at the shaded values and say "these already happened". Point at the blank ones and say "these have not happened yet, and nothing in them exists".

One thing is worth knowing so it does not surprise you. After the loop finishes, the counter still holds its **last** value.

```python
for n in range(1, 6):
    pass_number = n
print(f"after the loop, n is still {n}")
```

```text
after the loop, n is still 5
```

That is useful sometimes and confusing often. **Do not teach it today.** If a student finds it, tell them the truth in one sentence, "the box keeps whatever went in last", and move on.

### 5. The accumulator: the most reused shape in all of programming

This is the second half of the week, and the more important half.

> **accumulator** — a variable created **before** a loop and updated **inside** it, so that after the loop it holds a result built from every single pass.

```python
# running_total.py - an accumulator, with the running total shown every pass.

total = 0                                  # the accumulator. Set up BEFORE the loop.

for n in range(1, 6):                      # n takes 1, 2, 3, 4, 5
    total += n                             # add this n to the running total
    print(f"after adding {n}, total = {total}")

print(f"final total = {total}")            # NOT indented - runs once, at the end
```

```text
after adding 1, total = 1
after adding 2, total = 3
after adding 3, total = 6
after adding 4, total = 10
after adding 5, total = 15
final total = 15
```

Check it by hand: 1 + 2 + 3 + 4 + 5 = 15 ✔

**`total += n` is new syntax and it needs its own sentence.** It means, exactly: *take what is in `total`, add `n` to it, and put the answer back in `total`.*

It is a shortcut for `total = total + n`, and for numbers the two are identical. The shortcut is just shorter and harder to typo. There are three more in the same family that you will see: `-=`, `*=`, and `/=`.

**Three rules for an accumulator, and every accumulator bug is one of these three:**

1. **Set it up before the loop.** `total = 0` goes *above* the `for`, at the margin. If it goes inside, it gets wiped every pass.
2. **Update it inside the loop**, in the indent.
3. **Use it after the loop**, at the margin. Divide there. Print there.

![The running total fills up](../figures/fig-w07-3-accumulator-filling-up.svg)
*Figure 7.3 — One box, twelve additions, one division at the very end. The box is not twelve boxes; it is one box whose contents change.*

There are two ways to break an accumulator, and you will meet both today. **Type both.**

**Break 1 — the set-up goes inside.** No error message. The answer is the last number, every time.

```python
total = 0
for n in range(1, 6):
    total = 0          # <-- reset INSIDE the loop: wipes the total every pass
    total += n
print(total)
```

```text
5
```

**Break 2 — the division goes inside.** No error message. It divides before it has finished adding, so you get four wrong averages and the last one happens to be right.

```python
total = 0
for n in range(1, 6):
    total += n
    average = total / 5      # <-- divided INSIDE the loop
    print(f"average so far: {average:.2f}")
```

```text
average so far: 0.20
average so far: 0.60
average so far: 1.20
average so far: 2.00
average so far: 3.00
```

Neither of these is an error as far as Python is concerned. They are last week's silent bugs wearing new clothes, and the cure is the same: **predict the answer before you run, then look at whether the output makes sense.**

### 6. `"=" * 20` — multiplying text

This one is a gift and it takes twenty seconds. Type these two lines:

```python
print("=" * 20)
print("=" * 40)
```

```text
====================
========================================
```

`*` with two numbers means multiply. **`*` with a piece of text and a number means "repeat that text that many times."** In Week 4 the student typed forty equals signs by hand to draw a border. That is now one character and a number, and if they want the border longer they change the number.

Watch for two things:

- `"=" * "20"` is a `TypeError`. You cannot repeat text *text* times. The number must be a number.
- `"=" + 20` is a different `TypeError`. `+` glues text to text; it will not glue a number on.

### 7. Two small helpers you need for the grid

The grid activity needs two things that are not on this week's syntax list. They are small, they are not concepts, and you should teach them as tools rather than ideas.

**`end=""`** — normally `print` finishes by moving to a new line. `end=""` tells it to finish with *nothing*, so the next `print` carries on the same line. A bare `print()` with nothing in it then ends the line. That is how you build one line out of many prints.

**`f"{value:>4}"`** — the student met `:.2f` in Week 3 as "an instruction about how to show this value". `:>4` is another instruction from the same family: *"right-align this in four characters' worth of space."*

It is what makes columns line up. `7` becomes three spaces and a 7; `70` becomes two spaces and a 70. Both are four characters wide, so they stack.

That is all either of them does. **Do not open the whole formatting system.** If a student asks what else goes after the colon, the honest answer is "a lot, and we'll meet the useful ones when we need them."

### 8. A loop inside a loop, in one paragraph

For the grid you need one loop inside another. There is no new syntax. It is two `for` loops, the second one indented inside the first. The rule you need is the arithmetic. Type this:

```python
lines = 0
for row in range(1, 4):
    for col in range(1, 5):
        lines += 1
print(f"3 rows x 4 columns = {lines} passes of the inner block")
```

```text
3 rows x 4 columns = 12 passes of the inner block
```

**The inner loop runs all the way through, every single time the outer loop takes one step.** Three outer passes × four inner passes = twelve passes of the innermost line. For the 9 × 9 grid that is 81 numbers printed by one `print`.

The one thing that goes wrong is this: the bare `print()` that ends each row must be indented to the **outer** loop, not the inner one. Put it in the inner loop and every number gets its own line.

### 9. Off-by-one: the bug this lesson is built on

> **off-by-one** — a loop that runs one time too many or one time too few. Almost always a `range` boundary, and almost always silent.

There are three shapes, and you will meet all three this year:

- **Shape A** — forgetting that `range` stops early.
- **Shape B** — the fence-post problem.
- **Shape C** — the planted bug in today's activity.

**Shape A — forgot that `range` stops early.**

```python
# Goal: print the numbers 1 to 10.
for n in range(1, 10):
    print(n, end=" ")
print()
```

```text
1 2 3 4 5 6 7 8 9 
```

Nine numbers, no error. The fix is `range(1, 11)`.

**Shape B — the fence-post problem.** Five items have four gaps between them, but a loop that prints an item and then a divider prints five dividers:

```python
for i in range(1, 4):
    print(f"item {i}")
    print("-----")
```

```text
item 1
-----
item 2
-----
item 3
-----
```

Three items, three dividers, and the last one is dangling. Five fence panels need six posts; three items have only two gaps. Say the name out loud, because once it has a name it is easy to find.

**Shape C — the planted bug in today's activity.** The student wants to label their twelve scores 1 to 12, so they very reasonably write `range(1, 12)`. That hands out 1 through 11.

**Eleven prompts appear for twelve scores, and then the program divides by twelve anyway.** Total 827 instead of 900; average 68.92 instead of 75.

![Twelve scores in, eleven scores counted](../figures/fig-w07-4-off-by-one-missing-row.svg)
*Figure 7.4 — Nothing crashed. The card still has a number on it, and the average is quietly wrong. The only tool that finds this is counting.*

**The cure is a habit rather than a rule: count the output lines and compare them with the number of things that went in.** Twelve numbers on the card, eleven prompts on the screen. That comparison takes four seconds, and it is the most valuable reflex in this lesson.

### 10. The three misconceptions you will actually meet

**Misconception 1 — "`i` is something I have to set."** A student writes `i = 0` above the loop, or tries `i = i + 1` inside it. Both are harmless and both mean the mental model is wrong. **The fix:** cover the loop body and ask "who puts a value in `i`?" The answer is `range`, through the `for` line. Then Figure 7.2, hand on the hub.

**Misconception 2 — "`range(10)` counts to 10."** This is not stupidity; it is what the word "range" means in English.

**The fix is a number, not an explanation.** Have them run `for n in range(10): print(n, end=" ")` and count the numbers out loud with a finger. Ten numbers, last one 9. Then ask "how many values does `range(10)` hand out?" — ten. "What is the last one?" — nine. Both true at once, and that is the whole difficulty.

**Misconception 3 — "the total prints twelve times, so there are twelve totals."** A student sees the running total printed on every pass and concludes there are twelve totals. There is one box; it changes twelve times.

**The fix:** an actual box. Put a coin in a cup, then another, then another, counting out loud. There is one cup. Figure 7.3 is the same picture.

### 11. How deep to go, and where to stop

**Go this far:**

- `for` with `range` in all three forms
- predicting the number of passes before running
- the indent deciding what repeats
- `total += x` and the three accumulator rules
- dividing after the loop
- `"=" * 20`
- `end=""` and `:>4` as tools
- one loop inside another for the grid
- counting output lines to find an off-by-one

**Stop before:**

- `while` (that is next week, and mixing the two today halves what lands)
- looping over a list of things instead of a range of numbers (Week 12)
- `break` and `continue` (next week)
- `enumerate` (Week 14)
- anything about "why not use a list here" — the honest answer is that lists arrive in Week 11 and this week is deliberately doing it the long way so that the short way means something.

**If a fast student asks for the sum 1 to 100**, give it to them, because it is glorious. Type this:

```python
total = 0
for n in range(1, 101):            # 1, 2, 3 ... 100  (stops before 101)
    total += n
print(f"1 + 2 + ... + 100 = {total}")
```

```text
1 + 2 + ... + 100 = 5050
```

Then check it against the formula a mathematician would use: 100 × 101 ÷ 2 = 5050 ✔. Two different methods, same answer. That is what a correct program feels like.

---

### 12. 🧭 The Growing Map — two minutes at the end of the lesson

The student guide carries a figure called **Where This Fits**. It is the same picture every week with one
more piece filled in, and it is the only thing in this course that shows the learner the *shape* of what
they are building rather than this week's content.

![The Level 2 pipeline in Week 7: stage one's first tile is done and its second tile, choices and loops, is where you are](../figures/fig-w07-0-where-this-fits.svg)

*Figure 7.0 — Week 7's version. The first tile of stage one has turned plain white — done, and never
tinted again — and the gold badge has moved down to `choices · loops`, where it stays until Week 9.*

**How to run it, in about two minutes:**

1. **Show it before you say anything.** Then: *"we added a hundred numbers today in three lines — which
   box on this map was that?"* They should point at the gold `choices · loops` tile. Pointing is the
   whole exercise; do not ask them to explain it.
2. **Then the better question:** *"the box above it went white this week — what's in it?"* You want
   "print and variables and maths, that's finished". A learner who can name what is behind them has a
   sense of progress that no mark out of ten gives them.
3. **Then the dashed question:** *"why is most of this still dotted?"* — "because we haven't got there
   yet". Finish by having them update their own pencil copy in the inside cover of their notebook.

> **🧑‍🏫 Why this is worth two minutes.** Week 7 is the first week where the new thing is genuinely
> *harder* than the last thing, and some of the class will privately conclude they are falling behind.
> Two white boxes on a map is evidence against that conclusion, and it is evidence they can see.

> **⚠️ Watch out:** do not turn it into a quiz. The map is orientation, not assessment. If nobody
> remembers which thread is lit, that costs you nothing at all.

---

## 🧰 Prep Checklist

This section lists what to prepare the night before and on the day, and what to do if something fails. The complete runnable files live here.

### 15 minutes the night before

- [ ] **Print the whole Week 7 workbook.** The Build It section (the grid and the accumulator table) prints better in landscape.
- [ ] **Write the twelve-score index card**, big enough to read across a table:

  ```text
  88  92  70  65  100  54  78  81  47  90  62  73
  ```

  These twelve numbers total **900**, which divides by 12 to give **exactly 75**. That is deliberate: the hand-check has to come out clean, or the student will blame the arithmetic instead of the program.
- [ ] **Type and run `seven_times.py` yourself.** This is the file you will build in front of them, so build it once alone first.

  ```python
  # seven_times.py - the 7 times table, printed by a loop.

  print("=" * 20)                    # 20 equals signs, made by multiplying text
  print("  THE 7 TIMES TABLE")
  print("=" * 20)

  for n in range(1, 11):             # n takes 1, 2, 3 ... 10  (stops BEFORE 11)
      answer = 7 * n                 # work out this row's answer
      print(f"7 x {n} = {answer}")   # print one row per pass

  print("=" * 20)
  ```

  The exact expected output:

  ```text
  ====================
    THE 7 TIMES TABLE
  ====================
  7 x 1 = 7
  7 x 2 = 14
  7 x 3 = 21
  7 x 4 = 28
  7 x 5 = 35
  7 x 6 = 42
  7 x 7 = 49
  7 x 8 = 56
  7 x 9 = 63
  7 x 10 = 70
  ====================
  ```

  **Then change the 7 to a 13 — one character — and run it again.** Notice how that felt. That feeling is the hook.
- [ ] **Break the colon on purpose.** Delete the `:` from the `for` line, run it, and read the message:

  ```text
    File "/Users/you/ai-academy/level2/seven_times.py", line 7
      for n in range(1, 11)
                           ^
  SyntaxError: expected ':'
  ```

  You are going to make this mistake deliberately in front of the student at minute 24. Make it once in private first so your recovery looks unhurried.
- [ ] **Run `tables.py`** (the 9 × 9 grid, in the Activity section below) and check the columns line up on *your* screen and in *your* font. If they do not, the terminal font is not fixed-width, and that is worth knowing before the lesson rather than during it.
- [ ] **Do the hand-check yourself, on paper, with a pencil.** 900 ÷ 12. Write it out as long division. You are going to ask a 12-year-old to do this and you should have done it in the last twelve hours.
- [ ] Say the big idea out loud: *"one print, many lines — and the counter is a box Python refills."*

### 5 minutes on the day

- [ ] Terminal open in `~/ai-academy/level2`. Run last week's `grade.py` once — ten seconds, and it proves the setup still works.
- [ ] Editor open, **4-space indent confirmed.** This week is the first week where a wrong indent silently changes the answer instead of just looking untidy.
- [ ] An **empty** editor window ready. The Hook needs them typing into nothing.
- [ ] The twelve-score index card face down on the table.
- [ ] Notebook open at the Bug Log. Workbook on the table.
- [ ] A stopwatch or a phone timer. The Hook is timed, and the timing is the point.

### Fallback if the laptop or the install fails

| If this fails | Do this instead |
|---|---|
| **No laptop** | The paper version is genuinely good. Hand out the printed 9 × 9 grid with about a third of the cells blank and have them fill it in — that *is* the inner loop, done by hand, and they will feel the repetition. Then the accumulator on paper: the twelve scores in a column, and a second column where they write the running total after each one. Their second column will read 88, 180, 250, 315, 415, 469, 547, 628, 675, 765, 827, 900. **That column is Figure 7.3**, drawn by them. Finish with the division. |
| **Python not installed** | The paper version above is a complete 70-minute lesson. Do the install afterwards. |
| **The columns do not line up on screen** | The terminal is using a proportional font. Either change the terminal font to a monospaced one (Menlo, Consolas, Courier), or drop the `:>4` alignment entirely and print `f"{row} x {col} = {row * col}"` one per line. The loop lesson survives; only the prettiness is lost. |
| **The student already knows `for` loops** | Skip the Hook's typing race and go straight to `range(1, 12)`. Ask: *"how many prompts will this print?"* If they say twelve, you have your lesson. If they say eleven, give them the harder variation — the fence-post problem — which almost nobody has already met. |
| **The off-by-one is spotted instantly** | Excellent, and rarer than you would think. Flip it: **they** plant a bug in your copy while you look away, and you have to find it by counting. Being the one who sets the trap is a different and better relationship to the material. |

---

## ⏱️ The Lesson, Minute by Minute

This section is the script for the whole lesson. The table shows the five segments and their timings; each segment follows below.

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — Type It Out By Hand | 7 | 7 | A timed race they lose, then three lines that win |
| 🧠 Concept — The Box Python Refills | 16 | 23 | `for`, `range`, the zero, the accumulator |
| 💻 Live-Code Together — The Table and the Total | 18 | 41 | Two deliberate mistakes, one loud and one silent |
| 🎲 Their Turn — The Grid and the Twelve Scores | 20 | 61 | The grid, the accumulator, the planted off-by-one |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, Bug Log, homework |

---

### 🪝 Hook — Type It Out By Hand (7 minutes)

This segment lets the student feel the cost of repeating work by hand, so the loop has a reason to exist.

**Do this:** An empty editor window on the student's screen. Nothing else. You have the timer.

**Say this:**

> "Right. I want the seven times table on the screen. Seven ones are seven, all the way up to seven tens are seventy. Ten lines. Exactly like this:
>
> `7 x 1 = 7`
>
> You know everything you need — `print`, a bit of text, some maths. **You've got sixty seconds. Go.**"

Start the timer. Say nothing while they type. They will get somewhere between four and seven lines done, and they will be typing `print("7 x 4 = 28")` or `print(f"7 x 4 = {7 * 4}")`, and their hands will be getting bored.

At sixty seconds, stop them.

**Say this:**

> "Stop. How many did you get?"

(Four? Five?)

> "Okay. Now the real question. **How long would the thirteen times table take?**"

(The same. Another minute.)

> "And the thirteen times table up to a hundred? Not to ten — to a hundred."

Let them do the arithmetic on that. A hundred lines. Ten minutes of typing, minimum, and every one of those hundred lines is a chance to typo.

> "Here's the thing that should annoy you. Those ten lines you typed are *almost identical*. The only difference between line four and line five is one character. You typed `print` five times to say one idea five times. And a computer's entire reason for existing is doing the same thing over and over without getting bored or making mistakes.
>
> So watch this. I'm going to write the whole table in three lines, and then I'm going to change it to the thirteen times table by editing **one character.**"

**Do this:** on the shared screen, type — slowly, saying each part out loud:

```python
for n in range(1, 11):
    print(f"7 x {n} = {7 * n}")
```

Run it. The real output:

```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

Let it sit for a second. Then change both 7s to 13s and run it again. Then change `11` to `101` and run it again — a hundred rows scroll past.

**Say this:**

> "Two lines. A hundred rows. And I want you to notice something about the *shape* of what just happened, because it is the shape of every program you will write from now on.
>
> There is **one** `print` in that file. Look at it. One. And a hundred lines came out of it. That is not a trick and it is not a shortcut — it is a completely different way of writing down what you want. Instead of writing down every line you want printed, you write down the *pattern*, and you say how many times.
>
> That thing on the first line is called a **loop**. One trip round it — one run through the indented part — is called a **pass**, or if you want the proper word, an **iteration**. That file did a hundred iterations. You did five in sixty seconds."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "How many `print` lines are in my file?" | One. | If they say ten, point at the file and count with them. This has to be certain before anything else happens. |
| "How many lines came out?" | Ten. Then a hundred. | Fine either way — the mismatch is the point. |
| "What's the *only* difference between the row for 4 and the row for 5?" | The number. Everything else is identical. | If they say "the answer's different too" — right, and the answer is *made from* the number. That is why one line can produce both. |
| "How long would a thousand rows take you by hand?" | Hours. And it would have typos in it. | If they say "I'd copy and paste" — excellent, and then they would have to edit a thousand numbers. Ask how many they would get wrong. |
| "Is anything on the screen right now something you could not have typed by hand?" | No. **The loop does not do anything new. It does the same thing, without the typing.** | This one matters. A loop is not magic and it is not clever. It is *the same work*, written once. |

---

### 🧠 Concept — The Box Python Refills (16 minutes)

This segment teaches the counter, `range` and the accumulator, using the loop from the Hook as the worked example.

**Do this:** the loop from the Hook is still on the screen. Leave it there. It is the worked example.

**Say this — part 1, the counter:**

> "Look at the letter `n` on the first line. I want to be really clear about what it is, because this is where people get stuck.
>
> `n` is a **variable** — a box with a name on it, exactly like `pizza_price` in Week 2. But here's the difference, and it's the only new idea in the first half of today's lesson: **you do not put anything in this box. Python does. Once per pass.**
>
> First pass, Python puts 1 in it. Runs the indented line. Comes back. Puts 2 in it. Runs the indented line. Comes back. Puts 3 in. And so on, until it runs out of values — and then it stops on its own and carries on with whatever comes after the loop.
>
> You never write `n = 1`. You never write `n = n + 1`. If you find yourself typing either of those, something has gone wrong in your head about what the `for` line is *for*."

Show Figure 7.2. Put a finger on the hub.

> "The hub of that ring is `n`. Right now it says 3, which means we are on the third pass. The two shaded values already happened. The seven blank ones have not happened yet — and here is the important part — **nothing in them exists yet.** There is no fourth pass anywhere in the computer waiting to happen. There is only ever *this* pass."

**Say this — part 2, where the values come from:**

> "So where do the numbers come from? From that thing that looks like `range(1, 11)`. **`range` is a value factory.** You tell it where to start and where to stop, and it hands out one whole number per pass.
>
> And now the thing that catches every single person who learns to program, including me, including everyone you will ever work with. Type this and count what comes out."

Have them type it themselves:

```python
for n in range(4):
    print(n)
```

```text
0
1
2
3
```

> "Read them out. How many numbers?"

(Four.)

> "What's the last one?"

(Three.)

> "Both of those are true at the same time and that's what makes it hard. **`range(4)` hands out four values, and the last one is 3.** It starts at zero and it stops *before* the number you gave it. Say that back to me."

(range stops before the number you give it.)

> "Again, and this time say it like you're annoyed about it."

Make them say it twice. It is worth the theatre; this exact sentence saves them an hour of confusion later in the term.

> "Now — *why*? Because it isn't random, and knowing the reason is what makes it stick.
>
> Because it makes counting a subtraction. `range(1, 11)` gives 11 − 1 = **ten** values. `range(0, 4)` gives 4 − 0 = **four**. You never have to think 'difference plus one'. If range included the last number, then *every single count* in every program in the world would be 'the difference, plus one' — and that plus-one would be the thing everybody got wrong instead. They moved the problem to the place where it is easiest to remember."

Show Figure 7.1. Point at the fence post.

**Say this — part 3, the accumulator:**

> "Second half. This one's bigger than the loop, honestly, and it's the shape you'll still be using in April.
>
> Suppose I want the *total* of the twelve scores on this card, not just to print them. Where does the total live? Not in the loop's counter — that gets refilled every pass and the old value is gone. So I need my own box, and I need it to *survive* from one pass to the next.
>
> That box is called an **accumulator**. It's a variable you make **before** the loop starts, and you update it **inside** the loop, so that when the loop is over it holds something built out of every pass."

Type it in front of them and run it:

```python
total = 0                                  # the accumulator. Set up BEFORE the loop.

for n in range(1, 6):                      # n takes 1, 2, 3, 4, 5
    total += n                             # add this n to the running total
    print(f"after adding {n}, total = {total}")

print(f"final total = {total}")            # NOT indented - runs once, at the end
```

```text
after adding 1, total = 1
after adding 2, total = 3
after adding 3, total = 6
after adding 4, total = 10
after adding 5, total = 15
final total = 15
```

> "`total += n` — that's the new bit. It means: take what's in `total`, add `n` to it, put the answer back in `total`. It is exactly the same as writing `total = total + n`, and you may write it that way if you prefer. Everyone writes `+=` because it's shorter and because there's only one place to make a typo instead of two.
>
> Look at the middle column of the output. One, three, six, ten, fifteen. **That is not five totals. That is one box, five times.** Same box. The number in it changes."

Show Figure 7.3.

> "And three rules, which between them are every accumulator bug you will ever have:
>
> **One: set it up before the loop.** At the margin, above the `for`.
> **Two: update it inside the loop.** In the indent.
> **Three: use it after the loop.** Divide there. Print the final answer there.
>
> The indent is doing all the work in those three rules. Which is why I'm going to make an indent mistake on purpose in about four minutes, so you can watch what it looks like."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Who puts a value in `n`?" | Python does, through the `for` line — one value per pass. | If they say "I do" — cover the loop body and ask them to find the line where `n` gets set. There isn't one. |
| "`range(4)` — how many values, and what's the last one?" | Four values; the last is 3. | If they say "four, and the last is 4" — run it, count out loud with a finger on the screen. Do not explain; count. |
| "How many values does `range(3, 20)` hand out?" | 17. Twenty minus three. | If they guess, walk them to the subtraction. That is the whole trick. |
| "Why does the total have to be created before the loop?" | Because a box made inside the loop gets made fresh every pass, so it can never carry anything across. | If they cannot say it, show Break 1 from section 5 and let the answer `5` do the arguing. |
| "Is `total += n` different from `total = total + n`?" | No. Identical. Shorter to type, harder to typo. | If they think `+=` is faster or cleverer, say plainly that it is not; it is the same instruction with less typing. |
| "In my accumulator program, how many boxes named `total` are there?" | One. | This is Misconception 3. If they say five, put five coins in one cup, one at a time, counting out loud. |

---

### 💻 Live-Code Together — The Table and the Total (18 minutes)

This segment has the student type the table and the total with you, and shows two mistakes being made and fixed in front of them.

**Do this:** The student types every character. You type on the shared screen at the same pace. Three passes, and **two deliberate mistakes that you make and fix in front of them.**

#### Pass 1 (5 min) — the table, with a border

**Exact keystroke sequence.** Say the file name out loud, have them create it, then type these lines in this order:

```python
# seven_times.py - the 7 times table, printed by a loop.

print("=" * 20)                    # 20 equals signs, made by multiplying text
print("  THE 7 TIMES TABLE")
print("=" * 20)

for n in range(1, 11):             # n takes 1, 2, 3 ... 10  (stops BEFORE 11)
    answer = 7 * n                 # work out this row's answer
    print(f"7 x {n} = {answer}")   # print one row per pass

print("=" * 20)
```

Stop after the first `print("=" * 20)` and run it, before typing anything else. One line of output:

```text
====================
```

**Say this:**

> "Twenty equals signs, and I typed one. In Week 4 you drew a border by holding down the equals key and counting. Never again. `*` between two numbers means multiply; `*` between a piece of text and a number means **repeat**. Want it forty wide? Change the twenty."

Then type the rest and run. Full real output:

```text
====================
  THE 7 TIMES TABLE
====================
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
====================
```

> **⚠️ Watch out:** count the rows on the screen with the student before you move on. **Ten rows, last one `7 x 10 = 70`.** If there are only nine and the last one reads `7 x 9 = 63`, the `for` line says `range(1, 10)` and it is the off-by-one arriving early. Do not fix it for them — ask "how many rows did you want, and how many are there?" That is the whole of this week's debugging habit, and it costs fifteen seconds here.

#### Pass 2 (6 min) — ⚠️ **DELIBERATE MISTAKE #1**, the missing colon

**Do this:** now you are going to add the times-table *grid*, and you are going to leave the colon off the `for` line. Type this, out loud, and **do not fix it**:

```python
for row in range(1, 10)
    print(row)
```

Run it. The real message:

```text
  File "/Users/you/ai-academy/level2/tables.py", line 1
    for row in range(1, 10)
                           ^
SyntaxError: expected ':'
```

**Say this:**

> "Good. Look at that. I've made a mistake and I want you to read it to me rather than me telling you. **Last line first.** What does the last line say?"

(SyntaxError: expected ':')

> "So what's Python's complaint, in your own words?"

(It wanted a colon.)

> "Where? Point at the screen."

(At the little arrow, at the end of the line.)

> "Right. That little `^` is Python pointing at exactly the character position where it wanted something. It isn't guessing and it isn't being vague — it got all the way to the end of that line, found no colon, and stopped. Watch what happens when I put one in."

Add the colon. Run. It works.

> "One character. And notice: **it didn't run at all.** No output, no partial results, nothing. A `SyntaxError` means Python couldn't even read the file, so it never started. That's actually the friendliest kind of mistake there is, because you find out immediately."

#### Pass 3 (7 min) — ⚠️ **DELIBERATE MISTAKE #2**, the total that stays at zero

**Do this:** now the accumulator, and this time your mistake will be **silent**. Type this exactly, with `total = 0` in the wrong place:

```python
total = 0
for n in range(1, 6):
    total = 0          # <-- this line is in the wrong place, on purpose
    total += n
print(total)
```

Run it:

```text
5
```

**Say this:**

> "Now. That should be fifteen. One plus two plus three plus four plus five. Say the answer out loud first — fifteen. And the program said five.
>
> **And there's no error message.** Nothing is red. Python is completely happy. This is exactly last week's silent bug, and it is going to keep happening to you all year, so let's practise the thing that finds it.
>
> Put your finger on the first line of the loop body. Now walk it: first pass — `n` is 1, and the first thing that happens is..."

(total gets set to 0.)

> "So what was in `total` from last time?"

(Gone. Wiped.)

> "Every pass. Twelve times, if there were twelve scores. So what does it end up holding?"

(Just the last one.)

> "Just the last one. Which is five. **The program is doing exactly what the file says.** Where does that line need to be?"

Let them tell you: above the `for`, at the margin. Move it. Run it. `15`.

> "And one more, which is the same mistake wearing a different hat. Watch."

Change the last line so the division happens inside:

```python
total = 0
for n in range(1, 6):
    total += n
    average = total / 5      # <-- divided INSIDE the loop
    print(f"average so far: {average:.2f}")
```

```text
average so far: 0.20
average so far: 0.60
average so far: 1.20
average so far: 2.00
average so far: 3.00
```

> "Five averages, and only the last one is the real one. It divided before it had finished adding. **Set up before, add inside, divide after.** That's the rule, and both of the mistakes I just made in front of you were breaking it."

**Ask this, before moving on:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Which of my two mistakes had an error message?" | The colon one. The `total = 0` one had none. | If they think both did, scroll back. Seeing the two side by side is the point. |
| "Which was worse?" | The silent one, because nothing told you. | Accept either if they can argue it. What matters is noticing they are different *kinds* of trouble. |
| "Say the three accumulator rules." | Set up before · add inside · use after. | Make them say all three. They will use these until June. |

---

### 🎲 Their Turn — The Grid and the Twelve Scores (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–7:** the 9 × 9 grid, with two loops.
- **Minutes 7–14:** the twelve-score accumulator, and the hand-check on paper.
- **Minutes 14–20:** the planted off-by-one, found by counting.

---

### 🔑 Wrap & Assign (9 minutes)

This segment closes the lesson: the Bug Log, the three checks, and the homework.

**Do this:** laptops shut. Notebook open at the Bug Log. Workbook on the table.

**Say this:**

> "Two minutes on the Bug Log before anything else, while today is still fresh. Two entries. One of them was the missing colon, which had a message. The other was the eleven-scores-out-of-twelve, which had **no message at all** — and that one is the entry that will still be useful to you in April. Write down what you saw, what it meant in your own words, and what you changed."

Give them the two minutes and do not fill the silence. Then the three checks from **✅ Assessing Understanding** below, word for word — they take five minutes between them and they are the only measurement this lesson needs.

Then the homework, using the script in **📤 Homework to Assign**. Two sentences of framing before you hand the workbook over:

> "Start with Predict the Output, laptop shut — write down what each short program prints, exactly, *before* you run it, and in Practice Set A write every value each `range` hands out *and* how many there are. Then the Build It section, the grid and the twelve scores, and the part I'm marking hardest is the hand-check: I want to see the division worked out on paper, not the answer.
>
> And one habit to take away, which costs two seconds and will save you an hour. **Every single time you write a `range`, say out loud how many values it hands out before you run it.** `range(1, 13)` — 'twelve values, one to twelve'. That's it. That's the whole habit."

**Ask this, as they pack up:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "One sentence: what does a loop actually save you?" | Mistakes, not time. One place to change instead of ten. | If they say "typing" — accept it, then ask what happens when the pattern changes. |
| "How many values does `range(1, 13)` hand out?" | Twelve. | The last thing they hear should be the subtraction. |
| "Which of today's two bugs had no error message?" | The eleven-prompt one. | If they are unsure, that is the entry to write first in the Bug Log. |

---

## 🎲 The Activity, In Full

This section gives the full instructions for the student's turn: the grid, the twelve scores, and the planted off-by-one.

### Setup

**On the table:** the laptop · the workbook's Build It section (landscape), Parts 1–4 · its Part 5 (the Bug Log) · **the twelve-score index card, face down** · a pencil · a blank sheet for the long division.

**On the screen:** `seven_times.py` from the live-code, saved and working. It is the thing they are about to extend.

### Part 1 — The grid, with a loop inside a loop (7 minutes)

**Say this:**

> "One table is ten rows. A whole grid is nine tables side by side — eighty-one numbers. You are going to print all eighty-one with **one** `print`. The trick is a loop inside a loop: the outer one picks the row, and for each row the inner one runs all the way across."

Have them create `tables.py` and type it. The complete, working file:

```python
# tables.py - a 9 x 9 times-table grid, printed with a loop inside a loop.

print("   ", end="")                      # 3 blank spaces to clear the row-label column
for col in range(1, 10):                   # 1..9 across the top
    print(f"{col:>4}", end="")             # :>4 means "right-aligned in 4 characters"
print()                                    # end the header line

print("   +" + "-" * 36)                   # 9 columns x 4 characters = 36 dashes

for row in range(1, 10):                   # OUTER loop: one pass per row
    print(f"{row:>2} |", end="")           # the row label, then a bar
    for col in range(1, 10):               # INNER loop: 9 passes for THIS row
        print(f"{row * col:>4}", end="")   # one product, right-aligned in 4
    print()                                # end this row's line
```

The real output:

```text
      1   2   3   4   5   6   7   8   9
   +------------------------------------
 1 |   1   2   3   4   5   6   7   8   9
 2 |   2   4   6   8  10  12  14  16  18
 3 |   3   6   9  12  15  18  21  24  27
 4 |   4   8  12  16  20  24  28  32  36
 5 |   5  10  15  20  25  30  35  40  45
 6 |   6  12  18  24  30  36  42  48  54
 7 |   7  14  21  28  35  42  49  56  63
 8 |   8  16  24  32  40  48  56  64  72
 9 |   9  18  27  36  45  54  63  72  81
```

**Three things to point at, in this order:**

1. **`end=""`.** "Normally `print` finishes by going to a new line. `end=""` says finish with nothing, so the next print carries on the same line. That's how nine numbers end up on one row."
2. **The bare `print()` at the bottom.** "That's what ends the row. Count its indentation: it lines up with the *inner* `for`, which means it belongs to the *outer* loop — it happens once per row, not once per number."
3. **`:>4`.** "Right-align this in four characters. It's the same family as `:.2f` from Week 3 — an instruction about how to show the value. It's what makes the columns stack."

> **💡 Try this:** have them move the bare `print()` one level deeper, so it lines up with the inner `print`. Run it. Eighty-one lines, one number each. Then move it back. **Indentation is not decoration; it is the program.**

### Part 2 — The twelve scores, and the hand-check (7 minutes)

**Say this:**

> "Now the accumulator, for real. Twelve scores. Total them, then average them. And I want the running total printed on every single pass, because I want you to *watch the box fill up*."

Have them create `scores.py`:

```python
# scores.py - total and average twelve scores with an accumulator.

HOW_MANY = 12                              # how many scores we are going to read

print("=" * 34)
print("  SCORE TOTALLER")
print("=" * 34)

total = 0                                  # the accumulator. Empty before the loop.

for i in range(1, HOW_MANY + 1):           # i takes 1, 2, 3 ... 12
    score = int(input(f"Score {i} of {HOW_MANY}: "))   # text in, whole number out
    total += score                         # add this score to the running total
    print(f"   running total after {i} scores: {total}")

average = total / HOW_MANY                 # one division, AFTER the loop

print("-" * 34)
print(f"  Scores added : {HOW_MANY}")
print(f"  Total        : {total}")
print(f"  Average      : {average:.2f}")
print("-" * 34)
```

**Now turn the index card over** and have them type the twelve numbers, ticking each one off the card with a pencil as it goes in. The real transcript, with the typed numbers shown where they appear on screen:

```text
==================================
  SCORE TOTALLER
==================================
Score 1 of 12: 88
   running total after 1 scores: 88
Score 2 of 12: 92
   running total after 2 scores: 180
Score 3 of 12: 70
   running total after 3 scores: 250
Score 4 of 12: 65
   running total after 4 scores: 315
Score 5 of 12: 100
   running total after 5 scores: 415
Score 6 of 12: 54
   running total after 6 scores: 469
Score 7 of 12: 78
   running total after 7 scores: 547
Score 8 of 12: 81
   running total after 8 scores: 628
Score 9 of 12: 47
   running total after 9 scores: 675
Score 10 of 12: 90
   running total after 10 scores: 765
Score 11 of 12: 62
   running total after 11 scores: 827
Score 12 of 12: 73
   running total after 12 scores: 900
----------------------------------
  Scores added : 12
  Total        : 900
  Average      : 75.00
----------------------------------
```

**Then close the laptop.** This next bit is the part that matters and it happens with a pencil.

**Say this:**

> "Laptop shut. The program says the average is seventy-five. **Prove it.** Nine hundred divided by twelve, on paper, showing your working. I want to see the division, not a number you remember."

The hand-check, written out the way a 12-year-old should write it:

```text
  900 ÷ 12

  12 × 70 = 840          so 70 is too small, but close
  900 − 840 = 60         sixty left over
  60 ÷ 12 = 5            five more
  70 + 5 = 75            ✔

  Check the other way:  12 × 75 = 12 × 70 + 12 × 5 = 840 + 60 = 900  ✔
```

> "Seventy-five. Same as the program. **Now — and this is the actual point — what have you just proved?** You've proved the program agrees with you on *this* data. That's not the same as proving the program is right. It's much better than nothing and it's much worse than a guarantee. Hold on to that thought, because in about ten minutes I'm going to show you a version of this program that gets it wrong, and the only reason you'll catch it is that you did this."

### Part 3 — The planted off-by-one (6 minutes)

**Do this:** while they are doing the long division, open `scores.py` and change **one thing**: `range(1, HOW_MANY + 1)` becomes `range(1, HOW_MANY)`. Save it. Say nothing about it.

```python
for i in range(1, HOW_MANY):               # <-- the bug lives here
```

**Say this:**

> "Laptop open. Run it again with the same twelve numbers off the card. Tick each one off as you type it, same as before."

They will type numbers off the card, and the program will finish while they still have `73` un-ticked. The real transcript:

```text
==================================
  SCORE TOTALLER
==================================
Score 1 of 12: 88
   running total after 1 scores: 88
Score 2 of 12: 92
   running total after 2 scores: 180
Score 3 of 12: 70
   running total after 3 scores: 250
Score 4 of 12: 65
   running total after 4 scores: 315
Score 5 of 12: 100
   running total after 5 scores: 415
Score 6 of 12: 54
   running total after 6 scores: 469
Score 7 of 12: 78
   running total after 7 scores: 547
Score 8 of 12: 81
   running total after 8 scores: 628
Score 9 of 12: 47
   running total after 9 scores: 675
Score 10 of 12: 90
   running total after 10 scores: 765
Score 11 of 12: 62
   running total after 11 scores: 827
----------------------------------
  Scores added : 12
  Total        : 827
  Average      : 68.92
----------------------------------
```

**Now say nothing.** Count to five. Let them look at the card in their hand with one number still on it.

Then, and only these questions:

> "Did it crash?"

(No.)

> "How many numbers are on the card?"

(Twelve.)

> "How many did it ask for? Count the lines on the screen."

(Eleven.)

> "So what's in your hand?"

(Seventy-three. It never asked for it.)

> "Right. And look at the report. It says **'Scores added: 12'**, which is a lie — but it's a lie *I* wrote, because that line just prints `HOW_MANY` and `HOW_MANY` is still twelve. The program isn't lying to you on purpose. It genuinely doesn't know how many scores it read. Nobody asked it to keep track."

Show Figure 7.4.

> "One character. `HOW_MANY + 1` became `HOW_MANY`. And here's the bit I want you to write in your Bug Log: **there was no error message, and the average was wrong by more than six marks.** If those had been real people's marks, the class average would have been reported six marks too low, and the only way anyone would ever find out is if somebody counted."

Then the fix, and the proof:

> "Fix it — put the `+ 1` back. Then run it once more and tell me the two things you're checking."

(Twelve prompts. And the average is 75 again.)

> **🧑‍🏫 If a student asks** *"why would anyone write `range(1, 12)` in the first place?"* — because it looks right. They wanted the labels to read 1 to 12, and 1 and 12 are the two numbers in the sentence "score 1 of 12". Writing `range(1, 13)` feels wrong the first fifty times. That is exactly why this bug is worth a Bug Log entry: **the wrong version is the one that reads better in English.**

### What "finished" looks like

- `tables.py` prints a 9 × 9 grid with columns that line up, and the student can point at which loop is the outer one.
- `scores.py` reads twelve scores, prints a running total on every pass, and reports `Total: 900` and `Average: 75.00`.
- The long division `900 ÷ 12 = 75` is on paper, with working shown, matching the program.
- The student has seen the eleven-prompt version, **found it by counting**, and can say in one sentence what was wrong.
- **Two Bug Log entries:** the `SyntaxError: expected ':'` and the silent off-by-one.
- Every line commented, saying *why*.

### Variation — easier

- **Drop the grid to 5 × 5.** `range(1, 6)` twice. The nesting lesson is identical and there is a third less typing.
- **Skip `:>4` entirely.** Print `f"{row} x {col} = {row * col}"`, one per line. Twenty-five lines instead of a grid. The loop-inside-a-loop still lands; only the alignment is lost, and alignment is not this week's objective.
- **Six scores instead of twelve.** Use the first six from the card: 88, 92, 70, 65, 100, 54. Total 469; 469 ÷ 6 = 78.1666…, so use `{average:.2f}` and the hand-check becomes 469 ÷ 6 = 78.17 (to two places). **If you want the clean division, use the first four instead: 88 + 92 + 70 + 65 = 315, and 315 ÷ 4 = 78.75 exactly.**
- **Give them `scores.py` already typed** and have them only run it, watch the running total, and do the hand-check. Reading a loop is a real skill and it is the one that matters most today.
- **Cut Part 3.** If the accumulator itself took the whole time, that is fine and normal. Move the planted bug into next week's warm-up; it works just as well there.

### Variation — harder

1. **Three accumulators at once.** A total, a *counter* of how many scores were 50 or more, and a *highest*. All three are the same shape: set up before, update inside, report after.

   ```python
   # scores_plus.py - three accumulators at once: a total, a counter and a highest.

   HOW_MANY = 12

   total = 0            # accumulator 1: the running sum
   fifties = 0          # accumulator 2: a counter - how many scores are 50 or more
   highest = -1         # accumulator 3: lower than any real score, so anything beats it

   for i in range(1, HOW_MANY + 1):
       score = int(input(f"Score {i} of {HOW_MANY}: "))
       total += score                     # add to the sum
       if score >= 50:                    # a counter only counts when a test passes
           fifties += 1
       if score > highest:                # a new champion?
           highest = score

   average = total / HOW_MANY

   print("-" * 34)
   print(f"  Total          : {total}")
   print(f"  Average        : {average:.2f}")
   print(f"  Highest        : {highest}")
   print(f"  50 or more     : {fifties} of {HOW_MANY}")
   print("-" * 34)
   ```

   Real output on the card's twelve scores:

   ```text
   ----------------------------------
     Total          : 900
     Average        : 75.00
     Highest        : 100
     50 or more     : 11 of 12
   ----------------------------------
   ```

   Check by hand: the only score below 50 is 47, so eleven of twelve ✔. **Ask why `highest` starts at −1** rather than 0. (Because a score of 0 is possible, and `0 > 0` is `False`, so a class where everyone scored zero would report a highest of… zero, which happens to be right by luck. Start below every possible value and the luck is not needed.)

2. **The fence-post problem, on purpose.** Print three items with a divider *between* them and no dangling one at the end. This is genuinely hard with only `for` and `if`, and the honest answer is "print the divider before every item except the first" — which needs a test on `i`. Let them find it.

3. **Count in the other direction.** Rewrite the times table so it prints from ten down to one, using a negative step. Then ask: *"how many values does `range(10, 0, -1)` hand out, and why isn't zero one of them?"*

4. **Sum 1 to 100 two ways.** The loop (5050) and the formula `n * (n + 1) // 2` (5050). Two methods, same number. Then the question worth asking: *"which one would you trust more if they disagreed?"*

5. **The nesting arithmetic.** Without running it, how many lines does a `range(1, 5)` loop containing a `range(1, 4)` loop print? (Twelve.) Then have them check. Then ask what happens if the inner loop's range depends on the outer counter — `for col in range(1, row + 1)` — and let them discover the triangle.

6. **The one-character audit.** Give them this and ask what each version prints, before running anything: `range(10)`, `range(1, 10)`, `range(1, 11)`, `range(0, 11)`, `range(10, 1)`, `range(10, 0, -1)`. Six answers, and two of them print nothing at all.

---

## 🐞 The Debugging Clinic

This section is for when a student's program breaks: what each message or silent symptom means, and how to teach finding it without giving the answer.

Every message below came from running a real broken version of this week's code. Only the folder path in the `File` line will differ on your machine.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `SyntaxError: expected ':'` with `^` at the end of the `for` line | "I read the whole line and there was no colon." | The colon is missing from the end of `for n in range(10)`. | Add the `:`. The `^` marks the exact spot where Python wanted it. |
| `IndentationError: expected an indented block after 'for' statement on line 1` | "You told me to repeat something and then didn't give me anything to repeat." | The line under the `for` is at the margin instead of indented. | Indent it four spaces. **Every `for` needs at least one indented line under it.** |
| `IndentationError: unindent does not match any outer indentation level` | "This line doesn't line up with anything I know about." | Mixed indent widths, usually from pasting — three spaces on one line, four on the next. | Delete the leading spaces on that line and retype them. Look at the left edge, not the words. |
| `NameError: name 'total' is not defined` pointing at `total += n` | "You asked me to add to a box that doesn't exist." | `total = 0` is missing, or it is *below* the loop instead of above it. | Put `total = 0` above the `for`, at the margin. **This is accumulator rule one.** |
| `TypeError: 'str' object cannot be interpreted as an integer` pointing at the `for` line | "`range` needs a number and you gave it text." | `range(count)` where `count` came from `input()` and was never converted. | `count = int(input(...))`. Convert at the door, as in Week 4. |
| `TypeError: can't multiply sequence by non-int of type 'str'` | "You asked me to repeat text a *text* number of times." | `"=" * "20"` — the 20 is in quotes. | `"=" * 20`. Take the quotes off the number. |
| `TypeError: can only concatenate str (not "int") to str` | "`+` glues text to text. That's a number." | `"=" + 20` instead of `"=" * 20`. | Use `*` to repeat text. `+` only joins text to text. |
| `TypeError: unsupported operand type(s) for +=: 'int' and 'str'` pointing at `total += score` | "You're adding a piece of text to a number." | `score = input(...)` with no `int()`. Input is **always** text. | `score = int(input(...))`. |
| `ZeroDivisionError: division by zero` pointing at the average line | Exactly what it says. | Dividing by a count that turned out to be zero — often a `range` that handed out no values at all. | Check the range first. `range(3, 3)` and `range(10, 1)` both produce zero passes. |
| **No error, and the loop prints nothing at all** | Python ran the loop zero times, which is not a mistake as far as it is concerned. | `range(3, 3)`, or `range(10, 1)` with no negative step. | Count the values: `stop - start`. If that is zero or negative, you get no passes. |
| **No error, and the total comes out as the last number only** | Python is perfectly happy. | `total = 0` is *inside* the loop, so it is wiped every pass. | Move it above the `for`. |
| **No error, and there is one output line too few** | Python is perfectly happy. | `range(1, 12)` where `range(1, 13)` was meant — the classic off-by-one. | Count the output lines against the number of items that went in. **Twelve in, eleven out.** |
| **No error, and every number is on its own line instead of in a grid** | Python is perfectly happy. | The bare `print()` that ends a row is indented into the *inner* loop. | Move it out one level, so it lines up with the inner `for`. |
| **No error, and a divider appears after the last item as well as between items** | Python is perfectly happy. | The fence-post problem: three items, three dividers, two gaps. | Print the divider before each item except the first, or accept the dangling one and say so. |

### How to teach debugging without giving the answer

The four habits from earlier weeks still stand: **hands off the keyboard · last line first · ask, do not tell · log it.** This week adds one more, and it is the one that finds off-by-one bugs.

**5. Count. Do not read — count.**

Reading a loop does not find an off-by-one, because there is nothing wrong with any individual line. `for i in range(1, 12):` is a good line of Python. What finds it is a **count**, and counting needs two numbers:

1. **How many things went in?** Twelve numbers on the card. Get them to say the number.
2. **How many lines came out?** Count them on the screen with a finger. Out loud.

If those two numbers differ, you have found the bug's *fingerprint* before you have found the bug — and that is the right order. Then, and only then, look at the `range`.

Three questions that do the work without giving anything away:

- *"How many prompts do you expect? Say the number before you press Enter."*
- *"Count them. Out loud. Point at each one."*
- *"Which is bigger — what went in, or what came out?"*

Then name this habit explicitly, because it will save them for the rest of the year: **every time you write a `range`, say out loud how many values it hands out, and check that against how many you wanted.** Two seconds, every time. `range(1, 13)` — "twelve values, one to twelve" — right.

---

## ❓ Questions Students Ask This Week

This section gives honest answers to the questions students are likely to ask, so you are not caught out.

**"Why does `range` start at zero? Nobody counts from zero."**

You will, in about five weeks, and then it will feel obvious. The honest answer today is about the *count*.

`range(a, b)` hands out exactly `b - a` values (when `b` is above `a` and there is no step), and `range(n)` hands out exactly `n`. That works because the stop is excluded and the start is included. If both ends were included, every count would be "the difference, plus one", and you would spend your life adding and subtracting ones.

There is a second reason that lands in Week 11: when you meet lists, the first slot is numbered 0, so `range(len(scores))` gives you exactly the right slot numbers with no arithmetic at all. Today, zero looks like a wart. In Week 12 it looks like a plan.

**"Can I call the counter something other than `i`?"**

Yes, and you usually should. `i` is short for "index" and it is a habit from mathematics, not a rule.

`for row in range(1, 10)` reads better than `for i in range(1, 10)`, and it makes the bug easier to see when there are two loops. Use `i` when the number has no meaning beyond "which pass is this"; use a real word the moment it means anything.

**"What if I want to go through 3, 7, 8, 100 — numbers that aren't a pattern?"**

You can't, with `range`. `range` only makes evenly spaced numbers. What you want is a **list**, and it arrives in Week 11 — you will write `for score in [3, 7, 8, 100]:` and it will do exactly what you expect. Everything you are doing this week with `range` and an accumulator will still work; it will just have better data going into it. **This is worth saying out loud rather than dodging**, because the student has spotted a real limitation and they are right.

**"How many times can a loop run?"**

As many as you like. `range(1000000)` is fine and takes about a second. The limit is your patience, not Python's. What you cannot do is have it run *forever* by accident — with a `for` loop, the number of passes is decided before the first one starts. **Next week's `while` loop can absolutely run forever**, and you will make it happen on purpose.

**"Is a loop faster than typing the lines out?"**

Not for the computer, no. Be precise about this, because the intuition is wrong. Ten `print` lines and a loop that prints ten lines take essentially the same time to *run*.

The loop is faster to **write**, faster to **change**, and **impossible to get wrong in ten different places.** That last one is the one that matters. When you changed 7 to 13, you edited one character. The by-hand version needs ten edits, and any one of them can be missed. **Loops save mistakes, not milliseconds.**

**"What happens if I change `n` inside the loop?"**

You can, and it will not do what you hope. Say you write `n = n + 5` inside the body. `n` will hold the bigger number for the rest of *that* pass. On the next pass Python refills it from `range` anyway and your change is gone.

So it looks like it works and then does nothing. **Do not do it.** The counter belongs to the `for` line, and the `for` line reclaims it every pass.

**"Which is better — `total = total + n` or `total += n`?"** *(Nobody fully agrees, and here is why.)*

They do exactly the same thing, so the question is entirely about people reading it, which is why there is no settled answer.

- **The case for `+=`:** it is shorter, and the variable's name appears once instead of twice, so you cannot write `total = totl + n` and spend ten minutes on it.
- **The case for the long form:** it says out loud what is happening, "the new total is the old total plus n", and a beginner reading `+=` often has no idea whether it means "add" or "set to".

There is a real argument in professional code too, and it goes beyond taste: with big data structures the two forms can behave *differently* in ways that are outside this course.

**Honest position: use `+=` because everyone else does and you will read it constantly, but never let anyone tell you the long form is wrong.** Write whichever one you can still understand at eleven o'clock at night.

**"Could Python warn me that my loop runs eleven times instead of twelve?"**

No, and this one is not a limitation that will be fixed. Python has no way to know that you wanted twelve. `range(1, 12)` is an ordinary, correct, useful thing to write, and thousands of programs mean exactly that. The number twelve exists only in your head and on your index card.

**This is the same shape as last week's ordering bug:** the file is a good program, it simply is not the program you meant, and no tool can tell the difference because the difference is your intention. That is why the count is your job.

---

## ⚠️ Where This Lesson Goes Wrong

This section lists the ways the lesson tends to go off course, and what to do right now when it does.

| What happens | Why | What to do right now |
|---|---|---|
| You point out the missing prompt in Part 3 | It is agonising to watch someone hold a card with a number on it and not see | Ask only the four scripted questions: *"Did it crash?" · "How many are on the card?" · "How many did it ask for?" · "So what's in your hand?"* Put your hands behind your back. |
| The student types the twelve scores without ticking them off | The tick is boring and they are keen | **Insist.** The tick is the entire mechanism by which they find the bug. Without it they will type eleven numbers and never know. Hand them the pencil before they start typing. |
| `range(1, 13)` is "fixed" to `range(1, 12)` because 12 looks right | English says "one to twelve", and `13` looks like a typo | Do not correct it — run it and count. Then say the sentence: **"the version that reads better in English is the one that's wrong."** |
| The indent is three spaces on one line and four on the next | Copy-paste, or a mixture of tabs and spaces | `IndentationError: unindent does not match any outer indentation level`. Delete the leading whitespace on the offending line and retype it. Then turn on "show whitespace" in the editor and leave it on for the rest of the year. |
| The grid comes out one number per line | The row-ending `print()` is indented into the inner loop | Ask: *"which loop should end the line — the one that does nine numbers, or the one that does nine rows?"* Then have them move it and watch it fix itself. |
| The accumulator is set to 0 inside the loop | It feels tidy to put all the loop's variables together | Silent bug, answer is the last number. Trace pass one out loud: *"first thing that happens on this pass is…?"* |
| The student prints the average inside the loop and it "looks right" | The last of the twelve printed averages *is* right | Ask how many averages they wanted. (One.) Then ask what the first eleven mean. (Nothing.) |
| The whole lesson turns into a typing exercise on the grid | The grid has fiddly punctuation — `end=""`, `:>4`, the bare `print()` | The grid is objective 1 only. **If it is eating the room, cut it to 5 × 5 or drop the alignment.** The accumulator and the off-by-one are objectives 3, 4 and 5 and they matter more. |
| The hand-check gets done on a calculator | It is right there and it is faster | Take the laptop and the phone away for those three minutes. The point is not the answer 75; it is the student having an independent source of truth to hold the program to. |
| They conclude that loops are only for printing | Every example so far has printed something | The accumulator is the antidote — it produces a *number*, not output. Say it: "the loop printed nothing useful; the answer was in the box at the end." |
| `while` gets asked about, or googled, and arrives early | It is the obvious next question | Answer honestly in one sentence — "that's a loop that stops when a condition goes false, and it's next week" — and do not demonstrate it. Two loop shapes in one lesson halves what lands. |

---

## 🧭 Differentiation

This section covers what to cut, reteach or add when the student is struggling, flying or not engaging.

### If the student is struggling

**Cut, in this order:** the `:>4` alignment · the grid down to 5 × 5 · the grid entirely · twelve scores down to four · Part 3.

**What you must not cut:** the Hook (the typing race), and one accumulator with the running total printed on every pass. Between them those two deliver objectives 1 and 3, and neither needs the grid.

**Reteach the counter physically — the refilled cup.** Four minutes, works on nearly everybody.

Put an empty cup on the table and five cards face down beside it, with 1, 2, 3, 4, 5 written on them.

> "This cup is `n`. These cards are what `range` is going to hand out."

Now play the loop. You are Python. Take card 1, put it *in* the cup. "Pass one. What's in `n`?" They read it. They do the body out loud — "seven ones are seven". Then **take the card out and put it face down on the discard pile** before putting card 2 in.

> "Notice what I just did. I took the old one *out*. There is only ever one thing in the cup. That's why you can't get at pass one's number during pass two — it's gone."

When the cards run out, the loop stops. Point at that: **nobody told it to stop; it ran out.**

**Then reteach the accumulator with the same cup and a second one.** Cup A is `n`, cup B is `total`. Coins go into cup B and *stay there*. Do all five passes, counting the coins in B out loud after each one: 1, 3, 6, 10, 15. Two cups, two completely different jobs — one gets emptied every pass, one never does. **That distinction is the whole of today.**

**The copy-this-exactly scaffold.** Four scores instead of twelve, and the numbers chosen so the division is clean:

```python
# scores.py - type this exactly, then run it with 88, 92, 70 and 65.

HOW_MANY = 4                     # four scores this time

total = 0                        # the box. Made BEFORE the loop.

for i in range(1, HOW_MANY + 1):                  # 1, 2, 3, 4
    score = int(input(f"Score {i} of {HOW_MANY}: "))
    total += score                                # add it to the box
    print(f"   running total: {total}")           # watch the box fill up

average = total / HOW_MANY                        # divide AFTER the loop
print(f"Total   : {total}")
print(f"Average : {average:.2f}")
```

Real run with 88, 92, 70, 65:

```text
Score 1 of 4: 88
   running total: 88
Score 2 of 4: 92
   running total: 180
Score 3 of 4: 70
   running total: 250
Score 4 of 4: 65
   running total: 315
Total   : 315
Average : 78.75
```

Hand-check: 88 + 92 + 70 + 65 = 315. And 315 ÷ 4 = 78.75, because 4 × 78 = 312 with 3 left over, and 3 ÷ 4 = 0.75 ✔

**Reduce the writing.** A Bug Log entry of `no error — asked 11 times not 12 — range stops early` is full credit.

### If the student is flying

None of these need syntax they have not met.

1. **Three accumulators at once** (Variation — harder, item 1). Total, counter, highest. Then the good question: why does `highest` start at −1?
2. **Sum 1 to 100 two ways** (item 4), and which one they would trust if the two disagreed.
3. **The one-character audit** (item 6). Six ranges, two of which print nothing. Predict all six before running any.
4. **The triangle.** `for col in range(1, row + 1)` inside `for row in range(1, 10)`. It prints a triangle instead of a square, and working out *why* the inner loop's length changes is a genuinely good five minutes.
5. **The fence-post problem** (item 2). Hard, honest, and it has no tidy solution with only this week's tools — which is itself worth knowing.
6. **The counting question with a real edge.** Ask: *"your program reports 'Scores added: 12' because you typed 12 into `HOW_MANY`. How would you make it report the number it actually read?"* The answer is a second accumulator — a counter that goes up by one every pass — and it is the fix that would have made the planted bug *announce itself*. **That is a genuinely professional idea: make the program count what it did rather than what it was told to do.** Let them build it:

   ```python
   HOW_MANY = 12
   total = 0
   scores_read = 0                                   # count what actually happened

   for i in range(1, HOW_MANY):                      # the bug, left in on purpose
       score = int(input(f"Score {i} of {HOW_MANY}: "))
       total += score
       scores_read += 1                              # one more, really read

   print(f"asked for : {HOW_MANY}")
   print(f"read      : {scores_read}")
   print(f"average   : {total / scores_read:.2f}")
   ```

   With the twelve card scores typed in, the real output ends:

   ```text
   asked for : 12
   read      : 11
   average   : 75.18
   ```

   Two numbers that disagree, printed side by side, and an average that is now *right for the eleven scores it actually saw* (827 ÷ 11 = 75.18). **The bug is still there and the program is now telling you about it.** That is worth more than fixing it.

### If the student won't engage today

Do the Hook and then play **Human Loop**, which needs no computer.

You are the program and they are the counter. They hold a card that says `n`. You call out "pass one" and they write 1 on the card; you both say the body out loud; you rub it out and they write 2. Do the seven times table this way, out loud, alternating. It is silly and it is exactly the right mental model.

Then swap: **they** are the program and you are the counter, and **you make mistakes on purpose** — you write 0 first, or you keep 3 on the card for two passes, or you stop at 9 — and they have to catch you. A student who can catch a fake off-by-one in your hands can catch a real one in their own code.

Finish with one question, which is the whole week without a laptop:

> *"I want you to write out the eleven times table by hand, up to eleven times ten. Then tell me the smallest change that would turn it into the twelve times table."*

Every line changes. Then show them the loop again, where one character changes. **That contrast is objective 1**, and it arrived with a pencil.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — how many passes (spoken)**

> "How many times does the indented line run in `for n in range(4, 9):`? And what is the last value `n` takes?"

*Good answer:* five times (9 − 4), and the last value is 8. **What to catch:** "six times, last value 9." That is the off-by-one and it means the fence-post picture has not landed. Go back to Figure 7.1 and count the boxes with a finger.

**Check 2 — the three accumulator rules (spoken)**

> "I want to total up twenty numbers. Tell me exactly where the `total = 0` goes, where the adding goes, and where the dividing goes."

*Good answer:* `total = 0` before the loop at the margin; the adding inside the loop in the indent; the dividing after the loop at the margin. **What to catch:** any answer that puts the divide inside. Ask: "how many averages do you want?" (One.) "So how many times should that line run?" (Once.)

**Check 3 — finding an off-by-one (spoken)**

> "You gave your program fifteen numbers off a card and the screen shows fourteen prompts. Nothing crashed. What do you do first, and what are you looking for?"

*Good answer:* count the two numbers and notice they differ; then look at the `range` and check whether the stop value is one too small. The point is that they **count before they read.** **What to catch:** "I'd read through the program looking for the mistake." Reading does not find this one, because every line is a correct line. Say so, and then ask them to count instead.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Writes `i = 0` above the loop, or tries to set the counter inside it. Cannot say how many times a loop will run without running it. Puts `total = 0` inside the loop. |
| **2 — Emerging** | Copies a working loop and changes the numbers. Gets `range(1, 11)` right when reminded that it stops early. Builds an accumulator with the three rules written down in front of them. |
| **3 — Secure** | Writes a `for` loop over `range` unaided and **predicts the number of passes before running it.** Explains that `range(4)` gives four values ending at 3, and why. Builds a working accumulator, divides after the loop, and hand-checks the average on paper. **This is the target.** |
| **4 — Strong** | Finds an off-by-one by counting output lines against inputs, without being told to count. Explains why the accumulator must be created before the loop, using the "wiped every pass" argument. Uses a step and a negative step correctly. Can say which loop in a nested pair ends the line. |
| **5 — Exceptional** | Adds a counter so the program reports what it actually read rather than what it was told. Explains why Python cannot detect an off-by-one for you. Predicts that `range(3, 3)` prints nothing, and says why. Sees that the version reading better in English (`range(1, 12)`) is the wrong one, and can say why that makes the bug likely. |

---

## 📤 Homework to Assign

This section is the script for handing over the workbook, with its timings.

**Say this:**

> "About an hour, and the first thing is with the laptop shut.
>
> **Warm-Up — five questions about last week.** Short answers, from memory. Question 4 is a chain with the wrong order, and it has no error message. You will meet that shape again today.
>
> **Predict the Output — four short programs, laptop closed.** Write your prediction *before* you run anything. Two of the four have no error at all, so 'what do you expect' means 'what will it print, exactly, including the spaces'. Then run them, and write your score out of eight at the bottom.
>
> **Practice Set A — Read It, and Practice Set B — Write It.** Set A is six questions: ranges, a trace table, matching code to output, three broken programs, a diagram to label, and four sentences in your own words. Set B is five programs, from a one-line row of dashes up to the pocket-money week. Same rule as always: **write what you expect to happen before you run it.**
>
> **Fix the Broken Program.** `steps.py` has three bugs, one in each family — it never starts, it starts then stops, and it finishes and lies. Fix them in that order. The third one has no error message, so you will have to count. Then hand-check the new average on paper and **show the division, not the answer.**
>
> **Puzzle of the Week — The Range Detective.** Eight ranges, seven targets to write, a nesting table, and one request that cannot be done. The last one is a trick that is not a trick.
>
> **Think Deeper — two questions.** The second asks whether a computer could have caught today's bug for you, and the answer is more interesting than yes or no.
>
> **Build It — the big one, in five parts.** The stepped grid: the even times tables 2, 4, 6, 8 and 10, times 1 to 12, using a `range` with a **step** for the rows, with the columns lined up. Then the twelve scores off your card, with the running total on every pass. Then the hand-check — I want to see 12 × 70, and the sixty left over, and where the five comes from. Then break it on purpose, and then the **Bug Log**: two entries, at least one with no error message.
>
> **Draw It** and the **Self-Check** last. Every line of code commented, saying *why*."

**Workbook sections:** Warm-Up and Predict the Output can be started in class if there is time; **Practice Set A, Practice Set B, Fix the Broken Program, Puzzle of the Week, Think Deeper, Build It (Parts 1–5), Draw It and the Self-Check** at home. The Build It grid prints best in landscape.

**Expected time:** 10 min Warm-Up and Predict · 15 min Practice Set A · 15 min Practice Set B · 10 min Fix the Broken Program · 10 min Puzzle · 20 min Build It (grid and accumulator) · 5 min hand-check · 10 min Bug Log, Think Deeper, Draw It and Self-Check. This is a full workbook; if the hour runs out, protect **Predict the Output, Fix the Broken Program and Build It Parts 1–5** and let the Puzzle slip to next week's warm-up. About 60–90 minutes in all.

---

## 🔑 Answer Key

The key follows the workbook's own order and item labels (W1–W5, P1–P4, A1–A6, B1–B5, Bug 1–3, Puzzle P1–P6, T1–T2, Build It Parts 1–5, Draw It, Self-Check). Printed numbers and outputs match the workbook's Answers section.

### Warm-Up — last week's review

**W1.** `elif` is short for "else, if". It adds another condition to a chain and goes **between** the `if` and the `else`. You can have as many as you like; nothing comes after the `else`.

**W2.** That branch runs and **the whole rest of the chain is skipped.** The **first** match wins, not the best match.

**W3.** `and` is `True` in **one** row out of four. `or` is `True` in **three** rows out of four. `not True` is **`False`**.

**W4.** It prints **`C`**. `95 >= 60` is `True`, so the C branch runs and the `>= 90` test is never looked at. The answer is confidently wrong with **no error message**. Fix: put the highest threshold first.

**W5.** A **silent bug** is a mistake that gives a wrong answer with no error message. Accept any honest example (a 95 graded `C`; a mark of exactly 90 getting a B because `>` was written for `>=`; an `or` that hands back text). **Marking tip:** if the Bug Log entry they name is from Week 6, that is the right habit, so give the mark.

### Predict the Output

**P1.** Two lines: `0 1 2 ` then `1 2 `. `range(3)` hands out **three** values; `range(1, 3)` hands out 3 − 1 = **two**. Trailing space on each line, because `end=" "` follows every number, including the last. *Wrong-answer map:* `1 2 3` for the first means they think `range` starts at 1; `1 2 3` for the second means they included the stop.

**P2.** `6` then `3`. The first is the accumulator, 1 + 2 + 3. The second is the surprising one: **after the loop, `n` still holds the last value handed out**, 3. The box was never emptied; the loop simply stopped refilling it. *Wrong-answer map:* a `NameError` guess means they think the loop variable dies with the loop; `4` means they included the stop.

**P3.** **One line:** `1 2 3 2 4 6 `. The bare `print()` is at the margin, so it belongs to neither loop and runs once, after everything. If it were indented to line up with the inner `for`, it would run once per outer pass, giving two lines: `1 2 3 ` and `2 4 6 `. *Wrong-answer map:* two lines means they read the bare `print()` as inside the outer loop; six lines means they put it inside the inner loop too.

**P4.** `4`. The line says `total = n`, not `total += n`, so each pass **replaces** the total and the box ends up holding the last value. One missing character, the `+`, and no error. The correct line gives 1 + 2 + 3 + 4 = 10. *Wrong-answer map:* `10` means they read what the line was meant to say, not what it says. Tell them that is the most common mistake in programming.

**Score out of eight:** the workbook asks the student to count their own correct answers out of 8. Accept their count if it agrees with the answers above; the useful question is which one surprised them (usually P2's `n`, or P3's indentation).

### Practice Set A — Read It

**A1.**

| `range(...)` | Values | How many | Last one | Working |
|---|---|---|---|---|
| `range(10)` | 0 1 2 … 9 | 10 | 9 | 10 − 0 |
| `range(1, 5)` | 1 2 3 4 | 4 | 4 | 5 − 1 |
| `range(3, 20)` | 3 4 5 … 19 | 17 | 19 | 20 − 3 |
| `range(1, 13)` | 1 2 3 … 12 | 12 | 12 | 13 − 1 |
| `range(0, 101, 10)` | 0 10 20 … 100 | **11** | 100 | ten steps of 10, **plus the starting 0** |
| `range(5, 5)` | nothing | 0 | — | 5 − 5 |
| `range(10, 1)` | nothing | 0 | — | 1 − 10 is negative |

The two that hand out nothing are `range(5, 5)` and `range(10, 1)`: `stop - start` is zero or negative, and a positive step has nowhere to go. A loop with zero passes runs its body zero times, which is not an error, just silence. The `range(0, 101, 10)` row is the trap: eleven numbers, not ten. With a step, count the numbers rather than trusting the subtraction.

**A2.** `range(2, 11, 2)` hands out 2, 4, 6, 8, 10.

| Pass | `n` is | `total` before | `total` after |
|---|---|---|---|
| 1 | 2 | 0 | 2 |
| 2 | 4 | 2 | 6 |
| 3 | 6 | 6 | 12 |
| 4 | 8 | 12 | 20 |
| 5 | 10 | 20 | 30 |

The program prints `2`, `6`, `12`, `20`, `30`, one per line. Hand-check: 2 + 4 + 6 + 8 + 10 = 30. **Boxes called `total`: one.** It changes five times. *Wrong-answer map:* "five" is Misconception 3 again; use the cup and coins.

**A3.** a → **2** · b → **1** · c → **4** · d → **3**. The four outputs are `0 1 2 `, `1 2 `, `3 2 1 `, `0 2 `. `range(0, 4, 2)` gives 0 and 2 (the next would be 4, the stop): **two values, not three.**

**A4.**

- **(i) No error message.** Prints `5`. `total = 0` is *inside* the loop, so every pass wipes the total. Fix: move it above the `for`, at the margin. Breaks accumulator **rule 1**.
- **(ii) An error message:** `NameError: name 'total' is not defined`, reported on the `total += n` line. `+=` means "add to what is already there" and the box was never made. Fix: `total = 0` above the loop.
- **(iii) No error message.** Prints five averages: `0.2`, `0.6`, `1.2`, `2.0`, `3.0`. Only the last means anything; the others divided before the adding had finished. Fix: move the division and print below the loop, at the margin. Breaks accumulator **rule 3**.

Two of the three have no error message. Make them say it: that is what loop bugs are like.

**A5.** Values: **1, 2, 3, 4, 5**. Hub on pass 3: **3**; it is **pass 3 of 5**. Running totals after passes 1, 2, 3: **1 · 3 · 6**. Average at the end: **15 ÷ 5 = 3.0**. Rule boxes: **rule 1, `total = 0` above the `for`, at the margin · rule 2, the adding inside the loop, in the indent · rule 3, the dividing after the loop, at the margin.** *Marking tip:* `range(1, 6)` handing out six values, or a hub showing `0`, is the fence-post slip again.

**A6.**

- **(a)** Python does, through the `for` line, one value per pass from whatever `range` hands out. You never assign to it yourself.
- **(b)** So the count is a plain subtraction. `range(a, b)` hands out exactly `b - a` values (when `b` is above `a`, no step), with no plus-one to remember. Include the stop and every count in every program would be "the difference plus one", and *that* would be what everybody got wrong instead. **The argument, not the rule, is what earns the mark;** "because it does" gets half.
- **(c)** **Twelve.** The inner loop runs all the way through (3 passes) for each of the outer loop's 4 passes: 4 × 3 = 12.
- **(d)** Every individual line is correct Python. `for i in range(1, 12):` is a perfectly ordinary line and thousands of programs mean exactly that. **Counting** finds it: how many went in, how many lines came out. If they differ you have the bug's fingerprint before you have the bug.

### Practice Set B — Write It

**B1.** `print("-" * 20)` prints `--------------------` (twenty dashes, typed once). *Marking tip:* twenty typed dashes is not a wrong answer for the output but misses "Done looks like"; send it back.

**B2.**

```python
for n in range(1, 13):             # 1, 2, 3 ... 12  (13 - 1 = twelve values)
    print(f"12 x {n} = {12 * n}")  # one row per pass
```

Twelve rows, from `12 x 1 = 12` to `12 x 12 = 144`. `range(1, 12)` gives eleven and loses the `12 x 12` row, the off-by-one arriving exactly where it was warned.

**B3.**

```python
total = 0                          # the accumulator, BEFORE the loop
for n in range(1, 21):             # 1, 2, 3 ... 20  (21 - 1 = twenty values)
    total += n                     # add this n, INSIDE the loop
print(f"1 to 20 adds up to {total}")   # use it AFTER the loop, at the margin
```

Prints `1 to 20 adds up to 210`. Hand-check: 20 × 21 ÷ 2 = 210. Two different methods, same answer.

**B4.**

```python
for n in range(5, 51, 5):          # 5, 10, 15 ... 50  (stops before 51)
    print(n, end=" ")              # end=" " keeps it on one line
print()                            # a bare print() ends the line
```

Prints `5 10 15 20 25 30 35 40 45 50 ` (ten numbers). Why 51: `range` stops before its stop, so `range(5, 50, 5)` would quietly lose the 50. *Wrong-answer map:* last number 45 means stop value one step too small.

**B5.** `pocket.py`, a correct version:

```python
# pocket.py - five days of pocket money spent, totalled and averaged.

DAYS = 5                                        # five school days

print("=" * 28)
print("  POCKET MONEY WEEK")
print("=" * 28)

spent = 0                                       # the accumulator, BEFORE the loop

for day in range(1, DAYS + 1):                  # 1, 2, 3, 4, 5
    amount = int(input(f"Day {day} of {DAYS}: rupees spent? "))
    spent += amount                             # add today to the running total
    print(f"   running total: {spent} rupees")

average = spent / DAYS                          # divide AFTER the loop

print("-" * 28)
print(f"  Total   : {spent} rupees")
print(f"  Average : {average:.2f} rupees a day")
print("-" * 28)
```

With 40, 25, 60, 15, 30 the running totals are 40, 65, 125, 140, 170 and the report is `Total   : 170 rupees` and `Average : 34.00 rupees a day`, matching the workbook's expected output. Hand-check: 5 × 34 = 170. Mark these: five prompts, a running total on every pass, **one** average after the loop, and the paper check of 170 ÷ 5 = 34. Why `DAYS + 1`: five passes labelled 1 to 5 needs `range(1, 6)`.

### Fix the Broken Program

**Bug 1 (family 1, it never started).** Nothing ran. The colon is missing from the end of the `for` line and the `^` points at where Python wanted it. The fix line is `for day in range(1, DAYS):` for the moment; bug 3 changes it again.

**Bug 2 (family 2, it started then stopped).** The error is reported on line 11, `total += steps`, **but the mistake is not on line 11**: nothing above it made the box. The missing line is `total = 0`, above the `for`, at the margin. It broke accumulator **rule 1**. The answer to "is that where the mistake is?" is **No.**

**Bug 3 (family 3, it finished and lied).**

- **(a)** **Seven** days on the list; **six** prompts appeared.
- **(b)** **11500**, the last one, never asked for.
- **(c)** `range(1, DAYS)` is an ordinary, correct line. It hands out 1 to 6, which is what it should. The number seven exists only in the programmer's head, so Python has nothing to complain about.
- **(d)** `for day in range(1, DAYS + 1):`
- **(e)** Total **63000**, average **9000.00**. Real running totals: 8200, 17300, 24700, 35200, 42000, 51500, 63000. (With the bug, the report shows 51500 and 7357.14, as the workbook prints.)
- **(f)** Hand-check: 63000 ÷ 7, and 7 × 9000 = 63000 exactly, so 9000. Also accept adding the seven days in order to reach 63000. **Full credit needs the working.**
- **(g)** **Counting the prompts against the list** is the only test that catches it: six prompts for seven numbers. The total and the average are plausible and nothing crashes. A test that only checks "did it produce a number" misses it completely.

### Puzzle of the Week — The Range Detective

**P1.**

| `range(...)` | Values | Count |
|---|---|---|
| `range(1, 6)` | 1 2 3 4 5 | 5 |
| `range(0, 10, 2)` | 0 2 4 6 8 | 5 |
| `range(10, 0, -2)` | 10 8 6 4 2 | 5 |
| `range(5, 51, 5)` | 5 10 15 20 25 30 35 40 45 50 | 10 |
| `range(7, 8)` | 7 | 1 |
| `range(4, 4)` | nothing | 0 |
| `range(9, 2)` | nothing | 0 |
| `range(2, 3, 5)` | 2 | 1 |

**P2.** `range(4, 4)` and `range(9, 2)`. In common: `stop - start` is zero or negative with a positive step, so no passes and no error.

**P3.** `range(2, 3, 5)` hands out just `2`. After 2 the next would be 7, past the stop of 3. The step sets the size of the jumps, not whether the first value appears: the start is always handed out if it is below the stop.

**P4.**

| I want | The range |
|---|---|
| 1 … 10 | `range(1, 11)` |
| 0 … 99 | `range(100)` or `range(0, 100)` |
| 12, 14, 16, 18, 20 | `range(12, 21, 2)` |
| 100, 90, 80 … 10 | `range(100, 0, -10)` |
| the twelve numbers 1 to 12 | `range(1, 13)` |
| exactly one value: 50 | `range(50, 51)` |
| nothing, using two 6s | `range(6, 6)` |

Every stop is one past the last value wanted.

**P5.** 12 (4 × 3) · 81 (9 × 9, the times-table grid) · 60 (5 × 12, the homework grid) · 0 (0 × 99). The last row: the outer loop runs zero passes, so the inner loop never starts, and zero times ninety-nine is zero.

**P6.** **It cannot be done.** `range` makes evenly spaced numbers (a start, a stop, one fixed step), and the gaps between 3, 7, 8 and 100 are 4, 1 and 92. This is a real limitation, not a trick: it is what a **list** is for, arriving in Week 11 (`for score in [3, 7, 8, 100]:`). Give full credit for "it can't, because the gaps are not equal"; a student who writes a clever expression that is not a single `range` has not answered the question.

### Think Deeper

**T1.** A full-credit answer names something other than speed, at least two things, and one moment from this week. Model answer:

> Ten `print` lines and a loop that prints ten lines take about the same time to run, so speed is not the point. What the loop gives me is **one place to change things.** When I turned the seven times table into the thirteen times table I edited one character; by hand I would have had to edit ten lines, and if I had missed one the program would have printed a wrong row and not complained.
>
> The other thing it gives me is a program whose length does not depend on how much work it does. My loop is three lines whether it prints ten rows or ten thousand. That means I can *think* about ten thousand rows, which I could not do if I had to type them.
>
> So loops save mistakes, not milliseconds, and they let me write down a pattern instead of a list.

**T2.** Model answer.

- *Whose fault:* the programmer's, not Python's. That line prints `HOW_MANY`, a number *I* typed, so it reports what I intended, not what happened.
- *How to stop it:* a second accumulator, a counter that goes up by one every pass, and a report that prints the counter. With the bug left in and the twelve card scores typed, the counter version ends with `asked for : 12`, `read      : 11`, `average   : 75.18` (827 ÷ 11 = 75.18), two numbers that disagree, side by side.

**The principle: make the program report what it actually did, not what it was told to do.**

*Could a computer have caught it?* Accept either side if it names its cost.

- The strong "no" answer: `range(1, 12)` is a completely ordinary line that thousands of programs mean, and the number twelve existed only in my head and on the card. For Python to warn me it would need my intention, and my intention is not in the file. It is the same shape as last week's ordering bug.
- What *can* be automated is the check I did by hand (compare "how many I read" with "how many were in the file"), **but somebody has to decide to write that check, and that somebody is me.**
- A strong "yes" answer must say how the computer learns the intended count, and that is a check somebody wrote.

### Build It

**Part 1 — the stepped grid.** First the question: `range(2, 11, 2)` gives **5** rows (2, 4, 6, 8, 10); `range(2, 10, 2)` gives **4** (2, 4, 6, 8) and loses the ten times table. They want the first, because `range` stops before its stop number.

```python
# grid_step.py - the even times tables, 2 to 10, times 1 to 12.
# The outer loop uses range with a STEP of 2, so it visits 2, 4, 6, 8, 10.

print("     ", end="")                       # 5 spaces to clear the row label
for col in range(1, 13):                     # 1..12 across the top
    print(f"{col:>4}", end="")
print()

print("    +" + "-" * 48)                    # 12 columns x 4 characters = 48

for row in range(2, 11, 2):                  # OUTER: 2, 4, 6, 8, 10 (step 2)
    print(f"{row:>3} |", end="")             # the row label
    for col in range(1, 13):                 # INNER: 12 passes per row
        print(f"{row * col:>4}", end="")
    print()
```

The real output:

```text
        1   2   3   4   5   6   7   8   9  10  11  12
    +------------------------------------------------
  2 |   2   4   6   8  10  12  14  16  18  20  22  24
  4 |   4   8  12  16  20  24  28  32  36  40  44  48
  6 |   6  12  18  24  30  36  42  48  54  60  66  72
  8 |   8  16  24  32  40  48  56  64  72  80  88  96
 10 |  10  20  30  40  50  60  70  80  90 100 110 120
```

**Marking notes.** Five rows, not six — `range(2, 11, 2)` gives 2, 4, 6, 8, 10 and stops before 11. Sixty numbers printed by one `print`. If a student wrote `range(2, 10, 2)` they get four rows and lose the ten times table; that is the off-by-one again, and it is worth pointing at rather than correcting silently.

The workbook's "Fill in what you actually got" table:

| Check | Wanted | Got |
|---|---|---|
| Number of table rows | 5 | **5** |
| First row's label | 2 | **2** |
| Last row's label | 10 | **10** |
| Rightmost number on the last row | 120 | **120** |
| Total numbers printed | 60 | **60** (5 × 12) |
| Number of `print` statements doing the numbers | 1 | **1** |

**Part 2 — the twelve scores.** The complete file is in the Activity section above (`scores.py`). The real report with the card's twelve scores:

```text
----------------------------------
  Scores added : 12
  Total        : 900
  Average      : 75.00
----------------------------------
```

The running-total column the student should have on the page:

| Pass | Score in | Running total |
|---|---|---|
| 1 | 88 | 88 |
| 2 | 92 | 180 |
| 3 | 70 | 250 |
| 4 | 65 | 315 |
| 5 | 100 | 415 |
| 6 | 54 | 469 |
| 7 | 78 | 547 |
| 8 | 81 | 628 |
| 9 | 47 | 675 |
| 10 | 90 | 765 |
| 11 | 62 | 827 |
| 12 | 73 | **900** |

Total **900**, average **75.00**.

**Part 3 — the hand-check.** Full credit requires the working, not the answer:

```text
  900 ÷ 12

  12 × 70 = 840          70 is close but too small
  900 − 840 = 60         sixty left over
  60 ÷ 12 = 5            five more
  70 + 5 = 75            ✔

  Check backwards:  12 × 75 = 840 + 60 = 900  ✔
```

The program says `75.00`. They agree.

**(a)** It proves the program is right **on these twelve numbers**. That is real and worth having.
**(b)** It does **not** prove the program is right in general. The eleven-prompt version would also agree with a hand-check of *eleven* numbers. The hand-check gives an **independent source of truth**, the only reason you can ever catch a program that is confidently wrong.

**Part 4 — break it on purpose.**

| | Before | After |
|---|---|---|
| Prompts that appeared | **12** | **11** |
| Numbers left un-ticked on the card | **0** | **1 (73)** |
| Total reported | **900** | **827** |
| Average reported | **75.00** | **68.92** |
| `Scores added` line said | **12** | **12** |
| Error message | **none** | **none** |

827 ÷ 12 = 68.9166…, shown as `68.92` by `:.2f`.

**(c)** That line prints `HOW_MANY`, which is still 12 because nobody changed it. The program does not know how many scores it read; it reports a number *you* typed, not something it measured. It is not lying on purpose; it has never been asked to count.
**(d)** `Total : 827` is honest, since it really is the sum of the eleven scores seen. `Scores added : 12` is not: it is a plan printed as if it were a measurement. The average is dishonest by consequence (an honest total divided by a dishonest count).

**Marking notes.** Five grid rows, not six. If a student wrote `range(2, 10, 2)` they get four rows and lose the ten times table; that is the off-by-one again, and it is worth pointing at rather than correcting silently.

**Part 5 — the Bug Log.** Two entries, at least one with no error message:

| # | What I saw (real text) | What it meant, in my words | What I changed |
|---|---|---|---|
| 1 | `SyntaxError: expected ':'` with the `^` at the end of `for n in range(1, 11)` | Python read the whole line, got to the end, and there was no colon. It never ran the file at all — no output, nothing. | Added the `:` |
| 2 | **No error message.** It asked for eleven scores when I had twelve on the card, and the average came out as 68.92 instead of 75. | `range(1, 12)` hands out 1 to 11, because range stops *before* the number you give it. The version that reads correctly in English is the wrong one. I only found it because I was ticking numbers off the card and had one left. | `range(1, 13)` |

Also acceptable, and arguably better:

| # | What I saw | What it meant | What I changed |
|---|---|---|---|
| 3 | **No error message.** My total came out as 73, the last score, instead of 900. | I had `total = 0` inside the loop, so every pass wiped the running total before adding to it. There is only one box called `total`, and I was emptying it twelve times. | Moved `total = 0` above the `for` |
| 4 | `NameError: name 'total' is not defined` on the line `total += score` | `+=` means "add to what is already in there", and there was nothing in there because I never made the box. | Added `total = 0` before the loop |

**(e)** Probably one or both. Name the pattern: **loop bugs are usually silent**, because a loop that runs the wrong number of times is still a perfectly legal loop.
**(f)** **Counting.** Two numbers: how many things went in, and how many lines came out. If they differ, you have the bug's fingerprint before you have the bug, and *then* you look at the `range`.
**(g)** It turned "how many did it ask for?" into a physical fact. Without the ticks the eleventh prompt looks exactly like the twelfth, and you would have typed eleven numbers and stopped without noticing. **The tick is the count.**

### Draw It

There is no single right drawing. A strong answer has **exactly one box labelled `total`** in each snapshot, redrawn as it changes, and a hub holding **one** value at a time. The workbook's sample uses five days of screen time (45, 60, 30, 90, 25): totals 0, 45, 105, 135, 225, 250, then 250 ÷ 5 = 50. If the picture shows five `total` boxes side by side, or a counter holding two numbers at once, the mental model has slipped; redrawing it as one box changing is the whole exercise. Also check that **an arrow leaves the ring**: a drawing that shows the values running out understands why a `for` loop cannot run forever.

### Self-Check

The "I can…" rows are self-rated: no answers. If a row is marked 😕, point at the matching Build It part. The true-or-false rows:

| Statement | Answer |
|---|---|
| `range(5)` hands out 1, 2, 3, 4, 5 | **False.** 0, 1, 2, 3, 4. |
| `range(5)` hands out five values | **True.** The last one is 4. |
| You must set the loop counter yourself before the loop | **False.** Python fills it from `range`, once per pass. |
| `range(3, 3)` causes an error | **False.** It runs zero passes and prints nothing. |
| `total += n` is different from `total = total + n` | **False.** Identical. |
| An accumulator should be created inside the loop | **False.** Before it, or it gets wiped every pass. |
| The average should be worked out inside the loop | **False.** After it, when the adding has finished. |
| `"=" * 20` prints twenty equals signs | **True.** |
| `"=" * "20"` prints twenty equals signs | **False.** `TypeError` — the count must be a number. |
| An off-by-one bug usually has a clear error message | **False.** It usually has none at all. |
| In a nested loop, the inner loop finishes completely on every pass of the outer one | **True.** That is why 4 outer × 3 inner = 12. |
| Loops make a program run faster | **False.** They make it shorter, easier to change, and harder to get wrong in ten places at once. |

### Lesson questions posed in the Say-this scripts

- *"How many `print` lines are in my file?"* → One.
- *"How many lines came out?"* → Ten, then a hundred. One `print`, a hundred lines.
- *"What's the only difference between the row for 4 and the row for 5?"* → The number. The answer is made from the number, which is why one line produces both.
- *"How long would a thousand rows take you by hand?"* → Hours, with typos in it.
- *"Is anything on the screen something you could not have typed by hand?"* → No. A loop does the same work, written once.
- *"Who puts a value in `n`?"* → Python does, through the `for` line, one value per pass.
- *"`range(4)` — how many values, and what's the last one?"* → Four values; the last is 3.
- *"How many values does `range(3, 20)` hand out?"* → 17, because 20 − 3 = 17.
- *"Why does the total have to be created before the loop?"* → Because a box made inside the loop is remade every pass, so it can never carry anything across.
- *"Is `total += n` different from `total = total + n`?"* → No. Identical; just shorter and harder to typo.
- *"In my accumulator program, how many boxes named `total` are there?"* → One. It changes twelve times.
- *"Which of my two mistakes had an error message?"* → The missing colon. The `total = 0` in the wrong place had none.
- *"Which was worse?"* → The silent one, because nothing told you it had happened.
- *"Say the three accumulator rules."* → Set up before · add inside · use after.
- *"Did it crash?"* (Part 3) → No.
- *"How many numbers are on the card?"* → Twelve.
- *"How many did it ask for?"* → Eleven. Count the lines.
- *"So what's in your hand?"* → 73. It was never asked for.
- *"Why does `highest` start at −1?"* → Because 0 is a possible score and `0 > 0` is `False`. Start below every possible value and you never have to be lucky.

---

## 🔮 Next Week Preview

This section tells you what comes next week and what to prepare before it.

Week 8 is the project week, and it introduces the loop you cannot count in advance.

A `for` loop knows how many passes it will do before it starts the first one. That is why it can never run forever. Next week's **`while` loop** knows nothing of the kind: it checks a condition, runs the block, checks again, and keeps going for exactly as long as the answer stays `True`. That is what you need in order to write a program that waits for a human to get something right, because you have no idea how many tries a human will take.

Next week the student will:

- build **`guess.py`** — a secret number, higher/lower hints, a seven-try limit, and a replay loop
- write an infinite loop **on purpose**, watch it print forty thousand lines a second, and stop it with Ctrl+C in a controlled setting rather than in a panic at eleven at night
- harden it so that typing `banana` at every prompt cannot crash it

**Prep early:** three things.

1. **Keep this week's twelve-score index card.** Next week's `grade.py` uses the same twelve numbers, and the fact that the answer is still 900 and 75 is worth a lot when the program around it has changed shape.
2. **Find out where Ctrl+C is on the student's keyboard, and confirm it works.** On a Mac it is Ctrl, not Command, and a student who reaches for Command-C during a runaway loop will only copy something. Try it on this week's `seven_times.py` with `range(1, 1000000)` so you have both done it once when nothing was at stake.
3. **If the off-by-one landed hard and the accumulator did not, spend the first five minutes of next week re-running `scores.py`** rather than pressing on. `grade.py` is built directly on top of it and there is no point building on sand.

---

[⬅ Week 6](week-06.md) · [Course Home](../README.md) · [Week 8 ➡](week-08.md) · [Student Guide](../student-guide/week-07.md) · [Workbook](../workbook/week-07.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
