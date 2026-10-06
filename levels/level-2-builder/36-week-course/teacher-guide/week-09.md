# Week 9 — Term 1 Checkpoint: You Keep Typing the Same Five Lines

[⬅ Week 8](week-08.md) · [Course Home](../README.md) · [Week 10 ➡](week-10.md) · [Student Guide](../student-guide/week-09.md) · [Workbook](../workbook/week-09.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟪 Review — Term 1 checkpoint, taught by deleting twenty lines of the student's own code |
| **Big idea** | When the same block appears three times, give it a name. A function is a named block you can run whenever you want. |
| **New vocabulary** | function · define · call · return |
| **New syntax** | `def name():` · `name()` · `return value` |
| **Materials** | Printed workbook pages 9.1–9.6 · **three coloured pencils or highlighters** · the student's notebook, open at the **Bug Log**, with every entry from weeks 1–8 · a timer · the **weeks 1–8 code folder, on screen, with the real filenames** |
| **Tech needed** | Python 3, an editor that can show two files side by side (or two windows), one terminal. **No libraries at all** — nothing to install. |
| **Prep time** | 20 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** this week's material is **the student's own code**, and that is the entire design. Do not substitute the examples in this file for their files. The moment that makes a function feel necessary is the moment they see *their own* five lines, in *their own* handwriting, sitting in three different files — and that moment cannot be manufactured with somebody else's program. **Check the night before that those files still exist and still run.** If they have been deleted, spend the first ten minutes retyping one of them together; that is a better lesson than a substitute.

> **⚠️ Also watch out:** the second half is a timed repair round over ten broken programs, and the output of this lesson is **a list of weeks to revisit, not a mark.** If the student produces a number and treats it as a grade, the checkpoint has failed. Say so out loud before you start the timer.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Repair ten broken programs drawn from weeks 1–8**, unaided, and say what was wrong with each in one sentence.
2. **Name the error family for every traceback in their Bug Log from the message alone** — without seeing the code.
3. **Define a function with `def` and call it by name**, and explain why defining it is not the same as running it.
4. **Explain what `return` hands back**, and what happens when a function has no `return`.
5. **Produce their own list of which weeks need revisiting** — a list, not a grade.

Observable evidence: ten repaired programs that run; a Bug Log where every entry has been sorted into one of three families; one file in which a repeated block has been replaced by a function and whose output is **byte-identical** to the original (proved with `diff`); and a written revision list naming specific weeks and specific reasons.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

**You do not need to have programmed before to teach this.** Read this once with the laptop open and type every program in it. About 25 minutes. This week has one new idea, and it is the idea that separates "someone who can write ten lines" from "someone who can write a program".

### 1. The problem functions solve, in one concrete example

Here is a file that repeats itself. It is not a made-up example — it is exactly the shape of what your student has been writing for eight weeks. Save it as `report_long.py` and run it.

```python
# report_long.py - the version with the same five lines pasted three times.

print()
print("=" * 34)
print("   AI ACADEMY  -  SCORE REPORT")
print("=" * 34)
print()

print("Scores added : 12")
print("Total        : 900")

print()
print("=" * 34)
print("   AI ACADEMY  -  SCORE REPORT")
print("=" * 34)
print()

print("Average      : 75.00")
print("Highest      : 100")

print()
print("=" * 34)
print("   AI ACADEMY  -  SCORE REPORT")
print("=" * 34)
print()
```

The real output:

```text

==================================
   AI ACADEMY  -  SCORE REPORT
==================================

Scores added : 12
Total        : 900

==================================
   AI ACADEMY  -  SCORE REPORT
==================================

Average      : 75.00
Highest      : 100

==================================
   AI ACADEMY  -  SCORE REPORT
==================================
```

**Count what is wrong with that file. There are three things, and only one of them is "it's long".**

1. **Fifteen lines say one thing.** The five-line banner appears three times.
2. **If the wording changes, there are three places to change it.** Miss one and you have a report with two different headings and no error message anywhere.
3. **You cannot tell by looking whether the three copies are identical.** They might differ by a space. You would never know.

That third one is the real cost, and it is worth saying to the student in exactly those words: **duplicated code is code you cannot check.**

![The same five lines, pasted in three places](../figures/fig-w09-1-repeated-block-three-times.svg)
*Figure 9.1 — One idea, three places. The problem is not the typing; it is that changing your mind now means changing your mind three times without missing one.*

### 2. `def` and the call — two separate things, and this is the whole lesson

Here is the same program with the banner named. Save it as `report_short.py`.

```python
# report_short.py - the same output, with the five lines named once.

def print_header():                              # DEFINE: here is a block called print_header
    print()                                      # everything indented belongs to it
    print("=" * 34)
    print("   AI ACADEMY  -  SCORE REPORT")
    print("=" * 34)
    print()

print_header()                                   # CALL: run that block, now
print("Scores added : 12")
print("Total        : 900")

print_header()                                   # CALL it again - no retyping
print("Average      : 75.00")
print("Highest      : 100")

print_header()                                   # and again
```

**Run both files and compare their output.** Here is the check, and it is the check the student must do too:

```text
$ python3 report_long.py > long.txt
$ python3 report_short.py > short.txt
$ diff long.txt short.txt
$ 
```

`diff` printed nothing, which is how `diff` says *"these two files are identical."* Twenty-five lines became eighteen and **not one character of output changed.**

> **function** — a named block of code you write once and run whenever you like.
> **define** — writing the block down and giving it a name. `def print_header():`. Nothing runs.
> **call** — running it. `print_header()`. The block runs, top to bottom.

**The two-column table below is the single most useful thing on this page. Draw it on paper for the student.**

```text
   DEFINING                            CALLING
   def print_header():                 print_header()
   "Here is a recipe."                 "Cook it, now."
   Nothing runs.                       The whole block runs.
   You do it once.                     You do it as often as you like.
   The colon and the indent matter.    The brackets matter.
```

**A function you define and never call does absolutely nothing.** That is not a bug; it is the entire point of separating the two acts. Run this and see:

```python
def print_header():
    print("=" * 20)
```

```text
```

No output. No error. Exit code 0. Python read the recipe, filed it under `print_header`, and reached the end of the file with nothing to do. **If a student runs a file and gets no output whatsoever, the first question is always "did you call it?"**

And here is the near-miss version, which is worse because it looks right:

```python
def print_header():
    print("=" * 20)

print_header
```

```text
```

Also nothing. `print_header` without brackets is the *name* of the function — it refers to the recipe rather than cooking it. **The brackets are what mean "do it".** This one has no error message at all and it catches people for years.

![Define it once, call it as often as you like](../figures/fig-w09-2-function-machine-named.svg)
*Figure 9.2 — The machine is defined once and sits there. Each call is a press of the button. A machine nobody presses does nothing, and that is not a fault.*

### 3. Why the indent and the colon are the same rules as before

Good news for you: there is **no new punctuation this week.** `def name():` uses exactly the two rules the student already knows from `if` and `for`:

- **A colon at the end** means "the indented block below belongs to me."
- **The indent is the block.** Everything indented under the `def` is inside the function; the first line back at the margin is outside it again.

So the three errors they already know how to read all show up here in a new place:

```python
def print_header()
    print("=" * 20)
```

```text
  File "/Users/you/ai-academy/level2/header.py", line 1
    def print_header()
                      ^
SyntaxError: expected ':'
```

Same message as a `for` with no colon. Same fix.

```python
def print_header():
print("=" * 20)
```

```text
  File "/Users/you/ai-academy/level2/header.py", line 2
    print("=" * 20)
    ^
IndentationError: expected an indented block after function definition on line 1
```

Same shape as `for` with no indented body — and notice Python names the construct precisely: *"after function definition"*. **Python's error messages tell you which kind of block you failed to fill in.** That is worth pointing out; it turns a scary message into a useful one.

### 4. `return` — the thing that makes functions worth having

So far every function has printed. `print` puts characters on the screen where a human can read them. **`return` hands a value back to the line that called the function**, so the program can use it.

> **return** — immediately ends the function and hands one value back to whoever called it.

This is the distinction that matters most, and the fastest way to see it is side by side. Type this file:

```python
# show_vs_give.py - one shouts the answer, the other hands it over.

def show_average():          # this one PRINTS. It hands nothing back.
    print(75.0)

def give_average():          # this one RETURNS. It hands 75.0 back.
    return 75.0

shouted = show_average()     # the 75.0 appears on screen...
print(shouted)               # ...but what landed in the box?

handed = give_average()      # nothing appears on screen...
print(handed)                # ...until we print what landed in the box
print(handed + 25)           # and it is a real number, so maths works
```

The real output — four lines, and the second one is the lesson:

```text
75.0
None
75.0
100.0
```

Walk those four lines with a finger:

| Line of output | Where it came from |
|---|---|
| `75.0` | `show_average()` printing. The value went to the screen. |
| `None` | `print(shouted)`. **The box is empty.** A function with no `return` hands back `None`, Python's word for "no value at all". |
| `75.0` | `print(handed)`. The returned value, printed by *us*, not by the function. |
| `100.0` | `handed + 25`. It is a real number, so it can be used. |

**And here is what happens if you try to do maths with a shouted answer:**

```python
def show_average():
    print(75.0)

print(show_average() + 25)
```

```text
75.0
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/shout_maths.py", line 4, in <module>
    print(show_average() + 25)
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

The `75.0` was printed — you can see it — and then the program crashed trying to add 25 to nothing. **`NoneType` in a `TypeError` almost always means "a function you called forgot to return something."** That is one of the most useful sentences in this whole course and it will save the student an hour in Week 10.

![Shouting it across the room, or handing over the plate](../figures/fig-w09-3-return-hands-it-back.svg)
*Figure 9.3 — Printing sends the answer to the screen and leaves the caller's hands empty. Returning puts it in the caller's hands, where it can be stored, added to, or printed later.*

**The analogy to use out loud:**

- **A function that prints is a waiter who shouts your order across the restaurant.** Everyone hears it. Nobody can eat it.
- **A function that returns is a waiter who brings the plate to your table.** Now you can eat it, share it, weigh it, or take a photo.

You can always print a returned value — `print(give_average())` works fine. You can **never** recover a printed one. So the rule, which the student should write down: **return by default; print only at the very edge of the program, where a human is actually reading.**

Here is `return` doing real work, using Week 7's accumulator:

```python
# average_fn.py - a function that hands a number back.

def average_of_twelve():                   # DEFINE - no input, one answer out
    total = 0                              # week 7's accumulator, now living inside
    for i in range(1, 13):                 # 1, 2, 3 ... 12
        total += int(input(f"Score {i} of 12: "))
    return total / 12                      # RETURN - hand the answer back

average = average_of_twelve()              # CALL - and catch what comes back
print(f"Average : {average:.2f}")
print(f"Doubled : {average * 2:.2f}")      # you can do maths with a returned value
```

Typing the twelve numbers from Week 7's index card (88 92 70 65 100 54 78 81 47 90 62 73), the last two lines are:

```text
Average : 75.00
Doubled : 150.00
```

Same 75 as Week 7 and Week 8, from a program with a completely different shape. **That agreement across three weeks is the checkpoint doing its job.**

### 5. What `return` does to the rest of the function

One more fact, and it is short: **`return` ends the function immediately.** Nothing after it runs.

```python
def give_average():
    return 75.0
    print("this line never runs")
```

Call it and nothing is printed. That is not a bug and there is no warning. Say it once, plainly, and move on — a student who puts a `print` after a `return` and cannot see why it is silent has met one of the classic five-minute mysteries.

### 6. What this week deliberately does **not** cover

Week 9 gives functions with **no inputs**. `print_header()` prints the same banner every time and there is nowhere to tell it "make it forty wide instead of thirty-four". That hole is obvious, students notice it, and **it is Week 10's entire lesson.**

When they notice — and a good student will, within about four minutes — say exactly this: *"You've found next week. That's a real limitation and the answer is one line of new syntax. Write the question down."* Do not teach parameters today. Two new ideas in a checkpoint week is one too many, and the checkpoint half of the lesson is the half that matters more.

Also not today: `None` as a vocabulary word (show the output, name it next week) · scope, and why a variable inside a function is invisible outside it (Week 10) · docstrings · returning more than one value · functions calling themselves.

### 7. The three error families — the backbone of the second half

The repair round works because of a sorting idea, and it is worth having in your own head before you teach it. **Every mistake in Term 1 falls into one of three families, and you can tell which from the message alone.**

| Family | What you see | What it means | Members met so far |
|---|---|---|---|
| **It never started** | **No output at all**, and a `^` under one spot in your file | Python could not even read the file. Nothing ran. | `SyntaxError`, `IndentationError` |
| **It started, then stopped** | Some output, then `Traceback (most recent call last):`, a **line number**, and a message | Python read the file fine and got partway through before hitting something impossible | `NameError`, `TypeError`, `ValueError`, `ZeroDivisionError`, `AttributeError`, `KeyboardInterrupt` |
| **It finished, and lied** | **No message anywhere.** A complete, confident, wrong answer | The program is exactly what the file says. The file is not what you meant. | wrong `elif` order, off-by-one, a line at the wrong indent, `.isdigit` without brackets, text compared with a number |

![Three families of trouble](../figures/fig-w09-4-term1-error-family-tree.svg)
*Figure 9.4 — Read the last line first: it names the family. Then read the line number: it names the place. The third family has neither, which is what makes it the expensive one.*

**Two things to be able to say confidently, because a student will ask both:**

- **Why is "it never started" the friendliest?** Because you find out instantly and nothing wrong has happened yet. No file was written, no answer was reported, nobody was told anything untrue.
- **Why is the third family the expensive one?** Because it survives. It goes into the homework, into the marks the program printed, into next term. The grade program from Week 6 would have handed thirty students a wrong grade and nobody would ever have known.

### 8. The three misconceptions you will actually meet

**Misconception 1 — "defining it runs it."** A student writes a `def`, runs the file, sees nothing, and concludes the function is broken. **The fix:** ask "how many times did you tell Python to run it?" Then add the call and watch it appear. Then delete the call and watch it vanish. Twice each way.

**Misconception 2 — "`return` prints it."** They write `return` and expect output. Nothing appears, so they add a `print` *inside* the function as well, and now they have both — which works, and hides the confusion until Week 10. **The fix:** the four-line output of `show_vs_give.py` and a finger on the word `None`.

**Misconception 3 — "a function makes the program shorter, so that's the point."** Length is the least of it. **The fix is a question:** *"You've got the banner in three files. I want the heading to say LEVEL 2 instead of AI ACADEMY. How many places do you have to change it, and how do you know you got all of them?"* Then the same question with the function version. One place. Certainty.

### 9. How deep to go, and where to stop

**Go this far:** `def name():` with a colon and an indented body · `name()` with brackets to run it · define-once-call-many · defining is not running · `return value` hands one value back · a function with no `return` hands back `None` · `return` ends the function · sorting a traceback into one of three families from the last line alone · repairing broken programs from weeks 1–8 unaided.

**Stop before:** parameters and arguments (Week 10) · default values (Week 10) · scope (Week 10) · returning two things · `None` as vocabulary · lists (Week 11) · anything about whether functions should be "pure".

**And one thing to stop yourself doing:** do not turn the repair round into a lecture. Ten programs in twelve minutes means about seventy seconds each, and your job during those twelve minutes is to say almost nothing. If they are stuck for more than ninety seconds on one, tell them to write down which week it came from and move to the next. **The list of weeks is the product of this lesson. The repairs are just how the list gets written.**

---

### 10. 🧭 The Growing Map — the week a whole stage closes

**Where This Fits** is the one figure in the student guide that is not about this week's content. It
shows the shape of the year with one more piece filled in, and this week it marks the end of a stage.

![The Level 2 pipeline in Week 9: the second tile of stage one closes, and all of speak Python is filled in](../figures/fig-w09-0-where-this-fits.svg)

*Figure 9.0 — Week 9's version. The gold tile, `choices · loops`, finishes here. From Week 10 the whole
of stage one is plain white and the badge crosses the first arrow into stage two.*

**How to run it, in about two minutes:**

1. **Show it and ask the checkpoint question:** *"we gave a name to a block we had already typed three
   times — which tile did that just finish?"* They point at the gold tile. Then tell them plainly: that
   tile closes today, and the whole of stage one is now behind them.
2. **Ask why the rest is dashed** and take "we haven't done it yet" as a complete answer — then add the
   one sentence they will remember: *"next week we stop typing the data in ourselves and start holding
   it."* The arrow between stage one and stage two is worth pointing at while you say it.
3. **Have them ink in stage one on their own pencil copy.** Nine weeks, one stage, in pen. Term 1's
   product is not a program; it is a learner who can read their own file and fix it.

> **🧑‍🏫 Why this is worth two minutes.** This is a checkpoint week and some of the class will arrive
> at it feeling like they have learned an assortment of unrelated tricks. The map is the argument that
> they have not: printing, variables, decisions, loops and functions are one stage of one pipeline.

> **⚠️ Watch out:** there is no assessment in this. A learner who cannot name the five stages has lost
> nothing this week. The point is that they have seen the whole year has a shape and an end.

---

## 🧰 Prep Checklist

### 20 minutes the night before

- [ ] **Open the student's weeks 1–8 folder and check the files are there and still run.** This is the most important item on the list, because the whole first half of the lesson is their own code. You are looking for: `about_me.py` (Week 4), `grade.py` (Week 6 and again Week 8), `seven_times.py` and `scores.py` (Week 7), `guess.py` (Week 8). If two of them are gone, the Hook still works with one file and the pasted block inside it.
- [ ] **Find the repetition yourself, in advance.** Open two or three of their files side by side and look for a block of three or more identical lines. It will almost certainly be a banner — `print("=" * 40)` and a title and another `print("=" * 40)`. **Write down the exact filenames and line numbers.** You want to be able to say "open `guess.py` and `grade.py`" and not hunt during the lesson.
- [ ] **Type and run both `report_long.py` and `report_short.py`** from section 1, and run the `diff`:

  ```text
  $ python3 report_long.py > long.txt
  $ python3 report_short.py > short.txt
  $ diff long.txt short.txt
  $ 
  ```

  **`diff` printing nothing is the result you want.** If you have never used `diff`, that silence is unnerving — do it once now so it does not surprise you in front of a student. (If you would rather not use the terminal for this, `wc -l` on the two program files gives 25 and 18, and reading the two outputs side by side works fine.)
- [ ] **Type and run `show_vs_give.py`** from section 4 and confirm you get exactly:

  ```text
  75.0
  None
  75.0
  100.0
  ```

  **Sit with the `None` for a second.** That single word is the hardest thing in the lesson and you need to have met it calmly.
- [ ] **Print the ten broken programs** from the Answer Key onto ten separate slips, or set up ten files named `bug01.py` … `bug10.py`. Ten files is better if the machine is reliable; slips are better if you want the student's hands off the keyboard while they diagnose.
- [ ] **Read the student's Bug Log from the start.** Count the entries and note which weeks they came from — that count is your best single piece of evidence about which weeks need revisiting, and it takes four minutes to read.
- [ ] **Have three coloured pencils.** The repetition hunt uses one colour per repeated block, and colour is the whole mechanism.
- [ ] Say the big idea out loud: *"three copies is not a length problem, it's a truth problem — you can't check three copies are the same."*

### 5 minutes on the day

- [ ] Terminal open in `~/ai-academy/level2`. Run `report_long.py` once to prove the setup works.
- [ ] **Two editor windows, side by side, already showing two of the student's own files** — the two you found last night with the same banner in both. This should be on screen at minute zero.
- [ ] The ten bug files or the ten slips, ready but out of sight.
- [ ] The Bug Log open on the table, at the first page.
- [ ] Three coloured pencils. A timer.
- [ ] **A blank sheet headed "Weeks to revisit".** Put it on the table where they can see it from the start, so the lesson's product is visible before the lesson begins.

### Fallback if the laptop or the install fails

| If this fails | Do this instead |
|---|---|
| **No laptop** | Print two of their own programs and hand over the coloured pencils. The repetition hunt is *better* on paper — circling the same five lines in three places with a pencil is more visceral than highlighting on a screen. Then have them write the function version by hand, and read both aloud to check the output would be identical. The repair round works entirely on paper: give them the ten printed programs and have them write the family, the diagnosis and the fix for each. |
| **Their weeks 1–8 files are gone** | Do not substitute a stranger's code silently. Say what happened, then spend ten minutes retyping the Week 4 banner and the Week 8 banner from the printed workbook — and then the repetition is real again because they just typed it twice themselves. That is a better lesson than a stand-in. |
| **The Bug Log is nearly empty** | Then that is the finding, and it goes on the revision list first. Build one now, retrospectively: go through the ten repair programs and write an entry for each. Ten entries in twelve minutes, and the habit starts this week. |
| **`diff` is intimidating or unavailable** | Skip it. Run both programs, put the two terminal windows side by side, and read the outputs aloud in unison. Slower, entirely convincing. |
| **The whole thing is done in thirty minutes** | Go to the flying path: three functions extracted rather than one, a function that calls another function, and the `return` version of the Week 7 average. |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — The Repetition Hunt | 7 | 7 | Their own files, three colours, one uncomfortable count |
| 🧠 Concept — Give the Block a Name | 16 | 23 | `def`, the call, `return`, and the three error families |
| 💻 Live-Code Together — Lift It Out | 18 | 41 | Extract the block live. Two deliberate mistakes, both silent. |
| 🎲 Their Turn — Ten Repairs, Timed | 20 | 61 | The repair round, then the revision list |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the reflection sheet, homework |

---

### 🪝 Hook — The Repetition Hunt (7 minutes)

**Do this:** two of the student's own files, side by side on screen, already open. Three coloured pencils on the table. **Do not say what you are looking for.**

**Say this:**

> "Before we do anything new, I want you to look at something you already wrote.
>
> That's your `guess.py` on the left, from last week. That's your `grade.py` on the right. You wrote both. Nobody helped you.
>
> **Find me something that is in both of them.** Not something *similar* — something *identical*. Character for character."

Wait. They will find the banner within about thirty seconds — the `print("=" * 40)`, the title, the second `print("=" * 40)`.

> "Good. Take a pencil and circle it. Both copies, same colour."

Then:

> "Now open `about_me.py` from Week 4."

They will find it a third time, or something very close to it.

> "Circle that one too. Same colour."

**Now the count. This is the moment.**

**Say this:**

> "How many lines are in one copy?"

(Four? Five?)

> "And how many copies did we find?"

(Three.)

> "So how many lines have you typed, in total, to say that one thing?"

(Fifteen.)

> "Fifteen lines. One idea. Now — three questions, and the third one is the one I actually care about.
>
> **One.** I've decided the heading should say `LEVEL 2` instead of `AI ACADEMY`. How many places do you have to change?"

(Three.)

> "**Two.** What happens if you change two of them and forget the third?"

(Two files say one thing and one says another.)

> "And does Python tell you?"

(No.)

> "No. It's the third family of trouble from your Bug Log — a program that finishes and lies. Except this time it isn't even wrong, exactly. It's just inconsistent, quietly, and nobody finds out until somebody notices two reports don't match.
>
> **Three, and this is the real problem.** Look at the three circles. **Can you tell me, right now, without reading them character by character, that all three are identical?**"

Let them try. They cannot. One of them almost certainly has a different number of equals signs or an extra space.

> "You can't. And neither can I. **That's the actual cost of copying code: not that it's long, but that you can't check it.** Three copies is three separate truths and you are trusting your memory to keep them the same.
>
> So today you're going to give that block a name, write it down **once**, and then use the name. And when you change your mind about the wording, you'll change it in one place, and it will be impossible to miss the others, because there won't be any."

Show Figure 9.1.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Find something identical in both files." | The banner block. | If they cannot, point at the top of each file and say "start here". Banners live at the top. |
| "How many lines have you typed to say one thing?" | Fifteen, or however many their block is × 3. | The number matters less than the multiplication. Make them say it as "five times three". |
| "If the wording changes, how many places?" | Three. | If they say one, ask them to show you which one. Then ask about the other two. |
| "Does Python warn you if you miss one?" | No. | Connect it to the Bug Log's third family immediately. This is not a new kind of problem. |
| "Can you prove all three copies are identical?" | No — not without reading every character. | **This is the answer that makes the lesson necessary.** If they say yes, ask them to count the equals signs in all three. Someone will be wrong. |

---

### 🧠 Concept — Give the Block a Name (16 minutes)

**Do this:** a new file, `report_short.py`. You will build the idea in miniature before touching their real code.

**Say this — part 1, the two acts:**

> "New word first, because you need it to talk about what you're about to do. A **function** is a named block of code you write once and run whenever you like.
>
> You have been using functions since Week 1. `print` is a function. So are `input`, `int`, `len` and `range`. Somebody wrote those and gave them names, and you have been calling them by name ever since without ever seeing the block inside. **Today you write your own.**
>
> And there are two completely separate acts, and telling them apart is most of today."

Write this up and leave it up:

```text
   DEFINING                            CALLING
   def print_header():                 print_header()
   "Here is a recipe."                 "Cook it, now."
   Nothing runs.                       The whole block runs.
   You do it once.                     You do it as often as you like.
```

> "Look at the left column. `def`, then the name you choose, then a pair of empty brackets, then a colon — and then the block, indented. **You already know both of those punctuation rules.** The colon means 'the indented bit below belongs to me', exactly like `if` and `for`. And the indent *is* the block, exactly like `if` and `for`. There is no new punctuation this week at all.
>
> Now look at the right column. To run it, you say its name with brackets after it. That's called **calling** it."

Type it in front of them:

```python
def print_header():
    print()
    print("=" * 34)
    print("   AI ACADEMY  -  SCORE REPORT")
    print("=" * 34)
    print()
```

**Run it — with no call.** The real output:

```text
```

Nothing. Silence.

**Say this:**

> "Nothing happened. And I want to be really clear that nothing is broken. Python read that file, found a recipe, wrote the recipe down under the name `print_header`, got to the end of the file, and had nothing else to do. **Defining a function does not run it.**
>
> That is not a wart. It's the entire reason this is useful — the recipe sits there, and *you* decide when to cook it. Watch."

Add one line at the bottom:

```python
print_header()
```

Run. The banner appears. Add two more calls. Run. Three banners.

> "One definition. Three calls. And if I want to change the wording, how many places?"

(One.)

**Say this — part 2, the near-miss:**

> "One trap, and it's silent, so I'm showing it to you before it happens. Watch what I do to the last line."

Delete the brackets:

```python
print_header
```

Run it.

```text
```

> "Nothing again. No error. What do you think happened?"

Let them guess. Then:

> "`print_header` without brackets is the **name** of the recipe. It's a reference to the thing. `print_header()` **with** brackets means *do it*. I asked Python to think about the recipe, and it did, silently, and then moved on. **The brackets are what mean 'actually run it'**, and you're going to meet exactly this again in about ten minutes with `.isdigit` from last week — same trap, same missing brackets."

Show Figure 9.2.

**Say this — part 3, `return`:**

> "Now the bigger half. Every function I've shown you so far prints. Printing sends characters to the screen where a human can read them, and that's it — the value is gone.
>
> **`return` hands the value back to the line that called the function.** Which means the program can use it. Type this with me — two functions that look almost the same and are completely different."

```python
def show_average():          # this one PRINTS. It hands nothing back.
    print(75.0)

def give_average():          # this one RETURNS. It hands 75.0 back.
    return 75.0

shouted = show_average()     # the 75.0 appears on screen...
print(shouted)               # ...but what landed in the box?

handed = give_average()      # nothing appears on screen...
print(handed)                # ...until we print what landed in the box
print(handed + 25)           # and it is a real number, so maths works
```

Run it:

```text
75.0
None
75.0
100.0
```

> "Four lines out. Walk them with me.
>
> **Line one, `75.0`** — that's `show_average` printing. It shouted the number at the screen.
>
> **Line two, `None`** — and this is the whole lesson. That's me printing `shouted`, which is the box I put the result in. **The box is empty.** `None` is Python's word for 'no value at all'. `show_average` printed a number and handed back nothing, so `shouted` got nothing.
>
> **Line three, `75.0`** — same number, but this time *I* printed it, not the function. The function handed it over and I chose to display it.
>
> **Line four, `100.0`** — and this is why it matters. I added 25 to it. **You can do maths with a returned value. You cannot do maths with a printed one**, because a printed one isn't anywhere any more.
>
> Here's the way to remember it. A function that prints is a waiter who **shouts your order across the restaurant** — everyone hears it, nobody can eat it. A function that returns is a waiter who **brings the plate to your table.** Now you can eat it, share it, weigh it, take a photo of it.
>
> And notice: you can always print a returned value. You can never recover a printed one. So: **return by default. Print only right at the edge, where a person is reading.**"

Show Figure 9.3.

**Say this — part 4, the three families:**

> "Last five minutes of concept, and it's revision rather than new. Open your Bug Log at page one.
>
> Every single thing that has gone wrong for you in eight weeks belongs to one of **three families**, and you can tell which one from the message alone — you don't even need to see the code."

Write the three up, and go through the Bug Log entry by entry, sorting them out loud:

```text
   1.  IT NEVER STARTED       no output at all, and a ^ under one spot
                              SyntaxError, IndentationError

   2.  IT STARTED, THEN       some output, then "Traceback", a line number,
       STOPPED                and a message
                              NameError, TypeError, ValueError,
                              ZeroDivisionError, AttributeError,
                              KeyboardInterrupt

   3.  IT FINISHED,           no message anywhere. A confident wrong answer.
       AND LIED               wrong elif order, off-by-one, wrong indent
```

> "Family one is the **friendliest**. You find out instantly and nothing bad has happened yet — no file was written, nobody was told anything untrue.
>
> Family two is the **most informative**. It gives you a line number, which is a genuine gift.
>
> Family three is the **expensive** one, because it survives. Your Week 6 grade program would have handed out thirty wrong grades and nobody would ever have found out. **Count how many of your Bug Log entries are family three.**"

Let them count. It will be more than they expect.

Show Figure 9.4.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "What's the difference between defining and calling?" | Defining writes the recipe and runs nothing. Calling runs it. | If they blur the two, delete the call, run, and let the silence answer. |
| "I define a function and never call it. What happens?" | Nothing at all. No output, no error. | If they say "an error", run it. Exit code 0, no message. |
| "What's the difference between `print_header` and `print_header()`?" | The brackets mean "do it". Without them, nothing runs and nothing complains. | Connect it to `.isdigit` versus `.isdigit()` from last week. Same trap. |
| "What does a function with no `return` hand back?" | `None` — no value at all. | If they say "nothing" — right, and Python has a word for nothing, and it prints as `None`. |
| "Why can't I do maths with a printed answer?" | Because printing sends it to the screen and does not keep it anywhere. | Show `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` and read the word `NoneType` out loud. |
| "How many of your Bug Log entries had no error message?" | Whatever the honest count is — usually a third or more. | The count is the point. Write it on the revision sheet. |

---

### 💻 Live-Code Together — Lift It Out (18 minutes)

**Do this:** now the real thing — **their file, their banner.** The student types. Three passes, and **two deliberate mistakes you make and fix in front of them.** Both are silent, which is deliberate: functions fail quietly.

#### Pass 1 (6 min) — the extraction, on their own file

**Say this:**

> "Open `grade.py`. Your own. We're going to take those five circled lines out and give them a name, and when we're done the program has to print **exactly** what it printed before. Not nearly. Exactly."

**Exact keystroke sequence:**

1. **Copy** the five banner lines. Do not retype them — copy them. Say why: *"if we retype them and the output changes, we won't know whether it was the function or the typing."*
2. Go to the **top** of the file, below any `import`.
3. Type `def print_header():` and press Enter.
4. **Paste** the five lines and indent all five by four spaces (most editors: select them and press Tab).
5. Leave a blank line.
6. Go back down to where the banner used to be and **delete the original five lines**, replacing them with `print_header()`.

Run it. It should look identical to before.

> "Now prove it. Not 'it looks right' — **prove it.**"

Show them the check:

```text
$ python3 report_long.py > long.txt
$ python3 report_short.py > short.txt
$ diff long.txt short.txt
$ 
```

> "`diff` compares two files and tells you every line that differs. It printed **nothing**, which is how it says 'these are identical'. That silence is the strongest evidence you have produced all term."

For their own file, run the before-and-after version of the same trick: save the output before the change, then after, then `diff`. If the terminal is a step too far, run both and read the two outputs aloud together.

> "Twenty-five lines became eighteen in my example. But look at what actually changed: **there is now exactly one place in the whole file where that heading is written down.** If you want it to say LEVEL 2, you change one line and it is impossible to miss a copy, because there are no copies."

#### Pass 2 (6 min) — ⚠️ **DELIBERATE MISTAKE #1**, the function nobody calls

**Say this:**

> "Now I'm going to break it in a way that has no error message whatsoever, and I want you to catch it."

Delete the `print_header()` call — all of them — but leave the `def`. Run it.

The real output: the report body appears, with **no banners at all**, and no error message.

**Say this:**

> "Did it crash?"

(No.)

> "Is the banner code still in the file?"

(Yes — they can see it.)

> "Read the definition out loud. Is anything wrong with it?"

(No, it's fine.)

> "It's perfect. Every character of it is correct. So why is there no banner?"

Wait. Do not answer this. If they need a nudge, ask: *"how many times did you tell Python to run it?"*

(Zero.)

> "Zero. **A recipe nobody cooks makes no dinner.** And this is the number one thing that happens to people learning functions: the file gets longer, the output gets shorter, and nothing complains. Whenever you write a `def` and get less output than you expected, the first question is always the same: **did you call it?**"

Put the calls back.

#### Pass 3 (6 min) — ⚠️ **DELIBERATE MISTAKE #2**, print instead of return

**Say this:**

> "Second one, and this is the mistake you will actually make in April. We're going to write a function that works out an average — Week 7's accumulator, but with a name on it."

Type this, using `print` where `return` belongs:

```python
def average_of_twelve():
    total = 0
    for i in range(1, 13):
        total += int(input(f"Score {i} of 12: "))
    print(total / 12)          # <-- this is the mistake

average = average_of_twelve()
print(f"Average : {average:.2f}")
```

Run it, and type the twelve numbers from the Week 7 card. The real result:

```text
Score 1 of 12: 88
Score 2 of 12: 92
Score 3 of 12: 70
Score 4 of 12: 65
Score 5 of 12: 100
Score 6 of 12: 54
Score 7 of 12: 78
Score 8 of 12: 81
Score 9 of 12: 47
Score 10 of 12: 90
Score 11 of 12: 62
Score 12 of 12: 73
75.0
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/average_bad.py", line 8, in <module>
    print(f"Average : {average:.2f}")
TypeError: unsupported format string passed to NoneType.__format__
```

**Say this:**

> "Look at that carefully, because it is genuinely confusing the first time and you need to see through it.
>
> **The answer is on the screen.** `75.0`. It's right there, it's correct, it's the right number. And then the program crashed on the very next line.
>
> Read the last line. What word jumps out?"

(NoneType.)

> "`NoneType`. That's Python saying 'the thing you gave me is `None` — no value at all.' So where did the `None` come from?"

Walk them to it: `average = average_of_twelve()`. The function printed the number and returned nothing, so `average` holds `None`, and `:.2f` cannot format nothing.

> "**Here is the sentence I want you to memorise, and it will save you an hour before Christmas: if a `TypeError` mentions `NoneType`, a function you called forgot to `return` something.**
>
> And notice how sneaky this is. The number was *on the screen.* If you were only glancing, you'd swear the function worked."

Fix it — one word:

```python
    return total / 12          # RETURN, not print
```

Run it again with the same twelve numbers. The last line:

```text
Average : 75.00
```

> "Same number. Same twelve scores as Week 7. Same 75. **But now it's in a box with a name on it**, so I can format it, add to it, save it, or compare it. Which is the difference between a program that reports a number and a program that *uses* one."

**Ask this, before moving on:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Both my mistakes were silent-ish. Which was worse?" | The `print`-instead-of-`return` one, because the right answer was on the screen. | Accept either with an argument. What matters is noticing the answer being visible made it *harder*, not easier. |
| "What does `NoneType` in a `TypeError` almost always mean?" | A function forgot to return. | Have them write this in the Bug Log as a rule, not an entry. |
| "If you write a `def` and get less output than you expected, what's the first question?" | Did you call it? | This is the single most useful reflex of the week. |

---

### 🎲 Their Turn — Ten Repairs, Timed (20 minutes)

Full instructions in the next section. In the lesson flow:

- **Minutes 0–12:** the ten-program repair round, timed, Bug Log open, no help.
- **Minutes 12–16:** sort every Bug Log entry into one of the three families.
- **Minutes 16–20:** write the revision list. **Weeks, not marks.**

---

### 🔑 Wrap & Assign (9 minutes)

**Do this:** laptops shut. The Bug Log open. The **Weeks to revisit** sheet on the table where they can see it.

**Say this:**

> "Two minutes on the Bug Log, and this week one of your entries has to be a **function** bug — either the one where you defined it and never called it, or the `NoneType` one. Both of those were silent, and silent entries are the ones worth having.
>
> Then look at your revision sheet, and I want to say something about it before you put it away. **There is no number on that page and there is not going to be.** A number would tell you less than what is already written there. 'Seven out of ten' does not tell you what to do on Saturday. 'I missed all three of the silent ones' does."

Give them the two minutes. Then the three checks from **✅ Assessing Understanding** below, word for word — and note that all three are spoken, because this week's target is what they can *say*, not what they can type.

Then the homework, using the script in **📤 Homework to Assign**:

> "The big one is page 9.4 — three repeated blocks from your own weeks 1 to 8 files, each turned into a function, and the output has to come out **identical**. Not nearly. Identical, and you have to prove it.
>
> And one habit to take away, which is the last one of the term and it makes all the others usable. **Before you look for a bug, name the family from the message alone.** Never started, started-then-stopped, or finished-and-lied. That one decision tells you whether to look at a character, at a line number, or at a count."

**Ask this, as they pack up:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "One sentence: why is copying a block worse than naming it?" | Because you cannot check that the copies are identical. | If they say "it's longer" — accept, then ask them to prove their three banners match. |
| "What is the first question when a `def` produces no output?" | Did you call it? | The last thing they hear today should be this. |
| "Which family would you rather hand in?" | Family one — it never ran, so it cannot have told anyone anything untrue. | Any answer with a *reason* is fine. The reason is the assessment. |

---

## 🎲 The Activity, In Full

### Setup

**On the table:** the ten broken programs — either as ten files `bug01.py` … `bug10.py` or as ten printed slips · the Bug Log, open · workbook page 9.3 (the repair table) · page 9.5 (the reflection sheet) · **the blank sheet headed "Weeks to revisit"** · a pencil · a timer.

**On the screen:** their own newly-shortened file, working, with the function in it. Leave it there — it is the thing they will look at when the repair round gets frustrating.

### Part 1 — The repair round, timed (12 minutes)

**Say this first, and say all of it. This framing is not optional:**

> "Ten programs. Every one of them is broken and every one of them comes from something you have already learnt — weeks one to eight, nothing new. Twelve minutes, which is about seventy seconds each.
>
> Three rules.
>
> **One:** for each one, write down three things — **which family** it's in, **what's wrong** in one sentence, and **the fix.**
>
> **Two:** if you're stuck for more than ninety seconds, write down which week it came from and **move on.** Getting stuck is information. It's the most useful information in this lesson.
>
> **Three, and this is the important one: this is not a test and I am not going to give you a mark.** What we're making at the end is a list of weeks to go back to. If you get four of these and we find out exactly which four things you need, that is a *better* outcome than getting nine and learning nothing. **Do not try to look good. Try to find out.**"

Start the timer. **Then be quiet.** Your job for twelve minutes is to hand over slips and say almost nothing. If they ask, answer with a question from the list at the end of the Clinic.

The ten programs, their real messages, and their fixes are in the Answer Key (page 9.3). Here they are as a marking grid so you can see the coverage at a glance:

| # | From | Family | What it is |
|---|---|---|---|
| 1 | Week 1 | never started | `SyntaxError: unterminated string literal` — a missing closing quote |
| 2 | Week 1 | started, stopped | `NameError` — a bare word Python has never heard of |
| 3 | Week 2 | started, stopped | `TypeError` — text plus a number |
| 4 | Week 3 | **finished and lied** | a missing `f` — it printed the braces |
| 5 | Week 4 | started, stopped | `ValueError` — `int()` on something that is not a number |
| 6 | Week 5 | never started | `SyntaxError` — `=` where `==` was meant |
| 7 | Week 5 | never started | `IndentationError` — an `if` with no indented body |
| 8 | Week 6 | **finished and lied** | the ordering bug — a 95 gets a C |
| 9 | Week 7 | **finished and lied** | off-by-one — nine numbers where ten were wanted |
| 10 | Week 8 | started, stopped | infinite loop, `KeyboardInterrupt` — no change step |

**Three of the ten have no error message at all.** That is deliberate and it is the proportion that matters: if a student gets seven of the seven noisy ones and none of the three silent ones, you have learnt something very specific about what to teach next.

### Part 2 — Sort the Bug Log into families (4 minutes)

**Say this:**

> "Bug Log, page one. Every entry. Put a 1, a 2 or a 3 next to it — never started, started then stopped, or finished and lied. Do them all, fast, and then count the threes."

This takes three minutes for a term's worth of entries and it produces two numbers worth having:

- **The total number of entries.** A student with fifteen has been logging honestly. A student with three has not been logging, and that goes on the revision list as a habit rather than a topic.
- **How many are family three.** Silent bugs are the ones that will hurt them in the capstone, and knowing their own count changes how carefully they test.

Then one question:

> "Look at your family threes. Is there a week they cluster in?"

Weeks 6 and 7 usually. That is not a coincidence — `elif` chains and `range` boundaries are where silence lives.

### Part 3 — The revision list (4 minutes)

**This is the product of the lesson.** Hand them the blank sheet.

**Say this:**

> "No marks. A list. Three columns: **which week**, **what specifically**, and **how you'll know you've fixed it.** That third column is the one that makes this useful — 'revise Week 6' is a wish, 'write a four-branch chain and test both sides of every boundary' is a plan."

A realistic, good example of a completed sheet:

| Week | What specifically | How I'll know I've got it |
|---|---|---|
| 3 | I keep forgetting the `f` before the quote, so my braces print | Write five f-strings from memory with no example in front of me; check all five print values, not braces |
| 6 | I got the ordering bug wrong again in bug 8 — I looked at the `>= 90` line instead of the order | Write a five-branch chain from scratch and test 95, 80, 62, 50, 20; say which two tests prove the fix |
| 7 | Off-by-one. I said `range(1, 10)` gives ten numbers | Say out loud how many values every `range` I write hands out, for a week, before running it |
| — | My Bug Log only has six entries for eight weeks | One entry every single time something breaks, even if the fix took ten seconds |

**Notice the last row has no week in it.** A habit is a legitimate finding and it belongs on the list.

> **🧑‍🏫 If a student asks "so how did I do?"** — answer honestly and specifically, and do not give a number. Something like: *"You got seven of the ten, and the three you missed were all the silent ones, which tells us exactly what to work on. You're solid on reading tracebacks and you're not yet in the habit of checking output that looks plausible. That's a very normal place to be in week nine and it's completely fixable."* **A number would tell them less than that sentence does.**

### What "finished" looks like

- One of their own files has a repeated block replaced by a function, and the output is provably unchanged (`diff` silent, or the two outputs read aloud in unison).
- The student can state the difference between defining and calling, and can say what a function with no `return` hands back.
- At least seven of the ten repairs are diagnosed with a family, a sentence and a fix. **Ten is not the target; honest diagnosis is.**
- Every Bug Log entry is labelled 1, 2 or 3, and the number of 3s is written down.
- The **Weeks to revisit** sheet has at least two rows with a specific "how I'll know" for each.
- **Two new Bug Log entries**, at least one of them a function bug — the uncalled function or the `NoneType` `TypeError`.

### Variation — easier

- **Six programs instead of ten.** Use 1, 2, 3, 5, 7 and 9. That keeps one from each family and drops the fiddliest ones.
- **Tell them the family before they start** on each slip. Diagnosing *within* a known family is much easier and still valuable.
- **Do the repairs on paper**, with no running. Reading a traceback and saying the fix out loud is the skill; typing it is not.
- **Extract the function together rather than having them do it.** You type, they say the steps. Objective 3 still lands.
- **Skip `return` entirely.** `def` and the call is a complete lesson, and Week 10 opens with `return` anyway. If you do this, say so on the revision sheet so it does not get lost.
- **No timer.** For a student who freezes at timed anything, the timer subtracts more than it adds. The twelve minutes is a budget for you, not a pressure for them.

### Variation — harder

None of these need syntax they have not met.

1. **Three functions, not one.** Extract the banner, the divider and the goodbye block. Then have one function call another:

   ```python
   # three_functions.py - three blocks that were pasted more than once, each given a name.

   def print_banner():                      # was at the top of about_me.py AND grade.py
       print("=" * 34)
       print("   AI ACADEMY  -  LEVEL 2")
       print("=" * 34)

   def print_divider():                     # was between every section of every report
       print("-" * 34)

   def print_goodbye():                     # was at the bottom of guess.py AND grade.py
       print_divider()                      # a function may call another function
       print("  Thanks for using this program.")
       print("=" * 34)

   print_banner()
   print("Name  : Ramana")
   print("Class : 7")
   print_divider()
   print("Total   : 900")
   print("Average : 75.00")
   print_goodbye()
   ```

   The real output:

   ```text
   ==================================
      AI ACADEMY  -  LEVEL 2
   ==================================
   Name  : Ramana
   Class : 7
   ----------------------------------
   Total   : 900
   Average : 75.00
   ----------------------------------
     Thanks for using this program.
   ==================================
   ```

   **The interesting line is `print_divider()` inside `print_goodbye()`.** A function calling another function is not a new rule — it is just a call, in a place that happens to be inside a `def`. Ask them what would happen if `print_goodbye` called *itself*. (It would never stop. It is next term's rabbit hole and it has a name: recursion. Do not go in today.)

2. **Return the accumulator.** Rewrite Week 7's `scores.py` so the totalling lives inside a function that returns the average, as in section 4. Then the question that matters: *"the function reads twelve scores from the keyboard. Is that a good design?"* The honest answer is **no** — a function that both fetches data *and* computes is hard to test, because you cannot check it without typing twelve numbers. Separating them needs parameters, which is next week. **A student who feels that itch is ready for Week 10.**

3. **The silent-bug hunt, reversed.** Have them break a working program on purpose in a way that produces **no error message**, hand it to you, and time how long you take to find it. Three attempts. Being the one who plants the bug is a completely different relationship to the material.

4. **A function with two `return`s.** A grade function with a `return` in every branch of an `if`/`elif` chain — no parameters, so read the mark from `input()` inside it. Then notice that `return` ends the function immediately, which means you do not even need the `elif`s. **Both styles are correct** and seeing why is a genuinely satisfying five minutes.

5. **Count the savings honestly.** `report_long.py` is 25 lines and `report_short.py` is 18 — a saving of 7. Ask: *"how many headers would there have to be before the function version saved fifty lines?"* Each extra header costs 5 lines pasted versus 1 line called, so a net 4 lines saved per extra header. To save 50 you would need fourteen headers (4 × 14 − 6 = 50; the definition costs 6 lines up front). **Then the real question: if the saving is only 7 lines here, was it worth doing?** The answer is yes, and the reason has nothing to do with lines.

---

## 🐞 The Debugging Clinic

Every message below came from running a real broken version of this week's code. Only the folder path in the `File` line will differ on your machine.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| **No output at all, and no error** | Python read the file, learnt the recipe, and reached the end with nothing to do. | **A function defined but never called.** | Add `name()` at the margin. **First question every time: did you call it?** |
| **No output at all, and no error** (again) | Same silence, different cause. | `print_header` written **without brackets** — that names the function instead of running it. | `print_header()`. The brackets mean "do it". |
| `SyntaxError: expected ':'` with `^` after `def print_header()` | "I read the whole line and found no colon." | The colon is missing after the brackets. | Add the `:`. Same rule as `if` and `for`. |
| `SyntaxError: invalid syntax` with `^` under the colon in `def print_header:` | "A `def` needs brackets before its colon." | The empty `()` was left out. | `def print_header():` — the brackets are required even when there is nothing in them. |
| `IndentationError: expected an indented block after function definition on line 1` | "You told me a block was coming and then gave me nothing." | The body is at the margin instead of indented. | Indent the body four spaces. Note that Python names the construct: *function definition*. |
| `NameError: name 'print_header' is not defined` | "I have never heard of that name." | The call is **above** the `def`. Python reads top to bottom and cannot call a recipe it has not read yet. | Move the `def` above the call, or move the call below the `def`. **Definitions first, calls after.** |
| `TypeError: print_header() takes 0 positional arguments but 1 was given` | "You handed something to a function that has nowhere to put it." | `print_header(34)` on a function defined as `def print_header():`. | Either call it with empty brackets, or give it a parameter — **which is next week.** |
| `SyntaxError: 'return' outside function` with `^^^^^^^^^^^^` under the line | "There is no function here for me to return from." | A `return` at the margin, outside any `def`. | Move it inside the function, or use `print` if you are at the top level. |
| `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | "You tried to add 25 to nothing." | A function that **prints** instead of **returns**, so the caller received `None`. | Change `print(x)` to `return x` inside the function. **`NoneType` in a `TypeError` nearly always means a missing `return`.** |
| `TypeError: unsupported format string passed to NoneType.__format__` | "You asked me to show *nothing* to two decimal places." | Same cause as the row above, met through an f-string's `:.2f`. | `return`, not `print`. **The word `NoneType` is the clue, wherever it appears.** |
| **No error, and a line inside the function never runs** | Python is perfectly happy. | A line placed **after** a `return`. `return` ends the function immediately. | Move the line above the `return`, or delete it. |
| **No error, and the output changed slightly after the extraction** | Python is perfectly happy. | The block was **retyped** instead of copied — an extra space, or 34 equals signs instead of 40. | `diff` the before-and-after output. Then copy, do not retype. |
| **No error, and the function runs but nothing appears** | Python is perfectly happy. | The function `return`s a value and the caller never printed it. | `print(name())`, or store it and print it. **Returning is not showing.** |

### How to teach debugging without giving the answer

By Week 9 the six habits are established: **hands off the keyboard · last line first · ask, do not tell · log it · count, do not read · Ctrl+C first, think second.** This week adds the last one of Term 1, and it is the one that makes the other six usable.

**7. Name the family before you look for the bug.**

Before reading a single line of the program, read the *message* and say which of the three families it is in. That one decision narrows everything:

- **Never started?** Then no output on the screen means anything, and the `^` is pointing at the exact character. Look *at that character*, not at the logic.
- **Started, then stopped?** Then there is a line number and it is trustworthy. Go to that line. And read the message's nouns — `str`, `int`, `NoneType` — because they tell you what kind of thing surprised Python.
- **Finished and lied?** Then reading will not help you, because every line is legal. **Count something.** Compare it with a hand-worked answer. Predict and check.

Teaching this during the repair round takes three questions and nothing else:

1. *"Which family?"* — from the message alone, before looking at the code.
2. *"What's the last line of the message, word for word?"*
3. *"What did you expect, and what did you get?"* — the only question that works on family three.

And one thing to resist: **do not confirm a correct diagnosis immediately.** Ask "how would you prove it?" first. In family three, being sure without proof is exactly the habit that caused the bug.

---

## ❓ Questions Students Ask This Week

**"Why do I need a function? Copy and paste works."**

It does work, and it keeps working right up until the day you change your mind. Then you have three copies and you have to change all three, and nothing on earth will tell you that you missed one. But the deeper answer is the one from the Hook: **you cannot check that three copies are identical.** You can look at them, and they will look the same, and one of them will have thirty-four equals signs where the others have forty. With a function there is one copy, so the question cannot be asked. **Functions do not save typing so much as they remove a thing you would otherwise have to remember.**

**"Can I have a function that both prints and returns?"**

Yes, and it is legal, and it is usually a sign of a fuzzy plan. The clean version is: functions work things out and hand them back; the main part of the program decides what a human sees. That way you can use the function's answer in a calculation without a stray line of text appearing in the middle of your report. There is one honest exception — a function whose *whole job* is displaying something, like `print_header`, has nothing to return and should just print. **The test is: could I use this function twice, once to show something and once to work something out? If yes, split it.**

**"What's the difference between `print_header` and `print_header()`?"**

`print_header` is the name. `print_header()` is the instruction to run it. Writing the name on its own is legal, does nothing, and produces no error — which makes it one of the most quietly annoying mistakes in Python. You met exactly this last week with `.isdigit` versus `.isdigit()`, and it is the same rule in both places: **brackets mean "actually do it".**

**"How long should a function be?"**

There is no rule, but there is a good test: **can you say what it does in one short sentence with no "and" in it?** "Prints the report banner" — good. "Reads twelve scores and totals them and works out the average and prints the report" — that is four functions wearing one coat. Professionals argue endlessly about numbers (ten lines? twenty? one screen?) and the argument never resolves, because a straightforward twenty-line function is easier to read than a clever five-line one. Use the sentence test.

**"Should every repeated block become a function?"** *(Nobody fully agrees, and here is why.)*

This is a genuinely live argument among working programmers and it has slogans on both sides. One camp says **never write the same thing twice** — every duplication is a future inconsistency, so extract it the first time you copy it. The other camp says **wait until the third time**, because two similar-looking blocks quite often turn out to be two different ideas that happen to look alike today, and if you merge them early you end up with one function that has to serve two masters and grows flags and options to cope. That is arguably worse than the duplication was.

There is no settled answer, and the honest reason is that it depends on something you cannot know yet: whether those two blocks will change *together* or *separately* in future. **The rule of thumb this course uses: two copies, notice it; three copies, extract it.** And the rule that everyone agrees on: **if you have already changed the same thing in two places on the same day, extract it now.**

**"Can a function call another function?"**

Yes, and it is completely ordinary — `print_goodbye()` calling `print_divider()` is just a call that happens to sit inside a `def`. There is no special rule and no limit. The one thing to know: a function cannot be called before it has been defined, so if `print_goodbye` uses `print_divider`, then by the time `print_goodbye` is actually *called*, `print_divider` must already exist. In practice that means put all your `def`s together at the top and your calls below them, and it never comes up.

**"Can a function call itself?"**

It can, and it has a name — recursion — and it is genuinely one of the most beautiful ideas in programming. It is also a very good way to make a program run forever, which is why it is not today's lesson. If you try it now with no way to stop, you will get a wall of red ending in `RecursionError`, which is Python's version of Ctrl+C for a function that will not stop calling itself. **Write the question down.**

**"Why does Python need `def` at all? Couldn't it work out which lines belong together?"**

No, and the reason is the same as always: it would have to guess your intention. Look at any five consecutive lines in your program — there is nothing in them that says whether they are a group with a purpose or five unrelated things that happen to be next to each other. **`def` is you telling Python something it has no way to know: that these lines are one idea, and that the idea has a name.** That is why naming the function well matters more than almost anything else about it. The name is the only place where your intention is written down.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The repair round turns into a mark, and the student is deflated | Ten questions with right answers looks exactly like a test | **Say the framing before you start the timer, out loud, in full:** "this is not a test, and getting four and finding out exactly which four is better than getting nine and learning nothing." Then never state a total. |
| You substitute your own example files for theirs | Their folder is messy and yours is tidy | Do not. The whole force of the Hook is that it is *their* code in *their* three files. If the files are genuinely gone, retype one together — that is a better lesson than a stand-in. |
| The extraction is done by retyping, and the output changes | Retyping five lines introduces a typo | `diff` catches it. Say why copying matters: "if we retype and the output changes, we don't know whether it was the function or the typing." |
| The `def` goes below the call | Programs are usually written in the order things happen | `NameError: name 'print_header' is not defined`. Ask: "when Python read that line, had it read the recipe yet?" |
| The function is defined and never called, and they conclude functions do not work | The file is longer and the output is shorter, with no error | This is Deliberate Mistake #1 for exactly this reason. Ask "how many times did you tell Python to run it?" |
| `return` is used and nothing appears, so a `print` is added inside as well | Returning does not show anything, which feels broken | It now works and hides the confusion until Week 10. Ask them to delete the print and print the *returned* value instead. Then show `None`. |
| The `NoneType` `TypeError` is treated as a mystery | The right answer was visible on the screen just above it | Read the word `NoneType` out loud and ask what it means. Then have them write the rule — not the entry — in the Bug Log. |
| Twelve minutes of repairs becomes thirty | One program is genuinely interesting and you both get involved | Keep the timer and the ninety-second rule. **Being stuck is the finding.** Interesting programs can be finished at home. |
| The revision list says "revise everything" or "revise Week 6" | Vague is easier than specific, and specific feels like admitting something | Insist on the third column. "How will you know you've got it?" turns a wish into a plan, and it is the only column that will still be useful in March. |
| Parameters get taught because a student asks | It is the obvious next question and you know the answer | Answer in one sentence — "that's next week, and it's one line of new syntax" — and have them write the question down. Two new ideas in a checkpoint week is one too many. |
| The Bug Log turns out to be nearly empty and the sorting exercise collapses | The habit did not stick | Say it plainly and put it on the revision list as a *habit*. Then build ten entries now from the ten repair programs. The habit can start this week. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut, in this order:** `return` entirely · four of the ten repair programs · the Bug Log sorting · the third column of the revision list.

**What you must not cut:** the Hook, and one function extracted from one of their own files. Those two deliver objectives 3 and 5, and neither needs `return` or the timer.

**Reteach `def` physically — the recipe card.** Four minutes, works on essentially everybody.

Write the five banner lines on an index card. Write `print_header` on the back, big.

> "This card is the function. The back is its name; the front is what it does."

Put the card face down on the table, name up.

> "That's what `def` does. The card exists. It's on the table. **Has anything been printed?**"

(No.)

> "Nothing. Now — every time I say the name on that card, you turn it over and read the five lines out loud. `print_header`."

They read it. Say the name again. They read it again. Three times.

> "Three readings. **One card.** Now: I want the heading to say LEVEL 2. How many cards do you have to change?"

(One.)

Then lay three separate cards with the same five lines written out longhand, and ask the same question. Three. And then the killer:

> "Are those three cards identical? Check. Character by character."

Write one of them with a different number of equals signs on purpose. Let them find it. **That is the lesson, and it happened with card and pencil.**

**The copy-this-exactly scaffold.** Complete, working, and short:

```python
# report.py - type this exactly. One function, defined once, called three times.

def print_header():                      # DEFINE - nothing runs yet
    print("=" * 30)                      # everything indented belongs to the function
    print("   MY REPORT")
    print("=" * 30)

print_header()                           # CALL - now the block runs
print("Total   : 900")

print_header()                           # CALL it again
print("Average : 75.00")

print_header()                           # and again
```

Real output:

```text
==============================
   MY REPORT
==============================
Total   : 900
==============================
   MY REPORT
==============================
Average : 75.00
==============================
   MY REPORT
==============================
```

Then two experiments, in this order: **delete one call** and run it (one fewer banner, no error). **Delete the brackets from a call** and run it (that banner vanishes, no error). Two silent failures, both understood, in ninety seconds.

**Reduce the writing.** For the repair round, a diagnosis of `family 2 — no int() — add int()` is full credit. Sentences are not the skill this week.

### If the student is flying

1. **Three functions, and one calling another** (Variation — harder, item 1). Then the question about a function calling itself, and why you are not doing it today.
2. **Return the accumulator** (item 2), and the honest design question: is a function that reads from the keyboard *and* computes a good function? (No, and fixing it needs next week.)
3. **The reversed silent-bug hunt** (item 3). They break a program silently and time you finding it.
4. **A function with a `return` in every branch** (item 4), and the discovery that `return` makes the `elif`s unnecessary.
5. **Count the savings honestly** (item 5) — 25 lines to 18 — and then argue about whether seven lines was worth it. **The answer is yes and the reason is not lines**, and getting them to that answer themselves is the best five minutes available this week.
6. **The naming question, which is deeper than it looks.** Give them a function called `do_stuff()` that prints a banner, and ask them to rename it. Then ask: *"which is easier to fix — a program with badly named functions, or a program with no functions at all?"* There is a real argument on both sides: a misleading name actively lies to you, whereas duplicated code merely repeats itself. **A wrong name is worse than no name.** That is why `print_header` beats `ph` beats `do_stuff`, and it is worth a genuine two minutes.

### If the student won't engage today

Do the Hook — it is their own code and it usually lands even on a bad day — and then play **Name That Family**, which needs no computer.

Read them the last line of a traceback, out loud, with no code and no context. They say 1, 2 or 3. Score a point each. Twenty of them, fast, in three minutes. Use the ones from their own Bug Log first, then these:

| You read out | They say |
|---|---|
| `SyntaxError: expected ':'` | 1 |
| `NameError: name 'total' is not defined` | 2 |
| `TypeError: can only concatenate str (not "int") to str` | 2 |
| `IndentationError: unindent does not match any outer indentation level` | 1 |
| `ValueError: invalid literal for int() with base 10: 'banana'` | 2 |
| "It printed a C for a mark of 95 and no message at all" | 3 |
| `KeyboardInterrupt` | 2 |
| "It printed nine numbers when I wanted ten" | 3 |
| `ZeroDivisionError: division by zero` | 2 |
| `SyntaxError: unterminated string literal` | 1 |
| "It printed `{total}` with the curly brackets still there" | 3 |
| `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | 2 |

Then swap: **they** read one out and **you** answer, and you get some wrong on purpose so they have to correct you.

Finish with one question, which is the whole checkpoint in a sentence:

> *"Of the three families, which one would you rather have in a program you were about to hand in, and why?"*

The answer — family one, because it cannot possibly have told anyone anything untrue — **is the whole of Term 1's debugging education**, and it arrived without a laptop.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — define versus call (spoken)**

> "I write a `def` with five perfect lines inside it, save the file, and run it. Nothing appears on the screen and there is no error. What have I forgotten, and how do I know it isn't a bug in the function?"

*Good answer:* the call — `name()` at the margin. It is not a bug in the function because defining a function never runs it; Python filed the recipe and reached the end of the file. **What to catch:** "the function is broken." Ask how many times they told Python to run it.

**Check 2 — `return` versus `print` (spoken)**

> "One function prints 75 and one returns 75. I store each result in a box and print the box. What do the two boxes hold?"

*Good answer:* the returning one holds 75; the printing one holds `None`, because a function with no `return` hands back nothing. **What to catch:** "both hold 75." Show the four-line output of `show_vs_give.py` and put a finger on `None`.

**Check 3 — family from the message alone (spoken)**

> "I'm going to read you the last line of a traceback and you tell me which of the three families it's in, and what you'd do first. Ready? `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`."

*Good answer:* family two — it started, then stopped — so there is a trustworthy line number; go to that line. And `NoneType` means a function I called forgot to `return`. **What to catch:** any hesitation about the family. The family should be instant, from the presence of the word `Traceback` and a line number, before any thinking about the cause.

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Thinks defining a function runs it. Cannot repair a `SyntaxError` from its message. Cannot say what a traceback's line number is for. Produces "revise everything" as a revision plan. |
| **2 — Emerging** | Writes a `def` and a call when the shape is dictated. Repairs the noisy errors and none of the silent ones. Sorts a traceback into a family with prompting. |
| **3 — Secure** | Extracts a repeated block into a function unaided and **proves the output is unchanged.** States the define/call difference correctly. Uses `return` and knows a function without one hands back nothing. Repairs at least seven of ten, including one silent bug. Writes a revision list naming specific weeks. **This is the target.** |
| **4 — Strong** | Names the family from the message alone, instantly, before looking at the code. Recognises `NoneType` in a `TypeError` as a missing `return`. Diagnoses the uncalled function and the missing brackets, both silent. Writes a revision list with a "how I'll know" column that is genuinely testable. |
| **5 — Exceptional** | Argues the two-copies-versus-three-copies question with a reason on each side. Sees that the real cost of duplication is being unable to *check* it, not the length. Notices that a function reading from the keyboard is hard to test and asks for parameters before being taught them. Says why Python cannot work out for itself which lines belong together. |

---

## 📤 Homework to Assign

**Say this:**

> "About an hour, and it is more looking-back than usual because that is what a checkpoint is for.
>
> **Page 9.1 — name the family, laptop closed.** Twelve error messages, no code. For each one write 1, 2 or 3, and what you would do first. **You should be able to do this without any code in front of you at all** — that is the point of the exercise.
>
> **Pages 9.2 and 9.3 — functions, and the ten repairs.** Page 9.2 asks you about `def`, calling and `return`. Page 9.3 is the ten programs from class — the ones you didn't finish, finished properly, with the family, the diagnosis and the fix for each.
>
> **Page 9.4 — the big one. Three repeated blocks, three functions.** Go through your weeks 1 to 8 files and find **three** blocks that appear more than once. Turn each one into a function. And here is the requirement I'm marking hardest: **the output has to be byte-identical to what it was before.** Not nearly. Identical. Save the output before and after and compare them — if you can use `diff`, use it; if not, read the two side by side and check every line.
>
> **Page 9.5 — the Term 1 reflection sheet, and the revision list.** Weeks, what specifically, and how you'll know you've got it. **No marks anywhere on that page.** If I see a score I'll cross it out.
>
> **Page 9.6 — Bug Log, Think Deeper, self-check.** Two Bug Log entries, at least one of them a function bug — the one where you forgot to call it, or the `NoneType` one. And go back and label **every** entry in the log 1, 2 or 3, then count your 3s and write the number at the top.
>
> Every line commented, saying *why*."

**Workbook pages:** 9.1 in class if there is time; **9.2, 9.3, 9.4, 9.5 and 9.6** at home.

**Expected time:** 5 min naming families · 10 min the function questions · 15 min finishing the repairs · 15 min the three extractions and the diff · 10 min the reflection sheet · 5 min Bug Log. About 60 minutes.

---

## 🔑 Answer Key

### Page 9.1 — Warm-Up: name the family from the message alone

| # | The message | Family | What you would do first |
|---|---|---|---|
| a | `SyntaxError: expected ':'` | **1 — never started** | Look at the `^`. It points at the exact character where the colon should be. Nothing ran, so no output on screen means anything. |
| b | `NameError: name 'total' is not defined` | **2 — started, then stopped** | Go to the line number. Either the name is misspelled, or the box was never made — and if it is `total`, it is probably an accumulator with no set-up line. |
| c | `IndentationError: expected an indented block after 'for' statement on line 4` | **1 — never started** | Indent the line under the `for`. Python has even told you which construct you failed to fill in. |
| d | `TypeError: can only concatenate str (not "int") to str` | **2** | Go to the line number and find the `+`. One side is text and one is a number. |
| e | `ValueError: invalid literal for int() with base 10: 'banana'` | **2** | Find the `int(...)`. The value handed to it was not a number. Check before converting. |
| f | "It printed `{total}` with the curly brackets still showing" | **3 — finished and lied** | Look for a missing `f` before the opening quote. No message will ever appear for this. |
| g | `KeyboardInterrupt` | **2** | Nothing is wrong with the line it names — that is just where you stopped it. Find the variable in the loop's condition and ask what was supposed to change it. |
| h | "A mark of 95 came out as a C, no error" | **3** | Count and compare. Trace one value through the chain with a finger. The order of the branches is wrong. |
| i | `ZeroDivisionError: division by zero` | **2** | Go to the line and ask what the divisor was. Often a count that turned out to be 0 — a loop that ran no passes. |
| j | "It asked for eleven scores when I had twelve" | **3** | Count what went in against what came out. Then look at the `range` boundary. |
| k | `SyntaxError: 'break' outside loop` | **1** | Find the `break` and put it inside a loop, or delete it. An `if` is not a loop. |
| l | `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'` | **2** | The word `NoneType` is the clue: a function you called printed instead of returning. |

**9.1(m) Which family is the friendliest, and why?**
Family one. You find out instantly, and nothing has happened yet — no file was written, no number was reported, nobody was told anything untrue. It is the cheapest possible kind of mistake.

**9.1(n) Which family is the most expensive, and why?**
Family three. It survives, because nothing announces it. It goes into your homework, into the answers your program printed, into next term. The Week 6 grade chain would have handed thirty students a wrong grade and nobody would ever have found out.

**9.1(o) Which family gives you the most help, and what is the help?**
Family two. It gives you a **line number** you can trust, and the nouns in the message (`str`, `int`, `NoneType`) tell you what kind of thing surprised Python.

### Page 9.2 — Practice Set A: understand it

**9.2(a) What is a function?**
A named block of code you write once and run whenever you like.

**9.2(b) What is the difference between defining and calling?**
Defining (`def name():`) writes the block down under a name and **runs nothing.** Calling (`name()`) runs the block, top to bottom. You define once; you call as often as you like.

**9.2(c) I define a function and never call it. What happens?**
Nothing at all. No output, no error, and the program exits normally. Python read the recipe, filed it, and reached the end of the file with nothing to do.

**9.2(d) What is the difference between `print_header` and `print_header()`?**
`print_header` is the function's **name** — a reference to the recipe. `print_header()` is an instruction to **run** it. Writing the name on its own is legal, does nothing, and produces no error. **The brackets mean "actually do it"** — exactly like `.isdigit()` versus `.isdigit` in Week 8.

**9.2(e) What punctuation does `def` need, and where have you seen those rules before?**
Empty brackets and a colon on the `def` line, then an indented block. Both rules are the same as `if` and `for`: the colon means "the indented block below belongs to me", and the indent *is* the block. **There is no new punctuation this week.**

**9.2(f) What does `return` do?**
It immediately ends the function and hands one value back to the line that called it, so the program can store it, use it in a calculation, or print it.

**9.2(g) What does a function with no `return` hand back?**
`None` — Python's word for "no value at all". Printing it shows the word `None`.

**9.2(h) Why can you not do maths with a printed answer?**
Because printing sends the characters to the screen and keeps nothing. There is nothing left to add to. You can always print a returned value; you can never recover a printed one.

**9.2(i) What does `NoneType` in a `TypeError` almost always mean?**
That a function you called **printed** instead of **returning**, so the value you are working with is `None`.

**9.2(j) What happens to a line placed after a `return`?**
It never runs. `return` ends the function immediately. There is no error and no warning.

**9.2(k) Why does calling a function above its `def` fail?**
Because Python reads the file from top to bottom, and at the moment it reaches the call it has not read the definition yet, so the name does not exist. The message is `NameError: name 'print_header' is not defined`. **Definitions first, calls after.**

**9.2(l) Name the three families of trouble and the one-line tell for each.**
**1, it never started:** no output at all, and a `^` under one spot. **2, it started then stopped:** some output, then `Traceback`, a line number and a message. **3, it finished and lied:** no message anywhere, and a confident wrong answer.

### Page 9.3 — Build It: the ten repairs

Every message below came from a real run.

---

**Bug 1 — from Week 1.**

```python
print("Hello, world!)
```

*The real message:*

```text
  File "/Users/you/ai-academy/level2/bug01.py", line 1
    print("Hello, world!)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

**Family 1 — it never started.** The closing quote is missing, so as far as Python is concerned the text never ends. The `^` points at the quote that opened it. **Fix:** `print("Hello, world!")`.

---

**Bug 2 — from Week 1.**

```python
print(Hello)
```

*The real message:*

```text
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/bug02.py", line 1, in <module>
    print(Hello)
NameError: name 'Hello' is not defined
```

**Family 2 — it started, then stopped.** Without quotes, `Hello` is a *name*, and Python has never heard of it. **Fix:** `print("Hello")`. The quotes are what turn a name into text.

---

**Bug 3 — from Week 2.**

```python
age = "12"
print(age + 1)
```

*The real message:*

```text
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/bug03.py", line 2, in <module>
    print(age + 1)
TypeError: can only concatenate str (not "int") to str
```

**Family 2.** `age` holds the *text* `"12"`, not the number 12, and `+` cannot glue a number onto text. **Fix:** either `age = 12` (a number), or `print(int(age) + 1)`. Note that `"12" + "1"` would also "work" and give `121`, which would be family three.

---

**Bug 4 — from Week 3.**

```python
total = 900
print("The total is {total}")
```

*Real output:*

```text
The total is {total}
```

**Family 3 — it finished and lied.** No error at all. The `f` is missing before the opening quote, so the braces are just characters. **Fix:** `print(f"The total is {total}")`. **Tell:** curly brackets in the output.

---

**Bug 5 — from Week 4.**

```python
age = int(input("How old are you? "))
print(age)
```
…and the user types `twelve`.

*The real message:*

```text
How old are you? twelve
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/bug05.py", line 1, in <module>
    age = int(input("How old are you? "))
ValueError: invalid literal for int() with base 10: 'twelve'
```

**Family 2.** `int()` can only convert text that *looks like* a number. **Fix (Week 8's tool):** keep it as text, `.strip()`, check `.isdigit()`, and convert only after the check passes.

---

**Bug 6 — from Week 5.**

```python
score = 90
if score = 90:
    print("Full marks")
```

*The real message:*

```text
  File "/Users/you/ai-academy/level2/bug06.py", line 2
    if score = 90:
       ^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Family 1.** One `=` means "put this in the box"; two `==` means "are these equal?" **Fix:** `if score == 90:`. **Notice Python guessed correctly and told you** — read the whole message, not just the first three words.

---

**Bug 7 — from Week 5.**

```python
score = 90
if score >= 50:
print("Pass")
```

*The real message:*

```text
  File "/Users/you/ai-academy/level2/bug07.py", line 3
    print("Pass")
    ^
IndentationError: expected an indented block after 'if' statement on line 2
```

**Family 1.** The `if` promised an indented block and did not get one. **Fix:** indent `print("Pass")` four spaces.

---

**Bug 8 — from Week 6.**

```python
mark = 95

if mark >= 60:
    grade = "C"
elif mark >= 75:
    grade = "B"
elif mark >= 90:
    grade = "A"
else:
    grade = "F"

print(f"Mark {mark} gets grade {grade}")
```

*Real output:*

```text
Mark 95 gets grade C
```

**Family 3.** No error whatsoever. The chain checks top to bottom and stops at the first `True`, and `95 >= 60` is `True`, so the A and B branches are unreachable — dead code. **Fix:** highest threshold first: 90, then 75, then 60. **Tell:** the answer is confidently wrong, and every individual line is a correct line. Reading will not find it; tracing a value with a finger will.

---

**Bug 9 — from Week 7.**

```python
# Goal: print the numbers 1 to 10.
for n in range(1, 10):
    print(n, end=" ")
print()
```

*Real output:*

```text
1 2 3 4 5 6 7 8 9 
```

**Family 3.** Nine numbers where ten were wanted. `range` stops *before* its second number. **Fix:** `range(1, 11)`. **Tell:** count the output against what you asked for. The only reason you can tell at all is that the goal was written in a comment.

---

**Bug 10 — from Week 8.**

```python
# Goal: count down from 3 and then say Liftoff.
countdown = 3

while countdown > 0:
    print(countdown)

print("Liftoff!")
```

*What happens:* it prints `3` forever — tens of thousands of lines a second. After Ctrl+C, the real message:

```text
3
3
3
^C
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/bug10.py", line 5, in <module>
    print(countdown)
KeyboardInterrupt
```

**Family 2**, but only because you interrupted it — left alone it never ends and never reports anything, which makes it the one bug that belongs to two families at once. **The missing part is the CHANGE step:** nothing in the body moves `countdown` towards 0. **Fix:** add `countdown -= 1` inside the loop. Then the output is `3 2 1 Liftoff!`.

---

**9.3(k) How many of the ten had no error message?**
**Three** — bugs 4, 8 and 9. All three printed a complete, confident, wrong answer.

**9.3(l) Which of the ten did you find fastest, and what does that tell you?**
Almost always one of the family-one errors, because the `^` points straight at the character. **What it tells you: the errors that feel worst are the easiest, and the ones that feel like nothing are the expensive ones.**

**9.3(m) Sort the ten by family and count each.**
Family 1: bugs 1, 6, 7 — **three**. Family 2: bugs 2, 3, 5, 10 — **four**. Family 3: bugs 4, 8, 9 — **three**.

### Page 9.4 — Build It: three repeated blocks, three functions

A model answer. Three blocks that genuinely repeat across weeks 1–8 — a banner, a divider, and a sign-off:

```python
# three_functions.py - three blocks that were pasted more than once, each given a name.

def print_banner():                      # was at the top of about_me.py AND grade.py
    print("=" * 34)
    print("   AI ACADEMY  -  LEVEL 2")
    print("=" * 34)

def print_divider():                     # was between every section of every report
    print("-" * 34)

def print_goodbye():                     # was at the bottom of guess.py AND grade.py
    print_divider()                      # a function may call another function
    print("  Thanks for using this program.")
    print("=" * 34)

print_banner()
print("Name  : Ramana")
print("Class : 7")
print_divider()
print("Total   : 900")
print("Average : 75.00")
print_goodbye()
```

The real output:

```text
==================================
   AI ACADEMY  -  LEVEL 2
==================================
Name  : Ramana
Class : 7
----------------------------------
Total   : 900
Average : 75.00
----------------------------------
  Thanks for using this program.
==================================
```

**How to mark it, in this order:**

1. **Is the output identical to the original?** This is the requirement. The proof:

   ```text
   $ python3 report_long.py > long.txt
   $ python3 report_short.py > short.txt
   $ diff long.txt short.txt
   $ 
   ```

   `diff` printing nothing means the two are identical. If it prints anything at all, the block was retyped rather than copied — usually a different number of equals signs, or a lost blank line.
2. **Are all three functions actually called?** A defined-and-never-called function produces no output and no error, so a missing banner is the tell.
3. **Are the `def`s above the calls?** If not, `NameError`.
4. **Do the names say what the functions do?** `print_banner` is good. `banner` is acceptable. `do_stuff` loses a mark and deserves a conversation.

**9.4(b) How many lines did you save, and was that the point?**
For the model answer, `report_long.py` is 25 lines and `report_short.py` is 18 — **seven lines.** And no, that was not the point. The point is that the heading is now written down in exactly one place, so changing it is one edit and it is **impossible to miss a copy, because there are none.** Seven lines is a nice side effect of a change that was really about certainty.

**9.4(c) Why must you copy the block rather than retype it?**
Because if you retype it and the output changes, you will not know whether the change came from the function or from your typing. Copying makes the extraction the only variable — which is exactly how you test one change at a time.

**9.4(d) What does `print_divider()` inside `print_goodbye()` show?**
That a function can call another function, and that there is no special rule for it — it is an ordinary call that happens to sit inside a `def`. The only requirement is that `print_divider` must exist by the time `print_goodbye` is actually called, which it does if all the `def`s are at the top.

**9.4(e) Rewrite Week 7's average as a function that returns.**

```python
# average_fn.py - a function that hands a number back.

def average_of_twelve():                   # DEFINE - no input, one answer out
    total = 0                              # week 7's accumulator, now living inside
    for i in range(1, 13):                 # 1, 2, 3 ... 12
        total += int(input(f"Score {i} of 12: "))
    return total / 12                      # RETURN - hand the answer back

average = average_of_twelve()              # CALL - and catch what comes back
print(f"Average : {average:.2f}")
print(f"Doubled : {average * 2:.2f}")      # you can do maths with a returned value
```

With the twelve numbers from the Week 7 card, the last two lines of real output:

```text
Average : 75.00
Doubled : 150.00
```

**And the honest criticism of that function**, which a strong student will raise: it both **fetches** the data and **works it out**, which means you cannot test it without typing twelve numbers by hand. Splitting those two jobs needs a way to hand the numbers *in* — which is parameters, and which is next week.

### Page 9.5 — Term 1 reflection sheet and revision list

**There are no right answers on this page and there is no mark.** What follows is what a good, honest sheet looks like — use it to judge whether a student is being specific, not whether they agree.

**9.5(a) Which single thing from Term 1 do you use most often without thinking about it?**

> Probably `f"..."`. In Week 3 I had to stop and remember the `f` every time and now my hands just do it. Second would be `int(input(...))` — I no longer have to be told that input is text.

**9.5(b) Which week's idea took longest to land, and what finally made it land?**

> Week 6, the ordering bug. What made it land was not the explanation, it was tracing 95 down the chain with my finger and having to say "is 95 sixty or more?" out loud. When I read it silently I kept skipping to the answer I expected.

**9.5(c) Which mistake have you made more than three times?**

> Forgetting the colon. And off-by-one on `range`, which I have now done in weeks 7, 8 and 9.

**9.5(d) How many entries are in your Bug Log, and how many are family three?**

A number and a number. Fifteen entries with five family-threes is a healthy Term 1. Three entries means the log is not being kept, and **that goes on the revision list as a habit.**

**9.5(e) The revision list — weeks, specifics, and how you will know.**

| Week | What specifically | How I'll know I've got it |
|---|---|---|
| 3 | I keep forgetting the `f`, so my braces print | Write five f-strings from memory with no example in front of me; check all five print values, not braces |
| 6 | I got bug 8 wrong — I looked at the `>= 90` line instead of the order of the branches | Write a five-branch chain from scratch and test 95, 80, 62, 50, 20; then say which two of those five actually prove the fix |
| 7 | `range` off-by-one. I said `range(1, 10)` gives ten numbers | For one week, say out loud how many values every `range` I write hands out, before I run it |
| 8 | I converted with `int()` before checking with `.isdigit()` | Take one of my own programs and make it survive `banana` at every single prompt |
| — | Bug Log has six entries for eight weeks | One entry every time something breaks, even when the fix took ten seconds |

**What full credit looks like:** at least three rows, every row naming a *specific* thing rather than a week, and every row's third column being something you could actually check on a Saturday. "Revise Week 6" is not a plan. "Write a five-branch chain and test both sides of every boundary" is.

**9.5(f) One thing you can now do that you could not do in Week 1.**

Anything honest. The strongest answers are usually not about syntax:

> I can read the last line of a traceback and know roughly where to look before I even open the file.

### Page 9.6 — Bug Log, Think Deeper and Self-Check

**The Bug Log.** Two entries, at least one a function bug.

| # | What I saw (real text) | What it meant, in my words | What I changed |
|---|---|---|---|
| 1 | **No output at all and no error message.** The banner code was in the file and correct. | I defined the function and never called it. Python read the recipe, wrote it down, and got to the end of the file with nothing to do. **Defining is not running.** | Added `print_header()` at the margin, three times |
| 2 | `TypeError: unsupported format string passed to NoneType.__format__` — and the number 75.0 was on the screen just above it | My function used `print` where it should have used `return`, so it showed me the answer and handed back nothing. `average` held `None`, and you cannot format nothing to two decimal places. **`NoneType` in a `TypeError` means a missing `return`.** | `return total / 12` instead of `print(total / 12)` |

Also acceptable, and arguably better:

| # | What I saw | What it meant | What I changed |
|---|---|---|---|
| 3 | **No output and no error**, with the call clearly there on the last line | I wrote `print_header` without brackets. That is the function's *name*, not an instruction to run it — and Python was perfectly happy to think about it and move on. Same trap as `.isdigit` last week. | Added the brackets |
| 4 | `NameError: name 'print_header' is not defined`, on a line where the function obviously existed twenty lines below | Python reads top to bottom. When it reached my call it had not read the `def` yet, so the name did not exist. | Moved all the `def`s to the top |

**9.6(a) Should every repeated block become a function?**

A full-credit answer (4+ sentences) argues a side and names the cost of being wrong. Model answer:

> There are two real camps and I do not think either one is silly. One says never write the same thing twice, because every duplicate is a future inconsistency waiting to happen — and today proved that, because I could not tell whether my three banners were identical without reading every character.
>
> The other camp says wait until the third copy, and their argument is better than it first sounds. Two blocks that look identical today are sometimes two different ideas that happen to coincide, and if I merge them and then one of them needs to change, I end up with a single function trying to serve two masters. That usually grows extra options and flags, and ends up harder to read than the duplication was.
>
> What I notice is that the disagreement is really about something neither side can know: whether those two blocks will change *together* or *separately* in future. So the rule I am going to use is: two copies, notice it and leave it; three copies, extract it. And one thing that seems to settle it either way — **if I have already had to change the same thing in two places on the same day, extract it now**, because that is no longer a prediction, it is evidence.

**9.6(b) Which family of trouble would you rather have in a program you were about to hand in?**
Family one, without hesitation. It never ran, so it cannot possibly have told anybody anything untrue. Family two is next, because at least it stopped and pointed at a line. Family three is the one I would not want, because it hands in a confident wrong answer and there is nothing at all to notice. **A program that refuses to run has not misled anyone; a program that lies has.**

**9.6(c) Why does Python need `def`? Couldn't it work out which lines belong together?**
No, because there is nothing in five consecutive lines that says whether they are one idea or five unrelated things that happen to be next to each other. Grouping is a fact about my intention, and my intention is not in the file until I put it there. `def` is exactly how I put it there — **and that is why the function's name matters so much, because the name is the only place my intention gets written down.** A wrong name is worse than no name, because it actively misleads the next reader, and the next reader is usually me.

**9.6(d) Your revision list has no marks on it. Is that better or worse than a score out of ten?**
Better, and the reason is that a score answers a question nobody needs answered. "Seven out of ten" does not tell me what to do on Saturday. "You missed all three of the silent ones" does. A score also encourages me to try to look good, which is precisely the wrong instinct in a checkpoint — the whole value of today was **finding out**, and finding out requires being willing to get things wrong on purpose. The one thing a score is genuinely good for is comparing across time, and my Bug Log already does that better: five family-three bugs in Term 1 versus two in Term 2 is a real measurement of something that matters.

**Self-check.**

| Statement | Answer |
|---|---|
| Defining a function runs it | **False.** Defining files the recipe. Calling runs it. |
| A function defined and never called causes an error | **False.** No output, no error, exit code 0. |
| `print_header` and `print_header()` do the same thing | **False.** Without brackets nothing runs, and nothing complains. |
| `def name():` needs a colon | **True.** Same rule as `if` and `for`. |
| `def name:` without brackets is fine | **False.** `SyntaxError`. The empty brackets are required. |
| A function with no `return` hands back `None` | **True.** |
| `return` prints the value | **False.** It hands it back. If you want to see it, print it yourself. |
| Lines after a `return` still run | **False.** `return` ends the function immediately. |
| You can do maths with a returned value | **True.** That is the main reason to return. |
| You can do maths with a printed value | **False.** Printing keeps nothing. |
| `NoneType` in a `TypeError` usually means a missing `return` | **True.** |
| A call above the `def` works fine | **False.** `NameError` — Python reads top to bottom. |
| A function may call another function | **True.** It is an ordinary call that happens to sit inside a `def`. |
| A `SyntaxError` means part of your program ran | **False.** None of it ran. |
| A `Traceback` with a line number means the program started | **True.** That is family two. |
| The most dangerous bugs give the clearest messages | **False.** The most dangerous ones give no message at all. |

### Lesson questions posed in the Say-this scripts

- *"Find something identical in both files."* → The banner block, in `guess.py`, `grade.py` and `about_me.py`.
- *"How many lines have you typed to say one thing?"* → Five lines × three copies = fifteen.
- *"If the wording changes, how many places?"* → Three. And Python will not tell you if you miss one.
- *"Can you prove all three copies are identical?"* → No — not without reading every character. **That is the real cost of copying.**
- *"What's the difference between defining and calling?"* → Defining writes the recipe and runs nothing; calling runs it.
- *"I define a function and never call it — what happens?"* → Nothing at all. No output, no error.
- *"What's the difference between `print_header` and `print_header()`?"* → The brackets mean "do it". Without them, nothing runs and nothing complains.
- *"What does a function with no `return` hand back?"* → `None`, Python's word for no value at all.
- *"Why can't you do maths with a printed answer?"* → Because printing sends it to the screen and keeps nothing.
- *"How many of your Bug Log entries had no error message?"* → Whatever the honest count is; usually a third or more, clustering in weeks 6 and 7.
- *"Did it crash?"* (the uncalled function) → No. No output either.
- *"How many times did you tell Python to run it?"* → Zero.
- *"What word jumps out of that last line?"* → `NoneType`.
- *"Which of my two mistakes was worse?"* → The `print`-instead-of-`return` one, because the right answer was on the screen and it still crashed.
- *"So how did I do?"* → A sentence, never a number: which families you are solid on and which you are not.
- *"Of the three families, which would you rather hand in?"* → Family one. It never ran, so it cannot have told anyone anything untrue.

---

## 🔮 Next Week Preview

Week 10 fills the hole the student has almost certainly already noticed. Every function this week does exactly the same thing every time it is called: `print_header()` prints one banner, thirty-four characters wide, and there is nowhere to tell it "make it forty" or "say LEVEL 3 instead". Next week that changes with one line of new syntax — `def f(a, b):` — and functions become genuinely useful. They will meet **parameters** (the names inside the definition), **arguments** (the values you hand over at the call), **default values** for the ones you usually do not need to specify, and **scope**, which is the reason a variable created inside a function does not exist outside it. The week ends with a planted bug the student will remember in June: a function that prints the right answer, returns `None`, and crashes three lines later — which is exactly the bug they met today, met again with parameters attached, and by then they will recognise the word `NoneType` on sight.

**Prep early:** two things. First, **keep this week's shortened file** — the one with `print_header()` in it. Week 10 opens by giving that same function a parameter so the banner can be any width, and the contrast is far stronger on a file the student wrote themselves than on a fresh example. Second, and more important: **look at the revision list before next week's lesson.** If Week 6's ordering rule or Week 7's `range` boundary is on it, spend five minutes at the start of Week 10 on that rather than pressing on. Functions with parameters are built on top of everything in Term 1, and the whole reason this checkpoint exists is so that you know what is underneath before you build on it.

---

[⬅ Week 8](week-08.md) · [Course Home](../README.md) · [Week 10 ➡](week-10.md) · [Student Guide](../student-guide/week-09.md) · [Workbook](../workbook/week-09.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
