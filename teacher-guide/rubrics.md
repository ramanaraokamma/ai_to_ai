```
  ██████╗ ██╗   ██╗██████╗ ██████╗ ██╗ ██████╗███████╗
  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██║██╔════╝██╔════╝
  ██████╔╝██║   ██║██████╔╝██████╔╝██║██║     ███████╗
  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██║██║     ╚════██║
  ██║  ██║╚██████╔╝██████╔╝██║  ██║██║╚██████╗███████║
  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝
```

# 📏 AI Academy — Reusable Rubrics

### *Four rubrics you will use ~44 times. Every descriptor is something you can see, not something you have to feel.*

**Companion to:** [`README.md`](README.md) (teaching guide) · [`pacing-guide.md`](pacing-guide.md) · [`progress-tracker.md`](progress-tracker.md)

[⬅ Teacher guide](README.md) · [Back to AI Academy](../README.md) · [Curriculum map](../CURRICULUM_MAP.md)

---

## 🪝 Why These Exist

A learner shows you a notebook. It has charts. The model scored 0.91. They're pleased.

Without a rubric you will say "nice work," because that is the kind and available thing to say. With a rubric you will notice that there is no baseline, that the scaler was fitted before the split, that the cleaning log says *what* changed but never *why*, and that the "what I got wrong" section says "nothing really."

**A rubric is not for grading. It is for seeing.** Nobody in this course gets a report card. What they get is a specific, observable, non-personal statement of what exists in the work and what doesn't yet — which is the only feedback that changes anything.

---

## 🎯 How To Use Any Rubric In This File

### The four columns mean the same thing everywhere

| Column | What it means | The phrase to use out loud |
|---|---|---|
| 🌱 **Beginning** | The element is absent, or present in name only | *"This part isn't here yet."* |
| 🌿 **Developing** | Present but incomplete, inconsistent, or unexamined | *"It's here. It's not doing its job yet."* |
| 🌳 **Proficient** | ✅ **The target.** Done correctly and defensibly. | *"That's the standard. Well done."* |
| ✨ **Exceptional** | Goes beyond by being *more honest or more rigorous*, not by being bigger | *"You did something I wasn't expecting."* |

> **Proficient is the goal, not the middle.** Every learner should be aiming at 🌳 on every row. ✨ is not a stretch target to chase — it is what happens occasionally when someone gets genuinely curious. A project that is 🌳 on every row is an excellent project.

### The five rules of using them

1. **Score the artifact, never the person.** "The cleaning log has no reasons in it" — not "you were careless."
2. **Score with the learner, not about them.** Fill it in together, out loud. Ask "which column is this?" before you say it.
3. **Have them self-score first.** Then compare. **The gaps between their score and yours are the entire lesson** — especially the rows where they scored themselves *higher*.
4. **Pick two rows for next time.** Never more. A learner given nine improvements makes zero.
5. **🌱 means "not yet," and say it that way.** The distance between "this is Beginning" and "this isn't here yet" is the distance between a learner who continues and one who doesn't.

### Which rubric when

| You're looking at | Use |
|---|---|
| Any 🛠️ mini-project, any capstone | [Project rubric](#-rubric-1--the-project-rubric) |
| Anything the learner built with code or blocks | [Code-quality rubric](#-rubric-2--the-code-quality-rubric-per-level) for that level |
| "Explain this to me with the file closed" | [Conceptual-explanation rubric](#-rubric-3--the-conceptual-explanation-rubric) |
| A 🤔 Think Deeper answer, a bias report, a system card | [Ethics-reasoning rubric](#-rubric-4--the-ethics-reasoning-rubric) |
| A capstone | All four, plus the [capstone addendum](#-capstone-addendum--the-extra-rows) |

---

## 🛠️ Rubric 1 — The Project Rubric

**Use for:** all 36 mini-projects and all 4 capstones. Eight rows. Not every row applies to every project — mark N/A and move on (Level 1 Module 1's Spotter's Log has no model to evaluate).

### Row 1 — Problem framing

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Cannot say what the project is for beyond "the module said to" | States a topic ("something about cricket") but not a question or a decision | States the question in one sentence, names what is being predicted and from what, and says who would use the answer | States the question, names what a *wrong* answer would cost and to whom, and explains why this framing was chosen over a rejected alternative |

### Row 2 — Data honesty

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Cannot say where the data came from or how many rows there are | Knows the source and the size; has not looked for gaps, duplicates, or oddities | Reports source, size, collection method, and at least two known limitations; every cleaning change is logged **with a reason** | Names who is *missing* from the data and estimates the effect; identifies a way the collection method itself biased the result |

### Row 3 — Method correctness

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Test data was used in training, or there is no held-out set at all | A split exists but was made after scaling/fitting, or the same test set was reused while tuning | Split made before any fitting; preprocessing fitted on train only; the method matches the question (classification vs regression) | Uses a validation set (or cross-validation) for choices and touches test **once**; states explicitly what would have leaked if done otherwise |

### Row 4 — Evaluation

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Reports a number with no context, or reports the training score as the result | Reports test performance but with no baseline and no sense of whether it's good | Reports test performance **against a stated baseline** (majority class / random / previous version), with the metric justified by the question | Reports uncertainty (CV spread, error bars, or "n=40, so ±X"), and breaks the score out by subgroup or class |

### Row 5 — Failure analysis

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| No mistakes examined; "it works" | Says it makes mistakes but hasn't looked at which ones | Examines actual wrong predictions, names the pattern in them, and states a hypothesis for the cause | Constructs an input designed to break it, confirms the break, and explains the mechanism — not just the symptom |

### Row 6 — Communication

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Unlabelled charts, no narrative; reader cannot follow what happened | Everything is present but in the order it was made rather than the order it should be read | Reads as a story: question → data → method → result → limits. Every chart has axis labels, units and a title that states the finding | A reader who wasn't there can reproduce the result from the write-up alone; the hardest idea is explained without jargon |

### Row 7 — Human impact

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Not considered | A general statement ("AI can be biased") not tied to this project | Names a specific group this project could get wrong, states the consequence, and says what would need to change | Measures the disparity as a number, and states an honest condition under which they would not deploy it |

### Row 8 — Completion & craft

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Doesn't run / doesn't exist / stops halfway | Runs with manual intervention or only on the author's machine with hidden setup | Runs start to finish from a clean state; all success criteria in the module's checklist are ticked and true | Someone else ran it, unaided, and it worked — and the "level it up" extension is done |

### Scoring sheet

```
   ┌─────────────────────────────────────────────────────────────────────┐
   │  PROJECT: ______________________________  DATE: ____________        │
   │  LEVEL: ___  MODULE: ___                                            │
   ├─────────────────────────────────┬───────┬───────┬───────┬───────────┤
   │                                 │ 🌱 1  │ 🌿 2  │ 🌳 3  │  ✨ 4     │
   ├─────────────────────────────────┼───────┼───────┼───────┼───────────┤
   │  1. Problem framing             │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  2. Data honesty                │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  3. Method correctness          │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  4. Evaluation                  │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  5. Failure analysis            │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  6. Communication               │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  7. Human impact                │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   │  8. Completion & craft          │  [ ]  │  [ ]  │  [ ]  │   [ ]     │
   ├─────────────────────────────────┴───────┴───────┴───────┴───────────┤
   │  Two rows to move up next time:  ______________  ______________     │
   │  One thing that was genuinely good: _______________________________ │
   └─────────────────────────────────────────────────────────────────────┘
```

> ⚠️ **Row 3 is a gate, not a score.** If Method correctness is 🌱 — the test set was trained on — the project's headline number is meaningless and no other row can compensate. Fix that row and re-score. This is the one place where the rubric is pass/fail.

---

## 💻 Rubric 2 — The Code-Quality Rubric (per level)

Code quality means something different for an 11-year-old dragging Scratch blocks than for a 17-year-old shipping an agent. Four separate tables. **Use only the one for the level you're in** — holding a Level 2 learner to Level 4 standards is how you produce someone who is afraid to write code.

---

### 🧭 Level 1 — "Code" means unplugged procedures, spreadsheets, and Scratch blocks

| Dimension | 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|---|
| **Precision of instructions** | Steps are vague ("check if it's spam") — another person could not follow them | Steps are followable but ambiguous in places; the tester had to guess twice | A second person followed the rulebook/procedure and got the same answers the author did | The procedure states what to do in ambiguous cases *before* the tester meets one |
| **Spreadsheet correctness** | Formulas typed as text, or hard-coded numbers where a formula belongs | Formulas work in one cell but were retyped instead of filled; one or two are wrong | Formulas fill correctly across the range; a spot-check cell was verified by hand | Uses a named helper column to make the calculation readable, and explains why |
| **Scratch structure** | One long block stack; variables named `variable1` | Works, but repeated block sequences are copy-pasted three times | Named variables (`user_input`, `word_count`); repeated logic in a custom block or loop | The project handles an input the module never mentioned, gracefully |
| **Labelling & tidiness** | Nothing labelled; the author cannot re-find anything a week later | Some labels; inconsistent naming | Every column, class, sprite and file has a name that says what it is | A one-line "how to run this" note that a stranger could follow |
| **Reproducibility** | Cannot re-do the result; the model or sheet is gone | Could redo it with effort and some guessing | The saved `.tm` / `.sb3` / sheet exists, is named meaningfully, and reopens | A second run from saved files produced the same numbers, and this was checked |

---

### 🔨 Level 2 — Python: readable, working, and explainable line by line

| Dimension | 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|---|
| **It runs** | Crashes, or only works if you type the "right" input | Runs on the happy path; any unexpected input crashes it | Runs from a clean start; handles the obvious bad inputs the module names | Handles inputs the module didn't mention, with a helpful message rather than a traceback |
| **Names** | `x`, `a`, `thing`, `df2`, `temp3` | Mostly descriptive with a few mystery names left over | Every variable and function name says what it holds or does; no single letters except loop counters and standard maths (`i`, `k`, `x`, `y`) | Names make a comment unnecessary — `passed_students` instead of `students2 # the ones who passed` |
| **Functions** | Everything in one long top-level script | A couple of functions exist but still do three jobs each | Repeated logic lives in a function with parameters and a `return`; each function does one thing | Functions are importable and reused across files, exactly as `stats.py` is in Module 3 |
| **Comments** | None, or `# add one to x` above `x = x + 1` | Comments exist but describe *what* the line does, not why | Comments explain **why** — the choice, the unit, the gotcha. Level 2 modules ask for line-by-line commenting in mini-projects; this is met | A short docstring on each function saying what it takes and returns |
| **Correctness checking** | Assumes the output is right because it printed | Eyeballed the output; no independent check | At least one result verified by hand or against a known value (Module 3's median on even *and* odd lengths) | A small set of test cases with expected answers, run every time |
| **Data hygiene** | Test data used for training; scaler fitted on everything | Split exists but scaling/cleaning happened before it | Split first, then fit anything that learns from data; `random_state` set so results reproduce | Explains out loud what would have leaked, and can demonstrate the inflated score it would have produced |
| **Charts** | No axis labels; default title | Labelled but the chart type doesn't match the question | Every chart: title stating the finding, both axes labelled with units, legend if needed, y-axis starting at zero unless there's a stated reason | Saved with `savefig(dpi=120, bbox_inches="tight")` and readable when printed in black and white |

---

### ⚙️ Level 3 — Engineering: pipelines, artifacts, and code somebody else runs

| Dimension | 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|---|
| **Structure** | One notebook cell doing everything, run out of order | Script exists but training, evaluation and prediction are tangled together | Clear separation: data prep → `Pipeline` → train → evaluate → save. `predict.py` contains **zero** training code | Config constants at the top of the file; one function per stage; the whole thing runs with one command |
| **Pipeline discipline** | Preprocessing done in loose cells before the split | `Pipeline` used for the model but scaling done manually beforehand | All preprocessing inside `Pipeline`/`ColumnTransformer`, fitted on train only, saved with the model as one artifact | A deliberate leakage test exists — a check that fails loudly if preprocessing ever sees test rows |
| **Reproducibility** | Different result every run; nobody knows why | `random_state` on the split but not the model | Seeds set everywhere they matter; the artifact reloads in a **fresh process** and gives the identical prediction | Versioned model files (`model_v3.joblib`) with a note on what changed and what the score did |
| **Numerical care** | Shapes and dtypes never checked; errors met with random `.reshape()` | Shapes checked when something breaks | `.shape` printed at boundaries during development; float32/float64 conversions made deliberately at the edge | A numerical gradient check or an equivalent independent verification of the maths |
| **Error handling** | Silent failures; `except: pass` | Errors crash with the raw traceback | Predictable failures caught with a message that says what to do about it | Input validation at the boundary — bad rows rejected with the reason, not by exploding three functions later |
| **Documentation** | None | A README that says "run main.py" | A **model card**: intended use, training data, metrics (overall and by subgroup), known failure modes, out-of-scope uses | Plus a monitoring plan naming the exact number that would mean the model has gone stale |
| **Instrumentation** | Nothing logged | `print()` statements left in from debugging | Every prediction logged with its inputs, output and latency | Logs are structured (JSON lines) and queryable; p50/p95 latency reported from them |
| **Journal** | Not kept | Occasional entries with no detail | One dated entry per session: what broke, what you changed, what you now believe | Entries contain the *evidence* — the number before, the number after, the one thing changed |

---

### 🚀 Level 4 — Systems: agents, budgets, guardrails, and evidence

| Dimension | 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|---|
| **Tensor discipline** | Shape errors fixed by trying `.transpose()` until it stops complaining | Shapes checked at the end | Shapes stated in comments at every boundary (`# (B, T, C)`); a wrong shape is caught by an assert, not by silence | Hand-computed values verified against the implementation to 4+ decimal places |
| **Prompts as code** | Prompt edited in place, previous versions lost | Versions kept but compared by reading outputs | Prompts versioned in files; each version scored against a **frozen** test set with a programmatic scorer | Failure cases from production are added to the test set, and the old versions still run for regression |
| **Eval integrity** | No eval set; judgement by vibes | Eval set written after the system was built | Eval set frozen and committed **before** the system exists; test cases include the hard and the unanswerable | Judge agreement measured (Cohen's κ) and position bias tested by flipping the order |
| **Budget & limits** | No caps anywhere; cost unknown | Cost checked afterwards on the console | `MAX_ITERATIONS` and a `BudgetGuard` that raises **before** the call; cost per task measured from `usage`, not guessed | A cost regression check — the harness fails if a change makes the system 2× more expensive |
| **Safety boundaries** | Tools can touch anything the process can | Sandbox exists but path traversal is possible | Allowlisted tools, a sandbox directory with traversal guards, and a refusal path that fires even when the model insists | The system refuses correctly when a *retrieved document* issues the instruction, and there's a test proving it |
| **Grounding & citations** | Answers with no source | Sources listed but not tied to specific claims | Every claim cites its chunk; below the similarity threshold τ the system says "I don't know" | Refusal rate and recall@k are both reported, and the trade-off between them is discussed |
| **Traceability** | No log of what the system did | Final output logged | A full `trace.jsonl`: every decision, tool call, argument, result, and token count | The trace is sufficient to replay a failed run and find the exact step that went wrong |
| **Secrets** | Key hardcoded in a file or a notebook cell | Key in an env var but also in shell history / a screenshot | Env var only; never printed, never committed; a leaked key would be revoked immediately | `.gitignore` and a pre-commit check that refuses to commit anything matching a key pattern |
| **Honest documentation** | None | A README describing what it does | A **system card**: intended use, evals with numbers, limits, out-of-scope uses, red-team results | The last section is titled *"What this fails at, and who should not rely on it"* — and it is specific |

---

## 🧠 Rubric 3 — The Conceptual-Explanation Rubric

**Use for:** "explain it to me with the file closed." Run it at the end of every module, at every checkpoint week, and at every [level exit check](../CURRICULUM_MAP.md#-level-exit-checks). It takes four minutes and it is the highest-information assessment in this course.

**How to run it:** ask one question. Say nothing for the first 30 seconds of silence. Then use only these three prompts: *"Give me an example."* · *"What would break that?"* · *"Why does it work that way?"*

### Row 1 — Accuracy

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| The explanation is wrong, or is a memorised sentence with the meaning missing | Broadly right with one significant error, or right for the demo case and wrong in general | Correct, including the standard edge case; no misuse of terms | Correct, and volunteers the boundary of their own correctness ("this holds for balanced classes; with 1% positives it doesn't") |

### Row 2 — Grounding in a concrete example

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Definitions only; no example offered even when asked | Repeats the module's example verbatim, numbers included | Produces their **own** example, with their own numbers, unprompted | Produces two examples — one where the idea applies and one where it visibly fails |

### Row 3 — Causal depth ("why," not "what")

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Describes the steps without any mechanism ("you call fit and it learns") | Gives one level of why, then stops at "that's just how it works" | Explains the mechanism: what changes, what quantity drives the change, and in which direction | Connects the mechanism to a different one they already own ("this is the same chain rule as backprop, just over time steps") |

### Row 4 — Vocabulary

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Avoids the technical terms, or uses them as decoration in the wrong places | Uses the right terms but cannot unpack them when asked | Uses terms correctly **and** can immediately restate each in plain words | Chooses register deliberately — plain words for a beginner, precise terms for a peer — and knows why |

### Row 5 — Handling "what would break it?"

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| "Nothing, it works" | Names a failure only after being given a heavy hint | Names a realistic failure case and what the symptom would look like | Names a failure they personally hit, what the number was, and how they diagnosed it |

### Row 6 — Honesty about the edges

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Bluffs confidently past the edge of their knowledge | Goes quiet or changes the subject when it gets hard | Says "I don't know" cleanly and marks exactly where the knowledge stops | Says "I don't know" **and** states what they'd do to find out |

> 🔑 **Row 6 is the one that predicts everything else.** A learner who can say "I'm not sure past this point" at age 12 becomes an engineer people trust at 22. Praise it every single time it happens, especially when it's inconvenient.

### Ready-made prompts by level

| Level | Ask this |
|---|---|
| **1** | "Why is it cheating to test your model on the photos it trained on?" · "What is a pixel?" · "Where could a dataset be unfair to someone?" |
| **2** | "What does `train_test_split` actually do, and why does it exist?" · "Explain overfitting using your own numbers from the bake-off." · "Why does scaling matter for kNN but not for a decision tree?" |
| **3** | "Draw the supervised pipeline." · "Compute precision and recall from this matrix." · "What is a gradient, and why do we subtract it?" · "Why is backprop just the chain rule?" |
| **4** | "Draw a transformer block." · "Explain pretraining → SFT → RLHF in four sentences." · "Why does attention need `/√d_k`?" · "When is RAG the right answer and when is fine-tuning?" |

---

## ⚖️ Rubric 4 — The Ethics-Reasoning Rubric

**Use for:** 🤔 Think Deeper discussions, Level 1's fairness audit, Level 3's model card, Level 4's red-team report and system card, and the ethics paragraph every capstone requires.

> **What this rubric does NOT do:** it does not score whether the learner reached the "right" conclusion. There isn't one. It scores the **quality of the reasoning**, which is the only thing that transfers. A learner can land 🌳 on every row and disagree with you completely.

### Row 1 — Specificity

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Slogans: "AI can be biased," "privacy is important" | General category named ("it might be unfair to some groups") but no group and no mechanism | Names the specific group, the specific harm, and the specific decision that produces it | Traces the whole chain: this collection choice → this data gap → this error pattern → this person's outcome |

### Row 2 — Evidence

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Asserts harms with no evidence, or dismisses concerns with no evidence | Cites something heard or read, not checked | Uses a number from their **own** system — an accuracy gap, a refusal rate, a failing test case | Designs and runs a new measurement specifically to test the concern, and reports what it showed |

### Row 3 — Stakeholders

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Considers only the builder or only the user | Names two parties, usually "users" and "the company" | Names who benefits, who bears the cost, and who has no say but is affected anyway | Identifies a party nobody in the discussion had mentioned — and explains how they end up affected |

### Row 4 — Both sides

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| One position, held as obvious; the other side is treated as stupid | Acknowledges another view but only to knock it down with its weakest form | Can state the strongest version of the opposing case in a form its holders would accept | Identifies the real value conflict underneath (safety vs autonomy, accuracy vs privacy) rather than treating it as a factual dispute |

### Row 5 — Trade-offs and cost

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Proposes a fix with no cost ("just make it fair") | Acknowledges there's a cost but doesn't say what | States the trade-off concretely: what you give up, how much of it, and who pays | Quantifies the trade-off (recall drops 6 points to cut false alarms by half) and says which they'd choose and why |

### Row 6 — Action

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Concern noted; nothing follows from it | Vague intention ("I'd get more data") | A specific change they made or would make, and a way to check whether it worked | The change was **shipped, re-tested, and the result documented** — including if it didn't help |

### Row 7 — Self-application

| 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|
| Ethics is about other people's systems | Applies it to their own project only when told to | Applies it unprompted to their own work and finds a real problem in it | States a condition under which they would **not ship their own project** — and means it |

> ✨ **Row 7 Exceptional is the hardest thing in this entire rubric file.** Almost nobody does it. When a learner says "I don't think this should be used for X, even though it's mine, and here's the number that convinces me" — stop the session and tell them exactly what they just did.

### Ready-made prompts by level

| Level | Ask this |
|---|---|
| **1** | "Who is missing from your training photos?" · "If your model is wrong about someone, what happens to them?" · "Should your school use face recognition for attendance?" |
| **2** | "Whose data is this, and did they know?" · "Your model is wrong 1 time in 8. Who is that one?" · "Which chart here could someone use to mislead a reader?" |
| **3** | "Which is worse for your project — a false positive or a false negative? Show me the cost arithmetic." · "Which subgroup does your model do worst on, and by how much?" · "What would make you take this model out of service?" |
| **4** | "What's the strongest thing your system can be made to do that you didn't intend?" · "What does it do when it doesn't know? Prove it." · "If a retrieved document tells it to do something, does it?" · "Who should not rely on this?" |

---

## 🏆 Capstone Addendum — The Extra Rows

Capstones use the project rubric plus these. **Do not use these on mini-projects** — they will crush a two-hour build.

| Dimension | 🌱 Beginning | 🌿 Developing | 🌳 Proficient | ✨ Exceptional |
|---|---|---|---|---|
| **Independence** | Needed step-by-step direction throughout | Needed help at each milestone boundary | Made the design decisions themselves; asked for help on specifics, not on direction | Made a call the guide disagreed with, defended it with evidence, and turned out to be right |
| **Scope management** | Ran out of time with core pieces missing | Finished, but the last milestone is thin because early ones ate the time | Delivered every milestone; cut the right things when time got short, deliberately | Cut scope early and in writing, *before* it became a crisis, with the reason recorded |
| **Milestone discipline** | Built first, planned never | Milestones done out of order; evals written after the system | Milestones completed in order and gated — especially "eval harness before system" in Level 4 | The frozen artifact (eval set, design doc) is timestamped and demonstrably untouched afterwards |
| **The demo** | Could not show it working | Demo worked only on the one input rehearsed | 5 minutes, live, working, including one failure case shown **on purpose** | Handled an unrehearsed question from a stranger, including "I don't know, here's how I'd find out" |
| **The honest section** | Absent, or "it works well" | Lists minor cosmetic limitations | Names real limitations with evidence, and who should not rely on it | Names a limitation that materially undercuts their own headline claim, and reports it anyway |

---

## 📊 Turning Rubrics Into a Number (if you have to)

You mostly shouldn't. But if a school, a portfolio, or a scholarship application needs a score:

| Approach | How | Use when |
|---|---|---|
| **Column count** ✅ preferred | "6 Proficient, 2 Developing" | Almost always. Keeps the specifics visible. |
| **Mean** | 🌱=1, 🌿=2, 🌳=3, ✨=4 → average | A number is genuinely required. **2.75+ is a strong project.** |
| **Percentage** | mean ÷ 4 × 100 | A school demands one. Say out loud that 3/4 = 75% means *"met the standard,"* not *"a C."* |

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  ⚠️  THE PERCENTAGE TRAP                                             │
   │                                                                      │
   │  All-Proficient = 3.0/4.0 = 75%. In school currency that reads as    │
   │  mediocre. In this rubric it is EXCELLENT — the target, met on       │
   │  every dimension.                                                    │
   │                                                                      │
   │  If you must report a percentage, report the column count next to    │
   │  it, and say the sentence out loud: "Proficient is the goal."        │
   └──────────────────────────────────────────────────────────────────────┘
```

**Tracking growth over time** matters far more than any single score. In the [progress tracker](progress-tracker.md), record the column counts. The pattern to look for is not "scores going up" — it's **🌱s disappearing from Row 3 (method) and Row 5 (failure analysis)**, because those two are where real engineering maturity shows up first.

---

## ⚠️ Common Rubric Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| **Using the Level 4 code rubric on a Level 2 learner** | The Level 4 table looks like "real" standards | Each level's table *is* the real standard for that level. A Level 2 learner meeting Level 2 Proficient is doing excellent work. |
| **Scoring alone and delivering a verdict** | Faster, and avoids an awkward conversation | Score together, out loud. The conversation *is* the feedback; the sheet is just its skeleton. |
| **Marking ✨ for effort or volume** | A learner worked really hard and you want to say so | ✨ means *more honest or more rigorous*, never *bigger*. Praise the effort separately and by name. |
| **Giving nine improvements at once** | Every row has something in it | Pick two. Always exactly two. Write them down. Check them next time. |
| **Skipping the self-score** | It takes an extra five minutes | Those five minutes contain the most valuable data you will get all month — especially the rows they over-rate themselves on. |
| **Letting Row 3 (method) slide because the write-up is lovely** | Good communication is very persuasive | Method correctness is a gate. A beautiful report of a leaked score is a worse outcome than an ugly report of an honest one. |
| **Scoring the person** | Rubrics feel like grades and grades feel personal | Every descriptor in this file is a property of an artifact. Read them out as written. |
| **Using ethics rubric rows to enforce your conclusion** | You have opinions and they're probably reasonable | Every row scores the *reasoning*. A learner who disagrees with you at 🌳 across the board has done better work than one who agrees with you at 🌿. |

---

## 🔑 Key Takeaways

- **Proficient (🌳) is the target, not the middle.** All-Proficient is an excellent project. Say so.
- **Score the artifact, with the learner, out loud.** Self-score first; the gaps are the lesson.
- **Pick exactly two rows to improve.** Never nine.
- **Method correctness is a gate.** A leaked score makes every other row meaningless.
- **Use the code rubric for the level you're in.** Age-appropriate standards produce learners who write code; universal standards produce learners who don't.
- **The explanation rubric is the cheapest, highest-information assessment available.** Four minutes, file closed, three follow-up prompts.
- **The ethics rubric scores reasoning, never conclusions.** Disagreeing with you at Proficient beats agreeing with you at Developing.
- **"Not yet" is the phrase.** It is the difference between a learner who continues and one who doesn't.

---

## 📓 Rubric Vocabulary

| Term | What it means here | Example |
|---|---|---|
| **Observable descriptor** | A statement you can verify by looking at the work, not by judging the person | "Every chart has axis labels with units" |
| **Gate row** | A row where 🌱 invalidates the whole artifact regardless of other rows | Project rubric Row 3, Method correctness |
| **Self-score gap** | The difference between the learner's score and yours | Over-rating Row 5 is the most common and most useful gap |
| **Column count** | Reporting "6 Proficient, 2 Developing" rather than a mean | The preferred way to record a score |
| **Frozen artifact** | Something committed before the work it evaluates, and provably untouched | Level 4's eval set, written before the system exists |
| **Steelman (in Row 4)** | The opposing case stated in a form its holders would accept | Not "they just want money" |
| **Not yet** | The phrase that replaces "Beginning" when speaking to the learner | "The baseline isn't here yet" |

---

## ✅ Self-Check: Am I Using These Well?

<details>
<summary><strong>Click to reveal the eight questions</strong></summary>

1. **When did I last mark something 🌱?** Never marking Beginning means the rubric has become a ceremony. Some things genuinely aren't there yet, and saying so kindly is the job.
2. **When did I last mark ✨?** Never marking Exceptional means the learner has no visible ceiling. Look for it specifically in Row 5 (failure analysis) and ethics Row 7.
3. **Did the learner self-score first, this time?** If not, you gave a verdict rather than ran an assessment.
4. **Did I pick exactly two improvements?** Count them. It's usually four.
5. **Did I check last time's two?** If you never check them, the learner learns that rubric feedback is decorative.
6. **Am I using the right level's code rubric?** Look at the heading before you start scoring, every time.
7. **Have I scored an ethics discussion against my own conclusion?** Reread Row 4. If their steelman was better than yours, that's a ✨ regardless of where they landed.
8. **Do the tracker's column counts show 🌱s leaving Rows 3 and 5?** That's the real growth signal. If Row 3 still has 🌱s two levels later, the honesty habit hasn't installed and everything downstream is at risk.

</details>

---

**Next:** [`progress-tracker.md`](progress-tracker.md) — tick every module, capstone and assessment, and collect the badges.

[⬅ Teacher guide](README.md) · [Pacing guide](pacing-guide.md) · [Back to AI Academy](../README.md) · [Curriculum map](../CURRICULUM_MAP.md) · [Progress tracker](progress-tracker.md)
