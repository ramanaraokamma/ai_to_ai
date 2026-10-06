# Week 25 — Drawing the Table: Your First Chart

[⬅ Week 24](week-24.md) · [Course Home](../README.md) · [Week 26 ➡](week-26.md) · [Student Guide](../student-guide/week-25.md) · [Workbook](../workbook/week-25.md)

---

## 📋 At a Glance

| | |
|---|---|
| **Duration** | 70 minutes |
| **Type** | 🟦 Teach — one new library (matplotlib) and one new discipline (label everything) |
| **Big idea** | A chart with no axis labels is a decoration. The labels are what turn it into evidence. |
| **New vocabulary** | figure · axes · marker · axis label · savefig |
| **New syntax** | `fig, ax = plt.subplots(figsize=(6, 4))` · `ax.plot(x, y, marker="o")` · `ax.set_title()` / `ax.set_xlabel()` / `ax.set_ylabel()` · `fig.savefig("f.png", dpi=120, bbox_inches="tight")` |
| **Materials** | Printed workbook pages 25.1–25.6 · **one printed copy of the naked chart** (see Prep) · a pencil · a ruler is handy but optional |
| **Tech needed** | The `level2` folder, the `.venv` active, matplotlib installed (Orientation §4.3 and §4.5). One laptop is enough; two is better. |
| **Prep time** | 15 minutes the night before, 5 minutes on the day |

> **⚠️ Watch out:** matplotlib was installed and smoke-tested back in Orientation §4.5. **Run that smoke test again tonight**, before the lesson. Charts fail differently from everything else in Python — they can fail by producing *nothing at all*, with no error, and you do not want to be diagnosing that live in front of a student.

---

## 🎯 Lesson Objectives

By the end of the lesson the student can:

1. **Make a figure with one axes and draw a line on it** — typing `fig, ax = plt.subplots(figsize=(6, 4))` and `ax.plot(...)` from memory, and saying what each of the two names holds.
2. **Put a marker on every real data point** and say why that matters — that a line with no markers hides how many measurements it was drawn from.
3. **Add a title and both axis labels**, with the units named in each axis label.
4. **Save a chart to a PNG file** and explain why saving beats showing.
5. **Look at an unlabelled chart and state precisely what it does not tell you** — not "it's confusing", but a list: no units, no quantity, no time period, no idea how many points.

Observable evidence: three `.png` files on disk that the student can open, each with a title stating a finding and both axis labels naming units; plus a written list of at least four things a naked chart fails to say.

---

## 🧑‍🏫 What YOU Need to Know First

> **📌 About the code blocks in this guide.** Outside the **🧰 Prep Checklist** and the **🔑 Answer Key**, the blocks are **illustrations, not files** — each one carries on from the one above it, so the `import` lines and the data are typed once, in the first block that needs them. **The complete runnable files are in the Prep Checklist and the Answer Key.** If you paste an illustration on its own and get `NameError`, that is why, and nothing is broken.

You do not need to have drawn a chart in code before. Everything in this section is explained from zero, and by the end of it you will be able to answer "why?" as well as "what do I type?".

### 1. What matplotlib actually is, and why the name is odd

> **matplotlib** — a library that turns lists of numbers into pictures.

It is not part of Python itself. It was written by other people, installed with `pip` back in Orientation §4.3, and it lives in your `.venv`. The name is a squash of "MATLAB-like plotting library", MATLAB being a piece of maths software from the 1980s. Nobody says the name out loud without wincing. You import one particular part of it, and there is a universal nickname:

```python
import matplotlib.pyplot as plt
```

Read that line as: *"go into the matplotlib library, find the part called `pyplot`, and from now on let me call it `plt`."* The `as plt` bit is exactly the same trick as `import numpy as np` from Week 17. Every tutorial, every book, every Stack Overflow answer in the world uses `plt`. Do the same, so that when your student searches the internet in a panic the code they find matches the code on their screen.

### 2. The one genuinely confusing idea: a figure is not the same as an axes

This is the thing to get straight tonight, because it is the thing students get wrong all year.

🍕 **The analogy that works.** The **figure** is a sheet of paper. The **axes** is one drawing frame you have ruled onto that paper. One sheet of paper can hold several frames side by side — you will do exactly that in Week 27 — but this week there is one sheet and one frame.

> **Figure** — the whole picture, the thing that becomes a `.png` file.
> **Axes** — one drawing box inside a figure, with its own title, its own x axis and its own y axis.

![One figure, one axes, and the five things you must label](../figures/fig-w25-1-figure-and-axes-anatomy.svg)
*Figure 25.1 — The pale sheet is the figure. The pink box is the axes. Four of the five labelled parts are words you type.*

**Yes, "axes" is a terrible name.** It looks like the plural of "axis", and it is not. In matplotlib an *axes* (singular) is the box; the two lines inside it are the *x axis* and the *y axis*. It has been this way since 2003 and it is not going to change. When a student says "so an axes has two axises?", the correct answer is: "Yes. It is a bad name. Everyone agrees. Move on." Do not spend three minutes apologising for it — name it as a wart, and carry on.

**Why the split matters, practically.** Titles and axis labels belong to the **axes**, because a sheet with two frames needs two titles. Saving belongs to the **figure**, because you save the whole sheet, not one frame. That is why the calls split the way they do:

| You want to… | You ask… | Because… |
|---|---|---|
| add a title | `ax.set_title(...)` | the title belongs to one frame |
| label the x axis | `ax.set_xlabel(...)` | so does the axis |
| draw the data | `ax.plot(...)` | you draw *inside* a frame |
| save the file | `fig.savefig(...)` | you save the whole sheet |

If a student types `fig.set_title(...)` it will fail, and the reason is not arbitrary. It is: *a sheet of paper does not have a title; a drawing on it does.*

### 3. Every line of this week's code, explained to someone who has never programmed

Here is the whole file the class will build. Read it once, then read the line-by-line notes underneath. Nothing here is skipped.

```python
# week25_visits.py -- one line chart, fully labelled, saved to a file.
import matplotlib.pyplot as plt            # the drawing library. Everyone calls it plt.

# Week numbers, in order. This is the x axis.
weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# How many people came into the school library in each of those weeks.
visits = [118, 126, 131, 140, 152, 149,
          158, 171, 166, 158, 174, 189]

print("weeks :", len(weeks))               # how many x values are there?
print("visits:", len(visits))              # how many y values? Must be the same.

fig, ax = plt.subplots(figsize=(6, 4))     # fig = the sheet of paper, ax = the frame

ax.plot(weeks, visits, marker="o")         # draw the line, dot on every real point

ax.set_title("Library visits climbed 60% over one term")   # the finding
ax.set_xlabel("School week (week 1 = start of term)")      # what x is, and its units
ax.set_ylabel("Visits per week (count of people)")         # what y is, and its units

fig.savefig("visits.png", dpi=120, bbox_inches="tight")    # write the picture to disk
print("saved visits.png")
```

```text
weeks : 12
visits: 12
saved visits.png
```

**`import matplotlib.pyplot as plt`** — fetch somebody else's code and give it a short nickname. Already met in Week 17 (`import numpy as np`) and Week 21 (`import pandas as pd`). Nothing new except the name.

**`weeks = [1, 2, ... 12]`** — a list, from Week 11. Square brackets, commas between the items. These are the x values, and they are in order, which is what earns us the right to join them with a line at all.

**`visits = [118, ...]` split across two lines** — Python does not care about line breaks *inside* brackets. Once a `[` is open, it keeps reading until it finds the matching `]`. This is worth saying out loud, because a student who does not know it will squash all twelve numbers onto one 90-character line and then not be able to read their own file.

**`print("weeks :", len(weeks))`** — `len()` from Week 11 counts the items. This line exists purely as insurance. `ax.plot` demands that the two lists are the same length, and the error it gives when they are not is confusing. Printing both lengths first turns a confusing error into an obvious one. **Keep these two lines. They are not clutter; they are the seatbelt.**

**`fig, ax = plt.subplots(figsize=(6, 4))`** — the hard line. Three separate new things in it:

- **Two names on the left of one `=`.** So far every assignment has been `name = value`. This one is `name, name = ...`. It works because `plt.subplots()` hands back **two things at once**, and Python lets you catch them in two boxes in one go. Read it as: *"make a sheet and a frame, put the sheet in a box called `fig`, put the frame in a box called `ax`."* If the student writes `ax = plt.subplots(...)` instead, then `ax` ends up holding *both* things stuck together, and the next line explodes with `AttributeError: 'tuple' object has no attribute 'plot'`. That is Debugging Clinic row 3, and you should expect to meet it.
- **`figsize=(6, 4)`** — a **keyword argument**, met in Week 10. It says: make the sheet six inches wide and four inches tall. Inches, not pixels — matplotlib was designed by people printing on paper.
- **`(6, 4)`** — round brackets with a comma. A **pair**, like a coordinate on a graph. Width first, then height, the same order as everything else in the library. It is *not* a list, and the difference does not matter to anybody this year: "a pair you are not going to change" is a complete and sufficient explanation.

**`ax.plot(weeks, visits, marker="o")`** — draw inside the frame. First argument is the x values, second is the y values, and the order is not negotiable. `marker="o"` says *put a small circle at every real measurement*. That is a lowercase letter **o**, not a zero — matplotlib refuses the zero with a genuinely baffling error (Clinic row 8).

**`ax.set_title(...)`, `ax.set_xlabel(...)`, `ax.set_ylabel(...)`** — three method calls, each taking one string. `set_` at the front is a naming convention meaning "put this value in". They can go in any order. They can be typed at any point before the save. If you forget one, nothing breaks — and that is precisely the problem this week is about.

**`fig.savefig("visits.png", dpi=120, bbox_inches="tight")`** — write the picture to a file in the current folder.

- `"visits.png"` — the filename. The `.png` matters: matplotlib picks the file format from the extension. Leave it off and you get `visits.png` anyway, silently, which is fine but teaches nothing.
- `dpi=120` — **dots per inch**. The sheet is 6 × 4 inches, so at 120 dpi the figure is 720 × 480 pixels before cropping (`bbox_inches="tight"` trims the white border, so the saved file is a little smaller, about 650 × 470). Higher dpi means a bigger, sharper file. 120 is a good default for a screen; 300 is print quality and about six times as many pixels.
- `bbox_inches="tight"` — "crop off the empty white border, but do not cut off my labels". Without it, long axis labels sometimes get chopped at the edge of the image. One extra argument, one entire category of frustration removed. **Type it every time.**

**`print("saved visits.png")`** — because the alternative is a program that runs, prints nothing, and leaves you guessing.

### 4. Why saving beats showing, and the trap in `plt.show()`

There is a second way to see a chart: `plt.show()`, which tries to open a window. It has three problems, and the third is the one that will wreck a lesson.

1. **It blocks.** The program stops dead at `plt.show()` and does not continue until you close the window. Students think their program has hung. It has not; it is waiting.
2. **It cannot be handed in.** A window is not a file. You cannot print it, email it, or put it in a project folder.
3. **On some setups it does nothing at all.** If matplotlib cannot find a window system it prints a warning and carries on. The program says nothing is wrong, and no picture appears anywhere. Here is the real message:

```text
week25_visits.py:20: UserWarning: Matplotlib is currently using agg, which is a
non-GUI backend, so cannot show the figure.
  plt.show()
```

![A chart you never saved did not happen](../figures/fig-w25-4-savefig-always.svg)
*Figure 25.2 — Save first, always. Show a window as well if you like, but never instead.*

**The rule for this course: every chart calls `fig.savefig(...)`.** If a window also pops up, lovely. But the file on disk is the deliverable, and it works on every machine, including the one that has no screen. This is not a workaround — it is what people who actually produce charts for a living do.

### 5. Markers, and why an unmarked line is a small dishonesty

`marker="o"` looks cosmetic. It is not.

![Markers show how much you really measured](../figures/fig-w25-3-markers-show-real-points.svg)
*Figure 25.3 — The drawn line is identical in all three panels. Only the markers say whether it came from 4 measurements or 13.*

A smooth line drawn through 4 points and a smooth line drawn through 400 points can be *pixel-for-pixel identical*. Without markers, the reader cannot tell which they are looking at, and those two charts deserve very different amounts of trust. Putting a dot on every real measurement is the cheapest honesty available in the whole of data work: eleven characters.

### 6. A title states the finding. An axis label states the units.

Two rules, and they are the whole point of the week.

**Title.** `"Visits vs week"` is a filename, not a title. It describes the ingredients. `"Library visits climbed 60% over one term"` is a title, because it says what happened. **Test:** if your title would sit equally happily on top of any chart of that data, it is doing no work.

**Axis label.** `"Score"` could be out of 10, out of 100, or a percentage. `"Score (points out of 100)"` cannot be misread. `"Distance"` could be metres or kilometres. Units, in brackets, every time. It costs four seconds of typing and removes an entire species of misunderstanding.

![Three lines of typing turn a decoration into evidence](../figures/fig-w25-5-label-ladder.svg)
*Figure 25.4 — Rung 2 adds the two axis labels. Rung 3 adds the title. Same pixels of line all the way along.*

### 7. The three misconceptions you will actually meet

**Misconception 1 — "no error means it worked."** This is the big one, and this week is where it dies. A matplotlib program can run perfectly, exit with no error, and produce absolutely nothing. The student has done nothing wrong syntactically; they simply never asked for the picture. The sentence to use, and to keep using: **"A silent success is not a success. Where is the file?"** Then make them list the folder and look.

**Misconception 2 — "figure and axes are the same thing."** Cured by the sheet-of-paper picture and by one question: *"If I drew two graphs on one sheet, which title would there be two of?"* Answer: two axes titles, one file.

**Misconception 3 — "labels are decoration you add at the end if there's time."** Cured by the Hook, not by explanation. Show them an unlabelled rising line and let them discover that they cannot say a single true thing about it. Do not tell them; make them fail to describe it.

### 8. How deep to go, and where to stop

**Go this far:** figure vs axes, `ax.plot` with markers, the three label calls, `savefig`, and the discipline of stating what a chart does not tell you.

**Stop before:**
- **Colours, line styles, line widths, grids, fonts.** Every single one is a rabbit hole and none of them is a *chart* skill. If a student asks how to change the colour, tell them `color="red"` works and move straight on. Do not build a lesson on it.
- **Bar, histogram, scatter.** That is Week 26 and it is the payoff. Today is one shape only, so that all the attention lands on the labelling.
- **`ax.set_ylim(...)`.** That is Week 27's entire lesson, because it is how you lie with a chart. If it comes up today: "That is a whole lesson on its own, in two weeks, and it is the most interesting one of the term." Do not demonstrate it.
- **`ax.legend()`.** Week 27. It is pointless with one line, and matplotlib says so out loud.
- **`fig.tight_layout()`.** You do not need it; `bbox_inches="tight"` does the same job for a single-frame figure with one fewer line to remember.
- **Jupyter notebooks.** Plain `.py` files all week. Notebooks arrive in the capstone.

---

### 9. 🧭 The Growing Map — stage four opens

The student guide carries a figure called **Where This Fits**: the same picture every week with one
more piece filled in. It is the only page that shows the learner the *shape* of the year rather than
this week's content — and this week it moves further than it has moved since Week 19.

![The Level 2 pipeline in Week 25: stage three is finished and stage four opens with your first chart](../figures/fig-w25-0-where-this-fits.svg)

*Figure 25.0 — Week 25's version. Stage three is finished, so all six of its boxes are plain white.
Stage four is solid for the first time and its first tile is gold. Only **representation** is lit.*

**What to do with it, in about two minutes at the end of the lesson:**

1. **Show it and ask where today went.** *"`fig, ax`, the three labels, `savefig` — is that a new box,
   or a whole new stage?"* A new stage, and it is the fourth of five. Let them find `SEE IT`
   themselves; the jump is large enough to be visible from across the room.
2. **Then read a dashed label out loud:** *"the box next to ours says **honest axes**. What do you
   think a *dishonest* axis would look like?"* Take a guess or two and then **stop** — do not answer.
   That is Week 27, it is the best lesson of the term, and a two-week wait is what makes it land.
3. **Have them update their own copy.** Three whole stages go solid today — that is a satisfying thing
   to do in pencil, and it is the first time the left half of their map is finished.

> **🧑‍🏫 Why this is worth two minutes.** Charts feel like the fun bit after a month of admin, and that
> framing is a trap: it invites learners to treat labelling as optional decoration. The map fixes the
> framing without a lecture — `SEE IT` is a *stage of the pipeline*, sitting between cleaning and
> predicting, doing a job. Not a reward.

> **⚠️ Watch out:** **data** is not lit this week and **representation** is lit alone. If a student
> notices, the answer is good and short: *"we didn't change the numbers today, we only changed how they
> are shown."* That is exactly what the representation thread is for, and it is the cleanest example of
> it in the whole level.

---

## 🧰 Prep Checklist

### 15 minutes the night before

- [ ] **Print workbook pages 25.1–25.6.**
- [ ] **Print the naked chart for the Hook.** Open `../figures/fig-w25-2-naked-chart-says-nothing.svg`, and print **only the left-hand box** — the rising line with no words on it. Easiest way: print the whole figure, then fold or cut the page so the three note cards on the right are hidden. You will reveal them one at a time. If you cannot print, draw it by hand on paper: eight dots rising left to right with one small dip, joined up, with two bare axis lines and **not one single word or number**.
- [ ] **Run the smoke test again.** In your `level2` folder, with the venv active:

  ```bash
  python smoke_plot.py
  ```

  You want either a window with a rising line, or a new `smoke_plot.png` in the folder. Either is a pass. If neither happens, stop and fix it tonight using Orientation §4.7 — do not carry it into the lesson.
- [ ] **Type this week's file yourself, from scratch, without copying.** Create `week25_visits.py` in `~/ai-academy/level2` with exactly the code from section 3 above, and run it:

  ```bash
  python week25_visits.py
  ```

  Expected, exactly:

  ```text
  weeks : 12
  visits: 12
  saved visits.png
  ```

  Then **open `visits.png` and look at it.** Fifteen minutes of typing buys you the confidence to teach it, and you will hit at least one typo of your own, which is the best possible rehearsal.
- [ ] **Break it on purpose, once.** Change `ax.set_xlabel` to `ax.set_xlable` and run it. Read the error. That is the mistake you are going to make deliberately in front of the student, and you should see it before they do.
- [ ] **Find the student's Week 21 file.** They built a 10-row DataFrame about their own week. It is probably called something like `week21_myweek.py`. If it has vanished, use the fallback `myweek.py` in the Answer Key — copy it into the folder before the lesson so that "Their Turn" is not spent retyping data.

### 5 minutes on the day

- [ ] Terminal open, in `~/ai-academy/level2`, venv active, `python --version` checked.
- [ ] The folder window open **next to** the terminal, so the `visits.png` file can be seen appearing. This is not optional staging — the moment the file appears in the folder is the moment the lesson lands.
- [ ] Editor open on the `level2` folder with the `.venv` interpreter selected.
- [ ] The printed naked chart face down on the table.
- [ ] The three note cards (pizzas / rainfall / flu) cut out or folded, hidden.

### Fallback if the laptop fails

| If this fails | Do this instead |
|---|---|
| matplotlib will not import | Teach the whole lesson on **graph paper**. Hand the student the twelve numbers and have them plot the points, join them, and then write the title and both axis labels. Every objective except `savefig` is met, and objective 5 is met *better* on paper than on a screen. Do the code next week as a 15-minute catch-up. |
| No laptop at all | Same as above. This lesson survives paper better than any other week in the term, because the content is *what a chart must say*, not what matplotlib can do. |
| A window pops up and the program appears to hang | It has not hung. Close the window. Then delete `plt.show()` from the file — you do not need it, because you are saving. |
| No window and no file | You forgot `savefig`, or you are looking in the wrong folder. Run `ls` (macOS/Linux) or `dir` (Windows) in the terminal. **Do this in front of the student.** It is a better lesson than the one you planned. |
| The printer failed | Draw the naked chart on paper. Honestly, hand-drawn is better: it is obviously not a computer's fault. |
| The student's Week 21 DataFrame is gone | Use `myweek.py` from the Answer Key. Say out loud: "This is my week, not yours, so the numbers will be boring. Week 21's file is worth finding for next time." |

---

## ⏱️ The Lesson, Minute by Minute

| Segment | Minutes | Running total | What happens |
|---|---|---|---|
| 🪝 Hook — What Does This Chart Mean? | 7 | 7 | A rising line that means nothing at all |
| 🧠 Concept — Paper, Frame, and Five Labels | 16 | 23 | Figure vs axes; markers; why you save |
| 💻 Live-Code Together — Build `week25_visits.py` | 18 | 41 | Type it together, break it twice, fix it twice |
| 🎲 Their Turn — Three Charts From Your Own Table | 20 | 61 | Student drives; the silent-success bug is planted |
| 🔑 Wrap & Assign | 9 | 70 | Three checks, the takeaway, homework |

---

### 🪝 Hook — What Does This Chart Mean? (7 minutes)

**Do this:** Put the printed naked chart on the table, face up. Say nothing for five seconds. Then hand them a pencil.

**Say this:**

> "Here is a chart. Somebody made it and put it in front of you because they want you to believe something.
>
> I want you to write, on the paper, one sentence that this chart proves. One true sentence. Take a minute."

Let them try. Watch what happens. Almost every student writes something like *"it went up"*, and then stops, because there is nothing else available.

> "Read me what you wrote."

Whatever they say, take it seriously and then push on it.

> "'It went up.' Right. What went up?"

Wait. Let the silence sit. This is the whole hook and it works because they cannot answer.

> "You don't know. Neither do I. So let me tell you what this is a chart of."

**Do this:** Reveal note card 1 — *Pizzas sold each week*.

> "It's pizza sales at the place on the corner. Up sixty percent over a term. The shop is booming."

Pause. Then reveal card 2 — *Rainfall each week, in mm*.

> "Actually, no. It's rainfall in millimetres. Up sixty percent. The monsoon arrived early."

Pause. Then card 3 — *Flu cases each week*.

> "Or — and this is the same line, I have not touched it — it's flu cases at this school. Up sixty percent. Somebody should probably shut the school.
>
> Same line. Identical pixels. Three completely different worlds, and one of them is an emergency. **The line is not the chart.** The line is the easy part. The words are the chart, and there aren't any."

![An unlabelled chart does not mean anything](../figures/fig-w25-2-naked-chart-says-nothing.svg)
*Figure 25.5 — All three note cards fit that line exactly. So the line, on its own, is a decoration.*

> "Here's the sentence for the whole lesson, and I want you to write it at the top of page 25.1.
>
> **A chart with no labels is a decoration. The labels are what turn it into evidence.**
>
> By the end of today you'll be making charts nobody can do this to."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Write one true sentence this chart proves." | Something like "the thing went up" — and then they run out. | If they write "sales went up", ask "where does it say sales?" That is the win, and it is better coming from their own pencil. |
| "What went up?" | "I don't know." | If they guess confidently — "it's obviously money" — reveal the rainfall card immediately. Being confidently wrong here is the most useful thing that can happen. |
| "How many measurements is this drawn from?" | "No idea." (There are eight dots, but if you drew it without dots, they cannot even count.) | If they count the dots, brilliant — say so, and tell them that is exactly what `marker="o"` is for and they have just discovered objective 2. |
| "What's the biggest number on it?" | "There aren't any numbers." | If they point at the top of the line: "That's a height. What number is it?" |

---

### 🧠 Concept — Paper, Frame, and Five Labels (16 minutes)

**Do this:** Put workbook page 25.1 between you (the labelled-diagram page). Have Figure 25.1 visible — on screen or printed.

**Say this — part 1, the sheet and the frame:**

> "Before anything else, two words, because matplotlib will keep using them at you.
>
> The **figure** is the sheet of paper. It's the whole picture. It's what becomes the file.
>
> The **axes** is one drawing frame you've ruled onto that sheet. It has its own title, its own left-hand edge, its own bottom edge.
>
> And yes — 'axes' is a rotten name, because it looks like the plural of 'axis'. It isn't. An *axes* is a box, and inside the box there's an x axis and a y axis. It's been called that since before you were born and nobody is going to fix it. Just know it's a box."

Point at Figure 25.1 as you say this.

> "Why do we care? Because it decides which word you type. **Titles and labels belong to the frame.** Saving belongs to the sheet. If I drew two graphs on one sheet of paper, how many titles would I need?"

> "Two. One per frame. But how many files would I save?"

> "One. Because there's one sheet. That's the entire reason there are two names."

**Say this — part 2, the five things:**

> "Right. Look at Figure 25.1 and count the numbered pins with me. There are five parts to any chart, and **four of them are words you type.**
>
> One, the **title** — and a title's job is to say what you *found*, not what's in the chart. 'Visits versus week' is a filename. 'Library visits climbed sixty percent' is a title.
>
> Two and three, the **axis labels** — one for the bottom, one for the side. And here's the rule that stops all the arguing: **the units go in the label.** Not 'Score'. 'Score, points out of a hundred'. Not 'Distance'. 'Distance to school, in kilometres'. Four extra seconds. Whole category of confusion, gone.
>
> Four, the **marks** — the actual line, the actual dots. That's the bit everybody thinks is the chart. It's one fifth of it.
>
> Five, the **axes** itself, the box. You get that for free when you ask for it."

**Say this — part 3, markers:**

> "One more thing before we type, and it's small and it matters.
>
> When you draw the line, you can put a dot on every real measurement. Look at Figure 25.3." *(Show it.)*
>
> "Three panels. **The line is exactly the same in all three.** Same pixels. But the middle one was drawn from four measurements and the right-hand one from thirteen. And if you don't put the dots on, nobody — including you, in a month — can tell which.
>
> Would you trust those two charts the same amount?"

> "No. Four points and thirteen points are not the same evidence. So: **dots on every real point, every time.** It's eleven characters. `marker="o"`."

**Say this — part 4, saving:**

> "Last thing. When your program draws a chart, the chart exists — but it exists nowhere you can see. It's just sitting in the computer's memory. You have to ask for it.
>
> There are two ways to ask. You can ask for a **window** to pop up. Or you can ask for a **file** on disk. Look at Figure 25.2." *(Show it.)*
>
> "The window is nice when it works. The problem is it doesn't always work — some computers have no window system, and matplotlib just shrugs and carries on, and your program finishes with no error and no picture. Nothing. And you sit there thinking your code is broken when your code is fine.
>
> So the rule in this course, all year: **every chart gets saved to a file.** `fig.savefig`. If a window turns up as well, great. But the file is the thing. You can open it, print it, email it, stick it in your project."

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "If I put two graphs on one sheet, how many titles and how many files?" | Two titles, one file. | If they say two files, go back to the paper analogy and physically hold up one sheet. |
| "Which is the figure — the file, or the box the line is in?" | The file. The box is the axes. | If they mix them, ask "which one do you save?" That question always sorts it. |
| "'Score' as a y-axis label. What's wrong with it?" | No units. Out of 10? Out of 100? A percentage? | If they say "nothing", write `Score: 8` on paper and ask "good or bad?" Then write `Score: 8 out of 10`. |
| "Why put a dot on every point?" | So the reader knows how many real measurements there were. | If they say "it looks nicer" — accept it, then show Figure 25.3 again and ask which panel they trust more. |
| "My program ran, there was no error, and no picture appeared. What went wrong?" | Nothing went wrong with the code. It was never asked to save or show. | If they say "it's broken", that is the misconception in the wild. Reply: "It ran perfectly. It did exactly what you told it. What didn't you tell it?" |

---

### 💻 Live-Code Together — Build `week25_visits.py` (18 minutes)

You type on the shared screen; **the student types the same thing on their own machine, line for line.** Not copy-paste. Typing is where the syntax lands.

There are **two deliberate mistakes** in this segment, marked 🐞 below. Make them on purpose, with a straight face, and fix them out loud. Modelling the recovery is the point of the segment — arguably more valuable than the chart.

#### Step 1 — new file, the data, and the seatbelt (4 min)

**Do this:** New file, save it as `week25_visits.py`. Type:

```python
# week25_visits.py -- one line chart, fully labelled, saved to a file.
import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
visits = [118, 126, 131, 140, 152, 149,
          158, 171, 166, 158, 174, 189]

print("weeks :", len(weeks))
print("visits:", len(visits))
```

**Say this:**

> "Twelve weeks, twelve visit counts. Made-up numbers, but shaped like a real school library's.
>
> Notice the `visits` list runs over two lines. That's allowed — once you open a square bracket Python keeps reading until it finds the closing one. Use it. Twelve numbers on one line is unreadable.
>
> And those two `print` lines? Those are a seatbelt. In a second we're going to hand both lists to matplotlib, and it will refuse if they're different lengths. Printing both counts first means that if I've dropped a number, I find out in a way I can understand."

Run it. Expected:

```text
weeks : 12
visits: 12
```

> "Twelve and twelve. Safe to carry on."

#### Step 2 — the sheet, the frame, and the line (4 min)

**Do this:** Add:

```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(weeks, visits, marker="o")
```

**Say this:**

> "This is the strangest line you'll type today, so let's take it apart.
>
> `plt.subplots` makes a sheet and a frame and hands you **both at once**. Two things. So there are two names on the left of the equals sign, separated by a comma. `fig` catches the sheet, `ax` catches the frame. That's the only line all year that does this, and now you've seen it.
>
> `figsize=(6, 4)` — six inches wide, four inches tall. Inches, because this library was built by people printing on paper. The round brackets with a comma are just a pair: width, then height.
>
> Then `ax.plot` — draw, *inside the frame*. x values first, y values second. Never the other way round.
>
> And `marker="o"` — that's a letter o, lowercase. Put a dot on every real measurement."

**Ask this before running:** *"What do you think will happen when we run this?"*

Hoped-for answer: "a chart appears." Let them predict it. Then run it.

```text
weeks : 12
visits: 12
```

> "Nothing. No chart. No error either — look, it exited perfectly happily. **The chart exists. It's in memory. Nobody has asked to see it.** That's exactly what Figure 25.2 was about. Hold that thought — we'll fix it in two steps."

This is a real, honest, planned failure and it is the most valuable thirty seconds in the lesson. Do not rush past it.

#### Step 3 — the three labels, and 🐞 deliberate mistake #1 (5 min)

**Do this:** Add the title first:

```python
ax.set_title("Library visits climbed 60% over one term")
```

**Say this:**

> "Title first. And notice what I wrote — not 'visits by week'. That's a filename. I wrote what actually happened: it climbed sixty percent. If my title would fit on top of *any* chart of this data, it isn't earning its place."

🐞 **Now make the mistake.** Type, deliberately and without comment:

```python
ax.set_xlable("School week (week 1 = start of term)")
```

Run it. You get:

```text
weeks : 12
visits: 12
Traceback (most recent call last):
  File "/Users/you/ai-academy/level2/week25_visits.py", line 13, in <module>
    ax.set_xlable("School week (week 1 = start of term)")
AttributeError: 'Axes' object has no attribute 'set_xlable'. Did you mean: 'set_xlabel'?
```

**Say this:**

> "Right — red. Ritual first. **Read the last line out loud.**"

Have them read it. Then:

> "`'Axes' object has no attribute 'set_xlable'`. Translate it: *I asked the frame to do something called `set_xlable`, and the frame has never heard of that.* Which is fair, because I typo'd it. L-A-B-E-L. I typed L-A-B-L-E.
>
> And look — Python actually guessed. *'Did you mean set_xlabel?'* It will do that quite often. It is not always right, but when it offers, read it."

Fix it in front of them, run again, and add the y label:

```python
ax.set_xlabel("School week (week 1 = start of term)")
ax.set_ylabel("Visits per week (count of people)")
```

```text
weeks : 12
visits: 12
```

> "Still no picture. Still no error. We now have a fully labelled chart that nobody in the universe can see."

#### Step 4 — 🐞 deliberate mistake #2, then save it properly (5 min)

🐞 **Make the second mistake.** Type:

```python
plt.show()
```

Run it. **One of two things happens, and you must handle whichever you get:**

- **A window opens.** Say: "There it is. Now watch." Leave the window open for ten seconds. Point at the terminal: it is stuck; the prompt has not come back. "The program has stopped and it is waiting for me to close that window. And when I close it, that picture is gone forever. I can't print it, I can't hand it in, I can't email it to you."
- **No window, and a warning appears:**

  ```text
  week25_visits.py:15: UserWarning: Matplotlib is currently using agg, which is a
  non-GUI backend, so cannot show the figure.
    plt.show()
  ```

  Say: "That's this computer telling me it has no window system. It's a warning, not an error — the program finished fine. And produced nothing. **This is the failure I want you to be able to survive.**"

Then delete `plt.show()` and type the real thing:

```python
fig.savefig("visits.png", dpi=120, bbox_inches="tight")
print("saved visits.png")
```

**Say this:**

> "`fig.savefig` — note it's `fig`, the sheet, not `ax`. You save the whole sheet.
>
> `"visits.png"` — the name. The `.png` on the end tells matplotlib what kind of picture to make.
>
> `dpi=120` — dots per inch. Six inches wide at a hundred and twenty dots each, so the picture is seven hundred and twenty pixels wide before the tight crop trims the edges. Bigger number, sharper picture, bigger file.
>
> `bbox_inches="tight"` — 'trim the empty white edge, but don't cut off my labels'. Type it every single time. It is the difference between a chart with an axis label and a chart with half an axis label."

**Do this:** Run it. Then — and this is the moment — **point at the folder window and watch `visits.png` appear.**

```text
weeks : 12
visits: 12
saved visits.png
```

Open the file. Look at it together.

**Ask this:**

| Ask | Answer you want | If they say something else |
|---|---|---|
| "Before I run step 2 — what happens?" | "A chart appears." (They will be wrong, and that is the point.) | If they say "nothing, because we haven't saved it" — outstanding. Say so loudly, then run it and prove them right. |
| "Read the last line of that traceback." | `AttributeError: 'Axes' object has no attribute 'set_xlable'` | If they start reading from the top, stop them gently: "Bottom line first. Always. The top is just the route the error took." |
| "What does 'has no attribute' mean, in plain words?" | "The frame doesn't have a thing called that." | If stuck, offer: "I asked a dog to fetch the newspaper in French." |
| "Why `fig.savefig` and not `ax.savefig`?" | You save the whole sheet, not one frame. | If they guess, accept it and reinforce with the paper analogy. |
| "We ran it three times with no error and no picture. Was the code broken?" | No — it was doing exactly what it was told. | This is the key check of the segment. If they say "yes, broken", go back to Figure 25.2. |

---

### 🎲 Their Turn — Three Charts From Your Own Table (20 minutes)

Student on the keyboard. You do not touch it. Full instructions in the next section.

- **Minutes 0–4:** open the Week 21 file, print the DataFrame, decide which three columns to chart.
- **Minutes 4–16:** build the three charts. Every one gets a title, both axis labels with units, markers, and a `savefig`.
- **Minutes 16–20:** open all three PNGs side by side and write the three captions.

---

## 🎲 The Activity, In Full

### Setup

**On the table:** workbook pages 25.2 and 25.4, a pencil.

**On the machine:** the `level2` folder, terminal in it, venv active, editor open, and the folder window visible beside the editor.

**The data:** the student's own 10-row DataFrame from Week 21 — the one about their own week. If it is missing, drop `myweek.py` (Answer Key, page 25.4) into the folder and use that.

### The rules

1. **One chart per file is fine, and three files is fine too.** Do not make them write a function unless they want to. If they *do* want to, they have had functions since Week 10 and it is a lovely extension.
2. **A chart is not finished until the PNG exists and has been opened and looked at.** "It ran" is not finished.
3. **Every chart needs all four words-you-type:** title, x label, y label — and the units inside both axis labels.
4. **The title must state a finding.** If it could sit on any chart of that data, it goes back.
5. **Markers on. Every time.**

### Step 1 — Look at the table first (4 minutes)

```python
# week25_look.py
from myweek import build_my_week      # or: from week21_myweek import build_my_week

df = build_my_week()
print(df)
```

```text
   day day_name  homework_min  screen_min  sleep_hours  steps
0    1      Mon            45          60          8.0   6200
1    2      Tue            60          45          7.5   7100
2    3      Wed            30          90          8.5   5800
3    4      Thu            75          30          7.0   8400
4    5      Fri            20         120          9.0   6900
5    6      Sat             0         180          9.5  11200
6    7      Sun            90          75          8.0   4300
7    8      Mon            55          50          7.5   7600
8    9      Tue            65          40          8.0   8100
9   10      Wed            40          85          8.5   6500
```

> **🧑‍🏫 If a student asks:** *"Which columns should I chart?"* — Answer: "Any three number columns. But `day` has to be on the bottom of all three, because a line only earns the right to join points up when the x axis is in order. Days are in order. `day_name` is not a number, so it can't go on either axis yet."

### Step 2 — The first chart, all four labels (5 minutes)

```python
# week25_chart_homework.py
import matplotlib.pyplot as plt
from myweek import build_my_week

df = build_my_week()

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(df["day"], df["homework_min"], marker="o")

ax.set_title("Homework peaked at 90 minutes on day 7")
ax.set_xlabel("Day of the fortnight (day 1 = first Monday)")
ax.set_ylabel("Homework done (minutes)")

fig.savefig("myweek_homework.png", dpi=120, bbox_inches="tight")
print("saved myweek_homework.png")
```

```text
saved myweek_homework.png
```

**Then make them open it.** Not "it says saved". Open the file.

### Step 3 — Two more, and the planted bug (7 minutes)

Charts two and three: `screen_min` and `steps`. Same shape, new titles, new y labels.

> **⚠️ Watch out — the planted bug.** Most students copy the first file and edit it. About half of them will edit the `plot` line and the labels and **forget to change the filename in `savefig`**. So all three programs write to `myweek_homework.png`, each one flattening the last. The terminal says `saved` three times. Nothing is wrong. There is one file where there should be three.
>
> Do not point at the line. Say: **"Show me your three files."** Let them find it in the folder listing. This is the same lesson as the silent success, one level up: the program was obedient, and obedience is not correctness.

### Step 4 — Caption them (4 minutes)

For each chart, one sentence on page 25.4 saying **what it shows**, and one saying **what it does not tell you**.

Model answers:

| Chart | What it shows | What it does not tell you |
|---|---|---|
| homework | Homework climbed to 90 minutes on day 7 after a day of none at all. | Which subject, whether it was finished, or whether day 7 was catch-up for day 6. |
| screen time | Screen time hit 180 minutes on day 6, the Saturday, and dropped back to 75 on Sunday. | What was on the screen — homework research and cartoons look identical here. |
| steps | Day 6 was the only day over 10,000 steps; day 7 was the lowest at 4,300. | Whether the tracker was actually worn all day, or what counted as a step. |

### What "finished" looks like

- Three `.png` files in the folder, with three **different** names.
- All three have been opened and looked at.
- Every chart has a title that states a finding, and both axis labels name units.
- Every chart has visible markers, and the student can count them (there should be ten).
- Six sentences written: one "what it shows" and one "what it does not tell you" per chart.

### Variation — easier

- **Do one chart, not three.** Objective 1 to 4 are all met by one chart. Three is practice, not content.
- **Give them the file with four blanks in it** and have them fill in only the strings:

  ```python
  import matplotlib.pyplot as plt
  from myweek import build_my_week

  df = build_my_week()

  fig, ax = plt.subplots(figsize=(6, 4))
  ax.plot(df["day"], df["_______"], marker="o")   # pick a number column

  ax.set_title("_______________________________")  # what did you find?
  ax.set_xlabel("Day of the fortnight (day 1 = first Monday)")
  ax.set_ylabel("_______________________ (units)")  # what is y, in what units?

  fig.savefig("_____________.png", dpi=120, bbox_inches="tight")
  print("saved")
  ```

  Filling in four strings is a complete, honest version of this lesson.
- Skip the "what it does not tell you" sentence for two of the three charts. One is enough to hit objective 5.

### Variation — harder

1. **Write the function.** They have had `def` since Week 10. Turn the repeated six lines into one function that takes the x values, the y values and four strings, and call it three times. The Answer Key page 25.4 has the model version.
2. **Two decimal places on the axis.** Chart `sleep_hours` and notice that the y-axis ticks come out as 7.0, 7.5, 8.0 — matplotlib chose those. Ask: "who picked those numbers, and could they mislead anybody?" That is a soft, honest opening onto Week 27 with no new syntax.
3. **Count your own markers.** "How many dots should be on each chart? Count them in the PNG. If you get nine, what happened?" (A dropped row, or a list one item short. It is also how you would notice a missing day.)
4. **The naked-chart challenge, in reverse.** Take one of their finished charts and produce a *deliberately* stripped version with no title and no labels. Print both. Show them to somebody else in the house and ask what each one means. Bring back the answer. This is the Hook, run by the student, on a real person.

---

## 🐞 The Debugging Clinic

Every message below was produced by running a genuinely broken version of this week's code. The line numbers will differ on the student's machine; the last line will not.

| What the student sees (real message) | What it means | Most likely cause | The fix |
|---|---|---|---|
| `AttributeError: 'Axes' object has no attribute 'set_xlable'. Did you mean: 'set_xlabel'?` | "I asked the frame to do a thing it has never heard of." | Typo. `set_xlable` for `set_xlabel`. Also common: `set_xLabel`, `set_x_label`, `setxlabel`. | Fix the spelling. Python's own suggestion is right here — read it. |
| `ValueError: x and y must have same first dimension, but have shapes (12,) and (11,)` | "You gave me twelve x values and eleven y values. I cannot pair them up." | A number was dropped from one of the two lists, usually while reformatting it across two lines. | `print(len(weeks), len(visits))` and find the short one. This is exactly why the seatbelt prints are in the file. |
| `AttributeError: 'tuple' object has no attribute 'plot'` | "The thing you called `ax` is a *pair* of things, not a frame." | `ax = plt.subplots(...)` instead of `fig, ax = plt.subplots(...)`. One name on the left instead of two. | Add `fig, ` in front of `ax`. |
| `NameError: name 'plt' is not defined` | "You used a name I have never been told about." | The `import matplotlib.pyplot as plt` line is missing, or is below the code that uses it, or says `pyplot` without `as plt`. | Put `import matplotlib.pyplot as plt` on the first line of the file. |
| `ModuleNotFoundError: No module named 'matplotlib.pyplt'` | "There is no such part of matplotlib." | `pyplt` instead of `pyplot`. If it says `No module named 'matplotlib'` with nothing after it, the library is not installed *in the Python you are running* — see Orientation §4.7. | Fix the spelling, or activate the venv, or select the `.venv` interpreter in VS Code. |
| `TypeError: Figure.savefig() missing 1 required positional argument: 'fname'` | "You asked me to save, but not what to call it." | `fig.savefig(dpi=120)` — the filename was left out, usually while deleting and retyping. | `fig.savefig("visits.png", dpi=120, bbox_inches="tight")`. |
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` pointing at `visits = [118 126, 131]` | "I cannot even read this line, let alone run it." | A missing comma between two list items. Python's guess is correct. | Add the comma. Note the caret `^^^^^^^` under the exact spot. |
| `ValueError: Unrecognized marker style '0'` (after about fifteen lines of matplotlib internals) | "'0' is not a shape I know how to draw." | `marker="0"` — the digit zero instead of the letter o. Genuinely hard to see on most fonts. | `marker="o"`. Lowercase letter o. |
| `SyntaxError: invalid syntax` pointing at `ax.set_title "Library visits"` | "You named a thing and then put a string next to it. That is not a sentence I understand." | Missing brackets on a method call. | `ax.set_title("Library visits")`. |
| `AttributeError: Text.set() got an unexpected keyword argument 'figsize'` | "The title does not have a size-in-inches. The figure does." | `figsize=` given to `set_title` instead of to `subplots`. A copy-paste that landed one line too low. | Move `figsize=(6, 4)` into `plt.subplots(...)`. |
| `UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.` | "This computer has no window system, so I cannot pop a window. Carrying on." | `plt.show()` on a machine with no display. **It is a warning, not an error.** The program finished. | Nothing is broken. Use `fig.savefig(...)`. Delete `plt.show()`. |
| **No error, no output, no file.** | Nothing. The program did exactly what it was told. | There is no `savefig` and no `show`. Or `savefig` ran but you are looking in a different folder. | Add `fig.savefig(...)` and a `print("saved ...")`. Then `ls` / `dir` to prove it. |

### How to teach debugging without giving the answer

The escalation ladder from Orientation §8.2, applied to this week:

1. **"Read me the last line."** Out loud. Not the whole wall of red — the bottom line. Four seconds, and half the time they fix it themselves before they finish the sentence.
2. **"What line number does it name?"** Have them count to it in the editor. Do not point.
3. **"What did you *expect* that line to do?"** The gap between the expectation and the message is the bug, and they usually hear it themselves as they describe it.
4. **"Print the thing just before it breaks."** `print(len(weeks), len(visits))`, `print(type(ax))`. A print is always allowed and always cheap.
5. **Only now:** narrow it. "Look at the spelling of the word `label`." Still not the fix — the *location* of the fix.

And the one rule that matters more than the ladder: **do not touch the keyboard.** If you type it, they learn that errors are things adults make go away.

---

## ❓ Questions Students Ask This Week

**"Why is it called `axes` if it's a box?"**

Because in 2003 somebody named it after the thing you can see — the two axis lines — rather than the thing it actually is. It stuck, and now millions of lines of code depend on the name, so it will never be changed. It is a genuine wart. The useful mental move is to hear "axes" and think "**one drawing frame**", and to notice that the frame *contains* an x axis and a y axis. The word will stop bothering them in about a fortnight.

**"Can't I just use `plt.plot()` instead? It's shorter."**

You can, and half the internet does. `plt.plot(...)`, `plt.title(...)` works and it is two words shorter. Here is why we are not using it: `plt.plot` draws on "whichever frame is current", and it never tells you which one that is. With one chart, that is fine. With two charts side by side — which is Week 27 — it becomes a guessing game, and people lose whole evenings to charts landing on top of each other. `ax.plot` always says *which frame*, out loud, in the line itself. Learning the slightly longer one first means never having to unlearn the short one.

**"Do I have to type `bbox_inches="tight"` every single time?"**

Every time, yes, and it is worth understanding what it buys. Without it, matplotlib saves a fixed 6 × 4 inch rectangle, and a long axis label can run off the bottom of that rectangle and simply be missing from the file. With it, matplotlib measures where your labels actually ended up and crops to fit them. Since the whole point of this week is that the labels are the chart, losing half of one is not a small problem. Sixteen extra characters.

**"What's dpi? Why 120?"**

Dots per inch — how many pixels matplotlib packs into each inch of the sheet. Your sheet is 6 inches wide, so `dpi=120` gives a file 720 pixels across. `dpi=300` gives 1800 pixels before cropping: sharper, good for printing, about six times as many pixels in total. 120 is chosen because it looks crisp on a screen and the files stay small enough to email. Nothing magic about it. Try 40 once to see what "too low" looks like — it is instructive.

**"My chart is ugly. How do I make it look nice?"**

Honest answer: you mostly do not, this year, and it matters much less than you think. A plain matplotlib chart with a real title and units on both axes is more useful than a beautiful one without them. The two things that genuinely improve a chart are both free: **write a better title**, and **put the units in**. If they still want to fiddle, `color="darkorange"` inside `ax.plot(...)` works and takes three seconds. Then get back to the labels.

**"Should the y axis always start at zero?"** *(This one is genuinely contested. Say so.)*

**Nobody fully agrees, and here is why it is not a dodge.** For a **bar** chart the answer really is yes, always, and Week 27 will show you exactly what happens when it does not — because a bar asks your eye to compare *lengths*, and chopping the bottom off every bar deletes length that the reader has no way to add back.

For a **line** chart it is a real argument among people who do this for a living. A line asks you to follow a *shape*, not compare lengths. A chart of body temperature over a week that started at zero would be a flat line pressed against the top of the frame, telling you nothing, and 0 °C is not a meaningful floor for a human body anyway. But a chart of a company's monthly income starting at 95% of its maximum will make an ordinary month look like a crisis, and that is done on purpose all the time.

The rule most careful people end up with: *does the value zero mean anything for this quantity, and is the reader comparing lengths or following a shape?* Two people can apply that honestly and still disagree. What everybody agrees on is the second half: **if you do not start at zero, say so, loudly, in the label.** Something like `"Temperature (°C) — note: axis starts at 20"`. Hiding it is the dishonest part, not the choice itself.

**"Why do we save a picture instead of just looking at it?"**

Three reasons and they are all practical. A file can be opened again tomorrow; a window cannot. A file can be handed in, printed, or put in a project; a window cannot. And a file works on a computer with no screen at all — which is most of the computers in the world, and all of the ones that run real data jobs overnight. Looking at a window is a nice bonus. The file is the work.

---

## ⚠️ Where This Lesson Goes Wrong

| What happens | Why | What to do right now |
|---|---|---|
| The program runs, no error, no picture — and the student concludes Python is broken | This is the single most likely failure of the week, and it *feels* like a crash even though it is a success | Do not explain. Ask: **"Where is the file?"** Then run `ls` (or `dir`) together and look. The absence of the file is the lesson. Then ask: "What did you not tell it to do?" |
| Three charts all overwrite one file, because `savefig` was never renamed | Copying the first file is the sensible move, and the filename is the one string that does not look like it needs changing | Say **"show me your three files"** and let the folder listing do the teaching. Do not point at the line. |
| `plt.show()` opens a window and the terminal appears frozen | It is not frozen; the program is waiting for the window to close | Close the window. Then delete `plt.show()`. Say: "It was waiting for you. That's why we save instead." |
| The title says "visits vs week" and it gets waved through | It looks like a title, it has the right words in it, and it took two seconds | Hold the line every time, with one question: *"Could that title sit on top of any chart of this data?"* If yes, it goes back. This is the habit of the week and it is worth being tedious about. |
| Axis labels appear with no units — "Score", "Minutes", "Steps" | The quantity name feels like enough | Write the bare number on paper: `Score: 8`. Ask "good or bad?" Then write `Score: 8 out of 10`, then `Score: 8 out of 100`. Ten seconds, permanent cure. |
| `marker="o"` gets dropped because it "doesn't do anything" | With twelve close-together points, the dots genuinely look like decoration | Show Figure 25.3 again and ask which of the three panels they would trust. Then: "You cannot tell them apart without the dots. That is the whole reason." |
| The student edits the *first* chart over and over instead of making three | Iterating on one thing feels like progress | Make it physical: three separate files, three separate names, written on the workbook page **before** any code is typed. |
| Half the lesson disappears into colours, fonts and line styles | It is genuinely fun, and it is instantly rewarding | Give them one: `color="darkorange"`. Then: "That is the only styling we're doing today, because none of it makes a chart *say* anything. We're doing the part that does." Offer the whole rabbit hole as an at-home extra. |
| A student mixes up `fig` and `ax` repeatedly and gets frustrated | The names are short, similar, and both new in the same line | Write two labels on paper — SHEET and FRAME — and put them beside the screen. Point at them, physically, each time. Two lessons of pointing and it sticks. |

---

## 🧭 Differentiation

### If the student is struggling

**Cut:** one chart instead of three. Cut the `myweek` DataFrame entirely and use two typed-in lists — `days = [1, 2, 3, 4, 5]` and `minutes = [30, 45, 20, 60, 15]`. Every objective is reachable with five numbers.

**Reteach:** the sticking point is nearly always `fig, ax = plt.subplots(...)`, because it is the only two-names-one-equals line in the year. Do it away from the keyboard. Take two sheets of paper. Label one SHEET and one FRAME. Hand them both at once and say: "That's what that line does. It hands you two things, so you catch them in two boxes." Then have them draw on the frame and write on the frame, and *save the sheet*. Physical, ninety seconds, and it usually settles it for good.

**Copy-this-exactly scaffold** — this file works on its own with nothing else in the folder:

```python
# week25_scaffold.py -- copy this exactly. Then change only the five words in CAPITALS.
import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5]
minutes = [30, 45, 20, 60, 15]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(days, minutes, marker="o")

ax.set_title("MY TITLE SAYING WHAT I FOUND")
ax.set_xlabel("Day of the week (day 1 = Monday)")
ax.set_ylabel("MY QUANTITY (MY UNITS)")

fig.savefig("myfirstchart.png", dpi=120, bbox_inches="tight")
print("saved myfirstchart.png")
```

```text
saved myfirstchart.png
```

**Reduce:** accept a title that states the finding in the student's own words, however clumsy. "It went up a lot on Thursday" is a finding. "Minutes vs day" is not. That distinction is the objective; polish is not.

**One thing you must not cut:** objective 5. Even if no code runs at all, the Hook plus the "what it does not tell you" sentence is a complete and genuinely valuable lesson.

### If the student is flying

Extensions that need no new syntax at all:

1. **Write the function.** They have had `def` since Week 10. Six repeated lines become one function with six parameters, called three times. See the Answer Key for page 25.4. Then ask the real question: "You've written this function once. Which week are you going to `import` it in?" (The answer is the capstone.)
2. **Chart every number column in the table, in a loop.** They have had `for` since Week 7 and lists of strings since Week 11. `for column in ["homework_min", "screen_min", "steps"]:` and build a filename with an f-string from Week 3. Four charts from one loop and no new syntax.
3. **Interrogate a chart in the wild.** Find any chart — a newspaper, a cereal box, a phone battery screen — and write down five things it does not tell you. Then write the axis labels it *should* have had. This is objective 5 at full strength and it is harder than it sounds.
4. **The count-the-dots audit.** "Your chart should have ten dots. Count them in the PNG. Now break it on purpose: delete one number from one list, run it, and read the error." They produce the `ValueError` themselves, deliberately, which is the best possible way to meet it.
5. **Ask the Week 27 question early.** "What would happen to this chart if the y axis started at 100 instead of 0?" Do not answer it. Write their name and today's date next to the question and tell them it is the whole of Week 27.

### If the student won't engage today

Do the Hook, and only the Hook, and do it properly.

The naked-chart conversation is a complete, satisfying ten-minute lesson with no computer in it. Then turn it into a game: **"What Is This A Chart Of?"** You draw a shape on paper — a rising line, a falling line, a hump, a U, a flat line with one spike — and they invent three completely different things it could be a chart of, one of which must be alarming. Best of five. Then swap: they draw, you invent.

That game delivers objective 5 in full and takes ten minutes, and it makes the *point* of the whole week — that the shape is not the meaning — land harder than the code does. The code is not going anywhere; matplotlib will still be installed tomorrow.

---

## ✅ Assessing Understanding

Three checks, five minutes, exact wording.

**Check 1 — figure vs axes (spoken)**

> "I want two graphs side by side on one picture. How many figures do I need, and how many axes?"

*Good answer:* One figure, two axes. Full marks for "one sheet, two frames" — the words matter less than the split. **What to catch:** "two figures" means the sheet/frame idea has not landed. Go back to the two labelled sheets of paper; do not just repeat the definition.

**Check 2 — the silent success (spoken)**

> "My program ran. No red text, no error, and no picture appeared anywhere. What's the first thing you'd check?"

*Good answer:* "Whether there's a `savefig` line" — or "look in the folder for the file". Both are full marks. **What to catch:** "the code is broken" or "reinstall matplotlib". Reply: "It ran perfectly. It did exactly what you told it. What didn't you tell it?"

**Check 3 — what a chart does not say (written, 60 seconds)**

> "Here's a chart with a line going up and nothing else on it. Write down three things it does not tell you. Three separate things."

*Good answer:* any three of — what the quantity is; what the units are; what the x axis measures; over what period; how many real measurements; how big the numbers actually are; whose data it is. **What to catch:** one vague answer ("it's confusing") instead of three specific absences. Prompt once: "Not *how* it's confusing. What *specific fact* is missing?"

### Mastery scale for this week

| Level | What it looks like |
|---|---|
| **1 — Not yet** | Cannot get a chart onto disk without line-by-line help. Thinks "no error" means it worked. Cannot say what a figure is. |
| **2 — Emerging** | Produces a saved chart from a scaffold. Adds a title when reminded. Axis labels present but without units. Still confuses `fig` and `ax`. |
| **3 — Secure** | Types `fig, ax = plt.subplots(figsize=(6, 4))` unaided and can say what both names hold. Produces a fully labelled saved chart with units in both axis labels and markers on. Reads a traceback's last line first. **This is the target.** |
| **4 — Strong** | Writes a title that states a finding without being asked. Diagnoses "no error, no picture" without help. Can state four specific things an unlabelled chart fails to say. Explains why markers matter. |
| **5 — Exceptional** | Wraps the six chart lines in a function and reuses it. Notices unprompted that where the y axis starts could change what the chart appears to say. Interrogates a chart found in the wild and rewrites its labels. |

---

## 📤 Homework to Assign

**Say this:**

> "Three pages, about an hour.
>
> **First, page 25.3 — read the errors.** Four real error messages, copied off a real screen. For each one: write what Python is trying to tell you in your own plain words, and write the one thing you'd change. Not 'fix the typo'. Which typo, in which word.
>
> **Second, page 25.4 — the three charts.** This is the main job. Three line charts from your own Week 21 table, each one saved as its own PNG with its own name. Every chart needs a title that says what you *found*, both axis labels with the units in brackets, and markers on every real point. And under each one, two sentences: one saying what it shows, one saying what it does **not** tell you. That second sentence is the one I'm going to read first.
>
> **Third, page 25.6 — interrogate a naked chart.** There's an unlabelled chart printed on the page. List five things it does not tell you, then write out the exact five lines of Python that would fix it.
>
> And one instruction that isn't on any page: **open all three of your PNGs and look at them.** A chart you haven't looked at isn't finished. I will ask."

**Workbook pages:** 25.1, 25.2 and 25.5 in class; **25.3, 25.4, 25.6** at home.

**Expected time:** 12 min for the error reading · 35 min for the three charts · 12 min for the naked-chart interrogation. About 60 minutes.

---

## 🔑 Answer Key

### Page 25.1 — Name the parts

| # | Blank | Answer |
|---|---|---|
| (a) | The whole picture, the thing that becomes a `.png` | **figure** |
| (b) | One drawing frame inside it, with its own title and axes | **axes** |
| (c) | The call that hands you both at once | `plt.subplots()` |
| (d) | The call that draws the data inside the frame | `ax.plot()` |
| (e) | The dot placed on every real measurement | **marker** |
| (f) | The call that writes the picture to a file | `fig.savefig()` |
| (g) | The sentence at the top that states the finding | **title** |
| (h) | The words on the bottom and the side, which must include the units | **axis labels** |

**25.1(i) Why is a title different from an axis label?**
A title says **what you found** — the conclusion. An axis label says **what was measured, and in what units** — the ingredients. A chart can have perfect axis labels and a useless title, or the reverse, and both are broken in different ways.

**25.1(j) Why does saving belong to `fig` and titling belong to `ax`?**
Because you save the whole sheet of paper but you title one drawing on it. If a sheet held two graphs, you would need two titles and still only one file.

### Page 25.2 — Predict, then run

Six fragments. Write the prediction first, in pen, before running anything.

| # | Fragment | What actually happens | Why |
|---|---|---|---|
| (a) | `fig, ax = plt.subplots(figsize=(6, 4))` then `ax.plot([1,2,3],[4,5,6])` and nothing else | **Nothing.** No output, no error, no file. | The chart exists in memory. Nobody asked for it. |
| (b) | The same, plus `fig.savefig("a.png", dpi=120, bbox_inches="tight")` | A file `a.png` appears in the folder. Still no terminal output. | `savefig` writes the file silently. Add a `print` if you want to be told. |
| (c) | `ax = plt.subplots(figsize=(6, 4))` then `ax.plot([1,2],[3,4])` | `AttributeError: 'tuple' object has no attribute 'plot'` | One name caught two things, so `ax` holds the pair, not the frame. |
| (d) | `ax.plot([1,2,3,4],[10,20,30])` | `ValueError: x and y must have same first dimension, but have shapes (4,) and (3,)` | Four x values, three y values. They cannot be paired. |
| (e) | `fig.savefig("chart", dpi=120, bbox_inches="tight")` (no extension) | A file called **`chart.png`** appears. No error, no warning. | matplotlib falls back to PNG when no extension is given. It works, and it teaches you nothing, so write the `.png`. |
| (f) | `ax.plot([1,2,3],[4,5,6], marker="0")` | `ValueError: Unrecognized marker style '0'` after about fifteen lines of matplotlib internals | Digit zero instead of letter o. |

**25.2(g) Which of (a)–(f) produced no error but was still wrong?**
(a). It ran perfectly and produced nothing at all. **A silent success is not a success.**

### Page 25.3 — Read the error (homework)

| # | The message | What Python is telling you | The one thing to change |
|---|---|---|---|
| 1 | `AttributeError: 'Axes' object has no attribute 'set_xlable'. Did you mean: 'set_xlabel'?` | "I asked the drawing frame to do something called `set_xlable`, and it has never heard of that." | Spell it `set_xlabel` — l-a-b-e-l, not l-a-b-l-e. Python guessed it for you. |
| 2 | `ValueError: x and y must have same first dimension, but have shapes (12,) and (11,)` | "You handed me 12 x values and 11 y values, and I cannot pair them up." | Find the list with 11 items and put the missing number back. `print(len(weeks), len(visits))` finds it in one line. |
| 3 | `NameError: name 'plt' is not defined` | "You used a name I have never been told about." | Put `import matplotlib.pyplot as plt` at the top of the file, above everything that uses it. |
| 4 | `TypeError: Figure.savefig() missing 1 required positional argument: 'fname'` | "You asked me to save, but you never said what to call the file." | `fig.savefig("visits.png", dpi=120, bbox_inches="tight")` — the filename goes first. |

**25.3(e) Which line of a traceback do you read first, and why?**
The **last** line. It names the kind of error and what went wrong. Everything above it is the route Python took to get there, which matters only once you know what broke.

**25.3(f) One of these four is not really an error message at all. Which, and what is it?**
None of these four — but the `UserWarning` about the `agg` backend, which you met in the lesson, is a **warning**. The program did not stop; it finished. It is telling you the computer has no window system. The correct response is to save the file, not to fix anything.

### Page 25.4 — Three labelled line charts (homework)

Marked on structure, not on whose week it is. If the student's Week 21 table is lost, this is the fallback used throughout:

```python
# myweek.py -- the Week 21 DataFrame: ten days of my own life, typed in by hand.
import pandas as pd

def build_my_week():
    """Return the 10-row 'my own week' table from Week 21."""
    return pd.DataFrame({
        "day":          [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "day_name":     ["Mon", "Tue", "Wed", "Thu", "Fri",
                         "Sat", "Sun", "Mon", "Tue", "Wed"],
        "homework_min": [45, 60, 30, 75, 20, 0, 90, 55, 65, 40],
        "screen_min":   [60, 45, 90, 30, 120, 180, 75, 50, 40, 85],
        "sleep_hours":  [8.0, 7.5, 8.5, 7.0, 9.0, 9.5, 8.0, 7.5, 8.0, 8.5],
        "steps":        [6200, 7100, 5800, 8400, 6900, 11200, 4300, 7600, 8100, 6500],
    })

if __name__ == "__main__":
    df = build_my_week()
    print(df.shape)
    print(df)
```

```text
(10, 6)
   day day_name  homework_min  screen_min  sleep_hours  steps
0    1      Mon            45          60          8.0   6200
1    2      Tue            60          45          7.5   7100
2    3      Wed            30          90          8.5   5800
3    4      Thu            75          30          7.0   8400
4    5      Fri            20         120          9.0   6900
5    6      Sat             0         180          9.5  11200
6    7      Sun            90          75          8.0   4300
7    8      Mon            55          50          7.5   7600
8    9      Tue            65          40          8.0   8100
9   10      Wed            40          85          8.5   6500
```

**The full model answer.** Three separate files is perfectly acceptable. This single-file version uses the Week 10 function skill, and it is what a "flying" student should end up with:

```python
# week25_myweek_charts.py -- three labelled line charts from my Week 21 table.
import matplotlib.pyplot as plt
from myweek import build_my_week            # my own 10-row table, from Week 21

df = build_my_week()
print(df.shape)

def line_chart(x, y, title, xlabel, ylabel, filename):
    """Draw ONE fully labelled line chart and save it to filename."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, marker="o")               # a dot on every real day
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.savefig(filename, dpi=120, bbox_inches="tight")
    print("saved", filename)

DAY_LABEL = "Day of the fortnight (day 1 = first Monday)"

line_chart(df["day"], df["homework_min"],
           "Homework peaked at 90 minutes on day 7",
           DAY_LABEL, "Homework done (minutes)", "myweek_homework.png")

line_chart(df["day"], df["screen_min"],
           "Screen time hit 180 minutes on day 6, then dropped back",
           DAY_LABEL, "Screen time (minutes)", "myweek_screen.png")

line_chart(df["day"], df["steps"],
           "Day 6 was my only day over 10,000 steps",
           DAY_LABEL, "Steps walked (count)", "myweek_steps.png")

print("homework mean:", round(df["homework_min"].mean(), 1))
print("screen  max  :", df["screen_min"].max())
print("steps   max  :", df["steps"].max())
```

```text
(10, 6)
saved myweek_homework.png
saved myweek_screen.png
saved myweek_steps.png
homework mean: 48.0
screen  max  : 180
steps   max  : 11200
```

**Marking the six sentences.** One "what it shows" and one "what it does not tell you" per chart. The second one is where the marks are.

| Chart | What it shows | What it does **not** tell you |
|---|---|---|
| `myweek_homework.png` | Homework climbed to 90 minutes on day 7, straight after a day with none at all. | Which subject, whether any of it was finished, or whether day 7 was catch-up for day 6. Also: ten days is not a habit, it is a fortnight. |
| `myweek_screen.png` | Screen time hit 180 minutes on day 6 — the Saturday, its highest of the fortnight — then dropped back to school-day levels. | What was *on* the screen. Homework research, a film and a group chat are all identical on this chart. |
| `myweek_steps.png` | Day 6 was the only day over 10,000 steps; day 7 was the lowest of the fortnight at 4,300. | Whether the tracker was worn all day, what counted as a step, or whether a bike ride got logged as walking. |

**25.4(a) Why do all three charts have the same x axis label?**
Because all three are the same ten days. The x axis has not changed; only what is being measured up the side has. Reusing the label in a variable (`DAY_LABEL`) also means a typo can only happen once.

**25.4(b) You wrote three `savefig` lines. What happens if two of them use the same filename?**
The second one silently overwrites the first. No error, no warning, `saved` printed twice, and one file where there should be two. Check the folder, not the terminal.

**25.4(c) Could you draw a line chart with `day_name` on the x axis instead of `day`?**
matplotlib will draw it, but you should not, for two reasons. `day_name` is text, not a number, so "halfway between Mon and Tue" is meaningless — and worse, `Mon`, `Tue` and `Wed` each appear twice in ten days, so the chart would put day 1 and day 8 in the same place. A line chart needs an x axis that is **ordered and unique**. `day` is both.

### Page 25.5 — Caption clinic

Rewrite each weak title as a finding.

| # | Weak title | A title that states the finding |
|---|---|---|
| (a) | "Visits vs week" | "Library visits climbed 60% over one term" |
| (b) | "Homework data" | "Homework peaked at 90 minutes on day 7" |
| (c) | "Steps" | "Day 6 was the only day over 10,000 steps" |
| (d) | "Screen time chart" | "Screen time trebled at the weekend, then dropped back" |
| (e) | "Graph of sleep hours by day" | "I slept least on the two days I did the most homework" |

**The test to apply to all five:** could this title sit, unchanged, on top of *any* chart of the same data? If yes, it names the ingredients instead of the finding, and it goes back.

**25.5(f) Fix these three axis labels.**

| Weak | Fixed | What was missing |
|---|---|---|
| `Score` | `Score (points out of 100)` | The scale. 8 could be excellent or terrible. |
| `Time` | `Homework done (minutes)` | Both the quantity *and* the units. "Time" could be a clock reading. |
| `Distance` | `Distance to school (km)` | The units, and which distance. |

### Page 25.6 — Interrogate a naked chart (homework)

**Five things the printed chart does not tell you.** Any five of these earn full marks; the answer must be a *specific absence*, not "it's confusing".

1. **What is being measured.** Money, rainfall, people, pizzas — nothing on the chart says.
2. **The units.** Even if you knew it was money, is it rupees or thousands of rupees?
3. **What the x axis is.** Days, weeks, months, years, or something not time at all.
4. **Over what period.** A rise over ten days and a rise over ten years are different claims.
5. **How many real measurements it came from.** With no markers, four points and four hundred look identical.
6. **How big the numbers actually are.** There are no tick numbers, so a rise from 2 to 3 and a rise from 2,000 to 3,000 look the same.
7. **Whose data it is, and who drew it.** Every chart is somebody's argument.

**The five lines of Python that would fix it.** Any sensible quantity is fine; the *shape* of the answer is what is being marked.

```python
# week25_fix_the_naked_chart.py
import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4, 5, 6, 7, 8]
visits = [118, 131, 126, 152, 166, 158, 174, 189]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(weeks, visits, marker="o")                       # 1. markers on every point
ax.set_title("Library visits rose 60% over eight weeks")  # 2. the finding
ax.set_xlabel("School week (week 1 = start of term)")     # 3. what x is, with units
ax.set_ylabel("Visits per week (count of people)")        # 4. what y is, with units
fig.savefig("fixed.png", dpi=120, bbox_inches="tight")    # 5. save it so it exists
print("saved fixed.png")
```

```text
saved fixed.png
```

**25.6(a) Which of your five fixes would you make first, if you could only make one?**
The **y axis label with units**. Without it you do not know what the chart is *about*, and every other label is describing something unnamed. (A defensible alternative answer: the title, because a good title implies the quantity. Accept either if the reason is argued.)

**25.6(b) The chart on this page has no numbers on either axis. Is that worse than having no title?**
Different, and arguably worse. A missing title costs you the *conclusion*, which a careful reader can sometimes work out. Missing numbers cost you the *scale*, which nobody can recover — a doubling and a rise of two look identical, and there is no way to tell from the picture which one you are being shown.

### Lesson questions posed in the Say-this scripts

- *"Write one true sentence this chart proves."* → "It went up." And then nothing else is available, because nothing else is on the paper.
- *"What went up?"* → You cannot know. Pizzas, rainfall and flu cases all fit that line exactly.
- *"How many measurements is it drawn from?"* → Unknowable without markers. That is what `marker="o"` is for.
- *"Two graphs on one sheet — how many titles, how many files?"* → Two titles (one per axes), one file (one figure).
- *"Which is the figure — the file or the box?"* → The file. The box is the axes.
- *"What's wrong with `Score` as a y-axis label?"* → No units. Out of 10, out of 100, or a percentage — the reader has to guess.
- *"Why put a dot on every point?"* → So the reader can see how many real measurements there were, and therefore how much to trust the line.
- *"My program ran, no error, no picture. What went wrong?"* → Nothing. It did exactly what it was told. It was never told to save or to show.
- *"What do you think will happen when we run step 2?"* → Nothing at all. No chart, no error. The figure exists only in memory.
- *"Why `fig.savefig` and not `ax.savefig`?"* → You save the whole sheet of paper, not one drawing on it.
- *"Was the code broken, when it ran three times with no picture?"* → No. Obedient is not the same as correct.

---

## 🔮 Next Week Preview

Week 26 stops asking *how* to draw and starts asking *which shape to draw*. There are only a handful of question shapes in the world — how did something change over time, which category is biggest, how spread out are the values, do two numbers move together — and each one has exactly one chart that answers it well and several that answer it badly. The week opens with eight question cards face down on the table, and the student has to pick the chart shape from the question *before* touching a keyboard, which turns out to be the hard part. Then the sting: a column whose average is 62 turns out to be two separate clumps, one at 39 and one at 85, with not one single person anywhere near 62 — and the average, which is a perfectly correct number, was hiding it in plain sight. The histogram is what catches that, and it catches it in half a second.

**Prep early:** three things. First, **keep this week's `visits.png` and the three `myweek` PNGs** — Week 26 puts them next to the new shapes and asks which questions each one can and cannot answer. Second, **find the student's cleaned table from Week 24** (the 38-row Mess Detective result); if it has gone missing, the full typed-out version is in the Week 26 Answer Key and takes two minutes to drop into the folder. Third, **cut out the eight question cards** from workbook page 26.1 the night before — the activity depends on them being face down and genuinely unknown, and cutting them up in front of the student wastes four good minutes.

---

[⬅ Week 24](week-24.md) · [Course Home](../README.md) · [Week 26 ➡](week-26.md) · [Student Guide](../student-guide/week-25.md) · [Workbook](../workbook/week-25.md) · [Orientation](00-orientation.md) · [Glossary](../../glossary.md)
